# C3PO — work log

Running record of what Claude (C3PO) changed in this project and what was actually
verified. Newest entry first. Other agents in this tree keep their own logs under
their own names — this file is mine.

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
