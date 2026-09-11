# Game rules

Everything here is implemented in `Web/app.js`. Line numbers refer to that file. If the
code and this document disagree, the code is right and this document is a bug.

## The board

Three contestants at most, six categories a round, five clues per category.

| Round | On-screen values | Bank lookup keys |
| --- | --- | --- |
| Single (`Round One`) | 10, 25, 50, 100, 200 | 200, 400, 600, 800, 1000 |
| Double (`Round Two`) | 20, 50, 100, 150, 200 | 400, 800, 1200, 1600, 2000 |
| Final (`The Final Round`) | wager only | — |

Values are in millions of toman; see the comment on `SINGLE_VALUES` (`app.js:13`). The
bank keys are how a clue is looked up in `Web/data/clues.js`, and `clue.value` is
overwritten with the on-screen value when the board is built (`app.js:655`). **Double does
not literally double Single**: rows four and five go 100 to 150 and 200 to 200.

There is exactly one Daily Double per round, never in the top row (`app.js`, `buildBoard`).

## The clue sequence

Read, then buzz, then answer.

| Window | Seconds | Constant |
| --- | --- | --- |
| Read, before buzzers open | 6 | `READ_SECONDS` |
| Buzz | 8 | `BUZZ_SECONDS` |
| Answer, once buzzed | 12 | `ANSWER_SECONDS` |
| Pick a tile (round clock) | 20 | `BOARD_SECONDS` |
| Final, per contestant | 30 | `FINAL_SECONDS` |

A press before the buzzers open costs a 600 ms lockout (`PREMATURE_MS`), but the button
stays live so the press is punished rather than swallowed.

## Scoring

A correct answer adds the clue value. **A wrong answer subtracts it**, in Single and
Double alike. An answer that runs out the clock is scored as a wrong answer. Not buzzing
costs nothing: when the buzz window expires with nobody in, the clue resolves with no
score change and no lockout.

A wrong answer locks that contestant out for the rest of the clue. The remaining
contestants get a Second Chance, which re-arms the buzzers immediately with a fresh
eight-second clock. A clue ends on a correct answer, on a Daily Double, or when everyone
is locked out.

## Daily Double

One contestant, chosen at random, answers alone. The wager is a slider from 0 to
`maxWager(player)` = the larger of the contestant's score and 200 (`MAX_WAGER`), with
quarter, half, three-quarters and all-in buttons. There is no second chance, and **a
missed Daily Double loses the wager.**

## Answering is multiple choice

Not typed. The contestant picks one of the options and `optionIndex === clue.correct`
decides it, with the options reshuffled when the board is built. So there is no
case-folding, no punctuation stripping, no typo distance and no surname matching in the
web build. The `aliases` field exists on every clue record and is not read by `app.js`.

## Final Jeopardy

Every contestant wagers first, one at a time, using the same `maxWager` rule, zero
allowed. Then each answers the same clue alone, thirty seconds each. Scores move by the
wager. The answer, the explanation and the source are revealed only after the last
contestant has answered. **The clue value does not double here**; the wager is the whole
stake. Nothing prevents a contestant on or below zero from wagering and going further
negative.

## Ending

Scores sort descending. A tie for first is announced as "A Tie" and no winner is
highlighted; there is no cap on how many contestants can tie.

## The clue record

`Web/data/clues.js`, embedded as `window.CLUES`:

```
id, round, value, category, theme, difficulty, clue, answer, aliases, options,
correct, explanation, book, author, page, period, passage, correctLine, wrongLine
```

`round` is one of `single`, `double`, `final`. Final records carry `value: 0`. `correct`
is an index into `options`. `correctLine` and `wrongLine` are the host's verdict lines.
