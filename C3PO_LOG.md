# C3PO — work log

Running record of what Claude (C3PO) changed in this project and what was actually
verified. Newest entry first. Other agents in this tree keep their own logs under
their own names — this file is mine.

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
  machine, so the controller path has **never** been visually verified.
- The wager quick-buttons wrap awkwardly ("Quarter | Half | Three Quarters" with "All In"
  centred alone on a second row); LOCK IT IN sits far below the slider; "Quarter" yields
  $300 on a $1,000 max because of `Math.round(max * 0.25 / 100) * 100`.
- `Web/assets/emblem.png` is unreferenced dead weight but lives *inside* the tree, so by
  the location rule it stays.

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
