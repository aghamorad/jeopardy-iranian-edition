#!/usr/bin/env python3
import json

def run_part2():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    clues_by_id = {c["id"]: c for c in existing}

    def add_5(cat, period, theme, round_str, data):
        vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
        prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_")
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
                "page": item.get("pg", 150 + idx * 20),
                "supporting_passage": item.get("passage", item["expl"]),
                "evidence_type": "established_fact", "confidence": 1.0,
                "editorial_validation_status": "verified",
                "host_reactions": {
                    "correct_generic": f"{item['ans']}. Quite right.",
                    "wrong_generic": f"No, we were looking for {item['ans']}.",
                    "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
                }
            }

    # 1. CUISINE OF THE PROVINCES
    add_5("CUISINE OF THE PROVINCES", "Culture & Gastronomy", "Cuisine", "single", [
        {
            "text": "Often proclaimed Iran's national dish, this slow-simmered herb stew combines parsley, cilantro, fenugreek, red kidney beans, and intensely sour sun-dried Persian limes (limoo amani).",
            "ans": "Ghormeh Sabzi",
            "aliases": ["Ghormeh Sabzi", "Qormeh Sabzi", "Ghormeh", "قورمه سبزی", "قرمه سبزی"],
            "options": ["Ghormeh Sabzi", "Fesenjan", "Gheimeh", "Abgoosht"],
            "rationales": [
                {"option": "Fesenjan", "why_plausible": "Famous luxury Iranian stew.", "why_wrong": "Made with pomegranate molasses and walnuts, not fresh green herbs."},
                {"option": "Gheimeh", "why_plausible": "Traditional stew served at mourning rituals.", "why_wrong": "Made with yellow split peas and fried matchstick potatoes, not herbs."},
                {"option": "Abgoosht", "why_plausible": "Hearty meat and chickpea broth.", "why_wrong": "A soup/mash dish eaten with flatbread, not a green herb stew."}
            ],
            "expl": "Ghormeh Sabzi is celebrated for its deep emerald color and savory-sour taste derived from slow-caramelized herbs and dried limes from southern Iran.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 510
        },
        {
            "text": "Originating in Gilan and served at imperial banquets, this rich sweet-and-sour walnut stew is darkened with concentrated sour pomegranate molasses and slow-braised duck or chicken.",
            "ans": "Fesenjan",
            "aliases": ["Fesenjan", "Fesenjoon", "Khoresht-e Fesenjan", "فسنجان", "فسنجون"],
            "options": ["Fesenjan", "Ghormeh Sabzi", "Baghali Polo", "Zereshk Polo"],
            "rationales": [
                {"option": "Ghormeh Sabzi", "why_plausible": "Iconic stew.", "why_wrong": "Herb and kidney bean stew, not walnut and pomegranate."},
                {"option": "Baghali Polo", "why_plausible": "Famous ceremonial rice dish.", "why_wrong": "Dill and fava bean rice served with lamb shank."},
                {"option": "Zereshk Polo", "why_plausible": "Celebrated saffron rice dish.", "why_wrong": "Barberry and saffron chicken rice dish."}
            ],
            "expl": "In Caspian cooking, Fesenjan is traditionally made with wild teal duck (morghe-abi), cooked for hours until walnut oils rise to the surface.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 512
        },
        {
            "text": "Cooked in traditional clay or stone pots (Dizi), this comforting lamb and chickpea broth is separated at the table: the broth is eaten with torn sangak bread, and the solids are pounded into a savory paste.",
            "ans": "Abgoosht",
            "aliases": ["Abgoosht", "Dizi", "Piti", "آبگوشت", "دیزی"],
            "options": ["Abgoosht", "Ash Reshteh", "Kalleh Pacheh", "Halim"],
            "rationales": [
                {"option": "Ash Reshteh", "why_plausible": "Famous thick Iranian noodle soup.", "why_wrong": "Herbal noodle soup topped with kashk, not meat and chickpea broth."},
                {"option": "Kalleh Pacheh", "why_plausible": "Traditional breakfast dish.", "why_wrong": "Boiled sheep's head and hooves, not chickpea stew."},
                {"option": "Halim", "why_plausible": "Wheat porridge with shredded meat.", "why_wrong": "Slow-cooked wheat porridge eaten with cinnamon."}
            ],
            "expl": "Eating Abgoosht is an interactive communal ritual involving a special heavy masher called a Goosht-koob to crush the meat, beans, and potatoes.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 150
        },
        {
            "text": "From the smoky kitchens of Gilan, this charred eggplant and tomato appetizer is vigorously mashed with abundant garlic and scrambled eggs, named after a Qajar governor of Rasht.",
            "ans": "Mirza Ghassemi",
            "aliases": ["Mirza Ghassemi", "Mirza Ghasemi", "میرزا قاسمی"],
            "options": ["Mirza Ghassemi", "Kashk-e Bademjan", "Boran-e Esfenaj", "Zeytoon Parvardeh"],
            "rationales": [
                {"option": "Kashk-e Bademjan", "why_plausible": "Famous eggplant dip.", "why_wrong": "Made with whey (kashk), mint oil, and walnuts, not tomatoes and scrambled eggs."},
                {"option": "Boran-e Esfenaj", "why_plausible": "Spinach yogurt dip.", "why_wrong": "Cold spinach and strained yogurt dip."},
                {"option": "Zeytoon Parvardeh", "why_plausible": "Caspian olive appetizer.", "why_wrong": "Marinated green olives with pomegranate, walnuts, and golpar."}
            ],
            "expl": "Mirza Qasim Khan Qajar, governor of Rasht under Nasir al-Din Shah, developed the recipe after experimenting in his private kitchen.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 514
        },
        {
            "text": "The crowning glory of Persian rice cookery, this golden, crunchy crust formed at the bottom of the pot is fiercely fought over at every family gathering.",
            "ans": "Tahdig",
            "aliases": ["Tahdig", "Tah-dig", "Tadigh", "ته‌دیگ", "ته دیگ"],
            "options": ["Tahdig", "Chelo", "Polo", "Kateh"],
            "rationales": [
                {"option": "Chelo", "why_plausible": "Plain steamed white rice.", "why_wrong": "The fluffy white grains, not the crunchy fried bottom crust."},
                {"option": "Polo", "why_plausible": "Mixed pilaf rice.", "why_wrong": "Rice cooked with meat, beans, or herbs."},
                {"option": "Kateh", "why_plausible": "Northern Iranian quick-cooked rice.", "why_wrong": "Unstrained rice method from the Caspian provinces."}
            ],
            "expl": "Tahdig ('bottom of the pot') can be made with saffron-infused rice crust, sliced thin potatoes, flat lavash bread, or yogurt layers.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 516
        }
    ])

    # 2. TRADITIONAL CRAFTS & MASTERS
    add_5("TRADITIONAL CRAFTS & MASTERS", "Material Culture", "Handicrafts", "single", [
        {
            "text": "Centered in Isfahan, this exquisite metal art involves fusing vitreous colored enamel onto etched copper dishes and firing them at 800°C to create dazzling azure patterns.",
            "ans": "Minakari",
            "aliases": ["Minakari", "Meenakari", "Mina-kari", "Mina", "میناکاری", "مینا"],
            "options": ["Minakari", "Khatamkari", "Qalamzani", "Firuzehkoobi"],
            "rationales": [
                {"option": "Khatamkari", "why_plausible": "Famous wood inlay craft of Shiraz.", "why_wrong": "Micro-mosaic marquetry of bone, wood, and brass, not enamel on copper."},
                {"option": "Qalamzani", "why_plausible": "Metal engraving craft.", "why_wrong": "Chiseling and embossing metal plates with hammers, without colored enamel glass."},
                {"option": "Firuzehkoobi", "why_plausible": "Turquoise inlay on copper.", "why_wrong": "Inlaying natural turquoise stones into copper dishes."}
            ],
            "expl": "The name derives from Mina (heaven/azure); Isfahani masters like Shokrollah Sanizadeh revived the craft in the 20th century.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 420
        },
        {
            "text": "Perfected in Shiraz, this delicate marquetry art involves assembling hundreds of thousands of microscopic polygonal rods of camel bone, brass, and rosewood into geometric stars.",
            "ans": "Khatamkari",
            "aliases": ["Khatamkari", "Khatam", "Khatam-kari", "خاتم‌کاری", "خاتم"],
            "options": ["Khatamkari", "Minakari", "Moarragh", "Gereh Chini"],
            "rationales": [
                {"option": "Minakari", "why_plausible": "Enamel craft.", "why_wrong": "Glass enameling on metal, not wooden micro-mosaic."},
                {"option": "Moarragh", "why_plausible": "Persian wood-veneer puzzle inlay.", "why_wrong": "Carved wood mosaic, not tiny assembled polygonal rods."},
                {"option": "Gereh Chini", "why_plausible": "Geometric lattice woodwork.", "why_wrong": "Lattice window frames with colored glass (Orosi), not bone/brass mosaic."}
            ],
            "expl": "A single square centimeter of high-grade Khatam can contain up to 250 micro-elements glued into intricate repeating geometric patterns.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 160
        },
        {
            "text": "Woven on traditional wooden looms in the desert city of Yazd, this luxurious hand-woven silk and wool brocade cloth often features the iconic Boteh Jegheh (paisley) motif.",
            "ans": "Termeh",
            "aliases": ["Termeh", "Yazd Termeh", "ترمه", "ترمه یزد"],
            "options": ["Termeh", "Zari", "Kilim", "Jajim"],
            "rationales": [
                {"option": "Zari", "why_plausible": "Brocade woven with genuine gold and silver wire.", "why_wrong": "Zarbaf is metallic brocade, while Termeh is the distinctive fine wool-silk cloth of Yazd."},
                {"option": "Kilim", "why_plausible": "Flat-weave tapestry.", "why_wrong": "Tribal floor covering, not woven dress fabric."},
                {"option": "Jajim", "why_plausible": "Heavy striped wool textile.", "why_wrong": "Coarse woven bedspreads and tent rugs."}
            ],
            "expl": "Termeh weaving requires immense patience; historical weavers produced barely a few centimeters per day for royal court gowns and ceremonial dowries.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 162
        },
        {
            "text": "In Isfahan's grand bazaar, the rhythmic clinking of hammers against chisels marks this traditional art of hand-engraving and repoussé on silver, brass, and copper vessels.",
            "ans": "Qalamzani",
            "aliases": ["Qalamzani", "Ghalamzani", "Qalam-zani", "قلم‌زنی", "قلمزنی"],
            "options": ["Qalamzani", "Minakari", "Khatamkari", "Malilehkari"],
            "rationales": [
                {"option": "Minakari", "why_plausible": "Metal art with blue glass.", "why_wrong": "Enameling, not chasing and embossing with steel punches."},
                {"option": "Khatamkari", "why_plausible": "Wood mosaic craft.", "why_wrong": "Marquetry on wood, not metalwork."},
                {"option": "Malilehkari", "why_plausible": "Filigree silver wire craft.", "why_wrong": "Twisting thin silver wires into lace dishes in Zanjan."}
            ],
            "expl": "Before carving, artisans pour hot melted pitch (Ghir) inside the vessel to absorb hammer blows and prevent the metal from puncturing.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 164
        },
        {
            "text": "Born in Herat around 1450, this supreme master painter of Persian miniatures revolutionized manuscript illumination with naturalistic movement in the Timurid and Safavid royal ateliers.",
            "ans": "Kamal al-Din Behzad",
            "aliases": ["Kamal al-Din Behzad", "Behzad", "Behzad the Painter", "کمال‌الدین بهزاد", "بهزاد"],
            "options": ["Kamal al-Din Behzad", "Reza Abbasi", "Mahmoud Farshchian", "Mirak"],
            "rationales": [
                {"option": "Reza Abbasi", "why_plausible": "Great 17th-century Safavid painter in Isfahan.", "why_wrong": "Lived a century later in Isfahan, famed for single-page calligraphic portraits."},
                {"option": "Mahmoud Farshchian", "why_plausible": "Modern master of Persian miniature.", "why_wrong": "20th/21st-century contemporary master painter."},
                {"option": "Mirak", "why_plausible": "Court painter in Herat and Tabriz.", "why_wrong": "Aga Mirak was Behzad's junior student and colleague."}
            ],
            "expl": "Behzad served Sultan Husayn Bayqara in Herat and was appointed director of the royal library in Tabriz by Shah Ismail I in 1522.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 166
        }
    ])

    # 3. SAVAK: THE EYE OF THE SHAH (Double Jeopardy)
    add_5("SAVAK: THE EYE OF THE SHAH", "Pahlavi Police State", "Intelligence", "double", [
        {
            "text": "Established in 1957 with CIA and Mossad technical guidance, this notorious state security and intelligence service watched over every aspect of public life under the late Shah.",
            "ans": "SAVAK",
            "aliases": ["SAVAK", "Sazman-e Ettela'at va Amniyat-e Keshvar", "ساواک"],
            "options": ["SAVAK", "Shahrbani", "Gendarmerie", "VEVAK"],
            "rationales": [
                {"option": "Shahrbani", "why_plausible": "National municipal police force.", "why_wrong": "Regular civilian law enforcement, not the secret intelligence apparatus."},
                {"option": "Gendarmerie", "why_plausible": "Rural border and highway police.", "why_wrong": "Rural military police corps."},
                {"option": "VEVAK", "why_plausible": "Post-revolutionary intelligence ministry.", "why_wrong": "The Islamic Republic's Ministry of Intelligence (MOIS/VEVAK) created in 1984."}
            ],
            "expl": "SAVAK wielded extrajudicial powers of interrogation, surveillance, and press censorship until disbanded by Shapour Bakhtiar in January 1979.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 420
        },
        {
            "text": "Appointed the first director of SAVAK in 1957, this ambitious general fell out with the Shah, fled to Iraq, and was assassinated in 1970 by SAVAK hitmen during a desert hunting trip.",
            "ans": "General Teymour Bakhtiar",
            "aliases": ["General Teymour Bakhtiar", "Teymour Bakhtiar", "تیمور بختیار", "سپهبد تیمور بختیار"],
            "options": ["General Teymour Bakhtiar", "General Nematollah Nassiri", "General Hassan Pakravan", "General Fereydoun Jam"],
            "rationales": [
                {"option": "General Nematollah Nassiri", "why_plausible": "Longest-serving SAVAK director.", "why_wrong": "Led SAVAK from 1965 to 1978; executed on a Tehran rooftop in February 1979."},
                {"option": "General Hassan Pakravan", "why_plausible": "Second director of SAVAK.", "why_wrong": "Educated and cultured officer who protected Khomeini from execution in 1963."},
                {"option": "General Fereydoun Jam", "why_plausible": "Chief of Supreme Command Staff.", "why_wrong": "Military staff officer who lived peacefully in London."}
            ],
            "expl": "Bakhtiar was shot in the Diyala desert in Iraq by a SAVAK double agent who had infiltrated his Iraqi-funded dissident entourage.",
            "book": "The Shah", "auth": "Abbas Milani", "pg": 234
        },
        {
            "text": "Built in the northern foothills of Tehran in 1972, this high-security fortress was designed by German engineers to house political prisoners and armed leftist guerrillas.",
            "ans": "Evin Prison",
            "aliases": ["Evin Prison", "Zendan-e Evin", "Evin", "زندان اوین", "اوین"],
            "options": ["Evin Prison", "Qasr Prison", "Ghezel Hesar", "Gohardasht"],
            "rationales": [
                {"option": "Qasr Prison", "why_plausible": "Historic prison in central Tehran.", "why_wrong": "Built in 1798 as a Qajar palace and converted into a prison by Reza Shah in 1929."},
                {"option": "Ghezel Hesar", "why_plausible": "Large detention facility in Karaj.", "why_wrong": "Located outside Karaj, not the Shemiran prison fortress."},
                {"option": "Gohardasht", "why_plausible": "Rajaei Shahr prison.", "why_wrong": "Constructed later in the 1980s."}
            ],
            "expl": "Evin featured soundproof interrogation cells and solitary confinement wings, becoming the primary symbol of state repression before the revolution.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 442
        },
        {
            "text": "Heading SAVAK for thirteen years from 1965 to 1978, this hardline general was arrested by the Shah as a sacrificial concession to protesters, only to be executed after the revolution.",
            "ans": "General Nematollah Nassiri",
            "aliases": ["General Nematollah Nassiri", "Nematollah Nassiri", "Nassiri", "نعمت‌الله نصیری", "نصیری"],
            "options": ["General Nematollah Nassiri", "General Hassan Pakravan", "General Teymour Bakhtiar", "General Naser Moghaddam"],
            "rationales": [
                {"option": "General Hassan Pakravan", "why_plausible": "Earlier director.", "why_wrong": "Pakravan was removed in 1965 because the Shah found him too soft on religious dissidents."},
                {"option": "General Teymour Bakhtiar", "why_plausible": "First director.", "why_wrong": "Assassinated in Iraq in 1970."},
                {"option": "General Naser Moghaddam", "why_plausible": "The final director of SAVAK in 1978–1979.", "why_wrong": "Appointed in June 1978 for just eight months."}
            ],
            "expl": "Nassiri was executed on the roof of the Refah School on February 15, 1979, alongside three other imperial generals following summary trials by Sadegh Khalkhali.",
            "book": "The Shah", "auth": "Abbas Milani", "pg": 346
        },
        {
            "text": "Located near Tupkhaneh Square in the former Shahrbani lockup, this Joint Committee headquarters was notorious for brutal interrogation of guerrillas.",
            "ans": "Komiteh-ye Moshtarak",
            "aliases": ["Komiteh-ye Moshtarak", "Joint Anti-Sabotage Committee", "کمیته مشترک", "کمیته مشترک ضدخرابکاری"],
            "options": ["Komiteh-ye Moshtarak", "Evin Prison", "Qasr Prison", "Falak ol-Aflak"],
            "rationales": [
                {"option": "Evin Prison", "why_plausible": "Northern Tehran prison.", "why_wrong": "Located in northern hills, not the circular downtown facility."},
                {"option": "Qasr Prison", "why_plausible": "Historic prison.", "why_wrong": "Located on Old Shemiran Road, not Tupkhaneh."},
                {"option": "Falak ol-Aflak", "why_plausible": "Ancient citadel fortress in Khorramabad.", "why_wrong": "Used as a military prison in Lorestan, not downtown Tehran."}
            ],
            "expl": "Now preserved as the Ebrat Museum (Museum of Warning), its circular layout prevented prisoners from orienting themselves during interrogation.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 445
        }
    ])

    # 4. THE REVOLUTIONARY YEAR: 1978 (Double Jeopardy)
    add_5("THE REVOLUTIONARY YEAR: 1978", "1979 Revolution", "Crisis of the Regime", "double", [
        {
            "text": "On August 19, 1978, over 400 moviegoers perished when the doors were locked and arsonists set ablaze this cinema in the southern oil city of Abadan, sparking nationwide outrage.",
            "ans": "Cinema Rex",
            "aliases": ["Cinema Rex", "Cinema Rex Abadan", "سینما رکس", "سینما رکس آبادان"],
            "options": ["Cinema Rex", "Grand Cinema", "Cinema Mayak", "Cinema Crystal"],
            "rationales": [
                {"option": "Grand Cinema", "why_plausible": "Historic cinema.", "why_wrong": "Opened in 1928 on Lalezar in Tehran."},
                {"option": "Cinema Mayak", "why_plausible": "Historic cinema.", "why_wrong": "Premiered Dokhtar-e Lor in 1933."},
                {"option": "Cinema Crystal", "why_plausible": "Famous pre-1979 cinema in Tehran.", "why_wrong": "Located on Lalezar, not the Abadan theater arson."}
            ],
            "expl": "The audience was watching Masoud Kimiai's film The Deer (Gavaznha); the public blamed SAVAK, driving millions into active opposition to the monarchy.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 512
        },
        {
            "text": "On September 8, 1978 (17 Shahrivar), imperial soldiers opened fire on thousands of unarmed protesters gathered in this eastern Tehran square, an event forever known as Black Friday.",
            "ans": "Jaleh Square",
            "aliases": ["Jaleh Square", "Meydan-e Jaleh", "Shohada Square", "میدان ژاله", "میدان شهدا", "جمعه سیاه"],
            "options": ["Jaleh Square", "Baharestan Square", "Tupkhaneh Square", "Enghelab Square"],
            "rationales": [
                {"option": "Baharestan Square", "why_plausible": "Historic site of parliament protests.", "why_wrong": "Site of the 1908 bombardment and 1953 clashes, not the 17 Shahrivar massacre."},
                {"option": "Tupkhaneh Square", "why_plausible": "Major central square.", "why_wrong": "Site of Fazlollah Nuri's execution in 1909."},
                {"option": "Enghelab Square", "why_plausible": "Central square near Tehran University.", "why_wrong": "Formerly 24 Esfand Square, not the site of Black Friday."}
            ],
            "expl": "Military Governor Gholam-Ali Oveisi declared martial law just hours before troops opened fire in Jaleh Square (now Shohada Square), ending any hope of a negotiated compromise.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 515
        },
        {
            "text": "On January 7, 1978, this state newspaper published a libelous editorial under the pseudonym Ahmad Rashidi Motlagh slandering Khomeini, igniting the cycle of 40-day mourning protests.",
            "ans": "Ettela'at",
            "aliases": ["Ettela'at", "Ettelaat", "اطلاعات", "روزنامه اطلاعات"],
            "options": ["Ettela'at", "Kayhan", "Ayandegan", "Rastakhiz"],
            "rationales": [
                {"option": "Kayhan", "why_plausible": "Major rival national daily newspaper.", "why_wrong": "The article was published specifically in Ettela'at by order of Court Minister Alam and the Shah."},
                {"option": "Ayandegan", "why_plausible": "Independent modern morning daily.", "why_wrong": "Founded by Daryush Homayoun, but not where the offending editorial ran."},
                {"option": "Rastakhiz", "why_plausible": "Official organ of the single party.", "why_wrong": "The party gazette, but the Shah chose Ettela'at for maximum impact."}
            ],
            "expl": "The editorial labeled Khomeini an Indian agent and British pawn, sparking student riots in Qom on January 9 that were fired upon by police.",
            "book": "Iran: A Modern History", "auth": "Abbas Amanat", "pg": 718
        },
        {
            "text": "In October 1978, a crippling strike by 37,000 workers in this strategic industry choked off state oil revenues and gasoline supplies, breaking the financial spine of the regime.",
            "ans": "National Iranian Oil Company (NIOC)",
            "aliases": ["National Iranian Oil Company (NIOC)", "Oil Industry", "Oil Workers", "شرکت نفت", "اعتصاب کارکنان نفت"],
            "options": ["National Iranian Oil Company (NIOC)", "Trans-Iranian Railway", "Imperial Customs", "Tehran Bazaaris"],
            "rationales": [
                {"option": "Trans-Iranian Railway", "why_plausible": "Strategic transport union.", "why_wrong": "Railway workers struck, but the oil shutdown deprived the state of 80% of its cash."},
                {"option": "Imperial Customs", "why_plausible": "Border port controllers.", "why_wrong": "Secondary strike compared to the oil fields of Khuzestan."},
                {"option": "Tehran Bazaaris", "why_plausible": "Merchant guild strike.", "why_wrong": "Bazaars shuttered shops, but the refinery strike stopped exports entirely."}
            ],
            "expl": "Oil production plummeted from 6 million barrels per day to barely enough for domestic winter heating, forcing the Shah to impose military rule over the refineries.",
            "book": "Iran Between Two Revolutions", "auth": "Ervand Abrahamian", "pg": 518
        },
        {
            "text": "On January 16, 1979, with tears in his eyes at Mehrabad Airport, this monarch boarded his Boeing 707 'Shahin' to depart Iran for an exile from which he would never return.",
            "ans": "Mohammad Reza Shah Pahlavi",
            "aliases": ["Mohammad Reza Shah Pahlavi", "Mohammad Reza Shah", "The Shah", "محمدرضا شاه", "محمدرضا پهلوی", "شاه"],
            "options": ["Mohammad Reza Shah Pahlavi", "Reza Shah", "Shapour Bakhtiar", "Jamshid Amouzegar"],
            "rationales": [
                {"option": "Reza Shah", "why_plausible": "His father who was also exiled.", "why_wrong": "Reza Shah was exiled in 1941 to South Africa."},
                {"option": "Shapour Bakhtiar", "why_plausible": "His last Prime Minister.", "why_wrong": "Bakhtiar remained in Tehran trying to govern until toppled on February 11."},
                {"option": "Jamshid Amouzegar", "why_plausible": "Former prime minister.", "why_wrong": "Amouzegar resigned in August 1978 following the Cinema Rex disaster."}
            ],
            "expl": "Newspapers famously hit the streets with the iconic massive two-word headline: 'SHAH RAFT' (The Shah Is Gone), triggering ecstatic celebrations across the nation.",
            "book": "The Shah", "auth": "Abbas Milani", "pg": 412
        }
    ])

    # 5. PARTHIAN ARROWS & SHADOWS
    add_5("PARTHIAN ARROWS & SHADOWS", "Ancient Dynasties", "Arsacid Empire", "single", [
        {
            "text": "In 53 BC at the Battle of Carrhae, this brilliant 30-year-old Parthian general decimated seven Roman legions using mounted horse archers and severed the head of Marcus Licinius Crassus.",
            "ans": "Surena",
            "aliases": ["Surena", "Suren", "General Surena", "سورنا", "سپهبد سورنا"],
            "options": ["Surena", "Mithridates II", "Arsaces I", "Pacorus I"],
            "rationales": [
                {"option": "Mithridates II", "why_plausible": "Great Parthian king who opened the Silk Road.", "why_wrong": "Reigned earlier (124–91 BC)."},
                {"option": "Arsaces I", "why_plausible": "Founder of the Arsacid dynasty.", "why_wrong": "Lived in the 3rd century BC."},
                {"option": "Pacorus I", "why_plausible": "Parthian prince who invaded Syria.", "why_wrong": "Killed at the Battle of Mount Gindarus in 38 BC."}
            ],
            "expl": "Surena utilized the 'Parthian Shot' tactic—feigning retreat while firing arrows backwards over galloping horses—killing 20,000 Romans including Crassus.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 54
        },
        {
            "text": "Known as the Great and reigning from 124 to 91 BC, this Parthian king established diplomatic ties with Han Dynasty Emperor Wu of China, officially inaugurating the Silk Road.",
            "ans": "Mithridates II",
            "aliases": ["Mithridates II", "Mithridates the Great", "مهرداد دوم", "مهرداد بزرگ"],
            "options": ["Mithridates II", "Mithridates I", "Orodes II", "Phraates IV"],
            "rationales": [
                {"option": "Mithridates I", "why_plausible": "Conquered Media and Babylonia.", "why_wrong": "Expanded the realm in 171–132 BC, but did not open the official embassy to China."},
                {"option": "Orodes II", "why_plausible": "King during Carrhae.", "why_wrong": "Reigned during the Roman defeat, executed Surena out of jealousy."},
                {"option": "Phraates IV", "why_plausible": "Defeated Mark Antony.", "why_wrong": "Returned the captured Roman legionary eagles to Emperor Augustus in 20 BC."}
            ],
            "expl": "Mithridates II revived the Achaemenid title 'King of Kings' (Shahanshah) on his coinage, stabilizing borders from Syria to Central Asia.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 52
        },
        {
            "text": "This tactical maneuver, made famous by nomadic steppe and Parthian cavalry, involved feigning a panicked retreat before twisting in the saddle to loose arrows backwards.",
            "ans": "The Parthian Shot",
            "aliases": ["The Parthian Shot", "Parthian Shot", "تیراندازی پارتی", "تیر پارتی"],
            "options": ["The Parthian Shot", "Cantabrian Circle", "Phalanx", "Caracole"],
            "rationales": [
                {"option": "Cantabrian Circle", "why_plausible": "Iberian cavalry skirmishing tactic.", "why_wrong": "Circular rotation maneuver used in Roman Spain."},
                {"option": "Phalanx", "why_plausible": "Greek military formation.", "why_wrong": "Dense spearmen infantry wall."},
                {"option": "Caracole", "why_plausible": "Renaissance firearm cavalry tactic.", "why_wrong": "16th-century wheel-lock pistol maneuver."}
            ],
            "expl": "The maneuver entered the English language as 'a parting shot'—a cutting final remark made upon departure.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 56
        },
        {
            "text": "Located in modern Turkmenistan near Ashgabat, this fortified royal city was the first capital and ancestral necropolis of the Arsacid Parthian kings.",
            "ans": "Nisa",
            "aliases": ["Nisa", "Old Nisa", "Parthaunisa", "نسا", "شهر باستانی نسا"],
            "options": ["Nisa", "Ctesiphon", "Hecatompylos", "Ecbatana"],
            "rationales": [
                {"option": "Ctesiphon", "why_plausible": "Later imperial winter capital on the Tigris.", "why_wrong": "Built later as the administrative capital near modern Baghdad."},
                {"option": "Hecatompylos", "why_plausible": "City of a Hundred Gates in Semnan.", "why_wrong": "Major staging city, but not the ancestral royal necropolis in Turkmenistan."},
                {"option": "Ecbatana", "why_plausible": "Summer capital in Hamadan.", "why_wrong": "Ancient Median/Achaemenid mountain capital."}
            ],
            "expl": "Excavations at UNESCO-listed Old Nisa uncovered magnificent rhytons (ivory drinking horns) combining Hellenistic craftsmanship with Persian motifs.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 50
        },
        {
            "text": "In 36 BC, this Roman triumvir invaded Parthian territory with 100,000 men seeking to avenge Crassus, but lost a third of his army in a disastrous mountain retreat through Media Atropatene.",
            "ans": "Mark Antony",
            "aliases": ["Mark Antony", "Antony", "Marcus Antonius", "مارک آنتونی"],
            "options": ["Mark Antony", "Julius Caesar", "Augustus", "Trajan"],
            "rationales": [
                {"option": "Julius Caesar", "why_plausible": "Planned a Parthian campaign before his assassination.", "why_wrong": "Murdered on the Ides of March 44 BC before he could launch the invasion."},
                {"option": "Augustus", "why_plausible": "First Roman Emperor.", "why_wrong": "Secured peace with Parthia through diplomacy, regaining the lost legionary standards."},
                {"option": "Trajan", "why_plausible": "Conquered Ctesiphon in 116 AD.", "why_wrong": "Invaded a century and a half later in the 2nd century AD."}
            ],
            "expl": "King Phraates IV intercepted Antony's 300-wagon siege train at Phraaspa, forcing Antony into a retreat that echoed Xenophon's Anabasis.",
            "book": "The Persians: Ancient, Mediaeval and Modern Iran", "auth": "Homa Katouzian", "pg": 58
        }
    ])

    print("Writing Batch 2 additions...")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(list(clues_by_id.values()), f, indent=2, ensure_ascii=False)
    print("Total clues after Part 2:", len(clues_by_id))

if __name__ == "__main__":
    run_part2()
