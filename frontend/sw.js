'use strict';

const CACHE       = 'droidify';
const OFFLINE_URL = '/offline.html';

const PRECACHE = [
  '/',
  '/offline.html',
  '/css/style.css',
  '/js/terms.js',
  '/js/nav.js',
  '/js/home.js',
  '/manifest.json',
  '/favicon.svg',
];

// ── Message handler (from PWABuilder) — allows clients to trigger SW update ──
self.addEventListener('message', function (event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// ── Install — force-cache / and offline.html, pre-cache rest ─────────────────
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      var critical = [
        cache.put('/', fetch('/')),
        cache.put(OFFLINE_URL, fetch(OFFLINE_URL))
      ];
      var rest = PRECACHE
        .filter(function (u) { return u !== '/' && u !== OFFLINE_URL; })
        .map(function (url) {
          return cache.match(url).then(function (hit) {
            if (!hit) return cache.add(url).catch(function () {});
          });
        });
      return Promise.all(
        critical.concat(rest).map(function (p) { return p.catch(function () {}); })
      );
    }).then(function () { return self.skipWaiting(); })
  );
});

// ── Activate — enable navigation preload (from PWABuilder) + claim clients ───
self.addEventListener('activate', function (e) {
  e.waitUntil(
    Promise.all([
      self.clients.claim(),
      // Navigation preload speeds up navigation requests on supporting browsers
      self.registration.navigationPreload
        ? self.registration.navigationPreload.enable()
        : Promise.resolve()
    ])
  );
});

// ── Fetch ─────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', function (e) {
  var req = e.request;
  var url = new URL(req.url);

  // Skip non-GET and cross-origin
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  // API — always network, 503 JSON when offline
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(req).catch(function () {
        return new Response(JSON.stringify({ error: 'offline' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // Versioned static assets (?v=) — cache-first, background refresh
  if (url.search.indexOf('v=') !== -1) {
    e.respondWith(
      caches.match(req).then(function (cached) {
        var networkFetch = fetch(req).then(function (fresh) {
          if (fresh && fresh.status === 200) {
            caches.open(CACHE).then(function (c) { c.put(req, fresh.clone()); });
          }
          return fresh;
        }).catch(function () { return cached; });
        return cached || networkFetch;
      })
    );
    return;
  }

  // HTML navigation — use preload response if available (from PWABuilder),
  // then network, then cache, then offline.html
  var isNavigation = req.mode === 'navigate' ||
    url.pathname.endsWith('.html') ||
    url.pathname === '/' ||
    !url.pathname.includes('.');

  if (isNavigation) {
    e.respondWith((async function () {
      try {
        // Navigation preload (PWABuilder pattern) — parallel network request
        var preload = await e.preloadResponse;
        if (preload) {
          caches.open(CACHE).then(function (c) { c.put(req, preload.clone()); });
          return preload;
        }
        var fresh = await fetch(req);
        if (fresh && fresh.status === 200) {
          caches.open(CACHE).then(function (c) { c.put(req, fresh.clone()); });
        }
        return fresh;
      } catch (_) {
        var cached = await caches.match(req);
        if (cached) return cached;
        var offline = await caches.match(OFFLINE_URL);
        if (offline) return offline;
        return caches.match('/');
      }
    })());
    return;
  }

  // Everything else — network-first, cache on success
  e.respondWith(
    fetch(req).then(function (fresh) {
      if (fresh && fresh.status === 200) {
        caches.open(CACHE).then(function (c) { c.put(req, fresh.clone()); });
      }
      return fresh;
    }).catch(function () {
      return caches.match(req);
    })
  );
});
