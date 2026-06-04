(function () {
  'use strict';

  var esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  var safeUrl = function (u) {
    if (!u) return '#';
    var s = String(u).trim();
    return /^https?:\/\//i.test(s) ? s : '#';
  };

  var input = document.getElementById('search-input');
  var btn   = document.getElementById('search-btn');
  var grid  = document.getElementById('guide-grid');

  function loadGlobal() {
    return api.guides('').then(function (data) {
      var items = data.guides || [];
      if (items.length) renderGuides(items, true);
    }).catch(function () {});
  }

  function doSearch() {
    var q = input ? input.value.trim() : '';
    if (!q) { loadGlobal(); return; }
    if (grid) grid.innerHTML = '<div class="column"><div style="padding:2rem;text-align:center"><div class="spinner"></div></div></div>';
    api.guides(q).then(function (data) {
      var guides = data.guides || [];
      if (!guides.length) {
        if (grid) grid.innerHTML = '<div class="column"><div class="empty-state">No guides found for <strong>' + esc(q) + '</strong>.</div></div>';
        return;
      }
      renderGuides(guides, false);
    }).catch(function (e) {
      if (grid) grid.innerHTML = '<div class="column"><div class="empty-state">' + esc(e.message) + '</div></div>';
    });
  }

  function renderGuides(guides, isGlobal) {
    var header = isGlobal ? '<div class="column is-12"><p class="section-label">Universal guides</p></div>' : '';
    var cards = guides.map(function (g, i) {
      var url   = g.source_url || g.url || '';
      var type  = g.guide_type || g.category || 'guide';
      var steps = '';
      if (Array.isArray(g.steps) && g.steps.length) {
        var lis = g.steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('');
        var notes = g.notes ? '<p class="guide-notes">' + esc(g.notes) + '</p>' : '';
        steps = '<details class="guide-steps mt-2"><summary class="card-link">Steps (' + g.steps.length + ')</summary><ol class="guide-ol">' + lis + '</ol>' + notes + '</details>';
      }
      var link = url ? '<a href="' + safeUrl(url) + '" target="_blank" rel="noopener" class="card-link">Read guide →</a>' : '';
      var desc = g.description ? '<p class="card-sub">' + esc(g.description) + '</p>' : '';
      return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 50 + '">' +
        '<div class="card"><div class="card-content">' +
        '<div class="card-mfr">' + esc(type) + '</div>' +
        '<p class="title is-6 mb-1">' + esc(g.title || 'Guide') + '</p>' +
        desc + steps + link +
        '</div></div></div>';
    });
    if (grid) grid.innerHTML = header + cards.join('');
    if (window.AOS) AOS.refresh();
  }

  if (btn)   btn.addEventListener('click', doSearch);
  if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') doSearch(); });

  loadGlobal();
})();
