# Codex brief — the Qajar course's distinctive art

Repo: `~/Claude/Jeopardy - Iranian Edition`. The product is the web build in `Web/`.

The Qajar course (`courses/qajars/`) is written, banked and wired into the show. What it
does not have is its own art: it is wearing the *placeholder* tile and the *general
edition's* wordmark and backdrop. Generate the three missing pieces below.

**Its bank is not clean** — 512 rows that have never been through MAIN's content gate,
carrying the defects logged in `C3PO_LOG.md` for 2026-09-17. That does not touch this
brief: the art is independent of the clues, and nothing here asks you to read or edit
them.

Read `STYLE_SHEET.md` at the repo root first, and `Web/courses/qajars/course.css` — the
course already has a palette and the new art has to sit inside it.

---

## 1. What a course owns

Every course edition carries exactly **four** art files and no others. Iran in World
Politics is the only complete one; copy its treatment, not its subject matter.

| file | size | Qajar status |
|---|---|---|
| `assets/sprite-<professor>.png` | 89 × 175 RGBA | **done** — `sprite-stephanie.png` |
| `assets/tile-course.png` | 512 × 512 RGB | **placeholder** — wrong art |
| `assets/logo-wordmark-course.png` | 2167 × 726 RGBA | **missing** |
| `assets/stage-backdrop-course.png` | 1536 × 1024 RGB | **missing** |

Paths are `Web/courses/qajars/assets/…`. Do not render a Qajar *sprite* — the professor
sheet has already been through `Tools/make_stephanie_sprite.py` and is final.

**Generate nothing else.** No favicons, no app icons, no `soon-` cards, no pack lockup.

---

## 2. The wordmark — read this section twice

This is the piece the course most needs, and the one with a hard constraint on it.

### The house grammar

The wordmark is the same lockup every time, and only three things change between
editions. Read both existing files before you draw anything:

- `Web/assets/logo-wordmark.png` — the general edition
- `Web/courses/iran-in-world-politics/assets/logo-wordmark-course.png` — the course

The invariant: **`JEOPARDY!`** in the show's heavy letterforms, dark-outlined and
drop-shadowed, over a letterspaced subtitle in Latin caps, each word sitting on its own
dark rounded chip, over a thin tricolour rule.

The three variables:

1. **A letter is the flag-bearer.** One letter of `JEOPARDY!` is replaced by the
   edition's national or period emblem. Both existing editions give that job to the **O**:
   the Islamic Republic's emblem stands in for it, flat red on the general edition and
   polished red metal on the course.
2. **The remaining letters are filled with the subject.** The general edition is plain
   white; the course fills them with brushed grey metal engraved with a world map, and
   stands the Azadi Tower inside the **A**. The fill *is* the thesis of the course.
3. **The subtitle names the edition.** `IRANIAN EDITION` general,
   `IRAN IN WORLD POLITICS EDITION` course — course name, then the word `EDITION`, same
   letterspaced caps, same chips.

### What the Qajars must not wear

**The Islamic Republic's emblem has no place on this course.** It postdates everything on
the Qajar board by half a century and the course is explicitly the dynasty before it. It
must not appear in the lockup, in a chip, or as a watermark.

The same goes for the tricolour rule beneath the subtitle: the Iranian tricolour was only
fixed in the last decade of the dynasty. Either drop the rule, or re-tone it to this
course's palette — a **lapis / cream / rose-madder** stack, not green/white/red. Those two
hues are the course's, declared at the top of `courses/qajars/course.css`:
`--green: #2f57b4` (lapis) and `--red: #ad2447` (rose madder).

**No warm metal anywhere.** Coppers and golds were tried on the Iran course and rejected —
copper reads as gold, and gold lands next to the retired brown-and-gold design this
project threw out. Cool metals, stone, tile, or paint only.

### What it should wear — the lead

The period-correct analogue of the emblem-in-the-O is the **Lion and Sun** (شیر و خورشید)
— the Qajar state's own national device, the thing on the flag and the coinage of the
exact years this course covers. Put it in the O and the sentence "one letter is the
flag-bearer" stays true while the whole Islamic-Republic reading disappears.

Then give the other letters a Qajar fill and a subject element standing inside one of
them, exactly as the Tower stands inside the course's A. The course is eight taught weeks
on a dynasty that lost every argument with the nineteenth century; its material is the
tile, the qanat, the cossack, the concession, the printing press. Pick the element that
carries the *course*, not the most famous Qajar object — and pick it from the syllabus in
`Jeopardy - Courses - Sources/Qajars (Trinity 2016)/`, not from general Qajariana.

Subtitle: **`THE QAJARS EDITION`**.

### Technical

- 2167 × 726, transparent ground, or 2171 × 724 to match the general edition. The DOM
  places this image in six sizes via the `logo-*` classes; keep the same baseline and
  safe area as the two existing files so nothing reflows.
- The file is Latin-only. Both language editions show the same image; the Persian is
  handled by the DOM. Do not render Persian text into it.
- PNG, RGBA, under ~1.6 MB.

---

## 3. The tile and the backdrop

**`tile-course.png` — 512 × 512 RGB.** Currently the placeholder: byte-identical to
`Web/assets/soon-qajars.png`, a qālyān. Replace it with a real portrait-format course
tile in the treatment of `courses/iran-in-world-politics/assets/tile-course.png` — one
subject, strong silhouette, readable at 86 px on the front door, no text baked in.

**`stage-backdrop-course.png` — 1536 × 1024 RGB.** The board and the title card sit on
this. Iran's is a monochrome Tehran skyline at night, dark enough that white type and the
coloured washes survive on top of it. The Qajar one wants the same job done for its own
city and century — but keep it **dark and low-contrast**, because the engine lays
saturated lapis and rose-madder washes over its left and right edges and the backdrop must
not fight them.

---

## 4. Rules that apply to every future course, not just this one

These are house rules. They held for Iran in World Politics, they hold for the Qajars, and
they will hold for the Pahlavis and everything after.

1. **Four art files per course, and the naming is fixed**: `tile-course.png`,
   `logo-wordmark-course.png`, `stage-backdrop-course.png`, `sprite-<professor>.png`.
   The DOM looks for those names; a differently-named file is a 404 and a blank screen.
2. **The wordmark keeps the lockup and changes the emblem, the fill and the subtitle.**
   Every course replaces one letter with its period's own device. The Islamic Republic
   emblem belongs to the general edition and to Iran in World Politics, and to nothing
   else.
3. **The course's palette is declared in its `course.css` and the art obeys it.** Iran is
   green-and-red at night; the Qajars are lapis and rose madder. Do not bring a hue into
   the art that the stylesheet does not have.
4. **One professor, one sprite, keyed to the course.** Dr Stephanie teaches both the
   Qajars and the Pahlavis; each course gets its **own copy** of the sprite under its own
   folder, and each course's host cues are namespaced by course — `stephanie_qajars_*`,
   `stephanie_pahlavis_*`. Never a bare `stephanie_*`. This is why her cues are not
   shared files.
5. **A missing asset is left missing, never pointed at.** A rule that references a file
   which does not exist is a black stage and a blank lockup, which is worse than the
   general edition's art. `courses/qajars/course.css` currently carries no `.stage-bg` and
   no wordmark swap for exactly this reason, and documents both gaps in its header.
6. **Never overwrite another course's art, and never edit a bank.** The clue banks are
   frozen; this brief is about pictures only.

---

## 5. When you have the files

Drop them at the three paths in §1. Then two twelve-line wirings are still needed and are
**not** yours to guess at:

- The wordmark swap lives in `courses/iran-in-world-politics/course.js:196` — the `LOGO`
  constant and `swapWordmark()`. The Qajar equivalent is described in the header comment
  of `courses/qajars/course.js`, which names the exact block to copy and where to call it.
- The backdrop swap is a `.stage-bg` rule keyed to `html[data-edition="qajars"]`.

The Qajar `course.css` is already written and needs no changes from you beyond the
backdrop rule the day the art lands.

Report the three paths and their dimensions. Do not run a build, do not commit, and do not
touch `Web/data/clues.js`, `Web/data/clues_fa.js`, or anything under `QuestionBank/`.
