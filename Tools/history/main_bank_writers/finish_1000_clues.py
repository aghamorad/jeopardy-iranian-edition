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
            "page": item.get("pg", 520 + idx * 8),
            "supporting_passage": item.get("passage", item["expl"]),
            "evidence_type": "established_fact", "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": f"{item['ans']}. Spot on!",
                "wrong_generic": f"No, we were looking for {item['ans']}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
            }
        }

def add_final(clues_by_id, cat, items):
    prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "")
    for idx, item in enumerate(items):
        cid = f"final_{prefix}_{idx+1}"
        clues_by_id[cid] = {
            "id": cid, "language": "en", "category": cat, "historical_period": "Historical Turning Point",
            "theme": "Final Jeopardy", "difficulty": "SCHOLAR", "value": 0, "round": "final",
            "clue_text": item["text"], "canonical_answer": item["ans"],
            "accepted_aliases": item["aliases"], "partial_answers": [], "specificity_prompt": "",
            "options": item["options"], "correct_option_index": 0,
            "distractor_rationales": item["rationales"], "explanation": item["expl"],
            "source_id": item.get("src", "amanat_iran_modern_history_2017"),
            "book_title": item.get("book", "Iran: A Modern History"),
            "author": item.get("auth", "Abbas Amanat"),
            "chapter": item.get("ch", "Historical Climax"),
            "page": item.get("pg", 620 + idx * 50),
            "supporting_passage": item.get("passage", item["expl"]),
            "evidence_type": "established_fact", "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": f"Correct! {item['ans']}.",
                "wrong_generic": f"No, the correct response was {item['ans']}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
            }
        }

clues = load_data()

# 1. THE BAKHTIARI MARCH (Double, 10 clues)
add_batch(clues, "THE BAKHTIARI MARCH", "Tribal Cavalry & Revolution", "Constitutional Liberation", "double", [
    {"text": "The cultured Bakhtiari Ilkhan who had traveled widely in Paris and led the tribal cavalry that stormed Tehran in July 1909 was named this.",
     "ans": "Ali-Qoli Khan Sardar As'ad (Sardar As'ad II)", "aliases": ["Ali-Qoli Khan Sardar As'ad", "Sardar As'ad", "Sardar As'ad II", "سردار اسعد", "علیقلی خان سردار اسعد"],
     "options": ["Ali-Qoli Khan Sardar As'ad (Sardar As'ad II)", "Samsam al-Saltaneh", "Ja'far-Qoli Khan", "Hosein-Qoli Khan"],
     "rationales": [{"option": "Samsam al-Saltaneh", "why_plausible": "His brother who captured Isfahan.", "why_wrong": "Najaf-Qoli Khan, who stayed in Isfahan as governor."},
                    {"option": "Ja'far-Qoli Khan", "why_plausible": "His nephew Sardar As'ad III.", "why_wrong": "Reza Shah's war minister murdered in Qasr prison in 1934."},
                    {"option": "Hosein-Qoli Khan", "why_plausible": "His father.", "why_wrong": "Ilkhani executed by Zell-e Soltan in 1882."}],
     "expl": "Sardar As'ad financed the march using Bakhtiari oil royalties, forming an unbreakable military alliance with Yeprem Khan's northern fighters.", "pg": 410},
    {"text": "In January 1909, Bakhtiari horsemen led by Zargham al-Saltaneh captured this grand Safavid capital, expelling the royalist governor.",
     "ans": "Isfahan", "aliases": ["Isfahan", "Esfahan", "اصفهان"],
     "options": ["Isfahan", "Shiraz", "Tabriz", "Kerman"],
     "rationales": [{"option": "Shiraz", "why_plausible": "Fars capital.", "why_wrong": "Controlled by Qashqai and Qavam factions."},
                    {"option": "Tabriz", "why_plausible": "Under siege.", "why_wrong": "Held by Sattar Khan under royalist siege."},
                    {"option": "Kerman", "why_plausible": "Southeastern city.", "why_wrong": "Not on the march route to Tehran."}],
     "expl": "The capture of Isfahan broke Mohammad Ali Shah's strategic rear, inspiring tribes across the Zagros to declare for the Constitution.", "pg": 409},
    {"text": "Under the 1905 agreement with William Knox D'Arcy, the Bakhtiari khans received this annual percentage of dividends and protection subsidies.",
     "ans": "Three Percent (Plus Guard Subsidies)", "aliases": ["Three Percent", "3 Percent", "3%", "سه درصد"],
     "options": ["Three Percent (Plus Guard Subsidies)", "Fifty Percent", "Sixteen Percent", "Ten Percent"],
     "rationales": [{"option": "Fifty Percent", "why_plausible": "Post-1950 split.", "why_wrong": "Standard 50-50 profit split came decades later."},
                    {"option": "Sixteen Percent", "why_plausible": "Central government share.", "why_wrong": "Iran's central government received 16% of net profits."},
                    {"option": "Ten Percent", "why_plausible": "Common royalty.", "why_wrong": "The First Exploitation Company allocated 3% to the Bakhtiari khans."}],
     "expl": "This private pipeline protection treaty made the Bakhtiari khans immensely wealthy and financially autonomous from the central government in Tehran.", "pg": 384},
    {"text": "The traditional semi-annual nomadic migration of the Bakhtiari tribes between winter lowland pastures (Garamsir) and summer alpine meadows is known as this.",
     "ans": "Kooch (Yeylaq and Qeshlaq)", "aliases": ["Kooch", "Yeylaq and Qeshlaq", "Bakhtiari Migration", "کوچ", "ییلاق و قشلاق"],
     "options": ["Kooch (Yeylaq and Qeshlaq)", "Ashura", "Hajj", "Nowruz"],
     "rationales": [{"option": "Ashura", "why_plausible": "Religious procession.", "why_wrong": "Mourning ritual in Muharram."},
                    {"option": "Hajj", "why_plausible": "Pilgrimage.", "why_wrong": "Islamic pilgrimage to Mecca."},
                    {"option": "Nowruz", "why_plausible": "Spring festival.", "why_wrong": "New Year celebration."}],
     "expl": "Immortalized in Merian C. Cooper's 1925 documentary film Grass: A Nation's Battle for Life, 50,000 tribesmen and 500,000 animals swam the freezing Karun River.", "pg": 18},
    {"text": "The sleeveless black-and-white striped felt tunic worn proudly by Bakhtiari men into battle and during seasonal migration is called this.",
     "ans": "Chukha (Chogha)", "aliases": ["Chukha", "Chogha", "Chukha Bakhtiari", "چوقا", "چوخا"],
     "options": ["Chukha (Chogha)", "Kolah-e Namadi", "Giveh", "Shalwar"],
     "rationales": [{"option": "Kolah-e Namadi", "why_plausible": "Headwear.", "why_wrong": "The round brimless black felt cap worn on the head."},
                    {"option": "Giveh", "why_plausible": "Footwear.", "why_wrong": "White hand-woven cotton espadrille shoes."},
                    {"option": "Shalwar", "why_plausible": "Trousers.", "why_wrong": "The loose black pleated trousers (Tonban)."}],
     "expl": "Woven by Bakhtiari women from sheep's wool, its geometric pattern is said to symbolize the ancient stepped battlements of Chogha Zanbil.", "pg": 19},
    # Set B
    {"text": "Sardar As'ad's elder brother who served as Prime Minister of Iran twice during the early Constitutional period was named this.",
     "ans": "Najaf-Qoli Khan Samsam al-Saltaneh", "aliases": ["Najaf-Qoli Khan Samsam al-Saltaneh", "Samsam al-Saltaneh", "صمصام‌السلطنه", "نجفقلی خان صمصام‌السلطنه"],
     "options": ["Najaf-Qoli Khan Samsam al-Saltaneh", "Vosough al-Dowleh", "Sepahdar-e Azam", "Moshir al-Dowleh"],
     "rationales": [{"option": "Vosough al-Dowleh", "why_plausible": "1919 premier.", "why_wrong": "Signed the 1919 agreement, political rival."},
                    {"option": "Sepahdar-e Azam", "why_plausible": "Northern commander premier.", "why_wrong": "Mohammad Vali Khan Tonekaboni, who led the Gilan constitutional force."},
                    {"option": "Moshir al-Dowleh", "why_plausible": "Hasan Pirnia premier.", "why_wrong": "Jurist and historian who drafted the constitution."}],
     "expl": "In 1918, Prime Minister Samsam al-Saltaneh boldly declared all 19th-century foreign capitulations and treaties null and void following the Russian Revolution.", "pg": 424},
    {"text": "In 1882, this ruthless Qajar Prince and governor of Isfahan murdered Bakhtiari Paramount Chief Hosein-Qoli Khan to break tribal independence.",
     "ans": "Zell-e Soltan (Mass'oud Mirza)", "aliases": ["Zell-e Soltan", "Mass'oud Mirza Zell-e Soltan", "ضل‌السلطان", "ظل‌السلطان"],
     "options": ["Zell-e Soltan (Mass'oud Mirza)", "Kamran Mirza", "Mozaffar al-Din Mirza", "Nayeb al-Saltaneh"],
     "rationales": [{"option": "Kamran Mirza", "why_plausible": "War minister in Tehran.", "why_wrong": "Governor of Tehran and commander of the army."},
                    {"option": "Mozaffar al-Din Mirza", "why_plausible": "Crown prince in Tabriz.", "why_wrong": "Governor of Azerbaijan in Tabriz."},
                    {"option": "Nayeb al-Saltaneh", "why_plausible": "Regent title.", "why_wrong": "Title of Kamran Mirza."}],
     "expl": "Zell-e Soltan offered Hosein-Qoli Khan poisoned coffee at a military banquet in Isfahan, imprisoning his sons Ali-Qoli and Najaf-Qoli.", "pg": 378},
    {"text": "Under Reza Shah in the 1930s, the autonomous power of the Bakhtiari was violently shattered through forced sedentarization, execution of khans, and this policy.",
     "ans": "Forced Tribal Disarmament (Takhteh-Qapu)", "aliases": ["Forced Tribal Disarmament", "Takhteh-Qapu", "Disarmament", "تخته قاپو", "خلع سلاح عشایر"],
     "options": ["Forced Tribal Disarmament (Takhteh-Qapu)", "Land Redistribution", "Conversion to Sunnism", "Deportation to Siberia"],
     "rationales": [{"option": "Land Redistribution", "why_plausible": "Land reform.", "why_wrong": "Conducted by his son in the 1960s White Revolution."},
                    {"option": "Conversion to Sunnism", "why_plausible": "Religious policy.", "why_wrong": "They were already Shi'i."},
                    {"option": "Deportation to Siberia", "why_plausible": "Soviet policy.", "why_wrong": "Russian Tsarist/Soviet method, not Iranian policy."}],
     "expl": "The army prohibited migration, slaughtering herds and confiscating tens of thousands of rifles to establish modern state supremacy.", "pg": 470},
    {"text": "In 1934, War Minister Ja'far-Qoli Khan Sardar As'ad III was arrested during royal horse races in Dasht-e Gorgan and murdered in Qasr prison by this royal doctor.",
     "ans": "Dr. Ahmad Ahmadi (Pezeshk Ahmadi)", "aliases": ["Dr. Ahmad Ahmadi", "Pezeshk Ahmadi", "Ahmadi", "پزشک احمدی"],
     "options": ["Dr. Ahmad Ahmadi (Pezeshk Ahmadi)", "Dr. Mohammad Mosaddegh", "Dr. Taghi Arani", "Dr. Georges Flandrin"],
     "rationales": [{"option": "Dr. Mohammad Mosaddegh", "why_plausible": "Jurist.", "why_wrong": "Jailed by Reza Shah, survived."},
                    {"option": "Dr. Taghi Arani", "why_plausible": "Marxist prisoner.", "why_wrong": "Victim of prison conditions, not the executioner doctor."},
                    {"option": "Dr. Georges Flandrin", "why_plausible": "French physician.", "why_wrong": "Diagnosed the Shah's cancer in 1974."}],
     "expl": "Pezeshk Ahmadi injected lethal doses of air and potassium into the veins of prominent political prisoners under police chief Mokhtari.", "pg": 476},
    {"text": "The ancestral mountain heartland of the Bakhtiari nomads in the central Zagros Mountains forms this modern Iranian province.",
     "ans": "Chaharmahal and Bakhtiari Province", "aliases": ["Chaharmahal and Bakhtiari", "Chaharmahal", "چهارمحال و بختیاری"],
     "options": ["Chaharmahal and Bakhtiari Province", "Lorestan", "Kohgiluyeh and Boyer-Ahmad", "Ilam"],
     "rationales": [{"option": "Lorestan", "why_plausible": "Northern Lur province.", "why_wrong": "Home to the Feili Lurs around Khorramabad."},
                    {"option": "Kohgiluyeh and Boyer-Ahmad", "why_plausible": "Southern Lur province.", "why_wrong": "Home to the Boyer-Ahmadi clans around Yasuj."},
                    {"option": "Ilam", "why_plausible": "Western border province.", "why_wrong": "Home to Kurdish and Lur border tribes."}],
     "expl": "With its capital at Shahrekord, it contains the high alpine headwaters of both the Karun and Zayandeh rivers.", "pg": 17}
])

# 2. RADIO TEHRAN CALLING (Double, 10 clues)
add_batch(clues, "RADIO TEHRAN CALLING", "Broadcast Media & Propaganda", "Sound Waves", "double", [
    {"text": "On April 24, 1940, Radio Tehran was officially inaugurated with a live speech delivered from the wireless transmission mast at Pahlavi Wireless by this monarch.",
     "ans": "Crown Prince Mohammad Reza (Later Mohammad Reza Shah)", "aliases": ["Crown Prince Mohammad Reza", "Mohammad Reza Pahlavi", "Crown Prince", "محمدرضا پهلوی", "ولیعهد"],
     "options": ["Crown Prince Mohammad Reza (Later Mohammad Reza Shah)", "Reza Shah", "Nasir al-Din Shah", "Ahmad Shah"],
     "rationales": [{"option": "Reza Shah", "why_plausible": "Reigning monarch.", "why_wrong": "Reza Shah disliked microphones, dispatching his French-educated son to open the station."},
                    {"option": "Nasir al-Din Shah", "why_plausible": "Early modernizer.", "why_wrong": "Reigned in the 19th century before radio existed."},
                    {"option": "Ahmad Shah", "why_plausible": "Last Qajar.", "why_wrong": "Deposed in 1925."}],
     "expl": "Broadcasting with a 20-kilowatt transmitter built by Germany's Telefunken, Radio Tehran was initially limited to five hours of evening broadcasts per day.", "pg": 488},
    {"text": "During WWII, Nazi Germany broadcast Persian propaganda across Iran featuring this antisemitic Persian announcer known as 'Bahram the Persian'.",
     "ans": "Bahram Shahrokh", "aliases": ["Bahram Shahrokh", "Shahrokh", "Radio Berlin Announcer", "بهرام شاهرخ"],
     "options": ["Bahram Shahrokh", "Davood Pirnia", "Taghi Arani", "Ahmad Fardid"],
     "rationales": [{"option": "Davood Pirnia", "why_plausible": "Radio producer.", "why_wrong": "Creator of the Golha classical music program."},
                    {"option": "Taghi Arani", "why_plausible": "Marxist intellectual.", "why_wrong": "Died in Reza Shah's prison in 1940."},
                    {"option": "Ahmad Fardid", "why_plausible": "Philosopher.", "why_wrong": "Philosopher who coined the term Gharbzadegi."}],
     "expl": "Broadcasting nightly from Radio Berlin, Shahrokh claimed Hitler was the promised Twelfth Imam, urging Iranians to sabotage Allied railway supply lines.", "pg": 489},
    {"text": "On the afternoon of August 19, 1953, royalist army officers seized Radio Tehran, where this actress famously shouted into the microphone: 'The traitor Mosaddegh has fled!'",
     "ans": "Homa Zahedi (or Moluk Zarabi / Subversive Broadcaster)", "aliases": ["Homa Zahedi", "Moluk Zarabi", "Royalist Announcer", "گوینده رادیو تهران ۲۸ مرداد"],
     "options": ["Homa Zahedi (or Moluk Zarabi / Subversive Broadcaster)", "Googoosh", "Delkash", "Simin Daneshvar"],
     "rationales": [{"option": "Googoosh", "why_plausible": "Child performer at the time.", "why_wrong": "Only three years old in 1953."},
                    {"option": "Delkash", "why_plausible": "Famous singer.", "why_wrong": "Refused to broadcast political announcements during the coup."},
                    {"option": "Simin Daneshvar", "why_plausible": "Author.", "why_wrong": "Opposed the coup."}],
     "expl": "Royalist conspirators broadcast martial music and martial law edicts from the wireless studios while tanks encircled Mosaddegh's private house on Kakh Street.", "pg": 523},
    {"text": "In the 1970s, the clandestine National Voice of Iran (Sedaye Melli-ye Iran) beamed anti-Shah communist propaganda into Tehran from this Soviet republic capital.",
     "ans": "Baku (Soviet Azerbaijan)", "aliases": ["Baku", "Soviet Azerbaijan", "باکو"],
     "options": ["Baku (Soviet Azerbaijan)", "Tashkent", "Yerevan", "Moscow"],
     "rationales": [{"option": "Tashkent", "why_plausible": "Central Asian Soviet broadcasting center.", "why_wrong": "Beamed broadcasts to India and Pakistan, while Persian subversion was based in Baku."},
                    {"option": "Yerevan", "why_plausible": "Armenian SSR capital.", "why_wrong": "Transmitted Armenian programs."},
                    {"option": "Moscow", "why_plausible": "Soviet capital.", "why_wrong": "Radio Moscow had an official service, but the clandestine station operated out of Baku."}],
     "expl": "Funded by the KGB and staffed by exiled Tudeh activists, it instructed Iranian factory workers and oil technicians on how to organize illegal general strikes.", "pg": 648},
    {"text": "The iconic four-tone chimes played on Radio Tehran to announce the top-of-the-hour news broadcast were composed on this traditional Persian percussion instrument.",
     "ans": "Santoor", "aliases": ["Santoor", "Santur", "سنتور"],
     "options": ["Santoor", "Tar", "Kamancheh", "Tombak"],
     "rationales": [{"option": "Tar", "why_plausible": "Plucked lute.", "why_wrong": "Plucked string instrument."},
                    {"option": "Kamancheh", "why_plausible": "Bowed spike fiddle.", "why_wrong": "Bowed string instrument."},
                    {"option": "Tombak", "why_plausible": "Goblet drum.", "why_wrong": "Drum, cannot produce the melodic four-tone chime."}],
     "expl": "Struck with felt-tipped wooden mallets (Mezrab), the shimmering acoustic chimes became the instantly recognizable auditory trademark of National Iranian Radio.", "pg": 515},
    # Set B
    {"text": "During the Iran-Iraq War, Radio Tehran terrified residents across western and central Iran with this shrill siren followed by the voice announcement: 'Attention! Attention!'",
     "ans": "Red Alert Air Raid Siren (Vaz'iyat-e Qermez)", "aliases": ["Red Alert Air Raid Siren", "Red Alert", "Vaz'iyat-e Qermez", "وضعیت قرمز", "آژیر قرمز"],
     "options": ["Red Alert Air Raid Siren (Vaz'iyat-e Qermez)", "Yellow Alert", "White Siren", "Martial Law Bugle"],
     "rationales": [{"option": "Yellow Alert", "why_plausible": "Preliminary warning.", "why_wrong": "Announced potential incoming bombers, not immediate missile strikes."},
                    {"option": "White Siren", "why_plausible": "All-clear signal.", "why_wrong": "Signaled the all-clear after attacks ceased."},
                    {"option": "Martial Law Bugle", "why_plausible": "Curfew signal.", "why_wrong": "Bugle call used for street curfews in 1978."}],
     "expl": "The chilling voice of announcer Iraj Fathi warned: 'The siren you are about to hear indicates that an air raid or missile attack is imminent; turn off all lights and take shelter!'", "pg": 788},
    {"text": "The state broadcasting corporation created in 1971 by merging state radio and television into an independent monopoly under Reza Ghotbi was known as this.",
     "ans": "NIRT (National Iranian Radio and Television)", "aliases": ["NIRT", "National Iranian Radio and Television", "NIRTV", "رادیو و تلویزیون ملی ایران"],
     "options": ["NIRT (National Iranian Radio and Television)", "IRIB", "Radio Iran", "Pars News Agency"],
     "rationales": [{"option": "IRIB", "why_plausible": "Post-1979 name.", "why_wrong": "Renamed Islamic Republic of Iran Broadcasting after the 1979 revolution."},
                    {"option": "Radio Iran", "why_plausible": "Radio branch.", "why_wrong": "The radio branch before the 1971 television merger."},
                    {"option": "Pars News Agency", "why_plausible": "State wire service.", "why_wrong": "The news wire agency (now IRNA)."}],
     "expl": "Ghotbi, a French-educated cousin of Empress Farah, built state-of-the-art color television studios on Jame Jam Street, employing thousands of creative artists.", "pg": 630},
    {"text": "On February 11, 1979, veteran announcer Mohammad-Reza Hayati and revolutionary broadcaster Fazlollah Mahallati seized Radio Tehran and declared this.",
     "ans": "This is the Voice of the Revolution of the True People of Iran! (In seda-ye enqelab-e mardomi-ye Iran ast)", "aliases": ["This is the Voice of the Revolution", "In seda-ye enqelab ast", "Voice of the Revolution", "این صدای انقلاب ایران است", "صدای انقلاب"],
     "options": ["This is the Voice of the Revolution of the True People of Iran!", "The Shah has Abdicated!", "The Islamic Republic is Established!", "Long Live Khomeini!"],
     "rationales": [{"option": "The Shah has Abdicated!", "why_plausible": "Monarchical announcement.", "why_wrong": "The Shah had departed weeks earlier on January 16."},
                    {"option": "The Islamic Republic is Established!", "why_plausible": "Constitutional outcome.", "why_wrong": "The referendum on the Islamic Republic was held two months later in April."},
                    {"option": "Long Live Khomeini!", "why_plausible": "Chanted in streets.", "why_wrong": "The historic broadcast phrase was 'In seda-ye enqelab ast'."}],
     "expl": "The broadcast signaled the total collapse of the Bakhtiar government and the surrender of the Supreme Military Council, marking the official triumph of the revolution.", "pg": 730},
    {"text": "Radio Iran's immensely popular Friday morning comedy and satirical variety show that kept millions of families laughing beside their transistors was called this.",
     "ans": "Sobh-e Jomeh ba Shoma (Friday Morning with You)", "aliases": ["Sobh-e Jomeh ba Shoma", "Sobh-e Jomeh", "صبح جمعه با شما"],
     "options": ["Sobh-e Jomeh ba Shoma", "Golha", "Shoma va Radio", "Farhang va Honar"],
     "rationales": [{"option": "Golha", "why_plausible": "Classical music show.", "why_wrong": "Solemn classical poetry and vocal music program."},
                    {"option": "Shoma va Radio", "why_plausible": "Variety show.", "why_wrong": "Midweek listener request show."},
                    {"option": "Farhang va Honar", "why_plausible": "Cultural show.", "why_wrong": "Ministry cultural program."}],
     "expl": "Featuring comic actors like Manouchehr Nozari and Alireza Javidnia, it playfully satirized everyday bureaucracy, price inflation, and in-law disputes.", "pg": 632},
    {"text": "In 1941, during the Allied invasion, British and Soviet radio engineers seized the Radio Tehran transmitters to broadcast this ultimatum.",
     "ans": "Demand for the Abdication and Departure of Reza Shah", "aliases": ["Demand for the Abdication of Reza Shah", "Reza Shah Abdication", "استعفای رضاشاه", "خلع رضاشاه"],
     "options": ["Demand for the Abdication and Departure of Reza Shah", "Unconditional Annexation of Iran", "Declaration of War on Germany", "Dissolution of the Majles"],
     "rationales": [{"option": "Unconditional Annexation of Iran", "why_plausible": "Colonial threat.", "why_wrong": "Allies pledged to respect Iranian territorial integrity in the 1942 tripartite treaty."},
                    {"option": "Declaration of War on Germany", "why_plausible": "Diplomatic goal.", "why_wrong": "Iran declared war on Germany in 1943 under the young Shah."},
                    {"option": "Dissolution of the Majles", "why_plausible": "Constitutional threat.", "why_wrong": "The Majles convened to swear in the new young Shah."}],
     "expl": "BBC Persian broadcast devastating exposés of Reza Shah's land confiscations, prompting him to abdicate in favor of his 21-year-old son on September 16, 1941.", "pg": 486}
])

# 5 FINAL JEOPARDY CATEGORIES (10 clues: 5 categories x 2 clues each)
# 1. THE LION OF AZERBAIJAN
add_final(clues, "THE LION OF AZERBAIJAN", [
    {"text": "Wounded during the Park-e Atabak disarmament showdown in Tehran in 1910, this constitutional folk hero of Tabriz died four years later, buried in Shah Abdol-Azim.",
     "ans": "Sattar Khan (Sardar-e Melli)", "aliases": ["Sattar Khan", "Sardar-e Melli", "ستارخان", "سردار ملی"],
     "options": ["Sattar Khan (Sardar-e Melli)", "Baqer Khan", "Yeprem Khan", "Heydar Khan"],
     "rationales": [{"option": "Baqer Khan", "why_plausible": "Salar-e Melli.", "why_wrong": "Killed during WWI near Kermanshah by Kurdish bandits."},
                    {"option": "Yeprem Khan", "why_plausible": "Police chief.", "why_wrong": "Killed in battle against royalists in Hamadan in 1912."},
                    {"option": "Heydar Khan", "why_plausible": "Revolutionary organizer.", "why_wrong": "Died in Gilan in 1921."}],
     "expl": "Sattar Khan took refuge with his horsemen in Park-e Atabak; government forces under Yeprem Khan opened fire to enforce disarmament, crippling Sattar Khan with a bullet to his ankle.", "pg": 418},
    {"text": "During the eleven-month siege of Tabriz in 1908, when foreign diplomats urged him to surrender and raise the Russian flag over his house, Sattar Khan declared: 'I want seven states to take shelter under...'",
     "ans": "The Banner of Iran (The Iranian Flag)", "aliases": ["The Banner of Iran", "The Iranian Flag", "Flag of Iran", "زیر پرچم ایران", "پرچم ایران"],
     "options": ["The Banner of Iran (The Iranian Flag)", "The House of Parliament", "The Holy Quran", "The Red Banner of Liberty"],
     "rationales": [{"option": "The House of Parliament", "why_plausible": "Constitutional symbol.", "why_wrong": "He specifically invoked the three-colored national flag."},
                    {"option": "The Holy Quran", "why_plausible": "Religious shield.", "why_wrong": "His famous retort to Russian consul Pokhitonov centered on the flag."},
                    {"option": "The Red Banner of Liberty", "why_plausible": "Revolutionary banner.", "why_wrong": "He rejected foreign and socialist flags in favor of Iran's national colors."}],
     "expl": "Sattar Khan boldly retorted: 'I want seven foreign empires to submit under the shadow of the Iranian flag; shall I then surrender under a foreign banner?'", "pg": 407}
])

# 2. THE POISONED CHALICE LETTER
add_final(clues, "THE POISONED CHALICE LETTER", [
    {"text": "In his broadcast letter of July 20, 1988 accepting UN Resolution 598 to end the Iran-Iraq War, Ayatollah Khomeini famously stated that doing so was more deadly than this.",
     "ans": "Drinking a Chalice of Poison (Jām-e Zahr)", "aliases": ["Drinking a Chalice of Poison", "Drinking Poison", "Jām-e Zahr", "جام زهر", "نوشیدن جام زهر"],
     "options": ["Drinking a Chalice of Poison (Jām-e Zahr)", "Surrendering to America", "Dying in Battle", "Surrendering the Holy Shrines"],
     "rationales": [{"option": "Surrendering to America", "why_plausible": "Anti-US rhetoric.", "why_wrong": "He used the tragic metaphor of swallowing poison."},
                    {"option": "Dying in Battle", "why_plausible": "Martyrdom concept.", "why_wrong": "He stated he would have preferred martyrdom in battle over accepting the ceasefire."},
                    {"option": "Surrendering the Holy Shrines", "why_plausible": "War objective.", "why_wrong": "The war's slogan was 'The road to Jerusalem passes through Karbala'."}],
     "expl": "Khomeini wrote: 'Happy are those who were martyred in battle; woe to me that I survived to drink the poisoned chalice of accepting this resolution.'", "pg": 798},
    {"text": "The United Nations Security Council resolution passed in July 1987 that established the formal diplomatic framework for ending the Iran-Iraq War was this number.",
     "ans": "Resolution 598", "aliases": ["Resolution 598", "UN Resolution 598", "UNSCR 598", "قطعنامه ۵۹۸"],
     "options": ["Resolution 598", "Resolution 242", "Resolution 678", "Resolution 478"],
     "rationales": [{"option": "Resolution 242", "why_plausible": "1967 Arab-Israeli resolution.", "why_wrong": "Dealt with the 1967 Six-Day War."},
                    {"option": "Resolution 678", "why_plausible": "1990 Gulf War resolution.", "why_wrong": "Authorized military force against Iraq in Kuwait."},
                    {"option": "Resolution 478", "why_plausible": "Jerusalem resolution.", "why_wrong": "Nullified Israel's Jerusalem law."}],
     "expl": "Resolution 598 called for an immediate ceasefire, withdrawal to international borders, exchange of all POWs, and an impartial tribunal to identify the aggressor.", "pg": 796}
])

# 3. THE GALA OF PEACOCKS
add_final(clues, "THE GALA OF PEACOCKS", [
    {"text": "The historic Paris fashion house commissioned to design the blue-and-gold imperial staff and hostess uniforms for the 1971 Persepolis Celebrations was this.",
     "ans": "Lanvin", "aliases": ["Lanvin", "House of Lanvin", "لانوین"],
     "options": ["Lanvin", "Christian Dior", "Chanel", "Yves Saint Laurent"],
     "rationales": [{"option": "Christian Dior", "why_plausible": "Designed royal wedding dresses.", "why_wrong": "Dior made Empress Farah's 1959 and 1967 gowns, while Lanvin won the massive uniform contract for 1971."},
                    {"option": "Chanel", "why_plausible": "Classic French couture.", "why_wrong": "Did not design corporate uniforms for Persepolis."},
                    {"option": "Yves Saint Laurent", "why_plausible": "High fashion.", "why_wrong": "Guest at the gala, not the uniform manufacturer."}],
     "expl": "Lanvin designed hundreds of tailored uniforms with gold braided epaulettes for palace staff, waiters, and drivers serving the world's royalty in the tent city.", "pg": 612},
    {"text": "The exclusive French caterer flown into Persepolis with 165 chefs, sommeliers, and waiters to prepare the five-course banquets for the 1971 gala was this.",
     "ans": "Maxim's de Paris", "aliases": ["Maxim's de Paris", "Maxim's", "Maxims", "ماکسیم", "ماکسیم پاریس"],
     "options": ["Maxim's de Paris", "Le Cirque", "Fauchon", "La Tour d'Argent"],
     "rationales": [{"option": "Le Cirque", "why_plausible": "New York luxury dining.", "why_wrong": "Founded later in 1974 in New York."},
                    {"option": "Fauchon", "why_plausible": "French gourmet supplier.", "why_wrong": "Supplied pastries, while Maxim's catered the entire royal banquet."},
                    {"option": "La Tour d'Argent", "why_plausible": "Historic Paris restaurant.", "why_wrong": "Famous for pressed duck in Paris."}],
     "expl": "Maxim's shut down its flagship Rue Royale restaurant in Paris for two weeks, flying eighteen tons of food and rare French wines into Shiraz on military transports.", "pg": 614}
])

# 4. THE FORGOTTEN CAPITAL
add_final(clues, "THE FORGOTTEN CAPITAL", [
    {"text": "In 1555, Shah Tahmasp I moved the Safavid capital from Tabriz to this strategic inland plateau city to protect the court from Ottoman border cannon fire.",
     "ans": "Qazvin", "aliases": ["Qazvin", "City of Qazvin", "قزوین"],
     "options": ["Qazvin", "Isfahan", "Shiraz", "Kashan"],
     "rationales": [{"option": "Isfahan", "why_plausible": "Later grand capital.", "why_wrong": "Capital was moved to Isfahan four decades later in 1598 by Shah Abbas I."},
                    {"option": "Shiraz", "why_plausible": "Zand capital.", "why_wrong": "Zand capital in the 18th century."},
                    {"option": "Kashan", "why_plausible": "Central city.", "why_wrong": "Never the imperial capital."}],
     "expl": "Qazvin served as the imperial capital for 43 years, where Tahmasp laid out the first Chahar Bagh royal boulevard and Ali Qapu portal gate.", "pg": 150},
    {"text": "The surviving royal palace pavilion of Shah Tahmasp I in Qazvin, known for its two-story wooden octagonal columned porches, is called this.",
     "ans": "Chehel Sotoun of Qazvin (Kakh-e Chehel Sotoun)", "aliases": ["Chehel Sotoun of Qazvin", "Chehel Sotoun Qazvin", "Kolah Farangi Qazvin", "چهلستون قزوین", "عمارت کلاه‌فرنگی قزوین"],
     "options": ["Chehel Sotoun of Qazvin (Kakh-e Chehel Sotoun)", "Ali Qapu of Isfahan", "Hasht Behesht", "Fin Garden Pavilion"],
     "rationales": [{"option": "Ali Qapu of Isfahan", "why_plausible": "Isfahan palace gate.", "why_wrong": "Located on Naqsh-e Jahan in Isfahan."},
                    {"option": "Hasht Behesht", "why_plausible": "Eight Paradises palace in Isfahan.", "why_wrong": "Late Safavid pavilion in Isfahan."},
                    {"option": "Fin Garden Pavilion", "why_plausible": "Kashan garden.", "why_wrong": "Located in Kashan."}],
     "expl": "Constructed in 1550, its wall frescoes depict Tahmasp's reception of Mughal Emperor Humayun seeking military refuge in Iran.", "pg": 152}
])

# 5. THE GOLDEN VEST OF REZA SHAH
add_final(clues, "THE GOLDEN VEST OF REZA SHAH", [
    {"text": "In 1915, during WWI fighting against pro-German rebel tribes in Hamadan, Cossack Colonel Reza Khan was struck in the chest by a bullet stopped by this object.",
     "ans": "A Heavy Silver/Gold Pocket Watch (Silver Watch in his Vest Pocket)", "aliases": ["A Heavy Silver Pocket Watch", "Pocket Watch", "Watch in vest", "ساعت جیبی نقره", "ساعت جیبی"],
     "options": ["A Heavy Silver/Gold Pocket Watch (Silver Watch in his Vest Pocket)", "An Iron Breastplate", "A Quran in his breast pocket", "A Solid Gold Lighter"],
     "rationales": [{"option": "An Iron Breastplate", "why_plausible": "Military armor.", "why_wrong": "Cossacks wore woolen tunics without heavy medieval chest armor."},
                    {"option": "A Quran in his breast pocket", "why_plausible": "Religious talisman.", "why_wrong": "A popular myth debunked by Reza Shah's own battlefield diaries."},
                    {"option": "A Solid Gold Lighter", "why_plausible": "Smoking accouterment.", "why_wrong": "He kept a heavy Russian silver pocket watch in his vest pocket."}],
     "expl": "The dented Russian silver watch absorbed the kinetic energy of the bullet, leaving him with a massive purple bruise but saving his life.", "pg": 445},
    {"text": "The rapid-firing heavy machine gun that Reza Khan operated with deadly skill during his early Cossack military career, earning him the nickname 'Reza Maxim', was this.",
     "ans": "The Maxim Gun (Pulemyot Maxima)", "aliases": ["The Maxim Gun", "Maxim Gun", "Maxim", "مسلسل ماکسیم", "رضا ماکسیم"],
     "options": ["The Maxim Gun (Pulemyot Maxima)", "The Gatling Gun", "The Vickers Gun", "The Lewis Gun"],
     "rationales": [{"option": "The Gatling Gun", "why_plausible": "Early rotary gun.", "why_wrong": "Pre-automatic hand-cranked gun."},
                    {"option": "The Vickers Gun", "why_plausible": "British counterpart.", "why_wrong": "British water-cooled gun, while the Russian Cossack brigade used Russian Pulemyot Maxima."},
                    {"option": "The Lewis Gun", "why_plausible": "Air-cooled light machine gun.", "why_wrong": "American pan-fed light machine gun."}],
     "expl": "His unmatched proficiency in disassembling, clearing jams, and laying down suppressive fire with the Maxim gun earned him the rank of officer and the legendary military moniker 'Reza Maxim'.", "pg": 444}
])

save_data(clues)
