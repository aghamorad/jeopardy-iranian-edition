#!/usr/bin/env python3
"""Promote a course edition's clue bank into MAIN's archive.

MAIN absorbs a course; the course is never touched. A course bank is authored in
play shape (`Web/courses/<id>/data/bank-en.js`, 17 keys, `window.COURSE_CLUES_<ID>`);
MAIN's record is the 27-field archive. This tool reads one and appends the other.
The course files are opened read-only here, always.

Most of the map is mechanical -- renames, an option rotation so the answer sits at
index 0, a slugged `source_id`, and the constants MAIN already uses on every row
(`confidence` 1.0, `evidence_type` "established_fact").

Three fields have no counterpart in a course bank and are NOT derivable:

    supporting_passage      the quoted evidence behind the clue
    distractor_rationales   why each of the three wrong options is wrong
    historical_period       the era label

Both of the first two are archive-only -- `render_bank.py` ships `passage` but
nothing in `Web/` reads it, and `distractor_rationales` never reaches the play
file at all -- so a player sees no difference. They land empty and the row is
marked `editorial_validation_status: "promoted"` rather than "verified". The gates
require rationales and a passage only on rows marked verified, and print how many
promoted rows are still undressed, so the debt is counted rather than hidden.

`historical_period` is coarse on purpose -- one true era label beats 512 invented
precise ones -- but it is coarse *per course*, not one value for the tool. It is
looked up in PERIODS below and a course that is not in that table is a hard stop,
because the alternative is stamping the wrong century onto a whole bank in a field
nothing downstream re-checks. MAIN is contemporary; the Qajars are not.

The course is an argument, so this is not a one-off for `iran-in-world-politics`:

    python3 Tools/promote_course_bank.py qajars           # append
    python3 Tools/promote_course_bank.py qajars --check   # the gate

Appending refuses if any rebuilt row is already in MAIN, because a second run
would double every one of them. `--check` is the standing gate and asks a
different question: it rebuilds the rows from the course bank and looks each one
up in the archive by id. For a course that has been promoted that is drift
detection; for one that has not, every row comes back ABSENT -- which is the
failure MAIN's absorption rule is meant to produce, and why an unpromoted course
now fails its own build.
"""

import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_COURSE = "iran-in-world-politics"

ARCH_EN = "QuestionBank/verified_clues.json"
ARCH_FA = "QuestionBank/verified_clues_fa.json"

FA_COPY = ["QuestionBank/persian_clues.json", "App/Resources/persian_clues.json"]

PROMOTED = "promoted"
VERIFIED = "verified"

# One era label per course, until a provenance pass assigns finer ones. A course
# that is missing here stops the run: the failure this prevents is a bank of
# Qajar clues filed as "Contemporary Iran", which no checker would ever catch.
PERIODS = {
    "iran-in-world-politics": "Contemporary Iran",
    "qajars": "Qajar",
}


def bank_paths(course):
    return ("Web/courses/%s/data/bank-en.js" % course,
            "Web/courses/%s/data/bank-fa.js" % course)


def bank_glob(course):
    """The course's global, by the same rule the converter names it."""
    return "COURSE_CLUES_" + course.replace("-", "_").upper()

# MAIN's generic chapter marker; `chapter` is not shipped and not validated.
CHAPTER = "Historical Corpus"

DIFFICULTY = {
    ("single", 200): "CASUAL",
    ("single", 400): "STANDARD",
    ("single", 600): "STANDARD",
    ("single", 800): "SCHOLAR",
    ("single", 1000): "INSUFFERABLE",
    ("double", 400): "STANDARD",
    ("double", 800): "STANDARD",
    ("double", 1200): "SCHOLAR",
    ("double", 1600): "SCHOLAR",
    ("double", 2000): "INSUFFERABLE",
}

# The archive's own key order. Anything written here must match it.
KEY_ORDER = [
    "id", "language", "category", "historical_period", "theme", "difficulty",
    "value", "round", "clue_text", "canonical_answer", "accepted_aliases",
    "partial_answers", "specificity_prompt", "options", "correct_option_index",
    "distractor_rationales", "explanation", "source_id", "book_title", "author",
    "chapter", "page", "supporting_passage", "evidence_type", "confidence",
    "editorial_validation_status", "host_reactions",
]


def js_bank(name, path):
    """Slice a `window.<NAME>=[...];` bank out of its JS wrapper.

    Anchored on the `=` so the Persian global, whose name carries the English
    one as a prefix, cannot be mistaken for it.
    """
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    anchor = "window.%s=" % name
    if anchor not in text:
        anchor = re.search(r"window\.%s\s*=" % re.escape(name), text).group(0)
    start = text.index("[", text.index(anchor))
    return json.JSONDecoder().raw_decode(text, start)[0]


def archive(path):
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    start = text.index("[")
    return json.JSONDecoder().raw_decode(text, start)[0]


def slug(text):
    text = unicodedata.normalize("NFKD", str(text))
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return re.sub(r"_+", "_", text)


def surname(author):
    """`Abbas Amanat` -> `amanat`. Titles are dropped, not initialled."""
    parts = [p for p in re.split(r"\s+", str(author).strip()) if p]
    for p in reversed(parts):
        if re.fullmatch(r"[A-Z][a-z'’\-]+\.?", p):
            return slug(p.rstrip("."))
    return slug(parts[-1]) if parts else "unknown"


def source_id(row):
    return "_".join([surname(row["author"]), slug(row["book"])[:48]]).strip("_")


def rotate(options, answer):
    """Put the answer at index 0, the index MAIN writes on every row."""
    opts = list(options)
    i = opts.index(answer)
    return [opts[i]] + opts[:i] + opts[i + 1:]


def aliases(en_row, fa_row):
    """MAIN keeps one alias list for both languages, Latin and Persian together."""
    out = []
    for a in list(en_row.get("aliases") or []) + list(fa_row.get("aliases") or []):
        if a not in out:
            out.append(a)
    return out


def row(en_row, fa_row, period):
    """One promoted clue, in archive shape, taking each language's own text."""
    rid = en_row["id"]

    # `source_id()` needs both, and a bare KeyError here reads as a broken tool
    # rather than a broken row -- which is how the Iran course's `final_snapback`
    # sat in this gate unnoticed: it carries no book and no author, so the
    # promoter died on it before it could compare anything.
    for field in ("book", "author"):
        for lang, src in (("en", en_row), ("fa", fa_row)):
            if not src.get(field):
                raise SystemExit(
                    "%s: the %s course row carries no %s. MAIN cites a source "
                    "on every row, so this one cannot be promoted." % (rid, lang, field))

    difficulty = DIFFICULTY.get((en_row["round"], en_row["value"]))
    if en_row["round"] == "final":
        difficulty = "INSUFFERABLE"
    if difficulty is None:
        raise SystemExit("%s: (%s, %s) is not on any value ladder"
                         % (rid, en_row["round"], en_row["value"]))

    def side(src, lang):
        answer = src["answer"]
        return {
            "language": lang,
            "category": src["category"],
            "clue_text": src["clue"],
            "canonical_answer": answer,
            "options": rotate(src["options"], answer),
            "explanation": src["explanation"],
            "correct_generic": src["correctLine"],
            "wrong_generic": src["wrongLine"],
        }

    en, fa = side(en_row, "en"), side(fa_row, "fa")
    if en["canonical_answer"] != fa["canonical_answer"] and not fa["canonical_answer"]:
        raise SystemExit("%s: Persian row carries no answer" % rid)

    out = []
    for lang, own in (("en", en), ("fa", fa)):
        out.append({
            "id": rid,
            "language": lang,
            "category": own["category"],
            "historical_period": period,
            "theme": en_row["theme"],
            "difficulty": difficulty,
            "value": en_row["value"],
            "round": en_row["round"],
            "clue_text": own["clue_text"],
            "canonical_answer": own["canonical_answer"],
            "accepted_aliases": aliases(en_row, fa_row),
            "partial_answers": [],
            "specificity_prompt": "",
            "options": own["options"],
            "correct_option_index": 0,
            "distractor_rationales": [],
            "explanation": own["explanation"],
            "source_id": source_id(en_row),
            "book_title": en_row["book"],
            "author": en_row["author"],
            "chapter": CHAPTER,
            "page": en_row["page"] if en_row["round"] != "final" else None,
            "supporting_passage": "",
            "evidence_type": "established_fact",
            "confidence": 1.0,
            "editorial_validation_status": PROMOTED,
            "host_reactions": {
                "correct_generic": own["correct_generic"],
                "wrong_generic": own["wrong_generic"],
            },
        })
    for r in out:
        if list(r.keys()) != KEY_ORDER:
            raise SystemExit("%s: key order drifted" % rid)
    return out


def promoted_pairs(course):
    period = PERIODS.get(course)
    if period is None:
        raise SystemExit(
            "course '%s' has no era label in PERIODS. Add one -- it lands in "
            "historical_period on every row this tool writes, and nothing "
            "downstream re-checks it. Known: %s"
            % (course, ", ".join(sorted(PERIODS))))

    bank_en, bank_fa = bank_paths(course)
    glob = bank_glob(course)
    en_bank = js_bank(glob, bank_en)
    fa_bank = js_bank(glob + "_FA", bank_fa)
    if len(en_bank) != len(fa_bank):
        raise SystemExit("course banks differ in length: %d vs %d"
                         % (len(en_bank), len(fa_bank)))
    if [r["id"] for r in en_bank] != [r["id"] for r in fa_bank]:
        raise SystemExit("course banks disagree on id order")
    rows_en, rows_fa = [], []
    for a, b in zip(en_bank, fa_bank):
        x, y = row(a, b, period)
        rows_en.append(x)
        rows_fa.append(y)
    return rows_en, rows_fa


def append_json_array(path, rows, trailer):
    """Append to a pretty-printed array without disturbing a byte before it.

    The archive is indent=2 with no trailing newline in the English file and one
    in the Persian; both are reproduced exactly, because `render_bank.py --check`
    compares bytes and the whole point is that the settled rows never move.
    """
    raw = open(path, encoding="utf-8").read()
    head = raw[:raw.rindex("]")].rstrip()
    body = json.dumps(rows, indent=2, ensure_ascii=False)[1:-1].strip("\n")
    return head + ",\n" + body + "\n]" + trailer


def main():
    check = "--check" in sys.argv
    rest = [a for a in sys.argv[1:] if a != "--check"]
    if len(rest) > 1:
        raise SystemExit("usage: promote_course_bank.py [course-id] [--check]")
    course = rest[0] if rest else DEFAULT_COURSE

    if not os.path.exists(os.path.join(ROOT, bank_paths(course)[0])):
        raise SystemExit("no course bank at %s -- '%s' is not a course under "
                         "Web/courses/" % (bank_paths(course)[0], course))

    rows_en, rows_fa = promoted_pairs(course)

    if check:
        # Absent and changed are reported apart on purpose. Changed is the
        # original meaning of this check: a row the tool wrote, edited by hand
        # afterwards. Absent is a course whose bank never reached the archive at
        # all, and collapsing the two into one "missing or changed" line is how
        # an unpromoted course would read as mere drift.
        bad = 0
        for path, rows in ((ARCH_EN, rows_en), (ARCH_FA, rows_fa)):
            have = dict((r["id"], r) for r in archive(path))
            absent = [r["id"] for r in rows if r["id"] not in have]
            changed = [r["id"] for r in rows
                       if r["id"] in have and have[r["id"]] != r]
            if absent:
                bad = 1
                print("ABSENT %s: %d of %d rows from '%s' are not in MAIN "
                      "(first: %s). Promote the course -- MAIN absorbs a "
                      "course's whole bank, and this one did not."
                      % (path, len(absent), len(rows), course, absent[0]))
            if changed:
                bad = 1
                print("DRIFT  %s: %d rows from '%s' changed in MAIN after the "
                      "promotion (first: %s). The course bank is the source; "
                      "re-promote or revert the archive row."
                      % (path, len(changed), course, changed[0]))
            if not absent and not changed:
                print("ok     %s carries all %d rows from '%s' unchanged"
                      % (path, len(rows), course))
        return bad

    old_en = archive(ARCH_EN)
    old_fa = archive(ARCH_FA)
    ids = set(c["id"] for c in old_en)
    clash = [r["id"] for r in rows_en if r["id"] in ids]
    if clash:
        raise SystemExit("promoted ids already in MAIN: %s — this appends, and "
                         "a second run would double every row. Use --check to "
                         "see whether the rows it wrote are still intact."
                         % clash[:5])

    for path, rows, old in ((ARCH_EN, rows_en, old_en), (ARCH_FA, rows_fa, old_fa)):
        full = os.path.join(ROOT, path)
        trailer = "\n" if open(full, encoding="utf-8").read().endswith("\n") else ""
        want = append_json_array(full, rows, trailer)
        open(full, "w", encoding="utf-8").write(want)
        total = len(json.loads(want))
        print("wrote  %s  (%d rows, +%d)" % (path, total, total - len(old)))

    write_fa_copy(rows_fa)
    return 0


def write_fa_copy(rows_fa):
    """The Persian copy dictionaries the Swift shells read, keyed by id."""
    see = {}
    for path in FA_COPY:
        real = os.path.realpath(os.path.join(ROOT, path))
        if real in see:
            print("skip   %s (same file as %s)" % (path, see[real]))
            continue
        see[real] = path
        data = json.load(open(real, encoding="utf-8"))
        added = 0
        for r in rows_fa:
            if r["id"] in data:
                continue
            data[r["id"]] = {
                "clue_text": r["clue_text"],
                "canonical_answer": r["canonical_answer"],
                "options": r["options"],
                "explanation": r["explanation"],
                "specificity_prompt": "",
            }
            added += 1
        json.dump(data, open(real, "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        print("wrote  %s  (+%d entries)" % (path, added))


if __name__ == "__main__":
    sys.exit(main())
