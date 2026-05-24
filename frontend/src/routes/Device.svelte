<script>
  import { onMount } from 'svelte';
  import { currentRoute, navigate } from '../lib/router.js';
  import { api } from '../lib/api.js';
  import { reveal } from '../lib/reveal.js';

  $: codename = $currentRoute.path.split('/').pop();

  let device = null, loading = true, error = '';

  $: if (codename) loadDevice(codename);

  async function loadDevice(code) {
    loading = true; error = '';
    try {
      device = await api.device(code);
    } catch(e) {
      error = e.message.includes('404') ? `No device found for "${code}"` : e.message;
    }
    loading = false;
  }

  function tagClass(s) {
    return s === 'lineageos' || s === 'grapheneos' ? 'tag-green'
         : s === 'twrp' || s === 'orangefox' ? 'tag-blue'
         : 'tag-gray';
  }
</script>

<main class="container">
  {#if loading}
    <div class="skeleton" style="height:200px;margin-top:2rem"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
      {#each Array(4) as _}<div class="skeleton" style="height:150px"></div>{/each}
    </div>
  {:else if error}
    <div class="page-header">
      <h1>Device not found</h1>
      <p class="page-sub">{error}</p>
    </div>
    <button class="btn-primary" on:click={() => navigate('/devices')}>← Back to devices</button>
  {:else if device}
    <div use:reveal>
      <div class="page-header">
        <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem">
          <button on:click={() => navigate('/devices')}
            style="background:none;border:1px solid var(--border);color:var(--muted);padding:.3rem .7rem;border-radius:7px;font-size:.8rem;cursor:pointer">← Back</button>
        </div>
        <div style="font-size:.78rem;color:var(--muted);margin-bottom:.3rem">{device.manufacturer || ''}</div>
        <h1>{device.model_name || device.codename}</h1>
        <div style="font-family:monospace;color:var(--accent);font-size:.9rem;margin-top:.25rem">{device.codename}</div>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:2rem">
        {#each (device.sources || []) as s}
          <span class="tag {tagClass(s)}">{s}</span>
        {/each}
      </div>
    </div>

    <!-- ROMs -->
    {#if device.roms?.length}
      <section class="section" use:reveal>
        <div class="section-header"><h2>ROMs ({device.roms.length})</h2></div>
        <div class="device-grid">
          {#each device.roms as rom, i}
            <div use:reveal={{ delay: i * 40 }}>
              <div class="card">
                <div class="card-mfr">{rom.source || 'custom'}</div>
                <div class="card-title">{rom.name}</div>
                {#if rom.android_base}<div class="card-codename">Android {rom.android_base}</div>{/if}
                {#if rom.version_label}<div style="font-size:.78rem;color:var(--muted)">{rom.version_label}</div>{/if}
                {#if rom.download_url}
                  <div style="margin-top:.5rem">
                    <a href={rom.download_url} target="_blank" rel="noopener"
                      style="font-size:.78rem;color:var(--accent)">Download →</a>
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      </section>
    {:else}
      <section class="section" use:reveal>
        <div class="section-header"><h2>ROMs</h2></div>
        <div class="empty-state">No ROMs found for this device.</div>
      </section>
    {/if}

    <!-- Recoveries -->
    {#if device.recoveries?.length}
      <section class="section" use:reveal>
        <div class="section-header"><h2>Recoveries ({device.recoveries.length})</h2></div>
        <div class="device-grid">
          {#each device.recoveries as r, i}
            <div use:reveal={{ delay: i * 40 }}>
              <div class="card">
                <div class="card-mfr">{r.recovery_type || 'recovery'}</div>
                <div class="card-title">{r.model_name || r.codename}</div>
                {#if r.download_url}
                  <div style="margin-top:.5rem">
                    <a href={r.download_url} target="_blank" rel="noopener"
                      style="font-size:.78rem;color:var(--accent)">Download →</a>
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      </section>
    {/if}

    <!-- Links -->
    <section class="section" use:reveal>
      <div class="section-header"><h2>Links</h2></div>
      <div style="display:flex;flex-wrap:wrap;gap:.6rem">
        {#if device.wiki_url}
          <a href={device.wiki_url} target="_blank" rel="noopener" class="btn-primary" style="text-decoration:none;font-size:.82rem">LineageOS Wiki</a>
        {/if}
        {#if device.twrp_url}
          <a href={device.twrp_url} target="_blank" rel="noopener" class="btn-primary" style="text-decoration:none;font-size:.82rem;background:var(--card);border:1px solid var(--border);color:var(--text)">TWRP</a>
        {/if}
        {#if device.orangefox_url}
          <a href={device.orangefox_url} target="_blank" rel="noopener" class="btn-primary" style="text-decoration:none;font-size:.82rem;background:var(--card);border:1px solid var(--border);color:var(--text)">OrangeFox</a>
        {/if}
      </div>
    </section>
  {/if}
</main>
