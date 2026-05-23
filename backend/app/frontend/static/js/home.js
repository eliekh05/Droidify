/* home.js — Homepage logic */

document.getElementById('search-btn').addEventListener('click', () => {
  const q = document.getElementById('global-search').value.trim();
  if (q) window.location.href = `/devices.html?q=${encodeURIComponent(q)}`;
});
document.getElementById('global-search').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('search-btn').click();
});



function _roll(id, val) {
  const el = document.getElementById(id);
  if (!el || (val == null && val !== 0)) return;
  el.classList.remove('skeleton');
  const num = Number(val);
  // Skip animation if already showing the correct number (page reload)
  if (el.textContent === num.toLocaleString()) return;
  // Skip animation if user prefers reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.textContent = num.toLocaleString();
    return;
  }
  window._rollNumber ? window._rollNumber(el, num, 1200) : (el.textContent = num.toLocaleString());
}

async function loadHome() {
  // Fire all requests simultaneously but render each section as it arrives
  // No waiting for all to complete — sections appear progressively

  const devGrid  = document.getElementById('featured-devices');
  const pillsEl  = document.getElementById('android-pills');

  // Show skeletons immediately
  if (devGrid) devGrid.innerHTML = Array(6).fill('<div class="card skeleton" style="height:120px"></div>').join('');

  // Retry helper — keeps trying until data arrives or max attempts reached
  // Handles cold start where backend cache is still warming up
  async function _fetchWithRetry(fn, onSuccess, maxAttempts, delay) {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const data = await fn();
        onSuccess(data);
        return;
      } catch(e) {
        if (i < maxAttempts - 1) await new Promise(r => setTimeout(r, delay));
      }
    }
  }

  // Devices — retry up to 5 times with 2s between attempts
  _fetchWithRetry(
    () => api.devices({ limit: 50 }),
    data => {
      _roll('stat-devices', data.total);
      if (!devGrid) return;
      const shuffled = [...data.devices].sort(() => Math.random() - .5).slice(0, 6);
      devGrid.classList.remove('visible');
      devGrid.innerHTML = shuffled.map(deviceCardHTML).join('');
      void devGrid.offsetHeight;
      devGrid.classList.add('visible');
      if (window._reObserve) window._reObserve();
    },
    5, 2000
  );

  // Stats — each retries independently
  _fetchWithRetry(() => api.roms({ limit: 1 }),       d => _roll('stat-roms', d.total),       5, 2000);
  _fetchWithRetry(() => api.recoveries({ limit: 1 }), d => _roll('stat-recoveries', d.total), 5, 2000);
  _fetchWithRetry(() => api.tools(),                  d => _roll('stat-tools', d.total),       5, 2000);

  // Android versions — retry with pills
  _fetchWithRetry(
    () => api.androidVersions(),
    data => {
      _roll('stat-android', data.total);
      if (!pillsEl) return;
      const recent = [...data.versions].reverse().slice(0, 8);
      pillsEl.innerHTML = recent.map(v =>
        '<a href="/android.html" class="v-pill">' +
          '<span class="v-num">Android ' + escHtml(v.version_number) + '</span>' +
          '<span class="v-name">' + escHtml(v.codename || '—') + '</span>' +
        '</a>'
      ).join('');
    },
    5, 2000
  );

  // ROM families loaded separately — see loadRomFamilies() below
}

loadHome().catch(err => {
  document.getElementById('featured-devices').innerHTML =
    '<div class="error-state">Unable to load data. The service may be starting up — please refresh in a moment.</div>';
});

// Load ROM families independently — never blocks or breaks the main page
async function loadRomFamilies() {
  try {
    const colorMap = { LineageOS:'green', GrapheneOS:'blue', crDroid:'orange', '/e/OS':'gray',
      'PixelExperience':'blue', 'Evolution X':'orange', 'DerpFest':'gray', 'Project Elixir':'green' };
    const romData = await api.roms({ limit: 300 });
    const counts = {};
    for (const r of romData.roms || []) {
      const n = r.name || 'Unknown';
      counts[n] = (counts[n] || 0) + 1;
    }
    const families = Object.entries(counts)
      .sort((a, b) => b[1] - a[1]).slice(0, 8)
      .map(([name, cnt]) => ({ name, cnt, color: colorMap[name] || 'gray' }));
    const famEl = document.getElementById('rom-families');
    if (famEl && families.length) {
      famEl.innerHTML = families.map(f => `
        <div class="rom-family-card">
          <div class="rom-family-name">${escHtml(f.name)}</div>
          <div class="tags">${chip(f.name, f.color)}</div>
          <div class="rom-family-count" style="margin-top:.5rem">${f.cnt} build${f.cnt!==1?'s':''} indexed</div>
        </div>`).join('');
    }
  } catch (e) { /* leave empty — non-critical */ }
}
loadRomFamilies();

// ── PWA Install button ─────────────────────────────────────────────────────
// Android/Desktop: uses beforeinstallprompt (Chrome/Edge)
// iOS Safari:      shows step-by-step modal (no beforeinstallprompt on iOS)
// Already installed (standalone): button hidden

let _deferredPrompt = null;

// Detect platform
// ── iOS install modal ──────────────────────────────────────────────────────
// Steps verified against Apple support page:
// support.apple.com/guide/iphone/bookmark-favorite-webpages-iph42ab2f3a7/ios
const _iosMajor=(()=>{const m=navigator.userAgent.match(/OS (\\d+)_/);return m?parseInt(m[1],10):0;})();
function _showIOSModal() {
  document.getElementById('ios-install-modal')?.remove();

  const isIOS26Plus = _iosMajor >= 26;

  const steps = [
    {
      num: 1,
      title: 'Tap the Share button',
      desc: 'Tap the share icon in the Safari toolbar',
      icon: `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>
               <polyline points="16 6 12 2 8 6"/>
               <line x1="12" y1="2" x2="12" y2="15"/>
             </svg>`
    },
    {
      num: 2,
      title: 'Tap "Add to Home Screen"',
      desc: 'Scroll down the share sheet and tap this option',
      icon: `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <rect x="3" y="3" width="18" height="18" rx="3"/>
               <line x1="12" y1="8" x2="12" y2="16"/>
               <line x1="8" y1="12" x2="16" y2="12"/>
             </svg>`
    },
    {
      num: 3,
      title: 'Tap "Add"',
      desc: isIOS26Plus
        ? '"Open as Web App" is on by default since the manifest is present — just tap Add'
        : 'The icon and name are set from the manifest — tap Add to confirm',
      icon: `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <polyline points="20 6 9 17 4 12"/>
             </svg>`
    }
  ];

  const stepsHTML = steps.map((s, i) => `
    ${i > 0 ? '<div class="ios-modal-divider"></div>' : ''}
    <div class="ios-modal-step">
      <div class="ios-step-num">${s.num}</div>
      <div class="ios-step-content">
        <div class="ios-step-title">${s.title}</div>
        <div class="ios-step-desc">${s.desc}</div>
      </div>
      <div class="ios-step-icon">${s.icon}</div>
    </div>
  `).join('');

  const modal = document.createElement('div');
  modal.id = 'ios-install-modal';
  modal.innerHTML = `
    <div class="ios-modal-backdrop" id="ios-modal-backdrop"></div>
    <div class="ios-modal-sheet" role="dialog" aria-modal="true" aria-label="Install Droidify">
      <div class="ios-modal-handle"></div>
      <div class="ios-modal-header">
        <img src="/icons/icon-192.png" class="ios-modal-icon" alt="Droidify icon" />
        <div>
          <div class="ios-modal-title">Install Droidify</div>
          <div class="ios-modal-sub">Add to your Home Screen for quick access</div>
        </div>
        <button class="ios-modal-close" id="ios-modal-close" aria-label="Close">✕</button>
      </div>
      <div class="ios-modal-steps">${stepsHTML}</div>
      <div class="ios-modal-arrow">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--accent)">
          <path d="M12 16l-6-6h12z"/>
        </svg>
        <span>Share button is in the Safari toolbar</span>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  requestAnimationFrame(() => {
    modal.querySelector('.ios-modal-sheet').classList.add('ios-modal-open');
  });

  const close = () => {
    modal.querySelector('.ios-modal-sheet').classList.remove('ios-modal-open');
    setTimeout(() => modal.remove(), 300);
  };
  document.getElementById('ios-modal-backdrop').addEventListener('click', close);
  document.getElementById('ios-modal-close').addEventListener('click', close);
}

// ── Scroll reveal + count-up ──────────────────────────────────────────────
// Uses IntersectionObserver — Chrome/web.dev recommended pattern
// Registered in rAF so elements have layout before first check

function _animateCount(el, target) {
  const duration = 1400;
  const start = performance.now();
  const tick = (now) => {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3); // ease out cubic
    el.textContent = Math.round(eased * target).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
    else el.textContent = target.toLocaleString();
  };
  requestAnimationFrame(tick);
}