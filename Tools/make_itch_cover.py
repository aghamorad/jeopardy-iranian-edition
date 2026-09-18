#!/usr/bin/env python3
"""Build the cover image itch.io wants.

    /Users/Morad/Claude/Madavi/.depth/venv/bin/python Tools/make_itch_cover.py

Writes `.github/assets/itch-cover.png` at 1260x1000, which is 2x the 630x500
frame itch renders a cover in.

Same art as the banner, `Web/assets/logo-wordmark.png` — the show's one lockup.
The two files differ only in shape. A README is wide, so the banner comes out
1600x561, near the lockup's own 2.9:1 and barely padded. A cover is 1.26:1, so
the banner dropped into the dashboard would be cropped to its middle and lose the
first and last letters of JEOPARDY!. Hence a plate built for the frame instead.

Composited on the room colour for the same reason the banner is: the lockup is
lettering and statuary on transparency, and on the light half of a
store grid the picture would be missing and the words floating. See
`make_readme_banner.py` for the system-python-has-no-Pillow note.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Web" / "assets" / "logo-wordmark.png"
OUT = ROOT / ".github" / "assets" / "itch-cover.png"

ROOM = (5, 5, 5)      # --stage, the colour the show itself sits on
WIDTH = 1260          # itch renders 630x500; this is 2x for retina
HEIGHT = 1000
FILL = 0.92           # of the output width, after the art is trimmed


def main() -> None:
    logo = Image.open(SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())

    inner_w = round(WIDTH * FILL)
    inner_h = round(logo.height * inner_w / logo.width)
    logo = logo.resize((inner_w, inner_h), Image.LANCZOS)

    plate = Image.new("RGBA", (WIDTH, HEIGHT), ROOM + (255,))
    plate.alpha_composite(logo, ((WIDTH - inner_w) // 2, (HEIGHT - inner_h) // 2))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    plate.convert("RGB").save(OUT, optimize=True)
    print(f"{OUT.relative_to(ROOT)} {plate.width}x{plate.height} "
          f"{OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
