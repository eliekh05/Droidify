/**
 * Droidify nav.js
 * - Mobile hamburger
 * - PWA install
 * - Connection checking overlay
 * - Offline banner
 */
(function () {
  'use strict';

  // ── Mobile hamburger ──────────────────────────────────────────
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', e => {
      if (e.target.classList.contains('nav-link')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Connection checking overlay ───────────────────────────────
  const overlay = document.getElementById('connection-overlay');
  const offlineBanner = document.getElementById('offline-banner');

  function checkConnection() {
    if (!navigator.onLine) {
      if (overlay) overlay.classList.remove('show');
      if (offlineBanner) offlineBanner.classList.add('show');
      return;
    }
    // Verify API is actually reachable (not just network is up)
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    fetch('/api/health', { signal: ctrl.signal })
      .then(r => {
        clearTimeout(timer);
        if (overlay) overlay.classList.remove('show');
        if (offlineBanner) offlineBanner.classList.remove('show');
      })
      .catch(() => {
        clearTimeout(timer);
        if (overlay) overlay.classList.remove('show');
        // Don't show offline banner if navigator.onLine is true
        // — could be a server warmup issue
      });
  }

  // Show overlay briefly on page load to verify connection
  if (overlay) {
    overlay.classList.add('show');
    // Give the backend 3 seconds to respond before hiding
    setTimeout(() => {
      overlay.classList.remove('show');
    }, 3000);
    checkConnection();
  }

  // Listen for online/offline events
  window.addEventListener('offline', () => {
    if (offlineBanner) offlineBanner.classList.add('show');
  });
  window.addEventListener('online', () => {
    if (offlineBanner) offlineBanner.classList.remove('show');
    checkConnection();
  });

  // ── PWA install ───────────────────────────────────────────────
  const ua        = navigator.userAgent.toLowerCase();
  const isIOS     = /iphone|ipad|ipod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isMacSaf  = /macintosh/.test(ua) && /safari/.test(ua) && !/chrome|crios|chromium/.test(ua);
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;

  let deferred = null;
  const wrap   = document.getElementById('pwa-install-wrap');

  function showInstallBtn(label) {
    if (!wrap || isStandalone) return;
    wrap.style.display = 'flex';
    wrap.innerHTML = `<button class="btn-install" id="pwa-btn">${label}</button>`;
    document.getElementById('pwa-btn').addEventListener('click', async () => {
      if (deferred) {
        deferred.prompt();
        const { outcome } = await deferred.userChoice;
        if (outcome === 'accepted') wrap.style.display = 'none';
        deferred = null;
      } else if (isIOS) {
        alert('To install: tap the Share button (□↑) then "Add to Home Screen".');
      } else {
        alert('To install: open your browser menu and choose "Install app" or "Add to Home Screen".');
      }
    });
  }

  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferred = e;
    showInstallBtn('⬇ Install');
  });
  window.addEventListener('appinstalled', () => {
    if (wrap) wrap.style.display = 'none';
  });
  if ((isIOS || isMacSaf) && !isStandalone) {
    showInstallBtn(isIOS ? '⬇ Add to Home Screen' : '⬇ Install on Mac');
  }

  // ── Service worker ────────────────────────────────────────────
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }
})();
