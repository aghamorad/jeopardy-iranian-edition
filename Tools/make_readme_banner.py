#!/usr/bin/env python3
"""Build the banner the README leads with.

    /Users/Morad/Claude/Madavi/.depth/venv/bin/python Tools/make_readme_banner.py

Writes `.github/assets/logo-wordmark-banner.png`.

Why this exists rather than the README pointing at `Web/assets/logo-wordmark.png`:
that file is white lettering on transparency, which is correct on the show's own
near-black stage and invisible on GitHub's light theme. Dropping it into a README
unmodified gives you the game's wordmark for half the audience and a blank gap for
the other half. So the wordmark is composited onto the room colour — the same
`#050505` the stage sits on — and the result is a dark plate in either theme, which
is what the game actually looks like.

The system `python3` on this machine has no Pillow; the venv above does. Same as
`Tools/make_edition_tiles.py`.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Web" / "assets" / "logo-wordmark.png"
OUT = ROOT / ".github" / "assets" / "logo-wordmark-banner.png"

ROOM = (5, 5, 5)      # --stage, the colour the show itself sits on
WIDTH = 1600          # README renders ~880 wide; this is headroom for retina
PAD_X = 0.055         # of the output width, each side
PAD_Y = 0.075         # of the output height, each end


def main() -> None:
    logo = Image.open(SRC).convert("RGBA")

    inner_w = WIDTH - 2 * round(WIDTH * PAD_X)
    inner_h = round(logo.height * inner_w / logo.width)
    logo = logo.resize((inner_w, inner_h), Image.LANCZOS)

    plate_h = inner_h + 2 * round(inner_h * PAD_Y)
    plate = Image.new("RGBA", (WIDTH, plate_h), ROOM + (255,))
    plate.alpha_composite(logo, ((WIDTH - inner_w) // 2, (plate_h - inner_h) // 2))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    plate.convert("RGB").save(OUT, optimize=True)
    print(f"{OUT.relative_to(ROOT)} {plate.width}x{plate.height} "
          f"{OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
