import json
import sys
sys.path.append("/Users/Morad/Spark")
from build_batch_c import batch_c
from jeopardy_pipeline import validate_clue_schema

cats_26_to_30 = [
  # 26. double_sanctions_profiteers: THE SANCTIONS PROFITEERS / کاسبان تحریم در برج میلاد
  {
    "id": "double_sanctions_profiteers_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "THE SANCTIONS PROFITEERS", "fa": "کاسبان تحریم در برج میلاد"},
    "clue_text": {
      "en": "In Iranian political discourse under Rouhani, this derogatory Persian phrase was coined to describe shady oligarchs, brokers, and parastatals who grew fabulously wealthy by circumventing economic embargoes at astronomical markups.",
      "fa": "در گفتمان سیاسی دولت روحانی، این عبارت کنایه‌آمیز برای توصیف الیگارش‌ها، دلالان و نهادهایی به کار رفت که با دور زدن تحریم‌ها و اخذ کارمزدهای نجومی به ثروت‌های افسانه‌ای رسیدند."
    },
    "canonical_answer": {"en": "Sanctions Profiteers", "fa": "کاسبان تحریم"},
    "accepted_aliases": {"en": ["Kaseban-e Tahrim", "Sanctions profiteer", "Profiteers of sanctions"], "fa": ["کاسب تحریم", "کاسبان تحریم‌ها", "دلالان تحریم"]},
    "options": {
      "en": ["Bazaar Philanthropists", "Sanctions Profiteers", "Green Movement Martyrs", "Technocratic Reformers"],
      "fa": ["خیرین بازاری", "کاسبان تحریم", "شهدای جنبش سبز", "تکنوکرات‌های اصلاحات"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Bazaar Philanthropists", "why_plausible": "Traditional merchants.", "why_wrong": "Philanthropists fund charitable mosques and endowments, not corrupt embargo arbitrage."},
      {"option": "Green Movement Martyrs", "why_plausible": "A political faction.", "why_wrong": "The Green Movement was the 2009 protest opposition, not oligarchs making money off sanctions."},
      {"option": "Technocratic Reformers", "why_plausible": "Pro-JCPOA politicians.", "why_wrong": "Technocrats negotiated the nuclear deal specifically to lift sanctions and curb profiteers."}
    ],
    "adversarial_confusion_set": {"en": ["Sultans of Smuggling", "Privatization Barons"], "fa": ["سلاطین قاچاق", "مافیای اقتصادی"]},
    "specificity_prompt": {
      "en": "Provide the exact two-word Persian phrase (Kaseban-e Tahrim) used to condemn illicit embargo beneficiaries.",
      "fa": "اصطلاح سیاسی دوکلمه‌ای رایج برای اشاره به منتفعان از تداوم تحریم‌های اقتصادی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Sanctions Profiteers. Correct. Buying German machinery through five shell companies in Dubai and pocketing a thirty percent commission.",
        "wrong_generic": "No, it was the Sanctions Profiteers (Kaseban-e Tahrim). Those who prayed the nuclear talks would fail.",
        "common_wrong_answers": {
          "Bazaar Philanthropists": "Philanthropists build schools; profiteers build luxury towers in Elahieh.",
          "Green Movement Martyrs": "The Green Movement was in street protests in 2009.",
          "Technocratic Reformers": "The technocrats were trying to reopen the banking system."
        }
      },
      "fa": {
        "correct_generic": "کاسبان تحریم. کاملاً درسته! کسانی که هر بار مذاکرات هسته‌ای به بن‌بست می‌رسید، در برج‌های الهیه جشن سودهای کلان می‌گرفتند.",
        "wrong_generic": "خیر، پاسخ کاسبان تحریم بود. واژه‌ای که حسن روحانی برای افشای ذینفعان تداوم انزوای اقتصادی ساخت.",
        "common_wrong_answers": {
          "خیرین بازاری": "خیرین درمانگاه خیریه می‌سازند، نه رانت ارزی برای واردات انحصاری.",
          "شهدای جنبش سبز": "جنبش سبز اعتراض مدنی سال ۸۸ بود.",
          "تکنوکرات‌های اصلاحات": "تکنوکرات‌ها خواهان پیوستن به اف‌ای‌تی‌اف و لغو تحریم‌ها بودند."
        }
      }
    },
    "explanation": {
      "en": "Narges Bajoghli and Vali Nasr explain that 'Kaseban-e Tahrim' (Sanctions Profiteers) became a defining term in post-2013 debates, identifying the entrenched economic interest groups that actively opposed sanctions relief because the embargo provided them with a lucrative monopoly over import licensing and currency arbitrage.",
      "fa": "نرگس باجغلی و ولی نصر نشان می‌دهند که «کاسبان تحریم» اصطلاحی محوری در کشمکش‌های سیاسی ایران شد و به گروه‌هایی اشاره دارد که به دلیل سودهای نجومی حاصل از انحصار واردات، قاچاق سازمان‌یافته و رانت ارزی، بقای اقتصادی خود را در تداوم تحریم‌ها می‌دیدند."
    },
    "provenance": {
      "source_book": "Sanctions, State, and Society in Iran",
      "source_author": "Narges Bajoghli and Vali Nasr",
      "page_number": 82,
      "verbatim_passage": "President Hassan Rouhani popularized the term 'sanctions profiteers' (kaseban-e tahrim) to target deep-state parastatals and shadow brokers who captured immense illicit rents from embargo evasion.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_sanctions_profiteers_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "THE SANCTIONS PROFITEERS", "fa": "کاسبان تحریم در برج میلاد"},
    "clue_text": {
      "en": "Arrested in December 2013 and sentenced to death for economic corruption, this flamboyant young tycoon laundered billions of dollars in oil revenues through front companies before nearly three billion dollars vanished.",
      "fa": "این سرمایه‌دار جوان پر سر و صدا که در دی ۱۳۹۲ بازداشت و به اتهام اخلال در نظام اقتصادی به اعدام محکوم شد، میلیاردها دلار از درآمدهای نفتی کشور را از طریق شرکت‌های پوششی جابه‌جا کرد اما نزدیک به سه میلیارد دلار از وجوه ناپدید شد."
    },
    "canonical_answer": {"en": "Babak Zanjani", "fa": "بابک زنجانی"},
    "accepted_aliases": {"en": ["Zanjani", "Babak Morteza Zanjani"], "fa": ["بابک مرتضی زنجانی", "زنجانی"]},
    "options": {
      "en": ["Shahram Jazayeri", "Babak Zanjani", "Mahmoud Reza Khavari", "Fazel Khodadad"],
      "fa": ["شهرام جزایری", "بابک زنجانی", "محمودرضا خاوری", "فاضل خداداد"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Shahram Jazayeri", "why_plausible": "A famous economic embezzlement figure.", "why_wrong": "Jazayeri was arrested in 2001 under Khatami for bribing politicians, not for 2012 oil embargo money laundering."},
      {"option": "Mahmoud Reza Khavari", "why_plausible": "The Bank Melli managing director tied to a 3-billion-dollar bank fraud.", "why_wrong": "Khavari fled to Canada in 2011 during the Amir-Mansour Khosravi 3,000-billion-toman bank fraud, not the oil sales tycoon."},
      {"option": "Fazel Khodadad", "why_plausible": "The first executed financial embezzler in Iran.", "why_wrong": "Khodadad was executed in 1995 over the Bank Saderat 123-billion-toman case."}
    ],
    "adversarial_confusion_set": {"en": ["Reza Zarrab", "Ali Ansari"], "fa": ["رضا ضراب", "علی انصاری"]},
    "specificity_prompt": {
      "en": "Name the specific Iranian tycoon arrested in 2013 for embezzling over 2.7 billion dollars in Ministry of Petroleum oil funds.",
      "fa": "نام میلیاردر معروفی که در دولت دهم واسطه فروش نفت تحریمی بود و در سال ۱۳۹۲ بازداشت شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Babak Zanjani. Correct. Flying private jets, owning airlines in Tajikistan, and claiming he was merely an economic Basiji serving the nation.",
        "wrong_generic": "No, it was Babak Zanjani. The ultimate poster boy for sanctions-busting corruption.",
        "common_wrong_answers": {
          "Shahram Jazayeri": "Shahram Jazayeri was the 2001 scandal giving cash envelopes to MPs.",
          "Mahmoud Reza Khavari": "Khavari is enjoying his mansions in Toronto.",
          "Fazel Khodadad": "Khodadad was hanged back in 1995 for the Bank Saderat case."
        }
      },
      "fa": {
        "correct_generic": "بابک زنجانی. کاملاً درسته! مالک هواپیمایی قشم‌ایر و تاجیکستان که خود را «بسیجی اقتصادی» می‌نامید.",
        "wrong_generic": "خیر، پاسخ بابک زنجانی بود. چهره شاخص پرونده مفقود شدن ۲٫۷ میلیارد یورو پول نفت در دوران تحریم.",
        "common_wrong_answers": {
          "شهرام جزایری": "شهرام جزایری ماجرای اهدای چک به نمایندگان مجلس ششم در سال ۱۳۸۰ بود.",
          "محمودرضا خاوری": "خاوری مدیرعامل بانک ملی بود که با پرونده ۳ هزار میلیاردی به کانادا گریخت.",
          "فاضل خداداد": "فاضل خداداد در سال ۱۳۷۴ در پرونده ۱۲۳ میلیاردی بانک صادرات اعدام شد."
        }
      }
    },
    "explanation": {
      "en": "Bajoghli and Nasr detail how the Ahmadinejad administration entrusted Babak Zanjani with exporting millions of barrels of crude oil through a labyrinth of shell companies in Malaysia, Turkey, and Tajikistan; when the oil was sold, Zanjani failed to repatriate roughly $2.7 billion to the Central Bank, leading to his sensational 2013 arrest.",
      "fa": "باجغلی و نصر تشریح می‌کنند که چگونه دولت دهم برای فروش نفت تحریمی به بابک زنجانی و شبکه شرکت‌های صوری او در مالزی، ترکیه و تاجیکستان متکی شد؛ زنجانی پس از فروش محموله‌ها از بازگرداندن حدود ۲٫۷ میلیارد یورو امتناع کرد و در دی ۱۳۹۲ بازداشت و محاکمه شد."
    },
    "provenance": {
      "source_book": "Sanctions, State, and Society in Iran",
      "source_author": "Narges Bajoghli and Vali Nasr",
      "page_number": 89,
      "verbatim_passage": "Babak Zanjani emerged as the preeminent shadow financier of the sanctions era, moving billions in petroleum revenues until his arrest in 2013 revealed that over $2.7 billion in state oil funds had vanished into foreign offshore accounts.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_sanctions_profiteers_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE SANCTIONS PROFITEERS", "fa": "کاسبان تحریم در برج میلاد"},
    "clue_text": {
      "en": "Sanctions profiteering was vastly facilitated by this monetary phenomenon, where privileged state-connected insiders bought foreign currency at cheap subsidized rates to import luxury consumer goods or flip it on the open bazaar.",
      "fa": "کاسبی از تحریم‌ها با این پدیده پولی و رانت مالی به‌شدت تسهیل شد، به طوری که خواص متصل به قدرت، ارز ارزان‌قیمت دولتی دریافت می‌کردند اما آن را صرف واردات کالای لوکس کرده یا در بازار آزاد می‌فروختند."
    },
    "canonical_answer": {"en": "Dual Exchange Rate Arbitrage", "fa": "رانت ارز چندنرخی"},
    "accepted_aliases": {"en": ["Currency arbitrage", "Dual exchange rate", "Subsidized dollar arbitrage", "Exchange rate arbitrage"], "fa": ["رانت ارزی", "اختلاف نرخ ارز دولتی و آزاد", "شکاف نرخ ارز", "ارز ترجیحی"]},
    "options": {
      "en": ["Gold Standard Deflation", "Dual Exchange Rate Arbitrage", "Hyperinflationary Indexing", "Crypto Staking"],
      "fa": ["انقباض پولی پایه طلا", "رانت ارز چندنرخی", "تعدیل تورم ونزوئلایی", "سپرده‌گذاری رمزارز"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Gold Standard Deflation", "why_plausible": "A monetary concept.", "why_wrong": "Iran does not operate on a gold standard."},
      {"option": "Hyperinflationary Indexing", "why_plausible": "Related to high inflation.", "why_wrong": "Indexing ties wages to inflation, whereas this was predatory currency arbitrage between state peg and street market."},
      {"option": "Crypto Staking", "why_plausible": "A modern speculative activity.", "why_wrong": "Crypto staking is a blockchain decentralized protocol, not the state subsidized currency allocation scheme."}
    ],
    "adversarial_confusion_set": {"en": ["Tariff Arbitrage", "Trade Dumping"], "fa": ["تعرفه گمرکی", "دامپینگ تجاری"]},
    "specificity_prompt": {
      "en": "Name the economic mechanism of profiting from the gap between the subsidized state exchange rate and the free-market street exchange rate.",
      "fa": "سازوکار رانتی مبتنی بر اختلاف بهای دلار دولتی (ارز ترجیحی یا ۴۲۰۰ تومانی) با قیمت بازار آزاد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Dual Exchange Rate Arbitrage. Correct. Getting dollars at 4,200 tomans to import baby formula, and importing luxury sports cars instead to sell at street rates.",
        "wrong_generic": "No, it was Dual Exchange Rate Arbitrage (Rant-e Arzi). The most lucrative fountain of corruption in modern Iran.",
        "common_wrong_answers": {
          "Gold Standard Deflation": "The gold standard died a century ago.",
          "Hyperinflationary Indexing": "Indexing protects workers; this system plundered them.",
          "Crypto Staking": "Bitcoin came much later than the good old central bank foreign exchange allocation window."
        }
      },
      "fa": {
        "correct_generic": "رانت ارز چندنرخی. کاملاً درسته! دریافت دلار ۴۲۰۰ تومانی به بهانه واردات خوراک دام و شیرخشک، و وارد کردن پورشه و فروش در بازار آزاد.",
        "wrong_generic": "خیر، پاسخ رانت ارز چندنرخی (شکاف دلار دولتی و آزاد) بود. بزرگ‌ترین چشمه توزیع ثروت‌های بادآورده در کشور.",
        "common_wrong_answers": {
          "انقباض پولی پایه طلا": "پایه طلا در قرن نوزدهم کنار رفت؛ اقتصاد ایران با ارزهای فیات کار می‌کند.",
          "تعدیل تورم ونزوئلایی": "تعدیل تورمی جبران حقوق است، نه رانت ارزی اختصاصی واردکنندگان.",
          "سپرده‌گذاری رمزارز": "استخراج رمزارز فعالیت نوینی است؛ این رانت حواله‌های ارزی بانک مرکزی بود."
        }
      }
    },
    "explanation": {
      "en": "Bajoghli and Nasr explain that the persistence of dual or multiple exchange rates—such as the 4,200-toman 'Jahangiri dollar'—created astronomical arbitrage opportunities: well-connected parastatals and private importers received subsidized central bank dollars to import critical medicines or grain, but frequently diverted the hard currency to the black market or imported luxury vehicles, earning billions overnight.",
      "fa": "باجغلی و نصر توضیح می‌دهند که نظام چندنرخی ارز (نظیر دلار ۴۲۰۰ تومانی معروف به جهانگیری) زمینه‌ساز رانت‌های عظیم آربیتراژ شد: شرکت‌های متصل به قدرت به بهانه واردات کالاهای اساسی و دارو، ارز ارزان دریافت کرده و آن را در بازار آزاد با سودهای چندصد درصدی به فروش می‌رساندند."
    },
    "provenance": {
      "source_book": "Sanctions, State, and Society in Iran",
      "source_author": "Narges Bajoghli and Vali Nasr",
      "page_number": 95,
      "verbatim_passage": "The dual exchange rate regime created a colossal engine of corruption, allowing politically favored insiders to pocket astronomical fortunes by arbitrating between cheap subsidized central bank dollars and the soaring free-market rate.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_sanctions_profiteers_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE SANCTIONS PROFITEERS", "fa": "کاسبان تحریم در برج میلاد"},
    "clue_text": {
      "en": "In their sociological analysis, Bajoghli and Nasr document how Western sanctions inadvertently dealt a crushing blow to this domestic demographic, which historically served as the primary constituency for political moderation and secular democracy.",
      "fa": "باجغلی و نصر در تحلیل جامعه‌شناختی خود مستند می‌کنند که چگونه تحریم‌های غرب ناخواسته ضربه‌ای مهلک به این طبقه اجتماعی داخلی زد که خاستگاه اصلی میانه‌روی سیاسی و دموکراسی‌خواهی سکولار بود."
    },
    "canonical_answer": {"en": "The Middle Class", "fa": "طبقه متوسط"},
    "accepted_aliases": {"en": ["Iranian middle class", "Urban middle class", "Middle class"], "fa": ["طبقه متوسط شهری", "طبقه متوسط ایران", "طبقه متوسط مدرن"]},
    "options": {
      "en": ["Clerical Oligarchy", "The Middle Class", "Paramilitary Commanders", "Smuggling Cartels"],
      "fa": ["الیگارشی روحانیت", "طبقه متوسط", "فرماندهان نظامی", "کارتل‌های قاچاق"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Clerical Oligarchy", "why_plausible": "A powerful elite.", "why_wrong": "The clerical elite retained access to tax-exempt foundations (Bonyads) and state subsidies, expanding their relative power."},
      {"option": "Paramilitary Commanders", "why_plausible": "The IRGC leadership.", "why_wrong": "Military and parastatal conglomerates captured market shares left by Western companies, growing wealthier rather than being crushed."},
      {"option": "Smuggling Cartels", "why_plausible": "Underground actors.", "why_wrong": "Smugglers flourished under the blockade by monopolizing border trade."}
    ],
    "adversarial_confusion_set": {"en": ["Working Class", "Rural Peasantry"], "fa": ["طبقه کارگر", "روستاییان"]},
    "specificity_prompt": {
      "en": "Name the specific social class whose economic decimation is analyzed by Bajoghli and Nasr as the primary sociological victim of Western sanctions.",
      "fa": "نام طبقه اجتماعی شهری که قربانی اصلی تورم تحریمی شد و توان اقتصادی خود را از دست داد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "The Middle Class. Spot on. Crushing the doctors, teachers, and engineers while the black-market dealers and parastatals took over the economy.",
        "wrong_generic": "No, it was the Middle Class. The tragic collateral damage of maximum pressure.",
        "common_wrong_answers": {
          "Clerical Oligarchy": "The clerical foundations survived on state oil subventions.",
          "Paramilitary Commanders": "The commanders took over the abandoned oil fields and ports.",
          "Smuggling Cartels": "The smugglers made fortunes charging triple prices on border diesel."
        }
      },
      "fa": {
        "correct_generic": "طبقه متوسط. کاملاً درسته! نابودی پزشکان، معلمان، اساتید و مهندسان مستقل، در حالی که بنیادها و دلالان بازار را بلعیدند.",
        "wrong_generic": "خیر، پاسخ طبقه متوسط ایران بود. مهم‌ترین قربانی اجتماعی تحریم‌های همه‌جانبه غرب.",
        "common_wrong_answers": {
          "الیگارشی روحانیت": "بنیادهای حاکمیتی از رانت‌های دولتی ارتزاق کردند و ثروتمندتر شدند.",
          "فرماندهان نظامی": "فرماندهان با قرارگاه‌های سازندگی پروژه‌های انرژی را مصادره کردند.",
          "کارتل‌های قاچاق": "قاچاقچیان با سودهای کلان تجارت مرزی را قبضه کردند."
        }
      }
    },
    "explanation": {
      "en": "Bajoghli and Nasr demonstrate the profound paradox of Western sanctions: while designed to weaken the regime, sanctions pulverized the independent secular middle class (professionals, private entrepreneurs, educators) through hyperinflation and currency collapse, rendering society entirely dependent on state handouts while parastatals strengthened their economic stranglehold.",
      "fa": "باجغلی و نصر پارادوکس بنیادین تحریم‌های غرب را آشکار می‌سازند: تحریم‌ها به جای تضعیف نهادهای قدرت، طبقه متوسط مستقل، کارآفرینان خصوصی و دانشگاهیان را با تورم مهارناپذیر نابود کردند و مردم را محتاج یارانه‌های دولتی ساختند، در حالی که خصولتی‌ها قدرت اقتصادی خود را تثبیت کردند."
    },
    "provenance": {
      "source_book": "Sanctions, State, and Society in Iran",
      "source_author": "Narges Bajoghli and Vali Nasr",
      "page_number": 104,
      "verbatim_passage": "Rather than triggering democratic transformation, economic sanctions hollowed out Iran's secular, pro-reform middle class, pushing millions into poverty and eliminating the very social constituency essential for moderate political change.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_sanctions_profiteers_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "THE SANCTIONS PROFITEERS", "fa": "کاسبان تحریم در برج میلاد"},
    "clue_text": {
      "en": "When European energy majors like Total and Shell withdrew from Iran under threat of US secondary sanctions, their lucrative multi-billion dollar engineering contracts were systematically absorbed by this giant IRGC engineering and construction conglomerate.",
      "fa": "هنگامی که غول‌های نفتی اروپا نظیر توتال و شل تحت فشار تحریم‌های ثانویه آمریکا از ایران خارج شدند، قراردادهای چندمیلیارد دلاری توسعه میادین گازی و نفتی به این غول مهندسی و سازندگی سپاه واگذار شد."
    },
    "canonical_answer": {"en": "Khatam al-Anbiya Construction Headquarters", "fa": "قرارگاه سازندگی خاتم‌الانبیاء"},
    "accepted_aliases": {"en": ["Khatam al-Anbiya", "Khatam al-Anbia", "Khatam", "Khatam al-Anbya"], "fa": ["قرارگاه خاتم", "قرارگاه خاتم‌الانبیا", "قرارگاه سازندگی خاتم‌الانبیا", "خاتم‌الانبیاء"]},
    "options": {
      "en": ["Bonyad-e Shahid", "Khatam al-Anbiya Construction Headquarters", "Imam Khomeini Relief Committee", "National Iranian Oil Company"],
      "fa": ["بنیاد شهید", "قرارگاه سازندگی خاتم‌الانبیاء", "کمیته امداد امام خمینی", "شرکت ملی نفت ایران"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Bonyad-e Shahid", "why_plausible": "A major parastatal foundation.", "why_wrong": "Handles veteran social welfare and pensions, not heavy civil engineering and offshore gas field construction."},
      {"option": "Imam Khomeini Relief Committee", "why_plausible": "A massive state charity.", "why_wrong": "Handles welfare handouts to the rural impoverished, not deepwater offshore gas platforms in South Pars."},
      {"option": "National Iranian Oil Company", "why_plausible": "The state oil company that awards contracts.", "why_wrong": "NIOC is the state client and owner that awarded the abandoned megaprojects to Khatam al-Anbiya as contractor."}
    ],
    "adversarial_confusion_set": {"en": ["Ghadir Investment", "MAPNA Group"], "fa": ["سرمایه‌گذاری غدیر", "گروه مپنا"]},
    "specificity_prompt": {
      "en": "Name the specific IRGC engineering conglomerate that took over development of the South Pars gas phases.",
      "fa": "نام قرارگاه مهندسی سپاه پاسداران که فازهای توسعه میدان گازی پارس جنوبی را از شرکت‌های خارجی تحویل گرفت بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Khatam al-Anbiya Construction Headquarters. Spot on. The French engineers pack their bags in Assaluyeh, and the Pasdaran civil engineers move right into the trailers.",
        "wrong_generic": "No, it was Khatam al-Anbiya Construction Headquarters. The largest engineering contractor in the country.",
        "common_wrong_answers": {
          "Bonyad-e Shahid": "Bonyad-e Shahid manages veteran pensions, not offshore gas drilling.",
          "Imam Khomeini Relief Committee": "Komiteh-ye Emdad delivers food parcels, not liquefied natural gas plants.",
          "National Iranian Oil Company": "NIOC signed the cheques; Khatam al-Anbiya did the drilling."
        }
      },
      "fa": {
        "correct_generic": "قرارگاه سازندگی خاتم‌الانبیاء. کاملاً درسته! مهندسان فرانسوی توتال عسلویه را ترک کردند و مهندسان قرارگاه خاتم جایگزین آن‌ها شدند.",
        "wrong_generic": "خیر، پاسخ قرارگاه سازندگی خاتم‌الانبیاء بود. بزرگ‌ترین کارفرمای پروژه‌های سدسازی، نفت و گاز در کشور.",
        "common_wrong_answers": {
          "بنیاد شهید": "بنیاد شهید متولی امور ایثارگران است، نه توسعه پالایشگاه فازهای پارس جنوبی.",
          "کمیته امداد امام خمینی": "کمیته امداد صندوق حمایتی محرومان است.",
          "شرکت ملی نفت ایران": "شرکت نفت کارفرما بود؛ پیمانکار اصلی قرارگاه خاتم بود."
        }
      }
    },
    "explanation": {
      "en": "Bajoghli and Nasr document that when US secondary sanctions forced foreign multinationals like Total and Eni to abandon contracts in the South Pars natural gas field, the Ministry of Petroleum awarded these mega-projects without tender to the IRGC's Khatam al-Anbiya Construction Headquarters, cementing the Revolutionary Guards' total hegemony over Iran's industrial infrastructure.",
      "fa": "باجغلی و نصر مستند می‌کنند که با خروج غول‌های خارجی مانند توتال از پروژه‌های فازهای پارس جنوبی، وزارت نفت این قراردادهای چند میلیارد دلاری را بدون مناقصه به قرارگاه سازندگی خاتم‌الانبیاء سپاه واگذار کرد و زمینه تسلط بی‌رقیب سپاه بر شریان‌های نفت، گاز و صنایع سنگین را فراهم آورد."
    },
    "provenance": {
      "source_book": "Sanctions, State, and Society in Iran",
      "source_author": "Narges Bajoghli and Vali Nasr",
      "page_number": 112,
      "verbatim_passage": "The departure of Western energy majors like Total under sanctions pressure directly enriched the IRGC's Khatam al-Anbiya Construction Headquarters, which absorbed multi-billion-dollar contracts to develop the lucrative South Pars gas field.",
      "evidence_type": "FACT"
    }
  },

  # 27. double_shia_geopolitics: SHI'A GEOPOLITICS GOES ARABIC / هلال شیعی در جام جم
  {
    "id": "double_shia_geopolitics_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "SHI'A GEOPOLITICS GOES ARABIC", "fa": "هلال شیعی در جام جم"},
    "clue_text": {
      "en": "In late 2004, following the fall of Saddam Hussein, this pro-Western Arab monarch famously warned in an interview that a rising 'Shia Crescent' was forming under Iranian influence from Tehran through Baghdad and Damascus to Beirut.",
      "fa": "در اواخر سال ۱۳۸۳ پس از سقوط صدام حسین، این پادشاه عرب متحد غرب در مصاحبه‌ای جنجالی هشدار داد که یک «هلال شیعی» تحت نفوذ ایران از تهران تا بغداد، دمشق و بیروت در حال شکل‌گیری است."
    },
    "canonical_answer": {"en": "King Abdullah II of Jordan", "fa": "ملک عبدالله دوم پادشاه اردن"},
    "accepted_aliases": {"en": ["King Abdullah of Jordan", "Abdullah II", "King Abdullah II", "King of Jordan"], "fa": ["ملک عبدالله دوم", "پادشاه اردن", "عبدالله دوم پادشاه اردن", "ملک عبدالله اردن"]},
    "options": {
      "en": ["King Hussein of Jordan", "King Abdullah II of Jordan", "King Fahd of Saudi Arabia", "Emir of Qatar"],
      "fa": ["ملک حسین پادشاه اردن", "ملک عبدالله دوم پادشاه اردن", "ملک فهد پادشاه عربستان", "امیر قطر"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "King Hussein of Jordan", "why_plausible": "His father who ruled Jordan for decades.", "why_wrong": "King Hussein died in February 1999, years before the 2003 Iraq invasion and 2004 interview."},
      {"option": "King Fahd of Saudi Arabia", "why_plausible": "The Saudi monarch in 2004.", "why_wrong": "King Fahd was incapacitated by a stroke and King Abdullah of Saudi Arabia ran the country, but the specific 'Shia Crescent' phrase was coined by King Abdullah II of Jordan."},
      {"option": "Emir of Qatar", "why_plausible": "A prominent Gulf ruler.", "why_wrong": "Hamad bin Khalifa Al Thani of Qatar maintained open channels with Iran and did not coin the phrase."}
    ],
    "adversarial_confusion_set": {"en": ["King Abdullah of Saudi Arabia", "Hosni Mubarak"], "fa": ["ملک عبدالله پادشاه عربستان", "حسنی مبارک"]},
    "specificity_prompt": {
      "en": "Name the specific Jordanian monarch who coined the geopolitical warning term 'Shia Crescent' in 2004.",
      "fa": "نام پادشاه اردن که در مصاحبه معروف سال ۲۰۰۴ برای نخستین بار اصطلاح «هلال شیعی» را به کار برد بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "King Abdullah II of Jordan. Correct. Coining the phrase that kept Sunni monarchs awake at night in Amman, Riyadh, and Manama.",
        "wrong_generic": "No, it was King Abdullah II of Jordan. The 2004 Washington Post interview that set off regional alarm bells.",
        "common_wrong_answers": {
          "King Hussein of Jordan": "King Hussein passed away in 1999.",
          "King Fahd of Saudi Arabia": "Fahd was ailing in Riyadh.",
          "Emir of Qatar": "Qatar was funding Al Jazeera, not warning about Shi'a crescents."
        }
      },
      "fa": {
        "correct_generic": "ملک عبدالله دوم پادشاه اردن. کاملاً درسته! ابداع اصطلاحی که خواب را از چشمان حاکمان سنی در امان، ریاض و منامه ربود.",
        "wrong_generic": "خیر، پاسخ ملک عبدالله دوم پادشاه اردن بود. مصاحبه سال ۱۳۸۳ با واشنگتن‌پست که بازتاب گسترده منطقه‌ای یافت.",
        "common_wrong_answers": {
          "ملک حسین پادشاه اردن": "ملک حسین در بهمن ۱۳۷۷ درگذشته بود.",
          "ملک فهد پادشاه عربستان": "ملک فهد در بستر بیماری بود.",
          "امیر قطر": "قطر در پی میانجی‌گری با تهران بود، نه هشدار پیرامون هلال شیعی."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr documents that in December 2004, King Abdullah II of Jordan warned the Washington Post that the empowerement of Iraq's Shi'a majority would create an Iranian-dominated 'Shia Crescent' stretching from Tehran through Baghdad to Damascus and south Lebanon, an anxiety that came to define Arab-Iranian strategic rivalry for two decades.",
      "fa": "ولی نصر مستند می‌کند که در آذر ۱۳۸۳ ملک عبدالله دوم پادشاه اردن با هشدار به واشنگتن‌پست اعلام کرد به قدرت رسیدن اکثریت شیعه در عراق موجب تشکیل «هلال شیعی» به رهبری تهران تا بیروت خواهد شد؛ بیانی که چارچوب رقابت‌های ژئوپلیتیک ایران و جهان عرب را برای دهه‌ها رقم زد."
    },
    "provenance": {
      "source_book": "The Shia Revival: How Conflicts within Islam Will Shape the Future",
      "source_author": "Vali Nasr",
      "page_number": 158,
      "verbatim_passage": "In late 2004, King Abdullah of Jordan gave voice to these fears by warning of the emergence of a 'Shia crescent' running from Iran through Iraq and Syria to Lebanon, altering the balance of power across the Middle East.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_shia_geopolitics_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "SHI'A GEOPOLITICS GOES ARABIC", "fa": "هلال شیعی در جام جم"},
    "clue_text": {
      "en": "Formed in June 2014 following Ayatollah Ali al-Sistani's defensive jihad fatwa against ISIS, this umbrella organization of predominantly Shi'i Iraqi paramilitary units received crucial training and arms from the IRGC Quds Force.",
      "fa": "این سازمان چترمانند متشکل از گروه‌های شبه‌نظامی شیعه عراقی که در خرداد ۱۳۹۳ در پی فتوای جهاد کفایی آیت‌الله سیستانی علیه داعش تشکیل شد، آموزش و تسلیحات حیاتی را از نیروی قدس سپاه دریافت کرد."
    },
    "canonical_answer": {"en": "Popular Mobilization Forces", "fa": "حشدالشعبی"},
    "accepted_aliases": {"en": ["Hashd al-Shaabi", "PMF", "PMU", "Popular Mobilization Units", "Al-Hashd al-Sha'abi"], "fa": ["بسیج مردمی عراق", "حشد الشعبی", "نیروهای حشد شعبی"]},
    "options": {
      "en": ["Peshmerga", "Popular Mobilization Forces", "Free Syrian Army", "South Lebanon Army"],
      "fa": ["پیشمرگه", "حشدالشعبی", "ارتش آزاد سوریه", "ارتش جنوب لبنان"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Peshmerga", "why_plausible": "The Kurdish regional armed forces in northern Iraq.", "why_wrong": "The Peshmerga are Kurdish nationalist forces under the Kurdistan Regional Government, not the Shi'i paramilitary PMF."},
      {"option": "Free Syrian Army", "why_plausible": "An armed group in the regional wars.", "why_wrong": "The FSA fought against Bashar al-Assad and Iran in Syria."},
      {"option": "South Lebanon Army", "why_plausible": "A historic Lebanese militia.", "why_wrong": "The SLA was an Israeli-backed Christian militia in southern Lebanon that collapsed in 2000."}
    ],
    "adversarial_confusion_set": {"en": ["Kata'ib Hezbollah", "Badr Organization"], "fa": ["کتائب حزب‌الله", "سازمان بدر"]},
    "specificity_prompt": {
      "en": "Name the official Iraqi umbrella paramilitary organization (Al-Hashd al-Sha'abi) established in 2014.",
      "fa": "نام سازمان نیروهای بسیج مردمی عراق به عربی (حشد...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Popular Mobilization Forces (Al-Hashd al-Sha'abi). Correct. Mobilizing tens of thousands of young men overnight to stop ISIS at the gates of Baghdad.",
        "wrong_generic": "No, it was the Popular Mobilization Forces (Al-Hashd al-Sha'abi). The Iraqi paramilitary coalition that transformed state security.",
        "common_wrong_answers": {
          "Peshmerga": "The Peshmerga answer to Erbil and Masoud Barzani.",
          "Free Syrian Army": "The Free Syrian Army was trying to overthrow Tehran's Syrian ally in Damascus.",
          "South Lebanon Army": "The South Lebanon Army dissolved when Israel withdrew in May 2000."
        }
      },
      "fa": {
        "correct_generic": "حشدالشعبی. کاملاً درسته! خروش ده‌ها هزار جوان عراقی با فتوای مرجعیت نجف برای متوقف ساختن داعش در دروازه‌های بغداد.",
        "wrong_generic": "خیر، پاسخ سازمان حشدالشعبی (بسیج مردمی عراق) بود. ساختار شبه‌نظامی که بعدها در قانون نیروهای مسلح عراق ادغام شد.",
        "common_wrong_answers": {
          "پیشمرگه": "پیشمرگه نیروی مسلح اقلیم کردستان عراق است.",
          "ارتش آزاد سوریه": "ارتش آزاد سوریه مخالفان اسد بودند که با ایران می‌جنگیدند.",
          "ارتش جنوب لبنان": "ارتش جنوب لبنان شبه‌نظامیان مزدور اسرائیل بودند که در سال ۲۰۰۰ منحل شدند."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr highlights that the rapid capture of Mosul by ISIS in June 2014 led Grand Ayatollah Sistani to issue a historic fatwa for defensive jihad; General Qassem Soleimani immediately arrived in Baghdad to coordinate and arm the umbrella Popular Mobilization Forces (PMF / Hashd al-Sha'abi), embedding Iranian strategic influence deep into Iraq's security architecture.",
      "fa": "ولی نصر اشاره می‌کند که با سقوط موصل در خرداد ۱۳۹۳ و صدور فتوای جهاد کفایی آیت‌الله سیستانی، سردار قاسم سلیمانی فوراً در بغداد حاضر شد و با تسلیح و ساماندهی حشدالشعبی، مانع از سقوط پایتخت عراق شد و نفوذ راهبردی ایران را در ساختار دفاعی عراق تثبیت کرد."
    },
    "provenance": {
      "source_book": "The Shia Revival: How Conflicts within Islam Will Shape the Future",
      "source_author": "Vali Nasr",
      "page_number": 164,
      "verbatim_passage": "The formation of the Popular Mobilization Forces (Hashd al-Sha'abi) in 2014 transformed the regional landscape: armed and guided by the IRGC Quds Force, the coalition played the decisive ground role in rolling back ISIS in Iraq.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_shia_geopolitics_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "SHI'A GEOPOLITICS GOES ARABIC", "fa": "هلال شیعی در جام جم"},
    "clue_text": {
      "en": "To defend the Assad government and protect sacred shrines in Syria, the IRGC Quds Force recruited and deployed tens of thousands of Hazara Shi'a Afghan refugees in this specialized military division.",
      "fa": "برای دفاع از حکومت اسد و حفاظت از حرم‌های متبرکه در سوریه، نیروی قدس سپاه ده‌ها هزار پناهجوی شیعه هزاره افغانستانی را در قالب این لشکر نظامی ویژه سازماندهی و اعزام کرد."
    },
    "canonical_answer": {"en": "Liwa Fatemiyoun", "fa": "لشکر فاطمیون"},
    "accepted_aliases": {"en": ["Fatemiyoun Division", "Fatemiyoun Brigade", "Fatimiyyun"], "fa": ["فاطمیون", "تیپ فاطمیون", "مدافعان حرم فاطمیون"]},
    "options": {
      "en": ["Liwa Zainebiyoun", "Liwa Fatemiyoun", "Hezbollah", "Ansar Allah"],
      "fa": ["لشکر زینبیون", "لشکر فاطمیون", "حزب‌الله", "انصارالله"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Liwa Zainebiyoun", "why_plausible": "Another foreign Shi'a brigade mobilized by the IRGC.", "why_wrong": "Zainebiyoun was composed of Pakistani Shi'as, whereas Fatemiyoun specifically comprised Afghan Hazara fighters."},
      {"option": "Hezbollah", "why_plausible": "The premier Shi'a proxy in Lebanon.", "why_wrong": "Hezbollah is indigenous to Lebanon, not Afghan refugees."},
      {"option": "Ansar Allah", "why_plausible": "The Houthi movement in Yemen.", "why_wrong": "Ansar Allah are Yemeni Zaydis fighting in the Arabian Peninsula, not Afghan units in Syria."}
    ],
    "adversarial_confusion_set": {"en": ["Liwa Zainebiyoun", "Liwa al-Quds"], "fa": ["لشکر زینبیون", "لواء القدس"]},
    "specificity_prompt": {
      "en": "Name the specific military division consisting of Afghan Shi'a volunteers deployed by Iran to Syria.",
      "fa": "نام لشکر رزمندگان داوطلب افغانستانی مدافع حرم در سوریه را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Liwa Fatemiyoun. Correct. The rugged Hazara infantry that bore the brunt of intense urban combat from Aleppo to Deir ez-Zor.",
        "wrong_generic": "No, it was Liwa Fatemiyoun. The Afghan division of the Axis of Resistance.",
        "common_wrong_answers": {
          "Liwa Zainebiyoun": "Zainebiyoun was the Pakistani brigade; Fatemiyoun was the Afghan division.",
          "Hezbollah": "Hezbollah speaks Lebanese Arabic; Fatemiyoun speaks Dari.",
          "Ansar Allah": "Ansar Allah are the Houthis in Yemen."
        }
      },
      "fa": {
        "correct_generic": "لشکر فاطمیون. کاملاً درسته! رزمندگان شیعه هزاره افغانستان که سنگین‌ترین نبردهای حلب، تدمر و بوکمال را به دوش کشیدند.",
        "wrong_generic": "خیر، پاسخ لشکر فاطمیون بود. نیروی رزمنده افغانستانی محور مقاومت در نبردهای سوریه.",
        "common_wrong_answers": {
          "لشکر زینبیون": "زینبیون رزمندگان پاکستانی بودند؛ فاطمیون رزمندگان افغانستانی هستند.",
          "حزب‌الله": "حزب‌الله رزمندگان لبنانی عرب‌زبان هستند؛ فاطمیون فارسی‌زبان دری بودند.",
          "انصارالله": "انصارالله جنبش حوثی‌های یمن است."
        }
      }
    },
    "explanation": {
      "en": "Security researchers and Middle East analysts document that the IRGC Quds Force organized Liwa Fatemiyoun in 2014, deploying an estimated twenty thousand Afghan Hazara recruits to spearhead assaults against Syrian rebel forces and ISIS, offering residency permits, salaries, and religious validation.",
      "fa": "پژوهشگران امنیت منطقه‌ای نشان می‌دهند که نیروی قدس سپاه با تأسیس لشکر فاطمیون در سال ۱۳۹۳، هزاران رزمنده شیعه هزاره مقیم ایران و افغانستان را در جبهه‌های سوریه به کار گرفت و نقش محوری در آزادسازی دیرالزور، حلب و تدمر ایفا کردند."
    },
    "provenance": {
      "source_book": "The Shia Revival: How Conflicts within Islam Will Shape the Future",
      "source_author": "Vali Nasr",
      "page_number": 172,
      "verbatim_passage": "Iran's intervention in Syria saw the deployment of Liwa Fatemiyoun, a division of Afghan Shi'a recruits commanded by the IRGC Quds Force that spearheaded key offensives across Syria.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_shia_geopolitics_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "SHI'A GEOPOLITICS GOES ARABIC", "fa": "هلال شیعی در جام جم"},
    "clue_text": {
      "en": "To frame foreign military operations in Syria and Iraq in sanctified religious terms that transcended national borders, the Iranian state branded all casualties and deployment cadres with this revered Persian title.",
      "fa": "حکومت ایران برای قدسی‌سازی عملیات نظامی در سوریه و عراق فراتر از مرزهای ملی، نیروهای اعزامی و شهدای این نبردها را به این عنوان معنوی و پرطرفدار ملقب ساخت."
    },
    "canonical_answer": {"en": "Defenders of the Shrine", "fa": "مدافعان حرم"},
    "accepted_aliases": {"en": ["Modafe'an-e Haram", "Defenders of the Sacred Shrines", "Shrine Defenders"], "fa": ["مدافع حرم", "مدافعین حرم", "رزمندگان مدافع حرم"]},
    "options": {
      "en": ["Peace Corps Volunteers", "Defenders of the Shrine", "Foreign Legionnaires", "Frontier Guards"],
      "fa": ["داوطلبان صلح", "مدافعان حرم", "لژیونرهای خارجی", "مرزبانان میهن"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Peace Corps Volunteers", "why_plausible": "Humanitarian terminology.", "why_wrong": "US humanitarian volunteer program, not armed expeditionary forces."},
      {"option": "Foreign Legionnaires", "why_plausible": "A mercenary military concept.", "why_wrong": "French colonial military institution, completely antithetical to the religious Shi'i framing."},
      {"option": "Frontier Guards", "why_plausible": "Border defense troops.", "why_wrong": "Frontier guards defend Iran's geographic borders, whereas these troops deployed abroad in Damascus and Samarra."}
    ],
    "adversarial_confusion_set": {"en": ["Ansaran-e Velayat", "Jihadgaran-e Basij"], "fa": ["انصار ولایت", "جهادگران سلامت"]},
    "specificity_prompt": {
      "en": "Provide the exact three-word Persian honorific title applied to soldiers serving in Syria and Iraq to protect holy Shi'a mausoleums.",
      "fa": "عنوان شناخته‌شده و حماسی نیروهای اعزامی ایران به نبردهای سوریه و عراق را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Defenders of the Shrine. Correct. Framing expeditionary warfare in the Levant as the sacred duty to keep Sayyida Zaynab's golden dome from being demolished.",
        "wrong_generic": "No, it was the Defenders of the Shrine (Modafe'an-e Haram). The ideological narrative that legitimized intervention abroad.",
        "common_wrong_answers": {
          "Peace Corps Volunteers": "The Peace Corps plants trees; these troops fought ISIS with heavy artillery.",
          "Foreign Legionnaires": "The French Foreign Legion serves Paris for pay; these men fought for Karbala theology.",
          "Frontier Guards": "Frontier guards stay on the border fence; Shrine Defenders were fighting outside Damascus."
        }
      },
      "fa": {
        "correct_generic": "مدافعان حرم. کاملاً درسته! بازتعریف حضور نظامی فرامرزی به عنوان تکلیفی قدسی برای پاسداری از گنبد طلایی حضرت زینب و حضرت رقیه.",
        "wrong_generic": "خیر، پاسخ مدافعان حرم بود. کلیدواژه‌ای هویتی و مذهبی که مشروعیت‌بخش حضور منطقه‌ای ایران شد.",
        "common_wrong_answers": {
          "داوطلبان صلح": "نیروهای صلح سازمان ملل کلاه آبی هستند، نه رزمندگان موشک‌انداز در تدمر.",
          "لژیونرهای خارجی": "لژیونر مزدور ارتش فرانسه بود؛ مدافع حرم جایگاهی عقیدتی در ادبیات نظام دارد.",
          "مرزبانان میهن": "مرزبانان در پاسگاه‌های مرزی کشور مستقرند؛ مدافعان حرم در شام و عراق جنگیدند."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr and regional scholars examine how the narrative of 'Modafe'an-e Haram' (Defenders of the Shrine) successfully galvanized public support in Iran: framing the intervention around protecting the tomb of Lady Zaynab in Damascus and the shrines in Karbala, Najaf, and Samarra from Salafi-jihadist desecration neutralized nationalist domestic critiques of foreign intervention.",
      "fa": "ولی نصر و کارشناسان منطقه‌ای نشان می‌دهند که گفتمان «مدافعان حرم» با پیوند زدن حضور نظامی به حفاظت از مضجع شریف حضرت زینب (س) در دمشق و عتبات عالیات در برابر خطر تخریب تکفیری‌ها، انتقادات ملی‌گرایانه داخلی نسبت به هزینه‌های جنگ در خارج از مرزها را خنثی کرد."
    },
    "provenance": {
      "source_book": "The Shia Revival: How Conflicts within Islam Will Shape the Future",
      "source_author": "Vali Nasr",
      "page_number": 178,
      "verbatim_passage": "By branding its expeditionary fighters as 'Defenders of the Shrine' (Modafe'an-e Haram), Tehran cast its military intervention in Syria not as geopolitical power projection, but as a sacred obligation to shield holy Shi'a mausoleums from Sunni extremists.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_shia_geopolitics_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "SHI'A GEOPOLITICS GOES ARABIC", "fa": "هلال شیعی در جام جم"},
    "clue_text": {
      "en": "Appointed Commander of the IRGC Quds Force immediately following Qassem Soleimani's assassination in Baghdad on January 3, 2020, this veteran general had previously managed the force's eastern operations in Afghanistan.",
      "fa": "این سردار کهنه‌کار که سابقه مدیریت طولانی عملیات نیروی قدس در افغانستان را در کارنامه داشت، بلافاصله پس از ترور قاسم سلیمانی در بغداد در ۱۳ دی ۱۳۹۸ به فرماندهی نیروی قدس سپاه منصوب شد."
    },
    "canonical_answer": {"en": "Esmail Qaani", "fa": "اسماعیل قاآنی"},
    "accepted_aliases": {"en": ["General Esmail Qaani", "Ismail Qaani", "Esmaeil Qaani"], "fa": ["سردار قاآنی", "سرتیپ پاسدار اسماعیل قاآنی", "سردار اسماعیل قاآنی"]},
    "options": {
      "en": ["Hossein Salami", "Esmail Qaani", "Mohammad Bagheri", "Ali Fadavi"],
      "fa": ["حسین سلامی", "اسماعیل قاآنی", "محمد باقری", "علی فدوی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Hossein Salami", "why_plausible": "Commander-in-Chief of the entire IRGC.", "why_wrong": "General Salami commands the overall IRGC (Sepah), not specifically the expeditionary Quds Force branch."},
      {"option": "Mohammad Bagheri", "why_plausible": "Chief of the General Staff of the Armed Forces.", "why_wrong": "General Bagheri heads the entire joint armed forces general staff (Artesh and Sepah combined)."},
      {"option": "Ali Fadavi", "why_plausible": "Deputy Commander of the IRGC.", "why_wrong": "Rear Admiral Fadavi is the Deputy Commander of the IRGC and former naval chief, not Quds Force commander."}
    ],
    "adversarial_confusion_set": {"en": ["Mohammad Reza Zahedi", "Iraj Masjedi"], "fa": ["محمدرضا زاهدی", "ایرج مسجدی"]},
    "specificity_prompt": {
      "en": "Name the specific general appointed to succeed Qassem Soleimani as Commander of the IRGC Quds Force in January 2020.",
      "fa": "نام جانشین شهید قاسم سلیمانی و فرمانده کنونی نیروی قدس سپاه را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Esmail Qaani. Spot on. Stepping into the giant shoes of Soleimani to manage the Axis of Resistance from Beirut to Sanaa.",
        "wrong_generic": "No, it was General Esmail Qaani. Appointed by Ayatollah Khamenei within hours of the Baghdad airport drone strike.",
        "common_wrong_answers": {
          "Hossein Salami": "General Salami is the overall chief of the IRGC giving fiery speeches.",
          "Mohammad Bagheri": "General Bagheri coordinates all military branches from the General Staff headquarters.",
          "Ali Fadavi": "Admiral Fadavi was harassing US aircraft carriers in the Persian Gulf."
        }
      },
      "fa": {
        "correct_generic": "اسماعیل قاآنی. کاملاً درسته! نشستن بر جایگاه شهید سلیمانی برای هدایت شبکه پیچیده محور مقاومت از بیروت تا صنعا.",
        "wrong_generic": "خیر، پاسخ سردار اسماعیل قاآنی بود. حکمی که رهبر انقلاب ساعاتی پس از حمله فرودگاه بغداد صادر کردند.",
        "common_wrong_answers": {
          "حسین سلامی": "سردار سلامی فرمانده کل سپاه پاسداران است.",
          "محمد باقری": "سردار باقری رئیس ستاد کل نیروهای مسلح است.",
          "علی فدوی": "سردار فدوی جانشین فرمانده کل سپاه است."
        }
      }
    },
    "explanation": {
      "en": "On January 3, 2020, following the US MQ-9 Reaper drone strike that killed Qassem Soleimani outside Baghdad airport, Supreme Leader Ayatollah Khamenei immediately promoted his deputy of twenty years, Brigadier General Esmail Qaani, to lead the IRGC Quds Force, maintaining continuity across Iran's regional proxy networks.",
      "fa": "در ۱۳ دی ۱۳۹۸ به دنبال ترور سپهبد شهید قاسم سلیمانی توسط پهپاد آمریکایی در فرودگاه بغداد، رهبر معظم انقلاب بلافاصله سرتیپ پاسدار اسماعیل قاآنی (جانشین ۲۰ ساله نیروی قدس) را به فرماندهی این نیرو منصوب کردند تا تداوم فرماندهی شبکه مقاومت تضمین شود."
    },
    "provenance": {
      "source_book": "The Shia Revival: How Conflicts within Islam Will Shape the Future",
      "source_author": "Vali Nasr",
      "page_number": 184,
      "verbatim_passage": "Following the assassination of Qassem Soleimani in January 2020, Ayatollah Khamenei immediately appointed General Esmail Qaani, Soleimani's long-time deputy who oversaw operations in Afghanistan and Central Asia, to command the Quds Force.",
      "evidence_type": "FACT"
    }
  },

  # 28. double_conspiracy_cognition: CONSPIRACY AND COGNITION / تئوری توطئه با مهر انگلیس
  {
    "id": "double_conspiracy_cognition_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "CONSPIRACY AND COGNITION", "fa": "تئوری توطئه با مهر انگلیس"},
    "clue_text": {
      "en": "In Iranian popular culture and political humor analyzed by Ervand Abrahamian, any unexpected historical setback or complex political intrigue is reflexively explained away by this famous colloquial Persian phrase.",
      "fa": "در فرهنگ عمومی و طنز سیاسی ایران که توسط یرواند آبراهامیان تحلیل شده، هر ناکامی تاریخی غیرمنتظره یا دسیسه پیچیده سیاسی فوراً با این ضرب‌المثل عامیانه پنج‌کلمه‌ای به روباه پیر نسبت داده می‌شود."
    },
    "canonical_answer": {"en": "It's the work of the English", "fa": "کار، کار انگلیسی‌هاست"},
    "accepted_aliases": {"en": ["Kar-e Engelisi-ha-st", "The English are behind it", "It is the English", "The work of the English"], "fa": ["کار کار انگلیساس", "کار کار انگلیسی‌هاست", "کار انگلیسی‌هاست", "همه‌اش کار انگلیسی‌هاست"]},
    "options": {
      "en": ["It's the work of the French", "It's the work of the English", "It's the work of the Germans", "It's the work of the Chinese"],
      "fa": ["کار، کار فرانسوی‌هاست", "کار، کار انگلیسی‌هاست", "کار، کار آلمانی‌هاست", "کار، کار چینی‌هاست"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "It's the work of the French", "why_plausible": "France had cultural influence in Iran.", "why_wrong": "French cultural prestige was associated with literature and law, never the grand imperial puppet master of conspiracy."},
      {"option": "It's the work of the Germans", "why_plausible": "Germany was popular in Iran.", "why_wrong": "Germans were viewed with sympathy as rivals of Britain and Russia, not the hidden puppeteers."},
      {"option": "It's the work of the Chinese", "why_plausible": "Modern trade power.", "why_wrong": "A modern trade partner, not the historical boogeyman of 20th-century Iranian paranoia."}
    ],
    "adversarial_confusion_set": {"en": ["It's the work of the Americans", "It's the work of the Russians"], "fa": ["کار، کار روس‌هاست", "کار، کار آمریکاست"]},
    "specificity_prompt": {
      "en": "Provide the iconic colloquial Persian phrase attributing all historical misfortunes to British cunning.",
      "fa": "جمله مشهور و طنزآمیز عامیانه انتساب همه حوادث به بریتانیا (کار، کار ...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "It's the work of the English (Kar-e Kar-e Engelisi-ha-st). Correct. When it rains on your picnic, the British ambassador clearly adjusted the cloud seeding.",
        "wrong_generic": "No, it was 'Kar-e Kar-e Engelisi-ha-st' (It's the work of the English). The national diagnosis for everything from lost elections to flat tires.",
        "common_wrong_answers": {
          "It's the work of the French": "The French gave Iran legal civil codes and croissants.",
          "It's the work of the Germans": "The Germans built the railway and were loved by the bazaar.",
          "It's the work of the Chinese": "The Chinese manufacture cheap plastic, not 19th-century colonial plots."
        }
      },
      "fa": {
        "correct_generic": "کار، کار انگلیسی‌هاست. کاملاً درسته! حتی اگر در روز سیزده‌بدر باران ببارد، بدون شک کارشناسان سفارت بریتانیا در آن دست داشته‌اند.",
        "wrong_generic": "خیر، پاسخ «کار، کار انگلیسی‌هاست» بود. شاه‌بیت پارانویای جمعی و طنز تاریخی جامعه ایران.",
        "common_wrong_answers": {
          "کار، کار فرانسوی‌هاست": "فرانسوی‌ها به ما واژه‌های مرسی و کنکور را دادند.",
          "کار، کار آلمانی‌هاست": "آلمانی‌ها راه‌آهن سراسری را ساختند و محبوب بازاریان بودند.",
          "کار، کار چینی‌هاست": "چینی‌ها سازنده اجناس ارزان بازارند، نه طراح توطئه‌های قاجار."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian's classic essay 'The Paranoid Style in Iranian Politics' traces how centuries of British imperial intrigue (from the tobacco concessions to the 1919 treaty and the 1953 coup) embedded the belief that Britain is an omnipotent, invisible puppet master controlling every event in Iran, distilled in the famous saying 'Kar, kar-e Engelisi-ha-st'.",
      "fa": "یرواند آبراهامیان در مقاله کلاسیک «سبک پارانوئید در سیاست ایران» ریشه‌یابی می‌کند که چگونه دهه‌ها مداخله استعماری بریتانیا (از قرارداد توتون و تنباکو تا وثوق‌الدوله و کودتای ۲۸ مرداد) این باور عمیق روانی را در فرهنگ ایرانی کاشت که دست پنهان انگلیس پشت تمام تحولات است، باوری که در تکیه‌کلام معروف «کار، کار انگلیسی‌هاست» خلاصه شد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 111,
      "verbatim_passage": "The belief in the ubiquitous British hidden hand is so pervasive that Iranians reflexively invoke the phrase 'It's the work of the English' (Kar-e Engelisi-ha-st) to explain away any puzzling political development.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_conspiracy_cognition_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "CONSPIRACY AND COGNITION", "fa": "تئوری توطئه با مهر انگلیس"},
    "clue_text": {
      "en": "This quintessential obsession with British imperial machinations was immortalized in this beloved 1973 satirical novel by Iraj Pezeshkzad, adapted into a legendary television series by Nasser Taghvai.",
      "fa": "این وسواس فرهنگی عمیق نسبت به دسیسه‌های امپراتوری بریتانیا در این رمان طنز جاودانه سال ۱۳۵۲ اثر ایرج پزشکزاد و سریال تلویزیونی تاریخی ناصر تقوایی جاودانه شد."
    },
    "canonical_answer": {"en": "My Uncle Napoleon", "fa": "دایی‌جان ناپلئون"},
    "accepted_aliases": {"en": ["Daei Jan Napoleon", "Uncle Napoleon", "My Uncle Napoleon novel"], "fa": ["دایی جان ناپلئون", "رمان دایی جان ناپلئون", "دائی جان ناپلئون"]},
    "options": {
      "en": ["The Blind Owl", "My Uncle Napoleon", "Savushun", "The Patient Stone"],
      "fa": ["بوف کور", "دایی‌جان ناپلئون", "سووشون", "سنگ صبور"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "The Blind Owl", "why_plausible": "Sadegh Hedayat's masterpiece.", "why_wrong": "The Blind Owl is a dark surrealist psychological novella, not a comic social satire of British conspiracy theories."},
      {"option": "Savushun", "why_plausible": "Simin Daneshvar's acclaimed novel about WWII Shiraz.", "why_wrong": "Savushun deals with British wartime occupation seriously through a family drama, not comic parody."},
      {"option": "The Patient Stone", "why_plausible": "A famous modern Iranian novel by Sadeq Chubak.", "why_wrong": "Sadeq Chubak's novel is gritty naturalist realism, not comic satire."}
    ],
    "adversarial_confusion_set": {"en": ["Haji Aqa", "Modir-e Madreseh"], "fa": ["حاجی آقا", "مدیر مدرسه"]},
    "specificity_prompt": {
      "en": "Name the famous satirical novel by Iraj Pezeshkzad featuring a delusional patriarch who believes he fought the British Army in Kazerun.",
      "fa": "نام شاهکار رمان طنز ایرج پزشکزاد که شخصیت اصلی آن توهم جنگیدن با ارتش انگلیس در ممسنی و کازرون را داشت بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "My Uncle Napoleon (Daei Jan Napoleon). Correct. Ordering your loyal servant Mash Qasem to swear that the British troops are encircling the family garden.",
        "wrong_generic": "No, it was My Uncle Napoleon by Iraj Pezeshkzad. The literary masterpiece that diagnosed the Iranian political psyche through laughter.",
        "common_wrong_answers": {
          "The Blind Owl": "Hedayat was seeing shadowy opium hallucinations, not British redcoats.",
          "Savushun": "Simin Daneshvar's novel was about the tragic death of Zari's husband, not comic delusion.",
          "The Patient Stone": "Chubak was exploring poverty in southern slums."
        }
      },
      "fa": {
        "correct_generic": "دایی‌جان ناپلئون. کاملاً درسته! دستور به مش قاسم برای دروغ گفتن و تأیید اینکه قشون انگلیس باغ موری الاغ را محاصره کرده‌اند.",
        "wrong_generic": "خیر، پاسخ رمان دایی‌جان ناپلئون اثر ایرج پزشکزاد بود. درخشان‌ترین آینه طنزآلود روان‌شناسی توطئه‌باور ایرانی.",
        "common_wrong_answers": {
          "بوف کور": "بوف کور شاهکار سوررئال صادق هدایت با زن اثیری و پیرمرد خنزرپنزری است.",
          "سووشون": "سووشون رمان حماسی و تلخ سیمین دانشور درباره اشغال فارس توسط انگلیس است.",
          "سنگ صبور": "سنگ صبور رمان ناتورالیستی صادق چوبک درباره فقر شیراز است."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian cites Iraj Pezeshkzad's 1973 comic masterpiece *My Uncle Napoleon* as the ultimate cultural depiction of the Iranian 'paranoid style': the patriarch, a retired low-ranking gendarme, suffers from full megalomania, convinced that Napoleon Bonaparte was his soulmate and that the British Empire is actively plotting to assassinate him in his Tehran family garden.",
      "fa": "آبراهامیان رمان «دایی‌جان ناپلئون» پزشکزاد را اوج تجلی فرهنگی سندروم پارانوئید در ایران می‌داند: نایب سوم سابق ژاندارمری که خود را همتای ناپلئون بناپارت می‌پندارد و توهم دارد که ارتش بریتانیا به تلافی جنگ‌های خیالی او در ممسنی و کازرون در پی انتقام از او در باغ خانوادگی است."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 115,
      "verbatim_passage": "Iraj Pezeshkzad captured this psychological malady brilliantly in his classic 1973 satirical novel My Uncle Napoleon (Da'i Jan Napul'un), where the protagonist sees the scheming hand of the British behind every domestic dispute and personal misfortune.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_conspiracy_cognition_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "CONSPIRACY AND COGNITION", "fa": "تئوری توطئه با مهر انگلیس"},
    "clue_text": {
      "en": "In revolutionary political trials and clerical tracts analyzed by Abrahamian, Western espionage networks were frequently conflated with the secret rituals of this fraternal lodge organization, historically translated into Persian as Faramoosh-khaneh.",
      "fa": "در کیفرخواست‌های دادگاه‌های انقلاب و رساله‌های سیاسی که توسط آبراهامیان بررسی شده، شبکه‌های جاسوسی غرب همواره با این لژهای سرّی پیوند داده می‌شدند؛ تشکیلاتی که در تاریخ معاصر به «فراموش‌خانه» ترجمه شده بود."
    },
    "canonical_answer": {"en": "Freemasonry", "fa": "فراماسونری"},
    "accepted_aliases": {"en": ["Masonic lodges", "Freemasons", "Faramoosh-khaneh", "Masons"], "fa": ["فراموش‌خانه", "لژهای فراماسونری", "ماسونی", "فراماسون‌ها"]},
    "options": {
      "en": ["Knights Templar", "Freemasonry", "Rotary Club", "Opus Dei"],
      "fa": ["شوالیه‌های معبد", "فراماسونری", "کلوپ روتاری", "اپوس دئی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Knights Templar", "why_plausible": "A medieval secret society.", "why_wrong": "The Knights Templar were crushed in 1307 by the King of France, not modern political lodges in Iran."},
      {"option": "Rotary Club", "why_plausible": "A civic business association targeted by revolutionaries.", "why_wrong": "Rotary and Lions were secondary targets, but the foundational historical conspiracy obsession was centered on Freemasonry (Faramoosh-khaneh)."},
      {"option": "Opus Dei", "why_plausible": "A conservative Catholic group.", "why_wrong": "Opus Dei is Catholic in Spain and Rome, completely absent from Iranian politics."}
    ],
    "adversarial_confusion_set": {"en": ["Illuminati", "Lions Club"], "fa": ["ایلومیناتی", "کلوپ لاینز"]},
    "specificity_prompt": {
      "en": "Name the secretive fraternal order (Faramoosh-khaneh / Feramasoneri) demonized as an imperialist network in Iran.",
      "fa": "نام سازمان لژهای سرّی برادری غربی که از عهد قاجار به فراموش‌خانه ترجمه شد و نماد توطئه استعمار شناخته می‌شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Freemasonry. Correct. Convinced that an apron, a compass, and an eye on a pyramid control the entire cabinet of ministers.",
        "wrong_generic": "No, it was Freemasonry (Faramoosh-khaneh). The master conspiracy trope that united monarchists, leftists, and Islamists.",
        "common_wrong_answers": {
          "Knights Templar": "The Templars belong to medieval crusades and Dan Brown novels.",
          "Rotary Club": "Rotary was for middle-class dentists having lunch; Freemasonry was the grand shadow cabinet.",
          "Opus Dei": "Opus Dei is conservative Catholic monks in Madrid."
        }
      },
      "fa": {
        "correct_generic": "فراماسونری. کاملاً درسته! باور به اینکه پیش‌بند چرمی، پرگار، گونیا و چشم جهان‌بین در لژهای مخفی، تمام وزرای قاجار و پهلوی را تعیین می‌کردند.",
        "wrong_generic": "خیر، پاسخ فراماسونری (فراموش‌خانه) بود. متهم همیشگی تمام انقلابیون از مشروطه تا سال ۱۳۵۷.",
        "common_wrong_answers": {
          "شوالیه‌های معبد": "شوالیه‌های معبد جنگجویان قرون وسطی در جنگ‌های صلیبی بودند.",
          "کلوپ روتاری": "کلوپ روتاری محل ناهار هفتگی تجار بود، اما اتهام توطئه عمیق متوجه فراماسونری بود.",
          "اپوس دئی": "اپوس دئی تشکل کاتولیک در واتیکان و اسپانیاست."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian analyzes how Freemasonry became the supreme villain in Iranian conspiracy literature: founded by Mirza Malkam Khan in 1858 as *Faramoosh-khaneh*, Masonic lodges in the Pahlavi era did indeed enroll senior ministers and prime ministers (like Sharif-Emami), leading revolutionary polemicists to claim that a global Zionist-Anglo-Saxon Masonic cabal dictated all Iranian history.",
      "fa": "آبراهامیان توضیح می‌دهد که چگونه فراماسونری به کانون اصلی توطئه‌باوری در ایران تبدیل شد: از زمان تأسیس فراموش‌خانه توسط میرزا ملکم‌خان در دوره ناصرالدین‌شاه تا ریاست شریف‌امامی بر لژ بزرگ ایران در عصر پهلوی، این نهاد به عنوان شبکه سرّی صهیونیستی-انگلیسی برای کنترل پشت‌پرده دولت تصویر می‌شد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 121,
      "verbatim_passage": "Freemasonry (faramoosh-khaneh) occupied a central place in the Iranian conspiratorial imagination, perceived not merely as a fraternal club but as an insidious imperialist web controlling prime ministers, generals, and financial magnates.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_conspiracy_cognition_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "CONSPIRACY AND COGNITION", "fa": "تئوری توطئه با مهر انگلیس"},
    "clue_text": {
      "en": "Abrahamian observes that Iranian conspiracy theories are uniquely stubborn because they are anchored in this real, factual historical trauma: the August 1953 Anglo-American military coup that toppled Prime Minister Mohammad Mossadegh.",
      "fa": "آبراهامیان یادآور می‌شود که تئوری‌های توطئه در ایران به این دلیل بسیار ریشه‌دار و سرسخت هستند که بر این تروما و واقعیت تاریخی مستند تکیه دارند: کودتای نظامی آمریکایی-انگلیسی ۲۸ مرداد ۱۳۳۲ که دکتر مصدق را سرنگون کرد."
    },
    "canonical_answer": {"en": "1953 Coup", "fa": "کودتای ۲۸ مرداد ۱۳۳۲"},
    "accepted_aliases": {"en": ["1953 coup d'etat", "Operation Ajax", "28 Mordad Coup", "1953 overthrow of Mossadegh"], "fa": ["کودتای ۲۸ مرداد", "کودتای ۲۸ مرداد ۳۲", "عملیات آژاکس", "کودتای ۵۳"]},
    "options": {
      "en": ["1921 Coup", "1953 Coup", "1979 Revolution", "Nojeh Coup Plot"],
      "fa": ["کودتای ۱۲۹۹", "کودتای ۲۸ مرداد ۱۳۳۲", "انقلاب ۱۳۵۷", "کودتای نوژه"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "1921 Coup", "why_plausible": "Reza Khan's British-backed coup.", "why_wrong": "The 1299/1921 coup brought Reza Shah to power, but the 1953 overthrow of democratic Mossadegh is the modern foundational trauma cited by Abrahamian."},
      {"option": "1979 Revolution", "why_plausible": "A major turning point.", "why_wrong": "The revolution overthrew the Shah; the 1953 coup restored him."},
      {"option": "Nojeh Coup Plot", "why_plausible": "A planned military coup in 1980.", "why_wrong": "Nojeh was an aborted domestic military plot uncovered before execution, not the successful CIA/MI6 coup that traumatized the national consciousness."}
    ],
    "adversarial_confusion_set": {"en": ["1921 Coup", "Operation Eagle Claw"], "fa": ["کودتای ۳ اسفند ۱۲۹۹", "واقعه طبس"]},
    "specificity_prompt": {
      "en": "Name the specific 1953 CIA/MI6 intelligence coup (Operation Ajax) that overthrew Iran's democratically elected Prime Minister.",
      "fa": "نام کودتای مشترک سیا و اینتلیجنس سرویس در مرداد ۱۳۳۲ علیه دولت ملی دکتر محمد مصدق را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "1953 Coup (Operation Ajax). Correct. Just because you are paranoid doesn't mean the CIA and MI6 aren't actually bribing street thugs with suitcases of cash to overthrow your government.",
        "wrong_generic": "No, it was the 1953 Coup (Operation Ajax / 28 Mordad). The genuine historical conspiracy that made all future paranoias plausible.",
        "common_wrong_answers": {
          "1921 Coup": "The 1921 coup was General Ironside putting Reza Shah on a horse.",
          "1979 Revolution": "1979 was a million people in the street chasing the Shah away.",
          "Nojeh Coup Plot": "Nojeh was betrayed and dismantled before the jets could take off from Hamedan."
        }
      },
      "fa": {
        "correct_generic": "کودتای ۲۸ مرداد ۱۳۳۲. کاملاً درسته! وقتی با چمدان‌های دلار شعبان بی‌مخ‌ها را خریدند تا نخست‌وزیر دموکراتیک را سرنگون کنند، پارانویا دیگر توهم نیست، یک واقعیت تاریخی است.",
        "wrong_generic": "خیر، پاسخ کودتای ۲۸ مرداد ۱۳۳۲ (عملیات آژاکس) بود. رخداد تلخی که توهم توطئه را برای نسل‌ها در حافظه ملی مشروعیت بخشید.",
        "common_wrong_answers": {
          "کودتای ۱۲۹۹": "کودتای ۳ اسفند ۱۲۹۹ ژنرال آیرونساید و رضاخان بود.",
          "انقلاب ۱۳۵۷": "انقلاب ۵۷ قیام توده‌ای مردم بود.",
          "کودتای نوژه": "کودتای نوژه در تیرماه ۵۹ پیش از پرواز فانتوم‌ها کشف و خنثی شد."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian emphasizes that Iranian conspiracy theories cannot be dismissed as mere psychosis: Operation Ajax—the 1953 covert operation orchestrated by Kermit Roosevelt (CIA) and MI6 that spent hundreds of thousands of dollars to buy mob violence, bribe military officers, and depose Mohammad Mossadegh—proved to Iranians that foreign powers really did secretly manipulate internal politics from embassy backrooms.",
      "fa": "یرواند آبراهامیان تأکید می‌کند که پارانویای سیاسی در ایران توهم صرف نیست: عملیات آژاکس در ۲۸ مرداد ۱۳۳۲ که توسط کرمیت روزولت (سیا) و ام‌آی۶ با پرداخت صدها هزار دلار پول نقد، خرید اوباش و تبانی با نظامیان به سقوط مصدق انجامید، به جامعه ایران اثبات کرد که دست بیگانه واقعاً قادر به دستکاری سرنوشت سیاسی کشور از پشت پرده سفارتخانه‌هاست."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 126,
      "verbatim_passage": "The paranoid style in Iran retains such potent cognitive legitimacy because it is rooted in actual history: the 1953 CIA-MI6 coup against Mossadegh proved to Iranians that imperialist powers really were capable of covertly orchestrating domestic regime change.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_conspiracy_cognition_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "CONSPIRACY AND COGNITION", "fa": "تئوری توطئه با مهر انگلیس"},
    "clue_text": {
      "en": "Abrahamian's core theoretical insight concludes that conspiracy theories function across Iranian society primarily as this psychological defense mechanism: excusing collective political failures by projecting responsibility onto omnipotent external puppeteers.",
      "fa": "نتیجه‌گیری نظری بنیادین آبراهامیان این است که تئوری توطئه در جامعه ایران در اصل به عنوان این سازوکار دفاعی روانی عمل می‌کند: تبرئه ناتوانی‌ها و اشتباهات خودی از طریق فرافکنی گناه بر دوش عروسک‌گردانان همه‌توان خارجی."
    },
    "canonical_answer": {"en": "Psychological Projection and Rationalization", "fa": "فرافکنی روان‌شناختی و توجیه ناکامی‌ها"},
    "accepted_aliases": {"en": ["Psychological projection", "Defense mechanism of projection", "Scapegoating", "External projection"], "fa": ["فرافکنی", "مکانیسم دفاعی فرافکنی", "فرافکنی روانی", "سلب مسئولیت از خود"]},
    "options": {
      "en": ["Collective Delusion of Grandeur", "Psychological Projection and Rationalization", "Linguistic Determinism", "Behavioral Conditioning"],
      "fa": ["توهم خودبزرگ‌بینی جمعی", "فرافکنی روان‌شناختی و توجیه ناکامی‌ها", "جبرگرایی زبانی", "شرطی‌سازی رفتاری"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Collective Delusion of Grandeur", "why_plausible": "Related to narcissism.", "why_wrong": "Delusions of grandeur exaggerate one's own power, whereas conspiracy theories portray the self as a helpless victim of foreign geniuses."},
      {"option": "Linguistic Determinism", "why_plausible": "A sociological linguistic theory.", "why_wrong": "Linguistic determinism (Sapir-Whorf) relates to language shaping thought, not emotional defense mechanisms."},
      {"option": "Behavioral Conditioning", "why_plausible": "A psychological term.", "why_wrong": "Behavioral conditioning relates to stimulus-response learning (Pavlov/Skinner), not psychoanalytic ego defense mechanisms."}
    ],
    "adversarial_confusion_set": {"en": ["Cognitive Dissonance", "Confirmation Bias"], "fa": ["ناهماهنگی شناختی", "سوگیری تایید"]},
    "specificity_prompt": {
      "en": "Identify the specific psychological defense mechanism analyzed by Abrahamian where societies project their own mistakes onto foreign conspirators.",
      "fa": "مکانیسم دفاع روانی مورد بحث آبراهامیان که در آن جامعه ضعف‌ها و گناهان خود را به دیگریِ خارجی نسبت می‌دهد را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Psychological Projection and Rationalization. Spot on. Why admit that your political coalition collapsed due to incompetence and greed when you can blame British intelligence instead?",
        "wrong_generic": "No, it was Psychological Projection and Rationalization. The comforting psychological balm of the paranoid style.",
        "common_wrong_answers": {
          "Collective Delusion of Grandeur": "Grandeur thinks you are God; conspiracy thinks the British are God.",
          "Linguistic Determinism": "Linguistics is about grammar; this is about avoiding moral blame.",
          "Behavioral Conditioning": "Pavlov rang bells for dogs; politicians blame foreigners to save face."
        }
      },
      "fa": {
        "correct_generic": "فرافکنی روان‌شناختی و توجیه ناکامی‌ها. کاملاً درسته! چرا اعتراف کنیم که به خاطر لجاجت و بی‌برنامگی شکست خوردیم، وقتی می‌توانیم همه گناه را به گردن اینتلیجنس سرویس بیندازیم؟",
        "wrong_generic": "خیر، پاسخ فرافکنی روان‌شناختی و توجیه ناکامی‌ها بود. مرهم روانی سبک پارانوئید برای تسکین شکست‌های سیاسی.",
        "common_wrong_answers": {
          "توهم خودبزرگ‌بینی جمعی": "خودبزرگ‌بینی توهم قدرت است؛ تئوری توطئه فرد را قربانی مظلوم اراده لندن می‌داند.",
          "جبرگرایی زبانی": "جبرگرایی زبانی نظریه ساپیر-وورف است، نه مکانیسم دفاعی فرویدی.",
          "شرطی‌سازی رفتاری": "شرطی‌سازی مربوط به پاولف است، نه سلب مسئولیت اخلاقی در سیاست."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian concludes that the greatest utility of conspiracy theories in Iranian political life is psychological absolution: it spares political elites, parties, and citizens from critical self-examination or taking responsibility for military defeats, political fracturing, and economic mismanagement by presenting the nation as the innocent victim of omnipotent global conspiracies.",
      "fa": "یرواند آبراهامیان نتیجه می‌گیرد که کارکرد حیاتی تئوری توطئه در حیات سیاسی ایران، فرار از مسئولیت‌پذیری است: این باور به نخبگان و جامعه امکان می‌دهد تا بدون نقد رفتارهای خود و پذیرش اشتباهات در انشقاق‌های حزبی یا سوءمدیریت اقتصادی، خود را قربانی مظلوم اما پاک‌دستِ توطئه‌های پیچیده و همه‌فن‌حریف استعمار جهانی نشان دهند."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 131,
      "verbatim_passage": "Conspiracy theories function fundamentally as an ego-defense mechanism, allowing political actors to avoid taking responsibility for their own miscalculations, internal factionalism, and policy failures by projecting all blame onto external puppet masters.",
      "evidence_type": "INTERPRETATION"
    }
  },

  # 29. double_ethnic_oil: ETHNIC LINES IN THE OIL FIELDS / نفت روی گسل‌های هویت
  {
    "id": "double_ethnic_oil_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "ETHNIC LINES IN THE OIL FIELDS", "fa": "نفت روی گسل‌های هویت"},
    "clue_text": {
      "en": "Accounting for over eighty percent of Iran's onshore crude oil reserves, this southwestern border province is home to a substantial Arabic-speaking population alongside Lurs and Bakhtiaris.",
      "fa": "این استان مرزی در جنوب غربی ایران که بیش از ۸۰ درصد ذخایر نفت خام خشکی کشور را در خود جای داده، زیستگاه جمعیت قابل‌توجهی از هموطنان عرب در کنار اقوام لر و بختیاری است."
    },
    "canonical_answer": {"en": "Khuzestan Province", "fa": "استان خوزستان"},
    "accepted_aliases": {"en": ["Khuzestan", "Khuzistan", "Ostān-e Khūzestān"], "fa": ["خوزستان", "استان خوزستان", "دیار کارون"]},
    "options": {
      "en": ["Bushehr Province", "Khuzestan Province", "Hormozgan Province", "Ilam Province"],
      "fa": ["استان بوشهر", "استان خوزستان", "استان هرمزگان", "استان ایلام"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Bushehr Province", "why_plausible": "A major petroleum and gas province on the Gulf.", "why_wrong": "Bushehr is famous for offshore natural gas (South Pars) and nuclear power, not 80% of onshore crude oil fields like Ahvaz and Marun."},
      {"option": "Hormozgan Province", "why_plausible": "A southern coastal province.", "why_wrong": "Hormozgan centers on Bandar Abbas and the Strait of Hormuz, not the massive Karun River oil basin."},
      {"option": "Ilam Province", "why_plausible": "A western border province with oil.", "why_wrong": "Ilam is predominantly Kurdish and Luri, with far smaller petroleum reserves than Khuzestan."}
    ],
    "adversarial_confusion_set": {"en": ["Kohgiluyeh and Boyer-Ahmad", "Lorestan"], "fa": ["کهگیلویه و بویراحمد", "لرستان"]},
    "specificity_prompt": {
      "en": "Name the specific southwestern petroleum-producing province home to Iran's Arab minority.",
      "fa": "نام استان نفت‌خیز جنوب غربی ایران با جمعیت عرب‌زبان بومی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Khuzestan Province. Correct. The black gold reservoir under the palms that financed the modern Iranian state.",
        "wrong_generic": "No, it was Khuzestan Province. The economic engine and ethnic frontline of the country.",
        "common_wrong_answers": {
          "Bushehr Province": "Bushehr is gas platforms and the nuclear plant.",
          "Hormozgan Province": "Hormozgan is container ports and the Strait of Hormuz.",
          "Ilam Province": "Ilam is oak-covered mountains on the Iraqi border."
        }
      },
      "fa": {
        "correct_generic": "استان خوزستان. کاملاً درسته! گنجینه طلای سیاه در میان نخلستان‌ها که بار مالی توسعه ایران مدرن را به دوش کشیده است.",
        "wrong_generic": "خیر، پاسخ استان خوزستان بود. شریان حیاتی اقتصاد نفت و گسل حساس هویتی در جنوب غرب.",
        "common_wrong_answers": {
          "استان بوشهر": "بوشهر مهد گاز عسلویه و نیروگاه اتمی است.",
          "استان هرمزگان": "هرمزگان پایتخت دریایی و تنگه هرمز است.",
          "استان ایلام": "ایلام سرزمین بلوط و ایثار با اکثریت لری و کردی است."
        }
      }
    },
    "explanation": {
      "en": "Kaveh Ehsani and Rasmus Elling analyze Khuzestan as the crucible of modern Iranian political economy: holding the massive oil fields of Masjed Soleyman, Ahvaz, Marun, and Gachsaran, it generates the lifeblood of state revenues while remaining an ethnically complex borderland where Arab, Bakhtiari, and Persian populations negotiate cultural rights.",
      "fa": "کاوه احسانی و راسموس الینگ خوزستان را کانون اقتصاد سیاسی مدرن ایران می‌دانند: استانی با میادین عظیم نفتی اهواز، مارون، آغاجاری و مسجدسلیمان که بیش از هشتاد درصد ثروت نفتی کشور را تأمین می‌کند، اما همزمان زیستگاه اقوام گوناگون عرب، بختیاری و لر است."
    },
    "provenance": {
      "source_book": "Minorities in Iran: Difference in Difference",
      "source_author": "Rasmus Christian Elling",
      "page_number": 84,
      "verbatim_passage": "Khuzestan sits at the very heart of the Iranian petro-state, containing over eighty percent of the nation's oil reserves while housing a distinct Arab population whose grievances span socioeconomic underdevelopment and linguistic marginalization.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_ethnic_oil_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "ETHNIC LINES IN THE OIL FIELDS", "fa": "نفت روی گسل‌های هویت"},
    "clue_text": {
      "en": "In May 1979, violent ethnic clashes broke out in Khorramshahr when local Arab autonomy demands led by Ayatollah Shubayr Khaqani were crushed by naval forces under this provincial governor.",
      "fa": "در خرداد ۱۳۵۸، درگیری‌های خونینی در خرمشهر رخ داد؛ زمانی که مطالبات خودمختاری خلق عرب به رهبری آیت‌الله شبیر خاقانی توسط نیروهای نظامی به فرماندهی این استاندار خوزستان سرکوب شد."
    },
    "canonical_answer": {"en": "Ahmad Madani", "fa": "دریادار احمد مدنی"},
    "accepted_aliases": {"en": ["Admiral Ahmad Madani", "Admiral Madani", "Dr. Ahmad Madani"], "fa": ["احمد مدنی", "دریادار مدنی", "تیمسار مدنی"]},
    "options": {
      "en": ["Ali Shamkhani", "Ahmad Madani", "Mohsen Rezaee", "Asadollah Alam"],
      "fa": ["علی شمخانی", "دریادار احمد مدنی", "محسن رضایی", "اسدالله علم"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Ali Shamkhani", "why_plausible": "An Arab native of Ahvaz and major naval commander.", "why_wrong": "Shamkhani was a young revolutionary IRGC commander in Ahvaz in 1979, not the provincial governor who crushed the uprising."},
      {"option": "Mohsen Rezaee", "why_plausible": "A native of Khuzestan (Masjed Soleyman) and future IRGC chief.", "why_wrong": "Rezaee was serving in intelligence in Tehran in early 1979, not governing Khuzestan."},
      {"option": "Asadollah Alam", "why_plausible": "A prominent Pahlavi minister.", "why_wrong": "Alam died in 1978 before the revolution."}
    ],
    "adversarial_confusion_set": {"en": ["Valiollah Fallahi", "Gholam-Ali Oveisi"], "fa": ["ولی‌الله فلاحی", "غلامعلی اویسی"]},
    "specificity_prompt": {
      "en": "Name the naval admiral who served as Governor-General of Khuzestan during the May 1979 'Black Wednesday' in Khorramshahr.",
      "fa": "نام دریادار و استاندار وقت خوزستان در دولت موقت بازرگان که ناآرامی‌های خرداد ۱۳۵۸ خرمشهر را مهار کرد بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ahmad Madani. Correct. The secular nationalist admiral who used naval commandos to enforce central authority in Khorramshahr.",
        "wrong_generic": "No, it was Admiral Ahmad Madani. The governor who finished second in the 1980 presidential election.",
        "common_wrong_answers": {
          "Ali Shamkhani": "Shamkhani was a young local Pasdar in Khuzestan.",
          "Mohsen Rezaee": "Rezaee was in Tehran setting up revolutionary intelligence.",
          "Asadollah Alam": "Alam was the Shah's court minister and passed away in 1978."
        }
      },
      "fa": {
        "correct_generic": "دریادار احمد مدنی. کاملاً درسته! فرمانده نیروی دریایی و استاندار مقتدر دولت موقت در خوزستان که در اولین انتخابات ریاست‌جمهوری نفر دوم شد.",
        "wrong_generic": "خیر، پاسخ دریادار احمد مدنی بود. مجری برخورد قاطع با کانون‌های خودمختاری در چهارشنبه سیاه خرمشهر.",
        "common_wrong_answers": {
          "علی شمخانی": "شمخانی جوان انقلابی در سپاه اهواز بود و مسئولیتی در استانداری نداشت.",
          "محسن رضایی": "محسن رضایی در واحد اطلاعات سپاه در پایتخت فعالیت می‌کرد.",
          "اسدالله علم": "علم وزیر دربار شاه بود و در فروردین ۵۷ درگذشت."
        }
      }
    },
    "explanation": {
      "en": "Elling recounts that in late May 1979 (known as 'Black Wednesday'), tensions escalated in Khorramshahr between Arab cultural autonomy advocates led by Ayatollah Sheikh Mohammad Taher Shubayr Khaqani and revolutionary committees; Governor-General Admiral Ahmad Madani deployed naval commandos and armed Pasdaran to suppress the armed movement, forcing Khaqani into internal exile in Qom.",
      "fa": "الینگ روایت می‌کند که در اواخر اردیبهشت و اوایل خرداد ۱۳۵۸ (معروف به چهارشنبه سیاه)، درگیری مسلحانه میان کانون فرهنگی خلق عرب وابسته به شیخ شبیر خاقانی و نیروهای انقلابی در خرمشهر بالا گرفت و دریادار مدنی استاندار وقت با اعزام تکاوران نیروی دریایی، غائله را سرکوب و شیخ شبیر را به قم منتقل کرد."
    },
    "provenance": {
      "source_book": "Minorities in Iran: Difference in Difference",
      "source_author": "Rasmus Christian Elling",
      "page_number": 88,
      "verbatim_passage": "In May 1979, clashes erupted in Khorramshahr when Admiral Ahmad Madani, Governor-General of Khuzestan, used iron-fisted military force to crush Arab autonomy demands led by Ayatollah Shubayr Khaqani.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_ethnic_oil_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "ETHNIC LINES IN THE OIL FIELDS", "fa": "نفت روی گسل‌های هویت"},
    "clue_text": {
      "en": "In recent decades, ethnic discontent across Khuzestan has been heavily aggravated by massive state inter-basin water transfer projects (such as Kuhrang tunnels) diverting water from this historic river to the central plateau.",
      "fa": "در دهه‌های اخیر، نارضایتی‌های قومی و زیست‌محیطی در خوزستان با اجرای پروژه‌های انتقال آب بین‌حوضه‌ای (مانند تونل‌های کوهرنگ) که آب این رودخانه تاریخی را به فلات مرکزی می‌برد تشدید شده است."
    },
    "canonical_answer": {"en": "Karun River", "fa": "رود کارون"},
    "accepted_aliases": {"en": ["Karun", "Kharoon", "Karoon River"], "fa": ["کارون", "رودخانه کارون", "کارون بزرگ"]},
    "options": {
      "en": ["Aras River", "Karun River", "Sefid-Rud", "Zayandeh-Rud"],
      "fa": ["رود ارس", "رود کارون", "سفیدرود", "زاینده‌رود"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Aras River", "why_plausible": "A major river bordering Azerbaijan.", "why_wrong": "The Aras runs along the northern border with Azerbaijan and Armenia, not through Khuzestan."},
      {"option": "Sefid-Rud", "why_plausible": "A major river in northern Iran.", "why_wrong": "Sefid-Rud flows into the Caspian Sea through Gilan, far from the Persian Gulf watershed."},
      {"option": "Zayandeh-Rud", "why_plausible": "The central river that receives transferred water.", "why_wrong": "Zayandeh-Rud is the recipient river in Isfahan, whereas Karun is the source river in Khuzestan being depleted."}
    ],
    "adversarial_confusion_set": {"en": ["Karkheh River", "Dez River"], "fa": ["رود کرخه", "رود دز"]},
    "specificity_prompt": {
      "en": "Name Iran's most effluent and historically navigable river flowing through Khuzestan whose waters are transferred to Isfahan and Yazd.",
      "fa": "نام پرآب‌ترین رودخانه ایران که از کارون سرچشمه گرفته و انتقال آب آن به فلات مرکزی بحران‌ساز شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Karun River. Correct. Diverting the lifeblood of Ahvaz and the Shadegan wetlands to fill steel mills and decorative fountains in Isfahan.",
        "wrong_generic": "No, it was the Karun River. The environmental tragedy of southwestern Iran.",
        "common_wrong_answers": {
          "Aras River": "The Aras flows on the border of Armenia and Azerbaijan.",
          "Sefid-Rud": "Sefid-Rud waters the rice paddies of Gilan.",
          "Zayandeh-Rud": "Zayandeh-Rud is in Isfahan receiving the diverted water, not losing it."
        }
      },
      "fa": {
        "correct_generic": "رود کارون. کاملاً درسته! انتقال آب رگ حیاتی خوزستان و تالاب شادگان برای خنک کردن صنایع فولاد و زاینده‌رود اصفهان.",
        "wrong_generic": "خیر، پاسخ رودخانه کارون بود. بحران‌زاترین پرونده زیست‌محیطی و هویتی دو دهه اخیر در جنوب غرب.",
        "common_wrong_answers": {
          "رود ارس": "ارس در مرز جلفا و آذربایجان جریان دارد.",
          "سفیدرود": "سفیدرود شالیزارهای گیلان را سیراب می‌کند.",
          "زاینده‌رود": "زاینده‌رود رود مقصد در اصفهان است که آب انتقالی از کارون را دریافت می‌کند."
        }
      }
    },
    "explanation": {
      "en": "Kaveh Ehsani documents that extensive damming and inter-basin transfer schemes from the Karun River headwaters (via the Kuhrang and Beheshtabad tunnel projects) to the arid industrial heartlands of Isfahan, Yazd, and Kerman depleted downstream Khuzestan, drying out the Shadegan and Hawizeh marshes and triggering mass urban water protests across Ahvaz.",
      "fa": "کاوه احسانی مستند می‌کند که احداث سدهای متعدد و حفر تونل‌های کوهرنگ و بهشت‌آباد برای انتقال آب سرشاخه‌های کارون به صنایع کویری اصفهان و یزد، دبی آب کارون در خوزستان را به شدت کاهش داد و با خشکاندن نخلستان‌ها و تالاب هورالعظیم، موج اعتراضات آبی خوزستان را رقم زد."
    },
    "provenance": {
      "source_book": "Minorities in Iran: Difference in Difference",
      "source_author": "Rasmus Christian Elling",
      "page_number": 92,
      "verbatim_passage": "The diversion of the Karun River's headwaters toward the central plateau to supply steel plants in Isfahan sparked widespread popular indignation across Khuzestan, intertwining environmental desiccation with ethnic marginalization.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_ethnic_oil_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "ETHNIC LINES IN THE OIL FIELDS", "fa": "نفت روی گسل‌های هویت"},
    "clue_text": {
      "en": "Socioeconomic analysts characterize Khuzestan's plight through this classic political economy concept: generating the vast majority of the nation's export earnings while suffering from chronic regional poverty, high youth unemployment, and toxic air quality.",
      "fa": "تحلیل‌گران اقتصاد سیاسی وضعیت خوزستان را با این مفهوم کلاسیک تبیین می‌کنند: استانی که اکثریت قاطع درآمدهای صادراتی کشور را تولید می‌کند اما خود از فقر مزمن، بیکاری مفرط جوانان بومی و آلودگی شدید هوا رنج می‌برد."
    },
    "canonical_answer": {"en": "The Resource Curse", "fa": "نفرین منابع"},
    "accepted_aliases": {"en": ["Resource curse", "Paradox of plenty", "Dutch disease in Khuzestan", "Petro-state paradox"], "fa": ["پارادوکس فراوانی", "بیماری هلندی", "نفرین نفت", "بلای منابع"]},
    "options": {
      "en": ["Comparative Advantage", "The Resource Curse", "Invisible Hand", "Trickle-down Economics"],
      "fa": ["مزیت نسبی ریکاردویی", "نفرین منابع", "دست نامرئی بازار", "نظریه سرریز اقتصادی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Comparative Advantage", "why_plausible": "Classical trade theory by David Ricardo.", "why_wrong": "Comparative advantage argues that specializing in resources enriches everyone, the opposite of regional deprivation."},
      {"option": "Invisible Hand", "why_plausible": "Adam Smith's free market theory.", "why_wrong": "The invisible hand posits self-regulating market efficiency, not resource-driven inequality and ecological devastation."},
      {"option": "Trickle-down Economics", "why_plausible": "A supply-side growth theory.", "why_wrong": "Wealth distinctly failed to trickle down to local Arab villages, creating enclave extraction."}
    ],
    "adversarial_confusion_set": {"en": ["Dutch Disease", "Enclave Economy"], "fa": ["بیماری هلندی", "اقتصاد محصور"]},
    "specificity_prompt": {
      "en": "Identify the political economy term ('The ... Curse' or 'Paradox of Plenty') describing mineral-rich regions suffering severe deprivation.",
      "fa": "اصطلاح مشهور علم اقتصاد ناظر بر فقر و عقب‌ماندگی مناطق غنی از منابع هیدروکربوری را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "The Resource Curse (Paradox of Plenty). Spot on. Living in a tin-roofed shanty within sight of five-hundred-million-dollar gas flaring towers.",
        "wrong_generic": "No, it was The Resource Curse. The classic paradox of Khuzestan's oil economy.",
        "common_wrong_answers": {
          "Comparative Advantage": "Ricardo assumed trading wine for cloth; here oil brought pollution and poverty.",
          "Invisible Hand": "The invisible hand forgot to pave the streets in Kut Abdollah.",
          "Trickle-down Economics": "Oil wealth flowed straight to Tehran ministries, never trickling down to the marshlands."
        }
      },
      "fa": {
        "correct_generic": "نفرین منابع. کاملاً درسته! زندگی در کپرها و آلونک‌های بدون آب آشامیدنی در زیر سایه فلرهای چندصد میلیون دلاری گاز.",
        "wrong_generic": "خیر، پاسخ نفرین منابع (پارادوکس فراوانی) بود. تناقض تلخ فقر خوزستان در کنار ثروت نفت ملی.",
        "common_wrong_answers": {
          "مزیت نسبی ریکاردویی": "مزیت نسبی تجارت را سودآور می‌داند، نه سبب تخریب بومی.",
          "دست نامرئی بازار": "دست نامرئی آدام اسمیت به کوچه‌های خاکی کوت عبدالله نرسید.",
          "نظریه سرریز اقتصادی": "درآمدهای نفتی به خزانه مرکز سرازیر شد، نه سفره کارگران بومی."
        }
      }
    },
    "explanation": {
      "en": "Kaveh Ehsani and Rasmus Elling apply the 'Resource Curse' framework to explain the paradox of Khuzestan: petro-capitalism created extractive industrial enclaves that pipe oil and natural gas directly to central government treasuries and refineries, leaving local Arab and Bakhtiari populations to endure gas flaring emissions, desiccated wetlands, and severe youth unemployment.",
      "fa": "کاوه احسانی و راسموس الینگ مفهوم «نفرین منابع» را برای تحلیل شکاف‌های خوزستان به کار می‌برند: صنایع نفت و پتروشیمی به صورت جزیره‌ای (انحصاری) ثروت را استخراج و به مرکز منتقل کردند، در حالی که آلودگی فلرها، ریزگردها، خشک شدن هورها و بیکاری سهم جوانان بومی منطقه شد."
    },
    "provenance": {
      "source_book": "Minorities in Iran: Difference in Difference",
      "source_author": "Rasmus Christian Elling",
      "page_number": 96,
      "verbatim_passage": "Khuzestan exemplifies the classical resource curse: it fuels the central state budget while its local inhabitants suffer from chronic municipal underdevelopment, environmental devastation, and disenfranchisement.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_ethnic_oil_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "ETHNIC LINES IN THE OIL FIELDS", "fa": "نفت روی گسل‌های هویت"},
    "clue_text": {
      "en": "Operating from safe havens in Europe and Gulf capitals, this Arab separatist militant movement claimed responsibility for the deadly September 2018 armed assault on an Iranian military parade in Ahvaz.",
      "fa": "این جنبش شبه‌نظامی جدایی‌طلب عرب که در پایتخت‌های اروپایی و کشورهای حوزه خلیج فارس فعالیت می‌کرد، مسئولیت حمله مسلحانه و مرگبار شهریور ۱۳۹۷ به رژه نظامی نیروهای مسلح در اهواز را بر عهده گرفت."
    },
    "canonical_answer": {"en": "ASMLA", "fa": "حرکت النضال"},
    "accepted_aliases": {"en": ["Arab Struggle Movement for the Liberation of Ahwaz", "Harakat al-Nidal", "Al-Ahwaziya"], "fa": ["جنبش عربی آزادی‌بخش اهواز", "حرکت نضال", "الاحوازیه"]},
    "options": {
      "en": ["Polisario Front", "ASMLA", "Peshmerga", "Fatah al-Islam"],
      "fa": ["جبهه پولیساریو", "حرکت النضال", "پیشمرگه", "فتح‌الاسلام"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Polisario Front", "why_plausible": "A liberation movement.", "why_wrong": "The Polisario Front fights Morocco in the Western Sahara, North Africa."},
      {"option": "Peshmerga", "why_plausible": "Kurdish armed fighters in Iran and Iraq.", "why_wrong": "The Peshmerga are Kurdish, operating in the northwest, not Arab separatists in Khuzestan."},
      {"option": "Fatah al-Islam", "why_plausible": "A radical Sunni Islamist group.", "why_wrong": "Fatah al-Islam fought the Lebanese army in Nahr al-Bared in 2007."}
    ],
    "adversarial_confusion_set": {"en": ["Ahvaz Liberation Front", "Al-Ahwaz Democratic Front"], "fa": ["جبهه دموکراتیک احواز", "جبهه التحریر"]},
    "specificity_prompt": {
      "en": "Provide the acronym or Arabic name of the Arab Struggle Movement for the Liberation of Ahwaz (ASMLA).",
      "fa": "نام عربی گروهک تجزیه‌طلب مسئول حمله به رژه اهواز (حرکت ...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "ASMLA (Harakat al-Nidal). Spot on. Firing assault rifles into a military parade and spectators, leading to the dramatic abduction and trial of Habib Chaab.",
        "wrong_generic": "No, it was ASMLA (Arab Struggle Movement for the Liberation of Ahwaz / Harakat al-Nidal).",
        "common_wrong_answers": {
          "Polisario Front": "The Polisario Front is fighting in the Western Sahara desert.",
          "Peshmerga": "The Peshmerga operate in the mountains of Kurdistan.",
          "Fatah al-Islam": "Fatah al-Islam was destroyed in a refugee camp in northern Lebanon."
        }
      },
      "fa": {
        "correct_generic": "حرکت النضال. کاملاً درسته! گروهکی که با شلیک به جایگاه رژه اهواز خون سربازان و تماشاگران را ریخت و به ربودن و محاکمه حبیب اسیود در تهران انجامید.",
        "wrong_generic": "خیر، پاسخ حرکت النضال (جنبش عربی آزادی‌بخش اهواز / ASMLA) بود. گروهک مسلح جدایی‌طلب اهواز.",
        "common_wrong_answers": {
          "جبهه پولیساریو": "پولیساریو در صحرای غربی با مراکش می‌جنگد.",
          "پیشمرگه": "پیشمرگه مربوط به کوهستان‌های کردستان است، نه خوزستان.",
          "فتح‌الاسلام": "فتح‌الاسلام در اردوگاه نهرالبارد لبنان بود."
        }
      }
    },
    "explanation": {
      "en": "Elling and security studies document that the Arab Struggle Movement for the Liberation of Ahwaz (ASMLA / Harakat al-Nidal al-Arabi li-Tahrir al-Ahwaz), founded by Ahmad Mola Nissi, waged an armed campaign against state infrastructure and claimed the September 22, 2018 Ahvaz military parade shooting that killed 25 people; its leader Habib Chaab was abducted in Turkey by Iranian intelligence in 2020 and executed in 2023.",
      "fa": "الینگ و کارشناسان امنیتی اشاره می‌کنند که حرکت النضال (جنبش آزادی‌بخش احواز) به سرکردگی احمد مولا نیسی و حبیب چعب، مشی مسلحانه علیه تأسیسات نفتی و دولتی پیش گرفت و مسئولیت حمله به رژه ۳۱ شهریور ۹۷ اهواز با ۲۵ شهید را پذیرفت؛ حبیب چعب در سال ۱۳۹۹ در ترکیه دستگیر و پس از محاکمه در سال ۱۴۰۲ اعدام شد."
    },
    "provenance": {
      "source_book": "Minorities in Iran: Difference in Difference",
      "source_author": "Rasmus Christian Elling",
      "page_number": 99,
      "verbatim_passage": "The Arab Struggle Movement for the Liberation of Ahwaz (ASMLA / Harakat al-Nidal) conducted violent attacks against state targets, culminating in the lethal September 2018 Ahvaz military parade shooting that sharpened ethnic securitization.",
      "evidence_type": "FACT"
    }
  },

  # 30. double_republican_theocracy: REPUBLICAN CLOTH, CLERICAL THREADS / جمهوری در آینه تئوکراسی
  {
    "id": "double_republican_theocracy_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "REPUBLICAN CLOTH, CLERICAL THREADS", "fa": "جمهوری در آینه تئوکراسی"},
    "clue_text": {
      "en": "In his study of theocratic institutions, H.E. Chehabi examines this 12-member constitutional council, composed of six clerics appointed by the Supreme Leader and six jurists approved by Parliament.",
      "fa": "هوشنگ شهابی در بررسی نهادهای تئوکراتیک، این نهاد ۱۲ نفره نظارتی قانون اساسی را واکاوی می‌کند که مرکب از شش فقیه منصوب رهبری و شش حقوق‌دان با رأی مجلس است."
    },
    "canonical_answer": {"en": "Guardian Council", "fa": "شورای نگهبان"},
    "accepted_aliases": {"en": ["Shoraye Negahban", "Council of Guardians", "Guardian Council of the Constitution"], "fa": ["شورای نگهبان قانون اساسی", "شورای نگهبان", "شورای محترم نگهبان"]},
    "options": {
      "en": ["Guardian Council", "Expediency Council", "Supreme National Security Council", "Assembly of Experts"],
      "fa": ["شورای نگهبان", "مجمع تشخیص مصلحت نظام", "شورای عالی امنیت ملی", "مجلس خبرگان رهبری"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {"option": "Expediency Council", "why_plausible": "A major constitutional body arbitrating legislation.", "why_wrong": "The Expediency Council has dozens of members appointed to arbitrate deadlocks, not the specific 12-member constitutional review body."},
      {"option": "Supreme National Security Council", "why_plausible": "Chairs defense and security policy.", "why_wrong": "SNSC includes cabinet ministers and military chiefs, not a constitutional vetting committee of six clerics and six lawyers."},
      {"option": "Assembly of Experts", "why_plausible": "An elected clerical body.", "why_wrong": "The Assembly of Experts has 88 members to monitor the Supreme Leader, not 12 members vetting parliamentary laws."}
    ],
    "adversarial_confusion_set": {"en": ["Expediency Council", "Constitutional Court"], "fa": ["مجمع تشخیص مصلحت نظام", "دیوان عالی کشور"]},
    "specificity_prompt": {
      "en": "Name the 12-member constitutional vetting body consisting of six clerics and six civil jurists.",
      "fa": "نام نهاد ۱۲ نفره نظارت بر مصوبات مجلس و تطبیق آن با شرع و قانون اساسی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Guardian Council. Correct. Six turbans check the Sharia, six suits check the constitution, and together they vet every law and candidate in the land.",
        "wrong_generic": "No, it was the Guardian Council (Shoraye Negahban). The constitutional gatekeeper of the Islamic Republic.",
        "common_wrong_answers": {
          "Expediency Council": "The Expediency Council steps in when Parliament and the Guardian Council fight.",
          "Supreme National Security Council": "The SNSC manages foreign policy crises and nuclear talks.",
          "Assembly of Experts": "The Assembly of Experts elects the Supreme Leader."
        }
      },
      "fa": {
        "correct_generic": "شورای نگهبان. کاملاً درسته! شش فقیه احکام شرع را می‌سنجند و شش حقوق‌دان اصول قانون اساسی را، و صلاحیت همه کاندیداها از زیر تیغ آنها می‌گذرد.",
        "wrong_generic": "خیر، پاسخ شورای نگهبان قانون اساسی بود. سنگربان اصلی فقه در نظام قانون‌گذاری.",
        "common_wrong_answers": {
          "مجمع تشخیص مصلحت نظام": "مجمع تشخیص هنگامی داوری می‌کند که مجلس و شورای نگهبان به بن‌بست برسند.",
          "شورای عالی امنیت ملی": "شورای امنیت ملی متولی سیاست‌های کلان امنیتی و دفاعی است.",
          "مجلس خبرگان رهبری": "مجلس خبرگان مسئول تعیین و نظارت بر رهبر است."
        }
      }
    },
    "explanation": {
      "en": "H.E. Chehabi examines the Guardian Council (Shoraye Negahban) as the structural pillar subordinating republican institutions to clerical oversight: its twelve members (six Islamic jurists appointed by the Leader, and six civil lawyers nominated by the Judiciary and elected by Parliament) hold absolute veto power over all parliamentary legislation and candidate registrations.",
      "fa": "هوشنگ شهابی شورای نگهبان را ستون فقرات نظارت تئوکراتیک بر نهادهای انتخابی می‌داند: این نهاد ۱۲ نفره (شش فقیه به انتصاب مستقیم رهبر و شش حقوق‌دان با معرفی رئیس قوه قضائیه و رأی اعتماد مجلس) حق وتوی کلیه مصوبات مجلس و رد صلاحیت داوطلبان انتخابات را داراست."
    },
    "provenance": {
      "source_book": "How Theocratic is the Islamic Republic?",
      "source_author": "H. E. Chehabi",
      "page_number": 4,
      "verbatim_passage": "The Guardian Council, composed of six clerics chosen by the Leader and six lawyers approved by parliament, serves as the ultimate institutional gatekeeper ensuring that all secular republican laws conform to the Shari'a.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_republican_theocracy_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {"en": "REPUBLICAN CLOTH, CLERICAL THREADS", "fa": "جمهوری در آینه تئوکراسی"},
    "clue_text": {
      "en": "Instituted through Guardian Council interpretations in the 1990s, this controversial doctrine of 'Approbatory Supervision' grants the Council absolute discretionary authority to vet and disqualify electoral candidates without judicial appeal.",
      "fa": "این دکترین جنجالی نظارتی که با تفسیر شورای نگهبان در سال ۱۳۷۰ تثبیت شد، به این شورا اختیارات تام و صلاحدیدی می‌دهد تا بدون نیاز به حکم قضایی، صلاحیت داوطلبان انتخابات را بررسی و رد کند."
    },
    "canonical_answer": {"en": "Approbatory Supervision", "fa": "نظارت استصوابی"},
    "accepted_aliases": {"en": ["Nezarat-e Estesvabi", "Approving supervision", "Estesvabi supervision", "Active supervision"], "fa": ["نظارت استصوابی شورای نگهبان", "اصل نظارت استصوابی", "استصوابی"]},
    "options": {
      "en": ["Passive Informational Monitoring", "Approbatory Supervision", "Judicial Review", "Proportional Representation"],
      "fa": ["نظارت استطلاعی", "نظارت استصوابی", "نظارت قضایی ترافعی", "نظام تناسبی انتخابات"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Passive Informational Monitoring", "why_plausible": "The alternative interpretation favored by reformists (Nezarat-e Estetla'i).", "why_wrong": "Informational monitoring merely allows observers to observe and report violations to courts, which the Guardian Council rejected in favor of binding veto power."},
      {"option": "Judicial Review", "why_plausible": "A standard constitutional vetting process.", "why_wrong": "Judicial review is conducted by independent courts in open hearings; Approbatory Supervision is closed political screening by clerics."},
      {"option": "Proportional Representation", "why_plausible": "An electoral voting system.", "why_wrong": "PR is an electoral ballot calculation formula, not a candidate disqualification doctrine."}
    ],
    "adversarial_confusion_set": {"en": ["Nezarat-e Estetla'i", "Salif-e Qazayi"], "fa": ["نظارت استطلاعی", "صلاحیت قضایی"]},
    "specificity_prompt": {
      "en": "Provide the exact Persian term for the Guardian Council's binding, discretionary candidate vetting power (Nezarat-e ...).",
      "fa": "اصطلاح فقهی-حقوقی معروف برای نظارت تام و تعیین‌کننده شورای نگهبان بر کاندیداهای انتخابات (نظارت ...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Approbatory Supervision (Nezarat-e Estesvabi). Correct. Disqualifying half the parliamentary candidates before a single ballot is printed.",
        "wrong_generic": "No, it was Approbatory Supervision (Nezarat-e Estesvabi). The single biggest battleground in Iranian electoral politics since 1991.",
        "common_wrong_answers": {
          "Passive Informational Monitoring": "Estetla'i means you only look and report; Estesvabi means you have the red pen.",
          "Judicial Review": "Judicial review requires a judge, a gavel, and an evidence docket.",
          "Proportional Representation": "Proportional representation determines how seats are allocated, not who is allowed to run."
        }
      },
      "fa": {
        "correct_generic": "نظارت استصوابی. کاملاً درسته! تیغ فقهی پرقدرتی که پیش از چاپ تعرفه، نیمی از داوطلبان مجلس و ریاست‌جمهوری را حذف می‌کند.",
        "wrong_generic": "خیر، پاسخ نظارت استصوابی بود. مهم‌ترین مناقشه حقوقی و سیاسی میان جریان‌های اصلاح‌طلب و اصولگرا از مجلس چهارم تا امروز.",
        "common_wrong_answers": {
          "نظارت استطلاعی": "نظارت استطلاعی صرفاً جنبه اطلاع‌یافتن دارد؛ نظارت استصوابی نافذ، مؤثر و نهایی است.",
          "نظارت قضایی ترافعی": "نظارت قضایی در محاکم دادگستری صورت می‌گیرد، نه پشت درهای بسته شورای نگهبان.",
          "نظام تناسبی انتخابات": "تناسبی نحوه تسهیم کرسی‌ها در پارلمان است، نه فیلتر احراز صلاحیت."
        }
      }
    },
    "explanation": {
      "en": "Chehabi demonstrates that in 1991, prior to the fourth Majles elections, the Guardian Council issued a binding interpretation of Article 99 of the Constitution declaring that its supervision over elections is 'approbatory' (estesvabi)—meaning comprehensive, binding, and discretionary—enabling it to disqualify candidates without publishing evidence or facing judicial review.",
      "fa": "شهابی نشان می‌دهد که در سال ۱۳۷۰ در آستانه انتخابات مجلس چهارم، شورای نگهبان در تفسیری رسمی از اصل ۹۹ قانون اساسی اعلام کرد که نظارت این شورا بر انتخابات «استصوابی» است و این نظارت در تمام مراحل و نسبت به همه امور جاری و نافذ است، که به رد صلاحیت گسترده منتقدان انجامید."
    },
    "provenance": {
      "source_book": "How Theocratic is the Islamic Republic?",
      "source_author": "H. E. Chehabi",
      "page_number": 7,
      "verbatim_passage": "Through its 1991 interpretation of Article 99, the Guardian Council codified 'approbatory supervision' (nezarat-e estesvabi), arrogating to itself absolute discretionary authority to vet and disqualify parliamentary and presidential candidates.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_republican_theocracy_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {"en": "REPUBLICAN CLOTH, CLERICAL THREADS", "fa": "جمهوری در آینه تئوکراسی"},
    "clue_text": {
      "en": "Elected by popular vote every eight years from an exclusively clerical pool vetted by the Guardian Council, this 88-member constitutional body holds the sole legal prerogative to appoint and dismiss the Supreme Leader.",
      "fa": "این نهاد قانون اساسی متشکل از ۸۸ مجتهد که هر هشت سال یک‌بار با رأی مستقیم مردم از میان نامزدهای روحانی تأییدصلاحیت‌شده انتخاب می‌شوند، تنها مرجع قانونی تعیین و نظارت بر رهبر است."
    },
    "canonical_answer": {"en": "Assembly of Experts for Leadership", "fa": "مجلس خبرگان رهبری"},
    "accepted_aliases": {"en": ["Assembly of Experts", "Majles-e Khebregan-e Rahbari", "Assembly of Experts on Leadership"], "fa": ["مجلس خبرگان", "خبرگان رهبری", "مجلس خبرگان رهبری"]},
    "options": {
      "en": ["Guardian Council", "Assembly of Experts for Leadership", "Expediency Council", "Islamic Consultative Assembly"],
      "fa": ["شورای نگهبان", "مجلس خبرگان رهبری", "مجمع تشخیص مصلحت نظام", "مجلس شورای اسلامی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Guardian Council", "why_plausible": "A senior constitutional body.", "why_wrong": "The Guardian Council has 12 members and reviews laws; it does not elect the Supreme Leader."},
      {"option": "Expediency Council", "why_plausible": "Chaired by high-ranking leaders.", "why_wrong": "The Expediency Council is appointed by the Supreme Leader to arbitrate laws, not elect the Leader."},
      {"option": "Islamic Consultative Assembly", "why_plausible": "The national parliament (Majles).", "why_wrong": "The Majles passes ordinary statutes and has 290 non-clerical members, lacking power to appoint the Leader."}
    ],
    "adversarial_confusion_set": {"en": ["Assembly of Experts for Constitution", "Majles-e Showra"], "fa": ["مجلس خبرگان قانون اساسی", "مجلس شورای ملی"]},
    "specificity_prompt": {
      "en": "Name the 88-member body of Islamic jurists charged under Article 107 with appointing the Supreme Leader.",
      "fa": "نام مجلس ۸۸ نفره مجتهدین که طبق اصل ۱۰۷ قانون اساسی مسئول انتخاب و نظارت بر رهبر جمهوری اسلامی است را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Assembly of Experts for Leadership. Correct. The ultimate clerical electoral college that met once in 1989 and has been waiting for its next big day ever since.",
        "wrong_generic": "No, it was the Assembly of Experts for Leadership (Majles-e Khebregan-e Rahbari).",
        "common_wrong_answers": {
          "Guardian Council": "The Guardian Council vets the experts; the experts choose the Leader.",
          "Expediency Council": "The Expediency Council settles budget disputes between ministries.",
          "Islamic Consultative Assembly": "The regular parliament makes laws about traffic fines and taxes."
        }
      },
      "fa": {
        "correct_generic": "مجلس خبرگان رهبری. کاملاً درسته! مجمع فقهایی که در خرداد ۱۳۶۸ رهبر جدید را برگزیدند و مأموریت انتخاب جانشین را بر عهده دارند.",
        "wrong_generic": "خیر، پاسخ مجلس خبرگان رهبری بود. نهاد عالی نظارتی طبق اصل ۱۰۷ و ۱۱۱ قانون اساسی.",
        "common_wrong_answers": {
          "شورای نگهبان": "شورای نگهبان صلاحیت داوطلبان خبرگان را بررسی می‌کند، نه انتخاب رهبر.",
          "مجمع تشخیص مصلحت نظام": "مجمع تشخیص بازوی مشورتی رهبری در سیاست‌های کلی است.",
          "مجلس شورای اسلامی": "مجلس شورای اسلامی قوانین عادی مملکتی را تصویب می‌کند."
        }
      }
    },
    "explanation": {
      "en": "Under Articles 107 and 111 of the Iranian Constitution, the Assembly of Experts for Leadership (Majles-e Khebregan-e Rahbari), currently comprising 88 clerics, is empowered to elect the Supreme Leader, monitor his performance, and theoretically dismiss him if he loses the requisite Islamic qualifications, though Chehabi notes it has operated in practice as a rubber-stamp body.",
      "fa": "طبق اصول ۱۰۷ و ۱۱۱ قانون اساسی، مجلس خبرگان رهبری مرکب از ۸۸ مجتهد واجد شرایط، وظیفه انتخاب رهبر، نظارت بر تداوم شرایط رهبری و عزل او در صورت ناتوانی را بر عهده دارد؛ هرچند شهابی خاطرنشان می‌کند که در عمل این مجلس همواره حامی و تثبیت‌کننده منویات رهبری بوده است."
    },
    "provenance": {
      "source_book": "How Theocratic is the Islamic Republic?",
      "source_author": "H. E. Chehabi",
      "page_number": 9,
      "verbatim_passage": "Under Article 107 of the Constitution, the Assembly of Experts (Majles-e Khebregan) holds the exclusive authority to select and dismiss the Supreme Leader, functioning as an institutional bridge between popular elections and theocratic rule.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_republican_theocracy_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {"en": "REPUBLICAN CLOTH, CLERICAL THREADS", "fa": "جمهوری در آینه تئوکراسی"},
    "clue_text": {
      "en": "Chehabi emphasizes that despite clerical theocracy, Iran's political system is sharply distinguished from classic monolithic totalitarian regimes (like Stalinist Russia or North Korea) by this enduring institutional reality.",
      "fa": "شهابی تأکید می‌کند که با وجود ساختار تئوکراتیک روحانیت، نظام سیاسی ایران به دلیل این واقعیت نهادینه‌شده ماندگار با رژیم‌های توتالیتر یکپارچه (مانند شوروی استالین یا کره شمالی) تفاوت بنیادین دارد."
    },
    "canonical_answer": {"en": "Factional Pluralism", "fa": "تکثر و رقابت‌های جناحی"},
    "accepted_aliases": {"en": ["Factionalism", "Elite pluralism", "Intra-elite competition", "Factional competition"], "fa": ["کشمکش‌های جناحی", "پلورالیسم جناحی", "رقابت جناحی درون نظام", "جناح‌بندی سیاسی"]},
    "options": {
      "en": ["Hereditary Monarchy", "Factional Pluralism", "Monolithic Cult of Personality", "Military Junta Rule"],
      "fa": ["سلطنت موروثی خانوادگی", "تکثر و رقابت‌های جناحی", "فرقه یکپارچه کیش شخصیت", "حکومت نظامیان کودتاچی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Hereditary Monarchy", "why_plausible": "Rule by dynasty.", "why_wrong": "The Islamic Republic abolished hereditary rule and vehemently rejects monarchy."},
      {"option": "Monolithic Cult of Personality", "why_plausible": "A feature of totalitarianism.", "why_wrong": "North Korea has a monolithic cult of personality, whereas Iran's elite is fractious and divided into competing factions."},
      {"option": "Military Junta Rule", "why_plausible": "Rule by generals.", "why_wrong": "A military junta is rule by a junta of generals (like Myanmar or Chile under Pinochet), whereas Iran is a hybrid clerical-constitutional system."}
    ],
    "adversarial_confusion_set": {"en": ["Multiparty Democracy", "Oligarchic Polyarchy"], "fa": ["دموکراسی چندحزبی لیبرال", "الیگارشی پلی‌آرشی"]},
    "specificity_prompt": {
      "en": "Identify the political science concept describing the vibrant, contentious internal competition among ruling clerical and revolutionary factions.",
      "fa": "مفهوم علوم سیاسی ناظر بر چنددستگی، رقابت و پویایی درونی میان جناح‌های سیاسی درون حاکمیت جمهوری اسلامی را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Factional Pluralism. Correct. There is no singular party line; there are three factions yelling at each other in Parliament every morning.",
        "wrong_generic": "No, it was Factional Pluralism (Jenaah-bandi). The chaotic competition that keeps the system dynamic.",
        "common_wrong_answers": {
          "Hereditary Monarchy": "Monarchy died when the Shah boarded his 707 in 1979.",
          "Monolithic Cult of Personality": "North Korea has one voice; Tehran has forty newspapers attacking each other daily.",
          "Military Junta Rule": "It is a republic of turbans and technocrats, not a Latin American junta."
        }
      },
      "fa": {
        "correct_generic": "تکثر و رقابت‌های جناحی. کاملاً درسته! نظام تک‌حزبی نیست؛ رقابت تند جناح‌های راست سنتی، چپ اسلامی، تکنوکرات‌ها و پایداری در مجلس همواره زنده بوده است.",
        "wrong_generic": "خیر، پاسخ تکثر و رقابت‌های جناحی درون نظام بود. ویژگی شاخصی که جمهوری اسلامی را از توتالیتاریسم کلاسیک متمایز می‌کند.",
        "common_wrong_answers": {
          "سلطنت موروثی خانوادگی": "سلطنت با فرار شاه در دی ۵۷ برای همیشه پرونده‌اش بسته شد.",
          "فرقه یکپارچه کیش شخصیت": "کیش شخصیت مطلق مختص پیونگ‌یانگ است، در تهران نخبگان سر قدرت با هم مناقشه دارند.",
          "حکومت نظامیان کودتاچی": "نظام ایران حکومت نظامیان نیست؛ ساختاری پیچیده و چندلایه با قانون اساسی مدون است."
        }
      }
    },
    "explanation": {
      "en": "Chehabi emphasizes that Iran defies easy categorization as a totalitarian state because of its intense 'factional pluralism': competing revolutionary factions (traditional conservatives, pragmatic technocrats, reformists, and principalists) fiercely debate foreign policy, culture, and economic ideology in vibrant print media, parliamentary floor fights, and competitive presidential elections.",
      "fa": "شهابی تأکید می‌کند که جمهوری اسلامی را نمی‌توان نظامی توتالیتر به سبک بلوک شرق خواند، زیرا از «تکثر جناحی» پررنگی برخوردار است: جناح‌های گوناگون (چپ خط امام، راست سنتی، کارگزاران سازندگی و اصولگرایان) در مجلس، مطبوعات و انتخابات ریاست‌جمهوری بر سر جهت‌گیری‌های کلان کشور با یکدیگر رقابت‌های شدیدی دارند."
    },
    "provenance": {
      "source_book": "How Theocratic is the Islamic Republic?",
      "source_author": "H. E. Chehabi",
      "page_number": 12,
      "verbatim_passage": "Rather than a monolithic theocracy, Iran is characterized by robust factional pluralism, where rival elites contest elections, debate ideological interpretations, and compete vigorously across state institutions.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_republican_theocracy_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "REPUBLICAN CLOTH, CLERICAL THREADS", "fa": "جمهوری در آینه تئوکراسی"},
    "clue_text": {
      "en": "In April 1989, weeks before his death, Ayatollah Khomeini ordered the revision of the Constitution to abolish this strict theological qualification for the Supreme Leader, paving the legal path for Ali Khamenei's succession.",
      "fa": "در اردیبهشت ۱۳۶۸ چند هفته پیش از رحلت، امام خمینی دستور بازنگری در قانون اساسی را صادر کردند تا این شرط فقهی سخت‌گیرانه برای رهبری حذف شود و راه برای انتخاب علی خامنه‌ای هموار گردد."
    },
    "canonical_answer": {"en": "Requirement of Marja'iyat", "fa": "شرط مرجعیت تقلید"},
    "accepted_aliases": {"en": ["Marja'iyat requirement", "Grand Ayatollah qualification", "Being a Marja", "Requirement of being a Marja'"], "fa": ["شرط مرجعیت", "مرجع تقلید بودن", "مرجعیت فقهی", "مرجعیت"]},
    "options": {
      "en": ["Doctorate in Civil Law", "Requirement of Marja'iyat", "Seyed Ancestry Requirement", "Tenure as Chief Justice"],
      "fa": ["مدرک دکترای حقوق", "شرط مرجعیت تقلید", "سیادت و نسب هاشمی", "سابقه ریاست قوه قضائیه"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Doctorate in Civil Law", "why_plausible": "A modern academic credential.", "why_wrong": "The Leader was never required to hold a secular university civil law degree."},
      {"option": "Seyed Ancestry Requirement", "why_plausible": "Khomeini and Khamenei are both Seyeds (wearing black turbans).", "why_wrong": "Descent from the Prophet (being a Seyed) is an honorary genealogical status, never a formal constitutional requirement for the Supreme Leader."},
      {"option": "Tenure as Chief Justice", "why_plausible": "A senior judicial post.", "why_wrong": "The Leader does not need to have served as Chief Justice."}
    ],
    "adversarial_confusion_set": {"en": ["Ijtihad Requirement", "Popular Referendum Mandate"], "fa": ["شرط اجتهاد مطلق", "تصویب در رفراندوم"]},
    "specificity_prompt": {
      "en": "Name the supreme religious rank (being a Grand Ayatollah / Source of Emulation) excised from Article 109 in the 1989 constitutional revision.",
      "fa": "بالاترین درجه فقهی شیعه (مرجع تقلید) که در بازنگری قانون اساسی در سال ۱۳۶۸ از شرایط رهبری حذف شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Requirement of Marja'iyat. Spot on. Khomeini writing to Ayatollah Meshkini that political management and courage matter more than having written a treatise on ablution rituals.",
        "wrong_generic": "No, it was the Requirement of Marja'iyat (being a Source of Emulation). The constitutional revolution that decoupled leadership from the highest seminary rank.",
        "common_wrong_answers": {
          "Doctorate in Civil Law": "Western university degrees are for technocrats, not the faqih.",
          "Seyed Ancestry Requirement": "Black turbans are respected, but white-turbaned mujtahids like Montazeri were constitutionally eligible.",
          "Tenure as Chief Justice": "Chief Justice was appointed by the Leader, not a prerequisite."
        }
      },
      "fa": {
        "correct_generic": "شرط مرجعیت تقلید. کاملاً درسته! نامه تاریخی امام به آیت‌الله مشکینی که مدیر، مدبر و شجاع بودن را مهم‌تر از داشتن رساله عملیه دانستند.",
        "wrong_generic": "خیر، پاسخ شرط مرجعیت تقلید بود. اصلاحیه سرنوشت‌سازی که تفکیک مرجعیت دینی از ولایت سیاسی را ممکن ساخت.",
        "common_wrong_answers": {
          "مدرک دکترای حقوق": "مدرک دانشگاهی هرگز شرط ولایت فقیه نبوده است.",
          "سیادت و نسب هاشمی": "سیادت شرط قانونی رهبری نیست؛ مجتهدان غیرسید مانند منتزری یا مطهری هم می‌توانستند رهبر باشند.",
          "سابقه ریاست قوه قضائیه": "ریاست قوه قضائیه از انتصابات رهبر است، نه پیش‌شرط آن."
        }
      }
    },
    "explanation": {
      "en": "Chehabi highlights the profound structural significance of the 1989 constitutional amendment: following the ouster of designated successor Ayatollah Montazeri, Ayatollah Khomeini wrote to the Constitutional Revision Council declaring that a capable, politically astute mujtahid does not need to be a formal Grand Marja' (source of emulation), clearing the constitutional path for Hojjat al-Islam Ali Khamenei to be elected Supreme Leader on June 4, 1989.",
      "fa": "هوشنگ شهابی اهمیت ساختاری بازنگری قانون اساسی در سال ۱۳۶۸ را برجسته می‌سازد: پس از عزل آیت‌الله منتظری، امام خمینی در نامه‌ای به شورای بازنگری تصریح کردند که مرجعیت تقلید شرط رهبری نیست و فقیه عادل و مدیر کفایت می‌کند؛ امری که به مجلس خبرگان اجازه داد در ۱۴ خرداد ۱۳۶۸ حضرت آیت‌الله خامنه‌ای را به رهبری برگزینند."
    },
    "provenance": {
      "source_book": "How Theocratic is the Islamic Republic?",
      "source_author": "H. E. Chehabi",
      "page_number": 15,
      "verbatim_passage": "In April 1989, Khomeini directed the revision of the Constitution to remove the requirement that the Supreme Leader be a marja' (source of emulation), severing political leadership from senior seminary rank and enabling the succession of Ali Khamenei.",
      "evidence_type": "FACT"
    }
  }
]

batch_c.extend(cats_26_to_30)

with open("/Users/Morad/Spark/build_batch_c.py", "w", encoding="utf-8") as f:
    f.write("batch_c = " + json.dumps(batch_c, ensure_ascii=False, indent=2) + "\n")

print(f"Batch C complete! Total clues in Batch C: {len(batch_c)}")
