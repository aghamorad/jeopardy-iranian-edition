#!/usr/bin/env python3
"""Render the play files from the archive.

The archive (`QuestionBank/verified_clues.json`, `..._fa.json`) is canonical;
`Web/data/clues.js` and `Web/data/clues_fa.js` are generated from it. This is
that generator. Nothing else in the repo writes them.

    python3 Tools/render_bank.py            # rewrite both play files
    python3 Tools/render_bank.py --check    # report divergence, write nothing

`--check` is the honesty check: it rebuilds both play files in memory and
compares them byte for byte with what is on disk, so a hand-edit to a play file
cannot pass unnoticed.

The two shapes do not match and the play shape's key ORDER is load-bearing —
`json.dumps` preserves insertion order and `Web/app.js` reads these by name, so
the order below is the order the file has always had. The archive's field names
are on the left, the play file's on the right.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ARCHIVE = "QuestionBank/verified_clues.json"
ARCHIVE_FA = "QuestionBank/verified_clues_fa.json"
PLAY = "Web/data/clues.js"
PLAY_FA = "Web/data/clues_fa.js"

# (play key, archive key). `host_reactions.X` is reached through the row.
FIELDS = [
    ("id", "id"),
    ("round", "round"),
    ("value", "value"),
    ("category", "category"),
    ("theme", "theme"),
    ("difficulty", "difficulty"),
    ("clue", "clue_text"),
    ("answer", "canonical_answer"),
    ("aliases", "accepted_aliases"),
    ("options", "options"),
    ("correct", "correct_option_index"),
    ("explanation", "explanation"),
    ("book", "book_title"),
    ("author", "author"),
    ("page", "page"),
    ("period", "historical_period"),
    ("passage", "supporting_passage"),
    ("correctLine", "host_reactions.correct_generic"),
    ("wrongLine", "host_reactions.wrong_generic"),
]


def archive_rows(path):
    """Slice the JSON array out of the archive file.

    The archive is pretty-printed at indent=2 with no trailing newline (that
    exact serialization reproduces it byte for byte). We only read it here, so
    its shape does not matter — but anything that WRITES it must match it.
    """
    text = open(path, encoding="utf-8").read()
    start = text.find("[")
    if start < 0:
        raise SystemExit("%s: no JSON array found" % path)
    return json.JSONDecoder().raw_decode(text, start)[0]


def pick(row, key):
    if "." in key:
        head, tail = key.split(".", 1)
        return (row.get(head) or {}).get(tail)
    return row.get(key)


def render(rows, global_name):
    out = []
    for row in rows:
        out.append({play_key: pick(row, arch_key) for play_key, arch_key in FIELDS})
    return "window.%s=%s;\n" % (global_name, json.dumps(out, ensure_ascii=False))


JOBS = [
    (ARCHIVE, PLAY, "CLUES"),
    (ARCHIVE_FA, PLAY_FA, "CLUES_FA"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="compare without writing")
    args = ap.parse_args()

    bad = 0
    for archive, play, global_name in JOBS:
        want = render(archive_rows(os.path.join(ROOT, archive)), global_name)
        path = os.path.join(ROOT, play)
        have = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if have == want:
            print("ok    %s is in step with %s" % (play, archive))
            continue
        bad += 1
        if args.check:
            print("STALE %s does not match a fresh render of %s" % (play, archive))
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(want)
        print("wrote %s (%d rows, %d bytes)" % (play, len(archive_rows(os.path.join(ROOT, archive))), len(want.encode("utf-8"))))

    if args.check and bad:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
