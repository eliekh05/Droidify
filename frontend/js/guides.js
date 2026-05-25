(function () {
  'use strict';
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid  = document.getElementById('guides-grid');
  const input = document.getElementById('codename-input');
  const btn   = document.getElementById('search-btn');

  async function doSearch() {
    const q = input.value.trim();
    if (!q) return;
    grid.innerHTML = '<div class="loading-state"><div class="spinner"></div></div>';
    try {
      const data = await api.guides(q);
      const guides = data.guides || [];
      if (!guides.length) {
        grid.innerHTML = `<div class="empty-state">No guides found for "${esc(q)}".</div>`;
        return;
      }
      grid.innerHTML = guides.map(g=>`<div class="card reveal">
        <div class="card-mfr">${esc(g.guide_type||g.category||'guide')}</div>
        <div class="card-title">${esc(g.title)}</div>
        ${g.description?`<div style="font-size:.82rem;color:var(--muted);margin-top:.3rem;line-height:1.5">${esc(g.description)}</div>`:''}
        ${g.url?`<div style="margin-top:.5rem"><a href="${esc(g.url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Read guide →</a></div>`:''}
      </div>`).join('');
      if (window._reObserve) window._reObserve();
    } catch(e) {
      grid.innerHTML = `<div class="empty-state">${e.message.includes('404')?`No guides found for "${esc(q)}".`:esc(e.message)}</div>`;
    }
  }

  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', e => { if(e.key==='Enter') doSearch(); });
})();
