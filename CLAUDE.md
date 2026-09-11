# CLAUDE.md

Iranian Edition of Jeopardy. Three contestants, six categories a round, a clue bank of
one thousand sourced questions. Read this, then `ARCHITECTURE.md`, then `GAME_RULES.md`.
That is the whole bootstrap.

## The one thing to get right

**The web build is the product.** `Web/` is the show. The macOS and iOS apps are WebView
shells around it. There is no second native implementation of the game, and there is no
native UI to keep in step. Change `Web/` and all three builds change together.

Corollary: never treat `GameEngine/` as the game. It is a Swift rules engine that the
shipped apps do not import. Only `Tests/` uses it. See `ARCHITECTURE.md`.

## The look is settled

The design is the "sleek" version: monochrome Tehran skyline, black glass stage, white
condensed type, green and red washes. Source mockups are in
`Designs to Base Everything On/`; the only implementation is `Web/styles.css`.

Everyone works from the same contract: `STYLE_SHEET.md` at the project root. It carries
the palette, the three type stacks, the geometry scale, the component vocabulary, the RTL
rules, and the discarded look. Read it before changing `Web/styles.css` and before adding
a screen. If `styles.css` and the style sheet ever disagree, `styles.css` is what the
audience sees and the style sheet is what is wrong.

The previous brown-and-gold design is retired and must not be reintroduced. If you find
`tehranStudio`, `BroadcastTitle`, `ArchivalPanel`, or `ArchivalTheme` anywhere, that is a
phantom and it is wrong.

The host is smug, snarky and mean. That register governs every line of in-game copy, in
both languages.

## One build, two languages

English and Persian are the same game, not two games. There is no separate Persian build
and no Persian-only front end; the language is chosen on the splash and everything
downstream follows. `Web/data/clues.js` (`window.CLUES`) and `Web/data/clues_fa.js`
(`window.CLUES_FA`) are the two banks, both a thousand clues in the same shape;
`Web/i18n.js` holds every string in both, in two tables kept at exact parity; `Web/answers.js`
is the write-in judge. The Persian edition wears a `[BETA]` seal while the host's voice
stays English.

Answers are given either by multiple choice or by typing, chosen per match in the green
room, alongside who is sitting in the other two seats — people, or robots at one of four
difficulties.

## Commands

```bash
./run_game.sh
```

```bash
./build_release.sh
```

```bash
./run_tests.sh
```

```bash
python3 -m http.server 8788 --directory "Web"
```

```bash
./snapshot_web.sh beta-4
```

`run_game.sh` compiles and launches; `build_release.sh` only assembles `dist/`;
`run_tests.sh` is the test runner (use it, not bare `swift test`); `snapshot_web.sh`
freezes the web build under `Versions/` for a release.

## Working on this project

- Keep the work log in `C3PO_LOG.md`. Append a dated entry; never rewrite an older one.
  Record decisions and their reasons, not a transcript of what you did.
- Prose in the log and in docs follows his voice. No filler, no preamble, no summary of
  what a diff already shows.
- Move files to `~/.Trash` with `mv`. Never `rm`.
- `dist/` and `Versions/` are the release trail. Both are in the tree on purpose, even
  though `dist/` is gitignored.
- Never commit or push without being asked.
