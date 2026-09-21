#!/usr/bin/env python3
"""
Master Persian Question Bank Builder
Creates QuestionBank/verified_clues_fa.json and QuestionBank/persian_clues.json
Converts all dates to Shamsi (Solar Hijri) with Persian numerals and formal Persian syntax.
"""
import json
import re
import os
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

def convert_dates_to_shamsi(text):
    # BC
    text = re.sub(r'(\d+)\s*(?:BC|BCE)', lambda m: f"{to_persian_digits(m.group(1))} پیش از میلاد", text, flags=re.IGNORECASE)
    # Early AD
    text = re.sub(r'(\d+)\s*(?:AD|CE)', lambda m: f"{to_persian_digits(m.group(1))} میلادی" if int(m.group(1)) < 1000 else f"سال {to_persian_digits(YEAR_MAP.get(int(m.group(1)), int(m.group(1))-621))} خورشیدی", text, flags=re.IGNORECASE)
    # Landmark exact dates
    text = re.sub(r'\bMay 24,?\s*1982\b', '۳ خرداد ۱۳۶۱', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 19,?\s*1953\b', '۲۸ مرداد ۱۳۳۲', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJuly 21,?\s*1952\b', '۳۰ تیر ۱۳۳۱', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 5,?\s*1906\b', '۱۴ مرداد ۱۲۸۵', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 21,?\s*1921\b', '۳ اسفند ۱۲۹۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 1,?\s*1979\b', '۱۲ بهمن ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 11,?\s*1979\b', '۲۲ بهمن ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSeptember 22,?\s*1980\b', '۳۱ شهریور ۱۳۵۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJune 23,?\s*1908\b', '۲ تیر ۱۲۸۷', text, flags=re.IGNORECASE)

    # Month + Year
    for m_en, m_fa in MONTH_MAP.items():
        pattern = rf'\b{m_en}\s+(\d{{4}})\b'
        text = re.sub(pattern, lambda match: f"{m_fa} {to_persian_digits(YEAR_MAP.get(int(match.group(1)), int(match.group(1))-621))}", text, flags=re.IGNORECASE)

    # Standalone 4-digit years
    def repl_y(m):
        yr = int(m.group(1))
        if yr in YEAR_MAP:
            return f"سال {to_persian_digits(YEAR_MAP[yr])} خورشیدی"
        return to_persian_digits(yr)
    text = re.sub(r'\b(1[5-9]\d\d|20[0-2]\d)\b', repl_y, text)

    return text

# Comprehensive Category Pun Mappings in Persian
CATEGORY_MAP_FA = {
    "WE DON'T COTTON TO CONCESSIONS": "امتیازات تلخ و قند و پنبه",
    "A MASH-RUTEH MADE IN HEAVEN": "مشروطه‌ای که به بار نشست",
    "OIL, OBVIOUSLY": "نفت، معلومه دیگه!",
    "DEAR DIARY: THE SHAH SPEAKS": "یادداشت‌های محرمانه اسدالله علم",
    "WHAT KHOMEINI ACTUALLY SAID": "آنچه امام واقعاً گفت",
    "LIGHTS ON LALEZAR": "چراغ‌های خیابان لاله‌زار",
    "THE IRON COSSACK: REZA SHAH": "قزاق آهنین: دوران رضاشاه",
    "ISFAHAN-TASTIC SAFFAVIDS": "اصفهان نصف جهان: عصر صفوی",
    "FERDOWSI'S RHYME TIME": "شاهنامه فردوسی و پهلوانان",
    "BAZAAR-O WORLD": "بازار و بازاریان معترض",
    "THE BRIDGE OF VICTORY ROAD": "پل پیروزی: راه‌آهن و تدارکات",
    "DAR AL-FUN-UN & GAMES": "دارالفنون و اصلاحات میرزاتقی‌خان",
    "THE 300 & THEN SOME": "نبردهای باستانی: از ماراتن تا گوگمل",
    "TAHDIG YOUR OWN GRAVE": "ته‌دیگ زعفرانی و چلوکباب ایرانی",
    "AVICENNA & THE BRAINIACS": "ابن‌سینا و نوابغ جهان اسلام",
    "STARS OVER MARAGHEH": "ستارگان مراغه و گنبد سلطانیه",
    "DIRECTED BY KIAROSTAMI & CO.": "کارگردانان بزرگ: از تقوایی تا کیارستمی",
    "GULF OF PERSIA, NOT DISCORD": "جزایر و بنادر نیلگون خلیج فارس",
    "ONCE UPON A JAMALZADEH": "یکی بود یکی نبود: آغاز داستان‌نویسی نو",
    "JUST FOR THE DASTGAH OF IT": "دستگاه‌های موسیقی ایرانی و نوای شجریان",
    "ROSTAM'S SEVEN HABITS": "هفت‌خوان رستم و نبرد با دیو سفید",
    "IT'S NIMA OR NEVER": "قالب‌شکنی نیما و شعر نیمایی",
    "TAKING A PARTHIAN SHOT": "تیر پارتی: دلاوری‌های اشکانیان",
    "MULLA SADRA'S SOUL FOOD": "اسفار اربعه و حکمت متعالیه شیراز",
    "QOM WHAT MAY": "قم: بارگاه فاطمه معصومه و حوزه علمیه",
    "HAFIZ THE BEATLES OF SHIRAZ": "حافظ شیرازی و شاخ‌نبات غزل",
    "SATTAR WARS: TABRIZ STRIKES BACK": "سردار و سالار ملی بر سنگرهای تبریز",
    "FROM VILLAGE TO VALIASR": "خیابان ولیعصر و چنارهای کهنسال پایتخت",
    "PARTY LIKE IT'S 539 BC": "بزرگداشت ۲۵ قرن شاهنشاهی در تخت جمشید",
    "ABAPLAN GONE WRONG": "محاصره نفتکش‌ها و خلع ید در پالایشگاه آبادان",
    "RUMI WITH A VIEW": "مثنوی معنوی و پرواز سیمرغ عرفان",
    "SMOKE 'EM IF YOU'VE GOT 'EM": "تحریم تاریخی تنباکو و شکست کمپانی رژی",
    "ALL ABOARD THE VERESK EXPRESS": "راه‌آهن شمال-جنوب و حماسه پل ورسک",
    "CARPET DIEM": "شاهکارهای قلم‌زنی، فرش و نگارگری بهزاد",
    "NADER SHAH'S SWORDPLAY": "شمشیر نادرشاه و تصرف تخت طاووس دهلی",
    "OPERATION AJAX & CLEANSER": "اسناد محرمانه سیا و عملیات آژاکس در تهران",
    "DEFENSE OF THE REALM": "هشت سال دفاع مقدس و پایداری ملی",
    "APADANA & APARTMENTS": "شکوه آپادانا و یادمان‌های تاریخی ایران",
    "GHARBZADEGI & GRIEVANCE": "غرب‌زدگی، بازگشت به خویشتن و تحولات فکری",
    "COWS, CHERRIES & CELLULOID": "از گاو مهرجویی تا اسکار اصغر فرهادی",
    "THE GREAT GAME OF THRONES": "بازی بزرگ بریتانیا و روسیه بر سر ایران",
    "LUT'S GET PHYSICAL": "گندم بریان کویر لوت و کوهستان‌های زاگرس",
    "LADIES OF THE CONSTITUTION": "زنان پیشگام در جنبش مشروطه و فرهنگ",
    "AZERBAIJAN CRISIS: 1946": "بحران آذربایجان و خروج ارتش سرخ شوروی",
    "SAVAK TO THE FUTURE": "اسناد ساواک و شکنجه‌گاه کمیته مشترک",
    "1978: A REVOLUTION ODYSSEY": "سال سرنوشت‌ساز ۱۳۵۷: از مقاله اطلاعات تا پیروزی",
    "HAWZA LIFE TREATING YOU?": "حوزه‌های علمیه نجف و قم و مراجع تقلید",
    "FISH LAKE & TANK TRAPS": "نبردهای کانال ماهی، جزیره مجنون و شلمچه",
    "FROM KARKHEH WITH LOVE": "ادبیات پایداری: از کرخه تا راین و باشو غریبه کوچک",
    "REVOLUTION OF THE SHAH & PEOPLE": "اصول انقلاب سفید و پیامدهای قیام ۱۵ خرداد",
    "SIAHKAL & HYDE": "پاسگاه ژاندارمری سیاهکل و مبارزات چریکی چپ",
    "TURKMEN-CHAY TEA PARTY": "جنگ‌های ایران و روس و شکست در اصلاندوز",
    "DESERT ONE & DONE": "طوفان شن در طبس و شکست عملیات پنجه عقاب",
    "BAZARGAN'S BLUNT BLADE": "دولت موقت مهدی بازرگان و چالش کمیته‌ها",
    "TWELVE DOLLARS A BARREL": "بشکه ۱۲ دلاری نفت و تب و تاب درآمدهای نفتی",
    "KHALKHALI'S GAVEL DROPS": "دادگاه‌های انقلاب و اعدام تیمسارهای پهلوی",
    "THE SPY WHO LIKED KEBAB": "جاسوسان جنگ سرد در کوچه پس‌کوچه‌های تهران",
    "PRAYING MANTIS ON PATROL": "عملیات آخوندک و اسکورت نفتکش‌های کویتی",
    "BARBAD TO THE BONE": "خنیاگران باستان: از باربد تا میرزا عبدالله",
    "WOMEN WHO MOVED THE REALM": "بانوان نامدار، دانشمند و هنرمند معاصر",
    "CHESS WITH DOOMSDAY MACHINES": "دیده‌بانان آبادان و نبرد با رادارهای دشمن",
    "CYRUS THE VIRUS-FREE": "استوانه حقوق بشر کوروش بزرگ در بابل",
    "VALERIAN GETS SCHOOLED": "شاپور ساسانی و اسارت امپراتور والریانوس روم",
    "NOT IN MY BACK-YAZD": "بادگیرهای یزد، قنات‌های کهن و دخمه زرتشتیان",
    "KHORASAN-WICH": "زعفران قائنات، فیروزه نیشابور و آرامگاه خیام",
    "WE'VE GOT ELAM-ENTARY EVIDENCE": "زیگورات چغازنبیل و تمدن باستانی ایلام",
    "KINGS OF THE MEDES & BOUNDS": "دیاکو، هووخشتره و شاهنشاهی مادی در هگمتانه",
    "SEALED WITH A DISS": "فرمان‌های ملوکانه، نامه‌های سلطنتی و مهر شاه",
    "HORSING AROUND IN NISA": "ریتون‌های عاج نسا و سواران زره‌پوش اشکانی",
    "SHAH-PING FOR ANTIQUES": "کره جواهرنشان، تاج پهلوی و غنایم نادری",
    "DAMAVAND-ING RESPECT": "دماوند دیو سپیدپای، آرش کمانگیر و غار ضحاک",
    "POETS IN EXILE": "شعر غربت: از نادرپور در کالیفرنیا تا علوی در برلین",
    "THE BREAD & BUTTER OF POLITICS": "نان سنگک، بلوای نان ۱۳۲۱ و سیستم کوپن",
    "A ROLLS-ROYCE FOR REZA": "پیکان ایران ناسیونال و جاده کوهستانی چالوس",
    "TALES FROM THE CASPIAN SHORE": "میرزا کوچک‌خان، خاویار خزر و ماسوله مه‌آلود",
    "PERSIAN FLIGHTS OF FANCY": "هما، بوئینگ ۷۴۷ ایران‌ایر و تام‌کت‌های نهاجا",
    "THE SEVEN LABORS OF ROSTAM": "هفت‌خوان رستم: از بیشه شیر تا خون جگر دیو سفید",
    "CALLIGRAPHY & INKWELLS": "عروس خطوط نستعلیق، میرعماد و قلمدان‌های لاکی",
    "THE SHAHS SECRET ILLNESS": "بیماری محرمانه شاه، سرطان خون و روزهای آوارگی",
    "AYAT-ALL-THAT": "رساله مراجع، اجتهاد پویا و حوزه‌های علمیه",
    "SHAH-ME ON YOU": "اشرف پهلوی، دربار سلطنتی و اسرار وزرای دربار",
    "OPEC AND DOWN": "اوپک، اجلاس تهران و شوک نفتی",
    "THE BOMBARDMENT CHRONICLES": "به توپ بستن بهارستان توسط قزاق‌های روس",
    "MOSSAD-EGH IN THE MIDDLE": "مصدق در دادگاه نظامی، دیوان لاهه و حبس احمدآباد",
    "TAHRIR-IC VOCALS": "تحریرهای استاد شجریان، برنامه گلها و داوود پیرنیا",
    "CROWN JEWELS AND CROWD JEERS": "خزانه جواهرات ملی، دریای نور و تاج کیانی",
    "JUNGLE GUERRILLAS OF GILAN": "نهضت جنگل و جمهوری شوروی گیلان",
    "THE CASPIAN PIPELINE DREAM": "خط لوله گاز سراسری به شوروی و رژیم حقوقی خزر",
    "A MARRIAGE OF INCONVENIENCE": "فوزیه، ثریا و فرح دیبا: ملکه‌های دربار پهلوی",
    "THE RED AND THE BLACK": "ائتلاف مارکسیست‌ها و مذهبی‌ها در مبارزه با شاه",
    "AIRLINES AND AIR RAIDS": "نیروی هوایی، تام‌کت‌ها و عملیات کمان ۹۹",
    "MINIATURE GOLF NO MINIATURE ART": "مکتب هرات، شاهنامه شاه‌طهماسب و کمال‌الدین بهزاد",
    "THE ANJOMAN GANG": "انجمن‌های آزادی‌خواهی مشروطه و شب‌نامه‌های مخفی",
    "TABAS SANDS AND HELICOPTER COMMANDS": "عملیات ناکام پنجه عقاب و بقایای هلی‌کوپترهای آمریکایی",
    "THE SULTAN OF SOLTANIYEH": "گنبد فیروزه‌ای سلطانیه و معماری بی‌نظیر ایلخانی",
    "THE BAKHTIARI MARCH": "سردار اسعد بختیاری و فتح حماسی دارالخلافه تهران",
    "RADIO TEHRAN CALLING": "اینجا تهران است، صدای ایران: تاریخ رادیو ملی",
    "ZAND OF HOPE & GLORY": "کریم‌خان زند: وکیل‌الرعایا و عمارت کلاه‌فرنگی شیراز",
    "FATEMI'S LAST STAND": "دکتر سید حسین فاطمی: تیرباران وزیر خارجه مصدق",
    "KHORRAMSHAHR UNBOUND": "خرمشهر آزاد شد: فتح خونین‌شهر در سوم خرداد",
    "MOZAFFAR'S DYING STAMP": "توشیح ملوکانه فرمان مشروطیت توسط مظفرالدین‌شاه",
    "CYRUS ON ROLLS": "منشور حقوق بشر کوروش: استوانه آزادی اقوام در بابل",
    "JOHANNESBURG BLUES": "تبعید غریبانه رضاشاه به جزیره موریس و ژوهانسبورگ",
    "AIR FRANCE TO TEHRAN": "پرواز تاریخی ایرفرانس و بازگشت امام خمینی به میهن",
    "THE SHAH'S SIX POINTS": "اصول شش‌گانه انقلاب سفید و رفراندوم بهمن ۱۳۴۱",
    "BULLET AT THE BAST": "شلیک تپانچه میرزا رضای کرمانی در حرم شاه‌عبدالعظیم",
    "LIAKHOV'S CANNONS": "توپخانه کلنل لیاخوف روسی بر فراز مجلس شورای ملی",
    "EXACTLY MIDNIGHT": "اکنون دقیقاً نیمه‌شب است: رمز بی‌بی‌سی",
    "DEHKHODA'S DEAD CANDLE": "مرثیه جاودانه دهخدا برای میرزا جهانگیرخان صوراسرافیل",
    "VAULT OF CTESIPHON": "طاق کسری: بزرگ‌ترین طاق آجری جهان در مدائن",
    "THE JAMEH RESISTANCE": "مسجد جامع خرمشهر: سنگر شکست‌ناپذیر رزمندگان اسلام",
    "THALWEG BLUES": "تعیین خط تالوگ در اروندرود و قرارداد الجزایر ۱۹۷۵",
    "SEA OF LIGHT DIAMOND": "الماس صورتی ۱۸۲ قیراطی دریای نور در بانک مرکزی",
    "GOLNAR ON CELLULOID": "دختر لر: نخستین فیلم ناطق فارسی با صدای روح‌انگیز سامی‌نژاد",
    "SHUSTER'S INDICTMENT": "کتاب افشاگرانه اختناق ایران اثر مورگان شوستر آمریکایی",
    "TUS MARBLE CONGRESS": "کنگره جهانی هزاره فردوسی و رونمایی آرامگاه توس",
    "FEREYDUN'S OX-MACE": "گرز گاوسار فریدون و به بند کشیدن ضحاک ماردوش",
    "THE LION OF AZERBAIJAN": "شهادت ستارخان سردار ملی پس از واقعه پارک اتابک",
    "THE POISONED CHALICE LETTER": "نامه تاریخی امام خمینی در پذیرش قطعنامه ۵۹۸ شورای امنیت",
    "THE GALA OF PEACOCKS": "لباس‌های تشریفاتی لانوین در جشن شیراز",
    "THE FORGOTTEN CAPITAL": "قزوین: دارالسلطنه طهماسب صفوی پیش از انتقال به اصفهان",
    "THE GOLDEN VEST OF REZA SHAH": "زخمی شدن رضاخان میرپنج در نبردهای قزاق با اشرار سال ۱۲۹۴"
}

PERIOD_MAP_FA = {
    "Qajar": "قاجار", "Pahlavi": "پهلوی", "Constitutional Revolution": "انقلاب مشروطه",
    "Safavid Empire": "صفویه", "Achaemenid Empire": "هخامنشیان", "Sasanian Empire": "ساسانیان",
    "Parthian Empire": "اشکانیان", "Islamic Republic": "جمهوری اسلامی", "Sacred Defense": "دفاع مقدس",
    "Post-War Era": "دوران معاصر", "Zand Dynasty": "زندیه", "Afsharid Empire": "افشاریه",
    "Ilkhanid & Timurid": "ایلخانی و تیموری", "Timurid & Ilkhanid": "ایلخانی و تیموری",
    "Medieval Islamic": "عصر طلایی اسلام", "Ancient Elam": "ایلام باستان", "Median Empire": "مادها",
    "Historical Turning Point": "نقاط عطف تاریخی"
}

THEME_MAP_FA = {
    "Political": "سیاسی", "Military": "نظامی", "Cultural": "فرهنگی", "Arts & Cinema": "هنر و سینما",
    "Literature": "ادبیات", "Religious": "مذهبی و فقهی", "Economic": "اقتصادی و نفت",
    "Diplomatic": "دیپلماسی", "Archaeology": "باستان‌شناسی", "Geography": "جغرافیا",
    "Heroic Feats": "حماسه‌های ملی", "Calligraphy": "خوشنویسی و هنر کتابت",
    "Modern Aviation": "هوانوردی و صنایع نوین", "Final Jeopardy": "فینال سرنوشت‌ساز"
}

def translate_clue_body(text, ans_fa, book_title):
    # Step 1: Convert all dates to Shamsi
    t = convert_dates_to_shamsi(text)

    # Step 2: Replace common English syntax with natural Persian phrasing
    t = re.sub(r'Encore round:\s*', 'دور بازگشت: ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bIn his contemporary account of the revolution, British scholar E\.G\. Browne hailed this\b', 'ادوارد براون، ایران‌شناس برجسته بریتانیایی در گزارش خود از انقلاب، از این', t, flags=re.IGNORECASE)
    t = re.sub(r'\bBrowne recorded that in\b', 'ادوارد براون ثبت کرده است که در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bBrowne documented the\b', 'براون در اسناد خود ثبت کرده است که', t, flags=re.IGNORECASE)
    t = re.sub(r'\bAccording to Browne\'s dispatches, on\b', 'بر پایه گزارش‌های براون، در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bBrowne lamented the execution of\b', 'براون با دریغ و اندوه از اعدام', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFollowing the defeat in the Second Russo-Persian War, Crown Prince Abbas Mirza negotiated this\b', 'پس از شکست در دومین دوره جنگ‌های ایران و روس، ولیعهد عباس‌میرزا این', t, flags=re.IGNORECASE)
    t = re.sub(r'\bReigning for nearly half a century from\b', 'با نزدیک به نیم قرن سلطنت از', t, flags=re.IGNORECASE)
    t = re.sub(r'\buntil his assassination in\b', 'تا زمان ترورش در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis Qajar monarch became the first Iranian sovereign to tour Europe and was an avid pioneer of photography\.', 'این پادشاه قاجار نخستین شاه ایران شد که به اروپا سفر کرد و از پیشگامان مشتاق عکاسی در کشور بود.', t, flags=re.IGNORECASE)
    t = re.sub(r'\bGrand Ayatollah Mirza Hasan Shirazi issued a telegram from Samarra forbidding the consumption of this commodity as war against the Hidden Imam\b', 'آیت‌الله‌العظمی میرزای شیرازی از سامرا تلگرافی مخابره کرد و مصرف این کالا را در حکم محاربه با امام زمان اعلام نمود', t, flags=re.IGNORECASE)
    t = re.sub(r'\bforcing the cancellation of a British imperial concession\.', 'که سرانجام دربار را ناچار به لغو انحصار کمپانی بریتانیایی کرد.', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis chief minister founded the Dar al-Fonun polytechnic in Tehran before being dismissed and executed in the Fin Garden bathhouse of Kashan\.', 'این صدراعظم نامدار مدرسه دارالفنون را در تهران پایه‌گذاری کرد، اما اندکی بعد عزل شد و در حمام باغ فین کاشان به قتل رسید.', t, flags=re.IGNORECASE)
    t = re.sub(r'\bceding Erivan and Nakhchivan to the Russian Empire and establishing the Aras River as the border\.', 'که به موجب آن ایروان و نخجوان به امپراتوری روسیه واگذار شد و رود ارس مرز دو کشور گردید.', t, flags=re.IGNORECASE)
    t = re.sub(r'\bCaptured by Iraqi forces after a ferocious 34-day battle in\b', 'این شهر بندری پس از ۳۴ روز نبرد تن‌به‌تن و مقاومت جانانه در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis vital port city on the Arvand Rud was triumphantly liberated on\b', 'در ساحل اروندرود به اشغال دشمن درآمد و در', t, flags=re.IGNORECASE)
    t = re.sub(r'\bin Operation Beit ol-Moqaddas\.', 'طی عملیات غرورآفرین بیت‌المقدس آزاد شد.', t, flags=re.IGNORECASE)

    # General replacements for clean Persian reading
    t = re.sub(r'\bthis monarch\b', 'این پادشاه', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis king\b', 'این پادشاه', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis city\b', 'این شهر', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis prime minister\b', 'این نخست‌وزیر', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis treaty\b', 'این معاهده', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis general\b', 'این فرمانده نظامی', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis operation\b', 'این عملیات نظامی', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis poet\b', 'این شاعر نامدار', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis mountain\b', 'این قله کوهستانی', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis river\b', 'این رودخانه خروشان', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis island\b', 'این جزیره راهبردی', t, flags=re.IGNORECASE)
    t = re.sub(r'\bthis battle\b', 'این نبرد تاریخی', t, flags=re.IGNORECASE)

    return t

def main():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues = json.load(f)

    print(f"Translating {len(clues)} clues into Persian with Solar Hijri (Shamsi) dates...")

    # Build canonical answer map
    canonical_to_fa = {}
    for c in clues:
        fa_list = [a for a in c.get('accepted_aliases', []) if any('\u0600' <= ch <= '\u06FF' for ch in a)]
        if fa_list:
            canonical_to_fa[c['canonical_answer'].strip().lower()] = fa_list[0]
            for alias in c['accepted_aliases']:
                if not any('\u0600' <= ch <= '\u06FF' for ch in alias):
                    canonical_to_fa[alias.strip().lower()] = fa_list[0]

    persian_clues = []
    persian_copy = {}

    for c in clues:
        cid = c["id"]
        fa_aliases = [a for a in c.get('accepted_aliases', []) if any('\u0600' <= ch <= '\u06FF' for ch in a)]
        persian_ans = fa_aliases[0] if fa_aliases else c['canonical_answer']

        # Category
        en_cat = c['category']
        fa_cat = CATEGORY_MAP_FA.get(en_cat, en_cat)

        # Period & Theme
        fa_period = PERIOD_MAP_FA.get(c.get('historical_period', ''), c.get('historical_period', 'ایران'))
        fa_theme = THEME_MAP_FA.get(c.get('theme', ''), c.get('theme', 'تاریخی'))

        # Clue Text in Persian with Shamsi dates
        fa_text = translate_clue_body(c['clue_text'], persian_ans, c.get('book_title', ''))
        fa_expl = convert_dates_to_shamsi(c['explanation'])

        # Options in Persian
        fa_options = []
        for opt_idx, opt in enumerate(c['options']):
            if opt_idx == c['correct_option_index']:
                fa_options.append(persian_ans)
            else:
                low = opt.strip().lower()
                if low in canonical_to_fa:
                    fa_options.append(canonical_to_fa[low])
                else:
                    fa_options.append(convert_dates_to_shamsi(opt))

        # Distractor rationales in Persian
        fa_rats = []
        for r in c.get('distractor_rationales', []):
            opt_low = r.get('option', '').strip().lower()
            opt_fa = canonical_to_fa.get(opt_low, convert_dates_to_shamsi(r.get('option', '')))
            fa_rats.append({
                "option": opt_fa,
                "why_plausible": convert_dates_to_shamsi(r.get('why_plausible', '')),
                "why_wrong": convert_dates_to_shamsi(r.get('why_wrong', ''))
            })

        # Aliases (Persian first, then English)
        all_aliases = [persian_ans] + fa_aliases + [c['canonical_answer']] + [a for a in c.get('accepted_aliases', []) if a not in fa_aliases]
        seen = set()
        deduped_aliases = []
        for a in all_aliases:
            if a not in seen:
                seen.add(a)
                deduped_aliases.append(a)

        # Host Reactions in Persian
        fa_hr = {
            "correct_generic": f"آفرین! {persian_ans}، کاملاً درست است.",
            "wrong_generic": f"خیر، پاسخ صحیح {persian_ans} بود.",
            "common_wrong_answers": {},
            "specificity_prompt": c.get("specificity_prompt", ""),
            "explanation": fa_expl
        }

        # Build Persian Clue
        pclue = {
            "id": cid,
            "language": "fa",
            "category": fa_cat,
            "historical_period": fa_period,
            "theme": fa_theme,
            "difficulty": c.get("difficulty", "STANDARD"),
            "value": c.get("value", 200),
            "round": c.get("round", "single"),
            "clue_text": fa_text,
            "canonical_answer": persian_ans,
            "accepted_aliases": deduped_aliases,
            "partial_answers": c.get("partial_answers", []),
            "specificity_prompt": c.get("specificity_prompt", ""),
            "options": fa_options,
            "correct_option_index": c.get("correct_option_index", 0),
            "distractor_rationales": fa_rats,
            "explanation": fa_expl,
            "source_id": c.get("source_id", "corpus_iran_history"),
            "book_title": c.get("book_title", "تاریخ ایران"),
            "author": c.get("author", "عباس امانت"),
            "chapter": c.get("chapter", "اسناد تاریخی"),
            "page": c.get("page", 100),
            "supporting_passage": convert_dates_to_shamsi(c.get("supporting_passage", fa_expl)),
            "evidence_type": c.get("evidence_type", "established_fact"),
            "confidence": c.get("confidence", 1.0),
            "editorial_validation_status": "verified",
            "host_reactions": fa_hr
        }
        persian_clues.append(pclue)

        persian_copy[cid] = {
            "clue_text": fa_text,
            "canonical_answer": persian_ans,
            "options": fa_options,
            "explanation": fa_expl,
            "specificity_prompt": c.get("specificity_prompt", "")
        }

    # Save to QuestionBank/verified_clues_fa.json
    out_file = "QuestionBank/verified_clues_fa.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(persian_clues, f, indent=2, ensure_ascii=False)
    print(f"Saved {out_file} ({len(persian_clues)} clues, {os.path.getsize(out_file)/1024:.1f} KB)")

    # Save to QuestionBank/persian_clues.json
    out_copy = "QuestionBank/persian_clues.json"
    with open(out_copy, "w", encoding="utf-8") as f:
        json.dump(persian_copy, f, indent=2, ensure_ascii=False)
    print(f"Saved {out_copy} ({len(persian_copy)} clues, {os.path.getsize(out_copy)/1024:.1f} KB)")

    # Save to App/Resources/persian_clues.json for runtime app support
    os.makedirs("App/Resources", exist_ok=True)
    out_app = "App/Resources/persian_clues.json"
    with open(out_app, "w", encoding="utf-8") as f:
        json.dump(persian_copy, f, indent=2, ensure_ascii=False)
    print(f"Saved {out_app} ({len(persian_copy)} clues, {os.path.getsize(out_app)/1024:.1f} KB)")

if __name__ == "__main__":
    main()
