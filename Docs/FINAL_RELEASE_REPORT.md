# Final Release Report

Date: 2026-09-09

## Current state

- Automated test suite: **18 passed, 0 failed**.
- Offline game engine, answer-resolution pipeline, two-stage round progression, and local match persistence are operational.
- Question bank: **30 verified clues**, all in the single round.
- Corpus: six core sources represented in the verified clue bank; the full 49-book corpus is not yet ingested.
- Physical controller and microphone testing require an interactive macOS session; terminal tests are simulation-only.

## Known blockers to version 1.0

- Final Round and full wager presentation/editorial workflows remain incomplete.
- Persistence writes atomically under Application Support and restores the active board/players/round; interactive crash-resume and controller/microphone hardware tests remain pending.
- Release compilation now succeeds with the installed Apple Swift 6.4 toolchain using `build_release.sh`; unsigned local packaging is replaced by an ad-hoc signed app bundle.

## Build artifacts

- Release app: `dist/Jeopardy Iranian Edition.app`
- Build command: `./build_release.sh`
- Test command: `./run_tests.sh`
- The release bundle includes `verified_clues.json` and no network services are required for its question bank.
