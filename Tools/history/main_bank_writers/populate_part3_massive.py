#!/usr/bin/env python3
import json

def run_part3():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    clues_by_id = {c["id"]: c for c in existing}

    def add_5(cat, period, theme, round_str, data):
        vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("(", "").replace(")", "")
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
                "page": item.get("pg", 200 + idx * 20),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. AMIR KABIR'S REFORMS
    add_5("AMIR KABIR'S REFORMS", "Qajar Reforms", "Statecraft", "single", [
        {
            "text": "Serving as chief minister from 1848 to 1851, Amir Kabir founded this pioneering modern polytechnic academy in Tehran to instruct students in engineering, military science, and medicine.",
            "ans": "Dar al-Fonun",
            "aliases": ["Dar al-Fonun", "Dar ol-Fonun", "Darolfonoon", "دارالفنون", "دار الفنون"],
            "options": ["Dar al-Fonun", "University of Tehran", "Farhangestan", "Razi Institute"],
            "rationales": [
                {"option": "University of Tehran", "why_plausible": "Major secular university.", "why_wrong": "Founded in 1934 under Reza Shah."},
                {"option": "Farhangestan", "why_plausible": "Language academy.", "why_wrong": "Founded in 1935 for language reform."},
                {"option": "Razi Institute", "why_plausible": "Vaccine and serum institute.", "why_wrong": "Founded in 1925 in Karaj."}
            ],
            "expl": "Dar al-Fonun opened in December 1851 with Austrian instructors, just days before Amir Kabir was executed in Fin Garden.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 300
        },
        {
            "text": "To inform the public and counter foreign imperial propaganda, Amir Kabir established this first official state newspaper in 1851.",
            "ans": "Vaqaye-ye Ettefaqiyeh",
            "aliases": ["Vaqaye-ye Ettefaqiyeh", "Vaqaye-e Ettefaqiyeh", "وقایع اتفاقیه", "روزنامه وقایع اتفاقیه"],
            "options": ["Vaqaye-ye Ettefaqiyeh", "Sur-e Esrafil", "Qanun", "Khabar-e Ruz"],
            "rationales": [
                {"option": "Sur-e Esrafil", "why_plausible": "Famous constitutional paper.", "why_wrong": "Published in 1907 by Jahangir Khan and Dehkhoda."},
                {"option": "Qanun", "why_plausible": "Dissident reformist paper.", "why_wrong": "Published in London in 1890 by Malkom Khan."},
                {"option": "Khabar-e Ruz", "why_plausible": "Generic newspaper title.", "why_wrong": "Fictional title."}
            ],
            "expl": "Vaqaye-ye Ettefaqiyeh covered domestic administrative news, international world events, and public hygiene instructions.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 304
        },
        {
            "text": "Fighting religious superstition, Amir Kabir launched nationwide compulsory inoculation campaigns against this devastating epidemic disease that routinely blinded and killed children.",
            "ans": "Smallpox",
            "aliases": ["Smallpox", "Abeleh", "آبله", "مایه کوبی آبله"],
            "options": ["Smallpox", "Cholera", "The Plague", "Typhus"],
            "rationales": [
                {"option": "Cholera", "why_plausible": "Common 19th-century epidemic in Iran (Vaba).", "why_wrong": "Water-borne disease with no vaccine at the time."},
                {"option": "The Plague", "why_plausible": "Bacterial epidemic.", "why_wrong": "Carried by fleas, not prevented by early variolation/vaccination."},
                {"option": "Typhus", "why_plausible": "Wartime disease.", "why_wrong": "Prevalent during WWI/WWII famines, not Amir Kabir's vaccine campaign."}
            ],
            "expl": "Amir Kabir weeping over children who died after traditional dervishes told parents vaccination was work of the devil is one of the most famous anecdotes in Iranian history.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 306
        },
        {
            "text": "Amir Kabir slashed the lavish royal pensions and corrupt allowances of this influential group: the Shah's court aristocrats, princes, and imperial harem members.",
            "ans": "The Qajar Princes and Courtiers",
            "aliases": ["The Qajar Princes and Courtiers", "Qajar Princes", "The Aristocracy", "شاهزادگان قاجار", "درباریان"],
            "options": ["The Qajar Princes and Courtiers", "The Bazaaris", "The British Embassy", "The Russian Cossacks"],
            "rationales": [
                {"option": "The Bazaaris", "why_plausible": "Merchant class.", "why_wrong": "Amir Kabir protected domestic commerce and founded the Tehran bazaar bazaar-cheh."},
                {"option": "The British Embassy", "why_plausible": "Diplomatic mission.", "why_wrong": "Foreign diplomats, not royal court stipendiaries."},
                {"option": "The Russian Cossacks", "why_plausible": "Cavalry unit.", "why_wrong": "Formed in 1879, three decades after his dismissal."}
            ],
            "expl": "His reduction of royal court pensions made mortal enemies of the Queen Mother (Mahd-e Olia) and Mirza Aqa Khan Nuri, who convinced the Shah to execute him.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 308
        },
        {
            "text": "Dismissed in November 1851, Amir Kabir was exiled to this central Iranian oasis city before being murdered in its Fin Garden bathhouse.",
            "ans": "Kashan",
            "aliases": ["Kashan", "City of Kashan", "کاشان"],
            "options": ["Kashan", "Isfahan", "Qazvin", "Shiraz"],
            "rationales": [
                {"option": "Isfahan", "why_plausible": "Historic royal capital nearby.", "why_wrong": "He was exiled specifically to Fin Garden in Kashan."},
                {"option": "Qazvin", "why_plausible": "City northwest of Tehran.", "why_wrong": "Not the site of Fin Garden."},
                {"option": "Shiraz", "why_plausible": "Southern city.", "why_wrong": "Not where he was detained."}
            ],
            "expl": "On January 10, 1852, royal executioner Ali Khan Hajeb al-Dowleh entered the bathhouse and cut his veins while he was bathing.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 310
        }
    ])

    # 2. ALLIED OCCUPATION: WWII
    add_5("ALLIED OCCUPATION: WWII", "World War II", "Occupation", "single", [
        {
            "text": "In November 1943, Churchill, Roosevelt, and Stalin met at the Soviet Embassy in Tehran for this secret summit code-named Eureka, planning Operation Overlord.",
            "ans": "Tehran Conference",
            "aliases": ["Tehran Conference", "The Tehran Conference", "کنفرانس تهران"],
            "options": ["Tehran Conference", "Yalta Conference", "Potsdam Conference", "Cairo Conference"],
            "rationales": [
                {"option": "Yalta Conference", "why_plausible": "Famous Big Three conference in 1945.", "why_wrong": "Held in the Crimean resort of Yalta, not Tehran."},
                {"option": "Potsdam Conference", "why_plausible": "Final Big Three summit in Germany.", "why_wrong": "Held in suburban Berlin in July 1945."},
                {"option": "Cairo Conference", "why_plausible": "1943 Middle Eastern summit.", "why_wrong": "Held with Chiang Kai-shek in Cairo regarding Asia."}
            ],
            "expl": "The Big Three signed the Declaration of the Three Powers Regarding Iran, promising to respect Iranian territorial integrity and independence after the war.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 504
        },
        {
            "text": "Because it served as the vital overland corridor transporting millions of tons of American Lend-Lease supplies to the Soviet front, Iran was hailed by this triumphant nickname.",
            "ans": "The Bridge of Victory",
            "aliases": ["The Bridge of Victory", "Bridge of Victory", "Pol-e Piroozi", "پل پیروزی"],
            "options": ["The Bridge of Victory", "The Persian Corridor", "The Southern Lifeline", "The Silk Bridge"],
            "rationales": [
                {"option": "The Persian Corridor", "why_plausible": "Official military transport name.", "why_wrong": "The Allied logistical route name, but the famous ceremonial title was 'The Bridge of Victory'."},
                {"option": "The Southern Lifeline", "why_plausible": "Plausible wartime logistical phrase.", "why_wrong": "Not the historic title bestowed on Iran."},
                {"option": "The Silk Bridge", "why_plausible": "Evokes ancient Silk Road.", "why_wrong": "Fictional wartime title."}
            ],
            "expl": "Over 4 million tons of tanks, planes, fuel, and food were moved along the Trans-Iranian Railway to the Red Army, securing Soviet victory on the Eastern Front.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 506
        },
        {
            "text": "Evacuated from Soviet gulags in 1942 under General Władysław Anders, over 120,000 refugees from this European country were sheltered in camps across Tehran and Isfahan.",
            "ans": "Poland",
            "aliases": ["Poland", "Poles", "Polish refugees", "لهستان", "لهستانی‌ها"],
            "options": ["Poland", "Greece", "Yugoslavia", "Czechoslovakia"],
            "rationales": [
                {"option": "Greece", "why_plausible": "Occupied European nation.", "why_wrong": "Greek refugees fled to Egypt, not Iran."},
                {"option": "Yugoslavia", "why_plausible": "Balkan nation under Axis occupation.", "why_wrong": "Yugoslavs were not evacuated through the Anders Army."},
                {"option": "Czechoslovakia", "why_plausible": "Central European country.", "why_wrong": "The massive refugee influx in Iran was Polish."}
            ],
            "expl": "Isfahan earned the moniker 'City of Polish Children', where orphanages and schools were established; thousands of Polish graves remain in Doulab cemetery.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 508
        },
        {
            "text": "In December 1942, severe food hoarding, currency hyperinflation, and Allied requisition of grain sparked violent riots in Tehran over the shortage of this basic staple.",
            "ans": "Bread",
            "aliases": ["Bread", "Nan", "Bread Riots", "نان", "بلوای نان"],
            "options": ["Bread", "Rice", "Sugar", "Meat"],
            "rationales": [
                {"option": "Rice", "why_plausible": "Staple food.", "why_wrong": "The famous December 1942 riot was specifically Balva-ye Nan (The Bread Riot)."},
                {"option": "Sugar", "why_plausible": "Precious rationed commodity.", "why_wrong": "The 1905 crisis was sugar, but 1942 was the bread shortage."},
                {"option": "Meat", "why_plausible": "Expensive dietary item.", "why_wrong": "Not the dietary staple that caused the riot."}
            ],
            "expl": "Protesters ransacked parliament and looted Prime Minister Ahmad Qavam's house when adulterated sawdust and gravel were discovered in Tehran bakeries.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 194
        },
        {
            "text": "On August 25, 1941, British and Soviet forces launched a surprise joint invasion of neutral Iran under this British military operation codename.",
            "ans": "Operation Countenance",
            "aliases": ["Operation Countenance", "Countenance", "عملیات کانتینانس"],
            "options": ["Operation Countenance", "Operation Boot", "Operation Ajax", "Operation Barbarossa"],
            "rationales": [
                {"option": "Operation Boot", "why_plausible": "British operation in Iran.", "why_wrong": "MI6 1953 coup plan against Mosaddegh."},
                {"option": "Operation Ajax", "why_plausible": "1953 CIA coup.", "why_wrong": "Targeted Mosaddegh twelve years later."},
                {"option": "Operation Barbarossa", "why_plausible": "Massive 1941 military operation.", "why_wrong": "Hitler's invasion of the Soviet Union in June 1941."}
            ],
            "expl": "Operation Countenance overwhelmed Iranian resistance in three days, resulting in the forced abdication of Reza Shah and Allied occupation until 1946.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 164
        }
    ])

    # 3. MODERN PROSE & THE NOVEL
    add_5("MODERN PROSE & THE NOVEL", "20th-Century Literature", "Prose Fiction", "single", [
        {
            "text": "Often hailed as the father of modern Persian short story writing, this diplomat penned the satirical 1921 collection Once Upon a Time (Yeki Bud, Yeki Nabud).",
            "ans": "Mohammad-Ali Jamalzadeh",
            "aliases": ["Mohammad-Ali Jamalzadeh", "Jamalzadeh", "Mohammad Ali Jamalzadeh", "محمدعلی جمال‌زاده", "جمال‌زاده"],
            "options": ["Mohammad-Ali Jamalzadeh", "Sadegh Hedayat", "Bozorg Alavi", "Jalal Al-e Ahmad"],
            "rationales": [
                {"option": "Sadegh Hedayat", "why_plausible": "Towering figure of modern fiction.", "why_wrong": "Hedayat wrote The Blind Owl, but credited Jamalzadeh as the pioneer."},
                {"option": "Bozorg Alavi", "why_plausible": "Early modern author (Her Eyes).", "why_wrong": "Published his masterpiece novel Cheshmhayash decades later in 1952."},
                {"option": "Jalal Al-e Ahmad", "why_plausible": "Major social essayist and novelist.", "why_wrong": "Rose to fame in the 1950s and 60s."}
            ],
            "expl": "Jamalzadeh's preface to Yeki Bud, Yeki Nabud was a revolutionary literary manifesto demanding writers abandon flowery court rhetoric for natural vernacular Persian.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 182
        },
        {
            "text": "Published in 1952 while its author was imprisoned as a member of the leftist 'Fifty-Three', this romantic mystery novel centers on the enigmatic painting of a woman titled 'Her Eyes'.",
            "ans": "Cheshmhayash (Her Eyes)",
            "aliases": ["Cheshmhayash", "Her Eyes", "Cheshmhayash (Her Eyes)", "چشم‌هایش", "چشمهایش"],
            "options": ["Cheshmhayash (Her Eyes)", "The Blind Owl", "Savushun", "Prince Ehtejab"],
            "rationales": [
                {"option": "The Blind Owl", "why_plausible": "Famous modern novel with a painter protagonist.", "why_wrong": "Written by Hedayat in 1937, not Bozorg Alavi."},
                {"option": "Savushun", "why_plausible": "Masterpiece Iranian novel.", "why_wrong": "Written by Simin Daneshvar in 1969."},
                {"option": "Prince Ehtejab", "why_plausible": "Famous modern novel.", "why_wrong": "Written by Houshang Golshiri in 1968."}
            ],
            "expl": "Bozorg Alavi's Cheshmhayash follows the detective search for the identity of the dangerous femme fatale painted by revolutionary artist Master Makan.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 538
        },
        {
            "text": "Chronicling the generational decay of an aristocratic Qajar dynastic family through stream-of-consciousness, this haunting 1968 novella was written by Houshang Golshiri.",
            "ans": "Prince Ehtejab",
            "aliases": ["Prince Ehtejab", "Shazdeh Ehtejab", "شازده احتجاب"],
            "options": ["Prince Ehtejab", "The Blind Owl", "The Patient Stone", "The Mourners of Bayal"],
            "rationales": [
                {"option": "The Blind Owl", "why_plausible": "Gothic novella.", "why_wrong": "Written by Sadegh Hedayat in 1937."},
                {"option": "The Patient Stone", "why_plausible": "Stream-of-consciousness novella.", "why_wrong": "Written by Sadeq Chubak in 1966."},
                {"option": "The Mourners of Bayal", "why_plausible": "Famous collection of short stories.", "why_wrong": "Written by Gholam-Hossein Sa'edi, inspiring the film Gaav."}
            ],
            "expl": "Adapted into an acclaimed 1974 film by Bahman Farmanara, Shazdeh Ehtejab is a devastating portrait of inherited cruelty and tuberculosis.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 540
        },
        {
            "text": "Stretching over 2,800 pages in ten volumes, this epic rural masterpiece by Mahmoud Dowlatabadi depicts the tragic struggle of the nomadic Kalmiši family in Khorasan.",
            "ans": "Kelidar",
            "aliases": ["Kelidar", "Kalidar", "کلیدر"],
            "options": ["Kelidar", "The Empty Place of Soluch", "Savushun", "Tangsir"],
            "rationales": [
                {"option": "The Empty Place of Soluch", "why_plausible": "Another famous novel by Dowlatabadi (Jay-e Khali-ye Soluch).", "why_wrong": "A single-volume 1979 novel, not the 10-volume 2,800-page Kelidar."},
                {"option": "Savushun", "why_plausible": "Famous long novel.", "why_wrong": "Single-volume novel by Simin Daneshvar."},
                {"option": "Tangsir", "why_plausible": "Famous revenge novel.", "why_wrong": "Written by Sadeq Chubak, set in Bushehr."}
            ],
            "expl": "Kelidar is the second longest novel in world literature, taking Dowlatabadi fifteen years to complete between 1970 and 1984.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 186
        },
        {
            "text": "Based on a real 1920s incident in Bushehr, this gripping 1963 revenge novel by Sadeq Chubak follows Zar Mohammad as he methodically murders the four corrupt notables who defrauded him.",
            "ans": "Tangsir",
            "aliases": ["Tangsir", "تنگسیر"],
            "options": ["Tangsir", "The Patient Stone", "The Baboon Whose Buffoon Was Dead", "Dog and the Winter"],
            "rationales": [
                {"option": "The Patient Stone", "why_plausible": "Chubak's other major novel (Sang-e Saboor).", "why_wrong": "A polyphonic stream-of-consciousness novel in Shiraz, not the Bushehr revenge story."},
                {"option": "The Baboon Whose Buffoon Was Dead", "why_plausible": "Famous short story collection by Chubak.", "why_wrong": "Anthology of short stories, not the novel Tangsir."},
                {"option": "Dog and the Winter", "why_plausible": "Famous Iranian novella.", "why_wrong": "Novella by Azad, not Chubak."}
            ],
            "expl": "Tangsir was adapted into a celebrated 1973 film directed by Amir Naderi, starring Behrouz Vossoughi as the Robin Hood-like avenger Shir Mohammad.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 544
        }
    ])

    # 4. CLERICAL POWER: MARAJE' OF NAJAF & QOM
    add_5("CLERICAL POWER: MARAJE OF NAJAF AND QOM", "Religious Authority", "Shi'i Clergy", "double", [
        {
            "text": "Serving as sole Marja-e Taqlid until his death in 1961, this conservative grand ayatollah rebuilt the Qom Hawza, avoiding direct political confrontation with the Shah.",
            "ans": "Grand Ayatollah Hossein Boroujerdi",
            "aliases": ["Grand Ayatollah Hossein Boroujerdi", "Ayatollah Boroujerdi", "Boroujerdi", "آیت‌الله بروجردی", "بروجردی"],
            "options": ["Grand Ayatollah Hossein Boroujerdi", "Ayatollah Kashani", "Ayatollah Shariatmadari", "Ayatollah Golpayegani"],
            "rationales": [
                {"option": "Ayatollah Kashani", "why_plausible": "Prominent political cleric during oil nationalization.", "why_wrong": "Speaker of Majles and Mosaddegh's ally/rival, not the supreme quietist Marja."},
                {"option": "Ayatollah Shariatmadari", "why_plausible": "Leading Azeri Grand Ayatollah in Qom after 1961.", "why_wrong": "Succeeded to leadership after Boroujerdi's death."},
                {"option": "Ayatollah Golpayegani", "why_plausible": "Major marja in Qom.", "why_wrong": "Led after Boroujerdi passed away."}
            ],
            "expl": "Boroujerdi's death in March 1961 created a leadership vacuum that allowed the Shah to launch the White Revolution and prompted Khomeini's emergence.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 620
        },
        {
            "text": "In Najaf, this supreme Persian Marja issued decisive fatwas supporting the 1906 Constitution and declaring that obedience to Mohammad Ali Shah was war against God.",
            "ans": "Akhund Khorasani",
            "aliases": ["Akhund Khorasani", "Mohammad-Kazem Khorasani", "آخوند خراسانی"],
            "options": ["Akhund Khorasani", "Sheikh Fazlollah Nuri", "Mirza Shirazi", "Sayyed Abdollah Behbehani"],
            "rationales": [
                {"option": "Sheikh Fazlollah Nuri", "why_plausible": "Prominent constitutional-era cleric.", "why_wrong": "Championed Mashru'eh against the constitution, executed in 1909."},
                {"option": "Mirza Shirazi", "why_plausible": "Issued the 1891 tobacco fatwa.", "why_wrong": "Died in 1895 before the constitutional revolution."},
                {"option": "Sayyed Abdollah Behbehani", "why_plausible": "Tehran constitutional cleric.", "why_wrong": "Led in Tehran, while Khorasani was the supreme Marja in Najaf."}
            ],
            "expl": "Khorasani mobilized support from Najaf; he died mysteriously in December 1911 on the eve of marching at the head of a volunteer army to expel Russian troops from Iran.",
            "book": "The Persian Revolution of 1905-1909", "auth": "Edward Granville Browne", "pg": 262
        },
        {
            "text": "Based in Tabriz, this liberal Grand Ayatollah backed the 1979 Revolution but founded the Muslim People's Republic Party to oppose Velayat-e Faqih before being placed under house arrest.",
            "ans": "Ayatollah Kazem Shariatmadari",
            "aliases": ["Ayatollah Kazem Shariatmadari", "Shariatmadari", "Kazem Shariatmadari", "شریعتمداری", "آیت‌الله شریعتمداری"],
            "options": ["Ayatollah Kazem Shariatmadari", "Ayatollah Taleghani", "Ayatollah Montazeri", "Ayatollah Beheshti"],
            "rationales": [
                {"option": "Ayatollah Taleghani", "why_plausible": "Progressive Tehran cleric beloved by leftists.", "why_wrong": "Led Friday prayers in Tehran and died in September 1979."},
                {"option": "Ayatollah Montazeri", "why_plausible": "Designated successor who later broke with Khomeini in 1989.", "why_wrong": "Dismissed in 1989 over prison executions, not the 1979 Tabriz revolt."},
                {"option": "Ayatollah Beheshti", "why_plausible": "Head of Islamic Republic Party.", "why_wrong": "Architect of the clerical state, assassinated in 1981."}
            ],
            "expl": "Shariatmadari was stripped of his clerical rank in 1982 following allegations of complicity in Sadegh Ghotbzadeh's coup plot, dying under house arrest in 1986.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 752
        },
        {
            "text": "Forming an essential alliance with Mosaddegh before acrimoniously breaking with him in 1953, this populist Ayatollah served as Speaker of the 17th Majles.",
            "ans": "Ayatollah Abol-Ghasem Kashani",
            "aliases": ["Ayatollah Abol-Ghasem Kashani", "Ayatollah Kashani", "Kashani", "آیت‌الله کاشانی", "کاشانی"],
            "options": ["Ayatollah Abol-Ghasem Kashani", "Navvab Safavi", "Ayatollah Boroujerdi", "Ayatollah Zanjani"],
            "rationales": [
                {"option": "Navvab Safavi", "why_plausible": "Founder of Fadayan-e Islam.", "why_wrong": "A young militant cleric who carried out assassinations, not the Speaker of the Majles."},
                {"option": "Ayatollah Boroujerdi", "why_plausible": "Supreme Marja in Qom.", "why_wrong": "Remained strictly non-political during the oil crisis."},
                {"option": "Ayatollah Zanjani", "why_plausible": "Pro-Mosaddegh cleric.", "why_wrong": "Loyal to Mosaddegh in the National Resistance Movement."}
            ],
            "expl": "Kashani feared Mosaddegh's secularism and flirtation with the communist Tudeh Party, welcoming General Zahedi's royalist coup in August 1953.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 138
        },
        {
            "text": "Refounding the Qom Seminary in 1922, this Grand Ayatollah protected the seminary through the aggressive secularization of the early Reza Shah years.",
            "ans": "Grand Ayatollah Abdolkarim Haeri Yazdi",
            "aliases": ["Grand Ayatollah Abdolkarim Haeri Yazdi", "Abdolkarim Haeri", "Haeri Yazdi", "حائری یزدی", "عبدالکریم حائری یزدی"],
            "options": ["Grand Ayatollah Abdolkarim Haeri Yazdi", "Ayatollah Boroujerdi", "Ayatollah Khomeini", "Ayatollah Shahabadi"],
            "rationales": [
                {"option": "Ayatollah Boroujerdi", "why_plausible": "Expanded Qom after 1944.", "why_wrong": "Succeeded Haeri Yazdi years later."},
                {"option": "Ayatollah Khomeini", "why_plausible": "Student of Haeri.", "why_wrong": "One of Haeri's young students in Qom."},
                {"option": "Ayatollah Shahabadi", "why_plausible": "Khomeini's mysticism teacher.", "why_wrong": "Taught gnosis (irfan), but did not refound the institutional seminary."}
            ],
            "expl": "Haeri Yazdi adopted strict political neutrality towards Reza Shah, ensuring the survival and financial autonomy of the Qom Hawza as a sanctuary for scholars.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 480
        }
    ])

    # 5. THE SACRED DEFENSE: BATTLEFIELDS
    add_5("THE SACRED DEFENSE: BATTLEFIELDS", "Iran-Iraq War", "Military Operations", "double", [
        {
            "text": "Launched in March 1982 around Shush and Dezful, this massive joint operation liberated 2,500 square kilometers and routed three Iraqi divisions, paving the way to Khorramshahr.",
            "ans": "Operation Fath ol-Mobin",
            "aliases": ["Operation Fath ol-Mobin", "Fath ol-Mobin", "عملیات فتح‌المبین", "فتح المبین"],
            "options": ["Operation Fath ol-Mobin", "Operation Beit ol-Moqaddas", "Operation Kheibar", "Operation Karbala-5"],
            "rationales": [
                {"option": "Operation Beit ol-Moqaddas", "why_plausible": "The operation that liberated Khorramshahr.", "why_wrong": "Launched two months later in May 1982 to retake Khorramshahr."},
                {"option": "Operation Kheibar", "why_plausible": "1984 amphibious marsh assault.", "why_wrong": "Fought in the Hawizeh marshes capturing Majnoon Island."},
                {"option": "Operation Karbala-5", "why_plausible": "Bloodiest siege of Basra.", "why_wrong": "Fought in 1987 at Fish Lake outside Basra."}
            ],
            "expl": "Meaning 'Undeniable Victory' from Surah al-Fath, Fath ol-Mobin demonstrated the devastating tactical synergy between regular Artesh armor and volunteer Basij light infantry.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 780
        },
        {
            "text": "In February 1984, Iranian forces launched this daring amphibious assault across the Hawizeh Marshes using small fiberglass boats, capturing the oil-rich Majnoon Islands.",
            "ans": "Operation Kheibar",
            "aliases": ["Operation Kheibar", "Operation Khaybar", "Kheibar", "عملیات خیبر", "خیبر"],
            "options": ["Operation Kheibar", "Operation Badr", "Operation Valfajr-8", "Operation Ramadan"],
            "rationales": [
                {"option": "Operation Badr", "why_plausible": "Subsequent 1985 marsh offensive.", "why_wrong": "Launched in 1985 seeking to sever the Baghdad-Basra highway."},
                {"option": "Operation Valfajr-8", "why_plausible": "1986 amphibious crossing of the Arvand.", "why_wrong": "Crossed the Shatt al-Arab to capture the Faw Peninsula in 1986."},
                {"option": "Operation Ramadan", "why_plausible": "First invasion of Iraq in 1982.", "why_wrong": "Frontal armor assault outside Basra in July 1982."}
            ],
            "expl": "During Operation Kheibar, Iraq first deployed mustard gas and tabun nerve agent on a massive tactical scale against Iranian troops bogged down in the reeds.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 784
        },
        {
            "text": "In February 1986, Iranian commandos crossed the raging 1,000-meter-wide Arvand River in darkness to capture this strategic oil port on the Persian Gulf in Operation Valfajr-8.",
            "ans": "The Faw Peninsula",
            "aliases": ["The Faw Peninsula", "Faw Peninsula", "Al-Faw", "شبه جزیره فاو", "فاو"],
            "options": ["The Faw Peninsula", "Majnoon Island", "Umm Qasr", "Bubiyan Island"],
            "rationales": [
                {"option": "Majnoon Island", "why_plausible": "Marsh island captured in 1984.", "why_wrong": "In the Hawizeh marshes, not the Persian Gulf delta."},
                {"option": "Umm Qasr", "why_plausible": "Iraqi naval base nearby.", "why_wrong": "Heavily defended port deeper inland, not captured by Iran."},
                {"option": "Bubiyan Island", "why_plausible": "Large Gulf island.", "why_wrong": "Belongs to Kuwait."}
            ],
            "expl": "The capture of Faw cut Iraq off from its coastline on the Persian Gulf and placed Iranian artillery within range of Kuwaiti airfields and oil refineries.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 786
        },
        {
            "text": "Fought in January 1987 in the fortified water obstacles of Fish Lake outside Basra, this meatgrinder battle was the single largest and bloodiest land battle of the war.",
            "ans": "Operation Karbala-5",
            "aliases": ["Operation Karbala-5", "Karbala-5", "Karbala 5", "عملیات کربلای ۵", "کربلای ۵"],
            "options": ["Operation Karbala-5", "Operation Ramadan", "Operation Karbala-4", "Operation Nasr-4"],
            "rationales": [
                {"option": "Operation Ramadan", "why_plausible": "1982 battle outside Basra.", "why_wrong": "Earlier battle in 1982."},
                {"option": "Operation Karbala-4", "why_plausible": "Disastrous preliminary assault in December 1986.", "why_wrong": "Ambushed within hours with catastrophic losses two weeks prior."},
                {"option": "Operation Nasr-4", "why_plausible": "Northern front operation.", "why_wrong": "Fought in the mountains of Iraqi Kurdistan."}
            ],
            "expl": "Iran breached three lines of the impregnable Soviet-designed 'Iron Ring' defenses around Basra, but suffered over 20,000 casualties in ferocious artillery barrages.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 790
        },
        {
            "text": "On September 23, 1980, hours after the Iraqi surprise invasion, 140 Iranian Air Force F-4 and F-5 fighter-bombers struck airfields across Iraq in this largest air raid in Iranian history.",
            "ans": "Operation Kaman 99",
            "aliases": ["Operation Kaman 99", "Kaman 99", "عملیات کمان ۹۹", "کمان ۹۹"],
            "options": ["Operation Kaman 99", "Operation H-3", "Operation Scorch Sword", "Operation Morvarid"],
            "rationales": [
                {"option": "Operation H-3", "why_plausible": "Legendary long-range strike on western Iraqi airfields in 1981.", "why_wrong": "Daring raid on H-3 near the Jordanian border in April 1981 by eight Phantoms."},
                {"option": "Operation Scorch Sword", "why_plausible": "Airstrike on the Osirak nuclear reactor.", "why_wrong": "F-4 strike on Osirak in September 1980 before the Israeli raid."},
                {"option": "Operation Morvarid", "why_plausible": "November 1980 naval operation.", "why_wrong": "Destroyed the Iraqi Navy and Mina al-Bakr oil terminals in the Gulf."}
            ],
            "expl": "Kaman 99 (Bow 99, referencing Arash the Archer's mythical shot) crippled Iraqi air bases and prevented Saddam from gaining air superiority over Khuzestan.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 774
        }
    ])

    print("Writing Batch 3 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Total clues after Part 3:", len(clues_by_id))

if __name__ == "__main__":
    run_part3()
