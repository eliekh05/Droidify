'use strict';

const CACHE        = 'droidify';
const OFFLINE_URL  = '/offline.html';

// Pre-cache these on install — MUST include '/' and OFFLINE_URL
// so PWABuilder/Chrome offline check always gets a valid response
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

// Install — force-cache '/' and offline.html, skip others if already cached
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      // Always re-fetch the critical pages on install
      var critical = [cache.put('/', fetch('/')), cache.put(OFFLINE_URL, fetch(OFFLINE_URL))];
      var rest = PRECACHE.filter(function (u) { return u !== '/' && u !== OFFLINE_URL; })
        .map(function (url) {
          return cache.match(url).then(function (hit) {
            if (!hit) return cache.add(url).catch(function () {});
          });
        });
      return Promise.all(critical.concat(rest).map(function (p) {
        return p.catch(function () {});  // never let install fail
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

// Activate — claim clients immediately
self.addEventListener('activate', function (e) {
  e.waitUntil(self.clients.claim());
});

// Fetch strategies:
//  API calls          → always network (never cache)
//  CSS/JS with ?v=    → cache-first, background refresh (version busting)
//  HTML navigation    → network-first, cache fallback, offline.html last resort
//  Everything else    → network-first, cache on success
self.addEventListener('fetch', function (e) {
  var req = e.request;
  var url = new URL(req.url);

  // Skip non-GET and cross-origin requests
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  // API — always network, never cache
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

  // Versioned static assets — cache-first, background refresh
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

  // HTML navigation — network-first, cache fallback, offline.html last resort
  var isNavigation = req.mode === 'navigate' ||
    url.pathname.endsWith('.html') ||
    url.pathname === '/' ||
    !url.pathname.includes('.');

  if (isNavigation) {
    e.respondWith(
      fetch(req).then(function (fresh) {
        if (fresh && fresh.status === 200) {
          var clone = fresh.clone();
          caches.open(CACHE).then(function (c) { c.put(req, clone); });
        }
        return fresh;
      }).catch(function () {
        return caches.match(req)
          .then(function (cached) { return cached || caches.match(OFFLINE_URL); })
          .then(function (page)   { return page   || caches.match('/'); });
      })
    );
    return;
  }

  // Everything else — network-first, cache on success
  e.respondWith(
    fetch(req).then(function (fresh) {
      if (fresh && fresh.status === 200) {
        var clone = fresh.clone();
        caches.open(CACHE).then(function (c) { c.put(req, clone); });
      }
      return fresh;
    }).catch(function () {
      return caches.match(req);
    })
  );
});
