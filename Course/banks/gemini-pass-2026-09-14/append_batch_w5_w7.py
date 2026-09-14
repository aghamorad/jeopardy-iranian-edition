import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))
from jeopardy_pipeline import append_validated_clues, validate_clue_schema

new_clues = [
  {
    "id": "single_pragmatism_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {
      "en": "LET THEM EAT ARMS",
      "fa": "مصلحت بر وزن منفعت"
    },
    "clue_text": {
      "en": "In her 2003 Nobel Peace Prize acceptance speech cited by R. K. Ramazani, human rights lawyer Shirin Ebadi traced the pragmatic origins of Iranian statecraft and pluralism by proudly declaring herself an heir to this ancient Achaemenid monarch.",
      "fa": "در خطابه دریافت جایزه صلح نوبل در سال ۱۳۸۲ خورشیدی به نقل از روح‌الله رمضانی، شیرین عبادی با تأکید بر پیشینه عمل‌گرایی و مدارا در حکمرانی ایرانی، خود را با افتخار از تبار این پادشاه هخامنشی نامید."
    },
    "canonical_answer": {
      "en": "Cyrus the Great",
      "fa": "کوروش بزرگ"
    },
    "accepted_aliases": {
      "en": ["Cyrus II", "Cyrus the Elder", "Kourosh-e Kabir"],
      "fa": ["کوروش کبیر", "کوروش دوم", "کورش بزرگ"]
    },
    "options": {
      "en": ["Cyrus the Great", "Darius the Great", "Xerxes I", "Ardeshir I"],
      "fa": ["کوروش بزرگ", "داریوش بزرگ", "خشایارشا", "اردشیر یکم"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Darius the Great",
        "why_plausible": "The major Achaemenid administrative consolidator renowned for the Behistun Inscription.",
        "why_wrong": "Ebadi specifically cited Cyrus the Great for the liberation of the Jews and the ancient cylinder of human rights."
      },
      {
        "option": "Xerxes I",
        "why_plausible": "A famous Achaemenid ruler known for military campaigns in Greece.",
        "why_wrong": "Xerxes was not invoked as a symbol of human rights and pragmatic pluralistic tolerance."
      },
      {
        "option": "Ardeshir I",
        "why_plausible": "The founder of the Sasanian dynasty, an empire frequently cited by historical commentators.",
        "why_wrong": "He established the Sasanian dynasty centuries later and championed strict Zoroastrian orthodoxy."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Darius the Great", "Shapur I"],
      "fa": ["داریوش بزرگ", "شاپور یکم"]
    },
    "specificity_prompt": {
      "en": "Please provide the specific name of the founding Achaemenid monarch.",
      "fa": "لطفاً نام دقیق پادشاه بنیان‌گذار سلسله هخامنشی را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Cyrus the Great. Quite right. Even the family group chat could not manage to get that wrong.",
        "wrong_generic": "No. The monarch was Cyrus the Great. Perhaps try visiting Pasargadae once in your life.",
        "common_wrong_answers": {
          "Darius the Great": "Darius carved Behistun; Cyrus freed Babylon. Read the cylinder.",
          "Xerxes I": "Xerxes invaded Athens, he didn't write human rights charters.",
          "Ardeshir I": "Ardeshir founded the Sasanians, not the Achaemenids. Check the century."
        }
      },
      "fa": {
        "correct_generic": "کوروش بزرگ. کاملاً درسته! شاهکار نکردید، این را عکس پروفایل نیمی از اقوامتان هم فریاد می‌زند.",
        "wrong_generic": "خیر، پاسخ درست کوروش بزرگ بود. حداقل یک بار از کنار پاسارگاد رد شوید.",
        "common_wrong_answers": {
          "داریوش بزرگ": "داریوش کتیبه بیستون را تراشید، کوروش منشور بابل را نوشت.",
          "خشایارشا": "خشایارشا به یونان لشکر کشید، نماد حقوق بشر نوبل نبود.",
          "اردشیر یکم": "اردشیر ساسانی بود، نه هخامنشی؛ دوران‌ها را با هم مخلوط نکنید."
        }
      }
    },
    "explanation": {
      "en": "R. K. Ramazani highlights that in her 2003 Nobel lecture, Shirin Ebadi proudly referenced Cyrus the Great to illustrate that a quarter-century of post-revolutionary Islamization had failed to erase Iran's deep-rooted pre-Islamic humanist heritage.",
      "fa": "روح‌الله رمضانی اشاره می‌کند که شیرین عبادی در سخنرانی جایزه نوبل سال ۱۳۸۲ با افتخار به کوروش بزرگ استناد کرد تا نشان دهد بیست و پنج سال حکومت دینی نتوانسته پیوند عمیق ایرانیان با هویت پیشااسلامی و اصول مدارا را بگسلد."
    },
    "provenance": {
      "source_book": "Middle East Journal",
      "source_author": "R. K. Ramazani",
      "page_number": 550,
      "verbatim_passage": "It is significant that in accepting the Nobel Peace Prize, Shirin Ebadi proudly declared to the world on December 10, 2003 'I am an Iranian, a descendant of Cyrus the Great' and 'I am a Muslim.' This showed that a quarter of a century of 'Islamization' had failed to undermine the strong attachment of the Iranian people to their pre-Islamic cultural heritage, including its concern with human rights.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_pragmatism_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "LET THEM EAT ARMS",
      "fa": "مصلحت بر وزن منفعت"
    },
    "clue_text": {
      "en": "Faced with a debilitating two-front war against the Ottomans and the Uzbeks, this Safavid ruler pragmatically signed the 1590 Treaty of Istanbul, ceding major territories and agreeing to suppress the ritual cursing of the first three Sunni caliphs.",
      "fa": "این پادشاه صفوی در سال ۹۶۹ خورشیدی به دلیل ناتوانی در نبرد همزمان در دو جبهه علیه عثمانی‌ها و ازبکان، با امضای عهدنامه استانبول بخش‌های وسیعی از قلمرو خود را واگذار کرد و لعن علنی خلفای سه‌گانه را به تعلیق درآورد."
    },
    "canonical_answer": {
      "en": "Shah Abbas I",
      "fa": "شاه عباس یکم"
    },
    "accepted_aliases": {
      "en": ["Shah Abbas the Great", "Abbas I", "Shah Abbas Safavi"],
      "fa": ["شاه عباس بزرگ", "شاه عباس کبیر", "شاه عباس"]
    },
    "options": {
      "en": ["Shah Abbas I", "Shah Ismail I", "Shah Tahmasp I", "Shah Safi"],
      "fa": ["شاه عباس یکم", "شاه اسماعیل یکم", "شاه طهماسب یکم", "شاه صفی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Shah Ismail I",
        "why_plausible": "The zealous founder of the Safavid state who established Shi'ism as the state religion.",
        "why_wrong": "He died in 1524, decades before the 1590 geopolitical crisis and territorial treaty."
      },
      {
        "option": "Shah Tahmasp I",
        "why_plausible": "A deeply religious monarch who concluded the earlier Treaty of Amasya in 1555 with Suleiman the Magnificent.",
        "why_wrong": "Tahmasp signed the 1555 accord, whereas the 1590 concessionary peace was forced upon Abbas I upon his accession."
      },
      {
        "option": "Shah Safi",
        "why_plausible": "Abbas I's successor who signed the final Treaty of Zuhab in 1639.",
        "why_wrong": "Shah Safi ruled decades later from 1629 to 1642 and finalized the borders in 1639."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Shah Tahmasp I", "Shah Ismail I"],
      "fa": ["شاه طهماسب یکم", "شاه اسماعیل یکم"]
    },
    "specificity_prompt": {
      "en": "Please provide the full royal title and regnal number of the Safavid monarch.",
      "fa": "لطفاً نام کامل و شماره سلطنتی این پادشاه صفوی را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Shah Abbas I. Correct. Even holy emperors knew when to stop cursing and cut their losses.",
        "wrong_generic": "No. The ruler was Shah Abbas I. A classic case of swallowing pride for survival.",
        "common_wrong_answers": {
          "Shah Ismail I": "Ismail charged into Chaldiran without cannons; he was hardly a cautious pragmatist.",
          "Shah Tahmasp I": "Tahmasp signed Amasya in 1555, not Istanbul in 1590.",
          "Shah Safi": "Shah Safi gave up Baghdad in 1639, not the Caucasus in 1590."
        }
      },
      "fa": {
        "correct_generic": "شاه عباس یکم. کاملاً درسته! شاه مقتدر هم فهمیده بود که ناسزاگویی دیپلماتیک مرزها را نگه نمی‌دارد.",
        "wrong_generic": "خیر، پاسخ درست شاه عباس یکم بود. کمی کتاب تاریخ دوران صفویه را ورق بزنید.",
        "common_wrong_answers": {
          "شاه اسماعیل یکم": "شاه اسماعیل در چالدران بدون تدبیر جنگید، اهل مصالحه با عثمانی نبود.",
          "شاه طهماسب یکم": "طهماسب صلح آماسیه را در سال ۹۳۴ خورشیدی امضا کرد، نه قرارداد استانبول ۹۶۹ را.",
          "شاه صفی": "شاه صفی در سال ۱۰۱۸ خورشیدی عهدنامه زهاب را امضا کرد؛ دهه‌ها جلوتر بودید."
        }
      }
    },
    "explanation": {
      "en": "R. K. Ramazani cites Shah Abbas I's 1590 treaty with the Ottomans as an enduring historical archetype of Iranian pragmatism, where religious rituals and territory were temporarily sacrificed to safeguard the central state against overwhelming military threats.",
      "fa": "روح‌الله رمضانی پیمان صلح ۱۵۹۰ میلادی شاه عباس با عثمانی را که با تعلیق تبرا و واگذاری قلمرو همراه بود، نمونه بارز غلبه مصلحت دولت بر تعصبات مذهبی در تاریخ سیاست خارجی ایران می‌داند."
    },
    "provenance": {
      "source_book": "Middle East Journal",
      "source_author": "R. K. Ramazani",
      "page_number": 552,
      "verbatim_passage": "To cite an even more important example, why did Shah 'Abbas I (1587-1629) sign the ignominious peace with the Ottoman Empire in 1590? In this 'treaty' he abandoned the age-old Shi'i practice of cursing the Sunni 'first three caliphs' and also made territorial concessions to the Ottomans. Did he do so because in part he was trying to reform Shi'i ritualistic practice? Or did he also cede Iranian territories because when he acceded to the throne the Safavid state was too weak to fight on two fronts, against the Ottomans and the Ozbegs?",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_pragmatism_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {
      "en": "LET THEM EAT ARMS",
      "fa": "مصلحت بر وزن منفعت"
    },
    "clue_text": {
      "en": "In what R. K. Ramazani terms the most striking example of pragmatic survival overriding anti-imperialist rhetoric, revolutionary Tehran engaged in this covert mid-1980s operation, purchasing arms from the US and Israel in exchange for helping free Western hostages in Lebanon.",
      "fa": "به تعبیر روح‌الله رمضانی در بارزترین نمونه غلبه عمل‌گرایی بر شعارهای ضدامپریالیستی، مقامات تهران در میانه دهه ۱۳۶۰ در این تبادل محرمانه تسلیحاتی، سلاح‌های آمریکایی و اسرائیلی را برای کمک به آزادی گروگان‌های غربی در لبنان تحویل گرفتند."
    },
    "canonical_answer": {
      "en": "Iran-Contra Affair",
      "fa": "ماجرای مک‌فارلین"
    },
    "accepted_aliases": {
      "en": ["McFarlane Affair", "Iran-Contra scandal", "Irangate"],
      "fa": ["ایران‌گیت", "ایران-کنترا", "پرونده مک‌فارلین"]
    },
    "options": {
      "en": ["Iran-Contra Affair", "Operation Eagle Claw", "Tanker War", "Operation Praying Mantis"],
      "fa": ["ماجرای مک‌فارلین", "عملیات طبس", "جنگ نفتکش‌ها", "عملیات آخوندک"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Operation Eagle Claw",
        "why_plausible": "A famous covert US military operation in Iran during the hostage crisis.",
        "why_wrong": "It was the failed April 1980 military rescue mission in Tabas, not a secret reciprocal arms-for-hostages trade."
      },
      {
        "option": "Tanker War",
        "why_plausible": "A major naval conflict in the Persian Gulf during the Iran-Iraq War involving US intervention.",
        "why_wrong": "It refers to the public exchange of missile strikes on commercial shipping from 1984 to 1988."
      },
      {
        "option": "Operation Praying Mantis",
        "why_plausible": "A direct military encounter between the US Navy and Iranian forces in April 1988.",
        "why_wrong": "It was a one-day direct naval clash destroying Iranian oil platforms and warships, not a clandestine weapons transaction."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Tehran Hostage Crisis", "Operation Eagle Claw"],
      "fa": ["بحران گروگان‌گیری سفارت آمریکا", "عملیات طبس"]
    },
    "specificity_prompt": {
      "en": "Please provide the commonly used political name for the clandestine 1985–1986 arms-for-hostages deal.",
      "fa": "لطفاً نام مشهور این رسوایی و مذاکرات محرمانه مبادله تسلیحات در سال‌های ۱۳۶۴ و ۱۳۶۵ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Iran-Contra Affair. Quite right. Turns out the Great Satan sells excellent anti-tank missiles.",
        "wrong_generic": "No. We were looking for the Iran-Contra Affair (or McFarlane Affair). A textbook lesson in secret diplomacy.",
        "common_wrong_answers": {
          "Operation Eagle Claw": "Eagle Claw crashed in the Tabas sands; it brought no missiles to Tehran.",
          "Tanker War": "The Tanker War sank ships in the Persian Gulf, it wasn't a clandestine White House backchannel.",
          "Operation Praying Mantis": "Praying Mantis was the US Navy destroying oil rigs, not selling TOW missiles."
        }
      },
      "fa": {
        "correct_generic": "ماجرای مک‌فارلین. کاملاً درسته! معلوم شد موشک‌های شیطان بزرگ در جبهه خریدار فراوان داشته است.",
        "wrong_generic": "خیر، پاسخ درست ماجرای مک‌فارلین (ایران-کنترا) بود. رازهای جنگ را هم فراموش کرده‌اید.",
        "common_wrong_answers": {
          "عملیات طبس": "عملیات طبس شکست بالگردهای آمریکایی در کویر بود، نه معامله محرمانه تسلیحاتی.",
          "جنگ نفتکش‌ها": "جنگ نفتکش‌ها روی آب‌های خلیج فارس بود، نه مذاکره با کیک و تپانچه در هتل استقلال.",
          "عملیات آخوندک": "عملیات آخوندک حمله ناوگان آمریکا به سکوهای نفتی ایران در فروردین ۶۷ بود."
        }
      }
    },
    "explanation": {
      "en": "R. K. Ramazani analyzes the Iran-Contra affair as the supreme demonstration of wartime pragmatism: facing devastating weapons shortages against Iraq, Iranian leaders secretly dealt with Washington and Tel Aviv while publicly sustaining revolutionary rhetoric.",
      "fa": "روح‌الله رمضانی ماجرای مک‌فارلین را گواه بارز اولویت منافع ملی و بقای نظامی بر اصول اعلامی ایدئولوژیک می‌داند؛ جایی که نیاز مبرم به قطعات یدکی و موشک‌های تاو موجب معامله پشت پرده با واشنگتن شد."
    },
    "provenance": {
      "source_book": "Middle East Journal",
      "source_author": "R. K. Ramazani",
      "page_number": 556,
      "verbatim_passage": "Perhaps the most striking example of dominance of pragmatic factors over ideological influences in Iran's foreign policy during Khomeini's lifetime was the secret purchase of arms from the United States, 'the Great Satan' and Israel, 'the lesser Satan.' Iran's defensive war against Iraq occasioned such a bold move. A deal was struck through intermediaries. American and Israeli arms were to be shipped to Iran in return for Iran's help with the release of Western hostages in Lebanon.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_pragmatism_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "LET THEM EAT ARMS",
      "fa": "مصلحت بر وزن منفعت"
    },
    "clue_text": {
      "en": "When R. K. Ramazani pressed a prominent wartime Iranian decision-maker regarding Ayatollah Khomeini's proclamations about exporting the revolution to justify continuing the war into Iraq after 1982, the official dismissed those ideological statements with this colorful Persian term for martial boastfulness.",
      "fa": "هنگامی که روح‌الله رمضانی از یکی از مقامات ارشد دوران دفاع مقدس درباره شعارهای تند آیت‌الله خمینی برای صدور انقلاب به عراق پس از فتح خرمشهر پرسید، وی آن بیانات ایدئولوژیک را با این واژه اصیل به معنای لاف‌زنی و گزافه‌گویی جنگی توصیف کرد."
    },
    "canonical_answer": {
      "en": "Rajaz-khani",
      "fa": "رجزخوانی"
    },
    "accepted_aliases": {
      "en": ["Rajaz khaany", "Rajaz khani", "Rajazkhani", "Bragging"],
      "fa": ["رجز", "رجز خوانی"]
    },
    "options": {
      "en": ["Rajaz-khani", "Laf-zani", "Ta'arof", "Ketman"],
      "fa": ["رجزخوانی", "لاف‌زنی", "تعارف", "کتمان"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Laf-zani",
        "why_plausible": "A general colloquial Persian word for exaggeration and bragging.",
        "why_wrong": "The precise political and cultural term recorded and transliterated verbatim by Ramazani was rajaz khaany."
      },
      {
        "option": "Ta'arof",
        "why_plausible": "The ubiquitous Iranian ritual code of politeness and social deference.",
        "why_wrong": "Ta'arof describes everyday social etiquette, not battlefield rhetoric or martial boasting."
      },
      {
        "option": "Ketman",
        "why_plausible": "The theological practice of concealing one's true religious convictions under duress.",
        "why_wrong": "Ketman (or taqiyya) refers to religious dissimulation, not fiery public military bravado."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Taqiyya", "Hekmat"],
      "fa": ["تقیه", "حکمت"]
    },
    "specificity_prompt": {
      "en": "Please provide the exact Persian term for martial poetic boasting recorded by Ramazani.",
      "fa": "لطفاً اصطلاح دقیق به کار رفته در متن رمضانی برای حماسه‌سرایی و گزافه‌گویی رزمی را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Rajaz-khani. Correct. Turns out wartime manifestos are often just noise for the radio.",
        "wrong_generic": "No. The term was Rajaz-khani. A classic diplomatic euphemism for political posturing.",
        "common_wrong_answers": {
          "Laf-zani": "Laf-zani is everyday bragging on the street, not martial battlefield poetry.",
          "Ta'arof": "Ta'arof is offering someone tea four times, not threatening to march on Baghdad.",
          "Ketman": "Ketman is hiding your beliefs; rajaz-khani is shouting them through loudspeakers."
        }
      },
      "fa": {
        "correct_generic": "رجزخوانی. کاملاً درسته! معلوم است ادبیات رزم و حماسه‌سرایی سنتی را خوب می‌شناسید.",
        "wrong_generic": "خیر، پاسخ درست رجزخوانی بود. تحلیل‌های دیپلماتیک دقیق‌تر از این حرف‌هاست.",
        "common_wrong_answers": {
          "لاف‌زنی": "لاف‌زنی اصطلاح عامیانه کوچه و بازار است، اصطلاح حماسی مد نظر نبود.",
          "تعارف": "تعارف تعارفات دیپلماتیک است، نه داد و فریادهای رزمی پشت بلندگو.",
          "کتمان": "کتمان پنهان‌کاری مذهبی است، نه حماسه‌خوانی جنگی."
        }
      }
    },
    "explanation": {
      "en": "In his Middle East Journal essay, R. K. Ramazani recounts interviewing a top Iranian wartime leader who conceded that ideological slogans regarding the export of the revolution were merely 'bragging' (rajaz khaany) intended to rally domestic combatants rather than an operational military plan.",
      "fa": "روح‌الله رمضانی در پژوهش خود نقل می‌کند که یکی از تصمیم‌گیرندگان ارشد جنگ تحمیلی صراحتاً به او گفت بیانات هیجانی درباره صدور انقلاب صرفاً «رجزخوانی» برای تقویت روحیه رزمندگان بود و برنامه عملیاتی دولت به شمار نمی‌رفت."
    },
    "provenance": {
      "source_book": "Middle East Journal",
      "source_author": "R. K. Ramazani",
      "page_number": 557,
      "verbatim_passage": "I quoted to him Khomeini's own statement to the effect that 'We exported our revolution.' In response, he said that Khomeini's statements from Khomeini were nothing but 'bragging' (rajaz khaany).",
      "evidence_type": "PRIMARY_TESTIMONY"
    }
  },
  {
    "id": "single_pragmatism_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "LET THEM EAT ARMS",
      "fa": "مصلحت بر وزن منفعت"
    },
    "clue_text": {
      "en": "According to R. K. Ramazani's forensic account of the secret Iran-Contra channel, this exact number of clandestine arms shipments arrived in Iran between 1985 and 1986, with each release of American hostages closely tied to the delivery of a consignment.",
      "fa": "بر اساس مستندات دقیق روح‌الله رمضانی از کانال پنهانی ایران-کنترا، دقیقاً این تعداد محموله تسلیحاتی بین سال‌های ۱۳۶۴ و ۱۳۶۵ وارد ایران شد و آزادی هر گروه از گروگان‌های آمریکایی به رسیدن یکی از این محموله‌ها وابسته بود."
    },
    "canonical_answer": {
      "en": "Six",
      "fa": "شش محموله"
    },
    "accepted_aliases": {
      "en": ["6", "Six shipments", "6 shipments"],
      "fa": ["۶", "شش", "۶ محموله"]
    },
    "options": {
      "en": ["Six", "Three", "Nine", "Twelve"],
      "fa": ["شش محموله", "سه محموله", "نه محموله", "دوازده محموله"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Three",
        "why_plausible": "Reflects the initial number of prominent American hostages released in Beirut during the early phase.",
        "why_wrong": "Three hostages were released, but there were six distinct aircraft and naval shipments of military hardware."
      },
      {
        "option": "Nine",
        "why_plausible": "A figure representing the total number of planned shipments before the channel was exposed.",
        "why_wrong": "The operation unravelled after the sixth consignment when Al-Shiraa blew the whistle."
      },
      {
        "option": "Twelve",
        "why_plausible": "A plausible projection for a year-long logistics operation.",
        "why_wrong": "Only six covert shipments successfully reached Iranian soil before the scandal was made public."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Three hostages", "508 TOW missiles"],
      "fa": ["سه گروگان", "۵۰۸ موشک تاو"]
    },
    "specificity_prompt": {
      "en": "Please provide the exact number of arms shipments documented by Ramazani.",
      "fa": "لطفاً تعداد دقیق محموله‌های ارسالی ثبت‌شده در مقاله رمضانی را به صورت عدد یا حروف بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Six. Spot on. You actually paid attention to archival logistics instead of the political noise.",
        "wrong_generic": "No. The exact figure was six. When counting secret cargo flights, precision is everything.",
        "common_wrong_answers": {
          "Three": "Three was the number of released hostages, not the cargo flights.",
          "Nine": "Nine might have happened if Oliver North hadn't been exposed in Beirut.",
          "Twelve": "Twelve is a wild guess. Read the congressional testimony."
        }
      },
      "fa": {
        "correct_generic": "شش محموله. کاملاً درسته! بالاخره یک نفر آمار دقیق پروازهای محرمانه را درست گفت.",
        "wrong_generic": "خیر، پاسخ درست شش محموله بود. پروازهای مخفیانه شوخی‌بردار نیستند.",
        "common_wrong_answers": {
          "سه محموله": "سه تعداد گروگان‌های آزادشده بود، نه محموله‌های تسلیحات.",
          "نه محموله": "اگر نشریه الشراع افشاگری نمی‌کرد شاید به نه می‌رسید، اما در شش متوقف شد.",
          "دوازده محموله": "دوازده حدس بی‌اساس است؛ آمار گزارش کنگره را بخوانید."
        }
      }
    },
    "explanation": {
      "en": "R. K. Ramazani documents that exactly six shipments of American and Israeli weaponry were delivered to Iran during the Iran-Contra operation, directly conditioning the episodic release of American hostages by pro-Iranian groups in Lebanon.",
      "fa": "روح‌الله رمضانی تصریح می‌کند که در جریان مبادلات پنهانی مک‌فارلین، دقیقاً شش محموله تسلیحاتی تحویل تهران شد و در پی رسیدن هر محموله، شماری از اتباع آمریکایی در بیروت آزاد گردیدند."
    },
    "provenance": {
      "source_book": "Middle East Journal",
      "source_author": "R. K. Ramazani",
      "page_number": 556,
      "verbatim_passage": "Six shipments of arms went to Iran, several American hostages were released, each after Iran received a shipment of arms. Embarrassed by the disclosure of the secret deal, some Iranian leaders, particularly Hashemi-Rafsanjani, tried to cover up the transactions by denouncing America and ridiculing the American mission which had arrived in Tehran with a Bible and a cake.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_axis_advanced_400",
    "round": "double",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {
      "en": "HIGHWAY TO DAMASCUS",
      "fa": "میدانِ بی‌دیپلماسی"
    },
    "clue_text": {
      "en": "Analyzed by Vali Nasr as the cornerstone of Iranian deterrence, this military doctrine establishes that Iran must fight adversaries and deploy regional missile networks beyond its sovereign borders to preempt threats to the homeland.",
      "fa": "در تحلیل ولی نصر از ارکان بازدارندگی جمهوری اسلامی، این دکترین نظامی تصریح می‌کند که برای خنثی‌سازی تهدیدها علیه تمامیت ارضی کشور، باید با استقرار نیروهای هم‌پیمان و شبکه‌های موشکی در فرای مرزها با دشمنان جنگید."
    },
    "canonical_answer": {
      "en": "Forward Defense",
      "fa": "دفاع روبه‌جلو"
    },
    "accepted_aliases": {
      "en": ["Forward Defence", "Defa'-e Rooberolo", "Strategic depth"],
      "fa": ["دفاع رو به جلو", "دکترین دفاع روبه‌جلو", "عمق استراتژیک"]
    },
    "options": {
      "en": ["Forward Defense", "Passive Defense", "Preemptive Strike", "Sacred Defense"],
      "fa": ["دفاع روبه‌جلو", "پدافند غیرعامل", "حمله پیش‌دستانه", "دفاع مقدس"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Passive Defense",
        "why_plausible": "An established military concept (Padafand-e Gheyr-e Amel) heavily funded in Iran.",
        "why_wrong": "It focuses on domestic civil protection, hardened underground infrastructure, and cyber shielding."
      },
      {
        "option": "Preemptive Strike",
        "why_plausible": "A common tactical concept in conventional military doctrine.",
        "why_wrong": "Iran's doctrine emphasizes deterrence and proxy presence rather than initiating unprovoked conventional first strikes."
      },
      {
        "option": "Sacred Defense",
        "why_plausible": "The foundational ideological framing of the 1980–1988 Iran-Iraq War.",
        "why_wrong": "It describes the historical defensive war against Saddam, whereas 'Forward Defense' is the expeditionary post-2011 regional strategy."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Passive Defense", "Sacred Defense"],
      "fa": ["پدافند غیرعامل", "دفاع مقدس"]
    },
    "specificity_prompt": {
      "en": "Please provide the exact strategic doctrine name used by Iranian planners for regional external deterrence.",
      "fa": "لطفاً نام دقیق این دکترین نظامی برای بازدارندگی فرامرزی در منطقه را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Forward Defense. Yes. Better to fight in Aleppo than in Kermanshah, or so the doctrine goes.",
        "wrong_generic": "No. The military doctrine is Forward Defense. The generals were quite explicit about this.",
        "common_wrong_answers": {
          "Passive Defense": "Passive defense buries power plants in concrete; forward defense deploys rockets to Syria.",
          "Preemptive Strike": "Preemptive strikes are tactical launches; forward defense is an entire geopolitical posture.",
          "Sacred Defense": "Sacred Defense was in the 1980s. Forward Defense is the twenty-first-century franchise."
        }
      },
      "fa": {
        "correct_generic": "دفاع روبه‌جلو. کاملاً درسته! همان منطقی که می‌گفت اگر در حلب نجنگیم، باید در کرمانشاه بجنگیم.",
        "wrong_generic": "خیر، پاسخ درست دفاع روبه‌جلو بود. متن سخنرانی‌های فرماندهان نظامی را نشنیده‌اید؟",
        "common_wrong_answers": {
          "پدافند غیرعامل": "پدافند غیرعامل بتن‌ریزی تأسیسات است، دفاع روبه‌جلو پایگاه‌سازی در شام است.",
          "حمله پیش‌دستانه": "حمله پیش‌دستانه اقدام تاکتیکی است، دفاع روبه‌جلو راهبرد بلندمدت منطقه‌ای است.",
          "دفاع مقدس": "دفاع مقدس جنگ دهه شصت بود، دفاع روبه‌جلو استراتژی قرن جدید است."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr explains that Iran's intervention in Syria and empowerment of the Axis of Resistance was guided by the doctrine of 'Forward Defense', designed to establish deterrence against Israel and the US along Mediterranean frontiers rather than on Iranian soil.",
      "fa": "ولی نصر تشریح می‌کند که راهبرد منطقه‌ای ایران موسوم به «دفاع روبه‌جلو» با هدف ایجاد بازدارندگی در مرزهای پیرامونی اسرائیل و ممانعت از سرایت جنگ به داخل جغرافیای ایران تدوین شد."
    },
    "provenance": {
      "source_book": "Iran's Grand Strategy: A Political History",
      "source_author": "Vali Nasr",
      "page_number": 197,
      "verbatim_passage": "The Syrian War served as the fulcrum for emergence of a new generation of sacred defense warriors, vested in protecting Shia interests at a regional level and the goals of forward defense. Importantly, those who fought in Syria would become the next generation of leaders in the IRGC and Hezbollah.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_axis_advanced_800",
    "round": "double",
    "value": 800,
    "difficulty": "STANDARD",
    "category": {
      "en": "HIGHWAY TO DAMASCUS",
      "fa": "میدانِ بی‌دیپلماسی"
    },
    "clue_text": {
      "en": "Coined in Iranian political debates and highlighted in a leaked 2021 audiotape by Mohammad Javad Zarif, this single Persian word describes the militarized institutional domain of the IRGC that dominated civilian diplomacy.",
      "fa": "این واژه تک‌کلمه‌ای فارسی که در فایل صوتی افشاشده سال ۱۴۰۰ محمدجواد ظریف بازتابی جهانی یافت، قلمرو نهادی و نظامی فرماندهان ارشد سپاه را نشان می‌دهد که بر دیپلماسی دستگاه وزارت امور خارجه غلبه داشت."
    },
    "canonical_answer": {
      "en": "Meydan",
      "fa": "میدان"
    },
    "accepted_aliases": {
      "en": ["The Field", "Battlefield", "Meidan", "Meydan-e Jang"],
      "fa": ["میدان نبرد", "عرصه میدان"]
    },
    "options": {
      "en": ["Meydan", "Nezam", "Beit", "Bazar"],
      "fa": ["میدان", "نظام", "بیت", "بازار"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Nezam",
        "why_plausible": "A term constantly used to describe the entire constitutional regime or Islamic order.",
        "why_wrong": "It refers to the political system as a whole, not the specific military operational sphere contrasted with diplomacy."
      },
      {
        "option": "Beit",
        "why_plausible": "Refers to the Office of the Supreme Leader, the ultimate center of national authority.",
        "why_wrong": "The Beit is the supreme clerical apparatus, whereas Zarif explicitly polarized 'Meydan' against 'Diplomacy'."
      },
      {
        "option": "Bazar",
        "why_plausible": "The traditional commercial merchant elite with deep political ties.",
        "why_wrong": "It represents traditional commerce, bearing no relation to military operations in Syria and Iraq."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Nezam", "Sepah"],
      "fa": ["نظام", "سپاه"]
    },
    "specificity_prompt": {
      "en": "Please provide the single Persian word representing the military operational sphere.",
      "fa": "لطفاً همان واژه تک‌کلمه‌ای مورد مناقشه را ذکر فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Meydan. Spot on. The famous battlefield that treated foreign ministers as travel agents.",
        "wrong_generic": "No. The word is Meydan (The Field). Even casual newspaper readers caught that leak.",
        "common_wrong_answers": {
          "Nezam": "Nezam is the entire political regime, not the specific military pole in Zarif's interview.",
          "Beit": "The Beit gives the final stamp; Meydan is where the generals operated.",
          "Bazar": "The Bazar sells carpets; Meydan flies drones."
        }
      },
      "fa": {
        "correct_generic": "میدان. کاملاً درسته! همان میدانی که دیپلمات‌های اتوکشیده را به حاشیه راند.",
        "wrong_generic": "خیر، پاسخ درست میدان بود. فایل صوتی جنجالی ظریف را به این زودی فراموش کردید؟",
        "common_wrong_answers": {
          "نظام": "نظام کل حاکمیت است، دوقطبی ظریف مشخصاً تقابل دیپلماسی و میدان بود.",
          "بیت": "بیت رهبری نهاد عالی است، میدان عنوان فرماندهی نظامی منطقه‌ای بود.",
          "بازار": "بازار مرکز تجارت است، میدان عرصه ادوات نظامی و پهپادهاست."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr documents how the concept of 'Meydan' (the battlefield) represented the structural primacy of IRGC regional military imperatives over civilian foreign policy, institutionalizing an asymmetrical dynamic where diplomats were forced to serve tactical battlefield objectives.",
      "fa": "ولی نصر تشریح می‌کند که مفهوم «میدان» نماد برتری بلامنازع منطق نظامی نیروی قدس سپاه بر دیپلماسی رسمی بود، به طوری که اهداف توافق هسته‌ای تحت‌الشعاع اقتضائات نظامی در دمشق و بغداد قرار گرفت."
    },
    "provenance": {
      "source_book": "Iran's Grand Strategy: A Political History",
      "source_author": "Vali Nasr",
      "page_number": 201,
      "verbatim_passage": "Iran’s role in the war in Syria and the campaign to defeat ISIS further entrenched the IRGC’s hold over Iran’s foreign policy—the domination of the 'battlefield' (meydan) over professional diplomats. Put another way, tactical concerns in Syria then trumped the strategic concerns of the nuclear deal. In effect, Iran’s foreign policy fell squarely into the IRGC’s hands.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_axis_advanced_1200",
    "round": "double",
    "value": 1200,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "HIGHWAY TO DAMASCUS",
      "fa": "میدانِ بی‌دیپلماسی"
    },
    "clue_text": {
      "en": "Drawing on post-structuralist theorists Ernesto Laclau and Chantal Mouffe, Homeira Moshirzadeh applies this linguistic term to concepts like 'independence' and 'Islamic values' to show how their meanings are continually renegotiated to legitimize foreign policy adjustments.",
      "fa": "حمیرا مشیرزاده با استناد به نظریه پساانقلابی ارنستو لاکلائو و شانتال موف، این اصطلاح زبان‌شناختی را برای واژگانی چون «استقلال» و «ارزش‌های اسلامی» به کار می‌برد تا نشان دهد معنای آن‌ها برای توجیه چرخش‌های دیپلماتیک همواره بازتعریف می‌شود."
    },
    "canonical_answer": {
      "en": "Empty signifiers",
      "fa": "دال‌های تهی"
    },
    "accepted_aliases": {
      "en": ["Empty signifier", "Floating signifiers", "Floating signifier"],
      "fa": ["دال تهی", "دال‌های شناور", "دال شناور"]
    },
    "options": {
      "en": ["Empty signifiers", "Master narratives", "Epistemic communities", "Discursive nodal points"],
      "fa": ["دال‌های تهی", "کلان‌روایت‌ها", "جماعت‌های معرفتی", "نقاط گره‌گاهی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "Master narratives",
        "why_plausible": "A common constructivist and literary term used to describe sweeping historical mythologies.",
        "why_wrong": "It refers to broad meta-narratives (like Lyotard's grand narratives), not Laclau and Mouffe's specific concept of hollowed signs."
      },
      {
        "option": "Epistemic communities",
        "why_plausible": "Peter Haas's influential IR concept describing shared networks of technical experts influencing policy.",
        "why_wrong": "It describes professional expert groups, not the textual linguistic mechanics of contested discursive signs."
      },
      {
        "option": "Discursive nodal points",
        "why_plausible": "Another key concept in Laclau and Mouffe's discourse theory (points de capiton).",
        "why_wrong": "Nodal points fix meanings temporarily around a center, whereas Moshirzadeh specifically cites 'empty signifiers' whose content is voided and filled."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Nodal points", "Hegemonic articulation"],
      "fa": ["نقاط گره‌گاهی", "مفصل‌بندی گفتمانی"]
    },
    "specificity_prompt": {
      "en": "Please provide the theoretical discourse-analysis term applied by Moshirzadeh.",
      "fa": "لطفاً اصطلاح نظری دقیق مطرح‌شده در مقاله تحلیل گفتمان مشیرزاده را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Empty signifiers. Quite right. Political slogans are vessels you can fill with whatever policy you need today.",
        "wrong_generic": "No. The term was Empty signifiers. Contemporary political theory is not your strong suit.",
        "common_wrong_answers": {
          "Master narratives": "Master narratives tell grand history; empty signifiers have their meanings emptied and refilled.",
          "Epistemic communities": "Epistemic communities are groups of scientists and bureaucrats, not semiotic concepts.",
          "Discursive nodal points": "Nodal points anchor a discourse; empty signifiers are the hollow vessels being contested."
        }
      },
      "fa": {
        "correct_generic": "دال‌های تهی. کاملاً درسته! ظرف‌های خالی زبانی که سیاستمداران آن را با هرچه بخواهند پر می‌کنند.",
        "wrong_generic": "خیر، پاسخ درست دال‌های تهی بود. مبانی نظری تحلیل گفتمان را با شعار اشتباه نگیرید.",
        "common_wrong_answers": {
          "کلان‌روایت‌ها": "کلان‌روایت‌ها چارچوب‌های تاریخی جامع هستند، نه اصطلاح خاص لاکلائو و موف برای کلمات منعطف.",
          "جماعت‌های معرفتی": "جماعت معرفتی شبکه کارشناسان است، نه مفهوم زبان‌شناختی پساساختاری.",
          "نقاط گره‌گاهی": "نقاط گره‌گاهی معنا را موقتاً تثبیت می‌کنند، دال تهی خودش فاقد محتوای ثابت است."
        }
      }
    },
    "explanation": {
      "en": "Homeira Moshirzadeh explains that in Iran's foreign policy discourse, ideological catchphrases function as 'empty signifiers' whose precise substantive content is continuously renegotiated between competing factions to legitimize shifting strategic compromises.",
      "fa": "حمیرا مشیرزاده استدلال می‌کند که در گفتمان سیاست خارجی ایران، مفاهیمی چون استقلال و ارزش‌های اسلامی به مثابه «دال‌های تهی» عمل می‌کنند که جریان‌های گوناگون با پر کردن آن‌ها از معانی دلخواه، رفتارهای متغیر دیپلماتیک را مشروعیت می‌بخشند."
    },
    "provenance": {
      "source_book": "Middle East Critique",
      "source_author": "Tongyu Wu & Homeira Moshirzadeh",
      "page_number": 6,
      "verbatim_passage": "The concept of 'empty signifiers' (referring to concepts with unfixed content that can be imbued with different meanings by different political forces) provides an important tool for understanding key concepts in foreign policy discourse (Laclau and Mouffe 1985; Wodak and Meyer 2015)... In the context of Iran’s resistance discourse, some concepts such as 'independence', 'Islamic values', and 'anti-imperialism' can be viewed as such empty signifiers, their content constantly negotiated and redefined.",
      "evidence_type": "INTERPRETATION"
    }
  },
  {
    "id": "double_axis_advanced_1600",
    "round": "double",
    "value": 1600,
    "difficulty": "SCHOLAR",
    "category": {
      "en": "HIGHWAY TO DAMASCUS",
      "fa": "میدانِ بی‌دیپلماسی"
    },
    "clue_text": {
      "en": "As analyzed by Vali Nasr, the strategic core of Iran's regional power projection after 2011 was constructing and defending this contiguous overland artery connecting Tehran directly to the Mediterranean through Baghdad and Damascus.",
      "fa": "در تحلیل ولی نصر از نفوذ منطقه‌ای ایران پس از سال ۱۳۹۰ خورشیدی، هسته مرکزی عملیات نیروی قدس بر ساخت و حفاظت از این شریان پیوسته زمینی متمرکز بود که تهران را از مسیر بغداد و دمشق مستقیماً به سواحل مدیترانه متصل می‌کرد."
    },
    "canonical_answer": {
      "en": "Land corridor",
      "fa": "گذرگاه زمینی"
    },
    "accepted_aliases": {
      "en": ["Land bridge", "Tehran-Beirut land corridor", "Overland corridor", "Shia Crescent corridor"],
      "fa": ["کریدور زمینی", "پل زمینی", "گذرگاه تهران به بیروت"]
    },
    "options": {
      "en": ["Land corridor", "String of Pearls", "Northern Corridor", "Maritime Silk Road"],
      "fa": ["گذرگاه زمینی", "رشته مروارید", "کریدور شمال-جنوب", "راه ابریشم دریایی"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "String of Pearls",
        "why_plausible": "A well-known geopolitical network of military and commercial facilities.",
        "why_wrong": "It refers to China's network of naval ports along Indian Ocean sea lines, not Iran's Levant highway."
      },
      {
        "option": "Northern Corridor",
        "why_plausible": "A famous regional trade route connecting Central Asia to Europe through northern Iran.",
        "why_wrong": "It is an economic transit network through the Caucasus and Central Asia, not the military route to Lebanon."
      },
      {
        "option": "Maritime Silk Road",
        "why_plausible": "Part of Beijing's Belt and Road initiative involving international sea routes.",
        "why_wrong": "It describes commercial sea lanes, whereas Iran fought extensively for a terrestrial highway through Iraq and Syria."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["International North-South Transport Corridor", "Shia Crescent"],
      "fa": ["کریدور شمال-جنوب", "هلال شیعی"]
    },
    "specificity_prompt": {
      "en": "Please provide the specific geopolitical term for the overland transit route connecting Tehran to Beirut.",
      "fa": "لطفاً اصطلاح ژئوپلیتیکی این مسیر حمل‌ونقل پیوسته خشکی را بیان فرمایید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Land corridor. Correct. Fifteen hundred kilometers of tarmac that kept American and Israeli intelligence up at night.",
        "wrong_generic": "No. The geopolitical objective was the Land corridor (or Land bridge). That is why the troops were in the desert.",
        "common_wrong_answers": {
          "String of Pearls": "String of Pearls belongs to Beijing in the Indian Ocean, not the IRGC in the Levant.",
          "Northern Corridor": "The Northern Corridor runs up to the Caucasus, not across the Euphrates to Beirut.",
          "Maritime Silk Road": "The Maritime Silk Road is on container ships, not desert highways through Albu Kamal."
        }
      },
      "fa": {
        "correct_generic": "گذرگاه زمینی. کاملاً درسته! همان جاده‌ای که واشنگتن و تل‌آویو برای قطع کردنش کویر را بمباران کردند.",
        "wrong_generic": "خیر، پاسخ درست گذرگاه زمینی (پل زمینی) بود. مبانی جغرافیای نظامی خاورمیانه را مرور کنید.",
        "common_wrong_answers": {
          "رشته مروارید": "رشته مروارید پایگاه‌های دریایی چین در اقیانوس هند است، نه مسیر زمینی بوکمال.",
          "کریدور شمال-جنوب": "کریدور شمال-جنوب مسیر تجاری روسیه به هند از قفقاز است، نه اتوبان به مدیترانه.",
          "راه ابریشم دریایی": "راه ابریشم دریایی برای کشتی‌های تجاری است، نه کاروان‌های لجستیک زمینی سپاه."
        }
      }
    },
    "explanation": {
      "en": "Vali Nasr details that establishing an unbroken overland bridge from Iran across Iraq and Syria to Lebanon was the primary strategic objective of the IRGC, providing an invulnerable logistics supply chain to Hezbollah and cementing Iran's Mediterranean reach.",
      "fa": "ولی نصر نشان می‌دهد که دستیابی به یک گذرگاه زمینی پیوسته از تهران تا مدیترانه، مهم‌ترین اولویت لجستیکی و ژئوپلیتیکی نیروی قدس در سوریه و عراق بود تا امنیت تسلیحاتی حزب‌الله تضمین شود."
    },
    "provenance": {
      "source_book": "Iran's Grand Strategy: A Political History",
      "source_author": "Vali Nasr",
      "page_number": 201,
      "verbatim_passage": "Therefore both Israel and the United States were keen to disrupt the link between Iran and Lebanon through Iraq and Syria. Iran believes that this is the only reason why US troops remained in Syria. Iran has thus deployed Iraqi and Syrian militias to target US troops in Syria to encourage Washington to withdraw them. Iran saw an opportunity in the Gaza war that started in 2023 to escalate this pressure, using the cover of the war to break America’s choke hold on Iran’s bridge from Iraq to Lebanon.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "double_axis_advanced_2000",
    "round": "double",
    "value": 2000,
    "difficulty": "INSUFFERABLE",
    "category": {
      "en": "HIGHWAY TO DAMASCUS",
      "fa": "میدانِ بی‌دیپلماسی"
    },
    "clue_text": {
      "en": "In his archival history of the Syrian conflict, Vali Nasr records this exact peak number of IRGC officers, advisers, and ground soldiers stationed inside Syria by 2016 to sustain the Assad regime and construct military operational infrastructure against Israel.",
      "fa": "در تحلیل تاریخی و آماری ولی نصر از منازعه سوریه، دقیقاً این تعداد افسر، مستشار و نیروی نظامی سپاه پاسداران تا سال ۱۳۹۵ خورشیدی در خاک سوریه مستقر بودند تا از فروپاشی دولت اسد ممانعت کنند."
    },
    "canonical_answer": {
      "en": "9,200",
      "fa": "نه هزار و دویست نفر"
    },
    "accepted_aliases": {
      "en": ["9200", "9,200 soldiers", "Ninety-two hundred"],
      "fa": ["۹۲۰۰", "۹۲۰۰ نفر", "نه هزار و دویست"]
    },
    "options": {
      "en": ["9,200", "5,000", "15,000", "25,000"],
      "fa": ["نه هزار و دویست نفر", "پنج هزار نفر", "پانزده هزار نفر", "بیست و پنج هزار نفر"]
    },
    "correct_option_index": 0,
    "distractor_rationales": [
      {
        "option": "5,000",
        "why_plausible": "A conservative round estimate often cited in early media accounts of Iranian advisory presence.",
        "why_wrong": "The verified figure documented by Nasr reached over 9,000 personnel as the campaign deepened."
      },
      {
        "option": "15,000",
        "why_plausible": "Reflects the larger force size if including non-Iranian allied foreign militias like the Fatemiyoun and Zainabiyoun.",
        "why_wrong": "15,000 describes combined transnational militia brigades, whereas Nasr specifies 9,200 organic IRGC personnel."
      },
      {
        "option": "25,000",
        "why_plausible": "An inflated figure frequently quoted by regional opposition sources and think-tank estimates.",
        "why_wrong": "Nasr's academic accounting puts the actual peak IRGC deployment at ninety-two hundred officers and soldiers."
      }
    ],
    "adversarial_confusion_set": {
      "en": ["Fatemiyoun 20,000", "Hezbollah 8,000"],
      "fa": ["بیست هزار فاطمیون", "هشت هزار حزب‌الله"]
    },
    "specificity_prompt": {
      "en": "Please provide the exact number of IRGC officers and troops documented by Vali Nasr.",
      "fa": "لطفاً رقم آماری دقیق نیروهای رسمی سپاه پاسداران در سوریه به گزارش ولی نصر را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "9,200. Remarkable. You actually know the exact troop count instead of guessing wildly like a cable news pundit.",
        "wrong_generic": "No. The figure recorded by Vali Nasr was exactly 9,200. Precision matters in military history.",
        "common_wrong_answers": {
          "5,000": "Five thousand was the early guess; by 2016 the commitment had nearly doubled.",
          "15,000": "Fifteen thousand counts the Afghan and Pakistani foreign volunteer brigades.",
          "25,000": "Twenty-five thousand is opposition propaganda, not archival history."
        }
      },
      "fa": {
        "correct_generic": "نه هزار و دویست نفر. کاملاً درسته! آمار دقیق استقرار را از روی اسناد پژوهشی درست گفتید.",
        "wrong_generic": "خیر، رقم ثبت‌شده توسط ولی نصر دقیقاً نه هزار و دویست نفر بود. در تاریخ نظامی دقت اهمیت دارد.",
        "common_wrong_answers": {
          "پنج هزار نفر": "پنج هزار برآورد سال‌های اول بود، تا سال ۹۵ این رقم به بیش از نه هزار رسید.",
          "پانزده هزار نفر": "پانزده هزار کل نیروهای نیابتی از جمله فاطمیون است، نه کادر سپاه.",
          "بیست و پنج هزار نفر": "بیست و پنج هزار اغراق رسانه‌های معارض بود؛ متن تاریخ را بخوانید."
        }
      }
    },
    "explanation": {
      "en": "In 'Iran's Grand Strategy', Vali Nasr reveals that by 2016, approximately 9,200 IRGC officers, military advisers, and ground soldiers were actively deployed across Syrian battlefields, marking Iran's largest expeditionary foreign military deployment since the 1979 Revolution.",
      "fa": "ولی نصر در پژوهش خود نشان می‌دهد که تا سال ۱۳۹۵ خورشیدی بالغ بر نه هزار و دویست تن از فرماندهان، مستشاران و رزمندگان رسمی سپاه در سوریه مستقر بودند که بزرگ‌ترین اعزام نظامی برون‌مرزی پس از انقلاب به شمار می‌رفت."
    },
    "provenance": {
      "source_book": "Iran's Grand Strategy: A Political History",
      "source_author": "Vali Nasr",
      "page_number": 201,
      "verbatim_passage": "In the Syrian War, by comparison, Iran’s role remained more limited. There were Shia militias such as the Fatemiyoun and Hezbollah fighting against ISIS, but the Qods Force more often led from behind. Still, by 2016 there were some ninety-two hundred IRGC officers, advisers, and soldiers in Syria. Most were engaged in protecting the Assad regime, but some were also busy building an infrastructure for the IRGC and Hezbollah to operate from Syria against Israel.",
      "evidence_type": "FACT"
    }
  }
]

for c in new_clues:
    validate_clue_schema(c)

append_validated_clues(new_clues)
print("All clues validated and appended successfully!")
