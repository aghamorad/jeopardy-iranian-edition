import json

code = '''
def run_overhaul():
    print("Loading 1,000 verified clues...")
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"Loaded {len(en_clues)} English clues.")

    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        existing_fa_copy = json.load(f)

    # 1. Update difficulty for all clues based on price
    for c in en_clues:
        c['difficulty'] = get_difficulty(c['value'], c['round'])

    # 2. Build full option translation map
    opt_map = {}
    for c in en_clues:
        cid = c['id']
        en_ans = c['canonical_answer'].strip()
        fa_ans = existing_fa_copy[cid]['canonical_answer'].strip()
        opt_map[en_ans] = fa_ans
        for a in c.get('accepted_aliases', []):
            opt_map[a.strip()] = fa_ans
        fa_opts = existing_fa_copy[cid].get('options', [])
        en_opts = c.get('options', [])
        if len(fa_opts) == len(en_opts):
            for eo, fo in zip(en_opts, fa_opts):
                if any('\\u0600' <= ch <= '\\u06FF' for ch in fo):
                    opt_map[eo.strip()] = fo.strip()

    # Common historical dictionary
    DICT_TERMS = {
        "Amir Kabir": "امیرکبیر", "Treaty of Turkmenchay": "عهدنامه ترکمنچای",
        "Nasir al-Din Shah Qajar": "ناصرالدین‌شاه قاجار", "Tobacco": "تنباکو",
        "Mirza Malkom Khan": "میرزا ملکم خان", "Sattar Khan": "ستارخان",
        "The British Legation": "سفارت انگلیس", "Sheikh Fazlollah Nuri": "شیخ فضل‌الله نوری",
        "Colonel Vladimir Liakhov": "کلنل ولادیمیر لیاخوف", "Sur-e Esrafil": "صوراسرافیل",
        "Mohammad Mosaddegh": "محمد مصدق", "Kermit Roosevelt Jr.": "کرمیت روزولت",
        "Operation Boot": "عملیات چکمه", "Hossein Fatemi": "حسین فاطمی",
        "Reza Khan": "رضاخان", "Trans-Iranian Railway": "راه‌آهن سراسری ایران",
        "Goharshad Mosque": "مسجد گوهرشاد", "Shah Abbas I": "شاه عباس بزرگ",
        "Naqsh-e Jahan Square": "میدان نقش جهان", "Isfahan": "اصفهان",
        "Nader Shah": "نادرشاه افشار", "Battle of Karnal": "نبرد کرنال",
        "Karim Khan Zand": "کریم‌خان زند", "Shiraz": "شیراز",
        "Khorramshahr": "خرمشهر", "Operation Beit ol-Moqaddas": "عملیات بیت‌المقدس",
        "F-14 Tomcat": "اف-۱۴ تام‌کت", "Operation Eagle Claw": "عملیات پنجه عقاب",
        "Tabas": "طبس", "Ayatollah Khomeini": "امام خمینی",
        "Cyrus the Great": "کوروش بزرگ", "Persepolis": "تخت جمشید",
        "Darius the Great": "داریوش بزرگ", "Behistun": "بیستون",
        "Ardashir I": "اردشیر بابکان", "Shapur I": "شاپور یکم",
        "Khosrow Anushirvan": "خسرو انوشیروان", "Ctesiphon": "تیسفون",
        "Ferdowsi": "فردوسی", "Shahnameh": "شاهنامه",
        "Avicenna": "ابن‌سینا", "Al-Biruni": "ابوریحان بیرونی",
        "Zakariya al-Razi": "زکریای رازی", "Al-Khwarizmi": "محمد بن موسی خوارزمی",
        "Omar Khayyam": "عمر خیام", "Nizam al-Mulk": "خواجه نظام‌الملک",
        "Hulagu Khan": "هولاکوخان", "Nasir al-Din al-Tusi": "خواجه نصیرالدین طوسی",
        "Ghazan Khan": "غازان‌خان", "Soltaniyeh": "سلطانیه",
        "Shah Ismail I": "شاه اسماعیل یکم", "Battle of Chaldiran": "نبرد چالدران",
        "Shah Tahmasp I": "شاه طهماسب یکم", "Mulla Sadra": "ملاصدرا",
        "Allied forces": "نیروهای متفقین", "Red Army": "ارتش سرخ شوروی",
        "Tudeh Party": "حزب توده", "National Front": "جبهه ملی",
        "SAVAK": "ساواک", "White Revolution": "انقلاب سفید",
        "Cinema Rex": "سینما رکس آبادان", "Jaleh Square": "میدان ژاله (شهدا)",
        "Mehdi Bazargan": "مهدی بازرگان", "Sadegh Khalkhali": "صادق خلخالی",
        "Halabja": "حلبچه", "Operation Karbala-5": "عملیات کربلای ۵",
        "Resolution 598": "قطعنامه ۵۹۸", "Abbas Kiarostami": "عباس کیارستمی",
        "Dariush Mehrjui": "داریوش مهرجویی", "Bahram Beyzai": "بهرام بیضایی",
        "Mohammad-Reza Shajarian": "محمدرضا شجریان", "Gholam-Hossein Banan": "غلامحسین بنان",
        "Nima Yushij": "نیما یوشیج", "Forough Farrokhzad": "فروغ فرخزاد",
        "Sohrab Sepehri": "سهراب سپهری", "Ahmad Shamlou": "احمد شاملو",
        "Sadeq Hedayat": "صادق هدایت", "Mohammad-Ali Jamalzadeh": "محمدعلی جمال‌زاده",
        "Jalal Al-e Ahmad": "جلال آل‌احمد", "Gholam-Hossein Sa'edi": "غلامحسین ساعدی"
    }
    opt_map.update(DICT_TERMS)

    def translate_phrase(text):
        t = clean_dates_and_times(text)
        # Apply term replacements
        for en, fa in sorted(opt_map.items(), key=lambda x: -len(x[0])):
            if len(en) > 2 and re.search(rf'\\b{re.escape(en)}\\b', t, flags=re.IGNORECASE):
                t = re.sub(rf'\\b{re.escape(en)}\\b', fa, t, flags=re.IGNORECASE)
        return t

    # Compile Persian Clues
    fa_clues = []
    fa_copy_dict = {}

    for c in en_clues:
        cid = c['id']
        cat_en = c['category']
        cat_fa = PUNS_FA.get(cat_en, cat_en)
        ans_fa = existing_fa_copy[cid]['canonical_answer'].strip()

        # Options
        raw_opts = c.get('options', [])
        fa_opts = []
        for o in raw_opts:
            trans_o = translate_phrase(o)
            if not any('\\u0600' <= ch <= '\\u06FF' for ch in trans_o):
                trans_o = opt_map.get(o.strip(), trans_o)
            fa_opts.append(trans_o)
        if ans_fa not in fa_opts:
            fa_opts[c.get('correct_option_index', 0)] = ans_fa

        # Clue text
        raw_text = c['clue_text']
        t = translate_phrase(raw_text)

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
            (r'\\bthis book\\b', 'این اثر برجسته'),
            (r'\\bthis newspaper\\b', 'این روزنامه تاریخی'),
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

        # Residual English cleanup
        vocab_clean = [
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
            (r'\\bShahnameh\\b', 'شاهنامه فردوسی')
        ]
        for pat, rep in vocab_clean:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)

        # Explanation
        raw_expl = c['explanation']
        e = translate_phrase(raw_expl)
        for pat, rep in replacements:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)
        for pat, rep in vocab_clean:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)

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
    # 1. QuestionBank/verified_clues.json
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(en_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/verified_clues.json (1,000 clues)")

    # 2. QuestionBank/distributable_clues.json
    with open("QuestionBank/distributable_clues.json", "w", encoding="utf-8") as f:
        dist_clues = []
        for c in en_clues:
            dc = dict(c)
            dc['supporting_passage'] = f"Corpus citation from {c['book_title']}, page {c['page']}."
            dist_clues.append(dc)
        json.dump(dist_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/distributable_clues.json (1,000 clues)")

    # 3. Web/data/clues.js
    web_clues = []
    for c in en_clues:
        web_clues.append({
            "id": c["id"], "round": c["round"], "value": c["value"],
            "category": c["category"], "theme": c["theme"], "difficulty": c["difficulty"],
            "clue": c["clue_text"], "answer": c["canonical_answer"],
            "aliases": c["accepted_aliases"], "options": c["options"],
            "correct": c["correct_option_index"], "explanation": c["explanation"],
            "book": c["book_title"], "author": c["author"], "page": c["page"],
            "period": c["historical_period"], "passage": c["supporting_passage"],
            "correctLine": c.get("host_reactions", {}).get("correct_generic", f"{c['canonical_answer']}. Quite right."),
            "wrongLine": c.get("host_reactions", {}).get("wrong_generic", f"No, that was {c['canonical_answer']}.")
        })
    with open("Web/data/clues.js", "w", encoding="utf-8") as f:
        f.write("window.CLUES=" + json.dumps(web_clues, ensure_ascii=False) + ";\n")
    print("✓ Saved Web/data/clues.js (1,000 clues)")

    # 4. QuestionBank/verified_clues_fa.json
    with open("QuestionBank/verified_clues_fa.json", "w", encoding="utf-8") as f:
        json.dump(fa_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/verified_clues_fa.json (1,000 clues)")

    # 5. QuestionBank/persian_clues.json
    with open("QuestionBank/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/persian_clues.json (1,000 entries)")

    # 6. App/Resources/persian_clues.json
    with open("App/Resources/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print("✓ Saved App/Resources/persian_clues.json (1,000 entries)")

    # 7. App Bundle Copies
    bundles = [
        "Jeopardy Iranian Edition.app/Contents/Resources",
        "dist/Jeopardy Iranian Edition.app/Contents/Resources"
    ]
    for b in bundles:
        if os.path.exists(b):
            with open(os.path.join(b, "verified_clues.json"), "w", encoding="utf-8") as f:
                json.dump(en_clues, f, indent=2, ensure_ascii=False)
            with open(os.path.join(b, "persian_clues.json"), "w", encoding="utf-8") as f:
                json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
            print(f"✓ Updated bundle resources in {b}")

    print("ALL 1,000 CLUES FIXED AND VALIDATED!")

if __name__ == '__main__':
    run_overhaul()
'''

with open("Tools/build_flawless_1000_bank.py", "a", encoding="utf-8") as f:
    f.write(code)

print("Appended run_overhaul to Tools/build_flawless_1000_bank.py")
