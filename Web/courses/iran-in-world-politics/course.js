/* Iran in World Politics — a course edition of the show.
 *
 * The module the bank and the skin are both cut from: IR4595, University of
 * St Andrews, School of International Relations, Semester 1. Twelve weeks, of
 * which ten are taught (week 6 is independent learning, week 12 revision), one
 * two-hour seminar a week, assessed 50% essay and 50% exam. The ten taught weeks
 * are the ten rails on the title card, in order; the concept vocabulary the
 * module drills is the nine-line rail in the lobby; and the two things it grades
 * on are the five-line rail on the board. Nothing here is invented for the game
 * — it is the seminar schedule wearing a title card.
 *
 * The folder name, the id and the `?ed=` value are one string, and the bank
 * globals are `COURSE_CLUES_<UPPER_SNAKE(folder)>` (+ `_FA`). To start another
 * course, copy the folder — not these lines — and fill it in.
 */
(function () {
  'use strict';

  /* Registered after MAIN, and never before it. `general` registering first is
     what makes it the default; this show is the one opted into, not the one that
     opts the others in. */
  window.registerEdition({
    id: 'iran-in-world-politics',
    name: { en: 'Iran in World Politics', fa: 'ایران در سیاست جهانی' },
    blurb: { en: 'A university module, week by week', fa: 'یک درس دانشگاهی، هفته‌به‌هفته' },
    description: {
      en: 'Revolution, war, velayat-e faqih, factions, sanctions, gender and minorities. Ten weeks, forty-two readings, and your hot take has somehow survived every footnote.',
      fa: 'انقلاب، جنگ، ولایت فقیه، جناح‌ها، تحریم، جنسیت و اقلیت‌ها؛ ده هفته، چهل‌ودو متن درسی، و نظر داغت به‌شکلی مشکوک از همهٔ پاورقی‌ها جان سالم به در برده است.'
    },
    tile: 'courses/iran-in-world-politics/assets/tile-course.png',
    hero: 'courses/iran-in-world-politics/assets/stage-backdrop-course.png',
    logo: 'courses/iran-in-world-politics/assets/logo-wordmark-course.png',
    /* Who teaches it and where. The engine renders this on the selection circle,
       on the title card's imprint and in the lobby, and the strings live here for
       the same reason the name and the blurb do: a course knows its own code, its
       professor and its university in both languages, and none of it is a string
       the engine has any business owning. `code` and the numerals inside it are
       Latin in both languages — it is a module code, not a word. */
    credit: {
      code: 'IR4595',
      professor:   { en: 'Dr. Eskandar', fa: 'دکتر اسکندر' },
      institution: { en: 'University of St Andrews', fa: 'دانشگاه سنت اندروز' }
    },
    banks: { en: window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS,
             fa: window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS_FA },
    /* This course's shelf, for the Reading List panel: the module's own reading,
       week by week. Loaded above this file, so it is already on the window. */
    readings: window.READINGS_IRAN_IN_WORLD_POLITICS
  });

  var BAGS = {
    en: window.I18N && window.I18N.en,
    fa: window.I18N && window.I18N.fa
  };
  if (!BAGS.en || !BAGS.fa) return;

  var COURSE = {
    en: {
      /* The title card. Left rail is weeks 1-5, right rail weeks 6-10 — the ten
         taught weeks in seminar order, which is also the order they are numbered
         in `course.css`. Week 6 and week 12 are not topics and do not appear. */
      'splash.rail.left.0': 'Revolution',
      'splash.rail.left.1': 'War',
      'splash.rail.left.2': 'Factions',
      'splash.rail.left.3': 'The Guards',
      'splash.rail.left.4': 'Foreign policy',
      'splash.rail.right.0': 'Axis of Resistance',
      'splash.rail.right.1': 'Sanctions',
      'splash.rail.right.2': 'Gender',
      'splash.rail.right.3': 'Minorities',
      'splash.rail.right.4': 'Iran at war',

      /* The module's own question, and the honest answer to it: ten weeks in, the
         seminar still has not settled whether the Islamic Republic works. The
         line used to end on a dare at the students' reading. It is a better title
         card ending on the question, because the question is the module. */
      'splash.tagline': 'Ten weeks on a state that shouldn’t work.<br>Does it? You’ll find out.',

      /* The lobby. The engine's rail is nine boasts about a country; this one is
         the module's glossary, one concept a line, in the order the seminars take
         them. Same nine lines, same length, different argument. */
      'lobby.rail.0': 'Hybrid regime: theocracy with a ballot box',
      'lobby.rail.1': 'Velayat-e faqih, and who reads it how',
      'lobby.rail.2': 'Factions that fight and never quite split',
      'lobby.rail.3': 'The Guards, the Basij, and the bonyads',
      'lobby.rail.4': 'The Sacred Defence, sold and remembered',
      'lobby.rail.5': 'Sanctions, snapback, and the resistance economy',
      'lobby.rail.6': 'The Axis of Resistance, patron and client',
      'lobby.rail.7': 'Gender, the veil, and the law',
      'lobby.rail.8': 'Minorities inside a unitary state',

      'lobby.tagline': 'Everyone here has an opinion about the Islamic Republic.<br>Most of you never opened the reading.',

      /* The board. Five lines down the left margin, in the engine's own shape:
         two nouns, two complaints, one punchline. The nouns are the two things
         the module actually teaches; the complaints are the two sins its marking
         scheme names, the hot take and the claim that begins "Iran is…" and
         cites nothing. The last line is the engine's joke with a seminar's noun
         in it — a small edition, and the marker's whole complaint in one line. */
      'board.rail.0': 'Theory',
      'board.rail.1': 'History',
      'board.rail.2': 'Hot takes',
      'board.rail.3': 'Overgeneralisations',
      'board.rail.4': 'Citations, obviously.',

      /* The corner flourish, which the engine repeats on four screens and which
         the Persian side of the board's rail also opens with. "Same game" is the
         show's word for itself; this edition's object is a state the module never
         manages to settle. Only the noun moves. */
      'common.corner.egos': 'Same state.<br>Bigger egos.',

      /* The robots. The engine's four are a personality ladder — believes
         anything, stuck in the nineties, one enormous fact, has read everything.
         Only the names move, bar the last description: "all forty-nine books" is
         a fact about the general edition's sources, and this edition has a
         reading list. The middle two descriptions still fit their new owners. */
      'bot.easy': 'The Fresher',
      'bot.normal': 'The Pundit',
      'bot.hard': 'The Realist',
      'bot.brutal': 'The Archivist',
      'bot.normal.desc': 'Reads the news, never the sources.',
      'bot.brutal.desc': 'Has read the whole reading list. Twice.',

      'setup.tagline': 'Who is presenting this week?',

      /* The one screen the module's assessment actually changes the name of: the
         show calls it a score, the seminar calls it a mark. */
      'results.title': 'Final Mark'
    },
    fa: {
      'splash.rail.left.0': 'انقلاب',
      'splash.rail.left.1': 'جنگ',
      'splash.rail.left.2': 'جناح‌ها',
      'splash.rail.left.3': 'پاسداران',
      'splash.rail.left.4': 'سیاست خارجی',
      'splash.rail.right.0': 'محور مقاومت',
      'splash.rail.right.1': 'تحریم',
      'splash.rail.right.2': 'جنسیت',
      'splash.rail.right.3': 'اقلیت‌ها',
      'splash.rail.right.4': 'ایران در جنگ',

      'splash.tagline': 'ده هفته دربارهٔ دولتی که نباید کار کند.<br>کار می‌کند؟ خودت می‌فهمی.',

      'lobby.rail.0': 'رژیم هیبرید: تئوکراسی با صندوق رأی',
      'lobby.rail.1': 'ولایت فقیه، و اینکه چه کسی چطور می‌خواندش',
      'lobby.rail.2': 'جناح‌هایی که می‌جنگند و هرگز کامل جدا نمی‌شوند',
      'lobby.rail.3': 'سپاه، بسیج و بنیادها',
      'lobby.rail.4': 'دفاع مقدس، تبلیغ‌شده و به‌یادمانده',
      'lobby.rail.5': 'تحریم، اسنپ‌بک و اقتصاد مقاومتی',
      'lobby.rail.6': 'محور مقاومت، حامی و نیابتی',
      'lobby.rail.7': 'جنسیت، حجاب و قانون',
      'lobby.rail.8': 'اقلیت‌ها در دولت بسیط',

      'lobby.tagline': 'همهٔ اینجا دربارهٔ جمهوری اسلامی نظر دارند.<br>بیشترتان هنوز منابع را باز نکرده‌اید.',

      'board.rail.0': 'نظریه',
      'board.rail.1': 'تاریخ',
      'board.rail.2': 'نظرهای سرسری',
      'board.rail.3': 'تعمیم‌های بی‌دلیل',
      'board.rail.4': 'و البته ارجاع و منبع.',

      'common.corner.egos': 'همان دولت.<br>خودپسندیِ بیشتر.',

      'bot.easy': 'سال‌اولی',
      'bot.normal': 'کارشناس',
      'bot.hard': 'واقع‌گرا',
      'bot.brutal': 'بایگان',
      'bot.normal.desc': 'خبر می‌خواند، منبع نه.',
      'bot.brutal.desc': 'همهٔ فهرست منابع را خوانده. دو بار.',

      'setup.tagline': 'این هفته کی ارائه می‌دهد؟',

      'results.title': 'نمرهٔ نهایی'
    }
  };

  /* The engine's own wording, captured before the first patch overwrites any of
     it. Nothing in `COURSE` may go into the table without its original landing
     here first, or the general edition could never be handed its copy back. */
  var ORIG = { en: {}, fa: {} };
  Object.keys(COURSE).forEach(function (lang) {
    Object.keys(COURSE[lang]).forEach(function (key) {
      ORIG[lang][key] = BAGS[lang][key];
    });
  });

  /* The wordmark. One `<img>` per screen, five of them, each with `src` written
     into the markup and nothing in `app.js` touching it — so an edition cannot
     reach it from the string table and has to set the attribute itself. Held the
     same way as the strings: the engine's own path and alt are captured on the
     first wear, and handed back when the other edition is chosen.

     `alt` travels with `src`, because the two decorative copies in the clue bars
     carry an empty one on purpose — replacing it would put the show's name back
     into a screen reader's read of a question. */
  var LOGO = { src: 'courses/iran-in-world-politics/assets/logo-wordmark-course.png', alt: 'JEOPARDY! Iran in World Politics Edition' };
  var LOGO_ORIG = null;

  function swapWordmark(id) {
    var imgs = document.querySelectorAll('.logo');
    if (!imgs.length) return;
    if (!LOGO_ORIG) {
      LOGO_ORIG = Array.prototype.map.call(imgs, function (img) {
        return { src: img.getAttribute('src'), alt: img.getAttribute('alt') };
      });
    }
    var mine = id === 'iran-in-world-politics';
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

  /* The Persian rail beside each English one the table can reach is literal
     markup — no `data-i18n`, so nothing in the string table ever lands on it —
     and both therefore have to be fed by hand. Two rails, one difference that
     matters: the lobby's is the nine course lines, but the board's prefaces its
     five with the two lines of the corner flourish, so its mapping starts two
     entries in. Left alone, a course screen would read as the module down one
     margin and as general trivia down the other, in both languages.

     The lines are read back out of the table this edition has just written, so a
     rail and the node standing beside it can never disagree. Restoring is by
     index off the engine's own lines, captured the first time a rail is touched. */
  var FA_ORIG = {};

  function mirror(selector, id, lines) {
    var items = document.querySelectorAll(selector);
    if (!items.length) return;
    if (!FA_ORIG[selector]) {
      FA_ORIG[selector] = Array.prototype.map.call(items, function (li) { return li.innerHTML; });
    }
    var mine = id === 'iran-in-world-politics';
    Array.prototype.forEach.call(items, function (li, i) {
      var line = mine ? lines[i] : FA_ORIG[selector][i];
      if (line !== undefined) li.innerHTML = line;
    });
  }

  function mirrorRails(id) {
    var pick = function (prefix, n) {
      var out = [];
      for (var i = 0; i < n; i++) out.push(COURSE.fa[prefix + i]);
      return out;
    };
    var egos = (COURSE.fa['common.corner.egos'] || '').split('<br>');
    mirror('#screen-lobby .rail-fa .rail-list li', id, pick('lobby.rail.', 9));
    mirror('#screen-board .rail-fa .rail-list li', id, egos.concat(pick('board.rail.', 5)));
  }

  /* One string table serves both shows, so this edition's voice is worn rather
     than written: put on when a player picks this tile, taken off when they pick
     the other one. `applyI18n` re-renders every `data-i18n` node from whatever
     the table currently holds, which is what makes the swap take effect without
     a reload.

     Driven by the registry's event rather than by a read at load: this script
     runs before `app.js` boots, so at load time no edition has been chosen yet
     and `document.documentElement` carries no `data-edition` to read. The boot
     always dispatches — `setEdition` compares against a null current — so the
     listener fires once during startup, before the first paint. */
  function wear(id) {
    var mine = id === 'iran-in-world-politics';
    Object.keys(COURSE).forEach(function (lang) {
      var bag = BAGS[lang];
      var src = mine ? COURSE[lang] : ORIG[lang];
      Object.keys(src).forEach(function (key) {
        if (src[key] === undefined) { delete bag[key]; } else { bag[key] = src[key]; }
      });
    });
    if (window.applyI18n) window.applyI18n();
    mirrorRails(id);
    swapWordmark(id);
    publish(mine);
    if (!mine) standDown();
  }

  /* ── The professor ─────────────────────────────────────────────
   * The general edition's host is the engine's own voice and the engine carries
   * it in its own table. This edition replaces her with a man who was recorded
   * saying twenty-seven specific things, and it does that from outside, through
   * the three globals the engine reads on every draw: `HOST_CUE_MAP`, which
   * renames a cue at the moment it is played; `HOST_VOICE`, which replaces a
   * whole pool of verdict lines; and `hostbeat`, which is the engine announcing
   * a moment it cannot name rather than a line it wants said.
   *
   * All three are published live rather than merged once, because one build
   * carries both shows: whichever edition is on screen has to be the one
   * talking, and a merge made at boot would hand the professor the room
   * permanently, general edition and all. `publish` puts them on and takes them
   * off with the edition; absent them the engine is exactly the app it always
   * was.
   */

  /* The three cues the engine plays from its own host's script, renamed. Each is
     a moment this edition has its own words for: the title card, the Daily
     Double, and Final Jeopardy. */
  var CUE = {
    opening_challenge: 'prof_01_professor_welcome',
    host_wager:        'prof_12_daily_double',
    host_final:        'prof_13_final_jeopardy'
  };

  /* The four verdict kinds the engine draws. `right` and `wrong` each hold the
     two takes he recorded; `timeout` and `lockout` hold one apiece. The engine
     falls back to `wrong` for anything this table does not cover, so the four
     entries are the whole of what a verdict can ask for. */
  var POOL = {
    right:   ['prof_04_correct_annoyingly_so', 'prof_05_correct_surprised'],
    wrong:   ['prof_06_wrong_confident', 'prof_07_wrong_reading'],
    timeout: ['prof_08_timeout'],
    lockout: ['prof_09_close_call']
  };

  /* The lines the engine cannot ask for, because it does not know they exist.
     These wait behind whatever the verdict is already saying — see the queue
     below for why that has to be a wait rather than a play. */
  var BEAT = {
    streak:   'prof_10_three_in_a_row',
    comeback: 'prof_11_comeback',
    lead:     'prof_24_score_lead',
    win:      'prof_25_game_win',
    loss:     'prof_26_game_loss',
    leave:    'prof_27_class_dismissed'
  };

  /* Which of the two opening lines a fresh board gets. The Final has no entry on
     purpose: `13_final_jeopardy` is already saying that moment, and a round card
     over the top of it would be the same speech twice. */
  var ROUND_START = { single: 'prof_02_start_game', double: 'prof_03_choose_topic' };

  /* Two tiers, first match wins. The top tier is the board itself: every one of
     this course's 138 board categories, English and Persian, named exactly as the
     bank spells it (and lower-cased, because the caller lower-cases the name) and
     mapped to the week it belongs to. Mapped on 2026-09-14 by gpt-5.6-terra over
     the built bank, then read against the clues; two rows were overridden by hand
     and the three Final categories are left out on purpose. A pun name carries no
     subject word, which is why the older tier below never reached most of them.
     The tier below is that older match on subject words — most specific first,
     because `iraq` has to settle the Iran-Iraq war before the bare `war` further
     down can claim it, and `resistance economy` before either half of it pulls the
     category apart — and it stays as the fallback for any category not named above.
     A category that matches neither tier still gets no introduction, which is the
     right failure: the professor has nothing to say about a subject he does not
     teach. */
  var THEME = [
    ['who wants to be a mostazaf?', 'prof_14_topic_revolution'],
    ['ولایت به شرط چاقو',   'prof_14_topic_revolution'],
    ['neither east nor best', 'prof_18_topic_foreign_policy'],
    ['نه شرقی، نه غربی، فقط فرعی', 'prof_18_topic_foreign_policy'],
    ['vetting for godot',   'prof_16_topic_factional_politics'],
    ['استصوابیِ بی‌جوابی',  'prof_16_topic_factional_politics'],
    ['all the president\'s mullahs', 'prof_16_topic_factional_politics'],
    ['صندوق از ما، کلید از شما', 'prof_16_topic_factional_politics'],
    ['dr. strange-waltz',   'prof_18_topic_foreign_policy'],
    ['کیک زرد و چای قندپهلو', 'prof_18_topic_foreign_policy'],
    ['the invisible hand of deterrence', 'prof_23_topic_iran_at_war'],
    ['شوک‌درمانی با چاشنی باروت', 'prof_23_topic_iran_at_war'],
    ['provincial matters',  'prof_22_topic_minorities'],
    ['استان‌بازی با دم شیر', 'prof_22_topic_minorities'],
    ['tongue tied in tehran', 'prof_22_topic_minorities'],
    ['مشق وحدت با لهجه غلیظ', 'prof_22_topic_minorities'],
    ['maximum pressure, minimum wage', 'prof_20_topic_sanctions'],
    ['فشار حداکثری، جیب حداقلی', 'prof_20_topic_sanctions'],
    ['gando with the wind', 'prof_20_topic_sanctions'],
    ['دور زدن با چرخ پنچر', 'prof_20_topic_sanctions'],
    ['a veil of two cities', 'prof_21_topic_gender_politics'],
    ['تفکیک به نرخ روز',    'prof_21_topic_gender_politics'],
    ['fatwas & fallopian tubes', 'prof_21_topic_gender_politics'],
    ['فرزند کمتر، فتوای بیشتر', 'prof_21_topic_gender_politics'],
    ['white revolution, red ink', 'prof_14_topic_revolution'],
    ['تهدیگِ انقلاب سفید',  'prof_14_topic_revolution'],
    ['five stages of grief & revolution', 'prof_14_topic_revolution'],
    ['چله به چله تا سقوط',  'prof_14_topic_revolution'],
    ['romancing the revolution', 'prof_14_topic_revolution'],
    ['مدینه فاضله با اعمال شاقه', 'prof_14_topic_revolution'],
    ['east of eden, west of reason', 'prof_18_topic_foreign_policy'],
    ['نه شرقی، نه غربی، فقط پکن', 'prof_18_topic_foreign_policy'],
    ['post-war distress syndrome', 'prof_15_topic_iran_iraq_war'],
    ['سنگر دیروز، سهمیه امروز', 'prof_15_topic_iran_iraq_war'],
    ['minority retort',     'prof_15_topic_iran_iraq_war'],
    ['صلیب در جبهه، ناقوس در سنگر', 'prof_15_topic_iran_iraq_war'],
    ['subcontract killers', 'prof_17_topic_irgc_political_economy'],
    ['خصولتی‌های سر گردنه', 'prof_17_topic_irgc_political_economy'],
    ['zeal or no zeal',     'prof_19_topic_axis_of_resistance'],
    ['چریکی با حقوق بازنشستگی', 'prof_19_topic_axis_of_resistance'],
    ['heroic flexibility exercises', 'prof_18_topic_foreign_policy'],
    ['نرمش قهرمانانه در وقت اضافه', 'prof_18_topic_foreign_policy'],
    ['saving private assad', 'prof_19_topic_axis_of_resistance'],
    ['سوریه به نرخ حرم',    'prof_19_topic_axis_of_resistance'],
    ['pasdaran of the galaxy', 'prof_17_topic_irgc_political_economy'],
    ['کاریزمای بی‌درجه',    'prof_17_topic_irgc_political_economy'],
    ['boots, beards & banisadr', 'prof_17_topic_irgc_political_economy'],
    ['ارتش با کراوات، سپاه با صلوات', 'prof_17_topic_irgc_political_economy'],
    ['proxies and cons',    'prof_19_topic_axis_of_resistance'],
    ['نیابت در حد تعارف',   'prof_19_topic_axis_of_resistance'],
    ['the tail wags the tehran', 'prof_19_topic_axis_of_resistance'],
    ['دمی که شیر را می‌جنباند', 'prof_19_topic_axis_of_resistance'],
    ['the wheels on the bus go halal', 'prof_21_topic_gender_politics'],
    ['عقب‌نشینیِ خواهران',  'prof_21_topic_gender_politics'],
    ['divide & cartograph', 'prof_22_topic_minorities'],
    ['تفرقه‌انداز و نقشه بکش', 'prof_22_topic_minorities'],
    ['sanctions and sensibility', 'prof_21_topic_gender_politics'],
    ['سفره بی‌ریال، تحریمِ باکلاس', 'prof_21_topic_gender_politics'],
    ['devotion & devices',  'prof_21_topic_gender_politics'],
    ['تن به تن با تنظیم خانواده', 'prof_21_topic_gender_politics'],
    ['let them eat arms',   'prof_18_topic_foreign_policy'],
    ['مصلحت بر وزن منفعت',  'prof_18_topic_foreign_policy'],
    ['highway to damascus', 'prof_19_topic_axis_of_resistance'],
    ['میدانِ بی‌دیپلماسی',  'prof_19_topic_axis_of_resistance'],
    ['the janus of tehran', 'prof_16_topic_factional_politics'],
    ['دو رو در یک اقلیم',   'prof_16_topic_factional_politics'],
    ['from tyre to tehran', 'prof_19_topic_axis_of_resistance'],
    ['از صور تا پاستور',    'prof_19_topic_axis_of_resistance'],
    ['the pope of populism', 'prof_14_topic_revolution'],
    ['پوپولیسم با ذکر صلوات', 'prof_14_topic_revolution'],
    ['ramhormoz and confused', 'prof_15_topic_iran_iraq_war'],
    ['جنگ‌زده با سسِ تندِ آبادان', 'prof_15_topic_iran_iraq_war'],
    ['one nation under persian', 'prof_22_topic_minorities'],
    ['هم‌زبانی به زورِ باستانی', 'prof_22_topic_minorities'],
    ['rising lions, falling missiles', 'prof_23_topic_iran_at_war'],
    ['شیر خیزان در تله موشک', 'prof_23_topic_iran_at_war'],
    ['the socialization network', 'prof_18_topic_foreign_policy'],
    ['جامعه‌پذیری با اعمال شاقه', 'prof_18_topic_foreign_policy'],
    ['aligned, sealed, delivered', 'prof_18_topic_foreign_policy'],
    ['عدم تعهد به نیت معامله', 'prof_18_topic_foreign_policy'],
    ['pride and precarity', 'prof_20_topic_sanctions'],
    ['پراید به نرخ طلا',    'prof_20_topic_sanctions'],
    ['the bazaar and the barricade', 'prof_14_topic_revolution'],
    ['حجره‌های پای منبر',   'prof_14_topic_revolution'],
    ['ballots and barricades', 'prof_16_topic_factional_politics'],
    ['صندوقِ پر از بنزین',  'prof_16_topic_factional_politics'],
    ['crossing the chador line', 'prof_21_topic_gender_politics'],
    ['جراحی به شرط فتوا',   'prof_21_topic_gender_politics'],
    ['diplomacy in heels',  'prof_18_topic_foreign_policy'],
    ['مذاکرات روی بندِ رخت', 'prof_18_topic_foreign_policy'],
    ['the right to the seat', 'prof_21_topic_gender_politics'],
    ['خط ویژه خواهران',     'prof_21_topic_gender_politics'],
    ['where is my vote, dude?', 'prof_16_topic_factional_politics'],
    ['رأی من کو، پالتوی من کو', 'prof_16_topic_factional_politics'],
    ['a bridge too charismatic', 'prof_17_topic_irgc_political_economy'],
    ['سربند یا زهرا با بی‌سیمِ روسی', 'prof_17_topic_irgc_political_economy'],
    ['tie-dyed in the revolution', 'prof_14_topic_revolution'],
    ['کراواتی‌های کاخ‌نشین', 'prof_14_topic_revolution'],
    ['poison chalice, empty palace', 'prof_15_topic_iran_iraq_war'],
    ['جام زهر در سنگرِ خودی', 'prof_15_topic_iran_iraq_war'],
    ['lost in misrepresentation', 'prof_18_topic_foreign_policy'],
    ['سلام گرگ، لبخند روباه', 'prof_18_topic_foreign_policy'],
    ['proxy music',         'prof_19_topic_axis_of_resistance'],
    ['پروکسی بدون فیلترشکن', 'prof_19_topic_axis_of_resistance'],
    ['assembly required',   'prof_14_topic_revolution'],
    ['خبرگانِ بدون ضمانت',  'prof_14_topic_revolution'],
    ['strike while the oil is cold', 'prof_14_topic_revolution'],
    ['اعتصاب با طعم نفت خام', 'prof_14_topic_revolution'],
    ['the grammar of resistance', 'prof_19_topic_axis_of_resistance'],
    ['صرف و نحوِ استکبارستیزی', 'prof_19_topic_axis_of_resistance'],
    ['strait outta yemen',  'prof_19_topic_axis_of_resistance'],
    ['باب‌المندب با طعم پهپاد', 'prof_19_topic_axis_of_resistance'],
    ['a tale of two peripheries', 'prof_22_topic_minorities'],
    ['مرکزگریزی با لهجه محلی', 'prof_22_topic_minorities'],
    ['austerity at ground zero', 'prof_20_topic_sanctions'],
    ['جراحی اقتصادی در سایه اتم', 'prof_20_topic_sanctions'],
    ['bridges of khuzestan county', 'prof_15_topic_iran_iraq_war'],
    ['جاده خاکی به بهشت',   'prof_15_topic_iran_iraq_war'],
    ['no country for old khans', 'prof_22_topic_minorities'],
    ['خان‌بازی در وقت اضافه', 'prof_22_topic_minorities'],
    ['whose regime is it anyway?', 'prof_16_topic_factional_politics'],
    ['بداهه‌نوازی در بن‌بست', 'prof_16_topic_factional_politics'],
    ['the second step shuffle', 'prof_16_topic_factional_politics'],
    ['گام دوم با دنده عقب', 'prof_16_topic_factional_politics'],
    ['foucault around and find out', 'prof_14_topic_revolution'],
    ['عشق در روزگارِ مرگ بر آمریکا', 'prof_14_topic_revolution'],
    ['neither east nor western union', 'prof_18_topic_foreign_policy'],
    ['نه شرقی، نه غربی، فقط حواله', 'prof_18_topic_foreign_policy'],
    ['guerrillas in our midst', 'prof_14_topic_revolution'],
    ['از بعلبک تا جماران',  'prof_14_topic_revolution'],
    ['khatam and command',  'prof_17_topic_irgc_political_economy'],
    ['مهندسیِ سود و صلوات', 'prof_17_topic_irgc_political_economy'],
    ['the chador bomb squad', 'prof_21_topic_gender_politics'],
    ['تار مو و گره کور',    'prof_21_topic_gender_politics'],
    ['eggs, stones & dollar loans', 'prof_20_topic_sanctions'],
    ['تخم‌مرغ با عیار دلار', 'prof_20_topic_sanctions'],
    ['eighth imam, first victory', 'prof_15_topic_iran_iraq_war'],
    ['ثامن‌الائمه و شکستِ حصر', 'prof_15_topic_iran_iraq_war'],
    ['highway to jerusalem', 'prof_15_topic_iran_iraq_war'],
    ['طریق‌القدس با بلیت بستان', 'prof_15_topic_iran_iraq_war'],
    ['bulldozers in the bog', 'prof_15_topic_iran_iraq_war'],
    ['سنگر در مرداب، پل روی آب', 'prof_15_topic_iran_iraq_war'],
    ['a faction of seconds', 'prof_15_topic_iran_iraq_war'],
    ['مرز به شرط دعوا',     'prof_15_topic_iran_iraq_war'],
    ['no king for a day',   'prof_14_topic_revolution'],
    ['تاج‌تکانی در نجف',    'prof_14_topic_revolution'],
    ['turban renewal',      'prof_14_topic_revolution'],
    ['عمامه در ترازوی قدرت', 'prof_14_topic_revolution'],
    ['expediency is the best policy', 'prof_14_topic_revolution'],
    ['مصلحت بالاتر از شریعت', 'prof_14_topic_revolution'],
    ['guardian angles',     'prof_14_topic_revolution'],
    ['نظارت مشروطه یا ولایت مطلقه', 'prof_14_topic_revolution'],
    ['survey says: aqvam',  'prof_22_topic_minorities'],
    ['قوم و خویشِ سرشماری', 'prof_22_topic_minorities'],
    ['lur lur land',        'prof_22_topic_minorities'],
    ['لر و لور به روایت آمار', 'prof_22_topic_minorities'],
    ['waltzing with atoms', 'prof_18_topic_foreign_policy'],
    ['رقص والس با اورانیوم', 'prof_18_topic_foreign_policy'],
    ['shock therapy, no chaser', 'prof_20_topic_sanctions'],
    ['شوک‌درمانیِ بدون بیهوشی', 'prof_20_topic_sanctions'],
    ['pharmaceutical ill-will', 'prof_20_topic_sanctions'],
    ['نسخه پیچیده برای بیمار', 'prof_20_topic_sanctions'],
    ['panic at the grocery', 'prof_20_topic_sanctions'],
    ['سفره آب‌رفته',        'prof_20_topic_sanctions'],
    ['two is a crowd',      'prof_21_topic_gender_politics'],
    ['فرزند کمتر، زندگی بهتر', 'prof_21_topic_gender_politics'],
    ['health houses of cards', 'prof_21_topic_gender_politics'],
    ['خانه‌به‌خانه با بهورز', 'prof_21_topic_gender_politics'],
    ['shrine on you crazy diamond', 'prof_19_topic_axis_of_resistance'],
    ['حرم تا حلب',          'prof_19_topic_axis_of_resistance'],
    ['kremlin in the coalition', 'prof_19_topic_axis_of_resistance'],
    ['سوخو با مهر قم',      'prof_19_topic_axis_of_resistance'],
    ['shadow commander in chief', 'prof_19_topic_axis_of_resistance'],
    ['سایه در میدان',       'prof_19_topic_axis_of_resistance'],
    ['discourse with the devil', 'prof_19_topic_axis_of_resistance'],
    ['گفتمان با چاشنی مقاومت', 'prof_19_topic_axis_of_resistance'],
    ['assembly required ii', 'prof_14_topic_revolution'],
    ['ولایت در صحن علنی',   'prof_14_topic_revolution'],
    ['deputy of discontent', 'prof_14_topic_revolution'],
    ['قائم‌مقامِ در حاشیه', 'prof_14_topic_revolution'],
    ['prime ministers anonymous', 'prof_14_topic_revolution'],
    ['حذفِ صندلیِ نخست‌وزیر', 'prof_14_topic_revolution'],
    ['linz with a twist',   'prof_16_topic_factional_politics'],
    ['خوان لینز در جمهوری اسلامی', 'prof_16_topic_factional_politics'],
    ['crude awakenings',    'prof_14_topic_revolution'],
    ['شیرِ نفت در دست کارگر', 'prof_14_topic_revolution'],
    ['komiteh to memory',   'prof_14_topic_revolution'],
    ['کمیته‌بازی سر کوچه',  'prof_14_topic_revolution'],
    ['workers of the revolution, unite!', 'prof_14_topic_revolution'],
    ['شورا به وقت کارخانه', 'prof_14_topic_revolution'],
    ['bread, barracks & burnout', 'prof_15_topic_iran_iraq_war'],
    ['سهمیه در عصر سازندگی', 'prof_15_topic_iran_iraq_war'],
    ['neutrality has its perks', 'prof_15_topic_iran_iraq_war'],
    ['بی‌طرفی با طعم باقلوا', 'prof_15_topic_iran_iraq_war'],
    ['the satanic dismissal', 'prof_18_topic_foreign_policy'],
    ['فتوای بی‌ضمانت',      'prof_18_topic_foreign_policy'],
    ['hezbollah\'s winning hand', 'prof_19_topic_axis_of_resistance'],
    ['فرماندهی در ضاحیه، مشاوره در تهران', 'prof_19_topic_axis_of_resistance'],
    ['neither proxies nor peons', 'prof_19_topic_axis_of_resistance'],
    ['نه مزدور و نه دست‌نشانده', 'prof_19_topic_axis_of_resistance'],
    ['a chain reaction in tehran', 'prof_16_topic_factional_politics'],
    ['زنجیره‌ای از تجریش تا راه‌آهن', 'prof_16_topic_factional_politics'],
    ['activism as usual',   'prof_16_topic_factional_politics'],
    ['موج‌سواری با برگ رأی', 'prof_16_topic_factional_politics'],
    ['kahrizak and ruin',   'prof_16_topic_factional_politics'],
    ['کهریزک، خطِ پایانِ توجیه', 'prof_16_topic_factional_politics'],
    ['guardians of the status quo', 'prof_16_topic_factional_politics'],
    ['فیلتر با تیغ استصواب', 'prof_16_topic_factional_politics'],
    ['bonyad empires and paralaws', 'prof_17_topic_irgc_political_economy'],
    ['امپراتوری‌های بی‌مالیات', 'prof_17_topic_irgc_political_economy'],
    ['the mobin disconnection', 'prof_17_topic_irgc_political_economy'],
    ['اعتماد مبینِ بی‌صدا', 'prof_17_topic_irgc_political_economy'],
    ['contracts and cold water', 'prof_17_topic_irgc_political_economy'],
    ['سدسازی با طعم نفت',   'prof_17_topic_irgc_political_economy'],
    ['transnational guerrillas in the mist', 'prof_19_topic_axis_of_resistance'],
    ['چریک‌های فرامرزی در غبار', 'prof_19_topic_axis_of_resistance'],
    ['the jihad of brick and mortar', 'prof_15_topic_iran_iraq_war'],
    ['جهاد با بیل و بی‌سیم', 'prof_15_topic_iran_iraq_war'],
    ['khomeinism and its discontents', 'prof_14_topic_revolution'],
    ['پوپولیسم در ردای فقه', 'prof_14_topic_revolution'],
    ['when khomeini met molkara', 'prof_21_topic_gender_politics'],
    ['فتوای تغییر در اتاق جماران', 'prof_21_topic_gender_politics'],
    ['park life under patriarchy', 'prof_21_topic_gender_politics'],
    ['بوستانِ تفکیک‌شده',   'prof_21_topic_gender_politics'],
    ['the bomb according to waltz', 'prof_18_topic_foreign_policy'],
    ['والتز با کلاهک هسته‌ای', 'prof_18_topic_foreign_policy'],
    ['komitehs of the round table', 'prof_14_topic_revolution'],
    ['کمیته‌های محل به وقت تصفیه', 'prof_14_topic_revolution'],
    ['sanctions in the kitchen', 'prof_20_topic_sanctions'],
    ['تحریم در سفره بانوان', 'prof_20_topic_sanctions'],
    ['the proxy paradox',   'prof_19_topic_axis_of_resistance'],
    ['فرمانده بدون فرمانبردار', 'prof_19_topic_axis_of_resistance'],
    ['true promise, real headache', 'prof_23_topic_iran_at_war'],
    ['وعده صادق روی آسمان تل‌آویو', 'prof_23_topic_iran_at_war'],
    ['improv at the ministry', 'prof_16_topic_factional_politics'],
    ['بداهه‌سازی در دیوان‌سالاری', 'prof_16_topic_factional_politics'],
    ['justice for some shares', 'prof_17_topic_irgc_political_economy'],
    ['سهام عدالت در جیب خصولتی', 'prof_17_topic_irgc_political_economy'],
    ['the dialogue of the deaf', 'prof_18_topic_foreign_policy'],
    ['گفتگوی تمدن‌ها بدون بلندگو', 'prof_18_topic_foreign_policy'],
    ['discourse of disdain', 'prof_18_topic_foreign_policy'],
    ['صرف و نحو استکبارستیزی', 'prof_18_topic_foreign_policy'],
    ['the ardabil maneuver', 'prof_22_topic_minorities'],
    ['اردبیل‌سازی در حیاط خلوت', 'prof_22_topic_minorities'],
    ['revolution in one room', 'prof_14_topic_revolution'],
    ['انقلاب در یک اتاق: مجلس خبرگان ۵۸', 'prof_14_topic_revolution'],
    ['the baluchi divide',  'prof_22_topic_minorities'],
    ['مرزِ سوخت و سوگ',     'prof_22_topic_minorities'],
    ['family planning, mullah style', 'prof_21_topic_gender_politics'],
    ['تنظیم خانواده پای منبر', 'prof_21_topic_gender_politics'],
    ['the status anxiety of tehran', 'prof_18_topic_foreign_policy'],
    ['بحران شناسایی در اتاق بیضی', 'prof_18_topic_foreign_policy'],
    ['neoliberal nightmares in mashhad', 'prof_20_topic_sanctions'],
    ['شورش کوی طلاب در عصر تعدیل', 'prof_20_topic_sanctions'],
    ['maktabi vs expert',   'prof_15_topic_iran_iraq_war'],
    ['مکتبی در سنگر، متخصص در دفتر', 'prof_15_topic_iran_iraq_war'],
    ['mothers of the citadel', 'prof_15_topic_iran_iraq_war'],
    ['سنگردارانِ زینب',     'prof_15_topic_iran_iraq_war'],
    ['non-aligned and non-committed', 'prof_18_topic_foreign_policy'],
    ['نه شرقی، نه غربی، فقط نم', 'prof_18_topic_foreign_policy'],
    ['anatomy of a tehran barricade', 'prof_14_topic_revolution'],
    ['سفارت‌گیری با مجوز تاریخ', 'prof_14_topic_revolution'],
    ['the caspian equation', 'prof_18_topic_foreign_policy'],
    ['خزر با سهم مساویِ نامساوی', 'prof_18_topic_foreign_policy'],
    ['the ration book blues', 'prof_15_topic_iran_iraq_war'],
    ['کوپن به شرط صف',      'prof_15_topic_iran_iraq_war'],
    ['the sanctions profiteers', 'prof_20_topic_sanctions'],
    ['کاسبان تحریم در برج میلاد', 'prof_20_topic_sanctions'],
    ['shi\'a geopolitics goes arabic', 'prof_19_topic_axis_of_resistance'],
    ['هلال شیعی در جام جم', 'prof_19_topic_axis_of_resistance'],
    ['conspiracy and cognition', 'prof_14_topic_revolution'],
    ['تئوری توطئه با مهر انگلیس', 'prof_14_topic_revolution'],
    ['ethnic lines in the oil fields', 'prof_22_topic_minorities'],
    ['نفت روی گسل‌های هویت', 'prof_22_topic_minorities'],
    ['republican cloth, clerical threads', 'prof_16_topic_factional_politics'],
    ['جمهوری در آینه تئوکراسی', 'prof_16_topic_factional_politics'],

    ['iraq',                'prof_15_topic_iran_iraq_war'],
    ['axis of resistance',  'prof_19_topic_axis_of_resistance'],
    ['resistance economy',  'prof_20_topic_sanctions'],
    ['sanction',            'prof_20_topic_sanctions'],
    ['embargo',             'prof_20_topic_sanctions'],
    ['revolutionary guard', 'prof_17_topic_irgc_political_economy'],
    ['irgc',                'prof_17_topic_irgc_political_economy'],
    ['sepah',               'prof_17_topic_irgc_political_economy'],
    ['basij',               'prof_17_topic_irgc_political_economy'],
    ['bonyad',              'prof_17_topic_irgc_political_economy'],
    ['political economy',   'prof_17_topic_irgc_political_economy'],
    ['foreign policy',      'prof_18_topic_foreign_policy'],
    ['foreign',             'prof_18_topic_foreign_policy'],
    ['diplomac',            'prof_18_topic_foreign_policy'],
    ['nuclear',             'prof_18_topic_foreign_policy'],
    ['gender',              'prof_21_topic_gender_politics'],
    ['women',               'prof_21_topic_gender_politics'],
    ['hijab',               'prof_21_topic_gender_politics'],
    ['veil',                'prof_21_topic_gender_politics'],
    ['minorit',             'prof_22_topic_minorities'],
    ['ethnic',              'prof_22_topic_minorities'],
    ['kurd',                'prof_22_topic_minorities'],
    ['baluch',              'prof_22_topic_minorities'],
    ['azer',                'prof_22_topic_minorities'],
    ['religious',           'prof_22_topic_minorities'],
    ['2023',                'prof_23_topic_iran_at_war'],
    ['protest',             'prof_23_topic_iran_at_war'],
    ['faction',             'prof_16_topic_factional_politics'],
    ['reformist',           'prof_16_topic_factional_politics'],
    ['conservativ',         'prof_16_topic_factional_politics'],
    ['principalist',        'prof_16_topic_factional_politics'],
    ['war',                 'prof_15_topic_iran_iraq_war'],
    ['revolution',          'prof_14_topic_revolution'],
    ['velayat',             'prof_14_topic_revolution'],
    ['faqih',               'prof_14_topic_revolution'],
    ['supreme leader',      'prof_14_topic_revolution'],
    ['constitution',        'prof_14_topic_revolution'],
    ['islamic republic',    'prof_14_topic_revolution'],
    ['institution',         'prof_14_topic_revolution']
  ];

  /* What he says, keyed by the clip that says it — the pack's own filename-to-line
     mapping, inlined rather than fetched, so the bubble and the audio can never
     disagree and nothing is read off disk at run time.

     It is also the gate. The layer draws whoever the running edition registered,
     and every cue the engine raises reaches every registration — so the table is
     what decides she is speaking: a name in it is a clip worth showing a man for,
     and a name out of it is not hers to stand up for, whatever the cue. Undefined
     is the whole of the answer, and it needs no rule saying so. The clips she is
     *not* answering are the general edition's, which this table has never held. */
  var TEXT = {
    'prof_01_professor_welcome': 'Welcome to IR4595: Iran in World Politics. We’ll begin with revolution, move through war, factional politics, the Revolutionary Guards, sanctions, gender, minorities, foreign policy, and finally the rather inconvenient fact that history has refused to stop happening.',
    'prof_02_start_game': 'Right. Let’s see what you actually know.',
    'prof_03_choose_topic': 'Choose a topic. Preferably one you’ve read about.',
    'prof_04_correct_annoyingly_so': 'Correct. Annoyingly so.',
    'prof_05_correct_surprised': 'Yes. That is, in fact, the answer. I’m as surprised as you are.',
    'prof_06_wrong_confident': 'No. Confident, certainly. Correct, unfortunately not.',
    'prof_07_wrong_reading': 'That’s wrong. The reading was not merely decorative, you know.',
    'prof_08_timeout': 'Time. History has moved on without you.',
    'prof_09_close_call': 'Very close. In academia, of course, that remains wrong.',
    'prof_10_three_in_a_row': 'Three in a row. I may have underestimated you. Briefly.',
    'prof_11_comeback': 'A comeback. How very post-revolutionary of you.',
    'prof_12_daily_double': 'You’ve found the Daily Double. At last, a decision with consequences.',
    'prof_13_final_jeopardy': 'Final Jeopardy. One question, one wager, and considerably less room for bluffing.',
    'prof_14_topic_revolution': 'Revolution and the Islamic Republic. Ideology, institutions, and the small matter of who actually rules.',
    'prof_15_topic_iran_iraq_war': 'The Iran–Iraq War. Eight years, several turning points, and no shortage of people explaining them badly.',
    'prof_16_topic_factional_politics': 'Factional politics. Because calling the Islamic Republic a single actor is a very efficient way to lose marks.',
    'prof_17_topic_irgc_political_economy': 'The Revolutionary Guards and political economy. Guns, contracts, institutions, and the awkward business of deciding where the state actually ends.',
    'prof_18_topic_foreign_policy': 'Iranian foreign policy. Ideology, pragmatism, insecurity, status, recognition. Pick your explanation carefully. Preferably more than one.',
    'prof_19_topic_axis_of_resistance': 'The Axis of Resistance. Transnational solidarity, regional strategy, deterrence — and, as ever, a lively argument over which label is doing the most work.',
    'prof_20_topic_sanctions': 'Sanctions and the resistance economy. An excellent opportunity to discover why saying “sanctions hurt the economy” is the beginning of an answer, not the end of one.',
    'prof_21_topic_gender_politics': 'Gender politics. State power, social change, negotiation, resistance, and the usual danger of assuming the answer before examining the evidence.',
    'prof_22_topic_minorities': 'Ethnic and religious minorities. A subject on which sweeping generalisations will be punished with particular enthusiasm.',
    'prof_23_topic_iran_at_war': 'Iran at war, from 2023 to the present. Which is the syllabus politely acknowledging that the examination period may not be the most stressful event of the semester.',
    'prof_24_score_lead': 'You’re in the lead. Try not to convert that into a theory of your own brilliance just yet.',
    'prof_25_game_win': 'And that is the game. You’ve won. I’ll try not to let it affect the marking.',
    'prof_26_game_loss': 'And that is the game. You’ve lost, but quite usefully. There was clearly a great deal left to learn.',
    'prof_27_class_dismissed': 'Class dismissed. Do read before the next one. It makes the conversation considerably less painful for all of us.'
  };

  /* ── The soundtrack ───────────────────────────────────────────
   * The show's music and stings, replaced by the pack recorded for this course.
   * The map is keyed by the slot the engine asks for, and that is the whole of
   * why the engine needed one hook and no more: it is read where a file is
   * chosen, so nothing in the show has to know a course edition is on the floor.
   *
   * A slot this table does not name keeps the engine's own cue, which is eight
   * of the engine's eighteen — the select click, the buzzer, the two round
   * bumpers and the join sting are not on the album, so they are not claimed.
   *
   * This pack lives with the course, in `assets/audio/`, and not in the engine's
   * shared audio dir. A path here is safe for the same reason a bare name was:
   * the map is read only where a file is chosen, so every name that travels
   * anywhere else — `TEXT`, the `hostcue` the engine broadcasts, the guard that
   * stops a bed restarting — goes on seeing the clip's name and never its file.
   */
  var A = 'courses/iran-in-world-politics/assets/audio/';
  var SOUND = {
    menu_theme:        A + 'course_theme',
    splash_underscore: A + 'course_splash',
    thinking_loop:     A + 'course_thinking',
    wager:             A + 'course_daily_double',
    final:             A + 'course_final',
    armed:             A + 'course_lock_in',
    correct:           A + 'course_correct',
    incorrect:         A + 'course_wrong'
  };

  /* Everything else on the album is the professor, and the engine asks for those
     by the clip's own name rather than by slot. Keyed by their own names here, so
     the map and the folder stay in step by inspection: a clip dropped into
     `assets/audio/` without a line below plays nothing, and says so in the
     console. */
  ['prof_01_professor_welcome', 'prof_02_start_game', 'prof_03_choose_topic',
   'prof_04_correct_annoyingly_so', 'prof_05_correct_surprised',
   'prof_06_wrong_confident', 'prof_07_wrong_reading', 'prof_08_timeout',
   'prof_09_close_call', 'prof_10_three_in_a_row', 'prof_11_comeback',
   'prof_12_daily_double', 'prof_13_final_jeopardy', 'prof_14_topic_revolution',
   'prof_15_topic_iran_iraq_war', 'prof_16_topic_factional_politics',
   'prof_17_topic_irgc_political_economy', 'prof_18_topic_foreign_policy',
   'prof_19_topic_axis_of_resistance', 'prof_20_topic_sanctions',
   'prof_21_topic_gender_politics', 'prof_22_topic_minorities',
   'prof_23_topic_iran_at_war', 'prof_24_score_lead', 'prof_25_game_win',
   'prof_26_game_loss', 'prof_27_class_dismissed'
  ].forEach(function (n) { SOUND[n] = A + n; });

  function publish(mine) {
    if (mine) {
      window.HOST_CUE_MAP = CUE;
      window.HOST_VOICE = POOL;
      window.EDITION_SOUND = SOUND;
      window.HOST_PRECLUE = precue;
    } else {
      delete window.HOST_CUE_MAP;
      delete window.HOST_VOICE;
      delete window.EDITION_SOUND;
      delete window.HOST_PRECLUE;
    }
    /* After the swap, never before it: a bed already on the air was started from
       the mapping that was current then, and re-issuing it is how the arriving
       show stops playing the soundtrack of the one that just left. */
    if (window.Sound && window.Sound.refresh) window.Sound.refresh();
  }

  /* ── He talks when the room is quiet ──────────────────────────
   * The engine hands over two things: `hostcue`, which names the clip that just
   * started and reports null when one stops, and `hostbeat`, which reports a
   * moment. A beat cannot simply be played on the spot, and this is the part of
   * the design worth stating rather than discovering.
   *
   * The engine's verdict line is scheduled 650ms behind the verdict, and both
   * `showVerdict` and `finishFinal` open by cutting the audio. The score write
   * that detects a third consecutive answer therefore happens *before* the clip
   * that is about to comment on it. A streak line played the moment the beat
   * arrived would be cut off by the verdict, and a streak line routed through
   * the engine's own scheduler would be swallowed whole by that same cut. So a
   * beat waits: it queues, and it takes its turn once the room is quiet. The
   * instruction lands after the verdict, which is also when a person would say
   * it. */
  var QUIET_MS = 900;
  var queue = [];
  var pending = null;
  var speaking = false;
  /* The room being quiet is not the same as the room being free. While a clue
     is on screen and being read, the contestant's eye is on the question and a
     professor talking over it is not a beat, it is an interruption — and one the
     engine cannot see, because from the engine's side the room is silent. So the
     queue holds for the read and starts again when the lamp goes live. A Daily
     Double has no race and no lamp; its read is not held. */
  var holding = false;

  function standDown() {
    queue.length = 0;
    if (pending) { clearTimeout(pending); pending = null; }
    speaking = false;
    holding = false;
    if (window.HostLayer) window.HostLayer.hide();
  }

  function schedule() {
    if (pending) return;
    pending = setTimeout(drain, QUIET_MS);
  }

  function drain() {
    pending = null;
    if (holding || speaking || window.getEdition() !== 'iran-in-world-politics' || !queue.length) return;
    play(queue.shift());
    if (queue.length) schedule();
  }

  function enqueue(clip) {
    queue.push(clip);
    schedule();
  }

  function play(clip) {
    if (window.Sound && TEXT[clip]) window.Sound.voice(clip, 0.9);
  }

  /* ── The professor on the floor ───────────────────────────────
   * She is one speaker of two the build can put at the foot of the stage, so the
   * layer itself is `host-layer.js`'s — it owns the element, the pose lookup and
   * the pop. All this file contributes is *who*, and *what she says*: the sprite
   * and the `TEXT` table, which is also the gate that keeps her off the general
   * edition. Her name is out of that table and she stands down before the line
   * is ever written. */
  if (window.HostLayer) {
    window.HostLayer.register('iran-in-world-politics', {
      sprite: 'courses/iran-in-world-politics/assets/sprite-professor.png',
      lines: TEXT
    });
  }

  /* The bubble is `host-layer.js`'s business — it answers the same cue on its own
     listener. This one is about the audio queue only: a clip speaking holds the
     queue, and the cue going null is what releases it. */
  document.addEventListener('hostcue', function (e) {
    var name = e.detail && e.detail.name;
    if (name) {
      if (pending) { clearTimeout(pending); pending = null; }
      speaking = true;
    } else {
      speaking = false;
      schedule();
    }
  });

  /* Measured against the category name, so a category is introduced once in a
     match however many clues it gives up. The roll call is on the first board of
     a match, which is the one thing that reliably marks a new one. */
  var introduced = {};

  function theme(category) {
    for (var i = 0; i < THEME.length; i++) {
      if (category.indexOf(THEME[i][0]) !== -1) return THEME[i][1];
    }
    return null;
  }

  /* The category introduction, but now it owns the stage instead of waiting for
     it. The engine calls this through `HOST_PRECLUE` before it puts the question
     up, and it answers with `proceed` once the introduction is done — or at once
     if there is nothing to say. A tap anywhere during the clip reaches the same
     `proceed` through the engine's own gate, so the skip is the engine's, not
     ours. */
  function precue(clue, proceed) {
    var category = clue && String(clue.category || '').toLowerCase();
    var clip = category && !introduced[category] ? theme(category) : null;
    if (!clip) { proceed(); return; }
    introduced[category] = true;
    if (window.Sound && window.Sound.isEnabled && window.Sound.isEnabled() && TEXT[clip]) {
      window.Sound.voice(clip, 0.9, proceed);
    } else {
      proceed();
    }
  }

  document.addEventListener('hostbeat', function (e) {
    if (window.getEdition() !== 'iran-in-world-politics') return;
    var d = e.detail || {};
    var clip = null;
    /* Every beat but the opening of a raced clue means the read is behind us,
       so a hold can never outlive the clue that set it. */
    if (d.name !== 'clueOpen') holding = false;
    if (d.name === 'boardIdle') {
      var round = d.detail && d.detail.round;
      if (round === 'single') introduced = {};
      clip = ROUND_START[round] || null;
    } else if (d.name === 'clueOpen') {
      /* The category introduction is the pre-clue gate's now, not the queue's.
         This beat's remaining job is the hold: a raced clue reads in silence, so
         whatever the queue still carries waits for the lamp. A Daily Double has
         no race and no read, so it is not held. */
      if (d.detail && d.detail.race) holding = true;
      return;
    } else if (d.name === 'buzzersOpen') {
      schedule();
      return;
    } else {
      clip = BEAT[d.name] || null;
    }
    if (clip) enqueue(clip);
  });

  document.addEventListener('editionchange', function (e) { wear(e.detail.id); });
})();
