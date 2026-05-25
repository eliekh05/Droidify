/**
 * Droidify nav — mobile hamburger + PWA install
 */
(function () {
  // Mobile hamburger
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close nav when a link is clicked
    nav.addEventListener('click', e => {
      if (e.target.classList.contains('nav-link')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // PWA install
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

  // Chrome/Edge — wait for beforeinstallprompt
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferred = e;
    showInstallBtn('⬇ Install');
  });

  window.addEventListener('appinstalled', () => {
    if (wrap) wrap.style.display = 'none';
  });

  // Safari — always show since beforeinstallprompt never fires
  if ((isIOS || isMacSaf) && !isStandalone) {
    const label = isIOS ? '⬇ Add to Home Screen' : '⬇ Install on Mac';
    showInstallBtn(label);
  }

  // Service worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }
})();
