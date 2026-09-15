#!/usr/bin/env python3
"""Check a play-shaped bank: the file the browser actually loads.

`validate_1000_clues.py` and `validate_persian_bank.py` check the *archive*.
Nothing has ever checked the play file's contents — `verify_flawless_state.py`
looks at its row count and nothing else — so a generator bug ships silently.
This closes that gap, and it is also the only thing that checks a course
edition's bank, which has no archive behind it at all.

    python3 Tools/check_bank.py Web/data/clues.js
    python3 Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js
    python3 Tools/check_bank.py Web/courses/iran-in-world-politics/data/bank-en.js \\
        --fa Web/courses/iran-in-world-politics/data/bank-fa.js \\
        --edition Web/courses/iran-in-world-politics/course.js

`--archive` reads MAIN's canonical rows instead of a play file:

    python3 Tools/check_bank.py QuestionBank/verified_clues.json --archive \\
        --fa QuestionBank/verified_clues_fa.json

The archive carries four fields the play file never sees — `distractor_rationales`
above all — so the archive is the only place the rationale rules can be checked,
and the play file is the only place the button rules can. Both shapes are mapped
onto one set of row rules (`play_view`), so a rule is written once and holds
wherever the row can be checked at all.

Exit status is 1 if any ERROR was found, 0 otherwise. Warnings never fail a run.
`--verbose` adds per-row auditing aids that are deliberately not warnings: they
fire on words the clue is entitled to use, and are for reading one row at a time.

Read-only. Nothing here writes to a bank.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

# ── The ladders. `value` is the engine's slot key; the tile prints toman. ─────

LADDERS = {
    "single": [200, 400, 600, 800, 1000],
    "double": [400, 800, 1200, 1600, 2000],
    "final": [0],
}

# `difficulty` tracks the rung 1:1 across all 1,000 shipped rows. It is derived.
RUNG_DIFFICULTY = {
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
    ("final", 0): "INSUFFERABLE",
}

# Fields the engine reads. A missing one is a silent blank, not a crash.
CORE_KEYS = [
    "id", "round", "value", "category", "difficulty", "options",
    "clue", "answer", "aliases", "correct", "correctLine", "wrongLine",
]
# Provenance. The main bank carries all of these. A course bank is written from
# a syllabus rather than one book, so `passage` and `period` are MAIN's own —
# but `book`, `author` and `page` are the source line either way, and a course
# carries them too (all 693 rows of the one course do). What is required where is
# `check_citations`.
PROVENANCE_KEYS = ["book", "page", "passage", "author", "period"]

# `window.CLUES` / `_FA` is MAIN. Anything else is a course, and the only part
# of its global an agent is promised is the name: `COURSE_CLUES_<ID>` (+ `_FA`),
# where the id is the folder under `Web/courses/`. So the id is matched as an
# open run of name characters on either side of `CLUES` rather than enumerated —
# a new course must not need an edit here.
MARKER = re.compile(r"\b(window\.(?:[A-Z0-9_]*_)?CLUES(?:_[A-Z0-9_]+)?)\s*=")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MAIN absorbed a course's bank: every row of `Web/courses/<id>/data/bank-*.js`
# now also sits in MAIN's archive and its play file. Which ones is recorded in
# exactly one place — `editorial_validation_status` in the archive, which
# `render_bank.py` does not ship — so a rule that has to tell an absorbed row
# from MAIN's own asks the archive. Keyed by the bank's path from the repo root
# so a frozen copy under `Versions/` cannot borrow today's answer, and so a
# course bank (which has no archive behind it) simply matches nothing.
PROMOTED = "promoted"
ARCHIVE_FOR = {
    "Web/data/clues.js": "QuestionBank/verified_clues.json",
    "Web/data/clues_fa.js": "QuestionBank/verified_clues_fa.json",
}

ERRORS = []
WARNINGS = []
NOTES = []

# Answer words that show up in many different rows' answers. Such a word
# appearing in a clue gives almost nothing away — a question about Tehran that
# says "Tehran" is not captain obvious — so the token-level leak check consults
# this and stays quiet. Rebuilt per bank in report().
COMMON_ANSWER_TOKENS = set()

# Set by --verbose. Enables the high-false-positive auditing aids.
VERBOSE = False


def error(msg):
    ERRORS.append(msg)


def warn(msg):
    if msg not in WARNINGS:
        WARNINGS.append(msg)


def note(msg):
    if msg not in NOTES:
        NOTES.append(msg)


# ── Reading ──────────────────────────────────────────────────────────────────


def load(path, archive=False):
    """Read the array out of a `window.X = [...]` bank file, or an archive.

    The assignment is matched whole — marker, whitespace, `=`. A bare
    `text.find(marker)` stops at the wrong place, because `window.CLUES` is a
    prefix of `window.CLUES_FA`, and `window.COURSE_CLUES_X` of
    `window.COURSE_CLUES_X_FA`: the search would take the marker's position and
    then hand back the Persian array while calling it English.

    Three shapes are accepted, and nothing else is: MAIN's `window.CLUES`
    (`_FA`), and a course's `window.COURSE_CLUES_<ID>` (`_FA`). Course banks
    never live in `window.CLUES`; that separation is the whole point of the
    global, so a bank still naming the engine's array is a defect, not a
    variant.

    With `archive=True` the file is MAIN's own archive — a bare JSON array of
    rows, no global around it — and the marker comes back as `<archive>`.
    Language then has to be told, because nothing in the file says it: every
    row carries `language`, but a bank that got that field wrong is exactly the
    thing worth checking, so the caller states which side it handed over.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if archive:
        return "<archive>", json.loads(text)
    at = MARKER.search(text)
    if not at:
        raise ValueError(
            "no `window.CLUES = [...]` (MAIN) or `window.COURSE_CLUES_<ID> = "
            "[...]` (course) assignment in %s" % path)
    return at.group(1), json.loads(text[text.index("[", at.end()):text.rindex("]") + 1])


# Archive key -> play key, for the fields the two shapes spell differently.
ARCHIVE_TO_PLAY = {
    "clue": "clue_text",
    "answer": "canonical_answer",
    "aliases": "accepted_aliases",
    "correct": "correct_option_index",
    "book": "book_title",
    "passage": "supporting_passage",
    "period": "historical_period",
}


def play_view(row):
    """Rewrite an archive row into the play shape, so one rule set serves both.

    Every row rule below reads `clue`, `answer`, `aliases`, `correct` and the
    host's two lines. The archive says `clue_text`, `canonical_answer`,
    `accepted_aliases`, `correct_option_index`, and nests the host's lines under
    `host_reactions`. Rather than a second copy of each rule for the archive,
    the archive is renamed on the way in. The row itself is not touched: this
    returns a copy, and the archive is only ever read.
    """
    out = dict(row)
    for play_key, archive_key in ARCHIVE_TO_PLAY.items():
        if archive_key in row:
            out[play_key] = row[archive_key]
    reactions = row.get("host_reactions")
    if isinstance(reactions, dict):
        if "correct_generic" in reactions:
            out["correctLine"] = reactions["correct_generic"]
        if "wrong_generic" in reactions:
            out["wrongLine"] = reactions["wrong_generic"]
    return out


def promoted_ids(path, rows, archive=False):
    """Which of these rows MAIN absorbed from a course, by id.

    Read from the archive rather than the file handed in, because
    `editorial_validation_status` is an archive field. With `archive=True` the
    rows *are* the archive, so the answer is on the row. A bank with no archive
    behind it — a course's own, a snapshot — gets an empty set and is read as
    MAIN's own throughout, which is the safe direction to be wrong in.
    """
    if archive:
        return set(r.get("id") for r in rows
                   if r.get("editorial_validation_status") == PROMOTED)
    source = ARCHIVE_FOR.get(os.path.relpath(os.path.abspath(path), ROOT))
    if not source:
        return set()
    try:
        with open(os.path.join(ROOT, source), encoding="utf-8") as fh:
            canonical = json.loads(fh.read())
    except (OSError, ValueError):
        note("no readable archive at %s, so every row in %s is read as MAIN's "
             "own" % (source, os.path.basename(path)))
        return set()
    ids = set(r.get("id") for r in rows)
    return set(r.get("id") for r in canonical
               if r.get("editorial_validation_status") == PROMOTED
               and r.get("id") in ids)


def present(text):
    """The text as the button will carry it — the author's gloss taken off.

    `presentingOption` (`Web/app.js:297`) strips every parenthetical from an
    option before it reaches the board, in both scripts' brackets. Anything
    that reasons about what a player can see has to reason about this string:
    a rationale naming `Iraj` is naming its option correctly when the option
    reads `Iraj (Hossein Khajeh Amiri)`, and a distractor that reads `Iraj`
    beside that option is a board showing one name twice.
    """
    return re.sub(r"\s*[\(（][^\(\)（）]*[\)）]", "", str(text)).strip()


def normalise(s):
    """Fold a string down to what a giveaway test can compare.

    Persian needs more than casefolding: the Arabic and Persian forms of yeh and
    kaf are different code points that look identical, the diacritics are
    optional in writing, and the zero-width non-joiner is a word-internal mark.
    Two strings that a reader would call the same must compare equal here, or
    the answer-in-clue test reports a clean bank it never actually read.
    """
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = re.sub("[ً-ْٰـ]", "", s)          # harakat, tatweel
    s = s.replace("ي", "ی").replace("ك", "ک")   # yeh, kaf
    s = s.replace("أإآ", "ا")             # alef hamza forms
    s = s.replace("‌", "").replace("‏", "").replace("‎", "")
    s = re.sub(r"[^\w؀-ۿ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def words(norm):
    return [w for w in norm.split(" ") if w]


def related(alias, answer):
    """Could this alias plausibly be a way of writing this answer?

    Not a judgement — three refusals: same string, one contained in the other
    (`Iraj` inside `Iraj (Hossein Khajeh Amiri)`, `امیرکبیر` inside
    `میرزا تقی خان امیرکبیر`), or sharing a content word (`Reza Khan` /
    `Reza Shah Pahlavi`). Deliberately generous, because it is used as a floor:
    a row where *nothing* clears it is a row whose list came from elsewhere,
    which is the defect. A row where something does may still carry a bad
    entry, and that is the author's reading, not a machine's.
    """
    a, b = normalise(alias), normalise(answer)
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    if a.replace(" ", "") == b.replace(" ", ""):
        return True                       # `Ramhormoz` / `Ram Hormoz`
    if _initials(a) == _initials(b) and len(_initials(a)) >= 2:
        return True                       # `JCPOA` / `Joint Comprehensive Plan of Action`
    return bool((set(words(a)) - STOPWORDS) & (set(words(b)) - STOPWORDS))


def _initials(s):
    return "".join(w[0] for w in words(s) if w)


# ── Per-row checks ───────────────────────────────────────────────────────────

STOPWORDS = {
    "the", "a", "an", "of", "and", "in", "on", "at", "to", "for", "his", "her",
    "its", "their", "he", "she", "it", "who", "which", "this", "that", "was",
    "were", "is", "are", "by", "with", "as", "from", "not", "no",
}


def check_row(i, row, lang, latin_ok):
    rid = row.get("id", "<row %d has no id>" % i)
    where = "%s [%s]" % (rid, i)

    missing = [k for k in CORE_KEYS if k not in row]
    if missing:
        error("%s: missing key(s) %s — the engine reads these and gets undefined"
              % (where, ", ".join(missing)))
        return

    rnd, value = row["round"], row["value"]
    if rnd not in LADDERS:
        error("%s: round %r is not one of single/double/final" % (where, rnd))
    elif value not in LADDERS[rnd]:
        error("%s: round %s has no rung %r — must be one of %s"
              % (where, rnd, value, LADDERS[rnd]))
    else:
        want = RUNG_DIFFICULTY[(rnd, value)]
        if row["difficulty"] != want:
            error("%s: difficulty %r does not match rung %s/%s, which is %s"
                  % (where, row["difficulty"], rnd, value, want))

    if not str(row["category"]).strip():
        error("%s: empty category — it can never be dealt" % where)

    if not str(row["clue"]).strip():
        error("%s: empty clue text" % where)

    # exactly four options, distinct, and options[correct] is the answer
    opts = row["options"]
    if not isinstance(opts, list) or len(opts) != 4:
        error("%s: options is %s, not a list of four"
              % (where, "not a list" if not isinstance(opts, list) else
                 "a list of %d" % len(opts)))
    else:
        seen = Counter(normalise(o) for o in opts)
        dupes = [o for o, n in seen.items() if n > 1]
        if dupes:
            error("%s: options repeat (%s) — the answer is choiceable by shape"
                  % (where, ", ".join(sorted(dupes))))
        idx = row["correct"]
        if not isinstance(idx, int) or not 0 <= idx < len(opts):
            error("%s: correct index %r is not a position in options" % (where, idx))
        elif opts[idx] != row["answer"]:
            if normalise(opts[idx]) == normalise(row["answer"]):
                warn("%s: options[correct] %r differs from answer %r only in "
                     "spelling/accents" % (where, opts[idx], row["answer"]))
            else:
                error("%s: options[correct] is %r but the answer is %r — the "
                      "engine would mark the right choice wrong"
                      % (where, opts[idx], row["answer"]))
        if idx != 0:
            warn("%s: correct index is %d, not 0. Harmless — `shufflingOptions` "
                 "re-finds the right option by its text — but the house rule is to "
                 "store 0 everywhere and let the engine produce the spread, so this "
                 "one was done by hand." % (where, idx))

    if not isinstance(row["aliases"], list) or not row["aliases"]:
        error("%s: aliases is empty — only a byte-exact answer will be accepted"
              % where)

    # the one giveaway a machine can catch
    ans, clue = normalise(row["answer"]), normalise(row["clue"])
    if len(ans) >= 4 and ans and re.search(r"(?<!\w)" + re.escape(ans) + r"(?!\w)", clue):
        error("%s: the answer %r appears in its own clue text — captain obvious"
              % (where, row["answer"]))
    else:
        # weaker signal: the answer's own distinctive head word. "Distinctive"
        # is the operative word — a token that is the answer to many other rows
        # too carries no giveaway, so it is skipped rather than warned about.
        toks = [w for w in words(ans)
                if len(w) >= 5 and w not in STOPWORDS and w not in COMMON_ANSWER_TOKENS]
        if VERBOSE and toks and any(re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", clue)
                                    for t in toks):
            # Off by default. Roughly four rows in ten trip this, on words the
            # clue is entitled to use ("treaty", "mosque", "river"), because a
            # generic noun in both clue and answer is not a leak — the answer
            # still has to be the specific one. The whole-answer check above is
            # the defect class; this is an auditing aid for one row at a time.
            note("%s: a word from the answer (%s) also appears in the clue"
                 % (where, ", ".join(t for t in toks
                                     if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", clue))))

    for k in ("correctLine", "wrongLine"):
        if not str(row[k]).strip():
            warn("%s: %s is empty — the host falls back to the generic pool" % (where, k))

    # language contamination, kept crude on purpose
    if lang == "en":
        if re.search(r"[؀-ۿ]", str(row["clue"])):
            warn("%s: Persian script in the English bank" % where)
    elif lang == "fa" and not latin_ok:
        pass


def check_language_purity(rows, lang):
    """A bank that ships the wrong language plays under the other chrome, silently."""
    if lang != "en":
        return
    n = sum(1 for r in rows if re.search(r"[؀-ۿ]", str(r.get("clue", ""))))
    if n:
        warn("%d English row(s) carry Persian script in the clue text" % n)


def check_categories(rows, label):
    """Rung coverage, the deal floor, and the disjointness the board actually needs.

    A category is dealable when it carries a clue at *every* rung of its round —
    `buildBoard` keeps it only then, and discards it silently otherwise. Extra
    clues on a rung are fine (the shipped bank averages 8.3 rows a category
    across 1,000 rows and 120 categories).
    """
    by_round = defaultdict(lambda: defaultdict(set))
    for r in rows:
        if r.get("round") in LADDERS:
            by_round[r["round"]][r.get("category")].add(r.get("value"))

    complete = {}
    for rnd in ("single", "double", "final"):
        full = set(LADDERS[rnd])
        cats = by_round[rnd]
        if rnd == "final":
            n = sum(1 for r in rows if r.get("round") == "final")
            if n < 3:
                error("%s: %d final row(s); a match needs at least 3" % (label, n))
            note("%s: %d final rows" % (label, n))
            continue
        good = {c for c, vs in cats.items() if vs >= full}
        partial = {c: vs for c, vs in cats.items() if vs and vs < full}
        complete[rnd] = good
        note("%s: %d categories seen in the %s round, %d complete"
             % (label, len(cats), rnd, len(good)))
        for c, vs in sorted(partial.items()):
            warn("%s: category %r is missing rung(s) %s — it will be discarded "
                 "and the board comes up short" % (label, c, sorted(full - vs)))
        if len(good) < 6:
            error("%s: %d complete %s categories; a board deals 6"
                  % (label, len(good), rnd))

    single, double = complete.get("single", set()), complete.get("double", set())
    shared = single & double
    reachable = double - single
    if shared:
        note("%s: %d category name(s) appear in both rounds; the single round is "
             "dealt first and never gives one back" % (label, len(shared)))
    if len(reachable) < 6:
        error("%s: only %d double categories survive the single round (%d qualify "
              "in both) — the board can come up short"
              % (label, len(reachable), len(shared)))
    else:
        note("%s: %d double categories reachable after the single round"
             % (label, len(reachable)))


def check_slot_duplicates(rows, label):
    """One slot, one question. Two rows in a slot must ask different things.

    A slot is a `(category, round, value)` rung, and it is dealt as one tile:
    when the rung is reached, `buildBoard` picks at random among the rows
    sitting on it. Two rows there that ask the same question are not a
    duplicate tile — the board never shows both — they are half the replay
    variety the bank claims, and a player who plays twice meets the same
    question twice while the category pretends to hold two.

    The pair may be spelled any of the ways the bank spells a second row:
    `_a`/`_b`, `_encore`, or a final's `_1`/`_2`. Naming the ids is a
    convention, not the mechanism, so the rule reads the slot the engine reads
    rather than the suffixes. Nothing else in the pipeline can see this: the
    category still carries all five rungs, so the board deals it happily.
    """
    slots = defaultdict(list)
    for r in rows:
        if r.get("round") in LADDERS:
            slots[(r.get("category"), r.get("round"), r.get("value"))].append(r)
    dup = []
    for slot, group in sorted(slots.items(), key=lambda kv: str(kv[0])):
        if len(group) < 2:
            continue
        seen = defaultdict(list)
        for r in group:
            seen[normalise(str(r.get("clue", "")))].append(str(r.get("id")))
        for _, ids in seen.items():
            if len(ids) > 1:
                dup.append(" = ".join(sorted(ids)))
    if dup:
        error("%s: %d slot(s) hold the same clue text twice — the second question "
              "was never written: %s%s"
              % (label, len(dup), ", ".join(dup[:6]), " …" if len(dup) > 6 else ""))
    if VERBOSE:
        for name in dup:
            note("%s: duplicate slot text: %s" % (label, name))


def check_slot_pair_agreement(rows, label):
    """Two rows in one slot must agree about the answer they share.

    `check_slot_duplicates` above makes the two rows ask *different* things.
    This is the other half: when two rows in a slot answer the *same* thing,
    they have to agree about it.

    Which pairs those are is not a naming convention. A slot's two rows come
    in two kinds and only one of them shares an answer:

    - an `_encore` pair is one answer asked twice — the second row is a second
      question about the same thing, so the four options, the index into them,
      the aliases, the citation and the rung must be the slot's, not the row's;
    - an `_a`/`_b` pair is two different questions that happen to sit on the
      same rung, and it is *supposed* to hold two different answers (all 170 of
      them do). Requiring agreement there would flag the design as the defect.

    So the rule keys on the answer, not the suffix: rows that share an answer
    share everything else. A symmetric pair that genuinely shares an answer
    falls under the same rule, which is right — two rows the judge answers
    identically must accept the same spellings of it.

    What a row is still free to differ in is the question it asks and what
    follows the clue: `clue_text`, `explanation`, `supporting_passage`, the two
    host lines, the rationales. `page` goes with `supporting_passage` — the two
    questions of a final were drawn from different pages of the same book, and
    the citation follows the passage the row actually rests on. `book` does not:
    one answer is documented by one book.

    Nothing caught the real defect because of where it lives: a patch keyed on
    the base id lands on one row, the `_encore` twin keeps the old list, and
    every per-row rule passes on both — the aliases are each still names for
    their own answer, the options are still four, the index is still 0. The
    pair is the only place the disagreement is visible.
    """
    slots = defaultdict(list)
    for r in rows:
        if r.get("round") in LADDERS:
            slots[(r.get("category"), r.get("round"), r.get("value"))].append(r)
    shared = ("aliases", "options", "correct",
              "book", "author", "period", "theme", "difficulty")
    split = []
    for slot, group in sorted(slots.items(), key=lambda kv: str(kv[0])):
        if len(group) < 2:
            continue
        by_answer = defaultdict(list)
        for r in group:
            by_answer[normalise(str(r.get("answer", "")))].append(r)
        for _, same in sorted(by_answer.items()):
            if len(same) < 2:
                continue
            for field in shared:
                values = {}
                for r in same:
                    values.setdefault(json.dumps(r.get(field), sort_keys=True,
                                                 ensure_ascii=False),
                                      []).append(str(r.get("id")))
                if len(values) > 1:
                    split.append("%s (answer %s): %s is %s" % (
                        " vs ".join(sorted(i for ids in values.values() for i in ids)),
                        repr(same[0].get("answer")), field,
                        " / ".join(sorted(values))))
    if split:
        error("%s: %d slot(s) whose rows answer the same thing but disagree "
              "about it — one of the pair was patched and its twin was not: %s%s"
              % (label, len(split), "; ".join(split[:4]), " …" if len(split) > 4 else ""))
    if VERBOSE:
        for name in split:
            note("%s: slot pair split: %s" % (label, name))


def check_alias_ownership(rows, label, strict=True, provenance=frozenset()):
    """An alias belongs to the row that lists it. Nothing else enforces that.

    `accepted_aliases` is what the write-in judge reads. A list that names a
    different row's answer is not a typo a reader catches: the clue still
    reads well, the four options are still right, and the only symptom is that
    the game accepts a wrong answer as correct.

    Two rules, both about the row's *own* content:

    - at least one alias must be recognisably the row's answer — the same
      string, a substring of it, or sharing a content word. A list where
      nothing relates to the answer is a list inherited from somewhere else.
      One is the floor, not the bar: a list may carry both scripts of one name
      (`Amir Kabir` / `امیرکبیر`) and a spelling variant that shares nothing,
      and the author is entitled to it. But a list that shares nothing at all
      is asking to be re-read.
    - no alias may be one of the row's own wrong options. The judge would
      accept the distractor the player was just offered, and `_a`/`_b` pairs
      left unrewritten fail here first.

    `strict` is the MAIN bank's setting. The first rule found 347 inherited
    lists in MAIN's Persian archive and is at zero there, so it stays an error
    — and it is the wrong instrument for a course. A course's aliases are
    translations and transliterations by construction (`Muscat` / `Oman`,
    `Erbil` / `Hewler`, `Gasoline` / `Petrol`), which share no token however
    correct they are; 46 of the 90 course rows it flagged were exactly that.
    On a course it warns, so the list is still read, and does not fail a build
    over an alias that is right.

    `provenance` is the third case and the one MAIN is in now: a course's bank
    absorbed whole (`Tools/promote_course_bank.py`), so rows that a course
    authored sit in MAIN's own file. They get the course's setting — read, not
    failed — and *only* they do: MAIN's 1,000 own rows are still at zero and
    stay an error, which is the whole reason the set is by id and not by bank.
    Measured 2026-09-15: all 46 of the flagged rows are absorbed, none are MAIN's.
    """
    orphans, adopted, shadowed = [], [], []
    for r in rows:
        rid = r.get("id")
        aliases = r.get("aliases")
        answer = str(r.get("answer", ""))
        if not isinstance(aliases, list):
            continue
        if aliases and not any(related(a, answer) for a in aliases):
            (orphans if strict and rid not in provenance else adopted).append(rid)
        wrong = {normalise(present(o)) for o in (r.get("options") or [])
                 if normalise(present(o)) != normalise(present(answer))}
        for a in aliases:
            if normalise(present(a)) in wrong:
                shadowed.append("%s lists %r, which is one of its own wrong options"
                                % (rid, a))
    if orphans:
        error("%s: %d row(s) list aliases that share nothing with their own answer "
              "— the judge would accept another question's answer: %s%s"
              % (label, len(orphans), ", ".join(str(i) for i in orphans[:6]),
                 " …" if len(orphans) > 6 else ""))
    if adopted:
        warn("%s: %d row(s) list aliases that share nothing with their own answer "
             "— the judge would accept another question's answer: %s%s. Read, "
             "and not failed: a course's aliases are translations and "
             "transliterations by construction, which share no token however "
             "correct they are."
             % (label, len(adopted), ", ".join(str(i) for i in adopted[:6]),
                " …" if len(adopted) > 6 else ""))
    for name in (orphans + adopted) if VERBOSE else []:
        note("%s: orphan alias list: %s" % (label, name))
    for msg in shadowed:
        error("%s: %s" % (label, msg))


def check_citations(rows, label, strict=True):
    """Every answer says where it comes from.

    `Web/app.js:2710` prints `book · author · p. N` under the answer, after the
    explanation, once the last contestant has had their shot — that line is the
    reason a right answer teaches something, and a row without it is the one
    row in the bank that quietly shows nothing.

    Required: `book` and `author`, the two fields that line is made of. NOT
    required: `page`. A `final` row answers for a whole module or a whole book
    and has no single page to point at — the course's own two sourced finals
    carry both a book and an author and no page, and that is the convention,
    not a gap. Requiring a page would push an author toward a page number that
    does not mean anything, which is worse than the blank.

    MAIN's two archives are at 1,000 of 1,000 on both fields as of 2026-09-15,
    so the rule is an error there. A course is checked at a warning, because a
    course is one syllabus with one owner and the citation is that owner's call:
    the last gap was `final_snapback`, which asks for the JCPOA's snapback
    mechanism — a term that appears nowhere in the course's eleven weeks of
    readings (grepped, zero hits) — and it was closed on 2026-09-15 by citing
    the instrument itself, `Joint Comprehensive Plan of Action (UN Security
    Council Resolution 2231)` / `United Nations Security Council`, which is also
    the precedent for citing a document rather than a book about it. A `book`
    field need not be a book. Both banks of that course now cite on all 693 rows.

    The strict/warn split is the same shape as `check_alias_ownership`: a course
    is a different kind of bank and this checker does not get to fail it.
    """
    say = error if strict else warn
    missing = [r.get("id") for r in rows
               if not str(r.get("book") or "").strip()
               or not str(r.get("author") or "").strip()]
    if missing:
        say("%s: %d row(s) name no source, so the answer shows no book and no "
            "author: %s%s"
            % (label, len(missing), ", ".join(str(i) for i in missing[:6]),
               " …" if len(missing) > 6 else ""))
    unpaged = [r.get("id") for r in rows
               if not r.get("page") and r.get("round") != "final"]
    for name in unpaged if VERBOSE else []:
        note("%s: no page, and not a final: %s" % (label, name))


# A dash between words, a colon, or a semicolon. Not a hyphen *inside* a word:
# "Anglo-Iranian" is a name, and a rule that cannot tell the two apart has to be
# switched off, which is the same as not having it.
TELL = re.compile(r"(?:^|\s)[-–—]|[-–—](?=\s|$)|[:;؛]")


def check_option_surface(rows, label):
    """What the buttons look like, once the engine has had its way with them.

    Two ways an option gives itself away without saying anything:

    - the authored gloss. `presentingOption` takes every parenthetical off at
      deal time, so a gloss is not itself a tell — but an option that *becomes*
      a second copy of another option when its gloss comes off is a board with
      the same text in two squares, and the engine's merge guard then keeps the
      gloss on that one button, which puts the tell straight back.
    - punctuation on exactly one option. A dash, colon or semicolon on the
      answer and nowhere else is a beacon: the shipped bank was once findable
      by tapping the em-dash 196 times out of 210. A tell on every option says
      nothing; a tell on one says everything.
    """
    for r in rows:
        rid = r.get("id")
        opts = r.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            continue
        shown = [present(o) for o in opts]
        keys = defaultdict(list)
        for s in shown:
            keys[normalise(s)].append(s)
        merged = [v[0] for k, v in keys.items() if k and len(v) > 1]
        if merged:
            error("%s: two options collide once the engine strips their glosses "
                  "(%s) — the board would show one text twice"
                  % (rid, "; ".join(sorted(merged))))
        flagged = [s for s in shown if TELL.search(s)]
        if len(flagged) == 1:
            error("%s: option %r is the only one carrying a dash/colon — it is "
                  "findable by its punctuation" % (rid, flagged[0]))
        elif flagged:
            note("%s: %d options carry a dash/colon, so none of them is a beacon"
                 % (rid, len(flagged)))


def check_rationales(rows, label, provenance=frozenset()):
    """The three rationales describe *this* row's three wrong options.

    `distractor_rationales` is archive-only — it never reaches the player — and
    that is exactly why it drifts. Three entries that describe a different
    row's options are invisible in the game and invisible to every other gate,
    and they are the note an author reads before writing the next batch.

    The option is named inside each rationale, so what is compared is a set: the
    three names must be the row's own three wrong options, as the button carries
    them (glosses off, because the archive names `Iraj` while the option reads
    `Iraj (Hossein Khajeh Amiri)`).

    `provenance` is the set of ids MAIN absorbed from a course. A course bank
    has no such field — it is 17 keys and this is not one of them — so an
    absorbed row arrives with an empty list rather than three invented ones.
    Empty is read and counted, not failed, and the count is printed. Anything
    else is checked as usual: a partial list is still an error, and a full one
    is still held to naming the row's own wrong options, so the follow-up pass
    that fills these in is checked by this rule the moment it runs.
    """
    shapes, mismatched, owed = [], [], 0
    for r in rows:
        rid = r.get("id")
        rats = r.get("distractor_rationales")
        opts = r.get("options") or []
        answer = str(r.get("answer", ""))
        if rid in provenance and not rats:
            owed += 1
            continue
        if not isinstance(rats, list) or len(rats) != 3:
            shapes.append("%s has %s rationales, not 3"
                          % (rid, "no" if rats is None else len(rats)
                             if isinstance(rats, list) else "malformed"))
            continue
        for rat in rats:
            if not isinstance(rat, dict) or \
                    not all(str(rat.get(k, "")).strip() for k in
                            ("option", "why_plausible", "why_wrong")):
                shapes.append("%s has a rationale missing option/why_plausible/"
                              "why_wrong" % rid)
                break
        else:
            named = {normalise(present(rat["option"])) for rat in rats}
            wrong = {normalise(present(o)) for o in opts
                     if normalise(present(o)) != normalise(present(answer))}
            if named != wrong:
                mismatched.append("%s names %s; its wrong options are %s"
                                  % (rid, sorted(named) if len(named) <= 4 else
                                     "%d names" % len(named),
                                     sorted(wrong) if len(wrong) <= 4 else
                                     "%d options" % len(wrong)))
    if owed:
        note("%s: %d row(s) absorbed from a course, rationales still owed — "
             "archive-only, so nothing the player sees is missing"
             % (label, owed))
    for msg in shapes:
        error("%s: %s" % (label, msg))
    if mismatched:
        error("%s: %d row(s) carry rationales for options that are not on the row "
              "— they describe a different question's distractors: %s%s"
              % (label, len(mismatched), "; ".join(mismatched[:4]),
                 " …" if len(mismatched) > 4 else ""))
        if VERBOSE:
            for msg in mismatched:
                note("%s: rationale mismatch: %s" % (label, msg))


def check_category_spelling(rows, label):
    """A category is one string. Two spellings of it are two half-categories.

    `buildBoard` groups by the raw category string, so a category written
    `Qajar Iran` in four rows and `Qajar Iran ` — or `qajar iran` — in the fifth
    is two groups of four and one, neither of which covers all five rungs. The
    board does not fail; the category silently disappears and a shorter board
    is dealt. Nothing in the log or the docs names it, so it is checked here.
    """
    spellings = defaultdict(set)
    for r in rows:
        cat = r.get("category")
        if cat:
            spellings[normalise(str(cat))].add(str(cat))
    for _, variants in sorted(spellings.items()):
        if len(variants) > 1:
            error("%s: one category is spelled %d ways (%s) — the board would "
                  "split it and discard the pieces"
                  % (label, len(variants), ", ".join(repr(v) for v in sorted(variants))))


# The three shapes a batch of new host lines reproduces. Both archives are at
# zero on all three as of 2026-09-15, and they are errors rather than warnings
# because the only thing keeping them there is a gate that fails.
STOCK_TAILS = ("spot on", "quite right", "the history holds",
               "کاملا درسته", "تاریخ گواهی می‌دهد")
VERDICT_WORDS = {
    "en": r"(correct|yes|right|exactly|precisely|indeed|true|bravo|excellent|correctly|exactly right)",
    "fa": r"(بله|آفرین|درسته|درست|صحیح|دقیقا|دقیقاً|احسنت|کاملا درسته)",
}

# The flat shape wears a longer tail too: the answer named first and then
# nothing but praise for the player who named it — `Ahmadabad. Incredible
# precision.` `VERDICT_WORDS` above cannot see it, because it tests for one
# word and this verdict is a phrase (`Outstanding historical knowledge`).
# Eight English rows had it on 2026-09-15, all at the top rung, none Persian.
PRAISE_WORDS = {
    "en": set("""impressive outstanding incredible brilliant exceptional superb
        masterful excellent remarkable magnificent flawless impeccable
        extraordinary sterling admirable formidable encyclopedic scholarly
        precise perfect very quite truly most absolutely simply knowledge
        scholarship precision command recall memory grasp lore answer history
        research architectural literary historical""".split()),
    "fa": set(normalise(w) for w in
              "بی‌نقص عالی درخشان حیرت‌انگیز فوق‌العاده شگفت‌انگیز کامل بی‌نظیر "
              "استادانه چیره‌دست معلومات دانش احسنت آفرین".split()),
}


def check_host_lines(rows, label, lang):
    """The bank had a formula problem; a new batch should not reproduce it.

    Three named shapes, each the product of a wave that really happened: the
    stock tail (`… Quite right.`), the flat answer-plus-verdict
    (`<answer>. Correct.` — invisible to a search for stock tails, because it
    carries none), and the Persian `تو هم … گفتی.` hinge that all five writers
    of one wave reached independently. `QUESTION_AUTHORING.md` §8 has the counts.
    """
    for key in ("correctLine", "wrongLine"):
        lines = [str(r.get(key, "")) for r in rows if str(r.get(key, "")).strip()]
        if not lines:
            continue
        tails = Counter(" ".join(words(normalise(l))[-2:]) for l in lines)
        top = [(t, n) for t, n in tails.most_common(3) if n >= max(5, len(lines) // 10)]
        note("%s: %s — %d lines, %d distinct" % (label, key, len(lines), len(set(lines))))
        for t, n in top:
            warn("%s: %s — %d of %d lines end %r; write the tail fresh"
                 % (label, key, n, len(lines), t))

        verdict = re.compile(
            r"^(?P<pre>.+?)[.,!]\s*(?P<v>%s)[.!,]?$" % VERDICT_WORDS[lang], re.I)
        for r in rows:
            line = str(r.get(key, "")).strip()
            if not line:
                continue
            bare = normalise(line).rstrip(" .!?؟،؛")
            for tail in STOCK_TAILS:
                if bare.endswith(normalise(tail)):
                    error("%s: %s ends in the stock tail %r — %r"
                          % (label, key, tail, line))
            if lang == "fa" and bare.endswith(normalise("گفتی")):
                error("%s: %s ends گفتی, the Persian attractor — %r"
                      % (label, key, line))
            if key != "correctLine":
                continue
            forms = {normalise(r.get("answer") or "")}
            forms |= {normalise(a) for a in (r.get("aliases") or [])}
            forms.discard("")
            m = verdict.match(line)
            flat = bool(m) and normalise(m.group("pre")) in forms
            if not flat and forms:
                # Name the answer first, then say nothing but how well the
                # player did. Strip the answer's own words and read the rest.
                # What to write instead is the house shape — the answer named
                # and then paid off with a fact (`Amir Kabir. He printed his own
                # praises first.`, 149 English / 319 Persian rows). These two are
                # that shape with the fact removed, which is why they earn an
                # error and it earns nothing.
                rest = line
                for f in sorted(forms, key=len, reverse=True):
                    rest = re.sub(r"\b%s\b" % re.escape(f), " ", rest, flags=re.I)
                left = words(normalise(rest))
                flat = (0 < len(left) <= 5
                        and all(w in PRAISE_WORDS[lang] for w in left))
            if flat:
                error("%s: correctLine is the answer plus praise and nothing "
                      "else, so the player reads the answer twice — %r"
                      % (label, line))


def unjs(s):
    """Read a JS string literal's escapes back into the characters it spells."""
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append(s[i + 1])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def check_theme_reach(rows, label, edition_path, require, lang):
    """Which of the professor's ten clips the bank's category names can reach.

    `edition.js` matches a category against a keyword table, most specific
    first, with a plain substring test on the lowercased name. A category that
    matches nothing gets no introduction and **no error** — the clip simply
    never plays. That is the right failure for a subject he does not teach, and
    the wrong one for a week he does.
    """
    with open(edition_path, encoding="utf-8") as fh:
        text = fh.read()
    at = re.search(r"var\s+THEME\s*=\s*\[", text)
    if not at:
        warn("could not find a `var THEME = [` table in %s" % edition_path)
        return
    block = text[at.end():text.index("];", at.end())]
    # A row has to survive its own escapes. The table writes `\'` for an
    # apostrophe inside a category name, and a pattern that stops at the first
    # bare `'` fails to complete the row and — because a match has to start at
    # the `[` — drops it whole rather than mangling it. `all the president\'s
    # mullahs` then has no key left, and its category reads as unmatched. Match
    # the escape, then read it back.
    table = [(unjs(k), unjs(c)) for k, c in re.findall(
        r"\[\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*\]", block)]
    if not table:
        warn("the THEME table in %s parsed empty" % edition_path)
        return

    seen = defaultdict(set)
    for r in rows:
        if r.get("round") in ("single", "double") and r.get("category"):
            seen[str(r["category"])].add(1)
    cats = sorted(seen)
    silent, hit = [], defaultdict(list)
    for c in cats:
        low = c.lower()
        clip = next((clip for kw, clip in table if kw in low), None)
        if clip:
            hit[clip].append(c)
        else:
            silent.append(c)

    note("%s: %d categories, %d reach a professor theme clip, %d reach none"
         % (label, len(cats), len(cats) - len(silent), len(silent)))
    # Both banks get the same test. The table carries a row per category in each
    # language, so a Persian category reaching no clip is a real gap in the same
    # way an English one is — not, as this check used to assume, a fact of the
    # edition's design.
    if silent:
        msg = ("%s: %d categor(y/ies) fire no week clip: %s"
               % (label, len(silent), ", ".join(repr(c) for c in silent[:8])))
        if len(silent) > 8:
            msg += " …"
        (error if require else warn)(msg)
    dead = sorted({clip for _, clip in table} - set(hit))
    if dead:
        warn("%s: %d of the professor's theme clip(s) no category can reach: %s"
             % (label, len(dead), ", ".join(sorted(dead))))


def check_id_mirror(en, fa, en_label, fa_label):
    a = [r.get("id") for r in en]
    b = [r.get("id") for r in fa]
    bad = [i for i, x in enumerate(a) if i >= len(b) or b[i] != x]
    if len(a) != len(b):
        error("%s has %d rows and %s has %d — the pair must mirror"
              % (en_label, len(a), fa_label, len(b)))
    if bad:
        error("%d row(s) are not mirrored by id between %s and %s; first at index "
              "%d (%r vs %r)" % (len(bad), en_label, fa_label, bad[0],
                                 a[bad[0]], b[bad[0]] if bad[0] < len(b) else None))
    if Counter(a).most_common(1) and Counter(a).most_common(1)[0][1] > 1:
        dupe, n = Counter(a).most_common(1)[0]
        error("%s: id %r appears %d times — ids must be unique" % (en_label, dupe, n))


def report(bank_path, edition_path, require_theme, archive=False, lang=None):
    marker, rows = load(bank_path, archive=archive)
    label = os.path.basename(bank_path)
    if lang is None:
        lang = "fa" if marker.endswith("_FA") else "en"
    # MAIN owns the `window.CLUES` global; a course's is `window.COURSE_CLUES_*`.
    # Not inferred from the row shape — course rows carry `book` / `author` /
    # `page` too, so "has provenance fields" does not separate the two kinds.
    is_course = marker.startswith("window.COURSE_")
    if archive:
        rows = [play_view(r) for r in rows]
    note("%s: %d rows, %s shape, language %s"
         % (label, len(rows), "archive" if archive else "marker `%s`" % marker, lang))

    shape = Counter()
    for k in PROVENANCE_KEYS:
        if any(k in r for r in rows):
            shape[k] = sum(1 for r in rows if k in r)
    if not shape:
        note("%s: no provenance fields at all — the source line under every "
             "answer is blank" % label)

    # A word that is already all over the bank — in many clues, or in many
    # answers — is not a giveaway when it turns up in one more clue. Only a
    # word that lives almost nowhere else but this answer's clue says anything.
    # Counted across clue and answer together, one row counting once.
    counts = Counter()
    for r in rows:
        seen = set(w for w in words(normalise(str(r.get("answer", "")) + " " + str(r.get("clue", ""))))
                   if len(w) >= 5 and w not in STOPWORDS)
        counts.update(seen)
    floor = max(5, len(rows) // 50)
    global COMMON_ANSWER_TOKENS
    COMMON_ANSWER_TOKENS = set(w for w, n in counts.items() if n >= floor)

    for i, r in enumerate(rows):
        check_row(i, r, lang, latin_ok=(lang == "fa"))
    check_language_purity(rows, lang)
    check_categories(rows, label)
    check_category_spelling(rows, label)
    check_slot_duplicates(rows, label)
    check_slot_pair_agreement(rows, label)
    # Which rows MAIN absorbed from a course, asked of the archive that records
    # it. MAIN's own rows are checked as MAIN's own; the absorbed ones carry
    # their course's standards, and no others do.
    promoted = promoted_ids(bank_path, rows, archive)
    check_alias_ownership(rows, label, strict=not is_course, provenance=promoted)
    check_citations(rows, label, strict=not is_course)
    check_option_surface(rows, label)
    if archive:
        check_rationales(rows, label, provenance=promoted)
    check_host_lines(rows, label, lang)
    if edition_path:
        check_theme_reach(rows, label, edition_path, require_theme, lang)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bank", help="a play-shaped bank file "
                                "(window.CLUES for MAIN, COURSE_CLUES_<ID> for a course)")
    ap.add_argument("--fa", help="the other language's bank, to check ids mirror")
    ap.add_argument("--edition", help="a course.js, to check category -> theme clip reach")
    ap.add_argument("--require-theme-clips", action="store_true",
                    help="treat a category that reaches no theme clip as an error")
    ap.add_argument("--archive", action="store_true",
                    help="read MAIN's archive rows (a bare JSON array) rather than "
                         "a play file, and check the fields only the archive has, "
                         "`distractor_rationales` above all")
    ap.add_argument("--lang", choices=("en", "fa"),
                    help="the language of the bank handed in; only needed with "
                         "--archive, where nothing in the file says it")
    ap.add_argument("--verbose", action="store_true",
                    help="also print the per-row auditing aids, which fire on "
                         "roughly four rows in ten and are not defects")
    args = ap.parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    try:
        rows = report(args.bank, args.edition, args.require_theme_clips,
                      archive=args.archive, lang=args.lang)
        if args.fa:
            fa_rows = report(args.fa, args.edition, args.require_theme_clips,
                             archive=args.archive,
                             lang=args.lang and "fa")
            check_id_mirror(rows, fa_rows, os.path.basename(args.bank),
                            os.path.basename(args.fa))
    except (ValueError, OSError) as exc:
        print("cannot read the bank: %s" % exc, file=sys.stderr)
        return 2

    for m in NOTES:
        print("  %s" % m)
    if WARNINGS:
        print("\n%d warning(s):" % len(WARNINGS))
        for m in WARNINGS:
            print("  ! %s" % m)
    if ERRORS:
        print("\n%d error(s):" % len(ERRORS))
        for m in ERRORS:
            print("  X %s" % m)
        print("\nFAILED")
        return 1
    print("\nOK — no errors%s" % (" (%d warning(s))" % len(WARNINGS) if WARNINGS else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
