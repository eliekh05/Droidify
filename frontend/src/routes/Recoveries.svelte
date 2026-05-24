<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';
  import Pagination from '../components/Pagination.svelte';

  const LIMIT = 24;
  let recoveries = [], total = 0, offset = 0, loading = true, error = '', query = '';

  async function load(q = '', off = 0) {
    loading = true; error = '';
    try {
      const data = await api.recoveries({ q: q || undefined, limit: LIMIT, offset: off });
      recoveries = data.recoveries; total = data.total; offset = off;
    } catch(e) { error = e.message; }
    loading = false;
  }

  onMount(() => load('', 0));
  function search() { load(query, 0); }
</script>

<main class="container">
  <div class="page-header"><h1>Recoveries</h1><p class="page-sub">TWRP, OrangeFox, SHRP and more</p></div>
  <div class="filters-bar">
    <input class="search-input" type="search" placeholder="Search device or recovery..."
      bind:value={query} on:keydown={e => e.key === 'Enter' && search()} />
    <button class="btn-primary" on:click={search}>Search</button>
  </div>
  {#if total > 0}<div class="results-meta">{total.toLocaleString()} recovery build{total !== 1 ? 's' : ''}</div>{/if}
  {#if loading}
    <div class="device-grid">{#each Array(12) as _}<div class="skeleton" style="height:90px"></div>{/each}</div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else}
    <div class="device-grid">
      {#each recoveries as r}
        <div class="card">
          <div class="card-mfr">{r.recovery_type || 'recovery'}</div>
          <div class="card-title">{r.model_name || r.codename}</div>
          <div class="card-codename">{r.codename}</div>
          {#if r.download_url}
            <div style="margin-top:.5rem">
              <a href={r.download_url} target="_blank" rel="noopener"
                style="font-size:.78rem;color:var(--accent)">Download →</a>
            </div>
          {/if}
        </div>
      {/each}
    </div>
    <Pagination {total} {offset} limit={LIMIT} onPage={off => load(query, off)} />
  {/if}
</main>
