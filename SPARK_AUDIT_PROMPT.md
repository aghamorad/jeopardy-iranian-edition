# The Spark audit prompt

A hand-over for Gemini Spark (or any chat agent with a long context), for an independent
check of the MAIN bank after the 2026-09-20 re-cut into themed categories.

**How to run it by hand.** Open Spark, attach `QuestionBank/audit_digest.md`, and paste
everything between the two rules below as the message. Nothing else is needed — the digest
carries all 731 categories, so Spark does not need the repo, a shell, or network access.

**Why a digest.** Spark cannot read this folder, and the play files are 4.7 MB. The digest
is generated from `QuestionBank/verified_clues.json` and is 1 MB: every category with its
two titles, the books its five clues come from, and the five clues themselves. Regenerate
it with the script at the bottom of this file after any bank change.

**What is already machine-checked, and need not be re-argued.** `check_bank.py` passes on
both play files and both archives with no errors. `check_repeats.py` finds 0 repeats and 5
near-repeats. `run_tests.sh` is 27 of 27. Every category has exactly five clues, one at
each rung of its round, and at least three distinct books. So Spark's value is not in
re-counting what a script already counts — it is in the two things no tool covers:

1. **Does the theme hold?** Five clues from five books can still be five unrelated facts
   wearing a title. This is the defect the re-cut could have introduced and cannot detect.
2. **Does the title work?** A pun, in each language written separately — not a translation
   of the other, not a scholar's name, not a book's title, not a gloss.

**Known, and being fixed in-house — do not report these.** Ten categories repeat an answer
across two rungs, which the re-cut introduced and no checker catches:
`THRONE INTO BATTLE` (Shah Abbas I, 200/400), `SCHOOL OF HARD MAPS` (Dar al-Fonun, 400/1000),
`VOTE EARLY, GET VETTED OFTEN` (Rastakhiz, 400/800), `A MOVEMENT WITH TOO MANY CAPITALS`
(Tehran, 200/400), `CHECKS AND AYATOLLAHS` (Montazeri, 400/1600), `A POET, A PISTOL, AND A
CONSTITUTION` (Dehkhoda, 400/2000), `THE CLAUSE OF THE TURBAN` (Beheshti, 400/1000),
`A PACT, AND SIXTY-EIGHT LASHES` (Khatami, 200/400), `THE NUCLEAR OPTION, AT RETAIL`
(preferential foreign exchange, 800/1600), `PATIENT ZERO-SUM GAME` (Red Lion and Sun, 200/1000).
Report anything of that *shape* in a category not on this list, and say nothing about these.

---

```
You are auditing a clue bank for the Iranian Edition of Jeopardy, after it was re-cut so
that no category is a shelf for a single book. The bank is attached as audit_digest.md.

You have no shell and no network. Everything you need is in the attachment. Do not ask for
the repository and do not offer to run anything.

WHAT A CATEGORY IS
  - Exactly five clues, one at each rung of its round. Single round: 200 400 600 800 1000.
    Double round: 400 800 1200 1600 2000.
  - Drawn from at least three different books. Never more than two clues from any one book.
  - Its title is a pun on the theme, in English and in Persian, each written separately —
    never a translation of the other, never a subtitle, gloss or bucket label, and never a
    scholar's name or a book's title inside it.
  - The board groups clues by the raw category string, one round at a time. So two spellings
    of one name inside the same round are two half-categories and both get discarded. Two
    spellings in different rounds are two whole categories and are harmless.

ALREADY VERIFIED BY SCRIPT — do not recount, do not restate
  Row counts, rung coverage, book counts, and the name collisions have all been checked and
  pass. If you find yourself reporting "this category has five clues and three books", you
  are doing the machine's job and wasting the audit.

WHAT ONLY YOU CAN JUDGE

  1. THEME INTEGRITY. For every category, read the five clues and decide whether they are
     genuinely one theme an audience would recognise, or five facts that share only a keyword.
     A category titled for a theme whose five clues do not all sit inside that theme is the
     defect. Name it, quote the clue that does not belong, and say what it is instead.

  2. TITLE INTEGRITY. For each category in both languages:
       - Does the Persian title stand on its own as a Persian pun, or is it a translation of
         the English? A translation is a defect even when it is accurate.
       - Does the title contain a scholar's name, an author's name, or a book's title?
       - Is the title a pun, or merely a description of the subject matter?
       - Are the two titles saying the same joke, or did one language get a different and
         better one? Both are acceptable — report only if one language is flat where the
         other is not.

  3. THE CATEGORY THAT PASSES THE COUNT. Find any category that still reads as a shelf for
     one book even though its clues come from three or more volumes — for instance where four
     of the five are really about one man, one city, or one event.

  4. THE JOKE THAT DOES NOT LAND. Flag any title that is a pun only if you already know the
     answer, or that puns in English on a word that does not exist in the Persian.

  5. RUNG DIFFICULTY. Within each category, is the 1000 (or 2000) clue actually harder than
     the 200 (or 400)? List the categories where the ladder is inverted — where the top rung
     is the easiest clue in the column. The digest prints each clue with its value, so this
     is readable.

  6. WHAT I DID NOT ASK ABOUT. Say in one line, at the end, if you notice a defect class I
     have not described here. Do not develop it into a section.

REPORT FORMAT
  - Under 800 words. Findings only, most severe first.
  - One line per finding: the category name, the language if it applies, what is wrong.
    No preamble, no restatement of this brief, no summary of what you read.
  - Where a finding is a judgment call, give the one sentence of reasoning. Where it is a
    fact in the digest, quote it.
  - If a whole category is sound, say nothing about it. Do not list passing categories.
  - End with one line: how many categories you judged defective, and how many you read.
  - If the digest is truncated or you could not read all of it, say so plainly rather than
    auditing the part you got.
```

---

## Regenerating the digest

Run from the project root after any change to the archive. It writes
`QuestionBank/audit_digest.md` from `QuestionBank/verified_clues.json`, with the Persian
title pulled from `QuestionBank/verified_clues_fa.json` by id.

```bash
cd "/Users/Morad/Claude/Jeopardy - Iranian Edition" && python3 - <<'PY'
import json, collections, io
en = json.load(open('QuestionBank/verified_clues.json'))
fa = {r['id']: r for r in json.load(open('QuestionBank/verified_clues_fa.json'))}
cats = collections.defaultdict(list)
for r in en:
    if r.get('round') in ('single', 'double'):
        cats[(r['round'], r['category'])].append(r)
out = io.StringIO(); w = out.write
w("# MAIN clue bank — audit digest\n\n")
w("Every category in the shipped bank, with its two titles, the books its clues come from,\n")
w("and the five clues themselves. English clue text and English answer; the Persian title of\n")
w("each category is beside it. 731 categories, 3655 clues.\n\n")
w("Round rungs: single 200 400 600 800 1000 · double 400 800 1200 1600 2000.\n\n---\n\n")
for (rnd, cat), rows in sorted(cats.items()):
    rows.sort(key=lambda r: r['value'])
    ft = fa.get(rows[0]['id'], {}).get('category', '?')
    books = []
    for r in rows:
        b = (r.get('author', '') or '')[:28]
        t = (r.get('book_title', '') or '')[:44]
        s = '%s, %s' % (b, t) if b else t
        if s not in books: books.append(s)
    w("## [%s] %s\n" % (rnd, cat))
    w("fa: %s\n" % ft)
    w("sources (%d): %s\n" % (len(books), " · ".join(books)))
    for r in rows:
        q = ' '.join((r.get('clue_text') or '').split())
        w("- %s — %s  → %s\n" % (r['value'], q[:260], r.get('canonical_answer', '')))
    w("\n")
open('QuestionBank/audit_digest.md', 'w').write(out.getvalue())
print('categories:', len(cats))
PY
```
