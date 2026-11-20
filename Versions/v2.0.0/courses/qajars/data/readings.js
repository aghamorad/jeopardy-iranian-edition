/* The Qajar reading list — the eighty-five items Dr Cronin's syllabus sets for
 * the eight taught weeks, one row each.
 *
 * Authored, not generated, and read off `Qajars Syllabus, 2016.docx` — the
 * module's own document, which is the only source for these rows. Unlike IR4595
 * there is no PDF corpus behind the course: the module's readings are set as
 * bibliography rather than handed out as files, so no row carries a `src`. Titles
 * and years are copied off the syllabus, never composed; a year the syllabus does
 * not print is left `null` rather than guessed, and a spelling is the syllabus's.
 *
 * One group per taught week, in seminar order, and the week names are the ones
 * `course.js` already wears on the title card — the shelf and the splash speak
 * with one voice. Two things the syllabus prints are not shelves here:
 *
 *   * **General reading** — the five surveys at the head of the document
 *     (Abrahamian, the Cambridge History volume, Katouzian, Keddie, the
 *     encyclopaedia entries). They are not a week's set reading, and every one of
 *     them is a book MAIN already shelves under its own headings, so shelving
 *     them here would print them twice on MAIN's shelf. The course's shelf is its
 *     seminars.
 *   * **A repeat.** Seven works are set for two weeks each; a row that
 *     appears twice would file twice into MAIN, so each is kept once, at the week
 *     the syllabus sets it first. Nothing is dropped — the count below is every
 *     distinct item the eight weeks set.
 *
 * Two readings were corrected against the source, and both are worth the note:
 * Keddie's *Religion and Rebellion in Iran* prints the Tobacco Protest as
 * "1891-1982", a typo for 1891–1892, and the syllabus prints Keddie's CHI
 * co-author as "Amanat, M" where the chapter is Abbas Amanat's. Everything else,
 * including "Bayat-Philip" and the undated Cronin article, is as printed.
 */
window.READINGS_QAJARS = [
  { group: { en: 'Week 1 · The Russo-Persian wars', fa: 'هفته ۱ · جنگ‌های ایران و روس' }, items: [
    { title: '“Russian Invasion into the Guarded Domain”: Reflections of a Qajar Statesman on European Expansion', author: 'Abbas Amanat', year: 1993, kind: 'article' },
    { title: 'Russia and Iran, 1780–1828', author: 'Muriel Atkin', year: 1980, kind: 'book' },
    { title: 'An Encounter with the Russian Czar: The Image of Peter the Great in Early Qajar Historical Writings', author: 'Maryam Ekhtiar', year: 1996, kind: 'article' },
    { title: 'Iranian relations with Russia and the Soviet Union to 1921', author: 'F. Kazemzadeh', year: null, kind: 'chapter' },
    { title: 'Diplomacy and murder in Tehran: Alexander Griboyedov and the Tsar’s mission to the Shah of Persia', author: 'Laurence Kelly', year: 2002, kind: 'book' },
    { title: 'Iran during the Reigns of Fath Ali Shah and Muhammad Shah', author: 'G. Hambly', year: null, kind: 'chapter' },
  ] },
  { group: { en: 'Week 2 · The ulama & authority', fa: 'هفته ۲ · علما و اقتدار' }, items: [
    { title: 'Religion and State in Iran: 1789–1906', author: 'H. Algar', year: 1969, kind: 'book' },
    { title: 'Religious Forces in Eighteenth- and Nineteenth-Century Iran', author: 'H. Algar', year: null, kind: 'chapter' },
    { title: 'The Emergence of Scientific Modernity in Iran: Controversies Surrounding Astrology and Modern Astronomy in the Mid-Nineteenth Century', author: 'Kamran Arjomand', year: 1997, kind: 'article' },
    { title: 'Ideological Revolution in Shiʿism', author: 'Said Amir Arjomand', year: 1988, kind: 'chapter' },
    { title: 'The Shadow of God and the Hidden Imam', author: 'Said Amir Arjomand', year: 1984, kind: 'book' },
    { title: 'Modern Islamic Political Thought', author: 'Hamid Enayat', year: 1982, kind: 'book' },
    { title: 'Religion and society in Qajar Iran', author: 'R. Gleave', year: 2004, kind: 'book' },
    { title: 'Shiʿism and Constitutionalism in Iran: A Study of the Role Played by the Persian Residents of Iraq in Iranian Politics', author: 'A. H. Hairi', year: 1977, kind: 'book' },
    { title: 'The Legitimacy of the early Qajar Rule as Viewed by the Shiʿi Religious Leaders', author: 'Abdul-Hadi Hairi', year: 1988, kind: 'article' },
    { title: 'Iran under the Later Qajars, 1848–1922', author: 'Nikki R. Keddie & Abbas Amanat', year: null, kind: 'chapter' },
    { title: 'Qajar Persia (Eleven Studies)', author: 'A. K. S. Lambton', year: 1987, kind: 'book' },
    { title: 'Shiʿi scholars of nineteenth-century Iraq: the ʿulamaʾ of Najaf and Karbalaʾ', author: 'Meir Litvak', year: 1998, kind: 'book' },
    { title: 'Islam and modernism: the Iranian Revolution of 1906', author: 'Vanessa Martin', year: 1989, kind: 'book' },
  ] },
  { group: { en: 'Week 3 · Army reform', fa: 'هفته ۳ · اصلاح ارتش' }, items: [
    { title: 'Importing Modernity: European Military Missions to Qajar Iran', author: 'Stephanie Cronin', year: null, kind: 'article' },
    { title: 'The Origin and Early Development of the Persian Cossack Brigade', author: 'F. Kazemzadeh', year: 1956, kind: 'article' },
    { title: 'An Evaluation of Reform and Development of the State in the Early Qajar Period', author: 'Vanessa Martin', year: 1996, kind: 'article' },
    { title: 'The origins of modern reform in Iran', author: 'G. Nashat', year: 1981, kind: 'book' },
    { title: 'The Russian Military Mission and the Birth of the Persian Cossack Brigade: 1879–1894', author: 'Uzi Rabi & Nugzar Ter-Oganov', year: 2009, kind: 'article' },
    { title: 'The structure of central authority in Qajar Iran: 1871–1896', author: 'A. Reza Sheikholeslami', year: 1997, kind: 'book' },
    { title: 'The Persian Army, 1880–1907', author: 'Reza Ra’iss Tousi', year: 1988, kind: 'article' },
    { title: 'Immortal: a military history of Iran and its armed forces', author: 'Steven R. Ward', year: 2008, kind: 'book' },
    { title: 'The Qajar Pact: Bargaining, Protest and the State in Nineteenth Century Persia', author: 'Vanessa Martin', year: 2005, kind: 'book' },
  ] },
  { group: { en: 'Week 4 · Reformist thought', fa: 'هفته ۴ · اندیشهٔ اصلاح' }, items: [
    { title: 'Mirza Malkum Khan: A Study in the History of Iranian Modernism', author: 'H. Algar', year: 1973, kind: 'book' },
    { title: 'Iran: Monarchy, Bureaucracy, and Reform under the Qajars, 1858–1896', author: 'S. Bakhash', year: 1978, kind: 'book' },
    { title: 'Marking Boundaries, Marking Time: The Iranian Past and the Construction of the Self by Qajar Thinkers', author: 'Juan R. I. Cole', year: 1996, kind: 'article' },
    { title: 'Arabic Thought in the Liberal Age', author: 'A. Hourani', year: 1983, kind: 'book' },
    { title: 'Fragile Frontiers: The Diminishing Domains of Qajar Iran', author: 'F. Kashani-Sabet', year: 1997, kind: 'article' },
    { title: 'Picturing the homeland: geography and national identity in late nineteenth- and early twentieth-century Iran', author: 'F. Kashani-Sabet', year: 1998, kind: 'article' },
    { title: 'Sayyid Jamal al-Din “al-Afghani”: A Political Biography', author: 'N. R. Keddie', year: 1972, kind: 'book' },
    { title: 'Sayyid Jamal al-Din ‘al-Afghani’', author: 'N. R. Keddie', year: 1994, kind: 'chapter' },
    { title: 'Mirza Fath Ali Akhundzade and the call for modernization of the Islamic world', author: 'Mehrdad Kia', year: 1995, kind: 'article' },
    { title: 'Pan-Islamism in Late Nineteenth-Century Iran', author: 'Mehrdad Kia', year: 1996, kind: 'article' },
    { title: 'Women, Islam and Modernity in Akhundzade’s Plays and Unpublished Writings', author: 'Mehrdad Kia', year: 1998, kind: 'article' },
    { title: 'Persian Nationalism and the Campaign for Language Purification', author: 'Mehrdad Kia', year: 1998, kind: 'article' },
    { title: 'Nationalism, Modernism and Islam in the Writings of Talibov-i Tabrizi', author: 'Mehrdad Kia', year: 1994, kind: 'article' },
    { title: 'Constitutionalism, Economic Modernization and Islam in the Writings of Mirza Yusef Khan Mostashar od-Dowle', author: 'Mehrdad Kia', year: 1994, kind: 'article' },
    { title: 'Nationalizing Iran: culture, power, and the state, 1870–1940', author: 'Afshin Marashi', year: 2008, kind: 'book' },
    { title: 'Mirza Yaʿqub Khan’s Call for Representative Government, Toleration and Islamic Reform in Nineteenth-Century Iran', author: 'Cyrus Masroori', year: 2001, kind: 'article' },
  ] },
  { group: { en: 'Week 5 · The Tobacco Protest', fa: 'هفته ۵ · نهضت تنباکو' }, items: [
    { title: 'The Persian Revolution of 1905–1909', author: 'E. G. Browne', year: 1910, kind: 'book' },
    { title: 'Religion and Rebellion in Iran: The Iranian Tobacco Protest of 1891–1892', author: 'Nikki R. Keddie', year: 1966, kind: 'book' },
    { title: 'The Tobacco Regie: Prelude to Revolution I', author: 'A. K. S. Lambton', year: 1965, kind: 'article' },
    { title: 'The Tobacco Regie: Prelude to Revolution II', author: 'A. K. S. Lambton', year: 1965, kind: 'article' },
    { title: 'Shiʿi Political Discourse and Class Mobilization in the Tobacco Movement of 1890–1892', author: 'Mansoor Moaddel', year: 1992, kind: 'article' },
  ] },
  { group: { en: 'Week 6 · The Constitutional Revolution', fa: 'هفته ۶ · انقلاب مشروطه' }, items: [
    { title: 'The Iranian constitutional revolution, 1906–1911: grassroots democracy, social-democracy and feminism', author: 'Janet Afary', year: 1996, kind: 'book' },
    { title: 'The Crowd in the Persian Revolution', author: 'Ervand Abrahamian', year: 1969, kind: 'article' },
    { title: 'The Causes of the Constitutional Revolution in Iran', author: 'Ervand Abrahamian', year: 1979, kind: 'article' },
    { title: 'The Historians of the Constitutional Movement and the Making of the Iranian Populist Tradition', author: 'R. Afshari', year: 1993, kind: 'article' },
    { title: 'The Ulama’s Traditionalist Opposition to Parliamentarianism: 1907–1909', author: 'Said Amir Arjomand', year: 1981, kind: 'article' },
    { title: 'Iran’s first revolution: Shiʿism and the constitutional revolution of 1905', author: 'Mangol Bayat', year: 1991, kind: 'book' },
    { title: 'Armenians and the Iranian constitutional revolution of 1905–1911: “the love for freedom has no fatherland”', author: 'Houri Berberian', year: 2001, kind: 'book' },
    { title: 'The Russo-Caucasian origins of the Iranian left: social democracy in modern Iran', author: 'Cosroe Chaqueri', year: 2000, kind: 'book' },
    { title: 'Iran’s constitutional revolution: popular politics, cultural transformations and transnational connections', author: 'H. E. Chehabi & Vanessa Martin', year: 2010, kind: 'book' },
    { title: 'Religion, Culture and Politics in Iran', author: 'Joanna De Groot', year: 2007, kind: 'book' },
    { title: 'Shiʿism and Popular Leadership in the Iranian Constitutional Revolution, 1906–1911: the Case of Muhammad Kazim Khurasani', author: 'Mateo Mohammad Farzaneh', year: 2015, kind: 'book' },
    { title: 'The Opening Up of Qajar Iran: Some Economic and Social Aspects', author: 'Gad Gilbar', year: 1986, kind: 'article' },
    { title: 'The Persian Constitutional Revolution of 1905–06', author: 'A. K. S. Lambton', year: 1987, kind: 'chapter' },
    { title: 'Iran Between Islamic Nationalism and Secularism: The Constitutional Revolution of 1906', author: 'Vanessa Martin', year: 2013, kind: 'book' },
    { title: 'The anti-constitutionalist arguments of Shaikh Fazlallah Nuri', author: 'Vanessa Martin', year: 1986, kind: 'article' },
    { title: 'Autocracy, Modernization, and Revolution in Russia and Iran', author: 'Tim McDaniel', year: 1991, kind: 'book' },
    { title: 'The story of the daughters of Quchan: gender and national memory in Iranian history', author: 'Afsaneh Najmabadi', year: 1998, kind: 'book' },
    { title: 'The Strangling of Persia', author: 'Morgan W. Shuster', year: 1968, kind: 'book' },
  ] },
  { group: { en: 'Week 7 · Britain, Russia & the Great Game', fa: 'هفته ۷ · انگلیس، روسیه و بازی بزرگ' }, items: [
    { title: 'Britain and the Iranian constitutional revolution of 1906–1911: foreign policy, imperialism, and dissent', author: 'Mansour Bonakdarian', year: 2006, kind: 'book' },
    { title: 'British policy on railways in Persia, 1870–1900', author: 'John S. Galbraith', year: 1989, kind: 'article' },
    { title: 'British Policy and the Iranian Opposition 1901–1907', author: 'Nikki R. Keddie', year: 1967, kind: 'article' },
    { title: 'Hartwig and Russian policy in Iran 1906–8', author: 'Vanessa Martin', year: 1993, kind: 'article' },
    { title: 'Britain and Southwest Persia, 1880–1914: a study in imperialism and economic dependence', author: 'Shahbaz Shahnavaz', year: 2003, kind: 'book' },
    { title: 'Endgame: Britain, Russia and the final struggle for Central Asia', author: 'Jennifer Siegel', year: 2002, kind: 'book' },
  ] },
  { group: { en: 'Week 8 · Women in political life', fa: 'هفته ۸ · زنان در زندگی سیاسی' }, items: [
    { title: 'Sexual Politics in Modern Iran', author: 'Janet Afary', year: 2009, kind: 'book' },
    { title: 'On the origins of feminism in early 20th-century Iran', author: 'Janet Afary', year: null, kind: 'article' },
    { title: 'Resurrection and renewal: the making of the Babi Movement in Iran, 1844–1850', author: 'Abbas Amanat', year: 1989, kind: 'book' },
    { title: 'Pivot of the Universe: Nasir al-Din Shah Qajar and the Iranian Monarchy, 1831–1896', author: 'Abbas Amanat', year: 1997, kind: 'book' },
    { title: 'Women and revolution in Iran, 1905–1911', author: 'M. Bayat-Philip', year: 1978, kind: 'chapter' },
    { title: 'Inside the Court of Naser od-Din Shah Qajar, 1881–96: The Life and Diary of Mohammad Hasan Khan E’temad os-Saltaneh', author: 'Mehrdad Kia', year: 2001, kind: 'article' },
    { title: 'Women with mustaches and men without beards: gender and sexual anxieties of Iranian modernity', author: 'Afsaneh Najmabadi', year: 2005, kind: 'book' },
    { title: 'Women in Iran from 1800 to the Islamic Republic', author: 'G. Nashat & L. Beck (eds.)', year: 2004, kind: 'book' },
    { title: 'The women’s rights movement in Iran: mutiny, appeasement, and repression from 1900 to Khomeini', author: 'Eliz Sanasarian', year: 1982, kind: 'book' },
    { title: 'Women and the Political Process in Twentieth-century Iran', author: 'Parvin Paidar', year: 1995, kind: 'book' },
    { title: 'Crowning anguish: memoirs of a Persian princess from the harem to modernity 1884–1914', author: 'Tāj al-Saltanah', year: 1993, kind: 'primary source' },
    { title: 'Women of the West Imagined: The Farangi Other and the Emergence of the Women Question in Iran', author: 'Mohamad Tavakoli-Targhi', year: 1994, kind: 'chapter' },
  ] },
];
