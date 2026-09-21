#!/usr/bin/env python3
"""Reject a legacy-style direct MAIN archive writer in the active tool surface."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "Tools"

# The historic scripts opened the materialized archive directly for writing.
# The supported writer (`append_batch.py`) uses an atomic temporary-file path
# after its full batch gate, so it deliberately does not match this pattern.
DIRECT_ARCHIVE_WRITE = re.compile(
    r"open\([^\n]*verified_clues(?:_fa)?\.json[^\n]*['\"]w['\"]",
    re.IGNORECASE,
)


def main():
    offenders = []
    for path in TOOLS.glob("*.py"):
        if DIRECT_ARCHIVE_WRITE.search(path.read_text(encoding="utf-8")):
            offenders.append(path.name)
    if offenders:
        print("X active direct archive writer(s): " + ", ".join(sorted(offenders)))
        print("  Use Tools/append_batch.py; direct archive writers are not kept in this repository.")
        return 1
    print("ok    active Tools contains no legacy direct archive writer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
