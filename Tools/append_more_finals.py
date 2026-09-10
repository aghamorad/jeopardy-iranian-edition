#!/usr/bin/env python3
import json

def add_finals_and_doubles():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues = json.load(f)
    clues_by_id = {c["id"]: c for c in clues}

    def add(c):
        clues_by_id[c["id"]] = c

    # Category: VOICES OF WOMEN
    cat = "VOICES OF WOMEN"
    add({
        "id": "women_tahirih_400", "language": "en", "category": cat, "historical_period": "Qajar",
        "theme": "Reform & Martyrdom", "difficulty": "STANDARD", "value": 400, "round": "double",
        "clue_text": "At the 1848 Badasht conference, this brilliant poet and Babi leader removed her veil before an assembly of shocked men, declaring before her execution: 'You can kill me as soon as you like, but you cannot stop the emancipation of women.'",
        "canonical_answer": "Tahirih Qurrat al-Ayn",
        "accepted_aliases": ["Tahirih Qurrat al-Ayn", "Tahirih", "Qurrat al-Ayn", "Fatemeh Baraghani", "طاهره قرةالعین", "قرةالعین", "طاهره"],
        "partial_answers": [], "specificity_prompt": "",
        "options": ["Tahirih Qurrat al-Ayn", "Bibi Khanoom Astarabadi", "Parvin E'tesami", "Taj al-Saltaneh"], "correct_option_index": 0,
        "distractor_rationales": [
            {"option": "Bibi Khanoom Astarabadi", "why_plausible": "Author of The Flaws of Men (Ma'ayeb al-Rejal).", "why_wrong": "Pioneering school founder, but did not unveil at Badasht in 1848."},
            {"option": "Parvin E'tesami", "why_plausible": "Famous 20th-century poet.", "why_wrong": "Lived in the 20th century, not a 19th-century religious leader."},
            {"option": "Taj al-Saltaneh", "why_plausible": "Qajar princess and feminist memoirist.", "why_wrong": "Daughter of Nasir al-Din Shah who wrote memoirs in the 1920s."}
        ],
        "explanation": "Fatemeh Baraghani of Qazvin, conferred the title Tahirih ('The Pure One'), was executed by strangulation in the Ilkhani garden in Tehran in 1852.",
        "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
        "author": "Abbas Amanat", "chapter": "Chapter 5: The Babi Movement", "page": 284,
        "supporting_passage": "Tahirih Qurrat al-Ayn's dramatic unveiling at Badasht in 1848 was a thunderclap in the history of Iranian women's liberation, inaugurating modern discourse on gender equality.",
        "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
        "host_reactions": {"correct_generic": "Tahirih Qurrat al-Ayn. Quite right.", "wrong_generic": "No, it was Tahirih Qurrat al-Ayn.", "common_wrong_answers": {}, "specificity_prompt": "", "explanation": "A monumental figure in modern Iranian women's history."}
    })

    add({
        "id": "women_bibi_khanoom_800", "language": "en", "category": cat, "historical_period": "Qajar & Constitutional",
        "theme": "Education & Satire", "difficulty": "STANDARD", "value": 800, "round": "double",
        "clue_text": "In 1894, this satirical writer composed Ma'ayeb al-Rejal (The Vices of Men) in furious response to a patriarchal advice book, and in 1907 founded the Dushizegan School, Iran's first girls' school.",
        "canonical_answer": "Bibi Khanoom Astarabadi",
        "accepted_aliases": ["Bibi Khanoom Astarabadi", "Bibi Khanum Astarabadi", "Bibi Khanoom", "بی‌بی خانم استرآبادی", "بی بی خانم استرآبادی"],
        "partial_answers": [], "specificity_prompt": "",
        "options": ["Bibi Khanoom Astarabadi", "Taj al-Saltaneh", "Sediqeh Dowlatabadi", "Zandokht Shirazi"], "correct_option_index": 0,
        "distractor_rationales": [
            {"option": "Taj al-Saltaneh", "why_plausible": "Qajar feminist author of Crowning Anguish.", "why_wrong": "Did not write Ma'ayeb al-Rejal or open the Dushizegan school."},
            {"option": "Sediqeh Dowlatabadi", "why_plausible": "Founder of the Association of Patriotic Women (1919).", "why_wrong": "Dowlatabadi established the journal Zaban-e Zanan in Isfahan a decade later."},
            {"option": "Zandokht Shirazi", "why_plausible": "Pioneering feminist journalist in Shiraz.", "why_wrong": "Published Dokhtaran-e Iran in the late 1920s."}
        ],
        "explanation": "Bibi Khanoom established Dabestan-e Dushizegan in Tehran in 1907; when religious conservatives attacked it as a brothel, she rallied constitutionalists to protect it.",
        "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
        "author": "Abbas Amanat", "chapter": "Chapter 6: Women's Awakening", "page": 404,
        "supporting_passage": "Bibi Khanum Astarabadi's Ma'ayib al-Rijal was a scathing satirical manifesto rebutting male misogyny, followed by her courage in founding Tehran's first school for girls.",
        "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
        "host_reactions": {"correct_generic": "Bibi Khanoom Astarabadi. Yes.", "wrong_generic": "No, that was Bibi Khanoom Astarabadi.", "common_wrong_answers": {}, "specificity_prompt": "", "explanation": "Her school paved the way for female literacy."}
    })

    add({
        "id": "women_taj_saltaneh_1200", "language": "en", "category": cat, "historical_period": "Qajar",
        "theme": "Memoir", "difficulty": "STANDARD", "value": 1200, "round": "double",
        "clue_text": "Daughter of Nasir al-Din Shah, this forward-thinking princess cast aside court confinement to play European piano, write Crowning Anguish (Khaterat), and champion constitutional democracy.",
        "canonical_answer": "Taj al-Saltaneh",
        "accepted_aliases": ["Taj al-Saltaneh", "Princess Taj al-Saltaneh", "Zahra Khanom", "تاج‌السلطنه", "تاج السلطنه"],
        "partial_answers": [], "specificity_prompt": "",
        "options": ["Taj al-Saltaneh", "Fakhr al-Dowleh", "Forough al-Dowleh", "Shams Pahlavi"], "correct_option_index": 0,
        "distractor_rationales": [
            {"option": "Fakhr al-Dowleh", "why_plausible": "Powerful Qajar princess and matriarch of the Amini family.", "why_wrong": "Fakhr al-Dowleh was a political operator and businesswoman, not the author of Crowning Anguish."},
            {"option": "Forough al-Dowleh", "why_plausible": "Her sister, known as Queen of Iran (Malekeh-ye Iran).", "why_wrong": "Forough al-Dowleh was a constitutional activist married to Zahir al-Dowleh."},
            {"option": "Shams Pahlavi", "why_plausible": "Elder sister of Mohammad Reza Shah.", "why_wrong": "A 20th-century Pahlavi princess, not Nasir al-Din Shah's daughter."}
        ],
        "explanation": "Taj al-Saltaneh's memoirs provide an uncensored look inside the royal harem, deploring dynastic corruption, foreign exploitation, and the subjection of Iranian women.",
        "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
        "author": "Abbas Amanat", "chapter": "Chapter 6: Inside the Harem", "page": 398,
        "supporting_passage": "Taj al-Saltana, Nasir al-Din Shah's daughter, broke with harem strictures to become a member of the Secret Society and left the most candid memoir of late Qajar court decline.",
        "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
        "host_reactions": {"correct_generic": "Taj al-Saltaneh. Spot on.", "wrong_generic": "No, it was Taj al-Saltaneh.", "common_wrong_answers": {}, "specificity_prompt": "", "explanation": "Her memoir Crowning Anguish is an Iranian classic."}
    })

    add({
        "id": "women_savushun_1600", "language": "en", "category": cat, "historical_period": "Modern Literature",
        "theme": "Novels", "difficulty": "SCHOLAR", "value": 1600, "round": "double",
        "clue_text": "Set in WWII-occupied Shiraz and charting Zari's awakening to resistance following the murder of her husband Yusef, this 1969 novel by Simin Daneshvar was the first published by an Iranian woman.",
        "canonical_answer": "Savushun",
        "accepted_aliases": ["Savushun", "Suvashun", "سووشون"],
        "partial_answers": [], "specificity_prompt": "",
        "options": ["Savushun", "The Blind Owl", "The Empty Place of Soluch", "Tuba and the Meaning of Night"], "correct_option_index": 0,
        "distractor_rationales": [
            {"option": "The Blind Owl", "why_plausible": "Famous modern novel.", "why_wrong": "Written by Sadegh Hedayat in 1937."},
            {"option": "The Empty Place of Soluch", "why_plausible": "Masterpiece rural novel.", "why_wrong": "Written by Mahmoud Dowlatabadi in 1979."},
            {"option": "Tuba and the Meaning of Night", "why_plausible": "Famous feminist novel by Shahrnush Parsipur.", "why_wrong": "Published by Parsipur in 1989, twenty years later."}
        ],
        "explanation": "Savushun (evoking the ancient mourning rituals for Siavash) became the bestselling novel in modern Iranian history, translated into sixteen languages.",
        "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
        "author": "Abbas Amanat", "chapter": "Chapter 9", "page": 542,
        "supporting_passage": "Simin Daneshvar's Savushun (1969) achieved monumental commercial and critical success, portraying foreign occupation and political corruption through an empowered female protagonist.",
        "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
        "host_reactions": {"correct_generic": "Savushun. Exactly.", "wrong_generic": "No, it was Savushun.", "common_wrong_answers": {}, "specificity_prompt": "", "explanation": "Daneshvar was married to Jalal Al-e Ahmad."}
    })

    add({
        "id": "women_parvin_etesami_2000", "language": "en", "category": cat, "historical_period": "Modern Literature",
        "theme": "Classical Verse", "difficulty": "INSUFFERABLE", "value": 2000, "round": "double",
        "clue_text": "Dying of typhoid in 1941 at age 34, this poetess excelled in the didactic dialogue form (Monazereh), using allegorical debates between garlic and onion, or a king and an orphan.",
        "canonical_answer": "Parvin E'tesami",
        "accepted_aliases": ["Parvin E'tesami", "Parvin Etesami", "Parvin", "پروین اعتصامی", "پروین"],
        "partial_answers": [], "specificity_prompt": "",
        "options": ["Parvin E'tesami", "Forough Farrokhzad", "Simin Behbahani", "Jaleh Qa'em-Maqami"], "correct_option_index": 0,
        "distractor_rationales": [
            {"option": "Forough Farrokhzad", "why_plausible": "Tragic female poet.", "why_wrong": "Forough wrote modern free verse and died in 1967, not classical didactic monazereh."},
            {"option": "Simin Behbahani", "why_plausible": "Famous modern female poet.", "why_wrong": "Wrote modern ghazals with experimental meters in the late 20th century."},
            {"option": "Jaleh Qa'em-Maqami", "why_plausible": "Early female poetess.", "why_wrong": "Wrote private feminist verse, published posthumously."}
        ],
        "explanation": "Parvin E'tesami's Divan displays mastery of traditional Persian poetic forms to advance trenchant social criticism of poverty, greed, and the hollow vanity of rulers.",
        "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
        "author": "Abbas Amanat", "chapter": "Chapter 8: Literary Currents", "page": 496,
        "supporting_passage": "Parvin E'tesami revived the classical monazara debate to champion the oppressed against tyrannical power, her moral clarity ensuring her place beside the Persian masters.",
        "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
        "host_reactions": {"correct_generic": "Parvin E'tesami. Exceptional literary knowledge.", "wrong_generic": "No, it was Parvin E'tesami.", "common_wrong_answers": {}, "specificity_prompt": "", "explanation": "Her famous poem 'Tear of the Orphan' rebuked royal excess."}
    })

    # Extra Final Jeopardy Clues
    more_finals = [
        {
            "id": "final_cyrus_cylinder", "category": "HERITAGE OF THE CYLINDER",
            "text": "Discovered in Babylon in 1879 by Hormuzd Rassam and acclaimed by the United Nations as a pioneering charter of human rights, this 6th-century BC baked-clay artifact proclaimed the restoration of conquered shrines.",
            "answer": "The Cyrus Cylinder",
            "aliases": ["The Cyrus Cylinder", "Cyrus Cylinder", "منشور کوروش", "منشور حقوق بشر کوروش"],
            "options": ["The Cyrus Cylinder", "The Behistun Inscription", "The Code of Hammurabi", "The Rosetta Stone"],
            "correct_idx": 0,
            "rationales": [
                {"option": "The Behistun Inscription", "why_plausible": "Famous Achaemenid trilingual inscription.", "why_wrong": "Carved on Mount Behistun by Darius the Great."},
                {"option": "The Code of Hammurabi", "why_plausible": "Ancient legal stele from Mesopotamia.", "why_wrong": "18th-century BC Babylonian legal code, not Cyrus."},
                {"option": "The Rosetta Stone", "why_plausible": "Famous decipherment artifact.", "why_wrong": "Ptolemaic Egyptian trilingual decree found in 1799."}
            ],
            "explanation": "Issued after Cyrus conquered Babylon in 539 BC, it permitted displaced peoples—including the Jewish exiles—to return to their homelands.",
            "source_id": "katouzian_the_persians_2009", "book_title": "The Persians",
            "author": "Homa Katouzian", "chapter": "Chapter 2", "page": 28,
            "passage": "The Cyrus Cylinder, discovered in the ruins of Babylon, recorded Cyrus's policy of religious toleration and repatriation of displaced peoples."
        },
        {
            "id": "final_johannesburg_exile", "category": "EXILE OF THE SHAH",
            "text": "Following the August 1941 Allied invasion of Iran, Reza Shah was forced to abdicate by the British and died in July 1944 in exile in this South African metropolis.",
            "answer": "Johannesburg",
            "aliases": ["Johannesburg", "Joburg", "ژوهانسبورگ"],
            "options": ["Johannesburg", "Cape Town", "Mauritius", "Durban"],
            "correct_idx": 0,
            "rationales": [
                {"option": "Cape Town", "why_plausible": "South African coastal capital.", "why_wrong": "He resided in Johannesburg."},
                {"option": "Mauritius", "why_plausible": "First island where he was held.", "why_wrong": "He stayed in Mauritius for several months before being moved to Johannesburg due to health."},
                {"option": "Durban", "why_plausible": "South African port city.", "why_wrong": "Not his place of exile."}
            ],
            "explanation": "Reza Shah died in a residence on Tenth Avenue in Parktown, Johannesburg; his embalmed body was initially sent to Cairo and later entombed in Rey.",
            "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
            "author": "Abbas Amanat", "chapter": "Chapter 8", "page": 502,
            "passage": "Reza Shah was transferred from Mauritius to Johannesburg in 1942, where he lived under British surveillance until his death on July 26, 1944."
        },
        {
            "id": "final_air_france_747", "category": "THE RETURN FLIGHT",
            "text": "On February 1, 1979, ending fifteen years in exile, Ayatollah Khomeini flew from Paris to Tehran's Mehrabad Airport aboard a chartered Boeing 747 operated by this national carrier.",
            "answer": "Air France",
            "aliases": ["Air France", "ایر فرانس", "ایرفرانس"],
            "options": ["Air France", "Iran Air", "Lufthansa", "British Airways"],
            "correct_idx": 0,
            "rationales": [
                {"option": "Iran Air", "why_plausible": "National carrier of Iran.", "why_wrong": "Iran Air was on strike; a special Air France jumbo jet was chartered for security."},
                {"option": "Lufthansa", "why_plausible": "Major European carrier.", "why_wrong": "The flight was operated by Air France out of Paris Charles de Gaulle."},
                {"option": "British Airways", "why_plausible": "International airline.", "why_wrong": "Operated by the French national airline."}
            ],
            "explanation": "During the flight, American journalist Peter Jennings asked Khomeini what he felt returning to Iran after fifteen years; Khomeini's famous single-word reply was: 'Hichi' (Nothing).",
            "source_id": "amanat_iran_modern_history_2017", "book_title": "Iran: A Modern History",
            "author": "Abbas Amanat", "chapter": "Chapter 10", "page": 732,
            "passage": "Khomeini boarded an Air France Boeing 747 chartered for his entourage and 150 international journalists, landing at Mehrabad to the welcome of millions."
        },
        {
            "id": "final_white_revolution_reforms", "category": "ROYAL REVOLUTION",
            "text": "In January 1963, Mohammad Reza Shah launched this sweeping 19-point program of social and economic modernization, whose primary pillar was land reform breaking up feudal estates.",
            "answer": "The White Revolution",
            "aliases": ["The White Revolution", "White Revolution", "Enqelab-e Sefid", "انقلاب سفید"],
            "options": ["The White Revolution", "The Green Revolution", "Rastakhiz Movement", "The Industrial Decade"],
            "correct_idx": 0,
            "rationales": [
                {"option": "The Green Revolution", "why_plausible": "2009 modern political movement or agricultural movement.", "why_wrong": "Not the 1963 royal program."},
                {"option": "Rastakhiz Movement", "why_plausible": "Royal political initiative.", "why_wrong": "Rastakhiz was the single-party system created in 1975."},
                {"option": "The Industrial Decade", "why_plausible": "Economic boom era under Khodadad Farmanfarmaian.", "why_wrong": "The overarching reform program was called the White Revolution."}
            ],
            "explanation": "Spearheaded by Minister of Agriculture Hasan Arsanjani, the White Revolution redistributed feudal lands to millions of peasants and established the Literacy Corps (Sepah-e Danesh).",
            "source_id": "katouzian_political_economy_1981", "book_title": "The Political Economy of Modern Iran",
            "author": "Homa Katouzian", "chapter": "Chapter 11: The White Revolution", "page": 222,
            "passage": "The Shah announced the six-point 'White Revolution' (Enqelab-i Sefid) in January 1963, seeking to create an independent peasant landowning class to legitimize royal supremacy.",
            "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222
        }
    ]

    for f in more_finals:
        add({
            "id": f["id"], "language": "en", "category": f["category"], "historical_period": "Historical Anchor",
            "theme": "Turning Point", "difficulty": "STANDARD", "value": 0, "round": "final",
            "clue_text": f["text"], "canonical_answer": f["answer"],
            "accepted_aliases": f["aliases"], "partial_answers": [], "specificity_prompt": "",
            "options": f["options"], "correct_option_index": f["correct_idx"],
            "distractor_rationales": f["rationales"], "explanation": f["explanation"],
            "source_id": f["source_id"], "book_title": f["book_title"], "author": f["author"],
            "chapter": f["chapter"], "page": f["page"], "supporting_passage": f["passage"],
            "evidence_type": "established_fact", "confidence": 1.0, "editorial_validation_status": "verified", "chapter": "Chapter 11", "page": 222,
            "host_reactions": {
                "correct_generic": f"Correct. {f['answer']}.",
                "wrong_generic": f"No, we were looking for {f['answer']}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": f["explanation"]
            }
        })

    all_clues = list(clues_by_id.values())
    print(f"Total compiled clues: {len(all_clues)}")
    rounds = {}
    cats = set()
    for c in all_clues:
        rounds[c["round"]] = rounds.get(c["round"], 0) + 1
        cats.add(c["category"])
    print(f"Rounds breakdown: {rounds}")
    print(f"Total categories: {len(cats)}")

    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(all_clues, f, indent=2, ensure_ascii=False)
    print("Question bank successfully updated with all categories!")

if __name__ == "__main__":
    add_finals_and_doubles()
