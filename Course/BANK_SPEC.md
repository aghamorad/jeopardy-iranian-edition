# Course bank spec — what a course's questions have to contain

This is the contract between whoever writes the questions (you + a strong external text
model, from a syllabus) and the engine that plays them. Give the prompt at the bottom to
that model, paste the result back, and the course's bank is built from it.

The channel is a model, not a product — whichever one is reachable and affordable. On this
machine that has meant the Codex CLI; Gemini is rejected (bad output, awkward UI) and
`gpt-6-astra` is banned on cost. The contract below is what matters and it is
model-agnostic.

## Your bank is your syllabus, and nothing else

Everything in a course's bank is written for that course. A clue from the main game —
the comprehensive, all-of-Iran bank — never gets copied into it, however short of the
sixty a game needs the syllabus turns out to be. A borrowed clue fails mechanically as
well as in principle: a course recognises a category by keyword and introduces it as one
of the course's own weeks, so a category it does not recognise is a subject the class was
never taught.

The other direction is open. A question of yours that stands on its own — one a general
player could answer from the same reference books, without having sat the course — may
also be added to the main bank, which is the umbrella and holds everything ever designed.
That is a promotion, re-authored into the main bank's shape and contract, not a copy.

`BANK_SCOPE.md` in the engine repo states the rule for both directions and is the
canonical version if this section and that one ever disagree.

## The pipeline

```
syllabus ──> text model ──> two question banks ──> build_edition.sh ──> on the splash
```

There is no separate build any more. Every course lives inside the game's own web tree at
`Web/courses/<course-id>/`, and `Web/` is what ships, so a course written in the right
place is already in every build — the app, the desktop shell and the phone shell alike.
`build_edition.sh` is no longer a copier; it is a gate. Given a course id it runs the two
checkers and passes or fails, and it writes nothing.

**Online comes for free.** Netplay is the engine's own, so a course host can open a table
and invite a guest exactly as the general edition does, and the invite link carries the
edition — the guest lands on the course skin and joins that table. Nothing in a bank and
nothing in a course has to be written for it; there is no edition-specific online path to
keep in step.

## The one rule that will bite you

The board is built by grouping clues by `category`, then keeping only the categories
that carry a clue at **every** rung of that round's ladder. Six are drawn at random.

A category is spent when it is drawn and is never returned, so the single round and the
double round cannot share one. A full game therefore needs:

> **six complete single categories + six complete double categories = 60 clues,
> plus at least three final clues.**

Coming up short does not raise an error. The board just renders with too few columns,
and the first person to notice is the class. `check_edition.py` fails a course that
cannot fill one.

The two pools are only disjoint where the *names* are. One category name may carry all
five single values **and** all five double values, in which case it qualifies in both
rounds — and because a spent name is spent for the whole match, the single round is free
to take it. So what the double round can actually count on is not "the names that qualify
in double" but "the names that qualify in double and cannot qualify in single", and that
smaller set has to hold six by itself. Twelve distinct qualifying categories per language
satisfies both counts at once. A bank that reuses one name across the two rounds to reach
twelve does not, even though both per-round numbers print six.

`check_edition.py` checks both counts. It names any category that qualifies in both
rounds, and it fails when the double round's own pool — the double-qualifying names the
single round cannot take — is under six.

Sixty clues is exactly one game — every match deals the same board. For a board that
varies between matches, aim for **nine or more complete categories per round**
(~95 clues). More is better; there is no upper limit.

## The ladders

`value` is the ladder rung, **not** the number the tile prints. The engine re-stamps
the printed number itself, so use these exact values:

| round  | `value` must be one of     | the tile then prints |
|--------|----------------------------|----------------------|
| single | 200, 400, 600, 800, 1000   | ۱۰ … ۲۰۰ میلیون      |
| double | 400, 800, 1200, 1600, 2000 | ۲۰ … ۲۰۰ میلیون      |
| final  | 0                          | —                    |

Every category needs all five rungs of its round. `difficulty` is one of `CASUAL`,
`STANDARD`, `SCHOLAR`, `INSUFFERABLE` — and it is **not** a judgement call, it tracks the
rung exactly. This mapping holds across every row of the engine's own 1,000-clue bank, so
match it rather than choosing a label per clue:

| rung | `difficulty` |
|---|---|
| single 200 | `CASUAL` |
| single 400, single 600, double 400, double 800 | `STANDARD` |
| single 800, double 1200, double 1600 | `SCHOLAR` |
| single 1000, double 2000, final 0 | `INSUFFERABLE` |

## Fields

Required on every clue — the build fails without them:

| field | notes |
|---|---|
| `id` | unique, lowercase, no spaces. **Use the same id in both languages** so the two banks line up. |
| `round` | `single`, `double`, or `final` |
| `value` | a rung from the table above |
| `category` | a **pun**, not a description — real Jeopardy convention. Must match *exactly* across all five clues of the same category. |
| `theme` | see below — an English keyword, not a display string |
| `difficulty` | `CASUAL` / `STANDARD` / `SCHOLAR` / `INSUFFERABLE` |
| `clue` | the question, in that language |
| `answer` | the answer, in that language |
| `aliases` | accepted spellings. Never empty — an empty list means only an exact answer counts. |
| `options` | exactly 4 multiple-choice strings; `options[correct]` must equal `answer` |
| `correct` | index 0–3 |
| `explanation` | shown after the answer; say why, not just what |
| `correctLine` | host's line when answered right |
| `wrongLine` | host's line when answered wrong |

**Required — `book` and `author` on every row, in both languages.**

`book`, `author`, `page` — the reading a question came from: the lecture, chapter or
paper, so a student can look it up. The engine renders them as a source line under the
answer, after the explanation, once the last contestant has had their shot
(`Web/app.js:2710`):

> Iran: A Modern History · Abbas Amanat · p. 300

That line is the whole reason a right answer is *checkable* rather than merely scored,
and it is what makes this a course and not a quiz. Do not leave it out because the
engine tolerates a missing field — it renders the blank just as happily.

`page` is expected on every row except a `final`, which answers for a whole module and
has no single page; a final carries the book and the author and no page. **Never invent a
page number to fill the field.** `Course/check_edition.py` + `Tools/check_bank.py` catch a
row with no book or no author (`check_citations`), naming it. (`period` and `passage`
exist in the original banks but nothing reads them.)

## Two shapes exist — this spec is the one that plays

The engine repo holds the clue data twice, in two files whose **field names do not
match**:

- `Web/data/clues.js` (`window.CLUES`) is the **play file** — what the browser actually
  loads. This spec, and every course bank under `Web/courses/<id>/data/`, uses *this*
  shape: `clue`, `answer`, `aliases`, `correct`, `correctLine`, `wrongLine`.
- `QuestionBank/verified_clues.json` in the engine repo is the **archive** — a richer
  shape with `clue_text`, `canonical_answer`, `accepted_aliases`, `correct_option_index`
  and a flat `host_reactions` dict. **Nothing in `Web/` reads `host_reactions`**; the
  strings that play are the `correctLine` / `wrongLine` fields above.

The archive is **canonical**, and the play file is **generated** from it one-way: the
engine repo's `Tools/append_flawless_engine.py` maps each archive field onto its play-file
name (`clue_text`→`clue`, `canonical_answer`→`answer`, `host_reactions.correct_generic`→
`correctLine`, and so on), so the two cannot drift. Changing an engine clue therefore means
editing the archive and regenerating — never a hand edit to `clues.js`, which the next run
overwrites. (Verified 2026-09-14: byte-identical for all 1,000 rows in both languages.)

A course bank, by contrast, has no archive behind it: it is generated straight into the
play shape, which is why this spec only needs the one table and why `check_bank.py` is its
only content gate.

The same rules, stated once for the whole project, live in the engine repo's
`QUESTION_AUTHORING.md`. If you change a rule here, change it there too.

## `theme` is an English keyword — read this bit

`theme` is not shown to players. The engine lowercases it, glues it to the category
name, and looks for the words below. Whichever matches first decides the small grey
line under the category header — the subtitle that reads `سیاست و جامعه`,
`فرهنگ و هنر`, `تاریخ و انقلاب‌ها`, `مکان‌ها و جغرافیا`, or `مردم و چهره‌ها`.
Anything unmatched prints `متفرقه` (*miscellaneous*).

So: to get a sensible subtitle, put one of these English words in `theme`. This is the
engine's real list — `PERSIAN_BUCKETS` in `app.js`, read off the source, not abridged.

| subtitle shown | words that trigger it (any substring) |
|---|---|
| مردم و چهره‌ها | trailblazer, hero, maestro, instrument, tragic, pioneer, figure, coronation, epistolary, monarchy, royal |
| مکان‌ها و جغرافیا | geograph, mountain, river, desert, lake, maritime, capital, strait, frontier, garden, archaeolog, monument, territorial, island, shore, valley, caspian, gulf, ecology, city |
| تاریخ و انقلاب‌ها | war, battle, empire, dynast, revolt, rebellion, revolution, liberation, coup, occupation, conquest, siege, barricade, movement, uprising, conflict, military, combat, aftermath, constitution, reform, purge, destiny, turning point, crime |
| فرهنگ و هنر | poet, poetic, verse, literature, novel, prose, fiction, cinema, directing, palme, art, calligraph, architecture, music, radif, vocal, sound, handicraft, cuisine, festival, culture, material, memoir, linguistic, religion, theolog, mystic, philosoph, shrine, pilgrimage, clergy, science, medicine, engineering, aviation, mytholog, spectacle |
| سیاست و جامعه | politic, diploma, intelligence, statecraft, governance, geopolit, opec, petroleum, oil, econom, press, education, activism, espionage, spy, secret societ, coalition, ideolog, party, parliament, treasury, commerce, trade, boycott, sanction, law, legal, capitulation, advisor, concession, commodit, infrastructure, institution, agriculture |

These buckets are the engine's, and they are built for Iranian subject matter — the
general edition is the whole of Iran and this course is one aspect of it, so the same
vocabulary serves both. That is not true of every possible course: one on another subject
would land in whichever bucket a stray substring happened to fire, and a confident wrong
subtitle is worse than none. Extending the buckets is engine work, not a bank edit (see
below), so a new subject needs that done first. For an Iranian course `متفرقه` should
never appear — the `theme` rule in the prompt below is the whole mechanism.

**Two traps, both verified against the source.** First, the buckets are tested **in
order** and the first substring match wins, so a category with no exact word still lands
somewhere as long as its `theme` contains one of these fragments. Second, because
matching is *substring*, short keywords fire inside unrelated words: `party` contains
`art` and will render فرهنگ و هنر, `city` is inside `ethnicity`, and `oil` is inside
`boiling` and `turmoil`. So pick long, distinctive keywords. For a politics module,
`politic`, `geopolit`, `diploma`, `statecraft`, `governance`, `sanction`, `econom`,
`military`, `ideolog`, `clergy` and `religion` are the workhorses — avoid `party`,
`art`, `city` and `oil` when a longer form will do.

The genuine lexical gaps are *minority*, *ethnic*, *gender* and *diaspora* — no bucket
carries them. Route such a category through `politic` or `activism` rather than inventing
a word. The buckets live in `app.js`, which is engine code: extending them changes the
live site, so it is a decision, not a tweak. Choosing an existing keyword costs nothing.

## Bilingual — both banks, always

The game ships in English and Persian. The engine picks a bank by language with
`BANKS[lang] || BANKS.en`, so a course that ships only English **silently plays English
questions under Persian chrome**, with no error anywhere. The gate refuses to pass without
both files:

```
Web/courses/<course-id>/data/bank-en.js  →  window.COURSE_CLUES_<ID> = [ ... ]
Web/courses/<course-id>/data/bank-fa.js  →  window.COURSE_CLUES_<ID>_FA = [ ... ]
```

**The folder name is the id, and the globals are that name in upper snake case** —
`iran-in-world-politics` gives `COURSE_CLUES_IRAN_IN_WORLD_POLITICS`. Folder, `id`,
`?ed=` value and `data-edition` attribute are all one string; the bank names are derived
from it, so grep the folder name and you find everything the course owns.

**Never `window.CLUES`.** That global is the main edition's own bank — the whole of Iran,
everything ever designed. A course that writes to it deals its questions to MAIN, with no
error anywhere. `registerEdition` deals a show only its own array, which is the mechanism
that keeps the two apart; `check_edition.py` derives the required global from the folder
and fails on anything else.

Both files must be valid JSON between the brackets. Persian must be real Persian, not
a transliteration — the game has a tolerant answer judge that reads Persian, so
`aliases` should include both scripts for names that have both.

**Make one alias list per answer, and mean it.** An alias has to be a name for *its own*
row's answer: `Tools/check_bank.py` flags a row whose aliases share no token with the
answer it sits on, because the judge would then accept some other question's answer. In
MAIN that check is an error and it earns it — 347 of the 1,000 Persian rows were listing
another row's names. **In a course it warns, and that is deliberate.** A course's aliases
are translations and transliterations by construction — `Muscat` / `Oman`, `Erbil` /
`Hewler`, `Gasoline` / `Petrol` — correct pairs that share no token however right they
are. Read the warning; do not assume the tool is wrong, and do not assume the row is
either. 46 of the 90 rows a real course flagged were exactly that legitimate pair.

## The host

The host is smug, snarky and mean. `correctLine` and `wrongLine` are his dialogue:
dry, a little cruel, never congratulatory. "Correct. A real question would have been a
fairer test." not "Great job!". Keep it short — one sentence.

He has **no name** — do not give him one, and do not write him as a warm erudite
broadcaster. His comedy is aimed at the contestant and at Iranian social habits: the
confident uncle, the dinner-party fact, the family WhatsApp group, the taxi driver who
knows everything. Praise is grudging and backhanded; a correction is rude and never a
lecture. Same register in both languages.

**Do not let the lines fall into a formula.** Measured in the engine's own bank on
2026-09-14, at the point where the lines are written: 893 of 1,000 correctLines end in one
of three tails — "Spot on!" (340), "The history holds!" (325), "Quite right." (228) — and
only 665 distinct wrongLines cover the same 1,000 rows. That is a generator habit, not a
voice. Write each line fresh, and check the tail before you ship a batch.

**A zero tail count is not a clean bank.** Two shapes carry no stock tail and so survive
that search. The first is `<answer>. Correct.` — the answer, then a one-word verdict:
**49 English rows** of MAIN had it, and the player reads the answer twice, because
`app.js` prints the `correctLine` and then the canonical answer underneath. The second is
`<answer>. Exceptional scholarship.` — the answer, then a *phrase* of praise: **8 English
rows**, all at the top rung, and it hides a second time because the tail test looks for
one word and this verdict is three. Both are mechanical to catch: strip the answer and
every alias out of the line, and if five words or fewer of pure praise remain, there is no
line there.

**The house shape is to name the answer and then pay it off with a fact.** That is the
target, not a tolerated exception:

> `Amir Kabir. He printed his own praises first.`
> `Faramoushkhaneh. House of Oblivion, and you still couldn't place it.`

**149 English and 319 Persian rows** of MAIN carry it. The answer lands, and the second
sentence teaches the student something, or turns the knife, or both. Write toward it. The
two hollow shapes above are this one with the fact removed — so if you have written
`<answer>.` and cannot say what comes next, you do not have the line yet. Go find the fact.
Never admire the student in place of it.

## Prompt to give the model

> Write a Jeopardy question bank for a university course, from the syllabus below.
>
> Output **two** JavaScript files, nothing else in them: one English, one Persian.
> Each is a single array of objects:
>
> ```
> var bankEn = [ { "id": "...", "round": "single", "value": 200, ... } ];
> var bankFa = [ { ... } ];
> ```
>
> Rules:
> 1. Produce **six complete categories for the single round and six for the double
>    round**, five clues each — 60 clues per language. Add three final clues
>    (`"round": "final"`, `"value": 0`).
> 2. **Category titles are puns, never dry descriptions.** Real Jeopardy convention:
>    double entendres, pop-culture twists, idioms (`MOSSAD-EGH IN THE MIDDLE`,
>    `WE DON'T COTTON TO CONCESSIONS`, `OPERATION AJAX & CLEANSER`). In Persian the pun
>    must be native wit (طنز زبانی و کنایه) — never a literal translation of the English
>    one. `طوفان شن در طبس و شکست عملیات پنجه عقاب` is unacceptable; `پنجه در شن` is.
> 3. Within a category, the five clues must carry `value` 200/400/600/800/1000
>    (single) or 400/800/1200/1600/2000 (double) — one of each, no gaps, no repeats.
>    The `category` string must be byte-identical across its five clues. No two
>    categories in one bank may differ by nothing but a diacritic or a ZWNJ — the Persian
>    side of a real course did once (`صرف و نحو استکبارستیزی` against
>    `صرف و نحوِ استکبارستیزی`, one category to a reader and two to the engine), and the
>    two languages must make the same distinctions: where English has two categories,
>    Persian may not collapse them into one.
> 4. `difficulty` follows the rung exactly, one label per rung. Single round: 200 →
>    `CASUAL`, 400 and 600 → `STANDARD`, 800 → `SCHOLAR`, 1000 → `INSUFFERABLE`. Double
>    round: 400 and 800 → `STANDARD`, 1200 and 1600 → `SCHOLAR`, 2000 → `INSUFFERABLE`.
>    Final clues → `INSUFFERABLE`.
> 5. Every clue has exactly 4 `options`, `correct` is the 0-based index of the right
>    one, and `options[correct]` is the same text as `answer`.
> 6. `aliases` lists every spelling a student might type, including Persian and
>    English forms of names. Never empty.
> 7. `theme` is an **English** keyword, one per clue, chosen from this list — and it
>    must be a word from the list, not a word of your own invention:
>    trailblazer, hero, tragic, pioneer, figure, monarchy, royal, geograph, mountain,
>    river, desert, lake, maritime, capital, strait, frontier, garden, archaeolog,
>    monument, territorial, island, valley, caspian, gulf, city, war, battle, empire,
>    dynast, revolt, rebellion, revolution, liberation, coup, occupation, conquest,
>    siege, movement, uprising, conflict, military, combat, aftermath, constitution,
>    reform, purge, poet, literature, novel, cinema, art, calligraph, architecture,
>    music, handicraft, cuisine, festival, culture, memoir, religion, theolog, mystic,
>    philosoph, shrine, clergy, science, medicine, engineering, mytholog, politic,
>    diploma, intelligence, statecraft, governance, geopolit, petroleum, econom, press,
>    education, activism, coalition, ideolog, parliament, commerce, trade, boycott,
>    sanction, law, institution, agriculture. Pick the longest form that fits — short
>    words match inside longer ones and land in the wrong bucket.
> 8. `correctLine` and `wrongLine` are the quiz host's lines — smug, snarky, mean.
>    One short sentence each. They may be in the language of that bank. **Never reuse a
>    stock tail** ("Spot on!", "Quite right!", "The history holds!") — every line must
>    end its own way, and no two clues may share a line. Two shapes survive a tail
>    search and both are banned: `<answer>. Correct.` (the answer plus a one-word
>    verdict) and `<answer>. Exceptional scholarship.` (the answer plus a phrase of
>    praise). Either way the player reads the answer twice and learns nothing. **Write
>    the house shape instead: name the answer, then add a real fact about it** —
>    `Amir Kabir. He printed his own praises first.` That is the default, not a
>    concession; a `correctLine` that names the answer and then has nothing to add is
>    not finished.
> 9. `explanation` is two or three sentences of teaching: why the answer is right.
> 10. The Persian bank mirrors the English one clue for clue — same `id`, same
>     `round`, same `value`, same `correct` index — with the clue, answer, options,
>     explanation and host lines written natively in Persian. Do not transliterate.
> 11. **Cite every question.** `book` and `author` on every row, both languages, and
>     `page` too except on the final — the engine prints them under the answer as the
>     source line, and that line is why the student can check you. Never invent a page.
>     **The source need not be a book.** When the question is *about* a document — a
>     treaty, a resolution, a constitution — cite the document itself:
>     `Joint Comprehensive Plan of Action (UN Security Council Resolution 2231)` /
>     `United Nations Security Council`, as this course's `final_snapback` does. Cite the
>     instrument, not the reading about it. A document has no `page`, so it carries none.
> 12. Put the correct answer at index 0 on every clue and leave it there. The engine
>     reshuffles each clue's options as it deals (`shufflingOptions`), so every index
>     plays identically and spreading it by hand achieves nothing. One value on every row
>     also makes the two language banks trivially mirrorable — same `correct` everywhere.
>
> Syllabus:
> [PASTE SYLLABUS HERE]

Paste the two arrays back, wrap each in its named global, drop them in the course's
`data/`, and run `Course/build_edition.sh <course-id>`. Pass and the course is already in
the build — nothing is copied, and the next app build carries it on the splash.
