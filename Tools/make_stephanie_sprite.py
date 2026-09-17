#!/usr/bin/env python3
"""Cut the Qajar course's professor out of her character sheet.

Stephanie arrives as one sheet: a portrait, a five-frame idle, walk cycles in
four directions, a row of expressions and a row of gestures. The course needs
one figure — the resting stance a host wears when a cue has no pose of its own —
and it needs her alone on transparency, so the board behind her stays the board.

The take is the middle figure of the **IDLE (FRONT)** band, cut as its own
connected component: flood-fill from a seed inside the figure, keep only the
pixels that come back. A plain rectangle crop would drag in the shoulder of the
woman beside her, because the five are pitched close enough that their bounding
boxes overlap.

Nothing keys the background. The sheet ships with a real alpha channel — the
corners are (0,0,0,0) — but the figure stands on a painted brown gradient that
belongs to the sheet and not to her, so the mask is what stands between her and
a brown rectangle on a black stage. A colour key could not have done this: her
hair is the same value as the floor under it.

    python3 Tools/make_stephanie_sprite.py [--course qajars]

Writes Web/courses/<course>/assets/sprite-stephanie.png.
Deterministic: no randomness, no network, so a rebuild is byte-identical.
"""

import argparse
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHEET = os.path.join(ROOT, 'Designs to Base Everything On',
                     'stephanie-cronin-sheet.png')

BAND = (300, 800, 54, 230)   # x0, x1, y0, y1 -- the IDLE (FRONT) row alone,
                             # measured off the master; the label sits above it
                             # and the next band's heads below
ALPHA_FLOOR = 110            # a real pixel, not an anti-aliased fringe
EXPECTED_FIGURES = 5
TAKE = 2                     # the middle of the five, counting from the left
PAD = 10


def components(px, x0, x1, y0, y1):
    """Every opaque figure in the band, as (bbox, seed), left to right.

    A plain flood fill, four-connected, at a two-pixel stride: the sheet is
    soft-edged art, so a stride loses nothing the bbox needs — the exact mask is
    filled in later at full resolution, from the seed this returns.
    """
    s = 2
    gw, gh = (x1 - x0 + s - 1) // s, (y1 - y0 + s - 1) // s
    seen = bytearray(gw * gh)
    solid = bytearray(gw * gh)
    for j in range(gh):
        yy = y0 + j * s
        for i in range(gw):
            hit = 0
            for dy in range(s):
                for dx in range(s):
                    x = x0 + i * s + dx
                    if x < x1 and yy + dy <= y1 and px[x, yy + dy] > ALPHA_FLOOR:
                        hit += 1
            if hit >= 2:
                solid[j * gw + i] = 1

    found = []
    for start in range(gw * gh):
        if not solid[start] or seen[start]:
            continue
        seen[start] = 1
        stack = [start]
        minx = maxx = start % gw
        miny = maxy = start // gw
        count = 0
        while stack:
            p = stack.pop()
            count += 1
            i, j = p % gw, p // gw
            if i < minx: minx = i
            if i > maxx: maxx = i
            if j < miny: miny = j
            if j > maxy: maxy = j
            for n in (p - 1, p + 1, p - gw, p + gw):
                if not (0 <= n < gw * gh) or seen[n] or not solid[n]:
                    continue
                di, dj = n % gw - i, n // gw - j
                if abs(di) + abs(dj) != 1:
                    continue
                seen[n] = 1
                stack.append(n)
        if count < 400:                     # a fleck, not a figure
            continue
        bbox = (x0 + minx * s, x0 + maxx * s + 1, y0 + miny * s, y0 + maxy * s + 1)
        seed = (x0 + (minx + maxx) * s // 2, y0 + (miny + maxy) * s // 2)
        found.append((bbox, seed))
    found.sort(key=lambda f: f[0][0])
    return found


def figure_mask(px, seed, bbox):
    """The chosen figure alone, full resolution, as a byte mask.

    This is the step that drops the neighbour: flood from inside the figure and
    keep only what comes back, so an overlapping bounding box cannot smuggle in
    a sliver of the pose next door.
    """
    x0, y0 = bbox[0], bbox[2]
    w, h = bbox[1] - x0, bbox[3] - y0
    mask = bytearray(w * h)
    sx, sy = seed
    if px[sx, sy] <= ALPHA_FLOOR:                  # seed fell in a gap
        sx = sy = None
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                if px[xx, yy] > ALPHA_FLOOR:
                    sx, sy = xx, yy
                    break
            if sx is not None:
                break
        if sx is None:
            sys.exit('the chosen figure has no opaque pixel in its own box')

    stack = [(sx, sy)]
    mask[(sx - x0) + (sy - y0) * w] = 1
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (x0 <= nx < x0 + w and y0 <= ny < y0 + h):
                continue
            k = (nx - x0) + (ny - y0) * w
            if mask[k] or px[nx, ny] <= ALPHA_FLOOR:
                continue
            mask[k] = 1
            stack.append((nx, ny))
    return mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--course', default='qajars',
                    help='which course folder the sprite lands in; the sheet '
                         'is one sheet, and she teaches more than one course')
    args = ap.parse_args()
    out = os.path.join(ROOT, 'Web', 'courses', args.course, 'assets',
                       'sprite-stephanie.png')

    if not os.path.exists(SHEET):
        sys.exit('missing master: %s' % os.path.relpath(SHEET, ROOT))

    sheet = Image.open(SHEET).convert('RGBA')
    px = sheet.getchannel('A').load()
    found = components(px, *BAND)

    if len(found) != EXPECTED_FIGURES:
        sys.exit('expected %d figures in the idle band, found %d — the master '
                 'has changed; re-pick the take before shipping'
                 % (EXPECTED_FIGURES, len(found)))

    bbox, seed = found[TAKE]
    x0, y0, x1, y1 = bbox[0], bbox[2], bbox[1], bbox[3]
    mask = figure_mask(px, seed, bbox)

    win = sheet.crop((x0, y0, x1, y1))
    alpha = win.getchannel('A')
    ap = alpha.load()
    for y in range(win.height):
        for x in range(win.width):
            if not mask[x + y * win.width]:
                ap[x, y] = 0
    win.putalpha(alpha)

    canvas = Image.new('RGBA', (win.width + PAD * 2, y1 - y0), (0, 0, 0, 0))
    canvas.alpha_composite(win, (PAD, 0))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, 'PNG', optimize=True)
    print('%s  box %s  %dx%d  %d bytes'
          % (os.path.relpath(out, ROOT), bbox, canvas.width, canvas.height,
             os.path.getsize(out)))


if __name__ == '__main__':
    main()
