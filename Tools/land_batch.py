#!/usr/bin/env python3
"""Land a batch that was written outside this project.

    python3 Tools/land_batch.py qajars --from "~/.../Qajars (Trinity 2016)/bank"

Why this exists
---------------
A batch written in the project itself goes straight to `Tools/append_batch.py`:
the author writes into `QuestionBank/incoming/` and the merge picks it up. A batch
written somewhere else -- on Drive, by Gemini in Spark, from a phone -- arrives as
`rows-en.json` and `rows-fa.json` and has to be brought in first. That hop is the
only thing this script does, and it does it the same way every time so nobody has
to remember the path convention.

What it repairs, and what it will not
-------------------------------------
The Gemini contract asks for the archive's 27 field names and gets them right: the
ids mirror, the categories are complete, every row cites a source, the host lines
are distinct. Exactly one field comes back in a shape the archive does not take --
`distractor_rationales` arrives as one object keyed by the option text:

    {"Treaty of Gulistan": {"why_plausible": "...", "why_wrong": "..."}, ...}

where MAIN wants a list of three, each naming its own option:

    [{"option": "Treaty of Gulistan", "why_plausible": "...", "why_wrong": "..."}, ...]

The two carry the same three rationales, so this is a re-shape and not a decision.
The list is built in the row's own wrong-option order, keyed by text rather than by
position, so a row whose dict happens to be in a different order still lands right.
If a key is not one of that row's wrong options the row is refused by name -- that
is a different defect and inventing a rationale for it would hide it.

Everything else is left exactly as it arrived. This is not a validator and not an
editor: `Tools/append_batch.py` is the gate, and it reads the whole merged bank.
Checks that live there are deliberately not duplicated here.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCOMING = os.path.join(ROOT, "QuestionBank", "incoming")
ARCHIVE = os.path.join(ROOT, "QuestionBank", "verified_clues.json")

RATIONALE_KEYS = ("option", "why_plausible", "why_wrong")

# difficulty is derived from the rung, never invented -- §4 of the contract. A writer
# that carries the single-round ladder onto a double-round row gets 400 and 1200 wrong,
# and only those two, because they are the rungs the two ladders name differently.
RUNGS = {
    "single": {200: "CASUAL", 400: "STANDARD", 600: "STANDARD", 800: "SCHOLAR",
               1000: "INSUFFERABLE"},
    "double": {400: "STANDARD", 800: "STANDARD", 1200: "SCHOLAR", 1600: "SCHOLAR",
               2000: "INSUFFERABLE"},
    "final": {0: "INSUFFERABLE"},
}


def fail(msg):
    print("\n  %s\n" % msg, file=sys.stderr)
    sys.exit(2)


def load(path, what):
    if not os.path.exists(path):
        fail("There is no %s at\n    %s\n"
             "  Nothing written." % (what, path))
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        return json.loads(text)
    except ValueError as exc:
        # The likeliest cause by far: the file is still being written, or was cut off
        # mid-write. Say that rather than a line-and-column, because the fix is to
        # wait or ask for the rest, not to edit the JSON.
        fail("%s is not valid JSON yet -- %s\n    %s\n"
             "  If a writer is still working in that folder, this is the file it is\n"
             "  partway through. Wait for it to finish and run again."
             % (what, exc, path))


def find_rows(folder):
    """The two row files, from the course folder or from its bank/ subfolder."""
    for candidate in (folder, os.path.join(folder, "bank")):
        en = os.path.join(candidate, "rows-en.json")
        if os.path.exists(en):
            fa = os.path.join(candidate, "rows-fa.json")
            if not os.path.exists(fa):
                hint = ""
                if os.path.exists(os.path.join(candidate, "rows-fa.empty.json")):
                    hint = ("\n  There is a `rows-fa.empty.json` beside it -- an empty "
                            "[] left over from a first run.\n  The Persian batch was "
                            "never written, or was written elsewhere.")
                fail("Found rows-en.json but no rows-fa.json in\n    %s%s"
                     % (candidate, hint))
            return en, fa
    fail("No rows-en.json in\n    %s\n  nor in its bank/ subfolder." % folder)


def canonical_keys():
    """The archive's own field set, read from the archive.

    Read rather than written down, so that a field added to the archive later does
    not leave this script quietly refusing the new shape.
    """
    rows = load(ARCHIVE, "MAIN archive")
    if not rows:
        fail("The MAIN archive is empty, so there is no shape to match.")
    return set(rows[0].keys())


def already_archive_shaped(rats):
    return (isinstance(rats, list) and len(rats) == 3
            and all(isinstance(i, dict)
                    and all(str(i.get(k, "")).strip() for k in RATIONALE_KEYS)
                    for i in rats))


def condition_rationales(row, where):
    """The one repair. Returns None on success, or a sentence explaining the row."""
    rats = row.get("distractor_rationales")
    if already_archive_shaped(rats):
        return None
    if not isinstance(rats, dict):
        return ("%s: distractor_rationales came back as %s, which is neither the "
                "archive's list of three nor the option-keyed form this repairs"
                % (where, "nothing" if rats is None else type(rats).__name__))

    answer = row.get("canonical_answer")
    options = [o for o in (row.get("options") or []) if o != answer]
    if len(options) != 3:
        return ("%s: distractor_rationales can only be re-shaped against three "
                "wrong options, and this row has %d" % (where, len(options)))

    for key, value in rats.items():
        if key not in options:
            return ("%s: distractor_rationales names %r, which is not one of this "
                    "row's wrong options (%s)"
                    % (where, key, "; ".join(str(o) for o in options)))
        if not isinstance(value, dict) or \
                not all(str(value.get(k, "")).strip()
                        for k in ("why_plausible", "why_wrong")):
            return ("%s: the rationale for %r is not a why_plausible/why_wrong pair"
                    % (where, key))

    row["distractor_rationales"] = [
        {"option": option,
         "why_plausible": rats[option]["why_plausible"],
         "why_wrong": rats[option]["why_wrong"]}
        for option in options]
    return None


def condition_difficulty(row):
    """Put the rung's own difficulty label back. Returns True if it had to."""
    rung = RUNGS.get(row.get("round"), {})
    want = rung.get(row.get("value"))
    if want is None or row.get("difficulty") == want:
        return False
    row["difficulty"] = want
    return True


def condition(rows, lang, fields):
    """Every row through the one repair. Stops at the first row it cannot fix.

    Returns how many rows it had to re-shape. It is counted here rather than after
    the fact, because once repaired every row looks the same.
    """
    repaired = 0
    relabelled = 0
    for i, row in enumerate(rows):
        where = "%s[%d] %s" % (lang, i, row.get("id", "?"))
        got = set(row.keys())
        if got != fields:
            missing = sorted(fields - got)
            extra = sorted(got - fields)
            fail("%s is not the archive's shape.\n"
                 "    missing: %s\n    unexpected: %s\n"
                 "  Nothing written. The batch has to carry all %d fields, spelled "
                 "the way the archive spells them."
                 % (where, ", ".join(missing) or "none", ", ".join(extra) or "none",
                    len(fields)))
        keyed = isinstance(row.get("distractor_rationales"), dict)
        problem = condition_rationales(row, where)
        if problem:
            fail("%s\n  Nothing written. This is a real defect in the batch, not a "
                 "shape this script can fix -- fix the row and run again." % problem)
        if keyed:
            repaired += 1
        if condition_difficulty(row):
            relabelled += 1
    return repaired, relabelled


def run(cmd, label):
    """One of the project's own scripts, relayed verbatim."""
    print("  %s" % label)
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).rstrip()
    for line in out.splitlines():
        print("    %s" % line)
    return proc.returncode


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stem", nargs="?",
                    help="the batch's name, e.g. `qajars` -- it names the two files "
                         "in QuestionBank/incoming/. Defaults to the source folder's "
                         "name, lowercased.")
    ap.add_argument("--from", dest="source", required=True,
                    help="the folder holding rows-en.json and rows-fa.json, or the "
                         "course folder that has them under bank/")
    ap.add_argument("--check", action="store_true",
                    help="say what is wrong and write nothing")
    args = ap.parse_args()

    source = os.path.expanduser(args.source)
    if not os.path.isdir(source):
        fail("There is no folder at\n    %s" % source)

    stem = args.stem
    if not stem:
        name = os.path.basename(os.path.normpath(source))
        if name == "bank":
            name = os.path.basename(os.path.dirname(os.path.normpath(source)))
        stem = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not stem:
            fail("Could not make a batch name out of\n    %s\n"
                 "  Name it yourself: land_batch.py <stem> --from ..." % source)
        print("  batch name: %s  (from the folder name; pass one to override)\n" % stem)

    en_path, fa_path = find_rows(source)
    fields = canonical_keys()
    batches = {}
    reshaped = {}
    for lang, path in (("en", en_path), ("fa", fa_path)):
        rows = load(path, "%s batch" % lang)
        if not isinstance(rows, list):
            fail("%s is not a bare JSON array." % path)
        if not rows:
            fail("%s is empty." % path)
        reshaped[lang] = condition(rows, lang, fields)
        batches[lang] = rows

    for lang, path in (("en", en_path), ("fa", fa_path)):
        rats, rungs = reshaped[lang]
        print("  %s: %d row(s), %d with rationales re-shaped, %d with the rung's "
              "difficulty restored"
              % (os.path.relpath(path, source), len(batches[lang]), rats, rungs))

    if args.check:
        print("\n  --check: the shape is clean; nothing written. Re-run without "
              "--check to land it.\n")
        return 0

    written = []
    for lang, rows in batches.items():
        path = os.path.join(INCOMING, "%s-%s.json" % (stem, lang))
        if os.path.exists(path):
            print("  replacing %s" % os.path.relpath(path, ROOT))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        written.append(os.path.relpath(path, ROOT))

    print("\n  wrote %s" % ", ".join(written))

    # The gate, and then the same landing sequence GEMINI.md gives an in-project
    # author: merge, regenerate the play files, refresh the digest. Each one is the
    # project's own script and each is a stop.
    code = run([sys.executable, os.path.join(ROOT, "Tools", "append_batch.py"),
                stem, "--dry-run"], "rehearse the merge")
    if code != 0:
        fail("The rehearsal refused the batch (exit %d), so nothing was merged.\n"
             "  The two files above are written, with the rationales repaired, and\n"
             "  name the rows to fix. `append_batch.py %s --dry-run` re-reads them\n"
             "  where they are." % (code, stem))

    for cmd, label in (
            (["append_batch.py", stem], "land it into the archive"),
            (["render_bank.py"], "regenerate the play files"),
            (["bank_digest.py"], "refresh the digest the next batch reads")):
        code = run([sys.executable, os.path.join(ROOT, "Tools", cmd[0])] + cmd[1:],
                   label)
        if code != 0:
            fail("%s stopped with exit %d. Nothing after it ran -- read its output "
                 "above before doing anything else." % (cmd[0], code))

    print("\n  Landed. Two things downstream now want attention, both by hand:")
    print("    * Tools/validate_1000_clues.py, Tools/verify_flawless_state.py and")
    print("      Tools/validate_persian_bank.py pin the row count at 2,205 and the")
    print("      category count at 261. They now fail by arithmetic. Bump the numbers")
    print("      in the same commit as this batch.")
    print("    * If the batch added a category, QuestionBank/persian_clues.json and")
    print("      App/Resources/persian_clues.json lag behind it; nothing in this")
    print("      sequence writes them.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
