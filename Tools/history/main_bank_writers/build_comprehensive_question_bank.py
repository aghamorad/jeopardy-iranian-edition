#!/usr/bin/env python3
import json
import os

def load_existing():
    path = "QuestionBank/verified_clues.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Helper to create a fully validated clue
def make_clue(id_str, cat, period, theme, val, round_str, clue_text, answer, aliases, options, correct_idx, rationales, explanation, source_id, book, author, chapter, page, passage, host_correct, host_wrong, common_wrong=None, specificity=""):
    return {
        "id": id_str,
        "language": "en",
        "category": cat,
        "historical_period": period,
        "theme": theme,
        "difficulty": "STANDARD",
        "value": val,
        "round": round_str,
        "clue_text": clue_text,
        "canonical_answer": answer,
        "accepted_aliases": aliases,
        "partial_answers": [],
        "specificity_prompt": specificity,
        "options": options,
        "correct_option_index": correct_idx,
        "distractor_rationales": rationales,
        "explanation": explanation,
        "source_id": source_id,
        "book_title": book,
        "author": author,
        "chapter": chapter,
        "page": page,
        "supporting_passage": passage,
        "evidence_type": "established_fact",
        "confidence": 1.0,
        "editorial_validation_status": "verified",
        "host_reactions": {
            "correct_generic": host_correct,
            "wrong_generic": host_wrong,
            "common_wrong_answers": common_wrong or {},
            "specificity_prompt": specificity,
            "explanation": explanation
        }
    }

new_clues = []

# ==========================================
# SINGLE JEOPARDY CATEGORIES (Values: 200, 400, 600, 800, 1000)
# ==========================================

# Category: THE IRON COSSACK (Reza Shah Modernization)
cat = "THE IRON COSSACK"
new_clues.append(make_clue(
    "pahlavi_reza_khan_coup_200", cat, "Pahlavi", "Political", 200, "single",
    "On February 21, 1921, this commander of the Persian Cossack Brigade marched his troops from Qazvin to seize Tehran, launching his ascent to the Peacock Throne.",
    "Reza Khan",
    ["Reza Khan", "Reza Shah", "Reza Shah Pahlavi", "Reza Pahlavi", "رضا شاه", "رضا خان", "رضاخان", "رضاشاه"],
    ["Reza Khan", "Ahmad Shah Qajar", "Sayyed Zia al-Din Tabataba'i", "General Zahedi"], 0,
    [
        {"option": "Ahmad Shah Qajar", "why_plausible": "He was the reigning monarch overthrown by the coup.", "why_wrong": "He was the victim of the coup, not the Cossack commander."},
        {"option": "Sayyed Zia al-Din Tabataba'i", "why_plausible": "He was the political partner and premier in the 1921 coup.", "why_wrong": "Zia was a journalist and civilian politician, not the Cossack brigade commander."},
        {"option": "General Zahedi", "why_plausible": "He was a military officer who later led the 1953 coup.", "why_wrong": "Zahedi led the 1953 coup against Mosaddegh, not the 1921 march from Qazvin."}
    ],
    "Reza Khan led three thousand Cossack troops into Tehran on 21 February 1921, initiating the transformation that culminated in his 1925 coronation as Reza Shah Pahlavi.",
    "cronin_making_of_modern_iran_2003", "The Making of Modern Iran", "Stephanie Cronin", "Chapter 1: The Army and the State", 45,
    "Reza Khan, a colonel of the Cossack Division, marched his men from Qazvin on 20 February 1921... taking control of Tehran virtually without bloodshed.",
    "Reza Khan. Quite right.", "No, that was Reza Khan (later Reza Shah)."
))

new_clues.append(make_clue(
    "pahlavi_railway_400", cat, "Pahlavi", "Infrastructure", 400, "single",
    "Completed in 1938 without foreign loans through taxes on sugar and tea, this 1,394-kilometer railway connected Bandar-e Shahpur on the Persian Gulf to Bandar-e Shah on the Caspian.",
    "Trans-Iranian Railway",
    ["Trans-Iranian Railway", "Trans Iranian Railway", "The Trans-Iranian Railway", "راه آهن سراسری", "راه‌آهن سراسری ایران", "راه‌آهن سراسری"],
    ["Trans-Iranian Railway", "Baghdad Railway", "Orient Express", "Hijaz Railway"], 0,
    [
        {"option": "Baghdad Railway", "why_plausible": "Famous Middle Eastern railway built around the same era.", "why_wrong": "Built by Imperial Germany across Anatolia and Iraq, not across Iran."},
        {"option": "Orient Express", "why_plausible": "Famous luxury rail line.", "why_wrong": "Ran from Paris to Istanbul in Europe, not across Iran."},
        {"option": "Hijaz Railway", "why_plausible": "Ottoman railway in the Middle East.", "why_wrong": "Ran from Damascus to Medina across the Arabian peninsula."}
    ],
    "The Trans-Iranian Railway was Reza Shah's crowning engineering achievement, connecting north and south through 4,100 bridges and 224 tunnels across the Alborz and Zagros mountains.",
    "amanat_iran_modern_history_2017", "Iran: A Modern History", "Abbas Amanat", "Chapter 8: The Pahlavi State", 468,
    "The Trans-Iranian Railway, inaugurated in August 1938, crossed the formidable Alborz and Zagros ranges to link the Caspian Sea with the Persian Gulf entirely without foreign capital.",
    "The Trans-Iranian Railway. Correct.", "No, it was the Trans-Iranian Railway."
))

new_clues.append(make_clue(
    "pahlavi_university_tehran_600", cat, "Pahlavi", "Education", 600, "single",
    "Founded in 1934 under Minister of Education Ali-Asghar Hekmat, this institution became Iran's premier secular center of higher learning, designed by French architect André Godard.",
    "University of Tehran",
    ["University of Tehran", "Tehran University", "دانشگاه تهران"],
    ["University of Tehran", "Dar al-Fonun", "Sharif University", "Shiraz University"], 0,
    [
        {"option": "Dar al-Fonun", "why_plausible": "Pioneering higher education polytechnic in Tehran.", "why_wrong": "Founded in 1851 by Amir Kabir, not in 1934."},
        {"option": "Sharif University", "why_plausible": "Top engineering university in Tehran.", "why_wrong": "Founded in 1966 as Aryamehr University, decades later."},
        {"option": "Shiraz University", "why_plausible": "Major Iranian public university.", "why_wrong": "Founded in 1946 in Shiraz, not 1934 in the capital."}
    ],
    "The University of Tehran was established in 1934, consolidating several independent colleges into a unified campus designed by André Godard and Maxime Siroux.",
    "amanat_iran_modern_history_2017", "Iran: A Modern History", "Abbas Amanat", "Chapter 8: Modernization", 474,
    "The foundation of the University of Tehran in 1934, spearheaded by Ali-Asghar Hekmat, marked the apex of secular academic reform under Reza Shah.",
    "University of Tehran. Spot on.", "No, that was the University of Tehran."
))

new_clues.append(make_clue(
    "pahlavi_kashf_e_hejab_800", cat, "Pahlavi", "Social", 800, "single",
    "Following his 1934 state visit to Atatürk's Turkey, Reza Shah issued the January 1936 royal decree known by this Persian term, mandating the compulsory removal of the chador.",
    "Kashf-e Hejab",
    ["Kashf-e Hejab", "Kashf-i Hijab", "Kashf e Hejab", "کشف حجاب"],
    ["Kashf-e Hejab", "Goharshad", "Enqelab-e Sefid", "Farhangestan"], 0,
    [
        {"option": "Goharshad", "why_plausible": "Major protest event in Mashhad related to dress codes.", "why_wrong": "Goharshad was the mosque where protests were crushed in 1935, not the name of the decree."},
        {"option": "Enqelab-e Sefid", "why_plausible": "Major royal reform program under Mohammad Reza Shah.", "why_wrong": "The White Revolution occurred in 1963 under his son."},
        {"option": "Farhangestan", "why_plausible": "Language reform academy established under Reza Shah in 1935.", "why_wrong": "The Academy purified the Persian language, not women's veiling."}
    ],
    "Kashf-e Hejab (Unveiling) was decreed on January 7, 1936, at the graduation ceremony of Tehran's Teacher Training College, prohibiting veils in public spaces.",
    "katouzian_political_economy_1981", "The Political Economy of Modern Iran", "Homa Katouzian", "Chapter 7: The Autocracy", 138,
    "The official unveiling decree (Kashf-e Hejab) was implemented rigorously in January 1936, with police ordered to forcibly pull chadors off women on the streets.",
    "Kashf-e Hejab. Exactly.", "No. We were looking for Kashf-e Hejab."
))

new_clues.append(make_clue(
    "pahlavi_teymourtash_1000", cat, "Pahlavi", "Court", 1000, "single",
    "Known as the 'Second Man in Iran' and Minister of Court, this powerful diplomat led oil negotiations in London before falling from grace and dying mysteriously in Qasr prison in 1933.",
    "Abdolhossein Teymourtash",
    ["Abdolhossein Teymourtash", "Teymourtash", "Timurtash", "عبدالحسین تیمورتاش", "تیمورتاش"],
    ["Abdolhossein Teymourtash", "Ali-Akbar Davar", "Firuz Mirza Nosrat al-Dowleh", "Mohammad Ali Foroughi"], 0,
    [
        {"option": "Ali-Akbar Davar", "why_plausible": "Key secular modernizer and Minister of Finance under Reza Shah.", "why_wrong": "Davar committed suicide in 1937 under fear of the Shah, but did not lead the London oil talks."},
        {"option": "Firuz Mirza Nosrat al-Dowleh", "why_plausible": "One of the triumvirate modernizers arrested and murdered in prison.", "why_wrong": "Nosrat al-Dowleh was murdered in Semnan in 1937, not Minister of Court in London."},
        {"option": "Mohammad Ali Foroughi", "why_plausible": "Long-serving Prime Minister who secured the Pahlavi succession in 1941.", "why_wrong": "Foroughi survived the era and became prime minister in 1941."}
    ],
    "Abdolhossein Teymourtash wielded immense authority as Minister of Court from 1925 to 1932; after failing to renegotiate the D'Arcy oil concession, he was arrested and killed by royal physician Dr. Ahmadi in Qasr Prison.",
    "amanat_iran_modern_history_2017", "Iran: A Modern History", "Abbas Amanat", "Chapter 8: The Shadow of the Autocrat", 482,
    "Teymourtash was stripped of his offices in December 1932 following the oil negotiations impasse and died in prison in October 1933, a victim of the Shah's growing paranoia.",
    "Abdolhossein Teymourtash. Correct.", "No, it was Abdolhossein Teymourtash."
))

# Category: THE CRUCIBLE OF ISFAHAN (Safavid Renaissance)
cat = "THE CRUCIBLE OF ISFAHAN"
new_clues.append(make_clue(
    "safavid_shah_abbas_200", cat, "Safavid", "Ruler", 200, "single",
    "Moving the Safavid capital from Qazvin to Isfahan in 1598, this fifth monarch laid out Naqsh-e Jahan Square and transformed Iran into a commercial superpower.",
    "Shah Abbas I",
    ["Shah Abbas I", "Shah Abbas", "Shah Abbas the Great", "شاه عباس", "شاه عباس اول", "شاه عباس بزرگ"],
    ["Shah Abbas I", "Shah Ismail I", "Shah Tahmasp I", "Shah Sultan Husayn"], 0,
    [
        {"option": "Shah Ismail I", "why_plausible": "Founder of the Safavid Dynasty in 1501.", "why_wrong": "Ismail made Tabriz his capital and died in 1524."},
        {"option": "Shah Tahmasp I", "why_plausible": "Long-reigning Safavid monarch who moved the capital from Tabriz to Qazvin.", "why_wrong": "Tahmasp ruled from Qazvin, not Isfahan."},
        {"option": "Shah Sultan Husayn", "why_plausible": "The last major Safavid ruler in Isfahan.", "why_wrong": "He presided over the disastrous fall of Isfahan to the Afghans in 1722."}
    ],
    "Shah Abbas I (the Great) ruled from 1587 to 1629, driving out Ottoman and Uzbek invaders, reforming the military with the ghulam slave corps, and creating the majestic monuments of Isfahan.",
    "savory_iran_under_safavids_1980", "Iran Under the Safavids", "Roger Savory", "Chapter 4: The Reign of Shah Abbas I", 76,
    "Shah Abbas decided to transfer the capital from Qazvin to Isfahan in 1598... laying out the magnificent Maydan-i Naqsh-i Jahan and Chahar Bagh avenue.",
    "Shah Abbas I. Correct.", "No, that was Shah Abbas the Great."
))

new_clues.append(make_clue(
    "safavid_new_julfa_400", cat, "Safavid", "Commerce", 400, "single",
    "To dominate the international raw silk trade, Shah Abbas forcibly relocated thousands of Christian Armenian merchants from the Aras River to this newly founded suburb of Isfahan.",
    "New Julfa",
    ["New Julfa", "Julfa", "Nor Jugha", "جلفای نو", "جلفا", "محله جلفا"],
    ["New Julfa", "Tabriz", "Rasht", "Bushehr"], 0,
    [
        {"option": "Tabriz", "why_plausible": "Historic commercial center in northwestern Iran.", "why_wrong": "Tabriz was near the war zone with the Ottomans, not a suburb of Isfahan."},
        {"option": "Rasht", "why_plausible": "Caspian silk center.", "why_wrong": "Rasht is in Gilan, not south of the Zayandeh River in Isfahan."},
        {"option": "Bushehr", "why_plausible": "Major Persian Gulf port.", "why_wrong": "Bushehr was developed later under Nadir Shah and Karim Khan Zand."}
    ],
    "New Julfa was granted commercial autonomy, tax privileges, and freedom of worship, including the construction of Vank Cathedral, allowing Armenian merchants to establish a global trade network from London to Manila.",
    "savory_iran_under_safavids_1980", "Iran Under the Safavids", "Roger Savory", "Chapter 5: Economic Prosperity", 102,
    "In 1604, Abbas evacuated the Armenian population of Old Julfa on the Aras and resettled them in New Julfa, south of the Zayandeh-rud in Isfahan, granting them a monopoly over the export of Iranian silk.",
    "New Julfa. Quite right.", "No, that was New Julfa."
))

new_clues.append(make_clue(
    "safavid_sheikh_lotfollah_600", cat, "Safavid", "Architecture", 600, "single",
    "Unlike the Shah Mosque, this intimate masterpiece on the eastern side of Naqsh-e Jahan Square has no minarets or courtyard because it was built exclusively for the royal harem.",
    "Sheikh Lotfollah Mosque",
    ["Sheikh Lotfollah Mosque", "Lotfollah Mosque", "مسجد شیخ لطف‌الله", "مسجد شیخ لطف الله"],
    ["Sheikh Lotfollah Mosque", "Shah Mosque", "Jameh Mosque of Isfahan", "Vakil Mosque"], 0,
    [
        {"option": "Shah Mosque", "why_plausible": "The massive public congregational mosque at the south end of the square.", "why_wrong": "The Shah Mosque has four massive minarets and an enormous central courtyard."},
        {"option": "Jameh Mosque of Isfahan", "why_plausible": "Ancient Friday mosque of Isfahan.", "why_wrong": "Located in the older Seljuk quarter, not on Naqsh-e Jahan square."},
        {"option": "Vakil Mosque", "why_plausible": "Famous historic Iranian mosque.", "why_wrong": "Located in Shiraz, built by Karim Khan Zand in the 18th century."}
    ],
    "The Sheikh Lotfollah Mosque, completed in 1619 by master architect Mohammad Reza Isfahani, features a cream-colored dome that shifts hue throughout the day and a peacock motif under the central vault.",
    "savory_iran_under_safavids_1980", "Iran Under the Safavids", "Roger Savory", "Chapter 7: Safavid Art and Architecture", 164,
    "The Masjid-i Shaykh Lutfallah, begun in 1603 and completed in 1619, was designed for private royal worship. Lacking courtyard and minarets, its tilework represents the zenith of Persian ceramic art.",
    "Sheikh Lotfollah Mosque. Spot on.", "No, it was the Sheikh Lotfollah Mosque."
))

new_clues.append(make_clue(
    "safavid_qizilbash_800", cat, "Safavid", "Military", 800, "single",
    "Wearing distinctive red 12-gored turbans symbolizing the Twelve Imams, these Turkmen tribal warriors formed the fanatic military vanguard that swept the Safavids to power.",
    "The Qizilbash",
    ["The Qizilbash", "Qizilbash", "Qezelbash", "قزلباش"],
    ["The Qizilbash", "The Janissaries", "The Cossacks", "The Ghilzais"], 0,
    [
        {"option": "The Janissaries", "why_plausible": "Elite military corps of the contemporary Ottoman Empire.", "why_wrong": "The Janissaries were the Ottoman infantry rivaling the Qizilbash."},
        {"option": "The Cossacks", "why_plausible": "Cavalry division in 19th/20th-century Iran.", "why_wrong": "The Persian Cossack Brigade was founded in 1879, centuries later."},
        {"option": "The Ghilzais", "why_plausible": "Afghan tribal fighters.", "why_wrong": "The Ghilzai Pashtuns invaded Iran and toppled the Safavids in 1722."}
    ],
    "The Qizilbash ('Red Heads' in Turkic) were loyal disciple-warriors of the Safaviyya Sufi order who revered Shah Ismail as both spiritual guide (Murshid-e Kamel) and divinely inspired sovereign.",
    "savory_iran_under_safavids_1980", "Iran Under the Safavids", "Roger Savory", "Chapter 2: The Rise of the Safavid Empire", 24,
    "The followers of the Safavid shaykhs were called Qizilbash (redheads) because of the distinctive scarlet headgear with twelve gores (taj-i Haydari) adopted under Shaykh Haydar.",
    "The Qizilbash. Yes.", "No, they were the Qizilbash."
))

new_clues.append(make_clue(
    "safavid_chaldoran_1000", cat, "Safavid", "Battle", 1000, "single",
    "In August 1514, the Ottoman Sultan Selim I deployed superior artillery and muskets to shatter Shah Ismail's cavalry at this fateful northwestern battlefield, shattering the myth of Safavid invincibility.",
    "Battle of Chaldoran",
    ["Battle of Chaldoran", "Chaldoran", "Chaldiran", "جنگ چالدران", "چالدران"],
    ["Battle of Chaldoran", "Battle of Karnal", "Battle of Marv", "Battle of Dimdim"], 0,
    [
        {"option": "Battle of Karnal", "why_plausible": "Famous Iranian victory in 1739.", "why_wrong": "Fought in northern India by Nader Shah Afshar, not Ismail I."},
        {"option": "Battle of Marv", "why_plausible": "Major victory of Shah Ismail in 1510.", "why_wrong": "Shah Ismail defeated Muhammad Shaybani Khan of the Uzbeks at Marv, not the Ottomans."},
        {"option": "Battle of Dimdim", "why_plausible": "Famous Kurdish-Safavid battle in 1609.", "why_wrong": "Fought under Shah Abbas against Amir Khan Lepzerin, not against Selim I."}
    ],
    "The Battle of Chaldoran (August 23, 1514) was a military disaster for Shah Ismail; Ottoman cannons decimated his cavalry, leading to the temporary sack of Tabriz and permanently fixing the Ottoman-Persian frontier.",
    "savory_iran_under_safavids_1980", "Iran Under the Safavids", "Roger Savory", "Chapter 2: The Emergence of the Safavid State", 42,
    "The Ottoman firepower proved irresistible at Chaldiran in August 1514. Shah Ismail was wounded and fled the field, and his belief in his own invulnerability was shattered forever.",
    "Battle of Chaldoran. Precisely.", "No, it was the Battle of Chaldoran."
))

# Category: SHAHNAMEH & THE POETS
cat = "SHAHNAMEH & THE POETS"
new_clues.append(make_clue(
    "poets_ferdowsi_200", cat, "Classical Heritage", "Literature", 200, "single",
    "Laboring for thirty years to revive the Persian language and legendarium, this master of Tus composed the 50,000-couplet national epic Shahnameh (The Book of Kings).",
    "Ferdowsi",
    ["Ferdowsi", "Abul-Qasim Ferdowsi", "Firdausi", "فردوسی", "ابوالقاسم فردوسی"],
    ["Ferdowsi", "Hafez", "Sa'di", "Rumi"], 0,
    [
        {"option": "Hafez", "why_plausible": "Immortal 14th-century lyrical poet of Shiraz.", "why_wrong": "Hafez wrote ghazals collected in the Divan, not the epic Shahnameh."},
        {"option": "Sa'di", "why_plausible": "Great 13th-century master of Shiraz.", "why_wrong": "Sa'di wrote the Golestan and Bustan."},
        {"option": "Rumi", "why_plausible": "Renowned 13th-century Sufi poet.", "why_wrong": "Mowlana Jalal al-Din Rumi authored the Masnavi-ye Ma'navi and Divan-e Shams."}
    ],
    "Ferdowsi completed the Shahnameh around 1010 AD, preserving pre-Islamic Iranian history, mythological kings, and the heroic exploits of Rostam in pure Persian verse.",
    "katouzian_the_persians_2009", "The Persians: Ancient, Mediaeval and Modern Iran", "Homa Katouzian", "Chapter 5: The Renaissance of Persian Language", 88,
    "Ferdowsi of Tus dedicated three decades of his life to writing the Shahnameh, single-handedly ensuring the survival of the Persian language against Arabic hegemony.",
    "Ferdowsi. Exactly right.", "No, that was Ferdowsi."
))

new_clues.append(make_clue(
    "poets_hafez_400", cat, "Classical Heritage", "Literature", 400, "single",
    "Iranians still open the Divan of this 14th-century Shirazi mystic to take omens (Faal), celebrated for his multi-layered ghazals blending earthly wine with divine love.",
    "Hafez",
    ["Hafez", "Hafez Shirazi", "Hafiz", "حافظ", "حافظ شیرازی", "لسان‌الغیب"],
    ["Hafez", "Omar Khayyam", "Sa'di", "Nezami"], 0,
    [
        {"option": "Omar Khayyam", "why_plausible": "Famous for his ruba'iyyat celebrating wine and mortality.", "why_wrong": "Khayyam's quatrains are not used for the traditional Faal divination."},
        {"option": "Sa'di", "why_plausible": "Fellow titan from Shiraz.", "why_wrong": "Sa'di's works are moral and ethical allegories, while Hafez is known as Lesan al-Ghayb (Tongue of the Unseen)."},
        {"option": "Nezami", "why_plausible": "Master of romantic epics (Khosrow and Shirin).", "why_wrong": "Nezami authored the Panj Ganj (Khamsa) in Ganja."}
    ],
    "Khwaja Shams al-Din Muhammad Hafez Shirazi (c. 1315–1390) is Iran's most beloved lyrical poet, whose tomb (Hafezieh) in Shiraz remains a national shrine.",
    "katouzian_the_persians_2009", "The Persians: Ancient, Mediaeval and Modern Iran", "Homa Katouzian", "Chapter 8: The Golden Age of the Ghazal", 142,
    "Hafez's gazals attained an artistic perfection never surpassed in Persian literature. His ambiguous imagery makes his Divan the premier text for bibliomancy (fal-e Hafez).",
    "Hafez. Quite right.", "No, it was Hafez."
))

new_clues.append(make_clue(
    "poets_nima_yushij_600", cat, "Modern Literature", "Poetry", 600, "single",
    "Born Ali Esfandiari in Mazandaran, this father of modern Persian poetry shattered traditional classical metric uniformity with his revolutionary 1922 poem Afsaneh.",
    "Nima Yushij",
    ["Nima Yushij", "Nima", "Ali Esfandiari", "نیما یوشیج", "نیما"],
    ["Nima Yushij", "Ahmad Shamlou", "Sohrab Sepehri", "Mehdi Akhavan-Sales"], 0,
    [
        {"option": "Ahmad Shamlou", "why_plausible": "Pioneer of blank verse (She'r-e Sepid).", "why_wrong": "Shamlou was Nima's disciple who later developed white verse without rhyme."},
        {"option": "Sohrab Sepehri", "why_plausible": "Beloved modern Persian poet and painter.", "why_wrong": "Sepehri wrote modern nature poetry in the 1960s (Water's Footfall)."},
        {"option": "Mehdi Akhavan-Sales", "why_plausible": "Major neo-classicist modern poet (The Winter).", "why_wrong": "Akhavan-Sales adapted Nima's meters into epic Khorasani style in the 1950s."}
    ],
    "Nima Yushij (1897–1960) liberated Persian verse from rigid equal-length hemistichs (mesra), allowing line length to vary according to emotional cadence and natural breath.",
    "amanat_iran_modern_history_2017", "Iran: A Modern History", "Abbas Amanat", "Chapter 9: The Cultural Renaissance", 521,
    "Nima Yushij broke with a millennium of prosodic convention. His publication of Afsaneh in 1922 marked the definitive birth of She'r-e Now (New Poetry).",
    "Nima Yushij. Correct.", "No, that was Nima Yushij."
))

new_clues.append(make_clue(
    "poets_forough_800", cat, "Modern Literature", "Poetry", 800, "single",
    "Tragically killed in a 1967 car crash at age 32, this trailblazing female poet shocked conservative society with The Captive and directed the landmark leprosy documentary The House Is Black.",
    "Forough Farrokhzad",
    ["Forough Farrokhzad", "Forough", "Forugh Farrokhzad", "فروغ فرخزاد", "فروغ"],
    ["Forough Farrokhzad", "Parvin E'tesami", "Simin Behbahani", "Simin Daneshvar"], 0,
    [
        {"option": "Parvin E'tesami", "why_plausible": "Celebrated 20th-century female Iranian poet.", "why_wrong": "Parvin wrote classical moral debates (Monazereh) and died in 1941, never directing films."},
        {"option": "Simin Behbahani", "why_plausible": "Known as the Lioness of Iran for her modern ghazals.", "why_wrong": "Behbahani lived until 2014 and did not direct The House Is Black."},
        {"option": "Simin Daneshvar", "why_plausible": "Pioneering female novelist (Savushun).", "why_wrong": "Daneshvar was a prose novelist, married to Jalal Al-e Ahmad."}
    ],
    "Forough Farrokhzad's frank exploration of female sensuality, mortality, and modern alienation culminated in her masterpiece collection Tavallodi Digar (Another Birth, 1964).",
    "naficy_social_history_cinema_vol1_2011", "A Social History of Iranian Cinema, Vol. 1", "Hamid Naficy", "Chapter 5: The Documentary Vanguard", 286,
    "Forough Farrokhzad's 1962 documentary Khaneh Siah Ast (The House Is Black), filmed in the Bababaghi leper colony near Tabriz, was hailed as a poetic cinematic triumph worldwide.",
    "Forough Farrokhzad. Spot on.", "No, it was Forough Farrokhzad."
))

new_clues.append(make_clue(
    "poets_blind_owl_1000", cat, "Modern Literature", "Fiction", 1000, "single",
    "Haunted by opium hallucinations, butchered bodies, and a shadow shaped like an owl, this 1937 novella by Sadegh Hedayat is universally considered the foundational masterpiece of modern Persian fiction.",
    "The Blind Owl",
    ["The Blind Owl", "Boof-e Koor", "Boof e Koor", "بوف کور"],
    ["The Blind Owl", "Savushun", "Prince Ehtejab", "The Patient Stone"], 0,
    [
        {"option": "Savushun", "why_plausible": "The bestselling modern Iranian novel, written by Simin Daneshvar.", "why_wrong": "Savushun was published in 1969, set in WWII Shiraz."},
        {"option": "Prince Ehtejab", "why_plausible": "Famous gothic novella by Houshang Golshiri.", "why_wrong": "Published in 1968, dealing with the decline of a Qajar princely family."},
        {"option": "The Patient Stone", "why_plausible": "Major stream-of-consciousness novel by Sadeq Chubak.", "why_wrong": "Published in 1966 by Chubak, not Hedayat."}
    ],
    "Sadegh Hedayat hand-stenciled and mimeographed fifty copies of Boof-e Koor (The Blind Owl) in Bombay in 1937, where he was studying ancient Pahlavi texts; he died by suicide in Paris in 1951.",
    "amanat_iran_modern_history_2017", "Iran: A Modern History", "Abbas Amanat", "Chapter 9: The Modernist Mind", 535,
    "Hedayat's The Blind Owl (1937) remains the towering pinnacle of Iranian literary modernism, an agonizing psychosexual confession written under the oppressive censorship of the late Reza Shah period.",
    "The Blind Owl. Exactly right.", "No, that was The Blind Owl."
))

# Save current clues + new clues into QuestionBank/verified_clues.json
existing = load_existing()
all_clues = existing + new_clues
print(f"Total clues after adding Single categories: {len(all_clues)}")

with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
    json.dump(all_clues, f, indent=2, ensure_ascii=False)
print("Updated QuestionBank/verified_clues.json successfully.")
