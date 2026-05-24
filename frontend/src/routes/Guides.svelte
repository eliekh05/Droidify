<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let guides = [], loading = false, error = '', query = '';

  async function search() {
    if (!query.trim()) return;
    loading = true; error = '';
    try {
      const data = await api.guides({ codename: query.trim() });
      guides = data.guides || data;
    } catch(e) { error = e.message; guides = []; }
    loading = false;
  }
</script>

<main class="container">
  <div class="page-header"><h1>Guides</h1><p class="page-sub">Flashing, rooting, and Android modding guides</p></div>
  <div class="filters-bar">
    <input class="search-input" type="search" placeholder="Enter device codename (e.g. beryllium)..."
      bind:value={query} on:keydown={e => e.key === 'Enter' && search()} />
    <button class="btn-primary" on:click={search}>Search</button>
  </div>
  {#if loading}
    <div class="skeleton" style="height:200px"></div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else if guides.length === 0 && query}
    <div class="empty-state">No guides found for "{query}".</div>
  {:else}
    <div class="device-grid">
      {#each guides as g}
        <div class="card">
          <div class="card-mfr">{g.category || 'guide'}</div>
          <div class="card-title">{g.title}</div>
          {#if g.description}<div style="font-size:.82rem;color:var(--muted);margin-top:.3rem">{g.description}</div>{/if}
          {#if g.url}
            <div style="margin-top:.5rem">
              <a href={g.url} target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Read guide →</a>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</main>
