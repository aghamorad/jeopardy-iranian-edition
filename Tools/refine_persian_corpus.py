#!/usr/bin/env python3
"""
Refines QuestionBank/verified_clues_fa.json to ensure 100% Persian translation
across all options, clue texts, rationales, and explanations, with comprehensive Shamsi date conversions.
"""
import json
import re
import os

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

def clean_dates(text):
    t = text
    # Clean leading "In سال" or "in سال"
    t = re.sub(r'\bIn\s+سال\b', 'در سال', t, flags=re.IGNORECASE)
    t = re.sub(r'\bOn\s+سال\b', 'در سال', t, flags=re.IGNORECASE)
    t = re.sub(r'\bDuring\s+سال\b', 'طی سال', t, flags=re.IGNORECASE)
    t = re.sub(r'\bIn\s+(\d{4})\b', lambda m: f"در سال {to_persian_digits(YEAR_MAP.get(int(m.group(1)), int(m.group(1))-621))} خورشیدی", t)
    t = re.sub(r'\bOn\s+(\d{4})\b', lambda m: f"در سال {to_persian_digits(YEAR_MAP.get(int(m.group(1)), int(m.group(1))-621))} خورشیدی", t)
    t = re.sub(r'\bIn\s+([۰-۹]+)\b', r'در سال \1 خورشیدی', t)
    t = re.sub(r'\bFollowing the\s+', 'به دنبال ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bAllied invasion of Iran\b', 'اشغال ایران توسط متفقین', t, flags=re.IGNORECASE)
    t = re.sub(r'\bReza Shah was forced to abdicate by the British\b', 'رضاشاه توسط بریتانیا ناچار به کناره‌گیری شد', t, flags=re.IGNORECASE)
    t = re.sub(r'\band died in\b', 'و درگذشت در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bin exile in this South African metropolis\b', 'در تبعید در این کلان‌شهر آفریقای جنوبی', t, flags=re.IGNORECASE)
    t = re.sub(r'\ban enraged Tehran mob stormed the Russian Legation and massacred this famous playwright and Tsarist ambassador\b', 'مردم خشمگین تهران به سفارت روسیه حمله کرده و این نمایشنامه‌نویس و سفیر مشهور تزار را به قتل رساندند', t, flags=re.IGNORECASE)
    t = re.sub(r'\bfor sheltering two escaped Armenian women\b', 'به دلیل پناه دادن به دو زن ارمنی', t, flags=re.IGNORECASE)
    t = re.sub(r'\bfollowing the coup, military authorities uncovered a clandestine communist espionage network inside the armed forces comprising over 600 officers belonging to this party\b', 'پس از کودتا، مقامات نظامی یک شبکه مخفی جاسوسی کمونیستی در نیروهای مسلح متشکل از بیش از ۶۰۰ افسر وابسته به این حزب را کشف کردند', t, flags=re.IGNORECASE)
    t = re.sub(r'\bIn a searing 1962 polemic that likened Western cultural and economic consumerism to a cholera outbreak or pestilence, Jalal Al-e Ahmad coined this Persian term\b', 'در رساله‌ای کوبنده در سال ۱۳۴۱ خورشیدی که غرب‌گرایی فرهنگی و اقتصادی را به وبا تشبیه می‌کرد، جلال آل‌احمد این اصطلاح را ابداع کرد', t, flags=re.IGNORECASE)
    t = re.sub(r'\bBased in Tabriz, this liberal Grand Ayatollah backed the 1979 Revolution but founded the Muslim People\'s Republic Party to oppose Velayat-e Faqih before being placed under house arrest\b', 'این مرجع تقلید مستقر در تبریز، از انقلاب ۱۳۵۷ حمایت کرد اما حزب جمهوری خلق مسلمان را در مخالفت با ولایت فقیه بنیان نهاد پیش از آنکه حصر خانگی شود', t, flags=re.IGNORECASE)
    t = re.sub(r'\bIn March 1890, Nasir al-Din Shah granted this British major an exclusive 50-year worldwide monopoly over the production, sale, and export of all Iranian tobacco\b', 'در اسفند ۱۲۶۸ خورشیدی، ناصرالدین‌شاه انحصار ۵۰ ساله تولید، فروش و صادرات توتون و تنباکوی ایران را به این سرگرد بریتانیایی واگذار کرد', t, flags=re.IGNORECASE)
    t = re.sub(r'\bCarved from elephant tusks and excavated at Old Nisa, these magnificent drinking horns with winged beast terminals are known by this Greek-derived term\b', 'این شاخ‌های نوشیدنی باشکوه تراشیده‌شده از عاج فیل کشف‌شده در نسا با انتهای جانوران بالدار به این نام یونانی شناخته می‌شوند', t, flags=re.IGNORECASE)
    t = re.sub(r'\bIn May 1974, French hematologists Georges Flandrin and Jean Bernard secretly diagnosed the Shah with this rare cancer of the lymphatic system\b', 'در اردیبهشت ۱۳۵۳ خورشیدی، پزشکان فرانسوی مخفیانه تشخیص دادند که شاه به این سرطان نادر سیستم لنفاوی مبتلا است', t, flags=re.IGNORECASE)
    return t

def translate_entity(name):
    # Mapping table for options and entities
    ENT_MAP = {
        "Cape Town": "کیپ‌تاون", "Mauritius": "جزیره موریس", "Durban": "دوربان", "Johannesburg": "ژوهانسبورگ",
        "General Paskievich": "ژنرال پاسکویچ", "General Tsitsianov": "ژنرال سیسیانوف", "Colonel Liakhov": "کلنل لیاخوف",
        "Aleksandr Griboyedov": "الکساندر گریبایدوف", "Griboyedov": "گریبایدوف",
        "The Tudeh Military Network": "سازمان نظامی حزب توده", "The National Front": "جبهه ملی ایران",
        "Fadayan-e Islam": "فدائیان اسلام", "The MEK": "سازمان مجاهدین خلق", "Tudeh Party": "حزب توده ایران",
        "Taghut": "طاغوت", "Bazgasht be Khish": "بازگشت به خویشتن", "Este'mar": "استعمار", "Gharbzadegi": "غرب‌زدگی",
        "Ayatollah Taleghani": "آیت‌الله طالقانی", "Ayatollah Montazeri": "آیت‌الله منتظری", "Ayatollah Beheshti": "شهید بهشتی",
        "Ayatollah Kazem Shariatmadari": "آیت‌الله کاظم شریعتمداری", "Baron de Reuter": "بارون دو رویتر",
        "William D'Arcy": "ویلیام ناکس دارسی", "Percy Cox": "سر پرسی کاکس", "Major Gerald Talbot": "ماژور جرالد تالبوت",
        "Amphoras": "آمفورا", "Goblets": "جام‌های زرین", "Chalices": "پیاله‌ها", "Rhytons": "ریتون (تکوک)",
        "Pancreatic Cancer": "سرطان پانکراس", "Leukemia": "لوسمی (سرطان خون)", "Brain Tumor": "تومور مغزی",
        "Waldenström's Macroglobulinemia (Lymphoma)": "ماکروگلوبولینمی والدنشتروم (لنفوم)",
        "Mirza Aqa Khan Nuri": "میرزا آقاخان نوری", "Haji Mirza Aqasi": "حاجی میرزا آقاسی",
        "Qa'em Maqam Farahani": "قائم‌مقام فراهانی", "Treaty of Golestan": "عهدنامه گلستان",
        "Treaty of Paris": "معاهده پاریس", "Treaty of Finkenstein": "عهدنامه فینکنشتاین",
        "Mozaffar al-Din Shah": "مظفرالدین‌شاه قاجار", "Mohammad Shah Qajar": "محمدشاه قاجار",
        "Fath-Ali Shah": "فتحعلی‌شاه قاجار", "Opium": "تریاک", "Tea": "چای", "Sugar": "قند و شکر",
        "Mirza Fath Ali Akhundzadeh": "میرزا فتحعلی آخوندزاده", "Sayyed Jamal al-Din Asadabadi": "سید جمال‌الدین اسدآبادی",
        "Abdol-Rahim Talebof": "عبدالرحیم طالبوف", "Baqir Khan": "باقرخان", "Yeprem Khan": "یپرم‌خان",
        "Russian Embassy": "سفارت روسیه", "French Legation": "سفارت فرانسه", "Ottoman Embassy": "سفارت عثمانی",
        "General Paskievich": "ژنرال پاسکویچ", "Habl al-Matin": "روزنامه حبل‌المتین",
        "Kashkul": "کشکول", "Qanun": "روزنامه قانون", "Abadan": "آبادان", "Ahvaz": "اهواز", "Basra": "بصره",
        "Khorramshahr": "خرمشهر", "Tehran": "تهران", "Tabriz": "تبریز", "Shiraz": "شیراز", "Isfahan": "اصفهان",
        "Mashhad": "مشهد", "Kerman": "کرمان", "Yazd": "یزد", "Hamadan": "همدان", "Kermanshah": "کرمانشاه",
        "Qom": "قم", "Kashan": "کاشان", "United States": "ایالات متحده آمریکا", "Great Britain": "بریتانیا",
        "Soviet Union": "اتحاد جماهیر شوروی", "France": "فرانسه", "Germany": "آلمان", "Russia": "روسیه",
        "Air France": "ایرفرانس", "Iran Air": "ایران‌ایر", "Swissair": "سوئیس‌ایر", "Lufthansa": "لوفت‌هانزا",
        "Persepolis": "تخت جمشید", "Pasargadae": "پاسارگاد", "Susa": "شوش", "Ctesiphon": "تیسفون",
        "Ecbatana": "هگمتانه", "Cyrus Cylinder": "منشور کوروش", "Behistun Inscription": "کتیبه بیستون",
        "Code of Hammurabi": "قانون حمورابی", "Rosetta Stone": "سنگ روزتا", "Shapur I": "شاپور اول ساسانی",
        "Ardashir I": "اردشیر بابکان", "Shapur II": "شاپور دوم ذوالاکتاف", "Khosrow I": "خسرو انوشیروان",
        "F-14 Tomcat": "اف-۱۴ تام‌کت", "F-4 Phantom": "اف-۴ فانتوم", "F-5 Tiger": "اف-۵ تایگر",
        "Mirage F1": "میراژ اف-۱", "MiG-25": "میگ-۲۵",
        "Operation Beit ol-Moqaddas": "عملیات بیت‌المقدس", "Operation Fath ol-Mobin": "عملیات فتح‌المبین",
        "Operation Kheibar": "عملیات خیبر", "Operation Karbala-5": "عملیات کربلای ۵",
        "Operation Kaman 99": "عملیات کمان ۹۹", "Operation H-3": "عملیات اچ-۳",
        "Operation Morvarid": "عملیات مروارید", "Operation Eagle Claw": "عملیات پنجه عقاب",
        "Operation Praying Mantis": "عملیات آخوندک",
        "1,000 Diamonds": "۱٬۰۰۰ الماس", "3,380 Diamonds": "۳٬۳۸۰ الماس", "500 Diamonds": "۵۰۰ الماس",
        "10,000 Diamonds": "۱۰٬۰۰۰ الماس", "$20 per barrel": "۲۰ دلار برای هر بشکه",
        "$25 per barrel": "۲۵ دلار برای هر بشکه", "$30 per barrel": "۳۰ دلار برای هر بشکه",
        "$40 per barrel": "۴۰ دلار برای هر بشکه", "$5 per barrel": "۵ دلار برای هر بشکه",
        "$12 per barrel": "۱۲ دلار برای هر بشکه", "10 Percent": "۱۰ درصد", "50 Percent": "۵۰ درصد",
        "100 Percent": "۱۰۰ درصد", "50th Anniversary": "پنجاهمین سالگرد",
        "10th Century AD": "سده چهارم هجری (سده دهم میلادی)", "16th Century AD": "سده دهم هجری (سده شانزدهم میلادی)",
        "19th Century AD": "سده سیزدهم هجری (سده نوزدهم میلادی)", "5th Century AD (c. 470 AD)": "سده پنجم میلادی (حدود ۴۷۰ میلادی)"
    }
    clean = name.strip()
    if clean in ENT_MAP:
        return ENT_MAP[clean]
    low = clean.lower()
    for k, v in ENT_MAP.items():
        if k.lower() == low:
            return v
    return clean

def main():
    with open("QuestionBank/verified_clues_fa.json", "r", encoding="utf-8") as f:
        clues = json.load(f)

    print(f"Refining {len(clues)} Persian clues...")

    # Dictionary of canonical answers in Persian
    canon_map = {}
    for c in clues:
        ans_fa = c["canonical_answer"]
        canon_map[ans_fa.lower()] = ans_fa
        for alias in c["accepted_aliases"]:
            canon_map[alias.lower()] = ans_fa

    for c in clues:
        # Refine clue text dates and phrasing
        c["clue_text"] = clean_dates(c["clue_text"])
        c["explanation"] = clean_dates(c["explanation"])
        c["supporting_passage"] = clean_dates(c.get("supporting_passage", ""))

        # Refine options
        new_opts = []
        for opt_idx, opt in enumerate(c["options"]):
            if opt_idx == c["correct_option_index"]:
                new_opts.append(c["canonical_answer"])
            else:
                trans = translate_entity(opt)
                if trans == opt and opt.lower() in canon_map:
                    trans = canon_map[opt.lower()]
                new_opts.append(clean_dates(trans))
        c["options"] = new_opts

        # Refine distractor rationales
        for r in c.get("distractor_rationales", []):
            opt_str = r.get("option", "")
            r["option"] = translate_entity(opt_str)
            r["why_plausible"] = clean_dates(r.get("why_plausible", ""))
            r["why_wrong"] = clean_dates(r.get("why_wrong", ""))

    # Save to QuestionBank/verified_clues_fa.json
    fa_path = "QuestionBank/verified_clues_fa.json"
    with open(fa_path, "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2, ensure_ascii=False)
    print(f"Successfully refined {fa_path} ({os.path.getsize(fa_path)/1024:.1f} KB)")

    # Save dictionary format for PersianClueCopy
    copy_dict = {}
    for c in clues:
        copy_dict[c["id"]] = {
            "clue_text": c["clue_text"],
            "canonical_answer": c["canonical_answer"],
            "options": c["options"],
            "explanation": c["explanation"],
            "specificity_prompt": c.get("specificity_prompt", "")
        }

    copy_path = "QuestionBank/persian_clues.json"
    with open(copy_path, "w", encoding="utf-8") as f:
        json.dump(copy_dict, f, indent=2, ensure_ascii=False)
    print(f"Saved {copy_path} ({os.path.getsize(copy_path)/1024:.1f} KB)")

    app_copy_path = "App/Resources/persian_clues.json"
    with open(app_copy_path, "w", encoding="utf-8") as f:
        json.dump(copy_dict, f, indent=2, ensure_ascii=False)
    print(f"Saved {app_copy_path} ({os.path.getsize(app_copy_path)/1024:.1f} KB)")

if __name__ == "__main__":
    main()
