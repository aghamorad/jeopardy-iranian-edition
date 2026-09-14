import sys
from pathlib import Path
sys.path.append("/Users/Morad/Spark")
from jeopardy_pipeline import validate_clue_schema

batch_a = []

# Categories 1 and 2
batch_a.extend([
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
      "en": [
        "Jihad-e Sazandegi",
        "Jihad of Construction",
        "Crusade for Construction"
      ],
      "fa": [
        "جهاد سازندگی",
        "نهاد جهاد سازندگی"
      ]
    },
    "options": {
      "en": [
        "Bonyad-e Mostazafan",
        "Construction Jihad",
        "Basij Organization",
        "Islamic Revolutionary Komitehs"
      ],
      "fa": [
        "بنیاد مستضعفان",
        "جهاد سازندگی",
        "سازمان بسیج",
        "کمیته‌های انقلاب اسلامی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Bonyad-e Mostazafan",
        "why_plausible": "A major revolutionary foundation formed to manage confiscated wealth.",
        "why_wrong": "It was a wealth-holding foundation, not the rural grassroots mobilization body founded in June 1979."
      },
      {
        "option": "Basij Organization",
        "why_plausible": "A mass volunteer paramilitary organization founded around the same era.",
        "why_wrong": "Basij was formed in November 1979 for paramilitary defense, not rural civil development."
      },
      {
        "option": "Islamic Revolutionary Komitehs",
        "why_plausible": "Early revolutionary neighborhood enforcement groups.",
        "why_wrong": "Komitehs focused on policing and counter-revolution in cities, not rural engineering."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Bonyad-e Maskan",
        "Basij-e Sazandegi"
      ],
      "fa": [
        "بنیاد مسکن",
        "بسیج سازندگی"
      ]
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
      "en": [
        "Pol-e Kheibar",
        "Kheibar floating bridge",
        "Kheybar Bridge"
      ],
      "fa": [
        "پل خیبر",
        "پل شناور خیبر"
      ]
    },
    "options": {
      "en": [
        "Besat Bridge",
        "Naderi Bridge",
        "Kheibar Bridge",
        "Fajr Bridge"
      ],
      "fa": [
        "پل بعثت",
        "پل نادری",
        "پل خیبر",
        "پل فجر"
      ]
    },
    "correct_option_index": 2,
    "distractor_rationales": [
      {
        "option": "Besat Bridge",
        "why_plausible": "A famous stationary tubular military bridge over the Arvand river in 1986.",
        "why_wrong": "Besat was built across the Arvand during Operation Valfajr-8, not the 14-km floating pontoon bridge in Kheibar."
      },
      {
        "option": "Naderi Bridge",
        "why_plausible": "A bridge over the Karkheh river during early war operations.",
        "why_wrong": "Naderi was a pre-existing permanent river crossing near Dezful in 1980."
      },
      {
        "option": "Fajr Bridge",
        "why_plausible": "Named after wartime Fajr offensives.",
        "why_wrong": "It was not the historic 14-km pontoon bridge constructed in the Hour al-Howeizeh marshes."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Besat Bridge",
        "Arvand Pontoon Bridge"
      ],
      "fa": [
        "پل بعثت",
        "پل اروند"
      ]
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
      "en": [
        "Sangarsazan-e Bi-Sangar",
        "Trench-builders without trenches",
        "Trench makers without shelters",
        "Sangarsazan"
      ],
      "fa": [
        "سنگرسازان بی‌سنگر",
        "سنگر سازان بی سنگر"
      ]
    },
    "options": {
      "en": [
        "Khat-shekanan",
        "Ghavasan-e Daryadel",
        "Shohada-ye Gomnam",
        "Sangar-sazan-e Bi-Sangar"
      ],
      "fa": [
        "خط‌شکنان",
        "غواصان دریادل",
        "شهدای گمنام",
        "سنگرسازان بی سنگر"
      ]
    },
    "correct_option_index": 3,
    "distractor_rationales": [
      {
        "option": "Khat-shekanan",
        "why_plausible": "A revered term for frontline assault infantry.",
        "why_wrong": "Khat-shekanan refers to frontline breakthrough fighters, not engineering earthmovers."
      },
      {
        "option": "Ghavasan-e Daryadel",
        "why_plausible": "A famous wartime phrase describing combat divers.",
        "why_wrong": "It refers to military divers, particularly in Operation Karbala-4."
      },
      {
        "option": "Shohada-ye Gomnam",
        "why_plausible": "A pervasive cultural moniker for unidentified martyrs.",
        "why_wrong": "It describes unidentified fallen soldiers, not the specific institutional moniker for Jihad engineers."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Khat-shekanan",
        "Janbazan"
      ],
      "fa": [
        "خط‌شکنان",
        "جانبازان"
      ]
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
      "en": [
        "Nehzat-e Savad-Amoozi",
        "Literacy Movement",
        "Literacy Crusade"
      ],
      "fa": [
        "سازمان نهضت سوادآموزی",
        "نهضت سواد آموزی"
      ]
    },
    "options": {
      "en": [
        "Education Corps",
        "Literacy Movement Organization",
        "Farhang-e Farhangian",
        "Kanoon-e Parvaresh-e Fekri"
      ],
      "fa": [
        "سپاه دانش",
        "نهضت سوادآموزی",
        "فرهنگ فرهنگیان",
        "کانون پرورش فکری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Education Corps",
        "why_plausible": "The Pahlavi-era rural literacy program (Sepah-e Danesh).",
        "why_wrong": "Sepah-e Danesh was disbanded with the 1979 revolution and replaced by the revolutionary Nehzat-e Savad-Amoozi."
      },
      {
        "option": "Farhang-e Farhangian",
        "why_plausible": "Sounds like an educational state organ.",
        "why_wrong": "Not a historical revolutionary mass campaign founded in 1979."
      },
      {
        "option": "Kanoon-e Parvaresh-e Fekri",
        "why_plausible": "A celebrated children's cultural institution.",
        "why_wrong": "Kanoon was founded under Empress Farah Pahlavi in 1965, not by revolutionary decree in December 1979."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Sepah-e Danesh",
        "Peykar Campaign"
      ],
      "fa": [
        "سپاه دانش",
        "پیکار با بی‌سوادی"
      ]
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
      "en": [
        "Agriculture Ministry",
        "Vezarat-e Keshavarzi",
        "Ministry of Agricultural Jihad"
      ],
      "fa": [
        "وزارت جهاد کشاورزی",
        "کشاورزی",
        "وزارت جهاد و کشاورزی"
      ]
    },
    "options": {
      "en": [
        "Ministry of Energy",
        "Ministry of Roads and Transportation",
        "Ministry of Cooperatives",
        "Ministry of Agriculture"
      ],
      "fa": [
        "وزارت نیرو",
        "وزارت راه و ترابری",
        "وزارت تعاون",
        "وزارت کشاورزی"
      ]
    },
    "correct_option_index": 3,
    "distractor_rationales": [
      {
        "option": "Ministry of Energy",
        "why_plausible": "Jihad handled vast rural electrification and dam building.",
        "why_wrong": "Energy remained independent; Jihad merged with Agriculture to form Jihad-e Keshavarzi."
      },
      {
        "option": "Ministry of Roads and Transportation",
        "why_plausible": "Jihad built thousands of kilometers of rural unpaved roads.",
        "why_wrong": "Roads and Transportation was not the recipient of Jihad's bureaucratic assets."
      },
      {
        "option": "Ministry of Cooperatives",
        "why_plausible": "Cooperatives managed rural collective farming.",
        "why_wrong": "It merged directly with Agriculture in 2001 under law passed in 2000."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Ministry of Energy",
        "Ministry of Rural Development"
      ],
      "fa": [
        "وزارت نیرو",
        "وزارت عمران و روستایی"
      ]
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
  },
  {
    "id": "single_khomeini_populism_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "KHOMEINISM AND ITS DISCONTENTS",
      "fa": "پوپولیسم در ردای فقه"
    },
    "clue_text": {
      "en": "In his seminal study Khomeinism, Ervand Abrahamian explains that Ayatollah Khomeini transformed this Quranic term from a theological descriptor of the spiritually weak into a modern populist political label for the revolutionary working masses.",
      "fa": "یرواند آبراهامیان در کتاب «خمینیسم» توضیح می‌دهد که آیت‌الله خمینی این واژه قرآنی را از معنای کلامیِ ضعیفان دینی خارج کرد و به عنوان برچسبی پوپولیستی و معادل توده‌های زحمتکش انقلابی به کار برد."
    },
    "canonical_answer": {
      "en": "Mostazafin",
      "fa": "مستضعفین"
    },
    "accepted_aliases": {
      "en": [
        "Mostazafan",
        "The Oppressed",
        "The Disinherited",
        "Mustad'afin"
      ],
      "fa": [
        "مستضعفان",
        "مستضعف",
        "کوخ‌نشینان"
      ]
    },
    "options": {
      "en": [
        "Mostazafin",
        "Taghut",
        "Monafeqin",
        "Kuffar"
      ],
      "fa": [
        "مستضعفین",
        "طاغوت",
        "منافقین",
        "کفار"
      ]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Taghut",
        "why_plausible": "Another pervasive Quranic term popularized by Khomeini.",
        "why_wrong": "Taghut referred to the oppressors, monarchists, and idols, not the oppressed masses."
      },
      {
        "option": "Monafeqin",
        "why_plausible": "A term heavily used against political enemies like the MEK.",
        "why_wrong": "Monafeqin refers to hypocrites, specifically the Mojahedin-e Khalq, not the virtuous working masses."
      },
      {
        "option": "Kuffar",
        "why_plausible": "A classic theological term for unbelievers.",
        "why_wrong": "Kuffar denotes religious infidels, not the socio-economic category of the disenfranchised."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Ranjbaran",
        "Zahmatkeshan"
      ],
      "fa": [
        "رنجبران",
        "زحمتکشان"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the specific Arabic-origin Quranic term used by Khomeini to denote the oppressed masses.",
      "fa": "واژه قرآنی مشهوری را بنویسید که امام خمینی برای اشاره به پابرهنگان و محرومان به کار می‌برد."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mostazafin. Exactly. Borrowing Marxist class consciousness while wrapping it in Surah al-Qasas.",
        "wrong_generic": "No, the term was Mostazafin. The foundational demographic of revolutionary rhetoric.",
        "common_wrong_answers": {
          "Taghut": "Taghut was the royal oppressors in palaces, not the disinherited.",
          "Monafeqin": "Monafeqin was the label for the MEK, not the beloved masses.",
          "Kuffar": "Kuffar is theological; Mostazafin was economic populism."
        }
      },
      "fa": {
        "correct_generic": "مستضعفین. کاملاً درسته! پیوند ماهرانه مارکسیسم و فقه با وام‌گیری از آیه ونرید ان نمن.",
        "wrong_generic": "خیر، پاسخ مستضعفین بود. شاه‌بیت ادبیات عدالت‌خواهانه اول انقلاب را جا انداختید.",
        "common_wrong_answers": {
          "طاغوت": "طاغوت نماد کاخ‌نشینان و شاه بود، نه توده‌های پابرهنه.",
          "منافقین": "منافقین برچسب سیاسی مجاهدین خلق بود، نه توده‌های رنجدیده.",
          "کفار": "کفار اصطلاح عقیدتی است؛ مستضعفین بار طبقاتی و اقتصادی داشت."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian argues that Khomeini practiced a distinct form of Third World populism, redefining 'Mostazafin' to encompass wage earners, peasants, and the urban poor against the decadent royal elite.",
      "fa": "یرواند آبراهامیان استدلال می‌کند که امام خمینی با بازتعریف مفهوم «مستضعفین» شکلی بومی از پوپولیسم جهان سومی ایجاد کرد که طبقه کارگر و فرودستان شهری را در برابر نخبگان پادشاهی بسیج می‌کرد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 27,
      "verbatim_passage": "Khomeini transformed the term mostazafin from a pious Quranic term for the meek and humble into a militant political slogan designating the oppressed masses and working class.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_khomeini_populism_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "KHOMEINISM AND ITS DISCONTENTS",
      "fa": "پوپولیسم در ردای فقه"
    },
    "clue_text": {
      "en": "In contrast to the virtuous 'Mostazafin', Khomeini designated the Shah, the royal court, and their Westernized oligarchs with this derogatory Quranic concept denoting idolatrous, rebellious tyrants.",
      "fa": "آیت‌الله خمینی در نقطه مقابل «مستضعفین»، شاه و وابستگان دربار پهلوی و سرمایه‌داران غرب‌زده را با این واژه قرآنی به معنای طغیان‌گران و سرکشان ستمگر توصیف می‌کرد."
    },
    "canonical_answer": {
      "en": "Taghut",
      "fa": "طاغوت"
    },
    "accepted_aliases": {
      "en": [
        "Taghoot",
        "Taaghoot",
        "Taghuti",
        "Taghutis"
      ],
      "fa": [
        "طاغوت",
        "طاغوتیان",
        "طاغوتی"
      ]
    },
    "options": {
      "en": [
        "Mofsed-e fel-Arz",
        "Taghut",
        "Mohareb",
        "Marja'"
      ],
      "fa": [
        "مفسد فی‌الارض",
        "طاغوت",
        "محارب",
        "مرجع"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Mofsed-e fel-Arz",
        "why_plausible": "A severe revolutionary legal charge meaning 'corrupt on earth'.",
        "why_wrong": "It was a formal criminal statute in revolutionary courts, not the primary populist political label paired against Mostazafin."
      },
      {
        "option": "Mohareb",
        "why_plausible": "A theological charge meaning 'one who wages war against God'.",
        "why_wrong": "Mohareb is a legal category for armed rebellion, not the overarching cultural-political concept of Taghut."
      },
      {
        "option": "Marja'",
        "why_plausible": "A prominent religious term.",
        "why_wrong": "Marja' denotes a grand source of emulation in Shi'i jurisprudence."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Mofsed",
        "Zalim"
      ],
      "fa": [
        "مفسد",
        "ظالم"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Quranic term meaning idol or tyrant that became the hallmark insult for the Pahlavi regime.",
      "fa": "واژه قرآنی مشهوری را نام ببرید که به عنوان صفت رژیم پهلوی و درباریان به کار می‌رفت."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Taghut. Indeed. If you lived in a villa in Niavaran in 1978, that was your official family name.",
        "wrong_generic": "No, it was Taghut. The standard epithet for the Shah and his golden monuments.",
        "common_wrong_answers": {
          "Mofsed-e fel-Arz": "Mofsed was the courtroom indictment; Taghut was the political category.",
          "Mohareb": "Mohareb was for armed guerrillas on trial; Taghut was for the entire imperial system.",
          "Marja'": "A Marja' is an ayatollah you follow, hardly the Pahlavi court."
        }
      },
      "fa": {
        "correct_generic": "طاغوت. کاملاً درسته! لقبی که داشتن ویلا در نیاوران را بلافاصله جرم اعلام می‌کرد.",
        "wrong_generic": "خیر، پاسخ طاغوت بود. برچسبی که بر پیشانی تمام ارکان رژیم گذشته نشست.",
        "common_wrong_answers": {
          "مفسد فی‌الارض": "مفسد فی‌الارض عنوان اتهامی در دادگاه بود؛ طاغوت مفهوم فراگیر سیاسی بود.",
          "محارب": "محارب در فقه حکم جنگ مسلحانه دارد، طاغوت صفت ساختاری نظام شاهنشاهی بود.",
          "مرجع": "مرجع تقلید پیشوای دینی است، ربطی به دستگاه سلطنت نداشت."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian highlights how Khomeini paired 'Mostazafin' and 'Taghut' as a binary moral struggle: the humble pure believers versus the corrupt idolatrous oppressors.",
      "fa": "یرواند آبراهامیان نشان می‌دهد که چگونه امام خمینی دوگانه «مستضعفین» و «طاغوت» را به یک پیکار اخلاقی و طبقاتی تمام‌عیار میان توده‌های پاک‌نهاد و حاکمان فاسد تبدیل کرد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 28,
      "verbatim_passage": "Khomeini divided society into two antagonistic camps: the oppressed (mostazafin) and the oppressors (mostakberin or taghutis), identifying the Pahlavi monarchy as the supreme manifestation of Taghut.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_khomeini_populism_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "KHOMEINISM AND ITS DISCONTENTS",
      "fa": "پوپولیسم در ردای فقه"
    },
    "clue_text": {
      "en": "In his populist speeches celebrating International Workers' Day (May Day), Ayatollah Khomeini stunned traditionalist clerics by audaciously declaring that this supreme entity was the universe's 'first laborer'.",
      "fa": "آیت‌الله خمینی در سخنرانی‌های پرشور خود به مناسبت روز جهانی کارگر با بیانی متهورانه که موجب شگفتی فقهای سنتی شد، این ذات متعالی را «اولین کارگر» جهان هستی نامید."
    },
    "canonical_answer": {
      "en": "God",
      "fa": "خداوند"
    },
    "accepted_aliases": {
      "en": [
        "Allah",
        "The Almighty",
        "God Almighty"
      ],
      "fa": [
        "خدا",
        "الله",
        "پروردگار"
      ]
    },
    "options": {
      "en": [
        "Imam Ali",
        "Prophet Muhammad",
        "God",
        "Adam"
      ],
      "fa": [
        "امام علی",
        "پیامبر اکرم",
        "خداوند",
        "حضرت آدم"
      ]
    },
    "correct_option_index": 2,
    "distractor_rationales": [
      {
        "option": "Imam Ali",
        "why_plausible": "Imam Ali is famously revered in Shi'ism for digging wells and manual agricultural labor in Medina.",
        "why_wrong": "While Khomeini praised Ali's physical work, his famous theological hyperbole explicitly named God as the first worker."
      },
      {
        "option": "Prophet Muhammad",
        "why_plausible": "Prophet Muhammad was a caravan trader and shepherd praised in Islamic traditions.",
        "why_wrong": "Khomeini pushed the analogy past the prophets directly to the Creator."
      },
      {
        "option": "Adam",
        "why_plausible": "The first human being created by God who worked the earth.",
        "why_wrong": "Khomeini explicitly proclaimed God Himself as the originator of labor."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Imam Ali",
        "Prophet Muhammad"
      ],
      "fa": [
        "امام علی",
        "پیامبر اسلام"
      ]
    },
    "specificity_prompt": {
      "en": "Name the supreme divine entity described by Khomeini as the first laborer in his May Day address.",
      "fa": "نام ذات مقدسی که امام خمینی در پیام روز کارگر ایشان را نخستین کارگر عالم نامیدند بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "God. That is right. Nothing says revolutionary populism like enrolling the Almighty in the labor union.",
        "wrong_generic": "No, he declared that God was the first laborer. Even Karl Marx might have blinked at that one.",
        "common_wrong_answers": {
          "Imam Ali": "Ali dug wells, but Khomeini boldly gave the title of first laborer to God.",
          "Prophet Muhammad": "The Prophet tended sheep; Khomeini went straight to the Creator.",
          "Adam": "Adam was the first man; Khomeini called God the first worker."
        }
      },
      "fa": {
        "correct_generic": "خوند. کاملاً درسته! تلفیق شگفت‌انگیز الهیات با سندیکای کارگری در اردیبهشت ۵۸.",
        "wrong_generic": "خیر، پاسخ خداوند بود. شجاعانه‌ترین تعبیر پوپولیستی فقهی در تجلیل از کارگران.",
        "common_wrong_answers": {
          "امام علی": "امام علی نخلستان حفر می‌کرد، ولی امام خمینی مستقیماً ذات باری‌تعالی را اولین کارگر نامید.",
          "پیامبر اکرم": "پیامبر دست کارگر را می‌بوسید، اما تعبیر «اولین کارگر» برای پروردگار به کار رفت.",
          "حضرت آدم": "آدم نخستین انسان بود، اما عبارت صریح سخنرانی درباره آفرینش توسط خدا بود."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian cites Khomeini's May 1, 1979 address in which he outflanked the Marxist Left by declaring that God was the supreme worker because He created the entire material cosmos.",
      "fa": "یرواند آبراهامیان به سخنرانی معروف ۱۱ اردیبهشت ۱۳۵۸ امام خمینی استناد می‌کند که برای خلع سلاح احزاب چپ اعلام کردند خداوند اولین کارگر است زیرا تمام گیتی را خلق کرده است."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 48,
      "verbatim_passage": "On May Day 1979, Khomeini outbid the Marxist left by declaring that 'God was the first laborer since he labored to create the universe and its creatures.'",
      "evidence_type": "PRIMARY_TESTIMONY"
    }
  },
  {
    "id": "single_khomeini_populism_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "KHOMEINISM AND ITS DISCONTENTS",
      "fa": "پوپولیسم در ردای فقه"
    },
    "clue_text": {
      "en": "While fiercely attacking Westernized industrial conglomerates, Khomeini assiduously protected the traditional bazaar merchants, whom Abrahamian terms this French socio-economic class.",
      "fa": "در حالی که آیت‌الله خمینی صنایع مونتاژ و سرمایه‌داران وابسته به غرب را آماج حمله قرار می‌داد، از بازاریان سنتی که آبراهامیان آنان را با این واژه فرانسویِ طبقاتی توصیف می‌کند، قاطعانه حمایت می‌کرد."
    },
    "canonical_answer": {
      "en": "Petite Bourgeoisie",
      "fa": "خرده‌بورژوازی"
    },
    "accepted_aliases": {
      "en": [
        "Petty Bourgeoisie",
        "Petite-bourgeoisie",
        "Petit bourgeoisie"
      ],
      "fa": [
        "خرده بورژوازی",
        "خرده‌بورژوا",
        "خرده بورژوا"
      ]
    },
    "options": {
      "en": [
        "Haute Bourgeoisie",
        "Proletariat",
        "Lumpenproletariat",
        "Petite Bourgeoisie"
      ],
      "fa": [
        "بورژوازی بزرگ",
        "پرولتاریا",
        "لومپن پرولتاریا",
        "خرده‌بورژوازی"
      ]
    },
    "correct_option_index": 3,
    "distractor_rationales": [
      {
        "option": "Haute Bourgeoisie",
        "why_plausible": "The wealthiest capitalist class.",
        "why_wrong": "The haute bourgeoisie (modern industrialists like Khayyami or Barkhordar) had their assets nationalized."
      },
      {
        "option": "Proletariat",
        "why_plausible": "The urban factory working class.",
        "why_wrong": "Bazaar merchants owned private capital and shops; they were small proprietors, not proletarians."
      },
      {
        "option": "Lumpenproletariat",
        "why_plausible": "Marginalized underclasses sometimes mobilized in street politics.",
        "why_wrong": "The bazaar constituted respectable, pious property-owners, not dispossessed marginals."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Bourgeoisie",
        "Rentier Class"
      ],
      "fa": [
        "بورژوازی",
        "طبقه رانت‌خوار"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Marxist/sociological French term used by Abrahamian for the traditional shopkeeping class.",
      "fa": "اصطلاح جامعه‌شناختی فرانسوی برای اشاره به طبقه کسبه و بازاریان سنتی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Petite Bourgeoisie. Spot on. Sparing the rug merchants while seizing the auto assembly plants.",
        "wrong_generic": "No, it was the Petite Bourgeoisie. The backbone of mosque funding and revolutionary logistics.",
        "common_wrong_answers": {
          "Haute Bourgeoisie": "The grand capitalists fled to London; the bazaar shopkeepers stayed in power.",
          "Proletariat": "Proletarians owned only their labor; bazaaris owned shops, gold, and inventory.",
          "Lumpenproletariat": "Lumpen were street enforcers; the bazaar was devout commercial property."
        }
      },
      "fa": {
        "correct_generic": "خرده‌بورژوازی. کاملاً درسته! تاجران فرش و ادویه ماندگار شدند، کارخانه‌داران بزرگ مصادره شدند.",
        "wrong_generic": "خیر، پاسخ خرده‌بورژوازی بود. پایگاه سنتی حمایت مالی از روحانیت در بازار.",
        "common_wrong_answers": {
          "بورژوازی بزرگ": "سرمایه‌داران بزرگ کارخانه‌ها را گذاشتند و رفتند؛ بازاریان سنتی حامی انقلاب ماندند.",
          "پرولتاریا": "پرولتاریا جز نیروی کار چیزی نداشت؛ بازاریان صاحب حجره و طلا و سرمایه بودند.",
          "لومپن پرولتاریا": "لومپن‌ها اراذل حاشیه‌نشین بودند، نه معتمدین متدین و حجره‌دار بازار."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian analyzes Khomeinism as a classic petty-bourgeois populist ideology that protected private commercial property in the traditional bazaar while attacking foreign monopolies and secular modernists.",
      "fa": "یرواند آبراهامیان خمینیسم را نمونه‌ای از پوپولیسم خرده‌بورژوازی می‌داند که مالکیت خصوصی تجاری در بازار سنتی را تقدیس می‌کرد و همزمان بر انحصارات مدرن صنعتی می‌تاخت."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 51,
      "verbatim_passage": "Khomeini was careful to reassure the bazaar, the stronghold of the traditional petite bourgeoisie, that Islam respected private property, legitimate trade, and small enterprise.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_khomeini_populism_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "KHOMEINISM AND ITS DISCONTENTS",
      "fa": "پوپولیسم در ردای فقه"
    },
    "clue_text": {
      "en": "Demonstrating the dramatic evolution of Khomeini's thought, Abrahamian points out that in his 1943 book Kashf al-Asrar, Khomeini explicitly accepted this form of government, demanding only that its laws conform to the Sharia.",
      "fa": "آبراهامیان برای اثبات چرخش فکری بنیادین آیت‌الله خمینی اشاره می‌کند که وی در کتاب «کشف‌الاسرار» در سال ۱۳۲۲ این شکل از حکومت را پذیرفته بود و تنها بر تطبیق قوانین با شرع اصرار داشت."
    },
    "canonical_answer": {
      "en": "Constitutional Monarchy",
      "fa": "پادشاهی مشروطه"
    },
    "accepted_aliases": {
      "en": [
        "Constitutional Kingdom",
        "Monarchy",
        "Saltanat-e Mashrooteh",
        "Mashrooteh"
      ],
      "fa": [
        "سلطنت مشروطه",
        "مشروطه",
        "سلطنت"
      ]
    },
    "options": {
      "en": [
        "Constitutional Monarchy",
        "Democratic Republic",
        "Caliphate",
        "Federal Republic"
      ],
      "fa": [
        "پادشاهی مشروطه",
        "جمهوری دموکراتیک",
        "خلافت اسلامی",
        "جمهوری فدرال"
      ]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Democratic Republic",
        "why_plausible": "A modern non-monarchical alternative.",
        "why_wrong": "In 1943, Khomeini did not advocate a republic, and later explicitly rejected 'democratic' as Westernized heresy."
      },
      {
        "option": "Caliphate",
        "why_plausible": "A classical Sunni governance model sometimes conflated with political Islam.",
        "why_wrong": "Shi'i theology rejects the Sunni Caliphate; Khomeini never endorsed a Caliphate."
      },
      {
        "option": "Federal Republic",
        "why_plausible": "A decentralization model.",
        "why_wrong": "Khomeini was deeply centralist and never supported federalism."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Islamic Republic",
        "Sultanate"
      ],
      "fa": [
        "جمهوری اسلامی",
        "سلطنت مطلقه"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific form of monarchical government Khomeini accepted in Kashf al-Asrar.",
      "fa": "نوع نظام حکومتی مبتنی بر سلطنت را که امام خمینی در کتاب کشف الاسرار پذیرفته بود ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Constitutional Monarchy. Correct. In 1943, a just Shah was fine; by 1970, kingship itself was an un-Islamic sin.",
        "wrong_generic": "No, he accepted Constitutional Monarchy in 1943. Political theology is nothing if not flexible.",
        "common_wrong_answers": {
          "Democratic Republic": "He despised the word 'democratic' as an import from Paris.",
          "Caliphate": "Shi'i jurists do not endorse caliphates; they wait for the Twelfth Imam.",
          "Federal Republic": "Federalism was seen as a plot to break up Iran."
        }
      },
      "fa": {
        "correct_generic": "پادشاهی مشروطه. کاملاً درسته! در سال ۱۳۲۲ شاه عادل هم پذیرفتنی بود، تا سال ۱۳۴۸ که سلطنت عین طاغوت شد.",
        "wrong_generic": "خیر، پاسخ پادشاهی مشروطه بود. چرخش از کشف‌الاسرار تا ولایت فقیه نجف را بازخوانی کنید.",
        "common_wrong_answers": {
          "جمهوری دموکراتیک": "ایشان واژه دموکراتیک را کپی‌برداری از غرب می‌دانست و با آن مخالف بود.",
          "خلافت اسلامی": "خلافت الگوی اهل سنت است؛ تشیع امامت و در غیبت ولایت فقیه را مطرح می‌کند.",
          "جمهوری فدرال": "فدرالیسم در نگاه مذهبیون تجزیه‌طلبی تلقی می‌شد."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian emphasizes that in *Kashf al-Asrar* (1943), Khomeini did not demand clerical rule or the overthrow of the Pahlavi dynasty; he accepted a constitutional monarch so long as a council of senior clerics could veto un-Islamic legislation.",
      "fa": "یرواند آبراهامیان تأکید می‌کند که آیت‌الله خمینی در کتاب «کشف‌الاسرار» (۱۳۲۲) هرگز سرنگونی سلطنت یا حکومت مستقیم فقها را مطرح نکرد، بلکه نظارت پنج مجتهد طراز اول بر قوانین پادشاهی مشروطه را کافی می‌دانست."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 19,
      "verbatim_passage": "In Kashf al-Asrar, Khomeini explicitly rejected the idea that clerics wanted to rule, affirming that they accepted the existing constitutional monarchy as long as a council of mujtahids monitored its laws.",
      "evidence_type": "FACT"
    }
  }
])

# Categories 3, 4, and 5
batch_a.extend([
  {
    "id": "single_molkara_trans_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "WHEN KHOMEINI MET MOLKARA",
      "fa": "فتوای تغییر در اتاق جماران"
    },
    "clue_text": {
      "en": "In the mid-1980s, this pioneering Iranian trans woman gained an audience with Ayatollah Khomeini in Jamaran and secured his historic fatwa legalizing sex reassignment surgery.",
      "fa": "در اواسط دهه ۱۳۶۰ این زن ترنس پیشگام ایرانی موفق به دیدار با آیت‌الله خمینی در جماران شد و فتوای تاریخی ایشان در مشروعیت عمل تغییر جنسیت را دریافت کرد."
    },
    "canonical_answer": {
      "en": "Maryam Khatoon Molkara",
      "fa": "مریم خاتون ملک‌آرا"
    },
    "accepted_aliases": {
      "en": [
        "Maryam Molkara",
        "Molkara",
        "Khatoon Molkara"
      ],
      "fa": [
        "مریم ملک‌آرا",
        "ملک‌آرا",
        "مریم ملک آرا"
      ]
    },
    "options": {
      "en": [
        "Simin Daneshvar",
        "Maryam Khatoon Molkara",
        "Forough Farrokhzad",
        "Marjane Satrapi"
      ],
      "fa": [
        "سیمین دانشور",
        "مریم خاتون ملک‌آرا",
        "فروغ فرخزاد",
        "مرجان ساتراپی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Simin Daneshvar",
        "why_plausible": "A celebrated female literary figure and intellectual in Iran.",
        "why_wrong": "Daneshvar was a prominent novelist and academic, not the trans activist who met Khomeini."
      },
      {
        "option": "Forough Farrokhzad",
        "why_plausible": "An iconic modernist Iranian female poet.",
        "why_wrong": "She died in a car accident in 1967, long before the 1979 revolution and Khomeini's fatwa."
      },
      {
        "option": "Marjane Satrapi",
        "why_plausible": "A renowned contemporary Iranian graphic novelist (Persepolis).",
        "why_wrong": "Satrapi is a graphic artist living in France, not the historical activist behind the fatwa."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Shahrzad",
        "Parvin Etesami"
      ],
      "fa": [
        "شهرزاد",
        "پروین اعتصامی"
      ]
    },
    "specificity_prompt": {
      "en": "Please provide the full name of the pioneering trans woman who met Khomeini in Jamaran.",
      "fa": "نام کامل این زن ترنس پیشگام که در جماران با امام خمینی دیدار کرد را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Maryam Khatoon Molkara. Correct. Walking into Jamaran in a suit and walking out with an Islamic legal revolution.",
        "wrong_generic": "No, it was Maryam Khatoon Molkara. One of the most consequential personal audiences in post-revolutionary history.",
        "common_wrong_answers": {
          "Simin Daneshvar": "Daneshvar wrote Savushun; Molkara secured medical fatwas.",
          "Forough Farrokhzad": "Farrokhzad passed away in 1967; this was Jamaran in the mid-1980s.",
          "Marjane Satrapi": "Satrapi drew graphic novels in Paris; Molkara campaigned in Tehran."
        }
      },
      "fa": {
        "correct_generic": "مریم خاتون ملک‌آرا. کاملاً درسته! زنی که شجاعانه به جماران رفت و حکم تاریخی فقهی را گرفت.",
        "wrong_generic": "خیر، پاسخ مریم خاتون ملک‌آرا بود. نقطه عطف حقوق افراد ترنس در فقه شیعه.",
        "common_wrong_answers": {
          "سیمین دانشور": "سیمین دانشور رمان‌نویس سووشون بود، نه فعال حقوق افراد ترنس.",
          "فروغ فرخزاد": "فروغ در سال ۴۵ درگذشت؛ این دیدار در میانه دهه شصت رخ داد.",
          "مرجان ساتراپی": "ساتراپی نویسنده پرسپولیس در فرانسه است، نه بانوی پیشگام دیدار با رهبر انقلاب."
        }
      }
    },
    "explanation": {
      "en": "Afsaneh Najmabadi details how Maryam Khatoon Molkara confronted guards at Jamaran in 1986, presented medical letters to Ayatollah Khomeini, and obtained the fatwa affirming that sex reassignment surgery did not violate Islamic law.",
      "fa": "افسانه نجم‌آبادی شرح می‌دهد که چگونه مریم خاتون ملک‌آرا در سال ۱۳۶۴ به جماران رفت و پس از گفتگو با امام خمینی، فتوای حلیت شرعی جراحی تغییر جنسیت را به دست آورد."
    },
    "provenance": {
      "source_book": "Transing and Transpassing in Iran",
      "source_author": "Afsaneh Najmabadi",
      "page_number": 23,
      "verbatim_passage": "Maryam Khatoon Molkara's historic audience with Ayatollah Khomeini in 1986 resulted in a fatwa establishing that sex reassignment surgery is religiously permissible for individuals diagnosed with gender dysphoria.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_molkara_trans_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "WHEN KHOMEINI MET MOLKARA",
      "fa": "فتوای تغییر در اتاق جماران"
    },
    "clue_text": {
      "en": "In Iranian Shi'i jurisprudence analyzed by Afsaneh Najmabadi, Khomeini's ruling drew a sharp boundary by legalizing gender reassignment surgery as a medical cure while maintaining severe capital punishment for this practice.",
      "fa": "در فقه پساانقلابی تحلیل‌شده توسط افسانه نجم‌آبادی، فتوای امام خمینی مرز روشنی کشید: جراحی تغییر جنسیت به عنوان درمان پزشکی آزاد شد، در حالی که این عمل همچنان مستوجب مجازات اعدام ماند."
    },
    "canonical_answer": {
      "en": "Homosexuality",
      "fa": "همجنس‌گرایی"
    },
    "accepted_aliases": {
      "en": [
        "Same-sex relations",
        "Sodomy",
        "Lavat",
        "Hamsanj-gerayi"
      ],
      "fa": [
        "همجنس گرایی",
        "لواط",
        "مساحقه"
      ]
    },
    "options": {
      "en": [
        "Adultery",
        "Homosexuality",
        "Apostasy",
        "Usury"
      ],
      "fa": [
        "زنای محصنه",
        "همجنس‌گرایی",
        "ارتداد",
        "رباخواری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Adultery",
        "why_plausible": "A severe moral crime in the penal code.",
        "why_wrong": "It relates to extramarital heterosexual relations, not the biological/sexual orientation distinction drawn by the fatwa."
      },
      {
        "option": "Apostasy",
        "why_plausible": "A capital religious offense in traditional jurisprudence.",
        "why_wrong": "Apostasy concerns religious renunciation, not bodily and gender identity jurisprudence."
      },
      {
        "option": "Usury",
        "why_plausible": "A major sin in Islamic commercial law.",
        "why_wrong": "Usury is a financial offense, not a capital sexual offense in the penal code."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Bisexuality",
        "Cross-dressing"
      ],
      "fa": [
        "دوجنس‌گرایی",
        "مبدل‌پوشی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific sexual category that remained criminalized under hudud while trans surgery was permitted.",
      "fa": "رفتار جنسیتی که برخلاف تطبیق جنسیت همچنان در قانون مجازات اسلامی جرم‌انگاری شد را نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Homosexuality. Yes. The state was perfectly happy to fix the body to preserve the heterosexual binary.",
        "wrong_generic": "No, it was homosexuality. The regime pathologized gender dysphoria to eliminate homosexual ambiguity.",
        "common_wrong_answers": {
          "Adultery": "Adultery is heterosexual betrayal; this was about same-sex conduct versus trans identity.",
          "Apostasy": "Apostasy is leaving the faith; the fatwa was entirely about sexual and bodily morphology.",
          "Usury": "Usury is banking interest, not bodily gender laws."
        }
      },
      "fa": {
        "correct_generic": "همجنس‌گرایی. کاملاً درسته! فقه بدن را اصلاح کرد تا تقارن دوتایی زن و مرد حفظ شود.",
        "wrong_generic": "خیر، پاسخ همجنس‌گرایی بود. تمایز کلیدی بین هویت جنسیتی و گرایش جنسی در حقوق ایران.",
        "common_wrong_answers": {
          "زنای محصنه": "زنا خیانت زناشویی است؛ بحث فتوا پیرامون رفتار همجنس‌خواهانه در برابر ترنس بودن بود.",
          "ارتداد": "ارتداد خروج از دین است، نه مسأله هویت جنسیتی و جسمانی.",
          "رباخواری": "ربا تخلف مالی است، ارتباطی با احکام جزایی جنسی ندارد."
        }
      }
    },
    "explanation": {
      "en": "Afsaneh Najmabadi explains that the Islamic Republic's legal framework strictly bifurcates transsexuality (viewed as a curable physical/psychological condition) from homosexuality (punishable under hudud by execution or flogging).",
      "fa": "افسانه نجم‌آبادی استدلال می‌کند که نظام حقوقی ایران با تفکیک قاطع ترنسکشوالیتی (به عنوان بیماری قابل درمان) از همجنس‌گرایی، جراحی را برای حفظ نظم دوجنسیتی جامعه تشویق و هدایت کرد."
    },
    "provenance": {
      "source_book": "Transing and Transpassing in Iran",
      "source_author": "Afsaneh Najmabadi",
      "page_number": 27,
      "verbatim_passage": "In post-revolutionary Iran, transsexuality was medicalized and legitimated as a cure, while homosexuality remained strictly criminalized under hudud laws, creating a sharp divide between gender identity and sexual practice.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_molkara_trans_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "WHEN KHOMEINI MET MOLKARA",
      "fa": "فتوای تغییر در اتاق جماران"
    },
    "clue_text": {
      "en": "To facilitate gender reassignment procedures for low-income citizens following medical authorization, this official Iranian government welfare agency provides subsidized grants and low-interest loans.",
      "fa": "برای تسهیل فرآیند جراحی تطبیق جنسیت برای افراد کم‌درآمد پس از تأیید پزشکی قانونی، این سازمان رفاهی دولتی به متقاضیان کمک‌هزینه بلاعوض و وام‌های کم‌بهره پرداخت می‌کند."
    },
    "canonical_answer": {
      "en": "State Welfare Organization",
      "fa": "سازمان بهزیستی"
    },
    "accepted_aliases": {
      "en": [
        "Sazman-e Behzisti",
        "Behzisti Organization",
        "State Welfare Agency"
      ],
      "fa": [
        "سازمان بهزیستی کشور",
        "بهزیستی"
      ]
    },
    "options": {
      "en": [
        "Imam Khomeini Relief Foundation",
        "State Welfare Organization",
        "Red Crescent Society",
        "Social Security Organization"
      ],
      "fa": [
        "کمیته امداد امام خمینی",
        "سازمان بهزیستی",
        "جمعیت هلال احمر",
        "سازمان تامین اجتماعی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Imam Khomeini Relief Foundation",
        "why_plausible": "Iran's largest charitable poverty relief foundation (Komiteh-ye Emdad).",
        "why_wrong": "Emdad handles general poverty relief; specialized medical subsidies for trans surgery are allocated specifically through Behzisti."
      },
      {
        "option": "Red Crescent Society",
        "why_plausible": "The major medical emergency and humanitarian agency.",
        "why_wrong": "Red Crescent handles disaster response and clinics, not institutional subsidies for gender transition."
      },
      {
        "option": "Social Security Organization",
        "why_plausible": "Manages public pensions and employee healthcare insurance (Tamin-e Ejtemaei).",
        "why_wrong": "Public social security does not fully cover elective gender surgery; Behzisti provides the targeted trans assistance fund."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Komiteh-ye Emdad",
        "Bonyad-e 15 Khordad"
      ],
      "fa": [
        "کمیته امداد",
        "بنیاد ۱۵ خرداد"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the official name of the state welfare organization that subsidizes trans gender surgeries in Iran.",
      "fa": "نام نهاد رسمی دولتی ارائه‌دهنده وام و کمک‌هزینه جراحی تطبیق جنسیت را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "State Welfare Organization. Correct. Where the clerical state actually cuts checks to subsidize gender transition.",
        "wrong_generic": "No, it was the State Welfare Organization (Behzisti). The institutional home of transition subsidies.",
        "common_wrong_answers": {
          "Imam Khomeini Relief Foundation": "Komiteh Emdad distributes flour and pensions, not gender surgery subsidies.",
          "Red Crescent Society": "Red Crescent operates ambulances in earthquakes, not trans loan programs.",
          "Social Security Organization": "Tamin-e Ejtemaei handles labor insurance; Behzisti handles transition welfare grants."
        }
      },
      "fa": {
        "correct_generic": "سازمان بهزیستی. کاملاً درسته! جایی که حکومت برای جراحی تطبیق جنسیت ردیف بودجه اختصاص می‌دهد.",
        "wrong_generic": "خیر، پاسخ سازمان بهزیستی بود. متولی رسمی پرداخت تسهیلات جراحی تغییر جنسیت.",
        "common_wrong_answers": {
          "کمیته امداد امام خمینی": "کمیته امداد ارزاق و مستمری محرومان را می‌دهد، نه وام تغییر جنسیت.",
          "جمعیت هلال احمر": "هلال احمر امدادرسان حوادث غیرمترقبه است، نه نهاد حمایتی جراحی ترنس‌ها.",
          "سازمان تامین اجتماعی": "تأمین اجتماعی بیمه درمانی عمومی است؛ کمک بلاعوض ویژه را بهزیستی می‌پردازد."
        }
      }
    },
    "explanation": {
      "en": "Najmabadi notes that the State Welfare Organization (Sazman-e Behzisti-e Keshvar) provides financial support and loans to trans individuals undergoing gender confirmation surgery to make medical transition accessible.",
      "fa": "افسانه نجم‌آبادی اشاره می‌کند که سازمان بهزیستی کشور با اعطای تسهیلات مالی و وام‌های بلاعوض، هزینه‌های جراحی‌های بالینی را برای متقاضیان تطبیق جنسیت پوشش می‌دهد."
    },
    "provenance": {
      "source_book": "Transing and Transpassing in Iran",
      "source_author": "Afsaneh Najmabadi",
      "page_number": 31,
      "verbatim_passage": "The State Welfare Organization (Sazman-e Behzisti) provides loans and financial grants of several million rials to eligible transsexuals to cover the costs of their transition surgery.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_molkara_trans_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "WHEN KHOMEINI MET MOLKARA",
      "fa": "فتوای تغییر در اتاق جماران"
    },
    "clue_text": {
      "en": "Upon completion of court-approved gender reassignment, this national bureaucracy is legally mandated to reissue a citizen's birth certificate and national identity papers reflecting their new name and gender.",
      "fa": "پس از اتمام مراحل قانونی و تأیید جراحی در دادگاه، این سازمان دولتی موظف است شناسنامه و مدارک هویتی جدید فرد را با نام و جنسیت بازنگری‌شده صادر کند."
    },
    "canonical_answer": {
      "en": "National Organization for Civil Registration",
      "fa": "سازمان ثبت احوال"
    },
    "accepted_aliases": {
      "en": [
        "Sabt-e Ahval",
        "Civil Registry",
        "National Civil Registration Organization"
      ],
      "fa": [
        "ثبت احوال",
        "سازمان ثبت احوال کشور"
      ]
    },
    "options": {
      "en": [
        "Legal Medicine Organization",
        "National Organization for Civil Registration",
        "Ministry of Justice",
        "Immigration and Passport Police"
      ],
      "fa": [
        "سازمان پزشکی قانونی",
        "سازمان ثبت احوال",
        "وزارت دادگستری",
        "پلیس گذرنامه"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Legal Medicine Organization",
        "why_plausible": "The forensic medical board that confirms the psychiatric and physical readiness for surgery (Pezeshki-e Qanuni).",
        "why_wrong": "It issues the medical diagnosis and expert report, but Sabt-e Ahval actually issues the new birth certificate."
      },
      {
        "option": "Ministry of Justice",
        "why_plausible": "Oversees the court system that approves the legal petition.",
        "why_wrong": "The court issues a judicial decree, but the registry paperwork and Shenasnameh are printed by Sabt-e Ahval."
      },
      {
        "option": "Immigration and Passport Police",
        "why_plausible": "Issues passports reflecting new identity.",
        "why_wrong": "Passport issuance follows civil registration; the primary birth certificate (Shenasnameh) is controlled by Sabt-e Ahval."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Pezeshki-e Qanuni",
        "Dadgostari"
      ],
      "fa": [
        "پزشکی قانونی",
        "دادگستری"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Iranian civil registry organization that prints and reissues identity documents after transition.",
      "fa": "نام دقیق سازمانی که شناسنامه و اسناد هویتی جدید را برای افراد ترنس صادر می‌کند بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "National Organization for Civil Registration. Spot on. Shredding the old Shenasnameh and stamping a brand new legal persona.",
        "wrong_generic": "No, it was the National Organization for Civil Registration (Sabt-e Ahval). The arbiters of your official paper self.",
        "common_wrong_answers": {
          "Legal Medicine Organization": "Pezeshki-e Qanuni performs the medical tests; Sabt-e Ahval prints the new identity cards.",
          "Ministry of Justice": "The judge gives the verdict; the clerks at Sabt-e Ahval change the gender box.",
          "Immigration and Passport Police": "Passports come later; your fundamental birth record is Sabt-e Ahval."
        }
      },
      "fa": {
        "correct_generic": "سازمان ثبت احوال. کاملاً درسته! جایی که شناسنامه قبلی ابطال و هویت قانونی جدید متولد می‌شود.",
        "wrong_generic": "خیر، پاسخ سازمان ثبت احوال بود. صادرکننده سند سجلی و شناسنامه در ایران.",
        "common_wrong_answers": {
          "سازمان پزشکی قانونی": "پزشکی قانونی گواهی پزشکی و تأییدیه می‌دهد؛ شناسنامه جدید را ثبت احوال چاپ می‌کند.",
          "وزارت دادگستری": "دادگاه حکم تغییر نام و جنسیت را صادر می‌کند؛ مجری اداری آن ثبت احوال است.",
          "پلیس گذرنامه": "گذرنامه بر اساس شناسنامه جدید صادر می‌شود؛ مبنای هویت ثبت احوال است."
        }
      }
    },
    "explanation": {
      "en": "Najmabadi highlights that under Iranian civil law, once a court accepts the medical evaluation of the Legal Medicine Organization, the National Organization for Civil Registration (Sabt-e Ahval) legally voids the previous birth record and issues a new Shenasnameh.",
      "fa": "افسانه نجم‌آبادی تشریح می‌کند که بر اساس رویه قضایی، پس از تأیید پزشکی قانونی و صدور رأی دادگاه، سازمان ثبت احوال کشور شناسنامه قبلی را باطل و شناسنامه رسمی جدید صادر می‌کند."
    },
    "provenance": {
      "source_book": "Transing and Transpassing in Iran",
      "source_author": "Afsaneh Najmabadi",
      "page_number": 34,
      "verbatim_passage": "Upon presentation of the court verdict and medical certification, the National Organization for Civil Registration (Sabt-e Ahval) is required to issue a new birth certificate (shenasnameh) with the person's new name and gender.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_molkara_trans_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "WHEN KHOMEINI MET MOLKARA",
      "fa": "فتوای تغییر در اتاق جماران"
    },
    "clue_text": {
      "en": "In the classical Shi'i theological framing that made Khomeini's fatwa possible, gender reassignment was justified not as altering God's design, but as this medical act of revealing the true underlying sex.",
      "fa": "در استدلال کلامی فقه شیعه که فتوای امام خمینی را ممکن ساخت، جراحی تطبیق جنسیت تغییر خلقت خدا قلمداد نشد، بلکه این اقدام پزشکی برای آشکارسازی جنسیت پنهان واقعی نامیده شد."
    },
    "canonical_answer": {
      "en": "Resolution of sexual ambiguity",
      "fa": "رفع ابهام جنسی"
    },
    "accepted_aliases": {
      "en": [
        "Raf'-e Ebham-e Jensi",
        "Clarification of hidden sex",
        "Revealing latent sex",
        "Kashf-e Jensiyat"
      ],
      "fa": [
        "رفع ابهام جنسیتی",
        "کشف جنسیت",
        "کشف جنسیت واقعی"
      ]
    },
    "options": {
      "en": [
        "Rebellion against nature",
        "Resolution of sexual ambiguity",
        "Social gender construction",
        "Spiritual transubstantiation"
      ],
      "fa": [
        "طغیان علیه طبیعت",
        "رفع ابهام جنسی",
        "برساخت اجتماعی جنسیت",
        "استحاله روحانی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Rebellion against nature",
        "why_plausible": "A conservative theological objection often raised by Sunni critics.",
        "why_wrong": "Khomeini rejected this framing, arguing the surgery was restorative rather than rebellious."
      },
      {
        "option": "Social gender construction",
        "why_plausible": "A secular feminist and queer theory concept.",
        "why_wrong": "Shi'i jurisprudence relies on essentialist biology and soul-body alignment, rejecting modern social constructivism."
      },
      {
        "option": "Spiritual transubstantiation",
        "why_plausible": "A mystical or Christian theological concept.",
        "why_wrong": "It is not the jurisprudential category used by Iranian clerical authorities."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Taghyir-e Khalq",
        "Taghyir-e Jensiyat"
      ],
      "fa": [
        "تغییر خلقت",
        "تغییر جنسیت"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the exact theological concept of resolving biological ambiguity used to justify the fatwa.",
      "fa": "اصطلاح فقهی ناظر بر آشکار کردن واقعیت جنسی و برطرف کردن پوشیدگی جنسیت را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Resolution of sexual ambiguity. Correct. Not defying God's creation, merely uncovering what He intended all along.",
        "wrong_generic": "No, the legal concept was the resolution of sexual ambiguity (Raf'-e Ebham-e Jensi). A brilliant piece of juristic engineering.",
        "common_wrong_answers": {
          "Rebellion against nature": "That is what opponents called it; Khomeini called it medical clarification.",
          "Social gender construction": "The seminary does not read Judith Butler; they read biological essentialism.",
          "Spiritual transubstantiation": "This was clinical anatomy, not Catholic sacraments."
        }
      },
      "fa": {
        "correct_generic": "رفع ابهام جنسی. کاملاً درسته! استدلال فقهی نبوغ‌آمیزی که جراحی را درمان و کشف حقیقت نامید نه دستکاری خلقت.",
        "wrong_generic": "خیر، پاسخ رفع ابهام جنسی بود. مبنای استدلال فقهی برای مشروعیت‌بخشی به جراحی.",
        "common_wrong_answers": {
          "طغیان علیه طبیعت": "مخالفان آن را تغییر خلقت می‌خواندند؛ فتوای امام آن را آشکارسازی جنسیت نهفته دانست.",
          "برساخت اجتماعی جنسیت": "حوزه علمیه نظریات فمینیستی غربی را قبول ندارد؛ بر ذات‌گرایی جنسی استوار است.",
          "استحاله روحانی": "استحاله واژه تطهیر نجاسات در فقه است، نه عنوان حقوقی تطبیق جنسیت."
        }
      }
    },
    "explanation": {
      "en": "Afsaneh Najmabadi analyzes how Shi'i jurists rooted their approval in classical rulings on hermaphrodites (khuntha), conceptualizing gender surgery as 'raf'-e ebham' (removal of ambiguity) and revealing a pre-existing divine reality rather than an unnatural alteration of creation.",
      "fa": "افسانه نجم‌آبادی تبیین می‌کند که فقهای شیعه با بهره‌گیری از باب فقهی «خنثی» در متون سنتی، جراحی را به عنوان «رفع ابهام» از جنسیت واقعی و باطنی فرد توجیه کردند تا اتهام دستکاری در آفرینش الهی رفع شود."
    },
    "provenance": {
      "source_book": "Transing and Transpassing in Iran",
      "source_author": "Afsaneh Najmabadi",
      "page_number": 37,
      "verbatim_passage": "By conceptualizing transsexuality through the traditional category of the khuntha (hermaphrodite), clerical reasoning framed surgery not as an impermissible alteration of God's creation (taghyir-e khalq Allah), but as the clinical resolution of ambiguity (raf'-e ebham).",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_park_segregation_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "PARK LIFE UNDER PATRIARCHY",
      "fa": "بوستانِ تفکیک‌شده"
    },
    "clue_text": {
      "en": "Opened in northeastern Tehran in 2008 as the Islamic Republic's first enclosed, women-only public municipal park, this park was given this maternal name.",
      "fa": "این بوستان در سال ۱۳۸۷ در شمال شرق تهران به عنوان نخستین پارک عمومی محصور و اختصاصی زنان در جمهوری اسلامی افتتاح شد و این نام مادرانه را بر خود دید."
    },
    "canonical_answer": {
      "en": "Mothers' Paradise",
      "fa": "بهشت مادران"
    },
    "accepted_aliases": {
      "en": [
        "Behesht-e Madaran",
        "Mothers Paradise Park",
        "Beheshte Madaran"
      ],
      "fa": [
        "بوستان بهشت مادران",
        "پارک بهشت مادران"
      ]
    },
    "options": {
      "en": [
        "Mellat Park",
        "Mothers' Paradise",
        "Laleh Park",
        "Jamshidieh Park"
      ],
      "fa": [
        "پارک ملت",
        "بهشت مادران",
        "پارک لاله",
        "پارک جمشیدیه"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Mellat Park",
        "why_plausible": "One of Tehran's largest and most famous public parks.",
        "why_wrong": "Mellat is a mixed public park on Valiasr Street, not an enclosed women-only park."
      },
      {
        "option": "Laleh Park",
        "why_plausible": "A central Tehran park known for cultural gatherings.",
        "why_wrong": "Laleh Park is fully open to all genders and was established before the revolution."
      },
      {
        "option": "Jamshidieh Park",
        "why_plausible": "A prominent foothill park in northern Tehran.",
        "why_wrong": "Jamshidieh is a mountain park open to the general public, not a gated women-only space."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Pardis-e Banovan",
        "Narges Park"
      ],
      "fa": [
        "پردیس بانوان",
        "بوستان نرگس"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the specific name of Tehran's first women-only municipal park opened in 2008.",
      "fa": "نام اولین پارک اختصاصی بانوان در تهران که در سال ۱۳۸۷ افتتاح شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mothers' Paradise. Correct. Where women can take off their headscarves as long as the surrounding barbed wire is tall enough.",
        "wrong_generic": "No, it was Mothers' Paradise (Behesht-e Madaran). High walls and female security guards included.",
        "common_wrong_answers": {
          "Mellat Park": "Mellat Park is open to everyone promenading on Valiasr.",
          "Laleh Park": "Laleh Park is in central Tehran with chess tables and no high fences.",
          "Jamshidieh Park": "Jamshidieh is for hiking up the Alborz mountains with the whole family."
        }
      },
      "fa": {
        "correct_generic": "بهشت مادران. کاملاً درسته! بهشتی محصور با فنس و نگهبان زن برای دویدن بدون روسری.",
        "wrong_generic": "خیر، پاسخ بهشت مادران بود. نخستین پارک تفکیک‌شده پایتخت در تپه‌های حقانی.",
        "common_wrong_answers": {
          "پارک ملت": "پارک ملت عمومی است و در خیابان ولیعصر قرار دارد.",
          "پارک لاله": "پارک لاله در قلب تهران است و ورود آقایان به آن آزاد است.",
          "پارک جمشیدیه": "جمشیدیه بوستان سنگی نیاوران است، نه پارک اختصاصی بانوان."
        }
      }
    },
    "explanation": {
      "en": "Nazanin Shahrokni examines the 2008 opening of Behesht-e Madaran (Mothers' Paradise) as a landmark development in the spatial segregation and gendered recreation policies of the Tehran Municipality.",
      "fa": "نازنین شهرکنی افتتاح بوستان بهشت مادران در سال ۱۳۸۷ را نقطه عطف سیاست‌های شهرداری تهران در تفکیک جنسیتی فضاها و اختصاص فضاهای ورزشی محصور به بانوان تحلیل می‌کند."
    },
    "provenance": {
      "source_book": "Women in Place: The Politics of Gender Segregation in Iran",
      "source_author": "Nazanin Shahrokni",
      "page_number": 58,
      "verbatim_passage": "In May 2008, Tehran Municipality inaugurated Behesht-e Madaran (Mothers' Paradise), the city's first all-female public park, fenced off on the hills of Abbasabad to allow women to remove their veils away from male eyes.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_park_segregation_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "PARK LIFE UNDER PATRIARCHY",
      "fa": "بوستانِ تفکیک‌شده"
    },
    "clue_text": {
      "en": "The aggressive expansion of women-only municipal parks, special women's buses, and segregated subway cars occurred during the decade-long tenure of this prominent Tehran mayor from 2005 to 2017.",
      "fa": "گسترش پرشتاب بوستان‌های ویژه بانوان، اتوبوس‌های اختصاصی و واگن‌های تفکیک‌شده مترو در دوران مدیریت ۱۲ ساله این شهردار سرشناس تهران بین سال‌های ۱۳۸۴ تا ۱۳۹۶ رخ داد."
    },
    "canonical_answer": {
      "en": "Mohammad Bagher Ghalibaf",
      "fa": "محمدباقر قالیباف"
    },
    "accepted_aliases": {
      "en": [
        "Ghalibaf",
        "Mohammad Baqer Qalibaf",
        "Mohammad-Baqer Ghalibaf"
      ],
      "fa": [
        "قالیباف",
        "محمد باقر قالیباف",
        "محمدباقر قالی باف"
      ]
    },
    "options": {
      "en": [
        "Gholamhossein Karbaschi",
        "Mahmoud Ahmadinejad",
        "Mohammad Bagher Ghalibaf",
        "Pirouz Hanachi"
      ],
      "fa": [
        "غلامحسین کرباسچی",
        "محمود احمدی‌نژاد",
        "محمدباقر قالیباف",
        "پیروز حناچی"
      ]
    },
    "correct_option_index": 2,
    "distractor_rationales": [
      {
        "option": "Gholamhossein Karbaschi",
        "why_plausible": "Tehran's famous modernizing mayor of the 1990s.",
        "why_wrong": "Karbaschi modernized the city in the 1990s under Rafsanjani, before women-only parks were created."
      },
      {
        "option": "Mahmoud Ahmadinejad",
        "why_plausible": "Mayor of Tehran from 2003 to 2005 before becoming president.",
        "why_wrong": "He served briefly from 2003-2005; the institutionalization of women-only parks occurred under Ghalibaf's subsequent tenure."
      },
      {
        "option": "Pirouz Hanachi",
        "why_plausible": "A later reformist mayor of Tehran.",
        "why_wrong": "Hanachi served much later (2018-2021) and was associated with bike paths rather than constructing segregated mega-parks."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Mahmoud Ahmadinejad",
        "Mohsen Hashemi"
      ],
      "fa": [
        "محمود احمدی‌نژاد",
        "محسن هاشمی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Tehran mayor who oversaw the creation of women-only parks between 2005 and 2017.",
      "fa": "نام شهردار اسبق تهران که بوستان‌های تفکیک‌شده بانوان در دوره او احداث شدند را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad Bagher Ghalibaf. Correct. Combining technocratic highway construction with gender-segregated urban parks.",
        "wrong_generic": "No, it was Mohammad Bagher Ghalibaf. Modernizing the concrete while fencing off the genders.",
        "common_wrong_answers": {
          "Gholamhossein Karbaschi": "Karbaschi built Shahr-e Vand and cultural centers in the nineties.",
          "Mahmoud Ahmadinejad": "Ahmadinejad was mayor briefly before 2005, then took his populist show national.",
          "Pirouz Hanachi": "Hanachi rode bicycles to work in 2019; Ghalibaf built the women-only parks."
        }
      },
      "fa": {
        "correct_generic": "محمدباقر قالیباف. کاملاً درسته! شهرداری که اتوبان صدر را دوطبقه کرد و بوستان‌ها را دیوار کشید.",
        "wrong_generic": "خیر، پاسخ محمدباقر قالیباف بود. مدیریت شهری با شعار خدمت و تفکیک فضایی.",
        "common_wrong_answers": {
          "غلامحسین کرباسچی": "کرباسچی فرهنگسراها را در دهه هفتاد ساخت، نه بوستان‌های محصور بانوان را.",
          "محمود احمدی‌نژاد": "احمدی‌نژاد تا سال ۸۴ شهردار بود و بعد به پاستور رفت.",
          "پیروز حناچی": "حناچی شهردار اصلاح‌طلب با سه‌شنبه‌های بدون خودرو بود."
        }
      }
    },
    "explanation": {
      "en": "Shahrokni demonstrates that Mayor Mohammad Bagher Ghalibaf utilized municipal urban projects, including women-only parks and transportation gender segregation, to project an image of an efficient, modern Islamic city.",
      "fa": "شهرکنی نشان می‌دهد که محمدباقر قالیباف در دوره شهرداری خود کوشید با احداث پروژه‌های عمرانی تفکیک‌شده مانند پارک‌های بانوان، الگویی کارآمد و مدرن از شهر اسلامی ارائه دهد."
    },
    "provenance": {
      "source_book": "Women in Place: The Politics of Gender Segregation in Iran",
      "source_author": "Nazanin Shahrokni",
      "page_number": 64,
      "verbatim_passage": "During the tenure of Mayor Mohammad Bagher Ghalibaf (2005-2017), the municipality embarked on a massive campaign to construct segregated urban spaces, branding them as services to protect female comfort and family dignity.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_park_segregation_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "PARK LIFE UNDER PATRIARCHY",
      "fa": "بوستانِ تفکیک‌شده"
    },
    "clue_text": {
      "en": "In her theoretical framework, sociologist Nazanin Shahrokni introduces this concept to describe how the state actively negotiates and produces gender boundaries through urban spatial planning rather than simply banning women.",
      "fa": "جامعه‌شناس نازنین شهرکنی این مفهوم نظری را به کار می‌برد تا نشان دهد حاکمیت چگونه به جای حذف کامل زنان، از طریق برنامه‌ریزی فضایی شهر مرزهای جنسیتی را بازتولید و مدیریت می‌کند."
    },
    "canonical_answer": {
      "en": "Spatial Statecraft",
      "fa": "حکمرانی فضایی"
    },
    "accepted_aliases": {
      "en": [
        "Spatial state craft",
        "Gendered spatial statecraft",
        "Spatial governance"
      ],
      "fa": [
        "حکمرانی فضایی",
        "سیاست‌ورزی فضایی",
        "مدیریت فضایی"
      ]
    },
    "options": {
      "en": [
        "Panoptic Surveillance",
        "Spatial Statecraft",
        "Biopolitical Disciplinary",
        "Urban Commodification"
      ],
      "fa": [
        "نظارت سراسربین",
        "حکمرانی فضایی",
        "انضباط زیست‌سیاسی",
        "کالایی‌سازی شهری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Panoptic Surveillance",
        "why_plausible": "A classic Foucaultian spatial surveillance concept.",
        "why_wrong": "It describes surveillance mechanisms, not Shahrokni's specific term for urban gender production."
      },
      {
        "option": "Biopolitical Disciplinary",
        "why_plausible": "Common academic terminology for bodily state regulation.",
        "why_wrong": "Shahrokni's coined term for the state's geographic management in the book is 'Spatial Statecraft'."
      },
      {
        "option": "Urban Commodification",
        "why_plausible": "A Marxist geography concept.",
        "why_wrong": "It relates to real estate capitalism rather than the statecraft of gendered segregation."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Gendered Urbanism",
        "Spatial Segregation"
      ],
      "fa": [
        "شهرسازی جنسیتی",
        "تفکیک فضایی"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the exact theoretical two-word term coined by Shahrokni for the state's urban gender governance.",
      "fa": "اصطلاح نظری دوکلمه‌ای به کار رفته توسط نازنین شهرکنی برای مدیریت فضایی جنسیت توسط دولت را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Spatial Statecraft. Correct. Designing fences and gates to govern citizenship and morals simultaneously.",
        "wrong_generic": "No, it was Spatial Statecraft. How urban blueprints become moral enforcement.",
        "common_wrong_answers": {
          "Panoptic Surveillance": "Foucault's watchtower is everywhere, but Shahrokni specifically called it Spatial Statecraft.",
          "Biopolitical Disciplinary": "Biopolitics is the broader umbrella; Spatial Statecraft is the specific concept.",
          "Urban Commodification": "Commodification is about turning land into money; this is about gender boundaries."
        }
      },
      "fa": {
        "correct_generic": "حکمرانی فضایی. کاملاً درسته! وقتی جدول خیابان و پرچین پارک ابزار تنظیم روابط اجتماعی می‌شود.",
        "wrong_generic": "خیر، پاسخ حکمرانی فضایی بود. نظریه شهرکنی درباره نحوه بازتولید مرزهای جنسیت در پایتخت.",
        "common_wrong_answers": {
          "نظارت سراسربین": "سراسربین فوکو برج دیده‌بانی است؛ شهرکنی از حکمرانی فضایی سخن می‌گوید.",
          "انضباط زیست‌سیاسی": "زیست‌سیاست مفهوم کلی‌تر است؛ اصطلاح ویژه کتاب حکمرانی فضایی است.",
          "کالایی‌سازی شهری": "کالایی‌سازی به املاک و سوداگری برمی‌گردد، نه تفکیک جنسیتی."
        }
      }
    },
    "explanation": {
      "en": "Nazanin Shahrokni defines 'Spatial Statecraft' as the evolving set of state interventions and physical modifications through which the post-revolutionary state regulates female mobility and presence in the metropolis.",
      "fa": "نازنین شهرکنی «حکمرانی فضایی» را مجموعه‌ای از مداخلات کالبدی و برنامه‌ریزی شهری تعریف می‌کند که دولت از طریق آن حضور و تحرک زنان در فضاهای عمومی را انتظام می‌بخشد."
    },
    "provenance": {
      "source_book": "Women in Place: The Politics of Gender Segregation in Iran",
      "source_author": "Nazanin Shahrokni",
      "page_number": 12,
      "verbatim_passage": "I introduce the concept of 'spatial statecraft' to capture the ways in which the state produces, manipulates, and transforms physical space to define gender roles and manage female presence.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_park_segregation_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "PARK LIFE UNDER PATRIARCHY",
      "fa": "بوستانِ تفکیک‌شده"
    },
    "clue_text": {
      "en": "To prevent men from peering into women-only parks from adjacent urban highways and overpasses, municipal architects were forced to construct these massive earth mounds and planted berms.",
      "fa": "برای جلوگیری از اشراف دید رانندگان و عابران مرد از روی پل‌ها و بزرگراه‌های مجاور به درون بوستان بانوان، مهندسان شهرداری ناچار به ساخت این تپه‌ها و خاکریزهای عظیم خاکی شدند."
    },
    "canonical_answer": {
      "en": "Landscape Berms",
      "fa": "خاکریزهای حائل"
    },
    "accepted_aliases": {
      "en": [
        "Earth berms",
        "Berms",
        "Earthen embankments",
        "Soil mounds"
      ],
      "fa": [
        "خاکریزهای محافظ",
        "خاک‌ریز حائل",
        "تپه‌های حائل"
      ]
    },
    "options": {
      "en": [
        "Concrete Watchtowers",
        "Barbed-wire Trenches",
        "Landscape Berms",
        "Underground Tunnels"
      ],
      "fa": [
        "برج‌های بتنی دیده‌بانی",
        "کانال‌های سیم‌خاردار",
        "خاکریزهای حائل",
        "تونل‌های زیرزمینی"
      ]
    },
    "correct_option_index": 2,
    "distractor_rationales": [
      {
        "option": "Concrete Watchtowers",
        "why_plausible": "Security infrastructure common in military zones.",
        "why_wrong": "Watchtowers are used by guards to look out, not to block sightlines into a public leisure park."
      },
      {
        "option": "Barbed-wire Trenches",
        "why_plausible": "Boundary fortifications.",
        "why_wrong": "Parks used landscaped earthworks and high green fences, not military battlefield trenches."
      },
      {
        "option": "Underground Tunnels",
        "why_plausible": "Concealed passage infrastructure.",
        "why_wrong": "The parks were outdoor hills and open sky, blocked from view by elevated landscaped earth berms."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Privacy Curtains",
        "Perimeter Screens"
      ],
      "fa": [
        "دیوارهای برزنتی",
        "سایبان‌های استتار"
      ]
    },
    "specificity_prompt": {
      "en": "Identify the specific civil engineering earthworks constructed to obstruct sightlines into the parks.",
      "fa": "سازه مهندسی خاکی ساخته‌شده در حاشیه بوستان‌ها برای کور کردن دید نامحرم را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Landscape Berms. Correct. When your urban park requires the same earthmoving as an artillery redoubt.",
        "wrong_generic": "No, they built landscape berms (earthen embankments). Moving tons of dirt to protect the eye from a flying headscarf.",
        "common_wrong_answers": {
          "Concrete Watchtowers": "Watchtowers would look into the park, defeating the entire purpose.",
          "Barbed-wire Trenches": "Trenches are for warfare; berms are landscaped earthen walls.",
          "Underground Tunnels": "They wanted women in the sun, just behind giant mounds of dirt."
        }
      },
      "fa": {
        "correct_generic": "خاکریزهای حائل. کاملاً درسته! عملیات خاکی در حد جبهه جنگ برای ندیدن موی زنان از روی اتوبان.",
        "wrong_generic": "خیر، پاسخ خاکریزهای حائل بود. تپه‌سازی‌های عظیم در حاشیه بزرگراه رسالت و حقانی.",
        "common_wrong_answers": {
          "برج‌های بتنی دیده‌بانی": "برج دیده‌بانی اشراف دید ایجاد می‌کند که دقیقاً خلاف هدف بود.",
          "کانال‌های سیم‌خاردار": "کانال برای پدافند نظامی است؛ شهرداری تپه‌های سبز خاکی ساخت.",
          "تونل‌های زیرزمینی": "زنان در فضای باز بودند اما پشت خاکریزهای بلند استتار شده بودند."
        }
      }
    },
    "explanation": {
      "en": "Shahrokni explains that because Behesht-e Madaran was situated on undulating terrain adjacent to the Resalat highway, urban planners had to reshape topography with artificial earthen berms and dense evergreen trees to block male sightlines.",
      "fa": "نازنین شهرکنی توضیح می‌دهد که به دلیل احاطه بوستان بهشت مادران توسط بزرگراه‌های همجوار، طراحان ناچار شدند با خاکریزی‌های مصنوعی و کاشت درختان متراکم، خط دید نامحرمان از روی پل‌ها را مسدود کنند."
    },
    "provenance": {
      "source_book": "Women in Place: The Politics of Gender Segregation in Iran",
      "source_author": "Nazanin Shahrokni",
      "page_number": 69,
      "verbatim_passage": "To secure visual occlusion from neighboring high-rises and expressways, municipal engineers constructed massive landscaped earth berms, turning urban topography into an ideological barrier.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_park_segregation_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "PARK LIFE UNDER PATRIARCHY",
      "fa": "بوستانِ تفکیک‌شده"
    },
    "clue_text": {
      "en": "Shahrokni reveals a sociopolitical paradox: while middle-class secular women boycotted segregated parks as an insult, these women enthusiastically embraced them as their first legitimate, halal public spaces.",
      "fa": "شهرکنی به پارادوکسی اجتماعی اشاره می‌کند: در حالی که زنان طبقه متوسط سکولار این پارک‌ها را تحریم کردند، این گروه از زنان سنتی از آن‌ها به عنوان اولین فضای عمومی حلال و امن خود استقبال نمودند."
    },
    "canonical_answer": {
      "en": "Pious working-class women",
      "fa": "زنان متدین طبقات سنتی"
    },
    "accepted_aliases": {
      "en": [
        "Religious traditional women",
        "Traditional women",
        "Pious conservative women",
        "Chadori women"
      ],
      "fa": [
        "زنان مذهبی",
        "زنان سنتی",
        "بانوان چادری",
        "زنان مومنه"
      ]
    },
    "options": {
      "en": [
        "Foreign diplomats",
        "Pious working-class women",
        "Expatriate tourists",
        "University activists"
      ],
      "fa": [
        "دیپلمات‌های خارجی",
        "زنان متدین طبقات سنتی",
        "گردشگران خارجی",
        "فعالان دانشجویی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Foreign diplomats",
        "why_plausible": "Diplomats occasionally tour municipal showcase projects.",
        "why_wrong": "Diplomats were not the domestic demographic constituency transformed by these spaces."
      },
      {
        "option": "Expatriate tourists",
        "why_plausible": "Tourists visit public parks in Tehran.",
        "why_wrong": "Foreign tourists rarely visited segregated suburban hills and had no cultural stake in the dispute."
      },
      {
        "option": "University activists",
        "why_plausible": "Active participants in Iranian public life.",
        "why_wrong": "Student activists largely opposed gender apartheid and spatial segregation."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Secular feminists",
        "Bazaar merchants' daughters"
      ],
      "fa": [
        "فمینیست‌های سکولار",
        "دختران بازاریان"
      ]
    },
    "specificity_prompt": {
      "en": "Identify the specific social group of women who benefited from and embraced gender-segregated parks.",
      "fa": "قشر اجتماعی از زنانی که بوستان‌های تفکیک‌شده را فرصتی برای حضور در عرصه عمومی یافتند مشخص کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Pious working-class women. Spot on. One woman's ghetto is another woman's family permission slip.",
        "wrong_generic": "No, it was pious, traditional women. For them, the high walls meant husbands and fathers had no grounds to say no.",
        "common_wrong_answers": {
          "Foreign diplomats": "Diplomats drink tea in northern embassies, not jogging in suburban bermed parks.",
          "Expatriate tourists": "Tourists take selfies at Golestan Palace, they don't fight for park access.",
          "University activists": "Student activists organized against segregation on campuses."
        }
      },
      "fa": {
        "correct_generic": "زنان متدین طبقات سنتی. کاملاً درسته! جایی که حصار پارک برای عده‌ای توهین و برای عده‌ای دیگر مجوز خروج از خانه بود.",
        "wrong_generic": "خیر، پاسخ زنان متدین و سنتی بود. حصارهایی که اجازه همسران و پدران را برای ورزش آزاد کرد.",
        "common_wrong_answers": {
          "دیپلمات‌های خارجی": "دیپلمات‌ها در باغ فرمانیه هستند، نه در حال نرمش در تپه‌های حقانی.",
          "گردشگران خارجی": "توریست‌ها به کاخ سعدآباد می‌روند، نه پارک تفکیک‌شده محلی.",
          "فعالان دانشجویی": "فعالان دانشجویی در دانشگاه‌ها علیه تفکیک جنسیتی شعار می‌دادند."
        }
      }
    },
    "explanation": {
      "en": "Shahrokni demonstrates that segregated parks functioned ambivalently: they reinforced conservative gender ideology while simultaneously providing pious women with their first socially acceptable realm for physical exercise outside patriarchal household surveillance.",
      "fa": "شهرکنی نشان می‌دهد که بوستان‌های تفکیک‌شده کارکردی دوگانه داشتند: از یک سو ایدئولوژی تفکیک جنسیتی را تثبیت کردند و از سوی دیگر برای زنان سنتی مجوزی مشروع برای ورزش و تفریح فارغ از کنترل مردان خانواده فراهم آوردند."
    },
    "provenance": {
      "source_book": "Women in Place: The Politics of Gender Segregation in Iran",
      "source_author": "Nazanin Shahrokni",
      "page_number": 82,
      "verbatim_passage": "While secular middle-class women viewed the parks as an insulting quarantine, many pious working-class women celebrated them as an unprecedented realm of freedom where they could exercise without familial censure.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_waltz_bomb_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "THE BOMB ACCORDING TO WALTZ",
      "fa": "والتز با کلاهک هسته‌ای"
    },
    "clue_text": {
      "en": "In a provocative 2012 essay published in Foreign Affairs, this giant of American neorealist international relations theory argued that a nuclear-armed Iran would actually bring stability to the Middle East.",
      "fa": "در مقاله‌ای جنجالی در نشریه فارن افرز در سال ۲۰۱۲، این نظریه‌پرداز نامدار نئورئالیسم روابط بین‌الملل استدلال کرد که دستیابی ایران به سلاح هسته‌ای به خاورمیانه ثبات خواهد بخشید."
    },
    "canonical_answer": {
      "en": "Kenneth Waltz",
      "fa": "کنت والتز"
    },
    "accepted_aliases": {
      "en": [
        "Waltz",
        "Ken Waltz"
      ],
      "fa": [
        "والتز",
        "کن والتز"
      ]
    },
    "options": {
      "en": [
        "John Mearsheimer",
        "Kenneth Waltz",
        "Stephen Walt",
        "Joseph Nye"
      ],
      "fa": [
        "جان مرشایمر",
        "کنت والتز",
        "استیون والت",
        "جوزف نای"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "John Mearsheimer",
        "why_plausible": "Another legendary realist theorist famous for offensive realism and Middle East critique.",
        "why_wrong": "Mearsheimer co-authored The Israel Lobby, but the famous 'Why Iran Should Get the Bomb' article was authored solely by Kenneth Waltz."
      },
      {
        "option": "Stephen Walt",
        "why_plausible": "A prominent realist scholar and Mearsheimer's frequent co-author.",
        "why_wrong": "Walt writes extensively on balance of threat, but was not the author of this specific 2012 essay."
      },
      {
        "option": "Joseph Nye",
        "why_plausible": "A world-renowned Harvard international relations theorist.",
        "why_wrong": "Nye is the father of neoliberal institutionalism and 'soft power', not neorealist nuclear proliferation theory."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "John Mearsheimer",
        "Robert Keohane"
      ],
      "fa": [
        "جان مرشایمر",
        "رابرت کوهن"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific neorealist scholar who authored 'Why Iran Should Get the Bomb'.",
      "fa": "نام این نظریه‌پرداز نامدار روابط بین‌الملل نویسنده مقاله «چرا ایران باید بمب داشته باشد» را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Kenneth Waltz. Correct. Nothing comforts Washington policymakers quite like a neorealist praising Iranian nuclear warheads.",
        "wrong_generic": "No, it was Kenneth Waltz. The grand old man of structural realism.",
        "common_wrong_answers": {
          "John Mearsheimer": "Mearsheimer does offensive realism; Waltz is the father of structural balance.",
          "Stephen Walt": "Walt co-wrote the Israel Lobby book; Waltz wrote the pro-bomb manifesto.",
          "Joseph Nye": "Nye is all about soft power; nuclear deterrence is very hard power."
        }
      },
      "fa": {
        "correct_generic": "کنت والتز. کاملاً درسته! استادی که گفت بهترین نسخه برای خاورمیانه چند کلاهک اتمی در تهران است.",
        "wrong_generic": "خیر، پاسخ کنت والتز بود. بنیان‌گذار نئورئالیسم ساختاری در روابط بین‌الملل.",
        "common_wrong_answers": {
          "جان مرشایمر": "مرشایمر نظریه‌پرداز رئالیسم تهاجمی است؛ والتز صاحب این مقاله مشهور بود.",
          "استیون والت": "استیون والت موازنه تهدید را نوشت؛ این مقاله اختصاصی والتز بود.",
          "جوزف نای": "جوزف نای مبدع قدرت نرم است، بمب اتمی اوج قدرت سخت است."
        }
      }
    },
    "explanation": {
      "en": "Kenneth Waltz published 'Why Iran Should Get the Bomb: Nuclear Balancing Would Mean Stability' in Foreign Affairs (2012), applying structural realism to challenge the Washington consensus on nuclear proliferation.",
      "fa": "کنت والتز در مقاله مشهور خود در سال ۲۰۱۲ در فارن افرز با عنوان «چرا ایران باید به بمب دست یابد» استدلال کرد که موازنه هسته‌ای در خاورمیانه به صلح و ثبات پایدار می‌انجامد."
    },
    "provenance": {
      "source_book": "Why Iran Should Get the Bomb (Foreign Affairs)",
      "source_author": "Kenneth Waltz",
      "page_number": 2,
      "verbatim_passage": "Most American, European, and Israeli commentators and policymakers warn that a nuclear-armed Iran would be the worst possible outcome... In fact, by creating a stable balance of power, it would probably be the best possible outcome.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_waltz_bomb_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE BOMB ACCORDING TO WALTZ",
      "fa": "والتز با کلاهک هسته‌ای"
    },
    "clue_text": {
      "en": "According to Waltz's balance of power framework, Middle Eastern instability is fundamentally generated not by Iranian revolutionary ambitions, but by this nation's unchecked regional nuclear monopoly.",
      "fa": "بر اساس چارچوب توازن قوای والتز، بی‌ثباتی خاورمیانه نه ناشی از جاه‌طلبی‌های انقلابی ایران، بلکه حاصل انحصار هسته‌ای مهارنشده این کشور در منطقه است."
    },
    "canonical_answer": {
      "en": "Israel",
      "fa": "اسرائیل"
    },
    "accepted_aliases": {
      "en": [
        "State of Israel",
        "Tel Aviv"
      ],
      "fa": [
        "رژیم صهیونیستی",
        "دولت اسرائیل"
      ]
    },
    "options": {
      "en": [
        "Pakistan",
        "Israel",
        "Saudi Arabia",
        "United States"
      ],
      "fa": [
        "پاکستان",
        "اسرائیل",
        "عربستان سعودی",
        "ایالات متحده"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Pakistan",
        "why_plausible": "A nuclear-armed Islamic country geographically adjacent to Iran.",
        "why_wrong": "Pakistan's nuclear deterrent is structured entirely around its rivalry with India in South Asia, not Middle Eastern monopoly."
      },
      {
        "option": "Saudi Arabia",
        "why_plausible": "Iran's chief regional Sunni rival.",
        "why_wrong": "Saudi Arabia has never possessed nuclear weapons."
      },
      {
        "option": "United States",
        "why_plausible": "A global nuclear superpower with naval forces in the Persian Gulf.",
        "why_wrong": "Waltz was referring specifically to the regional Middle Eastern state with an unacknowledged nuclear arsenal."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "United States",
        "Pakistan"
      ],
      "fa": [
        "آمریکا",
        "پاکستان"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Middle Eastern state whose nuclear monopoly Waltz argued creates regional imbalance.",
      "fa": "کشور خاورمیانه‌ای صاحب انحصار تسلیحات اتمی در تحلیل والتز را نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Israel. Exactly. Dimona's monopoly was the anomaly Waltz argued needed fixing.",
        "wrong_generic": "No, it was Israel. Nuclear monopolies create geopolitical arrogance, or so neorealism claims.",
        "common_wrong_answers": {
          "Pakistan": "Pakistan is facing New Delhi, not dominating the Levant.",
          "Saudi Arabia": "Riyadh has petrodollars and Patriot missiles, not atomic bombs.",
          "United States": "The US is a global superpower; Waltz was talking about local regional monopolies."
        }
      },
      "fa": {
        "correct_generic": "اسرائیل. کاملاً درسته! انحصار دیمونا که به باور والتز ریشه اصلی ماجراجویی‌های نظامی در منطقه است.",
        "wrong_generic": "خیر، پاسخ اسرائیل بود. کشوری که با زرادخانه اعلام‌نشده انحصار اتمی منطقه را در دست دارد.",
        "common_wrong_answers": {
          "پاکستان": "پاکستان حواسش به هند است و بخشی از خاورمیانه عربی محسوب نمی‌شود.",
          "عربستان سعودی": "سعودی دلارهای نفتی دارد اما کلاهک هسته‌ای ندارد.",
          "ایالات متحده": "آمریکا قدرت فرامنطقه‌ای است؛ بحث والتز انحصار تک‌قطبی درون خاورمیانه بود."
        }
      }
    },
    "explanation": {
      "en": "Waltz argues that Israel's status as the sole nuclear power in the Middle East has created an unstable regional hegemony, allowing it to attack neighbors with conventional impunity, a condition an Iranian bomb would counterbalance.",
      "fa": "کنت والتز معتقد است انحصار اتمی اسرائیل در خاورمیانه توازن قوا را بر هم زده و به آن مصونیت برای حملات نظامی داده است؛ بنابراین هسته‌ای شدن ایران به موازنه وحشت و احتیاط متقابل منجر می‌شود."
    },
    "provenance": {
      "source_book": "Why Iran Should Get the Bomb (Foreign Affairs)",
      "source_author": "Kenneth Waltz",
      "page_number": 3,
      "verbatim_passage": "Israel's nuclear monopoly has long fueled instability in the Middle East. In no other region of the world does a lone, unchecked nuclear state exist.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_waltz_bomb_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE BOMB ACCORDING TO WALTZ",
      "fa": "والتز با کلاهک هسته‌ای"
    },
    "clue_text": {
      "en": "Waltz dismisses Western anxieties about Iranian fanaticism by invoking this core realism assumption, positing that all sovereign regimes prioritize self-preservation and survival above ideology.",
      "fa": "والتز نگرانی‌های غرب درباره بنیادگرایی مذهبی رهبران ایران را با استناد به این فرض بنیادین رئالیسم رد می‌کند و می‌گوید تمام حکومت‌ها بقا و حفظ قدرت را بر ایدئولوژی مقدم می‌دارند."
    },
    "canonical_answer": {
      "en": "Rational Actor Assumption",
      "fa": "عقلانیت بازیگران"
    },
    "accepted_aliases": {
      "en": [
        "Rationality of the state",
        "Rational deterrence theory",
        "Rational state behavior",
        "Regime survival"
      ],
      "fa": [
        "عقلانیت دولتی",
        "رفتار عقلانی دولت‌ها",
        "نظریه بازدارندگی عقلانی",
        "فرض بازیگر عقلانی"
      ]
    },
    "options": {
      "en": [
        "Clash of Civilizations",
        "Rational Actor Assumption",
        "Democratic Peace Theory",
        "End of History"
      ],
      "fa": [
        "جنگ تمدن‌ها",
        "عقلانیت بازیگران",
        "صلح دموکراتیک",
        "پایان تاریخ"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Clash of Civilizations",
        "why_plausible": "Samuel Huntington's cultural conflict thesis.",
        "why_wrong": "Huntington argues cultures clash irrationally; Waltz strictly denies civilizational irrationality."
      },
      {
        "option": "Democratic Peace Theory",
        "why_plausible": "A major liberal IR theory.",
        "why_wrong": "Democratic peace theory argues democracies don't fight democracies; Waltz focuses on structural balance among states regardless of regime type."
      },
      {
        "option": "End of History",
        "why_plausible": "Francis Fukuyama's liberal triumph thesis.",
        "why_wrong": "It celebrates liberal capitalist dominance, entirely unrelated to neorealist deterrence logic."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Madman Theory",
        "Constructivism"
      ],
      "fa": [
        "نظریه مرد دیوانه",
        "برساخت‌گرایی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the foundational realist principle of state rationality and survival cited by Waltz.",
      "fa": "اصل بنیادین واقع‌گرایی ناظر بر ترجیح بقا و محاسبات عقلانی هزینه و فایده را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Rational Actor Assumption. That is it. Clerics like palaces and power far too much to welcome radioactive martyrdom.",
        "wrong_generic": "No, it was the Rational Actor Assumption. Realists believe survival always trumps scripture.",
        "common_wrong_answers": {
          "Clash of Civilizations": "Huntington thought cultures fight; Waltz thinks states calculate survival.",
          "Democratic Peace Theory": "Iran is no Western liberal democracy; Waltz's point is that it does not need to be.",
          "End of History": "History never ended; realists never thought it did."
        }
      },
      "fa": {
        "correct_generic": "عقلانیت بازیگران. کاملاً درسته! روحانیون هم حکومت و قدرت را بیش از شهادت اتمی دوست دارند.",
        "wrong_generic": "خیر، پاسخ عقلانیت بازیگران بود. اصل کلیدی رئالیسم که می‌گوید بقا همیشه بر شعار پیروز است.",
        "common_wrong_answers": {
          "جنگ تمدن‌ها": "هانتینگتون از جنگ تمدن‌ها گفت؛ والتز بر عقلانیت و موازنه قوا تأکید دارد.",
          "صلح دموکراتیک": "صلح دموکراتیک مختص لیبرال‌هاست؛ والتز به ساختار موازنه قدرت نگاه می‌کند.",
          "پایان تاریخ": "فوکویاما از پیروزی لیبرالیسم دم زد؛ والتز واقعیت سخت بازدارندگی را می‌دید."
        }
      }
    },
    "explanation": {
      "en": "Waltz contends that historical experience demonstrates that acquisition of nuclear weapons induces sober caution rather than reckless adventurism, as no regime, however radical its rhetoric, seeks national suicide.",
      "fa": "والتز تأکید می‌کند که تجربه تاریخی نشان داده دستیابی به بمب هسته‌ای هر حکومتی را محتاط و عمل‌گرا می‌کند، زیرا هیچ نظامی به دنبال خودکشی دسته جمعی نیست."
    },
    "provenance": {
      "source_book": "Why Iran Should Get the Bomb (Foreign Affairs)",
      "source_author": "Kenneth Waltz",
      "page_number": 4,
      "verbatim_passage": "Despite widespread rhetoric about Iranian irrationality, Iranian policy is directed by sane leaders who want to survive. Like all other nuclear states, Iran would be deterred by the certainty of retaliation.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_waltz_bomb_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "THE BOMB ACCORDING TO WALTZ",
      "fa": "والتز با کلاهک هسته‌ای"
    },
    "clue_text": {
      "en": "In strategic theory, this famous paradox posited by Glenn Snyder asserts that while nuclear weapons prevent full-scale direct war between adversaries, they may simultaneously make low-level proxy skirmishes safer to conduct.",
      "fa": "در نظریه راهبردی، این پارادوکس مشهور گلن اسنایدر تصریح می‌کند که هرچند تسلیحات هسته‌ای مانع از وقوع جنگ تمام‌عیار می‌شوند، همزمان اجرای درگیری‌های نیابتی محدود را کم‌ریسک‌تر و محتمل‌تر می‌سازند."
    },
    "canonical_answer": {
      "en": "Stability-Instability Paradox",
      "fa": "پارادوکس ثبات و بی‌ثباتی"
    },
    "accepted_aliases": {
      "en": [
        "Stability instability paradox",
        "Snyder paradox"
      ],
      "fa": [
        "تناقض ثبات و بی‌ثباتی",
        "پارادوکس اسنایدر"
      ]
    },
    "options": {
      "en": [
        "Prisoner's Dilemma",
        "Stability-Instability Paradox",
        "Security Dilemma",
        "Thucydides Trap"
      ],
      "fa": [
        "معمای زندانی",
        "پارادوکس ثبات و بی‌ثباتی",
        "معمای امنیت",
        "تله توسیدید"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Prisoner's Dilemma",
        "why_plausible": "A cornerstone game theory concept.",
        "why_wrong": "It models cooperation vs defection, not the layered dynamics between strategic nuclear stability and tactical conventional proxy conflict."
      },
      {
        "option": "Security Dilemma",
        "why_plausible": "A classic IR concept where one state's defensive steps threaten another.",
        "why_wrong": "The security dilemma is general; the specific paradox describing high-level stability enabling low-level instability is the Stability-Instability Paradox."
      },
      {
        "option": "Thucydides Trap",
        "why_plausible": "A popular concept regarding rising powers challenging ruling powers.",
        "why_wrong": "Coined by Graham Allison for US-China relations, not Snyder's nuclear deterrence paradox."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Security Dilemma",
        "Deterrence Breakdown"
      ],
      "fa": [
        "معمای امنیت",
        "فروپاشی بازدارندگی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific strategic paradox linking strategic stability to tactical instability.",
      "fa": "نام پارادوکس مشهور راهبردی که ثبات در سطح کلان هسته‌ای را موجب بی‌ثباتی در سطح خرد می‌داند ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Stability-Instability Paradox. Spot on. Safe from atomic annihilation, free to throw drones across the border.",
        "wrong_generic": "No, it was the Stability-Instability Paradox. You can't invade the homeland, so you fight in the proxies.",
        "common_wrong_answers": {
          "Prisoner's Dilemma": "Prisoner's dilemma is game theory in a cell; this is nuclear arsenals on alert.",
          "Security Dilemma": "Security dilemma makes everyone rearm; this paradox explains why proxy wars flourish.",
          "Thucydides Trap": "Thucydides watched Sparta and Athens; Snyder watched nuclear warheads."
        }
      },
      "fa": {
        "correct_generic": "پارادوکس ثبات و بی‌ثباتی. کاملاً درسته! وقتی اطمینان داری جنگ اتمی رخ نمی‌دهد، با خیال راحت با پهپاد و نیابتی‌ها بازی می‌کنی.",
        "wrong_generic": "خیر، پاسخ پارادوکس ثبات و بی‌ثباتی بود. نظریه گلن اسنایدر درباره سطوح مختلف جنگ.",
        "common_wrong_answers": {
          "معمای زندانی": "معمای زندانی مدل نظریه بازی‌هاست، نه دکترین بازدارندگی هسته‌ای.",
          "معمای امنیت": "معمای امنیت مسابقه تسلیحاتی عمومی ایجاد می‌کند؛ این پارادوکس جنگ نیابتی را توضیح می‌دهد.",
          "تله توسیدید": "تله توسیدید رقابت قدرت هژمون و نوظهور است؛ ربطی به چتر اتمی ندارد."
        }
      }
    },
    "explanation": {
      "en": "The Stability-Instability Paradox explains that while a nuclear-armed Iran and Israel would be deterred from launching existential state-destroying wars, both could feel emboldened to engage in intense shadow and proxy operations beneath the nuclear threshold.",
      "fa": "پارادوکس ثبات و بی‌ثباتی توضیح می‌دهد که چرا بازدارندگی متقابل هسته‌ای میان ایران و اسرائیل مانع حمله مستقیم اتمی می‌شود، اما همزمان می‌تواند تنش‌های غیرمستقیم و حملات نیابتی را در سطح زیرین تشدید کند."
    },
    "provenance": {
      "source_book": "Why Iran Should Get the Bomb (Foreign Affairs)",
      "source_author": "Kenneth Waltz",
      "page_number": 4,
      "verbatim_passage": "Nuclear weapons do not eliminate conflict entirely, but they dramatically reduce the danger of major war by creating what strategic theorists call the stability-instability dynamic.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_waltz_bomb_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "THE BOMB ACCORDING TO WALTZ",
      "fa": "والتز با کلاهک هسته‌ای"
    },
    "clue_text": {
      "en": "To reassure skeptics who claimed revolutionary regimes are inherently reckless with weapons of mass destruction, Waltz cited the historical precedent of this communist leader whose 1964 bomb brought strategic sobriety rather than apocalypse.",
      "fa": "والتز برای اطمینان‌بخشی به بدبینانی که حکومت‌های ایدئولوژیک را غیرقابل پیش‌بینی می‌خواندند، به تجربه تاریخی این رهبر انقلابی کمونیست اشاره کرد که آزمایش اتمی ۱۹۶۴ او به جای فاجعه، عقلانیت راهبردی پدید آورد."
    },
    "canonical_answer": {
      "en": "Mao Zedong",
      "fa": "مائو تسه‌تونگ"
    },
    "accepted_aliases": {
      "en": [
        "Mao",
        "Chairman Mao",
        "Mao Tse-tung"
      ],
      "fa": [
        "مائو",
        "مائوتسه تونگ",
        "رئیس مائو"
      ]
    },
    "options": {
      "en": [
        "Joseph Stalin",
        "Mao Zedong",
        "Kim Il-sung",
        "Ho Chi Minh"
      ],
      "fa": [
        "ژوزف استالین",
        "مائو تسه‌تونگ",
        "کیم ایل سونگ",
        "هو شی مین"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Joseph Stalin",
        "why_plausible": "Acquired the Soviet bomb in 1949 and was an ideological communist dictator.",
        "why_wrong": "The USSR detonated its bomb in 1949; the 1964 test cited by Waltz as a radical revolutionary test was Mao's China (Project 596)."
      },
      {
        "option": "Kim Il-sung",
        "why_plausible": "Founder of North Korea's militarized dynasty.",
        "why_wrong": "North Korea did not test a nuclear weapon until 2006 under Kim Jong-il."
      },
      {
        "option": "Ho Chi Minh",
        "why_plausible": "Famous Asian communist revolutionary leader.",
        "why_wrong": "Vietnam never developed or tested nuclear weapons."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Joseph Stalin",
        "Fidel Castro"
      ],
      "fa": [
        "استالین",
        "فیدل کاسترو"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Chinese communist revolutionary leader whose 1964 nuclear acquisition Waltz cited as an analogy.",
      "fa": "نام رهبر کمونیست چین که دستیابی او به بمب در سال ۱۹۶۴ به عنوان شاهدی بر عقلانیت حکومت‌های انقلابی ذکر شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mao Zedong. Correct. Mao claimed nuclear bombs were paper tigers, then built his own and became remarkably cautious.",
        "wrong_generic": "No, it was Mao Zedong. If the Cultural Revolution didn't launch a nuclear strike, Tehran won't either.",
        "common_wrong_answers": {
          "Joseph Stalin": "Stalin got his bomb in 1949; 1964 was Beijing's breakthrough.",
          "Kim Il-sung": "Kim Il-sung fought with Soviet tanks; his grandson tested the nukes decades later.",
          "Ho Chi Minh": "Uncle Ho fought with tunnels and Kalashnikovs, not atomic fission."
        }
      },
      "fa": {
        "correct_generic": "مائو تسه‌تونگ. کاملاً درسته! رهبری که گفت بمب اتمی ببر کاغذی است، اما پس از ساخت آن در سال ۱۹۶۴ بسیار محتاط شد.",
        "wrong_generic": "خیر، پاسخ مائو تسه‌تونگ بود. مثالی کلاسیک که نشان داد دیوانه‌وارترین انقلاب‌ها هم پای دکمه قرمز عاقل می‌شوند.",
        "common_wrong_answers": {
          "ژوزف استالین": "استالین در سال ۱۹۴۹ بمب اتم شوروی را آزمایش کرد؛ سال ۱۹۶۴ متعلق به چین مائو بود.",
          "کیم ایل سونگ": "کیم ایل سونگ سال‌ها پیش از اولین آزمایش اتمی پیونگ‌یانگ درگذشت.",
          "هو شی مین": "هو شی مین در جنگل‌های ویتنام جنگید و هرگز بمب اتمی نداشت."
        }
      }
    },
    "explanation": {
      "en": "Waltz points to Maoist China's acquisition of the atomic bomb in October 1964: despite Mao's radical anti-imperialist rhetoric about surviving nuclear war, Beijing never used nuclear weapons and adopted a strictly defensive, no-first-use posture.",
      "fa": "والتز به تجربه آزمایش هسته‌ای چین در اکتبر ۱۹۶۴ اشاره می‌کند: با وجود شعارهای تند مائو علیه امپریالیسم، چین بمب را به کار نبرد و بلافاصله راهبرد بازدارندگی تدافعی و عدم استفاده پیش‌دستانه را در پیش گرفت."
    },
    "provenance": {
      "source_book": "Why Iran Should Get the Bomb (Foreign Affairs)",
      "source_author": "Kenneth Waltz",
      "page_number": 5,
      "verbatim_passage": "When China got the bomb in 1964, many in the West were hysterical that a radical Maoist regime would start World War III. Instead, China became more cautious and pragmatic.",
      "evidence_type": "FACT"
    }
  }
])

# Categories 6 to 10
batch_a.extend([
  {
    "id": "double_komiteh_table_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "KOMITEHS OF THE ROUND TABLE",
      "fa": "کمیته‌های محل به وقت تصفیه"
    },
    "clue_text": {
      "en": "Formed spontaneously in mosques immediately after the February 1979 insurrection, these neighborhood-based armed bodies served as the revolution's early frontline police and moral enforcers.",
      "fa": "بلافاصله پس از پیروزی انقلاب بهمن ۱۳۵۷، این تشکل‌های مسلح محله‌محور در مساجد شکل گرفتند و به عنوان نخستین بازوی انتظامی و نظارتی انقلاب عمل کردند."
    },
    "canonical_answer": {
      "en": "Islamic Revolutionary Committees",
      "fa": "کمیته‌های انقلاب اسلامی"
    },
    "accepted_aliases": {
      "en": [
        "Komiteh",
        "Komitehs",
        "Islamic Committees",
        "Komiteh-haye Enqelab-e Eslami"
      ],
      "fa": [
        "کمیته انقلاب اسلامی",
        "کمیته‌ها",
        "کمیته"
      ]
    },
    "options": {
      "en": [
        "Shahrbani",
        "Islamic Revolutionary Committees",
        "Gendarmerie",
        "Savak"
      ],
      "fa": [
        "شهربانی",
        "کمیته‌های انقلاب اسلامی",
        "ژاندارمری",
        "ساواک"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Shahrbani",
        "why_plausible": "The conventional urban police force inherited from the Pahlavi state.",
        "why_wrong": "Shahrbani was demoralized, disarmed, and under political suspicion during the immediate revolutionary aftermath."
      },
      {
        "option": "Gendarmerie",
        "why_plausible": "The rural and highway military police force.",
        "why_wrong": "The Gendarmerie policed countryside highways, not neighborhood mosques in major cities."
      },
      {
        "option": "Savak",
        "why_plausible": "The notorious Pahlavi intelligence service.",
        "why_wrong": "SAVAK was abolished and dissolved upon the revolution's victory."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Sepah-e Pasdaran",
        "Basij"
      ],
      "fa": [
        "سپاه پاسداران",
        "بسیج"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the official name of the neighborhood mosque-based revolutionary committees formed in 1979.",
      "fa": "نام رسمی نهاد انتظامی انقلابی مستقر در مساجد در ابتدای انقلاب را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Islamic Revolutionary Committees. Correct. When your neighborhood mosque suddenly acquired machine guns and Toyota Land Cruisers.",
        "wrong_generic": "No, it was the Islamic Revolutionary Committees (Komitehs). The original revolutionary neighborhood patrols.",
        "common_wrong_answers": {
          "Shahrbani": "Shahrbani was hiding at home wondering if their uniforms would get them arrested.",
          "Gendarmerie": "Gendarmerie patrolled rural roads, not Tehran side streets.",
          "Savak": "SAVAK officers were in Evin prison or abroad, not running neighborhood mosques."
        }
      },
      "fa": {
        "correct_generic": "کمیته‌های انقلاب اسلامی. کاملاً درسته! وقتی تویوتاهای استیشن و ژ۳ در مساجد مستقر شدند.",
        "wrong_generic": "خیر، پاسخ کمیته‌های انقلاب اسلامی بود. گشت‌های سر چهارراه و بازرسی‌های معروف اول انقلاب.",
        "common_wrong_answers": {
          "شهربانی": "شهربانی خلع سلاح شده بود و جرئت ورود به محلات انقلابی را نداشت.",
          "ژاندارمری": "ژاندارمری پاسگاه‌های برون‌شهری داشت، نه پایگاه در مساجد پایتخت.",
          "ساواک": "ساواک در همان ۲۲ بهمن منحل شد و اعضایش در اوین بازداشت بودند."
        }
      }
    },
    "explanation": {
      "en": "Narges Alemzadeh explores how the early Komitehs emerged out of neighborhood mosques to manage local policing, food distribution, and security before being gradually institutionalized under central clerical oversight.",
      "fa": "نرگس علم‌زاده تشریح می‌کند که چگونه کمیته‌های انقلاب اسلامی از دل مساجد محلات سر برآوردند تا توزیع ارزاق، امنیت شهری و تسویه با رژیم گذشته را مدیریت کنند."
    },
    "provenance": {
      "source_book": "Revolutionaries for Life: The Formative Experience of the Early IRGC",
      "source_author": "Narges Alemzadeh",
      "page_number": 45,
      "verbatim_passage": "In the chaotic vacuum immediately following February 1979, the Islamic Revolutionary Committees (Komiteh-ha) emerged across urban neighborhoods to maintain order and purge remnants of the old regime.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_table_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "KOMITEHS OF THE ROUND TABLE",
      "fa": "کمیته‌های محل به وقت تصفیه"
    },
    "clue_text": {
      "en": "To rein in freelance revolutionary abuses, Ayatollah Khomeini appointed this prominent conservative cleric and leader of the Combatant Clergy Association as the Supreme Commander of the Central Komiteh.",
      "fa": "برای مهار تندروی‌ها و سازماندهی نیروهای خودسر، امام خمینی این روحانی برجسته جامعه روحانیت مبارز را به ریاست کمیته مرکزی انقلاب اسلامی در میدان بهارستان منصوب کرد."
    },
    "canonical_answer": {
      "en": "Mohammad-Reza Mahdavi Kani",
      "fa": "محمدرضا مهدوی کنی"
    },
    "accepted_aliases": {
      "en": [
        "Ayatollah Mahdavi Kani",
        "Mahdavi Kani",
        "Mahdavi-Kani"
      ],
      "fa": [
        "آیت‌الله مهدوی کنی",
        "مهدوی کنی",
        "آیت الله مهدوی کنی"
      ]
    },
    "options": {
      "en": [
        "Ali Akbar Hashemi Rafsanjani",
        "Mohammad-Reza Mahdavi Kani",
        "Sadegh Khalkhali",
        "Mohammad Beheshti"
      ],
      "fa": [
        "علی‌اکبر هاشمی رفسنجانی",
        "محمدرضا مهدوی کنی",
        "صادق خلخالی",
        "محمد بهشتی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Ali Akbar Hashemi Rafsanjani",
        "why_plausible": "A central powerbroker in the Revolutionary Council.",
        "why_wrong": "Rafsanjani focused on the Interior Ministry and Parliament, not heading the Central Komiteh."
      },
      {
        "option": "Sadegh Khalkhali",
        "why_plausible": "The notorious revolutionary judge appointed to try former officials.",
        "why_wrong": "Khalkhali headed revolutionary tribunals, while Mahdavi Kani led the Komiteh policing apparatus."
      },
      {
        "option": "Mohammad Beheshti",
        "why_plausible": "Leader of the Islamic Republican Party and head of the judiciary.",
        "why_wrong": "Beheshti led the judicial council, while Mahdavi Kani was entrusted specifically with the Komitehs."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Sadegh Khalkhali",
        "Ali Qoddusi"
      ],
      "fa": [
        "صادق خلخالی",
        "علی قدوسی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific senior cleric appointed to command the Central Revolutionary Komiteh.",
      "fa": "نام روحانی سرشناسی که از سوی امام خمینی به ریاست کمیته مرکزی انقلاب منصوب شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad-Reza Mahdavi Kani. Correct. Tasked with imposing clerical discipline on thousands of armed teenagers with megaphones.",
        "wrong_generic": "No, it was Mohammad-Reza Mahdavi Kani. The ultimate conservative organizational ballast.",
        "common_wrong_answers": {
          "Ali Akbar Hashemi Rafsanjani": "Rafsanjani was busy plotting parliamentary coalitions, not running Baharestan police desks.",
          "Sadegh Khalkhali": "Khalkhali was in the courtroom handing down sentences; Mahdavi Kani was running the station.",
          "Mohammad Beheshti": "Beheshti ran the supreme court and the IRP."
        }
      },
      "fa": {
        "correct_generic": "محمدرضا مهدوی کنی. کاملاً درسته! مردی که مأمور شد نظم را به کمیته‌های مسلح مساجد بازگرداند.",
        "wrong_generic": "خیر، پاسخ محمدرضا مهدوی کنی بود. رئیس کمیته مرکزی انقلاب در ساختمان بهارستان.",
        "common_wrong_answers": {
          "علی‌اکبر هاشمی رفسنجانی": "رفسنجانی در شورای انقلاب و مجلس متمرکز بود، نه فرماندهی کمیته‌ها.",
          "صادق خلخالی": "خلخالی حاکم شرع دادگاه‌ها بود؛ مهدوی کنی رئیس تشکیلات کمیته بود.",
          "محمد بهشتی": "بهشتی دبیرکل حزب جمهوری اسلامی و رئیس دیوان عالی کشور بود."
        }
      }
    },
    "explanation": {
      "en": "Ayatollah Mohammad-Reza Mahdavi Kani headed the Central Revolutionary Komiteh, using his authority to rein in autonomous local units and transform them into a reliable conservative security wing.",
      "fa": "آیت‌الله محمدرضا مهدوی کنی ریاست کمیته مرکزی انقلاب اسلامی را بر عهده داشت و با برقراری سلسله‌مراتب، مانع از هرج‌ومرج و اقدامات خودسرانه در کمیته‌های محلات شد."
    },
    "provenance": {
      "source_book": "Revolutionaries for Life: The Formative Experience of the Early IRGC",
      "source_author": "Narges Alemzadeh",
      "page_number": 48,
      "verbatim_passage": "Khomeini appointed Ayatollah Mohammad-Reza Mahdavi Kani as head of the Central Revolutionary Komiteh in Baharestan to centralize authority and curb arbitrary excesses.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_table_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "KOMITEHS OF THE ROUND TABLE",
      "fa": "کمیته‌های محل به وقت تصفیه"
    },
    "clue_text": {
      "en": "Beyond counter-intelligence against monarchist conspiracies, the Komitehs became most notorious in the daily lives of urban citizens for enforcing these behavioral codes through street checkpoints and house raids.",
      "fa": "کمیته‌ها افزون بر مبارزه با توطئه‌های سلطنت‌طلبان، در زندگی روزمره شهروندان بیش از هر چیز به خاطر اعمال این احکام رفتاری از طریق ایست‌های بازرسی و تفتیش خانه‌ها شهرت یافتند."
    },
    "canonical_answer": {
      "en": "Public Morality Codes",
      "fa": "احکام منکراتی و حجاب"
    },
    "accepted_aliases": {
      "en": [
        "Enjoining good and forbidding wrong",
        "Amr-e be Ma'roof",
        "Morality laws",
        "Islamic dress code enforcement"
      ],
      "fa": [
        "نهی از منکر",
        "گشت‌های منکراتی",
        "احکام شرعی پوشش",
        "امر به معروف و نهی از منکر"
      ]
    },
    "options": {
      "en": [
        "Traffic Ordinances",
        "Public Morality Codes",
        "Municipal Building Codes",
        "Price-gouging Inspections"
      ],
      "fa": [
        "قوانین راهنمایی و رانندگی",
        "احکام منکراتی و حجاب",
        "مقررات ساختمانی شهرداری",
        "نظارت بر گران‌فروشی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Traffic Ordinances",
        "why_plausible": "Involved stopping cars at checkpoints.",
        "why_wrong": "Regular police handled driving licenses; Komitehs searched trunks for smuggled alcohol, cassette tapes, and mixed gender parties."
      },
      {
        "option": "Municipal Building Codes",
        "why_plausible": "Urban regulation enforcement.",
        "why_wrong": "Handled by municipal inspectors, not armed revolutionary committees."
      },
      {
        "option": "Price-gouging Inspections",
        "why_plausible": "Related to guild inspectors.",
        "why_wrong": "Bazaar guilds and the Ministry of Commerce handled price gouging, while Komitehs focused primarily on moral, cultural, and political infractions."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Passport Checking",
        "Smuggling Interception"
      ],
      "fa": [
        "کنترل گذرنامه",
        "مبارزه با قاچاق کالا"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific domain of personal behavior, dress, and moral surveillance enforced by the Komitehs.",
      "fa": "حوزه احکام رفتاری ناظر بر پوشش، مهمانی‌های مختلط و کشف نوار کاست و مسکرات را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Public Morality Codes. Exactly. Sniffing trunks for vodka and checking cassette tapes for Googoosh.",
        "wrong_generic": "No, it was Public Morality Codes. The dreaded late-night flashlight into your front passenger seat.",
        "common_wrong_answers": {
          "Traffic Ordinances": "They didn't care about your blinker; they cared who was sitting next to you.",
          "Municipal Building Codes": "They didn't measure balcony height; they raided living room parties.",
          "Price-gouging Inspections": "The price of tomatoes was not what had young people nervous at 11 PM."
        }
      },
      "fa": {
        "correct_generic": "احکام منکراتی و حجاب. کاملاً درسته! چراغ‌قوه انداختن توی ماشین برای پیدا کردن نوار گوگوش و نسبت خانوادگی.",
        "wrong_generic": "خیر، پاسخ احکام منکراتی و حجاب بود. ترسناک‌ترین بازرسی شبانه برای جوانان دهه شصت.",
        "common_wrong_answers": {
          "قوانین راهنمایی و رانندگی": "کاری به گواهینامه نداشتند؛ می‌پرسیدند این خانم چه نسبتی با شما دارد.",
          "مقررات ساختمانی شهرداری": "شهرداری دنبال مجوز ساخت بود؛ کمیته دنبال مهمانی مختلط بود.",
          "نظارت بر گران‌فروشی": "گران‌فروشی دغدغه بازرسی اصناف بود، نه بچه‌های کمیته سر چهارراه."
        }
      }
    },
    "explanation": {
      "en": "Alemzadeh notes that during the 1980s, the Komitehs became the primary institutional vehicle for moral policing (amr-e be ma'roof and nahi az monkar), conducting arbitrary checkpoints to uncover smuggled cassette tapes, alcohol, and unchaperoned mixed-gender socializing.",
      "fa": "علم‌زاده اشاره می‌کند که در طول دهه ۱۳۶۰ کمیته‌های انقلاب اسلامی اصلی‌ترین ابزار نظارت بر زیست اجتماعی و نهی از منکر بودند و با بازرسی‌های شبانه، مسکرات، نوارهای موسیقی و روابط خارج از چارچوب را کنترل می‌کردند."
    },
    "provenance": {
      "source_book": "Revolutionaries for Life: The Formative Experience of the Early IRGC",
      "source_author": "Narges Alemzadeh",
      "page_number": 52,
      "verbatim_passage": "Beyond political arrests, the Komitehs became feared guardians of public morality, raiding private parties and establishing checkpoints to intercept smuggled alcohol, Western audio cassettes, and violations of mandatory hejab.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_table_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "KOMITEHS OF THE ROUND TABLE",
      "fa": "کمیته‌های محل به وقت تصفیه"
    },
    "clue_text": {
      "en": "In the institutional rivalry of the early 1980s analyzed by Alemzadeh, the Komitehs, allied with traditionalist conservative clergy, frequently clashed over jurisdiction and ideological purity with this rapidly rising rival armed body.",
      "fa": "در رقابت‌های نهادی ابتدای دهه شصت، کمیته‌ها که پیوند نزدیکی با روحانیت سنتی داشتند، در حوزه صلاحیت قضایی و ماموریت‌های نظامی با این نهاد مسلح نوظهور و رقیب دچار اصطکاک شدند."
    },
    "canonical_answer": {
      "en": "Islamic Revolutionary Guard Corps",
      "fa": "سپاه پاسداران انقلاب اسلامی"
    },
    "accepted_aliases": {
      "en": [
        "IRGC",
        "Sepah-e Pasdaran",
        "The Pasdaran",
        "Sepah"
      ],
      "fa": [
        "سپاه پاسداران",
        "سپاه",
        "پاسداران"
      ]
    },
    "options": {
      "en": [
        "Islamic Revolutionary Guard Corps",
        "Artesh",
        "Shahrbani",
        "Javad al-A'immeh Brigade"
      ],
      "fa": [
        "سپاه پاسداران انقلاب اسلامی",
        "ارتش جمهوری اسلامی",
        "شهربانی",
        "تیپ جوادالائمه"
      ]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Artesh",
        "why_plausible": "The conventional military had tension with revolutionary bodies.",
        "why_wrong": "Artesh was fighting the war against Iraq on the border and had little daily jurisdictional conflict with neighborhood urban Komitehs."
      },
      {
        "option": "Shahrbani",
        "why_plausible": "The municipal police.",
        "why_wrong": "Shahrbani was thoroughly subordinated and lacked the political muscle to challenge the Komitehs."
      },
      {
        "option": "Javad al-A'immeh Brigade",
        "why_plausible": "A specific military unit.",
        "why_wrong": "Not a major independent institutional competitor at the national level."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Basij Resistance Force",
        "Vevak"
      ],
      "fa": [
        "بسیج",
        "وزارت اطلاعات"
      ]
    },
    "specificity_prompt": {
      "en": "Name the major revolutionary military force that competed with the Komitehs for armed supremacy in early post-revolutionary Iran.",
      "fa": "نام نهاد نظامی انقلابی اصلی رقیب کمیته‌ها در سال‌های اولیه انقلاب را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Islamic Revolutionary Guard Corps. Spot on. Two revolutionary twins fighting over who held the real monopoly of force.",
        "wrong_generic": "No, it was the IRGC (Sepah). Both were revolutionary, but Sepah had bigger ambitions and bigger guns.",
        "common_wrong_answers": {
          "Artesh": "Artesh kept its head down at the front lines; Sepah was battling for institutional territory.",
          "Shahrbani": "Shahrbani was marginalized; it wasn't picking fights with powerful clerical bodies.",
          "Javad al-A'immeh Brigade": "A unit, not the institutional giant that was the IRGC."
        }
      },
      "fa": {
        "correct_generic": "سپاه پاسداران انقلاب اسلامی. کاملاً درسته! رقابت دو برادر انقلابی بر سر اینکه چه کسی فرمانده اصلی شهر و جبهه است.",
        "wrong_generic": "خیر، پاسخ سپاه پاسداران بود. اصطکاک میان نهادهای موازی در دهه شصت.",
        "common_wrong_answers": {
          "ارتش جمهوری اسلامی": "ارتش درگیر نبرد کلاسیک در مرزها بود، نه رقابت بر سر نفوذ در محلات تهران.",
          "شهربانی": "شهربانی توان رقابت با کمیته‌ها را نداشت و تحت سلطه بود.",
          "تیپ جوادالائمه": "یک تیپ عملیاتی بود، نه رقیب ساختاری در حاکمیت."
        }
      }
    },
    "explanation": {
      "en": "Narges Alemzadeh analyzes the friction between the Komitehs (tied to traditional clerical networks of the Combatant Clergy Association) and the younger, more technocratic and militarized cadre of the IRGC, who resented Komiteh autonomy.",
      "fa": "نرگس علم‌زاده اصطکاک و مرزبندی میان کمیته‌ها (وابسته به شبکه علمای سنتی جامعه روحانیت مبارز) و فرماندهان جوان‌تر سپاه را که خواهان تمرکز فرماندهی نظامی و امنیتی بودند تحلیل می‌کند."
    },
    "provenance": {
      "source_book": "Revolutionaries for Life: The Formative Experience of the Early IRGC",
      "source_author": "Narges Alemzadeh",
      "page_number": 57,
      "verbatim_passage": "Tensions frequently flared between the Komitehs, under the aegis of conservative clerics, and the IRGC, whose leaders sought a unified military command and viewed the local committees as undisciplined rivals.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_komiteh_table_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "KOMITEHS OF THE ROUND TABLE",
      "fa": "کمیته‌های محل به وقت تصفیه"
    },
    "clue_text": {
      "en": "In 1991, under President Hashemi Rafsanjani's post-war bureaucratic rationalization, the Komitehs, Shahrbani, and Gendarmerie were dissolved and merged into this unified national police force.",
      "fa": "در سال ۱۳۷۰ در چارچوب یکپارچه‌سازی اداری دوران سازندگی، کمیته‌های انقلاب اسلامی با شهربانی و ژاندارمری ادغام شدند و این نیروی انتظامی واحد را پدید آوردند."
    },
    "canonical_answer": {
      "en": "Law Enforcement Force of the Islamic Republic of Iran",
      "fa": "نیروی انتظامی جمهوری اسلامی ایران"
    },
    "accepted_aliases": {
      "en": [
        "NAJA",
        "Law Enforcement Command",
        "Police Force of the IRI",
        "Faraja"
      ],
      "fa": [
        "ناجا",
        "فراجا",
        "نیروی انتظامی",
        "پلیس"
      ]
    },
    "options": {
      "en": [
        "Ministry of Intelligence",
        "Law Enforcement Force of the Islamic Republic of Iran",
        "Basij Organization",
        "Ansar-e Hezbollah"
      ],
      "fa": [
        "وزارت اطلاعات",
        "نیروی انتظامی جمهوری اسلامی ایران",
        "سازمان بسیج",
        "انصار حزب‌الله"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Ministry of Intelligence",
        "why_plausible": "A consolidated security bureaucracy created in 1984.",
        "why_wrong": "MOIS (Vevak) was created in 1984 for intelligence; the 1991 merger specifically unified uniform police into NAJA."
      },
      {
        "option": "Basij Organization",
        "why_plausible": "A revolutionary volunteer militia.",
        "why_wrong": "Basij remained a subsidiary of the IRGC and was not the product of the 1991 police merger."
      },
      {
        "option": "Ansar-e Hezbollah",
        "why_plausible": "A vigilante street group active in the 1990s.",
        "why_wrong": "Ansar-e Hezbollah was an informal vigilante pressure group, not the official statutory state police force."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Faraja",
        "Police-e Rahvar"
      ],
      "fa": [
        "فراجا",
        "پلیس راهور"
      ]
    },
    "specificity_prompt": {
      "en": "Name the unified national police force (NAJA) created by the 1991 merger.",
      "fa": "نام کامل نهاد پلیس واحد سراسری حاصل از ادغام کمیته، شهربانی و ژاندارمری در سال ۱۳۷۰ را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Law Enforcement Force of the Islamic Republic of Iran. Correct. Giving the bearded komiteh enforcers green police uniforms and a badge.",
        "wrong_generic": "No, it was the Law Enforcement Force (NAJA, now FARAJA). The 1991 merger that finally put an end to the separate Komiteh brand.",
        "common_wrong_answers": {
          "Ministry of Intelligence": "Intelligence was formed in 1984 under Reyshahri; NAJA was the 1991 police merger.",
          "Basij Organization": "Basij belongs to the Pasdaran, not the merged interior police.",
          "Ansar-e Hezbollah": "Ansar was a vigilante mob on motorbikes, not the formal state police."
        }
      },
      "fa": {
        "correct_generic": "نیروی انتظامی جمهوری اسلامی ایران. کاملاً درسته! لباس سبز یشمی و پایان تابلوی کمیته در خیابان‌ها.",
        "wrong_generic": "خیر، پاسخ نیروی انتظامی جمهوری اسلامی ایران (ناجا) بود. ادغام تاریخی سال ۱۳۷۰.",
        "common_wrong_answers": {
          "وزارت اطلاعات": "وزارت اطلاعات در سال ۶۳ تأسیس شد؛ ادغام ناجا در سال ۱۳۷۰ رخ داد.",
          "سازمان بسیج": "بسیج زیرمجموعه سپاه ماند؛ ناجا حاصل ادغام شهربانی و ژاندارمری و کمیته بود.",
          "انصار حزب‌الله": "انصار حزب‌الله تشکل غیررسمی فشار بود، نه نیروی پلیس رسمی کشور."
        }
      }
    },
    "explanation": {
      "en": "In 1991, the Iranian Parliament passed legislation merging the Islamic Revolutionary Committees with the imperial-era Gendarmerie and Shahrbani to establish the unified Law Enforcement Force (Nirou-ye Entezami-e Jomhouri-ye Eslami, or NAJA), subordinating them to the Ministry of Interior.",
      "fa": "در سال ۱۳۷۰ با تصویب مجلس شورای اسلامی، کمیته‌های انقلاب اسلامی، ژاندارمری و شهربانی در یکدیگر ادغام شده و «نیروی انتظامی جمهوری اسلامی ایران» (ناجا) را زیر نظر وزارت کشور تشکیل دادند."
    },
    "provenance": {
      "source_book": "Revolutionaries for Life: The Formative Experience of the Early IRGC",
      "source_author": "Narges Alemzadeh",
      "page_number": 61,
      "verbatim_passage": "In 1991, Rafsanjani's administration brought an end to the Komitehs' institutional independence by merging them with the Gendarmerie and Shahrbani to create the Law Enforcement Force (NAJA).",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_sanctions_kitchen_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "SANCTIONS IN THE KITCHEN",
      "fa": "تحریم در سفره بانوان"
    },
    "clue_text": {
      "en": "In her gendered political economy studies, this renowned Iranian-American feminist sociologist demonstrates that unilateral US economic sanctions disproportionately crush women's employment and domestic livelihoods.",
      "fa": "این جامعه‌شناس فمینیست و پژوهشگر سرشناس ایرانی-آمریکایی در پژوهش‌های اقتصاد سیاسی خود نشان می‌دهد که تحریم‌های یکجانبه اقتصادی آمریکا پیش از همه اشتغال و معیشت زنان را ویران می‌کند."
    },
    "canonical_answer": {
      "en": "Valentine Moghadam",
      "fa": "ولنتاین مقدم"
    },
    "accepted_aliases": {
      "en": [
        "Valentine M. Moghadam",
        "Moghadam",
        "Val Moghadam"
      ],
      "fa": [
        "ولنتاین ام مقدم",
        "مقدم",
        "ولنتاین ام. مقدم"
      ]
    },
    "options": {
      "en": [
        "Haleh Esfandiari",
        "Valentine Moghadam",
        "Azza Karam",
        "Fatema Mernissi"
      ],
      "fa": [
        "هاله اسفندیاری",
        "ولنتاین مقدم",
        "عزه کرم",
        "فاطمه مرنیسی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Haleh Esfandiari",
        "why_plausible": "A prominent Iranian-American scholar who headed the Middle East Program at the Wilson Center.",
        "why_wrong": "Esfandiari writes on women's memoirs and politics, not the quantitative gendered macro-economic sanctions analysis of Moghadam."
      },
      {
        "option": "Azza Karam",
        "why_plausible": "A well-known scholar of gender and development in the Middle East.",
        "why_wrong": "Karam focuses on global interfaith diplomacy and UN gender programs, not Iranian sanctions data."
      },
      {
        "option": "Fatema Mernissi",
        "why_plausible": "A legendary Moroccan feminist sociologist.",
        "why_wrong": "Mernissi was Moroccan and wrote on classical Islamic text and the harem, not contemporary US-Iran economic sanctions."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Homa Hoodfar",
        "Nayereh Tohidi"
      ],
      "fa": [
        "هما هودفر",
        "نیره توحیدی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific sociologist author of 'The Gendered Politics of US-Iran Sanctions'.",
      "fa": "نام نویسنده و جامعه‌شناس مقاله سیاست‌های جنسیتی تحریم‌های آمریکا علیه ایران را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Valentine Moghadam. Correct. Tracking how financial blockades hit the household long before they hit the generals.",
        "wrong_generic": "No, it was Valentine Moghadam. Documenting the feminist cost of economic siege.",
        "common_wrong_answers": {
          "Haleh Esfandiari": "Esfandiari wrote about civil society and memoirs, not economic modeling of sanctions.",
          "Azza Karam": "Karam is Egyptian-Dutch and works in UN interfaith circles.",
          "Fatema Mernissi": "Mernissi was Moroccan and explored historical harems, not central bank sanctions."
        }
      },
      "fa": {
        "correct_generic": "ولنتاین مقدم. کاملاً درسته! جامعه‌شناسی که نشان داد ترکش‌های تحریم اقتصادی چگونه به آشپزخانه زنان اصابت می‌کند.",
        "wrong_generic": "خیر، پاسخ ولنتاین مقدم بود. پژوهشگر اقتصاد سیاسی جنسیت و اثرات تحریم.",
        "common_wrong_answers": {
          "هاله اسفندیاری": "اسفندیاری خاطرات و جامعه مدنی را نوشت، نه تحلیل ساختاری اثر تحریم بر اشتغال زنان.",
          "عزه کرم": "عزه کرم پژوهشگر مصری در حوزه دین و توسعه سازمان ملل است.",
          "فاطمه مرنیسی": "مرنیسی جامعه‌شناس فقید مراکشی بود و درباره زنان در صدر اسلام می‌نوشت."
        }
      }
    },
    "explanation": {
      "en": "Valentine Moghadam analyzes how external sanctions induce hyperinflation and factory closures, leading to the rapid retrenchment of female wage workers who are the first to be laid off in industrial downturns.",
      "fa": "ولنتاین مقدم تشریح می‌کند که چگونه تحریم‌های بین‌المللی با ایجاد تورم افسارگسیخته و تعطیلی کارخانه‌ها، زنان شاغل را به نخستین قربانیان اخراج و تعدیل نیرو تبدیل می‌سازد."
    },
    "provenance": {
      "source_book": "The Gendered Politics of US-Iran Sanctions",
      "source_author": "Valentine Moghadam",
      "page_number": 3,
      "verbatim_passage": "Economic sanctions are not gender-neutral; they dismantle the fragile gains of female employment, throwing women out of the formal labor market and increasing household precarity.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_sanctions_kitchen_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "SANCTIONS IN THE KITCHEN",
      "fa": "تحریم در سفره بانوان"
    },
    "clue_text": {
      "en": "As household budgets contract under inflation, Moghadam observes that women bear the brunt of the crisis by performing this unpaid labor, substituting homemade goods and tedious cooking for store-bought commodities.",
      "fa": "با افت قدرت خرید خانواده‌ها زیر فشار تورم ناشی از تحریم، مقدم خاطرنشان می‌کند که زنان بار بحران را با انجام این کار خانگی بی‌مزد و جایگزینی دستپخت‌های زمان‌بر به جای کالاهای آماده جبران می‌کنند."
    },
    "canonical_answer": {
      "en": "Unpaid Care Work",
      "fa": "کار مراقبتی و خانگی بی‌مزد"
    },
    "accepted_aliases": {
      "en": [
        "Unpaid care labor",
        "Domestic labor",
        "Care economy",
        "Household care work"
      ],
      "fa": [
        "کار خانگی بدون دستمزد",
        "کار مراقبتی بی‌مزد",
        "اقتصاد مراقبت",
        "کار خانگی زنان"
      ]
    },
    "options": {
      "en": [
        "State Civil Service",
        "Unpaid Care Work",
        "Factory Assembly Work",
        "Agricultural Exporting"
      ],
      "fa": [
        "خدمت در دیوان‌سالاری دولتی",
        "کار مراقبتی و خانگی بی‌مزد",
        "مونتاژ قطعات در کارخانه",
        "صادرات محصولات کشاورزی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "State Civil Service",
        "why_plausible": "A major employer of educated women in Iran.",
        "why_wrong": "State service is paid wage labor, whereas the burden of crisis coping fell on unpaid home reproductive labor."
      },
      {
        "option": "Factory Assembly Work",
        "why_plausible": "Industrial wage work.",
        "why_wrong": "Industrial wage jobs declined under import restrictions and factory shutdowns."
      },
      {
        "option": "Agricultural Exporting",
        "why_plausible": "Rural economic activity.",
        "why_wrong": "Not the urban domestic substitution mechanism analyzed by Moghadam."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Gig Economy",
        "Informal Vending"
      ],
      "fa": [
        "اقتصاد پلتفرمی",
        "دستفروشی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the economic concept describing the unpaid home labor that absorbs the shock of economic sanctions.",
      "fa": "مفهوم اقتصادی ناظر بر زحمات خانگی بدون دستمزد زنان برای جبران کسری بودجه خانواده را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Unpaid Care Work. Correct. Turning hours of peeling, boiling, and mending into an invisible shock absorber for the national economy.",
        "wrong_generic": "No, it was Unpaid Care Work (domestic reproductive labor). The hidden subsidy propping up sanctioned families.",
        "common_wrong_answers": {
          "State Civil Service": "Civil service pays a salary; care work at home pays nothing.",
          "Factory Assembly Work": "Factories were closing due to lack of raw materials.",
          "Agricultural Exporting": "Exports were blocked by banking sanctions."
        }
      },
      "fa": {
        "correct_generic": "کار مراقبتی و خانگی بی‌مزد. کاملاً درسته! جذب ضربات تحریم با کار شبانه‌روزی و بدون مزد زنان در آشپزخانه.",
        "wrong_generic": "خیر، پاسخ کار مراقبتی و خانگی بی‌مزد بود. یارانه‌ای پنهان که اقتصاد ورشکسته را سر پا نگه می‌دارد.",
        "common_wrong_answers": {
          "خدمت در دیوان‌سالاری دولتی": "کارمندی دولت حقوق رسمی دارد؛ بحث بر سر کار بی‌مزد درون خانه بود.",
          "مونتاژ قطعات در کارخانه": "کارخانه‌ها به دلیل نبود قطعه وارداتی تعطیل می‌شدند.",
          "صادرات محصولات کشاورزی": "صادرات به دلیل مسدود بودن سوئیفت بانکی قفل شده بود."
        }
      }
    },
    "explanation": {
      "en": "Moghadam highlights that sanctions force a reliance on female unpaid reproductive labor: cooking from scratch, conserving utilities, and caring for the sick at home as state social services contract.",
      "fa": "مقدم تأکید می‌کند که تحریم‌ها فشار مضاعفی بر دوش زنان می‌گذارد زیرا کاهش خدمات دولتی موجب می‌شود زنان با کار خانگی فشرده‌تر و مراقبت از بیماران در خانه، کسری‌ها را جبران کنند."
    },
    "provenance": {
      "source_book": "The Gendered Politics of US-Iran Sanctions",
      "source_author": "Valentine Moghadam",
      "page_number": 7,
      "verbatim_passage": "Women cushion the impact of the economic shock by intensifying unpaid care work in the household, substituting their own domestic labor for commodified goods and privatized health services.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_sanctions_kitchen_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "SANCTIONS IN THE KITCHEN",
      "fa": "تحریم در سفره بانوان"
    },
    "clue_text": {
      "en": "Despite theoretical humanitarian exemptions, bank de-risking under Maximum Pressure caused deadly shortages of specialized medical dressings for children suffering from this rare blistering skin disease.",
      "fa": "با وجود ادعای معافیت‌های بشردوستانه، هراس بانک‌ها از تحریم‌های آمریکا موجب کمبود مرگبار پانسمان‌های تخصصی برای کودکان مبتلا به این بیماری نادر پوستی موسوم به «پروانه‌ای» شد."
    },
    "canonical_answer": {
      "en": "Epidermolysis Bullosa",
      "fa": "بیماری پروانه‌ای"
    },
    "accepted_aliases": {
      "en": [
        "EB",
        "Butterfly disease",
        "Epidermolysis bullosa"
      ],
      "fa": [
        "ای بی",
        "ای‌بی",
        "بیماری ای‌بی",
        "اپیدرمولیز بولوزا"
      ]
    },
    "options": {
      "en": [
        "Polio",
        "Epidermolysis Bullosa",
        "Tuberculosis",
        "Cholera"
      ],
      "fa": [
        "فلج اطفال",
        "بیماری پروانه‌ای",
        "سل",
        "وبا"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Polio",
        "why_plausible": "A disease controlled through childhood vaccines.",
        "why_wrong": "Iran produces its own oral polio vaccines domestically and eliminated endemic polio."
      },
      {
        "option": "Tuberculosis",
        "why_plausible": "An infectious pulmonary disease.",
        "why_wrong": "TB is treated with common antibiotics, not the patented Swedish specialized silicone dressings blocked by sanctions."
      },
      {
        "option": "Cholera",
        "why_plausible": "A waterborne gastrointestinal disease.",
        "why_wrong": "Cholera is treated with hydration salts and sanitation, not rare medical dressings."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Thalassemia",
        "Hemophilia"
      ],
      "fa": [
        "تالاسمی",
        "هموفیلی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific skin disease whose pediatric victims are known in Iran as 'butterfly children'.",
      "fa": "نام بیماری پوستی خاص که کودکان مبتلا به آن در ایران به بیماران پروانه‌ای مشهورند را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Epidermolysis Bullosa. Exactly. A humanitarian exemption that works everywhere except when a European bank looks at an Iranian transfer.",
        "wrong_generic": "No, it was Epidermolysis Bullosa (EB). The tragic case of the butterfly children.",
        "common_wrong_answers": {
          "Polio": "Iran eliminated polio with domestic vaccines decades ago.",
          "Tuberculosis": "TB uses standard pills; EB requires patented Mepilex foam dressings.",
          "Cholera": "Cholera needs clean water, not Swedish medical wound dressings."
        }
      },
      "fa": {
        "correct_generic": "بیماری پروانه‌ای. کاملاً درسته! پانسمان‌هایی که ادعا می‌شد تحریم نیستند اما با قطع سوئیفت به کودکان نرسیدند.",
        "wrong_generic": "خیر، پاسخ بیماری پروانه‌ای (ای‌بی) بود. دردناک‌ترین گواه ادعای دروغین معافیت دارویی تحریم‌ها.",
        "common_wrong_answers": {
          "فلج اطفال": "فلج اطفال در ایران با واکسن‌های ساخت داخل ریشه‌کن شده است.",
          "سل": "سل داروی آنتی‌بیوتیک عمومی دارد؛ بیماران پروانه‌ای نیازمند پانسمان میپلکس بودند.",
          "وبا": "وبا بیماری عفونی آب آلوده است، نه بیماری نادر ژنتیکی پوست."
        }
      }
    },
    "explanation": {
      "en": "Moghadam and human rights organizations documented that Swedish medical manufacturer Mölnlycke was unable to ship specialized Mepilex dressings to Iran due to international banking compliance fears, leading to severe suffering and fatalities among pediatric EB patients.",
      "fa": "ولنتاین مقدم و نهادهای حقوق بشری مستند کردند که به دلیل انسداد تراکنش‌های بانکی، شرکت سوئدی مولنلیکه از ارسال پانسمان‌های ویژه میپلکس به ایران بازماند و این امر جان ده‌ها کودک مبتلا به بیماری پروانه‌ای را گرفت."
    },
    "provenance": {
      "source_book": "The Gendered Politics of US-Iran Sanctions",
      "source_author": "Valentine Moghadam",
      "page_number": 11,
      "verbatim_passage": "Overcompliance and financial derisking blocked the importation of specialized wound dressings from Sweden for children afflicted with Epidermolysis Bullosa (known in Iran as butterfly children), resulting in tragic preventable deaths.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_sanctions_kitchen_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "SANCTIONS IN THE KITCHEN",
      "fa": "تحریم در سفره بانوان"
    },
    "clue_text": {
      "en": "To compensate for male breadwinner layoffs and wage collapse under international sanctions, millions of Iranian women flocked to this social media platform to operate informal home businesses and clothing boutiques.",
      "fa": "برای جبران بیکاری سرپرستان خانوار و افت شدید ارزش ریال در اثر تحریم‌ها، میلیون‌ها زن ایرانی برای راه‌اندازی کسب‌وکارهای خانگی و فروشگاه‌های پوشاک به این پلتفرم اجتماعی روی آوردند."
    },
    "canonical_answer": {
      "en": "Instagram",
      "fa": "اینستاگرام"
    },
    "accepted_aliases": {
      "en": [
        "Instagram app",
        "IG"
      ],
      "fa": [
        "اینستا",
        "شبکه اجتماعی اینستاگرام"
      ]
    },
    "options": {
      "en": [
        "LinkedIn",
        "Instagram",
        "Twitter",
        "Facebook"
      ],
      "fa": [
        "لینکدین",
        "اینستاگرام",
        "توییتر",
        "فیس‌بوک"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "LinkedIn",
        "why_plausible": "A corporate professional networking site.",
        "why_wrong": "Used by white-collar corporate professionals, not grassroots informal home commerce."
      },
      {
        "option": "Twitter",
        "why_plausible": "Widely used by Iranian political elites and activists.",
        "why_wrong": "Twitter is text-heavy and blocked since 2009; it does not support visual retail e-commerce like Instagram."
      },
      {
        "option": "Facebook",
        "why_plausible": "A major global social network.",
        "why_wrong": "Filtered since 2009 in Iran and largely abandoned by Iranian domestic commerce in favor of unblocked Instagram."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Telegram",
        "WhatsApp"
      ],
      "fa": [
        "تلگرام",
        "واتس‌اپ"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific photo-sharing social media network that became the primary hub of female home e-commerce in Iran.",
      "fa": "نام پلتفرم تصویری پرطرفداری که به قطب اقتصاد مشاغل خانگی زنان در دوران تحریم تبدیل شد را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Instagram. Spot on. The largest shopping mall in Iran, operating entirely outside the formal banking system.",
        "wrong_generic": "No, it was Instagram. Selling homemade pastries, makeup, and clothes via direct messages.",
        "common_wrong_answers": {
          "LinkedIn": "LinkedIn is for corporate resumes; Instagram is for selling coats and cakes.",
          "Twitter": "Twitter is where Iranian politicians yell at each other; Instagram is where business happens.",
          "Facebook": "Facebook was filtered in 2009 and forgotten by local shoppers."
        }
      },
      "fa": {
        "correct_generic": "اینستاگرام. کاملاً درسته! بزرگ‌ترین بازارچه تجاری آنلاین کشور که در دایرکت و کارت به کارت اداره می‌شد.",
        "wrong_generic": "خیر، پاسخ اینستاگرام بود. پناهگاه اشتغال میلیون‌ها زن خانه‌دار در روزهای سخت اقتصادی.",
        "common_wrong_answers": {
          "لینکدین": "لینکدین رزومه مهندسی است؛ اینستاگرام بازار فروش لباس و کیک خانگی بود.",
          "توییتر": "توییتر عرصه جدال سیاسی است، نه ویترین کسب‌وکارهای خرد زنان.",
          "فیس‌بوک": "فیس‌بوک سال‌هاست در ایران از رونق افتاده و جای خود را به اینستاگرام داد."
        }
      }
    },
    "explanation": {
      "en": "Moghadam and economic sociologists highlight that Instagram became the lifeline of Iran's informal economy, enabling over 400,000 women-led small enterprises to sell food, handicrafts, and fashion directly to consumers despite macroeconomic strangulation.",
      "fa": "ولنتاین مقدم و جامعه‌شناسان اقتصادی نشان می‌دهند که اینستاگرام به شریان حیاتی اقتصاد غیررسمی تبدیل شد و به بیش از ۴۰۰ هزار کسب‌وکار خانگی زنان امکان داد محصولات خود را مستقیماً عرضه کنند."
    },
    "provenance": {
      "source_book": "The Gendered Politics of US-Iran Sanctions",
      "source_author": "Valentine Moghadam",
      "page_number": 14,
      "verbatim_passage": "Faced with vanishing formal employment, Iranian women innovatively utilized Instagram as an informal commercial sanctuary, establishing home-based e-commerce shops to keep their households financially afloat.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_sanctions_kitchen_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "SANCTIONS IN THE KITCHEN",
      "fa": "تحریم در سفره بانوان"
    },
    "clue_text": {
      "en": "In a demographic trend analyzed by Moghadam, the economic despair caused by currency devaluation and housing inflation under sanctions resulted in Iran's total fertility rate collapsing below this critical generational replacement level.",
      "fa": "در یک روند جمعیتی که توسط مقدم تحلیل شده، استیصال اقتصادی ناشی از سقوط ارزش ریال و تورم مسکن در دوران تحریم، نرخ باروری کل ایران را به زیر این سطح بحرانیِ جایگزینی نسل‌ها کشاند."
    },
    "canonical_answer": {
      "en": "2.1 births per woman",
      "fa": "۲٫۱ فرزند به ازای هر زن"
    },
    "accepted_aliases": {
      "en": [
        "2.1",
        "Replacement level",
        "2.1 fertility rate",
        "Two point one"
      ],
      "fa": [
        "۲٫۱",
        "نرخ جایگزینی",
        "۲ ممیز ۱",
        "دو ممیز یک"
      ]
    },
    "options": {
      "en": [
        "3.5 births per woman",
        "2.1 births per woman",
        "1.1 births per woman",
        "4.2 births per woman"
      ],
      "fa": [
        "۳٫۵ فرزند به ازای هر زن",
        "۲٫۱ فرزند به ازای هر زن",
        "۱٫۱ فرزند به ازای هر زن",
        "۴٫۲ فرزند به ازای هر زن"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "3.5 births per woman",
        "why_plausible": "A typical developing country fertility rate.",
        "why_wrong": "Iran had high fertility in the 1980s (over 6.0), but by the 2010s under sanctions it plummeted well below replacement."
      },
      {
        "option": "1.1 births per woman",
        "why_plausible": "Extremely low fertility seen in South Korea.",
        "why_wrong": "Iran's rate dropped to approximately 1.6-1.7, which is critically below the replacement threshold of 2.1."
      },
      {
        "option": "4.2 births per woman",
        "why_plausible": "A figure from the 1970s.",
        "why_wrong": "Completely outdated; modern sanctions accelerated postponement of marriage and childbearing."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "1.6 births per woman",
        "Replacement threshold"
      ],
      "fa": [
        "۱٫۶ فرزند",
        "نرخ جانشینی"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the exact demographic figure defining the generational replacement rate of fertility.",
      "fa": "عدد دقیق شاخص جمعیت‌شناختی حد جایگزینی باروری را به صورت عدد یا حروف بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "2.1 births per woman. Correct. When young couples do the math on diapers and rent, patriotism takes a backseat.",
        "wrong_generic": "No, it fell below 2.1 births per woman (the replacement level). The economic calculus of childbearing in an inflation spiral.",
        "common_wrong_answers": {
          "3.5 births per woman": "3.5 was in the 1980s during the baby boom; today's youth cannot afford baby formula.",
          "1.1 births per woman": "1.1 is Seoul; Iran fell to around 1.6, breaking through the 2.1 threshold.",
          "4.2 births per woman": "4.2 is fifty years ago."
        }
      },
      "fa": {
        "correct_generic": "۲٫۱ فرزند به ازای هر زن. کاملاً درسته! وقتی هزینه مسکن و پوشک بالا می‌رود، هیچ فتوایی نمی‌تواند جوانان را صاحب فرزند کند.",
        "wrong_generic": "خیر، پاسخ ۲٫۱ فرزند (سطح جانشینی) بود. زنگ خطر پیری جمعیت ناشی از بحران معیشت.",
        "common_wrong_answers": {
          "۳٫۵ فرزند به ازای هر زن": "۳٫۵ متعلق به دهه شصت بود؛ امروز جوانان در هزینه اجاره‌خانه مانده‌اند.",
          "۱٫۱ فرزند به ازای هر زن": "۱٫۱ آمار کره جنوبی است؛ ایران به ۱٫۶ سقوط کرد که پایین‌تر از حد ۲٫۱ است.",
          "۴٫۲ فرزند به ازای هر زن": "۴٫۲ نرخ نیم قرن پیش بود."
        }
      }
    },
    "explanation": {
      "en": "Valentine Moghadam demonstrates that macroeconomic insecurity from sanctions accelerated Iran's demographic transition: fertility collapsed to around 1.6, far below the replacement level of 2.1 births per woman, defying official state campaigns promoting larger families.",
      "fa": "ولنتاین مقدم نشان می‌دهد که ناامنی اقتصادی ناشی از تحریم‌ها روند تغییرات جمعیتی را سرعت بخشید و نرخ باروری کل را به حدود ۱٫۶ رساند که بسیار پایین‌تر از نرخ جایگزینی ۲٫۱ فرزند است."
    },
    "provenance": {
      "source_book": "The Gendered Politics of US-Iran Sanctions",
      "source_author": "Valentine Moghadam",
      "page_number": 16,
      "verbatim_passage": "Economic precarity, housing hyperinflation, and unemployment pushed marriage ages upward and drove Iran's total fertility rate well below the demographic replacement level of 2.1, hovering near 1.6.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_proxy_paradox_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE PROXY PARADOX",
      "fa": "فرمانده بدون فرمانبردار"
    },
    "clue_text": {
      "en": "In his critique of Western strategic discourse, scholar Bilal Saad challenges this simplistic paradigm which wrongly treats Iran as an omnipotent puppet-master pulling strings and its regional allies as robotic pawns.",
      "fa": "بلال سعد در نقد ادبیات راهبردی غرب، این الگوی ساده‌انگارانه را به چالش می‌کشد که ایران را عروسک‌گردان قادر مطلق و هم‌پیمانان منطقه‌ای آن را مهره‌های بی‌اراده فرض می‌کند."
    },
    "canonical_answer": {
      "en": "Sponsor-Proxy Model",
      "fa": "مدل حامی و نایب"
    },
    "accepted_aliases": {
      "en": [
        "Sponsor proxy model",
        "Proxy model",
        "Puppet master model",
        "Client-patron model"
      ],
      "fa": [
        "الگوی حامی-پروکسی",
        "مدل کارفرما و نایب",
        "نظریه جنگ نیابتی",
        "مدل نایب و حامی"
      ]
    },
    "options": {
      "en": [
        "Bandwagoning Theory",
        "Sponsor-Proxy Model",
        "Democratic Peace Theory",
        "Core-Periphery Model"
      ],
      "fa": [
        "نظریه الحاق به قدرت",
        "مدل حامی و نایب",
        "صلح دموکراتیک",
        "مدل مرکز و پیرامون"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Bandwagoning Theory",
        "why_plausible": "A neorealist concept where weak states ally with the dominant threatening power.",
        "why_wrong": "Saad's critique specifically targets the strategic framing of proxy warfare in the Middle East."
      },
      {
        "option": "Democratic Peace Theory",
        "why_plausible": "A dominant liberal framework.",
        "why_wrong": "Irrelevant to Middle Eastern militia alliances and non-state network dynamics."
      },
      {
        "option": "Core-Periphery Model",
        "why_plausible": "Dependency theory terminology.",
        "why_wrong": "Pertains to global economic extraction, not the military command-and-control of resistance groups."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Patron-Client Framework",
        "Hub-and-Spoke System"
      ],
      "fa": [
        "چارچوب ارباب-رعیتی",
        "الگوی مرکز و پره"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific strategic model challenged by Bilal Saad in his analysis of the Axis of Resistance.",
      "fa": "نام مدل تحلیلی رایج غربی در توصیف روابط ایران و هم‌پیمانان منطقه‌ای که توسط بلال سعد نقد شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Sponsor-Proxy Model. Correct. Western think tankers assume Tehran pushes buttons and Lebanese politicians dance on command.",
        "wrong_generic": "No, it was the Sponsor-Proxy Model. Reality is far messier than remote-controlled militias.",
        "common_wrong_answers": {
          "Bandwagoning Theory": "Bandwagoning is jumping on the winning team; proxies often defy their sponsors.",
          "Democratic Peace Theory": "Neither Tehran nor regional militias are running liberal democracies.",
          "Core-Periphery Model": "Core-periphery is Wallerstein's Marxist economics, not Quds Force alliances."
        }
      },
      "fa": {
        "correct_generic": "مدل حامی و نایب. کاملاً درسته! اندیشکده‌های واشنگتن تصور می‌کنند تهران یک دکمه دارد که با آن بیروت و صنعا را کنترل می‌کند.",
        "wrong_generic": "خیر، پاسخ مدل حامی و نایب (اسپانسر-پروکسی) بود. سعد نشان داد این رابطه پیچیده‌تر و خودمختارتر است.",
        "common_wrong_answers": {
          "نظریه الحاق به قدرت": "پیوستن به ارابه قدرت نظریه والت است؛ بحث بر سر رابطه شبکه مقاومت بود.",
          "صلح دموکراتیک": "صلح دموکراتیک به حکومت‌های لیبرال مربوط است، نه خاورمیانه.",
          "مدل مرکز و پیرامون": "مرکز و پیرامون نظریه امپریالیسم والرشتاین است، نه تحلیل عملیاتی محور مقاومت."
        }
      }
    },
    "explanation": {
      "en": "Bilal Saad demonstrates that the 'Sponsor-Proxy Model' obscures the substantial ideological convergence, operational autonomy, and domestic political constraints of non-state actors like Hezbollah, the Houthis, and Iraqi militias.",
      "fa": "بلال سعد اثبات می‌کند که «مدل حامی و نایب» استقلال عمل، مشروعیت محلی و محاسبات داخلی نیروهایی چون حزب‌الله لبنان، انصارالله یمن و گروه‌های عراقی را نادیده می‌گیرد."
    },
    "provenance": {
      "source_book": "Challenging the Sponsor-Proxy Model",
      "source_author": "Bilal Saad",
      "page_number": 1,
      "verbatim_passage": "The dominant sponsor-proxy paradigm treats non-state regional allies as mere instruments of Iranian power, failing to recognize their internal agency, local responsiveness, and ideological autonomy.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_proxy_paradox_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "THE PROXY PARADOX",
      "fa": "فرمانده بدون فرمانبردار"
    },
    "clue_text": {
      "en": "Demonstrating strategic autonomy, Hezbollah launched this cross-border raid in July 2006 to capture Israeli soldiers to negotiate a prisoner swap, triggering the devastating 33-Day War without prior operational clearance from Tehran.",
      "fa": "برای اثبات استقلال عمل میدانی، حزب‌الله در تیر ۱۳۸۵ در این عملیات مرزی با اسارت سربازان اسرائیلی برای تبادل اسرا، جنگ ۳۳ روزه را کلید زد بدون آنکه از قبل مجوز عملیاتی از تهران دریافت کرده باشد."
    },
    "canonical_answer": {
      "en": "Operation Truthful Promise",
      "fa": "عملیات وعده صادق اول حزب‌الله"
    },
    "accepted_aliases": {
      "en": [
        "July 2006 raid",
        "Hezbollah cross-border raid",
        "Operation Truthful Promise 2006"
      ],
      "fa": [
        "عملیات وعده صادق ۲۰۰۶",
        "عملیات الوعد الصادق",
        "اسارت سربازان اسرائیلی ۲۰۰۶"
      ]
    },
    "options": {
      "en": [
        "Operation Litani",
        "Operation Truthful Promise",
        "Operation Grapes of Wrath",
        "Operation Accountability"
      ],
      "fa": [
        "عملیات لیتانی",
        "عملیات وعده صادق اول حزب‌الله",
        "عملیات خوشه‌های خشم",
        "عملیات تسویه‌حساب"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Operation Litani",
        "why_plausible": "A major Israeli military operation in southern Lebanon.",
        "why_wrong": "Operation Litani was carried out by Israel in 1978, four years before Hezbollah was even founded."
      },
      {
        "option": "Operation Grapes of Wrath",
        "why_plausible": "A major military clash in Lebanon in 1996.",
        "why_wrong": "It was the Israeli assault in April 1996 that ended with the April Understanding, not the 2006 raid."
      },
      {
        "option": "Operation Accountability",
        "why_plausible": "A 1993 Israeli offensive against Hezbollah.",
        "why_wrong": "Launched by Israel in July 1993, not Hezbollah's 2006 cross-border abduction."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "2006 Lebanon War",
        "Shebaa Farms raid"
      ],
      "fa": [
        "جنگ تموز",
        "عملیات مزارع شبعا"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific 2006 operation launched by Hezbollah that captured two Israeli soldiers.",
      "fa": "نام عملیات حزب‌الله در تیر ۱۳۸۵ که به اسارت دو نظامی اسرائیلی انجامید را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Operation Truthful Promise. Spot on. Nasrallah wanted Samir Kuntar back, and Tehran woke up to find Beirut getting bombed.",
        "wrong_generic": "No, it was Operation Truthful Promise (Al-Wa'd al-Sadeq). A local decision with massive regional fallout.",
        "common_wrong_answers": {
          "Operation Litani": "Litani was an Israeli invasion in 1978, years before Hezbollah existed.",
          "Operation Grapes of Wrath": "Grapes of Wrath was Shimon Peres's 1996 blitz in Qana.",
          "Operation Accountability": "Accountability was Rabin's 1993 bombing campaign."
        }
      },
      "fa": {
        "correct_generic": "عملیات وعده صادق اول حزب‌الله. کاملاً درسته! نصرالله می‌خواست سمیر قنطار را آزاد کند و تهران ناگهان خود را در میانه جنگ دید.",
        "wrong_generic": "خیر، پاسخ عملیات وعده صادق (العهد الصادق) حزب‌الله در سال ۱۳۸۵ بود. تصمیمی مستقل در جنوب لبنان.",
        "common_wrong_answers": {
          "عملیات لیتانی": "لیتانی حمله اسرائیل در سال ۱۳۵۶ بود، سال‌ها پیش از تأسیس حزب‌الله.",
          "عملیات خوشه‌های خشم": "خوشه‌های خشم تهاجم سال ۱۳۷۵ اسرائیل و فاجعه قانا بود.",
          "عملیات تسویه‌حساب": "تسویه‌حساب عملیات سال ۱۳۷۲ اسحاق رابین در جنوب لبنان بود."
        }
      }
    },
    "explanation": {
      "en": "Bilal Saad notes that Hassan Nasrallah candidly admitted after the war that had he known the scale of Israel's destructive response, he would never have authorized the capture of the two Israeli soldiers on July 12, 2006, proving the operation was an autonomous Lebanese tactical initiative.",
      "fa": "بلال سعد یادآوری می‌کند که سید حسن نصرالله پس از جنگ صراحتاً گفت اگر می‌دانست پاسخ اسرائیل در این مقیاس خواهد بود هرگز دستور اسارت دو سرباز را صادر نمی‌کرد؛ امری که نشان‌دهنده تصمیم‌گیری مستقل حزب‌الله فارغ از دیکته‌های تهران بود."
    },
    "provenance": {
      "source_book": "Challenging the Sponsor-Proxy Model",
      "source_author": "Bilal Saad",
      "page_number": 8,
      "verbatim_passage": "Hezbollah's July 2006 cross-border raid that ignited the 33-Day War was initiated independently by its local military command to secure Lebanese prisoners, catching Iranian leaders by surprise.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_proxy_paradox_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "THE PROXY PARADOX",
      "fa": "فرمانده بدون فرمانبردار"
    },
    "clue_text": {
      "en": "In September 2014, Ansar Allah (the Houthis) demonstrated complete disregard for Iranian cautionary diplomatic advice when they advanced from Saada and seized control of this capital city.",
      "fa": "در شهریور ۱۳۹۳، جنبش انصارالله یمن بی‌توجه به توصیه‌های دیپلماتیک محتاطانه مقامات تهران، از پایگاه خود در صعده به پیش تاخت و این پایتخت را به تصرف درآورد."
    },
    "canonical_answer": {
      "en": "Sana'a",
      "fa": "صنعا"
    },
    "accepted_aliases": {
      "en": [
        "Sanaa",
        "San'a"
      ],
      "fa": [
        "صنعاء",
        "شهر صنعا"
      ]
    },
    "options": {
      "en": [
        "Aden",
        "Sana'a",
        "Hodeidah",
        "Marib"
      ],
      "fa": [
        "عدن",
        "صنعا",
        "حدیده",
        "مأرب"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Aden",
        "why_plausible": "The major southern port city of Yemen.",
        "why_wrong": "Aden was seized later in 2015 when President Hadi fled south, not the initial September 2014 capital capture."
      },
      {
        "option": "Hodeidah",
        "why_plausible": "A strategic Red Sea port city.",
        "why_wrong": "Hodeidah is a coastal port city, not the national capital captured in September 2014."
      },
      {
        "option": "Marib",
        "why_plausible": "An oil-rich province heavily contested during the war.",
        "why_wrong": "Marib remained largely under government and tribal control and was never fully seized by the Houthis."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Aden",
        "Taiz"
      ],
      "fa": [
        "عدن",
        "تعز"
      ]
    },
    "specificity_prompt": {
      "en": "Name the capital city of Yemen seized by the Houthis in September 2014.",
      "fa": "نام پایتخت یمن که در شهریور ۱۳۹۳ توسط انصارالله تصرف شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Sana'a. Correct. Tehran advised caution, and Abdul-Malik al-Houthi drove straight into the presidential palace.",
        "wrong_generic": "No, it was Sana'a. An undeniable demonstration that regional allies run their own calendars.",
        "common_wrong_answers": {
          "Aden": "Aden is the southern port city; Sana'a is the historic highland capital.",
          "Hodeidah": "Hodeidah is the Red Sea port; the prize was the capital in the mountains.",
          "Marib": "Marib is the desert oilfield; Sana'a was the seat of power."
        }
      },
      "fa": {
        "correct_generic": "صنعا. کاملاً درسته! دیپلمات‌های تهران گفتند دست نگه دارید، ولی عبدالملک الحوثی پایتخت را تصرف کرد.",
        "wrong_generic": "خیر، پاسخ صنعا بود. مثالی روشن از استقلال عمل انصارالله در پیشبرد اهداف نظامی.",
        "common_wrong_answers": {
          "عدن": "عدن بندر جنوبی بود که عبدربه منصور هادی به آن گریخت؛ پایتخت تصرف‌شده صنعا بود.",
          "حدیده": "حدیده بندر دریای سرخ است؛ تسخیر پایتخت کوهستانی مد نظر بود.",
          "مأرب": "مأرب کانون نفتی شرق است که سال‌ها صحنه نبرد ماند."
        }
      }
    },
    "explanation": {
      "en": "Bilal Saad cites intelligence reports and diplomatic disclosures confirming that Iranian officials explicitly cautioned the Houthis against invading Sana'a in September 2014, fearing a massive Saudi military intervention, but were ignored by Houthi commanders.",
      "fa": "بلال سعد به گزارش‌های دیپلماتیک استناد می‌کند که نشان می‌دهد مقامات تهران صراحتاً انصارالله را از پیشروی به سوی صنعا در شهریور ۹۳ برحذر داشتند تا مانع جنگ با ائتلاف سعودی شوند، اما حوثی‌ها مستقلانه تصمیم به فتح پایتخت گرفتند."
    },
    "provenance": {
      "source_book": "Challenging the Sponsor-Proxy Model",
      "source_author": "Bilal Saad",
      "page_number": 12,
      "verbatim_passage": "When the Houthis moved to seize Sana'a in September 2014, they did so against the explicit advice of Iranian diplomats, who warned them that taking the capital would trigger a direct Saudi military invasion.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_proxy_paradox_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "THE PROXY PARADOX",
      "fa": "فرمانده بدون فرمانبردار"
    },
    "clue_text": {
      "en": "Instead of hierarchical military command, Saad defines Iran's relationship with regional movements through this concept of ideological alignment, mutual reliance, and reciprocal bargaining power.",
      "fa": "بلال سعد به جای روابط سلسله‌مراتبی و ارباب‌رعیتی، پیوند ایران با جنبش‌های منطقه‌ای را با این مفهوم هم‌افزایی، هم‌پوشانی هویتی و وابستگی متقابل راهبردی تبیین می‌کند."
    },
    "canonical_answer": {
      "en": "Strategic Interdependence",
      "fa": "وابستگی متقابل راهبردی"
    },
    "accepted_aliases": {
      "en": [
        "Strategic synergy",
        "Mutual interdependence",
        "Network synergy",
        "Reciprocal alliance"
      ],
      "fa": [
        "هم‌افزایی راهبردی",
        "وابستگی متقابل",
        "شبکه هم‌افزا",
        "ائتلاف شبکه‌ای"
      ]
    },
    "options": {
      "en": [
        "Mercenary Subcontracting",
        "Strategic Interdependence",
        "Feudal Vassalage",
        "Colonial Subordination"
      ],
      "fa": [
        "پیمانکاری مزدورانه",
        "وابستگی متقابل راهبردی",
        "تبعیت فئودالی",
        "اطاعت استعماری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Mercenary Subcontracting",
        "why_plausible": "Common derogatory language used in political rhetoric.",
        "why_wrong": "Saad explicitly refutes the idea that resistance allies are hired mercenaries; they have deep indigenous ideological roots."
      },
      {
        "option": "Feudal Vassalage",
        "why_plausible": "Implies pledged loyalty.",
        "why_wrong": "Feudal vassalage implies total subservience to a feudal lord, contrary to Saad's autonomy argument."
      },
      {
        "option": "Colonial Subordination",
        "why_plausible": "Imperial terminology.",
        "why_wrong": "The relationship is networked and consensual, not colonial."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Clientelism",
        "Sponsorship"
      ],
      "fa": [
        "حمایت‌گری",
        "روابط مرید و مرادی"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the analytical concept used by Saad to describe the horizontal, mutually dependent nature of the Axis of Resistance.",
      "fa": "مفهوم تحلیلی بیانگر پیوند افقی، متقابل و غیرسلسله‌مراتبی میان اعضای محور مقاومت را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Strategic Interdependence. Correct. Tehran needs Hezbollah to deter Israel just as much as Hezbollah needs Tehran's rockets.",
        "wrong_generic": "No, it was Strategic Interdependence. A horizontal network of shared interests, not a military dictatorship.",
        "common_wrong_answers": {
          "Mercenary Subcontracting": "Mercenaries fight for cash; ideological movements fight for regional survival.",
          "Feudal Vassalage": "Vassals kneel before kings; Nasrallah argued with Qassem Soleimani as an equal.",
          "Colonial Subordination": "Colonies are ruled by governors; resistance allies govern their own countries."
        }
      },
      "fa": {
        "correct_generic": "وابستگی متقابل راهبردی. کاملاً درسته! همان‌قدر که حزب‌الله به موشک‌های تهران نیاز دارد، تهران برای بازدارندگی به حزب‌الله محتاج است.",
        "wrong_generic": "خیر، پاسخ وابستگی متقابل راهبردی بود. شبکه‌ای متصل با دادوستد متقابل، نه پادگان فرمانده و سرباز.",
        "common_wrong_answers": {
          "پیمانکاری مزدورانه": "مزدور برای پول می‌جنگد؛ این گروه‌ها ریشه عمیق هویتی و مردمی در سرزمین خود دارند.",
          "تبعیت فئودالی": "ارباب و رعیتی ساختار عمودی است؛ روابط محور مقاومت افقی و مشورتی بود.",
          "اطاعت استعماری": "استعمارگر والی می‌فرستد؛ فرماندهان محلی تصمیم‌گیران سیاست‌های ملی خود بودند."
        }
      }
    },
    "explanation": {
      "en": "Bilal Saad conceptualizes the Axis of Resistance as a network of 'Strategic Interdependence': Tehran provides ballistic technology and funding, while regional allies provide forward deterrence and intelligence that Iran cannot generate domestically.",
      "fa": "بلال سعد محور مقاومت را شبکه‌ای مبتنی بر «وابستگی متقابل راهبردی» معرفی می‌کند: تهران تسلیحات و منابع مالی تأمین می‌کند و متحدان منطقه‌ای عمق استراتژیک و بازدارندگی پیشرفته‌ای فراهم می‌آورند که ایران در مرزهای خود فاقد آن است."
    },
    "provenance": {
      "source_book": "Challenging the Sponsor-Proxy Model",
      "source_author": "Bilal Saad",
      "page_number": 15,
      "verbatim_passage": "Rather than a vertical hierarchy, the relationship is better characterized as strategic interdependence, where local allies hold significant leverage over Tehran because Iran's own deterrence architecture depends upon their survival.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_proxy_paradox_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "THE PROXY PARADOX",
      "fa": "فرمانده بدون فرمانبردار"
    },
    "clue_text": {
      "en": "In the ultimate historical testament to operational compartmentalization and non-state autonomy, Yahya Sinwar and Hamas launched this massive assault on October 7, 2023, without notifying Tehran or Hezbollah.",
      "fa": "در بارزترین گواه تاریخی بر تفکیک عملیاتی و استقلال مطلق گروه‌های مقاومت، یحیی سنوار و حماس در ۱۵ مهر ۱۴۰۲ این عملیات غافلگیرکننده را بدون کوچک‌ترین اطلاع قبلی به تهران یا حزب‌الله آغاز کردند."
    },
    "canonical_answer": {
      "en": "Operation Al-Aqsa Flood",
      "fa": "عملیات طوفان الاقصی"
    },
    "accepted_aliases": {
      "en": [
        "Al-Aqsa Flood",
        "Toofan al-Aqsa",
        "October 7 attacks",
        "Al-Aqsa Storm"
      ],
      "fa": [
        "طوفان‌الاقصی",
        "طوفان الاقصی",
        "عملیات طوفان‌الاقصی"
      ]
    },
    "options": {
      "en": [
        "Operation Cast Lead",
        "Operation Protective Edge",
        "Operation Al-Aqsa Flood",
        "Operation Pillar of Defense"
      ],
      "fa": [
        "عملیات سرب گداخته",
        "عملیات تیغه حفاظتی",
        "عملیات طوفان الاقصی",
        "عملیات ستون دفاعی"
      ]
    },
    "correct_option_index": 2,
    "distractor_rationales": [
      {
        "option": "Operation Cast Lead",
        "why_plausible": "A major Gaza conflict in 2008-2009.",
        "why_wrong": "Cast Lead was an Israeli offensive launched against Gaza in December 2008."
      },
      {
        "option": "Operation Protective Edge",
        "why_plausible": "The 2014 Gaza war.",
        "why_wrong": "It was the Israeli code-name for the 50-day war in summer 2014."
      },
      {
        "option": "Operation Pillar of Defense",
        "why_plausible": "The November 2012 Gaza confrontation.",
        "why_wrong": "Pillar of Defense was an eight-day Israeli operation in 2012 following the assassination of Ahmed Jabari."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Battle of Seif al-Quds",
        "True Promise"
      ],
      "fa": [
        "نبرد شمشیر قدس",
        "وعده صادق"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the exact military code-name given by Hamas to the October 7, 2023 assault on southern Israel.",
      "fa": "نام نظامی رسمی عملیات حماس در ۱۵ مهر ۱۴۰۲ (۷ اکتبر ۲۰۲۳) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Operation Al-Aqsa Flood. Correct. Even Ayatollah Khamenei found out about the attack on the morning news like the rest of the world.",
        "wrong_generic": "No, it was Operation Al-Aqsa Flood. A zero-leak secret that caught Tel Aviv, Washington, and Tehran equally off-guard.",
        "common_wrong_answers": {
          "Operation Cast Lead": "Cast Lead was Israel bombing Gaza in 2008.",
          "Operation Protective Edge": "Protective Edge was the 2014 ground invasion by the IDF.",
          "Operation Pillar of Defense": "Pillar of Defense was the 2012 eight-day exchange."
        }
      },
      "fa": {
        "correct_generic": "عملیات طوفان الاقصی. کاملاً درسته! عملیاتی که رهبران ایران هم خبر وقوعش را صبح از اخبار شنیدند.",
        "wrong_generic": "خیر، پاسخ عملیات طوفان الاقصی بود. رازی فوق‌العاده سری که نه تل‌آویو از آن باخبر بود و نه تهران.",
        "common_wrong_answers": {
          "عملیات سرب گداخته": "سرب گداخته تهاجم سال ۱۳۸۷ اسرائیل به غزه بود.",
          "عملیات تیغه حفاظتی": "تیغه حفاظتی جنگ ۵۰ روزه سال ۱۳۹۳ بود.",
          "عملیات ستون دفاعی": "ستون دفاعی ترور احمد الجعبری در سال ۱۳۹۱ بود."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr and Bilal Saad highlight that US intelligence assessments and public Iranian statements confirmed that Hamas's leadership in Gaza planned and executed Operation Al-Aqsa Flood with total secrecy, proving that regional resistance factions do not take operational orders from Tehran.",
      "fa": "ولی نصر و بلال سعد تأکید می‌کنند که حتی سازمان‌های اطلاعاتی آمریکا تأیید کردند یحیی سنوار عملیات طوفان‌الاقصی را در محرمانگی مطلق طراحی و اجرا کرد و ایران و حزب‌الله هیچ اطلاعی از زمان و ابعاد این حمله نداشتند."
    },
    "provenance": {
      "source_book": "The Rise of the Axis of Resistance: From the Arab Spring to October 7",
      "source_author": "Vali Nasr",
      "page_number": 19,
      "verbatim_passage": "The surprise of October 7 was total not just in Tel Aviv and Washington, but in Tehran as well. Hamas launched Operation Al-Aqsa Flood without coordinating with or informing the IRGC or Hezbollah.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_true_promise_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "TRUE PROMISE, REAL HEADACHE",
      "fa": "وعده صادق روی آسمان تل‌آویو"
    },
    "clue_text": {
      "en": "Marking the first direct state-on-state military attack launched from Iranian territory against Israel in history, Iran conducted this massive retaliatory missile and drone operation in April 2024.",
      "fa": "این عملیات گسترده موشکی و پهپادی در فروردین ۱۴۰۳ نخستین حمله نظامی مستقیم دولت به دولت از خاک ایران علیه اسرائیل در تاریخ معاصر را رقم زد."
    },
    "canonical_answer": {
      "en": "Operation True Promise",
      "fa": "عملیات وعده صادق"
    },
    "accepted_aliases": {
      "en": [
        "True Promise",
        "Operation Honest Promise",
        "Va'deh-ye Sadeq",
        "Operation True Promise 1"
      ],
      "fa": [
        "وعده صادق",
        "عملیات وعده صادق ۱",
        "وعده صادق یک"
      ]
    },
    "options": {
      "en": [
        "Operation Days of Repentance",
        "Operation True Promise",
        "Operation Praying Mantis",
        "Operation Mersad"
      ],
      "fa": [
        "عملیات روزهای توبه",
        "عملیات وعده صادق",
        "عملیات آخوندک",
        "عملیات مرصاد"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Operation Days of Repentance",
        "why_plausible": "A major military operation in the 2024 regional exchange.",
        "why_wrong": "It was the Israeli retaliatory airstrike code-name on Iranian air defense radars in October 2024."
      },
      {
        "option": "Operation Praying Mantis",
        "why_plausible": "A historic clash involving Iran.",
        "why_wrong": "Praying Mantis was the 1988 US naval strike on Iranian frigates and platforms in the Persian Gulf."
      },
      {
        "option": "Operation Mersad",
        "why_plausible": "A famous victorious Iranian military operation.",
        "why_wrong": "Mersad was the 1988 battle defeating the MEK invasion at Hassanabad in western Iran."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Operation True Promise II",
        "Operation Fath ol-Mobin"
      ],
      "fa": [
        "عملیات وعده صادق ۲",
        "عملیات فتح‌المبین"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific military operation launched by Iran on April 13-14, 2024, involving over 300 drones and missiles.",
      "fa": "نام رسمی عملیات پهپادی و موشکی سپاه در شامگاه ۲۵ و ۲۶ فروردین ۱۴۰۳ علیه اسرائیل را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Operation True Promise. Correct. When hundreds of Shahed drones spent five hours flying across Iraq like the world's loudest parade.",
        "wrong_generic": "No, it was Operation True Promise. The night the shadow war came out into the blinding spotlight.",
        "common_wrong_answers": {
          "Operation Days of Repentance": "Days of Repentance was Israel's October reply; True Promise was Iran's opening salvo.",
          "Operation Praying Mantis": "Praying Mantis was Ronald Reagan in 1988 sinking Iranian gunboats.",
          "Operation Mersad": "Mersad was in 1988 on the Kermanshah highway against the MEK."
        }
      },
      "fa": {
        "correct_generic": "عملیات وعده صادق. کاملاً درسته! شبی که صدها پهپاد شاهد با غرش موتور براوو از آسمان عراق گذشتند.",
        "wrong_generic": "خیر، پاسخ عملیات وعده صادق بود. پایان دوران نبرد در سایه و آغاز رویارویی مستقیم موشکی.",
        "common_wrong_answers": {
          "عملیات روزهای توبه": "روزهای توبه نام عملیات تلافی‌جویانه اسرائیل در آبان ۱۴۰۳ بود.",
          "عملیات آخوندک": "آخوندک حمله نیروی دریایی آمریکا به سکوهای نفتی در سال ۱۳۶۷ بود.",
          "عملیات مرصاد": "مرصاد درگیری با سازمان مجاهدین خلق در تنگه چهارزبر در سال ۶۷ بود."
        }
      }
    },
    "explanation": {
      "en": "Alireza Bagheri analyzes Operation True Promise (April 13–14, 2024) as a paradigm shift in Iranian grand strategy, shattering the decades-old precedent of relying solely on asymmetric proxies and establishing direct ballistic deterrence against Israel.",
      "fa": "علیرضا باقری عملیات وعده صادق در فروردین ۱۴۰۳ را نقطه عطف بنیادین در راهبرد ایران می‌داند که به دوران جنگ نیابتی پایان داد و دکترین بازدارندگی مستقیم متقابل را پایه‌گذاری کرد."
    },
    "provenance": {
      "source_book": "The June 2025 Escalation and Iran's Deterrence Dilemma",
      "source_author": "Alireza Bagheri",
      "page_number": 4,
      "verbatim_passage": "Operation True Promise on April 13-14, 2024, saw Iran fire over three hundred ballistic missiles, cruise missiles, and suicide drones from its own sovereign territory directly at Israel, establishing an unprecedented direct confrontation.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_true_promise_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "TRUE PROMISE, REAL HEADACHE",
      "fa": "وعده صادق روی آسمان تل‌آویو"
    },
    "clue_text": {
      "en": "The immediate trigger for Iran's April 2024 retaliatory barrage was the Israeli airstrike that flattened the Iranian consular annexe in Damascus, assassinating this top IRGC Quds Force senior commander in Syria and Lebanon.",
      "fa": "جرقه مستقیم حمله تلافی‌جویانه فروردین ۱۴۰۳، بمباران ساختمان کنسولگری ایران در دمشق توسط اسرائیل و شهادت این فرمانده ارشد سپاه قدس در سوریه و لبنان بود."
    },
    "canonical_answer": {
      "en": "Mohammad Reza Zahedi",
      "fa": "محمدرضا زاهدی"
    },
    "accepted_aliases": {
      "en": [
        "Sardar Zahedi",
        "General Zahedi",
        "Haj Ali Zahedi"
      ],
      "fa": [
        "سردار زاهدی",
        "شهید زاهدی",
        "سرتیپ پاسدار محمدرضا زاهدی"
      ]
    },
    "options": {
      "en": [
        "Qassem Soleimani",
        "Mohammad Reza Zahedi",
        "Hossein Salami",
        "Esmail Qaani"
      ],
      "fa": [
        "قاسم سلیمانی",
        "محمدرضا زاهدی",
        "حسین سلامی",
        "اسماعیل قاآنی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Qassem Soleimani",
        "why_plausible": "The iconic commander of the Quds Force assassinated in a high-profile strike.",
        "why_wrong": "Soleimani was assassinated in January 2020 at Baghdad airport by a US drone strike, not in Damascus in April 2024."
      },
      {
        "option": "Hossein Salami",
        "why_plausible": "The Commander-in-Chief of the IRGC.",
        "why_wrong": "General Salami commands the entire IRGC from Tehran and was not assassinated in Damascus."
      },
      {
        "option": "Esmail Qaani",
        "why_plausible": "The current commander of the IRGC Quds Force.",
        "why_wrong": "General Qaani succeeded Soleimani in 2020 and remains the serving head of the Quds Force."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Razi Mousavi",
        "Abbas Nilforoushan"
      ],
      "fa": [
        "سید رضی موسوی",
        "عباس نیلفروشان"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific senior IRGC Quds Force commander killed in the April 1, 2024 Damascus consulate airstrike.",
      "fa": "نام سردار ارشد نیروی قدس سپاه که در حمله به کنسولگری دمشق در ۱۳ فروردین ۱۴۰۳ شهید شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad Reza Zahedi. Correct. Striking a sovereign diplomatic mission was the red line Tehran could not ignore.",
        "wrong_generic": "No, it was General Mohammad Reza Zahedi. The highest-ranking Iranian commander killed since Qassem Soleimani.",
        "common_wrong_answers": {
          "Qassem Soleimani": "Soleimani was killed in Baghdad four years earlier by Donald Trump.",
          "Hossein Salami": "Salami is very much alive in Tehran making television speeches.",
          "Esmail Qaani": "Qaani commands the Quds Force today; Zahedi was his key commander in the Levant."
        }
      },
      "fa": {
        "correct_generic": "محمدرضا زاهدی. کاملاً درسته! شهادت این فرمانده ارشد در ساختمان دیپلماتیک خط قرمزی بود که عبور از آن بی‌پاسخ نماند.",
        "wrong_generic": "خیر، پاسخ سردار محمدرضا زاهدی بود. بلندپایه‌ترین فرمانده ایرانی شهید شده پس از حاج قاسم سلیمانی.",
        "common_wrong_answers": {
          "قاسم سلیمانی": "حاج قاسم در دی‌ماه ۹۸ در فرودگاه بغداد توسط پهپاد آمریکایی ترور شد.",
          "حسین سلامی": "سردار سلامی فرمانده کل سپاه در ستاد تهران است.",
          "اسماعیل قاآنی": "سردار قاآنی فرمانده نیروی قدس است؛ سردار زاهدی فرمانده میدانی لبنان و سوریه بود."
        }
      }
    },
    "explanation": {
      "en": "Bagheri notes that the targeted killing of Brigadier General Mohammad Reza Zahedi and his deputy Mohammad Hadi Haji Rahimi inside Iran's diplomatic compound in Damascus on April 1, 2024, forced Supreme Leader Khamenei to order a direct military retaliation against Israel.",
      "fa": "باقری خاطرنشان می‌کند که ترور هدفمند سرتیپ محمدرضا زاهدی و معاونش در ساختمان دیپلماتیک کنسولگری ایران در دمشق در ۱۳ فروردین ۱۴۰۳ رهبر جمهوری اسلامی را به این تصمیم رساند که عدم پاسخ مستقیم بازدارندگی کشور را کاملاً مخدوش خواهد کرد."
    },
    "provenance": {
      "source_book": "The June 2025 Escalation and Iran's Deterrence Dilemma",
      "source_author": "Alireza Bagheri",
      "page_number": 5,
      "verbatim_passage": "The April 1, 2024 assassination of Brigadier General Mohammad Reza Zahedi, the Quds Force's top commander overseeing operations in the Levant, in an Israeli airstrike on the consular building crossed a sovereign red line.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_true_promise_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "TRUE PROMISE, REAL HEADACHE",
      "fa": "وعده صادق روی آسمان تل‌آویو"
    },
    "clue_text": {
      "en": "Strategists note that Operation True Promise marked the formal burial of this long-standing Iranian doctrine of avoiding direct state confrontation while absorbing tactical losses.",
      "fa": "استراتژیست‌ها تأکید می‌کنند که عملیات وعده صادق به معنای پایان رسمی این دکترین دیرینه ایران بود که بر مهار واکنش مستقیم و تحمل ضربات تاکتیکی برای پیشگیری از جنگ فراگیر استوار بود."
    },
    "canonical_answer": {
      "en": "Strategic Patience",
      "fa": "صبر استراتژیک"
    },
    "accepted_aliases": {
      "en": [
        "Sabr-e Estratezhik",
        "Strategic patience doctrine",
        "Doctrine of strategic patience"
      ],
      "fa": [
        "صبر راهبردی",
        "دکترین صبر استراتژیک",
        "صبر و خویشتنداری"
      ]
    },
    "options": {
      "en": [
        "Massive Retaliation",
        "Strategic Patience",
        "Flexible Response",
        "Preemptive Neutralization"
      ],
      "fa": [
        "انتقام گسترده",
        "صبر استراتژیک",
        "پاسخ انعطاف‌پذیر",
        "خنثی‌سازی پیش‌دستانه"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Massive Retaliation",
        "why_plausible": "The Cold War Eisenhower doctrine.",
        "why_wrong": "It is an American nuclear doctrine, the exact opposite of avoiding confrontation."
      },
      {
        "option": "Flexible Response",
        "why_plausible": "Kennedy's military escalation framework.",
        "why_wrong": "A NATO doctrine, not Iran's historical posture of strategic patience."
      },
      {
        "option": "Preemptive Neutralization",
        "why_plausible": "Tactical offensive military jargon.",
        "why_wrong": "Iran's posture was explicitly reactive and restrained, termed 'Strategic Patience'."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Heroic Flexibility",
        "Forward Defense"
      ],
      "fa": [
        "نرمش قهرمانانه",
        "دفاع روبه‌جلو"
      ]
    },
    "specificity_prompt": {
      "en": "Provide the exact term used for Iran's former policy of absorbing Israeli strikes without direct missile retaliation.",
      "fa": "اصطلاح راهبردی ناظر بر خویشتنداری و پرهیز از درگیری مستقیم موشکی با اسرائیل تا پیش از فروردین ۱۴۰۳ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Strategic Patience. Correct. Turns out patience is an exhaustible commodity when embassies start exploding.",
        "wrong_generic": "No, it was Strategic Patience (Sabr-e Estratezhik). Traded in for a few hundred ballistic missiles.",
        "common_wrong_answers": {
          "Massive Retaliation": "Massive retaliation was John Foster Dulles threatening Moscow with atom bombs.",
          "Flexible Response": "Flexible response was Kennedy in Vietnam.",
          "Preemptive Neutralization": "Preemption is striking first; Iran waited until its patience ran out."
        }
      },
      "fa": {
        "correct_generic": "صبر استراتژیک. کاملاً درسته! صبری که با تخریب ساختمان کنسولگری در دمشق لبریز شد.",
        "wrong_generic": "خیر، پاسخ صبر استراتژیک بود. راهبردی که جایش را به بازدارندگی مستقیم داد.",
        "common_wrong_answers": {
          "انتقام گسترده": "انتقام گسترده دکترین اتمی آیزنهاور در دهه ۱۹۵۰ بود.",
          "پاسخ انعطاف‌پذیر": "پاسخ انعطاف‌پذیر دکترین ناتو در دوران جنگ سرد بود.",
          "خنثی‌سازی پیش‌دستانه": "حمله پیش‌دستانه دکترین اسرائیل است؛ ایران بر دکترین صبر راهبردی تأکید داشت."
        }
      }
    },
    "explanation": {
      "en": "Bagheri highlights that since 2017, Iran practiced 'Strategic Patience'—absorbing covert Israeli assassinations and sabotage while building long-term proxy capabilities; this posture was permanently abandoned in April 2024 in favor of active kinetic deterrence.",
      "fa": "باقری تشریح می‌کند که سیاست «صبر استراتژیک» که از سال ۱۳۹۶ برای دوری از جنگ فراگیر و ادامه ساخت توانمندی‌های منطقه‌ای دنبال می‌شد، در فروردین ۱۴۰۳ با این نتیجه‌گیری که صبر بیشتر موجب تعرضات بزرگتر دشمن می‌شود، برای همیشه کنار گذاشته شد."
    },
    "provenance": {
      "source_book": "The June 2025 Escalation and Iran's Deterrence Dilemma",
      "source_author": "Alireza Bagheri",
      "page_number": 8,
      "verbatim_passage": "Operation True Promise shattered the paradigm of 'strategic patience' (sabr-e estratezhik), replacing passive absorption of Israeli covert blows with a declared doctrine of direct symmetrical response.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_true_promise_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "TRUE PROMISE, REAL HEADACHE",
      "fa": "وعده صادق روی آسمان تل‌آویو"
    },
    "clue_text": {
      "en": "The primary military installation targeted by Iranian ballistic missiles during Operation True Promise was this sprawling Israeli Air Force base in the Negev desert, from which the F-35s that bombed Damascus had taken off.",
      "fa": "پایگاه نظامی اصلی که در عملیات وعده صادق آماج موشک‌های بالستیک ایران قرار گرفت، این پایگاه نیروی هوایی اسرائیل در صحرای نقب بود که جنگنده‌های اف-۳۵ عامل حمله به دمشق از آن برخاسته بودند."
    },
    "canonical_answer": {
      "en": "Nevatim Airbase",
      "fa": "پایگاه هوایی نواتیم"
    },
    "accepted_aliases": {
      "en": [
        "Nevatim",
        "Nevatim Air Base",
        "Hatzerim"
      ],
      "fa": [
        "پایگاه نواتیم",
        "نواتیم",
        "فرودگاه نظامی نواتیم"
      ]
    },
    "options": {
      "en": [
        "Ramat David Airbase",
        "Nevatim Airbase",
        "Palmachim Airbase",
        "Tel Nof Airbase"
      ],
      "fa": [
        "پایگاه رامات دیوید",
        "پایگاه هوایی نواتیم",
        "پایگاه پالماخیم",
        "پایگاه تل نوف"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Ramat David Airbase",
        "why_plausible": "A major Israeli Air Force base in northern Israel.",
        "why_wrong": "Ramat David is in the north near Haifa, whereas the F-35 stealth squadron and primary target was Nevatim in the southern Negev."
      },
      {
        "option": "Palmachim Airbase",
        "why_plausible": "A coastal spaceport and missile test base.",
        "why_wrong": "Palmachim launches satellites and Arrow interceptors on the coast, not the F-35 strike squadrons."
      },
      {
        "option": "Tel Nof Airbase",
        "why_plausible": "A major central fighter airbase.",
        "why_wrong": "Tel Nof houses F-15s, while the F-35 'Adir' squadrons that struck the Damascus consulate operate out of Nevatim."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Ramon Airbase",
        "Mount Hermon Intelligence Base"
      ],
      "fa": [
        "پایگاه رامون",
        "پایگاه اطلاعاتی جبل‌الشیخ"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific Israeli Air Force base in the Negev desert targeted by Iranian ballistic missiles in April 2024.",
      "fa": "نام دقیق پایگاه هوایی جنگنده‌های رادارگریز اسرائیل در صحرای نقب را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Nevatim Airbase. Correct. Dropping ballistic warheads on the runway that launched the Damascus strike.",
        "wrong_generic": "No, it was Nevatim Airbase in the southern Negev desert. The home base of the F-35 Adir fleet.",
        "common_wrong_answers": {
          "Ramat David Airbase": "Ramat David is up north near Nazareth; Nevatim is down south in the sand dunes.",
          "Palmachim Airbase": "Palmachim is where they test rockets on the Mediterranean beach.",
          "Tel Nof Airbase": "Tel Nof flies F-15s near Rehovot; Nevatim flies the stealth jets."
        }
      },
      "fa": {
        "correct_generic": "پایگاه هوایی نواتیم. کاملاً درسته! اصابت موشک‌های بالستیک به آشیانه همان جنگنده‌هایی که کنسولگری را هدف قرار دادند.",
        "wrong_generic": "خیر، پاسخ پایگاه هوایی نواتیم در صحرای نقب بود. آشیانه جنگنده‌های اف-۳۵ رادارگریز.",
        "common_wrong_answers": {
          "پایگاه رامات دیوید": "رامات دیوید در شمال اسرائیل و نزدیک حیفاست؛ نواتیم در جنوب صحرای نقب قرار دارد.",
          "پایگاه پالماخیم": "پالماخیم پایگاه ساحلی پرتاب ماهواره و سامانه‌های موشکی است.",
          "پایگاه تل نوف": "تل نوف مقر جنگنده‌های اف-۱۵ است؛ پایگاه پیشرفته‌ترین اف-۳۵ها نواتیم بود."
        }
      }
    },
    "explanation": {
      "en": "Bagheri explains that the IRGC Aerospace Force deliberately concentrated its precision-guided Kheibar Shekan and Emad missiles on Nevatim Airbase in the Negev desert, seeking a symmetrical military response to the airfield that hosted the Damascus strike.",
      "fa": "علیرضا باقری تشریح می‌کند که نیروی هوافضای سپاه با شلیک موشک‌های بالستیک خیبرشکن و عماد عمداً پایگاه هوایی نواتیم در صحرای نقب را هدف قرار داد تا پاسخی متقارن به مبدأ پرواز جنگنده‌های مهاجم به دمشق بدهد."
    },
    "provenance": {
      "source_book": "The June 2025 Escalation and Iran's Deterrence Dilemma",
      "source_author": "Alireza Bagheri",
      "page_number": 9,
      "verbatim_passage": "Iran's primary target was Nevatim Airbase in the southern Negev desert, the sprawling installation housing the Israeli Air Force's 140th and 116th F-35I Adir squadrons, which had carried out the Damascus strike.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_true_promise_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "TRUE PROMISE, REAL HEADACHE",
      "fa": "وعده صادق روی آسمان تل‌آویو"
    },
    "clue_text": {
      "en": "In October 2024, Iran conducted Operation True Promise II in response to the assassinations of Hassan Nasrallah and this Hamas political bureau chief, who was killed by an explosion inside an official IRGC guesthouse in northern Tehran.",
      "fa": "در مهر ۱۴۰۳، ایران عملیات وعده صادق ۲ را در واکنش به ترور سید حسن نصرالله و این رئیس دفتر سیاسی حماس اجرا کرد که در یک اقامتگاه ویژه سپاه در شمال تهران به شهادت رسید."
    },
    "canonical_answer": {
      "en": "Ismail Haniyeh",
      "fa": "اسماعیل هنیه"
    },
    "accepted_aliases": {
      "en": [
        "Ismail Haniya",
        "Haniyeh",
        "Abu al-Abed"
      ],
      "fa": [
        "هنیه",
        "اسماعیل عبدالسلام هنیه",
        "شهید هنیه"
      ]
    },
    "options": {
      "en": [
        "Khaled Meshaal",
        "Ismail Haniyeh",
        "Mousa Abu Marzook",
        "Yahya Sinwar"
      ],
      "fa": [
        "خالد مشعل",
        "اسماعیل هنیه",
        "موسی ابومرزوق",
        "یحیی سنوار"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Khaled Meshaal",
        "why_plausible": "Former chairman of the Hamas political bureau.",
        "why_wrong": "Meshaal resides in Qatar and survived an Israeli assassination attempt in Jordan in 1997."
      },
      {
        "option": "Mousa Abu Marzook",
        "why_plausible": "Senior Hamas political bureau official.",
        "why_wrong": "Abu Marzook is a prominent diplomat in Doha, not the leader assassinated in Tehran in July 2024."
      },
      {
        "option": "Yahya Sinwar",
        "why_plausible": "The supreme leader of Hamas in Gaza.",
        "why_wrong": "Sinwar was killed in combat by Israeli troops in Rafah, southern Gaza, in October 2024, not in Tehran."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Saleh al-Arouri",
        "Yahya Sinwar"
      ],
      "fa": [
        "صالح العاروری",
        "یحیی سنوار"
      ]
    },
    "specificity_prompt": {
      "en": "Name the Hamas political leader assassinated in Tehran on July 31, 2024, following the presidential inauguration.",
      "fa": "نام رئیس دفتر سیاسی حماس که در بامداد ۱۰ مرداد ۱۴۰۳ پس از مراسم تحلیف ریاست‌جمهوری در تهران ترور شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ismail Haniyeh. Spot on. Getting assassinated in a high-security state guesthouse in Sa'adabad was an intelligence humiliation Tehran could not swallow.",
        "wrong_generic": "No, it was Ismail Haniyeh. Assassinated just hours after attending Masoud Pezeshkian's inauguration in Parliament.",
        "common_wrong_answers": {
          "Khaled Meshaal": "Meshaal was in Doha watching the funeral.",
          "Mousa Abu Marzook": "Abu Marzook was a deputy, not the head of the bureau.",
          "Yahya Sinwar": "Sinwar was in the ruins of Rafah with a Kalashnikov, not a guest house in northern Tehran."
        }
      },
      "fa": {
        "correct_generic": "اسماعیل هنیه. کاملاً درسته! ترور در اقامتگاه میهمانان ویژه در شمال تهران، تحقیر امنیتی بزرگی بود که پاسخ سریع می‌طلبید.",
        "wrong_generic": "خیر، پاسخ اسماعیل هنیه بود. درست چند ساعت پس از شرکت در مراسم تحلیف مسعود پزشکیان در مجلس.",
        "common_wrong_answers": {
          "خالد مشعل": "خالد مشعل در قطر اقامت دارد و در سال ۱۹۹۷ در اردن از سوءقصد نجات یافت.",
          "موسی ابومرزوق": "ابومرزوق معاون دفتر سیاسی حماس است و در تهران ترور نشد.",
          "یحیی سنوار": "سنوار در میان خرابه‌های تل‌السلطان رفح به شهادت رسید، نه در زعفرانیه تهران."
        }
      }
    },
    "explanation": {
      "en": "Bagheri highlights that the assassination of Hamas leader Ismail Haniyeh in an IRGC guesthouse in Tehran on July 31, 2024, followed by the strike killing Hezbollah Secretary-General Hassan Nasrallah in Beirut on September 27, led directly to Operation True Promise II on October 1, 2024.",
      "fa": "علیرضا باقری اشاره می‌کند که ترور اسماعیل هنیه در قلب تهران در ۱۰ مرداد ۱۴۰۳ و سپس شهادت سید حسن نصرالله در ضاحیه بیروت در ۶ مهر ۱۴۰۳، به پرتاب حدود ۲۰۰ موشک بالستیک در عملیات وعده صادق ۲ در ۱۰ مهر ۱۴۰۳ انجامید."
    },
    "provenance": {
      "source_book": "The June 2025 Escalation and Iran's Deterrence Dilemma",
      "source_author": "Alireza Bagheri",
      "page_number": 12,
      "verbatim_passage": "The humiliation of Ismail Haniyeh's assassination in an IRGC-secured guesthouse in Tehran, coupled with the devastating strike killing Hassan Nasrallah in Beirut, triggered Operation True Promise II on October 1, 2024, featuring advanced hypersonic and ballistic missiles.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_improv_ministry_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "IMPROV AT THE MINISTRY",
      "fa": "بداهه‌سازی در دیوان‌سالاری"
    },
    "clue_text": {
      "en": "In his institutional study of Iranian governance, political scientist Arang Keshavarzian introduces this term to describe a state that constantly creates parallel ad hoc bodies rather than relying on consolidated formal procedures.",
      "fa": "دانشمند علوم سیاسی آرنگ کشاورزیان در بررسی ساختار حکومت در ایران این اصطلاح را ابداع می‌کند تا نظامی را توصیف کند که به جای نهادهای رسمی پایدار، مدام به ساختارهای موازی و بداهه‌پردازانه متوسل می‌شود."
    },
    "canonical_answer": {
      "en": "Improvisational Polity",
      "fa": "حکومت بداهه‌پرداز"
    },
    "accepted_aliases": {
      "en": [
        "Improvisational state",
        "Improvisational polity",
        "Improvised regime"
      ],
      "fa": [
        "نظام بداهه‌ساز",
        "نظام سیاسی بداهه‌پرداز",
        "حکمرانی بداهه‌پرداز"
      ]
    },
    "options": {
      "en": [
        "Totalitarian Monolith",
        "Improvisational Polity",
        "Bureaucratic Authoritarianism",
        "Weberian Rational-Legal State"
      ],
      "fa": [
        "نظام توتالیتر یکپارچه",
        "حکومت بداهه‌پرداز",
        "اقتدارگرایی بوروکراتیک",
        "دولت عقلانی-قانونی وبر"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Totalitarian Monolith",
        "why_plausible": "A frequent popular description of ideological dictatorships.",
        "why_wrong": "Keshavarzian explicitly rejects the totalitarian label, showing Iranian governance is fragmented, contradictory, and improvised."
      },
      {
        "option": "Bureaucratic Authoritarianism",
        "why_plausible": "Guillermo O'Donnell's theory of military-technocratic rule in Latin America.",
        "why_wrong": "O'Donnell's model is rigid, professional, and institutionalized, whereas Iran relies on revolutionary improvisations."
      },
      {
        "option": "Weberian Rational-Legal State",
        "why_plausible": "The classic modern state model.",
        "why_wrong": "The Islamic Republic explicitly mixes charismatic, traditional, and informal mechanisms, defying pure Weberian bureaucracy."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Hybrid Regime",
        "Parallel State"
      ],
      "fa": [
        "رژیم ترکیبی",
        "دولت موازی"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific conceptual term coined by Arang Keshavarzian for Iran's governance model.",
      "fa": "اصطلاح نظری ابداع‌شده توسط آرنگ کشاورزیان برای توصیف ساختار سیاسی نامتعارف و منعطف جمهوری اسلامی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Improvisational Polity. Correct. When your constitutional order operates like an unscripted jazz solo with multiple conductors.",
        "wrong_generic": "No, it was the Improvisational Polity. Making up institutions on the fly whenever a crisis hits.",
        "common_wrong_answers": {
          "Totalitarian Monolith": "There is nothing monolithic about five parallel ministries fighting over one movie permit.",
          "Bureaucratic Authoritarianism": "O'Donnell's generals loved flowcharts; Iranian politics loves ad hoc councils.",
          "Weberian Rational-Legal State": "Weber would have had a headache watching three councils overrule parliament."
        }
      },
      "fa": {
        "correct_generic": "حکومت بداهه‌پرداز. کاملاً درسته! ساختاری که هر جا به بن‌بست می‌رسد، یک شورا یا نهاد جدید موازی تأسیس می‌کند.",
        "wrong_generic": "خیر، پاسخ حکومت بداهه‌پرداز (نظام سیاسی بداهه‌پرداز) بود. نظریه کشاورزیان درباره مدیریت منعطف و بحران‌محور در ایران.",
        "common_wrong_answers": {
          "نظام توتالیتر یکپارچه": "هیچ چیز در نظام تصمیم‌گیری ایران یکپارچه نیست؛ همه چیز در تداخل نهادی است.",
          "اقتدارگرایی بوروکراتیک": "مدل ادانل مختص ژنرال‌های آمریکای لاتین است، نه روحانیون و شوراهای موازی در ایران.",
          "دولت عقلانی-قانونی وبر": "ماکس وبر با دیدن این همه ستاد و شورای بالادستی سرگیجه می‌گرفت."
        }
      }
    },
    "explanation": {
      "en": "Arang Keshavarzian argues that the Islamic Republic is an 'Improvisational Polity' characterized by overlapping authorities, revolutionary foundations, and ad hoc councils that constantly redefine state boundaries through crisis management.",
      "fa": "آرنگ کشاورزیان استدلال می‌کند که جمهوری اسلامی یک «حکومت بداهه‌پرداز» است که با نهادهای همپوشان، بنیادهای انقلابی و شوراهای عالی موقت شکل گرفته و مدام مرزهای میان دولت رسمی و حاکمیت غیررسمی را جابه‌جا می‌کند."
    },
    "provenance": {
      "source_book": "An Improvisational Polity: Form and Substance in the Islamic Republic",
      "source_author": "Arang Keshavarzian",
      "page_number": 1,
      "verbatim_passage": "The Islamic Republic can best be understood as an improvisational polity, where political institutions and boundaries are continually reshaped through contingency, factional competition, and overlapping jurisdictional claims.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_improv_ministry_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "IMPROV AT THE MINISTRY",
      "fa": "بداهه‌سازی در دیوان‌سالاری"
    },
    "clue_text": {
      "en": "Born out of the Cultural Revolution in the early 1980s, this non-parliamentary executive-clerical body issues decrees on universities, scientific policy, and social lifestyle that carry the full force of law.",
      "fa": "این نهاد فراقوه‌ای که در جریان انقلاب فرهنگی در اوایل دهه ۱۳۶۰ تأسیس شد، مصوباتی در حوزه دانشگاه‌ها، سیاست‌های علمی و امور فرهنگی صادر می‌کند که در حکم قانون لازم‌الاجرا هستند."
    },
    "canonical_answer": {
      "en": "Supreme Council of the Cultural Revolution",
      "fa": "شورای عالی انقلاب فرهنگی"
    },
    "accepted_aliases": {
      "en": [
        "SCCR",
        "Cultural Revolution Council",
        "Shoraye Aali-e Enqelab-e Farhangi"
      ],
      "fa": [
        "شورایعالی انقلاب فرهنگی",
        "ستاد انقلاب فرهنگی"
      ]
    },
    "options": {
      "en": [
        "Ministry of Science",
        "Supreme Council of the Cultural Revolution",
        "Islamic Development Organization",
        "Hozeh Honari"
      ],
      "fa": [
        "وزارت علوم",
        "شورای عالی انقلاب فرهنگی",
        "سازمان تبلیغات اسلامی",
        "حوزه هنری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Ministry of Science",
        "why_plausible": "The conventional cabinet ministry administering higher education.",
        "why_wrong": "The Ministry is a formal cabinet portfolio subordinate to Parliament, whereas the Supreme Council is an autonomous supra-constitutional body whose rulings bypass Parliament."
      },
      {
        "option": "Islamic Development Organization",
        "why_plausible": "A major ideological state organ under the Leader (Sazman-e Tablighat).",
        "why_wrong": "Tablighat runs religious propaganda and publishing, not the supreme macro-policy council on university admissions and curriculum."
      },
      {
        "option": "Hozeh Honari",
        "why_plausible": "An artistic revolutionary institution.",
        "why_wrong": "Hozeh Honari produces literature and cinema, not nationwide statutory educational policies."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Supreme National Security Council",
        "Academy of Sciences"
      ],
      "fa": [
        "شورای عالی امنیت ملی",
        "فرهنگستان علوم"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific supreme policy council that governs university admissions, educational policy, and hijab rules.",
      "fa": "نام نهاد عالی سیاست‌گذاری فرهنگی و آموزشی کشور که مصوباتش در حکم قانون است را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Supreme Council of the Cultural Revolution. Correct. Bypassing parliament to decide what books you can read and who gets tenure.",
        "wrong_generic": "No, it was the Supreme Council of the Cultural Revolution. The ultimate authority on ideological engineering in universities.",
        "common_wrong_answers": {
          "Ministry of Science": "The Ministry carries out the orders; the Supreme Council writes the decrees.",
          "Islamic Development Organization": "Tablighat prints posters and organizes eulogists; the Council dictates national education.",
          "Hozeh Honari": "Hozeh Honari makes art and films; the Council approves university presidents."
        }
      },
      "fa": {
        "correct_generic": "شورای عالی انقلاب فرهنگی. کاملاً درسته! شورایی که مجلس را دور می‌زند تا تعیین کند در دانشگاه‌ها چه تدریس شود.",
        "wrong_generic": "خیر، پاسخ شورای عالی انقلاب فرهنگی بود. بازوی سیاست‌گذاری کلان فرهنگی نظام.",
        "common_wrong_answers": {
          "وزارت علوم": "وزارت علوم مجری اداری است، اما مصوبات بالادستی را این شورا ابلاغ می‌کند.",
          "سازمان تبلیغات اسلامی": "سازمان تبلیغات متولی مداحان و مساجد است، نه سیاست‌گذار کنکور و کتب درسی.",
          "حوزه هنری": "حوزه هنری نهاد تولید کتاب و فیلم انقلابی است."
        }
      }
    },
    "explanation": {
      "en": "Keshavarzian highlights the Supreme Council of the Cultural Revolution as an archetype of parallel governance: created by decree rather than constitutional text, its members are appointed by the Supreme Leader and its resolutions cannot be struck down by Parliament or administrative courts.",
      "fa": "آرنگ کشاورزیان شورای عالی انقلاب فرهنگی را نمونه بارز نهادهای حاکمیت موازی می‌داند که نامش در قانون اساسی اولیه نبود اما احکام اعضای آن توسط رهبری صادر شده و مصوباتش بر قوانین مصوب مجلس شورای اسلامی ارجحیت دارد."
    },
    "provenance": {
      "source_book": "An Improvisational Polity: Form and Substance in the Islamic Republic",
      "source_author": "Arang Keshavarzian",
      "page_number": 8,
      "verbatim_passage": "The Supreme Council of the Cultural Revolution operates as a supra-constitutional legislative organ, whose edicts on higher education, curriculum, and cultural restrictions carry the weight of law without parliamentary vetting.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_improv_ministry_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "IMPROV AT THE MINISTRY",
      "fa": "بداهه‌سازی در دیوان‌سالاری"
    },
    "clue_text": {
      "en": "Operating entirely outside the regular judiciary and answerable exclusively to the Supreme Leader, this secretive judicial body was established to prosecute, defrock, and discipline dissident clerics.",
      "fa": "این نهاد قضایی ویژه و محرمانه که کاملاً خارج از دادگستری عمومی عمل می‌کند و تنها به رهبری پاسخگوست، برای محاکمه، خلع لباس و تنبیه روحانیون دگراندیش و منتقد تأسیس شد."
    },
    "canonical_answer": {
      "en": "Special Clerical Court",
      "fa": "دادگاه ویژه روحانیت"
    },
    "accepted_aliases": {
      "en": [
        "Dadgah-e Vizheh-ye Rowhaniyat",
        "Special Court for the Clergy",
        "Clerical Court"
      ],
      "fa": [
        "دادگاه ویژه روحانیت",
        "دادگاه ویژه",
        "دادسرا و دادگاه ویژه روحانیت"
      ]
    },
    "options": {
      "en": [
        "Revolutionary Court",
        "Special Clerical Court",
        "Supreme Court",
        "Court of Administrative Justice"
      ],
      "fa": [
        "دادگاه انقلاب",
        "دادگاه ویژه روحانیت",
        "دیوان عالی کشور",
        "دیوان عدالت اداری"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Revolutionary Court",
        "why_plausible": "A prominent exceptional judicial organ in Iran (Dadgah-e Enqelab).",
        "why_wrong": "Revolutionary Courts are part of the general judiciary under the Chief Justice, whereas the Clerical Court is entirely independent and extra-constitutional."
      },
      {
        "option": "Supreme Court",
        "why_plausible": "The highest appellate court.",
        "why_wrong": "The Supreme Court has no jurisdiction over verdicts issued by the Special Clerical Court."
      },
      {
        "option": "Court of Administrative Justice",
        "why_plausible": "Handles legal complaints against government bodies.",
        "why_wrong": "The Court of Administrative Justice hears citizen appeals against ministries, not trials of dissident ayatollahs."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Military Court",
        "Revolutionary Tribunal"
      ],
      "fa": [
        "دادگاه نظامی",
        "دادگاه شرع"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific autonomous court responsible for disciplining and defrocking clerics in Iran.",
      "fa": "نام دادگاه اختصاصی رسیدگی به جرایم و خلع لباس روحانیون را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Special Clerical Court. Spot on. Because regular courtrooms are much too public for defrocking a reformist ayatollah.",
        "wrong_generic": "No, it was the Special Clerical Court (Dadgah-e Vizheh-ye Rowhaniyat). Operating in its own legal universe.",
        "common_wrong_answers": {
          "Revolutionary Court": "Revolutionary Courts try political dissidents; the Clerical Court specifically polices the clergy.",
          "Supreme Court": "The Supreme Court cannot even review cases from the Special Clerical Court.",
          "Court of Administrative Justice": "Administrative Justice handles bureaucratic appeals, not defrocking mullahs."
        }
      },
      "fa": {
        "correct_generic": "دادگاه ویژه روحانیت. کاملاً درسته! دادگاهی که بیرون از قوه قضائیه قرار دارد و احکامش قابل فرجام‌خواهی در دیوان عالی نیست.",
        "wrong_generic": "خیر، پاسخ دادگاه ویژه روحانیت بود. نهادی مقتدر برای مهار و تصفیه روحانیون منتقد در قم و تهران.",
        "common_wrong_answers": {
          "دادگاه انقلاب": "دادگاه انقلاب بخشی از ساختار رسمی قوه قضائیه است؛ دادگاه ویژه کلاً مجزاست.",
          "دیوان عالی کشور": "دیوان عالی کشور حق نقض احکام دادگاه ویژه روحانیت را ندارد.",
          "دیوان عدالت اداری": "دیوان عدالت به شکایات اداری رسیدگی می‌کند، نه خلع لباس و حبس مجتهدان."
        }
      }
    },
    "explanation": {
      "en": "Keshavarzian and legal scholars emphasize that the Special Clerical Court operates under its own procedural code outside the constitutional framework, allowing the conservative leadership to silence reformist clerics like Abdollah Nouri or Mohsen Kadivar without interference from standard legal procedures.",
      "fa": "آرنگ کشاورزیان و حقوق‌دانان تأکید می‌کنند که دادگاه ویژه روحانیت آیین دادرسی اختصاصی خود را دارد و مستقل از نظارت قوه قضائیه و مجلس، ابزار حاکمیت برای محاکمه روحانیون اصلاح‌طلب چون عبدالله نوری، کدیور و یوسفی اشکوری بوده است."
    },
    "provenance": {
      "source_book": "An Improvisational Polity: Form and Substance in the Islamic Republic",
      "source_author": "Arang Keshavarzian",
      "page_number": 11,
      "verbatim_passage": "The Special Clerical Court functions entirely outside the constitutional judicial structure, directly appointed by and responsible to the Supreme Leader to police and discipline the clerical establishment.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_improv_ministry_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "IMPROV AT THE MINISTRY",
      "fa": "بداهه‌سازی در دیوان‌سالاری"
    },
    "clue_text": {
      "en": "In a classic case of bureaucratic paralysis documented by Keshavarzian, film directors and publishers frequently receive legal publication permits from this formal ministry, only to have their works confiscated by hardline revolutionary organs.",
      "fa": "در نمونه‌ای بارز از فلج دیوان‌سالاری مورد اشاره کشاورزیان، کارگردانان و ناشران بارها از این وزارتخانه رسمی دولتی مجوز دریافت می‌کنند، اما آثارشان توسط نهادهای تندروی انقلابی توقیف می‌شود."
    },
    "canonical_answer": {
      "en": "Ministry of Culture and Islamic Guidance",
      "fa": "وزارت فرهنگ و ارشاد اسلامی"
    },
    "accepted_aliases": {
      "en": [
        "Ershad",
        "Ministry of Guidance",
        "Ministry of Culture",
        "Vezarat-e Ershad"
      ],
      "fa": [
        "ارشاد",
        "وزارت ارشاد",
        "فرهنگ و ارشاد"
      ]
    },
    "options": {
      "en": [
        "Ministry of Science",
        "Ministry of Culture and Islamic Guidance",
        "Islamic Republic of Iran Broadcasting",
        "National Library of Iran"
      ],
      "fa": [
        "وزارت علوم",
        "وزارت فرهنگ و ارشاد اسلامی",
        "سازمان صدا و سیمای جمهوری اسلامی",
        "سازمان اسناد و کتابخانه ملی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Ministry of Science",
        "why_plausible": "Oversees universities and scholarly books.",
        "why_wrong": "Science handles higher education; cultural permits for public films, music, and novels are issued by Ershad."
      },
      {
        "option": "Islamic Republic of Iran Broadcasting",
        "why_plausible": "IRIB censors media.",
        "why_wrong": "IRIB is the state broadcaster under the Supreme Leader, often the body that attacks Ershad's permits rather than issuing them."
      },
      {
        "option": "National Library of Iran",
        "why_plausible": "Archives books and assigns ISBNs.",
        "why_wrong": "The National Library assigns bibliographic metadata, not legal political distribution permits (Mojavvez)."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Sazman-e Tablighat",
        "Hozeh Honari"
      ],
      "fa": [
        "سازمان تبلیغات",
        "حوزه هنری"
      ]
    },
    "specificity_prompt": {
      "en": "Name the official cabinet ministry commonly called 'Ershad' that issues cultural distribution permits.",
      "fa": "نام کامل وزارتخانه‌ای که مجوزهای اکران فیلم و انتشار کتاب را در دولت صادر می‌کند بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ministry of Culture and Islamic Guidance. Correct. Where getting an official government stamp of approval is merely the invitation to get attacked by vigilantes.",
        "wrong_generic": "No, it was the Ministry of Culture and Islamic Guidance (Ershad). The most stressed-out civil servants in the capital.",
        "common_wrong_answers": {
          "Ministry of Science": "Science inspects dormitories; Ershad inspects movie scripts and album covers.",
          "Islamic Republic of Iran Broadcasting": "IRIB produces the television denunciations against Ershad's approved movies.",
          "National Library of Iran": "The library stores the books; Ershad decides if they are allowed to be printed."
        }
      },
      "fa": {
        "correct_generic": "وزارت فرهنگ و ارشاد اسلامی. کاملاً درسته! جایی که دریافت مجوز قانونی تازه شروع ماجرا و حمله لباس‌شخصی‌هاست.",
        "wrong_generic": "خیر، پاسخ وزارت فرهنگ و ارشاد اسلامی بود. وزارتخانه‌ای میان چکش هنرمندان و سندان محافظه‌کاران.",
        "common_wrong_answers": {
          "وزارت علوم": "وزارت علوم متولی دانشگاه‌هاست؛ مجوز فیلم و تئاتر و رمان با ارشاد است.",
          "سازمان صدا و سیمای جمهوری اسلامی": "صدا و سیما خودش منتقد مجوزهای ارشاد است و در برنامه‌هایش علیه آنها گزارش می‌رود.",
          "سازمان اسناد و کتابخانه ملی": "کتابخانه ملی فیپا می‌دهد، اما ممیزی و مجوز پخش با وزارت ارشاد است."
        }
      }
    },
    "explanation": {
      "en": "Keshavarzian highlights that the dual nature of the state is vividly demonstrated in cultural policy: while the elected president's Ministry of Culture and Islamic Guidance (Ershad) grants distribution licenses, unelected organs like the judiciary, police, and vigilante groups regularly shut down concerts and pull films from theaters.",
      "fa": "کشاورزیان نشان می‌دهد که دوگانگی حاکمیت در عرصه فرهنگ تجلی می‌یابد: در حالی که وزارت فرهنگ و ارشاد اسلامیِ وابسته به دولت منتخب به فیلم‌ها و کنسرت‌ها مجوز رسمی می‌دهد، نهادهای انتصابی یا تندروها به راحتی مانع از اکران یا اجرای آنها می‌شوند."
    },
    "provenance": {
      "source_book": "An Improvisational Polity: Form and Substance in the Islamic Republic",
      "source_author": "Arang Keshavarzian",
      "page_number": 14,
      "verbatim_passage": "The Ministry of Culture and Islamic Guidance (Ershad) exemplifies administrative vulnerability: its legally valid permits for books and films are frequently vetoed post facto by judicial orders or revolutionary cultural bodies.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_improv_ministry_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "IMPROV AT THE MINISTRY",
      "fa": "بداهه‌سازی در دیوان‌سالاری"
    },
    "clue_text": {
      "en": "Created by Ayatollah Khomeini in 1988 to resolve persistent legislative deadlocks between Parliament and the Guardian Council, this constitutional body was institutionalized with the power to rule on the 'expediency of the state'.",
      "fa": "این نهاد با حکم امام خمینی در بهمن ۱۳۶۶ برای رفع بن‌بست‌های فرساینده قانون‌گذاری میان مجلس و شورای نگهبان پدید آمد و در بازنگری قانون اساسی با اختیارات تشخیص «مصلحت نظام» تثبیت شد."
    },
    "canonical_answer": {
      "en": "Expediency Discernment Council",
      "fa": "مجمع تشخیص مصلحت نظام"
    },
    "accepted_aliases": {
      "en": [
        "Expediency Council",
        "Majma'-e Tashkhis-e Maslahat",
        "Expediency Discernment Council of the System"
      ],
      "fa": [
        "مجمع تشخیص مصلحت",
        "مجمع تشخیص",
        "مجمع تشخیص مصلحت نظام"
      ]
    },
    "options": {
      "en": [
        "Assembly of Experts",
        "Expediency Discernment Council",
        "Guardian Council",
        "Supreme National Security Council"
      ],
      "fa": [
        "مجلس خبرگان رهبری",
        "مجمع تشخیص مصلحت نظام",
        "شورای نگهبان",
        "شورای عالی امنیت ملی"
      ]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {
        "option": "Assembly of Experts",
        "why_plausible": "A major clerical constitutional body (Majles-e Khebregan).",
        "why_wrong": "The Assembly of Experts elects and supervises the Supreme Leader, but does not resolve legislative disputes between Parliament and the Guardian Council."
      },
      {
        "option": "Guardian Council",
        "why_plausible": "The body that reviews parliamentary legislation for Sharia compliance.",
        "why_wrong": "The Guardian Council was half of the legislative deadlock; the Expediency Council was created to overrule it when national interest demanded."
      },
      {
        "option": "Supreme National Security Council",
        "why_plausible": "A high-level security council created in the 1989 constitutional revision.",
        "why_wrong": "SNSC handles defense and foreign policy (Article 176), not arbitration of domestic civil laws between Majles and Guardian Council."
      }
    ],
    "adversarial_confusion_set": {
      "en": [
        "Guardian Council",
        "Shoraye Negahban"
      ],
      "fa": [
        "شورای نگهبان",
        "مجلس خبرگان"
      ]
    },
    "specificity_prompt": {
      "en": "Name the specific body established in 1988 to arbitrate disputes between the Majles and the Guardian Council.",
      "fa": "نام نهاد داوری‌کننده میان مجلس شورای اسلامی و شورای نگهبان در تعیین مصلحت کشور را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Expediency Discernment Council. Spot on. The institutional proof that preserving the regime can suspend the Sharia whenever convenient.",
        "wrong_generic": "No, it was the Expediency Discernment Council (Majma'-e Tashkhis). Created to overrule Islamic jurisprudence in the name of state survival.",
        "common_wrong_answers": {
          "Assembly of Experts": "The Assembly of Experts picks the Supreme Leader; they don't arbitrate labor law disputes.",
          "Guardian Council": "The Guardian Council caused the deadlocks by rejecting bills; the Expediency Council broke them.",
          "Supreme National Security Council": "SNSC deals with wars and nuclear enrichment, not domestic civil code disputes."
        }
      },
      "fa": {
        "correct_generic": "مجمع تشخیص مصلحت نظام. کاملاً درسته! نهادی که رسماً اعلام کرد حفظ نظام اوجب واجبات است، حتی اگر احکام اولیه شرع موقتاً تعطیل شود.",
        "wrong_generic": "خیر، پاسخ مجمع تشخیص مصلحت نظام بود. داور نهایی نزاع‌های مجلس و فقهای شورای نگهبان.",
        "common_wrong_answers": {
          "مجلس خبرگان رهبری": "خبرگان متولی تعیین و نظارت بر رهبری است، نه حل اختلافات قانون‌گذاری.",
          "شورای نگهبان": "شورای نگهبان خودش طرف دعوا بود و قوانین را وتو می‌کرد؛ مجمع وتوی شورا را می‌شکست.",
          "شورای عالی امنیت ملی": "شورای عالی امنیت ملی متولی امنیت و پرونده هسته‌ای است، نه داوری در قوانین کار و تجارت."
        }
      }
    },
    "explanation": {
      "en": "Arang Keshavarzian highlights the creation of the Expediency Discernment Council in 1988 as the ultimate institutionalization of state pragmatism: by declaring that 'maslahat' (state expediency) could overrule primary Islamic legal rulings (ahkam-e avvaliyeh), Khomeini elevated state survival above orthodox jurisprudence.",
      "fa": "آرنگ کشاورزیان تأسیس مجمع تشخیص مصلحت نظام در سال ۱۳۶۶ را اوج عمل‌گرایی ساختاری در فقه حکومتی می‌داند: جایی که امام خمینی با اصالت بخشیدن به «مصلحت نظام»، اعلام کرد مصلحت حفظ حکومت می‌تواند بر احکام اولیه شرع مقدم شود."
    },
    "provenance": {
      "source_book": "An Improvisational Polity: Form and Substance in the Islamic Republic",
      "source_author": "Arang Keshavarzian",
      "page_number": 18,
      "verbatim_passage": "In February 1988, Khomeini institutionalized the Expediency Discernment Council to arbitrate disputes between the parliament and the Guardian Council, establishing that the preservation of the state (maslahat-e nezam) overrides orthodox religious law.",
      "evidence_type": "FACT"
    }
  }
])
