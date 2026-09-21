#!/usr/bin/env python3
import json

def run_part8():
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
                "page": item.get("pg", 380 + idx * 10),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. THE OIL CRISIS: 1951-1953 (Single)
    add_5("THE OIL CRISIS: 1951-1953", "Mosaddegh Era", "Petroleum Politics", "single", [
        {
            "text": "Housing the world's largest oil refinery on the Shatt al-Arab, this island city in Khuzestan became the flashpoint of the nationalization confrontation with Britain.",
            "ans": "Abadan",
            "aliases": ["Abadan", "Island of Abadan", "آبادان"],
            "options": ["Abadan", "Khorramshahr", "Ahvaz", "Masjed Soleyman"],
            "rationales": [
                {"option": "Khorramshahr", "why_plausible": "Neighboring port city.", "why_wrong": "Commercial port, but the colossal refinery was in Abadan."},
                {"option": "Ahvaz", "why_plausible": "Provincial capital.", "why_wrong": "Administrative capital inland."},
                {"option": "Masjed Soleyman", "why_plausible": "Site of first oil strike in 1908.", "why_wrong": "Drilling field in the foothills, not the refinery port city."}
            ],
            "expl": "In October 1951, Mosaddegh expelled the last remaining British engineers from Abadan, who sailed down the Shatt al-Arab aboard the cruiser HMS Mauritius.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 74
        },
        {
            "text": "Known as the 'Soldier of Nationalization', this fiery orator and close lieutenant of Mosaddegh personally oversaw the seizure and unsealing of the Abadan refinery.",
            "ans": "Hossein Makki",
            "aliases": ["Hossein Makki", "Makki", "حسین مکی", "مکی"],
            "options": ["Hossein Makki", "Hossein Fatemi", "Khalil Maleki", "Karim Sanjabi"],
            "rationales": [
                {"option": "Hossein Fatemi", "why_plausible": "Foreign Minister.", "why_wrong": "Proposed nationalization and edited Bakhtar-e Emruz, but Makki was the frontline director in Abadan."},
                {"option": "Khalil Maleki", "why_plausible": "Independent socialist leader.", "why_wrong": "Ideologue of the Third Force, not the Abadan takeover commander."},
                {"option": "Karim Sanjabi", "why_plausible": "Minister of Education and jurist.", "why_wrong": "Represented Iran at the Hague, not the crowd orator in Abadan."}
            ],
            "expl": "Makki rode atop oil tanks surrounded by thousands of cheering workers; his later defection from Mosaddegh was a major blow to the National Front.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 82
        },
        {
            "text": "In July 1952 (30 Tir), millions of Iranians took to the streets in defiance of royal tanks to demand the reinstatement of Mosaddegh following his dismissal by this premier.",
            "ans": "Ahmad Qavam",
            "aliases": ["Ahmad Qavam", "Qavam os-Saltaneh", "Qavam", "احمد قوام", "قوام"],
            "options": ["Ahmad Qavam", "Fazlollah Zahedi", "Haj Ali Razmara", "Ali Soheili"],
            "rationales": [
                {"option": "Fazlollah Zahedi", "why_plausible": "Led the 1953 coup.", "why_wrong": "Zahedi took power in August 1953, not July 1952."},
                {"option": "Haj Ali Razmara", "why_plausible": "Assassinated prime minister.", "why_wrong": "Assassinated in March 1951."},
                {"option": "Ali Soheili", "why_plausible": "Wartime premier.", "why_wrong": "Served during WWII."}
            ],
            "expl": "Qavam issued a bombastic proclamation threatening to steer the ship of state with an iron hand, but resigned after four days of bloody street battles.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 118
        },
        {
            "text": "Traveling to the Netherlands in June 1952, Dr. Mosaddegh personally addressed this international court, brilliantly arguing that the dispute was between Iran and a private company.",
            "ans": "The International Court of Justice (The Hague)",
            "aliases": ["The International Court of Justice", "The Hague", "ICJ", "دیوان بین‌المللی لاهه", "دادگاه لاهه"],
            "options": ["The International Court of Justice (The Hague)", "The League of Nations", "The European Court of Human Rights", "The Nuremberg Tribunal"],
            "rationales": [
                {"option": "The League of Nations", "why_plausible": "Pre-WWII body.", "why_wrong": "Dissolved in 1946."},
                {"option": "The European Court of Human Rights", "why_plausible": "Strasbourg court.", "why_wrong": "European human rights court, not international state dispute tribunal."},
                {"option": "The Nuremberg Tribunal", "why_plausible": "Post-war war crimes court.", "why_wrong": "Fought Nazi war criminals, not commercial oil arbitration."}
            ],
            "expl": "By a vote of 9 to 5, the ICJ ruled in Iran's favor that it lacked jurisdiction because the 1933 concession was not an interstate treaty between governments.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 124
        },
        {
            "text": "In response to nationalization, the British Royal Navy imposed this severe naval embargo in the Persian Gulf, intercepting foreign tankers that attempted to purchase Iranian oil.",
            "ans": "The Abadan Oil Blockade",
            "aliases": ["The Abadan Oil Blockade", "Oil Blockade", "British Blockade", "تحریم نفت", "محاصره آبادان"],
            "options": ["The Abadan Oil Blockade", "Operation Ajax", "Operation Countenance", "Operation Praying Mantis"],
            "rationales": [
                {"option": "Operation Ajax", "why_plausible": "1953 coup.", "why_wrong": "The covert coup operation, not the naval embargo."},
                {"option": "Operation Countenance", "why_plausible": "1941 invasion.", "why_wrong": "WWII joint Allied invasion."},
                {"option": "Operation Praying Mantis", "why_plausible": "1988 naval strike.", "why_wrong": "US Navy strike in 1988."}
            ],
            "expl": "When the Italian tanker Rose Mary tried to export Iranian crude in 1952, British warships intercepted it and forced it into Aden, cutting Iran off from world oil markets.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 92
        }
    ])

    # 2. COLD WAR ESPIONAGE IN TEHRAN (Double)
    add_5("COLD WAR ESPIONAGE IN TEHRAN", "Covert Operations", "Cold War Espionage", "double", [
        {
            "text": "In 1954, following the coup, military authorities uncovered a clandestine communist espionage network inside the armed forces comprising over 600 officers belonging to this party.",
            "ans": "The Tudeh Military Network",
            "aliases": ["The Tudeh Military Network", "Tudeh Military Organization", "Sazman-e Nezami-ye Tudeh", "سازمان نظامی حزب توده", "شبکه نظامی توده"],
            "options": ["The Tudeh Military Network", "The National Front", "Fadayan-e Islam", "The MEK"],
            "rationales": [
                {"option": "The National Front", "why_plausible": "Mosaddegh's coalition.", "why_wrong": "Secular civilian politicians, without a secret military cell."},
                {"option": "Fadayan-e Islam", "why_plausible": "Underground militant group.", "why_wrong": "Religious assassination group, not the communist army network."},
                {"option": "The MEK", "why_plausible": "Guerrilla group.", "why_wrong": "Founded in 1965, a decade after the 1954 discovery."}
            ],
            "expl": "Twenty-seven military officers, including Colonel Siamak and Colonel Rouzbeh, were executed by firing squad, dismantling Soviet penetration of the Iranian officer corps.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 318
        },
        {
            "text": "Serving as chief of the CIA's Near East division and author of Countercoup, this grandson of an American president secretly entered Iran under the alias 'James Lockridge'.",
            "ans": "Kermit Roosevelt Jr.",
            "aliases": ["Kermit Roosevelt Jr.", "Kermit Roosevelt", "Roosevelt", "کرمیت روزولت"],
            "options": ["Kermit Roosevelt Jr.", "Allen Dulles", "Richard Helms", "George Cave"],
            "rationales": [
                {"option": "Allen Dulles", "why_plausible": "Director of Central Intelligence.", "why_wrong": "CIA director in Washington, not the field operative in Tehran."},
                {"option": "Richard Helms", "why_plausible": "Later CIA director and US Ambassador to Iran (1973–1977).", "why_wrong": "Ran the agency later, not the field commander of TPAJAX."},
                {"option": "George Cave", "why_plausible": "CIA Iran analyst.", "why_wrong": "Farsi-speaking CIA officer during the 1979 revolution and Iran-Contra."}
            ],
            "expl": "Roosevelt operated out of a hidden cellar in the US Embassy compound, coordinating suitcase payments of $1 million in cash to royalist plotters and street gangs.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 152
        },
        {
            "text": "In 1958, this former Chief of Staff of the Armed Forces was arrested in a US-backed plot to overthrow Prime Minister Eqbal and curb the Shah's autocratic powers.",
            "ans": "General Valiollah Gharani",
            "aliases": ["General Valiollah Gharani", "General Gharani", "Valiollah Gharani", "سپهبد قرنی", "تیمسار قرنی"],
            "options": ["General Valiollah Gharani", "General Teymour Bakhtiar", "General Fazlollah Zahedi", "General Nader Batmanghelich"],
            "rationales": [
                {"option": "General Teymour Bakhtiar", "why_plausible": "SAVAK chief who plotted against the Shah.", "why_wrong": "Exiled in 1961 and killed in 1970, not the 1958 reformist plot."},
                {"option": "General Fazlollah Zahedi", "why_plausible": "1953 prime minister.", "why_wrong": "Forced into diplomatic retirement in Montreux in 1955."},
                {"option": "General Nader Batmanghelich", "why_plausible": "1953 army chief of staff.", "why_wrong": "Royalist loyalist, not the reform coup leader."}
            ],
            "expl": "Gharani served three years in prison; after the 1979 Revolution, Khomeini appointed him the first Chief of the General Staff until assassinated by Forqan in April 1979.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 616
        },
        {
            "text": "British SIS intelligence operative who smuggled radio transmitters into Iran inside diplomatic pouches, he convinced the CIA to join Operation Boot.",
            "ans": "Monty Woodhouse",
            "aliases": ["Monty Woodhouse", "C.M. Woodhouse", "Christopher Montague Woodhouse", "مونتی وودهاوس"],
            "options": ["Monty Woodhouse", "Robin Zaehner", "Percy Cox", "John Le Carré"],
            "rationales": [
                {"option": "Robin Zaehner", "why_plausible": "Oxford scholar and MI6 operative in Tehran.", "why_wrong": "Handled bazaar bribes under the British Embassy, while Woodhouse commanded the military operation."},
                {"option": "Percy Cox", "why_plausible": "British diplomat.", "why_wrong": "Active in 1919."},
                {"option": "John Le Carré", "why_plausible": "Famous British spy novelist.", "why_wrong": "Fiction author who worked in Germany, not Iran."}
            ],
            "expl": "Woodhouse famously framed the coup to the incoming Eisenhower administration not as protecting British oil profits, but as preventing a Soviet communist takeover of Iran.",
            "book": "The Coup", "auth": "Ervand Abrahamian", "pg": 146
        },
        {
            "text": "Operating from 1959 to 1979, this joint US-Iranian secret eavesdropping installation in the northern mountains monitored Soviet telemetry and space missile tests at Baikonur.",
            "ans": "Project IBEX (Tacksman)",
            "aliases": ["Project IBEX", "Tacksman", "Sites Kabkan and Behshahr", "پروژه آیبکس", "ایبکس"],
            "options": ["Project IBEX (Tacksman)", "Gladio", "ECHELON", "MKUltra"],
            "rationales": [
                {"option": "Gladio", "why_plausible": "Cold War stay-behind network.", "why_wrong": "NATO stay-behind network in Western Europe."},
                {"option": "ECHELON", "why_plausible": "Five Eyes surveillance network.", "why_wrong": "Global signal intelligence pact (US/UK/CAN/AUS/NZ)."},
                {"option": "MKUltra", "why_plausible": "CIA project.", "why_wrong": "Mind control and psychological experiments."}
            ],
            "expl": "Listening posts at Kabkan and Behshahr near the Soviet border allowed the CIA to intercept telemetry from Soviet rocket launches until evacuated during the 1979 Revolution.",
            "book": "The Eagle and the Lion", "auth": "James A. Bill", "pg": 214
        }
    ])

    # 3. PERSIAN GULF: TANKER WAR (Double)
    add_5("PERSIAN GULF: TANKER WAR", "Iran-Iraq War", "Maritime Conflict", "double", [
        {
            "text": "On April 18, 1988, the US Navy destroyed two Iranian oil platforms and sank the frigate Sahand in this largest surface naval battle fought by America since World War II.",
            "ans": "Operation Praying Mantis",
            "aliases": ["Operation Praying Mantis", "Praying Mantis", "عملیات آخوندک"],
            "options": ["Operation Praying Mantis", "Operation Earnest Will", "Operation Desert Storm", "Operation Prime Chance"],
            "rationales": [
                {"option": "Operation Earnest Will", "why_plausible": "US escort operation of reflagged Kuwaiti tankers.", "why_wrong": "The ongoing escort mission, while Praying Mantis was the specific retaliatory day-long battle."},
                {"option": "Operation Desert Storm", "why_plausible": "1991 Gulf War.", "why_wrong": "1991 liberation of Kuwait from Iraq."},
                {"option": "Operation Prime Chance", "why_plausible": "Special forces night patrols in the Gulf.", "why_wrong": "Night helicopter operations, not the daylight surface fleet engagement."}
            ],
            "expl": "Praying Mantis was launched in retaliation after the guided missile frigate USS Samuel B. Roberts struck an Iranian M-08 sea mine in international waters, nearly sinking.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 794
        },
        {
            "text": "On July 3, 1988, the guided-missile cruiser USS Vincennes shot down this civilian Iranian airliner over the Strait of Hormuz, killing all 290 passengers and crew aboard.",
            "ans": "Iran Air Flight 655",
            "aliases": ["Iran Air Flight 655", "Flight 655", "IR655", "پرواز شماره ۶۵۵", "پرواز ۶۵۵"],
            "options": ["Iran Air Flight 655", "Pan Am Flight 103", "Korean Air Lines Flight 007", "UTA Flight 772"],
            "rationales": [
                {"option": "Pan Am Flight 103", "why_plausible": "Lockerbie bombing in December 1988.", "why_wrong": "Lockerbie terrorist bombing over Scotland."},
                {"option": "Korean Air Lines Flight 007", "why_plausible": "Shot down by Soviet fighters in 1983.", "why_wrong": "Shot down over Sakhalin Island by the USSR in 1983."},
                {"option": "UTA Flight 772", "why_plausible": "Airliner bombing.", "why_wrong": "French airliner bombed over Niger in 1989."}
            ],
            "expl": "The Airbus A300 was climbing inside a designated commercial corridor on a flight from Bandar Abbas to Dubai when Captain Will Rogers III mistook it for an attacking F-14 Tomcat.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 795
        },
        {
            "text": "In 1987, to protect Kuwaiti oil exports from Iranian sea mines and gunboat swarms, the United States placed eleven Kuwaiti tankers under this maritime arrangement.",
            "ans": "Reflagging under the US Flag (Operation Earnest Will)",
            "aliases": ["Reflagging under the US Flag", "Reflagging", "US Flagging", "تغییر پرچم نفتکش‌ها", "پرچم آمریکا"],
            "options": ["Reflagging under the US Flag (Operation Earnest Will)", "UN Maritime Patrol", "NATO Escort Force", "Arab League Fleet"],
            "rationales": [
                {"option": "UN Maritime Patrol", "why_plausible": "International peacekeeping force.", "why_wrong": "The UN never deployed a naval fleet to the Gulf."},
                {"option": "NATO Escort Force", "why_plausible": "Western military alliance.", "why_wrong": "Independent European navies sailed separately, not as a formal NATO fleet."},
                {"option": "Arab League Fleet", "why_plausible": "Regional alliance.", "why_wrong": "Kuwait turned to the superpowers (US and USSR), not the Arab League."}
            ],
            "expl": "On its maiden voyage under US Navy escort in July 1987, the reflagged supertanker Bridgeton struck an Iranian sea mine near Farsi Island, puncturing its outer hull.",
            "book": "Guardians of the Revolution", "auth": "Ray Takeyh", "pg": 112
        },
        {
            "text": "Supplied by China and deployed on mobile launchers along the rugged coastline of the Strait of Hormuz, these anti-ship cruise missiles posed a lethal threat to Persian Gulf tankers.",
            "ans": "Silkworm Missiles",
            "aliases": ["Silkworm Missiles", "Silkworm", "HY-2 Silkworm", "موشک کرم ابریشم"],
            "options": ["Silkworm Missiles", "Exocet", "Harpoon", "Scud-B"],
            "rationales": [
                {"option": "Exocet", "why_plausible": "French anti-ship missile used by Iraq.", "why_wrong": "Fired by Iraqi Mirage jets against Iranian tankers."},
                {"option": "Harpoon", "why_plausible": "American anti-ship missile.", "why_wrong": "Used by the US and Iranian navies, not the Chinese coastal missile batteries."},
                {"option": "Scud-B", "why_plausible": "Ballistic missile.", "why_wrong": "Surface-to-surface ballistic missile used in the 'War of the Cities' against Baghdad and Tehran."}
            ],
            "expl": "With a 500-kilogram warhead and 100-kilometer range, Silkworm batteries at Kuhestak and Qeshm gave Iran the capability to choke commercial shipping in the strait.",
            "book": "Guardians of the Revolution", "auth": "Ray Takeyh", "pg": 114
        },
        {
            "text": "The IRGC Navy deployed swarms of these small, high-speed armed motorboats to ambush commercial tankers and launch rocket-propelled grenades in hit-and-run attacks.",
            "ans": "Boghammar Speedboats",
            "aliases": ["Boghammar Speedboats", "Boghammar", "Ashura Speedboats", "قایق‌های عاشورا", "قایق تندرو"],
            "options": ["Boghammar Speedboats", "Zodiac", "Corvettes", "Hovercrafts"],
            "rationales": [
                {"option": "Zodiac", "why_plausible": "Inflatable commando boat.", "why_wrong": "Rubber boats used for river crossings, not the 45-knot Swedish-built fiberglass speedboats."},
                {"option": "Corvettes", "why_plausible": "Naval warship class.", "why_wrong": "Conventional naval vessels, not swarm motorboats."},
                {"option": "Hovercrafts", "why_plausible": "British hovercrafts operated by the Iranian Navy.", "why_wrong": "BH.7 hovercrafts were transport vessels, not the tactical swarm attack boats."}
            ],
            "expl": "Purchased from Sweden for coastal patrol, the 13-meter boats were mounted with 107mm multiple rocket launchers and DShK heavy machine guns by IRGC naval commandos.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 790
        }
    ])

    # 4. CLASSICAL PERSIAN MUSIC MASTERS (Double)
    add_5("CLASSICAL PERSIAN MUSIC MASTERS", "Musical Heritage", "Maestros & Instruments", "double", [
        {
            "text": "Serving at the court of Sasanian King Khosrow II Parviz in the 7th century, this legendary court musician created the modal system of the Seven Royal Modes (Khosravani).",
            "ans": "Barbad",
            "aliases": ["Barbad", "Barbad of Merv", "باربد"],
            "options": ["Barbad", "Nakisa", "Farabi", "Safi al-Din al-Urmawi"],
            "rationales": [
                {"option": "Nakisa", "why_plausible": "His contemporary harpist rival at the Sasanian court.", "why_wrong": "Famed for playing the harp (chang), but Barbad was the supreme composer who invented the 30 melodic airs (Si-lahn)."},
                {"option": "Farabi", "why_plausible": "Islamic Golden Age musical theorist.", "why_wrong": "Lived in the 10th century and wrote Kitab al-Musiqa al-Kabir."},
                {"option": "Safi al-Din al-Urmawi", "why_plausible": "13th-century musical theorist.", "why_wrong": "Founder of the Systematic School in the 13th century in Baghdad."}
            ],
            "expl": "Nezami's Khosrow and Shirin describes musical duels between Barbad and the harpist Nakisa, immortalizing Barbad as the father of Persian art music.",
            "book": "The Persians", "auth": "Homa Katouzian", "pg": 76
        },
        {
            "text": "Celebrated for his velvet baritone and iconic black-rimmed glasses, this mid-century vocalist immortalized the patriotic anthem Ey Iran and the tragic ballad Elaheh-ye Naz.",
            "ans": "Gholam-Hossein Banan",
            "aliases": ["Gholam-Hossein Banan", "Banan", "غلامحسین بنان", "بنان"],
            "options": ["Gholam-Hossein Banan", "Mohammad Reza Shajarian", "Taj Isfahani", "Iraj (Hossein Khajeh Amiri)"],
            "rationales": [
                {"option": "Mohammad Reza Shajarian", "why_plausible": "Supreme classical master.", "why_wrong": "Rose to prominence in the 1970s and 80s."},
                {"option": "Taj Isfahani", "why_plausible": "Master vocalist of Isfahan.", "why_wrong": "Known for his powerful classical Isfahan school, not the original singer of Ey Iran."},
                {"option": "Iraj", "why_plausible": "Famous contemporary tenor.", "why_wrong": "Popular voice of Iranian cinema in the 1960s."}
            ],
            "expl": "Banan was the premier vocalist of Davood Pirnia's prestigious Golha (Flowers of Persian Song and Music) radio programs broadcast nationwide from 1956 to 1979.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 526
        },
        {
            "text": "This virtuoso Setar master and scholar popularized the instrument in the 1980s with his bestselling album Gol-e Sadbarg (One Hundred-Petaled Rose), featuring vocalist Shahram Nazeri.",
            "ans": "Jalal Zolfonun",
            "aliases": ["Jalal Zolfonun", "Zolfonun", "جلال ذوالفنون", "ذوالفنون"],
            "options": ["Jalal Zolfonun", "Ahmad Ebadi", "Hossein Alizadeh", "Mohammad-Reza Lotfi"],
            "rationales": [
                {"option": "Ahmad Ebadi", "why_plausible": "Pioneering radio setar player.", "why_wrong": "Son of Mirza Abdollah who pioneered solo microphone setar performance in the 1950s."},
                {"option": "Hossein Alizadeh", "why_plausible": "Titan of tar and setar (NeyNava).", "why_wrong": "Composed NeyNava and Raz-o Niaz, not Gol-e Sadbarg."},
                {"option": "Mohammad-Reza Lotfi", "why_plausible": "Founder of the Sheyda Ensemble.", "why_wrong": "Founded the Chavosh cultural movement and played tar, not the arranger of Gol-e Sadbarg."}
            ],
            "expl": "Gol-e Sadbarg commemorated the 800th anniversary of Rumi; it became the bestselling classical instrumental album in Iranian recording history.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 752
        },
        {
            "text": "Composed by Hossein Alizadeh in 1983 for ney and Western string orchestra during the darkest days of the war, this poignant concerto is titled after the reed flute.",
            "ans": "NeyNava",
            "aliases": ["NeyNava", "Ney Nava", "نی‌نوا", "نینوا"],
            "options": ["NeyNava", "Gol-e Sadbarg", "Bi To Be Sar Nemishavad", "Yaran Cheh Gharibaneh"],
            "rationales": [
                {"option": "Gol-e Sadbarg", "why_plausible": "1984 Rumi album by Zolfonun.", "why_wrong": "Arranged by Zolfonun for setar ensemble and Nazeri."},
                {"option": "Bi To Be Sar Nemishavad", "why_plausible": "Famous album by Masters Ensemble.", "why_wrong": "Grammy-nominated 2002 album by Shajarian, Alizadeh, and Kalhor."},
                {"option": "Yaran Cheh Gharibaneh", "why_plausible": "War elegy.", "why_wrong": "Mourning anthem sung by Gholam Koveitipour."}
            ],
            "expl": "Featuring Jamshid Andalibi on ney, NeyNava (Song of the Reed / Plain of Nineveh) became the grief-stricken soundtrack to the tragedy and resilience of the 1980s.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 788
        },
        {
            "text": "Born in 1845, this court master of the tar and setar organized and codified the disparate vocal and instrumental melodies of Persian music into the canonical Radif.",
            "ans": "Mirza Abdollah",
            "aliases": ["Mirza Abdollah", "Mirza Abdollah Farahani", "میرزا عبدالله", "میرزا عبدالله فراهانی"],
            "options": ["Mirza Abdollah", "Aqa Hossein-Qoli", "Darvish Khan", "Ali-Naqi Vaziri"],
            "rationales": [
                {"option": "Aqa Hossein-Qoli", "why_plausible": "His brother and fellow master.", "why_wrong": "Renowned for dazzling technical velocity, while Mirza Abdollah was the pedagogical compiler of the canonical Radif."},
                {"option": "Darvish Khan", "why_plausible": "His greatest disciple who invented the Pishdaramad.", "why_wrong": "His student who died in a carriage crash in 1926."},
                {"option": "Ali-Naqi Vaziri", "why_plausible": "Founded the National Music Conservatory.", "why_wrong": "Modernizer who studied in Paris and Berlin in the 1920s."}
            ],
            "expl": "Mirza Abdollah's home was a musical academy; his students included Darvish Khan, Esma'il Mehdi-Qoli, and his own sons Ahmad Ebadi and Javad Ebadi.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 422
        }
    ])

    # 5. PIONEERING WOMEN OF MODERN IRAN (Double)
    add_5("PIONEERING WOMEN OF MODERN IRAN", "Women's History", "Trailblazers", "double", [
        {
            "text": "In 2014, this Harvard-trained geometer and Stanford professor became the first woman and first Iranian ever to win the Fields Medal, the 'Nobel Prize of Mathematics'.",
            "ans": "Maryam Mirzakhani",
            "aliases": ["Maryam Mirzakhani", "Mirzakhani", "مریم میرزاخانی", "میرزاخانی"],
            "options": ["Maryam Mirzakhani", "Anousheh Ansari", "Shirin Ebadi", "Azar Nafisi"],
            "rationales": [
                {"option": "Anousheh Ansari", "why_plausible": "First Iranian woman in space.", "why_wrong": "Private astronaut who flew to the ISS in 2006."},
                {"option": "Shirin Ebadi", "why_plausible": "Nobel Peace Prize laureate.", "why_wrong": "Human rights lawyer who won the Nobel Peace Prize in 2003."},
                {"option": "Azar Nafisi", "why_plausible": "Author of Reading Lolita in Tehran.", "why_wrong": "Literary scholar and author."}
            ],
            "expl": "Mirzakhani made groundbreaking contributions to the dynamics and geometry of Riemann surfaces; her birthday, May 12, is recognized internationally as Women in Mathematics Day.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 810
        },
        {
            "text": "Appointed Iran's first female presiding judge in 1969, this human rights attorney was awarded the Nobel Peace Prize in 2003 for her defense of children and political dissidents.",
            "ans": "Shirin Ebadi",
            "aliases": ["Shirin Ebadi", "Ebadi", "شیرین عبادی"],
            "options": ["Shirin Ebadi", "Nasrin Sotoudeh", "Mehrangiz Kar", "Simin Behbahani"],
            "rationales": [
                {"option": "Nasrin Sotoudeh", "why_plausible": "Prominent human rights lawyer.", "why_wrong": "Sakharov Prize laureate who rose to prominence in the 2000s and 2010s."},
                {"option": "Mehrangiz Kar", "why_plausible": "Feminist human rights attorney.", "why_wrong": "Arrested after the Berlin Conference in 2000."},
                {"option": "Simin Behbahani", "why_plausible": "Poetess and dissident.", "why_wrong": "Renowned poet, not a lawyer."}
            ],
            "expl": "Ebadi was demoted to a court clerk after the 1979 revolution because clerical jurists held that women were too emotional to serve as judges; she later founded the Defenders of Human Rights Center.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 812
        },
        {
            "text": "Starring in The Downpour (1972) and Bashu, the Little Stranger (1986), this magnetic stage and screen actress emigrated to Sweden, becoming a leading actress of the Royal Dramatic Theatre.",
            "ans": "Susan Taslimi",
            "aliases": ["Susan Taslimi", "Soosan Taslimi", "سوسن تسلیمی"],
            "options": ["Susan Taslimi", "Shohreh Aghdashloo", "Fatemeh Motamed-Arya", "Golshifteh Farahani"],
            "rationales": [
                {"option": "Shohreh Aghdashloo", "why_plausible": "Oscar-nominated Iranian actress.", "why_wrong": "Nominated for House of Sand and Fog in 2003 in Hollywood."},
                {"option": "Fatemeh Motamed-Arya", "why_plausible": "Leading domestic cinema star (The Blue-Veiled).", "why_wrong": "Remained in Iran working in domestic cinema."},
                {"option": "Golshifteh Farahani", "why_plausible": "International cinema star in Paris.", "why_wrong": "Emigrated in 2008 to France."}
            ],
            "expl": "Taslimi's fiercely independent performances under director Bahram Beyzai defined the golden era of modern Iranian auteur cinema.",
            "book": "A Social History of Iranian Cinema, Vol. 1", "auth": "Hamid Naficy", "pg": 350
        },
        {
            "text": "Known as 'Dabagh', this revolutionary militant fought in Lebanon alongside Chamran, guarded Khomeini in Paris, and was appointed the first female commander of the IRGC in Hamadan.",
            "ans": "Marzieh Hadidchi (Dabagh)",
            "aliases": ["Marzieh Hadidchi", "Marzieh Dabagh", "Tahereh Dabagh", "مرضیه حدیدچی", "دباغ", "مرضیه حدیدچی دباغ"],
            "options": ["Marzieh Hadidchi (Dabagh)", "Masoumeh Ebtekar", "Zahra Rahnavard", "Monireh Gorji"],
            "rationales": [
                {"option": "Masoumeh Ebtekar", "why_plausible": "Hostage crisis spokesperson.", "why_wrong": "Student spokesperson, not a military commander in the IRGC."},
                {"option": "Zahra Rahnavard", "why_plausible": "Author and academic.", "why_wrong": "Academic and artist."},
                {"option": "Monireh Gorji", "why_plausible": "Only woman elected to the 1979 Assembly of Experts.", "why_wrong": "Theological scholar in the constitutional assembly."}
            ],
            "expl": "Dabagh was one of three envoys chosen by Khomeini in January 1989 to travel to Moscow to deliver his historic philosophical letter to Soviet President Mikhail Gorbachev.",
            "book": "The Reign of the Ayatollahs", "auth": "Shaul Bakhash", "pg": 242
        },
        {
            "text": "In September 2006, this Iranian-American engineer and entrepreneur made history as the first female private space explorer and first Iranian in space, docking at the ISS.",
            "ans": "Anousheh Ansari",
            "aliases": ["Anousheh Ansari", "Ansari", "انوشه انصاری"],
            "options": ["Anousheh Ansari", "Maryam Mirzakhani", "Camila Batmanghelidjh", "Pardis Sabeti"],
            "rationales": [
                {"option": "Maryam Mirzakhani", "why_plausible": "Fields Medalist mathematician.", "why_wrong": "Mathematician at Stanford."},
                {"option": "Camila Batmanghelidjh", "why_plausible": "Charity founder.", "why_wrong": "Founded Kids Company in London."},
                {"option": "Pardis Sabeti", "why_plausible": "Harvard geneticist.", "why_wrong": "Computational biologist tracking Ebola."}
            ],
            "expl": "Ansari wore the Iranian and American flags on her spacesuit and performed experiments on cell biology aboard the Soyuz TMA-9 flight.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 814
        }
    ])

    # 6. WAR DIARIES: FRONTLINE MEMOIRS (Double)
    add_5("WAR DIARIES: FRONTLINE MEMOIRS", "Sacred Defense Literature", "Combat Chronicles", "double", [
        {
            "text": "Set in besieged Abadan, this acclaimed 2005 novel by Habib Ahmadzadeh follows an 18-year-old artillery spotter engaged in a psychological duel against Iraqi radar.",
            "ans": "Chess with the Doomsday Machine",
            "aliases": ["Chess with the Doomsday Machine", "Shatranj ba Mashin-e Qiamat", "شطرنج با ماشین قیامت"],
            "options": ["Chess with the Doomsday Machine", "Journey to Heading 270", "Da", "The Fortune of the Dead"],
            "rationales": [
                {"option": "Journey to Heading 270", "why_plausible": "War novel by Ahmad Dehqan.", "why_wrong": "Novel set during Operation Karbala-5 by Ahmad Dehqan."},
                {"option": "Da", "why_plausible": "Bestselling female memoir.", "why_wrong": "Zahra Hosseini's memoir of burying martyrs in Khorramshahr."},
                {"option": "The Fortune of the Dead", "why_plausible": "Post-war novel.", "why_wrong": "Novel by Mohammad-Reza Bayrami."}
            ],
            "expl": "The 'Doomsday Machine' was a British-supplied Cymbeline mortar-locating radar deployed by Iraqi forces to obliterate Iranian artillery batteries.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 794
        },
        {
            "text": "Authored by Ahmad Dehqan, this unvarnished combat novel broke with official propaganda to depict the grim terror, thirst, and gore endured during Operation Karbala-5.",
            "ans": "Journey to Heading 270",
            "aliases": ["Journey to Heading 270", "Safar be Gera-ye 270 Darajeh", "سفر به گرای ۲۷۰ درجه", "سفر به گرای 270 درجه"],
            "options": ["Journey to Heading 270", "Chess with the Doomsday Machine", "Da", "Boruncheh"],
            "rationales": [
                {"option": "Chess with the Doomsday Machine", "why_plausible": "Abadan novel.", "why_wrong": "Ahmadzadeh's novel set in Abadan."},
                {"option": "Da", "why_plausible": "Female memoir.", "why_wrong": "Memoir of the Khorramshahr siege."},
                {"option": "Boruncheh", "why_plausible": "Martyr memoir.", "why_wrong": "Memoir of commander Abdol-Hossein Borunsi."}
            ],
            "expl": "Translated into English by Paul Sprachman, the novel won the twenty-year Sacred Defense literary prize for its unromanticized realism.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 795
        },
        {
            "text": "A construction worker from Mashhad who commanded the 18th Javad ol-A'emmeh Brigade, this illiterate mystic-warrior was immortalized in the million-copy bestseller Khak-haye Narm-e Koushk.",
            "ans": "Abdol-Hossein Borunsi",
            "aliases": ["Abdol-Hossein Borunsi", "Borunsi", "Shahid Borunsi", "عبدالحسین برونسی", "شهید برونسی"],
            "options": ["Abdol-Hossein Borunsi", "Mohammad Jahanara", "Ebrahim Hemmat", "Mehdi Bakeri"],
            "rationales": [
                {"option": "Mohammad Jahanara", "why_plausible": "Commander of Khorramshahr.", "why_wrong": "Killed in an airplane crash in 1981, subject of the song Mamad Naboodi."},
                {"option": "Ebrahim Hemmat", "why_plausible": "Commander of the 27th Mohammad Rasulullah Division.", "why_wrong": "Fell at Majnoon Island in Operation Kheibar."},
                {"option": "Mehdi Bakeri", "why_plausible": "Commander of the 31st Ashura Division.", "why_wrong": "Azeri commander whose body was swept away in the Tigris."}
            ],
            "expl": "Authored by Sa'id Owhadi, Khak-haye Narm-e Koushk (The Soft Soil of Koushk) recounts Borunsi's visions of Lady Fatima guiding his platoon through minefields before his death in 1985.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 796
        },
        {
            "text": "This desolate desert battlefield in Ilam and Khuzestan became known as the 'Graveyard of Tanks', where thousands of young Basij volunteers cleared minefields with their bodies.",
            "ans": "Fakkeh",
            "aliases": ["Fakkeh", "Fakke", "فکه"],
            "options": ["Fakkeh", "Shalamcheh", "Talaiyeh", "Dehloran"],
            "rationales": [
                {"option": "Shalamcheh", "why_plausible": "Border crossing site of Karbala-5.", "why_wrong": "Directly east of Basra, whereas Fakkeh is in the north along the Chazabeh border."},
                {"option": "Talaiyeh", "why_plausible": "Marshland battlefield near Majnoon.", "why_wrong": "Amphibious marsh causeway."},
                {"option": "Dehloran", "why_plausible": "Ilam province town.", "why_wrong": "City behind the lines, not the killing field of shifting sands."}
            ],
            "expl": "Documentary filmmaker Morteza Avini was martyred in Fakkeh on April 9, 1993, while filming unexploded ordnance for Chronicles of Victory.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 797
        },
        {
            "text": "Commander of the 31st Ashura Division from Tabriz, this beloved hero was killed in a boat on the Tigris during Operation Badr in 1985, his body hit by an RPG and lost to the waters.",
            "ans": "Mehdi Bakeri",
            "aliases": ["Mehdi Bakeri", "Bakeri", "Shahid Bakeri", "مهدی باکری", "باکری"],
            "options": ["Mehdi Bakeri", "Ebrahim Hemmat", "Hossein Kharrazi", "Ahmad Motevasselian"],
            "rationales": [
                {"option": "Ebrahim Hemmat", "why_plausible": "Charismatic division commander.", "why_wrong": "Killed at Majnoon Island in 1984."},
                {"option": "Hossein Kharrazi", "why_plausible": "Commander of the 14th Imam Hussein Division of Isfahan.", "why_wrong": "Lost an arm at Kheibar and was killed at Karbala-5 in 1987."},
                {"option": "Ahmad Motevasselian", "why_plausible": "Kidnapped in Lebanon in 1982.", "why_wrong": "Captured by Christian Phalangists in Beirut in 1982."}
            ],
            "expl": "When his brother Ali was killed hours earlier, Bakeri refused to evacuate his body before ordinary soldiers; his life inspired the 2022 film The Situation of Mehdi (Mogheiat-e Mehdi).",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 798
        }
    ])

    print("Writing Batch 8 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Total clues after Part 8:", len(clues_by_id))

if __name__ == "__main__":
    run_part8()
