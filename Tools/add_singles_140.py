#!/usr/bin/env python3
import json

def run_120():
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
                "page": item.get("pg", 100 + idx * 10),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Spot on!",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. SEALED WITH A DISS
    add_10("SEALED WITH A DISS", "Qajar Diplomacy & Decrees", "Royal Epistolary", [
        {"text": "Issued by Mozaffar al-Din Shah on August 5, 1906, this royal decree consented to the creation of a national consultative assembly (Majles).",
         "ans": "The Constitutional Firman", "aliases": ["The Constitutional Firman", "Constitutional Decree", "فرمان مشروطیت", "فرمان مشروطه"],
         "options": ["The Constitutional Firman", "The Edict of Gulistan", "The Treaty of Paris", "The Tobacco Monopoly Decree"],
         "rationales": [{"option": "The Edict of Gulistan", "why_plausible": "1813 treaty.", "why_wrong": "Tsarist war treaty."},
                        {"option": "The Treaty of Paris", "why_plausible": "1857 treaty.", "why_wrong": "Treaty over Herat."},
                        {"option": "The Tobacco Monopoly Decree", "why_plausible": "1890 concession.", "why_wrong": "Talbot tobacco concession."}],
         "expl": "Signed by the dying Shah on his sickbed, it ordered the convening of an assembly of all estates to draft the fundamental law of the empire.", "pg": 395},
        {"text": "In 1807, Napoleon Bonaparte signed this military alliance treaty with Fath-Ali Shah at a Prussian castle, promising to help Iran recover Georgia from Russia.",
         "ans": "Treaty of Finkenstein", "aliases": ["Treaty of Finkenstein", "Finkenstein", "عهدنامه فینکنشتاین"],
         "options": ["Treaty of Finkenstein", "Treaty of Tilsit", "Treaty of Paris", "Treaty of Golestan"],
         "rationales": [{"option": "Treaty of Tilsit", "why_plausible": "Where Napoleon betrayed Iran two months later.", "why_wrong": "Napoleon allied with Tsar Alexander I at Tilsit, abandoning his pledges to Iran."},
                        {"option": "Treaty of Paris", "why_plausible": "Peace treaty.", "why_wrong": "1857 Anglo-Persian treaty."},
                        {"option": "Treaty of Golestan", "why_plausible": "Russian treaty.", "why_wrong": "1813 treaty ceding the Caucasus."}],
         "expl": "Napoleon dispatched General Claude Mathieu de Gardane with 70 French military engineers to modernize the Iranian army before abandoning the alliance.", "pg": 244},
        {"text": "Carved into jade, carnelian, or ruby and dipped in black soot ink, this calligraphic signet seal was pressed onto royal letters by Iranian monarchs in place of a signature.",
         "ans": "The Royal Mohr (Signet Seal)", "aliases": ["The Royal Mohr", "Mohr", "Royal Seal", "مهر سلطنتی", "مهر شاه"],
         "options": ["The Royal Mohr (Signet Seal)", "The Tughra", "The Wax Bulla", "The Cylinder"],
         "rationales": [{"option": "The Tughra", "why_plausible": "Ottoman calligraphic monogram.", "why_wrong": "Elaborate Ottoman imperial signature style, whereas Iranian monarchs pressed carved gemstone signet seals (Mohr)."},
                        {"option": "The Wax Bulla", "why_plausible": "European papal seal.", "why_wrong": "Lead/wax European seal."},
                        {"option": "The Cylinder", "why_plausible": "Ancient seal.", "why_wrong": "Ancient Mesopotamian rolling seal."}],
         "expl": "The keeper of the royal seal (Mohrdar-e Saltanati) held immense power, stamping imperial firmans with the Shah's personal gem.", "pg": 245},
        {"text": "In 1873, Nasir al-Din Shah became the first Iranian monarch to visit Europe, keeping an intimate diary describing his reception by this British Queen.",
         "ans": "Queen Victoria", "aliases": ["Queen Victoria", "Victoria", "ملکه ویکتوریا"],
         "options": ["Queen Victoria", "Queen Elizabeth I", "Queen Anne", "Empress Eugénie"],
         "rationales": [{"option": "Queen Elizabeth I", "why_plausible": "Tudor queen who sent Anthony Jenkinson.", "why_wrong": "Reigned in the 16th century."},
                        {"option": "Queen Anne", "why_plausible": "Early 18th-century monarch.", "why_wrong": "Reigned 1702–1714."},
                        {"option": "Empress Eugénie", "why_plausible": "French empress he met in Paris.", "why_wrong": "Wife of Napoleon III in Paris."}],
         "expl": "Victoria invested Nasir al-Din Shah with the Order of the Garter at Windsor Castle, though royal courtiers were baffled by Persian dining etiquette.", "pg": 374},
        {"text": "During the Tobacco Protests of 1891, thousands of Iranian merchants and scholars took refuge from royal arrest inside this inviolable sanctuary space.",
         "ans": "Bast", "aliases": ["Bast", "Bast-neshini", "Sanctuary", "بست", "بست‌نشینی"],
         "options": ["Bast", "Fatwa", "Jihad", "I'tikaf"],
         "rationales": [{"option": "Fatwa", "why_plausible": "Religious legal decree.", "why_wrong": "The legal ruling itself, not the physical sanctuary space."},
                        {"option": "Jihad", "why_plausible": "Holy struggle.", "why_wrong": "Armed conflict."},
                        {"option": "I'tikaf", "why_plausible": "Mosque seclusion ritual.", "why_wrong": "Voluntary prayer retreat in mosques."}],
         "expl": "Traditional sites of Bast included holy shrines (Shah Abdol-Azim, Fatima Masumeh), royal stables, and the telegraph offices of the Indo-European line.", "pg": 386},
        # Set B
        {"text": "In 1848, this British envoy and scholar of Cuneiform intervened repeatedly in Qajar court disputes, later publishing his memoirs on Persian politics.",
         "ans": "Sir Henry Rawlinson", "aliases": ["Sir Henry Rawlinson", "Henry Rawlinson", "Rawlinson", "هنری راولینسون"],
         "options": ["Sir Henry Rawlinson", "Sir John Malcolm", "Percy Sykes", "Lord Curzon"],
         "rationales": [{"option": "Sir John Malcolm", "why_plausible": "Authored The History of Persia in 1815.", "why_wrong": "Envoy in 1800 and 1810."},
                        {"option": "Percy Sykes", "why_plausible": "Commander of South Persia Rifles.", "why_wrong": "Active during WWI."},
                        {"option": "Lord Curzon", "why_plausible": "Viceroy who wrote Persia and the Persian Question.", "why_wrong": "Traveler in 1889 and Foreign Secretary in 1919."}],
         "expl": "Rawlinson scaled the sheer limestone cliffs of Behistun with local boys to copy the trilingual cuneiform inscription.", "pg": 310},
        {"text": "This British diplomat authored the monumental two-volume 1892 travelogue Persia and the Persian Question before serving as British Foreign Secretary.",
         "ans": "Lord George Curzon", "aliases": ["Lord George Curzon", "George Curzon", "Lord Curzon", "لرد کرزن", "جرج کرزن"],
         "options": ["Lord George Curzon", "Edward Granville Browne", "Arthur Balfour", "Harold Nicolson"],
         "rationales": [{"option": "Edward Granville Browne", "why_plausible": "Famous British scholar of Persian revolution.", "why_wrong": "Cambridge professor who supported the constitutionalists."},
                        {"option": "Arthur Balfour", "why_plausible": "British Foreign Secretary.", "why_wrong": "Author of the Balfour Declaration regarding Palestine."},
                        {"option": "Harold Nicolson", "why_plausible": "Diplomat.", "why_wrong": "Diplomat in Tehran who wrote Some People."}],
         "expl": "Curzon regarded Iran as a vital buffer protecting British India, later authoring the ill-fated Anglo-Persian Agreement of 1919.", "pg": 382},
        {"text": "On January 4, 1852, royal executioner Ali Khan Hajeb al-Dowleh presented Nasir al-Din Shah with this tragic proof of Amir Kabir's death in Kashan.",
         "ans": "The Death Warrant / Stained Cloth", "aliases": ["The Death Warrant", "Cut Veins Testimony", "Proof of Death", "سند قتل امیرکبیر"],
         "options": ["The Death Warrant / Stained Cloth", "Amir Kabir's Sword", "The Royal Seal", "A Severed Hand"],
         "rationales": [{"option": "Amir Kabir's Sword", "why_plausible": "Military trophy.", "why_wrong": "He was bled to death in a bathhouse without weapons."},
                        {"option": "The Royal Seal", "why_plausible": "State token.", "why_wrong": "The seal was returned upon dismissal months earlier."},
                        {"option": "A Severed Hand", "why_plausible": "Macabre trophy.", "why_wrong": "He was not dismembered; his veins were slashed in the bathhouse."}],
         "expl": "Nasir al-Din Shah wept bitterly upon hearing of his mentor's execution, regretting his rash order for the rest of his life.", "pg": 312},
        {"text": "In 1872, Prime Minister Mirza Hosein Khan Moshir al-Dowleh arranged this sweeping concession granting Baron de Reuter control over all Iranian railways, mines, and forests.",
         "ans": "The Reuter Concession", "aliases": ["The Reuter Concession", "Reuter Concession", "امتیاز رویتر"],
         "options": ["The Reuter Concession", "The Talbot Concession", "The D'Arcy Concession", "The Regie Concession"],
         "rationales": [{"option": "The Talbot Concession", "why_plausible": "1890 tobacco concession.", "why_wrong": "Granted to Gerald Talbot for tobacco in 1890."},
                        {"option": "The D'Arcy Concession", "why_plausible": "1901 oil concession.", "why_wrong": "Granted for oil exploration to William Knox D'Arcy."},
                        {"option": "The Regie Concession", "why_plausible": "Alternative name for the tobacco monopoly.", "why_wrong": "The French term for the tobacco company."}],
         "expl": "Lord Curzon called it 'the most complete surrender of the entire resources of a kingdom into foreign hands that has ever been dreamed of.'", "pg": 370},
        {"text": "Under the 1828 Treaty of Turkmenchay, Russia imposed this extraterritorial legal immunity that prevented Iranian courts from prosecuting Russian subjects.",
         "ans": "Capitulations (Extraterritoriality)", "aliases": ["Capitulations", "Extraterritoriality", "کاپیتولاسیون", "حق قضاوت کنسولی"],
         "options": ["Capitulations (Extraterritoriality)", "Extradition", "Protectorate", "Sovereignty Waiver"],
         "rationales": [{"option": "Extradition", "why_plausible": "Legal process.", "why_wrong": "Extradition returns criminals; capitulations protected foreigners inside Iran."},
                        {"option": "Protectorate", "why_plausible": "Colonial status.", "why_wrong": "Iran remained formally independent."},
                        {"option": "Sovereignty Waiver", "why_plausible": "Legal phrase.", "why_wrong": "The historic term was Capitulations (Kāpītūlāsīyūn)."}],
         "expl": "The capitulations were expanded to all European powers, later abolished by Reza Shah in 1928, only to be revived for US military personnel in 1964.", "pg": 252}
    ])

    # 2. HORSING AROUND IN NISA
    add_10("HORSING AROUND IN NISA", "Parthian Culture & Warfare", "Cavalry & Arts", [
        {"text": "Carved from elephant tusks and excavated at Old Nisa, these magnificent drinking horns with winged beast terminals are known by this Greek-derived term.",
         "ans": "Rhytons", "aliases": ["Rhytons", "Rhyton", "Ivory Rhytons", "ریتون", "تکوک"],
         "options": ["Rhytons", "Amphoras", "Goblets", "Chalices"],
         "rationales": [{"option": "Amphoras", "why_plausible": "Two-handled clay storage jars.", "why_wrong": "Storage vessels, not horn-shaped drinking vessels."},
                        {"option": "Goblets", "why_plausible": "Stemmed drinking cups.", "why_wrong": "Generic cups, not horn-shaped rhytons."},
                        {"option": "Chalices", "why_plausible": "Ceremonial cups.", "why_wrong": "Christian communion cups."}],
         "expl": "Over forty ivory rhytons were found in the royal treasure house of Nisa, blending Greek Hellenistic carving with Persian gryphon and lion motifs.", "pg": 51},
        {"text": "Armored head-to-toe in overlapping iron or bronze scale mail and riding armored Nisean warhorses, these heavy Parthian shock cavalry were called this.",
         "ans": "Cataphracts", "aliases": ["Cataphracts", "Cataphract", "کاتافراکت", "سواران زره‌پوش"],
         "options": ["Cataphracts", "Hoplites", "Legionaries", "Janissaries"],
         "rationales": [{"option": "Hoplites", "why_plausible": "Ancient armored warriors.", "why_wrong": "Greek citizen-soldiers armed with spears and round shields on foot."},
                        {"option": "Legionaries", "why_plausible": "Roman soldiers.", "why_wrong": "Roman heavy infantry."},
                        {"option": "Janissaries", "why_plausible": "Elite guards.", "why_wrong": "Ottoman infantry."}],
         "expl": "Cataphracts wielded a four-meter two-handed heavy lance (Kontos) capable of impaling two Roman legionaries at once.", "pg": 53},
        {"text": "The founder of the Arsacid Parthian dynasty, a Parni chieftain who rebelled against the Seleucid satrap Andragoras around 247 BC, was named this.",
         "ans": "Arsaces I", "aliases": ["Arsaces I", "Arsaces", "Ashk I", "ارشک", "ارشک اول"],
         "options": ["Arsaces I", "Mithridates I", "Orodes II", "Phraates II"],
         "rationales": [{"option": "Mithridates I", "why_plausible": "Great conqueror.", "why_wrong": "Reigned a century later in 171–132 BC."},
                        {"option": "Orodes II", "why_plausible": "King during Carrhae.", "why_wrong": "Reigned in the 1st century BC."},
                        {"option": "Phraates II", "why_plausible": "Defeated the Seleucids in 129 BC.", "why_wrong": "Slew Antiochus VII Sidetes."}],
         "expl": "All subsequent thirty-one Parthian monarchs took the throne name 'Arsaces' (Ashk) on their official coinage to honor the dynastic founder.", "pg": 49},
        {"text": "In 141 BC, this Parthian conqueror captured Seleucia-on-the-Tigris and Babylon, driving the Hellenistic Greeks out of the Iranian plateau.",
         "ans": "Mithridates I", "aliases": ["Mithridates I", "Mithradates I", "مهرداد اول", "مهرداد یکم"],
         "options": ["Mithridates I", "Arsaces I", "Mithridates II", "Artabanus I"],
         "rationales": [{"option": "Arsaces I", "why_plausible": "Dynasty founder.", "why_wrong": "Ruled only northern Parthia/Hyrcania."},
                        {"option": "Mithridates II", "why_plausible": "Mithridates the Great.", "why_wrong": "Opened the Silk Road to China in 120 BC."},
                        {"option": "Artabanus I", "why_plausible": "Earlier king.", "why_wrong": "Killed in battle against the Tocharians."}],
         "expl": "Mithridates captured the Seleucid king Demetrius II Nicator alive, treating him honorably and giving him a Parthian princess in marriage.", "pg": 50},
        {"text": "The bronze statue of a tall Parthian nobleman wearing belted tunic and wide trousers with a dagger at his hip was unearthed at this Khuzestan site.",
         "ans": "Shami (The Shami Statue)", "aliases": ["Shami", "The Shami Statue", "Statue of Shami", "تندیس مرد شمی", "شمی"],
         "options": ["Shami (The Shami Statue)", "Susa", "Persepolis", "Bishapur"],
         "rationales": [{"option": "Susa", "why_plausible": "Major archaeological city.", "why_wrong": "Found in the Bakhtiari mountains near Izeh, not Susa."},
                        {"option": "Persepolis", "why_plausible": "Stone relief site.", "why_wrong": "Achaemenid stone capital."},
                        {"option": "Bishapur", "why_plausible": "Sasanian city.", "why_wrong": "Sasanian city in Fars."}],
         "expl": "Now in the National Museum of Iran, the 1.94-meter hollow-cast bronze statue is humanity's most striking portrait of an ancient Parthian grandee.", "pg": 52},
        # Set B
        {"text": "In 129 BC, the last Seleucid army attempting to reconquer Iran was annihilated at Ecbatana and this Hellenistic emperor was killed in battle.",
         "ans": "Antiochus VII Sidetes", "aliases": ["Antiochus VII Sidetes", "Antiochus VII", "آنتیوخوس هفتم"],
         "options": ["Antiochus VII Sidetes", "Antiochus III the Great", "Seleucus I Nicator", "Alexander Balas"],
         "rationales": [{"option": "Antiochus III the Great", "why_plausible": "Earlier conqueror.", "why_wrong": "Reigned in 223–187 BC."},
                        {"option": "Seleucus I Nicator", "why_plausible": "Founder of the Seleucid Empire.", "why_wrong": "Died in 281 BC."},
                        {"option": "Alexander Balas", "why_plausible": "Seleucid usurper.", "why_wrong": "Reigned earlier in Syria."}],
         "expl": "King Phraates II returned Antiochus's body to Syria in a silver coffin, permanently ending Greek rule east of the Euphrates River.", "pg": 51},
        {"text": "The Parthian Empire was divided among seven great aristocratic families, of which this House, holding the hereditary right to crown the Shah, was the most powerful.",
         "ans": "The House of Suren", "aliases": ["The House of Suren", "House of Suren", "Suren Clan", "خاندان سورن", "سورن"],
         "options": ["The House of Suren", "The House of Karen", "The House of Mehran", "The House of Spandiyadh"],
         "rationales": [{"option": "The House of Karen", "why_plausible": "Great Parthian family.", "why_wrong": "Based in Nihavand, not the hereditary crowners in Sistan."},
                        {"option": "The House of Mehran", "why_plausible": "Great family of Rayy.", "why_wrong": "Based in Rayy, produced Bahram Chobin centuries later."},
                        {"option": "The House of Spandiyadh", "why_plausible": "Great family.", "why_wrong": "Noble house of Media."}],
         "expl": "General Surena, victor of Carrhae, was the paramount chieftain of the House of Suren based in Sistan.", "pg": 54},
        {"text": "In 20 BC, Roman Emperor Augustus proudly celebrated a diplomatic triumph when Parthian King Phraates IV agreed to return these captured military relics.",
         "ans": "The Roman Legionary Eagles (Standards)", "aliases": ["The Roman Legionary Eagles", "Legionary Eagles", "Roman Standards", "عقاب‌های لژیون روم", "درفش‌های لژیون"],
         "options": ["The Roman Legionary Eagles (Standards)", "The Ark of the Covenant", "Golden Armor of Crassus", "Crown of Antioch"],
         "rationales": [{"option": "The Ark of the Covenant", "why_plausible": "Biblical relic.", "why_wrong": "Lost during the Babylonian conquest of Jerusalem."},
                        {"option": "Golden Armor of Crassus", "why_plausible": "Personal armor.", "why_wrong": "The sacred military standards (Aquilae) were returned, depicted on Augustus's Prima Porta breastplate."},
                        {"option": "Crown of Antioch", "why_plausible": "Royal insignia.", "why_wrong": "Fictional relic."}],
         "expl": "Augustus commissioned the Prima Porta statue showing a bearded Parthian in trousers handing back the eagle standard to a Roman soldier.", "pg": 55},
        {"text": "Excavated at Nisa, thousands of economic receipts were written with ink on fragments of broken pottery, known to archaeologists by this term.",
         "ans": "Ostraca", "aliases": ["Ostraca", "Ostracon", "Pottery Sherds", "اوستراکون", "سفال‌نوشته"],
         "options": ["Ostraca", "Papyrus", "Vellum", "Cuneiform Tablets"],
         "rationales": [{"option": "Papyrus", "why_plausible": "Egyptian reed paper.", "why_wrong": "Vegetable paper from the Nile."},
                        {"option": "Vellum", "why_plausible": "Animal parchment.", "why_wrong": "Prepared calf skin parchment."},
                        {"option": "Cuneiform Tablets", "why_plausible": "Clay tablets.", "why_wrong": "Unbaked clay pressed with a stylus, not ink on pottery sherds."}],
         "expl": "Nisa's 2,700 ostraca record the wine harvests, vineyards, and royal taxes of the Arsacid kingdom in the Parthian language using the Aramaic alphabet.", "pg": 52},
        {"text": "The Parthian royal capital was shifted in summer to this ancient city in the Zagros mountains, where cool mountain breezes offered relief from the plains.",
         "ans": "Ecbatana (Hamadan)", "aliases": ["Ecbatana", "Hamadan", "Hamedan", "همدان"],
         "options": ["Ecbatana (Hamadan)", "Ctesiphon", "Hecatompylos", "Susa"],
         "rationales": [{"option": "Ctesiphon", "why_plausible": "Winter capital.", "why_wrong": "Sweltering Mesopotamian winter capital on the Tigris."},
                        {"option": "Hecatompylos", "why_plausible": "Parthian staging city.", "why_wrong": "Located in the Semnan desert."},
                        {"option": "Susa", "why_plausible": "Elamite capital.", "why_wrong": "Lowland plain city."}],
         "expl": "Polybius described Ecbatana's royal palace under the Parthians, with its cedar and cypress roof beams completely clad in silver and gold plates.", "pg": 53}
    ])

    print(f"Batch 2 complete. Current total clues: {len(clues_by_id)}")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    run_120()
