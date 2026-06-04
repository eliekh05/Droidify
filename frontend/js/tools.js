(function () {
  'use strict';

  const esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  const input = document.getElementById('search-input');
  const btn   = document.getElementById('search-btn');
  let allTools = [];

  api.tools().then(data => {
    allTools = data.tools || data;
    render(allTools);
  }).catch(e => {
    grid.innerHTML = `<div class="column"><div class="error-state">${esc(e.message)}</div></div>`;
  });

  function render(tools) {
    if (!tools.length) {
      grid.innerHTML = '<div class="column"><div class="empty-state">No tools found.</div></div>';
      return;
    }
    grid.innerHTML = tools.map((t, i) => {
      const ver    = t.latest_version || '';
      const dlUrl  = (t.download_urls && t.download_urls[0]) || t.release_url || t.official_url || '';
      const status = t.status === 'discontinued' ? '<span class="tag is-danger is-light ml-1">discontinued</span>' : '';
      return `<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*50}">
        <div class="card">
          <div class="card-content">
            <div class="card-mfr">${esc(t.category || '')}</div>
            <p class="title is-6 mb-1">${esc(t.name)}${status}</p>
            ${t.description ? `<p class="card-sub">${esc(t.description)}</p>` : ''}
            ${ver ? `<div class="card-codename">${esc(ver)}</div>` : ''}
            ${dlUrl ? `<a href="${esc(dlUrl)}" target="_blank" rel="noopener" class="card-link">Download →</a>` : ''}
          </div>
        </div>
      </div>`;
    }).join('');
    if (window.AOS) AOS.refresh();
  }

  function doSearch() {
    const q = input.value.trim().toLowerCase();
    render(q ? allTools.filter(t =>
      (t.name || '').toLowerCase().includes(q) ||
      (t.description || '').toLowerCase().includes(q) ||
      (t.category || '').toLowerCase().includes(q)
    ) : allTools);
  }

  btn.addEventListener('click', doSearch);
  input.addEventListener('input', doSearch);
})();
