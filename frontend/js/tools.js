(function () {
  'use strict';
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid  = document.getElementById('tools-grid');
  const input = document.getElementById('search-input');
  const btn   = document.getElementById('search-btn');
  let allTools = [];

  api.tools().then(data => {
    allTools = data.tools || data;
    render(allTools);
  }).catch(e => { grid.innerHTML=`<div class="error-state">${esc(e.message)}</div>`; });

  function render(tools) {
    grid.innerHTML = tools.map(t=>`<div class="card reveal">
      <div class="card-title">${esc(t.name)}</div>
      ${t.description?`<div style="font-size:.82rem;color:var(--muted);margin:.3rem 0;line-height:1.5">${esc(t.description)}</div>`:''}
      ${t.version?`<div class="card-codename">v${esc(t.version)}</div>`:''}
      ${t.download_url?`<div style="margin-top:.5rem"><a href="${esc(t.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a></div>`:''}
    </div>`).join('');
    if (window._reObserve) window._reObserve();
  }

  function doSearch() {
    const q = input.value.trim().toLowerCase();
    render(q ? allTools.filter(t =>
      (t.name||'').toLowerCase().includes(q) ||
      (t.description||'').toLowerCase().includes(q)
    ) : allTools);
  }
  btn.addEventListener('click', doSearch);
  input.addEventListener('input', doSearch);
})();
