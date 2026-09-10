# JEOPARDY! — Iranian Edition

An Iranian-history edition of the quiz show format. Six categories per round, six
questions each, three contestants, buzz-in answering, Daily Doubles and Final Jeopardy.
Content is sourced and cited rather than invented — every clue carries a reference back
to the book it came from.

The game runs on macOS and iOS from one shared Swift codebase, and in any browser from
a build-free static copy under `Web/`.

## Layout

| Path | What it is |
| --- | --- |
| `GameEngine/` | Rules, scoring, board, players, controller input, question bank. Platform-free. |
| `App/` | The show itself — SwiftUI views, theme, audio direction. Shared by macOS and iOS. |
| `App/Resources/` | Stage artwork, sounds, icons. |
| `QuestionBank/` | The clue corpus (`verified_clues.json` and the Persian copy). |
| `Tests/` | Automated test runner (an executable target, not XCTest). |
| `iOS/` | iOS app shell. Generated from `project.yml`. |
| `Web/` | Static web build of the show — desktop and mobile. No build step. |
| `Tools/`, `script/` | Build and content tooling. |
| `Sources/` | Reference books the clues were written from. **Not in the repo** — see below. |

## Building

Requires macOS 14+ and Swift 5.9+.

```bash
./run_game.sh
```

That compiles a release build, assembles `dist/Jeopardy Iranian Edition.app`, and launches
it. To only produce the bundle without launching:

```bash
./build_release.sh
```

Tests:

```bash
./run_tests.sh
```

## iOS

The iOS project is generated, not committed — `*.xcodeproj` is gitignored so it cannot
drift from the spec. To open it:

```bash
brew install xcodegen
cd iOS && xcodegen generate
```

Then open `iOS/JeopardyIranianEdition.xcodeproj`. The app icon, asset catalog and
Info.plist are committed; only the project file is generated.

## Web

`Web/` is a build-free static copy of the show — the same rules, clues, scoring and
audio as the Swift app, in plain HTML/CSS/JS. It works from `file://` (double-click
`index.html`) because the clue bank is embedded as `window.CLUES` rather than fetched,
and it is responsive: one layout on a laptop, another on a phone, both touch- and
keyboard-playable.

To serve it locally:

```bash
python3 -m http.server 8788 --directory "Web"
```

Then open <http://localhost:8788>.

`Web/data/clues.js` is a derived copy of `QuestionBank/verified_clues.json` — the same
1000 clues, re-serialised as `window.CLUES` so no HTTP request is needed. There is no
generator script yet, so the two must be kept in step by hand. The web build is
English-only for now; it is structured so the Persian bank can drop in later.

## What is not in this repo

`Sources/` holds roughly sixty reference books — the corpus the clues were written from.
They are copyrighted and several are near GitHub's per-file size limit, so they stay
local. Everything needed to build and play is here; everything needed to *author new
clues* is not.
