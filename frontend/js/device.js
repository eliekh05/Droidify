(function () {
  'use strict';
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const main     = document.getElementById('device-main');
  const codename = new URLSearchParams(location.search).get('c');

  if (!codename) {
    main.innerHTML = '<div class="page-header"><h1 class="title">No device specified</h1></div><a href="/devices.html" class="button is-primary">← Back to devices</a>';
    return;
  }
  document.title = `${codename} — Droidify`;

  function tagClass(s) {
    return ['lineageos','grapheneos'].includes(s) ? 'is-success'
         : ['twrp','orangefox'].includes(s)       ? 'is-info' : 'is-dark';
  }

  function render(device) {
    const sources = (device.sources||[]).map(s => `<span class="tag ${tagClass(s)}">${esc(s)}</span>`).join('');
    const roms = device.roms?.length
      ? device.roms.map((rom, i) => {
          const dl = rom.download_url||(rom.download_urls&&rom.download_urls[0])||'';
          return `<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*40}">
            <div class="card">
              <div class="card-content">
                <div class="card-mfr">${esc(rom.source||'custom')}</div>
                <p class="title is-6 mb-1">${esc(rom.name)}</p>
                ${rom.android_base?`<div class="card-codename">Android ${esc(rom.android_base)}</div>`:''}
                ${rom.version_label?`<p style="font-size:.78rem;color:let(--muted)">${esc(rom.version_label)}</p>`:''}
                ${dl?`<a href="${esc(dl)}" target="_blank" rel="noopener" style="font-size:.78rem;color:let(--accent)">Download →</a>`:''}
              </div>
            </div>
          </div>`;
        }).join('')
      : '<div class="column"><div class="empty-state">No ROMs found for this device.</div></div>';

    const recoveries = device.recoveries?.length
      ? device.recoveries.map((r,i) =>
          `<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*40}">
            <div class="card">
              <div class="card-content">
                <div class="card-mfr">${esc(r.recovery_type||'recovery')}</div>
                <p class="title is-6 mb-1">${esc(r.model_name||r.codename)}</p>
                ${r.download_url?`<a href="${esc(r.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:let(--accent)">Download →</a>`:''}
              </div>
            </div>
          </div>`
        ).join('') : '';

    const samfw = (device.stock_firmware||[]).map((f,i) =>
      `<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${i*40}">
        <div class="card">
          <div class="card-content">
            <div class="card-mfr">Stock Firmware</div>
            <p class="title is-6 mb-1">${esc(f.model)}</p>
            <p style="font-size:.82rem;color:let(--muted);margin:.3rem 0">${esc(f.description)}</p>
            <a href="${esc(f.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:let(--accent)">Download on SamFW →</a>
          </div>
        </div>
      </div>`
    ).join('');

    const links = [
      device.wiki_url ? `<a href="${esc(device.wiki_url)}" target="_blank" rel="noopener" class="button is-primary mr-2 mb-2">LineageOS Wiki</a>` : '',
      device.twrp_url ? `<a href="${esc(device.twrp_url)}" target="_blank" rel="noopener" class="button is-ghost mr-2 mb-2">TWRP</a>` : '',
      device.orangefox_url ? `<a href="${esc(device.orangefox_url)}" target="_blank" rel="noopener" class="button is-ghost mr-2 mb-2">OrangeFox</a>` : '',
    ].join('');

    main.innerHTML = `
      <div class="page-header" data-aos="fade-up">
        <div class="mb-3"><a href="/devices.html" class="button is-ghost">← Back</a></div>
        <p style="font-size:.78rem;color:let(--muted);margin-bottom:.3rem">${esc(device.manufacturer||'')}</p>
        <h1 class="title">${esc(device.model_name||device.codename)}</h1>
        <p style="font-family:let(--mono);color:let(--accent);font-size:.9rem">${esc(device.codename)}</p>
        ${sources?`<div class="tags mt-3">${sources}</div>`:''}
      </div>

      <section class="section pb-0">
        <div class="section-header" data-aos="fade-up">
          <h2 class="title is-6">ROMs${device.roms?.length?` (${device.roms.length})`:''}</h2>
        </div>
        <div class="columns is-multiline is-mobile">${roms}</div>
      </section>

      ${recoveries?`<section class="section pb-0">
        <div class="section-header" data-aos="fade-up">
          <h2 class="title is-6">Recoveries (${device.recoveries.length})</h2>
        </div>
        <div class="columns is-multiline is-mobile">${recoveries}</div>
      </section>`:''}

      ${samfw?`<section class="section pb-0">
        <div class="section-header" data-aos="fade-up">
          <h2 class="title is-6">Stock Firmware</h2>
        </div>
        <div class="columns is-multiline is-mobile">${samfw}</div>
      </section>`:''}

      ${links?`<section class="section" data-aos="fade-up">
        <div class="section-header"><h2 class="title is-6">Links</h2></div>
        <div>${links}</div>
      </section>`:''}
    `;
    document.title = `${device.model_name||device.codename} — Droidify`;
    if (window.AOS) AOS.refresh();
  }

  async function load(retry=false) {
    if (!retry) {
      main.innerHTML = `<div style="padding:3rem 0;text-align:center">
        <div class="spinner"></div>
        <p style="color:let(--muted)">Loading device data…</p>
      </div>`;
    }
    try {
      const device = await api.device(codename, 20000);
      render(device);
      if (!retry && (!device.roms||!device.roms.length)) {
        setTimeout(() => load(true), 3000);
      }
    } catch(e) {
      const msg = e.message.includes('timed out')
        ? 'Loading timed out — the server is still warming up. Please try again.'
        : e.message.includes('404') ? `Device "${codename}" not found.` : e.message;
      main.innerHTML = `
        <div class="page-header">
          <h1 class="title">Could not load device</h1>
          <p class="subtitle" style="color:let(--danger)">${esc(msg)}</p>
        </div>
        <button class="button is-primary mr-2" onclick="location.reload()">↺ Retry</button>
        <a href="/devices.html" class="button is-ghost">← Back to devices</a>`;
    }
  }
  load();
})();
