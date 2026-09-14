#!/usr/bin/env python3
"""
Turn the Gemini course bank (nested {en,fa} third shape) into the two hand-written
play-shape files a course edition ships:

    Web/courses/iran-in-world-politics/data/bank-en.js -> window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS
    Web/courses/iran-in-world-politics/data/bank-fa.js -> window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS_FA

The folder name is the course id, and the globals are that name in upper snake case.
The banks have to land inside `Web/`, because `Web/` is what ships: the shell loads
`Web/index.html` off the filesystem and nothing outside it is bundled.

Why a script and not by hand: 690 rows, two languages, and the one thing a human cannot
do reliably at that size is prove that every category still carries all five rungs under
a byte-identical title. This asserts it and refuses to write a bank that would not play.

The subtitle bucket is NOT free choice. `persianSubtitle` in Web/app.js reads the
category name plus cells[0].theme, lowercases them, and returns the first bucket whose
keyword is a substring -- in fixed bucket order. So a theme keyword only lands where we
want it if no EARLIER bucket's keyword appears in the category name. This script parses
PERSIAN_BUCKETS out of app.js and simulates that function exactly, so the rendered
subtitle in the built game is a checked fact, not a hope.

Usage:
    python3 convert_to_edition.py [--themes theme_buckets.tsv] [--check]
"""

import argparse
import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
APP_JS = os.path.join(ENGINE, "Web", "app.js")
SOURCE = os.path.join(HERE, "iranian_jeopardy_bank.json")
FINALS = os.path.join(HERE, "finals.json")
COURSE_ID = "iran-in-world-politics"
COURSE_GLOB = "COURSE_CLUES_" + COURSE_ID.replace("-", "_").upper()
COURSE = os.path.join(ENGINE, "Web", "courses", COURSE_ID)
BANKS = os.path.join(COURSE, "data")

BUCKET_CODES = {
    "P": "مردم و چهره‌ها",
    "G": "مکان‌ها و جغرافیا",
    "H": "تاریخ و انقلاب‌ها",
    "C": "فرهنگ و هنر",
    "S": "سیاست و جامعه",
}

# Which keyword to write into `theme` for a given target bucket, most specific first.
# Every entry must appear verbatim in PERSIAN_BUCKETS[bucket]; that is asserted at load.
PREFERRED = {
    "P": ["trailblazer", "pioneer", "figure", "monarchy", "royal"],
    "G": ["geograph", "territorial", "frontier", "caspian", "maritime"],
    "H": ["war", "revolution", "dynast", "siege", "uprising"],
    "C": ["poet", "literature", "music", "cinema", "mytholog"],
    "S": ["politic", "diploma", "governance", "econom", "sanction"],
}


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
    literal = src[start:j + 1]
    # strip JS line comments if any ever creep in, then parse as a Python literal
    literal = re.sub(r"//[^\n]*", "", literal)
    buckets = ast.literal_eval(literal)
    if len(buckets) != 5:
        sys.exit("PERSIAN_BUCKETS parsed to %d buckets, expected 5 -- app.js changed shape" % len(buckets))
    return buckets


def persian_subtitle(buckets, category, theme):
    hay = ((category or "") + " " + (theme or "")).lower()
    for label, keys in buckets:
        for key in keys:
            if key in hay:
                return label
    return "متفرقه"


def forced_by_category(buckets, label, category):
    """Return the earlier-bucket keyword that hijacks `category`, or None."""
    hay = (category or "").lower()
    for lab, keys in buckets:
        for key in keys:
            if key in hay:
                return (lab, key) if lab != label else None
        if lab == label:
            return None
    return None


def load_themes(path, buckets):
    """theme_buckets.tsv -> {english category name: bucket code}."""
    if not os.path.exists(path):
        sys.exit("missing %s -- the bucket classification has not been written yet" % path)
    by_bucket = {b[0]: set(b[1]) for b in buckets}
    out = {}
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or "\t" not in line:
            continue
        code, name = line.split("\t", 1)
        code, name = code.strip().upper(), name.strip()
        if code not in BUCKET_CODES:
            sys.exit("line %d: unknown bucket code %r" % (n, code))
        if name in out:
            sys.exit("line %d: category %r classified twice" % (n, name))
        out[name] = code
    for code in BUCKET_CODES:
        for kw in PREFERRED[code]:
            if kw not in by_bucket.get(BUCKET_CODES[code], ()):
                sys.exit("keyword %r is not in bucket %s -- PREFERRED has drifted from app.js"
                         % (kw, BUCKET_CODES[code]))
    return out


def theme_for(code, category, buckets, report):
    label = BUCKET_CODES[code]
    hijack = forced_by_category(buckets, label, category)
    for kw in PREFERRED[code]:
        if hijack is None:
            got = persian_subtitle(buckets, category, kw)
            if got == label:
                return kw
    if hijack:
        report["forced"].append((category, label, hijack[0], hijack[1]))
        # can't have this label; fall through to the hijacking bucket honestly
        other = [c for c, l in BUCKET_CODES.items() if l == hijack[0]]
        if other:
            for kw in PREFERRED[other[0]]:
                if persian_subtitle(buckets, category, kw) == hijack[0]:
                    return kw
    report["unreachable"].append((category, label))
    return PREFERRED[code][0]


def field(row, key, lang, default=None):
    v = row.get(key, default)
    if isinstance(v, dict):
        return v.get(lang)
    return v


def to_play(row, lang, theme, report):
    opts = field(row, "options", lang) or []
    answer = field(row, "canonical_answer", lang)
    idx = row.get("correct_option_index", 0)
    if not (isinstance(idx, int) and 0 <= idx < len(opts)) or opts[idx] != answer:
        got = opts.index(answer) if answer in opts else None
        if got is None:
            raise ValueError("row %s [%s]: answer not among options" % (row.get("id"), lang))
        report["index_repaired"].append((row.get("id"), lang, idx, got))
        idx = got
    prov = row.get("provenance") or {}
    out = {
        # ids mirror across the language pair, as in the archive and the placeholder
        "id": row["id"],
        "round": row["round"],
        "value": row["value"],
        "category": field(row, "category", lang),
        "theme": theme,
        "difficulty": row["difficulty"],
        "clue": field(row, "clue_text", lang),
        "answer": answer,
        "aliases": field(row, "accepted_aliases", lang) or [],
        "options": opts,
        "correct": idx,
        "explanation": field(row, "explanation", lang),
        "correctLine": ((row.get("host_reactions") or {}).get(lang) or {}).get("correct_generic"),
        "wrongLine": ((row.get("host_reactions") or {}).get(lang) or {}).get("wrong_generic"),
    }
    if prov.get("source_book"):
        out["book"] = prov["source_book"]
    if prov.get("source_author"):
        out["author"] = prov["source_author"]
    if prov.get("page_number") is not None:
        out["page"] = prov["page_number"]
    return out


def validate(rows, report, tag=""):
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        sys.exit("duplicate ids: %s" % dupes[:10])
    for r in rows:
        if len(r["options"]) != 4:
            sys.exit("%s: %d options" % (r["id"], len(r["options"])))
        if r["options"][r["correct"]] != r["answer"]:
            sys.exit("%s: options[correct] != answer" % r["id"])
        if not r["aliases"]:
            sys.exit("%s: empty aliases" % r["id"])
        if r["round"] not in ("single", "double", "final"):
            sys.exit("%s: bad round %r" % (r["id"], r["round"]))
        if not r["correctLine"] or not r["wrongLine"]:
            sys.exit("%s: missing host lines" % r["id"])
    ladder = {"single": [200, 400, 600, 800, 1000], "double": [400, 800, 1200, 1600, 2000]}
    for rnd, rungs in ladder.items():
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
        "// Generated by Course/banks/gemini-pass-2026-09-14/convert_to_edition.py -- edit the source, not this file.",
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
    ap.add_argument("--themes", default=os.path.join(HERE, "theme_buckets.tsv"))
    ap.add_argument("--check", action="store_true", help="validate and render, write nothing")
    args = ap.parse_args()

    buckets = load_buckets()
    by_name = load_themes(args.themes, buckets)
    source = json.load(open(SOURCE, encoding="utf-8"))
    finals = json.load(open(FINALS, encoding="utf-8"))
    for f in finals:
        f.setdefault("provenance", None)

    report = {"forced": [], "unreachable": [], "index_repaired": [], "categories": {}}

    rows = list(source) + list(finals)
    names = {field(r, "category", "en") for r in source}
    missing = sorted(n for n in names - set(by_name) if n is not None)
    extra = sorted(n for n in set(by_name) - names)
    if missing:
        sys.exit("no bucket assigned for %d categories, e.g. %s" % (len(missing), missing[:5]))
    if extra:
        print("note: %d bucket assignments match no category, e.g. %s" % (len(extra), extra[:5]))

    out = {"en": [], "fa": []}
    for lang in ("en", "fa"):
        for r in rows:
            cat_en = field(r, "category", "en")
            if r["round"] == "final":
                # finals carry their own theme; they are never dealt onto a board column
                theme = r.get("theme")
                if theme and persian_subtitle(buckets, cat_en, theme) == "متفرقه":
                    report["unreachable"].append((cat_en, theme))
            else:
                theme = theme_for(by_name[cat_en], cat_en, buckets, report)
            out[lang].append(to_play(r, lang, theme, report))

    validate(out["en"], report, tag="en")
    validate(out["fa"], report, tag="fa")
    # every category must render the same subtitle in both languages
    for r_en, r_fa in zip(out["en"], out["fa"]):
        if persian_subtitle(buckets, r_fa["category"], r_fa["theme"]) == "متفرقه":
            report["unreachable"].append((r_fa["category"], "fa"))

    print("rows: %d english, %d persian (%d source + %d final)"
          % (len(out["en"]), len(out["fa"]), len(source), len(finals)))
    print("complete categories: %s" % json.dumps(report["categories"], ensure_ascii=False))
    print("bucket assignments matched: %d/%d" % (len(names & set(by_name)), len(names)))
    if report["index_repaired"]:
        print("correct-index repaired on %d rows" % len(report["index_repaired"]))
    if report["forced"]:
        seen = {}
        for cat, want, got, kw in report["forced"]:
            seen.setdefault((cat, want, got, kw), 0)
            seen[(cat, want, got, kw)] += 1
        print("category names forced their own bucket on %d categories:" % len(seen))
        for (cat, want, got, kw), n in seen.items():
            print("   %-46s wanted %-16s %-12r wins -> %s" % (cat[:46], want, kw, got))
    if report["unreachable"]:
        print("unreachable (would print متفرقه): %s" % report["unreachable"][:10])

    dist = {}
    for r in out["fa"]:
        dist[persian_subtitle(buckets, r["category"], r["theme"])] = dist.get(
            persian_subtitle(buckets, r["category"], r["theme"]), 0) + 1
    print("rendered subtitle spread (english board, persian cell):")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print("   %-22s %d" % (k, v))

    if args.check:
        print("\n--check: nothing written")
        return

    os.makedirs(BANKS, exist_ok=True)
    en = os.path.join(BANKS, "bank-en.js")
    fa = os.path.join(BANKS, "bank-fa.js")
    a = emit(en, COURSE_GLOB, out["en"], "Iran in World Politics -- English bank")
    b = emit(fa, COURSE_GLOB + "_FA", out["fa"], "Iran in World Politics -- Persian bank")
    print("\nwrote %s (%d KB)" % (en, a // 1024))
    print("wrote %s (%d KB)" % (fa, b // 1024))


if __name__ == "__main__":
    main()
