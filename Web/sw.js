/* ── The show, kept ──────────────────────────────────────────────────────────
   A match is a box of files, not a service. Everything it needs — both clue banks,
   every voice, every picture — is already in the tree, so the only thing between a
   player and a game with no network is that a browser has to be told to hold on to
   it.

   This worker carries no roster of its own. It keeps what the page asks for, as the
   page asks for it — which, once it holds the slot, means the boot pass's own warm
   fills the cache behind it: the show warms itself on the way in and is whole on the
   way back. The one thing that cannot be left to that is the code, because on a
   first visit the code is asked for before there is a worker to ask it of. That is
   what the install pass below is for.

   The invalidation contract is the project's own. Every asset URL already carries a
   `?v=` tag, and this matches on the whole URL including it. A moved file comes with
   a new tag, the tag is a miss, and the copy underneath cannot go stale — including
   between two builds that share a version number, which is why nothing here has to
   trust the cache name to be right.

   Register with the version in the address (`sw.js?v=1.0.17`). The name is read back
   out of that query, so a new cut lands on a new cache and `activate` clears the old
   one on the way past.
   ─────────────────────────────────────────────────────────────────────────── */

var VERSION = (function () {
  var found = /[?&]v=([^&]+)/.exec(self.location.href);
  return found ? decodeURIComponent(found[1]) : '0';
})();

var CACHE = 'jeopardy-' + VERSION;

/* The page itself, for a request that arrives with no network at all. Everything
   else can lose and be fetched again; the shell cannot, because it is the thing
   that would do the fetching. */
var SHELL = [self.registration.scope, self.registration.scope + 'index.html'];

var SCOPE = self.registration.scope;
var ORIGIN = new URL(SCOPE).origin;

/* ── The first visit has to be enough ────────────────────────────────────────
   The page warms its own library on the way in, and on anything after the first
   visit every one of those requests passes through this worker and is kept. On the
   first visit it does not: the markup is parsed and the code is asked for in the
   first hundred milliseconds, which is before this worker has been installed,
   let alone given the slot. So the runtime cache ends up holding every voice and
   every picture and *none* of the code — a page that comes back offline with its
   cast and no script to run them.

   Hence this pass, run before the worker will take the slot. It reads the markup
   it is about to serve and keeps what the markup names: the document, every script
   and stylesheet and picture the page itself refers to, and the pictures the
   stylesheets refer to on their behalf. Read out of the files rather than written
   down here, because a script tag added to the show is a file this has to hold, and
   a list kept in two places is a list that goes stale in one of them.

   Nothing in here is allowed to fail the install. A file that will not come is not
   worth a worker that will not start. */

function same(text, base) {
  if (!text || text.charAt(0) === '#') return null;
  if (/^data:|^blob:/i.test(text)) return null;
  try {
    var made = new URL(text, base || SCOPE);
    return made.origin === ORIGIN ? made.href : null;
  } catch (err) { return null; }
}

function keep(cache, url) {
  return fetch(url).then(function (response) {
    if (response && response.status === 200 && response.type === 'basic') {
      return cache.put(url, response);
    }
  }).catch(function () {});
}

/* What the markup names, and which of those are stylesheets with pictures of
   their own. */
function named(html) {
  var files = [SCOPE, SCOPE + 'index.html'];
  var sheets = [];
  var tag = /<(?:script|link|img)\b[^>]*?\s(?:src|href)\s*=\s*["']([^"']+)["']/gi;
  var m;
  while ((m = tag.exec(html))) {
    var url = same(m[1]);
    if (!url || files.indexOf(url) >= 0) continue;
    files.push(url);
    if (/\.css(?:[?#]|$)/i.test(url)) sheets.push(url);
  }
  return { files: files, sheets: sheets };
}

/* The door's backdrop, the lens map, the figure at the foot of the stage: named in
   a stylesheet and nowhere else, and all of them furniture of a screen a player is
   looking at while the network is still being decided. */
function wardrobe(cache, url) {
  return fetch(url).then(function (response) {
    return response && response.ok ? response.text() : '';
  }).then(function (css) {
    var art = /url\(\s*["']?([^"')]+)["']?\s*\)/gi;
    var m, jobs = [];
    while ((m = art.exec(css))) {
      var made = same(m[1], url);
      if (made) jobs.push(keep(cache, made));
    }
    return Promise.all(jobs);
  }).catch(function () {});
}

function precache() {
  return caches.open(CACHE).then(function (cache) {
    return fetch(SCOPE + 'index.html').then(function (response) {
      return response && response.ok ? response.text() : '';
    }).catch(function () { return ''; }).then(function (html) {
      var kit = named(html);
      var jobs = kit.files.map(function (url) { return keep(cache, url); });
      return Promise.all(jobs.concat(kit.sheets.map(function (url) {
        return wardrobe(cache, url);
      })));
    });
  });
}

self.addEventListener('install', function (event) {
  /* A waiting worker is a player waiting to be allowed to play offline. Take the
     slot as soon as this one is ready and let `activate` do the tidying — but only
     once the show is in hand. */
  event.waitUntil(
    precache().then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (names) {
        return Promise.all(names.map(function (name) {
          return name === CACHE ? null : caches.delete(name);
        }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

/* The shell, whether the request named it or not — a `?ed=` link, a bare directory,
   an address typed by hand. Search is ignored here deliberately: the same document
   answers for all of them. */
function shell(cache) {
  return cache.match(SHELL[1], { ignoreSearch: true })
    .then(function (hit) { return hit || cache.match(SHELL[0], { ignoreSearch: true }); });
}

/* One request, three questions in this order: is it already kept; can the network
   answer; and failing both, is there anything close enough to do instead of
   nothing.

   The exact match first is the part that keeps the tags honest. While there is a
   network, a file whose tag has moved is a miss, is fetched, and is stored under
   its new name — so a re-recorded voice can never be answered with the take it
   replaced. The tag is only allowed to stop mattering once the network is gone,
   because a voice one take out of date is worth more to a player with no signal
   than the silence the alternative is. */
function serve(request) {
  return caches.open(CACHE).then(function (cache) {
    return cache.match(request).then(function (hit) {
      if (hit) return hit;

      return fetch(request).then(function (response) {
        /* A copy, because the original is on its way back to the page — and only a
           whole one. A range request answered with a 206 cannot be stored, and a
           player who seeks inside a voice should not have their part-file kept as
           if it were the whole of it. */
        if (response && response.status === 200 && response.type === 'basic') {
          cache.put(request, response.clone()).catch(function () {});
        }
        return response;
      }).catch(function (err) {
        if (request.mode === 'navigate') {
          return shell(cache).then(function (fallback) {
            if (fallback) return fallback;
            throw err;
          });
        }
        /* Nothing kept under that exact name. The same path under another tag is
           the best answer there is, and it is only ever reached from here. */
        return cache.match(request, { ignoreSearch: true }).then(function (loose) {
          if (loose) return loose;
          throw err;
        });
      });
    });
  });
}

self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') return;

  var url = new URL(request.url);
  /* Off-origin is somebody else's business and none of it is worth keeping: the
     release check on GitHub, the introductions server the online table needs. Both
     already fail without complaint, and neither should be answered from a cache. */
  if (url.origin !== self.location.origin) return;

  event.respondWith(serve(request));
});
