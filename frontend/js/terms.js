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
    const bar      = document.getElementById('terms-agree-bar');
    const btn      = document.getElementById('terms-agree-btn');
    const lockMsg  = document.getElementById('terms-lock-msg');
    const sentinel = document.getElementById('terms-end');
    let   reached  = false;

    if (sentinel && btn) {
      var obs = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && !reached) {
          reached = true;
          btn.disabled = false;
          btn.classList.remove('is-light');
          btn.classList.add('is-success');
          if (lockMsg) lockMsg.style.display = 'none';
        }
      }, { threshold: 0.1 });
      obs.observe(sentinel);
    }

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

    // bar is already visible via HTML class
    return;
  }

  if (isExempt) return;
  if (!localStorage.getItem(AGREED_KEY)) {
    window.location.href = TERMS_URL;
  }
})();
