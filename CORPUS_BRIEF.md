# Corpus brief — for an agent generating clues

You are being handed a body of source material and asked to turn it into playable
Jeopardy clues. This one page is your contract. `QUESTION_AUTHORING.md` is the long
form; read it before you write anything. `BANK_SCOPE.md` decides which bank you may
write into. Where this page and those disagree, they win.

## 1. Say which bank you are writing, before you write

There are two destinations and the rule between them runs **one way only**:

| you are writing… | into | which is |
|---|---|---|
| a **course / syllabus / subject** bank | `Web/courses/<course-id>/data/bank-en.js` (+ `bank-fa.js`) | locked to that syllabus |
| **MAIN** | `QuestionBank/verified_clues.json` (+ `_fa`) | the umbrella — everything ever designed |

A course question may later join MAIN, by being **re-authored** into MAIN's shape and
voice. A MAIN clue may **never** be copied down into a course bank to make up the 60 a
game needs. If your syllabus yields fewer than sixty, say so and stop. Do not borrow.

If you were given a syllabus, you write **two files and nothing else**, and your globals
are `window.COURSE_CLUES_<ID>` and `window.COURSE_CLUES_<ID>_FA` — `<ID>` being the
course folder in upper snake case, which is also the folder name, the `?ed=` value and
the `data-edition` attribute. Writing `window.CLUES` or a file named `clues.js` makes the
*general* edition play course questions. See `BANK_SCOPE.md` §"For an agent working a
syllabus" — it is the operative half of that document.

If your corpus is MAIN CORPUS in `Sources/MAIN CORPUS/`, you write
`QuestionBank/verified_clues.json` and `QuestionBank/verified_clues_fa.json` — the archive,
two files, one language each, ids mirrored across the pair **with each mirrored row
carrying its own question** (§5). Then stop: the play files are generated from the archive
by C3PO with `Tools/render_bank.py`, never by you. Use the archive's field names (§2),
append to the array, and **do not re-serialise the whole file** — it is pretty-printed at
`indent=2` with no trailing newline, and any other form (compact, a different indent, a
trailing newline) rewrites all 2,000 rows to move one. The bank already holds 1,000
clues; before writing, confirm your subject is not already on the board.

## 2. The two shapes do not match — this is the trap

Field names differ between the archive and the play file. A row written in the wrong
shape lands silently and plays as blank.

| | archive (`verified_clues.json`) | play (`Web/data/clues.js`) |
|---|---|---|
| question | `clue_text` | `clue` |
| answer | `canonical_answer` | `answer` |
| aliases | `accepted_aliases` | `aliases` |
| correct index | `correct_option_index` | `correct` |
| source | `book_title`, `historical_period`, `supporting_passage` | `book`, `period`, `passage` |
| host lines | `host_reactions.correct_generic` / `.wrong_generic` | `correctLine` / `wrongLine` |

`id`, `round`, `value`, `category`, `theme`, `difficulty`, `options`, `explanation`,
`author`, `page` pass through untouched.

**The archive is canonical and the play file is generated from it.** You append to the
archive; then C3PO runs

```
python3 Tools/render_bank.py
```

to regenerate both play files from both archives. `--check` renders in memory and reports
divergence without writing, which is how you prove a play file has not been hand-edited.
**Nothing else writes these files.** (An earlier version of this page named
`Tools/append_flawless_engine.py`; that is a spent one-shot migration appender, not a
generator. It rewrites both archives from its own in-memory copies, so re-running it would
silently drop every clue appended since it was written.)

Never hand-edit `Web/data/clues.js` — it is overwritten. A course bank is the opposite:
you write `Web/courses/<course-id>/data/bank-en.js` directly, in the play shape, by hand,
with no archive behind it.

The play file's **key order is load-bearing** — its keys are in the order the table above
lists them, `json.dumps` preserves insertion order, and the engine reads them by name.

## 3. The rungs — `value` is a slot key, not money

| round | `value` must be one of | the tile then prints |
|---|---|---|
| single | 200, 400, 600, 800, 1000 | 10, 25, 50, 100, 200 million toman |
| double | 400, 800, 1200, 1600, 2000 | 20, 50, 100, 150, 200 million toman |
| final | 0 | a wager |

`difficulty` tracks the rung 1:1 — single 200 = `CASUAL`; single 400/600 and double
400/800 = `STANDARD`; single 800, double 1200/1600 = `SCHOLAR`; single 1000, double
2000, final = `INSUFFERABLE`. Do not invent a difficulty.

**But the rung is a claim about difficulty that nothing else in the file makes true.**
Measured: the bank's clues are the same length at every rung — median ~165 characters at
the 200 and at the Final alike — so size carries no signal, and `difficulty` is only the
rung written out. What the rung promises, the clue has to deliver. A 200 may be answered
by anyone who knows the subject exists. A 1000, a double 2000 or a Final must need a
**second, specific thing** the first fact does not hand over — the date, the other actor,
the consequence, who was behind the office. Sort your batch by rung before you hand back
and read each clue as "could someone who has read this subject answer this?" A 1000 that
reads like a 200 is the defect this page exists to name, and no script will catch it for
you.

## 4. How many, and in what units

A full game deals **six categories per round**, and a dealt category is spent — single
and double cannot share one. So a playable board needs:

> **six complete single categories + six complete double categories = 60 clues**,
> plus at least three `final` rows.

Sixty is exactly one game, so every match deals the same board. Aim for **nine or more
complete categories per round** (~95 clues) for variety.

**A category is five clues — one at every rung of its round — or it is discarded.**
The board builder keeps a category only if every rung is present. One gap and the whole
category silently vanishes; the board just comes up short. The `category` string must
be **byte-identical across its five clues** — that string is the join key, and a stray
space forks it into two dead halves.

## 5. Every clue, checked

- exactly **four** `options`
- `options[correct_option_index]` **is** the canonical answer
- put that index at **0** and leave it. The engine reshuffles the options when it deals
  (`shufflingOptions`, `Web/app.js:274`), so every one of the bank's 1,000 rows stores 0
  and the balance is produced at runtime, not by you. Do not try to spread it yourself.
- the **answer must not appear in the clue text**. This is the one giveaway a machine can
  catch, and it is what "captain obvious" usually means. Ten distinct clues in the shipped
  1,000 fail it (thirteen rows — three carry `_encore` twins): `war_koveitipour_800`,
  `coldwar_cento_2000`, `single_philosophy_of_isfahan_the_metaphysicians_800`,
  `double_the_sultan_of_soltaniyeh_2000_a`, and six more. Check your own batch for it
  before you hand back.
- `accepted_aliases` non-empty; for Persian names carry both scripts
- wrong options are not filler: each shares the era, office, or arena of the right
  answer, and each comes with a stated reason it is plausible and a reason it is wrong
- a `theme` keyword (archive only) chosen for which grey Persian subtitle it should land
  under, not for how it reads — §5 of `QUESTION_AUTHORING.md` lists the buckets and the
  three substring traps
- provenance for every row: title, author, page, and the passage it came from
- **a `_b` row is a second question, not a copy of its `_a` twin.** The `_a`/`_b` suffix
  marks two *different* questions dealt from one rung — the slot exists for replay
  variety. A `_b` row carrying the `_a` row's clue and answer while carrying its own alias
  list is the worst kind of broken: the board shows a windcatcher clue that accepts
  "yakhchal", and a player is judged **right** for the wrong answer. If you write or
  translate the Persian bank, the Persian row carries **its own** question — never the
  `_a` twin's text, and never the English left untranslated.

**Category titles are puns.** Roughly a hundred jokes, not descriptions. A dry title is
a defect. The Persian category is the same joke written natively in Persian — never a
translation of the English one.

## 6. The host has no name, and he is not nice

He is smug, snarky and mean, identically in both languages. His comedy aims at the
contestant and at Iranian social habits — the confident uncle, the dinner-party fact,
the family WhatsApp group, the Tehran taxi driver who knows everything. Praise is
grudging and backhanded. One short dry sentence each: not "Great job!", more like
"Unfortunately you're right."

**Do not reproduce the shipped formula.** 893 of the existing 1,000 correct lines end in
one of three tails ("Spot on!", "The history holds!", "Quite right."). Write each line
fresh, then check the tails of your batch before handing it back.

## 7. Check yourself before you hand back

The machine checks are `Tools/check_bank.py` (a play file's contents) and
`Course/check_edition.py` (whether a course can fill a full board, and whether its banks
carry the right globals). Run both and read the exit code; do not eyeball. What neither
can check is the judgement:

1. Parse your own output. Valid JSON, unique `id`s, the two languages mirroring id for
   id.
2. Count complete categories per round — six minimum, nine better.
3. Confirm every category has all five rungs and one byte-identical title string.
4. Confirm `options[correct]` equals the answer on every row. The index stays **0** on
   every row — do **not** spread it across the four positions (§5); the engine reshuffles
   at deal time and re-finds the answer by its text.
5. Read your host lines back-to-back and count how many end the same way.
6. **Report the counts.** "55 clues, 7 single categories, 4 double, 2 finals, 12 host
   lines ending in three tails" is a handoff. "Done" is not.

You are the author, not the auditor — do not build a validation layer, do not
self-audit into a second document, do not silently top a bank up from another bank. If
something does not add up to a playable board, that is the honest result: say so.

## 8. Where things live

```
Jeopardy - Iranian Edition/          ← the one directory
├── Sources/                         ← corpora, gitignored, never committed
│   ├── MAIN CORPUS/                 ← books 1–7: what MAIN was written from
│   └── COURSES/IR4595 Iran in World Politics/
├── QuestionBank/                    ← MAIN's archive (canonical)
├── Web/                             ← the game, and the only thing that ships
│   ├── data/clues.js                ← MAIN's play bank, generated
│   └── courses/<course-id>/         ← one course per folder: its two banks, skin, art
├── Course/                          ← the authoring lab — nothing here ships
│   ├── BANK_SPEC.md                 ← the course contract
│   ├── course-template/             ← copy this to start a course
│   └── banks/                       ← banks that have not been wired in yet
├── QUESTION_AUTHORING.md            ← the long-form contract
└── CORPUS_BRIEF.md                  ← this page
```

`Sources/` is ~1.1 GB of copyrighted books, and each course keeps its marked-up syllabus
booklet beside its bank. Both are gitignored and **stay that way** — cite titles and
authors freely, never commit the books, the booklets, or long verbatim passages.
`Course/` is not ignored: the lab, its template and its banks belong in the repo, because
a course is built by writing into `Web/courses/`, and the lab is how the next one gets
written.
