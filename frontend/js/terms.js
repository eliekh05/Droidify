(function () {
  'use strict';

  var AGREED_KEY   = 'droidify_terms_agreed_v1';
  var NOT_READ_URL = '/not-read';
  var TERMS_URL    = '/terms';

  var path      = window.location.pathname;
  var onTerms   = path === '/terms';
  var onNotRead = path.endsWith('not-read.html') || path === '/not-read';
  var exempt    = ['/terms', '/not-read', '/privacy', '/faq'];
  var isExempt  = exempt.some(function (p) { return path === p || path.endsWith(p); });

  if (onNotRead) return;

  // ── Terms page — scroll-to-agree ──────────────────────────────────────────
  if (onTerms) {
    var fill   = document.getElementById('terms-progress-fill');
    var agreed = false;
    // ?read=1 means user just wants to read — no redirect, no gate
    var readOnly = window.location.search.indexOf('read=1') !== -1;

    // If already agreed (localStorage or server) — just show the page, no redirect
    if (localStorage.getItem(AGREED_KEY)) {
      agreed = true;
      if (fill) fill.style.width = '100%';
    } else if (!readOnly) {
      fetch('/api/terms/status')
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.agreed) {
            localStorage.setItem(AGREED_KEY, Date.now().toString());
            agreed = true;
            if (fill) fill.style.width = '100%';
          }
        })
        .catch(function () {});
    }

    // Block nav clicks until scroll complete
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
          href.includes('faq') ||
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
      if (scrollable <= 0) { complete(); return; }
      var pct = Math.min(100, Math.round((scrolled / scrollable) * 100));
      if (fill) fill.style.width = pct + '%';
      if (pct >= 100 && !agreed) complete();
    }

    function complete() {
      if (agreed) return;
      agreed = true;
      if (fill) fill.style.width = '100%';
      if (readOnly) return; // just reading — don't redirect or fire agree
      localStorage.setItem(AGREED_KEY, Date.now().toString());
      fetch('/api/terms/agree', { method: 'POST' }).catch(function () {});
      setTimeout(function () { window.location.replace('/'); }, 400);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return;
  }

  // ── All other pages — gate check ──────────────────────────────────────────
  if (isExempt) return;

  // Fast path — localStorage already set on this device
  if (localStorage.getItem(AGREED_KEY)) return;

  // Slow path — check server (handles signed-in users on new devices)
  fetch('/api/terms/status')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.agreed) {
        // Signed in and agreed on another device — unlock this device too
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        return;
      }
      // Not agreed anywhere — send to terms
      window.location.replace(TERMS_URL);
    })
    .catch(function () {
      // Network error — send to terms to be safe
      window.location.replace(TERMS_URL);
    });
})();
