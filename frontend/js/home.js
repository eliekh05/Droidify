(function () {
  'use strict';

  const esc = function (s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  };

  // Hero search
  const heroInput = document.getElementById('hero-search');
  const heroBtn   = document.getElementById('hero-search-btn');
  function doSearch() {
    const q = heroInput.value.trim();
    window.location.href = q ? `/devices.html?q=${encodeURIComponent(q)}` : '/devices.html';
  }
  heroBtn.addEventListener('click', doSearch);
  heroInput.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });

  // Stat roll animation
  function rollNumber(el, target, duration) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = Number(target).toLocaleString(); return;
    }
    const start = performance.now();
    const from  = parseInt(el.textContent.replace(/,/g,'')) || 0;
    function step(now) {
      const p = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (target - from) * ease).toLocaleString();
      if (p >= 1) { el.classList.add('popped'); setTimeout(() => el.classList.remove('popped'), 400); }
      else requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function updateStat(id, val) {
    const el = document.getElementById(id);
    if (!el || val == null) return;
    rollNumber(el, Number(val), 1200);
  }

  function deviceColHTML(d, delay) {
    const tags = [
      d.has_lineageos  ? '<span class="tag is-success">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag is-info">GrapheneOS</span>'   : '',
      d.has_twrp       ? '<span class="tag is-info">TWRP</span>'         : '',
      d.has_orangefox  ? '<span class="tag is-warning">OrangeFox</span>' : '',
    ].join('');
    return `<div class="column is-6-mobile is-4-tablet is-4-desktop" data-aos="fade-up" data-aos-delay="${delay}">
      <div class="card" style="cursor:pointer" onclick="location.href='/device.html?c=' + encodeURIComponent(d.codename)">
        <div class="card-content">
          <div class="card-mfr">${esc(d.manufacturer||'Unknown')}</div>
          <p class="title is-6 mb-1">${esc(d.model_name||d.codename)}</p>
          <div class="card-codename">${esc(d.codename)}</div>
          ${tags ? `<div class="tags">${tags}</div>` : ''}
        </div>
      </div>
    </div>`;
  }

  const featuredEl = document.getElementById('featured-devices');
  const romFamEl   = document.getElementById('rom-families');
  const pillsEl    = document.getElementById('android-pills');

  api.devices({ limit: 24 }).then(d => {
    updateStat('stat-devices', d.total);
    if (!featuredEl) return;
    const shuffled = [...d.devices].sort(() => Math.random() - .5).slice(0, 6);
    featuredEl.innerHTML = shuffled.map((dev, i) => deviceColHTML(dev, i * 60)).join('');
    if (window.AOS) AOS.refresh();
  }).catch(() => {
    if (featuredEl) featuredEl.innerHTML = '<p class="empty-state">Could not load devices.</p>';
  });

  api.roms({ limit: 1 }).then(d => updateStat('stat-roms', d.total)).catch(() => {});
  api.recoveries({ limit: 1 }).then(d => updateStat('stat-recoveries', d.total)).catch(() => {});
  api.tools().then(d => updateStat('stat-tools', d.total)).catch(() => {});

  api.androidVersions().then(d => {
    updateStat('stat-android', d.total);
    if (!pillsEl) return;
    const recent = [...d.versions].reverse().slice(0, 8);
    pillsEl.innerHTML = recent.map(v =>
      `<a href="/android.html" class="android-pill" data-aos="zoom-in">
        <span class="v-num">Android ${esc(v.version_number)}</span>
        <span class="v-name">${esc(v.codename||'—')}</span>
      </a>`
    ).join('');
    if (window.AOS) AOS.refresh();
  }).catch(() => {});

  api.roms({ limit: 20 }).then(d => {
    if (!romFamEl) return;
    const counts = {};
    for (const r of d.roms) counts[r.name] = (counts[r.name]||0) + 1;
    const families = Object.entries(counts).sort((a,b) => b[1]-a[1]).slice(0, 8);
    romFamEl.innerHTML = families.map(([name, count], i) =>
      `<div class="column is-6-mobile is-3-tablet" data-aos="fade-up" data-aos-delay="${i*50}">
        <div class="card" style="cursor:pointer" onclick="location.href='/roms.html?q=' + encodeURIComponent(name)">
          <div class="card-content">
            <p class="title is-6 mb-1">${esc(name)}</p>
            <p style="color:var(--muted);font-size:.8rem">${count} build${count!==1?'s':''}</p>
          </div>
        </div>
      </div>`
    ).join('');
    if (window.AOS) AOS.refresh();
  }).catch(() => {});
})();
