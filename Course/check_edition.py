#!/usr/bin/env python3
"""Check a course's question banks before it is built.

    python3 Course/check_edition.py Web/courses/iran-in-world-politics

The argument is the course's folder under `Web/courses/`, the one the build
ships. Its name is the id, so the two bank globals are derived from it rather
than named: `data/bank-en.js` and `data/bank-fa.js` hold
`COURSE_CLUES_<UPPER_SNAKE(folder)>` and that name with `_FA`.

The engine builds a board by grouping the clues of a round by `category`, then
keeping only the categories that carry a clue at EVERY value in that round's
ladder:

    single   200 400 600 800 1000
    double   400 800 1200 1600 2000

Six qualifying categories are drawn at random. `S.usedCategories` is set when a
match starts and is cleared only at the next match, not between rounds, so a
category spent in the single round is gone for the double round. A full game
therefore needs twelve distinct qualifying categories: six single, six double.

The two rounds are drawn from disjoint pools only where the categories are
themselves disjoint, and they need not be: a name may carry five single values
and five double values and qualify in both. Such a name is one the single round
can take, so what the double round can count on is the double-qualifying names
that the single round cannot touch. That set has to hold six by itself, and the
per-round count below does not see it. Both are checked.

Coming up short does not raise an error anywhere. The board simply renders with
too few columns, which is easy to miss until it is up in front of a class. That
is what this checks.

Exits 1 if the edition cannot produce a full board, 0 if it can.
"""

import json
import os
import re
import sys

LADDERS = {"single": [200, 400, 600, 800, 1000],
           "double": [400, 800, 1200, 1600, 2000]}
BANKS = [("English", "data/bank-en.js", ""),
         ("Persian", "data/bank-fa.js", "_FA")]

# Six is the legal minimum. This is where a second match starts repeating boards.
VARIETY_FLOOR = 9

REQUIRED = ["id", "round", "value", "category", "theme", "difficulty", "clue",
            "answer", "aliases", "options", "correct", "explanation",
            "correctLine", "wrongLine"]


def load(path, marker):
    """Read the clue array out of a bank file.

    `marker` is the whole global, `window.COURSE_CLUES_<ID>` or its `_FA` form.
    The assignment has to be matched whole — `marker`, whitespace, `=`. A plain
    `text.find(marker)` would stop at the wrong place in half the calls here,
    because the English global is a prefix of the Persian one: the first
    `..._POLITICS` in the Persian file is the start of `..._POLITICS_FA`, and
    the search would take the marker's position and then hand back the Persian
    array while calling it English.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    at = re.search(r"\b" + re.escape(marker) + r"\s*=", text)
    if not at:
        raise ValueError("no `%s = [...]` assignment in this file" % marker)
    return json.loads(text[text.index("[", at.end()):text.rindex("]") + 1])


def check_bank(label, path, marker):
    problems = []
    notes = []

    try:
        clues = load(path, marker)
    except (ValueError, json.JSONDecodeError) as err:
        return ["%s bank will not parse: %s" % (label, err)], []

    if not isinstance(clues, list) or not clues:
        return ["%s bank holds no clues" % label], []

    for i, clue in enumerate(clues):
        where = clue.get("id") or "clue #%d" % (i + 1)
        missing = [f for f in REQUIRED if f not in clue]
        if missing:
            problems.append("%s: missing %s" % (where, ", ".join(missing)))
            continue
        opts = clue["options"]
        if len(opts) != 4:
            problems.append("%s: %d options, the board wants exactly 4" % (where, len(opts)))
        elif not isinstance(clue["correct"], int) or not 0 <= clue["correct"] < 4:
            problems.append("%s: `correct` is %r, which is not an index into 4 options"
                            % (where, clue["correct"]))
        elif opts[clue["correct"]] != clue["answer"]:
            problems.append("%s: `correct` points at %r but `answer` says %r -- the board "
                            "would highlight the wrong option"
                            % (where, opts[clue["correct"]], clue["answer"]))
        if not isinstance(clue["aliases"], list) or not clue["aliases"]:
            problems.append("%s: `aliases` is empty, so only an exact answer will count" % where)
        if clue["round"] not in ("single", "double", "final"):
            problems.append("%s: round is %r, wanted single/double/final" % (where, clue["round"]))

    ok = [c for c in clues if isinstance(c, dict) and all(f in c for f in REQUIRED)]

    # Ids are what the two languages are matched by, so a repeat would make a
    # Persian clue answerable against the English one.
    ids = [c["id"] for c in ok]
    if len(ids) != len(set(ids)):
        seen, dupes = set(), []
        for one in ids:
            if one in seen and one not in dupes:
                dupes.append(one)
            seen.add(one)
        problems.append("%s: %d duplicate id%s (%s); ids have to be unique"
                        % (label, len(dupes), "" if len(dupes) == 1 else "s",
                           ", ".join(str(d) for d in dupes[:5])))

    print("  %s bank  %d clues" % (label, len(clues)))

    qualified_by_round = {}

    for rnd, ladder in sorted(LADDERS.items()):
        by_cat = {}
        for clue in ok:
            if clue["round"] == rnd:
                by_cat.setdefault(clue["category"], set()).add(clue["value"])
        qualified = sorted(name for name, values in by_cat.items()
                           if all(v in values for v in ladder))
        qualified_by_round[rnd] = set(qualified)
        print("    %-6s %2d of %d categories qualify" % (rnd, len(qualified), len(by_cat)))

        if len(qualified) < 6:
            problems.append("%s: only %d %s categories carry all five values; a board "
                            "needs 6, so it will come up short" % (label, len(qualified), rnd))
        elif len(qualified) < VARIETY_FLOOR:
            notes.append("%s: %d %s categories -- playable, but a second match repeats "
                         "the same board" % (label, len(qualified), rnd))

        thin = sorted(name for name, values in by_cat.items()
                      if name not in qualified and len(values) >= 3)
        for name in thin[:5]:
            notes.append("%s: category %r is one short of qualifying -- it has %s, "
                         "needs %s" % (label, name, sorted(by_cat[name]), ladder))

    # What the double round can actually count on. A name qualifying in both
    # rounds is one the single round may take first, so it is not a name the
    # double round has; only the rest are.
    single_q = qualified_by_round["single"]
    double_q = qualified_by_round["double"]
    shared = single_q & double_q
    reachable = sorted(double_q - single_q)
    if shared:
        print("    both   %2d category name%s qualify in both rounds (%s)"
              % (len(shared), "" if len(shared) == 1 else "s",
                 ", ".join(sorted(shared)[:5])))
    if len(reachable) < 6:
        problems.append(
            "%s: the double round can only count on %d categories of its own -- %d of "
            "its %d qualifying names also qualify in the single round, which is dealt "
            "first and never gives a category back, so the board can come up short"
            % (label, len(reachable), len(shared), len(double_q)))

    finals = [c for c in ok if c["round"] == "final"]
    print("    final  %d clue%s" % (len(finals), "" if len(finals) == 1 else "s"))
    if not finals:
        problems.append("%s: no final clue, so the last round has nothing to draw"
                        % label)

    return problems, notes


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    course = sys.argv[1].rstrip("/")
    if not os.path.isdir(course):
        print("No such course folder: %s" % course, file=sys.stderr)
        return 1

    # The naming rule, applied rather than trusted: the folder name is the id,
    # so the globals are its upper snake case. A course that renamed its folder
    # and forgot the banks fails here, by name.
    ident = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(course)).upper()
    glob = "window.COURSE_CLUES_%s" % ident

    problems, notes = [], []
    print("Checking %s  (banks named %s)" % (course, glob))
    for label, rel, suffix in BANKS:
        path = os.path.join(course, rel)
        if not os.path.isfile(path):
            problems.append("%s bank is missing (%s)" % (label, rel))
            continue
        p, n = check_bank(label, path, glob + suffix)
        problems += p
        notes += n

    for note in notes:
        print("  note: %s" % note)
    for problem in problems:
        print("  FAIL: %s" % problem)

    if problems:
        print("\n%d problem%s. Not building." % (len(problems), "" if len(problems) == 1 else "s"))
        return 1
    print("\nBoth banks present and able to fill a full board.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
