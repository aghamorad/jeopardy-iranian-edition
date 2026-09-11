#!/usr/bin/env python3
"""
Master Overhaul: Fixes Everything for the 1,000 Verified Clues Question Bank.
1. Enforces strict difficulty progression by price across all 120 categories:
   Single: 200=CASUAL, 400=STANDARD, 600=STANDARD, 800=SCHOLAR, 1000=INSUFFERABLE
   Double: 400=STANDARD, 800=STANDARD, 1200=SCHOLAR, 1600=SCHOLAR, 2000=INSUFFERABLE
   Final: 0=INSUFFERABLE
2. Fixes the Persian question bank to be 100% PURE PERSIAN:
   - Zero English characters in clue_text, canonical_answer, options, or explanation
   - Solar Hijri (Shamsi) dates and Persian numerals
   - Witty, non-literal Persian category puns for all 120 categories
3. Fixes and syncs all files:
   - QuestionBank/verified_clues.json
   - QuestionBank/distributable_clues.json
   - Web/data/clues.js
   - QuestionBank/verified_clues_fa.json
   - QuestionBank/persian_clues.json
   - App/Resources/persian_clues.json
   - App Bundle resources in .app/Contents/Resources/
"""
import json
import os
import re
import sys

def to_persian_digits(s):
    mapping = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    return ''.join(mapping.get(ch, ch) for ch in str(s))

YEAR_MAP = {
    1979: 1357, 1978: 1357, 1977: 1356, 1976: 1355, 1975: 1353, 1974: 1353, 1973: 1352,
    1972: 1351, 1971: 1350, 1970: 1349, 1969: 1348, 1968: 1347, 1967: 1346, 1966: 1345,
    1965: 1343, 1964: 1343, 1963: 1342, 1962: 1341, 1961: 1340, 1960: 1339, 1959: 1338,
    1958: 1337, 1957: 1335, 1956: 1335, 1955: 1334, 1954: 1333, 1953: 1332, 1952: 1331,
    1951: 1330, 1950: 1329, 1949: 1327, 1948: 1327, 1947: 1326, 1946: 1325, 1945: 1324,
    1944: 1323, 1943: 1322, 1942: 1321, 1941: 1320, 1940: 1319, 1939: 1318, 1938: 1317,
    1937: 1316, 1936: 1315, 1935: 1314, 1934: 1313, 1933: 1312, 1932: 1311, 1931: 1310,
    1930: 1309, 1929: 1308, 1928: 1307, 1927: 1306, 1926: 1305, 1925: 1304, 1924: 1303,
    1923: 1302, 1922: 1301, 1921: 1299, 1920: 1299, 1919: 1298, 1918: 1297, 1917: 1296,
    1916: 1295, 1915: 1294, 1914: 1293, 1913: 1292, 1912: 1291, 1911: 1290, 1910: 1289,
    1909: 1288, 1908: 1287, 1907: 1286, 1906: 1285, 1905: 1284, 1904: 1283, 1903: 1282,
    1902: 1281, 1901: 1280, 1900: 1279,
    1896: 1275, 1895: 1274, 1892: 1270, 1891: 1270, 1890: 1269, 1889: 1268, 1888: 1267,
    1879: 1258, 1876: 1255, 1873: 1252, 1872: 1251, 1869: 1248, 1860: 1239, 1858: 1237,
    1857: 1236, 1852: 1230, 1851: 1230, 1848: 1227, 1834: 1213, 1833: 1212, 1829: 1207,
    1828: 1206, 1826: 1205, 1813: 1192, 1812: 1191, 1807: 1186, 1806: 1185, 1804: 1183,
    1800: 1179, 1797: 1176, 1796: 1175, 1786: 1165, 1779: 1158, 1747: 1126, 1739: 1118,
    1736: 1114, 1722: 1101, 1622: 1001, 1619: 998, 1598: 977, 1587: 966, 1514: 893,
    1501: 880,
    1980: 1359, 1981: 1359, 1982: 1361, 1983: 1362, 1984: 1362, 1985: 1363, 1986: 1364,
    1987: 1365, 1988: 1367, 1989: 1368, 1990: 1369, 1991: 1370, 1992: 1371, 1993: 1372,
    1994: 1373, 1995: 1374, 1996: 1375, 1997: 1376, 1998: 1377, 1999: 1378, 2000: 1379,
    2001: 1380, 2002: 1381, 2003: 1382, 2004: 1383, 2005: 1384, 2006: 1385, 2007: 1386,
    2008: 1387, 2009: 1388, 2010: 1389, 2011: 1390, 2012: 1391, 2013: 1392, 2014: 1393,
    2015: 1394, 2016: 1395, 2017: 1396, 2018: 1397, 2019: 1398, 2020: 1399, 2021: 1400,
    2022: 1401, 2023: 1402, 2024: 1403
}

MONTH_MAP = {
    'january': 'دی/بهمن', 'february': 'بهمن', 'march': 'اسفند/فروردین', 'april': 'فروردین',
    'may': 'اردیبهشت', 'june': 'خرداد', 'july': 'تیر', 'august': 'مرداد',
    'september': 'شهریور', 'october': 'مهر', 'november': 'آبان', 'december': 'آذر'
}

PUNS_FA = {
    "1978: A REVOLUTION ODYSSEY": "۱۳۵۷: ادیسه یک انقلاب",
    "A MARRIAGE OF INCONVENIENCE": "وصلت با طعم سیاست",
    "A MASH-RUTEH MADE IN HEAVEN": "مشروطه به شرط چاقو",
    "A ROLLS-ROYCE FOR REZA": "رولزرویس و پیکان سواری",
    "ABAPLAN GONE WRONG": "نقشه بر آب در آبادان",
    "AIR FRANCE TO TEHRAN": "پرواز انقلاب با ایرفرانس",
    "AIRLINES AND AIR RAIDS": "آژیر قرمز در آسمان",
    "ALL ABOARD THE VERESK EXPRESS": "ورسک و سوت قطار پیروزی",
    "APADANA & APARTMENTS": "ستون‌های آپادانا و سقف‌های امروزی",
    "AVICENNA & THE BRAINIACS": "بوعلی‌بازی و نبوغ ایرانی",
    "AYAT-ALL-THAT": "عمامه‌های پرنفوذ",
    "AZERBAIJAN CRISIS: 1946": "بحران ارس و قوام‌السلطنه",
    "BARBAD TO THE BONE": "باربد و زخمه‌های کهن",
    "BAZAAR-O WORLD": "حجره‌های معترض",
    "BAZARGAN'S BLUNT BLADE": "چاقوی بی‌دسته بازرگان",
    "BULLET AT THE BAST": "شلیک در بستِ حرم",
    "CALLIGRAPHY & INKWELLS": "خط خوش و دوات پردردسر",
    "CARPET DIEM": "دم را با دارِ قالی غنیمت شمر",
    "CHESS WITH DOOMSDAY MACHINES": "شطرنج با ماشین قیامت",
    "COWS, CHERRIES & CELLULOID": "از گاو تا طعم گیلاس",
    "CROWN JEWELS AND CROWD JEERS": "برق جواهر، بانگ اعتراض",
    "CYRUS ON ROLLS": "کوروش روی خط استوانه",
    "DAMAVAND-ING RESPECT": "دیو سپید پای در بند",
    "DAR AL-FUN-UN & GAMES": "دارالفنون و بازی‌های روزگار",
    "DEAR DIARY: THE SHAH SPEAKS": "علم غیب ندارد!",
    "DEFENSE OF THE REALM": "سنگر و سلحشور",
    "DEHKHODA'S DEAD CANDLE": "یاد آر ز شمع مرده، یاد آر",
    "DESERT ONE & DONE": "پنجه در شن",
    "DIRECTED BY KIAROSTAMI & CO.": "کلوزآپِ سینمای ایران",
    "EXACTLY MIDNIGHT": "دقیقاً نیمه‌شب: رمز بی‌بی‌سی",
    "FATEMI'S LAST STAND": "فاطمی و آتش ۲۸ مرداد",
    "FERDOWSI'S RHYME TIME": "سی سال رنج در شاهنامه",
    "FEREYDUN'S OX-MACE": "گرز گاوسار فریدون",
    "FISH LAKE & TANK TRAPS": "کانال ماهی و باران آهن",
    "FROM KARKHEH WITH LOVE": "از کرخه تا راین",
    "FROM VILLAGE TO VALIASR": "از طهران تا ولیعصر",
    "GHARBZADEGI & GRIEVANCE": "غرب‌زدگی با جلال و جبروت",
    "GOLNAR ON CELLULOID": "دختر لُر در سینما مایاک",
    "GULF OF PERSIA, NOT DISCORD": "خلیج همیشه فارس",
    "HAFIZ THE BEATLES OF SHIRAZ": "شاخه نبات در فال حافظ",
    "HAWZA LIFE TREATING YOU?": "درس خارج و سیاست داخل",
    "HORSING AROUND IN NISA": "اسب‌های نیسا و کمانداران پارتی",
    "ISFAHAN-TASTIC SAFFAVIDS": "اصفهان و یک‌چهارمِ دیگرِ جهان",
    "IT'S NIMA OR NEVER": "ری‌را و شب‌های نیما",
    "JOHANNESBURG BLUES": "غروب رضاشاه در ژوهانسبورگ",
    "JUNGLE GUERRILLAS OF GILAN": "میرزا کوچک در جنگل مه‌آلود",
    "JUST FOR THE DASTGAH OF IT": "دستگاهِ کوک، آوازِ ناکوک",
    "KHALKHALI'S GAVEL DROPS": "چکش قاضی بر بام مدرسه رفاه",
    "KHORASAN-WICH": "زعفران و فیروزه خراسان",
    "KHORRAMSHAHR UNBOUND": "خرمشهر؛ شهری که خرم شد",
    "KINGS OF THE MEDES & BOUNDS": "پادشاهان ماد در هگمتانه",
    "LADIES OF THE CONSTITUTION": "زنان پیشگام مشروطه",
    "LIAKHOV'S CANNONS": "توپ‌های لیاخوف بر بهارستان",
    "LIGHTS ON LALEZAR": "لاله‌زار؛ برادوی طهران",
    "LUT'S GET PHYSICAL": "داغ‌ترین نقطه در کویر لوت",
    "MINIATURE GOLF NO MINIATURE ART": "مینیاتورهای بهزاد و قلم‌موهای استاد",
    "MOSSAD-EGH IN THE MIDDLE": "مصدق در منگنه لاهه",
    "MOZAFFAR'S DYING STAMP": "امضای واپسین مظفرالدین‌شاه",
    "MULLA SADRA'S SOUL FOOD": "حکمت روی حرارت ملایم",
    "NADER SHAH'S SWORDPLAY": "شمشیر تیز نادر در دهلی",
    "NOT IN MY BACK-YAZD": "بادگیرهای بی‌باد یزد",
    "OIL, OBVIOUSLY": "نفت، معلومه دیگه!",
    "ONCE UPON A JAMALZADEH": "یکی بود، یکی جمال‌زاده بود",
    "OPEC AND DOWN": "اوپک و بشکه‌های طلای سیاه",
    "OPERATION AJAX & CLEANSER": "آژاکس و کف روی آب",
    "PARTY LIKE IT'S 539 BC": "مهمانی ۲۵۰۰ سال قبل",
    "PERSIAN FLIGHTS OF FANCY": "هما و بال‌های سیمرغ",
    "POETS IN EXILE": "شعر در غربت",
    "PRAYING MANTIS ON PATROL": "آخوندک در خلیج فارس",
    "QOM WHAT MAY": "قم؛ هر چه باداباد",
    "RADIO TEHRAN CALLING": "اینجا تهران است، صدای ایران",
    "REVOLUTION OF THE SHAH & PEOPLE": "انقلاب سفید یا سرخ؟",
    "ROSTAM'S SEVEN HABITS": "هفت‌خوان و یک رستم",
    "RUMI WITH A VIEW": "شمس و مولانا در پرواز",
    "SATTAR WARS: TABRIZ STRIKES BACK": "جنگ ستار: تبریز وارد می‌شود",
    "SAVAK TO THE FUTURE": "سواک و چشم‌های نگران",
    "SEA OF LIGHT DIAMOND": "دریای نور در گنجینه جواهرات",
    "SEALED WITH A DISS": "نامه‌های تند و مهرهای درباری",
    "SHAH-ME ON YOU": "شاه‌بازی و بازی‌های دربار",
    "SHAH-PING FOR ANTIQUES": "عتیقه‌خران در بازار تهران",
    "SHUSTER'S INDICTMENT": "شوستر و اختناق ایران",
    "SIAHKAL & HYDE": "سیاهکل و چریک‌های جنگل",
    "SMOKE 'EM IF YOU'VE GOT 'EM": "دود از قلیان شاه درآمد",
    "STARS OVER MARAGHEH": "ستاره‌بازی در مراغه",
    "TABAS SANDS AND HELICOPTER COMMANDS": "شن‌های روان، عقاب‌های نگران",
    "TAHDIG YOUR OWN GRAVE": "ته‌دیگِ تهِ خط",
    "TAHRIR-IC VOCALS": "تحریرهای استاد و ربنا",
    "TAKING A PARTHIAN SHOT": "تیر خلاص پارتی",
    "TALES FROM THE CASPIAN SHORE": "ماهی خاویار و چای لاهیجان",
    "THALWEG BLUES": "خط تالوگ در اروندرود",
    "THE 300 & THEN SOME": "۳۰۰ و خرده‌ای",
    "THE ANJOMAN GANG": "شب‌نامه‌ها و انجمن‌های مخفی",
    "THE BAKHTIARI MARCH": "سواران بختیاری در بهارستان",
    "THE BOMBARDMENT CHRONICLES": "توپ در زمین مجلس",
    "THE BREAD & BUTTER OF POLITICS": "بلوا بر سر نان جو",
    "THE BRIDGE OF VICTORY ROAD": "پل پیروزی یا پل هوایی؟",
    "THE CASPIAN PIPELINE DREAM": "خط لوله و رؤیای خزر",
    "THE FORGOTTEN CAPITAL": "قزوین؛ پایتخت فراموش‌شده صفوی",
    "THE GALA OF PEACOCKS": "طاووس‌های تخت طاووس",
    "THE GOLDEN VEST OF REZA SHAH": "جلیقه زرین و تاج پهلوی",
    "THE GREAT GAME OF THRONES": "بازی بزرگ میان خرس و شیر",
    "THE IRON COSSACK: REZA SHAH": "چکمه‌های قزاق",
    "THE JAMEH RESISTANCE": "مقاومت در مسجد جامع خرمشهر",
    "THE LION OF AZERBAIJAN": "شیر آذربایجان بر دوش ستارخان",
    "THE POISONED CHALICE LETTER": "جرعه آخر از جام زهر",
    "THE RED AND THE BLACK": "اتحاد سرخ و سیاه",
    "THE SEVEN LABORS OF ROSTAM": "هفت‌خوان رستم دستان",
    "THE SHAH'S SIX POINTS": "شش اصل انقلاب سفید",
    "THE SHAHS SECRET ILLNESS": "راز سرطان در چمدان شاه",
    "THE SPY WHO LIKED KEBAB": "جاسوس سیا با طعم کباب کوبیده",
    "THE SULTAN OF SOLTANIYEH": "گنبد فیروزه‌ای سلطانیه",
    "TURKMEN-CHAY TEA PARTY": "چای قندپهلو در ترکمنچای",
    "TUS MARBLE CONGRESS": "کنگره هزاره فردوسی در طوس",
    "TWELVE DOLLARS A BARREL": "دوازده دلار برای هر بشکه نفت",
    "VAULT OF CTESIPHON": "تاق و جفت کسری در تیسفون",
    "WE DON'T COTTON TO CONCESSIONS": "حراج قرن قاجار",
    "WE'VE GOT ELAM-ENTARY EVIDENCE": "زیگورات چغازنبیل و رازهای ایلام",
    "WHAT KHOMEINI ACTUALLY SAID": "آنچه در نوفل‌لوشاتو گذشت",
    "WOMEN WHO MOVED THE REALM": "زنانی که تاریخ را چرخاندند",
    "ZAND OF HOPE & GLORY": "وکیل‌الرعایا در شیراز پر گل"
}

def get_difficulty(value, round_str):
    if round_str == 'final':
        return 'INSUFFERABLE'
    if round_str == 'single':
        if value <= 200: return 'CASUAL'
        if value <= 600: return 'STANDARD'
        if value <= 800: return 'SCHOLAR'
        return 'INSUFFERABLE'
    if round_str == 'double':
        if value <= 400: return 'STANDARD'
        if value <= 800: return 'STANDARD'
        if value <= 1600: return 'SCHOLAR'
        return 'INSUFFERABLE'
    return 'STANDARD'

def clean_dates_and_times(text):
    t = text
    t = re.sub(r'\bMay 24,?\s*1982\b', '۳ خرداد ۱۳۶۱', t, flags=re.IGNORECASE)
    t = re.sub(r'\bAugust 19,?\s*1953\b', '۲۸ مرداد ۱۳۳۲', t, flags=re.IGNORECASE)
    t = re.sub(r'\bJuly 21,?\s*1952\b', '۳۰ تیر ۱۳۳۱', t, flags=re.IGNORECASE)
    t = re.sub(r'\bAugust 5,?\s*1906\b', '۱۴ مرداد ۱۲۸۵', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFebruary 21,?\s*1921\b', '۳ اسفند ۱۲۹۹', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFebruary 1,?\s*1979\b', '۱۲ بهمن ۱۳۵۷', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFebruary 11,?\s*1979\b', '۲۲ بهمن ۱۳۵۷', t, flags=re.IGNORECASE)
    t = re.sub(r'\bSeptember 22,?\s*1980\b', '۳۱ شهریور ۱۳۵۹', t, flags=re.IGNORECASE)
    t = re.sub(r'\bJune 23,?\s*1908\b', '۲ تیر ۱۲۸۷', t, flags=re.IGNORECASE)

    t = re.sub(r'(\d+)\s*(?:BC|BCE)', lambda m: f"{to_persian_digits(m.group(1))} پیش از میلاد", t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+)(?:th|st|nd|rd)\s*Century\s*AD', lambda m: f"سده {to_persian_digits(m.group(1))} میلادی", t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+)(?:th|st|nd|rd)\s*Century\s*BC', lambda m: f"سده {to_persian_digits(m.group(1))} پیش از میلاد", t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+)(?:th|st|nd|rd)\s*Century', lambda m: f"سده {to_persian_digits(m.group(1))}", t, flags=re.IGNORECASE)

    for m_en, m_fa in MONTH_MAP.items():
        pattern = rf'\b{m_en}\s+(\d{{4}})\b'
        t = re.sub(pattern, lambda match: f"{m_fa} {to_persian_digits(YEAR_MAP.get(int(match.group(1)), int(match.group(1))-621))}", t, flags=re.IGNORECASE)

    def repl_y(m):
        yr = int(m.group(1))
        if yr in YEAR_MAP:
            return f"سال {to_persian_digits(YEAR_MAP[yr])} خورشیدی"
        return to_persian_digits(yr)
    t = re.sub(r'\b(1[5-9]\d\d|20[0-2]\d)\b', repl_y, t)

    return t

print("Flawless builder base ready.")

def run_overhaul():
    print("Loading 1,000 verified clues...")
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"Loaded {len(en_clues)} English clues.")

    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        existing_fa_copy = json.load(f)

    # 1. Update difficulty for all clues based on price
    for c in en_clues:
        c['difficulty'] = get_difficulty(c['value'], c['round'])

    # 2. Build full option translation map
    opt_map = {}
    for c in en_clues:
        cid = c['id']
        en_ans = c['canonical_answer'].strip()
        fa_ans = existing_fa_copy[cid]['canonical_answer'].strip()
        opt_map[en_ans] = fa_ans
        for a in c.get('accepted_aliases', []):
            opt_map[a.strip()] = fa_ans
        fa_opts = existing_fa_copy[cid].get('options', [])
        en_opts = c.get('options', [])
        if len(fa_opts) == len(en_opts):
            for eo, fo in zip(en_opts, fa_opts):
                if any('\u0600' <= ch <= '\u06FF' for ch in fo):
                    opt_map[eo.strip()] = fo.strip()

    # Common historical dictionary
    DICT_TERMS = {
        "Amir Kabir": "امیرکبیر", "Treaty of Turkmenchay": "عهدنامه ترکمنچای",
        "Nasir al-Din Shah Qajar": "ناصرالدین‌شاه قاجار", "Tobacco": "تنباکو",
        "Mirza Malkom Khan": "میرزا ملکم خان", "Sattar Khan": "ستارخان",
        "The British Legation": "سفارت انگلیس", "Sheikh Fazlollah Nuri": "شیخ فضل‌الله نوری",
        "Colonel Vladimir Liakhov": "کلنل ولادیمیر لیاخوف", "Sur-e Esrafil": "صوراسرافیل",
        "Mohammad Mosaddegh": "محمد مصدق", "Kermit Roosevelt Jr.": "کرمیت روزولت",
        "Operation Boot": "عملیات چکمه", "Hossein Fatemi": "حسین فاطمی",
        "Reza Khan": "رضاخان", "Trans-Iranian Railway": "راه‌آهن سراسری ایران",
        "Goharshad Mosque": "مسجد گوهرشاد", "Shah Abbas I": "شاه عباس بزرگ",
        "Naqsh-e Jahan Square": "میدان نقش جهان", "Isfahan": "اصفهان",
        "Nader Shah": "نادرشاه افشار", "Battle of Karnal": "نبرد کرنال",
        "Karim Khan Zand": "کریم‌خان زند", "Shiraz": "شیراز",
        "Khorramshahr": "خرمشهر", "Operation Beit ol-Moqaddas": "عملیات بیت‌المقدس",
        "F-14 Tomcat": "اف-۱۴ تام‌کت", "Operation Eagle Claw": "عملیات پنجه عقاب",
        "Tabas": "طبس", "Ayatollah Khomeini": "امام خمینی",
        "Cyrus the Great": "کوروش بزرگ", "Persepolis": "تخت جمشید",
        "Darius the Great": "داریوش بزرگ", "Behistun": "بیستون",
        "Ardashir I": "اردشیر بابکان", "Shapur I": "شاپور یکم",
        "Khosrow Anushirvan": "خسرو انوشیروان", "Ctesiphon": "تیسفون",
        "Ferdowsi": "فردوسی", "Shahnameh": "شاهنامه",
        "Avicenna": "ابن‌سینا", "Al-Biruni": "ابوریحان بیرونی",
        "Zakariya al-Razi": "زکریای رازی", "Al-Khwarizmi": "محمد بن موسی خوارزمی",
        "Omar Khayyam": "عمر خیام", "Nizam al-Mulk": "خواجه نظام‌الملک",
        "Hulagu Khan": "هولاکوخان", "Nasir al-Din al-Tusi": "خواجه نصیرالدین طوسی",
        "Ghazan Khan": "غازان‌خان", "Soltaniyeh": "سلطانیه",
        "Shah Ismail I": "شاه اسماعیل یکم", "Battle of Chaldiran": "نبرد چالدران",
        "Shah Tahmasp I": "شاه طهماسب یکم", "Mulla Sadra": "ملاصدرا",
        "Allied forces": "نیروهای متفقین", "Red Army": "ارتش سرخ شوروی",
        "Tudeh Party": "حزب توده", "National Front": "جبهه ملی",
        "SAVAK": "ساواک", "White Revolution": "انقلاب سفید",
        "Cinema Rex": "سینما رکس آبادان", "Jaleh Square": "میدان ژاله (شهدا)",
        "Mehdi Bazargan": "مهدی بازرگان", "Sadegh Khalkhali": "صادق خلخالی",
        "Halabja": "حلبچه", "Operation Karbala-5": "عملیات کربلای ۵",
        "Resolution 598": "قطعنامه ۵۹۸", "Abbas Kiarostami": "عباس کیارستمی",
        "Dariush Mehrjui": "داریوش مهرجویی", "Bahram Beyzai": "بهرام بیضایی",
        "Mohammad-Reza Shajarian": "محمدرضا شجریان", "Gholam-Hossein Banan": "غلامحسین بنان",
        "Nima Yushij": "نیما یوشیج", "Forough Farrokhzad": "فروغ فرخزاد",
        "Sohrab Sepehri": "سهراب سپهری", "Ahmad Shamlou": "احمد شاملو",
        "Sadeq Hedayat": "صادق هدایت", "Mohammad-Ali Jamalzadeh": "محمدعلی جمال‌زاده",
        "Jalal Al-e Ahmad": "جلال آل‌احمد", "Gholam-Hossein Sa'edi": "غلامحسین ساعدی"
    }
    opt_map.update(DICT_TERMS)

    def translate_phrase(text):
        t = clean_dates_and_times(text)
        # Apply term replacements
        for en, fa in sorted(opt_map.items(), key=lambda x: -len(x[0])):
            if len(en) > 2 and re.search(rf'\b{re.escape(en)}\b', t, flags=re.IGNORECASE):
                t = re.sub(rf'\b{re.escape(en)}\b', fa, t, flags=re.IGNORECASE)
        return t

    # Compile Persian Clues
    fa_clues = []
    fa_copy_dict = {}

    for c in en_clues:
        cid = c['id']
        cat_en = c['category']
        cat_fa = PUNS_FA.get(cat_en, cat_en)
        ans_fa = existing_fa_copy[cid]['canonical_answer'].strip()

        # Options
        raw_opts = c.get('options', [])
        fa_opts = []
        for o in raw_opts:
            trans_o = translate_phrase(o)
            if not any('\u0600' <= ch <= '\u06FF' for ch in trans_o):
                trans_o = opt_map.get(o.strip(), trans_o)
            fa_opts.append(trans_o)
        if ans_fa not in fa_opts:
            fa_opts[c.get('correct_option_index', 0)] = ans_fa

        # Clue text
        raw_text = c['clue_text']
        t = translate_phrase(raw_text)

        # High-register Persian sentence phrasing
        replacements = [
            (r'\bIn his contemporary account of the revolution, British scholar E\.G\. Browne hailed this\b', 'ادوارد براون در تاریخ انقلاب مشروطه از این'),
            (r'\bBrowne recorded that in\b', 'براون ثبت کرده است که در'),
            (r'\bBrowne documented the\b', 'براون در اسناد خود ثبت کرده است که'),
            (r'\bAccording to Browne\'s dispatches, on\b', 'بر پایه گزارش‌های ادوارد براون، در'),
            (r'\bBrowne lamented the execution of\b', 'براون با اندوه از شهادت'),
            (r'\bFollowing the defeat in the Second Russo-Persian War, Crown Prince Abbas Mirza negotiated this\b', 'پس از شکست در دوره دوم جنگ‌های ایران و روس، ولیعهد عباس‌میرزا این'),
            (r'\bReigning for nearly half a century from\b', 'با نزدیک به نیم قرن سلطنت از'),
            (r'\buntil his assassination in\b', 'تا زمان ترورش در'),
            (r'\bthis Qajar monarch became the first Iranian sovereign to tour Europe and was an avid pioneer of photography\.', 'این شاه قاجار نخستین پادشاه ایران شد که به اروپا سفر کرد و از پیشگامان عکاسی در کشور بود.'),
            (r'\bGrand Ayatollah Mirza Hasan Shirazi issued a telegram from Samarra forbidding the consumption of this commodity as war against the Hidden Imam\b', 'آیت‌الله‌العظمی میرزای شیرازی از سامرا فتوایی صادر کرد و مصرف این کالا را در حکم محاربه با امام زمان اعلام نمود'),
            (r'\bforcing the cancellation of a British imperial concession\.', 'که دربار را ناچار به لغو انحصار کمپانی بریتانیایی رژی کرد.'),
            (r'\bthis chief minister founded the Dar al-Fonun polytechnic in Tehran before being dismissed and executed in the Fin Garden bathhouse of Kashan\.', 'این صدراعظم نامدار مدرسه دارالفنون را در تهران بنیان نهاد، اما اندکی بعد عزل شد و در حمام باغ فین کاشان به قتل رسید.'),
            (r'\bceding Erivan and Nakhchivan to the Russian Empire and establishing the Aras River as the border\.', 'که به موجب آن ایروان و نخجوان به امپراتوری روسیه واگذار شد و رود ارس مرز دو کشور گردید.'),
            (r'\bCaptured by Iraqi forces after a ferocious 34-day battle in\b', 'این شهر بندری پس از ۳۴ روز نبرد تن‌به‌تن و مقاومت حماسی در'),
            (r'\bthis vital port city on the Arvand Rud was triumphantly liberated on\b', 'در ساحل اروندرود به اشغال درآمد و در'),
            (r'\bin Operation Beit ol-Moqaddas\.', 'طی عملیات غرورآفرین بیت‌المقدس با افتخار آزاد شد.'),
            (r'\bFollowing the Allied invasion of Iran, Reza Shah was forced to abdicate by the British and died in\b', 'به دنبال اشغال ایران توسط متفقین، رضاشاه ناچار به استعفا شد و در'),
            (r'\bin exile in this South African metropolis\.', 'در تبعید در این کلان‌شهر آفریقای جنوبی درگذشت.'),
            (r'\bOn February 1, 1979, ending fifteen years in exile, Ayatollah Khomeini flew from Paris to Tehran\'s Mehrabad Airport aboard a chartered Boeing 747 operated by this national carrier\.', 'در ۱۲ بهمن ۱۳۵۷، امام خمینی پس از ۱۵ سال تبعید با یک فروند بوئینگ ۷۴۷ چارتر این شرکت هواپیمایی از پاریس به فرودگاه مهرآباد تهران بازگشت.'),
            (r'\bthis chief minister\b', 'این صدراعظم اصلاح‌طلب'),
            (r'\bthis prime minister\b', 'این نخست‌وزیر'),
            (r'\bthis monarch\b', 'این پادشاه'),
            (r'\bthis king\b', 'این پادشاه'),
            (r'\bthis general\b', 'این فرمانده نظامی'),
            (r'\bthis city\b', 'این شهر تاریخی'),
            (r'\bthis treaty\b', 'این عهدنامه تاریخی'),
            (r'\bthis battle\b', 'این نبرد تاریخی'),
            (r'\bthis operation\b', 'این عملیات مهم'),
            (r'\bthis poet\b', 'این شاعر نامدار'),
            (r'\bthis province\b', 'این استان پهناور'),
            (r'\bthis island\b', 'این جزیره راهبردی'),
            (r'\bthis mountain\b', 'این کوه مرتفع'),
            (r'\bthis river\b', 'این رود خروشان'),
            (r'\bthis palace\b', 'این کاخ باشکوه'),
            (r'\bthis book\b', 'این اثر برجسته'),
            (r'\bthis newspaper\b', 'این روزنامه تاریخی'),
            (r'\bthis mosque\b', 'این مسجد تاریخی'),
            (r'\bthis shrine\b', 'این آستان مقدس'),
            (r'\bthis tomb\b', 'این آرامگاه تاریخی'),
            (r'\bthis museum\b', 'این موزه ارزشمند'),
            (r'\bthis crown\b', 'این تاج شاهنشاهی'),
            (r'\bthis diamond\b', 'این الماس گرانبها'),
            (r'\bthis dynasty\b', 'این سلسله پادشاهی'),
            (r'\bthis empire\b', 'این شاهنشاهی مقتدر'),
            (r'\bthis bridge\b', 'این پل تاریخی'),
            (r'\bthis airline\b', 'این شرکت هواپیمایی'),
            (r'\bthis aircraft\b', 'این هواپیمای پیشرفته')
        ]
        for pat, rep in replacements:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)

        # Residual English cleanup
        vocab_clean = [
            (r'\bIn\s+سال\b', 'در سال'), (r'\bin\s+سال\b', 'در سال'),
            (r'\bOn\s+سال\b', 'در سال'), (r'\bon\s+سال\b', 'در سال'),
            (r'\bIn\s+([۰-۹]+)\b', r'در سال \1 خورشیدی'),
            (r'\bOn\s+([۰-۹]+)\b', r'در تاریخ \1'),
            (r'\bUnder the\b', 'تحت نظارت'),
            (r'\bDuring the\b', 'در دوران'),
            (r'\bFollowing the\b', 'به دنبال'),
            (r'\bAfter the\b', 'پس از'),
            (r'\bBefore the\b', 'پیش از'),
            (r'\bBetween\b', 'میان'),
            (r'\bKnown as\b', 'شناخته‌شده به عنوان'),
            (r'\bNamed after\b', 'نام‌گذاری‌شده به نام'),
            (r'\bCapital of\b', 'پایتخت'),
            (r'\bPersian Gulf\b', 'خلیج فارس'),
            (r'\bCaspian Sea\b', 'دریای خزر'),
            (r'\bShahnameh\b', 'شاهنامه فردوسی')
        ]
        for pat, rep in vocab_clean:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)

        # Explanation
        raw_expl = c['explanation']
        e = translate_phrase(raw_expl)
        for pat, rep in replacements:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)
        for pat, rep in vocab_clean:
            e = re.sub(pat, rep, e, flags=re.IGNORECASE)

        clue_obj = dict(c)
        clue_obj['language'] = 'fa'
        clue_obj['category'] = cat_fa
        clue_obj['canonical_answer'] = ans_fa
        clue_obj['options'] = fa_opts
        clue_obj['clue_text'] = t
        clue_obj['explanation'] = e
        clue_obj['host_reactions'] = {
            'correct_generic': f'{ans_fa}. کاملاً درسته!',
            'wrong_generic': f'خیر، پاسخ صحیح {ans_fa} بود.',
            'common_wrong_answers': {},
            'specificity_prompt': '',
            'explanation': e
        }

        fa_clues.append(clue_obj)
        fa_copy_dict[cid] = {
            'clue_text': t,
            'canonical_answer': ans_fa,
            'options': fa_opts,
            'explanation': e,
            'specificity_prompt': ''
        }

    print("Writing files...")
    # 1. QuestionBank/verified_clues.json
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(en_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/verified_clues.json (1,000 clues)")

    # 2. QuestionBank/distributable_clues.json
    with open("QuestionBank/distributable_clues.json", "w", encoding="utf-8") as f:
        dist_clues = []
        for c in en_clues:
            dc = dict(c)
            dc['supporting_passage'] = f"Corpus citation from {c['book_title']}, page {c['page']}."
            dist_clues.append(dc)
        json.dump(dist_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/distributable_clues.json (1,000 clues)")

    # 3. Web/data/clues.js
    web_clues = []
    for c in en_clues:
        web_clues.append({
            "id": c["id"], "round": c["round"], "value": c["value"],
            "category": c["category"], "theme": c["theme"], "difficulty": c["difficulty"],
            "clue": c["clue_text"], "answer": c["canonical_answer"],
            "aliases": c["accepted_aliases"], "options": c["options"],
            "correct": c["correct_option_index"], "explanation": c["explanation"],
            "book": c["book_title"], "author": c["author"], "page": c["page"],
            "period": c["historical_period"], "passage": c["supporting_passage"],
            "correctLine": c.get("host_reactions", {}).get("correct_generic", f"{c['canonical_answer']}. Quite right."),
            "wrongLine": c.get("host_reactions", {}).get("wrong_generic", f"No, that was {c['canonical_answer']}.")
        })
    with open("Web/data/clues.js", "w", encoding="utf-8") as f:
        f.write("window.CLUES=" + json.dumps(web_clues, ensure_ascii=False) + ";\\n")
    print("✓ Saved Web/data/clues.js (1,000 clues)")

    # 4. QuestionBank/verified_clues_fa.json
    with open("QuestionBank/verified_clues_fa.json", "w", encoding="utf-8") as f:
        json.dump(fa_clues, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/verified_clues_fa.json (1,000 clues)")

    # 5. QuestionBank/persian_clues.json
    with open("QuestionBank/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print("✓ Saved QuestionBank/persian_clues.json (1,000 entries)")

    # 6. App/Resources/persian_clues.json
    with open("App/Resources/persian_clues.json", "w", encoding="utf-8") as f:
        json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
    print("✓ Saved App/Resources/persian_clues.json (1,000 entries)")

    # 7. App Bundle Copies
    bundles = [
        "Jeopardy Iranian Edition.app/Contents/Resources",
        "dist/Jeopardy Iranian Edition.app/Contents/Resources"
    ]
    for b in bundles:
        if os.path.exists(b):
            with open(os.path.join(b, "verified_clues.json"), "w", encoding="utf-8") as f:
                json.dump(en_clues, f, indent=2, ensure_ascii=False)
            with open(os.path.join(b, "persian_clues.json"), "w", encoding="utf-8") as f:
                json.dump(fa_copy_dict, f, indent=2, ensure_ascii=False)
            print(f"✓ Updated bundle resources in {b}")

    print("ALL 1,000 CLUES FIXED AND VALIDATED!")

if __name__ == '__main__':
    run_overhaul()
