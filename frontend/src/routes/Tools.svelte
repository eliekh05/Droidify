<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let tools = [], loading = true, error = '', query = '';
  let allTools = [];

  onMount(async () => {
    try {
      const data = await api.tools();
      allTools = data.tools || data;
      tools = allTools;
    } catch(e) { error = e.message; }
    loading = false;
  });

  function search() {
    const q = query.toLowerCase();
    tools = q ? allTools.filter(t =>
      (t.name || '').toLowerCase().includes(q) ||
      (t.description || '').toLowerCase().includes(q)
    ) : allTools;
  }
</script>

<main class="container">
  <div class="page-header"><h1>Tools</h1><p class="page-sub">Root, flash, and Android development tools</p></div>
  <div class="filters-bar">
    <input class="search-input" type="search" placeholder="Search tools..."
      bind:value={query} on:keydown={e => e.key === 'Enter' && search()}
      on:input={search} />
    <button class="btn-primary" on:click={search}>Search</button>
  </div>
  {#if loading}
    <div class="device-grid">{#each Array(8) as _}<div class="skeleton" style="height:110px"></div>{/each}</div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else}
    <div class="device-grid">
      {#each tools as t}
        <div class="card">
          <div class="card-title">{t.name}</div>
          {#if t.description}<div style="font-size:.82rem;color:var(--muted);margin:.3rem 0">{t.description}</div>{/if}
          {#if t.version}<div class="card-codename">v{t.version}</div>{/if}
          {#if t.download_url}
            <div style="margin-top:.5rem">
              <a href={t.download_url} target="_blank" rel="noopener"
                style="font-size:.78rem;color:var(--accent)">Download →</a>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</main>
