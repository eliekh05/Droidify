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

  var main     = document.getElementById('device-main');
  var codename = new URLSearchParams(location.search).get('c');

  if (!codename) {
    if (main) main.innerHTML = '<div class="page-header"><h1 class="title">No device specified</h1></div><a href="/devices.html" class="button is-primary">&larr; Back to devices</a>';
    return;
  }
  document.title = esc(codename) + ' - Droidify';

  function tagClass(s) {
    if (s === 'lineageos' || s === 'grapheneos') return 'is-success';
    if (s === 'twrp' || s === 'orangefox') return 'is-info';
    return 'is-dark';
  }

  function render(device) {
    var sources = (device.sources || []).map(function (s) {
      return '<span class="tag ' + tagClass(s) + '">' + esc(s) + '</span>';
    }).join('');

    var roms = '';
    if (device.roms && device.roms.length) {
      roms = device.roms.map(function (rom, i) {
        var dl = rom.download_url || (rom.download_urls && rom.download_urls[0]) || '';
        var android = rom.android_base ? '<div class="card-codename">Android ' + esc(rom.android_base) + '</div>' : '';
        var label   = rom.version_label ? '<p style="font-size:.78rem;color:var(--muted)">' + esc(rom.version_label) + '</p>' : '';
        var link    = dl ? '<a href="' + safeUrl(dl) + '" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download &rarr;</a>' : '';
        return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 40 + '">' +
          '<div class="card"><div class="card-content">' +
          '<div class="card-mfr">' + esc(rom.source || 'custom') + '</div>' +
          '<p class="title is-6 mb-1">' + esc(rom.name) + '</p>' +
          android + label + link + '</div></div></div>';
      }).join('');
    } else {
      roms = '<div class="column"><div class="empty-state">No ROMs found for this device.</div></div>';
    }

    var recoveries = '';
    if (device.recoveries && device.recoveries.length) {
      recoveries = device.recoveries.map(function (r, i) {
        var link = r.download_url ? '<a href="' + safeUrl(r.download_url) + '" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download &rarr;</a>' : '';
        return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + Math.min(i, 6) * 40 + '">' +
          '<div class="card"><div class="card-content">' +
          '<div class="card-mfr">' + esc(r.recovery_type || 'recovery') + '</div>' +
          '<p class="title is-6 mb-1">' + esc(r.model_name || r.codename) + '</p>' +
          link + '</div></div></div>';
      }).join('');
    }

    var samfw = '';
    if (device.stock_firmware && device.stock_firmware.length) {
      samfw = device.stock_firmware.map(function (f, i) {
        return '<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="' + (i * 40) + '">' +
          '<div class="card"><div class="card-content">' +
          '<div class="card-mfr">Stock Firmware</div>' +
          '<p class="title is-6 mb-1">' + esc(f.model) + '</p>' +
          '<p style="font-size:.82rem;color:var(--muted);margin:.3rem 0">' + esc(f.description) + '</p>' +
          '<a href="' + safeUrl(f.download_url) + '" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download on SamFW &rarr;</a>' +
          '</div></div></div>';
      }).join('');
    }

    var links = [
      device.wiki_url      ? '<a href="' + safeUrl(device.wiki_url)      + '" target="_blank" rel="noopener" class="button is-primary mr-2 mb-2">LineageOS Wiki</a>' : '',
      device.twrp_url      ? '<a href="' + safeUrl(device.twrp_url)      + '" target="_blank" rel="noopener" class="button is-ghost mr-2 mb-2">TWRP</a>' : '',
      device.orangefox_url ? '<a href="' + safeUrl(device.orangefox_url) + '" target="_blank" rel="noopener" class="button is-ghost mr-2 mb-2">OrangeFox</a>' : '',
    ].join('');

    var romCount     = device.roms ? device.roms.length : 0;
    var recoveryCount = device.recoveries ? device.recoveries.length : 0;

    if (!main) return;
    main.innerHTML =
      '<div class="page-header" data-aos="fade-up">' +
        '<div class="mb-3"><a href="/devices.html" class="button is-ghost">&larr; Back</a></div>' +
        '<p style="font-size:.78rem;color:var(--muted);margin-bottom:.3rem">' + esc(device.manufacturer || '') + '</p>' +
        '<h1 class="title">' + esc(device.model_name || device.codename) + '</h1>' +
        '<p style="font-family:var(--mono);color:var(--accent);font-size:.9rem">' + esc(device.codename) + '</p>' +
        (sources ? '<div class="tags mt-3">' + sources + '</div>' : '') +
      '</div>' +
      '<section class="section pb-0">' +
        '<div class="section-header" data-aos="fade-up">' +
          '<h2 class="title is-6">ROMs' + (romCount ? ' (' + romCount + ')' : '') + '</h2>' +
        '</div>' +
        '<div class="columns is-multiline is-mobile">' + roms + '</div>' +
      '</section>' +
      (recoveries ? '<section class="section pb-0">' +
        '<div class="section-header" data-aos="fade-up">' +
          '<h2 class="title is-6">Recoveries (' + recoveryCount + ')</h2>' +
        '</div>' +
        '<div class="columns is-multiline is-mobile">' + recoveries + '</div>' +
      '</section>' : '') +
      (samfw ? '<section class="section pb-0">' +
        '<div class="section-header" data-aos="fade-up">' +
          '<h2 class="title is-6">Stock Firmware</h2>' +
        '</div>' +
        '<div class="columns is-multiline is-mobile">' + samfw + '</div>' +
      '</section>' : '') +
      (links ? '<section class="section" data-aos="fade-up">' +
        '<div class="section-header"><h2 class="title is-6">Links</h2></div>' +
        '<div>' + links + '</div>' +
      '</section>' : '');

    document.title = esc(device.model_name || device.codename) + ' - Droidify';
    if (window.AOS) AOS.refresh();
  }

  function fetchDevice(codename, timeoutMs) {
    timeoutMs = timeoutMs || 20000;
    var ctrl  = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, timeoutMs);
    return fetch('/api/devices/' + encodeURIComponent(codename), { signal: ctrl.signal })
      .then(function (r) {
        clearTimeout(timer);
        if (!r.ok) throw new Error('API ' + r.status + ': /devices/' + codename);
        return r.json();
      })
      .catch(function (e) {
        clearTimeout(timer);
        if (e.name === 'AbortError') throw new Error('Request timed out: /devices/' + codename);
        throw e;
      });
  }

  function load(retry) {
    if (!retry && main) {
      main.innerHTML = '<div style="padding:3rem 0;text-align:center">' +
        '<div class="spinner"></div>' +
        '<p style="color:var(--muted)">Loading device data...</p>' +
      '</div>';
    }
    fetchDevice(codename, 20000).then(function (device) {
      render(device);
      if (!retry && (!device.roms || !device.roms.length)) {
        setTimeout(function () { load(true); }, 3000);
      }
    }).catch(function (e) {
      var msg = e.message.indexOf('timed out') !== -1
        ? 'Loading timed out - the server is still warming up. Please try again.'
        : e.message.indexOf('404') !== -1 ? 'Device "' + esc(codename) + '" not found.' : e.message;
      if (main) main.innerHTML =
        '<div class="page-header">' +
          '<h1 class="title">Could not load device</h1>' +
          '<p class="subtitle" style="color:var(--danger)">' + esc(msg) + '</p>' +
        '</div>' +
        '<button class="button is-primary mr-2" onclick="location.reload()">&cularr; Retry</button>' +
        '<a href="/devices.html" class="button is-ghost">&larr; Back to devices</a>';
    });
  }

  load(false);
})();
