#!/usr/bin/env python3
"""Is this clue already on the board?

A batch can be perfectly well-formed and still be worthless: rows that ask what
rows already on the board ask. `check_bank.py` catches a repeat *inside one
slot*; nothing caught a new clue that repeats the bank at large. This does, and
`append_batch.py` calls it before it writes anything.

Two verdicts:

  FATAL  the batch repeats something already on the board. Refuses the merge.
  WARN   the batch is close to something already on the board. Prints, and the
         author decides. Warnings never block a merge.

What counts as a repeat of a *question*: the same normalised clue text, or
near-identical wording — most of the shorter clue's content words shared, six
words or more in common. That is a reworded ask, not a shared era.

A repeated *answer* is never a refusal. The bank grows by adding a second
question to a slot it already holds — the `_b` and `_encore` rows — and those
answer the same entity on purpose. It warns, and the author decides.

"Same" is `check_bank.normalise`, so the two tools agree — including on the
Persian yeh and kaf and on the zero-width non-joiner.

    python3 Tools/check_repeats.py batch-2026-09      # one incoming batch
    python3 Tools/check_repeats.py --bank             # audit the bank itself
    python3 Tools/check_repeats.py --bank --list 40   # with a shortlist
    python3 Tools/check_repeats.py --file <bank-en.js> --lang en   # a course bank

`--file` audits any bank file against itself, and there a near-repeat is a
**fatal**, not a note: a course edition ships its bank whole, so a question asked
twice inside it is two clues the same board can deal in one match. It is the
third gate `build_edition.sh` runs, and it is the one the Qajars got past — the
course was built by a one-off converter that never called that script, and
nothing else in the tree could read a play-shape bank for repeats at all.

Exit status is 1 if any FATAL was raised, 2 if nothing could be read, else 0.
Read-only: it never writes the archive.
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Tools"))

import check_bank as cb  # noqa: E402  — the house definition of "same"

ARCHIVES = {
    "en": "QuestionBank/verified_clues.json",
    "fa": "QuestionBank/verified_clues_fa.json",
}

INCOMING = os.path.join(ROOT, "QuestionBank", "incoming")

# A reworded question shares most of the shorter clue's content words. Measured
# against the shipped bank: at 75% and six words, auditing 2,205 English rows
# against each other raised 7 hits, every one a genuine near-repeat. Two clues
# that merely both say "Tehran" share far fewer words than that and do not fire.
BANK_FLOOR = 0.75          # of the shorter clue's content words
MIN_SHARED = 6             # words in common, below which overlap is coincidence


# ── What a clue is made of ───────────────────────────────────────────────────

def content(text):
    """The words a clue is actually about, as a set."""
    return {w for w in cb.words(cb.normalise(text or "")) if len(w) > 1}


def overlap(a, b):
    """How much of the shorter clue the two share, and how many words."""
    if not a or not b:
        return 0.0, 0
    shared = a & b
    return len(shared) / float(min(len(a), len(b))), len(shared)


def slot(row):
    return (cb.normalise(row.get("round") or ""),
            cb.normalise(row.get("category") or ""),
            str(row.get("value")))


def clue_of(row):
    """The clue text, from either shape.

    MAIN's archive says `clue_text`; a course edition's bank says `clue`. Reading
    only `clue_text` made every course row look empty here, which is why a course
    bank could never be audited for repeats — `--bank` reads the archive, and this
    one function returned "" for a play-shape row, so nothing ever matched.
    """
    return row.get("clue_text") or row.get("clue") or ""


def label(row):
    return "%s  «%s» %s %s" % (row.get("id"), row.get("category"),
                               row.get("round"), row.get("value"))


# ── The comparison ───────────────────────────────────────────────────────────

def index(rows):
    """Precompute what every row is, once."""
    return [{"row": r, "clue": cb.normalise(clue_of(r)),
             "toks": content(clue_of(r)),
             "ans": cb.normalise(r.get("canonical_answer") or ""),
             "slot": slot(r)} for r in rows]


def compare_one(new, old):
    """Findings for one new row against one row already on the board.

    A repeated *question* is the defect, and it is fatal anywhere in the bank.
    A repeated *answer* is not: the bank grows by adding a second question to a
    slot it already holds — the `_b` and `_encore` rows — and those answer the
    same entity on purpose. That warns, and the author decides.
    """
    out = []
    if new["clue"] and new["clue"] == old["clue"]:
        return [("fatal", "asks the same question, word for word",
                 new["row"], old["row"])]

    ratio, shared = overlap(new["toks"], old["toks"])
    if shared >= MIN_SHARED and ratio >= BANK_FLOOR:
        out.append(("fatal", "asks the same question in other words "
                    "(%d words shared, %.0f%% of the shorter clue)"
                    % (shared, ratio * 100), new["row"], old["row"]))

    if new["ans"] and new["ans"] == old["ans"]:
        where = ("this slot already has" if new["slot"] == old["slot"]
                 else "the board already has at %s" % old["row"].get("id"))
        out.append(("warn", "answers %r, which %s — legal if the question "
                    "differs" % (new["row"].get("canonical_answer"), where),
                    new["row"], old["row"]))
    return out


def against(new_rows, old_rows):
    """Every finding for a set of new rows against a set already on the board."""
    old_index = index(old_rows)
    findings = []
    for n in index(new_rows):
        for o in old_index:
            findings += compare_one(n, o)
    return findings


def against_itself(rows, severity="warn"):
    """Every near-repeat inside one set. Audits the board, or one batch."""
    idx = index(rows)
    findings = []
    for i, a in enumerate(idx):
        if not a["clue"]:
            continue
        for b in idx[i + 1:]:
            if a["clue"] and a["clue"] == b["clue"]:
                findings.append((severity, "asks the same question, word for word",
                                 a["row"], b["row"]))
                continue
            ratio, shared = overlap(a["toks"], b["toks"])
            if shared >= MIN_SHARED and ratio >= BANK_FLOOR:
                findings.append((severity, "asks almost the same question "
                                 "(%d words shared, %.0f%%)" % (shared, ratio * 100),
                                 a["row"], b["row"]))
    return findings


# ── Reporting ────────────────────────────────────────────────────────────────

def render(findings, limit):
    fatal = [f for f in findings if f[0] == "fatal"]
    warn = [f for f in findings if f[0] == "warn"]
    if fatal:
        print("\n  REPEATS — these refuse the merge:")
        for _, detail, new, old in fatal[:limit]:
            print("    X %s\n      %s\n      already on the board: %s  %r"
                  % (label(new), detail, old.get("id"),
                     clue_of(old)[:90]))
        if len(fatal) > limit:
            print("    … and %d more" % (len(fatal) - limit))
    if warn:
        print("\n  near the board — read these, they do not block:")
        for _, detail, new, old in warn[:limit]:
            print("    ! %s\n      %s\n      against: %s  %r"
                  % (label(new), detail, old.get("id"),
                     clue_of(old)[:90]))
        if len(warn) > limit:
            print("    … and %d more" % (len(warn) - limit))
    print("\n  %d repeat(s), %d near-repeat(s)" % (len(fatal), len(warn)))
    return 1 if fatal else 0


def load_bank(lang):
    with open(os.path.join(ROOT, ARCHIVES[lang]), encoding="utf-8") as fh:
        return json.load(fh)


def resolve_batch(stem):
    paths = {lang: os.path.join(INCOMING, "%s-%s.json" % (stem, lang))
             for lang in ARCHIVES}
    missing = [p for p in paths.values() if not os.path.exists(p)]
    if missing:
        raise ValueError("no batch at %s" % ", ".join(missing))
    return paths


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stem", nargs="?", help="a batch stem in QuestionBank/incoming/")
    ap.add_argument("--bank", action="store_true",
                    help="audit a bank against itself instead of a batch")
    ap.add_argument("--file", metavar="PATH",
                    help="audit one bank file against itself — a course edition's "
                         "bank-en.js or bank-fa.js, or a bare rows-en.json before it "
                         "is wired in. A near-repeat here is fatal.")
    ap.add_argument("--lang", choices=("en", "fa"), default="en",
                    help="which bank to audit with --bank")
    ap.add_argument("--list", type=int, default=20, help="how many to print")
    args = ap.parse_args()

    if args.file:
        try:
            _, rows = cb.load(args.file)
        except (ValueError, OSError):
            # Not a `window.X = [...]` bank, so try a bare JSON array of rows -- the
            # shape an author hands over before anything is wired in. Same rows, one
            # file earlier than the bank they become.
            try:
                _, rows = cb.load(args.file, archive=True)
            except (ValueError, OSError) as exc:
                print("  X %s will not read: %s" % (args.file, exc), file=sys.stderr)
                return 2
        print("  %s: %d rows, auditing against itself"
              % (os.path.relpath(args.file, ROOT), len(rows)))
        return render(against_itself(rows, severity="fatal"), args.list)

    if args.bank:
        rows = load_bank(args.lang)
        print("  %s: %d rows, auditing against itself" % (ARCHIVES[args.lang], len(rows)))
        return render(against_itself(rows), args.list)

    if not args.stem:
        print("  X give a batch stem, or --bank", file=sys.stderr)
        return 2
    try:
        paths = resolve_batch(args.stem)
    except ValueError as exc:
        print("  X %s" % exc, file=sys.stderr)
        return 2

    findings = []
    for lang, path in paths.items():
        try:
            with open(path, encoding="utf-8") as fh:
                rows = json.load(fh)
        except (ValueError, OSError) as exc:
            print("  X %s will not parse: %s" % (path, exc), file=sys.stderr)
            return 2
        bank = load_bank(lang)
        print("  %s: %d new row(s) against %d on the board" % (lang, len(rows), len(bank)))
        findings += against(rows, bank)
        findings += against_itself(rows, severity="fatal")  # the batch itself
    return render(findings, args.list)


if __name__ == "__main__":
    sys.exit(main())
