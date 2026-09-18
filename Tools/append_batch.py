#!/usr/bin/env python3
"""Append a batch of new clues to MAIN's archive. The only thing that writes there.

An author — Gemini, or anyone — never opens `QuestionBank/verified_clues.json`.
Batches are written into `QuestionBank/incoming/` as bare JSON arrays in the
archive's own field shape, and this script is what puts them in. It does that
once, with a backup, a full-bank validation and a byte-level round-trip
assertion, so the archive cannot be reformatted or half-written.

    python3 Tools/append_batch.py batch-2026-09
    python3 Tools/append_batch.py QuestionBank/incoming/batch-2026-09-en.json \\
                                 QuestionBank/incoming/batch-2026-09-fa.json
    python3 Tools/append_batch.py batch-2026-09 --dry-run

A stem names both files: `<stem>-en.json` and `<stem>-fa.json` in
`QuestionBank/incoming/`. Both languages, or nothing — the two archives mirror
id for id, and half a pair is a broken bank.

What it refuses:

  * a batch whose rows are not in the archive's exact field shape
  * an id already in the archive, or one not mirrored across the languages
  * a clue the board already asks — the same question word for word, or the
    same question reworded — see `Tools/check_repeats.py`
  * anything that fails `Tools/check_bank.py` once merged with the archive
  * writing the archive in any serialisation but its own

It appends; it never rewrites, reorders or deletes an existing row. Exit status
is 1 if anything failed, and then nothing is written.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCOMING = os.path.join(ROOT, "QuestionBank", "incoming")
sys.path.insert(0, os.path.join(ROOT, "Tools"))

import check_repeats as cr  # noqa: E402

# The archive, per language: path, and whether it ends with a trailing newline.
# Measured 2026-09-18: neither file ends with one, at HEAD or in the working
# tree. Both are reproduced exactly, because any other form rewrites all 2,205
# rows to move one.
ARCHIVES = {
    "en": ("QuestionBank/verified_clues.json", False),
    "fa": ("QuestionBank/verified_clues_fa.json", False),
}

HOST_KEYS = ("correct_generic", "wrong_generic")


def fail(msg):
    print("  X %s" % msg, file=sys.stderr)
    return False


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def serialise(rows, trailing_newline):
    text = json.dumps(rows, ensure_ascii=False, indent=2)
    return text + "\n" if trailing_newline else text


def resolve(args):
    """Return {lang: batch path}, from a stem or from two explicit paths."""
    if args.en or args.fa:
        if not (args.en and args.fa):
            raise ValueError("give both --en and --fa, or neither")
        return {"en": args.en, "fa": args.fa}
    stem = args.stem
    if stem is None:
        raise ValueError("give a batch stem, or --en and --fa")
    return {lang: os.path.join(INCOMING, "%s-%s.json" % (stem, lang))
            for lang in ARCHIVES}


def check_shape(lang, rows, canonical_keys):
    """Every row carries exactly the archive's fields, in the archive's order."""
    ok = True
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            ok = fail("%s[%d] is not an object" % (lang, i)) and ok
            continue
        extra = set(row) - set(canonical_keys)
        missing = set(canonical_keys) - set(row)
        if extra:
            ok = fail("%s[%d] %s has fields the archive does not: %s"
                      % (lang, i, row.get("id", "?"), ", ".join(sorted(extra)))) and ok
        if missing:
            ok = fail("%s[%d] %s is missing: %s"
                      % (lang, i, row.get("id", "?"), ", ".join(sorted(missing)))) and ok
        if not extra and not missing:
            # Reorder onto the archive's own key order. Values are untouched.
            rows[i] = {k: row[k] for k in canonical_keys}
        if row.get("language") != lang:
            ok = fail("%s[%d] %s says language=%r"
                      % (lang, i, row.get("id", "?"), row.get("language"))) and ok
        hr = row.get("host_reactions")
        if not isinstance(hr, dict) or not all(k in hr for k in HOST_KEYS):
            ok = fail("%s[%d] %s has no host_reactions.%s"
                      % (lang, i, row.get("id", "?"), "/".join(HOST_KEYS))) and ok
    return ok


def check_ids(lang, rows, archive_ids):
    ok = True
    seen = {}
    for i, row in enumerate(rows):
        rid = row.get("id")
        if not isinstance(rid, str) or not rid:
            ok = fail("%s[%d] has no id" % (lang, i)) and ok
            continue
        if rid in archive_ids:
            ok = fail("%s: id %r is already in the archive" % (lang, rid)) and ok
        if rid in seen:
            ok = fail("%s: id %r appears twice in the batch (%d and %d)"
                      % (lang, rid, seen[rid], i)) and ok
        seen[rid] = i
    return ok


def check_replay(batches, archives, allow_repeats):
    """Refuse a batch that asks what the board already asks.

    The author never sees the archive, so a repeat is the likeliest defect in
    any hand-written batch and the one no other check catches. A row that
    merely answers something the board answers elsewhere is legal — the bank
    asks about one entity in several slots on purpose — so that warns only.
    """
    findings = []
    for lang, rows in batches.items():
        findings += cr.against(rows, archives[lang]["rows"])
        findings += cr.against_itself(rows, severity="fatal")
    fatal = [f for f in findings if f[0] == "fatal"]
    warn = [f for f in findings if f[0] == "warn"]
    for _, detail, new, old in fatal:
        fail("%s repeats %s — %s" % (new.get("id"), old.get("id"), detail))
    for _, detail, new, old in warn[:15]:
        print("  ! %s is near %s — %s" % (new.get("id"), old.get("id"), detail))
    if len(warn) > 15:
        print("  ! … and %d more near-repeats" % (len(warn) - 15))
    if fatal and allow_repeats:
        print("\n  --allow-repeats: %d repeat(s) let through by hand. Read them "
              "again before you trust this batch." % len(fatal), file=sys.stderr)
        return True
    return not fatal


def gate(tmp_en, tmp_fa):
    """Run the real validator over the merged bank. Its word is final."""
    cmd = [sys.executable, os.path.join(ROOT, "Tools", "check_bank.py"),
           tmp_en, "--archive", "--lang", "en", "--fa", tmp_fa]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = [ln for ln in (proc.stdout + proc.stderr).splitlines()
            if ln.strip().startswith(("X ", "cannot read"))]
    for ln in tail[-25:]:
        print("  %s" % ln.strip(), file=sys.stderr)
    if proc.returncode != 0:
        print("\n  check_bank.py failed on the merged bank (exit %d). "
              "Nothing written." % proc.returncode, file=sys.stderr)
        return False
    return True


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stem", nargs="?", help="a batch stem in QuestionBank/incoming/")
    ap.add_argument("--en", help="the English batch, explicitly")
    ap.add_argument("--fa", help="the Persian batch, explicitly")
    ap.add_argument("--dry-run", action="store_true",
                    help="validate and report, write nothing")
    ap.add_argument("--allow-repeats", action="store_true",
                    help="merge even if a row repeats the board; the repeat "
                         "checker is a reading, and this is how you overrule it")
    args = ap.parse_args()

    try:
        paths = resolve(args)
    except ValueError as exc:
        print("  X %s" % exc, file=sys.stderr)
        return 2

    # ── Read the archive as it stands, and prove we can reproduce it ─────────
    archives, batches, canonical_keys = {}, {}, None
    for lang, (rel, trailing_nl) in ARCHIVES.items():
        path = os.path.join(ROOT, rel)
        raw = open(path, encoding="utf-8").read()
        rows = json.loads(raw)
        if serialise(rows, trailing_nl) != raw:
            print("  X %s does not round-trip through json.dumps(indent=2, "
                  "ensure_ascii=False); refusing to touch it." % rel, file=sys.stderr)
            return 2
        if canonical_keys is None:
            canonical_keys = list(rows[0].keys())
        archives[lang] = {"path": path, "rows": rows, "trailing_nl": trailing_nl}
        print("  %s: %d rows" % (rel, len(rows)))

    # ── Read the batches ────────────────────────────────────────────────────
    for lang, path in paths.items():
        if not os.path.exists(path):
            print("  X no %s batch at %s" % (lang, path), file=sys.stderr)
            return 2
        try:
            rows = load_json(path)
        except (ValueError, OSError) as exc:
            print("  X %s will not parse: %s" % (path, exc), file=sys.stderr)
            return 2
        if not isinstance(rows, list) or not rows:
            print("  X %s is not a non-empty JSON array" % path, file=sys.stderr)
            return 2
        batches[lang] = rows
        print("  %s: %d new row(s)" % (os.path.relpath(path, ROOT), len(rows)))

    # ── The batch's own rules ───────────────────────────────────────────────
    ok = True
    for lang, rows in batches.items():
        ok = check_shape(lang, rows, canonical_keys) and ok
        ok = check_ids(lang, rows, {r["id"] for r in archives[lang]["rows"]}) and ok

    en_ids = {r.get("id") for r in batches["en"]}
    fa_ids = {r.get("id") for r in batches["fa"]}
    for rid in sorted(en_ids - fa_ids):
        ok = fail("id %r is in the English batch with no Persian twin" % rid) and ok
    for rid in sorted(fa_ids - en_ids):
        ok = fail("id %r is in the Persian batch with no English twin" % rid) and ok

    if ok:
        ok = check_replay(batches, archives, args.allow_repeats)

    if not ok:
        print("\n  Nothing written.", file=sys.stderr)
        return 1

    # ── The real gate: the whole merged bank, both languages, ids mirrored ──
    merged = {}
    with tempfile.TemporaryDirectory() as td:
        for lang in ARCHIVES:
            merged[lang] = archives[lang]["rows"] + batches[lang]
            tmp = os.path.join(td, "merged-%s.json" % lang)
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(serialise(merged[lang], archives[lang]["trailing_nl"]))
            paths[lang + "_tmp"] = tmp
        if not gate(paths["en_tmp"], paths["fa_tmp"]):
            return 1

        if args.dry_run:
            print("\n  Dry run: %d + %d = %d rows would be written. Nothing written."
                  % (len(archives["en"]["rows"]), len(batches["en"]),
                     len(merged["en"])))
            return 0

        # ── Write: backup, then the new bytes, atomically ───────────────────
        for lang, (rel, trailing_nl) in ARCHIVES.items():
            entry = archives[lang]
            backup = entry["path"] + ".pre-append"
            shutil.copy2(entry["path"], backup)
            text = serialise(merged[lang], trailing_nl)
            assert json.loads(text) == merged[lang]
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(entry["path"]))
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(text)
            os.replace(tmp, entry["path"])
            print("  %s: %d -> %d rows  (backup: %s)"
                  % (rel, len(entry["rows"]), len(merged[lang]),
                     os.path.basename(backup)))

    print("\n  Done. The play files are stale until you run:")
    print("    python3 Tools/render_bank.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
