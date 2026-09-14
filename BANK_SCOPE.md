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

## Upward: a course question may join MAIN

A course question that stands on its own belongs in MAIN as well. It stands on its own
when it is not about the week it was taught in — when a general player could answer it
from the same reference books the rest of the bank came from, without having sat the
course.

Promotion is an authoring act, not a copy. The clue is written into MAIN's shape and
against MAIN's contract (`QUESTION_AUTHORING.md`) like any other clue — into the archive,
which is then regenerated into the play file. Its id names its subject rather than its
week, its `theme` comes from MAIN's vocabulary rather than the course's, and its host
lines are the engine's own `correctLine` / `wrongLine` channel rather than the course's.
A pasted `course_*` row fails quietly, because the two banks have different field names
and different vocabularies throughout. `QUESTION_AUTHORING.md` §1 is where that
difference is set out.

Nothing here is automatic. A course bank does not sync into MAIN, and the build does not
look for one.

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

`Course/check_edition.py` checks a course bank for shape, for the naming rule, and for
the sixty-clue board floor. It cannot check provenance: nothing in the file says which
bank a clue was borrowed from. Whether a clue was written for the course or lifted from
the umbrella is a decision made while authoring, so it lives in these documents instead
of in the build.

The same rule, stated for MAIN, is at `QUESTION_AUTHORING.md` § 13. The course-side
statement is in `Course/BANK_SPEC.md`. All three are meant to agree; if you change one,
change the others.
