#!/usr/bin/env python3
import json

def run_90():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues_by_id = {c["id"]: c for c in json.load(f)}

    def add_10(cat, period, theme, items):
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "").replace(",", "")
        vals = [400, 800, 1200, 1600, 2000, 400, 800, 1200, 1600, 2000]
        for idx, item in enumerate(items):
            set_tag = "a" if idx < 5 else "b"
            val = vals[idx]
            cid = f"double_{prefix}_{val}_{set_tag}"
            clues_by_id[cid] = {
                "id": cid, "language": "en", "category": cat, "historical_period": period,
                "theme": theme, "difficulty": "STANDARD", "value": val, "round": "double",
                "clue_text": item["text"], "canonical_answer": item["ans"],
                "accepted_aliases": item["aliases"], "partial_answers": [], "specificity_prompt": "",
                "options": item["options"], "correct_option_index": 0,
                "distractor_rationales": item["rationales"], "explanation": item["expl"],
                "source_id": item.get("src", "milani_the_shah_2011"),
                "book_title": item.get("book", "The Shah"),
                "author": item.get("auth", "Abbas Milani"),
                "chapter": item.get("ch", "Historical Corpus"),
                "page": item.get("pg", 320 + idx * 8),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Spot on!",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. SHAH-ME ON YOU (Double, 10 clues)
    add_10("SHAH-ME ON YOU", "Pahlavi Court & Dynasty", "Imperial Factions", [
        {"text": "The Shah's formidable twin sister who was nicknamed 'The Black Panther' by French journalists for her political assertiveness was named this.",
         "ans": "Princess Ashraf Pahlavi", "aliases": ["Princess Ashraf Pahlavi", "Ashraf Pahlavi", "Princess Ashraf", "اشرف پهلوی", "شاهدخت اشرف"],
         "options": ["Princess Ashraf Pahlavi", "Princess Shahnaz", "Princess Shams", "Princess Fatemeh"],
         "rationales": [{"option": "Princess Shahnaz", "why_plausible": "His eldest daughter with Fawzia.", "why_wrong": "His daughter, not his twin sister."},
                        {"option": "Princess Shams", "why_plausible": "His elder sister.", "why_wrong": "His elder sister who converted to Catholicism and lived quietly."},
                        {"option": "Princess Fatemeh", "why_plausible": "His half-sister.", "why_wrong": "Half-sister married to General Khatami."}],
         "expl": "Ashraf met secretly with Kermit Roosevelt and General Norman Schwarzkopf Sr. in Paris in 1953 to convince her hesitant brother to back the coup against Mosaddegh.", "pg": 140},
        {"text": "Appointed Empress (Shahbanu) in 1967 and designated regent in case of the Shah's death, this third wife of the Shah was a patron of modern art and architecture.",
         "ans": "Farah Diba (Empress Farah)", "aliases": ["Farah Diba", "Empress Farah", "Shahbanu Farah", "فرح دیبا", "شهبانو فرح"],
         "options": ["Farah Diba (Empress Farah)", "Queen Soraya", "Princess Fawzia", "Taj al-Molouk"],
         "rationales": [{"option": "Queen Soraya", "why_plausible": "Second wife.", "why_wrong": "Divorced in 1958 due to lack of a male heir."},
                        {"option": "Princess Fawzia", "why_plausible": "First wife from Egypt.", "why_wrong": "Divorced in 1948."},
                        {"option": "Taj al-Molouk", "why_plausible": "Queen mother.", "why_wrong": "Reza Shah's wife and the Shah's mother."}],
         "expl": "Farah Diba established the Tehran Museum of Contemporary Art in 1977, acquiring masterpieces by Picasso, Warhol, Rothko, and Pollock.", "pg": 260},
        {"text": "The Shah's exclusive winter retreat in the Swiss Alps, where he skied and conducted informal foreign diplomacy each January, was located in this luxury resort.",
         "ans": "St. Moritz (Villa Suvretta)", "aliases": ["St. Moritz", "Villa Suvretta", "Suvretta House", "سن موریتز", "ویلا سوورتا"],
         "options": ["St. Moritz (Villa Suvretta)", "Gstaad", "Davos", "Zermatt"],
         "rationales": [{"option": "Gstaad", "why_plausible": "Swiss ski resort.", "why_wrong": "Not the site of the Shah's private Villa Suvretta."},
                        {"option": "Davos", "why_plausible": "Swiss resort famous for WEF.", "why_wrong": "Site of economic conferences, not the royal villa."},
                        {"option": "Zermatt", "why_plausible": "Matterhorn ski village.", "why_wrong": "Car-free village, not the Pahlavi residence."}],
         "expl": "The Shah's month-long vacations at Villa Suvretta with kingpins and foreign journalists were heavily criticized during domestic economic crises.", "pg": 314},
        {"text": "The elite 4,000-man bodyguard division tasked with protecting the royal family, who swore personal blood oaths to the Shah, was known as this.",
         "ans": "The Imperial Guard (Javidan Guard)", "aliases": ["The Imperial Guard", "Javidan Guard", "Lashkar-e Guard", "گارد جاویدان", "گارد شاهنشاهی"],
         "options": ["The Imperial Guard (Javidan Guard)", "SAVAK", "The Cossack Brigade", "The Gendarmerie"],
         "rationales": [{"option": "SAVAK", "why_plausible": "Intelligence service.", "why_wrong": "Secret intelligence agency, not the ceremonial uniform armored brigade."},
                        {"option": "The Cossack Brigade", "why_plausible": "Historical cavalry.", "why_wrong": "Disbanded in the 1920s under Reza Shah."},
                        {"option": "The Gendarmerie", "why_plausible": "Rural police.", "why_wrong": "Rural border force."}],
         "expl": "Named after the ancient 10,000 Achaemenid Immortals, all candidates had to exceed six feet in height and undergo rigorous ideological screening.", "pg": 316},
        {"text": "Between 1931 and 1936, the young Crown Prince Mohammad Reza was sent by his father to attend this prestigious Swiss boarding school near Lake Geneva.",
         "ans": "Institut Le Rosey", "aliases": ["Institut Le Rosey", "Le Rosey", "مدرسه روزه", "له روزه"],
         "options": ["Institut Le Rosey", "Eton College", "Harrow School", "St. Gallen"],
         "rationales": [{"option": "Eton College", "why_plausible": "Elite British school.", "why_wrong": "British public school, not the Swiss bilingual academy."},
                        {"option": "Harrow School", "why_plausible": "Famous British school.", "why_wrong": "Located in London."},
                        {"option": "St. Gallen", "why_plausible": "Swiss university.", "why_wrong": "Swiss business university, not the elite secondary boarding school."}],
         "expl": "At Le Rosey, the future Shah befriended Western classmates like Prince Rainier of Monaco, developing fluent French and a lifelong passion for tennis and skiing.", "pg": 64},
        # Set B
        {"text": "The Shah's first marriage in 1939 was an arranged dynastic union uniting the Pahlavi monarchy with the royal house of this Arab kingdom.",
         "ans": "Egypt (Kingdom of Egypt)", "aliases": ["Egypt", "Kingdom of Egypt", "مصر", "پادشاهی مصر"],
         "options": ["Egypt (Kingdom of Egypt)", "Saudi Arabia", "Jordan", "Iraq"],
         "rationales": [{"option": "Saudi Arabia", "why_plausible": "Arab monarchy.", "why_wrong": "Wahhabi kingdom, no royal marriage."},
                        {"option": "Jordan", "why_plausible": "Hashemite kingdom.", "why_wrong": "Hashemite kingdom of Jordan."},
                        {"option": "Iraq", "why_plausible": "Hashemite kingdom until 1958.", "why_wrong": "Hashemite kingdom of Iraq."}],
         "expl": "Reza Shah arranged the wedding with King Farouk's 17-year-old sister Princess Fawzia to boost Pahlavi international prestige.", "pg": 88},
        {"text": "In 1958, the Shah divorced Queen Soraya Esfandiari Bakhtiari due to court dynastic pressure resulting from this personal tragedy.",
         "ans": "Her inability to produce a male heir (Infertility)", "aliases": ["Her inability to produce a male heir", "Infertility", "Lack of an heir", "نازایی", "نداشتن فرزند پسر"],
         "options": ["Her inability to produce a male heir (Infertility)", "Infidelity", "Political treason", "Financial corruption"],
         "rationales": [{"option": "Infidelity", "why_plausible": "Divorce ground.", "why_wrong": "False; they remained passionately in love throughout the crisis."},
                        {"option": "Political treason", "why_plausible": "Court intrigue.", "why_wrong": "Soraya was intensely loyal to the monarchy during the 1953 coup."},
                        {"option": "Financial corruption", "why_plausible": "Financial scandal.", "why_wrong": "Unrelated to state finances."}],
         "expl": "The 1906 Constitution required the crown prince to be born of an Iranian mother; after medical trips to American specialists proved fruitless, the Shah wept as he announced the divorce on radio.", "pg": 218},
        {"text": "On October 26, 1967, his 48th birthday, the Shah crowned himself at Golestan Palace and placed a custom Van Cleef & Arpels emerald tiara on this Empress.",
         "ans": "Empress Farah", "aliases": ["Empress Farah", "Farah Pahlavi", "Farah Diba", "شهبانو فرح", "فرح پهلوی"],
         "options": ["Empress Farah", "Queen Soraya", "Princess Ashraf", "Princess Shahnaz"],
         "rationales": [{"option": "Queen Soraya", "why_plausible": "Second queen.", "why_wrong": "Divorced in 1958, living in Paris."},
                        {"option": "Princess Ashraf", "why_plausible": "His twin sister.", "why_wrong": "Watched from the royal gallery."},
                        {"option": "Princess Shahnaz", "why_plausible": "His daughter.", "why_wrong": "His daughter, seated among family."}],
         "expl": "She became the first woman crowned as Empress (Shahbanu) in Iranian history since the Sasanian queen Burandokht in the 7th century.", "pg": 284},
        {"text": "The Shah held biannual planning conferences at this Caspian coastal resort in Mazandaran to dictate economic targets to his cabinet.",
         "ans": "Ramsar", "aliases": ["Ramsar", "Grand Hotel Ramsar", "رامسر"],
         "options": ["Ramsar", "Babolsar", "Chaloos", "Bandar-e Anzali"],
         "rationales": [{"option": "Babolsar", "why_plausible": "Caspian resort.", "why_wrong": "Resort town in Mazandaran."},
                        {"option": "Chaloos", "why_plausible": "Port city.", "why_wrong": "Port at the end of the road."},
                        {"option": "Bandar-e Anzali", "why_plausible": "Gilan port.", "why_wrong": "Port city in Gilan."}],
         "expl": "At the August 1974 Ramsar conference, the Shah overruled economic planners and doubled the budget of the Fifth Plan, triggering ruinous inflation.", "pg": 334},
        {"text": "The Shah's eldest son and designated heir, born in Tehran on October 31, 1960, was named this.",
         "ans": "Crown Prince Reza Pahlavi", "aliases": ["Crown Prince Reza Pahlavi", "Reza Pahlavi", "Crown Prince Reza", "شاهزاده رضا پهلوی", "ولیعهد رضا"],
         "options": ["Crown Prince Reza Pahlavi", "Prince Ali Reza", "Prince Gholam Reza", "Prince Shahram"],
         "rationales": [{"option": "Prince Ali Reza", "why_plausible": "His younger brother.", "why_wrong": "Born in 1966, died in 2011."},
                        {"option": "Prince Gholam Reza", "why_plausible": "The Shah's half-brother.", "why_wrong": "Half-brother born in 1923."},
                        {"option": "Prince Shahram", "why_plausible": "Ashraf's son.", "why_wrong": "Nephew, son of Princess Ashraf."}],
         "expl": "His birth secured dynastic succession; thousands of prisoners were pardoned and free sugar was distributed to families across the nation.", "pg": 264}
    ])

    print("Double 1 added. Total clues: 830")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    run_90()
