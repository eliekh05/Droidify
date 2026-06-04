(function () {
  'use strict';

  const AGREED_KEY   = 'droidify_terms_agreed_v1';
  const SEEN_KEY     = 'droidify_terms_seen_v1';
  const NOT_READ_URL = '/not-read.html';
  const TERMS_URL    = '/terms.html';

  const path      = window.location.pathname;
  const onTerms   = path.endsWith('terms.html')    || path === '/terms';
  const onNotRead = path.endsWith('not-read.html') || path === '/not-read';
  const exempt    = ['/terms.html', '/not-read.html', '/privacy.html'];
  const isExempt  = exempt.some(function (p) { return path.endsWith(p); });

  if (onNotRead) return;

  if (onTerms) {
    localStorage.setItem(SEEN_KEY, '1');

    var check = document.getElementById('terms-agree-check');

    // Server-side skip for logged-in users who already agreed
    fetch('/api/terms/status')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.agreed) {
          localStorage.setItem(AGREED_KEY, Date.now().toString());
          window.location.href = '/';
        }
      })
      .catch(function () {});

    // Intercept ALL link clicks on the page
    // Use capture phase so it fires before any other handler
    document.addEventListener('click', function (e) {
      // Find the closest anchor
      var node = e.target;
      while (node && node.tagName !== 'A') {
        node = node.parentElement;
      }
      if (!node) return;

      var href = node.getAttribute('href') || '';
      if (!href || href === '#' ||
          href.startsWith('http') ||
          href.includes('terms') ||
          href.includes('not-read') ||
          href.includes('privacy') ||
          href.includes('mailto')) return;

      e.preventDefault();
      e.stopImmediatePropagation();
      window.location.href = NOT_READ_URL;
    }, true); // true = capture phase, fires first

    if (check) {
      check.addEventListener('change', function () {
        if (!check.checked) return;
        // Set agreed immediately
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        // Fire and forget server record
        fetch('/api/terms/agree', { method: 'POST' }).catch(function () {});
        // Small delay so localStorage write completes before navigation
        setTimeout(function () {
          window.location.href = '/';
        }, 50);
      });
    }

    return;
  }

  if (isExempt) return;

  // Gate — localStorage first, fastest
  if (localStorage.getItem(AGREED_KEY)) return;

  // Server check for logged-in users on another device
  fetch('/api/terms/status')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.agreed) {
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        return;
      }
      window.location.href = localStorage.getItem(SEEN_KEY)
        ? NOT_READ_URL
        : TERMS_URL;
    })
    .catch(function () {
      window.location.href = localStorage.getItem(SEEN_KEY)
        ? NOT_READ_URL
        : TERMS_URL;
    });
})();
