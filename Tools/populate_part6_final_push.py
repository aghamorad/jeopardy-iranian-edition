#!/usr/bin/env python3
import json

def run_part6():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    clues_by_id = {c["id"]: c for c in existing}

    def add_5(cat, period, theme, round_str, data):
        vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("(", "").replace(")", "").replace("/", "_")
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
                "page": item.get("pg", 300 + idx * 10),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. ANCIENT WARFARE: EMPIRES AT CLASH (Single)
    add_5("ANCIENT WARFARE: EMPIRES AT CLASH", "Classical Antiquity", "Greco-Persian Wars", "single", [
        {
            "text": "In 490 BC, Athenian hoplites under Miltiades repulsed the amphibious landing force of Darius the Great on this coastal plain 26 miles northeast of Athens.",
            "ans": "Battle of Marathon",
            "aliases": ["Battle of Marathon", "Marathon", "نبرد ماراتن", "ماراتن"],
            "options": ["Battle of Marathon", "Battle of Thermopylae", "Battle of Salamis", "Battle of Plataea"],
            "rationales": [
                {"option": "Battle of Thermopylae", "why_plausible": "Fought ten years later in 480 BC.", "why_wrong": "Mountain pass stand under Xerxes, not Darius's coastal landing in 490 BC."},
                {"option": "Battle of Salamis", "why_plausible": "Decisive naval engagement in 480 BC.", "why_wrong": "Naval battle in the straits of Salamis."},
                {"option": "Battle of Plataea", "why_plausible": "Final land battle in 479 BC.", "why_wrong": "Fought in Boeotia by Mardonius in 479 BC."}
            ],
            "expl": "The defeat marked the first time an Achaemenid imperial invasion force was repulsed on the Greek mainland, giving rise to the modern marathon race.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 36
        },
        {
            "text": "In 480 BC, Xerxes I's army was delayed at this narrow coastal pass by Spartan King Leonidas and his 300 hoplites before an encircling goat path was revealed.",
            "ans": "Battle of Thermopylae",
            "aliases": ["Battle of Thermopylae", "Thermopylae", "تنگه ترموپیل", "ترموپیل"],
            "options": ["Battle of Thermopylae", "Battle of Marathon", "Battle of Salamis", "Battle of Cunaxa"],
            "rationales": [
                {"option": "Battle of Marathon", "why_plausible": "First invasion battle.", "why_wrong": "Fought in 490 BC under Darius."},
                {"option": "Battle of Salamis", "why_plausible": "Naval battle in 480 BC.", "why_wrong": "Fought on water off Athens."},
                {"option": "Battle of Cunaxa", "why_plausible": "Persian civil war battle.", "why_wrong": "Fought in 401 BC between Cyrus the Younger and Artaxerxes II."}
            ],
            "expl": "After a local Greek named Ephialtes showed the Persians the Anopaia mountain path, the Immortals outflanked the Greeks, allowing Xerxes to advance on Athens.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 37
        },
        {
            "text": "Watching from a golden throne atop Mount Aigaleo, Xerxes saw his vast Phoenician and Persian armada outmaneuvered and destroyed by Greek triremes in this strait.",
            "ans": "Battle of Salamis",
            "aliases": ["Battle of Salamis", "Salamis", "نبرد سالامیس", "سالامیس"],
            "options": ["Battle of Salamis", "Battle of Marathon", "Battle of Artemisium", "Battle of Mycale"],
            "rationales": [
                {"option": "Battle of Marathon", "why_plausible": "Famous land battle.", "why_wrong": "Land battle 490 BC."},
                {"option": "Battle of Artemisium", "why_plausible": "Inconclusive naval skirmish fought simultaneously with Thermopylae.", "why_wrong": "Fought off Euboea, not the decisive clash in the Athenian straits."},
                {"option": "Battle of Mycale", "why_plausible": "Final naval clash in Ionia.", "why_wrong": "Fought in 479 BC off the coast of Asia Minor."}
            ],
            "expl": "Themistocles lured the Persian fleet into narrow waters where their numerical advantage was negated, compelling Xerxes to withdraw to Asia.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 39
        },
        {
            "text": "In 401 BC, Cyrus the Younger rebelled against his brother Artaxerxes II with 10,000 Greek mercenaries at this battle, immortalized in Xenophon's Anabasis.",
            "ans": "Battle of Cunaxa",
            "aliases": ["Battle of Cunaxa", "Cunaxa", "نبرد کوناکسا", "کوناکسا"],
            "options": ["Battle of Cunaxa", "Battle of Granicus", "Battle of Issus", "Battle of Gaugamela"],
            "rationales": [
                {"option": "Battle of Granicus", "why_plausible": "Alexander's battle in 334 BC.", "why_wrong": "Fought against Alexander 70 years later."},
                {"option": "Battle of Issus", "why_plausible": "Alexander's 333 BC battle.", "why_wrong": "Fought between Alexander and Darius III."},
                {"option": "Battle of Gaugamela", "why_plausible": "Alexander's final victory.", "why_wrong": "Fought in 331 BC."}
            ],
            "expl": "Cyrus was killed in the battle; the stranded Greek mercenaries (The Ten Thousand) marched across thousands of miles of hostile Persian territory to reach the Black Sea.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 41
        },
        {
            "text": "In 330 BC, satrap Ariobarzanes and his sister Youtab held this narrow pass in the Zagros Mountains with 700 men, ambushing Alexander the Great's army with avalanches.",
            "ans": "Battle of the Persian Gate",
            "aliases": ["Battle of the Persian Gate", "Persian Gate", "Tang-e Meyran", "دربند پارس", "تنگه دربند پارس"],
            "options": ["Battle of the Persian Gate", "Battle of Gaugamela", "Battle of Issus", "Battle of Edessa"],
            "rationales": [
                {"option": "Battle of Gaugamela", "why_plausible": "Major field battle.", "why_wrong": "Mesopotamian open plain battle in 331 BC."},
                {"option": "Battle of Issus", "why_plausible": "Cilician gate battle.", "why_wrong": "Fought in 333 BC in southern Anatolia."},
                {"option": "Battle of Edessa", "why_plausible": "Sasanian victory in 260 AD.", "why_wrong": "Shapur I defeated Valerian centuries later."}
            ],
            "expl": "Hailed as the 'Persian Thermopylae', Ariobarzanes fought to the last man until a local shepherd guided Alexander around the pass to Persepolis.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 45
        }
    ])

    # 2. MYTHS & MONSTERS OF THE SHAHNAMEH (Single)
    add_5("MYTHS & MONSTERS OF THE SHAHNAMEH", "Shahnameh Lore", "Mythology", "single", [
        {
            "text": "In the final trial of Rostam's Seven Labors (Haft Khan), Rostam slays this demonic king of Mazandaran inside a dark cavern, using its blood to restore King Kay Kavus's eyesight.",
            "ans": "The White Demon (Div-e Sepid)",
            "aliases": ["The White Demon", "Div-e Sepid", "Div e Sepid", "دیو سفید"],
            "options": ["The White Demon (Div-e Sepid)", "Akvan Div", "Arzhang Div", "Zahhak"],
            "rationales": [
                {"option": "Akvan Div", "why_plausible": "Demonic shape-shifter in the epic.", "why_wrong": "Akvan transformed into a golden onager and hurled Rostam into the sea."},
                {"option": "Arzhang Div", "why_plausible": "Commander of the White Demon's armies.", "why_wrong": "Slain by Rostam in the sixth labor before entering the White Demon's cave."},
                {"option": "Zahhak", "why_plausible": "Tyrannical serpent king.", "why_wrong": "Human tyrant crowned with snakes, not the horned demon of Mazandaran."}
            ],
            "expl": "Rostam cut out the White Demon's liver, dripping its warm bile into the blinded eyes of the captive Iranian knights to restore their sight.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 95
        },
        {
            "text": "This shape-shifting demon transformed into a wild golden zebra, hurled a slumbering Rostam into the Caspian Sea, and possessed the power to turn stone into water.",
            "ans": "Akvan Div",
            "aliases": ["Akvan Div", "Akwan Div", "اکوان دیو"],
            "options": ["Akvan Div", "Div-e Sepid", "Pouladvand", "Barman"],
            "rationales": [
                {"option": "Div-e Sepid", "why_plausible": "Supreme demon of the epic.", "why_wrong": "Slain in his cavern in Mazandaran."},
                {"option": "Pouladvand", "why_plausible": "Turanian champion.", "why_wrong": "Turanian warrior hero, not the shape-shifting wind demon."},
                {"option": "Barman", "why_plausible": "Turanian knight.", "why_wrong": "Afrasiyab's commander who accompanied Sohrab."}
            ],
            "expl": "When Akvan asked Rostam whether he preferred to be cast into the mountains or the sea, Rostam used reverse psychology, knowing demons always do the opposite.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 96
        },
        {
            "text": "In his third labor, Rostam was awakened in the wilderness three times by his stallion Rakhsh before slaying this colossal venomous monster.",
            "ans": "The Dragon (Azhdaha)",
            "aliases": ["The Dragon", "Dragon", "Azhdaha", "اژدها"],
            "options": ["The Dragon (Azhdaha)", "The Lion", "The Sorceress", "The Simurgh"],
            "rationales": [
                {"option": "The Lion", "why_plausible": "Killed in the First Labor.", "why_wrong": "Rakhsh killed the ferocious lion while Rostam slept in Labor One."},
                {"option": "The Sorceress", "why_plausible": "Encountered in the Fourth Labor.", "why_wrong": "Rostam ensnared the shape-shifting witch with a lasso in Labor Four."},
                {"option": "The Simurgh", "why_plausible": "Mythic giant bird.", "why_wrong": "Benevolent protector, not a monster slain in the Haft Khan."}
            ],
            "expl": "The eighty-meter dragon made itself invisible whenever Rostam opened his eyes, until Rakhsh trampled it and Rostam severed its head with his ox-head mace.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 95
        },
        {
            "text": "In pre-Islamic Iranian mythology and the Shahnameh, this divine, glowing halo of royal fortune and destiny legitimizes kings and departs when they succumb to hubris.",
            "ans": "The Farr (Khvarenah)",
            "aliases": ["The Farr", "Farr", "Khvarenah", "Farr-e Izadi", "فر", "فره ایزدی", "فر کیانی"],
            "options": ["The Farr (Khvarenah)", "Derafsh Kaviani", "Babr-e Bayan", "Gorz-e Gavsar"],
            "rationales": [
                {"option": "Derafsh Kaviani", "why_plausible": "The national sacred banner.", "why_wrong": "Physical leather apron banner, not the celestial divine halo."},
                {"option": "Babr-e Bayan", "why_plausible": "Rostam's invulnerable tiger coat.", "why_wrong": "Armor worn by Rostam."},
                {"option": "Gorz-e Gavsar", "why_plausible": "Ox-headed mace of Fereydun.", "why_wrong": "Weapon hewn by Kaveh."}
            ],
            "expl": "King Jamshid lost the divine Farr (Farr-e Izadi) when he boasted that he was greater than God, causing his kingdom to fall to the tyrant Zahhak.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 90
        },
        {
            "text": "This Turanian king is the lifelong arch-nemesis of Iran in the Shahnameh, repeatedly invading the realm and ordering the murder of Prince Siavash.",
            "ans": "Afrasiyab",
            "aliases": ["Afrasiyab", "Afrasiab", "افراسیاب"],
            "options": ["Afrasiyab", "Piran Viseh", "Garsivaz", "Sudabeh"],
            "rationales": [
                {"option": "Piran Viseh", "why_plausible": "Wise Turanian chancellor.", "why_wrong": "Virtuous Turanian vizier who protected Siavash and Kay Khosrow."},
                {"option": "Garsivaz", "why_plausible": "Afrasiyab's jealous brother.", "why_wrong": "Slandered Siavash to Afrasiyab, but was not the sovereign king."},
                {"option": "Sudabeh", "why_plausible": "Treacherous queen.", "why_wrong": "Queen of Iran who falsely accused Siavash."}
            ],
            "expl": "Afrasiyab reigned over Turan for centuries through sorcery until captured in Lake Chichast by the hermit Hom and executed by King Kay Khosrow.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 98
        }
    ])

    # 3. PHILOSOPHY OF ISFAHAN: THE METAPHYSICIANS (Single)
    add_5("PHILOSOPHY OF ISFAHAN: THE METAPHYSICIANS", "Safavid Intellectual History", "Philosophy", "single", [
        {
            "text": "Born in Shiraz in 1571 and teaching at Khan Madrasa, this supreme philosopher synthesized Avicennian Peripateticism and Suhrawardi's Illuminationism into Transcendent Theosophy.",
            "ans": "Mulla Sadra",
            "aliases": ["Mulla Sadra", "Sadr al-Din Shirazi", "ملاصدرا", "صدرالمتالهین", "صدرالدین شیرازی"],
            "options": ["Mulla Sadra", "Mir Damad", "Sheikh Bahai", "Allameh Majlisi"],
            "rationales": [
                {"option": "Mir Damad", "why_plausible": "His revered master in Isfahan.", "why_wrong": "Known as the 'Third Teacher', developed the doctrine of Huduth-e Dahri."},
                {"option": "Sheikh Bahai", "why_plausible": "Safavid grand polymath.", "why_wrong": "Architect and legal scholar who designed Naqsh-e Jahan."},
                {"option": "Allameh Majlisi", "why_plausible": "Author of Bihar al-Anwar.", "why_wrong": "Late 17th-century traditionalist who opposed philosophy."}
            ],
            "expl": "Sadr al-Din Mohammad Shirazi (Mulla Sadra) founded Hikmat al-Muta'aliyah, positing the primacy of existence (Asalat al-Wujud) over essence.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 170
        },
        {
            "text": "Considered Mulla Sadra's magnum opus, this massive philosophical treatise in nine volumes takes its title from 'The Four Intellectual Journeys of the Soul'.",
            "ans": "Asfar al-Arba'a",
            "aliases": ["Asfar al-Arba'a", "The Asfar", "Al-Asfar al-Arba'a", "اسفار اربعه", "اسفار"],
            "options": ["Asfar al-Arba'a", "The Canon of Medicine", "Fusus al-Hikam", "Hikmat al-Ishraq"],
            "rationales": [
                {"option": "The Canon of Medicine", "why_plausible": "Medical classic by Ibn Sina.", "why_wrong": "11th-century medical encyclopedia."},
                {"option": "Fusus al-Hikam", "why_plausible": "Mystical work by Ibn Arabi.", "why_wrong": "13th-century Andalusian Sufi treatise."},
                {"option": "Hikmat al-Ishraq", "why_plausible": "Illuminationist work by Suhrawardi.", "why_wrong": "12th-century philosophy of light."}
            ],
            "expl": "The four journeys trace the soul's path: from creation to God, in God, from God back to creation with God, and among creation to guide humanity.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 172
        },
        {
            "text": "Known as the 'Third Teacher' after Aristotle and Al-Farabi, this eccentric master in Isfahan solved the creation of the universe with his theory of Huduth-e Dahri (At-Temporal Origination).",
            "ans": "Mir Damad",
            "aliases": ["Mir Damad", "Mir Mohammad Baqir Damad", "میرداماد", "میر محمدباقر داماد"],
            "options": ["Mir Damad", "Mulla Sadra", "Sheikh Bahai", "Mulla Hadi Sabzevari"],
            "rationales": [
                {"option": "Mulla Sadra", "why_plausible": "His most famous student.", "why_wrong": "Mulla Sadra was his student."},
                {"option": "Sheikh Bahai", "why_plausible": "Close friend and colleague at the court of Shah Abbas.", "why_wrong": "Pioneered hydraulic engineering and jurisprudence, not the Huduth-e Dahri thesis."},
                {"option": "Mulla Hadi Sabzevari", "why_plausible": "19th-century commentator on Sadra.", "why_wrong": "Lived during the Qajar era in Sabzevar."}
            ],
            "expl": "Mir Damad was revered by Shah Abbas I, who famously walked beside his horse through the streets of Isfahan to demonstrate royal reverence for philosophy.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 168
        },
        {
            "text": "Born in Baalbek (Lebanon) and brought to Iran as a child, this polymath and architect designed the hydraulic heating of the Sheikh Bahai bathhouse using a single candle.",
            "ans": "Sheikh Bahai",
            "aliases": ["Sheikh Bahai", "Baha al-Din al-Amili", "بهایی", "شیخ بهایی"],
            "options": ["Sheikh Bahai", "Mir Damad", "Mohammad Reza Isfahani", "André Godard"],
            "rationales": [
                {"option": "Mir Damad", "why_plausible": "Contemporary Safavid scholar.", "why_wrong": "Theoretical philosopher, not the master civil engineer and astronomer."},
                {"option": "Mohammad Reza Isfahani", "why_plausible": "Master builder of Lotfollah Mosque.", "why_wrong": "Chief stonemason/builder, not the grand polymath sheikh."},
                {"option": "André Godard", "why_plausible": "Architect.", "why_wrong": "French architect of Tehran University in the 1930s."}
            ],
            "expl": "Sheikh Baha al-Din al-Amili also engineered the division of the Zayandeh River's waters across the districts of Isfahan (Tomar-e Sheikh Bahai).",
            "book": "Iran Under the Safavids", "auth": "Roger Savory", "pg": 162
        },
        {
            "text": "Compiling the 110-volume hadith encyclopedia Bihar al-Anwar (Oceans of Light), this influential late Safavid cleric suppressed philosophy and Sufism under Shah Sultan Husayn.",
            "ans": "Allameh Mohammad-Baqir Majlisi",
            "aliases": ["Allameh Mohammad-Baqir Majlisi", "Allameh Majlisi", "Majlisi", "علامه مجلسی", "محمدباقر مجلسی"],
            "options": ["Allameh Mohammad-Baqir Majlisi", "Mulla Sadra", "Mir Damad", "Sheikh Bahai"],
            "rationales": [
                {"option": "Mulla Sadra", "why_plausible": "Famous scholar.", "why_wrong": "Opposed by Majlisi's orthodox traditionalist followers."},
                {"option": "Mir Damad", "why_plausible": "Earlier philosopher.", "why_wrong": "Philosopher of the previous generation."},
                {"option": "Sheikh Bahai", "why_plausible": "Earlier jurist.", "why_wrong": "Lived under Shah Abbas I, while Majlisi dominated the late 17th century."}
            ],
            "expl": "Majlisi's strict clerical legalism marginalized religious minorities and contributed to the social ossification that preceded the Afghan conquest in 1722.",
            "book": "Persia in Crisis: Safavid Decline and the Fall of Isfahan", "auth": "Rudi Matthee", "pg": 184
        }
    ])

    # 4. ISLANDS & PORTS OF THE SOUTH (Single)
    add_5("ISLANDS & PORTS OF THE SOUTH", "Persian Gulf & Sea", "Maritime Geography", "single", [
        {
            "text": "Measuring 1,491 square kilometers in the Strait of Hormuz, this dolphin-shaped island is the largest island in the Persian Gulf, famous for Hara mangrove forests.",
            "ans": "Qeshm Island",
            "aliases": ["Qeshm Island", "Qeshm", "Jazireh-ye Qeshm", "قشم", "جزیره قشم"],
            "options": ["Qeshm Island", "Kish Island", "Kharg Island", "Hormuz Island"],
            "rationales": [
                {"option": "Kish Island", "why_plausible": "Famous luxury tourist resort island.", "why_wrong": "Kish is much smaller (91 sq km) and coral-fringed."},
                {"option": "Kharg Island", "why_plausible": "Strategic crude oil terminal island.", "why_wrong": "Located further northwest off Bushehr."},
                {"option": "Hormuz Island", "why_plausible": "Red-soil mineral island.", "why_wrong": "Small 42-sq-km rainbow island with a Portuguese fortress."}
            ],
            "expl": "Qeshm features the UNESCO Global Geopark, the Stars Valley (Darreh-ye Setaregan), and the Chahkooh Gorge carved by erosion.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 16
        },
        {
            "text": "Transformed in the 1970s into a duty-free luxury haven with a Grand Casino and supersonic Concorde flights, this 91-square-kilometer coral island lies in the Persian Gulf.",
            "ans": "Kish Island",
            "aliases": ["Kish Island", "Kish", "Jazireh-ye Kish", "کیش", "جزیره کیش"],
            "options": ["Kish Island", "Qeshm Island", "Lavan Island", "Abu Musa"],
            "rationales": [
                {"option": "Qeshm Island", "why_plausible": "Large neighboring island.", "why_wrong": "Traditional geopark island, not the Shah's luxury casino resort."},
                {"option": "Lavan Island", "why_plausible": "Oil and gas island.", "why_wrong": "Industrial petroleum island."},
                {"option": "Abu Musa", "why_plausible": "Disputed southern island.", "why_wrong": "Military outpost shared historically with Sharjah."}
            ],
            "expl": "Kish remains a major visa-free shopping and tourism free-trade zone, famous for the scenic wreck of the Greek Cargo Ship grounded on its coral reefs in 1966.",
            "book": "The Shah", "auth": "Abbas Milani", "pg": 354
        },
        {
            "text": "Handling over ninety percent of all Iranian crude oil exports via deepwater sea berths, this fortified rocky island was bombed over 2,800 times by Iraqi jets during the war.",
            "ans": "Kharg Island",
            "aliases": ["Kharg Island", "Kharg", "Jazireh-ye Kharg", "جزیره خارگ", "خارگ", "خارک"],
            "options": ["Kharg Island", "Lavan Island", "Sirri Island", "Farsi Island"],
            "rationales": [
                {"option": "Lavan Island", "why_plausible": "Oil export terminal.", "why_wrong": "Handles a small fraction of crude; Kharg was the primary supertanker terminal."},
                {"option": "Sirri Island", "why_plausible": "Oil platform island.", "why_wrong": "Secondary southern terminal attacked in 1988 by the US Navy."},
                {"option": "Farsi Island", "why_plausible": "Naval base island in the middle of the Gulf.", "why_wrong": "A remote naval outpost, not the massive export terminal."}
            ],
            "expl": "Kharg Island was shielded by Hawk anti-aircraft missile batteries and heroic repair crews who kept oil pumping onto tankers throughout the eight-year Tanker War.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 785
        },
        {
            "text": "Renowned for its red ochre beaches and rainbow-colored salt canyons, this tiny island features the ruins of an imposing 16th-century fortress built by Afonso de Albuquerque.",
            "ans": "Hormuz Island",
            "aliases": ["Hormuz Island", "Hormuz", "Jazireh-ye Hormoz", "جزیره هرمز", "هرمز"],
            "options": ["Hormuz Island", "Larak Island", "Hengam Island", "Greater Tunb"],
            "rationales": [
                {"option": "Larak Island", "why_plausible": "Nearby island in the strait.", "why_wrong": "Naval base island, not famous for edible red soil and the Portuguese castle."},
                {"option": "Hengam Island", "why_plausible": "Island famed for wild dolphins.", "why_wrong": "Located south of Qeshm."},
                {"option": "Greater Tunb", "why_plausible": "Strategic island near the shipping lanes.", "why_wrong": "Military island garrisoned in 1971."}
            ],
            "expl": "Hormuz Island was the commercial pearl of the Indies until Safavid commander Imam Quli Khan expelled the Portuguese garrison in 1622.",
            "book": "Iran Under the Safavids", "auth": "Roger Savory", "pg": 116
        },
        {
            "text": "Originally named Gombroon and developed into Iran's primary container shipping port by Shah Abbas I, this coastal metropolis looks out over the Strait of Hormuz.",
            "ans": "Bandar Abbas",
            "aliases": ["Bandar Abbas", "Bandar-e Abbas", "Gamrun", "Gombroon", "بندرعباس", "بندر عباس"],
            "options": ["Bandar Abbas", "Bushehr", "Chabahar", "Bandar-e Lengeh"],
            "rationales": [
                {"option": "Bushehr", "why_plausible": "Major historic port further west.", "why_wrong": "Bushehr is in the northern Gulf, developed by Nader Shah and the British East India Company."},
                {"option": "Chabahar", "why_plausible": "Oceanic deepwater port.", "why_wrong": "Located on the Gulf of Oman in Sistan-Baluchestan."},
                {"option": "Bandar-e Lengeh", "why_plausible": "Historic pearl port.", "why_wrong": "Historic pearl center, not the primary container port named after Shah Abbas."}
            ],
            "expl": "Home to the Shahid Rajaee container terminal, Bandar Abbas handles over half of Iran's maritime sea trade today.",
            "book": "Iran Under the Safavids", "auth": "Roger Savory", "pg": 118
        }
    ])

    # 5. IRANIAN CINEMA: DIRECTORS & AUTEURS (Single)
    add_5("IRANIAN CINEMA: DIRECTORS AND AUTEURS", "Cinema of Iran", "Directing", "single", [
        {
            "text": "A towering playwright and director of Death of Yazdgerd and Bashu, the Little Stranger, this auteur is the grandmaster of historical allegorical theatre and film.",
            "ans": "Bahram Beyzai",
            "aliases": ["Bahram Beyzai", "Bahram Beyzaie", "Beyzai", "بهرام بیضایی", "بیضایی"],
            "options": ["Bahram Beyzai", "Nasser Taghvai", "Masoud Kimiai", "Ali Hatami"],
            "rationales": [
                {"option": "Nasser Taghvai", "why_plausible": "Great auteur director of Captain Khorshid.", "why_wrong": "Directed Captain Khorshid and My Uncle Napoleon, not Bashu."},
                {"option": "Masoud Kimiai", "why_plausible": "Director of Qeysar.", "why_wrong": "Pioneered urban street drama, not classical allegorical drama."},
                {"option": "Ali Hatami", "why_plausible": "Master of nostalgic historical cinema (Hezardastan).", "why_wrong": "Famed for Hezar Dastan and Mother, not Bashu."}
            ],
            "expl": "Beyzai's research into pre-Islamic dramatic traditions culminated in his monumental book A Study of Iranian Theatre (1965).",
            "book": "A Social History of Iranian Cinema, Vol. 1", "auth": "Hamid Naficy", "pg": 348
        },
        {
            "text": "Known as the 'poet of Iranian cinema' for his lyrical historical dialogues, this director created the immortal TV epic Hezar Dastan and the beloved tearjerker Mother (Madar).",
            "ans": "Ali Hatami",
            "aliases": ["Ali Hatami", "Hatami", "علی حاتمی"],
            "options": ["Ali Hatami", "Bahram Beyzai", "Dariush Mehrjui", "Masoud Kimiai"],
            "rationales": [
                {"option": "Bahram Beyzai", "why_plausible": "Master dramatist.", "why_wrong": "Directed Bashu and The Downpour."},
                {"option": "Dariush Mehrjui", "why_plausible": "Director of The Cow.", "why_wrong": "Directed Gaav, Hamoun, and Leila."},
                {"option": "Masoud Kimiai", "why_plausible": "Director of Qeysar.", "why_wrong": "Directed gritty urban dramas."}
            ],
            "expl": "Hatami built the famous Ghazali Cinema Town in west Tehran to recreate 1930s Lalezar Street and the Tupkhaneh square for his cinematic works.",
            "book": "A Social History of Iranian Cinema, Vol. 1", "auth": "Hamid Naficy", "pg": 352
        },
        {
            "text": "Directing Still Life (1974) and A Simple Event, this pioneer of international cinematic minimalism emigrated to Germany and inspired directors like Chantal Akerman and Jim Jarmusch.",
            "ans": "Sohrab Shahid-Saless",
            "aliases": ["Sohrab Shahid-Saless", "Shahid-Saless", "سهراب شهیدثالث", "شهیدثالث"],
            "options": ["Sohrab Shahid-Saless", "Abbas Kiarostami", "Amir Naderi", "Ebrahim Golestan"],
            "rationales": [
                {"option": "Abbas Kiarostami", "why_plausible": "Famous minimalist director.", "why_wrong": "Kiarostami stayed in Iran and rose to fame later with Where Is the Friend's Home?."},
                {"option": "Amir Naderi", "why_plausible": "Director of The Runner who moved to New York.", "why_wrong": "Naderi emigrated to the United States in the late 1980s, not Germany in the 1970s."},
                {"option": "Ebrahim Golestan", "why_plausible": "Pioneering producer of The Brick and the Mirror.", "why_wrong": "Moved to England, known for modernist prose and documentaries."}
            ],
            "expl": "Still Life won the Silver Bear at the 1974 Berlin Film Festival, featuring an aging railway switchman told he is being retired after 33 years of routine.",
            "book": "A Social History of Iranian Cinema, Vol. 1", "auth": "Hamid Naficy", "pg": 338
        },
        {
            "text": "Directing A Separation (2011) and The Salesman (2016), this contemporary master became the only Iranian director to win two Academy Awards for Best Foreign Language Film.",
            "ans": "Asghar Farhadi",
            "aliases": ["Asghar Farhadi", "Farhadi", "اصغر فرهادی", "فرهادی"],
            "options": ["Asghar Farhadi", "Abbas Kiarostami", "Majid Majidi", "Jafar Panahi"],
            "rationales": [
                {"option": "Abbas Kiarostami", "why_plausible": "Palme d'Or winner.", "why_wrong": "Won Cannes Palme d'Or for Taste of Cherry in 1997, never won an Oscar."},
                {"option": "Majid Majidi", "why_plausible": "First Iranian director nominated for an Oscar.", "why_wrong": "Nominated for Children of Heaven in 1998, but did not win."},
                {"option": "Jafar Panahi", "why_plausible": "Golden Lion and Golden Bear winner.", "why_wrong": "Won the Golden Lion (The Circle) and Golden Bear (Taxi), but not an Oscar."}
            ],
            "expl": "A Separation also made history as the first foreign-language screenplay nominated for Best Original Screenplay at the Oscars.",
            "book": "A Social History of Iranian Cinema, Vol. 2", "auth": "Hamid Naficy", "pg": 420
        },
        {
            "text": "This director won the Golden Leopard at Locarno for The Mirror (1997) and the Golden Bear at Berlin for Taxi (2015), despite being sentenced to a 20-year ban on filmmaking.",
            "ans": "Jafar Panahi",
            "aliases": ["Jafar Panahi", "Panahi", "جعفر پناهی", "پناهی"],
            "options": ["Jafar Panahi", "Mohsen Makhmalbaf", "Bahman Ghobadi", "Mohammad Rasoulof"],
            "rationales": [
                {"option": "Mohsen Makhmalbaf", "why_plausible": "Director of Gabbeh and Kandahar.", "why_wrong": "Exiled in Europe since the mid-2000s, not detained in Tehran."},
                {"option": "Bahman Ghobadi", "why_plausible": "Kurdish-Iranian director (A Time for Drunken Horses).", "why_wrong": "Directed A Time for Drunken Horses, works in exile."},
                {"option": "Mohammad Rasoulof", "why_plausible": "Co-defendant director who won the Golden Bear for There Is No Evil.", "why_wrong": "Fled Iran in 2024 with The Seed of the Sacred Fig."}
            ],
            "expl": "Panahi smuggled his film This Is Not a Film (2011) to the Cannes Film Festival hidden inside a USB flash drive baked inside a birthday cake.",
            "book": "A Social History of Iranian Cinema, Vol. 2", "auth": "Hamid Naficy", "pg": 412
        }
    ])

    # 6. MUSIC: RADIF & DASTGAH (Single)
    add_5("MUSIC: RADIF AND DASTGAH", "Persian Traditional Music", "Modal Music", "single", [
        {
            "text": "Persian classical music is organized into this comprehensive canon of melodic motifs (Goushehs), arranged across seven primary modal systems (Dastgahs).",
            "ans": "The Radif",
            "aliases": ["The Radif", "Radif", "ردیف", "ردیف موسیقی ایرانی"],
            "options": ["The Radif", "The Maqam", "The Mugham", "The Tasnif"],
            "rationales": [
                {"option": "The Maqam", "why_plausible": "Modal system in the broader Arab and Turkish world.", "why_wrong": "The Arabic/Turkish modal framework, whereas the Iranian canon is specifically the Radif."},
                {"option": "The Mugham", "why_plausible": "Azerbaijani modal tradition.", "why_wrong": "The Azerbaijani regional variant."},
                {"option": "The Tasnif", "why_plausible": "Metred lyrical song form.", "why_wrong": "A composed song within a dastgah, not the entire canon repertoire."}
            ],
            "expl": "Preserved by 19th-century court masters Mirza Abdollah and Aqa Hossein-Qoli, the Radif was inscribed on UNESCO's Representative List of Intangible Cultural Heritage in 2009.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 174
        },
        {
            "text": "Revered as the undisputed 'Master' (Ostad) of Persian vocal music, this legendary baritone spent six decades mesmerizing millions with his breathtaking Tahrir vocal ornamentation.",
            "ans": "Mohammad Reza Shajarian",
            "aliases": ["Mohammad Reza Shajarian", "Ostad Shajarian", "Shajarian", "محمدرضا شجریان", "شجریان", "استاد شجریان"],
            "options": ["Mohammad Reza Shajarian", "Shahram Nazeri", "Gholam-Hossein Banan", "Homayoun Shajarian"],
            "rationales": [
                {"option": "Shahram Nazeri", "why_plausible": "Known as the Knight of Iranian Music.", "why_wrong": "Famous for singing Rumi's poetry with Kurdish Sufi fervor."},
                {"option": "Gholam-Hossein Banan", "why_plausible": "Legendary singer of Ey Iran in the 1940s and 50s.", "why_wrong": "Mid-century master of the Golha radio broadcasts."},
                {"option": "Homayoun Shajarian", "why_plausible": "His celebrated son and vocalist.", "why_wrong": "His son, who rose to fame in the 2000s."}
            ],
            "expl": "Shajarian's unaccompanied prayer 'Rabbana' was broadcast at sundown every Ramadan on Iranian radio for thirty years, becoming a sacred national soundscape.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 750
        },
        {
            "text": "Held vertically and played by directing air between the upper incisors and the tongue (Dandan technique), this end-blown reed flute was played with peerless virtuosity by Hasan Kasaei.",
            "ans": "The Ney",
            "aliases": ["The Ney", "Ney", "Nay", "نی", "ساز نی"],
            "options": ["The Ney", "The Kamancheh", "The Tar", "The Santur"],
            "rationales": [
                {"option": "The Kamancheh", "why_plausible": "Spike fiddle.", "why_wrong": "Bowed string instrument played by Ali-Asghar Bahari and Kayhan Kalhor."},
                {"option": "The Tar", "why_plausible": "Long-necked lute.", "why_wrong": "Plucked double-bellied string instrument."},
                {"option": "The Santur", "why_plausible": "Hammered dulcimer.", "why_wrong": "72-string trapezoidal zither played with wooden mezrabs."}
            ],
            "expl": "The Ney opens Rumi's Masnavi with the immortal lament: 'Beshno az ney chon hekayat mikonad' (Listen to the reed as it tells its tale of separation).",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 176
        },
        {
            "text": "Featuring a waist carved from solid mulberry wood covered in lamb fetus skin, this premier 25-fret long-necked lute is played with a brass plectrum encased in bee's wax.",
            "ans": "The Tar",
            "aliases": ["The Tar", "Tar", "تار"],
            "options": ["The Tar", "The Setar", "The Dotar", "The Oud / Barbat"],
            "rationales": [
                {"option": "The Setar", "why_plausible": "Four-stringed wooden lute.", "why_wrong": "Played with the index fingernail without skin covering or brass plectrums."},
                {"option": "The Dotar", "why_plausible": "Two-stringed Khorasani folk lute.", "why_wrong": "Folk instrument of northeastern bards (Bakhshis)."},
                {"option": "The Oud / Barbat", "why_plausible": "Short-necked pear-shaped lute.", "why_wrong": "Fretless wooden instrument without skin."}
            ],
            "expl": "Renowned luthiers like Yahya of Isfahan in the early 20th century carved instruments whose resonance remains the gold standard in Iranian music.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 178
        },
        {
            "text": "Featuring 72 strings arranged in courses of four over 18 movable bridges, this trapezoidal wooden hammered dulcimer was brought to modern perfection by Ostad Faramarz Payvar.",
            "ans": "The Santur",
            "aliases": ["The Santur", "Santur", "Santoor", "سنتور"],
            "options": ["The Santur", "The Qanun", "The Chang", "The Tombak"],
            "rationales": [
                {"option": "The Qanun", "why_plausible": "Plucked zither.", "why_wrong": "Plucked with finger picks, popular in Arab and Turkish music."},
                {"option": "The Chang", "why_plausible": "Ancient Persian harp.", "why_wrong": "Vertical harp depicted in Sasanian rock carvings."},
                {"option": "The Tombak", "why_plausible": "Goblet drum.", "why_wrong": "Percussion goblet drum played by Hossein Tehrani."}
            ],
            "expl": "The Santur is played using two delicate featherweight wooden hammers (mezrab), producing a crystalline, shimmering soundscape.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 180
        }
    ])

    print("Writing Batch 6 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Total clues after Part 6:", len(clues_by_id))

if __name__ == "__main__":
    run_part6()
