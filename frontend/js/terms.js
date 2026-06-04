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
    // Mark that the user has seen the terms page
    localStorage.setItem(SEEN_KEY, '1');

    var check = document.getElementById('terms-agree-check');

    // If already agreed server-side, skip
    fetch('/api/terms/status')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.agreed) {
          localStorage.setItem(AGREED_KEY, Date.now().toString());
          window.location.href = '/';
        }
      })
      .catch(function () {});

    // Intercept nav link clicks — if they navigate away without agreeing,
    // send to punishment page
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href]');
      if (!link) return;
      var href = link.getAttribute('href') || '';
      if (href.startsWith('#') ||
          href.startsWith('http') ||
          href.includes('terms') ||
          href.includes('not-read') ||
          href.includes('privacy')) return;
      e.preventDefault();
      window.location.href = NOT_READ_URL;
    });

    if (check) {
      check.addEventListener('change', function () {
        if (!check.checked) return;
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        fetch('/api/terms/agree', { method: 'POST' }).catch(function () {});
        window.location.href = '/';
      });
    }

    return;
  }

  if (isExempt) return;

  // Already agreed — let through
  if (localStorage.getItem(AGREED_KEY)) return;

  // Server check for logged-in users who agreed on another device
  fetch('/api/terms/status')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.agreed) {
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        return;
      }
      // Seen terms but navigated away without agreeing → punishment
      // Never seen terms yet → send to terms page
      if (localStorage.getItem(SEEN_KEY)) {
        window.location.href = NOT_READ_URL;
      } else {
        window.location.href = TERMS_URL;
      }
    })
    .catch(function () {
      if (localStorage.getItem(SEEN_KEY)) {
        window.location.href = NOT_READ_URL;
      } else {
        window.location.href = TERMS_URL;
      }
    });
})();
