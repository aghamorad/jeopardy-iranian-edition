#!/usr/bin/env python3
"""Cut every icon the four builds ship from one master.

    python3 Tools/make_app_icons.py

The master is `Assets/Generated/icon-main-*.png`, the art as it was drawn: a
glossy rounded-square glass tile on a transparent field, 1254 square. The tile
occupies ~0.877 of the canvas, which is what the icon has always been — the
first master measured 0.873 — so the treatment is a straight composite onto
opaque black and a resize. No re-framing, no crop.

Every target is 1:1 and full-bleed, because a launcher or a Dock tile draws its
own mask and a transparent margin would come out as a ragged rim:

  App/Resources/icon-master.png                  1254  the master kept in-tree
  App/Resources/AppIcon.png                      1024
  App/Resources/AppIcon.iconset/*                 10 files, then AppIcon.icns
  iOS/Assets.xcassets/AppIcon.appiconset/        1024
  Web/assets/icon-512.png                         512  favicon
  Web/assets/apple-touch-icon.png                 180
  Android mipmap-*/ic_launcher{,_round}.png       48 72 96 144 192
  Android mipmap-*/ic_launcher_foreground.png    108 162 216 324 432

The two Android shapes share one bitmap: Android 7 ignores which is which, and
`round` has been byte-identical to `ic_launcher` at every density since the
first cut. The adaptive icon's foreground is the exception to full-bleed — the
launcher supplies the shape, and only the middle two thirds of the canvas is
guaranteed to survive any mask, so the tile is scaled to 2/3 and centred on
black. See `mipmap-anydpi-v26/ic_launcher.xml`.

This writes onto files the apps serve, which the tooling rule otherwise forbids.
It is safe here for the reason that rule names: the master is in the tree, so a
re-run is a repaint and not a loss, and every previous icon is also in git.

Running it is not enough to ship — the four builds have to be cut again, since
the icons are baked into the bundles rather than read from `Web/`.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
GENERATED = ROOT / "Assets" / "Generated"
MASTER = sorted(GENERATED.glob("icon-main-*.png"))[-1]

MASTER_SIZE = 1254
PLATE = (0, 0, 0)          # the show's black, and what the tile already sits on
FOREGROUND_FRAC = 2 / 3    # of the canvas, inside the adaptive icon's safe zone

ICONSET = {
    "icon_16x16.png": 16, "icon_16x16@2x.png": 32,
    "icon_32x32.png": 32, "icon_32x32@2x.png": 64,
    "icon_128x128.png": 128, "icon_128x128@2x.png": 256,
    "icon_256x256.png": 256, "icon_256x256@2x.png": 512,
    "icon_512x512.png": 512, "icon_512x512@2x.png": 1024,
}

ANDROID = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)
    print(f"  {image.size[0]:>4}  {path.relative_to(ROOT)}  "
          f"{path.stat().st_size // 1024}KB")


def square(plate: Image.Image, size: int) -> Image.Image:
    return plate.resize((size, size), Image.LANCZOS)


def foreground(plate: Image.Image, size: int) -> Image.Image:
    inner = round(size * FOREGROUND_FRAC)
    canvas = Image.new("RGB", (size, size), PLATE)
    canvas.paste(plate.resize((inner, inner), Image.LANCZOS),
                 ((size - inner) // 2, (size - inner) // 2))
    return canvas


def main() -> None:
    if not MASTER.exists():
        sys.exit(f"no master in {GENERATED.relative_to(ROOT)}/ — nothing to cut")

    art = Image.open(MASTER).convert("RGBA")
    if art.size != (MASTER_SIZE, MASTER_SIZE):
        sys.exit(f"{MASTER.name} is {art.size}, expected {MASTER_SIZE} square")

    plate = Image.new("RGB", art.size, PLATE)
    plate.paste(art, (0, 0), art)
    print(f"{MASTER.relative_to(ROOT)} → {MASTER_SIZE} square, cut to:")

    save(plate, ROOT / "App" / "Resources" / "icon-master.png")
    save(square(plate, 1024), ROOT / "App" / "Resources" / "AppIcon.png")
    save(square(plate, 1024),
         ROOT / "iOS" / "Assets.xcassets" / "AppIcon.appiconset" / "icon1024.png")
    save(square(plate, 512), ROOT / "Web" / "assets" / "icon-512.png")
    save(square(plate, 180), ROOT / "Web" / "assets" / "apple-touch-icon.png")

    iconset = ROOT / "App" / "Resources" / "AppIcon.iconset"
    for name, size in ICONSET.items():
        save(square(plate, size), iconset / name)

    icns = ROOT / "App" / "Resources" / "AppIcon.icns"
    subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(icns)],
                   check=True)
    print(f"     —  {icns.relative_to(ROOT)}  {icns.stat().st_size // 1024}KB")

    for density, size in ANDROID.items():
        res = ROOT / "Android" / "app" / "src" / "main" / "res" / f"mipmap-{density}"
        launcher = square(plate, size)
        save(launcher, res / "ic_launcher.png")
        save(launcher, res / "ic_launcher_round.png")
        save(foreground(plate, size * 9 // 4), res / "ic_launcher_foreground.png")


if __name__ == "__main__":
    main()
