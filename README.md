# JEOPARDY! — Iranian Edition

Ask an Iranian about Iranian history and the answer comes immediately. Ask the next
Iranian and the answer is different, and just as immediate. This game is built on that.

Three contestants, six categories a round, one buzzer each. Single Jeopardy, Double
Jeopardy, a Daily Double hiding in each round, and a Final where you wager before you see
the clue. The categories are the ones people actually fight about: empires that fell
apart, revolutions that went sideways, poets, oil, and whatever your uncle is so sure
about.

Play it in a browser: <https://aghamorad.github.io/jeopardy-iranian-edition/>

## Take it with you

Three builds, all on the [Releases page](https://github.com/aghamorad/jeopardy-iranian-edition/releases/latest):

| File | Size | Runs on |
| --- | --- | --- |
| `Jeopardy-Iranian-Edition-macOS-universal.zip` | 13 MB | macOS 14 or later, Intel or Apple silicon |
| `Jeopardy-Iranian-Edition-iOS.ipa` | 14 MB | iOS or iPadOS 17 or later, iPhone and iPad |
| `Jeopardy-Iranian-Edition-web-beta-N.zip` | 11 MB | any browser — unzip and open `index.html` |

The first two are the web show in a native shell, so they carry the same `Web/` tree the
zip does. Take the zip if you want the show without installing anything.

Same thousand clues, same music, same host voice, same icon, in all three versions. The
Mac one has both architectures inside a single binary. The iPhone one is the entire show
packed up; it never asks the network for anything.

### Neither one is signed

No developer account, so no signature and no notarization. On a Mac that means Gatekeeper
takes one look and says no. Right-click the app, choose **Open**, then **Open** again in
the dialog. Or clear the flag once:

```bash
xattr -dr com.apple.quarantine "/Applications/Jeopardy Iranian Edition.app"
```

On an iPhone the `.ipa` will not install by dragging it into Finder. It has to be re-signed
with an Apple ID first, which is what the tools below are for.

### Getting the .ipa onto an iPhone

Pick the one that fits the computer you actually have:

- **[SideStore](https://sidestore.io)** — signs on the phone itself. Set it up once with a
  computer, then install and refresh from the device, no cable again. Closest thing here to
  a normal app.
- **[AltStore](https://altstore.io)** — the original. Wants AltServer running on a Mac or PC
  on the same Wi-Fi whenever you install or refresh.
- **[Sideloadly](https://sideloadly.io)** — no app on the phone at all. Plug it in, drop the
  `.ipa` on the window, type your Apple ID, and it signs and installs over the cable. Least
  setup, most repetition.
- **[LiveContainer](https://github.com/LiveContainer/LiveContainer)** — one host app that
  runs the `.ipa` inside it, so the game doesn't eat one of your three app slots.

All of them want a free Apple ID, and a free Apple ID comes with two rules: the app dies
after **seven days** and has to be refreshed, and you get **three** sideloaded apps at a
time. If your iOS version is inside
[TrollStore](https://github.com/opa334/TrollStore)'s range, use that instead. It signs
permanently and every caveat above stops applying.

Use your own Apple ID. Signing someone else's app with yours is a fine way to lose your
account.

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
history to the 1953 coup. Single-round clues are worth 10 to 200 million toman; the Double
round runs from 20 to 200.

## One game, three front ends

The show is a build-free static web build under `Web/`, which plays on its own in a
browser. The macOS and iOS apps are native shells wrapped around that same tree. One show,
three ways to open it.

| Path | What it is |
| --- | --- |
| `GameEngine/` | A Swift rules engine. **Neither app imports it** — only `Tests/` does. See `ARCHITECTURE.md`. |
| `App/` | The macOS and iOS shell: three Swift files wrapping a web view. |
| `App/Resources/` | The app icon, plus a legacy store of stage art and sounds. Only `AppIcon.icns` is used. |
| `QuestionBank/` | The clue corpus: `verified_clues.json` and the Persian copy. |
| `Tests/` | Test runner. An executable target, not XCTest. |
| `iOS/` | iOS shell. Generated from `project.yml`. |
| `Web/` | Static web build. Desktop and mobile. No build step. |
| `Versions/` | The web build frozen, one folder per release. Kept so a working show can be got back to. |
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

## Freezing a version

Every release also freezes the web build under `Versions/`, so a show that worked can
always be got back to even if `Web/` goes sideways later. Names only go forward — the
script refuses to overwrite a folder that already exists.

```bash
./snapshot_web.sh beta-3
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
