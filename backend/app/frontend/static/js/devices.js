/* devices.js — Device listing page */

const LIMIT = 24;
let currentOffset = 0;
let currentParams = {};

// Read URL params on load
const urlP = new URLSearchParams(window.location.search);
if (urlP.get('q')) document.getElementById('device-search').value = urlP.get('q');
if (urlP.get('manufacturer')) document.getElementById('mfr-filter').value = urlP.get('manufacturer');

async function loadDevices(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;

  const grid = document.getElementById('device-grid');
  grid.innerHTML = Array(6).fill('<div class="card skeleton"></div>').join('');
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.devices({ ...params, limit: LIMIT, offset });
    const { devices, total } = data;

    document.getElementById('results-meta').textContent =
      `${total.toLocaleString()} device${total !== 1 ? 's' : ''}${params.q ? ` for "${params.q}"` : ''}`;

    if (!devices.length) {
      grid.innerHTML = '<div class="empty-state">No devices found. Try a different search.</div>';
      document.getElementById('pagination').innerHTML = '';
      return;
    }

    // Remove .visible before swap so animation restarts cleanly on new nodes
    grid.classList.remove('visible');
    grid.innerHTML = devices.map(deviceCardHTML).join('');
    // Force reflow so browser registers the class removal before re-adding
    void grid.offsetHeight;
    grid.classList.add('visible');

    renderPagination('pagination', total, offset, LIMIT, newOffset => {
      loadDevices(currentParams, newOffset);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Populate manufacturer filter dynamically on first load
    if (offset === 0 && !params.manufacturer) {
      await populateMfrFilter();
    }
  } catch (err) {
    grid.innerHTML = `<div class="error-state">Error: ${escHtml(err.message)}</div>`;
  }
}

);
    const mfrs = [...new Set(data.devices.map(d => d.manufacturer).filter(Boolean))].sort();
    const sel  = document.getElementById('mfr-filter');
    const current = sel.value;
    mfrs.forEach(m => {
      const opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m;
      if (m === current) opt.selected = true;
      sel.appendChild(opt);
    });
  } catch (e) { /* ignore */ }
}

function getParams() {
  return {
    q:            document.getElementById('device-search').value.trim() || undefined,
    manufacturer: document.getElementById('mfr-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => {
  loadDevices(getParams(), 0);
});

document.getElementById('device-search').addEventListener('keydown', e => {
  if (e.key === 'Enter') loadDevices(getParams(), 0);
});

const debouncedSearch = debounce(() => loadDevices(getParams(), 0), 400);
document.getElementById('device-search').addEventListener('input', debouncedSearch);

document.getElementById('mfr-filter').addEventListener('change', () => loadDevices(getParams(), 0));

// Source filter (client-side since API doesn't expose it directly)
document.getElementById('source-filter').addEventListener('change', function() {
  // Will be applied on next load as a filter hint in params
  loadDevices(getParams(), 0);
});

// Initial load
loadDevices({ q: urlP.get('q') || undefined }, 0);