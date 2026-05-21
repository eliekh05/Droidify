/* roms.js — ROM listing page */
const LIMIT = 50;
let currentOffset = 0;
let currentParams = {};

async function loadRoms(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;
  const list = document.getElementById('rom-list');
  list.innerHTML = '<div class="skeleton" style="height:200px"></div>';
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.roms({ ...params, limit: LIMIT, offset });
    document.getElementById('results-meta').textContent =
      `${data.total.toLocaleString()} ROM entries found`;

    if (!data.roms.length) {
      list.innerHTML = '<div class="empty-state">No ROMs found.</div>';
      return;
    }

    list.innerHTML = `<div class="rom-list">${data.roms.map(r => `
      <div class="rom-card">
        <div class="rom-header">
          <span class="rom-name">${escHtml(r.name)}</span>
          ${chip('custom', 'gray')}
          ${r.is_official ? chip('official', 'blue') : ''}
        </div>
        <div class="rom-meta">
          ${r.codename ? `<span>Device: <a href="/device.html?c=${encodeURIComponent(r.codename)}">${escHtml(r.codename)}</a></span>` : ''}
          ${r.android_base ? `<span>Android ${escHtml(r.android_base)}</span>` : ''}
          ${r.version_label ? `<span>Branch: ${escHtml(r.version_label)}</span>` : ''}
          <span class="source-tag">via ${escHtml(r.source)}</span>
        </div>
        <div class="rom-links">
          ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Source →</a>` : ''}
          ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
        </div>
      </div>`).join('')}</div>`;

    renderPagination('pagination', data.total, offset, LIMIT, newOff => {
      loadRoms(currentParams, newOff);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  } catch (err) {
    list.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

function getParams() {
  return {
    q:            document.getElementById('rom-search').value.trim() || undefined,
    android_base: document.getElementById('android-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => loadRoms(getParams(), 0));
document.getElementById('rom-search').addEventListener('keydown', e => { if (e.key === 'Enter') loadRoms(getParams(), 0); });
document.getElementById('android-filter').addEventListener('change', () => loadRoms(getParams(), 0));
document.getElementById('rom-search').addEventListener('input', debounce(() => loadRoms(getParams(), 0), 400));

loadRoms({}, 0);
