/* device-detail.js — Device detail page */

const codename = new URLSearchParams(window.location.search).get('c');
if (!codename) window.location.href = '/devices.html';

document.title = `${codename} — Droidify`;

function romCardHTML(rom) {
  const android = rom.android_base ? `<span>Android ${escHtml(rom.android_base)}</span>` : '';
  const ver     = rom.version_label ? `<span>v${escHtml(rom.version_label)}</span>` : '';
  const maint   = rom.maintainer ? `<span>by ${escHtml(rom.maintainer)}</span>` : '';
  const src     = rom.source ? `<span class="source-tag">via ${escHtml(rom.source)}</span>` : '';

  const links = (rom.download_urls || []).map((u, i) =>
    `<a href="${escHtml(u)}" target="_blank" rel="noopener" class="rom-link">
      Download${(rom.download_urls?.length || 0) > 1 ? ' ' + (i+1) : ''} →
    </a>`
  ).join('');
  const srcLink = rom.source_url
    ? `<a href="${escHtml(rom.source_url)}" target="_blank" rel="noopener" class="rom-link">Source →</a>`
    : '';

  return `
    <div class="rom-card">
      <div class="rom-header">
        <span class="rom-name">${escHtml(rom.name)}</span>
        ${chip(rom.status === 'active' ? 'Active' : 'Discontinued', rom.status === 'active' ? 'green' : 'gray')}
        ${rom.is_official ? chip('Official', 'blue') : chip('Unofficial', 'gray')}
        ${chip('custom ROM', 'gray')}
      </div>
      <div class="rom-meta">${android}${ver}${maint}${src}</div>
      ${rom.description ? `<div class="card-sub" style="margin-top:.4rem">${escHtml(rom.description)}</div>` : ''}
      <div class="rom-links">${srcLink}${links}</div>
    </div>`;
}

function recoveryCardHTML(r) {
  const chip_color = r.recovery === 'OrangeFox' ? 'orange' : 'blue';
  return `
    <div class="rec-card" style="margin-bottom:.6rem">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.4rem">
        <span style="font-weight:600">${chip(r.recovery, chip_color)} ${escHtml(r.model_name || codename)}</span>
        ${r.status !== 'active' ? chip(r.status, 'gray') : ''}
      </div>
      <div style="margin-top:.5rem;display:flex;gap:.75rem;flex-wrap:wrap">
        ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Info →</a>` : ''}
        ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
      </div>
    </div>`;
}

async function loadDevice() {
  const content = document.getElementById('device-content');
  try {
    const d = await api.device(codename);
    document.title = `${d.model_name || codename} — Droidify`;

    const specRows = [
      ['SoC', d.soc],
      ['RAM', d.ram],
      ['CPU', d.cpu],
      ['GPU', d.gpu],
      ['Architecture', d.architecture],
      ['Released', d.released],
    ].filter(([, v]) => v).map(([k, v]) => `
      <div class="spec-item">
        <span class="spec-key">${escHtml(k)}</span>
        <span class="spec-val">${escHtml(v)}</span>
      </div>`).join('');

    const sourceTags = (d.sources || []).map(s => chip(s, 'gray')).join(' ');

    const roms = d.roms || [];
    const recoveries = d.recoveries || [];

    const limitedNote = !d.has_lineageos && roms.length < 2
      ? `<div class="detail-note">⚠ LIMITED ROM ECOSYSTEM — fewer than 2 ROM families found for this device across all indexed sources.</div>`
      : roms.length === 1
        ? `<div class="detail-note">⚠ ONLY ONE VERIFIED ROM FOUND — scraper discovery may be incomplete for this codename.</div>`
        : '';

    content.innerHTML = `
      <div class="detail-header">
        <div class="detail-mfr">${escHtml(d.manufacturer || '')}</div>
        <div class="detail-title">${escHtml(d.model_name || d.codename)}</div>
        <div class="detail-codename">${escHtml(d.codename)}</div>
        <div class="tags" style="margin-top:.65rem">
          ${sourceTags}
          ${d.has_lineageos ? chip('LineageOS', 'green') : ''}
          ${d.has_twrp ? chip('TWRP', 'blue') : ''}
          ${d.has_orangefox ? chip('OrangeFox', 'orange') : ''}
        </div>
        ${specRows ? `<div class="specs-grid" style="margin-top:1.1rem">${specRows}</div>` : ''}
        ${limitedNote}
      </div>

      <div class="section-title">ROMs (${roms.length} found)</div>
      ${roms.length
        ? `<div class="rom-list">${roms.map(romCardHTML).join('')}</div>`
        : '<div class="empty-state">No ROMs found in indexed sources for this device.</div>'}

      <div style="margin-top:1rem">
        <a href="/guides.html?c=${encodeURIComponent(codename)}&m=${encodeURIComponent(d.manufacturer||'')}"
           class="btn" style="display:inline-block">
          📖 View flashing &amp; root guides for ${escHtml(codename)} →
        </a>
      </div>

      ${recoveries.length ? `
        <div class="section-title">Recoveries (${recoveries.length})</div>
        <div>${recoveries.map(recoveryCardHTML).join('')}</div>
      ` : ''}

      <div style="margin-top:1.5rem;font-size:.78rem;color:var(--muted)">
        Data sourced live from: LineageOS · OrangeFox · TWRP · crDroid · GrapheneOS · DivestOS · CalyxOS · /e/OS.
        All sources free, no authentication required.
      </div>`;
  } catch (err) {
    content.innerHTML = `
      <div class="error-state">
        Device "<strong>${escHtml(codename)}</strong>" not found in any indexed source.<br>
        <a href="/devices.html" style="color:var(--accent)">← Back to devices</a>
      </div>`;
  }
}

loadDevice();