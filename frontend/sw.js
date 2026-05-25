/**
 * Droidify Service Worker
 * Offline support: caches static assets and HTML pages.
 * API calls: network-first, fallback to cache.
 * Static assets: cache-first (CSS, JS, icons, fonts).
 */
const VERSION     = 'droidify-v2';
const STATIC_URLS = [
  '/',
  '/index.html',
  '/devices.html',
  '/device.html',
  '/roms.html',
  '/recoveries.html',
  '/tools.html',
  '/android.html',
  '/guides.html',
  '/privacy.html',
  '/css/style.css',
  '/js/api.js',
  '/js/reveal.js',
  '/js/nav.js',
  '/js/home.js',
  '/js/devices.js',
  '/js/device.js',
  '/js/roms.js',
  '/js/recoveries.js',
  '/js/tools.js',
  '/js/android.js',
  '/js/guides.js',
  '/manifest.json',
  '/favicon.svg',
  '/favicon.ico',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

// Install: cache all static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(VERSION)
      .then(cache => cache.addAll(STATIC_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate: delete old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== VERSION).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch strategy:
// - API requests: network-first, cache fallback
// - Static assets: cache-first, network fallback
// - HTML pages: network-first, cache fallback
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;

  // API — network first, cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(res => {
          // Cache successful API responses
          if (res.ok) {
            const clone = res.clone();
            caches.open(VERSION).then(cache => cache.put(event.request, clone));
          }
          return res;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Static assets (CSS, JS, images) — cache first
  if (
    url.pathname.startsWith('/css/') ||
    url.pathname.startsWith('/js/') ||
    url.pathname.startsWith('/icons/') ||
    url.pathname.match(/\.(png|ico|svg|woff2?)$/)
  ) {
    event.respondWith(
      caches.match(event.request)
        .then(cached => cached || fetch(event.request)
          .then(res => {
            const clone = res.clone();
            caches.open(VERSION).then(cache => cache.put(event.request, clone));
            return res;
          })
        )
    );
    return;
  }

  // HTML pages — network first, cache fallback, index.html last resort
  event.respondWith(
    fetch(event.request)
      .then(res => {
        const clone = res.clone();
        caches.open(VERSION).then(cache => cache.put(event.request, clone));
        return res;
      })
      .catch(() =>
        caches.match(event.request)
          .then(cached => cached || caches.match('/index.html'))
      )
  );
});

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});
