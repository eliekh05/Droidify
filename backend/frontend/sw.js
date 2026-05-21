const STATIC_CACHE = 'droidify-static-v4';
const API_CACHE    = 'droidify-api-v2';

const PRECACHE_URLS = [
  '/','/index.html','/devices.html','/device.html','/roms.html',
  '/recoveries.html','/tools.html','/android.html','/guides.html','/404.html',
  '/css/style.css','/js/api.js','/js/home.js','/js/devices.js',
  '/js/device-detail.js','/js/roms.js','/js/recoveries.js','/js/tools.js',
  '/js/android.js','/js/guides.js','/favicon.svg','/manifest.json',
  '/icons/icon-192.png','/icons/icon-512.png',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  const keep = [STATIC_CACHE, API_CACHE];
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => !keep.includes(k)).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET') return;

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request, API_CACHE));
    return;
  }
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(request) || caches.match('/index.html'))
    );
    return;
  }
  event.respondWith(cacheFirst(request, STATIC_CACHE));
});

async function cacheFirst(req, cacheName) {
  const cached = await caches.match(req);
  if (cached) return cached;
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(cacheName)).put(req, res.clone());
    return res;
  } catch { return new Response('offline', { status: 503 }); }
}

async function networkFirst(req, cacheName) {
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(cacheName)).put(req, res.clone());
    return res;
  } catch {
    return await caches.match(req) ||
      new Response(JSON.stringify({ error: 'offline' }), {
        status: 503, headers: { 'Content-Type': 'application/json' }
      });
  }
}

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});
