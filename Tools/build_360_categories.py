#!/usr/bin/env python3
"""
Master Categories Catalog: 360 Categories with Witty Puns in both English and Farsi.
- 150 Single Jeopardy Categories
- 135 Double Jeopardy Categories
- 75 Final Jeopardy Categories
"""
import json

# 150 Single Categories
SINGLE_CATEGORIES = [
    # Existing 50 Single Categories (with perfected witty Persian puns)
    {"en": "WE DON'T COTTON TO CONCESSIONS", "fa": "حراج قرن قاجار", "period": "Qajar", "theme": "Diplomatic"},
    {"en": "A MASH-RUTEH MADE IN HEAVEN", "fa": "مشروطه به شرط چاقو", "period": "Constitutional Revolution", "theme": "Political"},
    {"en": "OIL, OBVIOUSLY", "fa": "نفت، معلومه دیگه!", "period": "Pahlavi", "theme": "Economic"},
    {"en": "LIGHTS ON LALEZAR", "fa": "لاله‌زار؛ برادوی طهران", "period": "Qajar & Pahlavi", "theme": "Arts & Cinema"},
    {"en": "A ROLLS-ROYCE FOR REZA", "fa": "رولزرویس و پیکان سواری", "period": "Pahlavi", "theme": "Infrastructure"},
    {"en": "ABAPLAN GONE WRONG", "fa": "نقشه بر آب در آبادان", "period": "Pahlavi", "theme": "Oil & Crisis"},
    {"en": "ALL ABOARD THE VERESK EXPRESS", "fa": "ورسک و سوت قطار پیروزی", "period": "Pahlavi", "theme": "Infrastructure"},
    {"en": "AVICENNA & THE BRAINIACS", "fa": "بوعلی‌بازی و نبوغ ایرانی", "period": "Medieval Islamic", "theme": "Sciences"},
    {"en": "BAZAAR-O WORLD", "fa": "حجره‌های معترض", "period": "Qajar", "theme": "Economic & Social"},
    {"en": "CALLIGRAPHY & INKWELLS", "fa": "خط خوش و دوات پردردسر", "period": "Islamic Eras", "theme": "Arts"},
    {"en": "CARPET DIEM", "fa": "دم را با دارِ قالی غنیمت شمر", "period": "Safavid to Modern", "theme": "Traditional Crafts"},
    {"en": "COWS, CHERRIES & CELLULOID", "fa": "از گاو تا طعم گیلاس", "period": "Modern Iran", "theme": "Cinema"},
    {"en": "DAMAVAND-ING RESPECT", "fa": "دیو سپید پای در بند", "period": "All Eras", "theme": "Geography"},
    {"en": "DAR AL-FUN-UN & GAMES", "fa": "دارالفنون و بازی‌های روزگار", "period": "Qajar", "theme": "Education"},
    {"en": "DEAR DIARY: THE SHAH SPEAKS", "fa": "علم غیب ندارد!", "period": "Pahlavi", "theme": "Court Life"},
    {"en": "DIRECTED BY KIAROSTAMI & CO.", "fa": "کلوزآپِ سینمای ایران", "period": "Post-1960s", "theme": "Cinema"},
    {"en": "FERDOWSI'S RHYME TIME", "fa": "سی سال رنج در شاهنامه", "period": "Medieval Islamic", "theme": "Literature"},
    {"en": "FROM VILLAGE TO VALIASR", "fa": "از طهران تا ولیعصر", "period": "Qajar & Pahlavi", "theme": "Urban History"},
    {"en": "GULF OF PERSIA, NOT DISCORD", "fa": "خلیج همیشه فارس", "period": "All Eras", "theme": "Maritime & Ports"},
    {"en": "HAFIZ THE BEATLES OF SHIRAZ", "fa": "شاخه نبات در فال حافظ", "period": "Medieval Islamic", "theme": "Poetry"},
    {"en": "HORSING AROUND IN NISA", "fa": "اسب‌های نیسا و کمانداران پارتی", "period": "Parthian Empire", "theme": "Antiquity"},
    {"en": "ISFAHAN-TASTIC SAFFAVIDS", "fa": "اصفهان و یک‌چهارمِ دیگرِ جهان", "period": "Safavid Empire", "theme": "Architecture & Power"},
    {"en": "IT'S NIMA OR NEVER", "fa": "ری‌را و شب‌های نیما", "period": "20th Century", "theme": "Modern Poetry"},
    {"en": "JUST FOR THE DASTGAH OF IT", "fa": "دستگاهِ کوک، آوازِ ناکوک", "period": "All Eras", "theme": "Classical Music"},
    {"en": "KHORASAN-WICH", "fa": "زعفران و فیروزه خراسان", "period": "All Eras", "theme": "Regional Culture"},
    {"en": "KINGS OF THE MEDES & BOUNDS", "fa": "پادشاهان ماد در هگمتانه", "period": "Median Empire", "theme": "Ancient History"},
    {"en": "LADIES OF THE CONSTITUTION", "fa": "زنان پیشگام مشروطه", "period": "Constitutional Revolution", "theme": "Women's History"},
    {"en": "LUT'S GET PHYSICAL", "fa": "داغ‌ترین نقطه در کویر لوت", "period": "All Eras", "theme": "Deserts & Geography"},
    {"en": "MULLA SADRA'S SOUL FOOD", "fa": "حکمت روی حرارت ملایم", "period": "Safavid Empire", "theme": "Philosophy"},
    {"en": "NADER SHAH'S SWORDPLAY", "fa": "شمشیر تیز نادر در دهلی", "period": "Afsharid Empire", "theme": "Conquests"},
    {"en": "NOT IN MY BACK-YAZD", "fa": "بادگیرهای بی‌باد یزد", "period": "All Eras", "theme": "Desert Architecture"},
    {"en": "ONCE UPON A JAMALZADEH", "fa": "یکی بود، یکی جمال‌زاده بود", "period": "20th Century", "theme": "Modern Prose"},
    {"en": "PARTY LIKE IT'S 539 BC", "fa": "مهمانی ۲۵۰۰ سال قبل", "period": "Pahlavi & Antiquity", "theme": "Imperial Celebrations"},
    {"en": "PERSIAN FLIGHTS OF FANCY", "fa": "هما و بال‌های سیمرغ", "period": "Pahlavi & Modern", "theme": "Aviation"},
    {"en": "POETS IN EXILE", "fa": "شعر در غربت", "period": "Contemporary", "theme": "Diaspora Literature"},
    {"en": "QOM WHAT MAY", "fa": "قم؛ هر چه باداباد", "period": "Safavid to Modern", "theme": "Shrines & Pilgrimage"},
    {"en": "ROSTAM'S SEVEN HABITS", "fa": "هفت‌خوان و یک رستم", "period": "Mythic & Epic", "theme": "Shahnameh"},
    {"en": "RUMI WITH A VIEW", "fa": "شمس و مولانا در پرواز", "period": "Medieval", "theme": "Sufism"},
    {"en": "SATTAR WARS: TABRIZ STRIKES BACK", "fa": "جنگ ستار: تبریز وارد می‌شود", "period": "Constitutional Revolution", "theme": "Resistance"},
    {"en": "SEALED WITH A DISS", "fa": "نامه‌های تند و مهرهای درباری", "period": "Qajar", "theme": "Royal Decrees"},
    {"en": "SHAH-PING FOR ANTIQUES", "fa": "عتیقه‌خران در بازار تهران", "period": "Qajar & Pahlavi", "theme": "Jewels & Relics"},
    {"en": "SMOKE 'EM IF YOU'VE GOT 'EM", "fa": "دود از قلیان شاه درآمد", "period": "Qajar", "theme": "Tobacco Protest"},
    {"en": "STARS OVER MARAGHEH", "fa": "ستاره‌بازی در مراغه", "period": "Ilkhanid & Timurid", "theme": "Astronomy & Renaissance"},
    {"en": "TAHDIG YOUR OWN GRAVE", "fa": "ته‌دیگِ تهِ خط", "period": "All Eras", "theme": "Cuisine"},
    {"en": "TAKING A PARTHIAN SHOT", "fa": "تیر خلاص پارتی", "period": "Parthian Empire", "theme": "Military Tactics"},
    {"en": "TALES FROM THE CASPIAN SHORE", "fa": "ماهی خاویار و چای لاهیجان", "period": "All Eras", "theme": "Northern Provinces"},
    {"en": "THE 300 & THEN SOME", "fa": "۳۰۰ و خرده‌ای", "period": "Achaemenid Empire", "theme": "Ancient Warfare"},
    {"en": "THE BREAD & BUTTER OF POLITICS", "fa": "بلوا بر سر نان جو", "period": "Qajar to WWII", "theme": "Urban Riots"},
    {"en": "THE BRIDGE OF VICTORY ROAD", "fa": "پل پیروزی یا پل هوایی؟", "period": "WWII", "theme": "Allied Occupation"},
    {"en": "WE'VE GOT ELAM-ENTARY EVIDENCE", "fa": "زیگورات چغازنبیل و رازهای ایلام", "period": "Elamite Empire", "theme": "Archaeology"}
]

print(f"Loaded {len(SINGLE_CATEGORIES)} base Single categories.")
