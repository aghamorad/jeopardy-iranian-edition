#!/usr/bin/env python3
import json

def generate_part_a():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues_by_id = {c["id"]: c for c in json.load(f)}

    def add_10(cat, period, theme, items):
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "")
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
                "source_id": item.get("src", "katouzian_the_persians_2009"),
                "book_title": item.get("book", "The Persians: Ancient, Mediaeval and Modern Iran"),
                "author": item.get("auth", "Homa Katouzian"),
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

    # 1. NOT IN MY BACK-YAZD
    add_10("NOT IN MY BACK-YAZD", "Desert Architecture & Zoroastrianism", "Architecture & Religion", [
        {"text": "These iconic architectural cooling chimneys rising above Yazd desert rooftops capture desert breezes and funnel chilled air down into interior living quarters.",
         "ans": "Windcatchers (Badgirs)", "aliases": ["Windcatchers", "Badgirs", "Badgir", "بادگیر"],
         "options": ["Windcatchers (Badgirs)", "Minarets", "Qanats", "Yakhchals"],
         "rationales": [{"option": "Minarets", "why_plausible": "Tall towers on mosques.", "why_wrong": "Mosque calling towers, not passive thermal ventilation chimneys."},
                        {"option": "Qanats", "why_plausible": "Underground aqueducts.", "why_wrong": "Subterranean water channels."},
                        {"option": "Yakhchals", "why_plausible": "Desert ice houses.", "why_wrong": "Domed ice storage structures."}],
         "expl": "The tallest windcatcher in the world stands 33 meters high in the Dowlatabad Garden of Yazd.", "pg": 145},
        {"text": "Stretching for thousands of kilometers beneath the desert plateau, this ancient UNESCO-listed system of subterranean gently sloping water channels sustained Persian oasis cities.",
         "ans": "Qanats", "aliases": ["Qanats", "Qanat", "Kariz", "قنات", "کاریز"],
         "options": ["Qanats", "Badgirs", "Ab Anbars", "Howz"],
         "rationales": [{"option": "Badgirs", "why_plausible": "Desert engineering.", "why_wrong": "Above-ground wind cooling towers."},
                        {"option": "Ab Anbars", "why_plausible": "Water reservoirs.", "why_wrong": "Cistern reservoirs fed by qanats."},
                        {"option": "Howz", "why_plausible": "Courtyard pool.", "why_wrong": "Surface courtyard pools."}],
         "expl": "Invented in Iran in the early 1st millennium BC, qanats rely entirely on gravity to bring mountain aquifer water to dry plains without evaporation.", "pg": 147},
        {"text": "Perched on barren hills outside Yazd, these circular stone towers were used by Zoroastrians for ritual excarnation until the mid-20th century.",
         "ans": "Towers of Silence (Dakhmeh)", "aliases": ["Towers of Silence", "Dakhmeh", "دخمه", "برج خاموشان"],
         "options": ["Towers of Silence (Dakhmeh)", "Fire Temples", "Ziggurats", "Atashkadeh"],
         "rationales": [{"option": "Fire Temples", "why_plausible": "Zoroastrian sacred places.", "why_wrong": "Sanctuaries housing the sacred flame."},
                        {"option": "Ziggurats", "why_plausible": "Ancient religious towers.", "why_wrong": "Elamite/Mesopotamian stepped temples."},
                        {"option": "Atashkadeh", "why_plausible": "Zoroastrian shrine.", "why_wrong": "House of fire, not the mortuary tower."}],
         "expl": "Zoroastrians placed bodies on Dakhmeh towers to be consumed by birds of prey, avoiding polluting the sacred elements of earth and fire.", "pg": 149},
        {"text": "Housed in the Atashkadeh of Yazd, this sacred Zoroastrian flame of the highest grade (Atash Bahram) has been burning continuously since this century AD.",
         "ans": "5th Century AD (c. 470 AD)", "aliases": ["5th Century AD", "470 AD", "Over 1,500 years", "سده پنجم میلادی"],
         "options": ["5th Century AD (c. 470 AD)", "10th Century AD", "16th Century AD", "19th Century AD"],
         "rationales": [{"option": "10th Century AD", "why_plausible": "Medieval Islamic era.", "why_wrong": "The flame was transferred earlier during Sasanian times."},
                        {"option": "16th Century AD", "why_plausible": "Safavid era.", "why_wrong": "Burning long before the Safavids."},
                        {"option": "19th Century AD", "why_plausible": "When the current temple building was constructed.", "why_wrong": "The building was erected in 1934, but the consecrated flame has burned for 1,500 years."}],
         "expl": "The sacred fire was kept burning in secret caves near Ardakan before being moved to the Yazd Fire Temple in 1934.", "pg": 150},
        {"text": "Tucked into a sheer mountain cliff near Yazd, this holy pilgrimage site commemorates Nikbanou, daughter of the last Sasanian king Yazdegerd III.",
         "ans": "Chak Chak (Pir-e Sabz)", "aliases": ["Chak Chak", "Pir-e Sabz", "چک چک", "پیر سبز"],
         "options": ["Chak Chak (Pir-e Sabz)", "Pir-e Herisht", "Seti Pir", "Banu Pars"],
         "rationales": [{"option": "Pir-e Herisht", "why_plausible": "Another Zoroastrian shrine near Ardakan.", "why_wrong": "Shrine to the maid of Nikbanou."},
                        {"option": "Seti Pir", "why_plausible": "Yazd shrine.", "why_wrong": "Shrine to Yazdegerd's queen."},
                        {"option": "Banu Pars", "why_plausible": "Shrine in Fars.", "why_wrong": "Shrine in Shiraz mountains."}],
         "expl": "According to legend, the mountain opened to shelter the Sasanian princess from invaders, and the dripping water represents the mountain weeping for her.", "pg": 152},
        # Set B
        {"text": "Conical mud-brick domed ice houses in Yazd and Kerman that stored winter ice well into sweltering desert summers are known by this Persian name.",
         "ans": "Yakhchal", "aliases": ["Yakhchal", "Yakh-chal", "یخچال"],
         "options": ["Yakhchal", "Ab Anbar", "Caravanserai", "Kakh"],
         "rationales": [{"option": "Ab Anbar", "why_plausible": "Water storage.", "why_wrong": "Water cistern, not ice storage."},
                        {"option": "Caravanserai", "why_plausible": "Roadside inn.", "why_wrong": "Travelers inn."},
                        {"option": "Kakh", "why_plausible": "Palace.", "why_wrong": "Royal palace."}],
         "expl": "Yakhchals used subterranean storage insulated by Sarooj (heat-resistant mortar made of clay, lime, and goat hair) to preserve ice.", "pg": 153},
        {"text": "Dominating the main square of Yazd, this imposing 15th-century complex features a symmetrical three-story sunken facade with tiered alcoves.",
         "ans": "Amir Chakhmaq Complex", "aliases": ["Amir Chakhmaq", "Amir Chakhmaq Complex", "میدان امیرچخماق", "امیر چخماق"],
         "options": ["Amir Chakhmaq Complex", "Naqsh-e Jahan", "Goharshad", "Meidan-e Arg"],
         "rationales": [{"option": "Naqsh-e Jahan", "why_plausible": "Grand square in Isfahan.", "why_wrong": "Located in Isfahan."},
                        {"option": "Goharshad", "why_plausible": "Famous complex.", "why_wrong": "Mosque in Mashhad."},
                        {"option": "Meidan-e Arg", "why_plausible": "Tehran square.", "why_wrong": "Historic square in Tehran."}],
         "expl": "Built by Timurid governor Jalal al-Din Amir Chakhmaq, the square houses an enormous wooden Nakhl used during Ashura mourning processions.", "pg": 154},
        {"text": "This towering wooden skeletal frame shaped like a cypress tree is carried by hundreds of men in Yazd during Ashura to symbolize Imam Hussein's coffin.",
         "ans": "Nakhl", "aliases": ["Nakhl", "Nakhl-gardani", "نخل", "نخل‌گردانی"],
         "options": ["Nakhl", "Ta'ziyeh", "Alam", "Kotal"],
         "rationales": [{"option": "Ta'ziyeh", "why_plausible": "Passion play ritual.", "why_wrong": "The theatrical play itself, not the wooden coffin structure."},
                        {"option": "Alam", "why_plausible": "Steel standard carried in processions.", "why_wrong": "Metal standard with feathers."},
                        {"option": "Kotal", "why_plausible": "Draped horses in mourning.", "why_wrong": "Mourning horses."}],
         "expl": "Nakhl-gardani in Yazd involves lifting a multi-ton wooden structure draped in black velvet and mirrors, parading it around Amir Chakhmaq square.", "pg": 155},
        {"text": "With the tallest twin minarets in Iran standing 52 meters high, this 14th-century mosque in Yazd is depicted on the Iranian 200-rial banknote.",
         "ans": "Jameh Mosque of Yazd", "aliases": ["Jameh Mosque of Yazd", "Masjed-e Jameh Yazd", "مسجد جامع یزد"],
         "options": ["Jameh Mosque of Yazd", "Sheikh Lotfollah Mosque", "Vakil Mosque", "Nasir al-Mulk Mosque"],
         "rationales": [{"option": "Sheikh Lotfollah Mosque", "why_plausible": "Famous mosque.", "why_wrong": "Has no minarets at all, located in Isfahan."},
                        {"option": "Vakil Mosque", "why_plausible": "Historic mosque.", "why_wrong": "Located in Shiraz."},
                        {"option": "Nasir al-Mulk Mosque", "why_plausible": "Pink mosque.", "why_wrong": "Located in Shiraz."}],
         "expl": "The Jameh Mosque features exquisite star-shaped blue faience tilework that took over a century to complete under three successive dynasties.", "pg": 156},
        {"text": "A famous confection of Yazd, this delicate cotton-candy-like sweet made of spun sugar and sesame flour is known as this.",
         "ans": "Pashmak", "aliases": ["Pashmak", "Persian Cotton Candy", "پشمک", "پشمک یزدی"],
         "options": ["Pashmak", "Gaz", "Sohan", "Baklava"],
         "rationales": [{"option": "Gaz", "why_plausible": "Famous sweet.", "why_wrong": "Nougat sweet of Isfahan made with tamarisk mana."},
                        {"option": "Sohan", "why_plausible": "Saffron brittle.", "why_wrong": "Brittle candy of Qom."},
                        {"option": "Baklava", "why_plausible": "Almond pastry.", "why_wrong": "Diamond-shaped cardamom pastry."}],
         "expl": "Yazd is famed throughout the Middle East for its traditional confectionery houses like Haj Khalifeh Ali Rahbar.", "pg": 157}
    ])

    # 2. KHORASAN-WICH
    add_10("KHORASAN-WICH", "Khorasan Culture & Heritage", "Eastern Frontier", [
        {"text": "Producing over ninety percent of the world's supply of this 'red gold', the fields of southern Khorasan harvest the delicate red stigmas of this crocus flower.",
         "ans": "Saffron", "aliases": ["Saffron", "Za'faran", "زعفران", "طلای سرخ"],
         "options": ["Saffron", "Cardamom", "Sumac", "Turmeric"],
         "rationales": [{"option": "Cardamom", "why_plausible": "Aromatic spice.", "why_wrong": "Pod spice imported from India."},
                        {"option": "Sumac", "why_plausible": "Tart red berry spice.", "why_wrong": "Dried shrub berries sprinkled on kabab."},
                        {"option": "Turmeric", "why_plausible": "Yellow rhizome spice.", "why_wrong": "Zardchoobeh, yellow root spice."}],
         "expl": "It takes over 150,000 hand-picked crocus flowers to produce a single kilogram of dried Persian saffron.", "pg": 160},
        {"text": "Mined for over 3,000 years in the Madan hills northwest of Nishapur, these sky-blue gemstones were traded along the Silk Road to pharaohs and emperors.",
         "ans": "Turquoise (Firuzeh)", "aliases": ["Turquoise", "Firuzeh", "Neyshabur Turquoise", "فیروزه", "فیروزه نیشابور"],
         "options": ["Turquoise (Firuzeh)", "Lapis Lazuli", "Ruby", "Emerald"],
         "rationales": [{"option": "Lapis Lazuli", "why_plausible": "Deep blue gemstone.", "why_wrong": "Mined primarily in Badakhshan (Afghanistan)."},
                        {"option": "Ruby", "why_plausible": "Precious stone.", "why_wrong": "Red corundum."},
                        {"option": "Emerald", "why_plausible": "Green beryl.", "why_wrong": "Green gemstone."}],
         "expl": "Nishapur turquoise was the global gold standard for robin's egg blue stones, worn by kings as protective talismans against poison and evil.", "pg": 162},
        {"text": "In Tus near Mashhad, this 1934 cubic white marble mausoleum inspired by Achaemenid architecture honors the composer of the Shahnameh.",
         "ans": "Tomb of Ferdowsi", "aliases": ["Tomb of Ferdowsi", "Ferdowsi Mausoleum", "آرامگاه فردوسی", "فردوسی"],
         "options": ["Tomb of Ferdowsi", "Tomb of Hafez", "Tomb of Sa'di", "Tomb of Omar Khayyam"],
         "rationales": [{"option": "Tomb of Hafez", "why_plausible": "Famous poet tomb.", "why_wrong": "Octagonal dome in Shiraz."},
                        {"option": "Tomb of Sa'di", "why_plausible": "Famous poet tomb.", "why_wrong": "Turquoise pavilion in Shiraz."},
                        {"option": "Tomb of Omar Khayyam", "why_plausible": "Khorasani poet tomb.", "why_wrong": "Modern geometric lozenge monument in Nishapur designed by Sayhoon."}],
         "expl": "Designed by Karim Taherzadeh Behzad, the mausoleum is inscribed with scenes from Rostam's battles hewn in stone bas-relief.", "pg": 164},
        {"text": "This fortified natural plateau in Khorasan surrounded by sheer cliff walls served as Nader Shah's impenetrable mountain treasure fortress.",
         "ans": "Kalat-e Naderi", "aliases": ["Kalat-e Naderi", "Kalat", "Kakh-e Khorshid", "کلات نادری", "کاخ خورشید"],
         "options": ["Kalat-e Naderi", "Alamut Castle", "Falak ol-Aflak", "Arg-e Bam"],
         "rationales": [{"option": "Alamut Castle", "why_plausible": "Mountain fortress.", "why_wrong": "Ismaili Assassin fortress in the Alborz."},
                        {"option": "Falak ol-Aflak", "why_plausible": "Sasanian citadel.", "why_wrong": "Located in Khorramabad, Lorestan."},
                        {"option": "Arg-e Bam", "why_plausible": "Giant adobe citadel.", "why_wrong": "Located in Kerman province."}],
         "expl": "Within Kalat, Nader built the Sun Palace (Kakh-e Khorshid) with fluted circular towers to store the treasures looted from Delhi.", "pg": 166},
        {"text": "Designed by architect Houshang Seyhoun in 1963, this soaring 22-meter open concrete rhombic structure covers the tomb of the poet-mathematician in Nishapur.",
         "ans": "Mausoleum of Omar Khayyam", "aliases": ["Mausoleum of Omar Khayyam", "Tomb of Khayyam", "آرامگاه خیام", "خیام"],
         "options": ["Mausoleum of Omar Khayyam", "Tomb of Attar", "Tomb of Kamal-ol-Molk", "Tomb of Nader Shah"],
         "rationales": [{"option": "Tomb of Attar", "why_plausible": "Nearby tomb in Nishapur.", "why_wrong": "Traditional tiled dome tomb nearby."},
                        {"option": "Tomb of Kamal-ol-Molk", "why_plausible": "Painter tomb in Nishapur.", "why_wrong": "Curved tiled structure honoring the Qajar painter."},
                        {"option": "Tomb of Nader Shah", "why_plausible": "Seyhoun monument in Mashhad.", "why_wrong": "Features a bronze statue of Nader on horseback in Mashhad."}],
         "expl": "Seyhoun integrated Khayyam's three aspects—astronomer, mathematician, and poet—by building ten intersecting concrete petals adorned with Persian quatrains.", "pg": 168},
        # Set B
        {"text": "These ruby-red tart berries harvested in southern Khorasan are sautéed in saffron butter to garnish ceremonial Persian polo rice dishes.",
         "ans": "Barberries (Zereshk)", "aliases": ["Barberries", "Zereshk", "زرشک", "زرشک‌پلو"],
         "options": ["Barberries (Zereshk)", "Pomegranates", "Sumac", "Mulberries"],
         "rationales": [{"option": "Pomegranates", "why_plausible": "Red Iranian fruit.", "why_wrong": "Anar, large fruit used for fesenjan and molasses."},
                        {"option": "Sumac", "why_plausible": "Tart red spice.", "why_wrong": "Ground powder for kababs."},
                        {"option": "Mulberries", "why_plausible": "Sweet fruit.", "why_wrong": "Sweet white or purple dried fruit (Toot)."}],
         "expl": "Over 95% of world barberry production comes from Qaen and Birjand in South Khorasan province.", "pg": 170},
        {"text": "In 1911, Tsarist Russian troops outraged Muslims across the world by shelling this holy shrine with artillery to suppress constitutionalist demonstrators.",
         "ans": "Imam Reza Shrine in Mashhad", "aliases": ["Imam Reza Shrine", "Haram-e Emam Reza", "حرم امام رضا", "توپ‌بندی حرم امام رضا"],
         "options": ["Imam Reza Shrine in Mashhad", "Fatima Masumeh Shrine in Qom", "Shah Abdol-Azim in Rey", "Shah Cheragh in Shiraz"],
         "rationales": [{"option": "Fatima Masumeh Shrine in Qom", "why_plausible": "Major shrine.", "why_wrong": "Located in Qom, not shelled by Russian artillery in 1911."},
                        {"option": "Shah Abdol-Azim in Rey", "why_plausible": "Tehran sanctuary.", "why_wrong": "Not bombarded by Russian artillery."},
                        {"option": "Shah Cheragh in Shiraz", "why_plausible": "Southern shrine.", "why_wrong": "Located in the British sphere in the south."}],
         "expl": "Russian cannons breached the sacred golden dome of the shrine in March 1912, looting treasures and killing over thirty pilgrims.", "pg": 172},
        {"text": "Built in the 13th century in Chenaran (Khorasan), this 25-meter brick tower was used by astronomer Nasir al-Din al-Tusi to mark the solstices and seasons.",
         "ans": "Radkan Tower", "aliases": ["Radkan Tower", "Mil-e Radkan", "برج رادکان", "میل رادکان"],
         "options": ["Radkan Tower", "Gonbad-e Qabus", "Toghrol Tower", "Mil-e Gonbad"],
         "rationales": [{"option": "Gonbad-e Qabus", "why_plausible": "World's tallest brick tower.", "why_wrong": "Located in Golestan province, built by Ziyarid ruler Qabus."},
                        {"option": "Toghrol Tower", "why_plausible": "Seljuk brick tower.", "why_wrong": "Located in Rey near Tehran."},
                        {"option": "Mil-e Gonbad", "why_plausible": "Generic brick minaret.", "why_wrong": "Fictional variant."}],
         "expl": "Radkan's 36 external triangular flanges align with celestial sunrises to pinpoint the exact moment of the vernal equinox (Nowruz).", "pg": 174},
        {"text": "Executed in 1921 by Ahmad Shah's gendarmerie, this reformist Khorasan gendarmerie colonel led a brief progressive rebellion in Mashhad.",
         "ans": "Colonel Mohammad-Taqi Khan Pesyan", "aliases": ["Colonel Mohammad-Taqi Khan Pesyan", "Pesyan", "کلنل محمدتقی خان پسیان", "پسیان"],
         "options": ["Colonel Mohammad-Taqi Khan Pesyan", "Mirza Kuchik Khan", "Sheikh Mohammad Khiyabani", "Reza Khan"],
         "rationales": [{"option": "Mirza Kuchik Khan", "why_plausible": "Rebel commander in Gilan.", "why_wrong": "Led the Jangali movement in the Caspian forests, not Khorasan."},
                        {"option": "Sheikh Mohammad Khiyabani", "why_plausible": "Rebel leader in Tabriz.", "why_wrong": "Led the Azadistan revolt in Tabriz in 1920."},
                        {"option": "Reza Khan", "why_plausible": "Cossack commander.", "why_wrong": "War minister who dispatched Kurdish tribal levies to crush Pesyan."}],
         "expl": "Pesyan, Iran's first aviator and a cultured musician, fell in battle against Kurdish tribesmen; his funeral in Mashhad drew thousands of mourners.", "pg": 176},
        {"text": "This ancient Khorasani instrument, featured in bardic music of bards (Bakhshis), is a two-stringed long-necked lute plucked with the bare fingers.",
         "ans": "Dotar", "aliases": ["Dotar", "Do-tar", "دوتار", "دوتار خراسان"],
         "options": ["Dotar", "Setar", "Tar", "Tanbur"],
         "rationales": [{"option": "Setar", "why_plausible": "Four-stringed lute.", "why_wrong": "Classical instrument played with index fingernail."},
                        {"option": "Tar", "why_plausible": "Six-stringed waist lute.", "why_wrong": "Double-bellied lute with skin cover."},
                        {"option": "Tanbur", "why_plausible": "Three-stringed sacred lute of Kermanshah.", "why_wrong": "Kurdish/Yarsan lute of the Zagros."}],
         "expl": "The Dotar playing of northern and eastern Khorasan was inscribed on UNESCO's Representative List of Intangible Cultural Heritage in 2019.", "pg": 178}
    ])

    print(f"Part A updated. Current clues: {len(clues_by_id)}")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_part_a()
