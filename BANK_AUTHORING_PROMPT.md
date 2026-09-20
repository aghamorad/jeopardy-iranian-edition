# Bank authoring prompts

Three prompts, hand-over-verbatim, for any capable model — Gemini, Claude, GPT.

- **Prompt 1 — the whole authoring prompt.** A fresh bank from a corpus. Self-contained.
- **Prompt 2 — the guard.** Eight rules to paste at the end of an ingest prompt already running.
- **Prompt 3 — the re-cut.** For a bank that exists but whose categories are shelves for
  single books. Includes the block technique, which is the part models fail without.

The player who found the defects, 2026-09-20:

> some of them start with "In this chapter" etc. where we are not supposed to know the
> chapters — we're supposed to be answering the questions. Secondly, the categories are not
> as fun. Like one whole category is reserved for Kenneth Waltz — while we want pun-filled,
> categories all surrounding a theme but not one particular book or reading.

---

## The arithmetic of a board

Everything below assumes this, so give it to any model up front.

- A board draws **six categories, five clues each**.
- Single round values: **200 400 600 800 1000**. Double round values: **400 800 1200 1600 2000**.
- **A category is exactly five clues and holds one clue at each rung.** Never two at the same
  value, never four. The game enforces it at load.
- So a bank of *N* usable clues yields **N ÷ 5 categories per round**, and the count of clues
  at each rung must be **identical** — that is what makes the board assemblable.
- **Every category draws on at least three different sources.** Two clues from one book is
  the ceiling. One source across all five is the defect this document exists to stop.
- Categories exist once and are played in both languages: **one pun title in English, one in
  Persian**, written separately. Finals sit outside the round structure and keep their own
  titles.

---

## Prompt 1 — the whole authoring prompt

```
You are authoring clue rows for the Iranian Edition of Jeopardy. Output JSON only, one
array of row objects, no prose around it.

INPUTS
  - a corpus of books and articles, in the project's source tree
  - the historical period this bank covers
  - the target row count

WHAT YOU ARE BUILDING
  A bank of rows. Each round of the show draws a board: six categories, five clues each.
  Categories are themes the audience can argue about; clues are single facts from the corpus.

  single round values: 200 400 600 800 1000
  double round values: 400 800 1200 1600 2000
  difficulty ladder, hardest last: CASUAL, STANDARD, SCHOLAR, INSUFFERABLE

  THE BANK IS COUNTED AT THE RUNG, NOT THE ROW. Aim for the same number of clues at every
  value of a round. A round whose 1000 rung is thin cannot be dealt into boards.

ROW SHAPE — every field, every row, both languages
{
  "id": "<period>_<slug>_<value>",   // unique; <period>_single_ or <period>_double_
  "language": "en",
  "category": "PUN-FILLED THEME TITLE",
  "historical_period": "<period>",
  "theme": "<one lowercase subject word: politics, war, press, economy, clergy, …>",
  "difficulty": "CASUAL | STANDARD | SCHOLAR | INSUFFERABLE",
  "value": 200,
  "round": "single | double",
  "clue_text": "The clue. One fact. Stands alone.",
  "canonical_answer": "The answer, in its shortest correct form.",
  "accepted_aliases": ["every spelling, transliteration and Persian form a player might type"],
  "partial_answers": ["a partial a generous judge may still credit"],
  "specificity_prompt": "Asked when the answer is right but under-specified.",
  "options": ["four options when the match plays multiple choice, else []"],
  "correct_option_index": 0,
  "distractor_rationales": ["why each wrong option is wrong, in order"],
  "explanation": "One or two sentences of context, after the answer is revealed.",
  "source_id": "<short citation key>",
  "book_title": "Title as printed on the work.",
  "author": "Author of that work.",
  "chapter": "Chapter or section, when the corpus has one.",
  "page": 123,                       // null on a final; NEVER invented
  "supporting_passage": "The sentence in the source that carries the fact.",
  "evidence_type": "direct | inferred | synthesis",
  "confidence": "high | medium | low",
  "editorial_validation_status": "unreviewed",
  "host_reactions": { "correct_generic": "…", "wrong_generic": "…" }
}

THE RULES THAT MATTER MOST

1. THE CLUE STANDS ALONE. A player has read nothing — no book, no chapter, no syllabus.
   Never write a clue that points at text the player cannot see: "In this chapter", "In
   Chapter 9", "in this week's reading", "the assigned text", "in this essay/piece", "the
   unit", "the module". State the fact as a fact.

2. NAME NO SOURCE IN THE CLUE. The book, author and page print under the answer once the
   round closes. Inside the clue they are dead weight.
     FORBIDDEN: "According to Waltz", "Katouzian argues", "Chehabi classifies",
     "Keshavarzian identifies", "Moshirzadeh draws on", "as documented by Amal Saad",
     "In A Social History of Iranian Cinema, Naficy credits…", and any echo of the source
     book's title.
   ONE EXCEPTION: the scholar is the answer. Then the name is the question and stays.
     BAD:  "In his comparative study, Chehabi utilizes this term for rule without law."
     GOOD: "This two-word term names rule unconstrained by any settled legal order."

3. BUILD CATEGORIES BY THEME, NOT BY SOURCE. A category is five clues around one subject
   the audience could have opinions about — a coup, a coup's aftermath, oil, the clergy,
   the press, the army, the exiles, a decade, a rivalry. It is never a shelf for one book
   or one scholar's output. Draw the five from as many different sources as the theme
   needs; at least three, and never more than two from any one source. A category whose
   five clues share one source IS the defect, even when it plays fine.

4. EVERY CATEGORY IS FIVE CLUES, ONE AT EACH RUNG. If you cannot fill every rung of a
   category from the material, the category is not finished — either the theme is too
   narrow for a board or the clues are not there yet. Do not pad a rung and do not leave
   one empty.

5. A CATEGORY TITLE IS A PUN ON THE THEME. No scholar's name, no source book's title, no
   echo of one, no academic phrase. The board prints the bare title — never a subtitle,
   gloss, bucket label or translation under it.
     BAD:  DR. STRANGE-WALTZ · WALTZING WITH ATOMS · THE BOMB ACCORDING TO WALTZ
           LINZ WITH A TWIST · THE DIALECTIC OF ARBITRARY RULE · A CENTURY OF PERSISTENT REVOLT
     GOOD: ISOTOPES AND ISOLATION · MAD, BAD, AND DANGEROUS TO KNOW
           THE MORE THE MERRIER, STRATEGICALLY · OPPOSITION, WITH RESERVATIONS
           TWO STEPS FORWARD, ONE COUP BACK · RECIPE FOR A REVOLUTION
           A PICK-AXE TO GRIND · THE JANUS OF TEHRAN · COSSACK AND A HARD PLACE
           SHRINE AND PUNISHMENT · DESPOTS OF WISDOM · OIL, OBVIOUSLY

6. ONE FACT, ONE ANSWER. The clue carries the single fact that makes the answer the only
   one that fits. Two facts pointing two ways is a broken clue, not a rich one.

7. A YEAR NAMED IN PERSIAN NAMES ITS CALENDAR — ۱۳۵۷ خورشیدی or ۱۹۷۹ میلادی. Every time.

8. EVERY ROW CARRIES ITS SOURCE: book and author on every row, page on every row except a
   final. Never invent a page — a wrong page is worse than an honest blank. When the answer
   IS a document, the document is the source — cite the instrument, not the reading about it.

9. PERSIAN IS NOT A TRANSLATION. The Persian row mirrors the English row in id, category
   slot and value — never in question. Write the question fresh, as a Persian speaker would
   actually ask it. Give it a native Persian pun as its title: its own joke, its own idiom,
   not the English title rendered into Persian. English and Persian titles are printed
   beside each other in the bank; a translation reads as one.
     the English title ISOTOPES AND ISOLATION is not answered by «انزوای ایزوتوپها».
     «زیارت به شرط سیاست» and «بازار، بازنده ندارد» are the shape: a Persian pun that would
     land in a Tehran living room, on the same theme as its English twin.

10. HOST LINES: smug, snarky, mean, and unafraid. The correct line names the answer and
    then pays it off with a real historical fact — "Amir Kabir. He printed his own praises
    first." A bare "Correct." is the shape with the fact removed; go find the fact instead.

11. WHEN THE CORPUS DOES NOT SUPPORT A FACT, DO NOT WRITE THE ROW. Say so in a short note
    outside the JSON. A citation for a book that does not exist cannot be caught by any
    checker; it can only be prevented by not writing it.

12. NO ENTITY ANSWERS TWICE IN ONE COLUMN. The five clues in a category answer five
    different things. Two rungs landing on one entity — the same body, person, city or
    event under two spellings — is the same defect as a repeated question, and it hides:
    `Guardian Council` and `Council of Guardians` are one answer, so are `Anzali` and
    `Enzeli`, so are `Ahmad Qavam` and `Qavam al-Saltana`. Compare the answers *and their
    aliases*, normalized (lower case, punctuation and ZWNJ stripped, leading articles
    dropped), across all five rungs before you call the column done. No checker looks for
    this.

13. EVERY CATEGORY TITLE IS UNIQUE BANK-WIDE. The board deals a title once and never
    returns it, and the single round is dealt first — so a title used in both rounds is a
    double category that can never be opened, with all five of its rungs sitting there
    unreachable. A theme you want to reprise gets a title of its own.

BEFORE YOU OUTPUT, RE-READ EVERY ROW AND ASK
  - does any clue say "chapter", "reading", "this text", "the module"?
  - does any clue name a modern scholar who is not the answer?
  - does any clue echo its source book's title?
  - does any category title name a person, a book, or a phrase from a book?
  - does every category have exactly five clues, one at each rung?
  - do any five clues in a category all come from one source, or more than two from any
    one source?
  - is the Persian title a pun of its own, or the English one translated?
  - does every row carry book, author, and a page (or a final's honest blank)?
  - does every settlable Persian year name its calendar?
  - does any English clue carry Persian script or parenthetical Persian dates?
  - do two rungs of one category answer the same entity, under any spelling?
  - is every category title unique across the whole bank, both languages?
  - is the correct answer placed at index 0 on every clue?
Then fix them. Only then output the JSON.
```

---

## Prompt 2 — the guard

Append this to any extraction or authoring prompt that is already running, when you do not
want to rewrite the whole thing.

```
HARD RULES. A row that breaks any of these is not a row; drop it and mine elsewhere.

1. THE CLUE STANDS ALONE. No "in this chapter", "in Chapter 9", "in this week's reading",
   "the assigned text", "in this essay/piece/text", "the unit", "the module", "as we saw
   above". State the fact as a fact.

2. NAME NO SOURCE IN THE CLUE. No "According to Waltz", "Katouzian argues", "Chehabi
   classifies", "Keshavarzian identifies", no book title echoed in the clue. The book,
   author and page print under the answer once the round closes. One exception: the scholar
   IS the answer.

3. BUILD CATEGORIES BY THEME, NOT BY SOURCE. Five clues around one subject the audience
   could argue about — a coup, oil, the press, the clergy, the army, the exiles. At least
   three different sources in every category, never more than two clues from one source.
   A category whose five clues share one source IS the defect, even when it plays fine.

4. A CATEGORY IS FIVE CLUES, ONE AT EACH RUNG. single: 200 400 600 800 1000.
   double: 400 800 1200 1600 2000. Never two at one value, never four clues.

5. A CATEGORY TITLE IS A PUN ON THE THEME. No scholar's name, no source book's title, no
   echo of one, no academic phrase, no subtitle or gloss under the header.
     BAD: DR. STRANGE-WALTZ · LINZ WITH A TWIST · THE DIALECTIC OF ARBITRARY RULE
     GOOD: ISOTOPES AND ISOLATION · COSSACK AND A HARD PLACE · SHRINE AND PUNISHMENT

6. ONE FACT, ONE ANSWER. Two facts pointing two ways is a broken clue, not a rich one.

7. A YEAR NAMED IN PERSIAN NAMES ITS CALENDAR — ۱۳۵۷ خورشیدی or ۱۹۷۹ میلادی.

8. EVERY ROW CARRIES ITS SOURCE: book and author on every row, page on every row except a
   final. Never invent a page. When the answer IS a document, cite the instrument.

9. PERSIAN IS NOT A TRANSLATION — not the question and not the title.

10. HOST LINES: smug, snarky, mean. Name the answer, then pay it off with a real fact.

11. NO ENTITY ANSWERS TWICE IN ONE COLUMN. Two rungs of a category landing on the same
    body, person, city or event is one fact in two slots — and it hides behind a second
    spelling (`Guardian Council` / `Council of Guardians`, `Anzali` / `Enzeli`). Compare
    the five answers *and their aliases*, normalized, before you call the column done.

12. EVERY CATEGORY TITLE IS UNIQUE BANK-WIDE. The single round is dealt first and a dealt
    title is never returned, so a title used in both rounds is a double category that can
    never be opened.

13. NO PERSIAN SCRIPT IN ENGLISH CLUES. English clues must never carry parenthetical Persian
    dates (like `(۲۰ اسفند ۱۳۵۷)`) or Persian characters. Use Gregorian dates in English; if an
    Iranian calendar day is historically significant, transliterate it (`30 Tir`, `15 Khordad`).

14. CORRECT ANSWER ALWAYS AT INDEX 0. Always store options[0] as the correct answer (`correct: 0` /
    `correct_option_index: 0`). The runtime engine shuffles options randomly upon dealing.

Before output: does any clue say "chapter" or name its own author? Does any title name a
book or person? Does any category draw on fewer than three sources? Does any category miss
a rung? Do two rungs of one category answer the same entity? Is every title unique across
the bank? Fix them, then output.
```

---

## Prompt 3 — the re-cut

For a bank that already exists and plays fine, but whose categories are shelves for single
books. This is a **partition problem**, and models fail it when it is posed as arithmetic.

**The lesson, paid for once.** Given a flat batch of 80 clues and the rule "each category
takes one from each of the five values", GPT-5.6 at low reasoning refused outright —
*"No valid partition exists: the batch has 80 clues, but rung counts are unequal (200: 16,
400: 16, 600: 17, 800: 16, 1000: 15)"* — a miscount, but a fatal one. Handed the identical
80 clues **pre-sorted into five named blocks of sixteen**, it returned sixteen clean boards,
one clue per rung, four to five sources each, titled *COSSACK AND A HARD PLACE*, *SHRINE AND
PUNISHMENT*, *DESPOTS OF WISDOM*, *REEL EXILES OF IRAN*. Never ask a model to verify a
partition it can be given structurally. Sort the batch yourself and label the blocks.

Also: never send a batch whose rung counts are unequal, and never send more than about 80
clues (16 categories) in one call. Shard at 16 per rung.

```
You are re-cutting the categories of a clue bank. Output JSON only. No prose.

THE JOB
Below is a batch of clues from one round. Right now they are filed under categories that
are shelves for a single book. Re-file them into categories that are THEMES. A category is
five clues about one subject the audience could argue about — a coup and its aftermath,
oil, the clergy, the press, the army, the exiles, a decade, a rivalry. Never a subject
defined by who wrote about it.

HARD CONSTRAINTS
1. Partition EVERY clue in the batch. No clue dropped, no clue used twice.
2. The batch arrives in five blocks, A through E, sixteen clues each. Every category takes
   EXACTLY ONE clue from each block and no more than one. Sixteen categories therefore
   consume the batch exactly once. Do not do arithmetic on this — the block rule IS the
   partition.
3. Each category draws on AT LEAST THREE different `book` values. At most two clues in a
   category may share one book.
4. The five clues in a category must genuinely belong together — a player who reads the
   title should be able to guess the domain, and the hardest clue should feel like the same
   subject as the easiest.

THE TITLE
A pun on the theme, ALL CAPS, in the show's register: smug, snarky, mean, unafraid.
  - no scholar's name, no source book's title or echo of one
  - no subtitle, gloss, translation, or bucket label — the board prints the bare title

TWO LANGUAGES, ONE CATEGORY
Give each category an English title and a Persian title. The Persian title is NOT a
translation. Write it fresh, in Persian script, as a pun a Persian speaker would actually
make on the same theme — its own joke, its own idiom.

OUTPUT — JSON only, nothing else:
[{"title_en": "THE ENGLISH PUN", "title_fa": "جناس فارسی",
  "ids": ["id_1","id_2","id_3","id_4","id_5"]}, ...]

Count your output before you finish: the ids must total exactly the number of clues below.

THE BATCH
### BLOCK A — pick EXACTLY ONE clue from this block per category
{"id": "…", "theme": "…", "answer": "…", "clue": "…", "book": "…"}
…
### BLOCK B …
```

**After the model returns, verify — do not trust it.** Parse the JSON; check every category
has five ids, one per rung, and three or more distinct books; check every id in the batch is
used exactly once. Two failure modes are routine at low reasoning effort and both are
cheap to repair mechanically:

- **A leaked partition.** The same clue lands in two categories and another is dropped. In
  practice the duplicate sits at the same rung as the clue it displaced, so the repair is
  exact: move the missing clue to the rung slot of one duplicate. **Then re-read the whole
  column, not just the rung you touched** — the moved clue brings its own answer, and the
  entity it now duplicates is rarely the one it displaced.
- **A title collision.** Two categories end up with the same title. Send those back for
  renaming; do not ship a board with two identical headers. A re-cut can produce this
  *across* the two rounds — the repair pass of 2026-09-20 did, 27 English and 9 Persian
  times — and the cost is silent: the single round is dealt first, so a title it takes is
  gone, and the double category holding all five of its rungs can never be opened. Rename
  in **both** languages; the two banks must end with the same number of distinct titles.

What the model is good at is the theme and the joke. What it is unreliable at is counting.
Divide the labour that way: **it chooses, code verifies.**

---

Written 2026-09-20. The MAIN bank had already been swept for both defect classes — 263
English and 245 Persian clue rewrites, six source-bound category titles retitled — when the
deeper defect surfaced: 499 of 708 categories drew all five clues from one book. The re-cut
re-partitioned the whole round structure into theme categories, at least three sources each,
titled in both languages. It also gave every category a title of its own, which the bank did
not have before: the two languages now carry **3,752 rows** each under **803 distinct
titles** (383 single, 348 double, 72 final), the same 803 on both sides.
