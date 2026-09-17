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
