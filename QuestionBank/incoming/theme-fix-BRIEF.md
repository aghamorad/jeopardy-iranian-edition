# Theme repair — authoring brief

You are authoring replacement clues for the Iranian Edition of Jeopardy. This is a shipping
product and the clue bank is its content. Work carefully; a script will reject anything that
does not meet this brief, and a person will read the board afterwards.

## Why this exists

Every category on the board must be a **theme**: five clues drawn from **at least three
different books, never more than two from any one book**. Twenty-one categories are currently
*stacked* — three of their five clues come from one over-used book. Your job is to replace
**exactly one clue in each of your assigned categories** with a clue drawn from a different
book, in English and in Persian.

## Read, in this order

1. `QUESTION_AUTHORING.md` — the governing contract. Especially §4 (categories), §6
   (distractors), §7 (answers and aliases), §8 (the host's voice and the `correctLine`
   shape), §9 (both languages; the Persian calendar rule), §10 (provenance), §14 (what a clue
   may say). It outranks this brief wherever the two seem to disagree.
2. The slice of `QuestionBank/incoming/theme-repair-candidates.md` named in your assignment.
   That is your candidate pool.

## The candidate file

Each `## ` section is one category. It names the over-used book, then `Remove exactly ONE of
these three:` with the three removable rows (answer, id, value, difficulty), then the two
rows that stay, and then — under one heading per removable row — a list of candidates sitting
at that row's rank band. Each candidate reads:

```
- **answer** | Book Title | pNN | chapter | source_id | Author
    quote: "the book's own sentence"
    fact:  the fact stated plainly
```

A trailing `← already elsewhere on the board` means that answer is already used by another
clue in the bank. Such a candidate is legal, but your clue must then ask something the
existing one does not — so prefer an unmarked candidate.

**Nothing outside that file may be cited.** Invent nothing. The `book_title`, `author`,
`page`, `chapter` and `source_id` you write must be copied from the candidate line, and your
`supporting_passage` must be taken **verbatim from that candidate's `quote:`** (trim it to the
sentence or clause that carries the fact if the quote is long; do not paraphrase it).

## Decide, per category

**Which ONE of the three listed rows to replace.** Replace it at the same `value` and
`difficulty` — the rung is fixed, because a category dies without all five rungs.

Choose the row whose candidate list offers a fact that genuinely *sits* at that rung's
difficulty (see §2–§3 of the contract), and choose a candidate whose:

- book is **not** the over-used book,
- book is ideally one **not already present** in that category,
- answer does not duplicate any of the other four clues in the category, and
- fact has not been asked by any other clue on the board.

If the rung you would prefer has a weak candidate list, replace a different row — swapping
which rung you fill is free; changing a rung's difficulty is not.

## Output

Two files, array-of-rows in the archive shape described in §1 of `QUESTION_AUTHORING.md`:

```
QuestionBank/incoming/<stem>-en.json    "language": "en"
QuestionBank/incoming/<stem>-fa.json    "language": "fa", same ids in the same order
```

One row per assigned category, both files.

- `id`, `round`, `value`, `category`, `difficulty`, `historical_period` and `theme`: copied
  **verbatim** from the row you are replacing. Read that row out of the live archive first:
  `python3 -c "import json;print(json.dumps([r for r in json.load(open('QuestionBank/verified_clues.json')) if r['id']=='<id>'][0],ensure_ascii=False,indent=1))"`
- `category` in the **Persian** file is the Persian title given in your assignment, not the
  English one.
- `correct_option_index`: `0`, and `options[0]` is the canonical answer.
- `partial_answers`: `[]`; `specificity_prompt`: `""`; `confidence`: `1.0`.
- `evidence_type`: one of `established_fact`, `scholarly_interpretation`, `primary_testimony`.
- `editorial_validation_status`: `"verified"` — your fact came from a page-anchored reading of
  the book, which is exactly what that status records.

## Hard rules — a script checks every one

- English rows: **no Persian script in `clue_text`**. Aliases may carry Persian.
- Persian rows: written as Persian, not a translation of the English row, and ideally asking
  its own question rather than restating the English one. **Every year in the row names its
  calendar** — `۱۳۵۷ خورشیدی`, `۱۹۷۹ میلادی`. A bare numeral is a defect.
- Four options, no duplicates, `options[correct_option_index] == canonical_answer`, and no
  option may appear as text inside the clue.
- Exactly three `distractor_rationales`, one per wrong option, each naming that option's text
  exactly in its `"option"` field, with a short `why_plausible` and `why_wrong`.
- `accepted_aliases` non-empty and including the canonical answer.
- `host_reactions` is exactly `{"correct_generic": ..., "wrong_generic": ...}`.
- `supporting_passage` is non-empty and appears verbatim in the candidate's `quote:`.
- The clue stands alone — it names no book, no author, no source.
- The clue must not repeat an existing clue. Six or more content words in common with any
  other clue in the bank, or 75% of the shorter clue's content words, reads as a repeat.
  Ask a question nobody has asked.

## The host

She is unnamed, smug, snarky and mean, and identical in register in both languages. These are
her lines. `correct_generic` is the house shape: **name the answer, then pay it off with a
fact** — *"The Society for National Monuments. It gave Ferdowsi a mausoleum, because national
memory also requires masonry."* An answer repeated back with no payoff is the defect, and so
are the five stock tails §8 lists. `wrong_generic` needles the contestant, never lectures.

## Do not

Edit any file outside `QuestionBank/incoming/`. Never touch `QuestionBank/verified_clues*.json`,
`Web/data/*`, or anything in `Tools/`.

## Report back

Under 200 words: for each category, which row you replaced, with what answer and what book;
and any category where the candidates were too weak to fill the slot well.
