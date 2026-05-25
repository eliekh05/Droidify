(function () {
  'use strict';
  const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const main = document.getElementById('device-main');
  const codename = new URLSearchParams(location.search).get('c');

  if (!codename) {
    main.innerHTML = '<div class="page-header"><h1>No device specified</h1></div><a href="/devices.html" class="btn-primary">← Back to devices</a>';
    return;
  }

  document.title = `${codename} — Droidify`;

  function tagClass(s) {
    return ['lineageos','grapheneos'].includes(s) ? 'tag-green'
         : ['twrp','orangefox'].includes(s)       ? 'tag-blue' : 'tag-gray';
  }

  function romCard(rom) {
    const dl = rom.download_url || (rom.download_urls && rom.download_urls[0]) || '';
    return `<div class="card reveal">
      <div class="card-mfr">${esc(rom.source || 'custom')}</div>
      <div class="card-title">${esc(rom.name)}</div>
      ${rom.android_base ? `<div class="card-codename">Android ${esc(rom.android_base)}</div>` : ''}
      ${rom.version_label ? `<div style="font-size:.78rem;color:var(--muted)">${esc(rom.version_label)}</div>` : ''}
      ${dl ? `<div style="margin-top:.5rem"><a href="${esc(dl)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a></div>` : ''}
    </div>`;
  }

  function render(device) {
    const sources = (device.sources || []).map(s =>
      `<span class="tag ${tagClass(s)}">${esc(s)}</span>`).join('');

    const roms = device.roms?.length
      ? `<section class="section">
          <div class="section-header reveal"><h2>ROMs (${device.roms.length})</h2></div>
          <div class="device-grid stagger-grid">${device.roms.map(romCard).join('')}</div>
        </section>`
      : `<section class="section reveal">
          <div class="section-header"><h2>ROMs</h2></div>
          <div class="empty-state">No ROMs found for this device.</div>
        </section>`;

    const recoveries = device.recoveries?.length
      ? `<section class="section">
          <div class="section-header reveal"><h2>Recoveries (${device.recoveries.length})</h2></div>
          <div class="device-grid stagger-grid">${device.recoveries.map(r => `
            <div class="card reveal">
              <div class="card-mfr">${esc(r.recovery_type || 'recovery')}</div>
              <div class="card-title">${esc(r.model_name || r.codename)}</div>
              ${r.download_url ? `<div style="margin-top:.5rem"><a href="${esc(r.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a></div>` : ''}
            </div>`).join('')}
          </div>
        </section>` : '';

    const links = [
      device.wiki_url      ? `<a href="${esc(device.wiki_url)}" target="_blank" rel="noopener" class="btn-primary" style="text-decoration:none;font-size:.82rem">LineageOS Wiki</a>` : '',
      device.twrp_url      ? `<a href="${esc(device.twrp_url)}" target="_blank" rel="noopener" class="btn-ghost" style="text-decoration:none;font-size:.82rem">TWRP</a>` : '',
      device.orangefox_url ? `<a href="${esc(device.orangefox_url)}" target="_blank" rel="noopener" class="btn-ghost" style="text-decoration:none;font-size:.82rem">OrangeFox</a>` : '',
    ].join('');

    main.innerHTML = `
      <div class="page-header reveal">
        <div style="margin-bottom:.5rem">
          <a href="/devices.html" class="btn-ghost" style="text-decoration:none;font-size:.82rem">← Back</a>
        </div>
        <div style="font-size:.78rem;color:var(--muted);margin-bottom:.3rem">${esc(device.manufacturer || '')}</div>
        <h1>${esc(device.model_name || device.codename)}</h1>
        <div style="font-family:var(--font-mono);color:var(--accent);font-size:.9rem;margin-top:.25rem">${esc(device.codename)}</div>
        ${sources ? `<div class="tags" style="margin-top:.75rem">${sources}</div>` : ''}
      </div>
      ${roms}
      ${recoveries}
      ${links ? `<section class="section reveal"><div class="section-header"><h2>Links</h2></div><div style="display:flex;flex-wrap:wrap;gap:.6rem">${links}</div></section>` : ''}
    `;
    document.title = `${device.model_name || device.codename} — Droidify`;
    if (window._reObserve) window._reObserve();
  }

  async function load(retry = false) {
    if (!retry) {
      main.innerHTML = `<div class="loading-state"><div class="spinner"></div>
        <p style="color:var(--muted)">Loading device data…</p>
        <p style="color:var(--muted);font-size:.78rem;margin-top:.3rem">Fetching ROMs from live sources</p>
      </div>`;
    }
    try {
      const device = await api.device(codename, 20000);
      render(device);
      // If ROMs empty and indexes still warming, retry once after 3s
      if (!retry && (!device.roms || device.roms.length === 0)) {
        setTimeout(() => load(true), 3000);
      }
    } catch(e) {
      const msg = e.message.includes('timed out')
        ? 'Loading timed out — the server is still warming up. Please try again.'
        : e.message.includes('404') ? `Device "${codename}" not found.` : e.message;
      main.innerHTML = `
        <div class="page-header">
          <h1>Could not load device</h1>
          <p class="page-sub" style="color:var(--danger)">${esc(msg)}</p>
        </div>
        <div style="display:flex;gap:.75rem;margin-top:1rem;flex-wrap:wrap">
          <button class="btn-primary" onclick="location.reload()">↺ Retry</button>
          <a href="/devices.html" class="btn-ghost" style="text-decoration:none">← Back to devices</a>
        </div>`;
    }
  }

  load();
})();
