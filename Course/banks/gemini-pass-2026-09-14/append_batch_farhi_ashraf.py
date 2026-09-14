import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/Morad/Spark")
from jeopardy_pipeline import validate_clue_schema, append_validated_clues

clues = [
  # CATEGORY 1: Single Jeopardy (Ashraf: Oil Strikes)
  {
    "id": "single_oil_strikes_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "CRUDE AWAKENINGS",
      "fa": "شیرِ نفت در دست کارگر"
    },
    "clue_text": {
      "en": "In mid-October 1978, workers in this vital industrial sector launched a nationwide walkout, shutting down refinery production and cutting off over 80 percent of the Pahlavi state's foreign exchange earnings.",
      "fa": "در اواسط مهر ۱۳۵۷، کارگران این بخش حیاتی صنعت با اعتصابی سراسری پالایشگاه‌ها را فلج کردند و بیش از هشتاد درصد از درآمدهای ارزی رژیم پهلوی را قطع نمودند."
    },
    "canonical_answer": {
      "en": "Oil industry",
      "fa": "صنعت نفت"
    },
    "accepted_aliases": {
      "en": ["Petroleum industry", "Iranian oil sector", "NIOC", "National Iranian Oil Company"],
      "fa": ["شرکت ملی نفت ایران", "نفت", "پالایشگاه‌های نفت"]
    },
    "options": {
      "en": ["Oil industry", "Automotive industry", "Textile industry", "Railway sector"],
      "fa": ["صنعت نفت", "صنعت خودروسازی", "صنعت نساجی", "راه‌آهن سراسری"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Automotive industry",
        "why_plausible": "Iran National and vehicle assembly plants engaged in major strikes in late 1978.",
        "why_wrong": "The auto sector catered to domestic passenger transit, not supplying 80% of state foreign exchange reserves."
      },
      {
        "option": "Textile industry",
        "why_plausible": "Isfahan and Yazd textile mills had historic labor union traditions.",
        "why_wrong": "Textile manufacturing was domestically oriented and had nowhere near the macroeconomic leverage of oil."
      },
      {
        "option": "Railway sector",
        "why_plausible": "National railway employees organized transport strikes that halted freight.",
        "why_wrong": "Rail freight disruptions choked inland transit, but did not starve the treasury of petroleum petrodollars."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Copper mining", "Steel manufacturing"],
      "fa": ["صنعت مس", "صنایع فولاد"]
    },
    "specificity_prompt": {
      "en": "Please identify the specific natural resource sector that halted production.",
      "fa": "لطفاً بخش دقیق منبع طبیعی متوقف‌شده را نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Oil industry. Spot on. You actually know which tap choked the Shah's treasury.",
        "wrong_generic": "No. The answer was the oil industry. Check your economic history.",
        "common_wrong_answers": {
          "Automotive industry": "Cars were Paykans; oil was the money.",
          "Textile industry": "Textiles spun cotton, not foreign exchange.",
          "Railway sector": "Trains carried grain; oil financed the state."
        }
      },
      "fa": {
        "correct_generic": "صنعت نفت. کاملاً درسته! بالاخره فهمیدید کدام شیر آب مالیات و دلار شاه را بست.",
        "wrong_generic": "خیر، پاسخ درست صنعت نفت بود. الفبای اقتصاد سیاسی انقلاب را نخوانده‌اید.",
        "common_wrong_answers": {
          "صنعت خودروسازی": "ایران ناسیونال پیکان مونتاژ می‌کرد، دلار نفتی نمی‌آورد.",
          "صنعت نساجی": "نساجی پارچه می‌بافت، ارز خارجی کشور را تأمین نمی‌کرد.",
          "راه‌آهن سراسری": "راه‌آهن بار جابه‌جا می‌کرد، خزانه رژیم با نفت پر می‌شد."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi note that the oil refinery strikes in October 1978 marked the fourth stage of the revolution, depriving the Pahlavi regime of its critical fiscal lifeline and triggering acute domestic fuel shortages.",
      "fa": "احمد اشرف و علی بنوعزیزی نشان می‌دهند که اعتصاب کارکنان صنعت نفت در مهر ۱۳۵۷ با خشکاندن درآمدهای ارزی و ایجاد بحران سوخت، نقطه عطف مرحله چهارم انقلاب را رقم زد."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 12,
      "verbatim_passage": "A decisive turning point in the fourth stage was the strike in the oil industry in mid-October... It cut off the state's main source of revenues and foreign exchange earnings, which accounted for over 80 percent of the total.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_oil_strikes_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "CRUDE AWAKENINGS",
      "fa": "شیرِ نفت در دست کارگر"
    },
    "clue_text": {
      "en": "Appointed prime minister by the Shah on November 6, 1978 to restore order, this joint chiefs general threatened striking oil workers with summary dismissal and temporarily arrested roughly 200 strike organizers.",
      "fa": "این ارتشبد ارتش شاهنشاهی که در ۱۵ آبان ۱۳۵۷ به نخست‌وزیری دولت نظامی منصوب شد، کارگران اعتصابی نفت را به اخراج تهدید کرد و نزدیک به دویست نفر از سازمان‌دهندگان اعتصاب را به بازداشت کشاند."
    },
    "canonical_answer": {
      "en": "Gholam-Reza Azhari",
      "fa": "غلامرضا ازهاری"
    },
    "accepted_aliases": {
      "en": ["General Azhari", "Gholam Reza Azhari", "Arteshbod Azhari"],
      "fa": ["ارتشبد ازهاری", "تیمسار ازهاری", "غلام‌رضا ازهاری"]
    },
    "options": {
      "en": ["Gholam-Reza Azhari", "Jafar Sharif-Emami", "Gholam-Ali Oveisi", "Shapour Bakhtiar"],
      "fa": ["غلامرضا ازهاری", "جعفر شریف‌امامی", "غلامعلی اویسی", "شاپور بختیار"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Jafar Sharif-Emami",
        "why_plausible": "He preceded Azhari as prime minister during the 'government of national reconciliation' in autumn 1978.",
        "why_wrong": "He headed a civilian reconciliation cabinet from August to November 1978, resigning after 'Black Friday' and the university clashes."
      },
      {
        "option": "Gholam-Ali Oveisi",
        "why_plausible": "The hardline military governor of Tehran responsible for imposing martial law on Black Friday.",
        "why_wrong": "He served as military governor of Tehran and armed forces commander, never appointed prime minister."
      },
      {
        "option": "Shapour Bakhtiar",
        "why_plausible": "The final prime minister appointed by the Shah in January 1979 before the revolution's victory.",
        "why_wrong": "Bakhtiar was a civilian National Front leader who headed the cabinet in January-February 1979, succeeding Azhari."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Abbas Gharabaghi", "Nasser Moghaddam"],
      "fa": ["عباس قره‌باغی", "ناصر مقدم"]
    },
    "specificity_prompt": {
      "en": "Please specify the full regnal name of the general who headed the military cabinet in November 1978.",
      "fa": "لطفاً نام و نام خانوادگی ارتشبدی را که در آبان ۱۳۵۷ مأمور تشکیل کابینه نظامی شد ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Gholam-Reza Azhari. Correct. The military general who thought loudspeakers were tape recorders.",
        "wrong_generic": "Wrong. We were looking for General Gholam-Reza Azhari.",
        "common_wrong_answers": {
          "Jafar Sharif-Emami": "Sharif-Emami resigned before the military cabinet was installed.",
          "Gholam-Ali Oveisi": "Oveisi was military governor of Tehran, not the prime minister.",
          "Shapour Bakhtiar": "Bakhtiar was the civilian appointed in January 1979 after Azhari stroked out."
        }
      },
      "fa": {
        "correct_generic": "غلامرضا ازهاری. کاملاً درسته! همان نظامی که شعارهای شبانه مردم روی پشت‌بام‌ها را نوار ضبط‌شده می‌دانست.",
        "wrong_generic": "خیر، نخست‌وزیر دولت نظامی غلامرضا ازهاری بود. وزرای پهلوی را از نو بشمارید.",
        "common_wrong_answers": {
          "جعفر شریف‌امامی": "شریف‌امامی دولت آشتی ملی داشت و قبل از ازهاری سقوط کرد.",
          "غلامعلی اویسی": "اویسی فرماندار نظامی تهران بود، نه نخست‌وزیر کابینه نظامی.",
          "شاپور بختیار": "بختیار رهبر جبهه ملی بود که در دی‌ماه جای ازهاری آمد."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi explain that after Sharif-Emami's government fell, the Shah appointed General G.R. Azhari to head a military government, attempting coercion against oil workers before vacillating into political concessions.",
      "fa": "احمد اشرف و علی بنوعزیزی شرح می‌دهند که شاه پس از ناکامی شریف‌امامی، ارتشبد غلامرضا ازهاری را مأمور سرکوب اعتصابات نفتی کرد، اما تزلزل در اعمال زور مانع مهار قیام شد."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 12,
      "verbatim_passage": "G.R. Azhari, the head of the joint chiefs, to replace Sharif-Emami as prime minister. Martial law and censorship of the press were imposed again by the new military government. The military government threatened the oil workers with dismissal if they did not return to work immediately.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_oil_strikes_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "CRUDE AWAKENINGS",
      "fa": "شیرِ نفت در دست کارگر"
    },
    "clue_text": {
      "en": "Under the brief resumption enforced by martial law threats in mid-November 1978, Iranian oil output briefly touched this historic near-peak volume of millions of barrels per day before plunging to zero for exports.",
      "fa": "در پی تهدیدهای حکومت نظامی در اواسط آبان ۱۳۵۷، تولید روزانه نفت ایران برای مدت کوتاهی به این اوج تاریخی چند میلیون بشکه‌ای نزدیک شد، پیش از آنکه با موج مجدد اعتصابات صادرات آن به صفر برسد."
    },
    "canonical_answer": {
      "en": "5.8 million barrels per day",
      "fa": "پنج و هشت دهم میلیون بشکه در روز"
    },
    "accepted_aliases": {
      "en": ["5.8 million barrels", "5.8 million bpd", "5.8 mbpd", "5.8 million"],
      "fa": ["۵٫۸ میلیون بشکه", "۵٫۸ میلیون بشکه در روز", "پنج ممیز هشت میلیون بشکه"]
    },
    "options": {
      "en": ["5.8 million barrels per day", "3.2 million barrels per day", "7.5 million barrels per day", "4.1 million barrels per day"],
      "fa": ["پنج و هشت دهم میلیون بشکه در روز", "سه و دو دهم میلیون بشکه در روز", "هفت و نیم میلیون بشکه در روز", "چهار و یک دهم میلیون بشکه در روز"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "3.2 million barrels per day",
        "why_plausible": "A common intermediate production average during partial strike slowdowns.",
        "why_wrong": "The pre-strike capacity under Azhari briefly rebounded to 5.8 million barrels per day."
      },
      {
        "option": "7.5 million barrels per day",
        "why_plausible": "The Shah's unrealized ambitious target planned in early 1970s OPEC projections.",
        "why_wrong": "Iran never reached 7.5 million barrels per day; maximum output plateaued below 6 million."
      },
      {
        "option": "4.1 million barrels per day",
        "why_plausible": "Represents typical post-revolutionary production targets under the Islamic Republic.",
        "why_wrong": "Under Azhari's immediate threats, production rebounded to 5.8 million barrels per day before collapsing."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["6 million bpd", "1 million bpd"],
      "fa": ["شش میلیون بشکه", "یک میلیون بشکه"]
    },
    "specificity_prompt": {
      "en": "Please state the exact numerical rate in millions of barrels per day documented by Ashraf.",
      "fa": "لطفاً رقم دقیق تولید روزانه نفت بر حسب میلیون بشکه را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "5.8 million barrels per day. Right. You actually retained a precise economic statistic.",
        "wrong_generic": "No. The figure was 5.8 million barrels per day. Guessing numbers is not a strategy.",
        "common_wrong_answers": {
          "3.2 million barrels per day": "3.2 million was a slump figure, not the pre-strike peak.",
          "7.5 million barrels per day": "7.5 million was the Shah's fantasy, not Iranian reality.",
          "4.1 million barrels per day": "4.1 million is modern post-war numbers. Check the 1978 data."
        }
      },
      "fa": {
        "correct_generic": "پنج و هشت دهم میلیون بشکه در روز. کاملاً درسته! بالاخره یک آمار عددی دقیق را از خود درنیاوردید.",
        "wrong_generic": "خیر، پاسخ درست پنج و هشت دهم میلیون بشکه در روز بود. آمارها شوخی‌بردار نیستند.",
        "common_wrong_answers": {
          "سه و دو دهم میلیون بشکه در روز": "سه و دو دهم میلیون آمار افت مقطعی بود، نه سقف تولید.",
          "هفت و نیم میلیون بشکه در روز": "هفت و نیم میلیون آرزوی بلندپروازانه شاه بود که هرگز محقق نشد.",
          "چهار و یک دهم میلیون بشکه در روز": "چهار و یک دهم مربوط به دوران پس از انقلاب است؛ تاریخ نفت را بخوانید."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi record that under Azhari's military ultimatum, oil workers briefly returned to work, pushing output to 5.8 million barrels per day, before renewing the strike that halted exports completely.",
      "fa": "احمد اشرف ثبت کرده است که کارگران در پی اخطار ارتشبد ازهاری موقتاً تولید را به ۵٫۸ میلیون بشکه رساندند، اما بلافاصله با از سرگیری اعتصاب، صادرات نفت به کلی متوقف گردید."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 12,
      "verbatim_passage": "The military government threatened the oil workers with dismissal if they did not return to work immediately. Most of them did return, and oil output soon rose to 5.8 million barrels per day, a level close to the highest production peaks achieved by the industry in recent years.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_oil_strikes_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "CRUDE AWAKENINGS",
      "fa": "شیرِ نفت در دست کارگر"
    },
    "clue_text": {
      "en": "Formed by Ayatollah Khomeini on December 29, 1978, this five-member body chaired by Mehdi Bazargan negotiated with striking oil workers in Khuzestan to produce petroleum strictly for domestic heating while blocking all exports.",
      "fa": "این هیئت پنج‌نفره که در ۸ دی ۱۳۵۷ به فرمان آیت‌الله خمینی و ریاست مهدی بازرگان تشکیل شد، با کارگران اعتصابی نفت در خوزستان مذاکره کرد تا صرفاً به میزان مصرف گرمایشی مردم سوخت تولید شود و صادرات خارجی مسدود بماند."
    },
    "canonical_answer": {
      "en": "Central Strike Committee",
      "fa": "هیئت تنظیم اعتصابات"
    },
    "accepted_aliases": {
      "en": ["Strike Regulation Committee", "Hey'at-e Tanzim-e E'tesabat", "Strike Coordination Committee", "Bazargan Strike Committee"],
      "fa": ["کمیته تنظیم اعتصابات", "هیئت تنظیم اعتصابات سراسری", "کمیته اعتصابات بازرگان"]
    },
    "options": {
      "en": ["Central Strike Committee", "Revolutionary Council", "Tehran Neighborhood Komiteh", "Society of Militant Clergy"],
      "fa": ["هیئت تنظیم اعتصابات", "شورای انقلاب اسلامی", "کمیته‌های محلات تهران", "جامعه روحانیت مبارز"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Revolutionary Council",
        "why_plausible": "The clandestine supreme political body established by Khomeini in January 1979.",
        "why_wrong": "The Revolutionary Council supervised the overall transition, whereas the Central Strike Committee was a specialized body sent to the oil fields."
      },
      {
        "option": "Tehran Neighborhood Komiteh",
        "why_plausible": "Local grass-roots armed groups maintaining order and rationing fuel in the capital.",
        "why_wrong": "Neighborhood committees distributed rations locally, but did not negotiate oil production quotas with refinery workers."
      },
      {
        "option": "Society of Militant Clergy",
        "why_plausible": "The main network of pro-Khomeini clerics coordinating public demonstrations in Tehran.",
        "why_wrong": "A political-religious clerical association, not the specialized commission managing winter energy extraction."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Worker Shura of Abadan", "Special Commission for Oil"],
      "fa": ["شورای کارگران آبادان", "کمیسیون ویژه نفت"]
    },
    "specificity_prompt": {
      "en": "Please state the official name of the committee formed by Khomeini to manage nationwide strikes.",
      "fa": "لطفاً عنوان رسمی این هیئت منتخب امام خمینی برای مدیریت اعتصابات را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Central Strike Committee. Quite right. The dual power that rationed winter kerosene.",
        "wrong_generic": "No. It was the Central Strike Committee (Hey'at-e Tanzim-e E'tesabat).",
        "common_wrong_answers": {
          "Revolutionary Council": "The Revolutionary Council was the shadow government; this was the strike steering committee.",
          "Tehran Neighborhood Komiteh": "Neighborhood committees guarded street barricades, not refinery valves.",
          "Society of Militant Clergy": "The clerics gave speeches; Bazargan's team negotiated barrel quotas."
        }
      },
      "fa": {
        "correct_generic": "هیئت تنظیم اعتصابات. کاملاً درسته! نهاد حاکمیت دوگانه‌ای که نفت سفید چراغ‌های زمستان ۵۷ را سهمیه‌بندی کرد.",
        "wrong_generic": "خیر، پاسخ درست هیئت تنظیم اعتصابات بود. اسناد تشکیل دولت موقت را بازخوانی کنید.",
        "common_wrong_answers": {
          "شورای انقلاب اسلامی": "شورای انقلاب نهاد بالادستی کل کشور بود، نه هیئت تخصصی مدیریت پالایشگاه‌ها.",
          "کمیته‌های محلات تهران": "کمیته‌های محلات امنیت کوچه را تأمین می‌کردند، نه چاه‌های نفت جنوب را.",
          "جامعه روحانیت مبارز": "روحانیت مبارز بیانیه صادر می‌کرد، بازرگان با تکنسین‌های نفت مذاکره می‌کرد."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi explain that the establishment of the Central Strike Committee under Bazargan was a hallmark of dual sovereignty, ensuring that striking workers extracted only enough fuel for domestic needs while bleeding the Pahlavi state.",
      "fa": "احمد اشرف تشریح می‌کند که اعزام هیئت تنظیم اعتصابات به ریاست بازرگان به خوزستان نماد حاکمیت دوگانه بود؛ کارگران با اذن مذهبی صرفاً برای مصرف داخلی شیرها را باز کردند تا شاه بی‌پول بماند."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 14,
      "verbatim_passage": "There were three principal moments of transition of state power from the incumbents to the contenders: (1) the establishment of local Islamic revolutionary committees and a central committee to supervise nationwide strikes; (2) the formation by Khomeini of a Council of the Islamic Revolution; and (3) Khomeini's return from exile.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_oil_strikes_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "CRUDE AWAKENINGS",
      "fa": "شیرِ نفت در دست کارگر"
    },
    "clue_text": {
      "en": "In Ashraf and Banuazizi's quantitative dataset analyzing the 1,195 mass strikes during the revolution, while schools and bazaars mounted nearly half, this exact proportion—almost two-fifths—occurred inside state agencies and public-sector institutions.",
      "fa": "در داده‌های آماری اشرف و بنوعزیزی از مجموع ۱۱۹۵ اعتصاب عمومی دوران انقلاب، در حالی که مدارس و بازاریان نزدیک به نیمی از آن را برپا کردند، تقریباً این نسبت دقیق (دو پنجم) در درون ادارات دولتی و نهادهای بخش عمومی به وقوع پیوست."
    },
    "canonical_answer": {
      "en": "Almost two-fifths",
      "fa": "تقریباً دو پنجم"
    },
    "accepted_aliases": {
      "en": ["Two-fifths", "About 40 percent", "40%", "Two fifths"],
      "fa": ["دو پنجم", "حدود چهل درصد", "۴۰ درصد", "دو پنجم اعتصابات"]
    },
    "options": {
      "en": ["Almost two-fifths", "One-tenth", "Over three-quarters", "Less than five percent"],
      "fa": ["تقریباً دو پنجم", "یک دهم", "بیش از سه چهارم", "کمتر از پنج درصد"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "One-tenth",
        "why_plausible": "A plausible estimate for peripheral rural or agrarian strikes.",
        "why_wrong": "Public sector strikes paralyzed the entire state administration, accounting for nearly 40% (two-fifths)."
      },
      {
        "option": "Over three-quarters",
        "why_plausible": "Public sector strikes were so visible they often seemed to dominate the entire strike wave.",
        "why_wrong": "Bazaars and schools accounted for nearly half, leaving the public sector at almost two-fifths."
      },
      {
        "option": "Less than five percent",
        "why_plausible": "Reflects the tiny proportion of strikes carried out strictly by traditional peasants.",
        "why_wrong": "Civil servants, bank employees, and state technocrats formed a huge 40% chunk of the strike total."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["One-half", "One-quarter"],
      "fa": ["یک دوم", "یک چهارم"]
    },
    "specificity_prompt": {
      "en": "Please state the fraction or ratio of public-sector strikes documented in the text.",
      "fa": "لطفاً نسبت یا کسر آماری اعتصابات بخش عمومی را طبق متن بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Almost two-fifths. Spot on. You actually paid attention to the footnotes and statistical tables.",
        "wrong_generic": "No. The proportion was almost two-fifths (about 40 percent). Read the tables before guessing.",
        "common_wrong_answers": {
          "One-tenth": "One-tenth is way too low; public bureaucracy was 40% of all strikes.",
          "Over three-quarters": "No, schools and bazaars had half the strikes.",
          "Less than five percent": "5% was peasants, not the civil service."
        }
      },
      "fa": {
        "correct_generic": "تقریباً دو پنجم. کاملاً درسته! معلوم است جداول آماری را هم از زیر ذره‌بین رد کرده‌اید.",
        "wrong_generic": "خیر، پاسخ درست تقریباً دو پنجم (حدود چهل درصد) بود. آمار جامعه‌شناختی را سرسری نگیرید.",
        "common_wrong_answers": {
          "یک دهم": "یک دهم بسیار کم است؛ چهل درصد اعتصابات در بوروکراسی دولتی رخ داد.",
          "بیش از سه چهارم": "نخیر، بازار و مدارس نیمی از اعتصابات را در دست داشتند.",
          "کمتر از پنج درصد": "کمتر از پنج درصد سهم روستاییان بود، نه کارمندان دولت."
        }
      }
    },
    "explanation": {
      "en": "In their empirical breakdown of 1,195 strikes during the fourth stage of the revolution, Ashraf and Banuazizi reveal that almost two-fifths took place across public-sector ministries and banks, shattering state administrative capacity.",
      "fa": "اشرف و بنوعزیزی در تحلیل کمّی ۱۱۹۵ اعتصاب انقلاب نشان می‌دهند که نزدیک به دو پنجم اعتصابات در وزارتخانه‌ها، بانک‌ها و نهادهای دولتی رخ داد و ماشین اداری رژیم را زمین‌گیر کرد."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "Similarly, of the total of 1,195 mass strikes, which occurred mainly in the fourth stage of the revolution, nearly one-half involved elements from the bazaar and from schools and universities, almost two-fifths took place in the various public-sector institutions and government ministries.",
      "evidence_type": "FACT"
    }
  },

  # CATEGORY 2: Double Jeopardy (Ashraf: Revolutionary Komitehs)
  {
    "id": "double_komiteh_power_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "KOMITEH TO MEMORY",
      "fa": "کمیته‌بازی سر کوچه"
    },
    "clue_text": {
      "en": "Ashraf and Banuazizi observe that local neighborhood Komitehs were originally established in late 1978 as civilian self-defense militias in response to armed incursions by these pro-regime, lumpenproletarian thugs.",
      "fa": "اشرف و بنوعزیزی نشان می‌دهند که کمیته‌های محلی انقلاب در اواخر سال ۱۳۵۷ در اصل به عنوان هسته‌های دفاع غیرنظامی در برابر یورش‌های خشونت‌بار این اوباش چماق‌دار طرفدار رژیم پهلوی شکل گرفتند."
    },
    "canonical_answer": {
      "en": "Club-wielders",
      "fa": "چماق‌داران"
    },
    "accepted_aliases": {
      "en": ["Chomaq-daran", "Lumpenproletarian club-wielders", "Chomaqdaran", "Pro-regime club-wielders"],
      "fa": ["چماقداران", "چماق‌دارها", "لات‌ها و چماق‌داران"]
    },
    "options": {
      "en": ["Club-wielders", "Imperial Guard", "SAVAK interrogators", "Gendarmerie officers"],
      "fa": ["چماق‌داران", "گارد جاویدان", "بازجویان ساواک", "افسران ژاندارمری"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Imperial Guard",
        "why_plausible": "The elite palace guard (Garde-e Javidan) that fought revolutionaries on the streets.",
        "why_wrong": "The Imperial Guard was a regular elite military uniform formation, not the hired lumpen street thugs."
      },
      {
        "option": "SAVAK interrogators",
        "why_plausible": "The hated secret police security apparatus directing covert operations.",
        "why_wrong": "SAVAK agents conducted surveillance and detention, but neighborhood defense committees specifically organized against street gangs wielding clubs."
      },
      {
        "option": "Gendarmerie officers",
        "why_plausible": "The rural and suburban policing force guarding outposts.",
        "why_wrong": "The gendarmerie were uniformed state constables who generally remained inside garrisons."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Shahrbani", "Rastakhiz youth brigades"],
      "fa": ["شهربانی", "جوانان حزب رستاخیز"]
    },
    "specificity_prompt": {
      "en": "Please name the colloquial Iranian term for the pro-Shah thugs armed with sticks.",
      "fa": "لطفاً عنوان مصطلح فارسی برای مزدوران چوب‌به‌دست حامی دربار را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Club-wielders (Chomaq-daran). Spot on. The regime's last street fighters.",
        "wrong_generic": "No. The answer was the club-wielders (Chomaq-daran).",
        "common_wrong_answers": {
          "Imperial Guard": "The Imperial Guard had Chieftain tanks; these thugs carried wooden clubs.",
          "SAVAK interrogators": "SAVAK worked in prisons; club-wielders smashed bazaar shop windows.",
          "Gendarmerie officers": "The Gendarmerie were rural police, not hired lumpen gangs."
        }
      },
      "fa": {
        "correct_generic": "چماق‌داران. کاملاً درسته! همان پیاده‌نظام چماق‌به‌دست دربار که دکان‌های بازار را آتش می‌زدند.",
        "wrong_generic": "خیر، پاسخ درست چماق‌داران بود. اصطلاحات خیابانی سال ۵۷ را از یاد برده‌اید.",
        "common_wrong_answers": {
          "گارد جاویدان": "گارد جاویدان تانک چیفتن داشت، چماق چوبی نداشت.",
          "بازجویان ساواک": "ساواک در شکنجه‌گاه‌ها فعال بود، این‌ها اوباش اجیرشده خیابان بودند.",
          "افسران ژاندارمری": "ژاندارمری نیروی انتظامی یونیفرم‌پوش بود، نه چماق‌دار چماق‌به‌دست."
        }
      }
    },
    "explanation": {
      "en": "Ashraf details how neighborhood Islamic committees originally mobilized to defend homes, schools, and shops against the lumpenproletarian club-wielders (chomaq-daran) hired by the Pahlavi regime.",
      "fa": "احمد اشرف توضیح می‌دهد که کمیته‌های محلی انقلاب در ابتدا برای محافظت از مغازه‌ها، مدارس و خانه‌ها در برابر چماق‌داران اجیرشده رژیم شاه به راه افتادند و بعداً قدرت محلات را به دست گرفتند."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 14,
      "verbatim_passage": "These committees, originally formed in response to the counter-revolutionary demonstrations by the lumpenproletarian club-wielders, began their activities during the fourth stage and continued to play such a role to the end.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_power_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "KOMITEH TO MEMORY",
      "fa": "کمیته‌بازی سر کوچه"
    },
    "clue_text": {
      "en": "Immediately after the collapse of the monarchy in February 1979, Ayatollah Khomeini appointed this conservative cleric to head the Central Revolutionary Komiteh (Komiteh-ye Markazi) in Tehran, supervising armed neighborhood cells.",
      "fa": "بلافاصله پس از سقوط سلطنت در بهمن ۱۳۵۷، آیت‌الله خمینی این روحانی سرشناس محافظه‌کار را به سرپرستی کمیته مرکزی انقلاب اسلامی در تهران منصوب کرد تا هزاران هسته مسلح محلات را سازماندهی کند."
    },
    "canonical_answer": {
      "en": "Mohammad Reza Mahdavi Kani",
      "fa": "محمدرضا مهدوی کنی"
    },
    "accepted_aliases": {
      "en": ["Mahdavi Kani", "Ayatollah Mahdavi Kani", "Mohammad-Reza Mahdavi Kani"],
      "fa": ["آیت‌الله مهدوی کنی", "مهدوی کنی", "شیخ محمدرضا مهدوی کنی"]
    },
    "options": {
      "en": ["Mohammad Reza Mahdavi Kani", "Sadeq Khalkhali", "Ali Akbar Hashemi Rafsanjani", "Mohammad Beheshti"],
      "fa": ["محمدرضا مهدوی کنی", "صادق خلخالی", "علی‌اکبر هاشمی رفسنجانی", "سید محمد حسینی بهشتی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Sadeq Khalkhali",
        "why_plausible": "The notorious chief of the revolutionary tribunals executing Pahlavi officials.",
        "why_wrong": "Khalkhali headed the Revolutionary Court (Dadgah-e Enqelab), not the administrative Central Komiteh."
      },
      {
        "option": "Ali Akbar Hashemi Rafsanjani",
        "why_plausible": "A key leader in the Revolutionary Council and later minister of interior.",
        "why_wrong": "He served on the Revolutionary Council and supervised parliament, but Mahdavi Kani directed the Komitehs."
      },
      {
        "option": "Mohammad Beheshti",
        "why_plausible": "The powerful leader of the Islamic Republican Party and head of the judiciary.",
        "why_wrong": "Beheshti led the IRP and the Supreme Court, delegating internal security Komitehs to Mahdavi Kani."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Abdolkarim Musavi Ardebili", "Asadollah Lajevardi"],
      "fa": ["عبدالکریم موسوی اردبیلی", "اسدالله لاجوردی"]
    },
    "specificity_prompt": {
      "en": "Please name the head of the Central Committee who later served as interim prime minister in 1981.",
      "fa": "لطفاً نام روحانی ریاست کمیته مرکزی انقلاب اسلامی را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad Reza Mahdavi Kani. Correct. The clerical patron of armed neighborhood youths.",
        "wrong_generic": "No. The head of the Central Komiteh was Ayatollah Mahdavi Kani.",
        "common_wrong_answers": {
          "Sadeq Khalkhali": "Khalkhali handed out death sentences in the courts; he didn't run the neighborhood patrol cars.",
          "Ali Akbar Hashemi Rafsanjani": "Rafsanjani was busy in the Revolutionary Council.",
          "Mohammad Beheshti": "Beheshti commanded the party; Mahdavi Kani commanded the Komitehs."
        }
      },
      "fa": {
        "correct_generic": "محمدرضا مهدوی کنی. کاملاً درسته! سرپرست کمیته‌های انقلاب در میدان بهارستان.",
        "wrong_generic": "خیر، رئیس کمیته مرکزی انقلاب مهدوی کنی بود. ساختار نهادهای امنیتی ابتدای انقلاب را مرور کنید.",
        "common_wrong_answers": {
          "صادق خلخالی": "خلخالی حاکم شرع دادگاه‌های انقلاب بود، نه سرپرست پاسداران کمیته.",
          "علی‌اکبر هاشمی رفسنجانی": "رفسنجانی عضو شورای انقلاب بود، کمیته‌ها دست مهدوی کنی بود.",
          "سید محمد حسینی بهشتی": "بهشتی حزب جمهوری را می‌چرخاند، مهدوی کنی مسلحین کمیته را هدایت می‌کرد."
        }
      }
    },
    "explanation": {
      "en": "Ashraf highlights how the local Komitehs, centralized under Ayatollah Mahdavi Kani, served as the paramount armed grass-roots institutions enforcing public order and clerical authority in the transition period.",
      "fa": "احمد اشرف تشریح می‌کند که چگونه کمیته‌های انقلاب اسلامی تحت هدایت آیت‌الله مهدوی کنی، نظم خیابانی و اعمال حاکمیت روحانیت را در محلات سراسر کشور برقرار ساختند."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 17,
      "verbatim_passage": "Under the new sovereignty, however, a new multiplicity of powers emerged, including the Islamic Revolutionary Committees under Khomeini and his immediate lieutenants, the state apparatus under Premier Bazargan, several armed radical guerrilla organizations.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_power_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "KOMITEH TO MEMORY",
      "fa": "کمیته‌بازی سر کوچه"
    },
    "clue_text": {
      "en": "In early 1979, Prime Minister Mehdi Bazargan famously denounced the uncoordinated armed actions of the autonomous Komitehs and revolutionary tribunals by comparing his government to a knife lacking this essential physical component.",
      "fa": "در اوایل سال ۱۳۵۸، نخست‌وزیر مهدی بازرگان در انتقادی مشهور از اقدامات خودسرانه کمیته‌ها و دادگاه‌های انقلاب، دولت موقت خود را به چاقویی تشبیه کرد که فاقد این عضو حیاتی است."
    },
    "canonical_answer": {
      "en": "A blade",
      "fa": "تیغه"
    },
    "accepted_aliases": {
      "en": ["Knife without a blade", "The blade", "A knife without a blade", "Cutting blade"],
      "fa": ["تیغه چاقو", "چاقوی بی‌تیغه", "تیغ"]
    },
    "options": {
      "en": ["A blade", "A handle", "A sheath", "A sharp edge"],
      "fa": ["تیغه", "دسته", "غلاف", "لبه تیز"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "A handle",
        "why_plausible": "A common mechanical component of hand weapons.",
        "why_wrong": "Bazargan held the administrative handle (the cabinet), but lamented that the armed Komitehs held the cutting power (the blade)."
      },
      {
        "option": "A sheath",
        "why_plausible": "A protective accessory associated with swords and daggers.",
        "why_wrong": "Bazargan's famous quote was specifically: 'The government is a knife without a blade' (chāqū-ye bī-tīgh)."
      },
      {
        "option": "A sharp edge",
        "why_plausible": "Synonymous with a dull or ineffective blade.",
        "why_wrong": "He lamented that the knife had no blade at all, not that its edge was dull."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["A gun without bullets", "A car without an engine"],
      "fa": ["تفنگ بی‌پوکه", "ماشین بدون موتور"]
    },
    "specificity_prompt": {
      "en": "Please identify the specific physical part of the knife Bazargan claimed his cabinet lacked.",
      "fa": "لطفاً جزء دقیق چاقو را در کلام بازرگان نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "A blade. Correct. 'A knife without a blade'—the classic summary of the Provisional Government.",
        "wrong_generic": "No. Bazargan said his government was a knife without a blade (tīgh).",
        "common_wrong_answers": {
          "A handle": "Bazargan had the handle; the Komitehs had the blade.",
          "A sheath": "A sheath holds a knife; he said he had no blade to cut with.",
          "A sharp edge": "He didn't say it was dull; he said the blade wasn't there at all."
        }
      },
      "fa": {
        "correct_generic": "تیغه. کاملاً درسته! همان «چاقوی بی‌تیغه» معروفی که بازرگان در برابر کمیته‌ها توصیف می‌کرد.",
        "wrong_generic": "خیر، پاسخ درست تیغه بود. تمثیل‌های مشهور مهدی بازرگان را هم از بر نیستید.",
        "common_wrong_answers": {
          "دسته": "دسته چاقو در دست بازرگان بود، تیغه برنده در دست کمیته‌ها بود.",
          "غلاف": "غلاف وسیله محافظت است، بازرگان گفت دولت قدرت برش ندارد.",
          "لبه تیز": "نگفت کند است، گفت اصلاً تیغه‌ای وجود ندارد."
        }
      }
    },
    "explanation": {
      "en": "Ashraf highlights the reality of dual sovereignty in 1979, where the official provisional state under Bazargan was routinely paralyzed by the autonomous revolutionary Komitehs, prompting Bazargan's remark that he was given 'a knife without a blade'.",
      "fa": "احمد اشرف تقابل حاکمیت دوگانه را توضیح می‌دهد که در آن کمیته‌های مسلح عملاً دستورات دولت موقت را وتو می‌کردند و بازرگان دولت خود را چاقوی بی‌تیغه نامید."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 17,
      "verbatim_passage": "Under the new sovereignty, however, a new multiplicity of powers emerged, including the Islamic Revolutionary Committees under Khomeini and his immediate lieutenants, the state apparatus under Premier Bazargan.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_komiteh_power_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "KOMITEH TO MEMORY",
      "fa": "کمیته‌بازی سر کوچه"
    },
    "clue_text": {
      "en": "According to Ashraf and Banuazizi's structural mapping, over 60 percent of early urban revolutionary Komitehs in Tehran were physically housed in and administered directly out of these local neighborhood institutions.",
      "fa": "طبق نقشه‌برداری ساختاری اشرف و بنوعزیزی، بیش از شصت درصد از کمیته‌های اولیه انقلاب در تهران، مقر فرماندهی خود را در این نهادهای محلی مستقر کرده بودند و مستقیماً از آنجا اداره می‌شدند."
    },
    "canonical_answer": {
      "en": "Mosques",
      "fa": "مساجد"
    },
    "accepted_aliases": {
      "en": ["Local mosques", "Neighborhood mosques", "Masajid"],
      "fa": ["مسجدها", "مساجد محلات", "مسجد"]
    },
    "options": {
      "en": ["Mosques", "Police stations", "Municipal council offices", "Secondary school gymnasiums"],
      "fa": ["مساجد", "کلانتری‌ها", "شهرداری‌ها", "سالن‌های ورزشی مدارس"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Police stations",
        "why_plausible": "Shahrbani police precincts were overrun by insurgents on February 11.",
        "why_wrong": "Precincts were disarmed, but the clerical Komiteh network deliberately established headquarters inside local mosques."
      },
      {
        "option": "Municipal council offices",
        "why_plausible": "Tehran municipality had regional branches across districts.",
        "why_wrong": "Municipal buildings remained part of the civilian civil bureaucracy, not the religious revolutionary militia centers."
      },
      {
        "option": "Secondary school gymnasiums",
        "why_plausible": "Large school halls were sometimes used for refugee or food storage.",
        "why_wrong": "Mosques were the organic communication and armed command nodal points for the revolutionary clerisy."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Husseiniyehs", "Bazaar caravanserai"],
      "fa": ["حسینیه‌ها", "کاروانسراهای بازار"]
    },
    "specificity_prompt": {
      "en": "Please identify the religious institutional building used as Komiteh command posts.",
      "fa": "لطفاً مکان مذهبی استقرار ستادهای محلی کمیته را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mosques. Spot on. The spiritual and tactical base of the revolutionary neighborhood.",
        "wrong_generic": "No. The command posts were mosques (masajid).",
        "common_wrong_answers": {
          "Police stations": "Police stations were disarmed; the new power sat in the mosques.",
          "Municipal council offices": "Town halls were civil offices, not armed revolutionary bastions.",
          "Secondary school gymnasiums": "Gymnasiums held volleyball, not revolutionary patrols."
        }
      },
      "fa": {
        "correct_generic": "مساجد. کاملاً درسته! سنگر اصلی و ستاد تدارکات کمیته‌های انقلاب در محلات.",
        "wrong_generic": "خیر، پایگاه‌های اصلی کمیته مساجد بودند. پایگاه اجتماعی روحانیت را فراموش کرده‌اید.",
        "common_wrong_answers": {
          "کلانتری‌ها": "کلانتری‌ها خلع سلاح شدند، قدرت جدید در مساجد مستقر شد.",
          "شهرداری‌ها": "شهرداری‌ها اداره امور شهری می‌کردند، کمیته‌ها در مساجد حکم می‌راندند.",
          "سالن‌های ورزشی مدارس": "سالن ورزشی محل ورزش بود، نه ستاد نگهبانی و بازداشتگاه محلی."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi document that neighborhood mosques served as the organic institutional cells of the revolution, housing the local Islamic committees, stockpiling seized armaments, and coordinating rationing.",
      "fa": "اشرف و بنوعزیزی نشان می‌دهند که مساجد محلات به ستادهای عملیاتی کمیته‌های انقلاب اسلامی بدل شدند و تسلیحات غنیمتی و سهمیه‌بندی مایحتاج در آنجا مدیریت می‌شد."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 27,
      "verbatim_passage": "The network of some 20,000 to 25,000 mosques in the country was the single most extensive, autonomous, and resourceful institutional structure in Iranian society... Over 60 percent of the revolutionary committees were based in local mosques.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_komiteh_power_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "KOMITEH TO MEMORY",
      "fa": "کمیته‌بازی سر کوچه"
    },
    "clue_text": {
      "en": "Twelve years after their chaotic street-level inception, the Islamic Revolutionary Komitehs were officially abolished in 1991 when the Majles merged them with the Gendarmerie and Shahrbani into this unified police force.",
      "fa": "دوازده سال پس از تأسیس جنجالی در خیابان‌ها، کمیته‌های انقلاب اسلامی در سال ۱۳۷۰ خورشیدی با مصوبه مجلس منحل و با ادغام در شهربانی و ژاندارمری، این نیروی انتظامی واحد را تشکیل دادند."
    },
    "canonical_answer": {
      "en": "Law Enforcement Force",
      "fa": "نیروی انتظامی جمهوری اسلامی ایران"
    },
    "accepted_aliases": {
      "en": ["NAJA", "Law Enforcement Command", "Disciplinary Force of the Islamic Republic of Iran", "Faraja", "Nirou-ye Entezami"],
      "fa": ["ناجا", "نیروی انتظامی", "فراجا", "شهربانی و ژاندارمری واحد"]
    },
    "options": {
      "en": ["Law Enforcement Force", "Basij Resistance Force", "Islamic Revolutionary Guard Corps", "Ansar-e Hezbollah"],
      "fa": ["نیروی انتظامی جمهوری اسلامی ایران", "نیروی مقاومت بسیج", "سپاه پاسداران انقلاب اسلامی", "انصار حزب‌الله"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Basij Resistance Force",
        "why_plausible": "A popular volunteer auxiliary force with street presence.",
        "why_wrong": "The Basij operated under the IRGC and was not the 1991 merger of the municipal police, rural gendarmerie, and Komitehs."
      },
      {
        "option": "Islamic Revolutionary Guard Corps",
        "why_plausible": "The primary military guardian of the revolution founded in 1979.",
        "why_wrong": "The IRGC remained a separate parallel military service branch; it did not absorb the regular civilian police and gendarmerie."
      },
      {
        "option": "Ansar-e Hezbollah",
        "why_plausible": "A hardline vigilante group enforcing dress codes in the 1990s.",
        "why_wrong": "An informal vigilante shock group, not the formal state statutory police merger created by parliamentary legislation."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["VAVAK", "Quds Force"],
      "fa": ["وزارت اطلاعات", "نیروی قدس"]
    },
    "specificity_prompt": {
      "en": "Please state the official name of the unified police force established by the 1991 merger.",
      "fa": "لطفاً نام رسمی نیروی مسلح ادغامی جدید در سال ۱۳۷۰ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Law Enforcement Force (NAJA). Spot on. When the boys in green merged with the boys with beards.",
        "wrong_generic": "No. The merged entity was the Law Enforcement Force (Nirou-ye Entezami - NAJA).",
        "common_wrong_answers": {
          "Basij Resistance Force": "The Basij reports to the IRGC; NAJA reports to the Interior Ministry.",
          "Islamic Revolutionary Guard Corps": "The IRGC kept its separate army; it didn't become traffic cops.",
          "Ansar-e Hezbollah": "Ansar-e Hezbollah rode motorbikes with iron bars, not official police cruisers."
        }
      },
      "fa": {
        "correct_generic": "نیروی انتظامی جمهوری اسلامی ایران. کاملاً درسته! ادغام بزرگ کمیته، شهربانی و ژاندارمری در سال ۱۳۷۰.",
        "wrong_generic": "خیر، نهاد حاصل از ادغام نیروی انتظامی (ناجا) بود. تاریخ تشکیلات پلیس را دوباره بخوانید.",
        "common_wrong_answers": {
          "نیروی مقاومت بسیج": "بسیج زیرمجموعه سپاه بود، نه حاصل ادغام شهربانی و ژاندارمری.",
          "سپاه پاسداران انقلاب اسلامی": "سپاه ارتش موازات ماند، پلیس راهور و کلانتری نشد.",
          "انصار حزب‌الله": "انصار حزب‌الله گروه فشار موتورسوار بود، نه نیروی انتظامی رسمی کشور."
        }
      }
    },
    "explanation": {
      "en": "Ashraf notes how the revolutionary Komitehs evolved from chaotic neighborhood militias into institutionalized security arms, until their 1991 formal merger into NAJA dismantled their autonomous clerical structure.",
      "fa": "احمد اشرف تشریح می‌کند که کمیته‌ها پس از یک دهه مداخله مستقل در امور قضایی و اجتماعی، سرانجام در سال ۱۳۷۰ با ژاندارمری و شهربانی ادغام شدند تا ساختار پلیس واحد (ناجا) شکل گیرد."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 17,
      "verbatim_passage": "Under the new sovereignty, however, a new multiplicity of powers emerged, including the Islamic Revolutionary Committees under Khomeini and his immediate lieutenants, the state apparatus under Premier Bazargan.",
      "evidence_type": "HISTORIOGRAPHICAL_DISPUTE"
    }
  },

  # CATEGORY 3: Single Jeopardy (Ashraf: Working Class Mobilization)
  {
    "id": "single_workers_shura_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "WORKERS OF THE REVOLUTION, UNITE!",
      "fa": "شورا به وقت کارخانه"
    },
    "clue_text": {
      "en": "During the collapse of factory management in late 1978, Iranian industrial workers established these collective self-management councils to take control of production lines and purge pro-Shah executives.",
      "fa": "در جریان فروپاشی مدیریت کارخانه‌ها در اواخر سال ۱۳۵۷، کارگران صنعتی ایران این شوراهای خودگردان جمعی را برای کنترل خطوط تولید و اخراج مدیران وابسته به رژیم شاه تشکیل دادند."
    },
    "canonical_answer": {
      "en": "Worker Shuras",
      "fa": "شوراهای کارگری"
    },
    "accepted_aliases": {
      "en": ["Factory Shuras", "Islamic Worker Councils", "Worker Councils", "Shura-haye Kargari"],
      "fa": ["شوراهای اسلامی کار", "شورای کارخانه", "شورای کارگری"]
    },
    "options": {
      "en": ["Worker Shuras", "Pahlavi Syndicates", "Guild Chambers", "Khayami Cooperatives"],
      "fa": ["شوراهای کارگری", "سندیکاهای دولتی پهلوی", "اتاق اصناف", "تعاونی‌های خیامی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Pahlavi Syndicates",
        "why_plausible": "Official government-sponsored labor unions functioning under the Shah.",
        "why_wrong": "Pahlavi syndicates were puppet state labor bodies dissolved by striking workers during the insurrection."
      },
      {
        "option": "Guild Chambers",
        "why_plausible": "The representative commercial body governing bazaar shopkeepers.",
        "why_wrong": "Guild chambers represented petty-bourgeois shop owners, not factory shop-floor industrial workers."
      },
      {
        "option": "Khayami Cooperatives",
        "why_plausible": "Company welfare organizations established by auto magnate Ahmad Khayami.",
        "why_wrong": "Paternalistic corporate benefits programs, not grassroots revolutionary worker councils."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Trade Union Congress", "Labor ministry boards"],
      "fa": ["کنگره اتحادیه‌های کارگری", "هیئت‌های حل اختلاف وزارت کار"]
    },
    "specificity_prompt": {
      "en": "Please name the Arabic-derived council term used by revolutionary factory workers.",
      "fa": "لطفاً اصطلاح عربی‌تبار شورای خودگردان کارگران را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Worker Shuras. Quite right. When the assembly line seized the factory keys.",
        "wrong_generic": "No. The answer was the Worker Shuras (شوراهای کارگری).",
        "common_wrong_answers": {
          "Pahlavi Syndicates": "Pahlavi syndicates were royal lapdogs; the Shuras kicked the bosses out.",
          "Guild Chambers": "Guild chambers are for bazaar merchants selling carpets, not factory assembly lines.",
          "Khayami Cooperatives": "Khayami was the owner fleeing to London, not the workers taking over."
        }
      },
      "fa": {
        "correct_generic": "شوراهای کارگری. کاملاً درسته! زمانی که کارگران خط تولید کارفرماها را بیرون انداختند.",
        "wrong_generic": "خیر، پاسخ درست شوراهای کارگری بود. نهادهای خودگردان کارخانه‌ها را فراموش کرده‌اید.",
        "common_wrong_answers": {
          "سندیکاهای دولتی پهلوی": "سندیکاهای پهلوی دست‌نشانده ساواک بودند و کارگران بساطشان را جمع کردند.",
          "اتاق اصناف": "اتاق اصناف متعلق به بازاریان و کسبه بود، نه کارگران کارخانه.",
          "تعاونی‌های خیامی": "برادران خیامی صاحب کارخانه بودند و فرار کردند، کارگران شورا ساختند."
        }
      }
    },
    "explanation": {
      "en": "Ashraf notes that industrial workers utilized worker councils (shuras) to take over industrial plants, expelling executives and directing production during the revolutionary transition.",
      "fa": "احمد اشرف تشریح می‌کند که کارگران صنعتی در اواخر سال ۱۳۵۷ با تشکیل شوراهای کارگری کارخانه‌ها را تصرف کرده و خود مدیریت خطوط تولید را بر عهده گرفتند."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "Two other strata, the modern middle class (principally salaried workers in the public sector and members of the liberal professions) and the industrial working class, joined the revolution only in its later stages. Although they were latecomers, their contribution to the success of the revolution was critical.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_workers_shura_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "WORKERS OF THE REVOLUTION, UNITE!",
      "fa": "شورا به وقت کارخانه"
    },
    "clue_text": {
      "en": "To sustain the crippling general strikes of late 1978 after the government froze wages, this traditional commercial class distributed financial strike funds, loans, and food rations to civil servants and industrial workers.",
      "fa": "برای تداوم اعتصابات فلج‌کننده اواخر سال ۱۳۵۷ پس از قطع حقوق توسط دولت، این طبقه سنتی تجاری با توزیع صندوق‌های همبستگی مالی، وام و آذوقه، کارمندان و کارگران صنعتی را حمایت کرد."
    },
    "canonical_answer": {
      "en": "Bazaaris",
      "fa": "بازاریان"
    },
    "accepted_aliases": {
      "en": ["Bazaar merchants", "Bazaar traders", "Bazaari class", "Traditional petty bourgeoisie"],
      "fa": ["کسبه و بازاریان", "اهالی بازار", "تجار بازار"]
    },
    "options": {
      "en": ["Bazaaris", "Foreign oil consortium", "Modern industrial magnates", "Court chamberlains"],
      "fa": ["بازاریان", "کنسرسیوم خارجی نفت", "صنعت‌گران مدرن وابسته", "درباریان پهلوی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Foreign oil consortium",
        "why_plausible": "The international consortium extracting Iranian petroleum.",
        "why_wrong": "The consortium opposed strikes and shut down shipping operations rather than funding striking workers."
      },
      {
        "option": "Modern industrial magnates",
        "why_plausible": "Large factory owners in Tehran and Karaj.",
        "why_wrong": "Tied directly to Pahlavi state contracts, they faced bankruptcy and strikes rather than financing them."
      },
      {
        "option": "Court chamberlains",
        "why_plausible": "Pahlavi royal officials distributing palace patronage.",
        "why_wrong": "They represented the royal court desperate to crush the strikes and restart the economy."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Landlords", "State banks"],
      "fa": ["زمین‌داران بزرگ", "بانک‌های دولتی"]
    },
    "specificity_prompt": {
      "en": "Please name the commercial merchant class that funded the strike relief funds.",
      "fa": "لطفاً صنف یا طبقه تجاری تأمین‌کننده مالی صندوق اعتصابات را نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Bazaaris. Exactly. The merchants who paid workers to stay home and bankrupt the throne.",
        "wrong_generic": "No. The strike funds were bankrolled by the Bazaaris.",
        "common_wrong_answers": {
          "Foreign oil consortium": "The consortium wanted oil pumped, not workers striking on strike pay.",
          "Modern industrial magnates": "The big factory bosses were fleeing to Europe, not writing strike checks.",
          "Court chamberlains": "The court was trying to break the strike, not fund it."
        }
      },
      "fa": {
        "correct_generic": "بازاریان. کاملاً درسته! حجره‌دارانی که حقوق کارگران اعتصابی را پرداختند تا دودمان سلطنت بر باد برود.",
        "wrong_generic": "خیر، تأمین مالی اعتصابات کار بازاریان بود. نقدینگی بازار را دست‌کم گرفته‌اید.",
        "common_wrong_answers": {
          "کنسرسیوم خارجی نفت": "کنسرسیوم نفت می‌خواست، نه اعتصاب و خوابیدن پالایشگاه.",
          "صنعت‌گران مدرن وابسته": "سرمایه‌داران وابسته فرار را بر قرار ترجیح دادند، نه پرداخت حقوق اعتصابیون.",
          "درباریان پهلوی": "درباریان مستأصل از اعتصاب بودند، پول به اعتصاب‌کننده نمی‌دادند."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi emphasize that the mosque-bazaar alliance sustained the late 1978 general strike by utilizing traditional religious charities, tithes, and guild credit to distribute cash allowances to striking families.",
      "fa": "اشرف و بنوعزیزی تشریح می‌کنند که ائتلاف مسجد و بازار با بهره‌گیری از وجوهات شرعی و اعتبارات بازاری، صندوق‌های حمایتی ایجاد کردند و نگذاشتند فقر مانع تداوم اعتصاب کارگران شود."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "For example, of some 2,483 demonstrations reported in the course of the revolution, 64 percent were organized by the mosque-bazaar alliance... The bazaar also provided critical financial backing for strikers across public and private sectors.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_workers_shura_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "WORKERS OF THE REVOLUTION, UNITE!",
      "fa": "شورا به وقت کارخانه"
    },
    "clue_text": {
      "en": "Although their strikes ultimately paralyzed the national economy, Ashraf and Banuazizi calculate that the industrial proletariat accounted for this minuscule percentage—just one percent—of all mass street demonstrations during the revolution.",
      "fa": "گرچه اعتصابات آنان اقتصاد کشور را فلج کرد، اما در تحلیل آماری اشرف و بنوعزیزی، طبقه کارگر صنعتی تنها این سهم ناچیز (یک درصد) را از کل تظاهرات خیابانی دوران انقلاب بر عهده داشتند."
    },
    "canonical_answer": {
      "en": "One percent",
      "fa": "یک درصد"
    },
    "accepted_aliases": {
      "en": ["1 percent", "1%", "One per cent"],
      "fa": ["۱ درصد", "۱٪", "یک درصدی"]
    },
    "options": {
      "en": ["One percent", "Twenty-five percent", "Fifteen percent", "Fifty percent"],
      "fa": ["یک درصد", "بیست و پنج درصد", "پانزده درصد", "پنجاه درصد"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Twenty-five percent",
        "why_plausible": "Reflects the substantial portion of demonstrations led by students and teachers.",
        "why_wrong": "Students and teachers mounted 23 percent; factory workers organized only 1 percent."
      },
      {
        "option": "Fifteen percent",
        "why_plausible": "A typical assumed contribution for industrial laborers in Marxist revolutions.",
        "why_wrong": "Ashraf's empirical street data shows the industrial working class was predominantly on strike rather than staging street marches."
      },
      {
        "option": "Fifty percent",
        "why_plausible": "Matches conventional socialist rhetoric claiming revolutions are half proletarian.",
        "why_wrong": "Mosque-bazaar networks accounted for 64%, leaving the factory working class at a tiny 1%."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Ten percent", "Two percent"],
      "fa": ["ده درصد", "دو درصد"]
    },
    "specificity_prompt": {
      "en": "Please specify the exact single-digit percentage of demonstrations attributed to industrial workers.",
      "fa": "لطفاً رقم درصد دقیق سهم کارگران صنعتی در راهپیمایی‌ها را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "One percent. Spot on. Proving that striking at work matters far more than shouting on the avenue.",
        "wrong_generic": "No. The statistical share was a mere one percent (1%).",
        "common_wrong_answers": {
          "Twenty-five percent": "25% was the university students, not factory laborers.",
          "Fifteen percent": "15% is romantic socialist mythology, not Ashraf's data.",
          "Fifty percent": "50%? The bazaar ran the streets, not the factories."
        }
      },
      "fa": {
        "correct_generic": "یک درصد. کاملاً درسته! آماری که نشان می‌دهد کارگران چرخ تولید را بستند، نه اینکه خیابان‌گردی کنند.",
        "wrong_generic": "خیر، سهم کارگران صنعتی در راهپیمایی‌ها فقط یک درصد (۱٪) بود. توهمات جزوه‌خوانی را کنار بگذارید.",
        "common_wrong_answers": {
          "بیست و پنج درصد": "بیست و پنج درصد سهم دانشجویان و معلمان بود، نه کارگران کارخانه‌ها.",
          "پانزده درصد": "پانزده درصد خیال‌بافی مارکسیستی است، نه آمار میدانی اشرف.",
          "پنجاه درصد": "پنجاه درصد؟ شصت و چهار درصد راهپیمایی‌ها دست ائتلاف مسجد و بازار بود."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi's quantitative analysis shows that industrial workers contributed through strikes at production sites, whereas street demonstrations were overwhelmingly dominated by the mosque-bazaar alliance (64%) and students (23%).",
      "fa": "تحلیل کمّی اشرف نشان می‌دهد که کارگران صنعتی قدرت خود را با خواباندن چرخ کارخانه‌ها نشان دادند و تنها ۱ درصد از تظاهرات را هدایت کردند، در حالی که خیابان‌ها در قبضه مسجد، بازار و دانشجویان بود."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "For example, of some 2,483 demonstrations reported in the course of the revolution, 64 percent were organized by the mosque-bazaar alliance, 23 percent by secondary-school and university students and teachers, and the remaining 13 percent by other groups such as peasants (2 percent), the industrial proletariat (1 percent), and white-collar public workers (1 percent).",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_workers_shura_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "WORKERS OF THE REVOLUTION, UNITE!",
      "fa": "شورا به وقت کارخانه"
    },
    "clue_text": {
      "en": "In Ashraf and Banuazizi's class taxonomy, this social stratum—consisting of salaried civil servants, engineers, technocrats, and lawyers—joined the revolutionary fold during Stage IV, crippling government ministries and banks with white-collar strikes.",
      "fa": "در طبقه‌بندی اجتماعی اشرف و بنوعزیزی، این قشر اجتماعی شامل کارمندان حقوق‌بگیر دولت، مهندسان، فن‌سالاران و وکلا، در مرحله چهارم به انقلاب پیوستند و با اعتصابات اداری، وزارتخانه‌ها و نظام بانکی را قفل کردند."
    },
    "canonical_answer": {
      "en": "Modern middle class",
      "fa": "طبقه متوسط جدید"
    },
    "accepted_aliases": {
      "en": ["New middle class", "Salaried middle class", "Professional middle class", "Tabaqeh-ye motavasset-e jadid"],
      "fa": ["طبقه متوسط مدرن", "قشر حقوق‌بگیر مدرن", "طبقه متوسط شهری جدید"]
    },
    "options": {
      "en": ["Modern middle class", "Traditional petty bourgeoisie", "Industrial working class", "Lumpenproletariat"],
      "fa": ["طبقه متوسط جدید", "خرده‌بورژوازی سنتی", "طبقه کارگر صنعتی", "لومپن‌پروولتاریا"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Traditional petty bourgeoisie",
        "why_plausible": "The classic merchant and artisan bazaar class supporting the clergy.",
        "why_wrong": "They formed the traditional bazaar core active from Stage I, distinct from Western-educated white-collar civil servants."
      },
      {
        "option": "Industrial working class",
        "why_plausible": "Comprised manual laborers in manufacturing plants.",
        "why_wrong": "They were blue-collar factory workers, not salaried public-sector professionals and technocrats."
      },
      {
        "option": "Lumpenproletariat",
        "why_plausible": "The marginalized urban underclass.",
        "why_wrong": "They lacked educational credentials and were frequently recruited by the regime as pro-Shah club-wielders."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Agrarian peasantry", "Comprador elite"],
      "fa": ["دهقانان", "اشراف وابسته"]
    },
    "specificity_prompt": {
      "en": "Please identify the sociological term used for salaried technocrats and public employees.",
      "fa": "لطفاً اصطلاح جامعه‌شناختی ناظر بر کارمندان و تحصیل‌کردگان شهری را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Modern middle class. Correct. The tie-wearing technocrats who stopped signing state vouchers.",
        "wrong_generic": "No. The stratum was the modern middle class (tabaqeh-ye motavasset-e jadid).",
        "common_wrong_answers": {
          "Traditional petty bourgeoisie": "The traditional petty bourgeoisie was the bazaar, not salaried ministry clerks.",
          "Industrial working class": "The working class held wrenches, not administrative stamp pads.",
          "Lumpenproletariat": "The lumpenproletariat were hired to beat protesters, not strike in ministries."
        }
      },
      "fa": {
        "correct_generic": "طبقه متوسط جدید. کاملاً درسته! همان کارمندان کراواتی که دست از امضا کردن اسناد دولتی کشیدند.",
        "wrong_generic": "خیر، پاسخ درست طبقه متوسط جدید بود. مرز میان خرده‌بورژوازی سنتی و مدرن را تشخیص نمی‌دهید.",
        "common_wrong_answers": {
          "خرده‌بورژوازی سنتی": "خرده‌بورژوازی سنتی بازار و حجره‌داران بودند، نه مهندسان و کارمندان وزارتخانه‌ها.",
          "طبقه کارگر صنعتی": "کارگران آچار به دست داشتند، این‌ها پشت میز اداری می‌نشستند.",
          "لومپن‌پروولتاریا": "لومپن‌ها پول می‌گرفتند تا چماق بزنند، پشت میز کامپیوتر نبودند."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi explain that the modern middle class was an essential latecomer to the revolution: their strikes in the central bank, customs, communications, and ministries severed state coordination.",
      "fa": "اشرف و بنوعزیزی توضیح می‌دهند که پیوستن طبقه متوسط جدید (کارمندان و تکنوکرات‌ها) در پاییز ۱۳۵۷ شریان اداری، بانکی و گمرکی رژیم شاه را قطع کرد و سقوط آن را قطعیت بخشید."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "Two other strata, the modern middle class (principally salaried workers in the public sector and members of the liberal professions) and the industrial working class, joined the revolution only in its later stages. Although they were latecomers, their contribution to the success of the revolution was critical in that they dramatically increased the opposition's economic clout.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_workers_shura_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "WORKERS OF THE REVOLUTION, UNITE!",
      "fa": "شورا به وقت کارخانه"
    },
    "clue_text": {
      "en": "According to the quantitative class analysis of Ashraf and Banuazizi, while the Pahlavi White Revolution claimed to have modernized the countryside, this demographic majority—comprising nearly 50 percent of Iran's total population in 1978—played no significant role in any phase of the revolution.",
      "fa": "بر اساس تحلیل طبقاتی کمّی اشرف و بنوعزیزی، با وجود ادعای انقلاب سفید در مدرن‌سازی روستاها، این اکثریت جمعیتی که نزدیک به نیمی از جمعیت ایران در سال ۱۳۵۷ را تشکیل می‌دادند، عملاً در هیچ‌یک از مراحل انقلاب نقش معناداری ایفا نکردند."
    },
    "canonical_answer": {
      "en": "Peasants",
      "fa": "روستاییان"
    },
    "accepted_aliases": {
      "en": ["The peasantry", "Rural population", "Peasantry", "Dehqanan", "Rural villagers"],
      "fa": ["دهقانان", "جمعیت روستایی", "کشاورزان و روستاییان", "طبقه دهقان"]
    },
    "options": {
      "en": ["Peasants", "Bazaaris", "Urban intelligentsia", "Clergy"],
      "fa": ["روستاییان", "بازاریان", "روشنفکران دانشگاهی", "روحانیون"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Bazaaris",
        "why_plausible": "A traditional class intimately connected with religious institutions.",
        "why_wrong": "The bazaaris were prime movers who organized 64 percent of mass demonstrations."
      },
      {
        "option": "Urban intelligentsia",
        "why_plausible": "Comprising students and professors staging university protests.",
        "why_wrong": "Students and teachers formed the vanguard, organizing 23 percent of demonstrations."
      },
      {
        "option": "Clergy",
        "why_plausible": "The leading religious elite mobilizing revolutionary sermons.",
        "why_wrong": "The clergy held supreme leadership and ideological control over the revolution."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Shantytown migrants", "Industrial workers"],
      "fa": ["حاشیه‌نشینان شهری", "کارگران صنعتی"]
    },
    "specificity_prompt": {
      "en": "Please state the rural agrarian class that remained largely passive throughout the revolution.",
      "fa": "لطفاً طبقه کشاورز و روستایی غیرفعال در انقلاب را نام ببرید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Peasants. Exactly. Half the population stayed in the fields while Tehran burned.",
        "wrong_generic": "No. The demographic absent from revolutionary mobilization was the peasants (dehqanan).",
        "common_wrong_answers": {
          "Bazaaris": "The bazaar funded the entire revolution; they were hardly passive.",
          "Urban intelligentsia": "The students were getting shot on campus; they were at the front lines.",
          "Clergy": "The clergy led the revolution. Pay attention to the question."
        }
      },
      "fa": {
        "correct_generic": "روستاییان. کاملاً درسته! نیمی از جمعیت کشور که در روستا ماندند و کاری به کار انقلاب شهری نداشتند.",
        "wrong_generic": "خیر، طبقه‌ای که در هیچ مرحله‌ای نقش جدی نداشت دهقانان و روستاییان بودند.",
        "common_wrong_answers": {
          "بازاریان": "بازار خرج انقلاب را داد، کجایش غایب بود؟",
          "روشنفکران دانشگاهی": "دانشجویان از سال ۵۶ در دانشگاه کتک می‌خوردند، پیشرو بودند.",
          "روحانیون": "روحانیت رهبری کل ماجرا را داشت؛ صورت مسئله را با دقت بخوانید."
        }
      }
    },
    "explanation": {
      "en": "Ashraf and Banuazizi observe a striking historical irony: despite the massive social engineering of the 1963 land reform, Iran's rural peasantry remained completely detached and passive during the revolutionary mobilization in the cities.",
      "fa": "اشرف و بنوعزیزی به این طنز تاریخی اشاره می‌کنند که به رغم اصلاحات ارضی دهه چهل، دهقانان ایرانی که نیمی از جمعیت کشور را تشکیل می‌دادند، در هیچ مرحله‌ای از انقلاب شهری مشارکت چشمگیری نداشتند."
    },
    "provenance": {
      "source_book": "State, Culture, and Society",
      "source_author": "Ahmad Ashraf and Ali Banuazizi",
      "page_number": 24,
      "verbatim_passage": "And, finally, the peasants, comprising about half of the country's population on the eve of the revolution, played no significant role in any phase of the revolution.",
      "evidence_type": "FACT"
    }
  },

  # CATEGORY 4: Double Jeopardy (Farhi: War Generation & Austerity)
  {
    "id": "double_war_austerity_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "BREAD, BARRACKS & BURNOUT",
      "fa": "سهمیه در عصر سازندگی"
    },
    "clue_text": {
      "en": "Immediately following Ayatollah Khomeini's death in 1989, President Hashemi Rafsanjani inaugurated this official policy era, signaling the end of revolutionary mobilization in favor of technocratic economic restructuring.",
      "fa": "بلافاصله پس از درگذشت آیت‌الله خمینی در سال ۱۳۶۸، رئیس‌جمهور هاشمی رفسنجانی این دوره رسمی را نام‌گذاری کرد که پایان بسیج انقلابی و آغاز بازسازی اقتصادی فن‌سالارانه را نوید می‌داد."
    },
    "canonical_answer": {
      "en": "Era of Reconstruction",
      "fa": "دوران سازندگی"
    },
    "accepted_aliases": {
      "en": ["Sazandegi", "Reconstruction Era", "Period of Reconstruction", "Dowran-e Sazandegi"],
      "fa": ["عصر سازندگی", "دولت سازندگی", "دوره سازندگی"]
    },
    "options": {
      "en": ["Era of Reconstruction", "Dialogue Among Civilizations", "Decade of Progress and Justice", "Second Step of the Revolution"],
      "fa": ["دوران سازندگی", "گفتگوی تمدن‌ها", "دهه پیشرفت و عدالت", "گام دوم انقلاب"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Dialogue Among Civilizations",
        "why_plausible": "The famous foreign policy doctrine of Mohammad Khatami in 1997.",
        "why_wrong": "Associated with Khatami's reformist presidency in the late 1990s, not Rafsanjani's 1989 economic agenda."
      },
      {
        "option": "Decade of Progress and Justice",
        "why_plausible": "An official development moniker coined by the Supreme Leader.",
        "why_wrong": "Designated in 2008 for the fourth decade of the Islamic Republic, not 1989."
      },
      {
        "option": "Second Step of the Revolution",
        "why_plausible": "A high-profile ideological manifesto issued on the 40th anniversary.",
        "why_wrong": "Issued in February 2019 by Ayatollah Khamenei, thirty years after the postwar period."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Economic Jihad", "Resistance Economy"],
      "fa": ["جهاد اقتصادی", "اقتصاد مقاومتی"]
    },
    "specificity_prompt": {
      "en": "Please provide the official political slogan for the Rafsanjani presidency.",
      "fa": "لطفاً نام مصطلح دوره ریاست‌جمهوری هاشمی رفسنجانی را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Era of Reconstruction. Correct. When building dams replaced building barricades.",
        "wrong_generic": "No. The era declared was the Era of Reconstruction (Dowran-e Sazandegi).",
        "common_wrong_answers": {
          "Dialogue Among Civilizations": "Khatami talked with civilizations; Rafsanjani poured concrete.",
          "Decade of Progress and Justice": "That was Khamenei's 2008 slogan, two decades later.",
          "Second Step of the Revolution": "The Second Step came out in 2019. Check your calendar."
        }
      },
      "fa": {
        "correct_generic": "دوران سازندگی. کاملاً درسته! زمانی که ساختن سد جایگزین سنگربندی در خیابان شد.",
        "wrong_generic": "خیر، پاسخ درست دوران سازندگی بود. القاب دولت‌های پس از جنگ را از بر نیستید.",
        "common_wrong_answers": {
          "گفتگوی تمدن‌ها": "گفتگوی تمدن‌ها شعار خاتمی بود؛ رفسنجانی پل و جاده می‌ساخت.",
          "دهه پیشرفت و عدالت": "دهه پیشرفت مال دهه چهارم انقلاب است، نه سال ۱۳۶۸.",
          "گام دوم انقلاب": "بیانیه گام دوم مال سال ۱۳۹۷ است، سی سال با دوران پس از جنگ فاصله دارد."
        }
      }
    },
    "explanation": {
      "en": "Farideh Farhi points out that Hashemi Rafsanjani's 'Era of Reconstruction' marked the transition where war veterans, previously celebrated as the vanguard of cultural purity, were abruptly recategorized as needy welfare recipients.",
      "fa": "فریده فرحی نشان می‌دهد که اعلام «دوران سازندگی» توسط رفسنجانی پایانی بر گفتمان حماسی جنگ بود و رزمندگان از الگوی طهارت انقلابی به قشر نیازمند خدمات و سهمیه بدل شدند."
    },
    "provenance": {
      "source_book": "The Antinomies of Iran's War Generation",
      "source_author": "Farideh Farhi",
      "page_number": 108,
      "verbatim_passage": "The declaration of an 'Era of Reconstruction' by Hashemi-Rafsanjani clearly suggested the end of other eras, specifically the revolution and war eras. Acknowledging the 'epic' nature of the war... Hashemi-Rafsanjani now talked about the problems and ruins left from the war era that needed to be overcome.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_war_austerity_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "BREAD, BARRACKS & BURNOUT",
      "fa": "سهمیه در عصر سازندگی"
    },
    "clue_text": {
      "en": "In the 1990s postwar era analyzed by Farhi, the state's reliance on these preferential university entrance and civil-service hiring policies turned disabled veterans and martyr families from moral heroes into objects of popular resentment.",
      "fa": "در دوران پس از جنگ به تحلیل فریده فرحی، اتکای حکومت به این امتیازات ترجیحی در کنکور دانشگاه‌ها و استخدام‌های دولتی، خانواده‌های شهدا و جانبازان را از قهرمانان معنوی به آماج خشم و کنایه جامعه تبدیل کرد."
    },
    "canonical_answer": {
      "en": "Quotas",
      "fa": "سهمیه‌ها"
    },
    "accepted_aliases": {
      "en": ["Sahmiyeh", "Veterans quotas", "Educational quotas", "University quotas", "Sahmiyeha"],
      "fa": ["سهمیه کنکور", "سهمیه ایثارگران", "سهمیه‌بندی دانشگاه‌ها"]
    },
    "options": {
      "en": ["Quotas", "Foreign scholarships", "Direct equity grants", "Exemption from income tax"],
      "fa": ["سهمیه‌ها", "بورسیه‌های اعزام به خارج", "واگذاری مستقیم سهام دولتی", "معافیت از مالیات بر درآمد"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Foreign scholarships",
        "why_plausible": "The state funded overseas doctoral studies for certain vetted candidates.",
        "why_wrong": "The primary social flashpoint for mass youth resentment was the domestic university entrance quota (sahmiyeh-ye konkūr)."
      },
      {
        "option": "Direct equity grants",
        "why_plausible": "Shares in state-owned companies granted to foundations.",
        "why_wrong": "Equity transfers (like Justice Shares) were introduced under Ahmadinejad in 2005, not the 1990s veteran friction."
      },
      {
        "option": "Exemption from income tax",
        "why_plausible": "A common economic perk for wounded service personnel.",
        "why_wrong": "Tax waivers did not displace competitive applicants from coveted university seats or spark street slogans."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Pension bonuses", "Subsidized mortgages"],
      "fa": ["حقوق بازنشستگی جانبازان", "وام‌های بلاعوض مسکن"]
    },
    "specificity_prompt": {
      "en": "Please state the Persian term for the contested university entrance and employment quotas.",
      "fa": "لطفاً اصطلاح پرمناقشه مربوط به ورود ترجیحی به دانشگاه را بیان کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Quotas (Sahmiyeh). Exactly. The single word that triggered an entire generation of Konkur test-takers.",
        "wrong_generic": "No. The contested policy was quotas (sahmiyeh).",
        "common_wrong_answers": {
          "Foreign scholarships": "Foreign trips went to diplomats' children; veterans got Konkur quotas.",
          "Direct equity grants": "Justice shares arrived under Ahmadinejad, not the 1990s reconstruction.",
          "Exemption from income tax": "Taxes didn't take away medical school seats; quotas did."
        }
      },
      "fa": {
        "correct_generic": "سهمیه‌ها. کاملاً درسته! همان واژه پرحرارتی که خواب را از چشم داوطلبان کنکور ربود.",
        "wrong_generic": "خیر، پاسخ درست سهمیه‌ها (سهمیه کنکور و ایثارگران) بود.",
        "common_wrong_answers": {
          "بورسیه‌های اعزام به خارج": "بورسیه خارج برای آقازاده‌ها بود، بچه‌های جبهه سهمیه دانشگاه داخلی گرفتند.",
          "واگذاری مستقیم سهام دولتی": "سهام عدالت مال دوره احمدی‌نژاد بود، نه دهه هفتاد.",
          "معافیت از مالیات بر درآمد": "معافیت مالیاتی کسی را در دانشکده پزشکی جابه‌جا نمی‌کرد، سهمیه می‌کرد."
        }
      }
    },
    "explanation": {
      "en": "Farhi explains how institutional quotas (sahmiyeh) transformed veterans in public perception from noble self-sacrificing volunteers into a privileged statutory interest group resented by younger peers.",
      "fa": "فریده فرحی تشریح می‌کند که چگونه اعطای سهمیه‌های دانشگاهی و استخدامی، تصویر رزمندگان را در افکار عمومی از ایثارگران مخلص به قشری برخوردار از رانت دولتی تغییر داد و شکاف نسلی عمیقی ایجاد کرد."
    },
    "provenance": {
      "source_book": "The Antinomies of Iran's War Generation",
      "source_author": "Farideh Farhi",
      "page_number": 108,
      "verbatim_passage": "families of the martyrs, the disabled war veterans, the freed prisoners of war, and those who sacrificed for the war, rather than being the source for the moral revitalization of the cities... became 'victims' and social categories in need of help, services, and special quotas (sahmiyeh). In turn, they became subjects of resentment on the part of others who felt left out of opportunities to enter universities or find employment.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_war_austerity_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "BREAD, BARRACKS & BURNOUT",
      "fa": "سهمیه در عصر سازندگی"
    },
    "clue_text": {
      "en": "In a blistering public letter addressed to President Mohammad Khatami after the 2001 election, the wife of a veteran classified in this medical-neurological category bitterly contrasted the youth dancing at reformist rallies with her husband's untreated trauma.",
      "fa": "در نامه‌ای تند خطاب به رئیس‌جمهور محمد خاتمی پس از انتخابات ۱۳۸۰، همسر جانبازی در این دسته پزشکی-عصبی، شادی و پایکوبی جوانان در میتینگ‌های اصلاح‌طلبان را با رنج و ترومای درمان‌نشده همسرش مقایسه کرد."
    },
    "canonical_answer": {
      "en": "Neurologically and psychologically disabled",
      "fa": "جانباز اعصاب و روان"
    },
    "accepted_aliases": {
      "en": ["Janbaz-e asab va ravan", "Nerve and psychological veteran", "Psychologically disabled veteran", "PTSD veterans"],
      "fa": ["جانبازان اعصاب و روان", "ایثارگر اعصاب و روان", "جانباز اعصاب"]
    },
    "options": {
      "en": ["Neurologically and psychologically disabled", "Chemical warfare victim", "Amputee veteran", "Blinded combatant"],
      "fa": ["جانباز اعصاب و روان", "جانباز شیمیایی", "جانباز قطع نخاعی", "جانباز روشندل"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Chemical warfare victim",
        "why_plausible": "Tens of thousands suffered from Iraqi mustard gas and nerve agent attacks.",
        "why_wrong": "The letter cited by Farhi specifically spoke for the spouses of psychologically and neurologically traumatized veterans (asab va ravan)."
      },
      {
        "option": "Amputee veteran",
        "why_plausible": "Combatants suffering physical limb loss from mines and artillery.",
        "why_wrong": "Physical amputees received different foundation classifications; the letter focused on psychological trauma."
      },
      {
        "option": "Blinded combatant",
        "why_plausible": "Shrapnel-induced sensory loss common among frontline sappers.",
        "why_wrong": "The letter addressed the hidden psychiatric and nervous wounds ignored amidst urban consumerism."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Prisoner of war", "Unidentified casualty"],
      "fa": ["آزاده دفاع مقدس", "شهید گمنام"]
    },
    "specificity_prompt": {
      "en": "Please provide the Persian clinical designation for veterans suffering from combat psychological trauma.",
      "fa": "لطفاً اصطلاح دقیق بالینی مربوط به جانبازان دچار شوک روانی ناشی از جنگ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Neurologically and psychologically disabled (Janbaz-e asab va ravan). Quite right. The tragic human wreckage left behind by eight years of shelling.",
        "wrong_generic": "No. The category was Janbaz-e asab va ravan (neurologically and psychologically disabled).",
        "common_wrong_answers": {
          "Chemical warfare victim": "Chemical victims suffered lung damage; this letter was about mental trauma.",
          "Amputee veteran": "Amputees lost limbs; these veterans were battling shell shock and PTSD.",
          "Blinded combatant": "Blindness was physical; asab va ravan was psychological devastation."
        }
      },
      "fa": {
        "correct_generic": "جانباز اعصاب و روان. کاملاً درسته! تلخ‌ترین یادگار هشت سال خمپاره و موج انفجار در گوشه آسایشگاه‌ها.",
        "wrong_generic": "خیر، جانباز اعصاب و روان پاسخ درست بود. گروه‌های آسیب‌دیده جنگ را تفکیک کنید.",
        "common_wrong_answers": {
          "جانباز شیمیایی": "جانبازان شیمیایی ریه‌شان تاول زد، این نامه درباره شوک روانی و روحی بود.",
          "جانباز قطع نخاعی": "جانباز قطع نخاع آسیب جسمی داشت، بحث اینجا ترومای روانی پس از سانحه بود.",
          "جانباز روشندل": "روشندل بینایی را از دست داد، اعصاب و روان با کابوس‌های شبانه جنگ دست به گریبان بود."
        }
      }
    },
    "explanation": {
      "en": "Farhi analyzes the poignant letter published in Ya Lessarat from the wife of a Janbaz-e asab va ravan living in Shahrak-e Shahid Mahallati, exposing the raw ideological resentment felt by traumatized veteran families toward the liberalizing middle classes.",
      "fa": "فریده فرحی نامه همسر جانباز اعصاب و روان در شهرک شهید محلاتی را تحلیل می‌کند که چگونه تضاد میان فقر خانواده‌های جنگ‌زده و رفاه‌طلبی جوانان شهری، سوخت موتور خشونت نیروهای انصار حزب‌الله شد."
    },
    "provenance": {
      "source_book": "The Antinomies of Iran's War Generation",
      "source_author": "Farideh Farhi",
      "page_number": 102,
      "verbatim_passage": "In an accusing letter to President Khatami, and while articulating a series of grievances about the dire economic condition of her husband and family, a reported wife of a 'neurologically and psychologically disabled war veteran' (Janbaz-e asab va ravan) bluntly asks whether Khatami has an explanation for the political rallies with 'dancing and celebrations'.",
      "evidence_type": "PRIMARY_TESTIMONY"
    }
  },
  {
    "id": "double_war_austerity_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "BREAD, BARRACKS & BURNOUT",
      "fa": "سهمیه در عصر سازندگی"
    },
    "clue_text": {
      "en": "In analyzing the cultural mobilization of the Iran-Iraq War, this political theorist argued that the state constructed a 'unitary consciousness' wherein worship was defined through combat, and questioning authority was treated as succumbing to passion.",
      "fa": "این نظریه‌پرداز و جامعه‌شناس سیاسی در تحلیل بسیج فرهنگی جنگ استدلال کرد که حکومت یک «آگاهی یگانه» برساخت که در آن عبادت با نبرد تعریف می‌شد و هرگونه پرسش از رهبری، تسلیم شدن در برابر هوای نفس تلقی می‌گردید."
    },
    "canonical_answer": {
      "en": "Mohammad-Javad Gholamreza-Kashi",
      "fa": "محمدجواد غلامرضاکاشی"
    },
    "accepted_aliases": {
      "en": ["Gholamreza Kashi", "Mohammad-Javad Kashi", "Javad Kashi", "Gholamreza-Kashi"],
      "fa": ["غلامرضا کاشی", "جواد کاشی", "محمدجواد کاشی"]
    },
    "options": {
      "en": ["Mohammad-Javad Gholamreza-Kashi", "Abdolkarim Soroush", "Mostafa Malekian", "Saeed Hajjarian"],
      "fa": ["محمدجواد غلامرضاکاشی", "عبدالکریم سروش", "مصطفی ملکیان", "سعید حجاریان"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Abdolkarim Soroush",
        "why_plausible": "The leading philosopher of religious reformism in 1990s Iran.",
        "why_wrong": "Soroush focused on religious epistemology and pluralism (*Qabz va Bast*), not analyzing the wartime 'unitary consciousness' discourse."
      },
      {
        "option": "Mostafa Malekian",
        "why_plausible": "A prominent contemporary philosopher of ethics and spirituality.",
        "why_wrong": "Malekian addressed spirituality and rationality, rather than sociological critiques of wartime mobilization culture."
      },
      {
        "option": "Saeed Hajjarian",
        "why_plausible": "The master political strategist behind Khatami's reform movement.",
        "why_wrong": "Hajjarian wrote on dual sovereignty and political development, not the cultural discourse analyzed by Farhi."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Hossein Bashiriyeh", "Hatam Ghaderi"],
      "fa": ["حسین بشیریه", "حاتم قادری"]
    },
    "specificity_prompt": {
      "en": "Please provide the name of the political scientist who formulated the concept of unitary consciousness.",
      "fa": "لطفاً نام جامعه‌شناس سیاسی ارائه‌دهنده نظریه آگاهی یگانه در فرهنگ جنگ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Mohammad-Javad Gholamreza-Kashi. Spot on. You actually read Farhi's theoretical framework.",
        "wrong_generic": "No. The political theorist was Mohammad-Javad Gholamreza-Kashi.",
        "common_wrong_answers": {
          "Abdolkarim Soroush": "Soroush wrote on hermeneutics, not the wartime culture of self-denial.",
          "Mostafa Malekian": "Malekian teaches ethics; Kashi dissected the war machine.",
          "Saeed Hajjarian": "Hajjarian was plotting reformist ballots, not studying wartime semiotics."
        }
      },
      "fa": {
        "correct_generic": "محمدجواد غلامرضاکاشی. کاملاً درسته! استاد جامعه‌شناسی که ساختار تک‌صدایی فرهنگ جبهه را کالبدشکافی کرد.",
        "wrong_generic": "خیر، تحلیل‌گر مفهوم آگاهی یگانه در متن مقاله، دکتر محمدجواد غلامرضاکاشی بود.",
        "common_wrong_answers": {
          "عبدالکریم سروش": "سروش قبض و بسط تئوریک شریعت می‌نوشت، نه نقد گفتمان جنگ.",
          "مصطفی ملکیان": "ملکیان مروج عقلانیت و معنویت بود، کار تحلیلی روی متن جنگ نکرده بود.",
          "سعید حجاریان": "حجاریان تئوریسین فتح سنگر به سنگر بود، نه تحلیل‌گر نشانه شناختی فرهنگ جبهه."
        }
      }
    },
    "explanation": {
      "en": "Farhi draws upon political scientist Mohammad-Javad Gholamreza-Kashi's discourse analysis to demonstrate how the war established a totalizing moral framework that branded dissent or material questioning as betrayal of the sacred.",
      "fa": "فرحی با تکیه بر آرا و مقالات دکتر غلامرضاکاشی نشان می‌دهد که چگونه گفتمان رسمی جنگ با حاکم کردن «آگاهی یگانه»، هرگونه نقد اجتماعی یا مطالبه رفاهی را به عنوان معصیت و دنیاطلبی سرکوب می‌کرد."
    },
    "provenance": {
      "source_book": "The Antinomies of Iran's War Generation",
      "source_author": "Farideh Farhi",
      "page_number": 104,
      "verbatim_passage": "Mohammad-Javad Gholamreza Kashi identifies emphasis on Shi‘i values, Shi‘i-generated epic aspects of the war, mourning, opposition to existing values in the city, martyrdom, action as opposed to words, purity and devotion, and spiritual rewards in the afterlife as the most important elements of the culture of war propagated by the war machine in Iran.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_war_austerity_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "BREAD, BARRACKS & BURNOUT",
      "fa": "سهمیه در عصر سازندگی"
    },
    "clue_text": {
      "en": "According to Mohammad Dorudian of the IRGC Center for War Studies, the volunteer forces evolved across three distinct waves, with the tragic final phase around Resolution 598 seeing the arrival of this specific label of individuals seeking post-war state benefits.",
      "fa": "بر اساس تحلیل محمد درودیان از مرکز مطالعات و تحقیقات جنگ سپاه، نیروهای داوطلب در سه موج تاریخی دگرگون شدند و در واپسین مرحله مقارن با قطعنامه ۵۹۸، پای این دسته از افراد برای دستیابی به امتیازات پس از جنگ به جبهه باز شد."
    },
    "canonical_answer": {
      "en": "Opportunists",
      "fa": "فرصت‌طلبان"
    },
    "accepted_aliases": {
      "en": ["The opportunists", "Opportunist wave", "Forsat-talaban", "Forsat-talab"],
      "fa": ["فرصت‌طلب‌ها", "داوطلبان فرصت‌طلب", "فرصت‌طلبان رانت‌جو"]
    },
    "options": {
      "en": ["Opportunists", "Conscripted regulars", "Foreign mercenaries", "Penitents"],
      "fa": ["فرصت‌طلبان", "سربازان وظیفه اجباری", "مزدوران خارجی", "توابین"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Conscripted regulars",
        "why_plausible": "Draftees served alongside volunteers throughout the conflict.",
        "why_wrong": "Draftees were part of standard military conscription, not the voluntary enlistment wave described by Dorudian."
      },
      {
        "option": "Foreign mercenaries",
        "why_plausible": "Foreign Shi'i volunteer brigades operated in certain theaters.",
        "why_wrong": "The third wave analyzed by Dorudian specifically refers to domestic Iranian opportunists positioning themselves for state benefits."
      },
      {
        "option": "Penitents",
        "why_plausible": "Former dissidents or criminals seeking political rehabilitation.",
        "why_wrong": "Tavvabin was a prison rehabilitation category, not Dorudian's term for late wartime bonus-seekers."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Careerists", "Ideologues"],
      "fa": ["کارمندان اداری", "ایدئولوگ‌ها"]
    },
    "specificity_prompt": {
      "en": "Please provide the exact term used by Dorudian for those joining at the tail end of the war for personal advantage.",
      "fa": "لطفاً واژه دقیق به کار رفته توسط درودیان برای داوطلبان اواخر جنگ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Opportunists (Forsat-talaban). Spot on. Jumping into uniform right before the ceasefire whistle to claim the pension.",
        "wrong_generic": "No. Dorudian called them opportunists (forsat-talaban).",
        "common_wrong_answers": {
          "Conscripted regulars": "Draftees had no choice; opportunists joined willingly for future quotas.",
          "Foreign mercenaries": "No foreign mercenaries; these were domestic opportunists looking for perks.",
          "Penitents": "Tawwabin were in Evin prison, not Dorudian's late volunteer wave."
        }
      },
      "fa": {
        "correct_generic": "فرصت‌طلبان. کاملاً درسته! کسانی که دقیقه نود پوتین پوشیدند تا سهمیه دانشگاه و کارت ایثارگری پس از جنگ را جمع کنند.",
        "wrong_generic": "خیر، تعبیر دقیق محمد درودیان «فرصت‌طلبان» بود. جزئیات متن تاریخ جنگ را دقت کنید.",
        "common_wrong_answers": {
          "سربازان وظیفه اجباری": "سرباز وظیفه به حکم قانون رفت، این‌ها داوطلبانه برای رانت آینده رفتند.",
          "مزدوران خارجی": "مزدور خارجی نبودند؛ ایرانیان فرصت‌طلبی بودند که بوی سهمیه را شنیده بودند.",
          "توابین": "توابین در زندان اوین بودند، ربطی به تحلیل امواج اعزام رزمندگان درودیان نداشت."
        }
      }
    },
    "explanation": {
      "en": "Farhi quotes IRGC military historian Mohammad Dorudian, who observed that the final phase of war mobilization before and after Resolution 598 unfortunately attracted opportunists who foresaw the immense social and material dividends of veteran status in the postwar Islamic Republic.",
      "fa": "فریده فرحی به نقل از محمد درودیان (از پژوهشگران برجسته جنگ در سپاه) یادآور می‌شود که در مرحله پایانی جنگ هم‌زمان با پذیرش قطعنامه، دسته‌ای از فرصت‌طلبان وارد جبهه شدند تا پس از پایان درگیری‌ها، از سهمیه‌ها و مزایای ایثارگری دولتی بهره‌مند گردند."
    },
    "provenance": {
      "source_book": "The Antinomies of Iran's War Generation",
      "source_author": "Farideh Farhi",
      "page_number": 109,
      "verbatim_passage": "Dorudian maintains that the very last stages of the war even included a number of 'opportunists' who, realizing the potential benefits of identifying themselves as [veterans]... rushed to the front.",
      "evidence_type": "INTERPRETATION"
    }
  }
]

print(f"Validating and appending {len(clues)} new clues...")
append_validated_clues(clues)
print("Done!")
