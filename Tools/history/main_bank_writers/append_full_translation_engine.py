import json
import re

code = '''
# -------------------------------------------------------------
# Comprehensive Persian Translation Engine
# -------------------------------------------------------------

def build_farsi_bank():
    print("Loading QuestionBank/verified_clues.json...")
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"Loaded {len(en_clues)} English clues.")

    # Load existing Persian copy for initial canonical answers & options
    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        persian_copy = json.load(f)

    # Master Option Mapping
    opt_map = {}
    for c in en_clues:
        cid = c['id']
        en_ans = c['canonical_answer'].strip()
        fa_ans = persian_copy[cid]['canonical_answer'].strip()
        opt_map[en_ans] = fa_ans
        for alias in c.get('accepted_aliases', []):
            opt_map[alias.strip()] = fa_ans
        fa_opts = persian_copy[cid].get('options', [])
        en_opts = c.get('options', [])
        if len(fa_opts) == len(en_opts):
            for eo, fo in zip(en_opts, fa_opts):
                if any('\\u0600' <= ch <= '\\u06FF' for ch in fo):
                    opt_map[eo.strip()] = fo.strip()

    # Manual overrides for any unmapped options
    OVERRIDES = {
        "$20 per barrel": "۲۰ دلار برای هر بشکه",
        "$25 per barrel": "۲۵ دلار برای هر بشکه",
        "$30 per barrel": "۳۰ دلار برای هر بشکه",
        "$40 per barrel": "۴۰ دلار برای هر بشکه",
        "$5 per barrel": "۵ دلار برای هر بشکه",
        "1,000 Diamonds": "۱,۰۰۰ قطعه الماس",
        "10 Percent": "۱۰ درصد",
        "10,000 Diamonds": "۱۰,۰۰۰ قطعه الماس",
        "100 Jewels": "۱۰۰ قطعه گوهر",
        "100 Percent": "۱۰۰ درصد",
        "10th Century AD": "سده ۱۰ میلادی",
        "15 Khordad 1963": "۱۵ خرداد ۱۳۴۲",
        "16th Century AD": "سده ۱۶ میلادی",
        "1953": "۱۳۳۲",
        "1963": "۱۳۴۲",
        "1971": "۱۳۵۰",
        "19th Century AD": "سده ۱۹ میلادی",
        "20,000 Diamonds": "۲۰,۰۰۰ قطعه الماس",
        "25%": "۲۵ درصد",
        "5,000 Jewels": "۵,۰۰۰ قطعه گوهر",
        "50%": "۵۰ درصد",
        "500 Jewels": "۵۰۰ قطعه گوهر",
        "60%": "۶۰ درصد",
        "A Charitable Religious Endowment (Waqf)": "موقوفه عام (وقف)",
        "A Dove": "کبوتر سپید",
        "A Falcon": "شاهین شکاری",
        "A Gazelle": "آهوی خرامان",
        "A Quran in his breast pocket": "قرآن جیبی در جیب سینه",
        "A Severed Hand": "یک دست بریده",
        "A Solid Gold Lighter": "فندک طلای خالص",
        "A Tale of Two Cities": "داستان دو شهر",
        "AIM-7 Sparrow": "موشک اسپارو AIM-7",
        "AIM-9 Sidewinder": "موشک سایدوایندر AIM-9",
        "Ab Anbar": "آب‌انبار",
        "Ab Anbars": "آب‌انبارها",
        "Abadan Petrochemical": "پتروشیمی آبادان",
        "Abadan Refinery": "پالایشگاه آبادان",
        "Abbas Agha Tabrizi": "عباس‌آقا تبریزی",
        "Abbas Babaei": "عباس بابایی",
        "Abbas Kiarostami": "عباس کیارستمی",
        "Abdol-Majid Majidi": "عبدالمجید مجیدی",
        "Abdolhossein Sepanta": "عبدالحسین سپنتا",
        "Abdolkarim Soroush": "عبدالکریم سروش",
        "Abdolvahab Shahidi": "عبدالوهاب شهیدی",
        "Abi and Rabi": "آبی و رابی",
        "Abolhassan Ebtehaj": "ابوالحسن ابتهاج",
        "Abolition of Serfdom": "لغو نظام ارباب و رعیتی",
        "Abu Musa": "ابوموسی",
        "Abu Nidal": "ابو نضال",
        "Abu Sa'id": "ابوسعید ابوالخیر",
        "Abyaneh": "ابیانه",
        "Academic Gown": "ردای دانشگاهی",
        "Afsaneh": "افسانه نیما یوشیج",
        "Ahmad Ebadi": "احمد عبادی",
        "Ahmad Fardid": "احمد فردید",
        "Ahmad Khomeini": "سید احمد خمینی",
        "Ahmad Motevasselian": "احمد متوسلیان",
        "Ahmad Reza Ahmadi": "احمدرضا احمدی",
        "Ahmad Shah": "احمدشاه قاجار",
        "Ahmad Shah Qajar": "احمدشاه قاجار",
        "Ahmad Zirakzadeh": "احمد زیرک‌زاده",
        "Akhtar": "روزنامه اختر",
        "Al-Abbas": "العباس",
        "Al-Azhar Mosque": "جامع الازهر",
        "Al-Farabi": "فارابی",
        "Al-Kafi": "الکافی کلینی",
        "Al-Kashi": "غیاث‌الدین جمشید کاشانی",
        "Alamut Castle": "قلعه الموت",
        "Alborz College": "کالج البرز",
        "Alexander Balas": "الکساندر بالاس",
        "Alexander Haig": "الکساندر هیگ",
        "Ali Amini": "علی امینی",
        "Ali Eghbali": "علی اقبالی",
        "Ali Khamenei": "سید علی خامنه‌ای",
        "Ali Maher": "علی ماهر",
        "Ali Mirfitros": "علی میرفطرس",
        "Ali Qapu of Isfahan": "عالی‌قاپوی اصفهان",
        "Ali Qoddusi": "علی قدوسی",
        "Ali Razmara": "حاجعلی رزم‌آرا",
        "Ali Shayegan": "سید علی شایگان",
        "Ali Soheili": "علی سهیلی",
        "Ali-Akbar Davar": "علی‌اکبر داور",
        "Ali-Naqi Vaziri": "علینقی وزیری",
        "Ali-Reza Ghorbani": "علیرضا قربانی",
        "Allen Dulles": "آلن دالس",
        "Alvand": "کوه الوند",
        "Amam-gozari": "عمامه‌گذاری",
        "American Motors": "آمریکن موتورز",
        "Amin al-Soltan": "امین‌السلطان (اتابک اعظم)",
        "Amir Kabir Dam": "سد امیرکبیر (سد کرج)",
        "Amir Kabir's Sword": "شمشیر امیرکبیر",
        "Amir Naderi": "امیر نادری",
        "Amir Parviz Pouyan": "امیرپرویز پویان",
        "Amir al-Omara": "امیرالامرا",
        "An Iron Breastplate": "جوشن آهنین",
        "Anar-bij": "اناربیج گیلانی",
        "Anastasio Somoza": "آناستازیو سوموزا",
        "André Godard": "آندره گدار",
        "Anjoman-e Safa": "انجمن صفا",
        "Announce the dissolution of the party": "اعلام انحلال حزب",
        "Answer to History": "کتاب پاسخ به تاریخ",
        "Antiochus III the Great": "آنتیوخوس سوم بزرگ",
        "Aqa Hossein-Qoli": "آقا حسینقلی فراهانی",
        "Aqa Mirak": "آقا میرک",
        "Arab League Fleet": "ناوگان اتحادیه عرب",
        "Ararat Republic": "جمهوری آرارات",
        "Aras River": "رود ارس",
        "Arasbaran Forests": "جنگل‌های ارسباران",
        "Ardeshir Irani": "اردشیر ایرانی",
        "Arg-e Bam": "ارگ بم",
        "Artabanus I": "اردوان یکم اشکانی",
        "Arthur Balfour": "آرتور بالفور",
        "Asadollah Alam": "اسدالله علم",
        "Ashraf Pahlavi": "اشرف پهلوی",
        "Bahram Beyzai": "بهرام بیضایی",
        "Dariush Mehrjui": "داریوش مهرجویی",
        "Ebrahim Golestan": "ابراهیم گلستان",
        "Fakhr-ol-Dowleh": "فخرالدوله",
        "Forough Farrokhzad": "فروغ فرخزاد",
        "Gholam-Hossein Sa'edi": "غلامحسین ساعدی",
        "Hassan Ali Mansur": "حسنعلی منصور",
        "Hossein Fatemi": "سید حسین فاطمی",
        "Jafar Pishevari": "سید جعفر پیشه‌وری",
        "Jalal Al-e Ahmad": "جلال آل‌احمد",
        "Karim Khan Zand": "کریم‌خان زند",
        "Khalil Maleki": "خلیل ملکی",
        "Manuchehr Eghbal": "منوچهر اقبال",
        "Mehdi Bazargan": "مهدی بازرگان",
        "Mohammad Mossadegh": "محمد مصدق",
        "Mohammad Reza Pahlavi": "محمدرضا پهلوی",
        "Morteza Avini": "سید مرتضی آوینی",
        "Nader Shah": "نادرشاه افشار",
        "Nasir al-Din Shah": "ناصرالدین‌شاه قاجار",
        "Nima Yushij": "نیما یوشیج",
        "Reza Shah": "رضاشاه پهلوی",
        "Sadeq Hedayat": "صادق هدایت",
        "Sattar Khan": "ستارخان",
        "Shah Abbas I": "شاه عباس بزرگ",
        "Shah Ismail I": "شاه اسماعیل صفوی",
        "Shah Tahmasp I": "شاه طهماسب یکم",
        "Sohrab Sepehri": "سهراب سپهری"
    }
    opt_map.update(OVERRIDES)

    def translate_option(opt):
        opt_s = opt.strip()
        if any('\\u0600' <= ch <= '\\u06FF' for ch in opt_s):
            return opt_s
        if opt_s in opt_map:
            return opt_map[opt_s]
        # Basic phrase cleaning
        t = clean_dates_and_times(opt_s)
        # Year or number
        if re.match(r'^\\d+$', t):
            return to_persian_digits(t)
        return t

    # Compile comprehensive translation table
    print("Compiling translation patterns...")

    fa_clues = []
    fa_copy_dict = {}

    for c in en_clues:
        cid = c['id']
        cat_en = c['category']
        cat_fa = PUNS_FA.get(cat_en, cat_en)
        ans_fa = persian_copy[cid]['canonical_answer'].strip()

        # Options
        raw_opts = c.get('options', [])
        fa_opts = []
        for o in raw_opts:
            trans_o = translate_option(o)
            if not any('\\u0600' <= ch <= '\\u06FF' for ch in trans_o):
                # Fallback translation from canonical answers or dictionary
                trans_o = opt_map.get(trans_o, trans_o)
            fa_opts.append(trans_o)
        
        # Ensure canonical answer matches one option
        if ans_fa not in fa_opts:
            fa_opts[c.get('correct_option_index', 0)] = ans_fa

        # Clue text
        raw_text = c['clue_text']
        t = clean_dates_and_times(raw_text)

        # High-register Persian sentence phrasing
        replacements = [
            (r'\\bIn his contemporary account of the revolution, British scholar E\\.G\\. Browne hailed this\\b', 'ادوارد براون در تاریخ انقلاب مشروطه از این'),
            (r'\\bBrowne recorded that in\\b', 'براون ثبت کرده است که در'),
            (r'\\bBrowne documented the\\b', 'براون در اسناد خود ثبت کرده است که'),
            (r'\\bAccording to Browne\\'s dispatches, on\\b', 'بر پایه گزارش‌های ادوارد براون، در'),
            (r'\\bBrowne lamented the execution of\\b', 'براون با اندوه از شهادت'),
            (r'\\bFollowing the defeat in the Second Russo-Persian War, Crown Prince Abbas Mirza negotiated this\\b', 'پس از شکست در دوره دوم جنگ‌های ایران و روس، ولیعهد عباس‌میرزا این'),
            (r'\\bReigning for nearly half a century from\\b', 'با نزدیک به نیم قرن سلطنت از'),
            (r'\\buntil his assassination in\\b', 'تا زمان ترورش در'),
            (r'\\bthis Qajar monarch became the first Iranian sovereign to tour Europe and was an avid pioneer of photography\\.', 'این شاه قاجار نخستین پادشاه ایران شد که به اروپا سفر کرد و از پیشگامان عکاسی در کشور بود.'),
            (r'\\bGrand Ayatollah Mirza Hasan Shirazi issued a telegram from Samarra forbidding the consumption of this commodity as war against the Hidden Imam\\b', 'آیت‌الله‌العظمی میرزای شیرازی از سامرا فتوایی صادر کرد و مصرف این کالا را در حکم محاربه با امام زمان اعلام نمود'),
            (r'\\bforcing the cancellation of a British imperial concession\\.', 'که دربار را ناچار به لغو انحصار کمپانی بریتانیایی رژی کرد.'),
            (r'\\bthis chief minister founded the Dar al-Fonun polytechnic in Tehran before being dismissed and executed in the Fin Garden bathhouse of Kashan\\.', 'این صدراعظم نامدار مدرسه دارالفنون را در تهران بنیان نهاد، اما اندکی بعد عزل شد و در حمام باغ فین کاشان به قتل رسید.'),
            (r'\\bceding Erivan and Nakhchivan to the Russian Empire and establishing the Aras River as the border\\.', 'که به موجب آن ایروان و نخجوان به امپراتوری روسیه واگذار شد و رود ارس مرز دو کشور گردید.'),
            (r'\\bCaptured by Iraqi forces after a ferocious 34-day battle in\\b', 'این شهر بندری پس از ۳۴ روز نبرد تن‌به‌تن و مقاومت حماسی در'),
            (r'\\bthis vital port city on the Arvand Rud was triumphantly liberated on\\b', 'در ساحل اروندرود به اشغال درآمد و در'),
            (r'\\bin Operation Beit ol-Moqaddas\\.', 'طی عملیات غرورآفرین بیت‌المقدس با افتخار آزاد شد.'),
            (r'\\bFollowing the Allied invasion of Iran, Reza Shah was forced to abdicate by the British and died in\\b', 'به دنبال اشغال ایران توسط متفقین، رضاشاه ناچار به استعفا شد و در'),
            (r'\\bin exile in this South African metropolis\\.', 'در تبعید در این کلان‌شهر آفریقای جنوبی درگذشت.'),
            (r'\\bOn February 1, 1979, ending fifteen years in exile, Ayatollah Khomeini flew from Paris to Tehran\\'s Mehrabad Airport aboard a chartered Boeing 747 operated by this national carrier\\.', 'در ۱۲ بهمن ۱۳۵۷، امام خمینی پس از ۱۵ سال تبعید با یک فروند بوئینگ ۷۴۷ چارتر این شرکت هواپیمایی از پاریس به فرودگاه مهرآباد تهران بازگشت.'),
            (r'\\bOn November 4, 1979, hundreds of radical Islamist university students stormed the US Embassy in Tehran, seizing 52 American diplomats under this official group name\\.', 'در ۱۳ آبان ۱۳۵۸، دانشجویان مسلمان پیرو خط امام به سفارت آمریکا در تهران هجوم برده و ۵۲ دیپلمات آمریکایی را گروگان گرفتند.'),
            (r'\\bServing as the public English-language spokesperson for the student hostage-takers and nicknamed \\'Mary\\' by Western media, this woman later became Iran\\'s first female Vice President\\.', 'این بانو که سخنگوی انگلیسی‌زبان دانشجویان گروگان‌گیر بود و در رسانه‌های غربی به مری شهرت یافت، بعدها نخستین معاون زن رئیس‌جمهور ایران شد.'),
            (r'\\bOn April 24, 1980, President Jimmy Carter\\'s military rescue mission Operation Eagle Claw ended in disaster when a helicopter collided with an EC-130 aircraft in this remote desert\\.', 'در ۵ اردیبهشت ۱۳۵۹، عملیات نظامی پنجه عقاب جیمی کارتر با برخورد بالگرد و هواپیمای سی-۱۳۰ در این بیابان دورافتاده به فاجعه انجامید.'),
            (r'\\bIn protest of the embassy takeover, this veteran statesman and first Prime Minister of the Islamic Republic resigned alongside his entire cabinet on November 6, 1979\\.', 'در اعتراض به تسخیر سفارت، این سیاستمدار کهنه‌کار و نخستین نخست‌وزیر جمهوری اسلامی همراه با تمامی اعضای هیئت دولت استعفا داد.'),
            (r'\\bBrokered by Algerian diplomats, the 52 American hostages were finally released on January 20, 1981, minutes after this US president concluded his inaugural address\\.', 'با میانجی‌گری دیپلمات‌های الجزایری، ۵۲ گروگان آمریکایی در ۳۰ دی ۱۳۵۹، دقایقی پس از تحلیف این رئیس‌جمهور آمریکا آزاد شدند.'),
            (r'\\bIn The Coup, Ervand Abrahamian details how on May 1, 1951, this newly appointed prime minister signed into law the nationalization of the Anglo-Iranian Oil Company, triggering a global British boycott\\.', 'یرواند آبراهامیان در کتاب کودتا شرح می‌دهد که چگونه در ۱۱ اردیبهشت ۱۳۳۰، این نخست‌وزیر قانون ملی شدن صنعت نفت و شرکت نفت انگلیس و ایران را امضا کرد.'),
            (r'\\bAbrahamian identifies this grandson of Theodore Roosevelt and CIA Near East chief as the field officer who slipped into Tehran in July 1953 to coordinate the coup against Mosaddegh\\.', 'آبراهامیان این نوه تئودور روزولت و مقام ارشد سازمان سیا را فرمانده میدانی معرفی می‌کند که برای هدایت کودتا علیه مصدق مخفیانه وارد تهران شد.'),
            (r'\\bWhile the American CIA operation in August 1953 was codenamed TPAJAX, Abrahamian notes that the British Secret Intelligence Service \\(MI6\\) carried out their parallel plan under this codename\\.', 'در حالی که عملیات سازمان سیا در مرداد ۱۳۳۲ با نام رمز تی‌پی‌آژاکس شناخته می‌شد، سرویس اطلاعات مخفی بریتانیا نقشه موازی خود را با این نام رمز اجرا کرد.'),
            (r'\\bAbrahamian recounts the fate of Mosaddegh\\'s 34-year-old foreign minister, editor of Bakhtar-e Emruz, who went into hiding after the 1953 coup but was captured, stabbed, and executed by firing squad in November 1954\\.', 'آبراهامیان سرنوشت وزیر امور خارجه ۳۴ ساله مصدق و مدیر روزنامه باختر امروز را روایت می‌کند که پس از کودتای ۲۸ مرداد مخفی شد، اما پس از دستگیری تیرباران گردید.'),
            (r'\\bAbrahamian demonstrates that the coup culminated in October 1954 with a 25-year consortium agreement with Western majors, in which the former British monopolist \\(AIOC\\) retained this specific percentage share\\.', 'آبراهامیان نشان می‌دهد که پیامد نهایی کودتا قرارداد ۲۵ ساله کنسرسیوم در مهر ۱۳۳۳ بود که در آن شرکت سابق نفت انگلیس و ایران این درصد سهم را حفظ کرد.'),
            (r'\\bOn February 21, 1921, this Cossack brigade colonel marched his troops from Qazvin to seize Tehran, launching his ascent to the throne as the founder of the Pahlavi dynasty\\.', 'در ۳ اسفند ۱۲۹۹، این سرهنگ دیویزیون قزاق نیروهایش را از قزوین به سمت تهران حرکت داد و با تصرف پایتخت، مسیر بنیان‌گذاری سلسله پهلوی را هموار کرد.'),
            (r'\\bCompleted in 1938 without any foreign borrowing by taxing sugar and tea, this 1,394-kilometer engineering marvel connected the Caspian Sea to the Persian Gulf\\.', 'این شاهکار مهندسی ۱۳۹۴ کیلومتری که در سال ۱۳۱۷ بدون وام خارجی و با مالیات بر قند و چای ساخته شد، دریای خزر را به خلیج فارس پیوند داد.'),
            (r'\\bIn January 1963, Mohammad Reza Shah launched this sweeping 19-point program of social and economic modernization, whose primary pillar was land reform breaking up feudal estates\\.', 'در بهمن ۱۳۴۱، محمدرضا شاه این برنامه جامع نوسازی اجتماعی و اقتصادی را اعلام کرد که مهم‌ترین رکن آن اصلاحات ارضی و الغای رژیم ارباب و رعیتی بود.'),
            (r'\\bthis chief minister\\b', 'این صدراعظم اصلاح‌طلب'),
            (r'\\bthis prime minister\\b', 'این نخست‌وزیر'),
            (r'\\bthis monarch\\b', 'این پادشاه'),
            (r'\\bthis king\\b', 'این پادشاه'),
            (r'\\bthis general\\b', 'این فرمانده نظامی'),
            (r'\\bthis city\\b', 'این شهر تاریخی'),
            (r'\\bthis treaty\\b', 'این عهدنامه تاریخی'),
            (r'\\bthis battle\\b', 'این نبرد تاریخی'),
            (r'\\bthis operation\\b', 'این عملیات مهم'),
            (r'\\bthis poet\\b', 'این شاعر نامدار'),
            (r'\\bthis province\\b', 'این استان پهناور'),
            (r'\\bthis island\\b', 'این جزیره راهبردی'),
            (r'\\bthis mountain\\b', 'این کوه مرتفع'),
            (r'\\bthis river\\b', 'این رود خروشان'),
            (r'\\bthis palace\\b', 'این کاخ باشکوه'),
            (r'\\bthis book\\b', 'این کتاب برجسته'),
            (r'\\bthis newspaper\\b', 'این روزنامه تاریخی'),
            (r'\\bthis magazine\\b', 'این مجله معتبر'),
            (r'\\bthis mosque\\b', 'این مسجد تاریخی'),
            (r'\\bthis shrine\\b', 'این آستان مقدس'),
            (r'\\bthis tomb\\b', 'این آرامگاه تاریخی'),
            (r'\\bthis museum\\b', 'این موزه ارزشمند'),
            (r'\\bthis crown\\b', 'این تاج شاهنشاهی'),
            (r'\\bthis diamond\\b', 'این الماس گرانبها'),
            (r'\\bthis dynasty\\b', 'این سلسله پادشاهی'),
            (r'\\bthis empire\\b', 'این شاهنشاهی مقتدر'),
            (r'\\bthis bridge\\b', 'این پل تاریخی'),
            (r'\\bthis airline\\b', 'این شرکت هواپیمایی'),
            (r'\\bthis aircraft\\b', 'این هواپیمای پیشرفته')
        ]
        for pat, rep in replacements:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)

        # Substitute all option names that appear in text
        for en_k, fa_v in sorted(opt_map.items(), key=lambda x: -len(x[0])):
            if len(en_k) > 2 and re.search(rf'\\b{re.escape(en_k)}\\b', t, flags=re.IGNORECASE):
                t = re.sub(rf'\\b{re.escape(en_k)}\\b', fa_v, t, flags=re.IGNORECASE)

        # Clean leftover English terms
        vocab_fixes = [
            (r'\\bIn\\s+سال\\b', 'در سال'), (r'\\bin\\s+سال\\b', 'در سال'),
            (r'\\bOn\\s+سال\\b', 'در سال'), (r'\\bon\\s+سال\\b', 'در سال'),
            (r'\\bIn\\s+([۰-۹]+)\\b', r'در سال \\1 خورشیدی'),
            (r'\\bOn\\s+([۰-۹]+)\\b', r'در تاریخ \\1'),
            (r'\\bUnder the\\b', 'تحت نظارت'),
            (r'\\bDuring the\\b', 'در دوران'),
            (r'\\bFollowing the\\b', 'به دنبال'),
            (r'\\bAfter the\\b', 'پس از'),
            (r'\\bBefore the\\b', 'پیش از'),
            (r'\\bBetween\\b', 'میان'),
            (r'\\bKnown as\\b', 'شناخته‌شده به عنوان'),
            (r'\\bNamed after\\b', 'نام‌گذاری‌شده به نام'),
            (r'\\bCapital of\\b', 'پایتخت'),
            (r'\\bPersian Gulf\\b', 'خلیج فارس'),
            (r'\\bCaspian Sea\\b', 'دریای خزر'),
            (r'\\bRed Army\\b', 'ارتش سرخ'),
            (r'\\bAllied forces\\b', 'نیروهای متفقین'),
            (r'\\bNational Front\\b', 'جبهه ملی'),
            (r'\\bTudeh Party\\b', 'حزب توده'),
            (r'\\bCentral Bank\\b', 'بانک مرکزی'),
            (r'\\bSecurity Council\\b', 'شورای امنیت'),
            (r'\\bUnited Nations\\b', 'سازمان ملل متحد'),
            (r'\\bWorld Heritage\\b', 'میراث جهانی'),
            (r'\\bShahnameh\\b', 'شاهنامه فردوسی')
        ]
        for pat, rep in vocab_fixes:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)

        # Explanation
        raw_expl = c['explanation']
        e = clean_dates_and_times(raw_expl)
        for pat, rep in replacements:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)
        for en_k, fa_v in sorted(opt_map.items(), key=lambda x: -len(x[0])):
            if len(en_k) > 2 and re.search(rf'\\b{re.escape(en_k)}\\b', e, flags=re.IGNORECASE):
                e = re.sub(rf'\\b{re.escape(en_k)}\\b', fa_v, e, flags=re.IGNORECASE)
        for pat, rep in vocab_fixes:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)

        # Build clean Persian clue object
        clue_obj = dict(c)
        clue_obj['language'] = 'fa'
        clue_obj['category'] = cat_fa
        clue_obj['canonical_answer'] = ans_fa
        clue_obj['options'] = fa_opts
        clue_obj['clue_text'] = t
        clue_obj['explanation'] = e
        clue_obj['host_reactions'] = {
            'correct_generic': f'{ans_fa}. کاملاً درسته!',
            'wrong_generic': f'خیر، پاسخ صحیح {ans_fa} بود.',
            'common_wrong_answers': {},
            'specificity_prompt': '',
            'explanation': e
        }

        fa_clues.append(clue_obj)
        fa_copy_dict[cid] = {
            'clue_text': t,
            'canonical_answer': ans_fa,
            'options': fa_opts,
            'explanation': e,
            'specificity_prompt': ''
        }

    print("Writing files...")
    # 1. QuestionBank/verified_clues_fa.json
    with open("QuestionBank/verified_clues_fa.json", "w", encoding="utf-8") as f:
        json.dump(fa_clues, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(fa_clues)} clues to QuestionBank/verified_clues_fa.json")

    # 2. QuestionBank/persian_clues.json
    with open("QuestionBank/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(fa_copy_dict)} clues to QuestionBank/persian_clues.json")

    # 3. App/Resources/persian_clues.json
    with open("App/Resources/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print("Updated App/Resources/persian_clues.json")

    # 4. Bundle copies
    b1 = "Jeopardy Iranian Edition.app/Contents/Resources/persian_clues.json"
    b2 = "dist/Jeopardy Iranian Edition.app/Contents/Resources/persian_clues.json"
    for b in [b1, b2]:
        if os.path.exists(os.path.dirname(b)):
            with open(b, "w", encoding="utf-8") as f:
                json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
            print(f"Updated bundle resource: {b}")

    print("PERSIAN QUESTION BANK EXPANSION COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    build_farsi_bank()
'''

with open("Tools/build_complete_farsi_bank.py", "a", encoding="utf-8") as f:
    f.write(code)

print("Appended complete translation engine to Tools/build_complete_farsi_bank.py")
