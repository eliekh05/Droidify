(function () {
  'use strict';

  const AGREED_KEY   = 'droidify_terms_agreed_v1';
  const NOT_READ_URL = '/not-read';
  const TERMS_URL    = '/terms.html';

  const path      = window.location.pathname;
  const onTerms   = path.endsWith('terms.html')    || path === '/terms';
  const onNotRead = path.endsWith('not-read.html') || path === '/not-read';
  const exempt    = ['/terms.html', '/not-read', '/privacy.html'];
  const isExempt  = exempt.some(function (p) { return path.endsWith(p); });

  if (onNotRead) return;

  if (onTerms) {
    var fill = document.getElementById('terms-progress-fill');
    var agreed = false;

    // Server-side skip for already-agreed logged-in users
    fetch('/api/terms/status')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.agreed) {
          localStorage.setItem(AGREED_KEY, Date.now().toString());
          window.location.href = '/';
        }
      })
      .catch(function () {});

    // Nav click intercept — capture phase
    // If they click away before scrolling to the bottom, punishment page
    document.addEventListener('click', function (e) {
      var node = e.target;
      while (node && node.tagName !== 'A') { node = node.parentElement; }
      if (!node) return;
      var href = node.getAttribute('href') || '';
      if (!href || href === '#' ||
          href.startsWith('http') ||
          href.includes('terms') ||
          href.includes('not-read') ||
          href.includes('privacy') ||
          href.includes('mailto')) return;
      if (!agreed) {
        e.preventDefault();
        e.stopImmediatePropagation();
        window.location.href = NOT_READ_URL;
      }
    }, true);

    function onScroll() {
      var scrolled   = Math.ceil(window.pageYOffset || window.scrollY);
      var docHeight  = Math.max(
        document.documentElement.scrollHeight,
        document.body.scrollHeight
      );
      var winHeight  = window.innerHeight;
      var scrollable = docHeight - winHeight;
      if (scrollable <= 0) {
        // Page too short to scroll — agree immediately
        complete();
        return;
      }
      var pct = Math.min(100, Math.round((scrolled / scrollable) * 100));
      if (fill) fill.style.width = pct + '%';
      if (pct >= 100 && !agreed) complete();
    }

    function complete() {
      if (agreed) return;
      agreed = true;
      if (fill) fill.style.width = '100%';
      localStorage.setItem(AGREED_KEY, Date.now().toString());
      fetch('/api/terms/agree', { method: 'POST' }).catch(function () {});
      // Small pause so user sees the bar complete before redirect
      setTimeout(function () { window.location.href = '/'; }, 400);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    // Check immediately — handles short pages
    onScroll();
    return;
  }

  if (isExempt) return;

  if (localStorage.getItem(AGREED_KEY)) return;

  fetch('/api/terms/status')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.agreed) {
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        return;
      }
      window.location.href = TERMS_URL;
    })
    .catch(function () {
      window.location.href = TERMS_URL;
    });
})();
