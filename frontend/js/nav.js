(function () {
  'use strict';

  // ── Mobile hamburger ──────────────────────────────────────────────────────
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');
  if (toggle && nav) {
    function doToggle(e) {
      e.preventDefault();
      toggle.classList.toggle('is-active');
      nav.classList.toggle('is-active');
      toggle.setAttribute('aria-expanded',
        nav.classList.contains('is-active') ? 'true' : 'false');
    }
    toggle.addEventListener('click',      doToggle);
    toggle.addEventListener('touchstart', doToggle, { passive: false });
    nav.addEventListener('click', e => {
      if (e.target.closest('a')) {
        toggle.classList.remove('is-active');
        nav.classList.remove('is-active');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Connection overlay ────────────────────────────────────────────────────
  const overlay       = document.getElementById('connection-overlay');
  const offlineBanner = document.getElementById('offline-banner');

  function checkConnection() {
    if (!navigator.onLine) {
      if (overlay) overlay.classList.remove('show');
      if (offlineBanner) offlineBanner.classList.add('show');
      return;
    }
    const ctrl  = new AbortController();
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
  window.addEventListener('offline', () => { if (offlineBanner) offlineBanner.classList.add('show'); });
  window.addEventListener('online',  () => { if (offlineBanner) offlineBanner.classList.remove('show'); checkConnection(); });

  // ── PWA install ───────────────────────────────────────────────────────────
  const ua         = navigator.userAgent.toLowerCase();
  const isIOS      = /iphone|ipad|ipod/.test(ua) ||
                     (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isMacSaf   = /macintosh/.test(ua) && /safari/.test(ua) && !/chrome|crios|chromium/.test(ua);
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                       navigator.standalone === true;

  let deferred = null;
  const installWrap = document.getElementById('pwa-install-wrap');

  function showPwaModal(iosMode) {
    const existing = document.getElementById('pwa-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'pwa-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Install Droidify');

    const steps = iosMode
      ? 'Tap the <strong>Share</strong> button (the square with an arrow) at the bottom of your browser, then tap <strong>Add to Home Screen</strong>.'
      : 'Open your browser menu (the three dots ⋮ or ⋯) and tap <strong>Install app</strong> or <strong>Add to Home Screen</strong>.';

    modal.innerHTML =
      '<div class="pwa-modal-overlay" id="pwa-modal-overlay"></div>' +
      '<div class="pwa-modal-box">' +
        '<div class="pwa-modal-icon">📲</div>' +
        '<h2 class="pwa-modal-title">Install Droidify</h2>' +
        '<p class="pwa-modal-body">' + steps + '</p>' +
        '<button class="pwa-modal-close" id="pwa-modal-close" aria-label="Close">Got it</button>' +
      '</div>';

    document.body.appendChild(modal);
    requestAnimationFrame(() => modal.classList.add('pwa-modal-visible'));

    function closeModal() {
      modal.classList.remove('pwa-modal-visible');
      setTimeout(() => modal.remove(), 250);
    }
    document.getElementById('pwa-modal-close').addEventListener('click', closeModal);
    document.getElementById('pwa-modal-overlay').addEventListener('click', closeModal);
    document.addEventListener('keydown', function onEsc(e) {
      if (e.key === 'Escape') { closeModal(); document.removeEventListener('keydown', onEsc); }
    });
  }

  function showInstallBtn(label) {
    if (!installWrap || isStandalone) return;
    installWrap.style.display = 'flex';
    installWrap.innerHTML = '<button class="btn-install" id="pwa-btn">' + label + '</button>';
    document.getElementById('pwa-btn').addEventListener('click', function () {
      if (deferred) {
        deferred.prompt();
        deferred.userChoice.then(function (result) {
          if (result.outcome === 'accepted') installWrap.style.display = 'none';
          deferred = null;
        });
      } else {
        showPwaModal(isIOS);
      }
    });
  }

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    showInstallBtn('⬇ Install');
  });
  window.addEventListener('appinstalled', function () {
    if (installWrap) installWrap.style.display = 'none';
  });
  if ((isIOS || isMacSaf) && !isStandalone) {
    showInstallBtn(isIOS ? '⬇ Add to Home Screen' : '⬇ Install on Mac');
  }

  // ── Service worker ────────────────────────────────────────────────────────
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  }

  // ── Theme switcher ────────────────────────────────────────────────────────
  const THEME_KEY = 'droidify_theme';

  function applyTheme(theme) {
    if (theme === 'system') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }
    document.querySelectorAll('.theme-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.theme === theme);
    });
  }

  function setupThemeSwitcher() {
    const switcher = document.getElementById('theme-switcher');
    if (!switcher) return;
    switcher.innerHTML =
      '<button class="theme-btn" data-theme="light"  title="Light mode"     aria-label="Light mode">☀</button>' +
      '<button class="theme-btn" data-theme="dark"   title="Dark mode"      aria-label="Dark mode">🌙</button>' +
      '<button class="theme-btn" data-theme="system" title="System default" aria-label="System default">💻</button>';
    const saved = localStorage.getItem(THEME_KEY) || 'system';
    switcher.querySelectorAll('.theme-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.theme === saved);
      btn.addEventListener('click', function () {
        const t = btn.dataset.theme;
        localStorage.setItem(THEME_KEY, t);
        applyTheme(t);
      });
    });
  }

  applyTheme(localStorage.getItem(THEME_KEY) || 'system');
  setupThemeSwitcher();

})();
