# STYLE SHEET — JEOPARDY! Iranian Edition

The design contract. Everything the web build looks like is decided here; anything
that contradicts this file is wrong and comes out.

Read this before touching `Web/styles.css`, before adding a screen, and before
building anything native that is meant to look like the show.

## Where the look comes from

Three mockups, all 1672×941, in `Designs to Base Everything On/`:

- `Splash Screen.png`
- `Lobby Screen.png`
- `Category Choice Sample Image.png`

All geometry in `styles.css` is scaled from those. Those three images are the
authority; this document is a restatement of them plus the values already in code.
If the two ever disagree, the mockups win.

## The thing being described

A full-bleed Tehran night photograph, staged. Over it: a letterboxed frame of
letterspaced-caps rails — English down the left, Persian down the right — thin-
bordered pill buttons with a trailing chevron, and the tricolour used as stage
lighting rather than ornament: green down the left edge, red down the right.

The stage is never panelised. There is no card with a border sitting in the middle
of the frame. Type sits directly on the photograph and is made legible by the halo
and the scrim, not by being boxed.

## Palette

No gold. The old warm-gold look is dead and must not return in any form — not in a
border, not in a divider, not in a "premium" accent. The flag is the only colour
that carries meaning.

| Token | Value | Use |
|---|---|---|
| `--ink` | `#f4f1ea` | Primary text |
| `--ink-dim` | `#c7c2b8` | Secondary text, chevrons, icons |
| `--ink-faint` | `#928d83` | Rails, corner marks, labels |
| `--hair` | `rgba(255,255,255,0.14)` | Pill borders, default rules |
| `--hair-soft` | `rgba(255,255,255,0.08)` | Ghost buttons, quiet rules |
| `--glass` | `rgba(8,8,9,0.46)` | Pill fill |
| `--glass-hi` | `rgba(24,24,27,0.78)` | Pill hover / selected |
| `--card` | `rgba(14,14,16,0.82)` | Opaque-ish slabs (verdict) |
| `--green` | `#17b25a` | Flag left, correct, live |
| `--red` | `#e02020` | Flag right, wrong |
| `--white` | `#f2efe9` | Focus ring, tagline, flag middle |

Page background is `#050505`. The flag rule is always
`linear-gradient(90deg, var(--green) 0 33.3%, #f4f1ea 33.3% 66.6%, var(--red) 66.6% 100%)`
— equal thirds, flat, no blending between them.

## Type

Three stacks, three jobs. Do not invent a fourth.

```
--sans:    -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif
--display: "Avenir Next Condensed", "AvenirNextCondensed-Medium",
           "Helvetica Neue Condensed", "Roboto Condensed", "Helvetica Neue", Arial, sans-serif
--fa:      "IRANSansWeb", "Vazirmatn", "Geeza Pro", "Tahoma", system-ui, sans-serif
```

- **`--display`** is the stage face. Every number the audience reads from across the
  room — tile values, scores, the clock, the wager — is set in it. Avenir Next
  Condensed ships in macOS core fonts and on iOS, so it costs no download.
- **`--sans`** is everything else in English.
- **`--fa`** is every Persian glyph. `IRANSansWeb` is bundled in three weights
  (400/500/700) at `Web/assets/fonts/`, declared by three `@font-face` blocks, each
  `font-display: swap`. It falls through to Geeza Pro only if the bundled face fails
  to decode — that fallback is a safety net, not a decision. Latin digits inside
  Persian text are a defect; `paintClock` had exactly that bug once.

**Letterspaced caps** are the house voice: `letter-spacing: var(--caps)` (`0.17em`),
`text-transform: uppercase`, small sizes. The eyebrow runs wider at `0.34em`. Caps
carry no case for Persian, so **every RTL rule that touches a caps element must also
clear `letter-spacing` and `text-transform`** — see Persian mode below.

### The halo

Letterspaced caps are nearly all counter and almost no ink, so over the bright city
in the stage photo they dissolve. Every legible text run wears `text-shadow: var(--halo)`
— a tight dark outline in each direction, then a wide soft bloom that darkens the
skyline directly behind the glyphs. It is not decoration; removing it makes the
splash unreadable.

For longer runs, `.tagline::before` adds a soft elliptical black scrim behind the
words: a blurred radial gradient, no edge and no border, so the stage still reads
full-bleed.

## Geometry

The frame is proportional, never fixed.

```
--rail-x: 6.9%      --pad-x: 3.6%      --caps: 0.17em
```

- **Rails** sit at `--rail-x` from their edge, top 15%; the board's rails at 20%.
  Content is `clamp(8.5px, 0.72vw, 12.5px)` caps in `--ink-faint`.
- **Corners** sit at `--pad-x`, top 3.4% / bottom 4.2%, `clamp(8px, 0.66vw, 11.5px)`.
  Each has a 1px fading rule; the right-hand rules fade the other way.
- **Pills** are `min(25.5vw, 426px)` wide, `clamp(44px, 5.6vh, 60px)` tall,
  `border-radius: 999px`, `padding: 0 46px`. Chevron at `right: 21px`, icon at
  `left: 19px`.
- **Logo**: hero `min(56.8vw, 950px)`, lobby `min(54vw, 905px)`,
  board `min(16vw, 290px)`, clue `min(13vw, 210px)`.
- **Below 1200px** the board's mid rails hide — the gutter gets too narrow for their
  wording and single words would spill onto the first tile column.

Every size is a `clamp()` on a viewport unit. If you find yourself typing a bare
pixel size in a new component, you are probably breaking the scale.

## Components

- **Pill** — the only button vocabulary. `--glass` fill, hairline border, blurred
  backdrop, caps label, chevron right. Variants: `.pill-primary` (flag hairline via
  a masked gradient border — the primary entry), `.pill-outline`, `.pill.is-on`
  (chosen, with the green inset ring).
- **The travelling shine** — `.shine::after`, a green→white→red band sweeping a
  masked border on a 2.4s loop. This is *the* mark for "this is the thing you have
  chosen." One class, reused on the menu cursor, a buzzed podium, a picked answer,
  and the board cursor. Do not invent a second selection indicator.
- **Rails and corners** — the letterbox. Quiet caps, fading rules, `--ink-faint`.
  Copy here is voice, not instruction; see the host's register below.
- **Flag rule** — `.flagrule`, the 4px tricolour bar (`3px` on the board). Used
  under the logo and on the results screen.
- **Write-in field** — `.write-field`, the only place the player types. `font-family:
  inherit` is set explicitly because there is no global input reset. In RTL it goes
  `direction: rtl; text-align: right`.
- **Verdict** — `.verdict`, a `--card` slab carrying the ruling. `.verdict.right` /
  `.verdict.wrong` carry the colour; `.verdict.aside` carries neither — it is the
  host cutting in mid-answer, so it reads as a note, not a ruling.

## Voice

The host is **smug, snarky and mean**. That register governs every piece of copy in
the game — splash taglines, lobby furniture, rail bullets, button labels, the
verdict lines, the robot names, the difficulty puns, and all of it again in Persian.
Neutral or helpful-sounding copy is a defect. Nothing here is cheerful; nothing here
is a customer-service string.

Robot names and difficulty tiers are puns in both languages and are written to be
read aloud.

## Persian mode

Persian is not a skin. It is a second edition of the same show, selected on the
splash (*Choose your language*, not "press any key"), and the game carries a `[BETA]`
seal while the voice-over remains English.

- `html[dir="rtl"]` is the switch. Set on the root, not on a wrapper.
- **Every caps element must be de-capped** under RTL: `text-transform: none;
  letter-spacing: 0`. The de-capping group and the `font-family: var(--fa)` swap live
  in the Persian-mode block at the end of `styles.css`.
- Persian glyph runs set `--fa`; Latin numerals and Latin words inside them are
  defects.
- The BETA seal is keyed on `html[dir="rtl"]`, *not* on a `.pill-fa` class —
  `.pill-fa` carries `dir="rtl"` permanently, so keying on it would put the seal on
  the English pill too.
- `.rail-fa` is the Persian rail face wherever both rails appear at once: `--fa`,
  no letterspacing, `#6f6a62`.
- The Persian bank is `window.CLUES_FA` (`Web/data/clues_fa.js`), same shape as
  `window.CLUES`, one thousand clues. `theme` stays English taxonomy in both banks;
  `category` is translated.
- Money is millions of toman. `fmt`/`fmtT` in `app.js` are the only formatters;
  `unit.m` is `'M'` in English and `''` in Persian, `unit.toman` is `' toman'` and
  `' میلیون تومان'`.

## The discarded look — permanently dead

Do not resurrect any of this. It is named here so that a future session recognises
it as wrong rather than finding it in an old file and rebuilding it:

- the `tehranStudio` palette
- the `BroadcastTitle` wordmark
- `ArchivalPanel` cards
- `ArchivalTheme`
- the retired SwiftUI theme
- gold anywhere

`Web/` is the product. `App/` and `iOS/` are shells that load it, and they must
present exactly this. Any file in the tree that presents the show as anything else
comes out.

## Long copy in the rails

Rails were originally single-line (`white-space: nowrap`), which is fine for
one-word categories and fatal for sentence-length voice copy — at 1000px the left
rail ran straight under the JEOPARDY! wordmark. The current rules:

- `.rail-list li` → `white-space: normal`, `max-width: clamp(130px, 14vw, 220px)`,
  `text-wrap: pretty`.
- Board rails only → `max-width: calc(clamp(10px, 14.2vw, 240px) - 6.9vw - 12px)`,
  derived from the same gutter `.board-wrap` reserves, so wrapped text cannot reach
  the first tile column.

If you add rail copy, check it at 900px, 1200px and 1672px before calling it done.
