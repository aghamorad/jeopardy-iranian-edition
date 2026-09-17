#!/usr/bin/env python3
"""Turn the Gemini Qajar course bank (two flat files, one per language) into the
two play-shape files a course edition ships:

    Web/courses/qajars/data/bank-en.js -> window.COURSE_CLUES_QAJARS
    Web/courses/qajars/data/bank-fa.js -> window.COURSE_CLUES_QAJARS_FA

The folder name is the course id and the globals are that name in upper snake
case. The banks land inside `Web/`, because `Web/` is what ships: the shell
loads `Web/index.html` off the filesystem and nothing outside it is bundled.

Why a script and not by hand: 512 rows, two languages, and the one thing a
human cannot do reliably at that size is prove that every category still
carries all five rungs under a byte-identical title. This asserts it and refuses
to write a bank that would not play.

This is the Qajar pass, and it differs from the Iran one in three places:

  * the source is two flat files rather than one nested one, so the language is
    chosen by which file the row came from, not by a key inside it;
  * provenance is flat (`book_title`, `author`, `page`) rather than a nested
    `provenance` object;
  * `theme` is already authored by the pass. Nothing here invents one.

`theme` still has to be checked, because it is not free text: `persianSubtitle`
in Web/app.js reads the category name plus cells[0].theme, lowercases them, and
returns the first bucket whose keyword is a substring -- in fixed bucket order.
A theme that matches no keyword anywhere renders `متفرقه` on a board that had a
subject. So this parses PERSIAN_BUCKETS out of app.js and simulates that
function exactly, for both languages, and refuses to ship a row that would fall
through to a blank garnish. What it does NOT do is re-pick a theme: the pass
chose these, and the simulation only reports what they render.

It also reports where the two languages disagree about a category's subtitle.
That is not a fault to be repaired. `persianSubtitle` buckets whatever board is
on the floor, and a pun that carries a bucket keyword in one language need not
carry it in the other -- "ENVOY OF THE TSAR: HARTWIG" trips on `art` inside the
name, `سفیرِ تزار: هارتویگ` does not. Each board stays honest about itself.

Usage:
    python3 convert_to_edition.py [--check]
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
APP_JS = os.path.join(ENGINE, "Web", "app.js")
SOURCE = {"en": os.path.join(HERE, "rows-en.json"),
          "fa": os.path.join(HERE, "rows-fa.json")}
COURSE_ID = "qajars"
COURSE_GLOB = "COURSE_CLUES_" + COURSE_ID.replace("-", "_").upper()
COURSE = os.path.join(ENGINE, "Web", "courses", COURSE_ID)
BANKS = os.path.join(COURSE, "data")
IRAN_BANK = os.path.join(ENGINE, "Web", "courses", "iran-in-world-politics",
                         "data", "bank-en.js")

LADDER = {"single": [200, 400, 600, 800, 1000],
          "double": [400, 800, 1200, 1600, 2000]}

# `difficulty` is derived from the rung, never copied. The first Qajar pass
# carried the single-round ladder onto the double round, so `double/400` shipped
# CASUAL and `double/1200` shipped STANDARD -- 200 rows the gate rejected. The
# table below is the gate's own, imported rather than restated, so a rung can
# never be labelled one way here and checked another way there.
sys.path.insert(0, os.path.join(ENGINE, "Tools"))
from check_bank import RUNG_DIFFICULTY


def derive_difficulty(row, lang):
    key = (row["round"], row["value"])
    if key not in RUNG_DIFFICULTY:
        sys.exit("row %s [%s]: %s/%s is not a rung"
                 % (row.get("id"), lang, row["round"], row["value"]))
    return RUNG_DIFFICULTY[key]


def load_buckets():
    src = open(APP_JS, encoding="utf-8").read()
    i = src.index("var PERSIAN_BUCKETS = [")
    start = src.index("[", i)
    depth, j = 0, start
    while True:
        if src[j] == "[":
            depth += 1
        elif src[j] == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    literal = re.sub(r"//[^\n]*", "", src[start:j + 1])
    buckets = ast.literal_eval(literal)
    if len(buckets) != 5:
        sys.exit("PERSIAN_BUCKETS parsed to %d buckets, expected 5 -- app.js changed shape"
                 % len(buckets))
    return buckets


def persian_subtitle(buckets, category, theme):
    hay = ((category or "") + " " + (theme or "")).lower()
    for label, keys in buckets:
        for key in keys:
            if key in hay:
                return label
    return "متفرقه"


def difficulty_vocabulary():
    """The four words the engine's board already knows, read off the course that
    is playing in front of an audience. A pass that invents a fifth would deal a
    colour no stylesheet has."""
    if not os.path.exists(IRAN_BANK):
        return None
    src = open(IRAN_BANK, encoding="utf-8").read()
    rows = json.loads(src[src.index("["):src.rindex("]") + 1])
    return {r["difficulty"] for r in rows}


def to_play(row, lang, buckets, report):
    theme = row.get("theme")
    if theme and persian_subtitle(buckets, row["category"], theme) == "متفرقه":
        report["theme_falls_through"].append((lang, row["id"], row["category"], theme))

    opts = row.get("options") or []
    answer = row.get("canonical_answer")
    idx = row.get("correct_option_index", 0)
    if not (isinstance(idx, int) and 0 <= idx < len(opts)) or opts[idx] != answer:
        got = opts.index(answer) if answer in opts else None
        if got is None:
            raise ValueError("row %s [%s]: answer not among options" % (row.get("id"), lang))
        report["index_repaired"].append((row.get("id"), lang, idx, got))
        idx = got

    reacts = row.get("host_reactions") or {}
    if isinstance(reacts, dict) and lang in reacts:      # a nested pair, if one ever appears
        reacts = reacts.get(lang) or {}
    out = {
        # ids mirror across the language pair, as in the archive and the other course
        "id": row["id"],
        "round": row["round"],
        "value": row["value"],
        "category": row["category"],
        "theme": theme,
        "difficulty": derive_difficulty(row, lang),
        "clue": row.get("clue_text"),
        "answer": answer,
        "aliases": row.get("accepted_aliases") or [],
        "options": opts,
        "correct": idx,
        "explanation": row.get("explanation"),
        "correctLine": reacts.get("correct_generic"),
        "wrongLine": reacts.get("wrong_generic"),
    }
    if row.get("book_title"):
        out["book"] = row["book_title"]
    if row.get("author"):
        out["author"] = row["author"]
    if row.get("page") is not None:
        out["page"] = row["page"]
    return out


def validate(rows, report, tag=""):
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        sys.exit("duplicate ids: %s" % dupes[:10])
    for r in rows:
        if not r["clue"] or not r["answer"] or not r["explanation"]:
            sys.exit("%s: a blank field" % r["id"])
        if len(r["options"]) != 4:
            sys.exit("%s: %d options" % (r["id"], len(r["options"])))
        if len(set(r["options"])) != len(r["options"]):
            sys.exit("%s: a repeated option" % r["id"])
        if r["options"][r["correct"]] != r["answer"]:
            sys.exit("%s: options[correct] != answer" % r["id"])
        if not r["aliases"]:
            sys.exit("%s: empty aliases" % r["id"])
        if not r["book"] or not r["author"]:
            sys.exit("%s: no citation" % r["id"])
        if r["round"] == "final":
            if "page" in r:
                sys.exit("%s: a final carries a page" % r["id"])
        elif "page" not in r:
            sys.exit("%s: a board clue with no page" % r["id"])
        if r["round"] not in ("single", "double", "final"):
            sys.exit("%s: bad round %r" % (r["id"], r["round"]))
        if not r["correctLine"] or not r["wrongLine"]:
            sys.exit("%s: missing host lines" % r["id"])
    for rnd, rungs in LADDER.items():
        groups = {}
        for r in rows:
            if r["round"] != rnd:
                continue
            groups.setdefault(r["category"], []).append(r)
        broken = [c for c, rs in groups.items()
                  if sorted(x["value"] for x in rs) != sorted(rungs)]
        if broken:
            sys.exit("%s: %d categories incomplete at some rung: %s"
                     % (tag or "row set", len(broken), broken[:3]))
        if len(groups) < 6:
            sys.exit("%s %s: only %d complete categories (need 6)"
                     % (tag or "row set", rnd, len(groups)))
        report["categories"][(tag + " " if tag else "") + rnd] = len(groups)
    return True


def emit(path, global_name, rows, banner):
    lines = [
        "// %s" % banner,
        "// Generated by Course/banks/qajar-pass-2026-09-17/convert_to_edition.py -- edit the source, not this file.",
        "// MAIN's bank lives in data/clues.js as window.CLUES. A course bank keeps its own",
        "// global, named for the course: the engine deals a show only its own array, which is",
        "// what keeps a course question out of MAIN and MAIN out of a course. Never rename",
        "// this file's global to window.CLUES -- that would hand the course the general board.",
        "",
        "window.%s = [" % global_name,
    ]
    # No trailing comma: JS accepts one, check_edition.py's strict parser does not.
    lines.append(",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows))
    lines.append("];")
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return os.path.getsize(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate and render, write nothing")
    args = ap.parse_args()

    buckets = load_buckets()
    src = {lang: json.load(open(path, encoding="utf-8")) for lang, path in SOURCE.items()}

    if len(src["en"]) != len(src["fa"]):
        sys.exit("row counts differ: %d english, %d persian" % (len(src["en"]), len(src["fa"])))
    if [r["id"] for r in src["en"]] != [r["id"] for r in src["fa"]]:
        sys.exit("the two files do not list the same ids in the same order")

    vocab = difficulty_vocabulary()
    if vocab:
        stray = sorted(set(RUNG_DIFFICULTY.values()) - vocab)
        if stray:
            sys.exit("difficulty words the engine's other course does not use: %s" % stray)

    report = {"theme_falls_through": [], "index_repaired": [],
              "categories": {}, "subtitle_spread": {}}

    out = {}
    for lang, rows in src.items():
        out[lang] = [to_play(r, lang, buckets, report) for r in rows]

    # every category must render the same subtitle in both languages
    for r_en, r_fa in zip(out["en"], out["fa"]):
        a = persian_subtitle(buckets, r_en["category"], r_en["theme"])
        b = persian_subtitle(buckets, r_fa["category"], r_fa["theme"])
        if a != b:
            report["subtitle_spread"].setdefault((a, b), []).append(r_en["id"])

    validate(out["en"], report, tag="en")
    validate(out["fa"], report, tag="fa")

    print("rows: %d english, %d persian" % (len(out["en"]), len(out["fa"])))
    rounds = {}
    for r in out["en"]:
        rounds[r["round"]] = rounds.get(r["round"], 0) + 1
    print("rounds: %s" % json.dumps(rounds))
    print("complete categories: %s" % json.dumps(report["categories"], ensure_ascii=False))
    print("difficulty words: %s" % sorted({r["difficulty"] for r in out["en"]}))
    if report["index_repaired"]:
        print("correct-index repaired on %d rows" % len(report["index_repaired"]))
    if report["theme_falls_through"]:
        print("THEMES THAT PRINT متفرقه: %d" % len(report["theme_falls_through"]))
        for row in report["theme_falls_through"][:10]:
            print("   %s" % (row,))
    else:
        print("themes: every row renders a real subtitle, in both languages")
    if report["subtitle_spread"]:
        print("LANGUAGES DISAGREE ON SUBTITLE: %d pairs" % len(report["subtitle_spread"]))
        for k, v in list(report["subtitle_spread"].items())[:10]:
            print("   %s -> %s  %s" % (k[0], k[1], v[:3]))
    dist = {}
    for r in out["fa"]:
        k = persian_subtitle(buckets, r["category"], r["theme"])
        dist[k] = dist.get(k, 0) + 1
    print("rendered subtitle spread (persian cell):")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print("   %-22s %d" % (k, v))

    if args.check:
        print("\n--check: nothing written")
        return

    os.makedirs(BANKS, exist_ok=True)
    en = os.path.join(BANKS, "bank-en.js")
    fa = os.path.join(BANKS, "bank-fa.js")
    a = emit(en, COURSE_GLOB, out["en"], "Qajars -- English bank")
    b = emit(fa, COURSE_GLOB + "_FA", out["fa"], "Qajars -- Persian bank")
    print("\nwrote %s (%d KB)" % (en, a // 1024))
    print("wrote %s (%d KB)" % (fa, b // 1024))

    # This script writes the banks itself, which is exactly how it stepped around
    # `Course/build_edition.sh` — the gate that checks difficulty against the rung
    # and repeats across categories. The Qajar edition shipped with 200 rows
    # mislabelled and 10 questions asked twice because nothing here ran it. A
    # converter that writes a bank now runs the gate or exits non-zero.
    gate = os.path.join(ENGINE, "Course", "build_edition.sh")
    print("\nrunning the edition gate: %s" % os.path.relpath(gate, ENGINE))
    sys.exit(subprocess.call(["bash", gate, COURSE_ID]))


if __name__ == "__main__":
    main()
