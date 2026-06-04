'use strict';

const CACHE_NAME = 'droidify-v1780572183';
const STATIC_URLS  = [
  '/',
  '/index.html',
  '/devices.html',
  '/device.html',
  '/roms.html',
  '/recoveries.html',
  '/tools.html',
  '/guides.html',
  '/android.html',
  '/faq.html',
  '/terms.html',
  '/privacy.html',
  '/not-read',
  '/css/style.css',
  '/js/terms.js',
  '/js/nav.js',
  '/js/api.js',
  '/js/home.js',
  '/js/devices.js',
  '/js/device.js',
  '/js/roms.js',
  '/js/recoveries.js',
  '/js/tools.js',
  '/js/android.js',
  '/js/guides.js',
  '/manifest.json',
];

// Install — cache all static assets
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) { return cache.addAll(STATIC_URLS); })
      .then(function () { return self.skipWaiting(); })
  );
});

// Activate — delete old caches
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE_NAME; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

// Fetch — network first for API, cache first for assets
self.addEventListener('fetch', function (event) {
  const url = new URL(event.request.url);

  // Always go to network for API calls
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Cache first, fallback to network, then update cache
  event.respondWith(
    caches.match(event.request).then(function (cached) {
      const networkFetch = fetch(event.request).then(function (response) {
        if (response && response.status === 200 && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(event.request, clone);
          });
        }
        return response;
      }).catch(function () { return cached; });

      return cached || networkFetch;
    })
  );
});
