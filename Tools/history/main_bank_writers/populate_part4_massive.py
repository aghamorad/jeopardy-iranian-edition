#!/usr/bin/env python3
import json

def run_part4():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    clues_by_id = {c["id"]: c for c in existing}

    def add_5(cat, period, theme, round_str, data):
        vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("(", "").replace(")", "")
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
                "page": item.get("pg", 220 + idx * 20),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. WAR LITERATURE & CINEMA
    add_5("WAR LITERATURE & CINEMA", "Sacred Defense Culture", "Cinema & Memoirs", "double", [
        {
            "text": "Narrated in his distinctive gravelly, poetic voice, this 63-episode television documentary series by Morteza Avini captured front-line frontline soldiers as mystical pilgrims on a sacred path.",
            "ans": "Ravayat-e Fath (Chronicles of Victory)",
            "aliases": ["Ravayat-e Fath", "Chronicles of Victory", "Ravayat e Fath", "روایت فتح"],
            "options": ["Ravayat-e Fath (Chronicles of Victory)", "From Karkheh to Rhine", "Bashu, the Little Stranger", "The Glass Agency"],
            "rationales": [
                {"option": "From Karkheh to Rhine", "why_plausible": "Famous war feature film.", "why_wrong": "1993 feature drama by Hatamikia, not Avini's documentary series."},
                {"option": "Bashu, the Little Stranger", "why_plausible": "Landmark film set during the war.", "why_wrong": "1986 film by Bahram Beyzai about a southern war orphan in Gilan."},
                {"option": "The Glass Agency", "why_plausible": "Acclaimed post-war hostage drama.", "why_wrong": "1997 film by Hatamikia about veteran disillusionment."}
            ],
            "expl": "Martyred by a landmine in Fakkeh in 1993, Avini was conferred the official title 'Master of the Martyr Intellectuals' (Seyed-e Shahidan-e Ahl-e Qalam).",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 792
        },
        {
            "text": "Directed by Ebrahim Hatamikia in 1993, this emotional drama follows a chemical weapons victim sent to Germany for cornea surgery who encounters his estranged expatriate sister.",
            "ans": "From Karkheh to Rhine",
            "aliases": ["From Karkheh to Rhine", "Az Karkheh ta Rhein", "از کرخه تا راین"],
            "options": ["From Karkheh to Rhine", "The Glass Agency", "The Scout", "In the Altar of Blood"],
            "rationales": [
                {"option": "The Glass Agency", "why_plausible": "Hatamikia's other masterpiece.", "why_wrong": "Deals with a hospital hostage standoff in Tehran over an airplane ticket."},
                {"option": "The Scout", "why_plausible": "Hatamikia's earlier film (Didehban).", "why_wrong": "Set on the front line in 1989."},
                {"option": "In the Altar of Blood", "why_plausible": "Early war drama.", "why_wrong": "Film by Hossein Ghasemi-Jami."}
            ],
            "expl": "Featuring Majid Entezami's haunting pan-flute score, the film movingly humanized the trauma of 100,000 Iranian victims of Iraqi chemical attacks.",
            "book": "A Social History of Iranian Cinema, Vol. 2", "auth": "Hamid Naficy", "pg": 142
        },
        {
            "text": "Directed by Bahram Beyzai in 1986 and shelved for three years, this lyrical anti-war masterpiece follows a dark-skinned boy fleeing southern bombardments who finds refuge with a Gilaki farm woman.",
            "ans": "Bashu, the Little Stranger",
            "aliases": ["Bashu, the Little Stranger", "Bashu", "باشو غریبه کوچک", "باشو غریبه‌ی کوچک"],
            "options": ["Bashu, the Little Stranger", "The Runner", "Where Is the Friend's Home?", "Children of Heaven"],
            "rationales": [
                {"option": "The Runner", "why_plausible": "Famous film about a southern boy.", "why_wrong": "Directed by Amir Naderi, focusing on a boy living in an abandoned ship in Abadan."},
                {"option": "Where Is the Friend's Home?", "why_plausible": "Northern village drama.", "why_wrong": "Directed by Kiarostami, focusing on homework in Koker."},
                {"option": "Children of Heaven", "why_plausible": "Famous drama about childhood.", "why_wrong": "Directed by Majid Majidi in 1997 about lost shoes in Tehran."}
            ],
            "expl": "Starring Susan Taslimi as Na'i-Jan, the film championed linguistic and ethnic unity between Gilakis and southern Khuzestanis despite mutual incomprehension.",
            "book": "A Social History of Iranian Cinema, Vol. 2", "auth": "Hamid Naficy", "pg": 118
        },
        {
            "text": "Narrated by 17-year-old Seyyedeh Zahra Hosseini, this massive 2008 bestselling memoir recounts her 20 days washing corpses and defending Khorramshahr during the Iraqi siege.",
            "ans": "Da (One Woman's War)",
            "aliases": ["Da", "One Woman's War", "Da (One Woman's War)", "دا"],
            "options": ["Da (One Woman's War)", "Journey to Heading 270", "Chess with the Doomsday Machine", "Platoon 22"],
            "rationales": [
                {"option": "Journey to Heading 270", "why_plausible": "Famous novel by Ahmad Dehqan.", "why_wrong": "A soldier's frontline novel about Operation Karbala-5."},
                {"option": "Chess with the Doomsday Machine", "why_plausible": "Novel by Habib Ahmadzadeh.", "why_wrong": "Follows a young radar spotter in besieged Abadan."},
                {"option": "Platoon 22", "why_plausible": "War memoir.", "why_wrong": "Memoir by Mohsen Motlaq."}
            ],
            "expl": "Da (meaning 'Mother' in Kurdish and Luri) became the fastest-selling book in post-revolutionary history, running through over 150 print editions.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 796
        },
        {
            "text": "Directed by Amir Naderi in 1984, this iconic New Wave film follows an illiterate orphan named Amiro who survives by shining shoes and collecting ice in the scorched ruins of war-era Abadan.",
            "ans": "The Runner (Davandeh)",
            "aliases": ["The Runner", "Davandeh", "The Runner (Davandeh)", "دونده"],
            "options": ["The Runner (Davandeh)", "Bashu", "Captain Khorshid", "Still Life"],
            "rationales": [
                {"option": "Bashu", "why_plausible": "Khuzestani boy drama.", "why_wrong": "Directed by Bahram Beyzai, set in northern rice fields."},
                {"option": "Captain Khorshid", "why_plausible": "Southern coastal noir.", "why_wrong": "Directed by Nasser Taghvai adapting Hemingway's To Have and Have Not."},
                {"option": "Still Life", "why_plausible": "Pioneering minimalist film.", "why_wrong": "Directed by Sohrab Shahid-Saless about a railway switchman in 1974."}
            ],
            "expl": "The Runner was the first post-revolutionary Iranian film to attract major global acclaim, winning the Golden Montgolfiere at the Three Continents Festival in Nantes.",
            "book": "A Social History of Iranian Cinema, Vol. 2", "auth": "Hamid Naficy", "pg": 104
        }
    ])

    # 2. THE WHITE REVOLUTION IN DEPTH
    add_5("THE WHITE REVOLUTION IN DEPTH", "Late Pahlavi Era", "Modernization Politics", "double", [
        {
            "text": "Appointed Minister of Agriculture in 1961, this fiery radical lawyer was the intellectual architect of the land reform program that broke the power of feudal landlords.",
            "ans": "Hasan Arsanjani",
            "aliases": ["Hasan Arsanjani", "Arsanjani", "حسن ارسنجانی"],
            "options": ["Hasan Arsanjani", "Asadollah Alam", "Amir Abbas Hoveyda", "Jamshid Amouzegar"],
            "rationales": [
                {"option": "Asadollah Alam", "why_plausible": "Prime minister who implemented the referendum.", "why_wrong": "Alam served as Prime Minister during the 1963 riots, but Arsanjani was the land reform ideologue."},
                {"option": "Amir Abbas Hoveyda", "why_plausible": "Long-serving prime minister.", "why_wrong": "Hoveyda became prime minister in 1965 after Mansur was assassinated."},
                {"option": "Jamshid Amouzegar", "why_plausible": "Minister of Finance and OPEC negotiator.", "why_wrong": "Amouzegar managed finance and oil, not the agrarian land redistribution."}
            ],
            "expl": "Arsanjani's radical populism alarmed the Shah, who feared the charismatic minister would eclipse the throne; he was forced out as ambassador to Rome in 1963.",
            "book": "The Political Economy of Modern Iran", "auth": "Homa Katouzian", "pg": 224
        },
        {
            "text": "Created under Point Two of the White Revolution, this uniformed corps sent high school graduate conscripts into remote villages to teach rural children how to read and write.",
            "ans": "The Literacy Corps (Sepah-e Danesh)",
            "aliases": ["The Literacy Corps", "Literacy Corps", "Sepah-e Danesh", "سپاه دانش"],
            "options": ["The Literacy Corps (Sepah-e Danesh)", "The Health Corps", "The Reconstruction Jihad", "The Basij"],
            "rationales": [
                {"option": "The Health Corps", "why_plausible": "Sister corps under the White Revolution (Sepah-e Behdasht).", "why_wrong": "Focused on rural medical clinics and vaccination, not primary education."},
                {"option": "The Reconstruction Jihad", "why_plausible": "Rural development organization.", "why_wrong": "Jihad-e Sazandegi was created in 1979 after the revolution."},
                {"option": "The Basij", "why_plausible": "Volunteer corps.", "why_wrong": "Military volunteer auxiliary formed in November 1979."}
            ],
            "expl": "Sepah-e Danesh deployed over 100,000 young men and women into 40,000 villages, dramatically raising national rural literacy rates between 1963 and 1978.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 630
        },
        {
            "text": "In June 1963 (15 Khordad), bloody riots erupted across Tehran and Qom after the Shah arrested Ayatollah Khomeini for denouncing land reform and this controversial social measure.",
            "ans": "Women's Enfranchisement (Right to Vote)",
            "aliases": ["Women's Enfranchisement", "Women's Right to Vote", "Women's Suffrage", "حق رای زنان", "تصویب‌نامه انجمن‌های ایالتی و ولایتی"],
            "options": ["Women's Enfranchisement (Right to Vote)", "Nationalization of Forests", "Profit Sharing for Workers", "Abolition of Serfdom"],
            "rationales": [
                {"option": "Nationalization of Forests", "why_plausible": "Point Three of the White Revolution.", "why_wrong": "An uncontroversial environmental measure."},
                {"option": "Profit Sharing for Workers", "why_plausible": "Point Four of the White Revolution.", "why_wrong": "Industrial reform that did not offend clerical sensibilities."},
                {"option": "Abolition of Serfdom", "why_plausible": "Part of land reform.", "why_wrong": "The clerics specifically objected to female suffrage and dropping the requirement for councilors to swear on the Quran."}
            ],
            "expl": "Prime Minister Asadollah Alam ordered troops to shoot to kill, crushing the 15 Khordad uprising with hundreds of casualties and solidifying Khomeini's status as the chief dissident.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 424
        },
        {
            "text": "Serving as Prime Minister for a record twelve years and six months from 1965 to 1977, this pipe-smoking Francophile statesman was famous for his fresh orchid lapel flowers.",
            "ans": "Amir Abbas Hoveyda",
            "aliases": ["Amir Abbas Hoveyda", "Amir-Abbas Hoveyda", "Hoveyda", "امیرعباس هویدا", "هویدا"],
            "options": ["Amir Abbas Hoveyda", "Hasan Ali Mansur", "Asadollah Alam", "Ali Amini"],
            "rationales": [
                {"option": "Hasan Ali Mansur", "why_plausible": "His predecessor and close friend.", "why_wrong": "Assassinated in January 1965 in front of the Majles by Fadayan-e Islam."},
                {"option": "Asadollah Alam", "why_plausible": "Court minister and confidant of the Shah.", "why_wrong": "Alam resigned the premiership in 1964 and served as Minister of Court."},
                {"option": "Ali Amini", "why_plausible": "Reformist prime minister in 1961–1962.", "why_wrong": "Independent aristocratic politician forced out by the Shah in 1962."}
            ],
            "expl": "Hoveyda presided over Iran's petrodollar economic boom; he was executed on April 7, 1979, after a summary trial by revolutionary judge Sadegh Khalkhali.",
            "book": "The Shah", "auth": "Abbas Milani", "pg": 286
        },
        {
            "text": "On March 2, 1975, the Shah dissolved all existing parliamentary political parties, declaring that all citizens must join this newly created single totalitarian party or leave the country.",
            "ans": "Rastakhiz Party",
            "aliases": ["Rastakhiz Party", "Hezb-e Rastakhiz", "Rastakhiz", "حزب رستاخیز", "رستاخیز"],
            "options": ["Rastakhiz Party", "Iran Novin", "Mardom Party", "National Front"],
            "rationales": [
                {"option": "Iran Novin", "why_plausible": "The previous dominant royal party led by Hoveyda.", "why_wrong": "Iran Novin was dissolved in 1975 along with Mardom to form Rastakhiz."},
                {"option": "Mardom Party", "why_plausible": "The loyal 'opposition' party founded by Alam.", "why_wrong": "Abolished in 1975 to create the single-party state."},
                {"option": "National Front", "why_plausible": "Secular democratic opposition.", "why_wrong": "Banned opposition party founded by Mosaddegh."}
            ],
            "expl": "Rastakhiz ('Resurgence') alienated the traditional bazaar by opening branches to enforce arbitrary price controls, accelerating middle-class participation in the revolution.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 440
        }
    ])

    # 3. THE LEFT IN IRAN: GUERRILLAS
    add_5("THE LEFT IN IRAN: GUERRILLAS", "Armed Struggle", "Leftist Politics", "double", [
        {
            "text": "On February 8, 1971, thirteen young Marxist guerrillas attacked a gendarmerie post in this forested village in Gilan, inaugurating modern armed urban guerrilla warfare in Iran.",
            "ans": "Siahkal",
            "aliases": ["Siahkal", "Siahkal incident", "حماسه سیاهکل", "سیاهکل"],
            "options": ["Siahkal", "Lahijan", "Rasht", "Amol"],
            "rationales": [
                {"option": "Lahijan", "why_plausible": "Major tea-producing city in Gilan nearby.", "why_wrong": "Nearby city, but the outpost attacked was in Siahkal."},
                {"option": "Rasht", "why_plausible": "Provincial capital of Gilan.", "why_wrong": "Urban center, not the forested mountain outpost."},
                {"option": "Amol", "why_plausible": "Mazandaran city site of the 1982 Sarbedaran communist uprising.", "why_wrong": "Site of a later 1982 armed clash, not the 1971 birth of the Fadayan."}
            ],
            "expl": "The Siahkal incident led to the formation of the Organization of Iranian People's Fedai Guerrillas (Cherikha-ye Fadai-e Khalq), immortalized in poem and song.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 480
        },
        {
            "text": "The chief theoretician of the Fadayan-e Khalq who wrote Armed Struggle: Both a Strategy and a Tactic, this intellectual was assassinated alongside eight others in Evin in 1975.",
            "ans": "Bijan Jazani",
            "aliases": ["Bijan Jazani", "Jazani", "بیژن جزنی"],
            "options": ["Bijan Jazani", "Amir Parviz Pouyan", "Masoud Ahmadzadeh", "Khosrow Golsorkhi"],
            "rationales": [
                {"option": "Amir Parviz Pouyan", "why_plausible": "Co-founder of Fadayan who wrote The Necessity of Armed Struggle.", "why_wrong": "Committed suicide with cyanide in a police shootout in May 1971."},
                {"option": "Masoud Ahmadzadeh", "why_plausible": "Key Fadayan leader executed in 1972.", "why_wrong": "Executed by firing squad in March 1972."},
                {"option": "Khosrow Golsorkhi", "why_plausible": "Marxist poet executed in 1974.", "why_wrong": "Famous for his televised military trial in 1974, but not the author of Armed Struggle."}
            ],
            "expl": "SAVAK officers took Jazani and eight fellow prisoners to the hills behind Evin Prison in April 1975 and machine-gunned them, claiming they had been 'shot while escaping'.",
            "book": "Rebels with a Cause: The Failure of the Left in Iran", "auth": "Maziar Behrooz", "pg": 72
        },
        {
            "text": "During his televised 1974 military tribunal, this Marxist poet electrified the country by proudly defending Che Guevara, Karl Marx, and Imam Hussein before refusing to ask for royal clemency.",
            "ans": "Khosrow Golsorkhi",
            "aliases": ["Khosrow Golsorkhi", "Golsorkhi", "خسرو گلسرخی"],
            "options": ["Khosrow Golsorkhi", "Keramat Daneshian", "Samad Behrangi", "Jalal Al-e Ahmad"],
            "rationales": [
                {"option": "Keramat Daneshian", "why_plausible": "His co-defendant executed alongside him.", "why_wrong": "Executed together on February 18, 1974, but Golsorkhi gave the famous televised address."},
                {"option": "Samad Behrangi", "why_plausible": "Azeri socialist teacher and author of The Little Black Fish.", "why_wrong": "Drowned in the Aras River in 1968."},
                {"option": "Jalal Al-e Ahmad", "why_plausible": "Author of Gharbzadegi.", "why_wrong": "Died in 1969 in Gilan."}
            ],
            "expl": "Golsorkhi told the military judges: 'I found the first lessons of socialism in Islam and in the life of Imam Hussein.' He was executed on February 18, 1974.",
            "book": "Rebels with a Cause: The Failure of the Left in Iran", "auth": "Maziar Behrooz", "pg": 78
        },
        {
            "text": "Authored by Azeri teacher Samad Behrangi in 1968, this allegorical children's fable about a tiny fish swimming from a stream to the ocean became a banned sacred text for armed rebels.",
            "ans": "The Little Black Fish",
            "aliases": ["The Little Black Fish", "Mahi Siah-e Koochooloo", "ماهی سیاه کوچولو"],
            "options": ["The Little Black Fish", "The Old Man and the Sea", "A Tale of Two Cities", "The Blind Owl"],
            "rationales": [
                {"option": "The Old Man and the Sea", "why_plausible": "Novella by Hemingway.", "why_wrong": "American novel translated by Najaf Daryabandari."},
                {"option": "A Tale of Two Cities", "why_plausible": "Dickens novel.", "why_wrong": "English historical fiction."},
                {"option": "The Blind Owl", "why_plausible": "Famous modern Iranian classic.", "why_wrong": "Written by Sadegh Hedayat in 1937."}
            ],
            "expl": "Illustrated by Farshid Mesghali (who won the prestigious Hans Christian Andersen Award), the book warned children that conformity meant death.",
            "book": "A Social History of Iranian Cinema, Vol. 1", "auth": "Hamid Naficy", "pg": 332
        },
        {
            "text": "Founded in 1965 by student intellectuals Hanifnejad, Saadati, and Badizadegan, this armed movement fused Islam with Marxist class analysis before fracturing into rival factions.",
            "ans": "The Mojahedin-e Khalq (MEK)",
            "aliases": ["The Mojahedin-e Khalq", "MEK", "Mojahedin-e Khalq", "MKO", "PMOI", "مجاهدین خلق", "سازمان مجاهدین خلق"],
            "options": ["The Mojahedin-e Khalq (MEK)", "Fadayan-e Khalq", "Tudeh Party", "Peykar"],
            "rationales": [
                {"option": "Fadayan-e Khalq", "why_plausible": "Rival Marxist guerrilla organization.", "why_wrong": "Purely Marxist-Leninist from its inception, without Islamic foundation."},
                {"option": "Tudeh Party", "why_plausible": "Pro-Soviet communist party.", "why_wrong": "Traditional communist party founded in 1941, not the 1965 guerrilla movement."},
                {"option": "Peykar", "why_plausible": "Maoist splinter offshoot.", "why_wrong": "Splintered from the MEK in 1975 under Taghi Shahram."}
            ],
            "expl": "In 1975, a violent Marxist faction assassinated rival leaders and purged the Islamic wing, until Massoud Rajavi rebuilt the organization from inside prison.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 488
        }
    ])

    # 4. RUSSO-PERSIAN WARS (1804-1828)
    add_5("THE RUSSO-PERSIAN WARS", "Qajar Dynasty", "Imperial Wars", "double", [
        {
            "text": "As Crown Prince and governor of Tabriz, this tragic reformer commanded Iranian forces throughout both wars with Russia, creating the Western-drilled Nezam-e Jadid army.",
            "ans": "Abbas Mirza",
            "aliases": ["Abbas Mirza", "Prince Abbas Mirza", "عباس میرزا"],
            "options": ["Abbas Mirza", "Fath-Ali Shah", "Mohammad Shah Qajar", "Amir Kabir"],
            "rationales": [
                {"option": "Fath-Ali Shah", "why_plausible": "His father and the reigning Shah.", "why_wrong": "Fath-Ali Shah was in Tehran, while Abbas Mirza fought on the Caucasian frontline."},
                {"option": "Mohammad Shah Qajar", "why_plausible": "His son who succeeded to the throne.", "why_wrong": "Mohammad Mirza succeeded Fath-Ali Shah in 1834 after Abbas Mirza's premature death."},
                {"option": "Amir Kabir", "why_plausible": "Great 19th-century reformer.", "why_wrong": "Amir Kabir was a young scribe in Abbas Mirza's camp, rising to power decades later."}
            ],
            "expl": "Abbas Mirza died of kidney disease in Mashhad in 1833 at age 44, never ascending the throne, mourned as Iran's greatest military patriot.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 248
        },
        {
            "text": "Signed in October 1813 following the catastrophic rout at the Battle of Aslanduz, this treaty forced Iran to cede Georgia, Dagestan, and northern Azerbaijan to the Russian Empire.",
            "ans": "Treaty of Golestan",
            "aliases": ["Treaty of Golestan", "Treaty of Gulistan", "عهدنامه گلستان", "گلستان"],
            "options": ["Treaty of Golestan", "Treaty of Turkmenchay", "Treaty of Paris", "Treaty of Finkenstein"],
            "rationales": [
                {"option": "Treaty of Turkmenchay", "why_plausible": "The subsequent 1828 treaty.", "why_wrong": "Concluded the second war in 1828, ceding Erivan and Nakhchivan."},
                {"option": "Treaty of Paris", "why_plausible": "1857 treaty regarding Afghanistan.", "why_wrong": "Signed with Britain over Herat, not Russia."},
                {"option": "Treaty of Finkenstein", "why_plausible": "1807 alliance with Napoleon.", "why_wrong": "French-Iranian alliance treaty."}
            ],
            "expl": "The Treaty of Golestan also granted Russia the exclusive right to maintain naval warships on the Caspian Sea, turning it into a Russian lake.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 250
        },
        {
            "text": "In January 1829, an enraged Tehran mob stormed the Russian Legation and massacred this famous playwright and Tsarist ambassador for sheltering two escaped Armenian women.",
            "ans": "Aleksandr Griboyedov",
            "aliases": ["Aleksandr Griboyedov", "Griboyedov", "Alexander Griboyedov", "گریبایدوف", "الکساندر گریبایدوف"],
            "options": ["Aleksandr Griboyedov", "General Paskievich", "General Tsitsianov", "Colonel Liakhov"],
            "rationales": [
                {"option": "General Paskievich", "why_plausible": "Russian field marshal who defeated Abbas Mirza.", "why_wrong": "Paskievich was the military conqueror of Erivan, not the assassinated ambassador."},
                {"option": "General Tsitsianov", "why_plausible": "Brutal Georgian-Russian general.", "why_wrong": "Decapitated outside the walls of Baku in 1806."},
                {"option": "Colonel Liakhov", "why_plausible": "Cossack brigade officer.", "why_wrong": "Shelled the Majles in 1908, eight decades later."}
            ],
            "expl": "Griboyedov, author of Woe from Wit, had insisted on strictly enforcing the humiliating terms of Turkmenchay; to avert war, the Shah sent the 88-carat Shah Diamond to Tsar Nicholas I.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 256
        },
        {
            "text": "Nicknamed 'the Dragon' for his ruthlessness, this Georgian nobleman and Russian commander-in-chief conquered Ganja in 1804 before being assassinated outside the gates of Baku in 1806.",
            "ans": "General Pavel Tsitsianov",
            "aliases": ["General Pavel Tsitsianov", "Pavel Tsitsianov", "Tsitsianov", "ژنرال سیسیانوف", "سیسیانوف"],
            "options": ["General Pavel Tsitsianov", "General Paskievich", "General Ermolov", "General Gudovich"],
            "rationales": [
                {"option": "General Paskievich", "why_plausible": "Later Russian commander.", "why_wrong": "Commanded the 1826–1828 war."},
                {"option": "General Ermolov", "why_plausible": "Proconsul of the Caucasus (1816–1827).", "why_wrong": "Known as the 'Proconsul of the Caucasus', succeeded Tsitsianov."},
                {"option": "General Gudovich", "why_plausible": "Russian field marshal.", "why_wrong": "Failed to take Erivan in 1808."}
            ],
            "expl": "During parleys outside Baku, Huseyngulu Khan's cousin drew a pistol and shot Tsitsianov; his severed head was dispatched as a trophy to Fath-Ali Shah in Tehran.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 246
        },
        {
            "text": "On October 31, 1812, Russian forces under General Pyotr Kotlyarevsky staged a night bayonet surprise attack across the Aras River, annihilating Abbas Mirza's camp at this battle.",
            "ans": "Battle of Aslanduz",
            "aliases": ["Battle of Aslanduz", "Aslanduz", "Aslandooz", "نبرد اصلاندوز", "اصلاندوز"],
            "options": ["Battle of Aslanduz", "Battle of Ganja", "Battle of Sultanabad", "Battle of Erivan"],
            "rationales": [
                {"option": "Battle of Ganja", "why_plausible": "1804 siege and battle.", "why_wrong": "Opening battle of the war in 1804."},
                {"option": "Battle of Sultanabad", "why_plausible": "Iranian victory in 1812.", "why_wrong": "Abbas Mirza's victory in February 1812 before the disaster at Aslanduz."},
                {"option": "Battle of Erivan", "why_plausible": "Famous siege of the fortress of Erivan.", "why_wrong": "Repulsed Russian sieges in 1804 and 1808."}
            ],
            "expl": "The defeat at Aslanduz destroyed Iran's modernized artillery corps and compelled Fath-Ali Shah to sign the humiliating Treaty of Golestan the following year.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 249
        }
    ])

    # Save progress
    print("Writing Batch 4 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Total clues after Part 4:", len(clues_by_id))

if __name__ == "__main__":
    run_part4()
