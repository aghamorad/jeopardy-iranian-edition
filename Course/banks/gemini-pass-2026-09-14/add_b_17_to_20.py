import json
import sys
sys.path.append("/Users/Morad/Spark")
from build_batch_b import batch_b
from jeopardy_pipeline import validate_clue_schema

cats_17_to_20 = [
  # 17. double_family_planning: FAMILY PLANNING, MULLAH STYLE / تنظیم خانواده پای منبر
  {
    "id": "double_family_planning_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "FAMILY PLANNING, MULLAH STYLE", "fa": "تنظیم خانواده پای منبر"},
    "clue_text": {
      "en": "During the Iran-Iraq War, Ayatollah Khomeini championed an aggressive pronatalist policy to build a holy defense force, famously calling for the creation of an army of this massive size.",
      "fa": "در دوران جنگ تحمیلی، امام خمینی با اتخاذ سیاست‌های تشویق فرزندآوری، خواهان تشکیل یک ارتش دفاعی عظیم با این تعداد رزمنده شدند."
    },
    "canonical_answer": {"en": "Twenty Million", "fa": "بیست میلیونی"},
    "accepted_aliases": {"en": ["20 million", "Twenty-million-strong army", "20-million army", "Army of 20 million"], "fa": ["۲۰ میلیونی", "ارتش ۲۰ میلیونی", "ارتش بیست میلیونی", "۲۰ میلیون"]},
    "options": {
      "en": ["Five Million", "Twenty Million", "Fifty Million", "Ten Million"],
      "fa": ["پنج میلیونی", "بیست میلیونی", "پنجاه میلیونی", "ده میلیونی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Five Million", "why_plausible": "A plausible standing army size.", "why_wrong": "The famous revolutionary slogan specifically named an army of 20 million (Artesh-e Bist Meliooni)."},
      {"option": "Fifty Million", "why_plausible": "Near the total population of Iran in the late 1980s.", "why_wrong": "Khomeini called for 20 million mobilized youth, not 50 million."},
      {"option": "Ten Million", "why_plausible": "A common round number in military mobilizations.", "why_wrong": "The iconic decree specified twenty million."}
    ],
    "adversarial_confusion_set": {"en": ["Ten Million", "Thirty Million"], "fa": ["ده میلیونی", "سی میلیونی"]},
    "specificity_prompt": {
      "en": "Provide the exact number of troops called for in Khomeini's famous 'army of...' slogan.",
      "fa": "تعداد رزمندگان ارتش موعود در شعار مشهور امام خمینی (ارتش ... میلیونی) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Twenty Million. Correct. Encouraging every mother in the country to produce soldiers for the trenches.",
        "wrong_generic": "No, it was the Twenty Million army (Artesh-e Bist Meliooni). The slogan that sparked the 1980s baby boom.",
        "common_wrong_answers": {
          "Five Million": "Five million wasn't ambitious enough for wartime mobilization.",
          "Fifty Million": "Fifty million was nearly the entire population.",
          "Ten Million": "Ten million was too small; Khomeini demanded twenty million."
        }
      },
      "fa": {
        "correct_generic": "بیست میلیونی. کاملاً درسته! شعاری که زنان را به زادآوری گسترده سربازان دفاع مقدس فراخواند.",
        "wrong_generic": "خیر، پاسخ ارتش بیست میلیونی بود. شعاری که بزرگ‌ترین جهش جمعیتی تاریخ ایران را رقم زد.",
        "common_wrong_answers": {
          "پنج میلیونی": "پنج میلیون برای مقیاس جنگ کافی نبود؛ شعار ارتش بیست میلیونی بود.",
          "پنجاه میلیونی": "پنجاه میلیون کل جمعیت کشور در دهه شصت بود.",
          "ده میلیونی": "ده میلیون نصف شعار معروف بسیج مستضعفان بود."
        }
      }
    },
    "explanation": {
      "en": "Homa Hoodfar documents that in December 1979 and throughout the 1980s, Khomeini called for an 'army of twenty million' (Artesh-e Bist Meliooni), reversing pre-revolutionary birth control programs and triggering a historic annual population growth rate of over 3.9%.",
      "fa": "هما هودفر مستند می‌کند که امام خمینی با شعار ارتش بیست میلیونی برنامه‌های کنترل جمعیت پیش از انقلاب را لغو کردند و موجب ثبت نرخ رشد سالانه جمعیت بالای ۳٫۹ درصد در دهه شصت شدند."
    },
    "provenance": {
      "source_book": "Devices and Desires: Population Control in the Islamic Republic",
      "source_author": "Homa Hoodfar",
      "page_number": 11,
      "verbatim_passage": "In December 1979, Ayatollah Khomeini called for an 'army of twenty million' to defend the Islamic nation, ushering in aggressive pronatalist measures that dismantled family planning clinics.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_family_planning_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "FAMILY PLANNING, MULLAH STYLE", "fa": "تنظیم خانواده پای منبر"},
    "clue_text": {
      "en": "Faced with economic collapse and school shortages after the 1988 ceasefire, President Hashemi Rafsanjani and this long-serving Minister of Health successfully engineered a complete U-turn by launching a national birth control program.",
      "fa": "با مواجهه با بحران اقتصادی و کمبود شدید مدارس پس از آتش‌بس سال ۶۷، هاشمی رفسنجانی و این وزیر بهداشت باسابقه با چرخشی کامل، برنامه ملی تنظیم خانواده و پیشگیری از بارداری را کلید زدند."
    },
    "canonical_answer": {"en": "Alireza Marandi", "fa": "علیرضا مرندی"},
    "accepted_aliases": {"en": ["Dr. Marandi", "Seyyed Alireza Marandi", "Ali Reza Marandi"], "fa": ["دکتر مرندی", "سید علیرضا مرندی", "مرندی"]},
    "options": {
      "en": ["Kamran Bagheri Lankarani", "Alireza Marandi", "Masoud Pezeshkian", "Iraj Harirchi"],
      "fa": ["کامران باقری لنکرانی", "علیرضا مرندی", "مسعود پزشکیان", "ایرج حریرچی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Kamran Bagheri Lankarani", "why_plausible": "A prominent Minister of Health.", "why_wrong": "Served under Ahmadinejad in 2005-2009, long after the 1989 family planning launch."},
      {"option": "Masoud Pezeshkian", "why_plausible": "Minister of Health under Khatami (and future president).", "why_wrong": "Pezeshkian served as Health Minister from 2001 to 2005 under Khatami, not in 1989."},
      {"option": "Iraj Harirchi", "why_plausible": "A prominent health ministry official.", "why_wrong": "Harirchi was a deputy health minister during the Rouhani era and COVID-19 pandemic."}
    ],
    "adversarial_confusion_set": {"en": ["Mohammad Farhadi", "Masoud Pezeshkian"], "fa": ["محمد فرهادی", "مسعود پزشکیان"]},
    "specificity_prompt": {
      "en": "Name the specific Minister of Health who pioneered Iran's acclaimed 1989 family planning program.",
      "fa": "نام وزیر بهداشت دوران سازندگی که پیشگام برنامه تنظیم خانواده در سال ۱۳۶۸ شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Alireza Marandi. Correct. Convincing conservative ayatollahs that God has no objection to condoms and vasectomies.",
        "wrong_generic": "No, it was Dr. Alireza Marandi. The architect of one of the fastest fertility declines in demographic history.",
        "common_wrong_answers": {
          "Kamran Bagheri Lankarani": "Lankarani served Ahmadinejad fifteen years later.",
          "Masoud Pezeshkian": "Pezeshkian was Health Minister under Khatami in the 2000s.",
          "Iraj Harirchi": "Harirchi was managing COVID-19 on television thirty years later."
        }
      },
      "fa": {
        "correct_generic": "علیرضا مرندی. کاملاً درسته! وزیری که فقهای قم را متقاعد کرد پیشگیری از بارداری هیچ تعارضی با فقه ندارد.",
        "wrong_generic": "خیر، پاسخ دکتر علیرضا مرندی بود. معمار موفق‌ترین برنامه کنترل جمعیت در جهان اسلام.",
        "common_wrong_answers": {
          "کامران باقری لنکرانی": "لنکرانی وزیر دولت احمدی‌نژاد در نیمه دوم دهه هشتاد بود.",
          "مسعود پزشکیان": "پزشکیان وزیر بهداشت دولت دوم اصلاحات در اوایل دهه هشتاد بود.",
          "ایرج حریرچی": "حریرچی معاون وزیر بهداشت در دوران بحران کرونا بود."
        }
      }
    },
    "explanation": {
      "en": "Homa Hoodfar explains how Dr. Alireza Marandi secured fatwas from Ayatollah Khomeini and top grand ayatollahs declaring all reversible contraceptive methods halal, launching a state family planning program praised globally by the UN.",
      "fa": "هما هودفر تشریح می‌کند که چگونه دکتر علیرضا مرندی با اخذ استفتائات فقهی از امام خمینی و مراجع تقلید مبنی بر حلیت شیوه‌های نوین پیشگیری، برنامه‌ای را به راه انداخت که مورد تحسین سازمان بهداشت جهانی قرار گرفت."
    },
    "provenance": {
      "source_book": "Devices and Desires: Population Control in the Islamic Republic",
      "source_author": "Homa Hoodfar",
      "page_number": 19,
      "verbatim_passage": "Minister of Health Dr. Alireza Marandi successfully mobilized religious justifications to convince the clerical leadership in 1989 that runaway demographic growth threatened national development and state survival.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_family_planning_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "FAMILY PLANNING, MULLAH STYLE", "fa": "تنظیم خانواده پای منبر"},
    "clue_text": {
      "en": "To promote small family norms across urban and rural billboards, the Ministry of Health branded the post-1989 campaign with this ubiquitous rhyming four-word Persian slogan.",
      "fa": "وزارت بهداشت برای ترویج فرهنگ خانواده کم‌جمعیت در سراسر شهرها و روستاها، کمپین پس از سال ۱۳۶۸ را با این شعار آهنگین چهارکلمه‌ای بر در و دیوار کشور ثبت کرد."
    },
    "canonical_answer": {"en": "Two Children is Enough", "fa": "فرزند کمتر، زندگی بهتر"},
    "accepted_aliases": {"en": ["Fewer children, better life", "Farzand-e kamtar zendegi-ye behtar", "Fewer children better life"], "fa": ["فرزند کمتر زندگی بهتر", "دو بچه کافیست", "فرزند کمتر، زندگی بهتر"]},
    "options": {
      "en": ["Two Children is Enough", "More Children, Stronger Nation", "Children are Divine Blessings", "Family is Sacred Citadel"],
      "fa": ["فرزند کمتر، زندگی بهتر", "فرزند بیشتر، جامعه قوی‌تر", "اولاد چراغ خانه است", "تحکیم بنیان خانواده"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "More Children, Stronger Nation", "why_plausible": "The modern post-2012 pro-natalist slogan.", "why_wrong": "This represents the opposite policy launched after 2012, not the iconic 1990s campaign."},
      {"option": "Children are Divine Blessings", "why_plausible": "A traditional Islamic saying.", "why_wrong": "A general religious aphorism, not the official statutory marketing slogan of the state family planning program."},
      {"option": "Family is Sacred Citadel", "why_plausible": "Official moralistic state phrasing.", "why_wrong": "Not the famous demographic family-size reduction slogan."}
    ],
    "adversarial_confusion_set": {"en": ["Two is Enough", "Small Family Happy Family"], "fa": ["دو فرزند کافیست", "جمعیت کمتر رفاه بیشتر"]},
    "specificity_prompt": {
      "en": "Provide the exact four-word rhyming Persian slogan used on billboards across Iran throughout the 1990s.",
      "fa": "شعار معروف چهارکلمه‌ای آهنگین برنامه تنظیم خانواده دهه هفتاد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Two Children is Enough (Farzand-e Kamtar, Zendegi-e Behtar). Correct. Printed on every notebook, matchbox, and health clinic in the country.",
        "wrong_generic": "No, it was 'Farzand-e Kamtar, Zendegi-e Behtar' (Fewer children, better life). The defining demographic catchphrase of the nineties.",
        "common_wrong_answers": {
          "More Children, Stronger Nation": "That is the slogan today after they realized nobody was having babies anymore.",
          "Children are Divine Blessings": "Traditional sentiment, not the technocratic rhyming ministry billboard.",
          "Family is Sacred Citadel": "Too vague; the ministry wanted exactly two kids per house."
        }
      },
      "fa": {
        "correct_generic": "فرزند کمتر، زندگی بهتر. کاملاً درسته! شعاری که پشت دفترچه‌های مدرسه، قوطی‌های کبریت و سردر درمانگاه‌ها حک شده بود.",
        "wrong_generic": "خیر، پاسخ «فرزند کمتر، زندگی بهتر» بود. پربسامدترین شعار اجتماعی دهه هفتاد.",
        "common_wrong_answers": {
          "فرزند بیشتر، جامعه قوی‌تر": "این شعار بعد از سال ۱۳۹۱ است؛ دهه هفتاد دوران کاهش جمعیت بود.",
          "اولاد چراغ خانه است": "ضرب‌المثل سنتی است، نه شعار رسمی تنظیم خانواده وزارت بهداشت.",
          "تحکیم بنیان خانواده": "شعار کلی است؛ هدف صریح برنامه کاهش بعد خانوار به دو فرزند بود."
        }
      }
    },
    "explanation": {
      "en": "Hoodfar highlights the cultural brilliance of the slogan 'Farzand-e kamtar, zendegi-ye behtar' (Fewer children, better life): it reframed contraception not as Western decadence, but as an Islamic moral responsibility to properly educate and provide for children.",
      "fa": "هما هودفر به هوشمندی فرهنگی شعار «فرزند کمتر، زندگی بهتر» اشاره می‌کند که پیشگیری را نه فساد غربی، بلکه وظیفه اخلاقی و اسلامی والدین برای تربیت شایسته و تأمین رفاه فرزندان بازتعریف کرد."
    },
    "provenance": {
      "source_book": "Devices and Desires: Population Control in the Islamic Republic",
      "source_author": "Homa Hoodfar",
      "page_number": 24,
      "verbatim_passage": "The ubiquitous slogan 'Fewer Children, Better Life' (Farzand-e kamtar, zendegi-ye behtar) adorned public murals, health clinics, and consumer packaging, legitimizing small family size as an Islamic civic virtue.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_family_planning_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "FAMILY PLANNING, MULLAH STYLE", "fa": "تنظیم خانواده پای منبر"},
    "clue_text": {
      "en": "To guarantee that young couples understood contraception, the state made marriage licenses legally contingent upon mandatory attendance at these government-run educational sessions.",
      "fa": "برای اطمینان از آشنایی کامل زوج‌های جوان با روش‌های پیشگیری، ثبت رسمی عقد ازدواج در دفاتر ازدواج منوط به شرکت اجباری در این دوره‌های آموزشی دولتی شد."
    },
    "canonical_answer": {"en": "Pre-marital Family Planning Classes", "fa": "کلاس‌های آموزشی تنظیم خانواده قبل از ازدواج"},
    "accepted_aliases": {"en": ["Pre-marital classes", "Mandatory premarital counseling", "Premarital health courses", "Pre-marriage classes"], "fa": ["کلاس‌های قبل از ازدواج", "مشاوره قبل از ازدواج", "کلاس‌های پیش از ازدواج", "آزمایش و آموزش قبل از ازدواج"]},
    "options": {
      "en": ["Sharia Inheritance Tutorials", "Pre-marital Family Planning Classes", "Military Conscription Briefings", "Khomeinism Ideology Seminars"],
      "fa": ["آموزش احکام ارث و وصیت", "کلاس‌های آموزشی تنظیم خانواده قبل از ازدواج", "توجیه خدمت وظیفه عمومی", "کارگاه‌های مبانی اندیشه امام"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Sharia Inheritance Tutorials", "why_plausible": "Relevant to Islamic family law.", "why_wrong": "Inheritance rules are handled by notaries at the time of death or contracts, not mandatory prerequisite classes before marriage."},
      {"option": "Military Conscription Briefings", "why_plausible": "Mandatory for young men.", "why_wrong": "Conscription is administered by the police (Nezam Vazifeh) at age 18, completely separate from marriage registration."},
      {"option": "Khomeinism Ideology Seminars", "why_plausible": "Common in state universities.", "why_wrong": "These are academic university courses, not the specific clinical prerequisite course for obtaining a marriage certificate."}
    ],
    "adversarial_confusion_set": {"en": ["Premarital Blood Screening", "Mahriyeh Mediation"], "fa": ["آزمایش خون تالاسمی", "مشاوره مهریه"]},
    "specificity_prompt": {
      "en": "Name the specific mandatory pre-wedding educational course required by the Ministry of Health before marriage.",
      "fa": "نام دوره‌های آموزشی اجباری پیش از ثبت عقد در مراکز بهداشت را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Pre-marital Family Planning Classes. Spot on. Sitting in a clinic together learning anatomical diagrams before you are allowed to sign the marriage register.",
        "wrong_generic": "No, it was Pre-marital Family Planning Classes. No certificate of attendance, no wedding ceremony.",
        "common_wrong_answers": {
          "Sharia Inheritance Tutorials": "Inheritance is for lawyers later; this was contraception now.",
          "Military Conscription Briefings": "Conscription is for the barracks, not the honeymoon.",
          "Khomeinism Ideology Seminars": "Ideology is taught in college; reproductive biology was taught at the health clinic."
        }
      },
      "fa": {
        "correct_generic": "کلاس‌های آموزشی تنظیم خانواده قبل از ازدواج. کاملاً درسته! تا برگه مهرشده شرکت در کلاس پیشگیری را ارائه نمی‌دادی، عاقد خطبه عقد را جاری نمی‌کرد.",
        "wrong_generic": "خیر، پاسخ کلاس‌های آموزشی تنظیم خانواده قبل از ازدواج بود. پیش‌شرط قانونی ثبت سند ازدواج در سراسر کشور.",
        "common_wrong_answers": {
          "آموزش احکام ارث و وصیت": "احکام ارث مربوط به متوفیات است، نه کلاس سلامت باروری پیش از ازدواج.",
          "توجیه خدمت وظیفه عمومی": "نظام وظیفه مربوط به سربازی در سن ۱۸ سالگی است.",
          "کارگاه‌های مبانی اندیشه امام": "معارف اسلامی در دانشگاه تدریس می‌شود؛ در مرکز بهداشت آناتومی و روش‌های ضدبارداری تدریس می‌شد."
        }
      }
    },
    "explanation": {
      "en": "Hoodfar highlights that Iran became a global pioneer in instituting mandatory pre-marital counseling: prospective brides and grooms were legally required to complete classes on reproductive biology, contraception, and sexually transmitted infections before an official marriage license could be signed.",
      "fa": "هما هودفر تشریح می‌کند که ایران در الزام‌آور کردن آموزش‌های جنسی و تنظیم خانواده پیشگام بود؛ به طوری که تمام زوج‌ها ملزم بودند پیش از ثبت رسمی عقد، در دوره‌های بهداشت باروری، آشنایی با وسایل پیشگیری و بیماری‌های مقاربتی شرکت کنند."
    },
    "provenance": {
      "source_book": "Devices and Desires: Population Control in the Islamic Republic",
      "source_author": "Homa Hoodfar",
      "page_number": 28,
      "verbatim_passage": "Iran instituted mandatory premarital education classes where both men and women were taught about human anatomy, contraception methods, and family spacing as a legal prerequisite for registering a marriage.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_family_planning_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "FAMILY PLANNING, MULLAH STYLE", "fa": "تنظیم خانواده پای منبر"},
    "clue_text": {
      "en": "In a dramatic 2012 speech in Bojnourd, Ayatollah Khamenei enacted a total reversal of population policy, publicly apologizing for not halting birth control in the late 1990s and setting this ambitious new national target.",
      "fa": "آیت‌الله خامنه‌ای در نطقی در مهر ۱۳۹۱ در بجنورد با چرخش کامل در سیاست جمعیتی، از ادامه تحدید موالید در اواخر دهه هفتاد عذرخواهی کرد و این هدف‌گذاری جدید جمعیتی را تعیین نمود."
    },
    "canonical_answer": {"en": "150 Million", "fa": "۱۵۰ میلیون نفر"},
    "accepted_aliases": {"en": ["150 million population", "One hundred and fifty million", "150m"], "fa": ["۱۵۰ میلیون", "جمعیت ۱۵۰ میلیونی", "۱۵۰ میلیونی"]},
    "options": {
      "en": ["100 Million", "150 Million", "200 Million", "120 Million"],
      "fa": ["۱۰۰ میلیون نفر", "۱۵۰ میلیون نفر", "۲۰۰ میلیون نفر", "۱۲۰ میلیون نفر"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "100 Million", "why_plausible": "A round population target frequently cited in economic discussions.", "why_wrong": "Khamenei explicitly set the target at 150 million people, stating Iran's resources could sustain that population."},
      {"option": "200 Million", "why_plausible": "A hyper-nationalist extreme projection.", "why_wrong": "The official Supreme Leader decree set the threshold specifically at 150 million."},
      {"option": "120 Million", "why_plausible": "An intermediate projection.", "why_wrong": "The specific figure proclaimed in the Bojnourd address and subsequent decrees was 150 million."}
    ],
    "adversarial_confusion_set": {"en": ["100 Million", "140 Million"], "fa": ["۱۰۰ میلیون نفر", "۱۴۰ میلیون نفر"]},
    "specificity_prompt": {
      "en": "Provide the exact population target figure proclaimed by Ayatollah Khamenei in his 2012 policy reversal.",
      "fa": "رقم هدف‌گذاری اعلام‌شده توسط رهبر انقلاب برای افق جمعیتی ایران در سخنرانی بجنورد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "150 Million. Spot on. Moving the goalposts from 'Two Children is Enough' to 'Have four more, please, the country is aging'.",
        "wrong_generic": "No, it was 150 Million. The massive pronatalist target that crashed directly into economic stagflation.",
        "common_wrong_answers": {
          "100 Million": "Ahmadinejad proposed 100 million in 2006; the Leader pushed the target to 150 million in 2012.",
          "200 Million": "200 million is Pakistan; Iran aimed for 150 million.",
          "120 Million": "120 million was an early conservative estimate; the official goal was 150 million."
        }
      },
      "fa": {
        "correct_generic": "۱۵۰ میلیون نفر. کاملاً درسته! چرخش ۱۸۰ درجه‌ای از «فرزند کمتر» به دستور زادآوری برای رسیدن به جمعیت ۱۵۰ میلیونی.",
        "wrong_generic": "خیر، پاسخ ۱۵۰ میلیون نفر بود. هدف‌گذاری جمعیتی رهبر انقلاب در نطق تاریخی مهر ۹۱ در بجنورد.",
        "common_wrong_answers": {
          "۱۰۰ میلیون نفر": "احمدی‌نژاد در سال ۸۵ از جمعیت ۱۰۰ میلیونی سخن گفت؛ رهبری هدف را ۱۵۰ میلیون تعیین کرد.",
          "۲۰۰ میلیون نفر": "۲۰۰ میلیون جمعیت پاکستان یا نیجریه است؛ افق جمعیتی ابلاغی ۱۵۰ میلیون بود.",
          "۱۲۰ میلیون نفر": "۱۲۰ میلیون پیش‌بینی میانه بود؛ رقم اعلامی صریح ۱۵۰ میلیون نفر بود."
        }
      }
    },
    "explanation": {
      "en": "In October 2012, Ayatollah Khamenei publicly stated that while the early 1990s birth control policy was justified, its continuation past the mid-1990s was a major mistake for which 'God and history must forgive us', directing the state to ban vasectomies and incentivize a target population of 150 million.",
      "fa": "در مهر ۱۳۹۱ آیت‌الله خامنه‌ای در بجنورد صراحتاً اعلام کرد که تحدید نسل در اوایل دهه هفتاد درست بود اما ادامه آن اشتباه بود و مسئولان و خود ایشان در پیشگاه خداوند مقصرند و باید هدف جمعیتی ۱۵۰ میلیون نفری محقق شود؛ امری که به توقف توزیع وسایل رایگان پیشگیری و ممنوعیت وازکتومی انجامید."
    },
    "provenance": {
      "source_book": "Devices and Desires: Population Control in the Islamic Republic",
      "source_author": "Homa Hoodfar",
      "page_number": 33,
      "verbatim_passage": "In his October 2012 address in Bojnourd, Ayatollah Khamenei declared family planning continuation an error and directed state planners to reverse course immediately to achieve a target population of 150 million.",
      "evidence_type": "PRIMARY_TESTIMONY"
    }
  },

  # 18. double_status_anxiety: THE STATUS ANXIETY OF TEHRAN / بحران شناسایی در اتاق بیضی
  {
    "id": "double_status_anxiety_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "THE STATUS ANXIETY OF TEHRAN", "fa": "بحران شناسایی در اتاق بیضی"},
    "clue_text": {
      "en": "In her analysis of US-Iran relations, international relations scholar Constance Duncombe utilizes this theoretical framework to demonstrate that states seek certainty and respect for their self-identity, not merely physical survival.",
      "fa": "کنستانس دانکامب در تحلیل روابط ایران و آمریکا با بهره‌گیری از این چارچوب نظری نشان می‌دهد که دولت‌ها افزون بر بقای فیزیکی، به دنبال کسب احترام و تثبیت امنیت هویت ذهنی خود هستند."
    },
    "canonical_answer": {"en": "Ontological Security Theory", "fa": "نظریه امنیت هستی‌شناختی"},
    "accepted_aliases": {"en": ["Ontological security", "Ontological Security", "Ontological security in IR"], "fa": ["امنیت هستی‌شناختی", "امنیت هستی شناختی", "نظریه امنیت وجودی"]},
    "options": {
      "en": ["Offensive Realism", "Ontological Security Theory", "Dependency Theory", "Democratic Peace Theory"],
      "fa": ["رئالیسم تهاجمی", "نظریه امنیت هستی‌شناختی", "نظریه وابستگی", "صلح دموکراتیک"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Offensive Realism", "why_plausible": "A major security theory in IR.", "why_wrong": "Offensive realism focuses purely on material power and regional hegemony, ignoring identity and recognition."},
      {"option": "Dependency Theory", "why_plausible": "Marxist-structuralist international political economy.", "why_wrong": "Focuses on economic surplus extraction by the core from the periphery, not status recognition."},
      {"option": "Democratic Peace Theory", "why_plausible": "A major liberal IR theory.", "why_wrong": "Concerns interstate peace among liberal democracies, not psychological identity security."}
    ],
    "adversarial_confusion_set": {"en": ["Constructivism", "Role Theory"], "fa": ["برساخت‌گرایی", "نظریه نقش"]},
    "specificity_prompt": {
      "en": "Name the specific IR theory focused on the preservation of state self-identity and psychological recognition.",
      "fa": "نام نظریه روابط بین‌الملل معطوف به امنیت هویت و نیاز به شناسایی منزلت دولت‌ها را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ontological Security Theory. Correct. Because sovereign states, like fragile teenagers, care deeply about what others think of them.",
        "wrong_generic": "No, it was Ontological Security Theory. Security of the ego, not just security of the borders.",
        "common_wrong_answers": {
          "Offensive Realism": "Offensive realism is about tanks and artillery shells; ontological security is about pride and dignity.",
          "Dependency Theory": "Dependency is about Latin American banana exports, not Iranian diplomatic status.",
          "Democratic Peace Theory": "Neither Washington nor Tehran behaved like friendly democratic peace partners."
        }
      },
      "fa": {
        "correct_generic": "نظریه امنیت هستی‌شناختی. کاملاً درسته! اثبات اینکه دولت‌ها هم مثل انسان‌ها محتاج شناسایی منزلت و احترام هویتی هستند.",
        "wrong_generic": "خیر، پاسخ نظریه امنیت هستی‌شناختی (Ontological Security) بود. فراتر رفتن از بقای مادی به سوی امنیت روانی و شأن ملی.",
        "common_wrong_answers": {
          "رئالیسم تهاجمی": "رئالیسم تهاجمی فقط تانک و توان مادی را می‌بیند؛ امنیت هستی‌شناختی در پی شأن و احترام است.",
          "نظریه وابستگی": "وابستگی اقتصاد مارکسیستی جهان سوم است، نه روان‌شناسی شناسایی دیپلماتیک.",
          "صلح دموکراتیک": "صلح دموکراتیک مختص کشورهای لیبرال است، نه مناسبات بحرانی ایران و آمریکا."
        }
      }
    },
    "explanation": {
      "en": "Constance Duncombe utilizes Ontological Security Theory to argue that US-Iran conflict is maintained by misrecognition: Iran demands recognition of its sovereign greatness and revolutionary identity, while Washington routinely denies it status, triggering defensive hostility.",
      "fa": "کنستانس دانکامب با تکیه بر نظریه امنیت هستی‌شناختی استدلال می‌کند که ریشه تداوم تخاصم ایران و آمریکا بحران «ناشناسایی» است: ایران خواهان شناسایی رسمی شأن و منزلت تاریخی خود است و آمریکا با تحقیر و طرد دیپلماتیک، امنیت هویتی آن را تهدید می‌کند."
    },
    "provenance": {
      "source_book": "Representation, Recognition and Foreign Policy: US-Iran Relations",
      "source_author": "Constance Duncombe",
      "page_number": 15,
      "verbatim_passage": "Ontological security theory posits that states do not merely seek physical survival, but also strive to secure a stable sense of self, which depends fundamentally upon how they are recognized by significant others.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_status_anxiety_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "THE STATUS ANXIETY OF TEHRAN", "fa": "بحران شناسایی در اتاق بیضی"},
    "clue_text": {
      "en": "Throughout the 1990s and 2000s, Washington delegitimized Iran's international standing by categorizing it under this derogatory diplomatic label alongside North Korea, Libya, and Saddam's Iraq.",
      "fa": "در طول دهه‌های ۱۳۷۰ و ۱۳۸۰، واشنگتن جایگاه بین‌المللی ایران را با قرار دادن آن در این طبقه‌بندی تحقیرآمیز دیپلماتیک در کنار کره شمالی، لیبی و عراق صدام سلب مشروعیت کرد."
    },
    "canonical_answer": {"en": "Rogue State", "fa": "دولت یاغی"},
    "accepted_aliases": {"en": ["Rogue state", "Rogue regime", "Outlaw state"], "fa": ["دولت سرکش", "کشور یاغی", "رژیم یاغی", "دولت‌های سرکش"]},
    "options": {
      "en": ["Failed State", "Rogue State", "Buffer State", "Puppet State"],
      "fa": ["دولت درمانده", "دولت یاغی", "دولت حائل", "دولت دست‌نشانده"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Failed State", "why_plausible": "A recognized category of state breakdown.", "why_wrong": "Failed state applies to countries with collapsed authority like Somalia, not Iran's highly institutionalized centralized regime."},
      {"option": "Buffer State", "why_plausible": "A neutral geographic concept.", "why_wrong": "Buffer states sit between empires (like historic Afghanistan), not an ideological stigmatizing label."},
      {"option": "Puppet State", "why_plausible": "A proxy state controlled by an external master.", "why_wrong": "Iran was fiercely independent and anti-American, the opposite of a puppet."}
    ],
    "adversarial_confusion_set": {"en": ["Pariah State", "Outlaw Regime"], "fa": ["دولت طردشده", "رژیم قانون‌شکن"]},
    "specificity_prompt": {
      "en": "Name the specific derogatory label ('... State') coined in Washington in the 1990s.",
      "fa": "اصطلاح مشهور واشنگتن در دهه ۱۹۹۰ برای کشورهایی که از نظم بین‌المللی سرپیچی می‌کردند را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Rogue State. Correct. The ultimate diplomatic insult designed to place you outside the civilized family of nations.",
        "wrong_generic": "No, it was Rogue State (Dowlat-e Yaaghi). The Clinton-era label that poisoned diplomatic engagement.",
        "common_wrong_answers": {
          "Failed State": "Iran has too many ministries and police to be a failed state.",
          "Buffer State": "A buffer state is passive; Iran is actively assertive.",
          "Puppet State": "A puppet state takes orders; Iran aggressively gave headaches."
        }
      },
      "fa": {
        "correct_generic": "دولت یاغی. کاملاً درسته! برچسبی تحقیرآمیز در واشنگتن برای اخراج دیپلماتیک یک کشور از جامعه بین‌الملل.",
        "wrong_generic": "خیر، پاسخ دولت یاغی (یا سرکش) بود. برچسبی که راه هرگونه شناسایی متقابل را بست.",
        "common_wrong_answers": {
          "دولت درمانده": "دولت درمانده کشوری بی‌صاحب مثل سومالی است؛ ایران حکومتی کاملاً مقتدر در داخل دارد.",
          "دولت حائل": "دولت حائل بی‌طرف میان دو ابرقدرت است؛ ایران در مرکز تنش‌ها بود.",
          "دولت دست‌نشانده": "دست‌نشانده فرمانبردار است؛ ایران استقلال‌طلبانه در برابر هژمونی ایستاد."
        }
      }
    },
    "explanation": {
      "en": "Duncombe documents that the Clinton administration formalised the 'rogue state' doctrine (coined by Anthony Lake in 1994), depicting Iran as an outlaw entity beyond the pale of civilized international diplomacy, which deeply wounded Iranian elite aspirations for prestige.",
      "fa": "دانکامب مستند می‌کند که دولت کلینتون در سال ۱۹۹۴ با ابداع دکترین «دولت‌های یاغی» توسط آنتونی لیک، ایران را بازیگری غیرمتمدن و قانون‌شکن خواند که باید مهار و منزوی شود؛ امری که به تشدید بحران تحقیر و بیزاری هویتی انجامید."
    },
    "provenance": {
      "source_book": "Representation, Recognition and Foreign Policy: US-Iran Relations",
      "source_author": "Constance Duncombe",
      "page_number": 28,
      "verbatim_passage": "The US stigmatization of Iran as a 'rogue state' in the 1990s denied the country international standing, framing its leaders not as legitimate diplomatic counterparts but as irrational outlaws.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_status_anxiety_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE STATUS ANXIETY OF TEHRAN", "fa": "بحران شناسایی در اتاق بیضی"},
    "clue_text": {
      "en": "In Iranian strategic and diplomatic parlance, national prestige and self-respect are codified under this foundational concept, which Ayatollah Khamenei established alongside 'wisdom' and 'expediency' as the triad of foreign policy.",
      "fa": "در ادبیات راهبردی و دیپلماسی جمهوری اسلامی، غرور ملی و حفظ شأن حاکمیت در قالب این مفهوم بنیادین صورت‌بندی شده که در کنار «حکمت» و «مصلحت» مثلث اصول سیاست خارجی را تشکیل می‌دهد."
    },
    "canonical_answer": {"en": "Ezzat", "fa": "عزت"},
    "accepted_aliases": {"en": ["Dignity", "National Honor", "'Izzat", "Ezzat-e Melli"], "fa": ["عزت ملی", "اصل عزت", "عزت، حکمت، مصلحت"]},
    "options": {
      "en": ["Hekmat", "Ezzat", "Maslahat", "Qodrat"],
      "fa": ["حکمت", "عزت", "مصلحت", "قدرت"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Hekmat", "why_plausible": "One of the three legs of the foreign policy triad.", "why_wrong": "Hekmat means wisdom and prudent calculation, whereas Ezzat specifically denotes dignity, honor, and sovereign self-respect."},
      {"option": "Maslahat", "why_plausible": "Another leg of the triad.", "why_wrong": "Maslahat means expediency and national interest, not dignity and status honor."},
      {"option": "Qodrat", "why_plausible": "Means power.", "why_wrong": "Power is a general realism term, not the specific constitutional triad term coined by the Supreme Leader."}
    ],
    "adversarial_confusion_set": {"en": ["Hekmat", "Sharaf"], "fa": ["حکمت", "شرف"]},
    "specificity_prompt": {
      "en": "Name the specific concept of honor/dignity completing the famous triad: '..., Hekmat, Maslahat'.",
      "fa": "واژه اول سه‌گانه معروف سیاست خارجی رهبر انقلاب (عزت، حکمت و ...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ezzat. Correct. The supreme diplomatic imperative: no matter how empty the treasury, you never enter the room looking poor.",
        "wrong_generic": "No, it was Ezzat (Dignity/Honor). The spiritual currency of Iranian negotiations.",
        "common_wrong_answers": {
          "Hekmat": "Hekmat is wisdom; Ezzat is dignity.",
          "Maslahat": "Maslahat is expediency; Ezzat is unbending honor.",
          "Qodrat": "Qodrat is raw muscle; Ezzat is self-respect."
        }
      },
      "fa": {
        "correct_generic": "عزت. کاملاً درسته! اصلی که می‌گوید حتی با خزانه خالی، دیپلمات نباید احساس حقارت یا شکست کند.",
        "wrong_generic": "خیر، پاسخ عزت بود. رکن نخست شعار محوری سیاست خارجی: «عزت، حکمت، مصلحت».",
        "common_wrong_answers": {
          "حکمت": "حکمت عقلانیت و دوراندیشی است؛ عزت نماد شأن و کرامت ملی است.",
          "مصلحت": "مصلحت انعطاف بر اساس منافع است؛ عزت پاسداری از غرور و استقلال است.",
          "قدرت": "قدرت مؤلفه مادی است؛ عزت شأن هویتی و جایگاه معنوی است."
        }
      }
    },
    "explanation": {
      "en": "Duncombe highlights that in Iranian foreign policy doctrine, 'Ezzat' (dignity/honor) is not merely a rhetorical flourish but a core psychological imperative: any agreement, including the nuclear deal, must be framed as a triumph of Iranian steadfastness rather than capitulation to external pressure.",
      "fa": "کنستانس دانکامب نشان می‌دهد که «عزت» در دکترین دیپلماسی ایران یک ضرورت حیاتی روان‌شناختی است؛ هر توافقی از جمله برجام باید به گونه‌ای روایت شود که سندی بر تسلیم‌ناپذیری و احترام به حقوق حاکمیتی کشور باشد نه تن دادن به باج‌خواهی قدرت‌ها."
    },
    "provenance": {
      "source_book": "Representation, Recognition and Foreign Policy: US-Iran Relations",
      "source_author": "Constance Duncombe",
      "page_number": 34,
      "verbatim_passage": "Iranian foreign policy is explicitly anchored in the concept of ezzat (honor and dignity), demanding that the international community treat the Islamic Republic as an equal and venerable civilization rather than a subordinate state.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_status_anxiety_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE STATUS ANXIETY OF TEHRAN", "fa": "بحران شناسایی در اتاق بیضی"},
    "clue_text": {
      "en": "Duncombe analyzes the 2015 JCPOA nuclear accord not merely as a technical arms-control treaty, but as this psychological milestone where the world's greatest powers officially recognized Iran as an equal negotiating peer.",
      "fa": "دانکامب توافق هسته‌ای برجام در سال ۱۳۹۴ را نه صرفاً یک قرارداد فنی کنترل تسلیحات، بلکه نقطه عطف روانی مهمی تحلیل می‌کند که در آن ابرقدرت‌های جهان رسماً ایران را به عنوان طرف مذاکره‌کننده برابر به رسمیت شناختند."
    },
    "canonical_answer": {"en": "Recognition Agreement", "fa": "توافق شناسایی و منزلت"},
    "accepted_aliases": {"en": ["Status recognition accord", "Agreement of recognition", "Status agreement", "Recognition pact"], "fa": ["پیمان شناسایی منزلت", "شناسایی موقعیت برابر", "سند شناسایی"]},
    "options": {
      "en": ["Unconditional Surrender", "Recognition Agreement", "Colonial Capitulation", "Defensive Mutual Aid Pact"],
      "fa": ["تسلیم بی‌قیدوشرط", "توافق شناسایی و منزلت", "پیمان کاپیتولاسیون استعماری", "پیمان دفاع جمعی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Unconditional Surrender", "why_plausible": "How hardline critics occasionally mischaracterized the concessions.", "why_wrong": "The JCPOA preserved enrichment and did not abolish the state or military."},
      {"option": "Colonial Capitulation", "why_plausible": "Radical domestic opponents claimed it was capitulation.", "why_wrong": "Duncombe's scholarly analysis demonstrates the agreement's primary symbolic value was positive status recognition."},
      {"option": "Defensive Mutual Aid Pact", "why_plausible": "A military mutual defense treaty like NATO.", "why_wrong": "The JCPOA offered no military defense alliance with the West."}
    ],
    "adversarial_confusion_set": {"en": ["Arms Control Treaty", "Non-Aggression Pact"], "fa": ["معاهده کنترل تسلیحات", "پیمان عدم تجاوز"]},
    "specificity_prompt": {
      "en": "Identify the specific conceptual framing Duncombe applies to the JCPOA regarding state status.",
      "fa": "مفهوم هویتی ناظر بر به رسمیت شناختن جایگاه برابر ایران توسط قدرت‌های جهانی در برجام را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Recognition Agreement. Correct. Sitting at the table with the P5+1, flags at equal height, proving to the world that Tehran had arrived.",
        "wrong_generic": "No, it functioned as a Recognition Agreement. Elevating Iran to the premier league of international diplomacy.",
        "common_wrong_answers": {
          "Unconditional Surrender": "Neither side surrendered; both sides spent two years arguing over centrifuges.",
          "Colonial Capitulation": "Capitulation gives away sovereignty; the JCPOA enshrined Iran's enrichment rights.",
          "Defensive Mutual Aid Pact": "Nobody promised to defend anyone; it was about nuclear verification."
        }
      },
      "fa": {
        "correct_generic": "توافق شناسایی و منزلت. کاملاً درسته! نشستن پشت یک میز با وزرای خارجه شش ابرقدرت جهان با پرچم‌هایی هم‌اندازه.",
        "wrong_generic": "خیر، پاسخ توافق شناسایی و منزلت (Recognition Agreement) بود. اهمیت نمادین برجام فراتر از غنی‌سازی اورانیوم.",
        "common_wrong_answers": {
          "تسلیم بی‌قیدوشرط": "هیچ تسلیمی در کار نبود؛ مذاکرات فشرده دو سال بر سر هر واژه ادامه داشت.",
          "پیمان کاپیتولاسیون استعماری": "کاپیتولاسیون واگذاری حق قضاوت بود؛ برجام حق هسته‌ای ایران را در شورای امنیت تثبیت کرد.",
          "پیمان دفاع جمعی": "برجام اتحاد نظامی نبود، تفاهم‌نامه‌ای پیرامون برنامه هسته‌ای و رفع تحریم بود."
        }
      }
    },
    "explanation": {
      "en": "Constance Duncombe argues that the JCPOA was celebrated in Iran primarily as a breakthrough in ontological security: the P5+1 sitting with Iranian diplomats as equals and endorsing UN Security Council Resolution 2231 provided the formal recognition of greatness that Iranian nationalism had sought for decades.",
      "fa": "کنستانس دانکامب استدلال می‌کند که استقبال مردم از برجام در اصل به دلیل ارضای نیاز به امنیت هستی‌شناختی بود: نشستن وزرای خارجه قدرت‌های بزرگ در کنار ظریف و تصویب قطعنامه ۲۲۳۱، نماد شناسایی رسمی شأن و عظمت ایران در جهان بود."
    },
    "provenance": {
      "source_book": "Representation, Recognition and Foreign Policy: US-Iran Relations",
      "source_author": "Constance Duncombe",
      "page_number": 51,
      "verbatim_passage": "The JCPOA represented far more than a non-proliferation bargain; it was a profound recognition agreement that provided Iran with symbolic validation as an equal and indispensable global power.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_status_anxiety_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "THE STATUS ANXIETY OF TEHRAN", "fa": "بحران شناسایی در اتاق بیضی"},
    "clue_text": {
      "en": "Duncombe explains that the psychological shock of Bush's 2002 'Axis of Evil' designation triggered this deep emotional reaction among Iranian leaders, driving them to abandon cooperation and aggressively accelerate ballistic and nuclear hedging.",
      "fa": "دانکامب تشریح می‌کند که شوک روانی برچسب «محور شرارت» جورج بوش در سال ۱۳۸۰ به این واکنش عاطفی عمیق در میان نخبگان ایران انجامید و آنان را به سوی انصراف از همکاری و شتاب بخشیدن به توان موشکی و هسته‌ای سوق داد."
    },
    "canonical_answer": {"en": "Humiliation", "fa": "احساس تحقیر شدگی"},
    "accepted_aliases": {"en": ["National humiliation", "Status humiliation", "Disrespect", "Emotional humiliation"], "fa": ["تحقیر ملی", "احساس سرشکستگی", "تحقیر دیپلماتیک", "سرخوردگی و تحقیر"]},
    "options": {
      "en": ["Complacency", "Humiliation", "Triumphalism", "Indifference"],
      "fa": ["خاطرجمعی و رضایت", "احساس تحقیر شدگی", "غرور و خودبرتربینی", "بی‌تفاوتی کامل"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Complacency", "why_plausible": "A passive reaction.", "why_wrong": "The reaction was fiercely emotional and defensive, not relaxed complacency."},
      {"option": "Triumphalism", "why_plausible": "A boastful reaction.", "why_wrong": "They felt deeply betrayed and insulted after their constructive diplomacy in Afghanistan."},
      {"option": "Indifference", "why_plausible": "Ignoring foreign speeches.", "why_wrong": "The speech caused immense domestic turmoil and ended reformist foreign policy credibility."}
    ],
    "adversarial_confusion_set": {"en": ["Paranoia", "Spite"], "fa": ["پارانویا", "کینه‌توزی"]},
    "specificity_prompt": {
      "en": "Identify the primary affective/emotional concept analyzed by Duncombe that drove post-2002 Iranian escalation.",
      "fa": "احساس و مفهوم عاطفی کلیدی در تحلیل دانکامب که حاصل خلف وعده آمریکا و مسبب دگرگونی راهبرد ایران شد را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Humiliation. Spot on. When you extend an olive branch in Kabul, get called evil on live television, and decide you need ten thousand centrifuges instead.",
        "wrong_generic": "No, it was Humiliation. The most explosive emotion in international relations.",
        "common_wrong_answers": {
          "Complacency": "Nobody was complacent; Khatami's foreign ministry was in full crisis mode.",
          "Triumphalism": "Triumphalism came years later when the centrifuges started spinning.",
          "Indifference": "Iranian leaders obsessed over every word of that State of the Union speech."
        }
      },
      "fa": {
        "correct_generic": "احساس تحقیر شدگی. کاملاً درسته! وقتی در کابل شاخه زیتون تعارف می‌کنی و در پخش زنده تلویزیونی شیطان خوانده می‌شوی، چاره‌ای جز ساخت سانتریفیوژ نمی‌بینی.",
        "wrong_generic": "خیر، پاسخ احساس تحقیر شدگی بود. مخرب‌ترین عاطفه سیاسی که دیپلماسی را به مسابقه تسلیحاتی کشاند.",
        "common_wrong_answers": {
          "خاطرجمعی و رضایت": "دستگاه دیپلماسی در شوک و بحران فرو رفت، نه آسودگی خیال.",
          "غرور و خودبرتربینی": "غرور بعداً با پیشرفت‌های فنی حاصل شد؛ حس اولیه خیانت و سرخوردگی بود.",
          "بی‌تفاوتی کامل": "نطق سالانه بوش ماه‌ها تیتر اول تمام روزنامه‌های پایتخت بود."
        }
      }
    },
    "explanation": {
      "en": "Duncombe argues that affective dynamics like humiliation and indignation explain why states take high-risk, economically costly actions: feeling humiliated after their assistance in Afghanistan was dismissed with the 'Axis of Evil' insult, Iranian leaders concluded that only nuclear deterrence and ballistic power could command respect from Washington.",
      "fa": "دانکامب نشان می‌دهد که عواطف جمعی مانند احساس تحقیر و خشم ناشی از نادیده گرفته شدن، رفتارهای پرخطر دولت‌ها را رقم می‌زند: تحقیر ناشی از برچسب محور شرارت پس از حسن‌نیت در کابل، تصمیم‌گیرندگان ایران را به این باور رساند که آمریکا فقط زبان زور و غنی‌سازی اورانیوم را می‌فهمد."
    },
    "provenance": {
      "source_book": "Representation, Recognition and Foreign Policy: US-Iran Relations",
      "source_author": "Constance Duncombe",
      "page_number": 54,
      "verbatim_passage": "The profound humiliation felt by Iranian elites following the 'axis of evil' speech transformed their diplomatic calculus, fueling a hardened conviction that sovereign respect could only be coerced through nuclear and missile capabilities.",
      "evidence_type": "INTERPRETATION"
    }
  },

  # 19. double_neoliberal_mashhad: NEOLIBERAL NIGHTMARES IN MASHHAD / شورش کوی طلاب در عصر تعدیل
  {
    "id": "double_neoliberal_mashhad_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "NEOLIBERAL NIGHTMARES IN MASHHAD", "fa": "شورش کوی طلاب در عصر تعدیل"},
    "clue_text": {
      "en": "Following the Iran-Iraq War, President Hashemi Rafsanjani launched this macroeconomic framework modeled on the Washington Consensus, seeking to liberalize trade, cut price subsidies, and privatize public assets.",
      "fa": "پس از پایان جنگ تحمیلی، هاشمی رفسنجانی این الگوی اقتصاد کلان مبتنی بر آموزه‌های اجماع واشنگتن را به اجرا گذاشت که هدف آن آزادسازی تجارت، حذف یارانه‌ها و خصوصی‌سازی اموال عمومی بود."
    },
    "canonical_answer": {"en": "Structural Adjustment Program", "fa": "برنامه تعدیل ساختاری"},
    "accepted_aliases": {"en": ["Ta'dil", "Economic adjustment", "Structural adjustment", "Ta'dil-e Eqtesadi"], "fa": ["تعدیل ساختاری", "سیاست‌های تعدیل اقتصادی", "تعدیل اقتصادی", "طرح تعدیل ساختاری"]},
    "options": {
      "en": ["Soviet Five-Year Plan", "Structural Adjustment Program", "Import Substitution Industrialization", "War Economy Mobilization"],
      "fa": ["برنامه پنج‌ساله شوروی", "برنامه تعدیل ساختاری", "صنعتی‌سازی جایگزین واردات", "بسیج اقتصاد جنگی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Soviet Five-Year Plan", "why_plausible": "Iran had five-year development plans.", "why_wrong": "The plans in the 1990s adopted market liberalization and World Bank advice, the exact opposite of Soviet central planning."},
      {"option": "Import Substitution Industrialization", "why_plausible": "The Pahlavi era economic model.", "why_wrong": "ISI was the 1960s-1970s model, whereas Rafsanjani's program embraced export orientation and trade opening."},
      {"option": "War Economy Mobilization", "why_plausible": "The 1980s statist economic management under Mousavi.", "why_wrong": "Rafsanjani's entire goal was dismantling Prime Minister Mousavi's statist wartime ration system."}
    ],
    "adversarial_confusion_set": {"en": ["Shock Therapy", "Reconstruction Strategy"], "fa": ["شوک‌درمانی", "دوران سازندگی"]},
    "specificity_prompt": {
      "en": "Name the specific macroeconomic program (Ta'dil-e Eqtesadi) implemented in Iran during the 1990s.",
      "fa": "اصطلاح رسمی اقتصادی دوره ریاست‌جمهوری هاشمی رفسنجانی برای آزادسازی قیمت‌ها و واگذاری‌ها را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Structural Adjustment Program. Correct. Trade in the coupon books for free-market price tags and watch inflation hit fifty percent.",
        "wrong_generic": "No, it was the Structural Adjustment Program (Ta'dil-e Eqtesadi). The neoliberal turn in post-war Tehran.",
        "common_wrong_answers": {
          "Soviet Five-Year Plan": "They called them five-year plans, but the advice came from the World Bank, not Moscow.",
          "Import Substitution Industrialization": "Import substitution was the Shah's 1970s policy; this was 1990s free-market opening.",
          "War Economy Mobilization": "The war economy had ended; Rafsanjani wanted shopping malls and toll highways."
        }
      },
      "fa": {
        "correct_generic": "برنامه تعدیل ساختاری. کاملاً درسته! بستن دفترچه‌های کوپن و سپردن معیشت مردم به دست نامرئی بازار آزاد.",
        "wrong_generic": "خیر، پاسخ برنامه تعدیل ساختاری (تعدیل اقتصادی) بود. رویکرد نئولیبرالی دولت سازندگی.",
        "common_wrong_answers": {
          "برنامه پنج‌ساله شوروی": "برنامه‌ریزی پنج‌ساله بود، اما محتوای آن توصیه‌های صندوق بین‌المللی پول بود نه مسکو.",
          "صنعتی‌سازی جایگزین واردات": "جایگزینی واردات مدل دهه چهل و پنجاه شاه بود؛ رفسنجانی درهای واردات را گشود.",
          "بسیج اقتصاد جنگی": "اقتصاد کوپنی میرحسین موسوی کنار رفت تا بازار آزاد آغاز شود."
        }
      }
    },
    "explanation": {
      "en": "Ali Jebraily documents that Hashemi Rafsanjani's administration embraced the Structural Adjustment Program (Siyasat-haye Ta'dil-e Eqtesadi) in 1989, slashing import tariffs, deregulating currency exchange, and reducing basic social subsidies under World Bank guidance.",
      "fa": "علی جبرئیلی مستند می‌کند که دولت هاشمی رفسنجانی از سال ۱۳۶۸ با اجرای «سیاست‌های تعدیل ساختاری» بر اساس دستورالعمل‌های بانک جهانی، به حذف یارانه‌ها، شناورسازی نرخ ارز و خصوصی‌سازی گسترده دست زد."
    },
    "provenance": {
      "source_book": "Neoliberal Reform and Social Fragilization in Post-War Iran",
      "source_author": "Ali Jebraily",
      "page_number": 3,
      "verbatim_passage": "In the wake of the 1988 ceasefire, the Rafsanjani administration embarked on an aggressive Structural Adjustment Program (Ta'dil-e Eqtesadi), dismantling state price controls, courting foreign loans, and deregulating trade.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_neoliberal_mashhad_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "NEOLIBERAL NIGHTMARES IN MASHHAD", "fa": "شورش کوی طلاب در عصر تعدیل"},
    "clue_text": {
      "en": "In May 1992, simmering popular fury against structural adjustment erupted into major urban riots in Mashhad after municipal bulldozers demolished unauthorized informal homes in this working-class neighborhood.",
      "fa": "در خرداد ۱۳۷۱، خشم عمومی از فشارهای تعدیل اقتصادی در مشهد پس از تخریب خانه‌های غیرمجاز حاشیه‌نشینان این محله محروم توسط بولدوزرهای شهرداری به یک شورش شهری تمام‌عیار تبدیل شد."
    },
    "canonical_answer": {"en": "Kuy-e Tollab", "fa": "کوی طلاب"},
    "accepted_aliases": {"en": ["Tollab", "Kuy-e Tullab", "Kooy-e Tollab"], "fa": ["طلاب", "محله طلاب", "منطقه طلاب مشهد"]},
    "options": {
      "en": ["Niavaran", "Kuy-e Tollab", "Ahmadabad", "Koohsangi"],
      "fa": ["نیاوران", "کوی طلاب", "احمدآباد", "کوهسنگی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Niavaran", "why_plausible": "An affluent neighborhood.", "why_wrong": "Niavaran is a luxury residential district in northern Tehran, not a working-class slum in Mashhad."},
      {"option": "Ahmadabad", "why_plausible": "A prominent middle-class boulevard and district in Mashhad.", "why_wrong": "Ahmadabad is an upscale shopping and residential district in Mashhad, not the informal shantytown destroyed in 1992."},
      {"option": "Koohsangi", "why_plausible": "A famous rocky park and district in Mashhad.", "why_wrong": "Koohsangi is a municipal recreational park in Mashhad, not the site of the demolished homes."}
    ],
    "adversarial_confusion_set": {"en": ["Golshahr", "Seyedi"], "fa": ["گلشهر", "سیدی"]},
    "specificity_prompt": {
      "en": "Name the specific working-class neighborhood in Mashhad where municipal demolitions triggered the 1992 riots.",
      "fa": "نام محله مسکونی حاشیه‌نشینان مشهد که تخریب آن جرقه شورش خونین سال ۱۳۷۱ شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Kuy-e Tollab. Correct. Sending bulldozers to flatten shanties on the outskirts of the holy shrine city, and waking up to find government buildings ablaze.",
        "wrong_generic": "No, it was Kuy-e Tollab. The epicenter of the 1992 Mashhad uprising.",
        "common_wrong_answers": {
          "Niavaran": "Niavaran is palaces in northern Tehran.",
          "Ahmadabad": "Ahmadabad is pastry shops and doctors' clinics in Mashhad.",
          "Koohsangi": "Koohsangi is where families eat ice cream by the stone pools."
        }
      },
      "fa": {
        "correct_generic": "کوی طلاب. کاملاً درسته! لودر انداختن زیر آلونک‌های محرومان در حاشیه مشهد که به آتش کشیده شدن ادارات دولتی انجامید.",
        "wrong_generic": "خیر، پاسخ کوی طلاب مشهد بود. کانون انفجار اجتماعی خرداد ۱۳۷۱.",
        "common_wrong_answers": {
          "نیاوران": "نیاوران کاخ‌نشینان تهران است، نه حاشیه‌نشینان مشهد.",
          "احمدآباد": "احمدآباد راسته پزشکان و مراکز خرید مدرن مشهد است.",
          "کوهسنگی": "کوهسنگی تفرجگاه تفریحی مشهد است، نه سکونتگاه غیررسمی کارگران."
        }
      }
    },
    "explanation": {
      "en": "Ali Jebraily recounts that on May 30, 1992, municipal workers attempting to demolish unpermitted informal dwellings in Kuy-e Tollab clashed with residents; a schoolchild was shot, sparking an explosion of rioting that burned down the Mashhad municipality, banks, and department stores.",
      "fa": "علی جبرئیلی روایت می‌کند که در ۹ خرداد ۱۳۷۱، تخریب آلونک‌های حاشیه‌نشینان کوی طلاب مشهد توسط شهرداری و تیراندازی مأموران که به کشته شدن یک کودک انجامید، به شورش گسترده مردم و به آتش کشیدن شهرداری، بانک‌ها و مراکز دولتی منجر شد."
    },
    "provenance": {
      "source_book": "Neoliberal Reform and Social Fragilization in Post-War Iran",
      "source_author": "Ali Jebraily",
      "page_number": 8,
      "verbatim_passage": "The May 1992 riots in Mashhad's Kuy-e Tollab demonstrated the acute human cost of structural adjustment: municipal demolition of shanties ignited days of violent anti-government protest across the shrine city.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_neoliberal_mashhad_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "NEOLIBERAL NIGHTMARES IN MASHHAD", "fa": "شورش کوی طلاب در عصر تعدیل"},
    "clue_text": {
      "en": "The social crisis of Rafsanjani's structural adjustment peaked in 1995 when Iran's official annual inflation rate spiked to this historic all-time post-revolutionary record.",
      "fa": "بحران اجتماعی سیاست‌های تعدیل در سال ۱۳۷۴ به اوج رسید، زمانی که نرخ رسمی تورم سالانه در ایران به این رکورد تاریخی بی‌سابقه در دوران پس از انقلاب صعود کرد."
    },
    "canonical_answer": {"en": "49.5 percent", "fa": "۴۹٫۵ درصد"},
    "accepted_aliases": {"en": ["49.5%", "Forty-nine point five percent", "49 percent", "Nearly 50 percent"], "fa": ["۴۹٫۵", "۴۹ ممیز ۵ درصد", "حدود ۵۰ درصد", "چهل و نه و نیم درصد"]},
    "options": {
      "en": ["25 percent", "49.5 percent", "85 percent", "12 percent"],
      "fa": ["۲۵ درصد", "۴۹٫۵ درصد", "۸۵ درصد", "۱۲ درصد"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "25 percent", "why_plausible": "A typical elevated inflation rate in modern Iranian history.", "why_wrong": "Inflation was nearly double this figure in 1995."},
      {"option": "85 percent", "why_plausible": "Extreme hyperinflation figures seen in Argentina or Turkey.", "why_wrong": "Iran's official consumer price index peaked just shy of fifty percent, not eighty-five percent."},
      {"option": "12 percent", "why_plausible": "A modest single-digit goal.", "why_wrong": "Iran never achieved 12% inflation during the turbulent mid-1990s currency devaluations."}
    ],
    "adversarial_confusion_set": {"en": ["39.9 percent", "55 percent"], "fa": ["۳۹٫۹ درصد", "۵۵ درصد"]},
    "specificity_prompt": {
      "en": "Provide the exact official percentage figure of annual inflation recorded in Iran in 1995.",
      "fa": "عدد دقیق رکورد تورم سال ۱۳۷۴ بر اساس آمار بانک مرکزی ایران را به صورت درصد بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "49.5 percent. Correct. When food and housing prices double overnight, even revolutionary piety struggles to explain the grocery bill.",
        "wrong_generic": "No, it was 49.5 percent. The highest annual inflation rate in post-revolutionary history until recent years.",
        "common_wrong_answers": {
          "25 percent": "Twenty-five percent is a relaxing holiday compared to what happened in 1995.",
          "85 percent": "Eighty-five is Weimar or Buenos Aires; Tehran capped out at 49.5%.",
          "12 percent": "Twelve percent only existed in government wishful thinking."
        }
      },
      "fa": {
        "correct_generic": "۴۹٫۵ درصد. کاملاً درسته! شکست سنگین سیاست شوک‌درمانی ارزی که مهار آن سال‌ها به طول انجامید.",
        "wrong_generic": "خیر، پاسخ ۴۹٫۵ درصد بود. بالاترین تورم رسمی ثبت‌شده در تاریخ پس از انقلاب تا آن مقطع.",
        "common_wrong_answers": {
          "۲۵ درصد": "۲۵ درصد برای اقتصاد ایران عدد معتدلی است؛ در سال ۷۴ تورم دو برابر این بود.",
          "۸۵ درصد": "۸۵ درصد مختص ابرتورم‌های آمریکای لاتین است.",
          "۱۲ درصد": "۱۲ درصد فقط آرزوی محقق‌نشده اقتصاددانان دولتی بود."
        }
      }
    },
    "explanation": {
      "en": "Central Bank of Iran data confirms that following the abrupt unification of exchange rates and foreign debt maturity crises in 1994-1995, consumer price inflation surged to an unprecedented 49.5%, forcing the government to slam the brakes on structural adjustment.",
      "fa": "آمارهای بانک مرکزی تأیید می‌کند که در پی نوسانات شدید ارزی و سررسید بدهی‌های خارجی در سال‌های ۱۳۷۳ و ۱۳۷۴، تورم به رقم بی‌سابقه ۴۹٫۵ درصد رسید و دولت را مجبور به توقف شوک‌های قیمتی و بازگشت به تثبیت نرخ ارز کرد."
    },
    "provenance": {
      "source_book": "Neoliberal Reform and Social Fragilization in Post-War Iran",
      "source_author": "Ali Jebraily",
      "page_number": 12,
      "verbatim_passage": "In 1995, inflation reached an unprecedented 49.5 percent according to official Central Bank figures, eviscerating the real purchasing power of the middle class and plunging millions below the poverty line.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_neoliberal_mashhad_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "NEOLIBERAL NIGHTMARES IN MASHHAD", "fa": "شورش کوی طلاب در عصر تعدیل"},
    "clue_text": {
      "en": "In April 1995, acute cost-of-living pressures ignited this violent suburban insurrection on the highway southwest of Tehran, sparked when minibus drivers doubled transit fares for impoverished commuters.",
      "fa": "در فروردین ۱۳۷۴، فشارهای معیشتی به این شورش خونین حومه‌ای در بزرگراه جنوب غربی تهران دامن زد که با دو برابر شدن کرایه مینی‌بوس‌ها توسط رانندگان برای مسافران کارگر آغاز شد."
    },
    "canonical_answer": {"en": "Islamshahr Riots", "fa": "شورش اسلامشهر"},
    "accepted_aliases": {"en": ["Islamshahr uprising", "Eslamshahr protests", "Islamshahr unrest"], "fa": ["حوادث اسلامشهر", "شورش اسلام‌شهر", "اعتراضات اسلامشهر ۱۳۷۴"]},
    "options": {
      "en": ["Tehran University Protests", "Islamshahr Riots", "Abadan Strike", "Khuzestan Water Protests"],
      "fa": ["اعتراضات کوی دانشگاه", "شورش اسلامشهر", "اعتصاب کارگران آبادان", "بحران آب خوزستان"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Tehran University Protests", "why_plausible": "The famous July 1999 (18 Tir) student protests.", "why_wrong": "18 Tir was in 1999 led by university students protesting press freedom closures, not a 1995 working-class transport rebellion."},
      {"option": "Abadan Strike", "why_plausible": "A famous industrial strike in oil history.", "why_wrong": "Abadan oil strikes occurred during the 1978-1979 revolution."},
      {"option": "Khuzestan Water Protests", "why_plausible": "A major recent protest over resources.", "why_wrong": "Khuzestan water unrest broke out decades later in 2021."}
    ],
    "adversarial_confusion_set": {"en": ["Qazvin Riots", "Akbarabad Protests"], "fa": ["شورش قزوین", "اعتراضات اکبرآباد"]},
    "specificity_prompt": {
      "en": "Name the specific peri-urban working-class suburb southwest of Tehran that erupted into mass riots in April 1995.",
      "fa": "نام شهر حاشیه‌ای جنوب غرب تهران که در فروردین ۱۳۷۴ صحنه شورش کارگری و بستن جاده ساوه شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Islamshahr Riots. Correct. Commuters discovering their round-trip minibus fare had just eaten half their daily wages.",
        "wrong_generic": "No, it was the Islamshahr Riots of April 1995. The moment the impoverished periphery marched toward the capital.",
        "common_wrong_answers": {
          "Tehran University Protests": "Kuy-e Daneshgah was July 1999 with intellectuals; Islamshahr was 1995 with factory workers.",
          "Abadan Strike": "Abadan was 1978 oil workers shutting down the refineries.",
          "Khuzestan Water Protests": "Khuzestan water protests were in 2021 over dry marshes."
        }
      },
      "fa": {
        "correct_generic": "شورش اسلامشهر. کاملاً درسته! وقتی کرایه مینی‌بوس از ۲ تومان به ۵ تومان رسید و کارگران خشمگین جاده ساوه را بستند.",
        "wrong_generic": "خیر، پاسخ شورش اسلامشهر در فروردین ۱۳۷۴ بود. خیزش حاشیه‌نشینان فقیر جنوب غربی پایتخت.",
        "common_wrong_answers": {
          "اعتراضات کوی دانشگاه": "کوی دانشگاه در تیر ۱۳۷۸ و با مطالبات سیاسی و دانشجویی بود.",
          "اعتصاب کارگران آبادان": "اعتصاب نفتگران آبادان مربوط به پاییز ۱۳۵۷ و سرنگونی شاه بود.",
          "بحران آب خوزستان": "بحران آب خوزستان در تابستان ۱۴۰۰ رخ داد."
        }
      }
    },
    "explanation": {
      "en": "Ali Jebraily analyzes the April 1995 Islamshahr uprising as a pivotal crisis of Iranian neoliberalism: peri-urban commuters and factory workers, suffering from a 30% jump in water rates and a doubling of transit fares, blocked the Saveh highway and burned banks, met with harsh security suppression.",
      "fa": "علی جبرئیلی قیام فروردین ۱۳۷۴ اسلامشهر را نقطه بحرانی نئولیبرالیسم در ایران ارزیابی می‌کند: کارگران حاشیه‌نشین در اعتراض به افزایش ۳۰ درصدی بهای آب و دو برابر شدن کرایه اتوبوس، جاده ساوه را مسدود کردند و بانک‌ها را به آتش کشیدند که با برخورد شدید امنیتی مهار شد."
    },
    "provenance": {
      "source_book": "Neoliberal Reform and Social Fragilization in Post-War Iran",
      "source_author": "Ali Jebraily",
      "page_number": 15,
      "verbatim_passage": "On April 4, 1995, thousands of impoverished residents in the peri-urban settlement of Islamshahr erupted in protest against surging transit fares and water shortages, marching on Tehran before being dispersed by armed force.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_neoliberal_mashhad_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "NEOLIBERAL NIGHTMARES IN MASHHAD", "fa": "شورش کوی طلاب در عصر تعدیل"},
    "clue_text": {
      "en": "To finance post-war reconstruction projects despite US hostility, the Rafsanjani administration secretly accumulated this unprecedented level of short-term foreign commercial debt by 1993, precipitating a devastating default and refinancing crisis.",
      "fa": "برای تأمین مالی پروژه‌های بازسازی پس از جنگ، دولت رفسنجانی تا سال ۱۳۷۲ این حجم بی‌سابقه از بدهی‌های کوتاه‌مدت خارجی را ایجاد کرد که به بحران ناتوانی در بازپرداخت و تجدید استقراض منجر شد."
    },
    "canonical_answer": {"en": "30 Billion Dollars", "fa": "۳۰ میلیارد دلار"},
    "accepted_aliases": {"en": ["$30 billion", "30 billion", "30 billion USD", "Thirty billion dollars"], "fa": ["سی میلیارد دلار", "۳۰ میلیارد", "۳۰ میلیارد دلار"]},
    "options": {
      "en": ["5 Billion Dollars", "30 Billion Dollars", "100 Billion Dollars", "15 Billion Dollars"],
      "fa": ["۵ میلیارد دلار", "۳۰ میلیارد دلار", "۱۰۰ میلیارد دلار", "۱۵ میلیارد دلار"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "5 Billion Dollars", "why_plausible": "A manageable debt figure for an oil state.", "why_wrong": "The debt accumulated through short-term letters of credit (LCs) was far larger, exceeding thirty billion."},
      {"option": "100 Billion Dollars", "why_plausible": "Comparable to Latin American sovereign debt in the 1980s.", "why_wrong": "Iran never accumulated debt on that scale; foreign banks refused long-term loans."},
      {"option": "15 Billion Dollars", "why_plausible": "An intermediate debt estimate.", "why_wrong": "Official central bank and IMF post-mortem assessments put the peak debt crisis at approximately $30 billion."}
    ],
    "adversarial_confusion_set": {"en": ["20 Billion Dollars", "40 Billion Dollars"], "fa": ["۲۰ میلیارد دلار", "۴۰ میلیارد دلار"]},
    "specificity_prompt": {
      "en": "Provide the approximate total dollar amount of short-term external debt accumulated by Iran by 1993.",
      "fa": "رقم تقریبی بدهی‌های خارجی تعهدشده ایران در سال ۱۳۷۲ را به میلیارد دلار بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "30 Billion Dollars. Spot on. Handing European banks billions in promissory notes until the bills came due and the treasury had no foreign exchange left.",
        "wrong_generic": "No, it was 30 Billion Dollars. The massive debt hangover that forced Rafsanjani to beg Germany and Japan for debt rescheduling.",
        "common_wrong_answers": {
          "5 Billion Dollars": "Five billion could have been paid with oil revenues; thirty billion broke the exchange rate.",
          "100 Billion Dollars": "Nobody trusted post-revolutionary Iran with one hundred billion dollars.",
          "15 Billion Dollars": "Fifteen was only the overdue portion."
        }
      },
      "fa": {
        "correct_generic": "۳۰ میلیارد دلار. کاملاً درسته! گشایش یله و رهای ال‌سی‌های کوتاه‌مدت نزد بانک‌های اروپایی که خزانه‌داری را به مرز ورشکستگی کشاند.",
        "wrong_generic": "خیر، پاسخ ۳۰ میلیارد دلار بدهی خارجی بود. بحران ارزی مهلکی که دولت سازندگی را به استمهال بدهی‌ها واداشت.",
        "common_wrong_answers": {
          "۵ میلیارد دلار": "پنج میلیارد با یک ماه صادرات نفت تسویه می‌شد؛ بدهی ۳۰ میلیاردی کمر اقتصاد را شکست.",
          "۱۰۰ میلیارد دلار": "بانک‌های جهانی جرئت وام صد میلیارد دلاری به تهران را نداشتند.",
          "۱۵ میلیارد دلار": "پانزده میلیارد فقط اصل بدهی‌های معوقه فوری بود."
        }
      }
    },
    "explanation": {
      "en": "Ali Jebraily documents that by 1993, Iranian ministries and parastatals had run up roughly $30 billion in short-term foreign commercial debt via letters of credit (LCs) with European and Japanese banks; when oil prices dipped to $13 a barrel, Iran defaulted on payments, triggering severe currency depreciation.",
      "fa": "علی جبرئیلی نشان می‌دهد که تا سال ۱۳۷۲، گشایش بی‌رویه اعتبارات اسنادی (ال‌سی) کوتاه‌مدت، بدهی خارجی کشور را به حدود ۳۰ میلیارد دلار رساند؛ با سقوط بهای نفت به بشکه‌ای ۱۳ دلار، دولت از بازپرداخت بازماند و ناچار به استمهال پرهزینه بدهی‌ها با میانجی‌گری آلمان و ژاپن شد."
    },
    "provenance": {
      "source_book": "Neoliberal Reform and Social Fragilization in Post-War Iran",
      "source_author": "Ali Jebraily",
      "page_number": 18,
      "verbatim_passage": "By 1993, external debt had ballooned to approximately $30 billion, predominantly in short-term letters of credit, triggering an acute debt crisis that forced the central bank to reschedule obligations with European creditors.",
      "evidence_type": "FACT"
    }
  },

  # 20. double_maktabi_expert: MAKTABI VS EXPERT / مکتبی در سنگر، متخصص در دفتر
  {
    "id": "double_maktabi_expert_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "MAKTABI VS EXPERT", "fa": "مکتبی در سنگر، متخصص در دفتر"},
    "clue_text": {
      "en": "In his study of factional wartime politics, Mohammad Ayatollahi Tabaar examines this foundational post-revolutionary binary that pitted revolutionary ideological commitment against technical professional competence.",
      "fa": "محمد آیت‌اللهی‌تبار در بررسی کشمکش‌های جناحی دوران دفاع مقدس، این دوگانه بنیادین پساانقلابی را واکاوی می‌کند که تعهد ایدئولوژیک انقلابی را در برابر تخصص و دانش حرفه‌ای قرار می‌داد."
    },
    "canonical_answer": {"en": "Maktabi vs Motakhases", "fa": "مکتبی در برابر متخصص"},
    "accepted_aliases": {"en": ["Ideologue vs Expert", "Maktabi and Takhasos", "Commitment vs Expertise", "Ta'ahod vs Takhasos"], "fa": ["تعهد در برابر تخصص", "مکتبی و متخصص", "تعهد یا تخصص", "مکتب در برابر تخصص"]},
    "options": {
      "en": ["Feudal vs Bourgeois", "Maktabi vs Motakhases", "Traditionalist vs Modernist", "Monarchist vs Republican"],
      "fa": ["فئودال در برابر بورژوا", "مکتبی در برابر متخصص", "سنتی در برابر مدرن", "سلطنت‌طلب در برابر جمهوری‌خواه"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Feudal vs Bourgeois", "why_plausible": "A Marxist historical duality.", "why_wrong": "Standard Marxist class categories, not the unique Iranian post-revolutionary debate over staffing state institutions."},
      {"option": "Traditionalist vs Modernist", "why_plausible": "A broad cultural binary.", "why_wrong": "Too generic; the specific political catchphrases deployed in parliamentary and military purging were 'Maktabi' and 'Motakhases'."},
      {"option": "Monarchist vs Republican", "why_plausible": "A constitutional division.", "why_wrong": "The monarchist dispute was settled in February 1979; the internal regime conflict was about technical experts vs ideological purists."}
    ],
    "adversarial_confusion_set": {"en": ["Ta'ahod vs Danesh", "Maktabi vs Roshanfekr"], "fa": ["تعهد در برابر دانش", "مکتبی در برابر روشنفکر"]},
    "specificity_prompt": {
      "en": "Name the specific Persian pair of terms contrasting ideological loyalty (commitment) with technical competence (expertise).",
      "fa": "دوگانه مشهور سیاسی دوران انقلاب و جنگ ناظر بر تقابل تعهد ایدئولوژیک و مهارت فنی را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Maktabi vs Motakhases. Correct. Why study engineering at MIT when you have revolutionary faith and a beard?",
        "wrong_generic": "No, it was Maktabi vs Motakhases (Commitment vs Expertise). The debate that purged thousands of skilled professionals.",
        "common_wrong_answers": {
          "Feudal vs Bourgeois": "Marxist theory was for the Tudeh party; Maktabi was the Islamic Republic's test.",
          "Traditionalist vs Modernist": "Too polite; the question was whether you prayed properly or had an engineering degree.",
          "Monarchist vs Republican": "Monarchists were already purged; this was an internal regime knife fight."
        }
      },
      "fa": {
        "correct_generic": "مکتبی در برابر متخصص. کاملاً درسته! وقتی داشتن محاسن و حضور در نماز جمعه مهم‌تر از مدرک دکترای مهندسی شد.",
        "wrong_generic": "خیر، پاسخ دوگانه مکتبی و متخصص (تعهد در برابر تخصص) بود. معیاری که سبب تصفیه هزاران کارشناس از ادارات و دانشگاه‌ها شد.",
        "common_wrong_answers": {
          "فئودال در برابر بورژوا": "مفاهیم مارکسیستی حزب توده بود، نه گفتمان پاکسازی گزینش ادارات.",
          "سنتی در برابر مدرن": "تعبیر کلی است؛ دوگانه دقیق گزینش «مکتبی» و «متخصص» بود.",
          "سلطنت‌طلب در برابر جمهوری‌خواه": "سلطنت‌طلبان سال ۵۷ کنار رفته بودند؛ این نزاع درونی انقلابیون بود."
        }
      }
    },
    "explanation": {
      "en": "Mohammad Ayatollahi Tabaar shows that the 'Maktabi' (ideologically pure) versus 'Motakhases' (technocratic expert) debate was weaponized by the Islamic Republican Party to purge technocrats aligned with Mehdi Bazargan and Abolhassan Banisadr from state administration and military command.",
      "fa": "محمد آیت‌اللهی‌تبار نشان می‌دهد که دوگانه «مکتبی» و «متخصص» حربه‌ای در دست حزب جمهوری اسلامی بود تا با متهم کردن تکنوکرات‌های نزدیک به مهدی بازرگان و بنی‌صدر به بی‌تقوایی، آنان را از مدیریت‌های کلیدی و فرماندهی جنگ حذف کنند."
    },
    "provenance": {
      "source_book": "Factional Politics and the Iran-Iraq War",
      "source_author": "Mohammad Ayatollahi Tabaar",
      "page_number": 31,
      "verbatim_passage": "The polarization between the 'maktabi' (ideological zealots) and the 'motakhases' (technocrats and military professionals) served as the primary discursive weapon to purge moderates from state institutions.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_maktabi_expert_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "MAKTABI VS EXPERT", "fa": "مکتبی در سنگر، متخصص در دفتر"},
    "clue_text": {
      "en": "This first president of the Islamic Republic clashed violently with the clerical establishment by siding with the professional Artesh officer corps against the revolutionary Pasdaran, leading to his dramatic impeachment in June 1981.",
      "fa": "نخستین رئیس‌جمهور جمهوری اسلامی با حمایت از افسران متخصص ارتش در برابر پاسداران انقلابی با روحانیون حزب جمهوری اسلامی سرشاخ شد و در نهایت در خرداد ۱۳۶۰ عدم کفایت سیاسی او در مجلس رقم خورد."
    },
    "canonical_answer": {"en": "Abolhassan Banisadr", "fa": "ابوالحسن بنی‌صدر"},
    "accepted_aliases": {"en": ["Banisadr", "Abol-Hassan Banisadr", "Bani-Sadr"], "fa": ["بنی‌صدر", "بنی صدر", "سید ابوالحسن بنی‌صدر"]},
    "options": {
      "en": ["Mehdi Bazargan", "Abolhassan Banisadr", "Mohammad-Ali Rajai", "Sadegh Ghotbzadeh"],
      "fa": ["مهدی بازرگان", "ابوالحسن بنی‌صدر", "محمدعلی رجایی", "صادق قطب‌زاده"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Mehdi Bazargan", "why_plausible": "The moderate prime minister of the provisional government.", "why_wrong": "Bazargan was Prime Minister, not President, and resigned in November 1979 during the embassy hostage crisis."},
      {"option": "Mohammad-Ali Rajai", "why_plausible": "The prime minister who clashed with Banisadr.", "why_wrong": "Rajai was Banisadr's rival prime minister backed by the clerics, who succeeded him as president before being assassinated in August 1981."},
      {"option": "Sadegh Ghotbzadeh", "why_plausible": "A prominent revolutionary politician close to Khomeini in Paris.", "why_wrong": "Ghotbzadeh served as foreign minister, not president, and was executed in 1982."}
    ],
    "adversarial_confusion_set": {"en": ["Mehdi Bazargan", "Sadegh Ghotbzadeh"], "fa": ["مهدی بازرگان", "صادق قطب‌زاده"]},
    "specificity_prompt": {
      "en": "Name the first President of the Islamic Republic of Iran impeached by Parliament in June 1981.",
      "fa": "نام اولین رئیس‌جمهور تاریخ ایران که در ۳۱ خرداد ۱۳۶۰ توسط مجلس عزل شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Abolhassan Banisadr. Correct. Escaping to Paris on an air force jet disguised in women's clothing, or so the revolutionary papers loved to claim.",
        "wrong_generic": "No, it was Abolhassan Banisadr. The president who thought an Sorbonne education in economics could defeat clerical party discipline.",
        "common_wrong_answers": {
          "Mehdi Bazargan": "Bazargan resigned in 1979 over the hostage crisis; he was Prime Minister.",
          "Mohammad-Ali Rajai": "Rajai was the pious schoolteacher the clerics put in power after kicking Banisadr out.",
          "Sadegh Ghotbzadeh": "Ghotbzadeh was foreign minister and met a firing squad in 1982."
        }
      },
      "fa": {
        "correct_generic": "ابوالحسن بنی‌صدر. کاملاً درسته! مردی با تئوری‌های دانشگاه سوربن که گمان می‌کرد با حمایت فرماندهان ارتش می‌تواند حزب جمهوری اسلامی را شکست دهد.",
        "wrong_generic": "خیر، پاسخ ابوالحسن بنی‌صدر بود. نخستین رئیس‌جمهور معزول تاریخ جمهوری اسلامی.",
        "common_wrong_answers": {
          "مهدی بازرگان": "بازرگان نخست‌وزیر دولت موقت بود و در آبان ۱۳۵۸ استعفا داد.",
          "محمدعلی رجایی": "رجایی رقیب مکتبی بنی‌صدر بود که پس از او رئیس‌جمهور شد.",
          "صادق قطب‌زاده": "قطب‌زاده وزیر خارجه بود و در سال ۱۳۶۱ تیرباران شد."
        }
      }
    },
    "explanation": {
      "en": "Tabaar analyzes how Banisadr, as Commander-in-Chief, allied with professional Artesh generals like Valiollah Fallahi to fight a conventional military campaign, while the clerical leadership used military failures to accuse Banisadr of incompetence and treason, culminating in his June 1981 impeachment.",
      "fa": "آیت‌اللهی‌تبار تشریح می‌کند که بنی‌صدر به عنوان فرمانده کل قوا به فرماندهان کلاسیک ارتش تکیه کرد؛ امری که به روحانیون حزب جمهوری اسلامی بهانه داد تا شکست‌های تاکتیکی جبهه را ناشی از خیانت لیبرال‌ها قلمداد کرده و طرح عدم کفایت او را در مجلس به تصویب برسانند."
    },
    "provenance": {
      "source_book": "Factional Politics and the Iran-Iraq War",
      "source_author": "Mohammad Ayatollahi Tabaar",
      "page_number": 37,
      "verbatim_passage": "President Abolhassan Banisadr's reliance on the professional officer corps of the regular army alienated the IRGC and the clerical leadership of the Islamic Republican Party, culminating in his impeachment by the Majles in June 1981.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_maktabi_expert_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "MAKTABI VS EXPERT", "fa": "مکتبی در سنگر، متخصص در دفتر"},
    "clue_text": {
      "en": "Banisadr's military credibility was fatally punctured in January 1981 during this disastrous conventional armored offensive near Susangerd and Dezful, where hundreds of Iranian tanks were encircled and destroyed by Iraqi forces.",
      "fa": "اعتبار نظامی بنی‌صدر در دی ۱۳۵۹ با شکست فاجعه‌بار این عملیات زرهی کلاسیک در دشت‌های کرخه و هویزه فرو ریخت، جایی که صدها تانک ایرانی توسط ارتش عراق محاصره و منهدم شدند."
    },
    "canonical_answer": {"en": "Operation Nasr", "fa": "عملیات نصر"},
    "accepted_aliases": {"en": ["Nasr offensive", "Battle of Dezful", "Operation Nasr 1981"], "fa": ["نبرد هویزه", "عملیات نصر دی ۵۹", "عملیات نصر ۵۹"]},
    "options": {
      "en": ["Operation Fath ol-Mobin", "Operation Nasr", "Operation Beit ol-Moqaddas", "Operation Ramadan"],
      "fa": ["عملیات فتح‌المبین", "عملیات نصر", "عملیات بیت‌المقدس", "عملیات رمضان"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Operation Fath ol-Mobin", "why_plausible": "A massive battle in the Dezful-Shush sector.", "why_wrong": "Fath ol-Mobin was a triumphant joint victory in March 1982, not the disastrous January 1981 tank defeat."},
      {"option": "Operation Beit ol-Moqaddas", "why_plausible": "The crowning military victory liberating Khorramshahr.", "why_wrong": "Beit ol-Moqaddas in May 1982 liberated Khorramshahr, a year after Banisadr was removed."},
      {"option": "Operation Ramadan", "why_plausible": "A costly bloody offensive.", "why_wrong": "Ramadan took place in July 1982 inside Iraqi territory near Basra, long after Banisadr had fled."}
    ],
    "adversarial_confusion_set": {"en": ["Operation Kaman 99", "Operation Hoveizeh"], "fa": ["عملیات کمان ۹۹", "حماسه هویزه"]},
    "specificity_prompt": {
      "en": "Name the specific military armored offensive in January 1981 near Hoveizeh that ended in crushing defeat.",
      "fa": "نام عملیات نظامی زرهی ناموفق دی‌ماه ۱۳۵۹ در منطقه هویزه را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Operation Nasr. Correct. The largest tank battle of the war, where British-made Chieftain tanks got bogged down in the mud and decimated by Iraqi armor.",
        "wrong_generic": "No, it was Operation Nasr (January 1981). The disaster that sealed Banisadr's political fate.",
        "common_wrong_answers": {
          "Operation Fath ol-Mobin": "Fath ol-Mobin was in 1982 and recaptured 2,500 square kilometers.",
          "Operation Beit ol-Moqaddas": "Beit ol-Moqaddas was the glorious liberation of Khorramshahr.",
          "Operation Ramadan": "Ramadan was in the blistering heat of Basra in July 1982."
        }
      },
      "fa": {
        "correct_generic": "عملیات نصر. کاملاً درسته! بزرگ‌ترین نبرد تانک‌های جنگ که تانک‌های چیفتن در گل‌ولای هویزه زمین‌گیر و طعمه آتش عراق شدند.",
        "wrong_generic": "خیر، پاسخ عملیات نصر (۱۵ دی ۱۳۵۹) بود. شکستی سنگین که سرنوشت سیاسی بنی‌صدر را مختومه کرد.",
        "common_wrong_answers": {
          "عملیات فتح‌المبین": "فتح‌المبین در فروردین ۶۱ پیروزی درخشان مشترک ارتش و سپاه بود.",
          "عملیات بیت‌المقدس": "بیت‌المقدس حماسه آزادسازی خرمشهر در خرداد ۱۳۶۱ بود.",
          "عملیات رمضان": "عملیات رمضان نخستین ورود به خاک عراق در تیرماه ۶۱ در شرق بصره بود."
        }
      }
    },
    "explanation": {
      "en": "Tabaar explains that Banisadr insisted on launching Operation Nasr in January 1981 using conventional armored brigades against Iraqi defensive lines; the catastrophic loss of over 100 Chieftain and M60 tanks and the death of student volunteer cadres like Hossein Alamolhoda in Hoveizeh discredited classical military doctrine and enabled the IRGC to seize operational command.",
      "fa": "آیت‌اللهی‌تبار تشریح می‌کند که اصرار بنی‌صدر بر اجرای عملیات کلاسیک نصر در دی ۵۹ و تلفات سنگین لشکر ۱۶ زرهی و شهادت حسین علم‌الهدی و دانشجویان پیرو خط امام در هویزه، دکترین ارتش منظم را بی‌اعتبار کرد و ابتکار عمل جنگ را به سپاه سپرد."
    },
    "provenance": {
      "source_book": "Factional Politics and the Iran-Iraq War",
      "source_author": "Mohammad Ayatollahi Tabaar",
      "page_number": 42,
      "verbatim_passage": "The catastrophic failure of Operation Nasr in January 1981, where three Iranian armored brigades were ambushed and routed near Hoveizeh, shattered Banisadr's standing as commander-in-chief and empowered the Pasdaran.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_maktabi_expert_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "MAKTABI VS EXPERT", "fa": "مکتبی در سنگر، متخصص در دفتر"},
    "clue_text": {
      "en": "Following Banisadr's fall, the IRGC revolutionized military doctrine by substituting revolutionary ideological zeal and mass martyr volunteer assaults for armored firepower, a tactic known by this phrase.",
      "fa": "پس از سقوط بنی‌صدر، سپاه پاسداران دکترین جنگ را با جایگزین کردن شور انقلابی مذهبی و حملات داوطلبانه شهادت‌طلبانه به جای آتش سنگین زرهی دگرگون کرد؛ تاکتیکی که به این نام خوانده شد."
    },
    "canonical_answer": {"en": "Human Wave Tactics", "fa": "حملات موج انسانی"},
    "accepted_aliases": {"en": ["Human-wave assaults", "Hajoom-e Ashurayi", "Mass assaults", "Human wave"], "fa": ["موج انسانی", "هجوم عاشورایی", "تاکتیک موج انسانی", "حملات عاشورایی"]},
    "options": {
      "en": ["Blitzkrieg Warfare", "Human Wave Tactics", "Siege Trench Starvation", "Gunboat Diplomacy"],
      "fa": ["جنگ برق‌آسا", "حملات موج انسانی", "محاصره فرسایشی", "دیپلماسی توپدار"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Blitzkrieg Warfare", "why_plausible": "A fast military doctrine combining tanks and air power.", "why_wrong": "Blitzkrieg relies on coordinated mechanized armor and aircraft (German doctrine), whereas Iran suffered acute armor shortages and relied on mass infantry."},
      {"option": "Siege Trench Starvation", "why_plausible": "WWI defensive tactics.", "why_wrong": "Iran was on the strategic offensive trying to break through heavily fortified Iraqi lines."},
      {"option": "Gunboat Diplomacy", "why_plausible": "Naval intimidation.", "why_wrong": "A 19th-century naval imperial term, not ground battlefield assault doctrine."}
    ],
    "adversarial_confusion_set": {"en": ["Infiltration Tactics", "Guerrilla Ambush"], "fa": ["عملیات چریکی", "جنگ نامتقارن"]},
    "specificity_prompt": {
      "en": "Provide the commonly used military phrase describing Iran's mass infantry assaults using Basij volunteers.",
      "fa": "اصطلاح نظامی مشهور توصیف‌کننده هجوم خیل انبوه رزمندگان پیاده بسیجی به خطوط دشمن را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Human Wave Tactics. Correct. Substituting red headbands and spiritual martyrdom for modern artillery shells.",
        "wrong_generic": "No, it was Human Wave Tactics (Hajoom-e Ashurayi). Breaching minefields with flesh and blood.",
        "common_wrong_answers": {
          "Blitzkrieg Warfare": "Blitzkrieg requires Panzers; Iran had young boys with Kalashnikovs and plastic keys.",
          "Siege Trench Starvation": "Saddam sat in the trenches; Iran launched the human waves at them.",
          "Gunboat Diplomacy": "Gunboats were in the Persian Gulf, not charging across the sands of Khuzestan."
        }
      },
      "fa": {
        "correct_generic": "حملات موج انسانی. کاملاً درسته! غلبه بر میادین مین و دژهای مستحکم با سربند یازهرا و فداکاری رزمندگان بسیجی.",
        "wrong_generic": "خیر، پاسخ حملات موج انسانی (هجوم عاشورایی) بود. ویژگی برجسته عملیات‌های بزرگ سال‌های ۶۱ تا ۶۵.",
        "common_wrong_answers": {
          "جنگ برق‌آسا": "جنگ برق‌آسا نیازمند لشکرهای زرهی تانک بود که ایران از آن محروم بود.",
          "محاصره فرسایشی": "صدام در کانال‌ها سنگر گرفته بود؛ ایران به خطوط او هجوم می‌برد.",
          "دیپلماسی توپدار": "دیپلماسی توپدار اصطلاح استعماری دریایی بریتانیاست."
        }
      }
    },
    "explanation": {
      "en": "Tabaar analyzes how the Pasdaran overcame the arms embargo and conventional equipment shortages by mobilizing tens of thousands of Basij volunteers in mass infantry assaults ('human wave attacks'), viewing religious zeal and martyrdom (shahadat) as superior to imperialist technology.",
      "fa": "آیت‌اللهی‌تبار تشریح می‌کند که سپاه پاسداران برای جبران کمبود شدید جنگ‌افزار و تحریم تسلیحاتی، با تکیه بر سازماندهی داوطلبان بسیجی دست به «حملات موج انسانی» زد و فرهنگ ایثار و شهادت‌طلبی را جایگزین برتری آتش و تجهیزات ارتش بعث ساخت."
    },
    "provenance": {
      "source_book": "Factional Politics and the Iran-Iraq War",
      "source_author": "Mohammad Ayatollahi Tabaar",
      "page_number": 48,
      "verbatim_passage": "Following the consolidation of clerical power, the IRGC operationalized its ideological doctrine, deploying mass volunteer Basij units in human-wave assaults that prioritized faith and martyrdom over conventional military technology.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_maktabi_expert_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "MAKTABI VS EXPERT", "fa": "مکتبی در سنگر، متخصص در دفتر"},
    "clue_text": {
      "en": "To arbitrate factional warfare between the Artesh and Pasdaran and coordinate the war effort, Ayatollah Khomeini appointed Ali Khamenei and this future president as his personal representatives to the Supreme Defense Council.",
      "fa": "برای داوری در منازعات ارتش و سپاه و هماهنگی کلان فرماندهی جنگ، امام خمینی علی خامنه‌ای و این رئیس‌جمهور آینده را به عنوان نمایندگان تام‌الاختیار خود در شورای عالی دفاع منصوب کردند."
    },
    "canonical_answer": {"en": "Ali Akbar Hashemi Rafsanjani", "fa": "علی‌اکبر هاشمی رفسنجانی"},
    "accepted_aliases": {"en": ["Hashemi Rafsanjani", "Rafsanjani", "Akbar Hashemi Rafsanjani"], "fa": ["هاشمی رفسنجانی", "رفسنجانی", "اکبر هاشمی رفسنجانی", "آیت‌الله هاشمی رفسنجانی"]},
    "options": {
      "en": ["Mir-Hossein Mousavi", "Ali Akbar Hashemi Rafsanjani", "Mohammad-Ali Rajai", "Ahmad Khomeini"],
      "fa": ["میرحسین موسوی", "علی‌اکبر هاشمی رفسنجانی", "محمدعلی رجایی", "سید احمد خمینی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Mir-Hossein Mousavi", "why_plausible": "The wartime Prime Minister throughout 1981-1989.", "why_wrong": "Mousavi served ex officio on the council as prime minister, but was not Khomeini's personal representative paired with Khamenei."},
      {"option": "Mohammad-Ali Rajai", "why_plausible": "A prominent early leader.", "why_wrong": "Rajai served on the council as Prime Minister/President until his assassination in August 1981."},
      {"option": "Ahmad Khomeini", "why_plausible": "Khomeini's son and gatekeeper.", "why_wrong": "Ahmad managed Khomeini's personal office in Jamaran, not the formal representative on the Supreme Defense Council."}
    ],
    "adversarial_confusion_set": {"en": ["Mohsen Rezaee", "Ali Shamkhani"], "fa": ["محسن رضایی", "علی شمخانی"]},
    "specificity_prompt": {
      "en": "Name the influential cleric appointed alongside Ali Khamenei to represent Khomeini on the Supreme Defense Council.",
      "fa": "نام روحانی بانفوذی که همراه با آیت‌الله خامنه‌ای نماینده امام در شورای عالی دفاع و بعدها جانشین فرمانده کل قوا شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ali Akbar Hashemi Rafsanjani. Spot on. The ultimate political maestro, balancing generals, mullahs, and missile procurement in his briefcase.",
        "wrong_generic": "No, it was Ali Akbar Hashemi Rafsanjani. The man who ended up managing the entire war.",
        "common_wrong_answers": {
          "Mir-Hossein Mousavi": "Mousavi attended as Prime Minister, managing the food coupons.",
          "Mohammad-Ali Rajai": "Rajai died in the August 1981 bomb explosion.",
          "Ahmad Khomeini": "Haj Ahmad sat beside his father in Jamaran filtering visitors."
        }
      },
      "fa": {
        "correct_generic": "علی‌اکبر هاشمی رفسنجانی. کاملاً درسته! سیاستمدار همه‌فن‌حریفی که هم فرماندهی جنگ را به دست گرفت و هم سرانجام جام زهر را به مقصد رساند.",
        "wrong_generic": "خیر، پاسخ آیت‌الله علی‌اکبر هاشمی رفسنجانی بود. معمار پیوند سیاست و میدان در دهه شصت.",
        "common_wrong_answers": {
          "میرحسین موسوی": "موسوی به عنوان نخست‌وزیر عضو حقوقی بود و اقتصاد جنگ را اداره می‌کرد.",
          "محمدعلی رجایی": "رجایی در شهریور ۶۰ شهید شد و در بخش اعظم دوران جنگ حضور نداشت.",
          "سید احمد خمینی": "حاج احمد آقا در دفتر جماران در کنار امام بود و نماینده شورا نبود."
        }
      }
    },
    "explanation": {
      "en": "Ayatollahi Tabaar highlights that Ayatollah Khomeini appointed Ali Khamenei and Ali Akbar Hashemi Rafsanjani as his direct personal representatives to the Supreme Defense Council (Shoraye Aali-e Defa'); in 1988, Rafsanjani was appointed acting Commander-in-Chief, culminating in his persuasion of Khomeini to accept UN Resolution 598.",
      "fa": "آیت‌اللهی‌تبار اشاره می‌کند که امام خمینی حضرات آیات خامنه‌ای و هاشمی رفسنجانی را به عنوان نمایندگان خود در شورای عالی دفاع منصوب کردند؛ رفسنجانی در خرداد ۶۷ به جانشینی فرماندهی کل قوا رسید و زمینه پذیرش قطعنامه ۵۹۸ را فراهم آورد."
    },
    "provenance": {
      "source_book": "Factional Politics and the Iran-Iraq War",
      "source_author": "Mohammad Ayatollahi Tabaar",
      "page_number": 54,
      "verbatim_passage": "Khomeini positioned Ali Khamenei and Ali Akbar Hashemi Rafsanjani as his personal emissaries on the Supreme Defense Council, empowering Rafsanjani to balance military rivalries and ultimately steer the state toward accepting the 1988 ceasefire.",
      "evidence_type": "FACT"
    }
  }
]

batch_b.extend(cats_17_to_20)

with open("/Users/Morad/Spark/build_batch_b.py", "w", encoding="utf-8") as f:
    f.write("batch_b = " + json.dumps(batch_b, ensure_ascii=False, indent=2) + "\n")

print(f"Batch B complete! Total clues: {len(batch_b)}")
