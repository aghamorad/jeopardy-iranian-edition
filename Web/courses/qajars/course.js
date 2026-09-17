/* The Qajars — a course edition of the show.
 *
 * The module the bank and the skin are both cut from: The Qajars, University of
 * Oxford, Trinity term, one two-hour seminar a week for eight taught weeks. The
 * eight taught weeks run Russo-Persian wars, the ulama, army reform, reformist
 * thought, the Tobacco Protest, the Constitutional Revolution, the Great Game,
 * women in political life, in that order. They are the title card's middle eight
 * rails; the first and the last are the two statements the module opens and
 * closes on, which is why the numerals on that card are the arc's rather than a
 * week's. The concept vocabulary the module drills is the nine-line rail in the
 * lobby; the two things it marks down are the five-line rail on the board.
 * Nothing here is invented for the game — it is the seminar schedule wearing a
 * title card.
 *
 * Two rules this file obeys, because every course from here on has the same two
 * problems:
 *
 *   * **A professor's cues are namespaced by course.** Stephanie teaches this
 *     one and the Pahlavis, and the same is true of any tutor who turns up in
 *     more than one module. So her cues are `stephanie_qajars_*` here and will
 *     be `stephanie_pahlavis_*` there, and nothing is keyed to a bare
 *     `stephanie_*` that a second course could collide with.
 *   * **A host whose lines are written but not yet recorded still gets a clip.**
 *     The bubble on the floor is measured by the audio that is playing, so a cue
 *     with no file behind it is a bubble that closes on the next frame. While
 *     her voice was still only words, every cue below was mapped through
 *     `EDITION_SOUND` to a silent placeholder of the right length. Her lines are
 *     recorded now, so the album points at the clips themselves and the
 *     placeholders are unclaimed; they are kept for the next course that wants
 *     them.
 *
 * The folder name, the id and the `?ed=` value are one string, and the bank
 * globals are `COURSE_CLUES_<UPPER_SNAKE(folder)>` (+ `_FA`). To start another
 * course, copy the folder — not these lines — and fill it in.
 *
 * The Qajar wordmark replaces MAIN's emblem-bearing O with the uncrowned Lion
 * and Sun. `swapWordmark()` wears it beside the rails and restores MAIN's on
 * return; the Iran course keeps its own wordmark when that course is selected.
 */
(function () {
  'use strict';

  /* Registered after MAIN, and never before it. `general` registering first is
     what makes it the default; this show is the one opted into, not the one that
     opts the others in. */
  window.registerEdition({
    id: 'qajars',
    name: { en: 'The Qajars', fa: 'قاجار' },
    blurb: { en: 'A dynasty, week by week', fa: 'یک سلسله، هفته‌به‌هفته' },
    description: {
      en: 'A bankrupt dynasty between two empires, its shahs, its ulama, and one fatwa about tobacco. Eight weeks, and your essay still calls it decline.',
      fa: 'سلسله‌ای ورشکسته میان دو امپراتوری، شاهانش، علمایش و یک فتوای تنباکو. هشت هفته، و مقاله‌ات هنوز اسمش را انحطاط می‌گذارد.'
    },
    /* The Qajar circle art; the new key releases the old cached placeholder. */
    tile: 'courses/qajars/assets/tile-course.png?v=20260917-qajar-art-2',
    /* Only the host sprite is preloaded here; stage and wordmark are swapped
       through CSS and `swapWordmark()` after their files have landed. */
    art: [
      'courses/qajars/assets/sprite-stephanie.png?v=20260917-qajar-1'
    ],
    /* Who teaches it and where. Rendered on the selection circle, on the title
       card's imprint and in the lobby. No `code`: the module is a taught paper
       with a title and no number printed anywhere, and inventing an Oxford
       paper number to fill the slot would be a fact made up for a caption. */
    credit: {
      professor:   { en: 'Dr. Stephanie', fa: 'دکتر استفانی' },
      institution: { en: 'University of Oxford', fa: 'دانشگاه آکسفورد' }
    },
    banks: { en: window.COURSE_CLUES_QAJARS, fa: window.COURSE_CLUES_QAJARS_FA },
    /* The eight taught weeks' bibliography, cut from Dr Cronin's 2016 syllabus.
       See `data/readings.js` for what the syllabus prints that the shelf does
       not carry, and why. */
    readings: window.READINGS_QAJARS
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
      'splash.rail.left.0': 'The Qajar state',
      'splash.rail.left.1': 'The Russo-Persian wars',
      'splash.rail.left.2': 'The ulama & authority',
      'splash.rail.left.3': 'Army reform',
      'splash.rail.left.4': 'Reformist thought',
      'splash.rail.right.0': 'The Tobacco Protest',
      'splash.rail.right.1': 'The Constitutional Revolution',
      'splash.rail.right.2': 'Britain, Russia & the Great Game',
      'splash.rail.right.3': 'Women in political life',
      'splash.rail.right.4': 'Then Reza Khan.',

      /* The verdict first, then the turn against it, which is the whole
         marking scheme in four lines: a dynasty that argued with the nineteenth
         century for a hundred years and lost every exchange, and a tutor who
         will not let you write that sentence without interrogating it. The two
         sins the seminar punishes — reading the outcome back into the causes,
         and calling the outcome inevitable — are both committed by the first two
         lines, and "Or did it?" is the red pen. No duration in it either: the
         splash is the title card of a game somebody is about to play, not the
         syllabus of a course somebody has enrolled in. The eight taught weeks
         belong on the front door and in the readings shelf, where they are a
         fact. */
      'splash.tagline': 'A dynasty that lost every argument<br>it had with the nineteenth century.<br>Or did it? They were more complicated than you think.',

      /* The lobby. The engine's rail is nine boasts about a country; this one is
         the module's glossary, one concept a line, roughly in the order the
         seminars take them. The last line hands the story to the next course,
         which is true — the Pahlavis are what comes after. */
      'lobby.rail.0': 'A dynasty of tribes wearing a crown',
      'lobby.rail.1': 'The ulama: an authority the shah cannot tax',
      'lobby.rail.2': 'Gulistan and Turkmanchay, and the habit of losing',
      'lobby.rail.3': 'Reform from the top: Mirza Taqi Khan, then nobody',
      'lobby.rail.4': 'A fatwa by telegraph: the Tobacco Protest',
      'lobby.rail.5': 'A constitution, a Majles, and a shah who signs',
      'lobby.rail.6': 'Britain and Russia, playing in your courtyard',
      'lobby.rail.7': 'Women, the veil, and the public argument',
      'lobby.rail.8': 'Then Reza Khan, which is another course',

      'lobby.tagline': 'Everyone here has an opinion about the Qajars.<br>It is usually that they were incompetent.',

      /* The board. Five lines down the left margin, in the engine's own shape:
         two nouns, two complaints, one punchline. The two nouns are the two
         words the module is actually about. The two complaints are the two sins
         the marking scheme names — reading the outcome back into the causes,
         and calling the outcome inevitable — which are the same complaint
         wearing two hats, and are what a Qajar seminar is for. */
      'board.rail.0': 'Decline',
      'board.rail.1': 'Modernity',
      'board.rail.2': 'Hindsight',
      'board.rail.3': 'Inevitability',
      'board.rail.4': 'And the archive, actually.',

      /* The corner flourish, which the engine repeats on four screens. The
         show's word for itself is "same game"; the thing this edition has less
         of than the general one is cash, which is also the Qajar problem. */
      'common.corner.egos': 'Same throne.<br>Smaller treasury.',

      /* The robots. The engine's four are a personality ladder — believes
         anything, stuck in the nineties, one enormous fact, has read everything.
         All four take their period's owners: a courtier agrees with whoever
         spoke last, a consular official reads the dispatches and never the
         sources, a mujtahid knows one enormous fact and will not be moved, and
         the archivist has read everything. The mujtahid and the archivist keep
         the engine's own descriptions, which fit them better than they fit what
         they were written for. */
      'bot.easy': 'The Courtier',
      'bot.normal': 'The Consul',
      'bot.hard': 'The Mujtahid',
      'bot.brutal': 'The Archivist',
      'bot.easy.desc': 'Agrees with whoever spoke last.',
      'bot.normal.desc': 'Reads the dispatches, never the sources.',
      'bot.brutal.desc': 'Has read every treaty. In the original.',

      'setup.tagline': 'Who is presenting this week?',

      /* The one screen the module's assessment actually changes the name of: the
         show calls it a score, the seminar calls it a mark. */
      'results.title': 'Final Mark'
    },
    fa: {
      'splash.rail.left.0': 'دولت قاجار',
      'splash.rail.left.1': 'جنگ‌های ایران و روس',
      'splash.rail.left.2': 'علما و اقتدار',
      'splash.rail.left.3': 'اصلاح ارتش',
      'splash.rail.left.4': 'اندیشهٔ اصلاح',
      'splash.rail.right.0': 'نهضت تنباکو',
      'splash.rail.right.1': 'انقلاب مشروطه',
      'splash.rail.right.2': 'انگلیس، روسیه و بازی بزرگ',
      'splash.rail.right.3': 'زنان در زندگی سیاسی',
      'splash.rail.right.4': 'و بعد، رضاخان.',

      'splash.tagline': 'سلسله‌ای که هر بحثی<br>با قرن نوزدهم داشت، باخت.<br>یا واقعاً باخت؟ این‌ها پیچیده‌تر از آن بودند که فکر می‌کنید.',

      'lobby.rail.0': 'سلسله‌ای از ایلات با تاجی بر سر',
      'lobby.rail.1': 'علما: اقتداری که مالیات نمی‌دهد',
      'lobby.rail.2': 'گلستان و ترکمانچای، و عادتِ باختن',
      'lobby.rail.3': 'اصلاح از بالا: میرزا تقی‌خان، و بعد هیچ‌کس',
      'lobby.rail.4': 'فتوا با تلگراف: نهضت تنباکو',
      'lobby.rail.5': 'قانون اساسی، مجلس، و شاهی که امضا می‌کند',
      'lobby.rail.6': 'انگلیس و روسیه، مشغول بازی در حیاط تو',
      'lobby.rail.7': 'زنان، حجاب و جدال عمومی',
      'lobby.rail.8': 'و بعد رضاخان، که درس دیگری است',

      'lobby.tagline': 'همهٔ اینجا دربارهٔ قاجار نظر دارند.<br>نظرشان معمولاً این است که بی‌عرضه بودند.',

      'board.rail.0': 'انحطاط',
      'board.rail.1': 'تجدد',
      'board.rail.2': 'حکمتِ بعد از واقعه',
      'board.rail.3': 'ناگزیری',
      'board.rail.4': 'و البته آرشیو.',

      'common.corner.egos': 'همان تخت.<br>خزانهٔ خالی‌تر.',

      'bot.easy': 'درباری',
      'bot.normal': 'کنسول',
      'bot.hard': 'مجتهد',
      'bot.brutal': 'بایگان',
      'bot.easy.desc': 'با هر که آخر حرف بزند موافق است.',
      'bot.normal.desc': 'گزارش‌ها را می‌خواند، منابع را نه.',
      'bot.brutal.desc': 'همهٔ قراردادها را به زبان اصلی خوانده.',

      'setup.tagline': 'این هفته کی ارائه می‌دهد؟',

      'results.title': 'نمرهٔ نهایی'
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
  var LOGO = { src: 'courses/qajars/assets/logo-wordmark-course.png?v=20260917-qajar-art-3', alt: 'JEOPARDY! The Qajars Edition' };
  var LOGO_ORIG = null;

  function swapWordmark(id) {
    var imgs = document.querySelectorAll('.logo');
    if (!imgs.length) return;
    var mine = id === 'qajars';
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
      var text = id === 'qajars' ? lines[i] : FA_ORIG[selector][i];
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

  function wear(id) {
    var mine = id === 'qajars';
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
    publish(mine);
    if (!mine) standDown();
  }

  /* ── Her voice ────────────────────────────────────────────────
     Every cue below is a clip that does not exist yet, and a caption that does.
     The names are what the engine says and what the bubble looks itself up with;
     the substitution to silence is at the foot of this section.

     The cue names carry the course because the professor does not: Stephanie
     teaches the Qajars and the Pahlavis, and a cue called `stephanie_welcome`
     would be one word for two modules. */

  /* The three cues the engine calls by name, plus the board handover it has a
     name for but does not currently call. Mapped rather than renamed in place:
     the engine owns `tannaz_*` and will keep saying it, and an unmapped one
     would play Tannaz's real recording under Stephanie's caption. */
  var CUE = {
    tannaz_opening_challenge: 'stephanie_qajars_welcome',
    tannaz_correct: 'stephanie_qajars_handover',
    tannaz_wager: 'stephanie_qajars_wager',
    tannaz_final: 'stephanie_qajars_final'
  };

  /* What she says when a verdict lands. `timeout` and `lockout` have their own
     lines rather than falling through to `wrong`, which is what the engine does
     when a pool is absent: a timeout is a different moment from a wrong answer
     and reads as one.
     Keyed the way the engine names a cue — the whole slug, not the number in
     front of it — because the bubble is handed the whole string. */
  var POOL = {
    right: [
      'stephanie_qajars_right_01_do_not_look_pleased',
      'stephanie_qajars_right_02_somebody_did_the_reading',
      'stephanie_qajars_right_03_one_is_almost_impressed',
      'stephanie_qajars_right_04_a_stopped_clock',
      'stephanie_qajars_right_05_mark_that_down_grudgingly',
      'stephanie_qajars_right_06_a_mind_in_there',
      'stephanie_qajars_right_07_also_the_easy_one',
      'stephanie_qajars_right_08_stop_fidgeting',
      'stephanie_qajars_right_09_a_book_singular',
      'stephanie_qajars_right_10_a_long_way_up',
      'stephanie_qajars_right_11_too_much_confidence',
      'stephanie_qajars_right_12_i_had_money_on_it',
      'stephanie_qajars_right_13_shall_i_get_you_a_sherry',
      'stephanie_qajars_right_14_your_tutor_would_be_surprised',
      'stephanie_qajars_right_15_right_occasionally',
      'stephanie_qajars_right_16_it_rarely_visits'
    ],
    wrong: [
      'stephanie_qajars_wrong_01_said_with_conviction',
      'stephanie_qajars_wrong_02_one_admires_the_certainty',
      'stephanie_qajars_wrong_03_so_very_sure',
      'stephanie_qajars_wrong_04_considered_reading',
      'stephanie_qajars_wrong_05_not_history_a_mood',
      'stephanie_qajars_wrong_06_confidently_though',
      'stephanie_qajars_wrong_07_oh_dear_no',
      'stephanie_qajars_wrong_08_your_seminar_group',
      'stephanie_qajars_wrong_09_never_been_given',
      'stephanie_qajars_wrong_10_hereditary',
      'stephanie_qajars_wrong_11_sit_with_it',
      'stephanie_qajars_wrong_12_pretend_we_did_not_hear',
      'stephanie_qajars_wrong_13_bold_baseless_and_brisk',
      'stephanie_qajars_wrong_14_a_publisher_is_weeping',
      'stephanie_qajars_wrong_15_hoped_you_would_surprise_me',
      'stephanie_qajars_wrong_16_do_not_explain_it'
    ],
    timeout: ['stephanie_qajars_timeout'],
    lockout: ['stephanie_qajars_lockout']
  };

  /* The beats the engine fires. Every one of these is a moment where the room
     has stopped and she can be heard; anything absent here is a beat she sits
     out. `boardIdle` is the round card and carries the round in its detail,
     which is the only place the engine says which half is starting. */
  var BEAT = {
    streak:   'stephanie_qajars_streak',
    comeback: 'stephanie_qajars_comeback',
    lead:     'stephanie_qajars_lead',
    win:      'stephanie_qajars_win',
    loss:     'stephanie_qajars_loss',
    leave:    'stephanie_qajars_leave'
  };

  var ROUND_START = {
    single: 'stephanie_qajars_start_single',
    double: 'stephanie_qajars_start_double'
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
    stephanie_qajars_welcome:
      'Welcome to the Qajars. One bankrupt dynasty and two empires conducting their rivalry across your front garden. We shall begin with the wars, because losing a war is the quickest way to learn where you live.',
    stephanie_qajars_start_single:
      'Right. The board. Let us see what survived the reading.',
    stephanie_qajars_start_double:
      'Round two, and rather more money on the table. Do choose a subject you have actually opened a book about.',
    stephanie_qajars_handover:
      'Correct, well played. The board is yours.',
    stephanie_qajars_wager:
      'A Daily Double. You may wager. History suggests you will wager badly.',
    stephanie_qajars_final:
      'Final Jeopardy. One answer, one wager, and no opportunity whatsoever to hedge.',
    stephanie_qajars_streak:
      'Three in a row. One would almost call it a method.',
    stephanie_qajars_comeback:
      'A comeback. How thoroughly nineteenth-century of you.',
    stephanie_qajars_lead:
      'You are ahead. Do try not to develop a theory about why.',
    stephanie_qajars_win:
      'And that is the game, and you have won it. I shall try not to let it colour my marking.',
    stephanie_qajars_loss:
      'And that is the game. You have lost. Usefully, one hopes.',
    stephanie_qajars_leave:
      'That is your hour. Do the reading. I dislike improvising the seminar on your behalf.',
    stephanie_qajars_timeout:
      'Time. The nineteenth century has moved on without you.',
    stephanie_qajars_lockout:
      'And you have locked yourself out. Bold, in the circumstances.',

    stephanie_qajars_right_01_do_not_look_pleased:
      'Correct. Do try not to look so pleased with yourself.',
    stephanie_qajars_right_02_somebody_did_the_reading:
      'Ah. So somebody did the reading.',
    stephanie_qajars_right_03_one_is_almost_impressed:
      'Yes. One is almost impressed.',
    stephanie_qajars_right_04_a_stopped_clock:
      'Quite right. Even a stopped clock, and so on.',
    stephanie_qajars_right_05_mark_that_down_grudgingly:
      'Correct. I shall mark that down, grudgingly.',
    stephanie_qajars_right_06_a_mind_in_there:
      'Well. There is a mind in there after all.',
    stephanie_qajars_right_07_also_the_easy_one:
      'Yes, that is the answer. It is also the easy one.',
    stephanie_qajars_right_08_stop_fidgeting:
      'Correct. You may now stop fidgeting.',
    stephanie_qajars_right_09_a_book_singular:
      'Right. Somebody has read a book. Singular.',
    stephanie_qajars_right_10_a_long_way_up:
      'Correct. Do not let it go to your head; it is a long way up.',
    stephanie_qajars_right_11_too_much_confidence:
      'Yes. A sound answer, delivered with entirely too much confidence.',
    stephanie_qajars_right_12_i_had_money_on_it:
      'Correct. I had money on you not knowing that.',
    stephanie_qajars_right_13_shall_i_get_you_a_sherry:
      'Quite. Shall I get you a sherry?',
    stephanie_qajars_right_14_your_tutor_would_be_surprised:
      'Correct. Your tutor would be… surprised.',
    stephanie_qajars_right_15_right_occasionally:
      'Yes, well. Even you must be right occasionally.',
    stephanie_qajars_right_16_it_rarely_visits:
      'Correct. Try to remember the feeling; it rarely visits.',

    stephanie_qajars_wrong_01_said_with_conviction:
      'No. But said with real conviction. Alarming.',
    stephanie_qajars_wrong_02_one_admires_the_certainty:
      'Wrong. One does admire the certainty.',
    stephanie_qajars_wrong_03_so_very_sure:
      'No. And you were so very sure of it.',
    stephanie_qajars_wrong_04_considered_reading:
      'Wrong, I am afraid. Have you considered reading?',
    stephanie_qajars_wrong_05_not_history_a_mood:
      'No. That is not history, that is a mood.',
    stephanie_qajars_wrong_06_confidently_though:
      'Wrong. Confidently, though. That is something.',
    stephanie_qajars_wrong_07_oh_dear_no:
      'Oh dear. No.',
    stephanie_qajars_wrong_08_your_seminar_group:
      'Wrong. Your seminar group will never know.',
    stephanie_qajars_wrong_09_never_been_given:
      'No. That answer has never been given in this room before, which is not a compliment.',
    stephanie_qajars_wrong_10_hereditary:
      'Wrong. One can only hope the confidence is hereditary.',
    stephanie_qajars_wrong_11_sit_with_it:
      'No. Sit with it a moment.',
    stephanie_qajars_wrong_12_pretend_we_did_not_hear:
      'I shall pretend we did not hear that.',
    stephanie_qajars_wrong_13_bold_baseless_and_brisk:
      'No. Bold, baseless, and brisk. How very modern.',
    stephanie_qajars_wrong_14_a_publisher_is_weeping:
      'Wrong. Somewhere a publisher is weeping.',
    stephanie_qajars_wrong_15_hoped_you_would_surprise_me:
      'No. One had rather hoped you would surprise me.',
    stephanie_qajars_wrong_16_do_not_explain_it:
      'Wrong. Do not explain it to anyone. Ever.'
  };

  /* ── The album ────────────────────────────────────────────────
     The ten slots every course has, then the pack's own extras under their own
     names so a later feature can reach them without the file moving. The extras
     are the week stingers and the hard-thinking bed; nothing here plays the
     week stingers yet, and they are registered so that wiring one up is a line
     in the engine rather than a re-cut of the album. */
  var A = 'courses/qajars/assets/audio/';
  var SOUND = {
    menu_theme:         A + 'course_theme',
    splash_underscore:  A + 'course_splash',
    thinking_loop:      A + 'course_thinking',
    wager:              A + 'course_daily_double',
    final:              A + 'course_final',
    armed:              A + 'course_lock_in',
    select:             A + 'course_select',
    correct:            A + 'course_correct',
    incorrect:          A + 'course_wrong'
  };

  /* `course_winner` is staged and deliberately unmapped: the results screen asks
     for `menu_theme`, and there is no winner slot in the engine to point at. */
  ['qajar_thinking_hard', 'qajar_board_reveal', 'qajar_clue_reveal',
   'qajar_countdown', 'qajar_end_round',
   'qajar_week1_russo_iranian_wars', 'qajar_week2_ulama_authority',
   'qajar_week3_army_reform', 'qajar_week4_reformist_thought',
   'qajar_week5_tobacco_protest', 'qajar_week6_constitutional_revolution',
   'qajar_week7_britain_russia_great_game', 'qajar_week8_women_political_life'
  ].forEach(function (n) { SOUND[n] = A + n; });

  /* Her own recordings, keyed by their own names, so the map and the folder
     stay in step by inspection: the cue name is the filename. Taken from
     `TEXT` rather than written out again, because that table is already the
     gate on what she says — keying the album off it means a line added there
     cannot arrive with a caption and no voice. */
  Object.keys(TEXT).forEach(function (n) { SOUND[n] = A + n; });

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
  window.HostLayer.register('qajars', {
    sprite: 'courses/qajars/assets/sprite-stephanie.png?v=20260917-qajar-1',
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
    if (window.getEdition && window.getEdition() !== 'qajars') return;
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

  /* The page may already be wearing this edition — an `?ed=qajars` load — in
     which case `editionchange` has been and gone before this file ran. */
  if (window.peekEdition && window.peekEdition() === 'qajars') wear('qajars');
})();
