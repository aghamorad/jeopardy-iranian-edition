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
validator passes today (2,205 clues, four options each, schema and citations intact —
373 category slots: 169 single, 164 double, 40 finals). The play file's contents are
checked by `Tools/check_bank.py` — see §11.

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

Not a judgement call — verified across the whole bank, every `(round, value)` pair maps
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

## 5. `theme` is metadata with no display consumer

`theme` never reaches a player. The board prints `category` and nothing else: the six grey
Persian subtitles that used to sit under each category header were removed on 2026-09-18,
and `persianSubtitle()` / `PERSIAN_BUCKETS` with them. The field stays in the bank as a
subject tag for tooling and for sorting a shelf; no screen reads it.

So a theme is a plain English subject — `Royal Marriages`, `Frontline Literature` — chosen
to describe the category. It no longer has to be tuned against a keyword list, and it is no
longer a place to fix a display problem, because there is no display.

---

## 6. Distractors

Exactly four `options`; `options[correct]` must equal `answer`. Wrong options are not
filler — each shares the era, office, or arena of the right answer, and each carries a
stated reason it is plausible and a reason it is wrong (`distractor_rationales` in the
source bank — populated on all 1,000 rows, three entries each, one per wrong option).

**The correct index is 0 on every row, on purpose.** All 1,000 archive rows store
`correct_option_index: 0`, and so does the generated play file; the balance comes from the
engine, which reshuffles each clue's options at deal time — `shufflingOptions`,
`Web/app.js:310`, called from `buildBoard` (1718) and `startFinal` (2888). So this is not a
task for the author. Do not spread the index by hand; it is not a rule the data follows.

Parentheses are never an answer marker. A canonical answer may carry a useful gloss or
abbreviation in parentheses — `National Iranian Oil Company (NIOC)` — and a distractor may
do the same, but the punctuation is presentation, not meaning. The engine strips the
authored gloss off every button before it deals the board (`presentingOption`,
`Web/app.js:297`), so the buttons read `National Iranian Oil Company` while the archive, the
judge, the verdict card and the host's line keep the gloss. Two consequences for the
author. A distractor that is the answer with its gloss removed — the same book shipped once
with its author and once without — is a duplicate the board cannot show, and the engine will
keep the gloss on all four buttons rather than print one text twice, so do not write one.
And do not dress an option up to look official: the dressing does not reach the board.

**No option may be distinguishable by its punctuation.** Parentheses come off, but a dash,
a colon, a semicolon or a trailing qualifier rides through to the button and becomes the
tell instead. That is measured, not hypothetical: flattening glosses to an em-dash left a
live leak for months, because the dash appeared only on the option that had carried the
gloss, and that option is the answer — 196 of the 210 glossed answers were still findable
by "tap the button with the dash". If the answer genuinely needs a qualifier, put it in the
clue text or list it in `accepted_aliases`. Nothing on an option may point at itself.

**The answer must not appear in the clue text.** The current general-bank checker
reports no such errors in either language (2026-09-14). Earlier counts described
older working-tree content. Check each new batch with `Tools/check_bank.py` (§11).

---

## 7. Answers and aliases

`answer` is the canonical historical name. `aliases` is every spelling, title, honorific
and transliteration a contestant might reasonably type, and **it must never be empty** —
an empty list means only a byte-exact answer is accepted, which fails real players. For
Persian names carry both scripts. The judge is tolerant but literal; it does not guess.

An alias belongs to the row that lists it. It must be a spelling, title, honorific or
transliteration **of that row's `answer`** — never a related name picked up from the row
above, from the same source passage, or from the English record the row was translated
from. Measured 2026-09-15: **347** of the 1,000 Persian rows carried an `accepted_aliases`
list sharing no token with their own answer. `reza_coup_200` answers ۳ اسفند ۱۲۹۹ and listed
Reza Khan / Reza Shah / Reza Shah Pahlavi; `bazaar_saffron_600` answers زعفران and listed
Khorasan / Razavi Khorasan. Each of those is a wrong answer the judge accepts in write-in
mode, which costs a player more than a rejected right answer does. The English bank has
zero such rows. (An earlier note said 348; the gate counts 347, and the gate is what
runs.) All 347 were repaired the same day, along with twelve rows that listed one of their
own wrong options as an alias. `Tools/check_bank.py` now fails a bank that reintroduces
either, and `--archive` runs it against the archive directly — read a fresh batch with it
before it ships rather than by eye.

**What that gate cannot catch, and why.** Its floor is `related()`: an alias counts as
belonging if it is the same string, is contained in the answer, or shares one content word
with it. That admits a whole second question when the two entities share a generic head
noun. Measured 2026-09-15, six Persian rows were found doing exactly this — the answer and
the clue had been rewritten to a different question while `accepted_aliases` was left as the
English row's list — and every one of them passes the gate:

| row | answers | listed instead |
|---|---|---|
| `single_sacred_shrines_and_pilgrimage_1000` | مسجد جمکران | Goharshad Mosque / مسجد گوهرشاد |
| `double_the_sacred_defense_battlefields_400` | عملیات کربلای ۵ | Operation Fath ol-Mobin |
| `double_the_sacred_defense_battlefields_800` | عملیات فتح‌المبین | Operation Kheibar |
| `double_the_sacred_defense_battlefields_2000` | عملیات رمضان | Operation Kaman 99 |
| `single_the_trans_iranian_railway_600` | بندر شاهپور | Bandar-e Shah / بندر ترکمن |
| `single_ancient_warfare_empires_at_clash_200` | نبرد گوگمل | Battle of Marathon |

`مسجد` is one shared word; so is `عملیات`, `بندر`, `نبرد`. No token test separates those
from the cases that are correct: `سفارت انگلیس` and `سفارت بریتانیا` are the same embassy and
share only `سفارت`, exactly as `نبرد گوگمل` and `نبرد ماراتن` share only `نبرد`. A rule tight
enough to catch the six would reject the synonyms. So it is a reading rule, not a gate rule:
**when a row's answer and clue are rewritten, rewrite its aliases in the same pass** — the
copy that survives is the copy nobody looks at. All twelve rows (each with its `_encore`
twin) were repaired by hand.

Relatedly, a clue that names one of its own aliases is not a defect: it is the standard
shape where the clue hands over one name and asks for the other — Persepolis / Takht-e
Jamshid, Avicenna / ابن سینا, سردار ملی / ستارخان. There are 47 such rows in English and 45 in
Persian and they are correct. Do not "fix" them.

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

### The tails are the defect this bank keeps producing

Every `correctLine` must be a line written for that row. Measured 2026-09-15 across both
archives: **1,000 of 1,000 distinct, 0 duplicates, 0 stock tails** — after a wave that
rewrote **581 English and 334 Persian base lines**. Before it, 906 of 1,000 English lines
ended in "Spot on!", "The history holds!" or "Quite right.", and 334 Persian lines ended in
"کاملا درسته". The bank is clean now because it was cleaned by hand; it drifts back the
moment a batch is written quickly. Five shapes reproduce it — check for each before
shipping.

**1. The stock tail.** `… Correct.` / `… Spot on!` / `… کاملا درسته`. The generator is not
innocent: its fallback templates, for rows with no `correct_generic`, are
`f"{answer}. Quite right."` and `f"No, that was {answer}."` — the habit is written into the
tool. A line whose last two words could close any other row is not a line.

**2. The flat answer-plus-verdict, which hides behind rule 1.** `<answer>. Correct.` /
`<answer>. Yes.` / `<answer>. Exactly.` — **49 English rows** had this and the tail wave
never saw them, because they carry no *stock* tail and so never matched the search. It is
invisible in a second way too: `Web/app.js:2687` prints the `correctLine` and then, a dozen
lines later, the canonical answer, so a line that is only the answer plus a verdict says
the answer twice and adds nothing. The test is mechanical — strip the trailing verdict and
ask whether what remains is `canonical_answer` or an `accepted_alias`. If it is, write a
real line.

**3. The Persian `تو هم … گفتی.` attractor.** Take this one seriously: it is not an accident
of one writer. Fifty-two of 334 Persian base lines — **15.6%** — ended `تو هم <adverb>
گفتی.`, and **all five writers reached it independently**, in the same wave, on the same
slot. After the `گفتی` endings were removed a further **19** still opened their verdict
clause with the bare `تو هم` hinge. It is a Persian attractor for this slot, not a
coincidence, and it returns every batch unless the contract forbids it by name. Open the
verdict clause with the verb or the noun, never with `تو هم`.

**4. The duplicated tail.** `آفرین، این را از نوارهای قدیمی یاد گرفته‌ای.` shipped on two
rows. Two lines that differ only in their opening are one line. Distinctness is checked
across the whole language, not within a shard.

**5. The praise tail, which hides behind rule 2.** `<answer>. Exceptional scholarship.` /
`<answer>. Outstanding historical knowledge.` / `<answer>. Very impressive.` — the same
defect as rule 2 in a longer coat, and invisible to rule 2 for the same reason rule 2 was
invisible to rule 1: rule 2's test looks for a *single* verdict word, and this verdict is a
phrase — "Outstanding historical knowledge" is not "Outstanding". **Eight English rows** had
it on 2026-09-15, every one of them at the top rung, and none in Persian, where all 319
answer-first lines carried a fact after the name. The shape names the answer and then says
only how clever the contestant is, so the player reads the answer, is told they are
brilliant, and learns nothing. The test is mechanical: strip the answer and every alias out
of the line, and if five words or fewer remain and all of them are praise vocabulary
(`Exceptional`, `knowledge`, `scholarship`, `Masterful`, `Very`, `impressive`), there is no
line there. `Tools/check_bank.py` runs it.

**The house shape — aim at this one.** Name the answer, then pay it off with a fact:

> `Amir Kabir. He printed his own praises first.`
> `Morgan Shuster. Organized a gendarmerie and got an ultimatum for it.`
> `Faramoushkhaneh. House of Oblivion, and you still couldn't place it.`

This is the default, not a tolerated exception — **149 English and 319 Persian rows** carry
it, and it is what makes a right answer worth hearing rather than just scored. The answer
lands, and the second sentence teaches the contestant something they did not know, or turns
the knife, or both. It is the target every `correctLine` should be written toward, and it is
the only reason rules 2 and 5 exist: those two are this shape with the fact removed. If you
have written `<answer>.` and cannot say what comes next, you do not yet have the line — go
find the fact. Never admire the contestant in place of it.

Two patterns are **variety, not defect**, and a rewrite should leave them alone: the Persian
`را نه` antithesis (**22** rows, a different sentence behind every one) and English lines
ending in `it` (**49**, eight of them `Knew it.`), where the constructions genuinely
differ. Density alone is not a defect; a fixed hinge with rotating content is. The same
judgement covers `wrongLine`: **1,870 English / 1,860 Persian distinct of 2,205** is fine, since
a wrong line is meant to be generic.

`Tools/check_bank.py` counts them on every run:

```
python3 Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js
```

It prints `correctLine — 1000 lines, 1000 distinct` when clean. Anything below 1,000 is a
duplicate and the batch is not finished.

---

## 9. Both languages, always

English bank for English mode, Persian bank for Persian mode — never mixed. `i18n.js`
holds no clue text and `app.js` selects a bank by language; a bank that ships one language
plays under the other language's chrome with no error. Persian must be real Persian, not
transliteration, and the two banks mirror each other id for id.

**They mirror in id, category and slot — not in question.** The Persian bank is not a
translation of the English one, and reading it as one is the mistake that produced most of
this file's repair list. Measured 2026-09-15 across the 325 slots that then held an
`_encore`: `fa_answer == en_answer` in **0** of them, and the two `clue_text`s were
identical in **0**. `single_golden_age_islamic_sciences_800` asks about Biruni in English
and al-Khwarizmi in Persian; `women_savushun_1600` asks the novel in English and its author
in Persian. So a Persian row's `accepted_aliases`, `distractor_rationales` and
`host_reactions` cannot be inherited from its English twin — the entities they name are not
on the Persian row at all. It also means the Persian bank must carry its own provenance and
is not answerable from the English passage; see §10.

### A year in a Persian clue names its calendar

Every year in the Persian bank that can be settled carries the name of the calendar it is
in — `۱۳۵۷ خورشیدی`, `۱۹۷۹ میلادی`. A bare numeral is a defect. The reader cannot tell
which calendar it is in, and some years are real in both: ۱۳۵۰ is 1971 shamsi and 1350 CE
Gregorian, and both readings are correct somewhere in this corpus.

- **An Iranian year is shamsi**: `۱۳۵۷ خورشیدی`.
- **A non-Iranian year, or an Iranian year before roughly 1800, keeps its Gregorian
  numeral and takes `میلادی`**: `۱۷۹۸ میلادی` for the Rosetta Stone, `۱۲۴۰ میلادی` for Ibn
  Arabi.
- **A year from about 1800 onward is rewritten into shamsi, not left Gregorian.** The
  bank's own marked rows do this; a Persian clue about 1953 says ۱۳۳۲, not ۱۹۵۳.
- **1200–1499 is the only genuinely ambiguous band.** If the Gregorian reading would be a
  real medieval event, name the calendar explicitly rather than inferring.
- **A year in 12xx–14xx following a Persian month name is shamsi.** The month heads no
  other calendar in this corpus, so this one inference is safe and should be taken.

`Tools/normalize_fa_prose.py` is this rule, in code — four ordered passes that resolve a
year against its English twin, the twin's explanation, a preceding month name, or the
century the row is about, and leave anything they cannot settle to a human review tail
rather than guessing. It is not a second opinion to be argued with; it is the definition.

```
python3 Tools/normalize_fa_prose.py --check
```

`--check` exits 1 if the bank still holds a year needing a calendar. `Tools/append_batch.py`
runs the same four passes over every candidate batch and refuses to land a Persian row whose
year names none — judged on that batch's own ids only, since the archive as it stands carries
bare years nobody has called yet. Authoring scripts (`Course/banks/*.py`, `Tools/build_batch_*.py`)
that write a year into a row write the marker with it, or they put the drift straight back.

---

## 10. Provenance

Every clue carries the book, author and page it came from, and the passage it was pulled
out of. `Sources/MAIN CORPUS/` — 48 copyrighted books in seven folders, the shelf this
bank was written from — is **gitignored and stays that way**; it cannot be redistributed
and several files sit near GitHub's size limit. Cite titles and authors freely; never
commit the books or long verbatim passages.

**A row's second question keeps the row's provenance, and only if the same book covers
it.** The 325 slots that used to hold an `_encore` — a byte-identical copy of the row above
it, stamped with a stock line by a generator reaching for "10 clues per category" — now hold
a genuinely different question on the *same* answer. Keeping the answer fixed is what makes
that safe: the three wrong options stay wrong, the aliases stay valid, and `book`, `author`
and `page` still point at the right shelf. Ground the second question in a **different fact
stated in the row's own `supporting_passage`** where the passage holds one; where it does
not, use another well-established fact about the same answer that `book_title` documents.
Never leave the citation as decoration for a fact the cited book does not carry.

**Every row carries a source, and the source is on screen.** `book_title` and `author` are
not metadata for the author's benefit — `Web/app.js:2710` prints them under the answer,
after the explanation, once the last contestant has had their shot, as
`Iran: A Modern History · Abbas Amanat · p. 300`. That line is what makes a right answer
*checkable* rather than merely scored, and it is the difference between a quiz and a
course. **Both fields on every row**, English and Persian: an empty one is a blank where
the source should be, and there is no row whose answer came from nowhere.

**The citation is copied, never composed.** Every field comes off the work itself: open
the source, take the title **as that work prints it**, the author from its title page or
its own citation line, and a page inside the range the work occupies.

- **A chapter's shelf entry is its book.** "Protests, Participation and Representation in
  an Improvisational Polity" is a chapter *inside* `The Sacred Republic: Power and
  Institutions in Iran` — that is the `book_title`, and the page is the chapter's page.
  Never assemble a book title out of the words of a chapter's own subtitle.
- **Search the source for your own passage.** A `supporting_passage` you cannot find in
  the work you named means the citation is wrong, however plausible it reads.
- **The page says how big the work is.** A chapter printed 47–65 cannot be cited at p. 8.
  Pages like 1, 8, 11, 14 under a book title are the shape of a number typed to fill a
  field.
- **If you cannot see the citation, the row is unsourced.** Say so and stop. An honest
  "no source found" is a row to replace or drop; an invented citation prints on screen
  under the answer, to an audience that can look it up.

**The precedent (2026-09-17).** Four rows of the Iran course's `IMPROV AT THE MINISTRY`
cite *An Improvisational Polity: Form and Substance in the Islamic Republic* at pages 1,
8, 11 and 14. No such work exists; the phrase "Form and Substance" appears nowhere in the
corpus; and the real chapter — Keshavarzian's, in *The Sacred Republic*, printed 47–65 —
contains none of the four passages. It was found by hand, because nothing in the tree
compares a citation against the source it names. This rule is the check.

`page` is expected too, with one exception: a `final` row answers for a whole book or a
whole module and has no single page to point at, so it carries the book and the author and
no page. Never invent a page to fill the field — a wrong page in an academic game is worse
than an honest blank. A non-final row with no page is a row whose citation was not
finished.

`Tools/check_bank.py` enforces the two required fields (`check_citations`) — an error in
MAIN, where both archives carry both fields on all 2,205 rows, and a warning on a course, where all 693
rows of `iran-in-world-politics` and all 512 of `qajars` now cite.

**A source does not have to be a book.** `book_title` is the first slot of the source line
and the line is `book_title · author · p. N`, so when the answer *is* a document — a treaty,
a Security Council resolution, a constitution, a manifesto — the document is what goes in
the two fields: `Joint Comprehensive Plan of Action (UN Security Council Resolution 2231)` /
`United Nations Security Council`. That row (`final_snapback`, the course's Final on the
snapback mechanism) is the precedent, set 2026-09-15 on Morad's instruction to "cite the
agreement itself" rather than the nearest chapter that mentions it. **Cite the instrument,
not the reading about it**, whenever the instrument is what the question is about. A
document has no page in the sense `page` means, so it carries none — the same exemption a
`final` gets, and for the same reason.

**The Persian bank's provenance fields are still the English row's.** Measured 2026-09-17:
`book_title`, `author`, `supporting_passage` and `historical_period` are the English values
in **2,205 of 2,205** rows — the mirroring is total, and every row added since the first
measurement inherited it. (On the 1,205 promoted rows `supporting_passage` is empty on both
sides, so that one mirrors trivially; the other three are copied values. `theme` is identical
as well, and that one is correct: it is an
English keyword in both banks by contract.) Since §9 establishes
that the two rows ask different questions about different entities, a Persian row's citation
is currently a citation for a different clue. **Reported, not repaired.** Giving 2,205
Persian rows their own provenance means reading the corpus in Persian and is a separate
piece of work; it is recorded here so nobody re-derives it or mistakes it for a translation
bug.

---

## 11. Writing a clue in — the mechanics

**Write a batch, merge it, regenerate the play file.** That is the whole procedure; the
rest of this section is how not to break the archive along the way.

A new clue is authored into `QuestionBank/incoming/<stem>-en.json` (+ `-fa.json`), and
`Tools/append_batch.py <stem>` is the only thing that writes the archive — it validates the
batch against the whole merged bank, backs both archives up, and refuses the write if
anything fails. Edit the archive by hand only to repair it. The play file is generated from
the archive and is the one that cannot be read by eye.

**A row you wrote is a draft until you have read it against its source.**
`editorial_validation_status` is `"draft"` on a row nobody has checked and `"verified"` once
someone has opened the book and found the passage. `Tools/append_batch.py` refuses a batch
carrying a draft row, and there is no override, because setting the status *is* the record
of having read it. The third word, `"promoted"`, is not an authoring status at all — it
belongs to the archive and marks a row that came up from a course (§13).

- `QuestionBank/verified_clues.json` is a plain JSON array — the one the merge writes to,
  for English; `QuestionBank/verified_clues_fa.json` holds Persian. Each row
  also carries its `language` field. `Web/data/clues.js` is
  literally `window.CLUES=[{...},{...},…];` followed by a newline; `clues_fa.js` is the
  same with `CLUES_FA`.
- **The archive is pretty-printed, and the play file is one line.** Measured 2026-09-17:
  `verified_clues.json` is 92,255 lines and `verified_clues_fa.json` 92,476 — two spaces per
  level, `ensure_ascii=False` so the Persian stays readable, no trailing newline on the
  English file and one on the Persian. A gate that calls both files "one enormous single
  line" is describing the play files only.
- **Re-serialise the archive only with those exact parameters.** It reproduces
  byte-for-byte, which is what makes a programmatic edit safe and reviewable: every row the
  edit does not touch comes back identical, so the diff is the change. `json.dump(rows,
  indent=2, ensure_ascii=False)` is right; the defaults are not — they collapse the file to
  one line and `ensure_ascii=True` turns every Persian character into `\uXXXX`, a rewrite
  of all 2,205 rows that buries the actual edit. Assert a round-trip before writing: if
  `json.dumps(json.load(f), indent=2, ensure_ascii=False)` plus the file's newline
  convention does not equal the bytes on disk, stop.
- **`grep -c` lies on the play file.** That one is a single line, so a count of `1` means
  "present", not "one occurrence". Parse in Python when the number matters. On the archive
  it counts rows honestly. To read a play file at all, use
  `json.JSONDecoder().raw_decode(text, text.index('['))` — `json.load` fails on the
  `window.CLUES=` prefix and the trailing `;`.
- Keep the JSON valid, keep `id` unique, and keep the same `id` across both languages so
  the two banks line up clue for clue.
- **Regenerate, never hand-edit the play file.** Run the generator in §1 after changing the
  archive. A hand edit to `Web/data/clues.js` is overwritten the next time anyone does, and
  a row that exists only in the archive does not play until it is.

### What checks what

Four kinds of script read a bank, and they answer different questions.

| script | question it answers | what it reads |
|---|---|---|
| `Tools/validate_1000_clues.py`, `Tools/validate_persian_bank.py` | is the **archive** well-formed? | `QuestionBank/verified_clues.json` — schema, citations, 373 category slots, no English in the Persian bank, the difficulty ladder |
| `Tools/verify_flawless_state.py` | is the **archive** still whole? | the same two files — placeholder formulas gone, every `(round, value)` pair on its exact difficulty label |
| `Tools/check_bank.py` | is a bank's **content** correct? | the play file — `Web/data/clues.js`, or a course's `Web/courses/<id>/data/bank-*.js` — or, with `--archive`, `QuestionBank/verified_clues*.json` itself |
| `Tools/check_repeats.py` | does a clue ask what another clue already asks? | a batch, or with `--bank` the whole archive — verbatim *and* reworded |

**All three archive validators pin the count.** `validate_1000_clues.py` and
`verify_flawless_state.py` assert 2,205 rows, and `validate_persian_bank.py` asserts 2,205
rows, 373 categories, and 2,205 entries in two derived dictionaries —
`QuestionBank/persian_clues.json` and `App/Resources/persian_clues.json`, both keyed by id.
A merge therefore makes them fail by arithmetic, not because anything is wrong: bump those
four numbers in the same commit as the batch. `Tools/append_batch.py` does **not** run them,
and it does not regenerate either dictionary, so a merge leaves both dictionaries one batch
short unless something else writes them — check them after a merge rather than assuming.
(`Tools/check_bank.py`, which `append_batch.py` does run, carries no count pin.)

`Tools/validate_3000_clues.py:67` makes the same shape assertions, but against **3,000
rows and 360 categories**. Stale: it describes an older 3,000-clue bank. Do not treat it as
a gate.

**`Tools/check_bank.py` is the bank content checker.** It checks, per row: the four options
and `options[correct] == answer`; non-empty `aliases`; all five rungs present per category
with a byte-identical title; `value` on the round's ladder; `difficulty` matching the rung;
the answer's distinctive words absent from the clue; language purity (no Persian script in
the English bank and vice versa); `id` mirroring between the two languages; that an
`_a`/`_b` pair carries **two** questions rather than one written twice; and — with
`--edition` — which categories reach a professor theme clip. It is also the only thing that
checks the *content* of a **course** bank, which has no archive behind it at all.

Against the archive it adds the checks the archive can answer and a play file cannot, which
are the ones this file's repair list kept finding by hand. `--archive` reads the archive's
key names (`clue_text`, `canonical_answer`, `accepted_aliases`, `correct_option_index`,
`book_title`, `supporting_passage`, `historical_period`) and maps
`host_reactions.correct_generic` onto the play shape, so one rule set covers both:

- **every slot holds two different questions.** A `(category, round, value)` slot with two
  rows must not carry the same `clue_text` twice — that is the `_encore` defect, and it was
  325 slots in both languages;
- **the two rows of a slot agree about what they share.** An `_encore` pair is one answer
  asked twice, so the four `options`, the `correct` index, the `aliases`, `book`, `author`,
  `period`, `theme` and `difficulty` belong to the **slot**, not to the row — patch one and
  its twin has to move with it. An `_a`/`_b` pair is the opposite case: two questions about
  two different answers, which all 170 are. So the rule keys on the **answer** and not the
  suffix, and two rows sharing a slot while answering differently are left alone. `page` is
  exempt on purpose — a final's two questions were drawn from different pages of the same
  book, and the citation follows the passage the row actually rests on. This rule exists
  because a repair wave patched one twin and not the other in five Persian finals and one
  encore pair, and nothing before it noticed;
- **an alias belongs to its own row** (§7) — the row's answer appears in its own list, no
  alias repeats, and no alias is one of the row's own wrong options;
- **an option is not findable by its surface.** Parenthetical glosses aside, a dash, colon
  or semicolon inside an option that no other option carries is a tell (§6);
- **rationales name the row's own distractors.** `distractor_rationales` must gloss the
  three wrong options *on that row* and no others. Archive-only: it is the only place that
  field exists, since it never reaches the player.
- **category spelling is consistent** across the rows that share a category.

```
python3 Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js
python3 Tools/check_bank.py QuestionBank/verified_clues.json --archive --lang en
python3 Tools/check_bank.py QuestionBank/verified_clues_fa.json --archive --lang fa
```

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
written for. **A course's bank is absorbed whole** — every clue on its board, the seminar
readings' questions included. There is no stand-alone test and no per-clue judgement;
an eligibility rule on top of a straight copy is what had to be unwound twice, so it is
gone and the rule is now simply that MAIN absorbs a course.

**It is a conversion, not a re-authoring.** `Tools/promote_course_bank.py` reads the
course's own play bank read-only and appends this archive's 27-field rows; the clue text,
the answers, the options and the host lines are copied, and only what is mechanical
changes — a subject-led id, an option rotation so the answer sits at index 0, a slugged
`source_id`. A pasted row still fails quietly (§1 and §5), which is why the tool and not
the hand does it, and the course's own files are never written to.

Two archive fields have no counterpart in a course bank and are not derivable — the
quoting `supporting_passage` and the three `distractor_rationales`. Both are archive-only,
so a player sees no difference; they land empty and the row is stamped
`editorial_validation_status: "promoted"` rather than `"verified"`. The gates require both
fields on verified rows and count the promoted ones, printing what is still owed, so the
debt is visible instead of being filled in with invented evidence. That stamp is the
promoted-row marker and lives only in the archive — the play file does not carry it. After
IR4595 and the Qajars the tally is `{"verified": 1000, "promoted": 1205}`, and
`Tools/promote_course_bank.py <course-id> --check` is the gate: it rebuilds the course's
rows from the course's own bank and fails on **ABSENT** — a course whose bank never
reached the archive, which is every row of a course that has not been promoted — and on
**DRIFT**, which is a row the archive still carries in a form the course no longer asks.
`Course/build_edition.sh` runs it as its fourth gate, so a course is not finished until
MAIN has absorbed it; a course edited after promotion leaves MAIN serving a question that
is no longer on the board, and that now fails the build rather than shipping.

**Every course is a source, not a chosen few.** Each course edition is written from its
own syllabus and is self-contained — one course never draws on another, and none draws on
MAIN — and each of those closed banks is at the same time open upward. Adding a course
adds a bank MAIN absorbs; there is nothing to authorize per course and no list of courses
cleared for it.

**A promoted course's readings join MAIN's shelf.** A promoted clue cites the reading it
came from, and that reading sits in the course's corpus rather than in
`Sources/MAIN CORPUS/`, so the course's reading list is added to the shelf
`window.READINGS_GENERAL` behind the main edition in the same movement. A citation the
player cannot look up is not a citation. MAIN's shelf is generated by
`Tools/make_readings.py` out of `Corpus/Metadata/corpus_manifest.json` and is never
hand-edited; a course's shelf is authored in the course's own folder, so the generator is
the thing that learns to read it — a `COURSE_SHELVES` line per absorbed course, which also
files each of that course's weeks under MAIN's own heading, since a week number belongs to
a seminar and not to MAIN's shelf. The rows keep their own chips, and the course's file is
never written to. The shelf is counted (`Tools/check_readings.py`, asserted **92 for MAIN**
and 42 for IR4595), so the count moves in the same commit and the move is stated.

The shelf is the corpus behind the bank — MAIN's own fifty sources in
`Sources/MAIN CORPUS/` plus the absorbed course's forty-two, not only those a board cites —
so it is not a standing guarantee that every citation resolves. As of 2026-09-15, 31 of
MAIN's 32 cited works are on it; the exception, `Guardians of the Revolution` (Ray
Takeyh), is cited with no PDF anywhere under `Sources/`.

Nothing travels the other way. A course bank holds that course's questions and nothing
else, and a clue from here never enters one to make up the sixty a game needs. The
reasoning, and the rule as it applies to an agent editing a syllabus, is in
`BANK_SCOPE.md`.
