(function () {
  'use strict';
  const LIMIT = 24;
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid    = document.getElementById('device-grid');
  const metaEl  = document.getElementById('results-meta');
  const paginEl = document.getElementById('pagination');
  const input   = document.getElementById('search-input');
  const btn     = document.getElementById('search-btn');
  const params  = new URLSearchParams(location.search);
  let currentQ  = params.get('q') || '';
  input.value   = currentQ;

  function cardHTML(d, i) {
    const tags = [
      d.has_lineageos  ? '<span class="tag is-success">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag is-info">GrapheneOS</span>'   : '',
      d.has_twrp       ? '<span class="tag is-info">TWRP</span>'         : '',
      d.has_orangefox  ? '<span class="tag is-warning">OrangeFox</span>' : '',
    ].join('');
    return `<div class="column is-6-mobile is-4-tablet is-4-desktop" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*60}">
      <div class="card" style="cursor:pointer" onclick="location.href='/device.html?c=${esc(d.codename)}'">
        <div class="card-content">
          <div class="card-mfr">${esc(d.manufacturer||'Unknown')}</div>
          <p class="title is-6 mb-1">${esc(d.model_name||d.codename)}</p>
          <div class="card-codename">${esc(d.codename)}</div>
          ${tags ? `<div class="tags">${tags}</div>` : ''}
        </div>
      </div>
    </div>`;
  }

  function renderPagination(total, offset) {
    const pages = Math.ceil(total/LIMIT), cur = Math.floor(offset/LIMIT);
    if (pages <= 1) { paginEl.innerHTML = ''; return; }
    let h = `<a class="pagination-previous button${cur===0?' is-disabled':''}" onclick="loadDevices(${(cur-1)*LIMIT})">Prev</a>`;
    h += `<a class="pagination-next button${cur>=pages-1?' is-disabled':''}" onclick="loadDevices(${(cur+1)*LIMIT})">Next</a><ul class="pagination-list">`;
    const s = Math.max(0,cur-3), e = Math.min(pages-1,cur+3);
    for (let i=s;i<=e;i++)
      h += `<li><a class="pagination-link button${i===cur?' is-current':''}" onclick="loadDevices(${i*LIMIT})">${i+1}</a></li>`;
    h += '</ul>';
    paginEl.innerHTML = h;
  }

  window.loadDevices = async function(offset=0) {
    grid.innerHTML = Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:110px"></div></div>').join('');
    metaEl.textContent = '';
    try {
      const data = await api.devices({ q: currentQ||undefined, limit: LIMIT, offset });
      if (!data.devices.length) {
        grid.innerHTML = '<div class="column"><div class="empty-state">No devices found.</div></div>';
        return;
      }
      metaEl.className = 'results-meta';
      metaEl.textContent = `${data.total.toLocaleString()} device${data.total!==1?'s':''}${currentQ?` for "${currentQ}"`: ''}`;
      grid.innerHTML = data.devices.map(cardHTML).join('');
      renderPagination(data.total, offset);
      if (window.AOS) AOS.refresh();
      if (offset) window.scrollTo({ top:0, behavior:'smooth' });
    } catch(e) {
      grid.innerHTML = `<div class="column"><div class="error-state">${esc(e.message)}</div></div>`;
    }
  };

  function doSearch() {
    currentQ = input.value.trim();
    const url = new URL(location.href);
    currentQ ? url.searchParams.set('q', currentQ) : url.searchParams.delete('q');
    history.pushState({}, '', url);
    loadDevices(0);
  }
  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', e => { if (e.key==='Enter') doSearch(); });
  loadDevices(0);
})();
