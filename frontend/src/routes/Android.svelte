<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let versions = [], filtered = [], loading = true, error = '';
  let statusFilter = '', minApi = '';

  onMount(async () => {
    try {
      const data = await api.androidVersions();
      versions = [...data.versions].reverse();
      filtered = versions;
    } catch(e) { error = e.message; }
    loading = false;
  });

  function applyFilter() {
    filtered = versions.filter(v => {
      if (statusFilter && v.status !== statusFilter) return false;
      if (minApi && v.api_level < parseInt(minApi)) return false;
      return true;
    });
  }
</script>

<main class="container">
  <div class="page-header"><h1>Android versions</h1><p class="page-sub">Complete Android release history</p></div>
  <div class="filters-bar">
    <select bind:value={statusFilter} on:change={applyFilter}
      style="background:var(--card);border:1px solid var(--border);color:var(--text);padding:.5rem .75rem;border-radius:8px;font-size:.85rem">
      <option value="">All statuses</option>
      <option value="active">Active</option>
      <option value="partial">Preview</option>
      <option value="eol">EOL</option>
    </select>
    <input type="number" placeholder="Min API level" bind:value={minApi} on:input={applyFilter}
      style="background:var(--card);border:1px solid var(--border);color:var(--text);padding:.5rem .75rem;border-radius:8px;font-size:.85rem;width:130px" />
    <button class="btn-primary" on:click={applyFilter}>Filter</button>
  </div>

  {#if loading}
    <div class="skeleton" style="height:300px"></div>
  {:else if error}
    <div class="error-state">{error}</div>
  {:else}
    <div style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="border-bottom:1px solid var(--border);color:var(--muted);font-size:.78rem;text-align:left">
            {#each ['Version','Codename','API','Year','Status'] as h}
              <th style="padding:.6rem .8rem">{h}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each filtered as v}
            <tr style="border-bottom:1px solid var(--border)">
              <td style="padding:.65rem .8rem;font-weight:600">Android {v.version_number}</td>
              <td style="padding:.65rem .8rem;color:var(--muted)">{v.codename || '—'}</td>
              <td style="padding:.65rem .8rem;font-family:monospace;color:var(--info)">{v.api_level}</td>
              <td style="padding:.65rem .8rem;color:var(--muted)">{v.release_year || '—'}</td>
              <td style="padding:.65rem .8rem">
                <span class="tag {v.status === 'active' ? 'tag-green' : v.status === 'partial' ? 'tag-orange' : 'tag-gray'}">
                  {v.status === 'active' ? 'Active' : v.status === 'partial' ? 'Preview' : 'EOL'}
                </span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</main>
