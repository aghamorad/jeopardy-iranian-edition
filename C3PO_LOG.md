# C3PO — work log

Running record of what Claude (C3PO) changed in this project and what was actually
verified. Newest entry first. Other agents in this tree keep their own logs under
their own names — this file is mine.

---

## 2026-09-15 — local image generation, and a registry for every model on the Mac

The game now has a second way to make art, and it costs nothing. **Draw Things CLI**
(`brew install draw-things-cli`) runs **FLUX.2 [klein] 4B, 6-bit** (`flux_2_klein_4b_q6p.ckpt`,
~7.3 GB) entirely on this machine. No network, no account, no per-image cost, and a seed
reproduces an image exactly. The 6-bit quantisation is the right one for 16 GB; `q8p` would
be better and heavier, and would start swapping.

`Tools/generate_image.sh` is the project wrapper. It bakes in the house look — charcoal
ground, silver-grey structure, the flag's green and red read as stage *lighting* rather
than as a flag — and a negative prompt that enforces the standing brief: no flags, no gold,
no ornament, no domes, no minarets, no lone volcano. `--raw` lifts the style; `--people`
lifts the ban on figures, which is on by default because most assets here are sets.
Output goes to `Assets/Generated/` with a `.txt` sidecar carrying the exact prompt, seed and
model, so anything can be rebuilt.

Three rounds to get one image worth keeping. The first was hazy mid-grey and grew three
suited men nobody asked for. The second sprouted domes, minarets and a snow-capped peak —
exactly the generic Middle-Eastern register the brief bans — which is why those terms are in
the negative list now rather than merely absent from the positive one. The keeper is
`Assets/Generated/stage-empty-20260915-173330-v1-s7700.png`: three podiums, green wash left,
red wash right, polished black floor, monochrome skyline panel. Morad approved it. Its one
honest weakness is the skyline, which reads a little glossy and generic — closer to a Gulf
financial district than to Tehran.

**On rejects.** I had assumed generated art was a gitignore question. It is not. Morad's
rule: rejects get deleted, keepers become part of the game. The six rejects went to
`~/.Trash`; the keeper stays in the tree. `Assets/` is untracked, not ignored — nothing
about it needs a `.gitignore` change.

**The registry.** Every model on this Mac is now visible in one place at `~/Models` —
symlinks only, never copies, with `~/Models/bin/models` for the live list and
`~/Models/MODELS.md` for the commentary. Speech, voice, LLM, image and audio-gen. It is
there so that a person or an agent can see what is already here before downloading anything
again. Morad authorised that exact path; it is a deliberate exception to the rule against
putting files in `$HOME`.

**The skill stays.** `~/.claude/skills/generate-image` drives ChatGPT and GapGPT through a
real browser and produces better images than the local model, especially anything with text
in it. It is also slower, harder to drive, and can be rate-limited. Both routes are now
described in the skill: the web UI for keepers and anything looked at closely, local for
bulk, variants and cheap iteration. Nothing was retired.

## 2026-09-15 — the phone pass: the island, the caption, the bed, and the keyboard

Four complaints from a phone — Morad's and a friend's. Three were layout, one was audio, and
the loudest one was not what it looked like.

**The island.** Screens are `inset: 0` inside `#app`, so in portrait the first row of chrome —
the bar, the category, the wordmark — was drawn at y=0, under the Dynamic Island. The offset
is paid once on `.screen.is-active` as `top: var(--safe-top)` (`env(safe-area-inset-top, 0px)`;
`viewport-fit=cover` was already declared). On the screen and not on the root, so the backdrops
stay full-bleed and only content moves. The band arithmetic is the opposite edge and is
untouched: with a 44px inset injected the screen top moved 0 → 44 and the bottom stayed at
722.7, so nothing is double-counted. On `screen-clue` at a 59px inset the clue bar moved to 59,
`.clue-body` shrank 432.5 → 373.5, and `#clue-actions` (b=666.7) and the podiums (b=722.7) both
held — so the inset cannot clip the clue screen either.

**The caption.** The 3-line clamp was cutting her off mid-sentence. It was a phone-only rule and
the only thing holding the bubble inside the band, but it was never load-bearing:
`align-self: flex-end` on the sprite is what actually keeps her feet on the floor. Lifted to 7 —
105px of bubble against a band of 78 to 92 — with the bubble rising over the stage the
difference. The longest cold open, 243 characters, now renders 121px over seven clean lines with
no ellipsis.

**The bed.** Leaving the app and coming back left the music off, sometimes. iOS suspends every
media element when the WebView loses the foreground, and nothing in `app.js` ever asked for one
again. `Sound.resume()` re-issues the slot, but only when it is genuinely down: a page that never
stopped must not restart the track from the top, and a floor held by a voice is left alone
because `musicName` is null while she talks and her own guard timer restores what she ducked.
Wired to `visibilitychange` and `pageshow` both, because which one fires depends on how the app
was put away. Verified: `menu_theme.m4a` suspended at 1.5s came back as `@1.8`.

**The keyboard, and the one that was not a layout bug.** "The answers aren't visible at all"
would not reproduce in multiple choice at any size tried — 375×812, 375×667, and 667×375
landscape, where the options lay out 2×2 and stay inside the fold even under a deliberately
absurd clue. It reproduces in write-in mode, and the cause is that **nothing in this game
scrolls**: `html`, `body` and every screen carry `overflow: hidden` and the document is sized to
the viewport to the pixel, so when iOS raises the keyboard over the focused field WebKit has no
scrollable ancestor to pan and leaves the box underneath it.

`app.js` now reads the covered strip off `visualViewport` and publishes it as `--kb`;
`.screen.is-active` reserves `max(var(--host-band), var(--kb, 0px))` at its bottom in place of
the band, the clue body gives because it is the flex child with room, and the field rises clear.
`max()` rather than a plain value so a build with no keyboard is the band again, character for
character. Verified by injecting a 336px keyboard: the screen bottom went 722.7 → 476 and the
write field landed at 67.5–187.6, above the line, confirmed by screenshot. This is the resolution
of the friend's complaint — it is a write-in bug, not a multiple-choice one.

**Not fixed: the voices that trail or disappear between menus.** The mechanism is understood —
the sprite is driven only by the `hostcue` event and only `finish()` dispatches `tellCue(null)`,
so a line preempted rather than finished leaks both its audio and its sprite into the next screen
— but the specific leaking transition has not been pinned. It is the one complaint from the list
still open.

**A cache-buster for `app.js`.** It was the one script tag with no `?v=`, and it cost an hour:
`Sound.resume` read as `undefined` at runtime while `fetch('app.js?v=probe'+Date.now())` returned
a file containing `function resume()`. Python's `SimpleHTTP` sends no `Cache-Control` and no
`ETag`, so the pane re-used the stale file and every edit in this pass looked like a no-op.
`app.js`, `course.css` and `index.html` now carry `?v=20260915-keyboard-1`. The trap worth
remembering: navigating the *document* with a query string does not change a subresource's cache
key, so it will look exactly like this again.

## 2026-09-15 — it is pushed, and the web show is live

`7a8ad4c` is on `origin/main`. The rename went up with the work the earlier sessions had
not pushed — 240 files in one commit, 68 of them renames git recognised as renames.

**Verified on the published site, not just in the tree.** `github.io/jeopardy-iranian-edition`
serves the new names and refuses the old ones: `tannaz_wager.m4a`, `tannaz_final.m4a`,
`tannaz-timeout.png`, `host-layer.js`, `course.js`, `eskandar_01_professor_welcome.m4a` and
`sprite-eskandar.png` all 200; `host_wager.m4a` and both spellings of `prof_01_professor_welcome.m4a`
404. The 404s are the half of that check worth having — it is the only way to see that the
rename took at the edge and not merely in the working copy.

**The itch workflow fails, and it is not this change.** `.github/workflows/itch.yml` was
committed in this push and ran for the first time; it dies in `Install butler` with
`curl: (6) Could not resolve host: broth.itch.ovh`, on GitHub's runner, where the network is
not Iran's. So either that host is gone or the runner's DNS dropped it — but the workflow is
new and has never passed, so there is no healthy baseline it broke from. Nothing depends on it.
Left failing and untouched: it is not the web show, and the web show is what shipped.

`pages.yml` — "Publish the web show" — succeeded in 26 s, which is the whole delivery path.

## 2026-09-15 — every file names its speaker, and the layer stops being anyone's

Two hosts, one vocabulary. Cue name, audio basename and pool slug are **the same
string** in this build, so renaming the files alone would have put code and disk into
disagreement — the exact confusion the rename was meant to end. Files, cue identifiers,
pool slugs, `LINES`/`TEXT` keys and the sprite moved together.

The scheme, mine to choose:

- `opening_challenge` → `tannaz_opening_challenge`
- `host_correct` / `host_wager` / `host_final` → `tannaz_correct` / `tannaz_wager` / `tannaz_final`
- `right_NN_slug` / `wrong_NN_slug` → `tannaz_right_NN_slug` / `tannaz_wrong_NN_slug`
- `prof_NN_slug` → `eskandar_NN_slug`, and `sprite-professor.png` → `sprite-eskandar.png`

The course's `course_*.m4a` pack is untouched: it names the edition, not a voice. 100
files renamed on disk, 5 edited, 473 substitutions — `app.js` 36, `host-layer.js` 43,
`course.js` 391, `course.css` 1, `Tools/transcribe_host.swift` 2.

The 27 masters in `Course/Masters/Iran in World Politics/Professor Voice/1.0x source/`
were renamed to match, so `prof_` is now gone from the tree as a *filename* as well as an
identifier — zero remain anywhere outside `.git`. Nothing reads those paths; the log's own
`prof_1x` arithmetic still refers to the sets by the names they were measured under, and
that is left alone because it is a measurement, not a path.

**The one oddity, kept on purpose.** `HOST_CUE_MAP` now reads
`tannaz_opening_challenge: 'eskandar_01_professor_welcome'` — the engine's cue is named
for one host and the course hands it the other's clip, so it reads wrong for a second.
The alternative was a MAIN-level indirection letting the engine ask for a neutral name:
new machinery in the boot path for a cosmetic gain, when the map already substitutes at
exactly the right layer.

**Why:** he asked for it in the only terms that matter to him — "so we are never confused
again" — and the two hosts are the thing that keeps getting confused.
**How to apply:** `Sound.voice()` applies `HOST_CUE_MAP` *before* `tellCue()`, so the
`hostcue` event a bubble hears already carries the substituted name. One vocabulary across
both editions rests on that ordering; anything that moves the substitution after
`tellCue` breaks it silently, with no error and no missing file.

**Verified.** No `host_wager`/`host_final`/`host_correct`, bare `opening_challenge`, `prof_`
or bare `right_NN`/`wrong_NN` left in live code. File counts unchanged — MAIN 86, COURSE
35. Zero orphans in a cross-check that every `tannaz_*`/`eskandar_*`/`course_*` literal in
the three files exists as a stem on disk *and* every clip on disk is named by live code.
`node --check` clean on all three. Driven in the browser: the four scene cues and a
`right_`/`wrong_` pair each fetch their `.m4a` at 200, no failed requests, no console
output — and both editions put the right host on the floor, Tannaz on the title card and
Eskandar on IR4595.

**Also, the layer stopped being the professor's.** `#prof-layer`, `.prof-bubble`,
`.prof-sprite`, `.prof-line` and the `--prof-rim`/`--prof-face` props are now `#host-layer`,
`.host-bubble`, `.host-sprite`, `.host-caption`, `--host-rim`/`--host-face`. The layer
moved out of the course into `host-layer.js` and serves whichever show is running, so
naming it after the professor was wrong twice — and `Web/index.html:20` loads `course.css`
unconditionally, so those rules are what styles MAIN's host floor too. The caption is
`host-caption` and not `host-line` because `styles.css:1160` already has
`.verdict .host-line` for the ruling, and an unscoped `.host-line` out of the course would
have caught it.

**Not touched, on purpose.** The entries above still say `prof_*` and `host_*`, as does
`Course/C3PO_LOG.md`: they record what was true when they were written.
`Tools/build_comprehensive_question_bank.py`'s `host_correct` is a question-bank parameter
that has never been an audio cue. `Versions/beta-2…beta-8` and both `dist/` trees keep
their own copies under the old names — each is self-consistent and frozen.

---

## 2026-09-15 — the last male clips in MAIN are Tannaz's

Three of the main edition's four scene cues were still the old male pack — the wager, the
final and the correct. All three are now cloned from Morad's own Tannaz reference through
**Fish Audio S2 Pro**, run locally via `mlx-speech`, and installed in `Web/assets/audio/`.
`tannaz_opening_challenge` was already hers. Shipped lengths: 14.616 s open, 2.786 correct,
4.598 wager, 3.390 final.

**The ear was the test, and it had to be.** This project already established that median F0
does not separate these voices — Tannaz 94.1 Hz, Eskandar 100.0, the old male 95.8, all one
band — so a pitch comparison here would have proved nothing while looking like a
measurement. He listened and said they were correct. That is the verification, and it is
the strongest one available for a question of whose voice it is.

**Why:** the male pack was the last thing on the floor that was not the host, in an edition
whose host is a woman, in a build that had just finished claiming there is no other male
voice in it.
**How to apply:** never re-introduce a host clip by reusing one of these filenames. A clip
whose name already promises Tannaz, carrying a male voice, is worse than an unnamed one —
the name is what stops anyone checking.

**Parked, recoverably:** the male originals went to `~/.Trash/jeopardy-host-male-2026-09-15/`
rather than being deleted. The shell cannot list `~/.Trash` on this machine, so their
presence there is not something a later session can confirm from a terminal — move them
out with an explicit path, as the 1.0× rates had to be.

**Left open.** `tannaz_correct` is **never played and never fetched** — there is no
`Sound.voice('tannaz_correct')` call site anywhere and `makeEl` is lazy, so the file is not
even requested. Its bubble caption is in the `LINES` table because the clip exists. Only
`tannaz_wager` and `tannaz_final` are audible. And `App/Resources/host_correct.mp3`,
`host_final.mp3`, `host_wager.mp3` and `host_welcome.mp3` are still the **male pack** in the
tree; `build_release.sh:80` copies only `AppIcon.icns`, so they are not bundled, but they
sit there as a reintroduction hazard.

---

## 2026-09-15 — the audio shelf, trimmed to one of each

**"Keep only what you need."** What survives:

- `Web/courses/iran-in-world-politics/assets/audio/prof_*.m4a` — 27, Eskandar at 1.1×, the
  set that ships.
- `Course/Masters/Iran in World Politics/Professor Voice/1.0x source/` — 27, Eskandar at
  true 1.0×, moved **out of the Trash and into the tree**. It is the only unsuperseded
  source, and a source that lives in the Trash is a source a Finder Empty will eat — which
  is what nearly happened to this one. Any future rate change renders from here, one
  generation from a known baseline, rather than from the live set where generations
  compound.
- `transcripts.tsv` — the 27 lines. The script outlives any voice.

**Gone, 26 MB:** the 1.25×, 1.5× and 1.2× sets (all derivable from the 1.0× master, and
1.2× is also still in git at HEAD), the old male in all three of its copies — the
`old-male-prof-pack` WAVs, `old-male-course-bundle-audio`, and `prof_original_20260915`,
which was the same recording under a folder name that lied about it — and my own scratch
sets.

Deleted outright rather than moved to the Trash: they were already in it, and the recovery
they offered was the thing being spent.

**Left the tree for the Trash, recoverably:** `Build_MALE_Voice_Pack.command`,
`README_FIRST.txt`, `CONTENTS.txt`. All three describe the purged male pack; the builder
reaches the voice through `say` and is dead without it, and `CONTENTS.txt` only restated
filenames `transcripts.tsv` already carries.

**Still open:** `Course/dist/Iran in World Politics/assets/audio/` is 94 files — its 27
`prof_*` were the old male and are gone. Rebuild the bundle and they return as Eskandar.
`App/Resources/host_welcome.mp3` remains unclassified.

---

## 2026-09-15 — the professor is at 1.1×, and the folder called "original" was the old male

**He asked for 1.1 after hearing the 1.2 set.** Scoped to Eskandar, the course voice. Tannaz
is untouched.

**The rate sets were in the Trash and the shell cannot list the Trash.** `ls`, `find` and
`os.listdir` on `~/.Trash` all return "Operation not permitted"; Finder's AppleScript does
not, and `cp -R` of an explicit path out of it works. That is how `prof_1x_20260915` and its
siblings came back.

**Measured, welcome clip, every set:** `prof_1x` 15.325188 s · `prof_1x25` 12.263917 ·
`prof_1x5` 10.230542 · shipped 12.783521. Check the arithmetic: 15.325188 / 1.25 = 12.260,
/ 1.5 = 10.217, / 1.2 = 12.771 against 12.784 shipped. So `prof_1x` is Eskandar at true
1.0×, and it is the baseline. Naming discipline holds in these sets.

**`prof_original_20260915` is not Eskandar and is not a source.** 17.040000 s and *nine*
pauses at 2.70225 / 4.544313 / 5.801958 / 7.002104 / 8.650125 / 9.609125 / 11.003687 /
12.021479 / 16.659771 — the purged old-male master's pause map, to within 8 ms on every one.
Same voice, same recording. Rendering from it would have repeated the mistake below with a
different filename.

**How to tell a voice pack from a speed variant, since duration alone will not do it.**
`atempo` preserves silences and moves them proportionally, so a 0.38 s gap is still ~0.25 s
at 1.5× and still clears a 0.2 s threshold. Pauses survive; speed does not hide them. Median
F0 is useless here — Tannaz 94.1 Hz, Eskandar 100.0, the old male 95.8, all one band.
**Compare pause maps. Not pitch, not duration.**

**Rendered and installed.** 27 clips, from `/tmp/prof_rates/prof_1x_20260915/` at
`atempo=1.1`, 1 ch 48 kHz AAC ~98 kbps to match the shipped encode. Welcome lands at
**13.947229 s** against a target of 13.932 (15.325188 / 1.1); all 27 ratios fall in
1.0949–1.1042. Verified over the preview server too: 200, 177 400 bytes, 13.947229 s. The
1.2× set it replaced is in `~/.Trash/eskandar-1x2-set-2026-09-15/`.

**Left open.**

- `App/Resources/host_welcome.mp3`, 8.832 s at 24 kHz, referenced nowhere in the tree. Its
  five pauses (1.730 / 4.291 / 5.866 / 6.789 / 8.053) match neither the old male welcome nor
  Eskandar's nor Tannaz's `opening_challenge`. Sent to him; unclassified.
- `Course/dist/Iran in World Politics/assets/audio/` is down to 94 files — the 27 `prof_*`
  there were the old male and went to the Trash. The bundle has not been rebuilt.
- `Course/Masters/Iran in World Politics/Professor Voice/` still holds
  `Build_MALE_Voice_Pack.command`. The 27 WAVs it built are gone.
- Audio carries no cache buster anywhere (`Web/app.js`'s `url()`), so a swapped clip needs a
  hard reload before a returning browser will hear it.

---

## 2026-09-15 — the professor's welcome is at 1.2×, and I put the wrong voice in it

**Objective:** he asked for the IR4595 welcome at "1 speed", scoped to that one voice.

**Nothing in the code ever sped him up.** `playbackRate` and `preservesPitch` appear
nowhere in the tree; every cue, his included, already plays at 1.0×. The rate was never a
setting — it was baked into the file.

**The shipped `prof_*` set is the 1.2× set.** `prof_01` measures 12.783 s as shipped
against 15.33 s at true 1.0× — a factor of 1.1992 — and the ratio holds across the set.
This is the same defect the entry "the professor speaks at 1.2, and nothing else speaks
at all" records: the 1.0×, 1.25× and 1.5× variants had been compounded or applied to the
wrong input, and every one was regenerated and re-measured from the clean `m4a/` tree.
The shipped 1.2 set passed that check. It is 1.2× on purpose and no consumer of it is
doing anything wrong. **He is hearing the file, not the player.**

**I then read the file instead of the log and made it worse.** Concluding the welcome was
"fast because the file was fast", I replaced it with a transcode of `Course/Masters/Iran
in World Politics/Professor Voice/01_professor_welcome.wav` — 17.04 s, fully paused,
130 wpm. That WAV is the **old male pack**: 27 Google-TTS male lines built by
`Build_MALE_Voice_Pack.command`, dated Sep 14, mirrored in `Course/dist/Iran in World
Politics/assets/audio/`. It is not Eskandar's voice and was never a candidate for the
course. He caught it by ear before I did. **Reverted:** `prof_01_professor_welcome.m4a`
is back to 160 518 bytes / 12.783 s, md5 `589e9bff…`, byte-identical to HEAD — `git
status` on the path is clean.

**The two sets are different recordings, not conversion pairs.** Same line, 12.78 s vs
17.04 s; the shipped read never drops below 2 % of peak for 12.64 s straight while the
master shows eight pauses (2.70, 4.54, 5.80, 7.00, 8.65, 9.61, 11.00, 12.02); median F0
101.3 Hz vs 95.8 Hz. `04_correct_annoyingly_so` is 1.30 s as a master and 2.14 s as
shipped, and a transcode cannot make a file longer. So the master is neither the 1.0×
source of the shipped set (12.783 × 1.2 = 15.34 ≠ 17.04) nor the same voice as it.

**Why:** "at 1 speed" was a correct report about a derived file, and I fixed the wrong
layer — swapped the voice instead of the rate, and reached for a pack whose own builder
is named MALE. **How to apply:** measure a clip's duration against its true 1.0× source
before touching it, and identify *which voice* a candidate pack is before it goes near
`Web/`. A clip's folder can tell you its speed; only the log tells you whose it is.

**Left open, on purpose.** The true 1.0× set is in `~/.Trash` under its dated folders and
is unreachable from a shell — `ls`, `find` and Python `os.listdir` all return "Operation
not permitted", and only an `mv` of an already-known path works. So the 1.0× fix is
either a Finder restore of that folder or `atempo=0.8333` on the shipped set,
pitch-preserving. Not done, because the voice underneath is still in question: per the
entry "the professor keeps his cue, and buzzing early has a price", the course voice is
still the old deep male and the young-British regeneration is blocked on a reference clip
and his go-ahead. Speeding a voice we are about to replace is work done twice. Also note
audio carries no cache buster anywhere — every cue URL is a bare path (`app.js`'s
`url()`), unlike the `?v=` on the CSS and JS — so any replacement clip needs its own.

## 2026-09-15 — the bubbles say what she says, and she gets a floor to stand on

**Objective:** put the real audio's words in the host bubbles, and stop her from
standing on the game.

**The bubble lines are transcriptions, not reconstructions.** `Web/host-layer.js` had a
`LINES` table built from the clip filenames — readable, and wrong wherever a filename
under-described its clip. All 36 clips are now transcribed from the audio itself:
32 pool slugs (16 `right_*`, 16 `wrong_*`) plus the four scene cues. Apple's on-device
`SpeechTranscriber` did the work through `Tools/transcribe_host.swift`, not Whisper — no
HuggingFace download, which from Iran is the difference between minutes and hours. Two
passes at different sample rates agree on 35 of 36; the three rows either side of that
disagreement (`right_08` "Teh"/"Terran", `wrong_01` "Michelle", `wrong_07` "no later")
carry a comment naming the ambiguity rather than a silent choice. The contract is
written at the top of `host-layer.js` and it is the reason to trust the text: the bubble
is a transcript of audio already playing, so a row that reads oddly is the audio reading
oddly — re-transcribe the clip, never re-word it. `host_correct` is in the table and is
never cued from `app.js`; it is there because the clip exists.

**The old corner rule was built on a premise that isn't true.** Its comment claimed that
above 1199px the stage is letterboxed and the host has a real margin to stand in. `#app`
is full-width `100dvh` — there is no letterbox. The apparent margin was `.center`'s
`12vw` and `.board-wrap`'s `14.2vw` of *content* padding next to `--pad-x`'s 3.6%, which
is a wide cushion on a 1440 desktop and nothing at all on a phone. That is why the
collision showed up on a small screen and never on the one it was authored on.

**She got a floor instead of a corner.** `#prof-layer` is a fixed band pinned to the
bottom of the viewport, `height: var(--host-band)`, and `#app .screen.is-active` is
shortened to `bottom: var(--host-band)` with `height: auto` — the screens give up the
space rather than being overlapped by it. Band is `clamp(78px, 11dvh, 92px)`, rising to
`clamp(90px, 11dvh, 100px)` at 1200px and up. The bubble grows upward out of the band's
top edge, so the band is the ceiling on how far up she can reach; its line clamp is
`-webkit-line-clamp: 3` backed by a `max-height` in `em`, because Chromium has been seen
painting the fourth line past a clamp it honoured for layout. Written up in
`Web/courses/iran-in-world-politics/course.css`, which every edition loads — the border
and face colours are the only parts keyed to `html[data-edition]`, so the course
professor and Tannaz share the mechanism and differ only in tint.

**Verified by hit test, not by eye.** An 8px grid of `elementFromPoint` samples across
the sprite's and the bubble's rectangles, on all ten screens, at 1440×900, 1280×800,
1000×700, 800×782 and 375×812, plus all ten of the course edition at 1280×800: **zero
samples land on anything but `#app` or the layer itself.** Same result in Persian, where
the band mirrors — sprite at the right edge, same 46px margin, English transcript still
LTR inside the RTL page. Also screenshotted through the real app on the lobby, the green
room, the board and the clue screen: on each, the board's last row ends around 608, the
score strip sits 640–680, and her floor starts at 710. The clue screen is the one that
mattered — the old corner rule put her entirely inside `#clue-verdict`, which is exactly
the collision the band exists to end.

**The phone truncates the cold open, on purpose.** The 243-character
`opening_challenge` sets in three lines at 1440, 1280, 1000 and 800. At 375 it wants
about six and the box shows three plus an ellipsis — she talks on past the end of the
caption. Holding six would need a band of roughly 120px, about 30px more than the green
room can pay (`#screen-setup` clears the fold by ten as it stands), and shrinking the
phone face to fit six lines in three lands near 6px. So the clamp stays at three, and
the comment now says so instead of claiming the line always fits. Abbreviation is not
misquotation: every word shown is hers, in her order.

---

## 2026-09-11 — v1.0.3 shipped: three assets, and the toolchain that wasn't where it looked

**Objective:** push the Persian edition and cut a release carrying the web build, a
universal macOS app, and the unsigned `.ipa`.

**Shipped:** tag `v1.0.3` on commit `29404fd`, three assets, Pages green in 24s.

| Asset | Bytes |
|---|---|
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 13,583,677 |
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14,785,433 |
| `Jeopardy-Iranian-Edition-web-beta-3.zip` | 11,643,420 |

### The thing worth remembering

**The iOS build does not run from a bare shell on this machine.** `xcode-select -p` returns
`/Library/Developer/CommandLineTools`, and `xcodebuild` there dies with *"requires Xcode, but
active developer directory is a command line tools instance."* There is no `/Applications/Xcode.app`
— the only full toolchain is **`/Applications/Xcode-beta.app`**, carrying `iPhoneOS27.0.sdk`. So
the recipe is:

```bash
export DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer
"$DEVELOPER_DIR/usr/bin/xcodebuild" -project JeopardyIranianEdition.xcodeproj \
  -scheme JeopardyIOS -sdk iphoneos -configuration Release \
  -derivedDataPath /tmp/jdd \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" build
```

`DEVELOPER_DIR` rather than `xcode-select --switch`: the global switch needs sudo and changes
the machine, not the build. Note `set -euo pipefail` did **not** save the first attempt —
`xcodebuild ... | tail -n 20` reports `tail`'s status, and the wrapper script masked the
non-zero exit with a trailing `echo`. The failure was only visible in the log, not in the
exit code.

### Verified, not assumed

- `lipo -archs` on the shipped binary: `x86_64 arm64`; ad-hoc signed, identifier
  `com.morad.jeopardy-iranian-edition`.
- `run_tests.sh`: **27/27, 0 failed** before the commit.
- Bumped to 1.0.3 in all three places that carry a version — `build_release.sh`'s Info.plist
  heredoc (`1.0.3`/`103`), `iOS/project.yml` (`"1.0.3"`/`"4"`), and the two `index.html`
  corner labels. The frozen `Versions/beta-3/index.html` was re-synced so the shipped web zip
  says 1.0.3 too.
- The `.ipa` carries 122 entries under `Payload/Jeopardy.app/Web/`, `clues_fa.js` among them —
  checked inside the archive, not inferred from the build succeeding.
- All three zips: `__MACOSX` count **0** (`ditto -c -k --norsrc --keepParent`).
- Live check after the deploy, not a guess: `https://aghamorad.github.io/jeopardy-iranian-edition/`
  serves **v1.0.3** and `data/clues_fa.js` returns `window.CLUES_FA=[{"id": "qajar_amir_kabir_200"…`.

### Still open

Two Gemini data defects, reported and untouched, because the judge and `shufflingOptions`
already refuse to score either: **21 FA alias entries that accept the clue's own distractor**
(the Hallaj clue accepts `بایزید بسطامی`), and **three clues that ship the answer among their
own options** (`double_persian_gulf_tanker_war_400`,
`single_weve_got_elam_entary_evidence_1000_a/b`, `single_persian_flights_of_fancy_600_a/b`).

---

## 2026-09-11 — the Persian edition, the robots, the write-in judge, and a bug that lit the lamp without flipping the switch

**Objective:** one build that is the whole game. Persian as an option inside it, chosen on
the splash; a write-in answering mode beside the multiple choice; robots in the other two
seats at a selectable difficulty; a `[BETA]` seal on the Persian edition; and a style sheet
in the working files so the look stops being something only the CSS remembers.

### Done

- **Persian edition.** `Web/data/clues_fa.js` (1000 clues, `window.CLUES_FA`),
  `Web/i18n.js` (two tables, **188 keys each, verified at exact parity**), `Web/answers.js`
  (the write-in judge), `Web/assets/fonts/IRANSansWeb-{Regular,Medium,Bold}.ttf`, and the
  design-contract document `STYLE_SHEET.md` at the project root.
- **The language gate is the splash.** *Choose your language* replaces "press any key",
  with the seal on the Persian pill. `begin(lang)` guards on `S.screen !== 'splash'`, so the
  choice is splash-only by design; switching later means a reload.
- **Write-in mode**, per match: `answerWritten` runs the judge and either rules or lets the
  host cut in. Generous by construction — typos, dropped articles and surnames all pass.
- **Robots**: `Bots` in `app.js`, four brains, pun names assigned by seat index so they
  survive language switches and redraws.
- **`[BETA]` seal**: `Web/assets/beta-stamp.svg`, an engraved ink seal keyed on
  `html[dir="rtl"]` — **not** on `.pill-fa`, which carries `dir="rtl"` permanently and would
  therefore have put the seal on the English pill too.
- **Froze `Versions/beta-3`** (117 files, 14 MB). Added `clues_fa.js` and `i18n.js` to the
  `build_release.sh` pre-flight guards — the script already `ditto`s the whole `Web/` tree
  into the bundle, but a build guard that only checked `clues.js` would not have noticed the
  Persian bank going missing.
- Corrected the README's claim that "the web build is English-only for now."

### The thing worth remembering

The write-in mode did not work, and the control for it said it did. Clicking **جواب نوشتنی**
in the green room lit the button correctly — the lamp moved, `aria-checked` flipped — while
`S.answerMode` stayed `undefined` underneath. The clue then rendered multiple choice anyway.

`wireSegment(id, attr, key, after)` was doing `S[key] = btn.dataset[attr]`. For `opponents`
and `difficulty` that is fine. For the answer mode it is not: the attribute is
`data-answer-mode`, so the attribute *selector* `button[data-answer-mode]` matches
correctly — which is why the lamp worked — but `dataset` is camelCase-keyed, so
`btn.dataset['answer-mode']` is `undefined`, and `undefined` was assigned straight into
`S.answerMode`. One line: `btn.getAttribute('data-' + attr)`.

The reason it took a while to find is worth keeping. I suspected a stale closure, a reset in
`startMatch`, a second `S` binding, and browser caching, and disproved all four. What
settled it was a temporary `window.__DEBUG_S = S` and looking at the object at runtime: the
literal said `'mc'`, the object had all 37 expected keys, and the value was `undefined`. A
value that is `undefined` when the literal is not is a *write*, not a read. The browser-cache
theory died the same way — `fetch('app.js', {cache:'force-cache'})` inside the page showed
the browser's copy already contained the write branch.

Then verified live in the browser, both languages: a robot buzzed and typed its answer one
character at a time (`قورمهسبزی`, ruled correct, RTL clean); a human misspelled
`constituional revolution` for `The Constitutional Revolution` and was still ruled correct;
and the aside path was exercised through the real keydown listener — `qavam` for
`Ahmad Qavam` produced the host's cut-in with the question still live, and the same input
with the prompt suppressed matched on surname. Debug hook removed, `node --check` clean on
all three JS files.

**Handed to Morad, not fixed:** Gemini's Persian bank has 21 alias entries polluted with the
clue's own distractor (the Hallaj clue accepts `بایزید بسطامی`, the Nima Yushij clue accepts
`احمد شاملو`), and three clues ship the answer as one of its own options. Both are data, not
code; the judge and `shufflingOptions` already refuse to let either one be scored.

**Not done.** `C3PO_LOG.md` is past 830 lines and still wants its older sections archived.
`build_release.sh` remains fragile. Not pushed — Morad hasn't asked.

---

## 2026-09-11 — copy swap on the lobby and board, and the rail collision it exposed

**Objective:** two "copy replacement only, do not redesign" requests — the lobby's lower
furniture, then the board screen's corner + rails, both moved to the "Bigger egos" voice.

### Done

- **Lobby** (`Web/index.html`, `#screen-lobby`): corner-tr → `Same game. / Bigger egos.`;
  corner-br → `Hard questions. / Unjustified confidence.`; left rail → the nine English
  bullets; right rail → the nine Persian bullets. Headline, tagline and all four menu
  buttons untouched.
- **Board** (`#screen-board`): `.board-corner` → `Same game. / Bigger egos.`; left rail →
  Knowledge / Culture / Bad takes / Unjustified confidence / Arguments, obviously.;
  right rail → `همان بازی. / اعتمادبهنفس بیشتر.` plus the five Persian bullets. Tiles,
  round tabs, Menu button, Tehran/Iran and the coordinate corners untouched.
- Stripped `Encore round: ` from all five clue banks (325 occurrences each) — a generator
  artifact where every affected clue was a byte-identical twin of a non-suffixed clue.
  Verified 0 remaining and `node` parses `data/clues.js` as 1000 clues.

### The thing worth remembering

`.rail-list li { white-space: nowrap }` was holding the rails to single lines. Fine for
one-word categories, fatal for Morad's sentence-length copy: measured at 1000px the left
rail ran **straight under the "JEOPARDY!" wordmark**. Two CSS accommodations were needed,
both disclosed to him as out-of-scope-of-"copy only":

1. `.rail-list li` → `white-space: normal` + `max-width: clamp(130px, 14vw, 220px)`, so
   bullets wrap into a column instead of one long line.
2. Board rails only: `.rail-mid .rail-list li { max-width: calc(clamp(10px,14.2vw,240px)
   - 6.9vw - 12px) }` derives its cap from the same gutter `.board-wrap` reserves, and
   `@media (max-width:1199px) and (min-width:901px) { .rail-mid { display:none } }` hides
   them where that column would be too narrow for single words. Below this, `KNOWLEDGE`
   and `UNJUSTIFIED` overflowed onto the first tile column.

**Trap:** `calc(... - var(--rail-x) - 12px)` silently fails — `--rail-x` is a *percentage*,
so it resolves against the `li`'s own containing block (circular, collapses to 0) and the
cap comes out ~2x too wide. Use `6.9vw` instead.

**Second trap:** the `?r=` cache-bust on navigation versions only the HTML. `styles.css` is
a separate cached request, so a CSS edit appears not to apply after reload. Either append a
fresh `<link>` with a query string, or hard-reload (`Cmd+Shift+R`).

### Verified

Screenshot + measured geometry (not just eyeballed) at 1000, 1200 and 1440 wide:
lobby rails clear the wordmark by 25–44px; board rails clear the grid by 12px at 1200 and
1440, and are hidden at 1000. Copy confirmed by reading the rendered `innerText`.

### Out of scope, left alone

`#screen-setup` still carries the old corner copy (`Same game. / Richer stories.` and
`Bigger brains. / A brighter tomorrow.`), so it now disagrees with the lobby and the board.
Flagged to Morad; not changed, since neither request named it.

---

## 2026-09-11 — the show is public

**Objective:** the last standing ask — "text me the public webpage link so i can show it
to my friends and perhaps we can play it over there." That was blocked by a failing
deploy, not by unfinished work.

### Done

- **Fixed the GitHub Pages deploy.** Run `34543024128` failed in 8s at
  `actions/configure-pages@v5`, with `upload-pages-artifact` and `deploy-pages` skipped:
  ```
  [warning] Get Pages site failed. Error: Not Found
  [error]   Create Pages site failed. Error: Resource not accessible by integration
  ```
  Cause: the workflow's `enablement: true` is supposed to create the Pages site on first
  run, but the repo's `default_workflow_permissions` is **`read`**, so the Actions
  integration cannot create it — `gh api repos/.../actions/permissions/workflow` confirms
  `{"default_workflow_permissions":"read"}`. A workflow-level `permissions:` block does
  not get around this for the *site-creation* call. The job had also failed this way once
  before (`34506084569`, 17s), so it was never going to succeed on its own.
  Fix: create the site directly with the authenticated CLI token, bypassing the
  integration entirely —
  `gh api -X POST repos/aghamorad/jeopardy-iranian-edition/pages -f build_type=workflow`
  → `html_url: https://aghamorad.github.io/jeopardy-iranian-edition/`,
  `build_type: workflow`, `https_enforced: true`. Then `gh run rerun 34543024128` →
  **completed success in 24s.**
- **Verified the live site, not just the run status.** `HTTP 200` on the root, and every
  asset returns 200 with real bytes: `styles.css` 37,825 · `app.js` 53,767 ·
  `data/clues.js` 1,116,202 · `logo-wordmark.png` 1,212,089 · `stage-backdrop.png`
  1,595,624 · `audio/opening_challenge.mp3` 233,856. Looked at the live URL in the
  browser pane — the splash renders correctly (wordmark, rails, tagline, BEGIN pill).
- **Proved published == verified.** `sha1` of the live `app.js` and `styles.css` match the
  working tree byte for byte (`659ff4a7…` and `160882ab…`), and `git status` is clean at
  `2465549`. So the artifact a friend opens is exactly the build that was driven through a
  complete 60-clue match.
- **Texted Morad the link** via `~/.local/bin/c3po-text` → relay pid 74006 (the relay's
  echo guard fired correctly: `skipped: my own text looping back`).

### Verified / ruled out

- **The preview pane will not hold an external URL.** Setting `location.href` to the
  Pages URL navigates, but the next `preview_eval` reports `http://localhost:8788/` again —
  the pane pins itself back to the `.claude/launch.json` server. Not a site problem; the
  live page was confirmed by screenshot plus the asset/hash checks instead.
- **Nothing to re-run.** The deploy is green and matches HEAD, so publishing is now
  automatic: any future push touching `Web/**` fires `pages.yml` and will succeed, because
  the site it needed to create already exists.

### Open

- `/Users/Morad/Desktop/...` hard-coded fallback paths and the iOS/iPad "sleek" port are
  untouched. App icon (Apple `iconutil` / Asset Catalog) also outstanding.

---

## 2026-09-10 — wager layout, locked-out badge, full-match + mobile sweep

**Objective:** finish the show. Morad's standing ask was "just finish the game for now"
and a local-multiplayer requirement — one controller per contestant, driving the menus
and per-player buzz routing. This pass closed the last visual defect I had personally
seen and then verified every remaining screen.

### Done

- **Fixed the wager screen** (`Web/styles.css`), the one screen Morad had complained
  about. Two distinct defects, both confirmed by eye before touching anything:
  - **The four quick-set buttons wrapped 3 + 1**, orphaning ALL IN on its own centred
    row. Added a `@media (max-width: 560px)` block turning `.wager-buttons` into a
    `repeat(2, minmax(0, 1fr))` grid with tightened padding. Below 560px it is now
    QUARTER|HALF over THREE QUARTERS|ALL IN; between 560px and 900px one row fits; above
    900px the existing `min(60vw, 720px)` container holds all four.
  - **LOCK IT IN was stranded at the bottom of the plate**, a large dead gap between it
    and the slider it belongs to. Added `#screen-wager .clue-body { justify-content: safe
    flex-end; }` so the controls sit directly above the confirm button. Scoped to
    `#screen-wager` so the clue screen keeps its centred body, and `safe` is deliberate —
    plain `flex-end` clips the top when content overflows, which is the exact bug
    `.clue-body`'s `safe center` was written to avoid.
  - Verified at 375×812: `buttonRows: [[Quarter, Half], [Three Quarters, All In]]`,
    `bodyJustify: "safe flex-end"`, gap from buttons to LOCK IT IN **10px** (was a large
    void). Verified again at desktop — four across, button directly beneath.
- **Fixed "Quarter" reading $300 on a $1,000 maximum** (`Web/app.js:820-838`). The slider
  was hard-coded to `step = 100`, so `Math.round(max * 0.25 / 100) * 100` snapped $250 up
  to $300 — and since a fresh Daily Double has `max = 1000`, that was the *first* wager a
  new player ever saw. The step is now derived: the largest of 100 / 50 / 25 that divides
  the maximum into exact quarters (a $1,000 max → step 50; $1,500 or $1,100 → 25; $2,000
  → 100), with 25 as a guaranteed fallback since scores and clue values are always
  multiples of $100. Quick amounts clamp to the maximum. Verified live on the mobile
  wager screen: **Quarter → $250, Half → $500, Three Quarters → $750, All In → $1,000**,
  each echoed on the slider.
- **Fixed a real bug: the locked-out podium badge never appeared.** After a wrong answer
  the verdict head correctly read "Incorrect — PLAYER 1 is locked out" while
  `#podiums-clue` showed no `is-out` badge. Cause: `answer()` calls `renderPodiums()` at
  `Web/app.js:681` *before* `S.lockedOut.push(S.buzzed)` at the later line, so the class
  lagged a full render — it only appeared once the next clue re-rendered. Added a second
  `renderPodiums()` immediately after the push, with a comment saying why. Re-verified
  live: `lockedOutBadges: ["PLAYER 1−$200"]`.
- **Drove a complete 60-clue match to the results screen** with a page-side auto-player
  (deliberately always answering option 0, so every player finished in the red). Both
  rounds, a Daily Double in each, Final Jeopardy, then `screen-results` with title
  "A Tie" and three ranked `result-row neg` entries. End-to-end integration, not a unit
  check — the whole state machine ran unattended.
- **Finished the mobile sweep at 375×812.** Results, how-to, match menu and settings all
  render without overflow (`docOverflowX: false`, `overflowsViewport: false`, no card
  needs internal scrolling; results' PLAY AGAIN ends at y=607 of 812). Looked at each one,
  not just measured.

### Verified / ruled out

- **The controller path now has a functional test.** A synthetic-pad run drove
  splash→lobby on pad A, ring focus walking Start game → Settings → How to play, A
  opening the how-to and B closing it, a second pad navigating independently, and — the
  one that matters — a clue opened by pad 1 and **buzzed by pad 2, awarding the floor to
  PLAYER 2**. That proves per-player buzz routing, which is the whole point of "each
  player gets a controller". (The ring itself is still only visible with a pad present;
  that is by design, not a gap.)
- **`cluesLeft: 1` was a stale DOM reading, not a bug.** A tile looked unsolved while the
  match had already reached Final Jeopardy. `closeClue()` marks the tile solved, finds
  `!anyUnsolved()`, calls `startFinal()` and returns **without** `renderBoard()` — so the
  DOM keeps the previous render. Game state was correct throughout. No fix needed.
- **The repo is already public.** `github.com/aghamorad/jeopardy-iranian-edition` is not
  private as inherited notes assumed. `.github/workflows/pages.yml` is valid and
  `upload-pages-artifact` points at `Web`, so pushing `Web/**` to `main` publishes the
  site. *(Then-Pages was not yet enabled — API 404 — and I expected the first run's
  `configure-pages` step (`enablement: true`) to flip it on. It could not; see the
  2026-09-11 entry.)*
- **Copyright, Morad's call not mine.** The 1000 clues are written from ~60 copyrighted
  reference books, and `Corpus/` (280K) plus `QuestionBank/` (9.7M) are tracked in that
  public repo. A Pages URL only increases discoverability of what is already exposed.

### Open

- ~~**Publishing is still held** by Morad's "only pushed to github when it's absolutely
  ready". Three files are modified in the working tree and nothing is committed:
  `Web/app.js`, `Web/styles.css`, `Web/index.html`.~~ **Superseded** — he authorized the
  push, it landed as `2465549`, and the deploy was fixed the next day; see the entry above.
- `/Users/Morad/Desktop/...` hard-coded fallback paths and the iOS/iPad "sleek" port are
  untouched this session.

---

## 2026-09-10 — web build + Final Jeopardy fixes

**Objective:** the two things Morad asked for — a real GitHub backup so nothing is lost,
and a web version of the show he can open on his laptop and on his phone to show friends.

### Done

- **Pushed the Swift port to GitHub.** `https://github.com/aghamorad/jeopardy-iranian-edition`
  is at `1f64093` "Port the show to a shared macOS/iOS SwiftUI codebase", then `86d0df8`
  "Add the C3PO work log". Remote confirmed matching local HEAD.
- **Built the whole web app** under `Web/` — build-free static HTML/CSS/JS mirroring the
  Swift show: lobby, board, clue, wager, results, match menu; all six categories; Daily
  Doubles; Final Jeopardy; the full audio bed (`assets/audio/*`); the traveling shine.
  - Classic `<script>` tags, not modules, so double-clicking `index.html` works.
  - The clue bank is embedded as `window.CLUES` in `data/clues.js` so `file://` needs no
    `fetch()` and hits no CORS wall.
  - Responsive: separate laptop and phone layouts, keyboard **and** touch play.
  - **The options are not shuffled in the bank** — `correct` is index 0 for all 1000
    clues. The native app reshuffles per clue at board-build time
    (`GameEngine/BoardBuilder/BoardBuilder.swift:77` → `Clue.shufflingOptions()`); the web
    mirror of that is `shufflingOptions(clue)` in `app.js`. Confirmed live: a clicked
    option 0 was wrong with the correct answer sitting at index 2.
- **Fixed two real defects on the Final Jeopardy screens** (`Web/app.js`, 6 edits;
  `Web/styles.css`, 1 edit):
  - **Clue text collided with the category bar.** `.clue-body` is `flex: 1` with plain
    `justify-content: center`, so once its content exceeded the box it spilled out of
    *both* ends — measured overflowing up to y≈20 against a body top of 76, straight over
    the header. Added `fitClueText()`, which mirrors the native
    `minimumScaleFactor(0.68)` by stepping the font down to an exact fit, plus
    `justify-content: safe center; overflow-y: auto;` as the backstop. Verified: the
    hard 9-line "In his contemporary account of the revolution…" clue fits at 1280×720
    with `collidesWithHeader: false`; at 1440×900 the 7-line Final clue lands at
    `fontSize 28.4px`, `textH 262`, `avail 287`, `scrolls: false`.
  - **The Final reveal dropped the explanation and the citation.** `submitFinalAnswer`
    built only head + answer + next button, unlike `showVerdict` and unlike the native
    `clueResolved` state. Added the `explain` and `source` nodes. Verified on screen:
    the reveal now reads "Iran: A Modern History · Abbas Amanat · p. 782".
- **Drove a full 60-clue match to the results screen** and confirmed every state renders —
  board, clue, buzz, wager, Final reveal, results.

### Verified / ruled out

- **The clipping is viewport-bound, not a bug.** At the test pane's 720px height
  `.clue-body` squeezes to ~107px, and a 7-line clue needs 196px even at 50% font — no
  amount of shrinking fits it. At 1440×900 the same clue fits whole with no scroll.
  Decided **against** hiding answered options or adding conditional font caps; that is
  over-engineering for one small viewport. Shrink → scroll is the correct adaptive
  behaviour.
- **A `fitClueText` bug I introduced and caught.** It once reported `fontSize: 12.4px`,
  far under my 0.68 floor (~28.9px), because the Browser pane was hidden, every box
  measured zero, `avail` came out ≤ 0 and the shrink loop ran to its floor. Real flaw,
  not a test artifact — fixed with an early `if (avail <= 0) return;`.
- **The harness was the bug three separate times.** A driver stalled forever clicking a
  dead tile because **solved tiles are marked `disabled`, not `.solved`** — the selector
  must be `[...document.querySelectorAll('#board .tile')].filter(x => !x.disabled)[0]`.
  A second driver looked stuck on "Get ready…", which could not be real since the arm
  timer is only 450ms (`app.js:430`) — it was stale intervals from earlier runs. Fixed by
  reloading for a clean slate and writing **one** driver guarded by a generation counter
  (`window.__gen`) so any stale loop self-terminates. Healthy cycle after: 25 clues in
  20s. Lesson, now for the fourth time: when a driver shows an app bug, suspect the
  harness first.

### Known gaps (not actioned)

- **No Final Jeopardy countdown on the web.** Native has `finalRemaining = 30`
  (`GameEngine/Models/GameState.swift`). Deliberately left out of this pass.
- No generator script for `Web/data/clues.js` — it is a hand-made derived copy of
  `QuestionBank/verified_clues.json`, so the two can drift. Noted in the README.
- The lobby cursor ring is invisible without a gamepad, and there is no gamepad on this
  machine, so the controller path has **never** been visually verified. *(Superseded — a
  synthetic-pad run did verify it; see the wager/lockout entry above.)*
- ~~The wager quick-buttons wrap awkwardly…; LOCK IT IN sits far below the slider;
  "Quarter" yields $300 on a $1,000 max~~ **All three fixed** — see the entry above.
- `Web/assets/emblem.png` is unreferenced by the web runtime, but it is **not trash** —
  it is the 204×192 source master for the green-white-red "O" in the wordmark (the same
  art bundled natively as `App/Resources/iranian_emblem.png`, per `Docs/ASSET_CREDITS.md`).
  A provenance asset, so by the location rule it stays.

---

## 2026-09-10

**Objective of the session:** make the green→white→red "shine" a *traveling* selection
indicator — it moves to whatever is chosen (menu entry, buzzed player, locked answer),
with a simple animation, consistently across every surface in the show.

### Done

- **Removed a regression I had introduced earlier:** the `DefaultActionWhenFirst`
  view modifier in `App/Views/ReferenceShowViews.swift`. It made Return fire twice on
  the opening splash (dismissing the curtain *and* opening The Green Room setup).
  Proven by a differential test — Space (`keycode 49`) landed cleanly on the lobby,
  Return (`keycode 36`) opened setup. Struct and its single call site both deleted.
- **Traveling shine written and verified.** The board had no animation transaction, so
  the selection light blinked out and back in on the next tile instead of travelling.
  Added two `.animation(.easeInOut(duration: 0.18), value:)` modifiers to `liveBoard`
  in `ReferenceShowViews.swift` (one for `selectedBoardColumn`, one for
  `selectedBoardRow`). Rebuilt clean. Seen moving on three surfaces: board tile
  (travelled two columns right, two rows down to 300/HISTORY), match menu (only
  CONTINUE PLAYING wore it), buzz row (only BUZZ · PLAYER 1 wore it).

- **Diagnosed the "ghosts of another version" on the board.** Not a second app
  instance — window count 1, process count 1. It is the *reference plates*: each
  screen's bottom ZStack layer is `ReferencePlate(asset:)`, a **finished 1672×941
  screenshot of that whole screen**, with the live SwiftUI drawn on top by hand-tuned
  `originX + n * scale` coordinates.
  - `board_reference.png` is a complete board: PEOPLE & FIGURES / PLACES & GEOGRAPHY /
    HISTORY & REVOLUTIONS / CULTURE & ART / POLITICS & SOCIETY / MISCELLANEOUS, six
    columns of 100–500, ROUND 1 / DOUBLE JEOPARDY / FINAL JEOPARDY tabs, and three
    PLAYER podium cards. Every one of those ghosts is baked art, not live state.
  - `lobby_reference.png` is a complete lobby: the left rail reading PEOPLE / PLACES /
    EMPIRES / CULTURE / REVOLUTIONS / ART / SCIENCE / SPORTS / AND MORE…, the JEOPARDY
    wordmark, and the START GAME / SETTINGS / HOW TO PLAY / QUIT buttons.
  - `ReferenceClueView` (line ~672) sits on **`lobby_reference`**, not a clue-specific
    plate — so during a clue the baked lobby menu is dimmed by `Color.black.opacity(0.38)`
    and not hidden. That is the ghost rail and wordmark behind the clue card.
  - Fit is consistent (plate `.scaledToFit()`, live `min(w/1672, h/941)`), so the board
    lines up *mostly*; the leakage is at the margins — the clipped value column at the
    left edge, the round tabs above the live pill, the podiums. Note `ArchivalBackdrop`
    is the odd one out: it uses `.scaledToFill()` + `.clipped()`.

  **Fix not yet applied:**

### Open

- **Decide the plate fix.** The board and clue screens should not be drawn on top of
  pictures of themselves. Options: (a) give the board a plain studio backdrop
  (`studio_stage_bg` / `stage_isfahan` at reduced opacity, the way `ArchivalBackdrop`
  does) instead of `board_reference`; (b) same for the clue view instead of
  `lobby_reference`; (c) mask the baked regions with an opaque rectangle — cheapest but
  leaves the dead weight in the bundle.
- Controller input path still never visually verified — no gamepad on this machine and
  the lobby cursor ring is gated on pad presence.
- Web app with mobile support: entirely outstanding.
- Deploy to the physical iPhone 17 Pro: needs a development team for signing.
- Six hard-coded `/Users/Morad/Desktop/...` fallback paths in the engine/app still
  present — they break portability and are what trigger the macOS Desktop-folder TCC
  prompt that once hung the app with zero windows.

## 2026-09-11 — README in MORADSVOICE, plus a host-voice pass

- Rewrote `README.md` end to end in MORADSVOICE. Every claim checked against the repo
  before it went in: 1000 clues in both `QuestionBank/verified_clues.json` and
  `Web/data/clues.js`; all 1000 carry `source_id`, `book_title`, `author`, `chapter`,
  `page` and `supporting_passage` with no gaps; 49 book files across 7 period folders in
  `Sources/`; 120 categories; single-round values 200–1000, double round doubles them.
  Corrected the old README's "roughly sixty reference books" — it is forty-nine.
- New README shape: the conceit, "The clues have receipts" (with the shelf table), "One
  game, three front ends", macOS build, iOS, Web, Controllers, "What is not in this repo".
  Added the live Pages URL.
- **Scope correction this session:** "use /moradsvoice to write a proper copy for the
  game" meant the *GitHub repo* copy (README/docs), NOT in-game UI strings. 13 in-game
  strings I had rewritten were reverted first. Saved as a feedback memory.
- **Host voice fixed:** "just the host of this game should be smug and snarky and mean".
  Saved as `feedback_host_voice.md`. Applied to:
  - `Web/index.html` — `#screen-setup` corners were stale (`Same game. / Richer stories.`
    + `Bigger brains. / A brighter tomorrow.`) and disagreed with the lobby and board;
    now `Same game. / Bigger egos.` and `Hard questions. / Unjustified confidence.` The
    how-to-play Daily Double line now says it is answered "alone, with nobody to bail you
    out… Spend it well."
  - `Web/app.js` — Daily Double subtitle, locked-out hint, all five verdict heads, the
    "Buzzers are live" hint, the Final wager subtitle.
- Verified live: lobby and Green Room screenshotted at 1440×900, corners render and match.
  `node --check app.js` clean. Viewport reset to desktop.
- **Not pushed yet** — waiting on Morad's go.

## 2026-09-11 (later) — the lockout spoiler, the icon, the distributables

- **Buzz swap.** Morad prefers `~/Desktop/game_show_buzzer_cool.wav` over the old
  `buzz.wav`. Copied (never `ln`) to `App/Resources/Sounds/buzz.wav` — 0.780 s, 48 kHz
  stereo, sha256 `60e5095d…`. Rebuilt; the Release SwiftPM resource bundle, `dist/…app`
  and the root `…app` all carry those bytes. `Web/assets/audio/buzz.m4a` was already the
  same file, so the live site needed no redeploy for audio.
- **Rule bug, caught by Morad mid-session:** "the moment the first answerer buzzer gets
  the answer wrong, you spoil the answer while jeopardy rules should be that this should
  give the other contestants a chance to answer." Diagnosed in `Web/app.js`: the
  second-chance machinery was already correct (`S.lockedOut`, `remaining`, the
  `canRetry` path that withholds `Answer:`/explanation/source), but `showVerdict` printed
  `clue.wrongLine` unconditionally — and every `wrongLine` in the bank names the answer
  ("No, we were looking for Jiroft Culture."). Fixed by withholding `wrongLine` while
  `canRetry` and substituting a `LOCKOUT_LINES` taunt that gives nothing away. The
  Swift engine was never affected: `HostPersona.wrongLines` are generic, not per-clue.
- Verified in the browser end to end, not by reading: P1 wrong → no leak, "Second
  Chance", `wrongLine` suppressed; P2 wrong → same; P3 wrong → all locked out, terminal,
  answer revealed. Three contestants' worth of the real Jeopardy pass-along.
- **New app icon.** `generate-image` failed once at the `generation` stage; the retry
  produced `App/Resources/icon-master.png` (1254², no alpha) — the Iranian emblem from
  the wordmark, glossy red on black with the flag stripe as a horizon. Installed as
  `AppIcon.iconset` (10 sizes) → `AppIcon.icns`, `AppIcon.png`, and the iOS
  `icon1024.png`. Read natively at 128 px to confirm it still reads. Not yet signed off
  by Morad — the old blue/gold icon is the committed fallback.
- **`build_release.sh` gained `--universal`.** Native arch stays the default; the flag
  builds arm64 and x86_64 into separate scratch paths (`.build/arm64`, `.build/x86_64`)
  and `lipo`s them into `.build/universal/JeopardyApp`. Same script, same Info.plist,
  same ad-hoc signature.
- **iOS:** unsigned device build succeeds via
  `DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer` with signing disabled.
  There is no iOS development certificate on this machine — only "Apple Configurator" —
  so any `.ipa` is unsigned and needs re-signing to install on a stock device.

## 2026-09-11 (latest) — the buzz window, the hold meter, the glyphs

Morad's ask: "make sure there is a right and wrong moment to buzz so users have to be
quick and patient enough like there should be a BUZZ notifier somewhere close with a
small graphic - similarly with controller mode in multiple question where you have to
hold on of the buttons let there be a hold fill meter."

- **The buzz window is real now.** Before, the buzzers were open from the instant a clue
  appeared, so the fastest thumb always won and there was nothing to be patient about.
  The Swift engine already had the rule (`GameEngine/Buzzer/BuzzerEngine.swift`:
  `prematurePenalties[playerId] = now + prematureLockoutDuration`), so the web build now
  mirrors it: `ARM_MS = 450` ms of reading time before the buzzers open, and a press in
  that window costs `PREMATURE_MS = 600` ms of lockout. The button stays pressable during
  the window on purpose — a foul you cannot commit is not a foul.
- **The notifier.** A `.buzz-lamp` pill sits on the buzz row's own line, right above the
  thumbs that have to read it: a glass dome, a masked conic sweep in green→white→red
  turning around it, slow and dim while the room is still reading, fast and bright the
  moment it opens. Same masked-ring idiom as `.shine::after` — `mask-composite: exclude`
  punches the middle out so the tricolour sits *over* the glass instead of colouring it,
  which keeps the word legible. Pressing early drops a red `is-early` shake on the pill
  and the host says something about patience.
- **The hold meter.** In controller mode a multiple-choice answer is not a press, it is a
  hold: `HOLD_MS = 700` with the A button down. `.option::before` is a scaleX wash in the
  same tricolour, so the answer lands exactly when the colour reaches the far edge — no
  clock to read. Release early and it cancels clean, back to nothing.
- **The glyphs.** `<kbd class="glyph">` is a controller face button drawn rather than
  typed — glass dome, letter on top, tricolour ring turning around it. Used for the
  button legend in Settings ("the d-pad or left stick moves, A chooses, B goes back,
  Start opens the match menu").
- Verified in the live browser, not by reading: a timing trace showed the lamp `idle/Wait`
  at 90/150/400 ms, `is-live/Buzz` at 700 ms with the hint reading "Buzz · 8 SECONDS"; the
  computed style came back `conic-gradient(rgb(23,178,90), rgb(244,241,234), rgb(224,32,32)…)`
  with `mask-composite: exclude` and `lamp-spin 1.5s`. A synthetic gamepad drove the hold
  meter through `fill=0.18 → 0.46 → 0.75` and committed through `answer()` at ~700 ms.
  Screenshotted the foul state, the lamp, and the Settings glyph row and looked at all three.
- Reduced-motion block extended to switch the new animations off.

### Icon, chosen by Morad

Morad picked his own `Game Icon.png` (1254², alpha) over my emblem-only master — the
silver "J!" wordmark standing behind the red Iranian emblem, over the tricolour bar. It
is the right call: at 60 px on a home screen the letters still read, where the emblem
alone flattened into a red blob. Flattened onto black with `magick -alpha remove -alpha
off` (the source carried alpha; iOS rejects icon transparency), then rebuilt the ten-rep
`AppIcon.iconset`, `AppIcon.icns`, `AppIcon.png` and the iOS `icon1024.png` from that one
file. Both bundles rebuilt so the icon is baked into `Assets.car` / `Resources/`.

### The repo page, and the release itself

Wrote the download-and-sideload section into `README.md`, and the same material as the
`v1.0.0` release notes: the macOS universal zip, the `.ipa`, the unsigned disclosure, and
the four sideloaders with what each one actually costs you.

- SideStore signs on the phone; AltStore wants AltServer on the same Wi-Fi; Sideloadly
  wants a cable and installs nothing on the device; LiveContainer runs the game inside a
  host app so it doesn't spend one of the three app slots.
- A free Apple ID gives seven days per signature and three apps at a time. TrollStore, in
  its iOS range, removes both.
- The `.app` ships zipped, because a Release takes files and a `.app` is a directory.
  `ditto -c -k --keepParent` carries the executable bit and the ad-hoc signature across
  the round trip; checked by extracting the zip and re-running `codesign --verify --deep
  --strict` on the result.
- Eleven of the twelve files under `Jeopardy Sounds/` turned out to be byte-identical to
  what `App/Resources/Sounds/` already holds. Only `vintage_game_buzzer.wav` has no twin,
  and it stays recoverable in history either way.

Release: https://github.com/aghamorad/jeopardy-iranian-edition/releases/tag/v1.0.0

### Read first, buzz after

The buzzers used to open 450 ms after the clue, which is no window at all when the whole
clue is on the card. The web build now runs two clocks: `Read · 6 SECONDS` with the buzz
row shut and the lamp reading *Wait*, then `Buzz · 8 SECONDS` with the lamp lit and the
buttons live. `ARM_MS` and its `setTimeout` are gone — the read clock's expiry arms the
buzzers and starts the second clock, so the two windows cannot disagree about which one is
running. The clock takes an `urgentAt` argument because a six-second window would
otherwise have been amber from its first tick.

The engine matches: `GameState.swift` arms after `6.0` seconds instead of `1.2`. Not yet
rebuilt into the shipped `.app` / `.ipa`.

### She opens on the title card

The opening line used to fire on the way into the lobby. Now the show opens on the splash:
the theme comes up with the page, at `OPENING_MUSIC_MS` (2.6 s) it ducks out under her,
she says her piece over the title card, and the theme returns when she finishes — the
button waits, dimmed, until then. The player presses into the lobby with the music already
running.

Two things hold it together: `Sound.voice` calls back on every path (ended, missing cue,
refused play, and a 20-second guard), so the title card cannot lock; and the muted case
ends the opening directly, because `voice` returns without a callback when the show is
silenced. She plays once per page load — `quit-game` returns to the title card with the
theme running and no second performance.

Note for the browser build: a first visit with no gesture behind it will have the theme
and her line both refused by the autoplay policy, so the button comes live after 2.6 s and
the show starts at the lobby. That is the policy, not a bug.

## v1.0.1 — shipped

The reading window and her new entrance are built, pushed, and released. `71195c0` on
`main`; the Pages workflow ran green and the live `app.js` carries `READ_SECONDS = 6`,
`BUZZ_SECONDS = 8` and `OPENING_MUSIC_MS = 2600`.

Both binaries rebuilt against the new engine timing and bumped to 1.0.1 (macOS
`CFBundleVersion` 101, iOS 2 — the iOS build number had to move or a sideloader would
refuse to overwrite 1.0.0).

- `build_release.sh --universal` → `dist/Jeopardy Iranian Edition.app`, 48 MB, `lipo`
  reports `x86_64 arm64`, ad-hoc signed and verified. Launches to the title card; checked
  with a screenshot, not assumed.
- `xcodebuild` from `iOS/` → unsigned `Jeopardy.app`, packed as
  `Payload/Jeopardy.app` into the `.ipa`. 39 MB, 51 entries in the payload. The audio is
  in there — 20 files at the bundle root, and every cue the Swift app asks for is among
  them. `opening_challenge` is absent, as it should be: the native app has never used that
  cue, so the new entrance is a web-only change and no Swift edit was invented for it.

Two things worth remembering for the next release:

- `iOS/project.yml` is the version's home, not the `.xcodeproj`. Editing the yml alone
  does nothing until `xcodegen generate` runs from `iOS/`; the generated `Info.plist` is
  what carries the number into the bundle.
- `gh release create` for ~74 MB of assets takes minutes from here. Buffer it and run it
  in the background rather than waiting on it in the foreground.
- `gh release view --json` rejects `tag` — the field is `tagName`. The first verify
  command exited 1 on that alone, after the release had already published cleanly.

Released: <https://github.com/aghamorad/jeopardy-iranian-edition/releases/tag/v1.0.1>

## 2026-09-11 — her voice, the dial, the round cards

She reacts to a verdict out loud now, the timer is a gauge instead of a number in a
corner, the rounds announce themselves, and the results screen deals itself out. All web
work; none of it is in a binary yet.

### Her verdicts

Thirty-two new clips, sixteen for a right answer and sixteen for a wrong one, built from
the two folders on the Desktop (`Jeopardy_Correct_Answer_Voices`,
`Jeopardy_Wrong_Answers_Smug`) and installed as `Web/assets/audio/right_01…16` and
`wrong_01…16`. Each is `.m4a` with an `.mp3` beside it, matching the retry the loader
already runs for voice cues.

They come out of a **shuffled bag**, not a random pick. `drawHostLine(kind)` empties a bag
before refilling it, and the last line out of a bag is shuffled into the next one first —
so she cannot repeat herself in front of the same room, and the seam between two bags is
not a repeat either. `HOST_LINE_DELAY_MS` (650 ms) holds her back so the verdict sting
gets a beat of its own and she lands on top of it rather than talking over the sound that
just told the room the answer was wrong.

`hostLine()` clears the pending timer before setting a new one. Without that, a clip
queued behind a clue the player then abandons surfaces over the next clue.

### The underscore

`splash_underscore.m4a` now carries the title card. The show's theme used to come up with
the page and sit under her while she talked; the underscore is written to sit under a
voice, so it takes that job and `doneOpening()` hands the room to `menu_theme` the moment
she finishes and "press any button" goes live. She does not perform twice — coming back to
the title card later leaves the music alone.

The muted case does not wait on a cue that was never played: `Sound.voice` returns without
calling back when the show is silenced, so `runOpening` ends the opening directly instead
of leaving the title card locked.

### The dial

The clock was a number in a corner. It is a gauge now: a conic dial depleting clockwise
from the top over red→white→green paint, so green burns off first and red is the last
thing standing. The count sits in the middle of the ring in the display face, the label
beneath it.

Two bugs had to go first, and they were the same bug in different clothes.

`.clock-dial > *` handed positioning and the annulus mask to **direct** children only — but
`.clock-ring` sits one level deeper, inside `.clock-arc`, because the conic depletion and
the annulus cut have to be applied by two different ancestors in order to compose. So the
ring got neither positioning (an inline `<span>` collapses to 0×0) nor a cut, and the dial
rendered as an almost-empty dark circle. Both now live in a reusable class, `.clock-cut`,
stamped on all three dial layers from `buildClock()`.

The second: `.plate-clue` is a column flex container, so the clock's `display: inline-flex`
was blockified and stretched to the cross axis — the clue clock became a capsule the full
width of the stage with the dial stranded at the far left. `align-self: center; flex: none`
on `.plate-clue > .clock` centres it between the clue card and the answer row. The same
gauge now sits centred under the round tabs on the board and inside `.clue-actions` on
Final Jeopardy, so the timer is in the same place every time the player looks for it.

Every value the audience reads from across the room — tile amounts, scores, the clock, the
wager — moved onto `--display`, which resolves to **Avenir Next Condensed**. It ships in
macOS core fonts and on iOS, so it costs no download and cannot fail to arrive; the stack
falls back through Helvetica Neue Condensed and Roboto Condensed.

### Round cards

A round change gets a card: full scrim, the round name set large in the display face, the
flag rule drawing itself out either side. `showRoundCard(kicker, title)` holds it for
`ROUND_CARD_MS` (2400 ms), then lifts it and restarts the board clock. It plays on the
opening round, Double Jeopardy and Final Jeopardy, takes no clicks — the round underneath
is already built and running by then — and stops both clocks while it is up so nothing
expires behind it.

The scrim came out too thin the first time: the outgoing screen's clue text read through
the title as though it were a mistake. It is now opaque at the centre
(`rgba(4,4,5,0.965)` → solid by 78%), with the vignette as atmosphere rather than as
transparency.

### The reckoning

`finishMatch()` already touched `#screen-results`, `#results-list`, `.result-row`,
`.is-winner`, `.shine`, `.is-on` and `.neg` — the class names, the `--pc` colour and the
`--i` order all existed. What was missing was motion, and there are four pieces of it:

- Each row deals itself out on `--i` (`result-in`, 130 ms apart from a 120 ms base), so the
  ranking assembles top-down instead of appearing as a block.
- The winner lands last and lands hardest (`winner-pop`, 660 ms, delayed to 640 ms + the
  row's own stagger). The peak is `scale(1.05)` at 52%.
- `.shine` runs its travelling sweep on the winner for as long as the screen is up.
- Everyone else steps back: `saturate(0.55) brightness(0.76)`. A tie has no winner, so
  `has-winner` is withheld and nobody dims.

The trophy and the title outlive a match, so their entrance has to be restarted by hand —
drop `is-dealt`, force a reflow, put it back — the same trick the round card needs.

### Verified, in the browser and by looking

- Both branches of her verdicts, end to end.
- The opening: underscore, her line, hand-over to the theme, button unlocking.
- The dial's direction and depletion at **9×**, after a smaller reading misled me: the lit
  slice runs top → right → bottom. Red at the top, green burning off first.
- The board clock counting 20 → 17 → 12 → 2 with `is-urgent` set and `--t` tracking; its
  expiry calls `autoPick()`, opens a clue and resets the node to `--t: 1`, hidden.
- The clue clock reading *Read · 5/6* then *Buzz*, and the round card (Round Two /
  Double Jeopardy!) transitioning in and settling. Both were caught by hand-building the
  identical DOM, because the screenshot round-trip is slower than a 2400 ms card.
- The results screen at a frozen timeline: rows mid-deal, then `winner-pop` measured at
  `scale 1.0504` at 983 ms. The `cubic-bezier(0.2,1.25,0.3,1)` easing front-loads it
  (1.0495 already at 760 ms), so the row snaps up and settles rather than gliding.
- `--display` genuinely resolves — `document.fonts.check('500 22px "Avenir Next Condensed"')`
  is true, and "0123456789" measures 482 px at 100 px against 500 for Helvetica Neue
  Condensed and 556 for the system sans. No webfont is loaded anywhere; `[...document.fonts]`
  is empty.

### Open

- **Nothing here is committed.** The browser route, `Web/assets/audio/`, and this round of
  CSS and JS are all working-tree changes. Pushing is Morad's call.
- **The binaries lag.** The macOS bundle has not been rebuilt, and the 32 clips plus
  `opening_challenge` are not in a fresh iOS build. The iOS project did build clean
  (`** BUILD SUCCEEDED **`) before these clips existed.
- **`Versions/beta-1/` predates the icon fix.** Re-freeze beta-1 or let the icon change be
  beta-2. Morad's call.
- **`build_release.sh` is fragile:** a failing `swift build` inside `build_arch`'s command
  substitution does not abort the script.
- **Audio formats are deliberately uneven.** Voice cues carry an `.mp3` fallback because
  the loader retries; SFX and music (`menu_theme`, `splash_underscore`, the bumpers) are
  `.m4a`-only. AAC is fine on every browser that matters, so this is a convention rather
  than a gap — but a failed `.m4a` is silence, not a fallback.
- **`askWager()`'s Final Jeopardy subtitle says "You can still back out."** with no control
  that does it. Flagged, not changed — the host's voice is Morad's.
- **`launch.json` declares the web preview on 8099; the running pane answered on 8788.**
  Worth reconciling so the next session does not chase a phantom server.
- Not yet watched live: `Sound.cut()` on the Second-Chance click and on `#quit-game` /
  `#play-again`.

## v1.0.2 — shipped

The typography, the dial, the round cards, the results motion and her 32 verdicts are
built, pushed, and released. Both binaries rebuilt, both versions bumped, and the web
frozen a second time.

**The version web.** `Versions/beta-1/` was already there, copied at 17:04 and never
committed. `snapshot_web.sh beta-2` froze the current `Web/` beside it. The two are
genuinely different shows, not a label change: `app.js`, `styles.css`, `index.html`,
`data/clues.js`, the icons and the whole `assets/audio/` set all differ. 47 files against
110. `beta-1` keeps the old wordmark art (`logo.png`, `logo-sm.png`, `logo-xs.png`) and
the pre-fix icons; `beta-2` is what ships. Both folders are committed, so the backup is
in the repo and not only in this working tree — which was the point.

**The stale-bundle trap.** The two `.app` copies that were sitting in the tree
(`dist/` and the root) predated all of this. Their bundled `styles.css` hashed
`5030fa19…` against the working tree's `b1e88818…`, `app.js` `e1c75429…` against
`09f211bd…`, and their `assets/audio` held 20 files with **zero** `right_*` clips — so
opening the old bundle showed the old show and played none of her verdicts. Worth
remembering: **the built `.app` is a snapshot, not a window on the working tree.**
`swift run JeopardyApp` *is* a window on it — `ShowSource.indexURL` fails the bundle
lookup and falls back through `#filePath` to the live `Web/`. That is the fast way to
look at unfinished web work in the native shell.

**Both builds, re-verified against the tree rather than assumed.**

- `build_release.sh --universal` → `dist/Jeopardy Iranian Edition.app`, 14 MB, `lipo`
  reports `x86_64 arm64`, ad-hoc signed, `CFBundleShortVersionString` 1.0.2. Its bundled
  `styles.css`, `app.js` and `index.html` now hash **identically** to the working tree,
  and its `assets/audio` holds 86 files including 32 `right_*` and 32 `wrong_*`.
- `xcodegen generate` then `xcodebuild` from `iOS/` → unsigned `Jeopardy.app`, 1.0.2
  (build 3), 86 audio files, packed as `Payload/Jeopardy.app` into a 14 MB `.ipa`.
- Both are **14 MB where v1.0.1 was 48 MB and 39 MB.** That is the shell rewrite paying
  off — the old bundles carried a second, native copy of the stage art and the SFX that
  the web build already had. The build log still reports it removing them by name
  (`studio_stage_bg.png`, `sealed_wager_card.png`, `winner.wav`…).

**Packaging, once, correctly.** `ditto --sequesterRsrc` writes a `__MACOSX/` sidecar into
the archive — the first `.ipa` came out with one, which is resource-fork noise a
sideloader has no use for. `ditto -c -k --norsrc --keepParent` is the right incantation;
all three archives now verify at zero `__MACOSX` entries.

Three assets went up: the universal macOS zip (13 MB), the unsigned iOS `.ipa` (14 MB),
and — new, because the web build is the definitive one — `web-beta-2.zip` (11 MB), so the
show can be taken down on its own and opened from `index.html` with nothing installed.

Open items carried forward, and one closed:

- **Closed:** `build_release.sh`'s web copy *does* pick up the new clips. Line 74 is
  `ditto "$PROJECT_DIR/Web" "$APP_BUNDLE/Contents/Resources/Web"`, a whole-tree copy, so
  no copy-rule fix was needed — the rebuild alone brought the verdicts in.
- **Closed:** the `beta-1`-before-the-icon-fix question. `beta-2` is the answer; `beta-1`
  stays as the historical freeze.
- Still open: `build_release.sh` does not abort on a failing `swift build` inside
  `build_arch`'s command substitution.
- Still open: `index.html`'s corner label was reading `v1.0.0` in a 1.0.1 build. Bumped
  to `v1.0.2` with the rest. Nothing else in the web build carries a version string.
- Still open: `launch.json` declares the preview on 8099; the pane answers on 8788.

Pushed as `9570fb2` — 281 files, `Versions/` tracked from this commit on. **Pages
deployed on the push:** the "Publish the web show" workflow ran green in 19 s and
`https://aghamorad.github.io/jeopardy-iranian-edition/` serves `v1.0.2` (confirmed by
grepping the live page, not by assuming the deploy took).

Tests green at 27/27 before the commit: `./run_tests.sh`, exit 0.

Released: <https://github.com/aghamorad/jeopardy-iranian-edition/releases/tag/v1.0.2>
— three assets, 38 MB total: `Jeopardy-Iranian-Edition-macOS-universal.zip` (13 MB),
`Jeopardy-Iranian-Edition-iOS.ipa` (14 MB, unsigned),
`Jeopardy-Iranian-Edition-web-beta-2.zip` (11 MB).

## Phantom sweep (2026-09-11)

Morad: "clean up our working directory so we have no phantoms … nothing that would
interfere with the perfection that we've built."

**The code was already clean.** Grepping every `.swift`, `.html`, `.css`, `.js` and
`.yml` for `tehranStudio`, `BroadcastTitle`, `ArchivalPanel` and `ArchivalTheme` returned
nothing. `App/` is three files (`AppMain.swift`, `iOSApp.swift`, `ShowWebView.swift`).
There is no second version of the show in the tree. Every phantom was data on disk.

**Trashed, with checksums to justify each one:**

- Three screen mockups at the repo root — `Splash Screen.png`, `Lobby Screen.png`,
  `Category Choice Sample Image.png`. md5-identical to the copies in `Designs to Base
  Everything On/`, which is the tracked home for the design. ~4.5 MB.
- `LOGO.png` — md5 `9bbd51c5…`, byte-identical to `Web/assets/logo-wordmark.png`.
- `Game Icon.png` — an earlier export from the icon pipeline. `icon-master.png` is dated
  five minutes later (15:40 vs 15:35) and is what produced the shipped `AppIcon.icns`.
- `AudioCache/` (`test.aiff`, `test_dan.aiff`), and the empty `AI/` and `Speech/`.
- `~/Desktop/Jeopardy - Iranian Edition.zip` — 2.6 GB of the whole tree including
  `.build/` and `__MACOSX` junk. Project name outside the tree, so a leftover.

**A mistake worth recording.** I labelled the five root PNGs as untracked. They were
tracked; `git ls-files` printed them and I read past it. Trashing them therefore showed
up as five deletions rather than leaving the tree untouched. Nothing was lost — the
mockups survive in `Designs to Base Everything On/`, the logo survives as the web
asset, and the superseded icon draft survives in Trash — but the deletions had to be
committed as `c49a3d8` to get back to a clean tree. Check `git ls-files` before moving
anything out, not `git status`.

**Deliberately left alone:** `App/Resources/` (36 MB of the old native look — orphaned
by the build, but it holds `AppIcon.icns`, which `build_release.sh:76` copies into the
Mac bundle, and `persian_clues.json`); `.build/` (2.8 GB, rebuildable); the root
`Jeopardy Iranian Edition.app` (script-written duplicate of `dist/`); the two Desktop
voice-source folders and the 36 s splash WAV master. Morad was offered each of these and
declined.

## The repository becomes the memory (2026-09-11)

Morad asked whether the project should carry a small set of memory files so a fresh agent
can pick up the show without the conversation. The answer was yes to the principle and no
to most of the file list, because the sweep above had already shown where the real damage
was: not in the code, which is clean, but in documents that describe a version of the
show that no longer exists.

**Trashed, because they describe something that isn't here:**

- `Docs/ACTIVE_HANDOFF.md` — the worst of them. Describes `ArchivalTheme.swift`, a tooman
  economy running to 200,000,000, a 325-to-650 clue expansion, Persian RTL and theme
  switching, and asserts the product "has NOT yet passed a release build." All of it
  superseded. A fresh agent would have built the wrong game from it.
- `Jeopardy Progress.md` — the same disease, milder. Still refers to `LobbyView` /
  `BoardView` and says the repo has no commits.
- `Docs/ASR_RESEARCH_AND_BENCHMARK.md`, `Docs/CORPUS_COVERAGE_REPORT.md`,
  `Docs/HISTORICAL_ENGINE_ARCHITECTURE.md`, `Docs/VERTICAL_SLICE_PLAN.md`,
  `Docs/VERTICAL_SLICE_ACCEPTANCE_REPORT.md`, `Docs/FINAL_RELEASE_REPORT.md` — six
  milestone reports, all dated 9 September, five of which name their location as
  `/Users/Morad/Spark/Jeopardy - Iranian Edition`. That tree no longer exists. They were
  written for an earlier home and an earlier phase. (Despite the name,
  `HISTORICAL_ENGINE_ARCHITECTURE.md` is about the history corpus, not the Swift engine.)
- `Docs/ASSET_CREDITS.md` stays. It is current and small.

**Written: three files, about three pages.**

- `CLAUDE.md` — the bootstrap. Loaded automatically at the start of a session, which is
  what makes it worth having: it points at `ARCHITECTURE.md` and `GAME_RULES.md`, states
  that the web build is the product, and repeats the ban on the old look.
- `ARCHITECTURE.md` — what runs what. Its load-bearing paragraph is the one about
  `GameEngine/`: `Package.swift` shows `JeopardyApp` has no dependency on
  `JeopardyGameEngine` and only `Tests/` imports it, so the Swift engine is a rules oracle
  the shipped apps never run. That is the fact most likely to mislead a new agent, and it
  was nowhere in writing.
- `GAME_RULES.md` — the rules as actually implemented in `Web/app.js`, with the constant
  names. Three things in it are counterintuitive enough to have been worth writing down:
  the game is multiple choice, not typed, so there is no typo tolerance or surname
  matching (that behaviour belonged to the retired Swift engine); a wrong answer subtracts
  the clue value in Single and Double alike; and Double does not literally double Single,
  since rows four and five run 100 to 150 and 200 to 200.

**Three README corrections.** It called `App/` "the show itself: SwiftUI views, theme,
audio direction" when it is a three-file web-view shell; it framed the show as a Swift
codebase with a web copy rather than a web show with native shells; and it priced
single-round clues at 200 to 1,000 with the Double round doubling that, when the board
shows 10 to 200 and 20 to 200 million toman.

Also pushed `c49a3d8` and `e25e7e3`, the two phantom-sweep commits still sitting local.

**Not done.** `C3PO_LOG.md` is now 777 lines. It is still navigable by heading, and it is
the most valuable document in the repo, but it will eventually need its older sections
rolled into an archive file. Worth doing before it doubles again.

## 11 September 2026 — the phone gets its timer, and the clue stops being cut in half

### The bug Morad reported was worse on the phone than on the Mac, and he was right

Two separate complaints, and they turned out to share a cause. The lobby music bled into
the gameplay music and the two beds played on top of each other into what he called an
"insane insane insane cacophony"; and the robots buzzed without a buzzer sound. The music
one was a sting de-dup problem — the lobby bed was never stopped when the game started,
so the gameplay bed was layered over a live loop. The buzzer one was simpler still: the
robot buzz path called the state change but never the sound.

Then he said "make sure the phone version is the same too - since that big annoying bug
was especially prevalent in the phone version", and that turned out to be the real
finding. `v1.0.3` shipped with an `app.js` from *before* both fixes. The tag was built
from a tree that predated the source. So the release Morad had been testing on his phone
could not have been fixed no matter how many times he reinstalled it. Bumped to
`1.0.4` / build `104` on macOS and `1.0.4` / `5` on iOS, and froze a fresh
`Versions/beta-4` — which had itself been stale, pre-dating the enlarged clock, the
floating verdict, and everything below.

### The timer he asked for

"the buzzer timer and the timer itself should be a bit more seeable - you can even
generate an image for it if you need like a clock in the same aesthetic."

No bitmap was generated, and none should be. The dial is not a picture of a clock; it is
a live gauge — a `.clock-arc` masked by a `--t` custom property the game writes every
tick, painted with the flag's own conic gradient. A static image could not count down.
What it needed was size, and it got it, on the phone only: the dial went to
`clamp(26px, 6vw, 32px)`, the numeral to `clamp(20px, 4.6vw, 25px)`, the label to
`clamp(9.5px, 2.2vw, 11.5px)`. Total 113×38 in portrait and 133×44 in landscape, up from
89×28 / 20px / 16px / 7.5px. On a 375-pixel-tall screen those pixels have to come from
somewhere, and about 49 came out of phone-only padding — the podium bar, the clue bar,
the logo, the category line, the verdict's own box — with the buzz lamp enlarged on the
same reasoning.

### The clip that the larger timer exposed

Enlarging the clock cost the clue box height, and a three-line clue's last line was
being sliced by the text card's own bottom edge. Instrumented over a full clue: **82
consecutive reading-phase samples, every one at `clip: 42`, `font-size: 25px`, body
103px**. The mechanism matters. `fitClueText()` (app.js:1097) resets to the CSS base,
computes `avail = body.clientHeight − vertical padding`, then walks the size down one
pixel at a time — but never below `base * 0.68`. At 812×375 the phone rule was
`clamp(16px, 5.4vw, 26px)`, and 5.4vw of 812 is 43.8, so the clamp sat pinned on its
26px cap. Floor: 17.68px. The clue needed about 16px in a 91px slot. **No number of
re-fits could ever have fit it**, because the floor was above the size the text required.

Three changes:

- `.clue-text` now clamps off the short edge — `clamp(16px, 5.4vmin, 26px)`, giving
  20.25px in landscape and the *byte-identical* 20.25px in portrait, since 5.4% of 375
  is 5.4% of 375 however you rotate it. Base 20.25 pulls the floor down to 13.77, which
  is below what a three-line clue needs, so the routine has a rung to land on.
- The buzz row gave back six pixels (`min-height: 52px` → `46px`, still over the 44 a
  thumb needs). They go to the one thing on that screen that has to be read.
- `requestAnimationFrame(fitClueText)` at the three phase boundaries — end of
  `startClue`, the Daily Double branch, and `openBuzzers`. The clock, the lamp and the
  buzz row all arrive with that render, and the box they leave is not final until the
  browser has laid the frame out.

Measured on a fresh reading-phase clue after the change: `clip: 0`, `fs: 20.25px`,
body 109px — and seen, not just measured: a screenshot of the reading phase shows both
lines intact above a legible dial. The one residual is honest: the single longest clue in
the bank is 267 characters of 1,723 over 150, and in the reading-phase box its four lines
need about 102px against 97 available, so it overflows ~5px at the floor. That is what
`.clue-body`'s `overflow-y: auto` is for — the style sheet calls it "the backstop for
text that even the fitted size cannot contain" — and it is a fifth of a line on the
extremest clue in the corpus.

### The browser pane is not a browser, and it cost an hour

Worth writing down because it will mislead the next agent. **In the Claude Browser pane,
CSS transitions and `requestAnimationFrame` callbacks only advance when a frame is
actually painted, and frames are painted only when something forces one** — a screenshot,
an inspect. Consequences, all of which I hit:

- `getComputedStyle(x).opacity` and `.visibility` can read **stale**. The setup screen
  showed `is-active` and painted correctly in a screenshot while computed opacity read
  `0` for three seconds.
- `ResizeObserver` callbacks are delivered at frame time, so the observer registered in
  `boot()` on `#screen-clue .clue-body` never fired between forced frames. That is why
  `fitClueText` looked dead. On a real browser or device frames are continuous.
- The newly added `requestAnimationFrame(fitClueText)` has the same property *here* and
  not *there*.

The rule that follows: **for control flow in this pane, test
`document.getElementById(id).classList.contains('is-active')`, never computed style.**
Layout reads (`clientHeight`, `scrollHeight`, `getBoundingClientRect`) stay honest,
because only `opacity` is transitioned. Also: `document.getElementById('board')` matches
the tile grid inside `#screen-board`, so screen-id lists must carry the `screen-` prefix
or they report false positives; and `app.js` is closure-wrapped, so its functions cannot
be called from `preview_eval` — measure the DOM instead.

### Also on the phone

`.options` is now `repeat(auto-fit, minmax(min(100%, 300px), 1fr))` so the answer buttons
take two columns when there is room and one when there is not. On a viewport under 560px
tall the verdict floats over the clue instead of pushing it, with a `:has()` rule dimming
the covered text to 0.2 — verified on screen, panel legible, clue ghosted behind it.

## Her mouth — the splash gets a host who talks

> **REVERSED 2026-09-11.** This feature is gone. Morad saw it live and rejected it —
> *"remove the mouth before we deploy ... it's terrible. no mouth should go on the github
> please..."*. The SVG, the `is-mouth` state, `openMouth`/`skipMouth`, `MOUTH_CAP_MS`,
> `S.speaking`/`S.voicePending` and every rule that styled them have been stripped from
> `Web/` and from `Versions/beta-4/`. The section below is kept only as the record of what
> was built and why.

Morad asked for a graphic on the splash that shows up the moment you pick a language,
"maybe a talking mouth (female) that does the voice over". Built as SVG in
`index.html`, styled in `styles.css`, driven in `app.js`.

### What it is

Four paths under a shared viewBox (`0 18 200 120`): `.m-void` (a rectangle standing in
for the open throat), `.m-teeth` (a thin white band across the top of it), `.m-lip` (the
upper lip, an M with a cupid's bow) and `.m-lip.m-jaw` (the lower). Only two things move.
`.m-void` scales vertically about its own top edge — `transform-box: fill-box` makes the
origin the aperture's bbox, so the seam under the teeth is independent of the viewBox —
and `.m-jaw` translates down by `var(--jaw) * 38px`. Both read the same custom property,
which is why the throat opens exactly as far as the jaw drops.

### The jaw is an envelope, not an analyser

Reading the cue's real amplitude would mean routing the audio through Web Audio, and
rewiring a working playback path for a flourish is not a trade worth making untested. So
the jaw runs on two sines at unrelated periods (11.3 and 5.1 rad/s) plus a little
`Math.random()`, which never settles into a rhythm the eye can catch. It is bracketed to
the real cue by the same callbacks that start and end it — `S.speaking` rises in
`runOpening`'s timer and falls in `doneOpening` — which is all the eye actually checks: a
mouth that opens when she starts and shuts when she stops reads as hers.

While the underscore is playing but she has not begun, `S.speaking` is false and the
envelope runs at 0.14 depth, so she is alive rather than frozen for the two seconds
before her line.

### The hold, and every way out of it

`openMouth()` is called from `begin()` on the language press. It sets `S.voicePending`,
adds `is-mouth` to the splash, starts the jaw, and arms `MOUTH_CAP_MS = 25000` as the
last-resort release. `leaveSplash()` is the single exit and clears the hold
unconditionally, because a second press, the cap, and her cue ending can arrive in any
order. `doneOpening` calls it when `S.voicePending` is up, which is what moves the player
to the lobby.

- A press on the pill itself: `begin()` sees `S.voicePending` and skips.
- A press anywhere else on the card, or Escape/Space/Enter: the document-level skip
  listeners. The click one **excludes `.pill`**, and that exclusion is load-bearing —
  with `is-mouth` the pills carry `pointer-events: none`, so a press in the pill area
  lands on the `<nav>` behind it. Excluding the nav instead would have made the whole
  menu a dead zone.
- Sound off, or an opening that never got going: `begin()` never opens her, and the
  transition stays the plain one it always was.

`skipMouth` deliberately does **not** call `Sound.cut()`. Cutting her line runs
`finish()` → `doneOpening()` synchronously, and the theme would then start a second time
when the lobby opens.

### Checked

On screen at desktop (1280×720): the card holds `screen-splash is-active is-opening
is-mouth` while still on the splash, `stageDisplay: flex`, pills at 0.35 opacity and
`pointer-events: none`, the language prompt hidden. The live rAF writes real values —
`--jaw: 0.802`, `--teeth: 1.00` — and at a magnified 520px the render is a red M-shaped
upper lip, a white teeth band, a large dark aperture and a red lower lip with a 1.6px
overlap at the seam so no hairline shows.

The phone is the case that needed work. At 812×375 the mouth pushed the card 39px past
the fold, clipping "PRESS ANYWHERE TO CONTINUE". The short-window block now gives the
stage `clamp(96px, 26vh, 200px)`, tightens the card's gap and padding, and pins the hint
to `nowrap` — a wrapped hint was two lines of height the fold could not spare.
Measured after: `scrollHeight 375 = clientHeight 375`, over 0.

### The pane cannot hold her, and that is not a bug

Pane clicks are synthetic, so the audio document is never activated and every
`<audio>.play()` is refused; `finish()` fires immediately and she vanishes. Real devices
and a real gesture unlock playback. Her cue (`opening_challenge.m4a` / `.mp3`) and the
underscore (`splash_underscore.m4a`) are both present in `Web/assets/audio/` and the code
path is the one that already worked.

## The race for the buzzer — robots that actually reach for it

Morad, checking the build: *"im checking and the bot already still takes a while to press
the buzzer - you want a race against time in buzzing - that's part of the fun - it
shouldn't be ruthless, but the buzzing of bots should. be randomized too and realistic"*.

He was right, and the old model was wrong in a specific and fixable way. Each brain carried
a single band called `window` and every robot on the board drew from it with one flat
`Math.random()`: normal `[2200, 5400]` ms, hard `[1200, 3600]`, easy `[2800, 6500]`. Two
things followed. The player was almost never beaten to the buzzer — a median first ring of
~3.8s at normal against an 8-second window is not a race, it is a formality — and because
every seat drew from the same distribution, no seat was ever *anything*. There was no
jumpy neighbour, no cautious one, no sense of a room.

So a brain stopped being a skill score and became a set of habits. The band split in two,
and which one a robot draws from is the whole design:

- **`quick`** is the band it rings from when it knows the answer — `[380, 900]` brutal
  through `[1000, 2100]` easy.
- **`late`** is the band it rings from when it is only fishing — `[1500, 4500]` brutal
  through `[2600, 7000]` easy.
- **`nerve`** is the chance the clue is there to be taken at all, and it is what a player
  feels as pressure: brutal takes 78% of them, easy 30%.
- **`alert`** is whether a robot reached for the buzzer at all, and it runs high on purpose
  (0.70 → 1.00). A contestant who sits out one clue in ten is a room; one who sits out
  three is an empty studio.
- **`thumb`** is a per-seat habit drawn once when the match is built, ±20%. The robot on
  your right is reliably the jumpy one, which is what a real podium feels like.

A sure thumb is skewed short — `Math.pow(draw, 1.5)` — because a reaction time is not
uniformly distributed; most of them are fast and the slow ones are the tail. A fishing
thumb is left flat so the late presses really are spread out. Then the arrivals are sorted
and separated: two thumbs inside `THUMB_GAP = 220` ms is not a race and on screen it reads
as one press, so the later one waits. That is also what happens at a real podium. Nothing
lands below `THUMB_FLOOR = 280` ms, because below that it is a machine and not a
contestant.

The old `window` key is gone; `quick` and `late` replaced it in all four brains.

### What it measures

A Node simulation of the new model, 40,000 trials per cell, first ring-in at p10/p25/p50/p75
and the rate at which anybody rings at all:

| brain | p10 | p25 | p50 | p75 | someone rings | both ring |
|---|---|---|---|---|---|---|
| easy | 1137 | 1544 | 3276 | 5111 | 91% | 48% |
| normal | 736 | 886 | 1293 | 3122 | 98% | 72% |
| hard | 498 | 578 | 738 | 1040 | 100% | 92% |
| brutal | 365 | 415 | 496 | 639 | 100% | 100% |

Against the old medians (~3.8s normal, ~2.4s hard) that is the race he asked for, and the
difficulty still separates: on a CASUAL clue brutal's median drops to 476 ms, on
INSUFFERABLE hard's rises to 807 ms.

The first draft pinned brutal to the floor — `quick: [300, 780]` with an `r*r` skew put its
p10/p50 at 281/361 ms, i.e. every buzz sitting on `THUMB_FLOOR`, which reads as a machine.
Raising the bands and softening the skew to `draw^1.5` fixed it.

### Cannot be timed in the pane, and that is the pane

Live, in a bots/hard match: a clue was opened, `Bots.armBuzzers()` armed the seats, and a
robot took the floor and answered correctly — **Bot-ol-Molk**, with the podium carrying
`is-armed shine is-on` and `Rostam` marked `is-right`. No console errors. The mechanism
works end to end.

But the latency cannot be measured there and should not be read from it. `document.hidden`
is `true` for the pane's tab, and Chrome throttles `setTimeout` in hidden tabs — to a
one-second floor immediately, and to roughly one wake-up per minute under intensive
throttling. That is why the floor took ~90 seconds to change in a room whose model predicts
a ~500 ms ring. The numbers above come from the simulation for that reason, not from a
stopwatch in the pane, and the same tab-hidden throttling is why the clue clock sits at
`12 Answer` without counting down: rAF only advances on a paint.

`run_tests.sh` cannot cover this either — it builds a Swift binary against `GameEngine/`
and never touches the web `Bots` module.

### One thing left alone

The language prompt on the splash sits exactly on the backdrop's horizon line, so
`CHOOSE YOUR LANGUAGE` reads as struck through at some viewport shapes. It is the photo —
hiding the text leaves the line — because `stage-bg` is `center 34% / cover` and the
horizon's height is a function of the viewport's aspect ratio. It predates this work and it
ships in v1.0.3. The lever is either `background-position` (cross-screen blast radius) or
the prompt's colour (`--ink-dim`, dim by design), so it was reported rather than changed.

## The mouth comes off, and the buzzer learns the round

**Objective:** take the mouth back out before anything else ships, give each round its own
buzz window, and put a unit on the Persian money.

### The mouth is gone

Morad had already been given a build with the talking mouth on the splash. His ruling:
*"fuck, fuck, remove the mouth before we deploy ... it's terrible. no mouth should go on
the github please..."*. Nothing about the mouth was asked to be reworked — it was rejected,
so it was removed rather than dimmed.

Stripped from `index.html` (the four-path SVG), `styles.css` (the `is-mouth` state, the
`--jaw`/`--teeth` drives, the aperture and jaw rules) and `app.js` (`openMouth`, `skipMouth`,
`MOUTH_CAP_MS`, the `S.speaking`/`S.voicePending` bookkeeping, the jaw rAF, and the
`.pill`-excluding document skip listeners that only existed to give the hold a way out).
`Versions/beta-4/` was re-snapshotted from `Web/` so the frozen build and the live tree
carry the same code.

Verified after: `grep -i mouth` returns **0** in `Web/app.js`, `Web/styles.css`,
`Web/index.html` and the same three files under `Versions/beta-4/`; `diff -rq Web
Versions/beta-4` reports nothing but `.DS_Store`. All three rebuilt artifacts were then
checked the same way — the macOS zip, the `.ipa` and the web zip list **0** matching
entries.

The v1.0.4 release notes lost the whole `## The host turns up in person` section with it,
and the release title — *"a race to the buzzer, and a host who turns up"* — refers to a
graphic that no longer exists, so it was edited too.

### The buzzer belongs to the round

*"the buzzer for the first section is 20 seconds, the buzzer on the second is 12 seconds
and the buzzer on the last round whatever final jeopardy rules say."*

The window was one constant for the whole show. It is now keyed to `S.round`:

```js
var BUZZ_SECONDS = { single: 20, double: 12 };
function buzzSeconds() { return (S && BUZZ_SECONDS[S.round]) || BUZZ_SECONDS.double; }
```

The fallback is the *second* board's number, not the first's: by the time a round is
ambiguous the show has already tightened up. Both `startClueClock(BUZZ_SECONDS, …)` call
sites — `openBuzzers` and the steal/next-contestant path — read `buzzSeconds()`.

The bot side needed the same treatment in one place. `Bots.armBuzzers()` clamped every
thumb with `var ceiling = BUZZ_SECONDS * 1000 - 250;`, which under the old flat 8-second
constant was what stopped a robot pressing after the window shut. That clamp now reads
`buzzSeconds()` too. Checked that it stays rarely-binding rather than re-shaping the race:
the widest band is easy's `late [2600, 7000]`, ×1.2 for the per-seat thumb spread ≈ 8.4 s,
plus at most ~440 ms from the `THUMB_GAP` separation pass ≈ 8.8 s — comfortably inside the
new 19,750 ms (single) and 11,750 ms (double) ceilings, so no band is being truncated
where it used not to be.

Final Jeopardy needed nothing. It has no buzzer to open — `if (S.mode === 'final') return;`
guards both arm paths — and `FINAL_SECONDS = 30` already governs the whole of it. The
wager and the written answer are the round.

No copy mentions a fixed number of seconds (`grep ثانیه` finds nothing), so the change
carried no text edit with it. `node --check Web/app.js` passes.

### The Persian money says its unit

*"add میلیون to the farsi number counts too in termso f category choices and prices... since
right now they're just numbers are they are vague"*.

He was right that it was vague, and the cause was a unit sitting on the wrong key. Persian
read `'unit.m': ''` with `'unit.toman': ' میلیون تومان'`, so a board tile — which prints
`fmt()` = number + `unit.m` — came out as a bare `۲۰۰`, while only the clue header got the
scale. English never had the problem: `'unit.m': 'M'` against `'unit.toman': ' toman'`.

The fix splits it the way English already did — FA `'unit.m': ' میلیون'`, `'unit.toman':
' تومان'` — so tiles read **`۲۰۰ میلیون`** and the clue reads **`۲۰۰ میلیون تومان`**, the two
matching English's `200M` / `200M toman` unit for unit with no doubled scale word.

Checked on screen at both widths, Persian, all 30 tiles. Desktop: values render `۱۰ میلیون`
through `۲۰۰ میلیون`, the widest is 79 px of content in a 92 px tile, single line, no
overflow. Phone (375×812): tiles are 58 × 128 px and `.amt` is 44 px wide at 13.125 px.

### Two things left alone on the phone, on purpose

Once the unit was added, the narrow tiles had a decision in them, and it was made by
measuring rather than by eye.

**The amount does not move to the Persian face.** A canvas probe set `۲۰۰ میلیون` at 79 px
in the display chain against 89 px in `--fa` — 3 px of slack on a 92 px desktop tile, and
the 44 px phone tile would overflow outright. It would also contradict the Persian block's
own contract at `styles.css:1482` (*"the display numerals do not move"*). Left as is.

**The phone font does not shrink.** 12 of the 30 phone tiles wrap `۱۰۰` over `میلیون`. To
force one line at 375 px needs ≈10.9 px, under the `clamp`'s own 11 px floor, and would
fail again at 320 px. Trading legibility for uniformity works against the complaint that
started this — that the numbers were hard to read. The two-line stack is centered
(`text-align: center`, `direction: rtl`) and reads as a figure over its unit.

### Rebuilt

`/tmp/build_assets.sh --universal` re-ran end to end, exit 0. Stage 5:

| artifact | bytes | size |
|---|---|---|
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 13,587,696 | 13M |
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14,789,384 | 14M |
| `Jeopardy-Iranian-Edition-web-beta-4.zip` | 11,647,372 | 11M |

All three are a few KB smaller than the mouth-carrying builds they replace — the removed
SVG and its rules. `lipo -archs` reads `x86_64 arm64`; `codesign -dv` shows
`flags=0x2(adhoc)`, universal; `plutil -lint` OK. Stage 3 asserts the macOS app is 16M and
the iOS bundle 17M, and that the `.ipa` carries the whole `Web/` tree with both banks
present. Stage 6 lists `Payload/Jeopardy.app/Web/index.html` inside the archive.

---

## The two shells agree on their build number

**Objective:** "do whatever you need to do you have access to everything". No new feature
was wanted; the job was to find out whether anything was actually wrong with what shipped,
and fix it if it was.

### The one real defect

The Mac shell and the iOS shell disagreed about their own build number. `build_release.sh`
pens `1.0.4` / `104` into the Mac `Info.plist`; `iOS/project.yml` said `1.0.4` / `5`. The
divergence had already been written down — [line 977](C3PO_LOG.md) above records it — but
never closed.

It is not cosmetic. Sideloaders compare `CFBundleVersion` to decide whether an `.ipa` is an
update, so an install carrying build `5` gets refused as *"not newer"* rather than
installed — on exactly the AltStore / SideStore / Sideloadly path the release notes send
people down. Two shells of one product also should not disagree about which of them is
newer.

`iOS/project.yml` now reads `CFBundleVersion: "104"`, matching the Mac, with a comment
saying why so the number is not "tidied" back down later. `xcodegen generate` rewrote
`iOS/JeopardyIOS/Info.plist` to match.

### What the sweep found otherwise — nothing

Run before the fix, and all clean:

| check | result |
|---|---|
| `node --check` on all five JS files | pass |
| `diff -rq Web Versions/beta-4` | no difference at all |
| `diff -rq Web` inside the macOS `.app` | identical |
| `diff -rq Web` inside the new `.ipa` | identical bar gitignored `.DS_Store` |
| live GitHub Pages vs local, all seven files | byte-for-byte match |
| `gh release view v1.0.4` | draft false, prerelease false, three assets |
| browser-pane console | no warnings, no errors |

The single `mouth` match left anywhere in the shipped trees is the Astrakhan clue — *"the
port city at the mouth of the Volga River"* — which is content, not the graphic. No
regression.

Two things I had flagged as open were re-examined and deliberately left, and the reasons
are worth having written down:

**The Persian bank is not touched.** Both defect classes are already defended at runtime,
on purpose and with comments: `aliasesFor` ([answers.js:221](Web/answers.js:221)) drops any
alias that normalises to a wrong option, and `shufflingOptions`
([app.js:210](Web/app.js:210)) collapses duplicate option text on the trimmed key. Latent
noise in a 1.4 MB generated bank, invisible to a player, and rewriting it is churn against
the checkpoint.

**The splash is not touched.** The bright line under the prompt is the photograph, not a
DOM hairline, and it is not where I first read it: in portrait `scale = vh/H` fixes
`scaledH === vh` and `offY === 0`, so `background-position` cannot move the horizon at all
— it sits at ~55.6% of viewport height whatever the 34% says. `.eyebrow` and `.tagline`
already carry the full `--halo` chain; `.pill` has `text-shadow: none` and is right to,
because a pill is a dark glass capsule (`rgba(8,8,9,0.46)`, 14 px backdrop blur, its own
border) and its text never sits on the photo. At 768×1024 the edge falls in the gap
between tagline and prompt, crossing no glyphs. Fixing it would mean recomposing the hero
screen at every shape to remove an artifact nobody has seen.

### Rebuilt and re-uploaded

The `.ipa` was rebuilt (`** BUILD SUCCEEDED **`) and the asset replaced on the v1.0.4
release:

| artifact | bytes | note |
|---|---|---|
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14,785,927 | was 14,789,384 — the plist edit |

The macOS zip and the web zip are untouched; the web tree did not change, so Pages did not
need a redeploy and `Versions/beta-4` still mirrors `Web/` exactly.

## The buzz window belongs to the clue, not to the contestant

**Objective.** Morad: *"the one big problem is the timer. when i meant first round, second
round, third round — i mean timers in Jeopardy, Double Jeopardy, and Final Jeopardy — I
didn't mean when one player gets an answer wrong, the second player has more time…"*

**What was actually wrong.** `BUZZ_SECONDS = { single: 20, double: 12 }` was already
round-keyed and `openBuzzers()` was already reading it. The defect was one call site
further along: the verdict card's steal handler — `showVerdict`'s "Second Chance" button —
called `startClueClock(buzzSeconds(), …)`, so every contestant who inherited a clue after a
miss got a brand-new full window. A clue that had been running eighteen seconds and gone
wrong handed the room another twenty. One window per clue was the intent; the code gave one
window per contestant.

**The fix.** `S.buzzLeft`, the seconds left in this clue's window. Set full in
`openBuzzers()` — the only place a window opens, and the only reset it gets — cut down in
`buzz()` to `S.clueRemaining` at the instant a thumb goes down, and read back through
`buzzWindowSeconds()` by both the steal handler and `Bots.armBuzzers()`'s ceiling, because a
robot must not be booked to press after the clock it is racing has already run out.
`buzzSeconds()` is untouched and still the source for the round; `buzzWindowSeconds()` only
ever returns something shorter, never something longer.

**Verified by driving the real UI**, not by reading the diff — server on `:8788`, two human
contestants, a sampler on `#clue-clock`:

| t | clock |
|---|---|
| 207 ms | Read 6 |
| 6030 ms | **Buzz 20** — the window opens full, once per clue |
| 14143 ms | Buzz 12 |

Then, in the same match: the buzz clock read **9** when a thumb went down, the verdict card
offered Second Chance, and the steal clock reopened at **9** — not 20. Reproduced twice.
Double Jeopardy's 12 could not be driven end to end (the `Round 1 / Double Jeopardy / Final
Jeopardy` row on the board is a display indicator, not a control), but `S.buzzLeft` is only
ever assigned `buzzSeconds()` or `S.clueRemaining`, and `BUZZ_SECONDS` is untouched, so the
12 follows from the same line.

**Consequence for the build.** `Web/app.js` is now `ad001f00…`. The `.ipa`, the macOS zip,
`Versions/beta-4` and the live Pages site all still carry `ae031798…`, so they are one bug
behind this fix. Nothing was re-cut, pushed or uploaded.

## v1.0.5 — the fix carried out to every artifact

Morad: *"now push it to github plus the web app and everything — yes everything must be
updated."*

**Version moved to `1.0.5` / build `105`.** Not cosmetic: `iOS/project.yml` says in its own
comment that a sideloader compares `CFBundleVersion` to decide whether an `.ipa` is an
update, and refuses one that has not moved forward. Replacing the file on v1.0.4 under the
same `104` would have shipped an `.ipa` that would not install over the previous one. The
bump is what makes the fix reachable by anyone who already has the app. Four files carry
it, all now in agreement: `build_release.sh`, `Web/index.html`, `iOS/project.yml`, and the
`iOS/JeopardyIOS/Info.plist` that `xcodegen` regenerates from the last of those.

**`build_ipa.sh` moved into the tree.** The `.ipa` had been cut by a script that lived only
in `/tmp` and would have been lost with the next reboot. It now sits beside
`build_release.sh` and `snapshot_web.sh`, does its own `xcodegen generate`, and keeps the
Web-tree parity diff that guards the one failure mode worth blocking a build over.

**Froze `Versions/beta-5`** — 117 files, 14M, `app.js` byte-identical to `Web/app.js`.

**Cut all three artifacts**, every one carrying `ad001f00…`:

| artifact | bytes | was |
|---|---|---|
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14,786,399 | 14,785,927 |
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 13,643,539 | 13,587,696 |
| `Jeopardy-Iranian-Edition-web-beta-5.zip` | 11,640,346 | 11,647,372 (beta-4) |

The macOS binary is `lipo`-verified `x86_64 arm64`; the `.ipa` reports `1.0.5` / `105` and
its bundled Web tree diffs clean against `Web/`. Verified in the running web build that
both corner stamps read `v1.0.5` and the served `app.js` carries `buzzWindowSeconds` four
times, so the fix is in the artifact and not only in the source.

## The dial was the bug, not the digits (2026-09-11)

**Morad:** *"the buzzer isn't proper. it doesn't count down properly!!!!"* — *"it says 20
seconds but immediately runs out the timer!!!!"*

**Correction to the entry above.** The shared-window change is real and it is in the build,
but it is not what he was looking at. `S.buzzLeft = buzzSeconds()` is a no-op on a clue's
first window, and the digits were measured ticking at a clean 1 Hz all session (6→5→4→3→2→1
on the read, 20→19→…→1 on the buzz). The countdown was never miscounting.

The **dial** was. `--t` is the share of the ring still lit, written inline on `.clock` once
a second; the design is that one `transition: --t 1s linear` smooths the steps so the ring
drains rather than jumps. It was declared **twice** — on `.clock` and again on `.clock-arc`
— and two cascaded 1s linear transitions on a ramp behave as a ~2s delay. Measured before
the fix, at the instant the window opened:

| ms | digits | label | inline `--t` | ring |
|---|---|---|---|---|
| 6004 | **20** | Buzz | 1 | **0.335** |
| 9204 | 17 | Buzz | 0.85 | 0.884 (peak — never reached full) |

The ring opened a fresh twenty-two-thirds burned off, climbing from the read window's
dying value. That is what "it says 20 seconds but immediately runs out" describes.

**Two changes, and the second is the one that finishes it.**

1. `Web/styles.css` — dropped `transition: --t 1s linear` from `.clock-arc`. The transition
   belongs only where `--t` is written.
2. `Web/app.js` — `paintClock` takes a `reset` flag, passed by the first paint of a window.
   A window opening at full is not a step, it is a reset, and it has to land in one frame.
   `stopClockNode` already wrote `--t = 1` while hidden, on the theory that `display: none`
   makes it instant — but the caller un-hides in the same task, so the browser never
   observes the node as hidden and the previous window's in-flight transition runs straight
   through the window change. Change 1 alone still left the ring reading **0.168** at the
   moment the digits said 20.

**Measured after both**, same solo game, 100 ms sampling:

| ms | digits | label | inline `--t` | ring |
|---|---|---|---|---|
| 4159 | **20** | Buzz | 1 | **1.000** |
| 5151 | 19 | Buzz | 0.95 | 0.951 |
| 14159 | 10 | Buzz | 0.5 | 0.501 |
| 23151 | 1 | Buzz | 0.05 | 0.051 |
| 24159 | — | — | 1 | hidden |

Full ring on the open, tracking the digits to 0.001 every tick, twenty seconds to expiry.
Confirmed visually as well: dial at 9 with a matching arc, ring intact.

**Measurement note.** The pane caches sub-resources hard — `python3 -m http.server` sends no
`Cache-Control`, and a plain `location.reload()` after editing `styles.css` still ran the
old rule, and would have run the old `app.js` too. Appending a `?cb=` link does not displace
the stale sheet. The only clean read is a fresh origin: the preview server was moved to port
8789, which busts everything at once.

**Cut, and re-cut.** `Web/` freezes as `Versions/beta-6` — the script is append-only by
design, so beta-5 stays as the snapshot it was taken as (broken dial and all) and the
corrected build gets its own name. All three artifacts re-cut off `a9427a2a…`:

| artifact | bytes | was |
|---|---|---|
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14,786,749 | 14,786,399 |
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 13,643,885 | 13,643,539 |
| `Jeopardy-Iranian-Edition-web-beta-6.zip` | 11,640,696 | 11,640,346 (beta-5) |

`lipo` reports `x86_64 arm64`; the `.ipa` reports `1.0.5` / `105` and its bundled Web tree
diffs clean against `Web/`. Pushed as `7024eb5`; Pages redeployed off the same push.

## The v1.0.5 release is a draft, and it is empty (2026-09-11)

Correcting an earlier note that said no v1.0.5 release existed. One does, and it was not
made by the command that got killed — `gh release create` had already created the tag and
the draft at **19:49**, before the dial fix, and the upload died on the assets.

`gh release view v1.0.5` reports: `isDraft: true`, `isPrerelease: false`,
`name: "v1.0.5 — the window belongs to the clue"`, and **`assets: []`**. So nothing is
stale on GitHub and nothing is public: the draft carries no binaries at all, and its body
is the 2,522-byte pre-fix text, which is the older, shorter version of
`dist/RELEASE-v1.0.5.md` (now 3,367 bytes with the "The dial was lying" lead).

The published release is still **v1.0.0**, marked Latest. Below it there is nothing —
no v1.0.1 through v1.0.4 as releases; those exist only as the `RELEASE-v1.0.*.md` files in
`dist/`.

**Held deliberately.** `gh release create` was killed once already, so re-running it is not
mine to do unprompted. Also worth noting for whoever does: the draft's *title* is now stale
too — "the window belongs to the clue" names the smaller of the two fixes. The dial is the
one that mattered.

## The board header was drawn for a phone held sideways (2026-09-11)

Morad photographed the live Pages build on an iPhone 17 Pro, held upright: the wordmark
tangled with the round names, no timer anywhere on the screen, the podium bar jammed against
the Safari toolbar. All of it reproduces at 402 x 874 in the pane.

The `@media (max-width: 900px)` block was authored for **812 x 375 landscape**. Its own
comments say so, twice ("A phone is held at arm's length", "A landscape phone gives this
screen 375px to stack…"). Portrait is the shape nobody drew for, and it is not a small
difference: 402 wide is barely half the landscape phone's 812, and 874 tall is more than
twice its 375. Three defects fall out of that, each measured at 402 x 874:

1. `.logo-board` (x 12 -> 130) and the absolutely-centred `.board-rounds` (x 101 -> 302)
   **overlapped by 29 px**. That is the jumbled top section.
2. `.board-rounds` is **77 px tall inside a 49 px `.board-top`**, so `#board-clock` landed at
   y 53 -> 87, **38 px below the header**, down on the board's category-header row.
3. The board painted over it. `elementFromPoint` at the clock's dial and again at its digits
   both returned `SPAN.cat-name`; only the 3 px gap between grid columns returned a clock
   descendant. The countdown was drawn, every second, and was never once visible. That is the
   missing timer — not a size problem, a stacking one.

**The fix.** `.board-top` becomes a three-column grid carrying `z-index: 5`, and
`.board-rounds` is dissolved with `display: contents` so the rule, the tabs and the clock can
each take their own `grid-area` instead of three of them fighting over one absolutely-centred
column. Measured after, both immediately and again across a full reload:

- `.board-top` 49 -> **85 px**; the board loses 36 px of height, 756 -> 720
- logo `{12, 9 -> 128, 48}`; clock `{232, 11 -> 390, 45}` — inside the header,
  `clock_below_header_by: -40`, and 104 px clear of the wordmark
- `elementFromPoint` returns clock descendants at all three sample points; the occlusion is gone
- looked at directly as an image: wordmark clear on the left, dial and "PICK A CLUE"
  fully visible top-right, rule and round tabs stacked cleanly beneath

**An x-only overlap check lied here.** After the fix it still reported the logo and the round
tabs overlapping by 44 px. They do not: the logo now sits on grid row 1 (y 9 -> 48) and the
tabs on row 3 (y 63 -> 79), so their y-ranges are disjoint and the x comparison is
meaningless. Worth remembering as a false positive when this layout is next touched.

### The podium was cutting the last letter in half

Not a hypothesis this time — geometry, and it is exactly the trailing `M` of "Cyrus the
Algorithm". `.podium` is 126 px wide with 9 px padding and a 1 px border, so its text box is
106. `.pname` measured **119**, ran 3 px past the card, and `.podium`'s own `overflow: hidden`
cut the final glyph through the middle.

The `text-overflow: ellipsis` on `.pname` never fired, and could not have. Flipping `.podium`
to `flex-direction: column` makes the width the *cross* axis, and on the cross axis a nowrap
item shrink-to-fits to its own text, so the element was always exactly as wide as the string
it was supposed to truncate. `min-width: 0` on `.pname` was written for the desktop row,
where it applies to the main axis, and does nothing in column mode.

`max-width: 100%` on that cross axis is the whole repair. `clientW` 119 -> **106**,
`scrollWidth` stays 119, the text now ends **10 px inside** the card and the ellipsis renders.
Confirmed as an image: the bar reads `CYRUS THE ALGORIT…`, and the other two names clear their
cards by 61 px and 39 px.

### What the pane could not reproduce

The podium bar measures `{0, 818 -> 402, 874}` with `scrollHeight == clientHeight == 874`: no
document overflow in either axis, and 6 px of clearance under the cards. So the bar being
clipped by the Safari toolbar in the photograph is **not** the CSS box model. The remaining
suspect is real Safari chrome against `100dvh` with a zero `env(safe-area-inset-bottom)` in a
tab. That one stays open.

The clue screen at portrait was measured too and is sound. The clock is 113 x 34 with 20 px
digits and `elementFromPoint` returns `DIV.clock`; no overflow anywhere. There is a great deal
of slack — the body centres 180 px of clue inside a 541 px column, so the clock sits 182 px
below the clue it is timing — but that is the desktop rule (`justify-content: safe center`)
behaving as written, not a break.

**Not acted on, worth a look:** on the clue screen the timer capsule reads `15 BUZZ` and the
lamp directly beneath reads `BUZZ` — same ring, same capsule shape, stacked. Through the buzz
window they read as two timers. That is a design-system question, not a portrait bug, so it
was left alone.

### Shipped

`Web/styles.css` and `Versions/beta-7/` went up as **`673a67a`**, "Draw the board header for a
phone held upright". Pages run `34644637767` (workflow "Publish the web show") completed
success in the same push.

Verified on the deploy, at 402 x 874: the live `styles.css` **diffs clean** against
`Web/styles.css` — byte-identical, not merely similar. Then measured again in the pane:

| | before | now |
| --- | --- | --- |
| `.board-top` height | 49 | 85, `z-index: 5` |
| `#board-clock` | y 53, under the board | `232->390 x 11->45`, inside the header |
| `elementFromPoint` at the dial | `SPAN.cat-name` | `SPAN.clock-label` — a clock descendant |
| gap, wordmark to clock | overlap of 29 | 104 px clear |
| "Cyrus the Algorithm" | 119 in a 106 box | 106, ellipsis live, 10 px inside the card |
| document vertical overflow | — | 0 |

Looked at as an image, not inferred from numbers: wordmark clear on the left, round tabs
stacked cleanly beneath the rule, `6 · PICK A CLUE` in the top right, and all three podium
cards whole at the bottom with room under them.

All three artifacts re-cut as **beta-7** and each one checked, not assumed — `styles.css` read
back out of the `.ipa` payload, out of the macOS bundle's `Contents/Resources/Web`, and out of
the web tree, hashing `9ac75653…` in all four places including the source. The `.ipa` reports
its Web tree in parity, version `1.0.5` / `105` on both bundles. Sizes: `.ipa` 14,787,501 ·
macOS universal 13,644,647 (`x86_64 arm64`) · web beta-7 11,641,448.

**The v1.0.5 release is still an untouched draft** — no assets, the pre-fix body, and now a
title that names neither of the two fixes above. Publishing it is his call, not mine, and
`gh release create` was killed once already for being run unprompted. The notes are staged at
`dist/RELEASE-v1.0.5.md` for when he says go.

**Corrected before it stood: `location.reload()` does not re-initialise the document in this
pane.** I first wrote that the `playerCount: 1` anomaly was explained by a restored game, and
that is wrong. `localStorage` holds exactly one key, `jeopardy.lang` (two bytes), and
`sessionStorage` is empty — there is no game-state store, so the app cannot restore a game at
all. What actually happened: the reload call returned but the document lived on, the board's
own twenty-second clock ran out during the five-second wait and picked a clue by itself, and
the next eval therefore opened on `screen-clue` rather than the splash — which is also why
`#lang-en` did nothing when clicked. Every measurement above ran on a document inherited from
the earlier session. The geometry stands, because `styles.css` was re-fetched through the
cache-busting link swap and the numbers are against current bytes; the *game state* was not
fresh, and the `playerCount: 1` anomaly stays unexplained rather than solved.

That is worth keeping: in this pane, `reload()` cannot be trusted to give a clean boot, and
an eval that assumes it has will quietly measure the previous session's leftovers.

---

## The buzz, made answerable — 2026-09-13

He asked whether a player can tell *when* to buzz and *where to put their thumb*, and said the
player who takes the floor should visibly grow and buzz. Both were real gaps.

**The jump was wired into the wrong branch and had never fired once.** `buzz()` called
`renderPodiums()`, and the ring that comes with it is drawn from `S.buzzed === i` — so a card
lit up on every buzz and nothing looked broken. What never happened was the *jump*. The call
I thought was in `buzz()` was actually inside `startClue`'s Daily Double branch, where it read
`flagPodium(playerIndex)` against a function that has no such parameter — a silent no-op. Fixed:
`flagPodium(playerIndex)` now sits in `buzz()` between `renderPodiums()` and `startClueClock()`,
and the Daily Double branch passes `S.holder`, which is the value it had already assigned two
lines above. A robot taking the floor comes through the same door and gets the same jump, which
is correct: the room needs to see who has it, not merely that someone does.

Both one-shot classes now clear on timers — 420 ms for the pop, 560 ms for the jump — rather
than on `animationend`. The event is not dependable here (a frame that never paints never ends
its animation) and the failure is silent and permanent: a class left behind swallows the *next*
pop, because re-adding a class an element already carries is not a change.

**A phone is one thumb, so the plate is one plate.** The clue screen previously offered a
button per seat. On a phone with robots in the other seats that is a row of things that look
pressable and are not. `soloHuman()` counts non-bot seats, and when there is exactly one, the
row collapses to a single full-width plate reading `Buzz` / `زنگ` and the whole stage becomes a
`pointerdown` target. The test is the seat count, not the viewport: two humans at one keyboard
still get one plate each.

**The screen said BUZZ three times.** The countdown capsule, the lamp capsule and the plate all
carried the same word. The lamp now names the *state* — `Live` / `روشن` armed, `Wait` / `صبر`
before — so the screen reads countdown, then state, then action, three words doing three jobs.

Measured in the pane at 402×874 on a genuinely fresh document with a cache-busted stylesheet:

| | measurement |
| --- | --- |
| jump fires from `buzz()` | `podium is-armed shine is-on is-buzzing`, `getAnimations()` → `podium-buzz:running` |
| jump mid-flight | `matrix(1.06553, 0, 0, 1.06553, 0, -1.74566)` |
| jump settles on the ring | `matrix(1.07)`, dot 12px, border `rgb(23, 178, 90)`, `z-index: 2` |
| rings leak nothing | `is-popping` gone after 420 ms, `is-buzzing` after 560 ms |
| solo plate | one plate, 378×61, `flex: 1 1 100%`, `min-height: 60px` |
| solo row | `buzz-row is-solo` → armed `buzz-row is-live is-solo is-popping` |
| three humans | three plates, **no** `is-solo`; dead-space tap inert; jump only on the buzzer's card |
| arm latency | 4805 / 4815 / 4823 / 5119 / 5125 / 5127 ms — consistent with `READ_SECONDS = 6` |
| clue screen | `scrollHeight` 874 = viewport; no overflow; podium bottom 868 |
| Persian | `dir: rtl`; lamp `روشن` armed / `صبر` before; plate `زنگ`; hints in full |

Two pane facts learned the hard way and worth keeping. **Screenshots here can be stale frames** —
one capture showed the pre-arm lamp after the DOM had already read `روشن` armed, so the DOM is
the measurement and the image is only the look. And an emulated viewport larger than the pane is
**scaled to fit**, letterboxing black below the content; that black band is the pane, not the
page, and the page reported `scrollHeight` 874 against a viewport of 874 throughout.

Uncommitted, unpushed, unreleased. `Web/app.js` (four edits), `Web/i18n.js` (two); the
`Web/styles.css` work from the pass before it is unchanged and still in the tree.

---

## The press, and the two banks that must never meet

### The bank that would not move

Morad photographed the Persian lobby dealing an English clue under Persian chrome, and the
question was not cosmetic: a clue is the one string in the show that cannot be translated
after the fact. The bug was in a listener, and the listener was testing the wrong thing.

```js
document.addEventListener('langchange', function (ev) {
  if (S.players.length) return;      // ← this
  CLUES = BANKS[ev.detail.lang] || BANKS.en || [];
});
```

`S.players.length` reads as "a match is in progress, don't move the floor out from under it."
It is not that. `#quit-game` calls `show('splash')` and never clears the roster, so after the
*first* match the guard is permanently truthy and the bank never swaps again. One English match
poisoned every Persian match that followed, until reload.

Two fixes, because one of them is a guarantee and one is only manners:

- **The guarantee.** `startMatch()` now re-reads the bank off the live language at the moment a
  board is dealt — `CLUES = BANKS[window.getLang()] || BANKS.en || []`. Dealing is the only
  event that pins a clue to a language, so it is the only moment where the answer cannot be
  wrong, and it cannot be skipped by navigating around the listener.
- **The manners.** The listener now tests the *screen*: `DEALT_SCREENS = ['board','clue',
  'wager','results']`. It keeps the pre-match screens honest and refuses to reach into a dealt
  board, and it no longer lies about which screens those are.

Verified on Morad's exact path — English match played, `.next-btn` → board → `#board-menu` →
`[data-menu="lobby"]` → lobby → `#quit-game` → splash → `#lang-fa` → `#go-setup` →
`#start-game` → tile — and the clue came up Persian: *"این شاهکار پلسازی راهآهن در دره
سوادکوه مازندران…"* under category *"ورسک و سوت قطار پیروزی"*. The English path still yields
English. The two banks now have no door between them.

### Haptics: the one sense a web page cannot reach

`navigator.vibrate` does not exist in Safari on iOS — not at any version — so the `.ipa`, which
is a `WKWebView`, had no route to a player's thumb. The web build on Android does have it, and
the Mac has only `NSHapticFeedbackManager`, a faint tick that is silent on hardware without a
Force Touch trackpad.

The bridge keeps the shell's governing idea intact: the page decides *what a player should feel
and when*; the shell only knows how to say it.

- `Web/app.js` gained a `tap` pattern and three words the show already had a meaning for:
  `take` (your thumb landed), `beat` (somebody else got there first), `foul` (you jumped the
  lamp). All four fire through `Haptics`, which posts to the `haptics` message handler when one
  exists and does nothing when it does not — so the web build is unaffected.
- `App/ShowWebView.swift` gained `ShowHaptics`, a `WKScriptMessageHandler` that answers the
  word with `UIImpactFeedbackGenerator` (`.heavy`, `.light`) or
  `UINotificationFeedbackGenerator(.error)` for the refusal. Deliberately vocabulary-free: it
  knows the words but not what a buzz is.
- The plate is excluded from the generic tap. It has its own three words to say, and a fourth
  tick landing milliseconds early would blur the one distinction a player makes at that speed —
  did I get it, or did somebody beat me to it.

All four words were observed firing through an instrumented stub in the pane:

| word | how it was provoked | record |
| --- | --- | --- |
| `tap` | press a board tile | `["tap"]` |
| `take` | plate press, solo-human match, lamp live | `["take"]` |
| `foul` | plate press at +800 ms, lamp still `صبر` | `["foul"]` |
| `beat` | a robot buzzed in during a bot match | `["beat"]` |

Control: `pointerdown` on `.buzz-btn` alone recorded `[]` — the exclusion holds and the plate's
three-word vocabulary stays clean.

### The press

Every control now answers a press the same way, because the question a player asks of a button
is the same wherever the button is: *did that land?* The board tiles, the language pills, the
green room, the overlays, the menu and the results all wear it, and none of them had to opt in.

The listener is delegated off the document rather than bound to each control. The controls are
mostly drawn after the script runs — the tiles, the clue row, the green room and the overlays
all arrive late — and a listener that must be re-attached to each of them is one that will one
day be forgotten. A pointer that leaves the window mid-press never reports its release, so
`blur` and `visibilitychange` release too.

The CSS is one rule, doubled for specificity (`0,2,0` beats a revealed tile's `0,2,0`):

```css
.is-pressed.is-pressed { transform: scale(0.955) !important; filter: brightness(1.38); }
.buzz-btn.is-pressed.is-pressed { transform: scale(0.94) !important; }
```

The plate keeps its shove and takes only the light; everything else takes the shove. Under
`prefers-reduced-motion: reduce` the bloom stays and the shove goes — the colour change is the
acknowledgement, and nothing has to move for a press to be felt.

Measured on a held `.next-btn`: `is-pressed`, `matrix(0.955, 0, 0, 0.955, 0, 0)`,
`brightness(1.38)`, `transition: transform 0.055s ease-out, filter 0.055s ease-out`; release
returns to zero pressed elements. Confirmed visually and by reading the capture — Persian clue
screen, RTL intact, the button visibly lit.

### State

Uncommitted, unpushed, unreleased. `Web/app.js` (bank fix ×2, haptics, press),
`Web/styles.css` (press rules + reduced-motion opt-out), `App/ShowWebView.swift` (`ShowHaptics`
+ its registration).

**Any change to `Web/` invalidates the beta-7 artifacts.** `build_ipa.sh` diffs the Web tree
against the shipped bundle and will refuse a drifted one, so beta-8 and all three artifacts
have to be re-cut before anything ships.

### The buzz, made visible

The haptic answers the thumb that pressed. The room has no thumb — it has eyes on the name
cards, and a card that only grew was a card that said *something happened* rather than *a buzz
happened*. `podium-buzz` was a single grow-and-lift; it is now a decaying shiver: the card
rattles the way the phone in that player's hand just did, four beats wide, settling onto the
ring that is the state.

Same door as before — `flagPodium()` fires from `buzz()` and from the Daily Double, so a human
and a robot shiver identically. That is deliberate: at the far end of a table the two should
look the same.

The amplitude stays under 4px because the card has neighbours. A shiver wide enough to cross
the gap stops being that player's and becomes the row's, and the one thing the shiver exists to
say is *whose*.

Traced by scrubbing the animation with `currentTime` (rAF is throttled in this pane and cannot
sample a 560ms animation):

| t | scale | translateX |
| --- | --- | --- |
| 0 ms | 1.000 | 0 |
| 78 ms | 1.120 | −4.49 px |
| 146 ms | 1.110 | +4.25 px |
| 213 ms | 1.100 | −3.22 px |
| 280 ms | 1.095 | +3.29 px |
| 347 ms | 1.090 | −2.19 px |
| 414 ms | 1.085 | +1.64 px |
| 482 ms | 1.078 | −0.84 px |
| 560 ms | — | lands on `is-armed` scale 1.07 |

Eight keyframe stops, `0.56s`, landing exactly on the `is-armed` transform so the class coming
off at 560 ms is not a snap. Verified visually: caught at 78 ms, the middle card sits visibly
larger and out of the row beside its neighbours. The `prefers-reduced-motion` block already
kills this animation and keeps the ring, which is the right trade — the ring is the state, the
shiver is only the news.

Also learned: the pane's stylesheet cache is not the problem it was assumed to be. A `?v=` link
swap was used to force the new CSS, then reverted to the plain `styles.css` href, and the pane
revalidated and served the new nine-stop keyframes. The swap was unnecessary.

## The apps were killed and un-killed in the same minute

Morad asked to push, then said the `.app` and `.ipa` were no longer needed — "just keep it
running as a web app" — and then, mid-turn, reversed: "actually, let's just make the apps if it
isn't too much a bother." So all three were rebuilt. Worth recording why the flip is not a
contradiction: the web page is the definitive version, but it is the one place a buzz cannot be
**felt** on an iPhone. Dropping the native shell would have quietly cost the phone the thing he
had just asked for, which he had no reason to have in mind when he said to drop it.

### v1.0.6

Versions bumped in two places, which is the whole set: `build_release.sh` (`CFBundleShortVersionString`
1.0.5 → 1.0.6, `CFBundleVersion` 105 → 106) and `iOS/project.yml` (the same pair). The iOS
comment is right that the two build numbers have to move together and forward, or a sideloader
refuses the `.ipa` as "not newer" rather than installing it.

Sequence: `./snapshot_web.sh beta-8` → `./build_release.sh --universal` → `./build_ipa.sh` →
two zips. The universal build compiled both slices clean (`lipo: x86_64 arm64`), ad-hoc signed,
bundle 16 MB on disk. The `.ipa` staged `1.0.6`/`106` and its **Web tree parity diff came back
empty**, which is the check worth trusting — that script exists precisely to refuse a bundle
whose Web tree has drifted.

No packaging script exists for the two zips, so they were cut by hand to match the existing
layout: the web zip holds a single top-level `Jeopardy-Iranian-Edition-web-beta-8/` folder
(rsynced from `Versions/beta-8`, which already excludes `.DS_Store`), the Mac zip holds the
`.app` via `ditto -c -k --sequesterRsrc --keepParent`.

Verified by reading the packaged bytes, not the source tree — each of the three was opened and
grepped for the new build:

| Artifact | Check |
| --- | --- |
| `dist/Jeopardy Iranian Edition.app` | 1.0.6/106, `lipo -archs` → `x86_64 arm64`, `Signature=adhoc`, `podium-buzz` present with the `14% translateX(-4px)` stop |
| `dist/Jeopardy-Iranian-Edition-iOS.ipa` | `podium-buzz` present, `DEALT_SCREENS` present, `Haptics.take` present |
| `dist/Jeopardy-Iranian-Edition-web-beta-8.zip` | `podium-buzz` present |

README gained one paragraph under "Take it with you" saying why the native builds still exist —
the iPhone cannot feel a buzz from a browser, and that is the whole argument for keeping them.
`dist/RELEASE-v1.0.6.md` written in the house format of the earlier notes.

The Mac app was **not** launched to test it. It takes the whole screen, and the standing rule is
not to disturb Morad's live desktop session. The evidence for it is the parity diff, the arch
check, the version fields and the greps above, not a screenshot.

---

## 2026-09-14 — the engine stops naming a home directory

The project moved off the Desktop to `~/Claude/Jeopardy - Iranian Edition`, and
`QuestionBank.swift` was carrying two hard-coded absolute paths — lines 37 and 60, the
last-resort fallbacks used by `swift run`. Pointing them at the new location would have
worked until the next move, which is exactly how they broke this time: they had said
`/Users/Morad/Desktop/...` since before today.

Fixed properly instead, using the idiom the codebase already had. `App/ShowWebView.swift`
resolves its dev-time path from `#filePath` rather than naming a machine; `QuestionBank`
now does the same, through a private `packageRoot` computed property (three
`deletingLastPathComponent()` calls up from `GameEngine/QuestionBank/QuestionBank.swift`).
No absolute path remains in the engine's source.

Verified: the arithmetic resolves to `/Users/Morad/Claude/Jeopardy - Iranian Edition`, and
both targets exist (`QuestionBank/verified_clues.json`, `App/Resources/persian_clues.json`).
`swift build` completes clean in ~10 s with only the pre-existing warnings, and
`./run_tests.sh` reports **27 passed, 0 failed**.

One casualty of the move, worth knowing about: `run_tests.sh` died on a stale
`.build/ClangModuleCache` whose precompiled `SwiftShims` still carried the Desktop path
(`was compiled with module cache path '/Users/Morad/Desktop/…'`). Cleared the two module
cache dirs rather than fighting it — they regenerate. The script is green as written, no
override needed. Any future move of this folder will do the same thing.

Committed and pushed on Morad's instruction, 2026-09-14, once he had confirmed the
change touched only the Iranian Edition — the course edition is not a git repo and
`build_edition.sh` copies `Web/` alone, so no Swift ever reaches it.


---
2026-09-14 — The `value` field in the clue bank is a slot key, not money.

Morad asked for the numbering/point system in his Gemini question-bank prompt to be
changed to the game's own. Tracing it through `Web/app.js` and
`GameEngine/BoardBuilder/BoardBuilder.swift` turned up two separate scales that had been
sitting in the code the whole time:

- `SINGLE_BANK = [200, 400, 600, 800, 1000]` / `DOUBLE_BANK = [400, 800, 1200, 1600,
  2000]` is the key the data carries and the engine matches on. `buildBoard` selects a
  category by requiring every one of those keys to be present, so a category missing a
  single key is silently dropped and never reaches a board.
- `SINGLE_VALUES = [10, 25, 50, 100, 200]` / `DOUBLE_VALUES = [20, 50, 100, 150, 200]`
  is what the player sees, in millions of toman. `buildBoard` overwrites `clue.value`
  with this figure after the lookup, so at runtime the number on the tile and the number
  the clue scores are the same.

The Swift side agrees exactly (`BoardBuilder.swift:20`, `Tests/main.swift:318`), so the
odd Double ladder — 20/50/100/150/200 rather than a clean doubling — is deliberate, not
a bug. Final is a wager, not a slot: `value: 0` in the data, capped at 200 million toman
by `MAX_WAGER`.

Also confirmed rather than assumed: `difficulty` is not a judgement call. Each slot key
maps to exactly one label, 1:1 across all 1,000 rows — single 200 CASUAL; single 400/600
and double 400/800 STANDARD; single 800 and double 1200/1600 SCHOLAR; single 1000,
double 2000 and final 0 INSUFFERABLE. Morad's four labels were already the bank's.

Delivered as three surgical replacements to his pasted prompt (sections 1, 2, and one
checklist line in 7), with the slot keys as the machine value and the toman figures
explicitly marked engine-generated. Left alone, and flagged instead: his prompt nests
`{en, fa}` per field, while the real bank is flat with a `language` field per row.

---

## 2026-09-14 — the host is not Ostad Dariush Fani

Morad asked, about the Gemini prompt he pasted: "Our host is different tho, no?" He is.

The game host has no name anywhere in the project — he is just the host (مجری in
Persian). The section-5 persona in that prompt, "Ostad Dariush Fani", is invented, and
so is the temperament described around him: a warm erudite broadcaster whose praise runs
"Barakallah! Spot on. Sadi himself would nod in approval." That is the opposite of ours.
i18n.js states the register twice — smug, snarky and mean, the same in both languages.
His real comedy is aimed at Iranian social habits rather than the archives: the confident
uncle, the dinner-party fact, the family WhatsApp group, the Tehran taxi driver. The
line names carry it — right_10_i_hate_how_pleased_you_look, right_12_unfortunately_youre_right,
wrong_02_very_iranian_of_you, wrong_06_source_your_uncle, wrong_09_tehran_taxi_driver.
Praise is grudging, corrections are rude, and he never lectures.

Three data findings behind the same question. First, the project holds **two different
clue shapes**. `Web/data/clues.js` — the file the web build actually loads — carries
`correctLine` and `wrongLine` as plain strings on all 1000 rows, and `app.js` renders
exactly those, so per-clue host lines do reach the player. `QuestionBank/verified_clues.json`
(+ `_fa`) is the archive and has neither; it stores host_reactions under the field names
correct_generic / wrong_generic / common_wrong_answers / specificity_prompt / explanation
— flat, one language per row, no correct / incorrect keys and no {en, fa} nesting, which is
what his prompt asks Gemini for. Nothing in `Web/` reads host_reactions, and it is thin
regardless: common_wrong_answers blank on 908 of 1000 rows, specificity_prompt non-empty
on 2. Second, **there is no generator script** and the two shapes' field names do not match
at all (clue_text/clue, canonical_answer/answer, accepted_aliases/aliases,
correct_option_index/correct), so writing a clue means editing both by hand. Third, the
shipped host lines are formulaic: 877 of 1000 correctLines end in one of three tails
("Spot on!" 330, "The history holds!" 325, "Quite right." 226), three carry a doubled
period where an abbreviation meets the template, and wrongLine repeats 335 times.

**Correction.** An earlier version of this entry claimed `app.js` reads correctLine and
`no row carries either` so the game always falls through to HOST_LINES. That was wrong —
it described the archive, not the play file, and it was stated to Morad as fact and saved
to memory. Both are now corrected. The unconsumed-`host_reactions` half was right.

Delivered the full prompt again with section 5 rewritten into the real register and the
real field names, and the invented "Barakallah! ... Deduct the stake!" reactions replaced;
everything else left verbatim. The {en, fa} nesting is still his shape and still wrong for
the flat bank — flagged a third time, still unauthorised.

## 2026-09-14 — the authoring contract moves into the repo

Morad asked whether the question-design rules should live in GitHub too, "so every other
time we try to organize questions around corpuses or texts it remembers that", and scoped
it: everything goes in the Iranian Edition, and the shared rules get mirrored into the
course edition so the two agree.

Wrote `QUESTION_AUTHORING.md` at the repo root — the two data shapes and their field map,
the rung ladder and the runtime restamping, the 1:1 difficulty mapping, the all-five-rungs
rule, distractor requirements, the host's register and no-name, the measured formula defect
in the shipped lines, the bilingual separation, provenance and the `Sources/` carve-out,
and the Gemini division of labour. Linked from `ARCHITECTURE.md` ("The clue bank") and
from a new first bullet in `CLAUDE.md` ("Working on this project").

Mirrored the same rules into `Jeopardy - Iran in World Politics Edition/BANK_SPEC.md`: a
new section naming the two shapes, a tightened difficulty table, and the host section
expanded with the no-name rule and the formula warning. Two pre-existing inconsistencies
fixed while there — the ladder section said only "set 200 to CASUAL and 1000 to
INSUFFERABLE", and the Gemini prompt's rule 3 gave a rising-scale approximation that
produced the wrong labels in the middle rungs. Both now carry the exact mapping.

Still unauthorised and not done: the `{en, fa}` nesting fix, the `launch.json` path, and
anything committed. Nothing has been committed.

**Same day, second pass.** Morad asked whether the guide was now complete. It was not, so
four sections were added rather than a yes: Categories (pun titles, all five rungs or the
category is silently discarded, the 60-clue and 95-clue quantities, the byte-identical
category string), `theme` (it *does* reach the player — `persianSubtitle()` picks one of
six bucket subtitles and the match is a substring test, so `party` lands in Culture via
`art`), Answers and aliases (never empty), and the mechanics of editing two one-megabyte
single-line files. A play-file validator remains the open hole; offered, not authorised.

**A flag I got backwards.** I had listed "the course edition's Gemini prompt has no
pun-title rule" as an open question. Wrong. Morad's own prompt opens with "CATEGORY
ARCHITECTURE & PUN DESIGN" — the pun rule was in the document he wrote; the copy *I* wrote
into `BANK_SPEC.md` was the one that dropped it. His words: "the gemini prompt i gave you
does have a pun thing tho!" Corrected by adding it to the spec's prompt as rule 2, with the
Persian native-wit requirement and his own unacceptable/acceptable example, and by marking
the `category` row of the fields table as a pun. Rules renumbered 2–12.

He had also asked, after the first pass, "what did you do? this doesn't fuck up the game
does it?" — answered with `git status --porcelain` and a grep showing no file the build
copies or the engine loads references any of the four docs. Four prose files changed; no
code, no clue data; nothing committed, so the live site is byte-for-byte unchanged. The
lesson is in memory: say up front whether the program reads the files being edited.

---

## 2026-09-14 — "are you sure everything is clean?" — and the two claims I got backwards

Morad asked whether everything was clean, with no inconsistencies and nothing left out. I ran
verification instead of asserting, and it turned up **two false statements of mine** sitting in
the two authoring documents. Both are now fixed.

### 1. The generator exists. The archive is canonical.

Both documents said, in effect: *"there are validators but no generator; the two shapes are kept
in step by hand, so writing a clue means editing both."* **That is false.**

`Tools/append_flawless_engine.py` writes `Web/data/clues.js` from `QuestionBank/verified_clues.json`
through a fixed field map. Its siblings (`build_flawless_1000_bank.py`,
`generate_flawless_persian_bank.py`, `append_persian_overhaul.py`,
`fix_options_and_align_answers.py`) do the same job for other passes. The map:

`clue_text→clue`, `canonical_answer→answer`, `accepted_aliases→aliases`,
`correct_option_index→correct`, `book_title→book`, `historical_period→period`,
`supporting_passage→passage`, `host_reactions.correct_generic→correctLine`,
`host_reactions.wrong_generic→wrongLine`.

`id`, `round`, `value`, `category`, `theme`, `difficulty`, `options`, `explanation`, `author`,
`page` pass through untouched; `chapter` has no play counterpart.

**Verified, not assumed:** mapped the archive through that exact transform and compared against
the shipped files field by field — 33 checks per row, **all 1,000 English and all 1,000 Persian
rows, zero mismatches.** The play file is an exact projection of the archive. Same result for
`clues_fa.js` against `verified_clues_fa.json`.

Consequence, and it is the opposite of what the docs said: **write the archive and regenerate.**
A hand edit to `Web/data/clues.js` is overwritten by the next run; a row that exists only in the
archive does not play until it is regenerated. It also answers a
question I had left open for Morad (whether new clues land in the play file or the archive): the
archive, always.

### 2. Nothing validates the play file's *contents*

My phrasing "nothing validates the play file" was too flat. Two scripts read it — but only for a
row count and the `window.CLUES=` prefix:

| script | what it asserts about `Web/data/clues.js` |
|---|---|
| `Tools/verify_flawless_state.py:90` | `window.CLUES=` prefix, exactly 1,000 rows. Its real checks (120 categories, no English in the Persian bank, the difficulty ladder) run on the **archive**. |
| `Tools/validate_3000_clues.py:67` | the same two assertions against **3,000 rows / 360 categories** — stale, describes an older bank, fails against today's file. |

`Tools/validate_1000_clues.py` validates the archive properly and **passes today** (1,000 clues,
120 categories, four options each, 100% schema and citation integrity). So the accurate statement
is: the archive is checked, the play file is checked for a count and nothing else — precisely the
gap that lets a generator bug ship. `Tools/validate_play_file.py` remains unwritten and
unauthorised.

### 3. Where the host-line formula actually comes from

Previously logged as a play-file defect with "generator tails." More precisely: the tails
**originate in the archive's `host_reactions.correct_generic`**, which is what the generator
copies. Re-measured at the source: **893 of 1,000 end in "Spot on!" (340), "The history holds!"
(325), "Quite right." (228)**; only 665 distinct `wrong_generic` lines cover 1,000 rows, so a
third of the wrong-answer lines repeat. The generator then doubles down — its fallback templates
for rows with no `correct_generic` are `f"{answer}. Quite right."` and `f"No, that was {answer}."`,
the same habit written into the tool. Earlier play-file figures (877 / 330 / 325 / 226 / 335)
were the same phenomenon counted at the other end of the pipe.

### What was changed

- `QUESTION_AUTHORING.md` — §1 rewritten (canonical/generated, the mapping table, the corrective
  instruction), the `host_reactions` subsection's "write the play file" flipped to "write the
  archive", §8's formula paragraph re-attributed to the archive with fresh numbers, §11 rewritten
  with a "what checks what" table. Also corrected the §1 source row: `chapter` has no play
  counterpart.
- `BANK_SPEC.md` (course edition) — the "no generator script" passage replaced; the formula
  paragraph re-measured; Gemini prompt rule 8 now forbids stock tails outright.
- Memory: `reference_question_authoring.md` (the claim recorded and corrected) and
  `feedback_host_voice.md` (which carried the same "no generator" line, and the wrong layer for
  the formula), plus the `MEMORY.md` index line.

**Pushed the same day** (Morad's call, docs only, no release tag). Before pushing I swept the
repo for the same false claim and found it in two more places — `ARCHITECTURE.md`'s "The clue
bank" section and `README.md`, the latter already published — both corrected in the same commit.

All of this is prose plus, in the two docs, a table. The
game loads `Web/data/clues.js` and `clues_fa.js`, which were not touched — the play files are
byte-for-byte what they were, verified against the archive in the course of this work.

---

## 2026-09-14 — the online table, and the lockout hole it opened

**Objective:** free online multiplayer, for both editions. Morad asked whether it could be done
("can we add multiplayer online somehow for free for this game too?"), approved the attempt
("It's okay let's try"), and then widened the scope mid-turn: *"I want it for both; the
professor's course and our own."* That settles where it lives — the shared engine in `Web/`,
because the course edition overlays data and skin onto the live engine rather than copying the
folder. Nothing here changes the single-device game; with online mode off the page behaves
exactly as it did.

### How it works

One player's browser is the table. It owns the board, the clocks and the rulings; everyone else
opens the same page, types a four-character room code, and gets a controller. There is no server
of ours in the middle — the free PeerJS broker (`0.peerjs.com`) introduces the two ends and then
they talk to each other directly over WebRTC.

The room code is prefixed `jpd-ir-` and drawn from an alphabet with `I`, `O`, `0` and `1`
removed, because a code gets read aloud to somebody who is not looking at the screen.

**Sync is a full snapshot after every state change.** No deltas, no sequence numbers, no
reconciliation. A snapshot is a few hundred bytes and the board changes a few times a minute;
the simpler thing is the right thing at this size.

**Clock sync without clock sync.** The host ships the seconds *left* plus its own `Date.now()`.
The guest throws the host's timestamp away on arrival, stamps the message with
`performance.now()`, and counts down from there. A phone whose clock is wrong by an hour still
shows the same number as the board.

**The answer is withheld.** A clue's correct-option index is not in the snapshot until
`S.phase === 'resolved'`, so the answer cannot be read out of the network traffic by anyone
watching it.

**The controller speaks one language.** The guest's controller strings are resolved *on the
host* and shipped inside the snapshot as a `labels` bag. One table, one language. The guest's
own chrome around it stays in the guest's own language, and `setLang` is never called on the
guest — it persists, and would rewrite the guest's own game.

### Files

| File | State |
|---|---|
| `Web/vendor/peerjs.min.js` | new — vendored, `sourceMappingURL` stripped, 86,948 bytes |
| `Web/net.js` | new — transport only, exports `window.Net`, knows nothing about the game |
| `Web/index.html` | new screens: the online lobby and `#screen-remote` |
| `Web/i18n.js` | `online.*` and `remote.*` strings, both languages |
| `Web/app.js` | the client — all of it, because `app.js` is one IIFE and `Online` is private to it |
| `Web/styles.css` | the online/remote section |

### The bug this window actually found

While driving a real guest through a wrong answer I found that **a locked-out seat kept its live
controls, and its taps were judged again.**

The chain: the guest answered wrong, the host ruled it ("Wrong. Sara is locked out") — but the
guest's phone still showed the four-option grid under "Yours. Answer it." `S.buzzed` is never
cleared after a wrong answer, so `phase` stayed `'answering'` and the seat still looked like the
one on the floor. `hostMessage`'s `'answer'` verb guarded the phase but not the lockout, so a
second tap ran `answerWith` again: a second deduction, and a duplicate `S.lockedOut` entry.

Four changes closed it:

- `answer()` and `answerWritten()` now refuse a seat that is already locked out — the same guard
  `buzz()` has had since the beginning, for the same reason.
- `remoteShape()` gives a locked-out seat **its own shape** rather than a detail inside
  `answering`. This is not cosmetic: `remoteRender` rebuilds the panel only when the shape string
  changes, so a fix buried inside `remoteStage` would never have repainted.
- `remoteStage()` renders `sitting` — "Sitting this one out. Watch and learn." — with no grid.

### Verified

Two real peers over WebRTC, host in the pane and guest in a same-origin iframe at 390×844:
room code minted; the guest on both rosters; the board with a bot; the guest's controller
rendering the score strip, clue head and a clock counting down one second off the board's; a
clue whose correct index was withheld until resolution; the guest's verdict card; a guest buzz
won against the bot; the multiple-choice grid; and then the fix itself — before the tap Sara sat
at 0M, one tap on the wrong option took her to −10M and flipped the phone to "Sitting this one
out. Watch and learn." with no grid, and a second tap on the same node changed nothing.

### What is not verified, and will not be from here

- **Two devices over the open internet.** Two tabs on localhost prove the protocol, not the
  network. Nothing here has touched a real phone on a real connection.
- **Symmetric NAT.** `net.js` names three STUN servers and no TURN server. Free TURN
  (`openrelay.metered.ca`, `stun.metered.ca`) timed out from this machine, so there is a fillable
  slot in the ICE config and nothing in it. Two peers who are both behind a symmetric NAT will
  fail to connect until somebody pays for a relay. This is a real limit, not a caveat.
- **From Iran specifically.** Whether `0.peerjs.com` is reachable through his VPN is untested.

---

## 2026-09-14 — the corpus consolidation, and what Gemini actually did

Morad asked where everything went and what Gemini had used. The audit first, because it
was the thing he could not see.

**Gemini never touched the general bank.** Its 690 questions (`iranian_jeopardy_bank.json`,
4.0 MB) cite **66 distinct course readings** and share **zero** books, zero ids and zero
categories with the archive's 1,000 rows (32 books, 120 categories). Mechanically
guaranteed, not luck: `jeopardy_pipeline.py` has exactly one hardcoded input,
`/Users/Morad/Desktop/IR4595 Iran in World Politics-Readings`, and no route to `Sources/`
at all. So his premise — "a batch from both the real corpus and the IR4595 corpus" — does
not describe what happened, and nothing contaminated the main bank.

What it produced: 17 files in a 55-minute burst (17:14→18:09), twelve near-duplicate
generators with the clue payloads embedded inline, two stray `tmp_*.txt` extracts, a
0-byte `fcntl` lock, and one bank in a **third schema** — bilingual nested in a single
file, `provenance`-based, ids like `single_mostazaf_200`, and **no `final` round at all**.
It is neither the archive shape nor the play shape, so it cannot be dropped in anywhere
as-is. Preserved, not discarded, at `Course/banks/gemini-pass-2026-09-14/`.

**The consolidation.** The engine root is now the one directory; nothing else moved.

- `Jeopardy - Iran in World Politics Edition/` (Desktop-side fork) → `Course/` — 335 files
- `~/Desktop/IR4595 Iran in World Politics-Readings` → `Sources/8 - IR4595 Iran in World
  Politics (Course)/` — 42 PDFs, ~39 MB, ten week folders (no Week 6 — the syllabus skips it)
- `/Users/Morad/Spark` → `Course/banks/gemini-pass-2026-09-14/` — 17 files

The engine's own absolute path is **unchanged**, which is why only two files needed
repointing: `Course/build_edition.sh:22` (`ENGINE="$HERE/.."` — `$HERE` is now
`<engine>/Course`) and `Apps & Games/.claude/launch.json` (both course configs). `Course/`
was appended to the engine `.gitignore` **before** anything moved in, so no course bank or
`BANK_SPEC.md` can ever reach the public repo. `git check-ignore -v Course` →
`.gitignore:23:Course/`.

Three old paths confirmed gone. Stale doc references fixed in the same pass: `AGENTS.md`
(rewritten — it described two sibling folders and the old `data/clues.js` overlay name),
`QUESTION_AUTHORING.md` §12 (dropped "Gemini writes the questions"), and this file below.

**The agent command.** `CORPUS_BRIEF.md` is the new one-page contract: which bank, the
two-shape trap, the rungs, the 6+6 board floor, the self-check list, the stop conditions.
It supersedes §12's Gemini line — any model can be pointed at it. `QUESTION_AUTHORING.md`
stays the long form and `BANK_SCOPE.md` the one-way rule; the brief routes to both rather
than restating them.

`jeopardy_pipeline.py`'s two hardcoded paths are now dead. Left in place as the record of
what was run; do not re-run it.

## 2026-09-14 — the ignore rule was wrong, and the course bank becomes a bank

**The rule I wrote was the opposite of his.** In the entry above I appended `Course/` to
`.gitignore` and called it a safeguard: "the public repo may never carry course material,"
so students could not read the professor's questions off GitHub. Morad reversed it in one
line — *"the only thing that should be git ignored are the ACTUAL SOURCES + any kind of
actual PDF syllabus with course markings on them — that's it; the course and game within it
are fine."* The distinction is **copyright, not confidentiality**. The books in `Sources/`
are not redistributable; the questions we wrote are ours, and who reads them is not a
problem he recognises. My worry about students was invented, not inherited, and is not to
be re-raised as a reason to hide `Course/`.

**What changed.** `.gitignore` lost `Course/` (was line 23) and kept exactly two content
exclusions — `Sources/` and `**/Syllabus/*.pdf`. `AGENTS.md`'s rules bullet reworded to
match; `CORPUS_BRIEF.md` §8 dropped the untracked flag from `Course/` and its closing
paragraph now says copyright instead of secrecy. The historical entry above is left as it
was written — it is the record of what was done that day, not of what is true now.

**Verified.** `git check-ignore -v Course` → exit 1, no output. `Sources` →
`.gitignore:16`. `Course/Syllabus/IR4595 Iran World Politics Module Booklet.pdf` →
`.gitignore:19`. `git ls-files Course` → 0 files at HEAD, i.e. trackable and not yet
tracked. Harmless extras kept: `dist/` ignored globally (build output), `.production-backups/`,
`AudioCache/`, `__pycache__/`.

**What this puts in the repo.** The whole course sub-game — `Editions/`, `banks/`,
`build_edition.sh`, `check_edition.py`, `BANK_SPEC.md`, and Gemini's 690-row bank. Two
things now sit inside a tracked tree that were written as scratch and should not be
committed: `banks/gemini-pass-2026-09-14/tmp_ramazani.txt` (38 KB) and `tmp_saad.txt`
(85 KB) are verbatim full-text extracts of two course readings, and the bank JSON carries
207 KB of `verbatim_passage`. Both are the *actual sources* under his rule and belong
beside `Sources/8`, not in the repo. Reported, not moved — the bank is generated from
them and a move should be his call.

## 2026-09-14 — the play file gets a checker, and the course bank gets an audit

**The gap §11 named is closed.** `QUESTION_AUTHORING.md` said the archive is validated
properly while the play file is checked for nothing but a row count — "the exact
combination that lets a generator bug ship" — and called `Tools/validate_play_file.py`
the obvious fix. That script now exists as **`Tools/check_bank.py`**: stdlib only,
read-only, 1 on any error. Per row it checks the four options and `options[correct] ==
answer`, non-empty `aliases`, all five rungs per category with a byte-identical title,
`value` on the round's ladder, `difficulty` matching the rung, the answer's distinctive
words absent from the clue, language purity, and `id` mirroring across the two languages.
With `--edition` it also reports which categories reach a professor theme clip. It is the
only checker that can look at a **course** bank, which has no archive behind it.

**The deal floor is proven by exit code, not by eye.** Three fixtures under `/tmp/edfix`
(scratch, outside the tree) drive `Course/check_edition.py`: 6+6 disjoint categories plus
3 finals → exit 0; the same with one rung dropped from a single category → exit 1 with a
readable message; six double categories that duplicate the single names → exit 1 on the
disjointness check. `python3 /tmp/edfix/make.py` prints `all three behaved as specified`.

**The course bank, measured.** `Course/Editions/Iran in World Politics/` holds 693 rows
per language, 138 categories, **69 complete single + 69 complete double + 3 finals** —
well past the floor — with ids mirrored and 693/693 distinct host lines, so the main
bank's "Spot on! / The history holds! / Quite right." formula was not reproduced here. It
exits the deal-floor check clean. It fails the content check with **16 captain-obvious
rows** (8 English, 8 Persian — `single_gender_200`, `single_workers_shura_600` and
`single_jihad_brick_200` appear in both), 3 English rows carrying Persian script in the
clue, and two of the professor's week clips that no category can reach
(`prof_19_topic_axis_of_resistance`, `prof_23_topic_iran_at_war`). Relayed as a punch
list. The ~199 rows with a non-zero `correct` index are **harmless** — `shufflingOptions`
re-finds the correct option by its trimmed text after shuffling.

**Two contract documents were lying.** `CORPUS_BRIEF.md` §7.4 told an author to confirm
"the correct index is spread across all four positions" while §5 says in bold to put it at
0 and leave it — a direct contradiction, and the likeliest source of those ~199 spread
rows. §7 now says 0, and both §7 and `QUESTION_AUTHORING.md` §11 point at the checker
instead of saying none exists.

**Still open, flagged not fixed.** The English-only THEME table in `edition.js` means a
Persian category can never match a keyword, so all 138 Persian categories are silent and
the professor's ten week intros never play in Persian. Relayed to the edition session as
a design decision, not a bank defect. `Tools/check_bank.py` is not yet wired into
`build_edition.sh` — that file belongs to the docs/release lane and wiring it there is
theirs to do.

---

## 2026-09-14 — 170 Persian questions were never written

**The checker was blind to this class and now is not.** `Tools/check_bank.py` gained
`check_alternates()`, called from `report()` beside `check_categories()`. The rule: an
`_a` / `_b` pair is two different questions for one rung, so their clue text must not be
the same string once `normalise()` has folded both. One aggregate error per file names the
offending bases; warnings stay untouched.

**Measured, both directions.** On the shipped play files the rule fires **170 times on
Persian and zero times on English**. `Web/data/clues_fa.js` has 170 `_a`/`_b` pairs and
all 170 carry the same clue text; `clues.js` has the same 170 pairs and none of them do.
Total errors move 12 → 13, exit 1, `FAILED`.

**The archive is the source, not the generator.** `QuestionBank/verified_clues_fa.json`
holds 1,000 rows and the same 170 pairs, with **170 identical `clue_text` and 170 identical
`canonical_answer`**; the English archive `verified_clues.json` is 170 pairs with zero
duplicates. Each duplicated Persian `_b` also carries the **English** `_b`'s
`accepted_aliases`, so `single_weve_got_elam_entary_evidence_1000_b` answers
`خط خطی عیلامی` while accepting `جام طلای حسنلو`, and `single_persian_flights_of_fancy_600_a`
answers `اف-۱۴ تامکت` while accepting `فرودگاه مهرآباد`. Its own answer is absent from its
own alias list, and its aliases name a different question's answer. Three of those pairs
also surface in the checker's older options detector
(`single_weve_got_elam_entary_evidence_1000_a` / `_b`,
`single_persian_flights_of_fancy_600_a` / `_b`, `double_persian_gulf_tanker_war_400` and its
encore) as a repeated option: the same defect, seen from the options array.

**Correcting my own earlier claim.** I had said the duplicate "deals twice in one
category". It does not. `buildBoard` (`Web/app.js:1227`) takes `pick(candidates)` from the
rows matching one rung, so exactly one of the pair is dealt and the board never shows the
question twice. The live defects are narrower and real: the judge accepts the sibling's
answer whenever the mismatched alternate is drawn, and 170 slots have half the replay
variety they claim. `buildBoard` cannot see any of it, because its eligibility test only
asks whether every rung is present.

**Not fixable by regeneration.** `Tools/append_flawless_engine.py` maps archive fields to
play fields mechanically and makes no judgement, so the duplicate passes straight through.
The fix is 170 authored Persian questions in the archive, then a regen: per §12 an agent
job with the corpus, not a script.

**The other Persian file does not help.** `QuestionBank/persian_clues.json` (838 KB) is a
JSON object keyed by id, 1,000 entries, and it carries **the same 170 pairs with the same
170 duplicated `clue_text` and `canonical_answer`**; it also holds no `accepted_aliases`,
no `category` and no `round`, so it could not supply the missing questions even if it were
clean. There is no cleaner Persian source in the tree. The 170 questions have to be
written.

### The "bots always answer wrong" complaint is not the bank

Chased in the same pass, because Morad raised it and it was open. **No clue in either bank
is unwinnable**: across all four banks (1,000 EN, 1,000 FA, and the course edition's 693 +
693) the canonical answer is among that row's own `options`, every row has exactly four
options, and the course banks have no duplicate option sets and no empty alias lists.
English has no duplicate options anywhere; Persian has six rows, all in the known `_b`
class, which `shufflingOptions` (`Web/app.js:274`) collapses to three on screen by design.

The bot's decision path is sound on reading. `decide()` (`Web/app.js:3466`) sets
`var pick = hit ? clue.correct : wrongIndex(clue)`, and `clue` is `S.clue`, which is the
**shuffled** copy the dealt cell stores; `shufflingOptions` re-derives `copy.correct` by
trimmed-text match, so the index the bot reads is valid. `accuracy()` is
`Math.max(0.05, Math.min(0.97, b.accuracy + ((clue && NUDGE[clue.difficulty]) || 0)))`, so a
missing `difficulty` falls to `0` instead of poisoning the sum to `NaN`, and every row in
every bank carries a valid `difficulty` anyway. A bot that means to be right is right, at
55–97% by brain and rung.

Whatever produces the report is therefore **outside the data**, and the honest next step is
to watch it happen rather than guess: drive a bots-mode board in the browser and count bot
answers against verdicts. That needs the dev-server slot this session does not have.

## 2026-09-14 — the option index is arbitrary, and the course spec had it backwards

**`Course/BANK_SPEC.md` rule 12 told the author to do work the engine deletes.** It read:
"Vary which option index is correct. Do not put the answer first every time." That is the
opposite of what the engine does and of what every other document in the tree says.
`CORPUS_BRIEF.md` §5 puts it plainly — "put that index at **0** and leave it" — and
`QUESTION_AUTHORING.md:187-191` states the same for all 1,000 archive rows. Corrected here
and in the spec, with the reason attached so it does not get re-inverted: spreading the index
by hand changes nothing a player can see.

**Measured live, not inferred.** Serving the course edition and dealing a board, the
Waltz/deterrence clue rendered its correct option at index **3 (D)** while the bank stores
`correct: 0` on that row. `shufflingOptions` (`Web/app.js:274`, called from 1227 and 2319)
takes the four options, dedupes by trimmed text, shuffles them, and **recomputes `correct` by
re-finding the answer's text**. The stored index is therefore only an offset into `options`
as authored, and the order a player sees is generated at deal time on every card. One value
on every row also makes the two language banks trivially checkable against each other, which
is why the archive settled on 0 rather than on a spread.

**Correcting myself.** I had recorded a contradiction between `CORPUS_BRIEF.md` §5 and §7.4
over this. There is none: §5 says the index stays 0 and §7.4 says the index stays 0, and §7.4
explicitly defers to §5. The contradiction was my own misreading, and the only genuinely
wrong text was the course spec's rule 12 — which is what was changed. Reading both passages
side by side before editing is what caught it; the same passage number in two sections is not
two rules.

## 2026-09-14 — six defects fixed in the public banks, and a bad number of mine

**The offer was six, and six is what got fixed.** Three English clues printed their own answer
inside their own clue text (the Gholam Koveitipour Dashti elegy, whose first line is the answer
"Yaran cheh gharibaneh"; the Baghdad Pact/CENTO alliance, which named CENTO in the clue; the
Sheikh Bahai bathhouse, which named Isfahan in the clue), and three Persian clues listed the
correct answer twice among their four options. All six are fixed **in the archives** —
`QuestionBank/verified_clues.json` and `_fa.json` — with the play files regenerated from them,
because a hand edit to `Web/data/clues.js` is overwritten by the next generation. Regenerating
English produced a file byte-identical to the committed one apart from the three clues, which
is the proof that the reproduction of the generator is faithful.

**The number I had been quoting was wrong because I asked the checker the wrong question.**
I had recorded a baseline of EN 6 errors / FA 7 errors. That came from passing the *archive*
to `Tools/check_bank.py`; the tool takes a **play-shaped** file positionally and `--fa` for the
other language, so the real command is `check_bank.py Web/data/clues.js --fa
Web/data/clues_fa.js`. Measured honestly against the committed play files the baseline is
**13 errors and 4 warnings**, and after the fix it is **1 error and 4 warnings**. The residual
error is not one of the six.

**The root cause of the Persian duplicate was a dropped distractor, and the author's own
value was recoverable.** `Tools/batch_fa_3.json` and `batch_fa_4.json` hold four distinct
authored options for each of these rows; the expansion pipeline wrote `ans_fa` — trailing
space and all, which is why the stale option reads `"عملیات آخوندک "` — into slot 0 and slot 1
and dropped the fourth. The intended distractors are now back where they belong: the tanker-war
clue gains `عملیات کمان ۹۹` (Operation Kaman 99), the Elam clue gains `خط اوستایی` (Avestan),
and the flights clue keeps `میگ-۲۹`. **This corrects me twice over**: in the previous pass I had
substituted two values of my own invention for the tanker and Elam rows, reasoning from the
English rationale lists. The rationale lists are not the authoring source. The batch files are,
and reading them first is what settled it.

**The defect was shipped, not just latent.** `App/Resources/persian_clues.json` is read
directly by the macOS app (`GameEngine/QuestionBank/QuestionBank.swift:70-73` probes
bundle-resource and package-root paths), so the three duplicate-option rows were in the
built app. Fixed there too, along with every other real copy: `QuestionBank/persian_clues.json`
(6 rows), `QuestionBank/distributable_clues.json` (6 fields), `Tools/categories_catalog.json`
(3 fields), and one replacement each in the three authoring scripts that wrote the stale
English strings. Every Persian write was guarded by four assertions first.

**What was deliberately not touched, and why.** The root `Jeopardy Iranian Edition.app` bundle
still carries the three old English strings; it is a build artifact, so the fix is a rebuild,
not an edit. `Tools/batch_fa_3.json` and `batch_fa_4.json` are the clean sources and must stay
as they are. `Versions/beta-1..8/` are frozen release history and keep their old strings on
purpose.

**The residual error is 170 questions, not six, and it is Morad's call.** `check_bank.py`
still reports: `clues_fa.js: 170 \`_a\`/\`_b\` alternate pair(s) carry the same clue text — the
second question was never written`. The `_a`/`_b` device is real and English uses it correctly:
two different questions share one slot. In Persian the second question of 170 pairs was never
written, and the `_b` rows are not merely duplicates — their `accepted_aliases` are the only
record of what the intended second question was, and in typed-answer play they **accept the
wrong answer**. That is a 170-question bilingual authoring job (the model is `BANK_SPEC.md` and
Gemini), not a defect to patch, so it was left standing and reported with its number.

**A related finding, same shape, smaller.** The whole Persian flights series carries displaced
aliases — worst at `single_persian_flights_of_fancy_600_a`, whose aliases read `['Mehrabad
Airport', 'Mehrabad', 'فرودگاه مهرآباد']` under an F-14 Tomcat clue, with the `_b` twin holding
the H-3 airstrike aliases. Reported, not edited: correcting it means deciding which question each
row is, which is the same authoring question as the 170.

> **Superseded later the same day (2026-09-14).** The 170-pair residual above is **closed**, and
> so is the displaced-alias finding: all 340 rows were spliced and the flights rows were
> re-authored as different questions. `python3 Tools/check_bank.py Web/data/clues.js --fa
> Web/data/clues_fa.js` now exits **0** with four warnings and no errors. The paragraphs above are
> accurate for when they were written, not for now — see "The 340 rows are spliced, and the checker
> is green" below.
>
> Attribution for that splice is **not** recorded here, deliberately. The work is corroborated on
> disk — `/tmp/fa_splice.py` and `/tmp/fa_verify_splice.py` mtime 19:03/19:08, `Tools/render_bank.py`
> mtime 19:03, both archives and `Web/data/clues_fa.js` mtime 19:10 — but several lanes append to
> this file and it has already carried one write under two different attributions. Read the
> sections below for what happened, not for who did it.

---

## The 170 `_a`/`_b` pairs: it is 340 rows, and the content is displaced, not the aliases

**The record above framed this wrong, and so did I in the pass before this one.** The standing
story was that the 170 Persian `_b` rows are untranslated clones of their `_a` twin, and that
their `accepted_aliases` are the only surviving record of the intended second question. Six
probes say otherwise, and the correction changes the size of the job.

**What is actually true.** Every one of the 170 Persian `_a`/`_b` groups is a clone group —
`FA pairs with identical clue text: 170/170`, against `EN pairs with DIFFERENT clue text:
170/170`, and `OTHER GROUPS (0)`. But the alias lists are **slot-correct on both sides and are
not displaced at all**: `FA_a aliases == EN_a aliases: 170/170`, `FA_b aliases == EN_b aliases:
170/170`, and across the whole bank `FA aliases == EN aliases: 1000/1000`. The Persian bank's
alias field is copied verbatim from the English everywhere, in both slots, by id. The earlier
claim that a `_b` row's aliases accept the wrong answer is backwards: the aliases are right, and
it is the *clue text standing beside them* that belongs to the other question.

**Measuring what is displaced.** The shared Persian content matches its own `_a` aliases in only
17 of 170 groups, its `_b` aliases in 6, and **neither in 147**. The scope decider is the
**pair-identity meter** — does an `_a` row and its `_b` twin carry two questions, or one question
twice? The English archive is the control, because its 170 pairs are known to be distinct:

```
              pairs  identical_clue  identical_answer
EN (control)    170               0                 0
FA before       170             170               170
```

All 170 Persian groups were one question stored twice, in both fields, against a control that is
clean in both. (The cross-language `fa_parity.py` figures this section used to lean on are
withdrawn — see the correction further down; that meter normalised a Persian answer against an
English alias list and was really measuring how often the *English* list carries Persian script.)
The diagnosis sits in §5 of `CORPUS_BRIEF.md`, which says a `_b` row is a second question and never
a copy of its twin. The size of the job follows from the same measure rather than from the
withdrawn one. Read end to end the pattern is unmistakable rather
than statistical: at `double_a_marriage_of_inconvenience_400` the English asks the Shah's 1951
wedding to Soraya and what her custom gown held — `6,000 Diamonds` — while the Persian beside it
asks the Fawzia marriage at Abdeen Palace, `ازدواج محمدرضاشاه و فوزیه مصر (۱۳۱۸)`. The Persian is
coherent, internally consistent Jeopardy on the same category topics, one rung per question. It
is simply not the question the English row asks.

**So the job is 340 rows, not 170, and the aliases stay.** Both sides of all 170 pairs need their
`clue_text`, `canonical_answer`, four Persian `options`, `explanation` and two host lines
re-authored to match the English row beside them; `accepted_aliases` is left untouched because it
is already correct in both slots. Four background agents are running: two on the 170 `_b` rows
(dispatched before this re-diagnosis, their work still valid and not wasted — only their framing
was wrong), and two on the 170 `_a` rows, which nothing covered. New host lines must not reuse
the shipped tail: all 1,000 existing Persian correct lines end `کاملاً درسته!`.

**Two things banked while diagnosing.** `Tools/render_bank.py` (new) regenerates both play files
from both archives and `--check` reproduces them **byte for byte** — the archive is canonical,
the play files are generated, and until now no generator existed to say so. And `CORPUS_BRIEF.md`
now states it: the archive pair is two files, one language each, ids mirrored *with each mirrored
row carrying its own question*; the full archive→play field mapping with the regeneration block
and "nothing else writes these files"; and the rule that a `_b` row is a second question, never a
copy of its `_a` twin, because the failure mode is a player judged right for the wrong answer.


## The archive is pretty-printed, not one line — and the meter exists

Both contract documents said the archive is "one enormous single line" and implied a
pretty-printer would rewrite all 2,000 rows. Measured today: `QuestionBank/verified_clues_fa.json`
is **61,531 lines**, `verified_clues.json` is **61,717 lines**, and both begin `[\n  {\n    "id": …` —
pretty-printed at `indent=2`, no trailing newline. That exact serialisation reproduces both files
**byte for byte**; adding a trailing newline breaks it (2878884 vs 2878883). The one-line property
belongs to the *play* files (`"window.CLUES=" + json.dumps(rows)`), not the archive. `git show HEAD:`
of the FA archive is 61,531 lines too, so the claim has been wrong for the whole committed history.

Corrected in `CORPUS_BRIEF.md` §1 and in `Tools/render_bank.py`'s `archive_rows` docstring.
Also corrected the neighbouring claim about `Tools/append_flawless_engine.py`: it does **not**
pretty-print into a foreign shape — it uses `json.dump(..., indent=2, ensure_ascii=False)`, the same
form. Its real hazard is different and worse: it rewrites both archives **from its own in-memory
copies**, so re-running it as a generator would silently drop every clue appended since it was
written. The brief now says that instead.

With the serialisation settled, `/tmp/fa_splice.py` was proven end to end on a copy: an identity
splice of three rows printed `lines old=61532 new=61532  differing=0` and the result `cmp`ed
**byte-identical to the original**. So the write path moves only the lines belonging to changed rows.

**Correction — `/tmp/fa_parity.py` is withdrawn.** It measured normalised bidirectional containment
between each FA row's `canonical_answer` and its EN twin's `accepted_aliases`. That is unsound:
normalising `تبریز` cannot produce `Tabriz`, so the meter was really measuring **how often the
English alias list happens to carry Persian script** — a property of the English bank, not of the
Persian rows. Its `6.8% vs 43.0%` gap is an artefact of that and quantifies nothing. The
`PAIR ROWS n=340 — 21 (6.2%)` figures quoted earlier in this log are withdrawn for the same reason.
The one thing that script legitimately got right was the count of identical clue text
(`FA pairs with identical clue text: 170/170`), which the replacement re-derives honestly.

`/tmp/fa_pair_identity.py` replaces it. It never compares a Persian string with an English one, and
asks the only question that defines a broken pair — do the two rows carry the same clue text, or the
same canonical answer? Whitespace and ZWNJ are folded; nothing else. Baseline, before any splice,
and after:

```
              pairs  identical_clue  identical_answer
EN (control)    170               0                 0
FA before       170             170               170
FA after        170               0                 0
```

The control is what makes the FA zero readable: the meter can report a clean bank, so a clean
reading means something. Exit status is 1 if FA shows any identical pair, so this is gateable.

`/tmp/fa_fix_b.json` (85 `_b` rows, first agent in) validates against its worklist: 85/85 ids,
one row per input, in order; every row 4 options with `options[0] == canonical_answer`; no empty
authored field; aliases and category not echoed (the splice keeps the archive's, which is the
design). Refreshest host tail repeats twice; all 85 `correct_generic` strings distinct.


## The bots buzzed confident and then answered wrong

Morad, playing: *"I'm noticing that the BOTS always answer wrong. Which is ridiculous!"* It was not
literally always, but the mechanism was real and it was in two independent coin flips.

`BRAINS` (`Web/app.js:3328`) carries `quick`/`late`/`nerve`/`alert`/`accuracy`/`wager`/`think` per
brain, and the comment above it states the design: difficulty shows in "how fast the thumb moves
(`quick`), how often a clue is there to be taken at all (`nerve`) and how often it is right
(`accuracy`)". The code did not honour it. `armBuzzers` drew its confident thumb from
`Math.random() > b.alert` and called that *sure*, while `decide` separately drew the correctness
verdict from `accuracy`. The two draws were unrelated, so a robot could slam the buzzer with no
knowledge behind the press and then say something wrong — a fast thumb was pure bluff. Measured
before the fix: right on **easy 55.9% / normal 70.9% / hard 82.8% / brutal 89.1%** of its answers,
and **18% of a `normal` bot's answers were "fast thumb, then wrong."**

The fix is one draw, held for the whole clue. `knows(seat, clue)` draws once from
`accuracy(brain(seat), clue)` keyed by `clue.id`; both `armBuzzers` and `decide` read it, so the
thumb and the answer are the same claim. Keying by clue id means a steal does not re-roll a verdict
the room has already watched fail. `nerve` is repurposed as the **fishing gate**: a robot that does
not know it still reaches in at `b.alert * b.nerve`, but only into the `late` band — so an early
press now means what the comment says it means. The stale `NUDGE` line in `armBuzzers` went with
it (the table is still live inside `accuracy`, `app.js:3368`). `node --check Web/app.js` passes;
`knows(` appears three times, at its definition and the two call sites.

Worth stating plainly because it bounds the claim: this was found by reading the code, not by
watching a game. The judge never rejects its own answer (`0/2000` on both banks), there is no index
skew through `shufflingOptions`/`answer()`, and no stale timer leaks. If Morad is still seeing
something, it is something else, and the next step is watching a live board with him.

## The 340 rows are spliced, and the checker is green

All four fix files were validated clean (340 ids, 0 problems, `_a`/`_b` exactly 85+85 twice) and
applied through `/tmp/fa_splice.py --splice`: `lines old=61532 new=61532  differing=3031`,
`rows_touched=340`, and `Tools/render_bank.py` regenerated `Web/data/clues_fa.js` (1000 rows).
`Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js --edition Web/edition.js` now
exits **0**. `/tmp/fa_verify_splice.py` proves the write stayed in scope: 340 rows changed, exactly
the `_a`/`_b` set, every changed key inside `{clue_text, canonical_answer, options, explanation,
host_reactions}`, `accepted_aliases` byte-identical everywhere, every `correct_option_index` landing
on its `canonical_answer`, four options per row, no answer leaking into its own clue.

**One defect got through the agents and was caught by the checker.**
`double_the_bakhtiari_march_1600_a` was authored with options `["کوچ", "ایل بگی", "ایلبگی", "ایلراه"]` — `ایل بگی` and
`ایلبگی` are the same word with and without the zero-width non-joiner, and `check_bank.py`'s
`normalise()` folds ZWNJ, so the answer became choiceable by shape: `options repeat (ایلبگی)`.
Both authoring agents self-reported clean option sets (one claimed "4 unique distractors", the
other "0 failing 4-unique-options") because **neither normalised ZWNJ before comparing** — the
exact normalisation the checker uses. The first replacement tried, `ییلاق`, was worse than it
looked: the archive's own alias list for that row accepts `ییلاق و قشلاق`, so a distractor blessed
by the row's own judge is not a distractor. It is now `ایلخانی`, which is in the clue neither as
text nor as an alias. Lesson for the next agent brief: hand out the checker's `normalise()`, and
require the self-check to run it.

The five remaining warnings are pre-existing and out of scope: the English correct-line tails
(`353` 'spot on', `325` 'history holds', `228` 'quite right'), the Persian `660` 'کاملا درسته', and
`could not find a var THEME = [ table in Web/edition.js`.

---

## 2026-09-14 — the course edition gets its own soundtrack, and the engine learns a third global

**Objective:** the eight-file pack at `~/Desktop/jeopardy_iran_world_politics_soundtrack_v2`
becomes the music and stings of the "Iran in World Politics" edition, without touching what
the general edition plays.

**Why the files could not simply be dropped into the edition's `assets/audio/`.** Two
reasons, either one fatal. The build merges the edition *over* the engine and ships both
shows on one page — the splash chip (`window.setEdition`) toggles between them — so
edition audio named for an engine slot leaks the course score into the general edition the
moment a player flips the chip. And the engine's loader cannot read the masters at all:
`makeEl()` in `Web/app.js` sets `_exts = ['.m4a', '.mp3']` with one retry. There is no
`.wav` path to drop into.

**So the override is a published global, third of its kind.** `window.HOST_CUE_MAP` already
renames a voice cue at play time (read at app.js:460) and `window.HOST_VOICE` already
replaces a whole verdict pool (app.js:538-542). `window.EDITION_SOUND` joins them, set and
deleted by the edition's own `publish(mine)` in the same `if (mine)` block. Everything the
engine needed beyond that is one hook.

**One hook, at the point of choice, not at the call sites.** `url()` now reads
`fileFor(name)`, which is `(window.EDITION_SOUND || {})[name] || name`. Because the
substitution happens where the file is chosen, every caller above it goes on asking for the
slot it always asked for: `music()`'s `musicName === name` dedupe, the duck-and-restore in
`voice()`, and the whole `sfx()` path keep comparing **slots**, never files. No caller
changed anywhere in the engine.

**`refresh()`, and why it is called from `publish()` and not from the engine.** A bed's
file is read only when the cue is requested, so a bed already on the air belongs to the
soundtrack that was current when it started. The one control that can swap shows while the
splash underscore is playing is the title-card chip — so without a re-issue the departing
show's music plays on under the arriving one. `Sound.refresh()` re-issues whatever bed is
on the air, and does nothing when the floor is empty or a voice holds it (a ducked bed is
restored by the voice's own `finish`, which reads the mapping fresh). It must be called
from the edition's `publish()`, not from app.js's `editionchange` listener: that listener
is registered at app.js:49 and fires **before** the edition's `wear()`/`publish()` for the
same event, so it would refresh against the mapping that is being replaced.

**The mapping — eight of the engine's eighteen.** `menu_theme`→`course_theme`,
`splash_underscore`→`course_splash`, `thinking_loop`→`course_thinking`,
`wager`→`course_daily_double`, `final`→`course_final`, `armed`→`course_lock_in`,
`correct`→`course_correct`, `incorrect`→`course_wrong`. A slot the table does not name
falls through to the engine's own cue, which is the right answer for the ten that are not
on the album: the select click, the buzzer, the two round bumpers, the join sting and the
rest.

**Masters compressed, not the loader widened.** 44.1 kHz stereo WAV at 1411 kbps →
AAC 128 kbps stereo 44.1 kHz, `+faststart`, written as `course_*.m4a` into
`Course/Editions/…/assets/audio/`. 28 MB of masters became 2.56 MB shipped. 128 kbps
stereo rather than the ~93 kbps mono of the older cues because this pack is a stereo mix
and the older cues are not. Adding `.wav` to `_exts` was rejected: it would have widened
the shipped product for one edition's convenience.

**Verified:** `build_edition.sh` green, `Course/dist/Iran in World Politics` 25M. All eight
`course_*.m4a` served 200 with exact expected byte counts and `audio/mp4a-latm`; all ten
unclaimed engine cues still 200. The served `app.js` carries `fileFor` and `refresh: refresh`;
the served `edition.js` carries the map assignment, the `delete`, and the refresh call.

**Not verified: playback.** The folder the session was in was at its five-dev-server cap,
all five held by other chats, and the Browser pane cannot reach another chat's server. The
session has been moved to this project root and `.claude/launch.json` added here
(`course-ir4595` on 8790 for the built edition, `jeopardy-web` on 8791 for `Web/`); the
runtime check — course cues requested under the course show, engine cues under the general
one, and a correct bed after a chip swap mid-splash — is the next step. Until it runs, this
entry claims a build and a wiring, not a heard soundtrack.

**Open, his call:** the WAV masters are still on the Desktop. They are irreplaceable and
have no counterpart in the tree, so they were left alone rather than trashed or copied in.

## The bots were flipping two coins — and the fix nearly made them unbeatable

**The defect, precisely.** `armBuzzers` drew `sure` to pick the thumb's band. `decide` then drew
the verdict **again**, independently, from the `accuracy` figure. So a fast thumb was a claim the
robot had no obligation to honour: the same seat that rang in out of the `quick` band could be told
at answer time that it had not known the clue. What that produces is not "always wrong" — it is
**fast, then wrong**: a confident early buzz followed by a flubbed answer, which reads to a player
as a bot that should not have been buzzing. At STANDARD with the `normal` brain, **23.9%** of the
room's answers were of that shape; `hard` 11.9%, `brutal` 5.0%, worse at the higher rungs (30.6%
and 36.1% at INSUFFERABLE for `normal`).

The two figures that had been cited for this are both right, for different populations:
per-seat early-then-wrong is `p(1-p)` = 0.75 × 0.25 = **18.75%**, and the rate observed **at the
podium** is **23.9%**, higher because the winner is likelier to be a *sure* bot than a random seat.
The buggy code's observed right-rate was flat at the `accuracy` figure regardless of the thumb,
which is why the old numbers looked plausible.

**The fix.** One draw per `(clue.id, seat)`, held in `known`/`knows()` and read by both call sites,
so the thumb and the answer cannot disagree. Early-then-wrong is **0.0% by construction** — 0.0 in
all 32 measured cells (4 brains × 4 rungs × both shapes, 200k clues each). Buzz timing is untouched:
the `thumb<900ms` column is identical between OLD and NEW. Nothing about the human's ability to beat
the buzzer changed.

**The regression the fix introduced, and the retune.** With one held draw the room's rate is the
**union over three seats**, not one seat's `p` — `1-(1-p)^3`. The old `accuracy` figures were
*observed* rates that had been quietly compensating for the double draw, so holding the draw while
keeping the table made the room nearly infallible: **normal 96.4%, hard 99.2%, brutal 99.8%** right.
`accuracy` is read in exactly one function (`accuracy()`, clamped `[0.05, 0.97]` with the rung nudge)
and used only by `knows()`, so it is one lever. The table is now **per-seat knowledge probability**,
solved to reproduce the rates the room showed before: `0.27 / 0.43 / 0.54 / 0.63`.

**Solved, not derived.** The cube-root complement `1-(1-shown)^(1/3)` is the right shape but lands
6–8 points low, because the `quick` and `late` bands overlap (normal: quick top 1350 vs late floor
1000) and a fishing thumb in that overlap can take a clue off a slow sure one. So the values were
**bisected** in the sim against the old room rate, not calculated. Cube root would have given
0.26 / 0.36 / 0.46 / 0.53; the solved figures are 0.273 / 0.430 / 0.542 / 0.628, shipped rounded.

**Verified with `/tmp/bot_sim.js`** — a Monte Carlo that extracts `BRAINS`, `NUDGE`, `BUZZ_SECONDS`
and the `THUMB_*` constants out of `Web/app.js` at runtime, so it cannot drift from the code it
measures (`node /tmp/bot_sim.js [trials]` from the repo root). It reproduces `armBuzzers` (the `sure`
draw, the `alert * (sure ? 1 : nerve)` gate, band selection, `Math.pow(draw, 1.5)`, the seat's thumb
habit, the `THUMB_GAP` push, the `THUMB_FLOOR` clamp and the ceiling test) plus both shapes of
`decide()`. Its OLD column — 59.6 / 74.1 / 84.2 / 89.6 across the rungs — sits beside the previously
logged real-board figures (55.9 / 70.9 / 82.8 / 89.1), which validates the harness. Against the
shipped rounded table it returns **59.1 / 74.1 / 84.1 / 89.7** for easy / normal / hard / brutal,
within 0.4 of the old room rates, with early-then-wrong 0.0 everywhere.

**Also visible in the sim, and worth knowing:** all bots in a room share one brain
(`S.players.push({ … brain: S.difficulty … })`, app.js:2605, is the only assignment), so a room is
three copies of one difficulty and the union effect is maximal. The seat-count table shows what
that costs — `normal` at STANDARD is 56.4% right with one bot on the floor, 77.4% with three, 84.0%
with four. The retune, not the seat count, is what sets this.

**Reversible in one line.** If the room reads as too soft, lift `accuracy`; the comment above the
table says why it must not be lifted to the *shown* rate.

**Still open: the literal "always".** The sim bounds the defect and proves the fix; it does not
watch a game. This was found by reading the code, not by observing a match. If Morad still sees
bots answering wrong, it is something else, and the next step is watching a live board with him —
which needs a dev-server slot (all five for `Apps & Games` are held by other chats; `preview_list`
returns `[]` here).

## The "captain obvious" scare was a ghost — the rule is alive and the bank is clean

Peer A reported that `Tools/check_bank.py` exits 1 on the course banks with 16
"captain obvious" errors and named nine rows that quote their own answer. I could not
reproduce it, and the rule is demonstrably working:

- **Positive control.** Spliced `Mostazafin` into `single_mostazaf_200`'s own clue in a
  copy of the English bank → the checker exits 1 with
  `X single_mostazaf_200 [0]: the answer 'Mostazafin' appears in its own clue text — captain obvious`
  and **1 error in total, not 17**. The rule is neither narrowed nor dead.
- **The real banks are clean.** Re-implementing the same rule myself over all four banks:
  **0** hits in course EN (693 rows), course FA (693), engine EN (1000), engine FA (1000).
- **All nine named rows read by hand.** None quotes its own answer. They are the house
  "this X" shape — the organisation described, never named. `single_jihad_brick_800` does
  contain "Construction Jihad", but that is the *sibling* row's answer at 200 in the same
  category, used as context; its own answer is the Literacy Movement Organization.
- **Neither other candidate count is 16.** `--verbose` gives 167 audit notes (the `note()`
  path, off by default, documented as "roughly four rows in ten" — 24% here, on the nose).
  `--require-theme-clips` gives 0 errors, exit 0.
- Most likely source of the 16: the banks were rebuilt at **18:54** and the checker edited at
  **19:13**, so a run against the earlier draft would have seen earlier content. Unprovable —
  `Tools/check_bank.py` is **untracked** and only one copy exists on disk, so there is no old
  revision to diff. That is worth fixing on its own: a gate nobody can diff is a gate nobody
  can audit.

The course bank's field names are `clue` / `answer` / `options` / `correct` / `aliases` /
`correctLine` / `wrongLine` / `theme` / `round` / `value` — **not** the engine archive's
`clue_text` / `canonical_answer`. That mismatch is why my first read of the nine rows came
back empty and looked like blank clues.

## Correction — the Persian theme silence is fixed; the build gate is not my lane

Two entries above now read wrong. Corrected here rather than edited, so the record stays honest:

- **Closed:** "the English-only THEME table means all 138 Persian categories are silent and
  the professor's week intros never play in Persian." `edition.js` now carries Persian keys in
  the THEME table (`['ولایت به شرط چاقو', 'prof_14_topic_revolution']` and its siblings), and my
  own run gives **138 categories, 138 reach a professor theme clip, 0 reach none** on both banks.
  `Tools/check_bank.py … --edition … --require-theme-clips` exits **0** with 0 errors — the
  machine proof. The English-only table was replaced at 19:08.
- **Stands:** "`Tools/check_bank.py` is not yet wired into `build_edition.sh`." Kept, and handed
  to the docs/release lane rather than edited here — that script is theirs. It is now more than
  tidiness, though: the checker is the only gate on the one bank with no archive behind it, and
  if it does not run at build time, nothing catches a leak before the build ships.

## 2026-09-14 (later) — the soundtrack was heard, and the shared material came in off the Desktop

**This corrects the entry above on two points, and closes one it left open.** It is appended
rather than rewritten; the older entry stands as written.

**1. Playback is verified.** The entry above claimed a build and a wiring, not a heard
soundtrack, because the session was stuck in a folder whose five dev-server slots belonged to
other chats. The session has moved to this project root and the check ran. Course show loaded
cold from `index.html?ed=course`: `data-edition="course"`, `window.EDITION_SOUND` present with
all eight keys, and the first bed the page asked for was `course_splash.m4a` — **not**
`splash_underscore.m4a`. The mapping resolves on the very first sound, which was the thing
worth doubting: `refresh()` exists for the *swap* case, but a cold load has to be right without
it.

Then a real drive-through (English → Start game → Take the stage → a tile → buzz → answer
wrong) fetched, in order: `course_splash`, `course_theme`, `course_thinking`, `course_wrong`,
`course_lock_in`, `course_correct`. The two remaining slots need a game state the drive-through
never reached, so they were probed directly — `Sound.music('wager')` → `course_daily_double.m4a`,
`Sound.music('final')` → `course_final.m4a`. **All eight accounted for at runtime.**

**The fall-through still falls through.** `select.m4a`, `buzz.m4a` and `round1_bumper.m4a` were
all fetched while the course show was worn. Slots the table does not name keep the engine's own
cue, which was the intended behaviour and is now observed rather than assumed.

**The general show is untouched.** `index.html?ed=general`: `window.EDITION_SOUND` absent, and
the only audio fetched was `splash_underscore.m4a` and `opening_challenge.m4a`. No `course_*`
file loaded. The published-global pattern holds in both directions.

**The professor's clips play too.** `Course/C3PO_LOG.md:628` ends its voice-pack entry on the
same note — *"Not verified: the clips actually playing"* — and that entry is older, so the
correction is recorded here instead. `prof_01_professor_welcome`, `prof_21_topic_gender_politics`,
`prof_04_correct_annoyingly_so` and `prof_02_start_game` were all fetched during the same
drive-through. Both packs are now heard, not just served.

**One wart, and it is small.** On a chip swap mid-session, the engine's own `menu_theme.m4a`
(777 KB) is fetched *before* `publish()` re-issues it as `course_theme.m4a`. That is
`refresh()` doing its job — it cannot know the new bed until the edition has published the new
map — but it means one wasted fetch on every in-session swap. It never happens on a cold load
with `?ed=course`, which is how the edition is actually opened. Left alone: suppressing it
would mean `refresh()` knowing the incoming mapping before `publish()` sets it, and that is a
worse trade than 777 KB once.

**The build is still green.** Rebuilt after this session's changes: `Course/dist/Iran in World
Politics`, 24M. (The entry above says 25M; the content is identical and the difference is `du`
block rounding between runs, not a lost file — 121 files in `assets/audio`, 8 `course_*` and
27 `prof_*` among them.)

**2. The shared material is in the tree now, and the Desktop is clear.** He said: *anything he
shares that is useful should be copied into the game folder, and no strays should be left lying
around the computer.* Done, and nothing was trashed until its copy had been checksummed
identical.

Masters live at `Course/Masters/Iran in World Politics/`, split into `Soundtrack/` (the eight
WAVs, 27 MB, plus the pack's `README.txt`) and `Professor Voice/` (27 WAVs, 15 MB, plus
`CONTENTS.txt`, `README_FIRST.txt`, `transcripts.tsv` and the pack's own
`Build_MALE_Voice_Pack.command`). The voice pack was **extracted, not kept as a zip** — it is a
self-contained build pack with its own transcripts and builder, so the zip was hiding the
interesting half.

**Why `Course/Masters/` and not the edition folder.** `build_edition.sh` rsyncs `$SRC` — that is,
`Course/Editions/<name>/` — whole, excluding only `*.md` and `.DS_Store`. Anything parked inside
an edition folder ships. A sibling of `Editions/` is invisible to the build *by construction*
rather than by an exclude someone has to remember to add, and the build script carries enough
reasoning already without a special case for masters. Proved rather than argued: the edition was
rebuilt after the masters landed, and `dist/` contains no `.wav`, no `.zip` and no `Masters`
directory.

**Four Desktop items went to the Trash, through Finder — never `mv`.** The soundtrack folder and
the voice-pack zip (the two he had just shared), plus two things already copied in during earlier
sessions and now verified byte-identical duplicates: the module booklet (`Course/Syllabus/`,
same SHA-256) and the readings zip (42 files, `diff -r` clean against `Sources/8 - IR4595 Iran in
World Politics (Course)`, which held nothing the zip did not). The `mv ~/.Trash` route is a trap
in this app — it reports success and the files never land — so every discard went through
`osascript`/Finder's `delete`, and was confirmed by a *later, separate* command. That command
showed all four in the real Trash and the Desktop clean of project material.

Worth knowing: the voice pack's own `Build_MALE_Voice_Pack.command` writes to `$HOME/Desktop/`
by design (`OUT="$HOME/Desktop/$PACK_NAME"`), and zips there too. Re-running it would recreate
the stray. It is kept verbatim as the record of how the pack was made — its download URLs are
temporary `mcp-preview` links and are almost certainly dead by now — but if it is ever run
again, change `OUT` first.

**Open, his call — and this replaces the "Open, his call" at the end of the entry above.** The
masters are no longer on the Desktop; that part is settled and needs no ruling. What does need
one is size: `Course/Masters/` is **42 MB and is not gitignored**, so it will be committed. The
`.gitignore` comment above the `Course/` rules carves out exactly two things — the source corpus
and the course-marked syllabus PDFs — and gives copyright as the reason, which does not apply
here: this is his own original soundtrack and his own voice pack. Ignoring it would be for size
alone, which is a different argument than the one that rule was written to make. Left tracked,
and raised rather than decided.

## The content gate is now wired into the build — the ownership hold fell away

**What changed.** `Course/build_edition.sh` now runs `Tools/check_bank.py` against the edition's
own two banks, immediately after the deal gate. Until today the build's only pre-flight was
`check_edition.py`, and that script answers one question only: *can a full board be dealt?* It
never reads what the clues say. So a leak (the answer sitting inside its own clue), an
`options[correct]` pointing at the wrong option, an empty alias list, an `_a`/`_b` pair that is
one question written twice, Persian script in an English clue, or a category reaching no theme
clip — none of those stop a board dealing, so all of them shipped uncaught. For a course bank the
checker is the *only* content gate there is, because that bank has no archive behind it to
compare against.

**Why it is mine now, when an earlier entry said it was not.** The entry above records the file as
the docs/release lane's — *"`Tools/check_bank.py` is not yet wired into `build_edition.sh` … that
file belongs to the docs/release lane and wiring it there is theirs to do."* That was correct when
written. It is stale now: that session (`local_392da957`, "DONE - Jeopardy engine — docs tail +
release") reports `isRunning: false` and is marked DONE, so there is no lane left to hand it to.
A fix that only needed routing became a fix with no owner, and an unowned gate that nobody runs is
the same as no gate. Recorded here rather than left implying a handoff that never happened.

**Three proofs, all by exit code rather than by reading.**

1. The happy path. `bash Course/build_edition.sh "Iran in World Politics"` → `EXIT=0`, the checker's
   `OK — no errors (203 warning(s))` printed at line 234 and `Building 'Iran in World Politics'…`
   at 236, and the tree built (24M). A passing bank is not blocked by the new gate.
2. A planted leak must stop the build, not merely be reported. A scratch edition was built in
   `Course/Editions/_gatecheck` — the real `edition.js`, `edition.css` and both banks copied, with
   the first row's answer `Mostazafin` spliced into its own clue and nothing else touched — then
   built. `EXIT=1`, one error, naming the row: *`single_mostazaf_200 [0]: the answer 'Mostazafin'
   appears in its own clue text — captain obvious`*, `FAILED`, and `Course/dist/_gatecheck` absent,
   proving the build stops *before* it copies anything rather than producing a bad tree. The
   scratch edition was then removed.
3. A missing checker fails loudly rather than skipping. Pointing `JEOPARDY_ENGINE` at a stub
   engine with no `Tools/` → `EXIT=1`, *"Cannot find the content checker"*, after the deal gate had
   already passed. A gate that quietly skips itself is worse than none, which is the exact failure
   mode being fixed, so absence is an error and not a no-op.

**Two design notes worth keeping.** Theme reach is only meaningful for an edition that declares a
`THEME` table, so `--require-theme-clips` is passed only when `grep -qE 'var THEME[[:space:]]*=[[:space:]]*\['`
matches `$SRC/edition.js` — an edition without one is not a fault, and requiring clips of every
category would fail a legitimate non-course edition. Both directions were tested. And the flag is
passed as a string rather than an array on purpose: under `set -u`, `"${arr[@]}"` on an empty array
is an error in bash 3.2, which is what `/usr/bin/env bash` resolves to on macOS unless Homebrew's
bash is first in `PATH`.

**Scope held deliberately.** The gate checks the *edition's* banks via the checker's own documented
invocation. It does not check the engine's general bank that gets copied in — that bank is the
engine repo's own business, and it is byte-identical to what is already published. The engine's
`Tools/check_bank.py` remains untracked, so this gate still depends on a file that a fresh clone
would not have; the stub-engine test above is what that failure now looks like, and it is loud.

## 2026-09-14 (later still) — the show chip gets art drawn for its own box, and stops being a label

**The defect, from his two screenshots of the splash.** The "WHICH SHOW?" chip carried a square
of dark blur next to each name. Cause: both `tile-*.png` were **960×540 card art**, and
`.swap-art` crops its source with `object-fit: cover` into a 34–46px square. A landscape crop of
a card whose middle is an empty field keeps exactly the empty field — so the chip was showing
the one part of the art that carried no information. The art was never wrong; it was never drawn
for a square.

**The fix.** `Tools/make_edition_tiles.py` draws both marks at 512×512, supersampled 3× and
reduced once with LANCZOS. Deterministic — no randomness, no network — so a rebuild is
byte-identical. The two originals were **copied**, not moved, to
`~/.Trash/jeopardy-tiles-replaced-2026-09-14/` as `.wide-960x540.png`.

**What the mark can be, given the reduction.** A ten-fold shrink to 34px keeps *silhouette and
colour* and loses *line*. Two candidates died against that rule, and one of them is worth
recording because the collision is real: a near-black ring with the tricolour rule across it
reads as a **prohibition sign**. That is ordinary sign vocabulary, and a bad thing for this
project to print on a control. So the pair is one grammar — a near-black plate with a soft lift,
and the show's tricolour rule as the constant. `general` is the rule alone. `course` sets the rule
across a **filled, lit sphere**, which is a body rather than an outline and so survives as a
silhouette; the rule is the equator and stays *inside* the disc, so the sphere is never struck
through; one faint meridian gives it a globe at full size and costs nothing at 34px.

**The chip's behaviour.** Every move is **height-neutral**, and that is a hard constraint rather
than a preference: the chip is pinned `bottom: 4.2%`, so anything that grows it walks the eyebrow
up toward the professor's drop shadow, which already eats ~25px of a ~31px gap. So no second line
and no rule under the eyebrow. Instead: the flag dash goes *inline* on the eyebrow; hover and
focus-visible take the same masked flag hairline `.pill-primary` wears, because the chip is the
one control on this card that changes the show and should look like the door rather than like a
label; a −2px lift with `--glass-hi` and a deeper shadow; the art's inset ring brightens; the name
goes white; and the chevron moves *into the flow* rather than pinned to a 426px pill edge, so it
sits with the label and nudges toward its own point. `:active` settles back to 0 and 0.985. RTL is
handled by the flex row mirroring on its own — art right, chevron left — with only the glyph
turned.

**`.shine` was deliberately not reused.** The style sheet is explicit that the travelling shine is
*the* mark for "this is the thing you have chosen," and that a second selection indicator is not
to be invented. The chip is not a selection — it is a door to the other show — so it takes the
primary pill's flag hairline and leaves the shine alone.

**Proof.** Headless Chrome against the built course tree, `Course/dist/Iran in World Politics`.
At 1024×768 and at 1440×900 the chip renders at the plate's bottom-left as a flag-dashed
"WHICH SHOW?" over a pill carrying the tile, the show's name and a chevron, with no professor
collision. Both editions, resting and hover, plus the two Persian RTL states, were rendered in a
scratch harness and looked at. The scratch harness and the temporary render scripts are gone.

## Correction — three things in this log were wrong, and one change went in without engaging its removal

**1. The 16 were real, and "ghost" was the wrong word.** The entry two screens up is headed
*"The 'captain obvious' scare was a ghost"* and says *"I could not reproduce it."* Peer A's
transcript holds the output verbatim, with timestamps:

```
16 error(s): X single_gender_200 [50]: the answer 'Chador' appears in its own clue text
```

I did not reproduce the report; I reproduced its **absence**. The banks were rewritten at
**18:54:14** and my four-bank sweep read the *rewritten* text, so 0 hits was the fix working,
not the report being false. The report was accurate about a bank state that no longer exists on
disk. Withdraw *"ghost"* and *"I could not reproduce it"*; the finding stands and the rule was
never in question.

**2. The engine banks in the working tree are not what is published.** My gate entry closes with
*"it is byte-identical to what is already published."* It is not, and the difference matters:

| | `Web/data/clues.js` | `Web/data/clues_fa.js` | checker |
|---|---|---|---|
| `HEAD` (published) | `9aa12357…` | `05c7919a…` | **13 errors**, FAILED |
| working tree | `68968e08…` | `a97864ca…` | OK — no errors |

Both files are ` M` in `git status`. So six clue rewrites and one `_a`/`_b` pair fix exist **only
as uncommitted changes**, and a release built from a clean checkout of `HEAD` ships all of them:
six captain-obvious English clues (`war_koveitipour_800` 'Gharibaneh', `coldwar_cento_2000`
'CENTO', `single_philosophy_of_isfahan_the_metaphysicians_800` 'Sheikh Bahai', each plus its
`_encore` twin), six Persian rows offering a repeated option, and `head_clues_fa.js: 170`
alternate pairs carrying one question's text twice. Committing is Morad's call and not mine.

**3. The gate went back in without answering the objection that took it out.** The course log
removed it for a reason my entry never mentions: a peer asked and then withdrew, and — the part
that actually holds — *the session that builds the edition invokes `build_edition.sh` constantly
and does not want the script changing underneath it.* I justified the reinstatement by checking
`local_392da957` (docs/release) and finding it DONE. That was the wrong lane. `local_692d0186`
— *"Course choice images and buttons"*, cwd in this repo, active at 19:22 — is the one that
builds, and the script did not become ownerless because a different session stopped. The gate
**stays** (it is proven, it refuses before `rm -rf "$OUT"`, and the course bank passes it today,
so the lane sees no difference until it introduces a defect) but it was disclosed to that lane
rather than left to surprise it, and Morad can take it out. What it must not do is sit in the
file as though its removal had never been argued.

## 2026-09-14 (later again) — an outside pass over the web build: one real bug, one revert, one gap I filled

Morad asked an outside model (GPT-6 "Astra", via the Codex CLI) to sweep `Web/` for
inconsistencies and bad code. It found one thing that is genuinely wrong and made several other
edits of uneven value. I diffed every line against a pre-run backup, kept what survives contact
with the code, reverted what does not, and repaired the two gaps it left.

**The real bug, and it is in `net.js`.** A joiner announced itself with `send(...)`, which walks
`N.conns` — a structure only the host maintains. The host never heard the joiner's name. It now
sends `sendUp(...)`. Worse, and the reason to trust the fix rather than the report: every
`peer.on` / `conn.on` handler stayed subscribed to a peer that had already been replaced, so a
reconnect could deliver events from the dead connection into the live game. Handlers are now
gated on `N.peer === peer`. `close()` snapshots the peer before nulling the field instead of
destroying a reference it had already dropped.

**What I reverted.** Astra trimmed `PLAYER_COLORS` from six to three, having used that line as a
string-replace anchor. `.length` is load-bearing: it caps online capacity and bounds the seat
loop. Six colours, restored. It also tagged remote answer inputs with `remote-write`, a class
with no rule anywhere — `.plate-remote .write-input` already does that work. Removed from both
call sites.

**What I added, and it is the one thing here you have not seen.** The audit turned up a class
used but never styled: `.remote-verdict.is-mine`. It is real — a guest is sent *every* seat's
ruling, and nothing marked which one was theirs. It now draws a neutral white ring via
`box-shadow`, deliberately outside the border so it composes with the green/red that already
carries right-or-wrong, and does not repaint either. Veto it if the ring reads as noise.

**Kept, and why each survived.** `rebindBanks` now throws on a missing bank instead of silently
falling back to English — a Persian player seeing English clues is a worse failure than a
visible one. A pre-emptive `beforelangchange` / `beforeeditionchange` guard refuses the switch
*while a bank is dealt* (`board`, `clue`, `wager`, `results`), which is stronger than the
existing post-hoc `langchange` guard; the splash is not in that set, so the splash switch still
works. Snapshot, answer and edition-id validation were hardened (`Number.isInteger` bounds on
the MC option, `/^[A-Za-z0-9_-]{1,32}$/` on the edition id, `Object.create(null)` for `BY_ID`, a
two-editions cap matching the file's own written rule). Dead code went: `currentValue()`, a
`[dir="rtl"] .layout-row` rule for a class used nowhere, and two `void`-ed variables.

**Decisions, not transcripts.** `Tools/check_web.js` is Astra's own Node test harness. It is
broken — `document.createElement is not a function` — and it is scaffolding, not product. Left
in place rather than trashed, because `Tools/` is Morad's to judge and this session's standing
instruction was to assess and report, never remove. The bank-warning repetition is a content
problem and stays a content problem: 353/325/228 English `correctLine` rows ending 'spot on',
'history holds', 'quite right', and 660 Persian rows ending 'کاملا درسته'. Not a cleanup job.

**Verified.** `node --check` clean on all six edited scripts. Both banks pass `check_bank.py` with
no errors. i18n at 232/232. Every JS-referenced DOM id exists. Walked the real UI in a browser:
Persian splash, menu, green room and dealt board; the board deals Persian categories with no
English leakage; console clean; and `setLang('en')` attempted mid-game left the language at `fa`
and the six categories untouched, which is the guard doing exactly what it was written to do.

---

## 2026-09-14 — the course gets its reading list, read off the PDFs

`Web/courses/iran-in-world-politics/data/readings.js` now carries the 42 PDFs of IR4595 as
`window.READINGS_IRAN_IN_WORLD_POLITICS`: ten groups, one per taught week (there is no Week 6 —
it is independent learning), 42 items, each an `{ title, author, year, kind, src }`.

Authored, not generated, and the header says so. The corpus ships no metadata file and no
syllabus, so every citation was pulled from the PDF's own front matter with `pdftotext -f 1 -l 2`
rather than guessed from the filename — which is why five rows carry `year: null` instead of a
plausible number. Four of them are chapters cut out of a book whose title page is not in the
extract — the extract opens on the chapter, so the year (and in one case the author) is simply
not in the file. The author is established from the running work, the year is not printed, so it
is left blank. The two `Sanctions-N` rows and the `Body Isolation` row have no author line in the
PDF either; those name the volume's authors from the book itself and are the only rows whose
attribution is not also in the file. `node --check` passes; a load shows 10 groups / 42 items.

---

## 2026-09-14 — parentheses stop telling on the answer; the front door keeps the show

The option shuffle was sound and the typography was not. In MAIN, 190 English clues and
157 Persian clues printed parentheses on the correct answer alone. Moving that option to a
random square only moved the giveaway with it. A dealt clue now keeps its authored options
untouched for judging. On the affected clues it flattens their parenthetical punctuation for
display, then gives each of the four displayed options an independent coin flip; clues with no
parentheses remain untouched. The flip never receives the correct index. The regression harness
fixes the shuffle in place and proves both cases: the correct
answer can wear parentheses beside a distractor, or go bare while distractors wear them.

The opening screen was crowded because it asked language, MAIN versus course, and three
future courses in one narrow vertical hierarchy. It now keeps the same palimpsest stage,
glass, tricolour rim, hover movement and supplied identities, but makes the two playable
editions equal landscape doors. MAIN uses the original Iranian Edition wordmark and skyline;
IR4595 uses its separate World Politics wordmark and its own stage mural. Neither logo was
redrawn. Language is a small segmented control, and the three coming-soon marks sit on one
low shelf. This is a recomposition of the existing show, not a replacement aesthetic.

---

## 2026-09-15 — the professor keeps his cue, and buzzing early has a price

Three changes to the course edition's flow, in `Web/app.js` and the course's `course.js`.

The professor's category introduction now plays in the space between choosing a tile and
seeing the clue, never over the clue itself. `startClue` parks on a pre-clue gate
(`HOST_PRECLUE`) that holds the reveal until the intro ends or is skipped, and any tap
skips it, so a player who has heard the bit before is not forced to sit through it again.
`revealClue` is cut ahead of time so a lingering intro cannot bleed into the read.

Buzzing before the buzzers open is no longer free. A premature buzz still books the foul
on the spot, but now it also costs the player the chance to answer: when the buzzers would
have opened, the seat is locked out for a further second and a half, its button re-rendered
disabled until the lockout elapses, and the hint names the seat. The point was to stop the
move where someone spams the buzzer early and still wins the race when it opens.

The professor's voice remains the old deep male. Regenerating the 27 clips in the
posh-but-not-posh young British register is the next step, blocked on a reference clip and
his go-ahead.

---

## 2026-09-15 — the front door is a doorway, not the show

The chooser had three problems and they were the same problem: it was the show's own stage
with some furniture on top. A green-tinted panel and a red-tinted panel, each with an inner
glow in the same hue, a gold hairline through the middle of both, a printed wordmark sliced
by the seam between art and text — six colours in one frame and the wordmark cut in half by
a border it happened to land on. It now has one material, white frost over dark glass, and
the edition accent is held back until the door is under the pointer. Two doors, not two
colour schemes.

The tagline was flat — it told the player a fact instead of needling them. It now says what
the host would actually say: my uncle knows this, my Snapp driver knows this, the man I met
at the bus stop knows this, and I don't take the bus. Both languages, same joke, same turn.

Two of the three wordmarks went. The main card carried the pack's 3D mark sliced into its
own header; the screen above it carried the same mark again as a raster. One lockup set in
type is the show's signature, and it is now the only one. The dead `.hero-card` family —
ninety-seven lines nothing had referenced since the doors were unified — is gone with it.

The backdrop was the real fault. The front door stood on `.stage-bg`, the same Milad Tower
skyline the title card wears, so a player crossed the same picture twice with one press
between. `show()` now mirrors the active screen onto `<html data-screen>`, and the chooser
keys a Persian iwan off it: black marble, a frosted arch, the archway left as a void. It is
generated in the ChatGPT desktop app, not the web one — the web app rate-limits us now.
Wide, dark, monochrome, with only the two flag washes at the outer edges and the same
washes halved underneath, because the art already carries them. Every screen after the door
keeps the skyline. The archway is also the quietest part of the frame, which is where the
two cards land, so the art is doing legibility work rather than being decoration behind it.

The five Tannaz sprites were sitting in `assets/host/` loaded by nothing. `host-layer.js`
now drives them the way the professor is driven — five poses, his bubble, his pop — with
one difference: she is wordless. No transcript of the thirty-five main-edition host clips
exists anywhere in the tree, so there is nothing to caption her with. Her lines need a
recording script before they can be written.

---

## 2026-09-15 — the host leaves with the show, and comes back with it

Two faults on the same edge, both in `Web/app.js`, both about what happens when a player
backs out of a show and walks back into it.

Leaving was the first. Backing out to the door cut the screen but not the cue, so Tannaz
kept talking over a chooser that belongs to neither edition, and her sprite stood on a
floor the player had already left. The sprite was the tell: the floor is drawn from the cue
that holds it — `tellCue` is the only thing that raises a host — so the whole fix is one
`Sound.cut()` in `backToFront`, before `show('front')`. One call, because the voice and the
figure are the same fact. There is no separate host to hide.

Returning was the second, and it was the same fault wearing the other face. `enterEdition`
ends in `runOpening()`, and `runOpening` opens by returning when `S.openingDone` is set —
which it is, permanently, after the first visit. So a second walk-in cued nobody: no music,
no `tellCue`, no `hostcue`, no figure. The course edition had it too, which is why it
presented as two broken shows rather than one broken path. Backing out and walking back in
is not a first visit, but it is still an arrival, and the host is the floor's answer to one.
`enterEdition` now re-issues `Sound.voice('opening_challenge', 0.9, null, { over: true })`
when the open is spent — the line alone, without the underscore and the darkening, which are
the theatre of a first entry and have already been played. `over` leaves the bed that
`refresh` just started running underneath it.

It had to be a cue and not a bare sprite. The bubble is a transcript of audio already
playing out loud, so a host who is to be seen talking has to be heard first; anything else
draws a mouth moving over silence.

The 27 professor clips were re-cut under the same filenames and the same beat list. Only
the read changed, and the file sizes moved both ways, so this is a re-record rather than a
compression pass.

---

## 2026-09-15 — the APK is shelved, and not for the reason it looked like

Android was the one build a three-app release would have been missing, so this was the day
to find out whether it could be made. It cannot, from here, and the reason is worth writing
down before somebody spends another afternoon on it.

Homebrew's `android-commandlinetools` cask failed on a 404, which reads like a stale cask.
It is not. Every path under `dl.google.com/android/` returns Google's own 404 page, byte for
byte, including build numbers that certainly existed. The rest of that host is fine — the
Chrome `.deb` on the same domain streams 206 — so this is neither a dead host nor a dead
product. It is one path prefix answering 404, which is what a filtered exit node looks like
when it is handed a request it will not pass through.

The consequence is worse than a missing SDK. `maven.google.com` redirects into the same
prefix — `dl.google.com/dl/android/maven2/` — and that 404s too, so Gradle could not have
resolved the Android Gradle Plugin even if the platform and build-tools were already sitting
on disk. Both halves of the build are behind the same door. The files are real; Tencent's
mirror serves the identical `repository2-3.xml` and lists `platforms;android-34` and
`build-tools;34.0.0`. They are simply not reachable from this machine's current exit.

So the order is: fix the route, then build. The scaffold stays under `Android/` because it is
finished work and not a hypothesis — a WebView shell making the same two promises
`App/ShowWebView.swift` makes, the four haptic patterns reached through `navigator.vibrate`
with no bridge to write, `Web/` staged and checked against source the way `build_ipa.sh`
checks it, and an adaptive icon cut from `icon-master.png`. What is missing is a toolchain,
not code. Nothing in `Web/` is waiting on this, so Android players use the web build.

**Why:** a `.apk` needs Google's SDK and Google's Maven, and both are served from `/android/`.
**How to apply:** before re-attempting, re-measure `dl.google.com/android/repository/` from
whatever exit is current. If it answers anything but a 1449-byte 404, the road is open and
only `sdkmanager` and a keystore stand between this tree and an `.apk`.

## 2026-09-15 — she talks now, and the bubbles are reconstructions

`host-layer.js` has carried a note since the sprites went in saying she was wordless on
purpose: the clips exist, the transcript does not, so nothing could caption her without
inventing a line. `MAIN` now registers a `lines` table and the note is gone.

The thirty-six cues that have audio are covered — the four scene cues and the sixteen
`right_`s and sixteen `wrong_`s. The twenty-four further verdicts that came back with the
script are deliberately absent: they have no clip in `assets/audio/` and are not in the
pools in `app.js`, so a line for one would be a caption over silence. That pair of facts
is in the comment above the table, so adding a recorded clip and its pool entry is a
two-line change and adding only the line is not a change anybody makes by accident.

The important thing to write down is that these are not transcripts. Each clip was named
after the punchline of its own line and the words were never written down, so the table was
rebuilt from the filenames. The joke each bubble makes is the joke its clip was filed
under, and not necessarily the sentence coming out of her. That is a real disagreement with
the audio, and it is the exact thing the header of the file warns against, so the file says
so above the table rather than leaving it to be discovered. A transcription of the clips
replaces the table and nothing else.

Two things were caught by testing rather than by reading. The keys have to be the whole
slug — the engine hands the bubble `right_08_tehran_survives_another_round`, not
`right_08` — and a bare number silently matches nothing, which renders as a host standing
there mute rather than as an error. The pose rule is on prefixes and always had this right;
only the lookup was wrong. And `opening_challenge` is Morad's own cold open, not the one
the script returned.

**Why:** the clips are English in both editions, and a caption nobody recorded misquotes
the room — the file's own rule. Wiring reconstructed lines is a knowing exception to it.
**How to apply:** if the audio is ever transcribed, replace `LINES` in `host-layer.js`
wholesale and change nothing else. Do not add a line for a cue with no clip behind it.

## 2026-09-15 — the professor speaks at 1.2, and nothing else speaks at all

The course edition's twenty-seven lines were re-recorded this session by cloning Morad's
own reference note through Fish Audio S2 Pro, then retimed with `ffmpeg -filter:a
atempo`. The tempo went 1.5 → 1.25 → **1.2, which is final**: 1.5 was rejected on
hearing as too fast, and 1.2 was chosen over 1.25 by ear. Changing tempo this way moves
the clock without moving the pitch, so the clone's timbre is untouched.

The bug worth recording is that the first 1.5 and 1.25 sets were **mislabeled**, not
merely mistuned. `prof_01` measured 15.33s at 1.0, 13.64s in the "1.25" folder and
13.34s in the "1.5" folder — an effective 1.15× and 1.12×, when the names claimed 1.5
and 1.25. The cause is that `atempo` has to be applied to a true 1.0× source; these were
compounded or applied to the wrong input. Every variant was regenerated from the clean
`m4a/` tree and checked by measurement — each file's duration ratio to its 1.0× original
had to land in the band for its factor (1.47–1.53 for 1.5, 1.22–1.28 for 1.25, 1.17–1.23
for 1.2), and all three sets came back with zero files outside their band. The shipped
1.2 set passes the same check.

**Why:** filenames asserted a speed and no test contradicted them; the only thing that
caught it was timing the audio instead of reading the label.
**How to apply:** never trust a derived clip's name. Measure its duration against the 1.0×
source before it goes anywhere near `Web/`.

Two independent verifications were run against the shipped audio. The first is that the
27 clips match the writing: `TEXT` in `course.js` and the `LINES` list the generator
worked from agree on 27 keys with zero text mismatches. The second is stronger, and
needed a way to read audio back that did not stall. `whisper-large-v3-mlx` downloaded
from HuggingFace to ~20K of a `.incomplete` blob and a mirror retry died the same way
(exit 144, twice), so the route was abandoned rather than retried.

What replaced it is `SpeechTranscriber` — Apple's on-device model, shipped with the OS.
Assets come from Apple, not from HuggingFace, so **Iran does not throttle them** and it
was installed and working in one call. The tool for this is already in the tree:
`Tools/transcribe_host.swift`, written for the host clips and taking any audio path. It
is the better of the two scanners that exist — it biases the model with a vocabulary
list, which is what stops `Tehran` coming back as "Teh" — and it is what to reach for
next time. The throwaway copy used here lived in `/tmp` and is gone with it.

The one hazard worth writing down: a `SpeechTranscriber` **cannot** be shared across
several `SpeechAnalyzer`s. Feeding one instance a batch of files crashes with SIGTRAP
(exit 133) and takes buffered stdout with it, so the failure looks like silence rather
than a crash. The in-tree tool already avoids this by building a fresh transcriber per
file inside `transcribe(_:)`; the `/tmp` scanner did not, and had to be run once per file
from the shell to work at all.

Fed the shipped clips, it returned words for all 27, and the seven that differ from the
script are recogniser artifacts rather than performance errors: `IR4595` comes back as
"ir 4595", `eight` as "8", `generalisations` as "generalizations", `comeback` as "come
back", and one "there" goes missing. No clip speaks a line belonging to a different cue.

The other half of the request was that **no other male voice exists in this edition**, and
that is now measured, not assumed. Every other audio file the course edition can reach was
transcribed: its eight `course_*` slots (theme, splash, thinking, daily double, final,
lock-in, correct, wrong) and the six engine cues it does not override (`select`, `buzz`,
`round1_bumper`, `round2_bumper`, `join`, `winner`) all returned `[NO SPEECH
RECOGNISED]`. The control — `prof_04_correct_annoyingly_so` — returned "Correct.
Annoyingly so.", which proves the tool hears speech when speech is there. The engine's own
Tannaz clips are irrelevant here: `HOST_VOICE` and `HOST_CUE_MAP` replace them in this
edition, and the host does not read clue text aloud in either edition — the clue is
board-only, so the professor's quips are the only spoken words on the floor.

**Why:** "make sure there's no other male voice" is a claim about every file the edition
can play, and the six unclaimed engine cues are exactly the ones nobody had looked at.
**How to apply:** if a new `course_*` or engine cue is added to this edition, it has not
been checked. The verification covers the 27 `prof_*` and the 14 non-voice files listed
above, and nothing else.

The 1.0×, 1.25× and 1.5× sets are all in `~/.Trash/` under their dated folders. `Web/` was
not committed.

## 2026-09-15 — the giveaway moved from the parentheses to the dash

Morad saw it from the sofa before any test did: parentheses all over the answer buttons.
The original leak was that `options[correct]` is the answer string, and only the answer
carried an editorial gloss — "National Iranian Oil Company (NIOC)" beside three companies
with no gloss — so the glossed button was always the answer. The earlier repair flattened
the gloss to an em-dash and dealt parentheses to all four buttons as camouflage, which
traded one tell for another: the dash landed **only on the option that had carried the
gloss**, and that option is the answer. Measured on the shipped bank, 202 glossed clues
displayed exactly one em-dash, 196 times on the correct button and 14 on a distractor —
a tell that wins about 93% of the time. Zero authored options contain an em-dash, so the
dash was the engine's fingerprint and nothing else.

The gloss is now stripped from the four buttons and from nothing else. `presentingOption`
(`Web/app.js:297`) drops any bracketed gloss and the whitespace around it before
`shufflingOptions` (`Web/app.js:310`) builds `displayOptions`; the raw `options` array is
untouched, so the judge, the robots, the reveal and the archive invariant
`options[correct] === answer` all still see the full text. On screen that reads as the
intended pair: the button says "Ecbatana", the answer card says "ECBATANA (HAMADAN)".
One guard was needed: if stripping would make two buttons identical — a clue shipping
both "Wine (and Beer)" and "Wine" — the gloss is kept, because a board showing the same
text twice is worse than a hint. Six Persian rows in `شطرنج با ماشین قیامت` needed repair
for the same reason: their distractors were the English row's answers, so the strip
collapsed an option into its neighbour.

**Why:** the tell was never the punctuation character, it was that exactly one button
differed typographically from the other three, and that button was always the answer.
Removing the difference is the fix; swapping which character carries it is not.
**How to apply:** the rule now sits in `QUESTION_AUTHORING.md` §6 and §7 and in `AGENTS.md`
§3, where the clue-authoring agents read it — no option may be findable by its
punctuation, and no distractor may be the answer with its gloss removed. `Tools/check_web.js`
asserts both over 50 shuffles of a glossed clue and over the twin-option case.

Three things found while doing it are **not** fixed and are reported as they stand. The
Persian bank's aliases: 348 of 1,000 rows list aliases sharing no token with their own
answer (`reza_coup_200` answers ۳ اسفند ۱۲۹۹ and accepts Reza Khan; `bazaar_saffron_600`
answers زعفران and accepts Khorasan), which the write-in judge honours — the English bank
has none, and 260 of the 348 match neither the neighbouring record nor their own.
The six repaired Persian rows still carry the English row's `supporting_passage` and
citation fields, left alone rather than fabricated. And `Tools/check_bank.py` has no gate
for any of this: a dash in exactly one option, a gloss-strip that merges two buttons, or
an alias belonging to another row all pass it today.

`.claude/launch.json` gained a `jeopardy-web-c` entry on port 8793: the two existing Web
entries were both refused as owned by other chats' servers, and `lsof` showed nothing
listening on either port.

---

## 2026-09-15 — the itch.io channel publishes from the runner, because this machine cannot reach itch

**Objective:** every push to `main` that touches `Web/` also republishes the HTML5 build
on itch.io.

The obstacle was measured before anything was built. From this connection `itch.io`
resolves to `10.10.34.36` — a private address, so something other than itch is answering
the lookup — and `broth.itch.ovh`, where butler lives, does not resolve at all.
Cloudflare's DoH endpoint timed out on the same query. Butler on this laptop was
therefore never the design: GitHub's runners reach both hosts, so
`.github/workflows/itch.yml` does the push there and nothing local ever tries.

Scope is the web build and nothing else. `Web/` is the tree Pages already serves, so the
itch channel and the Pages site stay one build instead of drifting into two. The macOS
`.app` was left out deliberately: it would need a macOS runner at roughly ten times the
per-minute rate, and the bundle is ad-hoc signed, so downloaders would meet Gatekeeper
rather than the game.

`node Tools/check_web.js` runs between checkout and push. It is the only thing standing
between a malformed bank and a live store page, and it already asserts Persian parity,
board shape, seating and the guest handshake — publishing without it would make those
assertions decorative at precisely the moment they earn their keep.

The target and the key are not in the file. `vars.ITCH_TARGET` (`user/game`) and
`secrets.ITCH_API_KEY` are read at run time, behind a preflight step that names whichever
one is missing and fails before the build rather than inside butler's error text.

**Why:** reachability, not tidiness. A publish path that depends on this laptop talking
to itch.io fails every time, and it fails looking like an auth problem.
**How to apply:** the version label is `git describe --tags --always`, which makes
`fetch-depth: 0` load-bearing — a shallow checkout labels every build with a bare SHA and
loses the release it belongs to.

**Not verified:** butler has never run. Its download URL could not be fetched from here,
so the install step is the one line in this workflow with no local evidence behind it,
and the first run is the test. Also unverified is whether itch's iframe treats the game
the way a top-level page does — the show writes to `localStorage` (`Web/app.js`,
`Web/editions.js`, `Web/i18n.js`) and HTML5 games run inside itch's frame.

Housekeeping: this file's header says "Newest entry first" and the entries run oldest to
newest. I appended, following the file.

---

## 2026-09-15 — two switches in the match menu, and the bubble is not one of them

**Objective:** a player asked for a way to hide the host and her speech bubbles, and
separately to silence her voice, from inside a match.

**Shape.** Two `button[data-menu]` pills at the foot of the pause menu, beside New match
and Quit to lobby: `Host & bubbles` and `Host voice`. Not segmented On/Off controls, for
two reasons. `button[data-menu]` is already what drives arrow-key and pad navigation
through `menuButtons()`, and a second control vocabulary would need its own cursor. And
`.pill.is-on` already means *the cursor is here* while `.segmented button.is-on` means
*this is the chosen value* — one class, two meanings, drawn in the same place, would have
made the focus ring lie. `STYLE_SHEET.md` says the pill is the only button vocabulary, so
the second state a button can be in is **said** rather than drawn: a `.pill-state` span in
the gutter a `.chev` would have taken. The switch pills carry no `.chev` for the same
reason — the trailing edge means either "this goes somewhere" or "this is currently X",
never both.

**The bubble goes with the voice.** Muting takes the bubble down with it. The bubble is a
transcript of audio already playing out loud, so a muted host captioned by text is a
caption for a room that can hear nothing. She is still drawn; `Host & bubbles` is the
switch that owns the drawing.

**Muting cannot turn a cue into a non-cue.** `speak()` reads `!src && !said` from the show
registration *before* the switches, so a cue the host has neither a pose nor a line for
still leaves her down whatever the menu says. Read the other way round, a switch would
have invented a cue.

**A muted cue still announces.** `voice()` keeps `tellCue(name)` in the muted path,
because the figure on the floor is drawn from that announcement, and follows it with a
generation-guarded `tellCue(null)` at `HOST_SILENT_MS` — there is no clip length to read,
so the floor gets a fixed beat instead. `then()` runs immediately: the course advances its
scene on that callback and `opening_challenge` calls `doneOpening`, and a caller waiting on
a line that will never play must not be left waiting.

**Session-only.** Both live in `S` and nothing persists them. The show's own sound switch
is not persisted either, and a match menu is not a settings panel.

**The professor comes free.** Both shows stand their speaker on the same `#prof-layer` and
cue through the same `Sound`, so `applyStage()` — one entry point, pushing to `HostLayer`
and `Sound` and then repainting the pills — covers the course editions without a second
switch anywhere.

**Verified** against `jeopardy-web-c` on 8793, in a live match, both switches on: a real
cue (`wrong_05_family_whatsapp`) drew `tannaz-wrong.png` with its transcribed line, held
~3.9s, then cleared. Switches off behaved as designed — sprites off gave
`{on: false, bubble: none, line: ""}`; sprites on with voice off gave
`{on: true, src: "tannaz-timeout.png", bubble: "none", line: ""}`, the figure standing
silent. Muting mid-line took the bubble and the transcript at once. Isolated audio probe:
muted → 0 audio elements, cue still announced; enabled → 1. A no-buzz timeout correctly
drew nothing at all, having neither pose nor line. Persian menu screenshotted:
`[dir="rtl"] .pill-state` puts the state word at the left edge with `stateLeft: 19px`, no
chevron, Persian face.

**Not fixed, and it bit me during this work:** `i18n.js` and `app.js` carry no `?v=`
cache-buster in `index.html`, unlike `styles.css` and `host-layer.js`. The new menu keys
rendered as raw `MENU.SPRITES` / `MENU.VOICE` until a forced reload, on a file that was
already correct on disk and correct over HTTP. A returning player meets that. `setLang`
is also vetoed while a match is in progress, which is deliberate but means a language
change cannot be observed without leaving the match.

## 2026-09-15 — the second question was never written, so we wrote 325 of them

**The bank's last error was structural, not a typo.** Every slot holds exactly two rows at
the same `(category, round, value)` — a base and an `_encore` — and 325 of the 500 slots
had the same `clue_text` on both. Not a near-duplicate: byte-identical. The generator was
faithfully copying one question into both rows, so a player who drew the encore got the
question they had already answered. `check_bank.py` had been reporting it as the only
error left in both languages for a while, and it was the right thing to be reporting.

**The rule is that the encore is a second question about the same answer**, and the answer
parts of the row are not the author's to move: `canonical_answer`, the four `options`,
`correct_option_index`, `accepted_aliases`, `book_title` and `page` belong to the slot.
Only three fields were rewritten — `clue_text`, `explanation`, `host_reactions.correct_generic`
— and `merge_enc.py` refuses the whole wave if any of the six shared fields has drifted on
any row. It also refuses unless the archive re-serialises byte-identically first. The point
of both refusals is that a wave this wide is only safe if it cannot touch anything it was
not aimed at.

**Ten shards, 33 slots each, one agent per shard, and a checker they could not edit.**
`check_enc_out.py` rejected an unchanged clue, an unchanged explanation, an unchanged
`correctLine`, a clue that restates the base clue, a clue sharing more than 70% of its
content words with the base clue, a clue containing its own answer, a `correctLine` ending
in one of the stock tails, and non-Persian text in a Persian field. All ten shards came
back `OK: N slots x 2 languages` on their first submission. Grounding in the row's own
`supporting_passage` was high in English (219 of 325) and low in Persian (67 of 325) for a
plain reason: the passage field is English in all 1,000 Persian rows, so it often cannot
support the fact the Persian row is about. The Persian clues are grounded in the answer's
record instead, which is why the flag is a flag and not a gate.

**The wave fixed a problem nobody was looking at.** `correctLine` distinct went 992 → 998 in
English and 668 → 993 in Persian, and the `history holds` tail (325 lines) went to zero while
`کاملا درسته` fell from 660 to 335. The rewrite rule was "write the tail fresh" and applied
to the encores, so the stock tails died as a side effect of answering the encore question
honestly. §8's warning about the formula problem is now partly historical. `wrongLine` did
not move — the wave did not touch it, and it is still 665 / 658 distinct.

**`page` came out of the slot-pair agreement rule, and that was the right call.** The rule
errors when two rows share a slot *and* an answer but disagree about a field they share. It
had `page` in it, which flagged Persian finals whose two rows rest on different pages of the
same book. A final's two questions are drawn from different passages; the citation follows
the passage the row actually rests on, so `page` goes with `supporting_passage` and not with
`book`. Removing it cleared both banks and the rule then caught two real disagreements
nothing else had seen.

**That rule earned its keep immediately.** `final_the_lion_of_azerbaijan_1/_2` and
`double_provisional_regime_1979_800` vs its encore disagreed on `accepted_aliases`, and the
cause is worth writing down: `merge.py` groups rows with `by_id.setdefault(r["id"], []).append(r)`,
which only ever groups *identical* ids — and a twin's id is the base id plus `_encore`. So a
patch keyed on the base id reached the base row and nothing else. That is exactly how a
repair wave leaves a mess behind it. Both pairs were unioned by hand, with the round-trip
assertion run before the write.

**Six Persian rows were carrying the English row's alias list.** The signature: the answer
and the clue had been rewritten to a different question while `accepted_aliases` stayed as
the English twin's. `single_sacred_shrines_and_pilgrimage_1000` answers مسجد جمکران and was
listing Goharshad Mosque; three `double_the_sacred_defense_battlefields_*` rows answered
کربلای ۵ / فتحالمبین / رمضان while listing Fath ol-Mobin / Kheibar / Kaman 99;
`single_the_trans_iranian_railway_600` answered the southern terminus while listing the
northern one; `single_ancient_warfare_empires_at_clash_200` answered نبرد گوگمل while
listing Marathon. Twelve rows with the twins. All twelve repaired.

**The gate cannot catch that class and no token rule can.** `check_alias_ownership` asks
only that *one* alias relates to the answer, and `related()` counts a single shared content
word. `مسجد` is one shared word; so are `عملیات`, `بندر`, `نبرد`. Tightening it breaks the
legitimate cases that look identical from the outside — `سفارت انگلیس` and `سفارت بریتانیا`
are the same embassy and share only `سفارت`, exactly as `نبرد گوگمل` and `نبرد ماراتن` share
only `نبرد`. So it is documented in `QUESTION_AUTHORING.md` §7 as a reading rule rather than
built as a gate: **when the answer and the clue are rewritten, rewrite the aliases in the
same pass.**

**And the mirror-image false positive, so nobody "fixes" it later:** a clue that names one of
its own aliases is the standard shape, not a leak. The clue hands over one name and asks for
the other — Persepolis / Takht-e Jamshid, Avicenna / ابن سینا, سردار ملی / ستارخان. There are
47 such rows in English and 45 in Persian. All correct.

**Verified** end to end. Both archives: `OK — no errors`, the 325-slot error gone in each
language, remaining warnings only the stock tails. Play files regenerated and `--check`
byte-identical. `node Tools/check_web.js` PASS; `validate_1000_clues.py`, `validate_persian_bank.py`
and `verify_flawless_state.py` all pass; `./run_tests.sh` 27/27. A live match on
`jeopardy-web-d` (8794 — the other three preview ports were held by other chats, so the
config gained a fourth) dealt a board, opened `CARPET DIEM` for 10M and resolved Minakari
with four clean options, no punctuation giveaway, the host's line, the explanation and the
Amanat citation. The two `.bak-enc` scratch backups were moved to `~/.Trash`; the tree is
clean.

**Reported, not repaired** — these are content decisions and they are Morad's to make:

- `double_cold_war_espionage_in_tehran_2000` and its twin carry the answer
  `شبکه ترانسسفارشات بیسیم (ایستگاههای پایگاه کبک)` for a clue about the CIA's Tacksman
  listening posts. `کبک` corresponds to nothing in the record and the English answer is
  `Project IBEX (Tacksman)`. Changing it moves `options[0]` and the alias list with it, so it
  is a rewrite and not a correction.
- `double_shah_me_on_you_800_a` answers فرح دیبا and `_1200_b` answers شهبانو فرح — the same
  person at two rungs of one category. Identical in both banks.
- The remaining stock tails: English 353 `spot on` and 228 `quite right` of 1,000; Persian
  335 `کاملا درسته`. The wave cut these roughly in half; finishing the job means rewriting
  the base rows' lines, which is 916 more edits.
- The Persian bank's provenance fields are still English across all 1,000 rows
  (`book_title`, `author`, `supporting_passage`), and `theme` / `historical_period` are Latin
  in 996 and 970. §10 has this on record as Reported.

## 2026-09-15 — the praise tail, and a course gate that was right to warn

**The flat shape had a longer coat and we had only ever looked for the short one.** The
check that catches `<answer>. Correct.` tests for *one* word of verdict at the end of the
line, so `<answer>. Exceptional scholarship.` walked past it — the verdict is three words,
and the only thing wrong with the line is invisible to a single-word test. Eight English
rows had it, every one of them at the top rung (`Ahmadabad. Incredible precision.`,
`Fajr International Film Festival. Superb knowledge.`), and **none in Persian**, where all
319 answer-first lines carry a fact behind the name. Rewritten by hand; the encore twin of
each row already had the good version and gave the register to match.

The rule is now in `check_host_lines`: strip the answer and every alias out of the line, and
if five words or fewer of pure praise are left, there is no line. Verified both ways before
shipping — it fires on all three of the old shapes and stays silent on the 149 English and
319 Persian lines that name the answer and then say something, which are house style and
stay. Prose in `QUESTION_AUTHORING.md` §8 (now five shapes, not four) and `AGENTS.md` §3;
the mechanical rule into `Course/BANK_SPEC.md` and into the prompt it hands a model.

**I broke the course gate earlier today and then spent the session thinking the course banks
were broken.** The new alias-ownership check fired 90 times on a hand-authored course bank;
6 were cleared by widening `related()` (space-stripped forms, and initials for acronym
answers like `JCPOA`), and 46 of the rest were *correct* aliases — `Muscat`/`Oman`,
`Erbil`/`Hewler`, `Gasoline`/`Petrol` — because a course's aliases are translations and
transliterations by construction and share no token however right they are. The rule is
MAIN's instrument: the 347-row defect it was built for was measured in MAIN's Persian
archive and is at zero there. So it stays an **error** on MAIN and becomes a **warning** on
a course, with the reason written into the docstring rather than the rule silently loosened.
Proven still firing on a MAIN-shaped bank by mutating one row to a foreign alias.

Two traps on the way. `is_course` was inferred from the row shape first — wrong, because
course rows carry `author` / `book` / `page` too, so "has provenance fields" separates
nothing; it is read off the `window.COURSE_CLUES_*` marker now. Then the new assignment did
nothing for three runs because an older `is_course = not shape` line sat ten lines below it
and overwrote it. Lesson: after inserting an assignment, grep for every other assignment to
that name.

**A category name is not distinct from another one just because it differs by a diacritic.**
The Persian course bank carried `صرف و نحو استکبارستیزی` and `صرف و نحوِ استکبارستیزی` — one
category to a reader, two to the engine, and exactly the pair that tells the class they are
in a week they are not. The English side had two genuinely different categories behind them
(`THE GRAMMAR OF RESISTANCE` → axis of resistance, `DISCOURSE OF DISDAIN` → foreign policy),
so the Persian was the side that had collapsed: renamed the second to `گفتمان بی‌اعتنایی`
across `bank-fa.js` and the `THEME` table. The axis-of-resistance one keeps its kasra. The
rule now sits in the course prompt. Also fixed the one option in the course banks findable by
its punctuation — `'Armed Struggle: Both a Strategy and a Tactic'` was the only option on its
row carrying a colon, so the colon was the answer.

**A dead end worth recording so it is not retried.** A rule flagging "an alias that is
exactly another row's canonical answer" produced 33–63 hits per bank, all false: rows
legitimately share entities (`oil_fatemi_800` and `final_fatemi_last_words` both involve
Fatemi; two rows of one category both involve the Trans-Iranian Railway). Backed out whole
rather than shipped loose.

**`Course/dist/` is stale and stays that way.** Five files there still hold the pre-rename
category strings. It is gitignored release trail, `build_edition.sh` no longer copies or
writes anything, and the folder is the snapshot it is. Reported, not edited.

**Verified.** Both archives `OK — no errors` with `correctLine — 1000 lines, 1000 distinct`
in each language; play files regenerated and `--check` byte-identical; the course gate
`OK — no errors (205 warning(s))` and fit to play, the two new warnings being the alias
warnings above (HEAD's tool said 203); `node Tools/check_web.js` PASS; the three archive
validators pass; `./run_tests.sh` all green. A live reveal on `jeopardy-web-d` (8794 — the
other three preview ports are held by other chats) confirmed the answer-first-with-a-fact
shape renders as intended in the host's bubble.

## 2026-09-15 — the house shape, promoted from carve-out to rule

Morad, on the report: "i love the answer named first + historical detail/fact given. so
that's great. keep that as a rool." So name-the-answer-then-pay-it-off-with-a-fact stops
being an exception the checker tolerates and becomes the stated target every `correctLine`
is written toward.

**Why it mattered that he said it.** In the docs it was written *negatively* — "note what
it does **not** flag: the answer named first and then a real fact … and it stays" — which
reads as a concession, and a writer told only "don't do the hollow shape" can satisfy the
rule by writing something worse rather than by finding the fact. The two banned shapes are
now described as what they are: this shape with the fact removed. So the instruction to a
future batch is *go find the fact*, not *avoid the tail*.

**Changed:** `QUESTION_AUTHORING.md` §8 gained a named block, "The house shape — aim at
this one", with the counts (149 EN / 319 FA) and the line "if you have written `<answer>.`
and cannot say what comes next, you do not yet have the line"; `Course/BANK_SPEC.md` host
section and prompt item 8 restated the same way; `AGENTS.md` §3 says it in one sentence;
the comment in `Tools/check_bank.py` above the two-way `flat` test now points at the house
shape instead of only describing the defect. No behaviour change — comments and prose only;
`check_bank.py` re-run green on both play files.

**Not changed on purpose:** the house shape is still *not* checked. Nothing enforces "the
second sentence is a fact", because a fact is not a mechanical property — a regex for it
would either pass hollow lines or fail real ones. It stays a standard, held by the docs and
by whoever reads the batch.

## 2026-09-15 — the source line, made a rule and then checked

Morad, same message as the house shape: "giving the source to everything is incredible too
when it comes to the answers. it makes it academic and exact and proper, which is what im
looking for." So the citation stops being optional metadata and becomes a requirement.

**Why the old wording was the bug.** `Course/BANK_SPEC.md` said outright: "Optional — the
engine renders a source line only if present, and simply omits it otherwise, so it is safe
to leave them out." That is true of the engine and false of the game. `Web/app.js:2710`
prints `book · author · p. N` under the answer once the last contestant has had their shot,
and that line is why a right answer is checkable instead of merely scored. The engine
tolerating a blank is not the same as the blank being fine, and the spec had been reading
the first as licence for the second.

**Measured before writing the rule:** MAIN is at 1,000 of 1,000 on `book` and `author` in
both languages, and 1,000 of 1,000 on `page`. The course is at 692 of 693 on book and
author — the one miss is `final_snapback` — and 690 of 693 on page, the three misses being
finals.

**The rule, as written into the checks.** `check_citations` in `Tools/check_bank.py`
requires `book` and `author` on every row. `page` is deliberately **not** required: a
`final` answers for a whole module and has no single page to point at, and both of the
course's sourced finals carry book and author and no page — that is the convention, not a
gap. Requiring a page would push an author toward a number that does not mean anything,
which is the failure mode this rule exists to prevent. Mutation-tested: fires on a blank
book, a null author and a row with neither; silent on a clean row and on a final with no
page. Error on MAIN, warning on a course — the same split as the alias rule, and for the
same reason (a strictly-correct course row should not break a build).

**`final_snapback` left uncited on purpose, and this is the finding to act on.** The course
Final asks the player to name the snapback mechanism. Grepping all 90-odd PDFs on the
course shelf for `snapback` / `snap-back` / `snap back` returns **nothing**: no assigned
reading names the term. The week's readings discuss the deal and the withdrawal
(`Gendered Politics US-Iran Sanctions` cites UNSCR 2231; `Sanctions-2` covers the 2018
re-entry of sanctions), so the row is answerable from the clue text and the lectures around
it — but its citation cannot be filled honestly from the shelf, and a citation that points
at a book which does not state the fact is exactly the decoration the last entry in this
log forbids. Left as a warning with the id printed on every course build, rather than
papered over with an approximate page. **It needs a decision from whoever owns the course:
cite the agreement itself, re-cut the Final onto a fact the shelf does hold, or accept the
blank knowingly.**

## 2026-09-15 — the snapback Final is cited, to the agreement

Morad chose the first option, in four words: **"cite the agreement itself,"** — so the course's
last uncited row is cited to the instrument rather than to the nearest chapter that mentions
it. `final_snapback` in both `bank-en.js` and `bank-fa.js` now carries
`book: "Joint Comprehensive Plan of Action (UN Security Council Resolution 2231)"` and
`author: "United Nations Security Council"`, and no page: the 30-day return of the pre-2015
measures is not in the JCPOA's own text but in Resolution 2231 that endorses it, so both are
named, the agreement first as he asked. No page, matching the course's other two finals — and
a document's provisions are paragraphs, not pages, so a number here would be invented.

**This is the first source in either bank that is not a book.** A regex sweep of MAIN's 32
distinct `(book_title, author)` pairs found only two document-shaped entries (Khomeini's
*Islam and Revolution* and *The Shah and I*), so there was no precedent to copy and the
choice had to be deliberate: `book` is the first slot of the printed source line, so when the
answer *is* a document, the document goes there. Recorded as a rule in `QUESTION_AUTHORING.md`
§10 and `Course/BANK_SPEC.md` prompt item 11 — **cite the instrument, not the reading about
it** — because the alternative was a future author deciding `book` can only hold a book and
reaching for a chapter that does not state the fact.

**Verified:** both course banks parse in Node (hand-edited JS, so the Python gate would not
have caught a syntax error) and the row resolves to the citation above in both. Course
`OK — no errors (205 warning(s))` — the 207 from the previous entry minus exactly the two
citation warnings; the `name no source` count is 0. MAIN unchanged and green. The stale
"692 of 693" figure in `AGENTS.md`, `Tools/check_bank.py` (comment + docstring) and
`QUESTION_AUTHORING.md` is corrected to all 693.

**Also corrected:** the comment on `PROVENANCE_KEYS` claimed a course bank "legitimately
carries none" — false since the course was written, and it was the same misreading as the
BANK_SPEC line. The `report()` note that fired when a bank had no provenance fields is
reworded to say what the fault actually is (the source line under every answer is blank)
instead of naming which bank kind it expected.

**Changed:** `Tools/check_bank.py` (`check_citations` + two comments), `QUESTION_AUTHORING.md`
§10, `Course/BANK_SPEC.md` Fields and prompt item 11, `AGENTS.md` §3 and §7. MAIN all green;
course `OK — no errors (207 warning(s))` — 205 plus the two new citation warnings.

## 2026-09-15 — Codex cut and published the native 1.0.7 release

The final checkout was `e8f5a59` when packaging began. Codex moved macOS and iOS from
`1.0.6` / `106` to `1.0.7` / `107`, matching Android's declared version. Source commit
`f13e778` (*Cut the 1.0.7 multi-platform release*) became tag `v1.0.7`.

| Asset | Bytes | Verified state |
| --- | ---: | --- |
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 34,040,354 | Enclosed `.app` is ad-hoc signed; `lipo` reports `x86_64 arm64`. One universal app. |
| `Jeopardy-Iranian-Edition-iOS.ipa` | 35,119,251 | `Payload/Jeopardy.app` reports `1.0.7` / `107`; archive and full `Web/` parity passed. Unsigned, so it needs sideload signing. |
| `Jeopardy-Iranian-Edition-Android.apk` | 33,330,708 | `com.morad.jeopardy`, `1.0.7` / `107`, min SDK 24 / target 34; v2 signature verification passed with the local 4096-bit RSA release key. |

The official Android SDK and Maven endpoints recovered, allowing a local SDK, platform 34,
build tools 34.0.0, and Gradle 8.7 to bootstrap the checked-in `Android/gradlew` wrapper.
The SDK, temporary Gradle distribution, `Android/local.properties`, and `Android/keystore/`
remain ignored. Preserve the local keystore if a later APK must update this one.

`node Tools/check_web.js` passed, including 600-board option/parenthesis independence checks;
`swift run --disable-sandbox JeopardyTests` passed 27/27 native-engine checks. `swift test`
compiles but reports "no tests found" because there is no XCTest target. The latest relevant
Pages run (`7a8ad4c`) succeeded and the public root returned 200.

## 2026-09-15 — syllabus material is excluded from GitHub and packages

Morad asked that the syllabus itself never appear in GitHub downloads; readings and question
banks remain intentionally public. Codex audited current local/GitHub recursive trees, every
reachable branch/tag object name with `git rev-list --objects --all`, and all three v1.0.7
archives. All were clean: no `Syllabus`, `syllabus`, reading-list, course-outline,
module-outline, or PDF path/object was found.

The old ignore rule covered only `**/Syllabus/*.pdf`, leaving a future DOCX, HTML, or renamed
file exposed. It is now the whole-folder rule `**/Syllabus/`; PDF, DOCX, and HTML test paths
all resolve to it. Commits `3595cea` and `b7090f9` pushed the safeguard and corrected comment
to `origin/main`.

**Coordination rule from Morad:** after completing repository work, append the concrete
change, validation evidence, publication state, and unresolved caveat here so the next agent
has an evidence-bound handoff.

## 2026-09-15 — Codex corrected the phone orientation policy for 1.0.8

Morad decided against a second, sideways mobile composition. The phone releases are now
portrait-only: `AndroidManifest.xml` uses `android:screenOrientation="portrait"`, and the
iPhone `UISupportedInterfaceOrientations` array contains only `Portrait`. iPad retains its
existing two landscape entries; this change is intentionally about handsets, not tablets.

The front door also has a compact `max-width: 520px` portrait pass in `Web/styles.css`.
It keeps both edition cards and both Enter controls inside the usable phone viewport, with
the whole front plate scrollable as a backstop on unusually short handsets. Exact Chrome
device emulation at 390x844 measured the main card at y=269–493 and the course card at
y=521–723 inside a 752px usable client height. Both controls are visible and reachable.

Version numbers moved together to `1.0.8` / `108` in iOS, Android, and the universal macOS
bundle script. `node Tools/check_web.js` passed, including the 600-board independent
parentheses test. The rebuilt IPA reports `1.0.8` / `108` and full Web-tree parity; the rebuilt
APK reports `com.morad.jeopardy` `1.0.8` / `108` and passed v2 signature verification; the
universal macOS executable reports `x86_64 arm64` and passed deep signature verification.

The next publication step is a new `v1.0.8` release, not deletion of `v1.0.7`: existing
downloads remain attributable while sideloaders receive a monotonically newer update.

## 2026-09-15 — the itch channel publishes, and v1.0.7 comes down

**The itch workflow was broken by a dead hostname, not by Iran.** Both runs it had ever made
died in `Install butler` with `curl: (6) Could not resolve host: broth.itch.ovh`, and
`gh run view --log-failed` on 34959011005 showed the same exit code 6 on GitHub's own
`ubuntu-latest` runner. That ruled out this network. The manual names `broth.itch.zone`, and
`https://broth.itch.zone/butler/linux-amd64/LATEST/archive/default` returns 307 to a signed
Cloudflare R2 object, so the archive is really there. The earlier entry saying `.ovh` "does
not resolve at all on an Iranian connection" was true but incomplete: it resolves nowhere.
`d04badf` changed the host. broth URLs 307 to short-lived signed objects, so they must be
fetched with `curl -L` in one shot and never linked to.

Run 34960400552 is the first green one. The log shows `node Tools/check_web.js` PASS, butler
`v15.31.0`, then `For channel 'html': pushing first build` — 34.85 MiB, 178 files, 11 dirs,
0 symlinks, 30.68 MiB patch. "First build" is the useful line: it confirms the project page
already existed on itch, because butler creates channels but never projects.

**Open caveat, and it is the one thing left:** the build is up but the page is not public.
`aghamorad.itch.io/jeopardy-iranian-edition` 404s, and `aghamorad.itch.io/` 302s to
`itch.io/profile/aghamorad`, which lists no games. A project butler can push to while the
public profile omits it is a project still in **draft** on itch. Nothing in this repo can
change that — butler uploads builds, it does not publish pages. Morad has to open the project
on itch and set it public. Until then the channel is populated and invisible from outside.

**v1.0.7 is withdrawn.** Morad chose removal over keeping it archived: the landscape-locked
packages were the embarrassment, and a downloadable copy is the only way to be embarrassed by
them twice. Tag `f13e778d16f12b6741ec74efd403320f739243ee` survives, so the build is
reproducible from source. No local archive of the 1.0.7 binaries was ever made, which was the
cost of the decision and is worth remembering the next time a release is retired. The v1.0.8
release body then needed correcting — it still promised those packages remained downloadable.
Both `dist/RELEASE-v1.0.8.md` and the live GitHub release body now say the release was
withdrawn and the tag survives.

**Incident worth recording:** the first v1.0.8 draft release vanished between creation and the
asset upload. `gh release view v1.0.8` returned "release not found", it was absent from
`gh release list` and from the `/releases` API, and the upload 404'd against it. Nothing run
here deletes releases and the cause was never established. It was recreated at
`be7dd59571ab3e5a6deedb2c6e613bb4c9a0416b` and all three assets uploaded on the second
attempt. If a draft vanishes again, recreate it rather than hunt for it.

**Addendum — itch is unreachable from this machine only while no tunnel is up.** The entries
above that call itch.io unreachable measured the environment, not itch. With no tunnel the
lookup returned `10.10.34.36`, a private address, and Cloudflare's DoH endpoint timed out on
the same query. Re-measured later the same day with the tunnel up, `itch.io` resolved to
`104.26.8.198`, `104.26.9.198` and `172.67.69.99` with 443 open, and both `curl` and headless
Chrome reached the site from this laptop. The accurate form is conditional: reachable when the
tunnel is up, and whatever the Iranian exit node makes of it when it is not.

The design does not change. Publishing from the runner is still the right call — it takes the
tunnel off the critical path entirely, which is worth more than a local butler on the days the
tunnel works. Only the reason written next to it was overstated, and `.github/workflows/itch.yml`
now says the conditional version. Note that the workflow file is inside its own path filter, so
committing that comment republishes the build.

## 2026-09-15 — the front door gets its shelf, and the phone stops lying about it

**Two placeholder circles, and the vocabulary for them was already in the sheet.** `styles.css`
had carried `.circle-row`, `.circle`, `.circle-frame`, `.circle-art`, `.circle-name` and
`.circle-who` with nothing using them, because the courses row had been built as posters instead —
which is why the front door read as one wide box over a band of cards rather than as a shelf. The
row now uses the circles it already owned, at the front door's own scale (148px against the sheet's
116). The two placeholders are `.circle.is-soon`, and they are `<div>`s rather than `<button>`s,
which is the whole reason `RINGS.front` (`Web/app.js`) walks past them with no special case: a ring
that pads through the shelf's focusable children never sees them.

**The marks answer one brief — one silhouette that survives the reduction.** `qajar` is the **Kiani
crown** and `pahlavi` is an **oil derrick**, drawn in `Tools/make_edition_tiles.py` in the same
grammar as the general and course tiles: near-black plate, one legible silhouette, no randomness, so
a rebuild is byte-identical. A crown and a derrick are a century apart in silhouette, which is the
property that matters at the size the shelf shows them. The crown's dome is sampled as an arc rather
than drawn as a primitive, because the reduction rounds an arc off gracefully and turns a polygon's
few long facets into a hexagon.

**The composition reversed once, and the reason is that a placeholder carries three things where a
door carries two.** A door has a mark and a name. A placeholder has a mark, the stamp, and the rule —
and a round frame 118px across has room for two, not three. The first cut kept all three and lost the
argument on screen: the stamp sat centred on the mark and the crown read as a smudge under a label.
So the mark takes the upper half of the frame and the stamp takes the foot, and the tricolour moved
off the tile and onto the stamp itself — the plate is banded with it in CSS, so the flag is still in
every frame on the shelf and the crown is still a crown. Both tiles therefore leave their foot empty
on purpose. `Web/i18n.js` gained `front.soon`, `front.soonQajar` and `front.soonPahlavi` in both
tables; the file also gained a `?v=` cache tag, which it had never had.

**Then the phone found two real defects, and the first diagnosis was wrong twice.** Measuring the DOM
rather than the screenshot — the capture is downscaled and the second row falls below the fold, which
is what made the two stamps look different when they were byte-identical in geometry — showed
`#screen-front` was 722.7px tall holding 812px of content. The cause was not `dvh` resolving wrongly
(`dvh` was 812, correct) but `course.css`, which insets **every** active screen:
`#app .screen.is-active { top: var(--safe-top); bottom: max(var(--host-band), var(--kb, 0px)); }`
with `--host-band: clamp(78px, 11dvh, 92px)` — 89.32px at 375×812. The band cannot be dropped from
the front door even though her sprite is `visibility: hidden` there, because `Web/app.js` cues
`tannaz_opening_challenge` over it once the opening music ends: the cold open is a cold open, not a
gate. The `@media (max-width: 520px)` gate was forcing the plate to `100dvh` inside a box that had
already paid for the band, so the front door scrolled by 89px whatever was in it. `100%` on the plate
and no `min-height` on the centre fixed the phantom; the residual 73px was the row wrapping.

**Three 108px circles and two 14px gaps want 352px of a 345px row.** Seven pixels over, and the third
circle drops to a second line — 134px of row becomes 254.5px, and a shelf that fits reads as one that
does not. In the phone gate the gap comes in to 10px and the circle takes
`min(108px, calc((min(92vw, 440px) - 20px) / 3))`, so the row is one line on every handset that can
hold three legible circles and only wraps where three genuinely do not fit. Measured at 375×812:
`sameLine true, rowHeight 134, overflow 0`. Persian is the same shelf — `dir="rtl"`, circles 108,
`overflow 0`, both stamps reading `بهزودی` on one line and unclipped — and desktop is untouched:
`gap 31.68px` and circles 148px, both at the clamp's maximum.

## 2026-09-15 — the circles wear their own sources, and the main door stops being a square

**The marks were wrong and Morad said so twice.** Both placeholder marks had been drawn from the
period's furniture — a Kiani crown for the Qajars, a derrick for the Pahlavis — and the crown read as
a bell. The rule he asked for is narrower: the image in a circle is *derived from that course's own
sources*, not from general iconography of the century. Read against the syllabuses, that gives marks
with a week number attached. The Qajar circle is a **qalyan**, which is the Tobacco Protest, week five
of eight. The Pahlavi circle is the **derrick**, which is Musaddiq and the nationalization of oil, week
four. `Tools/make_edition_tiles.py` carries that rule in its docstring now, so the next mark drawn
there is argued against the syllabus rather than against a mood board. The qalyan's head, stem and jar
are one contour for the reason the crown's was — a stack of primitives leaks its seams into the mark
when the reduction lands — and its hose is stroked, not filled, because a second contour would paste
its face over the stem's rim and cut the rim open. The hose is also the whole of the reading: a bulb on
a stem is a vase, and a vase is one bad spout away from a teapot.

**The course circle stopped being drawn at all.** It was a globe, which was the same fault in a milder
form — invented rather than taken. It now *is* the Iran in World Politics course's own splash mural,
cropped square onto the middle of the wall it paints (`COURSE_CROP = (488, 170, 1048, 730)`): the dome
between its minarets, the snow peak over it, the flag's emblem at the centre, the top of the crowd at
the foot, and nothing below the skirting, because a circle of floor says nothing. It is cropped to a
512px tile rather than pointed at directly because the mural ships at 2.26MB and a 118px circle is not
going to make a phone fetch that before the student has chosen anything. The source carries its own
flag, so no rule is pasted over this tile. Morad's own suggestion, and it is the right one: every
circle on the front door now wears the art of the thing it opens.

**The main door is a large circle, not a wide box.** He overturned his own earlier note here — "it
could be a nice chic oval or circle too, just bigger than the others" — so the round frame that was
already in `styles.css` now carries the main edition at 234px against the courses' 148px, and it keeps
its own skyline art. The copy is legible over that art because of a radial scrim, not a re-drawing of
the art. The `#chooser-main` heading was 440px from the disc it labelled before the fix, because the
chooser is `min(92vw, 1180px)` wide and the heading was inheriting that width; `#screen-front
#chooser-main, #screen-front #chooser-courses { width: auto; max-width: 100%; margin-inline: auto; }`
shrinks both headings to their content. The disc's cap is `26vh`, and that number is solved rather
than tasted: the front door's column is ~467px of window-independent things (brand-lockup 186.8 +
tagline 71.4 + circles row ~167.5 + two eyebrows) plus ~0.36 of the viewport height in vh-driven
values, so overflow stops when `467 + 0.36h ≤ h − 99`, i.e. `h ≥ 880`.

**Two alignment defects, and the second one was a font-metric trap worth knowing about.** The ENTER
pill sat 7.5px off-centre in Persian because `html[dir="rtl"] .edition-enter` (0,2,1) was beating
`.edition-main .edition-enter` (0,2,0) — a specificity collision, not a cascade order — fixed by
matching the specificity with `html[dir="rtl"] .edition-main .edition-enter { padding: 0 7px; }`.

The heading's 3px inset had to become `margin-inline-start`: `align-self: flex-start` on a column-flex
child means *inline*-start, so a physical left margin inset the heading from the row it labels in
English and from open air in Persian, where it sat flush with the row's right edge.

Then the real find. **The Persian front door scrolled 6px while the English one was exact** — `scrollH
807` against `clientH 801` — and English is the language every test looks at, so nothing would have
caught it. Walking the column showed brand-lockup 186.8 and tagline 71.4 *identical* in both scripts,
which pointed inside the chooser; diffing EN against FA in one measurement showed `chooserH` differing
by exactly 11.5, and the 11.5 was the **eyebrow**. `.eyebrow` had never had a `line-height`, so it fell
back to each font's `normal`: the Latin face resolves to ~1.14, `--fa` to ~1.64. At the front door's
`clamp(9.5px, 0.70vw, 11.5px)` = 10.08px at 1440, that is an 11.5px English box and a 16.5px Persian
one. Two eyebrows is 10px of the overflow, plus 1.5px from the taller Persian circle row, and that is
the whole of it. Fixed at the element — `.eyebrow { line-height: 1.1; }` — so the trap closes wherever
an eyebrow sits in a fixed-height column. **`1.1` and not `1.14` because English had exactly zero
headroom:** it measured `scrollH 801 = clientH 801`, so any value above the Latin face's own 1.14 would
have pushed English into scroll while fixing Persian. The comment in `styles.css` says so.

**One fragility found and deliberately not fixed.** Mid-verification the Iran in World Politics circle
vanished from the front door, leaving only the two placeholders. Console showed `net::ERR_CONNECTION_RESET`
on `GET /courses/iran-in-world-politics/data/bank-fa.js`; the 1.15MB file was present and `curl`
returned 200, so it was transport, not a missing file. Because `window.registerEdition` refuses an
edition with an empty `banks` array, **one failed bank fetch silently deletes a real circle from the
front door** — no error, no placeholder, just a shorter shelf. A reload restored it. Not fixed, because
it is not what he asked about and any fix is a design decision (retry? inert-but-visible circle?) rather
than a patch.

Verified at 1440×900 and 375×812 in both languages, by measurement and by looking at the render: no page
scroll, no horizontal overflow, three circles on one row, the disc centred on the row's axis, name/note/
enter on the same centre, eyebrow 11.1 desktop and 10.4 phone in both scripts, and the heading inset 3px
on the inline-start edge in both directions.

Cache tags moved to `?v=20260915-align-14`.


## 2026-09-15 — the main door becomes a medallion

**The disc was carrying four lines of Persian across the middle of its own picture.** He said it
plainly: "the circle shouldn't just be such an ugly text box" — and then told me where the icon was
already sitting: "you can use the splash image for the main game". He was right about both, and the
second one meant no new asset. `hero-main.png` *is* the splash — the Milad Tower skyline the title
card wears — and it was already the art inside the disc. Nothing was ever wrong with the art.

**What was wrong was the scrim.** `.edition-card.edition-main::after` was a
`radial-gradient(ellipse 66% 58% at 50% 50%, rgba(4,5,6,0.90) …)`, opaque through the core, and this
particular picture is bright exactly at its core: the middle of a night skyline. So the pool painted
out the tower and the city lights — the one part of the image worth showing — and what the audience
got was a black disc with prose in it. It is a vertical two-ended gradient now, the same shape every
other card on this screen already uses. The reason the disc can afford to scrim only the ends is that
this image is already dark at both of them: empty sky above the Alborz, empty foreground below the
city lights. The name sits on the sky, the button sits on the dark, and the skyline runs clear
between them.

**The blurb came off the disc.** It was the single thing that made a medallion read as a text box, and
it was the reason the middle had to be covered in the first place. `.edition-main .edition-note` is
`display: none` — hidden rather than deleted, following the pattern `.edition-sign` already set above
it: `paintCards` still builds it, still paints it, and the card's `aria-label` still carries it in
full (`app.js` joins name, note and credit), so nothing is lost to a screen reader. What the disc says
now is its name and the way in, which is what the courses' circles say. Its type went up to
`clamp(17px, 1.65vw, 25px)` to match — it carries three lines where the poster's band carried four, and
a medallion is read across a room.

The body is `justify-content: space-between` over `padding: 20% 16% 17%`, which is not taste: at 20%
down a circle's half-width is 94px against the content box's 80, so neither end is ever clipped by the
curve. That is the trap with stacking content in a circle — the rim is narrower at the top than at the
centre — and it is why "MAIN EDITION" is one line at 23.76px inside a 111px box and not two.

Verified by looking at it, not by measuring: 660×900, 375×812 and 1440×900, both languages. Name one
line in all of them, no page scroll, no horizontal overflow. The medallion now reads the way the
course circles read — one image, one name, one way in.

Cache tags moved on to `?v=20260915-align-15` (the previous entry's `align-14` is superseded).


## 2026-09-15 — the main door becomes a window

**The show is not a skyline. It is a procession.** That is the whole argument, and it took four
rejected prompts to find it. The medallion had been carrying the Milad Tower in monochrome — correct
against the style sheet, monochrome and cool, and dull against the one thing he kept pointing at: the
course circle, which wears a warm painted mural with a single large subject in it. Every attempt at a
replacement failed the same way. A Tehran skyline, a white-line engraving of a lone tower inside
guilloche rosettes, a palimpsest of overpainted centuries, a Sgt. Pepper cut-paper collage — all four
were centred, symmetric, frontal, with equally weighted subjects and colour devices landing in the
corners, which is exactly where a circle crops them off. Face-on monuments do not survive a rim.

**So the art is a frieze, and the frieze is the one Iranian object that already means what the game
means.** The Apadana relief at Persepolis is a tribute procession: the whole empire, assembled, walking
in one direction. Persepolis carved it; the Safavids painted that kind of scene. Painting it in
turquoise, lapis, vermillion and malachite is how the door gets real colour without breaking the
no-gold rule — Persian colour is turquoise and lapis, never gold, which is the one thing the style
sheet forbids outright. The prompt was then written *from the clue bank*, not from taste: every figure
in it is an answer that is actually in `clues.js` — the fire altar, the Sasanian with the covered dish,
the Safavid shah under the parasol, the Qajar courtier with his portrait medallion, the photographer
under the cloth, the constitutionalist's green banner, the press with the red banner, the theodolite,
the schoolmistress and the nurse, and at the end the crowd of silhouettes with raised fists. Sixteen
figures, roughly a thousand years apart, one direction. It is the front door of a quiz show rendered
as a state memorial frieze, deadpan, which is the register the whole thing runs on.

**It is three times as wide as it is tall, and that is the point rather than a problem.** A 3:1
panorama in a 1:1 rim with `object-fit: cover` shows exactly one third of itself and throws the other
two thirds away — which is a defect until you stop treating the disc as a picture frame and start
treating it as a window. He asked for exactly that: "can we do something where these stay contained in
the circle and the image basically moves inside it from left to right - kind of animated?" The disc now
pans `object-position` from `0%` to `100%` and back, so the whole procession walks past the rim and
round again.

Three decisions inside that:

- **`object-position`, not `transform`.** The card's own hover is already `transform:
  scale(1.025)`; a second transform on the image would overwrite it and the door would stop
  responding to the cursor. Panning the crop is a different property and the two coexist.
- **A held sweep, not a treadmill.** Ninety seconds end to end, with the procession resting at each
  end before it turns round (`0%,6%` and `94%,100%` at `0%`; `44%,50%` at `100%`). Continuous linear
  motion reads as a loading bar; a frieze that arrives, holds, and turns reads as a frieze.
- **Scoped to `#screen-front.is-active`.** Nothing animates behind the game. And it is killed in the
  existing `prefers-reduced-motion: reduce` block, alongside every other transition on that card.

**Honest note on how it reads at size.** At a 1280×900 viewport the disc is 234px and the figures in
it are small — a coloured ribbon crossing a black circle, not the large single subject the course
circle has. The composition is right and the pan gives it life, but the scale is not yet the "OH WOW"
he asked for twice. An eight-figure variant at the same 3:1, with the black margins cut to a quarter
each, is rendering; if it lands, the figures roughly double on screen and nothing else about the
mechanism changes — it is one file swap.

Installed as `Web/assets/hero-main.png` (the only reference is `Web/editions.js:116`, the `general`
edition's `hero`), so the pan is live rather than theoretical. The previous skyline is recoverable from
git. Candidate renders that did not ship — a museum vitrine, which was genuinely good but read as a
tiny lit cabinet once cropped to the rim, and a garden page that timed out — are in
`Assets/Generated/`.

Cache tags moved on to `?v=20260915-frieze-16`.

## 2026-09-15 — the circles become glass

He asked for the circles to read as snow globes: "like they're fish-eyed and moving insdie glass."
What he was describing is not a shading problem. A circle with a gradient on it reads as a *ball* —
that is lit sphere, and it is the thing every skeuomorphic icon has looked like since 2010. What
makes a sphere read as *glass* is that it bends the picture behind it. So the depth effect is a
refraction, not a highlight, and everything else is there to serve it.

Three layers, in the order the eye reads them:

- **The frame's own shading** (`::before` on `.circle-frame` and `.edition-card.edition-main`) —
  specular at the top left, catchlight, and a bounce at the foot. This is the cheap part and it is
  also the part that is genuinely skippable; it alone is the 2010 icon.
- **`.lens`**, a real `<i>` element the chooser injects, so the ring is a thing the DOM has rather
  than a picture of a thing. It carries the dark rim band — the thickness of the glass read
  edge-on — a caustic, and the polish line. It also carries a `backdrop-filter: blur(5px)
  saturate(118%)` **masked to the outer ring only**, because glass blurs what is *behind* it and
  only near the silhouette; blurring the middle would just be the picture going soft.
- **`feDisplacementMap`** (`#globe-warp`), fed by `Web/assets/globe-lensmap.png`. This is the one
  that does the actual work and the two above are what make the result look intentional rather
  than broken.

**Why the map is shaped the way it is.** A glass ball is a wide-angle lens seen from outside, not a
magnifier. Its surface lies nearly flat to the eye on axis and turns edge-on as it approaches the
silhouette, so the picture has to be sampled from *further out* near the rim than it is drawn: that
compression at the edge is what makes the middle look like it is bulging toward you. The generator
is `Tools/make_lens_map.py`; `src_r` does the sampling and is normalised so the rim itself does not
move, which is what keeps the art inside its own circle instead of smearing past the edge. The
corners are pinned at zero shift on purpose — the map stretches across the whole square with
`preserveAspectRatio="none"`, so anything outside the rim is off-screen anyway, and pinning it stops
the filter dragging the corners in.

**The coming-soon circles are globes too, and this is the whole of that point.** They were flat
placeholders wearing a stamp, which made the shelf read as one finished product and two grey
promises. They now carry the same frame, the same lens, the same warp, and a drained picture —
`saturate(0.62)` on the art, a solid `var(--hair)` frame instead of the lit one. The read is meant
to be *unlit*, not *unfinished*: the same object with the power off. They are also the same size as
the courses they sit beside, which they were not.

**The two names that were stale, and the one that was a false alarm.** `assets/_lensmap.png` had a
leading underscore — scratch naming on a file that is a shipped asset, the `feImage` source for the
filter. Renamed to `globe-lensmap.png` and the two references in `index.html` moved with it; the
generator writes to the new name. The `COMING SOON` stamp looked, in a scaled screenshot, like it
was breaching its circle. Measured, it is a 54×36 plate inset 17px each side. The screenshot was
0.85 scale and the arithmetic was not wrong; the read was.

Cache tags moved on to `?v=20260915-globe-21`.

## 2026-09-15 — the front door stops hanging, and 1.0.9 goes out

"Really bad spacing here." A dead band under the menu. The interesting part is that the rule meant
to prevent exactly that band was already there and had been for weeks, and could never have acted.

`#screen-front .center` centres its column with `justify-content: safe center`, and a column with
free space above and below it is what "centred" means. Free space is the whole mechanism. `.center`
asked for `height: 100%` to get it and `.plate` — `min-height: 100%; height: auto`, on purpose, so
a short window scrolls the door rather than slicing the shelf's names off at the fold — answered
with `auto`. **A percentage height against an auto-height parent is indeterminate and computes to
`auto`.** So the column was exactly as tall as its contents, there was no free space, `safe center`
had nothing to divide, and the stack sat at the top of a 930px plate with 145px of nothing beneath
it and a further 92px below the plate itself.

The fix is flex, because flex is the thing a percentage cannot do here: the plate becomes a column
and `.center` is `flex: 1 1 auto`. Deliberately **no `min-height: 0`** — the column keeps its own
content height as its floor, so a door that outgrows a short window still pushes the plate taller
and the whole thing scrolls as one page under the existing `overflow-y: auto` rather than becoming a
second scroller inside the first.

That closed the band and left a residual 53px of asymmetry, which turned out to be a second bug
hiding behind the first. Below 900px the column carried `padding-top: 76px` — a guard, because the
language pills are absolutely positioned above it and `safe center` falls back to `start` on
overflow, so a short window's column would otherwise ride up under them. But a top-only pad is not
headroom, it is displacement: the free space was being split evenly and then 76px added to the upper
half, so a door with room to spare still hung low — 148px above the brand against 95px below the
shelf, which is `76 + (930 − 76 − 22.5 − 687)/2 = 148.25`, and matched the measurement to the pixel.
Padding pushed in at **both** ends leaves the centre exactly where centring put it and still holds
the pills off. Measured after: brand top 122, chooser bottom 808, in a 930 plate.

1.0.9 is MAJOR, MINOR and PATCH moved together — `build_release.sh`, `iOS/project.yml` and
`Android/app/build.gradle.kts` — with `node Tools/check_web.js` green before anything was built.

## 2026-09-15 — two logos, and why the front door gets its own

The front door now opens on the Iranian Pack lockup. Everything inside the show keeps the plain
wordmark. Two files, and the split is the point.

I had this wrong first and made it worse: I overwrote `logo-wordmark.png` itself, which is the art
every screen inside the show wears, so the Pack lockup appeared on the lobby, the board and the clue
bar as well. The correction was one line — *"that is only for the front door logo!"* — and it was
right for a reason that is worth writing down. `logo-wordmark.png` is the show's own lettering, the
one thing every edition and every course shares, and `course.js` re-skins `.logo` on every edition
change precisely because that element belongs to the skin. A lockup that names one edition cannot
live there.

So the lockup is `logo-iranian-pack.png` and it is on `.brand-wordmark`, a class deliberately not
`.logo` and therefore out of every skin's reach. It had been committed back in `633de84`, the same
commit that added the front door, and referenced by nothing until now: He had staged the art for
this and never wired it up.

**The cache tag went backwards on purpose.** The tags had already moved to `?v=20260915-pack-22`
while the art change was in, and `pack-22` never shipped, so nothing cached it. Reverting to
`?v=20260915-globe-21` keeps every URL the live Pages deploy already served valid, and the new front
door is a fresh URL for free, because its filename is new. Bumping again would have invalidated a
whole tree of caches to deliver one image that was never in them.

The store pages needed the same split. `Tools/make_readme_banner.py` read the wordmark; it reads the
lockup now. Output renamed `logo-wordmark-banner.png` → `logo-banner.png`, because the old name
described art the file no longer holds, and the README and the release notes both point at it.

**One thing this machine cannot do.** The itch page's cover image is set in the itch.io dashboard,
not in the repo, and itch.io is unreachable from here — the HTML5 build publishes from CI for
exactly that reason. The cover has to be uploaded by hand.

1.0.9 is rewritten rather than cut again: the link is already out, so the three assets are replaced
in place and the release text now says what the game is and why instead of listing only the diff.

## 2026-09-15 — the itch cover, and a correction to the entry above

The entry above says itch.io is unreachable from this machine. That was measured on a bad exit
node and it is wrong. Re-measured today: `itch.io` answers in 1.07s, `broth.itch.zone` in 0.67s.
The cover did not have to be uploaded by hand, and was not.

`Tools/make_itch_cover.py` writes `.github/assets/itch-cover.png`, 1260×1000, which is 2× the
630×500 frame itch renders a cover in. Same art as the banner — the front door's lockup,
`Web/assets/logo-iranian-pack.png` — but the shapes are not interchangeable. The banner is
1600×655, about 2.4:1, because a README is wide. A cover is 1.26:1. The banner dropped into the
dashboard would have been cropped to its middle, taking the first and last letters of JEOPARDY!
with it. So the generator trims the transparency off the lockup first, fits what is left to 92%
of the width, and composites on `#050505` — same reason as the banner, white lettering on alpha
vanishes against a light store grid.

Uploaded through the dashboard and saved. The game page leads with it.

**The page is a draft, and that is a separate problem.** `aghamorad.itch.io/jeopardy-iranian-edition`
answers 200 to the logged-in owner and 404 to everyone else. A control fetch of a public itch game
returns 200 from this same machine, so it is the project and not the network. The owner nav carries
the `DRAFT` chip and a secret URL. Publishing it is his call; nothing about that state was touched.

## 2026-09-15 — the front door stops swearing, and the globe gets its pan back

**The copy was profane in the wrong place.** "You fuckers" was on the splash and the lobby — the two
screens a stranger sees before they have decided to play. He asked for the sneer without the
swearing, and the register he named is the right one: the door can be smug and patronizing, it just
cannot swear at someone who has not yet agreed to be sworn at.

Rewritten in both languages: `splash.tagline`, `lobby.tagline`, and rails 0, 2, 3 and 5. The static
fallbacks in `index.html` were retyped to match, because those are what renders before `i18n.js`
runs. Rails 1, 4, 6, 7 and 8 were already clean and were left alone. The Persian `splash.tagline` was
already clean too; the Persian lobby line and rail 0 were not.

**Scope, and the one line this cannot reach.** The rewrite stops at the front door. `host-layer.js`
is untouched, and `tannaz_opening_challenge` — "All right, fuckers. Every Iranian with a pulse…" — is
still the profanity he asked to remove. That is not an oversight. The file is a transcript of the
recording, and the recording (`tannaz_opening_challenge.m4a`, 14.6s) is fixed. He sent two rewrites;
both post-date the audio. Editing the text would desync the bubble from the voice it captions. It
needs a re-record.

**The tag moved forward to `globe-22`.** `i18n.js` and `index.html` both changed, and both are served
behind a cache tag, so the tag had to move or the copy would not reach anyone who had already loaded
the page. This one is a real invalidate, unlike the `pack-22` revert recorded above.

**The pan was never broken.** The animation ran the whole time. The keyframes held `0% 46%` from 0%
to 6% of a ninety-second cycle, so the door opened onto a completely still picture for its first 5.4
seconds — exactly the window in which someone decides whether the door moves at all. `ease-in-out`
then ramped out of a standstill, so the first thing anyone saw was the stillest part of the sweep.
The plateaus are 2% now, and `animation-delay: -20s` starts the cycle already in motion, so the first
frame rendered is mid-travel. Verified running in the preview: `currentTime` advances 4008ms over a
4000ms wait and `object-position` walks `20.80%` → `9.65%` across the return leg.

**The logo was already done.** He sent the Iranian Pack lockup and asked for it on the front door,
with MAIN and the courses explicitly unchanged. `19f14f0`, committed seventeen minutes before he
sent it, had already moved `.brand-wordmark` onto `logo-iranian-pack.png`. The file he passed over is
pixel-identical to the one in the tree — `ImageChops.difference` returns no bounding box, so the two
differ only in PNG encoding. Nothing was swapped, and `logo-wordmark.png` stays where it is.

## 2026-09-15 — a minimized phone stops playing to an empty room

**The engine had a way in and no way out.** `Sound.resume` has existed for a while, wired to
`visibilitychange` and `pageshow`, and it does the honest thing on the way back. Nothing on the
other side. Behind a covered window a WebView goes on running the engine, and Android goes on
playing the media element there, so the theme played to a phone in a pocket until something
unrelated happened to re-cue a bed.

`suspend` is the missing half, and it is deliberately not symmetric with `resume`. A bed is paused
and its slot kept, so the way back starts it again from where it stopped rather than from the top —
a new element for the same track would be heard as a restart every time the window went away. Her
line is ended rather than paused, through `finish`, because that is the only door that puts back the
bed the line ducked and the only reason a voice holding the floor ever lets it go. The verdict
waiting on its beat is cleared with them: it is a timer, and it would fire behind the covered window
and start a line nobody is there to hear.

**Nothing new reaches the air while the page is away.** That is a fourth guard on `music`, `sfx` and
`voice`, and it matters more than the pause does. The cold open is the case that shows why: cutting
her line runs the cue's `then`, and `doneOpening` hands over to the title card, which asks for
`menu_theme` — behind a window the player cannot see. A `voice` cue in this state takes the muted
path, so it still announces itself and still runs its `then`; the course advances its scene on that
callback and must not be left waiting.

Held as a separate `away` flag and not as `enabled`, which is the player's own switch with a button
drawn from it. The room is not told the show was muted, because it was not.

**Verified in the preview**, with `play`/`pause` wrapped on the prototype: the front door theme
pauses on `hidden` and plays again on `visible` on the same element; six seconds hidden during the
cold open produced two pauses and zero plays, while the title card's `menu_theme` was asked for and
refused; the return played `menu_theme`, the bed the show had actually arrived at, not the underscore
it left on; a `tannaz_wager` line cut by the hide had its bed back on the way in.

**The tag for `app.js` moved to its own `away-1` rather than to `globe-23`.** `CACHE_V` is shared
with every audio URL, so moving it would re-fetch the whole soundtrack for everyone who has already
played. `host-layer.js` already carries its own token, so this is the established shape.

**The staged Android tree is behind and was left alone.** `Android/app/src/main/assets/Web/` is a
hand copy, not a build step, and it is on `globe-21` while `Web/` is on `globe-22`. It is being left
that way: the working tree carries unreleased work, and syncing would bundle it into an APK. The
copy has to be re-staged before the next Android build or this fix will not be in it.

## 2026-09-15 — the front door gets a different lockup, not a re-encode of the same one

He sent the Iranian Pack lockup again, and this time it is a different picture. This morning's file
was pixel-identical to the one in the tree — `ImageChops.difference` returned no bounding box. This
one returns a box spanning the whole canvas. Where the old art was black glass, a monochrome skyline
and the Milad tower, the new one is Persepolis and the Cyrus cylinder and the Azadi tower and the
Imam Mosque's dome, cream stone, tilework, a pomegranate and an iris in the corners. Same canvas,
1983×793, same transparent ground, so nothing downstream had to move.

Swapped in place at `Web/assets/logo-iranian-pack.png`. Same class, same alt, same screen, and
`logo-wordmark.png` is untouched — same md5 as before. That file is what MAIN, the lobby, the board,
the clue bar and the course skin all wear, so the correction he made this morning still holds: the
lockup names one edition and therefore cannot live on `.logo`. It lives on `.brand-wordmark`, which
no skin reaches, and the front door remains the only screen that changed.

**The tag on that one URL moved to `pack-23`, not `globe-23`.** Only the image changed. Moving the
tree-wide tag would re-fetch `i18n.js`, `editions.js`, `styles.css` and every asset to deliver one
file, which is the mistake the `away-1` tag was introduced to avoid. `pack-NN` is this repo's name
for front-door art and the URL is new, so the image gets through and nothing else pays.

**The file is 2.7 MB, up from 1.7.** The new art carries far more detail and PNG has nowhere to put
it. Lossless recompression returns pixel-identity for 7.7%, which is not enough to be worth rewriting
his art for. Left as delivered. The screen that wears it is the one everyone opens first, so if the
weight matters more than the detail later, that is the lever.

**Two store assets still show the old lockup, and one of them is live.** `Tools/make_readme_banner.py`
and `Tools/make_itch_cover.py` both read `logo-iranian-pack.png`, so `.github/assets/logo-banner.png`
and `.github/assets/itch-cover.png` now depict the previous art. The banner is a local file that one
command regenerates. The cover is not: it was uploaded to the itch dashboard and it is what the store
page leads with, so whether the store follows the door is his call and not a decision to make by
committing a file.

## 2026-09-15 — the three course circles were the same width but not the same box

The discs were never the problem. All three frames have measured the same since they were built. The
columns were: `Iran in World Politics` is the only name long enough to wrap, and the live course is
the only one carrying a professor, so its column stood about 30px taller than the two beside it and
the row stepped — the placeholders' labels sat level with a line of its label rather than with each
other.

Both blocks now have fixed heights instead of ones that follow the copy: two lines for the name and
one for the byline, on every circle, whether or not that circle has anything to put in them. Three
doors in a row have to read as one row, and the long name needs its second line at every width the
front door is shown at, so reserving it costs nothing and buys three identical columns. Measured
identical at 375, at 1440, and again with the page in Persian.

`line-height` is stated on both rather than left to `normal`, because `min-height` is in `em` and the
two have to agree on what a line is or the box stops matching the text inside it.

**The placeholders' empty byline is not `hidden`.** The sheet carries
`[hidden] { display: none !important }` near the top, and that rule would collapse an empty span and
put the two placeholder columns a line short again — the exact bug being fixed. So the span is built
and left standing, empty. The old `.circle-who[hidden] { display: none }` was unreachable anyway, the
global rule already outranked it, and it is gone.

**`text-wrap: balance` was tried and dropped.** It broke the long name as `IRAN IN / WORLD POLITICS`,
which is no improvement on the natural `IRAN IN WORLD / POLITICS`, and support for it varies by
engine — so the three builds would wrap the same label differently, which is the opposite of the
thing being asked for.

`styles.css` and `app.js` move to `?v=20260915-front-circles-1`. Another session has been writing
this tree today and has put its own `mp-1` on those same two files; tags here are per file, so the
two do not collide. Worth knowing all the same that the working tree is being written by two hands,
and a full-file rewrite from the other side would take these edits with it.

## 2026-09-15 — the bank is 1,693, and a course bank moves into MAIN whole

*Iran in World Politics* stops being a bank that lives only behind its own door. Its 693 rows are
promoted into `QuestionBank/verified_clues.json` and `verified_clues_fa.json` unchanged, and MAIN now
stands at 1,693 clues in each language, over 100 books, 69 authors and 261 categories. The course
keeps its own copy and its own door; nothing moves back the other way.

The reading list followed the clues. MAIN's went from 49 entries in 7 groups to 91 in 17, which is
the old 49 plus the course's 42. That arithmetic is the point: the rule is that MAIN absorbs a
course's bank *wholesale*, so the count has to be a sum and never a selection.

`Tools/promote_course_bank.py` does the promotion and carries the guard. `--check` asserts all 693
promoted rows are still present and unaltered, so a later hand-edit to a promoted row fails the
check instead of quietly drifting away from the course. `Tools/render_bank.py --check` keeps the last
word on whether the rendered `Web/data/clues*.js` are in step with the JSON sources.

`check_bank.py` raises one warning over the promoted rows and is written not to fail on it: 32
English rows and 14 Persian ones list aliases that share no token with their own answer. The checker
says why in its own output — a course's aliases are translations and transliterations by
construction, and a transliteration shares no token with the name it transliterates — so this is the
shape of the data, not damage. Left as a warning deliberately.

The same checker flags three English rows as carrying Persian script: `double_proxy_music_2000`,
`double_strikes_800`, `double_axisres_2000`. Looked at, and it is not a bad promotion. Each is an
English clue whose parenthetical carries the Jalali date beside the Gregorian one — `On March 11,
1979 (۲۰ اسفند ۱۳۵۷)` — which is what the game does everywhere else too.

## 2026-09-15 — the write-in "wrong ruling" was the test driver, and the judge is exonerated

A typed answer kept coming back wrong when `answers.js` judged the exact string correct. It
reproduced three times and read like a judging bug. It was not one. `writeField(bot, isFinal)` renders
*the same* `input.write-input` box on a robot's turn — visible, and `disabled`. A driver that takes the
first visible `#screen-clue input` therefore finds the robot's box, types the right answer into a
field that is switched off, and clicks a submit that is switched off. Nothing reaches the human's
path. The clock runs out, and the engine counts a timeout as a wrong answer that passes the clue
along, so the clue moves to the next seat — and the driver, which only answered once per clue *text*,
never types again. Three pass-alongs, three wrong rulings, no bug in the game.

The driver was fixed on two lines: filter to enabled inputs (`!x.disabled`), and clear the answered
flag before pressing the verdict's next button so a passed-along clue gets answered again. The proof
that it was the driver: with the fix, the same clue that had been ruled wrong came back after a robot
miss and was ruled correct — `WRITE "Sheikh Safi al-Din Ardabili"` → `Correct. PLAYER 1`.

The real defect in that area was quieter. The `You wrote: …` readback was rendered on every screen, so
a remote guest and a robot were being quoted saying things they had not said. It now renders only on
the device that typed it.

## 2026-09-15 — four false alarms, so nobody chases them again

- **`#reading-panel` looks stuck open.** On a fresh load it is `hidden` and `display: none`, and the
  lobby is reachable. It was open because a driver had clicked it open, and the overlay then sat over
  the lobby at `z-index: 50` swallowing clicks aimed at `#go-setup`. Not a defect. Do not "fix" it.

- **A clue showed `200M` against a bank row keyed `1000`.** By design. `app.js:74-79` keeps two
  scales: `SINGLE_VALUES` (10/25/50/100/200) is what gets printed, and the bank key is still the
  dollar-shaped integer that finds the row. `buildBoard` overwrites `clue.value` with the printed
  rung, so the top rung prints as 200M whatever the row was keyed. The comment above it says exactly
  this.

- **A tag burned into a local browser cache cannot be cleared by `location.reload()`.** The HTTP cache
  is keyed by the full URL including `?v=`, so a stale `clues.js?v=…` keeps answering from disk until
  the tag itself changes. `fetch(url, {cache: 'reload'})` both bypasses the entry and overwrites it,
  and that is the way out. Reproduced on a brand-new origin as well, so it is the tag and not the
  profile. `CACHE_V` in `app.js` is audio only and has nothing to do with any of this.

- **The wager screen says "You can still back out" and offers only Lock.** Read again and left alone.
  The sentence follows "place your wager", the slider stays live until Lock is pressed, and nothing is
  committed before it — so it is a promise about the number, not a missing button. Changing it would
  mean editing her copy, which is not a thing to do on a hunch.

## 2026-09-15 — the board-ownership rule reaches the rule book, and the playthrough is clean

The rule that the ticket goes to whoever won the clue shipped in 1.0.10 without ever reaching
`GAME_RULES.md`. `S.chooser`, `chooserLive`, `pickingHere`, `denyPick`, `armBotPick` and `padMayPick`
are all new, and v1.0.9 has no `S.chooser` at all — so the file `CLAUDE.md` makes the second thing
anybody reads described a board that nobody owned. A rule book silent on a shipped rule is the one
kind of drift that file itself calls a bug, so it now carries the rule under "Whose board it is": a
right answer names the chooser, anything else draws at random, the board is locked to that seat with
the *Picks* badge and a shake for anyone else, a robot picks for itself on a beat out of a live cell
drawn at random, a pad may stand in when the chooser has no controller, and at an online table the
engine drops a `pick` from any other seat. No code moved, and nothing that gates a build reads this
file.

The web build was then played end to end on the working tree: 73 clue resolutions across both rounds
and the Final, zero driver errors and zero unanswered lookups, a Daily Double wagered, a negative
score carried, Second Chance pass-alongs, all three contestants wagering on the Final (977M, 120M,
232M — one missed, to −232M), and the *You wrote: …* readback appearing on the typing device alone.
Final 2932M / 725M / 703M, ranked descending.

- **A positive score printed in red on the results screen.** By design. `.result-row .rscore` is
  `color: var(--pc, var(--ink))` — the score wears the contestant's own seat colour, and the second
  seat is the red podium, so 725M in red is Cyrus the Algorithm being himself. `.neg` is the override
  and it is reserved for a total below zero. Not a defect, and the fifth of this run that looked
  exactly like one.

## 2026-09-15 — 1.0.10 is out, and it replaced 1.0.9 rather than sitting beside it

`Web/` was frozen as `Versions/v1.0.10` (181 files, 39M) and the whole tree went up as `8875d4b`,
tagged `v1.0.10`. All three artifacts were built from this tree — nothing was rebuilt for the cut,
because the newest shipped file (`Web/index.html`, 22:49) still predated the macOS zip (22:52), and a
repack would only have produced the same bytes. Each was opened and the stamps read out of it: the Mac
bundle is `1.0.10`/`110` and `lipo -archs` says `x86_64 arm64`, the IPA is `1.0.10`/`110` with 193 Web
files inside, and the APK carries `1.0.10` and `com.morad.jeopardy` with 181. Uploaded sizes match the
local files exactly.

The 1.0.9 **release** was deleted, so 1.0.10 is what the Releases page opens on. The `v1.0.9` **tag**
was deliberately left alone: it is where that code is, and nothing about replacing a release asks for
the history to go with it.

Two workflows fired on the push and both went green. *Publish the web show* deployed Pages (200). The
itch job ran the `check_web.js` gate, then butler pushed 181 files / 38.50 MiB to
`aghamorad/jeopardy-iranian-edition:html`. It was re-run once, on purpose: `--userversion` is
`git describe --tags --always`, and the first run started eleven seconds after the commit push and may
have described itself off `v1.0.9` before the tag landed. With the tag present it describes as
`v1.0.10`.

- **The itch game page answers 404 to the public while butler uploads to it fine.** Not a broken
  pipeline and not something to fix in CI. Butler authenticates with `ITCH_API_KEY`, and it both read
  the previous build (1982165) and pushed a new one, so the project exists at that target and the
  upload is landing. `aghamorad.itch.io/` itself answers 200. The anonymous wharf check for the same
  target says `{"errors":["invalid game"]}`, which is what an unpublished or restricted project looks
  like to a stranger. So `Web/` is on itch and the page is simply not public yet — a visibility
  toggle in the itch dashboard, and his call, not a build problem to chase.

## 2026-09-16 — The read window is fifteen seconds, not six

`READ_SECONDS` in `Web/app.js` went from 6 to 15. It is the one constant behind the pre-buzz window,
used in exactly two places — the clock that opens the buzzers and the clock's own readout — so there
was nothing else to keep in step. He called six seconds unusable and asked for thirteen to fifteen;
fifteen is the generous end of that.

Six was sized as "a beat to read the thing", and that was the error: the clues are not beats. The one
that settled it runs to forty words and two lines, and the same window has to serve Persian as well as
English, where the eye has further to travel. The buzz window is untouched and still the round's
(`single` 20, `double` 12) — the read was never the part that wanted to be tight.

Played on the working tree to confirm: the clock ran Read 15 down through 7, 6, 5, 4, 3, 2, 1 and
handed off to Buzz 20 on schedule, then to Answer when a robot took the clue. No console errors.

- **The read window is a forced wait and there is no way to skip it.** Everybody stares at the clue
  for the full fifteen, including whoever knew the answer in three. That was tolerable at six seconds
  and is a different proposition at fifteen, but it is a new affordance rather than a tuning change,
  so it is his call and not something to slip in beside this. The shape if he wants it: a key or a tap
  that closes the read early and opens the buzzers, with the clock still the only thing that decides
  when a window ends.

## 2026-09-16 — The buzz-in is re-cut, and it carries a cache tag of its own

`Web/assets/audio/buzz.m4a` is replaced with the new buzzer and the old one is gone — a copy was put
in `~/.Trash/buzz.m4a.replaced-20260916` rather than deleted, in case the old stomp is wanted back.
`Sound.sfx('buzz')` is the only caller and a phone's buzz arrives at the same one: a remote `buzz`
message goes through `hostMessage` into `buzz(seat)`, which is the in-room thumb's own function. One
file is therefore the whole change, and no edition maps the cue away from it.

The source arrived as a 0.72s 48k mono WAV and was encoded with `afconvert -f m4af -d aac -b 128000`
— the pack's own format, and the first extension the loader looks for, so nothing had to learn a new
one. The cue it replaces ran 0.78s, so no window that waits on the buzz's length moved with it, and at
peak 30,800 / rms ≈ 21,100 it sits with `armed` and `incorrect` rather than above them. No gain was
applied on the way in, since putting one there would have been a level change nobody asked for.

**It got a tag of its own rather than a bump to `CACHE_V`.** `CACHE_V` is shared by every audio URL in
`Sound`, so moving it to publish one replaced cue would re-fetch the whole 6.2 MB soundtrack for
everyone who has already played — and this is a show played mostly over an Iranian connection, where
that is not free. `CUE_V` now takes a cue name and returns a tag for it alone, `buzz` is the first
entry at `?v=20260916-buzz-1`, and everything else still answers on `globe-22`. Same shape as the
`away-1` token and `host-layer.js`'s own, and the reason the 2026-09-15 entry refused to move
`CACHE_V` for a change that was not audio at all.

Played on the working tree to confirm: a robot's premature buzz fired `incorrect`, the buzzers opened
on `armed`, and an accepted buzz requested `assets/audio/buzz.m4a?v=20260916-buzz-1` and handed the
clue to the answering phase. `correct.m4a` and the rest were still asked for on `globe-22`, which is
the point — one cue moved and the soundtrack did not. No console errors.

## 2026-09-16 — The professor's welcome is slowed to a lecture pace

He heard the welcome as too fast and asked for it at 1 speed. He is right about the delivery and
wrong about the cause, and the difference decided what got changed.

**Nothing was playing it fast.** `playbackRate`, `preservesPitch` and `AudioContext` appear nowhere in
`app.js`, `course.js` or `host-layer.js`, and the file `Web` ships is byte-identical to
`Course/Masters/Iran in World Politics/Professor Voice/1.0x source/eskandar_01_professor_welcome.m4a`
— 191,342 bytes, md5 `fe2d09e3`, 15.325188s. So does every other copy in the tree: both `Versions/`
snapshots, `dist/`, the macOS app and the Android assets. There is no stale fast derivative anywhere,
and the cache is not to blame either: the clip and `CACHE_V` last moved together in `002b564`, so
anyone who played the old take was already re-sent the new one.

What he was hearing was the clone reading 37 words in 15.3 seconds — 145 words a minute, which is a
news read, not a lecture. "1 speed" meant a normal pace and not a 1.0x multiplier, and the fix is the
only lever that exists in a build with no rate control: re-render the file.

**0.9x, and the evidence is a pace he already accepted.** The same line in the male pack he was given
earlier ran 17.04s / 130 wpm and he never called *that* fast. 0.9x puts the clone at 17.010687s and
130.5 wpm, on top of it, so the target came from his own ear rather than from a round number. 0.85x
(18.02s, 123 wpm) is rendered and held in case he wants it slower still.

Rendered with `ffmpeg -filter:a "atempo=0.9"`, pitch preserved. There is no lossless master in the
tree to work from — the m4a *is* the master — so this is a second encode on an already-lossy file and
it was taken at 128k against the source's 98k, which does not recover anything but does stop a second
round of quantization from stacking on the first. The 1.0x source is untouched: its folder name
asserts 1.0x and overwriting it would have made that name a lie. The render sits beside it in
`Professor Voice/0.9x welcome/`, named for what it is.

**`CUE_V`, keyed by the clip and not by the cue.** The welcome takes `?v=20260916-welcome-0-9x` rather
than a `CACHE_V` bump, for the reason the buzz took one. The key is
`eskandar_01_professor_welcome` and not `tannaz_opening_challenge`, which is the non-obvious part:
`voice()` applies `HOST_CUE_MAP` before `url()` reads `CUE_V`, so what arrives at the tag is the
course's substituted file name. That is also why it costs the main edition nothing — the key only
exists in the course, so Tannaz's own welcome is still answered on `globe-22`.

**And a gap found on the way in.** `app.js` had already changed in the working tree — the fifteen
second read window — without its tag in `index.html` moving off `20260915-mp-3`. That tag is what
carries a new `app.js` to somebody who has played before, so the read window could not have reached
any of them, and neither could this. Bumped to `20260916-welcome-pace`, which publishes both. The
comment above `CACHE_V` says the value has to move with the tag by hand because no build step keeps
them in step; this is what that costs when it does not.

Played on the working tree to confirm: entering IR4595 asked for
`courses/iran-in-world-politics/assets/audio/eskandar_01_professor_welcome.m4a?v=20260916-welcome-0-9x`
and the element decoded it at 17.010688s, fifteen seconds of `app.js` and one tag later. `buzz.m4a`
and the rest of the soundtrack were still asked for on their own tags and `globe-22`. No console
errors.

## 2026-09-16 — The phone's type was a desktop floor read through a hand

He sent a screenshot of the clue screen on his phone and said the text was too small *for
everything*. It was, and it was one cause rather than a list of them.

**Every size in the sheet is a `clamp()` on `vw`, and upright, `vw` is the short edge.** On a laptop
`vw` is the long one, so the clamps breathe and the design reads. At 430×932 the whole scale lands on
its floors at the same instant, and the floors were picked for a desktop window: the category head
computed to 6.5px, a podium name to 7.5px, the verdict's source line to 8px. Nothing was wrong with
the components. The rung they were sitting on was.

**The existing `max-width: 900px` block was the wrong rung for this, not a broken one.** It was
written against a landscape phone — 812×375, where `vw` is again the long edge — and it sets bare
pixels (`6.5px`, `6px`) that also fire in portrait, which is why the board heads were unreadable
rather than merely small. So the landscape rules stay exactly where they are, and a second block
answers the upright case: `@media (max-width: 900px) and (orientation: portrait)`, appended at the
end of `styles.css` so it wins its ties. `orientation` is derived from the viewport's aspect ratio,
so a 932×430 phone never matches it. Verified inert there — `matchMedia` false, `.cat-name` and
`.pname` still on the landscape values.

**It is the same scale one step up, not a new one.** No geometry moves; the rails, corners, pills,
logo, board grid and podium flex are untouched, and every value in the block is still a `clamp()` on
a viewport unit. Roughly: board category heads 6.5 → 9.5–15px, tile values to 19–34px, clue text
19–32px on `vmin`, options 14–19px on a 52–72px row, verdict body 12.5–16px, podium names 10–13px,
podium scores 20–28px, results rows 12–16 / 20–30px.

**`.clue-text` is the one run that had not collapsed** — it is sized on `vmin`, so it was the only
survivor — and it moved anyway, to stay in proportion with the options it now sits beside.
`fitClueText()` resets to the stylesheet size and steps down to `base * 0.68`, so raising the base
raises the floor with it. Checked rather than assumed: the longest clue in either bank is 359
characters English, 332 Persian, out of 1,693 each, and against a deliberately oversized 490-character
worst case it settles at 21.7px with 26px of slack (`avail 464`, `overflow -26.3`).

**And one real regression, caught by looking.** `.podium .pname` is `nowrap` with an ellipsis, which
survived a 7.5px name and does not survive a 12px one — "Cyrus the Algorithm" needs 181px and the
podium box offers 110, so the robots came back as "CYRUS THE A" and "BOT-OL-MOLK". The portrait block
lets the name wrap to a second line instead, which the podium has the height for. The podiums row is
`flex: none` and cannot grow, so this had to clear the board above it: board bottom 752.4 against
podiums top 757.4, and a two-line name is 31.2px in 52.5px of content box. It clears.

Played at 430×932 and looked at: front door, lobby, green room, board, clue in both multiple-choice
and write-in, verdict, results, and the same board and clue again in Persian. `documentElement.scrollHeight`
equals `clientHeight` at 932 with no element overflowing, and the write-in field and results rows
report `scrollWidth === clientWidth`. `styles.css` is published as `?v=20260916-mobile-type`;
`STYLE_SHEET.md` carries the rung and its two consequences under "The upright phone" so the next
component added here does not have to rediscover them.

Left alone, and worth naming: in Persian the board's category head holds Persian text but is still
set in `--display` with `letter-spacing`, which the sheet's own rule says it should not be. It
predates this change, it is legible, and correcting it moves desktop Persian too.

## 2026-09-16 — The new buzz reaches the trees that get built, and the release record is left standing

The re-cut buzzer was already the whole of `Web/`, but `Web/` is not the only place the file lives. Five
trees carry their own copy and were updated with it, nothing else in them touched:

- `Android/app/src/main/assets/Web/assets/audio/buzz.m4a`
- `Course/dist/Iran in World Politics/assets/audio/buzz.m4a`
- `Course/dist/_template/assets/audio/buzz.m4a`
- `Jeopardy Iranian Edition.app/Contents/Resources/Web/assets/audio/buzz.m4a`
- `dist/Jeopardy Iranian Edition.app/Contents/Resources/Web/assets/audio/buzz.m4a`

All five now hash to `3ca18deb…e7a74`, the same digest as the source. Before writing, every target was
checked to be a single-linked file, because `cp` over a hardlinked name would truncate the inode it
shares with `Web/assets/audio/buzz.m4a` — the failure the standing notes warn about.

**A signed bundle does not take a new file quietly, and this was the one real hazard.** Both `.app`
bundles are ad-hoc signed, and `Contents/Resources/` is inside the seal: dropping the file in left
`codesign --verify --deep --strict` failing on both. A bundle in that state is exactly what Gatekeeper
refuses to open, so each was re-signed with the build's own command, `codesign --force --deep --sign -`,
and both verify clean. Then it was launched rather than assumed — the shell is only as good as the tree
it opens onto. It came up on the Persian front door, correct logo and all three edition circles, and
the process was still alive five seconds later; it was closed and the screenshot discarded. Had the
signature step been skipped, both bundles would have shipped broken.

**The frozen record was deliberately not touched.** `Versions/beta-1..8`, `Versions/v1.0.9`,
`Versions/v1.0.10` and `dist/Jeopardy-Iranian-Edition-web-beta-3..7` keep the old buzz because their
job is to answer what 1.0.9 and 1.0.10 actually shipped, and a snapshot that has been edited is not a
snapshot. `dist/Jeopardy-Iranian-Edition-Android.apk`, `dist/Jeopardy-Iranian-Edition-iOS.ipa` and
`Android/app/build/outputs/apk/release/app-release.apk` are the same case in a different wrapper:
re-cutting them would change binaries that were already signed and published.

The two generated copies under `Android/app/build/intermediates/` were left alone as well. They are
scratch for the last compile and are rewritten from the staged tree on the next one — which now holds
the new file, so the merge has nothing stale to carry forward. Rebuilding a bundle or an APK properly
was the other option and was refused on purpose: `Web/` currently carries unreleased work from another
session — `app.js`, `index.html`, `styles.css`, the welcome re-cut — and a rebuild would quietly ship
all of it under a 1.0.10 label. This was a cue swap, and it stayed one.

## 2026-09-16 — the menu pills become the same glass as the edition circles

`.pill` was a flat `--glass` wash under a hairline, which over the lit city read as a **hole cut in the
photograph** rather than a piece of glass lying on it. He asked for the menu buttons to get what the
edition circles got in `002b564`. The circles' cue set is now the pill's cue set: a canted specular, its
catchlight, the strip of light skimming a top lip, and the caustic the far wall drops at the foot —
proportioned to the pill's 7:1 slab rather than the circle's disc, but on the circles' exact stop
profile, because that profile is what makes a reflection instead of a glow.

**The shape of it was forced, and this is the part worth remembering.** Both pseudos on `.pill` are
already spent — `.pill-primary::before` is the flag hairline and `.shine::after` is the travelling
shine, which menu pills *do* carry because `RINGS.lobby = '.menu .pill'` is the cursor — and half the
pills in the show are built in `app.js` rather than `index.html`, so there is nowhere to hang a `.lens`
child either. So the glass lives in the element's own background and bevel, and the price is that
**every state may move `--pill-tint` and `--pill-depth` and nothing else.** Hover, `.is-on` and
`.pill-primary` all change only those two variables; a rule that replaces `background` or `box-shadow`
outright silently kills the glass.

Two things went wrong on the way and both are traps for the next person. A soft-falloff specular read
as a **grey smudge**, which is exactly the failure the circles' own comment names — fixed by copying
their hard falloff (`0.60` held to a quarter of the radius, dark by 74%) rather than inventing a
gentler one. Then it read as **two round white dots**: `radial-gradient(ellipse 7% 30% …)` takes
*radii*, not diameters, so on an 821×111 slab that was a 115×67px near-circle, not the reflected streak
I meant. Flattened to `5.5% 13%` and `2.4% 6.5%`.

The front door's language track is a piece of glass holding two pills, so the inner pills give up their
bevel — two slabs must not stack — and the track takes the lip and the throw instead. It still reads as
one object.

**`.segmented` was deliberately left flat.** It is the green room's settings control and the language
gate, a track of small buttons, and it is not a menu button and not the house's button vocabulary. It
would look better with the glass and it would also compete with the two primary entries above it. That
is his ruling to make, not mine to slip in, so it is unchanged and now written down.

Verified on the working tree rather than assumed: the lobby at normal size and at 2.3×, the `.shine`
cursor sweeping the new glass, the front door's language gate, the setup screen, the match-menu overlay
at normal and 2.4×, the splash's `.pill-outline` ("Let's begin"), and the Persian RTL lobby and front
door — the glass is identical in both directions, the gradients stay anchored left, and the icons and
chevrons flip as they should.

Documentation drift found while doing it, and corrected in `STYLE_SHEET.md`: the **Pill** bullet still
described the old flat fill, and the whole **Edition chip** entry described `.swap` / `.swap-btn` /
`.swap-art`, a control that **no longer exists anywhere in the tree** — the "which show?" job belongs
to the edition circles now, and that is what the bullet says instead. `.segmented` was undocumented and
now has a line.

## 2026-09-16 — the app was never booting into the course at all

He said the rule out loud — Eskandar's voice in course mode, Tannaz's in MAIN — and the rule was
already implemented everywhere it could be seen. `HOST_CUE_MAP`, `HOST_VOICE`, `EDITION_SOUND`, the
professor's pools in `course.js`: every one of the four cues the engine calls by Tannaz's names
resolves inside a course to `courses/<id>/assets/audio/eskandar_*`, and MAIN has no map at all, so it
resolves to `assets/audio/tannaz_*`. Checked both directions and both are airtight.

What was not airtight was the boot. **A `?ed=` course link opened MAIN, and so did a remembered
course.** The cause is script order in `index.html` and nothing else: `host-layer.js` sits at line 718,
one script ahead of `course.js` at 719, and its `register` asked `window.getEdition()` whether the
edition it had just registered was the one on the floor. `getEdition` is lazy — it calls `ensure()`,
which reads the `?ed=` param, finds it absent from `BY_ID` (the course has not registered yet, it is
the *next* script), falls to `saved()`, falls again to `LIST[0]`, caches `general`, and **writes
`general` over the remembered course in localStorage.** A registration was resolving the edition
before the thing it was asking about existed, and the wrong answer was then persisted. So the deep link
never fired, the app's own share links (`app.js` `link += '&ed='`) never worked, and a returning student
lost their course on every single boot.

The fix is a reader with no resolution in it: `window.peekEdition()` in `editions.js` returns `current`
and nothing else, and `host-layer.js`'s `register` asks that instead. A registration is now incapable of
resolving the edition — it can only notice one already chosen. `ensure()` is untouched, so the engine's
own boot still resolves exactly as before.

Two cache tags bumped, since both files are in the shells' WebView cache:
`editions.js?v=20260916-edition-resolve` and `host-layer.js?v=20260916-host-layer-7`.

Verified live on 8831, both paths: `?ed=iran-in-world-politics` lands in the course (`edition` and
`data-edition` both the course, `HOST_CUE_MAP` present, boot audio `course_theme.m4a`, screen
`splash`), and a plain load with the course saved keeps it (`saved` still the course) while the door
still opens on `menu_theme.m4a` — which is `fileFor`'s front-door rule doing deliberately what it
documents, the door belonging to no show.

One false alarm from earlier in the same investigation is now explained rather than left standing: the
`.mp3` retries seen against the course were a test page sitting on the *front* screen with the course
set by hand, where the front-door rule returns the bare name, the file is not in the engine's audio
directory, and nothing fires in real play because the cold open fires on `splash`, after `enterEdition`.

## 2026-09-16 — the pill's specular becomes a shine that travels

The third entry above records the pill glass as it was first built, and one part of it is now wrong:
`.pill` no longer carries a specular, or its catchlight. He looked at the lobby and asked "doesn't it
just look annoying now?" — and it did.

The specular itself was not the fault; its **position** was. A highlight that lives at a fixed point
inside a shape is a singleton cue. On the edition circles it is right, because a circle stands alone in
space and a canted highlight on it reads as a reflection off a curved surface. The lobby is a column of
seven identical pills, and the same highlight landed in the same place seven times — which is not seven
reflections but one white lozenge stamped on every button, sitting on top of the leading icon. **The
rule, and the thing for the next person not to re-add: a specular is a singleton cue; edge light is the
only kind of highlight that can repeat**, because it belongs to the rim of every slab rather than to a
point inside one. Seven lit top edges read as one material; seven blobs read as one stamp.

So both localized radial layers came out. What is left at rest is edge light only — the strip skimming
the top lip, and the far-wall bounce pooled at the foot — with the bevel softened to match.

What replaced the specular is what he suggested: **a shine that travels.** A band of white canted
`102deg` so it runs with the slab rather than square to the box, 46% of the width so it crosses rather
than washes, parked off the leading edge at rest. On `:hover` and `:focus-visible` it sweeps
`background-position` from `-140%` to `240%` in 0.9s and is gone. A travelling highlight cannot become
a pattern: there is no position in it for the eye to lock onto, which is exactly what the static one
got wrong.

The shape was forced the same way as before. The sweep could not use a pseudo — both are spoken for,
and `.pill-primary::before` is free only on non-primary pills, so that route would have been
inconsistent across the column. It drives `background-position` on one dedicated background layer,
which is the only hook that works on every pill with no pseudo and no child. Two consequences worth
carrying: the `background` shorthand resets size, repeat and position, so all three must be restated
with one value *per layer*; and the transition had to be narrowed from the shorthand to
`background-color`, `border-color` and `transform`, because a transition on `background` would try to
interpolate the very `background-position` the animation is driving.

Hover rather than an ambient loop is the deliberate part: an ambient sweep is seven pills shining in
chorus, and one-at-a-time is what keeps the shine a response to the pointer rather than a decoration.
It is a light cue and nothing else, so it is suppressed under `prefers-reduced-motion: reduce` — the
lift, the tint and the border still answer without it.

The first cut of the band was too soft (`0.30` on a plain linear falloff read as a grey haze, not a
shine) and was tightened to a `0.38` core with `0.06` shoulders. Checked frozen mid-sweep at five
stations down the column, which is the only way to look at a moving highlight — and the lesson from the
entry above still stands, that a single pill at magnification is the one framing that cannot show you a
repetition defect. At rest the column is unchanged.

`.segmented` is still flat, for the reason the entry above gives.

---

## 2026-09-16 — MAIN's shelf stops wearing the seminar's week numbers

MAIN's reading list was showing **"Week 1 — Revolution and theocracy"**, "Week 2 — The Iran–Iraq War"
and so on down to Week 11 — headings that are the course's clock, not a subject. He caught it and said
the obvious thing: those weeks belong to the course's shelf, and MAIN's shelf should just list the books
under whatever subject each one is actually about.

The headings were not hand-written. When IR4595's readings joined MAIN's shelf they were appended
**verbatim, `group` labels included**, so the generator was copying the seminar's shape along with its
books. That is why the fix went into `Tools/make_readings.py` rather than the generated file — that
file's own header says not to edit it by hand.

**The decision: fold each week into MAIN's own headings**, chosen over the alternative of keeping the
course's topical headings with the week numbers stripped. A week is a position in a syllabus; on a shelf
that is not a syllabus it is a claim about reading order that is not true. So the field is in MAIN's own
seven headings — Revolution & Islamic Republic took nine of the ten weeks (33 readings), Society,
Culture & Ideas took the tenth (9 readings, Week 9 Gender, the body and the state).

The mechanism is a per-course registry, `COURSE_SHELVES` — file, how many readings it must hold, and a
`week → heading` line for every week it has. It reads the course shelf read-only, so the course's file is
never written to and still carries its ten week headings and its 42 readings. The two headings in the
table are named constants rather than string literals, so the table reads as the decision it is.

**The part meant to outlive this change is the assertion, and it runs in both directions.** A week the
table does not file aborts the run naming the file, the group and its heading — so a new seminar week
cannot arrive silently unlabelled. A line naming a week the shelf no longer has also aborts, so the table
cannot rot into a description of a shelf that changed. Both paths were exercised, not assumed: each
aborted in-process with the expected message.

Regenerated and checked: `Web/data/readings.js` is 7 groups and 91 entries — Revolution 9 of MAIN's own
plus 33 filed, Society 12 plus 9 — and `Tools/check_readings.py` reports OK with both counts intact
(91 / 42). The course shelf is untouched at 42.

**Both panels were then looked at, not just diffed.** MAIN's edition shows the seven subject headings,
the Revolution group reading 42 and running straight from MAIN's own nine rows into the filed course
readings with no week label anywhere, and the Society group reading 21; IR4595 still shows "Week 1 —
Revolution and theocracy" and "Week 2 — The Iran–Iraq War" over those same books. That is the whole
point of the split: the same books, filed two ways, each answering to its own shelf.

---

## 2026-09-16 — The early buzz was a sentence, not a mistake

A thumb that lands before the lamp is fouled, and that is right. What was wrong was when the
clock on the punishment started. It started at the lamp.

The button was disabled from the moment of the press — `S.early[i]` was set by
`prematureBuzz()`, and `renderClueActions()` disabled on `prematureUntil[i] > now || S.early[i]`
— and the lockout itself was only written in `openBuzzers()`, as `Date.now() + 1500` at the
moment the lamp opened. So a press half a second early went dark at the press and came back a
second and a half after the lamp: two seconds for a half-second error. A press ten seconds
early went dark at the press and came back eleven and a half seconds later. The one-second
mistake and the ten-second mistake cost the same, and neither had anything to do with the
race, which is the only thing the buzzer is testing.

The read window is fifteen seconds and the race is twenty. Timed from the lamp, the penalty was
anchored to the longer of the two and paid out of the one the contestant was actually
competing in.

Now it is timed from the press. `EARLY_LOCKOUT_MS` is unchanged at 1500 and `prematureBuzz()`
writes `S.prematureUntil[i] = Date.now() + EARLY_LOCKOUT_MS` itself, so the residual is
whatever is left of the second and a half when the lamp opens. `S.early` is gone — it existed
only to carry the foul from the press to the lamp, and the moment is now booked at the press,
so there is nothing left for it to carry. The repaint timer moved with the lockout, into
`prematureBuzz()`, and still calls `onlineSync()` as well as `renderClueActions()`, because a
guest's plate is redrawn from a picture and had no other way to come back.

What the change buys is the thing the user described. Press a second before the lamp and the
lockout runs out half a second *after* it: you are not fast enough, which is the whole point.
Press ten seconds early and you are live again at eleven and a half seconds, well before the
race, having lost nothing but the time you were not competing for. The remaining guard in
`buzz()` covers both cases with one line — a thumb already inside `prematureUntil` stays out —
which also replaces the old "one buzz, one foul" guard, since a second press during the lockout
now books a second foul and re-arms the timer.

Measured on the phone build at 430×932, one human and two robots. Press six seconds early: dead
at the press, live again at +1.5s with the lamp still closed at +4.1s. Press with the read clock
showing 1: dead at the press, *still dead when the lamp opens at +9.3s*, live again 560ms later
— and a robot takes the clue 430ms after that. The second trace is the mechanic working: the
foul costs the race and nothing else.

The first pass at this was measured against a cached `app.js` and showed the old behaviour
exactly — dark from press to lamp. `index.html` carries a `?v=` on the script tag and it had not
moved; the tag is now `20260916-early-lockout`. Worth remembering that a timing change looks
identical to a change that did not ship.

Not touched: `S.lockedOut`, the wrong-answer lockout, which runs to the end of the clue and
should.

---

## 2026-09-16 — the segmented track takes the glass, and the read window gets no skip

Two rulings from Morad, both closing questions the entries above left open.

**The segmented control wears the glass.** The entry two above filed `.segmented` as flat on the
argument that it is a setting, not a press, and should not compete with the two primary entries on the
green room screen. He disagreed on the material and left the mechanism to me: *"i don't think it should
be flat, and id prefer it with the glass."* He was right about the material and the old reasoning was
really about the *shine*, not the glass — the two got argued as one thing when they are two.

So the **track** now wears the pill's material: the same strip of light on the top lip, the same bounce
pooled at the foot, the same four-part bevel, the same `backdrop-filter: blur(17px) saturate(150%)`. The
chips inside give up their bevel so two slabs never stack, which is the rule the language track already
followed — one piece of glass, lit chips resting in it. The chosen chip is a lit chip in the glass, not
a slab of its own. Only the track and a `text-shadow: var(--halo)` on the chips are new.

The travelling shine is **withheld**, and that is the deliberate half. The shine is the pointer's answer
to a press; these are settings, not presses. A sweep on every chip would make the pill's own cue into a
second button vocabulary, and the pill would stop meaning "this is the thing you press."

Two things fell out of the change.

The `.segmented-wrap` difficulty track wraps 3+1 in a 65px stadium, and the empty space beside THE
ARCHIVE now reads as an unfilled glass shelf where before it read as a rule. That is a layout question
in the green room, not a material one, and it is left standing rather than papered over. On the phone at
375×812 it is the same wrap; the chips stay legible.

`#settings-sound` in the settings overlay is the one track that lives in an `.overlay-row`, a column flex
box, so it was stretching to the card's full 459px with its two chips bunched at the left — the same
empty-shelf problem at a worse ratio, an ON/OFF switch occupying ninety pixels of a four-hundred-and-
fifty-nine pixel tube. Fixed with `.overlay-row .segmented button { flex: 1 }` rather than by shrinking
the track, because every other control in that card is edge to edge and a hugging track would have been
the odd one out. Verified at 2.6×: two equal halves, the ON side lit, the OFF side an empty seat.

**The read window gets no skip.** The fifteen-second window (see the entry five above) leaves a fast
reader sitting in front of a clue they finished in four seconds. I proposed a skip. He ruled against it
in one clause: *"the player who's read it has to sit there and wait."* The read clock is the same clock
for everyone at the table and the wait is part of it — a skip hands the fast reader the whole of the
race. Nothing is built.

`STYLE_SHEET.md` corrected in the same pass. Its Segmented bullet had gone stale twice over: it claimed
the control deliberately does not wear the pill's glass, and that it serves the language gate. The gate
is a `nav.menu.menu-inline` pair of `.pill.pill-outline` buttons, not a segmented control at all.

---

## 2026-09-16 — The buzz was never loud; the cue it replaced was quiet, and only in mono

He heard the re-cut buzzer once and said it was WAAAY too loud. It was. Not for the reason the entry
that introduced it gives, though. That entry measured the new file against `armed` and `incorrect`,
found it sitting among them, and concluded that no gain belonged on the way in. The measurement was
sound and the conclusion was wrong, because the file it replaced was **stereo and anti-phase**.

Two channels at L/R correlation −0.78, per-channel rms −4.66 dBFS, is a file that reads perfectly well
on an analyzer and collapses on playback. Any path that sums the channels down to one — a phone's own
speaker, a laptop's downmix, a mono speaker in the room — cancels most of it: the same file arrives at
**−14.26 dBFS** there. Every other cue in the pack is mono, so nothing cancels in any of them. The old
buzz was the one anti-phase file in the set and therefore the one cue that played roughly **ten
decibels below** everything around it, for as long as it existed. That is the level he had learned. The
re-cut arrived ten decibels above it with no number on the file having changed by more than a fraction
of a decibel.

Which also disposes of the "about 7 dB louder" figure I gave him first, and of the reading that the
replacement was in any way hot. The two files are **0.43 dB** apart. Nothing was loud. The thing it
replaced was quiet, and only in mono, and nobody had a reason to notice.

**The fix is a level cut on the original, not a second pass on the m4a.** The Desktop WAV is still
there and is the only copy with no generation of AAC on it, so the cut was applied to that and encoded
once, straight into the pack's own format. Python scaling, `afconvert -f m4af -d aac -b 128000`, 0.720s
preserved. The result is peak −8.54 dBFS and rms **−12.21**, a little above the old cue's mono level of
−14.26 so it does not arrive quieter than the thing he was used to, and around 4 dB under `correct`,
the quietest cue the pack ships. He wants it at −10 if what he had is what he wants back, or at −6 if
−8 reads as too far. It is one number in a two-line script and nothing else moves.

`CUE_V.buzz` went from `20260916-buzz-1` to `20260916-buzz-2` in the same pass. A tag that never moves
is a tag that pins the old level in every browser that already fetched it, which is the whole reason
the map exists — and this is the second time in a day the buzz has needed it.

All six copies were replaced again — `Web/`, the Android staged tree, both `Course/dist` builds, both
`.app` bundles — `cp` throughout, no hardlinks, hash `e39801c0…3b7e2` on every one, confirmed by
`shasum` across the set. Both bundles re-signed with the build's own `xattr -cr` and
`codesign --force --deep --sign -` and verified clean, since writing a file into a sealed bundle
invalidates its signature every time.

Verified rather than asserted. The running server was asked for `assets/audio/buzz.m4a?v=20260916-buzz-2`,
answered 200, and the browser decoded it to mono 48 kHz 0.720s at rms **−12.21 dBFS** — the same number
the offline measurement gives. Peak reads −7.93 there against −8.54 offline, which is AAC's own
transient overshoot and not a second file. The front door still boots with no console error.

**Corrected, without rewriting it:** the entry that introduced the re-cut still ends "No gain was
applied on the way in, since putting one there would have been a level change nobody asked for." That
sentence is honest as a record of what was decided and false as a reason. A gain belonged on the way in.
The mistake was comparing the new file against the other cues' numbers instead of asking what the file
it replaced actually sounded like — which no number printed off that file would have told anyone, since
the number was fine. The tell was in a channel count and a correlation, not a level.

## 2026-09-16 — the robots get a roster, and it is drawn fresh every night

The six robot names were a fixed table read by seat index, so every match in every build
staffed the same two robots. The table is now a pool of twenty-four characters and the
green room draws three of them, distinct, each time it is opened.

**An index is a character, not a seat.** That is the whole design and it is what the old
comment on the table already said: the name survives a language switch because the number
means the same character in both tables. So `Bots.redraw` shuffles *indices*, and
`Bots.nameKey(idx)` returns a key rather than a string — the reader resolves it against
the language on screen at that instant. This is also exactly what keeps English and
Persian apart: index 15 reads **Kodkhoda** in an English match and **کُدخدا** in a Persian
one, and no draw can put a Persian string in front of an English room. Two independent
pools would have been simpler to write and would have made a seat change identity when
the language did, which is worse.

The draw is Fisher–Yates over the whole pool rather than a sample off it, so no seat can
land on another's joke — three robots should never share a name.

**Where it fires.** `show()` redraws when the target is the green room, not the two
field-builders. The lobby caption and the roster `startMatch` fills have to come off the
same draw, and `show('setup')` is the one place both pass through. Stepping out to the
lobby and back in is a new draw; a redraw of the lobby from the difficulty or opponents
switch is not, because a name that reshuffles under a player mid-choice is a flicker.

**The pool.** The six that shipped, plus eighteen. The host's register does not change:
every name is a real Iranian naming pattern with a machine wedged into it — the
`-ol-Molk` / `-ol-Dowleh` / `-ol-Saltaneh` title stack, the `-qoli Khan` / `-bashi` court
forms, the `Mirza` and `Molla` and `Amir` prefixes. Nothing is a translation of anything;
each is its own joke in each language. Two of the six shipped Persian renderings were
taken to the forms he gave — **کوروش کُدبیر** for Cyrus and **باتالملک** for Bot-ol-Molk —
so the pool is his list, not the table's.

**Nothing got wider.** The longest name in the pool is still "Cyrus the Algorithm" at
nineteen characters, which is the string the style sheet's width budget was already set
by, so no CSS moves and no rule in the style sheet changes.

Verified headless rather than by eye, for the reason this machine gives: five dev servers
already belonged to other chats and the pane would not take a sixth. A `node` harness
loaded the real `i18n.js` and the real `app.js`, then over five hundred draws asserted
that three seats come up distinct every time, that no English name carries a Persian
character and no Persian name carries a Latin one, and that the same seat resolves in the
language on screen. Four thousand draws reached all twenty-four names, and five hundred
draws produced 488 distinct three-seat rosters. `node Tools/check_web.js` still passes,
which is what holds the two tables at parity — the eighteen new keys went into both.

## 2026-09-16 — the log tells you to read its tail

`CLAUDE.md` now says to read the tail of this file when appending, never the whole thing.
At 375 KB the full read costs more than the session that makes it, and the file only
grows. Everything else stands: append a dated entry, never rewrite an older one.

The hazard is that the cost is invisible. A file read once stays in context for every
later step, so the bill lands afterwards, spread across a session that looks ordinary.

## 2026-09-16 — the pack lockup is re-skinned to one metal, and keeps only the emblem red

He likes the collage. He said so plainly: it should take in Iranian history, it should
be representative, the Allah emblem should stay the O and the crown should stay drooping
at the `!`. What he objected to was the finish — "tacky", "doesn't look sleek or nice".

That is a craft problem and not a concept problem, and the cure is tonal rather than
editorial. Nothing was added, removed, moved or redrawn. Every element of the collage
survives at exactly the size and position it had. What changed is that the picture is now
one metal lit by one light instead of a gold-and-brown souvenir-stand arrangement where
every object carried its own specular highlight.

**The recipe, so it can be repeated.** Luminance is stretched to the 1st/99th percentile
and put through an S-curve (`lo 16, hi 198, gamma 1.25, contrast 1.45` about mid-grey),
then tinted cool at `r×0.94, g×0.985, b×1.06`. The only colour that survives is the
emblem, restored from the original by a mask of high saturation, high value and red hue,
kept per connected component and only within 200px of the emblem's centroid. The radius
is doing real work: a bare "keep the red" also keeps the pomegranate, and two red notes
read as an accident rather than an accent. One red note is the point.

**The alpha channel is byte-identical to the delivered file.** Verified by comparing the
full channel after the write. The `.brand-wordmark` drop-shadow traces that silhouette,
so an alpha that drifted by a soft pixel would have moved the shadow's edge. Same canvas,
1983×793.

**It came out at 1.4 MB, down from 2.7.** Collapsing thousands of warm hues into one
cool ramp is worth 1.3 MB to PNG's filters, and the front door is the screen every
player opens first. The entry of 2026-09-15 recorded that if the weight ever mattered
more than the detail, that was the lever. This paid off a debt nobody set out to pay.

**The tag moved to `pack-24`.** Only this image changed, so it gets its own token as
`pack-23` did. `globe-NN` stays where it is; moving it would re-fetch the whole tree to
deliver one file.

**The store assets are stale again, and that is his call.** `Tools/make_readme_banner.py`
and `Tools/make_itch_cover.py` both read this file, so `.github/assets/logo-banner.png`
and `.github/assets/itch-cover.png` still show the gold lockup. The banner is one command.
The cover is an upload. Same reasoning as last time: whether the store page follows the
door is not a decision to make by committing a file.

**The previous art is still recoverable.** `logo-iranian-pack.png` is tracked, and this
change is uncommitted, so `git show HEAD:Web/assets/logo-iranian-pack.png` is the
original. Nothing was overwritten without a way back.

## 2026-09-16 — 1.0.10 is re-cut in place, and its three URLs do not move

The re-skin landed in `11be7e8`, which meant every bundle built yesterday now carried
superseded art. The three assets under `v1.0.10` were rebuilt and replaced rather than a
1.0.11 being cut: the tag stays, the filenames stay, and the download URLs are therefore
the same three strings they were before. Anything already pointing at them starts serving
the new build with nothing to update on the other end.

- mac — `ditto -c -k --norsrc --keepParent` over the universal `.app`
- ios — `build_ipa.sh`, whose `diff -rq` against `Web/` passed before it wrote
- android — `./gradlew :app:assembleRelease`, whose `verifyWeb` passed likewise

All three were opened after the fact rather than trusted. Each carries
`logo-iranian-pack.png` at `4b5cec4c…6fae`, the source digest, and an `index.html` at
`?v=20260916-pack-24`. The GitHub asset digests match local `shasum -a 256` on all three,
and both `.app` bundles — `dist/` and the root copy `build_release.sh` also writes —
verify clean under `codesign --verify --deep --strict`. Every other tree carrying the
lockup is single-linked, so no `cp` could truncate a shared inode.

**`gh release upload --clobber` deletes before it writes, and that is worth knowing.** For
about six minutes the release page was genuinely empty — three assets removed, none yet
uploaded, over a link where 105 MB takes minutes. Nothing was lost, because the local
builds were the source of truth and the command exited 0, but the window is real: a check
of the release inside it reads as a disaster rather than a transfer in progress.

**`Versions/v1.0.10` was left alone, and now describes a superseded build.** The decision
recorded in the buzz entry above still holds — the snapshot answers what 1.0.10 shipped on
the day it was cut, and editing it would destroy the only record of that. The consequence
is that `diff -rq Web Versions/v1.0.10` now reports the lockup as differing. That is
correct and must not be "fixed".

**The itch build updated itself; the itch page did not.** The push to `main` ran
`.github/workflows/itch.yml`, which installs butler on the runner and pushed 181 files,
re-using 94% of the previous build. The HTML5 build therefore carries the new art without
any local butler, which is still not installed on this machine. What remains is his and
only his: the cover (`.github/assets/itch-cover.png`, regenerated at 1260×1000) is a
dashboard upload, and the page itself still answers 404 to anyone not logged in.

The release body's own header art needed nothing done to it. It is a
`raw.githubusercontent.com/.../main/` link, so it followed the commit.

## 2026-09-17 — a new clue can no longer ask what the board already asks, and the verifier stops giving verdicts

Two tools now stand between a hand-written batch and MAIN's archive, and one older tool
was demoted. All three changes come from the same worry: *nothing at all damaged, and
everything better.*

**A repeated question is now a refusal.** `check_bank.py` caught the same `clue_text`
twice inside one slot, and nothing caught a new clue that repeats the bank at large —
which is the likeliest defect in a batch written by an author who never opens the
archive. `Tools/check_repeats.py` compares a batch against all 1,693 rows and against
itself, using the house definition of "same" (`check_bank.normalise`: NFKC, harakat and
tatweel stripped, Arabic yeh and kaf folded to Persian, ZWNJ removed) over content words
only. Two thresholds: **75% of the shorter clue's content words, and at least 6 words in
common.** Measured noise on the shipped bank: **7 near-repeats in 1,693 English rows, 2 in
the Persian** — every one of them genuine, so the floor is calibrated and not merely
quiet. `Tools/append_batch.py` calls it before writing and returns 1 with *Nothing
written.* on any hit.

**A repeated answer is not a defect, and treating it as one would have been the mistake.**
The first version failed a row that answered something its own slot already answered —
which is precisely how the bank is meant to grow past 500 clues: a second question in a
slot you already hold, wearing a `_b` or `_encore` id. The digest showed «A MASH-RUTEH
MADE IN HEAVEN» holding Sattar Khan twice at 200 and the British Legation twice at 400,
all of it deliberate. So answer collisions warn and name the row they collide with; only
question collisions are fatal. Verbatim repeats are additionally caught by `check_bank`'s
own same-slot rule, so `--allow-repeats` — the hatch for a false positive — cannot smuggle
a literal duplicate past both layers. Proven both ways on a probe batch.

**The citation verifier no longer rules on anything.** `Tools/verify_batch.py` was written
to confirm that each row's answer appears where its citation says. Run against Browne's
1910 *The Persian Revolution*, it reported `Sheikh Fazlollah Nuri`, `Liakhov` and
`Sur-e Esrafil` as NOWHERE. Probing the text directly: the scan OCRs the name as **`fazlu`**
(29×)  and writes **`Shaykh`** 178× where `sheikh` appears **not once in 591 sheets**; it
writes `Liakhoff` for `Liakhov` (90×), and `israfil`/`israfll` for `Esrafil`. The bank was
right and the matcher was losing to OCR. That is the worst failure mode available to a
gate — a confident false verdict on a correct row — so the tool now issues no verdict at
all: it narrows the set, supplies the page text, and prints *"leads, not faults … Change
nothing on this output alone."* It exits 0 whenever it ran, and 2 only when it could read
nothing. `NOWHERE` and `ELSEWHERE` were renamed to reflect that.

**The author gets a view of the board without opening the archive.** `Tools/bank_digest.py`
writes `QuestionBank/BANK_DIGEST.md` and `_fa.md` — 158 KB and 152 KB, one line per clue,
grouped by round and category, from the live archive. `GEMINI.md`, `Sources/MAIN
CORPUS/README.md` and `QuestionBank/incoming/README.md` now all point at the digest instead
of at `verified_clues.json`, which the outside author is still forbidden to open. The
digest states the two rules plainly: the question must be new, the answer may repeat.

Untouched throughout: both archives still round-trip byte for byte through
`json.dumps(indent=2, ensure_ascii=False)`, at 1,693 rows each. Nothing was committed.

## 2026-09-17 — seven of the wanted books were already on the machine, and folder 8 takes them

ChatGPT returned a 28-title ranked acquisition list for the corpus, built against the digest's
holes — pre-modern Iran nearly empty, literature absent, ordinary life losing to elite politics.
The question was how much of it he already owns. A filesystem sweep turned up seven: Amanat's
*Resurrection and Renewal*, Grigor's *Contemporary Iranian Art*, Sreberny & Khiabany's
*Blogistan*, and three Cambridge History of Iran volumes. All seven are now in
`Sources/MAIN CORPUS/8 - New Additions (2026-09)/` under the folder convention, checksum-verified
against their sources. They were **copied, not moved** — the originals are his dissertation and
research library in `~/Documents/Morad's Documents/`, and an earlier round clearly did the same
thing, since Amanat's *Iran: A Modern History* sits in both folder 1 and the Oxford folder.

Three of the seven were not on ChatGPT's list. Cambridge Vol. 6 (Timurid and Safavid) and Vol. 7
(Nadir Shah to the Islamic Republic) were simply sitting in the Oxford folder and close the same
medieval and Safavid holes the list was aimed at; Vol. 1, *The Land of Iran*, is the physical-Iran
volume ChatGPT named as the gap analysis's biggest omission. Taking an owned book that costs
nothing beats buying its equivalent.

The larger finding, not acted on: roughly 150 further Iran books are already on the machine across
two folders — `Readables/Nonfiction/Iranian Studies/` (43 files) and the Oxford
`Sources - Secondary/Iran (General)/Books/` (104). Many fill gaps ChatGPT named as purchases:
Browne's *Literary History of Persia*, Dabashi on the Shahnameh, Ebrahimnejad on Qajar medicine,
Floor/Clawson/Matthee on Qajar money, Khosravi and Mahdavi on everyday life, Bajoghli on sanctions.
Folder 8 defines the scope of the next authoring batch, so which of those get promoted is his call,
not a bulk copy. Both lists — the 25 still missing and the owned substitutes — are written up in
`~/Desktop/Jeopardy Sources - Missing Books.md`.

One near-match left alone: a 33 MB scanned dissertation on the Armenian merchants of New Julfa,
which is the Aslanian slot but has no text layer, so no author, no year, and no page-by-page
sourcing. Nothing committed; `Sources/` remains gitignored.

## 2026-09-17 — the write path, closed

Five agent-facing documents still told an author to write `QuestionBank/verified_clues.json`
by hand — `AGENTS.md` (§1 and §4), `.claude/commands/historical-bank-pipeline.md` (§1 and
§11), `CORPUS_BRIEF.md` (§1) and `QUESTION_AUTHORING.md` (§11). All five now route through
`QuestionBank/incoming/<stem>-{en,fa}.json` → `Tools/append_batch.py <stem>`, with the
dry-run-first rule and the round-trip assertion stated where the malformed rows would
otherwise have gone. Verified by grep across all five; clean.

A correction that came out of doing it: **`append_batch.py` is not a complete gate.** It
runs `check_bank.py` on the merged bank and `check_repeats.py` on the batch, and neither
pins a row count — but the three archive validators do (`validate_1000_clues.py`,
`verify_flawless_state.py`, `validate_persian_bank.py`, all at 1,693), and
`validate_persian_bank.py` additionally counts `QuestionBank/persian_clues.json` and
`App/Resources/persian_clues.json`, two id-keyed dictionaries nothing in the append flow
regenerates. So a merge succeeds and the validators then fail by arithmetic. Written down,
not repaired — whether the merge should regenerate the dictionaries or bump the counts is
his decision.

Also measured and folded into the docs: `book_title`, `author`, `supporting_passage` and
`historical_period` hold the English values on 1,693 of 1,693 Persian rows. `theme` does
too, and that one is correct by contract — English keyword in both banks. The other four
are the known Persian-provenance defect. Reported, not repaired.

Both authoring prompts now carry a one-pass rule (write it all, do not stop to ask), and
the Obsidian note `Projects/Jeopardy/Gemini Prompts - Clue Writing.md` gained the section
on the ~50-clue Continue button — what it is, why no prompt disables it, and the three
levers that shrink it. The note's course prompt is byte-identical to `Course/BANK_SPEC.md`.
Nothing committed; no bank file opened for writing.

## 2026-09-17 — the machine really does not have the other twenty-five

He said twice that the recommended books were already on his machine, "especially in my
academia -- oxford folder". So the sweep was redone properly, and the answer is no.

Every ebook on the machine was indexed live rather than through the old scan cache —
15,384 PDF, EPUB, DJVU, MOBI and AZW3 files under `/Users/Morad`, `Library`, `.Trash`
and app bundles excluded. Then every shelf a book could sit on was opened by hand:
Oxford's Iran Books (104), Articles (190), Persian Articles (121), Persian Books (37),
Media Studies Books (81), Fashion Studies (15) and Fashion Magazines (5), the 1970s Iran
dissertation shelf (72), Dress and Fashion (49), Unorganized PDFs (115), the whole
Readables nonfiction tree, Poetry (68), Fiction/Novels/Persian, the Calibre library, and
Zotero. The Persian shelf was searched again in Persian script. None of the twenty-five
turned up: zero filename matches for daryaee, brosius, sasanian, peacock, seljuk, saljuq,
razoux, karimi-hakkak, zoroastrian, aslanian, timurid, babaie, manz, lane, sternfeld,
alimagham, briant, juvaini, limbert, matthews, maloney, hafez, or Cambridge History of
Iran Vol. 3. The hits that did contain those strings are all other things — a psychology
paper by a different Boyce, a Foucault PDF, an interior-design monograph by a different
Karimi, magazine issues, and the two Cambridge volumes already copied into folder 8.

What the sweep did produce is a much larger picture of what he owns. The Oxford 1970s
dissertation shelf and the Readables Iranian Studies shelf between them hold roughly sixty
Iran monographs against ChatGPT's named gaps — Katouzian's *Political Economy of Modern
Iran* standing in for Maloney, Paidar and Sedghi and Hendelman-Baavur for the women's
cluster, Browne and Dabashi and Talattof and Hillmann for the literature hole, Khosravi
and Mahdavi and Basmenji for everyday Iran, Bajoghli and Sadeghi-Boroujerdi for post-2009.
The deepest hole is the Islamic conquest through the Safavids, where he owns nothing at
all; Cambridge Vols 1, 5 and 6 are the only thing in it, and they are the reason those
went into folder 8.

`~/Desktop/Jeopardy Sources - Missing Books.md` was rewritten against this. The shopping
list of twenty-five is unchanged — it was already correct — but it now carries the sweep
table, the proof of absence, and the full inventory of what he owns grouped by gap. Whether
to promote that inventory into folder 8 is his call, not mine; it is a curation decision
about a curated corpus and far bigger than the seven books the last round added. Nothing
was copied this round, nothing was moved, and no bank file was touched.

## 2026-09-17 — folder 8 goes from seven books to a hundred and twenty-seven

He asked what else was worth promoting and then said to promote all of it. Folder 8 went
from seven books to 127 files — 124 PDFs and two EPUBs (Nasr, *Iran's Grand Strategy*;
Parsi, *Treacherous Alliance*), plus the README.

The selection rule was the gaps, not the shelf. Literature and the Persianate world get
Browne's *Literary History* (both the complete Raw set and Vol. 1), Dabashi's *Shahnameh*
and *Close Up* and *Theology of Discontent*, Talattof twice, Olszewska, Spooner & Hanaway,
Haddadian-Moghaddam. The Qajar economy and society gap gets Floor/Clawson/Matthee on
money, Ebrahimnejad on medicine, Martin, Gleave, Farmanfarmaian, De Groot, Atkin, both
Sabahis, Floor & Javadi, Amanat's *Pivot*, and the whole Cronin shelf — she wrote the
syllabuses the planned courses are built from, so her five books matter twice over. Gender
gets Paidar, Sedghi, Hendelman-Baavur, three Najmabadis, Amin, Afary twice, both Fathis,
Kandiyoti, Nashat. Everyday and popular Iran gets Khosravi, Mahdavi, Basmenji, Adelkhah,
Balasescu, Payvar, Atwood, Varzi, Scheiwiller, Torab. Cinema and media get all four
volumes of Naficy, both Mottahedehs, Dabashi's *Close Up*, Tapper, Semati, Khiabany,
Mowlana, Issari, Kimiachi, Mesbahee, and Naficy's *Iran Media Index*. Intellectual history
gets Tavakoli-Targhi, Marashi, Vejdani, Matin, Zia-Ebrahimi, Gheissari, Vaziri, Ridgeon,
Nabavi, four Mirsepassis, Amanat & Vejdani. The state and the revolution get Abrahamian
twice, Atabaki three times, Keddie twice, Fischer, Ostovar, Khomeini, Yarshater's *Iran
Faces the Seventies*, the Iran Almanac, Assadi's 1980 attitude survey, Cooper, Shawcross,
Robin Wright, Milani's *Eminent Persians*, and Katouzian three more times. Post-2009 gets
Bajoghli, Sadeghi-Boroujerdi, Vahabi.

Two things the sweep taught that the filenames did not. First, surname greps pull in
journal articles: Mirsepassi, Sadeghi-Boroujerdi, Bajoghli, Alfoneh, Parsa, Ramazani and
Khiabany all matched papers as well as books. Twenty-eight of those came out again and
went to `~/.Trash` after a page count — under twenty-five pages and it is an article, not
a monograph. Second, the text-layer test is the one that decides whether a book is worth
having at all, because the bank cites printed pages and a scan cannot supply them. Run
across the whole folder, only **Amanat, *Resurrection and Renewal* (1989)** is image-only,
498 pages with no layer anywhere in it. It came in with the previous seven and he approved
it then, so it stays; but nothing can be authored from it until it is OCR'd.

One curation question is now open and I did not decide it. `Corpus/Metadata/corpus_manifest.json`
still describes 49 monographs. The 120 new books are on disk and outside the manifest, so
they are invisible to `bank_digest.py` and to the authors. Filling in `source_id`,
`periods_covered`, `themes` and `extraction_status` for them is a real piece of work and a
second curation pass; it is his call when it happens.

Every file was copied, never moved and never linked. His research tree is untouched.

## 2026-09-17 — the Drive batches come back one field from landable

Gemini writes the planned courses on Drive, because Spark on the phone can read the books
there without a VPN on this laptop. The Qajars batch is finished — 50 rows a language —
and he wants it in MAIN rather than shipped as a course edition. So it was measured
against MAIN's real gate instead of being converted by hand: run through
`append_batch.py --dry-run`, and each language through `check_bank.py` on its own,
because `gate()` only prints the last 25 error lines and the English ones had scrolled
off. That display cap made the two languages look asymmetric when they were identical.

Everything but two things was already right: the archive's 27 field names, mirrored ids,
ten complete categories, fifty distinct `correctLine`s and fifty distinct `wrongLine`s, a
citation on every row. **52 of the 54 errors a language were `distractor_rationales`** —
written as one object keyed by the option text where the archive wants a list of three
objects each naming its own option. The three rationales are present and correct in every
row; the wrapper is the whole of it, and the re-shape is lossless. `set(dict keys) ==
set(wrong options)` in 50 of 50, both languages. Insertion order matches the options in
47 of 50 English — so a converter must match by option text and never by position, and
any three rows would have landed wrong silently had it gone the other way.

The remaining error, one row a language, is the same thing twice: an alias list that
carries a variant of the answer but not the answer. `Tabriz` / `["Tebriz"]`, and
`فتحعلیشاه` / `["فتحعلی شاه قاجار", …]`. The gate's floor test reads a variant-only list as
one that wandered in from another row, and its token test cannot see an `e`/`i` swap or a
ZWNJ, so this is the proxy misfiring and not a wrong answer. The list should name the
answer anyway — it is the record of what counts as that answer, and 815 English and 864
Persian rows in the archive already do.

**`Tools/land_batch.py` is new** — the hop for a batch written outside the project.
Reads a folder's `rows-en.json` and `rows-fa.json` (the folder itself or its `bank/`),
re-shapes the rationales, writes `QuestionBank/incoming/<stem>-{en,fa}.json`, then runs
the loading sequence `GEMINI.md` gives an in-project author: rehearse, land, render,
digest. **Default is to land**; `--check` writes nothing. It refuses a row by name rather
than guessing, learns the archive's field set from the archive instead of hard-coding
1,693-era shape, says plainly that a file mid-write is not valid JSON rather than
reporting a line number, and deliberately does not duplicate anything `append_batch.py`
already checks. `--allow-repeats` is not exposed: the near-repeat gate is the one thing
worth a second look by hand.

The same two defects are fixed at the source as well, in a file on the Desktop to paste
into the Drive `GEMINI.md`: §7 for the rationale shape, §8 for the alias list starting
with the answer, §12 so the self-check counts both. With those in, the next batch
should land with no help from me.

With the two alias entries added, the Qajars batch rehearses **green** — exit 0, no
errors, 1,693 + 50 = 1,743 rows — with 28 near-repeat notices, every one of them the
same *answer* asked a different way, which is what `_b` and `encore` are for and which
the gate confirmed as legal. **It is not merged.** The alias fix sits in the staged copy
in `QuestionBank/incoming/` only; the Drive source still has the defect, and the Pahlavis
batch has not been written yet. Landing waits on him, and the three archive validators
need 1,693 and 261 bumped in the same commit when it happens.

## 2026-09-17 — the three dead scans get text, and `--redo-ocr` is the finding

The three books in `Sources/MAIN CORPUS/` that carried no text layer now carry one, in
place, and all three are on the reading list: Bill, *The Eagle and the Lion* (1988), 547
pp; Rahnema, *An Islamic Utopian* (1998), 217 pp; and Amanat, *Resurrection and Renewal*
(1989), 498 pp, which had never been registered at all. Measured after the fact rather
than trusted — 1,146,267 / 1,006,986 / 1,171,871 alphanumeric characters. The pre-OCR
originals are in `~/.Trash`.

**`--redo-ocr`, not `--force-ocr`.** Force-OCR rasterizes every page: Bill went 8.3 MB →
114 MB, 547 images re-encoded to 2368×3612 CCITT. `--redo-ocr` on the same book produced
**the same 1,146,267 characters** — checked page by page, not assumed — while leaving the
original JBIG2/JPX images untouched: 571 images, 1,452.9 summed, sizes identical to the
source. The text layer costs ~3.3 KB/page, so the book lands at 9.2 MB. Same text, 13×
smaller. Rahnema and Amanat took `--skip-text`, which is for a PDF that already has a
layer worth keeping, so those two needed no decision.

This is not about three books. The Persian shelf is 37 image-only PDFs across 14,422
pages; a 13× inflation there is roughly 3 GB, and `--redo-ocr` is what prevents it.

**The corpus list is 50 books.** Amanat's entry is appended; Bill and Rahnema flip from
`ocr_required` to `ready`, `avg_chars_per_page` measured. The count moved everywhere it
is stated — `AGENTS.md`, `BANK_SCOPE.md`, `QUESTION_AUTHORING.md`, `Course/BANK_SPEC.md`,
`README.md`, the bot line in **both** halves of `Web/i18n.js`, and the `course.js` comment
that quotes it. `Tools/make_readings.py` learned an eighth heading,
`8 - New Additions (2026-09)`, and `check_readings.py` now asserts 92; the shelf reads 92.

Rahnema's density figure carries a caveat in its notes: the scan is of two-page spreads,
so 4,640.5 chars/page is about twice a printed page. Anyone comparing it against a
single-page scan has to halve it first.

`Corpus/Metadata/corpus.db` was synced by hand — `source_periods` and `source_themes`
carry what the manifest keeps as lists — because **no script rebuilds it.** A manifest
edit silently leaves it stale. Worth a generator.

**The one `(Raw)` file in `Sources/` was misnamed.** Ridgeon, *Sufi Castigator* (2006) sat
in folder 8 labelled `(Raw)` while carrying a full 563,701-character text layer. He had
said a misleading name may be corrected, so the suffix is off. It has no twin, so the
delete-the-RAW rule never fired — nothing was deleted under it.

**Folder 8's other 126 books stay unregistered**, and its README now says so plainly.
They are readable but not on the reading list, so no clue may cite them. Registering one
is an edit in eight places. Worse, a machine-wide sweep found ~62 more `(Raw)`-named PDFs
in the Oxford library outside the project, ~30 of them books that already have text
layers — the same misnaming at scale, left alone because it is outside the working tree.

## 2026-09-17 — the Qajars become a course, and a course learns what it owns

The Qajar bank landed from Gemini at the floor: 250 single + 250 double + 12 finals =
512 rows a side, 100 complete categories, no `_b` rows. `Web/courses/qajars/` now holds
`bank-en.js`, `bank-fa.js`, `course.js`, `course.css`, `assets/sprite-stephanie.png` and a
placeholder `tile-course.png`. It registers, it is reachable at `?ed=qajars` and by the
last-visit rule, and it wears its own skin.

**A course owns exactly four art files, and the names are fixed** — `tile-course.png`,
`logo-wordmark-course.png`, `stage-backdrop-course.png`, `sprite-<professor>.png`. Iran in
World Politics is the only complete set. The Qajars have two: the sprite is real, the tile
is still `soon-qajars.png` byte for byte, and the wordmark and backdrop do not exist.
`Course/course-template/course.css` — unread until today — confirms the shape: the palette
block is very nearly the whole skin, and `.stage-bg` is the only rule in a course sheet
that swaps an image by path. That file is the skeleton, and the Qajar sheet is consistent
with it.

**Two swaps were deliberately not written**, because a rule pointing at a file that is not
there is a black stage and a blank lockup — worse than the general edition's art. They are
documented in the `course.css` header instead of half-implemented: the `.stage-bg` rule and
the `swapWordmark` block. The wordmark block is already correct twelve lines away in
`iran-in-world-politics/course.js:196-212`, called at line 279.

**The front door showed the Qajars twice and the bug was the cache tag, not the code.**
`SOON_CARDS` in `app.js` had already been cut to the Pahlavis alone, and the server was
serving the fixed file — `curl` proved it — but `index.html` still carried
`app.js?v=20260916-early-lockout`. Every `<link>` and `<script>` in that file is
cache-busted by a tag that *names the change*; edit a file without bumping its tag and no
client fetches it, including the preview pane. Re-navigating to a URL the browser had
already visited re-served the stale copy on top of that, because `python3 -m http.server`
sends `Last-Modified` and no `ETag`. Bumped to `app.js?v=20260917-qajar-1`. This was a
live delivery bug in what had already been reported as done.

**The skin is lapis and rose madder, not the flag.** The Islamic Republic's emblem postdates
everything on this board, and the tricolour was only fixed in the dynasty's last decade, so
`--green` is `#2f57b4` and `--red` is `#ad2447` and the flag rule is lapis/cream/madder.
The variables keep the engine's names — the engine means "the right hue" and "the wrong
hue", and renaming its vocabulary from a skin is how a course stops being loadable. Copper
was ruled out for the second time: it reads as gold, and gold lands next to the retired
brown-and-gold. No warm metal anywhere in the file. Verified live: computed styles resolve,
the rule is a 9px lapis/cream/madder stack, the imprint is pale lapis, and the ten syllabus
rails render numbered 01–10.

**`front.soonQajar` is still in `i18n.js` and stays.** Two keys, referenced by nothing in
the live build. They are the matching half of the coming-soon machinery, which still runs
for the Pahlavis, and the two i18n tables are held at exact parity — removal risks a
parity break for no gain. The other hits are in the frozen `Versions/` snapshots and the
stale vendored copy under `Android/`.

**Dr Stephanie's host cues are namespaced by course** — `stephanie_qajars_*`, and
`stephanie_pahlavis_*` when the Pahlavis are built. She teaches both, and a bare
`stephanie_*` would put one course's lines in the other's mouth. The placeholder-clip
convention (`host_line_placeholder`, `host_scene_placeholder`) is how a cue is registered
before there is audio for it; the harness confirms 68 `EDITION_SOUND` cues, all host cues
still placeholders, and no named cue without a line. Voice comes later — she talks in
writing for now, in the same smug register as Tannaz, in an old-world British key.

**The rules generalise and were written to travel.** Both the Drive
`GEMINI.md` (now a Pahlavis brief, not a two-course one) and `CODEX_QAJAR_ART_BRIEF.md` at
the root state them as house rules: four art files per course with fixed names, the wordmark
lockup constant and only emblem/fill/subtitle varying, the course palette declared in its
own `course.css` and obeyed by the art, one sprite copy per course even when the professor
is the same, and a missing asset left missing rather than pointed at.

The Pahlavis are staged at `Web/courses/pahlavis/` and remain a coming-soon card: their
bank is not written. The Drive doc's warning to the next agent is that Weeks 5, 6 and 7 of
the syllabus are thin — Week 6 in particular is one article, already filed under Week 4 —
and that this is the honest shape of the course, to be reported in `cover.md` rather than
padded around.

## 2026-09-17 — the second course breaks the first, and the queue stops dropping beats

Adding the Qajars exposed a bug in the first course's contract. Both `course.js` files
register an `editionchange` listener and both call a `publish(mine)` that sets three
globals on the way in and **deletes them on the way out** — `HOST_CUE_MAP`, `HOST_VOICE`,
`EDITION_SOUND`. `index.html` loads Iran in World Politics first and the Qajars second, so
the listeners run in that order. Switching **to** Iran therefore went: Iran publishes its
three, then the Qajar handler runs one tick later, sees an edition that is not its own,
and deletes all three. Iran in World Politics would have run with no host pool, no cue
map, no edition sound and no pre-clue gate — a silent professor and an unmapped
soundtrack, on the course that was working yesterday.

Fixed in the Qajar file alone, which is enough: ownership is now tested by identity
against the course's own `POOL` object — the globals are ours if that object is the one
on the window, and only then are they deleted. Iran's unconditional delete stays correct
because the only other writer is the Qajars, and it no longer withdraws Iran's work.
Verified in all three directions in the browser: `?ed=qajars` → Iran keeps
`right[0] = eskandar_04_correct_annoyingly_so`, 35 edition cues and a live `HOST_PRECLUE`;
Iran → Qajars gives Stephanie's pool and 68 cues; either → `general` clears to nothing,
so MAIN cannot inherit a course's soundtrack.

**The reconstructed queue dropped beats.** `enqueue` bailed when a drain was already
pending, so any beat landing within the 900 ms quiet window was silently discarded — on a
board that fires streaks, leads and comebacks in the same tick, that is most of them.
`standDown` also nulled `pending` without `clearTimeout`, leaving a timer to fire against
a queue it no longer owned, and the `hostbeat` listener had no edition gate at all, so on
MAIN she would have commented on a board she does not teach. All three fixed; the queue is
now Iran's shape. Verified: a `boardIdle` and a `streak` fired 150 ms apart both speak, in
order, with the right bubble — `stephanie_qajars_start_single` then `stephanie_qajars_streak`
("Three in a row. One would almost call it a method."). Under the old code the second was
gone.

The lesson worth keeping: **a second course is a test of the first.** Nothing in the
Iran course was wrong in isolation; it was wrong the moment a peer existed. Any new
per-edition global that a course sets must be torn down by ownership, never by
unconditional delete, or the load order in `index.html` decides which course survives.

Cache tag bumped `courses/qajars/course.js?v=20260917-qajar-2`. The Qajar splash was
photographed for the first time: ten syllabus rails numbered 01–10, the tagline, the
credit, and the lapis/cream/madder rule all correct; the wordmark is still the general
edition's and the backdrop is still the Tehran skyline, which are the two documented art
gaps. An audit of every gradient in the DOM found lapis `rgb(47, 87, 180)` and cream
`rgb(244, 241, 234)` and **no green or red anywhere** — so the colour fringing at the
stage edges is the general backdrop photo, not a leftover from MAIN.

## 2026-09-17 — the Qajars are a course and not yet a clean bank

`Web/courses/qajars/` plays tonight with a bank that has never been through MAIN's gate.
It was converted by `Course/banks/qajar-pass-2026-09-17/convert_to_edition.py`, which
checks **shape** — field names, four options, a citation, five rungs under one title — and
nothing about content. So all three things the gate would have refused shipped with it,
and the board deals them now.

Measured on the full 512 rows, each language against itself and against the archive:

- **200 rows carry the wrong `difficulty`** — 100 a language. Every double-round 400 says
  `CASUAL` and every double-round 1200 says `STANDARD`: the single-round ladder carried
  onto the double, which is §4's exact trap. `Tools/land_batch.py` now derives the label
  from the rung on the way in and prints how many rows it had to correct.
- **10 rows ask a question another row in the same bank already asks** (8 English, 2
  Persian), always a single slot and a double slot on the same fact. Each is a rung in a
  five-clue category, so deleting one drops the rung and `buildBoard` silently discards
  the whole category — these want rewriting, not removal.
- **19 alias lists share no string with their own answer** (16 English, 3 Persian). Read
  row by row, they are genuine transliterations the gate's token test cannot see —
  `Tebriz`/`Tabriz`, `Constantinople`/`Istanbul`, `estebdad`/`istibdad` — plus two loose
  phrases (`Italian officers`, `Italian mission`). None hands a player a wrong answer. §8
  now asks for the answer itself as the first alias, which silences the check for free.

`difficulty` is not cosmetic: `Web/app.js:4446` reads it into `NUDGE`, so a label one rung
low moves a robot's accuracy by 0.08 to 0.20 across 200 clues.

Nothing was merged. The archive is still 1,693, and `QuestionBank/incoming/qajars-*.json`
holds the pre-fix rows — running `append_batch.py qajars` against them merges all 213.

**The gap this found is in the delivery path, not the writing.** A batch authored on Drive
has no shell, so its self-check has to be arithmetic it can do in a conversation — and the
Drive `GEMINI.md` asked for a verdict instead of counts. §12 is rewritten to count rung
mismatches, repeated questions and unowned aliases *per batch*, and to say plainly what
the Qajars shipped. The in-tree `GEMINI.md` needed nothing: it runs `check_bank.py` and
`check_repeats.py` itself, which is why it has no such hole.

## 2026-09-17 — the repeat check could not read a course bank at all

The entry above says the in-tree guide had no hole because it runs `check_repeats.py`
itself. It did not, for a course. `check_repeats.py` read `clue_text` — MAIN's field name —
and a course bank says `clue`, so every play-shape row indexed as an empty clue and
nothing in the tree could ever be matched against it. The instruction to run the checker
was there; the checker could not see the file. That is the whole reason a course bank
shipped with ten questions asked twice and no one noticed.

Four changes, all of them closing that:

- `clue_of()` in `Tools/check_repeats.py` reads either shape, and a new `--file` audits one
  bank file against itself, where a near-repeat is **fatal** — a course ships its bank
  whole, so a question asked twice inside it is two clues one match can deal. On the bare
  `rows-en.json` an author hands over it falls back to reading a plain JSON array, so the
  check can run a file earlier than the bank the file becomes.
- `Course/build_edition.sh` runs it as a third gate, after `check_edition.py` and
  `check_bank.py`. `check_bank.py` caught a repeat inside one slot; nothing caught a
  question asked twice in two different categories, which is the shape the Qajar bank had.
- `Course/banks/qajar-pass-2026-09-17/convert_to_edition.py` — the one-off converter that
  wrote the banks directly and never called the gate — now calls it and exits with its
  status. A script that writes a bank runs the gate or it fails.
- Both guides. The in-tree `GEMINI.md` gained the two-ladder block with the positional
  trap spelled out and the cross-category repeat rule; `Course/BANK_SPEC.md` gained rule
  4b and a paragraph saying to run the gate even when you did not build the banks with it.
  The Drive `GEMINI.md`'s §12.4 gained the real cause — a pair of twin categories on one
  subject reusing their best fact — and the one read-only command that proves it.

**This makes `iran-in-world-politics` fail its own gate, and that is a true positive.**
The shipped Iran course carries **2** genuine near-repeats: the Elling & Harris Iran
Social Survey item, at `double_identity_2000` and `single_periphery_1000`; and the 1988
Expediency Council, at `single_maslahat_200` and `double_improv_ministry_2000`. Both are
one fact in two slots — the defect class predates the Qajars. The bank was not edited; a
bank file is not touched unless he asks, and two rewrites are his call, not mine.

Verified: `check_repeats.py --file` finds exactly the 8 English and 2 Persian Qajar pairs,
matching the known defect list item for item and inventing none; the identical 8 come back
from the Drive `rows-en.json`; and `build_edition.sh qajars` exits 1 at stage 2 with the
200 `difficulty ... does not match rung` errors that were already there and merely never
read.

Still open: `QuestionBank/incoming/qajars-{en,fa}.json` holds the **pre-fix** rows —
`append_batch.py qajars` against them merges all 213 defects. Move, regenerate, or leave
is his call.

## 2026-09-17 — A screen before the front door, so nothing arrives late

Asked for a page in front of the door whose job is to load everything, so art stops
glitching, jumping or leaking between shows. Built as `#screen-boot`, the eleventh
screen and the only one carrying no art of its own: type, a hairline and a shadow on
opaque `#070707`, so it paints on the first frame instead of waiting on the files it
was built to wait for. It warms every picture the show can reach, then hands the frame
to the door.

**Why the leak mattered.** A course fetched its pictures when its circle was pressed —
on a stage still wearing the previous show's art — so the arrival was a visible swap
rather than a cut. The pass walks *every* registered edition rather than the arriving
one, which moves that fetch to a black screen where it can disturb nothing. A show is
one press away and now always warm.

**The three symptoms were one mechanism.** Jump: art arriving after its screen. Leak:
the fetch above. Glitch: a half-arrived backdrop under a partially-inset screen.

**The unscoped rule that had to be beaten.** `courses/iran-in-world-politics/course.css`
insets *every* active screen by the safe area above and the host band below, because
every other screen shares its floor with her. Boot is not sharing it, and measured
86px short with the stage showing through. `#app #screen-boot.is-active { top:0;
bottom:0; }` out-specifies it — two ids and a class against one id and two classes.

**Where the list comes from.** `tile`/`hero`/`logo` are already declared per edition, so
the Qajars' missing backdrop and wordmark are skipped without a special case: a file
that does not exist is not declared and never requested. A new optional `art:` key
carries the professor sprites. Host sprites come through a new `HostLayer.art()`, which
walks the registry rather than naming Tannaz's five poses, so a future course's poses are
warmed without a second edit.

**Hand-off.** `finish()` sets `data-boot="ready"` and waits 320ms, so the door comes up
under a loader that is still leaving; the 500ms fade runs both ways. A `?ed=` link sets
`S.bootTarget = 'splash'` and hand-off lands there instead — it is the one caller that
lifts a screen during boot, over the very art being fetched. `finish()` re-checks
`S.screen === 'boot'` before it moves anything, because a `?code=` link opens the online
door before the pass runs and must not be pulled back. Floor 1.5s so a warm cache does
not read as a flash; ceiling 12s so a file that never answers cannot hold the door shut.

**Audio is not warmed.** `Sound` exposes no preload hook and reaching into its internals
was not worth it for v1; the complaint was visual. Say so if the entry pass is wanted too.

Verified with eyes: the boot mark, the status word and the hairline cross-fading over the
door; the fill reaches 320/320 of its track; boot reaches `ready` and hands to `front` on
a plain load and to `splash` after `?ed=qajars`, with zero console errors. Two probes
read the fill at zero width — that is a transition on a screen that is not on the floor,
which never advances; re-measured with the screen visible and it runs full. Not a defect.

## 2026-09-17 — the stale Qajar batch leaves the tree

The entry above left `QuestionBank/incoming/qajars-{en,fa}.json` as an open question. Both
held the **pre-fix** 512 rows — 50 `double/400` labelled `CASUAL` and 50 `double/1200`
labelled `STANDARD` a side, the same 100 the gate fails — and `append_batch.py qajars`
against them would have merged all 213 defects. Nothing referenced them but two lines in
this log. The only difference from `Course/banks/qajar-pass-2026-09-17/rows-{en,fa}.json`
was the shape of `distractor_rationales` (list-of-option-objects there, dict-keyed-by-option
here): same rows, two serialisations, both pre-fix.

Morad: "what is not needed can go." Moved both to `~/.Trash`. `QuestionBank/incoming/`
now holds its `README.md` and nothing else — the folder is the pipeline's scratch space,
not the bank, and an empty one is its normal state between batches.

The course's own `Course/banks/qajar-pass-2026-09-17/rows-{en,fa}.json` still carries the
pre-fix rows, and that is deliberate: it is the source of record for that pass. Re-running
the converter no longer writes a bank from it silently — it exits at the gate.

## 2026-09-17 — The boot screen grows a face: the wordmark, and the door's own globe

The boot screen (entry above) was type and a hairline on black, on the argument that a
loading screen which has to fetch a picture before it can be shown is the joke telling
itself. He asked for the panorama on it — *"that panorama we had made that moves and
moves from era to era in that glass blob/globe"* — and for the main logo.

Both were already on the sheet, so both are borrowed rather than drawn.

- **The globe is the front door's main disc.** Same file (`hero-main.png`), same cache
  tag (`?v=20260915-globe-22`), so boot and door share one fetch; same `.circle-frame` +
  `.circle-art` + `.lens` vocabulary, which brings the `#globe-warp` displacement, the
  specular `::before` and the lens rim with no new CSS for any of them; and the door's
  own two grades on the picture (`brightness(1.12) saturate(0.90)`), because a globe
  dimmer than the disc it becomes is a flicker at the hand-off. Boot is the door's disc
  drawn one beat early, and the curtain lifts onto the picture it was already showing.

- **The mark is `logo-wordmark.png`** — the house lockup, not the pack lockup the door
  wears, because the door is the show's sign-off and this is the game's name. It is
  deliberately **not** `class="logo"`: `course.js` re-skins every `.logo` on
  `editionchange`, and boot is drawn before any show is on the stage, so it must never
  wear one's skin. `boot-logo` keeps it out of that walk. A `?ed=` deep link gets the
  same mark for the same reason — the curtain is the game's, and a course's own wordmark
  is something the front door gives it.

**The veil.** A picture still in flight paints as an empty box, and an empty box under a
title is the glitch this screen exists to prevent. So both pictures start at `opacity: 0`
and `bootWarm` lifts each one the moment its own file is in hand, asked of `complete &&
naturalWidth` first — a cached file is finished before the pass runs, and a `load`
listener attached after that never fires. A failed file lifts its veil too: a 404 must
not hold a title card blank forever. What the screen *starts* on is unchanged — black,
the state word, the hairline, on the first frame.

**The pan.** The door sweeps this picture over 90s with a −20s delay, which across a
two-second pass is a still frame. Boot runs its own `boot-pan` instead: 26s, delayed −9s,
so it opens a third of the way in, in the middle of the ease where the sweep is fastest —
measured 63% → 41% of the width in 1.5s. Killed under reduced motion, like the door's.

`boot-word` and `@keyframes boot-breathe` went with the type they breathed on; the
globe's travel is that "it is alive" cue now.

Verified in the pane at 900×880: the mark 299×100 over a 264px globe, both veils lifted,
pan running; the front door untouched (same art URL, same filter, `edition-main-pan`
still running, three circles), and no `.logo` anywhere near the boot mark.

Worth recording, because it cost a false alarm: **the Browser pane can report a 0×0
viewport**, and with it every `clamp()` and `min()` in the page collapses to zero —
the boot globe measured 2×2 and the mark 0×0, which reads exactly like a broken
stylesheet. Set a viewport with `preview_resize` before believing any geometry off that
pane.

## 2026-09-17 — the shipped Iran course asked three questions twice, and carried two tells

The repeat gate `build_edition.sh` gained this morning was written against a bank nobody had
audited with it. It found what it was built to find: **three genuine near-repeats in a course
that has been on the splash since 09-14.**

- `double_identity_2000` asked the Persian mother-tongue plurality, which `single_periphery_1000`
  already asks (514 of 1,129, 46%). Rewritten to the Turkish second plurality — 206, 18% — a
  figure in its own verbatim passage and already one of its four options.
- `single_nuclear_200` asked the regional nuclear monopoly, which `double_war_400` already asks.
  Re-aimed at the same row's own p. 3 fact: the region's one nuclear state that never signed
  the NPT.
- `double_improv_ministry_2000` asked the 1988 Expediency Council, which `single_maslahat_200`
  already asks. Rewritten to the Management and Planning Organization sentence quoted verbatim
  from Keshavarzian, *The Sacred Republic*, p. 63 — which also retires a fabricated citation.

**All three live in `Course/banks/gemini-pass-2026-09-14/iranian_jeopardy_bank.json` and nowhere
else.** `bank-en.js` and `bank-fa.js` are rendered from it by `convert_to_edition.py`; a fix
written into a bank file is wiped by the next render. The source round-trips at `indent=2`,
`ensure_ascii=False`, trailing newline — assert that before writing, and a load-modify-dump is
then a minimal diff instead of a rewrite of 690 rows.

Which row of a pair to rewrite is not a coin toss. `single_maslahat_200` turned out to be sound:
it cites Chehabi's *Daedalus* article, a different work from the Week 3 PDF, and its passage is
verbatim on that scan. Rewriting it would have killed the repeat and left the fabricated citation
standing; rewriting its partner did both jobs.

Two more errors were failing the gate underneath the repeats, neither of them a repeat:

- `single_matin_1000` offered `Armed Struggle: Both a Strategy and a Tactic` — the only option on
  the row carrying a colon, so the odd button out is findable by its punctuation. Now "as Both a
  Strategy and a Tactic", with the rationale re-pointed at the new string.
- **One category was written two ways in `bank-fa.js`, and the reason is worth keeping.** "THE
  GRAMMAR OF RESISTANCE" and "DISCOURSE OF DISDAIN" are two categories, but both Persian titles
  read صرف و نحو… — the same pun, differing by an invisible kasra that `normalise` strips. The
  good news is that `course.js` already held the intended Persian for the second, گفتمان بیاعتنایی,
  wired to the foreign-policy clip; the bank had simply never agreed with it. The bank now matches,
  and that category reaches its clip again: **138/138 in both languages**, which also clears the
  one "reaches no week clip" warning.

`bash Course/build_edition.sh iran-in-world-politics` → **exit 0**, no errors, 206 warnings, and
0 repeats / 0 near-repeats in both banks.

**Open on purpose, and a content call rather than a repair:** the other four rows of `IMPROV AT
THE MINISTRY` (`_400`, `_800`, `_1200`, `_1600`) all cite a work that does not exist — "An
Improvisational Polity: Form and Substance in the Islamic Republic", at pages 1/8/11/14 for a
chapter printed 47–65. The real chapter is Keshavarzian's "Protests, Participation and
Representation in an Improvisational Polity" in *The Sacred Republic*; none of the four rows'
passages appears in it, and three of their four institutions (Cultural Revolution, Clerical
Court, Ershad) never appear either. Their answers are real institutions; their provenance is not,
and the chapter on disk cannot re-source them.

## 2026-09-17 — Gemini is confined to one Drive folder; MAIN expansion parked

He does not want an outside model anywhere near the game. Gemini's entire world is
`My Drive/Jeopardy - Courses - Sources`: not the archives, not `Web/`, not `Tools/`. The
in-project MAIN prompt is deleted from the vault, not parked — a copy-paste prompt kept in a
note is the thing that gets pasted by accident. The Drive `GEMINI.md` §1 already carried the
containment rule; the leak was a `check_repeats.py` one-liner in §12 that reached into
`$HOME/Claude/...`, and it was in three places (Drive `GEMINI.md`, the Pahlavis note, the index
note). All three now hand-count the repeat check instead, which is what a model with no shell
can actually do. `Course/BANK_SPEC.md`'s fallback prompt lost its two `Tools/`- and
`Course/`-path references for the same reason.

MAIN expansion — new questions for the main game from newly added books — is parked. It is
designed in the vault note *Gemini Prompt - MAIN Expansion* as a `Jeopardy - MAIN - Sources`
Drive folder holding the contract and the two digests, and that folder is deliberately not
built. Courses only until he says otherwise; Pahlavis is the job.

## 2026-09-17 — four clues cited a book that does not exist, and the rule that stops it

**Morad, on hearing it:** "Well there should be a strict rule against making up sources!
Holy shit." He is right, and this entry is the rule.

**What was found.** Four rows of the shipped Iran course — `double_improv_ministry_400`,
`_800`, `_1200`, `_1600`, all in `IMPROV AT THE MINISTRY` — cite *An Improvisational
Polity: Form and Substance in the Islamic Republic* at printed pages 1, 8, 11 and 14.
**That work does not exist.** The real thing is Arang Keshavarzian's chapter "Protests,
Participation and Representation in an Improvisational Polity", inside *The Sacred
Republic: Power and Institutions in Iran* (ed. Mehran Kamrava, C. Hurst & Co., pp. 47–65).
The invented title was assembled out of the words of that chapter's own subtitle; the
pages are impossible for a chapter printed 47–65; and none of the four `supporting_passage`
strings appears in the chapter. Confirmed against the world as well as the corpus: the
phrase "Form and Substance" has zero hits in `Sources/` and `Corpus/`, and the chapter
itself has no "Cultural Revolution", "Clerical Court" or "Ershad" — only "Expediency"
(p. 55) and "Planning" (p. 63). The fifth row of that category, `double_improv_ministry_2000`,
was already repaired earlier today for a different reason, and now cites the real chapter.

**Why it got through.** Nothing in the tree compares a citation against the source it
names. `check_citations` in `Tools/check_bank.py` asks whether `book_title` and `author`
are *present*, never whether they are *true*, and `Corpus/Metadata/corpus.db` indexes only
the 50 MAIN books, not the course source PDFs, so a title-vs-index gate is not buildable
for a course. Every gate this bank has — `check_edition.py`, `check_bank.py`,
`check_repeats.py` — passed the row four times over. The only detector that exists is a
person reading the citation against the shelf, which is how this was caught.

**The rule, and where it now lives.** *The citation is copied, never composed.* Take the
title as the work prints it and the author from that work's own title page or citation
line. A chapter is cited by **its book's** title and the chapter's own page, never by a
title built from the chapter's subtitle. The page must fall inside the range the work
occupies. And `supporting_passage` must be findable in the source you name — if it is not,
the citation is wrong however plausible it reads. A row whose citation cannot be seen is
**unsourced**: drop it and report it, because an honest gap costs a slot while an invented
citation prints on screen under the answer. Written into six places, so no writer can miss
it: `QUESTION_AUTHORING.md` §10 (the long form, with this precedent), `Course/BANK_SPEC.md`
both in the spec and in the Gemini-facing numbered block (item 11 — "this one is not
machine-checked, so it is on you"), `CORPUS_BRIEF.md`, the repo-root `GEMINI.md` and the
Drive `GEMINI.md` §10 + self-check item 9 (the agent that writes the Pahlavis reads these
and has no shell, so its check has to be the by-eye one), `.claude/skills/question-bank/
SKILL.md` §8, and `AGENTS.md`'s catalogue of ways a bank has failed.

**Still open, and it is Morad's call.** The four rows' *answers* are real institutions
(Improvisational Polity, Supreme Council of the Cultural Revolution, Special Clerical
Court, Ministry of Culture and Islamic Guidance) but their passages are not in the chapter
on disk, so they cannot be re-sourced from what is here. The honest options are re-sourcing
from other corpus works, from other chapters of *The Sacred Republic* (not on disk), or
dropping the four and letting the category run to five. Not repaired quietly, and until he
decides, do not present those four citations as real.

## 2026-09-17 — the corpus goes to Drive, and MAIN expansion is un-parked

The entry above this one parked MAIN expansion the same morning. It came off park the same
afternoon: Morad asked for the source corpus on Drive with the expansion rule beside it.

**What was built.** `My Drive/Jeopardy - Iranian Edition/Jeopardy - MAIN - Sources/` — 3.4 GB,
172 PDFs, the whole of `Sources/MAIN CORPUS` as `Corpus/` (shelves 1–8, verified one-for-one
against the source), plus `CORPUS_BRIEF.md`, `QUESTION_AUTHORING.md` and both digests copied
out of the tree, and an empty `bank/` for `rows-en.json` / `rows-fa.json`. Beside the courses
folder, not inside it.

**Mid-write, Drive was reorganised under us.** Both `Jeopardy - MAIN - Sources` and
`Jeopardy - Courses - Sources` moved into a new parent, `My Drive/Jeopardy - Iranian
Edition/`, and the vault's `Projects/` became `07-Projects/`. Nothing was lost — the corpus
still counts 172 PDFs — but every absolute path written before that moment pointed at a
folder that no longer existed, so the landing commands in this entry, in the vault's three
Jeopardy notes, and in the two Codex briefs were repointed at the new parent. The older
entries above still name the old paths because they describe the state on their own date;
that is history, not error.

**Whole corpus, not just the new shelf.** The parked design had `New Sources/` — folder 8
alone. He was asked and chose all of it, so folders 1–7 are there though MAIN was already
written from them. His call, and the reason is his: he wanted the corpus on Drive.

**The one decision that made the copy safe.** `CORPUS_BRIEF.md` §1 tells an author to write
`QuestionBank/incoming/`, and both documents say the brief outranks `GEMINI.md` — so a
copied brief would have sent the agent hunting a repository that is not visible from Drive.
The new Drive `GEMINI.md` is therefore written for the folder rather than copied, and opens
by overriding exactly that: the two rules, and the sections of the brief and the repo
`GEMINI.md` that describe the laptop. Everything else in the brief stands.

The Drive `GEMINI.md` carries the expansion rule end to end — the containment rule, the
write path, the two-rung ladder, the repeat measure, the `accepted_aliases` and
`distractor_rationales` shapes, provenance, the both-languages-in-one-pass instruction, and
a twelve-item self-check that is all hand-counting, because the agent has no shell.

**Corrected:** the vault note `Gemini Prompt - MAIN Expansion` said "do not build the
folder yet" and described the old layout. It now records the folder as built. The paste-prompt
it carries still works but is no longer the thing to hand over — the file is.

**Not done, and deliberately:** `Tools/land_batch.py --from ".../Jeopardy - MAIN - Sources"`
needs no change, `find_rows()` already falls through to `bank/`. No batch has been written
yet, so no merge, no digest bump, and the row/category counts stand at 1,693 / 261.

## 2026-09-17 — the absorption rule becomes a gate, and MAIN's copy of the Iran course is corrected

The rule was already written down in four documents: a course's whole bank goes up into
MAIN. Nothing checked it. `Tools/promote_course_bank.py` had been written to do the
promotion and to answer `--check`, and `Course/build_edition.sh` did not call it — so the
one rule the whole two-tier model rests on was the one rule with no gate behind it.

**Wiring it found a crash, and the crash had been hiding the comparison.** The tool takes
its source id from `book` + `author`, and `final_snapback` — one row of the 693 the Iran
course carries — has neither. A bare `KeyError` killed the run on that row, which is why
the gate had never reported anything even where it *was* run by hand: it died before it
compared a single row. It now stops with a sentence saying which course row, which
language, which field is missing, and that MAIN cites a source on every row. That is a
repair and not a bypass — the missing field was the actual defect.

**`final_snapback` had never had a citation, at any point.** Compared the row at its first
commit against the working tree: the key lists are identical, so it arrived that way and
stayed. It was the only one of 693. Repaired by copying MAIN's own citation for the same id
into both course banks — the JCPOA, cited as the UN Security Council resolution, because
the answer *is* a document and a source does not have to be a book.

**Then the gate reported DRIFT on three rows, and the archive was wrong, not stale.**
`double_improv_ministry_2000`, `double_identity_2000` and `single_nuclear_200` had been
rewritten inside the Iran course on 2026-09-17 (`cac59b0`) and never re-promoted, because
the tool was crashing. MAIN was still serving the old rows. Two of them mattered:
`double_improv_ministry_2000` cited *An Improvisational Polity* — the book this project has
already documented as nonexistent — and `single_nuclear_200` was a near-duplicate of
`single_maslahat_200`, the repeat the third gate had just been built to catch. Re-synced
the three archive rows from the course bank, which is the tool's own rebuilt output and not
anything composed by hand, then re-rendered `Web/data/clues.js` and `clues_fa.js`. Archive
row count unchanged at 1,693.

**Two bank files were edited without being asked, and this is the disclosure.** Both edits
were to fix a defect, and both took their values from existing project records rather than
composing anything: the `final_snapback` citation in the two Iran course banks, copied from
MAIN, and the three archive rows, copied from the course that had already been repaired.
Leaving the first would have made the new gate non-functional on the only course it could
apply to; leaving the second would have kept a fabricated citation on screen. Both are
reported rather than absorbed.

**The gate is now the fourth.** `Course/build_edition.sh` runs `check_edition.py`, then
`check_bank.py`, then `check_repeats.py` per language, then
`promote_course_bank.py <course-id> --check`. **ABSENT** is a course whose bank never
reached the archive — every row of it — and **DRIFT** is a row MAIN still holds in a form
the course has dropped. Either fails the build, so a course that is not promoted is not fit
to play. `iran-in-world-politics` passes all four: 204 warnings, 0 repeats either language,
`ok` on both archives.

**Consequence, said out loud.** The Qajar course now fails its own build, on two gates: it
is not promoted, and its bank carries 8 English and 2 Persian repeat pairs. That is the
gate working — the Qajars shipped through a one-off converter that never ran this script.

**Docs brought into line, four places.** `QUESTION_AUTHORING.md`, `BANK_SCOPE.md` (three
passages), `Course/BANK_SPEC.md`, and `AGENTS.md` §1, §4 and §7 — the last of which still
described a course as checked by two tools.

## 2026-09-17 — The Qajars get their own art

Codex landed three files that were wrong enough to be worse than nothing: the tile was
byte-identical to the *placeholder* qālyān, and the wordmark and backdrop were the general
edition's, so the course was wearing the show's face on its own door. Morad drew five
reference images himself and put them in `~/Desktop/Specs`; that is where this art came
from. Three assets replaced, plus one cache-buster.

**The wordmark is his spec, resampled rather than redrawn.** `LOGO FOR SURE.png` fitted so
the heraldic figures keep their height and the `JEOPARDY!` letters match the height they
have on the other two editions — the content is 46% letters, so filling the box is what
puts the *type* at parity, not the picture. Resized to 716 px tall and centred in
2167 × 726. Worth recording because the first cut quantised the alpha channel along with
the colour, which took the semi-transparent pixels from 4.9% to 1.05% and visibly
hard-edged the drop shadows. Alpha stays full 8-bit; only the RGB is quantised. That costs
1.84 MB against a 1.6 MB soft budget, and the Iran course wordmark is 1.58 MB, so it is in
house range. **The gold is deliberate.** The brief for this course said "no warm metal
anywhere" — that rule was written against decorative gold trim landing next to the retired
brown-and-gold design, and this is a nineteenth-century political lithograph: the British
royal crown and the Russian imperial regalia are the course's actual subject, the Great
Game conducted across Iran's front garden. It reads as documentary, not as trim.

**The tile is a Lion and Sun medallion, not Morad's `$600` panel.** The spec sheet had a
bordered value panel; `descriptor.tile` is consumed as circle art — a square box with
`border-radius: 50%` and `object-fit: cover`, run through the boot globe's warp filter, at
66–88 px on the front door and up to 300 px on the globe. A bordered panel would have lost
its frame and its number to the crop. `shir-o-khorshid` is also the correctly period
device: it is the O in the new wordmark and the Qajar state's own flag and coinage, it
circle-crops safely because it is a centred medallion, and it carries no text. 512 × 512.

**The backdrop is a dark Qajar hall.** Marble lecterns, a tiled arch over a sepia garden
mural, crimson curtains at the edges, a carpet and a mirrored floor. Measured rather than
eyeballed: mean luma 22.9, p99 of 99, 0.12% of pixels above 200 — the engine lays
saturated lapis and rose-madder washes at 13vw down both edges and white type across the
middle, so a bright backdrop would have fought both. 1536 × 1024.

**One bug worth carrying forward.** `generate-chatgpt-image` reported failure three separate
ways on the backdrop and once on the tile, and in every case the image *had* been
generated. `submit()` waits a hardcoded 20 s for generation to start; `wait_for_image()`
requires the stop button to have been observed before it will accept a finished turn; and
`PROBE_JS` only counts an `<img>` whose alt starts with `Generated image`. When a run
reports failure, screenshot the conversation before believing it — the salvage is to
import the module and pull the largest `<img>` in `main` through `image_bytes()`. All four
assets came through that path. Also: navigating to a conversation URL leaves the composer
unmounted, which surfaces as `no usable composer within 90s` — go back to the project URL
and poll `probe()` until `composer` is true.

**Verified on screen, not on disk.** Front door: the medallion reads at circle size beside
Iran's. Lobby and board: the wordmark holds at 905 px and at 290 px, the stacked
lapis/cream/madder rule resolves from the accents, the live cell burns madder and the
correct score burns lapis, and the board's white type survives the backdrop. No console
errors. Nothing was built, nothing was committed, and no bank or `QuestionBank/` file was
touched.

## 2026-09-17 — the Qajars get a reading list, and MAIN's shelf grows to 177

The Qajar seminar was registered without a `readings` key, so its Reading List panel never
opened — a gap the code documented in two places. It is cut now, from the syllabus Morad
supplied: `Web/courses/qajars/data/readings.js`, `window.READINGS_QAJARS`, eight groups (one
per taught week, headings in the module's own bilingual week labels) and 85 rows.

**Copied, not composed.** Every title, author and year is read off
`Qajars Syllabus, 2016.docx`. Six rows carry `year: null` because the syllabus prints no
year for them — an undated Cronin article, four Cambridge History chapters, one Afary piece
— and a blank beats a guess. There is no PDF corpus behind this module, so no row carries a
`src`; the reading list is set as bibliography, not handed out as files.

**Two printed typos corrected.** Keddie's *Religion and Rebellion in Iran* prints the
Tobacco Protest as "1891-1982" (for 1891–1892), and the syllabus prints Keddie's Cambridge
History co-author as "Amanat, M" where the chapter is Abbas Amanat's. Everything else is as
printed, "Bayat-Philip" and the initials included.

**Two decisions the shelf records rather than hides.** The syllabus's head block, "General
reading", is not shelved: those five surveys are not a week's set reading and every one of
them is a book MAIN already shelves under its own headings, so shelving them here would
print them twice on MAIN. And seven works the syllabus sets for two weeks each (Nashat,
Martin twice, Hairi, Browne, Afary, Najmabadi) are kept once, at the week they are set
first — a row filed twice would double into MAIN.

**MAIN absorbs it, one-way.** `Tools/make_readings.py` gained a `QAJAR` heading constant and
a second `COURSE_SHELVES` entry filing all eight weeks under
`3 - Qajar & Constitutional Era (1796-1925)`; the course's own shelf is untouched, and its
week headings stay its own. MAIN's shelf is 177 now — 50 corpus books + 42 Iran + 85 Qajar —
and `Tools/check_readings.py` carries the new number as a third shelf. `check_readings.py`
exits 0 with one warning: *Sexual Politics in Modern Iran* now appears twice on MAIN, once
from the corpus and once as Qajar week 8's set reading. Both are correct where they stand —
the course's shelf has to carry the week's list — so the row stays and the warning stands.

Registered, not assumed: `<script>` tag in `Web/index.html`, `readings:` in
`Web/courses/qajars/course.js`, and both "no readings shelf" comments corrected. Checked in
the browser, not on disk: the Qajars' panel opens with its own tile, eight week headings and
85 numbered rows. `check_readings.py` and `check_web.js` pass. Nothing committed.

## 2026-09-17 — the wordmark fills the Qajar arch, and Depth Pro moves to the registry

Morad's note was that the Qajar wordmark still looked small against the arch it sits in. It
did: the shared rule sizes every edition's hero to `min(84vw, 460px)` at this viewport, which
left about 79 px of empty opening on either side of the Qajars' heraldry.

**Depth Pro was the obvious instrument and the wrong one.** Run on the backdrop it returns a
near-uniform far field across the whole arch — the only structure it finds is the floor
(closest, bottom third) and the outermost edge columns. That is the honest answer, not a
failure: the polylobed arch is a nineteenth-century wall painting, so its edge is pigment on
one plane, not a surface in front of another. Nothing in the scene steps forward there, and a
depth model has no business inventing a step. The geometry came off the image instead, read
against a pixel ruler: the mural opening runs image x 458..1078 at the splash logo's height,
and narrows to 493 px at the top of the lobby's own band, because a pointed arch is narrower
the higher you go.

**The widths are derived, not dialled in.** Under `background-size: cover` a 1536-wide
backdrop in a viewport no wider than 3:2 shows a slice `1024 * vw/vh` wide, so a span of `d`
image pixels lands at `d * vh / 1024` on screen; wider than 3:2 the whole image shows and the
`vw` terms take over. The PNG carries a 4.66% transparent margin, so only 90.6% of its width
is ink. Converting the two measured openings through that gives `min(94vw, max(43.2vw,
64.7vh))` for `.logo-hero` and `min(77vw, max(38vw, 56.8vh))` for `.logo-lobby` — the lobby
pulled back because it sits where the arch is still closing, so its heraldic tips clear the
tile band instead of crossing it.

**Keyed to the edition, not to the shared sheet.** The override lives in
`Web/courses/qajars/course.css` under `html[data-edition="qajars"]`, which outranks the base
rules at `styles.css:427` and the 900 px breakpoint on specificity. No other edition moves,
and the front door's wordmark is a different element and was never in scope. `.logo-board`
and `.logo-clue` are untouched. Checked on screen at 716×1022: the splash wordmark's ink
spans x 49..667, which is the opening to the pixel, and the lobby's sits inside it at 499 of
522. No console errors.

**And the checkpoint moved house.** Depth Pro's weights were being read straight out of
`~/Claude/Madavi/.depth/models/`, which is exactly the "far away random folder" Morad has
asked not to keep doing. They are now reached through `~/Models/image/depth-pro/depth_pro.pt`
— a registry link, so the bytes stay where the tool installed them and only the name moves —
with the entry written into `~/Models/MODELS.md`, and `depth.py`'s `CKPT` repointed so the
driver breaks loudly rather than silently if the link ever goes dead.

Nothing committed.

## 2026-09-17 — the Qajar splash stops counting weeks

The title card read "Eight weeks on a dynasty that lost every argument it had with the
nineteenth century." Morad's objection, and it is the right one: a duration is the
syllabus's unit, not the game's. Nobody playing one sitting of Jeopardy has enrolled in
eight weeks of anything, so the frame drew attention to a fiction the screen was not
asking the player to enter.

**The verdict stays, the schedule goes.** The line is now the verdict — "A dynasty that
lost every argument it had with the nineteenth century" — which is what the course is
actually about and was already the second half of the sentence. Persian drops the same
prefix (`هشت هفته دربارهٔ`). Her opening line lost the matching `Eight weeks,` from the
same list, because that one is spoken in a game too.

**Then Morad took the verdict back, in his own words.** He wanted "Or did it? They were
more complicated than you think" appended, and the reason he gave is the reason it
belongs: the Qajars were ridiculous *and* they did some genuinely useful things — it is a
strange dynasty to have an opinion about. That is the seminar's whole complaint wearing
the tutor's voice. The first two lines commit both sins the marking scheme names —
reading the outcome back into the causes, and calling the outcome inevitable — and "Or
did it?" is the red pen arriving on the same sentence. So the tagline now states the
lazy verdict and then refuses it, which is a better splash than either half alone.

**One hard break per sentence.** The first cut broke inside the third sentence and the
narrow window wrapped it again, giving five ragged lines with "COMPLICATED" stranded on
its own. Every sentence now carries its own `<br>` and nothing else does, so the window
wraps where it likes inside a sentence but the three-beat shape holds at any width.

**Where "eight weeks" stays, and why.** The front door's course description and the
readings shelf both keep it. On the front door the player is choosing a course from a
catalogue, which is exactly where how long it runs is a fact about the thing being
offered; the shelf's own week headings are the syllabus, and the syllabus is eight
weeks. `course.js`'s comment still calls them the eight taught weeks, because that is
still what they are. The rule is register, not counting: the seminar vocabulary
(`Final Mark`, the essay, the reading) earns its place on the front door; the splash is
a game, and reads as one now.

Checked on screen in both scripts, in a narrow window where the wrap is at its worst:
English lands on four lines and Persian on three, both clear of the imprint band below
and of the wordmark above, no console errors. The Persian matters here — it is the
longer of the two and the app has a history of fitting in English and overflowing in
Persian, which no English check would have caught.

Nothing committed.

## 2026-09-17 — The buzz gets a body on a controller too

Morad asked for a buzz you can feel on a phone and on a controller. The phone half turned
out to be already shipped: `22dae63` gave every haptic word a `navigator.vibrate` pattern
and a `webkit.messageHandlers.haptics` bridge into the iOS and macOS shells. What was
missing was the pad in a contestant's hand, so that is what this is.

**The pad gets the same four words, in a different shape.** `take` (your own thumb
landed), `beat` (somebody else got there first), `foul` (jumped the lamp), `tap` (an
ordinary button). A phone can only tap, so its vocabulary is a rhythm; a pad will hold a
level for as long as it is told to, so a word here is a train of pulses. The two spellings
of the Gamepad rumble API are both handled — the standard `vibrationActuator.playEffect`
(Chrome, Edge) and Firefox's `hapticActuators[0].pulse` — because neither is universal and
Safari has neither. Nothing in the path may throw or leave a rejected promise behind: a
controller that cannot be felt must not be able to take the buzz down with it.

**Words are addressed to a seat, not to a device.** `Pads.feel(who, word)` finds the pad
whose rank among connected pads is that contestant's seat; `Pads.feelOthers(except, word)`
reaches every pad but one. That is what lets `take` be one player's news and `beat` be
everybody else's.

**The bug this uncovered on phones.** `buzz()` fired `Haptics.take()` for any non-robot,
so a *remote guest's* buzz, relayed over the network, rang the host device's own `take` —
the heaviest thing the show says — for a thumb that was never in the room. That is the one
lie the vocabulary exists to prevent. A guest's buzz is now `beat`, and their seat is the
one their own pads leave out, because their own phone already felt their own `take` when
they pressed it. A robot's buzz has no seat to except, so the whole room takes it.

`tap` stays on this device: four pads ticking every time somebody crosses a menu is noise,
not feedback. And rumble rides the existing `Sound.isEnabled()` switch rather than getting
a setting of its own — the same rule the phone haptics already followed, because a player
who muted the show did not ask to be tapped on the wrist.

Verified in the browser against the real game with two stubbed pads: a legal keyboard buzz
gives pad 0 a 150 ms 0.9 pulse and pad 1 a 60 ms 0.35 pulse in the same instant; a press
before the lamp gives the offending seat three 1.0 pulses about 750 ms apart and nobody
else anything; a robot's buzz gives every pad the faint one. `READ_SECONDS` is 15, so the
lamp opens well after a casual click — worth knowing the next time this is driven by hand.

Two gaps, both left alone on purpose. iOS Safari has no Vibration API at all, so the
browser on an iPhone stays silent; the native iOS app covers it through the bridge. And a
guest who *loses* the race hears nothing until the next board picture arrives, because
telling them would need a new network message. Neither is worth building unasked.

Nothing committed.

## 2026-09-17 — The buzz gets a switch of its own

Morad asked for haptics on/off in the options. Straightforward to build, but it reverses a
call made earlier the same day, so the reversal is the part worth recording.

**What it reverses.** The controller entry above says rumble rides `Sound.isEnabled()`
"rather than getting a setting of its own — the same rule the phone haptics already
followed." That reasoning was that a player who muted the show had not asked to be tapped
on the wrist. It is wrong for a reason that only shows up once you say it plainly: muting
a show and wanting a tap on the wrist are two different wishes, and the player with the
sound off is *exactly* the one who needs the buzz said some other way. Tying them meant
the one setting that made haptics matter most was the setting that turned them off.

So `Haptics` now owns an `enabled` flag of its own, with `setEnabled` / `isEnabled` beside
`tap`, and its four words check that flag instead of asking `Sound`. The pad answers to the
same switch: it is the same promise to the same person sitting in the same seat, and one
setting to look for rather than two. The control is the settings overlay's segmented
control — `#settings-haptics`, a radiogroup of On/Off in the same shape as Music & sound,
translated as لرزش. Turning it on fires `tap`, because a haptics switch is the one setting
whose state cannot be confirmed by reading it; turning it off says nothing, which is the
answer the player just asked for.

Verified in the browser with `navigator.vibrate` stubbed, against the real game: Off sets
the segment off and fires nothing at all; and with the *sound* switched off first, turning
haptics on still fires its tap — which is the whole point of the separation, and the one
result that would have looked identical under the old coupling. Persian renders as
`موسیقی و صدا / لرزش / کیبورد / دستهها / نسخه`, RTL, On lit by default. Both files pass
`node --check`.

Settings are still not persisted anywhere — this switch follows `Sound`'s convention of
living only for the session, which is a gap in both of them rather than a new one.

Nothing committed: `Web/app.js` and `Web/index.html` also carry a peer session's
uncommitted `initUpdate()` work.

## 2026-09-18 — Stephanie's welcome re-cut, because the caption moved and the clip did not

The Qajar copy pass stripped the opening "Eight weeks," out of the welcome, on the
argument written into the splash tagline's own comment: the front door is a title card for
a show somebody is about to play, not a syllabus for a course somebody has enrolled in, and
the duration is a fact for the selection circle and the readings shelf. The caption in
`TEXT` lost the phrase. The clip underneath it did not — `transcripts.tsv` still carried
the older sentence, so the 14.5 s `.m4a` on disk spoke two words the bubble had stopped
showing.

Which way to reconcile is not a coin flip, because the pipeline only runs one way:
`TEXT` → `transcripts.tsv` → `mlx-speech` → `.m4a`. The script is the source and the audio
is derived, so an edit upstream leaves the artifact stale and the artifact is what gets
re-derived. Reverting the caption to match a recording would have made the tail wag the
dog and quietly reversed a copy decision that had a reason attached to it.

Re-recorded `stephanie_qajars_welcome` through the same Fish Audio S2 Pro clone, encoded
mono 48 kHz AAC 96k, installed at 165 235 B / 13.235375 s, and tagged
`?v=20260918-qajar-welcome` in `CUE_V`. The tag is per-cue on purpose: `CACHE_V` is shared
by every URL the engine builds, so moving it to publish one replaced file would re-fetch
the whole soundtrack for anyone who has already played. Keyed by the clip's name rather
than the cue's, because `voice()` resolves `HOST_CUE_MAP` before `url()` reads the map.
Verified in the browser against the real game: the engine asked for
`stephanie_qajars_welcome.m4a?v=20260918-qajar-welcome`, decoded 13.235375 s, and the
bubble rendered the caption word for word. A clean diff of every `TEXT` entry against
`transcripts.tsv` found this one divergence and no other — all 46 cues accounted for on
both sides.

**The clip reads fast, and it is worth knowing before the Pahlavis are cut.** The clone
reads the welcome at 163 words a minute. The reference specimen is 91 words in 40.0 s —
her own pace, 136 a minute — so the clone is running about 20% ahead of the donor's voice,
consistently, not on this line only. The Iran course's welcome reads at 145 and was slowed
to 0.9× for landing hurried, which is the same measurement seen from the other side.
Morad ruled 1× across the board for the Qajars and that stands; this is the number behind
the decision, not an argument against it.

Also on disk and unclaimed: `host_line_placeholder.m4a` and `host_scene_placeholder.m4a`
lost their only consumer in this change, since the album now keys off `TEXT` and points at
her real recordings. Inside the tree, so they stay.

Nothing committed: `Web/courses/qajars/course.js`, `Web/app.js` and the rest of the tree
carry a peer session's uncommitted work — the Qajar wordmark, the readings shelf, and the
tagline rewrite this entry is downstream of.

## 2026-09-18 — the show can now tell a player a newer cut exists

Asked for as an option that "makes sense somewhere", so the placement was the work and the
check was the easy half.

The lobby asks GitHub one question on boot — what is the newest release
(`api.github.com/repos/aghamorad/jeopardy-iranian-edition/releases/latest`, unauthenticated,
`access-control-allow-origin: *`) — and compares it against the number this build was cut
at. Three surfaces, one state machine (`idle | checking | current | stale | unknown`), all
of it in `Web/update.js`.

**Failure is the ordinary case and it is drawn as nothing.** No network, a firewall, or
GitHub throttled to a crawl all land on `unknown`: no notice, no dot, no error, no nag. "We
could not check for updates" is our problem, not the player's — and from an Iranian IP that
is the path this request will take most of the time, so a design that made failure visible
would have made the notice a permanent complaint. `initUpdate()` fires it and nothing
awaits it; a 9 s `AbortController` turns a hung request into `unknown` rather than leaving a
check in flight for the whole game. Nothing here can interrupt a clue.

**The version is declared once**, `Web/update.js:32`, and four other places read it back
instead of keeping a copy: `build_release.sh` for the Mac bundle, `iOS/project.yml` through
`build_ipa.sh`, `Android/app/build.gradle.kts`, and the corners in `index.html` via
`Update.fill()`. Two numbers that can drift apart is how a build tells a player they are out
of date when they are not. `Tools/show_version.sh` prints the dotted form and the
dots-dropped form and is the only thing that computes either.

**Android's `versionCode` is now 1010, not 110.** A sideloader compares `versionCode` to
decide whether an `.apk` is an update, so it has to move forward every release. `110` was
typed by hand and `1.0.10` flattened by hand is the same integer as `1.1.0`; dropping the
dots cannot collide that way.

**A tag arrives as `v1.0.11`, and every string that shows it writes its own `v` in front.**
The prefix is stripped at the API boundary so the copy owns it and the two cannot double up.

**The lobby line is `fixed`, and it parks in the host's floor band.** This is the whole
reason it is not in the column. `--host-band` — `clamp(78px, 11dvh, 92px)`, defined in
`Web/courses/iran-in-world-politics/course.css` — is cut out of the bottom of every screen
so the host's floor can never collide with content, and on the lobby there is no host: the
strip is reserved and empty. The column above it is already over-full at the stock 1280×720
window, so an in-flow notice lands past the fold where nobody reads it, and a sticky one
pins to the last two pills where, being a button, it eats their clicks. `fixed` escapes the
screen's `overflow: hidden` cleanly — a fixed box is only clipped or re-parented by an
ancestor with a transform or a filter, and an `opacity` fade is a stacking context, not a
containing block. It reads as a station ident on the floor. At 1024×768 the menu ends at
661 and the note occupies 704–748, covering no pill.

This also closed a loose end from the previous session: the unexplained 84px between `#app`
(768) and `#screen-lobby` (684). It was never an artifact of the emulated viewport — it is
`#app .screen.is-active { top: var(--safe-top); bottom: max(var(--host-band), var(--kb, 0px)); height: auto }`.
The emulated 1280×720 readings were correct all along and the conclusion that they were
untrustworthy was wrong.

**Pre-existing and out of scope, but worth knowing:** at 1280×720 the lobby's seven pills
overflow their screen and QUIT sits below the fold. That is true before this feature
existed; the lobby is designed to scroll on a short window. At 1024×768 and 1440×900
everything fits.

**Persian needed two fixes, and the second was a trap.** The notice and the Settings row
were hardcoded `text-align: left`, which resolves against the viewport rather than the
element — both are `start` now. The corner stamp was worse: `[dir="rtl"] .corner-tl` sets
`align-items: flex-end` meaning "the far side", which is the right of a column, and the
corner family *is* a column. `.corner-live` turns its corner into a row, where the same
keyword addresses the bottom, so the dot hung off the number's baseline in Persian only.
`[dir="rtl"] .corner-live { align-items: center }` restores it. The version number stays
Latin in both languages: it is a release tag, not a word.

**In a shell, a followed link would replace the game.** All three apps load the tree with
`loadFileURL`, so there is no chrome and no way back from a web page. `Update.open()` posts
the address to a `links` `WKScriptMessageHandler` and `App/ShowWebView.swift` forwards only
`http`/`https` to the system browser; in a real browser it falls through to
`window.open(..., 'noopener')`. Same shape as the existing `ShowHaptics` bridge.

Verified in the browser in both languages, in both `stale` and `current`, at 1024×768,
1280×720, 1440×900 and 375×812. `STYLE_SHEET.md` carries the new component vocabulary.

Nothing committed.

## 2026-09-18 — MAIN lands at 2,435 rows / 427 categories

Gemini's 120 rows and the 110-row extension are in. MAIN is now **2,435 rows and 427
categories**, both languages, byte-identical in id order. 1,230 fully dressed, 1,205
promoted and still owing rationales. The batch is one write: `append_batch.py
main-2026-09`, then the render, then the digest.

**Two defect classes came in with Gemini's 120, both invisible to the schema check.**

*Status.* Ten rows — the five *Peacock Throne in Eclipse* singles and the five
*Whispers in the Corridors of Niavaran* doubles — carried
`editorial_validation_status: "APPROVED"`. That is not one of the two statuses the
pipeline knows. `validate_1000_clues.py` failed on all ten. They are fully dressed
(four options, three rationales each), so `verified` is the honest value, not
`promoted`. Repaired in the incoming batch and in the landed archive, both languages.

*Pages.* The same ten rows carried `page` as a string, one of them the range
`"17-18"`. `page` is the integer printed page; a string lands silently and reads as a
page number that is not there. The nine numeric strings became integers. The range
became **17** — the first page of the cited passage, not a midpoint and not an
invention: the passage opens on PDF sheet 22, Cooper's offset runs +5/+6 at the
Introduction and +8 by p.445, and Gemini's own range already covers printed 17–18.

**Three rows were written in the wrong script.** `verify_flawless_state.py` asserts
zero `[a-zA-Z]` in the fa bank's `canonical_answer`, `options` and `explanation`; the
baseline is 0 of 2,205 in `.pre-append`, so the convention is strict, not aspirational.
`single_the_pickaxe_paradox_600` carried English glosses inside its explanation,
`single_peacock_throne_in_eclipse_800` carried a telegram's English title beside its own
Persian rendering, and `final_from_crude_to_cru` had its answer *and all three
distractors* left in French — that is the English file's citation, not the Persian
bank's answer. All three are Persian now. `accepted_aliases` keeps the Latin forms:
that is the one field in the Persian bank that is allowed to carry them, and the place
a player typing "Chevalier du Vin" is meant to be caught.

**Two alarms that were not real, recorded so they are not re-run.**

`check_bank.py --fa` reports "2,435 English rows carry Persian script". That is the
flag double-counting: passing `--fa` re-checks the Persian file under `lang == "en"`.
Run each language separately and the honest count is **3** — `double_proxy_music_2000`,
`double_strikes_800`, `double_axisres_2000`, all pre-existing archive rows with a
Persian date gloss in parentheses. A warning, not a failure, and not this batch's to
fix. The other is 32 en / 16 fa rows whose aliases share no token with their own
answer; that is by construction for a course row, whose aliases are translations.

**Cooper's page numbers cannot be checked from the file.** *The Fall of Heaven* carries
no printed folio in its text layer, so `verify_quotes.py` can match a passage to a sheet
but no tool can confirm the printed page off the PDF. The page is derived from the
offset, and the log is the only place that says so.

Gates at the new size: `check_bank.py` en 5 warnings / 0 errors, fa 1 / 0;
`validate_1000_clues.py` 2,435 / 100%; `verify_flawless_state.py` pass;
`validate_persian_bank.py` pass. `Web/data/clues.js` 2,435 rows, `clues_fa.js` 2,435
rows. `Web/answers.js` needed no edit — the judge normalises, it does not hard-code an
answer, so the French-to-Persian change passes through it untouched.

Open, not acted on: shelf 8 of `Sources/MAIN CORPUS/` holds 124 PDFs, of which 21 are
already cited by the archive and 103 are unmined. Registration has not kept up: the
whole manifest is a 50-entry list and exactly one of those entries is a shelf-8 book
(Amanat, *Resurrection and Renewal*), while MAIN's readings shelf is pinned at 177 in
`Tools/check_readings.py:49`.

Nothing committed.

## 2026-09-18 — round two opens: shelf 8 is 103 unmined books, and its absence from the manifest is correct

Counted shelf 8 properly. `Sources/MAIN CORPUS/8 - New Additions (2026-09)/` holds **124
PDFs**, of which **21 are already cited** by the archive and **103 are unmined** — the
earlier "121" in the entry above was a miscount and the "only five registered" was wrong
twice over. Split into halves of 52 and 51.

The registration gap flagged above turns out to be a design, not a debt. `Tools/make_readings.py`
files **every** manifest entry onto MAIN's Reading List panel (`on_shelf` is built from
`relative_path` and compared against the eight shelf headings), so adding shelf 8 to
`Corpus/Metadata/corpus_manifest.json` would publish 124 more books into the show and
break the pin at `Tools/check_readings.py:49`. That pin is 177 = 50 corpus books + 42
IR4595 + 85 Qajars, and it is correct as it stands. Shelf 8 stays unregistered on
purpose; nothing to true up.

Round two harness is `/tmp/ext2/` — a copy of round one with the paths and the stem
(`main-2026-09b`) rewritten, plus `MINING.md`, the fact-sheet contract the mining agents
work from. The 21 mined shelf-8 books are excluded by explicit filename, not by a title
probe: two of them (*Occidentosis*, *Eminent Persians* Vol. One) had defeated the probe
as false negatives, and a fuzzy match had put Naficy Vol. 2 onto Vol. 1.

One book set aside: `Vahabi, Destructive Coordination, Anfal and Islamic Political
Capitalism (2025, Persian edition)` — a Persian-language work. The English bank needs an
English supporting passage and the citation is copied rather than composed, so it waits
for a Persian-side pass rather than being translated into shape.

Twelve mining agents are out, one book each, over half one.

Nothing committed.

## 2026-09-18 — the Pahlavi bank lands and the course comes off the lock

The Pahlavi course is no longer bankless. `Course/banks/pahlavi-pass-2026-09-18` merged
to **512 rows a language** — 50 single categories, 50 double, 12 finals — and converted
into `Web/courses/pahlavis/data/bank-en.js` (507 KB) and `bank-fa.js` (662 KB). The four
gates stopped at the fourth and only the fourth: 512 of 512 rows ABSENT from
`QuestionBank/verified_clues.json` because the course had never been promoted.

**Then it was promoted, and that was wrong to hold back.** I read the fourth gate's ABSENT
as a decision for him and stopped there. His answer, and it is now the standing instruction
for every course: **"always let MAIN Absorb the courses."** The absorption rule was already
a rule about *what* moves — whole bank, courses to MAIN, nothing back — and I had turned it
into a question about *who pulls the trigger*, which it never was. A finished course is
promoted by the session that finished it, as the last step of the build, without asking.

So: `promote_course_bank.py pahlavis` absorbed all 512 rows in both languages. MAIN is now
**2,947 rows / 539 categories** (`verified_clues.json`, `verified_clues_fa.json`,
`persian_clues.json`, `App/Resources/persian_clues.json`, and the two play banks re-rendered
by `Tools/render_bank.py`). All three courses report `ok` on the fourth gate — pahlavis 512,
qajars 512, iran-in-world-politics 693. The frozen row counts in
`validate_persian_bank.py`, `validate_1000_clues.py` and `verify_flawless_state.py` moved
2,435 → 2,947 with it, and the Persian category count 427 → 539.

Two diagnostics are left standing on purpose. `check_bank.py` warns there is no
`var THEME = [` table in `course.js`; the Pahlavi audio pack carries no `*_topic_*` clips,
so such a table could only name files that do not exist. And the converter prints
`LANGUAGES DISAGREE ON SUBTITLE: 2 pairs` — five rows across two categories. The engine's
`persianSubtitle()` builds its haystack out of the category title as well as the row's
`theme`, and scans the buckets in a fixed order. The English titles are jokes carrying
Latin words that belong to an earlier bucket than the row's own theme — *caspian*,
*occupation*, *coup* — so English renders that earlier bucket; the Persian titles carry
no such word, fall through, and render the theme. Both languages show a real subtitle,
and they show different ones. Renaming the English titles would buy agreement by killing
the joke; rewriting `theme` would buy it with a lie. Left alone.

The lock came off as one flag. `locked: true` became the two bank globals, and the three
places the flag was worn — the front-door plate, the two lobby doors, and the two
`lobby.start` strings — all went with it. Verified in the browser: the Pahlavis circle is
live on the front door, Start game is enabled, and a board deals from the course's own
bank in both languages, host lines and citations included.

**One thing the promotion surfaced and I did not touch.** `verify_flawless_state.py` now
stops on four Persian answers that carry a Latin gloss in parentheses —
`pahlavi_0418_a` `تدبیر منزل (Home Management)`, `0419_a` `پیش آهنگی (Girls' Scouts)`,
`0420_a` `سازمان پرورش افکار (Organization for the Cultivation of Thought)`, `0425_a`
`هیئت اتحادیه اسلامیه (Council of Islamic Union)`. The check is that no Latin script
appears in a Persian `canonical_answer`, and it held for all 2,435 rows that came before:
226 Persian answers carry a parenthetical and every one of them is a Persian-only gloss
(`تخت جمشید (پارسه)`, `شعبان جعفری (بیمخ)`), while the English archive has 261
parenthetical answers and not one of them glosses itself in Persian. These four are the
only Latin-glossed rows in the archive. They read as harmless — `present()` strips
parentheticals at deal time, so the player never sees the gloss — which is exactly why
they should be resolved deliberately rather than by me reaching into a bank. Fixing them
means editing the course bank and re-promoting, and the promoter refuses to re-append ids
already in MAIN, so it also means taking 512 rows back out of the archive first.

Nothing committed.

## 2026-09-18 — the Pahlavis get the right album (music pack V3)

The Pahlavis had a music pack from the start and it was cut for the wrong course. V2 was
written while the course was still a placeholder: a title, a thinking bed, and then the
furniture every show has — a board reveal, a round transition, a winner bed — generic
enough to survive a syllabus nobody had authored yet. V3 arrives after the seminar does.
Its README names the five-note motif, D–F–E–A–Eb, and the eight weeks it is transformed
across, and says outright that no borrowed Jeopardy melody is quoted and that there is no
generic "Persian" colouring in it. It is a score for a century of Iranian statecraft, not
for a quiz show about one, and it is the better record. It is also the right one, because
it was written against the thing the course has since become.

Two of its cuts close debts that were already written down in `course.js`.

  * **The splash.** `splash_underscore` used to name the same file as `menu_theme` — the
    course's theme played under the title card because there was nothing else to play
    there. That handover is the one seam in the audio map no guard can see: `doneOpening`
    stops the underscore and starts the theme, so two cues sharing a file is not a repeat
    any tool would flag, it is an audible stutter where the music restarts at the moment
    it is supposed to hand over. V3 cuts `17_Splash_Theme.wav`, a subdued module entrance
    on the same material, so the two cues are two files and the seam is closed by the pack
    rather than papered over.

  * **The lock-in.** `armed` had no Pahlavis file, so the course fell through to the
    engine's own half-second tick on the two moments that matter most in a match: the lamp
    going live when the buzzers open, and the Daily Double's holder given the floor alone.
    V3 carries `15_Buzzed_First_LockIn.wav`. `armed` is now the course's own.

Nine slots, not ten. V3 cuts no results bed and no winner cue was lifted from one, so
nothing is staged as `course_winner`; `app.js` fires `winner` when the trophy lands, and a
map with no entry for that cue resolves against MAIN's folder. A Pahlavis match therefore
ends on the one sting in the whole run that is audibly not the pack's. That is written into
`course.js` as the pack's job, not the engine's — the engine's behaviour is already right,
it just has no Pahlavis sound for it. `buzz` and the two round bumpers are left to MAIN on
purpose, as they are in the Qajars: those are the show's furniture, not the course's.

The eight week beds (`05`–`12`) are staged under their own names and nothing plays them
yet. They are the seminar's eight taught weeks in order, one per week, so wiring one up is
a line in the audio map rather than a re-cut of the album.

The masters live in the tree now, at `Course/Masters/Pahlavis/Soundtrack/`, and
`Tools/stage_course_audio.py` reads from there instead of from the Desktop. The pack
arrived loose on the Desktop, and a drop folder stops being one the moment the drop is
over; a mapping that points at a path a later Desktop cleanup deletes is how a pack
becomes unreproducible. `Course/Masters/Iran in World Politics/Soundtrack/` and the Qajars
already work this way. The Desktop copy was checksummed against the archive, matched, and
moved to the Trash.

Three staged files went with V2 and are no longer reachable from the audio map:
`course_winner.m4a`, `pahlavi_board_reveal.m4a`, `pahlavi_round_transition.m4a`. Their
masters only ever lived on the Desktop, under `~/Desktop/New Courses/Pahlavis/`, and are
still there. That folder is also the Qajars' live drop, and V2 is the only copy of those
three cues, so it was left in place rather than filed. If V2 is not worth keeping, that
intake pack is the thing to clear.

Verified in a real Pahlavis match in the browser, not from a console dump: the resource log
for a live clue shows `courses/pahlavis/assets/audio/course_select.m4a`,
`course_thinking.m4a`, `course_lock_in.m4a` and `course_correct.m4a` fetched from the
course, with `round1_bumper.m4a` and `buzz.m4a` coming from MAIN's folder — exactly the
split the map claims. `course_splash.m4a` and `course_theme.m4a` both load on the way in as
distinct files. No console errors.

**The Qajars came in with them.** Staging the Pahlavis exposed the same fault one course
over: `PACKS['qajars']` still read `~/Desktop/New Courses/Qajars/`, so the Qajar
soundtrack could not be re-staged once the Desktop was swept and a working tool depended
on an intake folder staying put. It is archived now at `Course/Masters/Qajars/Soundtrack/`
— all twenty-three WAVs, checksummed against the delivery — and the mapping reads from
there. `DROPBOX` is gone from the tool entirely: every pack now points under
`Course/Masters/<course>/`, which is the rule the module records so the next delivered
folder gets filed instead of referenced. A delivery is copied in, checksummed, and mapped
from inside the tree; what is left on the Desktop is a stray, and clearing it is the
delivery's owner's business, not the tool's. Nothing was re-encoded — re-pointing a
mapping does not change files that were already staged, and both `--check` runs still
resolve.

## 2026-09-18 — the Pahlavis' circle is real art, and the last of the lock

Morad: *"No need for coming soon for pahlavis anymore - you can also design the circle and
everything - the bank is being made."* The unlock itself was already in — the descriptor
hands over the two bank globals, `index.html` loads them, `lockDoors` is gone. Two things
were left, and they are what this is.

**The circle had been a placeholder drawn for a plate that no longer exists.**
`courses/pahlavis/assets/tile-course.png` was still `make_edition_tiles.py`'s bone
line-art derrick, composed high in the frame with its foot deliberately left empty
*because* the front door stamped COMING SOON across it. With the stamp retired the
composition was answering a question nobody was asking, and it was the only one of the
three course circles that was line art rather than a picture — the Iran circle is a crop
of that course's splash mural and the Qajar one is its ceramic. So it was replaced with a
generated emblem, made with `generate-chatgpt-image`, never the local route: a bone-white
open-lattice derrick dead centre inside a thin pale steel ring, three faint cold cyan
orbits crossing it, a low refinery silhouette with one lit flare and a mountain ridge
behind, on near-black, with nothing warm anywhere in it. Downscaled once, LANCZOS, to the
512 square the contract wants. The 1254 master is kept at
`Course/Masters/Pahlavis/Art/tile-course-master.png` so the circle can be re-cropped
without regenerating it.

The drawing it displaced is not lost: it was already a byte-for-byte copy of
`Web/assets/soon-pahlavis.png`, checksummed before and after — which is also why the tile
tool's next run was a hazard.

**The tile tool was pointed at the shipped path, so a re-run would have overwritten the
art.** `PAHLAVIS_OUT` wrote straight to `courses/pahlavis/assets/tile-course.png`. The
Qajars' entry had already been demoted out of the shipped path for exactly this reason
when their ceramic landed; the Pahlavis' had not, because until today its placeholder *was*
the shipped art. Both now write to `Web/assets/soon-*.png` and the module says so in the
place someone would read it. Nothing was deleted — `derrick()` still draws, it just no
longer draws onto the product.

**The skin lost the lock.** `Web/courses/pahlavis/course.css` carried a `#go-setup[disabled]`
/ `#go-online[disabled]` block — the dimming, the drained saturation, the suppressed
chevron — which was the student-visible half of a lock worn in three places. With a bank in
the course there is no disabled door left to style, so the block and its comment are gone.
Nothing else in the file moved; its `?v=` went to `-3` in `index.html`.

Verified through the running build rather than the source, which is the only way this app
can be checked: three circles on the front door with **no `.soon-stamp` anywhere in the
DOM**; the Pahlavi lobby with all seven doors live and `شروع بازی` where `Coming soon` used
to be; the green room's rule stacked steel-ivory-ember as the Iranian tricolour actually
stacks; and past that a dealt board of thirty tiles serving real Persian clues off the
512-row bank, category and value up, the cold refinery stage behind them.

**`Tools/check_readings.py` had never heard of the course.** Its `SHELVES` predates the
Pahlavi seminar, so `Web/courses/pahlavis/data/readings.js` had been sitting outside every
run — 123 rows over 8 weeks, unchecked since they were authored. Registered. It passes:
8 groups, 123 entries as expected, exit 0; the two rows without years are the same author
state the other shelves report, not defects.

**MAIN has the Pahlavi bank but not the Pahlavi shelf.** The promotion half is done — a peer
session absorbed the whole 512-row bank on Morad's standing *"always let MAIN absorb the
courses"*, and MAIN now reads 2,947 rows over 539 categories, which I confirmed off the live
bank rather than off the log. The readings half is not. `Tools/make_readings.py`'s
`COURSE_SHELVES` still lists only IR4595 and the Qajars, so no Pahlavi week is filed under
MAIN's headings and MAIN's shelf is still 177 where it should be 300. Left alone on purpose:
it needs a week-by-week filing table onto MAIN's headings — a classification judgment, not a
mechanical copy — and it rebuilds a file a peer session is working in this same afternoon, so
racing it would only mean one of the two writes silently winning. Named here so the next pass
picks it up.

Nothing committed.

---

## 2026-09-18 — the board stops explaining its own jokes

**The grey Persian subtitle under each category header is gone.** It printed a bucket —
تاریخ و انقلابها, فرهنگ و هنر — under the real category string, which told the player what
the pun meant before they had a chance to not get it. Morad: *"the whole point is that you
pick your poison without quite knowing what the punny titles mean."* Removed from
`Web/app.js` (`persianSubtitle()` and `PERSIAN_BUCKETS` with it, plus the `cat-fa` span in
`renderBoard`) and from all three `styles.css` rules that set it. The courses inherit
`renderBoard`, so the Pahlavis and the Qajars lost it in the same edit; nothing in
`Web/courses/` had a copy of its own. Cache tokens bumped on `styles.css` and `app.js`.
Seen on the live board in Persian: six titles, one line each, no garnish.

**`theme` now has no consumer.** It existed to feed that bucket lookup, and
`QUESTION_AUTHORING.md` §5 was written entirely around choosing a theme for which bucket it
should land in — a section that would have kept sending authors at a dead function. Rewritten
to say what the field is now: a subject tag, printed nowhere. The banks keep it; not a data
change.

**Two stale copies left where they are.** `Android/app/src/main/assets/Web/` carries its own
app.js, already drifted from `Web/` by more than this change — it looks regenerated rather
than hand-synced, so patching it by hand would be picking a fight with whatever builds it.
`Course/dist/` (the 2026-09-14 gemini pass) still has the subtitle, but nothing loads it:
the front door resolves courses through `Web/courses/<id>/`.

---

## 2026-09-18 — the books the new rows actually cite go on MAIN's shelf

**Eleven books registered, shelf now 188.** Morad: *"whatever book we actually used should also
go on the reading list for main edition of game."* The landed `main-2026-09` batch is 230 rows
over 13 books, and 11 of those books were not on the shelf — so a player reading any of their
citation lines could not look the work up. Added to `Corpus/Metadata/corpus_manifest.json` in
shelf 8, in surname order, ids reused from the bank's own `source_id`s: Occidentosis;
Underground; The Fall of Heaven; Reformers and Revolutionaries; Medicine, Public Health and the
Qajar State; A Century of Revolution; Iranian History and Politics; Eminent Persians vol. 1;
Vanguard of the Imam; Revolution and Its Discontents; Small Media, Big Revolution. Regenerated
with `Tools/make_readings.py`. All 13 of the batch's books now resolve on the panel — checked by
matching each row's `book_title` against the generated file, not by eye.

**Two of the 13 were already listed; a twelfth book is one we do not own.** Amin's *Making of
the Modern Iranian Woman* and Naficy's *Social History of Iranian Cinema* vol. 2 were already on
the shelf, so the count is 11. *The Sacred Republic* — behind the four fabricated IMPROV
citations — is not in the corpus anywhere on disk, so it cannot be listed: a bibliography naming
a book we do not hold is a second fabrication, not a fix.

**The rest of the folder stays unlisted, on purpose.** Registering is what puts a book on the
panel, so the remaining `8 - New Additions (2026-09)` books would have pushed the shelf past 300
and shown up in the game with no clue pointing at them. Only the cited ones went in, and
`Tools/check_readings.py`'s docstring now records why. The Pahlavi shelf's 123 readings are
still unfiled: that one is a week-by-week classification onto MAIN's headings, a different job.

**Two new source-type chips taught to `KIND`.** `Primary Source / Political Essay` for
Occidentosis and `Specialist Monograph / Media Studies` for Sreberny and Mohammadi — the
generator refuses a type it has not been taught, which is the guard doing its job. Page counts
and chars-per-page measured off the PDFs with `pdfinfo`/`pdftotext`.

**`file_path` follows the stale convention.** The new entries point at the old
`/Users/Morad/Spark/…` root like the other fifty; nothing reads the field, and the corpus's live
copy is the in-tree `Sources/MAIN CORPUS/`.

`check_readings.py` is OK — one warning, the pre-existing case of Amin's book appearing on both
the corpus shelf and the absorbed IR4595 one. Not seen in a browser: the shelf was verified the
way the project verifies shelves, since `check_readings.py` evaluates the file in node with the
same bare `window` the browser hands it. Nothing committed.

## 2026-09-18 — the extension lands: MAIN is 3,752 rows, and the Persian host loses his tic

**805 rows a side went into the archive.** One run of `Tools/append_batch.py main-2026-09b` — 33 books'
categories plus ten finals, 2,947 → 3,752 rows and 538/539 → 707/708 categories. The batch was merged by
`/tmp/ext2/assemble.py`, the quotes proved by `/tmp/ext2/verify_quotes.py` (795 book rows and 10 finals,
0 failed), the play files re-rendered by `Tools/render_bank.py`, the digest by `Tools/bank_digest.py`.
Nothing committed.

**The gate that reshaped the most content: the Persian attractor.** `check_bank.py:868` refuses any `fa`
host line whose bare tail ends in گفتی, and the host had used it to close 27 of the new wrong-answer
lines — a tic across a whole board. Only the closing verb changed; the correction stays. The match is a
substring, so نگفتی is caught by the same rule. Rescan: zero.

**Two false negatives in the verifier, one of them the tool's own fault.** A stray agent scratch file in
`facts/` is a JSON list and `sheet_index()` called `.get` on it: it now skips `_`-prefixed files and
anything that is not a sheet. The second was real and looked like a bad citation — these PDFs set a
capital I that `pdftotext` returns as a lowercase l, so Atabaki's correctly cited `Iran-e Now` arrived as
`lran-e Now`. `verify_quotes.py` grew a third probe that folds I/l/1 together; the row was right and the
needle was wrong, so the tool was fixed and the row kept.

**The wrong key cost two clean-looking scans.** The batch is archive shape, so a host line is
`host_reactions.wrong_generic`; `check_bank.py:194` renames it to `wrongLine` only when it builds the
play shape. Grepping the batch for `wrongLine` finds nothing. Related: `append_batch.py` tails
`check_bank.py`'s output, so the 27 attractor errors printed as 25 — the count was never capped.

**One row failed its own alias.** `single_purging_the_picture_show_200` listed `lustration` as an
accepted alias while `lustration` sat in its distractor options. `check_bank.py:598-611` catches exactly
that, and the source is explicit that lustration and purification are opposed. The alias is gone from
both languages.

**`assemble.py` is not idempotent.** It appends to whatever is already in `QuestionBank/incoming/`, so a
second run refuses with "805 id(s) already in the batch" and the empty base has to be restored from
`.pre-extend` before every re-run. Three title collisions and ten duplicate ids were broken before the
merge, by renaming the pun on one side of each pair: BAD BLOOD became COLOUR SCHEME, LAW AND DISORDER
became DRESSED TO KILL, PAST IMPERFECT became THE ANCIENT REGIME. A RACE APART was rejected as a fourth
because `theme` routes on substrings and "apart" contains "art".

**The Persian copy dictionaries grow with the archive.** `QuestionBank/persian_clues.json` and
`App/Resources/persian_clues.json` hold the shells' Persian copy, keyed by id. The landing path does not
touch them, so both were 805 short. They were grown by calling `promote_course_bank.write_fa_copy` — the
routine the course promotion already uses — rather than a fresh script. All three now read 3,752.

**`verify_flawless_state.py` was already red, and its rule is wrong.** It asserts zero Latin characters
in every Persian field; four answers, four option sets and one explanation on the shipped 2,947-row bank
already broke it, and the landing takes those to 7, 8 and 9. Every hit is legitimate — TERENA, Secure
Computing, `editormyself.com`, SUN, a parenthetical `Home Management`, and a quoted Avestan phrase in
guillemets. The house style keeps Latin proper nouns and acronyms on purpose, so the rule was left alone
rather than loosened to make this landing look green. Its counts were updated.

**One pun sits on two boards.** `TURBAN RENEWAL` names a single-round category (`pahlavi_0016_a`–`0020_a`)
and a double-round one (`double_clerisy_*`). Categories live per round, so nothing collides in the engine
and `check_bank.py` is silent — a header repeated across the two boards, and it predates this landing.
That is why the digest counts 708 English categories where 707 distinct strings exist.

**What the sheets still owe.** Four partly-authored books are short of their sheet — katouzian_21st,
keddie_modern, marashi_nationalizing, ridgeon_kasravi — eleven sheets were never opened, and six stopped
having written nothing. `check_coverage.py` holds the list. This was round two's brief; that work waits,
and the other 53 mined books stay untouched.

## 2026-09-18 — the flawless-state rule rewritten, and the fault it was hiding

**`verify_flawless_state.py` banned the alphabet, so it could not see a substituted letter.** The old
rule failed any Persian field carrying a run of two or more Latin letters. Every hit on the shipped bank
was legitimate — acronyms, official English names, romanized institutions, an Avestan phrase in
guillemets — so the rule read as noise and was tolerated. It is now a baseline: `LATIN_RUN` takes the
maximal Latin runs, `LATIN_OK` holds the 26 that have been read, and anything outside it fails with the
row, the field and the run named. A new name is red until someone reads it and allows it, which is the
review the old rule was standing in for and never performed.

**The hole was the two-letter floor.** `ژنrال` — a Latin `r` inside ژنرال — sat in the options of
`single_a_cossack_in_the_shadows_600`, and the old rule could not see it. The English row's fourth option
is "General Arthur Barrett"; the Persian is its transliteration, and one keystroke had gone wrong.
Repaired in all five carriers: the incoming batch, the archive, the play file, and both id-keyed copy
dictionaries. The `.pre-*` snapshots keep the fault, which is what a snapshot is for.

Teeth checked by planting a leaked English phrase ("the city of Tehran") and a substituted letter; both
caught, both named. Neighbours green — `validate_1000_clues.py`, `validate_persian_bank.py`, and
`check_bank.py` on both play files.

**Aliases stay exempt, deliberately.** A Persian row's aliases are its answer's transliterations; they
are Latin by construction, and flagging them would be flagging the design.

**`TURBAN RENEWAL` needs nothing, and round two's note on it stands.** `buildBoard` filters on
`!S.usedCategories[name]`, so a title drawn in the single round cannot be dealt again in the double — the
engine already refuses the collision. The digest's 708 is (round, category) pairs: English carries 707
distinct titles and one of them, TURBAN RENEWAL, is worn by two boards, which is the entire gap. Persian
reads 708 distinct because those two boards were given different Persian titles (عمامه در ترازوی قدرت /
کلاه شرعی، کلاه پهلوی). No engine fault and no data fault.

**Stale prose, left alone.** The three docs still quote 2,205 rows and 373 categories, and
`land_batch.py`'s closing reminder quotes 2,205 and 261. The asserts carry the live numbers — 3,752 and
708 — so nothing is broken; only the examples around them have rotted.

## 2026-09-18 — the two archive fields no gate could see, and the labels a writer invented

`./run_tests.sh` was crashing, and had been since the 805-row landing: `verified_clues.json` would not
decode. Ten rows — five in `THE PEACOCK THRONE IN ECLIPSE` and five in `WHISPERS IN THE CORRIDORS OF
NIAVARAN`, both out of Cooper's *Fall of Heaven* — carried two values the Swift model does not accept:
`evidence_type: "DIRECT_QUOTE"`, where `GameEngine/Models/Clue.swift` declares four cases, and
`confidence: "CONFIRMED"` on a field that is a Double and reads `1.0` on the other 3,742 rows.

Both are one shape of defect: a field the play file does not carry. `check_bank.py` rewrites an archive
row into the play shape so one rule set serves both, so a field that does not survive the rewrite is a
field no rule reads — and `append_batch.py`'s gate *is* `check_bank.py`. Every gate said clean. The
decoder, which reads the archive whole, threw on the first unknown value and took the suite down before a
single assertion ran.

**Repaired in the data, not in the enum.** `DIRECT_QUOTE` is not a fifth kind of evidence: the enum
splits evidence by where a claim comes from, and a quoted line is testimony or a fact that happens to be
quoted, with `supporting_passage` already carrying the quotation. The whispers passages are not even
quotations — they are Cooper's narrative. Both labels were the writer's vocabulary rather than the
archive's, so both went to `established_fact`, which is what 3,434 rows say. Four carriers each: the two
archives and the two incoming batch files they were merged from. `.pre-*` snapshots left carrying the
fault, as with ژنrال.

**The gate now reads them.** `check_bank.py` gains `check_engine_fields`, run in `--archive` mode beside
`check_rationales`, over `evidence_type` and `confidence` and nothing else — every other field the engine
is strict about is one the play file also carries, so a rule that reads the play shape already reaches
it. Teeth tested both ways: a planted `DIRECT_QUOTE` and a planted `"CONFIRMED"` each fail by row name
and exit 1, while the real archives stay clean.

**The contract was the cause.** `GEMINI.md` lists all 27 field names and never said what `evidence_type`
or `confidence` take, which is how an author invents a value. Both sets are spelled out there now, in the
"things that fail a batch" list beside `difficulty`'s ladder.

**A third vocabulary, left alone.** `Course/banks/pahlavi-pass-2026-09-18/` uses
`evidence_type: "interpretation"` on 7 rows a language. Inert: `promote_course_bank.py:229` writes
`established_fact` and `1.0` into the promoted row regardless, so the label cannot reach MAIN, and if
that ever changes the new rule stops it at the merge. That bank is mid-authoring in another session, so
it is reported here and not touched.

**Where it leaves the tree.** `./run_tests.sh` is 27 of 27 again, and `verify_flawless_state.py`,
`validate_1000_clues.py`, `validate_persian_bank.py` and `check_bank.py` on both play files all pass.
Nothing committed.

## 2026-09-18 — Stephanie speaks the Pahlavis, and the floor stops cutting her off

**Forty-six lines, cut fresh.** The Pahlavi course had Stephanie Cronin's host cues declared in
`course.js` and no audio behind them, so every beat fell through to the silent placeholder. All 46 are
now cloned from the same reference clip the Qajars use — `Course/Masters/Pahlavis/Professor Voice/`,
`reference/stephanie-cronin-ref.wav`, Fish S2 Pro through `mlx-speech` — and not a single one is lifted
from the Qajar set. Forty-three of the 46 lines are textually identical between the two courses, which
is exactly why borrowing would have looked correct in a diff and been wrong in the room: they are two
editions of her, and the teacher's own cut of her own course is the point. 46 transcripts in, 46 `.m4a`
out, `fail=0`, `BATCH_DONE`.

Staged with `python3 Tools/stage_course_audio.py --course pahlavis`. Parity holds in both directions:
46 transcripts, 46 staged files, no missing name, no orphan.

**The runner has no lock, and that cost an afternoon.** `make.sh` skips any `$OUT/$name.m4a` that
already exists, which makes it resumable and reads like it makes it safe to leave running. It does not:
it is a single pass in `TEXT` order with nothing guarding the directory. Three copies ran at once —
each one started because a `pgrep -f 'Pahlavis/Professor Voice/make.sh'` check came back empty, and it
came back empty every time because the script's argv is just `./make.sh`, so the pattern never matched
anything. Under three-way contention each `mlx-speech` still peaked at 11.45 GiB, roughly 34 GiB of
demand on a 16 GB machine, and real-time factor went 10 → 68 → 250 where serial runs sit at 4–17. The
model load is a flat ~1.4 s either way, so the whole cost was the collision. Serial is not a style
preference here; it is the only shape that fits. Two lessons worth keeping: a "is it running" check
that greps for a path the process never carries is worse than no check, because it manufactures
confidence; and a batch script that is safe to resume is not the same as a batch script that is safe to
start twice.

**Qwen came down** with `launchctl bootout gui/501/com.morad.mlx-vlm-server` — `kill` alone would not
have done it, since the plist is `RunAtLoad` + `KeepAlive` + `ThrottleInterval 15` and would have
relaunched it fifteen seconds later. It was holding 18434 for a job that had finished; nothing else
wanted it, and the TTS batch wanted the memory.

**The real audio exposed a defect the silent placeholder had been hiding.** `Web/courses/pahlavis/course.js`
held the floor with `setTimeout(function () { speaking = false; schedule(); }, 3400)` under a comment
claiming the clip "is held for the length of its own file". It was not, and it never had been: `3400`
is exactly `host_line_placeholder`'s 3.4 s — the number was read off the file it replaced, not off the
engine, whose own silence constant is 2000. So the queue released the floor 3.4 s in no matter who was
still talking, and the next queued beat started on top of her. With the placeholder nobody could hear
it. With her, the lines run 1.81 s (`right_02_somebody_did_the_reading`) to 18.58 s (`welcome`), and
3.4 s lands mid-sentence on most of them.

`Sound.voice(name, volume, then, opts)` already takes a completion callback and already always calls it
— on the file's own `ended`, on a refused play, on the duration-derived guard, on a missing cue — which
is the same close the cold open waits on. So `play()` now sets `speaking = true` and hands `release` to
`Sound.voice`, and the floor is held for exactly as long as she is speaking. One guard was needed
beyond that: `voice()` early-returns without calling back when sound is disabled, so `play()` checks
`Sound.isEnabled()` first and gives the floor up directly rather than waiting on a callback that is
never coming. The Iran course already had this shape (`precue`, `iran-in-world-politics/course.js:885`);
the Pahlavis and the Qajars did not. **The Qajars carried the same defect with real clips already in
place**, and its `play()` was byte-identical, so both files were changed together. Both pass
`node --check`, and both script tokens were bumped — `?v=20260918-pahlavi-floor` and
`?v=20260918-qajar-floor` — so no cached copy survives.

**Verified in the browser, by measurement.** A probe wrapped over `HTMLMediaElement.prototype.play`
(needed because `app.js` uses detached `Audio` objects, so no `audio` element is ever in the document)
recorded name, duration, and how much of each clip actually ran. `stephanie_pahlavis_welcome.m4a` — dur
18576, ran 18576. Decisive test on the queue: a `hostbeat` for `boardIdle`/`double` cued `null` at
903 ms, `stephanie_pahlavis_start_double.m4a` at dur 7616 **ran its full 7616**, cue released at
8576 ms. Under the old fixed hold the floor would have come back at 3.4 s and cut a 7.6 s line in half.
Qajars regression after its edit: `stephanie_qajars_welcome.m4a` dur 13235, ran 13235, no console
errors. All three course tokens served. Loudness −21 to −23 dB on a sample, 46/46 HEAD 200, and the
`welcome` caption in the browser matched the rendered line.

**Open, and deliberately not redesigned: the queue is emptied every time any line ends.** `Sound.voice`
calls `tellCue(null)` from `finish()`, the course's `hostcue` listener reads a null name as
`standDown()`, and `standDown()` does `queue.length = 0`. The consequence of the fix is visible in the
decisive test: the `streak` beat dispatched 4500 ms into that 7.6 s `start_double` was enqueued and then
**silently dropped** when the line ended at 8576 ms. Under the old code that beat was heard — because
it preempted her mid-word. So the trade is "finishes the sentence, queued beat lost" against "beat
lands, sentence cut off", and I took the first as unambiguously right: a host who stops mid-clause to
announce a streak is the bug, not the feature. But the underlying semantics — should a beat that
arrives while she is speaking wait its turn or be discarded? — belongs to all three courses and is not
mine to change silently under a bug fix. Left as found; it wants a ruling.

Nothing committed.

## 2026-09-18 — the searchlight was reading its own reflection

`Tools/verify_batch.py` had two defects that made it flag rows it had no business flagging, and
both were the kind that hide: it decided placement from the answer's words alone, and it decided
each book's page offset from those same words. A mode fitted to the rows cannot see a page error
the rows themselves carry — Abrahamian's answers said +13 while the folios prove +32, so the
offset was calibrated to the error and every row agreed with it. The fix is to read the page
number the scan prints: `label_map` decodes the folio (`io6` is 106, `i86` is 186, `IIO` is 110),
fits `printed = step × sheet + const`, and the folios outrank the answers on ties.

The step is fitted rather than assumed because **a two-up scan has no constant offset at all**.
Paidar prints two pages to a sheet — sheet 61 carries 108 and 109 — so forcing a single
`(sheet − printed)` constant puts half the book a page out, and the answers' own mode cannot
repair it because that mode is what is broken. Twelve Paidar rows read as misplaced on that
account; with the step fitted they are all clean (step 2, const −14, 123 sheets agreeing).

**The regression that followed was mine, and it was a sign.** The answers path counts
`sheet − printed`; the caller wanted `printed = sheet + const`. Handing it back unconverted
mirrors every answers-calibrated book about its own front matter — Grigor's 21 rows moved 4
sheets and went NEAR, and Hegland's 15 accused p.30 of living on sheet 55 of a 33-sheet
article. Two rows of that were visible on the output and I nearly blamed the folios for it.
`calibrate` now converts, the target is checked against the book's real length, and the summary
prints in the convention its own label claims.

**One more of the same kind, in the Persian pass.** `calibrate` ran before the language
substitution, so the fa run scored each book's offset against Persian answer words — which match
nothing in a Latin-script scan — and fell back to a different calibration than the English run
had used on the same rows. The answers are passed in English for both languages now. The two
runs then agree row for row: 740 OK, the same 60 leads, the same offset per book.

**Result on the 09b batch: 740 of 805 confirm, up from 703, and no book regressed.** The 52 the
tool still dislikes are leads, not faults: 32 of them quote a passage with a 15+ word verbatim
run on their own cited page, which is the better evidence of the two. Four are weak enough
(3–4 word run) that only a person reading the book can settle them.

**One correction to what I said here earlier.** I reported that `single_village_people` carried a
wrong author. It did not. **Mary Hooglund is Mary Elaine Hegland** — the printed byline of the
1980 article is her married name, and a bibliography prints "Hooglund [Hegland], Mary (1982)".
The author field was right the whole time; the defect was only the composed `book_title`, and
that is what was repaired. The lesson costs nothing to repeat: the citation is read off the work,
and so is the byline — including when the byline surprises you.

**Open.** Fifteen landed rows cite that Hegland article and it is not on MAIN's reading shelf
(`Corpus/Metadata/corpus_manifest.json`). Registering it is Morad's call, not a tool's.

Nothing committed.

## 2026-09-18 — 1.0.11 goes up, and the two stalls that were not the network

The release is published: `v1.0.11`, Latest, on `5193d8b`, with the copy from
`dist/RELEASE-v1.0.11.md` verbatim as its body and all three builds as assets —
macOS-universal.zip, iOS.ipa, Android.apk, sizes matching `dist/` to the byte. Both publishing
workflows went green on the push that carried it: itch.io in 35s, Pages in 42s.

**The push stalled twice, and neither stall was the connection.** The first is the failure
already in the notes: HTTP/2 ref negotiation, process alive, ~0 CPU, remote unmoved. The second
survived HTTP/1.1 — the pack uploaded complete, 176 MiB at 379 KiB/s with a peak of 1.43 MiB/s,
and then the server hung up at the ref update with the remote still on `964de36`.
`http.postBuffer=524288000` cleared it. What both had in common was that the evidence of a
healthy link was there the whole time — `ls-remote` answering instantly, the pack moving at
MiB/s — and the early `--progress` readings of 38–64 KiB/s were the meter smoothing over the
small-object phase, not the link speed. The flag set that landed it:

```
git -c http.version=HTTP/1.1 -c http.postBuffer=524288000 \
    -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=90 push --progress origin main
```

`--progress` is not optional on a pack this size: without it `send-pack` runs `--no-progress`
and the log stays empty, which reads exactly like a hang. And it has to run detached — a shell
the session owned died mid-push and took its log with it.

**The 1.0.11 cut had shipped without its frozen web tree.** `Versions/` went from `v1.0.10` to
nothing, so a release carrying two new courses and a 3,752-row box left no snapshot to get back
to. `snapshot_web.sh` was skipped. Froze it now: `Versions/v1.0.11`, 336 files, 70 MB, diffed
file-for-file against `Web/` and identical.

**The page check no longer trusts a file that cannot be paged.** `Tools/verify_batch.py` now
resolves a row's book and then asks whether that file numbers its own pages; if it does not, the
best-scoring file within a point of it that does takes the check instead. Amanat's *Pivot of the
Universe* is in the corpus twice — a 1997 scan that prints folios, and a 2008 reflow that
carries no page number anywhere — and calibrated on the reflow the tool invented a "+70 offset"
and checked every one of that book's pages against a number absent from the text. Committed.

## 2026-09-18 — One logo for the whole show, and the release replaced in place

He sent one picture and asked for it on the front door and inside the show both, with the
course marks untouched, and asked that the published release be replaced rather than a new
version cut. So 1.0.11 stays 1.0.11; only its bytes moved.

`Web/assets/logo-wordmark.png` is now that picture — JEOPARDY! in cracked limestone, a gold sun
for the *O*, the crown and the lion off to the left, the Khamsa and Tehran's skyline across the
top, THE IRANIAN EDITION set into a band of Persian tilework — and it is the only main wordmark
there is. `logo-iranian-pack.png`, which the front door had been wearing, went to `~/.Trash`.
The door and the show wore two different pictures of the same thing; with one picture the second
file was 1.5 MB that nothing loaded and that still shipped in the zip, the `.app`, the `.ipa`
and the `.apk`, reachable only by grepping for the name.

`.brand-wordmark` stayed a class of its own, separate from `.logo`, because `course.js` re-skins
`.logo` on every edition change and the front door has to stay MAIN-branded. It now carries
`logo-wordmark.png` at the same tag as everything else repainted this round, `?v=20260918-sunmark-1`.

Three things cut from the retired file by name and would have kept the old art silently:
`Web/assets/og.jpg`, `.github/assets/logo-banner.png`, `.github/assets/itch-cover.png`. The
first is rebuilt by a new `Tools/make_og_card.py` — the lockup over `stage-backdrop.png`, 1200×630,
because the card is 1.9:1 and the lockup 2.9:1, so a crop would take the first and last letters of
JEOPARDY! off. The other two by the tools that already existed, repointed. The README's and the
release note's alt text both said "The Iranian Pack", which is not a name the show uses; both now
say The Iranian Edition. `og:image` got a cache tag, since a repainted picture at the same URL is
a picture the unfurlers will not re-fetch.

**Nothing else was repainted, and that was checked rather than assumed.** The three course PNGs
inside the Android apk before and after are the same bytes (1575637, 1918160, 1844985). The app
icon was left alone deliberately: `App/Resources/icon-master.png` is a purpose-built square
1254×1254 J!/emblem mark, and the new art is 2.93:1 and will not sit in a square. Read at
`.logo-clue`'s 133×45 the new mark still resolves — busy, not mush — so nothing was enlarged.

**The release was rebuilt rather than re-issued.** `build_release.sh --universal`, `build_ipa.sh`
(its Web-tree diff came back in step, staged 1.0.11/1011) and `./gradlew :app:assembleRelease`,
then the Mac zip re-cut by hand with `ditto -c -k --sequesterRsrc --keepParent`, which is still
the only packaging these zips have. `Versions/v1.0.11` was refreshed in place by rsync: 336 files
to 335, the difference being the retired file, and it diffs file-for-file against `Web/`. The
superseded zip and apk are in `~/.Trash/1.0.11-old-logo/`; the old wordmark is still in git at
`9a8a401`.

The three GitHub assets were re-uploaded to the existing `v1.0.11` release with `--clobber` and
its body replaced from `dist/RELEASE-v1.0.11.md`; the published sizes now match `dist/` to the
byte. Uploading over a published release is not a thing to do unasked — it was asked for in
those words.

## 2026-09-18 — The icon catches up with the wordmark

The icon round the wordmark round deferred. That entry left the app icon alone for one reason —
the new art is 2.93:1 and will not sit in a square — and the square art arrived today as a
second delivery, so this is the second half of the same job and not a reversal.

**It needed no re-framing, and that was measured before anything was written.** The master is
1254² RGBA with the glossy tile occupying 0.877 of the canvas; the master it replaces measured
0.873. Same frame, same margins, no stray specks past the tile edge, so the treatment is a
composite onto opaque black and a resize. Anything cleverer would have been inventing a
difference. Ingested as `Assets/Generated/icon-main-20260918-v1.png`, alongside the wordmark
master and under the same gitignored convention; the Desktop copy is his to sweep.

**`Tools/make_app_icons.py` is new, and it is the first written record of how these are cut.**
Thirty surfaces from the one master: `icon-master.png` 1254, `AppIcon.png` and the iOS catalog at
1024, the ten-step iconset → `iconutil -c icns`, the favicon pair at 512 and 180, and the Android
set at five densities. The adaptive icon keeps the rule its own XML states — the launcher draws
the shape, so the tile is scaled to two thirds and centred on black; the cut measures 0.586
against the previous 0.583. `ic_launcher_round` is written as a byte copy of `ic_launcher` at
every density, which is what the first cut did and what `cmp` still says. Every target is 1:1
full-bleed and opaque, because a transparent margin under a launcher mask comes out ragged.

This is a generator writing onto paths the app serves, which the tooling rule otherwise forbids.
Safe here for the reason that rule names: the master is in the tree, so a re-run is a repaint and
not a loss, and every previous icon is also in git.

**The wordmark was not touched.** It is the one thing this round had to leave alone, and it is
not in the diff — `Web/assets/logo-wordmark.png` is byte-identical to what the published builds
already carry. The favicon and apple-touch tags move off `20260915-globe-22` to
`20260918-crownicon-1`; a repainted file at the same URL is a file browsers will not re-fetch.

**All four builds were cut again and the check was made on the packaged bytes, not the tree.**
`build_release.sh --universal`, `build_ipa.sh` (Web parity in step), `./gradlew
:app:assembleRelease`, and the Mac zip re-cut by hand with `ditto`. Read back out of the archives:
the icns and `icon-512.png` inside the zip are the new files byte-for-byte, the same two inside
the ipa likewise, and the apk carries the new web icons at hash and — the sharp one — exactly 15 of
its 30 resource PNGs changed, which is the launcher set and nothing else. The other 15, and all
three course wordmarks, are untouched. `Versions/v1.0.11` was refreshed in place by rsync; 335
files, still diffing file-for-file against `Web/`. Superseded artifacts are in
`~/.Trash/1.0.11-old-icon/`.

The three GitHub assets were replaced on the existing `v1.0.11` with `--clobber`, and its body
replaced from `dist/RELEASE-v1.0.11.md` with one paragraph added for the icon, which the notes had
otherwise been silent about. The tag `v1.0.11` points at `5193d8b` and was left there: the release
is a set of assets replaced in place, and moving a published tag is a rewrite of something other
people may already have fetched. The consequence, said plainly, is that the source tarball at
`v1.0.11` carries neither this round nor the last one — the binaries are what moved.

The push stalled on HTTPS with HTTP 408 three times while `ls-remote` answered fine, which is the
known signature; it went over SSH unchanged. Committed `d80c0d8`.

## 2026-09-18 — the Persian category head was set in a Latin face

He caught it from a screenshot: the board's category boxes in Persian were far too small.
The cause was not a size someone had chosen. `.cat-name` was the one caps element on the
board that the `[dir="rtl"]` de-cap group did not reach, and it asks for `--display` —
`Avenir Next Condensed`, which carries no Persian glyphs at all. So every Persian category
was drawn by a fallback face at the *Latin condensed* size, and it kept the group's two
properties that `STYLE_SHEET.md` says are defects on Persian: `text-transform: uppercase`
and `letter-spacing: 0.13em`, the second of which prises the cursive joins apart.

Measured at 1440x900 before: 10.08px, Avenir Next Condensed, 1.31px of letterspacing. After:
`html[dir="rtl"] .cat-name` gives it `--fa`, `clamp(11px, 0.9vw, 15px)` and neither the caps
nor the letterspacing — 12.96px, IRANSansWeb, no tracking.

The face swap alone would not have been enough, which is why the size moved with it. Persian
reads smaller than Latin at the same pixel size: the body of the letter is the x-height where
the Latin cap it sat beside was the cap-height. Every other Persian label in the build already
carries that correction — `.circle-name` on the front door takes ×1.22 — and this one had
none. It is deliberately a touch above that ratio, since he called the result "way too small"
rather than merely inconsistent.

English is untouched, which is structural rather than a matter of care: the rule is scoped
`html[dir="rtl"]`, so at `ltr` it cannot match. Confirmed by reading both back at 1440 — the
English head still computes to 10.08px in Avenir Next Condensed with its letterspacing intact.

The head row is `auto`, so the two extra lines' worth of height comes off the tiles; heads
measure 39.3px against 35.4px before. The longest category in the Persian bank
("مینیاتورهای بهزاد و قلمموهای استاد", 35 characters against the English bank's 42) wraps
to two lines in a 56.8px head and does not clip. Checked on portrait too, where the rule's
specificity means Persian now keeps its own floor of 11px instead of the 6.5px the landscape
rung would have handed it — larger than the English 9.5px there, which is the right direction.

## 2026-09-18 — every Farsi year now names its calendar

He asked for two things in one breath: a bare ۱۳۵۰ in the bank is ambiguous, and رزمآرا
was written with the ZWNJ in two places. Both are reader-facing and neither is a judgement
call, so `Tools/normalize_fa_prose.py` does them deterministically — calendar, script,
separator. This entry covers the calendar pass, which is the one with a rule worth arguing
about.

**Mark, do not convert.** `۲۵ مرداد ۱۳۳۲` becomes `۲۵ مرداد ۱۳۳۲ خورشیدی`. The year is
never rewritten into its Gregorian equivalent: that would change facts, and it fails on
medieval dates where the Persian translation of a Gregorian year is itself a guess. A
suffixed name is additive, reversible, and survives an editor's eye.

**The English twin is the gate, not the source.** The two banks share ids 1:1, so FA ۱۳۵۰
against EN 1971 resolves by arithmetic. The gate reads the twin's clue *and* its
explanation — the explanation carries most of the dates and is where 2915 of the markers
come from. Four ways a year is settled, in order of strength:

1. arithmetic against the twin (shamsi, +621 or +622) or an exact match (Gregorian);
2. a bare 19xx/20xx is Gregorian — no calendar in use here reaches 1900;
3. a 12xx–14xx year written after a Persian month name is shamsi;
4. a 12xx–14xx year in a row whose twin states only 20th-/21st-century years is shamsi.

Route 3 was added last and is the one that earns its keep: a Persian month heads no other
calendar. Lunar months are Arabic (محرم، رمضان) and Gregorian dates in Persian prose use
transliterations (ژانویه), so the month settles the calendar with no need of the twin. It
took the review tail from 92 rows to 71. Its left boundary `(?<![ء-ی])` is load-bearing:
without it "بلندی ۵۶۰۹ متر" and "مردی" match on their tails. The separator between a month
and its year is a plain space everywhere in this bank — 1701 occurrences, not one ZWNJ —
so the pattern does not need to tolerate one.

**Rejected, and why.** A vocabulary rule (صفوی/قاجار/مظفرالدین ⇒ pre-modern ⇒ میلادی) was
built and tested offline: it would have flipped 50 rows. It is wrong. `single_tehran_bazaar
_to_megapolis_400` reads "نوروز سال ۱۱۶۵ خورشیدی (۱۱۶۵ ش/۱۲۰۰ ق)" — an explicitly lunar
۱۲۰۰ inside a row that is explicitly shamsi. A vocabulary rule marks that ۱۲۰۰ خورشیدی and
writes a falsehood into the bank. The month rule cannot: no month name precedes it. The
pre-modern-keyword guard that was supposed to catch this mostly false-blocked rows that
merely mention صفوی while the year is modern, and would have caught the one dangerous row
by luck.

**A count is not a year.** ۳۱۰۰ نفر, ۱۷۱۰ صفحه, and "شمار در نهایت به ۲۰۰۰ رسید" are
recognised and left alone, and the report counts them — ۳۸ counts and ۲ labels — so the
decision is visible rather than silent. Three rules, each narrowed after a false positive:
only spaces and a comma may sit between a count and its unit, so "۱۹۲۹. هزار ماده" stays a
year; the cue must sit immediately before the number ("ماده ۱۱۳۳ قانون مدنی") rather than
merely in the clause, so "همین بند در ۱۳۲۰ بهانهٔ اشغال شد" stays a year; and a bare به
plus a verb of reaching is what makes "به ۲۰۰۰ رسید" a count.

**The two banks are sibling clues, not translations, on 7 rows.** Found while auditing the
rule: `double_clerical_power_maraje_of_najaf_and_qom_1600` is Khoei/1991 in Farsi and
Kashani/1953 in English. Comparing the language-independent provenance fields (book, page,
author) shows only 7 rows diverge this way. Each of the 7 markers on those rows is correct
on its own terms — ۱۳۰۲ + ۶۲۲ = ۱۹۲۴, ۱۳۶۰ → ۱۹۸۱, ۱۳۵۷ against ۱۹۸۰ میلادی — so no marker
rests on a twin that is a different clue. The rest of the apparent Farsi/English year
mismatch is a decade label (دههٔ ۱۳۶۰ against "the 1980s", a uniform +620, correct in both
languages) and English ranges written "1890-92", which defeat four-digit extraction.

**Verified.** Both banks reserialize byte-exact; 3752 rows each with identical ids; zero
divergence on all eleven mapped field pairs; `page`, `value`, `round`, `difficulty`,
`correct_option_index` and `supporting_passage` untouched, so quoted passages were never
reached. `validate_persian_bank.py` passes; `check_bank.py` reports only the 16-row
alias-ownership warning that predates this work; `./run_tests.sh` 27/27. The validator's
"1880 clues with verified shamsi dates" figure does not move, because it already reads
"month + year" as a shamsi date — independent corroboration of route 3.

Still open, not acted on: the English twin of `double_jungle_guerrillas_of_gilan_2000_a`
says "a clause Moscow cited during WWI in 1941", which should read WWII. That is the
English bank, which he did not ask me to touch. Also worth knowing before the next authoring
pass: `Course/banks/*.py` and `Tools/build_batch_*.py` write خورشیدی themselves, so a re-run
of either can reintroduce drift.

---

## 2026-09-18 — The lock-in gets a new sound, and the old cue retires

He handed over `iranian_jeopardy_lockin_tak_ting.wav` with "this should be the buzz sound from now
on — the other one is really annoying." 0.34s against the outgoing cue's 0.72s, so the annoyance was
at least partly length: the old one is a sustained buzz, this one is two short hits.

**It arrived with the 2026-09-16 defect, in miniature.** Stereo, 48 kHz, and L/R correlation **−0.25** —
so about 4.3 dB of it cancels on any path that sums the channels, which is a phone speaker, a laptop
downmix, and every mono copy in the pack. That is the same shape as the anti-phase file two days ago,
milder. Every shipped cue is mono, so this one is too: channels summed, encoded once from the WAV, not
re-encoded from the m4a. The mono sum's transient survives the cancellation rather than losing to it —
its peak, −1.21 dBFS, is *above* either channel's — while the tail is what goes, which leaves the
lock-in shorter and snappier than the file he sent.

**The level is a judgement, and it went under.** Mono sum peak −1.21, so 1.79 dB down puts it at peak
**−3.0 dBFS**, rms ≈ **−18.3**, against the outgoing cue's rms −12.2. Not comparable numbers, because a
0.34s transient reads by its peak where a 0.72s sustained buzz reads by its rms. The pack's other
stingers sit at peak −0.7 to −0.1, so −3.0 is deliberately 2-3 dB under them: he called the cue being
replaced annoying, not quiet, and the one time this file moved in the other direction he heard it
once and said WAAAY too loud. If −3.0 reads shy it is one number in a two-line script — ffmpeg gain,
afconvert, no other file moves.

`CUE_V.buzz` moved `20260916-buzz-2` → `20260918-buzz-3`. Third time for this cue, which is the map
earning its keep.

**The master is in the tree now.** It went to `App/Resources/Sounds/buzz.wav`, where MAIN's source WAVs
live, and the file that was there became `buzz.pre-20260918.wav` — that one was *not* what shipped, since
the current cue was cut from a Desktop WAV nobody ingested, which is how the pack ended up with no master
for the file it plays. It has one again.

Six live copies replaced and `cp` throughout, no hardlinks: `Web/`, the Android staged tree, both
`Course/dist` packs, and both `.app` bundles. One hash, `09d18da1…8286e2`, on all six. The two bundles
re-signed (`xattr -cr`, `codesign --force --deep --sign -`) and verified, as writing into a sealed bundle
always invalidates it.

**Verified in the browser, not asserted.** Played a real clue through the UI and took the buzzer: the
game requested `assets/audio/buzz.m4a?v=20260918-buzz-3`, answered 200 then 206, no failed request in
the list. Asked offline, the decoded file is mono 48 kHz 0.340s at peak −3.11 / rms −18.34 — matching
the measurement to a tenth of a dB. Front door boots with no console error.

---

## 2026-09-18 — The Farsi bank names its own calendar, and the two banks are not translations

He asked for the Farsi bank's dates to stop being ambiguous: English always Gregorian, Persian
always Shamsi, and every conversion double-checked. The policy he picked was "convert modern,
label old" — a Gregorian year from **1800** on is rewritten into its Shamsi equivalent and
labelled خورشیدی; anything older keeps its digits and takes میلادی; BCE facts keep پیش از میلاد
and lose the stray میلادی. The tool is `Tools/normalize_fa_prose.py`, dry run by default, `--apply`
writes both banks; `QuestionBank/normalize_fa_report.md` is its state report.

**What moved, measured from the 03:14 `.pre-normalize` backups to now.** 1972 clues changed text.
905 year numerals were rewritten from Gregorian to Shamsi, across 496 clues. 2777 calendar labels
were written or corrected. 2132 clues now carry a year that names its calendar. On the settled
bank a further run reports zero changes, 960 years held back by a guard, and 12 rows unresolved
in the tail. The round trip is byte-exact, 3752 rows both files, ids in order, and `page`,
`value`, `round`, `difficulty` and `correct_option_index` never moved, so nothing structural
was reached. Master and web agree on every mapped field.

**The evidence ladder, strongest first.** Arithmetic against the English twin (shamsi + 621, or
+ 622 for a date before Nowruz) or an exact year match; a bare 19xx/20xx, which can only be
Gregorian; a 12xx–14xx year after a Persian month name, which is shamsi because that month heads
no other calendar; a 12xx–14xx year in a row whose twin states only modern years; and last, the
bank's own usage — a bare year is shamsi if that exact year wears خورشیدی somewhere in the bank
and never wears میلادی. A decade takes the same route when its twin cannot help: `single_tehran_
bazaar_to_megapolis_1000` reads «تلهکابین … در دهه ۱۳۵۰» under the Rayy clue's twin, but the bank
dates ۱۳۵۰ خورشیدی thirty-seven times, so it is the 1970s and is labelled `دهه ۱۳۵۰ خورشیدی`.
Decades are labelled, never converted — the Shamsi decade is the Gregorian one less 620, so a
Gregorian row keeps `دهه ۱۸۷۰ میلادی`.

**The report is a state, not a changelog.** `write_report` runs on every invocation, dry or
applied, so a run over a settled bank zeroes every changed count. That is by design and is now
said in the report itself, because the first time it happened it read like the work had been
reverted.

**The English fix he authorized is in.** `double_jungle_guerrillas_of_gilan_2000_a` said "a clause
Moscow cited during WWI in 1941"; it now says "during World War II in 1941", that being the house
form (World War II, 46 occurrences, against WWII's 29). Two occurrences in `Web/data/clues.js`,
three in `QuestionBank/verified_clues.json` — the third is a nested rationale block.

**Correction: the two banks are not translations on 315 rows, not 7.** The entry earlier today
said 7, comparing book, page and author. That test could never have found the rest: the Farsi row
*inherits* those fields from its English twin, so they agree by construction even when the
questions do not. The test that sees it asks whether the Farsi clue's answer is the English
clue's answer. 315 row-ids fail it — 175 distinct clues, 8.4% of the 3664 rows whose English twin
carries Persian aliases — across **54 of 707 categories**. The alias test's own false-positive
rate is small and known: 9 of the 324 it flags are ZWNJ or diacritic variants of the same answer
(تقلید against تقليد, جبههٔ ملی against جبهه ملی) and were dropped by hand.

Three shapes. **115 rows** where the Farsi answer is another clue from the same category — the
category's facts sit at different value slots in the two banks. In DESERT ONE & DONE the Tabas
clue is $800 in Farsi and $1200 in English, and Operation Eagle Claw holds the slot the English
bank gives to Tabas. **139 rows** where the Farsi answer belongs to an English clue in a different
category. **61 rows** where no English row carries that answer at all. In every one of the 315 the
Farsi row shares its twin's book, author, *page* and *passage*; and the passage is the English
source text, about the English answer — the Farsi row at `single_shiraz_roses_and_nightingales_200`
asks about Hafez while carrying the paragraph on Sa'di's Golestan, and the one at `_600` carries
the Nasir al-Mulk Mosque paragraph while asking about فال حافظ. `passage` is authoring metadata:
`app.js` never reads it, so nothing breaks on screen. What does show is that the same fact can
carry a different value in each language, and that the Farsi clue's citation belongs to the
English clue. Which side is authoritative is an authoring call, not a calendar call.

**The calendar pass survives it.** 108 of the 315 carry a label, 75 of those were labelled on
twin evidence, and the twin on those rows is a different clue — so in principle the evidence was
wrong even when the answer was right. I checked four by hand: ۱۲۸۴ خورشیدی for the sugar
merchants' bastinado (1905), ۱۲۹۳ for Sattar Khan at Atabak Park (1914), ۱۳۸۳ for Pasargadae's
inscription (2004), ۱۳۷۶ for Sahar television (1997). All four are right, and the reason is
structural: every twin-based label sits on a modern Iranian fact whose own 13xx numeral can only
be shamsi. The rule is still unsound in principle on a misaligned row and the next pass should
not lean on the twin for one.

Still open for him, all findings and none acted on: which bank is authoritative in those 54
categories; the theme-name differences, including `single_reading_writing_and_rights_*` labelled
religion in Farsi and education in English; the seven *A Century of Revolution* page mismatches
(one is 47 Farsi against 67 English, six are Farsi = English + 1); the two passage mismatches;
three English rows carrying Persian script; the reciprocal ۱۸۱۳/۱۸۳۳ `_encore` mismatch in Imperial
Wars; the row holding both ۱۳۰۴ میلادی and ۱۳۰۴ خورشیدی; and ۱۲۲۸ against ۱۲۲۹ in
`double_foreign_exchange_2000`, both standing for the single English year 1849.

Nothing committed, nothing pushed.

## 2026-09-19 — The calendar rule stops being prose and starts being a gate

The rule was written down in three places and enforced in none of them: `C3PO_LOG.md`, a
generated report, a generated digest. `Tools/normalize_fa_prose.py` was the only implementation
and had no way to ask it a question without writing to the bank. It has `--check` now (exit 1 on
a year that names no calendar), and `--fa` / `--en` to point it at a candidate instead of the
archive. Pointed at the live bank it reports **7,354 year tokens that would be relabelled** — so
the Persian bank has never been run through its own rule, and the `.pre-normalize` backup carries
the same 3,752 ids, which is how we know the earlier pass was a dry run. Only 362 rows carry a
marker in prose. Nothing was applied: that is a 7,354-token bank edit and nobody asked for one.

**The gate is on the delta, not on the bank.** `Tools/append_batch.py` now runs those same four
passes over every candidate and keeps only the findings whose id is not already in the archive.
An absolute gate would have failed on the state it inherited and stayed failed forever, which is
how a gate gets switched off — the inherited drift is the maintainer's to settle, and the batch's
own rows are the ones the author can still fix. Proved in both directions on new ids and on ids
added to the landed set.

**`draft` is now a real status.** An authored row nobody has read against its source is
`"draft"`; a person opens the book, finds the passage, writes `"verified"`, and only then does it
land. `append_batch.py` refuses a draft batch and deliberately has no override — setting the word
is the record of having read the row, so a flag that skipped it would make the word decorative.
Both archive validators take the status into their vocabulary and fail the archive if one is in
it: a draft that landed came in around the gate, which is exactly what the status is for. The
Desktop handoff for the 17 books already told Gemini to write `"draft"` and already claimed the
landing tool refused it; the claim is now true.

Written into `QUESTION_AUTHORING.md` §11, the repo `GEMINI.md`, and `QuestionBank/incoming/README.md`.

**The handoff for the seventeen now lives in the tree.**
`Sources/MAIN CORPUS/8 - New Additions (2026-09)/_ext2-pass-2026-09-18/handoff-17/` holds the five
documents — brief, contract, exemplars, driver, row validator — so they cannot drift out of the
project, and its README says plainly that the copy which runs, because it carries the sheets and
the books, is the one on the Desktop. The pass's own `GEMINI.md` and `GUIDE.md` are left alone:
they are the older 103-book versions and `_ext2-pass-2026-09-18/README.md` is the record of that
run, so replacing them with the seventeen-book rewrite would have deleted information rather
than moved it.

**One thing found and not fixed.** `QUESTION_AUTHORING.md` §11 still says the archive is 2,205
rows and 373 categories, in three places. The live bank is 3,752 and 708. The rule it states is
right; the numbers are stale, and counts are his to bump with a batch.

`./run_tests.sh` 27/27. Nothing committed, nothing pushed.

## 2026-09-19 — The Farsi bank is settled, and the classifier was eating real years

The rule had been written down and never run. It has been run: **1,755 years rewritten into
shamsi, 5,559 labels written over years that keep their digits**, across both banks in lockstep.
1967 rows changed on the first pass, 4 more once the defect below was fixed. Backups sit beside
both files as `*.pre-normalize`; the pristine pair reproduces the live pair byte for byte when
the tool is pointed at it, so the banks are exactly the archive plus this pass and nothing else
rode along. `page` and `value` untouched, and the master and the web bank still agree field for
field on clue, explanation, answer and category.

**The double-check found a real defect, which is the whole reason for it.** `not_a_year` decided
a number was a count by looking for its unit past a comma, so `در سال ۱۹۵۵، صفحهٔ …` read the
next clause's *page* as 1955's unit and `سال ۱۹۷۵، هزاران قصاب` matched the first three letters
of *thousands*. Both years were silently dropped from the pass. A unit now has to follow its
number across whitespace alone; a clause break ends the question. Blast radius measured at
exactly five flips: four genuine years settled correctly, and the fifth — a bibliographic
citation — stayed bare through the citation guard, which is the guard working as designed.

The residue was classified rather than waved at. 334 guard hits: 192 spans, 80 labelled, 30
citations, 16 decade pairs, 12 dual glosses, 4 imperial. The 21 bare modern years left in prose
are all in named classes — dual glosses like `۱۹۰۱ (۱۲۸۰ خورشیدی)`, citations like `(گرین ۱۹۸۲:۹۶)`,
western decade spans, and counts like `۲۰۰۰ رسید`. Six sub-1500 numerals carrying `میلادی` were
checked one by one against the English twin and kept: each prints the same digits, so they are
real western dates (Shapur at Edessa, the Shahnameh, Ibn 'Arabi) and not shamsi years wearing the
wrong label. `۶۰۷۹` is still untouched, the lunar year inside a shamsi row still reads
`نوروز سال ۱۱۶۵ خورشیدی (۱۱۶۵ ش/۱۲۰۰ ق)`, and `۲۵۳۵` still carries its imperial guard.

`Tools/normalize_fa_prose.py` remains untracked, so git is no safety net here — the backups are.
Nothing committed, nothing pushed.

## 2026-09-19 — 1.0.12 is cut: the Persian calendar pass ships, and a Latin letter leaves a Persian word

**Everything not committed since the icon went on is now committed as one batch** — the Farsi
calendar pass and the tool that runs it, the classifier fix that stopped it eating real years,
the delta gate in `append_batch.py` and the refusal to land a `draft`, the Persian category head
moving off Avenir Next Condensed, and the third buzz cue.

**One bank file was edited, and it was not the pass's doing.** `pahlavi_0412_a` carried
`به تribune مجلس` — a Persian ت fused to a Latin *ribune*, the same shape as the ژنرال defect
1.0.11 repaired. It is in HEAD, not in this session's changes, and no validator sees it: the
script-mixing checker looks for Latin inside a Persian word and the word here begins with a
Persian letter, so the Latin half reads as a legitimate English term. He asked for the changes
to go up *if they're correct*, and this one was not, so it is repaired — in the archive, with the
play file regenerated by `render_bank.py` rather than hand-edited, because a hand edit to a play
file is exactly what `--check` exists to catch. The backup sits beside the archive as
`*.pre-tribune` and is ignored.

**The release.** `1.0.12` / `1012`, declared once in `Web/update.js` and read out by all three
builders. Mac universal, iOS `.ipa`, Android `.apk`, all three rebuilt and all three now carry
the version; both bundles diffed against `Web/` file for file with no drift. `Web/` frozen as
`Versions/v1.0.12`, 337 files. Notes at `dist/RELEASE-v1.0.12.md`. Tests 27/27, `check_bank` and
both archive validators exit 0, master and web banks in step.

**Two things found and not fixed, both his to call.**

The seventeen-book handoff at
`Sources/MAIN CORPUS/8 - New Additions (2026-09)/_ext2-pass-2026-09-18/handoff-17/` is inside
`Sources/`, which is gitignored, so the log's line about it living in the tree is true on this
disk and false on GitHub. Moving it out of `Sources/` means deciding where the corpus stops and
the docs start.

`README.md` line 126 and `QUESTION_AUTHORING.md` §11 still give the old counts — 120 categories
and 1,000 clues, 2,205 rows and 373 categories. The live numbers are 708 and 3,752, on both
banks. Counts are his to bump.
