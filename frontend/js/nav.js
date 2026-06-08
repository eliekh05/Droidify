(function () {
  'use strict';

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

  function showPwaModal(iosMode, macSafMode) {
    const existing = document.getElementById('pwa-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'pwa-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Install Droidify');

    var steps;
    if (isIOS) {
      steps = 'Tap the <strong>Share</strong> button (the square with an arrow ↑) at the bottom of Safari, then tap <strong>Add to Home Screen</strong>.';
    } else if (isMacSaf) {
      steps = 'In Safari, click <strong>File</strong> in the menu bar, then click <strong>Add to Dock</strong>. Or click the <strong>Share</strong> button in the toolbar and select <strong>Add to Dock</strong>.';
    } else {
      steps = 'Open your browser menu (the three dots ⋮) and click <strong>Install app</strong> or <strong>Add to Home Screen</strong>.';
    }

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
        showPwaModal(isIOS, isMacSaf);
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

  // ── Theme switcher ────────────────────────────────────────────────────────
  const THEME_KEY = 'droidify_theme';

  function applyTheme(theme) {
    if (theme === 'system') {
      document.documentElement.removeAttribute('data-theme');
      // Manually apply system preference since CSS @media inside selectors
      // has limited browser support — set data-theme to match system
      var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      // But mark it as system so we know to follow changes
      document.documentElement.setAttribute('data-system-theme', '1');
    } else {
      document.documentElement.removeAttribute('data-system-theme');
      document.documentElement.setAttribute('data-theme', theme);
    }
    document.querySelectorAll('.theme-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.theme === theme);
    });
  }

  // Watch for system theme changes while in system mode
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (document.documentElement.getAttribute('data-system-theme')) {
      document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });

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

  // ── Auth state ───────────────────────────────────────────────────────────
  function setupAuth() {
    var wrap = document.getElementById('auth-wrap');
    if (!wrap) return;
    fetch('/api/auth/me')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.user) {
          wrap.innerHTML =
            '<div class="navbar-item auth-user">' +
              '<img src="' + d.user.avatar_url + '" class="auth-avatar" alt="' + d.user.login + '">' +
              '<span class="auth-login">' + d.user.login + '</span>' +
              '<a href="/api/auth/logout" class="auth-logout">Sign out</a>' +
            '</div>';
        } else {
          wrap.innerHTML =
            '<a href="/api/auth/login" class="navbar-item auth-signin">' +
              '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right:.35rem">' +
                '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>' +
              '</svg>' +
              'Sign in with GitHub' +
            '</a>';
        }
      })
      .catch(function () {
        wrap.innerHTML =
          '<a href="/api/auth/login" class="navbar-item auth-signin">' +
            'Sign in with GitHub' +
          '</a>';
      });
  }

  setupAuth();


  // ── ROM alert badge ────────────────────────────────────────────────────────
  function updateAlertBadge() {
    fetch('/api/alerts/count')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var count = d.count || 0;
        // Find Watchlist link in navbar
        var links = document.querySelectorAll('a.navbar-item');
        var wl    = null;
        for (var i = 0; i < links.length; i++) {
          if (links[i].getAttribute('href') === '/watchlist') { wl = links[i]; break; }
        }
        if (!wl) return;
        var existing = wl.querySelector('.alert-badge');
        if (count > 0) {
          if (!existing) {
            var badge = document.createElement('span');
            badge.className = 'alert-badge';
            badge.style.cssText = [
              'display:inline-flex', 'align-items:center', 'justify-content:center',
              'background:#ff3860', 'color:#fff', 'border-radius:999px',
              'font-size:.6rem', 'font-weight:700', 'min-width:1.1rem', 'height:1.1rem',
              'padding:0 .25rem', 'margin-left:.35rem', 'vertical-align:middle',
              'line-height:1'
            ].join(';');
            wl.appendChild(badge);
            existing = badge;
          }
          existing.textContent = count > 9 ? '9+' : String(count);
        } else if (existing) {
          existing.remove();
        }
      })
      .catch(function () {});
  }

  // Only fetch if user might be logged in (cookie present)
  if (document.cookie.indexOf('droidify_session') !== -1) {
    updateAlertBadge();
  }

})();
