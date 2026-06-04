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

    // Starts disabled — enabled only after scrolling to bottom
    if (check) check.disabled = true;

    // Add padding-bottom so page scrolls past the fixed bar
    var bar = document.getElementById('terms-agree-bar');
    var barH = bar ? bar.offsetHeight : 100;
    document.body.style.paddingBottom = (barH + 16) + 'px';

    function unlock() {
      if (reached) return;
      reached = true;
      if (check) check.disabled = false;
      if (lockMsg) lockMsg.textContent = 'Check the box to agree and continue.';
      if (label) label.classList.add('terms-label-active');
    }

    function checkScroll() {
      var remaining = document.documentElement.scrollHeight
                    - window.innerHeight
                    - window.scrollY;
      if (remaining <= 2) {
        unlock();
        window.removeEventListener('scroll', checkScroll);
      }
    }

    window.addEventListener('scroll', checkScroll, { passive: true });
    checkScroll();

    if (check) {
      check.addEventListener('change', function () {
        if (!reached) {
          check.checked = false;
          window.location.href = NOT_READ_URL;
          return;
        }
        if (check.checked) {
          localStorage.setItem(AGREED_KEY, Date.now().toString());
          window.location.href = '/';
        }
      });
    }

    return;
  }

  if (isExempt) return;
  if (!localStorage.getItem(AGREED_KEY)) {
    window.location.href = TERMS_URL;
  }
})();
