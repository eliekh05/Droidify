'use strict';

const CACHE = 'droidify';

const PRECACHE = [
  '/',
  '/css/style.css',
  '/js/terms.js',
  '/js/nav.js',
  '/js/home.js',
  '/manifest.json',
  '/favicon.svg',
];

self.addEventListener('message', function (event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      var critical = [cache.put('/', fetch('/'))];
      var rest = PRECACHE
        .filter(function (u) { return u !== '/'; })
        .map(function (url) { return cache.add(url).catch(function () {}); });
      return Promise.all(
        critical.concat(rest).map(function (p) { return p.catch(function () {}); })
      );
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    Promise.all([
      self.clients.claim(),
      self.registration.navigationPreload
        ? self.registration.navigationPreload.enable()
        : Promise.resolve()
    ])
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  var url = new URL(req.url);

  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  if (url.pathname.startsWith('/api/')) {
    e.respondWith(fetch(req));
    return;
  }

  if (url.search.indexOf('v=') !== -1) {
    e.respondWith(
      caches.match(req).then(function (cached) {
        var networkFetch = fetch(req).then(function (fresh) {
          if (fresh && fresh.status === 200)
            caches.open(CACHE).then(function (c) { c.put(req, fresh.clone()); });
          return fresh;
        }).catch(function () { return cached; });
        return cached || networkFetch;
      })
    );
    return;
  }

  e.respondWith(
    (async function () {
      try {
        var preload = await e.preloadResponse;
        if (preload) {
          caches.open(CACHE).then(function (c) { c.put(req, preload.clone()); });
          return preload;
        }
        var fresh = await fetch(req);
        if (fresh && fresh.status === 200)
          caches.open(CACHE).then(function (c) { c.put(req, fresh.clone()); });
        return fresh;
      } catch (_) {
        return caches.match(req);
      }
    })()
  );
});
