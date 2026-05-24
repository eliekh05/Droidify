// Droidify Service Worker
// NO fetch listener — intentional.
// Safari 17+ WebKit bug (bugs.webkit.org/261767): any fetch
// listener that calls event.respondWith() causes
// 'TypeError: Load failed' blocking the entire page load.
// Droidify has no cache and no offline mode.
// Without a fetch listener the browser handles all requests natively.
// This SW exists for: PWA installability, Background Sync, Periodic Sync.

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', e => e.waitUntil(
  caches.keys()
    .then(keys => Promise.all(keys.map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

// Background Sync — notify clients to retry last search when back online
self.addEventListener('sync', event => {
  if (event.tag === 'droidify-search-sync') {
    event.waitUntil(
      self.clients.matchAll({ type: 'window' })
        .then(clients => clients.forEach(c =>
          c.postMessage({ type: 'SYNC_COMPLETE' })
        ))
    );
  }
});

// Periodic Background Sync — warm the server cache once a day
self.addEventListener('periodicsync', event => {
  if (event.tag === 'droidify-refresh') {
    event.waitUntil(Promise.all([
      fetch('/api/devices?limit=1').catch(() => {}),
      fetch('/api/roms?limit=1').catch(() => {}),
    ]));
  }
});

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});
