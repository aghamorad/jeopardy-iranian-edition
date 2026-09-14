/* The edition registry — which shows this build can play.
 *
 * The engine registers MAIN, `general`, out of the two banks that ship in the box.
 * Every course the build carries then registers one more, from its own
 * `Web/courses/<course-id>/course.js`, which loads after this file. There is no
 * ceiling: a build ships MAIN plus as many courses as it has folders for, and
 * adding a course means adding that folder and three tags to `index.html` —
 * nothing in this file changes.
 *
 * This file is engine code. A course must never replace it.
 *
 * An edition descriptor is:
 *
 *   { id:    'iran-in-world-politics',               // url-safe, the ?ed= value
 *     name:  { en: '…', fa: '…' },                   // the splash tile label
 *     blurb: { en: '…', fa: '…' },                   // one line of shelf copy, optional
 *     tile:  'courses/<id>/assets/tile-<id>.png',    // splash tile art, optional
 *     banks: { en: window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS,
 *              fa: window.COURSE_CLUES_IRAN_IN_WORLD_POLITICS_FA } }
 *
 * `name` and `blurb` are edition data, not i18n keys: an edition names and
 * describes itself in both languages and the engine never has to learn either.
 * MAIN carries no `blurb` — it is the boxed edition and does not have to sell
 * itself — which is why the shelf draws that card without a second line.
 *
 * The folder name, the id and the `?ed=` value are the same string, and the bank
 * globals are `COURSE_CLUES_<UPPER_SNAKE(folder)>` (`+ _FA`). Grep the folder
 * name and you find everything that course owns.
 *
 * `banks` must be live arrays — the engine rebinds them by identity when the
 * language or the edition changes. A course's banks are its own arrays and are
 * never merged into `window.CLUES`: that is what keeps MAIN out of a course and
 * one course out of another. Authoring may draw on MAIN's material; the runtime
 * never mixes them.
 */
(function () {
'use strict';

var LIST = [];   /* ids, in registration order — the chooser's order and the default */
var BY_ID = Object.create(null);
var KEY = 'jeopardy.edition';

window.registerEdition = function (ed) {
  if (!ed || !/^[A-Za-z0-9_-]{1,32}$/.test(ed.id || '') || !ed.banks) return;
  if (!Array.isArray(ed.banks.en) || !ed.banks.en.length ||
      !Array.isArray(ed.banks.fa) || !ed.banks.fa.length) return;
  if (BY_ID[ed.id]) return;          /* first registration wins, so a course
                                        cannot shadow MAIN */
  BY_ID[ed.id] = ed;
  LIST.push(ed.id);
};

window.getEditions = function () {
  return LIST.map(function (id) { return BY_ID[id]; });
};

function readParam() {
  var m = /[?&]ed=([A-Za-z0-9_-]{1,32})/.exec(location.search || '');
  return m ? m[1] : '';
}

function saved() {
  try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; }
}

var current = null;

window.setEdition = function (id, persist) {
  if (!BY_ID[id] || id === current) return;
  if (!document.dispatchEvent(new CustomEvent('beforeeditionchange', {
    cancelable: true, detail: { id: id }
  }))) return;
  current = id;
  /* The skin hooks off this attribute, the way the existing RTL rules hook off
     `html[dir]`. It is set before the event fires so a listener may read it. */
  document.documentElement.setAttribute('data-edition', id);
  if (persist !== false) { try { localStorage.setItem(KEY, id); } catch (e) {} }
  document.dispatchEvent(new CustomEvent('editionchange', { detail: { id: id } }));
};

/* Resolution is lazy, and deliberately so: a course's `course.js` is a later
   script than this one, so a course link read at load time would look like an
   unknown edition and fall back. The first caller is the engine's own boot.

   Order: a shared link wins, then the last visit, then the first registered
   edition. A link persists, so following one and then navigating around does
   not silently revert to the other show. */
function ensure() {
  if (current) return;
  var wanted = readParam();
  if (!BY_ID[wanted]) {
    wanted = saved();
    if (!BY_ID[wanted]) wanted = LIST[0];
  }
  if (wanted) window.setEdition(wanted);
}

window.getEdition = function () { ensure(); return current || ''; };

/* `general` is MAIN — the boxed edition, carrying the full corpus. It registers
   first, so it is the default in every build, and so no course can displace it.
   Its `id` stays `general` because ids are load-bearing and this one is in saved
   state and in the `?ed=` of every link ever shared; only the name the player
   reads moves to the vocabulary the rest of the project uses. */
window.registerEdition({
  id: 'general',
  name: { en: 'Main Edition', fa: 'نسخهٔ اصلی' },
  /* Two images, because the front door uses them differently: `tile` is the small
     square that has to survive a stamp, and `hero` is the wide art behind the one
     large card. A build that has only a tile falls back to it. */
  tile: 'assets/tile-general.png',
  hero: 'assets/hero-main.png',
  logo: 'assets/logo-wordmark.png',
  /* Her, in the same shape a course declares its professor and its institution:
     an edition's own copy in both languages, not an i18n key. This is what the
     title card prints on MAIN's imprint — see the course for the other half. */
  host: { name: { en: 'Tannaz Deadband', fa: 'طناز ددبند' } },
  banks: { en: window.CLUES, fa: window.CLUES_FA },
  readings: window.READINGS_GENERAL
});

})();
