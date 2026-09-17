# Pahlavi course bank — authoring brief for this pass

You are writing clue rows for the **Pahlavis** course edition of the Jeopardy Iranian
Edition. The bank already holds 150 rows a language (30 categories). This pass adds the
rest: 35 single categories, 35 double categories and 12 finals, per language, to bring
the course to 50 single + 50 double + 12 finals = **512 rows a language**.

Read this file completely before writing anything. It supersedes your instincts about
what a good quiz question looks like — Jeopardy has its own shape and this bank has its
own schema. Where this file and any other document disagree, this file wins.

---

## 1. Where you write

Write **one file per language** into the batch folder you are told to use:

```
Course/banks/pahlavi-pass-2026-09-18/batches/<group>-en.json
Course/banks/pahlavi-pass-2026-09-18/batches/<group>-fa.json
```

Each file is a bare JSON array of row objects. No wrapper object, no comments, no
trailing commas. The two files must contain **the same ids in the same order** — they
mirror each other row for row. A batch with mismatched ids is refused.

The `<group>` and your **id block** are assigned in the task you were given. Ids are
`pahlavi_<4-digit>_a`, zero-padded, contiguous within your block, running first through
your single categories, then your double categories, then your finals. English and
Persian share the id: row 1 of `-en.json` and row 1 of `-fa.json` both carry the same id.

**Do not write to `rows-en.json` / `rows-fa.json`**, to `Web/`, or to `QuestionBank/`.
You write your two batch files and stop.

---

## 2. The row — exactly these 27 keys, spelled exactly like this

```json
{
  "id": "pahlavi_0151_a",
  "language": "en",
  "category": "THE CATEGORY TITLE",
  "historical_period": "Pahlavi",
  "theme": "military",
  "difficulty": "CASUAL",
  "value": 200,
  "round": "single",
  "clue_text": "the clue, a statement with the answer blanked out",
  "canonical_answer": "The Answer",
  "accepted_aliases": ["The Answer", "other spelling", "transliteration"],
  "partial_answers": [],
  "specificity_prompt": "",
  "options": ["The Answer", "wrong one", "wrong two", "wrong three"],
  "correct_option_index": 0,
  "distractor_rationales": [
    {"option": "wrong one", "why_plausible": "...", "why_wrong": "..."},
    {"option": "wrong two", "why_plausible": "...", "why_wrong": "..."},
    {"option": "wrong three", "why_plausible": "...", "why_wrong": "..."}
  ],
  "explanation": "one sentence saying why the answer is the answer",
  "source_id": "stephanie_cronin_anglo_iranian_relati",
  "book_title": "Anglo-Iranian Relations since 1800",
  "author": "Stephanie Cronin",
  "chapter": "Britain, the Iranian Military and the Rise of Reza Khan",
  "page": 99,
  "supporting_passage": "the sentence, copied verbatim out of the source, that proves it",
  "evidence_type": "established_fact",
  "confidence": 1.0,
  "editorial_validation_status": "draft",
  "host_reactions": {
    "correct_generic": "The Answer. then a fact about it",
    "wrong_generic": "a fresh insult, no stock tail",
    "common_wrong_answers": {},
    "specificity_prompt": "",
    "explanation": "same sentence as explanation"
  }
}
```

Copy that skeleton. Every key present, no extra keys, no missing keys. `language` is
`"en"` in the English file and `"fa"` in the Persian file. `historical_period` is
`"Pahlavi"` on every row in both languages.

---

## 3. The two difficulty ladders — derived from `value`, never chosen

This is the single most common way this bank goes wrong. The label is **looked up from
`value`**, and there are **two different ladders**. The mistake is applying one ladder by
position (first rung casual, second standard, third standard, fourth scholar, fifth
insufferable) — which is right for `single` and wrong for `double`.

```
round    value   difficulty
single    200    CASUAL
single    400    STANDARD
single    600    STANDARD
single    800    SCHOLAR
single   1000    INSUFFERABLE

double    400    STANDARD      <-- note: NOT casual
double    800    STANDARD
double   1200    SCHOLAR
double   1600    SCHOLAR
double   2000    INSUFFERABLE

final       0    INSUFFERABLE
```

A single category is five rows at values 200, 400, 600, 800, 1000. A double category is
five rows at 400, 800, 1200, 1600, 2000. A final is one row at value 0.

Write the correct label for every row. A row whose label disagrees with this table fails
the build gate by name.

---

## 4. Category integrity

**A category is exactly five rows, one at every rung of its round.** Four rows or six, or
a missing rung, and the board builder throws the whole category away without a word.

The `category` string must be **byte-identical** across all five rows — same capitals,
same punctuation, same spacing. `"OIL AND THE MAJESTIC"` and `"OIL AND THE MAJESTIC "`
are two different categories and both are broken.

Write category titles as Jeopardy writes them: short, all capitals, a joke or a pun where
it fits. Look at what is already on the board for the house voice —
`BOOTS ON THE TEHRAN GROUND`, `VOSUQ TO NO GOOD`, `TUDEH OR NOT TUDEH`,
`PULPIT VS. PEACOCK`, `FLIRTING WITH NIKITA`. That is the register. Do not reuse any
title already in the bank.

**The Persian file carries the category title in Persian.** This is the house convention
and the existing 150 rows do it — `TREATY YOURSELF TO TURKMENCHAY` is `ترکمنچای داغ` in
the Persian bank, `TSAR QUALITY` is `تزارِ خزان`. So each of your categories has **two
titles**: an English one used byte-identically on all five English rows, and a Persian
one used byte-identically on all five Persian rows. Translating the title literally is
not required — write the Persian title that does the same job in Persian, the way the
Qajar example does. Reuse the Persian title on the matching five rows and no others.

A category's five rows should sit at five clearly different difficulty levels of the
*same subject*: the 200 is something a well-read undergraduate knows, the 1000 is
something only a specialist knows.

---

## 5. `theme` is not free text

`theme` is a **single lowercase keyword** that the Persian edition matches against a
fixed list to print a subtitle. Pick a keyword that **appears as a substring inside** one
of these lists, or the category's Persian subtitle renders as the catch-all "متفرقه".

Reach for one of these words, chosen to fit the category's actual subject:

- people → `monarchy`, `royal`, `figure`, `pioneer`, `tragic`, `coronation`
- places → `caspian`, `gulf`, `city`, `capital`, `frontier`, `mountain`, `geograph`
- history → `military`, `war`, `occupation`, `coup`, `revolution`, `rebellion`,
  `constitution`, `reform`, `uprising`, `movement`, `purge`, `conflict`, `dynast`
- culture → `clergy`, `religion`, `poet`, `cinema`, `music`, `education`, `press`,
  `philosoph`, `spectacle`
- politics/economy → `politic`, `diploma`, `oil`, `petroleum`, `econom`, `party`,
  `intelligence`, `ideolog`, `statecraft`, `agriculture`, `infrastructure`, `treasury`,
  `sanction`, `law`, `geopolit`

Good: `"oil"`, `"diploma"`, `"military"`, `"clergy"`, `"constitution"`.
Bad: `"oil nationalization"`, `"Oil"`, `"the coup"`, `"gender"` — none of those match.

---

## 6. The clue

Jeopardy works backwards. The clue is a **statement with the answer left out**, and the
contestant supplies the thing the statement is about. Write it as a plain declarative
sentence, not a question.

- **The answer must not appear in the clue text.** Any form of it — spelled, translated,
  romanised. If the answer is "Musaddiq", the clue cannot contain "Musaddiq",
  "Mosaddeq", "Mossadegh" or "مصدق".
- A clue points at exactly one thing. If two answers would fit, it is not a clue.
- The best clues carry a second, verifiable detail that makes the rung's difficulty
  honest, rather than just withholding the name.
- No "this Iranian leader", "this man", "this thing" filler. Write the fact.

Register: the show's host is smug and mean, but the *clue* is straight. The jokes live in
the host lines and in the category titles, never in the clue.

---

## 7. Options and rationales

- **Exactly four options.** `options[0]` is always the canonical answer, verbatim.
- **`correct_option_index` is `0` on every row in this bank.** Always. The engine
  reshuffles the options when it deals, so writing 0 is correct and spreading the index
  is a defect.
- The three wrong options must be **wrong for a reason** — a plausible contemporary, a
  near-miss, a thing from the same year or the same institution. Not a random other noun.
- `distractor_rationales` is a **list of exactly three objects**, one per wrong option, in
  the same order as the wrong options appear in `options`. Each object names its own
  option in `option` exactly as it is spelled in `options`, then says
  `why_plausible` (why a student might reach for it) and `why_wrong` (the fact that rules
  it out). Never a dict keyed by the option text.
- `explanation` is one sentence: why the answer is the answer.
- `host_reactions.common_wrong_answers` may be `{}` or a dict mapping a tempting wrong
  option to a one-line correction.

---

## 8. Aliases

`accepted_aliases` is **never empty**. It leads with the canonical answer itself, then
carries every other spelling, transliteration, honorific and script a contestant might
type, in **both Latin and Persian script** on the English row too.

- Every alias must share a real string with its own row's answer. An alias belongs to its
  own row and no other. `"Cossack Division"` may not carry `"South Persia Rifles"` as an
  alias.
- Only add an alias that is genuinely another name for the same thing. Adding a plausible
  neighbour is how a right answer gets scored wrong.

Example: for `the Caspian Sea` →
`["Caspian", "Caspian Sea", "Bahr-e Khazar", "Darya-ye Khazar", "Mazandaran Sea", "دریای خزر", "دریای مازندران"]`

---

## 9. Host lines — written fresh, never a stock tail

`correct_generic` and `wrong_generic` are the host's spoken lines. They are the one place
the show's meanness lives.

**Shape for `correct_generic`: name the answer, then pay it off with a fact.**
`"Cossack Division. Marched into the capital and forgot how to leave."`

- No praise (`Correct.`, `Exactly.`, `Well done.`, `Spot on!`).
- No admiration standing in for a fact.
- **Do not end any line in these tails** — the shipped bank already ends 893 of its 1,000
  lines in them and this bank must not add more: `"Spot on!"`, `"The history holds!"`,
  `"Quite right."`
- Vary the shape. Some lines are a fact, some are a dry aside, some are a verdict on the
  contestant. Write each one for its own clue — a line that would fit any clue in the
  category is a bad line.
- `wrong_generic` is a fresh insult. Mean is fine, profane is fine, cruel about the
  answer is fine. It must never be the same sentence twice in your batch.

---

## 10. Citations — copied off the work, never composed

**You may only cite the readings in your assigned week folder.** The PDFs are at:

```
/Users/Morad/Desktop/Pahlavis (Michaelmas 2016)/Weeks/Week <N>/
```

Read them with `pdftotext -layout "<file>" /tmp/<name>.txt` and then read the text.

The rule that matters most in this whole brief:

- **Take `book_title` and `author` as the work prints them.** A journal article is cited
  by its **journal's title** as `book_title` and its **author** as `author`; the article's
  own title goes in `chapter`.
- **Never build a book title out of the words of a chapter's subtitle.** That is exactly
  how a plausible book that does not exist gets invented, and no checker can catch it — a
  person reading the citation against the shelf is what catches it.
- **`page` is the printed page number, as it appears on the page.** Not the PDF's internal
  index. If the article starts at printed page 501, the first page is 501, not 1.
- **The `page` must fall inside the range that work occupies.** A chapter printed at
  47–65 is not at p. 8.
- **`supporting_passage` must be a sentence you actually found in the source you named.**
  Copy it verbatim. If you cannot find the sentence, the citation is wrong — change the
  row, or drop it.
- **If you cannot source a row at all, drop it and say so in your report.** An honest gap
  costs one slot. An invented citation is printed on screen under the answer.

`source_id` is a lowercase slug of the citation, e.g. `stephanie_cronin_anglo_iranian_relati`.
Make it stable and derived from author + short title.

`evidence_type` is `"established_fact"` for things the sources state as fact, or
`"contested"` / `"interpretation"` where the readings argue rather than state.
`confidence` is `1.0` for a sourced established fact; lower it if the reading is doing
interpretive work.

---

## 11. A final round row

A final answers for a whole book and is the hardest rung.

- `round`: `"final"`, `value`: `0`, `difficulty`: `"INSUFFERABLE"`.
- Its `category` is **unique to that one row** — a final is not a five-row category.
- **`page` is `null`.** It carries `book_title` and `author` and no page.
- The clue is long and densely detailed — a final is where the show lets a clue run to
  three clauses.

---

## 12. The Persian row is its own question

`rows-fa.json` is **not a translation of `rows-en.json`.** It is the same clue slot asked
in Persian, and it should be written as a Persian-language question: its own phrasing, its
own aliases, its own distractors, its own host lines, its own `supporting_passage`
(a Persian sentence from the source if the source is in Persian, otherwise the same
English sentence). Same `id`, same `category` (in Latin capitals — category titles stay in
English in both files), same `value`, `round` and `difficulty`.

The canonical answer in the Persian row is the Persian name of the thing. `fa_answer ==
en_answer` in a near-zero number of rows in the shipped banks, and that is correct.

`category` is the one field where the two files deliberately differ: the English file
carries the English title, the Persian file carries the Persian title of the same
category. Everything else — `id`, `value`, `round`, `difficulty`, `theme`,
`historical_period` — is identical across the pair, and the two files hold the same
number of categories in the same order.

Write the Persian without machine-translation stiffness — Morad is a native speaker and
this is the edition he will actually play.

---

## 13. No question is asked twice anywhere in the bank

Not in your batch, and not against the 150 rows already in `rows-en.json` /
`rows-fa.json` (read them, they are in the folder above you). Repeating an **answer** is
fine. Repeating a **question** is not.

"Same question" is measured, not judged: **six or more content words in common AND 75% of
the shorter clue contained in the longer.** Two rows in different categories at different
rungs asking the same thing is the same defect as an exact copy.

The trap is a pair of twin categories on one subject (two categories both about the 1953
coup, or both about oil) reusing their best fact across the pair. Watch for it
specifically when you write your second category on a subject you have already used.

---

## 14. Self-check before you hand back

Run this over your own batch file and fix everything it names before reporting:

```bash
python3 Course/banks/pahlavi-pass-2026-09-18/selfcheck.py <group>
```

It checks: 27 keys on every row; ids unique, contiguous, and mirrored between the two
languages; every category whole (five rows, all five rungs, byte-identical title); every
`difficulty` matching the ladder for its `value` and `round`; `options` four unique
entries with `options[0] == canonical_answer`; `correct_option_index == 0`;
`distractor_rationales` three items in wrong-option order; aliases non-empty and
overlapping the answer; answer text absent from its own clue; page present except on
finals; and no repeated question inside the batch.

Fix the batch until it passes, then report counts — not prose.
