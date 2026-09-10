# Jeopardy! Iranian Edition — Progress Handoff

**Project:** `/Users/Morad/Desktop/Jeopardy - Iranian Edition`
**Written:** 2026-09-10, after the previous session was cut off by server overload.
**Goal:** A polished, playable, TV-broadcast-quality Iranian Jeopardy-style game — judged only by the running release `.app`, never by "it compiles."

---

## ✅ Done so far

### Latest verification — 10 September 2026
- `./run_tests.sh` passes **26/26** (the earlier 23/23 note is stale).
- `./build_release.sh` succeeds and refreshes both `dist/Jeopardy Iranian Edition.app` and the root app bundle.
- `App/Resources/persian_clues.json` is valid JSON with **1,000 entries** and is present in both fresh release bundles.
- Fresh bundles contain `buzz.wav`, `correct.wav`, `incorrect.wav`, and `host_challenge.mp3` under `Contents/Resources/Sounds/`.
- In-game menu is now a full-screen broadcast-style control-room page rather than a small modal overlay.
- فارسی is explicitly labeled `UNDER CONSTRUCTION` in opening and settings; mixed-language Persian content is not presented as finished.
- Accepted buzz no longer plays the harsh duplicate `armed.wav`/`buzz.wav`; it uses a quiet system chime, and other cue volumes are reduced.
- Buzz updated again per user: packaged `classic_gameshow_BUZZ.wav` plays once only for accepted physical presses; arming/bots stay silent.
- Round progress rail uses an opaque backing to hide the legacy tab labels baked into `board_reference`.
- Latest verification: **27/27 tests pass** and the signed release build succeeds.

### Stability & build
- **Fixed the mic-engine crash** in `GameEngine/Speech/Engines/WhisperSpeechEngine.swift` — an `inputTapInstalled` guard now prevents removing an input tap that was never installed when a new match stops an uninitialized audio engine. Test suite: **23/23 passing** via `./run_tests.sh` (use this, not bare `swift test` — the sandbox blocks the manifest compile).
- **Release pipeline works:** `./build_release.sh` produces `dist/Jeopardy Iranian Edition.app` (~48 MB, copied to project root too). Occasional dsymutil/SwiftPM-lock failures are environment permission issues — rerun, they clear.
- **Fixed the zero-window launch bug** (app ran with audio but no visible window after state restore): switched `WindowGroup` → `Window("Jeopardy Iranian Edition", id: "main")` in `AppMain.swift` and added a `JeopardyAppDelegate`. Confirmed visible window afterwards via CoreGraphics window listing. Also cleared stale `NSWindow Frame` defaults.

### Visual redesign (the big one)
- **Replaced the old brown-and-gold template** with a rebuild directly on top of the supplied reference designs in `Designs to Base Everything On/` (1672×941 plates: monochrome Tehran night skyline, Milad Tower, black glass stage, green left / red right washes, white condensed type).
- New `App/Views/ReferenceShowViews.swift` (~570 lines at last count) containing `ReferenceLobbyView`, `ReferenceBoardView`, `ReferenceClueView`, wired into `AppMain.swift` in place of the old `LobbyView`/`BoardView`/`ClueActiveView` for those phases.
- Opening/splash screen reworked: no more duplicate "press any key" prompt, no profanity, generated `opening_stage_v2.png` cinematic backdrop (later deprioritized in favor of the reference plates).
- Lobby fixes: clue count corrected **650 → 1,000**, Start button now has `.keyboardShortcut(.defaultAction)` + accessibility identifier.

### Audio
- **Music continuity:** `Start Game` no longer stops the music. Continuous scored music across menu → board → clues (dedicated `musicPlayer` in `Theatre.swift` with ducking under host lines). Added `thinking_loop.wav` (from `Jeopardy Sounds/iranian_jeopardy_thinking_loop_30s.wav`).
- **Corrected sound cues** (previously mismatched):
  - `buzz.wav` ← `jeopardy_buzzed_first_lockin.wav`
  - `correct.wav` ← `jeopardy_correct_answer_happy.wav`
  - `incorrect.wav` ← `jeopardy_wrong_answer_buzzer.wav`
- Fixed a shadowing bug where the female host's opening recording was being overridden by a same-named WAV — now loaded as `host_challenge.mp3` (`playOpeningChallenge()` in `Theatre.swift`).
- Removed a duplicated "buzzers armed" sound trigger in `AppMain.swift`.

### Menus & flow
- **Pre-match green room / setup flow:** "Start Game" now opens a setup overlay that asks **answer format first** (Type/Speak response vs. Multiple Choice), editable contestant names, human/bot mixing, and Continue-saved-game — so players don't dig through Settings mid-game.
- **In-game MENU button** with Save, Save & Main Menu, New Match, Save & Quit.
- Host renamed **"Bibi Zangzadeh"** with Don Rickles-style snarky host ruling cards after right and wrong answers (in `HostPersona.swift`).

### Answer judging
- **Jeopardy-style leniency** in `AnswerResolver.swift`: surname-only acceptance for distinctive names, and Persian transliteration tolerance (e.g. "Mosadeq"/"Mossadegh"/"مصدق" all accepted). Matching tests added to `Tests/main.swift` — passing.

### Controllers
- `ControllerManager.swift` rebuilt around **controller family detection**: PlayStation shows △/□/○/× in the pad's diamond layout; Xbox shows Y/X/B/A. Buzz = × (PS) / A (Xbox) with a mini glyph prompt next to the buzz button; multiple-choice options map to the diamond with **hold-to-select**. Connected-controller list shown in the lobby.

### Persian / Farsi version (in progress)
- Language choice (English / فارسی) added to the splash/opening in the same visual style (`OpeningView.swift` with `selectedLanguage`, arrow-key + click selection), setting `gameState.configuration.language`.
- Persian scaffolding in place: `GameEngine/Localization/PersianClueCopy.swift`, `QuestionBank.localized(_:language:)`, `BoardBuilder` now serves localized clues, `PlayerCopy` with Persian numerals (۰–۹) and RTL support. **Voice-over and music stay English** — only text switches.
- Local Ollama translation (qwen2.5:3b, TranslateGemma) was tried and **abandoned** — quality was garbage (repetitive nonsense text). User said they'd supply the translated bank themselves.
- **`App/Resources/persian_clues.json` now exists** (user supplied it just before the crash) — it was located by `find` but **not yet wired into the game**.

---

## 🔴 What's left (in rough priority order)

1. **Wire in the Persian question bank.** `App/Resources/persian_clues.json` is sitting in Resources but the loading path (`QuestionBank` / `BoardBuilder`) hasn't been pointed at it yet. Verify: Persian clues, categories, answer options, accepted answers all render RTL, and a full Persian game is playable.
2. **Finish the full-screen staged menu.** The current in-game MENU button/overlay was flagged as "really weak" — mid-rework to become a proper full menu *page* in the same visual language as the lobby (clean styled buttons, not a small overlay). This was the task in flight when the session died.
3. **Host name pun still not good.** "Bibi Zangzadeh" was rejected feedback ("the pun of the host isn't good"). Needs a sharper, funnier Persian pun — ask the user for direction or propose options.
4. **The mandatory final validation pass** (per the BUILD RULE) — has not been completed since the last round of changes:
   - `./run_tests.sh` (expect 23/23)
   - `./build_release.sh`
   - Kill every running `JeopardyApp`, launch the **exact new dist bundle**
   - Play a representative full game in **both languages**: splash language choice → setup (names, format) → board → clue → buzz → answer (typed + spoken + multiple choice) → wager → Final → winner presentation
   - Verify in the running app: music continuity through category selection and rounds, correct buzz/correct/incorrect sounds, host voice lines, controller glyphs + hold-to-select with a real controller, save/continue/quit flows
5. **Verify the bundle contents** — confirm `dist/.../Contents/Resources/Sounds/` holds the corrected buzz/correct/incorrect files and `host_challenge.mp3`, and that `persian_clues.json` is copied into the bundle by `build_release.sh` (check the script's resource-copy list — it may need a new line for this file).
6. Smaller known gaps from earlier passes (verify they're actually closed): lobby "How to Play" overlay polish, winner-presentation screen quality vs. the reference designs.

---

## 📝 Session notes for whoever continues

- The repo is a git repo with **no commits yet** — everything is uncommitted. A first commit would be cheap insurance before the next big change.
- Useful tooling already in the project: `build_release.sh`, `run_tests.sh`, `Tools/run_speech_benchmark.swift`, `/tmp/find_jeopardy_window.swift` (CGWindow listing — the accessibility bridge was flaky last session, reporting 0 windows while CoreGraphics showed the window fine; trust the CG helper).
- The user's standard: **"If I open the app with no knowledge of the code, does it immediately look, sound and play like a complete, high-quality Iranian Jeopardy-style game show?"** If no → keep building. Compiles/tests-passing is never the finish line.
- macOS automation last session was fighting the agent (focus stealing by Telegram/Chrome/Mail, App switcher not finding the app by name). Direct binary launch + `osascript` frontmost + `screencapture -l <windowID>` was the working recipe.
