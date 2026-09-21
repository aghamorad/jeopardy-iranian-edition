/* The Pahlavi reading list — the hundred and twenty-three items Dr Cronin's
 * syllabus sets for the eight taught weeks, one row each.
 *
 * Authored, not generated, and read off `Pahlavis Syllabus, 2016.docx` — the
 * module's own document, which is the only source for these rows. Unlike IR4595
 * there is no PDF corpus behind the course: the module's readings are set as
 * bibliography rather than handed out as files, so no row carries a `src`. Titles
 * and years are copied off the syllabus, never composed; a year the syllabus does
 * not print is left `null` rather than guessed, and a spelling is the syllabus's,
 * from "Bayat-Philip" to the encyclopaedia's transliterations.
 *
 * One group per taught week, in seminar order, and the week names are the ones
 * `course.js` wears on the title card — the shelf and the splash speak with one
 * voice. Two things the syllabus prints are not rows here:
 *
 *   * **General reading** — the sixteen surveys at the head of the document
 *     (Abrahamian twice, Katouzian, Afary, Ansari, Avery/Hambly/Melville, Azimi,
 *     Daniel, Foran twice, Gheissari, Gheissari and Nasr, Halliday, Mottahedeh,
 *     Ridgeon, and the encyclopaedia entries). They are not a week's set reading,
 *     and every one of them is a book MAIN already shelves under its own
 *     headings, so shelving them here would print them twice on MAIN's shelf. The
 *     course's shelf is its seminars.
 *   * **A repeat.** Ten works recur across the eight weeks; a row that appears
 *     twice would file twice into MAIN, so each is kept once, at the week the
 *     syllabus sets it first. Nothing is silently dropped — the count above is
 *     every distinct item the eight weeks set.
 *
 * The syllabus leans on the "same author again" convention, naming an author once
 * and printing further works under no name at all. Three of those continuations
 * are resolved to the name above them: Bast's two other chapters in week one,
 * Eshraqi's second article in week three (the syllabus marks the pair 1984a and
 * 1984b), and O'Sullivan's companion volume in the same week. Week four's account
 * of the 1953 coup is shelved as its two citable pieces — Wilber's "CLANDESTINE
 * SERVICE HISTORY" and the New York Times feature that carried it — and the three
 * web addresses under them are links, not rows.
 */
window.READINGS_PAHLAVIS = [
  { group: { en: 'Week 1 · The 1921 coup', fa: 'هفته ۱ · کودتای ۱۲۹۹' }, items: [
    { title: 'Duping the British and outwitting the Russians? Iran’s foreign policy, the ‘Bolshevik threat’, and the genesis of the Soviet-Iranian Treaty of 1921', author: 'Oliver Bast', year: 2013, kind: 'chapter' },
    { title: 'The Council for International Propaganda and the Establishment of the Iranian Communist Party', author: 'Oliver Bast', year: 2006, kind: 'chapter' },
    { title: 'Putting the Record Straight: Vosuq al-Dowleh’s Foreign Policy in 1918/19', author: 'Oliver Bast', year: 2004, kind: 'chapter' },
    { title: 'The Soviet Socialist Republic of Iran, 1920-1921: birth of the trauma', author: 'Cosroe Chaqueri', year: 1995, kind: 'book' },
    { title: 'Britain, the Iranian Military and the Rise of Reza Khan', author: 'Stephanie Cronin', year: 2005, kind: 'chapter' },
    { title: 'Iran and the Rise of Reza Shah: from Qajar Collapse to Pahlavi Rule', author: 'Cyrus Ghani', year: 1998, kind: 'book' },
    { title: 'State and Society in Iran: The Eclipse of the Qajars and the Emergence of the Pahlavi dynasty', author: 'Homa Katouzian', year: 2000, kind: 'book' },
    { title: 'Some aspects of Anglo-Iranian relations, 1914-1919: a study in Great Power politics in regional affairs', author: 'William J. Olson', year: 1980, kind: 'book' },
    { title: 'British Policy in Persia 1918-1925', author: 'Houshang Sabahi', year: 1990, kind: 'book' },
  ] },
  { group: { en: 'Week 2 · Reza Shah: reformer or despot', fa: 'هفته ۲ · رضاشاه: مصلح یا مستبد' }, items: [
    { title: 'The Making of Modern Iran: State and Society under Riza Shah, 1921-41', author: 'Stephanie Cronin', year: 2003, kind: 'book' },
    { title: 'The making of the modern Iranian woman: gender, state policy, and popular culture, 1865-1946', author: 'Camron Michael Amin', year: 2002, kind: 'book' },
    { title: 'Men of order: authoritarian modernization under Atatürk and Reza Shah', author: 'Touraj Atabaki', year: 2003, kind: 'book' },
    { title: 'The state and the subaltern: modernization, society and the state in Turkey and Iran', author: 'Touraj Atabaki', year: 2007, kind: 'book' },
    { title: 'The Growth of Towns and Villages in Iran 1900-66', author: 'J. Bharier', year: 1972, kind: 'article' },
    { title: 'Staging the emperor’s new clothes: dress codes and nation-building under Reza Shah', author: 'Houchang Chehabi', year: 1993, kind: 'article' },
    { title: 'Knitting Iran together: The Land Transport Revolution, 1920-1940', author: 'Patrick Clawson', year: 1993, kind: 'article' },
    { title: 'The Army and the creation of the Pahlavi state in Iran, 1921-1926', author: 'Stephanie Cronin', year: 1997, kind: 'book' },
    { title: 'Reformers and revolutionaries in modern Iran: new perspectives on the Iranian left', author: 'Stephanie Cronin', year: 2004, kind: 'book' },
    { title: 'Tribal politics in Iran: rural conflict and the new state, 1921-1941', author: 'Stephanie Cronin', year: 2006, kind: 'book' },
    { title: 'Shahs, Soldiers and Subalterns: Opposition, Protest and Revolt, 1921-1941', author: 'Stephanie Cronin', year: 2010, kind: 'book' },
    { title: 'Culture and cultural politics under Reza Shah: the Pahlavi state, new bourgeoisie and the creation of a modern society in Iran', author: 'Bianca Devos & Christoph Werner', year: 2013, kind: 'book' },
    { title: 'The Ulama-State relations in Iran: 1921-1941', author: 'Mohammad H. Faghfoory', year: 1987, kind: 'article' },
    { title: 'The Impact of Modernization on the Ulama in Iran, 1925-1941', author: 'Mohammad H. Faghfoory', year: 1993, kind: 'article' },
    { title: 'Iranian Intellectuals in the 20th Century', author: 'Ali Gheissari', year: 1998, kind: 'book' },
    { title: 'The Iranian Communist Party under Reza Shah', author: 'Mohammad Reza Ghods', year: 1990, kind: 'article' },
    { title: 'Iranian Nationalism and Reza Shah', author: 'Mohammad Reza Ghods', year: 1991, kind: 'article' },
    { title: 'The Pahlavi Autocracy: Riza Shah, 1921-1941', author: 'Gavin Hambly', year: 1991, kind: 'chapter' },
    { title: 'The Pahlavi Regime in Iran', author: 'Homa Katouzian', year: 1998, kind: 'chapter' },
    { title: 'Qajar Iran and the rise of Reza Khan, 1796-1925', author: 'Nikki Keddie', year: 1999, kind: 'book' },
    { title: 'Turban or Hat, Seminarian or Soldier: State Building and Clergy Building in Reza Shah’s Iran', author: 'Arang Keshavarzian', year: 2003, kind: 'article' },
    { title: 'Persian Nationalism and the campaign for language purification', author: 'Mehrdad Kia', year: 1998, kind: 'article' },
    { title: 'Education and the Making of Modern Iran', author: 'David Menashri', year: 1992, kind: 'book' },
    { title: 'Women and the Political Process in Twentieth-century Iran', author: 'Parvin Paidar', year: 1995, kind: 'book' },
    { title: 'Reza Shah’s Court Minister: Teymourtash', author: 'Miron Rezun', year: 1980, kind: 'article' },
    { title: 'Who is Knowledgeable is Strong: Science, Class, and the Formation of Modern Iranian Society, 1900-1950', author: 'Cyrus Schayegh', year: null, kind: 'book' },
    { title: 'Imperial power and dictatorship: Britain and the rise of Reza Shah', author: 'Michael P. Zirinsky', year: 1992, kind: 'article' },
  ] },
  { group: { en: 'Week 3 · The Allied occupation', fa: 'هفته ۳ · اشغال ایران' }, items: [
    { title: 'Under Five Shahs', author: 'Hassan Arfa', year: 1964, kind: 'book' },
    { title: 'Iran: The Crisis of Democracy 1941-53', author: 'F. Azimi', year: 1989, kind: 'book' },
    { title: 'Letters from Tehran', author: 'Reader Bullard', year: 1991, kind: 'book' },
    { title: 'Oil, the Cold War, and the Crisis in Azerbaijan of March 1946', author: 'James Clark', year: 2004, kind: 'article' },
    { title: 'Anglo-Soviet Occupation of Iran in 1941', author: 'F. Eshraqi', year: 1984, kind: 'article' },
    { title: 'The Immediate Aftermath of Anglo-Soviet Occupation of Iran in August 1941', author: 'F. Eshraqi', year: 1984, kind: 'article' },
    { title: 'Iran and the Cold War: The Azarbaijan Crisis of 1946', author: 'Louise Fawcett L’Estrange', year: 1992, kind: 'book' },
    { title: 'Revisiting the Iranian Crisis of 1946: How Much More Do We Know?', author: 'Louise Fawcett', year: 2014, kind: 'article' },
    { title: 'At the dawn of the Cold War: the Soviet-American crisis over Iranian Azerbaijan, 1941-1946', author: 'Jămil Ḣăsănov', year: 2006, kind: 'book' },
    { title: 'Anatomy of an Iranian Political Crowd: The Tehran Bread Riot of December 1942', author: 'Stephen L. McFarland', year: 1985, kind: 'article' },
    { title: 'Espionage and counterintelligence in occupied Persia (Iran): the success of the Allied secret services, 1941-45', author: 'Adrian O’Sullivan', year: 2015, kind: 'book' },
    { title: 'Nazi secret warfare in occupied Persia (Iran): the failure of the German intelligence services, 1939-45', author: 'Adrian O’Sullivan', year: 2014, kind: 'book' },
  ] },
  { group: { en: 'Week 4 · Musaddiq and the oil', fa: 'هفته ۴ · مصدق و نفت' }, items: [
    { title: 'Musaddiq, Iranian Nationalism & Oil', author: 'J.A. Bill & Roger Wm. Louis', year: 1988, kind: 'book' },
    { title: 'Mohammad Mosaddeq and the 1953 coup in Iran', author: 'Mark J. Gasiorowski & Malcoom Byrne', year: 2004, kind: 'book' },
    { title: 'Tudeh Factionalism and the 1953 Coup in Iran', author: 'Maziar Behrooz', year: 2001, kind: 'article' },
    { title: 'The Cairo-Tehran connection in Anglo-American rivalry in the Middle East, 1951-1953', author: 'H. W. Brands', year: 1989, kind: 'article' },
    { title: 'Iran’s Economic Policy during the Mosaddeq Era', author: 'Kamran Dadkhah', year: 2000, kind: 'article' },
    { title: 'The Oil Nationalization Movement, the british Boycott, and the Iranian Economy, 1950-1953', author: 'Kamran Dadkhah', year: 1988, kind: 'chapter' },
    { title: 'Dr. Mohammad Mossadegh; A Political Biography', author: 'Farhad Diba', year: 1986, kind: 'book' },
    { title: 'Oil, power, and principle: Iran’s oil nationalization and its aftermath', author: 'Mostafa Elm', year: 1992, kind: 'book' },
    { title: 'The Mussadiq era in Iran, 1951-1953: a contemporary diplomat’s view', author: 'Sir S. Falle', year: 1996, kind: 'chapter' },
    { title: 'Blood and oil: memoirs of a Persian prince', author: 'Manucher Farmanfarmaian', year: 1997, kind: 'book' },
    { title: 'The 1953 Coup d’état in Iran', author: 'Mark J. Gasiorowski', year: 1987, kind: 'article' },
    { title: 'U.S. foreign policy toward Iran during the Mussadiq era', author: 'Mark J. Gasiorowski', year: 1996, kind: 'chapter' },
    { title: 'Politics, Power, and U.S. Policy in Iran, 1950-1953', author: 'Francis J. Gavin', year: 1999, kind: 'article' },
    { title: 'Musaddiq and the struggle for power in Iran', author: 'Homa Katouzian', year: 1990, kind: 'book' },
    { title: 'Musaddiq’s Memoirs', author: 'Homa Katouzian', year: 1988, kind: 'book' },
    { title: 'All The Shah’s Men: An American Coup and the Roots of Middle East Terror', author: 'Stephen Kinzer', year: 2003, kind: 'book' },
    { title: 'Voice of America and Iran, 1949-1953: U.S. liberal developmentalism, propaganda and the Cold War', author: 'Deborah Kisatsky', year: 1999, kind: 'article' },
    { title: 'US Policy in the Near East: The Triumphs and Tribulations of the Truman Administration', author: 'Bruce R. Kuniholm', year: 1989, kind: 'chapter' },
    { title: 'The 1951-53 Oil nationalization dispute and the Iranian economy: a rejoinder', author: 'M.G. Majd', year: 1995, kind: 'article' },
    { title: 'The United States, Iran and Operation ‘Ajax’: Inverting Interpretative Orthodoxy', author: 'Steve Marsh', year: 2003, kind: 'article' },
    { title: 'State-centred vs. class-centred perspectives on international politics: the case of U.S. and British participation in the 1953 coup against Premier Mosaddeq in Iran', author: 'Mansour Moaddel', year: 1989, kind: 'article' },
    { title: 'Paved with good intentions: the American experience and Iran', author: 'Barry Rubin', year: 1981, kind: 'book' },
    { title: 'Operation ‘AJAX’ revisted: Iran 1953', author: 'Moiara de Moraes Ruehsen', year: 1993, kind: 'article' },
    { title: 'Iranian perceptions of the United States and the Mussadiq period', author: 'Sussan Siavoshi', year: 1996, kind: 'chapter' },
    { title: 'The Mossadegh era: roots of the Iranian revolution', author: 'Sepehr Zabih', year: 1982, kind: 'book' },
    { title: 'CLANDESTINE SERVICE HISTORY, OVERTHROW OF PREMIER MOSSADEQ OF IRAN, November 1952-August 1953', author: 'Donald Wilber', year: 1954, kind: 'article' },
    { title: 'New York Times special feature on the CIA’s secret history of the 1953 coup in Iran', author: 'The New York Times', year: 2000, kind: 'article' },
  ] },
  { group: { en: 'Week 5 · Muhammad Reza Shah', fa: 'هفته ۵ · محمدرضاشاه' }, items: [
    { title: 'The Oppositional Role of the Ulama in Twentieth Century Iran', author: 'Hamid Algar', year: 1972, kind: 'chapter' },
    { title: 'The Eagle and the Lion: America and Iran', author: 'James Bill', year: 1988, kind: 'book' },
    { title: 'The Revolutionary Character of the Iranian Ulama: Wishful Thinking or Reality?', author: 'Willem m. Floor', year: 1980, kind: 'article' },
    { title: 'Iran: Dictatorship and Development', author: 'Fred Halliday', year: 1979, kind: 'book' },
    { title: 'The Pahlavi Autocracy: Muhammad Riza Shah, 1941-79', author: 'Gavin Hambly', year: 1991, kind: 'chapter' },
    { title: 'Land and Revolution in Iran, 1960-1980', author: 'Eric Hoogland', year: 1982, kind: 'book' },
    { title: 'Oil, state and industrialization in Iran', author: 'Massoud Karshenas', year: 1990, kind: 'book' },
    { title: 'Bazaar and State in Iran: The Politics of the Tehran Marketplace', author: 'Arang Kesharvarzian', year: 2007, kind: 'book' },
    { title: 'Mission for my Country', author: 'Mohammed Reza Pahlavi', year: 1961, kind: 'book' },
    { title: 'The White Revolution', author: 'Mohammed Reza Pahlavi', year: 1967, kind: 'book' },
    { title: 'Land Reform and Social Change in Rural Iran', author: 'Afsaneh Najmabadi', year: 1988, kind: 'book' },
    { title: 'For a White Revolution: John F. Kennedy and the Shah of Iran', author: 'April R. Summit', year: 2004, kind: 'article' },
  ] },
  { group: { en: 'Week 6 · The Left in Iran', fa: 'هفته ۶ · چپ در ایران' }, items: [
    { title: 'Tortured confessions: prisons and public recantations in modern Iran', author: 'Ervand Abrahamian', year: 1999, kind: 'book' },
    { title: 'The Iranian constitutional revolution, 1906-1911: grassroots democracy, social-democracy and feminism', author: 'Janet Afary', year: 1996, kind: 'book' },
    { title: 'Rebels with a Cause: The Failure of the Left in Iran', author: 'Maziar Behrooz', year: 1999, kind: 'book' },
    { title: 'The Condition of the working class in Iran (a documentary history)', author: 'Cosroe Chaqueri', year: 1978, kind: 'book' },
    { title: 'The Russo-Caucasian origins of the Iranian left: social democracy in modern Iran', author: 'Cosroe Chaqueri', year: 2000, kind: 'book' },
    { title: 'The Left and Revolution in Iran: A Critical Analysis', author: 'V. Moghadam', year: 1988, kind: 'chapter' },
    { title: 'The Communist Movement in Iran', author: 'Sepehr Zabih', year: 1966, kind: 'book' },
  ] },
  { group: { en: 'Week 7 · Gender and modernity', fa: 'هفته ۷ · جنسیت و تجدد' }, items: [
    { title: 'Sexual Politics in Modern Iran', author: 'Janet Afary', year: 2009, kind: 'book' },
    { title: 'On the origins of feminism in early 20th-century Iran', author: 'Janet Afary', year: null, kind: 'article' },
    { title: 'Women and revolution in Iran, 1905-1911', author: 'M. Bayat-Philip', year: 1978, kind: 'chapter' },
    { title: 'Women in the Muslim world', author: 'Lois Beck & Nikki Keddie', year: 1978, kind: 'book' },
    { title: 'Daughter of Persia: a woman’s journey from her father’s harem through the Islamic Revolution', author: 'Sattareh Farman Farmaian with Dona Munker', year: 1992, kind: 'book' },
    { title: 'Law of desire: temporary marriage in Shi’i Iran', author: 'Shahla Haeri', year: 1989, kind: 'book' },
    { title: 'The Politics of Reproduction: Maternalism and Women’s Hygiene in Iran, 1896-1941', author: 'Firoozeh Kashani-Sabet', year: 2006, kind: 'article' },
    { title: 'Patriotic Womanhood: The Culture of Feminism in Modern Iran, 1900-1941', author: 'Firoozeh Kashani-Sabet', year: 2005, kind: 'article' },
    { title: 'Women, religion and culture in Iran', author: 'V. Martin & S. Ansari', year: 2002, kind: 'book' },
    { title: 'Women and Popular Protest: Women’s Demonstrations in Nineteenth-century Iran', author: 'V. Martin', year: 2010, kind: 'chapter' },
    { title: 'The story of the daughters of Quchan: gender and national memory in Iranian history', author: 'Afsaneh Najmabadi', year: 1998, kind: 'book' },
    { title: 'Women with mustaches and men without beards: gender and sexual anxieties of Iranian modernity', author: 'Afsaneh Najmabadi', year: 2005, kind: 'book' },
    { title: 'Women in Iran from 1800 to the Islamic Republic', author: 'G. Nashat & L. Beck', year: 2004, kind: 'book' },
    { title: 'The women’s rights movement in Iran: mutiny, appeasement, and repression from 1900 to Khomeini', author: 'Eliz Sanasarian', year: 1982, kind: 'book' },
    { title: 'Women and Politics in Iran: veiling, unveiling and reveiling', author: 'Hamideh Sedghi', year: 2007, kind: 'book' },
    { title: 'The Iranian Left and ‘the woman question’ in the Revolution of 1978-1979', author: 'Hammed Shahidian', year: 1994, kind: 'article' },
    { title: 'Crowning anguish: memoirs of a Persian princess from the harem to modernity 1884-1914', author: 'Tāj al-Salṭanah', year: 1993, kind: 'book' },
    { title: 'Women of the West Imagined: The Farangi Other and the Emergence of the Women Question in Iran', author: 'Mohamad Tavakoli-Targhi', year: 1994, kind: 'chapter' },
    { title: 'From Patriotism to Matriotism: A Tropological Study of Iranian Nationalism, 1870-1909', author: 'Mohamad Tavakoli-Targhi', year: 2002, kind: 'article' },
  ] },
  { group: { en: 'Week 8 · Iran and the world', fa: 'هفته ۸ · ایران و جهان' }, items: [
    { title: 'Nixon, Kissinger, and the Shah: The United States and Iran in the Cold War', author: 'Roham Alvandi', year: 2014, kind: 'book' },
    { title: 'The Foreign Relations of Iran: a Developing State in a Zone of Great-Power Competition', author: 'Shahram Chubin', year: 1974, kind: 'book' },
    { title: 'Iran Between the Arab West and the Asian East', author: 'Shahram Chubin', year: 1974, kind: 'article' },
    { title: 'US Foreign Policy and the Shah: Building a Client State in Iran', author: 'Mark J. Gasiorowski', year: 1991, kind: 'book' },
    { title: 'Anglo-Iranian relations since 1800', author: 'V. Martin', year: 2005, kind: 'book' },
    { title: 'Iran’s Foreign Policy 1500-1941: A Developing Nation in World Affairs', author: 'Rouhollah K. Ramazani', year: 1966, kind: 'book' },
    { title: 'Iran’s Foreign Policy 1941-73: A Study of Foreign Policy in Modernizing Nations', author: 'Rouhollah K. Ramazani', year: 1975, kind: 'book' },
    { title: 'The Northern Tier: Afghanistan, Iran and Turkey', author: 'Rouhollah K. Ramazani', year: 1966, kind: 'book' },
    { title: 'The Persian Gulf: Iran’s Role', author: 'Rouhollah K. Ramazani', year: 1972, kind: 'book' },
    { title: 'Iran’ Foreign Policy, 1921-79', author: 'Amin Saikal', year: 1991, kind: 'chapter' },
  ] },
];
