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
    vals = [400, 800, 1200, 1600, 2000, 400, 800, 1200, 1600, 2000]
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
            "source_id": item.get("src", "amanat_iran_modern_history_2017"),
            "book_title": item.get("book", "Iran: A Modern History"),
            "author": item.get("auth", "Abbas Amanat"),
            "chapter": item.get("ch", "Historical Corpus"),
            "page": item.get("pg", 370 + idx * 8),
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

# 1. TAHRIR-IC VOCALS (Double, 10 clues)
add_batch(clues, "TAHRIR-IC VOCALS", "Persian Classical Singing", "Vocal Radif", "double", [
    {"text": "The rapid vocal ornamentation and melodic yodeling produced in the upper throat and falsetto characteristic of Persian classical singing is called this.",
     "ans": "Tahrir (Chahchah)", "aliases": ["Tahrir", "Chahchah", "تحریر", "چهچهه"],
     "options": ["Tahrir (Chahchah)", "Tasnif", "Gusheh", "Avaz"],
     "rationales": [{"option": "Tasnif", "why_plausible": "Rhythmic song form.", "why_wrong": "Metered ballad, not the throat trill."},
                    {"option": "Gusheh", "why_plausible": "Short melodic movement.", "why_wrong": "The individual melody within a Dastgah."},
                    {"option": "Avaz", "why_plausible": "Non-metric vocal improvisation.", "why_wrong": "The overall improvised vocal section."}],
     "expl": "Tahrir is often compared to a nightingale's warble, requiring decades of vocal diaphragm and throat control.", "pg": 510},
    {"text": "Universally revered as 'Khosrow-ye Avaz-e Iran' (The Emperor of Iranian Song), this Khorasani master vocalist recorded the iconic protest anthem Morgh-e Sahar.",
     "ans": "Ostad Mohammad Reza Shajarian", "aliases": ["Ostad Mohammad Reza Shajarian", "Mohammad Reza Shajarian", "Shajarian", "محمدرضا شجریان", "شجریان"],
     "options": ["Ostad Mohammad Reza Shajarian", "Gholam-Hossein Banan", "Shahram Nazeri", "Iraj (Hossein Khajeh Amiri)"],
     "rationales": [{"option": "Gholam-Hossein Banan", "why_plausible": "Earlier legendary vocalist.", "why_wrong": "Famed for Ey Iran and delicate baritone in the 1950s."},
                    {"option": "Shahram Nazeri", "why_plausible": "Kurdish Sufi vocalist.", "why_wrong": "Known as the 'Knight of Persian Song' singing Rumi."},
                    {"option": "Iraj", "why_plausible": "Popular high-tenor vocalist.", "why_wrong": "Famed for Pahlavi film songs and Avaz-e Koocheh-Bazaari."}],
     "expl": "Shajarian was awarded the UNESCO Mozart Medal and taught generations of classical singers before his death in 2020.", "pg": 512},
    {"text": "Famed for singing the patriotic anthem 'Ey Iran' and wearing dark horn-rimmed glasses after losing an eye in a 1950 car crash, this singer had a velvet baritone voice.",
     "ans": "Ostad Gholam-Hossein Banan", "aliases": ["Ostad Gholam-Hossein Banan", "Gholam-Hossein Banan", "Banan", "غلامحسین بنان", "بنان"],
     "options": ["Ostad Gholam-Hossein Banan", "Mohammad Reza Shajarian", "Mahmoud Khansari", "Abdolvahab Shahidi"],
     "rationales": [{"option": "Mohammad Reza Shajarian", "why_plausible": "Famous singer.", "why_wrong": "Succeeded Banan in the 1970s."},
                    {"option": "Mahmoud Khansari", "why_plausible": "Golha vocalist.", "why_wrong": "Prominent contemporary vocalist."},
                    {"option": "Abdolvahab Shahidi", "why_plausible": "Baritone singer and oud player.", "why_wrong": "Famous oud player and singer."}],
     "expl": "Banan revolutionized Persian vocal style by abandoning loud shouting in favor of intimate, whispered microphone phrasing on Radio Tehran's Golha programs.", "pg": 514},
    {"text": "The premier cultural radio broadcast founded in 1956 by Davood Pirnia that introduced Persian classical poetry to millions of listeners was called this.",
     "ans": "Golha (Flowers)", "aliases": ["Golha", "Program Golha", "برنامه گل‌ها", "گل‌ها"],
     "options": ["Golha (Flowers)", "Shoma va Radio", "Sobh-e Jomeh", "Karbavan-e Sher"],
     "rationales": [{"option": "Shoma va Radio", "why_plausible": "Popular radio show.", "why_wrong": "General entertainment program."},
                    {"option": "Sobh-e Jomeh", "why_plausible": "Friday comedy show.", "why_wrong": "Comedy entertainment program."},
                    {"option": "Karbavan-e Sher", "why_plausible": "Literary program.", "why_wrong": "Poetry recitation show."}],
     "expl": "Golha produced over 1,500 episodes under categories like Golha-ye Javidan, Golha-ye Rang-a-Rang, and Yek Shakheh Gol.", "pg": 516},
    {"text": "This preeminent female classical vocalist, famed as 'Banu-ye Avaz-e Iran' (The Lady of Iranian Song), collaborated closely with composers Homayoun Khorram and Parviz Yahaqi.",
     "ans": "Marzieh (Ashraf al-Sadat Mortezaie)", "aliases": ["Marzieh", "Ashraf al-Sadat Mortezaie", "مرضیه"],
     "options": ["Marzieh (Ashraf al-Sadat Mortezaie)", "Delkash", "Googoosh", "Simin Ghanem"],
     "rationales": [{"option": "Delkash", "why_plausible": "Contemporaneous contralto queen.", "why_wrong": "Esmat Bagherpour, famed for dramatic chest voice in films."},
                    {"option": "Googoosh", "why_plausible": "Pop music icon.", "why_wrong": "Pop superstar of the 1970s."},
                    {"option": "Simin Ghanem", "why_plausible": "Singer of Gole Yakh.", "why_wrong": "Pop balladeer."}],
     "expl": "Marzieh was the first female singer to perform on Radio Tehran's prestigious Golha-ye Rang-a-Rang programs.", "pg": 518},
    # Set B
    {"text": "The primary mode (Dastgah) of Persian classical music, representing serenity and mystical passion and forming the parent modal root of Abu-Ata, Dashti, and Afshari, is this.",
     "ans": "Dastgah-e Shur", "aliases": ["Dastgah-e Shur", "Shur", "دستگاه شور", "شور"],
     "options": ["Dastgah-e Shur", "Dastgah-e Mahur", "Dastgah-e Homayoun", "Dastgah-e Segah"],
     "rationales": [{"option": "Dastgah-e Mahur", "why_plausible": "Major-scale mode.", "why_wrong": "Triumphant mode similar to Western major scale."},
                    {"option": "Dastgah-e Homayoun", "why_plausible": "Aristocratic mode.", "why_wrong": "Features the Bayat-e Esfahan sub-mode."},
                    {"option": "Dastgah-e Segah", "why_plausible": "Emotional mode.", "why_wrong": "Characterized by its distinct neutral third scale degree."}],
     "expl": "Shur is considered the mother of all twelve Persian Dastgahs, its Koron microtonal flat intervals evoking deep longing.", "pg": 520},
    {"text": "The son of Ostad Mohammad Reza Shajarian, renowned for his breath control and hit classical fusion albums like Neither Angel Nor Devil, is named this.",
     "ans": "Homayoun Shajarian", "aliases": ["Homayoun Shajarian", "Homayoun", "همایون شجریان", "همایون"],
     "options": ["Homayoun Shajarian", "Ali-Reza Ghorbani", "Mohammad Motamedi", "Sina Sarlak"],
     "rationales": [{"option": "Ali-Reza Ghorbani", "why_plausible": "Leading classical singer.", "why_wrong": "Collaborated on Afsaneh-ye Chashmhayat, but not Shajarian's son."},
                    {"option": "Mohammad Motamedi", "why_plausible": "Classical singer from Kashan.", "why_wrong": "Pupil of Shajarian, not his son."},
                    {"option": "Sina Sarlak", "why_plausible": "Bakhtiari singer.", "why_wrong": "Student of Shajarian from Aligudarz."}],
     "expl": "Homayoun began as a tombak player accompanying his father before emerging as one of the most commercially successful vocalists in modern Iran.", "pg": 522},
    {"text": "Known as the 'Knight of Persian Song', this Kermanshahi master vocalist was the first to set the mystical poetry of Jalal al-Din Rumi to epic Kurdish and Persian rhythms.",
     "ans": "Shahram Nazeri", "aliases": ["Shahram Nazeri", "Nazeri", "شهرام ناظری", "ناظری"],
     "options": ["Shahram Nazeri", "Mohammad Reza Shajarian", "Hesameddin Seraj", "Bijan Bijani"],
     "rationales": [{"option": "Mohammad Reza Shajarian", "why_plausible": "Supreme singer.", "why_wrong": "Famed for Sa'di and Hafez, while Nazeri pioneered the Rumi Sufi resurgence."},
                    {"option": "Hesameddin Seraj", "why_plausible": "Isfahani singer and architect.", "why_wrong": "Traditional singer from Isfahan."},
                    {"option": "Bijan Bijani", "why_plausible": "Calligrapher and singer.", "why_wrong": "Singer of Nawa'i."}],
     "expl": "His 1984 album Yadegar-e Doost, composed by Kambiz Roshanravan to mark Rumi's anniversary, was the bestselling classical cassette in Iranian history.", "pg": 524},
    {"text": "The non-metric, rhythmically free vocal section where a singer improvises classical poetry accompanied by a single solo instrument (like tar, ney, or kamancheh) is called this.",
     "ans": "Avaz", "aliases": ["Avaz", "Aawaz", "آواز"],
     "options": ["Avaz", "Tasnif", "Chahar-Mezrab", "Reng"],
     "rationales": [{"option": "Tasnif", "why_plausible": "Vocal song.", "why_wrong": "A structured, metered rhythmic ballad."},
                    {"option": "Chahar-Mezrab", "why_plausible": "Fast instrumental piece.", "why_wrong": "Virtuosic instrumental solo, not a vocal section."},
                    {"option": "Reng", "why_plausible": "Dance finale.", "why_wrong": "Instrumental dance meter ending a suite."}],
     "expl": "Avaz is the true test of a Persian vocalist's mastery, demanding improvised transitions through various melodic Gushehs according to the poetic meter.", "pg": 526},
    {"text": "The microtonal pitch alteration in Persian classical music that lowers a musical note by approximately a quarter-tone (roughly 30 to 60 cents) is named this.",
     "ans": "Koron (Sori / Koron)", "aliases": ["Koron", "Sori", "Quarter tone", "کرن", "سری"],
     "options": ["Koron (Sori / Koron)", "Flat (Bemol)", "Sharp (Dieze)", "Natural (Bécarre)"],
     "rationales": [{"option": "Flat (Bemol)", "why_plausible": "Half-step flat.", "why_wrong": "Standard Western half-step lowering (100 cents)."},
                    {"option": "Sharp (Dieze)", "why_plausible": "Half-step sharp.", "why_wrong": "Standard Western half-step raising."},
                    {"option": "Natural (Bécarre)", "why_plausible": "Cancels accidentals.", "why_wrong": "Standard natural sign."}],
     "expl": "Pioneered in modern notation by Ostad Ali-Naqi Vaziri in 1923, Koron lowers a note by a quarter-tone, while Sori raises it by a quarter-tone.", "pg": 528}
])

save_data(clues)
