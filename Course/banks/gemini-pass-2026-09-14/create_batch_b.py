import json
import sys
sys.path.append("/Users/Morad/Spark")
from jeopardy_pipeline import validate_clue_schema

batch_b = []

# Categories 11 to 20
c11_to_c20 = [
  # 11. single_justice_shares: JUSTICE FOR SOME SHARES / سهام عدالت در جیب خصولتی
  {
    "id": "single_justice_shares_200",
    "round": "single",
    "value": 200,
    "difficulty": "CASUAL",
    "category": {"en": "JUSTICE FOR SOME SHARES", "fa": "سهام عدالت در جیب خصولتی"},
    "clue_text": {
      "en": "Launched with great fanfare in 2006 by President Mahmoud Ahmadinejad, this populist voucher privatization scheme distributed shares of state-owned enterprises to low-income deciles.",
      "fa": "این طرح واگذاری سهام در سال ۱۳۸۵ با هیاهوی فراوان توسط محمود احمدی‌نژاد برای توزیع مالکیت شرکت‌های دولتی میان دهک‌های کم‌درآمد اجرا شد و سهام عدالت نام گرفت."
    },
    "canonical_answer": {"en": "Justice Shares", "fa": "سهام عدالت"},
    "accepted_aliases": {"en": ["Saham-e Edalat", "Justice Shares scheme", "Shares of Justice"], "fa": ["طرح سهام عدالت", "برگه سهام عدالت", "سهام عدالت"]},
    "options": {
      "en": ["Targeted Subsidies", "Justice Shares", "Mehr Housing Project", "National Development Fund"],
      "fa": ["هدفمندی یارانه‌ها", "سهام عدالت", "مسکن مهر", "صندوق توسعه ملی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Targeted Subsidies", "why_plausible": "A major economic reform under Ahmadinejad.", "why_wrong": "Targeted Subsidies (Hadafmandi-e Yaraneh-ha) replaced price subsidies with monthly cash transfers in 2010, not the 2006 voucher shares."},
      {"option": "Mehr Housing Project", "why_plausible": "A massive Ahmadinejad public works housing scheme.", "why_wrong": "Maskan-e Mehr built suburban apartment blocks, not equity vouchers in state industrial firms."},
      {"option": "National Development Fund", "why_plausible": "A sovereign wealth fund managing oil revenues.", "why_wrong": "It holds foreign currency reserves from oil exports, not citizen voucher privatization."}
    ],
    "adversarial_confusion_set": {"en": ["Maskan-e Mehr", "Yaraneh"], "fa": ["مسکن مهر", "یارانه نقدی"]},
    "specificity_prompt": {
      "en": "Name the specific voucher privatization program initiated in 2006 under Mahmoud Ahmadinejad.",
      "fa": "نام طرح واگذاری سهام شرکت‌های دولتی به اقشار فرودست در سال ۱۳۸۵ را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Justice Shares. Correct. Handing out paper vouchers to millions while state bureaucrats kept all the voting control.",
        "wrong_generic": "No, it was Justice Shares (Saham-e Edalat). The centerpiece of oil-fueled populist economics.",
        "common_wrong_answers": {
          "Targeted Subsidies": "Subsidies put cash into bank accounts in 2010; Justice Shares gave equity paper in 2006.",
          "Mehr Housing Project": "Maskan-e Mehr poured concrete in the desert; Justice Shares gave stakes in petrochemicals.",
          "National Development Fund": "The National Fund hoards petrodollars, it doesn't print coupon vouchers for the public."
        }
      },
      "fa": {
        "correct_generic": "سهام عدالت. کاملاً درسته! توزیع برگه‌های کاغذی سهام میان مردم در حالی که مدیریت در پاستور باقی ماند.",
        "wrong_generic": "خیر، پاسخ سهام عدالت بود. شاهکار پوپولیسم اقتصادی دولت نهم.",
        "common_wrong_answers": {
          "هدفمندی یارانه‌ها": "هدفمندی واریز ماهانه ۴۵ هزار و ۵۰۰ تومان پول نقد بود، نه واگذاری سهام کارخانجات.",
          "مسکن مهر": "مسکن مهر ساخت آپارتمان در بیابان‌های پردیس و پرند بود، نه اوراق بهادار.",
          "صندوق توسعه ملی": "صندوق توسعه ملی ذخیره ارزی نفت است، نه توزیع سهام بین مردم."
        }
      }
    },
    "explanation": {
      "en": "Kevan Harris explains that Saham-e Edalat (Justice Shares) was introduced in 2006 to redistribute equity in state-owned enterprises to the bottom income deciles, transforming populist rhetoric into an immense voucher-based state capitalism.",
      "fa": "کوان هریس تشریح می‌کند که طرح سهام عدالت در سال ۱۳۸۵ با هدف توزیع سهام شرکت‌های دولتی میان فرودستان آغاز شد اما عملاً به ایجاد سرمایه‌داری دولتی مبتنی بر اوراق واگذاری انجامید."
    },
    "provenance": {
      "source_book": "The Rise of the Subcontractor State: Politics of Privatization in the IRI",
      "source_author": "Kevan Harris",
      "page_number": 48,
      "verbatim_passage": "In 2006, President Ahmadinejad initiated the 'Justice Shares' (Saham-e Edalat) program, transferring shares of state enterprises to millions of low-income citizens through provincial investment intermediaries.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_justice_shares_400",
    "round": "single",
    "value": 400,
    "difficulty": "STANDARD",
    "category": {"en": "JUSTICE FOR SOME SHARES", "fa": "سهام عدالت در جیب خصولتی"},
    "clue_text": {
      "en": "The legal foundation for mass privatization was established when Supreme Leader Khamenei issued a groundbreaking 2004 decree reinterpreting this article of the Iranian Constitution, which had originally placed heavy industry entirely under state ownership.",
      "fa": "بستر قانونی خصوصی‌سازی گسترده با ابلاغیه ساختارشکنانه رهبری در سال ۱۳۸۴ فراهم شد که این اصل قانون اساسی را بازتفسیر کرد؛ اصلی که پیش‌تر صنایع بزرگ را منحصراً در مالکیت دولت قرار داده بود."
    },
    "canonical_answer": {"en": "Article 44", "fa": "اصل ۴۴"},
    "accepted_aliases": {"en": ["Article 44 of the Constitution", "Principle 44", "Asl-e 44"], "fa": ["اصل چهل و چهار", "اصل ۴۴ قانون اساسی", "اصل چهل و چهارم"]},
    "options": {
      "en": ["Article 4", "Article 44", "Article 110", "Article 176"],
      "fa": ["اصل ۴", "اصل ۴۴", "اصل ۱۱۰", "اصل ۱۷۶"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Article 4", "why_plausible": "A major article stating all laws must conform to Islamic criteria.", "why_wrong": "Article 4 governs Islamic supremacy over legislation, not economic sector ownership."},
      {"option": "Article 110", "why_plausible": "A famous constitutional article outlining the powers of the Supreme Leader.", "why_wrong": "Article 110 lists the Leader's constitutional prerogatives, not the economic structure of state versus private property."},
      {"option": "Article 176", "why_plausible": "Pertains to high-level state governance.", "why_wrong": "Article 176 establishes the Supreme National Security Council, not property rights."}
    ],
    "adversarial_confusion_set": {"en": ["Article 43", "Article 49"], "fa": ["اصل ۴۳", "اصل ۴۹"]},
    "specificity_prompt": {
      "en": "Name the specific article of the Iranian Constitution governing the division between state, cooperative, and private economic sectors.",
      "fa": "شماره اصلی از قانون اساسی جمهوری اسلامی که نظام اقتصادی کشور را به سه بخش دولتی، تعاونی و خصوصی تقسیم کرده بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Article 44. Correct. Reinterpreting 1979 socialist-leaning constitutional text into a green light for parastatal capitalism.",
        "wrong_generic": "No, it was Article 44. The constitutional bedrock of Iran's controversial privatization wave.",
        "common_wrong_answers": {
          "Article 4": "Article 4 is Sharia compliance; Article 44 is economic ownership.",
          "Article 110": "Article 110 is the Leader's powers; Article 44 is factories and mines.",
          "Article 176": "Article 176 runs the Security Council; Article 44 runs the economy."
        }
      },
      "fa": {
        "correct_generic": "اصل ۴۴. کاملاً درسته! بازتفسیری که متن چپ‌گرایانه قانون اساسی اول انقلاب را به مجوز واگذاری کارخانه‌ها تبدیل کرد.",
        "wrong_generic": "خیر، پاسخ اصل ۴۴ قانون اساسی بود. سنگ‌بنای حقوقی موج خصوصی‌سازی در دهه هشتاد.",
        "common_wrong_answers": {
          "اصل ۴": "اصل ۴ درباره انطباق تمام قوانین با موازین اسلام است، نه مالکیت صنایع.",
          "اصل ۱۱۰": "اصل ۱۱۰ وظایف و اختیارات رهبری است؛ اصل ۴۴ بخش‌های اقتصادی کشور را معین کرده است.",
          "اصل ۱۷۶": "اصل ۱۷۶ مربوط به شورای عالی امنیت ملی است."
        }
      }
    },
    "explanation": {
      "en": "Kevan Harris analyzes how the 2004-2005 reinterpretation of Article 44 of the Iranian Constitution by the Supreme Leader allowed the divestment of up to 80% of state-owned shares in heavy industry, banking, and communications, formally reversing early revolutionary statism.",
      "fa": "کوان هریس تحلیل می‌کند که چگونه ابلاغ سیاست‌های کلی اصل ۴۴ قانون اساسی توسط رهبر جمهوری اسلامی در سال ۱۳۸۴ اجازه واگذاری تا ۸۰ درصد سهام صنایع سنگین، بانک‌ها و مخابرات دولتی را صادر کرد و دولت‌گرایی دهه شصت را وارونه ساخت."
    },
    "provenance": {
      "source_book": "The Rise of the Subcontractor State: Politics of Privatization in the IRI",
      "source_author": "Kevan Harris",
      "page_number": 51,
      "verbatim_passage": "In 2004, Supreme Leader Khamenei issued an executive decree reinterpreting Article 44 of the Constitution, transforming an article originally intended to prevent capitalist consolidation into a mandate for privatizing state industry.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_justice_shares_600",
    "round": "single",
    "value": 600,
    "difficulty": "STANDARD",
    "category": {"en": "JUSTICE FOR SOME SHARES", "fa": "سهام عدالت در جیب خصولتی"},
    "clue_text": {
      "en": "Rather than transferring enterprises to independent private entrepreneurs, privatization in Iran overwhelmingly benefited military, clerical, and pension conglomerates, popularized in public discourse by this Persian portmanteau.",
      "fa": "خصوصی‌سازی در ایران به جای انتقال شرکت‌ها به کارآفرینان واقعی بخش خصوصی، عمدتاً به کام نهادهای نظامی، بنیادها و صندوق‌های بازنشستگی تمام شد و این اصطلاح طنزآمیز تلفیقی برای توصیف آن‌ها رواج یافت."
    },
    "canonical_answer": {"en": "Khosoolati", "fa": "خصولتی"},
    "accepted_aliases": {"en": ["Khosulati", "Quasi-state", "Parastatal sector", "Khosulaty"], "fa": ["شبه‌دولتی", "شرکت‌های خصولتی", "شبه دولتی"]},
    "options": {
      "en": ["Bazaari", "Khosoolati", "Ashrafi", "Mostazaf"],
      "fa": ["بازاری", "خصولتی", "اشرافی", "مستضعف"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Bazaari", "why_plausible": "Traditional private commercial class.", "why_wrong": "Bazaaris are traditional merchants, not the military/parastatal hybrid giants spawned by post-2005 privatization."},
      {"option": "Ashrafi", "why_plausible": "Refers to aristocratic wealth.", "why_wrong": "Ashrafi means aristocratic or regal, not the specific political portmanteau blending 'private' and 'state'."},
      {"option": "Mostazaf", "why_plausible": "A revolutionary term for the poor.", "why_wrong": "Mostazaf denotes the underprivileged, the very opposite of parastatal monopolies."}
    ],
    "adversarial_confusion_set": {"en": ["Semi-private", "Aghazadeh"], "fa": ["شبه‌خصوصی", "آقازاده"]},
    "specificity_prompt": {
      "en": "Provide the exact Persian portmanteau blending 'private' (khosusi) and 'state' (dowlati) used to describe these conglomerates.",
      "fa": "واژه مرکب عامیانه‌ای که از ترکیب دو کلمه «خصوصی» و «دولتی» برای اشاره به این بنگاه‌های رانتی ساخته شده را بنویسید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Khosoolati. Spot on. Privatization Iranian style: transferring a state factory from the left pocket of the regime to the right pocket of the IRGC.",
        "wrong_generic": "No, the term was Khosoolati. A brilliant linguistic marriage of 'private' and 'governmental'.",
        "common_wrong_answers": {
          "Bazaari": "Bazaaris sell rugs in the alleys; Khosoolati giants buy entire telecommunications monopolies.",
          "Ashrafi": "Ashrafi is old royal aristocracy; Khosoolati is revolutionary parastatals.",
          "Mostazaf": "The mostazafin received paper vouchers; the parastatals received the billion-dollar assets."
        }
      },
      "fa": {
        "correct_generic": "خصولتی. کاملاً درسته! خصوصی‌سازی به سبک وطنی: انتقال کارخانه از جیب چپ وزارتخانه به جیب راست نهادهای نظامی.",
        "wrong_generic": "خیر، پاسخ خصولتی بود. واژه تلفیقی گویایی که ماهیت بنگاه‌های شبه‌دولتی را بر ملا می‌کند.",
        "common_wrong_answers": {
          "بازاری": "بازاری کسبه سنتی است؛ خصولتی‌ها کنسرسیوم‌های میلیاردی وابسته به قدرت هستند.",
          "اشرافی": "اشرافی صفت کلی است؛ خصولتی اصطلاح دقیق تلفیق خصوصی و دولتی است.",
          "مستضعف": "مستضعفان تماشاگر بازی بودند؛ خصولتی‌ها سهام مخابرات و پتروشیمی را بلعیدند."
        }
      }
    },
    "explanation": {
      "en": "Kevan Harris examines the rise of the 'subcontractor state', where state assets were transferred to parastatals like Khatam al-Anbiya, the Armed Forces Social Security Organization (SATA), and bonyads, commonly derided as 'khosoolati' (quasi-governmental).",
      "fa": "کوان هریس ظهور «دولت پیمانکار» را بررسی می‌کند که در آن دارایی‌های ملی به نهادهایی چون قرارگاه خاتم‌الانبیاء، ساتا و بنیادها واگذار شد؛ بخش عظیم اقتصادی که در فرهنگ عمومی به «خصولتی» شهرت یافت."
    },
    "provenance": {
      "source_book": "The Rise of the Subcontractor State: Politics of Privatization in the IRI",
      "source_author": "Kevan Harris",
      "page_number": 56,
      "verbatim_passage": "In everyday parlance, Iranians coined the portmanteau term khosulati—a blend of khosusi (private) and dowlati (governmental)—to mock an ownership structure where enterprises enjoyed private profits alongside sovereign impunity.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_justice_shares_800",
    "round": "single",
    "value": 800,
    "difficulty": "SCHOLAR",
    "category": {"en": "JUSTICE FOR SOME SHARES", "fa": "سهام عدالت در جیب خصولتی"},
    "clue_text": {
      "en": "Under the Justice Shares design analyzed by Harris, individual citizens did not receive direct stock in individual firms, but were aggregated into these provincial holding entities that held the collective portfolio.",
      "fa": "در سازوکار سهام عدالت که توسط هریس بررسی شده، به شهروندان مستقیماً سهام کارخانجات داده نشد، بلکه مالکیت آنها در این نهادهای سرمایه‌گذاری استانی تجمیع گردید که کل سبد دارایی را مدیریت می‌کردند."
    },
    "canonical_answer": {"en": "Provincial Investment Companies", "fa": "شرکت‌های سرمایه‌گذاری استانی"},
    "accepted_aliases": {"en": ["Sherkat-haye Sarmayegozari-e Ostani", "Provincial investment firms", "Provincial holding companies"], "fa": ["شرکت‌های سرمایه گذاری استانی", "سرمایه‌گذاری استانی", "شرکت سرمایه‌گذاری استان"]},
    "options": {
      "en": ["Tehran Stock Exchange", "Provincial Investment Companies", "Bonyad-e Ta'avon", "Agricultural Bank"],
      "fa": ["بورس اوراق بهادار تهران", "شرکت‌های سرمایه‌گذاری استانی", "بنیاد تعاون", "بانک کشاورزی"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Tehran Stock Exchange", "why_plausible": "The national market where publicly traded shares are listed.", "why_wrong": "Justice Shares were deliberately kept off the direct trading floor of the TSE for over a decade."},
      {"option": "Bonyad-e Ta'avon", "why_plausible": "A major cooperative foundation connected to armed forces.", "why_wrong": "Bonyad-e Ta'avon manages military personnel benefits, not the statutory provincial Justice Shares holding companies."},
      {"option": "Agricultural Bank", "why_plausible": "A state bank serving rural citizens who received shares.", "why_wrong": "Bank Keshavarzi is a credit and lending institution, not the corporate holding structure holding Justice Shares portfolios."}
    ],
    "adversarial_confusion_set": {"en": ["Justice Shares Cooperatives", "Regional Development Banks"], "fa": ["شرکت‌های تعاونی سهام عدالت", "صندوق‌های بازنشستگی استانی"]},
    "specificity_prompt": {
      "en": "Name the specific provincial intermediary corporate entities created to hold and manage Justice Shares.",
      "fa": "نام شرکت‌های واسطه‌ای در سطح استان‌ها که سهام عدالت شهروندان در آن‌ها تجمیع و اداره می‌شد را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Provincial Investment Companies. Correct. Layering another opaque bureaucracy between the citizen and the stock certificate.",
        "wrong_generic": "No, it was the Provincial Investment Companies (Sherkat-haye Sarmayegozari-e Ostani). The institutional barrier that prevented citizens from voting their own shares.",
        "common_wrong_answers": {
          "Tehran Stock Exchange": "The shares were locked away from the stock exchange for nearly fifteen years.",
          "Bonyad-e Ta'avon": "Ta'avon belongs to the military, not the provincial Justice Share boards.",
          "Agricultural Bank": "The bank cashed dividend checks; it didn't hold the corporate equity."
        }
      },
      "fa": {
        "correct_generic": "شرکت‌های سرمایه‌گذاری استانی. کاملاً درسته! ایجاد یک لایه بوروکراتیک تاریک دیگر میان دست سهامدار و کارخانه.",
        "wrong_generic": "خیر، پاسخ شرکت‌های سرمایه‌گذاری استانی بود. ساختاری که رأی و کنترل سهام مردم را در دست مدیران دولتی نگه داشت.",
        "common_wrong_answers": {
          "بورس اوراق بهادار تهران": "سهام عدالت تا ۱۵ سال اجازه دادوستد مستقیم در تالار بورس را نداشت.",
          "بنیاد تعاون": "بنیاد تعاون مربوط به نیروهای مسلح است، نه ساختار اداری استانی سهام عدالت.",
          "بانک کشاورزی": "بانک کشاورزی عامل واریز سود بود، نه شرکت مادر دارنده سهام."
        }
      }
    },
    "explanation": {
      "en": "Kevan Harris explains that rather than direct equity ownership, the state channeled citizens into Provincial Investment Companies (Sherkat-haye Sarmayegozari-e Ostani), which in turn were controlled by government-appointed boards, ensuring the state retained operational control over privatized firms.",
      "fa": "کوان هریس توضیح می‌دهد که به جای اعطای سهام مستقیم، سهام مردم در «شرکت‌های سرمایه‌گذاری استانی» بلوکه شد که هیئت‌مدیره آن‌ها توسط مقامات دولتی تعیین می‌شد تا حاکمیت کنترل عملیاتی صنایع واگذارشده را حفظ کند."
    },
    "provenance": {
      "source_book": "The Rise of the Subcontractor State: Politics of Privatization in the IRI",
      "source_author": "Kevan Harris",
      "page_number": 59,
      "verbatim_passage": "Citizens were not issued shares in individual firms, but rather in thirty Provincial Investment Companies, allowing the Ministry of Economy to appoint board members and retain proxy control over major privatized enterprises.",
      "evidence_type": "FACT"
    }
  },
  {
    "id": "single_justice_shares_1000",
    "round": "single",
    "value": 1000,
    "difficulty": "INSUFFERABLE",
    "category": {"en": "JUSTICE FOR SOME SHARES", "fa": "سهام عدالت در جیب خصولتی"},
    "clue_text": {
      "en": "Harris highlights this central political paradox of the Justice Shares scheme: while tens of millions of low-income citizens received periodic dividend cash payouts, they were strictly legally denied this fundamental shareholder prerogative.",
      "fa": "هریس به این پارادوکس بنیادین طرح سهام عدالت اشاره می‌کند: در حالی که ده‌ها میلیون شهروند فرودست سود نقدی دوره‌ای دریافت می‌کردند، از نظر قانونی از این حق اولیه و بنیادین سهامداری کاملاً محروم بودند."
    },
    "canonical_answer": {"en": "Voting Rights on Corporate Boards", "fa": "حق رأی در مجامع و انتخاب هیئت‌مدیره"},
    "accepted_aliases": {"en": ["Voting rights", "Board voting rights", "Proxy voting", "Shareholder voting rights"], "fa": ["حق رای در مجامع", "حق رای", "انتخاب هیات مدیره", "حق رای سهامداری"]},
    "options": {
      "en": ["Right to Receive Dividends", "Voting Rights on Corporate Boards", "Right to Open a Bank Account", "Right to Inheritance"],
      "fa": ["حق دریافت سود نقدی", "حق رأی در مجامع و انتخاب هیئت‌مدیره", "حق افتتاح حساب بانکی", "حق انتقال به وارث"]
    },
    "correct_option_index": 1,
    "distractor_rationales": [
      {"option": "Right to Receive Dividends", "why_plausible": "A primary shareholder right.", "why_wrong": "Citizens DID receive dividend payments (Sood-e Saham); it was voting governance they were denied."},
      {"option": "Right to Open a Bank Account", "why_plausible": "A basic civil requirement.", "why_wrong": "Every citizen had bank accounts specifically to receive cash payouts under the subsidy reforms."},
      {"option": "Right to Inheritance", "why_plausible": "Property succession right.", "why_wrong": "Justice Shares were legally inherited by heirs under Islamic inheritance law upon death."}
    ],
    "adversarial_confusion_set": {"en": ["Right to Sell Immediately", "Right to Inspect Audits"], "fa": ["حق فروش فوری در بازار", "حق بازرسی دفاتر مالی"]},
    "specificity_prompt": {
      "en": "Specify the crucial corporate governance power denied to Justice Shares recipients while the state retained control.",
      "fa": "حق اساسی سهامداری در مدیریت و عزل و نصب هیئت‌مدیره که از دارندگان سهام عدالت سلب شده بود را ذکر کنید."
    },
    "host_reactions": {
      "en": {
        "correct_generic": "Voting Rights on Corporate Boards. Spot on. You get forty dollars a year for tea, while the ministry picks the CEO.",
        "wrong_generic": "No, they were denied Voting Rights on Corporate Boards. The illusion of popular ownership without a shred of managerial control.",
        "common_wrong_answers": {
          "Right to Receive Dividends": "They received the dividends every year before elections.",
          "Right to Open a Bank Account": "You needed a bank account just to cash the coupon.",
          "Right to Inheritance": "The shares passed to children upon death."
        }
      },
      "fa": {
        "correct_generic": "حق رأی در مجامع و انتخاب هیئت‌مدیره. کاملاً درسته! سالی چند صد هزار تومان سود واریز می‌شد، اما صندلی هیئت‌مدیره دست دولت ماند.",
        "wrong_generic": "خیر، پاسخ حق رأی در مجامع و انتخاب هیئت‌مدیره بود. توهم سهامداری بدون ذره‌ای حق نظارت و تصمیم‌گیری.",
        "common_wrong_answers": {
          "حق دریافت سود نقدی": "سود نقدی اتفاقاً در آستانه انتخابات‌ها به حساب‌ها واریز می‌شد.",
          "حق افتتاح حساب بانکی": "برای دریافت سود همه موظف به معرفی شماره شبا بودند.",
          "حق انتقال به وارث": "سهام عدالت طبق قانون ارث به بازماندگان متوفی منتقل می‌شد."
        }
      }
    },
    "explanation": {
      "en": "Harris emphasizes that the state decoupled the cash flow rights of shares from corporate control rights: citizens received dividend checks, but the state retained proxy voting power over 40% of Iran's major corporate boards, cementing parastatal dominance.",
      "fa": "کوان هریس تأکید می‌کند که دولت با تفکیک حق سودآوری از حق حاکمیت شرکتی، سود ناچیز نقدی را به مردم داد اما حق رأی در مجامع شرکت‌ها را حفظ کرد تا کنترل ۴۰ درصد از بزرگ‌ترین شرکت‌های بورسی در دست وزرا و نهادهای قدرت باقی بماند."
    },
    "provenance": {
      "source_book": "The Rise of the Subcontractor State: Politics of Privatization in the IRI",
      "source_author": "Kevan Harris",
      "page_number": 63,
      "verbatim_passage": "By retaining the proxy voting rights of Justice Shares in government-controlled hands while dispersing non-voting equity to millions, the Iranian state engineered mass political inclusion without surrendering managerial control.",
      "evidence_type": "INTERPRETATION"
    }
  }
]

batch_b.extend(c11_to_c20)
for c in batch_b:
    validate_clue_schema(c)

print(f"Validated {len(batch_b)} clues in Category 11 successfully.")
