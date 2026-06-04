(function () {
  'use strict';

  var esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  var LIMIT    = 24;
  var grid     = document.getElementById('device-grid');
  var metaEl   = document.getElementById('results-meta');
  var paginEl  = document.getElementById('pagination');
  var input    = document.getElementById('search-input');
  var btn      = document.getElementById('search-btn');
  var params   = new URLSearchParams(location.search);
  var currentQ = params.get('q') || '';
  if (input) input.value = currentQ;

  function cardHTML(d, i) {
    var tags = [
      d.has_lineageos  ? '<span class="tag is-success">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag is-info">GrapheneOS</span>'   : '',
      d.has_twrp       ? '<span class="tag is-info">TWRP</span>'         : '',
      d.has_orangefox  ? '<span class="tag is-warning">OrangeFox</span>' : '',
    ].filter(Boolean).join('');
    return '<div class="column is-6-mobile is-4-tablet is-4-desktop" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 60 + '">' +
      '<a href="/device.html?c=' + encodeURIComponent(d.codename) + '" class="card" style="display:block">' +
      '<div class="card-content">' +
      '<div class="card-mfr">' + esc(d.manufacturer || 'Unknown') + '</div>' +
      '<p class="title is-6 mb-1">' + esc(d.model_name || d.codename) + '</p>' +
      '<div class="card-codename">' + esc(d.codename) + '</div>' +
      (tags ? '<div class="tags">' + tags + '</div>' : '') +
      '</div></a></div>';
  }

  function renderPagination(total, offset) {
    var pages = Math.ceil(total / LIMIT);
    var cur   = Math.floor(offset / LIMIT);
    if (pages <= 1 || !paginEl) { if (paginEl) paginEl.innerHTML = ''; return; }
    var h = '<a class="pagination-previous button' + (cur === 0 ? ' is-disabled' : '') + '" onclick="loadDevices(' + ((cur - 1) * LIMIT) + ')">Prev</a>';
    h += '<a class="pagination-next button' + (cur >= pages - 1 ? ' is-disabled' : '') + '" onclick="loadDevices(' + ((cur + 1) * LIMIT) + ')">Next</a><ul class="pagination-list">';
    for (var i = Math.max(0, cur - 3); i <= Math.min(pages - 1, cur + 3); i++) {
      h += '<li><a class="pagination-link button' + (i === cur ? ' is-current' : '') + '" onclick="loadDevices(' + (i * LIMIT) + ')">' + (i + 1) + '</a></li>';
    }
    paginEl.innerHTML = h + '</ul>';
  }

  window.loadDevices = function (offset) {
    offset = offset || 0;
    if (grid) grid.innerHTML = Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:110px"></div></div>').join('');
    if (metaEl) metaEl.textContent = '';
    api.devices({ q: currentQ || undefined, limit: LIMIT, offset: offset })
      .then(function (data) {
        if (!grid) return;
        if (!data.devices.length) {
          grid.innerHTML = '<div class="column"><div class="empty-state">No devices found.</div></div>';
          return;
        }
        if (metaEl) {
          metaEl.className = 'results-meta';
          metaEl.textContent = data.total.toLocaleString() + ' device' + (data.total !== 1 ? 's' : '') + (currentQ ? ' for "' + currentQ + '"' : '');
        }
        grid.innerHTML = data.devices.map(cardHTML).join('');
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
    window.loadDevices(0);
  }

  if (btn)   btn.addEventListener('click', doSearch);
  if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') doSearch(); });
  window.loadDevices(0);
})();
