# STYLE SHEET — JEOPARDY! Iranian Edition

The written design contract. `Web/styles.css` is the shipped visual truth.
Report discrepancies and correct this document against the implementation.

Read this before touching `Web/styles.css`, before adding a screen, and before
building anything native that is meant to look like the show.

## Where the look comes from

Three mockups, all 1672×941, in `Designs to Base Everything On/`:

- `Splash Screen.png`
- `Lobby Screen.png`
- `Category Choice Sample Image.png`

Those mockups establish the look. `Web/styles.css` records its shipped geometry
and takes precedence when this document or the mockups disagree.

## The thing being described

A full-bleed Tehran night photograph, staged. Over it: a letterboxed frame of
letterspaced-caps rails — English down the left, Persian down the right — thin-
bordered pill buttons with a trailing chevron, and the tricolour used as stage
lighting rather than ornament: green down the left edge, red down the right.

Splash type sits directly on the photograph, supported by the halo and scrim.
Game controls, verdicts, results and overlays use the black glass panels defined
in `styles.css`.

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
| `--glass` | `rgba(8,8,9,0.46)` | The pill's default tint (`--pill-tint`) |
| `--glass-hi` | `rgba(24,24,27,0.78)` | Pill hover / selected tint |
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
  `border-radius: 999px`, `padding: 0 52px`. Chevron at `right: 15px`, icon at
  `left: 19px`.
- **Logo**: hero `min(56.8vw, 950px)`, lobby `min(54vw, 905px)`,
  board `min(16vw, 290px)`, clue `min(13vw, 210px)`.
- **Below 1200px** the board's mid rails hide — the gutter gets too narrow for their
  wording and single words would spill onto the first tile column.

Every size is a `clamp()` on a viewport unit. If you find yourself typing a bare
pixel size in a new component, you are probably breaking the scale.

### The upright phone

The scale above is written against `vw`, and on a handset held upright `vw` is the
**short** edge — 430px, not 932px. Every clamp in the sheet therefore lands on its
floor at once, and the floors were chosen for a desktop window: a category head
computed to 6.5px, a podium name to 7.5px, the verdict's source line to 8px. The
sheet was legible on a laptop and illegible in a hand.

`@media (max-width: 900px) and (orientation: portrait)` is the rung that answers
this. It restates the same scale one step up — none of the geometry moves, every
value is still a `clamp()` on a viewport unit — and because `orientation` is
derived from the viewport's aspect ratio, a landscape phone (932×430) never
matches it and keeps the landscape-rung rules in the `max-width: 900px` block
above. It lives at the end of `styles.css` so it wins its ties.

Two consequences worth knowing before you add to it:

- `.clue-text` is the one run sized on `vmin`, so it never collapsed; it moves
  here mostly to stay in proportion with the options beside it. `fitClueText()`
  resets to the stylesheet size and steps down to `base * 0.68`, so raising the
  base raises that floor too — check the longest clue in the bank (359 characters)
  still fits.
- `.podium .pname` is `nowrap` with an ellipsis at the base rung, which survives
  the floor size and does not survive this one: "Cyrus the Algorithm" needs 181px
  and the podium offers 110. The portrait rung lets it wrap to a second line
  instead. The podiums row is `flex: none` and cannot grow, so anything that adds
  height there comes off the board.

## Components

- **Pill** — the only button vocabulary. Caps label, chevron right, hairline border,
  and a fill that is a **slab of glass** rather than a flat wash: three background
  gradients in the element's own background, a `box-shadow` bevel and
  `backdrop-filter: blur(17px) saturate(150%)`. Two of the layers are **edge light** —
  the strip of light that skims a top lip, and the far-wall bounce pooled at the foot —
  over a bevel with two lit lips and a real throw.
  - **A pill carries no specular, and this is the rule that matters.** The edition
    circles wear one and it is right there, because a circle stands alone in space. The
    lobby is a column of seven identical pills, and the same highlight in the same place
    seven times stops being a reflection and becomes wallpaper — a white lozenge stamped
    on every button, on top of the leading icon. **A specular is a singleton cue; edge
    light is the only highlight that can repeat.** This was built once with a specular
    copied from the circles and cut after looking at the lobby.
  - The third layer is the **travelling shine**: a band of white canted `102deg`, 46% of
    the width, parked off the leading edge, swept `background-position` from `-140%` to
    `240%` in `0.9s` on `:hover` / `:focus-visible`. A highlight that is only ever
    passing through cannot become a pattern — there is no position in it for the eye to
    lock onto — which is what the specular got wrong. It is driven on a background layer
    rather than a pseudo because both pseudos are spoken for and `::before` is free only
    on non-primary pills. Hover, not an ambient loop: seven pills shining in chorus is
    the wallpaper problem again.
  - Because the shine animates `background-position`, the `transition` names
    `background-color`, `border-color` and `transform` rather than the `background`
    shorthand, which would try to interpolate the same property. `background-size`,
    `-repeat` and `-position` each need one value **per layer** after the shorthand.
  - The shape is forced: both pseudos are spoken for (`.pill-primary::before` is the
    flag hairline, `.shine::after` the travelling shine, and the menu pills are the
    cursor so they carry it), and half the pills are built in `app.js` rather than
    `index.html`, so there is nowhere to hang a `.lens` child. The glass therefore
    lives in the element itself.
  - Consequence: **every state may move `--pill-tint` and `--pill-depth` and nothing
    else.** Hover, `.is-on` and `.pill-primary` all change only those two variables,
    so the sheen and the bevel survive all three. A rule that replaces `background` or
    `box-shadow` outright kills the glass.
  - A `background` shorthand ends in `var(--pill-tint)` — a bare colour is a legal
    final layer. Computed `background-image` is identical across states, so
    `background-color` interpolates and the hover transition still animates.
  - If you ever do reach for a `radial-gradient(ellipse X% Y%)` here, note it takes
    **radii, not diameters**: a `7% 30%` ellipse on an 821×111 slab is a 115×67px
    near-circle, not the sliver you pictured.
  - Variants: `.pill-primary` (flag hairline via a masked gradient border — the primary
    entry), `.pill-outline` (its own tint), `.pill.is-on` (chosen, with the green inset
    ring). Where pills sit inside another piece of glass, as in the language track, the
    inner pills give up their bevel so two slabs do not stack — the track takes the lip
    and the throw instead.
- **Edition circles** — `.circle-row` / `.circle` / `.circle-frame`, the front door's
  "which show?" control. One large disc for MAIN, smaller ones for the courses, each
  wearing art from its own source. A circle is a **globe you look into**, not a picture
  in a frame: `.circle-frame::before` carries the four glass layers above, `.lens` adds
  a masked rim `backdrop-filter` (the dark band where glass is seen edge-on, which is
  what thickness looks like), and `.circle-art` wears `filter: url(#globe-warp)` — an
  SVG displacement that actually bends the picture, the half of the glass shading
  cannot do. `.circle.is-soon` is the unbuilt course: desaturated art, no cursor.
- **The travelling shine** — `.shine::after`, a green→white→red band sweeping a
  masked border on a 2.4s loop. This is *the* mark for "this is the thing you have
  chosen." One class, reused on the menu cursor, a buzzed podium, a picked answer,
  and the board cursor. Do not invent a second selection indicator.
- **Rails and corners** — the letterbox. Quiet caps, fading rules, `--ink-faint`.
  Copy here is voice, not instruction; see the host's register below.
- **Flag rule** — `.flagrule`, the 4px tricolour bar (`3px` on the board). Used
  under the logo and on the results screen.
- **Write-in field** — `.write-input`, the answer field. `font-family:
  inherit` is set explicitly because there is no global input reset. In RTL it goes
  `direction: rtl; text-align: right`.
- **Verdict** — `.verdict`, a `--card` slab carrying the ruling. `.verdict.right` /
  `.verdict.wrong` carry the colour; `.verdict.aside` carries neither — it is the
  host cutting in mid-answer, so it reads as a note, not a ruling.
- **Segmented** — `.segmented`, the green room's settings control (contestants,
  opponents, difficulty, sound, answer mode). A **track** of small buttons under one
  capsule, one of which is `is-on`. The **track** wears the pill's glass — the same
  top lip, foot bounce, four-part bevel and `blur(17px) saturate(150%)` — and the chips
  inside give up their bevel so two slabs never stack. Same shape as the pill's own
  inner-pill rule below: one piece of glass, lit chips resting in it.
  - The track does **not** wear the pill's travelling shine. The shine is the pointer's
    answer to a press; these are settings, not presses, and a sweep on every chip would
    turn the pill's cue into a second button vocabulary.
  - `.overlay-row .segmented button { flex: 1 }` — inside a dialog card the controls run
    edge to edge, so the chips share the track instead of leaving an empty stadium
    beside them. Flat that read as a rule; as glass it read as an unfilled shelf.
  - `.segmented-wrap` is the variant that wraps (`difficulty` has four long labels).
  - The language gate is **not** a segmented control: it is a `nav.menu.menu-inline`
    pair of `.pill.pill-outline` buttons, and the BETA seal keys on `html[dir="rtl"]`.
- **The update surfaces** — one check, three places it can show, all driven from
  `Web/update.js` and its `idle | checking | current | stale | unknown` state. Nothing
  here ever interrupts a game, and a failed check is **silent**: no network, a firewall,
  or GitHub throttled to a crawl all land on `unknown`, which draws nothing at all.
  "We could not check for updates" is our problem, not the player's.
  - **The corner stamp** — `.corner-live`, the lobby's version number turned into a
    button. It keeps the corner's own type and adds only the button reset, because a
    version you can press should not look like a different object from the version you
    cannot. The dot beside it is the show's only news mark: 5px of `--green-lit` in a
    soft ring, and nothing else is ever added to a corner.
  - **The lobby line** — `.update-note`, a green-hairlined capsule wearing the same dot,
    shown only in `stale`. It is `position: fixed` and sits in the **host's floor band**,
    which is the whole reason it is fixed. `--host-band` is cut out of the bottom of
    every screen so the host's floor never collides with content, and on the lobby there
    is no host: the strip is reserved and empty. The column above it is already over-full
    at the stock 1280×720 window, so anywhere in flow is either past the fold or on top
    of the last two pills — where, being a button, it would eat their clicks. `fixed`
    escapes the screen's `overflow: hidden` cleanly, because an `opacity` fade is a
    stacking context and not a containing block for a fixed descendant. It reads as a
    station ident on the floor, not a dialogue box.
  - **The Settings row** — `.update-row`, the real entrance. The corner is a stamp on a
    wide window and the phone hides every corner, so this is the one that has to work
    everywhere. It opens `#update-panel`, a plain `--card` whose copy lives in
    `.update-status`, with one action.
  - **The number is Latin in both languages.** It is a release tag, not a word: the
    notice's sentence takes the Persian face, nothing transliterates `1.0.10`.
  - In RTL the live corner needs an `align-items: center` of its own. The corner family
    is a column, where the RTL block's `flex-end` means "the far side"; the live one is a
    row, where the same keyword addresses the bottom instead and hangs the dot off the
    number's baseline.
  - **The version is declared once**, in `Web/update.js`, and read back out by
    `build_release.sh`, `iOS/project.yml` and `Android/app/build.gradle.kts`. Two numbers
    that can drift apart is how a build tells a player they are out of date when they are
    not. Android's `versionCode` is the same number with the dots dropped, because a
    sideloader compares it to decide what counts as an update.

## Voice

The host is **smug, snarky and mean**. That register governs every piece of copy in
the game — splash taglines, lobby furniture, rail bullets, button labels, the
verdict lines, the robot names, the difficulty puns, and all of it again in Persian.
Neutral or helpful-sounding copy is a defect. Nothing here is cheerful; nothing here
is a customer-service string.

Robot names and difficulty tiers are puns in both languages and are written to be
read aloud.

## Persian mode

Persian is not a skin. It is a language of the same show, selected on the
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
