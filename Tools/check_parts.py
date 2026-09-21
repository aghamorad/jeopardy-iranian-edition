#!/usr/bin/env python3
"""Verify the append-only MAIN-bank ledger.

This is deliberately narrow: it validates recorded new parts against the live
archives without re-running every editorial heuristic over every historical
row. The full release sweep retains those broader checks.
"""

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "QuestionBank", "parts", "manifest.json")
ARCHIVES = {
    "en": os.path.join(ROOT, "QuestionBank", "verified_clues.json"),
    "fa": os.path.join(ROOT, "QuestionBank", "verified_clues_fa.json"),
}


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fail(message):
    print("X " + message, file=sys.stderr)
    return False


def main():
    try:
        manifest = json.load(open(MANIFEST, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail("cannot read parts manifest: %s" % exc)
    if manifest.get("format") != 1 or not isinstance(manifest.get("parts"), list):
        return fail("unsupported parts manifest")

    archives = {lang: {row["id"]: row for row in json.load(open(path, encoding="utf-8"))}
                for lang, path in ARCHIVES.items()}
    seen = set()
    rows = 0
    ok = True
    for part in manifest["parts"]:
        stem = part.get("stem")
        if not isinstance(stem, str) or not stem or stem in seen:
            ok = fail("part has a missing or duplicate stem: %r" % stem) and ok
            continue
        seen.add(stem)
        paired = {}
        for lang in ("en", "fa"):
            rel, expected = part.get(lang), part.get(lang + "_sha256")
            path = os.path.join(ROOT, rel) if isinstance(rel, str) else ""
            if not path or not os.path.isfile(path):
                ok = fail("%s: missing %s source" % (stem, lang)) and ok
                continue
            if digest(path) != expected:
                ok = fail("%s: %s source digest changed" % (stem, lang)) and ok
                continue
            try:
                paired[lang] = json.load(open(path, encoding="utf-8"))
            except ValueError as exc:
                ok = fail("%s: %s source is invalid JSON: %s" % (stem, lang, exc)) and ok
                continue
            if len(paired[lang]) != part.get("rows_per_language"):
                ok = fail("%s: %s row count differs from manifest" % (stem, lang)) and ok
        if set(paired) != {"en", "fa"}:
            continue
        en_ids = {row.get("id") for row in paired["en"]}
        fa_ids = {row.get("id") for row in paired["fa"]}
        if en_ids != fa_ids or None in en_ids:
            ok = fail("%s: English and Persian IDs do not mirror" % stem) and ok
            continue
        for lang in ("en", "fa"):
            for row in paired[lang]:
                archived = archives[lang].get(row["id"])
                if archived != row:
                    ok = fail("%s: %s is absent from or differs in the %s archive"
                              % (stem, row["id"], lang)) and ok
        rows += len(en_ids)
        print("ok    %s: %d mirrored rows" % (stem, len(en_ids)))
    if ok:
        print("ok    %d immutable part(s), %d rows per language" % (len(seen), rows))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
