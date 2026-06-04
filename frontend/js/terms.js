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
    const btn     = document.getElementById('terms-agree-btn');
    const lockMsg = document.getElementById('terms-lock-msg');
    let   reached = false;

    // Disable via JS so click events always fire regardless of disabled state
    if (btn) {
      btn.disabled = true;
    }

    function unlock() {
      if (reached) return;
      reached = true;
      if (btn) {
        btn.disabled = false;
        btn.classList.remove('is-light');
        btn.classList.add('is-success');
      }
      if (lockMsg) lockMsg.style.display = 'none';
      window.removeEventListener('scroll', checkScroll);
    }

    function checkScroll() {
      // MDN recommended pattern — tolerates rounding differences
      var remaining = document.documentElement.scrollHeight
                    - window.innerHeight
                    - window.scrollY;
      if (remaining <= 2) unlock();
    }

    window.addEventListener('scroll', checkScroll, { passive: true });
    // Check immediately — unlocks if page is too short to scroll
    checkScroll();

    if (btn) {
      btn.addEventListener('click', function () {
        if (!reached) {
          window.location.href = NOT_READ_URL;
          return;
        }
        localStorage.setItem(AGREED_KEY, Date.now().toString());
        window.location.href = '/';
      });
    }

    return;
  }

  if (isExempt) return;
  if (!localStorage.getItem(AGREED_KEY)) {
    window.location.href = TERMS_URL;
  }
})();
