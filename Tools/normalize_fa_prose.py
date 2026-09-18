#!/usr/bin/env python3
"""Normalize Persian prose in the clue bank.

Three passes, all deterministic:

  calendar   Name the calendar on every year. A bare ۱۳۵۰ is ambiguous — it can be
             shamsi (1971) or Gregorian (1350 CE), and both readings occur in this
             corpus. Persian clues get "خورشیدی" or "میلادی" appended after the year.

             The English twin is the gate. The two banks share ids 1:1, so
             "FA ۱۳۵۰ / EN 1971" resolves by arithmetic (+621). The gate reads the
             twin's clue and its explanation — the explanation carries most of the
             dates. Four ways a year is resolved, in order of strength:

               1. arithmetic against the twin (shamsi) or an exact match
                  (Gregorian);
               2. a 19xx/20xx year is Gregorian: no calendar in use here reaches
                  1900, and a bare one is never lunar;
               3. a 12xx–14xx year written after a Persian month name is shamsi:
                  the month settles the calendar on its own, twin or no twin;
               4. a 12xx–14xx year in a row whose twin states only 20th- and
                  21st-century years is shamsi: the row is modern history, so the
                  Persian calendar is the only reading that fits.

             Nothing is guessed beyond those. A year none of the four can
             settle goes to the review tail for a human call. A count that
             merely looks like a year ("۱۷۱۰ صفحه", "۳۱۰۰ نفر", "شمار به ۲۰۰۰
             رسید") and an identifier that looks like one ("تامکت شمارهٔ
            ۳-۶۰۷۹") are recognised and left alone — the report counts them so
             the decision is visible rather than silent.

  script     Persian never uses Arabic yeh ي, alef maqsura ى, or Arabic kaf ك.
             Where they appear the glyph is near-identical but the codepoint is
             wrong, which also breaks answer matching.

  separator  A handful of names and compounds are written with the ZWNJ in two
             different places across the bank. Curated list, not a detector — a
             detector cannot tell "خانه‌ای" (of a house) from "خان‌های" (of the
             khans), and those are two different words, both correct.

Usage:
    python3 Tools/normalize_fa_prose.py            # dry run, writes a review report
    python3 Tools/normalize_fa_prose.py --apply    # writes both banks
    python3 Tools/normalize_fa_prose.py --check    # exit 1 if the bank still has
                                                   # a year that needs a calendar

`--check` is the gate. It is the same four passes, so a batch it passes is a
batch `--apply` would leave alone. Point it at a candidate instead of the bank
when that is what you mean to judge:

    python3 Tools/normalize_fa_prose.py --check \\
        --fa <candidate-fa.json> --en <candidate-en.json>
"""
import json
import re
import sys
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "QuestionBank" / "verified_clues_fa.json"
WEB = ROOT / "Web" / "data" / "clues_fa.js"
EN_WEB = ROOT / "Web" / "data" / "clues.js"
REPORT = ROOT / "QuestionBank" / "normalize_fa_report.md"

FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
MARKERS = ("خورشیدی", "شمسی", "میلادی", "قمری", "ه.ش", "ه.ق", "هجری")

# ---------------------------------------------------------------- text passes

SCRIPT_MAP = {"ى": "ی", "ي": "ی", "ك": "ک"}
SCRIPT_WORDS = {"آيةالله": "آیتالله"}

SEPARATOR_MAP = {
    "رزمآرا": "رزمآرا",
    "ثقةالاسلام": "ثقةالاسلام",
    "وکیلا‌لرعایا": "وکیل‌الرعایا",
    "جا‌به‌جا": "جابه‌جا",
    "نمایش‌نامه‌نویس": "نمایشنامه‌نویس",
    "علی‌قلی‌خان": "علیقلی‌خان",
    "یو‌اس‌اس": "یواس‌اس",
    "نفت‌کش‌ها": "نفتکش‌ها",
    "پنجاه‌و‌دو": "پنجاه‌ودو",
    "مرام‌نامه‌ای": "مرامنامه‌ای",
}


def fix_script(text):
    for bad, good in SCRIPT_WORDS.items():
        text = text.replace(bad, good)
    for bad, good in SCRIPT_MAP.items():
        text = text.replace(bad, good)
    return text


def fix_separator(text):
    for bad, good in SEPARATOR_MAP.items():
        text = text.replace(bad, good)
    return text


def fix_tree(value):
    """Apply the script and separator passes at any depth.

    distractor_rationales is a list of {option, why_wrong, why_plausible}
    mappings, so a list-of-strings comprehension never reaches it.
    """
    if isinstance(value, str):
        return fix_separator(fix_script(value))
    if isinstance(value, list):
        return [fix_tree(v) for v in value]
    if isinstance(value, dict):
        return {k: fix_tree(v) for k, v in value.items()}
    return value


# ------------------------------------------------------------ calendar pass

UNIT = re.compile(r"(?<![۰-۹])([۰-۹]{4})(?:[–—ـ-]([۰-۹]{4}))?(?![۰-۹])")

# "۱۹۳۹ تا ۱۹۴۰" — a span is one fact, and its terminal year carries the marker.
# Both ends move together or neither does: converting the second alone left the
# sentence half Gregorian ("۱۹۳۹ تا ۱۳۱۹ خورشیدی").
SPAN_TA = re.compile(r"^[\s‌]*تا[\s‌]*([۰-۹]{4})(?![۰-۹])")

# A decade is not a year. "دهههای ۱۸۷۰ تا ۱۸۹۰" has no Shamsi reading that keeps
# the sentence's meaning, so a span introduced by دهه stays where it was, and its
# میلادی label keeps it legible. The plural and the ezafe construct count as the
# same word: دهه، دههٔ، دههها، دهههای — all of them head a decade, not a year.
DECADE_LEAD = re.compile(r"دهه[ٔ‌\s]*(?:ها[ی‌]?|ی)?[‌\s]*$")

# The decades are the one place the two calendars do not convert term for term:
# the bank's own marked rows write "دهه ۱۳۵۰ خورشیدی" for the 1970s, so a Shamsi
# decade is the Gregorian decade minus 620, and the two overlap by nine years
# rather than ten. A twin that states a year inside that window names the
# decade's calendar; a 19xx decade is Gregorian and says so itself.
DECADE_SPAN = 620

# A year the bank has already put on the Shamsi side of the ledger.
SHAMSI_LABELLED = re.compile(r"([۰-۹]{4})[\s‌]*(?:خورشیدی|شمسی)(?![ء-ی])")

# The Gregorian counterpart, so the two ledgers can be compared and a year the
# bank uses on both sides is left alone. Filled by run(), read by bank_says().
GREG_LABELLED = re.compile(r"([۰-۹]{4})[\s‌]*(?:میلادی|م\.)(?![ء-ی])")
BANK_SHAMSI = set()
BANK_GREG = set()

# "میان ۱۸۶۰ میلادی و دهه ۱۸۸۰ میلادی" — a decade cannot be rewritten, so the
# year it is compared with cannot move either, or the clause comes out half
# Shamsi and half Gregorian, which is the confusion this pass exists to end.
# A calendar word between the year and the conjunction does not break the pair:
# "۱۸۶۰ میلادی و دهه ۱۸۸۰" is the same comparison said with both labels on.
PAIR_MARKER = r"(?:میلادی|خورشیدی|شمسی|م|ش)?"
DECADE_PAIR_AFTER = re.compile(
    r"^[\s‌]*%s[\s‌]*(?:و|تا)[\s‌]{0,3}دهه[ٔ‌\s]*(?:ها[ی‌]?|ی)?[‌\s]*[۰-۹]{4}"
    % PAIR_MARKER
)
DECADE_PAIR_BEFORE = re.compile(
    r"دهه[ٔ‌\s]*(?:ها[ی‌]?|ی)?[‌\s]*[۰-۹]{4}[\s‌]*%s[\s‌]*(?:و|تا)[\s‌]{0,3}$"
    % PAIR_MARKER
)

# "اوایل ۱۹۷۴" is February, which is Dey or Bahman of ۱۳۵۲ — late, not early. A
# date before Nowruz sits at the tail of the previous Shamsi year, so a relative
# qualifier flips when the offset does.
FLIP_QUALIFIER = {"اوایل": "اواخر", "اواخر": "اوایل"}
QUALIFIER_LEAD = re.compile(r"(اوایل|اواخر)[\s‌]*$")

# "(۱۸۵۷ م)" — a bare calendar abbreviation is already the marker. The
# lookahead keeps this off ordinary words ("۱۳۳۳ مرداد").
ABBREV = re.compile(r"^[\s‌]*(?:[مشق](?![ء-ی])|ه\.[\s‌]?[شق](?![ء-ی]))")

# "(۱۸۹۱-۹۲)" — an abbreviated range tail. The marker belongs after the tail,
# not between the two halves.
SHORT_TAIL = re.compile(r"^[–—ـ-][۰-۹]{1,3}(?![۰-۹])")


def fa_to_int(s):
    return int(s.translate(str.maketrans(FA_DIGITS, "0123456789")))


# A four-digit run outside these bounds is not a year of either calendar — a
# Tomcat tail number ("۳-۶۰۷۹"), a population, a price.
SHAMSI_RANGE = (900, 1500)
GREGORIAN_RANGE = (500, 2100)

# Nouns that turn a four-digit run into a count, and cues that make it an
# identifier. Both are read off the immediate surroundings, not the row.
NON_YEAR_UNITS = (
    "صفحه", "نفر", "جلد", "درصد", "تومان", "ریال", "کیلومتر", "متر", "میلیون",
    "میلیارد", "هزار", "کلمه", "بار", "امتیاز", "دلار", "پوند", "سنت", "گرم",
    "کیلو", "لیتر", "ساله",
)
NON_YEAR_CUES = ("شماره", "ماده", "کد", "بند", "ردیف", "قسمت", "جلسه", "قطعنامه")

# A count is followed by its unit noun. These are matched as whole words, not as
# prefixes: "تنها" begins with "تن" and "مترو" with "متر", so a prefix test would
# silently spare real years that stand next to those words.
COUNT_UNITS = (
    "تن", "شهید", "سرباز", "مأمور", "دستگاه", "کلوب", "امضا", "مایل", "مایلی",
    "پاسخدهنده", "اعتصاب", "روستا", "دفتر", "نسخه", "صندلی", "واگن", "اتاق",
    "تخت", "استاد", "دانشجو", "کارمند", "جام", "سنگ", "برگ", "قلب", "سال",
    "نفر", "جلد", "صفحه", "کلمه", "امتیاز", "بار", "میلیون", "میلیارد",
)
COUNT_WORD = re.compile(r"[\s‌]*([ء-ی‌]+)")

# Persian month names head no other calendar — the lunar months are Arabic
# (محرم، رمضان) and Gregorian dates in Persian prose use transliterations
# (ژانویه). So a 12xx–14xx year written after one — "۲۵ مرداد ۱۳۳۲",
# "اردیبهشت ۱۳۵۹" — is settled by the text itself, with no need of the twin.
# The left boundary keeps the two-letter month off words that merely end in it
# ("مردی", "مهرآباد" fails on the trailing-space test instead).
PERSIAN_MONTHS = (
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان",
    "آذر", "دی", "بهمن", "اسفند",
)
MONTH_LEAD = re.compile(r"(?<![ء-ی])(?:%s)[\s‌]*$" % "|".join(PERSIAN_MONTHS))

# These lunar months are Arabic and name no solar month, so a 12xx–14xx year after
# one is Hijri and keeps its digits under قمری: "۳۰ تیر ۱۲۹۳ (رمضان ۱۳۳۲ قمری)"
# is July 1914 and Shawwal ۱۳۱۳ falls in March 1896, not in the 14th century.
# The English twin cannot settle these — it prints "Ramadan 1332" as it stands —
# so the month name is the whole of the evidence.
#
# محرم is deliberately absent. In Persian usage it names the Muharram that fell in
# a given solar year, and this bank writes it that way: "دهم محرم ۱۳۴۲" is 1963
# and "محرم ۱۲۸۴" is 1905, both confirmed against their English twins, and both
# currently read خورشیدی. A محرم date that really is Hijri always arrives beside
# its solar twin ("در ۱۰ دی ۱۲۹۰ مصادف با دهم محرم ۱۳۳۰ قمری") and carries its own
# label already.
LUNAR_MONTHS = (
    "صفر", "ربیع", "ربيع", "جمادی", "جمادي", "رجب", "شعبان", "رمضان", "شوال",
    "ذیقعده", "ذیالقعده", "ذیحجه", "ذیالحجه", "ذی‌قعده", "ذی‌حجه",
)
LUNAR_LEAD = re.compile(
    r"(?<![ء-ی])(?:%s)(?:[\s‌]*(?:ال)?[\s‌]*[ء-ی]+)?[\s‌]*$" % "|".join(LUNAR_MONTHS)
)

# The cue must sit immediately before the number ("ماده ۱۱۳۳ قانون مدنی"), not
# merely appear in the same clause — "همین بند در ۱۳۲۰ بهانهٔ اشغال شد" is a year.
# The gap allows a serial prefix, as in "تامکت شمارهٔ ۳-۶۰۷۹".
LABEL_LEAD = re.compile(r"(?:%s)[\s‌:ٔـ\-۰-۹]*$" % "|".join(NON_YEAR_CUES))

# "شمار در نهایت به ۲۰۰۰ رسید" — a quantity the sentence arrives at, not a year.
# A year here is introduced by سال, یا در, یا تا, or a named event ("قرارداد ۱۹۰۷"),
# so a bare به in front of the number plus a verb of reaching is a count.
REACH_VERB = re.compile(r"^[\s‌]*(?:رسید|رسیدند|رسان|رساند|رسیده|بالغ|افزایش|کاهش)")
COUNT_LEAD = re.compile(r"(?:^|[\s‌،؛:.])(?:به|از|تا)[\s‌]+$")


def count_unit_after(text, end):
    m = COUNT_WORD.match(text[end:])
    if not m:
        return False
    word = m.group(1)
    return any(
        word == u
        or (len(u) >= 3 and re.fullmatch(re.escape(u) + r"(ان|ها|های|هایی)?", word))
        for u in COUNT_UNITS
    )


def not_a_year(text, start, end):
    # Only whitespace may sit between a count and its unit. A full stop does not:
    # "۱۹۲۹. هزار ماده" is a year, a new sentence, then an unrelated count, and
    # stripping the stop made the two read as one phrase. Nor does a comma — see
    # the unit test below, where crossing one silenced a real year.
    if MONTH_LEAD.search(text[max(0, start - 16) : start]):
        # A Persian month heads a date, never a count. The count word is in the
        # next clause: "در خرداد ۱۳۸۸، میلیونها ایرانی به خیابان آمدند" is June
        # 2009, not one thousand three hundred and eighty-eight million people.
        return None
    if count_unit_after(text, end):
        return "count"
    # The unit must follow the number across whitespace alone. It may not cross a
    # clause break: in "در سال ۱۹۵۵، صفحهٔ «آلبوم هنرمندان»" the page belongs to the
    # next clause and the year stands alone, and in "کودتای ۱۹۵۳، هزاران نفر" the
    # thousands are the next clause's count. Reading across the comma made the unit
    # of an unrelated phrase silence the year.
    tail = text[end : end + 14]
    if tail[:1] in ("", " ", "‌"):
        tail = tail.lstrip(" ‌")
        if any(tail.startswith(u) for u in NON_YEAR_UNITS):
            return "count"
    if LABEL_LEAD.search(text[max(0, start - 16) : start]):
        return "label"
    if COUNT_LEAD.search(text[max(0, start - 8) : start]) and REACH_VERB.match(
        text[end:]
    ):
        return "count"
    return None


def classify(token, en_years, modern, month_before=False):
    """Return 'shamsi', 'gregorian', or None when nothing can settle it."""
    if 1200 <= token <= 1499 and month_before:
        # A Persian month name settles the calendar on its own, and it outranks
        # the twin. The English edition sometimes prints a Shamsi date in Latin
        # digits — "on 2 Khordad 1376" — which puts 1376 into en_years and would
        # otherwise read as the same year in the western calendar.
        return "shamsi"
    if SHAMSI_RANGE[0] <= token <= SHAMSI_RANGE[1]:
        if token + 621 in en_years or token + 622 in en_years:
            return "shamsi"
    if GREGORIAN_RANGE[0] <= token <= GREGORIAN_RANGE[1] and token in en_years:
        return "gregorian"
    if 1900 <= token <= 2099:
        # Shamsi has not reached 1900 and a lunar year of that size would be the
        # 25th century, so a bare 19xx or 20xx can only be Gregorian.
        return "gregorian"
    if SHAMSI_RANGE[1] < token <= GREGORIAN_RANGE[1]:
        # Above the top of the Persian band a bare number has no Persian reading
        # — Shamsi stands in the 1400s — so the western calendar is the only one
        # left, whether or not the twin happens to print the year. The English
        # edition leaves it out here: "ترجمهٔ فیتزجرالد از رباعیات در سال ۱۸۵۹"
        # names 1859 CE, and the twins of both Russo-Persian war rows carry the
        # other row's year, so neither can settle it. The digits can.
        return "gregorian"
    if 1200 <= token <= 1499 and modern:
        # The twin states only 20th- and 21st-century years, so this row is
        # modern history and a bare 13xx is the Persian calendar.
        return "shamsi"
    return None


# ------------------------------------------------------------------ the policy
# 2026-09-18: the English edition prints Gregorian years and the Persian edition
# prints Shamsi ones, so a modern Gregorian year in the Persian bank is rewritten
# into its Shamsi equivalent rather than merely labelled. Anything older keeps
# its Gregorian digits and gains a میلادی label, because no Persian text prints
# 1010 CE as ۳۸۹.
MODERN_CE = 1800

# Shamsi year N begins on 21 March of CE year N + 621, so a whole CE year is
# mostly covered by CE - 621. January, February and March up to the 20th belong
# to CE - 622 instead, and the English twin says which: a date stated there
# settles the offset. Without one the year is taken at CE - 621.
SHAMSI_OFFSET = 621
EARLY_OFFSET = 622
MARCH_TURN = 21

# The day is optional and may stand on either side of the month, because both
# "February 26, 1921" and "3 March 1963" are dates.
EN_DATE = re.compile(
    r"\b(?:(?P<day1>\d{1,2})\s+)?"
    r"(?P<month>%s)\.?\s+(?:(?P<day2>\d{1,2}),?\s+)?(?P<year>\d{4})(?!\d)"
    % "|".join(
        m.capitalize()
        for m in (
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december",
        )
    ),
    re.I,
)

GREG_MONTHS = (
    "ژانویه", "فوریه", "سپتامبر", "نوامبر", "دسامبر", "اکتبر", "ژوئیه",
    "ژوئن", "آوریل", "مارس", "اوت", "مه",
)
GREG_MONTH_LEAD = re.compile(r"(?<![ء-ی])(?:%s)[\s‌ٔ]*$" % "|".join(GREG_MONTHS))
# A month heading a year settles that year's calendar with no label at all: no
# Persian month ever heads a western year, and no western month ever heads a
# Shamsi one. Read across a whole row rather than beside one year, because the
# month is what a row carries when the label would be redundant — "مارس ۱۹۰۸"
# in the clue, a bare "۱۹۰۸" in the explanation.
FA_MONTH_YEAR = re.compile(
    r"(?<![ء-ی])(?:%s)[\s‌]+([۰-۹]{4})(?![۰-۹])" % "|".join(PERSIAN_MONTHS)
)
GREG_MONTH_YEAR = re.compile(
    r"(?<![ء-ی])(?:%s)[\s‌ٔ]+([۰-۹]{4})(?![۰-۹])" % "|".join(GREG_MONTHS)
)
BCE_AFTER = re.compile(
    r"^[\s‌]*(?:پیش از میلاد|ق\.?[\s‌]?م\.?|پ\.?[\s‌]?م\.?)(?![ء-ی])"
)
STRAY_BCE = re.compile(
    r"^[\s‌]*(?:میلادی|شمسی|خورشیدی)[\s‌]*"
    r"(?=(?:پیش از میلاد|ق\.?[\s‌]?م\.?|پ\.?[\s‌]?م\.?)(?![ء-ی]))"
)
DUAL_AFTER = re.compile(r"^[\s‌]*\([\s‌]*[۰-۹]{3,4}(?![۰-۹])")
# "۱۹۷۰ میلادی (بهمن ۱۳۴۸ خورشیدی)" — the row already states the year in Shamsi,
# so the Gregorian half goes rather than being converted beside it. Converting it
# produced "۱۳۴۸ خورشیدی (بهمن ۱۳۴۸ خورشیدی)".
DUAL_GLOSS_AFTER = re.compile(
    r"^[\s‌]*میلادی[\s‌]*\([\s‌]*([^()]{0,32}?)([۰-۹]{4})[\s‌]*"
    r"(?:خورشیدی|شمسی)[\s‌]*\)"
)
DUAL_SLASH = re.compile(r"[\s‌]*/[\s‌]*$")
PAGE_AFTER = re.compile(r"^[\s‌]*:[\s‌]*[۰-۹]")


def fa_from_int(n):
    return str(n).translate(str.maketrans("0123456789", FA_DIGITS))


def en_dated(text):
    """Every month/day/year the English twin states."""
    return [
        (
            m.group("month").lower(),
            int(m.group("day1") or m.group("day2") or 0) or None,
            int(m.group("year")),
        )
        for m in EN_DATE.finditer(text or "")
    ]


FA_SHAMSI_GLOSS = re.compile(r"([۰-۹]{4})[\s‌]*(?:خورشیدی|شمسی)")


def dual_offset(pairs, year):
    """The offset the row states about itself. Only ever a tiebreaker: a dated
    English twin wins.

    Takes (text, twin_years) pairs, because an encore reads its parent's prose
    too and each text can only be judged against the years its own twin states.

    Two readings, strongest first. A gloss standing beside the year —
    "۱۲۳۵ خورشیدی (۱۸۵۷ م)", or "(اسفند ۱۳۷۸ خورشیدی)" after "مارس ۲۰۰۰ میلادی".
    Failing that, a Shamsi year the row states elsewhere is its calendar anchor,
    and can be this year's twin only if the difference is the offset. An anchor
    already spoken for by another year the twin states belongs to that year
    instead: a row holding "۱۳۸۶ خورشیدی" for a 2007 painting says nothing about
    a sale it dates to 2008 — and a parent's "شهریور ۱۳۲۰" for the 1941 invasion
    says nothing about the 1942 death its encore asks after.
    """
    ce = fa_from_int(year)
    for text, _years in pairs:
        for m in re.finditer(re.escape(ce), text or ""):
            window = text[max(0, m.start() - 30) : m.end() + 30]
            for g in FA_SHAMSI_GLOSS.finditer(window):
                stated = fa_to_int(g.group(1))
                if year - stated in (SHAMSI_OFFSET, EARLY_OFFSET):
                    return year - stated
    for text, twin_years in pairs:
        stated = {
            fa_to_int(g.group(1)) for g in FA_SHAMSI_GLOSS.finditer(text or "")
        }
        free = {
            a
            for a in stated
            if 1200 <= a <= 1499
            and year - a in (SHAMSI_OFFSET, EARLY_OFFSET)
            and not any(
                y != year and y - a in (SHAMSI_OFFSET, EARLY_OFFSET)
                for y in twin_years
            )
        }
        if len(free) == 1:
            return year - free.pop()
    return None


def shamsi_offset(year, dates):
    """CE - 621, or CE - 622 when the twin puts the year before Nowruz.

    None when the twin cannot say, which is any of three things: it never dates
    the year, it names March but no day — the 1st-20th fall in the old Shamsi
    year and the 21st-31st in the new one — or it names months on both sides of
    Nowruz, which means the row is telling two stories. The caller settles those
    from the row itself, or falls back to CE - 621.
    """
    early = late = False
    for month, day, y in dates or ():
        if y != year:
            continue
        if month in ("january", "february"):
            early = True
        elif month == "march":
            if day is not None:
                (early, late) = (True, late) if day < MARCH_TURN else (early, True)
        else:
            late = True
    if early == late:
        return None
    # A day settled it, even if the twin also names March bare elsewhere.
    return EARLY_OFFSET if early else SHAMSI_OFFSET


def marker_after(text, end):
    """The calendar name after a year, and the offset just past it."""
    raw = text[end : end + 16]
    stripped = raw.lstrip(" ‌")
    off = end + len(raw) - len(stripped)
    for word in MARKERS:
        if stripped.startswith(word):
            return word, off + len(word)
    return None, None


def dual_gloss(text, start, end):
    """A year already glossed in the other calendar — ۱۹۰۱ (۱۲۸۰), ۱۲۶۹/۱۸۵۲."""
    return bool(DUAL_AFTER.match(text[end:])) or bool(
        DUAL_SLASH.search(text[max(0, start - 3) : start])
    )


SLASH_PARTNER = re.compile(r"[\s‌]*/[\s‌]*([۰-۹]{4})(?![۰-۹])")


def hijri_pair(text, end, first):
    """A year written across a slash from a western one: ۱۲۶۹/۱۸۵۲-۵۳.

    That pairing is how this bank writes a Hijri date beside its western
    equivalent, and the two are 621 apart only when the Persian half is solar —
    1269 AH is 1852-53 and its Shamsi twin is 1231, so a slash pair that is not
    the arithmetic settles the lunar calendar on its own. A pair that *is* the
    arithmetic (+621/+622) is a Shamsi/Gregorian gloss and is left to the
    ordinary rules.
    """
    m = SLASH_PARTNER.match(text[end:])
    if not m:
        return False
    partner = fa_to_int(m.group(1))
    return partner >= MODERN_CE and partner not in (first + 621, first + 622)


def in_citation(text, start, end):
    """A source's publication year — آبکاشک ۱۹۸۵:۱۴ or (نباتی ۱۹۹۹)."""
    if PAGE_AFTER.match(text[end:]):
        return True
    open_paren = text.rfind("(", 0, start)
    close_paren = text.rfind(")", 0, start)
    if open_paren <= close_paren or text.find(")", start) == -1:
        return False
    if MONTH_LEAD.search(text[max(0, start - 16) : start]):
        # A Persian month heads this year, so the parenthesis holds a date and
        # not a source. It is common in this bank to bracket a phase of an event:
        # "(به‌ویژه در نبرد هویزه در دی ۱۳۵۹)", "(تأسیس دی ۱۳۵۸)", "(آذر تا بهمن
        # ۱۳۵۷)". Every one of those was read as a citation and left with no
        # calendar name at all.
        return False
    # A parenthesis holding nothing but a date is a date, not a source.
    # "(۱۲۲۶–۱۳۱۲)" is سلطان ولد's lifespan and "(۱۷۹۹–۱۸۳۷)" is ضیاءالسلطنه's;
    # both were read as citations and so came out with no calendar name at all.
    # A word inside the parenthesis — "(نباتی ۱۹۹۹)" — is what makes it a source.
    return any(ch.isalpha() for ch in text[open_paren + 1 : start])


def bank_says(year):
    """Which calendar the bank itself gives this exact year, or None.

    The last resort before the review tail, and the only tier that reads the
    bank as its own authority. A year is ambiguous on its face only inside the
    overlap of the two calendars: ۱۲۴۰ is both a Shamsi year (1861 CE) and the
    Gregorian year Ibn Arabi died in. Which one this bank means is a fact about
    this bank — it writes ۱۲۴۰ خورشیدی in six rows and ۱۲۴۰ میلادی in two, so
    those two rows are never touched, while a year only ever labelled one way is
    settled by that.
    """
    if year in BANK_SHAMSI and year not in BANK_GREG:
        return "shamsi"
    if year in BANK_GREG and year not in BANK_SHAMSI:
        return "gregorian"
    return None


def settled(year, row_said):
    """Which calendar this year is in, the row's own word beating the bank's.

    The row is the tighter witness: a year the row itself labels, or heads with
    a month, is settled by that alone. Failing that the bank answers, the same
    way it does everywhere else.
    """
    return (row_said or {}).get(year) or bank_says(year)


def decade_calendar(decade, en_years, theme_years=()):
    """Which calendar a decade names, or None when the row says nothing.

    A decade is not a year: it has no single Shamsi value, so the tool never
    rewrites one, it only names the calendar. The window is the Gregorian decade
    the bank's own usage pairs with this Shamsi one.

    When the twin is silent the theme answers: a theme is one story, and a year
    its other rows already label خورشیدی, falling inside this decade, is that
    story saying which calendar it keeps.
    """
    for y in en_years or ():
        if decade + DECADE_SPAN <= y <= decade + DECADE_SPAN + 9:
            return "shamsi"
    for y in theme_years or ():
        if decade <= y <= decade + 9:
            return "shamsi"
    # Last resort, and the same one a year gets. A year the bank labels only
    # خورشیدی anywhere inside this decade is the bank saying which calendar the
    # decade keeps: the Tochal row reads دهه ۱۳۵۰ and the bank dates ۱۳۵۰ خورشیدی
    # thirty-seven times, so it means the 1970s. The twin cannot help there — at
    # that id it states the year Rayy fell, which is a different clue.
    said = {bank_says(y) for y in range(decade, decade + 10)} - {None}
    if len(said) == 1:
        return said.pop()
    if MODERN_CE <= decade <= 2099:
        return "gregorian"
    return None


def decade_pair(text, start, end):
    """This year and a decade are the two ends of one comparison."""
    return bool(
        DECADE_PAIR_AFTER.match(text[end:])
        or DECADE_PAIR_BEFORE.search(text[max(0, start - 30) : start])
    )


def imperial_year(text, start, end, first):
    """Whether this year is a year of the imperial calendar rather than a date.

    "سال رسمی ۲۵۳۵ شاهنشاهی" and "(جهش از سال ۱۳۵۵ به ۲۵۳۵)" make the same claim:
    the row is counting from Cyrus, so the digits stand and take no name. The
    word alone is not the test — "ارتشبد ارتش شاهنشاهی که در ۱۵ آبان ۱۳۵۷…" is an
    army described as royal standing twenty-odd characters from a real date, and
    reading that date as imperial leaves it with no calendar name at all. So the
    year must be an imperial year itself, in a row that says which calendar it
    means, or the word must sit against the year.
    """
    if "شاهنشاهی" in text[max(0, start - 12) : end + 12]:
        return True
    return 2500 <= first <= 2699 and "شاهنشاهی" in text


def settle_offset(year, dates, gloss):
    """Which side of Nowruz the year falls on, or None when nothing can say.

    A date in the English twin is the strongest evidence, then a gloss the row
    states about itself, then the plain CE - 621 default. The one case left
    undecided is a twin that names March for the year and gives no day: the
    whole of March straddles Nowruz, so either side is a coin flip.
    """
    off = shamsi_offset(year, dates)
    if off is not None:
        return off
    off = dual_offset(gloss, year)
    if off is not None:
        return off
    if any(y == year and m == "march" for m, _d, y in dates or ()):
        return None
    return SHAMSI_OFFSET


def flip_qualifier(prefix, off):
    """The text before a converted year, with a relative qualifier turned round
    when the conversion moved the year back across Nowruz."""
    if off != EARLY_OFFSET:
        return prefix
    m = QUALIFIER_LEAD.search(prefix)
    if not m:
        return prefix
    # QUALIFIER_LEAD swallows the space between the qualifier and the year, and
    # the year is about to be re-emitted after it, so put the separator back.
    return (
        prefix[: m.start()]
        + FLIP_QUALIFIER[m.group(1)]
        + m.group(0)[len(m.group(1)) :]
        + prefix[m.end() :]
    )


def normalize_calendar(
    text,
    en_years,
    modern,
    dates,
    gloss,
    log,
    field,
    row_id,
    theme_years=(),
    row_said=None,
):
    """Print each year in the calendar the language uses: a modern Gregorian
    year is rewritten into its Shamsi equivalent, anything older keeps its
    digits and gains the name of its calendar."""
    if not text:
        return text
    out = []
    pos = 0
    handled = 0
    for m in UNIT.finditer(text):
        start, end = m.span()
        if start < handled:
            # A span or a dual gloss already spoke for this year. Its parts are
            # separate matches, so without this the second half is converted a
            # second time — "۱۹۳۹ تا ۱۳۱۹ خورشیدی۱۳۱۹ خورشیدی".
            continue
        first = fa_to_int(m.group(1))
        second = fa_to_int(m.group(2)) if m.group(2) else None
        tail = SHORT_TAIL.match(text[end:])
        tail_digits = ""
        if tail:
            tail_digits = tail.group().lstrip("–—ـ-")
            if second is None and len(tail_digits) < 4:
                # "۱۸۹۱-۹۲" is one year pair, not a year and a stray count: the
                # tail carries the century the first half does not repeat.
                second = fa_to_int(m.group(1)[: 4 - len(tail_digits)] + tail_digits)
            end += tail.end()
        greg_month = GREG_MONTH_LEAD.search(text[max(0, start - 16) : start]) is not None
        decadal = DECADE_LEAD.search(text[max(0, start - 12) : start]) is not None
        guarded = (
            "imperial"
            if imperial_year(text, start, end, first)
            else "dual"
            if dual_gloss(text, start, end)
            else "citation"
            if in_citation(text, start, end)
            else "decade-pair"
            if not decadal and decade_pair(text, start, end)
            else None
        )
        if greg_month and second is None:
            # A Gregorian month name settles the year beyond doubt: "۷ مارس ۱۹۵۱"
            # is the western calendar and nothing else, and the day cannot be
            # carried over without a Jalali day converter — so the year keeps its
            # digits and takes the name. Settled ahead of the citation guard,
            # because a Gregorian date in parentheses is a date and not a source:
            # "(۷ مارس ۱۹۵۱)" stands beside its own Shamsi twin.
            greg_marker, _ = marker_after(text, end)
            if greg_marker is None:
                out.append(text[pos:end])
                out.append(" میلادی")
                pos = end
                log["applied"].append((row_id, field, text[start:end], "میلادی"))
            continue
        if BCE_AFTER.match(text[end:]):
            # "۱۲۵۰ پیش از میلاد" already names its era.
            continue
        stray = STRAY_BCE.match(text[end:])
        if stray:
            # "۱۲۵۰ میلادی پیش از میلاد" — the era is named twice and the wedged
            # marker is wrong. Drop the marker, keep the year. The pattern eats
            # the separator too, so put a single space back.
            out.append(text[pos:end])
            out.append(" ")
            pos = end + stray.end()
            log["bce"].append((row_id, field, text[start:end]))
            continue
        span = SPAN_TA.match(text[end:])
        if span:
            # Both ends or neither: the terminal year is the one that carries the
            # marker, so a half-converted span is what the old order produced.
            span_second = fa_to_int(span.group(1))
            span_end = end + span.end()
            span_marker, span_after = marker_after(text, span_end)
            handled = span_after if span_marker else span_end
            month_before = (
                MONTH_LEAD.search(text[max(0, start - 16) : start]) is not None
            )
            offs = None
            if (
                not decadal
                and not greg_month
                and not guarded
                and all(MODERN_CE <= p <= 2099 for p in (first, span_second))
            ):
                offs = [settle_offset(p, dates, gloss) for p in (first, span_second)]
                if None in offs:
                    offs = None
            if offs:
                new_span = (
                    fa_from_int(first - offs[0])
                    + text[end : span_end - len(span.group(1))]
                    + fa_from_int(span_second - offs[1])
                    + " خورشیدی"
                )
                out.append(text[pos:start])
                out.append(new_span)
                pos = handled
                log["convert"].append((row_id, field, text[start:span_end], new_span))
                if EARLY_OFFSET in offs:
                    log["boundary"].append(
                        (row_id, field, text[start:span_end], new_span)
                    )
            elif (
                second is None
                and span_marker is None
                and guarded in (None, "citation")
                and not decadal
                and not greg_month
                and not BCE_AFTER.match(text[span_end:])
                and {
                    classify(p, en_years, modern, month_before)
                    for p in (first, span_second)
                }
                == {"shamsi"}
            ):
                # A span already written in Shamsi — "از ۱۳۵۹ تا ۱۳۶۷" — which the
                # policy must not convert, because subtracting 621 from a Persian
                # year is nonsense. It takes the name, not the arithmetic: the
                # twin dates both ends at +621, so both ends are solar.
                out.append(text[pos:start])
                out.append(text[start:span_end] + " خورشیدی")
                pos = span_end
                log["applied"].append((row_id, field, text[start:span_end], "خورشیدی"))
            elif (
                second is None
                and span_marker is None
                and guarded in (None, "citation")
                and not decadal
                and not greg_month
                and not BCE_AFTER.match(text[span_end:])
                and all(p in en_years for p in (first, span_second))
            ):
                # A span the policy will not convert — pre-modern, or straddling
                # the 1800 line — but which the twin dates in both halves. Those
                # years are the western calendar and the row should say so:
                # سلطان ولد (۱۲۲۶–۱۳۱۲) and ضیاءالسلطنه (۱۷۹۹–۱۸۳۷). Left bare
                # they read as Persian years, which is the confusion this whole
                # pass exists to remove.
                out.append(text[pos:start])
                out.append(text[start:span_end] + " میلادی")
                pos = span_end
                log["applied"].append((row_id, field, text[start:span_end], "میلادی"))
            elif (
                second is None
                and span_marker is None
                and guarded in (None, "citation")
                and not decadal
                and not greg_month
                and not BCE_AFTER.match(text[span_end:])
                and {settled(p, row_said) for p in (first, span_second)}
                == {"shamsi"}
            ):
                # Neither the twin nor the arithmetic can speak for this span —
                # the English side of "سال‌های ۱۳۵۰ تا ۱۳۵۲" states no year at all
                # — but the row and the bank can. The row's own explanation dates
                # ۱۳۵۵ خورشیدی and the bank dates ۱۳۵۰ خورشیدی thirty-seven times,
                # so both ends are solar and the span takes the name, not the
                # arithmetic: subtracting 621 from a Persian year is nonsense.
                out.append(text[pos:start])
                out.append(text[start:span_end] + " خورشیدی")
                pos = span_end
                log["applied"].append((row_id, field, text[start:span_end], "خورشیدی"))
            elif (
                second is None
                and span_marker is None
                and guarded in (None, "citation")
                and not decadal
                and not greg_month
                and not BCE_AFTER.match(text[span_end:])
                and {settled(p, row_said) for p in (first, span_second)}
                == {"gregorian"}
            ):
                # The same span, settled the other way: a lifespan the row writes
                # out in western years with no Shamsi reading anywhere in it.
                out.append(text[pos:start])
                out.append(text[start:span_end] + " میلادی")
                pos = span_end
                log["applied"].append((row_id, field, text[start:span_end], "میلادی"))
            else:
                log["guarded"].append((row_id, field, text[start:span_end], "span"))
            continue
        marker, after = marker_after(text, end)
        if (
            marker
            or text[end : end + 1].isalpha()
            or ABBREV.match(text[end : end + 12])
        ):
            if marker == "میلادی" and second is None and 1200 <= first <= 1499:
                # A 12xx–14xx year already wearing میلادی. That name is the right
                # one when the row really means the western calendar — ابن عربی
                # (۱۱۶۵–۱۲۴۰ میلادی) — and the wrong one when a Persian month
                # heads the year or the twin dates it at +621/+622, which is how
                # an earlier pass came to mislabel دی ۱۳۱۴ and ۲ خرداد ۱۳۷۶.
                if MONTH_LEAD.search(text[max(0, start - 16) : start]) or (
                    first + 621 in en_years or first + 622 in en_years
                ):
                    out.append(text[pos:end])
                    out.append(" خورشیدی")
                    pos = after
                    log["reconvert"].append((row_id, field, text[start:end]))
                elif LUNAR_LEAD.search(text[max(0, start - 24) : start]):
                    out.append(text[pos:end])
                    out.append(" قمری")
                    pos = after
                    log["reconvert"].append((row_id, field, text[start:end]))
                continue
            if (
                (marker == "میلادی" or (marker is None and text[end : end + 1] == "م"))
                and second is None
                and MODERN_CE <= first <= 2099
            ):
                if not decadal and (
                    greg_month or (row_said or {}).get(first) == "gregorian"
                ):
                    # The label already agrees with the row. A western month
                    # heads the year, or the row says the calendar in as many
                    # words somewhere else in its own voice — مه ۲۰۰۴ in the
                    # explanation settling a bare ۲۰۰۴ in the clue. Consulting
                    # the row's own word here is not circular for a numeral this
                    # large: a Shamsi year never reaches 1800, so a میلادی on a
                    # modern numeral is never an earlier pass's mislabel, and
                    # there is nothing to convert it away from. Re-deriving on
                    # arithmetic alone would overrule the Gregorian month the
                    # row just printed and date it a year forward.
                    continue
                if greg_month or guarded or decadal:
                    log["guarded"].append((row_id, field, text[start:end], "labelled"))
                    continue
                # An earlier pass labelled a modern year instead of converting
                # it. The policy is to print it in Shamsi.
                off = settle_offset(first, dates, gloss)
                if off is None:
                    log["guarded"].append((row_id, field, text[start:end], "march"))
                    continue
                dual = DUAL_GLOSS_AFTER.match(text[end:])
                if dual:
                    if fa_to_int(dual.group(2)) != first - off:
                        # The row glosses the year in Shamsi and the two readings
                        # disagree. Leave both halves standing for the report.
                        log["guarded"].append(
                            (row_id, field, text[start:end], "dual-mismatch")
                        )
                        continue
                    gloss_text = (dual.group(1) + dual.group(2)).strip() + " خورشیدی"
                    prefix = text[pos:start]
                    if not re.match(r"^[۰-۹]", gloss_text):
                        # "در اوایل سال ۱۹۷۰ (بهمن ۱۳۴۸ خورشیدی)" reads "… در
                        # اوایل بهمن ۱۳۴۸ خورشیدی": a year made redundant by its
                        # own gloss goes, and سال goes with it, because what
                        # follows is a month.
                        prefix = re.sub(r"[\s‌]*سال[\s‌]+$", " ", prefix)
                    out.append(prefix)
                    out.append(gloss_text)
                    pos = handled = end + dual.end()
                    log["dual"].append((row_id, field, text[start:end], gloss_text))
                    continue
                out.append(flip_qualifier(text[pos:start], off))
                out.append(fa_from_int(first - off) + " خورشیدی")
                pos = after if marker else end + 1
                log["reconvert"].append((row_id, field, text[start:end]))
                if off == EARLY_OFFSET:
                    log["boundary"].append((row_id, field, text[start:end], first - off))
            continue
        skip = not_a_year(text, start, end)
        if skip:
            log["notyear"].append((row_id, field, text[start:end], skip))
            continue
        if 1200 <= first <= 1499 and (
            LUNAR_LEAD.search(text[max(0, start - 24) : start])
            or hijri_pair(text, end, first)
        ):
            # A Hijri year, named by its month or by the western year across the
            # slash from it. The digits stand as written and only the calendar is
            # named; it is settled before the citation guard, because a lunar date
            # in parentheses is a date and not a page or a publication.
            out.append(text[pos:end])
            out.append(" قمری")
            pos = end
            log["applied"].append((row_id, field, text[start:end], "قمری"))
            continue
        if guarded:
            log["guarded"].append((row_id, field, text[start:end], guarded))
            continue
        if decadal:
            # A decade keeps its digits and gains the name of its calendar.
            verdict = decade_calendar(first, en_years, theme_years)
            if verdict is None:
                log["tail"].append(
                    {
                        "id": row_id,
                        "field": field,
                        "token": text[start:end],
                        "en_years": sorted(en_years),
                        "context": text[max(0, start - 70) : end + 50].strip(),
                    }
                )
                continue
            word = "خورشیدی" if verdict == "shamsi" else "میلادی"
            out.append(text[pos:end])
            out.append(" " + word)
            pos = end
            log["applied"].append((row_id, field, text[start:end], word))
            continue
        verdicts = set()
        month_before = MONTH_LEAD.search(text[max(0, start - 16) : start]) is not None
        for tok in filter(None, (first, second)):
            v = classify(tok, en_years, modern, month_before)
            if (
                v in (None, "gregorian")
                and 1200 <= tok <= 1499
                and (
                    tok in theme_years
                    or (row_said or {}).get(tok) == "shamsi"
                )
            ):
                # The twin prints a Shamsi year in Latin digits — "turned lunar
                # 1343 into 1304" — so the same number then reads as a western
                # year and beats the row's own naming, and when the twin states
                # no year at all the number has no verdict to start with. Either
                # way a year the row calls خورشیدی, or that a sibling row of the
                # same theme calls خورشیدی, is Shamsi.
                v = "shamsi"
            if v is None:
                verdicts = {None}
                break
            verdicts.add(v)
        if not verdicts or None in verdicts or len(verdicts) > 1:
            parts = [p for p in (first, second) if p is not None]
            used = {bank_says(p) for p in parts}
            if len(used) == 1 and used != {None}:
                verdicts = used
            else:
                log["tail"].append(
                    {
                        "id": row_id,
                        "field": field,
                        "token": text[start:end],
                        "en_years": sorted(en_years),
                        "context": text[max(0, start - 70) : end + 50].strip(),
                    }
                )
                continue
        if "shamsi" in verdicts:
            out.append(text[pos:end])
            out.append(" خورشیدی")
            pos = end
            log["applied"].append((row_id, field, text[start:end], "خورشیدی"))
            continue
        parts = [p for p in (first, second) if p is not None]
        if all(MODERN_CE <= p <= 2099 for p in parts) and not greg_month and not decadal:
            if all((row_said or {}).get(p) == "gregorian" for p in parts):
                # The row settles this year itself, and settles it western:
                # "مارس ۱۹۰۸" in the clue and a bare ۱۹۰۸ in the explanation are
                # one date written twice, and the row has already told the reader
                # which calendar it keeps. Converting on the CE−621 arithmetic
                # alone would date that explanation one year forward, and a
                # Gregorian month cannot be carried back over Nowruz without a
                # Jalali day converter — so the year keeps its digits and takes
                # the name the row gave it.
                out.append(text[pos:end])
                out.append(" میلادی")
                pos = end
                log["applied"].append((row_id, field, text[start:end], "میلادی"))
                continue
            offs = [settle_offset(p, dates, gloss) for p in parts]
            if None in offs:
                log["guarded"].append((row_id, field, text[start:end], "march"))
                continue
            new_span = text[start:end].replace(
                m.group(1), fa_from_int(first - offs[0]), 1
            )
            if m.group(2) is not None:
                new_span = new_span.replace(
                    m.group(2), fa_from_int(second - offs[1]), 1
                )
            elif tail_digits:
                new_span = new_span.replace(
                    tail_digits, fa_from_int(second - offs[1])[-len(tail_digits) :], 1
                )
            out.append(flip_qualifier(text[pos:start], offs[0]))
            out.append(new_span + " خورشیدی")
            pos = end
            log["convert"].append((row_id, field, text[start:end], new_span))
            if EARLY_OFFSET in offs:
                log["boundary"].append((row_id, field, text[start:end], new_span))
            continue
        if greg_month and MODERN_CE <= first <= 2099:
            log["guarded"].append((row_id, field, text[start:end], "greg-month"))
        word = "میلادی"
        out.append(text[pos:end])
        out.append(" " + word)
        pos = end
        log["applied"].append((row_id, field, text[start:end], word))
    out.append(text[pos:])
    return "".join(out)


# ------------------------------------------------------------------ loading


def load_js(path, var):
    raw = path.read_text(encoding="utf-8")
    body = raw[raw.index("[") : raw.rindex("]") + 1]
    pre, post = raw[: raw.index("[")], raw[raw.rindex("]") + 1 :]
    return json.loads(body), pre, post, raw


# ------------------------------------------------------------------- passes

WEB_PROSE = ("clue", "explanation", "correctLine", "wrongLine")
WEB_TEXT = WEB_PROSE + ("answer", "category")
WEB_LISTS = ("aliases", "options")

MASTER_PROSE = ("clue_text", "explanation")
MASTER_TEXT = MASTER_PROSE + ("category", "specificity_prompt")
MASTER_LISTS = (
    "canonical_answer",
    "accepted_aliases",
    "partial_answers",
    "options",
)
# Master-only, never shipped, so no year markers — but the script and separator
# passes must reach it, or Arabic yeh/kaf survive in the source of record.
MASTER_TREES = ("distractor_rationales",)

HOST_PROSE = ("correct_generic", "wrong_generic", "explanation", "specificity_prompt")


def run(apply=False, fa_path=None, en_path=None):
    """`fa_path` / `en_path` override the bank the pass reads. Pointed at a
    candidate batch they answer the only question a landing gate has: would
    these rows, merged, need a calendar written on them? Nothing is written
    either way unless `apply` — the caller decides what a finding means."""
    en_rows, _, _, _ = load_js(en_path or EN_WEB, "CLUES")
    # The twin's explanation carries most of the dates, so the gate reads both
    # fields. FA and EN are the same story under two languages and share ids 1:1.
    en_years = {
        r["id"]: {
            int(y)
            for y in re.findall(
                r"(?<!\d)(\d{4})(?!\d)",
                (r.get("clue") or "") + " " + (r.get("explanation") or ""),
            )
        }
        for r in en_rows
    }
    # A date stated in the twin settles which side of Nowruz the year falls on.
    en_dates = {
        r["id"]: en_dated(
            " ".join(
                str(r.get(f) or "")
                for f in ("clue", "explanation", "passage")
            )
        )
        for r in en_rows
    }

    def en_of(row_id):
        return en_years.get(row_id, set())

    def is_modern(row_id):
        years = en_of(row_id)
        return bool(years) and all(y >= 1900 for y in years)

    log = {
        "tail": [],
        "applied": [],
        "notyear": [],
        "convert": [],
        "reconvert": [],
        "dual": [],
        "boundary": [],
        "bce": [],
        "guarded": [],
        "script": Counter(),
        "separator": Counter(),
    }

    master = json.loads((fa_path or MASTER).read_text(encoding="utf-8"))

    # The row's own prose, so a dual gloss stated somewhere in it can settle a
    # year whose English twin names March without a day. An encore re-asks its
    # parent's clue and so reads its parent's gloss too — but each blob is paired
    # with the twin years of the row it came from, or the parent's anchor would
    # be read as the child's. Host lines are part of the row's own voice, and are
    # where a year is most often spelled out for the player in as many words.
    def row_prose(r):
        hr = r.get("host_reactions") or {}
        return " ".join(
            [str(v) for f in MASTER_TEXT if isinstance(v := r.get(f), str)]
            + [str(v) for f in HOST_PROSE if isinstance(v := hr.get(f), str)]
        )

    # A label standing in front of a unit or of "پیش از میلاد" is not a calendar
    # claim: "۳۱۳۲ میلادی متر" is a wavelength, and "۱۲۵۰ میلادی پیش از میلاد" is a
    # BCE year whose wedged marker this pass deletes on the same run. Reading
    # either as the bank's own usage would let a number that is not a year at all
    # decide how a real one is labelled.
    def claimed(text, m):
        after = text[m.end() :]
        return not (
            BCE_AFTER.match(after)
            or any(after[:14].lstrip(" ‌").startswith(u) for u in NON_YEAR_UNITS)
        )

    def row_settlements(blob):
        """Which calendar this row says each year is in, on its own word.

        Two witnesses and no others: an explicit label, and a month heading the
        year. A Persian month never heads a western year and a western month
        never heads a Shamsi one, so the month alone settles it — which is what a
        row carries when a label would only repeat itself. A year the row labels
        both ways is a row contradicting itself, and it settles nothing.
        """
        said = {}
        for rx, word in ((SHAMSI_LABELLED, "shamsi"), (GREG_LABELLED, "gregorian")):
            for m in rx.finditer(blob):
                if claimed(blob, m):
                    y = fa_to_int(m.group(1))
                    if said.setdefault(y, word) != word:
                        said[y] = None
        for y in [y for y, w in said.items() if w is None]:
            del said[y]
        for rx, word in ((FA_MONTH_YEAR, "shamsi"), (GREG_MONTH_YEAR, "gregorian")):
            for m in rx.finditer(blob):
                said.setdefault(fa_to_int(m.group(1)), word)
        return said

    # Each pass reads its evidence off the bank as the bank now stands and then
    # rewrites the bank, so one pass settles what the next one reads: the host
    # line naming ۱۳۱۸ خورشیدی is a label this same tool wrote a moment ago, and
    # the sibling row that needs it cannot see it until that pass is over. The
    # growth is monotone — a pass only ever adds a name to a year that lacked one
    # — so a few passes reach the fixed point, and a bank already settled reaches
    # it in the first, with nothing left to write.
    # Both banks are the same prose under two sets of field names, so they are
    # walked together and must settle together: a bank walked only after the
    # other had settled would read the settled evidence against its own pristine
    # text and label the odd year the other had ruled on — the same row's clue
    # shamsi in one bank and western in the other. Evidence is still the master's
    # alone; the web bank's own labels never feed it back.
    web_rows, pre, post, _ = load_js(WEB, "CLUES_FA")

    def snapshot():
        return json.dumps([master, web_rows], ensure_ascii=False, sort_keys=True)

    for _pass in range(12):
        before = snapshot()
        for key in ("tail", "guarded", "notyear", "bce"):
            log[key].clear()

        fa_blob = {r["id"]: row_prose(r) for r in master}
        fa_gloss = {}
        for rid, blob in fa_blob.items():
            pairs = [(blob, en_of(rid))]
            parent = rid[: -len("_encore")] if rid.endswith("_encore") else None
            if parent in fa_blob:
                pairs.append((fa_blob[parent], en_of(parent)))
            fa_gloss[rid] = tuple(pairs)

        # The bank's own labelled Shamsi years, gathered by theme. A theme is one
        # story told across its rows, so a decade one row leaves bare can be read
        # from a year another row already dates خورشیدی.
        theme_years = {}
        theme_of = {}
        for r in master:
            theme_of[r["id"]] = r.get("theme")
            for m in SHAMSI_LABELLED.finditer(fa_blob[r["id"]]):
                theme_years.setdefault(r.get("theme"), set()).add(fa_to_int(m.group(1)))

        # What each row claims about its own years, before the bank's usage is
        # consulted: a row is the tighter witness on the years it states.
        row_said = {r["id"]: row_settlements(fa_blob[r["id"]]) for r in master}

        BANK_SHAMSI.clear()
        BANK_GREG.clear()
        for r in master:
            blob = fa_blob[r["id"]]
            for m in SHAMSI_LABELLED.finditer(blob):
                if claimed(blob, m):
                    BANK_SHAMSI.add(fa_to_int(m.group(1)))
            for m in GREG_LABELLED.finditer(blob):
                if claimed(blob, m):
                    BANK_GREG.add(fa_to_int(m.group(1)))

        def walk(row, field, is_prose, rid=None):
            # host_reactions is walked as its own mapping, so it cannot supply the
            # id — the English twin is keyed by the parent row's id.
            if rid is None:
                rid = row.get("id", "?")
            val = row.get(field)
            if isinstance(val, str):
                new = fix_script(val)
                new = fix_separator(new)
                if new != val:
                    log["script"]["master"] += 1
                if is_prose:
                    new = normalize_calendar(
                        new,
                        en_of(rid),
                        is_modern(rid),
                        en_dates.get(rid, ()),
                        fa_gloss.get(rid, ()),
                        log,
                        f"{field}",
                        rid,
                        theme_years.get(theme_of.get(rid), ()),
                        row_said.get(rid),
                    )
                row[field] = new
            elif isinstance(val, list):
                row[field] = [
                    fix_separator(fix_script(s)) if isinstance(s, str) else s
                    for s in val
                ]

        for row in master:
            for f in MASTER_TEXT:
                walk(row, f, f in MASTER_PROSE)
            for f in MASTER_LISTS:
                walk(row, f, False)
            for f in MASTER_TREES:
                if f in row:
                    row[f] = fix_tree(row[f])
            hr = row.get("host_reactions")
            if isinstance(hr, dict):
                for f in HOST_PROSE:
                    walk(hr, f, True, rid=row.get("id", "?"))

        for row in web_rows:
            for f in WEB_TEXT:
                walk(row, f, f in WEB_PROSE)
            for f in WEB_LISTS:
                walk(row, f, False)

        if snapshot() == before:
            break
    else:
        raise RuntimeError("the calendar pass never reached a fixed point")

    return master, web_rows, pre, post, log


def write_report(log):
    # The master and the web bank are the same prose under two field names, so
    # every finding arrives twice. Collapse to the name a player would see.
    FIELD = {
        "clue_text": "clue",
        "clue": "clue",
        "explanation": "explanation",
        "correct_generic": "correctLine",
        "correctLine": "correctLine",
        "wrong_generic": "wrongLine",
        "wrongLine": "wrongLine",
    }

    rows = defaultdict(list)
    for item in log["tail"]:
        rows[item["id"]].append(
            (
                FIELD.get(item["field"], item["field"]),
                item["token"],
                tuple(item["en_years"]),
                item["context"],
            )
        )

    def band(token):
        years = [fa_to_int(y) for y in re.findall(r"[۰-۹]{4}", token)]
        if not years:
            return "no 4-digit number"
        return (
            "in the 1000–1499 band — could be either calendar"
            if all(1000 <= y <= 1499 for y in years)
            else "outside the band — the twin states no year, or this is not a year"
        )

    lines = ["# Farsi prose normalization — what changed, and what is left", ""]
    lines.append(
        "The English edition prints Gregorian years and the Persian edition "
        "prints Shamsi ones, so every Gregorian year from "
        f"**{MODERN_CE}** on is rewritten into its Shamsi equivalent "
        f"(`CE - {SHAMSI_OFFSET}`) and labelled خورشیدی; anything older keeps its "
        "digits and gains a میلادی label."
    )
    lines.append("")
    lines.append(
        f"Years rewritten to Shamsi: **{len(log['convert'])}**. "
        f"Years already labelled میلادی, rewritten: **{len(log['reconvert'])}** "
        f"(**{len(log['boundary'])}** of them by CE − {EARLY_OFFSET}). "
        f"Labels written over years that keep their digits: **{len(log['applied'])}**. "
        f"Stray era markers removed: **{len(log['bce'])}**. "
        f"Years a guard kept out of the rewrite: **{len(log['guarded'])}**. "
        f"Distinct rows still unresolved: **{len(rows)}**."
    )
    lines.append("")
    lines.append(
        "These are what the run that wrote this report changed, so on a bank that "
        "is already normalized every count but the guards and the tail is zero — "
        "a second pass over a settled bank is a no-op by design."
    )
    lines.append("")
    pairs = Counter((o, n) for _r, _f, o, n in log["convert"])
    if pairs:
        lines.append("## Rewritten, Gregorian year → Shamsi year")
        lines.append("")
        shown = " · ".join(f"`{o}`→`{n}`" for (o, n), _c in pairs.most_common(40))
        lines.append(shown)
        lines.append("")
        lines.append(
            "× counts, commonest first: "
            + ", ".join(f"`{o}`→`{n}` ({c})" for (o, n), c in pairs.most_common(12))
        )
        lines.append("")
    if log["reconvert"]:
        lines.append("## Already labelled میلادی, now Shamsi")
        lines.append("")
        lines.append(
            ", ".join(
                f"`{o}` ({r})" for r, _f, o in sorted(set(log["reconvert"]))[:40]
            )
        )
        lines.append("")
    if log["boundary"]:
        lines.append("## Rewritten from the year before Nowruz — CE − 622")
        lines.append("")
        lines.append(
            "These fall before Nowruz — either the English twin dates them to "
            "January, February or the first twenty days of March, or the row "
            "glosses the year itself against a Shamsi one — and so land in the "
            "previous Shamsi year:"
        )
        lines.append("")
        lines.append(
            ", ".join(f"`{o}` ({r})" for r, _f, o, _n in sorted(set(log["boundary"])))
        )
        lines.append("")
    if log["bce"]:
        lines.append("## Stray markers removed in front of پیش از میلاد")
        lines.append("")
        lines.append(", ".join(f"`{o}` ({r})" for r, _f, o in log["bce"]))
        lines.append("")
    if log["guarded"]:
        kinds = Counter(k for _r, _f, _t, k in log["guarded"])
        lines.append("## Left alone by a guard")
        lines.append("")
        lines.append(
            ", ".join(f"{k} ({c})" for k, c in kinds.most_common())
            + " — a citation year, a year already glossed in the other calendar, "
            "a year pinned by a Gregorian month name, or an Imperial-calendar year."
        )
        lines.append("")
        if kinds.get("march"):
            lines.append(
                "`march` means the twin names March for that year and gives no "
                "day, so the year sits astride Nowruz and cannot be converted "
                "without inventing a date. Each stays as it stands, its year "
                "still labelled میلادی:"
            )
            lines.append("")
            lines.append(
                ", ".join(
                    f"`{t}` / {r}"
                    for r, _f, t, k in sorted(set(log["guarded"]))
                    if k == "march"
                )
            )
            lines.append("")
    lines.append(
        "A year is settled only when the English twin confirms it by arithmetic "
        "(shamsi +621 or +622), states it identically (Gregorian), or the row "
        "settles it on its own — a Persian month name before a 12xx–14xx year "
        "makes it shamsi, a bare 19xx/20xx can only be Gregorian, and a bare 13xx "
        "in a row whose twin states only 20th- and 21st-century years can only be "
        f"shamsi. Which side of Nowruz a converted year falls on comes from the "
        f"same evidence: a date in the twin settles it (CE − {EARLY_OFFSET} before "
        f"the 21st of March, CE − {SHAMSI_OFFSET} otherwise), and a dual gloss "
        "inside the row is the tiebreaker. Every year left unresolved lands here, "
        "and each one needs a call: shamsi or Gregorian (میلادی)."
    )
    lines.append("")
    lines.append(
        "When none of that reaches a year, the bank is asked what it means by it: "
        "a bare year is shamsi if that exact year wears خورشیدی somewhere in the "
        "bank and never wears میلادی. The label is what carries the evidence, so a "
        "year the bank itself calls Gregorian stays Gregorian even in a Persian "
        "sentence. A decade takes the same route when its twin cannot help — "
        "`single_tehran_bazaar_to_megapolis_1000` reads «تله‌کابین تاریخی "
        "احداث‌شده در دهه ۱۳۵۰» and its twin at that id is the Rayy clue, but the "
        "bank dates ۱۳۵۰ خورشیدی thirty-seven times, so the decade is 1970s and is "
        "labelled `دهه ۱۳۵۰ خورشیدی`. Decades are labelled, never converted: the "
        "Shamsi decade is the Gregorian one less 620, so a Gregorian row keeps "
        "`دهه ۱۸۷۰ میلادی`."
    )
    lines.append("")
    # One row is walked twice (master and web) and a token can repeat inside a
    # field, so the same decision arrives several times. Count distinct pairs.
    by_kind = {"count": set(), "label": set()}
    for rid, _field, tok, kind in log["notyear"]:
        by_kind[kind].add((rid, tok))
    lines.append(
        "Four-digit runs recognised as **not years** and left alone — "
        "**{} counts** and **{} labels** (serial numbers, clause numbers), "
        "counted once per row:".format(
            len(by_kind["count"]), len(by_kind["label"])
        )
    )
    lines.append("")
    for kind, label in (("count", "counts"), ("label", "labels")):
        if not by_kind[kind]:
            continue
        sample = sorted(by_kind[kind])[:15]
        shown = ", ".join(f"`{t}` ({r})" for r, t in sample)
        more = (
            f" and {len(by_kind[kind]) - len(sample)} more"
            if len(by_kind[kind]) > len(sample)
            else ""
        )
        lines.append(f"- {label}: {shown}{more}")
    lines.append("")
    lines.append(
        "The recurring hard case is a row that mixes registers: a shamsi year "
        "and a Gregorian year for the same story, neither marked. The twin only "
        "settles years it happens to state, and it often states a neighbouring "
        "event's year instead."
    )
    lines.append("")
    for rid in sorted(rows):
        items = sorted(set(rows[rid]))
        lines.append(f"## `{rid}`")
        for field, token, en_years, ctx in items:
            lines.append(f"- **{field}** · `{token}` — {band(token)}")
            lines.append(f"  - twin's years: {en_years or '—'}")
            lines.append(f"  - …{ctx}…")
        lines.append("")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def opted(argv, flag):
    """The value after `flag`, or None. Kept dumb on purpose: this script takes
    four options and a parser would be more code than the options."""
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            return Path(argv[i + 1])
    return None


def main():
    argv = sys.argv[1:]
    check = "--check" in argv
    apply = "--apply" in argv and not check
    master, web_rows, pre, post, log = run(
        apply, opted(argv, "--fa") or opted(argv, "--master"), opted(argv, "--en")
    )

    # The four passes that change a row. `guarded` and `tail` are decisions left
    # to a reader — a year a guard held out of the rewrite, and a year with no
    # twin to settle it — and a gate that fires on those fires on honest work.
    changes = sum(
        len(log[k]) for k in ("applied", "convert", "reconvert", "bce")
    )
    if check:
        where = opted(argv, "--fa") or opted(argv, "--master") or MASTER
        for k in ("applied", "convert", "reconvert", "bce"):
            # `bce` and `reconvert` record three fields, `applied` and `convert`
            # four. Print what is there rather than assume the arity. The first
            # field is always the id, which is how a caller tells a finding on a
            # landed row from one on the batch it is judging.
            for item in log[k]:
                print("  X %s" % " · ".join(str(p) for p in item))
        print(
            f"{where}: {changes} year(s) would be relabelled"
            f" · {len(log['guarded'])} held by a guard"
            f" · {len(log['tail'])} with nothing to settle them"
        )
        sys.exit(1 if changes else 0)

    print(f"calendar markers applied : {len(log['applied'])}")
    print(f"rewritten to shamsi      : {len(log['convert'])}")
    print(f"relabelled from میلادی   : {len(log['reconvert'])}")
    print(f"  of which CE - {EARLY_OFFSET}      : {len(log['boundary'])}")
    print(f"stray era markers cut    : {len(log['bce'])}")
    print(f"kept back by a guard     : {len(log['guarded'])}")
    print(f"calendar review tail     : {len(log['tail'])}")
    write_report(log)
    print(f"report                   : {REPORT.relative_to(ROOT)}")

    if not apply:
        print("\ndry run — nothing written. Re-run with --apply.")
        return

    for path in (MASTER, WEB):
        backup = path.with_suffix(path.suffix + ".pre-normalize")
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"backup                   : {backup.name}")

    MASTER.write_text(
        json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    WEB.write_text(
        pre + json.dumps(web_rows, ensure_ascii=False) + post, encoding="utf-8"
    )
    print("written                  : verified_clues_fa.json, Web/data/clues_fa.js")


if __name__ == "__main__":
    main()
