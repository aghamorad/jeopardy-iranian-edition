import json
import sys
sys.path.append("/Users/Morad/Spark")
from build_batch_c import batch_c
from jeopardy_pipeline import validate_clue_schema

cats_23_to_25 = [
  # 23. single_embassy_anatomy: ANATOMY OF A TEHRAN BARRICADE / سفارت‌گیری با مجوز تاریخ
  {
    "id": "single_embassy_anatomy_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {"en": "ANATOMY OF A TEHRAN BARRICADE", "fa": "سفارت‌گیری با مجوز تاریخ"},
    "clue_text": {
      "en": "On November 4, 1979, the US Embassy compound in central Tehran was breached and occupied by radical revolutionary university students calling themselves by this name.",
      "fa": "در ۱۳ آبان ۱۳۵۸، محوطه سفارت آمریکا در مرکز تهران توسط دانشجویان انقلابی با این عنوان اشغال شد."
    },
    "canonical_answer": {"en": "Muslim Student Followers of the Imam's Line", "fa": "دانشجویان مسلمان پیرو خط امام"},
    "accepted_aliases": {"en": ["Students Following the Line of the Imam", "Daneshjuyan-e Peyrow-e Khatt-e Emam", "Muslim Students of the Imam's Line"], "fa": ["دانشجویان خط امام", "دانشجویان مسلمان پیرو خط امام", "دانشجویان پیرو خط امام"]},
    "options": {
      "en": ["Fada'iyan-e Islam", "Muslim Student Followers of the Imam's Line", "Mojahedin-e Khalq", "Tudeh Youth League"],
      "fa": ["فدائیان اسلام", "دانشجویان مسلمان پیرو خط امام", "سازمان مجاهدین خلق", "جوانان حزب توده"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Fada'iyan-e Islam", "why_plausible": "A historic fundamentalist group from the 1950s.", "why_wrong": "Fada'iyan was a mid-20th century underground group, not the 1979 university student collective."},
      {"option": "Mojahedin-e Khalq", "why_plausible": "A major armed opposition group active in 1979.", "why_wrong": "The MEK tried to claim credit outside, but the actual organizers inside were Khomeinist students."},
      {"option": "Tudeh Youth League", "why_plausible": "The communist party youth wing.", "why_wrong": "The takeover was explicitly Islamist and loyal to Khomeini, not communist."}
    ],
    "adversarial_confusion_set": {"en": ["Daftar-e Tahkim-e Vahdat", "Sazman-e Mojahedin"], "fa": ["دفتر تحکیم وحدت", "سازمان مجاهدین انقلاب"]},
    "specificity_prompt": {
      "en": "Name the specific student organization that executed the 1979 seizure of the US Embassy in Tehran.",
      "fa": "نام کامل تشکل دانشجویی تسخیرکننده سفارت آمریکا در آبان ۱۳۵۸ را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Muslim Student Followers of the Imam's Line. Correct. Planning a forty-eight-hour sit-in that lasted 444 days.",
        "wrong_generic": "No, it was the Muslim Student Followers of the Imam's Line (Daneshjuyan-e Peyrow-e Khatt-e Emam).",
        "common_wrong_answers": {
          "Fada'iyan-e Islam": "Fada'iyan was Navvab Safavi in the 1950s; these were engineering students in 1979.",
          "Mojahedin-e Khalq": "The MEK cheered from the sidewalk; Khomeini's students held the gates.",
          "Tudeh Youth League": "The communists supported the takeover from afar, but weren't given the keys."
        }
      },
      "fa": {
        "correct_generic": "دانشجویان مسلمان پیرو خط امام. کاملاً درسته! تحصنی که قرار بود ۴۸ ساعت طول بکشد اما ۴۴۴ روز به درازا انجامید.",
        "wrong_generic": "خیر، پاسخ دانشجویان مسلمان پیرو خط امام بود. تسخیرکنندگانی که دیپلماسی دو کشور را منجمد کردند.",
        "common_wrong_answers": {
          "فدائیان اسلام": "نواب صفوی دهه‌ها قبل تیرباران شده بود؛ این‌ها دانشجویان پلی‌تکنیک و تهران بودند.",
          "سازمان مجاهدین خلق": "مجاهدین خلق پشت در شعار می‌دادند، اما تسخیر کار دانشجویان خط امام بود.",
          "جوانان حزب توده": "توده‌ای‌ها از بیرون هورا می‌کشیدند اما کلید لانه دست بچه‌های خط امام بود."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian recounts that on November 4, 1979, university students stormed the compound calling themselves the 'Muslim Student Followers of the Imam's Line' to preempt any attempt by Prime Minister Bazargan to normalize relations with Washington.",
      "fa": "یرواند آبراهامیان روایت می‌کند که در ۱۳ آبان ۱۳۵۸ دانشجویان با عنوان «دانشجویان مسلمان پیرو خط امام» وارد سفارت آمریکا شدند تا مانع از عادی‌سازی روابط میان دولت موقت بازرگان و واشنگتن شوند."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 62,
      "verbatim_passage": "On November 4, 1979, the Muslim Student Followers of the Imam's Line seized the US embassy, triggering a 444-day hostage crisis that shattered the provisional government and radicalized the revolution.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_embassy_anatomy_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "ANATOMY OF A TEHRAN BARRICADE", "fa": "سفارت‌گیری با مجوز تاریخ"},
    "clue_text": {
      "en": "The immediate catalyst that prompted the students to storm the embassy was President Jimmy Carter's decision to admit this exiled monarch into the United States for cancer medical treatment.",
      "fa": "جرقه مستقیمی که دانشجویان را به تسخیر سفارت واداشت، تصمیم جیمی کارتر برای پذیرش این پادشاه مخلوع به آمریکا جهت معالجه پزشکی بیماری سرطان بود."
    },
    "canonical_answer": {"en": "Mohammad Reza Pahlavi", "fa": "محمدرضا پهلوی"},
    "accepted_aliases": {"en": ["The Shah", "Shah of Iran", "Mohammad Reza Shah"], "fa": ["شاه", "محمدرضا شاه", "محمدرضاشاه پهلوی"]},
    "options": {
      "en": ["Reza Shah", "Mohammad Reza Pahlavi", "King Farouk", "Sultan Qaboos"],
      "fa": ["رضاشاه", "محمدرضا پهلوی", "ملک فاروق", "سلطان قابوس"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Reza Shah", "why_plausible": "The founder of the Pahlavi dynasty.", "why_wrong": "Reza Shah died in exile in Johannesburg in 1944."},
      {"option": "King Farouk", "why_plausible": "The former King of Egypt.", "why_wrong": "King Farouk was overthrown in 1952 and died in 1965."},
      {"option": "Sultan Qaboos", "why_plausible": "The long-ruling Sultan of Oman.", "why_wrong": "Sultan Qaboos was an ally who ruled Oman, not an exiled monarch in 1979."}
    ],
    "adversarial_confusion_set": {"en": ["Reza Pahlavi", "Shapur Bakhtiar"], "fa": ["رضا پهلوی", "شاپور بختیار"]},
    "specificity_prompt": {
      "en": "Name the specific deposed Iranian monarch admitted to a New York hospital in October 1979.",
      "fa": "نام پادشاه مخلوع ایران که ورودش به بیمارستان نیویورک موجب خشم انقلابیون شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad Reza Pahlavi. Correct. Admitting the dying Shah for medical treatment became the most expensive hospital stay in geopolitical history.",
        "wrong_generic": "No, it was Mohammad Reza Pahlavi (the Shah). The decision that sank the Carter presidency.",
        "common_wrong_answers": {
          "Reza Shah": "Reza Shah died in South Africa thirty-five years earlier.",
          "King Farouk": "Farouk was the King of Egypt who died in Rome.",
          "Sultan Qaboos": "Qaboos ruled Oman peacefully for fifty years."
        }
      },
      "fa": {
        "correct_generic": "محمدرضا پهلوی. کاملاً درسته! صدور ویزای درمان برای شاه مخلوع که به سقوط دولت بازرگان و شکست کارتر انجامید.",
        "wrong_generic": "خیر، پاسخ محمدرضا پهلوی بود. تصمیمی که آتش خشم انقلابیون را شعله‌ور ساخت.",
        "common_wrong_answers": {
          "رضاشاه": "رضاشاه در سال ۱۳۲۳ در آفریقای جنوبی درگذشته بود.",
          "ملک فاروق": "ملک فاروق پادشاه مخلوع مصر بود.",
          "سلطان قابوس": "سلطان قابوس حاکم عمان بود."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian notes that when Jimmy Carter admitted the deposed Shah to New York in late October 1979, revolutionaries feared a repeat of the 1953 CIA coup, triggering the preemptive seizure of the embassy.",
      "fa": "یرواند آبراهامیان اشاره می‌کند که با ورود شاه به بیمارستان نیویورک، خاطره کودتای ۲۸ مرداد ۱۳۳۲ زنده شد و انقلابیون برای جلوگیری از کودتای مجدد، سفارت را تسخیر کردند."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 64,
      "verbatim_passage": "The immediate spark was Carter's fateful decision in October 1979 to admit the deposed Shah into the United States for medical treatment, raising widespread fears in Tehran of a second CIA-engineered counter-coup.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_embassy_anatomy_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {"en": "ANATOMY OF A TEHRAN BARRICADE", "fa": "سفارت‌گیری با مجوز تاریخ"},
    "clue_text": {
      "en": "Painstakingly piecing together shredded embassy cables strip by strip using skilled carpet weavers, the students published dozens of volumes of intelligence under this famous multi-volume title.",
      "fa": "دانشجویان با بهره‌گیری از هنر قالیبافان سنتی و کنار هم چیدن رشته‌های اسناد خردشده سفارت، ده‌ها جلد کتاب اطلاعاتی را با این عنوان پرآوازه منتشر کردند."
    },
    "canonical_answer": {"en": "Documents from the US Espionage Den", "fa": "اسناد لانه جاسوسی"},
    "accepted_aliases": {"en": ["Asnad-e Laneh-ye Jasusi", "Espionage Den Documents", "Documents from the Nest of Spies"], "fa": ["اسناد لانه جاسوسی آمریکا", "کتاب‌های لانه جاسوسی", "اسناد سفارت آمریکا"]},
    "options": {
      "en": ["Pentagon Papers", "Documents from the US Espionage Den", "Mitrokhin Archive", "WikiLeaks Cables"],
      "fa": ["اسناد پنتاگون", "اسناد لانه جاسوسی", "بایگانی میتروخین", "افشاگری‌های ویکی‌لیکس"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Pentagon Papers", "why_plausible": "A famous leak of US defense files.", "why_wrong": "The Pentagon Papers concerned the Vietnam War and were published in 1971."},
      {"option": "Mitrokhin Archive", "why_plausible": "A major intelligence leak.", "why_wrong": "The Mitrokhin Archive contains KGB files smuggled from Russia in 1992."},
      {"option": "WikiLeaks Cables", "why_plausible": "Massive release of State Department cables.", "why_wrong": "WikiLeaks published digital files in 2010, thirty years after Tehran."}
    ],
    "adversarial_confusion_set": {"en": ["SAVAK Archives", "Tehran Cables"], "fa": ["اسناد ساواک", "پرونده‌های سفارت"]},
    "specificity_prompt": {
      "en": "Name the multi-volume book series published by the students containing reconstructed shredded embassy documents.",
      "fa": "عنوان مجموعه کتاب‌های چندجلدی اسناد بازسازی‌شده سفارت آمریکا توسط دانشجویان را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Documents from the US Espionage Den. Correct. Carpet weavers patiently gluing paper strips back together into political dynamite.",
        "wrong_generic": "No, it was the Documents from the US Espionage Den (Asnad-e Laneh-ye Jasusi). Seventy volumes of confidential cables.",
        "common_wrong_answers": {
          "Pentagon Papers": "The Pentagon Papers were about Vietnam in the New York Times.",
          "Mitrokhin Archive": "Mitrokhin smuggled KGB notes out of Moscow.",
          "WikiLeaks Cables": "WikiLeaks was digital files in 2010; these were paper shreds."
        }
      },
      "fa": {
        "correct_generic": "اسناد لانه جاسوسی. کاملاً درسته! چسباندن رشته‌های کاغذ خردشده توسط دختران دانشجو که به انتشار ده‌ها جلد سند محرمانه انجامید.",
        "wrong_generic": "خیر، پاسخ اسناد لانه جاسوسی بود. مجموعه‌ای از اسناد دیپلماتیک محرمانه.",
        "common_wrong_answers": {
          "اسناد پنتاگون": "اسناد پنتاگون افشاگری جنگ ویتنام بود.",
          "بایگانی میتروخین": "میتروخین اسناد کا‌گ‌ب را به غرب برد.",
          "افشاگری‌های ویکی‌لیکس": "ویکی‌لیکس اسناد دیجیتال سال ۲۰۱۰ بود."
        }
      }
    },
    "explanation": {
      "en": "Abrahamian highlights that the publication of over seventy volumes of *Asnad-e Laneh-ye Jasusi* was weaponized by radical factions to brand moderate politicians as Western agents and purge them from the state apparatus.",
      "fa": "آبراهامیان اشاره می‌کند که انتشار بیش از ۷۰ جلد اسناد لانه جاسوسی به ابزاری برای متهم کردن چهره‌های میانه‌رو به جاسوسی و حذف آنان از بدنه حکومت تبدیل شد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 66,
      "verbatim_passage": "By reconstructing shredded embassy cables strip by strip, the students published over seventy volumes titled Documents from the US Espionage Den (Asnad-e Laneh-ye Jasusi), using them as political artillery to discredit the liberal opposition.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_embassy_anatomy_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {"en": "ANATOMY OF A TEHRAN BARRICADE", "fa": "سفارت‌گیری با مجوز تاریخ"},
    "clue_text": {
      "en": "Within forty-eight hours of the embassy's occupation, this liberal nationalist Prime Minister and his entire provisional cabinet submitted their resignations, realizing that Khomeini had endorsed the students over the formal government.",
      "fa": "ظرف ۴۸ ساعت پس از اشغال سفارت، این نخست‌وزیر ملی‌گرای میانه‌رو و تمام اعضای کابینه دولت موقت استعفا دادند، چرا که دریافتند امام خمینی اقدام دانشجویان را بر دولت رسمی ترجیح داده است."
    },
    "canonical_answer": {"en": "Mehdi Bazargan", "fa": "مهدی بازرگان"},
    "accepted_aliases": {"en": ["Bazargan", "Prime Minister Bazargan", "Engineer Mehdi Bazargan"], "fa": ["مهندس بازرگان", "مهندس مهدی بازرگان", "بازرگان"]},
    "options": {
      "en": ["Karim Sanjabi", "Mehdi Bazargan", "Shapur Bakhtiar", "Ali Amini"],
      "fa": ["کریم سنجابی", "مهدی بازرگان", "شاپور بختیار", "علی امینی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Karim Sanjabi", "why_plausible": "Foreign Minister who resigned earlier.", "why_wrong": "Sanjabi resigned in April 1979, months before the embassy crisis."},
      {"option": "Shapur Bakhtiar", "why_plausible": "The Shah's last prime minister.", "why_wrong": "Bakhtiar fled Iran in February 1979 and was in exile in Paris."},
      {"option": "Ali Amini", "why_plausible": "A former prime minister.", "why_wrong": "Amini served as premier under the Shah in 1961, not during the revolutionary transition."}
    ],
    "adversarial_confusion_set": {"en": ["Ebrahim Yazdi", "Sadegh Ghotbzadeh"], "fa": ["ابراهیم یزدی", "صادق قطب‌زاده"]},
    "specificity_prompt": {
      "en": "Name the Prime Minister of the Provisional Government whose cabinet resigned on November 6, 1979.",
      "fa": "نام نخست‌وزیر دولت موقت که در ۱۵ آبان ۱۳۵۸ در اعتراض به تسخیر سفارت استعفا کرد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mehdi Bazargan. Correct. Shaking hands with Brzezinski in Algiers on Friday, out of power by Tuesday.",
        "wrong_generic": "No, it was Mehdi Bazargan. The end of the Provisional Government.",
        "common_wrong_answers": {
          "Karim Sanjabi": "Sanjabi had already stepped down in April.",
          "Shapur Bakhtiar": "Bakhtiar was in exile in Paris.",
          "Ali Amini": "Amini governed in 1961."
        }
      },
      "fa": {
        "correct_generic": "مهدی بازرگان. کاملاً درسته! دست دادن با برژینسکی در الجزایر و کناره‌گیری رسمی از قدرت چند روز بعد.",
        "wrong_generic": "خیر، پاسخ مهندس مهدی بازرگان بود. پایان مأموریت دولت موقت در آبان ۵۸.",
        "common_wrong_answers": {
          "کریم سنجابی": "دکتر سنجابی در فروردین ۵۸ از وزارت خارجه استعفا داد.",
          "شاپور بختیار": "بختیار آخرین نخست‌وزیر شاه در پاریس بود.",
          "علی امینی": "علی امینی نخست‌وزیر سال ۱۳۴۰ بود."
        }
      }
    },
    "explanation": {
      "en": "Ervand Abrahamian emphasizes that the embassy takeover ended the Provisional Government: Prime Minister Mehdi Bazargan and his cabinet resigned on November 6, 1979, transferring full state executive authority to the Revolutionary Council.",
      "fa": "یرواند آبراهامیان تأکید می‌کند که تسخیر سفارت پایان کار دولت موقت را رقم زد و با استعفای بازرگان در ۱۵ آبان ۱۳۵۸، شورای انقلاب اداره کامل کشور را به دست گرفت."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 68,
      "verbatim_passage": "Two days after the embassy compound fell, Mehdi Bazargan and his provisional cabinet resigned, realizing they had been utterly outflanked by the radical students and that Khomeini had endorsed the takeover as 'a second revolution greater than the first.'",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_embassy_anatomy_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "ANATOMY OF A TEHRAN BARRICADE", "fa": "سفارت‌گیری با مجوز تاریخ"},
    "clue_text": {
      "en": "The 52 remaining American hostages were finally liberated on January 20, 1981, after exactly 444 days in captivity, released through Algerian diplomatic mediation under this historic bilateral accord.",
      "fa": "۵۲ گروگان آمریکایی سرانجام در ۳۰ دی ۱۳۵۹ پس از دقیقاً ۴۴۴ روز اسارت، با میانجی‌گری دیپلماتیک دولت الجزایر بر اساس این توافقنامه تاریخی آزاد شدند."
    },
    "canonical_answer": {"en": "Algiers Accords", "fa": "بیانیه الجزایر"},
    "accepted_aliases": {"en": ["Algiers Agreement", "1981 Algiers Accords", "Algiers Declarations"], "fa": ["قرارداد الجزایر", "بیانیه‌های الجزایر", "توافقنامه الجزایر"]},
    "options": {
      "en": ["Dayton Accords", "Algiers Accords", "Oslo Accords", "Camp David Accords"],
      "fa": ["پیمان دیتون", "بیانیه الجزایر", "پیمان اسلو", "پیمان کمپ دیوید"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Dayton Accords", "why_plausible": "A famous peace treaty.", "why_wrong": "The Dayton Accords ended the Bosnian War in 1995."},
      {"option": "Oslo Accords", "why_plausible": "A famous Middle Eastern breakthrough.", "why_wrong": "The Oslo Accords governed Israeli-PLO negotiations in 1993."},
      {"option": "Camp David Accords", "why_plausible": "A famous diplomatic treaty.", "why_wrong": "Camp David was the 1978 Egypt-Israel accord."}
    ],
    "adversarial_confusion_set": {"en": ["1975 Algiers Agreement", "Paris Accords"], "fa": ["قرارداد ۱۹۷۵ الجزایر", "پیمان پاریس"]},
    "specificity_prompt": {
      "en": "Name the specific 1981 bilateral accord signed between the United States and Iran that resolved the hostage crisis.",
      "fa": "نام بیانیه و توافقنامه بین‌المللی سال ۱۳۵۹ که منجر به آزادی گروگان‌های آمریکایی شد را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Algiers Accords. Spot on. Releasing the hostages the moment Ronald Reagan finished taking the oath of office.",
        "wrong_generic": "No, it was the Algiers Accords (January 1981). Establishing the Hague Claims Tribunal.",
        "common_wrong_answers": {
          "Dayton Accords": "Dayton was Bosnia in 1995.",
          "Oslo Accords": "Oslo was Palestine in 1993.",
          "Camp David Accords": "Camp David was Egypt and Israel in 1978."
        }
      },
      "fa": {
        "correct_generic": "بیانیه الجزایر. کاملاً درسته! پرواز هواپیمای گروگان‌ها دقیقاً همزمان با پایان مراسم تحلیف ریگان.",
        "wrong_generic": "خیر، پاسخ بیانیه الجزایر بود. سندی که دعوای گروگان‌گیری را در دیوان لاهه سامان داد.",
        "common_wrong_answers": {
          "پیمان دیتون": "دیتون مربوط به بوسنی در سال ۱۹۹۵ است.",
          "پیمان اسلو": "اسلو توافق سال ۱۹۹۳ فلسطین و اسرائیل بود.",
          "پیمان کمپ دیوید": "کمپ دیوید صلح مصر و اسرائیل در سال ۱۹۷۸ بود."
        }
      }
    },
    "explanation": {
      "en": "Signed on January 19, 1981, through Algerian mediation, the Algiers Accords pledged US non-intervention in Iranian internal affairs, unfroze roughly eight billion dollars in Iranian assets, and created the Iran-United States Claims Tribunal at The Hague.",
      "fa": "بیانیه‌های الجزایر در دی ۱۳۵۹ با وساطت الجزایر امضا شد و آمریکا متعهد به عدم مداخله در امور داخلی ایران و آزادسازی دارایی‌های مسدودشده شد و دیوان داوری لاهه تشکیل شد."
    },
    "provenance": {
      "source_book": "Khomeinism: Essays on the Islamic Republic",
      "source_author": "Ervand Abrahamian",
      "page_number": 71,
      "verbatim_passage": "The Algiers Accords ended the 444-day standoff on January 20, 1981, freeing the fifty-two hostages at the precise moment of Ronald Reagan's inauguration and establishing the Iran-US Claims Tribunal at The Hague.",
      "evidence_type": "FACT"
    }
  },

  # 24. single_caspian_equation: THE CASPIAN EQUATION / خزر با سهم مساویِ نامساوی
  {
    "id": "single_caspian_equation_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {"en": "THE CASPIAN EQUATION", "fa": "خزر با سهم مساویِ نامساوی"},
    "clue_text": {
      "en": "Bordering northern Iran along Gilan, Mazandaran, and Golestan, this vast body of water is the world's largest enclosed inland water body, containing massive sturgeon caviar and offshore petroleum reserves.",
      "fa": "این پهنه آبی پهناور در سواحل شمالی استان‌های گیلان، مازندران و گلستان، بزرگ‌ترین پیکره آبی محصور در خشکی جهان است که ذخایر عظیم خاویار و نفت را در بر دارد."
    },
    "canonical_answer": {"en": "Caspian Sea", "fa": "دریای خزر"},
    "accepted_aliases": {"en": ["Caspian", "Mazandaran Sea", "Daryaye Khazar"], "fa": ["دریای مازندران", "خزر", "دریای قزوین"]},
    "options": {
      "en": ["Black Sea", "Caspian Sea", "Aral Sea", "Lake Urmia"],
      "fa": ["دریای سیاه", "دریای خزر", "دریای آرال", "دریاچه ارومیه"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Black Sea", "why_plausible": "A major sea in the region.", "why_wrong": "The Black Sea connects to the Mediterranean through the Turkish Straits and does not border Iran."},
      {"option": "Aral Sea", "why_plausible": "A famous inland lake in Central Asia.", "why_wrong": "The Aral Sea sits between Kazakhstan and Uzbekistan and has largely dried up."},
      {"option": "Lake Urmia", "why_plausible": "An inland salt lake inside Iran.", "why_wrong": "Lake Urmia is an internal hypersaline lake in northwestern Iran, not an international sea bordering Russia and Turkmenistan."}
    ],
    "adversarial_confusion_set": {"en": ["Persian Gulf", "Sea of Oman"], "fa": ["خلیج فارس", "دریای عمان"]},
    "specificity_prompt": {
      "en": "Name the world's largest inland sea bordering northern Iran.",
      "fa": "نام بزرگ‌ترین دریاچه جهان واقع در شمال ایران را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Caspian Sea. Correct. The inland sea of beluga sturgeon, oil platforms, and century-long legal debates.",
        "wrong_generic": "No, it was the Caspian Sea (Daryaye Khazar / Mazandaran).",
        "common_wrong_answers": {
          "Black Sea": "The Black Sea is bordered by Turkey and Ukraine, not Iran.",
          "Aral Sea": "The Aral Sea is a dried-up tragedy in Uzbekistan.",
          "Lake Urmia": "Lake Urmia is in Azerbaijan, not on the northern border."
        }
      },
      "fa": {
        "correct_generic": "دریای خزر. کاملاً درسته! پهنه آبی خاویار بلوگا، دکل‌های نفتی و دهه‌ها مناقشه حقوقی رژیم بهره‌برداری.",
        "wrong_generic": "خیر، پاسخ دریای خزر (دریای مازندران) بود. بزرگ‌ترین دریاچه روی کره زمین.",
        "common_wrong_answers": {
          "دریای سیاه": "دریای سیاه در شمال ترکیه است و با ایران هم‌مرز نیست.",
          "دریای آرال": "دریای آرال در آسیای میانه است و بخش اعظم آن خشک شده است.",
          "دریاچه ارومیه": "دریاچه ارومیه در شمال غرب کشور و درون ایران واقع است."
        }
      }
    },
    "explanation": {
      "en": "The Caspian Sea, bordering Iran to the north along with Russia, Azerbaijan, Kazakhstan, and Turkmenistan, is the world's largest enclosed body of water, historically governed by bilateral Soviet-Iranian treaties before multilateral negotiations emerged post-1991.",
      "fa": "دریای خزر بزرگ‌ترین پهنه آبی بسته جهان است که از جنوب به ایران متصل است و پس از فروپاشی شوروی، رژیم حقوقی آن از یک توافق دوجانبه به مذاکراتی پیچیده میان پنج کشور ساحلی تبدیل شد."
    },
    "provenance": {
      "source_book": "The Caspian Sea: A Quest for Environmental Security",
      "source_author": "Asghar Jafari Valdani",
      "page_number": 12,
      "verbatim_passage": "The Caspian Sea, encompassing approximately 371,000 square kilometers, represents the planet's largest enclosed inland water body, holding immense geostrategic importance for Iran's northern frontiers.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_caspian_equation_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "THE CASPIAN EQUATION", "fa": "خزر با سهم مساویِ نامساوی"},
    "clue_text": {
      "en": "Prior to 1991, the legal regime of the Caspian Sea was defined by bilateral friendship and commerce treaties signed between Iran and this northern superpower in 1921 and 1940.",
      "fa": "پیش از سال ۱۳۷۰، رژیم حقوقی دریای خزر بر اساس قراردادهای دوستی و بازرگانی دوجانبه منعقدشده میان ایران و این ابرقدرت شمالی در سال‌های ۱۹۲۱ و ۱۹۴۰ تنظیم می‌شد."
    },
    "canonical_answer": {"en": "Soviet Union", "fa": "اتحاد جماهیر شوروی"},
    "accepted_aliases": {"en": ["USSR", "Soviet Russia", "Soviets"], "fa": ["شوروی", "دولت شوروی", "اتحاد شوروی"]},
    "options": {
      "en": ["British Empire", "Soviet Union", "Ottoman Empire", "Qing Dynasty"],
      "fa": ["امپراتوری بریتانیا", "اتحاد جماهیر شوروی", "امپراتوری عثمانی", "سلسله چینگ"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "British Empire", "why_plausible": "A major imperial power operating in Iran.", "why_wrong": "Britain had naval influence in the Persian Gulf, not the inland Caspian."},
      {"option": "Ottoman Empire", "why_plausible": "A historic neighbor.", "why_wrong": "The Ottoman Empire collapsed in 1922 and bordered Iran on the western land frontier, not the Caspian."},
      {"option": "Qing Dynasty", "why_plausible": "Imperial power in Asia.", "why_wrong": "Qing China fell in 1912 and never reached the Caspian basin."}
    ],
    "adversarial_confusion_set": {"en": ["Tsarist Russia", "Russian Federation"], "fa": ["روسیه تزاری", "فدراسیون روسیه"]},
    "specificity_prompt": {
      "en": "Name the communist superpower that shared the Caspian condominium with Iran from 1921 to 1991.",
      "fa": "نام ابرقدرت شرقی همسایه شمالی ایران در معاهدات ۱۹۲۱ و ۱۹۴۰ را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Soviet Union. Correct. Back when dividing the Caspian was simple: Moscow took the north, Tehran took the south, and nobody asked Baku or Astana.",
        "wrong_generic": "No, it was the Soviet Union (USSR). The treaties of 1921 and 1940 treated the Caspian as a joint Soviet-Iranian sea.",
        "common_wrong_answers": {
          "British Empire": "The British were busy controlling the oil tankers in the Persian Gulf.",
          "Ottoman Empire": "The Ottomans bordered Tabriz and Baghdad, not the Caspian shore.",
          "Qing Dynasty": "China was thousands of miles east across the mountains."
        }
      },
      "fa": {
        "correct_generic": "اتحاد جماهیر شوروی. کاملاً درسته! دورانی که خزر فقط دو صاحب داشت: مسکو در شمال و تهران در جنوب.",
        "wrong_generic": "خیر، پاسخ اتحاد جماهیر شوروی بود. معاهدات ۱۹۲۱ و ۱۹۴۰ که دریای ایران و شوروی را تعریف می‌کردند.",
        "common_wrong_answers": {
          "امپراتوری بریتانیا": "انگلیسی‌ها در آب‌های خلیج فارس نفوذ داشتند، نه در خزر.",
          "امپراتوری عثمانی": "عثمانی همسایه غربی بود و ساحلی در خزر نداشت.",
          "سلسله چینگ": "چین فرسنگ‌ها آن سوتر در شرق آسیا بود."
        }
      }
    },
    "explanation": {
      "en": "The 1921 Treaty of Friendship and the 1940 Commerce and Navigation Agreement between Iran and the Soviet Union established the Caspian as a 'Soviet-Iranian Sea' (condominium), guaranteeing equal navigation rights and a 10-mile exclusive fishing zone without delimiting the seabed.",
      "fa": "قرارداد ۱۹۲۱ دوستی و موافقت‌نامه ۱۹۴۰ بازرگانی و بحرپیمایی میان ایران و شوروی، خزر را دریای مشترک (مشاع) دو کشور اعلام کرد که در آن حق کشتیرانی آزاد و منطقه انحصاری ماهیگیری ۱۰ مایلی لحاظ شده بود اما بستر دریا تحدید حدود نشده بود."
    },
    "provenance": {
      "source_book": "The Caspian Sea: A Quest for Environmental Security",
      "source_author": "Asghar Jafari Valdani",
      "page_number": 28,
      "verbatim_passage": "The 1921 and 1940 treaties established a condominium regime over the Caspian Sea between Iran and the USSR, recognizing it as a closed common lake with equal rights of navigation.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_caspian_equation_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {"en": "THE CASPIAN EQUATION", "fa": "خزر با سهم مساویِ نامساوی"},
    "clue_text": {
      "en": "The legal regime of the Caspian Sea was thrown into complete turmoil in December 1991 due to this monumental geopolitical event, which suddenly expanded the number of littoral states from two to five.",
      "fa": "رژیم حقوقی دریای خزر در آذر ۱۳۷۰ بر اثر این رخداد ژئوپلیتیکی سترگ دچار تحول بنیادین شد؛ واقعه‌ای که ناگهان تعداد کشورهای ساحلی خزر را از ۲ کشور به ۵ کشور افزایش داد."
    },
    "canonical_answer": {"en": "Dissolution of the Soviet Union", "fa": "فروپاشی اتحاد جماهیر شوروی"},
    "accepted_aliases": {"en": ["Collapse of the Soviet Union", "Fall of the USSR", "Soviet collapse", "Dissolution of the USSR"], "fa": ["فروپاشی شوروی", "انحلال شوروی", "سقوط اتحاد جماهیر شوروی"]},
    "options": {
      "en": ["Treaty of Versailles", "Dissolution of the Soviet Union", "Cuban Missile Crisis", "Suez Crisis"],
      "fa": ["معاهده ورسای", "فروپاشی اتحاد جماهیر شوروی", "بحران موشکی کوبا", "بحران کانال سوئز"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Treaty of Versailles", "why_plausible": "A major treaty reshaping borders.", "why_wrong": "Versailles ended WWI in 1919 in Western Europe."},
      {"option": "Cuban Missile Crisis", "why_plausible": "A major Cold War standoff.", "why_wrong": "Took place in the Caribbean in 1962, without affecting the Caspian legal status."},
      {"option": "Suez Crisis", "why_plausible": "A major Middle East waterway conflict.", "why_wrong": "Occurred in 1956 in Egypt regarding the nationalization of the Suez Canal."}
    ],
    "adversarial_confusion_set": {"en": ["Fall of the Berlin Wall", "Yugoslav Breakup"], "fa": ["سقوط دیوار برلین", "فروپاشی یوگسلاوی"]},
    "specificity_prompt": {
      "en": "Identify the historical event in December 1991 that created Azerbaijan, Kazakhstan, and Turkmenistan as new Caspian littoral states.",
      "fa": "رخداد تاریخی سال ۱۹۹۱ که جمهوری‌های جدید آذربایجان، قزاقستان و ترکمنستان را در سواحل خزر پدید آورد بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Dissolution of the Soviet Union. Correct. Going to bed sharing a sea with one superpower, and waking up sharing it with Russia, Azerbaijan, Kazakhstan, and Turkmenistan.",
        "wrong_generic": "No, it was the Dissolution of the Soviet Union in December 1991. The birth of a five-way Caspian diplomatic headache.",
        "common_wrong_answers": {
          "Treaty of Versailles": "Versailles redraw Europe in 1919.",
          "Cuban Missile Crisis": "Cuba was nuclear war in the Caribbean in 1962.",
          "Suez Crisis": "Suez was Nasser in 1956."
        }
      },
      "fa": {
        "correct_generic": "فروپاشی اتحاد جماهیر شوروی. کاملاً درسته! شب خوابیدن با یک همسایه مقتدر، و صبح بیدار شدن با چهار کشور مستقل تازه تأسیس.",
        "wrong_generic": "خیر، پاسخ فروپاشی اتحاد جماهیر شوروی در سال ۱۹۹۱ بود. رویدادی که معادله حقوقی خزر را پنج‌ضلعی کرد.",
        "common_wrong_answers": {
          "معاهده ورسای": "ورسای پایان جنگ جهانی اول در سال ۱۹۱۹ بود.",
          "بحران موشکی کوبا": "بحران موشکی در دریای کارائیب در سال ۱۹۶۲ رخ داد.",
          "بحران کانال سوئز": "کانال سوئز بحران مصر در سال ۱۹۵۶ بود."
        }
      }
    },
    "explanation": {
      "en": "With the collapse of the USSR in December 1991, the Caspian littoral expanded from two nations (Iran and the USSR) to five: Iran, Russia, Azerbaijan, Kazakhstan, and Turkmenistan, igniting decades of bitter dispute over whether the body should be partitioned as a lake under international water law or divided as an enclosed sea.",
      "fa": "با فروپاشی شوروی در آذر ۱۳۷۰، تعداد کشورهای ساحلی خزر از دو کشور به پنج کشور (ایران، روسیه، آذربایجان، قزاقستان و ترکمنستان) افزایش یافت و مناقشات گسترده‌ای پیرامون تقسیم دریا بر اساس حقوق دریاها یا رژیم دریاچه‌های بسته درگرفت."
    },
    "provenance": {
      "source_book": "The Caspian Sea: A Quest for Environmental Security",
      "source_author": "Asghar Jafari Valdani",
      "page_number": 35,
      "verbatim_passage": "The dissolution of the Soviet Union in late 1991 transformed the Caspian from a stable bilateral condominium into a complex multilateral dispute among five sovereign littoral states.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_caspian_equation_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE CASPIAN EQUATION", "fa": "خزر با سهم مساویِ نامساوی"},
    "clue_text": {
      "en": "After twenty-two years of grueling multilateral negotiations, the five littoral heads of state met in this Kazakh port city in August 2018 to sign the historic Convention on the Legal Status of the Caspian Sea.",
      "fa": "پس از ۲۲ سال مذاکرات فشرده چندجانبه، سران پنج کشور ساحلی در مرداد ۱۳۹۷ در این بندر قزاقستان گرد هم آمدند تا کنوانسیون تاریخی رژیم حقوقی دریای خزر را امضا کنند."
    },
    "canonical_answer": {"en": "Aktau", "fa": "آکتائو"},
    "accepted_aliases": {"en": ["City of Aktau", "Aqtau", "Aktau Summit"], "fa": ["بندر آکتائو", "شهر آکتائو", "آکتائو قزاقستان"]},
    "options": {
      "en": ["Astana", "Aktau", "Baku", "Ashgabat"],
      "fa": ["آستانه", "آکتائو", "باکو", "عشق‌آباد"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Astana", "why_plausible": "Capital of Kazakhstan.", "why_wrong": "Astana is an inland city on the steppe; the Caspian summit was hosted in the coastal port of Aktau."},
      {"option": "Baku", "why_plausible": "The premier oil port on the Caspian in Azerbaijan.", "why_wrong": "Baku hosted earlier working groups, but the landmark 2018 summit was hosted in Kazakhstan's port of Aktau."},
      {"option": "Ashgabat", "why_plausible": "Capital of Turkmenistan.", "why_wrong": "Ashgabat hosted summits in 2002 and 2022, not the 2018 landmark convention signing."}
    ],
    "adversarial_confusion_set": {"en": ["Atyrau", "Turkmenbashi"], "fa": ["آتیرائو", "ترکمن‌باشی"]},
    "specificity_prompt": {
      "en": "Name the specific Kazakh port city where the 2018 Convention on the Legal Status of the Caspian Sea was signed.",
      "fa": "نام بندر کشور قزاقستان که محل امضای کنوانسیون رژیم حقوقی خزر در مرداد ۱۳۹۷ بود را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Aktau. Correct. The summit where Hassan Rouhani signed the convention, sparking furious domestic debates in Tehran over whether Iran gave away its historic share.",
        "wrong_generic": "No, it was Aktau (in Kazakhstan). The August 2018 Caspian treaty summit.",
        "common_wrong_answers": {
          "Astana": "Astana is the steppe capital with glassy futuristic towers; Aktau is the port on the Caspian shore.",
          "Baku": "Baku was too controversial to host the compromise signing.",
          "Ashgabat": "Ashgabat is the city of white marble monuments in Turkmenistan."
        }
      },
      "fa": {
        "correct_generic": "آکتائو. کاملاً درسته! اجلاسی در مرداد ۹۷ با حضور حسن روحانی که امضای آن با جنجال‌های فراوان در رسانه‌های تهران بر سر سهم ایران همراه شد.",
        "wrong_generic": "خیر، پاسخ بندر آکتائو در قزاقستان بود. محل امضای کنوانسیون رژیم حقوقی دریای خزر پس از دو دهه کشمکش.",
        "common_wrong_answers": {
          "آستانه": "آستانه پایتخت قزاقستان در دشت‌های شمالی است؛ آکتائو بندر ساحلی خزر است.",
          "باکو": "باکو به دلیل مناقشات میادین نفتی با ترکمنستان و ایران میزبان امضای نهایی نشد.",
          "عشق‌آباد": "عشق‌آباد پایتخت سنگ مرمرین ترکمنستان است."
        }
      }
    },
    "explanation": {
      "en": "On August 12, 2018, the leaders of Iran, Russia, Kazakhstan, Azerbaijan, and Turkmenistan signed the Convention on the Legal Status of the Caspian Sea in Aktau, Kazakhstan, granting the Caspian special legal status (neither lake nor sea), establishing 15-mile territorial waters and 10-mile fishing zones, while deferring the contentious delimitation of the seabed to future bilateral negotiations.",
      "fa": "در ۲۱ مرداد ۱۳۹۷، سران پنج کشور ساحلی در بندر آکتائوی قزاقستان کنوانسیون رژیم حقوقی را امضا کردند که وضعیت ویژه (نه دریا و نه دریاچه) را برای خزر تصویب کرد و پهنای ۱۵ مایلی آب‌های سرزمینی و ۱۰ مایلی ماهیگیری را مشخص ساخت، در حالی که تحدید بستر و زیربستر به مذاکرات دوجانبه بعدی موکول شد."
    },
    "provenance": {
      "source_book": "The Caspian Sea: A Quest for Environmental Security",
      "source_author": "Asghar Jafari Valdani",
      "page_number": 42,
      "verbatim_passage": "The Fifth Caspian Summit held in Aktau, Kazakhstan, on August 12, 2018, concluded with the signing of the Convention on the Legal Status of the Caspian Sea after over two decades of negotiations.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_caspian_equation_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "THE CASPIAN EQUATION", "fa": "خزر با سهم مساویِ نامساوی"},
    "clue_text": {
      "en": "From Tehran's national security perspective, the supreme strategic achievement embedded in Article 3 of the 2018 Aktau Convention was this strict military prohibition.",
      "fa": "از منظر امنیت ملی جمهوری اسلامی، بزرگ‌ترین دستاورد راهبردی گنجانده‌شده در اصل سوم کنوانسیون آکتائو ۲۰۱۸ این ممنوعیت نظامی قاطع بود."
    },
    "canonical_answer": {"en": "Ban on Non-Littoral Military Forces", "fa": "ممنوعیت حضور نیروهای نظامی بیگانه"},
    "accepted_aliases": {"en": ["Exclusion of foreign military forces", "Ban on foreign military", "Prohibition of non-Caspian military presence"], "fa": ["ممنوعیت حضور نظامی بیگانگان", "ممنوعیت ورود ارتش‌های خارجی", "ممنوعیت پایگاه‌های خارجی در خزر"]},
    "options": {
      "en": ["Ban on Commercial Container Shipping", "Ban on Non-Littoral Military Forces", "Mandatory Submarine Demilitarization", "Ban on Caviar Harvesting"],
      "fa": ["ممنوعیت حمل کانتینری کالا", "ممنوعیت حضور نیروهای نظامی بیگانه", "خلع سلاح کامل زیردریایی‌ها", "ممنوعیت صید خاویار"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Ban on Commercial Container Shipping", "why_plausible": "Maritime regulation.", "why_wrong": "Commercial shipping is strongly encouraged for the International North-South Transport Corridor (INSTC)."},
      {"option": "Mandatory Submarine Demilitarization", "why_plausible": "An arms control clause.", "why_wrong": "Russia and Iran operate naval warships and sub-surface vessels in the Caspian; only non-littoral forces are banned."},
      {"option": "Ban on Caviar Harvesting", "why_plausible": "An environmental moratorium.", "why_wrong": "Sturgeon moratoria are handled by ecological protocols, not the supreme security clause of the convention."}
    ],
    "adversarial_confusion_set": {"en": ["Pipeline Moratorium", "Demilitarized Neutral Zone"], "fa": ["توقف خط لوله ترانس‌کاسپین", "منطقه کاملاً غیرنظامی"]},
    "specificity_prompt": {
      "en": "Identify the key security clause in the Aktau Convention that barred NATO or external military forces from entering the Caspian.",
      "fa": "مهم‌ترین دستاورد امنیتی ایران و روسیه در کنوانسیون آکتائو مبنی بر جلوگیری از استقرار نظامیان غیرساحلی (مانند ناتو و آمریکا) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ban on Non-Littoral Military Forces. Spot on. Keeping the US Navy and NATO out of the Caspian basin permanently.",
        "wrong_generic": "No, it was the Ban on Non-Littoral Military Forces. Tehran and Moscow's primary geopolitical red line.",
        "common_wrong_answers": {
          "Ban on Commercial Container Shipping": "Commercial shipping is expanding every year on the North-South corridor.",
          "Mandatory Submarine Demilitarization": "Russia tests cruise missiles and warships in the Caspian regularly.",
          "Ban on Caviar Harvesting": "Caviar is fish; this was about keeping American destroyers away."
        }
      },
      "fa": {
        "correct_generic": "ممنوعیت حضور نیروهای نظامی بیگانه. کاملاً درسته! بستن راه ورود ناتو و ناوگان آمریکا به پهنه آبی شمال کشور برای همیشه.",
        "wrong_generic": "خیر، پاسخ ممنوعیت حضور نیروهای نظامی غیرساحلی (بیگانه) بود. خط قرمز مشترک و بنیادین تهران و مسکو در خزر.",
        "common_wrong_answers": {
          "ممنوعیت حمل کانتینری کالا": "تجارت کانتینری در کریدور شمال-جنوب با تمام توان در حال توسعه است.",
          "خلع سلاح کامل زیردریایی‌ها": "روسیه و ایران ناوهای موشک‌انداز در خزر دارند و خلع سلاح نشده‌اند.",
          "ممنوعیت صید خاویار": "حفاظت از خاویار پروتکل زیست‌محیطی جداگانه دارد؛ این ماده یک اصل ژئوپلیتیک نظامی است."
        }
      }
    },
    "explanation": {
      "en": "Article 3, Paragraph 6 of the 2018 Aktau Convention enshrines the principle of the 'non-presence of armed forces not belonging to the Parties in the Caspian Sea', a vital strategic priority for both Tehran and Moscow designed to permanently block NATO and the United States from establishing military bases in Azerbaijan, Turkmenistan, or Kazakhstan.",
      "fa": "بند ۶ اصل سوم کنوانسیون آکتائو تصریح می‌کند که حضور نیروهای مسلح متعلق به کشورهای غیرعضو در دریای خزر ممنوع است؛ این بند اولویت راهبردی درجه اول ایران و روسیه بود تا از استقرار هرگونه پایگاه نظامی ناتو یا آمریکا در سواحل قفقاز و آسیای میانه جلوگیری کند."
    },
    "provenance": {
      "source_book": "The Caspian Sea: A Quest for Environmental Security",
      "source_author": "Asghar Jafari Valdani",
      "page_number": 48,
      "verbatim_passage": "The crucial geopolitical victory for Iran and Russia was Article 3(6) of the Aktau Convention, which strictly prohibited the presence of any military forces belonging to non-littoral states, effectively excluding NATO and the US from the Caspian Sea.",
      "evidence_type": "FACT"
    }
  },

  # 25. single_ration_book: THE RATION BOOK BLUES / کوپن به شرط صف
  {
    "id": "single_ration_book_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {"en": "THE RATION BOOK BLUES", "fa": "کوپن به شرط صف"},
    "clue_text": {
      "en": "Introduced in 1980 to ensure equitable distribution of basic food and fuel during wartime rationing, these paper vouchers became an indispensable part of everyday Iranian life for nearly three decades.",
      "fa": "این برگه‌ها و کالابرگ‌های کاغذی که در سال ۱۳۵۹ برای توزیع عادلانه اقلام اساسی و سوخت در شرایط جنگی عرضه شدند، نزدیک به سه دهه به بخشی جدایی‌ناپذیر از زندگی روزمره مردم ایران بدل گشتند."
    },
    "canonical_answer": {"en": "Ration Coupons", "fa": "کوپن‌های اقتصادی"},
    "accepted_aliases": {"en": ["Coupons", "Koupon", "Ration stamps", "Kalabarg"], "fa": ["کوپن", "کالابرگ", "کوپن‌های ارزاق", "دفترچه کوپن"]},
    "options": {
      "en": ["Stock Options", "Ration Coupons", "Cryptocurrency Tokens", "Bearer Bonds"],
      "fa": ["اوراق قرضه بهادار", "کوپن‌های اقتصادی", "توکن‌های رمزارز", "سهام بورس"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Stock Options", "why_plausible": "Financial paper assets.", "why_wrong": "Stock options are corporate investment instruments, not wartime food rationing vouchers."},
      {"option": "Cryptocurrency Tokens", "why_plausible": "Modern digital vouchers.", "why_wrong": "Cryptocurrency did not exist in the 1980s."},
      {"option": "Bearer Bonds", "why_plausible": "Financial debt certificates.", "why_wrong": "Bearer bonds are treasury investment tools, not municipal food allocation chits."}
    ],
    "adversarial_confusion_set": {"en": ["Food Stamps", "Kalabarg-e Electronik"], "fa": ["کالابرگ الکترونیک", "بن کارمندی"]},
    "specificity_prompt": {
      "en": "Name the paper ration vouchers (Koupon) distributed by the Iranian government throughout the war years.",
      "fa": "اصطلاح عامیانه و رایج فرانسوی‌الاصل برای کالابرگ‌های کاغذی سهمیه‌بندی کالاهای اساسی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Ration Coupons. Correct. Snapping off coupon number 14 with scissors to buy a tub of solidified vegetable ghee.",
        "wrong_generic": "No, it was Ration Coupons (Koupon). The paper currency that fed a nation under siege.",
        "common_wrong_answers": {
          "Stock Options": "Stock options were for Wall Street bankers, not wartime bread queues.",
          "Cryptocurrency Tokens": "Bitcoin was decades in the future.",
          "Bearer Bonds": "Bearer bonds don't buy two kilograms of sugar at the cooperative grocery."
        }
      },
      "fa": {
        "correct_generic": "کوپن‌های اقتصادی. کاملاً درسته! بریدن کوپن شماره ۱۴ با قیچی برای تحویل گرفتن حلب روغن نباتی از بقالی محل.",
        "wrong_generic": "خیر، پاسخ کوپن‌های اقتصادی (کالابرگ) بود. برگه کاغذی حیات‌بخش معیشت خانواده‌ها در دهه شصت.",
        "common_wrong_answers": {
          "اوراق قرضه بهادار": "اوراق بهادار برای سرمایه‌گذاری است، نه دریافت سهمیه تخم‌مرغ و قند.",
          "توکن‌های رمزارز": "رمزارز سه دهه بعد از جنگ متولد شد.",
          "سهام بورس": "بورس در دوران جنگ نیمه‌تعطیل بود."
        }
      }
    },
    "explanation": {
      "en": "Farideh Farhi and socioeconomic historians document that following the outbreak of the Iran-Iraq War and international embargoes, the Islamic Republic established a nationwide coupon rationing system in 1980, ensuring that every household received subsidized rations of flour, sugar, cooking oil, and meat regardless of income.",
      "fa": "فریده فرحی و پژوهشگران تاریخ اقتصادی مستند می‌کنند که با آغاز جنگ و تشدید تحریم‌ها، ستاد بسیج اقتصادی در سال ۱۳۵۹ سیستم کوپن‌دهی سراسری را ایجاد کرد تا اقلام اساسی مانند قند، شکر، روغن نباتی، برنج و صابون با نرخ دولتی میان تمام اقشار توزیع شود."
    },
    "provenance": {
      "source_book": "The Economic Consequences of the Iran-Iraq War",
      "source_author": "Farideh Farhi",
      "page_number": 15,
      "verbatim_passage": "In 1980, the Iranian government launched a nationwide rationing coupon system (koupon) to ensure equitable distribution of foodstuffs and fuel during the war, shielding the vulnerable working class from starvation.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_ration_book_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "THE RATION BOOK BLUES", "fa": "کوپن به شرط صف"},
    "clue_text": {
      "en": "Created within days of the Iraqi invasion in autumn 1980, this powerful executive body managed state procurement, supply chains, and consumer goods allocation across the country.",
      "fa": "این ستاد مقتدر دولتی که در پاییز ۱۳۵۹ بلافاصله پس از تهاجم ارتش عراق تشکیل شد، مدیریت واردات، زنجیره تأمین و سهمیه‌بندی کالاهای مصرفی را در سراسر کشور در دست گرفت."
    },
    "canonical_answer": {"en": "Economic Mobilization Headquarters", "fa": "ستاد بسیج اقتصادی"},
    "accepted_aliases": {"en": ["Setad-e Basij-e Eqtesadi", "Economic Mobilization Committee", "Headquarters for Economic Mobilization"], "fa": ["ستاد بسیج اقتصادی کشور", "بسیج اقتصادی", "شورای بسیج اقتصادی"]},
    "options": {
      "en": ["Privatization Organization", "Economic Mobilization Headquarters", "Stock Exchange Council", "Foreign Investment Bureau"],
      "fa": ["سازمان خصوصی‌سازی", "ستاد بسیج اقتصادی", "شورای عالی بورس", "سازمان سرمایه‌گذاری خارجی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Privatization Organization", "why_plausible": "A major economic agency.", "why_wrong": "The Privatization Organization was founded in 2001 under Khatami to sell state companies, the complete antithesis of wartime state planning."},
      {"option": "Stock Exchange Council", "why_plausible": "Oversees financial markets.", "why_wrong": "Wartime economic administration was socialist and statist, not stock exchange capitalism."},
      {"option": "Foreign Investment Bureau", "why_plausible": "Manages capital inflows.", "why_wrong": "Foreign capital fled Iran during the war; this agency managed domestic ration procurement."}
    ],
    "adversarial_confusion_set": {"en": ["Bonyad-e Mostazafan", "Plan and Budget Organization"], "fa": ["بنیاد مستضعفان", "سازمان برنامه و بودجه"]},
    "specificity_prompt": {
      "en": "Name the specific cabinet-level headquarters created in 1980 that coordinated wartime rationing and logistics.",
      "fa": "نام ستاد عالی دولتی متولی سهمیه‌بندی و مدیریت اقتصاد جنگی در سال ۱۳۵۹ را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Economic Mobilization Headquarters. Correct. Operating like a command economy general staff allocating tons of sugar and barrels of fuel to each province.",
        "wrong_generic": "No, it was the Economic Mobilization Headquarters (Setad-e Basij-e Eqtesadi). The nerve center of wartime statism.",
        "common_wrong_answers": {
          "Privatization Organization": "Privatization is Rafsanjani and Khatami; this was pure state rationing.",
          "Stock Exchange Council": "The stock market was dormant while artillery rained down on Khuzestan.",
          "Foreign Investment Bureau": "No foreign investors were lining up in 1980."
        }
      },
      "fa": {
        "correct_generic": "ستاد بسیج اقتصادی. کاملاً درسته! قرارگاه فرماندهی اقتصاد متمرکز دولتی برای تخصیص تن به تن شکر، برنج و گازوئیل در استان‌ها.",
        "wrong_generic": "خیر، پاسخ ستاد بسیج اقتصادی کشور بود. اتاق فرمان اقتصاد کوپنی در سال‌های جنگ.",
        "common_wrong_answers": {
          "سازمان خصوصی‌سازی": "خصوصی‌سازی متعلق به دهه‌های بعدی است؛ دهه شصت اوج مدیریت دولتی بود.",
          "شورای عالی بورس": "تالار بورس در آن سال‌ها رونقی نداشت.",
          "سازمان سرمایه‌گذاری خارجی": "سرمایه‌گذار خارجی در میانه موشک‌باران به ایران نمی‌آمد."
        }
      }
    },
    "explanation": {
      "en": "Farhi explains that the Economic Mobilization Headquarters (Setad-e Basij-e Eqtesadi) centralized control over all foreign trade, food distribution, and pricing, establishing what became the most comprehensive command-economy apparatus in modern Iranian history.",
      "fa": "فریده فرحی توضیح می‌دهد که ستاد بسیج اقتصادی با متمرکز کردن واردات، توزیع و قیمت‌گذاری کالاها در سراسر کشور، فراگیرترین ساختار اقتصاد دستوری و دولتی را در تاریخ معاصر ایران پایه‌گذاری کرد."
    },
    "provenance": {
      "source_book": "The Economic Consequences of the Iran-Iraq War",
      "source_author": "Farideh Farhi",
      "page_number": 19,
      "verbatim_passage": "Established in October 1980, the Economic Mobilization Headquarters (Setad-e Basij-e Eqtesadi) placed the entire supply chain of consumer staples under strict ministerial supervision to maintain social stability under siege.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_ration_book_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {"en": "THE RATION BOOK BLUES", "fa": "کوپن به شرط صف"},
    "clue_text": {
      "en": "Serving as Prime Minister throughout the entire duration of the war from 1981 to 1989, this politician became the chief champion of statist economic planning and egalitarian price controls.",
      "fa": "این سیاستمدار که در تمام طول جنگ از سال ۱۳۶۰ تا ۱۳۶۸ مقام نخست‌وزیری را بر عهده داشت، نماد اصلی اقتصاد دولتی و عدالت‌خواهانه و تثبیت قیمت‌ها بود."
    },
    "canonical_answer": {"en": "Mir-Hossein Mousavi", "fa": "میرحسین موسوی"},
    "accepted_aliases": {"en": ["Mousavi", "Prime Minister Mousavi", "Mir Hossein Mousavi"], "fa": ["مهندس موسوی", "میر حسین موسوی", "موسوی"]},
    "options": {
      "en": ["Ali Akbar Hashemi Rafsanjani", "Mir-Hossein Mousavi", "Mohammad-Ali Rajai", "Ali Khamenei"],
      "fa": ["علی‌اکبر هاشمی رفسنجانی", "میرحسین موسوی", "محمدعلی رجایی", "علی خامنه‌ای"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Ali Akbar Hashemi Rafsanjani", "why_plausible": "Speaker of Parliament and future president.", "why_wrong": "Rafsanjani was Speaker of Parliament and favored pragmatic post-war market reforms."},
      {"option": "Mohammad-Ali Rajai", "why_plausible": "A pious prime minister.", "why_wrong": "Rajai served briefly as prime minister and president before his tragic assassination in August 1981."},
      {"option": "Ali Khamenei", "why_plausible": "President during the war.", "why_wrong": "Khamenei was President and frequently clashed with Mousavi over economic policy, favoring more bazaar commerce."}
    ],
    "adversarial_confusion_set": {"en": ["Mohsen Noorbakhsh", "Behzad Nabavi"], "fa": ["محسن نوربخش", "بهزاد نبوی"]},
    "specificity_prompt": {
      "en": "Name the wartime Prime Minister of Iran who governed from 1981 until the post was abolished in 1989.",
      "fa": "نام نخست‌وزیر دوران هشت سال دفاع مقدس را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mir-Hossein Mousavi. Correct. Managing an eight-year war on an annual budget of six billion dollars in oil revenue without hyperinflation.",
        "wrong_generic": "No, it was Mir-Hossein Mousavi. The prime minister who made the coupon system work.",
        "common_wrong_answers": {
          "Ali Akbar Hashemi Rafsanjani": "Rafsanjani was in Parliament dreaming of toll highways and malls.",
          "Mohammad-Ali Rajai": "Rajai died in the August 1981 bomb blast.",
          "Ali Khamenei": "Khamenei was President and preferred letting the bazaar trade freely."
        }
      },
      "fa": {
        "correct_generic": "میرحسین موسوی. کاملاً درسته! اداره یک جنگ هشت‌ساله با درآمد نفتی سالانه تنها ۶ تا ۷ میلیارد دلار بدون قحطی و فروپاشی معیشت.",
        "wrong_generic": "خیر، پاسخ میرحسین موسوی بود. نخست‌وزیر دوران جنگ و معمار اقتصاد سهمیه‌بندی شده دولتی.",
        "common_wrong_answers": {
          "علی‌اکبر هاشمی رفسنجانی": "رفسنجانی رئیس مجلس بود و پس از جنگ خصوصی‌سازی را کلید زد.",
          "محمدعلی رجایی": "شهید رجایی در شهریور ۱۳۶۰ ترور شد.",
          "علی خامنه‌ای": "آیت‌الله خامنه‌ای رئیس‌جمهور بود و با تمرکزگرایی افراطی اقتصادی مخالفت داشت."
        }
      }
    },
    "explanation": {
      "en": "Mir-Hossein Mousavi served as Prime Minister of Iran from 1981 to 1989, leading the 'statist left' (Chap-e Sonnati) that relied on price controls, state rationing, and public distribution networks to keep food and medicine affordable despite collapsed oil revenues.",
      "fa": "میرحسین موسوی در طول سال‌های ۱۳۶۰ تا ۱۳۶۸ سکان نخست‌وزیری را در دست داشت و به عنوان رهبر جناح چپ خط امام، با نظارت شدید بر بازار، کنترل قیمت‌ها و توزیع کالابرگی، مانع از بروز قحطی در دوران فشار جنگ شد."
    },
    "provenance": {
      "source_book": "The Economic Consequences of the Iran-Iraq War",
      "source_author": "Farideh Farhi",
      "page_number": 23,
      "verbatim_passage": "Prime Minister Mir-Hossein Mousavi's administration championed a statist economic model, fiercely defending price controls and rationing against conservative bazaar merchants and clerical factions.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_ration_book_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {"en": "THE RATION BOOK BLUES", "fa": "کوپن به شرط صف"},
    "clue_text": {
      "en": "During cold wartime winters, urban families lined up in the snow with metal jerrycans for hours to collect their allocated rations of this liquid fuel, crucial for heating home heaters.",
      "fa": "در زمستان‌های سرد دوران جنگ، خانواده‌های شهری با پیت‌های فلزی ساعت‌ها در صف‌های برفی می‌ایستادند تا سهمیه این سوخت مایع حیاتی برای گرمایش بخاری‌های خانگی را دریافت کنند."
    },
    "canonical_answer": {"en": "Kerosene", "fa": "نفت سفید"},
    "accepted_aliases": {"en": ["Heating oil", "Paraffin", "Naft-e Sefid"], "fa": ["نفت", "نفت خانگی", "نفت بخاری"]},
    "options": {
      "en": ["Natural Gas", "Kerosene", "Aviation Jet Fuel", "Heavy Bunker Fuel"],
      "fa": ["گاز طبیعی لوله‌کشی", "نفت سفید", "سوخت جت هواپیما", "مازوت سنگین"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Natural Gas", "why_plausible": "How Iranian homes are heated today.", "why_wrong": "Widespread urban natural gas pipelines were constructed decades later in the 1990s and 2000s; during the 1980s homes used kerosene space heaters."},
      {"option": "Aviation Jet Fuel", "why_plausible": "A refined kerosene product.", "why_wrong": "Jet fuel was reserved strictly for the Air Force and civil airliners."},
      {"option": "Heavy Bunker Fuel", "why_plausible": "An industrial fuel.", "why_wrong": "Mazut is thick black fuel for power plants, completely unsuitable for residential portable indoor heaters."}
    ],
    "adversarial_confusion_set": {"en": ["Diesel", "Liquid Propane Gas"], "fa": ["گازوئیل", "کپسول گاز مایع"]},
    "specificity_prompt": {
      "en": "Name the specific liquid heating fuel (Naft-e Sefid) carried home in metal cans during 1980s winters.",
      "fa": "نام سوخت مایع بخاری‌های چکه‌ای و والورهای خانگی در دهه شصت (نفت ...) را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Kerosene (Naft-e Sefid). Correct. Standing in the freezing dusk waiting for the horse-drawn oil cart or the local depot to open.",
        "wrong_generic": "No, it was Kerosene (Naft-e Sefid). The scent of Aladdin and Valor heaters in every 1980s living room.",
        "common_wrong_answers": {
          "Natural Gas": "Piped natural gas was a luxury of the late 1990s.",
          "Aviation Jet Fuel": "Jet fuel went into the Phantoms at Mehrabad, not into the living room Valor stove.",
          "Heavy Bunker Fuel": "Bunker fuel is tar for cement factories."
        }
      },
      "fa": {
        "correct_generic": "نفت سفید. کاملاً درسته! ایستادن در صف‌های طولانی با پیت‌های ۲۰ لیتری برای روشن نگه داشتن بخاری‌های علاءالدین و والور.",
        "wrong_generic": "خیر، پاسخ نفت سفید بود. بوی نوستالژیک بخاری‌های نفتی در سوز سرمای زمستان‌های دهه شصت.",
        "common_wrong_answers": {
          "گاز طبیعی لوله‌کشی": "شبکه گاز شهری پروژه دوران سازندگی و اصلاحات بود؛ دهه شصت فقط نفت بود.",
          "سوخت جت هواپیما": "سوخت جت مخصوص پایگاه‌های شکاری بود.",
          "مازوت سنگین": "مازوت قیر سنگین نیروگاه‌هاست."
        }
      }
    },
    "explanation": {
      "en": "Before the nationwide expansion of the urban natural gas grid in the 1990s, virtually all residential home heating relied on kerosene (Naft-e Sefid) burned in Aladdin and Valor space heaters; during wartime fuel refinery disruptions, kerosene rationing was among the most intensely felt aspects of civilian hardship.",
      "fa": "پیش از گازکشی سراسری شهرها در دهه‌های هفتاد و هشتاد، گرمایش خانه‌ها متکی به نفت سفید در بخاری‌های نفتی و والور بود؛ در دوران جنگ به دلیل بمباران پالایشگاه آبادان و تهران، توزیع کوپنی نفت سفید و صف‌های طولانی پیت‌های نفتی از صحنه‌های ماندگار زمستان‌های کشور بود."
    },
    "provenance": {
      "source_book": "The Economic Consequences of the Iran-Iraq War",
      "source_author": "Farideh Farhi",
      "page_number": 27,
      "verbatim_passage": "During the bitter winters of the war, urban households spent hours queuing with twenty-liter jerrycans to receive their allocated rations of kerosene (naft-e sefid), vital for household heating amid severe fuel refining shortages.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_ration_book_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "THE RATION BOOK BLUES", "fa": "کوپن به شرط صف"},
    "clue_text": {
      "en": "Because affluent families did not consume their full flour or sugar allotments while impoverished households needed cash, this thriving informal street trade emerged on city sidewalks, buying and selling unused coupon sheets.",
      "fa": "از آنجا که خانوارهای مرفه تمام سهمیه قند و روغن خود را استفاده نمی‌کردند و اقشار کم‌درآمد به پول نقد نیاز داشتند، این بازار غیررسمی در پیاده‌روهای شهرها برای خرید و فروش برگه‌های کوپن شکل گرفت."
    },
    "canonical_answer": {"en": "Coupon Black Market", "fa": "بازار سیاه کوپن"},
    "accepted_aliases": {"en": ["Black market for coupons", "Bazar-e Siah-e Koupon", "Coupon trading", "Informal coupon market"], "fa": ["بازار سیاه کوپن", "خرید و فروش کوپن", "کوپن‌فروشی", "دلالان کوپن"]},
    "options": {
      "en": ["Real Estate Exchange", "Coupon Black Market", "Government Bond Auction", "Foreign Currency Exchange"],
      "fa": ["بورس املاک و مستغلات", "بازار سیاه کوپن", "حراج اوراق خزانه دولتی", "صرافی رسمی ارز"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Real Estate Exchange", "why_plausible": "Property trading market.", "why_wrong": "Real estate involves formal land titling, not informal trading of paper food coupons on street corners."},
      {"option": "Government Bond Auction", "why_plausible": "An official finance market.", "why_wrong": "State debt auctions are conducted through the Central Bank, not illicit sidewalk trading."},
      {"option": "Foreign Currency Exchange", "why_plausible": "A famous black market in Tehran (Ferdowsi Street).", "why_wrong": "Ferdowsi Street traded US dollars and gold coins; the coupon market traded paper ration chits for rice and butter."}
    ],
    "adversarial_confusion_set": {"en": ["Bazar-e Azad", "Smuggling Network"], "fa": ["بازار آزاد", "شبکه احتکار"]},
    "specificity_prompt": {
      "en": "Name the thriving underground/informal trade where citizens bought and sold state rationing coupons.",
      "fa": "اصطلاح رایج برای دادوستد غیرقانونی و دلال‌بازی برگه‌های کالابرگ در پیاده‌روها را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Coupon Black Market. Spot on. Shouting 'Koupon kharidaram!' (Buying coupons!) on street corners near the cooperative grocers.",
        "wrong_generic": "No, it was the Coupon Black Market (Bazar-e Siah-e Koupon). Where paper state vouchers turned into liquid cash.",
        "common_wrong_answers": {
          "Real Estate Exchange": "Real estate is villas in Shemiran; this was butter coupons on the sidewalk.",
          "Government Bond Auction": "Bonds are for the Central Bank; coupons were sold by teenagers in flip-flops.",
          "Foreign Currency Exchange": "Currency trading was on Ferdowsi Avenue shouting dollar rates."
        }
      },
      "fa": {
        "correct_generic": "بازار سیاه کوپن. کاملاً درسته! فریاد «کوپن خریداریم، کوپن باطله خریداریم» دلالان سر چهارراه‌ها و جلوی فروشگاه‌های قدس و کوروش.",
        "wrong_generic": "خیر، پاسخ بازار سیاه کوپن بود. بازاری موازی که سهمیه‌های استفاده‌نشده روغن و قند را به اسکناس نقد تبدیل می‌کرد.",
        "common_wrong_answers": {
          "بورس املاک و مستغلات": "املاک سند رسمی دارد؛ این بازار کاغذپاره‌های روغن نباتی بود.",
          "حراج اوراق خزانه دولتی": "اوراق خزانه ابزار بدهی بانک مرکزی است.",
          "صرافی رسمی ارز": "صرافی خیابان فردوسی دلار معامله می‌کرد، نه کوپن گوشت و مرغ."
        }
      }
    },
    "explanation": {
      "en": "Farhi notes that despite state criminalization of coupon reselling under anti-hoarding and anti-speculation laws, a massive informal black market flourished across Iranian cities: dealers on street corners bought surplus coupons from upper-class families and resold them to restaurants, bakeries, or poorer households, creating an informal secondary currency.",
      "fa": "فریده فرحی اشاره می‌کند که با وجود جرم‌انگاری تعزیراتی خرید و فروش کوپن، بازار سیاه پررونقی در سراسر شهرها شکل گرفت: دلالان با خرید کوپن‌های مازاد طبقات مرفه و فروش آن به رستوران‌ها، قنادی‌ها و خانوارها، کوپن را به یک شبه‌پول رایج در اقتصاد غیررسمی تبدیل کردند."
    },
    "provenance": {
      "source_book": "The Economic Consequences of the Iran-Iraq War",
      "source_author": "Farideh Farhi",
      "page_number": 31,
      "verbatim_passage": "An active black market for ration coupons emerged in all major cities, where sidewalk brokers bought unused sheets from affluent citizens and resold them to commercial enterprises, circumventing official quotas.",
      "evidence_type": "FACT"
    }
  }
]

batch_c.extend(cats_23_to_25)

with open("/Users/Morad/Spark/build_batch_c.py", "w", encoding="utf-8") as f:
    f.write("batch_c = " + json.dumps(batch_c, ensure_ascii=False, indent=2) + "\n")

print(f"Categories 21 through 25 written! Total clues: {len(batch_c)}")
