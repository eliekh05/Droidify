/* home.js — Homepage logic */

document.getElementById('search-btn').addEventListener('click', () => {
  const q = document.getElementById('global-search').value.trim();
  if (q) window.location.href = `/devices.html?q=${encodeURIComponent(q)}`;
});
document.getElementById('global-search').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('search-btn').click();
});

async function loadHome() {
  const [devices, roms, recoveries, tools, versions] = await Promise.allSettled([
    api.devices({ limit: 6 }),
    api.roms({ limit: 1 }),
    api.recoveries({ limit: 1 }),
    api.tools(),
    api.androidVersions(),
  ]);

  if (devices.status === 'fulfilled') {
    const dEl = document.getElementById('stat-devices');
    dEl.classList.remove('skeleton');
    dEl.querySelector('.stat-value').textContent = devices.value.total.toLocaleString();
  }
  if (roms.status === 'fulfilled') {
    const rEl = document.getElementById('stat-roms');
    rEl.classList.remove('skeleton');
    rEl.querySelector('.stat-value').textContent = roms.value.total.toLocaleString();
  }
  if (recoveries.status === 'fulfilled') {
    const rcEl = document.getElementById('stat-recoveries');
    rcEl.classList.remove('skeleton');
    rcEl.querySelector('.stat-value').textContent = recoveries.value.total.toLocaleString();
  }
  if (tools.status === 'fulfilled') {
    const tEl = document.getElementById('stat-tools');
    tEl.classList.remove('skeleton');
    tEl.querySelector('.stat-value').textContent = tools.value.total;
  }
  if (versions.status === 'fulfilled') {
    const vEl = document.getElementById('stat-android');
    vEl.classList.remove('skeleton');
    vEl.querySelector('.stat-value').textContent = versions.value.total;
  }

  const devGrid = document.getElementById('featured-devices');
  if (devices.status === 'fulfilled') {
    devGrid.innerHTML = devices.value.devices.map(deviceCardHTML).join('');
  } else {
    devGrid.innerHTML = '<div class="error-state">Could not load devices — backend may be starting up.</div>';
  }

  const pillsEl = document.getElementById('android-pills');
  if (versions.status === 'fulfilled') {
    const recent = [...versions.value.versions].reverse().slice(0, 8);
    pillsEl.innerHTML = recent.map(v => `
      <a href="/android.html" class="v-pill">
        <span class="v-num">Android ${escHtml(v.version_number)}</span>
        <span class="v-name">${escHtml(v.codename || '—')}</span>
      </a>`).join('');
  }

  const romFamilies = [
    { name: 'LineageOS',  desc: 'AOSP-based, 281 devices',    color: 'green'  },
    { name: 'GrapheneOS', desc: 'Privacy-focused, 14 Pixels', color: 'blue'   },
    { name: 'crDroid',    desc: 'Feature-rich AOSP fork',     color: 'orange' },
    { name: '/e/OS',      desc: 'De-Googled with microG',     color: 'gray'   },
  ];
  const famEl = document.getElementById('rom-families');
  famEl.innerHTML = romFamilies.map(f => `
    <div class="rom-family-card">
      <div class="rom-family-name">${escHtml(f.name)}</div>
      <div class="tags">${chip(f.name, f.color)}</div>
      <div class="rom-family-count" style="margin-top:.5rem">${escHtml(f.desc)}</div>
    </div>`).join('');
}

loadHome().catch(err => {
  console.error('Home load error:', err);
  document.getElementById('featured-devices').innerHTML =
    '<div class="error-state">API not reachable. Make sure the backend is running on port 8000.</div>';
});

// ── PWA Install button ─────────────────────────────────────────────────────
// Android/Desktop: uses beforeinstallprompt (Chrome/Edge)
// iOS Safari:      shows step-by-step modal (no beforeinstallprompt on iOS)
// Already installed (standalone): button hidden

let _deferredPrompt = null;

// Detect platform
// ── iOS install modal ──────────────────────────────────────────────────────
// Steps verified against Apple support page:
// support.apple.com/guide/iphone/bookmark-favorite-webpages-iph42ab2f3a7/ios
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

// Register observers after first paint so elements have dimensions
requestAnimationFrame(() => {
  // Scroll reveal observer
  // Note: negative rootMargin is buggy on iOS Safari — use threshold only
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.05 });

  document.querySelectorAll('.reveal, .reveal-grid').forEach(el => {
    revealObs.observe(el);
  });

  // Count-up observer — re-checks every 300ms until cards are loaded
  const countObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const valueEl = e.target.querySelector('.stat-value');
      if (!valueEl) return;
      const num = parseInt(valueEl.textContent.replace(/,/g, ''), 10);
      if (!isNaN(num) && num > 0) _animateCount(valueEl, num);
      countObs.unobserve(e.target);
    });
  }, { threshold: 0.3 });

  // Poll until skeletons are replaced with real data, then observe
  let attempts = 0;
  const watchCards = setInterval(() => {
    const cards = document.querySelectorAll('.stat-item:not(.skeleton)');
    if (cards.length > 0 || attempts++ > 30) {
      cards.forEach(c => countObs.observe(c));
      clearInterval(watchCards);
    }
  }, 300);
});
