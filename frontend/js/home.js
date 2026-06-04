(function () {
  'use strict';

  var esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  var heroInput = document.getElementById('hero-search');
  var heroBtn   = document.getElementById('hero-search-btn');

  function doSearch() {
    var q = heroInput ? heroInput.value.trim() : '';
    window.location.href = q ? '/devices.html?q=' + encodeURIComponent(q) : '/devices.html';
  }
  if (heroBtn)   heroBtn.addEventListener('click', doSearch);
  if (heroInput) heroInput.addEventListener('keydown', function (e) { if (e.key === 'Enter') doSearch(); });

  function rollNumber(el, target, duration) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = Number(target).toLocaleString(); return;
    }
    var start = performance.now();
    var from  = parseInt(el.textContent.replace(/,/g, '')) || 0;
    function step(now) {
      var p    = Math.min((now - start) / duration, 1);
      var ease = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (target - from) * ease).toLocaleString();
      if (p >= 1) {
        el.classList.add('popped');
        setTimeout(function () { el.classList.remove('popped'); }, 400);
      } else {
        requestAnimationFrame(step);
      }
    }
    requestAnimationFrame(step);
  }

  function updateStat(id, val) {
    var el = document.getElementById(id);
    if (!el || val == null) return;
    rollNumber(el, Number(val), 1200);
  }

  function deviceColHTML(d, delay) {
    var tags = [
      d.has_lineageos  ? '<span class="tag is-success">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag is-info">GrapheneOS</span>'   : '',
      d.has_twrp       ? '<span class="tag is-info">TWRP</span>'         : '',
      d.has_orangefox  ? '<span class="tag is-warning">OrangeFox</span>' : '',
    ].filter(Boolean).join('');
    return '<div class="column is-6-mobile is-4-tablet is-4-desktop" data-aos="fade-up" data-aos-delay="' + delay + '">' +
      '<a href="/device.html?c=' + encodeURIComponent(d.codename) + '" class="card" style="display:block">' +
      '<div class="card-content">' +
      '<div class="card-mfr">' + esc(d.manufacturer || 'Unknown') + '</div>' +
      '<p class="title is-6 mb-1">' + esc(d.model_name || d.codename) + '</p>' +
      '<div class="card-codename">' + esc(d.codename) + '</div>' +
      (tags ? '<div class="tags">' + tags + '</div>' : '') +
      '</div></a></div>';
  }

  var featuredEl = document.getElementById('featured-devices');
  var romFamEl   = document.getElementById('rom-families');
  var pillsEl    = document.getElementById('android-pills');

  api.devices({ limit: 24 }).then(function (d) {
    updateStat('stat-devices', d.total);
    if (!featuredEl) return;
    var shuffled = d.devices.slice().sort(function () { return Math.random() - 0.5; }).slice(0, 6);
    featuredEl.innerHTML = shuffled.map(function (dev, i) { return deviceColHTML(dev, i * 60); }).join('');
    if (window.AOS) AOS.refresh();
  }).catch(function () {
    if (featuredEl) featuredEl.innerHTML = '<p class="empty-state">Could not load devices.</p>';
  });

  api.roms({ limit: 1 }).then(function (d) { updateStat('stat-roms', d.total); }).catch(function () {});
  api.recoveries({ limit: 1 }).then(function (d) { updateStat('stat-recoveries', d.total); }).catch(function () {});
  api.tools().then(function (d) { updateStat('stat-tools', d.total); }).catch(function () {});

  api.androidVersions().then(function (d) {
    updateStat('stat-android', d.total);
    if (!pillsEl) return;
    var recent = d.versions.slice().reverse().slice(0, 8);
    pillsEl.innerHTML = recent.map(function (v) {
      return '<a href="/android.html" class="android-pill" data-aos="zoom-in">' +
        '<span class="v-num">Android ' + esc(v.version_number) + '</span>' +
        '<span class="v-name">' + esc(v.codename || '-') + '</span>' +
        '</a>';
    }).join('');
    if (window.AOS) AOS.refresh();
  }).catch(function () {});

  api.roms({ limit: 20 }).then(function (d) {
    if (!romFamEl) return;
    var counts = {};
    d.roms.forEach(function (r) { counts[r.name] = (counts[r.name] || 0) + 1; });
    var families = Object.keys(counts)
      .map(function (name) { return [name, counts[name]]; })
      .sort(function (a, b) { return b[1] - a[1]; })
      .slice(0, 8);
    romFamEl.innerHTML = families.map(function (pair, i) {
      var name  = pair[0];
      var count = pair[1];
      return '<div class="column is-6-mobile is-3-tablet" data-aos="fade-up" data-aos-delay="' + (i * 50) + '">' +
        '<a href="/device.html?c=' + encodeURIComponent(d.codename) + '" class="card" style="display:block">' +
        '<div class="card-content">' +
        '<p class="title is-6 mb-1">' + esc(name) + '</p>' +
        '<p style="color:var(--muted);font-size:.8rem">' + count + ' build' + (count !== 1 ? 's' : '') + '</p>' +
        '</div></a></div>';
    }).join('');
    if (window.AOS) AOS.refresh();
  }).catch(function () {});
})();
