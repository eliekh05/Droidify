/**
 * Droidify reveal.js
 * Single IntersectionObserver for ALL elements — every element animates.
 * MutationObserver watches for dynamically added content.
 * GPU-accelerated: only opacity + transform.
 * Stagger: calculated per-group via data-index attribute set on injection.
 */
(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function showAll() {
    document.querySelectorAll('.reveal').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }

  if (reduced) {
    document.readyState === 'loading'
      ? document.addEventListener('DOMContentLoaded', showAll)
      : showAll();
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -30px 0px',
  });

  function observe() {
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
      observer.observe(el);
    });
  }

  // Initial observe
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observe);
  } else {
    observe();
  }

  // Watch for dynamically added content (cards loaded via JS)
  const mutationObserver = new MutationObserver(() => observe());
  document.addEventListener('DOMContentLoaded', () => {
    mutationObserver.observe(document.body, { childList: true, subtree: true });
  });

  // Manual trigger after dynamic content
  window._reObserve = observe;
})();
