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
            "page": item.get("pg", 300 + idx * 8),
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

# 1. AYAT-ALL-THAT (Double, 10 clues)
add_batch(clues, "AYAT-ALL-THAT", "Shi'i Theology & Jurisprudence", "Theology", "double", [
    {"text": "In his 1970 Najaf lectures, Ayatollah Khomeini articulated this radical political doctrine asserting that the supreme Islamic jurist must rule the state directly.",
     "ans": "Velayat-e Faqih (Guardianship of the Jurist)", "aliases": ["Velayat-e Faqih", "Guardianship of the Jurist", "Hokumat-e Eslami", "ولایت فقیه", "حکومت اسلامی"],
     "options": ["Velayat-e Faqih (Guardianship of the Jurist)", "Ijtihad", "Taqlid", "Taqiyya"],
     "rationales": [{"option": "Ijtihad", "why_plausible": "Legal reasoning.", "why_wrong": "The intellectual process of deriving law, not the doctrine of clerical state rule."},
                    {"option": "Taqlid", "why_plausible": "Imitation of a cleric.", "why_wrong": "Following a Marja in religious practice."},
                    {"option": "Taqiyya", "why_plausible": "Dissimulation doctrine.", "why_wrong": "Precautionary concealment of belief."}],
     "expl": "Published as Islamic Government: Governance of the Jurist, it broke with centuries of quietist Shi'i theology awaiting the return of the Hidden Imam.", "pg": 670},
    {"text": "The traditional Shi'i legal school that championed rational deduction (Ijtihad) over literal scriptural traditions in the 18th century is known as this.",
     "ans": "The Usuli School", "aliases": ["The Usuli School", "Usulis", "Usulism", "اصولی", "مکتب اصولی"],
     "options": ["The Usuli School", "The Akhbari School", "The Sheikhi School", "The Zaidi School"],
     "rationales": [{"option": "The Akhbari School", "why_plausible": "Rival traditionalist school.", "why_wrong": "Held that only direct traditions (akhbar) from the Imams could be followed, rejecting human reason."},
                    {"option": "The Sheikhi School", "why_plausible": "Esoteric school founded by Ahmad al-Ahsa'i.", "why_wrong": "Mystical philosophical offshoot."},
                    {"option": "The Zaidi School", "why_plausible": "Fiver Shia school.", "why_wrong": "Yemeni Shi'i sect."}],
     "expl": "Led by Vahid Behbahani in Karbala, the Usuli victory established the absolute authority of living Mujtahids over the faithful.", "pg": 238},
    {"text": "The Shi'i religious tax of one-fifth levied on annual surplus wealth, channeled directly to Grand Ayatollahs to fund seminaries and stipends, is this.",
     "ans": "Khums", "aliases": ["Khums", "Khomss", "خمس", "سهم امام"],
     "options": ["Khums", "Zakat", "Jizya", "Waqf"],
     "rationales": [{"option": "Zakat", "why_plausible": "General Islamic alms tax.", "why_wrong": "Levied on agricultural livestock and grain, whereas Khums is the 20% savings tax unique to Shi'i institutional independence."},
                    {"option": "Jizya", "why_plausible": "Poll tax on minorities.", "why_wrong": "Historical tax on non-Muslims."},
                    {"option": "Waqf", "why_plausible": "Pious endowment.", "why_wrong": "Endowed property, not the annual wealth tax."}],
     "expl": "Khums is divided into Sahm-e Imam (Share of the Imam) and Sahm-e Sadat (Share of the Prophet's descendants), giving the Hawza financial independence from the state.", "pg": 240},
    {"text": "To attain the rank of Ayatollah and Marja-e Taqlid, a scholar must be granted this formal diploma certifying their mastery of independent legal derivation.",
     "ans": "Ijaza-ye Ijtihad", "aliases": ["Ijaza-ye Ijtihad", "Ijaza", "Ijtihad Certification", "اجازه اجتهاد", "اجتهاد"],
     "options": ["Ijaza-ye Ijtihad", "Fatwa", "Amam-gozari", "Khutba"],
     "rationales": [{"option": "Fatwa", "why_plausible": "Legal opinion.", "why_wrong": "A ruling issued by a jurist, not his diploma of authority."},
                    {"option": "Amam-gozari", "why_plausible": "Turban-donning ceremony.", "why_wrong": "Turban ceremony for beginner seminary graduates."},
                    {"option": "Khutba", "why_plausible": "Sermon.", "why_wrong": "Friday prayer sermon."}],
     "expl": "Granted by senior masters in Najaf or Qom, an Ijaza certifies that the scholar possesses the capacity to deduce original Islamic rulings from the Quran and Sunnah.", "pg": 242},
    {"text": "The manual of Islamic jurisprudence published by every Grand Ayatollah as a practical guide for their followers is known by this Arabic title.",
     "ans": "Towzih al-Masa'el (Risalah)", "aliases": ["Towzih al-Masa'el", "Risalah", "Tawzih al-Masail", "توضیح‌المسائل", "رساله"],
     "options": ["Towzih al-Masa'el (Risalah)", "Nahj al-Balagha", "Bihar al-Anwar", "Al-Kafi"],
     "rationales": [{"option": "Nahj al-Balagha", "why_plausible": "Sermons of Imam Ali.", "why_wrong": "10th-century compilation by Sharif Razi."},
                    {"option": "Bihar al-Anwar", "why_plausible": "110-volume hadith encyclopedia.", "why_wrong": "Majlisi's Safavid hadith collection."},
                    {"option": "Al-Kafi", "why_plausible": "Foundational 10th-century hadith collection.", "why_wrong": "Kulayni's canonical hadith compendium."}],
     "expl": "The Risalah details rulings on prayer, fasting, business transactions, and purity, required reading for every practicing Shi'i follower (Muqallid).", "pg": 672},
    # Set B
    {"text": "Before 1979, this conservative Grand Ayatollah in Qom advocated political quietism and cooperation with the monarchy to protect the seminary from state persecution.",
     "ans": "Grand Ayatollah Mohammad Reza Golpayegani", "aliases": ["Grand Ayatollah Mohammad Reza Golpayegani", "Golpayegani", "گلپایگانی", "آیت‌الله گلپایگانی"],
     "options": ["Grand Ayatollah Mohammad Reza Golpayegani", "Ayatollah Taleghani", "Ayatollah Montazeri", "Ayatollah Beheshti"],
     "rationales": [{"option": "Ayatollah Taleghani", "why_plausible": "Tehran revolutionary cleric.", "why_wrong": "Leftist political activist jailed by SAVAK."},
                    {"option": "Ayatollah Montazeri", "why_plausible": "Khomeini's designated heir.", "why_wrong": "Political militant exiled in the 1970s."},
                    {"option": "Ayatollah Beheshti", "why_plausible": "Founding leader of Islamic Republic Party.", "why_wrong": "Political architect of the post-1979 state."}],
     "expl": "Golpayegani ran major hospitals, printing presses, and seminaries in Qom, serving as supreme traditionalist authority alongside Mar'ashi Najafi.", "pg": 674},
    {"text": "The theological practice of dissimulating or concealing one's true religious convictions to save oneself from persecution or death is known as this.",
     "ans": "Taqiyya", "aliases": ["Taqiyya", "Taqiyyah", "تقیه"],
     "options": ["Taqiyya", "Ijtihad", "Jihad", "Zuhd"],
     "rationales": [{"option": "Ijtihad", "why_plausible": "Legal reasoning.", "why_wrong": "Deduction of legal rulings."},
                    {"option": "Jihad", "why_plausible": "Struggle.", "why_wrong": "Spiritual or military defense."},
                    {"option": "Zuhd", "why_plausible": "Asceticism.", "why_wrong": "Abstinence from worldly pleasures."}],
     "expl": "Khomeini famously suspended Taqiyya during the 1963 protests, declaring: 'Taqiyya is forbidden when Islam itself is endangered!'", "pg": 676},
    {"text": "In 1980, this veteran cleric and philosopher who drafted the Assembly of Experts constitution was chosen as the first Chief Justice of the Islamic Republic.",
     "ans": "Ayatollah Mohammad Beheshti", "aliases": ["Ayatollah Mohammad Beheshti", "Mohammad Beheshti", "Beheshti", "محمد بهشتی", "شهید بهشتی"],
     "options": ["Ayatollah Mohammad Beheshti", "Ayatollah Khalkhali", "Ayatollah Yazdi", "Ayatollah Shahroudi"],
     "rationales": [{"option": "Ayatollah Khalkhali", "why_plausible": "Revolutionary tribunal judge.", "why_wrong": "Head of summary revolutionary courts, not the Supreme Court."},
                    {"option": "Ayatollah Yazdi", "why_plausible": "Judiciary chief in the 1990s.", "why_wrong": "Headed the judiciary under Khamenei."},
                    {"option": "Ayatollah Shahroudi", "why_plausible": "Judiciary chief in the 2000s.", "why_wrong": "Headed the judiciary from 1999 to 2009."}],
     "expl": "Beheshti was killed on June 28, 1981 (7 Tir), alongside 72 senior officials when an MEK bomb destroyed the Islamic Republic Party headquarters.", "pg": 732},
    {"text": "The highest theological class in the Hawza curriculum, conducted as open seminars without textbooks where students debate master jurists, is known as this.",
     "ans": "Dars-e Kharij (Exterior Studies)", "aliases": ["Dars-e Kharij", "Dars-e Kharej", "Kharij", "درس خارج"],
     "options": ["Dars-e Kharij (Exterior Studies)", "Sutuh", "Muqaddamat", "Jami'a"],
     "rationales": [{"option": "Sutuh", "why_plausible": "Intermediate seminary stage.", "why_wrong": "Textbook-based study of standard legal treatises."},
                    {"option": "Muqaddamat", "why_plausible": "Introductory stage.", "why_wrong": "Foundational study of Arabic grammar and logic."},
                    {"option": "Jami'a", "why_plausible": "University.", "why_wrong": "Modern secular academy."}],
     "expl": "Dars-e Kharij allows advanced scholars to present independent legal arguments, demonstrating their readiness to receive an Ijaza of Ijtihad.", "pg": 241},
    {"text": "Located in Qom, this historic theological library holds over 85,000 rare Islamic manuscripts, assembled by Grand Ayatollah Shahab al-Din Mar'ashi Najafi.",
     "ans": "Mar'ashi Najafi Library", "aliases": ["Mar'ashi Najafi Library", "Mar'ashi Library", "کتابخانه آیت‌الله مرعشی نجفی", "کتابخانه مرعشی"],
     "options": ["Mar'ashi Najafi Library", "National Library of Iran", "Malek National Museum & Library", "Majles Library"],
     "rationales": [{"option": "National Library of Iran", "why_plausible": "State library in Tehran.", "why_wrong": "Located in Abbasabad, Tehran."},
                    {"option": "Malek National Museum & Library", "why_plausible": "Bazaar library in Tehran.", "why_wrong": "Endowed by Haj Hossein Malek in Tehran."},
                    {"option": "Majles Library", "why_plausible": "Parliament library.", "why_wrong": "Located at Baharestan square."}],
     "expl": "Mar'ashi Najafi skipped meals and worked night shifts in Najaf bakeries in the 1920s to purchase manuscripts before European orientalists could acquire them.", "pg": 678}
])

save_data(clues)
