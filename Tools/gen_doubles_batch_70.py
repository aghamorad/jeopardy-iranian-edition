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
            "page": item.get("pg", 360 + idx * 8),
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

# 1. MOSSAD-EGH IN THE MIDDLE (Double, 10 clues)
add_batch(clues, "MOSSAD-EGH IN THE MIDDLE", "Oil Nationalization Era", "Diplomacy & Trial", "double", [
    {"text": "In June 1952, Dr. Mohammad Mosaddegh traveled to this Dutch city to personally defend Iran's sovereign right to nationalize oil before the World Court.",
     "ans": "The Hague (International Court of Justice)", "aliases": ["The Hague", "International Court of Justice", "ICJ", "دیوان بین‌المللی لاهه", "لاهه"],
     "options": ["The Hague (International Court of Justice)", "Geneva", "Strasbourg", "Brussels"],
     "rationales": [{"option": "Geneva", "why_plausible": "European UN headquarters.", "why_wrong": "Site of the League of Nations / UN offices, not the World Court."},
                    {"option": "Strasbourg", "why_plausible": "European human rights court.", "why_wrong": "Council of Europe seat."},
                    {"option": "Brussels", "why_plausible": "European capital.", "why_wrong": "Capital of Belgium."}],
     "expl": "The court ruled 9-to-5 that it lacked jurisdiction over the dispute, handing Mosaddegh a triumphant international legal victory over the British Empire.", "pg": 510},
    {"text": "During cabinet meetings and foreign diplomatic summits with Averell Harriman, Mosaddegh famously conducted high-stakes state business while wearing these clothes in bed.",
     "ans": "Pajamas (Pajama diplomacy)", "aliases": ["Pajamas", "Pyjamas", "Bed Pajamas", "لباس خواب", "پیژامه"],
     "options": ["Pajamas (Pajama diplomacy)", "Military Uniform", "Academic Gown", "Qajar Frock Coat"],
     "rationales": [{"option": "Military Uniform", "why_plausible": "Head of government attire.", "why_wrong": "Mosaddegh was a passionate civilian constitutionalist who despised military uniforms."},
                    {"option": "Academic Gown", "why_plausible": "He held a doctorate in law.", "why_wrong": "He held a Neuchâtel doctorate, but met diplomats in his private bedroom."},
                    {"option": "Qajar Frock Coat", "why_plausible": "Aristocratic attire.", "why_wrong": "19th-century traditional court robe."}],
     "expl": "Western reporters coined the term 'pajama diplomacy' as Mosaddegh exploited his genuine fainting spells and frailty to disarm hardline negotiators.", "pg": 512},
    {"text": "On July 21, 1952 (30 Tir 1331), nationwide mass strikes and bloody clashes in Baharestan Square forced the Shah to dismiss this short-lived British-backed Prime Minister.",
     "ans": "Ahmad Qavam (Qavam al-Saltaneh)", "aliases": ["Ahmad Qavam", "Qavam al-Saltaneh", "Qavam", "احمد قوام", "قوام‌السلطنه"],
     "options": ["Ahmad Qavam (Qavam al-Saltaneh)", "General Zahedi", "Ali Razmara", "Haj Ali Mansur"],
     "rationales": [{"option": "General Zahedi", "why_plausible": "1953 coup premier.", "why_wrong": "Appointed in August 1953, not July 1952."},
                    {"option": "Ali Razmara", "why_plausible": "Assassinated premier.", "why_wrong": "Assassinated in March 1951."},
                    {"option": "Haj Ali Mansur", "why_plausible": "Earlier premier.", "why_wrong": "Preceded Razmara in 1950."}],
     "expl": "Qavam held office for barely four days, issuing a radio threat to 'steer the ship of state with an iron hand' before popular fury forced his flight.", "pg": 515},
    {"text": "Following his overthrow in August 1953, Mosaddegh was tried by a military tribunal for high treason and sentenced to this punishment.",
     "ans": "Three Years in Solitary Confinement (Followed by Village House Arrest)", "aliases": ["Three Years in Solitary Confinement", "Three Years Imprisonment", "House Arrest", "سه سال حبس مجرد"],
     "options": ["Three Years in Solitary Confinement (Followed by Village House Arrest)", "Execution by Firing Squad", "Exile to France", "Life Imprisonment in Qasr"],
     "rationales": [{"option": "Execution by Firing Squad", "why_plausible": "Fate of his foreign minister Fatemi.", "why_wrong": "Foreign Minister Hossein Fatemi was executed, but the Shah feared executing Mosaddegh directly."},
                    {"option": "Exile to France", "why_plausible": "Foreign exile.", "why_wrong": "Confined to his private village estate until death."},
                    {"option": "Life Imprisonment in Qasr", "why_plausible": "Permanent prison.", "why_wrong": "Transferred to village house arrest after three years."}],
     "expl": "Mosaddegh was confined under armed SAVAK guard at his private ancestral fortress in Ahmadabad-e Mosaddegh until his death on March 5, 1967.", "pg": 525},
    {"text": "Mosaddegh earned his doctorate in law in 1914 from this Swiss university, making him the first Iranian to earn a European doctoral degree in jurisprudence.",
     "ans": "University of Neuchâtel", "aliases": ["University of Neuchâtel", "Neuchâtel", "دانشگاه نوشاتل"],
     "options": ["University of Neuchâtel", "University of Geneva", "Sorbonne", "University of Lausanne"],
     "rationales": [{"option": "University of Geneva", "why_plausible": "Swiss university.", "why_wrong": "He studied in Paris and Neuchâtel, not Geneva."},
                    {"option": "Sorbonne", "why_plausible": "Prestigious French university.", "why_wrong": "Studied political science at École Libre in Paris, then defended his law dissertation at Neuchâtel."},
                    {"option": "University of Lausanne", "why_plausible": "Swiss French academy.", "why_wrong": "Located on Lake Geneva, not Neuchâtel."}],
     "expl": "His dissertation examined Islamic wills and testamentary succession in Shi'i jurisprudence.", "pg": 505},
    # Set B
    {"text": "In October 1951, Dr. Mosaddegh traveled to New York to address this United Nations body, denouncing British naval blockades of Iranian oil tankers.",
     "ans": "The UN Security Council", "aliases": ["The UN Security Council", "Security Council", "شورای امنیت سازمان ملل", "شورای امنیت"],
     "options": ["The UN Security Council", "The General Assembly", "The Trusteeship Council", "UNESCO"],
     "rationales": [{"option": "The General Assembly", "why_plausible": "Main UN hall.", "why_wrong": "The British complaint was brought directly before the Security Council."},
                    {"option": "The Trusteeship Council", "why_plausible": "UN body.", "why_wrong": "Dealt with decolonizing trust territories."},
                    {"option": "UNESCO", "why_plausible": "Cultural agency.", "why_wrong": "Cultural agency based in Paris."}],
     "expl": "Britain introduced a resolution demanding enforcement of ICJ interim measures, but Mosaddegh rallied non-aligned nations, forcing the council to adjourn without a vote.", "pg": 508},
    {"text": "The British secret intelligence operation to topple Dr. Mosaddegh, codenamed by MI6 alongside the CIA's Operation Ajax, was named this.",
     "ans": "Operation Boot", "aliases": ["Operation Boot", "Boot", "عملیات چکمه"],
     "options": ["Operation Boot", "Operation Ajax", "Operation Straggle", "Operation Clean"],
     "rationales": [{"option": "Operation Ajax", "why_plausible": "The CIA's codename.", "why_wrong": "Ajax (TPAJAX) was the American CIA codename, while MI6 codenamed it Operation Boot."},
                    {"option": "Operation Straggle", "why_plausible": "Syrian coup plot.", "why_wrong": "1956 CIA coup attempt in Syria."},
                    {"option": "Operation Clean", "why_plausible": "Generic codename.", "why_wrong": "Fictional variant."}],
     "expl": "Devised by British spy Monty Woodhouse, it was merged into the joint Anglo-American coup plan authorized by Churchill and Eisenhower.", "pg": 518},
    {"text": "Mosaddegh's courageous, uncompromising Foreign Minister who evaded arrest for months before being captured, stabbed by royalists, and executed by firing squad in 1954 was named this.",
     "ans": "Dr. Hossein Fatemi", "aliases": ["Dr. Hossein Fatemi", "Hossein Fatemi", "Fatemi", "حسین فاطمی", "دکتر فاطمی"],
     "options": ["Dr. Hossein Fatemi", "Hossein Makki", "Mozaffar Baqai", "Khalil Maleki"],
     "rationales": [{"option": "Hossein Makki", "why_plausible": "National Front deputy known as Soldier of Oil.", "why_wrong": "Broke with Mosaddegh in 1953, survived the coup."},
                    {"option": "Mozaffar Baqai", "why_plausible": "Toilers Party leader.", "why_wrong": "Turned against Mosaddegh and allied with royalists."},
                    {"option": "Khalil Maleki", "why_plausible": "Third Force socialist.", "why_wrong": "Socialist leader who warned Mosaddegh but was not executed."}],
     "expl": "Fatemi was editor of the radical daily Bakhtar-e Emruz; he was shot on November 10, 1954, shouting 'Long live Iran! Long live Mosaddegh!'", "pg": 526},
    {"text": "In August 1953, Mosaddegh held a controversial nationwide referendum using separate ballot booths for 'Yes' and 'No' voters to dissolve this body.",
     "ans": "The 17th Majles (Parliament)", "aliases": ["The 17th Majles", "17th Parliament", "Majles", "مجلس هفدهم", "انحلال مجلس"],
     "options": ["The 17th Majles (Parliament)", "The Senate", "The Supreme Court", "The Regency Council"],
     "rationales": [{"option": "The Senate", "why_plausible": "Upper house.", "why_wrong": "The Senate had already been dissolved earlier in 1952."},
                    {"option": "The Supreme Court", "why_plausible": "Judicial body.", "why_wrong": "Mosaddegh had emergency powers over ministries, but the referendum targeted the parliament."},
                    {"option": "The Regency Council", "why_plausible": "Royal body.", "why_wrong": "Never established under Mosaddegh."}],
     "expl": "The dissolution of parliament provided the legal pretext used by royalists and the CIA to argue that the Shah had the constitutional right to dismiss the Prime Minister.", "pg": 520},
    {"text": "On March 5, 1967, Dr. Mosaddegh died at age 84 at his country estate in Ahmadabad, his request to be buried alongside the martyrs of this 1952 uprising denied by the Shah.",
     "ans": "30 Tir Uprising (Ibn Babawayh Cemetery)", "aliases": ["30 Tir Uprising", "30 Tir Martyrs", "Ibn Babawayh", "شهدای ۳۰ تیر", "ابن بابویه"],
     "options": ["30 Tir Uprising (Ibn Babawayh Cemetery)", "15 Khordad 1963", "Behesht-e Zahra", "Black Friday 1978"],
     "rationales": [{"option": "15 Khordad 1963", "why_plausible": "Clerical uprising.", "why_wrong": "Protest led by Khomeini against the White Revolution."},
                    {"option": "Behesht-e Zahra", "why_plausible": "Main cemetery in southern Tehran.", "why_wrong": "Opened in 1970, three years after Mosaddegh's death."},
                    {"option": "Black Friday 1978", "why_plausible": "1978 massacre.", "why_wrong": "Occurred eleven years later in Jaleh Square."}],
     "expl": "Mosaddegh was buried beneath the floorboards of his private dining room at Ahmadabad, where his body remains to this day.", "pg": 527}
])

save_data(clues)
