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

Every status but NOSCAN is decided by the answer's **words**, never by the row's
passage, so a row whose passage lies verbatim on its own cited page can still read
ELSEWHERE when the answer is a number the writer rounded or a name the scan broke.
The passage is measured separately, and is the better evidence of the two.

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

# The lower bound has to reach past a journal article's front matter. The Hegland
# article's first printed page is 27 on sheet 2, so its offset is -25 — outside a
# -20 floor, which made all 15 rows that cite it read as ELSEWHERE when every one of
# them is on its own page.
CAL_RANGE = range(-40, 81)   # candidate (sheet - printed page) offsets
CAL_MIN_HITS = 3             # an offset must land this many answers to be believed
NEAR_SLACK = 3               # sheets either side of the calibrated sheet that still pass
FAR_SLACK = 10               # sheets either side that count as NEAR rather than ELSEWHERE
FUZZ_LEN = 6                 # words this long or longer get fuzzy matching
FUZZ_EDITS = 2               # how many edits apart two spellings may be
DECISIVE_RUN = 15            # verbatim words on one sheet that settle a page by themselves
PASSAGE_SHARE = 0.6          # share of a passage's words one sheet must hold to place it

# One author, two names. The corpus files her under her scholarly name, Hegland; the
# 1980 article's own first page prints her married name, Hooglund ("Department of
# Anthropology, SUNY at Binghamton"), and a bibliography prints the pair outright —
# "Hooglund [Hegland], Mary (1982)". Without the alias those 15 rows read as citing a
# book that does not exist.
AUTHOR_ALIASES = {"hooglund": "hegland"}

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
    """Every PDF and EPUB under Sources/, keyed by its normalised filename.

    Walked in sorted order because two files can normalise to the same key, and which
    of them wins was otherwise whatever order the directory happened to list.
    """
    found = {}
    for dirpath, dirnames, filenames in os.walk(SOURCES):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if fn.lower().endswith((".pdf", ".epub")):
                found.setdefault(norm(fn), os.path.join(dirpath, fn))
    return found


def surnames_of(author):
    """Every surname the author string carries.

    "Abbas Amanat" -> ["Amanat"]; "Cronin (ed.)" -> ["Cronin"];
    "Homa Katouzian and Hossein Shahidi" -> ["Katouzian", "Shahidi"].

    A multi-author work is usually filed under its first author, so keeping only
    the last one made `Katouzian & Shahidi` and `Afary & Anderson` unresolvable
    and reported 21 correctly-cited rows as citing a book that does not exist.
    """
    author = re.sub(r"\([^)]*\)", " ", author or "")
    out = []
    for part in re.split(r"\band\b|&|,|;|/", author):
        parts = re.findall(r"[A-Za-z][A-Za-z'\-]*", part)
        while parts and len(parts[-1]) == 1:   # tolerate a trailing initial
            parts.pop()
        if parts and parts[-1] not in out:
            out.append(parts[-1])
    for s in list(out):
        alias = AUTHOR_ALIASES.get(norm(s))
        if alias and alias not in out:
            out.append(alias)
    return out


def resolve_book(row, files):
    """Find the file a row cites: surname coverage first, then the title's own words.

    Returns (path, rivals): the file, and any other file that fits the citation just as
    well. Rivals are returned rather than swallowed because the tie is not always
    harmless. An author string naming two people is only satisfied by a file naming both,
    but scoring that all-or-nothing left the two Sreberny books a single shared title word
    apart at an identical score, and which one won came down to the order the directory
    was walked — so the same row was checked against Blogistan on one run of this tool and
    against Cultural Revolution in Iran on the next, silently. The second name settles it;
    where nothing settles it, the row says so.
    """
    surnames = [norm(s) for s in surnames_of(row.get("author"))]
    title_tokens = {t for t in words(row.get("book_title") or "") if len(t) > 3}
    # A row's own source_id names its book as squarely as the title does, and unlike the
    # title it is not abbreviated on the file: sreberny_blogistan_2010 against a filename.
    sid_tokens = {t for t in words((row.get("source_id") or "").replace("_", " "))
                  if len(t) > 3}

    scored = []
    for key, path in files.items():
        key_tokens = set(key.split())
        matched = sum(1 for s in surnames if s in key)
        if surnames and not matched:
            continue                      # wrong book, however well the title lands
        score = 2.0 + 2.0 * matched / len(surnames)
        if title_tokens:
            score += 3.0 * len(title_tokens & key_tokens) / len(title_tokens)
        if sid_tokens:
            score += 1.5 * len(sid_tokens & key_tokens) / len(sid_tokens)
        scored.append((score, path))
    if not scored:
        return None, []
    # Ties broken by the shorter filename and then the path, so that two runs of this
    # tool read the same row against the same book whether or not the citation is enough.
    scored.sort(key=lambda t: (-t[0], len(t[1]), t[1]))
    best_score, best = scored[0]
    if best_score < 2.5:                  # surname alone is not enough: Naficy has 4 volumes
        return None, [p for _, p in scored[:4]]
    return best, [p for s, p in scored[1:] if s == best_score]


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

    # A scan prints its own folio, and OCR mangles it: Paidar's p. 108 comes out
    # "io 8", p. 124 "1 2 4". Letter-for-digit lookalikes are read, nothing else.
    _LOOKALIKE = str.maketrans({"i": "1", "l": "1", "I": "1", "o": "0", "O": "0",
                                "s": "5", "S": "5", "g": "9", "G": "6", "q": "9",
                                "z": "2", "Z": "2", "b": "6", "B": "8", "a": "4"})

    def page_label(self, index):
        """The printed page number this sheet carries, or None if it prints none."""
        if not (0 <= index < len(self.raw)):
            return None
        lines = [l.strip() for l in self.raw[index].splitlines() if l.strip()]
        for line in lines[:2] + lines[-2:]:
            if not 1 <= len(line) <= 6:
                continue
            digits = line.replace(" ", "").translate(self._LOOKALIKE)
            if digits.isdigit() and 1 <= len(digits) <= 4:
                n = int(digits)
                if 1 <= n <= 1500:
                    return n
        return None

    def label_map(self):
        """(step, const, hits): printed = step * sheet + const, read off the folios.

        Ground truth where the answer-based calibration is only a guess: the latter
        searches a fixed window, so a work whose printed numbering starts deep inside a
        larger book — Fathi (ed.) is a partial scan running 106–, an offprint of a
        chapter at pp. 105+ — falls outside it and every one of its rows reads as
        misplaced when each is on its own page.

        The step is fitted, not assumed, because a two-up scan prints two pages to a
        sheet and then no single (sheet - printed) constant describes the book at all:
        Paidar's sheet 61 carries 108 and 109. Forcing step 1 there settles on a
        constant wrong for half the book, and the answers' own mode cannot repair it —
        it fits the rows, so it hides the error it is meant to find.
        """
        pairs = []
        for i in range(len(self.raw)):
            n = self.page_label(i)
            if n is not None:
                pairs.append((i + 1, n))
        best = (1, 0, 0)
        for step in (1, 2, 3):
            votes = Counter(p - step * s for s, p in pairs)
            if not votes:
                continue
            top = votes.most_common(2)
            const, hits = top[0]
            # Both halves of a two-up sheet print, so its folios vote for the sheet's
            # lower page and for its upper one, one apart; the lower is the sheet's floor.
            # A step-1 sheet prints one page only, so there the runner-up is noise — a
            # plate number or a footnote marker the reader mistook for a folio — and
            # absorbing it would move the whole book by a page. Only merge for step > 1.
            if step > 1 and len(top) == 2 and abs(top[1][0] - const) == 1:
                const, hits = min(top[0][0], top[1][0]), hits + top[1][1]
            if hits > best[2]:
                best = (step, const, hits)
        return best

    def sheet_index(self, printed, step, const):
        """The sheet carrying a printed page, under a step-fit calibration."""
        q = printed - const
        return q // step - 1 if q >= 0 else -1

    def best_run(self, quote_words, lo, hi):
        """(longest run of consecutive quote words on one sheet, the sheet it is on).

        Returns the sheet as well as the length, because the two questions a flagged row
        raises are different: whether the passage is on the page the row cites, and — if
        it is not — which page it is on instead. The second one names the correction.
        """
        best, where = 0, None
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
                        best, where = k, i
        return best, where

    def longest_run(self, quote_words, lo, hi):
        """Longest run of consecutive quote words appearing consecutively on a sheet."""
        return self.best_run(quote_words, lo, hi)[0]

    def best_overlap(self, quote_words, lo, hi):
        """(most of the passage's distinct content words on one sheet, that sheet).

        The run measurement only works on a quotation, and most of this bank is not one —
        the passages are compressed paraphrase, 2 to 11 words verbatim. Counting how many
        of the passage's own words a single sheet holds locates a paraphrased passage
        anyway, which is what a row whose run is 3 is asking to be told.
        """
        want = set(w for w in quote_words if len(w) > 3)
        if not want:
            return 0, None
        best, where = 0, None
        for i in range(max(0, lo), min(len(self.raw), hi)):
            n = len(want & set(words(self.raw[i])))
            if n > best:
                best, where = n, i
        return best, where


def book_for(path):
    if path not in _BOOKS:
        _BOOKS[path] = Book(path)
    return _BOOKS[path]


def calibrate(book, rows, answer_words=None):
    """The offset that lands the most cited answers on their own cited pages.

    The book's own folios decide it when they have the evidence — they are ground
    truth, and the answer-based mode can only be as good as the window it searches
    and as trustworthy as the answers' spelling. The folio count is sheets agreeing,
    the answer count is rows landing, so the folios win on ties.

    Returns (step, const, hits, rows, how): printed = step * sheet + const, and how many
    sheets or rows agree. The answer-based path is always a step of 1 — it counts one
    sheet per cited page and could not see a two-up scan even if it landed on it.

    `answer_words` overrides each row's own answer, which the Persian pass needs: the
    scans are Latin-script, so scoring offsets against Persian words scores nothing and
    leaves the book uncalibrated. It is passed in English for both languages.
    """
    scored = Counter()
    total = 0
    first = CAL_RANGE.start - 1
    last = CAL_RANGE.stop - 1
    for row in rows:
        claimed, ans = cited(row)
        if answer_words is not None:
            ans = answer_words.get(row.get("id"), [])
        if claimed is None or not ans:
            continue
        total += 1
        for sheet in book.sheets_with(ans):
            gap = sheet + 1 - claimed
            if first <= gap <= last:
                scored[gap] += 1
    ans_offset, ans_hits = scored.most_common(1)[0] if scored else (0, 0)
    lab_step, lab_offset, lab_hits = book.label_map()
    if lab_hits >= CAL_MIN_HITS and lab_hits >= ans_hits:
        return lab_step, lab_offset, lab_hits, total, "folios"
    if ans_hits >= CAL_MIN_HITS:
        # scored counts (sheet - printed); the caller wants printed = sheet + const,
        # which is the same offset with the sign flipped. Handing it back unconverted
        # mirrors every answers-calibrated book about its own front matter.
        return 1, -ans_offset, ans_hits, total, "answers"
    return 1, 0, ans_hits, total, "none"


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
    en_words = {rid: [w for w in words(a) if len(w) > 2]
                for rid, a in en_answers.items()}
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
            results.append({"id": row.get("id", "?"), "status": None, "_row": row,
                            "rivals": [os.path.basename(p) for p in near]})

    for path, group in groups.items():
        book = book_for(path)
        if book.error:
            for rec in results:
                if rec["status"] is None and rec["_row"] in group:
                    rec.update(status="NOSCAN", book=book.name,
                               reason="%s: %s" % (book.name, book.error))
            continue
        step, offset, hits, total, how = calibrate(
            book, group, en_words if lang == "fa" else None)
        geom = ("offset %+d" % -offset) if step == 1 else ("%d x sheet %+d" % (step, offset))
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
            rec["step"] = step
            if how == "folios" and step > 1:
                rec["calibration"] = ("%d sheets print %d pages each (printed = %d x sheet %+d)"
                                      % (hits, step, step, offset))
            elif how == "folios":
                rec["calibration"] = "%d sheets print at %+d" % (hits, -offset)
            elif how == "answers":
                rec["calibration"] = "%d/%d rows land at %+d" % (hits, total, -offset)
            else:
                rec["calibration"] = "no offset calibrates"

            if claimed is None:
                rec.update(status="NOPAGE",
                           reason="no page to check (legal for final rows and instruments)")
                continue

            # the passage is measured, never gated
            passage = words(row.get("supporting_passage") or "")

            if not ans:
                # A bare number is the usual cause: the answer is present, but there is
                # no word to search a scan for, so the placement is uncheckable here.
                rec.update(status="NOPAGE",
                           reason="answer %r is not searchable text (a bare number is "
                                  "unverifiable by word search)" % row.get("canonical_answer"))
                continue

            target = book.sheet_index(claimed, step, offset)
            in_scan = 0 <= target < len(book.raw)

            # Measured on the cited sheet itself, never on a window around the printed
            # number: the question a run answers is whether the passage is on the page the
            # row cites. A window says only that it is somewhere near, which is not the
            # claim being checked and is not the claim a page correction rests on.
            if passage and in_scan:
                rec["quote"] = book.longest_run(passage, target, target + 1)

            found = book.sheets_with(ans)
            if in_scan and target in found:
                rec.update(status="OK", sheet=target + 1,
                           reason="printed p.%d is sheet %d (%s); answer is there"
                                  % (claimed, target + 1, geom))
                continue

            # The row is going to be reported, so ask the second question: the passage is
            # copied off the source, so if it lies on some other sheet, that sheet is the
            # page the row should have cited, and `passage_page` names it in the book's own
            # numbering. Only asked of rows that failed — a run this long does not happen by
            # chance, which is what makes it a correction rather than a coincidence, but a
            # row that already passed does not need the repair.
            if passage:
                run, at = book.best_run(passage, 0, len(book.raw))
                if at is not None and at != target and run >= DECISIVE_RUN:
                    rec["passage_sheet"] = at + 1
                    rec["passage_page"] = step * (at + 1) + offset
                    rec["passage_run"] = run
                else:
                    share, oat = book.best_overlap(passage, 0, len(book.raw))
                    total = len(set(w for w in passage if len(w) > 3))
                    if oat is not None and oat != target and total \
                            and share >= PASSAGE_SHARE * total:
                        rec["passage_sheet"] = oat + 1
                        rec["passage_page"] = step * (oat + 1) + offset
                        rec["passage_share"] = "%d/%d" % (share, total)

            if not in_scan:
                # A cited page with no sheet to be on: either the page is wrong or the
                # calibration is, and a mirrored fit reports this on every row at once.
                rec.update(status="ELSEWHERE",
                           reason="cited p.%d is sheet %d, but %s holds %d sheets — "
                                  "that page is not in this scan"
                                  % (claimed, target + 1, book.name, len(book.raw)))
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
        if rec.get("rivals"):
            # Said out loud on the row: a second file fits this citation equally well, so
            # every number beside it was measured against a book chosen by a tie-break.
            rec["reason"] = (rec.get("reason") or "") + \
                " — a second file fits this citation equally: %s" % ", ".join(rec["rivals"])
        elif "rivals" in rec:
            rec.pop("rivals")
        # One line here instead of inside each failing branch: a flagged row that knows
        # where its own passage sits is a page correction, and the report should read as
        # one without the reader having to join two fields together.
        if rec.get("passage_page") is not None and rec["status"] in FLAGGED + ("NEAR",):
            rec["reason"] += (" — the passage is quoted on printed p.%d"
                              % rec["passage_page"] if rec.get("passage_run") is not None
                              else " — the passage's own words gather on printed p.%d (%s)"
                                   % (rec["passage_page"], rec.get("passage_share")))
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
        print("\n  passage fidelity — longest verbatim run on the cited sheet:")
        print("    median %d words;  %d%% quote %d+ words;  %d%% quote under 5"
              % (quotes[n // 2],
                 100 * sum(1 for q in quotes if q >= DECISIVE_RUN) // n,
                 DECISIVE_RUN,
                 100 * sum(1 for q in quotes if q < 5) // n))

    # offset is stored as the fit constant (printed = sheet + const); the summary
    # reads in the older sheet - printed convention, which is its negative.
    offsets = Counter(-r["offset"] for r in results
                      if r.get("offset") is not None and r.get("step") == 1)
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
