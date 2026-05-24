/**
 * Svelte action: use:reveal
 * Adds scroll-triggered fade-up animation using IntersectionObserver.
 * Usage: <div use:reveal> or <div use:reveal={{ delay: 100 }}>
 */
export function reveal(node, options = {}) {
  const {
    delay = 0,
    duration = 500,
    threshold = 0.12,
    y = 24,
  } = options;

  // Respect prefers-reduced-motion
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return {};

  // Set initial state
  node.style.opacity = '0';
  node.style.transform = `translateY(${y}px)`;
  node.style.transition = `opacity ${duration}ms cubic-bezier(.22,1,.36,1) ${delay}ms, transform ${duration}ms cubic-bezier(.22,1,.36,1) ${delay}ms`;
  node.style.willChange = 'opacity, transform';

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          node.style.opacity = '1';
          node.style.transform = 'translateY(0)';
          node.style.willChange = 'auto';
          observer.unobserve(node); // fire once only
        }
      });
    },
    { threshold }
  );

  observer.observe(node);

  return {
    destroy() {
      observer.unobserve(node);
    }
  };
}
