/* ── The wire ────────────────────────────────────────────────────────────────
   Transport for the online table. Knows nothing about the game.

   One player's browser is the host; it owns the board, the clocks and the
   rulings. Everyone else opens the same page, types the room code, and gets a
   controller. There is no server of ours in the middle — the free PeerJS broker
   only introduces the two ends, and after that the browsers talk to each other
   directly.

   Messages are small JSON objects. The shape is the game's business, not this
   file's: everything above arrives unexamined through on('message', …).

   Contract:
     Net.on(name, fn)      ready | join | leave | message | connected | closed | error
     Net.host(code)        become the table
     Net.join(code, name, cid)  sit down at someone else's; cid is who you are
                           across a reconnection, and it is what lets the host
                           give you your own seat and score back.
     Net.emit(msg)         host → every guest, guest → host
     Net.close()           tear it all down
     Net.code()            a fresh four-character room code
     Net.supported()       does this browser have WebRTC at all
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  /* PeerJS's own default ICE list is Google STUN and nothing else. Do not
     inherit it: name the servers explicitly so the list is ours to change. */
  var ICE = {
    iceServers: [
      { urls: ['stun:stun.l.google.com:19302', 'stun:stun1.l.google.com:19302'] },
      { urls: ['stun:stun.cloudflare.com:3478'] },
      { urls: ['stun:stun.nextcloud.com:3478'] }
      /* Some pairs of networks — both ends behind a symmetric NAT — cannot be
         introduced to each other without a relay. Put a TURN server here and
         those pairs connect too:

         { urls: 'turn:your.host:3478', username: '…', credential: '…' }      */
    ]
  };

  var PREFIX = 'jpd-ir-';

  /* I, O, 0 and 1 are out: a room code gets read aloud and typed by somebody
     who is not looking at the screen. */
  var ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

  var N = {
    role: null,   /* 'host' or 'guest' */
    code: null,
    peer: null,
    conns: {},    /* the host's table: peerId → connection */
    up: null,     /* the guest's single line to the host */
    ready: false
  };

  var handlers = {};

  function on(name, fn) { handlers[name] = fn; return N; }

  function fire(name, a, b) {
    var fn = handlers[name];
    if (!fn) return;
    try { fn(a, b); }
    catch (err) { console.error('[net] handler "' + name + '" threw', err); }
  }

  function supported() {
    return !!(window.RTCPeerConnection && window.Peer && window.Peer.prototype);
  }

  function code() {
    var out = '';
    for (var i = 0; i < 4; i++) out += ALPHABET.charAt(Math.floor(Math.random() * ALPHABET.length));
    return out;
  }

  /* Signalling is the one thing that has to reach the network. If the broker is
     unreachable the two browsers have no way to find each other, so say so in
     words rather than letting a bare 'error' event drift up. */
  function explain(err, prefix) {
    var kind = err && err.type;
    var line = prefix || '';
    if (kind === 'peer-unavailable') return 'No table answering to that code.';
    if (kind === 'unavailable-id') return 'That code is taken. Try again.';
    if (kind === 'browser-incompatible') return 'This browser has no WebRTC.';
    if (kind === 'network' || kind === 'server-error' || kind === 'socket-error') {
      return 'Could not reach the introductions server. Check the connection.';
    }
    return line || (err && err.message) || 'Something went wrong.';
  }

  function listen(peer, source, event, fn) {
    source.on(event, function () {
      if (N.peer === peer) fn.apply(null, arguments);
    });
  }

  function host(roomCode) {
    close();
    N.role = 'host';
    N.code = roomCode;

    var peer = new window.Peer(PREFIX + roomCode, { config: ICE, debug: 1 });
    N.peer = peer;

    listen(peer, peer, 'open', function () { N.ready = true; fire('ready', roomCode); });

    listen(peer, peer, 'connection', function (conn) {
      listen(peer, conn, 'open', function () {
        N.conns[conn.peer] = conn;
        fire('join', conn.peer, conn.metadata || {});
      });
      listen(peer, conn, 'data', function (data) { fire('message', conn.peer, data); });
      listen(peer, conn, 'close', function () {
        delete N.conns[conn.peer];
        fire('leave', conn.peer);
      });
      listen(peer, conn, 'error', function (err) { fire('error', explain(err)); });
    });

    listen(peer, peer, 'error', function (err) {
      /* A browser tab that goes away leaves its id in the broker for a moment.
         Retrying once under a fresh code is friendlier than a dead button. */
      fire('error', explain(err, err && err.type === 'unavailable-id'
        ? 'That code is taken. Try again.' : ''));
    });

    return N;
  }

  function join(roomCode, name, cid) {
    close();
    N.role = 'guest';
    N.code = roomCode;

    var peer = new window.Peer(null, { config: ICE, debug: 1 });
    N.peer = peer;

    listen(peer, peer, 'open', function () {
      var conn = peer.connect(PREFIX + roomCode, {
        reliable: true,
        metadata: { name: name || '', cid: cid || '' }
      });
      N.up = conn;

      listen(peer, conn, 'open', function () {
        N.ready = true;
        fire('connected', roomCode);
        sendUp({ t: 'hello', name: name || '', cid: cid || '' });
      });
      listen(peer, conn, 'data', function (data) { fire('message', data); });
      listen(peer, conn, 'close', function () { N.ready = false; fire('closed'); });
      listen(peer, conn, 'error', function (err) { fire('error', explain(err)); });
    });

    listen(peer, peer, 'error', function (err) { fire('error', explain(err)); });

    return N;
  }

  function send(msg) {
    var ids = Object.keys(N.conns);
    for (var i = 0; i < ids.length; i++) {
      try { N.conns[ids[i]].send(msg); }
      catch (err) { console.warn('[net] dropped for ' + ids[i], err); }
    }
  }

  function sendTo(peerId, msg) {
    var conn = N.conns[peerId];
    if (!conn) return;
    try { conn.send(msg); }
    catch (err) { console.warn('[net] dropped for ' + peerId, err); }
  }

  function sendUp(msg) {
    if (!N.up) return;
    try { N.up.send(msg); }
    catch (err) { console.warn('[net] dropped to host', err); }
  }

  /* One verb, whichever end you are on. */
  function emit(msg) {
    if (N.role === 'host') send(msg); else sendUp(msg);
  }

  function close() {
    var peer = N.peer;
    N.peer = null;
    if (peer) { try { peer.destroy(); } catch (err) { /* already gone */ } }
    N.conns = {};
    N.up = null;
    N.ready = false;
    N.role = null;
    N.code = null;
  }

  window.Net = {
    on: on,
    host: host,
    join: join,
    emit: emit,
    send: send,
    sendTo: sendTo,
    close: close,
    code: code,
    supported: supported,
    state: N,
    peers: function () { return Object.keys(N.conns); }
  };
})();
