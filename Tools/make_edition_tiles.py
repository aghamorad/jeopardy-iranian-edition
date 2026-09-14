#!/usr/bin/env python3
"""Draw the edition tiles the splash shelf shows.

The shelf crops its art into a 40–46px square, so the tile is not a card and must
not be laid out like one: a mark has to survive a ten-fold reduction and read at
a glance. What survives that reduction is silhouette and colour, not line. So the
pair is built from one grammar: a near-black plate, and the show's tricolour rule
as the constant. `general` is the rule alone, which is the flag the app prints on
every screen, and it is the brightest thing in its own frame.

`course` sets the same rule across the face of a globe. The globe is a bone rim
on a near-black interior, not a filled pale body: a pale sphere was the first cut
and it lost at the size that matters, where it is a grey mass the rule has to
fight, and the meridian drawn to say "globe" at full size survives the reduction
as a stray oval instead of as geography. A rim keeps the flag the brightest thing
in the frame — the property the general tile has — and the circle alone carries
the reading at every size.

    python3 Tools/make_edition_tiles.py

Writes Web/assets/tile-general.png, and the Iran in World Politics course's own
tile inside its folder under Web/courses/.
Deterministic: no randomness, no network, so a rebuild is byte-identical.
"""

import os

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERAL_OUT = os.path.join(ROOT, 'Web', 'assets', 'tile-general.png')
COURSE_OUT = os.path.join(
    ROOT, 'Web', 'courses', 'iran-in-world-politics', 'assets', 'tile-course.png')

SIZE = 512          # what ships
SS = 3              # supersample factor: drawn 3x, reduced once
N = SIZE * SS

PLATE_EDGE = (5, 5, 6)
PLATE_LIFT = (30, 38, 34)       # the soft wash behind the mark
RULE_SHADOW = (0, 0, 0)

GREEN = (23, 178, 90)
BONE = (242, 239, 233)
RED = (224, 32, 32)

# The globe's interior: a lift kept far below the rule's value, so the disc reads
# as a face turned toward the light without ever becoming a second bright shape.
# The lift has to clear the plate's own wash — a face drawn at the plate's value is
# a hole, and the ring then reads as an empty frame rather than as a globe.
GLOBE_HI = (48, 48, 52)
GLOBE_LO = (16, 16, 19)


def plate(n):
    """Near-black, with a soft lift so the mark is not floating on a void."""
    img = Image.new('RGB', (n, n), PLATE_EDGE)

    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).ellipse(
        [n * 0.06, n * 0.06, n * 0.94, n * 0.94], fill=190)
    mask = mask.filter(ImageFilter.GaussianBlur(n * 0.10))

    return Image.composite(Image.new('RGB', (n, n), PLATE_LIFT), img, mask)


def tricolour(width, height, radius):
    """The flag rule the app prints everywhere: equal flat thirds.

    Drawn as one rounded slab with the bands clipped into it, so the ends are
    round and the band joins are square — three separate rounded bands would
    scallop the middle of the rule.
    """
    slab = Image.new('RGB', (int(width), int(height)), BONE)
    d = ImageDraw.Draw(slab)
    third = height / 3.0
    d.rectangle([0, 0, width, third], fill=GREEN)
    d.rectangle([0, height - third, width, height], fill=RED)

    mask = Image.new('L', (int(width), int(height)), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, width - 1, height - 1], radius=radius, fill=255)
    slab.putalpha(mask)
    return slab


def paste_rule(img, cx, cy, width, height):
    """The rule, with a soft drop shadow so it sits on the plate rather than in it."""
    slab = tricolour(width, height, height / 2)

    shadow = Image.new('L', img.size, 0)
    shadow.paste(slab.getchannel('A'),
                 (int(cx - width / 2), int(cy - height / 2 + height * 0.35)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(height * 0.30))
    img.paste(Image.new('RGB', img.size, RULE_SHADOW), (0, 0), shadow)

    img.paste(slab, (int(cx - width / 2), int(cy - height / 2)), slab)


def globe(img, cx, cy, r):
    """The globe's face: near-black, lit from above, ringed in bone.

    Two passes, not one. The fill goes down first so the rim has something to sit
    against, and the rim is drawn as a stroke of a fixed proportion of the canvas
    rather than of the radius — the rim is the whole of the mark at chip size and
    must not thin out when a course wants a smaller globe.
    """
    d = int(2 * r)
    column = Image.new('L', (1, d))
    for i in range(d):
        column.putpixel((0, i), int(255 * i / (d - 1)))
    body = Image.composite(
        Image.new('RGB', (d, d), GLOBE_HI),
        Image.new('RGB', (d, d), GLOBE_LO),
        column.resize((d, d)))

    mask = Image.new('L', (d, d), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
    img.paste(body, (int(cx - r), int(cy - r)), mask)

    ImageDraw.Draw(img).ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        outline=BONE, width=max(4, int(N * 0.019)))


def general():
    img = plate(N)
    paste_rule(img, N / 2, N / 2, N * 0.60, N * 0.185)
    return img


def course():
    img = plate(N)
    r = N * 0.285
    cx = cy = N / 2

    globe(img, cx, cy, r)

    # The rule crosses the face as a band on the globe. It stops inside the rim, so
    # the circle is never struck clean through — a bar that meets the rim at both
    # ends reads as a prohibition sign, not as a country.
    paste_rule(img, cx, cy, r * 1.62, N * 0.20)
    return img


def write(img, path):
    out = img.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, 'PNG', optimize=True)
    return out


def main():
    for name, fn, path in (('general', general, GENERAL_OUT),
                           ('iran-in-world-politics', course, COURSE_OUT)):
        out = write(fn(), path)
        print('%-22s %s  %dx%d  %d bytes'
              % (name, os.path.relpath(path, ROOT), out.width, out.height,
                 os.path.getsize(path)))


if __name__ == '__main__':
    main()
