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

    if (check) {
      check.addEventListener('change', function () {
        if (!check.checked) return;

        fetch('/api/terms/agree', { method: 'POST' })
          .then(function (r) { return r.json(); })
          .then(function () {
            localStorage.setItem(AGREED_KEY, Date.now().toString());
            window.location.href = '/';
          })
          .catch(function () {
            localStorage.setItem(AGREED_KEY, Date.now().toString());
            window.location.href = '/';
          });
      });
    }

    return;
  }

  if (isExempt) return;

  fetch('/api/terms/status')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.agreed) return;
      if (localStorage.getItem(AGREED_KEY)) return;
      window.location.href = TERMS_URL;
    })
    .catch(function () {
      if (!localStorage.getItem(AGREED_KEY)) {
        window.location.href = TERMS_URL;
      }
    });
})();
