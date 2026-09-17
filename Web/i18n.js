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
      /* The boot screen, one screen before the door. Two words and no more: the
         mark above them is the mark itself, Latin in both editions the way the
         wordmark image is, so this is the only copy on the screen. */
      'boot.loading': 'Warming the studio',
      'boot.ready': 'Rolling',
      /* The front door. Its own line, and the mild one: a stranger who tapped an
         icon has not asked to be talked down to yet, so the sneer is held back
         until the title card one screen later. Same voice, lower volume. */
      'front.tagline': 'Sure, you say you know Iranian history. So does my uncle, my Snapp driver, and the guy I met at the bus stop — and I don’t even take the bus.<br>Let’s put that to the test.',
      'front.subtitle': 'Iranian Edition',
      'front.enter': 'Enter',
      'front.mainSign': 'Main Edition',
      'front.coursesSign': 'Courses',
      'front.back': 'Back',
      'front.soon': 'Coming soon',
      /* The names of the two courses that are announced but not written. They are
         keys rather than edition data because there is no edition to hold them —
         see the note on `SOON_CARDS` in `app.js`. */
      'front.soonQajar': 'Qajars',
      'front.soonPahlavi': 'Pahlavis',

      /* The two rows of the chooser, and the one label over each. A show's own
         name, blurb and credits are edition data, not keys — see `editions.js`
         and each course's `course.js`. */
      'splash.main': 'The main show',
      'splash.courses': 'Or try a separate course',

      /* The title card */
      'splash.tagline': 'Because you don’t know your own history<br>and it’s time somebody told you so.',
      'splash.enter': 'Let’s begin',
      /* MAIN's imprint slot, which a course fills with its code, its professor
         and its university. `{name}` is the host. */
      'imprint.hosted': 'Hosted by {name}',
      'imprint.courseHosted': 'Hosted by {who} at the {where}',
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

      /* Lobby */
      'common.corner.egos': 'Same game.<br>Bigger egos.',
      'common.corner.hard': 'Hard questions.<br>Unjustified confidence.',
      'common.corner.place': 'Tehran<br>35.6892° N, 51.3890° E',
      'lobby.tagline': 'A country full of experts.<br>Let’s find out how much of that survives.',
      'lobby.rail.0': 'People, from geniuses to charlatans',
      'lobby.rail.1': 'Places you swear you know',
      'lobby.rail.2': 'Empires that blew it',
      'lobby.rail.3': 'Culture, customs & pretension',
      'lobby.rail.4': 'Revolutions & bad decisions',
      'lobby.rail.5': 'Art, from genius to “what on earth?”',
      'lobby.rail.6': 'Science, so stop guessing',
      'lobby.rail.7': 'Sports, for the stat freaks',
      'lobby.rail.8': 'And plenty more you’re weirdly confident about…',
      'lobby.start': 'Start game',
      'lobby.editions': 'Other shows',
      'lobby.settings': 'Settings',
      'lobby.howto': 'How to play',
      'lobby.quit': 'Quit',
      /* The Reading List. Its rows are citations in whatever language they were
         published in, so only this chrome is translated. */
      'reading.menu': 'Reading list',
      'reading.title': 'Reading list',

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
      'bot.brutal.desc': 'Has read all fifty books. Twice.',

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
      'menu.sprites': 'Host & bubbles',
      'menu.voice': 'Host voice',

      /* Settings */
      'settings.eyebrow': 'Settings',
      'settings.sound': 'Music & sound',
      'settings.keyboard': 'Keyboard',
      'settings.keyboardBody': 'Buzz with <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd>, or with <kbd>Space</kbd> or <kbd>Return</kbd> when you are the only one at the machine. Answer with <kbd>A</kbd>–<kbd>D</kbd>. Arrow keys move through the board and the menus, <kbd>Return</kbd> chooses, <kbd>Esc</kbd> opens the match menu.',
      'settings.keyboardBodyWrite': 'Buzz with <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd>, or with <kbd>Space</kbd> or <kbd>Return</kbd> when you are the only one at the machine. Then type the answer and press <kbd>Return</kbd>. Arrow keys move through the board and the menus, and <kbd>Esc</kbd> opens the match menu.',
      'settings.controllers': 'Controllers',
      'settings.controllersBody': 'Plug in one controller per contestant — the first is Player 1, the second Player 2, and so on, and each one only buzzes for its own player. Every controller also drives the menus and the board: the d-pad or left stick moves, <kbd class="glyph">A</kbd> chooses, <kbd class="glyph">B</kbd> goes back, and <kbd class="glyph pill">Start</kbd> opens the match menu.',
      'settings.close': 'Close',

      /* How to play */
      'howto.eyebrow': 'How to play',
      'howto.body1': 'Pick a tile from the board to open a clue. When the clue appears, everyone races to hit their own <em>Buzz</em> button — first one in gets the floor and chooses an answer. Right answers add the clue’s value; wrong ones subtract it and hand the clue to everyone else.',
      'howto.body2': 'One tile a round is a Daily Double and gets answered alone, with nobody to bail you out. The match closes with Final Jeopardy: you wager before you see the clue. Spend it well.',

      /* The chooser in the lobby. One show, several question sets. */
      'editions.title': 'Which show?',
      'editions.body': 'One show, different questions. The main edition deals from the whole bank; each course deals only from its own.'
    },

    fa: {
      'doc.title': 'جپاردی! — نسخهٔ ایرانی',

      'lang.choose': 'زبانت را انتخاب کن',
      'lang.en': 'English',
      'lang.fa': 'فارسی',
      'lang.beta': 'نسخهٔ فارسی آزمایشی است',
      'boot.loading': 'استودیو در حال گرم شدن',
      'boot.ready': 'آماده‌ایم',
      'front.tagline': 'خب، می‌گویی تاریخ ایران را بلدی. عموی من هم بلد است، رانندهٔ اسنپم هم، و آن آقایی که دم ایستگاه اتوبوس دیدم — من اصلاً اتوبوس سوار نمی‌شوم.<br>بیا ببینیم این ادعا چقدر می‌ارزد.',
      'front.subtitle': 'نسخهٔ ایرانی',
      'front.enter': 'ورود',
      'front.mainSign': 'نسخهٔ اصلی',
      'front.coursesSign': 'دوره‌ها',
      'front.back': 'بازگشت',
      'front.soon': 'به‌زودی',
      'front.soonQajar': 'قاجار',
      'front.soonPahlavi': 'پهلوی',
      'splash.main': 'برنامهٔ اصلی',
      'splash.courses': 'یا یک درس جدا را امتحان کنید',

      'splash.tagline': 'چون هیچ‌کدام‌تان تاریخ خودتان را نمی‌دانید<br>و وقتش رسیده دست‌کم یک چیزی یاد بگیرید',
      'splash.enter': 'شروع کنیم',
      'imprint.hosted': 'با اجرای {name}',
      'imprint.courseHosted': 'با میزبانی {who} از {where}',
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

      'common.corner.egos': 'همان بازی.<br>خودپسندیِ بیشتر.',
      'common.corner.hard': 'سؤال‌های سخت.<br>اعتمادبه‌نفس بی‌مورد.',
      'common.corner.place': 'تهران<br><span class="lat">35.6892° N, 51.3890° E</span>',
      'lobby.tagline': 'یک مملکت پر از کارشناس.<br>حالا ببینیم چقدرش دوام می‌آورد.',
      'lobby.rail.0': 'آدم‌ها، از نابغه تا شارلاتان',
      'lobby.rail.1': 'جاهایی که فکر می‌کنی بلدی',
      'lobby.rail.2': 'امپراتوری‌هایی که گند زدند',
      'lobby.rail.3': 'فرهنگ، رسم و رسوم و ادا و اطوار',
      'lobby.rail.4': 'انقلاب‌ها و تصمیم‌های فاجعه‌بار',
      'lobby.rail.5': 'هنر، از شاهکار تا «این دیگه چیه؟»',
      'lobby.rail.6': 'علم، وقتی حدس جواب نمی‌دهد',
      'lobby.rail.7': 'ورزش، برای آماربازها',
      'lobby.rail.8': 'و کلی چیز دیگر که زیادی درباره‌شان مطمئنی…',
      'lobby.start': 'شروع بازی',
      'lobby.editions': 'نمایش‌های دیگر',
      'lobby.settings': 'تنظیمات',
      'lobby.howto': 'طرز بازی',
      'lobby.quit': 'خروج',
      'reading.menu': 'فهرست خواندنی‌ها',
      'reading.title': 'فهرست خواندنی‌ها',

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
      'bot.brutal.desc': 'هر پنجاه کتاب را خوانده. دو بار.',

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
      'menu.sprites': 'مجری و حبابها',
      'menu.voice': 'صدای مجری',

      'settings.eyebrow': 'تنظیمات',
      'settings.sound': 'موسیقی و صدا',
      'settings.keyboard': 'کیبورد',
      'settings.keyboardBody': 'با <kbd>۱</kbd> <kbd>۲</kbd> <kbd>۳</kbd> بزن؛ اگر تنها کسی هستی که پای این دستگاه نشسته، با <kbd>Space</kbd> یا <kbd>Return</kbd> هم می‌توانی بزنی. با <kbd>A</kbd> تا <kbd>D</kbd> جواب بده. کلیدهای جهت روی تخته و در منوها راه می‌روند، <kbd>Return</kbd> انتخاب می‌کند و <kbd>Esc</kbd> منوی مسابقه را باز می‌کند.',
      'settings.keyboardBodyWrite': 'با <kbd>۱</kbd> <kbd>۲</kbd> <kbd>۳</kbd> بزن؛ اگر تنها کسی هستی که پای این دستگاه نشسته، با <kbd>Space</kbd> یا <kbd>Return</kbd> هم می‌توانی بزنی. بعد جواب را تایپ کن و <kbd>Return</kbd> را بزن. کلیدهای جهت روی تخته و در منوها راه می‌روند و <kbd>Esc</kbd> منوی مسابقه را باز می‌کند.',
      'settings.controllers': 'دسته‌ها',
      'settings.controllersBody': 'برای هر شرکت‌کننده یک دسته وصل کن — اولی بازیکن ۱، دومی بازیکن ۲ و همین‌طور؛ و هر دسته فقط برای بازیکن خودش زنگ می‌زند. هر دسته منوها و تخته را هم می‌گرداند: دی‌پد یا آنالوگ چپ حرکت می‌دهد، <kbd class="glyph">A</kbd> انتخاب می‌کند، <kbd class="glyph">B</kbd> برمی‌گردد و <kbd class="glyph pill">Start</kbd> منوی بازی را باز می‌کند.',
      'settings.close': 'بستن',

      'howto.eyebrow': 'طرز بازی',
      'howto.body1': 'از روی تخته یک خانه انتخاب کن تا سؤال باز شود. وقتی سؤال آمد، همه با هم با دکمهٔ زنگ خودشان می‌زنند — هر که اول بزند زمین را می‌گیرد و جواب می‌دهد. جواب درست ارزش سؤال را اضافه می‌کند؛ جواب غلط آن را کم می‌کند و سؤال را به بقیه می‌سپارد.',
      'howto.body2': 'در هر دور یک خانه دوبل روزانه است و تنها جواب داده می‌شود، بی‌اینکه کسی نجاتت دهد. بازی با جپاردی پایانی تمام می‌شود: پیش از دیدن سؤال شرط می‌بندی. خوب خرجش کن.',

      /* The chooser in the lobby. One show, several question sets. */
      'editions.title': 'کدام‌شان؟',
      'editions.body': 'یک نمایش، سؤال‌های متفاوت. نسخهٔ اصلی از کل گنجینه می‌پرسد و هر دوره فقط از سؤال‌های خودش.'
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
      /* The podium badge on the seat whose turn it is to open the board. */
      'board.picks': 'Picks',

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

      /* The robot roster. An index is a character, not a seat: the same number
         reads as the same joke in both languages, so a seat keeps its name
         across a language switch. `Bots.redraw` shuffles these indices once
         per green room, which is why the pool is much larger than the table —
         a seat should not be the same robot every night. */
      'bot.name.1': 'Mirza ChatGPT',
      'bot.name.2': 'Cyrus the Algorithm',
      'bot.name.3': 'Bot-ol-Molk',
      'bot.name.4': 'Clippy Khan',
      'bot.name.5': 'Nostradamus.exe',
      'bot.name.6': 'Shah Mat',
      'bot.name.7': 'Amir Kabot',
      'bot.name.8': 'Khayyam the Query',
      'bot.name.9': 'Grand VazAIr',
      'bot.name.10': 'Molla SadRAM',
      'bot.name.11': "Malek al-Sho'arAI",
      'bot.name.12': 'Mirza Cache Khan',
      'bot.name.13': 'Gholam-Ali Gorithm',
      'bot.name.14': 'AI-Tollah',
      'bot.name.15': 'Kodkhoda',
      'bot.name.16': 'Houshang Artificial',
      'bot.name.17': 'Mashinollah Khan',
      'bot.name.18': 'Chat-qoli Khan',
      'bot.name.19': 'Kod ol-Saltaneh',
      'bot.name.20': 'Hafez ol-Dowleh',
      'bot.name.21': 'Prompt ol-Molk',
      'bot.name.22': 'Botbashi',
      'bot.name.23': 'Ram Ali Khan',
      'bot.name.24': 'Algorithm-qoli Khan',

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
      'buzz.soloLive': 'The whole screen is the buzzer. Prove something.',
      'buzz.soloWait': 'Not yet. When the lamp turns, the whole screen is the buzzer.',
      'buzz.plate': 'Buzz',
      'buzz.lampOn': 'Live',
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
      'pad.disconnected': 'Controller disconnected',

      /* ── The online table ──────────────────────────────────────────────── */
      'online.title': 'The Online Table',
      'online.blurb': 'One device runs the board and does the counting. Everybody else gets a buzzer and their own excuses.',
      'online.host': 'Host a Table',
      'online.join': 'Join a Table',
      'online.hostBlurb': 'Your device is the board. Theirs are the buzzers.',
      'online.joinBlurb': 'Somebody else is holding the board. Type what they read out.',
      'online.code': 'Room Code',
      'online.codeHint': 'Four characters. Read them out loud.',
      'online.yourName': 'Your Name',
      'online.namePlaceholder': 'Whatever you call yourself',
      'online.connect': 'Sit Down',
      'online.connecting': 'Knocking…',
      'online.waiting': 'Waiting for the host to start',
      'online.waitingHost': 'Waiting for the others',
      'online.waitLock': 'Waiting for {name} to lock it in',
      'online.roster': 'At the Table',
      'online.nobody': 'Nobody yet. Just you and your confidence.',
      'online.seated': '{name} sat down.',
      'online.left': '{name} left.',
      'online.dropped': '{name} lost the wire. Holding their seat.',
      'online.back': '{name} is back.',
      'online.reconnecting': 'Reconnecting…',
      'online.lost': 'Lost the table. Read the code out and try again.',
      'online.setup': 'Set Up the Match',
      'online.copyLink': 'Copy Link',
      'online.copied': 'Copied',
      'online.leave': 'Leave the Table',
      'online.closed': 'The host closed the table.',
      'online.linkHint': 'Or send them this link.',
      'online.roomFull': 'The table is full.',
      'online.noWebrtc': 'This browser has no WebRTC. There is no fixing that.',

      /* The phone in a player's hand */
      'remote.eyes': 'Eyes on the board.',
      'remote.pick': 'Waiting for somebody to pick a clue.',
      'remote.reading': 'Read it. Buzzers are shut.',
      'remote.live': 'Buzzers are live. Prove something.',
      'remote.buzz': 'Buzz',
      'remote.yours': 'Yours. Answer it.',
      'remote.theirs': '{name} has it.',
      'remote.sitting': 'Sitting this one out. Watch and learn.',
      'remote.wager': 'Wager',
      'remote.lockWager': 'Lock the Wager',
      'remote.typeAnswer': 'Type the answer',
      'remote.lockIn': 'Lock It In',
      'remote.nobody': 'Nobody wanted it.',
      /* The board belongs to one seat, and the phones are where the room finds
         out which. The chooser gets a board of their own to open; everybody else
         is told whose turn it is, by name. */
      'remote.pickYours': 'Your board. Open it.',
      'remote.pickBy': '{name} opens the next one.'
    },
    fa: {
      /* A bare ۲۰۰ on a tile is a number, not money: the compact form carries
         its own unit so the board reads as figures of toman, and the spelled
         form then adds only the currency, the same split as `M` + `toman`. */
      'unit.m': ' میلیون', 'unit.toman': ' تومان',
      'clock.read': 'بخوان', 'clock.buzz': 'زنگ', 'clock.answer': 'جواب',
      'clock.pick': 'یک سؤال انتخاب کن',
      'tab.single': 'دور اول', 'tab.double': 'جپاردی دو', 'tab.final': 'جپاردی پایانی',
      'board.round': 'دور',
      'board.picks': 'انتخاب',

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
      'bot.name.2': 'کوروش کُدبیر',
      'bot.name.3': 'بات‌الملک',
      'bot.name.4': 'کلیپی‌خان',
      'bot.name.5': 'نوستراداموس نسخهٔ ۲',
      'bot.name.6': 'شاه‌مات',
      'bot.name.7': 'امیر کُدبیر',
      'bot.name.8': 'عمر کوئریام',
      'bot.name.9': 'وزیر اعظَم‌پی‌تی',
      'bot.name.10': 'ملا صد‌رَم',
      'bot.name.11': 'ملک‌الشعربات',
      'bot.name.12': 'میرزا کَش‌الدوله',
      'bot.name.13': 'غلامعلی‌گوریتم',
      'bot.name.14': 'آی‌تی‌الله',
      'bot.name.15': 'کُدخدا',
      'bot.name.16': 'هوشنگ مصنوعی',
      'bot.name.17': 'ماشین‌الله خان',
      'bot.name.18': 'چت‌قلی‌خان',
      'bot.name.19': 'کُدالسلطنه',
      'bot.name.20': 'حافظه‌الدوله',
      'bot.name.21': 'پرومپت‌الملک',
      'bot.name.22': 'بات‌باشی',
      'bot.name.23': 'رم‌علی‌خان',
      'bot.name.24': 'الگوریتم‌قلی‌خان',

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
      'buzz.soloLive': 'تمام صفحه زنگه. یه چیزی ثابت کن.',
      'buzz.soloWait': 'هنوز نه. چراغ که روشن شد، تمام صفحه زنگه.',
      'buzz.plate': 'زنگ',
      'buzz.lampOn': 'روشن',
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
      'pad.disconnected': 'دستگاه قطع شد',

      /* ── میز آنلاین ────────────────────────────────────────────────────── */
      'online.title': 'میز آنلاین',
      'online.blurb': 'یک دستگاه میز را می‌گرداند و حساب‌وکتاب می‌کند. بقیه فقط یک زنگ دارند و عالمی از بهانه.',
      'online.host': 'میز بزن',
      'online.join': 'سر میز بنشین',
      'online.hostBlurb': 'دستگاه تو میز است. مال آن‌ها زنگ.',
      'online.joinBlurb': 'یکی دیگر میز را دارد. هر چه می‌خواند تایپ کن.',
      'online.code': 'کد اتاق',
      'online.codeHint': 'چهار حرف. بلند بخوانشان.',
      'online.yourName': 'نامت',
      'online.namePlaceholder': 'هر چه خودت را صدا می‌زنی',
      'online.connect': 'بنشین',
      'online.connecting': 'در می‌زند…',
      'online.waiting': 'منتظریم میزبان شروع کند',
      'online.waitingHost': 'منتظر بقیه',
      'online.waitLock': 'منتظریم {name} قفلش کند',
      'online.roster': 'سر میز',
      'online.nobody': 'هنوز هیچ‌کس. فقط تو و اعتمادبه‌نفست.',
      'online.seated': '{name} نشست سر میز.',
      'online.left': '{name} رفت.',
      'online.dropped': 'ارتباط {name} قطع شد. جایش نگه داشته می‌شود.',
      'online.back': '{name} برگشت.',
      'online.reconnecting': 'داریم وصل می‌شویم…',
      'online.lost': 'میز از دست رفت. کد را بلند بخوان و دوباره امتحان کن.',
      'online.setup': 'بازی را بچین',
      'online.copyLink': 'کپی پیوند',
      'online.copied': 'کپی شد',
      'online.leave': 'از میز بلند شو',
      'online.closed': 'میزبان میز را بست.',
      'online.linkHint': 'یا این پیوند را برایشان بفرست.',
      'online.roomFull': 'میز پر است.',
      'online.noWebrtc': 'این مرورگر WebRTC ندارد. کاریش نمی‌شود کرد.',

      /* گوشی در دست بازیکن */
      'remote.eyes': 'چشم به تخته.',
      'remote.pick': 'منتظریم یکی سؤال انتخاب کند.',
      'remote.reading': 'بخوان. زنگ‌ها بسته است.',
      'remote.live': 'زنگ‌ها آزادن. یه چیزی ثابت کن.',
      'remote.buzz': 'زنگ',
      'remote.yours': 'مال خودت است. جواب بده.',
      'remote.theirs': 'دست {name} است.',
      'remote.sitting': 'این یکی را نشستی. نگاه کن و یاد بگیر.',
      'remote.wager': 'شرط',
      'remote.lockWager': 'شرط را قفل کن',
      'remote.typeAnswer': 'جواب را تایپ کن',
      'remote.lockIn': 'قفلش کن',
      'remote.nobody': 'هیچ‌کس نخواست.',
      'remote.pickYours': 'تخته مالِ توئه. بازش کن.',
      'remote.pickBy': 'انتخاب سؤال بعدی با {name} است.'
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
    var latin = String(s).replace(/[۰-۹]/g, function (digit) {
      return String(digit.charCodeAt(0) - 0x06F0);
    });
    return LANG === 'fa' ? toFaDigits(latin) : latin;
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
    var next = code === 'fa' ? 'fa' : 'en';
    if (next !== LANG && !document.dispatchEvent(new CustomEvent('beforelangchange', {
      cancelable: true, detail: { lang: next }
    }))) return;
    LANG = next;
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
