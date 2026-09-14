/* A scaffold for a new course edition. Not a show.
 *
 * Copy this folder to `Web/courses/<course-id>/`, then change one string — the
 * course's id — everywhere it appears:
 *
 *   the folder name            Web/courses/<course-id>/
 *   `id` below, and `?ed=`     <course-id>
 *   the tile path below        courses/<course-id>/assets/…
 *   the two bank globals       COURSE_CLUES_<UPPER_SNAKE(course-id)> (+ `_FA`)
 *   the bank headers           data/bank-en.js, data/bank-fa.js
 *
 * That is the naming rule, and it is the whole of it: the folder, the id and the
 * `?ed=` value are one string, and the bank globals are that string in upper
 * snake case. Grep the folder name and you find everything the course owns.
 * Then add one `<link>` and three `<script>` tags to `Web/index.html`, in the
 * blocks marked for courses, and the show is on air.
 *
 * The banks are not optional and not a stub to fill later — `registerEdition`
 * refuses a course missing either language, and an empty array is not a bank.
 * The placeholders in `data/` already fill a playable board, so copy the folder,
 * watch it deal, and then replace the questions.
 *
 * Everything after the registration is optional, and the two pieces below are
 * the two things a course usually wants. Delete what you do not use: a course
 * with no voice and no skin is a course with different questions in it, which is
 * exactly what a course is.
 */
(function () {
  'use strict';

  var ID = 'your-course';

  /* Required, and the only required part.
   *
   * `editions.js` loads after MAIN has registered itself out of `data/clues.js`,
   * so `general` is already first in the list and stays the default; a course is
   * the show a player opts into. A course cannot register before MAIN, and the
   * first registration for an id wins, so this never shadows another show.
   *
   * `name` is the label on the chooser row and the splash chip, one per language.
   * `tile` is optional — the scaffold borrows MAIN's placeholder until the course
   * has art of its own. */
  window.registerEdition({
    id: ID,
    name: { en: 'Your Course', fa: 'دورهٔ شما' },
    tile: 'courses/your-course/assets/tile-course.png',
    banks: { en: window.COURSE_CLUES_YOUR_COURSE,
             fa: window.COURSE_CLUES_YOUR_COURSE_FA }
  });

  /* ── The course's own words (optional) ──────────────────────────────────────
   *
   * One string table serves every show, so a course's voice is worn rather than
   * written: put on when a player picks this tile, handed back when they leave.
   * Any key in `Web/i18n.js` can be overridden, in either language or both.
   *
   * Patch by key. Never replace the table object, or the engine's copy of the
   * rest of the room goes with it. */
  var BAGS = { en: window.I18N && window.I18N.en, fa: window.I18N && window.I18N.fa };
  if (!BAGS.en || !BAGS.fa) return;

  var COURSE = {
    en: {
      // 'lobby.rollout': 'The first seminar',
    },
    fa: {
      // 'lobby.rollout': 'نخستین جلسه',
    }
  };

  /* The engine's own wording, captured before the first wear overwrites any of
     it. Nothing may go into `COURSE` without its original landing here first, or
     MAIN could never be handed its copy back. */
  var ORIG = { en: {}, fa: {} };
  Object.keys(COURSE).forEach(function (lang) {
    Object.keys(COURSE[lang]).forEach(function (key) {
      ORIG[lang][key] = BAGS[lang][key];
    });
  });

  /* ── The course's own voice and stings (optional) ───────────────────────────
   *
   * Two globals, read by the engine on every draw while the course is on:
   *
   *   HOST_CUE_MAP  rename an engine cue to one of this course's clips
   *   HOST_VOICE    replace a whole pool of the host's lines
   *   EDITION_SOUND point a cue at a file under this course's own `assets/audio/`
   *
   * Clip NAMES stay bare identifiers in both maps — `course_theme`, never a
   * path. Only the values in `EDITION_SOUND` carry a path, and only that map is
   * allowed to: the engine resolves a file through it and falls back to its own
   * `assets/audio/` for anything the course does not claim. A cue name is also
   * broadcast to the rest of the course, which is how a clip gets a transcript
   * line — so a renamed cue still has to exist as a bare name here.
   *
   * All of them are published live rather than merged once, and deleted on the
   * way out: one build carries every show, so a merge made at boot would hand
   * this voice the room permanently, MAIN included. */
  var A = 'courses/your-course/assets/audio/';
  var SOUND = {
    // menu_theme: A + 'course_theme',
    // correct:    A + 'course_correct',
  };

  /* ── Worn on entering, taken off on leaving ─────────────────────────────────
   *
   * Driven by the registry's event, not by a read at load: this script runs
   * before `app.js` boots, and at load time no show has been chosen yet and
   * `document.documentElement` carries no `data-edition` to read. The boot
   * always dispatches — `setEdition` compares against a null current — so this
   * listener fires once during startup, before the first paint. */
  function wear(id) {
    var mine = id === ID;

    Object.keys(COURSE).forEach(function (lang) {
      var bag = BAGS[lang];
      var src = mine ? COURSE[lang] : ORIG[lang];
      Object.keys(src).forEach(function (key) {
        if (src[key] === undefined) { delete bag[key]; } else { bag[key] = src[key]; }
      });
    });
    if (window.applyI18n) window.applyI18n();

    if (mine) {
      window.EDITION_SOUND = SOUND;
    } else {
      delete window.EDITION_SOUND;
    }
    /* After the swap, never before it: a bed already on the air was started from
       the mapping that was current then, and re-issuing it is how the arriving
       show stops playing the soundtrack of the one that just left. No-op on the
       boot dispatch, where the audio layer does not exist yet. */
    if (window.Sound && window.Sound.refresh) window.Sound.refresh();
  }

  document.addEventListener('editionchange', function (e) { wear(e.detail.id); });
})();
