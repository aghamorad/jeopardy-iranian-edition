# Question authoring

How a clue gets made, so the next person — or the next agent — does not re-derive it.
Read this before touching either bank. `ARCHITECTURE.md` describes the engine;
`GAME_RULES.md` describes play; this describes authorship.

---

## 1. There are two shapes, not one

Two files hold clues, and their **field names do not match**. Renaming a field for
consistency lands silently in the wrong file.

| | `QuestionBank/verified_clues.json` (+ `_fa`) | `Web/data/clues.js` (`window.CLUES`) |
|---|---|---|
| what it is | the **source bank** — canonical, the thing you edit | the **play file**, what the engine loads — *generated* from the source bank |
| rows | 1000 English, 1000 Persian | 1000, current language only |
| language | a `language` field, one language per row | no field — one file per language |
| question | `clue_text` | `clue` |
| answer | `canonical_answer` | `answer` |
| aliases | `accepted_aliases` | `aliases` |
| correct index | `correct_option_index` | `correct` |
| source | `book_title`, `chapter`, `supporting_passage` | `book`, `page`, `passage` (`chapter` has no play counterpart) |
| host lines | `host_reactions` (a dict — see below) | `correctLine`, `wrongLine` (strings) |

**The source bank is canonical; the play file is generated from it.** This is a
one-way street, and it decides every question about which file to touch.

The generator is `Tools/append_flawless_engine.py` (its siblings
`build_flawless_1000_bank.py`, `generate_flawless_persian_bank.py`,
`append_persian_overhaul.py`, `fix_options_and_align_answers.py` do the same job for
other passes). It reads the archive row by row and writes the play file through a fixed
mapping — nothing is translated by judgement, so the two files cannot disagree:

| archive | → | play file |
|---|---|---|
| `clue_text` | → | `clue` |
| `canonical_answer` | → | `answer` |
| `accepted_aliases` | → | `aliases` |
| `correct_option_index` | → | `correct` |
| `book_title` | → | `book` |
| `historical_period` | → | `period` |
| `supporting_passage` | → | `passage` |
| `host_reactions.correct_generic` | → | `correctLine` |
| `host_reactions.wrong_generic` | → | `wrongLine` |

`id`, `round`, `value`, `category`, `theme`, `difficulty`, `options`, `explanation`,
`author` and `page` pass through untouched. Verified 2026-09-14: every one of those
fields is byte-identical between the archive and the shipped play files, for **all 1,000
English and all 1,000 Persian rows** — 33 checks per row, zero mismatches.

So: **write the archive, then regenerate.** A clue typed into the play file by hand
disappears the next time anyone runs the generator, and a clue added only to the archive
does not play until it is regenerated.

Validation runs the other way round and is lopsided. `Tools/validate_1000_clues.py`
and `Tools/validate_persian_bank.py` check the **archive** properly, and the archive
validator passes today (1,000 clues, 120 categories, four options each, schema and
citations intact). **Nothing checks the play file's contents** — see §11.

### `host_reactions` is not what the player hears

The source bank carries a flat `host_reactions` dict — `correct_generic`,
`wrong_generic`, `common_wrong_answers`, `specificity_prompt`, `explanation` — with no
`en`/`fa` nesting. **Nothing in `Web/` reads it.** The lines that actually play are the
strings `correctLine` / `wrongLine` in the play file — which the generator copies out of
`correct_generic` / `wrong_generic`. So **write those two keys in the archive**; editing
`correctLine` in the play file is editing a file that gets overwritten.

Note the name collision: `host_reactions.explanation` is a host aside, while the
`explanation` the player sees is the **row-level** `explanation`. Only the row-level one
is copied through.

Measured 2026-09-14, so nobody has to guess again:

| field | populated |
|---|---|
| `correct_generic` | 1000 / 1000 |
| `wrong_generic` | 1000 / 1000 |
| `explanation` | 1000 / 1000 |
| `common_wrong_answers` | 92 / 1000 |
| `specificity_prompt` | 2 / 1000 |

---

## 2. `value` is a rung, not money

`value` is the engine's slot key. The stake the player sees is generated at runtime by
`buildBoard`, which then **overwrites `clue.value`** with the toman figure so tile and
score agree. Never write the toman number into the data, and never describe `value` as
dollars.

| round | `value` must be one of | the tile prints |
|---|---|---|
| single | 200, 400, 600, 800, 1000 | 10, 25, 50, 100, 200 million toman |
| double | 400, 800, 1200, 1600, 2000 | 20, 50, 100, 150, 200 million toman |
| final | 0 | a wager |

The Double ladder is **not** a clean doubling. That is deliberate, and the Swift side
agrees exactly (`GameEngine/BoardBuilder/BoardBuilder.swift`), so it is not a bug to fix.

---

## 3. `difficulty` tracks the rung, 1:1

Not a judgement call — verified across all 1,000 rows, every `(round, value)` pair maps
to exactly one label:

| rung | label |
|---|---|
| single 200 | `CASUAL` |
| single 400, single 600, double 400, double 800 | `STANDARD` |
| single 800, double 1200, double 1600 | `SCHOLAR` |
| single 1000, double 2000, final 0 | `INSUFFERABLE` |

---

## 4. Categories

**A category's title is a pun.** Real Jeopardy convention, and the house style here — the
bank's categories are roughly a hundred jokes, not descriptions (`WE DON'T COTTON TO
CONCESSIONS`, `MOSSAD-EGH IN THE MIDDLE`, `OPERATION AJAX & CLEANSER`). A dry title is a
defect. The Persian category is the same joke written natively in Persian, never a
translation of the English one.

**All five rungs or the category is discarded.** `buildBoard` keeps a category only if it
carries a clue at *every* rung of its round (`bank.every(...)`). One gap and the category
silently vanishes — no error, no warning, the board just comes up short.

**Quantities.** A full game deals six categories per round, and a dealt category is
**spent** — the single and double rounds cannot share one. So a complete board needs:

> six complete single categories + six complete double categories = **60 clues**, plus at
> least three finals.

Sixty is exactly one game, so every match deals the same board. For variety, aim for
**nine or more complete categories per round** (~95 clues). There is no upper limit.

**The `category` string must be byte-identical across its five clues** — that string is
the join key. A stray space forks the category into two incomplete ones, and both die.

---

## 5. `theme` is an English keyword, not a display string

`theme` never reaches a player as written. Its only consumer is `persianSubtitle()` in
`Web/app.js`, which builds a haystack from **the category string plus the first clue's
`theme`**, lowercase, and returns the first match against `PERSIAN_BUCKETS` — the six grey
Persian subtitles printed under a category header. No match falls to `متفرقه`.

| bucket | matches on |
|---|---|
| مردم و چهرهها | `trailblazer`, `hero`, `figure`, `royal`, `pioneer`, `coronation`, `monarchy`… |
| مکانها و جغرافیا | `geograph`, `city`, `mountain`, `gulf`, `capital`, `monument`, `island`… |
| تاریخ و انقلابها | `war`, `empire`, `coup`, `revolt`, `revolution`, `reform`, `siege`… |
| فرهنگ و هنر | `poet`, `cinema`, `music`, `art`, `religion`, `science`, `architecture`… |
| سیاست و جامعه | `politic`, `oil`, `press`, `law`, `econom`, `party`, `diploma`, `spy`… |

**The match is a substring test, in bucket order**, which creates three traps:

- `party` matches **`art`** in فرهنگ و هنر before it ever reaches the politics bucket.
- `city` matches inside **`ethnicity`**, landing an ethnic topic in geography.
- `oil` matches inside **`boiling`** or **`turmoil`**.

So a theme is chosen for which bucket it should land in, not for how well it reads.
Genuine coverage gaps — a clue about minorities, ethnicity, gender or the diaspora tends
to fall through to `متفرقه`. Those are the places to reach for a keyword that exists.

---

## 6. Distractors

Exactly four `options`; `options[correct]` must equal `answer`. Wrong options are not
filler — each shares the era, office, or arena of the right answer, and each carries a
stated reason it is plausible and a reason it is wrong (`distractor_rationales` in the
source bank). Vary which index is correct; never park the answer at 0.

---

## 7. Answers and aliases

`answer` is the canonical historical name. `aliases` is every spelling, title, honorific
and transliteration a contestant might reasonably type, and **it must never be empty** —
an empty list means only a byte-exact answer is accepted, which fails real players. For
Persian names carry both scripts. The judge is tolerant but literal; it does not guess.

---

## 8. The host

**He has no name.** Nothing in this project names him; he is the host, مجری in Persian.
Do not invent one.

He is **smug, snarky and mean**, and that register is identical in both languages — the
Persian is the same sneer written natively, not a translation. His comedy is aimed at the
contestant and at Iranian social habits: the confident uncle, the dinner-party fact, the
family WhatsApp group, the Tehran taxi driver who knows everything. Praise is grudging
and backhanded; a correction is rude and never a history lecture. He does not sound like a
warm erudite broadcaster, and archival flourishes ("a misreading of the archives") are
not him.

`correctLine` / `wrongLine`: one short sentence each, dry, a little cruel. Not
"Great job!" — more like "Unfortunately you're right."

### The shipped lines have a formula problem — do not reproduce it

Measured 2026-09-14 in the **archive's** `host_reactions.correct_generic`, which is where
the lines are actually written: **893 of 1,000 end in one of three tails** — "Spot on!"
(340), "The history holds!" (325), "Quite right." (228). Only 107 break the pattern. The
play file carries them through unchanged, because the generator copies the string. Three
lines also carry a doubled period where an abbreviation meets the tail ("Kermit Roosevelt
Jr.. The history holds!"). And `wrong_generic` holds only **665 distinct lines across
1,000 rows** — the rest are repeats.

The generator is not innocent here: its fallback templates, for rows with no
`correct_generic`, are `f"{answer}. Quite right."` and `f"No, that was {answer}."` — the
same habit, written into the tool. So the formula is not the host's voice and not even an
accident of one batch; it is baked into both the archive and the pipeline. Write each line
fresh, and check the tails of a batch before shipping it.

---

## 9. Both languages, always

English bank for English mode, Persian bank for Persian mode — never mixed. `i18n.js`
holds no clue text and `app.js` selects a bank by language; a bank that ships one language
plays under the other language's chrome with no error. Persian must be real Persian, not
transliteration, and the two banks mirror each other id for id.

---

## 10. Provenance

Every clue carries the book, author and page it came from, and the passage it was pulled
out of. `Sources/` — roughly sixty copyrighted books — is **gitignored and stays that
way**; it cannot be redistributed and several files sit near GitHub's size limit. Cite
titles and authors freely; never commit the books or long verbatim passages.

---

## 11. Writing a clue in — the mechanics

**Edit the archive, then regenerate the play file.** That is the whole procedure; the rest
of this section is how not to break the archive while doing it.

Both files are **one enormous single line**, and this is where a careless edit does real
damage.

- `QuestionBank/verified_clues.json` is a plain JSON array — this is the one you write to,
  for both languages, one language per row in its `language` field. `Web/data/clues.js` is
  literally `window.CLUES=[{...},{...},…];` followed by a newline; `clues_fa.js` is the
  same with `CLUES_FA`.
- **Append to the array; do not re-serialise the file.** A round-trip through a
  pretty-printer rewrites all 1,000 rows and buries the actual change. (A round-trip
  through `json.loads` fails outright on a play file, because of the `window.CLUES=` prefix
  and trailing `;`. To read one, use
  `json.JSONDecoder().raw_decode(text, text.index('['))`, or just read the archive.)
- **`grep -c` lies here.** The file is one line, so a count of `1` means "present", not
  "one occurrence". Parse in Python when the number matters.
- Keep the JSON valid, keep `id` unique, and keep the same `id` across both languages so
  the two banks line up clue for clue.
- **Regenerate, never hand-edit the play file.** Run the generator in §1 after changing the
  archive. A hand edit to `Web/data/clues.js` is overwritten the next time anyone does, and
  a row that exists only in the archive does not play until it is.

### What checks what — and the gap

Two scripts read the play file, but neither looks at its **contents**:

| script | what it does with `Web/data/clues.js` |
|---|---|
| `Tools/verify_flawless_state.py:90` | asserts the `window.CLUES=` prefix and **exactly 1,000 rows**. Its real checks — 120 categories, no English in the Persian bank, the difficulty ladder — all run against the **archive**. |
| `Tools/validate_3000_clues.py:67` | the same two assertions, but against **3,000 rows and 360 categories**. Stale: it describes an older 3,000-clue bank and fails against today's 1,000-clue file. Do not treat it as a gate. |

So the archive is checked properly (`validate_1000_clues.py`, green on 2026-09-14) and the
play file is checked for nothing but a row count — the exact combination that lets a
generator bug ship. Until a play-file checker exists, verify a regenerated batch by hand:
four options, `options[correct]` matches `answer`, `aliases` non-empty, all five rungs
present per category, `theme` present, and the host lines actually differ from each other.
Writing `Tools/validate_play_file.py` is the obvious fix and has been offered, not
authorised.

---

## 12. Who writes what

Morad supplies a syllabus or corpus, **Gemini writes the questions**, and C3PO checks and
builds. Gemini's job is the questions and nothing else — no self-audit pass, no validation
layer. Distractors that are random rather than logically adjacent are a defect, not
padding.

The course-edition contract lives in `Jeopardy - Iran in World Politics Edition/`
`BANK_SPEC.md`, which carries the same rules against a syllabus plus a paste-ready Gemini
prompt. The two documents are meant to agree; if you change one, change the other.
