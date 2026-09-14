# Architecture

The show is one static web build. The macOS and iOS apps are native shells that display
it. There is no second implementation of the game and no native UI to keep in step.

```
Web/                 the show: rules, scoring, timers, judging, design, audio, clues
  app.js             the real game engine
  styles.css         the shared visual design
  i18n.js            232 UI keys per language and language selection
  answers.js         write-in judging
  net.js             PeerJS transport for online controllers
  editions.js        bilingual edition registry: MAIN plus every course
  data/clues_fa.js   MAIN's Persian bank, embedded as window.CLUES_FA
  index.html         the shell
  data/clues.js      MAIN's English bank, embedded as window.CLUES
  courses/<id>/      one self-contained course per folder: registration, skin,
                     its two banks, its art
  assets/            art and audio

App/                 macOS shell: three Swift files, no game logic
  AppMain.swift
  ShowWebView.swift
  iOSApp.swift

iOS/                 iOS shell, generated from project.yml by xcodegen

GameEngine/          a Swift rules engine the shipped apps DO NOT use
Tests/               the only thing that imports GameEngine
QuestionBank/        canonical clue bank (verified_clues.json)
Versions/            the web build frozen, one folder per release
```

## Web

Plain HTML, CSS and JavaScript with no build step. It runs off `file://` because the
clues are embedded as `window.CLUES` rather than fetched, so the same tree works in a
browser and inside an app bundle. `Web/app.js` holds the rules; `Web/styles.css` holds
the design. Rule values are in [GAME_RULES.md](GAME_RULES.md).

## App

Three files. A `WKWebView` pointed at the copy of `Web/` that the build places inside the
bundle. `Package.swift` shows `JeopardyApp` has **no dependency on
`JeopardyGameEngine`** and bundles no assets of its own, deliberately: the Mac app is a
window onto the web show, not a copy of it.

## iOS

Generated, not committed. `iOS/project.yml` is the spec; `*.xcodeproj` is gitignored so the
project cannot drift from it. Both targets take `../App` (excluding `App/Resources`) and
`../Web` as a folder reference.

## GameEngine — read this before touching it

`GameEngine/` is a Swift library that implements rules, scoring, the board, players,
controller input and the question bank. **Neither shipped app imports it.** The only
importer is `Tests/main.swift`, so the Swift engine is exercised by the test suite and by
nothing a player runs.

Treat it as a rules oracle, not the game's brain. A change to how the game actually plays
belongs in `Web/app.js`. Whether to keep the Swift engine, or to make it authoritative, is
an open decision.

## The two kinds of bank

**MAIN** — the edition called `general` — is the whole of Iran: everything ever designed.
Its archive is `QuestionBank/verified_clues.json` and `verified_clues_fa.json`, canonical
for English and Persian respectively. **A course** is one syllabus, an aspect of that same
material, and its bank is written straight into `Web/courses/<id>/data/bank-*.js` in the
play shape — a course has no archive behind it.

Every question may go to MAIN. A course never leaks into another course, and MAIN never
leaks into a course. The mechanism is the global: the engine deals a show only the array
it registered, so MAIN plays `window.CLUES` and a course plays only its own
`COURSE_CLUES_<ID>`. See `BANK_SCOPE.md` for the rule and `AGENTS.md` for which one you
are writing.

MAIN's play file, `Web/data/clues.js`, is a derived copy re-serialised as `window.CLUES`,
generated from the archive by `Tools/render_bank.py` through a fixed field map.
`python3 Tools/render_bank.py --check` detects drift, and a hand edit to the play file is
overwritten by the next run. **Writing a MAIN clue means editing the archive, then
regenerating.** Every clue carries book, author, chapter, page and the source passage;
`Docs/ASSET_CREDITS.md` covers asset provenance.

The two shapes do not share field names — the archive uses `clue_text` /
`canonical_answer` /
`accepted_aliases` / `correct_option_index` and a flat `host_reactions` dict, the play file
uses `clue` / `answer` / `aliases` / `correct` and the `correctLine` / `wrongLine` strings
that actually play. See [QUESTION_AUTHORING.md](QUESTION_AUTHORING.md) for the field map,
the value ladder, the difficulty mapping and the host's register.

## Builds and the release trail

- `build_release.sh` compiles the universal macOS binary, assembles `dist/Jeopardy Iranian
  Edition.app`, copies `Web/` to `Contents/Resources/Web`, copies the icon from
  `App/Resources/AppIcon.icns`, writes the `Info.plist`, and finally copies the bundle to
  the repo root. That root `.app` is a build artifact, not a second app.
- `snapshot_web.sh <name>` freezes `Web/` into `Versions/<name>`. Names only go forward;
  the script refuses to overwrite.
- `dist/` and `Versions/` are the release trail and stay in the tree even though `dist/` is
  gitignored.
- Both binaries are unsigned. There is no developer account, so the `.ipa` needs re-signing
  and the Mac app needs a right-click Open. Details in [README.md](README.md).

## Design

The shipped visual truth is `Web/styles.css`; `STYLE_SHEET.md` describes it.
Mockups in `Designs to Base Everything On/` establish the look. A course that wants its
own look ships `Web/courses/<id>/course.css`, which loads after `styles.css` and overrides
it — keyed to `html[data-edition="<id>"]`, so its rules reach nothing while MAIN is on the
floor.

The previous look is retired. `tehranStudio`, `BroadcastTitle`, `ArchivalPanel` and
`ArchivalTheme` are phantoms; their presence anywhere means something was reintroduced by
mistake.

## Known loose ends

- `App/Resources/` is largely a legacy store (old stage art, badges, host lines, a Persian
  clue file). Only `AppIcon.icns` is consumed by the build.
- `build_release.sh` runs `swift build` inside a command substitution, so a failing compile
  does not abort the script.
