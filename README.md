# JEOPARDY! — Iranian Edition

Ask an Iranian about Iranian history and the answer comes immediately. Ask the next
Iranian and the answer is different, and just as immediate. This game is built on that.

Three contestants, six categories a round, one buzzer each. Single Jeopardy, Double
Jeopardy, a Daily Double hiding in each round, and a Final where you wager before you see
the clue. The categories are the ones people actually fight about: empires that fell
apart, revolutions that went sideways, poets, oil, and whatever your uncle is so sure
about.

Play it in a browser: <https://aghamorad.github.io/jeopardy-iranian-edition/>

## The clues have receipts

There are a thousand of them. Every one carries the book it came from, the author, the
chapter, the page, and the passage the clue was pulled out of. All five fields, on all
thousand clues, no gaps.

Forty-nine books are behind that bank, shelved by period:

| Shelf | Books |
| --- | --- |
| General history, multi-era | 4 |
| Safavid, Afsharid & Zand, 1501–1796 | 3 |
| Qajar & Constitutional, 1796–1925 | 3 |
| Pahlavi & Mosaddegh, 1925–1979 | 10 |
| Revolution & Islamic Republic, 1979–present | 9 |
| Biographies & memoirs | 8 |
| Society, culture & ideas | 12 |

The bank runs across 120 categories and 1,000 clues, from Safavid chronicles to cinema
history to the 1953 coup. Single-round clues are worth 200 to 1,000; the Double round
doubles that.

## One game, three front ends

The show runs on macOS and iOS from a single Swift codebase, and in a browser from a
build-free static copy under `Web/`. Same rules, same clues, same scoring, same audio.

| Path | What it is |
| --- | --- |
| `GameEngine/` | Rules, scoring, board, players, controller input, question bank. No UI. |
| `App/` | The show itself: SwiftUI views, theme, audio direction. Shared by macOS and iOS. |
| `App/Resources/` | Stage artwork, sounds, icons. |
| `QuestionBank/` | The clue corpus: `verified_clues.json` and the Persian copy. |
| `Tests/` | Test runner. An executable target, not XCTest. |
| `iOS/` | iOS shell. Generated from `project.yml`. |
| `Web/` | Static web build. Desktop and mobile. No build step. |
| `Tools/`, `script/` | Build and content tooling. |
| `Sources/` | The forty-nine books the clues came from. **Not in the repo.** See below. |

## Building it on macOS

Needs macOS 14 or later and Swift 5.9 or later.

```bash
./run_game.sh
```

That compiles a release build, assembles `dist/Jeopardy Iranian Edition.app`, and launches
it. To get the bundle without the launch:

```bash
./build_release.sh
```

Tests:

```bash
./run_tests.sh
```

## iOS

The Xcode project is generated, not committed, so `*.xcodeproj` stays gitignored and
cannot drift away from the spec that produces it.

```bash
brew install xcodegen
cd iOS && xcodegen generate
```

Then open `iOS/JeopardyIranianEdition.xcodeproj`. The app icon, the asset catalog and the
Info.plist are committed. Only the project file is generated.

## Web

`Web/` is the same show with no build step: plain HTML, CSS and JavaScript, the same
clues and scoring and audio as the Swift app. Double-click `index.html` and it runs off
`file://`, because the clue bank is embedded as `window.CLUES` instead of fetched over
HTTP. The layout changes between laptop and phone; both touch and keyboard work.

To serve it:

```bash
python3 -m http.server 8788 --directory "Web"
```

Then open <http://localhost:8788>.

`Web/data/clues.js` is a derived copy of `QuestionBank/verified_clues.json` — the same
thousand clues re-serialised as `window.CLUES`. There is no generator script yet, so the
two are kept in step by hand. The web build is English-only for now, and structured so
the Persian bank can drop in later.

## Controllers

Plug in one controller per contestant. The first one is Player 1, the second is Player 2,
and so on, and each controller buzzes for its own player only. Every controller also
drives the menus and the board: d-pad or left stick to move, A to choose, B to go back,
Start for the match menu.

## What is not in this repo

`Sources/` is 1.1 GB of the forty-nine books the clues were written from, and they are
copyrighted, and several of them sit close to GitHub's per-file limit. So they stay on my
disk. Everything you need to build and play is here. Everything you need to write new
clues is not.
