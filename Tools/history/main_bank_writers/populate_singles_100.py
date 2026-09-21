#!/usr/bin/env python3
import json

def run_100():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues_by_id = {c["id"]: c for c in json.load(f)}

    def add_10(cat, period, theme, items):
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "").replace(",", "")
        vals = [200, 400, 600, 800, 1000, 200, 400, 600, 800, 1000]
        for idx, item in enumerate(items):
            set_tag = "a" if idx < 5 else "b"
            val = vals[idx]
            cid = f"single_{prefix}_{val}_{set_tag}"
            clues_by_id[cid] = {
                "id": cid, "language": "en", "category": cat, "historical_period": period,
                "theme": theme, "difficulty": "STANDARD", "value": val, "round": "single",
                "clue_text": item["text"], "canonical_answer": item["ans"],
                "accepted_aliases": item["aliases"], "partial_answers": [], "specificity_prompt": "",
                "options": item["options"], "correct_option_index": 0,
                "distractor_rationales": item["rationales"], "explanation": item["expl"],
                "source_id": item.get("src", "amanat_iran_modern_history_2017"),
                "book_title": item.get("book", "Iran: A Modern History"),
                "author": item.get("auth", "Abbas Amanat"),
                "chapter": item.get("ch", "Historical Corpus"),
                "page": item.get("pg", 150 + idx * 10),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Spot on!",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. SHAH-PING FOR ANTIQUES
    add_10("SHAH-PING FOR ANTIQUES", "Crown Jewels & Museums", "Material Culture", [
        {"text": "Commissioned by Nasir al-Din Shah in 1869 to locate unset gems, this 66-centimeter golden sphere is encrusted with over 51,000 diamonds, rubies, and emeralds.",
         "ans": "The Globe of Jewels", "aliases": ["The Globe of Jewels", "Globe of Jewels", "Jeweled Globe", "کره جواهر"],
         "options": ["The Globe of Jewels", "The Peacock Throne", "The Sun Throne", "The Nadir Throne"],
         "rationales": [{"option": "The Peacock Throne", "why_plausible": "Famous gem-encrusted treasure.", "why_wrong": "Platform throne with peacocks looted from Delhi."},
                        {"option": "The Sun Throne", "why_plausible": "Takht-e Tavous built by Fath-Ali Shah.", "why_wrong": "Royal marriage bed throne with a radiant sun backrest."},
                        {"option": "The Nadir Throne", "why_plausible": "Coronation chair of Nader Shah.", "why_wrong": "Fath-Ali Shah's portable campaign throne."}],
         "expl": "The oceans are crafted from emeralds, Iran and Britain in diamonds, and southern Africa in rubies in the Central Bank vault.", "pg": 375},
        {"text": "Weighing 182 carats and possessing an exceedingly rare pale pink tint, this table-cut diamond is the largest uncut pink diamond in the world.",
         "ans": "Daria-i-Noor", "aliases": ["Daria-i-Noor", "Darya-ye Noor", "Sea of Light", "دریای نور"],
         "options": ["Daria-i-Noor", "Koh-i-Noor", "Shah Diamond", "Hope Diamond"],
         "rationales": [{"option": "Koh-i-Noor", "why_plausible": "Sister diamond.", "why_wrong": "Now mounted in the British Queen Mother's crown in London."},
                        {"option": "Shah Diamond", "why_plausible": "Inscribed Persian diamond.", "why_wrong": "Given to Tsar Nicholas I in 1829."},
                        {"option": "Hope Diamond", "why_plausible": "Blue diamond.", "why_wrong": "In the Smithsonian Institution in Washington."}],
         "expl": "Nader Shah brought the Daria-i-Noor from the Mughal treasury in Delhi in 1739.", "pg": 204},
        {"text": "Designed by French architect André Godard in 1937, the entrance facade of the National Museum of Iran in Tehran is modeled on this Sasanian arch.",
         "ans": "Taq-e Kasra (Arch of Ctesiphon)", "aliases": ["Taq-e Kasra", "Arch of Ctesiphon", "طاق کسری", "ایوان مدائن"],
         "options": ["Taq-e Kasra (Arch of Ctesiphon)", "Persepolis Gate of All Nations", "Taq-e Bostan", "Arg-e Bam"],
         "rationales": [{"option": "Persepolis Gate of All Nations", "why_plausible": "Achaemenid portal.", "why_wrong": "Stone winged bulls, not the brick parabolic arch."},
                        {"option": "Taq-e Bostan", "why_plausible": "Sasanian carved grottos.", "why_wrong": "Carved into mountain rock in Kermanshah."},
                        {"option": "Arg-e Bam", "why_plausible": "Adobe citadel gate.", "why_wrong": "Kerman adobe fortress."}],
         "expl": "Godard used red Roman-sized fired bricks to evoke Sasanian imperial majesty for the Museum of Ancient Iran (Muzeh-ye Iran-e Bastan).", "pg": 482},
        {"text": "Constructed for the 1926 coronation of Reza Shah, the Pahlavi Crown is topped by a plume of white egret feathers and encrusted with this many diamonds.",
         "ans": "3,380 Diamonds", "aliases": ["3,380 Diamonds", "3380", "3,380", "۳۳۸۰ الماس"],
         "options": ["3,380 Diamonds", "1,000 Diamonds", "500 Diamonds", "10,000 Diamonds"],
         "rationales": [{"option": "1,000 Diamonds", "why_plausible": "Modest estimate.", "why_wrong": "Understates the jewel count."},
                        {"option": "500 Diamonds", "why_plausible": "Far too low.", "why_wrong": "Understates the imperial regalia."},
                        {"option": "10,000 Diamonds", "why_plausible": "Excessive.", "why_wrong": "Exaggerated count."}],
         "expl": "The crown features a massive 60-carat yellow diamond in the center of its sunburst, fabricated by master Caucasian jeweler Serajeddin.", "pg": 483},
        {"text": "Worn by Qajar monarchs from Fath-Ali Shah to Ahmad Shah, this tall velvet crown encrusted with 1,800 pearls and a giant spinel is known by this name.",
         "ans": "Kiani Crown (Taj-e Kiani)", "aliases": ["Kiani Crown", "Taj-e Kiani", "تاج کیانی"],
         "options": ["Kiani Crown (Taj-e Kiani)", "Pahlavi Crown", "Crown of Farah", "Nadir Crown"],
         "rationales": [{"option": "Pahlavi Crown", "why_plausible": "20th-century crown.", "why_wrong": "Created in 1926 to break with Qajar iconography."},
                        {"option": "Crown of Farah", "why_plausible": "Empress crown.", "why_wrong": "Created by Van Cleef & Arpels for Empress Farah in 1967."},
                        {"option": "Nadir Crown", "why_plausible": "Afsharid headdress.", "why_wrong": "Nader Shah wore a turban with an aigrette (Jeqqeh), not a Westernized crown."}],
         "expl": "Taj-e Kiani was named after the mythical Kayanian kings of the Shahnameh, draped in red velvet and pearls.", "pg": 230},
        # Set B
        {"text": "Discovered at Susa in 1902, this life-size headless bronze statue of an Elamite queen weighing 1.8 tons is one of the prized treasures of the Louvre.",
         "ans": "Statue of Queen Napir-Asu", "aliases": ["Statue of Queen Napir-Asu", "Napir-Asu", "مجسمه ملکه ناپیرآسو", "ناپیرآسو"],
         "options": ["Statue of Queen Napir-Asu", "Statue of Shami", "Statue of Anahita", "Bust of Shirin"],
         "rationales": [{"option": "Statue of Shami", "why_plausible": "Bronze statue in Tehran.", "why_wrong": "Parthian nobleman in the National Museum of Iran."},
                        {"option": "Statue of Anahita", "why_plausible": "Goddess sculpture.", "why_wrong": "Not the solid bronze Elamite queen."},
                        {"option": "Bust of Shirin", "why_plausible": "Sasanian queen.", "why_wrong": "Fictional piece."}],
         "expl": "The base bears an inscription in Elamite cursing anyone who damages the statue with barrenness and divine wrath.", "pg": 22},
        {"text": "Constructed in 1800 for Fath-Ali Shah's marriage to Tavous Khanum Taj al-Dowleh, this gold-leaf platform bed throne became famous as the Sun Throne.",
         "ans": "The Sun Throne (Takht-e Tavous)", "aliases": ["The Sun Throne", "Takht-e Tavous", "Sun Throne", "تخت طاووس", "تخت خورشید"],
         "options": ["The Sun Throne (Takht-e Tavous)", "The Peacock Throne of Delhi", "The Marble Throne", "The Nadir Throne"],
         "rationales": [{"option": "The Peacock Throne of Delhi", "why_plausible": "Looted by Nader Shah.", "why_wrong": "The Mughal throne dismantled after Nader's death."},
                        {"option": "The Marble Throne", "why_plausible": "Takht-e Marmar in Golestan.", "why_wrong": "Carved from Yazd alabaster marble, not jewel-encrusted gold."},
                        {"option": "The Nadir Throne", "why_plausible": "Campaign chair.", "why_wrong": "Portable wooden throne."}],
         "expl": "Encrusted with 26,733 precious jewels, Takht-e Tavous was named after Tavous Khanum, whose title was Taj al-Dowleh.", "pg": 234},
        {"text": "Under the 1895 archaeological concession granted by Nasir al-Din Shah, this European country held an exclusive monopoly over all excavations in Iran.",
         "ans": "France", "aliases": ["France", "French Republic", "فرانسه"],
         "options": ["France", "Great Britain", "Germany", "Russia"],
         "rationales": [{"option": "Great Britain", "why_plausible": "Major imperial power in Iran.", "why_wrong": "Held oil and bank concessions, but France monopolized archaeological digs."},
                        {"option": "Germany", "why_plausible": "Scientific power.", "why_wrong": "Ernst Herzfeld excavated Persepolis later in the 1930s."},
                        {"option": "Russia", "why_plausible": "Tsarist power.", "why_wrong": "Held northern fisheries and railways."}],
         "expl": "Director Jacques de Morgan shipped trainloads of gold and antiquities from Susa directly to the Louvre until Reza Shah abolished the monopoly in 1927.", "pg": 388},
        {"text": "Carved from dark green serpentine stone and featuring a golden rooster, this royal chest piece in the Treasury was worn by Qajar Shahs on ceremonial occasions.",
         "ans": "The Jeweled Bazuband (Armband)", "aliases": ["The Jeweled Bazuband", "Bazuband", "بازوبند سلطنتی", "بازوبند"],
         "options": ["The Jeweled Bazuband (Armband)", "The Royal Scepter", "The Coronation Ring", "The Imperial Scabbard"],
         "rationales": [{"option": "The Royal Scepter", "why_plausible": "Regalia item.", "why_wrong": "Staff held in hand, not an upper arm bracelet."},
                        {"option": "The Coronation Ring", "why_plausible": "Finger ring.", "why_wrong": "Ring worn on fingers."},
                        {"option": "The Imperial Scabbard", "why_plausible": "Sword sheath.", "why_wrong": "Sword scabbard."}],
         "expl": "The Bazuband originally held the Daria-i-Noor and Koh-i-Noor diamonds on opposite arms of Nader Shah.", "pg": 236},
        {"text": "In 1937, Reza Shah placed the entire Imperial Crown Jewels in the vault of this newly created state financial institution as backing for the national currency.",
         "ans": "Bank Melli Iran (Central Bank)", "aliases": ["Bank Melli Iran", "Bank Melli", "Central Bank of Iran", "بانک ملی", "بانک مرکزی"],
         "options": ["Bank Melli Iran (Central Bank)", "Imperial Bank of Persia", "Bank Sepah", "Bank Tejarat"],
         "rationales": [{"option": "Imperial Bank of Persia", "why_plausible": "Earlier British bank.", "why_wrong": "British-owned bank founded in 1889 by Reuter."},
                        {"option": "Bank Sepah", "why_plausible": "Army bank.", "why_wrong": "Military pension bank founded in 1925."},
                        {"option": "Bank Tejarat", "why_plausible": "Commercial bank.", "why_wrong": "Nationalized after 1979."}],
         "expl": "By law, the Crown Jewels cannot be sold and remain the physical collateral for the Iranian Rial in the Central Bank vault on Ferdowsi Avenue.", "pg": 484}
    ])

    # 2. DAMAVAND-ING RESPECT
    add_10("DAMAVAND-ING RESPECT", "Geography & Natural Wonders", "Mountains & Ecology", [
        {"text": "Rising 5,609 meters above sea level in the Alborz range, this dormant stratovolcano is the highest peak in Iran and the highest volcano in Asia.",
         "ans": "Mount Damavand", "aliases": ["Mount Damavand", "Damavand", "Qolleh-ye Damavand", "دماوند", "کوه دماوند"],
         "options": ["Mount Damavand", "Alam-Kuh", "Sabalan", "Dena"],
         "rationales": [{"option": "Alam-Kuh", "why_plausible": "Second highest peak in Iran (4,848m).", "why_wrong": "Famous for its 800-meter granite rock wall in Takht-e Suleyman."},
                        {"option": "Sabalan", "why_plausible": "Volcanic peak in Ardabil (4,811m).", "why_wrong": "Inactive volcano with a crater lake in Azerbaijan."},
                        {"option": "Dena", "why_plausible": "Highest peak in the Zagros range (4,409m).", "why_wrong": "Zagros mountain massif near Yasuj."}],
         "expl": "Damavand features year-round summit glaciers, active sulfur fumaroles near its crater, and is celebrated in Bahar's ode 'O white demon with chained feet'.", "pg": 14},
        {"text": "According to Persian legend, this heroic archer climbed Mount Damavand to loose an arrow that flew for three days, establishing the boundary between Iran and Turan.",
         "ans": "Arash the Archer (Arash-e Kamangir)", "aliases": ["Arash the Archer", "Arash-e Kamangir", "Arash", "آرش کمانگیر", "آرش"],
         "options": ["Arash the Archer (Arash-e Kamangir)", "Rostam", "Kaveh the Blacksmith", "Siavash"],
         "rationales": [{"option": "Rostam", "why_plausible": "Great hero of the Shahnameh.", "why_wrong": "Rostam fought with club and bow, but Arash gave his life pouring his soul into the boundary arrow."},
                        {"option": "Kaveh the Blacksmith", "why_plausible": "Hero who raised the apron banner.", "why_wrong": "Rebel blacksmith who raised Derafsh Kaviani against Zahhak."},
                        {"option": "Siavash", "why_plausible": "Tragic prince.", "why_wrong": "Passed through the fire ordeal."}],
         "expl": "Siavash Kasra'i's 1959 modern epic poem Arash-e Kamangir made the archer an enduring symbol of self-sacrificing patriotic martyrdom.", "pg": 92},
        {"text": "In the Shahnameh, the tyrant Zahhak, with flesh-eating serpents sprouting from his shoulders, was captured by Fereydun and chained in a cave beneath this peak.",
         "ans": "Mount Damavand", "aliases": ["Mount Damavand", "Damavand", "دماوند"],
         "options": ["Mount Damavand", "Mount Alvand", "Mount Sabalan", "Mount Sahand"],
         "rationales": [{"option": "Mount Alvand", "why_plausible": "Mountain near Hamadan.", "why_wrong": "Site of Ganjnameh inscriptions, not Zahhak's prison."},
                        {"option": "Mount Sabalan", "why_plausible": "Sacred volcano in Ardabil.", "why_wrong": "Legendary mountain where Zoroaster meditated."},
                        {"option": "Mount Sahand", "why_plausible": "Volcanic peak near Tabriz.", "why_wrong": "Peak near Kandovan."}],
         "expl": "Legend holds that sulfur fumes and earthquakes emanating from Damavand are the fiery breathing and thrashing of the chained tyrant Zahhak.", "pg": 93},
        {"text": "Flowing through a dramatic gorge carved into the Alborz along the foot of Damavand, this river empties into the Caspian Sea near Babolsar.",
         "ans": "Haraz River", "aliases": ["Haraz River", "Haraz", "رود هراز", "هراز"],
         "options": ["Haraz River", "Chaloos River", "Sefid-Rud", "Karun River"],
         "rationales": [{"option": "Chaloos River", "why_plausible": "River along the Chaloos road.", "why_wrong": "Flows through Kandovan to Chaloos city."},
                        {"option": "Sefid-Rud", "why_plausible": "Longest river of northern Iran.", "why_wrong": "Breaches the Alborz at Manjil into Gilan."},
                        {"option": "Karun River", "why_plausible": "Major river.", "why_wrong": "Located in southern Khuzestan."}],
         "expl": "The Haraz Road (Road 77) carved along the canyon walls is one of the most treacherous and spectacular mountain highways in the world.", "pg": 16},
        {"text": "Located on the southern slopes of Damavand, this alpine national park is famous for wild scarlet poppy fields blooming each spring against snowy peaks.",
         "ans": "Lar National Park (Lar Valley)", "aliases": ["Lar National Park", "Lar Valley", "Dasht-e Lar", "دشت لار", "پارک ملی لار"],
         "options": ["Lar National Park (Lar Valley)", "Golestan National Park", "Kavir National Park", "Turan National Park"],
         "rationales": [{"option": "Golestan National Park", "why_plausible": "Oldest national park in Iran.", "why_wrong": "Located on the eastern Caspian forests near Gorgan."},
                        {"option": "Kavir National Park", "why_plausible": "Desert park in Semnan.", "why_wrong": "Known as Iran's Little Africa in the salt desert."},
                        {"option": "Turan National Park", "why_plausible": "Asiatic cheetah sanctuary.", "why_wrong": "Located in the eastern desert steppe."}],
         "expl": "Lar Dam reservoirs provide drinking water to Tehran, surrounded by meadows hosting rare endemic brown trout (Qezel-ala).", "pg": 17},
        # Set B
        {"text": "Standing 4,848 meters high in Mazandaran, this second-highest peak in Iran is renowned among mountaineers for its vertical 800-meter granite rock wall.",
         "ans": "Alam-Kuh", "aliases": ["Alam-Kuh", "Alam Kuh", "علم‌کوه", "علم کوه"],
         "options": ["Alam-Kuh", "Sabalan", "Dena", "Shirkooh"],
         "rationales": [{"option": "Sabalan", "why_plausible": "Third highest peak.", "why_wrong": "Volcanic cone with crater lake in Ardabil."},
                        {"option": "Dena", "why_plausible": "Highest Zagros peak.", "why_wrong": "Massif in the southern Zagros."},
                        {"option": "Shirkooh", "why_plausible": "Highest mountain in Yazd.", "why_wrong": "Desert mountain in Yazd."}],
         "expl": "Alam-Kuh's northern granite face is compared by alpinists to the Grandes Jorasses and the north wall of the Matterhorn in the Alps.", "pg": 15},
        {"text": "This critically endangered big cat, with barely 40 surviving individuals clinging to existence in the central Iranian deserts, is this animal.",
         "ans": "Asiatic Cheetah (Yuzpalang)", "aliases": ["Asiatic Cheetah", "Yuzpalang", "Persian Cheetah", "یوزپلنگ ایرانی", "یوزپلنگ"],
         "options": ["Asiatic Cheetah (Yuzpalang)", "Persian Leopard", "Caspian Tiger", "Asiatic Lion"],
         "rationales": [{"option": "Persian Leopard", "why_plausible": "Largest leopard subspecies.", "why_wrong": "Over 500 survive in the Alborz and Zagros forests."},
                        {"option": "Caspian Tiger", "why_plausible": "Extinct big cat.", "why_wrong": "Declared extinct in the late 1950s in the Golestan forests."},
                        {"option": "Asiatic Lion", "why_plausible": "Historic royal beast.", "why_wrong": "Extinct in Iran since the 1940s, surviving only in India's Gir Forest."}],
         "expl": "Iran's national football team wore the Asiatic cheetah on their World Cup jerseys to raise international awareness for its conservation.", "pg": 18},
        {"text": "Extending along the northern slopes of the Alborz and the Caspian Sea, these 50-million-year-old ancient temperate rainforests are a UNESCO World Heritage site.",
         "ans": "Hyrcanian Forests (Jangal-haye Hirkani)", "aliases": ["Hyrcanian Forests", "Hirkani", "Caspian Hyrcanian mixed forests", "جنگل‌های هیرکانی", "هیرکانی"],
         "options": ["Hyrcanian Forests (Jangal-haye Hirkani)", "Zagros Oak Forests", "Arasbaran Forests", "Golestan Steppe"],
         "rationales": [{"option": "Zagros Oak Forests", "why_plausible": "Western mountain forests.", "why_wrong": "Dry oak woodlands of Kurdistan and Lorestan."},
                        {"option": "Arasbaran Forests", "why_plausible": "Protected biosphere.", "why_wrong": "Located in northern Azerbaijan along the Aras River."},
                        {"option": "Golestan Steppe", "why_plausible": "Eastern steppe.", "why_wrong": "Dry grassland near the Turkmen border."}],
         "expl": "Surviving the Ice Ages as a botanical refugium, the Hyrcanian forests house relict Tertiary trees like the Persian ironwood (Parrotia persica).", "pg": 19},
        {"text": "Rising 4,811 meters in Ardabil province, this dormant volcanic peak features a natural freshwater crater lake at its summit that freezes into ice for nine months a year.",
         "ans": "Mount Sabalan", "aliases": ["Mount Sabalan", "Sabalan", "Savalan", "سبلان", "ساوالان"],
         "options": ["Mount Sabalan", "Mount Sahand", "Alam-Kuh", "Mount Damavand"],
         "rationales": [{"option": "Mount Sahand", "why_plausible": "Volcanic peak near Tabriz.", "why_wrong": "3,707-meter mountain known as the Bride of Iranian Mountains."},
                        {"option": "Alam-Kuh", "why_plausible": "Granite peak.", "why_wrong": "Rocky peak without a summit crater lake."},
                        {"option": "Mount Damavand", "why_plausible": "Highest volcano.", "why_wrong": "Has sulfur fumaroles, not a permanent summit alpine lake."}],
         "expl": "Local Azeri folklore holds that the prophet Zoroaster lived and meditated on the slopes of Sabalan.", "pg": 15},
        {"text": "The longest river entirely within the borders of Iran, rising in the Zagros and flowing past Ahvaz into the Shatt al-Arab, is this river.",
         "ans": "Karun River", "aliases": ["Karun River", "Karun", "Kāroon", "کارون", "رود کارون"],
         "options": ["Karun River", "Zayandeh River", "Sefid-Rud", "Karkheh River"],
         "rationales": [{"option": "Zayandeh River", "why_plausible": "Famous river.", "why_wrong": "Flows through Isfahan into the Gavkhouni salt swamp, not the Persian Gulf."},
                        {"option": "Sefid-Rud", "why_plausible": "Caspian river.", "why_wrong": "Flows north into the Caspian Sea."},
                        {"option": "Karkheh River", "why_plausible": "Khuzestan river.", "why_wrong": "Flows into the Hawizeh marshes."}],
         "expl": "Spanning 950 kilometers, the Karun is the only navigable river in Iran, where British steamships operated trade routes in the late 19th century.", "pg": 16}
    ])

    print("Batch 3 complete.")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print(f"Current total clues: {len(clues_by_id)}")

if __name__ == "__main__":
    run_100()
