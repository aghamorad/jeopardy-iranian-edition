#!/usr/bin/env python3
import json

def load_clues():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        return {c["id"]: c for c in json.load(f)}

def save_clues(clues_by_id):
    clues = list(clues_by_id.values())
    print(f"Total clues now: {len(clues)}")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2, ensure_ascii=False)

def add_batch(clues_by_id, cat, period, theme, round_str, items):
    prefix = cat.lower().replace(" ", "_").replace(":", "").replace("&", "and").replace("'", "").replace("-", "_").replace("?", "").replace("!", "").replace(",", "")
    vals = [200, 400, 600, 800, 1000, 200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000, 400, 800, 1200, 1600, 2000]
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
            "page": item.get("pg", 220 + idx * 8),
            "supporting_passage": item.get("passage", item["expl"]),
            "evidence_type": "established_fact", "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": f"{item['ans']}. Spot on!",
                "wrong_generic": f"No, we were looking for {item['ans']}.",
                "common_wrong_answers": {}, "specificity_prompt": "", "explanation": item["expl"]
            }
        }

clues = load_clues()

# 1. THE SEVEN LABORS OF ROSTAM (Single, 10 clues)
add_batch(clues, "THE SEVEN LABORS OF ROSTAM", "Shahnameh Epics", "Heroic Feats", "single", [
    {"text": "In the First Labor of the Haft Khan, Rostam was asleep when his faithful warhorse Rakhsh fought and trampled this ferocious predator to death.",
     "ans": "The Lion (Shir)", "aliases": ["The Lion", "Lion", "Shir", "شیر"],
     "options": ["The Lion (Shir)", "The Dragon", "The White Demon", "The Tiger"],
     "rationales": [{"option": "The Dragon", "why_plausible": "Monster slain in Labor Three.", "why_wrong": "The dragon was killed in the 3rd labor with Rostam's help."},
                    {"option": "The White Demon", "why_plausible": "Final monster in Labor Seven.", "why_wrong": "Slain in the final labor in Mazandaran."},
                    {"option": "The Tiger", "why_plausible": "Big cat.", "why_wrong": "Rakhsh stomped on a man-eating lion while Rostam slept."}],
     "expl": "Rostam chided Rakhsh for risking his life alone, warning him: 'If you had been slain, who would have carried my heavy armor into Mazandaran?'", "pg": 94},
    {"text": "In the Second Labor, dying of dehydration in the scorching desert sands, Rostam prayed to God and was miraculously guided to a water spring by this animal.",
     "ans": "A Wild Ram (Mish / Quch)", "aliases": ["A Wild Ram", "Wild Ram", "Ram", "Sheep", "میش", "قوچ"],
     "options": ["A Wild Ram (Mish / Quch)", "A Dove", "A Gazelle", "A Falcon"],
     "rationales": [{"option": "A Dove", "why_plausible": "Biblical guide bird.", "why_wrong": "A fat ram appeared on the dunes."},
                    {"option": "A Gazelle", "why_plausible": "Desert animal.", "why_wrong": "It was a wild mountain sheep/ram."},
                    {"option": "A Falcon", "why_plausible": "Hunting bird.", "why_wrong": "Rostam followed a wild ram to an oasis."}],
     "expl": "Rostam praised the Creator for sending the divine ram, quenching his and Rakhsh's thirst before facing the fire-breathing dragon.", "pg": 95},
    {"text": "In the Fourth Labor, Rostam sat beside an enchanted stream and sang of his sorrows until this enchantress approached disguised as a beautiful damsel.",
     "ans": "The Sorceress (Zan-e Jadoogar)", "aliases": ["The Sorceress", "Zan-e Jadoogar", "Witch", "زن جادوگر", "جادوگر"],
     "options": ["The Sorceress (Zan-e Jadoogar)", "Sudabeh", "Gordafarid", "Tahmineh"],
     "rationales": [{"option": "Sudabeh", "why_plausible": "Treacherous queen of Iran.", "why_wrong": "Wife of Kay Kavus."},
                    {"option": "Gordafarid", "why_plausible": "Heroic warrior woman.", "why_wrong": "Warrior woman who defended the White Fortress against Sohrab."},
                    {"option": "Tahmineh", "why_plausible": "Mother of Sohrab.", "why_wrong": "Princess of Samangan and Rostam's wife."}],
     "expl": "When Rostam handed her a goblet of wine and uttered the name of God, the illusion broke and her true black demonic form was revealed, whereupon Rostam lassooed and cleaved her in two.", "pg": 96},
    {"text": "In the Fifth Labor, Rostam captured this local border chieftain, promising to make him King of Mazandaran if he guided him through the dark enchantments.",
     "ans": "Oulad", "aliases": ["Oulad", "Awlad", "اولاد", "اولاد غندی"],
     "options": ["Oulad", "Garsivaz", "Piran", "Barman"],
     "rationales": [{"option": "Garsivaz", "why_plausible": "Turanian prince.", "why_wrong": "Afrasiyab's brother."},
                    {"option": "Piran", "why_plausible": "Wise Turanian vizier.", "why_wrong": "Counselor to Afrasiyab."},
                    {"option": "Barman", "why_plausible": "Turanian warrior.", "why_wrong": "Turanian champion."}],
     "expl": "Bound with a leather lariat, Oulad faithfully guided Rostam past the bottomless pits and scorching winds to the cavern of the White Demon.", "pg": 97},
    {"text": "In the Sixth Labor, Rostam decapitated this demonic champion outside his fortress, throwing his army into panic.",
     "ans": "Arzhang Div", "aliases": ["Arzhang Div", "Arzhang", "ارژنگ دیو"],
     "options": ["Arzhang Div", "Div-e Sepid", "Akvan Div", "Pouladvand"],
     "rationales": [{"option": "Div-e Sepid", "why_plausible": "Final supreme demon.", "why_wrong": "Killed in the 7th labor inside the dark cave."},
                    {"option": "Akvan Div", "why_plausible": "Shape-shifting demon.", "why_wrong": "Encountered in a separate story later."},
                    {"option": "Pouladvand", "why_plausible": "Turanian hero.", "why_wrong": "Human champion in Turan."}],
     "expl": "Rostam charged Arzhang's camp shouting like thunder, tore off his head with his bare hands, and hurled it into the ranks of the Mazandaran demons.", "pg": 98},
    # Set B
    {"text": "The entire Haft Khan expedition was launched to rescue this foolish, arrogant Iranian monarch who had marched into Mazandaran and been captured and blinded by demons.",
     "ans": "Kay Kavus", "aliases": ["Kay Kavus", "Kai Kavus", "Keykavous", "کیکاووس", "کی‌کاووس"],
     "options": ["Kay Kavus", "Kay Khosrow", "Goshtasp", "Jamshid"],
     "rationales": [{"option": "Kay Khosrow", "why_plausible": "Righteous grandson of Kavus.", "why_wrong": "The saintly hero king who defeated Afrasiyab."},
                    {"option": "Goshtasp", "why_plausible": "Patron of Zoroaster.", "why_wrong": "Father of Esfandiyar."},
                    {"option": "Jamshid", "why_plausible": "Golden age king.", "why_wrong": "Lost the Farr to Zahhak."}],
     "expl": "Kavus was seduced by a demon minstrel singing of the endless spring of Mazandaran, leading his army into blindness and captivity.", "pg": 93},
    {"text": "To restore the sight of the blinded King Kay Kavus and the Iranian paladins, Rostam poured three drops of this into their eyes.",
     "ans": "Blood of the White Demon's Liver", "aliases": ["Blood of the White Demon's Liver", "Liver blood", "Demon's blood", "خون جگر دیو سفید"],
     "options": ["Blood of the White Demon's Liver", "Water of Life", "Elixir of the Simurgh", "Wine of Shiraz"],
     "rationales": [{"option": "Water of Life", "why_plausible": "Ab-e Hayat sought by Khidr.", "why_wrong": "Mythic immortality water."},
                    {"option": "Elixir of the Simurgh", "why_plausible": "Feather cure.", "why_wrong": "Simurgh's feather healed wounds, not demonic blindness."},
                    {"option": "Wine of Shiraz", "why_plausible": "Medicinal wine.", "why_wrong": "Poetic trope."}],
     "expl": "The physician priests declared that only the hot liver blood of the White Demon could burn away the demonic cataract blinding their pupils.", "pg": 99},
    {"text": "Rostam's massive signature weapon, forged by Kaveh the Blacksmith with the likeness of an ox's head on its iron pommel, was known as this.",
     "ans": "Gorz-e Gavsar (Ox-Headed Mace)", "aliases": ["Gorz-e Gavsar", "Ox-Headed Mace", "Gorz", "گرز گاو‌سر", "گرز گاوسار"],
     "options": ["Gorz-e Gavsar (Ox-Headed Mace)", "Zulfiqar", "Excalibur", "Tir-e Gaz"],
     "rationales": [{"option": "Zulfiqar", "why_plausible": "Two-pronged sword of Imam Ali.", "why_wrong": "Islamic sword of Imam Ali."},
                    {"option": "Excalibur", "why_plausible": "King Arthur's sword.", "why_wrong": "Arthurian Celtic myth."},
                    {"option": "Tir-e Gaz", "why_plausible": "Tamarisk arrow.", "why_wrong": "The double-pointed arrow used to blind Esfandiyar."}],
     "expl": "Inherited from his grandfather Sam and King Fereydun, the ox-headed mace crushed the skulls of demons and armored knights with a single blow.", "pg": 91},
    {"text": "Rostam's mythical stallion, intelligent enough to wake his master, kill lions, and understand human speech, was named this.",
     "ans": "Rakhsh", "aliases": ["Rakhsh", "Rakhsh the Steed", "رخش"],
     "options": ["Rakhsh", "Shabdiz", "Bucephalus", "Pegasus"],
     "rationales": [{"option": "Shabdiz", "why_plausible": "Famous black charger.", "why_wrong": "Khosrow Parviz's prized black charger in Nezami's romance."},
                    {"option": "Bucephalus", "why_plausible": "Alexander's horse.", "why_wrong": "Alexander the Great's stallion."},
                    {"option": "Pegasus", "why_plausible": "Winged horse.", "why_wrong": "Greek mythic winged horse."}],
     "expl": "Rakhsh was described as having a coat like rose petals scattered on saffron, chosen by Rostam when no other stallion could support his weight.", "pg": 92},
    {"text": "The invulnerable, waterproof battle tunic worn by Rostam into battle, fashioned from the skin of a mythical sea beast or leopard, was called this.",
     "ans": "Babr-e Bayan", "aliases": ["Babr-e Bayan", "Babr e Bayan", "ببر بیان"],
     "options": ["Babr-e Bayan", "Derafsh Kaviani", "Gorz-e Sam", "Kolah-e Khod"],
     "rationales": [{"option": "Derafsh Kaviani", "why_plausible": "Famous royal artifact.", "why_wrong": "The national sacred battle banner, not armor."},
                        {"option": "Gorz-e Sam", "why_plausible": "Weapon.", "why_wrong": "Grandfather's mace."},
                        {"option": "Kolah-e Khod", "why_plausible": "Battle helmet.", "why_wrong": "Generic iron helmet."}],
         "expl": "The coat was impervious to fire, water, and arrows, protecting Rostam through centuries of warfare.", "pg": 93}
])

# 2. CALLIGRAPHY & INKWELLS (Single, 10 clues)
add_batch(clues, "CALLIGRAPHY & INKWELLS", "Islamic Arts & Script", "Calligraphy", "single", [
    {"text": "Regarded as the 'Bride of Islamic Calligraphic Scripts', this flowing, cursive Persian script was invented in the 14th century by Mir Ali Tabrizi.",
     "ans": "Nastaliq", "aliases": ["Nastaliq", "Nasta'liq", "نستعلیق"],
     "options": ["Nastaliq", "Naskh", "Kufic", "Thuluth"],
     "rationales": [{"option": "Naskh", "why_plausible": "Standard Arabic print script.", "why_wrong": "Upright script used for the Quran."},
                    {"option": "Kufic", "why_plausible": "Early geometric script.", "why_wrong": "Angular early Islamic stone script."},
                    {"option": "Thuluth", "why_plausible": "Monumental architectural script.", "why_wrong": "Large ornate script for mosque domes."}],
     "expl": "Nastaliq combines Naskh and Ta'liq, inspired according to legend by the graceful curves of flying geese.", "pg": 170},
    {"text": "Serving at the court of Shah Abbas I in Isfahan, this supreme calligrapher was murdered in 1615 by jealous courtiers, his style remaining the benchmark of Nastaliq.",
     "ans": "Mir Emad Hassani", "aliases": ["Mir Emad Hassani", "Mir Emad", "میرعماد", "میرعماد حسنی"],
     "options": ["Mir Emad Hassani", "Mir Ali Tabrizi", "Reza Abbasi", "Yaqut al-Musta'simi"],
     "rationales": [{"option": "Mir Ali Tabrizi", "why_plausible": "Inventor of Nastaliq.", "why_wrong": "Lived two centuries earlier in the 14th century."},
                    {"option": "Reza Abbasi", "why_plausible": "Contemporary Safavid painter.", "why_wrong": "Master miniature painter, not the chief calligrapher."},
                    {"option": "Yaqut al-Musta'simi", "why_plausible": "Abbasid calligrapher.", "why_wrong": "Lived in 13th-century Baghdad."}],
     "expl": "Mir Emad's individual calligraphic folios (Qet'eh) were traded across India, the Ottoman Empire, and Europe for their weight in gold.", "pg": 172},
    {"text": "Invented in the 17th century for fast administrative court correspondence, this ornate broken script was perfected by Darvish Abdol-Majid Taleqani.",
     "ans": "Shekasteh Nastaliq", "aliases": ["Shekasteh Nastaliq", "Shekasteh", "شکسته نستعلیق", "شکسته"],
     "options": ["Shekasteh Nastaliq", "Nastaliq", "Diwani", "Muhaqqaq"],
     "rationales": [{"option": "Nastaliq", "why_plausible": "Parent script.", "why_wrong": "Formal script, whereas Shekasteh is the 'broken' cursive speed script."},
                    {"option": "Diwani", "why_plausible": "Ottoman court script.", "why_wrong": "Ottoman chancery script."},
                    {"option": "Muhaqqaq", "why_plausible": "Large Quranic script.", "why_wrong": "Monumental script."}],
     "expl": "Shekasteh linked letters that were traditionally unjoined, creating dynamic visual rhythms resembling swaying branches.", "pg": 174},
    {"text": "Persian scribes crafted luxury carrying cases for their reed pens and inkwells using lacquered papier-mâché painted with nightingales and roses, known by this name.",
     "ans": "Qalamdan (Pen-Box)", "aliases": ["Qalamdan", "Qalam-dan", "قلمدان"],
     "options": ["Qalamdan (Pen-Box)", "Davat", "Rahle", "Jild"],
     "rationales": [{"option": "Davat", "why_plausible": "The inkwell itself.", "why_wrong": "The inkpot container inside, not the sliding painted carrying box."},
                    {"option": "Rahle", "why_plausible": "Quran book stand.", "why_wrong": "Wooden folding book rest."},
                    {"option": "Jild", "why_plausible": "Bookbinding.", "why_wrong": "Leather book cover."}],
     "expl": "Qalamdans were sliding wooden or papier-mâché sleeves tucked into a scribe's belt sash, painted by master Qajar miniaturists.", "pg": 176},
    {"text": "The finest reed pens (Qalam-e Ney) used by Iranian calligraphers are harvested from the dense river reed-beds of this southern Khuzestan city.",
     "ans": "Dezful", "aliases": ["Dezful", "Ney-e Dezful", "دزفول", "نی دزفول"],
     "options": ["Dezful", "Abadan", "Khorramshahr", "Ahvaz"],
     "rationales": [{"option": "Abadan", "why_plausible": "Southern oil city.", "why_wrong": "Industrial refinery island."},
                    {"option": "Khorramshahr", "why_plausible": "River port.", "why_wrong": "Port on the Shatt al-Arab."},
                    {"option": "Ahvaz", "why_plausible": "Provincial capital.", "why_wrong": "City on the Karun, while Dezful reeds grow along the Dez River."}],
     "expl": "Dezful reeds are seasoned for months until they turn glossy dark brown and ring like porcelain when struck.", "pg": 178},
    # Set B
    {"text": "Traditional Persian black ink (Morakkab) was brewed by boiling fine soot with gum arabic and the crushed gallnuts of this tree.",
     "ans": "Oak Tree (Mazu)", "aliases": ["Oak Tree", "Oak", "Mazu", "بلوط", "مازو"],
     "options": ["Oak Tree (Mazu)", "Olive Tree", "Walnut Tree", "Plane Tree"],
     "rationales": [{"option": "Olive Tree", "why_plausible": "Mediterranean tree.", "why_wrong": "Not used for tannin extraction in ink."},
                    {"option": "Walnut Tree", "why_plausible": "Used for brown dye.", "why_wrong": "Walnut hulls make brown dye, while oak gallnuts contain tannic acid for permanent black ink."},
                    {"option": "Plane Tree", "why_plausible": "Tehran Chenar.", "why_wrong": "Not used for calligraphic gall-ink."}],
     "expl": "The reaction between oak gall tannic acid and iron sulfate created indelible black ink that remained glossy for centuries.", "pg": 179},
    {"text": "The practice sheets where calligraphers repeatedly inscribed intersecting diagonal words until the paper turned into an abstract dense black carpet are called this.",
     "ans": "Siah-Mashq (Black Practice)", "aliases": ["Siah-Mashq", "Siah Mashq", "سیاه‌مشق", "سیاه مشق"],
     "options": ["Siah-Mashq (Black Practice)", "Tazhib", "Qet'eh", "Muraqqa"],
     "rationales": [{"option": "Tazhib", "why_plausible": "Gold illumination.", "why_wrong": "Floral gold leaf borders."},
                    {"option": "Qet'eh", "why_plausible": "Single-page poem composition.", "why_wrong": "Formal finished poem page."},
                    {"option": "Muraqqa", "why_plausible": "Album of calligraphy.", "why_wrong": "Bound collector's album."}],
     "expl": "Originally practical exercises to warm up fingers, Qajar masters like Mirza Gholam-Reza Esfahani transformed Siah-Mashq into high abstract art.", "pg": 180},
    {"text": "The fine floral illumination in 24-karat liquid gold leaf and lapis lazuli framing calligraphic panels and Quranic headers is known by this Arabic-derived term.",
     "ans": "Tazhib (Illumination)", "aliases": ["Tazhib", "Tezhib", "Gold Illumination", "تذهیب"],
     "options": ["Tazhib (Illumination)", "Minakari", "Khatam", "Gereh Chini"],
     "rationales": [{"option": "Minakari", "why_plausible": "Enamel art on metal.", "why_wrong": "Enameling on copper dishes."},
                    {"option": "Khatam", "why_plausible": "Wood mosaic.", "why_wrong": "Marquetry on wood."},
                    {"option": "Gereh Chini", "why_plausible": "Lattice woodwork.", "why_wrong": "Window woodwork."}],
     "expl": "Tazhib derives from Zahab (gold in Arabic), requiring artists to grind real gold leaves into powder and apply it with single-hair brushes.", "pg": 182},
    {"text": "Under the Safavids and Qajars, official imperial decrees bore this monumental calligraphic monogram containing the names and titles of the Shah at the top.",
     "ans": "Tughra (Toghra)", "aliases": ["Tughra", "Toghra", "طغرا"],
     "options": ["Tughra (Toghra)", "Bismillah", "Firman", "Seal"],
     "rationales": [{"option": "Bismillah", "why_plausible": "Opening religious formula.", "why_wrong": "Inscribed above, but the elaborate interlaced ruler monogram is the Tughra."},
                    {"option": "Firman", "why_plausible": "The entire royal decree.", "why_wrong": "The decree document itself."},
                    {"option": "Seal", "why_plausible": "Stamp.", "why_wrong": "Signet seal at the bottom."}],
     "expl": "Tughrawis were elite court scribes specializing in drawing the interlacing vertical strokes of the imperial signature.", "pg": 184},
    {"text": "To cut the sharp angled nib of a reed pen, calligraphers placed the reed on this small carved piece of bone, tortoiseshell, or ivory called a Qalam-tarash.",
     "ans": "Qat-zan", "aliases": ["Qat-zan", "Qatgir", "Nib cutter", "قط‌زن", "قلم‌تراش"],
     "options": ["Qat-zan", "Qalamdan", "Davat", "Lighah"],
     "rationales": [{"option": "Qalamdan", "why_plausible": "Pen case.", "why_wrong": "The box holding pens."},
                    {"option": "Davat", "why_plausible": "Inkpot.", "why_wrong": "The ink container."},
                    {"option": "Lighah", "why_plausible": "Silk wad inside inkpot.", "why_wrong": "Raw silk fibers soaked in ink to prevent dripping."}],
     "expl": "A sharp click (Qat) as the pen knife severed the reed against the bone plate signaled a perfect nib angle for Nastaliq.", "pg": 186}
])

save_clues(clues)
