import sys
import json
from pathlib import Path
sys.path.append("/Users/Morad/Spark")
from jeopardy_pipeline import validate_clue_schema

batch_1_clues = [
  # 1. single_jihad_brick: THE JIHAD OF BRICK AND MORTAR / جهاد با بیل و بی‌سیم
  {
    "id": "single_jihad_brick_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "THE JIHAD OF BRICK AND MORTAR",
      "fa": "جهاد با بیل و بی‌سیم"
    },
    "clue_text": {
      "en": "Founded by Ayatollah Khomeini in June 1979 to bring electrification, roads, and healthcare to neglected villages, this revolutionary grassroots development organization was known as Construction Jihad.",
      "fa": "این نهاد انقلابی در خرداد ۱۳۵۸ به فرمان آیت‌الله خمینی برای محرومیت‌زدایی، برق‌رسانی و جاده‌سازی در روستاهای دورافتاده تأسیس شد و جهاد سازندگی نام گرفت."
    },
    "canonical_answer": {
      "en": "Construction Jihad",
      "fa": "جهاد سازندگی"
    },
    "accepted_aliases": {
      "en": ["Jihad-e Sazandegi", "Jihad of Construction", "Crusade for Construction"],
      "fa": ["جهاد سازندگی", "نهاد جهاد سازندگی"]
    },
    "options": {
      "en": ["Construction Jihad", "Bonyad-e Mostazafan", "Basij Organization", "Islamic Revolutionary Komitehs"],
      "fa": ["جهاد سازندگی", "بنیاد مستضعفان", "سازمان بسیج", "کمیته‌های انقلاب اسلامی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Bonyad-e Mostazafan", "why_plausible": "A major revolutionary foundation formed to manage confiscated wealth.", "why_wrong": "It was a wealth-holding foundation, not the rural grassroots mobilization body founded in June 1979."},
      {"option": "Basij Organization", "why_plausible": "A mass volunteer paramilitary organization founded around the same era.", "why_wrong": "Basij was formed in November 1979 for paramilitary defense, not rural civil development."},
      {"option": "Islamic Revolutionary Komitehs", "why_plausible": "Early revolutionary neighborhood enforcement groups.", "why_wrong": "Komitehs focused on policing and counter-revolution in cities, not rural engineering."}
    ],
    "adversarial_confusion_set": {
      "en": ["Bonyad-e Maskan", "Basij-e Sazandegi"],
      "fa": ["بنیاد مسکن", "بسیج سازندگی"]
    },
    "specificity_prompt": {
      "en": "Please name the specific revolutionary rural development organization founded in June 1979.",
      "fa": "لطفاً نام دقیق این نهاد انقلابی عمران روستایی تأسیس‌شده در خرداد ۵۸ را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Construction Jihad. Correct. Paving roads and preaching revolution at the same time.",
        "wrong_generic": "No, it was Construction Jihad. The pickup trucks with loudspeakers were unmistakable.",
        "common_wrong_answers": {
          "Bonyad-e Mostazafan": "The Bonyad seized palaces; Jihad dug irrigation ditches.",
          "Basij Organization": "Basij guarded street corners; Jihad paved mud tracks.",
          "Islamic Revolutionary Komitehs": "Komitehs raided homes; Jihad built rural bathhouses."
        }
      },
      "fa": {
        "correct_generic": "جهاد سازندگی. کاملاً درسته! سنگرسازان بی سنگری که بیل را با تفنگ عوض کردند.",
        "wrong_generic": "خیر، پاسخ جهاد سازندگی بود. وانت‌های گل‌آلود و شعارهای روستایی را یادتان رفته است.",
        "common_wrong_answers": {
          "بنیاد مستضعفان": "بنیاد کاخ‌ها را مصادره کرد، جهاد در روستا جوی آب کشید.",
          "سازمان بسیج": "بسیج نیروی شبه‌نظامی بود، جهاد متولی عمران و آبادانی روستاها شد.",
          "کمیته‌های انقلاب اسلامی": "کمیته‌ها امنیت شهری را پایش می‌کردند، نه لوله‌کشی آب در کویر."
        }
      }
    },
    "explanation": {
      "en": "Eric Lob explains that Construction Jihad was established in June 1979 as a populist, decentralized mobilization agency to bridge the urban-rural gap and win rural loyalty for the new Islamic regime.",
      "fa": "اریک لوب توضیح می‌دهد که جهاد سازندگی در خرداد ۱۳۵۸ به عنوان بازوی پوپولیستی و غیرمتمرکز نظام برای توسعه روستایی و جلب وفاداری روستاییان به جمهوری اسلامی شکل گرفت."
    },
    "provenance": {
      "source_book": "An Institutional Approach to the Construction Jihad",
      "source_author": "Eric Lob",
      "page_number": 268,
      "verbatim_passage": "On June 17, 1979, Ayatollah Ruhollah Khomeini called for the creation of the Construction Jihad to assist the rural poor and reconstruct devastated villages throughout Iran.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_jihad_brick_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE JIHAD OF BRICK AND MORTAR",
      "fa": "جهاد با بیل و بی‌سیم"
    },
    "clue_text": {
      "en": "During the 1984 Operation Kheibar in the marshlands of southern Iraq, Construction Jihad engineers achieved a military marvel by constructing this 14-kilometer floating pontoon bridge.",
      "fa": "مهندسان جهاد سازندگی در عملیات خیبر در سال ۱۳۶۲ در هورالهویزه شاهکاری نظامی خلق کردند و این پل شناور ۱۴ کیلومتری را روی باتلاق‌ها ساختند."
    },
    "canonical_answer": {
      "en": "Kheibar Bridge",
      "fa": "پل خیبر"
    },
    "accepted_aliases": {
      "en": ["Pol-e Kheibar", "Kheibar floating bridge", "Kheybar Bridge"],
      "fa": ["پل خیبر", "پل شناور خیبر"]
    },
    "options": {
      "en": ["Kheibar Bridge", "Besat Bridge", "Naderi Bridge", "Fajr Bridge"],
      "fa": ["پل خیبر", "پل بعثت", "پل نادری", "پل فجر"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Besat Bridge", "why_plausible": "A famous stationary tubular military bridge over the Arvand river in 1986.", "why_wrong": "Besat was built across the Arvand during Operation Valfajr-8, not the 14-km floating pontoon bridge in Kheibar."},
      {"option": "Naderi Bridge", "why_plausible": "A bridge over the Karkheh river during early war operations.", "why_wrong": "Naderi was a pre-existing permanent river crossing near Dezful in 1980."},
      {"option": "Fajr Bridge", "why_plausible": "Named after wartime Fajr offensives.", "why_wrong": "It was not the historic 14-km pontoon bridge constructed in the Hour al-Howeizeh marshes."}
    ],
    "adversarial_confusion_set": {
      "en": ["Besat Bridge", "Arvand Pontoon Bridge"],
      "fa": ["پل بعثت", "پل اروند"]
    },
    "specificity_prompt": {
      "en": "Name the specific 14-kilometer floating pontoon bridge built across the marshes in 1984.",
      "fa": "نام دقیق پل شناور ۱۴ کیلومتری ساخته‌شده در هورالهویزه را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Kheibar Bridge. That is it. Fourteen kilometers of foam and steel floating under artillery fire.",
        "wrong_generic": "No, it was the Kheibar Bridge. Quite a leap across the marshes to forget.",
        "common_wrong_answers": {
          "Besat Bridge": "Besat spanned the Arvand with steel pipes in 1986; Kheibar floated on foam in 1984.",
          "Naderi Bridge": "Naderi was near Dezful; Kheibar spanned the deep southern marshes.",
          "Fajr Bridge": "Not Fajr; Kheibar gave its name to the offensive and the floating pontoon."
        }
      },
      "fa": {
        "correct_generic": "پل خیبر. کاملاً درسته! طولانی‌ترین پل شناور تاریخ نظامی که روی باتلاق‌ها شناور شد.",
        "wrong_generic": "خیر، پاسخ پل خیبر بود. ۱۴ کیلومتر پل یونولیتی زیر آتش توپخانه را از یاد بردید.",
        "common_wrong_answers": {
          "پل بعثت": "پل بعثت لوله‌ای بود و روی اروند در سال ۶۴ احداث شد، خیبر شناور بود در سال ۶۲.",
          "پل نادری": "پل نادری روی کرخه در دزفول بود، نه وسط هورالهویزه.",
          "پل فجر": "عملیات فجر نام‌های دیگری داشت؛ نام این شاهکار مهندسی پل خیبر است."
        }
      }
    },
    "explanation": {
      "en": "Eric Lob documents that Construction Jihad's war support headquarters designed and prefabricated the 14-kilometer Pol-e Kheibar pontoon bridge using fiberglass and foam blocks to connect supply lines across the Hawizeh marshes.",
      "fa": "اریک لوب مستند می‌کند که ستاد پشتیبانی جهاد سازندگی با طراحی قطعات فایبرگلاس و یونولیت، پل شناور ۱۴ کیلومتری خیبر را احداث کرد تا خطوط تدارکاتی در هورالهویزه به یکدیگر متصل شوند."
    },
    "provenance": {
      "source_book": "An Institutional Approach to the Construction Jihad",
      "source_author": "Eric Lob",
      "page_number": 275,
      "verbatim_passage": "Jihad engineers demonstrated technical ingenuity by designing and assembling the fourteen-kilometer floating Kheibar Bridge in the Hawizeh marshes during Operation Kheibar in 1984.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_jihad_brick_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE JIHAD OF BRICK AND MORTAR",
      "fa": "جهاد با بیل و بی‌سیم"
    },
    "clue_text": {
      "en": "Because its bulldozer operators and trench diggers built protective earthen ramparts under direct enemy fire without personal fortifications, Construction Jihad personnel earned this famous Persian moniker.",
      "fa": "رانندگان لودر و بلدوزرهای جهاد سازندگی به دلیل احداث خاکریز زیر آتش مستقیم دشمن و بدون جان‌پناه فردی، به این عنوان پرآوازه ملقب شدند."
    },
    "canonical_answer": {
      "en": "Sangar-sazan-e Bi-Sangar",
      "fa": "سنگرسازان بی سنگر"
    },
    "accepted_aliases": {
      "en": ["Sangarsazan-e Bi-Sangar", "Trench-builders without trenches", "Trench makers without shelters", "Sangarsazan"],
      "fa": ["سنگرسازان بی‌سنگر", "سنگر سازان بی سنگر"]
    },
    "options": {
      "en": ["Sangar-sazan-e Bi-Sangar", "Khat-shekanan", "Ghavasan-e Daryadel", "Shohada-ye Gomnam"],
      "fa": ["سنگرسازان بی سنگر", "خط‌شکنان", "غواصان دریادل", "شهدای گمنام"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Khat-shekanan", "why_plausible": "A revered term for frontline assault infantry.", "why_wrong": "Khat-shekanan refers to frontline breakthrough fighters, not engineering earthmovers."},
      {"option": "Ghavasan-e Daryadel", "why_plausible": "A famous wartime phrase describing combat divers.", "why_wrong": "It refers to military divers, particularly in Operation Karbala-4."},
      {"option": "Shohada-ye Gomnam", "why_plausible": "A pervasive cultural moniker for unidentified martyrs.", "why_wrong": "It describes unidentified fallen soldiers, not the specific institutional moniker for Jihad engineers."}
    ],
    "adversarial_confusion_set": {
      "en": ["Khat-shekanan", "Janbazan"],
      "fa": ["خط‌شکنان", "جانبازان"]
    },
    "specificity_prompt": {
      "en": "Provide the exact Persian honorary title given to unarmed Jihad earthmover operators at the front.",
      "fa": "عنوان مشهور جهادگران راننده بولدوزر در خطوط مقدم را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Sangar-sazan-e Bi-Sangar. Correct. Driving a yellow Caterpillar directly into tank fire is certainly one way to build a resume.",
        "wrong_generic": "No, they were Sangar-sazan-e Bi-Sangar. Unarmed earthmovers facing heavy artillery.",
        "common_wrong_answers": {
          "Khat-shekanan": "Khat-shekanan were infantry shock troops, not bulldozer drivers.",
          "Ghavasan-e Daryadel": "Combat divers swam in rivers; these men drove heavy diggers into mud.",
          "Shohada-ye Gomnam": "Shohada-ye Gomnam are unidentified casualties; Sangar-sazan was an active wartime title."
        }
      },
      "fa": {
        "correct_generic": "سنگرسازان بی سنگر. کاملاً درسته! نشستن پشت فرمان بلدوزر زیر باران خمپاره دل شیر می‌خواست.",
        "wrong_generic": "خیر، پاسخ سنگرسازان بی سنگر بود. معروف‌ترین تعبیر دوران جنگ درباره جهادگران را فراموش کردید.",
        "common_wrong_answers": {
          "خط‌شکنان": "خط‌شکنان نیروهای پیاده خط مقدم بودند، نه رانندگان ماشین‌آلات سنگین مهندسی.",
          "غواصان دریادل": "غواصان در اروند شنا می‌کردند، جهادگران با لودر خاکریز می‌زدند.",
          "شهدای گمنام": "شهدای گمنام عنوان عمومی ایثارگران مفقودالاثر است، نه نشان اختصاصی جهاد."
        }
      }
    },
    "explanation": {
      "en": "Eric Lob highlights that Construction Jihad drivers operating heavy machinery under direct artillery fire to build frontline earthen embankments were officially commemorated by Khomeini as 'Sangar-sazan-e Bi-Sangar' (Trench-builders without trenches).",
      "fa": "اریک لوب اشاره می‌کند که امام خمینی رانندگان ادوات سنگین جهاد سازندگی را که زیر آتش برای رزمندگان جان‌پناه می‌ساختند، «سنگرسازان بی‌سنگر» نامید."
    },
    "provenance": {
      "source_book": "An Institutional Approach to the Construction Jihad",
      "source_author": "Eric Lob",
      "page_number": 277,
      "verbatim_passage": "Because the bulldozer and excavator operators built ramparts and trenches under direct fire without protective armor, Khomeini affectionately dubbed them 'the trench-makers without trenches' (sangar-sazan-e bi-sangar).",
      "evidence_type": "PRIMARY_TESTIMONY"
    }
  },
  {
    "id": "single_jihad_brick_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "THE JIHAD OF BRICK AND MORTAR",
      "fa": "جهاد با بیل و بی‌سیم"
    },
    "clue_text": {
      "en": "To counter the ideological appeal of Marxist and leftist guerrilla movements in rural provinces like Kurdistan and Gonbad, Construction Jihad paired civil works with this literacy campaign founded in December 1979.",
      "fa": "برای خنثی‌سازی نفوذ گروه‌های چپ‌گرا و مارکسیست در مناطق روستایی گنبد و کردستان، جهاد سازندگی اقدامات عمرانی خود را با این نهضت سوادآموزی پیوند زد که در دی ۱۳۵۸ تأسیس شد."
    },
    "canonical_answer": {
      "en": "Literacy Movement Organization",
      "fa": "نهضت سوادآموزی"
    },
    "accepted_aliases": {
      "en": ["Nehzat-e Savad-Amoozi", "Literacy Movement", "Literacy Crusade"],
      "fa": ["سازمان نهضت سوادآموزی", "نهضت سواد آموزی"]
    },
    "options": {
      "en": ["Literacy Movement Organization", "Education Corps", "Farhang-e Farhangian", "Kanoon-e Parvaresh-e Fekri"],
      "fa": ["نهضت سوادآموزی", "سپاه دانش", "فرهنگ فرهنگیان", "کانون پرورش فکری"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Education Corps", "why_plausible": "The Pahlavi-era rural literacy program (Sepah-e Danesh).", "why_wrong": "Sepah-e Danesh was disbanded with the 1979 revolution and replaced by the revolutionary Nehzat-e Savad-Amoozi."},
      {"option": "Farhang-e Farhangian", "why_plausible": "Sounds like an educational state organ.", "why_wrong": "Not a historical revolutionary mass campaign founded in 1979."},
      {"option": "Kanoon-e Parvaresh-e Fekri", "why_plausible": "A celebrated children's cultural institution.", "why_wrong": "Kanoon was founded under Empress Farah Pahlavi in 1965, not by revolutionary decree in December 1979."}
    ],
    "adversarial_confusion_set": {
      "en": ["Sepah-e Danesh", "Peykar Campaign"],
      "fa": ["سپاه دانش", "پیکار با بی‌سوادی"]
    },
    "specificity_prompt": {
      "en": "Name the specific post-revolutionary literacy organization established in December 1979.",
      "fa": "نام نهاد انقلابی سوادآموزی تأسیس‌شده در دی ۱۳۵۸ را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Literacy Movement Organization. Correct. Teaching the alphabet alongside revolutionary slogans in the barn.",
        "wrong_generic": "No, it was the Literacy Movement (Nehzat-e Savad-Amoozi). Replacing Pahlavi text with revolutionary doctrine.",
        "common_wrong_answers": {
          "Education Corps": "Sepah-e Danesh was the Shah's program; the revolution scrapped it for Nehzat.",
          "Farhang-e Farhangian": "A fabricated ministry; you wanted Nehzat-e Savad-Amoozi.",
          "Kanoon-e Parvaresh-e Fekri": "Kanoon was Farah Diba's creation, not Khomeini's 1979 campaign."
        }
      },
      "fa": {
        "correct_generic": "نهضت سوادآموزی. کاملاً درسته! تدریس الفبا همراه با جزوه‌های ایدئولوژیک در کپرها.",
        "wrong_generic": "خیر، پاسخ نهضت سوادآموزی بود. بازوی فرهنگی انقلاب در روستاها را فراموش کرده‌اید.",
        "common_wrong_answers": {
          "سپاه دانش": "سپاه دانش برنامه پهلوی بود که پس از انقلاب منحل شد؛ نهضت جایگزین آن گردید.",
          "فرهنگ فرهنگیان": "چنین نهاد انقلابی در سال ۵۸ وجود خارجی نداشت.",
          "کانون پرورش فکری": "کانون پیش از انقلاب تأسیس شده بود، نه با فرمان دی‌ماه ۵۸."
        }
      }
    },
    "explanation": {
      "en": "Eric Lob demonstrates that Construction Jihad collaborated closely with Nehzat-e Savad-Amoozi (founded December 1979) to eliminate rural illiteracy and displace leftist revolutionary student organizers in the rural periphery.",
      "fa": "اریک لوب نشان می‌دهد که جهاد سازندگی با همکاری نهضت سوادآموزی (تأسیس دی ۱۳۵۸) تلاش کرد با ریشه‌کنی بی‌سوادی، نفوذ نیروهای چپ در مناطق پیرامونی و روستایی را مهار کند."
    },
    "provenance": {
      "source_book": "An Institutional Approach to the Construction Jihad",
      "source_author": "Eric Lob",
      "page_number": 272,
      "verbatim_passage": "Construction Jihad synchronized its rural development initiatives with the Literacy Movement Organization (Nehzat-e Savad-Amuzi) created in December 1979, combating Marxist appeal by propagating religious texts.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_jihad_brick_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "THE JIHAD OF BRICK AND MORTAR",
      "fa": "جهاد با بیل و بی‌سیم"
    },
    "clue_text": {
      "en": "In a controversial 2001 bureaucratic consolidation enacted during Mohammad Khatami's reformist presidency, the Ministry of Construction Jihad was permanently merged into this conventional cabinet ministry.",
      "fa": "در یک ادغام اداری مناقشه‌برانگیز در سال ۱۳۷۹ در دوران ریاست‌جمهوری محمد خاتمی، وزارت جهاد سازندگی رسماً در این وزارتخانه سنتی حل شد."
    },
    "canonical_answer": {
      "en": "Ministry of Agriculture",
      "fa": "وزارت کشاورزی"
    },
    "accepted_aliases": {
      "en": ["Agriculture Ministry", "Vezarat-e Keshavarzi", "Ministry of Agricultural Jihad"],
      "fa": ["وزارت جهاد کشاورزی", "کشاورزی", "وزارت جهاد و کشاورزی"]
    },
    "options": {
      "en": ["Ministry of Agriculture", "Ministry of Energy", "Ministry of Roads and Transportation", "Ministry of Cooperatives"],
      "fa": ["وزارت کشاورزی", "وزارت نیرو", "وزارت راه و ترابری", "وزارت تعاون"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Ministry of Energy", "why_plausible": "Jihad handled vast rural electrification and dam building.", "why_wrong": "Energy remained independent; Jihad merged with Agriculture to form Jihad-e Keshavarzi."},
      {"option": "Ministry of Roads and Transportation", "why_plausible": "Jihad built thousands of kilometers of rural unpaved roads.", "why_wrong": "Roads and Transportation was not the recipient of Jihad's bureaucratic assets."},
      {"option": "Ministry of Cooperatives", "why_plausible": "Cooperatives managed rural collective farming.", "why_wrong": "It merged directly with Agriculture in 2001 under law passed in 2000."}
    ],
    "adversarial_confusion_set": {
      "en": ["Ministry of Energy", "Ministry of Rural Development"],
      "fa": ["وزارت نیرو", "وزارت عمران و روستایی"]
    },
    "specificity_prompt": {
      "en": "Name the specific cabinet ministry that absorbed Construction Jihad in 2001.",
      "fa": "نام وزارتخانه‌ای که در سال ۱۳۷۹ با جهاد سازندگی ادغام شد را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ministry of Agriculture. Correct. Turning a revolutionary holy crusade into standard civil service desk jobs.",
        "wrong_generic": "No, it merged into the Ministry of Agriculture. Thus creating the hybrid Jihad-e Keshavarzi.",
        "common_wrong_answers": {
          "Ministry of Energy": "Energy kept the power grid; Agriculture absorbed the entire Jihad machinery.",
          "Ministry of Roads and Transportation": "They built roads, but Agriculture claimed the institutional prize.",
          "Ministry of Cooperatives": "Cooperatives had other duties; Keshavarzi absorbed the crusade."
        }
      },
      "fa": {
        "correct_generic": "وزارت کشاورزی. کاملاً درسته! پایان رؤیای انقلابی و تبدیل مجاهدان به کارمندان پشت‌میزنشین.",
        "wrong_generic": "خیر، پاسخ وزارت کشاورزی بود که به تشکیل «وزارت جهاد کشاورزی» انجامید.",
        "common_wrong_answers": {
          "وزارت نیرو": "وزارت نیرو متولی برق بود، اما کل ساختار جهاد جذب کشاورزی شد.",
          "وزارت راه و ترابری": "جهادگران جاده کشیدند اما سازمان اداری‌شان به کشاورزی واگذار شد.",
          "وزارت تعاون": "تعاون ادغام نشد؛ کشاورزی و جهاد در هم آمیختند."
        }
      }
    },
    "explanation": {
      "en": "Eric Lob analyzes the 2001 merger of Construction Jihad with the Ministry of Agriculture as the culmination of state institutionalization, stripping the movement of its original revolutionary autonomy and subordinating it to bureaucratic routines.",
      "fa": "اریک لوب ادغام سال ۱۳۷۹ جهاد سازندگی با وزارت کشاورزی را پایان استقلال نهادهای انقلابی و پیروزی دیوان‌سالاری متعارف بر ساختارهای خودجوش می‌داند."
    },
    "provenance": {
      "source_book": "An Institutional Approach to the Construction Jihad",
      "source_author": "Eric Lob",
      "page_number": 284,
      "verbatim_passage": "In January 2001, Parliament approved the merger of the Ministry of Construction Jihad with the Ministry of Agriculture, creating the Ministry of Agricultural Jihad (Vezarat-e Jihad-e Keshavarzi) and effectively ending its revolutionary exceptionalism.",
      "evidence_type": "FACT"
    }
  }
]

for c in batch_1_clues:
    validate_clue_schema(c)

print(f"Validated {len(batch_1_clues)} clues for Category 1 successfully.")
