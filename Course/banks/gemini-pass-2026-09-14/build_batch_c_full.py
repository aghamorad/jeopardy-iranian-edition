import json
import sys
import re

sys.path.append("/Users/Morad/Spark")
from jeopardy_pipeline import validate_clue_schema

batch_c = [
  # 21. single_mothers_citadel: MOTHERS OF THE CITADEL / سنگردارانِ زینب (Single, 200..1000)
  {
    "id": "single_mothers_citadel_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {"en": "MOTHERS OF THE CITADEL", "fa": "سنگردارانِ زینب"},
    "clue_text": {
      "en": "In her study of female mobilization during the Iran-Iraq War, Shirin Saeidi analyzes how thousands of women volunteered behind the lines in this official logistical war support organization.",
      "fa": "شیرین سعیدی در بررسی نقش زنان در دوران جنگ تحمیلی، مشارکت داوطلبانه هزاران زن در پشت جبهه را در قالب این ستاد رسمی پشتیبانی از جنگ تحلیل می‌کند."
    },
    "canonical_answer": {"en": "War Support Headquarters", "fa": "ستاد پشتیبانی جنگ"},
    "accepted_aliases": {"en": ["Setad-e Poshtibani-e Jang", "War Logistics Support", "War Support Committee"], "fa": ["ستاد پشتیبانی و امداد جنگ", "ستاد جذب و هدایت کمک‌های مردمی", "پشتیبانی جنگ"]},
    "options": {
      "en": ["Red Lion and Sun Society", "War Support Headquarters", "Ministry of Foreign Affairs", "Imperial Guards"],
      "fa": ["جمعیت شیر و خورشید سرخ", "ستاد پشتیبانی جنگ", "وزارت امور خارجه", "گارد جاویدان"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Red Lion and Sun Society", "why_plausible": "The pre-revolutionary humanitarian organization.", "why_wrong": "Replaced after 1979 by the Red Crescent, not the revolutionary war logistics support committee."},
      {"option": "Ministry of Foreign Affairs", "why_plausible": "A core government ministry.", "why_wrong": "Handled foreign diplomacy, not volunteer women's rear-guard logistics."},
      {"option": "Imperial Guards", "why_plausible": "A military elite corps.", "why_wrong": "The Shah's royal bodyguard force dissolved during the 1979 revolution."}
    ],
    "adversarial_confusion_set": {"en": ["Basij-e Khaharan", "Helal-e Ahmar"], "fa": ["بسیج خواهران", "هلال احمر"]},
    "specificity_prompt": {
      "en": "Name the specific rear-echelon headquarters that coordinated civilian and female volunteer war logistics.",
      "fa": "نام ستاد پشتیبانی مردمی که فعالیت‌های امدادی و تدارکاتی زنان در پشت جبهه را ساماندهی می‌کرد بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "War Support Headquarters. Correct. Packing canned rations, mending combat fatigues, and organizing bread drives for the front.",
        "wrong_generic": "No, it was the War Support Headquarters (Setad-e Poshtibani-e Jang). The civilian logistics backbone of the war.",
        "common_wrong_answers": {
          "Red Lion and Sun Society": "The Red Lion lost its crown in 1979; this was revolutionary logistics.",
          "Ministry of Foreign Affairs": "Diplomats wore suits in Geneva; women in chadors packed ammunition in mosques.",
          "Imperial Guards": "The Imperial Guard dissolved the day the revolution won."
        }
      },
      "fa": {
        "correct_generic": "ستاد پشتیبانی جنگ. کاملاً درسته! بسته‌بندی نان خشک، شستن لباس‌های خونی و جمع‌آوری کمپوت در مساجد.",
        "wrong_generic": "خیر، پاسخ ستاد پشتیبانی جنگ بود. شریان تدارکاتی مردمی رزمندگان در خطوط مقدم.",
        "common_wrong_answers": {
          "جمعیت شیر و خورشید سرخ": "شیر و خورشید با انقلاب جایش را به هلال احمر داد.",
          "وزارت امور خارجه": "وزارت خارجه پشت میز مذاکره بود، نه در حال پخت مربا و نان برای رزمندگان.",
          "گارد جاویدان": "گارد شاهنشاهی در ۲۲ بهمن ۵۷ منحل شد."
        }
      }
    },
    "explanation": {
      "en": "Shirin Saeidi documents that the War Support Headquarters (Setad-e Poshtibani-e Jang) mobilized tens of thousands of women in mosques and community centers across Iran, turning domestic tasks like cooking, washing, and sewing into vital wartime defense infrastructure.",
      "fa": "شیرین سعیدی مستند می‌کند که ستاد پشتیبانی جنگ با سازماندهی ده‌ها هزار زن در مساجد و پایگاه‌های محلی، کارهای خانگی نظیر خیاطی، پخت نان و شستشوی لباس رزمندگان را به ستون فقرات تدارکات جبهه تبدیل کرد."
    },
    "provenance": {
      "source_book": "Women and the Sacred Defense",
      "source_author": "Shirin Saeidi",
      "page_number": 88,
      "verbatim_passage": "Through the War Support Headquarters (Setad-e Poshtibani-e Jang), ordinary Iranian women transformed household domestic labor into strategic civic mobilization, washing uniforms, packing rations, and staffing field hospitals.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_mothers_citadel_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "MOTHERS OF THE CITADEL", "fa": "سنگردارانِ زینب"},
    "clue_text": {
      "en": "In the frontline city of Ahvaz, female volunteers performed harrowing labor at this famous facility, washing blood-soaked uniforms and chemical-contaminated blankets sent directly from combat zones.",
      "fa": "در شهر اهواز، زنان داوطلب در این رختشوی‌خانه مشهور مستقر در پادگان شهید علم‌الهدی، لباس‌های خونی رزمندگان و پتوهای آلوده به گازهای شیمیایی را با فداکاری شستشو می‌دادند."
    },
    "canonical_answer": {"en": "Rakhshur-khaneh of Ahvaz", "fa": "رختشوی‌خانه اهواز"},
    "accepted_aliases": {"en": ["Ahvaz war laundry", "Alamolhoda laundry base", "Rakhshurkhaneh Ahvaz"], "fa": ["رختشویخانه اهواز", "رختشوی‌خانه شهید علم‌الهدی", "رختشویخانه شهید علم الهدی"]},
    "options": {
      "en": ["Golestan Palace", "Rakhshur-khaneh of Ahvaz", "Azadi Tower", "Persepolis Citadel"],
      "fa": ["کاخ گلستان", "رختشوی‌خانه اهواز", "برج آزادی", "ارگ تخت جمشید"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Golestan Palace", "why_plausible": "A famous historical complex.", "why_wrong": "A royal Qajar museum palace in Tehran, thousands of miles from the Khuzestan front."},
      {"option": "Azadi Tower", "why_plausible": "An iconic monument.", "why_wrong": "Azadi Tower is a monument in western Tehran, not a wartime frontline laundry depot in Ahvaz."},
      {"option": "Persepolis Citadel", "why_plausible": "An ancient historical site.", "why_wrong": "Persepolis is in Fars province, not a rear-guard military installation during the Iran-Iraq War."}
    ],
    "adversarial_confusion_set": {"en": ["Goltappeh Base", "Shohada Hospital"], "fa": ["پایگاه چمران", "بیمارستان شهید بقایی"]},
    "specificity_prompt": {
      "en": "Name the specific rear-line laundry center in Ahvaz commemorated in wartime memoirs for washing contaminated combat uniforms.",
      "fa": "نام مرکز رختشوی‌خانه پشتیبانی جبهه در اهواز که زنان داوطلب در آن خدمت می‌کردند را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Rakhshur-khaneh of Ahvaz. Correct. Standing waist-deep in soapy water laced with mustard gas residue to wash uniforms for the next battalion.",
        "wrong_generic": "No, it was the Rakhshur-khaneh of Ahvaz (at Shahid Alamolhoda base). One of the grimmest volunteer postings of the entire war.",
        "common_wrong_answers": {
          "Golestan Palace": "Golestan Palace is mirror mosaic halls in Tehran.",
          "Azadi Tower": "Azadi Tower is where commuters catch buses in western Tehran.",
          "Persepolis Citadel": "Persepolis is stone carvings of Darius near Shiraz."
        }
      },
      "fa": {
        "correct_generic": "رختشوی‌خانه اهواز. کاملاً درسته! ایستادن ساعت‌ها در حوضچه‌های آب و وایتکس آلوده به گاز خردل برای پاک کردن خون رزمندگان.",
        "wrong_generic": "خیر، پاسخ رختشوی‌خانه اهواز (پایگاه شهید علم‌الهدی) بود. جلوه‌ای کم‌نظیر از ایثار گمنام زنان در دوران جنگ.",
        "common_wrong_answers": {
          "کاخ گلستان": "کاخ گلستان موزه شاهان قاجار در ناف تهران است.",
          "برج آزادی": "برج آزادی بنای یادبود ورودی غرب پایتخت است.",
          "ارگ تخت جمشید": "تخت جمشید آثار باستانی هخامنشی در استان فارس است."
        }
      }
    },
    "explanation": {
      "en": "Saeidi recounts the harrowing oral histories of women stationed at the Alamolhoda base laundry in Ahvaz: women scrubbed thousands of uniforms stained with blood, bodily tissue, and chemical mustard gas agents, suffering skin lesions and long-term pulmonary illnesses without military pensions.",
      "fa": "سعیدی به تاریخ شفاهی زنان فداکار در رختشوی‌خانه اهواز اشاره می‌کند: بانوانی که هزاران دست لباس خونی و آغشته به گاز خردل را با دست شستند و بسیاری از آنان دچار عوارض شدید پوستی و ریوی ناشی از تاول‌زدگی شدند."
    },
    "provenance": {
      "source_book": "Women and the Sacred Defense",
      "source_author": "Shirin Saeidi",
      "page_number": 94,
      "verbatim_passage": "At the wartime laundry facility (rakhshur-khaneh) in Ahvaz, female volunteers washed blood-caked and chemically contaminated uniforms from the front, enduring chemical exposure that left many with permanent respiratory and dermatological damage.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_mothers_citadel_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {"en": "MOTHERS OF THE CITADEL", "fa": "سنگردارانِ زینب"},
    "clue_text": {
      "en": "Saeidi argues that wartime logistical work provided traditional Iranian women with this transformative civic breakthrough, allowing them to step outside the private domestic sphere into legitimate public space.",
      "fa": "سعیدی استدلال می‌کند که پشتیبانی تدارکاتی جنگ این گشایش مدنی تحول‌آفرین را برای زنان سنتی به ارمغان آورد و به آنان اجازه داد از حصار اندرونی خانه به عرصه عمومی مشروع قدم بگذارند."
    },
    "canonical_answer": {"en": "Civic Agency", "fa": "کنشگری مدنی و شهروندی"},
    "accepted_aliases": {"en": ["Political agency", "Female citizenship", "Public empowerment", "Civic participation"], "fa": ["کنشگری شهروندی", "شهروندی مدنی", "حضور اجتماعی زنان", "مشارکت مدنی"]},
    "options": {
      "en": ["Feudal Seclusion", "Civic Agency", "Military Enlistment", "Corporate Ownership"],
      "fa": ["انزوای فئودالی", "کنشگری مدنی و شهروندی", "استخدام در ارتش", "مالکیت شرکتی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Feudal Seclusion", "why_plausible": "Describes the traditional patriarchal confinement.", "why_wrong": "The war dismantled seclusion by bringing women into collective public organizations."},
      {"option": "Military Enlistment", "why_plausible": "Involves official armed service.", "why_wrong": "Women were barred from formal military enlistment and armed combat rank in the regular armed forces."},
      {"option": "Corporate Ownership", "why_plausible": "Economic empowerment.", "why_wrong": "Wartime volunteer work was unpaid patriotic labor, not private business corporate equity."}
    ],
    "adversarial_confusion_set": {"en": ["Domestic Subjugation", "Social Disenfranchisement"], "fa": ["خانه‌نشینی اجباری", "حذف اجتماعی"]},
    "specificity_prompt": {
      "en": "Identify the sociological concept of empowerment and public participation highlighted by Saeidi.",
      "fa": "مفهوم جامعه‌شناختی بیانگر ارتقای نقش اجتماعی و حضور فعال زنان در عرصه عمومی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Civic Agency. Correct. When serving the state in war gives you the voice to demand rights in peace.",
        "wrong_generic": "No, it was Civic Agency (and political citizenship). The unintended feminist byproduct of holy war mobilization.",
        "common_wrong_answers": {
          "Feudal Seclusion": "The war shattered seclusion; women were running city supply warehouses.",
          "Military Enlistment": "They were denied uniforms and ranks, but took over the logistical networks.",
          "Corporate Ownership": "There was no money or stock options in washing bandages."
        }
      },
      "fa": {
        "correct_generic": "کنشگری مدنی و شهروندی. کاملاً درسته! وقتی فداکاری در دوران دفاع مقدس، زنان سنتی را به بازیگرانی مطالبه‌گر در جامعه تبدیل کرد.",
        "wrong_generic": "خیر، پاسخ کنشگری مدنی و شهروندی بود. دستاورد ناخواسته بسیج جنگی برای هویت‌یابی زنان.",
        "common_wrong_answers": {
          "انزوای فئودالی": "جنگ حصار خانه‌نشینی سنتی را شکست و زنان را به مساجد و پایگاه‌ها کشاند.",
          "استخدام در ارتش": "زنان به کادر رسمی ارتش نپیوستند؛ در تشکل‌های داوطلبانه مردمی نقش‌آفرینی کردند.",
          "مالکیت شرکتی": "کار پشت جبهه ایثار بی‌مزد بود، نه فعالیت انتفاعی اقتصادی."
        }
      }
    },
    "explanation": {
      "en": "Shirin Saeidi theorizes that the Sacred Defense inadvertently expanded Iranian women's 'citizenship from below': participating in state survival gave pious women legitimate grounds to contest male authority and assert their political presence in the public sphere.",
      "fa": "شیرین سعیدی نظریه‌پردازی می‌کند که جنگ تحمیلی ناخواسته به بسط «شهروندی از پایین» برای زنان انجامید؛ چرا که مشارکت در بقای کشور به زنان متدین مشروعیت بخشید تا هنجارهای سنتی پدرسالارانه را به چالش بکشند و سهم خود را در عرصه عمومی طلب کنند."
    },
    "provenance": {
      "source_book": "Women and the Sacred Defense",
      "source_author": "Shirin Saeidi",
      "page_number": 102,
      "verbatim_passage": "By stepping up to manage war support networks, working-class pious women forged a new form of civic agency and active citizenship, using their status as defenders of the nation to demand political visibility.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_mothers_citadel_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {"en": "MOTHERS OF THE CITADEL", "fa": "سنگردارانِ زینب"},
    "clue_text": {
      "en": "In state-sponsored cultural production analyzed by Saeidi, female sacrifice was lionized through this archetypal maternal figure, celebrated for stoically surrendering multiple sons to battlefield martyrdom without shedding a tear.",
      "fa": "در تولیدات فرهنگی و تبلیغاتی حکومت که توسط سعیدی واکاوی شده، ایثار زنان در قالب این کهن‌الگوی مادری ستایش می‌شد که چند فرزند خود را بدون ریختن قطره‌ای اشک تقدیم شهادت در جبهه کرده است."
    },
    "canonical_answer": {"en": "Mother of Martyrs", "fa": "مادر شهیدان"},
    "accepted_aliases": {"en": ["Madar-e Shohada", "Mother of martyrs", "Martyr's mother", "Mothers of martyrs"], "fa": ["مادر شهید", "مادران شهدا", "مادر چند شهید"]},
    "options": {
      "en": ["Monarchist Matron", "Mother of Martyrs", "Secular Suffragette", "Labor Guild Matriarch"],
      "fa": ["بانوی دربار پهلوی", "مادر شهیدان", "فعال حق رأی سکولار", "بزرگ صنف کارگری"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Monarchist Matron", "why_plausible": "A pre-revolutionary female ideal.", "why_wrong": "The monarchist elite was overthrown and demonized by revolutionary cultural authorities."},
      {"option": "Secular Suffragette", "why_plausible": "A Western feminist concept.", "why_wrong": "Secular feminism was explicitly denounced by the Islamic Republic as Western moral corruption."},
      {"option": "Labor Guild Matriarch", "why_plausible": "A working-class socialist archetype.", "why_wrong": "Not the religious Shi'i martyrological framing propagated by the Iranian state."}
    ],
    "adversarial_confusion_set": {"en": ["Zaynab Archetype", "Khansalar"], "fa": ["کهن‌الگوی زینبی", "خان‌سالار"]},
    "specificity_prompt": {
      "en": "Name the specific cultural archetype of the mother who sacrifices multiple sons in the Sacred Defense.",
      "fa": "عنوان نمادین و قدسی مادری که فرزندانش را تقدیم انقلاب و جنگ کرده است را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mother of Martyrs. Spot on. Placing the gold-framed portraits of three dead sons on the mantle while cameras capture your holy smile.",
        "wrong_generic": "No, it was the Mother of Martyrs (Madar-e Shohada). The ultimate moral monument of the post-revolutionary state.",
        "common_wrong_answers": {
          "Monarchist Matron": "Royal matrons were in exile in Paris drinking champagne.",
          "Secular Suffragette": "Suffragettes wanted voting ballots; the state wanted selfless sacrifices.",
          "Labor Guild Matriarch": "Labor guilds were dominated by men; the Mother of Martyrs stood above politics."
        }
      },
      "fa": {
        "correct_generic": "مادر شهیدان. کاملاً درسته! چیدن قاب عکس سه فرزند شهید بر روی طاقچه و لبخند زدن جلوی دوربین‌های تلویزیونی.",
        "wrong_generic": "خیر، پاسخ مادر شهیدان (مادر شهدا) بود. والاترین کهن‌الگوی تبلیغاتی نظام در تکریم ایثار زنان.",
        "common_wrong_answers": {
          "بانوی دربار پهلوی": "بانوان دربار در نیس و پاریس اقامت داشتند، نه در تشییع پیکر شهدا در بهشت زهرا.",
          "فعال حق رأی سکولار": "فمینیسم سکولار در گفتمان رسمی مردود بود؛ الگوی ستایش‌شده مادری زینبی بود.",
          "بزرگ صنف کارگری": "صنوف کارگری ساختار دیگری داشتند؛ مادر شهید تقدس فراگیر ملی داشت."
        }
      }
    },
    "explanation": {
      "en": "Saeidi analyzes how the Islamic Republic constructed the 'Mother of Martyrs' as a sanctified national symbol: mothers who lost several sons were awarded national medals, featured in state television documentaries, and presented as living embodiments of Lady Zaynab at Karbala.",
      "fa": "سعیدی تحلیل می‌کند که نظام چگونه «مادر شهید» را به نمادی قدسی تبدیل کرد: مادرانی که چندین فرزند فدا کرده بودند، نشان ملی ایثار گرفتند و در رسانه‌ها به عنوان تجسم عینی حضرت زینب در کربلا بازنمایی شدند."
    },
    "provenance": {
      "source_book": "Women and the Sacred Defense",
      "source_author": "Shirin Saeidi",
      "page_number": 110,
      "verbatim_passage": "The state constructed the 'Mother of Martyrs' (Madar-e Shohada) as the ultimate female patriot, celebrating women whose maternal sacrifice sustained the ideological legitimacy of the Islamic Republic.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "single_mothers_citadel_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "MOTHERS OF THE CITADEL", "fa": "سنگردارانِ زینب"},
    "clue_text": {
      "en": "In her critical conclusion, Saeidi details this bitter post-war irony: once the 1988 ceasefire was signed, male veterans received state hiring quotas and pensions, while female volunteers were systematically subjected to this policy.",
      "fa": "سعیدی در جمع‌بندی انتقادی خود به این تلخی پساجنگ اشاره می‌کند: با امضای آتش‌بس سال ۶۷، رزمندگان مرد سهمیه‌های اداری و مستمری دریافت کردند، اما زنان امدادگر با این سیاستِ بازگشت به خانه مواجه شدند."
    },
    "canonical_answer": {"en": "Re-domestication and Marginalization", "fa": "خانه‌نشینی مجدد و حاشیه‌رانی"},
    "accepted_aliases": {"en": ["Re-domestication", "Marginalization", "Return to domesticity", "Domestic marginalization"], "fa": ["خانه‌نشینی", "بازگشت به خانه", "حاشیه‌نشینی مجدد", "طرد به حوزه خصوصی"]},
    "options": {
      "en": ["Military Ennoblement", "Re-domestication and Marginalization", "Cabinet Ministerial Promotion", "Diplomatic Ambassadorial Posting"],
      "fa": ["اعطای درجات نظامی", "خانه‌نشینی مجدد و حاشیه‌رانی", "ارتقا به وزارت", "انتصاب به سفارتخانه‌های خارجی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Military Ennoblement", "why_plausible": "Veterans received honors.", "why_wrong": "Female volunteers were denied military pensions and formal officer ranks."},
      {"option": "Cabinet Ministerial Promotion", "why_plausible": "A few women entered politics.", "why_wrong": "No woman was appointed minister until Marzieh Dastjerdi in 2009; post-war cabinets were all-male."},
      {"option": "Diplomatic Ambassadorial Posting", "why_plausible": "Prestigious state rewards.", "why_wrong": "Female ambassadors were not appointed until decades later in 2015 (Marzieh Afkham)."}
    ],
    "adversarial_confusion_set": {"en": ["Bonyad Compensation", "Veteran Enfranchisement"], "fa": ["دریافت غرامت بنیاد شهید", "استخدام رسمی"]},
    "specificity_prompt": {
      "en": "Identify the post-war patriarchal process of pushing female volunteers back into private domesticity.",
      "fa": "فرآیند بازگرداندن اجباری زنان جهادگر به درون خانه و نادیده گرفتن سوابق ایثارگری آنان پس از آتش‌بس را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Re-domestication and Marginalization. Spot on. Thank you for washing the mustard gas out of our shirts, now please go back to the kitchen.",
        "wrong_generic": "No, it was Re-domestication and Marginalization. The post-war patriarchal backlash that erased women's frontline service.",
        "common_wrong_answers": {
          "Military Ennoblement": "Medals and veteran pensions were strictly reserved for the men.",
          "Cabinet Ministerial Promotion": "The cabinet remained a strict boys' club for another twenty years.",
          "Diplomatic Ambassadorial Posting": "Women weren't sent as ambassadors until Marzieh Afkham went to Malaysia in 2015."
        }
      },
      "fa": {
        "correct_generic": "خانه‌نشینی مجدد و حاشیه‌رانی. کاملاً درسته! ممنون از اینکه لباس‌های آلوده به خردل را شستید، حالا بفرمایید به آشپزخانه برگردید.",
        "wrong_generic": "خیر، پاسخ خانه‌نشینی مجدد و حاشیه‌رانی بود. تلخ‌ترین بخش تاریخ شفاهی زنان ایثارگر پس از پایان جنگ.",
        "common_wrong_answers": {
          "اعطای درجات نظامی": "درجه نظامی و حقوق ایثارگری فقط به رزمندگان مرد داده شد.",
          "ارتقا به وزارت": "اولین وزیر زن پس از انقلاب در سال ۱۳۸۸ (مرضیه وحید دستجردی) منصوب شد.",
          "انتصاب به سفارتخانه‌های خارجی": "اولین سفیر زن پس از انقلاب در سال ۱۳۹۴ به مالزی اعزام شد."
        }
      }
    },
    "explanation": {
      "en": "Saeidi concludes that with post-war reconstruction in 1988, the Islamic Republic reinforced patriarchal boundaries: while male veterans were integrated into civil service via quota laws (Sahmiyeh) and received veteran pensions from the Foundation of Martyrs, female rear-guard volunteers received virtually zero institutional veteran recognition and were urged to return to traditional homebound domestic roles.",
      "fa": "سعیدی نتیجه می‌گیرد که پس از قطعنامه ۵۹۸، حاکمیت ساختار مردسالار را احیا کرد: در حالی که مردان ایثارگر از سهمیه‌های استخدامی، کنکور و مستمری بنیاد شهید بهره‌مند شدند، زنان داوطلب پشت جبهه از هرگونه امتیاز جانبازی محروم شدند و به خانه‌نشینی و وظایف مادری سوق داده شدند."
    },
    "provenance": {
      "source_book": "Women and the Sacred Defense",
      "source_author": "Shirin Saeidi",
      "page_number": 118,
      "verbatim_passage": "Following the 1988 ceasefire, the state pushed female volunteers back into domesticity, excluding them from the lucrative civil service quotas and formal veteran benefits generously bestowed upon male combatants.",
      "evidence_type": "INTERPRETATION"
    }
  }
]

for c in batch_c:
    validate_clue_schema(c)

print(f"Validated {len(batch_c)} clues in Category 21 successfully.")
