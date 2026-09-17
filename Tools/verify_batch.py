#!/usr/bin/env python3
"""Check that a clue's citation is real: the answer is where the row says it is.

`Tools/check_bank.py` checks a row's *shape* — four options, index 0, aliases
non-empty, the category complete. It cannot check whether the citation is true,
because it has never seen the books. This does, and it is the only thing standing
between a plausible-sounding row and an invented page number.

It is pure string matching over `pdftotext`. No model, no API, no tokens, nothing
to pay for. A thousand rows is a minute of CPU.

    python3 Tools/verify_batch.py QuestionBank/incoming/batch-2026-09-en.json
    python3 Tools/verify_batch.py QuestionBank/verified_clues.json --archive --lang en
    python3 Tools/verify_batch.py batch-fa.json --lang fa --report /tmp/fa.json

What it establishes, per row, is one thing: **does the answer appear on the page
the row cites, in the book the row cites.** That is the claim a player can check
for themselves, because `Web/app.js` prints `book · author · p. N` under the answer.

It does not require the row's `supporting_passage` to be a verbatim quote. It isn't,
in the shipped bank — measured 2026-09-17, the passages are compressed paraphrase
with only 2–11 words matching the book in order. So the passage is *measured*, not
gated: `quote` in the report is the longest run of consecutive words the passage and
the page share. A high number means the row quotes its source; a low one means it
paraphrases. New rows should quote.

The page offset is a trap this exists for. `page` is the **printed** page and
`pdftotext` counts **sheets**, so a book with front matter carries a constant offset —
+47 on Amanat's *Iran: A Modern History*. The offset is not guessable per book, so it
is **calibrated**: every candidate offset is tried and the one that lands the most of
the book's answers on their own cited pages wins. A book with no constant offset simply
fails to calibrate, which is itself the finding.

Statuses, worst first:

    NOBOOK     no file under Sources/ matches the row's author and title
    NOSCAN     the cited file is an EPUB, or has no text layer for pdftotext
    NOWHERE    the book has a text layer and the answer is not anywhere in it
    ELSEWHERE  the answer is in the book, but not near the page the row cites
    NEAR       the answer is within a few sheets of the cited page
    OK         the answer is on the sheet the cited page resolves to
    NOPAGE     the row carries no page — legal for a final, or an instrument

**Nothing here is a verdict.** This tool is a searchlight, not a judge. It cannot
tell a wrong citation from a book that spells the answer differently, and the
shipped bank has plenty of the second kind. Measured 2026-09-17 on Browne's *The
Persian Revolution of 1905-1909*: the bank writes `Sheikh Fazlollah Nuri` and
`Liakhov`, while the 1910 scan — which OCRs `sheikh` not once in 591 sheets —
gives `Shaykh ... fazlu` and `Liakhoff`, the last 90 times. A name OCR has
broken, a transliteration the author did not use, and an answer the book
discusses but never prints all land in NOWHERE. None of them is an error in the
bank, and acting on them would be the damage this tool was meant to prevent.

So NOWHERE and ELSEWHERE mean *read this row*, never *fix this row*. The reader
is meant to be a model holding the passage, not this tool holding a word list.
The exit status reflects that: 0 whenever the tool ran, 2 only if it could read
nothing at all. Read-only: it never writes a bank, and never writes to `Sources/`.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "Sources")

CAL_RANGE = range(-20, 81)   # candidate (sheet - printed page) offsets
CAL_MIN_HITS = 3             # an offset must land this many answers to be believed
NEAR_SLACK = 3               # sheets either side of the calibrated sheet that still pass
FAR_SLACK = 10               # sheets either side that count as NEAR rather than ELSEWHERE
FUZZ_LEN = 6                 # words this long or longer get fuzzy matching
FUZZ_EDITS = 2               # how many edits apart two spellings may be

# ── Normalisation ────────────────────────────────────────────────────────────
# Scans and PDFs disagree about apostrophes, dashes, ligatures and spacing, and
# `pdftotext` re-wraps every line. Normalise both sides before comparing, or
# every match fails on a curly quote.

_PUNCT = {
    0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'",
    0x201C: '"', 0x201D: '"', 0x201E: '"', 0x2032: "'", 0x2033: '"',
    0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2013: "-", 0x2014: "-",
    0x02BC: "'", 0x00B4: "'", 0x0060: "'", 0x00AB: '"', 0x00BB: '"',
    0x00A0: " ", 0x2009: " ", 0x202F: " ", 0xFEFF: " ",
}


def norm(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_PUNCT)
    text = text.lower()
    text = re.sub(r"[^a-z0-9؀-ۿ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def words(text):
    return norm(text).split()


# ── Book resolution ──────────────────────────────────────────────────────────

def index_sources():
    """Every PDF and EPUB under Sources/, keyed by its normalised filename."""
    found = {}
    for dirpath, dirnames, filenames in os.walk(SOURCES):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith((".pdf", ".epub")):
                found.setdefault(norm(fn), os.path.join(dirpath, fn))
    return found


def surname_of(author):
    """"Abbas Amanat" -> "Amanat"; "Cronin (ed.)" -> "Cronin"; "X & Y" -> "Y"."""
    author = re.sub(r"\([^)]*\)", " ", author or "")
    parts = re.findall(r"[A-Za-z][A-Za-z'\-]*", author)
    while parts and len(parts[-1]) == 1:       # tolerate a trailing initial
        parts.pop()
    return parts[-1] if parts else ""


def resolve_book(row, files):
    """Find the file a row cites: author surname must match, title overlap ranks."""
    surname = norm(surname_of(row.get("author")))
    title_tokens = {t for t in words(row.get("book_title") or "") if len(t) > 3}

    best, best_score, near = None, 0.0, []
    for key, path in files.items():
        if surname and surname not in key:
            continue                      # wrong book, however well the title lands
        score = 2.0
        if title_tokens:
            score += 3.0 * len(title_tokens & set(key.split())) / len(title_tokens)
        if score > best_score:
            best, best_score, near = path, score, [(score, path)]
        elif score == best_score:
            near.append((score, path))
    if best_score < 2.5:                  # surname alone is not enough: Naficy has 4 volumes
        return None, [p for _, p in near]
    return best, []


# ── Per-book text, extracted once ────────────────────────────────────────────

_BOOKS = {}


def within(a, b, limit):
    """Is the edit distance between two words at most `limit`?"""
    if abs(len(a) - len(b)) > limit:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        best = i
        for j, cb in enumerate(b, 1):
            v = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            cur.append(v)
            if v < best:
                best = v
        if best > limit:
            return False
        prev = cur
    return prev[-1] <= limit


class Book:
    """A cited file's text: per-sheet token sets, and a transliteration-tolerant index.

    A book spells a name its own way — Amanat's index says `Teymurtash` nine times and
    `Teymourtash` once — so exact matching reports a real answer as absent. Long words
    are therefore matched within a small edit distance, but only against words that
    start with the same letter and are within two characters of the same length, or
    every short word matches everything.
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.raw = []
        self.sheets = []
        self.vocab = set()
        self._by_first = defaultdict(set)
        self._sheets_cache = {}
        self.error = None
        if path.lower().endswith(".epub"):
            self.error = "EPUB — pdftotext cannot read it"
            return
        try:
            proc = subprocess.run(["pdftotext", "-q", path, "-"],
                                  capture_output=True, text=True, timeout=1800)
        except (OSError, subprocess.SubprocessError) as exc:
            self.error = "pdftotext failed: %s" % exc
            return
        self.raw = proc.stdout.split("\f")
        for page in self.raw:
            ws = set(words(page))
            self.sheets.append(ws)
            self.vocab |= ws
        for w in self.vocab:
            self._by_first[w[0]].add(w)
        if not self.vocab:
            self.error = "no text layer"

    def variants(self, word):
        """The book's spellings of this word: itself, plus near-misses when long."""
        if word in self.vocab or len(word) < FUZZ_LEN:
            return (word,)
        cands = [w for w in self._by_first.get(word[0], ())
                 if w[:1] == word[:1] and within(word, w, FUZZ_EDITS)]
        return tuple(cands) or (word,)

    def sheet_has(self, index, word):
        """Is this word on this sheet, allowing the book its own spelling?"""
        if not (0 <= index < len(self.sheets)):
            return False
        sheet = self.sheets[index]
        if word in sheet:
            return True
        if len(word) >= FUZZ_LEN:
            for cand in sheet:
                if len(cand) >= 3 and cand[0] == word[0] \
                        and within(word, cand, FUZZ_EDITS):
                    return True
        return False

    def sheets_of(self, word):
        """Every sheet index carrying this word. Cached: calibration asks repeatedly."""
        if word not in self._sheets_cache:
            vs = self.variants(word)
            self._sheets_cache[word] = frozenset(
                i for i, s in enumerate(self.sheets) if any(v in s for v in vs))
        return self._sheets_cache[word]

    def sheets_with(self, ws):
        """Every sheet index holding all of these words."""
        if not ws:
            return []
        sets = [self.sheets_of(w) for w in ws]
        if not all(sets):
            return []
        return sorted(sets[0].intersection(*sets[1:]))

    def longest_run(self, quote_words, lo, hi):
        """Longest run of consecutive quote words appearing consecutively on a sheet."""
        best = 0
        for i in range(max(0, lo), min(len(self.raw), hi)):
            page = words(self.raw[i])
            at = defaultdict(list)
            for j, w in enumerate(page):
                at[w].append(j)
            for a, w in enumerate(quote_words):
                for b in at.get(w, ()):
                    k = 0
                    while a + k < len(quote_words) and b + k < len(page) \
                            and quote_words[a + k] == page[b + k]:
                        k += 1
                    if k > best:
                        best = k
        return best


def book_for(path):
    if path not in _BOOKS:
        _BOOKS[path] = Book(path)
    return _BOOKS[path]


def calibrate(book, rows):
    """The offset that lands the most cited answers on their own cited pages."""
    scored = Counter()
    total = 0
    first = CAL_RANGE.start - 1
    last = CAL_RANGE.stop - 1
    for row in rows:
        claimed, ans = cited(row)
        if claimed is None or not ans:
            continue
        total += 1
        for sheet in book.sheets_with(ans):
            gap = sheet + 1 - claimed
            if first <= gap <= last:
                scored[gap] += 1
    if not scored:
        return 0, 0, total
    offset, hits = scored.most_common(1)[0]
    return (offset, hits, total) if hits >= CAL_MIN_HITS else (0, hits, total)


# ── The checks ───────────────────────────────────────────────────────────────

def cited(row):
    """(printed page or None, the answer's significant words)."""
    try:
        claimed = int(str(row.get("page", "")).strip())
    except (TypeError, ValueError):
        claimed = None
    ans = [w for w in words(row.get("canonical_answer") or "") if len(w) > 2]
    return claimed, ans


def verify(rows, lang, files, en_answers):
    # Group by book first: one pdftotext call per book, and calibration needs
    # every row that cites it.
    groups = defaultdict(list)
    results = []
    for row in rows:
        path, near = resolve_book(row, files)
        if path is None:
            rec = {"id": row.get("id", "?"), "status": "NOBOOK", "sheet": None,
                   "offset": None, "quote": None,
                   "reason": "no source file matches %r by %r" % (
                       row.get("book_title"), row.get("author"))}
            if near:
                rec["reason"] += " — closest: %s" % ", ".join(
                    os.path.basename(p) for p in near[:3])
            results.append(rec)
        else:
            groups[path].append(row)
            results.append({"id": row.get("id", "?"), "status": None, "_row": row})

    for path, group in groups.items():
        book = book_for(path)
        if book.error:
            for rec in results:
                if rec["status"] is None and rec["_row"] in group:
                    rec.update(status="NOSCAN", book=book.name,
                               reason="%s: %s" % (book.name, book.error))
            continue
        offset, hits, total = calibrate(book, group)
        for rec in results:
            if rec["status"] is not None or rec["_row"] not in group:
                continue
            row = rec["_row"]
            rid = row.get("id", "?")
            claimed, ans = cited(row)
            if lang == "fa":
                ans = [w for w in words(en_answers.get(rid, "")) if len(w) > 2]
            rec["book"] = book.name
            rec["offset"] = offset
            rec["calibration"] = "%d/%d rows land at %+d" % (hits, total, offset) \
                if hits else "no offset calibrates"

            if claimed is None:
                rec.update(status="NOPAGE",
                           reason="no page to check (legal for final rows and instruments)")
                continue

            # the passage is measured, never gated
            passage = words(row.get("supporting_passage") or "")
            lo, hi = claimed + offset - FAR_SLACK, claimed + offset + FAR_SLACK + 1
            if passage:
                rec["quote"] = book.longest_run(passage, max(0, claimed - 60),
                                                min(len(book.raw), claimed + 60))

            if not ans:
                rec.update(status="NOPAGE", reason="row has no canonical answer to place")
                continue

            target = claimed + offset - 1
            found = book.sheets_with(ans)
            if target in found:
                rec.update(status="OK", sheet=target + 1,
                           reason="printed p.%d is sheet %d (offset %+d); answer is there"
                                  % (claimed, target + 1, offset))
                continue
            if not found:
                rec.update(status="NOWHERE",
                           reason="answer %r appears nowhere in %s"
                                  % (row.get("canonical_answer"), book.name))
                continue
            nearest = min(found, key=lambda i: abs(i - target))
            gap = nearest - target
            rec.update(sheet=nearest + 1, gap=gap)
            if abs(gap) <= NEAR_SLACK:
                rec.update(status="OK",
                           reason="answer on sheet %d, %+d from the cited sheet %d"
                                  % (nearest + 1, gap, target + 1))
            elif abs(gap) <= FAR_SLACK:
                rec.update(status="NEAR",
                           reason="answer on sheet %d, %+d from the cited sheet %d"
                                  % (nearest + 1, gap, target + 1))
            else:
                rec.update(status="ELSEWHERE",
                           reason="cited p.%d is sheet %d, but the answer is on sheet %d"
                                  " (%+d)" % (claimed, target + 1, nearest + 1, gap))
    for rec in results:
        rec.pop("_row", None)
        if rec["status"] is None:
            rec.update(status="NOBOOK", reason="row was not checked")
    return results


# ── Reporting ────────────────────────────────────────────────────────────────

ORDER = ("OK", "NOPAGE", "NEAR", "ELSEWHERE", "NOWHERE", "NOSCAN", "NOBOOK")

# The statuses that mean "a reader should look at this". They are leads, not
# faults: see the module docstring. Nothing here fails a build.
FLAGGED = ("ELSEWHERE", "NOWHERE", "NOBOOK")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bank", help="a batch file, or the archive with --archive")
    ap.add_argument("--archive", action="store_true",
                    help="the file is a bare archive array rather than a batch")
    ap.add_argument("--lang", choices=("en", "fa"), default="en",
                    help="only needed with --archive")
    ap.add_argument("--limit", type=int, help="check only the first N rows")
    ap.add_argument("--only", help="check only rows whose id contains this")
    ap.add_argument("--report", help="write the per-row results here as JSON")
    ap.add_argument("--list", type=int, default=40,
                    help="how many failing rows to print (default 40)")
    args = ap.parse_args()

    try:
        with open(args.bank, encoding="utf-8") as fh:
            rows = json.load(fh)
    except (ValueError, OSError) as exc:
        print("cannot read %s: %s" % (args.bank, exc), file=sys.stderr)
        return 2
    if not isinstance(rows, list):
        print("%s is not a JSON array" % args.bank, file=sys.stderr)
        return 2

    if args.only:
        rows = [r for r in rows if args.only in (r.get("id") or "")]
    if args.limit:
        rows = rows[:args.limit]
    if not rows:
        print("no rows to check", file=sys.stderr)
        return 2

    en_answers = {}
    if args.lang == "fa":
        en_path = os.path.join(ROOT, "QuestionBank", "verified_clues.json")
        if os.path.exists(en_path):
            with open(en_path, encoding="utf-8") as fh:
                en_answers = {r["id"]: r.get("canonical_answer")
                              for r in json.load(fh)}

    files = index_sources()
    print("%d row(s); %d source file(s) under Sources/" % (len(rows), len(files)))
    results = verify(rows, args.lang, files, en_answers)

    counts = Counter(r["status"] for r in results)
    print()
    for status in ORDER:
        if counts[status]:
            print("  %-9s %4d" % (status, counts[status]))

    quotes = [r["quote"] for r in results if r.get("quote") is not None]
    if quotes:
        quotes.sort()
        n = len(quotes)
        print("\n  passage fidelity — longest verbatim run shared with the page:")
        print("    median %d words;  %d%% quote 15+ words;  %d%% quote under 5"
              % (quotes[n // 2],
                 100 * sum(1 for q in quotes if q >= 15) // n,
                 100 * sum(1 for q in quotes if q < 5) // n))

    offsets = Counter(r["offset"] for r in results if r.get("offset") is not None)
    if offsets:
        print("\n  calibrated offsets (sheet - printed), by book:")
        for off, k in sorted(offsets.items()):
            print("    %+4d  %d row(s)" % (off, k))

    flagged = [r for r in results if r["status"] in FLAGGED]
    if flagged:
        print("\n  %d row(s) a reader should look at — leads, not faults:"
              % len(flagged))
        for r in flagged[:args.list]:
            print("    %-9s %-40s %s" % (r["status"], r["id"], r["reason"]))
        if len(flagged) > args.list:
            print("    … and %d more" % (len(flagged) - args.list))

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=2)
        print("\n  wrote %s" % args.report)

    if counts["NOBOOK"] == len(results):
        print("\nFAILED — no row could be checked at all")
        return 2
    if flagged:
        print("\nREAD — %d of %d cited rows did not confirm. These are leads for "
              "a reader, not faults in the bank: an OCR'd name, a transliteration "
              "the book did not use, or an answer the book never printed all land "
              "here. Change nothing on this output alone."
              % (len(flagged), len(results)))
        return 0
    print("\nOK — every cited answer was found where its row says it is")
    return 0


if __name__ == "__main__":
    sys.exit(main())
