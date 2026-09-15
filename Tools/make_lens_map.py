#!/usr/bin/env python3
"""Build the radial displacement map the globes on the front door are bent with.

    python3 Tools/make_lens_map.py

Writes `Web/assets/globe-lensmap.png`, which `#globe-warp` in `index.html` feeds to
`feDisplacementMap`. Re-run it only if the curvature changes; the output is
committed, not built.

The map is a field in the same the format `feDisplacementMap` reads: R is the
horizontal shift, G the vertical, both centred on 128 so that 128 means "do not
move", and B is flat because nothing uses it.

Why it is shaped the way it is: a glass ball is a *wide-angle* lens seen from
outside, not a magnifier. Its surface lies nearly flat to the eye on axis and
turns edge-on as it approaches the silhouette, so the picture has to be sampled
from further out near the rim than it is drawn — that is what compresses the
edge and makes the middle look like it is bulging toward you. `src_r` does
exactly that, and it is normalised so the rim itself does not move, which keeps
the art inside its own circle instead of smearing past the edge.

Corners are left at zero shift on purpose: the map is stretched across the whole
square element with `preserveAspectRatio="none"`, so anything outside the rim is
off-screen anyway, and pinning it stops the filter from dragging the corners in.
"""

from pathlib import Path

import numpy as np
from PIL import Image

SIZE = 256          # geometry, not detail: 256 is ~10KB and reads identically
CURVATURE = 0.55    # 0 is a flat sheet of glass, 1 is a doorknob
OUT = Path(__file__).resolve().parent.parent / "Web" / "assets" / "globe-lensmap.png"


def main() -> None:
    n = SIZE
    yy, xx = np.mgrid[0:n, 0:n]
    c = (n - 1) / 2.0
    x, y = (xx - c) / c, (yy - c) / c
    r = np.sqrt(x * x + y * y)
    safe = np.clip(r, 1e-6, None)

    src_r = safe * (1.0 + CURVATURE * safe * safe) / (1.0 + CURVATURE)
    inside = r <= 1.0
    src_r = np.where(inside, src_r, safe)

    ux, uy = x / safe, y / safe
    dx = np.where(inside, (src_r - safe) * ux, 0.0)
    dy = np.where(inside, (src_r - safe) * uy, 0.0)

    rgb = np.stack([0.5 + dx * 0.5, 0.5 + dy * 0.5, np.full_like(dx, 0.5)], axis=-1)
    img = Image.fromarray(np.clip(rgb * 255.0, 0, 255).astype(np.uint8), "RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"{OUT} {img.size[0]}x{img.size[1]} {OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
