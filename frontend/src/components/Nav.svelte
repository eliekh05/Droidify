<script>
  import { navigate } from '../lib/router.js';
  export let active = '';
  
  const links = [
    { key: 'home',       href: '/',               label: 'Home' },
    { key: 'devices',    href: '/devices',         label: 'Devices' },
    { key: 'roms',       href: '/roms',            label: 'ROMs' },
    { key: 'recoveries', href: '/recoveries',      label: 'Recoveries' },
    { key: 'tools',      href: '/tools',           label: 'Tools' },
    { key: 'android',    href: '/android',         label: 'Android' },
    { key: 'guides',     href: '/guides',          label: 'Guides' },
  ];

  let deferred = null;
  let installed = false;
  let showInstall = false;

  // Platform detection
  const ua = typeof navigator !== 'undefined' ? navigator.userAgent.toLowerCase() : '';
  const isIOS  = /iphone|ipad|ipod/.test(ua) || (navigator?.platform === 'MacIntel' && navigator?.maxTouchPoints > 1);
  const isMac  = /macintosh/.test(ua) && !isIOS;
  const isSafari = /safari/.test(ua) && !/chrome|crios|chromium/.test(ua);

  // Determine install label per platform
  $: installLabel = isIOS
    ? '⬇ Add to Home Screen'
    : isMac && isSafari
    ? '⬇ Install on Mac'
    : '⬇ Install';

  if (typeof window !== 'undefined') {
    // Chrome/Edge: capture the native prompt
    window.addEventListener('beforeinstallprompt', e => {
      e.preventDefault();
      deferred = e;
      showInstall = true;
    });

    window.addEventListener('appinstalled', () => {
      installed = true;
      showInstall = false;
      deferred = null;
    });

    // Safari (iOS + macOS): always show install button since beforeinstallprompt never fires
    if (isSafari || isIOS) {
      // Only show if not already in standalone mode
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches
        || window.navigator.standalone === true;
      if (!isStandalone) showInstall = true;
    }
  }

  async function install() {
    if (deferred) {
      // Chrome/Edge — use native prompt
      deferred.prompt();
      const { outcome } = await deferred.userChoice;
      if (outcome === 'accepted') { installed = true; showInstall = false; deferred = null; }
    } else if (isIOS) {
      alert('To install: tap the Share button (□↑) then "Add to Home Screen".');
    } else if (isMac && isSafari) {
      alert('To install: click File menu → "Add to Dock…" or use the Share button.');
    } else {
      alert('To install: open your browser menu and choose "Install app" or "Add to Home Screen".');
    }
  }

  let menuOpen = false;

  function handleNav(e, href) {
    e.preventDefault();
    menuOpen = false;
    navigate(href);
  }
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo" on:click={e => handleNav(e, '/')}>
      <span class="accent">Droid</span>ify
    </a>
    <button class="nav-toggle" on:click={() => menuOpen = !menuOpen} aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class={menuOpen ? 'open' : ''}>
      {#each links as { key, href, label }}
        <a
          {href}
          class="nav-link {active === key ? 'active' : ''}"
          on:click={e => handleNav(e, href)}
        >{label}</a>
      {/each}
    </nav>
    <div class="nav-end">
      {#if showInstall && !installed}
        <button class="btn-install" on:click={install}>{installLabel}</button>
      {/if}
      <a
        href="https://github.com/eliekh05/Droidify"
        class="btn-github"
        target="_blank"
        rel="noopener"
      >
        <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
