# C3PO_LOG — the personalized edition builder

A running record of decisions and measurements for this project. The engine has its own
log at `../Jeopardy - Iranian Edition/C3PO_LOG.md`; this one covers only the fork.

---

## 2026-09-14 — the fork exists, and it moved

**What this is.** A second edition of the game for a professor's class: same engine,
questions drawn from his syllabus. Morad supplies a syllabus, Gemini writes the two
question banks, Morad pastes them back, and the edition gets built here. He does not run
scripts, so the build is always this side's job.

**Why an overlay and not a folder copy.** `build_edition.sh` copies the live `Web/` tree
whole and rsyncs `Editions/<Name>/` over it. An edition therefore holds only what
differs — its banks, optionally a stylesheet or art. A copy of the whole folder would
drift: the v1.0.6 buzzer fix would have to be applied twice, forever.

**Verified, not asserted:** the built `dist/_template/app.js` is byte-identical to
`../Jeopardy - Iranian Edition/Web/app.js` —
`a9a62e9ca4ca7536dce1aef48186e34e3e45b61881692d7feccfdd8f01d483a6`, both sides. The
build copies the engine; it does not reimplement it. Zero `.DS_Store` in a build.

**What the board actually requires.** A category qualifies only if it carries a clue at
every rung of its round's ladder — single 200/400/600/800/1000, double
400/800/1200/1600/2000. Six categories are drawn, and `S.usedCategories` is never
cleared, so single and double cannot share one. A full game is **twelve complete
categories (60 clues) plus three finals**. Coming up short raises nothing: the board just
renders with too few columns, and the class notices first. `check_edition.py` refuses to
build a bank that fails this, and warns below nine categories per round because at six
every match deals the same board.

**Two gates added to `check_edition.py`,** both proven to fire and proven not to
false-positive against the 2000 shipped clues: `options[correct]` must equal `answer`,
and ids must be unique across a bank (ids are what pairs the English clue with the
Persian one, so a repeat would make one answerable against the other).

**Bilingual is not optional.** `app.js` resolves the bank with `BANKS[lang] || BANKS.en`,
so an edition shipping only English **silently deals English clues under Persian
chrome**. `build_edition.sh` refuses to build without both `data/clues.js` and
`data/clues_fa.js`. Checked in both directions: Persian board renders Persian heads,
`english_leak: false`.

**The contract is `BANK_SPEC.md`.** Since Gemini writes the banks rather than C3PO, the
load-bearing artifact is the feed format: the field table, the ladders, the
twelve-category rule, the host's voice, and a paste-ready prompt. Keep it in step with
`check_edition.py`.

**The buckets are fine after all.** `theme` is an English keyword, not a display
string, and `persianSubtitle()` matches it against `PERSIAN_BUCKETS` in `app.js`.
I had this logged as a limit that would put `متفرقه` under every category of a
non-history edition. Morad settled it on 2026-09-14: every edition stays Iranian, and
successive editions take different *aspects* of Iran rather than different subjects.
The five buckets are Iran vocabulary, so they keep working, and the engine's
"IRANIAN EDITION" wordmark already says the right thing.

**Corrected against the source, same day.** I first wrote that `sanction` had no bucket
and that a politics module would fall through to `متفرقه`. That was wrong — I had an
abridged copy of the keyword list in my notes. Read off `app.js` lines 155–175, the real
lists are far longer and include exactly the words this module needs: `sanction`,
`diploma`, `statecraft`, `governance`, `geopolit`, `petroleum`, `econom`, `military`,
`clergy`, `theolog`, `strait`, `gulf`. A sanctions or foreign-policy category routes
cleanly. `BANK_SPEC.md` now carries the full list and its Gemini prompt asks for it.

Two real traps found while reading. The buckets are tested **in order**, first substring
match wins, and matching is *substring* — so `party` contains `art` and renders
`فرهنگ و هنر`, `city` sits inside `ethnicity`, `oil` inside `boiling`. The genuine gaps
are only *minority*, *ethnic*, *gender* and *diaspora*; route those through `politic` or
`activism`. No engine change needed either way.

**The move, same day, and then the split.** Both projects left the Desktop for
`~/Claude/Jeopardy/` first. Then Morad asked for the two to be **separated entirely**,
with this one named for the course rather than a generic "Personalized". Final layout —
two siblings, no shared parent:

```
~/Claude/Jeopardy - Iranian Edition/            ← the engine, git repo, live site
~/Claude/Jeopardy - Iran in World Politics Edition/  ← this folder
```

> **[SUPERSEDED — see "The fold into `Course/`" at the end of this log.]** The layout
> above did not hold. `~/Claude/Jeopardy - Iran in World Politics Edition/` no longer
> exists; this folder now lives *inside* the engine tree, at
> `Jeopardy - Iranian Edition/Course/`. The paragraphs below are the record of the day
> and are left as written.

The `Jeopardy/` parent is gone (`rmdir`, empty). Both moves were same-volume renames,
not copies. Verified either side: engine 11984 files / 1632 dirs and this folder 127 / 12,
both **unchanged**; engine still on `main` with `aghamorad/jeopardy-iranian-edition`
intact and `app.js` unchanged at `a9a62e9c…d483a6`.

Two live references had to follow it, both edited twice (once per move):

- `GameEngine/QuestionBank/QuestionBank.swift` — absolute fallback paths on lines 37 and
  60, now `/Users/Morad/Claude/Jeopardy - Iranian Edition/…`. These are the only
  machine-specific strings left in the engine, and both were checked to point at files
  that exist. **This edit leaves the public repo dirty (` M`, 2 insertions / 2
  deletions); it is not committed — Morad's call.**
- `~/Claude/Apps & Games/.claude/launch.json` — the two preview servers' `--directory`
  arguments.

`build_edition.sh` needed no edit either time: its `ENGINE` default was
`$HERE/../Jeopardy - Iranian Edition` while the two folders were siblings, and they sat
at the same depth after the split as before it. Proved by rebuilding `_template` from
the final location — exit 0, 63 EN + 63 FA clues, 6/6 categories qualifying in each
round per bank, 3 finals, and the built `app.js` byte-identical to the engine's.
**[That default is `ENGINE="${JEOPARDY_ENGINE:-$HERE/..}"` today.]** The fold into
`Course/` put the engine one level up instead of beside, so the name to spell out
disappeared with the sibling. See the end of this log.

`AGENTS.md` now sits at `~/Claude/AGENTS.md`, the workspace root, since there is no
parent folder left to hold it. It describes both projects and which one is public.

Stale and deliberately untouched: `Corpus/Metadata/corpus_manifest.json` points at
`/Users/Morad/Spark/...`, a tree that has not existed for some time, and `.build/` holds
199 files with absolute SwiftPM cache paths that regenerate on the next build.

**The syllabus, filed 2026-09-14.** `Syllabus/IR4595 Iran World Politics Module
Booklet.pdf`, copied from iCloud with `cp -p` and verified byte-identical (2,051,575
bytes, sha256 `1aea614e…18c9f4` on both sides). It is a University of St Andrews
module — IR4595 *Iran in World Politics*, Dr Eskandar Sadeghi-Boroujerdi, Semester 1
AY 2026-27: 42 pages, twelve weeks, assessed 50% essay / 50% exam. The readings run
in Appendix 1, pages 13–42. **No questions have been written and none should be** —
Gemini writes the banks from this document, Morad pastes them back.

**What the module actually contains.** Twelve teaching weeks, but only eleven carry
readings — Week 6 is Independent Learning Week and Week 12 is Revision Week. In order:
1 Revolution and the Islamic Republic (ideology, institutions) · 2 The Iran–Iraq War,
1980–88 · 3 Hybrid Regime, Elite Contestation and Factional Politics · 4 Guardians of
the Revolution (IRGC, political economy, the "subcontractor state") · 5 Iranian Foreign
Policy in Perspective · 7 The Axis of Resistance (Hizballah, sponsor–proxy debate) ·
8 Sanctions and the "Resistance Economy" · 9 Gender Politics · 10 Ethnic and Religious
Minorities · 11 Iran at War, 2023 to the present (nuclear balancing, Strait of Hormuz).
Appendix 1 ends at p.35 with a consolidated bibliography under six headings, ~60–70
entries, citation material only.

Two things worth carrying forward. **This is a politics and political-economy module,
not a cultural one** — the `فرهنگ و هنر` bucket would draw almost nothing legitimate
from it, which is fine since nothing forces a category into it. And the reading lists
are excellent material for the optional `book`/`author`/`page` fields on each clue,
which is exactly the "put the reading here" use the spec describes. The natural
categories fall out as: The 1979 Revolution · Khomeini & Velayat-e Faqih · The Iran–Iraq
War · Guardians of the Revolution · Factional Politics · Iran's Foreign Policy · The
Axis of Resistance · Sanctions & the Resistance Economy · Nuclear Iran · Gender & the
Islamic Republic · Ethnic & Religious Minorities · Reform & Elections — twelve, which is
exactly one complete single + one complete double round, so **the variety floor argues
for a second set of twelve**.

**Open:** whether a replacement
`assets/logo-wordmark.png` is wanted at all now that every edition stays Iranian (the
engine's art is already correct); and whether the class wants a Persian bank at all,
since the build hard-refuses an edition without one.

**The French flag, 2026-09-14.** Morad: *"why is the color coding like the French flag?"*
He was right, and it was the engine's own geometry rather than anything this fork added.
`.flagrule` is `linear-gradient(90deg, var(--green) 0 33.3%, #f4f1ea 33.3% 66.6%,
var(--red) 66.6% 100%)` — `styles.css:338–344` — which draws three colours as **upright
stripes side by side**. That is the French and Italian arrangement. The Iranian flag's
stripes run **horizontally**, so an Iranian flag drawn as three vertical bands is not a
flag of Iran at all; it is the tricolour of somewhere else in the flag's own colours.

Where it appeared, and what was done to each:

| surface | engine | course edition |
|---|---|---|
| `.flagrule` ×5 (lobby, board, clue, wager, results) | `90deg`, 4px | `180deg`, 9px (board 8px) |
| `.pill-primary::before` — every primary CTA's 1px hairline (`styles.css:434`) | `90deg` | `180deg` |
| `.rc-rule` — the round card's full-width beat (`styles.css:1544`) | `90deg`, 4px | `180deg`, 9px |
| the wordmark's ribbon | baked into the PNG | repainted to horizontal bands |
| the tile's band | side-by-side, show colours | redrawn, stacked |

Three of the engine's other `90deg` gradients are **left horizontal on purpose**:
`.option::before` (`styles.css:1025`) is the answer hold-timer, which has to empty along the
answer's reading direction; `.wager-range` (`styles.css:1191`) is a slider track, directional
by function; `.shine::after` (`styles.css:467`) sweeps as a focus highlight. A vertical
gradient on any of the three would be a bug, not a flag.

**Diagnostic worth keeping.** Chrome canonicalises `linear-gradient(180deg, …)` to
`linear-gradient(…)` with the angle omitted, but prints `90deg` verbatim. So in a
`getComputedStyle(...).backgroundImage` string, **"no angle" means correctly stacked**, and
any visible `90deg` means the horizontal tricolour is still in force. This is how every flag
check was adjudicated, and it matters because a 9px bar scaled down to 481px width *looks*
like green-left/red-right even when it is green-top/red-bottom. Measure, don't squint.

**The tile, drawn rather than generated.** GapGPT produced a tile but the Sotoon CDN 503'd
every delivery route for over an hour, so the installed art is deterministic PIL output.
The parameters are recorded here because they exist nowhere else:

```python
W, H = 960, 540
BASE, PEAK = (5, 9, 7), (20, 44, 31)        # near-black -> emerald
gw, gh = 96, 54                              # drawn small, then bicubic to size
cx, cy = gw * 0.5, gh * 0.42                 # glow centre, slightly above middle
f = 2.718281828 ** (-(dx*dx + dy*dy) * 1.35) # gaussian falloff, dx/dy normalised by
                                             #   (gw*0.40) and (gh*0.46)
d.rectangle([26, 26, 933, 513], outline=(44, 168, 100), width=2)   # emerald hairline
for y0, y1, c in ((466, 475, GREEN), (476, 485, BONE), (486, 495, RED)):  # stacked flag
    d.rectangle([96, y0, 864, y1], fill=c)
# GREEN, BONE, RED = (18,138,70), (244,241,234), (184,29,36)
```
960×540, md5 `b22354b49f73e12edaae3fb060f23734`. It is a deliberate sibling of the engine's
`tile-general.png` — same frame inset, same band geometry, same 960×540 — differing only in
plate and in whether the band runs across or stacks. The general tile's side-by-side band is
**untouched**, because the public build must stay byte-for-byte.

**The backdrop, installed and looked at.** `assets/stage-backdrop-course.png`, 2,266,592
bytes, md5 `fb8b1cb433826e9020f603b653672aa2`. A full-history Islamic Republic mural on a
dark vaulted exhibition-hall wall: Khomeini's portrait upper-left in official stencil idiom;
snow-capped Damavand, cypresses and a golden dome with two minarets centre; two fighter jets
and a cluster of missiles angled up-right; the Allah emblem on a flowing green/white/red
ribbon with sweeping nasta'liq; a wrecked tank lower-right; raised fists and a black flag
lower-left. This is the answer to *"even the backdrop should be more Islamic Republic
themed"* and to *"war and missiles alongside everything else — this is the full history of
the IRI."*

**Engine proven untouched this window.** `styles.css:338–344` is still `90deg` at
`height: 4px`; `find Web -newermt "-90 minutes"` returned nothing; `git status --porcelain`
shows only the modifications carried from the plan's earlier steps.

**Left as engine furniture, flagged for override:** `i18n.js:348–355` owns six bot seat
names — Mirza ChatGPT, Cyrus the Algorithm, Bot-ol-Molk, Clippy Khan, Nostradamus.exe, Shah
Mat. They appear in the verdict line ("Correct. Bot-ol-Molk 10M"). The course edition
overrides only the difficulty labels (The Fresher / The Pundit / The Realist / The
Archivist), not the names. Say so if the names should change; it is a four-line edit.

## The professor clears the edition chip — measured, not guessed

`edition.css`'s `--prof-lift` is the one dial that moves the professor's whole layer on the
title card. It was `54px`, chosen by eye. At 1024×768 the sprite is an 86×91 box and the
edition chip's eyebrow ("WHICH SHOW?") begins at y 672. At 54px the box ran y 601–692 — the
man stood **20px across the words that explain the chip**.

Raising it to 76px cleared the box by 2px, which looked like a fix and was not one: the
sprite carries `drop-shadow(0 10px 30px …)`, whose shadow reaches roughly 25px below the
box, so the smudge still crossed the eyebrow. **The lift is set by the shadow, not the box.**
`104px` puts the box at y 551–642 (31px of clearance) and a shadow-aware collision scan
(26px pad) returns nothing.

Two things were checked before settling on it, rather than assumed:

- The bubble rides up with the sprite, so it had to be proven harmless at the new height.
  It lands at x 37–344, y 418–541. The tagline starts at x 353 — **no overlap, 9px clear.**
  The left rail ends at y 273, far above. The only thing it touches anywhere is the language
  nav: 66×26px of the "English" pill's left cap. That is left alone on purpose — the layer is
  `pointer-events: none` so the pill stays clickable, and the pill's centred label stays
  clear of the bubble's edge, so it reads as a speech bubble in front of a control rather
  than a covered one.
- `104px` was reached from the shadow arithmetic, then confirmed by re-measuring, not the
  other way round.

**A stale-CSS scare that was not a bug.** The preview tab reported `--prof-lift: 54px` after
a rebuild that had provably written 76px (source and `dist/` md5-identical). Cause: the dev
server is `python3 -m http.server`, which sends no `Cache-Control`, so Chrome applies
heuristic freshness and served its own copy. A cache-busted `edition.css?v=…` showed the
truth immediately, and a plain reload afterwards picked the change up on its own. Worth
remembering when a `Course/` rebuild "doesn't take": bust the URL before debugging the build.

**The fold into `Course/`.** The sibling layout recorded above was undone on purpose.
This folder now lives **inside** the engine tree at
`~/Claude/Jeopardy - Iranian Edition/Course/`, and the folder it used to be —
`~/Claude/Jeopardy - Iran in World Politics Edition/` — does not exist. Every path in
this log that spells that sibling out is dead and is kept only as the record; the
paragraphs above carry pointers to here.

Why inside rather than beside. The merged build puts both shows in one app and rsyncs
the overlay over `Web/` at build time, so the overlay has to sit next to the tree it
overlays. `ENGINE` therefore collapses to `$HERE/..` — one level up, with no sibling
name left to get wrong. Secrecy is the other half: `Course/` is in the engine's
`.gitignore` (line 26), so the course banks and `BANK_SPEC.md` cannot reach the public
repo even by accident, while the build script still reaches the engine with a single
relative path. The public tree is untouched by this — same `app.js`, same 1,000 general
clues.

**That ignore line did not exist, and I nearly logged it as though it did.** Writing the
paragraph above, I asserted the folder was already ignored and cited `.gitignore:23` for
it. The citation was invented — line 23 is `__pycache__/`, and there was **no `Course`
entry in `.gitignore` at all**. So I checked instead of trusting: `git ls-files Course`
returned **0** and `git log --all -- Course` was empty, so nothing had ever been committed
and no bank had leaked — but `git status -uall Course` listed **68** paths a single
`git add -A` would have swept in, the two course banks and `BANK_SPEC.md` among them. The
folder was protected by nobody having run that command yet, which is not protection.
`Course/` is now ignored as a folder (`.gitignore:26`), not by a file list, and the count
is 0. The engine's own stubs — `Web/edition.js`, `Web/editions.js`,
`Web/data/edition_clues*.js`, `Web/edition.css` — stay untracked-but-trackable on purpose:
they belong in the public repo. The lesson is the one this log keeps teaching: a path git
has not been asked about is a path whose status is unknown, however confident the note.

**The chooser is a chip, not tiles.** The plan called for the second edition to be
revealed as tiles inside the splash after the language press. It was built as a corner
chip instead and that is the shape that ships: `#edition-swap` (`index.html:81`), whose
button carries the art and the name (`index.html:83-85`), wired at `app.js:1033-1071`.
A menu of one is not a menu, so the chip exists only when `getEditions().length > 1`
(`app.js:1034`) — in the public build it is not in the DOM at all and the splash is
exactly what it was. Pressing it re-skins the card **where it stands** rather than
leaving it: `setEdition(id)` fires `editionchange`, `paintSwap()` repaints the chip on
both `langchange` and `editionchange`, and the language press (`begin(lang)`) stays the
only way off the title card. Recorded here so it is not "restored" later by someone
reading the plan.

**Two smaller things landed with it.** The `build_edition.sh` title rewrite is now
edition-aware: it reads the display name out of `$SRC/edition.js`'s own
`name: { en: … }` declaration rather than mangling the folder name with `tr '_' ' '`,
because the folder is named for the filesystem while the declaration is the string a
player reads — and the rewrite is now conditional, so a build whose overlay declares no
name keeps the engine's title instead of being labelled for a second show that is not
there. A full rebuild is green and the built `index.html` carries
`<title>JEOPARDY! — Iranian Edition & Iran in World Politics</title>` with the matching
`og:title`. And the bilingual path block in `BANK_SPEC.md` was already corrected to
`data/edition_clues.js` / `window.EDITION_CLUES` — peer-authored, with a bolder warning
than my draft about shadowing the general bank, so the edit I went to make had already
been made.

## Reading the clues before dealing them (2026-09-14)

`Tools/check_bank.py` reads a bank's clues and fails on the two things a player notices
unaided: the answer sitting inside its own clue, and the same option offered twice. It is
the complement of `check_edition.py`, which proves a board can be *dealt* — six categories,
five rungs each, six doubles still reachable after the single round — and never reads a
clue. A gate wiring it into `build_edition.sh` as a second fatal pre-flight was written,
verified, and then **removed again the same day**. That sequence is the entry.

**Why it went in, and why it came out.** A peer asked for the gate. The same peer withdrew
the ask within hours, on two grounds: the sprite session invokes `build_edition.sh`
constantly and does not want the script changing underneath it, and a peer cannot authorise
work in a lane that is not its own. Both hold. The ask was never Morad's, so once it was
withdrawn nothing remained to hold the change in place — a gate on the build script is a
decision for whoever builds, not for a suggestion between sessions. The reversal cost the
gate and not the finding: the checker itself was never modified and runs by hand on any
bank, which is all the finding needed. What the gate did prove while it existed is that the
refusal landed before `rm -rf "$OUT"` — `build_edition.sh "Iran in World Politics"` exited 1
with `dist/Iran in World Politics/index.html` keeping its mtime — so anyone who wires it back
in can do so without risking a half-deleted build in the folder the preview serves.

**The course bank fails it: 16 errors, 8 in each language, every one `captain obvious`.**
No duplicate options. Measured by running the checker rather than taken from the relay that
reported it — same number, and worth noting a relayed figure was right for once. That is the
`Questions` session's bank to rewrite.

**The engine's own public bank fails the same checker, and nobody had run it.** 12
errors, 6 per language; read as distinct defects rather than lines, 6. Three English
clues print their own answer (`war_koveitipour_800` / 'Gharibaneh', `coldwar_cento_2000`
/ 'CENTO', `single_philosophy_of_isfahan_the_metaphysicians_800` / 'Sheikh Bahai'), and
three Persian clues offer a repeated option (`double_persian_gulf_tanker_war_400`,
`single_weve_got_elam_entary_evidence_1000_a`, `single_persian_flights_of_fancy_600_a`).
Each of the 12 is one of those six printed twice, because the `_encore` / Second Chance
twin carries the same text — so six edits clear all twelve. Not fixed here: rewriting a
clue is authoring work under `QUESTION_AUTHORING.md` and this is the public repo's
content. Recorded so a release does not ship a question that answers itself, twice.

**And the theme clips do not fire in Persian.** `--edition` reports, without failing,
that 138 of the course bank's categories reach none of the ten week clips: the `THEME`
keyword table in `edition.js` keys on English words, while the Persian bank's category
names are Persian. The professor's week intros play in English and stay silent in
Persian. That table is `edition.js`, so it is the sprite lane's — handed over rather
than patched. Worth deciding, since the recordings are English and silence in Persian may
be exactly right; the problem is that it is silence by accident right now.

**Not debris, for release purposes: `Web/net.js` and `Web/vendor/`.** Flagged as possibly
stray while surveying the release; a peer identified them and the wiring checks out on disk.
`index.html:541-542` load `vendor/peerjs.min.js` and `net.js`, and `app.js` consumes `Net.*`
at 22 sites from 3732 to 4266. They are the PeerJS online-table transport, untracked only
because online mode has not been committed. They belong in a release build and must not be
swept out with the strays.

---

## 2026-09-14 — the course bank plays, in both languages

**The fork's blocker was never the engine; it was the bank's shape.** `build_edition.sh`
already laid an overlay over a live `Web/` tree. What was missing was something to lay
over. Gemini's pass landed as `banks/gemini-pass-2026-09-14/iranian_jeopardy_bank.json` in
a **third shape** — nested `{en, fa}` per field — which is neither the archive's field names
nor the play file's, so nothing under `Web/` could read it. The bridge is
`banks/gemini-pass-2026-09-14/convert_to_edition.py`, and the two files it writes are what
the edition now ships:

| file | global | size | rows |
|---|---|---|---|
| `Editions/Iran in World Politics/data/edition_clues.js` | `window.EDITION_CLUES` | 830 KB | 693 |
| `Editions/Iran in World Politics/data/edition_clues_fa.js` | `window.EDITION_CLUES_FA` | 1.1 MB | 693 |

693 = 690 source rows + 3 finals, mirrored id for id across the pair. **Not one row of the
engine's own 1,000-clue bank was touched** — an edition is generated straight into the play
shape and keeps its own global, which is the whole reason the `EDITION_` prefix exists
(`BANK_SPEC.md` §"Bilingual").

**The subtitles are a checked fact, not a hope.** `theme` is not a display string;
`persianSubtitle` (`Web/app.js:215`) glues the category name to `cells[0].theme`, lowercases
the pair, and returns the first `PERSIAN_BUCKETS` keyword found as a **substring**, testing
the buckets in fixed order. A theme keyword therefore only lands where we want it if no
*earlier* bucket's word appears in the category name — and course category names are puns,
which is precisely where stray substrings live. The converter parses `PERSIAN_BUCKETS` out
of `app.js` by bracket scan and simulates that function exactly, so it knows before writing
which names hijack themselves. **Nine of 138 do:**

| category | wanted | the word that wins instead |
|---|---|---|
| ROMANCING THE REVOLUTION | سیاست و جامعه | `revolution` → تاریخ و انقلاب‌ها |
| HEROIC FLEXIBILITY EXERCISES | سیاست و جامعه | `hero` → مردم و چهره‌ها |
| DIVIDE & CARTOGRAPH | سیاست و جامعه | `art` → فرهنگ و هنر |
| BALLOTS AND BARRICADES | سیاست و جامعه | `barricade` → تاریخ و انقلاب‌ها |
| TIE-DYED IN THE REVOLUTION | فرهنگ و هنر | `revolution` → تاریخ و انقلاب‌ها |
| PROXY MUSIC | سیاست و جامعه | `music` → فرهنگ و هنر |
| STRAIT OUTTA YEMEN | سیاست و جامعه | `strait` → مکان‌ها و جغرافیا |
| SHRINE ON YOU CRAZY DIAMOND | سیاست و جامعه | `shrine` → فرهنگ و هنر |
| BONYAD EMPIRES AND PARALAWS | سیاست و جامعه | `empire` → تاریخ و انقلاب‌ها |

None of those is forced. Rather than write a theme the engine will not render, each falls
through to the bucket that actually wins — the subtitle the reader will see, not the one
the classification wanted. `BONYAD EMPIRES AND PARALAWS` rendering تاریخ و انقلاب‌ها on the
dealt board is that prediction confirmed against the live engine, which is the strongest
evidence available that the simulation matches the real function.

**The one defect the first write had: a trailing comma.** `emit()` joined the rows with one.
JS accepts it; `check_edition.py`'s strict parser does not, and the build refused. Fixed by
joining with `",\n".join(...)`. Worth naming because it is the class of failure this project
keeps hitting — the data was correct and the *serialisation* was not, so no amount of reading
the questions would have found it.

**69 + 69, both languages.** `check_edition.py` is green on the built edition: 69 complete
single categories and 69 complete double, in each language. `BANK_SPEC.md` §"The one rule
that will bite you" warns that a name qualifying in both rounds inflates both counts without
being playable; here the double-only pool — the names the single round cannot spend — stands
at 63 against a floor of six. Nothing reuses a name across rounds.

**Verified by playing it, which is the only verification that counts.** Driving a scriptable
Chrome over CDP (a scratch profile on :9222, distinct from the :9333 ChatGPT profile), the
shipped edition served from `http://localhost:8177/` reports

```
{"edition":"course","clues":1000,"edClues":693,"edCluesFa":693}
```

— the active edition is the course overlay and the engine's bank sits intact underneath it.
The **English board** dealt six course categories (WALTZING WITH ATOMS, ASSEMBLY REQUIRED II,
BONYAD EMPIRES AND PARALAWS, ASSEMBLY REQUIRED, WHERE IS MY VOTE, DUDE?, THE CASPIAN
EQUATION), rungs 10M→200M, each carrying a sensible Persian subtitle. A full clue cycle
renders end to end: the Waltz/deterrence clue, "10M toman", four options, the host's line,
the explanation, and the citation `Foreign Affairs · Kenneth N. Waltz · p. 2` — so
`book`/`author`/`page` reach the screen and do reach the student. The correct option rendered
at index **3** although the bank stores **0**, which is `shufflingOptions` (`Web/app.js:274`)
reordering at deal time.

The **Persian board** was seen too, not inferred: `document.documentElement.lang === "fa"`,
RTL layout, Persian chrome, Persian numerals (۱۰ میلیون … ۲۰۰ میلیون), and six Persian course
categories each with its own Persian subtitle. Bilingual is a property the build claims about
itself; this is the measurement.

**One concentration, recorded and not fixed.** The rendered subtitle spread over the 693 rows
is سیاست و جامعه 397 / تاریخ و انقلاب‌ها 186 / فرهنگ و هنر 75 / مکان‌ها و جغرافیا 25 /
مردم و چهره‌ها 10 — politics-heavy because the course is a politics module, and exactly one
category was classified P at all. That is the shape of the syllabus showing through, not a
bucket defect, and it is left alone.

**`BANK_SPEC.md` rule 12 was wrong, and is corrected.** It read "Vary which option index is
correct. Do not put the answer first every time." — which contradicts `CORPUS_BRIEF.md` §5
and `QUESTION_AUTHORING.md:187-191`, both of which say the index is **0 on every row, on
purpose**, because the balance is produced at runtime. The rule was not merely redundant, it
was backwards: it asked for work that `shufflingOptions` erases at deal time. Rewritten to
state the real rule and the reason. A stale cross-reference to "rule 6 above" (there are no
numbered rules in that section) went with it.

**Not re-recorded here, because these entries already stand:** `check_bank.py`'s 16 errors on
this bank (8 per language, all `captain obvious`) and the `edition.js` `THEME` table reaching
none of the ten week clips, so the professor's intros play in English and stay silent in
Persian. Both are in the entries above and neither was in scope for wiring the bank in.

**The log entry that is not a fix.** The board is playable, both languages, with citations,
out of a bank nobody could read this morning. What remains is authoring: the 16 `captain
obvious` rows, and the decision about whether silence in Persian is the intent.

## 2026-09-14 — the 16 `captain obvious` rows, rewritten by an external model

**Morad's instruction, in three parts.** "Can't we hand that off to GPT or something and
make it do it, since it's very smart?" — then, when I offered Gemini: "I think Gemini is
really bad — and it is relly hard to navigate." — then, naming the mechanism himself:
"Can't you use the Codex CLI?" — then the cost fence: "Just don't use Astra — because it
kills our usage limits. Decide which model to use; something that is smart enough but won't
empty us out so we can keep working."

**There are two Codex CLIs on this machine, on two different quota buckets.** Not one
rebranded other — separate binaries, separate homes, separate models, separate bills:

| | `codex` | `gapcode` |
|---|---|---|
| binary | `~/.local/bin/codex` | `~/.gapcode/bin/gapcode` |
| home | `~/.codex` | `~/.gapcode` |
| backend | the ChatGPT account (`auth.json`) | `model_provider = "gapgpt"` |
| model | `gpt-5.6-terra` | `gpt-5.6-sol` |

That is what made the fallback possible. Both shell functions force a cwd
(`~/.zshrc:50-51`, `_agent_enter`), so the job was driven by invoking the **binary** with
`-C` rather than through the wrapper.

**The model was chosen on his criterion, not by default.** GapCode/`gpt-5.6-sol` first,
because GapGPT is a separate bucket from the ChatGPT account he keeps exhausting; when that
bucket answered "You've hit your usage limit for GapCode. Switch to another model now",
the fallback was the Codex CLI on `gpt-5.6-terra` — its configured default, and two tiers
below `gpt-6-astra`, which is the one he banned. Neither call went near Astra.

**The defect class is the one a machine can catch.** `captain obvious` = the answer string
appears inside its own clue text. `check_bank.py` flags it as an `X`. Sixteen rows carried
it — 8 English, 8 Persian, across 13 ids (three ids were affected in both languages).

**The pass.** `build_payload.py` extracted the 16 rows and wrote a prompt that asked for
`clue_text` and nothing else: answer unchanged, no inflected/possessive/plural form of it,
no translation, no distinctive multi-word fragment; same length, same register, same rung;
Persian native; re-angle rather than delete when the giveaway is load-bearing; introduce no
new giveaway. The reply was one JSON object keyed `"<id>|<lang>"`.

**One row failed and was sent back.** `single_improv_600|en` came back still reading
"…the historic presidential election of May 1997" — which *is* the answer. Caught by
reading the output, not by a script, then fixed with a second narrowly-scoped call that
named the error and forbade the month and any year adjacent to "election". The two calls
cost 15,974 and 9,517 tokens.

**The merge is a gate, not a pipe.** `merge.py` re-reads every rewrite and **refuses to
write the bank at all** if any row is missing, mis-languaged, empty, unchanged, or still
contains its own answer. It would have blocked the bad `single_improv_600` row if I had not
already caught it by eye. Sixteen rewrites applied, all sixteen longer or shorter in the
same register, none longer than 293 characters.

**Before and after, measured.** `Tools/check_bank.py` on the rebuilt edition:
**16 error lines → 0**; warnings **661 → 205**. `Course/check_edition.py`: EXIT=0, 693 clues
per bank, 69 complete single categories and 69 complete double, 3 finals, both languages
able to fill a full board. `convert_to_edition.py` regenerated both shipped banks with its
own assertions intact (693/693, bucket assignments matched 138/138, the same nine forced
categories). `build_edition.sh` rebuilt the 22M dist. The 205 remaining warnings are
pre-existing and unrelated: the 0-index house-rule note, three English rows carrying
Persian script, and the `THEME` table reaching no week clip.

**One rewrite is weaker than the other fifteen, and is flagged not fixed.**
`single_oil_strikes_1000|en` now reads "…while schools and bazaars mounted nearly half, this
exact proportion occurred inside state agencies and public-sector institutions" — it no
longer leaks, but the arithmetic no longer parses cleanly. It is a judgement call for the
author of the bank, not a defect for a checker.

**The prompt that built this bank still names Gemini.** `BANK_SPEC.md`'s pipeline diagram
and its "Prompt to give Gemini" heading are now wrong about *who* runs it — the contract
itself (fields, ladders, buckets, the board floor) is unchanged and still correct. Corrected
in place to name a strong external text model rather than one vendor's UI.

**Addendum — the `Course/` ignore in the entry above is reversed.** Morad's rule, stated
plainly: "the only thing… that should be git ignored are the ACTUAL SOURCES + any kind of
actual PDF syllabus with course markings on them — that's it; the course and game within it
are fine." The distinction is **copyright, not confidentiality**, and a bank of questions
written *about* a reading is not the reading. So `.gitignore:26`'s blanket `Course/` is
gone, replaced by a comment; what stays is the pair of lines that are the real reason —
`Sources/` (line 16) and `**/Syllabus/*.pdf` (line 19). Read that pair rather than this
paragraph if they ever drift.

**What that means for today's work, and for the earlier entry's claim.** "`git status`
was clean for that directory, so it must have been committed" was wrong — it was clean
because the folder was invisible to git. `Course/` shows as a single untracked entry now,
and the sixteen rewrites exist only in the working tree. Nothing is at risk (the dist is
regenerated from the bank on every build) but **there was no version-control undo**, and the
earlier entry's 68-paths-would-be-swept-in warning is now moot: sweeping them in is the
intent. Nothing is staged or committed — that is his call, and the repo is public.

**One measurement closes the copyright worry the pending list carried.** The source bank is
4.0 MB across 690 rows and its `verbatim_passage` field totals **2,760 bytes** — not the
207 KB previously recorded — and neither shipped `edition_clues*.js` contains a `passage`
field at all (850 KB and 742 KB, no match). Whatever the 207 KB figure was, it is not this
file. The copyright-bearing artifacts remain the ~60-book `Sources/` corpus and the
course-marked syllabus booklet, both still ignored.

## 2026-09-14 — the theme clips: every board category now gets its week

His words: *"can you fix what needs fixing using the chatgpt cli - perhaps using the terra
model?"* Two things were outstanding from the status report, and one of the two turned out
to be my own error rather than a finding.

**The mechanism, read before anything was written.** `edition.js:557-560` lower-cases
`d.detail.category` and hands it to `theme()`, which walks `THEME` first-match-wins on
`indexOf`. Only the **category name** arrives — the row's `theme` field never reaches it. So
a pun name carrying no subject word can never match, and the old table was written under its
own stated assumption: "the bank is not written yet, so the match is on subject words and
not on names." The bank is written now, and its names are jokes.

**The pass.** 141 columns (69 single, 69 double, 3 final) against the ten topic clips, handed
to `gpt-5.6-terra` through the Codex CLI — `/Users/Morad/.local/bin/codex exec -m gpt-5.6-terra
-s read-only -C /tmp/c3po-map --skip-git-repo-check`, brief on stdin, 28.8 KB, 20,310 tokens,
exit 0. The brief gave the ten clips with a description each, `INDEX|CLIP_ID` line format,
and then one line per column: both pun names, the id slug, and the five answers. The **gate**
was count (141/141), no duplicate index, no invented clip id — it passed on the first reply,
so nothing was retried and no backend was switched.

**The reply was read, not trusted.** Ten rows that looked wrong on the name alone were pulled
with their five real clues. Eight held: the "deterrence" column really is the June 2025 war
(Muscat caught off-guard, Mashhad radar, ballistic performance data); `MINORITY RETORT`'s
clues are four of five about the war's treatment of religious minorities, so the war clip is
right despite the name; `STRIKE WHILE THE OIL IS COLD` is the 1978 oil strikes, so the
revolution is right. Two were overridden by hand:

- `NEITHER EAST NOR BEST` (`foreign`) — terra followed its majority-of-clues rule to the
  Iran-Iraq war; the column is named for non-alignment, its own id says `foreign`, and terra
  had already given the sibling `week5_east` column foreign policy. → `prof_18_topic_foreign_policy`.
- `THE PROXY PARADOX` (`proxy_paradox`) — terra sent it to the 2025 war while sending both
  `proxy` and `proxy_music` to the axis. → `prof_19_topic_axis_of_resistance`.

The rule behind both: the clip plays when the **category name** opens, so the label should fit
the name, not the average of the clues.

**Where it went.** A new top tier in `THEME`: 276 exact names (138 columns × two languages,
lower-cased to match the caller), with the old 41 subject-word pairs kept below as the
fallback and the comment rewritten to say so. The three Final categories are excluded on
purpose — the Final already has its own moment, and `ROUND_START` omits it for exactly that
reason.

**Measured after the rebuild.** 138/141 categories fire a clip **in both languages**, column
for column identical; the 3 silent are the Finals. All ten topic clips are reachable —
`prof_19` on 18 columns and `prof_23` on 3, and those two previously had *no* category that
could reach them at all. Before this pass: 49/141 English, 41/141 Persian, and only 3 of 12
clips in Persian. The Persian side now matches the English exactly, which the keyword tier
never could: it was matching English subject words against Persian pun names.

**A correction to my own earlier report, in the other direction.** `prof_05_correct_surprised`
and `prof_07_wrong_reading` are **not unreachable**. They are the second takes in `POOL.right`
and `POOL.wrong` (`edition.js:287-292`), published as `window.HOST_VOICE` and drawn by the
engine's shuffle bag (`app.js:538-557`) — the bag holds the whole pool, is exhausted, then
reshuffles, so both takes play. My "8 of 12 clips reachable" note had counted only the `THEME`
tier and mistook pool variants for dead clips. It was wrong on the way to the right answer:
the topic tier really was broken.

**Verified:** `node --check` on the source and on the built copy, `check_edition.py` green
(693 clues a side, 69/69 categories in each round), dist rebuilt at 22M with the new block in
it. **Not verified: the clips actually playing.** That is audio — it needs his ears, or a
browser session, and no dev-server slot was free this session. The wiring is proven; the
sound is not.

## 2026-09-14 — professor layer verification, and the deal-floor fixtures

**Plan verification, course build (professor layer).** All four sub-items of the phone check
are done and were read off a screenshot, not asserted blind: at 375x812 the clue text and all four
options stay legible and the verdict slab is complete once the bubble retracts, the board renders
6x5 with bilingual headers, `document.documentElement.scrollHeight (812) <= innerHeight (812)` (the
layer adds no scrollbar), and the viewport was reset to desktop afterwards. Persian is mirrored at
a >=900px viewport — EN `left:46.08 / right:988.43` against FA `left:986.07 / right:46.08` — while
`.prof-line` stays `dir="ltr" lang="en"`. Three cue orderings are proven from the network log: a
streak of three gives `04`/`05` and then `10` last (so the queued beat is not swallowed by the
verdict's `Sound.cut()`); a Final run fetches `13_final_jeopardy` at the reveal and a verdict clip
at the result, with none of `14`-`23` (so the category beat fires at app.js:1452 only); and a Final
clock running out fetches `08_timeout` through the `finishFinal` site, not just `showVerdict`.

Two things did not come out as expected, and are recorded rather than papered over. The results
screen's `win`/`loss` beats (`25`/`26`) stayed silent because that match ended in a tie — players 2
and 3 level at -100M — and both beats sit behind `finishMatch`'s `!tie` guard (app.js:2502, 2542,
2543). The firing case is therefore still unproven. And the third Final contestant produced no
`08_timeout` at all; the hypothesis is the same 650 ms race already proven for the last clue of a
round — `finishMatch` opens with `Sound.cut()` (app.js:2499) and clears the host-line timer the
verdict scheduled at 2490 — but it is unproven and should not be treated as settled.

**Deal-floor fixtures (plan step 8, proved by exit code).** `check_edition.py` already carried both
fixes: the anchored marker match (`\b` + marker + `\s*=`, line 62) with the prefix trap explained in
its docstring, and the disjointness check (`double_q - single_q`, lines 146-159). Three throwaway
fixtures were built under /tmp and run to confirm the exit codes: a disjoint 6+6 bank passes (exit
0); the same bank with Alpha's 1000 rung removed fails with the readable "only 5 single categories
carry all five values" (exit 1); and a bank whose only six double names are the same six that
qualify in single fails on the disjointness check *while both per-round counts read 6 of 6* — which
is the whole point of adding it (exit 1). The anchoring was proved separately: a file holding only
`window.EDITION_CLUES_FA` now reports "English bank will not parse" instead of silently handing
back the Persian array. The real edition passes as it stands — 693 clues per bank, 69 of 69
categories qualifying in each round, 3 final clues, exit 0. Fixtures were scratch and are deleted;
`build_edition.sh` step 9 (the edition-aware `<title>`/`og:title` rewrite, keyed off the name the
overlay declares) was already in place and needed nothing.

**Flag.** `Web/app.js` is being edited by a concurrent session. It measured 177,748 bytes at one
point in this session and 177,989 with an mtime 22 seconds later, which produced a flapping `cmp`
against the restored dist. The build artifact is a copy and lags the source, so the dist now trails
by one engine revision; any course-dist check before the next rebuild reflects a stale engine. The
retuned bot accuracies (0.60 / 0.75 / 0.88 / 0.95 at app.js:3330-3336, `NUDGE` at 3343) are intact
in the engine source.

## 2026-09-14 — the theme-clip "gap" was a checker bug, not a bank gap

**Two peer sessions reported the professor's week clips as mostly unreachable** — "17 of 138
English", "0 of 138 Persian", with `prof_19_topic_axis_of_resistance` and
`prof_23_topic_iran_at_war` declared dead in both languages. I measured it myself before touching
anything. The report is stale, and in both directions: it understates the coverage and it
misidentifies the cause.

`Course/Editions/Iran in World Politics/edition.js` was rewritten at 19:08 today, after the peers
read it. The THEME table now opens with a two-tier header comment (311-324) and carries a row for
every board category in **both** languages, named as the bank spells it and lower-cased because the
caller lower-cases. Counting by mirroring the engine's own matcher (`theme()`, 852-857 — plain
substring, first match wins, a miss returns `null` with no clip and no warning) over each built bank:

- English: 138 categories, **138 reach a clip**, 0 reach none.
- Persian: 138 categories, **138 reach a clip**, 0 reach none.

The three categories per language that reach nothing are the three **Final** clues — `PEACE, WITH A
HEMLOCK CHASER`, `THE BOOMERANG CLAUSE`, `THE JURIST'S BURDEN` and their Persian pairs. That is the
documented design, and it holds twice over: the header says the three Final categories are left out
on purpose, and the category beat is wired at app.js:1452 only and never at the Final reveal (2223),
so those names could not fire a clip even if they had rows. Both "dead" clips are alive with several
explicit rows apiece. No edit to `edition.js` was needed and none was made.

**The real defect was in the tool.** `Tools/check_bank.py`'s theme-reach check built its keyword
table with `re.findall(r"\[\s*'([^']+)'\s*,\s*'([^']+)'\s*\]", block)`. A row can only match from its
`[`, so a key containing a JS escape (`['all the president\'s mullahs', ...]`) never completes the
pattern and the row is **dropped whole** — not mangled, dropped. Every category whose name carries an
apostrophe then has no key left and reads as unmatched: precisely the three the checker flagged
(`ALL THE PRESIDENT'S MULLAHS`, `HEZBOLLAH'S WINNING HAND`, `SHI'A GEOPOLITICS GOES ARABIC`), all
three of which have live rows in the table. It was blind in the other direction too, and it
hard-coded the belief — true before the 19:08 rewrite — that the table keys on English words only,
so it excused every Persian miss as a fact of the design.

Fixed: the row pattern now matches the escape (`(?:[^'\\]|\\.)*`) and each key is read back through a
small `unjs()`, and the English-only assumption is gone so both banks get the same test. Proved on the
live edition: **138 of 138 English, 138 of 138 Persian, 0 miss, "OK — no errors."** The file is
untracked in git, so no tracked file moved; both peers were told, so we don't each edit it.

Also corrected with both peers: the claimed `Tools/check_bank.py` pre-flight in `build_edition.sh`,
with a `SKIP_BANK_CHECK=1` bypass, does not exist. The 146-line file's only gate is line 92,
`python3 "$HERE/check_edition.py" "$SRC" || exit 1`.

## 2026-09-14 — public build regression, the last verification item on the plan

Engine on 8788, serving `Web/` directly. Every public-build check the plan names:

- **Registry reads one entry.** `window.getEditions()` returns an array of length 1 — id `general`,
  fields `id/name/tile/banks`. The accessor is a function, not a global object: `editions.js`
  publishes `registerEdition/getEditions/setEdition/getEdition` and there is no `window.EDITIONS`,
  which is what the plan's prose assumed. Worth knowing before anything greps for it.
- `#prof-layer` is absent from the DOM.
- The chooser markup does exist in `index.html` (81-87) but carries `hidden`, its art `<img>` has no
  `src`, and its name span is empty — no visible chooser, no dead image path.
- Zero failed requests, zero console output.
- The splash still fetches `assets/audio/opening_challenge.m4a`, so the course CUE table did not
  substitute it.
- The `HOST_FALLBACK` path holds. `window.HOST_VOICE` and `window.HOST_CUE_MAP` are both `undefined`;
  a direct `Sound.hostLine('lockout')` fetched `wrong_08_mashallah_you_have_opinions.m4a`, i.e. the
  requested kind resolved to the `wrong` pool exactly as it did before the edition machinery existed.
  `timeout` sits on the same table line and shares that target.

**Not run, deliberately: the full offline regression** (both languages, a 6x5 board, a Daily Double,
single-to-double, the Final, results). That tests the engine at large rather than this change, and
`Web/app.js` is being rewritten by a concurrent session — 1550 changed lines in the working tree
right now — so a pass or a fail would describe someone else's half-finished edit. It should run once
those edits settle, or against the built dist, which is a frozen copy.

**Divergence recorded, not fixed.** Plan step 4 asked for the chooser to be "rendered from the
registry into JS, not hard-coded in markup," so the course tile could leave no dead path in the
public build. What shipped is a single swap button naming the *other* edition, hard-coded in
`index.html`, with JS filling its `src` and label. The plan's stated reason is satisfied anyway — the
`<img>` ships with no `src`, so nothing can 404 — and the run above proves it. But it is one toggle
rather than the pair of tiles the plan described. Against the user's own words ("a nice square or
chic circle with an image in it saying 'Iran in World Politics' edition") there is a name and an
image, so it reads as an acceptable substitute. Recorded so the choice stays visible.
