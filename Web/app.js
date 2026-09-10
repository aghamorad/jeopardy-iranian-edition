/* JEOPARDY! — Iranian Edition, web build.
   Zero dependencies, zero build step. Open index.html and it plays. */
(function () {
'use strict';

var CLUES = window.CLUES || [];
var PLAYER_COLORS = ['#1f9d55', '#cf3446', '#f2e9da'];
var SINGLE_VALUES = [200, 400, 600, 800, 1000];
var DOUBLE_VALUES = [400, 800, 1200, 1600, 2000];

// ── Helpers ────────────────────────────────────────────────

function el(id) { return document.getElementById(id); }

function make(tag, className, text) {
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

function fmt(n) {
  var sign = n < 0 ? '−' : '';
  return sign + '$' + Math.abs(n).toLocaleString('en-US');
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
  var pool = {};

  function url(name) { return 'assets/audio/' + name + '.m4a'; }

  function makeEl(name, volume, loop) {
    var a = document.createElement('audio');
    a.src = url(name);
    a.volume = volume;
    a.preload = 'auto';
    a.loop = !!loop;
    return a;
  }

  /* Music is a single slot — switching cues fades the old one out rather
     than stacking loops. */
  function music(name) {
    if (musicName === name) return;
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
    if (play && play.catch) play.catch(function () {});
    var rise = setInterval(function () {
      if (musicEl !== a) { clearInterval(rise); return; }
      a.volume = Math.min(0.34, a.volume + 0.04);
      if (a.volume >= 0.34) clearInterval(rise);
    }, 50);
  }

  function sfx(name, volume) {
    if (!enabled || !name) return;
    var node = pool[name];
    if (!node) { node = makeEl(name, 1, false); pool[name] = node; }
    var a = node.cloneNode(true);
    a.volume = volume == null ? 0.7 : volume;
    a.play().catch(function () {});
  }

  function setEnabled(on) {
    enabled = on;
    if (!on) {
      if (musicEl) { musicEl.pause(); musicEl = null; }
      musicName = null;
    }
  }

  return { music: music, sfx: sfx, setEnabled: setEnabled, isEnabled: function () { return enabled; } };
})();

// ── State ──────────────────────────────────────────────────

var S = {
  screen: 'lobby',
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
  armTimer: null,
  armed: false,
  cursor: { col: 0, row: 0 },
  menuIndex: 0,
  finalQueue: [],
  finalAnswers: []
};

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

  el('sound-toggle').addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-sound]');
    if (!btn) return;
    var on = btn.dataset.sound === 'on';
    Sound.setEnabled(on);
    Array.prototype.forEach.call(el('sound-toggle').children, function (b) {
      b.classList.toggle('is-on', b === btn);
      b.setAttribute('aria-checked', b === btn ? 'true' : 'false');
    });
    if (on) { Sound.music('menu_theme'); Sound.sfx('select'); }
  });

  el('start-game').addEventListener('click', startMatch);
  el('play-again').addEventListener('click', function () { show('lobby'); Sound.music('menu_theme'); });
}

// ── Board construction ─────────────────────────────────────

function buildBoard(round) {
  var pool = CLUES.filter(function (c) { return c.round === round; });
  var values = round === 'single' ? SINGLE_VALUES : DOUBLE_VALUES;
  var byCat = groupBy(pool, function (c) { return c.category; });

  var available = Object.keys(byCat).filter(function (name) {
    return !S.usedCategories[name] && values.every(function (v) {
      return byCat[name].some(function (c) { return c.value === v; });
    });
  });

  var chosen = shuffle(available).slice(0, 6);
  chosen.forEach(function (name) { S.usedCategories[name] = true; });

  var columns = chosen.map(function (name) {
    var cells = values.map(function (v) {
      var candidates = byCat[name].filter(function (c) { return c.value === v; });
      var clue = shufflingOptions(pick(candidates));
      return { clue: clue, value: v, solved: false };
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
  var labels = { single: 'Round One', double: 'Double Jeopardy' };
  ['single', 'double'].forEach(function (r) {
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
    host.appendChild(head);
  });

  for (var row = 0; row < 5; row++) {
    for (var col = 0; col < S.board.length; col++) {
      host.appendChild(tile(col, row));
    }
  }
  renderPodiums();
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

  S.clue = cell.clue;
  S.clueCtx = { col: col, row: row };
  S.lockedOut = [];
  S.buzzed = null;
  S.holder = null;
  S.armed = false;

  if (cell.dailyDouble) {
    Sound.sfx('wager');
    var who = S.players.length ? Math.floor(Math.random() * S.players.length) : 0;
    S.mode = 'dd';
    S.holder = who;
    askWager({
      title: 'Daily Double',
      category: cell.clue.category,
      subtitle: S.players[who].name + ' has the floor. Name your wager.',
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

function startClue(withBuzzers) {
  if (S.armTimer) clearTimeout(S.armTimer);
  S.phase = 'reading';
  S.armed = false;
  S.buzzed = null;
  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = fmt(S.clue.value);
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
    Sound.music(null);
    Sound.sfx('armed');
    renderClueActions();
    renderPodiums();
    return;
  }

  Sound.music('thinking_loop');
  S.armTimer = setTimeout(function () {
    S.armed = true;
    Sound.sfx('armed', 0.55);
    renderClueActions();
  }, 450);
}

function renderClueActions() {
  var host = el('clue-actions');
  host.innerHTML = '';

  if (S.phase === 'reading') {
    var row = make('div', 'buzz-row');
    S.players.forEach(function (p, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'buzz-btn';
      b.style.setProperty('--pc', p.color);
      b.disabled = !S.armed || S.lockedOut.indexOf(i) !== -1;
      b.appendChild(make('span', null, 'Buzz · ' + p.name));
      b.appendChild(make('small', null, String(i + 1)));
      b.addEventListener('click', function () { buzz(i); });
      row.appendChild(b);
    });
    host.appendChild(row);

    var hint = make('p', 'hint', S.lockedOut.length
      ? 'Locked out — someone else can still take it.'
      : (S.armed ? 'Buzzers are live.' : 'Get ready…'));
    host.appendChild(hint);
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
}

function buzz(playerIndex) {
  if (S.mode !== 'board') return;
  if (S.phase !== 'reading' || !S.armed) return;
  if (S.lockedOut.indexOf(playerIndex) !== -1) return;

  Sound.sfx('buzz');
  Sound.music(null);
  S.buzzed = playerIndex;
  S.phase = 'answering';
  renderClueActions();
  renderPodiums();
}

function answer(optionIndex) {
  if (S.mode === 'final') return;
  if (S.phase !== 'answering' || S.buzzed == null) return;
  Sound.music(null);
  var clue = S.clue;
  var isCorrect = optionIndex === clue.correct;
  var player = S.players[S.buzzed];
  var delta = isCorrect ? clue.value : -clue.value;
  player.score += delta;

  var buttons = el('clue-actions').querySelectorAll('.option');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].disabled = true;
    if (i === optionIndex) buttons[i].classList.add('shine', 'is-on');
    if (i === clue.correct) buttons[i].classList.add('is-right');
    else if (i === optionIndex) buttons[i].classList.add('is-wrong');
    else buttons[i].classList.add('is-dim');
  }

  Sound.sfx(isCorrect ? 'correct' : 'incorrect');
  renderPodiums();

  if (!isCorrect) {
    S.lockedOut.push(S.buzzed);
    var remaining = S.players.filter(function (_, i) {
      return S.lockedOut.indexOf(i) === -1;
    });
    if (remaining.length > 0) {
      showVerdict('wrong', clue, player, optionIndex, true);
      return;
    }
  }
  resolve(isCorrect, clue, player, optionIndex);
}

function resolve(isCorrect, clue, player, optionIndex) {
  S.phase = 'resolved';
  if (optionIndex == null) optionIndex = clue.correct;
  showVerdict(isCorrect ? 'right' : 'wrong', clue, player, optionIndex, false);
}

function showVerdict(kind, clue, player, optionIndex, canRetry) {
  var host = el('clue-verdict');
  host.hidden = false;
  host.innerHTML = '';
  host.className = 'verdict ' + (kind === 'right' ? 'right' : 'wrong');

  var head;
  if (kind === 'right') head = 'Correct — ' + player.name + ' ' + fmt(clue.value);
  else if (canRetry) head = 'Incorrect — ' + player.name + ' is locked out';
  else if (S.buzzed == null) head = 'Nobody buzzed';
  else head = 'Incorrect — ' + player.name + ' ' + fmt(-clue.value);
  host.appendChild(make('div', 'head', head));

  var line = kind === 'right' ? clue.correctLine : clue.wrongLine;
  if (line) host.appendChild(make('p', 'host-line', '“' + line + '”'));

  var ans = make('p', 'answer');
  ans.appendChild(document.createTextNode('Answer: '));
  ans.appendChild(make('b', null, clue.answer));
  host.appendChild(ans);

  if (clue.explanation) host.appendChild(make('p', 'explain', clue.explanation));

  var src = [clue.book, clue.author, clue.page ? 'p. ' + clue.page : null]
    .filter(Boolean).join(' · ');
  if (src) host.appendChild(make('div', 'source', src));

  var next = make('button', 'next-btn', canRetry ? 'Second Chance' : 'Continue');
  next.type = 'button';
  next.addEventListener('click', function () {
    if (canRetry) {
      S.buzzed = null;
      S.phase = 'reading';
      S.armed = true;
      host.hidden = true;
      host.innerHTML = '';
      Sound.music('thinking_loop');
      renderClueActions();
      renderPodiums();
      return;
    }
    closeClue();
  });
  host.appendChild(next);

  if (kind === 'right') Sound.sfx('correct', 0.5);
  host.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function closeClue() {
  if (S.clueCtx) S.board[S.clueCtx.col].cells[S.clueCtx.row].solved = true;
  S.clue = null;
  S.clueCtx = null;
  S.buzzed = null;
  S.lockedOut = [];
  S.phase = 'idle';
  Sound.music(null);

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

function maxWager(player, round) {
  var top = round === 'double' ? 2000 : 1000;
  return Math.max(player.score > 0 ? player.score : 0, top);
}

function askWager(opts) {
  el('wager-category').textContent = opts.category;
  el('wager-value').textContent = opts.title;
  el('wager-prompt').textContent = opts.subtitle;
  el('wager-control').innerHTML = '';
  el('wager-actions').innerHTML = '';

  var player = S.players[opts.playerIndex] || S.players[0];
  var max = maxWager(player, S.round === 'double' ? 'double' : 'single');
  var amount = Math.min(Math.max(player.score, 0) || Math.round(max / 2), max);

  var display = make('div', 'wager-amount', fmt(amount));
  var range = document.createElement('input');
  range.type = 'range';
  range.className = 'wager-range';
  range.min = '0';
  range.max = String(max);
  range.step = '100';
  range.value = String(amount);
  range.setAttribute('aria-label', 'Wager amount');

  var quick = make('div', 'wager-buttons');
  [[0.25, 'Quarter'], [0.5, 'Half'], [0.75, 'Three Quarters'], [1, 'All In']].forEach(function (pair) {
    var b = make('button', null, pair[1]);
    b.type = 'button';
    b.addEventListener('click', function () {
      amount = Math.round(max * pair[0] / 100) * 100;
      range.value = String(amount);
      display.textContent = fmt(amount);
      Sound.sfx('select', 0.4);
    });
    quick.appendChild(b);
  });

  range.addEventListener('input', function () {
    amount = parseInt(range.value, 10);
    display.textContent = fmt(amount);
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
  Sound.sfx('host_final', 0.6);

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
    subtitle: player.name + ', place your wager.',
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
  el('clue-value').textContent = 'Final · ' + fmt(S.clue.value);
  el('clue-text').textContent = S.clue.clue;
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  show('clue');
  renderPodiums();
  renderClueActions();

  var banner = make('p', 'hint', S.players[idx].name + ' answers · wager ' + fmt(S.clue.value));
  el('clue-actions').insertBefore(banner, el('clue-actions').firstChild);
  fitClueText();
}

function submitFinalAnswer(optionIndex) {
  if (S.mode !== 'final' || S.phase !== 'answering') return;
  S.phase = 'resolved';
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
    (isCorrect ? 'Correct — ' : 'Incorrect — ') + player.name + ' ' +
    fmt(isCorrect ? S.clue.value : -S.clue.value)));
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
  }
  if (S.armTimer) clearTimeout(S.armTimer);
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
  Sound.music(null);
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
    if (action === 'lobby') { show('lobby'); Sound.music('menu_theme'); }
  });
}

function openMenu() {
  S.menuIndex = 0;
  el('match-menu').hidden = false;
  paintMenu();
  Sound.sfx('select', 0.4);
}

function closeMenu() { el('match-menu').hidden = true; }

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

// ── Boot ───────────────────────────────────────────────────

function boot() {
  initLobby();
  initBoardChrome();
  initKeyboard();
  renderPodiums();

  // The clue body grows and shrinks as the verdict panel and answer buttons
  // come and go, so re-fit the clue text whenever its box changes.
  var body = document.querySelector('#screen-clue .clue-body');
  if (body && window.ResizeObserver) new ResizeObserver(fitClueText).observe(body);

  // The show opens on the lobby, but browsers won't start audio until the
  // first gesture — so the theme kicks in the moment the user touches anything.
  var once = function () {
    document.removeEventListener('pointerdown', once);
    if (Sound.isEnabled() && S.screen === 'lobby') Sound.music('menu_theme');
  };
  document.addEventListener('pointerdown', once);
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();

})();
