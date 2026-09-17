# Working in this repo as a clue author

You are writing Jeopardy clues from a source corpus into MAIN's archive. Read
`CORPUS_BRIEF.md` first — it is the contract, and `QUESTION_AUTHORING.md` is the long
form. Where this file and those disagree, they win. This file only tells you **where to
write and what not to touch.**

## The one rule

**Never open `QuestionBank/verified_clues.json` or `QuestionBank/verified_clues_fa.json`.**

You do not write the archive. You are not allowed to read it in order to edit it. A
merge script (`Tools/append_batch.py`) puts your work in, after a validator passes it.
If you reformat that file — even to add one row — you rewrite all 2,205 rows and damage
the bank. So: don't open it for writing, at all.

Don't read it to check your subject either. 2,205 rows is more than you can hold, and it
is not a working document. Read the **digest** instead:

```
QuestionBank/BANK_DIGEST.md        every English clue on the board, by category
QuestionBank/BANK_DIGEST_fa.md     the Persian board
```

One line per clue — the answer, then the question it was asked in — generated from the
live bank by `python3 Tools/bank_digest.py`. This is the view of the bank you get, and it
is the one that keeps you from repeating it.

## Where you write

```
QuestionBank/incoming/<stem>-en.json     ← bare JSON array, English rows
QuestionBank/incoming/<stem>-fa.json     ← same ids, Persian rows
```

One stem names both files. `batch-2026-09` gives `batch-2026-09-en.json` and
`batch-2026-09-fa.json`. Both languages or the batch is refused — the two archives
mirror id for id. Nothing else in the repo is yours to write.
`Web/data/clues.js` is **generated**; editing it does nothing.

## Where the new sources are

`Sources/MAIN CORPUS/` — folders 1–7 are the books MAIN was already written from, so
most of what is in them is already on the board. Folder **`8 - New Additions (2026-09)`**
holds the sources for this batch: read those first, and prefer them.

**Read `QuestionBank/BANK_DIGEST.md` before you write.** It carries every clue already on
the board, by category. Do not write a question that is already there — word for word, or
reworded. Repeating an *answer* is fine: that is what a `_b` or `_encore` id does, adding a
second question to a slot the board already holds. Repeating a *question* is not fine
anywhere in the bank. `Tools/append_batch.py` refuses a repeat and names the row you
collided with, so a duplicate costs you a re-run, not the bank.

## The row

Every row carries exactly the archive's fields, spelled exactly as the archive spells
them — `Tools/append_batch.py` rejects anything else. All 27:

`id` · `language` · `category` · `historical_period` · `theme` · `difficulty` · `value` ·
`round` · `clue_text` · `canonical_answer` · `accepted_aliases` · `partial_answers` ·
`specificity_prompt` · `options` · `correct_option_index` · `distractor_rationales` ·
`explanation` · `source_id` · `book_title` · `author` · `chapter` · `page` ·
`supporting_passage` · `evidence_type` · `confidence` · `editorial_validation_status` ·
`host_reactions`

The things that fail a batch:

- **`difficulty` is derived from the rung, never chosen.** One label per rung, and there
  are two ladders, not one. Copy the wrong one and the row still looks fine, still plays,
  and still fails the gate:

  ```
  single   200 → CASUAL      400 → STANDARD   600 → STANDARD
           800 → SCHOLAR    1000 → INSUFFERABLE
  double   400 → STANDARD    800 → STANDARD  1200 → SCHOLAR
          1600 → SCHOLAR    2000 → INSUFFERABLE
  final      0 → INSUFFERABLE
  ```

  The way this goes wrong is applying the ladder **by position** — first rung casual,
  second standard, third standard, fourth scholar, fifth insufferable — instead of by
  value. On the single round that is correct. On the double round it puts `CASUAL` on
  400 and `STANDARD` on 1200, and gets 800, 1600 and 2000 right by accident, so **exactly
  two rows per double category** come out wrong. That is how the Qajar bank shipped 100
  wrong rows a language: 50 double categories × 2. This is not cosmetic —
  `Web/app.js:4386` nudges a robot's accuracy 0.08–0.20 by label, so a mislabelled row
  plays easier than its rung says. `Tools/check_bank.py:315` fails the row by name.
- **`correct_option_index` is 0 on every row.** Always. The engine reshuffles when it
  deals. Do not spread the index.
- **Four options.** `options[0]` is the canonical answer.
- **The answer must not appear in the clue text.**
- **`accepted_aliases` is never empty** — every spelling, transliteration, honorific and
  script. An alias belongs to *its own row's* answer and no other.
- **A category is five clues** — one at every rung of its round — or the board builder
  discards it silently. The `category` string must be byte-identical across all five.
- **No question is asked twice anywhere in the bank — not just inside one slot.** Two rows
  in *different categories*, at *different rungs*, asking the same thing is the same
  defect as an exact copy: one fact occupying two slots, and a match can deal both. The
  way it happens is a pair of twin categories on one subject (STEAM ON THE KARUN and
  PADDLEWHEELS & SHEIKHS: THE KARUN) reusing their best fact. "Same" is measured, not
  judged: **six or more content words in common and 75% of the shorter clue's** —
  `Tools/check_repeats.py`, which is what refuses the merge. Repeating an *answer* is
  fine and deliberate (`_b`, `_encore`); repeating a *question* is not.
- **Never invent a page.** Printed page, not PDF index. A `final` answers for a whole
  book and carries book and author with no page. A source_id must point at a real book.
- **Never invent a source, either — the citation is copied off the work, never composed.**
  No tool catches this one. Four rows of the Iran course cited a book that does not exist
  and passed every gate; a person reading the citation against the shelf is what found it.
  Take `book_title` as the work
  prints it and `author` from that work's own title page or citation line. **A chapter is
  cited by its book's title and the chapter's own page** — never build a title out of the
  words of the chapter's subtitle, which is how a plausible book that does not exist gets
  made. The `page` must fall inside the range that work occupies: a chapter printed 47–65
  is not at p. 8. **Find your `supporting_passage` in the source you name before you write
  the row** — if you cannot find the sentence, the citation is wrong. If you cannot see a
  citation at all, that row is unsourced: drop it and say so in the hand-back. An honest
  gap costs a slot; an invented citation is printed on screen under the answer.
- **Host lines are written fresh.** The shipped bank already ends 893 of its 1,000 lines
  in three stock tails ("Spot on!", "The history holds!", "Quite right."). Do not
  reproduce them. Shape: name the answer, then pay it off with a fact —
  `Amir Kabir. He printed his own praises first.` No praise, no `Correct.`, no admiration
  in place of the fact.
- **The Persian row is its own question**, with its own aliases and its own citation. It
  is not a translation of the English row. `fa_answer == en_answer` in 0 of 325 older
  twin slots.
- **A `_b` row is a second question**, not a copy of its `_a` twin.

## Land it

You write the batch; the script writes the bank. That division does not change here — you
are not being asked to edit the archive. But you are the one holding the batch, so you run
the sequence that puts it in. **Run these in this order, and stop at the first one that
fails.** Replace `<stem>` with your batch's stem throughout.

**1. Rehearse.** Validates the batch against the merged bank — shape, mirrored ids, repeats,
and the whole bank through the content checker. Writes nothing.

```
python3 Tools/append_batch.py <stem> --dry-run
```

If it prints anything other than a clean pass, **fix the batch and rehearse again.** Do not
run step 2 over a failing rehearsal. Every complaint it makes names the row, so it is a
list of edits, not a verdict.

**2. Land it.** Backs both archives up to `*.pre-append` first, then appends. If anything
fails it writes nothing at all, so a bad batch costs a re-run and cannot cost a clue.

```
python3 Tools/append_batch.py <stem>
```

**3. Regenerate the play files.** Until this runs the clues are in the bank but not on the
board.

```
python3 Tools/render_bank.py
```

**4. Refresh the digest** the next batch will be written against.

```
python3 Tools/bank_digest.py
```

**5. Prove it, over everything — not just your batch.**

```
python3 Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js
```

```
python3 Tools/check_bank.py QuestionBank/verified_clues.json --archive --lang en
```

```
python3 Tools/check_bank.py QuestionBank/verified_clues_fa.json --archive --lang fa
```

```
python3 Tools/check_repeats.py --bank --lang en
```

```
python3 Tools/check_repeats.py --bank --lang fa
```

A warning is not a pass with a footnote. Read every line.

### Two things that are not yours to fix

**The three archive validators will now fail, and that is expected.** `validate_1000_clues.py`,
`verify_flawless_state.py` and `validate_persian_bank.py` each pin the row count at 2,205 and
the category count at 373. After a merge they fail by arithmetic, not because anything is
wrong. **Report the new row and category counts and stop** — those numbers belong to the
maintainer and are bumped with the batch, not by you.

**If your batch added a new category, the two Persian dictionaries**
(`QuestionBank/persian_clues.json`, `App/Resources/persian_clues.json`) also lag, because
nothing in this sequence writes them. Mention it; do not write them.

## Hand back

Report counts, not a document: clues written, complete categories per round, finals, how
many host lines end in a shared tail, how many options the answer could be found from by
punctuation, and anything the corpus could not support. Add the exit code of step 5 and the
new row and category totals from step 2. "Done" is not a handoff. If the sources do not
yield a playable board, say so and stop — that is the honest result, and it is what we want
to hear.
