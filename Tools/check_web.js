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
   regression case. Hold the shuffle still, then prescribe two independent mask
   patterns: once the correct answer wears parentheses alongside a distractor;
   once it does not while two distractors do. No branch receives `correct`. */
const parenClue = {
  answer: 'National Iranian Oil Company (NIOC)',
  options: ['National Iranian Oil Company (NIOC)', 'Anglo-Iranian Oil Company',
            'National Petrochemical Company', 'Iranian Offshore Oil Company'],
  correct: 0
};
function dealtWith(sequence) {
  vm.runInContext(`Math.random = (function (a) { return function () { return a.shift(); }; })(${JSON.stringify(sequence)})`, ctx);
  return ctx.audit.shufflingOptions(parenClue);
}
let parenthesized = dealtWith([.99, .99, .99, .1, .9, .1, .9]);
assert.equal(Array.from(parenthesized.displayOptions, s => /^\(/.test(s)).join(','),
  'true,false,true,false');
assert.equal(parenthesized.options[parenthesized.correct], parenClue.answer);
assert.ok(parenthesized.displayOptions[0].includes('NIOC'), 'flattening must preserve the gloss');
parenthesized = dealtWith([.99, .99, .99, .9, .1, .9, .1]);
assert.equal(Array.from(parenthesized.displayOptions, s => /^\(/.test(s)).join(','),
  'false,true,false,true');
assert.equal(parenthesized.displayOptions[0], 'National Iranian Oil Company — NIOC');
assert.equal(parenthesized.options[parenthesized.correct], parenClue.answer);
vm.runInContext('delete Math.random', ctx);
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
assert.equal(ctx.CLUES.length, 1000);
assert.equal(ctx.CLUES_FA.length, 1000);
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
console.log('PASS: i18n parity, reversible numerals, 600 boards, independent option parentheses, bank shape/identity/immutability, match guards, three seats, guest handshake, stale transport events and parenthetical glosses.');
