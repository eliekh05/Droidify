/**
 * Droidify scroll reveal
 * Single IntersectionObserver instance — best practice 2025
 * Only opacity + transform animated (GPU-composited)
 * Fires once per element then unobserves
 */
(function () {
  if (typeof window === 'undefined') return;

  // Respect prefers-reduced-motion — skip setup entirely
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    });
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // fire once only
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px', // trigger slightly before fully in view
  });

  function observe() {
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }

  // Observe on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observe);
  } else {
    observe();
  }

  // Re-observe after dynamic content added
  window._reObserve = () => {
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => observer.observe(el));
  };
})();
