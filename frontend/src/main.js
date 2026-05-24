import './app.css';
import App from './App.svelte';
import { mount } from 'svelte';

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(() => {});
}

const app = mount(App, { target: document.getElementById('app') });
export default app;
