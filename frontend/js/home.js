(function () {
  'use strict';

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
    const start = performance.now();
    const from  = parseInt(el.textContent.replace(/,/g, '')) || 0;
    function step(now) {
      const p = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3); // ease-out-cubic
      el.textContent = Math.round(from + (target - from) * ease).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function updateStat(id, val) {
    const el = document.getElementById(id);
    if (!el || val == null) return;
    rollNumber(el, Number(val), 1200);
    el.closest('.stat-item')?.classList.remove('skeleton');
  }

  // Device card HTML
  function deviceCardHTML(d) {
    const tags = [
      d.has_lineageos  ? '<span class="tag tag-green">LineageOS</span>' : '',
      d.has_grapheneos ? '<span class="tag tag-blue">GrapheneOS</span>' : '',
      d.has_twrp       ? '<span class="tag tag-blue">TWRP</span>'       : '',
      d.has_orangefox  ? '<span class="tag tag-orange">OrangeFox</span>': '',
    ].join('');
    const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    return `<div class="card reveal" style="cursor:pointer" onclick="location.href='/device.html?c=${esc(d.codename)}'">
      <div class="card-mfr">${esc(d.manufacturer || 'Unknown')}</div>
      <div class="card-title">${esc(d.model_name || d.codename)}</div>
      <div class="card-codename">${esc(d.codename)}</div>
      ${tags ? `<div class="tags">${tags}</div>` : ''}
    </div>`;
  }

  // Load all sections independently
  const featuredEl  = document.getElementById('featured-devices');
  const romFamEl    = document.getElementById('rom-families');
  const pillsEl     = document.getElementById('android-pills');

  // Stats
  api.devices({ limit: 24 }).then(d => {
    updateStat('stat-devices', d.total);
    if (!featuredEl) return;
    const shuffled = [...d.devices].sort(() => Math.random() - .5).slice(0, 6);
    featuredEl.innerHTML = shuffled.map(deviceCardHTML).join('');
    if (window._reObserve) window._reObserve();
  }).catch(() => {
    if (featuredEl) featuredEl.innerHTML = '<p class="empty-state">Could not load devices. Please refresh.</p>';
  });

  api.roms({ limit: 1 }).then(d => updateStat('stat-roms', d.total)).catch(() => {});
  api.recoveries({ limit: 1 }).then(d => updateStat('stat-recoveries', d.total)).catch(() => {});
  api.tools().then(d => updateStat('stat-tools', d.total)).catch(() => {});

  api.androidVersions().then(d => {
    updateStat('stat-android', d.total);
    if (!pillsEl) return;
    const recent = [...d.versions].reverse().slice(0, 8);
    pillsEl.innerHTML = recent.map(v =>
      `<a href="/android.html" class="v-pill">
        <span class="v-num">Android ${v.version_number}</span>
        <span class="v-name">${v.codename || '—'}</span>
      </a>`
    ).join('');
  }).catch(() => {});

  api.roms({ limit: 20 }).then(d => {
    if (!romFamEl) return;
    const counts = {};
    for (const r of d.roms) counts[r.name] = (counts[r.name] || 0) + 1;
    const families = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 8);
    const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    romFamEl.innerHTML = families.map(([name, count]) =>
      `<div class="card reveal" style="cursor:pointer" onclick="location.href='/roms.html?q=${encodeURIComponent(name)}'">
        <div class="card-title">${esc(name)}</div>
        <div style="color:var(--muted);font-size:.8rem;margin-top:.25rem">${count} build${count !== 1 ? 's' : ''}</div>
      </div>`
    ).join('');
    if (window._reObserve) window._reObserve();
  }).catch(() => {});

})();
