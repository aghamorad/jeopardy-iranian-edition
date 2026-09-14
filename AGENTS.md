# Working on the clue data

You are here to write or check questions. This page is the order of operations; the
contracts it points at are the detail. Read this, then read the two documents it names
below, and you have everything.

## 1. Which bank are you writing?

There are two kinds, and they never mix. Decide first — the answer changes where you
write, what shape the row is, and who checks it.

|  | **MAIN** (`general`) | a **course** |
|---|---|---|
| what it is | the whole of Iran — everything ever designed, the umbrella | one syllabus, one module, one aspect of the main game |
| you write | `QuestionBank/verified_clues.json` (+ `verified_clues_fa.json`) | `Web/courses/<course-id>/data/bank-en.js` (+ `bank-fa.js`) |
| shape | the **archive** shape — `clue_text`, `canonical_answer`, `accepted_aliases`, `correct_option_index`, `host_reactions` | the **play** shape — `clue`, `answer`, `aliases`, `correct`, `correctLine`, `wrongLine` |
| the contract | `QUESTION_AUTHORING.md` | `Course/BANK_SPEC.md` |
| checked by | `Tools/validate_1000_clues.py`, `Tools/validate_persian_bank.py`, `Tools/verify_flawless_state.py`, `Tools/check_bank.py` | `Course/check_edition.py` + `Tools/check_bank.py` (via `Course/build_edition.sh`) |
| from the shelf | `Sources/MAIN CORPUS/` | `Sources/COURSES/<course>/` |

**Never name a bank `clues.js` and never write `window.CLUES` in a course.** That global
is MAIN's own bank; a course that takes it deals its questions to the main game — with no
error anywhere, at any point, ever. The engine deals a show only the array it registered,
and that separation is the entire mechanism behind the rule below.

## 2. The scope rule

> **Every question may go to MAIN. A course never leaks into another course. MAIN never
> leaks into a course.**

Stated fully in `BANK_SCOPE.md`, which is canonical if anything here disagrees with it.
Two directions, and only one of them is open:

- **A course question may be promoted to MAIN** — but only if it stands on its own, one a
  general player could answer from the same reference books without having sat the course.
  That is a re-authoring into the archive shape, not a copy.
- **A MAIN question never goes into a course.** Not even to fill a board that came up
  short. A borrowed clue also fails mechanically: a course recognises its own categories
  and presents them as its own weeks, so a category it does not recognise is a subject the
  class was never taught.

## 3. How to craft a clue

Read `QUESTION_AUTHORING.md` before writing anything. It carries the value ladders, the
difficulty mapping (which is *not* a judgement call — it tracks the rung exactly), how to
write distractors, what belongs in `aliases`, and the host's register: **smug, snarky,
mean**, in both languages.

`Course/BANK_SPEC.md` is the same rules restated for a course bank, and it is the one
carrying the `theme`-keyword table — the mechanism that decides the small subtitle under a
category header. Read that table before choosing a `theme`; a short keyword fires inside
unrelated words and lands in the wrong bucket.

Two things measured in the live bank that a batch of new lines will otherwise repeat: the
host's `correctLine`s drift into a handful of stock tails, and `options[correct]` should
always be **0** — the engine reshuffles as it deals, so spreading the index by hand
achieves nothing and breaks the two languages' mirror.

## 4. How to grow the bank

**MAIN.** Append to the archive (`QuestionBank/verified_clues.json`), never to the play
file. Then regenerate:

```bash
python3 Tools/render_bank.py
```

`Web/data/clues.js` (`window.CLUES`) is *derived* — `Tools/render_bank.py` writes it from
the archive through a fixed field map, so the two cannot drift. A hand edit to the play
file survives until the next run and then vanishes. `python3 Tools/render_bank.py --check`
reports drift without writing.

**A course.** You write the play shape directly, by hand or through the lab's converter
(`Course/banks/`). There is no archive behind a course bank — which is also why
`Tools/check_bank.py` is its only content gate. Append rows to the array; keep both
languages at parity, same `id`s on both sides.

## 5. How to add a course

Courses are a permanent part of the game, present in every build, and there will be more
of them (§6). A new one is one folder, and the folder name is the whole design:

```
Web/courses/<course-id>/
  course.js          registration, and optionally the course's own words and voice
  course.css         the skin — optional
  data/bank-en.js    window.COURSE_CLUES_<UPPER_SNAKE(course-id)>
  data/bank-fa.js    window.COURSE_CLUES_<UPPER_SNAKE(course-id)>_FA
  assets/            tile, backdrop, audio
```

The naming rule: **the folder name is the `id` is the `?ed=` value**, and the bank globals
are that name in upper snake case. One string in five places — folder, `id`, `?ed=`, the
bank globals, and the `data-edition` attribute in the CSS. Grep the folder name and you
find everything the course owns.

To start one, copy the scaffold and rename:

```bash
cp -R "Course/course-template" "Web/courses/<course-id>"
```

Its placeholder banks already fill a playable board, so the right first move is to copy
the folder, watch it deal, and *then* replace the questions. Read the header of
`Course/course-template/course.js` — it lists the five places the id appears, and the
template's globals are named so that copying it gets the rule right by default.

Last step is wiring, and it is three lines in `Web/index.html`: one `<link>` for the skin
in the head, and two `<script>` tags for the banks plus one for `course.js` at the foot of
the body, in the blocks marked for courses. Nothing in `editions.js` or `app.js` changes —
the registry takes any number of courses in registration order, which is the order the
chooser lists them.

Then gate it:

```bash
./Course/build_edition.sh <course-id>
```

## 6. Where the source material lives

`Sources/` is gitignored (copyrighted books, ~1.1 GB) but it is the shelf every question
is drawn from, and it is split to match the two bank kinds:

```
Sources/
  MAIN CORPUS/   1–7   what MAIN was written from
  COURSES/            <course>/  ...its Week N/ readings
```

A course's shelf folder maps to its bank folder: `Sources/COURSES/<course>/` is where its
questions come from, and `Web/courses/<course-id>/` is where they go.

## 7. What checks what

Run the gate, don't reason about it.

```bash
./Course/build_edition.sh <course-id>
```

That is `Course/check_edition.py` (can it fill a board at all — six complete categories a
round, both languages, ids unique) followed by `Tools/check_bank.py` (what the clues
actually say — a leak, a wrong `options[correct]`, an empty alias list, a `_a`/`_b` pair
that is one question twice, Persian script in the English bank). For MAIN, run
`Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js` and the archive
validators beside it.

A warning is not a pass with a footnote. Read every line the checker prints.
