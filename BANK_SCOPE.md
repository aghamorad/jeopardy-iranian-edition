# Bank scope — what may go in which bank

The rule, in two halves:

> **Every question ever designed belongs in Jeopardy: Iranian Edition.**
> **A course bank holds only questions written for that course.**

Morad's own words for it: *"one is the MAIN EDITION of the game, the one with the full
corpus using everything; the others are under COURSES editions."* MAIN is the umbrella,
not a sibling of the course banks, and the course banks are locked against it. The code's
word for the main edition is `general`.

That is one rule, not two, because the flow is one-way.

| | MAIN | a course |
|---|---|---|
| what it is | the umbrella — everything the game knows | one syllabus, and nothing else |
| canonical source | `QuestionBank/verified_clues.json` (+ `verified_clues_fa.json`) | `Web/courses/<course-id>/data/bank-en.js` (+ `bank-fa.js`), written by hand |
| what the engine loads | `Web/data/clues.js` (`window.CLUES`), **generated** from the archive | `window.COURSE_CLUES_<ID>` / `..._FA`, written by hand |
| id shape | subject-led: `qajar_amir_kabir_200` | `course_single_1_200` |
| the contract | `QUESTION_AUTHORING.md` | `Course/BANK_SPEC.md` |
| who edits it | Morad, with C3PO | Morad, with C3PO, or an agent he points at a syllabus |

Where each is written is decided by the naming rule: the course folder under
`Web/courses/` is the id, the `?ed=` value, and the stem of both its bank globals. A
course bank that names `window.CLUES` is the one defect this whole page exists to
prevent — it does not fail, it deals the course's questions to the main game.

## Upward: a course's bank joins MAIN, whole

**MAIN absorbs a course's question bank; courses remain contained.** That is the whole
rule, and it is a hard one — not a filter, not a shortlist, not a per-clue judgement.
When a course's bank is promoted, all of it goes up, the journal-article questions and the
single-article figures included. Nothing is held back for being too narrow, because "too
narrow for MAIN" was an earlier version of this rule and it was the wrong one: it made a
straight copy-up into an eligibility argument, twice, and had to be unwound twice.

This holds for **every** course, the ones that ship and the ones not written yet. There
is no whitelist of courses cleared for promotion and no per-course decision to make when
one is added — a course is promotable in the same way it is playable, by existing. Adding
a course adds a bank MAIN will absorb.

The move is a **conversion, not a re-authoring**. `Tools/promote_course_bank.py` reads the
course's own play bank (`Web/courses/<course-id>/data/bank-en.js` and `bank-fa.js`,
`window.COURSE_CLUES_<ID>`) **read-only** and appends MAIN's 27-field archive rows. Clue
text, answers, options, explanations and host lines are copied, never rewritten; the
mechanical part is renames, an option rotation so the answer sits at index 0, and a
slugged `source_id`. A course's file is an input and is never written to — the one-way
rule is enforced by what this tool opens for writing, which is MAIN's archive and nothing
else.

Two archive fields have no counterpart in a course bank and are **not** derivable: the
quoting `supporting_passage` behind the clue, and the three `distractor_rationales`. Both
are archive-only — `render_bank.py` ships `passage`, nothing in `Web/` reads either — so a
player sees no difference. They land empty and the row is marked
`editorial_validation_status: "promoted"` rather than `"verified"`. The gates require both
fields on verified rows and **count** the promoted ones instead, printing how many are
still owed, so the debt stays visible rather than being papered over with invented
evidence. `historical_period` takes the single value `Contemporary Iran` for the same
reason: a true coarse label beats 141 invented precise ones.

That marker is the only place promotion is recorded, and it is what lets the tools tell a
promoted row from one of MAIN's own — the play file does not carry it, so a rule that has
to make the distinction asks the archive (`Tools/check_bank.py` does exactly this, keyed by
file path). After IR4595 the count reads `{"verified": 1000, "promoted": 693}`, and the
promotion's own gate is `Tools/promote_course_bank.py --check`: it rebuilds the 693 rows
from the course and fails if the archive no longer carries one of them unchanged.

### The course's readings come with it

A promoted clue cites the reading it came from, and the citation line is what makes an
answer checkable. That reading is a journal article or a chapter off the course's own
syllabus, sitting in `Sources/COURSES/` and not in `Sources/MAIN CORPUS/`, so promoting a
course's clues **brings that course's readings onto MAIN's shelf in the same movement** —
`Web/data/readings.js` (`window.READINGS_GENERAL`), the list the main edition shows.

MAIN's shelf is *generated*, not authored: `Tools/make_readings.py` writes it out of
`Corpus/Metadata/corpus_manifest.json`, and the file's own header says not to edit it by
hand. A course's shelf is the other way round — the course corpus ships no manifest, so
`Web/courses/<course-id>/data/readings.js` is authored by hand. Putting a course's
readings on MAIN's shelf therefore means **teaching the generator to read a course's
list**, and changing `Tools/make_readings.py` in the same commit as the readings — never
pasting rows into `Web/data/readings.js`, which the next run erases.

How it lands: `Tools/make_readings.py` gained a `COURSE_SHELVES` registry — one line per
absorbed course, `(file, how many readings)` — and appends that course's groups after the
seven corpus headings, reproduced verbatim with their own headings, their own `article` /
`chapter` chips and their `src` PDFs, none of it run through the corpus's `row()`. Adding
a course adds a line to that tuple and nothing else. The count in the registry is asserted,
not trusted, and `Tools/check_readings.py` independently asserts the shelf's total, so a
course shelf that quietly loses a row is a loud failure in two places.

One thing to get right, because it was written down wrong first: **the shelf is the corpus
behind the bank, not the handful of sources a given board happens to cite.** MAIN's own
forty-nine sources sit in `Sources/MAIN CORPUS/`, and the absorbed course's forty-two come
with it, which is why the shelf reads 91 and not 49. It is therefore *not* a
checker-enforced promise that every citation resolves, and it must not be described as
one. Measured 2026-09-15: 31 of MAIN's 32 cited works are on it, and the exception,
`Guardians of the Revolution` (Ray Takeyh), is cited on a row whose PDF is not on disk
anywhere under `Sources/`. That gap predates this rule. The shelf's job is that a player
who wants to look a source up can find it, which is exactly why a promoted clue's source
belongs on it.

The count is asserted in `Tools/check_readings.py` — **91 for MAIN, 42 for IR4595**. It
moves in the same commit as the readings, and the move is said out loud rather than
absorbed. The course's own file is 42 before and after: absorbing is one-way, and nothing
on this side ever writes to it.

Nothing here happens by itself. A course bank does not sync into MAIN, and the build does
not go looking for one — the promotion is a run of `Tools/promote_course_bank.py` and the
shelf follows it only because a line was added to `COURSE_SHELVES`. What is automatic is
that once registered, the shelf is rebuilt from the course's own file on every run rather
than hand-copied, so the two cannot drift.

## Downward: nothing. Ever.

MAIN is not a reserve a short course bank may draw on. Two mechanical reasons, either of
which is enough:

- **The category has to be a taught week.** A course board's categories are matched
  against the ten taught weeks, and a category outside them gets no introduction, no
  theme, and no place on the syllabus the class was examined on. A comprehensive
  MAIN clue tested the class on something nobody taught them.
- **The banks do not share a shape.** A MAIN clue has a subject-led id, MAIN's `theme`
  vocabulary and engine host lines. It is not a row that can be moved.

The course bank's whole purpose is that everything on its board came from the syllabus
and the readings. One borrowed clue costs that, and the person who notices is the class.

## For an agent working a syllabus

This is the operative half. If you are writing a course's bank from a syllabus — the
prompt in `Course/BANK_SPEC.md` is written for exactly this — then:

1. You write **two files and nothing else**, inside the course's own folder:
   `Web/courses/<course-id>/data/bank-en.js` and `data/bank-fa.js`. Never a file named
   `clues.js`, and never `Web/data/`.
2. Your global is `window.COURSE_CLUES_<ID>` (and `..._FA`), where `<ID>` is the course
   folder in upper snake case. `window.CLUES` is MAIN's bank and is not yours to write.
   A bank that assigns `window.CLUES` leaves the *general* edition playing course
   questions, with no error anywhere.
3. You do not read MAIN, write MAIN, or lift a MAIN clue into yours to make up the 60 a
   game needs. If your syllabus does not yield sixty, say so and stop; a board that deals
   short is the honest failure.
4. Questions in MAIN that are also on your syllabus are fine, and expected. Write your
   own version from the syllabus. Do not copy MAIN's wording.

You may only ever touch the bank for the course you were given. Editing one syllabus
gives you no authority over another course, and none at all over MAIN.

## Why this is written down rather than enforced

The asymmetry is the point. The **upward** direction leaves a machine record:
`Tools/promote_course_bank.py` stamps every row it writes with
`editorial_validation_status: "promoted"`, which is why the gates can tell an absorbed row
from one of MAIN's own and count the rationales and passages still owed on it. The
**downward** direction leaves none. `Course/check_edition.py` checks a course bank for
shape, for the naming rule and for the sixty-clue board floor, and it cannot check
provenance: nothing in a course file says which bank a clue was borrowed from. Whether a
course clue was written from the syllabus or lifted from the umbrella is a decision made
while authoring, so it lives in these documents instead of in the build.

The same rule, stated for MAIN, is at `QUESTION_AUTHORING.md` § 13; the course-side
statement is in `Course/BANK_SPEC.md`; and the one-paragraph version an agent is handed is
in `AGENTS.md` § 2. All four are meant to agree. If you change one, change the others.
