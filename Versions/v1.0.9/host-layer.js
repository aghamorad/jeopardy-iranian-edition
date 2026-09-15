/* ── The host on the floor ──────────────────────────────────────
   Whichever show is running, one figure stands at the foot of the stage while
   the room is quiet. That figure is page furniture rather than course property:
   MAIN has Tannaz Hearsay, a course brings its own, and both want the same
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

  /* The two switches the match menu owns, and they are not the same switch.
     `sprites` is whether she is on the floor at all; `voice` is whether
     anything is coming out of her. Held here rather than read from `Sound`,
     because one of them is about a drawing and the other is about a caption
     and neither is about an audio element. */
  var showSprites = true;
  var hostVoice = true;

  (function build() {
    var host = document.getElementById('app');
    if (!host) return;

    layer = document.createElement('div');
    layer.id = 'host-layer';
    layer.setAttribute('aria-hidden', 'true');

    bubble = document.createElement('div');
    bubble.className = 'host-bubble';

    line = document.createElement('p');
    line.className = 'host-caption';
    /* The lines are English because the clips are English, whichever language
       the game is being played in. Marked, so the browser and a reader both take
       the line left-to-right inside a Persian page rather than guessing. */
    line.setAttribute('lang', 'en');
    line.setAttribute('dir', 'ltr');
    bubble.appendChild(line);

    sprite = document.createElement('img');
    sprite.className = 'host-sprite';
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
       to stand up for — she stays down and the room has it to itself. Asked
       before the switches, not after: a host with neither sprite nor line is
       hidden whatever the menu says, and reading it the other way round would
       let a switch turn a non-cue into a cue. */
    if (!src && !said) { hide(); return; }

    /* Switched off, she does not come out. Checked before the fallback sprite
       so the resting pose is not worn while the layer is meant to be empty. */
    if (!showSprites) return;
    if (!src) src = show.sprite;

    /* Her voice switched off takes the bubble with it — the bubble is a
       transcript of audio, and there is no audio. She is still drawn, because
       `sprites` is the switch that owns the drawing. */
    if (!hostVoice) said = null;

    setSprite(src);
    /* No empty glass rectangle over a host with no transcript: the panel is the
       line's, so it goes with the line. */
    bubble.style.display = said ? '' : 'none';
    line.textContent = said || '';

    layer.classList.add('is-on');
  }

  /* The match menu's two switches, set together because they are set from one
     place and a half-applied pair would be a frame of the wrong show. Both
     affect a line that is already up: hiding the sprites while she is talking
     takes the figure and the bubble away and clears the transcript, and muting
     her takes the bubble away and leaves her standing there — the same rule
     `speak` applies, applied to the cue already on the floor rather than to the
     next one. The floor is not given a grace period here; this is a switch, not
     a re-cue. */
  function setStage(next) {
    var sprites = next && next.sprites !== undefined ? !!next.sprites : showSprites;
    var voice = next && next.voice !== undefined ? !!next.voice : hostVoice;
    var changed = sprites !== showSprites || voice !== hostVoice;
    showSprites = sprites;
    hostVoice = voice;
    if (!changed || !layer) return;

    if (!showSprites) {
      if (clearTimer) { clearTimeout(clearTimer); clearTimer = null; }
      layer.classList.remove('is-on');
      line.textContent = '';
      bubble.style.display = 'none';
      return;
    }
    if (!hostVoice) {
      line.textContent = '';
      bubble.style.display = 'none';
    }
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
    hide: hide,
    /* `{sprites: bool, voice: bool}`; an omitted key keeps its current value, so
       a caller can flip one without having to know the other. */
    setStage: setStage
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
     rather than as a table of the thirty-six clips, so a line recorded later
     and dropped into the pool is drawn correctly without an edit here.

     `lines` is a transcription of the clips themselves. The words were never
     written down anywhere — each clip was named after its own punchline and the
     script behind it is gone — so every row here came out of the audio, via
     `Tools/transcribe_host.swift` and Apple's on-device speech model. Two runs
     at different sample rates agreed word for word on thirty-five of the
     thirty-six, which is the only reason this table is worth trusting; the
     three places the audio is genuinely ambiguous are called out at their rows.

     It follows that a row must not be rewritten to taste. The bubble captions
     audio a player can hear, so a line edited for rhythm or polish is a bubble
     that misquotes the speaker to her face. If a line reads oddly, the audio is
     what is odd. Re-transcribe the clip, don't re-word it. */
  var H = 'assets/host/tannaz-';
  var POSES = {
    greeting: H + 'greeting.png',
    right:    H + 'right.png',
    wrong:    H + 'wrong.png',
    timeout:  H + 'timeout.png',
    final:    H + 'final.png'
  };

  function poseFor(name) {
    if (name === 'tannaz_opening_challenge') return 'greeting';
    if (name === 'tannaz_correct') return 'right';
    /* Hand to the chin, looking away: the wager is the one beat where she is
       thinking about your chances rather than performing them. */
    if (name === 'tannaz_wager') return 'timeout';
    if (name === 'tannaz_final') return 'final';
    if (name.indexOf('tannaz_right_') === 0) return 'right';
    if (name.indexOf('tannaz_wrong_') === 0) return 'wrong';
    return null;
  }

  /* Keyed the way the engine names a cue, which for a verdict is the whole slug
     out of the pools in `app.js` and not the number in front of it — the bubble
     is handed `tannaz_right_08_tehran_survives_another_round` and has nothing but that
     string to look itself up with. The scene cues below are the four the engine
     calls by their own names.

     Only cues that have a clip behind them are listed: the twelve `right_17`+
     and twelve `wrong_17`+ lines from the script have no audio in the tree and
     are absent from the pools, so a line here would caption silence. */
  var LINES = {
    tannaz_opening_challenge: 'All right, fuckers. Every Iranian with a pulse thinks they\'re a historian, a political analyst, and the smartest bastard in the room. Wonderful. Now shut up and prove it. Let\'s see how much of that confidence survives the first five questions.',

    tannaz_correct: 'Correct, well played. The next choice is yours.',
    tannaz_wager:   'A sealed wager. The board can wait. How much are you prepared to risk?',
    tannaz_final:   'This is final, thirty seconds, one answer, make it count.',

    tannaz_right_01_well_look_at_you: 'Well, look at you, you actually knew one.',
    /* The rise on "Correct?" is hers, not a question I typed: the model hears it
       on right_02, right_10 and right_13 alike, on every pass. */
    tannaz_right_02_try_not_to_become_unbearable: 'Correct? Try not to become unbearable.',
    tannaz_right_03_mashallah_an_actual_fact: 'Mashallah, a fact, an actual fact.',
    tannaz_right_04_confidence_matched_the_answer: 'Oh, good. The confidence finally matched the answer.',
    tannaz_right_05_please_remain_humble: 'Correct. Please remain humble. I know that\'s difficult.',
    tannaz_right_06_actual_knowledge_how_refreshing: 'There it is, actual knowledge. How refreshing.',
    tannaz_right_07_tell_your_uncle: 'Well done. Go tell your uncle he raised you right.',
    /* Heard as "Teh" and, on the resampled pass, "Terran". The clue is in the
       filename and she says the word plainly elsewhere; this is the model. */
    tannaz_right_08_tehran_survives_another_round: 'Correct. Tehran survives another round.',
    tannaz_right_09_annoyingly_good: 'Very good. Annoyingly good actually.',
    tannaz_right_10_i_hate_how_pleased_you_look: 'Correct? I hate how pleased you look.',
    tannaz_right_11_not_just_opinions_after_all: 'Look at that, not just opinions after all.',
    tannaz_right_12_unfortunately_youre_right: 'Yes, unfortunately you\'re right.',
    tannaz_right_13_dont_get_used_to_this_feeling: 'Correct? Don\'t get used to this feeling.',
    tannaz_right_14_four_thousand_years_finally_correct: 'Four thousand years of civilization, and finally, a correct answer.',
    tannaz_right_15_try_not_to_explain_it_to_everyone: 'Perfect. Now try not to explain it to everyone.',
    tannaz_right_16_you_may_be_smug_for_five_seconds: 'Correct, fine. You may be smug for five seconds.',

    /* Heard as "Michelle" — a glitch on a word the same model gets right in
       right_03 and wrong_08, and the filename is the word. */
    tannaz_wrong_01_mashallah_the_confidence: 'Mashallah, the confidence.',
    tannaz_wrong_02_very_iranian_of_you: 'Very Iranian of you, completely sure, completely wrong.',
    tannaz_wrong_03_no_facts_full_confidence: 'No facts, full confidence, beautiful.',
    tannaz_wrong_04_dinner_party: 'You\'ve definitely argued about this at a dinner party.',
    tannaz_wrong_05_family_whatsapp: 'Oh, that sounded much better in your family WhatsApp group.',
    tannaz_wrong_06_source_your_uncle: 'Source? Your uncle said so?',
    /* Heard flat as "no later", on every pass and at three tempos. "Know
       later" is the same phonemes and the only reading that is a sentence. */
    tannaz_wrong_07_iranian_method: 'Ah, yes, the Iranian method. Answer first, know later.',
    tannaz_wrong_08_mashallah_you_have_opinions: 'You don\'t know, but Mashallah, you do have opinions.',
    tannaz_wrong_09_tehran_taxi_driver: 'Wrong, but wow, delivered with the confidence of a Tehran taxi driver.',
    tannaz_wrong_10_iranian_uncle_nodding: 'Somewhere, an Iranian uncle is nodding along with you.',
    tannaz_wrong_11_national_tradition: 'Congratulations. You\'ve turned guessing into a national tradition.',
    /* No verb where a verb goes. Nothing audible between "confidence" and
       "world", across five passes, so nothing is written in for it. */
    tannaz_wrong_12_world_class_confidence: 'Not even close, but the confidence world class.',
    tannaz_wrong_13_four_thousand_years: 'Four thousand years of civilization, and this is your answer?',
    tannaz_wrong_14_cyrus_the_great: 'Cyrus the Great did not die for this.',
    tannaz_wrong_15_dinner_fact: 'Please do not tell everyone at dinner. This is a fact.',
    tannaz_wrong_16_explain_it_loudly: 'Perfect. Now go explain it loudly to everyone else.'
  };

  window.HostLayer.register('general', {
    sprite: POSES.greeting,
    poses: POSES,
    pose: poseFor,
    lines: LINES
  });
})();
