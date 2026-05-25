(function () {
  'use strict';
  const LIMIT = 24;
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid    = document.getElementById('rom-grid');
  const metaEl  = document.getElementById('results-meta');
  const paginEl = document.getElementById('pagination');
  const input   = document.getElementById('search-input');
  const btn     = document.getElementById('search-btn');

  const params = new URLSearchParams(location.search);
  let currentQ = params.get('q') || '';
  input.value = currentQ;

  function pagination(total, offset) {
    const pages = Math.ceil(total/LIMIT), cur = Math.floor(offset/LIMIT);
    if (pages <= 1) { paginEl.innerHTML=''; return; }
    let h = cur>0 ? `<button class="page-btn" onclick="load(${(cur-1)*LIMIT})">←</button>` : '';
    for (let i=Math.max(0,cur-3); i<=Math.min(pages-1,cur+3); i++)
      h += `<button class="page-btn${i===cur?' active':''}" onclick="load(${i*LIMIT})">${i+1}</button>`;
    if (cur<pages-1) h += `<button class="page-btn" onclick="load(${(cur+1)*LIMIT})">→</button>`;
    paginEl.innerHTML = h;
  }

  window.load = async function(offset=0) {
    grid.innerHTML = Array(6).fill('<div class="skeleton" style="height:90px"></div>').join('');
    try {
      const data = await api.roms({ q: currentQ||undefined, limit:LIMIT, offset });
      metaEl.className='results-meta';
      metaEl.textContent = `${data.total.toLocaleString()} ROM${data.total!==1?'s':''}`;
      grid.innerHTML = data.roms.length
        ? data.roms.map(r => `<div class="card reveal">
            <div class="card-mfr">${esc(r.source||'custom')}</div>
            <div class="card-title">${esc(r.name)}</div>
            <div class="card-codename">${esc(r.codename)}</div>
            ${r.android_base?`<div style="font-size:.78rem;color:var(--muted)">Android ${esc(r.android_base)}</div>`:''}
            ${r.download_url?`<div style="margin-top:.5rem"><a href="${esc(r.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a></div>`:''}
          </div>`).join('')
        : '<div class="empty-state">No ROMs found.</div>';
      pagination(data.total, offset);
      if (window._reObserve) window._reObserve();
      if (offset) window.scrollTo({ top:0, behavior:'smooth' });
    } catch(e) { grid.innerHTML=`<div class="error-state">${esc(e.message)}</div>`; }
  };

  function doSearch() {
    currentQ = input.value.trim();
    const url = new URL(location.href);
    currentQ ? url.searchParams.set('q',currentQ) : url.searchParams.delete('q');
    history.pushState({}, '', url);
    load(0);
  }
  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', e => { if(e.key==='Enter') doSearch(); });
  load(0);
})();
