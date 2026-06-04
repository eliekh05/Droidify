(function () {
  'use strict';

  var grid     = document.getElementById('watchlist-grid');
  var subtitle = document.getElementById('watchlist-subtitle');

  var esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  function renderEmpty(msg) {
    if (!grid) return;
    grid.innerHTML = '<div class="empty-state" style="text-align:center;padding:3rem 1rem;color:var(--muted)">' +
      '<div style="font-size:3rem;margin-bottom:1rem">&#128203;</div>' +
      '<p style="font-size:1rem">' + msg + '</p></div>';
  }

  function renderCard(device) {
    var tags = '';
    if (device.has_lineageos) tags += '<span class="tag is-small" style="background:var(--accent-dim);color:var(--accent)">LineageOS</span> ';
    if (device.has_twrp)      tags += '<span class="tag is-small" style="background:var(--accent-dim);color:var(--accent)">TWRP</span> ';
    if (device.has_orangefox) tags += '<span class="tag is-small" style="background:var(--accent-dim);color:var(--accent)">OrangeFox</span> ';
    return '<div class="card device-card" style="position:relative"><div class="card-content">' +
      '<div style="display:flex;justify-content:space-between;align-items:flex-start">' +
      '<div>' +
      '<p class="card-codename">' + esc(device.codename) + '</p>' +
      (device.model ? '<p class="card-model">' + esc(device.model) + '</p>' : '') +
      (device.manufacturer ? '<p style="font-size:.78rem;color:var(--muted)">' + esc(device.manufacturer) + '</p>' : '') +
      '</div>' +
      '<button class="watchlist-remove" data-codename="' + esc(device.codename) + '" ' +
      'title="Remove from watchlist" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:1.1rem;padding:.25rem">x</button>' +
      '</div>' +
      (tags ? '<div style="margin-top:.6rem;display:flex;flex-wrap:wrap;gap:.3rem">' + tags + '</div>' : '') +
      '<div style="margin-top:.75rem">' +
      '<a href="/device.html?c=' + encodeURIComponent(device.codename) + '" class="button is-small is-ghost" style="padding:0;color:var(--accent)">View device &rarr;</a>' +
      '</div></div></div>';
  }

  function attachRemoveButtons() {
    if (!grid) return;
    grid.querySelectorAll('.watchlist-remove').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var codename = btn.dataset.codename;
        btn.disabled = true;
        btn.textContent = '...';
        fetch('/api/watchlist/' + encodeURIComponent(codename), { method: 'DELETE' })
          .then(function () { return load(); })
          .catch(function () { btn.disabled = false; btn.textContent = 'x'; });
      });
    });
  }

  function load() {
    return fetch('/api/auth/me')
      .then(function (r) { return r.json(); })
      .then(function (me) {
        if (!me.user) {
          if (subtitle) subtitle.textContent = 'Sign in with GitHub to save devices to your watchlist.';
          renderEmpty('Your watchlist is empty. Sign in to start saving devices.');
          return;
        }
        return fetch('/api/watchlist')
          .then(function (r2) { return r2.json(); })
          .then(function (data) {
            if (!data.watchlist || !data.watchlist.length) {
              if (subtitle) subtitle.textContent = 'No saved devices yet.';
              renderEmpty('Browse devices and click the bookmark icon to save them here.');
              return;
            }
            if (subtitle) subtitle.textContent = data.total + ' saved device' + (data.total !== 1 ? 's' : '');
            if (grid) grid.innerHTML = data.watchlist.map(renderCard).join('');
            attachRemoveButtons();
          });
      })
      .catch(function () {
        renderEmpty('Could not load watchlist. Please try again.');
      });
  }

  load();
})();
