import { writable } from 'svelte/store';

export const currentRoute = writable(getRoute());

function getRoute() {
  const path = window.location.pathname;
  const query = new URLSearchParams(window.location.search);
  return { path, query };
}

export function navigate(path) {
  window.history.pushState({}, '', path);
  currentRoute.set(getRoute());
}

window.addEventListener('popstate', () => currentRoute.set(getRoute()));
