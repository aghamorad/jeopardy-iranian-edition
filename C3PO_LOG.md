# C3PO — work log

Running record of what Claude (C3PO) changed in this project and what was actually
verified. Newest entry first. Other agents in this tree keep their own logs under
their own names — this file is mine.

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
  site — but Pages is not yet enabled on the repo (API 404), and the first run's
  `configure-pages` step (`enablement: true`) is what flips it on.
- **Copyright, Morad's call not mine.** The 1000 clues are written from ~60 copyrighted
  reference books, and `Corpus/` (280K) plus `QuestionBank/` (9.7M) are tracked in that
  public repo. A Pages URL only increases discoverability of what is already exposed.

### Open

- **Publishing is still held** by Morad's "only pushed to github when it's absolutely
  ready". Three files are modified in the working tree and nothing is committed:
  `Web/app.js`, `Web/styles.css`, `Web/index.html`.
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
