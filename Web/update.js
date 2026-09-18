/* ── Is this a stale cut of the show? ────────────────────────────────────────
   One question to GitHub on boot: what is the newest release? If it is newer
   than the version this build was cut at, the lobby says so — quietly, in the
   margin — and Settings has the rest of it.

   Nothing here ever interrupts a game. A notice that halted a clue would be
   worse than the stale build it was warning about, so the answer only ever
   decorates a screen the player is already looking at.

   Failure is the ordinary case, not the exception: no network, a firewall, or
   GitHub throttled to a crawl all land on `unknown` and the show carries on
   exactly as it did before. There is deliberately no error a player can see —
   "we could not check for updates" is our problem, not theirs.

   The build's version is written here once and nowhere else. `build_release.sh`
   reads it out of this file for the bundle's CFBundleShortVersionString, and the
   corners in index.html are filled from it on boot, so a version bump is one
   edit and cannot end up comparing against a number the build is not.

   Contract:
     Update.version        the version this build was cut at, without the v
     Update.check()        ask GitHub; resolves to the state
     Update.state()        idle | checking | current | stale | unknown
     Update.latest()       the newest release number, without the v, or null
     Update.notesURL()     where to send a player for the newer cut
     Update.on('state', fn)  every change, including the first check
     Update.fill(root)     write the version into every [data-version] in a tree
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var VERSION = '1.0.12';

  var REPO = 'aghamorad/jeopardy-iranian-edition';
  var API = 'https://api.github.com/repos/' + REPO + '/releases/latest';
  var FALLBACK = 'https://github.com/' + REPO + '/releases/latest';

  /* GitHub answers, or it does not; a throttled connection can leave the request
     open for minutes. Nothing is waiting on the answer, so cut it loose and call
     that "unknown" rather than letting a check sit in flight for the whole game. */
  var TIMEOUT = 9000;

  var state = 'idle';
  var latest = null;
  var link = null;
  var handlers = {};
  var inFlight = null;

  function on(name, fn) { handlers[name] = fn; return U; }

  function fire() {
    var fn = handlers.state;
    if (!fn) return;
    try { fn(state, latest); }
    catch (err) { console.error('[update] handler threw', err); }
  }

  function set(next, tag, url) {
    state = next;
    /* Only overwrite what this call actually learned: a failure after a
       successful check must not erase the tag the player was already shown. */
    if (tag) latest = tag;
    if (url) link = url;
    fire();
  }

  /* '1.0.10' and 'v1.0.10' are the same number. A tag carrying more parts than we
     expect ('1.0.10.2') compares on the parts it has rather than throwing. */
  function parts(v) {
    return String(v).replace(/^v/i, '').split('.').map(function (n) {
      return parseInt(n, 10) || 0;
    });
  }

  function newer(a, b) {
    var x = parts(a), y = parts(b), i, len = Math.max(x.length, y.length);
    for (i = 0; i < len; i++) {
      var xi = x[i] || 0, yi = y[i] || 0;
      if (xi !== yi) return xi > yi;
    }
    return false;
  }

  function check() {
    if (inFlight) return inFlight;
    if (!window.fetch) { set('unknown'); return Promise.resolve(state); }

    set('checking');

    var give_up = null;
    var options = {
      /* The API's own media type: it is the documented way to ask, and it keeps
         the response on the versioned shape rather than whatever the default is. */
      headers: { Accept: 'application/vnd.github+json' },
      cache: 'no-store'
    };
    if (window.AbortController) {
      var ctl = new AbortController();
      options.signal = ctl.signal;
      give_up = setTimeout(function () { ctl.abort(); }, TIMEOUT);
    }

    inFlight = window.fetch(API, options)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        var tag = data && data.tag_name;
        if (!tag) throw new Error('no tag_name in the release');
        /* The tag arrives dressed as `v1.0.11`, and every string that shows it
           writes its own `v` in front. Keep the number here, so the copy owns
           the prefix and the two cannot double up. */
        var released = String(tag).replace(/^v/i, '');
        set(newer(released, VERSION) ? 'stale' : 'current', released,
          (data && data.html_url) || FALLBACK);
        return state;
      })
      .catch(function (err) {
        if (give_up) clearTimeout(give_up);
        console.warn('[update] check failed:', err && err.message);
        set('unknown');
        return state;
      })
      .then(function (result) {
        if (give_up) clearTimeout(give_up);
        inFlight = null;
        return result;
      });

    return inFlight;
  }

  function fill(root) {
    var scope = root || document;
    var n = scope.querySelectorAll('[data-version]');
    for (var i = 0; i < n.length; i++) n[i].textContent = 'v' + VERSION;
  }

  /* The show runs in a webview with no chrome, so a plain link would replace the
     game with a web page and offer no way back. Ask the shell to hand the address
     to the system browser instead; in a real browser, open normally. */
  function open(url) {
    var handlers_ = window.webkit && window.webkit.messageHandlers;
    var native = handlers_ && handlers_.links;
    if (native) {
      try { native.postMessage(url); return; }
      catch (err) { console.warn('[update] shell refused the link', err); }
    }
    window.open(url, '_blank', 'noopener');
  }

  var U = {
    version: VERSION,
    check: check,
    state: function () { return state; },
    latest: function () { return latest; },
    notesURL: function () { return link || FALLBACK; },
    on: on,
    fill: fill,
    open: open
  };

  window.Update = U;
})();
