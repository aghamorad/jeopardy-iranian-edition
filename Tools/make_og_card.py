#!/usr/bin/env python3
"""Build the social share card.

    python3 Tools/make_og_card.py

Writes `Web/assets/og.jpg` at 1200x630, the size every unfurler crops to.
`Web/index.html` points `og:image` at exactly this path, so the name is
load-bearing.

The card is the stage the front door already opens on — `stage-backdrop.png`,
the green-lit and red-lit walls around the Tehran skyline — with the show's
lockup laid across the skyline band, which is where the show itself puts it.
Composited rather than cropped because the lockup is 2.9:1 and the card is
1.9:1, so dropping one into the other would take the first and last letters of
JEOPARDY! off.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BACKDROP = ROOT / "Web" / "assets" / "stage-backdrop.png"
SRC = ROOT / "Web" / "assets" / "logo-wordmark.png"
OUT = ROOT / "Web" / "assets" / "og.jpg"

WIDTH = 1200
HEIGHT = 630
FILL = 0.72           # of the output width, after the art is trimmed
SHADE = 0.28          # of the backdrop's own brightness, behind the lockup


def main() -> None:
    backdrop = Image.open(BACKDROP).convert("RGB")
    scale = max(WIDTH / backdrop.width, HEIGHT / backdrop.height)
    backdrop = backdrop.resize(
        (round(backdrop.width * scale), round(backdrop.height * scale)),
        Image.LANCZOS,
    )
    left = (backdrop.width - WIDTH) // 2
    top = (backdrop.height - HEIGHT) // 2
    card = backdrop.crop((left, top, left + WIDTH, top + HEIGHT))

    logo = Image.open(SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    inner_w = round(WIDTH * FILL)
    inner_h = round(logo.height * inner_w / logo.width)
    logo = logo.resize((inner_w, inner_h), Image.LANCZOS)

    card = Image.blend(card, Image.new("RGB", card.size, (0, 0, 0)), SHADE)
    card = card.convert("RGBA")
    card.alpha_composite(logo, ((WIDTH - inner_w) // 2, (HEIGHT - inner_h) // 2))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    card.convert("RGB").save(OUT, quality=90, optimize=True)
    print(f"{OUT.relative_to(ROOT)} {WIDTH}x{HEIGHT} {OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
