# MAIN batch hand-over prompt

For Gemini, which has already drafted a batch of fresh rows for MAIN. The prompt tells it to
rework that draft against the rules the bank now plays by, then hand back the two files. It
does not land them — a person reads the rows against their sources and lands them.

Attach nothing. The prompt points at the repo; the only file worth pasting alongside is
`QuestionBank/BANK_DIGEST.md`, and Gemini can read it from the tree.

---

```
You are authoring a batch of fresh clue rows for the MAIN bank of the Iranian Edition of
Jeopardy. You have already drafted a batch. Your job now is to rework that draft against the
rules below and hand it back. You are not landing it: a person reads the rows against their
sources and lands them.

WHAT CHANGED, AND WHY YOUR DRAFT HAS TO MOVE
MAIN was re-cut on 2026-09-20. Before that, 499 of its 708 categories were shelves for a single
book — five clues from one monograph, which reads as a bibliography. The board gives nothing
away, but the citation prints under the answer at the reveal, so the same book comes up five
times in a row and the column reads as one author's greatest hits. Every category in MAIN now draws on at
least three different books, and a category is a theme with a pun on it rather than one
author's output. Your batch joins that bank, so it is shaped the same way — and the two defect
classes the re-cut exposed are now rules:

  - A CATEGORY NEVER HOLDS THE SAME ANSWER AT TWO RUNGS. The re-cut created ten of these by
    pulling themed rows together. Both checkers were blind to it: one compares clue text, the
    other never looks at answers, and a column whose five clues read three books passed the
    whole time.
  - TWO CATEGORIES IN THE SAME ROUND NEVER SHARE A TITLE, in either language. The board
    builder groups by the raw category string, so a name spelled two ways in one round is one
    column of ten and the round deals short. Punctuation and Persian diacritics are folded
    first, so nearly-identical is identical.

READ FIRST, IN THE REPO
  QuestionBank/BANK_DIGEST.md       every English clue already on the board, by category
  QuestionBank/BANK_DIGEST_fa.md    the Persian board
  BANK_AUTHORING_PROMPT.md          the rules behind these, with the bad and the good of each
  CORPUS_BRIEF.md                   the corpus contract
Do not open QuestionBank/verified_clues.json or verified_clues_fa.json. 3,752 rows is more than
you can hold, nothing in this job writes to them, and the digest is the view of the bank you
get — it is the thing that keeps you from repeating it.

SOURCES
  Sources/MAIN CORPUS/8 - New Additions (2026-09)   this batch's sources; read these first
  Sources/MAIN CORPUS/1-7                           already mined. Use only for a fact folder 8
                                                    does not carry, and expect the digest to
                                                    already hold the obvious ones.

THE ARITHMETIC, GIVEN UP FRONT. Do not derive it, and do not do arithmetic on it.
  - A board draws six categories of five clues.
  - single round: 200 400 600 800 1000     double round: 400 800 1200 1600 2000
  - A category is EXACTLY five clues, one at every rung of its round — never two at one value,
    never four. The board builder discards a four-clue category silently.
  - Every rung of a round therefore needs the same number of clues, in your batch as in the
    bank. A round whose 1000 rung is thin cannot be dealt. Send complete categories, not a
    flat pile of rows.
  - Difficulty is DERIVED FROM THE VALUE, never chosen. There are two ladders, and the wrong
    one still looks fine and still plays:

      single   200 CASUAL     400 STANDARD   600 STANDARD    800 SCHOLAR   1000 INSUFFERABLE
      double   400 STANDARD   800 STANDARD  1200 SCHOLAR    1600 SCHOLAR  2000 INSUFFERABLE
      final      0 INSUFFERABLE

    It goes wrong by applying the ladder by position instead of by value: on the double round
    that puts CASUAL on 400 and STANDARD on 1200, and gets 800, 1600 and 2000 right by
    accident, so exactly two rows per double category come out wrong. A mislabelled row is not
    cosmetic — the robot players nudge their accuracy by the label, so the row plays easier
    than its rung says.

HARD RULES. A row that breaks one is not a row — drop it and mine elsewhere.

1. THE CLUE STANDS ALONE. A player has read nothing: no book, no chapter, no syllabus. Never
   write a clue that points at text the player cannot see — "in this chapter", "in Chapter 9",
   "in this week's reading", "the assigned text", "in this essay/piece", "the unit", "the
   module". State the fact as a fact.

2. NAME NO SOURCE IN THE CLUE. The book, author and page print under the answer once the round
   closes; inside the clue they are dead weight.
     FORBIDDEN: "According to Waltz", "Katouzian argues", "Chehabi classifies", "as documented
     by Amal Saad", "In A Social History of Iranian Cinema, Naficy credits…", and any echo of
     the source book's title.
   ONE EXCEPTION: the scholar IS the answer. Then the name is the question and stays.
     BAD:  "In his comparative study, Chehabi utilizes this term for rule without law."
     GOOD: "This two-word term names rule unconstrained by any settled legal order."

3. CATEGORIES BY THEME, NOT BY SOURCE. A category is five clues about one subject the audience
   could have opinions about — a coup, oil, the press, the clergy, the army, the exiles, a
   decade, a rivalry. At least three different books per category, and never more than two
   clues from any one book. A category whose five clues share one source IS the defect, even
   when it plays fine.

4. A CATEGORY IS FIVE CLUES, ONE AT EACH RUNG. If you cannot fill every rung from the material,
   the category is not finished — do not pad a rung and do not leave one empty.

5. THE TITLE IS A PUN ON THE THEME. No scholar's name, no source book's title or echo of one,
   no academic phrase. The board prints the bare title: never a subtitle, gloss, bucket label
   or translation under it.
     BAD:  DR. STRANGE-WALTZ · WALTZING WITH ATOMS · LINZ WITH A TWIST
           THE DIALECTIC OF ARBITRARY RULE · A CENTURY OF PERSISTENT REVOLT
     GOOD: ISOTOPES AND ISOLATION · COSSACK AND A HARD PLACE · SHRINE AND PUNISHMENT
           DESPOTS OF WISDOM · RECIPE FOR A REVOLUTION · THE ECONOMY HAS LEFT THE STATE
           PACT AND FURIOUS · A PICK-AXE TO GRIND

6. ONE ANSWER PER COLUMN. No category carries the same canonical_answer at two rungs.

7. ONE TITLE PER ROUND. No two categories in the same round share a title, in either language.

8. A NEW QUESTION, NEVER A REPEATED ONE. No question on the board may be asked twice anywhere —
   not just inside one slot. Two rows in different categories at different rungs asking the
   same thing is the same defect as an exact copy, and a match can deal both. It happens when
   two themed categories on one subject reuse their best fact. "Same" is measured: six or more
   content words in common and 75% of the shorter clue's. Repeating an ANSWER is fine and
   deliberate; repeating a QUESTION is not.

9. ONE FACT, ONE ANSWER. The clue carries the single fact that makes the answer the only one
   that fits. Two facts pointing two ways is a broken clue, not a rich one.

10. EVERY ROW CITES ITS SOURCE, AND THE CITATION IS COPIED, NEVER COMPOSED. Book and author on
    every row, page on every row except a final. Take book_title as the work prints it and the
    author from that work's own title page. A chapter is cited by its book's title and the
    chapter's own page — never build a title out of a chapter subtitle's words, which is how a
    plausible book that does not exist gets made. Never invent a page: a wrong page is worse
    than an honest blank. When the answer IS a document, cite the instrument, not the reading
    about it. If you cannot find the sentence you are citing, the citation is wrong — drop the
    row and name it in your hand-back. No checker can catch an invented citation; a person
    reading it against the shelf is what catches it.

11. A YEAR NAMED IN PERSIAN NAMES ITS CALENDAR — ۱۳۵۷ خورشیدی or ۱۹۷۹ میلادی. Every time. An
    Iranian year is shamsi; a non-Iranian year, or an Iranian year before roughly 1800, keeps
    its Gregorian numeral and takes میلادی; a year from about 1800 on is rewritten into shamsi.
    A 12xx–14xx year after a Persian month name is shamsi and you may take that. A bare numeral
    is a defect — ۱۳۵۰ is 1971 shamsi and 1350 CE, and both readings occur on the board.

12. PERSIAN IS NOT A TRANSLATION — not the question and not the title. The Persian row mirrors
    the English row in id, rung and value, never in wording. Write the question fresh, the way
    a Persian speaker would ask it. Give it a native Persian pun: its own joke, its own idiom,
    not the English title rendered into Persian. The two titles print beside each other in the
    bank, and a translation reads as one.
      the English title ISOTOPES AND ISOLATION is not answered by «انزوای ایزوتوپها».
      «زیارت به شرط سیاست» and «بازار، بازنده ندارد» are the shape: a Persian pun that would
      land in a Tehran living room, on the same theme as its English twin.

13. HOST LINES ARE WRITTEN FRESH. Smug, snarky, mean, unafraid. The correct line names the
    answer and then pays it off with a real historical fact — "Amir Kabir. He printed his own
    praises first." A bare "Correct." is that shape with the fact removed; go and find the fact.
    The shipped bank already ends 893 of its 1,000 lines in three stock tails ("Spot on!", "The
    history holds!", "Quite right."). Do not reproduce them, and do not end your lines in one
    shared tail of your own.

THE ROW. All 27 fields, spelled exactly as the archive spells them. The English file:

{
  "id": "single_<slug>_200",            // single_<slug>_<value> | double_<slug>_<value> |
                                        // final_<slug>. <slug> names the category set and is
                                        // unique in the bank. The two files mirror id for id.
  "language": "en",
  "category": "THE ENGLISH PUN",        // byte-identical across the category's five rows
  "historical_period": "…",             // reuse the spelling MAIN already uses for these sources
  "theme": "…",                         // one lowercase subject word: oil, press, clergy, war…
  "difficulty": "CASUAL",               // derived from the value, never chosen
  "value": 200,
  "round": "single",                    // single | double | final
  "clue_text": "The clue. One fact. Stands alone.",
  "canonical_answer": "The answer, shortest correct form.",
  "accepted_aliases": ["…"],            // never empty
  "partial_answers": ["…"],
  "specificity_prompt": "Asked when the answer is right but under-specified.",
  "options": ["…", "…", "…", "…"],      // four; options[0] IS the canonical answer
  "correct_option_index": 0,            // 0 on every row
  "distractor_rationales": [            // one object per wrong option, in order
    { "option": "…", "why_plausible": "…", "why_wrong": "…" }
  ],
  "explanation": "One or two sentences of context, after the answer is revealed.",
  "source_id": "amanat_iran_modern_history_2017",
  "book_title": "Title as printed on the work.",
  "author": "Author of that work.",
  "chapter": "Chapter or section, when the source has one.",
  "page": 300,                          // printed page; null on a final; NEVER invented
  "supporting_passage": "The sentence in the source that carries the fact.",
  "evidence_type": "established_fact",
  "confidence": 1.0,
  "editorial_validation_status": "draft",
  "host_reactions": { "correct_generic": "…", "wrong_generic": "…" }
}

The Persian file carries the same ids, and every field in the row's OWN language: category is
the Persian pun, canonical_answer and options are Persian, aliases carry the Persian forms
AND the Latin transliterations, host lines are Persian. `language` is "fa".

FIELD TRAPS. Each of these fails the batch, or worse, the archive.

  - evidence_type is one of four words: established_fact, scholarly_interpretation,
    primary_testimony, disputed — and established_fact on almost everything. A quotation is
    not a fifth kind: the enum splits evidence by where the claim comes from, and the quotation
    already has its own field, supporting_passage. Any other spelling is not a softer label —
    it stops the WHOLE archive loading, which takes the test suite down with it.
  - confidence is the number 1.0 on every row. Not "high", not "CONFIRMED". A status word goes
    in editorial_validation_status, the string field beside it.
  - editorial_validation_status is "draft" — you wrote the row, nobody has read it against its
    source. A person sets "verified" and lands it. There is no override, and that is the point
    of the field.
  - correct_option_index is 0 on every row. The engine reshuffles when it deals. Do not spread
    the index.
  - The answer must not appear in the clue text.
  - accepted_aliases is never empty, and an alias belongs to its own row's answer and no other.

DELIVERABLE
  QuestionBank/incoming/<stem>-en.json     bare JSON array, English rows
  QuestionBank/incoming/<stem>-fa.json     the same ids, Persian rows
Two files or the batch is refused: the archives mirror id for id. Nothing else in the repo is
yours to write — Web/data/clues.js is generated, and editing it does nothing.

Do not run Tools/append_batch.py. It refuses a batch of drafts by design, before it checks
anything else, and that refusal is the honest state of your work: a row is a draft until
somebody has opened the book and found the passage.

NOT YOURS
  - The three archive validators — validate_1000_clues.py, verify_flawless_state.py,
    validate_persian_bank.py — pin the row count and the category count, and will fail after any
    merge by arithmetic rather than because something is wrong. Do not edit those numbers.
  - 237 English rows on the board name their own cited author inside the clue. The rule now
    forbids that shape and the bank has not been swept yet, so rule and bank disagree by design.
    Do not add new ones, and do not sweep the old ones. That is not this batch.

BEFORE YOU OUTPUT, READ EVERY ROW BACK AND ASK
  - does any clue say "chapter", "reading", "this text", "the module", "as we saw above"?
  - does any clue name a modern scholar who is not the answer, or echo its source book's title?
  - does any category title name a person, a book, or a phrase from a book?
  - does any category have other than five clues, or two clues at one rung?
  - do any five clues in a category come from fewer than three books, or more than two from one?
  - does any category hold the same answer at two rungs?
  - do any two categories in the same round share a title, in either language?
  - is any question already in the digest, word for word or reworded?
  - is the Persian title a pun of its own, or the English one translated?
  - does every row carry book, author, and a page (or a final's honest blank)?
  - does every settlable Persian year name its calendar?
  - is every difficulty the one its value gives, checked by value and not by position?
  - does any host line end in "Spot on!", "The history holds!", "Quite right.", or a shared tail
    of your own?
Then fix them. Only then write the files.

HAND BACK — counts, not a document
Rows written; complete categories per round; finals; how many distinct books the batch draws
on; how many host lines end in a shared tail; and anything the corpus could not support, naming
the row ids you dropped for want of a source. "Done" is not a handoff. If the sources do not
yield complete five-rung theme categories, say so and stop — that is the honest result, and it
is the one we want to hear.
```

---

Written 2026-09-20, after the re-cut. Two things in the older prompt files disagree with the
shipped archive and are corrected here: `BANK_AUTHORING_PROMPT.md`'s Prompt 1 row shape gives
`evidence_type` as `direct | inferred | synthesis`, `confidence` as `high | medium | low`,
`editorial_validation_status` as `unreviewed`, string `distractor_rationales`, and an id pattern
of `<period>_single_<slug>_<value>`. None of those five match the archive. `GEMINI.md`'s field
list is right; this prompt takes its shape from the archive itself, row by row.
