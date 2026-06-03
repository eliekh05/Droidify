(function () {
  'use strict';

  const AGREED_KEY   = 'droidify_terms_agreed_v1';
  const NOT_READ_URL = '/not-read.html';
  const TERMS_URL    = '/terms.html';

  const path      = window.location.pathname;
  const onTerms   = path.endsWith('terms.html')    || path === '/terms';
  const onNotRead = path.endsWith('not-read.html') || path === '/not-read';
  const exempt    = ['/terms.html', '/not-read.html', '/privacy.html'];
  const isExempt  = exempt.some(p => path.endsWith(p));

  // Punishment page — nothing interactive, just the back button
  if (onNotRead) return;

  // terms.html — scroll gate only
  if (onTerms) {
    const bar     = document.getElementById('terms-agree-bar');
    const btn     = document.getElementById('terms-agree-btn');
    const lockMsg = document.getElementById('terms-lock-msg');
    let   reached = false;

    const sentinel = document.getElementById('terms-end');
    if (sentinel) {
      const obs = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !reached) {
          reached = true;
          btn.disabled = false;
          btn.classList.remove('is-light');
          btn.classList.add('is-success');
          if (lockMsg) lockMsg.style.display = 'none';
        }
      }, { threshold: 0.4 });
      obs.observe(sentinel);
    }

    btn.addEventListener('click', () => {
      if (!reached) {
        window.location.href = NOT_READ_URL;
        return;
      }
      localStorage.setItem(AGREED_KEY, Date.now().toString());
      window.location.href = '/';
    });

    if (bar) setTimeout(() => bar.classList.add('terms-bar-visible'), 600);
    return;
  }

  // Every other page — gate check
  if (isExempt) return;
  if (!localStorage.getItem(AGREED_KEY)) {
    window.location.href = TERMS_URL;
  }
})();
