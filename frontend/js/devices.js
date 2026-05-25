(function () {
  'use strict';
  const LIMIT = 24;
  const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const searchInput = document.getElementById('search-input');
  const searchBtn   = document.getElementById('search-btn');
  const grid        = document.getElementById('device-grid');
  const metaEl      = document.getElementById('results-meta');
  const paginEl     = document.getElementById('pagination');

  const params = new URLSearchParams(location.search);
  let currentQ = params.get('q') || '';
  let currentOffset = 0;

  searchInput.value = currentQ;

  function deviceCardHTML(d) {
    const tags = [
      d.has_lineageos  ? '<span class="tag tag-green">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag tag-blue">GrapheneOS</span>' : '',
      d.has_twrp       ? '<span class="tag tag-blue">TWRP</span>'       : '',
      d.has_orangefox  ? '<span class="tag tag-orange">OrangeFox</span>': '',
    ].join('');
    return `<div class="card reveal" style="cursor:pointer" onclick="location.href='/device.html?c=${esc(d.codename)}'">
      <div class="card-mfr">${esc(d.manufacturer || 'Unknown')}</div>
      <div class="card-title">${esc(d.model_name || d.codename)}</div>
      <div class="card-codename">${esc(d.codename)}</div>
      ${tags ? `<div class="tags">${tags}</div>` : ''}
    </div>`;
  }

  function renderPagination(total, offset) {
    const pages = Math.ceil(total / LIMIT);
    const current = Math.floor(offset / LIMIT);
    if (pages <= 1) { paginEl.innerHTML = ''; return; }
    let html = '';
    if (current > 0) html += `<button class="page-btn" onclick="loadDevices(${(current-1)*LIMIT})">←</button>`;
    const start = Math.max(0, current - 3);
    const end   = Math.min(pages - 1, current + 3);
    for (let i = start; i <= end; i++) {
      html += `<button class="page-btn${i===current?' active':''}" onclick="loadDevices(${i*LIMIT})">${i+1}</button>`;
    }
    if (current < pages - 1) html += `<button class="page-btn" onclick="loadDevices(${(current+1)*LIMIT})">→</button>`;
    paginEl.innerHTML = html;
  }

  window.loadDevices = async function(offset = 0) {
    currentOffset = offset;
    grid.innerHTML = Array(6).fill('<div class="skeleton" style="height:110px"></div>').join('');
    metaEl.textContent = '';
    try {
      const data = await api.devices({ q: currentQ || undefined, limit: LIMIT, offset });
      if (data.devices.length === 0) {
        grid.innerHTML = '<div class="empty-state">No devices found. Try a different search.</div>';
        metaEl.textContent = '';
      } else {
        metaEl.className = 'results-meta';
        metaEl.textContent = `${data.total.toLocaleString()} device${data.total !== 1 ? 's' : ''}${currentQ ? ` for "${currentQ}"` : ''}`;
        grid.innerHTML = data.devices.map(deviceCardHTML).join('');
        if (window._reObserve) window._reObserve();
        renderPagination(data.total, offset);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } catch(e) {
      grid.innerHTML = `<div class="error-state">Error: ${e.message}</div>`;
    }
  };

  function doSearch() {
    currentQ = searchInput.value.trim();
    const url = new URL(location.href);
    currentQ ? url.searchParams.set('q', currentQ) : url.searchParams.delete('q');
    history.pushState({}, '', url);
    loadDevices(0);
  }

  searchBtn.addEventListener('click', doSearch);
  searchInput.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });

  loadDevices(0);
})();
