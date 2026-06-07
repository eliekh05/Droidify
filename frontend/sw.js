// This is the service worker with the combined offline experience (Offline page + Offline copy of pages)

const CACHE = 'droidify';
const offlineFallbackPage = '/offline.html';

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

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('install', async (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => {
      // Force-cache / and offline.html on every install
      var critical = [
        cache.put('/', fetch('/')),
        cache.put(offlineFallbackPage, fetch(offlineFallbackPage))
      ];
      var rest = PRECACHE
        .filter((u) => u !== '/' && u !== offlineFallbackPage)
        .map((url) => cache.match(url).then((hit) => {
          if (!hit) return cache.add(url).catch(() => {});
        }));
      return Promise.all(
        critical.concat(rest).map((p) => p.catch(() => {}))
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', async (event) => {
  event.waitUntil(
    Promise.all([
      self.clients.claim(),
      self.registration.navigationPreload
        ? self.registration.navigationPreload.enable()
        : Promise.resolve()
    ])
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET and cross-origin
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  // API — always network, 503 JSON when offline
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(req).catch(() =>
        new Response(JSON.stringify({ error: 'offline' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        })
      )
    );
    return;
  }

  // Versioned static assets (?v=) — cache-first, background refresh
  if (url.search.indexOf('v=') !== -1) {
    event.respondWith(
      caches.match(req).then((cached) => {
        const networkFetch = fetch(req).then((fresh) => {
          if (fresh && fresh.status === 200)
            caches.open(CACHE).then((c) => c.put(req, fresh.clone()));
          return fresh;
        }).catch(() => cached);
        return cached || networkFetch;
      })
    );
    return;
  }

  // HTML navigation — preload response first, then network, then cache, then offline page
  const isNavigation = req.mode === 'navigate' ||
    url.pathname.endsWith('.html') ||
    url.pathname === '/' ||
    !url.pathname.includes('.');

  if (isNavigation) {
    event.respondWith((async () => {
      try {
        const preloadResp = await event.preloadResponse;
        if (preloadResp) {
          caches.open(CACHE).then((c) => c.put(req, preloadResp.clone()));
          return preloadResp;
        }
        const networkResp = await fetch(req);
        if (networkResp && networkResp.status === 200)
          caches.open(CACHE).then((c) => c.put(req, networkResp.clone()));
        return networkResp;
      } catch (error) {
        const cached = await caches.match(req);
        if (cached) return cached;
        const offline = await caches.match(offlineFallbackPage);
        if (offline) return offline;
        return caches.match('/');
      }
    })());
    return;
  }

  // Everything else — network-first, cache on success
  event.respondWith(
    fetch(req).then((fresh) => {
      if (fresh && fresh.status === 200)
        caches.open(CACHE).then((c) => c.put(req, fresh.clone()));
      return fresh;
    }).catch(() => caches.match(req))
  );
});
