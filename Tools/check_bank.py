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
# Provenance. The main bank carries all of these; a course bank is written from
# a syllabus rather than a book and legitimately carries none.
PROVENANCE_KEYS = ["book", "page", "passage", "author", "period"]

# `window.CLUES` / `_FA` is MAIN. Anything else is a course, and the only part
# of its global an agent is promised is the name: `COURSE_CLUES_<ID>` (+ `_FA`),
# where the id is the folder under `Web/courses/`. So the id is matched as an
# open run of name characters on either side of `CLUES` rather than enumerated —
# a new course must not need an edit here.
MARKER = re.compile(r"\b(window\.(?:[A-Z0-9_]*_)?CLUES(?:_[A-Z0-9_]+)?)\s*=")

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


def load(path):
    """Read the array out of a `window.X = [...]` bank file.

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
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    at = MARKER.search(text)
    if not at:
        raise ValueError(
            "no `window.CLUES = [...]` (MAIN) or `window.COURSE_CLUES_<ID> = "
            "[...]` (course) assignment in %s" % path)
    return at.group(1), json.loads(text[text.index("[", at.end()):text.rindex("]") + 1])


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


def check_alternates(rows, label):
    """`_a` and `_b` are two different questions for one rung, not one written twice.

    Both rows are dealt from the same slot, so the board never shows the
    duplicate — but the second question was never authored, the slot has half
    the replay variety it claims, and the `_b` alias list still names the answer
    the pair was *supposed* to ask for. A player typing that answer is judged
    correct against a clue about something else. Nothing else in the pipeline
    can see this: the category still carries all five rungs, so `buildBoard`
    deals it without complaint.
    """
    groups = {}
    for r in rows:
        m = re.match(r"^(.*)_(a|b)$", str(r.get("id") or ""))
        if m:
            groups.setdefault(m.group(1), {})[m.group(2)] = r
    dup = []
    for base, pair in sorted(groups.items()):
        if "a" not in pair or "b" not in pair:
            continue
        ta = normalise(pair["a"].get("clue") or pair["a"].get("clue_text") or "")
        tb = normalise(pair["b"].get("clue") or pair["b"].get("clue_text") or "")
        if ta and ta == tb:
            dup.append(base)
    if dup:
        error("%s: %d `_a`/`_b` alternate pair(s) carry the same clue text — the "
              "second question was never written: %s%s"
              % (label, len(dup), ", ".join(dup[:6]),
                 " …" if len(dup) > 6 else ""))


def check_host_lines(rows, label):
    """The shipped bank has a formula problem; a new batch should not reproduce it."""
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


def report(bank_path, edition_path, require_theme):
    marker, rows = load(bank_path)
    label = os.path.basename(bank_path)
    lang = "fa" if marker.endswith("_FA") else "en"
    note("%s: %d rows, marker `%s`, language %s" % (label, len(rows), marker, lang))

    shape = Counter()
    for k in PROVENANCE_KEYS:
        if any(k in r for r in rows):
            shape[k] = sum(1 for r in rows if k in r)
    if not shape:
        note("%s: no provenance fields — expected for a course bank, NOT for the "
             "main bank" % label)

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
    check_alternates(rows, label)
    check_host_lines(rows, label)
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
    ap.add_argument("--verbose", action="store_true",
                    help="also print the per-row auditing aids, which fire on "
                         "roughly four rows in ten and are not defects")
    args = ap.parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    try:
        rows = report(args.bank, args.edition, args.require_theme_clips)
        if args.fa:
            fa_rows = report(args.fa, args.edition, args.require_theme_clips)
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
