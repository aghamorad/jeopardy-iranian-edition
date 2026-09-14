#!/usr/bin/env python3
"""Cut the MAIN edition's host out of her character sheet.

Tannaz Deadband arrives as one sheet: three rows of the same figure — ten
full-body poses, ten busts, nine at the lectern. The game needs five, and it
needs them to look like one character rather than five. So every sprite is cut
from the **first row**, the full-body set, at a single shared vertical window:
head to upper thigh, the framing the course's professor already wears. Cutting
the five at one window is what keeps her the same size and shape on every
screen; taking a bust from the second row for one of them would have her change
build the moment an answer lands.

The five are chosen for the register the host speaks in — presenting, smug,
shrugging, thinking, making a point — not for variety:

    greeting  the open palm, arm out. She is showing you the show.
    right     arms crossed, smirking. She is not impressed that you knew.
    wrong     both palms up, brows raised. Well. What can you do.
    timeout   hand to the chin, looking away. Thinking about your chances.
    final     one finger up. Pay attention, this one is for the money.

**Nothing keys the background.** The sheet ships with a real alpha channel —
the corners are (0,0,0,0), not a black matte — so there is no backdrop to
flood-fill and no risk of eating the dark trousers, which is the trap a
luminance threshold would have set. What the alpha *cannot* stop is a
neighbour: the figures are pitched close enough that their bounding boxes
overlap, so a plain rectangle crop drags in a corner of the woman beside her.
Each sprite is therefore cut as its **own connected component** — flood-fill
from a seed inside the figure, keep only the pixels that come back — and pasted
onto a shared canvas at a shared width. That is what makes the five crops
interchangeable instead of five pictures that happen to be near each other.

The sheet is row-major art, and this reads exactly the ten components of the
first row. If the master is ever re-exported with a figure added or a row
re-pitched the component count moves and the tool stops rather than shipping
five wrong women.

    python3 Tools/make_host_sprites.py

Writes Web/assets/host/tannaz-<pose>.png.
Deterministic: no randomness, no network, so a rebuild is byte-identical.
"""

import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHEET = os.path.join(ROOT, 'Designs to Base Everything On',
                     'tannaz-deadband-sheet.png')
OUT_DIR = os.path.join(ROOT, 'Web', 'assets', 'host')

ROW1 = (16, 409)          # the full-body band, measured off the master
ALPHA_FLOOR = 110         # a real pixel, not an anti-aliased fringe

CROP_TOP = 14             # one window for all five, so they share a scale and a
CROP_H = 280              # hairline: top of the head down to the upper thigh
PAD = 10

# Slot -> which figure of the first row it is, counting from the left.
POSES = (
    ('greeting', 4),
    ('right',    7),
    ('wrong',    6),
    ('timeout',  2),
    ('final',    8),
)

EXPECTED_FIGURES = 10


def components(px, w, y0, y1):
    """Every opaque figure in the band, as (seed, bbox), left to right.

    A plain flood fill, four-connected, at a two-pixel stride: the sheet is
    soft-edged art, so a stride loses nothing that the bbox needs — the exact
    mask is filled in later at full resolution, from the seed this returns.
    """
    s = 2
    gw, gh = (w + s - 1) // s, ((y1 - y0) + s - 1) // s
    seen = bytearray(gw * gh)
    solid = bytearray(gw * gh)
    for j in range(gh):
        yy = y0 + j * s
        for i in range(gw):
            hit = 0
            for dy in range(s):
                for dx in range(s):
                    x = i * s + dx
                    if x < w and yy + dy <= y1 and px[x, yy + dy] > ALPHA_FLOOR:
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
            if i > 0 and solid[p - 1] and not seen[p - 1]:
                seen[p - 1] = 1
                stack.append(p - 1)
            if i < gw - 1 and solid[p + 1] and not seen[p + 1]:
                seen[p + 1] = 1
                stack.append(p + 1)
            if j > 0 and solid[p - gw] and not seen[p - gw]:
                seen[p - gw] = 1
                stack.append(p - gw)
            if j < gh - 1 and solid[p + gw] and not seen[p + gw]:
                seen[p + gw] = 1
                stack.append(p + gw)
        if count < 400:                     # a fleck, not a figure
            continue
        found.append(((minx * s, maxx * s + 1, y0 + miny * s, y0 + maxy * s + 1),
                      ((minx + maxx) * s // 2, (miny + maxy) * s // 2 + y0)))
    found.sort(key=lambda f: f[0][0])
    return found


def figure_mask(px, seed, bbox):
    """The chosen figure alone, full resolution, as a byte mask.

    This is the step that drops the neighbour: flood from inside the figure and
    keep only what comes back, so an overlapping bounding box cannot smuggle in
    a sliver of the pose next door.
    """
    x0, x1, y0, y1 = bbox
    mask = bytearray((x1 - x0) * (y1 - y0))
    sx, sy = seed
    if not px[sx, sy] > ALPHA_FLOOR:                  # seed fell in a gap
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                if px[xx, yy] > ALPHA_FLOOR:
                    sx, sy = xx, yy
                    break
            else:
                continue
            break

    def at(x, y):
        return (x - x0) + (y - y0) * (x1 - x0)

    stack = [(sx, sy)]
    mask[at(sx, sy)] = 1
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (x0 <= nx < x1 and y0 <= ny < y1):
                continue
            k = at(nx, ny)
            if mask[k] or px[nx, ny] <= ALPHA_FLOOR:
                continue
            mask[k] = 1
            stack.append((nx, ny))
    return mask


def cut(sheet, px, bbox, seed):
    """One sprite: the figure, in the shared window, on transparency."""
    x0, x1, _, _ = bbox
    mask = figure_mask(px, seed, bbox)

    win = sheet.crop((x0, CROP_TOP, x1, CROP_TOP + CROP_H))
    sw = x1 - x0
    alpha = win.getchannel('A')
    ap = alpha.load()

    def belongs(x, y):
        """Is sheet pixel (x, y) part of this figure?"""
        ry = y - bbox[2]
        if not (0 <= ry < bbox[3] - bbox[2]):
            return False
        return bool(mask[(x - x0) + ry * sw])

    for y in range(win.height):
        for x in range(win.width):
            if not belongs(x0 + x, CROP_TOP + y):
                ap[x, y] = 0
    win.putalpha(alpha)
    return win


def main():
    if not os.path.exists(SHEET):
        sys.exit('missing master: %s' % os.path.relpath(SHEET, ROOT))

    sheet = Image.open(SHEET).convert('RGBA')
    px = sheet.getchannel('A').load()
    found = components(px, sheet.width, *ROW1)

    if len(found) != EXPECTED_FIGURES:
        sys.exit('expected %d figures in the first row, found %d — the master '
                 'has changed; re-pick the poses before shipping'
                 % (EXPECTED_FIGURES, len(found)))

    boxes = [f[0] for f in found]
    canvas_w = max(b[1] - b[0] for b in boxes) + PAD * 2
    canvas_h = CROP_H

    os.makedirs(OUT_DIR, exist_ok=True)
    for slot, idx in POSES:
        bbox, seed = found[idx]
        sprite = cut(sheet, px, bbox, seed)

        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        cx = (canvas_w - sprite.width) // 2
        canvas.alpha_composite(sprite, (cx, 0))

        path = os.path.join(OUT_DIR, 'tannaz-%s.png' % slot)
        canvas.save(path, 'PNG', optimize=True)
        print('%-9s <- figure %2d  %s  %dx%d  %d bytes'
              % (slot, idx + 1, os.path.relpath(path, ROOT),
                 canvas.width, canvas.height, os.path.getsize(path)))


if __name__ == '__main__':
    main()
