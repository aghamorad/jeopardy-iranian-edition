# C3PO — work log

Running record of what Claude (C3PO) changed in this project and what was actually
verified. Newest entry first. Other agents in this tree keep their own logs under
their own names — this file is mine.

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
