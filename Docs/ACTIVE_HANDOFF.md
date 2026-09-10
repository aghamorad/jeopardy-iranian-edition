# Active development handoff — 10 September 2026

## User requirement
Work directly in `/Users/Morad/Desktop/Jeopardy - Iranian Edition`. Deliver a polished playable native Iranian history quiz show. Build success is not completion. Inspect exact release GUI and verify images, sound, controls, complete rounds and Final. Keep this log current after substantial work. Do not erase original corpus, prior source or other agents' work.

## Current status
IMPLEMENTATION IN PROGRESS. Updated product has NOT yet passed a release build or live GUI validation. Do not call complete.

## Preserved originals
` .production-backups/20260910/` (without leading space) contains original App, GameEngine and build_release.sh. Git initialized in project. No corpus or question-bank source files altered.

## Implemented
- New original stage illustration `App/Resources/stage_isfahan.png`, actually rendered behind the game; existing background had only procedural gradients and a faint watermark.
- Rebuilt lobby with prominent title and start action, stage artwork, archive cards, contestant controls and expandable settings.
- New original raster app icon plus generated proper AppIcon.icns; packaging points to ICNS.
- Original instrumental score composed/rendered using macOS sampled mallets, strings, bass and percussion. ~57-second menu composition; 30-second Final; brief mastered cues. No television theme recording used. Packaged WAVs are 16-bit stereo. Instrument soundbank not redistributed.
- Neural recorded welcome `host_welcome.mp3`; three additional recordings generated but not yet downloaded/integrated (see next steps).
- Compact host bar replaces emoji portrait; clue speech status reflects actual synthesizer.
- Fixed controller A simultaneously buzzing AND choosing answer A. Added d-pad board selection and contextual A.
- Added arrow-key board selection, focus outline, Return/Space opening selected clue; typing no longer feeds contestant hotkeys.
- Stopped repeated buzz audio on every 0.1-second timer change and round fanfares on every board return.
- Fixed zero-dollar special-wager scoring, special-wager ceiling, option index bounds, player index bounds, stale bot answer callbacks, duplicate Final submissions, specificity-answer timeout.
- Rebuilt human Final entry: secure answer fields per human, submission lock, 30-second countdown, scoring only at reveal, ties represented.
- Added cancellation when leaving match, native Match menu, typed Return submission, live transcript display, 12-second answer window.
- All 325 original clues had correct option at index 0. Board construction now shuffles options while preserving correct index. Replay chooses fresh categories ahead of used ones.
- Removed misleading reversed-English Persian UI: setting now explicitly selects spoken-answer language. Full Persian content/UI remains outstanding.
- Speech recognizer checks actual Persian locale support, guards microphone format, invalidates delayed permission callbacks, and exposes runtime errors to typed fallback.

## Assets / rights
See Docs/ASSET_CREDITS.md. Two LOC photographs: Ahmad Shah Qajar (`2014683756`), Tehran family photochrom (`2017656787`), both catalogued no known restrictions. Tehran download succeeded. Qajar first download incomplete; retry currently pending and MUST validate image before using. Original generated stage is interpretive art, never present as archival evidence.

## Build failures and next action
First updated build failed because installed CLT macOS 27 SDK has no SwiftUI State macro plugin. Replaced newly added @State with @StateObject observable helper classes. Second build exposed missing `import JeopardyGameEngine` in App/Theme/ArchivalTheme.swift for HostAudioPlayer. Fix that import, then compile again; inspect all compiler errors.
Build log: `/Users/Morad/Documents/Codex/2026-09-10/referenced-chatgpt-conversation-this-is-an/work/release.log`.

## Pending work
1. Fix missing import, finish host recordings and credits, validate complete archive JPEG.
2. Add meaningful regression tests for zero wager, correct-index shuffle, duplicate Final and full match progression. Existing tests not yet rerun.
3. Complete stable project build-and-run script and Run action.
4. Build exact RELEASE .app, stop stale JeopardyApp process, open exact fresh root bundle, inspect GUI and exercise flows.
5. GUI access uses node_repl @oai/sky. Read computer-use skill. Full path first attempt timed out; bundle ID is ambiguous because root and dist share identifier. After fresh launch target exact root path. No actual GUI verification yet.
6. Assess remaining limitations honestly: all bank questions English; source quotations/pages inherited and not independently audited; full natural clue voice not implemented (recorded host plus optional macOS clue TTS); physical gamepad and actual speech recognition require runtime evidence. Do not falsely claim these complete.

## Tools / scripts
Intermediate implementation scripts are in `/Users/Morad/Documents/Codex/2026-09-10/referenced-chatgpt-conversation-this-is-an/work/`: upgrade.py, presentation.py, gameplay_finish.py, fix_build.py, package_assets.py, compose.swift. Do NOT rerun blind: string patches are one-shot. Source edits already present. Generated music in work/music.
Build: `./build_release.sh`; tests `./run_tests.sh`. Desktop mutations and audio component access required sandbox escalation (user explicitly authorized direct project work).

## Generated host recordings still to integrate
correct: https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/da358b75-85b1-40f1-986e-1aa744524e8c.mp3
wager: https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/7f85f20e-8aeb-4e1c-bc99-e2152bd1e3da.mp3
final: https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/17810400-4206-41c8-853c-7b52e7ddba98.mp3

## Update: gameplay regression coverage and recordings
Missing engine import fixed. Added four production regression tests (answer shuffle, zero wager, invalid inputs, two-round Final/duplicate scoring/replay); not run yet. Host correct/wager/Final integration added and downloads underway. New `script/build_and_run.sh` and `.codex/environments/environment.toml` provide release/build/launch. Qajar photo retry remains truncated at 131072/148868 bytes; resuming remaining bytes. Latest release build running.

## Update: first live GUI inspection
Fresh release built and launched successfully. Live screenshot confirms new stage imagery renders behind clue. Inspection discovered original reading/buzzer phases have NO mouse buzzer controls (EmptyView). Added contestant podium buzz buttons and No answer/reveal action; added vertical breathing space to clue presentation and contextual host text. These changes require next release rebuild. Qajar JPEG resumed successfully (148868 bytes expected; validate marker). Regression suite currently running.

## Update: host direction
Default clue narration is now enabled. The host reacts in audio after correct and incorrect resolutions, with sharper dry/mockingly theatrical remarks, and announces the champion at Final reveal. The visible host strip follows those reactions. This still uses macOS TTS for dynamic clues/reactions, with separate recorded deep-voice moments for welcome, correct, wager and Final. Rebuild and inspect are still required after this change.

## Update: settings and vocal direction
Settings is now a separate interactive page with Back to lobby and Done actions; it is no longer appended beneath the lobby. Dynamic narration defaults to Samantha rather than Daniel and uses punctuation-sensitive pacing/pitch for a more animated broadcast read. Recorded deep voice remains used for welcome/correct/wager/Final moments. The next release still needs rebuild and live page verification.

## Update: full clue reads and buzzer voice
Removed the eight-second clue speech cutoff; a 30-second watchdog now only handles a stalled synthesizer, so the completion callback normally arms the buzzer after the entire clue. Wager clues now receive the same full narration. Accepted buzzes trigger the buzzer cue and an audible host call of the contestant's name. Dynamic host delivery has a slightly faster, brighter broadcast cadence. Rebuild and live audio verification remain required.

## Update: theme switching
Theme selection now publishes a theatre pulse so Lobby, Board, Clue and backdrop colors redraw immediately. The backdrop gradient uses the selected theme's primary and secondary palette over the stage illustration; picker changes also play the selection cue. Settings remains a separate screen.

## Update: tooman economy and Iranian wordmark
Player-facing clue values, wagers, scores and speech normalization now use toomans. Single round values are 10,000,000 / 25,000,000 / 50,000,000 / 100,000,000 / 200,000,000; Double uses 20,000,000 / 50,000,000 / 100,000,000 / 150,000,000 / 200,000,000. Source clue tiers remain internal for matching. The attached Iranian emblem is bundled as `App/Resources/iranian_emblem.png` and replaces the O position in the wordmark with green/white/red coloring. Build and test still required.

## Update: tooman verification
Release build succeeded after the currency and wordmark changes. The full test suite now passes 22/22 after updating the board-value assertion to the new tooman amounts. The live settings page was previously verified with Back to lobby, theme radio selection and Done; theme selection visibly publishes a redraw pulse.
## Update: currency display bug found in live play
Live inspection found the clue header and scoring still reading the source bank's legacy clue value. The header now uses the board slot's tooman value, and ordinary clue awards/deductions use the slot value as well. The board itself already carried the new values.

## Update: written answers, Persian mode, typography, and expanded corpus
Voice answer capture is removed from the live game path. Human Classic mode is now Typed Response; the clue is shown in full, then the player types and locks the response. Multiple Choice remains available. Clue reading no longer invokes TTS, and the audio speech toggle is disabled. The app layout switches to RTL when Persian is selected, key answer controls are translated, Persian numerals remain active, and several categories have Persian pun titles. Value typography uses compact monospaced amounts with a separate تومان label. The question bank is expanded from 325 to 650 unique IDs through an encore round variant, with a production test asserting the count and uniqueness. Release build completed successfully after these changes; rerun the full suite after the added corpus test.

## Update: duplicate toman label corrected
Board value tiles now render the complete formatted amount once. The redundant standalone تومان line beneath each amount was removed. Release bundle rebuilt and signed successfully.

## Update: category puns and lobby wordmark
Added Jeopardy-style pun titles for the visible category headers, including “Rostam-atically Speaking,” “Amir Kabir? Amir Kidding!,” “Crude Awakening,” “The Spy Who Came in from Tehran,” and others, while preserving the original category keys for gameplay. Replaced the lobby’s plain JEOPARDY text with the Iranianized BroadcastTitle wordmark using the attached emblem in green, white, and red. Release bundle rebuilt and signed successfully.

## Update: buzzer reliability and wordmark scale
Accepted buzzes now post a shared game event at the engine boundary, so mouse, keyboard, and controller paths all invoke the same buzzer sound. The sound player stops the prior cue and boosts the buzzer volume to full. The Iranianized wordmark was enlarged and tightened on the board and lobby so the green-white-red emblem clearly occupies the O position in JE◉PARDY. Release bundle rebuilt and signed successfully.

## Update: clue music continuity and opening screen
Removed the board view’s music shutdown so the round music bed continues under clue presentation. Reinstated a direct buzz cue on the answering transition in addition to the shared engine event, covering all input paths. The lobby wordmark now sits in a centered framed show card for a cleaner opening impression. Release bundle rebuilt and signed successfully.

## Update: Persian labels and distinct theme compositions
Persian category display now always produces Persian text, including a Persian fallback for categories without a custom pun, and the board round title and typed-answer controls follow the selected language. RTL is now paired with visible Persian labels. Theme backdrops received distinct visual motifs for Isfahan, Tehran studio, Caspian, and Persepolis selections in addition to their palette changes, with artwork and composition layers changing per theme. Release bundle rebuilt and signed successfully.

## Update: final user-directed correction
Theme backgrounds now switch by scene source, not only by tint. Mouse buzzer actions call the buzz sound directly before state handling. Compact typography is live verified in the actual app: the clue header displays `۲۵ میلیون تومان` for a 25,000,000 slot. Release build succeeds and the full test suite passes 22/22. The exact fresh root bundle was relaunched for this verification. The current remaining limitation is voice quality: dynamic 325-clue narration still uses installed macOS speech, while deep recorded voice covers show moments; replacing every clue with a human or neural recording would require generating and packaging 325 separate recordings.
