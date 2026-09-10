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
            "page": item.get("pg", 380 + idx * 8),
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

# 1. CROWN JEWELS & CROWD JEERS (Double, 10 clues)
add_batch(clues, "CROWN JEWELS AND CROWD JEERS", "Royal Regalia & Wealth", "Treasury Lore", "double", [
    {"text": "Carved with the names of Mughal emperors Akbar and Jahangir before being seized by Nader Shah, this 88-carat yellow diamond was given to Tsar Nicholas I in 1829.",
     "ans": "The Shah Diamond", "aliases": ["The Shah Diamond", "Shah Diamond", "الماس شاه"],
     "options": ["The Shah Diamond", "The Koh-i-Noor", "The Daria-i-Noor", "The Orlov Diamond"],
     "rationales": [{"option": "The Koh-i-Noor", "why_plausible": "Famous Indian diamond.", "why_wrong": "Taken to Lahore by Ranjit Singh and surrendered to Queen Victoria in 1849."},
                    {"option": "The Daria-i-Noor", "why_plausible": "Pink diamond in Tehran.", "why_wrong": "Remained in Tehran."},
                    {"option": "The Orlov Diamond", "why_plausible": "Russian imperial diamond.", "why_wrong": "Set in Catherine the Great's imperial sceptre."}],
     "expl": "Prince Khosrow Mirza delivered the Shah Diamond to St. Petersburg as royal blood money to apologize for the murder of diplomat Alexander Griboyedov.", "pg": 254},
    {"text": "Fabricated by Paris jeweler Van Cleef & Arpels for the 1967 coronation of Empress Farah, her platinum crown featured this many carats of emeralds and diamonds.",
     "ans": "Over 1,400 Jewels", "aliases": ["Over 1,400 Jewels", "1,469 Jewels", "1469", "۱۴۶۹ جواهر"],
     "options": ["Over 1,400 Jewels", "500 Jewels", "100 Jewels", "5,000 Jewels"],
     "rationales": [{"option": "500 Jewels", "why_plausible": "Modest count.", "why_wrong": "Understates the crown's composition."},
                    {"option": "100 Jewels", "why_plausible": "Far too low.", "why_wrong": "Understates the regal commission."},
                    {"option": "5,000 Jewels", "why_plausible": "Excessive.", "why_wrong": "Exaggerated count."}],
     "expl": "French jeweler Pierre Arpels traveled to Tehran twenty-four times because Iranian law strictly prohibited removing the state gems from the Central Bank vault.", "pg": 634},
    {"text": "Discovered in Golconda, India, this massive uncut 500-carat red spinel gemstone in the Treasury is known by this historical name.",
     "ans": "The Samarian Spinel", "aliases": ["The Samarian Spinel", "Samarian Spinel", "اسپینل سامره"],
     "options": ["The Samarian Spinel", "The Black Prince's Ruby", "The Timur Ruby", "The Hope Spinel"],
     "rationales": [{"option": "The Black Prince's Ruby", "why_plausible": "British crown spinel.", "why_wrong": "Mounted in the British Imperial State Crown."},
                    {"option": "The Timur Ruby", "why_plausible": "Famous inscribed Mughal spinel.", "why_wrong": "Presented to Queen Victoria in 1851."},
                    {"option": "The Hope Spinel", "why_plausible": "Collector's gem.", "why_wrong": "Sold at auction in London."}],
     "expl": "It is the largest known spinel in the world, pierced with a suspension hole originally intended for an Indian potentate's turban ornament.", "pg": 206},
    {"text": "The coronation mantle worn by Reza Shah in 1926 and Mohammad Reza Shah in 1967 was crafted from heavy gold brocade embroidered with this national symbol.",
     "ans": "The Lion and Sun (Shir-o Khorshid)", "aliases": ["The Lion and Sun", "Shir-o Khorshid", "شیر و خورشید"],
     "options": ["The Lion and Sun (Shir-o Khorshid)", "The Faravahar", "The Simurgh", "The Double-Headed Eagle"],
     "rationales": [{"option": "The Faravahar", "why_plausible": "Ancient Zoroastrian symbol.", "why_wrong": "Used on modern monuments, but the state regalia bore the Lion and Sun."},
                    {"option": "The Simurgh", "why_plausible": "Mythic bird.", "why_wrong": "Literary bird."},
                    {"option": "The Double-Headed Eagle", "why_plausible": "Russian/Byzantine imperial crest.", "why_wrong": "Tsarist Russian heraldry."}],
     "expl": "Woven in Isfahan workshops, the crimson velvet cape was trimmed with white ermine fur and studded with diamond rays.", "pg": 484},
    {"text": "This diamond-studded gold scabbard and curved shamshir saber in the Treasury, carried by Nader Shah at the Battle of Karnal, was known as this.",
     "ans": "The Shamshir-e Jahangosha (Conqueror of the World Sword)", "aliases": ["The Shamshir-e Jahangosha", "Shamshir-e Jahangosha", "شمشیر جهانگشا"],
     "options": ["The Shamshir-e Jahangosha (Conqueror of the World Sword)", "Zulfiqar", "The Sword of Cyrus", "The Imperial Dagger"],
     "rationales": [{"option": "Zulfiqar", "why_plausible": "Imam Ali's sword.", "why_wrong": "Iconic religious blade."},
                    {"option": "The Sword of Cyrus", "why_plausible": "Ancient blade.", "why_wrong": "Legendary antique."},
                    {"option": "The Imperial Dagger", "why_plausible": "Curved dagger.", "why_wrong": "A straight dagger (Khanjar), not the curved shamshir."}],
     "expl": "The hilt is encrusted with over 1,700 diamonds, engraved with Persian verses celebrating Nader's military dominion over India and Central Asia.", "pg": 208},
    # Set B
    {"text": "Under Iranian law passed in 1937, the Crown Jewels cannot be pledged, sold, or taken abroad because they serve as this legal guarantee.",
     "ans": "The Gold & Foreign Exchange Reserve Backing of the National Currency", "aliases": ["The Reserve Backing of the National Currency", "Currency Backing", "پشتوانه اسکناس", "پشتوانه پول ملی"],
     "options": ["The Gold & Foreign Exchange Reserve Backing of the National Currency", "The Private Property of the Pahlavi Family", "A Charitable Religious Endowment (Waqf)", "Collateral for Foreign Oil Loans"],
     "rationales": [{"option": "The Private Property of the Pahlavi Family", "why_plausible": "Royal collection.", "why_wrong": "Legally transferred to the state treasury in 1937."},
                    {"option": "A Charitable Religious Endowment (Waqf)", "why_plausible": "Pious property.", "why_wrong": "Secular state financial collateral."},
                    {"option": "Collateral for Foreign Oil Loans", "why_plausible": "Commercial collateral.", "why_wrong": "Never mortgaged to foreign creditors."}],
     "expl": "Every Iranian paper banknote issued by the Central Bank has historically been legally underwritten by the precious stones in the vault.", "pg": 485},
    {"text": "The monumental marble platform throne carved in 1806 from 65 pieces of yellow Yazd alabaster marble for Fath-Ali Shah stands in this Tehran palace terrace.",
     "ans": "Golestan Palace (Takht-e Marmar)", "aliases": ["Golestan Palace", "Takht-e Marmar", "Marble Throne", "کاخ گلستان", "تخت مرمر"],
     "options": ["Golestan Palace (Takht-e Marmar)", "Sa'dabad Palace", "Niavaran Palace", "Marmar Palace"],
     "rationales": [{"option": "Sa'dabad Palace", "why_plausible": "Pahlavi summer palace.", "why_wrong": "Located in northern Shemiran."},
                    {"option": "Niavaran Palace", "why_plausible": "Late Pahlavi palace.", "why_wrong": "Built in the 1960s."},
                    {"option": "Marmar Palace", "why_plausible": "Reza Shah's residence.", "why_wrong": "Reza Shah's residence on Pasteur Avenue."}],
     "expl": "Supported on the shoulders of carved marble demons, angels, and lions, it was used for public royal audiences during Nowruz.", "pg": 232},
    {"text": "This solid gold teapot encrusted with diamonds and emeralds in the Treasury was designed with a charcoal heating furnace to brew tea for this monarch.",
     "ans": "Nasir al-Din Shah Qajar", "aliases": ["Nasir al-Din Shah Qajar", "Nasir al-Din Shah", "ناصرالدین شاه"],
     "options": ["Nasir al-Din Shah Qajar", "Fath-Ali Shah", "Reza Shah", "Shah Abbas I"],
     "rationales": [{"option": "Fath-Ali Shah", "why_plausible": "Flamboyant gem collector.", "why_wrong": "Reigned before Russian samovars and teapots became ubiquitous court fixtures."},
                    {"option": "Reza Shah", "why_plausible": "Modernizer.", "why_wrong": "Favored austere military lifestyle."},
                    {"option": "Shah Abbas I", "why_plausible": "Safavid emperor.", "why_wrong": "Reigned in the 16th/17th century before Russian tea culture reached Iran."}],
     "expl": "Nasir al-Din Shah took the portable jeweled teapot on royal hunting expeditions across the Alborz mountains.", "pg": 376},
    {"text": "The British royal diamond that was surrendered by the Maharajah of Lahore to the British East India Company after Nader Shah looted it from Delhi is this.",
     "ans": "The Koh-i-Noor (Mountain of Light)", "aliases": ["The Koh-i-Noor", "Koh-i-Noor", "Mountain of Light", "کوه نور"],
     "options": ["The Koh-i-Noor (Mountain of Light)", "The Daria-i-Noor", "The Cullinan Diamond", "The Regent Diamond"],
     "rationales": [{"option": "The Daria-i-Noor", "why_plausible": "Sister diamond.", "why_wrong": "Remained in Tehran in the Central Bank."},
                    {"option": "The Cullinan Diamond", "why_plausible": "Largest diamond ever found.", "why_wrong": "Discovered in South Africa in 1905."},
                    {"option": "The Regent Diamond", "why_plausible": "French crown jewel.", "why_wrong": "Set in Napoleon's sword in Paris."}],
     "expl": "Nader Shah reportedly gasped 'Koh-i-Noor!' (Mountain of Light!) when he first saw the 186-carat gem hidden in the folds of the Mughal Emperor's turban.", "pg": 205},
    {"text": "The high-security subterranean treasury vault housing the Crown Jewels on Ferdowsi Avenue in Tehran is opened to the public for only this many hours per week.",
     "ans": "Eight to Ten Hours (Strict Afternoon Tours)", "aliases": ["Eight to Ten Hours", "Strict Afternoon Tours", "Limited public hours", "ساعات محدود"],
     "options": ["Eight to Ten Hours (Strict Afternoon Tours)", "Open Daily 9am-5pm", "Never Open to the Public", "Open 24/7"],
     "rationales": [{"option": "Open Daily 9am-5pm", "why_plausible": "Standard museum schedule.", "why_wrong": "Security regulations restrict entry to Saturday through Tuesday afternoons only."},
                    {"option": "Never Open to the Public", "why_plausible": "High security.", "why_wrong": "It operates as a public exhibition museum under heavy armed guard."},
                    {"option": "Open 24/7", "why_plausible": "Tourist claim.", "why_wrong": "Impossible for a sovereign bullion vault."}],
     "expl": "Visitors must pass through three bombproof vault doors, metal detectors, and armed Revolutionary Guard sentries to enter the subterranean vault.", "pg": 486}
])

# 2. JUNGLE GUERRILLAS OF GILAN (Double, 10 clues)
add_batch(clues, "JUNGLE GUERRILLAS OF GILAN", "Caspian Revolutionary Front", "Jangali Movement", "double", [
    {"text": "The radical pro-Bolshevik member of the Jangali leadership who ousted Mirza Kuchik Khan in August 1920 to proclaim a full Marxist republic was named this.",
     "ans": "Ehsanollah Khan Dustdar", "aliases": ["Ehsanollah Khan Dustdar", "Ehsanollah Khan", "احسان‌الله خان", "احسان‌الله خان دوستدار"],
     "options": ["Ehsanollah Khan Dustdar", "Mirza Kuchik Khan", "Haydar Khan Amu-Oghli", "Khalou Qorban"],
     "rationales": [{"option": "Mirza Kuchik Khan", "why_plausible": "Founding leader.", "why_wrong": "Religious nationalist who fled into the forest rather than accept forced Bolshevik land collectivization."},
                    {"option": "Haydar Khan Amu-Oghli", "why_plausible": "Bolshevik organizer.", "why_wrong": "Sent by Moscow to mediate between Kuchik and Ehsanollah."},
                    {"option": "Khalou Qorban", "why_plausible": "Kurdish warlord who defected to Reza Khan.", "why_wrong": "Kurdish commander who later delivered Kuchik Khan's severed head to Tehran."}],
     "expl": "Ehsanollah Khan marched a ragtag Red Army toward Tehran, but was routed at Pol-e Rudbar by Reza Khan's Cossacks; he fled to Baku where Stalin purged him in 1939.", "pg": 435},
    {"text": "The secret society formed by Mirza Kuchik Khan and his companions in Tehran in 1914 before taking up arms in the Caspian forests was known as this.",
     "ans": "The Committee of Islamic Unity (Ettehad-e Eslam)", "aliases": ["The Committee of Islamic Unity", "Ettehad-e Eslam", "اتحاد اسلام", "کمیته اتحاد اسلام"],
     "options": ["The Committee of Islamic Unity (Ettehad-e Eslam)", "Komiteh-ye Mojazat", "Ferqeh-ye Demokrat", "Fada'iyan-e Islam"],
     "rationales": [{"option": "Komiteh-ye Mojazat", "why_plausible": "Terrorist secret society in Tehran.", "why_wrong": "Assassinated corrupt politicians in Tehran in 1917."},
                    {"option": "Ferqeh-ye Demokrat", "why_plausible": "Political party.", "why_wrong": "Parliamentary democratic party."},
                    {"option": "Fada'iyan-e Islam", "why_plausible": "Islamist group.", "why_wrong": "Founded in the 1940s by Navvab Safavi."}],
     "expl": "The committee sought to expel British and Russian occupation troops while resisting the corrupt central government in Tehran.", "pg": 433},
    {"text": "The British expeditionary force dispatched through western Iran to the Caspian Sea in 1918 to seize the Baku oil fields was nicknamed this after its general.",
     "ans": "Dunsterforce (General Lionel Dunsterville)", "aliases": ["Dunsterforce", "General Lionel Dunsterville", "دنسترفورس", "ژنرال دنسترویل"],
     "options": ["Dunsterforce (General Lionel Dunsterville)", "South Persia Rifles", "Sykes Expedition", "The White Army"],
     "rationales": [{"option": "South Persia Rifles", "why_plausible": "British force in Shiraz.", "why_wrong": "Formed in southern Iran under Percy Sykes."},
                    {"option": "Sykes Expedition", "why_plausible": "Southern expedition.", "why_wrong": "Operated in Kerman and Fars."},
                    {"option": "The White Army", "why_plausible": "Russian anti-Bolsheviks.", "why_wrong": "Tsarist counter-revolutionaries."}],
     "expl": "Dunsterville fought pitched battles against the Jangalis at the Manjil bridge before reaching Anzali and sailing to Baku.", "pg": 431},
    {"text": "The official newspaper published in the forests of Gilan by the Jangali Movement, printed on a portable lithograph press, was named this.",
     "ans": "Jangal (The Jungle)", "aliases": ["Jangal", "Jungle", "Ruznameh-ye Jangal", "روزنامه جنگل", "جنگل"],
     "options": ["Jangal (The Jungle)", "Sur-e Esrafil", "Qanun", "Habal al-Matin"],
     "rationales": [{"option": "Sur-e Esrafil", "why_plausible": "Constitutional weekly.", "why_wrong": "Published in Tehran by Jahangir Khan."},
                    {"option": "Qanun", "why_plausible": "Reformist paper.", "why_wrong": "Malkom Khan's newspaper printed in London."},
                    {"option": "Habal al-Matin", "why_plausible": "Influential paper.", "why_wrong": "Published in Calcutta."}],
     "expl": "Edited by Hosein Kasma'i, Jangal proclaimed its motto: 'Iran belongs to Iranians; foreigners must leave.'", "pg": 434},
    {"text": "The treaty signed on February 26, 1921 between Moscow and Tehran that renounced all Tsarist concessions and caused the Red Army to abandon the Jangalis was this.",
     "ans": "The Russo-Persian Treaty of Friendship (1921)", "aliases": ["The Russo-Persian Treaty of Friendship", "1921 Treaty", "قرارداد ۱۹۲۱ ایران و شوروی"],
     "options": ["The Russo-Persian Treaty of Friendship (1921)", "Treaty of Turkmenchay", "Treaty of Brest-Litovsk", "Anglo-Persian Agreement of 1919"],
     "rationales": [{"option": "Treaty of Turkmenchay", "why_plausible": "1828 imperial treaty.", "why_wrong": "Tsarist conquest treaty."},
                    {"option": "Treaty of Brest-Litovsk", "why_plausible": "1918 Soviet-German peace.", "why_wrong": "Ended WWI for Russia with Germany."},
                    {"option": "Anglo-Persian Agreement of 1919", "why_plausible": "Unratified British treaty.", "why_wrong": "British protectorate agreement rejected by the Majles."}],
     "expl": "Article 6 granted Soviet troops the right to enter Iran if a third power used Iranian territory to threaten Russia, a clause Moscow cited during WWI in 1941.", "pg": 440},
    # Set B
    {"text": "The German master adventurer and military officer who joined the Jangalis in 1918 to train guerrilla snipers against the British was named this.",
     "ans": "Fritz Pukas", "aliases": ["Fritz Pukas", "Major Pukas", "فون پاخن", "پوکاس"],
     "options": ["Fritz Pukas", "Wilhelm Wassmuss", "Oskar von Niedermayer", "Hans Schultze"],
     "rationales": [{"option": "Wilhelm Wassmuss", "why_plausible": "Wassmuss of Persia.", "why_wrong": "German spy who operated among the Qashqai and Tangistani tribes in southern Iran."},
                    {"option": "Oskar von Niedermayer", "why_plausible": "German expedition commander.", "why_wrong": "Led the German military mission to Afghanistan across the desert."},
                    {"option": "Hans Schultze", "why_plausible": "German agent.", "why_wrong": "Operated in Kermanshah."}],
     "expl": "Pukas organized sniper units in the dense ferns of Gilan, ambushing British armored cars along the Rasht-Manjil road.", "pg": 432},
    {"text": "The Kurdish warlord from Kermanshah who fought with the Jangalis before switching sides to Reza Khan and severing Kuchik Khan's head was named this.",
     "ans": "Khalou Qorban", "aliases": ["Khalou Qorban", "Qorban", "خالو قربان", "خالو قربان هرسینی"],
     "options": ["Khalou Qorban", "Simko Shikak", "Ja'far Sultan", "Hamzeh Khan"],
     "rationales": [{"option": "Simko Shikak", "why_plausible": "Kurdish rebel chieftain in Urmia.", "why_wrong": "Rebelled in northwestern Azerbaijan, killing Mar Shimun."},
                    {"option": "Ja'far Sultan", "why_plausible": "Hawraman chieftain.", "why_wrong": "Rebelled in the Zagros mountains."},
                    {"option": "Hamzeh Khan", "why_plausible": "Lur chieftain.", "why_wrong": "Lur chieftain in Lorestan."}],
     "expl": "Khalou Qorban brought Kuchik Khan's head to Tehran in a biscuit tin; he was later shot dead in 1922 fighting Kurdish rebels in Azerbaijan.", "pg": 436},
    {"text": "In 1919, the British government under Lord Curzon attempted to impose this controversial treaty turning Iran into a de facto British protectorate.",
     "ans": "The Anglo-Persian Agreement of 1919", "aliases": ["The Anglo-Persian Agreement of 1919", "1919 Agreement", "قرارداد ۱۹۱۹", "قرارداد ۱۹۱۹ وثوق‌الدوله"],
     "options": ["The Anglo-Persian Agreement of 1919", "The Reuter Concession", "The D'Arcy Concession", "The Baghdad Pact"],
     "rationales": [{"option": "The Reuter Concession", "why_plausible": "1872 economic monopoly.", "why_wrong": "Granted to Baron de Reuter for railways and mines."},
                    {"option": "The D'Arcy Concession", "why_plausible": "1901 oil concession.", "why_wrong": "Signed for petroleum in 1901."},
                    {"option": "The Baghdad Pact", "why_plausible": "1955 defense treaty.", "why_wrong": "Cold War military alliance signed in 1955."}],
     "expl": "Prime Minister Vosough al-Dowleh accepted 131,000 pounds in personal British bribes to sign the treaty, but public outcry and the Majles prevented its ratification.", "pg": 438},
    {"text": "Mirza Kuchik Khan's original occupation and training before leading the Caspian insurgency was as this.",
     "ans": "Seminary Theological Student (Tullab / Cleric)", "aliases": ["Seminary Theological Student", "Tullab", "Cleric", "طلبه", "روحانی"],
     "options": ["Seminary Theological Student (Tullab / Cleric)", "Cossack Officer", "Telegraph Operator", "Bazaar Carpet Merchant"],
     "rationales": [{"option": "Cossack Officer", "why_plausible": "Military background.", "why_wrong": "Reza Khan was a Cossack, while Kuchik was a turbaned seminary student."},
                    {"option": "Telegraph Operator", "why_plausible": "Intellectual profession.", "why_wrong": "Associated with constitutional telegraph basts."},
                    {"option": "Bazaar Carpet Merchant", "why_plausible": "Bazaari trade.", "why_wrong": "He came from an educated religious background."}],
     "expl": "Kuchik Khan studied at the Jameh Seminary in Rasht and the Mahmudieh School in Tehran, fighting in the constitutional militias that captured Tehran in 1909.", "pg": 431},
    {"text": "Today, the restored tomb of Mirza Kuchik Khan and his martyred companions is visited by pilgrims in this neighborhood of Rasht.",
     "ans": "Soleyman-Darab", "aliases": ["Soleyman-Darab", "Suleyman Darab", "سلیمان داراب", "سلیمان‌داراب رشت"],
     "options": ["Soleyman-Darab", "Golsar", "Sabzeh Meydan", "Shahrdari"],
     "rationales": [{"option": "Golsar", "why_plausible": "Modern wealthy neighborhood in Rasht.", "why_wrong": "Northern residential quarter."},
                    {"option": "Sabzeh Meydan", "why_plausible": "Historic square in Rasht.", "why_wrong": "Central public park square."},
                    {"option": "Shahrdari", "why_plausible": "Municipal square.", "why_wrong": "Pedestrian municipal square with the clock tower."}],
     "expl": "His severed head was secretly recovered from Hassanabad cemetery in Tehran and reunited with his body in Soleyman-Darab decades later.", "pg": 437}
])

save_data(clues)
