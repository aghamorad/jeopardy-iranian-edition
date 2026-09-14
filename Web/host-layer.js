/* ── The host on the floor ──────────────────────────────────────
   Whichever show is running, one figure stands at the foot of the stage while
   the room is quiet. That figure is page furniture rather than course property:
   MAIN has Tannaz Deadband, a course brings its own, and both want the same
   bubble, the same crop and the same pop as a cue starts. So the layer is built
   and driven from here, and each show *registers* the speaker it wants on the
   floor.

   A registration is three things, and any of them may be absent:

       sprite   the resting image, worn when a cue has no pose of its own
       poses    pose name -> image, for a host drawn differently as she reacts
       pose     cue name -> pose name, the rule that picks one
       lines    cue name -> what she is saying

   A host with no line for a cue stands there wordless rather than being handed
   the other show's words. The bubble is a transcript of audio already playing
   out loud, and a caption nobody recorded is a caption that misquotes the room,
   so nothing in this file invents a line for anybody.

   The general edition registers itself below, because it is the page's own show
   and is always present. A course registers from its own script as it loads.
   The registry is keyed by edition id and re-worn on `editionchange`, which is
   the same live swap the rest of the build does — a boot-time merge would hand
   one show's host the other show's stage permanently.

   Built here rather than written into the markup: `index.html` is engine
   property and the build refuses an overlay that ships one. It hangs off `#app`
   rather than a `.screen`, which is `overflow: hidden` and hidden when inactive
   — a sprite inside one would be clipped and would vanish on every screen
   change — and rather than `body`, which would put it over the pause menu. As
   the last child of `#app` it shares that element's stacking context, where
   z-index 20 sits above every screen and below the overlays.

   `aria-hidden`, because the line it writes is a transcript of audio already
   playing out loud and should not be read a second time; `pointer-events: none`
   in the stylesheet, because this is a speaker, not a control. */
(function () {
  'use strict';

  var HOSTS = {};
  var show = null;
  var layer = null;
  var bubble = null;
  var line = null;
  var sprite = null;
  var clearTimer = null;

  (function build() {
    var host = document.getElementById('app');
    if (!host) return;

    layer = document.createElement('div');
    layer.id = 'prof-layer';
    layer.setAttribute('aria-hidden', 'true');

    bubble = document.createElement('div');
    bubble.className = 'prof-bubble';

    line = document.createElement('p');
    line.className = 'prof-line';
    /* The lines are English because the clips are English, whichever language
       the game is being played in. Marked, so the browser and a reader both take
       the line left-to-right inside a Persian page rather than guessing. */
    line.setAttribute('lang', 'en');
    line.setAttribute('dir', 'ltr');
    bubble.appendChild(line);

    sprite = document.createElement('img');
    sprite.className = 'prof-sprite';
    sprite.setAttribute('alt', '');

    layer.appendChild(bubble);
    layer.appendChild(sprite);
    host.appendChild(layer);
  })();

  function setSprite(src) {
    if (!sprite) return;
    if (!src) { sprite.removeAttribute('src'); return; }
    /* Guarded, because reassigning a `src` the element already has restarts the
       load and blanks the image for a frame — which on a run of same-pose cues
       would flicker her at exactly the moment she is meant to be holding still. */
    if (sprite.getAttribute('src') !== src) sprite.setAttribute('src', src);
  }

  function hide() {
    if (!layer) return;
    if (clearTimer) clearTimeout(clearTimer);
    /* Deferred, because a cue that stops is usually a cue that is about to be
       replaced: the engine cuts and re-cues inside the same tick, so hiding on
       the null would flicker the bubble shut and open again on every preempt. A
       new line cancels the hide before it lands. */
    clearTimer = setTimeout(function () {
      clearTimer = null;
      layer.classList.remove('is-on');
    }, 120);
  }

  function speak(name) {
    if (!layer || !show) return;
    if (clearTimer) { clearTimeout(clearTimer); clearTimer = null; }

    var pose = show.pose ? show.pose(name) : null;
    var src = pose && show.poses ? show.poses[pose] : null;
    var said = show.lines ? (show.lines[name] || null) : null;

    /* A cue the host has nothing drawn for and nothing to say about is not hers
       to stand up for — she stays down and the room has it to itself. */
    if (!src && !said) { hide(); return; }
    if (!src) src = show.sprite;

    setSprite(src);
    /* No empty glass rectangle over a host with no transcript: the panel is the
       line's, so it goes with the line. */
    bubble.style.display = said ? '' : 'none';
    if (said) line.textContent = said;

    layer.classList.add('is-on');
  }

  function wear(id) {
    show = HOSTS[id] || null;
    if (!layer) return;

    /* Swapped mid-line, which is what happens when someone changes show while a
       host is talking: the floor is cleared here and now rather than through
       `hide()`. That line is a transcript of the outgoing show's audio, so
       leaving it up would caption the incoming host with the outgoing host's
       words. Not deferred, for the same reason — the 120ms grace exists to
       survive a re-cue inside one show, and this is not that. */
    if (clearTimer) { clearTimeout(clearTimer); clearTimer = null; }
    layer.classList.remove('is-on');
    line.textContent = '';

    if (!show) { setSprite(null); return; }
    setSprite(show.sprite);
  }

  window.HostLayer = {
    /* Called by an edition as it loads, not on every change: a registration is
       static data. The re-wear is for the case where the edition it names is
       already the one on the floor — a course script is a later script than the
       registry, so a link that opened straight into it has already fired. */
    register: function (id, spec) {
      HOSTS[id] = spec;
      if (window.getEdition && window.getEdition() === id) wear(id);
    },
    speak: speak,
    hide: hide
  };

  document.addEventListener('editionchange', function (e) {
    wear(e.detail && e.detail.id);
  });

  /* The floor answers the engine's own cue rather than waiting to be told, so an
     edition only has to say who its host is. An edition that also needs the cue
     for its own reasons — the course runs an audio queue off the same signal —
     listens alongside this, not through it. */
  document.addEventListener('hostcue', function (e) {
    var name = e.detail && e.detail.name;
    if (name) speak(name); else hide();
  });

  /* ── MAIN's host ──────────────────────────────────────────────
     Five poses, cut from her sheet by `Tools/make_host_sprites.py`, and a rule
     that picks one from the name of the cue. The rule is written on prefixes
     rather than as a table of the thirty-five clips, so a line recorded later
     and dropped into the pool is drawn correctly without an edit here.

     No `lines`, deliberately: the clips exist and the transcript does not. Until
     it does she reacts in silence, which is the honest version of a room whose
     host was recorded saying things nobody wrote down. */
  var H = 'assets/host/tannaz-';
  var POSES = {
    greeting: H + 'greeting.png',
    right:    H + 'right.png',
    wrong:    H + 'wrong.png',
    timeout:  H + 'timeout.png',
    final:    H + 'final.png'
  };

  function poseFor(name) {
    if (name === 'opening_challenge') return 'greeting';
    if (name === 'host_correct') return 'right';
    /* Hand to the chin, looking away: the wager is the one beat where she is
       thinking about your chances rather than performing them. */
    if (name === 'host_wager') return 'timeout';
    if (name === 'host_final') return 'final';
    if (name.indexOf('right_') === 0) return 'right';
    if (name.indexOf('wrong_') === 0) return 'wrong';
    return null;
  }

  window.HostLayer.register('general', {
    sprite: POSES.greeting,
    poses: POSES,
    pose: poseFor
  });
})();
