(function () {
  'use strict';

  const esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  const LIMIT = 20;

  const safeUrl = function (u) {
    if (!u) return '#';
    var s = String(u).trim();
    return /^https?:\/\//i.test(s) ? s : '#';
  };

  const grid    = document.getElementById('rom-grid');
  const metaEl  = document.getElementById('results-meta');
  const paginEl = document.getElementById('pagination');
  const input   = document.getElementById('search-input');
  const btn     = document.getElementById('search-btn');
  let currentQ  = new URLSearchParams(location.search).get('q') || '';
  input.value   = currentQ;

  function renderPagination(total, offset) {
    const pages=Math.ceil(total/LIMIT),cur=Math.floor(offset/LIMIT);
    if (pages<=1) { paginEl.innerHTML=''; return; }
    let h = `<a class="pagination-previous button${cur===0?' is-disabled':''}" onclick="load(${(cur-1)*LIMIT})">Prev</a>`;
    h += `<a class="pagination-next button${cur>=pages-1?' is-disabled':''}" onclick="load(${(cur+1)*LIMIT})">Next</a><ul class="pagination-list">`;
    for (let i=Math.max(0,cur-3);i<=Math.min(pages-1,cur+3);i++)
      h += `<li><a class="pagination-link button${i===cur?' is-current':''}" onclick="load(${i*LIMIT})">${i+1}</a></li>`;
    h += '</ul>';
    paginEl.innerHTML = h;
  }

  window.load = async function(offset=0) {
    grid.innerHTML = Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:90px"></div></div>').join('');
    try {
      const data = await api.roms({ q:currentQ||undefined, limit:LIMIT, offset });
      metaEl.className='results-meta';
      metaEl.textContent=`${data.total.toLocaleString()} ROM${data.total!==1?'s':''}`;
      grid.innerHTML = data.roms.length
        ? data.roms.map((r,i)=>`<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*40}">
            <div class="card">
              <div class="card-content">
                <div class="card-mfr">${esc(r.source||'custom')}</div>
                <p class="title is-6 mb-1">${esc(r.name)}</p>
                <div class="card-codename">${esc(r.codename)}</div>
                ${r.android_base?`<p style="font-size:.78rem;color:var(--muted)">Android ${esc(r.android_base)}</p>`:''}
                ${r.download_url?`<a href="${safeUrl(r.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>`:''}
              </div>
            </div>
          </div>`).join('')
        : '<div class="column"><div class="empty-state">No ROMs found.</div></div>';
      renderPagination(data.total, offset);
      if (window.AOS) AOS.refresh();
      if (offset) window.scrollTo({top:0,behavior:'smooth'});
    } catch(e) { grid.innerHTML=`<div class="column"><div class="error-state">${esc(e.message)}</div></div>`; }
  };

  function doSearch() {
    currentQ = input.value.trim();
    const url = new URL(location.href);
    currentQ ? url.searchParams.set('q',currentQ) : url.searchParams.delete('q');
    history.pushState({}, '', url);
    load(0);
  }
  btn.addEventListener('click',doSearch);
  input.addEventListener('keydown',e=>{if(e.key==='Enter')doSearch();});
  load(0);
})();
