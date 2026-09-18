# Incoming batches

Scratch space for clues that have been authored but not yet merged into MAIN's
archive. Nothing here plays, and nothing here is the bank.

An author (Gemini, or anyone working from `GEMINI.md`) writes two files per batch:

```
<stem>-en.json     bare JSON array, archive shape
<stem>-fa.json     the same ids, Persian rows
```

Before writing, read `QuestionBank/BANK_DIGEST.md` — every clue already on the board,
by category, one line each. It is generated from the live bank by
`python3 Tools/bank_digest.py`. Do not write a question that is already there, word for
word or reworded.

Every year in a `-fa.json` row names its calendar — `۱۳۵۷ خورشیدی`, or `۱۹۷۹ میلادی` for a
Gregorian date. A bare numeral is a defect, because ۱۳۵۰ is 1971 shamsi and 1350 CE
Gregorian and both readings occur here. The rule in full is §9 of `QUESTION_AUTHORING.md`
and `Tools/normalize_fa_prose.py`; the appendix gives it in three lines:

```
python3 Tools/normalize_fa_prose.py --check --fa <stem>-fa.json --en <stem>-en.json
```

A row you have written but not read against its source is `"draft"` in
`editorial_validation_status`; it becomes `"verified"` when someone has opened the book and
found the passage. `python3 Tools/append_batch.py` refuses a batch that still carries a
draft, and there is no override — the status is the record of having read the row.

Merging is a separate step, done by a script and never by hand:

```
python3 Tools/append_batch.py <stem>
```

That validates the batch against the whole merged bank, backs both archives up to
`*.pre-append`, and appends. It refuses to write if anything fails — including a clue
that repeats one already on the board, which it reports and blocks. `--dry-run`
validates without writing; `--allow-repeats` overrules the repeat check if you have
read the collision and disagree with it. After a merge,
`python3 Tools/render_bank.py` regenerates the play files.

To audit the board itself for near-repeats:

```
python3 Tools/check_repeats.py --bank --lang en
```

A batch that has been merged can stay here as the authoring trail, or be moved to
`~/.Trash` — the archive is the record once the rows are in.
