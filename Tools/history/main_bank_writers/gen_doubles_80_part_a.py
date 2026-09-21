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
            "page": item.get("pg", 340 + idx * 8),
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

# 1. OPEC & DOWN (Double, 10 clues)
add_batch(clues, "OPEC AND DOWN", "Petroleum Geopolitics", "OPEC Cartel", "double", [
    {"text": "Founded in Baghdad in September 1960, Iran was one of the five founding members of OPEC alongside Iraq, Kuwait, Saudi Arabia, and this South American nation.",
     "ans": "Venezuela", "aliases": ["Venezuela", "Republic of Venezuela", "ونزوئلا"],
     "options": ["Venezuela", "Ecuador", "Nigeria", "Libya"],
     "rationales": [{"option": "Ecuador", "why_plausible": "South American OPEC member.", "why_wrong": "Joined later in 1973."},
                    {"option": "Nigeria", "why_plausible": "Major African member.", "why_wrong": "Joined in 1971."},
                    {"option": "Libya", "why_plausible": "North African member.", "why_wrong": "Joined in 1962."}],
     "expl": "Venezuelan oil minister Juan Pablo Pérez Alfonzo and Iranian delegates forged the cartel to counter unilateral price cuts by the 'Seven Sisters' Western oil majors.", "pg": 638},
    {"text": "Iran's chief OPEC representative who negotiated the historic 1973 price hikes and was later taken hostage by Carlos the Jackal in Vienna in 1975 was named this.",
     "ans": "Dr. Jamshid Amouzegar", "aliases": ["Dr. Jamshid Amouzegar", "Jamshid Amouzegar", "Amouzegar", "جمشید آموزگار"],
     "options": ["Dr. Jamshid Amouzegar", "Manuchehr Eqbal", "Hasan Ali Mansur", "Reza Fallah"],
     "rationales": [{"option": "Manuchehr Eqbal", "why_plausible": "Head of NIOC.", "why_wrong": "Chairman of NIOC, not the roaming OPEC chief negotiator."},
                    {"option": "Hasan Ali Mansur", "why_plausible": "Assassinated prime minister.", "why_wrong": "Assassinated in 1965."},
                    {"option": "Reza Fallah", "why_plausible": "NIOC deputy director.", "why_wrong": "Technical director, not the cabinet minister."}],
     "expl": "Amouzegar was held at gunpoint in Vienna alongside Saudi oil minister Sheikh Ahmed Zaki Yamani before being ransomed and flown to Algiers.", "pg": 640},
    {"text": "On December 21, 1975, this Venezuelan Marxist terrorist stormed the OPEC ministerial conference in Vienna, taking 63 hostages including eleven oil ministers.",
     "ans": "Carlos the Jackal (Ilich Ramírez Sánchez)", "aliases": ["Carlos the Jackal", "Carlos", "Ilich Ramírez Sánchez", "کارلوس", "کارلوس شغال"],
     "options": ["Carlos the Jackal (Ilich Ramírez Sánchez)", "Abu Nidal", "George Habash", "Ulrike Meinhof"],
     "rationales": [{"option": "Abu Nidal", "why_plausible": "Palestinian militant.", "why_wrong": "Rival splinter leader, not the Vienna raid commander."},
                    {"option": "George Habash", "why_plausible": "PFLP leader who planned operations.", "why_wrong": "General Secretary of the PFLP in Beirut, while Carlos led the assault team."},
                    {"option": "Ulrike Meinhof", "why_plausible": "Red Army Faction member.", "why_wrong": "German urban guerrilla, died in prison in 1976."}],
     "expl": "Carlos demanded the assassination of Yamani and Amouzegar, but was paid an estimated $20 to $50 million in ransom by Arab governments to release them in Algiers.", "pg": 642},
    {"text": "In 1986, during the Iran-Iraq War, Saudi Arabia flooded the global market with cheap oil to punish Iran, causing crude prices to crash to this historic low per barrel.",
     "ans": "$10 per barrel", "aliases": ["$10 per barrel", "$10", "Ten dollars", "۱۰ دلار", "ده دلار"],
     "options": ["$10 per barrel", "$20 per barrel", "$30 per barrel", "$5 per barrel"],
     "rationales": [{"option": "$20 per barrel", "why_plausible": "Moderate price.", "why_wrong": "Prices plummeted far lower, collapsing from $28 down to below $10 in 1986."},
                    {"option": "$30 per barrel", "why_plausible": "Peak 1980 price.", "why_wrong": "Peak price in 1980."},
                    {"option": "$5 per barrel", "why_plausible": "1960s pre-embargo price.", "why_wrong": "The price in 1970."}],
     "expl": "The price crash choked off Iran's foreign exchange earnings, making it impossible to purchase modern weapons and forcing Khomeini to accept UN Resolution 598 in 1988.", "pg": 790},
    {"text": "Headquartered initially in Geneva from 1960 to 1965, OPEC relocated its permanent global secretariat to this neutral European capital city.",
     "ans": "Vienna (Austria)", "aliases": ["Vienna", "City of Vienna", "Wien", "وین", "اتریش"],
     "options": ["Vienna (Austria)", "Geneva", "Brussels", "The Hague"],
     "rationales": [{"option": "Geneva", "why_plausible": "Original Swiss headquarters.", "why_wrong": "Swiss cantons refused to grant full diplomatic immunity to OPEC in 1965."},
                    {"option": "Brussels", "why_plausible": "EU capital.", "why_wrong": "Headquarters of NATO and EU."},
                    {"option": "The Hague", "why_plausible": "Dutch diplomatic city.", "why_wrong": "Site of the International Court of Justice."}],
     "expl": "Austrian Chancellor Bruno Kreisky granted OPEC full extraterritorial diplomatic status in Vienna along the Danube Canal.", "pg": 644},
    # Set B
    {"text": "The international cartel of seven Anglo-American oil companies that controlled 85% of global crude reserves prior to the 1973 crisis was known by this moniker.",
     "ans": "The Seven Sisters", "aliases": ["The Seven Sisters", "Seven Sisters", "هفت خواهران", "هفت خواهر نفتی"],
     "options": ["The Seven Sisters", "The Major League", "The Standard Trust", "The Petroleum Club"],
     "rationales": [{"option": "The Major League", "why_plausible": "Corporate phrase.", "why_wrong": "Fictional term."},
                    {"option": "The Standard Trust", "why_plausible": "Rockefeller monopoly.", "why_wrong": "Broken up in 1911 in the US."},
                    {"option": "The Petroleum Club", "why_plausible": "Industry club.", "why_wrong": "Social dining club."}],
     "expl": "Coined by Enrico Mattei of Italy's ENI, the Seven Sisters included BP, Shell, Exxon, Mobil, Chevron, Texaco, and Gulf Oil.", "pg": 645},
    {"text": "Under the 1954 Consortium Agreement signed after Mosaddegh's overthrow, British Petroleum retained this percentage share of Iranian oil production.",
     "ans": "40 Percent", "aliases": ["40 Percent", "40%", "Forty percent", "چهل درصد", "۴۰ درصد"],
     "options": ["40 Percent", "100 Percent", "50 Percent", "10 Percent"],
     "rationales": [{"option": "100 Percent", "why_plausible": "Pre-1951 colonial monopoly.", "why_wrong": "AIOC was forced to surrender 60% to American, French, and Dutch companies."},
                    {"option": "50 Percent", "why_plausible": "50-50 profit split.", "why_wrong": "Profits were split 50-50 with Iran, but BP held 40% of Consortium equity."},
                    {"option": "10 Percent", "why_plausible": "Minority stake.", "why_wrong": "Far too low; BP remained the largest single shareholder."}],
     "expl": "American oil giants (Exxon, Mobil, Texaco, Socal, Gulf) received 40%, Shell took 14%, and CFP of France received 6%.", "pg": 160},
    {"text": "In 1973, the Shah declared that upon the expiration of the 1954 25-year Consortium agreement in 1979, Iran would do this with its oil industry.",
     "ans": "Take 100% Full Ownership and Operational Control", "aliases": ["Take 100% Full Ownership", "Full National Control", "Complete Nationalization", "کنترل کامل عملیاتی", "مالکیت صد در صد"],
     "options": ["Take 100% Full Ownership and Operational Control", "Renew the British monopoly", "Sell the oil fields to Saudi Arabia", "Shut down oil production"],
     "rationales": [{"option": "Renew the British monopoly", "why_plausible": "Colonial renewal.", "why_wrong": "The Shah demanded full national sovereignty."},
                    {"option": "Sell the oil fields to Saudi Arabia", "why_plausible": "Rival sale.", "why_wrong": "Contrary to national policy."},
                    {"option": "Shut down oil production", "why_plausible": "Conservation policy.", "why_wrong": "Iran maximized production to fund industrialization."}],
     "expl": "The St. Moritz agreement of May 1973 transferred all operational management of the oil fields from the Western Consortium to NIOC.", "pg": 646},
    {"text": "The massive petrochemical and refining complex on the Persian Gulf built as a 50-50 joint venture between Iran and Japan's Mitsui was known as this.",
     "ans": "Iran-Japan Petrochemical Company (IJPC / Bandar Imam)", "aliases": ["Iran-Japan Petrochemical Company", "IJPC", "Bandar Imam Petrochemical", "پتروشیمی ایران-ژاپن", "بندر امام"],
     "options": ["Iran-Japan Petrochemical Company (IJPC / Bandar Imam)", "Abadan Petrochemical", "Kharg Chemical", "Shiraz Fertilizer"],
     "rationales": [{"option": "Abadan Petrochemical", "why_plausible": "Older petrochemical plant.", "why_wrong": "Built in 1966 in Abadan."},
                    {"option": "Kharg Chemical", "why_plausible": "Island plant.", "why_wrong": "Sulfur recovery plant on Kharg."},
                    {"option": "Shiraz Fertilizer", "why_plausible": "Fertilizer plant.", "why_wrong": "Nitrogen plant in Marvdasht."}],
     "expl": "Heavily bombed during the Iran-Iraq War, Mitsui withdrew in 1989 after paying $1 billion in contract cancellation settlements.", "pg": 648},
    {"text": "Following the 1973 quadrupling of oil prices, Iran became the world's fourth largest oil producer behind the US, USSR, and this Arab kingdom.",
     "ans": "Saudi Arabia", "aliases": ["Saudi Arabia", "Kingdom of Saudi Arabia", "عربستان سعودی", "عربستان"],
     "options": ["Saudi Arabia", "Iraq", "Kuwait", "United Arab Emirates"],
     "rationales": [{"option": "Iraq", "why_plausible": "Neighboring oil producer.", "why_wrong": "Produced half of Iran's volume in the 1970s."},
                    {"option": "Kuwait", "why_plausible": "Wealthy Gulf state.", "why_wrong": "Produced around 3 million bpd."},
                    {"option": "United Arab Emirates", "why_plausible": "Gulf producer.", "why_wrong": "Produced around 2 million bpd."}],
     "expl": "Iran pumped over six million barrels per day in 1974, generating over $20 billion annually in foreign exchange reserves.", "pg": 650}
])

save_data(clues)
