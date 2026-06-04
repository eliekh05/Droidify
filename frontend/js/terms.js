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
    var check   = document.getElementById('terms-agree-check');
    var lockMsg = document.getElementById('terms-lock-msg');
    var label   = document.getElementById('terms-agree-label');
    var reached = false;

    if (check) check.disabled = true;

    function unlock() {
      if (reached) return;
      reached = true;
      if (check) check.disabled = false;
      if (lockMsg) lockMsg.textContent = 'Check the box to agree and continue.';
      if (label) label.classList.add('terms-label-active');
      window.removeEventListener('scroll', checkScroll);
    }

    function checkScroll() {
      // MDN recommended pattern — Math.ceil handles subpixel precision
      // document.body.offsetHeight used as fallback per Stack Overflow consensus
      // barH accounts for fixed bar covering bottom of viewport
      var barH      = 100; // safe default, updated on load
      var bar       = document.getElementById('terms-agree-bar');
      if (bar) barH = bar.getBoundingClientRect().height;

      var docHeight = Math.max(
        document.documentElement.scrollHeight,
        document.body.scrollHeight,
        document.body.offsetHeight
      );
      var scrolled  = Math.ceil(window.pageYOffset || window.scrollY);
      var remaining = docHeight - window.innerHeight - scrolled;

      // Fire when within (bar height + 10px safety margin) of bottom
      if (remaining <= barH + 10) unlock();
    }

    window.addEventListener('scroll', checkScroll, { passive: true });

    // Run after full layout including images and fonts
    window.addEventListener('load', function () {
      // Apply padding so content scrolls past fixed bar
      var bar  = document.getElementById('terms-agree-bar');
      var barH = bar ? bar.getBoundingClientRect().height : 100;
      document.body.style.paddingBottom = (barH + 24) + 'px';
      // Check immediately in case page is short
      checkScroll();
    });

    if (check) {
      check.addEventListener('change', function () {
        if (!reached) {
          check.checked = false;
          window.location.href = NOT_READ_URL;
          return;
        }
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
