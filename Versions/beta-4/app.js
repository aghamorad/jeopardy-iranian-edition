/* JEOPARDY! — Iranian Edition, web build.
   Zero dependencies, zero build step. Open index.html and it plays. */
(function () {
'use strict';

/* Two banks ship in the box — the English original and the Persian edition —
   and the language gate picks one. They are the same shape, so a match is built
   from whichever is loaded and nothing downstream has to know which it is. The
   language is chosen on the splash, before a match exists, so the bank is
   resolved once here and again only if the room changes language in the lobby. */
var BANKS = { en: window.CLUES, fa: window.CLUES_FA };
var CLUES = BANKS[savedLang()] || BANKS.en || [];
/* Only while nothing is on the board: a match already dealt out of one bank
   cannot be rebuilt out of the other. The gate is on the splash, so this fires
   before a match exists; the guard is here for the lobby. */
document.addEventListener('langchange', function (ev) {
  if (S.players.length) return;
  CLUES = BANKS[ev.detail.lang] || BANKS.en || [];
});
var PLAYER_COLORS = ['#17b25a', '#e02020', '#f2efe9', '#0e8a45', '#a81616', '#c9c5bd'];
/* Everything the player sees is denominated in millions of toman, the way the
   native board is (BoardBuilder: 10M/25M/50M/100M/200M, doubling in Round II).
   The clue bank itself is still keyed by the old dollar-shaped integer, so both
   scales are kept: the bank key finds the clue, the toman figure is what is
   printed. */
var SINGLE_VALUES = [10, 25, 50, 100, 200];
var DOUBLE_VALUES = [20, 50, 100, 150, 200];
var SINGLE_BANK = [200, 400, 600, 800, 1000];
var DOUBLE_BANK = [400, 800, 1200, 1600, 2000];

/* The engine caps a wager at 200,000,000 regardless of round. */
var MAX_WAGER = 200;

/* Seconds. The answering window is the engine's own
   (GameConfiguration.answeringTimeoutSeconds); the buzz window and the board
   clock are the web build's, sized to keep a shared screen moving. */
var ANSWER_SECONDS = 12;
var BUZZ_SECONDS = 8;
var BOARD_SECONDS = 20;

/* The clue goes up with the buzzers shut and a countdown of its own, because a
   shared screen needs a beat to read the thing before anybody's thumb moves.
   The buzz window opens after that, on a clock of its own.
   The penalty for jumping the gun is the engine's own number
   (GameConfiguration.buzzerLockoutPenaltyMs) — short enough that an itchy thumb
   is survivable, long enough that whoever waited gets the floor first. */
var READ_SECONDS = 6;
var PREMATURE_MS = 600;

/* How much of the theme plays over the title card before she starts talking.
   Long enough to be a bar of music, short enough that nobody is waiting on it. */
var OPENING_MUSIC_MS = 2600;

/* The bed under her opening line. It is written to sit under a voice rather than
   to be listened to on its own, and it hands over to the show's theme the moment
   she finishes and the title card goes live. */
var SPLASH_UNDERSCORE = 'splash_underscore';

/* How long a round card holds the stage before it lifts and the clock starts.
   Long enough to read the round, short enough that a returning player is not
   waiting on ceremony. */
var ROUND_CARD_MS = 2400;

/* Her reaction to a verdict. Sixteen of each, and she should not repeat herself
   in front of the same room — so these are drawn from a shuffled bag rather than
   picked freely, which means every line is heard before any line is heard twice.
   The last one to be drawn goes back in with the rest on the next shuffle, so
   the bag boundary is not a repeat either.

   A clip only ever runs two to four seconds, so the sting underneath it gets a
   beat of its own first and she lands on top of it. */
var HOST_LINES = {
  right: [
    'right_01_well_look_at_you',
    'right_02_try_not_to_become_unbearable',
    'right_03_mashallah_an_actual_fact',
    'right_04_confidence_matched_the_answer',
    'right_05_please_remain_humble',
    'right_06_actual_knowledge_how_refreshing',
    'right_07_tell_your_uncle',
    'right_08_tehran_survives_another_round',
    'right_09_annoyingly_good',
    'right_10_i_hate_how_pleased_you_look',
    'right_11_not_just_opinions_after_all',
    'right_12_unfortunately_youre_right',
    'right_13_dont_get_used_to_this_feeling',
    'right_14_four_thousand_years_finally_correct',
    'right_15_try_not_to_explain_it_to_everyone',
    'right_16_you_may_be_smug_for_five_seconds'
  ],
  wrong: [
    'wrong_01_mashallah_the_confidence',
    'wrong_02_very_iranian_of_you',
    'wrong_03_no_facts_full_confidence',
    'wrong_04_dinner_party',
    'wrong_05_family_whatsapp',
    'wrong_06_source_your_uncle',
    'wrong_07_iranian_method',
    'wrong_08_mashallah_you_have_opinions',
    'wrong_09_tehran_taxi_driver',
    'wrong_10_iranian_uncle_nodding',
    'wrong_11_national_tradition',
    'wrong_12_world_class_confidence',
    'wrong_13_four_thousand_years',
    'wrong_14_cyrus_the_great',
    'wrong_15_dinner_fact',
    'wrong_16_explain_it_loudly'
  ]
};
var HOST_LINE_DELAY_MS = 650;

/* The host's per-clue `wrongLine` names the answer, so it is only safe once the
   clue is dead. While the others can still steal it, the host has to be rude
   about something other than the answer. */
var LOCKOUT_LINES = [
  'clue.lockout.0',
  'clue.lockout.1',
  'clue.lockout.2',
  'clue.lockout.3',
  'clue.lockout.4'
];

/* The six Persian subtitles the board mockup prints under each category
   header. The bank's real categories are ~100 jokes and its `theme` field is
   the only honest signal, so bucket the theme by keyword and let anything
   unrecognised fall to متفرقه. The English name is always the real category;
   this is the grey garnish beneath it. */
var PERSIAN_BUCKETS = [
  ['مردم و چهره‌ها', ['trailblazer', 'hero', 'maestro', 'instrument', 'tragic',
    'pioneer', 'figure', 'coronation', 'epistolary', 'monarchy', 'royal']],
  ['مکان‌ها و جغرافیا', ['geograph', 'mountain', 'river', 'desert', 'lake', 'maritime',
    'capital', 'strait', 'frontier', 'garden', 'archaeolog', 'monument', 'territorial',
    'island', 'shore', 'valley', 'caspian', 'gulf', 'ecology', 'city']],
  ['تاریخ و انقلاب‌ها', ['war', 'battle', 'empire', 'dynast', 'revolt', 'rebellion',
    'revolution', 'liberation', 'coup', 'occupation', 'conquest', 'siege', 'barricade',
    'movement', 'uprising', 'conflict', 'military', 'combat', 'aftermath', 'constitution',
    'reform', 'purge', 'destiny', 'turning point', 'crime']],
  ['فرهنگ و هنر', ['poet', 'poetic', 'verse', 'literature', 'novel', 'prose', 'fiction',
    'cinema', 'directing', 'palme', 'art', 'calligraph', 'architecture', 'music', 'radif',
    'vocal', 'sound', 'handicraft', 'cuisine', 'festival', 'culture', 'material', 'memoir',
    'linguistic', 'religion', 'theolog', 'mystic', 'philosoph', 'shrine', 'pilgrimage',
    'clergy', 'science', 'medicine', 'engineering', 'aviation', 'mytholog', 'spectacle']],
  ['سیاست و جامعه', ['politic', 'diploma', 'intelligence', 'statecraft', 'governance',
    'geopolit', 'opec', 'petroleum', 'oil', 'econom', 'press', 'education', 'activism',
    'espionage', 'spy', 'secret societ', 'coalition', 'ideolog', 'party', 'parliament',
    'treasury', 'commerce', 'trade', 'boycott', 'sanction', 'law', 'legal', 'capitulation',
    'advisor', 'concession', 'commodit', 'infrastructure', 'institution', 'agriculture']]
];

function persianSubtitle(col) {
  var hay = ((col.category || '') + ' ' + ((col.cells[0] && col.cells[0].clue.theme) || '')).toLowerCase();
  for (var i = 0; i < PERSIAN_BUCKETS.length; i++) {
    var keys = PERSIAN_BUCKETS[i][1];
    for (var j = 0; j < keys.length; j++) if (hay.indexOf(keys[j]) !== -1) return PERSIAN_BUCKETS[i][0];
  }
  return 'متفرقه';
}

// ── Helpers ────────────────────────────────────────────────

function el(id) { return document.getElementById(id); }

function make(tag, className, text) {
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

/* `n` is millions of toman. The compact form goes where the same figure
   repeats all over the screen (tiles, podiums, results); fmtT spells the unit
   out for the two places a player is reading the stakes. */
function fmt(n) {
  return (n < 0 ? '−' : '') + num(Math.abs(n)) + T('unit.m');
}

function fmtT(n) {
  return fmt(n) + T('unit.toman');
}

function shuffle(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

function groupBy(arr, key) {
  var out = {};
  arr.forEach(function (item) {
    var k = key(item);
    (out[k] || (out[k] = [])).push(item);
  });
  return out;
}

/* The bank ships with the right answer always at index 0 — the native app
   reshuffles per clue in BoardBuilder, so the web app does the same rather
   than teaching players to always tap the first option. Duplicated option
   texts are collapsed here, compared on their trimmed form: three Persian
   clues ship the answer twice, once correct and once as a distractor a space
   longer, and a board that shows the same text in two squares is not a
   board anyone can play. The exact string is kept for display, but the
   correct index is found on the trimmed key so collapsing cannot lose it. */
function shufflingOptions(clue) {
  var key = function (s) { return String(s).replace(/^\s+|\s+$/g, ''); };
  var correctKey = key(clue.options[clue.correct]);
  var keys = [];
  var unique = [];
  clue.options.forEach(function (text) {
    if (keys.indexOf(key(text)) === -1) { keys.push(key(text)); unique.push(text); }
  });
  var opts = shuffle(unique);
  var copy = {};
  for (var k in clue) if (Object.prototype.hasOwnProperty.call(clue, k)) copy[k] = clue[k];
  copy.options = opts;
  copy.correct = -1;
  for (var i = 0; i < opts.length; i++) {
    if (key(opts[i]) === correctKey) { copy.correct = i; break; }
  }
  return copy;
}

// ── Audio ──────────────────────────────────────────────────

var Sound = (function () {
  var enabled = true;
  var musicName = null;
  var musicEl = null;

  /* The one voice on the floor. Only one line is ever worth hearing, so a new
     cue cuts the old one off through its own `finish` — that restores the music
     the old line had ducked before the new one reads the slot, which is what
     keeps the betting house from going quiet after a fast pair of verdicts. */
  var voiceEl = null;

  /* Her reaction is scheduled rather than fired, so that the sting underneath
     gets a beat to itself. One timer for the whole show — a verdict that
     arrives while the last one is still waiting is the same timer, retimed. */
  var hostTimer = null;

  function url(name, ext) { return 'assets/audio/' + name + ext; }

  /* Remembers which extension each cue turned out to have, so the guessing
     costs one failed request per cue and not one per play. */
  var resolved = {};

  /* Cues are dropped in by hand and arrive in whatever format they were made
     in — .m4a from this machine, .mp3 from anywhere else. A cue gets one
     retry on the other extension before it counts as absent, so replacing a
     line never needs a code change. */
  function makeEl(name, volume, loop) {
    var a = document.createElement('audio');
    a.preload = 'auto';
    a.loop = !!loop;
    a.volume = volume;
    a._exts = resolved[name] ? [resolved[name]] : ['.m4a', '.mp3'];
    a._ext = 0;
    a.src = url(name, a._exts[0]);

    a.addEventListener('error', function () {
      /* A released element has no source on purpose — that is not a cue that
         failed to load, and it must not be sent looking for its other format. */
      if (a._released) return;
      if (a._ext + 1 < a._exts.length) {
        a._ext++;
        a._retrying = true;
        a.src = url(name, a._exts[a._ext]);
        a.load();
        a.play().catch(function () {});
        return;
      }
      /* Both extensions are missing. Clear the flag so callers see a real
         failure rather than a retry that is still in flight. */
      a._retrying = false;
    });

    a.addEventListener('loadeddata', function () {
      resolved[name] = a._exts[a._ext];
      a._retrying = false;
    });

    return a;
  }

  /* A one-shot gives its decoder back the moment it finishes. iOS WebKit caps
     how many media elements may be live at once, and a show that leaks one per
     buzzer, sting and select-click runs out of room to play the next one —
     which arrives as silence rather than as an error. */
  function release(a) {
    a.addEventListener('ended', function () {
      a._released = true;
      a.pause();
      a.removeAttribute('src');
      a.load();
    });
  }

  /* iOS WebKit ignores the volume property: the setter is a no-op and the
     getter always answers 1. Every fade in this file walks a level toward a
     target, so on a phone they all ran without ever arriving — the old cue
     never reached zero, never paused, and each screen change stacked another
     loop on top of the last until the entire show was playing at once. Probe
     the property once and stop trusting it anywhere it does real work. */
  var volumeWorks = (function () {
    var probe = document.createElement('audio');
    try { probe.volume = 0.5; } catch (e) { return false; }
    return Math.abs(probe.volume - 0.5) < 0.01;
  })();

  var MUSIC_LEVEL = 0.34;

  /* The old bed stops here, and it stops by being paused — the fade is the
     courtesy on the way, never the thing that does the stopping. */
  function stopMusic(dying) {
    if (!volumeWorks) { dying.pause(); return; }
    var ticks = 0;
    var fade = setInterval(function () {
      dying.volume = Math.max(0, dying.volume - 0.06);
      /* The last tick is a deadline as much as a level, so a cue that cannot be
         faded is paused anyway rather than left running under the next one. */
      if (dying.volume <= 0.001 || ++ticks >= 12) {
        clearInterval(fade);
        dying.pause();
      }
    }, 40);
  }

  /* Music is a single slot — a new cue replaces the old one rather than
     stacking on it. Returns `true` when the cue is already on the air,
     the play promise when this call started it, and `false` when the show is
     muted — the cold open reads the difference, because an opening that was
     never heard has to stay armed for the next gesture. */
  function music(name) {
    /* The name guard is what stops a cue restarting on every screen change, but
       it must not outlive the audio itself — an element a duck left paused, or
       one whose first play the browser refused, still counts as "already
       playing" unless we look at it. */
    if (musicName === name && musicEl && !musicEl.paused) return true;
    musicName = name;
    if (musicEl) stopMusic(musicEl);
    musicEl = null;
    if (!enabled || !name) return false;
    /* On a platform with no usable volume the bed simply plays at its own
       level; there is no fade to make, and the level below is the intent. */
    var a = makeEl(name, volumeWorks ? 0 : MUSIC_LEVEL, true);
    musicEl = a;
    var play = a.play();
    /* A refused play — the autoplay policy, on a page nobody has touched yet —
       must not leave the slot claimed, or the name guard at the top of this
       function swallows every later attempt and the show runs silent. */
    if (play && play.catch) play.catch(function () {
      if (musicEl === a) { musicEl = null; musicName = null; }
    });
    if (volumeWorks) {
      var rise = setInterval(function () {
        if (musicEl !== a) { clearInterval(rise); return; }
        a.volume = Math.min(MUSIC_LEVEL, a.volume + 0.04);
        if (a.volume >= MUSIC_LEVEL) clearInterval(rise);
      }, 50);
    }
    return play;
  }

  function sfx(name, volume) {
    if (!enabled || !name) return;
    var a = makeEl(name, volume == null ? 0.7 : volume, false);
    release(a);
    a.play().catch(function () {});
  }

  /* A one-shot cue that takes the floor: the music drops out while it plays
     and comes back when it is done. Used for the host's lines and for the
     opening challenge, which run anywhere from three seconds to fifteen.
     `opts.over` keeps the bed running underneath instead — the splash
     underscore is written to sit under her line, so it must not be the thing
     that gets ducked out of the way. */
  function voice(name, volume, then, opts) {
    if (!enabled || !name) return;
    /* Whoever is talking gives up the floor first. `finish` puts back the music
       it ducked, so doing this before reading `musicName` below means the new
       line ducks the right bed instead of inheriting a hole. */
    if (voiceEl && voiceEl._finish) voiceEl._finish();
    var over = !!(opts && opts.over);
    var a = makeEl(name, volume == null ? 0.85 : volume, false);
    voiceEl = a;
    var ducked = over ? null : musicName;
    var done = false;
    var guard = null;
    if (ducked) music(null);

    function finish() {
      if (done) return;
      done = true;
      if (voiceEl === a) voiceEl = null;
      clearTimeout(guard);
      a.pause();
      /* Only restore the cue it interrupted — if the game moved on to a new
         one while it was playing, that cue wins. Failing that, fall back to the
         theme: the show always has a bed, so a cue that ends with the slot
         empty hands the lobby its music back instead of leaving silence.
         A voice that ran `over` the bed never touched the slot, so it leaves it
         exactly as it found it — `then` decides what happens next. */
      if (enabled && !over && musicName === null) music(ducked || 'menu_theme');
      if (then) then();
    }
    a._finish = finish;

    a.addEventListener('ended', finish);
    /* A missing .m4a is the normal case for a hand-dropped .mp3 — let the
       retry finish before treating the cue as absent. */
    a.addEventListener('error', function () { if (!a._retrying) finish(); });
    /* The safety net is sized to the cue once its length is known, so a long
       one is never cut off and a short one never holds the music hostage. */
    a.addEventListener('loadedmetadata', function () {
      if (isFinite(a.duration) && a.duration > 0) {
        clearTimeout(guard);
        guard = setTimeout(finish, a.duration * 1000 + 2500);
      }
    });
    guard = setTimeout(finish, 20000);
    /* A play() the browser blocks never fires `ended`, which would otherwise
       leave the music muted for the rest of the match. The catch has to ignore
       the abort that the .m4a miss throws on its way to the .mp3 retry —
       otherwise the retry is cancelled a microtask after it starts and the cue
       never sounds. */
    a.play().catch(function () { if (!a._retrying) finish(); });
  }

  /* Draw from a shuffled bag rather than picking at random, so she does not say
     the same thing twice in front of the same room. The bag empties completely
     before it is refilled — and the last line out of a bag is the first thing
     shuffled into the next one, so the seam is not a repeat either. */
  var hostBag = { right: [], wrong: [] };

  function drawHostLine(kind) {
    var pool = HOST_LINES[kind];
    if (!pool || !pool.length) return null;
    if (!hostBag[kind].length) {
      var bag = pool.slice();
      for (var i = bag.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var swap = bag[i]; bag[i] = bag[j]; bag[j] = swap;
      }
      hostBag[kind] = bag;
    }
    return hostBag[kind].pop();
  }

  /* Her verdict line. The sting fires first and she lands on top of it, so this
     waits a beat instead of talking over the sound that just told the room the
     answer was wrong. */
  function hostLine(kind) {
    clearTimeout(hostTimer);
    if (!enabled) return;
    var name = drawHostLine(kind);
    if (!name) return;
    hostTimer = setTimeout(function () {
      hostTimer = null;
      voice(name, 0.85);
    }, HOST_LINE_DELAY_MS);
  }

  /* Stop the room talking, now. Used when the game moves on — a click landing
     inside the delay above would otherwise cut silence and then let the clip
     start over the next clue. Goes through `finish` rather than `pause`,
     because only `finish` fires `ended`'s work and puts the ducked music back. */
  function cut() {
    clearTimeout(hostTimer);
    hostTimer = null;
    if (voiceEl && voiceEl._finish) voiceEl._finish();
  }

  function setEnabled(on) {
    enabled = on;
    if (!on) {
      if (musicEl) { musicEl.pause(); musicEl = null; }
      musicName = null;
      /* Muting mid-sentence has to end her line the same way it ends the music,
         or the cue would carry on unheard and hold the floor. */
      cut();
    }
  }

  return {
    music: music, sfx: sfx, voice: voice, hostLine: hostLine, cut: cut,
    setEnabled: setEnabled, isEnabled: function () { return enabled; }
  };
})();

// ── State ──────────────────────────────────────────────────

var S = {
  screen: 'splash',
  playerCount: 3,
  /* Empty on purpose: an empty input shows the placeholder, which is the one
     copy that has to change with the language. The fallback name is built at
     the moment the match starts. */
  names: ['', '', ''],
  opponents: 'mixed',  // human | mixed | bots
  difficulty: 'normal',
  answerMode: 'mc',    // mc | write
  players: [],
  round: 'single',
  roundsDone: [],
  board: [],
  usedCategories: {},
  clue: null,
  clueCtx: null,
  mode: 'board',       // board | dd | final — decides who may answer
  phase: 'idle',       // reading | answering | resolved
  buzzed: null,
  holder: null,        // the contestant with the floor in dd/final
  lockedOut: [],
  armed: false,
  opening: false,      // she is mid-sentence on the title card
  openingDone: false,  // she has had her say; the title card will not replay it
  openTimer: null,
  speaking: false,     // her cue is on the air, so her jaw is running
  voicePending: false, // the player is held on the title card until she is done
  mouthCap: null,      // the last-resort release of that hold
  prematureUntil: {},  // player index -> the moment they may buzz again
  /* The judge asks for a full name on some clues. It is asked once per clue:
     the second attempt passes `noPrompt`, so a player who answers "Qavam" and
     is told to be specific is not asked to be specific forever. */
  writePrompted: false,
  earlyTimer: null,
  cursor: { col: 0, row: 0 },
  menuIndex: 0,
  finalQueue: [],
  finalAnswers: [],
  finalTimer: null,
  finalRemaining: 0,
  clueTimer: null,
  clueRemaining: 0,
  boardTimer: null,
  boardRemaining: 0,
  roundCardOn: false,  // the scene change is covering the screen
  roundCardTimer: null
};

/* Seconds a contestant gets to answer the Final clue, per the engine. */
var FINAL_SECONDS = 30;

// ── Screen plumbing ────────────────────────────────────────

function show(id) {
  var screens = document.querySelectorAll('.screen');
  for (var i = 0; i < screens.length; i++) screens[i].classList.remove('is-active');
  var target = el('screen-' + id);
  if (target) target.classList.add('is-active');
  S.screen = id;
  window.scrollTo(0, 0);
}

/* ── The round card ───────────────────────────────────────────
   The scene change: a scrim, the round named large, the flag drawing itself
   out. The round underneath is already built when the card goes up, so this is
   presentation only — but it is opaque and unskippable, which means the board
   clock must not run behind it. Whoever is waiting to pick a clue gets those
   seconds back; the clock starts when the scrim lifts. */
function showRoundCard(kicker, title) {
  var card = el('round-card');
  if (!card) return;

  el('round-kicker').textContent = kicker;
  el('round-title').textContent = title;

  S.roundCardOn = true;
  stopBoardClock();
  stopClueClock();

  card.hidden = false;
  /* The reflow is what lets the entrance replay on a card that was already
     shown once this match. */
  void card.offsetWidth;
  card.classList.add('is-on');

  if (S.roundCardTimer) clearTimeout(S.roundCardTimer);
  S.roundCardTimer = setTimeout(function () {
    card.classList.remove('is-on');
    S.roundCardTimer = setTimeout(function () {
      card.hidden = true;
      S.roundCardTimer = null;
      S.roundCardOn = false;
      if (S.screen === 'board') startBoardClock();
    }, 460);
  }, ROUND_CARD_MS);
}

// ── Lobby ──────────────────────────────────────────────────

function renderNames() {
  var host = el('names');
  host.innerHTML = '';
  for (var i = 0; i < S.playerCount; i++) {
    (function (idx) {
      var wrap = make('div', 'name-field');
      var dot = make('span', 'dot');
      dot.style.background = PLAYER_COLORS[idx];
      wrap.appendChild(dot);

      /* A robot seat is a caption, not a field: its name is the host's joke and
         its brain is the difficulty the room chose. Offering a text box there
         would invite a name that is then thrown away at the first clue. */
      if (Bots.seatIsBot(idx)) {
        wrap.classList.add('is-bot');
        wrap.appendChild(make('span', 'bot-name', T('bot.name.' + (idx + 1))));
        wrap.appendChild(make('span', 'bot-brain', T('bot.' + S.difficulty)));
        host.appendChild(wrap);
        return;
      }

      var input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 14;
      input.value = S.names[idx] || '';
      input.setAttribute('placeholder', T('setup.playerDefault', { n: num(idx + 1) }));
      input.setAttribute('aria-label', T('setup.nameAria', { n: num(idx + 1) }));
      input.addEventListener('input', function () {
        S.names[idx] = input.value;
      });
      wrap.appendChild(input);
      host.appendChild(wrap);
    })(i);
  }
}

function setSoundSegments(on) {
  ['sound-toggle', 'settings-sound'].forEach(function (id) {
    var host = el(id);
    if (!host) return;
    Array.prototype.forEach.call(host.children, function (b) {
      var isOn = (b.dataset.sound === 'on') === on;
      b.classList.toggle('is-on', isOn);
      b.setAttribute('aria-checked', isOn ? 'true' : 'false');
    });
  });
}

function initLobby() {
  renderNames();

  el('player-count').addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-count]');
    if (!btn) return;
    S.playerCount = parseInt(btn.dataset.count, 10);
    Array.prototype.forEach.call(el('player-count').children, function (b) {
      b.classList.toggle('is-on', b === btn);
      b.setAttribute('aria-checked', b === btn ? 'true' : 'false');
    });
    renderNames();
    Sound.sfx('select');
  });

  // Two identical segmented controls switch the same setting — the green-room
  // one and the settings overlay — so both have to move together.
  ['sound-toggle', 'settings-sound'].forEach(function (id) {
    var host = el(id);
    if (!host) return;
    host.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-sound]');
      if (!btn) return;
      var on = btn.dataset.sound === 'on';
      Sound.setEnabled(on);
      setSoundSegments(on);
      if (on) { Sound.music('menu_theme'); Sound.sfx('select'); }
    });
  });

  /* ── The cold open ────────────────────────────────────────
     The underscore and her challenge used to fire at boot. A browser refuses
     to play audio on a page nobody has touched, and `voice()` reads a refused
     play as a cue that ended — so on the web the whole opening was skipped in
     silence, while inside the apps (which suppress that policy) it played. It
     is armed on the first real gesture instead: the same press that picks a
     language starts the show. */
  /* The screens the show has not started on. The cold open belongs to these and
     stops at the end of them: the board is the game, and nothing from the
     splash follows it there. */
  var preGameScreen = function () {
    return S.screen === 'splash' || S.screen === 'lobby' || S.screen === 'setup';
  };

  var runOpening = function () {
    if (S.opening || S.openingDone) return;
    var started = Sound.music(SPLASH_UNDERSCORE);
    /* Muted: there is nothing to hear, so the opening is over before it began
       and the flag stays down for good. */
    if (started === false) { S.openingDone = true; return; }
    S.opening = true;
    S.openingDone = true;
    document.body.classList.add('is-opening');
    el('screen-splash').classList.add('is-opening');
    /* The browser answers a refused play a tick later. If that answer is a no,
       nothing is on the air: put the whole opening back the way it was so the
       next gesture can have another go at it. */
    if (started && started.catch) started.catch(function () {
      S.opening = false;
      S.openingDone = false;
      document.body.classList.remove('is-opening');
      el('screen-splash').classList.remove('is-opening');
      if (S.openTimer) { clearTimeout(S.openTimer); S.openTimer = null; }
      if (Sound.isEnabled()) Sound.music('menu_theme');
    });
    S.openTimer = setTimeout(function () {
      S.openTimer = null;
      /* She plays over whatever pre-game screen the player has moved on to — the
         cold open is a cold open, not a gate. But a line arriving once the board
         is up would talk straight through the clue bed with nothing ducking it,
         so by then she has missed her cue. */
      if (!Sound.isEnabled() || !preGameScreen()) { doneOpening(); return; }
      S.speaking = true;
      /* Only worth running if her mouth is actually up — the player may have
         walked past the title card already, and a jaw ticking over a hidden
         stage is a frame loop for nothing. */
      if (S.voicePending) jawStart();
      Sound.voice('opening_challenge', 0.9, doneOpening, { over: true });
    }, OPENING_MUSIC_MS);
  };

  /* Sound.voice always calls back — a missing cue, a refused play and a cue
     that simply ends all arrive here — so the opening can never be left
     hanging. The underscore has done its job by now, so this is where it hands
     over to the theme, unless she is still talking over a screen the player
     has left and something else already owns the music. */
  var doneOpening = function () {
    /* However the opening ended, no line is left waiting behind it. */
    if (S.openTimer) { clearTimeout(S.openTimer); S.openTimer = null; }
    if (!S.opening) return;
    S.opening = false;
    S.speaking = false;
    document.body.classList.remove('is-opening');
    if (el('screen-splash')) el('screen-splash').classList.remove('is-opening');
    /* She was the last thing between the player and the lobby, so her ending is
       what opens it. `leaveSplash` hands the music over — doing it here as well
       would start the theme twice. */
    if (S.voicePending) { leaveSplash(); return; }
    if (preGameScreen()) Sound.music('menu_theme');
  };

  /* Capture phase, and left in place rather than taken off on the first press:
     a refused play has to be able to try again on the next one, and `runOpening`
     is its own guard once the opening has genuinely started. Capture matters on
     the very first press, because the boot listener is on the bubble phase and
     would otherwise bring the theme up over the underscore. */
  var arm = function () { if (!S.openingDone) runOpening(); };
  document.addEventListener('pointerdown', arm, true);
  document.addEventListener('keydown', arm, true);
  document.addEventListener('gamepadconnected', arm, true);

  /* ── Her mouth ─────────────────────────────────────────────────
     There is no analyser behind this. Reading her cue's amplitude would mean
     running the audio through Web Audio, and rewiring a working path for a
     flourish is not a trade worth making untested, so the jaw runs on an
     envelope instead: two sines at unrelated periods plus a little noise, so
     that no loop of it settles into a rhythm. It is bracketed to the real cue
     by the same callbacks that start and end the cue, which is all the eye
     actually checks — a mouth that opens when she starts and shuts when she
     stops reads as hers. */
  var MOUTH_CAP_MS = 25000;   // the hold lifts by this, whatever else fails

  var mouthEl = el('mouth');
  var mouthOn = false, mouthT0 = 0, mouthAmp = 0, mouthRaf = 0;
  var reduceMotion = !!(window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  var jawFrame = function (ts) {
    if (!mouthOn || !mouthEl) { mouthOn = false; mouthRaf = 0; return; }
    if (!mouthT0) mouthT0 = ts;
    var t = (ts - mouthT0) / 1000;
    /* Eased in when she starts and eased out when she stops. While she is only
       waiting her turn the same envelope runs at a fraction of its depth, so
       she is alive through the underscore instead of frozen for two seconds. */
    var want = S.speaking ? 1 : 0.14;
    mouthAmp += (want - mouthAmp) * (want > mouthAmp ? 0.3 : 0.12);
    var v = 0.42 * (0.55 + 0.45 * Math.sin(t * 11.3))
          + 0.34 * (0.5 + 0.5 * Math.sin(t * 5.1 + 1.7))
          + 0.24 * Math.random();
    v = Math.min(1, Math.max(0.05, v)) * mouthAmp;
    mouthEl.style.setProperty('--jaw', v.toFixed(3));
    mouthEl.style.setProperty('--teeth', Math.min(1, v * 2.6).toFixed(2));
    mouthRaf = requestAnimationFrame(jawFrame);
  };

  var jawStart = function () {
    if (!mouthEl || mouthOn || reduceMotion) return;
    mouthOn = true; mouthT0 = 0; mouthAmp = 0;
    mouthRaf = requestAnimationFrame(jawFrame);
  };

  var jawStop = function () {
    mouthOn = false;
    if (mouthRaf) { cancelAnimationFrame(mouthRaf); mouthRaf = 0; }
    if (mouthEl) {
      mouthEl.style.setProperty('--jaw', '0');
      mouthEl.style.setProperty('--teeth', '0');
    }
  };

  /* The one way off the title card. It clears the hold unconditionally — a
     second press, the cap, or her cue ending can all arrive in any order — and
     only moves the screen if the player is still on the splash. */
  var leaveSplash = function () {
    S.voicePending = false;
    if (S.mouthCap) { clearTimeout(S.mouthCap); S.mouthCap = null; }
    jawStop();
    if (el('screen-splash')) el('screen-splash').classList.remove('is-mouth');
    if (S.screen === 'splash') show('lobby');
    /* While `S.opening` is up the music is hers; doneOpening hands it over. */
    if (!S.opening) Sound.music('menu_theme');
  };

  var skipMouth = function () { leaveSplash(); };

  /* The language press is the moment the show starts, so it is the moment she
     comes up. Nothing here waits on the audio having begun: `runOpening` may
     still be working its way back from a refused play, and she is worth showing
     either way — if her cue then arrives she is already mid-sentence, which is
     the truth. */
  var openMouth = function () {
    S.voicePending = true;
    if (el('screen-splash')) el('screen-splash').classList.add('is-mouth');
    jawStart();
    S.mouthCap = setTimeout(skipMouth, MOUTH_CAP_MS);
  };

  var begin = function (lang) {
    if (S.screen !== 'splash') return;
    /* A second press — a pad's A landing on a pill that has already been read,
       most often — means the player is done waiting. */
    if (S.voicePending) { skipMouth(); return; }
    if (lang) setLang(lang);
    /* She has the floor now: the title card holds her and the lobby waits. With
       the sound off, or with an opening that never got going, there is nothing
       to wait for and this stays the plain transition it has always been. */
    if (S.opening) { openMouth(); return; }
    leaveSplash();
  };
  el('lang-en').addEventListener('click', function () { Sound.sfx('select'); begin('en'); });
  el('lang-fa').addEventListener('click', function () { Sound.sfx('select'); begin('fa'); });

  /* Anywhere else on the card moves on: the mouth carries no affordance of its
     own, and two silent seconds would read as a freeze. The pill's own press
     bubbles up here as well, so without the `.pill` exclusion the press that
     brings her up would skip her in the same breath. The exclusion is on the
     pill rather than the menu because a disabled pill is not hit-testable —
     the press lands on the nav behind it and must come through as a skip. */
  document.addEventListener('click', function (ev) {
    if (!S.voicePending) return;
    if (ev.target && ev.target.closest && ev.target.closest('.pill')) return;
    skipMouth();
  });
  document.addEventListener('keydown', function (ev) {
    if (!S.voicePending || ev.repeat) return;
    if (ev.key === 'Escape' || ev.key === ' ' || ev.key === 'Enter') skipMouth();
  });

  /* The green room's three new choices all work the same way — one value on S,
     one lamp lit, one click — so they share a wire. `attr` is the data
     attribute, `key` the field on S. */
  var wireSegment = function (id, attr, key, after) {
    var host = el(id);
    if (!host) return;
    host.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-' + attr + ']');
      if (!btn) return;
      /* Read the attribute, not `dataset[attr]`: the key is hyphenated
         (`answer-mode`), and dataset names are camelCase, so the property
         lookup would silently store `undefined`. */
      S[key] = btn.getAttribute('data-' + attr);
      Array.prototype.forEach.call(host.children, function (b) {
        b.classList.toggle('is-on', b === btn);
        b.setAttribute('aria-checked', b === btn ? 'true' : 'false');
      });
      if (after) after();
      Sound.sfx('select');
    });
  };
  /* A room of humans has nobody to make clever: the robot brains row hides
     rather than sitting there doing nothing. */
  var showDifficulty = function () {
    var row = el('difficulty-row');
    if (row) row.hidden = S.opponents === 'human';
  };
  /* Which seats are robots depends on this switch, so the roster is redrawn
     with it — otherwise the field the player just named turns into a robot
     without the label saying so. */
  wireSegment('opponents', 'opponents', 'opponents', function () {
    showDifficulty();
    renderNames();
  });
  wireSegment('difficulty', 'difficulty', 'difficulty', function () {
    /* The brain tag beside a robot's name is the chosen difficulty; it is only
       ever visible in a room that has robots in it. */
    if (S.opponents !== 'human') renderNames();
  });
  wireSegment('answer-mode', 'answer-mode', 'answerMode');
  showDifficulty();

  el('go-setup').addEventListener('click', function () { Sound.sfx('select'); show('setup'); });
  el('setup-back').addEventListener('click', function () { Sound.sfx('select'); show('lobby'); });
  el('quit-game').addEventListener('click', function () {
    Sound.cut();
    Sound.sfx('select');
    /* Back to the top of the show, not to silence — the theme runs through. */
    show('splash');
  });

  el('open-settings').addEventListener('click', function () { Sound.sfx('select'); el('settings-panel').hidden = false; });
  el('open-howto').addEventListener('click', function () { Sound.sfx('select'); el('howto-panel').hidden = false; });
  Array.prototype.forEach.call(document.querySelectorAll('[data-close]'), function (btn) {
    btn.addEventListener('click', function () {
      var panel = el(btn.dataset.close);
      if (panel) panel.hidden = true;
      Sound.sfx('select');
    });
  });

  el('start-game').addEventListener('click', startMatch);
  el('play-again').addEventListener('click', function () {
    Sound.cut();
    show('lobby');
    Sound.music('menu_theme');
  });

  setSoundSegments(Sound.isEnabled());

  /* The name fields carry the one piece of copy that is made in JS rather than
     written in the markup — the placeholder and the aria-label — so they are
     rebuilt when the room changes language. Unconditionally, because the
     language is picked on the splash and the green room is still hidden when
     that fires: gating this on the screen on show is what left "PLAYER 1" in
     Latin behind a Persian gate. `S.names` is the source of truth, so a rebuild
     never costs the player a name they have typed. */
  document.addEventListener('langchange', renderNames);

  runOpening();
}

// ── Board construction ─────────────────────────────────────

function buildBoard(round) {
  var pool = CLUES.filter(function (c) { return c.round === round; });
  var bank = round === 'single' ? SINGLE_BANK : DOUBLE_BANK;
  var values = round === 'single' ? SINGLE_VALUES : DOUBLE_VALUES;
  var byCat = groupBy(pool, function (c) { return c.category; });

  var available = Object.keys(byCat).filter(function (name) {
    return !S.usedCategories[name] && bank.every(function (v) {
      return byCat[name].some(function (c) { return c.value === v; });
    });
  });

  var chosen = shuffle(available).slice(0, 6);
  chosen.forEach(function (name) { S.usedCategories[name] = true; });

  var columns = chosen.map(function (name) {
    var cells = bank.map(function (bv, i) {
      var candidates = byCat[name].filter(function (c) { return c.value === bv; });
      var clue = shufflingOptions(pick(candidates));
      /* Overwrite the bank's key with the figure the tile prints, so the value
         on screen and the value the clue scores are the same number. */
      clue.value = values[i];
      return { clue: clue, value: values[i], solved: false };
    });
    return { category: name, cells: cells };
  });

  // One Daily Double per round, never in the top row.
  if (columns.length) {
    var ddCol = Math.floor(Math.random() * columns.length);
    var ddRow = 1 + Math.floor(Math.random() * (values.length - 1));
    columns[ddCol].cells[ddRow].dailyDouble = true;
  }
  return columns;
}

// ── Podiums ────────────────────────────────────────────────

function renderPodiums() {
  ['podiums-board', 'podiums-clue'].forEach(function (hostId) {
    var host = el(hostId);
    if (!host) return;
    host.innerHTML = '';
    S.players.forEach(function (p, i) {
      var card = make('div', 'podium');
      card.style.setProperty('--pc', p.color);
      if (p.score < 0) card.classList.add('neg');
      if (S.buzzed === i) card.classList.add('is-armed', 'shine', 'is-on');
      if (S.lockedOut.indexOf(i) !== -1) card.classList.add('is-out');

      var name = make('span', 'pname');
      name.appendChild(make('span', 'pdot'));
      name.appendChild(document.createTextNode(p.name));
      var score = make('span', 'pscore', fmt(p.score));
      card.appendChild(name);
      card.appendChild(score);
      host.appendChild(card);
    });
  });
}

// ── Board rendering ────────────────────────────────────────

function renderRounds() {
  var host = el('round-tabs');
  host.innerHTML = '';
  var labels = {
    single: T('tab.single'),
    double: T('tab.double'),
    final: T('tab.final')
  };
  ['single', 'double', 'final'].forEach(function (r) {
    var b = make('button', null, labels[r]);
    b.type = 'button';
    if (S.round === r) b.classList.add('is-now');
    else if (S.roundsDone.indexOf(r) !== -1) b.classList.add('is-done');
    b.disabled = true;
    host.appendChild(b);
  });
}

function renderBoard() {
  var host = el('board');
  host.innerHTML = '';
  if (!S.board.length) return;

  S.board.forEach(function (col) {
    var head = make('div', 'cat-head');
    head.appendChild(make('span', 'cat-name', col.category));
    head.appendChild(make('span', 'cat-fa', persianSubtitle(col)));
    host.appendChild(head);
  });

  for (var row = 0; row < 5; row++) {
    for (var col = 0; col < S.board.length; col++) {
      host.appendChild(tile(col, row));
    }
  }
  renderPodiums();
  startBoardClock();
}

function tile(col, row) {
  var cell = S.board[col].cells[row];
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'tile';
  btn.dataset.col = col;
  btn.dataset.row = row;
  btn.appendChild(make('span', 'amt', fmt(cell.value)));

  var isOpen = S.clueCtx && S.clueCtx.col === col && S.clueCtx.row === row && S.clue;
  if (isOpen) btn.classList.add('shine', 'is-on');
  else if (S.cursor.col === col && S.cursor.row === row && !cell.solved) {
    btn.classList.add('shine', 'is-on');
  }
  if (cell.solved) {
    btn.disabled = true;
  } else {
    btn.addEventListener('click', function () { openClue(col, row); });
  }
  return btn;
}

// ── Clocks ─────────────────────────────────────────────────

/* The clue clock counts the buzz window and then the answering window; running
   out is a wrong answer either way, the same as the engine's
   handleAnsweringTimeout. The board clock has no engine counterpart — the
   native build waits for a contestant to choose — so it is the web build's own
   pacing: pick in time or the show picks for you. */

/* A clock is a host element filled once with a dial, a number and a label. After
   that it is driven by exactly two things: the text in .clock-num, and the --t
   custom property, which the stylesheet turns into the dial's depletion mask.
   The markup is built here rather than written out three times in index.html. */
function buildClock(node) {
  if (!node || node.firstChild) return;
  node.innerHTML =
    '<span class="clock-dial">' +
      '<span class="clock-track clock-cut"></span>' +
      '<span class="clock-arc clock-cut">' +
        '<span class="clock-ring clock-cut"></span>' +
      '</span>' +
    '</span>' +
    '<span class="clock-text">' +
      '<span class="clock-num"></span>' +
      '<span class="clock-label"></span>' +
    '</span>';
}

/* --t is the share of the dial still lit. It is written once a second; the CSS
   transition carries it across the gap, so the ring drains rather than steps. */
function paintClock(node, seconds, total, label, urgent) {
  buildClock(node);
  var digits = node.querySelector('.clock-num');
  var lab = node.querySelector('.clock-label');
  /* num(), not String(): the countdown is read by the player. The local is not
     called `num` because that would shadow the helper and leave Latin digits on
     a Persian board. The --t property below stays ASCII — it feeds a calc(). */
  if (digits) digits.textContent = num(seconds);
  if (lab) lab.textContent = label;
  node.style.setProperty('--t', String(Math.max(0, seconds) / total));
  node.classList.toggle('is-urgent', seconds <= urgent);
}

function stopClockNode(node) {
  if (!node) return;
  node.hidden = true;
  node.classList.remove('is-urgent');
  /* Reset while hidden, where display:none makes the change instant, so the next
     run opens on a full dial instead of filling up from wherever this one died. */
  node.style.setProperty('--t', '1');
}

function stopClueClock() {
  if (S.clueTimer) { clearInterval(S.clueTimer); S.clueTimer = null; }
  stopClockNode(el('clue-clock'));
}

function startClueClock(seconds, label, onExpire, urgentAt) {
  stopClueClock();
  var node = el('clue-clock');
  if (!node) return;
  /* When the clock goes amber is passed in, because a six-second read window
     would otherwise be urgent from its first tick. */
  var urgent = urgentAt == null ? 5 : urgentAt;
  S.clueRemaining = seconds;
  node.hidden = false;

  var paint = function () {
    paintClock(node, S.clueRemaining, seconds, label, urgent);
  };
  paint();

  S.clueTimer = setInterval(function () {
    S.clueRemaining -= 1;
    if (S.clueRemaining <= 0) { stopClueClock(); onExpire(); return; }
    paint();
  }, 1000);
}

function stopBoardClock() {
  if (S.boardTimer) { clearInterval(S.boardTimer); S.boardTimer = null; }
  stopClockNode(el('board-clock'));
}

function startBoardClock() {
  stopBoardClock();
  var node = el('board-clock');
  /* Nobody can pick a clue they cannot see, so the clock stays down for as
     long as the round card is up. showRoundCard starts it on the way out. */
  if (!node || !anyUnsolved() || S.roundCardOn) return;
  S.boardRemaining = BOARD_SECONDS;
  node.hidden = false;

  var paint = function () {
    paintClock(node, S.boardRemaining, BOARD_SECONDS, T('clock.pick'), 5);
  };
  paint();

  S.boardTimer = setInterval(function () {
    S.boardRemaining -= 1;
    if (S.boardRemaining <= 0) { stopBoardClock(); autoPick(); return; }
    paint();
  }, 1000);
}

/* The cursor is where a contestant is already pointing, so that is what the
   clock opens; failing that, the first clue still on the board. */
function autoPick() {
  var col = S.board[S.cursor.col];
  if (col && !col.cells[S.cursor.row].solved) {
    openClue(S.cursor.col, S.cursor.row);
    return;
  }
  for (var c = 0; c < S.board.length; c++) {
    for (var r = 0; r < S.board[c].cells.length; r++) {
      if (!S.board[c].cells[r].solved) { openClue(c, r); return; }
    }
  }
}

// ── Clue flow ──────────────────────────────────────────────

function anyUnsolved() {
  return S.board.some(function (col) {
    return col.cells.some(function (c) { return !c.solved; });
  });
}

function currentValue() {
  return S.clue ? S.clue.value : 0;
}

/* The native clue view shrinks long clue text to fit (a minimumScaleFactor of
   0.68) rather than letting it run over the header. Long Final Jeopardy clues
   will otherwise overflow the centred clue body and collide with the category
   bar. Reset to the stylesheet size first so repeated calls cannot ratchet. */
function fitClueText() {
  var text = el('clue-text');
  if (!text) return;
  text.style.fontSize = '';
  var base = parseFloat(getComputedStyle(text).fontSize);
  if (!base) return;
  var body = text.parentNode;
  var cs = getComputedStyle(body);
  var avail = body.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
  // A hidden pane or a screen that has not been laid out yet reports no space;
  // shrinking against that would strand the text at its floor.
  if (avail <= 0) return;
  var size = base;
  var floor = base * 0.68;
  while (size > floor && text.getBoundingClientRect().height > avail) {
    size -= 1;
    text.style.fontSize = size + 'px';
  }
}

function openClue(col, row) {
  var cell = S.board[col].cells[row];
  if (!cell || cell.solved) return;

  stopBoardClock();
  S.clue = cell.clue;
  S.clueCtx = { col: col, row: row };
  S.lockedOut = [];
  S.buzzed = null;
  S.holder = null;
  S.armed = false;

  if (cell.dailyDouble) {
    Sound.sfx('wager');
    Sound.voice('host_wager', 0.85);
    var who = S.players.length ? Math.floor(Math.random() * S.players.length) : 0;
    S.mode = 'dd';
    S.holder = who;
    askWager({
      title: T('wager.dailyDouble'),
      category: cell.clue.category,
      subtitle: S.players[who].name + T('dd.solo'),
      value: cell.value,
      playerIndex: who,
      onLock: function (amount) {
        S.clue.value = amount;
        startClue(false);
      }
    });
    return;
  }
  S.mode = 'board';
  startClue(true);
}

function startClue(withBuzzers) {  if (S.earlyTimer) clearTimeout(S.earlyTimer);
  stopClueClock();
  Bots.cancel();
  S.phase = 'reading';
  S.armed = false;
  S.prematureUntil = {};
  S.buzzed = null;
  S.writePrompted = false;
  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = fmtT(S.clue.value);
  el('clue-text').textContent = S.clue.clue;
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  show('clue');
  renderPodiums();
  renderClueActions();
  fitClueText();
  /* The clock, the lamp and the buzz row all arrive with this render, and the
     box they leave the clue is what the fit is measured against — a box that is
     not final until the browser has laid the frame out. A re-fit on the next
     frame is what makes the difference between a clue that is fitted and one
     that is merely cut off at its own bottom edge. */
  requestAnimationFrame(fitClueText);

  if (!withBuzzers) {
    // Daily Double: the holder answers alone, no race.
    S.phase = 'answering';
    S.buzzed = S.holder;
    Sound.music('thinking_loop');
    Sound.sfx('armed');
    renderClueActions();
    renderPodiums();
    startClueClock(ANSWER_SECONDS, T('clock.answer'), function () { answer(-1); });
    requestAnimationFrame(fitClueText);
    Bots.onFloor(S.holder);
    return;
  }

  Sound.music('thinking_loop');
  /* The read window is the clock's, not a timer's: when it runs out the buzzers
     open and a fresh clock takes over. One mechanism, so the two windows can
     never disagree about which one is running. */
  startClueClock(READ_SECONDS, T('clock.read'), openBuzzers, 3);
}

/* The clue has been read. The lamp goes live and the race starts. */
function openBuzzers() {
  if (S.phase !== 'reading') return;
  S.armed = true;
  Sound.sfx('armed');
  renderClueActions();
  startClueClock(BUZZ_SECONDS, T('clock.buzz'), expireBuzz);
  /* The lamp goes live and the read clock becomes the buzz clock, so the clue's
     box changes here too, and this is the window the contestant is reading in. */
  requestAnimationFrame(fitClueText);
  Bots.armBuzzers();
}

/* Nobody took the clue in time. */
function expireBuzz() {
  if (S.phase !== 'reading') return;
  Sound.sfx('incorrect', 0.5);
  resolve(false, S.clue, null, null);
}

/* The lamp that tells the room when the buzzers are actually open. It sits
   directly above the buzzers rather than in the clue bar, because it is the
   thing a contestant's eye has to catch without leaving the question. */
function buzzNotifier() {
  var wrap = make('span', 'buzz-lamp' + (S.armed ? ' is-live' : ''));
  wrap.id = 'buzz-lamp';
  wrap.appendChild(make('i', 'lamp'));
  wrap.appendChild(make('b', 'lamp-word', T(S.armed ? 'buzz.lampOn' : 'buzz.lampOff')));
  return wrap;
}

function renderClueActions() {
  var host = el('clue-actions');
  host.innerHTML = '';

  if (S.phase === 'reading') {
    host.appendChild(buzzNotifier());

    var row = make('div', 'buzz-row' + (S.armed ? ' is-live' : ''));
    var early = null;
    S.players.forEach(function (p, i) {
      var b = document.createElement('button');
      b.type = 'button';
      var cooled = S.prematureUntil[i] > Date.now();
      if (cooled) early = p.name;
      b.className = 'buzz-btn' + (cooled ? ' is-early' : '');
      b.style.setProperty('--pc', p.color);
      /* A premature press is not swallowed — it costs. The button stays live
         through the arm delay precisely so an itchy thumb can be punished. */
      b.disabled = (S.armed && cooled) || S.lockedOut.indexOf(i) !== -1;
      b.appendChild(make('span', null, T('buzz.with', { name: p.name })));
      b.appendChild(make('small', null, num(i + 1)));
      b.addEventListener('click', function () { buzz(i); });
      row.appendChild(b);
    });
    host.appendChild(row);

    var hint;
    if (S.lockedOut.length) {
      hint = T('buzz.out');
    } else if (early) {
      hint = T('buzz.early', { name: early });
    } else if (S.armed) {
      hint = T('buzz.live');
    } else {
      hint = T('buzz.wait');
    }
    host.appendChild(make('p', 'hint', hint));
    return;
  }

  if (S.phase === 'answering') {
    var isFinal = S.mode === 'final';
    /* A robot holding the floor gets no live controls: the buttons are there to
       be watched, not pressed, and a human is not allowed to answer for it. */
    var bot = Bots.isBot(S.buzzed);

    /* Write-in mode replaces the board's four choices with the box. Painting
       the choices underneath would hand the clue to anyone who glances at
       them, which is the one thing the mode exists to prevent. */
    if (S.answerMode === 'write') {
      host.appendChild(writeField(bot, isFinal));
      Pads.syncOptions();
      return;
    }

    var opts = make('div', 'options');
    S.clue.options.forEach(function (text, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'option';
      b.disabled = bot;
      /* The keycap names a physical key, so A–D stay Latin in both languages and
         are bidi-isolated rather than mirrored. The fallback is a position. */
      b.appendChild(make('span', 'key lat', 'ABCD'[i] || num(i + 1)));
      b.appendChild(make('span', null, text));
      b.addEventListener('click', function () {
        if (isFinal) submitFinalAnswer(i); else answer(i);
      });
      opts.appendChild(b);
    });
    host.appendChild(opts);
  }

  /* Fresh buttons mean the controller's cursor has to be put back on the first
     one — otherwise the pad has no visible position from which to move. The
     write field is not a pad target, so the option row keeps the cursor. */
  Pads.syncOptions();
}

/* ── The write-in field ───────────────────────────────────────
   One text box for the contestant holding the floor. It is a text input and
   not a `<textarea>` because the answer is a name, a title, a date — one line,
   and Enter has to mean "lock it in".

   A robot's turn is the same box, disabled, with its answer appearing in it a
   character at a time: the room has to be able to watch it get the clue wrong
   the way a person does, rather than see the verdict arrive out of nowhere. */
function writeField(bot, isFinal) {
  var wrap = make('div', 'write-field' + (bot ? ' is-bot' : ''));

  var input = document.createElement('input');
  input.type = 'text';
  input.className = 'write-input';
  input.setAttribute('autocomplete', 'off');
  input.setAttribute('autocorrect', 'off');
  input.setAttribute('autocapitalize', 'off');
  input.setAttribute('spellcheck', 'false');
  input.setAttribute('placeholder', T('clue.writePlaceholder'));
  input.setAttribute('aria-label', T('clue.writePlaceholder'));
  input.disabled = bot;

  var submit = make('button', 'write-submit', T('clue.submit'));
  submit.type = 'button';
  submit.disabled = bot;

  var fire = function () {
    var text = input.value;
    if (!text.trim()) return;
    if (isFinal) submitFinalWritten(text); else answerWritten(text);
  };
  submit.addEventListener('click', fire);
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') { ev.preventDefault(); fire(); }
  });

  wrap.appendChild(input);
  wrap.appendChild(submit);
  wrap.appendChild(make('p', 'write-hint', T('clue.writeHint')));
  if (!bot) setTimeout(function () { if (!input.disabled) input.focus(); }, 0);
  return wrap;
}

function buzz(playerIndex) {
  if (S.mode !== 'board') return;
  if (S.phase !== 'reading') return;
  if (S.lockedOut.indexOf(playerIndex) !== -1) return;

  /* Jumping the lamp is a foul, not a no-op: the thumb goes in the sin bin for
     the engine's own penalty window while everyone else stays live. */
  if (S.prematureUntil[playerIndex] > Date.now()) return;
  if (!S.armed) { prematureBuzz(playerIndex); return; }

  Sound.sfx('buzz');
  S.buzzed = playerIndex;
  S.phase = 'answering';
  S.writePrompted = false;
  renderClueActions();
  renderPodiums();
  startClueClock(ANSWER_SECONDS, T('clock.answer'), function () { answer(-1); });
  Bots.onFloor(playerIndex);
}

function prematureBuzz(playerIndex) {
  S.prematureUntil[playerIndex] = Date.now() + PREMATURE_MS;
  Sound.sfx('incorrect', 0.4);
  renderClueActions();
  /* The lamps come on mid-penalty, so the row has to be repainted when it
     lifts — otherwise a cooled-out contestant keeps a dead button all clue. */
  if (S.earlyTimer) clearTimeout(S.earlyTimer);
  S.earlyTimer = setTimeout(function () {
    S.earlyTimer = null;
    if (S.phase === 'reading') renderClueActions();
  }, PREMATURE_MS + 20);
}

/* Both ways of answering a clue land here. They differ only in how the verdict
   was reached, so the scoring, the lockout, the reveal and the terminal test
   live here once and the two front doors stay thin.

   `result` carries: `correct`, `timedOut`, `mark` (the option to light up, or
   -1 for a timeout, or null when there is no option to light), `said` (the
   contestant's own words, for write-in) and `note` (a line the judge wants
   spoken before the answer is revealed). */
function answerWith(result) {
  if (S.mode === 'final') return;
  if (S.phase !== 'answering' || S.buzzed == null) return;
  stopClueClock();
  Bots.cancel();

  var clue = S.clue;
  var isCorrect = result.correct === true;
  var timedOut = result.timedOut === true;
  var player = S.players[S.buzzed];
  player.score += isCorrect ? clue.value : -clue.value;

  var remaining = null;
  if (!isCorrect && S.mode !== 'dd') {
    S.lockedOut.push(S.buzzed);
    remaining = S.players.filter(function (_, i) {
      return S.lockedOut.indexOf(i) === -1;
    });
  }
  /* Nothing may give the answer away while a contestant can still steal the
     clue. A Daily Double is answered alone, so its miss ends it there — the
     engine marks the slot solved instead of passing it round. */
  var terminal = isCorrect || S.mode === 'dd' || remaining.length === 0;

  var buttons = el('clue-actions').querySelectorAll('.option');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].disabled = true;
    if (!timedOut && result.mark != null && i === result.mark) {
      buttons[i].classList.add('shine', 'is-on');
      buttons[i].classList.add(isCorrect ? 'is-right' : 'is-wrong');
    } else if (terminal && i === clue.correct) {
      buttons[i].classList.add('is-right');
    } else {
      buttons[i].classList.add('is-dim');
    }
  }

  var field = el('clue-actions').querySelector('.write-input');
  if (field) { field.disabled = true; field.blur(); }
  var submit = el('clue-actions').querySelector('.write-submit');
  if (submit) submit.disabled = true;

  /* A right answer's sting belongs to `showVerdict`, which is about to play it
     — playing it here as well puts two copies of the same cue on the same
     frame, which is one ding heard twice rather than a louder ding. A miss has
     no sting there, so this stays the only place a miss gets one. */
  if (!isCorrect) Sound.sfx('incorrect');
  /* Re-render: a lockout recorded above has to put the badge on the podium. */
  renderPodiums();

  var mark = timedOut ? -1 : (result.mark == null ? null : result.mark);
  var extra = { said: result.said || null, note: result.note || null };

  if (!terminal) {
    showVerdict('wrong', clue, player, mark, true, extra);
    return;
  }
  resolve(isCorrect, clue, player, mark, extra);
}

/* optionIndex is -1 when the answering window ran out. The engine counts a
   timeout as a wrong answer, so it costs the contestant the clue and passes it
   along exactly like a miss. */
function answer(optionIndex) {
  if (S.mode === 'final') return;
  if (S.phase !== 'answering' || S.buzzed == null) return;
  if (optionIndex < 0) return answerWith({ correct: false, timedOut: true, mark: -1 });
  answerWith({ correct: optionIndex === S.clue.correct, mark: optionIndex });
}

/* A typed answer. The judge is the only thing that decides this one — there is
   no index to compare. A "prompt" is not a wrong answer: the host is asking
   which Fazlollah, and the clock keeps running while the contestant says. */
function answerWritten(text) {
  if (S.mode === 'final') { submitFinalWritten(text); return; }
  if (S.phase !== 'answering' || S.buzzed == null) return;
  if (!text || !text.trim()) return;

  var verdict = window.Answers.judge(text, S.clue, { noPrompt: !!S.writePrompted });

  if (verdict.result === 'prompt') {
    S.writePrompted = true;
    var field = el('clue-actions').querySelector('.write-input');
    if (field) { field.focus(); field.select(); }
    Sound.sfx('select', 0.5);
    showHostAside(T(verdict.clarification));
    return;
  }

  answerWith({
    correct: verdict.result === 'correct',
    mark: null,
    said: text,
    /* The confusion rules reject a specific wrong person — his father, the
       wrong Qajar — and the reason is the useful half of that verdict, so it
       is spoken rather than left to a random taunt. */
    note: verdict.clarification ? T(verdict.clarification) : null
  });
}

/* A line from the host that is not a verdict: the judge asking for a surname,
   which leaves the question live. It borrows the verdict slab's styling
   without any of its consequences, and the next real verdict replaces it. */
function showHostAside(text) {
  Sound.cut();
  var host = el('clue-verdict');
  host.hidden = false;
  host.innerHTML = '';
  host.className = 'verdict aside';
  host.appendChild(make('div', 'head', T('verdict.says')));
  host.appendChild(make('p', 'host-line', '“' + text + '”'));
  host.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function resolve(isCorrect, clue, player, optionIndex, extra) {
  S.phase = 'resolved';
  showVerdict(isCorrect ? 'right' : 'wrong', clue, player, optionIndex, false, extra);
}

function showVerdict(kind, clue, player, optionIndex, canRetry, extra) {
  /* A new verdict takes the floor — whatever she was saying about the last one
     is about the last one. */
  Sound.cut();
  var host = el('clue-verdict');
  host.hidden = false;
  host.innerHTML = '';
  host.className = 'verdict ' + (kind === 'right' ? 'right' : 'wrong');

  var timedOut = optionIndex != null && optionIndex < 0;

  var head;
  if (kind === 'right') head = T('verdict.correct', { name: player.name, value: fmt(clue.value) });
  else if (canRetry) head = T('verdict.lockedOut', { name: player.name });
  else if (player == null) head = T(S.lockedOut.length ? 'verdict.nobody' : 'verdict.nobodyBuzzed');
  else if (timedOut) head = T('verdict.tooSlow', { name: player.name, value: fmt(-clue.value) });
  else head = T('verdict.wrong', { name: player.name, value: fmt(-clue.value) });
  host.appendChild(make('div', 'head', head));

  /* `wrongLine` spells out the answer, so it waits for the terminal screen. A
     miss that the others can still steal gets a taunt that gives nothing away.
     Those taunts live in the string table as keys, because the host's nastiness
     has to survive translation. */
  var line = kind === 'right' ? clue.correctLine : (canRetry ? null : clue.wrongLine);
  if (!line && extra && extra.note) line = extra.note;
  if (!line && canRetry) {
    line = T(LOCKOUT_LINES[Math.floor(Math.random() * LOCKOUT_LINES.length)]);
  }
  if (line) host.appendChild(make('p', 'host-line', '“' + line + '”'));

  /* A typed answer is worth reading back before it is contradicted: the
     contestant has to see what was judged, not only that it was wrong. */
  if (extra && extra.said) {
    host.appendChild(make('p', 'you-wrote', T('verdict.youWrote', { text: extra.said })));
  }

  /* The answer, the explanation and the source all give the clue away, so they
     wait until the last contestant has had their shot. */
  if (!canRetry) {
    var ans = make('p', 'answer');
    ans.appendChild(document.createTextNode(T('verdict.answer')));
    ans.appendChild(make('b', null, clue.answer));
    host.appendChild(ans);

    if (clue.explanation) host.appendChild(make('p', 'explain', clue.explanation));

    var src = [clue.book, clue.author, clue.page ? T('verdict.sourcePage', { n: num(clue.page) }) : null]
      .filter(Boolean).join(' · ');
    if (src) host.appendChild(make('div', 'source', src));
  }

  var next = make('button', 'next-btn', T(canRetry ? 'verdict.secondChance' : 'verdict.continue'));
  next.type = 'button';
  next.addEventListener('click', function () {
    if (canRetry) {
      Sound.cut();
      S.buzzed = null;
      S.phase = 'reading';
      S.armed = true;
      S.prematureUntil = {};
      /* A fresh steal is a fresh question to the judge: the next contestant is
         not inheriting the previous one's demand for a full name. */
      S.writePrompted = false;
      host.hidden = true;
      host.innerHTML = '';
      Sound.music('thinking_loop');
      renderClueActions();
      renderPodiums();
      startClueClock(BUZZ_SECONDS, T('clock.buzz'), expireBuzz);
      Bots.armBuzzers();
      return;
    }
    closeClue();
  });
  host.appendChild(next);

  /* The sting states the outcome; she comments on it a beat later. Every
     verdict gets a line now, not just the right ones. */
  if (kind === 'right') Sound.sfx('correct', 0.5);
  Sound.hostLine(kind === 'right' ? 'right' : 'wrong');
  host.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function closeClue() {
  /* The clue is over; so is her comment on it. */
  Sound.cut();
  if (S.clueCtx) S.board[S.clueCtx.col].cells[S.clueCtx.row].solved = true;
  S.clue = null;
  S.clueCtx = null;
  S.buzzed = null;
  S.lockedOut = [];
  S.phase = 'idle';
  stopClueClock();
  /* Back to the board bed rather than silence — the theme runs the whole show. */
  Sound.music('menu_theme');

  if (!anyUnsolved()) {
    if (S.round === 'single') {
      S.roundsDone.push('single');
      S.round = 'double';
      S.board = buildBoard('double');
      Sound.sfx('round2_bumper');
      show('board');
      renderRounds();
      renderBoard();
      showRoundCard(T('round.double.kicker'), T('round.double.title'));
      return;
    }
    startFinal();
    return;
  }

  show('board');
  renderRounds();
  renderBoard();
}

// ── Wagers (Daily Double and Final) ────────────────────────

function maxWager(player) {
  return Math.max(player.score > 0 ? player.score : 0, MAX_WAGER);
}

function askWager(opts) {
  el('wager-category').textContent = opts.category;
  el('wager-value').textContent = opts.title;
  el('wager-prompt').textContent = opts.subtitle;
  el('wager-control').innerHTML = '';
  el('wager-actions').innerHTML = '';

  var player = S.players[opts.playerIndex] || S.players[0];
  var max = maxWager(player);
  var amount = Math.min(Math.max(player.score, 0) || Math.round(max / 2), max);

  /* A quarter of the maximum has to be reachable on the slider, or "Quarter"
     snaps to a neighbouring grid point and a 200M max reads 30M. Scores and
     clue values are always whole millions, so one of these always divides the
     max into exact quarters; 1 is the guaranteed fallback. */
  var step = [10, 5, 1].filter(function (c) { return max % (c * 4) === 0; })[0] || 1;

  var display = make('div', 'wager-amount', fmtT(amount));
  var range = document.createElement('input');
  range.type = 'range';
  range.className = 'wager-range';
  range.min = '0';
  range.max = String(max);
  range.step = String(step);
  range.value = String(amount);
  range.setAttribute('aria-label', T('wager.amountAria'));

  var quick = make('div', 'wager-buttons');
  [[0.25, 'wager.quickQuarter'], [0.5, 'wager.quickHalf'],
   [0.75, 'wager.quickThreeQuarters'], [1, 'wager.quickAll']].forEach(function (pair) {
    var b = make('button', null, T(pair[1]));
    b.type = 'button';
    b.addEventListener('click', function () {
      amount = Math.min(max, Math.round(max * pair[0] / step) * step);
      range.value = String(amount);
      display.textContent = fmtT(amount);
      Sound.sfx('select', 0.4);
    });
    quick.appendChild(b);
  });

  range.addEventListener('input', function () {
    amount = parseInt(range.value, 10);
    display.textContent = fmtT(amount);
  });

  el('wager-control').appendChild(display);
  el('wager-control').appendChild(range);
  el('wager-control').appendChild(quick);

  var lock = make('button', 'primary-btn', T('wager.lock'));
  lock.type = 'button';
  lock.addEventListener('click', function () {
    Sound.sfx('select');
    opts.onLock(amount);
  });
  el('wager-actions').appendChild(lock);

  show('wager');

  /* A robot does not need a slider. It picks its number and locks, and the
     slider walks over to the number it picked so the room can see the size of
     the bet before it is committed. */
  if (Bots.isBot(opts.playerIndex)) {
    Bots.autoWager(opts.playerIndex, max, step, function (value) {
      amount = value;
      range.value = String(value);
      display.textContent = fmtT(value);
    }, lock);
  }
}

function startFinal() {
  S.roundsDone.push('double');
  var finals = CLUES.filter(function (c) { return c.round === 'final'; });
  S.mode = 'final';
  S.clue = shufflingOptions(pick(finals));
  S.clueCtx = null;
  S.lockedOut = [];
  S.finalAnswers = [];
  Sound.music('final');
  /* She announces it, then the Final cue comes up underneath. */
  Sound.voice('host_final', 0.85);
  showRoundCard(T('round.final.kicker'), T('round.final.title'));

  S.finalQueue = S.players.map(function (_, i) { return i; });
  nextFinalWager();
}

function nextFinalWager() {
  if (!S.finalQueue.length) { askFinalAll(); return; }
  var idx = S.finalQueue.shift();
  var player = S.players[idx];
  askWager({
    title: T('wager.final'),
    category: S.clue.category,
    subtitle: player.name + T('wager.place'),
    value: 0,
    playerIndex: idx,
    onLock: function (amount) {
      S.finalAnswers.push({ player: idx, wager: amount });
      nextFinalWager();
    }
  });
}

function askFinalAll() {
  S.finalQueue = S.players.map(function (_, i) { return i; });
  askFinalNext();
}

function askFinalNext() {
  if (!S.finalQueue.length) { finishMatch(); return; }
  var idx = S.finalQueue.shift();
  var entry = S.finalAnswers.filter(function (a) { return a.player === idx; })[0];
  S.mode = 'final';
  S.holder = idx;
  S.clue.value = entry ? entry.wager : 0;
  S.buzzed = idx;
  S.phase = 'answering';
  S.lockedOut = [];
  S.writePrompted = false;

  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = T('wager.finalTag', { value: fmtT(S.clue.value) });
  el('clue-text').textContent = S.clue.clue;
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  show('clue');
  renderPodiums();
  renderClueActions();

  var banner = make('div', 'clock final-clock', '');
  el('clue-actions').insertBefore(banner, el('clue-actions').firstChild);
  fitClueText();
  startFinalClock(idx, banner);
  Bots.onFloor(idx);
}

/* One contestant at a time, thirty seconds each. Running out scores the
   wager against them, the way the engine's timer does. */
function startFinalClock(idx, banner) {
  if (S.finalTimer) clearInterval(S.finalTimer);
  S.finalRemaining = FINAL_SECONDS;
  var label = T('wager.wagerOf', { name: S.players[idx].name, value: fmtT(S.clue.value) });
  var paint = function () {
    paintClock(banner, S.finalRemaining, FINAL_SECONDS, label, 10);
  };
  paint();
  S.finalTimer = setInterval(function () {
    S.finalRemaining -= 1;
    if (S.finalRemaining <= 0) {
      clearInterval(S.finalTimer);
      S.finalTimer = null;
      submitFinalAnswer(-1);
      return;
    }
    paint();
  }, 1000);
}

function submitFinalAnswer(optionIndex) {
  if (optionIndex < 0) return finishFinal({ correct: false, timedOut: true, mark: -1 });
  finishFinal({ correct: optionIndex === S.clue.correct, mark: optionIndex });
}

/* Final is answered alone, so there is no lockout and no steal — but it is
   still answered either from the four choices or from a text box, and the two
   have to reach the same verdict screen. */
function submitFinalWritten(text) {
  if (S.mode !== 'final' || S.phase !== 'answering') return;
  if (!text || !text.trim()) return;
  var verdict = window.Answers.judge(text, S.clue, { noPrompt: !!S.writePrompted });
  if (verdict.result === 'prompt') {
    S.writePrompted = true;
    var field = el('clue-actions').querySelector('.write-input');
    if (field) { field.focus(); field.select(); }
    Sound.sfx('select', 0.5);
    showHostAside(T(verdict.clarification));
    return;
  }
  finishFinal({
    correct: verdict.result === 'correct',
    mark: null,
    said: text,
    note: verdict.clarification ? T(verdict.clarification) : null
  });
}

function finishFinal(result) {
  if (S.mode !== 'final' || S.phase !== 'answering') return;
  Sound.cut();
  if (S.finalTimer) { clearInterval(S.finalTimer); S.finalTimer = null; }
  Bots.cancel();
  var clock = el('clue-actions').querySelector('.final-clock');
  if (clock) clock.remove();
  S.phase = 'resolved';
  var timedOut = result.timedOut === true;
  var idx = S.holder;
  var player = S.players[idx];
  var isCorrect = result.correct === true;
  player.score += isCorrect ? S.clue.value : -S.clue.value;
  Sound.sfx(isCorrect ? 'correct' : 'incorrect');
  renderPodiums();

  var buttons = el('clue-actions').querySelectorAll('.option');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].disabled = true;
    if (!timedOut && result.mark != null && i === result.mark) buttons[i].classList.add('shine', 'is-on');
    if (i === S.clue.correct) buttons[i].classList.add('is-right');
    else if (!timedOut && i === result.mark) buttons[i].classList.add('is-wrong');
    else buttons[i].classList.add('is-dim');
  }
  var field = el('clue-actions').querySelector('.write-input');
  if (field) { field.disabled = true; field.blur(); }
  var submitBtn = el('clue-actions').querySelector('.write-submit');
  if (submitBtn) submitBtn.disabled = true;

  var verdict = el('clue-verdict');
  verdict.hidden = false;
  verdict.className = 'verdict ' + (isCorrect ? 'right' : 'wrong');
  verdict.innerHTML = '';
  verdict.appendChild(make('div', 'head',
    T(timedOut ? 'final.timeUp' : (isCorrect ? 'final.correctLead' : 'final.incorrectLead')) +
    player.name + ' ' + fmt(isCorrect ? S.clue.value : -S.clue.value)));
  if (result.said) {
    verdict.appendChild(make('p', 'you-wrote', T('verdict.youWrote', { text: result.said })));
  }
  /* Everyone answers the same clue, so the answer, the explanation and the
     source wait for the last one to answer — otherwise the first contestant's
     verdict hands the answer to whoever is still sitting there. */
  if (!S.finalQueue.length) {
    var ans = make('p', 'answer');
    ans.appendChild(document.createTextNode(T('verdict.answer')));
    ans.appendChild(make('b', null, S.clue.answer));
    verdict.appendChild(ans);

    if (S.clue.explanation) verdict.appendChild(make('p', 'explain', S.clue.explanation));

    var src = [S.clue.book, S.clue.author, S.clue.page ? T('verdict.sourcePage', { n: num(S.clue.page) }) : null]
      .filter(Boolean).join(' · ');
    if (src) verdict.appendChild(make('div', 'source', src));
  }

  Sound.hostLine(isCorrect ? 'right' : 'wrong');

  var next = make('button', 'next-btn', T(S.finalQueue.length ? 'final.next' : 'final.score'));
  next.type = 'button';
  next.addEventListener('click', function () { askFinalNext(); });
  verdict.appendChild(next);
}

function finishMatch() {
  Sound.cut();
  var ranked = S.players.slice().sort(function (a, b) { return b.score - a.score; });
  var top = ranked[0];
  var tie = ranked.length > 1 && ranked[1].score === top.score;

  el('results-title').textContent = tie
    ? T('results.tie')
    : T('results.winner', { name: top.name });
  var host = el('results-list');
  host.innerHTML = '';
  host.classList.toggle('has-winner', !tie);
  ranked.forEach(function (p, i) {
    var row = make('div', 'result-row');
    /* --i is the finishing order: the rows deal themselves out on it. */
    row.style.setProperty('--pc', p.color);
    row.style.setProperty('--i', String(i));
    if (p.score < 0) row.classList.add('neg');
    if (i === 0 && !tie) row.classList.add('is-winner', 'shine', 'is-on');
    row.appendChild(make('span', 'rank', String(i + 1)));
    row.appendChild(make('span', 'rname', p.name));
    row.appendChild(make('span', 'rscore', fmt(p.score)));
    host.appendChild(row);
  });

  /* The trophy and the title live on across matches, so their entrance has to
     be restarted by hand: drop the class, force a reflow, put it back. */
  var screen = el('screen-results');
  screen.classList.remove('is-dealt');
  void screen.offsetWidth;
  screen.classList.add('is-dealt');

  stopClueClock();
  stopBoardClock();
  Sound.music(null);
  Sound.sfx('winner');
  show('results');
}

// ── Match control ──────────────────────────────────────────

function startMatch() {
  Sound.cut();
  S.players = [];
  for (var i = 0; i < S.playerCount; i++) {
    var raw = (S.names[i] || '').trim();
    /* `mixed` is the couch: the person who set the game up has the leftmost
       podium and everybody to their right is a robot. `bots` is the practice
       room. A robot takes its name from the host's string table rather than the
       field, so a seat keeps its name across a language switch. */
    var bot = Bots.seatIsBot(i);
    S.players.push({
      name: bot ? T('bot.name.' + (i + 1)) : (raw || T('setup.playerDefault', { n: num(i + 1) })),
      score: 0,
      color: PLAYER_COLORS[i],
      bot: bot,
      brain: S.difficulty,
      thumb: bot ? Bots.thumb() : 0
    });
  }
  if (S.finalTimer) clearInterval(S.finalTimer);
  S.finalTimer = null;
  stopClueClock();
  stopBoardClock();
  S.round = 'single';
  S.roundsDone = [];
  S.usedCategories = {};
  S.lockedOut = [];
  S.buzzed = null;
  S.holder = null;
  S.mode = 'board';
  S.phase = 'idle';
  S.clue = null;
  S.clueCtx = null;
  S.finalQueue = [];
  S.finalAnswers = [];
  S.cursor = { col: 0, row: 0 };
  S.board = buildBoard('single');

  Sound.sfx('round1_bumper');
  /* The show's theme carries straight out of the lobby and under the board —
     it is never cut, only ever handed to the clue bed. */
  Sound.music('menu_theme');
  show('board');
  renderRounds();
  renderBoard();
  showRoundCard(T('round.single.kicker'), T('round.single.title'));
}

function initBoardChrome() {
  el('board-menu').addEventListener('click', openMenu);
  el('match-menu').addEventListener('click', function (ev) {
    if (ev.target === el('match-menu')) closeMenu();
    var btn = ev.target.closest('button[data-menu]');
    if (!btn) return;
    var action = btn.dataset.menu;
    closeMenu();
    if (action === 'resume') return;
    if (action === 'restart') { startMatch(); return; }
    if (action === 'lobby') {
      stopClueClock();
      stopBoardClock();
      show('lobby');
      Sound.music('menu_theme');
    }
  });
}

function openMenu() {
  S.menuIndex = 0;
  el('match-menu').hidden = false;
  paintMenu();
  /* The board clock waits while the menu is up. */
  stopBoardClock();
  Sound.sfx('select', 0.4);
}

function closeMenu() {
  el('match-menu').hidden = true;
  if (S.screen === 'board') startBoardClock();
}

function menuButtons() {
  return el('match-menu').querySelectorAll('button[data-menu]');
}

function paintMenu() {
  var btns = menuButtons();
  for (var i = 0; i < btns.length; i++) {
    btns[i].classList.toggle('shine', true);
    btns[i].classList.toggle('is-on', i === S.menuIndex);
  }
}

// ── Input ──────────────────────────────────────────────────

function moveCursor(dc, dr) {
  if (!S.board.length) return;
  var col = Math.min(Math.max(S.cursor.col + dc, 0), S.board.length - 1);
  var row = Math.min(Math.max(S.cursor.row + dr, 0), 4);
  if (col === S.cursor.col && row === S.cursor.row) return;
  S.cursor = { col: col, row: row };
  Sound.sfx('select', 0.3);
  renderBoard();
}

function initKeyboard() {
  document.addEventListener('keydown', function (ev) {
    var menuOpen = !el('match-menu').hidden;
    /* A contestant typing an answer is not pressing A, B, C or 1–4: while a
       field has the keyboard, the field has the keyboard. Enter belongs to the
       field too, which is how the answer is locked in. */
    var typing = ev.target && (ev.target.tagName === 'INPUT' || ev.target.tagName === 'TEXTAREA');

    if (ev.key === 'Escape') {
      if (menuOpen) { closeMenu(); return; }
      if (S.screen === 'board' || S.screen === 'clue') { openMenu(); return; }
    }

    if (menuOpen) {
      var btns = menuButtons();
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault();
        S.menuIndex = (S.menuIndex + (ev.key === 'ArrowDown' ? 1 : btns.length - 1)) % btns.length;
        paintMenu();
        Sound.sfx('select', 0.3);
        return;
      }
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        btns[S.menuIndex].click();
        return;
      }
      return;
    }

    if (S.screen === 'board') {
      if (ev.key === 'ArrowLeft') { ev.preventDefault(); moveCursor(-1, 0); }
      else if (ev.key === 'ArrowRight') { ev.preventDefault(); moveCursor(1, 0); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); moveCursor(0, -1); }
      else if (ev.key === 'ArrowDown') { ev.preventDefault(); moveCursor(0, 1); }
      else if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        openClue(S.cursor.col, S.cursor.row);
      }
      return;
    }

    if (S.screen === 'clue' || S.screen === 'wager') {
      if (typing) return;
      if (S.phase === 'reading') {
        var n = parseInt(ev.key, 10);
        if (n >= 1 && n <= S.players.length) { ev.preventDefault(); buzz(n - 1); }
        return;
      }
      if (S.phase === 'answering') {
        var letter = ev.key.toUpperCase();
        var idx = -1;
        if ('ABCD'.indexOf(letter) !== -1) idx = 'ABCD'.indexOf(letter);
        else if (/^[1-4]$/.test(ev.key)) idx = parseInt(ev.key, 10) - 1;
        if (idx >= 0 && idx < S.clue.options.length) {
          ev.preventDefault();
          if (S.mode === 'final') submitFinalAnswer(idx);
          else answer(idx);
        }
        return;
      }
    }

    if (!typing && (ev.key === 'Enter' || ev.key === ' ')) {
      var next = document.querySelector('#screen-clue .verdict .next-btn, #screen-wager .primary-btn');
      if (next && next.offsetParent !== null) { ev.preventDefault(); next.click(); }
    }
  });
}

// ── Gamepads ───────────────────────────────────────────────

/* One controller per contestant. The browser reports pads in connection order,
   so the first pad plugged in is player 1, the second is player 2, and so on —
   four people on a couch with four controllers each get their own buzzer. Every
   pad also drives the menus, so nobody has to put a controller down mid-match.

   Buttons follow the Gamepad API "standard" mapping, which is what an Xbox pad,
   a DualShock/DualSense and most third-party controllers all report. */

var Pads = (function () {
  var A = 0, B = 1, START = 9, DUP = 12, DDOWN = 13, DLEFT = 14, DRIGHT = 15;
  var DEAD = 0.55;          // stick travel before it counts as a direction
  var FIRST_REPEAT = 380;   // hold a direction this long before it starts stepping
  var REPEAT_RATE = 130;    // then step this often

  /* Which controls a pad can walk through on each screen. Text fields are left
     out on purpose — naming contestants is a keyboard job. */
  var RINGS = {
    splash: '.menu-inline .pill',
    lobby: '.menu .pill',
    setup: '#player-count button, #opponents button, #difficulty button, ' +
           '#answer-mode button, #sound-toggle button, .menu .pill',
    results: '.menu .pill'
  };
  var OVERLAYS = ['match-menu', 'settings-panel', 'howto-panel'];

  var held = {};        // pad index -> last frame's button states
  var repeat = {};      // pad index -> { dir, at }
  var focus = {};       // key -> index into that ring
  var optionFocus = 0;
  var lastScreen = null, lastOverlay = null;

  /* Hold-to-confirm. A multiple-choice clue is committed by holding A until
     the meter fills, so a thumb on its way to the d-pad cannot answer for
     someone. Only the contestant holding the floor gets a meter. */
  var HOLD_MS = 700;
  var holdPad = -1, holdStartedAt = 0, holdNode = null;

  var toastEl = null, toastTimer = null;

  function now() {
    return (window.performance && performance.now) ? performance.now() : Date.now();
  }

  function down(pad, i) {
    var b = pad.buttons[i];
    if (!b) return false;
    return typeof b === 'object' ? (b.pressed || b.value > 0.5) : b > 0.5;
  }

  function direction(pad) {
    if (down(pad, DUP)) return 'up';
    if (down(pad, DDOWN)) return 'down';
    if (down(pad, DLEFT)) return 'left';
    if (down(pad, DRIGHT)) return 'right';
    var x = pad.axes[0] || 0, y = pad.axes[1] || 0;
    if (y < -DEAD) return 'up';
    if (y > DEAD) return 'down';
    if (x < -DEAD) return 'left';
    if (x > DEAD) return 'right';
    return null;
  }

  function connected() {
    var list = navigator.getGamepads ? navigator.getGamepads() : [];
    var out = [];
    for (var i = 0; i < list.length; i++) if (list[i]) out.push(i);
    return out;
  }

  /* A pad's rank among the connected ones, which is the contestant it belongs
     to. Plugging a second pad in shifts nobody — ranks only ever grow. */
  function playerOf(padIndex) {
    var order = connected();
    for (var i = 0; i < order.length; i++) if (order[i] === padIndex) return i;
    return -1;
  }

  function holderHasPad(who) {
    var order = connected();
    return who >= 0 && who < order.length;
  }

  function openOverlay() {
    for (var i = 0; i < OVERLAYS.length; i++) {
      var o = el(OVERLAYS[i]);
      if (o && !o.hidden) return o;
    }
    return null;
  }

  function nodes(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function ringFor(screenId) {
    var sel = RINGS[screenId];
    var s = el('screen-' + screenId);
    return (sel && s) ? nodes(sel, s) : [];
  }

  function paint(ring, i) {
    for (var k = 0; k < ring.length; k++) {
      ring[k].classList.toggle('is-on', k === i);
      ring[k].classList.toggle('shine', k === i);
    }
    if (ring[i] && ring[i].scrollIntoView) {
      ring[i].scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }
  }

  function shift(key, ring, delta) {
    if (!ring.length) return;
    var i = ((focus[key] || 0) + delta) % ring.length;
    if (i < 0) i += ring.length;
    focus[key] = i;
    paint(ring, i);
    Sound.sfx('select', 0.3);
  }

  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'pad-toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 2400);
  }

  /* ── contexts ───────────────────────────────────────────── */

  function wagerRange() {
    return el('wager-control') ? el('wager-control').querySelector('.wager-range') : null;
  }

  function nudgeWager(delta) {
    var range = wagerRange();
    if (!range) return;
    var step = parseInt(range.step, 10) || 100;
    var lo = parseInt(range.min, 10) || 0;
    var hi = parseInt(range.max, 10) || 0;
    var v = parseInt(range.value, 10) + delta * step;
    range.value = String(Math.min(Math.max(v, lo), hi));
    range.dispatchEvent(new Event('input'));
    Sound.sfx('select', 0.3);
  }

  function answerRing() {
    return nodes('#clue-actions .option');
  }

  function paintOptions(ring, i) {
    for (var k = 0; k < ring.length; k++) {
      ring[k].classList.toggle('is-on', k === i);
      ring[k].classList.toggle('shine', k === i);
    }
  }

  function advance() {
    var next = document.querySelector('#screen-clue .verdict .next-btn, #screen-wager .primary-btn');
    if (next && next.offsetParent !== null) next.click();
  }

  /* The option ring a given pad is allowed to answer from, or null when that
     pad has no business touching the clue. */
  function holdRing(padIndex) {
    if (S.screen !== 'clue' || S.phase !== 'answering') return null;
    var ring = answerRing();
    if (!ring.length) return null;
    var who = S.mode === 'final' ? S.holder : S.buzzed;
    if (playerOf(padIndex) !== who && holderHasPad(who)) return null;
    return ring;
  }

  function paintHold(node, p) {
    node.classList.add('is-holding');
    node.style.setProperty('--fill', String(p));
  }

  function endHold() {
    if (holdNode) {
      holdNode.classList.remove('is-holding');
      holdNode.style.removeProperty('--fill');
    }
    holdPad = -1;
    holdStartedAt = 0;
    holdNode = null;
  }

  function commitOption() {
    var ring = answerRing();
    if (!ring.length) return;
    optionFocus = Math.min(optionFocus, ring.length - 1);
    if (S.mode === 'final') submitFinalAnswer(optionFocus);
    else answer(optionFocus);
  }

  function onDir(padIndex, dir) {
    var back = (dir === 'left' || dir === 'up') ? -1 : 1;
    if (S.screen === 'board') {
      moveCursor(dir === 'left' ? -1 : dir === 'right' ? 1 : 0,
                 dir === 'up' ? -1 : dir === 'down' ? 1 : 0);
      return;
    }
    if (S.screen === 'wager') {
      /* The wager is the floor-holder's call alone. S.holder covers both cases —
         the Daily Double picks one contestant at random, Final Jeopardy carries
         the survivor of the earlier rounds. */
      if (playerOf(padIndex) !== S.holder && holderHasPad(S.holder)) return;
      if (dir === 'left' || dir === 'right') nudgeWager(back);
      return;
    }
    if (S.screen === 'clue' && S.phase === 'answering') {
      var ring = answerRing();
      if (!ring.length) return;
      var who = S.mode === 'final' ? S.holder : S.buzzed;
      /* The cursor belongs to whoever holds the floor — a second pad nudging it
         would let someone else walk off with the answer. */
      if (playerOf(padIndex) !== who && holderHasPad(who)) return;
      optionFocus = ((optionFocus + back) % ring.length + ring.length) % ring.length;
      paintOptions(ring, optionFocus);
      Sound.sfx('select', 0.3);
      return;
    }
    shift(S.screen, ringFor(S.screen), back);
  }

  function onConfirm(padIndex) {
    if (S.screen === 'board') {
      if (S.board.length) openClue(S.cursor.col, S.cursor.row);
      return;
    }

    if (S.screen === 'clue' && S.phase === 'reading') {
      var who = playerOf(padIndex);
      if (who >= 0 && who < S.players.length) buzz(who);
      return;
    }

    if (S.screen === 'clue' && S.phase === 'answering') {
      var ring = answerRing();
      if (!ring.length) return;
      var who2 = S.mode === 'final' ? S.holder : S.buzzed;
      var mine = playerOf(padIndex);
      /* Only the contestant holding the floor may answer — unless that player
         has no controller connected, in which case any pad can stand in so a
         one-controller group never gets stuck. */
      if (mine !== who2 && holderHasPad(who2)) return;
      optionFocus = Math.min(optionFocus, ring.length - 1);
      if (S.mode === 'final') submitFinalAnswer(optionFocus);
      else answer(optionFocus);
      return;
    }

    if (S.screen === 'wager') {
      if (playerOf(padIndex) !== S.holder && holderHasPad(S.holder)) return;
      var lock = el('wager-actions') ? el('wager-actions').querySelector('.primary-btn') : null;
      if (lock) { lock.click(); return; }
      advance();
      return;
    }

    if (S.screen === 'clue' || S.screen === 'wager') { advance(); return; }

    if (S.screen === 'splash') {
      var ring0 = ringFor('splash');
      if (ring0.length) ring0[focus.splash || 0].click();
      return;
    }

    var ring2 = ringFor(S.screen);
    if (ring2.length) ring2[focus[S.screen] || 0].click();
  }

  function onBack() {
    var ov = openOverlay();
    if (ov) { ov.hidden = true; Sound.sfx('select', 0.4); return; }
    if (S.screen === 'setup') { el('setup-back').click(); return; }
    if (S.screen === 'board' || S.screen === 'clue') { openMenu(); return; }
    if (S.screen === 'results') { el('play-again').click(); return; }
  }

  function onMenuButton() {
    if (S.screen === 'board' || S.screen === 'clue') {
      if (el('match-menu').hidden) openMenu(); else closeMenu();
    }
  }

  /* ── the loop ───────────────────────────────────────────── */

  function step(padIndex, pad) {
    var was = held[padIndex] || {};
    var is = {};
    for (var b = 0; b < pad.buttons.length; b++) is[b] = down(pad, b);
    held[padIndex] = is;

    var menuEl = openOverlay();
    if (menuEl) {
      /* An open overlay swallows everything so a stray press never reaches the
         board underneath it. */
      var okey = menuEl.id;
      var oring = nodes('button', menuEl);
      if (is[START] && !was[START]) { menuEl.hidden = true; return; }
      if (is[B] && !was[B]) { menuEl.hidden = true; Sound.sfx('select', 0.4); return; }
      var dir = direction(pad);
      var r = repeat[padIndex] || (repeat[padIndex] = { dir: null, at: 0 });
      var t = now();
      if (dir !== r.dir) {
        r.dir = dir; r.at = t + FIRST_REPEAT;
        if (dir) shift(okey, oring, dir === 'up' || dir === 'left' ? -1 : 1);
      } else if (dir && t >= r.at) {
        r.at = t + REPEAT_RATE;
        shift(okey, oring, dir === 'up' || dir === 'left' ? -1 : 1);
      }
      if (is[A] && !was[A]) {
        var ob = oring[focus[okey] || 0];
        if (ob) ob.click();
      }
      return;
    }

    if (S.screen === 'splash') {
      /* The language gate is a two-item ring, so the shared direction handling
         further down moves it — this only has to catch the send. A, B and Start
         all mean "go with the one that is lit": there is nothing behind the
         gate to go back to. */
      if ((is[A] && !was[A]) || (is[B] && !was[B]) || (is[START] && !was[START])) {
        var lring = ringFor('splash');
        if (lring.length) lring[focus.splash || 0].click();
        return;
      }
    }

    /* A hold already under way is advanced before any new edge is read, so the
       meter and the commit stay in step even when the frame rate wobbles. */
    if (holdPad === padIndex) {
      var hring = is[A] ? holdRing(padIndex) : null;
      if (!hring) {
        endHold();
      } else {
        optionFocus = Math.min(optionFocus, hring.length - 1);
        var node = hring[optionFocus];
        if (node !== holdNode) { holdNode = node; holdStartedAt = now(); }
        var filled = Math.min(1, (now() - holdStartedAt) / HOLD_MS);
        paintHold(node, filled);
        if (filled >= 1) { endHold(); commitOption(); return; }
      }
    }

    if (is[START] && !was[START]) { onMenuButton(); return; }
    if (is[B] && !was[B]) { onBack(); return; }
    if (is[A] && !was[A]) {
      if (holdRing(padIndex)) {
        holdPad = padIndex;
        holdStartedAt = now();
        holdNode = null;
        Sound.sfx('select', 0.3);
        return;
      }
      onConfirm(padIndex);
      return;
    }

    /* Direction, with auto-repeat so crossing a six-by-five board or a long
       menu doesn't mean twenty separate presses. */
    var d = direction(pad);
    var rr = repeat[padIndex] || (repeat[padIndex] = { dir: null, at: 0 });
    var tt = now();
    if (d !== rr.dir) {
      rr.dir = d; rr.at = tt + FIRST_REPEAT;
      if (d) onDir(padIndex, d);
    } else if (d && tt >= rr.at) {
      rr.at = tt + REPEAT_RATE;
      onDir(padIndex, d);
    }
  }

  function frame() {
    var list = navigator.getGamepads ? navigator.getGamepads() : [];
    var any = false;

    for (var i = 0; i < list.length; i++) {
      if (!list[i]) continue;
      any = true;
      /* Re-read the ring whenever the screen changes so focus starts at the
         top of the new one rather than wherever it sat on the last. */
      if (S.screen !== lastScreen) {
        lastScreen = S.screen;
        focus[S.screen] = 0;
        optionFocus = 0;
        var fresh = ringFor(S.screen);
        if (fresh.length) paint(fresh, 0);
      }
      var ov = openOverlay();
      if (ov && ov.id !== lastOverlay) {
        lastOverlay = ov.id;
        focus[ov.id] = 0;
        paint(nodes('button', ov), 0);
      } else if (!ov) {
        lastOverlay = null;
      }
      step(i, list[i]);
    }

    /* Nothing connected: drop the edge state so a reconnected pad doesn't fire
       a burst of stale presses. */
    if (!any) { held = {}; repeat = {}; }
  }

  function init() {
    window.addEventListener('gamepadconnected', function (ev) {
      var rank = connected().length;
      var name = (ev.gamepad && ev.gamepad.id || T('pad.controller')).split(' (')[0];
      toast(T('pad.player', { n: num(Math.max(rank, 1)), name: name }));
    });
    window.addEventListener('gamepaddisconnected', function () {
      toast(T('pad.disconnected'));
    });
    /* Polled on a timer rather than requestAnimationFrame: this is input
       sampling, not animation, and rAF stops dead whenever the compositor has
       nothing to paint — which is exactly when a buzzer must still land. */
    setInterval(frame, 16);
  }

  /* Public so the clue renderer can hand the pad a starting position. */
  function syncOptions() {
    var ring = answerRing();
    if (!ring.length) return;
    optionFocus = 0;
    paintOptions(ring, 0);
  }

  return {
    init: init,
    syncOptions: syncOptions,
    count: function () { return connected().length; }
  };
})();

function initGamepads() { Pads.init(); }

// ── The robots ─────────────────────────────────────────────

/* Four brains, one per difficulty. A brain is a set of habits rather than a
   skill score: whether a claw lands on a clue at all — and if so, whether it
   lands because the robot knows the answer or only because it is willing to
   guess — how often it is even paying attention when the read window closes,
   how much of its stack it will put on a wager, and how long it sits on the
   floor before answering. Nothing here reads the other contestants' scores,
   because a robot that plays the room is a different and much less amusing
   opponent than one that plays the clue. */
var Bots = (function () {
  /* `alert` is whether a robot reached for the buzzer at all, and it is the
     difference between a room and an empty studio — a contestant who sits out
     one clue in ten is not playing the game. It runs high on every brain on
     purpose: the difficulty shows in how fast the thumb moves (`quick`), how
     often a clue is there to be taken at all (`nerve`) and how often it is
     right (`accuracy`), never in whether anyone bothered.
     `quick` is the band a robot rings in from when it knows the answer and
     `late` the band it rings from when it is only fishing. Keeping them apart
     is the whole point: one flat band made every robot average, and nobody was
     ever genuinely beaten to the buzzer. */
  var BRAINS = {
    easy:   { quick: [1000, 2100], late: [2600, 7000], nerve: 0.30,
              alert: 0.70, accuracy: 0.38, wager: [0.05, 0.20], think: [1400, 3000] },
    normal: { quick: [700, 1600], late: [2200, 6000], nerve: 0.45,
              alert: 0.85, accuracy: 0.58, wager: [0.10, 0.35], think: [1000, 2200] },
    hard:   { quick: [500, 1200], late: [1800, 5200], nerve: 0.62,
              alert: 0.96, accuracy: 0.78, wager: [0.20, 0.55], think: [700, 1600] },
    brutal: { quick: [380, 900],  late: [1500, 4500], nerve: 0.78,
              alert: 1.00, accuracy: 0.92, wager: [0.35, 0.85], think: [400, 1100] }
  };

  /* A clue's difficulty is the writer's judgement of how hard it is, and the
     robot should feel it: a CASUAL clue is one anybody gets, an INSUFFERABLE
     one is close to a coin flip for most of the couch. This is the only thing
     that lets an easy robot look briefly clever. */
  var NUDGE = { CASUAL: 0.20, STANDARD: 0.0, SCHOLAR: -0.08, INSUFFERABLE: -0.16 };

  var pending = [];      // buzz and wager timers, all short-lived
  var thinkTimer = null;
  var typeTimer = null;

  /* Which seats the roster will hand to a robot. This is the single rule, read
     by the green room when it draws the fields and by startMatch when it fills
     them, so the label and the seat can never disagree. */
  function seatIsBot(idx) {
    if (S.opponents === 'bots') return true;
    if (S.opponents === 'mixed' && idx > 0) return true;
    return false;
  }

  function isBot(idx) {
    return idx != null && S.players[idx] != null && S.players[idx].bot === true;
  }

  function brain(idx) {
    var p = S.players[idx];
    return BRAINS[(p && p.brain) || 'normal'] || BRAINS.normal;
  }

  function accuracy(b, clue) {
    var n = (clue && NUDGE[clue.difficulty]) || 0;
    return Math.max(0.05, Math.min(0.97, b.accuracy + n));
  }

  function cancel() {
    for (var i = 0; i < pending.length; i++) clearTimeout(pending[i]);
    pending = [];
    if (thinkTimer) { clearTimeout(thinkTimer); thinkTimer = null; }
    if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
  }

  function later(fn, ms) {
    var t = setTimeout(function () { fn(); }, ms);
    pending.push(t);
    return t;
  }

  var THUMB_FLOOR = 280;   // below this it is a machine, not a contestant
  var THUMB_SPREAD = 0.20; // how much of itself a seat's habit can add or take
  var THUMB_GAP = 220;     // two thumbs inside this read as one press on screen

  /* A seat's habit, drawn once when the match is built: the robot on your right
     is reliably the jumpy one, which is what a real podium feels like. */
  function thumb() {
    return (Math.random() * 2 - 1) * THUMB_SPREAD;
  }

  /* The buzzers have opened. Each robot has had the whole read window to look at
     the clue, so what it does now is what a contestant does: if it is sure, the
     thumb goes down almost at once; if it is fishing, it comes in late and
     usually wrong. A sure thumb is skewed short — raising the draw to a power
     above one piles them up against the near edge of the band — because a
     reaction time is not uniform; most of them are fast and the slow ones are
     the tail. A fishing thumb is left flat, so the late presses really are
     spread out. */
  function armBuzzers() {
    cancel();
    var ceiling = BUZZ_SECONDS * 1000 - 250;
    var n = (S.clue && NUDGE[S.clue.difficulty]) || 0;
    var calls = [];

    S.players.forEach(function (p, i) {
      if (!isBot(i)) return;
      if (S.lockedOut.indexOf(i) !== -1) return;
      var b = brain(i);
      if (Math.random() > b.alert) return;
      var sure = Math.random() < Math.max(0.08, Math.min(0.95, b.nerve + n * 0.6));
      var band = sure ? b.quick : b.late;
      var draw = Math.random();
      var at = band[0] + (sure ? Math.pow(draw, 1.5) : draw) * (band[1] - band[0]);
      at *= 1 + (p.thumb || 0);
      calls.push({ seat: i, at: at });
    });

    /* Two thumbs inside a fifth of a second is not a race and on screen it reads
       as one press, so the later arrival waits. That is also what happens at a
       real podium. */
    calls.sort(function (a, b) { return a.at - b.at; });
    for (var k = 1; k < calls.length; k++) {
      if (calls[k].at - calls[k - 1].at < THUMB_GAP) {
        calls[k].at = calls[k - 1].at + THUMB_GAP;
      }
    }

    calls.forEach(function (c) {
      var at = Math.max(THUMB_FLOOR, c.at);
      /* Someone else may already have rung in. A press past the window is not a
         steal: the race is over and the room has moved on. */
      if (at > ceiling) return;
      later(function () {
        if (S.phase !== 'reading' || !S.armed) return;
        if (S.lockedOut.indexOf(c.seat) !== -1) return;
        buzz(c.seat);
      }, at);
    });
  }

  /* The floor is a robot's. It thinks, then it answers. */
  function onFloor(idx) {
    cancel();
    if (!isBot(idx)) return;
    var b = brain(idx);
    var delay = b.think[0] + Math.random() * (b.think[1] - b.think[0]);
    thinkTimer = setTimeout(function () {
      thinkTimer = null;
      decide(idx);
    }, delay);
  }

  function wrongIndex(clue) {
    var opts = clue.options || [];
    var pool = [];
    for (var i = 0; i < opts.length; i++) if (i !== clue.correct) pool.push(i);
    return pool.length ? pool[Math.floor(Math.random() * pool.length)] : -1;
  }

  function decide(idx) {
    if (S.phase !== 'answering' || S.buzzed !== idx) return;
    var clue = S.clue;
    if (!clue) return;
    var hit = Math.random() < accuracy(brain(idx), clue);
    var isFinal = S.mode === 'final';

    if (S.answerMode === 'write') {
      /* A miss is a plausible wrong answer drawn from the board's own
         distractors, not noise — a robot that types gibberish is not a robot
         anyone believes in. */
      var miss = wrongIndex(clue);
      var text = hit || miss < 0 ? clue.answer : clue.options[miss];
      typeIn(text, function () {
        if (S.phase !== 'answering' || S.buzzed !== idx) return;
        if (isFinal) submitFinalWritten(text); else answerWritten(text);
      });
      return;
    }

    var pick = hit ? clue.correct : wrongIndex(clue);
    if (isFinal) submitFinalAnswer(pick); else answer(pick);
  }

  /* Typing, not pasting: the answer arrives in the disabled field one character
     at a time, so the room can watch it come in and can see it go wrong before
     the verdict says so. */
  function typeIn(text, done) {
    var field = el('clue-actions').querySelector('.write-input');
    if (!field) { done(); return; }
    var i = 0;
    var step = Math.max(26, Math.min(85, 900 / Math.max(1, text.length)));
    field.value = '';
    typeTimer = setInterval(function () {
      if (S.phase !== 'answering' || !field.isConnected) {
        clearInterval(typeTimer); typeTimer = null;
        return;
      }
      i += 1;
      field.value = text.slice(0, i);
      if (i >= text.length) {
        clearInterval(typeTimer);
        typeTimer = null;
        later(done, 340);
      }
    }, step);
  }

  /* The robot's wager: a band of its own stack, chosen before it sees the
     clue, which is the only honest way to bet. The slider is walked over to the
     number so the room sees the size of the bet before it is committed. */
  function autoWager(idx, max, step, paint, lock) {
    var b = brain(idx);
    var frac = b.wager[0] + Math.random() * (b.wager[1] - b.wager[0]);
    var value = Math.round(max * frac / step) * step;
    value = Math.max(0, Math.min(max, value));
    later(function () {
      paint(value);
      Sound.sfx('select', 0.4);
      later(function () { if (S.screen === 'wager') lock.click(); }, 720);
    }, 900);
  }

  return {
    seatIsBot: seatIsBot, isBot: isBot, cancel: cancel, thumb: thumb,
    armBuzzers: armBuzzers, onFloor: onFloor, autoWager: autoWager
  };
})();

// ── Boot ───────────────────────────────────────────────────

function boot() {
  /* Before anything is built: `renderNames` and every renderer downstream read
     the table through `T`, and half of them write their copy into the DOM at
     the moment they run. */
  setLang(savedLang());
  initLobby();
  initBoardChrome();
  initKeyboard();
  initGamepads();
  renderPodiums();

  // The clue body grows and shrinks as the verdict panel and answer buttons
  // come and go, so re-fit the clue text whenever its box changes.
  var body = document.querySelector('#screen-clue .clue-body');
  if (body && window.ResizeObserver) new ResizeObserver(fitClueText).observe(body);

  /* The theme is the bed the whole show sits on, so it comes up as soon as the
     page does and is never handed back to silence. A browser will refuse that
     first play on a page nobody has touched yet; the gesture listener re-asks,
     and Sound.music clears its slot on a refusal so the second ask is not
     swallowed by the name guard.

     Unless the house lights are still down: the splash underscore owns the
     room until she finishes, and asking for the theme here would fade the
     underscore out from under her first sentence. `doneOpening` is what hands
     over, and it does it at the moment the title card goes live. */
  if (!S.opening) Sound.music('menu_theme');
  var once = function () {
    document.removeEventListener('pointerdown', once);
    document.removeEventListener('keydown', once);
    /* Not while she is talking: a click on the title card must not bring the
       theme up under her line. */
    if (Sound.isEnabled() && !S.opening) Sound.music('menu_theme');
  };
  document.addEventListener('pointerdown', once);
  document.addEventListener('keydown', once);
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();

})();
