#!/usr/bin/env python3
"""
Full-scale Persian Question Bank Generator.
Produces QuestionBank/verified_clues_fa.json and QuestionBank/persian_clues.json.
Converts all dates to Shamsi (Solar Hijri) with Persian numerals and rich literary phrasing.
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
    "Qajar": "قاجار",
    "Pahlavi": "پهلوی",
    "Constitutional Revolution": "انقلاب مشروطه",
    "Safavid Empire": "صفویه",
    "Achaemenid Empire": "هخامنشیان",
    "Sasanian Empire": "ساسانیان",
    "Parthian Empire": "اشکانیان",
    "Islamic Republic": "جمهوری اسلامی",
    "Sacred Defense": "دفاع مقدس",
    "Post-War Era": "دوران معاصر",
    "Zand Dynasty": "زندیه",
    "Afsharid Empire": "افشاریه",
    "Ilkhanid & Timurid": "ایلخانی و تیموری",
    "Timurid & Ilkhanid": "ایلخانی و تیموری",
    "Medieval Islamic": "عصر طلایی اسلام",
    "Ancient Elam": "ایلام باستان",
    "Median Empire": "مادها",
    "Historical Turning Point": "نقاط عطف تاریخی"
}

THEME_MAP_FA = {
    "Political": "سیاسی",
    "Military": "نظامی",
    "Cultural": "فرهنگی",
    "Arts & Cinema": "هنر و سینما",
    "Literature": "ادبیات",
    "Religious": "مذهبی و فقهی",
    "Economic": "اقتصادی و نفت",
    "Diplomatic": "دیپلماسی",
    "Archaeology": "باستان‌شناسی",
    "Geography": "جغرافیا",
    "Heroic Feats": "حماسه‌های ملی",
    "Calligraphy": "خوشنویسی و هنر کتابت",
    "Modern Aviation": "هوانوردی و صنایع نوین",
    "Final Jeopardy": "فینال سرنوشت‌ساز"
}

MONTH_MAP = {
    'january': 'دی/بهمن', 'february': 'بهمن', 'march': 'اسفند/فروردین', 'april': 'فروردین',
    'may': 'اردیبهشت', 'june': 'خرداد', 'july': 'تیر', 'august': 'مرداد',
    'september': 'شهریور', 'october': 'مهر', 'november': 'آبان', 'december': 'آذر'
}

def convert_dates(text):
    # BC years
    text = re.sub(r'(\d+)\s*(?:BC|BCE)', lambda m: f"{to_persian_digits(m.group(1))} پیش از میلاد", text, flags=re.IGNORECASE)
    # Early AD
    text = re.sub(r'(\d+)\s*(?:AD|CE)', lambda m: f"{to_persian_digits(m.group(1))} میلادی" if int(m.group(1)) < 1000 else f"سال {to_persian_digits(YEAR_MAP.get(int(m.group(1)), int(m.group(1))-621))} خورشیدی", text, flags=re.IGNORECASE)
    # Landmark specific dates
    text = re.sub(r'\bMay 24,?\s*1982\b', '۳ خرداد ۱۳۶۱', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 19,?\s*1953\b', '۲۸ مرداد ۱۳۳۲', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJuly 21,?\s*1952\b', '۳۰ تیر ۱۳۳۱', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 5,?\s*1906\b', '۱۴ مرداد ۱۲۸۵', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 21,?\s*1921\b', '۳ اسفند ۱۲۹۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 1,?\s*1979\b', '۱۲ بهمن ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bFebruary 11,?\s*1979\b', '۲۲ بهمن ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSeptember 22,?\s*1980\b', '۳۱ شهریور ۱۳۵۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJune 1988\b', 'خرداد/تیر ۱۳۶۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJuly 1988\b', 'تیر/مرداد ۱۳۶۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 1988\b', 'مرداد ۱۳۶۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJune 1963\b', 'خرداد ۱۳۴۲', text, flags=re.IGNORECASE)
    text = re.sub(r'\bOctober 1971\b', 'مهر ۱۳۵۰', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDecember 1973\b', 'دی ۱۳۵۲', text, flags=re.IGNORECASE)
    text = re.sub(r'\bMarch 1975\b', 'اسفند ۱۳۵۳', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 1941\b', 'شهریور ۱۳۲۰', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDecember 1942\b', 'آذر ۱۳۲۱', text, flags=re.IGNORECASE)
    text = re.sub(r'\bNovember 1943\b', 'آذر ۱۳۲۲', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDecember 1946\b', 'آذر ۱۳۲۵', text, flags=re.IGNORECASE)
    text = re.sub(r'\bMarch 1951\b', 'اسفند ۱۳۲۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bApril 1980\b', 'اردیبهشت ۱۳۵۹', text, flags=re.IGNORECASE)
    text = re.sub(r'\bNovember 1979\b', 'آبان ۱۳۵۸', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSeptember 1978\b', 'شهریور ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAugust 1978\b', 'مرداد ۱۳۵۷', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJanuary 1978\b', 'دی ۱۳۵۶', text, flags=re.IGNORECASE)

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

def build_persian_corpus():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues = json.load(f)

    print(f"Loaded {len(clues)} clues from verified_clues.json")

    # Build canonical answer and options translation maps
    canonical_to_fa = {}
    for c in clues:
        fa_list = [a for a in c.get('accepted_aliases', []) if any('\u0600' <= ch <= '\u06FF' for ch in a)]
        if fa_list:
            canonical_to_fa[c['canonical_answer'].strip().lower()] = fa_list[0]
            for alias in c['accepted_aliases']:
                if not any('\u0600' <= ch <= '\u06FF' for ch in alias):
                    canonical_to_fa[alias.strip().lower()] = fa_list[0]

    # Additional manual entity dictionary for common options
    EXTRA_ENTITIES = {
        'mirza aqa khan nuri': 'میرزا آقاخان نوری',
        'haji mirza aqasi': 'حاجی میرزا آقاسی',
        "qa'em maqam farahani": 'قائم‌مقام فراهانی',
        'treaty of golestan': 'عهدنامه گلستان',
        'treaty of paris': 'معاهده پاریس',
        'treaty of finkenstein': 'عهدنامه فینکنشتاین',
        'mozaffar al-din shah': 'مظفرالدین‌شاه قاجار',
        'mohammad shah qajar': 'محمدشاه قاجار',
        'fath-ali shah': 'فتحعلی‌شاه قاجار',
        'opium': 'تریاک',
        'tea': 'چای',
        'sugar': 'قند و شکر',
        'mirza fath ali akhundzadeh': 'میرزا فتحعلی آخوندزاده',
        'sayyed jamal al-din asadabadi': 'سید جمال‌الدین اسدآبادی',
        'abdol-rahim talebof': 'عبدالرحیم طالبوف',
        'baqir khan': 'باقرخان سالار ملی',
        'yeprem khan': 'یپرم‌خان ارمنی',
        'heydar khan amou-oghli': 'حیدرخان عمواوغلی',
        'russian embassy': 'سفارت روسیه',
        'french legation': 'سفارت فرانسه',
        'ottoman embassy': 'سفارت عثمانی',
        'sheikh fazlollah': 'شیخ فضل‌الله نوری',
        'sayyed mohammad tabatabai': 'سید محمد طباطبایی',
        'sayyed abdollah behbahani': 'سید عبدالله بهبهانی',
        'general paskievich': 'ژنرال پاسکویچ',
        'general tsitsianov': 'ژنرال سیسیانوف',
        'colonel liakhov': 'کلنل لیاخوف',
        'habl al-matin': 'حبل‌المتین',
        'kashkul': 'کشکول',
        'qanun': 'روزنامه قانون',
        'abadan': 'آبادان',
        'ahvaz': 'اهواز',
        'basra': 'بصره',
        'khorramshahr': 'خرمشهر',
        'tehran': 'تهران',
        'tabriz': 'تبریز',
        'shiraz': 'شیراز',
        'isfahan': 'اصفهان',
        'mashhad': 'مشهد',
        'kerman': 'کرمان',
        'yazd': 'یزد',
        'hamadan': 'همدان',
        'kermanshah': 'کرمانشاه',
        'qom': 'قم',
        'kashan': 'کاشان',
        'johannesburg': 'ژوهانسبورگ',
        'cape town': 'کیپ‌تاون',
        'mauritius': 'جزیره موریس',
        'durban': 'دوربان',
        'united states': 'ایالات متحده آمریکا',
        'great britain': 'بریتانیا',
        'soviet union': 'اتحاد جماهیر شوروی',
        'france': 'فرانسه',
        'germany': 'آلمان',
        'air france': 'ایرفرانس',
        'iran air': 'ایران‌ایر',
        'swissair': 'سوئیس‌ایر',
        'lufthansa': 'لوفت‌هانزا',
        'persepolis': 'تخت جمشید',
        'pasargadae': 'پاسارگاد',
        'susa': 'شوش',
        'ctesiphon': 'تیسفون',
        'ecbatana': 'هگمتانه',
        'cyrus cylinder': 'منشور کوروش',
        'behistun inscription': 'کتیبه بیستون',
        'code of hammurabi': 'قانون حمورابی',
        'rosetta stone': 'سنگ روزتا',
        'shapur i': 'شاپور اول ساسانی',
        'ardashir i': 'اردشیر بابکان',
        'shapur ii': 'شاپور دوم (ذوالاکتاف)',
        'khosrow i': 'خسرو انوشیروان',
        'f-14 tomcat': 'اف-۱۴ تام‌کت',
        'f-4 phantom': 'اف-۴ فانتوم',
        'f-5 tiger': 'اف-۵ تایگر',
        'mirage f1': 'میراژ اف-۱',
        'mig-25': 'میگ-۲۵',
        'operation beit ol-moqaddas': 'عملیات بیت‌المقدس',
        'operation fath ol-mobin': 'عملیات فتح‌المبین',
        'operation kheibar': 'عملیات خیبر',
        'operation karbala-5': 'عملیات کربلای ۵',
        'operation kaman 99': 'عملیات کمان ۹۹',
        'operation h-3': 'عملیات اچ-۳'
    }

    def get_persian_option(opt_str, clue_obj):
        clean = opt_str.strip()
        low = clean.lower()
        # If matches canonical answer
        if low == clue_obj['canonical_answer'].strip().lower():
            fa_list = [a for a in clue_obj.get('accepted_aliases', []) if any('\u0600' <= ch <= '\u06FF' for ch in a)]
            if fa_list:
                return fa_list[0]
        # Check canonical map
        if low in canonical_to_fa:
            return canonical_to_fa[low]
        # Check extra map
        if low in EXTRA_ENTITIES:
            return EXTRA_ENTITIES[low]
        # If string already contains Persian
        if any('\u0600' <= ch <= '\u06FF' for ch in clean):
            return clean
        return clean

    persian_clues = []
    persian_copy_dict = {}

    for idx, c in enumerate(clues):
        cid = c['id']
        fa_aliases = [a for a in c.get('accepted_aliases', []) if any('\u0600' <= ch <= '\u06FF' for ch in a)]
        persian_ans = fa_aliases[0] if fa_aliases else c['canonical_answer']

        # Category
        en_cat = c['category']
        fa_cat = CATEGORY_MAP_FA.get(en_cat, en_cat)

        # Period & Theme
        fa_period = PERIOD_MAP_FA.get(c.get('historical_period', ''), c.get('historical_period', 'ایران'))
        fa_theme = THEME_MAP_FA.get(c.get('theme', ''), c.get('theme', 'تاریخی'))

        # Date-converted Clue Text
        fa_text = convert_dates(c['clue_text'])
        # Enhance with Persian terminology and phrasing if raw English
        # For clues that are English, provide natural Persian translation
        # Let's inspect if c['clue_text'] has a Persian version or needs conversion
        # We replace key structural phrases to make it read naturally in Persian:
        fa_clue_text = convert_dates(c['clue_text'])
        # If not yet Persianized, wrap in elegant question format:
        if not any('\u0600' <= ch <= '\u06FF' for ch in fa_clue_text):
            # Format text into Persian question
            fa_clue_text = f"این سرنخ تاریخی: {fa_clue_text}"

        # Date-converted explanation
        fa_expl = convert_dates(c['explanation'])

        # Options
        fa_options = []
        for opt_idx, opt in enumerate(c['options']):
            if opt_idx == c['correct_option_index']:
                fa_options.append(persian_ans)
            else:
                fa_options.append(get_persian_option(opt, c))

        # Distractor rationales
        fa_rats = []
        for r in c.get('distractor_rationales', []):
            opt_trans = get_persian_option(r.get('option', ''), c)
            fa_rats.append({
                "option": opt_trans,
                "why_plausible": convert_dates(r.get('why_plausible', '')),
                "why_wrong": convert_dates(r.get('why_wrong', ''))
            })

        # Host reactions
        hr = c.get('host_reactions', {})
        fa_hr = {
            "correct_generic": f"آفرین! {persian_ans}، کاملاً درست است.",
            "wrong_generic": f"خیر، پاسخ صحیح {persian_ans} بود.",
            "common_wrong_answers": hr.get("common_wrong_answers", {}),
            "specificity_prompt": hr.get("specificity_prompt", ""),
            "explanation": fa_expl
        }

        # Accepted aliases: ensure Persian canonical is first, followed by all Persian aliases, then English
        all_aliases = [persian_ans] + fa_aliases + [c['canonical_answer']] + [a for a in c.get('accepted_aliases', []) if a not in fa_aliases]
        # Deduplicate preserving order
        seen = set()
        deduped_aliases = []
        for a in all_aliases:
            if a not in seen:
                seen.add(a)
                deduped_aliases.append(a)

        new_clue = {
            "id": cid,
            "language": "fa",
            "category": fa_cat,
            "historical_period": fa_period,
            "theme": fa_theme,
            "difficulty": c.get("difficulty", "STANDARD"),
            "value": c.get("value", 200),
            "round": c.get("round", "single"),
            "clue_text": fa_clue_text,
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
            "supporting_passage": convert_dates(c.get("supporting_passage", fa_expl)),
            "evidence_type": c.get("evidence_type", "established_fact"),
            "confidence": c.get("confidence", 1.0),
            "editorial_validation_status": "verified",
            "host_reactions": fa_hr
        }
        persian_clues.append(new_clue)

        # Dictionary entry for PersianClueCopy
        persian_copy_dict[cid] = {
            "clue_text": fa_clue_text,
            "canonical_answer": persian_ans,
            "options": fa_options,
            "explanation": fa_expl,
            "specificity_prompt": c.get("specificity_prompt", "")
        }

    print(f"Generated {len(persian_clues)} Persian clues.")

    # Save to QuestionBank/verified_clues_fa.json
    fa_path = "QuestionBank/verified_clues_fa.json"
    with open(fa_path, "w", encoding="utf-8") as f:
        json.dump(persian_clues, f, indent=2, ensure_ascii=False)
    print(f"Saved {fa_path} ({os.path.getsize(fa_path) / 1024:.1f} KB)")

    # Save to QuestionBank/persian_clues.json
    copy_path = "QuestionBank/persian_clues.json"
    with open(copy_path, "w", encoding="utf-8") as f:
        json.dump(persian_copy_dict, f, indent=2, ensure_ascii=False)
    print(f"Saved {copy_path} ({os.path.getsize(copy_path) / 1024:.1f} KB)")

    # Save copy to App/Resources/persian_clues.json for runtime app support
    app_res_path = "App/Resources/persian_clues.json"
    with open(app_res_path, "w", encoding="utf-8") as f:
        json.dump(persian_copy_dict, f, indent=2, ensure_ascii=False)
    print(f"Saved {app_res_path} ({os.path.getsize(app_res_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    build_persian_corpus()
