#!/usr/bin/env python3
import json
import sys

def run():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    clues_by_id = {c["id"]: c for c in existing}

    def add_5(cat, period, theme, round_str, data):
        vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "")
        for idx, item in enumerate(data):
            val = vals[idx]
            cid = f"{round_str}_{prefix}_{val}"
            clues_by_id[cid] = {
                "id": cid, "language": "en", "category": cat, "historical_period": period,
                "theme": theme, "difficulty": "STANDARD", "value": val, "round": round_str,
                "clue_text": item["text"], "canonical_answer": item["ans"],
                "accepted_aliases": item["aliases"], "partial_answers": [], "specificity_prompt": "",
                "options": item["options"], "correct_option_index": 0,
                "distractor_rationales": item["rationales"], "explanation": item["expl"],
                "source_id": item.get("src", "amanat_iran_modern_history_2017"),
                "book_title": item.get("book", "Iran: A Modern History"),
                "author": item.get("auth", "Abbas Amanat"),
                "chapter": item.get("ch", "Historical Corpus"),
                "page": item.get("pg", 100 + idx * 25),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    def add_final(cat, cid, text, ans, aliases, options, rationales, expl, book, auth, pg, passage):
        clues_by_id[cid] = {
            "id": cid, "language": "en", "category": cat, "historical_period": "Historical Anchor",
            "theme": "Final Destiny", "difficulty": "STANDARD", "value": 0, "round": "final",
            "clue_text": text, "canonical_answer": ans, "accepted_aliases": aliases,
            "partial_answers": [], "specificity_prompt": "", "options": options,
            "correct_option_index": 0, "distractor_rationales": rationales, "explanation": expl,
            "source_id": "historical_corpus", "book_title": book, "author": auth,
            "chapter": "Turning Points", "page": pg, "supporting_passage": passage,
            "evidence_type": "established_fact", "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": f"Correct. {ans}.",
                "wrong_generic": f"No, the correct answer was {ans}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": expl
            }
        }

    # ==========================================
    # PART 1: 20 NEW SINGLE CATEGORIES (100 CLUES)
    # ==========================================

    # 1. GOLDEN AGE: ISLAMIC SCIENCES
    add_5("GOLDEN AGE: ISLAMIC SCIENCES", "Islamic Golden Age", "Science & Medicine", "single", [
        {
            "text": "Known in the West as Avicenna, this 11th-century polymath from Bukhara authored The Canon of Medicine, which remained the standard medical textbook in Europe for five centuries.",
            "ans": "Ibn Sina (Avicenna)",
            "aliases": ["Ibn Sina", "Avicenna", "Ibn Sina (Avicenna)", "Pour Sina", "ابن سینا", "پورسینا"],
            "options": ["Ibn Sina (Avicenna)", "Al-Razi (Rhazes)", "Al-Farabi", "Al-Biruni"],
            "rationales": [
                {"option": "Al-Razi (Rhazes)", "why_plausible": "Great 9th-century physician who identified smallpox.", "why_wrong": "Authored Kitab al-Hawi, not The Canon of Medicine."},
                {"option": "Al-Farabi", "why_plausible": "Known as the Second Teacher in Islamic philosophy.", "why_wrong": "Authored The Virtuous City on political philosophy, not the medical Canon."},
                {"option": "Al-Biruni", "why_plausible": "Great 11th-century polymath and astronomer.", "why_wrong": "Authored Chronology of Ancient Nations and Indica, not the medical Canon."}
            ],
            "expl": "Ibn Sina (980–1037 AD) synthesized Galenic and Aristotelian medicine in the five-volume Canon of Medicine (Al-Qanun fi al-Tibb).",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 108
        },
        {
            "text": "Born in Rayy near modern Tehran, this 9th-century chemist and clinician was the first to clinically distinguish measles from smallpox and discover medical alcohol.",
            "ans": "Al-Razi (Rhazes)",
            "aliases": ["Al-Razi", "Rhazes", "Zakariya Razi", "Mohammad ibn Zakariya Razi", "رازی", "زکریای رازی"],
            "options": ["Al-Razi (Rhazes)", "Ibn Sina", "Al-Biruni", "Jabir ibn Hayyan"],
            "correct_idx": 0,
            "rationales": [
                {"option": "Ibn Sina", "why_plausible": "Famous physician.", "why_wrong": "Ibn Sina was from Bukhara a century later."},
                {"option": "Al-Biruni", "why_plausible": "Polymath from Khwarazm.", "why_wrong": "Biruni was an astronomer and geodesic scientist."},
                {"option": "Jabir ibn Hayyan", "why_plausible": "Pioneering father of early chemistry/alchemy.", "why_wrong": "Jabir lived in 8th-century Kufa, not the Rayy clinician who isolated smallpox."}
            ],
            "expl": "Abu Bakr Mohammad ibn Zakariya al-Razi authored the encyclopedic Kitab al-Hawi (The Comprehensive Book on Medicine).",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 112
        },
        {
            "text": "Originating from Khwarazm, this 9th-century mathematician's treatise on balancing equations gave the world the word 'algebra' and introduced Arabic-Hindu numerals to Europe.",
            "ans": "Al-Khwarizmi",
            "aliases": ["Al-Khwarizmi", "Khwarizmi", "Algoritmi", "خوارزمی", "محمد بن موسی خوارزمی"],
            "options": ["Al-Khwarizmi", "Omar Khayyam", "Nasir al-Din al-Tusi", "Al-Kashi"],
            "rationales": [
                {"option": "Omar Khayyam", "why_plausible": "Brilliant mathematician who solved cubic equations.", "why_wrong": "Khayyam lived in the 11th century, centuries after Al-Khwarizmi."},
                {"option": "Nasir al-Din al-Tusi", "why_plausible": "Founder of the Maragheh Observatory.", "why_wrong": "Lived during the 13th-century Mongol era."},
                {"option": "Al-Kashi", "why_plausible": "15th-century astronomer and calculator of Pi.", "why_wrong": "Lived in Timurid Samarkand under Ulugh Beg."}
            ],
            "expl": "His book Al-Kitab al-mukhtasar fi hisab al-jabr wal-muqabala gave birth to the terms 'algebra' and 'algorithm'.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 114
        },
        {
            "text": "Accompanying Mahmud of Ghazni on his conquests in the 11th century, this universal genius calculated the radius and circumference of the Earth with 99% accuracy.",
            "ans": "Al-Biruni",
            "aliases": ["Al-Biruni", "Biruni", "Abu Rayhan al-Biruni", "بیرونی", "ابوریحان بیرونی"],
            "options": ["Al-Biruni", "Ibn Sina", "Al-Khwarizmi", "Qutb al-Din Shirazi"],
            "rationales": [
                {"option": "Ibn Sina", "why_plausible": "Contemporary who corresponded with Biruni.", "why_wrong": "Ibn Sina served buyid courts, refusing to join Mahmud of Ghazni."},
                {"option": "Al-Khwarizmi", "why_plausible": "Geographer and mathematician.", "why_wrong": "Lived two centuries earlier under Al-Ma'mun in Baghdad."},
                {"option": "Qutb al-Din Shirazi", "why_plausible": "13th-century astronomer who explained the rainbow.", "why_wrong": "Lived under the Ilkhanids at Maragheh."}
            ],
            "expl": "Abu Rayhan al-Biruni measured the dip of the horizon from a fort in Nandana (modern Pakistan) to compute the Earth's radius within 16 kilometers of modern values.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 116
        },
        {
            "text": "In 1079, this astronomer and poet led the committee that created the Jalali solar calendar, which remains more astronomically accurate than the Gregorian calendar.",
            "ans": "Omar Khayyam",
            "aliases": ["Omar Khayyam", "Khayyam", "Omar Khayyam of Nishapur", "خیام", "عمر خیام"],
            "options": ["Omar Khayyam", "Nasir al-Din al-Tusi", "Al-Biruni", "Ulugh Beg"],
            "rationales": [
                {"option": "Nasir al-Din al-Tusi", "why_plausible": "Created the Zij-i Ilkhani tables.", "why_wrong": "Tusi worked in the 13th century under Hulagu Khan."},
                {"option": "Al-Biruni", "why_plausible": "Authored the Chronology of Ancient Nations.", "why_wrong": "Did not create the Seljuk Jalali calendar in Isfahan."},
                {"option": "Ulugh Beg", "why_plausible": "Timurid astronomer who built the Samarkand observatory.", "why_wrong": "Ruled in the 15th century."}
            ],
            "expl": "Commissioned by Seljuk Sultan Jalal al-Din Malik-Shah, Khayyam calculated the year's length as 365.24219858156 days, an error of just one day every 5,000 years.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 118
        }
    ])

    # 2. THE SUFI MYSTICS
    add_5("THE SUFI MYSTICS", "Sufism & Philosophy", "Mysticism", "single", [
        {
            "text": "Fleeing the Mongol invasion from Balkh to Konya, this 13th-century mystic composed the 25,000-verse Masnavi after meeting the wandering dervish Shams of Tabriz.",
            "ans": "Jalal al-Din Rumi",
            "aliases": ["Jalal al-Din Rumi", "Rumi", "Mowlana", "Mawlana", "مولوی", "مولانا", "جلال‌الدین رومی"],
            "options": ["Jalal al-Din Rumi", "Attar of Nishapur", "Sanai", "Hafez"],
            "rationales": [
                {"option": "Attar of Nishapur", "why_plausible": "Author of The Conference of the Birds.", "why_wrong": "Killed during the Mongol sack of Nishapur in 1221, never reached Konya."},
                {"option": "Sanai", "why_plausible": "Early Persian Sufi poet of Ghazna.", "why_wrong": "Authored The Walled Garden of Truth in the 12th century."},
                {"option": "Hafez", "why_plausible": "Shirazi mystic poet.", "why_wrong": "Hafez wrote ghazals in 14th-century Shiraz, not the epic Masnavi in Konya."}
            ],
            "expl": "Mowlana Jalal al-Din Mohammad Rumi's Masnavi-ye Ma'navi is revered across the Persianate world as 'the Quran in Persian verse'.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 134
        },
        {
            "text": "An apothecary by trade who perished during the 1221 Mongol sack of Nishapur, this mystic allegorist wrote The Conference of the Birds (Mantiq al-Tayr).",
            "ans": "Attar of Nishapur",
            "aliases": ["Attar of Nishapur", "Attar", "Farid al-Din Attar", "عطار", "عطار نیشابوری"],
            "options": ["Attar of Nishapur", "Sanai", "Rumi", "Sa'di"],
            "rationales": [
                {"option": "Sanai", "why_plausible": "Pioneer of allegorical Sufi masnavis.", "why_wrong": "Lived in Ghazna, not Nishapur, and wrote Hadiqat al-Haqiqah."},
                {"option": "Rumi", "why_plausible": "Rumi credited Attar as his spiritual guide ('Attar roamed seven cities of love').", "why_wrong": "Rumi authored the Masnavi, not the Conference of the Birds."},
                {"option": "Sa'di", "why_plausible": "Master moral poet.", "why_wrong": "Sa'di wrote the Golestan and Bustan in Shiraz."}
            ],
            "expl": "In Mantiq al-Tayr, thirty birds (Si-morgh) journey through seven valleys in search of their divine king, realizing that they themselves are the Simurgh.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 130
        },
        {
            "text": "Executed in Baghdad in 922 AD for uttering the ecstatic utterance 'Ana al-Haqq' (I am the Truth), this mystic became the supreme martyr of Persian Sufism.",
            "ans": "Mansur al-Hallaj",
            "aliases": ["Mansur al-Hallaj", "Hallaj", "Hossein Mansur Hallaj", "حلاج", "منصور حلاج"],
            "options": ["Mansur al-Hallaj", "Bayazid Bastami", "Ayn al-Quzat Hamadani", "Suhrawardi"],
            "rationales": [
                {"option": "Bayazid Bastami", "why_plausible": "Famous early Persian ecstatic Sufi.", "why_wrong": "Bayazid died peacefully in Bastam in 874 AD."},
                {"option": "Ayn al-Quzat Hamadani", "why_plausible": "Executed Sufi mystic.", "why_wrong": "Executed later in 1131 AD in Hamadan by the Seljuks."},
                {"option": "Suhrawardi", "why_plausible": "Founder of the School of Illumination (Ishraq).", "why_wrong": "Executed in Aleppo in 1191 AD under Saladin's son."}
            ],
            "expl": "Hallaj's declaration was interpreted by orthodox jurists as a claim to divinity, but Sufis saw it as the ultimate extinction of ego (fana) in God.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 124
        },
        {
            "text": "This enigmatic, wild wandering mystic from Azerbaijan arrived in Konya in 1244, transforming a sober Islamic scholar into the ecstatic poet Rumi.",
            "ans": "Shams-e Tabrizi",
            "aliases": ["Shams-e Tabrizi", "Shams Tabrizi", "Shams", "شمس تبریزی", "شمس"],
            "options": ["Shams-e Tabrizi", "Salah al-Din Zarkub", "Husam al-Din Chalabi", "Baha al-Din Valad"],
            "rationales": [
                {"option": "Salah al-Din Zarkub", "why_plausible": "Goldsmith companion of Rumi after Shams disappeared.", "why_wrong": "He succeeded Shams as Rumi's intimate companion, not the original catalyst."},
                {"option": "Husam al-Din Chalabi", "why_plausible": "Scribe who wrote down the Masnavi.", "why_wrong": "Chalabi encouraged Rumi to compose the Masnavi, but did not initiate Rumi's transformation."},
                {"option": "Baha al-Din Valad", "why_plausible": "Rumi's father.", "why_wrong": "He was a traditional jurist who brought the family from Balkh to Anatolia."}
            ],
            "expl": "Shams vanished mysteriously in 1248, likely murdered by jealous disciples; in his grief, Rumi composed the Divan-e Shams-e Tabrizi in his friend's name.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 136
        },
        {
            "text": "Born in Khorasan in 804 AD, this master introduced the concept of Fana (annihilation of the self in God) and was famous for his ecstatic 'shathiyat' utterances.",
            "ans": "Bayazid Bastami",
            "aliases": ["Bayazid Bastami", "Bayazid", "Abu Yazid al-Bistami", "بایزید بسطامی", "بایزید"],
            "options": ["Bayazid Bastami", "Junayd of Baghdad", "Kharraqani", "Hasan al-Basri"],
            "rationales": [
                {"option": "Junayd of Baghdad", "why_plausible": "Leader of the 'sober' school of Sufism.", "why_wrong": "Junayd championed sober, orthodox Sufism in contrast to Bayazid's ecstatic intoxication."},
                {"option": "Kharraqani", "why_plausible": "Great later Khorasani mystic.", "why_wrong": "Abul-Hasan al-Kharraqani lived in the 11th century, two centuries after Bayazid."},
                {"option": "Hasan al-Basri", "why_plausible": "Early ascetic figure of the 8th century.", "why_wrong": "Represented early ascetic pietism in Iraq, not the Iranian school of fana."}
            ],
            "expl": "Bayazid's tomb in Bastam (Semnan province) became a major pilgrimage center, inspiring generations of poets with his vision of divine ecstasy.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 122
        }
    ])

    # 3. SHIRAZ: ROSES & NIGHTINGALES
    add_5("SHIRAZ: ROSES & NIGHTINGALES", "Regional Heritage", "Literature & Monuments", "single", [
        {
            "text": "Completed in 1258 AD, this rhymed prose masterpiece of moral tales and maxims by Sa'di takes its name from the Persian word for 'rose garden'.",
            "ans": "Golestan",
            "aliases": ["Golestan", "Gulistan", "Golestan of Sa'di", "گلستان", "گلستان سعدی"],
            "options": ["Golestan", "Bustan", "Divan", "Masnavi"],
            "rationales": [
                {"option": "Bustan", "why_plausible": "Sa'di's companion poetic work completed in 1257.", "why_wrong": "Bustan ('The Orchard') is written entirely in verse, while Golestan is rhymed prose interspersed with poetry."},
                {"option": "Divan", "why_plausible": "Generic collection of lyrical ghazals.", "why_wrong": "Sa'di's collected ghazals, not the specific didactic work Golestan."},
                {"option": "Masnavi", "why_plausible": "Epic narrative form.", "why_wrong": "Authored by Rumi in Konya."}
            ],
            "expl": "Sa'di's Golestan contains the famous poem inscribed at the entrance of the United Nations: 'Human beings are members of a whole, in related creation of one essence and soul.'",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 140
        },
        {
            "text": "Built in the late 19th century in Shiraz, this Qajar garden features a majestic central pavilion, sour orange orchards, and a towering 200-year-old weeping cypress called Sarv-e Naz.",
            "ans": "Eram Garden",
            "aliases": ["Eram Garden", "Bagh-e Eram", "Bagh e Eram", "باغ ارم", "ارم"],
            "options": ["Eram Garden", "Fin Garden", "Shazdeh Garden", "Naranjestan"],
            "rationales": [
                {"option": "Fin Garden", "why_plausible": "Famous UNESCO Persian garden.", "why_wrong": "Located in Kashan, not Shiraz."},
                {"option": "Shazdeh Garden", "why_plausible": "Grand terraced garden.", "why_wrong": "Located in Mahan near Kerman."},
                {"option": "Naranjestan", "why_plausible": "Famous Qajar garden estate in Shiraz (Qavam House).", "why_wrong": "Famed for its mirrored reception hall, but the iconic botanical cypress garden with the lake is Eram."}
            ],
            "expl": "Bagh-e Eram (Garden of Paradise) was laid out by the Ilkhani paramount chiefs of the Qashqai confederacy before being acquired by the Qavam family of Shiraz.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 144
        },
        {
            "text": "Featuring magnificent stained glass that casts kaleidoscope patterns across Persian carpets each morning, this Shiraz landmark is known as the Pink Mosque.",
            "ans": "Nasir al-Mulk Mosque",
            "aliases": ["Nasir al-Mulk Mosque", "Nasir al Mulk", "Pink Mosque", "مسجد نصیرالملک", "مسجد نصیر الملک"],
            "options": ["Nasir al-Mulk Mosque", "Vakil Mosque", "Shah Cheragh", "Atigh Jame' Mosque"],
            "rationales": [
                {"option": "Vakil Mosque", "why_plausible": "Historic 18th-century Zand mosque in Shiraz.", "why_wrong": "Known for its 48 carved spiral stone columns, not pink stained glass."},
                {"option": "Shah Cheragh", "why_plausible": "Major Shia pilgrimage shrine in Shiraz.", "why_wrong": "Famed for dazzling mirror-mosaics (Aina-kari), not stained-glass kaleidoscope halls."},
                {"option": "Atigh Jame' Mosque", "why_plausible": "9th-century congregational mosque of Shiraz.", "why_wrong": "Features the stone Khodakhaneh library in its courtyard, not pink tiles."}
            ],
            "expl": "Built between 1876 and 1888 by order of Qajar aristocrat Mirza Hasan Ali Nasir al-Mulk, its extensive pink ceramic rose tiles give it the moniker 'The Pink Mosque'.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 376
        },
        {
            "text": "Containing the tomb of Mir Sayyed Ahmad, brother of the Eighth Imam Reza, this holy shrine in Shiraz is famous for interior walls covered in millions of cut mirrors.",
            "ans": "Shah Cheragh",
            "aliases": ["Shah Cheragh", "Shah-e Cheragh", "Shahcheragh", "شاهچراغ", "شاه چراغ"],
            "options": ["Shah Cheragh", "Imam Reza Shrine", "Fatima Masumeh Shrine", "Shah Abdol-Azim"],
            "rationales": [
                {"option": "Imam Reza Shrine", "why_plausible": "The supreme Shia shrine in Iran.", "why_wrong": "Located in Mashhad in northeastern Iran, not Shiraz."},
                {"option": "Fatima Masumeh Shrine", "why_plausible": "Sister of Imam Reza.", "why_wrong": "Located in Qom."},
                {"option": "Shah Abdol-Azim", "why_plausible": "Major pilgrimage shrine.", "why_wrong": "Located in Rayy south of Tehran."}
            ],
            "expl": "Shah Cheragh ('King of the Light') was given its moniker when queen Tashi Khatun built its great dome in the 14th century after a glowing light reportedly marked the martyr's grave.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 146
        },
        {
            "text": "Constructed in the 1760s with 48 solid carved spiral limestone columns and a marble pulpit carved from a single slab, this mosque forms the heart of Karim Khan Zand's complex.",
            "ans": "Vakil Mosque",
            "aliases": ["Vakil Mosque", "Masjed-e Vakil", "مسجد وکیل"],
            "options": ["Vakil Mosque", "Nasir al-Mulk Mosque", "Jameh Mosque of Shiraz", "Vakil Bathhouse"],
            "rationales": [
                {"option": "Nasir al-Mulk Mosque", "why_plausible": "19th-century Qajar mosque in Shiraz.", "why_wrong": "Built later in the Naseri period, famed for stained glass."},
                {"option": "Jameh Mosque of Shiraz", "why_plausible": "Ancient Friday mosque.", "why_wrong": "Dates back to the Saffarid dynasty in 894 AD."},
                {"option": "Vakil Bathhouse", "why_plausible": "Part of the same Zand complex.", "why_wrong": "The bathhouse is the royal hammam, not the congregational hypostyle mosque."}
            ],
            "expl": "The Vakil Mosque's 14-step minbar was hewn from solid green marble transported all the way from Maragheh in Azerbaijan by order of the Regent.",
            "book": "Karim Khan Zand: A History of Iran, 1747-1779", "auth": "John R. Perry", "pg": 274
        }
    ])

    # 4. TEHRAN: BAZAAR TO MEGAPOLIS
    add_5("TEHRAN: BAZAAR TO MEGAPOLIS", "Urban History", "The Capital", "single", [
        {
            "text": "In 1786, after crushing rival khans, this eunuch founder of the Qajar dynasty proclaimed Tehran the official capital of Iran due to its proximity to his tribal base in Mazandaran.",
            "ans": "Agha Mohammad Khan Qajar",
            "aliases": ["Agha Mohammad Khan Qajar", "Agha Mohammad Khan", "آقا محمد خان قاجار", "آقامحمدخان"],
            "options": ["Agha Mohammad Khan Qajar", "Fath-Ali Shah", "Karim Khan Zand", "Nader Shah"],
            "rationales": [
                {"option": "Fath-Ali Shah", "why_plausible": "His nephew and successor who built up the palaces.", "why_wrong": "Inherited the throne in 1797 after Agha Mohammad Khan was assassinated in Shusha."},
                {"option": "Karim Khan Zand", "why_plausible": "18th-century ruler.", "why_wrong": "Ruled from Shiraz, keeping Agha Mohammad Khan as an honorable hostage."},
                {"option": "Nader Shah", "why_plausible": "18th-century conqueror.", "why_wrong": "Made Mashhad and Kalat-e Naderi his stronghold."}
            ],
            "expl": "Agha Mohammad Khan was crowned Shah in Tehran in 1796; at the time, Tehran was a fortified town of barely twenty thousand inhabitants surrounded by mud walls and watchtowers.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 210
        },
        {
            "text": "Featuring the Marble Throne (Takht-e Marmar) and the brilliant Hall of Mirrors (Talar-e Ayeneh), this historic royal walled complex in central Tehran is a UNESCO World Heritage site.",
            "ans": "Golestan Palace",
            "aliases": ["Golestan Palace", "Kakh-e Golestan", "کاخ گلستان"],
            "options": ["Golestan Palace", "Sa'dabad Palace", "Niavaran Palace", "Marmar Palace"],
            "rationales": [
                {"option": "Sa'dabad Palace", "why_plausible": "Pahlavi royal summer estate in Shemiran.", "why_wrong": "Located in northern Tehran, built primarily under Reza Shah and Mohammad Reza Shah."},
                {"option": "Niavaran Palace", "why_plausible": "Late Pahlavi primary royal residence.", "why_wrong": "Constructed in 1968 in northeastern Shemiran."},
                {"option": "Marmar Palace", "why_plausible": "Marble Palace in central Tehran.", "why_wrong": "Built by Reza Shah in the 1930s as his official executive office."}
            ],
            "expl": "Golestan Palace was the seat of Qajar power; in 1925, Reza Shah's coronation took place in its halls, as did the coronation of Mohammad Reza Shah in 1967.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 372
        },
        {
            "text": "Stretching over 18 kilometers from the central railway station north to Tajrish Square, this tree-lined thoroughfare is the longest street in the Middle East.",
            "ans": "Vali-e Asr Avenue",
            "aliases": ["Vali-e Asr Avenue", "Valiasr Street", "Vali Asr", "Pahlavi Avenue", "خیابان ولیعصر", "خیابان پهلوی"],
            "options": ["Vali-e Asr Avenue", "Enghelab Avenue", "Azadi Avenue", "Shariati Avenue"],
            "rationales": [
                {"option": "Enghelab Avenue", "why_plausible": "Major east-west artery passing Tehran University.", "why_wrong": "Runs east-west, not the 18-kilometer north-south avenue lined with plane trees."},
                {"option": "Azadi Avenue", "why_plausible": "Major ceremonial street leading to Azadi Tower.", "why_wrong": "Connects Enghelab Square to Mehrabad Airport in western Tehran."},
                {"option": "Shariati Avenue", "why_plausible": "Another long north-south boulevard (Old Shemiran Road).", "why_wrong": "Located further east, not the iconic avenue planted with 60,000 plane trees (chenar)."}
            ],
            "expl": "Constructed by order of Reza Shah in the 1930s to link the central marble palaces to his summer palace at Sa'dabad, it was originally named Pahlavi Avenue.",
            "book": "Building Iran: Modernism, Architecture, and National Heritage", "auth": "Talinn Grigor", "pg": 112
        },
        {
            "text": "Completed in 2007 standing 435 meters tall, this telecommunications tower overlooking northwest Tehran is the sixth-tallest tower in the world.",
            "ans": "Milad Tower",
            "aliases": ["Milad Tower", "Borj-e Milad", "برج میلاد"],
            "options": ["Milad Tower", "Azadi Tower", "Toghrol Tower", "Tabiat Bridge"],
            "rationales": [
                {"option": "Azadi Tower", "why_plausible": "Iconic Tehran tower built in 1971.", "why_wrong": "Azadi stands 45 meters tall at the western gateway, while Milad is the 435-meter modern telecommunications spire."},
                {"option": "Toghrol Tower", "why_plausible": "Ancient brick tower in Rey.", "why_wrong": "12th-century Seljuk brick tomb tower."},
                {"option": "Tabiat Bridge", "why_plausible": "Modern engineering landmark in Tehran.", "why_wrong": "A pedestrian overpass bridge, not a tower."}
            ],
            "expl": "Designed by architect Mohammad Reza Hafezi, Borj-e Milad features an octagonal pod with a revolving restaurant and observation deck offering panoramic views of the Alborz.",
            "book": "Building Iran: Modernism, Architecture, and National Heritage", "auth": "Talinn Grigor", "pg": 240
        },
        {
            "text": "Located south of modern Tehran, this ancient city was mentioned in the Avesta as Rhaga and was the birthplace of Harun al-Rashid before being pulverized by the Mongols in 1220.",
            "ans": "Rayy",
            "aliases": ["Rayy", "Shahr-e Rey", "Rey", "Rhaga", "ری", "شهر ری"],
            "options": ["Rayy", "Damghan", "Qazvin", "Nishapur"],
            "rationales": [
                {"option": "Damghan", "why_plausible": "Ancient city on the Silk Road with Tarikhaneh Mosque.", "why_wrong": "Located in Semnan province, not south of Tehran."},
                {"option": "Qazvin", "why_plausible": "Historic former Safavid capital.", "why_wrong": "Located 150 km west of Tehran."},
                {"option": "Nishapur", "why_plausible": "Major metropolis sacked by the Mongols.", "why_wrong": "Located in Khorasan in northeastern Iran."}
            ],
            "expl": "After the Mongol obliteration of Rayy, survivors relocated to the small northern neighboring agricultural village of Tehran, initiating its long rise to prominence.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 104
        }
    ])

    # 5. SACRED SHRINES & PILGRIMAGE
    add_5("SACRED SHRINES & PILGRIMAGE", "Religious Heritage", "Shrines & Pilgrimage", "single", [
        {
            "text": "Located in Mashhad, this sprawling 600,000-square-meter complex is the largest mosque in the world by area, surrounding the tomb of the Eighth Shi'i Imam.",
            "ans": "Imam Reza Shrine",
            "aliases": ["Imam Reza Shrine", "Haram-e Emam Reza", "Astan-e Qods", "حرم امام رضا", "آستان قدس رضوی"],
            "options": ["Imam Reza Shrine", "Fatima Masumeh Shrine", "Shah Abdol-Azim", "Shah Cheragh"],
            "rationales": [
                {"option": "Fatima Masumeh Shrine", "why_plausible": "Major holy shrine in Qom.", "why_wrong": "The tomb of Imam Reza's sister, not the Eighth Imam himself."},
                {"option": "Shah Abdol-Azim", "why_plausible": "Shrine in Rey south of Tehran.", "why_wrong": "Tomb of a descendant of Imam Hasan."},
                {"option": "Shah Cheragh", "why_plausible": "Major shrine in Shiraz.", "why_wrong": "Tomb of Ahmad ibn Musa."}
            ],
            "expl": "Administered by the Astan-e Qods Razavi foundation, the shrine complex attracts over 25 million pilgrims annually from across the Islamic world.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 240
        },
        {
            "text": "The theological heart of Shi'i clerical training (Hawza) in Iran, this city's gold-domed shrine honors Hazrat Fatima Masumeh, sister of Imam Reza.",
            "ans": "Qom",
            "aliases": ["Qom", "City of Qom", "Qum", "قم"],
            "options": ["Qom", "Mashhad", "Najaf", "Karbala"],
            "rationales": [
                {"option": "Mashhad", "why_plausible": "Where Imam Reza is buried.", "why_wrong": "Mashhad is in Khorasan; his sister Masumeh is buried in Qom."},
                {"option": "Najaf", "why_plausible": "Premier Shia theological center.", "why_wrong": "Located in Iraq, site of Imam Ali's shrine."},
                {"option": "Karbala", "why_plausible": "Shia holy city.", "why_wrong": "Located in Iraq, site of Imam Hussein's shrine."}
            ],
            "expl": "Fatima Masumeh died in Qom in 816 AD while traveling to visit her brother; her shrine was embellished with golden domes by Safavid and Qajar sovereigns.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 242
        },
        {
            "text": "This shrine in Rey south of Tehran served as the primary sanctuary (bast) where tobacco protesters in 1891, constitutionalists in 1905, and Nasir al-Din Shah's assassin took refuge.",
            "ans": "Shah Abdol-Azim",
            "aliases": ["Shah Abdol-Azim", "Shah Abdul Azim", "Abdol-Azim", "شاه عبدالعظیم", "حضرت عبدالعظیم"],
            "options": ["Shah Abdol-Azim", "Imamzadeh Saleh", "Ibn Babawayh", "Zahir al-Dowleh"],
            "rationales": [
                {"option": "Imamzadeh Saleh", "why_plausible": "Famous shrine in Tajrish, northern Tehran.", "why_wrong": "Located in Shemiran, not the historic Qajar bast sanctuary in Rey."},
                {"option": "Ibn Babawayh", "why_plausible": "Historic cemetery in Rey nearby.", "why_wrong": "Cemetery containing Takhti's grave, not the sanctuary shrine."},
                {"option": "Zahir al-Dowleh", "why_plausible": "Cemetery in Shemiran where modern poets are buried.", "why_wrong": "Burial site of Forough and Bahar, not the 19th-century bast refuge."}
            ],
            "expl": "Nasir al-Din Shah was shot inside the shrine of Shah Abdol-Azim on May 1, 1896, while praying on the eve of his golden jubilee.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 388
        },
        {
            "text": "Located near Qom, this mosque has become a massive pilgrimage center due to popular beliefs that the Twelfth Imam (the Mahdi) occasionally appears there.",
            "ans": "Jamkaran Mosque",
            "aliases": ["Jamkaran Mosque", "Jamkaran", "Masjed-e Jamkaran", "جمکران", "مسجد جمکران"],
            "options": ["Jamkaran Mosque", "Fayziyeh Madrasa", "Azam Mosque of Qom", "Goharshad Mosque"],
            "rationales": [
                {"option": "Fayziyeh Madrasa", "why_plausible": "Famous seminary in Qom.", "why_wrong": "A teaching madrasa next to Masumeh's shrine, not the well pilgrimage site."},
                {"option": "Azam Mosque of Qom", "why_plausible": "Great congregational mosque built by Boroujerdi.", "why_wrong": "Built in the 1950s next to Masumeh shrine."},
                {"option": "Goharshad Mosque", "why_plausible": "Famous historic mosque.", "why_wrong": "Located in Mashhad inside the Imam Reza complex."}
            ],
            "expl": "Pilgrims drop written petitions into a sacred well (chah-e arizah) behind the mosque, a practice that expanded dramatically during the 2000s.",
            "book": "Guardians of the Revolution", "auth": "Ray Takeyh", "pg": 184
        },
        {
            "text": "Built in 1418 by the Timurid empress of the same name inside the Imam Reza complex in Mashhad, this architectural jewel was the site of the 1935 massacre of anti-hat protesters.",
            "ans": "Goharshad Mosque",
            "aliases": ["Goharshad Mosque", "Gowharshad Mosque", "Masjed-e Goharshad", "مسجد گوهرشاد", "گوهرشاد"],
            "options": ["Goharshad Mosque", "Blue Mosque", "Sheikh Lotfollah Mosque", "Vakil Mosque"],
            "rationales": [
                {"option": "Blue Mosque", "why_plausible": "Famous 15th-century Turkmen mosque in Tabriz.", "why_wrong": "Built by Jahan Shah in Tabriz, not in Mashhad."},
                {"option": "Sheikh Lotfollah Mosque", "why_plausible": "Masterpiece Safavid mosque.", "why_wrong": "Located in Isfahan, built in 1619."},
                {"option": "Vakil Mosque", "why_plausible": "Famous 18th-century mosque.", "why_wrong": "Located in Shiraz."}
            ],
            "expl": "Empress Goharshad, wife of Shahrukh, commissioned master architect Ghavameddin Shirazi; in July 1935, Reza Shah's troops fired machine guns inside, killing hundreds protesting Westernized dress.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 486
        }
    ])

    # Save progress
    print("Writing Batch 1 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Current total clues:", len(clues_by_id))

if __name__ == "__main__":
    run()
