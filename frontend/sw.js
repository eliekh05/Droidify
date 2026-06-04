'use strict';

// Single persistent cache — never wiped, updated incrementally
const CACHE = 'droidify';

// URLs to pre-cache on install (only fetched if not already cached)
const PRECACHE = [
  '/css/style.css',
  '/js/terms.js',
  '/js/nav.js',
  '/js/home.js',
  '/js/device.js',
  '/manifest.json',
  '/favicon.svg',
];

// Install — cache any PRECACHE URLs not already stored
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(
        PRECACHE.map(function (url) {
          return cache.match(url).then(function (hit) {
            if (!hit) return cache.add(url).catch(function () {});
          });
        })
      );
    }).then(function () { return self.skipWaiting(); })
  );
});

// Activate — claim clients, no cache deletion
self.addEventListener('activate', function (e) {
  e.waitUntil(self.clients.claim());
});

// Fetch strategy:
// API calls            → always network
// HTML pages           → network first, cache fallback (always fresh content)
// CSS/JS with ?v=      → cache first (version param busts when changed)
// Everything else      → network first, update cache on success
self.addEventListener('fetch', function (e) {
  var url = new URL(e.request.url);

  // Skip non-GET and cross-origin
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  // API — always network
  if (url.pathname.startsWith('/api/') || url.pathname === '/not-read') {
    e.respondWith(fetch(e.request));
    return;
  }

  // Static assets with version param — cache first, update in background
  if (url.search.indexOf('v=') !== -1) {
    e.respondWith(
      caches.match(e.request).then(function (cached) {
        if (cached) {
          // Refresh in background
          fetch(e.request).then(function (fresh) {
            if (fresh && fresh.status === 200) {
              caches.open(CACHE).then(function (c) { c.put(e.request, fresh); });
            }
          }).catch(function () {});
          return cached;
        }
        return fetch(e.request).then(function (fresh) {
          if (fresh && fresh.status === 200) {
            var clone = fresh.clone();
            caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
          }
          return fresh;
        });
      })
    );
    return;
  }

  // HTML pages — network first, cache fallback
  if (url.pathname.endsWith('.html') || url.pathname === '/' ||
      !url.pathname.includes('.')) {
    e.respondWith(
      fetch(e.request).then(function (fresh) {
        if (fresh && fresh.status === 200) {
          var clone = fresh.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
        }
        return fresh;
      }).catch(function () {
        return caches.match(e.request).then(function (cached) {
          return cached || caches.match('/');
        });
      })
    );
    return;
  }

  // Everything else — network first, update cache
  e.respondWith(
    fetch(e.request).then(function (fresh) {
      if (fresh && fresh.status === 200) {
        var clone = fresh.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
      }
      return fresh;
    }).catch(function () {
      return caches.match(e.request);
    })
  );
});
