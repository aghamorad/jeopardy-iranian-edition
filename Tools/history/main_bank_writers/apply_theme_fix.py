#!/usr/bin/env python3
"""
Splice fourth-book replacement rows into MAIN's archive, in place.

A category is a theme: five clues, at least three different books, never more
than two clues from any one book. A *stacked* category takes three from one
book and cannot be fixed by shuffling -- one of its five rows has to be
rewritten from a different book. That rewrite is authored (see
QuestionBank/incoming/theme-fix-BRIEF.md) and lands through this script, which
holds the row's identity, its rung and its category fixed and takes only the
content from the authored row.

Every authored row is checked against QuestionBank/incoming/
theme-repair-candidates.md: the book, author, page, chapter and source_id must
be copied off a candidate line, and the supporting passage must appear verbatim
in that candidate's quoted sentence. A citation that cannot be traced back to
the sheet is the defect this exists to catch -- nobody can read 3,700 rows
against 50 books by hand.

Usage:
    python3 Tools/apply_theme_fix.py theme-fix-1 theme-fix-2 ...   [--dry-run]

Each stem resolves to QuestionBank/incoming/<stem>-en.json and <stem>-fa.json.
Run Tools/render_bank.py afterwards; this script never writes a play file.
"""
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter, defaultdict

CANDIDATES = "QuestionBank/incoming/theme-repair-candidates.md"
EN = "QuestionBank/verified_clues.json"
FA = "QuestionBank/verified_clues_fa.json"
BRIEF = "QuestionBank/incoming/theme-fix-BRIEF.md"

CONTENT_KEYS = [
    "clue_text", "canonical_answer", "accepted_aliases", "options",
    "correct_option_index", "distractor_rationales", "explanation",
    "source_id", "book_title", "author", "chapter", "page",
    "supporting_passage", "evidence_type", "confidence",
    "editorial_validation_status", "host_reactions",
]
FIXED_KEYS = [
    "id", "language", "category", "historical_period", "theme",
    "difficulty", "value", "round", "partial_answers", "specificity_prompt",
]
ALL_KEYS = set(FIXED_KEYS) | set(CONTENT_KEYS)
EVIDENCE = {"established_fact", "scholarly_interpretation", "primary_testimony"}
SPACE = re.compile(r"\s+")
ARABIC = re.compile(r"[؀-ۿﭐ-﷿ﹰ-﻿]")
QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "«": '"', "»": '"'})


def norm(text):
    return SPACE.sub(" ", unicodedata.normalize("NFC", str(text)).translate(QUOTES)).strip()


def fold(text):
    """Answer comparison: case, articles, punctuation and spacing all stop mattering."""
    t = norm(text).casefold()
    t = re.sub(r"[^\w\s؀-ۿ]", " ", t)
    t = re.sub(r"\b(the|a|an|el|al|of|d[eu])\b", " ", t)
    return SPACE.sub(" ", t).strip()


CAND_LINE = re.compile(r"^- \*\*(.+?)\*\* \| (.+?) \| p(\S+) \| (.*?) \| (\S+) \| (.*)$")


def load_candidates():
    """-> list of candidate dicts, each tagged with the section it sits under.

    Single pass on purpose. The same candidate is offered under more than one
    removable row, so the file carries the same line several times; matching
    quote lines back to candidates by their text would pair them wrongly.
    """
    out = []
    section = None
    heading = None
    cur = None
    with open(CANDIDATES, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                section = line[3:].strip()
                heading = None
                cur = None
                continue
            if line.startswith("### "):
                # "### if you remove the 200 row (id `x`, CASUAL) — candidates at ranks 1-2"
                # says which removable row this block of candidates was offered for.
                heading = line[4:].strip()
                cur = None
                continue
            m = CAND_LINE.match(line)
            if m:
                answer, book, page, chapter, sheet, author = m.groups()
                author = re.sub(r"←.*$", "", author).replace("*", "").strip()
                cur = {
                    "section": section, "heading": heading, "answer": answer.strip(),
                    "book": book.strip(), "page": page.strip(),
                    "chapter": chapter.strip(), "source_id": sheet.strip(),
                    "author": author, "quote": "", "fact": "", "raw": line,
                }
                out.append(cur)
                continue
            if cur is None:
                continue
            body = line.strip()
            if body.startswith("quote:"):
                cur["quote"] = body[len("quote:"):].strip().strip('"').strip()
            elif body.startswith("fact:"):
                cur["fact"] = body[len("fact:"):].strip()
    return out


HEADING_ID = re.compile(r"id `([^`]+)`")


def rung_of(candidate):
    """The row id this block of candidates was offered to replace, if stated."""
    m = HEADING_ID.search(candidate.get("heading") or "")
    return m.group(1) if m else None


def section_for_row_id(cands, row_id):
    """The section that files candidates for this row.

    Sections are titled in English, but a Persian row carries the Persian
    category title -- so joining on the category name works for one language
    and silently finds nothing for the other. The headings name the row id
    instead, and a row id belongs to exactly one category, so that is the join.
    """
    for c in cands:
        if rung_of(c) == row_id:
            return c["section"]
    return None


def find_candidate(cands, category, round_, row, row_id):
    """Locate the candidate an authored row claims. Returns (candidate, errors)."""
    want_section = section_for_row_id(cands, row_id) or "%s | %s" % (round_.upper(), category)
    answer = fold(row["canonical_answer"])
    pool = [c for c in cands if c["section"] == want_section]
    if not pool:
        return None, ["no candidate section %r" % want_section]
    exact = [c for c in pool if fold(c["answer"]) == answer]
    if not exact:
        near = [c["answer"] for c in pool if answer[:18] in fold(c["answer"]) or fold(c["answer"])[:18] in answer]
        return None, ["answer %r is not a candidate in %s%s" % (
            row["canonical_answer"], want_section,
            " (near: %s)" % ", ".join(near[:4]) if near else "")]
    # The sheet files each candidate under the row it fits. A candidate offered
    # for the 800 rung is not a candidate for the 200.
    on_rung = [c for c in exact if rung_of(c) == row_id]
    if on_rung:
        return on_rung[0], []
    offered = sorted({rung_of(c) or "?" for c in exact})
    return exact[0], ["the sheet offers this candidate for %s, not for %s — the rung is "
                      "fixed, pick a candidate filed under %s or replace a different row"
                      % (", ".join(offered), row_id, row_id)]


def check_row(row, fixed_row, cands, label, lookup_answer=None):
    errs = []
    extra = set(row) - ALL_KEYS
    missing = ALL_KEYS - set(row)
    if extra:
        errs.append("unknown keys %s" % sorted(extra))
    if missing:
        errs.append("missing keys %s" % sorted(missing))
        return errs

    for k in ("round", "value", "difficulty", "category"):
        if row[k] != fixed_row[k]:
            errs.append("%s changed: %r -> %r" % (k, fixed_row[k], row[k]))
    for k in ("historical_period", "theme"):
        if row[k] != fixed_row[k]:
            print("    note %s: %s retagged %r -> %r" % (label, k, fixed_row[k], row[k]))

    if row["language"] != ("en" if label == "EN" else "fa"):
        errs.append("language is %r" % row["language"])
    if row["correct_option_index"] != 0:
        errs.append("correct_option_index is %r, must be 0" % row["correct_option_index"])
    opts = row["options"]
    if not isinstance(opts, list) or len(opts) != 4 or any(not isinstance(o, str) or not o.strip() for o in opts):
        errs.append("options is not four non-empty strings")
    elif len({fold(o) for o in opts}) != 4:
        errs.append("options repeat")
    elif opts[0] != row["canonical_answer"]:
        errs.append("options[0] != canonical_answer")
    if not row["canonical_answer"].strip():
        errs.append("empty canonical_answer")
    clue = fold(row["clue_text"])
    if fold(row["canonical_answer"]) and fold(row["canonical_answer"]) in clue:
        errs.append("the clue contains its own answer")
    for o in opts[1:] if isinstance(opts, list) and len(opts) == 4 else []:
        if len(fold(o)) > 8 and fold(o) in clue:
            errs.append("a distractor (%r) appears in the clue" % o)
    if not row["accepted_aliases"]:
        errs.append("no aliases")
    elif not any(fold(a) == fold(row["canonical_answer"]) for a in row["accepted_aliases"]):
        errs.append("aliases do not include the canonical answer")
    # check_alias_ownership fails a row whose alias is one of its own wrong
    # options, because the judge would then accept a distractor as right.
    wrong_fold = {fold(o) for o in opts[1:]} if isinstance(opts, list) and len(opts) == 4 else set()
    for a in row["accepted_aliases"]:
        if fold(a) in wrong_fold:
            errs.append("alias %r is one of its own wrong options" % a)
    rats = row["distractor_rationales"]
    if not isinstance(rats, list) or len(rats) != 3:
        errs.append("needs exactly 3 distractor_rationales, has %s" % len(rats))
    else:
        for d in rats:
            if set(d) != {"option", "why_plausible", "why_wrong"}:
                errs.append("rationale keys are %s" % sorted(d))
            elif not d["why_plausible"].strip() or not d["why_wrong"].strip():
                errs.append("rationale for %r is empty" % d["option"])
        if all(set(d) == {"option", "why_plausible", "why_wrong"} for d in rats):
            if {fold(d["option"]) for d in rats} != {fold(o) for o in opts[1:]}:
                errs.append("rationales do not match the three wrong options")
    hr = row["host_reactions"]
    if not isinstance(hr, dict) or set(hr) != {"correct_generic", "wrong_generic"}:
        errs.append("host_reactions keys are %s" % sorted(hr) if isinstance(hr, dict) else "host_reactions is not an object")
    elif not hr["correct_generic"].strip() or not hr["wrong_generic"].strip():
        errs.append("a host line is empty")
    if not row["supporting_passage"].strip():
        errs.append("no supporting_passage")
    if row["evidence_type"] not in EVIDENCE:
        errs.append("evidence_type %r" % row["evidence_type"])
    if row["confidence"] != 1.0:
        errs.append("confidence %r" % row["confidence"])
    if row["editorial_validation_status"] != "verified":
        errs.append("status is %r" % row["editorial_validation_status"])
    if row["partial_answers"] != [] or row["specificity_prompt"] != "":
        errs.append("partial_answers/specificity_prompt must be empty")
    if not isinstance(row["page"], int):
        errs.append("page is %r, must be an integer" % row["page"])

    if label == "EN" and ARABIC.search(row["clue_text"]):
        errs.append("English clue carries Persian script")
    for field, value in (("book_title", row["book_title"]), ("author", row["author"])):
        if norm(value).casefold() in clue:
            errs.append("the clue names its %s" % field)

    cand, cerrs = find_candidate(cands, fixed_row["category"], fixed_row["round"],
                                 {"canonical_answer": lookup_answer or row["canonical_answer"]},
                                 fixed_row["id"])
    errs += cerrs
    if cand:
        for k, ck in (("book_title", "book"), ("author", "author"), ("source_id", "source_id"), ("chapter", "chapter")):
            if norm(row[k]) != norm(cand[ck]):
                errs.append("%s is %r but the candidate cites %r" % (k, row[k], cand[ck]))
        if str(row["page"]) != cand["page"]:
            errs.append("page is %r but the candidate says p%s" % (row["page"], cand["page"]))
        passage = norm(row["supporting_passage"])
        haystack = norm(cand["quote"] + " || " + cand["fact"])
        if passage not in haystack:
            errs.append("supporting_passage is not in the candidate's quote: %r" % passage[:90])
    return errs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    for stem in args:
        if not re.fullmatch(r"[\w.-]+", stem):
            sys.exit("bad stem %r" % stem)

    cands = load_candidates()
    en_rows = json.load(open(EN, encoding="utf-8"))
    fa_rows = json.load(open(FA, encoding="utf-8"))
    en_ix = {r["id"]: i for i, r in enumerate(en_rows)}
    fa_ix = {r["id"]: i for i, r in enumerate(fa_rows)}
    if len(en_ix) != len(en_rows):
        sys.exit("duplicate ids in the English archive")

    loaded = {"EN": {}, "FA": {}}
    failed = 0
    for stem in args:
        for label in ("EN", "FA"):
            path = "QuestionBank/incoming/%s-%s.json" % (stem, label.lower())
            try:
                loaded[label][stem] = (path, json.load(open(path, encoding="utf-8")))
            except Exception as exc:
                print("FAIL %s: %s" % (path, exc))
                failed += 1
    if failed:
        sys.exit("\n%d file(s) missing or unreadable; nothing written." % failed)

    # A Persian row asks its own question, so its canonical answer is the
    # Persian form and cannot be looked up in the sheet, which is keyed on the
    # English answers. Its English partner in the same batch names the
    # candidate, and both rows must then cite the same book and page.
    en_partner = {}
    for _stem, (_path, rows) in loaded["EN"].items():
        for r in rows:
            en_partner.setdefault(r.get("id"), r)

    staged = {"EN": [], "FA": []}
    for stem in args:
        for label in ("EN", "FA"):
            path, rows = loaded[label][stem]
            ix = en_ix if label == "EN" else fa_ix
            archive = en_rows if label == "EN" else fa_rows
            print("\n%s  (%d row(s))" % (path, len(rows)))
            for row in rows:
                rid = row.get("id", "<no id>")
                errors = []
                lookup = None
                if rid not in ix:
                    errors = ["id is not in the archive"]
                else:
                    if label == "FA":
                        partner = en_partner.get(rid)
                        if partner is None:
                            errors = ["the batch carries no English row with this id"]
                        else:
                            lookup = partner.get("canonical_answer")
                    if not errors:
                        errors = check_row(row, archive[ix[rid]], cands, label, lookup)
                if errors:
                    failed += 1
                    print("  FAIL %s" % rid)
                    for e in errors:
                        print("        %s" % e)
                else:
                    staged[label].append(row)
                    print("  ok   %s  %s" % (rid, row["canonical_answer"][:52]))

    if failed:
        sys.exit("\n%d row(s) failed; nothing written." % failed)

    ids = [r["id"] for r in staged["EN"]]
    if sorted(ids) != sorted(r["id"] for r in staged["FA"]):
        sys.exit("English and Persian batches do not carry the same ids")
    if len(set(ids)) != len(ids):
        sys.exit("the same row is claimed twice")

    # The whole point: measure each category's book spread as it will stand
    # *after* the splice, not as it stands now. And the same pass catches the
    # two other ways one new row can break a column that already passes.
    thin = 0
    for label, rows in (("EN", staged["EN"]), ("FA", staged["FA"])):
        archive = en_rows if label == "EN" else fa_rows
        new_row = {r["id"]: r for r in rows}
        by_cat = defaultdict(list)
        by_cat_rows = defaultdict(list)
        for r in archive:
            if r["round"] != "final":
                by_cat[r["category"]].append(new_row.get(r["id"], r)["book_title"])
                by_cat_rows[r["category"]].append(new_row.get(r["id"], r))
        print("\nbook spread after the splice (%s):" % label)
        for cat in sorted({r["category"] for r in rows}):
            c = Counter(by_cat[cat])
            top, n = c.most_common(1)[0]
            bad = n > 2 or len(c) < 3 or sum(c.values()) != 5
            # check_category_answer_repeats: one rung, one answer. A column that
            # asks the same thing at two rungs is the theme running out of
            # subjects, and it fails the sweep.
            at = defaultdict(set)
            for r in by_cat_rows[cat]:
                if fold(r["canonical_answer"]):
                    at[fold(r["canonical_answer"])].add(r["value"])
            for answer, rungs in at.items():
                if len(rungs) > 1:
                    bad = True
                    print("  FAIL %s: %r sits at %s" % (cat, answer, sorted(rungs)))
            thin += 1 if bad else 0
            print("  %s %-42s %d clue(s) from %d book(s), worst %s x%d" % (
                "FAIL" if bad else "ok  ", cat, sum(c.values()), len(c), top[:30], n))
    if thin:
        sys.exit("\n%d categor(y/ies) would still be stacked, thin, or answering "
                 "the same thing twice; nothing written." % thin)

    if dry:
        sys.exit("\ndry run: %d row(s) per language would be spliced." % len(staged["EN"]))

    for label, rows, ix, path, rows_all in (
            ("EN", staged["EN"], en_ix, EN, en_rows),
            ("FA", staged["FA"], fa_ix, FA, fa_rows)):
        backup = path + ".pre-theme-fix2"
        try:
            open(backup, "x").close()
            shutil.copy2(path, backup)
        except FileExistsError:
            pass
        for r in rows:
            target = rows_all[ix[r["id"]]]
            if target["language"] != r["language"]:
                sys.exit("language mismatch on %s" % r["id"])
            for k in CONTENT_KEYS:
                target[k] = r[k]
        out = json.dumps(rows_all, indent=2, ensure_ascii=False)
        if json.loads(out) != rows_all:
            sys.exit("re-serialization of %s did not round-trip" % path)
        open(path, "w", encoding="utf-8").write(out)
        print("spliced %d row(s) into %s (backup %s)" % (len(rows), path, backup))

    print("\nNow run: python3 Tools/render_bank.py")
    print("Then:   python3 Tools/check_repeats.py --bank")


if __name__ == "__main__":
    main()
