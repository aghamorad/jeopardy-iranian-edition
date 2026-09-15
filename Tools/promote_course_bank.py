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
`historical_period` takes the single value "Contemporary Iran" for the same
reason: a true coarse label beats 141 invented precise ones.

The promotion has landed, so running the tool again would append a second copy of
every row; it refuses. `--check` is what to run from here: it rebuilds the rows
from the course and asserts the archive still carries each one unchanged, which
is the only way the two can drift apart now. It is a gate, not a one-shot.
"""

import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = "iran-in-world-politics"

BANK_EN = "Web/courses/%s/data/bank-en.js" % COURSE
BANK_FA = "Web/courses/%s/data/bank-fa.js" % COURSE
ARCH_EN = "QuestionBank/verified_clues.json"
ARCH_FA = "QuestionBank/verified_clues_fa.json"

FA_COPY = ["QuestionBank/persian_clues.json", "App/Resources/persian_clues.json"]

PROMOTED = "promoted"
VERIFIED = "verified"

# The one era label promoted rows carry until a provenance pass assigns real ones.
PERIOD = "Contemporary Iran"

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


def row(en_row, fa_row):
    """One promoted clue, in archive shape, taking each language's own text."""
    rid = en_row["id"]
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
            "historical_period": PERIOD,
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


def promoted_pairs():
    en_bank = js_bank("COURSE_CLUES_IRAN_IN_WORLD_POLITICS", BANK_EN)
    fa_bank = js_bank("COURSE_CLUES_IRAN_IN_WORLD_POLITICS_FA", BANK_FA)
    if len(en_bank) != len(fa_bank):
        raise SystemExit("course banks differ in length: %d vs %d"
                         % (len(en_bank), len(fa_bank)))
    if [r["id"] for r in en_bank] != [r["id"] for r in fa_bank]:
        raise SystemExit("course banks disagree on id order")
    rows_en, rows_fa = [], []
    for a, b in zip(en_bank, fa_bank):
        x, y = row(a, b)
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
    rows_en, rows_fa = promoted_pairs()

    if check:
        # The promotion has landed, so "in step" means something different from
        # what it meant the first time: the rows it wrote are still in the
        # archive exactly as it rebuilt them. That catches the one way the two
        # can drift now -- an absorbed row edited by hand, or by a later pass
        # that did not come through here -- and it stays meaningful forever,
        # where re-running the append could only ever report a clash.
        bad = 0
        for path, rows in ((ARCH_EN, rows_en), (ARCH_FA, rows_fa)):
            have = dict((r["id"], r) for r in archive(path))
            drift = [r["id"] for r in rows if have.get(r["id"]) != r]
            if drift:
                bad = 1
                print("DRIFT  %s: %d of %d promoted rows are missing or changed "
                      "since the promotion (first: %s)"
                      % (path, len(drift), len(rows), drift[0]))
            else:
                print("ok     %s carries all %d promoted rows unchanged"
                      % (path, len(rows)))
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
