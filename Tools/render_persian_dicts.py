#!/usr/bin/env python3
"""Regenerate the two legacy Persian lookup dictionaries from the archive."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "QuestionBank/verified_clues_fa.json"
TARGETS = [ROOT / "QuestionBank/persian_clues.json", ROOT / "App/Resources/persian_clues.json"]
FIELDS = ("clue_text", "canonical_answer", "options", "explanation", "specificity_prompt")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    args = ap.parse_args()
    rows = json.loads(SOURCE.read_text(encoding="utf-8"))
    data = {row["id"]: {field: row.get(field, "") for field in FIELDS} for row in rows}
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    stale = False
    for target in TARGETS:
        have = target.read_text(encoding="utf-8") if target.exists() else None
        if have == text:
            print(f"ok    {target.relative_to(ROOT)} is in step with {SOURCE.relative_to(ROOT)}")
        elif args.check:
            stale = True
            print(f"STALE {target.relative_to(ROOT)} does not match {SOURCE.relative_to(ROOT)}")
        else:
            target.write_text(text, encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)} ({len(data)} entries)")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
