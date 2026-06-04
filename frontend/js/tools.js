(function () {
  'use strict';

  var esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  var input    = document.getElementById('search-input');
  var btn      = document.getElementById('search-btn');
  var grid     = document.getElementById('tool-grid');
  var allTools = [];

  api.tools().then(function (data) {
    allTools = data.tools || data || [];
    render(allTools);
  }).catch(function (e) {
    if (grid) grid.innerHTML = '<div class="column"><div class="error-state">' + esc(e.message) + '</div></div>';
  });

  function render(tools) {
    if (!grid) return;
    if (!tools.length) {
      grid.innerHTML = '<div class="column"><div class="empty-state">No tools found.</div></div>';
      return;
    }
    var cards = tools.map(function (t, i) {
      var ver    = t.latest_version || '';
      var dlUrl  = (t.download_urls && t.download_urls[0]) || t.release_url || t.official_url || '';
      var status = t.status === 'discontinued' ? '<span class="tag is-danger is-light ml-1">discontinued</span>' : '';
      var desc   = t.description ? '<p class="card-sub">' + esc(t.description) + '</p>' : '';
      var verEl  = ver ? '<div class="card-codename">' + esc(ver) + '</div>' : '';
      var link   = dlUrl ? '<a href="' + esc(dlUrl) + '" target="_blank" rel="noopener" class="card-link">Download →</a>' : '';
      return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 50 + '">' +
        '<div class="card"><div class="card-content">' +
        '<div class="card-mfr">' + esc(t.category || '') + '</div>' +
        '<p class="title is-6 mb-1">' + esc(t.name || '') + status + '</p>' +
        desc + verEl + link +
        '</div></div></div>';
    });
    grid.innerHTML = cards.join('');
    if (window.AOS) AOS.refresh();
  }

  function doSearch() {
    var q = input ? input.value.trim().toLowerCase() : '';
    render(q ? allTools.filter(function (t) {
      return (t.name || '').toLowerCase().indexOf(q) !== -1 ||
             (t.description || '').toLowerCase().indexOf(q) !== -1 ||
             (t.category || '').toLowerCase().indexOf(q) !== -1;
    }) : allTools);
  }

  if (btn)   btn.addEventListener('click', doSearch);
  if (input) input.addEventListener('input', doSearch);
})();
