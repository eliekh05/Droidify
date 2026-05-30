/**
 * Droidify nav.js
 * - Mobile hamburger (Bulma uses is-active on navbar-menu)
 * - PWA install
 * - Connection checking overlay
 * - Offline banner
 */
(function () {
  'use strict';

  // ── Mobile hamburger ──────────────────────────────────────────
  // Bulma requires is-active on both the burger AND the navbar-menu
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('is-active');
      nav.classList.toggle('is-active');
      const open = nav.classList.contains('is-active');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', e => {
      if (e.target.closest('a')) {
        toggle.classList.remove('is-active');
        nav.classList.remove('is-active');
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
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    fetch('/api/health', { signal: ctrl.signal })
      .then(() => {
        clearTimeout(timer);
        if (overlay) overlay.classList.remove('show');
        if (offlineBanner) offlineBanner.classList.remove('show');
      })
      .catch(() => {
        clearTimeout(timer);
        if (overlay) overlay.classList.remove('show');
      });
  }

  if (overlay) {
    overlay.classList.add('show');
    setTimeout(() => overlay.classList.remove('show'), 3000);
    checkConnection();
  }

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
