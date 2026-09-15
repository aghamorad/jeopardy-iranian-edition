#!/usr/bin/env python3
"""Draw the edition tiles the splash shelf shows.

The shelf crops its art into a 40–46px square, so the tile is not a card and must
not be laid out like one: a mark has to survive a ten-fold reduction and read at
a glance. What survives that reduction is silhouette and colour, not line. So the
pair is built from one grammar: a near-black plate, and the show's tricolour rule
as the constant. `general` is the rule alone, which is the flag the app prints on
every screen, and it is the brightest thing in its own frame.

`course` is not drawn at all. It is the Iran in World Politics course's own
splash mural, cropped square onto the middle of the wall it paints. Every circle
on the front door wears art from its own source, and the mural is that course's
own source — the room the student walks into. It is cut down to a tile rather
than pointed at directly because the mural ships at 2.3MB and a 118px circle is
not going to make a phone fetch that before the student has chosen anything.

Two more marks stand in for courses that are not written yet, and they answer the
same brief: one silhouette that survives the reduction, taken from the syllabus
rather than from the period's furniture. `qajar` is a qalyan and `pahlavi` is an
oil derrick. They are placeholders on the front door, so they carry no words —
the COMING SOON stamp is HTML, over the top of them, and so is the period's name.
What the art has to do is tell the two apart at a glance from across the room,
and a water pipe and a derrick are a century apart in silhouette.

Neither is a royal emblem, which the first cut had them be. The crown that came
before was drawn from general Qajar imagery and read as a bell; the derrick was
drawn the same way and got lucky. The rule now is that a mark stands for a week
of the actual syllabus: the qalyan is the Tobacco Protest, week five of eight,
and the derrick is Musaddiq and the nationalization of oil, week four.

The two placeholders are the one pair on the shelf that does **not** carry the
rule in its art. They did, first cut, as a plinth at the foot — and it had to go,
because a placeholder carries three things where a door carries two: the mark, the
stamp, and the rule. A round frame 118px across has room for two of them. The
first composition kept all three and lost the argument on screen: the stamp sat
centred on the mark and the mark read as a smudge under a label. So the mark takes
the upper half of the frame and the stamp takes the foot, and the rule moved onto
the stamp itself — the plate is banded with it in CSS, so the flag is still in
every frame on the shelf and the mark is still a mark.

    python3 Tools/make_edition_tiles.py

Writes Web/assets/tile-general.png, the two placeholders under Web/assets/, and
the Iran in World Politics course's own tile inside its folder under Web/courses/.
Deterministic: no randomness, no network, so a rebuild is byte-identical — the
course tile included, since resampling a fixed crop is as reproducible as drawing.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERAL_OUT = os.path.join(ROOT, 'Web', 'assets', 'tile-general.png')
COURSE_OUT = os.path.join(
    ROOT, 'Web', 'courses', 'iran-in-world-politics', 'assets', 'tile-course.png')
SOON_OUT = {
    'qajars': os.path.join(ROOT, 'Web', 'assets', 'soon-qajars.png'),
    'pahlavis': os.path.join(ROOT, 'Web', 'assets', 'soon-pahlavis.png'),
}

# The course's own splash mural, and the square of it the circle wears. The crop
# is the middle of the painted wall: the dome between its two minarets, the snow
# peak over it, the flag's emblem at the centre, and the top of the crowd at the
# foot. It stops above the skirting, because below that is a dark floor with a
# reflection on it and a circle of floor says nothing.
COURSE_SPLASH = os.path.join(
    ROOT, 'Web', 'courses', 'iran-in-world-politics', 'assets',
    'stage-backdrop-course.png')
COURSE_CROP = (488, 170, 1048, 730)

SIZE = 512          # what ships
SS = 3              # supersample factor: drawn 3x, reduced once
N = SIZE * SS

DOME_STEPS = 24     # segments on a mark's quarter-arc; below ~16 the arc facets
HOSE_STEPS = 28     # segments on the qalyan's hose; it is drawn as a polyline

PLATE_EDGE = (5, 5, 6)
PLATE_LIFT = (30, 38, 34)       # the soft wash behind the mark, at its head
PLATE_FOOT = (14, 16, 15)       # the same wash at its foot: dark, never the void
RULE_SHADOW = (0, 0, 0)

GREEN = (23, 178, 90)
BONE = (242, 239, 233)
RED = (224, 32, 32)

# A mark's interior: a lift kept far below the rule's value, so the face reads as
# turned toward the light without ever becoming a second bright shape. The lift
# has to clear the plate's own wash — a face drawn at the plate's value is a hole,
# and the rim then reads as an empty frame rather than as a solid mark.
FACE_HI = (48, 48, 52)
FACE_LO = (16, 16, 19)


def plate(n):
    """Near-black, with a soft lift so the mark is not floating on a void.

    Full-bleed, and it has to be. The frame crops this square into a circle, so a
    wash that dies before the tile's edge leaves the sphere dark well inside its
    own rim: the glass then reads at the diameter of the wash rather than at the
    diameter of the frame, and a placeholder on the shelf sits visibly smaller
    than the course beside it. The first cut drew the lift as an ellipse across
    6%–94% and that is exactly what it did — 88px of frame reading as 65px of
    globe, next to a course tile that is a photograph and fills all 88.

    The corners are off-screen under that crop, so the ground runs to the tile's
    edge and the only falloff is the lamp: the same top-down lighting `lit_body`
    draws every filled mark with, so a plate is lit like the mark standing on it.

    The foot stays above `PLATE_EDGE` — a wash that reaches the plate's own value
    before the rim cuts the sphere in half, and a hemisphere is not a globe.
    """
    column = Image.new('L', (1, n))
    for i in range(n):
        column.putpixel((0, i), int(255 * (1.0 - i / float(n - 1))))
    ground = Image.composite(
        Image.new('RGB', (n, n), PLATE_LIFT),
        Image.new('RGB', (n, n), PLATE_FOOT),
        column.resize((n, n)))

    circle = Image.new('L', (n, n), 0)
    ImageDraw.Draw(circle).ellipse([0, 0, n - 1, n - 1], fill=255)
    circle = circle.filter(ImageFilter.GaussianBlur(n * 0.03))
    return Image.composite(ground, Image.new('RGB', (n, n), PLATE_EDGE), circle)


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


def lit_body(w, h):
    """The face a mark is filled with: near-black, lit from above.

    One gradient, shared by every filled mark on the shelf, so a qalyan and a
    derrick are lit by the same lamp. H kept below the rule's value — a face drawn
    at the rule's own brightness competes with the flag, which is the one thing in
    the frame allowed to be the brightest.
    """
    column = Image.new('L', (1, h))
    for i in range(h):
        column.putpixel((0, i), int(255 * i / (h - 1)))
    return Image.composite(
        Image.new('RGB', (w, h), FACE_HI),
        Image.new('RGB', (w, h), FACE_LO),
        column.resize((w, h)))


def contour(img, pts, width):
    """A closed mark: a lit face inside a bone rim.

    The face is filled before the rim goes on, so the rim has an edge to sit on
    rather than a void — the same order the globe is drawn in. One polygon, not a
    stack of primitives: a stack leaks its seams into the mark when the reduction
    lands, and at 88px the seam is the whole reading.
    """
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    img.paste(lit_body(img.size[0], img.size[1]), (0, 0), mask)
    ImageDraw.Draw(img).line(list(pts) + [pts[0]], fill=BONE, width=width,
                             joint='curve')


def qalyan(img, cx, cy, h):
    """The qalyan: the Qajar mark, for the Tobacco Protest.

    The mark that stood here was a Kiani crown, drawn from the period's furniture
    rather than from the course, and it read as a bell — a dome running straight
    into a skirt with two stubs either side. There is no room to argue with that
    at 118px, so the mark changed to one the syllabus actually names: the tobacco
    protest is week five of eight, and a water pipe is what everyone pictures.
    The Qajar dynasty's own emblems are a lion and a sun, which at this size is a
    smudge whichever way it is drawn.

    The head, the stem and the jar are one contour, for the reason the crown's
    one polygon was: a stack of primitives leaks its seams into the mark when the
    reduction lands. The jar is sampled as two arcs on the same construction, so
    the bulb rounds off gracefully instead of faceting into a hexagon.

    The hose is the whole of the reading. A bulb on a stem is a vase, and it is a
    vase that a teapot is one bad spout away from — so the hose leaves the stem
    high, sweeps out to one side and hangs, and it is stroked rather than filled,
    because a second contour would paste its face over the stem's rim and cut the
    rim open. It is drawn last and it is the widest line on the tile for the same
    reason the derrick's legs are not: it has to survive the reduction on its own.
    """
    top = cy - h * 0.50

    hr = h * 0.084          # half-width at the head's rim
    hb = h * 0.036          # half-width where the head meets the stem
    head_bot = top + h * 0.135

    sw = h * 0.028          # the stem's half-width

    jneck = top + h * 0.400
    jnw = h * 0.058         # where the stem enters the jar
    jwide = top + h * 0.700
    jwid = h * 0.205        # the jar at its widest
    jfoot = top + h * 0.945
    jfw = h * 0.090         # the foot's shoulder
    jbot = top + h * 1.000
    jbw = h * 0.078         # the base it stands on

    pts = [(cx - hr, top), (cx - hb, head_bot), (cx - sw, head_bot),
           (cx - sw, jneck), (cx - jnw, jneck)]

    for step in range(1, DOME_STEPS + 1):
        a = math.pi * 0.5 * step / DOME_STEPS
        pts.append((cx - jnw - (jwid - jnw) * math.sin(a),
                    jneck + (jwide - jneck) * (1 - math.cos(a))))

    for step in range(1, DOME_STEPS + 1):
        a = math.pi * 0.5 * step / DOME_STEPS
        pts.append((cx - jfw - (jwid - jfw) * math.cos(a),
                    jwide + (jfoot - jwide) * math.sin(a)))

    pts += [(cx - jbw, jbot), (cx + jbw, jbot), (cx + jfw, jfoot)]

    for step in range(DOME_STEPS, 0, -1):
        a = math.pi * 0.5 * step / DOME_STEPS
        pts.append((cx + jfw + (jwid - jfw) * math.cos(a),
                    jwide + (jfoot - jwide) * math.sin(a)))

    for step in range(DOME_STEPS, 0, -1):
        a = math.pi * 0.5 * step / DOME_STEPS
        pts.append((cx + jnw + (jwid - jnw) * math.sin(a),
                    jneck + (jwide - jneck) * (1 - math.cos(a))))

    pts += [(cx + sw, jneck), (cx + sw, head_bot), (cx + hb, head_bot),
            (cx + hr, top)]

    contour(img, pts, max(4, int(N * 0.022)))

    # Out and down in one sweep, ending below the jar's shoulder so the eye reads
    # a pipe that hangs rather than a spout that pours.
    d = ImageDraw.Draw(img)
    w = max(4, int(N * 0.034))
    ax, ay = cx + sw, top + h * 0.250
    hose = []
    for step in range(HOSE_STEPS + 1):
        t = step / float(HOSE_STEPS)
        a = t * math.pi * 0.60
        hose.append((ax + h * 0.400 * math.sin(a),
                     ay + h * 0.520 * (1 - math.cos(a))))
    d.line(hose, fill=BONE, width=w, joint='curve')

    # The mouthpiece: the hose ends in a hard little tip, which is the last thing
    # separating it from a loop of wire.
    d.ellipse([hose[-1][0] - w * 0.95, hose[-1][1] - w * 0.95,
               hose[-1][0] + w * 0.95, hose[-1][1] + w * 0.95], fill=BONE)


def derrick(img, cx, cy, h):
    """The oil derrick: the Pahlavi mark.

    Left as an open lattice, and drawn with strokes rather than filled, because a
    solid tower is a black wedge at 88px and says nothing. Three rungs and one
    cross-brace: enough panels to read as a frame, few enough that the reduction
    does not close them into lint. The sill is wider than the legs and that
    overhang is what separates a derrick from a ladder.
    """
    d = ImageDraw.Draw(img)
    w = max(4, int(N * 0.022))

    top = cy - h * 0.50
    bot = cy + h * 0.50
    t_top = top + h * 0.082     # the tower's apex, under the crown block
    tw = h * 0.085              # half-width at the crown
    bw = h * 0.235              # half-width at the sill

    def half_at(t):
        return tw + (bw - tw) * t

    for side in (-1, 1):
        d.line([(cx + side * tw, t_top), (cx + side * bw, bot)],
               fill=BONE, width=w)

    for t in (0.30, 0.58, 0.86):
        hw = half_at(t)
        y = t_top + (bot - t_top) * t
        d.line([(cx - hw, y), (cx + hw, y)], fill=BONE, width=w)

    d.line([(cx - bw * 1.20, bot), (cx + bw * 1.20, bot)], fill=BONE, width=w)

    h0 = half_at(0.58)
    h1 = half_at(0.86)
    y0 = t_top + (bot - t_top) * 0.58
    y1 = t_top + (bot - t_top) * 0.86
    d.line([(cx - h0, y0), (cx + h1, y1)], fill=BONE, width=w)
    d.line([(cx + h0, y0), (cx - h1, y1)], fill=BONE, width=w)

    d.rectangle([cx - h * 0.105, top, cx + h * 0.105, t_top],
                outline=BONE, width=w)


def general():
    img = plate(N)
    paste_rule(img, N / 2, N / 2, N * 0.60, N * 0.185)
    return img


def course():
    """The course's own splash mural, square onto the middle of its wall.

    Not drawn, and not the globe that was here. A circle on this shelf wears the
    art of the thing it opens, and the thing this one opens is a room with that
    mural painted down one side of it. The flag is already in the picture, which
    is why no rule is pasted over the top — the source carries its own.
    """
    src = Image.open(COURSE_SPLASH).convert('RGB').crop(COURSE_CROP)
    return src.resize((N, N), Image.LANCZOS)


def qajars():
    """The qalyan, high in the frame, over an empty foot.

    The foot is left empty on purpose: the COMING SOON plate is placed there in
    CSS, and a mark that runs down into it is a mark with a label across its face.
    The mark is sized off its own half, so it clears the plate rather than being
    cropped by it — see the module docstring for why the rule left this tile.
    """
    img = plate(N)
    h = N * 0.420
    # Left of centre by half the hose's reach, so the silhouette is centred even
    # though the jar — the mass — is not.
    qalyan(img, N / 2 - h * 0.115, N * 0.295, h)
    return img


def pahlavis():
    """The derrick, composed as the crown is."""
    img = plate(N)
    derrick(img, N / 2, N * 0.295, N * 0.420)
    return img


def write(img, path):
    out = img.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, 'PNG', optimize=True)
    return out


def main():
    for name, fn, path in (('general', general, GENERAL_OUT),
                           ('iran-in-world-politics', course, COURSE_OUT),
                           ('qajars', qajars, SOON_OUT['qajars']),
                           ('pahlavis', pahlavis, SOON_OUT['pahlavis'])):
        out = write(fn(), path)
        print('%-22s %s  %dx%d  %d bytes'
              % (name, os.path.relpath(path, ROOT), out.width, out.height,
                 os.path.getsize(path)))


if __name__ == '__main__':
    main()
