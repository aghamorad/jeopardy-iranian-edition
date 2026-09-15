/* Read-only regression checks for the shipped web logic. Run: node Tools/check_web.js */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..', 'Web');
const events = new Map();
const digits = [{ textContent: '1' }, { textContent: '2' }, { textContent: '3' }];
const attributes = {};
const document = {
  readyState: 'loading',
  createElement() { return { volume: 1 }; },
  documentElement: { setAttribute(k, v) { attributes[k] = v; } },
  body: { classList: { toggle() {} } },
  addEventListener(k, fn) { events.set(k, [...(events.get(k) || []), fn]); },
  dispatchEvent(ev) { for (const fn of events.get(ev.type) || []) fn(ev); return !ev.defaultPrevented; },
  querySelectorAll(q) { return q === '[data-num]' ? digits : []; }
};
class CustomEvent {
  constructor(type, options = {}) { this.type = type; Object.assign(this, options); }
  preventDefault() { if (this.cancelable) this.defaultPrevented = true; }
}
const ctx = { document, CustomEvent, console, location: { search: '' },
  localStorage: { getItem() { return null; }, setItem() {} },
  navigator: {}, performance: { now: () => 0 }, setTimeout, clearTimeout, setInterval, clearInterval,
  Audio: class { constructor() { this.volume = 1; } },
  requestAnimationFrame() {}, addEventListener() {} };
ctx.window = ctx;
vm.createContext(ctx);
function load(file) { vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file }); }
for (const f of ['i18n.js', 'data/clues.js', 'data/clues_fa.js', 'editions.js', 'answers.js']) load(f);
let app = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
app = app.replace(/\}\)\(\);\s*$/, 'window.audit = { S: S, buildBoard: buildBoard, rebindBanks: rebindBanks, bank: function () { return CLUES; }, freeSeat: freeSeat, Online: Online, shufflingOptions: shufflingOptions };\n})();');
vm.runInContext(app, ctx, { filename: 'app.js' });
const keys = Object.keys(ctx.I18N.en).sort();
// Parity is the invariant; the total is not. An exact count has to be edited by
// hand for every new string, which trains the edit to be made without thought —
// and it fails on a correct build the moment a key is added. The floor is the
// other half: it catches a file that loaded empty or half-parsed, which is the
// failure an exact count was there to catch.
assert.ok(keys.length >= 232,
  `expected at least 232 strings per language, got ${keys.length}`);
assert.deepEqual(keys, Object.keys(ctx.I18N.fa).sort(),
  'the en and fa tables must carry the same keys');
for (const lang of ['en', 'fa', 'en']) {
  ctx.setLang(lang);
  assert.equal(digits[0].textContent, lang === 'fa' ? '۱' : '1');
  const bank = lang === 'fa' ? ctx.CLUES_FA : ctx.CLUES;
  assert.equal(ctx.audit.bank(), bank);
  const original = JSON.stringify(bank);
  for (let trial = 0; trial < 100; trial++) {
    ctx.audit.S.usedCategories = {};
    for (const round of ['single', 'double']) {
      const board = ctx.audit.buildBoard(round);
      assert.equal(board.length, 6);
      let doubles = 0;
      for (const col of board) {
        assert.equal(col.cells.length, 5);
        for (const [row, cell] of col.cells.entries()) {
          assert(bank.some(c => c.id === cell.clue.id && c.clue === cell.clue.clue));
          assert.equal(cell.clue.options[cell.clue.correct], cell.clue.answer);
          if (cell.dailyDouble) { doubles++; assert(row > 0); }
        }
      }
      assert.equal(doubles, 1);
    }
  }
  assert.equal(JSON.stringify(bank), original, 'dealing must not mutate source bank');
}

/* A clue whose authored correct answer alone has a parenthetical is the exact
   regression case. The buttons must not carry the author's gloss at all — not
   on the correct option, not on a distractor, and not as a flattened dash. The
   dash was the earlier disguise and leaked just as loudly as the parentheses:
   it only ever appeared on the option that had been glossed, and that option is
   the answer. Asserted across shuffles, because which position the answer lands
   in is not what makes it findable. */
const parenClue = {
  answer: 'National Iranian Oil Company (NIOC)',
  options: ['National Iranian Oil Company (NIOC)', 'Anglo-Iranian Oil Company',
            'National Petrochemical Company', 'Iranian Offshore Oil Company'],
  correct: 0
};
const bare = ['National Iranian Oil Company', 'Anglo-Iranian Oil Company',
  'National Petrochemical Company', 'Iranian Offshore Oil Company'].sort();
for (let trial = 0; trial < 50; trial++) {
  const dealt = ctx.audit.shufflingOptions(parenClue);
  assert.equal(dealt.options[dealt.correct], parenClue.answer);
  assert.equal(Array.from(dealt.displayOptions).sort().join('|'), bare.join('|'),
    'the buttons show the names, without the gloss');
  assert.equal(dealt.displayOptions[dealt.correct], 'National Iranian Oil Company');
  for (const shown of dealt.displayOptions) {
    assert.ok(!/[\(\)（）]/.test(shown), `a button still wears a parenthesis: ${shown}`);
    assert.ok(shown.indexOf('—') === -1, `a button still wears the giveaway dash: ${shown}`);
  }
}
assert.equal(parenClue.options[0], parenClue.answer, 'the source clue is never edited');
/* The gloss is not deleted, only kept off the buttons: the verdict card and the
   host's line read `options`, and the archive invariant lives there too. */
const settled = ctx.audit.shufflingOptions(parenClue);
assert.ok(settled.options[settled.correct].indexOf('NIOC') !== -1,
  'the gloss must survive on the raw options');
/* Stripping can merge two buttons when a clue ships a name and that name with a
   gloss as two different options. A board that shows the same text twice is
   worse than a hint, so the gloss stays in that case. */
const twinClue = {
  answer: 'Wine (and Beer)',
  options: ['Wine (and Beer)', 'Wine', 'Sherbet', 'Doogh'],
  correct: 0
};
const twins = ctx.audit.shufflingOptions(twinClue);
assert.equal(new Set(twins.displayOptions).size, twins.displayOptions.length,
  'stripping a gloss must not merge two buttons on one board');
assert.ok(twins.displayOptions.includes('Wine (and Beer)'),
  'the gloss is kept when dropping it would collide');
ctx.registerEdition({ id: 'missing', banks: { en: ctx.CLUES } });
assert.equal(ctx.getEditions().length, 1);
ctx.registerEdition({ id: 'test', banks: { en: ctx.CLUES, fa: ctx.CLUES_FA } });
ctx.audit.S.screen = 'board';
ctx.setLang('fa');
ctx.setEdition('test');
assert.equal(ctx.getLang(), 'en');
assert.equal(attributes.dir, 'ltr');
assert.equal(ctx.getEdition(), 'general');
ctx.audit.S.screen = 'splash';
ctx.audit.S.players = [{ name: 'stale roster' }];
ctx.setLang('fa');
assert.equal(ctx.audit.bank(), ctx.CLUES_FA);
ctx.setEdition('test');
assert.equal(ctx.getEdition(), 'test');
ctx.audit.Online.order = [{ seat: 1 }, { seat: 2 }];
assert.equal(ctx.audit.freeSeat(), -1);
const enIds = new Map(ctx.CLUES.map(c => [c.id, Object.keys(c).sort().join(',')]));
/* Parity and shape are the invariants here; the total is not, for the same
   reason the i18n table above gives. The bank grows — a course's clues are
   promoted up into it — and a number written down by hand turns every
   legitimate addition into a red build, which is how a real failure learns to
   be waved through. The floor is the other half: it still catches a bank that
   loaded empty or half-parsed. */
assert.ok(ctx.CLUES.length >= 1000, `only ${ctx.CLUES.length} English clues in the bank`);
assert.equal(ctx.CLUES_FA.length, ctx.CLUES.length, 'the two banks must carry the same rows');
for (const clue of ctx.CLUES_FA) assert.equal(enIds.get(clue.id), Object.keys(clue).sort().join(','));
/* A parenthetical in `answer` is an editorial gloss — "Wine (and Beer)",
   "National Iranian Oil Company (NIOC)" — not a second answer. The generous
   rules used to treat it as one, because they read the last word of whatever
   string they were handed and the answer ended in (NIOC), (Armband),
   (Illumination). The gloss is gone from that string now, so a verdict on the
   gloss can no longer be justified by the answer itself. It may still be
   correct — an alias the clue lists can carry it, as "Jamal al-Din Asadabadi"
   carries "Asadabadi" — and that is the author's listing, which is the point.
   The clue that lists its own printed answer as an alias is exempt for the same
   reason. */
const norm = s => ctx.Answers.normalize(s, false);
let glosses = 0;
for (const clue of ctx.CLUES.concat(ctx.CLUES_FA)) {
  const gloss = (/\(([^)]*)\)/.exec(clue.answer) || [])[1];
  if (!gloss) continue;
  if ((clue.aliases || []).map(norm).includes(norm(clue.answer))) continue;
  glosses++;
  const verdict = ctx.Answers.judge(gloss.trim(), clue, {});
  assert.notEqual(verdict.matched, clue.answer,
    `the parenthetical of ${JSON.stringify(clue.answer)} was answered by the clue's own answer string`);
  assert.equal(ctx.Answers.judge(clue.answer, clue, {}).result, 'correct',
    `the answer as printed must still be accepted: ${JSON.stringify(clue.answer)}`);
}
assert.ok(glosses >= 190, `only ${glosses} glosses exercised — the bank or the rule moved`);
class Emitter {
  constructor() { this.handlers = {}; }
  on(k, fn) { this.handlers[k] = fn; }
  fire(k, ...args) { if (this.handlers[k]) this.handlers[k](...args); }
}
class Peer extends Emitter {
  constructor() { super(); Peer.instances.push(this); }
  connect() { this.conn = new Emitter(); this.conn.sent = []; this.conn.send = m => this.conn.sent.push(m); return this.conn; }
  destroy() { this.fire('error', { message: 'stale' }); }
}
Peer.instances = [];
ctx.Peer = Peer;
load('net.js');
let errors = 0, connected = 0;
ctx.Net.on('error', () => errors++);
ctx.Net.on('connected', () => connected++);
ctx.Net.join('TEST', 'Guest');
const first = Peer.instances[0];
first.fire('open'); first.conn.fire('open');
assert.equal(first.conn.sent[0].t, 'hello');
assert.equal(connected, 1);
ctx.Net.join('NEXT', 'Guest');
first.conn.fire('open'); first.conn.fire('close'); first.fire('error', {});
assert.equal(errors, 0);
assert.equal(connected, 1);
assert.equal(ctx.Net.state.code, 'NEXT');
ctx.Net.close();

/* ── The host on the floor ────────────────────────────────────────
   `host-layer.js` says in its own header that a row of `LINES` is a transcript
   of a clip, and that a line reworded to taste is a bubble that misquotes the
   speaker to her face. That rule is a comment, and a comment cannot fail a
   build — so the half of it a machine can hold is held here.

   What is checked is the pairing, not the wording. A caption with no clip puts
   words in her mouth over silence; a clip with no caption leaves her mute
   through a cue she was recorded for. Both are invisible in review and loud in
   the room. Whether a caption matches the *sound* is not something a check can
   know without speech recognition: the table is a hand-corrected reading of a
   fuzzy transcript and three of its rows are documented ambiguities, so an
   exact comparison would fail on a correct tree. Re-record, then re-transcribe.
   ───────────────────────────────────────────────────────────────── */
const hostCtx = { console, setTimeout, clearTimeout,
  document: { getElementById: () => null, createElement: () => ({}), addEventListener() {} } };
hostCtx.window = hostCtx;
vm.createContext(hostCtx);
/* The table is closed over, the same way the engine's state is: reached by
   appending to the IIFE rather than by widening what the page exposes. */
let host = fs.readFileSync(path.join(root, 'host-layer.js'), 'utf8');
host = host.replace(/\}\)\(\);\s*$/, 'window.hostAudit = { LINES: LINES };\n})();');
vm.runInContext(host, hostCtx, { filename: 'host-layer.js' });
const LINES = hostCtx.hostAudit.LINES;
const audio = path.join(root, 'assets', 'audio');
const clips = fs.readdirSync(audio).filter(f => /^tannaz_.*\.m4a$/.test(f))
  .map(f => f.slice(0, -4)).sort();
assert.deepEqual(Object.keys(LINES).sort(), clips,
  'every cue with a clip carries a caption, and every caption carries a clip');
for (const [cue, said] of Object.entries(LINES)) {
  assert.ok(said && said.trim(), `${cue} has an empty caption`);
  for (const ext of ['m4a', 'mp3']) {
    assert.ok(fs.existsSync(path.join(audio, `${cue}.${ext}`)),
      `${cue} is captioned but ships no .${ext}`);
  }
}

/* ── What the front door asks for ────────────────────────────────
   A path typo in `index.html` is a blank screen with nothing in the console to
   explain it, and it is the one shipped file no other check reads. */
const page = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const refs = [...page.matchAll(/(?:src|href)="([^"]+)"/g)].map(m => m[1])
  .filter(u => !/^(?:https?:|data:|mailto:|#|\/)/.test(u))
  .map(u => u.split('?')[0]).filter(Boolean);
/* The floor, because a parser that matched nothing would pass an empty loop. */
assert.ok(refs.length >= 20, `only ${refs.length} local references found in index.html`);
for (const ref of new Set(refs)) {
  assert.ok(fs.existsSync(path.join(root, ref)),
    `index.html asks for a file that is not there: ${ref}`);
}

console.log('PASS: i18n parity, reversible numerals, 600 boards, gloss-free buttons, bank shape/identity/immutability, match guards, three seats, guest handshake, stale transport events, parenthetical glosses, host caption/clip pairing and front-door references.');
