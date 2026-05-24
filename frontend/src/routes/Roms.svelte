<script>
  import { onMount } from 'svelte';
  import { currentRoute, navigate } from '../lib/router.js';
  import { api } from '../lib/api.js';
  import { reveal } from '../lib/reveal.js';
  import Pagination from '../components/Pagination.svelte';

  const LIMIT = 24;
  let roms = [], total = 0, offset = 0, loading = true, error = '';
  let query = '';

  async function load(q = '', off = 0) {
    loading = true; error = '';
    try {
      const data = await api.roms({ q: q || undefined, limit: LIMIT, offset: off });
      roms = data.roms; total = data.total; offset = off;
    } catch(e) { error = e.message; }
    loading = false;
  }

  onMount(() => { query = $currentRoute.query.get('q') || ''; load(query, 0); });
  function search() { navigate(query.trim() ? `/roms?q=${encodeURIComponent(query.trim())}` : '/roms'); }
</script>

<main class="container">
  <div class="page-header" use:reveal><h1>ROMs</h1><p class="page-sub">Browse custom Android ROMs across all supported devices</p></div>
  <div class="filters-bar">
    <input class="search-input" type="search" placeholder="Search ROM name..." bind:value={query}
      on:keydown={e => e.key === 'Enter' && search()} />
    <button class="btn-primary" on:click={search}>Search</button>
  </div>
  {#if total > 0}<div class="results-meta">{total.toLocaleString()} ROM{total !== 1 ? 's' : ''}</div>{/if}
  {#if loading}
    <div class="device-grid">{#each Array(12) as _}<div class="skeleton" style="height:90px"></div>{/each}</div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else if roms.length === 0}
    <div class="empty-state">No ROMs found.</div>
  {:else}
    <div class="device-grid">
      {#each roms as rom, i}
        <div use:reveal={{ delay: i * 40 }}>
          <div class="card">
            <div class="card-mfr">{rom.source || 'custom'}</div>
            <div class="card-title">{rom.name}</div>
            <div class="card-codename">{rom.codename}</div>
            {#if rom.android_base}<div style="font-size:.78rem;color:var(--muted);margin-top:.3rem">Android {rom.android_base}</div>{/if}
            {#if rom.download_url}
              <div style="margin-top:.5rem">
                <a href={rom.download_url} target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
    <Pagination {total} {offset} limit={LIMIT} onPage={off => load(query, off)} />
  {/if}
</main>
