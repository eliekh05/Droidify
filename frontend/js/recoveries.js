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
  var grid     = document.getElementById('recovery-grid');
  var metaEl   = document.getElementById('results-meta');
  var paginEl  = document.getElementById('pagination');
  var input    = document.getElementById('search-input');
  var btn      = document.getElementById('search-btn');
  var currentQ = '';

  window.load = function (offset) {
    offset = offset || 0;
    if (grid) grid.innerHTML = Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:90px"></div></div>').join('');
    api.recoveries({ q: currentQ || undefined, limit: LIMIT, offset: offset })
      .then(function (data) {
        if (metaEl) {
          metaEl.className = 'results-meta';
          metaEl.textContent = data.total.toLocaleString() + ' recovery build' + (data.total !== 1 ? 's' : '');
        }
        if (!grid) return;
        if (!data.recoveries.length) {
          grid.innerHTML = '<div class="column"><div class="empty-state">No recoveries found.</div></div>';
        } else {
          grid.innerHTML = data.recoveries.map(function (r, i) {
            var link = r.download_url ? '<a href="' + safeUrl(r.download_url) + '" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>' : '';
            return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 40 + '">' +
              '<div class="card"><div class="card-content">' +
              '<div class="card-mfr">' + esc(r.recovery_type || 'recovery') + '</div>' +
              '<p class="title is-6 mb-1">' + esc(r.model_name || r.codename) + '</p>' +
              '<div class="card-codename">' + esc(r.codename) + '</div>' +
              link + '</div></div></div>';
          }).join('');
        }
        var pages = Math.ceil(data.total / LIMIT);
        var cur   = Math.floor(offset / LIMIT);
        if (pages > 1 && paginEl) {
          var h = '<a class="pagination-previous button' + (cur === 0 ? ' is-disabled' : '') + '" onclick="load(' + ((cur - 1) * LIMIT) + ')">Prev</a>';
          h += '<a class="pagination-next button' + (cur >= pages - 1 ? ' is-disabled' : '') + '" onclick="load(' + ((cur + 1) * LIMIT) + ')">Next</a><ul class="pagination-list">';
          for (var i = Math.max(0, cur - 3); i <= Math.min(pages - 1, cur + 3); i++) {
            h += '<li><a class="pagination-link button' + (i === cur ? ' is-current' : '') + '" onclick="load(' + (i * LIMIT) + ')">' + (i + 1) + '</a></li>';
          }
          paginEl.innerHTML = h + '</ul>';
        }
        if (window.AOS) AOS.refresh();
        if (offset) window.scrollTo({ top: 0, behavior: 'smooth' });
      })
      .catch(function (e) {
        if (grid) grid.innerHTML = '<div class="column"><div class="error-state">' + esc(e.message) + '</div></div>';
      });
  };

  function doSearch() {
    currentQ = input ? input.value.trim() : '';
    window.load(0);
  }

  if (btn)   btn.addEventListener('click', doSearch);
  if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') doSearch(); });
  window.load(0);
})();
