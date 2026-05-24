<script>
  import { onMount } from 'svelte';
  import { navigate } from '../lib/router.js';
  import { api } from '../lib/api.js';
  import DeviceCard from '../components/DeviceCard.svelte';

  let stats = { devices: null, roms: null, recoveries: null, tools: null, android: null };
  let featured = [];
  let romFamilies = [];
  let androidPills = [];
  let query = '';

  function search() {
    if (query.trim()) navigate(`/devices?q=${encodeURIComponent(query.trim())}`);
    else navigate('/devices');
  }

  onMount(() => {
    // Load each independently so nothing blocks
    api.devices({ limit: 50 }).then(d => {
      stats.devices = d.total;
      featured = [...d.devices].sort(() => Math.random() - .5).slice(0, 6);
    }).catch(() => {});

    api.roms({ limit: 1 }).then(d => { stats.roms = d.total; }).catch(() => {});
    api.recoveries({ limit: 1 }).then(d => { stats.recoveries = d.total; }).catch(() => {});
    api.tools().then(d => { stats.tools = d.total; }).catch(() => {});
    api.androidVersions().then(d => {
      stats.android = d.total;
      androidPills = [...d.versions].reverse().slice(0, 8);
    }).catch(() => {});

    api.roms({ limit: 50 }).then(d => {
      const counts = {};
      for (const r of d.roms) counts[r.name] = (counts[r.name] || 0) + 1;
      romFamilies = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 8)
        .map(([name, count]) => ({ name, count }));
    }).catch(() => {});
  });

  const SOURCES = ['LineageOS API','Wikipedia','OrangeFox API','TWRP','GrapheneOS','GitHub API','crDroid','DivestOS','CalyxOS','/e/OS'];
</script>

<main class="container">
  <section class="hero">
    <h1 class="hero-title"><span class="accent">Droid</span>ify</h1>
    <p class="hero-sub">Devices, ROMs, recoveries, and tools — fetched in real time from LineageOS, Wikipedia, OrangeFox, TWRP, GitHub and more. Zero hardcoded data. No signin. No payment.</p>
    <div class="hero-search">
      <input class="search-input" type="search" placeholder="Search device, codename or manufacturer..."
        bind:value={query} on:keydown={e => e.key === 'Enter' && search()} />
      <button class="btn-primary" on:click={search}>Search</button>
    </div>
  </section>

  <div class="sources-banner">
    <div class="badges">
      {#each SOURCES as s}<span class="badge">{s}</span>{/each}
    </div>
    <span class="sources-note">All free · No signin · Live data</span>
  </div>

  <section class="section" style="margin-top:2rem">
    <div class="section-header"><h2>Stats</h2></div>
    <div class="stats-box">
      {#each [
        ['stat-devices',   stats.devices,    'Devices indexed'],
        ['stat-roms',      stats.roms,       'ROM builds'],
        ['stat-recoveries',stats.recoveries, 'Recovery builds'],
        ['stat-tools',     stats.tools,      'Tools listed'],
        ['stat-android',   stats.android,    'Android versions'],
      ] as [id, val, label]}
        <div class="stat-item">
          <div class="stat-value" {id}>{val != null ? val.toLocaleString() : '—'}</div>
          <div class="stat-label">{label}</div>
        </div>
      {/each}
    </div>
  </section>

  <section class="section">
    <div class="section-header">
      <h2>Featured devices</h2>
      <a href="/devices" class="section-link" on:click|preventDefault={() => navigate('/devices')}>Browse all →</a>
    </div>
    {#if featured.length}
      <div class="device-grid">
        {#each featured as device}
          <DeviceCard {device} />
        {/each}
      </div>
    {:else}
      <div class="device-grid">
        {#each Array(6) as _}
          <div class="skeleton" style="height:110px"></div>
        {/each}
      </div>
    {/if}
  </section>

  {#if romFamilies.length}
    <section class="section">
      <div class="section-header">
        <h2>ROM families</h2>
        <a href="/roms" class="section-link" on:click|preventDefault={() => navigate('/roms')}>Browse all →</a>
      </div>
      <div class="device-grid">
        {#each romFamilies as { name, count }}
          <div class="card" style="cursor:pointer" role="button" tabindex="0"
            on:click={() => navigate(`/roms?q=${encodeURIComponent(name)}`)}
            on:keydown={e => e.key === 'Enter' && navigate(`/roms?q=${encodeURIComponent(name)}`)}>
            <div class="card-title">{name}</div>
            <div class="card-sub" style="color:var(--muted);font-size:.8rem">{count} build{count !== 1 ? 's' : ''}</div>
          </div>
        {/each}
      </div>
    </section>
  {/if}

  {#if androidPills.length}
    <section class="section">
      <div class="section-header">
        <h2>Android versions</h2>
        <a href="/android" class="section-link" on:click|preventDefault={() => navigate('/android')}>Full history →</a>
      </div>
      <div class="android-pills">
        {#each androidPills as v}
          <div class="v-pill" role="button" tabindex="0"
            on:click={() => navigate('/android')}
            on:keydown={e => e.key === 'Enter' && navigate('/android')}>
            <span class="v-num">Android {v.version_number}</span>
            <span class="v-name">{v.codename || '—'}</span>
          </div>
        {/each}
      </div>
    </section>
  {/if}
</main>
