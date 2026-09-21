#!/usr/bin/env python3
"""Generate the boot asset manifest from every shipped image, audio file, and font.

The splash consumes this list as a real readiness contract. Keep it generated:
adding an asset anywhere under Web/assets or a course's assets folder cannot make
the loader silently miss it.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "Web"
TARGET = WEB / "data" / "boot_assets.js"
KINDS = {
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".webp": "image", ".svg": "image",
    ".m4a": "audio", ".mp3": "audio", ".wav": "audio", ".ogg": "audio",
    ".ttf": "font", ".otf": "font", ".woff": "font", ".woff2": "font",
}


def manifest():
    roots = [WEB / "assets"] + sorted((WEB / "courses").glob("*/assets"))
    rows = []
    for base in roots:
        for path in sorted(base.rglob("*")):
            kind = KINDS.get(path.suffix.lower())
            if kind:
                rows.append({"src": path.relative_to(WEB).as_posix(), "kind": kind})
    return rows


def render(rows):
    return "window.BOOT_ASSETS=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    args = ap.parse_args()
    text = render(manifest())
    have = TARGET.read_text(encoding="utf-8") if TARGET.exists() else None
    if have == text:
        print("ok    Web/data/boot_assets.js covers every shipped visual, audio, and font asset")
        return 0
    if args.check:
        print("STALE Web/data/boot_assets.js does not match shipped assets")
        return 1
    TARGET.write_text(text, encoding="utf-8")
    print("wrote Web/data/boot_assets.js (%d assets)" % len(manifest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
