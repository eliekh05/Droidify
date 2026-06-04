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

  var LIMIT    = 20;
  var grid     = document.getElementById('rom-grid');
  var metaEl   = document.getElementById('results-meta');
  var paginEl  = document.getElementById('pagination');
  var input    = document.getElementById('search-input');
  var btn      = document.getElementById('search-btn');
  var currentQ = new URLSearchParams(location.search).get('q') || '';
  if (input) input.value = currentQ;

  function renderPagination(total, offset) {
    var pages = Math.ceil(total / LIMIT);
    var cur   = Math.floor(offset / LIMIT);
    if (pages <= 1 || !paginEl) { if (paginEl) paginEl.innerHTML = ''; return; }
    var h = '<a class="pagination-previous button' + (cur === 0 ? ' is-disabled' : '') + '" onclick="load(' + ((cur - 1) * LIMIT) + ')">Prev</a>';
    h += '<a class="pagination-next button' + (cur >= pages - 1 ? ' is-disabled' : '') + '" onclick="load(' + ((cur + 1) * LIMIT) + ')">Next</a><ul class="pagination-list">';
    for (var i = Math.max(0, cur - 3); i <= Math.min(pages - 1, cur + 3); i++) {
      h += '<li><a class="pagination-link button' + (i === cur ? ' is-current' : '') + '" onclick="load(' + (i * LIMIT) + ')">' + (i + 1) + '</a></li>';
    }
    paginEl.innerHTML = h + '</ul>';
  }

  window.load = function (offset) {
    offset = offset || 0;
    if (grid) grid.innerHTML = Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:90px"></div></div>').join('');
    api.roms({ q: currentQ || undefined, limit: LIMIT, offset: offset })
      .then(function (data) {
        if (metaEl) {
          metaEl.className = 'results-meta';
          metaEl.textContent = data.total.toLocaleString() + ' ROM' + (data.total !== 1 ? 's' : '');
        }
        if (!grid) return;
        if (!data.roms.length) {
          grid.innerHTML = '<div class="column"><div class="empty-state">No ROMs found.</div></div>';
        } else {
          grid.innerHTML = data.roms.map(function (r, i) {
            var android = r.android_base ? '<p style="font-size:.78rem;color:var(--muted)">Android ' + esc(r.android_base) + '</p>' : '';
            var link    = r.download_url ? '<a href="' + safeUrl(r.download_url) + '" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>' : '';
            return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 40 + '">' +
              '<div class="card"><div class="card-content">' +
              '<div class="card-mfr">' + esc(r.source || 'custom') + '</div>' +
              '<p class="title is-6 mb-1">' + esc(r.name) + '</p>' +
              '<div class="card-codename">' + esc(r.codename) + '</div>' +
              android + link + '</div></div></div>';
          }).join('');
        }
        renderPagination(data.total, offset);
        if (window.AOS) AOS.refresh();
        if (offset) window.scrollTo({ top: 0, behavior: 'smooth' });
      })
      .catch(function (e) {
        if (grid) grid.innerHTML = '<div class="column"><div class="error-state">' + esc(e.message) + '</div></div>';
      });
  };

  function doSearch() {
    currentQ = input ? input.value.trim() : '';
    var url  = new URL(location.href);
    if (currentQ) { url.searchParams.set('q', currentQ); } else { url.searchParams.delete('q'); }
    history.pushState({}, '', url);
    window.load(0);
  }

  if (btn)   btn.addEventListener('click', doSearch);
  if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') doSearch(); });
  window.load(0);
})();
