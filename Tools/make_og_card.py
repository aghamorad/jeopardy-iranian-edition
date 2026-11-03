#!/usr/bin/env python3
"""Build the social share card.

    python3 Tools/make_og_card.py

Writes two files from one composition: `Web/assets/og.jpg` at 1200x630, the
size every unfurler crops to, and `.github/assets/social-preview.jpg` at
1280x640, which is the size GitHub asks for when the repository's social
preview is uploaded by hand in Settings. That one cannot be committed into
place — GitHub only reads it from the settings form — so the file is here to
be dragged in, and regenerated whenever the lockup moves. It is a JPEG, not a
PNG, because GitHub will not take an upload over 1 MB and the backdrop does
not survive a lossless encode inside that budget.
`Web/index.html` points `og:image` at exactly the first path, so the name is
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
PREVIEW = ROOT / ".github" / "assets" / "social-preview.jpg"

WIDTH = 1200
HEIGHT = 630
PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 640
FILL = 0.72           # of the output width, after the art is trimmed
SHADE = 0.28          # of the backdrop's own brightness, behind the lockup


def compose(width: int, height: int) -> Image.Image:
    backdrop = Image.open(BACKDROP).convert("RGB")
    scale = max(width / backdrop.width, height / backdrop.height)
    backdrop = backdrop.resize(
        (round(backdrop.width * scale), round(backdrop.height * scale)),
        Image.LANCZOS,
    )
    left = (backdrop.width - width) // 2
    top = (backdrop.height - height) // 2
    card = backdrop.crop((left, top, left + width, top + height))

    logo = Image.open(SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    inner_w = round(width * FILL)
    inner_h = round(logo.height * inner_w / logo.width)
    logo = logo.resize((inner_w, inner_h), Image.LANCZOS)

    card = Image.blend(card, Image.new("RGB", card.size, (0, 0, 0)), SHADE)
    card = card.convert("RGBA")
    card.alpha_composite(logo, ((width - inner_w) // 2, (height - inner_h) // 2))
    return card.convert("RGB")


def main() -> None:
    for path, width, height in (
        (OUT, WIDTH, HEIGHT),
        (PREVIEW, PREVIEW_WIDTH, PREVIEW_HEIGHT),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        compose(width, height).save(path, quality=90, optimize=True)
        print(f"{path.relative_to(ROOT)} {width}x{height} "
              f"{path.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
