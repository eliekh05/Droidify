<script>
  import { onMount } from 'svelte';
  import { currentRoute, navigate } from '../lib/router.js';
  import { api } from '../lib/api.js';
  import DeviceCard from '../components/DeviceCard.svelte';
  import Pagination from '../components/Pagination.svelte';
  import { reveal } from '../lib/reveal.js';

  const LIMIT = 24;
  let devices = [], total = 0, offset = 0, loading = true, error = '';
  let query = '';

  $: currentQuery = $currentRoute.query.get('q') || '';

  async function load(q = '', off = 0) {
    loading = true; error = '';
    try {
      const data = await api.devices({ q: q || undefined, limit: LIMIT, offset: off });
      devices = data.devices; total = data.total; offset = off;
    } catch(e) { error = e.message; }
    loading = false;
  }

  onMount(() => {
    query = currentQuery;
    load(query, 0);
  });

  $: if (typeof window !== 'undefined') { query = currentQuery; load(query, 0); }

  function search() { navigate(query.trim() ? `/devices?q=${encodeURIComponent(query.trim())}` : '/devices'); }
</script>

<main class="container">
  <div class="page-header">
    <h1>Devices</h1>
    <p class="page-sub">Browse and search over 1,100 Android devices</p>
  </div>

  <div class="filters-bar">
    <input class="search-input" type="search" placeholder="Search device, codename or manufacturer..."
      bind:value={query} on:keydown={e => e.key === 'Enter' && search()} />
    <button class="btn-primary" on:click={search}>Search</button>
  </div>

  {#if total > 0}
    <div class="results-meta">{total.toLocaleString()} device{total !== 1 ? 's' : ''}{query ? ` for "${query}"` : ''}</div>
  {/if}

  {#if loading}
    <div class="device-grid">
      {#each Array(12) as _}<div class="skeleton" style="height:110px"></div>{/each}
    </div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else if devices.length === 0}
    <div class="empty-state">No devices found. Try a different search.</div>
  {:else}
    <div class="device-grid">
      {#each devices as device, i}
        <div use:reveal={{ delay: i * 40 }}><DeviceCard {device} /></div>
      {/each}
    </div>
    <Pagination {total} {offset} limit={LIMIT} onPage={off => load(query, off)} />
  {/if}
</main>
