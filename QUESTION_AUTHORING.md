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

The current serializer is `Tools/render_bank.py`. Run it after archive edits;
`python3 Tools/render_bank.py --check` reports drift without writing. Historical
`append_*` and `build_*` scripts can rebuild archives and other outputs as well;
do not use them as routine serializers. The fixed field map is:

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
citations intact). The play file's contents are checked by `Tools/check_bank.py` — see §11.

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

**The label is derived; the difficulty itself is not.** Measured 2026-09-14: clue length is
flat across the whole bank — median 159–171 characters at *every* `(round, value)` pair,
from single 200 to the Final — so nothing in the data distinguishes an easy clue from a
hard one. The rung is the author's claim and `difficulty` merely transcribes it. The claim
is honoured in the clue's content: the 200 rung may be answerable by anyone who knows the
subject exists, while the 1000, double 2000 and Final rungs must require something the
first fact does not supply. No script checks this, and none can; it is the author's to
check, by sorting a batch by rung and reading it.

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
> least one final.

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
source bank — populated on all 1,000 rows, three entries each, one per wrong option).

**The correct index is 0 on every row, on purpose.** All 1,000 archive rows store
`correct_option_index: 0`, and so does the generated play file; the balance comes from the
engine, which reshuffles each clue's options at deal time — `shufflingOptions`,
`Web/app.js:274`, called from `buildBoard` (1221) and `startFinal` (2313). So this is not a
task for the author. Do not spread the index by hand; it is not a rule the data follows.

Parentheses are never an answer marker. A canonical answer may carry a useful gloss or
abbreviation in parentheses, and a distractor may do the same, but neither role is allowed
to own that punctuation. The web engine neutralises authored parentheses and then gives
each displayed option an independent presentation coin flip. Do not write distractors to
imitate that runtime treatment, and do not infer correctness from punctuation in source data.

**The answer must not appear in the clue text.** The current general-bank checker
reports no such errors in either language (2026-09-14). Earlier counts described
older working-tree content. Check each new batch with `Tools/check_bank.py` (§11).

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
the lines are actually written: **906 of 1,000 end in one of three tails** — "Spot on!"
(353), "The history holds!" (325), "Quite right." (228). Only 94 break the pattern. The
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
out of. `Sources/MAIN CORPUS/` — 48 copyrighted books in seven folders, the shelf this
bank was written from — is **gitignored and stays that way**; it cannot be redistributed
and several files sit near GitHub's size limit. Cite titles and authors freely; never
commit the books or long verbatim passages.

---

## 11. Writing a clue in — the mechanics

**Edit the archive, then regenerate the play file.** That is the whole procedure; the rest
of this section is how not to break the archive while doing it.

Both files are **one enormous single line**, and this is where a careless edit does real
damage.

- `QuestionBank/verified_clues.json` is a plain JSON array — this is the one you write to,
  for English; `QuestionBank/verified_clues_fa.json` holds Persian. Each row
  also carries its `language` field. `Web/data/clues.js` is
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

### What checks what

Three kinds of script read a bank, and they answer different questions.

| script | question it answers | what it reads |
|---|---|---|
| `Tools/validate_1000_clues.py`, `Tools/validate_persian_bank.py` | is the **archive** well-formed? | `QuestionBank/verified_clues.json` — schema, citations, 120 categories, no English in the Persian bank, the difficulty ladder |
| `Tools/verify_flawless_state.py:90` | is the **play file** the right *shape*? | `Web/data/clues.js` — the `window.CLUES=` prefix and exactly 1,000 rows, and nothing else |
| `Tools/check_bank.py` | is the **play file's content** correct? | any play-shaped bank — `Web/data/clues.js`, or a course's `Web/courses/<id>/data/bank-*.js` |

`Tools/validate_3000_clues.py:67` makes the same two shape assertions as
`verify_flawless_state.py`, but against **3,000 rows and 360 categories**. Stale: it
describes an older 3,000-clue bank and fails against today's 1,000-clue file. Do not treat
it as a gate.

**`Tools/check_bank.py` is the play-file content checker** (§11 previously said none
existed — this is the fix). It checks, per row: the four options and
`options[correct] == answer`; non-empty `aliases`; all five rungs present per category with
a byte-identical title; `value` on the round's ladder; `difficulty` matching the rung; the
answer's distinctive words absent from the clue; language purity (no Persian script in the
English bank and vice versa); `id` mirroring between the two languages; that an `_a`/`_b`
pair carries **two** questions rather than one written twice; and — with
`--edition` — which categories reach a professor theme clip. It is also the only thing that
checks the *content* of a **course** bank, which has no archive behind it at all.

```
python3 Tools/check_bank.py Web/data/clues.js \
    --fa Web/data/clues_fa.js
```

Exit status is 1 on any error, 0 otherwise; warnings never fail a run. It is read-only and
stdlib-only. A course bank is checked by pointing it at
`Web/courses/<id>/data/bank-en.js` with `--fa .../bank-fa.js`; passing
`--edition Web/courses/<id>/course.js` adds the category-to-theme-clip check.

What no script can check is **judgement**: whether the 200 rung is genuinely easier than
the 1000 (§3), whether a distractor is adjacent rather than random (§6), and whether the
host lines actually sound like the host (§8). Those stay with the author, read by sorting a
batch by rung and scanning the tails.

---

## 12. Who writes what

Morad supplies a syllabus or corpus, **an agent writes the questions**, and C3PO checks
and builds. The agent's job is the questions and nothing else — no self-audit pass, no
validation layer, no second document. Distractors that are random rather than logically
adjacent are a defect, not padding.

**Which agent does not matter.** There is one brief and any model can be pointed at it:
hand the agent `CORPUS_BRIEF.md` — the one-page contract, which routes to this document
for the detail. Nothing here is written for one vendor, and no step depends on one.

The course contract is `Course/BANK_SPEC.md`, which carries the same rules
against a syllabus plus a paste-ready prompt. The two documents are meant to agree; if
you change one, change the other.

---

## 13. What belongs in MAIN, and what may not

MAIN is the umbrella: every question ever designed, whichever edition it was
written for. A question written for a course joins it when the question stands on its
own — when a general player could answer it from the same reference books as the rest of
the bank, without having sat the course. It joins by being authored into this document's
contract like any other clue, not by being copied across: an id that names a subject
rather than a week, this bank's `theme` vocabulary, this bank's host lines (see §1 and
§5 for why a pasted row fails quietly).

Nothing travels the other way. A course bank holds that course's questions and nothing
else, and a clue from here never enters one to make up the sixty a game needs. The
reasoning, and the rule as it applies to an agent editing a syllabus, is in
`BANK_SCOPE.md`.
