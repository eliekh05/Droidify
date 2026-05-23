/* recoveries.js — Recovery listing page */
const LIMIT = 50;
let currentOffset = 0;
let currentParams = {};

async function loadRecoveries(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;
  const grid = document.getElementById('rec-grid');
  grid.innerHTML = Array(6).fill('<div class="card skeleton"></div>').join('');
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.recoveries({ ...params, limit: LIMIT, offset });
    document.getElementById('results-meta').textContent =
      `${data.total.toLocaleString()} recovery entries (TWRP + OrangeFox)`;

    if (!data.recoveries.length) {
      grid.innerHTML = '<div class="empty-state">No recoveries found.</div>';
      return;
    }

    grid.innerHTML = data.recoveries.map(r => {
      const cc = r.recovery === 'OrangeFox' ? 'orange' : 'blue';
      return `<div class="card">
        <div class="card-top">
          <div>
            <div class="card-mfr">${escHtml(r.manufacturer || '')}</div>
            <div class="card-title">${escHtml(r.model_name || r.codename)}</div>
            <div class="card-codename">${escHtml(r.codename)}</div>
          </div>
          ${chip(r.recovery, cc)}
        </div>
        <div class="tags" style="margin-top:.5rem">
          ${chip(r.status === 'active' ? 'Active' : r.status, r.status === 'active' ? 'green' : 'gray')}
        </div>
        <div class="rom-links" style="margin-top:.65rem">
          ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Info →</a>` : ''}
          ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
        </div>
      </div>`;
    }).join('');

    renderPagination('pagination', data.total, offset, LIMIT, newOff => {
      loadRecoveries(currentParams, newOff);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Populate manufacturer filter
    if (offset === 0 && !params.manufacturer) {
      const mfrs = [...new Set(data.recoveries.map(r => r.manufacturer).filter(Boolean))].sort();
      const sel = document.getElementById('mfr-filter');
      mfrs.forEach(m => {
        const o = document.createElement('option');
        o.value = m; o.textContent = m; sel.appendChild(o);
      });
    }
  } catch (err) {
    grid.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

function getParams() {
  return {
    q:            document.getElementById('rec-search').value.trim() || undefined,
    recovery:     document.getElementById('rec-filter').value || undefined,
    manufacturer: document.getElementById('mfr-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => loadRecoveries(getParams(), 0));
document.getElementById('rec-search').addEventListener('keydown', e => { if (e.key === 'Enter') loadRecoveries(getParams(), 0); });
document.getElementById('rec-filter').addEventListener('change', () => loadRecoveries(getParams(), 0));
document.getElementById('mfr-filter').addEventListener('change', () => loadRecoveries(getParams(), 0));
document.getElementById('rec-search').addEventListener('input', debounce(() => loadRecoveries(getParams(), 0), 400));

loadRecoveries({}, 0);