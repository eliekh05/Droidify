(function () {
  'use strict';
  const esc = s => String(s || '').replace(/[&<>"']/g, c =>
    ({'&':'&amp;
// safeUrl: only allow http/https URLs — strips javascript:, data:, etc.
  const safeUrl = u => {
    if (!u) return '#';
    const s = String(u).trim();
    if (/^https?:\/\//i.test(s)) return s;
    return '#';
  };','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const grid  = document.getElementById('guides-grid');
  const input = document.getElementById('codename-input');
  const btn   = document.getElementById('search-btn');

  // Load and render global guides on page load
  async function loadGlobal() {
    try {
      const data  = await api.guides('');
      const items = data.guides || [];
      if (items.length) renderGuides(items, true);
    } catch (_) { /* silently ignore — global guides optional */ }
  }

  async function doSearch() {
    const q = input.value.trim();
    if (!q) { loadGlobal(); return; }
    grid.innerHTML = '<div class="column"><div style="padding:2rem;text-align:center"><div class="spinner"></div></div></div>';
    try {
      const data   = await api.guides(q);
      const guides = data.guides || [];
      if (!guides.length) {
        grid.innerHTML = `<div class="column"><div class="empty-state">No guides found for <strong>${esc(q)}</strong>.</div></div>`;
        return;
      }
      renderGuides(guides, false);
    } catch (e) {
      grid.innerHTML = `<div class="column"><div class="empty-state">${
        e.message.includes('404')
          ? `No guides for <strong>${esc(q)}</strong>. Try a codename like <code>beryllium</code> or <code>sargo</code>.`
          : esc(e.message)
      }</div></div>`;
    }
  }

  function renderGuides(guides, isGlobal) {
    const header = isGlobal
      ? '<div class="column is-12"><p class="section-label">Universal guides</p></div>'
      : '';
    grid.innerHTML = header + guides.map((g, i) => {
      const url  = g.source_url || g.url || '';
      const type = g.guide_type || g.category || 'guide';
      const steps = Array.isArray(g.steps) && g.steps.length
        ? `<details class="guide-steps mt-2"><summary class="card-link">Steps (${g.steps.length})</summary>
            <ol class="guide-ol">${g.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>
            ${g.notes ? `<p class="guide-notes">${esc(g.notes)}</p>` : ''}
           </details>`
        : '';
      return `<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*50}">
        <div class="card">
          <div class="card-content">
            <div class="card-mfr">${esc(type)}</div>
            <p class="title is-6 mb-1">${esc(g.title || 'Guide')}</p>
            ${g.description ? `<p class="card-sub">${esc(g.description)}</p>` : ''}
            ${steps}
            ${url ? `<a href="${safeUrl(url)}" target="_blank" rel="noopener" class="card-link">Read guide →</a>` : ''}
          </div>
        </div>
      </div>`;
    }).join('');
    if (window.AOS) AOS.refresh();
  }

  // Expose global load for the guides API route (GET /api/guides)
  api.guides = function(codename) {
    if (!codename) return fetch('/api/guides')
      .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error('API ' + r.status)); })
      .catch(function(e) { return Promise.reject(e); });
    return fetch('/api/guides/' + encodeURIComponent(codename))
      .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error('API ' + r.status)); })
      .catch(function(e) { return Promise.reject(e); });
  };

  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });

  loadGlobal();
})();
