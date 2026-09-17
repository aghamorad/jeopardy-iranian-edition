# Codex brief — stage the Pahlavis course, and keep it behind the coming-soon door

Repo: `~/Claude/Jeopardy - Iranian Edition`. The product is the web build in `Web/`.

The Pahlavis course is a **course edition that is not written yet**: it has no clue bank,
so it is not an edition and must not become one. What it should be by the end of this job
is *finished in every other respect* — folder, skin, art, cue map, audio — and still
invisible behind the coming-soon circle it already wears on the front door.

Read `CODEX_QAJAR_ART_BRIEF.md` first. Its **§2 (the wordmark)** and **§4 (house rules)**
are the grammar this course also obeys; do not re-derive them, and do not repeat what they
already say. `STYLE_SHEET.md` at the root is the show's contract. `Web/courses/qajars/` is
the worked example of a course — copy its shape, not its subject.

## 1. What is already there, and what is missing

`Web/courses/pahlavis/` today holds:

- `assets/sprite-stephanie.png` — **done and final.** Same professor as the Qajars, her own
  copy under this folder, per house rule 4. Do not re-render it.
- `assets/audio/` — 12 files, staged from the pack: eight of the ten `course_*` slots, two
  `pahlavi_*` stingers, and the two silent host placeholders. Two slots are unfilled and
  the pack cannot fill either — see §5.

Missing:

| piece | path | note |
|---|---|---|
| the skin | `Web/courses/pahlavis/course.css` | does not exist |
| the module | `Web/courses/pahlavis/course.js` | does not exist |
| course tile | `assets/tile-course.png` | missing — the door wears `assets/soon-pahlavis.png` |
| course wordmark | `assets/logo-wordmark-course.png` | missing |
| stage backdrop | `assets/stage-backdrop-course.png` | missing |
| **`course_theme.m4a`** | `assets/audio/` | **absent — the pack carries no lobby loop** |
| **`course_lock_in.m4a`** | `assets/audio/` | **absent — the pack carries no lock-in sting** |

The skeleton for all of it is `Course/course-template/` — `course.js`, `course.css`, and
the `data/` shape. It is the next best thing to the Qajar folder and has been read.

## 2. Do not make it live. This is the part not to get wrong.

The front door already carries a coming-soon circle for the Pahlavis. It is built by the
`SOON_CARDS` array in `Web/app.js:1490` and rendered as a plain `.circle.is-soon` `<div>`
that is not a button and that the pad ring skips. **It stays exactly as it is.** The work
below adds a folder the show never asks for a file from; a course becomes live only when
`Web/index.html` gains its tags, and nothing else does that.

So, in `Web/index.html`:

- **Do not add** `courses/pahlavis/data/bank-en.js`, `-fa.js`, or `courses/pahlavis/course.js`.
- **Do not add** the `courses/pahlavis/course.css` stylesheet link.
- **Do not touch** `SOON_CARDS`, `soon-pahlavis.png`, or `front.soonPahlavi` in `i18n.js`.

And in the folder:

- **Do not create `Web/courses/pahlavis/data/` at all**, not even empty bank files.
  `window.registerEdition` in `Web/editions.js` refuses an edition whose `banks` array is
  empty or missing, and a stub bank is one careless script tag away from a course that
  loads and cannot deal a board. The clue bank is not your lane in any case — it is being
  written separately into MAIN's archive, and `GEMINI.md` at the root governs that work.

Net effect, and the thing you are aiming at: the Qajar course is how a *live* course looks;
this one should be complete to the same depth and still not on the door.

## 3. The art

Three files, at the fixed names and sizes in `CODEX_QAJAR_ART_BRIEF.md` §1, into
`Web/courses/pahlavis/assets/`. The lockup grammar from §2 applies unchanged — heavy
`JEOPARDY!`, one letter carrying the edition's device, the rest filled with the course's
own thesis, a letterspaced subtitle on chips, Latin only, RGBA, under ~1.6 MB.

What differs is the three variables. **These are a lead, not a specification** — you may
propose against it, but say so rather than quietly departing:

1. **The subtitle is `THE PAHLAVIS EDITION`.**
2. **The flag-bearer letter is the O, and the device is the Lion and Sun *surmounted by the
   imperial crown*** — the Pahlavi state's own device, the thing on the flag and the coat of
   arms of the exact years this course covers. The Qajars take the uncrowned Lion and Sun for
   their O; the crown is what separates the two readings, keeps the house grammar constant
   (one letter is the flag-bearer, and it is the O in every edition), and puts the correct
   century on the card. **The Islamic Republic's emblem is banned here too**, for the
   different reason that this course ends in 1979.
3. **The fill and the subject element.** The course is Iranian history from 1905 to 1979 —
   the constitutional revolution, oil, the coup, the White Revolution, the shah. Give the
   remaining letters a fill drawn from that century, and stand the course's own element
   inside one letter the way Iran in World Politics stands the Azadi Tower inside its A.
   The lead is **the derrick**: it is already this course's mark on the front door, from
   week four of the syllabus, and putting it in the lockup makes the door and the wordmark
   agree. Pick from the syllabus, not from Pahlavi-era furniture — the crown is the one
   exception, and it is there as the *device*, not as decor.
4. **No warm metal** — house rule, twice enforced. Coppers and golds read as the retired
   brown-and-gold.

**The tile and the backdrop.** `tile-course.png` is 512 × 512 RGB: one subject, strong
silhouette, readable at 86 px, no text baked in. `stage-backdrop-course.png` is 1536 × 1024
RGB, dark and low-contrast, because the engine lays the course's saturated washes over its
left and right edges and the backdrop must not fight them.

**The tile is also a decision you do not make.** The front door keeps wearing
`soon-pahlavis.png` — the derrick — until the course goes live, so the new tile will not be
seen by anyone yet. Produce it; leave the door alone.

## 4. The palette, and why it comes first

`course.css` does not exist, and house rule 3 says the art obeys the palette the course
declares. So **write the palette first**, before any art file, and keep every image inside
it. Read `Web/courses/qajars/course.css` for the shape: the palette block is very nearly the
whole skin, and the engine's two hue variables keep their engine names — `--green` means
"the right hue" and `--red` means "the wrong hue", and renaming them from a skin is how a
course stops being loadable. Both #2f57b4 and #ad2447 belong to the Qajars; do not reuse
either.

The territory for this course, offered as a lead: **graphite and steel** — a cool, dark,
industrial ground, with two accents that are neither the flag's nor the Qajars' tile
colours. The Pahlavi era's own materials are oil, steel, rail and concrete, and the course's
argument runs through them. The tricolour is *legitimately* period-correct for this course
in a way it is not for the Qajars — but it is also what MAIN already wears, so if you reach
for it, the treatment has to be what distinguishes it, not the hue. Propose the hexes and
report them; the palette is the course's identity and is the one part of this job that is
expected to come back for a ruling before the art is drawn on top of it.

## 5. The skin, the module, and the audio

- **`course.js`** — model it on `Web/courses/qajars/course.js`, which is the worked example.
  Its header comments name the two rules you must keep: her cues are namespaced by course
  (`stephanie_pahlavis_*`, never a bare `stephanie_*`), and a cue whose line is written but
  whose clip is not recorded still gets a clip — every host cue maps through `EDITION_SOUND`
  to `host_line_placeholder`/`host_scene_placeholder`. Her voice is a **later, separate job**
  for both courses together; it is not yours, and you are not to fake it.
  The title card's rails come from the real syllabus — see §6 — and nothing in them is
  invented for the game.
- **`course.css`** — the palette, keyed to `html[data-edition="pahlavis"]`, plus the two
  swaps: the `.stage-bg` rule and the wordmark swap. Both are twelve-line blocks already
  correct in `Web/courses/iran-in-world-politics/course.js` (the `LOGO` / `swapWordmark`
  pair at lines 196–212, called at 279) and both are described in the Qajar sheet's header.
  Unlike the Qajars, **you will have the art in hand**, so write them rather than documenting
  the gap — a rule pointing at a file that is not there is a black stage and a blank lockup.
- **Two audio slots are empty, and the pack cannot fill either.** The pack is at
  `~/Desktop/New Courses/Pahlavis/Pahlavi_Jeopardy_Music_Pack`; `Tools/stage_course_audio.py`
  at the root is the tool that puts a pack into the engine's shape (slot names, m4a, 44.1 kHz
  stereo AAC ~128 kbps) and its docstring is the contract. Its `PACKS['pahlavis']` block at
  `Tools/stage_course_audio.py:87` maps eight pack files to eight slots, and the pack holds
  nothing else an engine slot claims. The two it leaves empty:
  - **`course_theme.m4a`** — the menu's music. `01_Pahlavi_Main_Theme_65s.wav` went to
    `course_splash`, which is exactly what the Qajars do with their main theme
    (`Tools/stage_course_audio.py:60`); there is no lobby loop in the pack at all.
  - **`course_lock_in.m4a`** — the buzzed-first lock-in sting. The Qajars get it from
    `03_sfx/02_qajar_buzzed_first_lockin_polished_1s.wav`
    (`Tools/stage_course_audio.py:67`) and both live courses map `armed:` to it
    (`courses/qajars/course.js:476`, `courses/iran-in-world-politics/course.js:742`). The
    Pahlavi pack carries no equivalent.

  Neither is yours to synthesise, and house rule 5 forbids pointing at a file that is not
  there. So write `armed:` against the silent `host_line_placeholder` — the cue gets a clip
  and the lock-in is simply unheard for now — and name both gaps in your report.

## 6. Sources

- **The syllabus** — the course is Dr Stephanie Cronin's *Iranian History from 1905 to 1979*,
  Michaelmas 2016. The PDF is in the Drive folder
  `~/Library/CloudStorage/GoogleDrive-aghamorad2000@gmail.com/My Drive/Jeopardy - Iranian Edition/Jeopardy - Courses - Sources/Pahlavis (Michaelmas 2016)/Pahlavis Syllabus, 2016/`.
  Read it before writing a rail. Its honest shape matters: **weeks 5, 6 and 7 are thin, and
  week 6 is a single article already filed under week 4.** Report that; do not pad it into a
  symmetrical ten.
- **The Drive `GEMINI.md`**, in the same `Jeopardy - Courses - Sources/` folder, is the
  authoring brief for the clue bank that will eventually make this course live. It is not
  your job and you should not write clues, but it is where the course's scope is stated.
- **Do not read or edit any bank** — not `QuestionBank/`, not `Web/data/clues*.js`, not
  `Web/courses/qajars/data/`. The Qajar bank is mid-repair and the MAIN banks are frozen.

## 7. When you are done

Report, and stop:

- the palette hexes and the file that declares them;
- the three art paths with their pixel dimensions;
- the two swap blocks and which files they landed in;
- confirmation that the pack carries neither `course_theme.m4a` nor `course_lock_in.m4a`, and
  which file you pointed `armed:` at;
- the syllabus's thin weeks, as written;
- and confirmation that `Web/index.html` and `SOON_CARDS` are untouched.

Do not run a build, do not start a server, and do not commit or push.
