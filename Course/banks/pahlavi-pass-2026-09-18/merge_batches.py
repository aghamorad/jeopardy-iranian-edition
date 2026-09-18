#!/usr/bin/env python3
"""Fold the authored group batches into the pass's two working row files.

    python3 merge_batches.py [--check]

Reads `rows-en.json` / `rows-fa.json` (the 150 seed rows) and every
`batches/*-en.json` / `batches/*-fa.json`, checks that the result is a bank the
converter and the gate can both accept, and writes the merged files back.

Run with `--check` to validate every batch and report, writing nothing.

What it refuses, and why each one would otherwise be silent:

  * **An id collision.** Two groups using the same block would drop a clue off
    the board with no error anywhere -- ids are what the converter and the
    engine key on.
  * **The two languages not mirroring.** `registerEdition` takes a bank per
    language and the engine deals them in parallel; a row present in one file
    and not the other is a board with a hole in it.
  * **A batch that is not five rungs under one title.** Already checked per
    batch, re-checked here because groups are merged, and a category split
    across two batches would look whole to each of them.

It does NOT check content -- that is `selfcheck.py` per batch, then
`Tools/check_bank.py` and `Tools/check_repeats.py` over the merged file by way
of `Course/build_edition.sh`, which the converter runs.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BATCHES = os.path.join(HERE, "batches")
ROWS = {"en": os.path.join(HERE, "rows-en.json"),
        "fa": os.path.join(HERE, "rows-fa.json")}
LADDER = {"single": [200, 400, 600, 800, 1000],
          "double": [400, 800, 1200, 1600, 2000]}

# The id blocks assigned to each group. A batch whose ids stray outside its
# block means two authors have been given the same numbers.
BLOCKS = {
    "w1":  (151, 190), "w2a": (191, 220), "w2b": (221, 250),
    "w3":  (251, 290),
    "w4a": (291, 325), "w4b": (326, 360), "w5": (361, 380), "w6": (381, 400),
    "w7a": (401, 425), "w7b": (426, 450), "w8":  (451, 500),
}
FINALS = (501, 512)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def number(row):
    """The integer part of `pahlavi_0151_a`."""
    return int(row["id"].split("_")[1])


def groups():
    out = []
    for name in sorted(os.listdir(BATCHES)):
        if name.endswith("-en.json"):
            out.append(name[: -len("-en.json")])
    return out


def check_batch(group, report):
    en = load(os.path.join(BATCHES, group + "-en.json"))
    fa = load(os.path.join(BATCHES, group + "-fa.json"))
    trail = os.path.join(BATCHES, group + "-fa.json")

    if [r["id"] for r in en] != [r["id"] for r in fa]:
        sys.exit("%s: the two languages do not mirror id for id" % group)

    lo, hi = BLOCKS.get(group, FINALS)
    ids = [number(r) for r in en]
    if len(set(ids)) != len(ids):
        sys.exit("%s: duplicate id inside the batch" % group)
    body = [n for n in ids if n < FINALS[0]]
    finals = [n for n in ids if n >= FINALS[0]]
    if body and (min(body) < lo or max(body) > hi):
        sys.exit("%s: ids outside its block %d-%d: %s"
                 % (group, lo, hi, sorted(body)))
    if finals and (min(finals) < FINALS[0] or max(finals) > FINALS[1]):
        sys.exit("%s: final ids outside %d-%d" % (group, FINALS[0], FINALS[1]))

    for lang, rows in (("en", en), ("fa", fa)):
        if any(r["language"] != lang for r in rows):
            sys.exit("%s [%s]: a row is labelled the wrong language" % (group, lang))
        cats = {}
        for r in rows:
            cats.setdefault(r["category"], []).append(r)
        for cat, rs in cats.items():
            if rs[0]["round"] == "final":
                if len(rs) != 1:
                    sys.exit("%s [%s]: final %r has %d rows" % (group, lang, cat, len(rs)))
                continue
            rnd = rs[0]["round"]
            if {r["round"] for r in rs} != {rnd}:
                sys.exit("%s [%s]: %r mixes rounds" % (group, lang, cat))
            if sorted(r["value"] for r in rs) != LADDER[rnd]:
                sys.exit("%s [%s]: %r is not whole (%s)"
                         % (group, lang, cat, rnd))

    n_en = len(en)
    report["batches"][group] = {
        "rows": n_en,
        "single": len({r["category"] for r in en if r["round"] == "single"}),
        "double": len({r["category"] for r in en if r["round"] == "double"}),
        "final": len({r["category"] for r in en if r["round"] == "final"}),
    }
    return en, fa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate and report, write nothing")
    args = ap.parse_args()

    report = {"batches": {}}
    seed = {lang: load(path) for lang, path in ROWS.items()}
    if [r["id"] for r in seed["en"]] != [r["id"] for r in seed["fa"]]:
        sys.exit("the seed files do not mirror id for id")

    merged = {"en": list(seed["en"]), "fa": list(seed["fa"])}
    names = groups()
    if not names:
        sys.exit("no batches in %s" % os.path.relpath(BATCHES, HERE))

    for group in names:
        en, fa = check_batch(group, report)
        merged["en"].extend(en)
        merged["fa"].extend(fa)

    # Global checks the per-batch pass cannot see.
    for lang, rows in merged.items():
        ids = [r["id"] for r in rows]
        if len(set(ids)) != len(ids):
            dupes = sorted({i for i in ids if ids.count(i) > 1})
            sys.exit("duplicate ids across batches [%s]: %s" % (lang, dupes[:10]))
    if [r["id"] for r in merged["en"]] != [r["id"] for r in merged["fa"]]:
        sys.exit("the merged files do not mirror id for id")

    en = merged["en"]
    rounds = {}
    for r in en:
        rounds[r["round"]] = rounds.get(r["round"], 0) + 1
    cats = {}
    for r in en:
        if r["round"] != "final":
            cats.setdefault(r["round"], set()).add(r["category"])
    finals = len({r["category"] for r in en if r["round"] == "final"})

    print("batches merged: %s" % ", ".join(names))
    print("rows: %d english, %d persian" % (len(merged["en"]), len(merged["fa"])))
    print("rounds: %s" % json.dumps(rounds))
    print("categories: %d single, %d double, %d finals"
          % (len(cats.get("single", ())), len(cats.get("double", ())), finals))
    for group in names:
        b = report["batches"][group]
        print("   %-4s %3d rows  %2d single  %2d double  %d final"
              % (group, b["rows"], b["single"], b["double"], b["final"]))

    if args.check:
        print("\n--check: nothing written")
        return

    for lang, rows in merged.items():
        with open(ROWS[lang], "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("wrote %s (%d rows)" % (os.path.relpath(ROWS[lang], HERE), len(rows)))


if __name__ == "__main__":
    main()
