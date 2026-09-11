/* JEOPARDY! — Iranian Edition, web build.
   Zero dependencies, zero build step. Open index.html and it plays. */
(function () {
'use strict';

var CLUES = window.CLUES || [];
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

/* The host's per-clue `wrongLine` names the answer, so it is only safe once the
   clue is dead. While the others can still steal it, the host has to be rude
   about something other than the answer. */
var LOCKOUT_LINES = [
  'Wrong. Somebody else want to have a go?',
  'Nope. Who else thinks they know?',
  'Wrong. Anyone else feeling brave?',
  'No. Somebody take it off their hands.',
  'Wrong. The clue is still on the board.'
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
  return (n < 0 ? '−' : '') + Math.abs(n) + 'M';
}

function fmtT(n) {
  return fmt(n) + ' تومان';
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
   than teaching players to always tap the first option. */
function shufflingOptions(clue) {
  var correctText = clue.options[clue.correct];
  var opts = shuffle(clue.options);
  var copy = {};
  for (var k in clue) if (Object.prototype.hasOwnProperty.call(clue, k)) copy[k] = clue[k];
  copy.options = opts;
  copy.correct = opts.indexOf(correctText);
  return copy;
}

// ── Audio ──────────────────────────────────────────────────

var Sound = (function () {
  var enabled = true;
  var musicName = null;
  var musicEl = null;

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

  /* Music is a single slot — switching cues fades the old one out rather
     than stacking loops. */
  function music(name) {
    /* The name guard is what stops a cue restarting on every screen change, but
       it must not outlive the audio itself — an element a duck left paused, or
       one whose first play the browser refused, still counts as "already
       playing" unless we look at it. */
    if (musicName === name && musicEl && !musicEl.paused) return;
    musicName = name;
    if (musicEl) {
      var dying = musicEl;
      var fade = setInterval(function () {
        dying.volume = Math.max(0, dying.volume - 0.06);
        if (dying.volume <= 0.001) { clearInterval(fade); dying.pause(); }
      }, 40);
    }
    musicEl = null;
    if (!enabled || !name) return;
    var a = makeEl(name, 0, true);
    musicEl = a;
    a.volume = 0;
    var play = a.play();
    /* A refused play — the autoplay policy, on a page nobody has touched yet —
       must not leave the slot claimed, or the name guard at the top of this
       function swallows every later attempt and the show runs silent. */
    if (play && play.catch) play.catch(function () {
      if (musicEl === a) { musicEl = null; musicName = null; }
    });
    var rise = setInterval(function () {
      if (musicEl !== a) { clearInterval(rise); return; }
      a.volume = Math.min(0.34, a.volume + 0.04);
      if (a.volume >= 0.34) clearInterval(rise);
    }, 50);
  }

  function sfx(name, volume) {
    if (!enabled || !name) return;
    var a = makeEl(name, volume == null ? 0.7 : volume, false);
    a.play().catch(function () {});
  }

  /* A one-shot cue that takes the floor: the music drops out while it plays
     and comes back when it is done. Used for the host's lines and for the
     opening challenge, which run anywhere from three seconds to fifteen. */
  function voice(name, volume, then) {
    if (!enabled || !name) return;
    var a = makeEl(name, volume == null ? 0.85 : volume, false);
    var ducked = musicName;
    var done = false;
    var guard = null;
    if (ducked) music(null);

    function finish() {
      if (done) return;
      done = true;
      clearTimeout(guard);
      a.pause();
      /* Only restore the cue it interrupted — if the game moved on to a new
         one while it was playing, that cue wins. Failing that, fall back to the
         theme: the show always has a bed, so a cue that ends with the slot
         empty hands the lobby its music back instead of leaving silence. */
      if (enabled && musicName === null) music(ducked || 'menu_theme');
      if (then) then();
    }

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

  function setEnabled(on) {
    enabled = on;
    if (!on) {
      if (musicEl) { musicEl.pause(); musicEl = null; }
      musicName = null;
    }
  }

  return {
    music: music, sfx: sfx, voice: voice,
    setEnabled: setEnabled, isEnabled: function () { return enabled; }
  };
})();

// ── State ──────────────────────────────────────────────────

var S = {
  screen: 'splash',
  playerCount: 3,
  names: ['PLAYER 1', 'PLAYER 2', 'PLAYER 3'],
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
  prematureUntil: {},  // player index -> the moment they may buzz again
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
  boardRemaining: 0
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

// ── Lobby ──────────────────────────────────────────────────

function renderNames() {
  var host = el('names');
  host.innerHTML = '';
  for (var i = 0; i < S.playerCount; i++) {
    (function (idx) {
      var wrap = make('div', 'name-field');
      var dot = make('span', 'dot');
      dot.style.background = PLAYER_COLORS[idx];
      var input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 14;
      input.value = S.names[idx] || '';
      input.setAttribute('aria-label', 'Contestant ' + (idx + 1) + ' name');
      input.addEventListener('input', function () {
        S.names[idx] = input.value;
      });
      wrap.appendChild(dot);
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

  /* The house lights. The theme comes up over the title card, drops out under
     her, and carries on when she is done — so by the time anybody presses
     anything the show is already running. She will not sit through it twice:
     coming back to the title card later leaves the music alone. */
  var runOpening = function () {
    if (S.opening || S.openingDone) return;
    S.opening = true;
    S.openingDone = true;
    el('screen-splash').classList.add('is-opening');
    S.openTimer = setTimeout(function () {
      S.openTimer = null;
      if (S.screen !== 'splash') return;
      /* Sound.voice returns without a callback when the show is muted, which
         would leave the title card locked — so the muted case ends the opening
         here instead of waiting on a cue that was never played. */
      if (!Sound.isEnabled()) { doneOpening(); return; }
      Sound.voice('opening_challenge', 0.9, doneOpening);
    }, OPENING_MUSIC_MS);
  };

  /* Sound.voice always calls back — a missing cue, a refused play and a cue
     that simply ends all arrive here — so the title card can never be left
     locked. */
  var doneOpening = function () {
    S.opening = false;
    el('screen-splash').classList.remove('is-opening');
  };

  var begin = function () {
    if (S.screen !== 'splash' || S.opening) return;
    show('lobby');
    Sound.music('menu_theme');
  };
  el('begin').addEventListener('click', begin);
  document.addEventListener('keydown', function (ev) {
    if (S.screen !== 'splash') return;
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    ev.preventDefault();
    begin();
  });

  el('go-setup').addEventListener('click', function () { Sound.sfx('select'); show('setup'); });
  el('setup-back').addEventListener('click', function () { Sound.sfx('select'); show('lobby'); });
  el('quit-game').addEventListener('click', function () {
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
  el('play-again').addEventListener('click', function () { show('lobby'); Sound.music('menu_theme'); });

  setSoundSegments(Sound.isEnabled());

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
  var labels = { single: 'Round 1', double: 'Double Jeopardy', final: 'Final Jeopardy' };
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

function stopClueClock() {
  if (S.clueTimer) { clearInterval(S.clueTimer); S.clueTimer = null; }
  var node = el('clue-clock');
  if (node) { node.hidden = true; node.textContent = ''; node.classList.remove('is-urgent'); }
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
    node.textContent = label + ' · ' + S.clueRemaining +
      (S.clueRemaining === 1 ? ' SECOND' : ' SECONDS');
    node.classList.toggle('is-urgent', S.clueRemaining <= urgent);
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
  var node = el('board-clock');
  if (node) { node.hidden = true; node.textContent = ''; node.classList.remove('is-urgent'); }
}

function startBoardClock() {
  stopBoardClock();
  var node = el('board-clock');
  if (!node || !anyUnsolved()) return;
  S.boardRemaining = BOARD_SECONDS;
  node.hidden = false;

  var paint = function () {
    node.textContent = 'Pick a clue · ' + S.boardRemaining +
      (S.boardRemaining === 1 ? ' SECOND' : ' SECONDS');
    node.classList.toggle('is-urgent', S.boardRemaining <= 5);
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
      title: 'Daily Double',
      category: cell.clue.category,
      subtitle: S.players[who].name + ", you're on your own here. Wager whatever you dare.",
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
  S.phase = 'reading';
  S.armed = false;
  S.prematureUntil = {};
  S.buzzed = null;
  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = fmtT(S.clue.value);
  el('clue-text').textContent = S.clue.clue;
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  show('clue');
  renderPodiums();
  renderClueActions();
  fitClueText();

  if (!withBuzzers) {
    // Daily Double: the holder answers alone, no race.
    S.phase = 'answering';
    S.buzzed = S.holder;
    Sound.music('thinking_loop');
    Sound.sfx('armed');
    renderClueActions();
    renderPodiums();
    startClueClock(ANSWER_SECONDS, 'Answer', function () { answer(-1); });
    return;
  }

  Sound.music('thinking_loop');
  /* The read window is the clock's, not a timer's: when it runs out the buzzers
     open and a fresh clock takes over. One mechanism, so the two windows can
     never disagree about which one is running. */
  startClueClock(READ_SECONDS, 'Read', openBuzzers, 3);
}

/* The clue has been read. The lamp goes live and the race starts. */
function openBuzzers() {
  if (S.phase !== 'reading') return;
  S.armed = true;
  Sound.sfx('armed');
  renderClueActions();
  startClueClock(BUZZ_SECONDS, 'Buzz', expireBuzz);
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
  wrap.appendChild(make('b', 'lamp-word', S.armed ? 'Buzz' : 'Wait'));
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
      b.appendChild(make('span', null, 'Buzz · ' + p.name));
      b.appendChild(make('small', null, String(i + 1)));
      b.addEventListener('click', function () { buzz(i); });
      row.appendChild(b);
    });
    host.appendChild(row);

    var hint;
    if (S.lockedOut.length) {
      hint = 'Out of it — and someone else wants your money.';
    } else if (early) {
      hint = early + ' jumped it. That is what patience looks like, ' + early + '.';
    } else if (S.armed) {
      hint = 'Buzzers are live. Prove something.';
    } else {
      hint = 'Not yet. Watch the lamp — jump it and you sit out the start.';
    }
    host.appendChild(make('p', 'hint', hint));
    return;
  }

  if (S.phase === 'answering') {
    var isFinal = S.mode === 'final';
    var opts = make('div', 'options');
    S.clue.options.forEach(function (text, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'option';
      b.appendChild(make('span', 'key', 'ABCD'[i] || String(i + 1)));
      b.appendChild(make('span', null, text));
      b.addEventListener('click', function () {
        if (isFinal) submitFinalAnswer(i); else answer(i);
      });
      opts.appendChild(b);
    });
    host.appendChild(opts);
  }

  /* Fresh buttons mean the controller's cursor has to be put back on the first
     one — otherwise the pad has no visible position to move from. */
  Pads.syncOptions();
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
  renderClueActions();
  renderPodiums();
  startClueClock(ANSWER_SECONDS, 'Answer', function () { answer(-1); });
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

/* optionIndex is -1 when the answering window ran out. The engine counts a
   timeout as a wrong answer, so it costs the contestant the clue and passes it
   along exactly like a miss. */
function answer(optionIndex) {
  if (S.mode === 'final') return;
  if (S.phase !== 'answering' || S.buzzed == null) return;
  stopClueClock();

  var clue = S.clue;
  var timedOut = optionIndex < 0;
  var isCorrect = !timedOut && optionIndex === clue.correct;
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
    if (!timedOut && i === optionIndex) {
      buttons[i].classList.add('shine', 'is-on');
      buttons[i].classList.add(isCorrect ? 'is-right' : 'is-wrong');
    } else if (terminal && i === clue.correct) {
      buttons[i].classList.add('is-right');
    } else {
      buttons[i].classList.add('is-dim');
    }
  }

  Sound.sfx(isCorrect ? 'correct' : 'incorrect');
  /* Re-render: a lockout recorded above has to put the badge on the podium. */
  renderPodiums();

  if (!terminal) {
    showVerdict('wrong', clue, player, optionIndex, true);
    return;
  }
  resolve(isCorrect, clue, player, optionIndex);
}

function resolve(isCorrect, clue, player, optionIndex) {
  S.phase = 'resolved';
  showVerdict(isCorrect ? 'right' : 'wrong', clue, player, optionIndex, false);
}

function showVerdict(kind, clue, player, optionIndex, canRetry) {
  var host = el('clue-verdict');
  host.hidden = false;
  host.innerHTML = '';
  host.className = 'verdict ' + (kind === 'right' ? 'right' : 'wrong');

  var timedOut = optionIndex != null && optionIndex < 0;

  var head;
  if (kind === 'right') head = 'Correct. ' + player.name + ' ' + fmt(clue.value);
  else if (canRetry) head = 'Wrong. ' + player.name + ' is locked out';
  else if (player == null) head = S.lockedOut.length ? 'Nobody had it' : 'Nobody even buzzed';
  else if (timedOut) head = 'Too slow, ' + player.name + '. ' + fmt(-clue.value);
  else head = 'Wrong, ' + player.name + '. ' + fmt(-clue.value);
  host.appendChild(make('div', 'head', head));

  /* `wrongLine` spells out the answer, so it waits for the terminal screen. A
     miss that the others can still steal gets a taunt that gives nothing away. */
  var line = kind === 'right' ? clue.correctLine : (canRetry ? null : clue.wrongLine);
  if (!line && canRetry) {
    line = LOCKOUT_LINES[Math.floor(Math.random() * LOCKOUT_LINES.length)];
  }
  if (line) host.appendChild(make('p', 'host-line', '“' + line + '”'));

  /* The answer, the explanation and the source all give the clue away, so they
     wait until the last contestant has had their shot. */
  if (!canRetry) {
    var ans = make('p', 'answer');
    ans.appendChild(document.createTextNode('Answer: '));
    ans.appendChild(make('b', null, clue.answer));
    host.appendChild(ans);

    if (clue.explanation) host.appendChild(make('p', 'explain', clue.explanation));

    var src = [clue.book, clue.author, clue.page ? 'p. ' + clue.page : null]
      .filter(Boolean).join(' · ');
    if (src) host.appendChild(make('div', 'source', src));
  }

  var next = make('button', 'next-btn', canRetry ? 'Second Chance' : 'Continue');
  next.type = 'button';
  next.addEventListener('click', function () {
    if (canRetry) {
      S.buzzed = null;
      S.phase = 'reading';
      S.armed = true;
      S.prematureUntil = {};
      host.hidden = true;
      host.innerHTML = '';
      Sound.music('thinking_loop');
      renderClueActions();
      renderPodiums();
      startClueClock(BUZZ_SECONDS, 'Buzz', expireBuzz);
      return;
    }
    closeClue();
  });
  host.appendChild(next);

  if (kind === 'right') {
    Sound.sfx('correct', 0.5);
    Sound.voice('host_correct', 0.85);
  }
  host.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function closeClue() {
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
  range.setAttribute('aria-label', 'Wager amount');

  var quick = make('div', 'wager-buttons');
  [[0.25, 'Quarter'], [0.5, 'Half'], [0.75, 'Three Quarters'], [1, 'All In']].forEach(function (pair) {
    var b = make('button', null, pair[1]);
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

  var lock = make('button', 'primary-btn', 'Lock It In');
  lock.type = 'button';
  lock.addEventListener('click', function () {
    Sound.sfx('select');
    opts.onLock(amount);
  });
  el('wager-actions').appendChild(lock);

  show('wager');
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

  S.finalQueue = S.players.map(function (_, i) { return i; });
  nextFinalWager();
}

function nextFinalWager() {
  if (!S.finalQueue.length) { askFinalAll(); return; }
  var idx = S.finalQueue.shift();
  var player = S.players[idx];
  askWager({
    title: 'Final Jeopardy',
    category: S.clue.category,
    subtitle: player.name + ', place your wager. You can still back out.',
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

  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = 'Final · ' + fmtT(S.clue.value);
  el('clue-text').textContent = S.clue.clue;
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  show('clue');
  renderPodiums();
  renderClueActions();

  var banner = make('p', 'hint final-clock', '');
  el('clue-actions').insertBefore(banner, el('clue-actions').firstChild);
  fitClueText();
  startFinalClock(idx, banner);
}

/* One contestant at a time, thirty seconds each. Running out scores the
   wager against them, the way the engine's timer does. */
function startFinalClock(idx, banner) {
  if (S.finalTimer) clearInterval(S.finalTimer);
  S.finalRemaining = FINAL_SECONDS;
  var paint = function () {
    banner.textContent = S.players[idx].name + ' answers · wager ' + fmtT(S.clue.value) +
      ' · ' + S.finalRemaining + (S.finalRemaining === 1 ? ' SECOND' : ' SECONDS');
    banner.classList.toggle('is-urgent', S.finalRemaining <= 10);
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
  if (S.mode !== 'final' || S.phase !== 'answering') return;
  if (S.finalTimer) { clearInterval(S.finalTimer); S.finalTimer = null; }
  var clock = el('clue-actions').querySelector('.final-clock');
  if (clock) clock.remove();
  S.phase = 'resolved';
  var timedOut = optionIndex < 0;
  var idx = S.holder;
  var player = S.players[idx];
  var isCorrect = optionIndex === S.clue.correct;
  player.score += isCorrect ? S.clue.value : -S.clue.value;
  Sound.sfx(isCorrect ? 'correct' : 'incorrect');
  renderPodiums();

  var buttons = el('clue-actions').querySelectorAll('.option');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].disabled = true;
    if (i === optionIndex) buttons[i].classList.add('shine', 'is-on');
    if (i === S.clue.correct) buttons[i].classList.add('is-right');
    else if (i === optionIndex) buttons[i].classList.add('is-wrong');
    else buttons[i].classList.add('is-dim');
  }

  var verdict = el('clue-verdict');
  verdict.hidden = false;
  verdict.className = 'verdict ' + (isCorrect ? 'right' : 'wrong');
  verdict.innerHTML = '';
  verdict.appendChild(make('div', 'head',
    (timedOut ? "Time's up — " : (isCorrect ? 'Correct — ' : 'Incorrect — ')) +
    player.name + ' ' + fmt(isCorrect ? S.clue.value : -S.clue.value)));
  var ans = make('p', 'answer');
  ans.appendChild(document.createTextNode('Answer: '));
  ans.appendChild(make('b', null, S.clue.answer));
  verdict.appendChild(ans);

  if (S.clue.explanation) verdict.appendChild(make('p', 'explain', S.clue.explanation));

  var src = [S.clue.book, S.clue.author, S.clue.page ? 'p. ' + S.clue.page : null]
    .filter(Boolean).join(' · ');
  if (src) verdict.appendChild(make('div', 'source', src));

  var next = make('button', 'next-btn', S.finalQueue.length ? 'Next Contestant' : 'Final Score');
  next.type = 'button';
  next.addEventListener('click', function () { askFinalNext(); });
  verdict.appendChild(next);
}

function finishMatch() {
  var ranked = S.players.slice().sort(function (a, b) { return b.score - a.score; });
  var top = ranked[0];
  var tie = ranked.length > 1 && ranked[1].score === top.score;

  el('results-title').textContent = tie ? 'A Tie' : (top.name + ' Wins');
  var host = el('results-list');
  host.innerHTML = '';
  ranked.forEach(function (p, i) {
    var row = make('div', 'result-row');
    row.style.setProperty('--pc', p.color);
    if (p.score < 0) row.classList.add('neg');
    if (i === 0 && !tie) row.classList.add('is-winner', 'shine', 'is-on');
    row.appendChild(make('span', 'rank', String(i + 1)));
    row.appendChild(make('span', 'rname', p.name));
    row.appendChild(make('span', 'rscore', fmt(p.score)));
    host.appendChild(row);
  });

  stopClueClock();
  stopBoardClock();
  Sound.music(null);
  Sound.sfx('winner');
  show('results');
}

// ── Match control ──────────────────────────────────────────

function startMatch() {
  S.players = [];
  for (var i = 0; i < S.playerCount; i++) {
    var raw = (S.names[i] || '').trim();
    S.players.push({
      name: raw || ('PLAYER ' + (i + 1)),
      score: 0,
      color: PLAYER_COLORS[i]
    });
  }  if (S.finalTimer) clearInterval(S.finalTimer);
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

    if (ev.key === 'Enter' || ev.key === ' ') {
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
    lobby: '.menu .pill',
    setup: '#player-count button, #sound-toggle button, .menu .pill',
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

    if (S.screen === 'splash') { el('begin').click(); return; }

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
      if ((is[A] && !was[A]) || (is[B] && !was[B]) || (is[START] && !was[START]) || direction(pad)) {
        el('begin').click();
      }
      return;
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
      var name = (ev.gamepad && ev.gamepad.id || 'Controller').split(' (')[0];
      toast('Player ' + Math.max(rank, 1) + ' — ' + name);
    });
    window.addEventListener('gamepaddisconnected', function () {
      toast('Controller disconnected');
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

// ── Boot ───────────────────────────────────────────────────

function boot() {
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
     swallowed by the name guard. */
  Sound.music('menu_theme');
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
