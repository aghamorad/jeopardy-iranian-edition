/* JEOPARDY! — Iranian Edition, web build.
   Zero dependencies, zero build step. Open index.html and it plays. */
(function () {
'use strict';

/* The bank is picked by two gates — the language and the edition — and both are
   resolved by lookup at the moment of use rather than captured here, because
   both are chosen on the splash, after this line has run. Two banks ship in the
   box (the English original and the Persian edition) and a registered edition
   brings its own pair; all four are the same shape, so a match is built from
   whichever pair is live and nothing downstream has to know which it is. */
function editionBanks() {
  var id = window.getEdition();
  var all = window.getEditions();
  for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i].banks;
  return { en: window.CLUES, fa: window.CLUES_FA };
}
function rebindBanks(lang) {
  var banks = editionBanks();
  /* A locked course declares no bank at all, and this runs at boot and on every
     edition change, so throwing here would take the whole IIFE down and leave a
     student whose saved edition is the preview with no chooser to escape
     through. `CLUES` is emptied rather than left standing: leaving the last
     edition's array bound would deal MAIN's clues under a course's name, which
     is the one thing the registry exists to prevent. Nothing reaches a board
     from here anyway — `startMatch` refuses for a locked edition — so an empty
     array costs nothing and is the safe thing to hold. */
  if (!banks) { CLUES = []; return; }
  if (!Array.isArray(banks[lang]) || !banks[lang].length) {
    throw new Error('Jeopardy: missing ' + lang + ' bank for ' + window.getEdition());
  }
  CLUES = banks[lang];
}

/* Resolved before anything can listen for it: `getEdition` reads `?ed=` and
   localStorage and may dispatch `editionchange`, and this early in the file the
   listeners below do not exist and `S` is still hoisted-undefined. */
window.getEdition();
var CLUES = [];
rebindBanks(savedLang());

/* The screens that can be looking at a dealt board, and therefore the only ones where
   the bank must not move under the clue on screen. */
var DEALT_SCREENS = ['board', 'clue', 'wager', 'results'];

/* A match already dealt out of one bank cannot be rebuilt out of the other, so the
   swap is refused while a board is dealt.

   This used to test `S.players.length`, which is not the same question: quitting a
   match to the splash leaves the roster standing, so the guard silently refused a
   swap and the Persian lobby dealt English clues under Persian chrome. `startMatch`
   now re-reads the bank from the live language anyway, so this listener only keeps
   the screens before a match honest — but it must not lie about which those are. */
document.addEventListener('langchange', function (ev) {
  if (DEALT_SCREENS.indexOf(S.screen) !== -1) return;
  rebindBanks(ev.detail.lang);
});

/* An edition swap is refused mid-match for exactly the same reason: the board on
   screen was dealt out of one bank and cannot be rebuilt out of the other. */
document.addEventListener('editionchange', function () {
  if (DEALT_SCREENS.indexOf(S.screen) !== -1) return;
  rebindBanks(window.getLang());
});
/* Refuse the change before either the chrome or the bank can move. */
['beforelangchange', 'beforeeditionchange'].forEach(function (name) {
  document.addEventListener(name, function (ev) {
    if (S && DEALT_SCREENS.indexOf(S.screen) !== -1) ev.preventDefault();
  });
});
var PLAYER_COLORS = ['#17b25a', '#e02020', '#f2efe9', '#0e8a45', '#a81616', '#c9c5bd'];
/* The table is three, and the palette is longer than the table on purpose — the
   extra colours are there so a future mode can widen without touching the array.
   Anything that means "how many seats are there" has to say PLAYER_SEATS: the
   array's length is a fact about the palette, and reading it as capacity would
   seat a fourth contestant the green room cannot describe. */
var PLAYER_SEATS = 3;
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
/* The buzz window is the round's, not the show's. The first board leaves a room
   twenty seconds to find the thumb; the second tightens it to twelve, because by
   then everybody has settled in and the race should bite. Final Jeopardy is not
   a race at all — it is a wager and a written answer on FINAL_SECONDS — so it
   has no entry here and no buzzer to open. */
var BUZZ_SECONDS = { single: 20, double: 12 };
var BOARD_SECONDS = 20;

/* A round that has not said otherwise gets the second board's window: by the
   time anything is ambiguous, the show has already tightened up. */
function buzzSeconds() { return (S && BUZZ_SECONDS[S.round]) || BUZZ_SECONDS.double; }

/* The race is one window per clue, not one per contestant. A thumb going down
   ends the race where it stands, so what the next contestant inherits is the
   seconds the last one left — `S.buzzLeft`, snapshotted in `buzz`. Each clue
   opens a fresh one in `openBuzzers`, which is the only reset it gets. */
function buzzWindowSeconds() {
  return (S && S.buzzLeft != null) ? S.buzzLeft : buzzSeconds();
}

/* The clue goes up with the buzzers shut and a countdown of its own, because a
   shared screen needs the room to actually read the thing before anybody's thumb
   moves. Six seconds was a glance, not a read — a two-line clue in English or
   Persian takes a real pass, and the same window has to serve both scripts. The
   buzz window opens after that, on a clock of its own. */
var READ_SECONDS = 15;
/* The penalty for jumping the gun is this long and it starts when the thumb
   lands, not when the lamp opens. That is the difference between a mistake and a
   sentence: measured from the lamp, a press ten seconds early left the button
   dead for eleven and a half, so a one-second error and a ten-second one cost
   the same and neither had anything to do with the race. Anchored to the press,
   the penalty is a second and a half whenever it is paid, and what it buys is
   exactly the thing the buzzer is testing — press a second early and the last
   half-second of the lockout falls on the far side of the lamp, so you are not
   fast enough. Press ten seconds early and you are live again well before the
   race, having lost nothing but the time you were not competing for. */
var EARLY_LOCKOUT_MS = 1500;

/* How long a miss that the room can still steal stays on screen before the
   buzzers come back on their own. That panel announces a lockout and holds the
   answer back, so there is nothing on it to read and nothing on it to decide —
   a click there is not a choice, it is a chore, and the room ends up watching a
   button instead of thinking about the clue. Long enough to register who is
   out, short enough that the steal still feels like a steal. */
var STEAL_BEAT_MS = 2000;

/* How long a robot holds the board before it opens a tile. A beat, so the room
   sees a contestant choosing rather than the clock choosing for them. */
var BOT_PICK_MS = 1400;

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
    'tannaz_right_01_well_look_at_you',
    'tannaz_right_02_try_not_to_become_unbearable',
    'tannaz_right_03_mashallah_an_actual_fact',
    'tannaz_right_04_confidence_matched_the_answer',
    'tannaz_right_05_please_remain_humble',
    'tannaz_right_06_actual_knowledge_how_refreshing',
    'tannaz_right_07_tell_your_uncle',
    'tannaz_right_08_tehran_survives_another_round',
    'tannaz_right_09_annoyingly_good',
    'tannaz_right_10_i_hate_how_pleased_you_look',
    'tannaz_right_11_not_just_opinions_after_all',
    'tannaz_right_12_unfortunately_youre_right',
    'tannaz_right_13_dont_get_used_to_this_feeling',
    'tannaz_right_14_four_thousand_years_finally_correct',
    'tannaz_right_15_try_not_to_explain_it_to_everyone',
    'tannaz_right_16_you_may_be_smug_for_five_seconds'
  ],
  wrong: [
    'tannaz_wrong_01_mashallah_the_confidence',
    'tannaz_wrong_02_very_iranian_of_you',
    'tannaz_wrong_03_no_facts_full_confidence',
    'tannaz_wrong_04_dinner_party',
    'tannaz_wrong_05_family_whatsapp',
    'tannaz_wrong_06_source_your_uncle',
    'tannaz_wrong_07_iranian_method',
    'tannaz_wrong_08_mashallah_you_have_opinions',
    'tannaz_wrong_09_tehran_taxi_driver',
    'tannaz_wrong_10_iranian_uncle_nodding',
    'tannaz_wrong_11_national_tradition',
    'tannaz_wrong_12_world_class_confidence',
    'tannaz_wrong_13_four_thousand_years',
    'tannaz_wrong_14_cyrus_the_great',
    'tannaz_wrong_15_dinner_fact',
    'tannaz_wrong_16_explain_it_loudly'
  ]
};

/* A kind with no pool of its own falls through to one of the two the engine
   always has, so a verdict the host has nothing recorded for still gets a
   reaction rather than silence. `timeout` reads as a plain wrong answer; a
   lockout is a stealable miss, which is the same beat. In the public build both
   entries are the path the request already took. */
var HOST_FALLBACK = { timeout: 'wrong', lockout: 'wrong' };
var HOST_LINE_DELAY_MS = 650;

/* How long the floor stays hers when there is no clip to measure. A muted cue
   still puts her on her feet — see `voice` — and a figure that appeared and
   vanished inside a frame would read as a glitch rather than as a host. Sized
   to the beat a verdict lands on, not to any of the clips. */
var HOST_SILENT_MS = 2000;

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

/* Parentheses used to leak the answer. The archive quite reasonably writes a
   canonical name as "National Iranian Oil Company (NIOC)", but distractors
   usually have no gloss. Shuffling the four positions did nothing to hide that
   editorial fingerprint: the one option with parentheses was still the answer.

   The first disguise was worse than the leak. Flattening the gloss to a dash
   and then coin-flipping parentheses onto all four options moved the tell
   instead of hiding it: the em-dash landed only on the option that had carried
   the gloss, so "tap the button with a dash" won 196 times out of 210, and
   every distractor in those clues wore parentheses it had no reason to wear.

   Presentation is dealt separately from meaning, and the gloss therefore comes
   off: the buttons show the name, the archive keeps the gloss, and the host's
   line names it in full at the reveal. `options` stays untouched for judging,
   robots and the archive invariant; only `displayOptions` reaches the buttons. */
function presentingOption(text) {
  return String(text).replace(/\s*[\(（][^\(\)（）]*[\)）]/g, '')
    .replace(/\s+/g, ' ').replace(/^\s+|\s+$/g, '');
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
  /* Clues without authored parentheses come back from the strip unchanged and
     keep their ordinary typography. Two buttons can only merge into the same
     text if one option carried a gloss and another was that name alone, which
     is an authoring mistake — but a board showing the same text in two squares
     is the worse failure, so the gloss survives when dropping it would merge. */
  var shown = opts.map(presentingOption);
  var merged = shown.some(function (text, i) { return shown.indexOf(text) !== i; });
  copy.displayOptions = merged ? opts.slice() : shown;
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

  /* The page is out of sight — a phone minimized, a shell's window covered —
     and the show is held rather than ended. Separate from `enabled`, which is
     the player's own switch and has a button drawn from it: the room is not
     told the show was muted, because it was not. */
  var away = false;

  /* The one voice on the floor. Only one line is ever worth hearing, so a new
     cue cuts the old one off through its own `finish` — that restores the music
     the old line had ducked before the new one reads the slot, which is what
     keeps the betting house from going quiet after a fast pair of verdicts. */
  var voiceEl = null;

  /* Her clips are a switch of their own, separate from the show's sound: a
     room that wants the stings and the theme and not a woman swearing at it.
     Muted, a cue costs no clip, no duck and no floor — but it is still
     announced, because the figure on the stage is drawn from the cue and a
     silent host is still a host. */
  var voiceEnabled = true;

  /* Bumped by every cue, so the exit timer a muted cue leaves behind can tell
     whether something newer has taken the floor in the meantime. */
  var voiceGen = 0;

  /* Her reaction is scheduled rather than fired, so that the sting underneath
     gets a beat to itself. One timer for the whole show — a verdict that
     arrives while the last one is still waiting is the same timer, retimed. */
  var hostTimer = null;

  /* An edition may ship its own soundtrack for a slot the engine knows by name.
     The substitution is made here, where the file is chosen, and not at the call
     sites: every caller above goes on asking for the slot it always asked for,
     so the name guard in `music`, the duck-and-restore under a voice, and the
     sfx path all keep comparing slots and never files.

     The front door and the boot screen before it are the two that belong to no
     show — the door is the screen that picks one, and boot runs before the door is
     even open — so nothing heard on either may be re-voiced by the edition that
     happens to be current. That matters because a course remembers itself: a
     student who last played the course boots on the door with the course in
     `localStorage` and the course's own `course.js` already publishing its
     mapping, and the door would open on the course's theme. It plays MAIN's,
     which is the theme of the show it is about to walk into. */
  function fileFor(name) {
    if (S.screen === 'front' || S.screen === 'boot') return name;
    return (window.EDITION_SOUND || {})[name] || name;
  }

  /* A substitution may carry a path: a course keeps its pack with the course, in
     `courses/<id>/assets/audio/`, rather than in the engine's own audio dir. A
     bare name still resolves there, so MAIN's cues are untouched. */
  var CACHE_V = '20260915-globe-22';

  /* One cue can be re-cut without re-cutting the rest. `CACHE_V` is shared by
     every URL built below, so moving it to publish a single replaced file would
     re-fetch the entire soundtrack for everyone who has already played — six
     megabytes of host lines that did not change — and over the connection this
     show is mostly played on, that is not free. A cue named here carries a tag
     of its own; everything else follows the shared one. The buzz is the first:
     it was replaced on 2026-09-16 and the old one is gone, so anyone who has
     already heard it must not be answered from the cache. The tag moved again
     the same day when the cut came down 8 dB: the first replacement was the
     right file at the wrong level, and a tag that never moves would leave that
     level in every browser that had already fetched it. It moved once more on
     2026-09-18, when the cue itself was replaced by a shorter one. */
  var CUE_V = {
    buzz: '20260918-buzz-3',
    /* The professor's welcome was re-timed from 1.0x to 0.9x — 15.3s to 17.0s —
       because the clone read the line at about 145 words a minute and it landed
       as hurried. Keyed by the clip's own name rather than the cue, because
       `voice` applies `HOST_CUE_MAP` before this is read: the course's
       substitution is what arrives here, so only the course's file is refetched
       and the main edition's welcome keeps the shared tag. */
    eskandar_01_professor_welcome: '20260916-welcome-0-9x',
    /* The Qajar welcome was re-cut on 2026-09-18: the caption dropped its
       opening "Eight weeks," in the Qajar copy pass, so the clip was re-recorded
       to match rather than the caption reverted. Same filename, new audio — any
       browser that has already played the course holds the old reading. */
    stephanie_qajars_welcome: '20260918-qajar-welcome'
  };

  /* The version is not decoration and it is not only for scripts. Audio is cached
     by URL like everything else, and the WebView shells hold that cache across
     launches — so a cue that is re-recorded or re-timed reaches nobody who has
     already heard the old one, which is exactly what happened to a set of host
     lines that were re-timed after the first people had played. Every other asset
     on the front door carries a `?v=`, and the only reason audio did not was that
     nothing had changed yet. It has now.
     The value has to move with the tag in `index.html`; there is no build step
     that could keep the two in step for us. */
  function url(name, ext) {
    var f = fileFor(name);
    var p = f.indexOf('/') >= 0 ? f + ext : 'assets/audio/' + f + ext;
    return p + '?v=' + (CUE_V[name] || CACHE_V);
  }

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
    /* The cue's own level, kept beside the level that actually goes to the
       element: `setVolume` walks the live floor and needs to know what each
       element was asking for before the master is applied to it. */
    a._base = volume;
    a.volume = volume * master;
    /* Which file this element was cut for, remembered so `refresh` can tell a
       mapping that moved from one that did not. */
    a._file = fileFor(name);
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

  /* The player's level for the whole show, and the one number every cue passes
     through on its way to an element. Remembered across launches, which nothing
     else about sound in this file is: a mute you have to re-make is a switch,
     but a volume you have to re-set every time you open the show is a chore.
     Clamped on the way in — the value is read back from storage, and storage is
     a file a stale build or a curious player can edit. */
  var master = (function () {
    var stored;
    try { stored = parseFloat(localStorage.getItem('jpd-volume')); } catch (e) { stored = NaN; }
    return isFinite(stored) ? Math.max(0, Math.min(1, stored)) : 1;
  })();

  /* Set the show's level. The elements on the floor are moved with it — the
     bed and her line are the two that are still sounding when a hand is on the
     slider; a sting is a fraction of a second and will be over before anyone
     has let go — and everything cued afterwards reads the new master in
     `makeEl`. On a platform that ignores the volume property this is a no-op
     twice over: the assignments do nothing, and the slider that calls it is
     never drawn. */
  function setVolume(level) {
    master = Math.max(0, Math.min(1, level));
    try { localStorage.setItem('jpd-volume', String(master)); } catch (e) { /* no storage */ }
    if (voiceEl) voiceEl.volume = (voiceEl._base == null ? 1 : voiceEl._base) * master;
    if (musicEl && !musicEl.paused) musicEl.volume = MUSIC_LEVEL * master;
  }

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
    /* The slot is named either way. A page that is away takes the name and
       starts nothing, which is what `resume` needs to find. */
    if (!enabled || away || !name) return false;
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
        /* Read per tick rather than captured: a hand on the volume slider while
           a bed is coming up moves the target under the fade, and the fade
           follows it instead of climbing past it. */
        var target = MUSIC_LEVEL * master;
        a.volume = Math.min(target, a.volume + 0.04);
        if (a.volume >= target) clearInterval(rise);
      }, 50);
    }
    return play;
  }

  /* Re-issues the bed that is on the air. A cue's file is only read when the cue
     is asked for, so a bed already playing belongs to the soundtrack that was
     current when it started — an edition that changes its own mapping has to
     say so, or the show it just left keeps playing under the new one. Nothing
     happens when the floor is empty or a voice holds it: a ducked bed is put
     back by the voice's own `finish`, which reads the mapping fresh. */
  function refresh() {
    if (!musicName) return;
    /* Nothing to do when the slot still resolves to the file that is already
       playing. Nothing has moved — `music`'s name guard compares slots, and a bed
       is not re-cut for a slot that answers with the same file; a track that is
       already correct must not be heard restarting from the top. */
    if (musicEl && !musicEl.paused && musicEl._file === fileFor(musicName)) return;
    var name = musicName;
    musicName = null;
    music(name);
  }

  /* A show that has been put away comes back with its audio still down. iOS
     suspends every media element when the WebView loses the foreground, and
     nothing in this file ever asks for one again — the slot is still named, so
     re-issuing it is the whole repair, and a return that lands on a screen whose
     bed happens to be re-cued anyway is the only reason the theme was ever heard
     again at all. That is the "sometimes gone, sometimes there": it came back
     when some screen change asked for a bed and the name guard let a paused
     element through, and stayed silent when none did.

     Only a bed that is actually down is re-issued. Coming back to a page that
     never stopped must not restart the track from the top, and a floor held by a
     voice is left alone: `musicName` is null while she talks, and her own guard
     timer restores the bed she ducked when it expires. */
  function resume() {
    var held = away;
    away = false;
    if (!enabled || !musicName) return;
    /* A bed that was only set down — paused by `suspend`, on a page that went
       out of sight — carries on from where it stopped. Making it again, which
       is what the rest of this function does, would start a theme the player
       has already heard the top of. This is the one case the page itself
       created; the ones below belong to the platform. */
    if (held && musicEl && musicEl._away) {
      musicEl._away = false;
      if (musicEl.paused) musicEl.play().catch(function () {});
      return;
    }
    if (musicEl && !musicEl.paused) return;
    var name = musicName;
    musicName = null;
    music(name);
  }

  /* Put the show down. The page going out of sight is the one transition no
     screen change announces, and every shell and browser has a way of handing
     it to us; behind a covered window a WebView goes on running the engine,
     and Android goes on playing a media element there, so nothing else is
     going to stop this one. Without it a phone in a pocket plays the theme to
     a room that has left. `resume` above is the other half.

     What is set down is not the same as what is thrown away. The bed is paused
     and its slot kept, so the way back can start it again. Her line is ended
     rather than paused: `finish` is the only door that puts back the bed it
     ducked, and a line heard in a pocket is worth nothing on the way back.
     The verdict waiting on its beat goes with them — that is a timer, and it
     would otherwise fire behind a covered window and start a line nobody is
     there to hear.

     Nothing new is started while `away` holds. A screen the game reached under
     its own steam still names its bed, and a voice cue still announces itself
     and still runs its `then`, but neither reaches the air; the name is what
     `resume` plays, so the show comes back to whatever it had arrived at. */
  function suspend() {
    if (away) return;
    away = true;
    clearTimeout(hostTimer);
    hostTimer = null;
    if (voiceEl && voiceEl._finish) voiceEl._finish();
    if (musicEl && !musicEl.paused) {
      musicEl._away = true;
      musicEl.pause();
    }
  }

  function sfx(name, volume) {
    /* A sting fired by a timer behind a covered window is a shot into an empty
       room, and there is nothing on the way back that could pick it up. */
    if (!enabled || away || !name) return;
    var a = makeEl(name, volume == null ? 0.7 : volume, false);
    release(a);
    a.play().catch(function () {});
  }

  /* Tells anyone listening which cue holds the floor, and `null` when the floor
     goes empty. An edition draws the speaker and their words from this; the
     engine itself has no listener and the dispatch costs nothing. */
  function tellCue(name) {
    document.dispatchEvent(new CustomEvent('hostcue', { detail: { name: name } }));
  }

  /* A one-shot cue that takes the floor: the music drops out while it plays
     and comes back when it is done. Used for the host's lines and for the
     opening challenge, which run anywhere from three seconds to fifteen.
     `opts.over` keeps the bed running underneath instead — the splash
     underscore is written to sit under her line, so it must not be the thing
     that gets ducked out of the way. */
  function voice(name, volume, then, opts) {
    if (!enabled || !name) return;
    /* An edition may have recorded its own voice for a cue the engine calls by
       name. The map is a straight substitution and is applied before anything
       below reads `name`, so the announcement carries the file that actually
       plays rather than the one that was asked for. */
    name = (window.HOST_CUE_MAP || {})[name] || name;

    var gen = ++voiceGen;
    /* A host the player has silenced and a host nobody is there to hear say the
       same thing, so a page that is away takes this door too. */
    if (!voiceEnabled || away) {
      /* Muted. The cue is announced anyway, for the same reason it is announced
         on the way to a clip: the figure on the floor is drawn from it. What is
         skipped is the audio, and with it the duck — there is no line to make
         room for. The floor is then given a fixed beat rather than a duration,
         since there is no clip length to read, and `then` runs at once: a
         caller waiting on a line that will never play must not be left waiting
         (the course advances its scene on that callback). The generation guard
         keeps this exit from clearing a cue that has since taken over. */
      tellCue(name);
      setTimeout(function () { if (voiceGen === gen) tellCue(null); }, HOST_SILENT_MS);
      if (then) then();
      return;
    }

    /* Whoever is talking gives up the floor first. `finish` puts back the music
       it ducked, so doing this before reading `musicName` below means the new
       line ducks the right bed instead of inheriting a hole. */
    if (voiceEl && voiceEl._finish) voiceEl._finish();
    /* Announced after the preempt and before the new clip claims the slot, so a
       listener clears the old line and sets the new one in that order rather
       than being told to clear something that is already gone. */
    tellCue(name);
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
      /* The slot is empty again, so whoever is drawing the line goes away with
         it. `done` above already guards this against a double fire. */
      tellCue(null);
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
  /* Which pool each bag was filled from, so a pool that changes under a half-
     emptied bag is noticed rather than finishing out the old one. */
  var hostBagOf = { right: null, wrong: null };

  /* The pool behind a kind. An edition may have recorded its own host and
     publishes whole pools under `HOST_VOICE`, keyed the same way; those win
     outright, because the course edition replaces the show's host with a
     professor and a half-merge would leave the room talking in two voices.

     Read per draw rather than merged once at boot. The same build ships both
     editions, so the answer has to follow whichever one is on screen, and an
     edition picked up or put down mid-session changes it — a boot-time merge
     into `HOST_LINES` would hand the professor the show's room permanently.
     Absent the global this is the engine's own table, which is the whole of
     what the public build sees. */
  function hostPool(kind) {
    var voiced = window.HOST_VOICE;
    if (voiced && voiced[kind] && voiced[kind].length) return voiced[kind];
    return HOST_LINES[kind];
  }

  function drawHostLine(kind) {
    var pool = hostPool(kind);
    if (!pool || !pool.length) return null;
    if (hostBagOf[kind] !== pool) {
      hostBagOf[kind] = pool;
      hostBag[kind] = [];
    }
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
    if (!name && HOST_FALLBACK[kind]) name = drawHostLine(HOST_FALLBACK[kind]);
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

  /* Silences her without touching the rest of the show. Muting mid-sentence
     ends the line through `finish` for the same reason muting the whole show
     does: the clip would otherwise play on unheard and hold the floor, and
     whoever was waiting on it — the cold open, a course scene — would never be
     told it was over. With the audio gone the cue's null takes her off the
     floor too, which is the right shape: a muted host has nothing to caption. */
  function setVoiceEnabled(on) {
    if (voiceEnabled === on) return;
    voiceEnabled = on;
    if (!on) cut();
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
    refresh: refresh, resume: resume, suspend: suspend,
    setEnabled: setEnabled, isEnabled: function () { return enabled; },
    setVoiceEnabled: setVoiceEnabled,
    setVolume: setVolume, volume: function () { return master; },
    canSetVolume: function () { return volumeWorks; }
  };
})();

/* The one handle the engine hands out. An edition needs it to play a line of
   its own — a beat the scoreboard announces rather than a cue the show calls
   for — and `voice` is on the object above. Nothing in this file reads it. */
window.Sound = Sound;

/* Announces a moment the engine knows about but has no line for. The edition
   decides whether anything is said and in whose voice; with no listener this is
   an observed-by-nobody event and the public build is unaffected. */
function beat(name, detail) {
  document.dispatchEvent(new CustomEvent('hostbeat', {
    detail: { name: name, detail: detail || null }
  }));
}

/* Who held what after the last score was written, so a single write can tell a
   comeback from a first lead. Reset with the seats at the top of a match. */
var MATCH_BEATS = { top: null, last: null };

/* Called after every score write, with the seat that moved. Keeps the streak on
   the seat itself rather than in a side table, because the seats are rebuilt at
   the top of every match and the counters should not outlive them. Returns
   nothing; the beats it fires are advisory.

   The three remarks behind it are all addressed to a player — "you're in the
   lead", "a comeback" — so a seat with no human behind it never triggers one.
   The edition could make that call itself, but a bot leading would then queue a
   line that gets thrown away, and this is the side that knows the difference. */
function noteScore(player, isCorrect) {
  if (!player) return;
  player._streak = isCorrect ? (player._streak || 0) + 1 : 0;

  /* Ranked after the write, compared against the seats that held the top and
     the bottom before it. The seats are the same objects throughout a match, so
     `wasLast` is an identity test rather than a score one — by now their scores
     have already moved. */
  var ranked = S.players.slice().sort(function (a, b) { return b.score - a.score; });
  var top = ranked[0];
  var hadTop = MATCH_BEATS.top;
  var wasLast = MATCH_BEATS.last === player;
  var tie = ranked.length > 1 && ranked[1].score === top.score;

  MATCH_BEATS.top = top;
  MATCH_BEATS.last = ranked[ranked.length - 1];

  /* A bot scoring still moves the record of who leads, but never gets a remark:
     the lines are all addressed to the person playing. */
  if (player.bot || player.remote || !isCorrect) return;

  if (player._streak === 3) beat('streak', { seat: player });
  if (tie) return;
  if (wasLast && player === top) { beat('comeback', { seat: player }); return; }
  if (hadTop && hadTop !== player && player === top) beat('lead', { seat: player });
}

/* The one thing a device can say to a thumb that a screen cannot.

   Safari ships no Vibration API at all — not on iOS, not anywhere — so on an iPhone
   the shell in `App/ShowWebView.swift` carries the message instead and answers it
   with the platform's own feedback generator. Everywhere else it is the platform's
   own vibrator. A pattern nobody can play is a no-op, never an error.

   It has a switch of its own, in Settings. It used to ride the sound switch, on the
   reasoning that a player who muted the show had not asked to be tapped on the wrist
   — but muting a show and wanting a tap on the wrist are two different wishes, and
   the player with the sound off is exactly the one who needs the buzz said some other
   way. The pad in a contestant's hand answers to this same switch: it is the same
   promise to the same person, and one setting to look for rather than two. */
var Haptics = (function () {
  var enabled = true;
  /* Deliberately unalike. The one thing a player must never be unsure of at this
     speed is whether the press counted — so an accepted buzz, somebody else's buzz
     and a refusal have to be three different feelings, not one feeling three times. */
  var PATTERNS = {
    take: [26, 46, 26],
    beat: [14],
    foul: [11, 30, 11, 30, 11],
    /* A button, any button: the shortest thing the hardware can say. */
    tap: [7]
  };

  /* This machine's own body: a phone, a trackpad. The other device a word lands
     on is the pad in a player's hand, and `Pads` owns that one — this side only
     has to know which contestant each word is about. */
  function fire(name) {
    var handlers = window.webkit && window.webkit.messageHandlers;
    var native = handlers && handlers.haptics;
    if (native) {
      try { native.postMessage(name); return; } catch (e) { /* fall through */ }
    }

    if (navigator.vibrate) {
      try { navigator.vibrate(PATTERNS[name]); } catch (e) {}
    }
  }

  /* Every word is about somebody, and `who` is that contestant's seat. A word
     with no `who` is about nobody in particular and stays on this device, which
     is what an ordinary button press is. */
  return {
    /* Your own thumb landing on the plate, and the heaviest thing the show says.
       It is also the one word that is news to everybody else: the race just
       stopped for them, so their pads say so too — faintly, because losing is
       not the same event as winning. */
    take: function (who) {
      if (!enabled) return;
      fire('take');
      Pads.feel(who, 'take');
      Pads.feelOthers(who, 'beat');
    },
    /* Somebody else got there first: the room moved and you did not. `except` is
       the seat whose pad has already been told something else — a guest, who felt
       their own thumb land on their own phone. A robot's buzz has no seat to
       except, so every pad in the room takes it. */
    beat: function (except) {
      if (!enabled) return;
      fire('beat');
      Pads.feelOthers(except == null ? -1 : except, 'beat');
    },
    /* Jumped the lamp. A refusal has to be unmistakable from an acceptance. */
    foul: function (who) {
      if (!enabled) return;
      fire('foul');
      Pads.feel(who, 'foul');
    },
    /* An ordinary button, pressed. This one stays on the device: four pads
       ticking every time somebody crosses a menu is noise, not feedback. */
    tap: function () {
      if (!enabled) return;
      fire('tap');
    },
    setEnabled: function (on) { enabled = on; },
    isEnabled: function () { return enabled; }
  };
})();

/* The press, made visible — and made felt, on a device that can feel.

   Delegated off the document rather than bound to each control, because the
   controls are mostly drawn after this line runs: the board tiles, the clue row,
   the green room and the overlays all arrive late, and a listener that has to be
   re-attached to each of them is a listener that will one day be forgotten.

   The plate is excluded from the tap, not from the press: it has its own three
   words to say — took it, lost it, jumped the lamp — and a fourth tick landing a
   few milliseconds early would blur the one distinction a player has to make at
   that speed. */
var Press = (function () {
  var SELECTOR = 'button, .tile, .option, [role="button"], [role="radio"], [data-press]';
  var held = null;

  function hit(node) {
    while (node && node.nodeType === 1) {
      if (node.matches && node.matches(SELECTOR)) return node;
      node = node.parentNode;
    }
    return null;
  }

  function down(ev) {
    var target = hit(ev.target);
    if (!target || target.disabled || target.getAttribute('aria-disabled') === 'true') return;
    if (held && held !== target) held.classList.remove('is-pressed');
    held = target;
    target.classList.add('is-pressed');
    if (!target.classList.contains('buzz-btn')) Haptics.tap();
  }

  function release() {
    if (!held) return;
    held.classList.remove('is-pressed');
    held = null;
  }

  document.addEventListener('pointerdown', down, true);
  document.addEventListener('pointerup', release, true);
  document.addEventListener('pointercancel', release, true);
  /* A pointer that leaves the window mid-press never reports its release, so the
     control would keep the class until the next tap. */
  window.addEventListener('blur', release);
  document.addEventListener('visibilitychange', release);

  return { release: release };
})();

// ── State ──────────────────────────────────────────────────

var S = {
  screen: 'boot',
  /* Where the boot pass hands over, when it is not the front door: a `?ed=`
     link names its own show and goes straight to that title card. Null on every
     other load. */
  bootTarget: null,
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
  /* Seconds left in this clue's buzz window. One per clue, set full when the
     buzzers open and cut down each time a thumb goes down, so a steal resumes
     the window instead of restarting it. */
  buzzLeft: null,
  opening: false,      // she is mid-sentence on the title card
  openingDone: false,  // she has had her say; the title card will not replay it
  openTimer: null,
  prematureUntil: {},  // player index -> the moment they may buzz again after fouling
  lockoutTimer: null,  // re-renders the buzz row when that lockout lifts
  /* The judge asks for a full name on some clues. It is asked once per clue:
     the second attempt passes `noPrompt`, so a player who answers "Qavam" and
     is told to be specific is not asked to be specific forever. */
  writePrompted: false,
  cursor: { col: 0, row: 0 },
  menuIndex: 0,
  /* The host's two switches, and the single copy of them — `applyStage` pushes
     them down to the layer that draws her and the module that plays her, and
     `paintStage` writes them into the settings panel's chips. Session-only,
     like the show's own sound switch beside them on that panel: nothing here is
     a preference the show remembers. */
  sprites: true,
  voice: true,
  finalQueue: [],
  finalAnswers: [],
  finalTimer: null,
  finalRemaining: 0,
  clueTimer: null,
  clueRemaining: 0,
  boardTimer: null,
  boardRemaining: 0,
  /* Whose board it is to open, and who earned it. See `nameChooser`. */
  chooser: null,
  clueWinner: null,
  pickTimer: null,
  roundCardOn: false,  // the scene change is covering the screen
  roundCardTimer: null,
  /* Non-null while this device is sitting at an online table, and null the
     rest of the time. The offline game never asks. */
  online: null
};

/* Seconds a contestant gets to answer the Final clue, per the engine. */
var FINAL_SECONDS = 30;

// ── Screen plumbing ────────────────────────────────────────

function show(id) {
  var screens = document.querySelectorAll('.screen');
  for (var i = 0; i < screens.length; i++) screens[i].classList.remove('is-active');
  var target = el('screen-' + id);
  if (target) target.classList.add('is-active');
  /* Mirrored onto the root so the stage can carry a different backdrop per
     screen. The chooser is a doorway, not the show, and it wants its own art. */
  document.documentElement.setAttribute('data-screen', id);
  S.screen = id;
  /* Opening the green room draws the night's robots. It is here rather than in
     the field-builders because the caption in the lobby and the roster the
     match is built from have to be the same draw, and this is the one place
     both pass through. Stepping out to the lobby and back in is a new draw,
     which is the point of the feature. */
  if (id === 'setup') { Bots.redraw(); renderNames(); }
  window.scrollTo(0, 0);
  onlineSync();
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
      /* The board is only now touchable — the card was covering it until this
         instant. Called once per round, because the card is shown once per
         round; the other two callers of `startBoardClock` are a re-render and a
         pause-menu exit, and neither is the board becoming available. */
      beat('boardIdle', { round: S.round });
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
        wrap.appendChild(make('span', 'bot-name', T(Bots.nameKey(idx))));
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

/* The haptics switch has one home — the settings overlay — so it needs no
   pairing loop of its own. */
function setHapticsSegments(on) {
  var host = el('settings-haptics');
  if (!host) return;
  Array.prototype.forEach.call(host.children, function (b) {
    var isOn = (b.dataset.haptics === 'on') === on;
    b.classList.toggle('is-on', isOn);
    b.setAttribute('aria-checked', isOn ? 'true' : 'false');
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

  /* The host's two switches, in the one home they have. `applyStage` is the door
     they go through rather than a bare `paintStage`: the value has to reach the
     layer that draws her and the module that plays her as well as the chips, and
     painting alone would leave the show obeying the old one. */
  ['sprites', 'voice'].forEach(function (key) {
    var host = el('settings-' + key);
    if (!host) return;
    host.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-' + key + ']');
      if (!btn) return;
      S[key] = btn.getAttribute('data-' + key) === 'on';
      applyStage();
      Sound.sfx('select', 0.4);
    });
  });

  /* The volume, where the platform honours it. The row is taken out of the card
     rather than drawn dead: iOS WebKit ignores the volume property outright, and
     a slider that moves while nothing changes is a lie about the machine. On a
     phone the show runs at the level its cues were mastered to, and the hardware
     buttons are the control — which is the answer the room already knows. */
  var volRow = el('settings-volume-row');
  var vol = el('settings-volume');
  if (volRow && vol && !Sound.canSetVolume()) {
    volRow.hidden = true;
  } else if (vol) {
    vol.value = String(Math.round(Sound.volume() * 100));
    vol.addEventListener('input', function () {
      Sound.setVolume(parseInt(vol.value, 10) / 100);
    });
    /* Heard as well as moved. A sting on release is the level the player has just
       chosen, which is the only read-out a slider has — and at zero it says
       nothing at all, which is the answer they asked for. */
    vol.addEventListener('change', function () { Sound.sfx('select'); });
  }

  /* Nothing confirms a haptics switch except a haptic, so turning it on says the
     shortest word the hardware has. Turning it off says nothing, which is the
     answer the player just asked for. */
  var hapticsHost = el('settings-haptics');
  if (hapticsHost) {
    hapticsHost.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-haptics]');
      if (!btn) return;
      var on = btn.dataset.haptics === 'on';
      Haptics.setEnabled(on);
      setHapticsSegments(on);
      if (on) Haptics.tap();
    });
  }

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
    return S.screen === 'boot' || S.screen === 'front' || S.screen === 'splash' ||
           S.screen === 'lobby' || S.screen === 'setup';
  };

  var runOpening = function () {
    /* The cold open belongs to the title card, not to the front door. Boot no
       longer calls this at all — `enterEdition` does, on the press that picks a
       show — and the gesture listeners below call it too, which is why the guard
       is here rather than at each caller: on the front screen a stray pointerdown
       must not start the show's music under a screen that has not been chosen. */
    if (S.screen !== 'splash') return;
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
      Sound.voice('tannaz_opening_challenge', 0.9, doneOpening, { over: true });
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
    document.body.classList.remove('is-opening');
    if (el('screen-splash')) el('screen-splash').classList.remove('is-opening');
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

  var currentEdition = function () {
    var ed = window.getEdition();
    var all = window.getEditions();
    for (var i = 0; i < all.length; i++) if (all[i].id === ed) return all[i];
    return null;
  };

  /* The one way off the title card, and all it does is move the screen: her cue
     plays over the lobby, because the cold open is a cold open and not a gate. */
  var leaveSplash = function () {
    if (S.screen === 'splash') show('lobby');
    /* While `S.opening` is up the music is hers; doneOpening hands it over. */
    if (!S.opening) Sound.music('menu_theme');
  };

  /* Three steps, and the two directions between them.

     `enterEdition` is the press that picks a show; it re-skins the card, starts
     the cold open, and stops there — the player lands on the title card, not in
     the lobby, so the show still gets to announce itself. It deliberately does
     not touch the language: that is its own choice, made on the front door, and
     `getLang()` already holds it.

     `enterTitle` is today's `begin` under its real name: the press that walks in.

     `backToFront` is the way back out, the one exit that is also an undo — the
     player is leaving the show rather than walking into it. It must not touch
     `S.opening` — quitting the open half-way and returning is not a reason to
     play it again, and `S.openingDone` is what stops it. What it must do is
     `cut`: her cue can still be running when the door comes up, and the host on
     the floor is drawn from the cue that holds it, so one `cut` takes both the
     voice and the figure. Without it the door is announced by the show the
     player just backed out of, still talking, over a screen that belongs to
     neither edition. */
  var enterEdition = function (id) {
    if (S.screen !== 'front') return;
    Sound.sfx('select');
    /* Before the open, not after: `setEdition` fires `editionchange`
       synchronously, so the skin and the course's own audio are in place before
       she says a word. */
    if (window.getEdition() !== id) window.setEdition(id);
    show('splash');
    /* Crossing the door is what moves the mapping — see `fileFor` — and a show
       that is already current fires no `editionchange`, so nothing else would
       re-read it: the door's theme would follow the player in. Only when the cold
       open will not take the floor itself, though; a running open hands the bed
       back through `doneOpening`, which reads the mapping fresh, and re-issuing
       here would only cross-fade two beds into the underscore. */
    if (S.openingDone) {
      Sound.refresh();
      /* The open is spent, so `runOpening` below returns on the flag and nothing
         else on this path cues anybody: the player walks into a show whose stage
         is empty, host and all. Backing out to the door and walking in again is
         not a first visit, but it is still an arrival, and the host is the
         floor's answer to one — so he says hello again. The line alone, without
         the underscore and the darkening the open brings with it: those are the
         theatre of a first entry and they have already been spent.

         It has to be a cue and not a bare sprite, because the bubble is a
         transcript of audio and a host who is to be seen talking must first be
         heard. `over` keeps the bed `refresh` just started running underneath,
         which is the same contract the open uses on this screen. */
      Sound.voice('tannaz_opening_challenge', 0.9, null, { over: true });
    }
    runOpening();
  };

  var enterTitle = function () {
    if (S.screen !== 'splash') return;
    leaveSplash();
  };

  var backToFront = function () {
    if (S.screen !== 'splash') return;
    Sound.sfx('select');
    /* Before the screen moves, so the cue is already off the floor when the door
       lands — see the note above. This also puts back the bed her line ducked
       out, which the `refresh` below then re-reads as the door's. */
    Sound.cut();
    show('front');
    /* The door is MAIN's wherever the player came from. While the cold open is
       up the bed is the underscore and hers; `doneOpening` hands it over and
       reads the mapping fresh, under the door this time. */
    if (!S.opening) Sound.refresh();
  };

  /* ── Whose show is on the stage ───────────────────────────────────────────
     A course knows its own code, its professor and its university; MAIN knows
     its host. Both are edition data in both languages, not i18n keys — the same
     rule `editions.js` already sets for `name` and `blurb`. Everything below
     only arranges what a descriptor declares, and a descriptor that declares
     neither prints nothing at all, which is what keeps the main edition from
     wearing a course-shaped hole. */
  var readCredit = function (ed, lang) {
    var c = ed && ed.credit;
    if (!c) return null;
    return {
      code: c.code || '',
      name: (ed.name && ed.name[lang]) || ed.id,
      who: (c.professor && c.professor[lang]) || '',
      where: (c.institution && c.institution[lang]) || ''
    };
  };

  var paintCredits = function () {
    var lang = window.getLang();
    var ed = currentEdition();
    var c = readCredit(ed, lang);
    var host = ed && ed.host && ed.host.name;
    var hosted = host ? (host[lang] || host.en) : '';

    var card = el('edition-imprint');
    if (card) {
      card.classList.toggle('imprint-course', !!c);
      card.textContent = '';
      var bits = c ? [c.code, c.name].filter(Boolean) : [];
      if (c) {
        var title = document.createElement('span');
        title.className = 'imprint-title';
        title.textContent = bits.join(' · ');
        card.appendChild(title);
        var byline = document.createElement('span');
        byline.className = 'imprint-byline';
        byline.textContent = T('imprint.courseHosted', { who: c.who, where: c.where });
        card.appendChild(byline);
      } else if (hosted) {
        card.textContent = T('imprint.hosted', { name: hosted });
      }
      card.hidden = !c && !hosted;
    }

    /* The lobby's line is the same facts stacked for a column rather than run
       along a rule: who teaches it, and where. */
    var line = el('lobby-credit');
    if (line) {
      line.textContent = '';
      if (c && (c.who || c.where)) {
        if (c.who) {
          var who = document.createElement('span');
          who.className = 'credit-who';
          who.textContent = c.who;
          line.appendChild(who);
        }
        if (c.where) {
          var where = document.createElement('span');
          where.className = 'credit-where';
          where.textContent = c.where;
          line.appendChild(where);
        }
        line.hidden = false;
      } else {
        line.hidden = true;
      }
    }
  };

  /* ── The chooser ──────────────────────────────────────────────────────────
     Which show to put on the stage. Filled here, out of the registry, rather
     than written into the markup — a build carries MAIN plus every course it has
     a folder for, so any hand-written list would go stale the first time a
     course is added.

     Two shapes, because Morad asked for two: MAIN is a wide box, since the main
     edition is the corpus and is a different kind of thing from a course, and a
     course is a circle. The circles run in one row and the placeholders extend
     it — named, so a student can see which courses are coming, and stamped, so
     nobody queued up for one.

     Placeholders are plain elements rather than disabled buttons. That is not
     decoration — the pad walks a ring of real buttons, so a disabled control
     would need a special case to be skipped, and a div needs none.

     Every real door is one press into the show. Which one is current is marked,
     but nothing here depends on it: the press names the edition it is entering. */
  var footCards = [];

  /* The courses that are announced and not written *at all*: no folder, no
     syllabus, no art of their own, just a drawing and a name. A constant rather
     than more entries in the registry, because there was no edition behind them
     to carry. `name` is an i18n key for the same reason.

     Currently empty, and that is the good outcome: the Pahlavis were the last
     entry, and they have since gone the whole way — a real course in the
     registry, a bank behind it, and no plate on the front door at all. This
     stays because it is the established way to announce a course before there
     is a folder to put one in, and the machinery is proven. Adding the next one
     is one line here and one art file. */
  var SOON_CARDS = [];

  /* The plate that says the questions are not written yet. One builder for both
     kinds of unwritten course — the announced-with-a-folder and the
     announced-with-a-drawing — because it is the same sentence in both cases:
     the mark is real, the questions are not. */
  var makeStamp = function () {
    var stamp = document.createElement('span');
    stamp.className = 'soon-stamp';
    stamp.setAttribute('data-i18n', 'front.soon');
    stamp.textContent = T('front.soon');
    return stamp;
  };

  var makeArt = function (cls, src) {
    var art = document.createElement('img');
    art.className = cls;
    art.alt = '';
    art.setAttribute('aria-hidden', 'true');
    /* `src` is set only once there is art to put in it: a descriptor with no
       tile must not request a path it does not have and log a 404. */
    if (src) art.src = src;
    return art;
  };

  /* The glass over a circle. Empty, and it carries no content by design: it is
     the rim of the globe, and the only reason it is a node rather than a
     pseudo-element is that the mask which confines its `backdrop-filter` to the
     edge would also clip the specular highlight, and the highlight needs the
     whole box. The pseudo keeps the highlight; this keeps the edge. */
  var makeLens = function () {
    var lens = document.createElement('i');
    lens.className = 'lens';
    lens.setAttribute('aria-hidden', 'true');
    return lens;
  };

  /* MAIN's door. One shape for one show: the wide box the course circles are
     read against. */
  var makeDoor = function (ed) {
    var card = document.createElement('button');
    card.type = 'button';
    card.className = 'edition-card edition-main';

    var sign = document.createElement('span');
    sign.className = 'edition-sign';
    card.appendChild(sign);

    card.appendChild(makeArt('edition-art', ed.hero || ed.tile));
    card.appendChild(makeLens());

    var name = document.createElement('span');
    name.className = 'edition-name';

    var note = document.createElement('span');
    note.className = 'edition-note';

    var credit = document.createElement('span');
    credit.className = 'edition-credit';

    var lines = document.createElement('span');
    lines.className = 'edition-body';
    lines.appendChild(name);
    lines.appendChild(note);
    lines.appendChild(credit);

    var enter = document.createElement('span');
    enter.className = 'edition-enter';
    var enterLabel = document.createElement('span');
    enterLabel.className = 'edition-enter-label';
    var chev = document.createElement('span');
    chev.className = 'chev';
    chev.setAttribute('aria-hidden', 'true');
    enter.appendChild(enterLabel);
    enter.appendChild(chev);
    lines.appendChild(enter);
    card.appendChild(lines);

    card.addEventListener('click', function () { enterEdition(ed.id); });

    footCards.push({ el: card, ed: ed, name: name, note: note, credit: credit,
      enter: enterLabel, sign: sign, isHero: true });
    return card;
  };

  /* A course. Still a button — it is a door — but a circle, with the tile in the
     frame and the professor under the name, which is the one fact that tells a
     student they are in the right place. */
  var makeCourse = function (ed) {
    var card = document.createElement('button');
    card.type = 'button';
    card.className = 'circle';

    var frame = document.createElement('span');
    frame.className = 'circle-frame';
    frame.appendChild(makeArt('circle-art', ed.tile));
    frame.appendChild(makeLens());
    /* A course that is open but not yet written is the one circle that is both
       a door and carrying a plate: you may walk in and read the syllabus, and
       the questions are still coming. It keeps its own tile at full strength —
       the plate is the whole of the signal, and draining the art as well would
       say "not a door", which is the opposite of true here. */
    if (ed.locked) {
      frame.appendChild(makeStamp());
      card.classList.add('is-locked');
    }
    card.appendChild(frame);

    var name = document.createElement('span');
    name.className = 'circle-name';
    var who = document.createElement('span');
    who.className = 'circle-who';
    card.appendChild(name);
    card.appendChild(who);

    card.addEventListener('click', function () { enterEdition(ed.id); });

    footCards.push({ el: card, ed: ed, name: name, who: who, isHero: false });
    return card;
  };

  var makeSoon = function (spec) {
    var d = document.createElement('div');
    d.className = 'circle is-soon';
    d.setAttribute('aria-disabled', 'true');

    var frame = document.createElement('span');
    frame.className = 'circle-frame';
    frame.appendChild(makeArt('circle-art', spec.art));
    frame.appendChild(makeLens());

    /* The stamp goes inside the frame, so the frame's own clip lands it on the
       art as a stamp rather than floating it over the circle. */
    frame.appendChild(makeStamp());
    d.appendChild(frame);

    var name = document.createElement('span');
    name.className = 'circle-name';
    name.setAttribute('data-i18n', spec.name);
    name.textContent = T(spec.name);
    d.appendChild(name);

    /* No professor to name, but the slot is built and left standing empty:
       `#screen-front` gives it a line's height on every circle, so the three
       columns come out the same size and the three labels land on one line.
       Leaving it out would put these two a byline shorter than the live course
       beside them. It is not `hidden`, because the sheet's
       `[hidden] { display: none !important }` would take the line back. */
    var who = document.createElement('span');
    who.className = 'circle-who';
    d.appendChild(who);
    return d;
  };

  var paintCards = function () {
    /* A show's name and its blurb are edition data, not i18n keys — an edition
       names itself in both languages and the engine never has to learn it. The
       placeholders are the exception in both directions, because there is no
       edition behind them; theirs are keys, and `apply()` repaints them. */
    var lang = window.getLang();
    var here = window.getEdition();
    for (var i = 0; i < footCards.length; i++) {
      var entry = footCards[i];
      var ed = entry.ed;
      var name = (ed.name && ed.name[lang]) || ed.id;
      var c = readCredit(ed, lang);
      entry.name.textContent = name;

      var label;
      if (entry.isHero) {
        var note = (ed.description && ed.description[lang]) ||
          ((ed.blurb && ed.blurb[lang]) || '');
        var credit = c ? T('imprint.courseHosted', { who: c.who, where: c.where }) : '';
        entry.note.textContent = note;
        entry.note.hidden = !note;
        entry.credit.textContent = credit;
        entry.credit.hidden = !credit;
        entry.enter.textContent = T('front.enter');
        entry.sign.textContent = T('front.mainSign');
        label = [name, note, credit].filter(Boolean).join(' — ');
      } else {
        /* The line is left in the row even when a course has no professor to
           name, so that every circle in it is the same height. Empty rather
           than `hidden` — see `makeSoon`. */
        var who = c ? c.who : '';
        entry.who.textContent = who;
        label = [name, who].filter(Boolean).join(' — ');
      }

      entry.el.setAttribute('aria-label', label);
      if (ed.id === here) entry.el.setAttribute('aria-current', 'true');
      else entry.el.removeAttribute('aria-current');
    }
  };

  (function buildChooser() {
    var mainRow = el('foot-main');
    var courseRow = el('foot-courses');
    var all = window.getEditions();

    for (var i = 0; i < all.length; i++) {
      /* `general` is MAIN by name in the registry, and the registry is the one
         place that knows it. Anything else registered under this engine is a
         course — there is no third kind of show. */
      if (all[i].id === 'general') mainRow.appendChild(makeDoor(all[i]));
      else courseRow.appendChild(makeCourse(all[i]));
    }
    /* Real courses first, placeholders after: a student scanning the row meets
       the course they can sit in before the ones they cannot. */
    for (var j = 0; j < SOON_CARDS.length; j++) {
      courseRow.appendChild(makeSoon(SOON_CARDS[j]));
    }

    /* Each group hides with its own row, so a build with no courses still gets a
       front door rather than a heading over nothing. The courses group is what
       the placeholders hang off, so in practice it is always open. */
    el('chooser-main').hidden = !mainRow.firstChild;
    el('chooser-courses').hidden = !courseRow.firstChild;
    /* The chooser itself ships `hidden` in markup so the screen paints as one
       wordmark and a tagline before this runs — a flash of empty circles reads
       worse than a beat with none. By here every door has been built. */
    el('chooser').hidden = false;

    paintCards();
    paintCredits();
    /* Both, because the chooser answers two questions at once: the language
       decides how a show is spelled, and which show is current decides which
       door wears the mark. */
    document.addEventListener('langchange', paintCards);
    document.addEventListener('editionchange', paintCards);
    document.addEventListener('langchange', paintCredits);
    document.addEventListener('editionchange', paintCredits);
  })();

  /* Language is its own step, not a way into the game: the pills are on the
     front door and they leave you on the front door. The literal is passed
     because a pill is an explicit choice — the stored language is only a
     starting point. */
  function paintLanguageChoice() {
    var lang = window.getLang();
    [['lang-en', 'en'], ['lang-fa', 'fa']].forEach(function (pair) {
      var button = el(pair[0]);
      var on = pair[1] === lang;
      button.classList.toggle('is-on', on);
      button.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  el('lang-en').addEventListener('click', function () { Sound.sfx('select'); setLang('en'); });
  el('lang-fa').addEventListener('click', function () { Sound.sfx('select'); setLang('fa'); });
  document.addEventListener('langchange', paintLanguageChoice);
  paintLanguageChoice();
  el('splash-enter').addEventListener('click', enterTitle);
  el('splash-back').addEventListener('click', backToFront);

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

  el('open-settings').addEventListener('click', openSettings);
  el('open-howto').addEventListener('click', function () { Sound.sfx('select'); el('howto-panel').hidden = false; });

  /* The chooser. Its rows are built from the registry, so a build carrying one
     edition gets one row and a build carrying five gets five, with nothing here
     to keep in step. Built on open rather than at boot, which is also what keeps
     the names right: a row's label is edition data read in the current language,
     and half of what this list is for is being read after the language moved. */
  var editionsPanel = el('editions-panel');
  var buildEditions = function () {
    var body = el('editions-body');
    var here = window.getEdition();
    var lang = window.getLang();
    body.textContent = '';
    window.getEditions().forEach(function (ed) {
      var row = document.createElement('button');
      row.type = 'button';
      var mine = ed.id === here;
      /* The rim the controller's focus ring already uses. It reads as "this is
         the chosen one" here without a second thing for the eye to work out. */
      row.className = 'pill' + (mine ? ' is-on' : '');
      if (mine) row.setAttribute('aria-current', 'true');
      var label = document.createElement('span');
      label.className = 'pill-label';
      label.textContent = (ed.name && ed.name[lang]) || ed.id;
      row.appendChild(label);
      /* The current row carries no chevron: there is nowhere for it to go, and
         a control that visibly leads somewhere and then does not is worse than
         one that plainly does not. */
      if (!mine) {
        var chev = document.createElement('span');
        chev.className = 'chev';
        chev.setAttribute('aria-hidden', 'true');
        row.appendChild(chev);
      }
      row.addEventListener('click', function () {
        Sound.sfx('select');
        window.setEdition(ed.id);
        editionsPanel.hidden = true;
      });
      body.appendChild(row);
    });
  };

  el('open-editions').addEventListener('click', function () {
    Sound.sfx('select');
    buildEditions();
    editionsPanel.hidden = false;
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-close]'), function (btn) {
    btn.addEventListener('click', function () {
      var panel = el(btn.dataset.close);
      if (panel) panel.hidden = true;
      Sound.sfx('select');
    });
  });

  /* ── The Reading List ─────────────────────────────────────────────────────
     The shelf behind the questions: everything the current edition's corpus
     contains, not only the handful of books a given board happened to cite. The
     verdict card already prints which book an answer came from; this is the list
     that book belongs to.

     Which shelf is the current edition's — `readings` on the descriptor, the
     same way `banks` works and for the same reason — so a course ships its own
     and the engine learns nothing about any of them. An edition that declares no
     shelf gets an empty panel rather than MAIN's books under a course's name.

     Rebuilt on open, like the show list: the group headings and the panel's own
     title are in the current language, and `kind` is the corpus's own vocabulary
     (MAIN's shelves classify scholarship, the course's classify seminar
     reading), so neither the labels nor the counts can be baked in.

     Citations are Latin text on a page that may be RTL, so every one of them
     wears `.lat`. The chrome around them is translated; the books are not — a
     title is not a phrase, and it is not this engine's job to translate one. */
  var readingPanel = el('reading-panel');
  var pad2 = function (n) { return (n < 10 ? '0' : '') + n; };

  var buildReading = function () {
    var body = el('reading-body');
    var ed = currentEdition();
    var lang = window.getLang();
    body.textContent = '';

    el('reading-for').textContent = ed ? ((ed.name && ed.name[lang]) || ed.id) : '';
    var tile = el('reading-tile');
    if (ed && ed.tile) { tile.src = ed.tile; tile.hidden = false; }
    else { tile.removeAttribute('src'); tile.hidden = true; }

    var shelf = (ed && ed.readings) || [];
    var n = 0;

    shelf.forEach(function (group) {
      if (!group || !group.items || !group.items.length) return;

      var h = document.createElement('h3');
      h.className = 'reading-group';
      var gn = document.createElement('span');
      gn.className = 'reading-group-name';
      gn.textContent = (group.group && (group.group[lang] || group.group.en)) || '';
      var gc = document.createElement('span');
      gc.className = 'reading-count mono';
      gc.textContent = num(group.items.length);
      h.appendChild(gn);
      h.appendChild(gc);
      body.appendChild(h);

      group.items.forEach(function (item) {
        n += 1;
        var row = document.createElement('article');
        row.className = 'reading-row';

        var idx = document.createElement('span');
        idx.className = 'reading-num mono lat';
        idx.textContent = pad2(n);
        row.appendChild(idx);

        var text = document.createElement('span');
        text.className = 'reading-text';
        var title = document.createElement('span');
        title.className = 'reading-title lat';
        title.textContent = item.title || '';
        text.appendChild(title);
        if (item.author) {
          var author = document.createElement('span');
          author.className = 'reading-author lat';
          author.textContent = item.author;
          text.appendChild(author);
        }
        /* The annotation is MAIN's, written for this purpose in the manifest, and
           it is English-only — so it is printed where an English annotation
           belongs and never invented for the Persian edition. */
        if (item.note) {
          var note = document.createElement('span');
          note.className = 'reading-note lat';
          note.textContent = item.note;
          text.appendChild(note);
        }
        row.appendChild(text);

        var meta = document.createElement('span');
        meta.className = 'reading-meta';
        if (item.kind) {
          var kind = document.createElement('span');
          kind.className = 'reading-kind lat';
          kind.textContent = item.kind;
          meta.appendChild(kind);
        }
        if (item.year) {
          var year = document.createElement('span');
          year.className = 'reading-year mono lat';
          year.textContent = String(item.year);
          meta.appendChild(year);
        }
        row.appendChild(meta);

        body.appendChild(row);
      });
    });
  };

  el('open-reading').addEventListener('click', function () {
    Sound.sfx('select');
    buildReading();
    readingPanel.hidden = false;
  });

  el('start-game').addEventListener('click', startMatch);
  el('play-again').addEventListener('click', function () {
    Sound.cut();
    /* The match is over and the room is being left. Dispatched after the cut so
       the line lands in a silence rather than on top of the winner sting. */
    beat('leave');
    show('lobby');
    Sound.music('menu_theme');
  });

  setSoundSegments(Sound.isEnabled());
  setHapticsSegments(Haptics.isEnabled());

  /* The name fields carry the one piece of copy that is made in JS rather than
     written in the markup — the placeholder and the aria-label — so they are
     rebuilt when the room changes language. Unconditionally, because the
     language is picked on the splash and the green room is still hidden when
     that fires: gating this on the screen on show is what left "PLAYER 1" in
     Latin behind a Persian gate. `S.names` is the source of truth, so a rebuild
     never costs the player a name they have typed. */
  document.addEventListener('langchange', renderNames);

  /* A shared link lands on the show it names, not on the front door: the URL has
     already answered the question the chooser asks. `?ed=` outranks saved state
     inside `editions.js`, so the registry has resolved it before boot gets here;
     all this checks is whether the param named a show this build actually
     carries. An unknown id falls back to a saved or default edition, which is a
     front-door decision, so the markup's own landing screen stands.

     Deliberately no `runOpening()` here. Boot is not a gesture, so a play started
     now would be refused by the autoplay gate and the cold open would be lost
     silently; `arm()` already owns that job below and fires on the first real
     gesture, which is also the retry path when a play is refused. */
  (function deepLink() {
    var m = /[?&]ed=([A-Za-z0-9_-]{1,32})/.exec(location.search || '');
    if (!m || m[1] !== window.getEdition()) return;
    /* Not yet, while the boot pass is still running. This is the one caller that
       lifts a screen during boot, and the artwork it would be lifting it over is
       the artwork being fetched at that moment. The pass is told where to hand
       over instead, and lands here rather than on the front door. */
    if (S.screen === 'boot') { S.bootTarget = 'splash'; return; }
    show('splash');
  })();
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
  /* A short board is not an error the game can act on -- it deals what it has --
     but it is invisible until it is up in front of a room, and the usual cause
     is a bank that cannot fill twelve categories across the two rounds. Say so
     where the bank author will see it. */
  if (chosen.length < 6) {
    console.warn('Jeopardy: the ' + round + ' board deals ' + chosen.length +
                 ' categories, not 6. A category needs a clue at every rung of ' +
                 'the ' + round + ' ladder, and the rounds do not share.');
  }
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
      /* Which board is whose, said on the podium the room is already watching.
         It is a board-time fact and nowhere else: during a clue the same seat
         would be wearing "picks" while somebody else answers. */
      var choosing = hostId === 'podiums-board' && S.screen === 'board' &&
        S.phase === 'idle' && chooserLive() && S.chooser === i;
      if (choosing) card.classList.add('is-choosing');

      var name = make('span', 'pname');
      name.appendChild(make('span', 'pdot'));
      name.appendChild(document.createTextNode(p.name));
      if (choosing) name.appendChild(make('span', 'ppicks', T('board.picks')));
      var score = make('span', 'pscore', fmt(p.score));
      card.appendChild(name);
      card.appendChild(score);
      host.appendChild(card);
    });
  });
  onlineSync();
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

/* The first cell nobody has taken, read left to right and top to bottom. Where the
   cursor goes when the cell it was sitting on is gone. Null once the board is clear. */
function firstLive() {
  for (var row = 0; row < 5; row++) {
    for (var col = 0; col < S.board.length; col++) {
      var cell = S.board[col] && S.board[col].cells[row];
      if (cell && !cell.solved) return { col: col, row: row };
    }
  }
  return null;
}

function renderBoard() {
  var host = el('board');
  host.innerHTML = '';
  if (!S.board.length) return;

  /* The cursor is not reset between rounds, so it can end up on a cell that no
     longer exists or that has since been answered — and a cursor parked on a dead
     cell is drawn by nobody, which looks like the cursor has gone. Move it to the
     first live cell before anything is painted. */
  var here = S.board[S.cursor.col] && S.board[S.cursor.col].cells[S.cursor.row];
  if (!here || here.solved) {
    var live = firstLive();
    if (live) S.cursor = live;
  }

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
  startBoardClock();
  /* A robot holding the board is not a hung board. The pick clock would get
     there in twenty seconds; a contestant gets there in one. */
  armBotPick();
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
    btn.addEventListener('click', function () {
      if (!pickingHere()) { denyPick(); return; }
      openClue(col, row);
    });
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
   transition carries it across the gap, so the ring drains rather than steps.
   `reset` marks the first paint of a window. That one is not a step but a jump
   back to full, and it has to land in a single frame. Left to the transition it
   animates instead, and because stopClockNode's reset runs in the same task as
   the un-hiding, the browser never sees the node as hidden, so the previous
   window's in-flight transition carries straight through — a fresh twenty
   opening on a dial still showing what the last window died at. */
function paintClock(node, seconds, total, label, urgent, reset) {
  buildClock(node);
  var digits = node.querySelector('.clock-num');
  var lab = node.querySelector('.clock-label');
  /* num(), not String(): the countdown is read by the player. The local is not
     called `num` because that would shadow the helper and leave Latin digits on
     a Persian board. The --t property below stays ASCII — it feeds a calc(). */
  if (digits) digits.textContent = num(seconds);
  if (lab) lab.textContent = label;
  var share = String(Math.max(0, seconds) / total);
  if (reset) {
    node.style.transition = 'none';
    node.style.setProperty('--t', share);
    void node.offsetWidth;   /* land the jump before the transition comes back */
    node.style.transition = '';
  } else {
    node.style.setProperty('--t', share);
  }
  node.classList.toggle('is-urgent', seconds <= urgent);
}

function stopClockNode(node) {
  if (!node) return;
  node.hidden = true;
  node.classList.remove('is-urgent');
  /* Leave the dial full rather than wherever this run died, so a window that
     opens without an explicit reset still starts from the top. */
  node.style.setProperty('--t', '1');
}

/* Is the show being held? True whenever an overlay is up — the match menu, the
   settings panel, the how-to — because every one of them is read at leisure and
   none of them should be reading it to a running clock. All three of the game's
   clocks ask this on each tick and return early rather than their interval being
   cleared, and the difference matters: a cleared interval is reported to an
   online guest as no clock at all, so the guest's hand would vanish and come
   back while the host's sat still. Left running, the interval keeps publishing a
   countdown that has stopped moving, which is exactly what the same pause looks
   like from the other end of the wire. */
function showHeld() {
  return !!document.querySelector('.overlay:not([hidden])');
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

  var paint = function (reset) {
    paintClock(node, S.clueRemaining, seconds, label, urgent, reset);
  };
  paint(true);

  S.clueTimer = setInterval(function () {
    if (showHeld()) return;
    S.clueRemaining -= 1;
    if (S.clueRemaining <= 0) { stopClueClock(); onExpire(); return; }
    paint();
  }, 1000);
  /* A clock is the one thing on this screen that moves with nobody touching
     anything, so the hand in a guest's hand is reset the moment it does. */
  onlineSync();
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

  var paint = function (reset) {
    paintClock(node, S.boardRemaining, BOARD_SECONDS, T('clock.pick'), 5, reset);
  };
  paint(true);

  S.boardTimer = setInterval(function () {
    if (showHeld()) return;
    S.boardRemaining -= 1;
    if (S.boardRemaining <= 0) { stopBoardClock(); autoPick(); return; }
    paint();
  }, 1000);
  /* The pick clock starts after the board is up, so the sync that `show`
     already fired had nothing to say about it. */
  onlineSync();
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
  if (S.pickTimer) { clearTimeout(S.pickTimer); S.pickTimer = null; }
  S.clue = cell.clue;
  S.clueCtx = { col: col, row: row };
  S.clueWinner = null;
  S.lockedOut = [];
  S.buzzed = null;
  S.holder = null;
  S.armed = false;
  S.onlineVerdict = null;

  if (cell.dailyDouble) {
    Sound.sfx('wager');
    Sound.voice('tannaz_wager', 0.85);
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

function startClue(withBuzzers) {
  clearStealBeat();
  stopClueClock();
  Bots.cancel();
  S.phase = 'reading';
  S.armed = false;
  S.prematureUntil = {};
  if (S.lockoutTimer) { clearTimeout(S.lockoutTimer); S.lockoutTimer = null; }
  S.buzzed = null;
  S.writePrompted = false;

  /* The stage goes up before the question. An edition that introduces the
     category first needs somewhere to say it, and putting the board away here is
     what stops a second click landing mid-introduction. The text and the buzz
     row stay down until `revealClue`, so there is nothing to read — or buzz —
     while the room is still being set. */
  el('clue-category').textContent = S.clue.category;
  el('clue-value').textContent = fmtT(S.clue.value);
  el('clue-text').textContent = '';
  el('clue-verdict').hidden = true;
  el('clue-verdict').innerHTML = '';
  el('clue-actions').innerHTML = '';
  show('clue');
  renderPodiums();

  /* The pre-clue gate. An edition may own this moment — introduce the category,
     set the stage — and is handed the clue plus a `proceed` it must call when it
     is finished, or when the player skips it. A tap anywhere skips. With no
     edition asking for the gate the question goes straight up, which is the
     public build's behaviour, unchanged. */
  var revealed = false;
  function skip() { proceed(); }
  function proceed() {
    if (revealed) return;
    revealed = true;
    document.removeEventListener('pointerdown', skip, true);
    Sound.cut();
    revealClue(withBuzzers);
  }
  if (window.HOST_PRECLUE) {
    document.addEventListener('pointerdown', skip, true);
    window.HOST_PRECLUE(S.clue, proceed);
  } else {
    revealClue(withBuzzers);
  }
}

/* The question itself. Everything the engine does *with* a clue on the board —
   the announcement, the text, the clock, the buzz row — lives here, so none of
   it can run while the pre-clue gate still owns the stage. */
function revealClue(withBuzzers) {
  beat('clueOpen', { category: S.clue.category, race: !!withBuzzers });
  el('clue-text').textContent = S.clue.clue;
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
    flagPodium(S.holder);
    startClueClock(ANSWER_SECONDS, T('clock.answer'), function () { answer(-1); });
    requestAnimationFrame(fitClueText);
    Bots.onFloor(S.holder);
    return;
  }

  Sound.music('thinking_loop');
  renderClueActions();
  /* The read window is the clock's, not a timer's: when it runs out the buzzers
     open and a fresh clock takes over. One mechanism, so the two windows can
     never disagree about which one is running. */
  startClueClock(READ_SECONDS, T('clock.read'), openBuzzers, 3);
}

/* The clue has been read. The lamp goes live and the race starts. */
function openBuzzers() {
  if (S.phase !== 'reading') return;
  S.armed = true;
  /* Nothing to settle here: a foul was timed and booked at the press, and the
     timer that lifts it was set then. The lamp does not start or extend a
     penalty, it only ends the wait — a thumb that went down early is already
     partway through its second and a half by the time the room is racing. */
  /* The read is over and the room is quiet for it. An edition that talks over a
     clue gets its moment here instead — once per clue, because a steal comes
     back through the steal beat and not through this door. */
  beat('buzzersOpen', { category: S.clue.category });
  /* The clue's one window, full. Every press shortens what is left of it. */
  S.buzzLeft = buzzSeconds();
  Sound.sfx('armed');
  renderClueActions();
  popBuzzers();
  startClueClock(buzzWindowSeconds(), T('clock.buzz'), expireBuzz);
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

/* Whose thumb owns the screen. A buzz is a race between people, and a robot is
   not a thing that can reach over and press a plate — so the plate stops being
   one of a row the moment there is only one person sitting at the machine. Two
   humans at one keyboard still get one plate each; two humans at one *phone*
   cannot, which is the whole reason the count is the test and not the viewport. */
function soloHuman() {
  var humans = 0;
  for (var i = 0; i < S.players.length; i++) {
    /* A guest at an online table is not a thumb at this machine, however human
       they are on the other end of the wire. */
    if (!S.players[i].bot && !S.players[i].remote) humans++;
  }
  return humans === 1;
}

/* Is this seat somebody else's device? */
function isRemote(idx) {
  return idx != null && S.players[idx] != null && !!S.players[idx].remote;
}

/* A seat that answers for itself: a robot has its own brain and a guest has the
   phone in their hand, so neither one's answer is a thumb at this machine's to
   give. The clue screen has always said so by disabling their buttons — this is
   the same test, named, so the keyboard and the pad can be held to it too. */
function answersItself(idx) {
  return Bots.isBot(idx) || isRemote(idx);
}

/* ── Whose board it is ────────────────────────────────────────

   The clue was answered by one seat, and that seat takes the room to the next
   clue. It used to be whoever happened to be sitting at the machine, which at
   an online table is always the host and on a couch is always the left podium —
   so player one chose every category for the whole show.

   The rule is the show's: the seat that got it right picks. If nobody got it
   right, nobody earned it, so the pick is drawn at random. The board is then
   LOCKED to that seat the way the buzz floor is locked to the thumb that rang
   in — a board anyone can move is a board that is back to being player one's.

   A seat that cannot act does not become the room's problem. A robot picks for
   itself on a beat, and if the chooser has no controller plugged in, any pad may
   stand in, exactly as the answering floor already allows. */

function randomSeat() {
  return S.players.length ? Math.floor(Math.random() * S.players.length) : null;
}

function chooserLive() {
  return S.chooser != null && S.chooser >= 0 && S.chooser < S.players.length;
}

function chooserName() {
  return chooserLive() ? S.players[S.chooser].name : null;
}

/* The seat that just answered. A right answer names the chooser; anything else
   is a board the room won at random. Called once per clue, on the way out. */
function nameChooser() {
  S.chooser = S.clueWinner != null ? S.clueWinner : randomSeat();
  S.clueWinner = null;
}

/* Whether the thumb on THIS device is the chooser's own. A robot picks for
   itself and a guest picks on their own phone, so neither is done from here —
   and `null` means the match has not named anybody, which locks nobody out. */
function pickingHere() {
  if (!chooserLive()) return true;
  if (Bots.isBot(S.chooser)) return false;
  if (Online.role === 'host') return !isRemote(S.chooser);
  if (Online.role === 'guest') return S.chooser === Online.me;
  return true;
}

/* A locked board has to say so. Doing nothing at all reads as a broken button,
   and a player will press it four more times before concluding anything else. */
function denyPick(who) {
  if (S.screen !== 'board') return;
  Sound.sfx('incorrect', 0.35);
  Haptics.foul(who);
  ['podiums-board', 'podiums-clue'].forEach(function (hostId) {
    var host = el(hostId);
    var card = host && chooserLive() && host.children[S.chooser];
    if (!card) return;
    card.classList.add('is-denied');
    setTimeout(function () { card.classList.remove('is-denied'); }, 420);
  });
}

/* A robot that won the board takes it on a beat, the way a contestant reaches
   for a tile: look, then choose. It picks a live cell rather than the cursor so
   the room cannot tell a robot's turn from the clock running out. */
function armBotPick() {
  if (S.pickTimer) { clearTimeout(S.pickTimer); S.pickTimer = null; }
  if (S.screen !== 'board' || !chooserLive() || !Bots.isBot(S.chooser)) return;
  S.pickTimer = setTimeout(function () {
    S.pickTimer = null;
    if (S.screen !== 'board' || !chooserLive() || !Bots.isBot(S.chooser)) return;
    var live = [];
    for (var c = 0; c < S.board.length; c++) {
      for (var r = 0; r < S.board[c].cells.length; r++) {
        if (!S.board[c].cells[r].solved) live.push({ col: c, row: r });
      }
    }
    if (!live.length) return;
    var spot = live[Math.floor(Math.random() * live.length)];
    S.cursor = spot;
    openClue(spot.col, spot.row);
  }, BOT_PICK_MS);
}

/* The window opening is the one moment on this screen nobody may miss, so the
   plate arrives rather than merely changing colour. Fired from the arm and not
   from the row's own class, because repainting for a foul must not replay it. */
function popBuzzers() {
  var row = el('clue-actions').querySelector('.buzz-row');
  if (!row) return;
  row.classList.add('is-popping');
  /* Cleared on a timer rather than on `animationend`: the event is not dependable
     (a frame that never paints never ends its animation) and a class left behind
     would swallow the pop on the next arm, because re-adding a class the element
     already carries is not a change. */
  setTimeout(function () { row.classList.remove('is-popping'); }, 420);
}

/* Taking the floor is the one event the whole room has to catch, and the name
   card is where the room is already looking. It jumps once, in the player's own
   colour. The jump is the news and the ring it lands on is the state — so this
   fires from the buzz and never from the class, or a repaint on a wrong answer
   would announce the same news twice. Robots come through the same door. */
function flagPodium(index) {
  ['podiums-board', 'podiums-clue'].forEach(function (hostId) {
    var host = el(hostId);
    var card = host && host.children[index];
    if (!card) return;
    card.classList.add('is-buzzing');
    setTimeout(function () { card.classList.remove('is-buzzing'); }, 560);
  });
}

function renderClueActions() {
  var host = el('clue-actions');
  host.innerHTML = '';

  if (S.phase === 'reading') {
    host.appendChild(buzzNotifier());

    var solo = soloHuman();
    var row = make('div', 'buzz-row' + (S.armed ? ' is-live' : '') + (solo ? ' is-solo' : ''));
    var early = null;
    S.players.forEach(function (p, i) {
      /* One person at the machine means every other seat is a robot, and a
         robot's plate is a thing that looks pressable and is not. Showing one
         plate is the whole point of the solo layout; showing four is the
         question it exists to answer. */
      if (p.remote) return;
      if (solo && p.bot) return;
      var b = document.createElement('button');
      b.type = 'button';
      var cooled = S.prematureUntil[i] > Date.now();
      if (cooled) early = p.name;
      b.className = 'buzz-btn' + (cooled ? ' is-early' : '');
      b.style.setProperty('--pc', p.color);
      /* A premature press is not swallowed — it costs. The button goes dead the
         moment the thumb lands early and comes back when the lockout it started
         expires, which may be before the lamp even opens. */
      b.disabled = cooled || S.lockedOut.indexOf(i) !== -1;
      if (solo) {
        /* Nobody to tell apart, and no number row worth reaching for, so the
           plate says the only word it needs to say. */
        b.appendChild(make('span', null, T('buzz.plate')));
      } else {
        b.appendChild(make('span', null, T('buzz.with', { name: p.name })));
        b.appendChild(make('small', null, num(i + 1)));
      }
      b.addEventListener('click', function () { buzz(i); });
      row.appendChild(b);
    });
    host.appendChild(row);

    var hint;
    if (S.lockedOut.length) {
      hint = T('buzz.out');
    } else if (early) {
      hint = T('buzz.early', { name: early });
    } else if (solo) {
      /* One plate and one person means the plate can stop being an instruction
         to find and start being an instruction to act on. */
      hint = T(S.armed ? 'buzz.soloLive' : 'buzz.soloWait');
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
       be watched, not pressed, and a human is not allowed to answer for it. The
       same goes for a guest at an online table — their controls are the ones in
       their hand, and the host pressing for them would be passing the answer
       across the room. */
    var bot = answersItself(S.buzzed);

    /* Write-in mode replaces the board's four choices with the box. Painting
       the choices underneath would hand the clue to anyone who glances at
       them, which is the one thing the mode exists to prevent. */
    if (S.answerMode === 'write') {
      host.appendChild(writeField(bot, isFinal));
      Pads.syncOptions();
      return;
    }

    var opts = make('div', 'options');
    (S.clue.displayOptions || S.clue.options).forEach(function (text, i) {
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
  /* A thumb already fouled stays fouled — one press, one foul, no drumroll of
     wrong-answer bleeps. This also covers the press that is the foul. */
  if (S.prematureUntil[playerIndex] > Date.now()) return;

  /* Jumping the lamp is a foul, not a no-op: the thumb goes in the sin bin for
     the engine's own penalty window while everyone else stays live. */
  if (!S.armed) { prematureBuzz(playerIndex); return; }

  /* The race stops here. Whatever is left of the clue's window is what the next
     contestant inherits if this answer is wrong — a steal is the rest of the
     same window, not a fresh one. Grab it before the answer clock below takes
     `S.clueRemaining` for itself. */
  S.buzzLeft = Math.max(1, S.clueRemaining);

  Sound.sfx('buzz');
  /* Whose thumb this was, felt. A robot and a guest on their own phone are both
     somebody else getting there first, and both have to feel different from your
     own thumb landing — otherwise the one thing the haptic exists to tell you is
     the one thing it cannot say. The guest is the one that used to lie: their
     buzz rang this device's own take, the heaviest thing the show says, for a
     thumb that was never in this room. Their own phone already felt that take
     when they pressed it, which is why this seat is the one their pads leave out. */
  if (isRemote(playerIndex)) Haptics.beat(playerIndex);
  else if (S.players[playerIndex] && S.players[playerIndex].bot) Haptics.beat();
  else Haptics.take(playerIndex);
  S.buzzed = playerIndex;
  S.phase = 'answering';
  S.writePrompted = false;
  renderClueActions();
  renderPodiums();
  flagPodium(playerIndex);
  startClueClock(ANSWER_SECONDS, T('clock.answer'), function () { answer(-1); });
  Bots.onFloor(playerIndex);
}

function prematureBuzz(playerIndex) {
  /* The penalty starts at the press, and this is deliberate. Timed from the
     lamp it was a sentence rather than a mistake: a thumb ten seconds early sat
     dead for eleven and a half, identical in cost to one a second early, and
     neither had anything to do with being fast. Timed from the press it is a
     second and a half whenever it is served, so a press one second before the
     lamp leaves half a second of it on the far side of the lamp — not fast
     enough, which is the whole thing the buzzer is testing — while a press ten
     seconds early has come and gone long before the race. */
  S.prematureUntil[playerIndex] = Date.now() + EARLY_LOCKOUT_MS;
  Sound.sfx('incorrect', 0.4);
  /* A refusal has to be unmistakable from an acceptance. This is the only place
     the show says no to a live thumb, so it is the only place that says it. */
  if (!(S.players[playerIndex] && S.players[playerIndex].bot)) Haptics.foul(playerIndex);
  renderClueActions();
  /* The buzz row repaints once when the lockout lifts. The clock's own tick
     only paints the clock, so a button disabled here would stay dead for the
     rest of the clue unless this timer brings it back. */
  if (S.lockoutTimer) clearTimeout(S.lockoutTimer);
  S.lockoutTimer = setTimeout(function () {
    S.lockoutTimer = null;
    if (S.phase === 'reading') renderClueActions();
    /* The repaint above is the host's own row. A guest's button lives on the
       guest's phone and is only ever redrawn from a picture, so without this
       the phone stayed fouled for the rest of the clue — which is what "my
       buzzer sometimes shows up" looks like from the sofa. */
    onlineSync();
  }, EARLY_LOCKOUT_MS + 20);
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
  noteScore(player, isCorrect);
  /* The right answer is the one thing that earns the next board. A miss leaves
     the mark where it is, so a steal can still take it. */
  if (isCorrect) S.clueWinner = S.buzzed;

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
  /* The same ruling `buzz` makes, for the same reason: a seat that has already
     missed this clue is out of it. The buttons are disabled on the host's own
     screen and on the phone alike — but only one of those can be trusted. */
  if (S.lockedOut.indexOf(S.buzzed) !== -1) return;
  if (optionIndex < 0) return answerWith({ correct: false, timedOut: true, mark: -1 });
  answerWith({ correct: optionIndex === S.clue.correct, mark: optionIndex });
}

/* A typed answer. The judge is the only thing that decides this one — there is
   no index to compare. A "prompt" is not a wrong answer: the host is asking
   which Fazlollah, and the clock keeps running while the contestant says. */
function answerWritten(text) {
  if (S.mode === 'final') { submitFinalWritten(text); return; }
  if (S.phase !== 'answering' || S.buzzed == null) return;
  if (S.lockedOut.indexOf(S.buzzed) !== -1) return;
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

/* The pending hand-over, if there is one. Cancelled by anything that ends the
   clue or opens a new one, so a beat armed for a miss cannot outlive it. */
function clearStealBeat() {
  if (S.stealTimer) { clearTimeout(S.stealTimer); S.stealTimer = null; }
}

/* Whether a typed answer was typed on THIS device. The readback below exists so
   that whoever typed can see what was judged, and it addresses them as "you" —
   which is only true of the seat in front of this screen. A robot types into
   the same field the room is already watching it fill, and a guest's answer was
   typed on a phone that gets the same line out of the snapshot, so neither one
   is told its own words were the player's. */
function typedHere(seat) {
  if (seat == null || seat < 0) return false;
  if (Bots.isBot(seat)) return false;
  if (Online.role === 'host') return seat === 0;
  return Online.role == null;
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
  if (extra && extra.said && typedHere(S.players.indexOf(player))) {
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

  /* Handing the room the steal back. One function for both doors into it — the
     beat and the button — so the button can never leave a beat armed behind it
     and put the buzzers up twice for one clue.

     Only the button is allowed to talk over her. A player pressing on is asking
     for the next thing and her taunt is in their way; the beat is nobody asking
     for anything, and the wrong-answer lines run from 1.7 to 4.4 seconds — cut
     at a fixed two, every one of them would lose its punchline. Left alone she
     finishes over the live window, and her bed comes back when she does. */
  function stealAgain(cut) {
    clearStealBeat();
    if (cut) Sound.cut();
    S.buzzed = null;
    S.phase = 'reading';
    S.armed = true;
    S.prematureUntil = {};
    if (S.lockoutTimer) { clearTimeout(S.lockoutTimer); S.lockoutTimer = null; }
    /* A fresh steal is a fresh question to the judge: the next contestant is
       not inheriting the previous one's demand for a full name. */
    S.writePrompted = false;
    host.hidden = true;
    host.innerHTML = '';
    Sound.music('thinking_loop');
    renderClueActions();
    renderPodiums();
    /* `S.buzzLeft`, not `buzzSeconds()`: the clue has one window and whoever
       just missed has already spent some of it. Handing the room a fresh
       twenty seconds here is the bug this line used to be. */
    startClueClock(buzzWindowSeconds(), T('clock.buzz'), expireBuzz);
    Bots.armBuzzers();
  }

  var next = make('button', 'next-btn', T(canRetry ? 'verdict.secondChance' : 'verdict.continue'));
  next.type = 'button';
  next.addEventListener('click', function () {
    if (canRetry) stealAgain(true);
    else closeClue();
  });
  host.appendChild(next);

  /* A miss the room can still steal hands itself back after a beat. The timer
     stays out of the current task on purpose: `onlineSync` coalesces a burst of
     state changes into one picture for the guests, and a hand-over fired in the
     same task as the verdict would push only the buzzers — the phones would
     never see the lockout. A timer is its own task, exactly like the click this
     replaces. */
  if (canRetry) {
    clearStealBeat();
    S.stealTimer = setTimeout(function () {
      S.stealTimer = null;
      /* Only the clue still on screen may be reopened. A player who quit or hit
         Escape while the panel was up has taken the clue away with them. */
      if (S.screen !== 'clue' || S.phase !== 'answering' || S.buzzed == null) return;
      stealAgain(false);
    }, STEAL_BEAT_MS);
  }

  /* The sting states the outcome; she comments on it a beat later. Every
     verdict gets a line now, not just the right ones. */
  if (kind === 'right') Sound.sfx('correct', 0.5);
  /* A miss is not always the same miss. Running out of time is its own kind, and
     so is a lockout — a wrong answer with the clue still live for a steal. Both
     are real pools an edition may have recorded for and neither is `wrong`. */
  Sound.hostLine(kind === 'right'
    ? 'right'
    : (timedOut ? 'timeout' : (canRetry ? 'lockout' : 'wrong')));

  /* The guest's phone shows this verdict too, and it has no DOM to scrape: what
     goes on the wire is the ruling in its parts. The answer and the explanation
     are held back with everything else that would give the clue away, so a
     steal still has something to steal. */
  S.onlineVerdict = {
    kind: kind === 'right' ? 'right' : 'wrong',
    head: head,
    line: line || null,
    said: (extra && extra.said) || null,
    seat: player ? S.players.indexOf(player) : null,
    by: player ? player.name : null,
    canRetry: !!canRetry,
    answer: canRetry ? null : clue.answer,
    explain: canRetry ? null : (clue.explanation || null),
    source: canRetry ? null : (src || null)
  };
  onlineSync();

  host.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function closeClue() {
  /* The clue is over; so is her comment on it. */
  clearStealBeat();
  Sound.cut();
  /* The last clue of the round names the chooser for the round after it: the
     seat that answered it opens the next board too, and a round change is not a
     new show. */
  nameChooser();
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

  /* A guest wagers on their own phone. The host keeps the wager screen, because
     that is the show — but the slider here is dead, because the number is not
     the host's to pick. The guest's lock comes back over the wire and lands in
     `Online.wager.lock`, which is the same `onLock` a thumb here would have
     fired. */
  if (isRemote(opts.playerIndex)) {
    Online.wager = {
      index: opts.playerIndex,
      lock: opts.onLock,
      max: max,
      step: step,
      panel: {
        title: opts.title,
        category: opts.category,
        subtitle: opts.subtitle,
        amount: amount
      }
    };
    lock.disabled = true;
    lock.textContent = T('online.waitLock', { name: player.name });
    onlineSync();
    return;
  }

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
  onlineSync();
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
  Sound.voice('tannaz_final', 0.85);
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
    /* The Final's thirty seconds are the worst of the three to let run behind a
       menu: they are scored against the contestant whose turn it is. */
    if (showHeld()) return;
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
  noteScore(player, isCorrect);
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
  if (result.said && typedHere(idx)) {
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

  /* The Final has no steal — the wager is settled and the match is over — so of
     the two ways to miss, only running out of time gets its own pool here. */
  Sound.hostLine(isCorrect ? 'right' : (timedOut ? 'timeout' : 'wrong'));

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

  /* Two remarks a match can end on, and both are addressed to the person
     playing — so neither fires unless the human took the top seat outright or
     finished strictly last. A tie is nobody's win and a table of robots has
     nobody to congratulate. The seats are already ranked; the checks are the
     same three the results screen just drew. */
  var last = ranked[ranked.length - 1];
  if (!tie && top && !top.bot && !top.remote) beat('win', { seat: top });
  else if (!tie && last && last !== top && !last.bot && !last.remote) beat('loss', { seat: last });
}

// ── Match control ──────────────────────────────────────────

function startMatch() {
  /* The second lock on the locked course's door. The lobby's own button is out
     of service for one and says why, so this is unreachable from the ordinary
     path — but a queued press, a keyboard path or a caller added later would
     otherwise deal six empty categories and stall the show on a board with
     nothing on it. Refusing loudly is not possible here (there is no board to
     shake) and is not needed: the screen the player is standing on already
     spells it out. */
  if (!editionBanks()) return;
  Sound.cut();
  /* The bank is read here, off the language and the edition that are actually on
     screen. This is the last moment before a board is dealt, and dealing is the
     only thing that pins a clue to a bank — so it is the only moment where the
     answer cannot be wrong. Everything upstream of this is a convenience that can
     be skipped; this cannot. */
  rebindBanks(window.getLang());
  /* At an online table the host is seat 0 and everybody who turned up has a
     seat of their own, so the table is never smaller than the people at it. The
     seats nobody took are robots, the same as a couch game. */
  var online = S.online && S.online.role === 'host' ? S.online : null;
  if (online && S.playerCount < online.order.length + 1) {
    S.playerCount = Math.min(PLAYER_SEATS, online.order.length + 1);
  }
  /* The seats are about to be rebuilt from nothing, and the streak counters and
     the record of who led live on the seats — so the ledger resets with them
     rather than carrying a match's worth of history into the next one. */
  MATCH_BEATS = { top: null, last: null };
  S.players = [];
  for (var i = 0; i < S.playerCount; i++) {
    var guest = online ? onlineGuest(i) : null;
    var raw = guest ? guest.name : (S.names[i] || '').trim();
    /* `mixed` is the couch: the person who set the game up has the leftmost
       podium and everybody to their right is a robot. `bots` is the practice
       room. A robot takes its name from the host's string table rather than the
       field, so a seat keeps its name across a language switch. */
    var bot = online ? (!guest && i > 0) : Bots.seatIsBot(i);
    S.players.push({
      name: guest ? (guest.name || T('setup.playerDefault', { n: num(i + 1) }))
        : bot ? T(Bots.nameKey(i))
        : (raw || T('setup.playerDefault', { n: num(i + 1) })),
      score: 0,
      color: PLAYER_COLORS[i],
      bot: bot,
      remote: guest ? guest.peerId : null,
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
  /* Nobody has earned the board yet — the show opens on a draw, not on the
     podium nearest the camera. */
  S.clueWinner = null;
  S.chooser = randomSeat();
  if (S.pickTimer) { clearTimeout(S.pickTimer); S.pickTimer = null; }

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
  /* Every screen a match can be running on carries one of these, so the menu is
     never out of a thumb's reach: the board's corner on a computer, and the same
     control in the clue bar on the clue and the wager, where there is no corner
     and — on a phone — no Escape key and often no controller either. Bound by
     attribute rather than by id so the three are one listener. */
  var openers = document.querySelectorAll('[data-open-menu]');
  for (var m = 0; m < openers.length; m++) openers[m].addEventListener('click', openMenu);
  el('match-menu').addEventListener('click', function (ev) {
    if (ev.target === el('match-menu')) closeMenu();
    var btn = ev.target.closest('button[data-menu]');
    if (!btn) return;
    var action = btn.dataset.menu;

    closeMenu();
    if (action === 'resume') return;
    if (action === 'restart') { startMatch(); return; }
    /* The same panel the lobby opens, reached from inside a match. Closing the
       menu first is what keeps the two overlays from stacking: `openOverlay()`
       hands the pad the first one it finds, and a settings panel hidden behind a
       live match menu would be unreachable to a controller. */
    if (action === 'settings') { openSettings(); return; }
    if (action === 'lobby') {
      stopClueClock();
      stopBoardClock();
      show('lobby');
      Sound.music('menu_theme');
    }
  });
}

/* One opener for the settings panel, because it now has two doors: the lobby's
   button and the in-match menu. */
function openSettings() {
  /* The keyboard row describes the answer controls, and the two answer modes
     have different ones — A–D versus typing. Pick the row's string here rather
     than leaving it fixed, or a write-in room is told to press keys it has no
     buttons for. */
  var kb = document.querySelector('[data-i18n-html^="settings.keyboardBody"]');
  if (kb) {
    kb.setAttribute('data-i18n-html',
      S.answerMode === 'write' ? 'settings.keyboardBodyWrite' : 'settings.keyboardBody');
    applyI18n();
  }
  Sound.sfx('select');
  el('settings-panel').hidden = false;
}

function openMenu() {
  S.menuIndex = 0;
  el('match-menu').hidden = false;
  paintMenu();
  /* The board clock waits while the menu is up, and `showHeld` is what does the
     waiting now. It used to be stopped here and restarted on the way out, which
     did pause it — and also silently handed a fresh BOARD_SECONDS to anyone who
     opened the menu forty seconds into a pick, since `startBoardClock` assigns
     the count rather than resuming it. One mechanism, and the count survives. */
  Sound.sfx('select', 0.4);
}

function closeMenu() {
  el('match-menu').hidden = true;
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
  paintStage();
}

/* The two switches, handed to the halves that obey them and then written into
   the settings panel's chips. The drawing half is a course's property as much
   as MAIN's — both stand their speaker on the same layer — so this reaches the
   professor in the course editions too, and the audio half is the same `Sound`
   both shows cue through. Called once at boot, which is what keeps the panel
   from describing a stage the layer is not standing on. */
function applyStage() {
  if (window.HostLayer) window.HostLayer.setStage({ sprites: S.sprites, voice: S.voice });
  Sound.setVoiceEnabled(S.voice);
  paintStage();
}

/* Each switch is written into the segmented control that carries it. The chips
   are lit the way every other segmented control in the show is — `is-on` and
   `aria-checked` — because there is no longer a pill here to hold a state word,
   and a settings row should read like the settings rows around it. */
function paintStage() {
  var states = { sprites: S.sprites, voice: S.voice };
  Object.keys(states).forEach(function (key) {
    var host = el('settings-' + key);
    if (!host) return;
    Array.prototype.forEach.call(host.children, function (b) {
      var isOn = (b.getAttribute('data-' + key) === 'on') === states[key];
      b.classList.toggle('is-on', isOn);
      b.setAttribute('aria-checked', isOn ? 'true' : 'false');
    });
  });
}

// ── Input ──────────────────────────────────────────────────

function moveCursor(dc, dr) {
  if (!S.board.length) return;
  var col = S.cursor.col, row = S.cursor.row;
  /* Step past anything already answered. The cursor is only ever lit on a live
     cell, so parking it on a dead one would look like the cursor had gone and
     leave Return with nothing to open. Walk until a live cell or the wall. */
  for (var step = 0; step < 6; step++) {
    var nc = Math.min(Math.max(col + dc, 0), S.board.length - 1);
    var nr = Math.min(Math.max(row + dr, 0), 4);
    if (nc === col && nr === row) break;
    col = nc; row = nr;
    var cell = S.board[col] && S.board[col].cells[row];
    if (cell && !cell.solved) break;
  }
  /* A direction with nothing live left in it is not a move, it is a wall. */
  var landed = S.board[col] && S.board[col].cells[row];
  if (!landed || landed.solved) { col = S.cursor.col; row = S.cursor.row; }
  if (col === S.cursor.col && row === S.cursor.row) return;
  S.cursor = { col: col, row: row };
  Sound.sfx('select', 0.3);
  renderBoard();
}

/* What the arrow keys walk on a screen that has no cursor of its own. Focus moves
   for real rather than a lamp being painted on a ring, so the browser's own
   Return and Space do the activating and Tab keeps working beside them.

   The scope is passed in and never assumed to be the document: an inactive screen
   is `visibility: hidden`, not display:none, so its controls are still laid out
   and a walk over everything would hand the keyboard to a button nobody can see. */
function focusables(scope) {
  if (!scope) return [];
  var all = scope.querySelectorAll('button, [href], input, select, textarea');
  var out = [];
  for (var i = 0; i < all.length; i++) {
    if (all[i].disabled || !all[i].getClientRects().length) continue;
    out.push(all[i]);
  }
  return out;
}

function walkFocus(ev, scope) {
  var dir = ev.key === 'ArrowRight' || ev.key === 'ArrowDown' ? 1
          : ev.key === 'ArrowLeft' || ev.key === 'ArrowUp' ? -1 : 0;
  if (!dir) return false;
  var list = focusables(scope);
  if (!list.length) return false;
  var at = list.indexOf(document.activeElement);
  /* Nothing focused yet, so the first arrow press lands on the first control —
     and the last one, if the press was Up or Left. */
  if (at === -1) at = dir > 0 ? -1 : 0;
  ev.preventDefault();
  list[(at + dir + list.length) % list.length].focus();
  Sound.sfx('select', 0.3);
  return true;
}

/* One person at one screen is one thumb, and asking that thumb to find a plate
   the size of a postage stamp on a phone is the wrong question. While exactly
   one seat is human, the stage itself is the buzzer: any press that does not
   land on a real control is a press on the plate.

   Only while the lamp is on. Before the window opens the full screen is not a
   buzz surface at all — a stray tap on a phone is not a jumped lamp, and the
   penalty for one belongs to the plate a contestant had to aim at, not to the
   wallpaper. Capture phase, so the race is won on the way down and a press that
   lands mid-scroll still counts as a press. */
function initStageBuzz() {
  document.addEventListener('pointerdown', function (ev) {
    if (!soloHuman()) return;
    if (S.screen !== 'clue' || S.phase !== 'reading' || !S.armed) return;
    if (ev.target && ev.target.closest &&
        ev.target.closest('button, a, input, select, textarea, label, summary, .overlay')) return;
    buzz(0);
  }, true);
}

function initKeyboard() {
  document.addEventListener('keydown', function (ev) {
    var menuOpen = !el('match-menu').hidden;
    /* A contestant typing an answer is not pressing A, B, C or 1–4: while a
       field has the keyboard, the field has the keyboard. Enter belongs to the
       field too, which is how the answer is locked in. */
    var typing = ev.target && (ev.target.tagName === 'INPUT' || ev.target.tagName === 'TEXTAREA');

    /* The frontmost thing on the page is an overlay if there is one — settings or
       how-to — and the frontmost thing is what the keyboard answers to first. */
    var overlay = document.querySelector('.overlay:not([hidden])');

    if (ev.key === 'Escape') {
      if (menuOpen) { closeMenu(); return; }
      if (overlay) {
        var shut = overlay.querySelector('[data-close]');
        if (shut) { shut.click(); return; }
      }
      if (S.screen === 'board' || S.screen === 'clue' || S.screen === 'wager') { openMenu(); return; }
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

    /* An overlay owns the arrows while it is up, so they never reach the board
       behind it. Return is left alone: the browser already activates whichever
       control has focus. */
    if (overlay) {
      if (!typing) walkFocus(ev, overlay);
      return;
    }

    if (S.screen === 'board') {
      var arrows = { ArrowLeft: [-1, 0], ArrowRight: [1, 0],
                     ArrowUp: [0, -1], ArrowDown: [0, 1] };
      var open = ev.key === 'Enter' || ev.key === ' ';
      if (arrows[ev.key] || open) {
        ev.preventDefault();
        /* The keyboard is the machine's own hand, so it answers to the same rule
           the pads do: the board is the chooser's, and it says so when it is
           not yours. */
        if (!pickingHere()) { denyPick(); return; }
        if (open) openClue(S.cursor.col, S.cursor.row);
        else moveCursor(arrows[ev.key][0], arrows[ev.key][1]);
      }
      return;
    }

    if (S.screen === 'clue' || S.screen === 'wager') {
      if (typing) return;
      if (S.phase === 'reading') {
        /* One human at the keyboard has no seat to disambiguate, so there is no
           reason to make the hand leave the space bar for the number row. */
        if (soloHuman() && (ev.key === ' ' || ev.key === 'Enter' || ev.key === 'Spacebar')) {
          ev.preventDefault(); buzz(0); return;
        }
        var n = parseInt(ev.key, 10);
        if (n >= 1 && n <= S.players.length) { ev.preventDefault(); buzz(n - 1); }
        return;
      }
      if (S.phase === 'answering') {
        /* A–D and 1–4 are the keyboard's version of the four buttons, so they
           die where those buttons are disabled. Without this the letters keep
           working on a robot's turn — and since `answer` credits whoever holds
           the floor, a keystroke meant for the person at the machine is filed
           against the robot's name. */
        if (answersItself(S.buzzed)) return;
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

    /* Screens with no cursor of their own — the title card, the lobby, the green
       room, the results — hand the arrows to whatever controls they are showing.
       This runs last, so it never steals an arrow from the board or the clue. */
    if (!typing && walkFocus(ev, document.querySelector('.screen.is-active'))) return;

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
    /* The front door's two steps in one ring: the language pills, then a door per
       show. A pad walks straight down it, which is the order the screen reads in.
       The COMING SOON circles are `<div>`s, not disabled buttons, so they are not
       matched and never take focus — no special case needed for them. */
    front: '.menu-inline .pill, .chooser button:not([disabled])',
    /* Only the way in. `#splash-back` is a ghost button and stays off the ring,
       because B is the way back and should be the only way back. */
    splash: '.menu-inline .pill',
    lobby: '.menu .pill',
    setup: '#player-count button, #opponents button, #difficulty button, ' +
           '#answer-mode button, #sound-toggle button, .menu .pill',
    results: '.menu .pill'
  };
  /* Every overlay a pad may walk, and the only ones it can dismiss. A panel
     missing from here is invisible to the controller: `openOverlay()` never sees
     it, so A-presses leak through to the screen underneath and B closes nothing. */
  var OVERLAYS = ['match-menu', 'settings-panel', 'howto-panel',
                  'editions-panel', 'reading-panel'];

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

  /* The board belongs to the chooser's controller, the same way the answering
     floor belongs to whoever holds it. Same escape hatch too: a chooser with no
     pad plugged in must not strand a one-controller couch. */
  function padMayPick(padIndex) {
    if (!chooserLive()) return true;
    if (playerOf(padIndex) === S.chooser) return true;
    return !holderHasPad(S.chooser);
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
    if (answersItself(S.buzzed)) return;
    var ring = answerRing();
    if (!ring.length) return;
    optionFocus = Math.min(optionFocus, ring.length - 1);
    if (S.mode === 'final') submitFinalAnswer(optionFocus);
    else answer(optionFocus);
  }

  function onDir(padIndex, dir) {
    var back = (dir === 'left' || dir === 'up') ? -1 : 1;
    if (S.screen === 'board') {
      if (!padMayPick(padIndex)) { denyPick(playerOf(padIndex)); return; }
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
      if (!padMayPick(padIndex)) { denyPick(playerOf(padIndex)); return; }
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
      /* A robot or a remote guest answers for itself — no controller at this
         table can stand in for it, because `answer` files the result against
         whoever holds the floor. */
      if (answersItself(who2)) return;
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

    /* The front door and the title card are both ordinary rings — language pills
       and doors on one, the single way in on the other — so they fall through to
       the shared line below. */
    var ring2 = ringFor(S.screen);
    if (ring2.length) ring2[focus[S.screen] || 0].click();
  }

  function onBack() {
    var ov = openOverlay();
    if (ov) { ov.hidden = true; Sound.sfx('select', 0.4); return; }
    if (S.screen === 'setup') { el('setup-back').click(); return; }
    /* B is the only way back off the title card, which is why the button it
       stands in for is absent from `RINGS.splash`. */
    if (S.screen === 'splash') { el('splash-back').click(); return; }
    if (S.screen === 'board' || S.screen === 'clue' || S.screen === 'wager') { openMenu(); return; }
    if (S.screen === 'results') { el('play-again').click(); return; }
  }

  function onMenuButton() {
    if (S.screen === 'board' || S.screen === 'clue' || S.screen === 'wager') {
      if (el('match-menu').hidden) openMenu(); else closeMenu();
    }
  }

  /* The Android shell's back gesture. A phone has no Escape key, so this is the
     one control every player already has and it used to be the one control that
     killed the show: with no handler in `MainActivity`, the system finished the
     activity and a match in progress went with it. The shell asks the page first
     and quits only when the page declines — the page decides, because the page is
     the only thing that knows whether a menu should open or a screen should step
     back. The walk below is deliberately the Escape key's walk, for the same
     reason: on a phone, this gesture *is* Escape. `true` means the press was
     taken; `false` means the front door is behind you and the app may go. */
  window.JeopardyBack = function () {
    var menu = el('match-menu');
    if (menu && !menu.hidden) { closeMenu(); return true; }

    var overlay = document.querySelector('.overlay:not([hidden])');
    if (overlay) {
      /* Press the panel's own close button where it has one, so the sound and
         whatever the button tears down happen here too. */
      var shut = overlay.querySelector('[data-close]');
      if (shut) { shut.click(); return true; }
      overlay.hidden = true;
      return true;
    }

    if (S.screen === 'setup')  { el('setup-back').click(); return true; }
    if (S.screen === 'splash') { el('splash-back').click(); return true; }
    if (S.screen === 'board' || S.screen === 'clue' || S.screen === 'wager') {
      openMenu();
      return true;
    }
    /* The lobby and the results are both one step from the top of the show, and
       `quit-game` is that step on either: it is the button that goes back to the
       front door, not one that belongs to the lobby's own layout. */
    if (S.screen === 'lobby' || S.screen === 'results') { el('quit-game').click(); return true; }

    /* The front door itself. Nothing is behind it, so the press is Android's. */
    return false;
  };

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

  /* ── Rumble ──────────────────────────────────────────────── */

  /* The pad in a player's hand is a device the show can feel with, the same way
     a phone is, and it gets the same four words. It gets them in a different
     shape, though: a phone can only tap, so the phone's vocabulary is a rhythm,
     while a pad will hold a level for as long as it is told to — so a word here
     is a train of pulses. [strong, weak, milliseconds]. */
  var RUMBLE = {
    take: [[0.9, 0.55, 150]],
    beat: [[0.35, 0.15, 60]],
    foul: [[1, 0.7, 45], [1, 0.7, 45], [1, 0.7, 45]],
    tap: [[0.25, 0.12, 20]]
  };
  var PULSE_GAP = 55;   // the silence inside a train

  /* The Gamepad API spells rumble two ways and neither is universal: the
     standard, which is what Chrome and Edge implement, calls it
     `vibrationActuator`; Firefox calls it `hapticActuators`; Safari has neither
     on any platform, so a pad on a Mac in Safari is simply silent. Nothing in
     here may throw, and nothing may leave a rejected promise behind — a
     controller that cannot be felt must not be able to take the buzz down with
     it, and must not put an error in the console either. */
  function pulse(pad, spec) {
    var actuator = pad.vibrationActuator;
    if (actuator && actuator.playEffect) {
      try {
        var it = actuator.playEffect('dual-rumble', {
          duration: spec[2], startDelay: 0,
          strongMagnitude: spec[0], weakMagnitude: spec[1]
        });
        if (it && it.catch) it.catch(function () {});
      } catch (e) {}
      return;
    }
    var list = pad.hapticActuators;
    if (list && list.length && list[0].pulse) {
      try {
        var fired = list[0].pulse(spec[0], spec[2]);
        if (fired && fired.catch) fired.catch(function () {});
      } catch (e) {}
    }
  }

  /* One pulse at a time. The standard actuator plays a single effect per call,
     so a train is something the show schedules over a few frames rather than
     something it hands over whole. */
  function train(pad, specs, i) {
    if (i >= specs.length) return;
    pulse(pad, specs[i]);
    if (i + 1 < specs.length) {
      setTimeout(function () { train(pad, specs, i + 1); }, specs[i][2] + PULSE_GAP);
    }
  }

  function shake(test, word) {
    var specs = RUMBLE[word];
    if (!specs) return;
    /* Same snapshot the poll loop reads, so a pad cannot be felt and stepped in
       the same frame off two different pictures of the room. */
    var list = navigator.getGamepads ? navigator.getGamepads() : [];
    var order = connected();
    for (var i = 0; i < order.length; i++) {
      /* A seat with no pad plugged into it is unreachable rather than broken.
         Most of the show is one screen and no controllers at all. */
      if (!test(playerOf(order[i]))) continue;
      train(list[order[i]], specs, 0);
    }
  }

  /* The pad belonging to one contestant. */
  function feel(who, word) {
    if (who == null) return;
    shake(function (player) { return player === who; }, word);
  }

  /* Every pad at the table but one seat's — "somebody else got there first".
     An `except` of -1 excludes nobody, which is how a robot's buzz reaches a
     room that has no seat to leave out. */
  function feelOthers(except, word) {
    shake(function (player) { return player !== except; }, word);
  }

  return {
    init: init,
    syncOptions: syncOptions,
    count: function () { return connected().length; },
    feel: feel,
    feelOthers: feelOthers
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
  /* The bands are measured against a person, not against each other. A
     contestant who has read the clue waits for the lamp and then moves: half a
     second if the answer is already there, a little over one if it has to be
     assembled. So `quick` has to open near half a second and `late` has to close
     inside about two and a half, or the room spends the lamp watching a robot
     think and the buzzer stops being a race. The old bands opened `late` at two
     and a quarter seconds and ran it to six, which meant the common case was
     four seconds of nothing — a robot that had already lost, being waited on. */
  /* `accuracy` is how often ONE seat actually knows the clue, so what the room
     sees is the union over the seats — three normal robots at 0.43 between them
     answer about 0.74 of what they ring in on. These figures are solved, not
     assumed. The room should SHOW roughly easy 0.56, normal 0.71, hard 0.83,
     brutal 0.90 across the whole board, and the cube-root complement
     1-(1-shown)^(1/3) is the right shape for that — but it lands a little low,
     because a fishing thumb in the part of the two bands that overlaps can
     still take a clue off a slow sure one. Hence 0.27 / 0.43 / 0.54 / 0.63
     against a cube root of 0.26 / 0.36 / 0.46 / 0.53. Do not lift these to the
     shown rate. They were once the shown rate, and they looked right only
     because the verdict was drawn a second time here and again in `decide` — a
     fast thumb answered at the flat figure whatever it had claimed. Now that
     the thumb and the answer are one draw, the flat figure would be the room's
     floor and not its average: three robots at 0.75 would take nearly every
     clue off you. The rung multiplier below reaches -0.16, and better than half
     the archive is SCHOLAR or INSUFFERABLE, which is why the shown rates sit
     under the nominal four. */
  var BRAINS = {
    easy:   { quick: [900, 1900], late: [1400, 3400], nerve: 0.34,
              alert: 0.78, accuracy: 0.27, wager: [0.05, 0.20], think: [1400, 3000] },
    normal: { quick: [620, 1350], late: [1000, 2400], nerve: 0.58,
              alert: 0.92, accuracy: 0.43, wager: [0.10, 0.35], think: [1000, 2200] },
    hard:   { quick: [470, 1000], late: [780, 1800], nerve: 0.74,
              alert: 0.97, accuracy: 0.54, wager: [0.20, 0.55], think: [700, 1600] },
    brutal: { quick: [340, 760],  late: [560, 1350], nerve: 0.88,
              alert: 1.00, accuracy: 0.63, wager: [0.35, 0.85], think: [400, 1100] }
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

  /* Which joke a seat wears. An index into the string table is a character and
     not a seat, and the two tables carry the same characters in the same order,
     so drawing indices rather than strings is what keeps a seat's name in
     whatever language it was drawn under. The draw happens once per green room
     — a name that reshuffled on every redraw of the lobby would flicker under
     the player while they are still choosing a difficulty. */
  var NAME_COUNT = (function () {
    var en = (window.I18N && window.I18N.en) || {};
    var n = 0;
    for (var k in en) if (/^bot\.name\.\d+$/.test(k)) n++;
    return n;
  })();
  var roster = [];

  function redraw() {
    var pool = [];
    for (var i = 1; i <= NAME_COUNT; i++) pool.push(i);
    /* Fisher–Yates over the whole pool rather than a sample off it, so no seat
       can land on another's joke: three robots should never share one name. */
    for (var j = pool.length - 1; j > 0; j--) {
      var k = Math.floor(Math.random() * (j + 1));
      var t = pool[j]; pool[j] = pool[k]; pool[k] = t;
    }
    roster = pool;
  }

  /* The key, not the string, because the reader resolves it against the
     language on screen at that moment. The `idx + 1` is a floor, not a
     fallback: an empty pool means a build whose table lost its roster, and a
     seat still has to be called something. */
  function nameKey(idx) {
    if (!roster.length) redraw();
    return 'bot.name.' + (roster[idx] || idx + 1);
  }

  function brain(idx) {
    var p = S.players[idx];
    return BRAINS[(p && p.brain) || 'normal'] || BRAINS.normal;
  }

  function accuracy(b, clue) {
    var n = (clue && NUDGE[clue.difficulty]) || 0;
    return Math.max(0.05, Math.min(0.97, b.accuracy + n));
  }

  /* What each robot knows about the clue in front of it, drawn once and held for
     the whole clue. The thumb and the answer are the same claim — a robot that
     rings in early is telling the room it knows — so they have to come from one
     draw. They used to be drawn separately, which made every fast thumb a bluff
     the robot then had to live down: it slammed the buzzer and said something
     wrong. Held by clue id, so a steal does not re-roll a verdict the room has
     already watched fail. */
  var known = null;

  function knows(seat, clue) {
    var id = clue && clue.id;
    if (!id) return Math.random() < accuracy(brain(seat), clue);
    if (!known || known.id !== id) known = { id: id, by: {} };
    if (known.by[seat] == null) {
      known.by[seat] = Math.random() < accuracy(brain(seat), clue);
    }
    return known.by[seat];
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
  var DEAD_WINDOW = 1200;  // long enough to see the lamp go live, short enough to be a beat

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
    /* The floor of what the window actually gives them — a steal's leftover is
       shorter than the round's full length. A thumb past this is not a late
       press, it is a press after the window shut, and the room has moved on. */
    var ceiling = buzzWindowSeconds() * 1000 - 250;
    var calls = [];

    S.players.forEach(function (p, i) {
      if (!isBot(i)) return;
      if (S.lockedOut.indexOf(i) !== -1) return;
      var b = brain(i);
      var sure = knows(i, S.clue);
      /* A robot that does not know it still reaches in, in proportion to its
         nerve — but only into the fishing band, so an early press means what it
         is supposed to mean. */
      if (Math.random() > b.alert * (sure ? 1 : b.nerve)) return;
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

    var live = 0;
    calls.forEach(function (c) {
      var at = Math.max(THUMB_FLOOR, c.at);
      /* Someone else may already have rung in. A press past the window is not a
         steal: the race is over and the room has moved on. */
      if (at > ceiling) return;
      live++;
      later(function () {
        if (S.phase !== 'reading' || !S.armed) return;
        if (S.lockedOut.indexOf(c.seat) !== -1) return;
        buzz(c.seat);
      }, at);
    });

    /* Empty room. Every robot that declined its nerve check is a robot that is
       not pressing, so with no scheduled press left — and no human or guest seat
       still open to take the floor by hand — the window is dead air. Waiting it
       out makes the room sit through twenty seconds of nothing to learn what the
       board could have told it at once. Reveal on a beat instead; the timer is
       cleared with every other pending one by the module's own cancel(). */
    var open = false;
    for (var h = 0; h < S.players.length; h++) {
      if (!isBot(h) && S.lockedOut.indexOf(h) === -1) { open = true; break; }
    }
    if (!live && !open) {
      later(function () {
        if (S.phase !== 'reading' || !S.armed) return;
        expireBuzz();
      }, DEAD_WINDOW);
    }
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
    /* The same verdict that moved the thumb. A robot that rang in early has
       already told the room it knows; re-rolling here made that a bluff. */
    var hit = knows(idx, clue);
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
    redraw: redraw, nameKey: nameKey,
    armBuzzers: armBuzzers, onFloor: onFloor, autoWager: autoWager
  };
})();

// ── The online table ───────────────────────────────────────

/* One device runs the show and everybody else holds a phone. The host plays its
   own game exactly as it always did; the only difference is that some of the
   seats are not thumbs in this room.

   The wire carries one thing: a picture of the whole state, sent after every
   change. There are no deltas to get out of step with and no sequence numbers,
   because the last picture to arrive is the truth and it came from the machine
   that owns the board. Nothing below runs unless somebody went to the online
   table — the offline game asks none of these questions. */

/* A phone on a mobile network changes towers, loses the tunnel for four seconds,
   and comes back with a new identity as far as PeerJS is concerned. None of that
   is the player's fault, and none of it should cost them their seat or their
   score — so both ends work to put the same person back in the same chair. */
var REJOIN_TRY_MS = 2000;      /* how long a dropped guest waits between knocks */
var REJOIN_TRIES = 20;         /* …and how many knocks before it gives up: ~40s */
var REJOIN_GRACE_MS = 45000;   /* how long the host holds a seat for an absent guest */
var SILENT_MS = 10000;         /* no word from the host for this long means the wire is dead */
var BEAT_MS = 2000;            /* how often the host says it is still there */

var Online = {
  role: null,      /* 'host' | 'guest' | null */
  code: null,
  order: [],       /* the guests, in seat order */
  me: -1,          /* my seat, guest side */
  snap: null,      /* the last picture the host sent */
  shown: -1,       /* the second currently painted on a guest's dial */
  key: null,       /* which clock window that dial belongs to */
  tick: null,      /* the guest's repaint interval */
  wager: null,     /* host side: the wager waiting on somebody else's thumb */
  draft: '',       /* guest side: what is typed but not yet locked */
  bet: 0,
  cooled: false,
  name: '',        /* guest side: what to call me when I come back */
  cid: '',         /* guest side: who I am, so the host can hand me my chair */
  tries: 0,        /* guest side: how many times this knock has been repeated */
  retry: null,     /* guest side: the pending knock */
  dropped: false,  /* guest side: the wire is down and we are trying to get it back */
  rejoining: false,/* guest side: a chain of knocks is running, each booking the next */
  heard: 0,        /* guest side: when the host last said anything at all */
  beat: null       /* host side: the "still here" pulse */
};

/* The offline game gets a non-null `S.online` whose role is null, so every
   read site can go straight at it without a guard. */
S.online = Online;

function onlineGuest(seat) {
  for (var i = 0; i < Online.order.length; i++) {
    if (Online.order[i].seat === seat) return Online.order[i];
  }
  return null;
}

function guestByPeer(peerId) {
  for (var i = 0; i < Online.order.length; i++) {
    if (Online.order[i].peerId === peerId) return Online.order[i];
  }
  return null;
}

/* Seat 0 is the host and always will be; the guests take what is left, lowest
   first, so a seat freed by somebody leaving is the next one filled. The cap is
   the table, not the palette — see PLAYER_SEATS. */
function freeSeat() {
  for (var seat = 1; seat < PLAYER_SEATS; seat++) {
    if (!onlineGuest(seat)) return seat;
  }
  return -1;
}

function onlineName(seat) {
  return T('setup.playerDefault', { n: num(seat + 1) });
}

/* One table speaks one language. The host's page is the one that reads the
   room, so the host resolves the phone's copy and ships it resolved. Calling
   setLang on the guest would be worse than useless: it persists, and it would
   rewrite the language of the guest's own game while it sat at somebody
   else's table. */
function remoteLabels() {
  return {
    eyes: T('remote.eyes'),
    pick: T('remote.pick'),
    reading: T('remote.reading'),
    live: T('remote.live'),
    buzz: T('remote.buzz'),
    yours: T('remote.yours'),
    sitting: T('remote.sitting'),
    wager: T('remote.wager'),
    lockWager: T('remote.lockWager'),
    typeAnswer: T('remote.typeAnswer'),
    lockIn: T('remote.lockIn'),
    nobody: T('remote.nobody'),
    byName: T('remote.theirs'),
    pickYours: T('remote.pickYours'),
    pickBy: T('remote.pickBy'),
    waitLock: T('online.waitLock'),
    waitingHost: T('online.waitingHost')
  };
}

function onlineRoster() {
  var out = [];
  for (var i = 0; i < Online.order.length; i++) {
    var g = Online.order[i];
    out.push({
      name: g.name, seat: g.seat, gone: !!g.gone,
      color: PLAYER_COLORS[g.seat]
    });
  }
  return out;
}

/* What is left of the running clock, and which window it is. The total and the
   label are resolved here because the guest has no board to read them off. */
function onlineClock() {
  if (S.boardTimer) {
    return { left: S.boardRemaining, total: BOARD_SECONDS, label: T('clock.pick'), urgent: 5 };
  }
  if (S.finalTimer) {
    return { left: S.finalRemaining, total: FINAL_SECONDS, label: T('clock.answer'), urgent: 10 };
  }
  if (S.clueTimer) {
    var armed = S.phase === 'reading' && S.armed;
    if (S.phase === 'answering') {
      return { left: S.clueRemaining, total: ANSWER_SECONDS, label: T('clock.answer'), urgent: 5 };
    }
    if (armed) {
      return { left: S.clueRemaining, total: buzzWindowSeconds(), label: T('clock.buzz'), urgent: 5 };
    }
    return { left: S.clueRemaining, total: READ_SECONDS, label: T('clock.read'), urgent: 3 };
  }
  return null;
}

function onlineResults() {
  var ranked = S.players.slice().sort(function (a, b) { return b.score - a.score; });
  var top = ranked[0];
  var tie = ranked.length > 1 && ranked[1].score === top.score;
  return {
    tie: tie,
    title: tie ? T('results.tie') : T('results.winner', { name: top.name }),
    rows: ranked.map(function (p, i) {
      return { name: p.name, score: fmt(p.score), rank: i + 1,
               color: p.color, winner: i === 0 && !tie };
    })
  };
}

/* Everything a phone needs to draw the show, and nothing that would give a
   clue away early: the correct option and the answer text stay on the host
   until the clue is resolved, which is what leaves a steal something to
   steal. */
function onlineSnapshot() {
  var out = {
    lang: window.getLang(),
    screen: S.screen,
    phase: S.phase,
    mode: S.mode,
    round: S.round,
    started: S.players.length > 0,
    armed: !!S.armed,
    buzzed: S.buzzed == null ? null : S.buzzed,
    holder: S.holder == null ? null : S.holder,
    lockedOut: S.lockedOut.slice(),
    premature: Object.keys(S.prematureUntil).filter(function (k) {
      return S.prematureUntil[k] > Date.now();
    }).map(Number),
    writing: S.answerMode === 'write',
    players: S.players.map(function (p) {
      return { name: p.name, score: fmt(p.score), color: p.color };
    }),
    roster: onlineRoster(),
    clock: onlineClock(),
    verdict: S.onlineVerdict || null,
    labels: remoteLabels()
  };
  out.clockKey = out.clock ? out.clock.label + '|' + out.clock.total : null;

  /* The board is one seat's to open, and a chooser holding a phone needs the
     board itself to open it with: the categories, and what is still in them.
     The clues do not travel — a chooser picking a cell is not entitled to read
     it. Sent only while the board is up, so a picture during a clue stays the
     size it was. */
  if (S.screen === 'board' && S.board.length) {
    out.chooser = chooserLive() ? S.chooser : null;
    out.board = S.board.map(function (col) {
      return {
        category: col.category,
        cells: col.cells.map(function (cell) {
          return cell.solved ? null : fmtT(cell.value);
        })
      };
    });
  }

  if (S.screen === 'clue' && S.clue) {
    out.category = S.clue.category;
    out.value = fmtT(S.clue.value);
    out.text = S.clue.clue;
    out.options = S.clue.displayOptions ? S.clue.displayOptions.slice() :
      (S.clue.options ? S.clue.options.slice() : null);
    /* `resolved` is the only phase at which the answer is already public — the
       steal retry puts the clue back to `reading` and takes it away again. */
    out.correct = S.phase === 'resolved' ? S.clue.correct : null;
  }
  if (S.screen === 'wager' && S.clue) {
    out.category = S.clue.category;
    out.value = fmtT(S.clue.value);
  }
  if (S.screen === 'results') out.results = onlineResults();
  /* An empty table still needs a picture, or the wait screen has nothing to
     draw and the guest is left staring at a spinner. */
  out.waiting = !out.started;
  return out;
}

/* A burst of state changes in one task is one picture, not five. The verdict
   is safe under this because the host's way out of it is always a later task:
   the steal beat's timer, or the button when a hand gets there first. */
var onlineQueued = false;

function onlineSync() {
  if (Online.role !== 'host') return;
  if (onlineQueued) return;
  onlineQueued = true;
  setTimeout(function () {
    onlineQueued = false;
    onlinePush();
  }, 0);
}

function onlinePush() {
  if (Online.role !== 'host') return;
  var ids = Net.peers();
  if (!ids.length) return;
  var base = onlineSnapshot();
  for (var i = 0; i < ids.length; i++) {
    var guest = guestByPeer(ids[i]);
    if (!guest) continue;
    var msg = { t: 'state', seat: guest.seat, snap: base };
    /* A wager is one contestant's business, so it rides alone. */
    if (Online.wager && Online.wager.index === guest.seat) {
      msg.wager = {
        title: Online.wager.panel.title,
        category: Online.wager.panel.category,
        subtitle: Online.wager.panel.subtitle,
        amount: Online.wager.panel.amount,
        max: Online.wager.max,
        step: Online.wager.step
      };
    }
    Net.sendTo(ids[i], msg);
  }
}

/* ── What the host does with what a phone says ────────────── */

function hostMessage(peerId, msg) {
  if (!msg || !msg.t) return;
  var guest = guestByPeer(peerId);
  if (!guest) return;
  var seat = guest.seat;

  if (msg.t === 'buzz') {
    /* No policing here. Whether the lamp is up, whether this thumb is already
       in the sin bin, whether the seat is locked out — the engine's own `buzz`
       already rules on all of it, and it rules identically for a thumb in the
       room. */
    buzz(seat);
    onlineSync();
    return;
  }

  if (msg.t === 'answer') {
    var onTheFloor = S.mode === 'final' ? S.holder === seat : S.buzzed === seat;
    if (!onTheFloor || S.phase !== 'answering') return;
    if (S.answerMode === 'mc' && Number.isInteger(msg.option) &&
        msg.option >= 0 && msg.option < S.clue.options.length) {
      if (S.mode === 'final') submitFinalAnswer(msg.option); else answer(msg.option);
    } else if (S.answerMode === 'write' && typeof msg.text === 'string') {
      if (S.mode === 'final') submitFinalWritten(msg.text); else answerWritten(msg.text);
    } else {
      return;
    }
    onlineSync();
    return;
  }

  if (msg.t === 'pick') {
    /* A phone asks to open a cell, and the engine — not the phone — decides
       whether it may. The board belongs to the chooser, so a request from any
       other seat is dropped, and so is one for a cell that is already gone; a
       phone that has stopped being the chooser mid-tap must not be able to open
       somebody else's board. */
    if (S.screen !== 'board' || !chooserLive() || S.chooser !== seat) return;
    var col = Number(msg.col), row = Number(msg.row);
    if (!(col >= 0 && col < S.board.length)) return;
    if (!(row >= 0 && row < S.board[col].cells.length)) return;
    if (S.board[col].cells[row].solved) return;
    S.cursor = { col: col, row: row };
    openClue(col, row);
    onlineSync();
    return;
  }

  if (msg.t === 'wager') {
    if (!Online.wager || Online.wager.index !== seat) return;
    var hand = Online.wager;
    var amount = Number(msg.amount);
    if (!isFinite(amount)) return;
    amount = Math.max(0, Math.min(hand.max, Math.round(amount / hand.step) * hand.step));
    Online.wager = null;
    /* `onLock` is whatever the host's own lock button would have fired. */
    hand.lock(amount);
    onlineSync();
  }
}

function onlineArrived(peerId, meta) {
  var guest = guestByPeer(peerId);
  if (guest) { guest.name = (meta.name || '').trim() || guest.name; return; }

  /* Somebody knocking who has knocked before. A dropped wire gives them a new
     PeerJS id, so the id cannot be the identity — the ticket they carry can. */
  var cid = (meta.cid || '').trim();
  var back = null;
  if (cid) {
    for (var i = 0; i < Online.order.length; i++) {
      if (Online.order[i].cid === cid) { back = Online.order[i]; break; }
    }
  }
  if (back) {
    if (back.goneTimer) { clearTimeout(back.goneTimer); back.goneTimer = null; }
    back.peerId = peerId;
    back.gone = false;
    back.name = (meta.name || '').trim().slice(0, 14) || back.name;
    /* The match holds the same pairing, and the seat they are in is theirs. */
    if (S.players[back.seat]) S.players[back.seat].remote = peerId;
    renderOnlineRosters();
    onlineNote('online.back', { name: back.name });
    onlineSync();
    return;
  }

  var seat = freeSeat();
  if (seat === -1) { Net.sendTo(peerId, { t: 'bye', why: 'full' }); return; }
  var name = (meta.name || '').trim().slice(0, 14) || onlineName(seat);
  Online.order.push({
    peerId: peerId, name: name, seat: seat,
    cid: cid, gone: false, goneTimer: null
  });
  Online.order.sort(function (a, b) { return a.seat - b.seat; });
  renderOnlineRosters();
  onlineNote('online.seated', { name: name });
  onlineSync();
}

function onlineLeft(peerId) {
  var guest = guestByPeer(peerId);
  if (!guest) return;
  /* The chair is not given away the moment the wire drops. Nearly every drop on
     a phone is a tower handover or a few seconds behind a tunnel, and the player
     is back before the clue is over; free the seat now and they return a
     stranger with no score to a table that has already moved on. Hold it, and
     only let it go when nobody has come back for it. */
  guest.gone = true;
  if (guest.goneTimer) clearTimeout(guest.goneTimer);
  guest.goneTimer = setTimeout(function () {
    guest.goneTimer = null;
    Online.order = Online.order.filter(function (g) { return g !== guest; });
    renderOnlineRosters();
    onlineNote('online.left', { name: guest.name });
    onlineSync();
  }, REJOIN_GRACE_MS);
  renderOnlineRosters();
  onlineNote('online.dropped', { name: guest.name });
  onlineSync();
}

/* ── The lobby roster ─────────────────────────────────────── */

function renderOnlineRoster(id, rows, mineSeat) {
  var host = el(id);
  if (!host) return;
  host.innerHTML = '';
  if (!rows.length) {
    host.appendChild(make('li', 'online-seat is-empty', T('online.nobody')));
    return;
  }
  rows.forEach(function (r) {
    var li = make('li', 'online-seat'
      + (r.seat === mineSeat ? ' is-you' : '')
      + (r.gone ? ' is-gone' : ''));
    li.style.setProperty('--pc', r.color || PLAYER_COLORS[r.seat]);
    li.appendChild(make('span', 'online-seat-dot'));
    li.appendChild(make('span', 'online-seat-name', r.name));
    if (r.gone) li.appendChild(make('span', 'online-seat-gone', T('online.reconnecting')));
    host.appendChild(li);
  });
}

function renderOnlineRosters() {
  renderOnlineRoster('online-roster-host', onlineRoster(), 0);
  renderOnlineRoster('online-roster-guest', Online.order, Online.me);
}

function onlineNote(key, vars) {
  var node = el('online-note');
  if (!node) return;
  node.textContent = key ? T(key, vars) : '';
  node.hidden = !key;
}

/* ── What a phone draws ───────────────────────────────────── */

/* The body is rebuilt whenever the shape of the game changes — which is rare,
   a handful of times a clue — and never on a clock tick. Rebuilding it once a
   second would take the caret out of the answer box on the second. */
function remoteShape(snap) {
  if (!snap) return 'wait';
  if (snap.waiting) return 'wait';
  if (snap.screen === 'results') return 'results';
  if (snap.verdict && snap.phase === 'resolved') return 'verdict';
  if (snap.screen === 'wager') return 'wager';
  if (snap.screen !== 'clue') {
    /* The board is one seat's to open, and this phone is that seat. It gets the
       board itself to choose from; every other phone, including the host's own
       guests at a robot's table, is watching somebody else do it. */
    if (snap.screen === 'board' && snap.board && snap.chooser === Number(Online.me)) {
      return 'picking';
    }
    return 'board';
  }
  /* Out of this clue is its own shape, not a detail inside `answering`: the
     panel is rebuilt on shape, so a locked-out seat would otherwise keep the
     dead grid on screen for as long as the others are still stealing. */
  if (snap.phase === 'answering') {
    return snap.lockedOut.indexOf(Number(Online.me)) !== -1 ? 'sitting' : 'answering';
  }
  if (snap.phase === 'reading') return snap.armed ? 'live' : 'reading';
  return 'board';
}

function remoteScoreStrip(snap) {
  var strip = make('div', 'remote-strip');
  snap.players.forEach(function (p) {
    var chip = make('span', 'remote-score');
    chip.style.setProperty('--pc', p.color);
    chip.appendChild(make('span', 'remote-score-name', p.name));
    chip.appendChild(make('span', 'remote-score-num', p.score));
    strip.appendChild(chip);
  });
  return strip;
}

function remoteStage(snap) {
  var stage = make('div', 'remote-stage');
  var label = snap.labels;
  var shape = remoteShape(snap);
  var me = Online.me;
  var mine = snap.mode === 'final' ? snap.holder === me : snap.buzzed === me;

  if (shape === 'wait') {
    stage.appendChild(make('p', 'remote-lead', label.waitingHost));
    return stage;
  }
  if (shape === 'results') {
    stage.appendChild(make('p', 'remote-lead', snap.results.title));
    var list = make('ol', 'remote-results');
    snap.results.rows.forEach(function (r) {
      var li = make('li', 'remote-result' + (r.winner ? ' is-winner' : ''));
      li.style.setProperty('--pc', r.color);
      li.appendChild(make('span', 'remote-result-rank', String(r.rank)));
      li.appendChild(make('span', 'remote-result-name', r.name));
      li.appendChild(make('span', 'remote-result-score', r.score));
      list.appendChild(li);
    });
    stage.appendChild(list);
    return stage;
  }
  if (shape === 'verdict') {
    var v = snap.verdict;
    var box = make('div', 'remote-verdict is-' + v.kind);
    if (v.seat === me) box.classList.add('is-mine');
    var head = make('p', 'remote-verdict-head', v.head || '');
    if (v.line) {
      head.appendChild(make('span', 'remote-verdict-line', ' ' + v.line));
    }
    box.appendChild(head);
    if (v.said) box.appendChild(make('p', 'remote-verdict-said', v.said));
    if (v.answer) box.appendChild(make('p', 'remote-verdict-answer', T('verdict.answer') + v.answer));
    if (v.explain) box.appendChild(make('p', 'remote-verdict-explain', v.explain));
    if (v.source) box.appendChild(make('p', 'remote-verdict-source', v.source));
    if (v.canRetry) box.appendChild(make('p', 'remote-hint', label.reading));
    stage.appendChild(box);
    return stage;
  }
  if (shape === 'wager') {
    var w = Online.wagerAsk;
    if (!w) {
      stage.appendChild(make('p', 'remote-lead', label.wager));
      stage.appendChild(make('p', 'remote-hint', label.waitLock));
      return stage;
    }
    stage.appendChild(make('p', 'remote-kicker', w.category));
    stage.appendChild(make('p', 'remote-lead', w.title));
    if (w.subtitle) stage.appendChild(make('p', 'remote-hint', w.subtitle));
    var amount = make('p', 'remote-amount', fmtT(Online.bet));
    stage.appendChild(amount);
    var range = document.createElement('input');
    range.type = 'range';
    range.className = 'wager-range remote-range';
    range.min = '0';
    range.max = String(w.max);
    range.step = String(w.step);
    range.value = String(Online.bet);
    range.addEventListener('input', function () {
      Online.bet = Number(range.value);
      amount.textContent = fmtT(Online.bet);
    });
    stage.appendChild(range);
    var lock = make('button', 'pill pill-primary remote-big', label.lockWager);
    lock.type = 'button';
    lock.addEventListener('click', function () {
      if (lock.disabled) return;
      lock.disabled = true;
      Sound.sfx('select');
      Net.emit({ t: 'wager', amount: Online.bet });
    });
    stage.appendChild(lock);
    return stage;
  }

  if (shape === 'picking') {
    /* The board, on the phone of the only seat allowed to touch it. A chooser
       chooses by amount, not by clue: the categories are the wide thing and the
       amounts are what the room reads off the wall, so this is the wall's own
       shape — a row per category, what is left in it, one tap to open it. A
       solved cell keeps its slot as a dash, because a row that changes length
       under a thumb is a row that gets mis-tapped. */
    stage.appendChild(make('p', 'remote-lead', label.pickYours));
    var wall = make('div', 'remote-board');
    snap.board.forEach(function (col, ci) {
      var row = make('div', 'remote-row');
      row.appendChild(make('span', 'remote-row-cat', col.category));
      var strip = make('div', 'remote-cells');
      col.cells.forEach(function (value, ri) {
        if (value == null) {
          strip.appendChild(make('span', 'remote-cell is-gone', '—'));
          return;
        }
        var cell = make('button', 'pill remote-cell', value);
        cell.type = 'button';
        cell.addEventListener('click', function () {
          if (cell.disabled) return;
          cell.disabled = true;
          Sound.sfx('select');
          Net.emit({ t: 'pick', col: ci, row: ri });
        });
        strip.appendChild(cell);
      });
      row.appendChild(strip);
      wall.appendChild(row);
    });
    stage.appendChild(wall);
    return stage;
  }

  /* From here down it is a clue, and the clue's own head is the same on every
     phone: category bar, amount, the text. */
  stage.appendChild(remoteClueHead(snap));

  if (shape === 'board') {
    /* Whose board it is, by name. "Waiting for somebody to pick a clue" is the
       truth and it is not worth anything: the room wants to know whether the
       board is theirs, and if it is not, whose it is. */
    var owner = snap.chooser != null ? snap.players[snap.chooser] : null;
    if (owner) {
      stage.appendChild(make('p', 'remote-lead', label.pickBy.replace('{name}', owner.name)));
      stage.appendChild(make('p', 'remote-hint', label.eyes));
      return stage;
    }
    stage.appendChild(make('p', 'remote-lead', label.eyes));
    stage.appendChild(make('p', 'remote-hint', label.pick));
    return stage;
  }
  if (shape === 'reading') {
    stage.appendChild(make('p', 'remote-lead', label.reading));
    return stage;
  }
  if (shape === 'live') {
    /* Locked out of this clue is not the same as having already answered it:
       the lamp is up for everybody still in it, and this seat is not in it. */
    if (snap.lockedOut.indexOf(me) !== -1) {
      stage.appendChild(make('p', 'remote-lead', label.sitting));
      return stage;
    }
    stage.appendChild(make('p', 'remote-lead', label.live));
    var cooled = snap.premature.indexOf(me) !== -1;
    var buzzBtn = make('button', 'buzz-btn remote-buzz' + (cooled ? ' is-early' : ''), label.buzz);
    buzzBtn.type = 'button';
    buzzBtn.disabled = cooled;
    buzzBtn.addEventListener('click', function () {
      if (buzzBtn.disabled) return;
      buzzBtn.disabled = true;
      /* The host rules on it, so the button does not: it shuts itself off and
         waits to be told whether that was a thumb or a foul. */
      Haptics.take();
      Sound.sfx('select', 0.7);
      Net.emit({ t: 'buzz' });
      setTimeout(function () { buzzBtn.disabled = false; }, 400);
    });
    stage.appendChild(buzzBtn);
    return stage;
  }

  if (shape === 'sitting') {
    stage.appendChild(make('p', 'remote-lead', label.sitting));
    return stage;
  }

  /* answering */
  if (!mine) {
    var holder = snap.mode === 'final' ? snap.holder : snap.buzzed;
    var who = snap.players[holder];
    var line = who ? label.byName.replace('{name}', who.name) : label.nobody;
    stage.appendChild(make('p', 'remote-lead', line));
    return stage;
  }
  stage.appendChild(make('p', 'remote-lead is-you', label.yours));

  if (snap.writing) {
    var field = document.createElement('input');
    field.type = 'text';
    field.className = 'write-input';
    field.id = 'remote-write';
    field.autocomplete = 'off';
    field.spellcheck = false;
    field.value = Online.draft;
    field.setAttribute('placeholder', label.typeAnswer);
    field.addEventListener('input', function () { Online.draft = field.value; });
    stage.appendChild(field);
    var send = make('button', 'pill pill-primary remote-big', label.lockIn);
    send.type = 'button';
    send.addEventListener('click', function () {
      var text = (field.value || '').trim();
      if (!text) { field.focus(); return; }
      Sound.sfx('select');
      Net.emit({ t: 'answer', text: text });
    });
    stage.appendChild(send);
    /* Only on the first build of this window, or a chatty repaint would steal
       the caret out of the box the contestant is typing in. */
    if (!Online.focused) {
      Online.focused = true;
      setTimeout(function () { field.focus(); }, 40);
    }
    return stage;
  }

  if (snap.options && snap.options.length) {
    var grid = make('div', 'options remote-options');
    snap.options.forEach(function (opt, i) {
      var btn = make('button', 'option', opt);
      btn.type = 'button';
      btn.addEventListener('click', function () {
        Sound.sfx('select');
        Net.emit({ t: 'answer', option: i });
      });
      grid.appendChild(btn);
    });
    stage.appendChild(grid);
  } else {
    var typed = document.createElement('input');
    typed.type = 'text';
    typed.className = 'write-input';
    typed.value = Online.draft;
    typed.setAttribute('placeholder', label.typeAnswer);
    typed.addEventListener('input', function () { Online.draft = typed.value; });
    stage.appendChild(typed);
    var lockIn = make('button', 'pill pill-primary remote-big', label.lockIn);
    lockIn.type = 'button';
    lockIn.addEventListener('click', function () {
      Net.emit({ t: 'answer', text: typed.value });
    });
    stage.appendChild(lockIn);
  }
  return stage;
}

function remoteClueHead(snap) {
  var head = make('div', 'remote-clue-head');
  head.appendChild(make('span', 'remote-cat', snap.category || ''));
  if (snap.value) head.appendChild(make('span', 'remote-value', snap.value));
  var text = make('p', 'remote-clue', snap.text || '');
  head.appendChild(text);
  return head;
}

function remoteRender() {
  var body = el('remote-body');
  if (!body) return;
  var snap = Online.snap;
  var shape = remoteShape(snap);

  /* Leaving a window ends its business: the draft goes back to empty, the bet
     goes back to the middle, and the caret is free to be taken again. */
  if (shape !== Online.shape) {
    Online.focused = false;
    if (shape !== 'answering') Online.draft = '';
    if (shape !== 'wager') { Online.bet = 0; Online.wagerAsk = null; }
    Online.shape = shape;
  }

  body.innerHTML = '';
  if (!snap) {
    /* A stale picture is worse than no picture: a dial that has stopped moving
       reads as "the host is waiting for you", which is exactly the wrong thing
       for a player whose phone has quietly lost the table. */
    body.appendChild(make('p', 'remote-lead' + (Online.dropped ? ' remote-dropped' : ''),
      Online.dropped ? T('online.reconnecting') : T('online.waiting')));
    return;
  }
  if (snap.players.length) body.appendChild(remoteScoreStrip(snap));

  var stage = remoteStage(snap);
  var clock = snap.clock;
  if (clock) {
    var dial = make('div', 'clock remote-clock');
    dial.id = 'remote-clock';
    stage.appendChild(dial);
  }
  body.appendChild(stage);

  if (clock) {
    Online.shown = -1;
    Online.key = null;
    remoteTick();
  }

  /* A thumb that was too early has to feel it, and the only way it finds out is
     the next picture. */
  var cooled = snap.premature.indexOf(Online.me) !== -1;
  if (cooled && !Online.cooled) { Haptics.foul(); Sound.sfx('incorrect', 0.4); }
  Online.cooled = cooled;
}

/* The dial is the one thing on this screen that moves without anybody touching
   anything, so it is the one thing redrawn on a timer. A phone whose own clock
   is wrong by an hour still counts down the right number of seconds: it was
   told what was left and when, and the difference is all it uses. */
function remoteTick() {
  var snap = Online.snap;
  var node = el('remote-clock');
  if (!snap || !snap.clock || !node) return;
  var c = snap.clock;
  if (c.key && Online.key !== c.key) { Online.key = c.key; Online.shown = -1; }
  var left = Math.max(0, Math.round(c.left - (performance.now() - c.at) / 1000));
  if (left === Online.shown) return;
  var first = Online.shown === -1;
  Online.shown = left;
  paintClock(node, left, c.total, c.label, c.urgent, first);
}

/* ── What a phone does with what the host says ────────────── */

function guestMessage(msg) {
  if (!msg || !msg.t) return;

  /* Anything at all from the host is proof the line is still up — a beat will
     do — and proof is what stands the knocking down. */
  Online.heard = Date.now();
  Online.rejoining = false;
  Online.tries = 0;
  if (Online.retry) { clearTimeout(Online.retry); Online.retry = null; }

  if (msg.t === 'beat') return;

  if (msg.t === 'bye') {
    /* The table said no, or the table is gone. Take the whole seat apart, not
       just the picture: a guest left holding the role is one the silence check
       would start knocking at that same shut door. */
    onlineLeave();
    show('online');
    onlineRejoinPrompt();
    onlineNote(msg.why === 'full' ? 'online.roomFull' : 'online.closed');
    return;
  }
  if (msg.t !== 'state') return;

  /* A picture means the knock was answered, whatever the wire said in between.
     Take the reconnecting line down with it — a guest who is back should not be
     left staring at a note that says they are not. */
  if (Online.dropped) { Online.dropped = false; onlineNote(null); }
  if (typeof msg.seat === 'number') Online.me = msg.seat;
  var snap = msg.snap;
  if (!snap || !Array.isArray(snap.players) || !Array.isArray(snap.roster)) return;
  if ((snap.lang === 'en' || snap.lang === 'fa') && snap.lang !== window.getLang()) {
    setLang(snap.lang);
  }
  var clock = snap.clock;
  if (clock) {
    /* The host's timestamp is meaningless here — the two machines do not share
       a clock. What it means is "this many seconds, as of now", and now is the
       moment the picture arrived. */
    clock.at = performance.now();
    clock.key = snap.clockKey || null;
  }
  Online.snap = snap;
  Online.wagerAsk = msg.wager || null;
  if (msg.wager && !Online.bet) Online.bet = msg.wager.amount;

  if (snap.started && S.screen !== 'remote') show('remote');
  if (S.screen === 'remote') remoteRender();
  renderOnlineRoster('online-roster-guest', snap.roster, Online.me);
}

/* ── The lobby ────────────────────────────────────────────── */

function onlineSupported() {
  return !!(window.Net && Net.supported());
}

/* The pills carry their label in a span of their own, so writing to the button
   would throw the chevron away with the text. */
function onlinePill(btn, key) {
  if (!btn) return;
  var slot = btn.querySelector('.pill-label') || btn;
  slot.textContent = T(key);
}

function onlineLeave() {
  /* The repaint interval is not torn down here even though this is the way
     out of a table: it is armed once at boot and every join goes through this
     function first, so clearing it left every guest who typed a code with a
     dial that froze between pictures. Its own guard — role and screen — makes
     it a no-op when there is nobody to draw for. */
  Online.snap = null;
  Online.order = [];
  Online.me = -1;
  Online.shape = null;
  Online.wager = null;
  Online.wagerAsk = null;
  Online.bet = 0;
  Online.draft = '';
  Online.role = null;
  Online.code = null;
  Online.dropped = false;
  Online.tries = 0;
  Online.rejoining = false;
  /* No silence clock until somebody has actually answered: a code typed wrong
     must not send a guest knocking at a room that was never there. */
  Online.heard = 0;
  if (Online.retry) { clearTimeout(Online.retry); Online.retry = null; }
  if (window.Net) Net.close();
}

/* Back to the form that asks for a code, with the button live again. The seat
   is gone, and the next thing this player does is try again or try another
   room — which is also where a failed first knock already leaves them. */
function onlineRejoinPrompt() {
  el('online-panel-join').hidden = false;
  el('online-panel-wait').hidden = true;
  var go = el('online-go');
  if (go) { go.disabled = false; onlinePill(go, 'online.connect'); }
}

/* Who this device is, as opposed to which wire it happens to be on. Minted
   once and kept, so that a player who loses the network and comes back through
   a different connection is the same person to the host's table. */
function onlineCid() {
  var id = '';
  try { id = localStorage.getItem('jpd-cid') || ''; } catch (err) { /* no storage */ }
  if (!id) {
    id = 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    try { localStorage.setItem('jpd-cid', id); } catch (err) { /* no storage */ }
  }
  return id;
}

/* Knock. Everything a guest needs to sit down and to sit back down is in these
   three fields, so a retry is the same call as the first attempt.

   A knock that fails does not always say so. A room that has gone answers with
   peer-unavailable, which arrives as an error and not as a close, and a wire
   that is merely quiet answers with nothing at all — so nothing here can be
   made to depend on the transport reporting its own death. While a guest is
   getting back in, the next knock is booked as this one goes out, and the first
   word from the host stands the chain down. A guest who never got in at all —
   a mistyped code — never enters a chain and is told the reason instead. */
function onlineKnock() {
  Online.retry = null;
  if (Online.role !== 'guest' || !Online.code) return;
  Online.tries += 1;
  Net.join(Online.code, Online.name, Online.cid);
  if (Online.rejoining && Online.tries < REJOIN_TRIES) {
    Online.retry = setTimeout(onlineKnock, REJOIN_TRY_MS);
  }
}

/* The wire went. Do not throw the player back to a form asking for a room code
   they cannot see — it is on somebody else's screen. Hold their place, say so
   on the glass, and keep knocking. */
function onlineDropped() {
  if (Online.role !== 'guest') return;
  Online.dropped = true;
  Online.rejoining = true;
  Online.snap = null;
  if (S.screen === 'remote') remoteRender();
  onlineNote('online.reconnecting');
  if (Online.tries >= REJOIN_TRIES) {
    /* Out of knocks. Stand the retry loop down for good — otherwise the next
       silence check would start the whole thing over on a phone that is plainly
       not getting back in. */
    Online.dropped = false;
    Online.rejoining = false;
    Online.heard = 0;
    Online.role = null;
    if (window.Net) Net.close();
    if (S.screen === 'remote') show('online');
    onlineRejoinPrompt();
    onlineNote('online.lost');
    return;
  }
  if (!Online.retry) Online.retry = setTimeout(onlineKnock, REJOIN_TRY_MS);
}

function onlineInviteLink() {
  var base = location.origin + location.pathname;
  var link = base + '?code=' + encodeURIComponent(Online.code || '');
  /* An invited guest should land on the skin their host is playing, not on
     whichever show they last opened. Only a build carrying a second edition can
     be ambiguous, so the public build's link is the string it always was. */
  if (window.getEditions().length > 1) link += '&ed=' + encodeURIComponent(window.getEdition());
  return link;
}

function initOnline() {
  var goBtn = el('go-online');
  if (goBtn) {
    goBtn.addEventListener('click', function () {
      Sound.sfx('select');
      onlineNote(null);
      el('online-choice').hidden = false;
      el('online-panel-host').hidden = true;
      el('online-panel-join').hidden = true;
      el('online-panel-wait').hidden = true;
      show('online');
      if (!onlineSupported()) onlineNote('online.noWebrtc');
    });
  }

  var hostBtn = el('online-host');
  if (hostBtn) {
    hostBtn.addEventListener('click', function () {
      if (!onlineSupported()) { onlineNote('online.noWebrtc'); return; }
      Sound.sfx('select');
      onlineLeave();
      Online.role = 'host';
      Online.code = Net.code();
      el('online-choice').hidden = true;
      el('online-panel-join').hidden = true;
      el('online-panel-wait').hidden = true;
      el('online-panel-host').hidden = false;
      el('online-code').textContent = Online.code;
      el('online-link').textContent = onlineInviteLink();
      onlineNote(null);
      renderOnlineRosters();

      Net.on('ready', function () {
        Online.code = Net.state.code;
        el('online-code').textContent = Online.code || '';
        el('online-link').textContent = onlineInviteLink();
        onlineNote(null);
      });
      Net.on('join', function (peerId, meta) {
        if (Online.role === 'host') onlineArrived(peerId, meta || {});
      });
      Net.on('leave', function (peerId) {
        if (Online.role === 'host') onlineLeft(peerId);
      });
      Net.host(Online.code);
    });
  }

  var joinBtn = el('online-join');
  if (joinBtn) {
    joinBtn.addEventListener('click', function () {
      if (!onlineSupported()) { onlineNote('online.noWebrtc'); return; }
      Sound.sfx('select');
      el('online-choice').hidden = true;
      el('online-panel-host').hidden = true;
      el('online-panel-wait').hidden = true;
      el('online-panel-join').hidden = false;
      onlineNote(null);
      var name = el('online-name');
      if (name) name.focus();
    });
  }

  var form = el('online-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var name = (el('online-name').value || '').trim().slice(0, 14);
      var code = (el('online-code-input').value || '').trim().toUpperCase();
      if (!code) { el('online-code-input').focus(); return; }
      onlineLeave();
      Online.role = 'guest';
      Online.code = code;
      Online.name = name;
      Online.cid = onlineCid();
      var go = el('online-go');
      if (go) { go.disabled = true; onlinePill(go, 'online.connecting'); }
      el('online-panel-join').hidden = true;
      el('online-panel-wait').hidden = false;
      renderOnlineRoster('online-roster-guest', [], -1);

      Net.on('connected', function () {
        if (Online.role !== 'guest') return;
        Online.dropped = false;
        Online.rejoining = false;
        Online.tries = 0;
        Online.heard = Date.now();
        if (Online.retry) { clearTimeout(Online.retry); Online.retry = null; }
        if (go) { go.disabled = false; onlinePill(go, 'online.connect'); }
        if (!Online.snap) onlineNote(null);
      });
      /* A drop is not the end of the table. Only a closed door is. */
      Net.on('closed', function () { onlineDropped(); });
      onlineKnock();
    });
  }

  var copy = el('online-copy');
  if (copy) {
    copy.addEventListener('click', function () {
      var link = onlineInviteLink();
      var slot = copy.querySelector('.pill-label') || copy;
      var done = function () {
        slot.textContent = T('online.copied');
        setTimeout(function () { slot.textContent = T('online.copyLink'); }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(link).then(done, function () { onlineNote(null); });
      } else {
        /* A clipboard API is not universal and the link is on screen anyway. */
        var tmp = document.createElement('textarea');
        tmp.value = link;
        document.body.appendChild(tmp);
        tmp.select();
        try { document.execCommand('copy'); done(); } catch (err) { /* read it out loud */ }
        tmp.remove();
      }
    });
  }

  var setupBtn = el('online-setup');
  if (setupBtn) {
    setupBtn.addEventListener('click', function () {
      if (Online.role !== 'host') return;
      Sound.sfx('select');
      startMatch();
    });
  }

  var back = el('online-back');
  if (back) {
    back.addEventListener('click', function () {
      Sound.sfx('select');
      onlineLeave();
      show('lobby');
    });
  }

  /* The host's own name is seat 0's name — the setup screen is skipped at an
     online table, so this is the only place to type it. */
  var hostName = el('online-host-name');
  if (hostName) {
    hostName.addEventListener('input', function () {
      S.names[0] = hostName.value;
    });
  }

  /* One handler for both ends of the wire: the host's messages carry the
     sender's id and the guest's do not, so the role decides which way round
     the two arguments go. */
  Net.on('message', function (a, b) {
    if (Online.role === 'guest') guestMessage(a);
    else if (Online.role === 'host') hostMessage(a, b);
  });

  Net.on('error', function (line) {
    /* An error while the game is running is the wire's problem, not the
       player's, and they are holding a controller in the middle of a clue.
       Only rearrange the lobby under them. */
    if (Online.role === 'guest' && S.screen === 'online') onlineRejoinPrompt();
    onlineNote(null);
    var note = el('online-note');
    if (note) { note.textContent = line; note.hidden = false; }
  });

  /* The guest's dial runs on a timer, but only while it is the guest. The same
     beat is where a guest notices that the host has gone quiet: a wire can die
     without either end being told, and a frozen picture is the one failure the
     player cannot tell from their own mistake. */
  Online.tick = setInterval(function () {
    if (Online.role !== 'guest') return;
    if (S.screen === 'remote') remoteTick();
    /* Silence is the only signal a dead wire reliably gives, and it is read
       here only while no knock is in flight: a booked knock is a retry already
       under way, and its own chain either lands or runs out of tries. */
    if (!Online.retry && Online.heard && Date.now() - Online.heard > SILENT_MS) {
      onlineDropped();
    }
  }, 200);

  /* And the host says so, out loud, twice a second. It costs nothing — the
     message has no payload — and it is the only way a guest can tell a quiet
     moment from a dead line. */
  Online.beat = setInterval(function () {
    if (Online.role !== 'host') return;
    if (!window.Net || !Net.peers().length) return;
    Net.send({ t: 'beat' });
  }, BEAT_MS);

  /* Somebody followed a link. Put the code in the box and open the door. */
  var m = /[?&]code=([A-Za-z0-9]{1,8})/.exec(location.search || '');
  if (m) {
    el('online-code-input').value = m[1].toUpperCase();
    el('online-choice').hidden = true;
    el('online-panel-host').hidden = true;
    el('online-panel-join').hidden = false;
    show('online');
    if (!onlineSupported()) onlineNote('online.noWebrtc');
  }
}

/* ── The keyboard ────────────────────────────────────────────
   Nothing here scrolls. `html`, `body` and every screen carry `overflow: hidden`
   and the document is sized to the viewport to the pixel, so when iOS raises the
   keyboard over a focused field there is no scrollable ancestor for WebKit to
   pan. Its usual repair — scroll the field into view — has nothing to grab, and
   the box the contestant is typing into ends up under the keyboard.

   So the layout moves instead. `visualViewport` reports the part of the page the
   keyboard has not covered; the difference is published as `--kb`, and the active
   screen reserves that much at its bottom in place of the host band. The clue
   body is the flex child that gives, and the field stays above the keyboard.

   A desktop browser has no keyboard to report, leaves the difference at zero, and
   the rule collapses to the band it was always reserving. */
function watchKeyboard() {
  var vv = window.visualViewport;
  if (!vv) return;

  var last = -1;
  var apply = function () {
    var kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop));
    if (kb === last) return;
    last = kb;
    document.documentElement.style.setProperty('--kb', kb + 'px');
  };

  vv.addEventListener('resize', apply);
  vv.addEventListener('scroll', apply);
  window.addEventListener('orientationchange', apply);
  apply();
}

// ── Boot ───────────────────────────────────────────────────

/* ── The update notice ────────────────────────────────────────────────────────
   The asking and the comparing are update.js's; this is only the three places
   the answer is shown. Nothing here is allowed to be the reason a player
   notices something is wrong — every failure lands on the same quiet stamp the
   build would have worn anyway. */
function initUpdate() {
  if (!window.Update) return;

  /* The corners print the version, and they print it from one constant rather
     than from three copies of the same string in the markup. */
  Update.fill();

  function say(state) {
    var fresh = state === 'stale';
    var vars = { latest: Update.latest() || '', version: Update.version };

    /* The lobby line and the corner dot exist only while there is something
       newer to say. A standing "you are up to date" is not news, and a line that
       said it on every launch is the first thing anyone learns to stop reading. */
    var note = el('update-note');
    if (note) {
      note.hidden = !fresh;
      if (fresh) el('update-note-copy').textContent = T('update.note', vars);
    }
    var cornerDot = el('update-corner-dot');
    if (cornerDot) cornerDot.hidden = !fresh;

    /* Settings: the version is always there, the marker only when it applies. */
    var rowDot = el('settings-update-dot');
    if (rowDot) rowDot.hidden = !fresh;
    var rowNote = el('settings-update-note');
    if (rowNote) rowNote.textContent = fresh ? T('update.newer', vars) : '';

    /* The card. `idle` means nobody has asked yet, so it says nothing rather than
       claiming the shelf was out of reach. */
    var status = el('update-status');
    if (status) {
      status.textContent =
        state === 'idle'     ? '' :
        state === 'checking' ? T('update.checking') :
        state === 'stale'    ? T('update.stale', vars) :
        state === 'current'  ? T('update.current') :
                               T('update.unknown');
    }

    /* One button wearing two labels. Checking is not something to ask for twice
       at once, so it stands down while a check is in the air. */
    var label = el('update-action-label');
    if (label) label.textContent = fresh ? T('update.get', vars) : T('update.check');
    var action = el('update-action');
    if (action) {
      action.classList.toggle('pill-primary', fresh);
      action.disabled = state === 'checking';
    }
  }

  function openCard() {
    Sound.sfx('select');
    el('update-panel').hidden = false;
    /* Opening the card is asking. A player who came here has been told nothing
       if the check that ran at boot never got an answer, so try again — this is
       the one moment somebody is definitely waiting for it. */
    var state = Update.state();
    if (state === 'idle' || state === 'unknown') Update.check();
  }

  el('update-corner').addEventListener('click', openCard);
  el('settings-update').addEventListener('click', openCard);

  el('update-action').addEventListener('click', function () {
    Sound.sfx('select');
    if (Update.state() === 'stale') Update.open(Update.notesURL());
    else Update.check();
  });

  Update.on('state', say);
  /* The notice is built in JS rather than carried in the markup, so a language
     change has to tell it to say itself again. */
  document.addEventListener('langchange', function () { say(Update.state()); });

  say(Update.state());
  Update.check();
}

function boot() {
  /* Before anything is built: `renderNames` and every renderer downstream read
     the table through `T`, and half of them write their copy into the DOM at
     the moment they run. */
  setLang(savedLang());
  initLobby();
  initOnline();
  initBoardChrome();
  /* Last, and deliberately so: the version stamps are decoration on a screen
     that is already drawn, and the check goes out over the network the moment
     this runs. Nothing above it should be waiting on a reply that may never
     come. */
  initUpdate();
  /* The pills ship `aria-pressed="true"` and no state word, and this is what
     fills in the word. Handing the layer its own defaults back is the point:
     the switches are drawn from `S`, so a boot that skipped this would leave the
     menu describing a stage the layer was not standing on. */
  applyStage();
  initKeyboard();
  initStageBuzz();
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

  /* Leaving the app and coming back is the one transition no screen change
     announces, so the show is put down on the way out and asked for again on the
     way in. `pageshow` is the same repair for a page restored rather than
     unhidden — iOS WebView does both and which one fires depends on how it was
     put away — and `pagehide` is its way out, which on iOS arrives before the
     page is ever called hidden. Both directions are idempotent, so a shell that
     fires all four handlers costs nothing. */
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') Sound.resume();
    else Sound.suspend();
  });
  window.addEventListener('pageshow', function () { Sound.resume(); });
  window.addEventListener('pagehide', function () { Sound.suspend(); });

  watchKeyboard();

  /* Not part of the door, and never in front of it: a worker that refuses to
     register costs the browser build its offline copy and nothing else. */
  keepOffline();

  /* Last, and deliberately: the pass collects its work by reading `document.images`,
     so it has to run after the chooser has been built. See `bootWarm`. */
  bootWarm();
}

/* ── The show with no network ────────────────────────────────
   The game is a box of files, not a service. Every clue, every voice and every
   picture is already in the tree, so the only thing standing between a player and
   a match with no network is that the browser has to be told to keep them.

   The worker caches what the pass fetches, under the cache tags already written
   into every URL. That tag is the project's own invalidation contract: bump it,
   and the next request is a miss whatever any cache thinks, so a moved file can
   never be served from a stale copy.

   Guarded twice. A webview loads the show off `file://`, where a worker cannot
   register at all — the apps are already offline by construction, so there is
   nothing to add there — and a page served from a socket has no use for one. */
function keepOffline() {
  if (!navigator.serviceWorker || !navigator.serviceWorker.register) return;
  if (location.protocol !== 'http:' && location.protocol !== 'https:') return;
  try {
    /* The version is in the address on purpose: a new cut registers a new URL,
       which is what makes the browser run the new worker rather than the old one. */
    navigator.serviceWorker.register('sw.js?v=' + Update.version)
      .catch(function (err) { console.warn('[offline] no worker:', err && err.message); });
  } catch (err) {
    console.warn('[offline] no worker:', err && err.message);
  }
}

/* ── The pass before the door ────────────────────────────────
   One screen of waiting, and a door that opens on the screen about to be shown
   rather than on the whole library.

   What the door is made of is small: the three pictures the stylesheet and the
   lens reach for, the wordmark and the disc this screen already wears, the tile
   and the wordmark of every circle on the door, and — when a `?ed=` link is
   heading straight past it — that edition's title card. Everything else waits
   behind the door and is allowed to lose. A voice that never arrives should cost
   its own line and nothing else.

    That permission is the point. The gate used to be the library: 307 files and
   57 MB, 27 MB of it voice, and one throttled request meant a show that never
   opened, on the one screen with no way past it.

   The rest is warmed behind the door, and it is warmed by asking for bytes rather
   than by opening files as media. That distinction is the whole of why the phones
   work: a warm that opened an `<audio>` per voice spent hundreds of the live media
   slots a handset rations, before a single buzzer sounded, which is how a show ends
   up unable to play its own theme. `fetch` asks for the same file, puts it in the
   cache the show will read from later, and holds nothing open to do it.

   A handful of files are in flight at once for the same reason, and on a bundle
   read off the disk the warm does not run at all: those bytes are already local,
   and a `file://` fetch is refused rather than served.

   Warm the rest anyway, and walk the registry whole rather than filtered to the
   edition that happens to be current: a course fetches its pictures when its
   circle is pressed, which is on a stage still wearing the previous show's, so
   warming here moves that fetch to where nothing can see it. The registry declares
   `tile`, `hero` and `logo` per edition, so the walk skips the Qajars' missing
   wordmark and backdrop without a special case: a file that does not exist is not
   declared, and is never requested. */

var BOOT_ART = [
  'assets/front-portal.jpg?v=20260915-globe-22',
  'assets/stage-backdrop.png?v=20260915-globe-22',
  'assets/globe-lensmap.png?v=20260915-globe-22'
];

/* A pass over a warm cache finishes in a few frames, and a screen that appeared
   and vanished would read as a flash rather than as a title. */
var BOOT_MIN_MS = 1500;

/* Patience, not a verdict: a file still in flight when this runs is left to
   arrive later and the door opens without it. The show is never held shut by a
   file that will not come. */
var BOOT_SLOW_MS = 8000;

/* How many files the pass may have in flight at once. A phone is half the reason
   the number exists — hundreds of open requests is more than a handset will carry,
   and a webview that runs out of memory takes the page, boot screen and all, down
   with it — and the other half is that six is about as many connections as a
   browser will open to one host anyway. The same warm, in the same order, a handful
   at a time. */
var BOOT_WINDOW = 6;

function bootWarm() {
  var section = el('screen-boot'), fill = el('boot-fill'), track = el('boot-track');
  var seen = {}, list = [], done = 0, ready = 0, gated = 0, missed = [];
  var settled = false, started = Date.now();
  var i, j;

  /* The apps, and the `file://` page a developer opened by hand: the show is already
     on the disk under it. Nothing below is worth doing, and the fetches would be
     refused. */
  var local = location.protocol === 'file:';

  /* The door's own files, keyed the way the roster is: the path with the query
     stripped, because the same picture can be asked for under two cache tags and
     that is still one file. */
  var gate = {};
  var hold = function (src) {
    if (!src) return;
    gate[String(src).split('?')[0]] = 1;
  };

  var add = function (src, kind) {
    if (!src) return;
    var key = String(src).split('?')[0];
    if (seen[key]) return;
    seen[key] = 1;
    list.push({ src: src, kind: kind || 'image' });
  };

  var imgs = document.images;
  for (i = 0; i < imgs.length; i++) {
    add(imgs[i].getAttribute('src'), 'image');
    /* This screen's own two: the wordmark above, the disc under the lens. */
    if (imgs[i].id === 'boot-logo' || imgs[i].id === 'boot-globe-art') {
      hold(imgs[i].getAttribute('src'));
    }
  }
  for (i = 0; i < BOOT_ART.length; i++) {
    add(BOOT_ART[i], 'image');
    hold(BOOT_ART[i]);
  }

  /* Generated from the shipped tree. This covers CSS-only art, every voice and
     sting, and the fonts as well as the pictures already in the document. */
  var shipped = window.BOOT_ASSETS || [];
  if (!local) for (i = 0; i < shipped.length; i++) add(shipped[i].src, shipped[i].kind);

  var eds = window.getEditions ? window.getEditions() : [];
  for (i = 0; i < eds.length; i++) {
    add(eds[i].tile, 'image'); add(eds[i].hero, 'image'); add(eds[i].logo, 'image');
    var extra = eds[i].art || [];
    for (j = 0; j < extra.length; j++) add(extra[j], 'image');
    /* Every circle on the door wears its edition's tile, and the lockup is the
       wordmark, so both are the door's own furniture. What an edition wears once
       it has been opened is not. */
    hold(eds[i].tile); hold(eds[i].logo);
  }

  /* A `?ed=` link skips the door for one edition's title card, so when this pass
     is handing over to `splash` the art on the screen about to be shown belongs
     to that edition: its hero over its own tile. */
  if (S.bootTarget === 'splash') {
    var bound = null;
    var opening = window.getEdition ? window.getEdition() : '';
    for (i = 0; i < eds.length; i++) if (eds[i].id === opening) bound = eds[i];
    if (bound) {
      hold(bound.hero);
      var wears = bound.art || [];
      for (i = 0; i < wears.length; i++) hold(wears[i]);
    }
  }

  /* And the figure at the foot of the stage, every show's. She is the one picture
     that is asked for mid-match rather than at a screen change, so without this
     the first verdict of a round is where her face arrives. */
  if (window.HostLayer && window.HostLayer.art) {
    var floor = window.HostLayer.art();
    for (i = 0; i < floor.length; i++) add(floor[i], 'image');
  }

  /* Which of them the door is actually waiting on — and they go first. The roster
     is built by appending: the document's pictures, this screen's three, then the
     whole shipped library, and the editions' tiles only after it. Left in that
     order the pass spends its window on voices the door is not waiting for while
     the two pictures it is waiting for sit four hundred deep, so every boot ends up
     opened by the patience timer instead of by the files, and every one of those
     files is fetched late enough that a player who goes offline in between is
     holding half a door. The door's furniture first, then the library behind it. */
  var front = [], back = [];
  for (i = 0; i < list.length; i++) {
    list[i].gate = gate[String(list[i].src).split('?')[0]] ? 1 : 0;
    gated += list[i].gate;
    (list[i].gate ? front : back).push(list[i]);
  }
  list = front.concat(back);

  /* The bar is the door's own progress, because the door is what it is holding.
     The rest of the library goes on arriving behind it, and nothing on this screen
     waits for that. */
  var paint = function () {
    var share = gated ? ready / gated : 1;
    if (fill) fill.style.transform = 'scaleX(' + share + ')';
    if (track) track.setAttribute('aria-valuenow', String(Math.round(share * 100)));
  };

  var finish = function () {
    if (settled) return;
    settled = true;
    /* A file that never arrived is named for whoever has the console open, and is
       not a reason to keep the show shut. */
    if (missed.length) {
      console.warn('[boot] opening without ' + missed.length + ' file(s):', missed);
    }
    var pause = Math.max(0, BOOT_MIN_MS - (Date.now() - started));
    setTimeout(function () {
      /* The screen is asked whether it is still the one on the floor, because a
         link carrying `?code=` opens the online door from `initOnline` — which
         runs before this pass — and a loader that finished while the player was
         already somewhere else must not pull them back to the front door. */
      if (S.screen !== 'boot') return;
      if (section) section.setAttribute('data-boot', 'ready');
      var word = el('boot-status');
      if (word) word.textContent = T('boot.ready');
      /* The door comes up under a loader that is still leaving: `#screen-boot`
         fades over half a second, so the hand-off is here rather than on the
         transition's end. `bootTarget` is the one thing that beats it — a
         `?ed=` link, which skips the door for its own title card. */
      var target = S.bootTarget || 'front';
      setTimeout(function () {
        if (S.screen === 'boot') show(target);
      }, 320);
    }, pause);
  };

  /* The two pictures on this screen are held invisible by the stylesheet and
     lifted here, one file each, the moment that file is in hand. Asked of
     `complete` first: a file already in the cache is finished before this runs,
     and a `load` listener added after that never fires. A failed file lifts the
     veil too — a 404 must not hold a title card blank forever. */
  var unveil = function (nodeId, imgId) {
    var node = el(nodeId), img = el(imgId), on;
    if (!node || !img) return;
    on = function () { node.classList.add('is-on'); };
    if (img.complete && img.naturalWidth) { on(); return; }
    img.addEventListener('load', on);
    img.addEventListener('error', on);
  };
  unveil('boot-logo', 'boot-logo');
  unveil('boot-globe', 'boot-globe-art');

  /* A file that failed is not a file that is loading, so each one answers once. */
  var cursor = 0, open = 0;
  var tick = function (asset, bad) {
    if (asset.fired) return;
    asset.fired = true;
    open--;
    if (bad) missed.push(asset.src);
    done++;
    if (asset.gate) ready++;
    paint();
    if (ready >= gated) finish();
    pump();
  };

  /* How one file is asked for, which is not the same question for all of them.

     The door's own art is loaded as art, because it is on the screen and the point
     is that a player is looking at it: an `Image` that reports back is the only
     proof of that.

     Everything behind the door is only ever being asked for its bytes. Fetching it
     puts the file in the cache — the browser's, and the worker's, which is what
     makes the show playable offline — and costs nothing an element costs: no
     decoder, and no slot on a floor where slots are the scarce thing. A phone caps
     how many media elements may be live at once (`release`, above, exists because
     this show already ran into that), and a warm that opened one per voice would
     spend the entire allowance before the first buzzer sounded. The cue's own
     element is cut when the cue is played, reads the file out of the cache, and
     gives its decoder back when it ends.

     On a bundle read off the disk there is nothing here to do at all: those bytes
     are already local, and a `fetch` of a `file://` URL is refused. Hence the
     guard, and hence a warm that only ever runs where there is a network to save
     the show from. */
  var load = function (asset, index) {
    if (asset.kind === 'font') {
      var face = new FontFace('JeopardyBoot' + index, 'url("' + asset.src + '")');
      face.load().then(function (loaded) {
        document.fonts.add(loaded); tick(asset, false);
      }).catch(function () { tick(asset, true); });
    } else if (asset.gate) {
      var im = new Image();
      im.onload = function () { tick(asset, false); };
      im.onerror = function () { tick(asset, true); };
      im.src = asset.src;
    } else if (window.fetch) {
      /* Asked of the network the ordinary way, so the request goes through the
         worker and lands in its cache as well as the browser's. */
      fetch(asset.src)
        .then(function (res) { tick(asset, !res || !res.ok); })
        .catch(function () { tick(asset, true); });
    } else {
      tick(asset, true);
    }
  };

  /* The window: never more than `BOOT_WINDOW` files in flight, and the next one
     starts as one lands. The rest of the library finishes arriving behind the
     door, at whatever pace the line allows. */
  var pump = function () {
    while (cursor < list.length && open < BOOT_WINDOW) {
      var index = cursor++;
      load(list[index], index);
      open++;
    }
  };

  paint();
  setTimeout(function () {
    if (settled) return;
    missed.push('still in flight: ' + Math.max(0, gated - ready) + ' of ' + gated + ' gated');
    finish();
  }, BOOT_SLOW_MS);

  if (list.length && gated) pump();
  else finish();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();

})();
