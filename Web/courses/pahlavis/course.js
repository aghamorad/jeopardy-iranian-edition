/* The Pahlavis — a course edition of the show.
 *
 * The module the bank and the skin are both cut from: *Iranian History from 1905
 * to 1979*, University of Oxford, Dr Stephanie Cronin's taught paper — a weekly
 * essay, a seminar to argue it in, and one three-hour examination at the end.
 * The eight taught weeks run the 1921 coup, Reza Shah, the Allied occupation,
 * Musaddiq and the oil, Muhammad Reza Shah, the Left, gender and modernity, and
 * Iran and the world, in that order. They are the title card's middle eight
 * rails; the first and the last are the two statements the module opens and
 * closes on, which is why the numerals on that card are the arc's rather than a
 * week's. The concept vocabulary the module drills is the nine-line rail in the
 * lobby; the two things it marks down are the five-line rail on the board.
 * Nothing here is invented for the game — it is the seminar schedule wearing a
 * title card.
 *
 * **This is the first locked course.** It has a syllabus, a professor, a shelf
 * and a stage, and its questions are still being written, so it registers with
 * no `banks` at all and carries `locked: true` instead. A student may walk the
 * lobby, read the shelf and meet the host; nobody may be dealt a board. The lock
 * is worn in three places — the plate on the front door's circle, the disabled
 * Start button in the lobby, and `startMatch`'s own refusal in the engine — and
 * the three of them say the same thing rather than one of them being the only
 * one that works. See `editions.js` for why the flag is required rather than
 * optional, and `wear()` below for the lobby half.
 *
 * Two rules this file obeys, because every course from here on has the same two
 * problems:
 *
 *   * **A professor's cues are namespaced by course.** Stephanie teaches this
 *     one and the Qajars, and the same is true of any tutor who turns up in more
 *     than one module. So her cues are `stephanie_pahlavis_*` here and
 *     `stephanie_qajars_*` there, and nothing is keyed to a bare `stephanie_*`
 *     that a second course could collide with.
 *   * **A host whose lines are written but not yet recorded still gets a clip.**
 *     The bubble on the floor is measured by the audio that is playing, so a cue
 *     with no file behind it is a bubble that closes on the next frame. Her lines
 *     are written and not yet in the booth, so every cue below resolves through
 *     `EDITION_SOUND` to the silent placeholder of the right length rather than to
 *     a file that is not there. Drop a recording in under the cue's own name and
 *     the album is one line away from wearing it — see the note at the foot of
 *     this section.
 *
 * The folder name, the id and the `?ed=` value are one string. A locked course
 * has no bank globals; the moment its questions land it gains them, at
 * `COURSE_CLUES_<UPPER_SNAKE(folder)>` (+ `_FA`), and loses `locked`. To start
 * another course, copy the folder — not these lines — and fill it in.
 *
 * The Pahlavi wordmark replaces MAIN's emblem-bearing O with the uncrowned Lion
 * and Sun. `swapWordmark()` wears it beside the rails and restores MAIN's on
 * return; the Iran course keeps its own wordmark when that course is selected.
 */
(function () {
  'use strict';

  /* Registered after MAIN, and never before it. `general` registering first is
     what makes it the default; this show is the one opted into, not the one that
     opts the others in. */
  window.registerEdition({
    id: 'pahlavis',
    name: { en: 'The Pahlavis', fa: 'پهلوی' },
    blurb: { en: 'A state built in fifty years', fa: 'دولتی که در پنجاه سال ساخته شد' },
    description: {
      en: 'Two shahs, one railway, an occupied country and an oil industry taken back. Fifty-seven years, and the argument still has not settled.',
      fa: 'دو شاه، یک راه‌آهن، کشوری اشغال‌شده و صنعت نفتی که پس گرفته شد. پنجاه‌وهفت سال، و این بحث هنوز تمام نشده.'
    },
    /* The Pahlavi circle art; the new key releases the old cached placeholder. */
    tile: 'courses/pahlavis/assets/tile-course.png?v=20260918-pahlavi-1',
    /* Announced, not yet written. The questions are being authored; everything a
       student may walk through in the meantime is real, so this is a course that
       has not finished rather than one that is not there. */
    locked: true,
    /* Only the host sprite is preloaded here; stage and wordmark are swapped
       through CSS and `swapWordmark()` after their files have landed. */
    art: [
      'courses/pahlavis/assets/sprite-stephanie.png?v=20260918-pahlavi-1'
    ],
    /* Who teaches it and where. Rendered on the selection circle, on the title
       card's imprint and in the lobby. No `code`: the module is a taught paper
       with a title and no number printed anywhere, and inventing an Oxford
       paper number to fill the slot would be a fact made up for a caption. */
    credit: {
      professor:   { en: 'Dr. Stephanie', fa: 'دکتر استفانی' },
      institution: { en: 'University of Oxford', fa: 'دانشگاه آکسفورد' }
    },
    /* No `banks`. The registry admits this descriptor on the strength of
       `locked` alone, and `app.js` empties `CLUES` rather than leaving the last
       edition's array bound — dealing MAIN's clues under this course's name is
       the one thing the registry exists to prevent. */
    /* The eight taught weeks' bibliography, cut from Dr Cronin's 2016 syllabus.
       See `data/readings.js` for what the syllabus prints that the shelf does
       not carry, and why. */
    readings: window.READINGS_PAHLAVIS
  });

  var BAGS = {
    en: window.I18N && window.I18N.en,
    fa: window.I18N && window.I18N.fa
  };
  if (!BAGS.en || !BAGS.fa) return;

  var COURSE = {
    en: {
      /* The title card. Left rail is the first five of the module's ten lines,
         right rail the last five. The middle eight are the eight taught weeks
         in seminar order; the two bookends are the statements the module opens
         on and closes on, which is what the first and last numerals are for. */
      'splash.rail.left.0': 'What the Qajars left',
      'splash.rail.left.1': 'The 1921 coup',
      'splash.rail.left.2': 'Reza Shah: reformer or despot',
      'splash.rail.left.3': 'The Allied occupation',
      'splash.rail.left.4': 'Musaddiq and the oil',
      'splash.rail.right.0': 'Muhammad Reza Shah',
      'splash.rail.right.1': 'The Left in Iran',
      'splash.rail.right.2': 'Gender and modernity',
      'splash.rail.right.3': 'Iran and the world',
      'splash.rail.right.4': 'And then 1979.',

      /* The essay title the syllabus sets for week two, then the instruction,
         then the red pen — which is the whole marking scheme in four lines. The
         question is genuinely the module's own, and the last line is the reason
         it is a fair one: both answers have been handed in before, and neither
         of them is the answer. No duration in it either, for the reason the
         Qajars' rails have none: the splash is the title card of a game
         somebody is about to play, not the syllabus of a course somebody has
         enrolled in. The eight taught weeks belong on the front door and in the
         readings shelf, where they are a fact. */
      'splash.tagline': 'Enlightened reformer, or misguided despot?<br>Choose one, then argue it properly.<br>I have marked both answers before.',

      /* The lobby. The engine's rail is nine boasts about a country; this one is
         the module's glossary, one concept a line, roughly in the order the
         seminars take them. The last line does not hand the story on, because
         there is nowhere to hand it: 1979 is this paper's own boundary, and the
         seminar stops just short of it rather than teaching it. */
      'lobby.rail.0': 'A coup with a Cossack brigade and a newspaperman',
      'lobby.rail.1': 'Conscription, the railway, and a state built in a hurry',
      'lobby.rail.2': 'Reza Shah: reformer, despot, or both at once',
      'lobby.rail.3': 'An occupation, and a bread riot in Tehran',
      'lobby.rail.4': 'Oil: nationalized in 1951, taken back in 1953',
      'lobby.rail.5': 'Land reform, and calling it a revolution',
      'lobby.rail.6': 'The Tudeh, and a left that ran out of time',
      'lobby.rail.7': 'Unveiling, and the argument it started',
      'lobby.rail.8': 'And 1979, which this paper stops just short of',

      /* The two-position version of the same line the splash makes: this is a
         subject on which everybody has a view and no two views agree. The
         Qajars got "they were incompetent"; the Pahlavis get a split, which is
         the honest report of the field. */
      'lobby.tagline': 'Everyone here has an opinion about the Pahlavis.<br>Usually two, and they contradict each other.',

      /* The board. Five lines down the left margin, in the engine's own shape:
         two nouns, two complaints, one punchline. The two nouns are the two
         words the module is actually about. The two complaints are the two sins
         the marking scheme names — reading 1979 backwards into the fifty years
         before it, and awarding the whole period to the British — which is what
         a Pahlavi seminar exists to take apart. */
      'board.rail.0': 'The state',
      'board.rail.1': 'Development',
      'board.rail.2': 'Hindsight',
      'board.rail.3': 'Foreign hands',
      'board.rail.4': 'And the oil, obviously.',

      /* The corner flourish, which the engine repeats on four screens. The
         show's word for itself is "same game"; the thing this edition has more
         of than the general one is infrastructure, which is also the Pahlavi
         boast. The railway is the signature of the period rather than a
         decoration of it — Clawson's "Knitting Iran together" is on the week-two
         shelf. */
      'common.corner.egos': 'Same throne.<br>Now with a railway.',

      /* The robots. The engine's four are a personality ladder — believes
         anything, stuck in the nineties, one enormous fact, has read everything.
         All four take their period's owners: a bagman agrees with whoever is
         paying, an attaché reads the dispatches and never the sources, a censor
         knows one enormous fact and will not be moved, and a planning officer
         has read every plan including the ones that failed. The censor keeps the
         engine's own description, which fits him better than it fits what it was
         written for. */
      'bot.easy': 'The Bagman',
      'bot.normal': 'The Attaché',
      'bot.hard': 'The Censor',
      'bot.brutal': 'The Planning Officer',
      'bot.easy.desc': 'Agrees with whoever is paying.',
      'bot.normal.desc': 'Reads the dispatches, never the sources.',
      'bot.brutal.desc': 'Has read every plan. Including the ones that failed.',

      'setup.tagline': 'Who has done the reading?',

      /* The one screen the module's assessment actually changes the name of: the
         show calls it a score, the seminar calls it a mark, and the syllabus
         calls the thing that produces it a single three-hour essay
         examination. */
      'results.title': 'Examination Mark',

      /* The lock, in the one place a student standing in the lobby will look.
         The engine's own label is "Start game" and this course cannot start one,
         so the button wears the front-door plate's words instead of doing
         nothing under them. Short because it is a button, and a `COURSE` key
         rather than a line written into the markup so that returning to MAIN
         restores "Start game" exactly as it was found. */
      'lobby.start': 'Coming soon'
    },
    fa: {
      'splash.rail.left.0': 'آنچه قاجارها گذاشتند',
      'splash.rail.left.1': 'کودتای ۱۲۹۹',
      'splash.rail.left.2': 'رضاشاه: مصلح یا مستبد',
      'splash.rail.left.3': 'اشغال ایران',
      'splash.rail.left.4': 'مصدق و نفت',
      'splash.rail.right.0': 'محمدرضاشاه',
      'splash.rail.right.1': 'چپ در ایران',
      'splash.rail.right.2': 'جنسیت و تجدد',
      'splash.rail.right.3': 'ایران و جهان',
      'splash.rail.right.4': 'و بعد، ۱۳۵۷.',

      'splash.tagline': 'مصلحِ روشن‌فکر، یا مستبدِ گمراه؟<br>یکی را انتخاب کن و درست از آن دفاع کن.<br>من هر دو جواب را قبلاً تصحیح کرده‌ام.',

      'lobby.rail.0': 'کودتایی با یک بریگاد قزاق و یک روزنامه‌نگار',
      'lobby.rail.1': 'خدمت اجباری، راه‌آهن، و دولتی که شتابان ساخته شد',
      'lobby.rail.2': 'رضاشاه: مصلح، مستبد، یا هر دو با هم',
      'lobby.rail.3': 'اشغال، و نان‌واژه‌ای در تهران',
      'lobby.rail.4': 'نفت: ملی شد در ۱۳۳۰، پس گرفته شد در ۱۳۳۲',
      'lobby.rail.5': 'اصلاحات ارضی، و نامیدنش به انقلاب',
      'lobby.rail.6': 'حزب توده، و چپی که وقت کم آورد',
      'lobby.rail.7': 'کشف حجاب، و جدالی که راه انداخت',
      'lobby.rail.8': 'و ۱۳۵۷، که این درس درست پیش از آن می‌ایستد',

      'lobby.tagline': 'همهٔ اینجا دربارهٔ پهلوی نظر دارند.<br>معمولاً دو نظر، و با هم در تناقض.',

      'board.rail.0': 'دولت',
      'board.rail.1': 'توسعه',
      'board.rail.2': 'حکمتِ بعد از واقعه',
      'board.rail.3': 'دستِ بیگانه',
      'board.rail.4': 'و البته نفت.',

      'common.corner.egos': 'همان تخت.<br>این بار با راه‌آهن.',

      'bot.easy': 'پول‌دارِ همراه',
      'bot.normal': 'وابستهٔ سفارت',
      'bot.hard': 'سانسورچی',
      'bot.brutal': 'افسر برنامه‌ریزی',
      'bot.easy.desc': 'با هر که پول می‌دهد موافق است.',
      'bot.normal.desc': 'گزارش‌ها را می‌خواند، منابع را نه.',
      'bot.brutal.desc': 'هر برنامهٔ عمرانی را خوانده. از جمله آن‌هایی که شکست خورد.',

      'setup.tagline': 'خواندهٔ این هفته کیست؟',

      'results.title': 'نمرهٔ امتحان',

      'lobby.start': 'به‌زودی'
    }
  };

  /* What the general edition says, captured before this file touches it, so the
     course can be put back exactly as it was found. Walked rather than listed:
     a key added to `COURSE` later and forgotten here would otherwise leak the
     course's words into MAIN permanently. */
  var ORIG = { en: {}, fa: {} };
  ['en', 'fa'].forEach(function (lang) {
    Object.keys(COURSE[lang]).forEach(function (key) {
      ORIG[lang][key] = BAGS[lang][key];
    });
  });

  /* Each screen's original wordmark and alt travel together. The clue-bar
     copies deliberately have empty alt text, which must remain empty. */
  var LOGO = { src: 'courses/pahlavis/assets/logo-wordmark-course.png?v=20260918-pahlavi-2', alt: 'JEOPARDY! The Pahlavis Edition' };
  var LOGO_ORIG = null;

  function swapWordmark(id) {
    var imgs = document.querySelectorAll('.logo');
    if (!imgs.length) return;
    var mine = id === 'pahlavis';
    if (!mine && id !== 'general') return;
    if (!LOGO_ORIG) {
      LOGO_ORIG = Array.prototype.map.call(imgs, function (img) {
        return { src: img.getAttribute('src'), alt: img.getAttribute('alt') };
      });
    }
    Array.prototype.forEach.call(imgs, function (img, i) {
      var was = LOGO_ORIG[i];
      if (mine) {
        img.setAttribute('src', LOGO.src);
        if (was.alt) img.setAttribute('alt', LOGO.alt);
      } else {
        img.setAttribute('src', was.src);
        if (was.alt) img.setAttribute('alt', was.alt);
      }
    });
  }

  /* The lobby and board rails are lists, and the engine builds them from the
     markup rather than from the string table. The markup has English in it, so
     the two lists on the Persian side are rewritten here, in place. Snapshot the
     English first: the restore path is the same walk with the other array. */
  var FA_ORIG = {};
  function mirror(selector, id, lines) {
    var nodes = document.querySelectorAll(selector);
    if (!nodes.length) return;
    Array.prototype.forEach.call(nodes, function (node, i) {
      if (!(selector in FA_ORIG)) FA_ORIG[selector] = [];
      if (!(i in FA_ORIG[selector])) FA_ORIG[selector][i] = node.innerHTML;
      var text = id === 'pahlavis' ? lines[i] : FA_ORIG[selector][i];
      if (text !== undefined) node.innerHTML = text;
    });
  }

  function pick(prefix, n) {
    var out = [];
    for (var i = 0; i < n; i++) out.push(COURSE.fa[prefix + i]);
    return out;
  }

  function mirrorRails(id) {
    mirror('#screen-lobby .rail-fa .rail-list li', id, pick('lobby.rail.', 9));
    var egos = (COURSE.fa['common.corner.egos'] || '').split('<br>');
    mirror('#screen-board .rail-fa .rail-list li', id, egos.concat(pick('board.rail.', 5)));
  }

  /* The lobby's two doors, and the whole of the lock as far as the lobby is
     concerned. This course has no questions, so pressing Start would deal an
     empty board; `app.js` refuses that in `startMatch` as well, and the refusal
     there is the one that has to be right, because a keyboard, a link or a future
     screen can all reach a match without coming through this button. What this
     does is tell the student before they press rather than after.

     Both doors end at `startMatch`, so disabling one and leaving the other live
     would only move the dead end. `#open-editions` stays up: it is the way back
     out of a course he did not mean to open. */
  var DOORS = ['go-setup', 'go-online'];

  function lockDoors(mine) {
    DOORS.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.disabled = !!mine;
    });
  }

  function wear(id) {
    var mine = id === 'pahlavis';
    ['en', 'fa'].forEach(function (lang) {
      var from = mine ? COURSE[lang] : ORIG[lang];
      var bag = BAGS[lang];
      Object.keys(COURSE[lang]).forEach(function (key) {
        if (from[key] === undefined) delete bag[key];
        else bag[key] = from[key];
      });
    });
    if (window.applyI18n) window.applyI18n();
    mirrorRails(id);
    swapWordmark(id);
    /* After `applyI18n`, because that is what the label is: `lobby.start` is
       rewritten to this course's words by the walk above, and the button's text
       node is a `data-i18n` span the walk just repainted. */
    lockDoors(mine);
    publish(mine);
    if (!mine) standDown();
  }

  /* ── Her voice ────────────────────────────────────────────────
     Every cue below is a clip that does not exist yet, and a caption that does.
     The names are what the engine says and what the bubble looks itself up with;
     the substitution to silence is at the foot of this section.

     The cue names carry the course because the professor does not: Stephanie
     teaches the Pahlavis and the Qajars, and a cue called `stephanie_welcome`
     would be one word for two modules. */

  /* The three cues the engine calls by name, plus the board handover it has a
     name for but does not currently call. Mapped rather than renamed in place:
     the engine owns `tannaz_*` and will keep saying it, and an unmapped one
     would play Tannaz's real recording under Stephanie's caption. */
  var CUE = {
    tannaz_opening_challenge: 'stephanie_pahlavis_welcome',
    tannaz_correct: 'stephanie_pahlavis_handover',
    tannaz_wager: 'stephanie_pahlavis_wager',
    tannaz_final: 'stephanie_pahlavis_final'
  };

  /* What she says when a verdict lands. `timeout` and `lockout` have their own
     lines rather than falling through to `wrong`, which is what the engine does
     when a pool is absent: a timeout is a different moment from a wrong answer
     and reads as one.
     Keyed the way the engine names a cue — the whole slug, not the number in
     front of it — because the bubble is handed the whole string. */
  var POOL = {
    right: [
      'stephanie_pahlavis_right_01_do_not_look_pleased',
      'stephanie_pahlavis_right_02_somebody_did_the_reading',
      'stephanie_pahlavis_right_03_one_is_almost_impressed',
      'stephanie_pahlavis_right_04_a_stopped_clock',
      'stephanie_pahlavis_right_05_mark_that_down_grudgingly',
      'stephanie_pahlavis_right_06_a_mind_in_there',
      'stephanie_pahlavis_right_07_also_the_easy_one',
      'stephanie_pahlavis_right_08_stop_fidgeting',
      'stephanie_pahlavis_right_09_a_book_singular',
      'stephanie_pahlavis_right_10_a_long_way_up',
      'stephanie_pahlavis_right_11_too_much_confidence',
      'stephanie_pahlavis_right_12_i_had_money_on_it',
      'stephanie_pahlavis_right_13_shall_i_get_you_a_sherry',
      'stephanie_pahlavis_right_14_your_tutor_would_be_surprised',
      'stephanie_pahlavis_right_15_right_occasionally',
      'stephanie_pahlavis_right_16_it_rarely_visits'
    ],
    wrong: [
      'stephanie_pahlavis_wrong_01_said_with_conviction',
      'stephanie_pahlavis_wrong_02_one_admires_the_certainty',
      'stephanie_pahlavis_wrong_03_so_very_sure',
      'stephanie_pahlavis_wrong_04_considered_reading',
      'stephanie_pahlavis_wrong_05_not_history_a_mood',
      'stephanie_pahlavis_wrong_06_confidently_though',
      'stephanie_pahlavis_wrong_07_oh_dear_no',
      'stephanie_pahlavis_wrong_08_your_seminar_group',
      'stephanie_pahlavis_wrong_09_never_been_given',
      'stephanie_pahlavis_wrong_10_hereditary',
      'stephanie_pahlavis_wrong_11_sit_with_it',
      'stephanie_pahlavis_wrong_12_pretend_we_did_not_hear',
      'stephanie_pahlavis_wrong_13_bold_baseless_and_brisk',
      'stephanie_pahlavis_wrong_14_a_publisher_is_weeping',
      'stephanie_pahlavis_wrong_15_hoped_you_would_surprise_me',
      'stephanie_pahlavis_wrong_16_do_not_explain_it'
    ],
    timeout: ['stephanie_pahlavis_timeout'],
    lockout: ['stephanie_pahlavis_lockout']
  };

  /* The beats the engine fires. Every one of these is a moment where the room
     has stopped and she can be heard; anything absent here is a beat she sits
     out. `boardIdle` is the round card and carries the round in its detail,
     which is the only place the engine says which half is starting. */
  var BEAT = {
    streak:   'stephanie_pahlavis_streak',
    comeback: 'stephanie_pahlavis_comeback',
    lead:     'stephanie_pahlavis_lead',
    win:      'stephanie_pahlavis_win',
    loss:     'stephanie_pahlavis_loss',
    leave:    'stephanie_pahlavis_leave'
  };

  var ROUND_START = {
    single: 'stephanie_pahlavis_start_single',
    double: 'stephanie_pahlavis_start_double'
  };

  /* ── What she says ────────────────────────────────────────────
     The register is the show's — smug, ironic, entirely unimpressed — moved
     out of Tehran and into an Oxford seminar room: the voice of a tutor who has
     marked this essay before, at length, in red. Same attitude as MAIN's host,
     different century, different idiom.

     This table is also the gate. A cue whose name is not a key here is not this
     host's to stand up for: `HostLayer` asks for a line, gets nothing, and
     leaves the floor empty rather than captioning her with the other show's
     words. So every name in `POOL`, `BEAT`, `ROUND_START` and `CUE` must appear
     below, and a name that appears below must be one she actually says. */
  var TEXT = {
    stephanie_pahlavis_welcome:
      'Welcome. Iranian history, 1905 to 1979: a constitution, a coup, a railway, an occupation, two shahs, and an oil industry that three governments believed they owned. We begin in 1921, because everything after it follows from what happened there.',
    stephanie_pahlavis_start_single:
      'Right. The board. Let us see what survived the reading.',
    stephanie_pahlavis_start_double:
      'Round two, and rather more money on the table. Do choose a subject you have actually opened a book about.',
    stephanie_pahlavis_handover:
      'Correct, well played. The board is yours.',
    stephanie_pahlavis_wager:
      'A Daily Double. You may wager. History suggests you will wager badly.',
    stephanie_pahlavis_final:
      'Final Jeopardy. One answer, one wager, and no opportunity whatsoever to hedge.',
    stephanie_pahlavis_streak:
      'Three in a row. One would almost call it a method.',
    stephanie_pahlavis_comeback:
      'A comeback. The twentieth century does permit those.',
    stephanie_pahlavis_lead:
      'You are ahead. Do try not to develop a theory about why.',
    stephanie_pahlavis_win:
      'And that is the game, and you have won it. I shall try not to let it colour my marking.',
    stephanie_pahlavis_loss:
      'And that is the game. You have lost. Usefully, one hopes.',
    stephanie_pahlavis_leave:
      'That is your hour. Do the reading. I dislike improvising the seminar on your behalf.',
    stephanie_pahlavis_timeout:
      'Time. The century has moved on without you.',
    stephanie_pahlavis_lockout:
      'And you have locked yourself out. Bold, in the circumstances.',

    stephanie_pahlavis_right_01_do_not_look_pleased:
      'Correct. Do try not to look so pleased with yourself.',
    stephanie_pahlavis_right_02_somebody_did_the_reading:
      'Ah. So somebody did the reading.',
    stephanie_pahlavis_right_03_one_is_almost_impressed:
      'Yes. One is almost impressed.',
    stephanie_pahlavis_right_04_a_stopped_clock:
      'Quite right. Even a stopped clock, and so on.',
    stephanie_pahlavis_right_05_mark_that_down_grudgingly:
      'Correct. I shall mark that down, grudgingly.',
    stephanie_pahlavis_right_06_a_mind_in_there:
      'Well. There is a mind in there after all.',
    stephanie_pahlavis_right_07_also_the_easy_one:
      'Yes, that is the answer. It is also the easy one.',
    stephanie_pahlavis_right_08_stop_fidgeting:
      'Correct. You may now stop fidgeting.',
    stephanie_pahlavis_right_09_a_book_singular:
      'Right. Somebody has read a book. Singular.',
    stephanie_pahlavis_right_10_a_long_way_up:
      'Correct. Do not let it go to your head; it is a long way up.',
    stephanie_pahlavis_right_11_too_much_confidence:
      'Yes. A sound answer, delivered with entirely too much confidence.',
    stephanie_pahlavis_right_12_i_had_money_on_it:
      'Correct. I had money on you not knowing that.',
    stephanie_pahlavis_right_13_shall_i_get_you_a_sherry:
      'Quite. Shall I get you a sherry?',
    stephanie_pahlavis_right_14_your_tutor_would_be_surprised:
      'Correct. Your tutor would be… surprised.',
    stephanie_pahlavis_right_15_right_occasionally:
      'Yes, well. Even you must be right occasionally.',
    stephanie_pahlavis_right_16_it_rarely_visits:
      'Correct. Try to remember the feeling; it rarely visits.',

    stephanie_pahlavis_wrong_01_said_with_conviction:
      'No. But said with real conviction. Alarming.',
    stephanie_pahlavis_wrong_02_one_admires_the_certainty:
      'Wrong. One does admire the certainty.',
    stephanie_pahlavis_wrong_03_so_very_sure:
      'No. And you were so very sure of it.',
    stephanie_pahlavis_wrong_04_considered_reading:
      'Wrong, I am afraid. Have you considered reading?',
    stephanie_pahlavis_wrong_05_not_history_a_mood:
      'No. That is not history, that is a mood.',
    stephanie_pahlavis_wrong_06_confidently_though:
      'Wrong. Confidently, though. That is something.',
    stephanie_pahlavis_wrong_07_oh_dear_no:
      'Oh dear. No.',
    stephanie_pahlavis_wrong_08_your_seminar_group:
      'Wrong. Your seminar group will never know.',
    stephanie_pahlavis_wrong_09_never_been_given:
      'No. That answer has never been given in this room before, which is not a compliment.',
    stephanie_pahlavis_wrong_10_hereditary:
      'Wrong. One can only hope the confidence is hereditary.',
    stephanie_pahlavis_wrong_11_sit_with_it:
      'No. Sit with it a moment.',
    stephanie_pahlavis_wrong_12_pretend_we_did_not_hear:
      'I shall pretend we did not hear that.',
    stephanie_pahlavis_wrong_13_bold_baseless_and_brisk:
      'No. Bold, baseless, and brisk. How very modern.',
    stephanie_pahlavis_wrong_14_a_publisher_is_weeping:
      'Wrong. Somewhere a publisher is weeping.',
    stephanie_pahlavis_wrong_15_hoped_you_would_surprise_me:
      'No. One had rather hoped you would surprise me.',
    stephanie_pahlavis_wrong_16_do_not_explain_it:
      'Wrong. Do not explain it to anyone. Ever.'
  };

  /* ── The album ────────────────────────────────────────────────
     The ten slots every course has, then the pack's own extras under their own
     names so a later feature can reach them without the file moving.

     An omitted slot is not silence. `makeEl` resolves a name with no slash in it
     against the engine's own `Web/assets/audio/`, so a cue this table leaves out
     plays MAIN's file of that name — inside a course match. Only the front door
     and the boot screen skip the map, and neither is where these slots are
     heard.

     The pack carries one 65-second piece and no separate title-card bed, so
     `splash_underscore` is that piece rather than a file cut from it. This is
     the one cue where the course is audibly not the pack's equal: `doneOpening`
     hands the underscore over to `menu_theme`, and two slot names over one file
     is a handover the name guard cannot see — it compares the names it is handed
     and finds them different, so the theme starts again from the top. A course
     with its own underscore, as the Qajars have, has no seam there. Cutting a
     bed out of this theme is the fix; it is a job for the pack. */
  var A = 'courses/pahlavis/assets/audio/';
  var SOUND = {
    splash_underscore:  A + 'course_theme',
    menu_theme:         A + 'course_theme',
    thinking_loop:      A + 'course_thinking',
    wager:              A + 'course_daily_double',
    final:              A + 'course_final',
    select:             A + 'course_select',
    correct:            A + 'course_correct',
    incorrect:          A + 'course_wrong'
  };

  /* Two slots the pack cannot fill.

     `armed` is the lock-in — the lamp going live when the buzzers open, and the
     Daily Double's holder being given the floor alone. The pack carries no sting
     for it: its only short cue is the 2.5-second category select, and a melodic
     sting that long would land over the thinking loop on every clue in the
     match, which is worse than the engine's own half-second tick. So MAIN's
     plays, which is the arrangement this course already has with `buzz`,
     `round1_bumper` and `round2_bumper`: the furniture of the game belongs to
     the show, and only the music belongs to the course.

     `course_winner` is staged and unmapped because there is no winner slot in
     the engine to point at — the results screen asks for `menu_theme`. */
  ['pahlavi_board_reveal', 'pahlavi_round_transition']
    .forEach(function (n) { SOUND[n] = A + n; });

  /* Her own recordings resolve to the placeholder, not to themselves.
     `app.js` looks a cue up in `EDITION_SOUND` and falls back to the cue *as a
     filename*, so a line written here and not yet in the booth would 404, give
     the bubble no duration, and close it on the next frame. The placeholder is
     a real file of the right length, so every written line is heard as silence
     and read as a caption until the booth catches up.

     Keyed off `TEXT` rather than written out again, because that table is
     already the gate on what she says: a line added there cannot arrive with a
     caption and no audio at all. */
  Object.keys(TEXT).forEach(function (n) { SOUND[n] = A + 'host_line_placeholder'; });

  function publish(mine) {
    var keys = ['HOST_CUE_MAP', 'HOST_VOICE', 'EDITION_SOUND'];
    /* Only ever unpublish our own three. Every course on the page runs this on
       the same `editionchange`, and the arriving course publishes after the
       departing one withdraws — so an unconditional delete here would land one
       handler later than Iran's publish and erase the globals it had just set,
       leaving its host silent and its music unmapped. Identity against our own
       `POOL` object is the ownership test: the three are ours if that one is. */
    if (!mine) {
      if (window.HOST_VOICE === POOL) keys.forEach(function (k) { delete window[k]; });
      return;
    }
    /* The map is applied before every other use of a cue name, so what
       `HostLayer` is handed is the name on the right, not the one the engine
       passed. That is why `TEXT` is keyed by the `stephanie_*` names. */
    window.HOST_CUE_MAP = CUE;
    window.HOST_VOICE = POOL;
    window.EDITION_SOUND = SOUND;
    /* After the swap, never before: `refresh` re-reads the map and re-resolves
       whatever is already on the floor. */
    if (window.Sound && window.Sound.refresh) window.Sound.refresh();
  }

  /* ── The floor ────────────────────────────────────────────────
     One sprite, no poses. She is cut from her character sheet in one resting
     stance, which is what a host wears when a cue has no pose of its own — and
     with no `poses` and no `pose` rule, every cue is such a cue. */
  window.HostLayer.register('pahlavis', {
    sprite: 'courses/pahlavis/assets/sprite-stephanie.png?v=20260918-pahlavi-1',
    lines: TEXT
  });

  /* ── The queue ────────────────────────────────────────────────
     The engine fires beats from inside the routines that are also cutting the
     audio, and the clip that would comment on a moment is often cued in the
     same tick as the moment that ends it. A beat handed straight to `Sound`
     is therefore cut before it is heard. So beats are queued and drained a
     beat-space apart, and the queue holds while a clip is speaking.

     This is the same queue Iran in World Politics runs, and it is here for the
     same reason: it is what makes a course host audible at all rather than
     audible only on verdicts. */
  var QUIET_MS = 900;
  var queue = [];
  var pending = null;
  var speaking = false;
  var holding = false;

  function standDown() {
    queue.length = 0;
    if (pending) { clearTimeout(pending); pending = null; }
    speaking = false;
    holding = false;
    if (window.HostLayer) window.HostLayer.hide();
  }

  function schedule() {
    if (pending || speaking || holding || !queue.length) return;
    pending = setTimeout(drain, QUIET_MS);
  }

  function drain() {
    pending = null;
    if (speaking || holding) return;
    var clip = queue.shift();
    if (!clip) return;
    play(clip);
  }

  function enqueue(clip) {
    if (!clip || queue.indexOf(clip) >= 0) return;
    queue.push(clip);
    schedule();
  }

  function play(clip) {
    speaking = true;
    if (window.Sound && TEXT[clip]) window.Sound.voice(clip, 0.9);
    /* No completion callback to hang off: the bubble is measured by the audio,
       which is silent, so the clip is held for the length of its own file and
       released when the engine says the next cue has landed. */
    setTimeout(function () { speaking = false; schedule(); }, 3400);
  }

  document.addEventListener('hostcue', function (e) {
    var name = e.detail && e.detail.name;
    if (!name) { standDown(); return; }
    if (TEXT[name]) speaking = true;
  });

  document.addEventListener('hostbeat', function (e) {
    /* The engine broadcasts beats on every edition, and this file is loaded on
       every one of them. Without the gate she would comment on the general
       edition's board, in a course she is not teaching. */
    if (window.getEdition && window.getEdition() !== 'pahlavis') return;
    var d = (e.detail || {});
    if (d.name === 'boardIdle') {
      enqueue(ROUND_START[d.round]);
      return;
    }
    /* A clue has opened over the board and the buzzers are about to: she stays
       quiet until the buzzers are open, so the queue cannot talk over a clue. */
    if (d.name === 'clueOpen') {
      holding = !!(d.detail && d.detail.race) || !!d.race;
      return;
    }
    if (d.name === 'buzzersOpen') { holding = false; schedule(); return; }
    enqueue(BEAT[d.name]);
  });

  document.addEventListener('editionchange', function (e) {
    wear(e.detail && e.detail.id);
  });

  /* The page may already be wearing this edition — an `?ed=pahlavis` load — in
     which case `editionchange` has been and gone before this file ran. */
  if (window.peekEdition && window.peekEdition() === 'pahlavis') wear('pahlavis');
})();
