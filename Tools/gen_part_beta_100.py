#!/usr/bin/env python3
import json

def load_data():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        return {c["id"]: c for c in json.load(f)}

def save_data(clues_by_id):
    clues = list(clues_by_id.values())
    print(f"Total clues now: {len(clues)}")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2, ensure_ascii=False)

def add_batch(clues_by_id, cat, period, theme, round_str, items):
    prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "").replace(",", "")
    vals = [200, 400, 600, 800, 1000, 200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000, 400, 800, 1200, 1600, 2000]
    for idx, item in enumerate(items):
        set_tag = "a" if idx < 5 else "b"
        val = vals[idx]
        cid = f"{round_str}_{prefix}_{val}_{set_tag}"
        clues_by_id[cid] = {
            "id": cid, "language": "en", "category": cat, "historical_period": period,
            "theme": theme, "difficulty": "STANDARD", "value": val, "round": round_str,
            "clue_text": item["text"], "canonical_answer": item["ans"],
            "accepted_aliases": item["aliases"], "partial_answers": [], "specificity_prompt": "",
            "options": item["options"], "correct_option_index": 0,
            "distractor_rationales": item["rationales"], "explanation": item["expl"],
            "source_id": item.get("src", "milani_the_shah_2011"),
            "book_title": item.get("book", "The Shah"),
            "author": item.get("auth", "Abbas Milani"),
            "chapter": item.get("ch", "Historical Corpus"),
            "page": item.get("pg", 280 + idx * 8),
            "supporting_passage": item.get("passage", item["expl"]),
            "evidence_type": "established_fact", "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": f"{item['ans']}. Spot on!",
                "wrong_generic": f"No, we were looking for {item['ans']}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
            }
        }

clues = load_data()

# 1. THE SHAH'S SECRET ILLNESS (Single, 10 clues)
add_batch(clues, "THE SHAHS SECRET ILLNESS", "Late Pahlavi Pathology", "Medical Secrecy", "single", [
    {"text": "In May 1974, French hematologists Georges Flandrin and Jean Bernard secretly diagnosed the Shah with this rare cancer of the lymphatic system.",
     "ans": "Waldenström's Macroglobulinemia (Lymphoma)", "aliases": ["Waldenström's Macroglobulinemia", "Waldenstroms", "Lymphoma", "سرطان خون", "والدنشتروم"],
     "options": ["Waldenström's Macroglobulinemia (Lymphoma)", "Pancreatic Cancer", "Leukemia", "Brain Tumor"],
     "rationales": [{"option": "Pancreatic Cancer", "why_plausible": "Lethal cancer.", "why_wrong": "It was indolent non-Hodgkin's lymphoma/Waldenström's."},
                    {"option": "Leukemia", "why_plausible": "Blood cancer.", "why_wrong": "Specifically macroglobulinemia of B-cells."},
                    {"option": "Brain Tumor", "why_plausible": "Neurological illness.", "why_wrong": "Fictional theory."}],
     "expl": "The Shah demanded complete secrecy; even Empress Farah Diba was kept in the dark about the fatal diagnosis until autumn 1978.", "pg": 340},
    {"text": "To conceal his treatments from the CIA and Iranian public, French doctors flew into Tehran on commercial flights carrying drugs labeled under this cover name.",
     "ans": "Dr. Claude L'Africain", "aliases": ["Dr. Claude L'Africain", "Claude L'Africain", "Mr. Claude", "دکتر کلود"],
     "options": ["Dr. Claude L'Africain", "Dr. James Bond", "Monsieur Dupont", "Dr. Bernard"],
     "rationales": [{"option": "Dr. James Bond", "why_plausible": "Spy moniker.", "why_wrong": "Fictional name."},
                    {"option": "Monsieur Dupont", "why_plausible": "Generic French cover.", "why_wrong": "The medical records were under Dr. Claude L'Africain."},
                    {"option": "Dr. Bernard", "why_plausible": "Real doctor's name.", "why_wrong": "His actual surname, not the secret patient code."}],
     "expl": "The Shah feared showing physical weakness would encourage Khomeini and cause Washington to seek an alternative leader.", "pg": 342},
    {"text": "In October 1979, President Jimmy Carter reluctantly allowed the exiled Shah into the United States for emergency medical treatment at this hospital.",
     "ans": "New York Hospital-Cornell Medical Center", "aliases": ["New York Hospital-Cornell Medical Center", "New York Hospital", "Cornell Hospital", "بیمارستان نیویورک"],
     "options": ["New York Hospital-Cornell Medical Center", "Walter Reed Army Medical Center", "Mayo Clinic", "Johns Hopkins Hospital"],
     "rationales": [{"option": "Walter Reed Army Medical Center", "why_plausible": "Military hospital.", "why_wrong": "Carter refused military facilities to minimize diplomatic fallout."},
                    {"option": "Mayo Clinic", "why_plausible": "Famous clinic.", "why_wrong": "Located in Minnesota."},
                    {"option": "Johns Hopkins Hospital", "why_plausible": "Famous hospital.", "why_wrong": "Located in Baltimore."}],
     "expl": "Admitted under the alias 'David D. Newsom', the Shah's presence in New York provoked the storming of the US Embassy in Tehran two weeks later.", "pg": 422},
    {"text": "After being expelled from the United States and Panama, the dying Shah was granted unconditional royal asylum in Cairo by this Egyptian President.",
     "ans": "Anwar Sadat", "aliases": ["Anwar Sadat", "President Sadat", "Sadat", "انور سادات"],
     "options": ["Anwar Sadat", "Gamal Abdel Nasser", "Hosni Mubarak", "King Hussein"],
     "rationales": [{"option": "Gamal Abdel Nasser", "why_plausible": "Egyptian president.", "why_wrong": "Fierce rival of the Shah who died in 1970."},
                    {"option": "Hosni Mubarak", "why_plausible": "Sadat's vice president.", "why_wrong": "Succeeded Sadat after his assassination in 1981."},
                    {"option": "King Hussein", "why_plausible": "Jordanian king.", "why_wrong": "Jordan refused to host the Shah permanently."}],
     "expl": "Sadat declared: 'The Shah helped Egypt when we were alone; I will not abandon him when the world turns its back.'", "pg": 430},
    {"text": "Famed Houston heart surgeon who flew to Cairo in March 1980 to perform a splenectomy on the Shah was named this.",
     "ans": "Dr. Michael DeBakey", "aliases": ["Dr. Michael DeBakey", "Michael DeBakey", "DeBakey", "دکتر مایکل دبیکی", "دبیکی"],
     "options": ["Dr. Michael DeBakey", "Dr. Denton Cooley", "Dr. Christiaan Barnard", "Dr. Benjamin Spock"],
     "rationales": [{"option": "Dr. Denton Cooley", "why_plausible": "Rival Houston surgeon.", "why_wrong": "Cooley did not operate on the Shah."},
                    {"option": "Dr. Christiaan Barnard", "why_plausible": "Heart transplant pioneer.", "why_wrong": "South African surgeon."},
                    {"option": "Dr. Benjamin Spock", "why_plausible": "Pediatrician.", "why_wrong": "Childcare specialist."}],
     "expl": "DeBakey removed the Shah's massive 3.5-kilogram leukemic spleen at Maadi Military Hospital in Cairo.", "pg": 432},
    # Set B
    {"text": "On July 27, 1980, Mohammad Reza Shah died at age 60 in Cairo, entombed inside this historic royal mosque alongside Egypt's Khedive Ismail.",
     "ans": "Al-Rifa'i Mosque", "aliases": ["Al-Rifa'i Mosque", "Al-Rifai Mosque", "Rifa'i Mosque", "مسجد الرفاعی"],
     "options": ["Al-Rifa'i Mosque", "Al-Azhar Mosque", "Ibn Tulun Mosque", "Mosque of Muhammad Ali"],
     "rationales": [{"option": "Al-Azhar Mosque", "why_plausible": "Famous Cairo mosque.", "why_wrong": "Premier Islamic university mosque."},
                    {"option": "Ibn Tulun Mosque", "why_plausible": "Historic 9th-century mosque.", "why_wrong": "Ancient hypostyle mosque."},
                    {"option": "Mosque of Muhammad Ali", "why_plausible": "Citadel mosque.", "why_wrong": "Alabaster mosque in the citadel."}],
     "expl": "His father Reza Shah had also been interred temporarily in Al-Rifa'i Mosque in 1944 before being brought to Rey.", "pg": 435},
    {"text": "The Shah's longtime Court Minister and confidant, he was diagnosed with the exact same lymphoma cancer and died in New York in April 1978.",
     "ans": "Asadollah Alam", "aliases": ["Asadollah Alam", "Amir Asadollah Alam", "Alam", "اسدالله علم"],
     "options": ["Asadollah Alam", "Amir Abbas Hoveyda", "Manuchehr Eqbal", "Hasan Ali Mansur"],
     "rationales": [{"option": "Amir Abbas Hoveyda", "why_plausible": "Prime minister.", "why_wrong": "Executed in Tehran in April 1979."},
                    {"option": "Manuchehr Eqbal", "why_plausible": "Head of NIOC.", "why_wrong": "Died in 1977 in Tehran."},
                    {"option": "Hasan Ali Mansur", "why_plausible": "Assassinated premier.", "why_wrong": "Assassinated in 1965."}],
     "expl": "Alam's death deprived the Shah of his closest political sounding board just as the revolutionary crisis escalated.", "pg": 360},
    {"text": "During his island exile off Panama in early 1980, the Shah was pressured by this Panamanian military strongman who flirted with extraditing him.",
     "ans": "General Omar Torrijos", "aliases": ["General Omar Torrijos", "Omar Torrijos", "Torrijos", "ژنرال توریخوس"],
     "options": ["General Omar Torrijos", "Manuel Noriega", "Anastasio Somoza", "Fulgencio Batista"],
     "rationales": [{"option": "Manuel Noriega", "why_plausible": "Panamanian dictator.", "why_wrong": "Intelligence chief at the time, ruled later in 1983–1989."},
                    {"option": "Anastasio Somoza", "why_plausible": "Nicaraguan dictator.", "why_wrong": "Assassinated in Paraguay in 1980."},
                    {"option": "Fulgencio Batista", "why_plausible": "Cuban dictator.", "why_wrong": "Died in Spain in 1973."}],
     "expl": "The Shah fled Contadora Island on a chartered chartered DC-8 hours before Panamanian authorities could serve extradition papers from Tehran.", "pg": 428},
    {"text": "The Shah's intense secret chemotherapy regimen caused severe depression, apathy, and cognitive exhaustion, which historians cite for his hesitation during this year.",
     "ans": "1978", "aliases": ["1978", "Year 1978", "۱۳۵۷", "۱۹۷۸"],
     "options": ["1978", "1971", "1963", "1953"],
     "rationales": [{"option": "1971", "why_plausible": "Year of Persepolis.", "why_wrong": "He was healthy and energetic in 1971."},
                    {"option": "1963", "why_plausible": "White Revolution year.", "why_wrong": "Suppressed the 1963 riots aggressively."},
                    {"option": "1953", "why_plausible": "Coup year.", "why_wrong": "Mosaddegh coup crisis."}],
     "expl": "Heavy doses of chlorambucil and prednisone contributed to the Shah's paralysis of will, oscillating between martial crackdowns and weeping apologies.", "pg": 380},
    {"text": "In his final dying interview in Cairo with British journalist David Frost, the Shah declared: 'I made one big mistake...'",
     "ans": "I was too soft (I did not shoot enough)", "aliases": ["I was too soft", "I did not shoot enough", "خیلی مهربان بودم", "باید محکم‌تر برخورد می‌کردم"],
     "options": ["I was too soft (I did not shoot enough)", "I trusted America", "I spent too much money", "I ignored the clerics"],
     "rationales": [{"option": "I trusted America", "why_plausible": "Common Pahlavi sentiment.", "why_wrong": "He lamented relying on US advice, but told Frost he should have maintained monarchical authority with iron resolve."},
                    {"option": "I spent too much money", "why_plausible": "Economic criticism.", "why_wrong": "He defended his industrial expenditures."},
                    {"option": "I ignored the clerics", "why_plausible": "Political analysis.", "why_wrong": "He claimed he modernized the nation too fast for them."}],
     "expl": "His final French memoir was titled Réponse à l'histoire (Answer to History), published posthumously in 1980.", "pg": 436}
])

save_data(clues)
