/* JEOPARDY! — Iranian Edition, language layer.

   Two languages, one show. This file holds every string the player reads and
   the plumbing that swaps them: `T(key)` for JS-built copy, `data-i18n*`
   attributes for anything already in the markup, and `setLang()` which is the
   only thing that turns the room over.

   The host's register is the same in both languages — smug, snarky, mean. The
   Persian is not a translation of the English so much as the same joke told by
   the same man in the language he'd actually tell it in.

   The voiceovers stay English. Morad's call: re-recording her is a bigger job
   than this round, and the host's line files are keyed by name, not by text. */

(function () {
  'use strict';

  var STRINGS = {
    en: {
      'doc.title': 'JEOPARDY! — Iranian Edition',

      /* The language gate */
      'lang.choose': 'Choose your language',
      'lang.en': 'English',
      'lang.fa': 'فارسی',
      'lang.beta': 'Persian is in beta',

      /* Title card */
      'splash.tagline': 'Because you fuckers don’t know your history<br>and it’s time you learn a goddamn thing or two',
      'splash.rail.left.0': 'People',
      'splash.rail.left.1': 'Places',
      'splash.rail.left.2': 'Empires',
      'splash.rail.left.3': 'Culture',
      'splash.rail.left.4': 'Revolutions',
      'splash.rail.right.0': 'Kings',
      'splash.rail.right.1': 'Poets',
      'splash.rail.right.2': 'Wars',
      'splash.rail.right.3': 'Oil',
      'splash.rail.right.4': 'And more…',

      /* The cold open. She talks, the aperture below her label opens with her. */
      'splash.mouth.who': 'Your host',
      'splash.mouth.hint': 'Press anywhere to continue',

      /* Lobby */
      'common.corner.egos': 'Same game.<br>Bigger egos.',
      'common.corner.hard': 'Hard questions.<br>Unjustified confidence.',
      'common.corner.place': 'Tehran<br>35.6892° N, 51.3890° E',
      'lobby.tagline': 'A country full of experts.<br>Let’s see what you actually know, you sons of bitches.',
      'lobby.rail.0': 'People, from geniuses to assholes',
      'lobby.rail.1': 'Places you swear you know',
      'lobby.rail.2': 'Empires that fucked it up',
      'lobby.rail.3': 'Culture, customs &amp; bullshit',
      'lobby.rail.4': 'Revolutions &amp; bad decisions',
      'lobby.rail.5': 'Art, from genius to “what the fuck?”',
      'lobby.rail.6': 'Science, so stop guessing',
      'lobby.rail.7': 'Sports, for the stat freaks',
      'lobby.rail.8': 'And plenty more you’re weirdly confident about…',
      'lobby.start': 'Start game',
      'lobby.settings': 'Settings',
      'lobby.howto': 'How to play',
      'lobby.quit': 'Quit',

      /* The Green Room */
      'setup.eyebrow': 'The Green Room',
      'setup.tagline': 'Who’s taking the stage tonight?',
      'setup.rail.0': 'Contestants',
      'setup.rail.1': 'Categories',
      'setup.rail.2': 'Buzzers',
      'setup.rail.3': 'Wagers',
      'setup.rail.4': 'Final',
      'setup.contestants': 'Contestants',
      'setup.names': 'Names',
      'setup.sound': 'Sound',
      'setup.on': 'On',
      'setup.off': 'Off',
      'setup.start': 'Take the stage',
      'setup.back': 'Back',
      'setup.nameAria': 'Contestant {n} name',
      'setup.playerDefault': 'PLAYER {n}',

      /* Opponents and how you answer */
      'setup.opponents': 'Opponents',
      'setup.opponents.human': 'Humans',
      'setup.opponents.mixed': 'Mixed',
      'setup.opponents.bots': 'Robots',
      'setup.difficulty': 'Robot difficulty',
      'setup.answerMode': 'Answering',
      'setup.answerMode.mc': 'Multiple choice',
      'setup.answerMode.write': 'Write-in',

      /* The robots */
      'bot.easy': 'Cable Access',
      'bot.normal': 'Nostalgia',
      'bot.hard': 'Your Uncle',
      'bot.brutal': 'The Archive',
      'bot.easy.desc': 'Believes everything it saw on Instagram.',
      'bot.normal.desc': 'Convinced the nineties were better.',
      'bot.hard.desc': 'Knows one enormous fact and will not be moved.',
      'bot.brutal.desc': 'Has read all forty-nine books. Twice.',

      /* Board */
      'board.menu': 'Menu',
      'board.rail.0': 'Knowledge',
      'board.rail.1': 'Culture',
      'board.rail.2': 'Bad takes',
      'board.rail.3': 'Unjustified confidence',
      'board.rail.4': 'Arguments, obviously.',
      'round.single.kicker': 'Round One',
      'round.single.title': 'Jeopardy!',
      'round.double.kicker': 'Round Two',
      'round.double.title': 'Double Jeopardy',
      'round.final.kicker': 'The Final Round',
      'round.final.title': 'Final Jeopardy',

      /* Clue */
      'clue.buzz': 'Buzz',
      'clue.buzzLocked': 'Locked out',
      'clue.answering': 'Answering',
      'clue.nobody': 'Nobody in?',
      'clue.nobodyBody': 'The clue is still on the board.',
      'clue.writePlaceholder': 'Type your answer',
      'clue.submit': 'Lock it in',
      'clue.correct': 'Correct',
      'clue.incorrect': 'Incorrect',
      'clue.outOfTime': 'Out of time',
      'clue.theAnswer': 'The answer',
      'clue.nearMiss': 'Close enough',

      /* Wager */
      'wager.prompt': 'Wager before you see the clue.',
      'wager.dailyDouble': 'Daily Double',
      'wager.final': 'Final Jeopardy',
      'wager.youHave': 'You have',
      'wager.max': 'Max',
      'wager.all': 'All in',
      'wager.half': 'Half',
      'wager.quarter': 'A quarter',
      'wager.threeQuarters': 'Three quarters',
      'wager.lock': 'Lock it in',
      'wager.waiting': '{name} is wagering…',

      /* Results */
      'results.title': 'Final Score',
      'results.tie': 'A Tie',
      'results.winner': '{name} wins',
      'results.playAgain': 'Play again',

      /* Match menu */
      'menu.eyebrow': 'Match menu',
      'menu.resume': 'Continue playing',
      'menu.restart': 'New match',
      'menu.lobby': 'Quit to lobby',

      /* Settings */
      'settings.eyebrow': 'Settings',
      'settings.sound': 'Music &amp; sound',
      'settings.keyboard': 'Keyboard',
      'settings.keyboardBody': 'Buzz with <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd>, answer with <kbd>A</kbd>–<kbd>D</kbd>. Arrow keys and <kbd>Return</kbd> move through the board.',
      'settings.keyboardBodyWrite': 'Buzz with <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd>, then type the answer and press <kbd>Return</kbd>. Arrow keys and <kbd>Return</kbd> move through the board when no clue is open.',
      'settings.controllers': 'Controllers',
      'settings.controllersBody': 'Plug in one controller per contestant — the first is Player 1, the second Player 2, and so on, and each one only buzzes for its own player. Every controller also drives the menus and the board: the d-pad or left stick moves, <kbd class="glyph">A</kbd> chooses, <kbd class="glyph">B</kbd> goes back, and <kbd class="glyph pill">Start</kbd> opens the match menu.',
      'settings.close': 'Close',

      /* How to play */
      'howto.eyebrow': 'How to play',
      'howto.body1': 'Pick a tile from the board to open a clue. When the clue appears, everyone races to hit their own <em>Buzz</em> button — first one in gets the floor and chooses an answer. Right answers add the clue’s value; wrong ones subtract it and hand the clue to everyone else.',
      'howto.body2': 'One tile a round is a Daily Double and gets answered alone, with nobody to bail you out. The match closes with Final Jeopardy: you wager before you see the clue. Spend it well.'
    },

    fa: {
      'doc.title': 'جپاردی! — نسخهٔ ایرانی',

      'lang.choose': 'زبانت را انتخاب کن',
      'lang.en': 'English',
      'lang.fa': 'فارسی',
      'lang.beta': 'نسخهٔ فارسی آزمایشی است',

      'splash.tagline': 'چون هیچ‌کدام‌تان تاریخ خودتان را نمی‌دانید<br>و وقتش رسیده دست‌کم یک چیزی یاد بگیرید',
      'splash.rail.left.0': 'آدم‌ها',
      'splash.rail.left.1': 'جاها',
      'splash.rail.left.2': 'امپراتوری‌ها',
      'splash.rail.left.3': 'فرهنگ',
      'splash.rail.left.4': 'انقلاب‌ها',
      'splash.rail.right.0': 'شاه‌ها',
      'splash.rail.right.1': 'شاعران',
      'splash.rail.right.2': 'جنگ‌ها',
      'splash.rail.right.3': 'نفت',
      'splash.rail.right.4': 'و بیشتر…',

      /* The cold open. She talks, the aperture below her label opens with her. */
      'splash.mouth.who': 'میزبان شما',
      'splash.mouth.hint': 'برای ادامه، هر جا را بزنید',

      'common.corner.egos': 'همان بازی.<br>خودپسندیِ بیشتر.',
      'common.corner.hard': 'سؤال‌های سخت.<br>اعتمادبه‌نفس بی‌مورد.',
      'common.corner.place': 'تهران<br><span class="lat">35.6892° N, 51.3890° E</span>',
      'lobby.tagline': 'یک مملکت پر از کارشناس.<br>حالا ببینیم واقعاً چی بلدید، ای آشغال‌ها.',
      'lobby.rail.0': 'آدم‌ها، از نابغه تا مفت‌خور',
      'lobby.rail.1': 'جاهایی که فکر می‌کنی بلدی',
      'lobby.rail.2': 'امپراتوری‌هایی که گند زدند',
      'lobby.rail.3': 'فرهنگ، رسم و رسوم و ادا و اطوار',
      'lobby.rail.4': 'انقلاب‌ها و تصمیم‌های فاجعه‌بار',
      'lobby.rail.5': 'هنر، از شاهکار تا «این دیگه چیه؟»',
      'lobby.rail.6': 'علم، وقتی حدس جواب نمی‌دهد',
      'lobby.rail.7': 'ورزش، برای آماربازها',
      'lobby.rail.8': 'و کلی چیز دیگر که زیادی درباره‌شان مطمئنی…',
      'lobby.start': 'شروع بازی',
      'lobby.settings': 'تنظیمات',
      'lobby.howto': 'طرز بازی',
      'lobby.quit': 'خروج',

      'setup.eyebrow': 'پشت صحنه',
      'setup.tagline': 'امشب کی می‌خواهد برود روی صحنه؟',
      'setup.rail.0': 'شرکت‌کنندگان',
      'setup.rail.1': 'دسته‌ها',
      'setup.rail.2': 'زنگ‌ها',
      'setup.rail.3': 'شرط‌ها',
      'setup.rail.4': 'پایانی',
      'setup.contestants': 'شرکت‌کنندگان',
      'setup.names': 'اسم‌ها',
      'setup.sound': 'صدا',
      'setup.on': 'روشن',
      'setup.off': 'خاموش',
      'setup.start': 'برو روی صحنه',
      'setup.back': 'برگشت',
      'setup.nameAria': 'نام شرکت‌کنندهٔ {n}',
      'setup.playerDefault': 'بازیکن {n}',

      'setup.opponents': 'حریف‌ها',
      'setup.opponents.human': 'آدم‌ها',
      'setup.opponents.mixed': 'قاطی',
      'setup.opponents.bots': 'ربات‌ها',
      'setup.difficulty': 'درجهٔ سختی ربات‌ها',
      'setup.answerMode': 'نحوهٔ جواب دادن',
      'setup.answerMode.mc': 'چهارگزینه‌ای',
      'setup.answerMode.write': 'جواب نوشتنی',

      'bot.easy': 'آنتن‌خر',
      'bot.normal': 'نوستالژی',
      'bot.hard': 'عموی تو',
      'bot.brutal': 'بایگانی',
      'bot.easy.desc': 'هر چه در اینستاگرام دیده را باور می‌کند.',
      'bot.normal.desc': 'مطمئن است دههٔ هفتاد بهتر بود.',
      'bot.hard.desc': 'یک واقعیت غول‌آسا می‌داند و از آن تکان نمی‌خورد.',
      'bot.brutal.desc': 'هر چهل‌ونُه کتاب را خوانده. دو بار.',

      'board.menu': 'منو',
      'board.rail.0': 'اطلاعات',
      'board.rail.1': 'فرهنگ',
      'board.rail.2': 'نظرهای مزخرف',
      'board.rail.3': 'اعتمادبه‌نفس بی‌دلیل',
      'board.rail.4': 'و البته بحث و دعوا',
      'round.single.kicker': 'دور اول',
      'round.single.title': 'جپاردی!',
      'round.double.kicker': 'دور دوم',
      'round.double.title': 'جپاردی دوبل',
      'round.final.kicker': 'دور پایانی',
      'round.final.title': 'جپاردی پایانی',

      'clue.buzz': 'زنگ',
      'clue.buzzLocked': 'از دور خارج',
      'clue.answering': 'در حال جواب دادن',
      'clue.nobody': 'کسی نبود؟',
      'clue.nobodyBody': 'سؤال هنوز روی تخته است.',
      'clue.writePlaceholder': 'جوابت را بنویس',
      'clue.submit': 'ثبت کن',
      'clue.correct': 'درست',
      'clue.incorrect': 'غلط',
      'clue.outOfTime': 'وقت تمام شد',
      'clue.theAnswer': 'پاسخ',
      'clue.nearMiss': 'نزدیک بود',

      'wager.prompt': 'قبل از دیدن سؤال شرط ببند.',
      'wager.dailyDouble': 'دوبل روزانه',
      'wager.final': 'جپاردی پایانی',
      'wager.youHave': 'موجودی‌ات',
      'wager.max': 'حداکثر',
      'wager.all': 'همه‌اش',
      'wager.half': 'نصف',
      'wager.quarter': 'یک‌چهارم',
      'wager.threeQuarters': 'سه‌چهارم',
      'wager.lock': 'ثبت کن',
      'wager.waiting': '{name} دارد شرط می‌بندد…',

      'results.title': 'نتیجهٔ نهایی',
      'results.tie': 'مساوی',
      'results.winner': '{name} برد',
      'results.playAgain': 'دوباره بازی کن',

      'menu.eyebrow': 'منوی بازی',
      'menu.resume': 'ادامهٔ بازی',
      'menu.restart': 'بازی جدید',
      'menu.lobby': 'برگشت به لابی',

      'settings.eyebrow': 'تنظیمات',
      'settings.sound': 'موسیقی و صدا',
      'settings.keyboard': 'کیبورد',
      'settings.keyboardBody': 'با <kbd>۱</kbd> <kbd>۲</kbd> <kbd>۳</kbd> بزن، با <kbd>A</kbd> تا <kbd>D</kbd> جواب بده. کلیدهای جهت و <kbd>Return</kbd> روی تخته جابه‌جا می‌شوند.',
      'settings.keyboardBodyWrite': 'با <kbd>۱</kbd> <kbd>۲</kbd> <kbd>۳</kbd> بزن، بعد جواب را تایپ کن و <kbd>Return</kbd> را بزن. وقتی سؤالی باز نیست، کلیدهای جهت و <kbd>Return</kbd> روی تخته جابه‌جا می‌شوند.',
      'settings.controllers': 'دسته‌ها',
      'settings.controllersBody': 'برای هر شرکت‌کننده یک دسته وصل کن — اولی بازیکن ۱، دومی بازیکن ۲ و همین‌طور؛ و هر دسته فقط برای بازیکن خودش زنگ می‌زند. هر دسته منوها و تخته را هم می‌گرداند: دی‌پد یا آنالوگ چپ حرکت می‌دهد، <kbd class="glyph">A</kbd> انتخاب می‌کند، <kbd class="glyph">B</kbd> برمی‌گردد و <kbd class="glyph pill">Start</kbd> منوی بازی را باز می‌کند.',
      'settings.close': 'بستن',

      'howto.eyebrow': 'طرز بازی',
      'howto.body1': 'از روی تخته یک خانه انتخاب کن تا سؤال باز شود. وقتی سؤال آمد، همه با هم با دکمهٔ زنگ خودشان می‌زنند — هر که اول بزند زمین را می‌گیرد و جواب می‌دهد. جواب درست ارزش سؤال را اضافه می‌کند؛ جواب غلط آن را کم می‌کند و سؤال را به بقیه می‌سپارد.',
      'howto.body2': 'در هر دور یک خانه دوبل روزانه است و تنها جواب داده می‌شود، بی‌اینکه کسی نجاتت دهد. بازی با جپاردی پایانی تمام می‌شود: پیش از دیدن سؤال شرط می‌بندی. خوب خرجش کن.'
    }
  };

  /* Units, clock labels and the host's running commentary sit outside the screen
     tables because a formatter, a timer and the clue machinery read them rather
     than the markup — but both languages still fill from here so there is one
     place to change a word.

     The host is smug, snarky and mean; that is the register in both languages,
     and it is the one place a translation is judged on attitude rather than
     accuracy. */
  var EXTRA = {
    en: {
      'unit.m': 'M', 'unit.toman': ' toman',
      'clock.read': 'Read', 'clock.buzz': 'Buzz', 'clock.answer': 'Answer',
      'clock.pick': 'Pick a clue',
      'tab.single': 'Round 1', 'tab.double': 'Double Jeopardy', 'tab.final': 'Final Jeopardy',
      'board.round': 'Round',

      /* Five taunts drawn at random when a wrong answer hands the clue on. */
      'clue.lockout.0': 'Wrong. Somebody else want to have a go?',
      'clue.lockout.1': 'Nope. Who else thinks they know?',
      'clue.lockout.2': 'Wrong. Anyone else feeling brave?',
      'clue.lockout.3': 'No. Somebody take it off their hands.',
      'clue.lockout.4': 'Wrong. The clue is still on the board.',

      /* The verdict line over the answer. {name} and {value} are filled in —
         `value` already carries its sign and its unit. */
      'verdict.correct': 'Correct. {name} {value}',
      'verdict.lockedOut': 'Wrong. {name} is locked out',
      'verdict.nobody': 'Nobody had it',
      'verdict.nobodyBuzzed': 'Nobody even buzzed',
      'verdict.tooSlow': 'Too slow, {name}. {value}',
      'verdict.wrong': 'Wrong, {name}. {value}',
      'verdict.answer': 'Answer: ',
      'verdict.sourcePage': 'p. {n}',
      'verdict.secondChance': 'Second Chance',
      'verdict.continue': 'Continue',
      'verdict.youWrote': 'You wrote: {text}',
      /* The head over a host line that is not a verdict — the judge asking
         which Fazlollah, while the question is still live. */
      'verdict.says': 'The host cuts in',

      /* Six robots, named once so a seat keeps its name across a language
         switch and a redraw of the lobby. */
      'bot.name.1': 'Mirza ChatGPT',
      'bot.name.2': 'Cyrus the Algorithm',
      'bot.name.3': 'Bot-ol-Molk',
      'bot.name.4': 'Clippy Khan',
      'bot.name.5': 'Nostradamus.exe',
      'bot.name.6': 'Shah Mat',

      /* The write-in field. Generous by design, and the hint says so, because
         a player who does not know the game forgives transliteration should
         not be playing it as a spelling test. */
      'clue.writeHint': 'Spelling forgiven. A surname will do.',
      'wager.botWrites': '{name} has locked a wager.',

      /* The confusion set, spoken when a player reaches for the wrong man of
         the same name. Each is a comeback, not a correction: the host knows
         exactly which one was meant and is enjoying that the player does not. */
      'judge.hisFather': 'That would be his father.',
      'judge.hisSon': 'You are a generation too late. That was his son.',
      'judge.qajarMajles': 'No. Mohammad Ali Shah was the Qajar who bombarded the Majles.',
      'judge.pahlaviMonarch': 'No. Mohammad Reza Shah was the Pahlavi monarch.',
      'judge.zahedi': 'No. Zahedi was the 1953 premier, not the constitutional-era cleric.',
      'judge.whichFazlollah': 'Which Fazlollah? Give me a title or a surname.',
      'judge.whichQavam': 'Which Qavam? There is more than one and you know it.',
      'judge.fullName': 'Full name, please. I am not giving this one away for a surname.',
      'judge.whichHassan': 'Which Hassan? A surname would help.',
      'judge.mostowfi': 'No. That was Mostowfi ol-Mamalek.',

      /* The buzz row and its lamp. */
      'buzz.out': 'Out of it — and someone else wants your money.',
      'buzz.early': '{name} jumped it. That is what patience looks like, {name}.',
      'buzz.live': 'Buzzers are live. Prove something.',
      'buzz.wait': 'Not yet. Watch the lamp — jump it and you sit out the start.',
      'buzz.lampOn': 'Buzz',
      'buzz.lampOff': 'Wait',
      'buzz.with': 'Buzz · {name}',

      /* Daily Double */
      'dd.solo': ', you’re on your own here. Wager whatever you dare.',

      /* Wagers. `wager.quarter` and friends name the idea; these label the
         three quick buttons beside the slider. */
      'wager.amountAria': 'Wager amount',
      'wager.quickQuarter': 'Quarter',
      'wager.quickHalf': 'Half',
      'wager.quickThreeQuarters': 'Three Quarters',
      'wager.quickAll': 'All In',
      'wager.place': ', place your wager. You can still back out.',
      'wager.finalTag': 'Final · {value}',
      'wager.wagerOf': '{name} · wager {value}',

      /* Final Jeopardy's own verdict line and its closing button. */
      'final.timeUp': 'Time’s up — ',
      'final.correctLead': 'Correct — ',
      'final.incorrectLead': 'Incorrect — ',
      'final.next': 'Next Contestant',
      'final.score': 'Final Score',

      /* Controller toasts. `pad.player` is the odd one out in Persian: the name
         leads, because in RTL the leftmost token is the last one read. */
      'pad.controller': 'Controller',
      'pad.player': 'Player {n} — {name}',
      'pad.disconnected': 'Controller disconnected'
    },
    fa: {
      'unit.m': '', 'unit.toman': ' میلیون تومان',
      'clock.read': 'بخوان', 'clock.buzz': 'زنگ', 'clock.answer': 'جواب',
      'clock.pick': 'یک سؤال انتخاب کن',
      'tab.single': 'دور اول', 'tab.double': 'جپاردی دو', 'tab.final': 'جپاردی پایانی',
      'board.round': 'دور',

      'clue.lockout.0': 'غلط. یکی دیگه دوست داره امتحان کنه؟',
      'clue.lockout.1': 'نه. کی فکر می‌کنه می‌دونه؟',
      'clue.lockout.2': 'غلط. کسی جراتش رو داره؟',
      'clue.lockout.3': 'نه. یکی از دستش بگیره.',
      'clue.lockout.4': 'غلط. سؤال هنوز روی تخته است.',

      'verdict.correct': 'درست. {name} {value}',
      'verdict.lockedOut': 'غلط. {name} از دور خارج شد',
      'verdict.nobody': 'هیچ‌کس جوابش رو نداشت',
      'verdict.nobodyBuzzed': 'هیچ‌کس حتی زنگ نزد',
      'verdict.tooSlow': 'خیلی کند، {name}. {value}',
      'verdict.wrong': 'غلط، {name}. {value}',
      'verdict.answer': 'پاسخ: ',
      'verdict.sourcePage': 'ص. {n}',
      'verdict.secondChance': 'فرصت دوباره',
      'verdict.continue': 'ادامه',
      'verdict.youWrote': 'نوشتی: {text}',
      'verdict.says': 'مجری وسط حرف می‌پرد',

      'bot.name.1': 'میرزا چت‌جی‌پی‌تی',
      'bot.name.2': 'کوروش الگوریتم',
      'bot.name.3': 'بت‌الملک',
      'bot.name.4': 'کلیپی‌خان',
      'bot.name.5': 'نوستراداموس نسخهٔ ۲',
      'bot.name.6': 'شاه‌مات',

      'clue.writeHint': 'غلط املایی را می‌بخشیم. فامیل هم قبول است.',
      'wager.botWrites': '{name} شرطش را ثبت کرد.',

      'judge.hisFather': 'آن پدرش بود.',
      'judge.hisSon': 'یک نسل دیر رسیدی. آن پسرش بود.',
      'judge.qajarMajles': 'نه. محمدعلی‌شاه همان قاجاری بود که مجلس را به توپ بست.',
      'judge.pahlaviMonarch': 'نه. محمدرضاشاه پهلوی بود.',
      'judge.zahedi': 'نه. زاهدی نخست‌وزیر ۱۳۳۲ بود، نه آن روحانی عصر مشروطه.',
      'judge.whichFazlollah': 'کدام فضل‌الله؟ لقب یا فامیلش را بگو.',
      'judge.whichQavam': 'کدام قوام؟ بیش از یکی داریم و خودت هم می‌دانی.',
      'judge.fullName': 'نام کامل لطفاً. با یک فامیل این را لو نمی‌دهم.',
      'judge.whichHassan': 'کدام حسن؟ فامیلش کمک می‌کند.',
      'judge.mostowfi': 'نه. آن مستوفی‌الممالک بود.',

      'buzz.out': 'از بازی بیرونی — و یکی دیگه پولت رو می‌خواد.',
      'buzz.early': '{name} زود زد. صبر یعنی همین، {name}.',
      'buzz.live': 'زنگ‌ها آزادن. یه چیزی ثابت کن.',
      'buzz.wait': 'هنوز نه. چراغ رو بپا — زود بزنی، از اول بازی بیرونی.',
      'buzz.lampOn': 'زنگ',
      'buzz.lampOff': 'صبر',
      'buzz.with': 'زنگ · {name}',

      'dd.solo': '، اینجا تنها هستی. هر چه جرات داری شرط ببند.',

      'wager.amountAria': 'مبلغ شرط',
      'wager.quickQuarter': 'یک‌چهارم',
      'wager.quickHalf': 'نصف',
      'wager.quickThreeQuarters': 'سه‌چهارم',
      'wager.quickAll': 'همه‌اش',
      'wager.place': '، شرطت رو بذار. هنوز می‌تونی پشیمون بشی.',
      'wager.finalTag': 'پایانی · {value}',
      'wager.wagerOf': '{name} · شرط {value}',

      'final.timeUp': 'وقت تمام — ',
      'final.correctLead': 'درست — ',
      'final.incorrectLead': 'غلط — ',
      'final.next': 'نفر بعدی',
      'final.score': 'امتیاز نهایی',

      'pad.controller': 'دستگاه',
      'pad.player': '{name} — بازیکن {n}',
      'pad.disconnected': 'دستگاه قطع شد'
    }
  };
  ['en', 'fa'].forEach(function (code) {
    var t = STRINGS[code], x = EXTRA[code], k;
    for (k in x) if (Object.prototype.hasOwnProperty.call(x, k)) t[k] = x[k];
  });

  var LANG = 'en';

  /* The Persian digits are a display concern only — nothing computed ever sees
     them. `num()` is for the strings that go on screen; the maths stays ASCII. */
  var FA_DIGITS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

  function toFaDigits(s) {
    return String(s).replace(/[0-9]/g, function (d) { return FA_DIGITS[+d]; });
  }

  /* Numbers the audience reads — scores, values, clocks, wagers — turn over with
     the language. Numbers inside a URL, a class or an id never come through
     here. */
  function num(s) {
    return LANG === 'fa' ? toFaDigits(s) : String(s);
  }

  function T(key, vars) {
    var table = STRINGS[LANG] || STRINGS.en;
    var s = table[key];
    if (s == null) s = STRINGS.en[key];
    if (s == null) return key;
    if (vars) {
      s = s.replace(/\{(\w+)\}/g, function (m, k) {
        return Object.prototype.hasOwnProperty.call(vars, k) ? String(vars[k]) : m;
      });
    }
    return s;
  }

  /* Fills every element that carried its copy in the markup. Four attributes,
     one per kind of slot: text, markup (the taglines carry a line break and the
     overlays carry <kbd>), aria-label, and placeholder. */
  function apply(root) {
    var scope = root || document;
    var i, n, key, val;

    n = scope.querySelectorAll('[data-i18n]');
    for (i = 0; i < n.length; i++) {
      key = n[i].getAttribute('data-i18n');
      val = T(key);
      if (n[i].textContent !== val) n[i].textContent = val;
    }

    n = scope.querySelectorAll('[data-i18n-html]');
    for (i = 0; i < n.length; i++) {
      key = n[i].getAttribute('data-i18n-html');
      val = T(key);
      if (n[i].innerHTML !== val) n[i].innerHTML = val;
    }

    n = scope.querySelectorAll('[data-i18n-aria]');
    for (i = 0; i < n.length; i++) {
      n[i].setAttribute('aria-label', T(n[i].getAttribute('data-i18n-aria')));
    }

    n = scope.querySelectorAll('[data-i18n-ph]');
    for (i = 0; i < n.length; i++) {
      n[i].setAttribute('placeholder', T(n[i].getAttribute('data-i18n-ph')));
    }

    n = scope.querySelectorAll('[data-i18n-title]');
    for (i = 0; i < n.length; i++) {
      n[i].setAttribute('title', T(n[i].getAttribute('data-i18n-title')));
    }

    /* Numerals the audience reads sit in the markup, not in a string table, so
       they are caught by a marker attribute instead of a key. Re-running this
       is safe: the Persian digits are outside [0-9]. */
    n = scope.querySelectorAll('[data-num]');
    for (i = 0; i < n.length; i++) {
      n[i].textContent = num(n[i].textContent);
    }
  }

  /* The one switch. Everything else — the mirrored rails, the Persian face, the
     numbers — is CSS keyed off `dir`, so this is the whole of it. */
  function setLang(code) {
    LANG = code === 'fa' ? 'fa' : 'en';
    window.LANG = LANG;

    var html = document.documentElement;
    html.setAttribute('lang', LANG === 'fa' ? 'fa' : 'en');
    html.setAttribute('dir', LANG === 'fa' ? 'rtl' : 'ltr');

    document.body.classList.toggle('lang-fa', LANG === 'fa');

    try { localStorage.setItem('jeopardy.lang', LANG); } catch (e) { /* file:// */ }

    apply(document);

    /* Anything built in JS rather than carried in the markup has to be told to
       rebuild itself. app.js listens for this. */
    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: LANG } }));
  }

  function savedLang() {
    try {
      var v = localStorage.getItem('jeopardy.lang');
      return v === 'fa' ? 'fa' : 'en';
    } catch (e) { return 'en'; }
  }

  window.I18N = STRINGS;
  window.T = T;
  window.num = num;
  window.setLang = setLang;
  window.applyI18n = apply;
  window.getLang = function () { return LANG; };
  window.LANG = LANG;
  window.savedLang = savedLang;
})();
