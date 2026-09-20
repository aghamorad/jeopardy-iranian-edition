# Farsi prose normalization — what changed, and what is left

The English edition prints Gregorian years and the Persian edition prints Shamsi ones, so every Gregorian year from **1800** on is rewritten into its Shamsi equivalent (`CE - 621`) and labelled خورشیدی; anything older keeps its digits and gains a میلادی label.

Years rewritten to Shamsi: **0**. Years already labelled میلادی, rewritten: **0** (**0** of them by CE − 622). Labels written over years that keep their digits: **0**. Stray era markers removed: **0**. Years a guard kept out of the rewrite: **338**. Distinct rows still unresolved: **10**.

These are what the run that wrote this report changed, so on a bank that is already normalized every count but the guards and the tail is zero — a second pass over a settled bank is a no-op by design.

## Left alone by a guard

span (196), labelled (80), citation (30), decade-pair (14), dual (14), imperial (4) — a citation year, a year already glossed in the other calendar, a year pinned by a Gregorian month name, or an Imperial-calendar year.

A year is settled only when the English twin confirms it by arithmetic (shamsi +621 or +622), states it identically (Gregorian), or the row settles it on its own — a Persian month name before a 12xx–14xx year makes it shamsi, a bare 19xx/20xx can only be Gregorian, and a bare 13xx in a row whose twin states only 20th- and 21st-century years can only be shamsi. Which side of Nowruz a converted year falls on comes from the same evidence: a date in the twin settles it (CE − 622 before the 21st of March, CE − 621 otherwise), and a dual gloss inside the row is the tiebreaker. Every year left unresolved lands here, and each one needs a call: shamsi or Gregorian (میلادی).

When none of that reaches a year, the bank is asked what it means by it: a bare year is shamsi if that exact year wears خورشیدی somewhere in the bank and never wears میلادی. The label is what carries the evidence, so a year the bank itself calls Gregorian stays Gregorian even in a Persian sentence. A decade takes the same route when its twin cannot help — `single_tehran_bazaar_to_megapolis_1000` reads «تله‌کابین تاریخی احداث‌شده در دهه ۱۳۵۰» and its twin at that id is the Rayy clue, but the bank dates ۱۳۵۰ خورشیدی thirty-seven times, so the decade is 1970s and is labelled `دهه ۱۳۵۰ خورشیدی`. Decades are labelled, never converted: the Shamsi decade is the Gregorian one less 620, so a Gregorian row keeps `دهه ۱۸۷۰ میلادی`.

Four-digit runs recognised as **not years** and left alone — **53 counts** and **4 labels** (serial numbers, clause numbers), counted once per row:

- counts: `۲۵۰۰` (court_persepolis_200), `۱۳۵۰` (court_persepolis_200_encore), `۲۵۰۰` (court_persepolis_200_encore), `۲۵۰۰` (double_a_republic_so_far_1200), `۱۰۰۰` (double_airlines_and_air_raids_800_a), `۴۲۰۰` (double_austerity_800), `۳۰۰۰` (double_ballots_barricades_400), `۲۰۰۰` (double_baluchi_divide_1200), `۴۲۰۰` (double_jebraily_neoliberal_1600), `۹۲۰۰` (double_kremlin_2000), `۱۱۲۹` (double_lur_khuzestan_2000), `۱۹۴۱` (double_reading_writing_and_reza_shah_800), `۱۷۱۰` (double_ruling_class_1600), `۴۲۰۰` (double_sanctions_profiteers_1200), `۲۵۰۰` (double_strikes_800) and 38 more
- labels: `۶۰۷۹` (double_airlines_and_air_raids_400_a), `۱۱۳۳` (double_clause_for_alarm_400), `۲۲۳۱` (double_status_anxiety_1600), `۱۳۲۵` (single_diplomacy_heels_600)

The recurring hard case is a row that mixes registers: a shamsi year and a Gregorian year for the same story, neither marked. The twin only settles years it happens to state, and it often states a neighbouring event's year instead.

## `double_a_marriage_of_inconvenience_400_a`
- **wrongLine** · `۶۰۰۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1951,)
  - …خیر، پاسخ درست ۶۰۰۰ الماس بود.…

## `double_ballots_barricades_400`
- **explanation** · `۱۰۰۰` — in the 1000–1499 band — could be either calendar
  - twin's years: (2019,)
  - …همیه‌بندی شبانه بنزین در ۲۴ آبان ۱۳۹۸ خورشیدی و افزایش نرخ آزاد آن از ۱۰۰۰ به ۳۰۰۰ تومان، موجب مسدود شدن فوری اتوبان‌ها توسط…

## `double_identity_2000`
- **clue** · `۱۱۲۹` — in the 1000–1499 band — could be either calendar
  - twin's years: (2016,)
  - …الینگ و هریس در شمارش ۱۱۲۹ پاسخ‌دهنده‌ای که در پیمایش اجتماعی ایران در سال ۱…
- **explanation** · `۱۱۲۹` — in the 1000–1499 band — could be either calendar
  - twin's years: (2016,)
  - …راسموس الینگ و کوان هریس ثبت کرده‌اند که از میان ۱۱۲۹ پاسخ‌دهنده‌ای که در پیمایش سال ۱۳۹۵ خورشیدی گزینه…

## `double_tahrir_ic_vocals_1600_a`
- **clue** · `۱۵۰۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1956,)
  - …گذاشته شد و شعر کلاسیک فارسی را به میلیون‌ها شنونده معرفی کرد؛ بیش از ۱۵۰۰ قسمت از آن با شاخه‌هایی چون «جاویدان» و «رنگارنگ»…

## `final_anquetil_duperron`
- **clue** · `۱۷۶۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1750, 1760, 1771)
  - …این فرانسوی در دههٔ ۱۷۶۰ با دست‌نوشته‌های اوستا از هند به خانه بازگشت و در…
- **explanation** · `۱۷۵۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1750, 1760, 1771)
  - …آبراهام ایاسنت آنکتیل دوپرون در دههٔ ۱۷۵۰ به هند سفر کرد، اوستایی را از موبدان پارسی آموخت…

## `single_bazaar_barricade_200`
- **explanation** · `۲۴۸۳` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1979,)
  - …احمد اشرف و علی بنوعزیزی اثبات می‌کنند که ۶۴ درصد از مجموع ۲۴۸۳ مورد تظاهرات توده‌ای در انقلاب سال ۱۳۵۷ خورشیدی ت…

## `single_periphery_1000`
- **clue** · `۱۱۲۹` — in the 1000–1499 band — could be either calendar
  - twin's years: (2016,)
  - …در پیمایش اجتماعی ۱۳۹۵ خورشیدی ایران، از میان ۱۱۲۹ پاسخ‌دهنده‌ای که هویت قومی خود را نمی‌دانستند، دق…

## `single_shah_ping_for_antiques_800_a`
- **wrongLine** · `۳۳۸۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1926,)
  - …خیر، پاسخ درست ۳۳۸۰ الماس بود.…

## `single_struct_800`
- **correctLine** · `۲۵۳۵` — outside the band — the twin states no year, or this is not a year
  - twin's years: (1355, 1976, 2535)
  - …۲۵۳۵. کاملاً درسته؛ هزار و خرده‌ای سال را یک‌شبه جلو ر…

## `single_trunk_call_800`
- **correctLine** · `۱۵۰۰` — outside the band — the twin states no year, or this is not a year
  - twin's years: —
  - …۱۵۰۰. ثبت‌نام سریع بود، چون جایگزینش قفل در بود.…

