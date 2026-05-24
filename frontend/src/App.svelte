<script>
  import { currentRoute } from './lib/router.js';
  import Nav from './components/Nav.svelte';
  import Home from './routes/Home.svelte';
  import Devices from './routes/Devices.svelte';
  import Device from './routes/Device.svelte';
  import Roms from './routes/Roms.svelte';
  import Recoveries from './routes/Recoveries.svelte';
  import Tools from './routes/Tools.svelte';
  import Android from './routes/Android.svelte';
  import Guides from './routes/Guides.svelte';
  import Privacy from './routes/Privacy.svelte';

  $: path = $currentRoute.path.replace(/\/$/, '') || '/';

  $: active = {
    '/':           'home',
    '/devices':    'devices',
    '/roms':       'roms',
    '/recoveries': 'recoveries',
    '/tools':      'tools',
    '/android':    'android',
    '/guides':     'guides',
  }[path] ?? (path.startsWith('/device/') ? 'devices' : '');
</script>

<Nav {active} />

{#if path === '/'}
  <Home />
{:else if path === '/devices'}
  <Devices />
{:else if path.startsWith('/device/')}
  <Device />
{:else if path === '/roms'}
  <Roms />
{:else if path === '/recoveries'}
  <Recoveries />
{:else if path === '/tools'}
  <Tools />
{:else if path === '/android'}
  <Android />
{:else if path === '/guides'}
  <Guides />
{:else if path === '/privacy'}
  <Privacy />
{:else}
  <Home />
{/if}

<footer class="site-footer">
  <div class="container">
    <p>Droidify — Live Android ecosystem indexer · Free &amp; open sources only · No signin required ·
      <a href="/privacy" on:click|preventDefault={() => { window.history.pushState({}, '', '/privacy'); window.dispatchEvent(new PopStateEvent('popstate')); }}>Privacy</a>
    </p>
  </div>
</footer>
