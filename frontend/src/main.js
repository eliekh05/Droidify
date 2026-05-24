import './app.css';
import App from './App.svelte';

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(() => {});
}

const app = new App({ target: document.getElementById('app') });
export default app;
