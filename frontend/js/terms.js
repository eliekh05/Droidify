(function () {
  'use strict';

  const AGREED_KEY   = 'droidify_terms_agreed_v1';
  const NOT_READ_URL = '/not-read.html';
  const TERMS_URL    = '/terms.html';

  const path      = window.location.pathname;
  const onTerms   = path.endsWith('terms.html')    || path === '/terms';
  const onNotRead = path.endsWith('not-read.html') || path === '/not-read';
  const exempt    = ['/terms.html', '/not-read.html', '/privacy.html'];
  const isExempt  = exempt.some(function (p) { return path.endsWith(p); });

  if (onNotRead) return;

  if (onTerms) {
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

    // Capture phase — intercept nav clicks before Bulma handlers
    document.addEventListener('click', function (e) {
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
    }, true);

    if (check) {
      check.addEventListener('change', function () {
        if (!check.checked) return;
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        fetch('/api/terms/agree', { method: 'POST' }).catch(function () {});
        setTimeout(function () { window.location.href = '/'; }, 50);
      });
    }

    return;
  }

  if (isExempt) return;

  // Gate — localStorage first
  if (localStorage.getItem(AGREED_KEY)) return;

  // Server check for logged-in users on another device
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
