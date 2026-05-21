/**
 * Droidify API client — pure JS, no framework.
 * Communicates with the FastAPI backend.
 */

const API_BASE = '';  // Relative — FastAPI serves both frontend and /api/* on same port

const api = {
  async get(path, params = {}) {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ''))
    ).toString();
    const url = `${API_BASE}/api${path}${qs ? '?' + qs : ''}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`API ${res.status}: ${url}`);
    return res.json();
  },

  devices(params = {})        { return this.get('/devices', params); },
  device(codename)            { return this.get(`/devices/${encodeURIComponent(codename)}`); },
  roms(params = {})           { return this.get('/roms', params); },
  tools(params = {})          { return this.get('/tools', params); },
  recoveries(params = {})     { return this.get('/recoveries', params); },
  androidVersions(params = {}){ return this.get('/android-versions', params); },
};

/* ── DOM helpers ───────────────────────────────────────────────────────────── */

function el(tag, className, inner) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (inner !== undefined) e.innerHTML = inner;
  return e;
}

function setText(id, text) {
  const e = document.getElementById(id);
  if (e) e.textContent = text;
}

function setHTML(id, html) {
  const e = document.getElementById(id);
  if (e) e.innerHTML = html;
}

function show(id)  { const e = document.getElementById(id); if (e) e.style.display = ''; }
function hide(id)  { const e = document.getElementById(id); if (e) e.style.display = 'none'; }

function chip(label, cls = 'gray') {
  return `<span class="chip chip-${cls}">${escHtml(label)}</span>`;
}

function escHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function debounce(fn, delay = 300) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}

/* ── Device card ───────────────────────────────────────────────────────────── */
function deviceCardHTML(d) {
  const sources = (d.sources || []).map(s => `<span class="source-tag">${escHtml(s)}</span>`).join(' ');
  const romCount = d.rom_count != null ? chip(`${d.rom_count} ROMs`, d.rom_count >= 5 ? 'green' : d.rom_count >= 3 ? 'blue' : 'gray') : '';
  const hasLos  = d.has_lineageos ? chip('LineageOS', 'green') : '';
  const hasTwrp = d.has_twrp     ? chip('TWRP', 'blue') : '';
  const hasFox  = d.has_orangefox? chip('OrangeFox', 'orange') : '';

  return `
    <div class="card">
      <a class="card-link" href="/device.html?c=${encodeURIComponent(d.codename)}">
        <div class="card-mfr">${escHtml(d.manufacturer || '')}</div>
        <div class="card-title">${escHtml(d.model_name || d.codename)}</div>
        <div class="card-codename">${escHtml(d.codename)}</div>
        <div class="tags" style="margin-top:.5rem">
          ${romCount}${hasLos}${hasTwrp}${hasFox}
        </div>
        <div class="card-sub" style="margin-top:.4rem">${sources}</div>
      </a>
    </div>`;
}

/* ── Pagination ────────────────────────────────────────────────────────────── */
function renderPagination(containerId, total, offset, limit, onPage) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const totalPages = Math.ceil(total / limit);
  const current    = Math.floor(offset / limit);
  if (totalPages <= 1) { container.innerHTML = ''; return; }

  let html = '';
  if (current > 0)
    html += `<button class="page-btn" data-page="${current - 1}">← Prev</button>`;

  const start = Math.max(0, current - 2);
  const end   = Math.min(totalPages - 1, current + 2);
  for (let i = start; i <= end; i++) {
    html += `<button class="page-btn ${i === current ? 'active' : ''}" data-page="${i}">${i + 1}</button>`;
  }

  if (current < totalPages - 1)
    html += `<button class="page-btn" data-page="${current + 1}">Next →</button>`;

  container.innerHTML = html;
  container.querySelectorAll('.page-btn').forEach(btn => {
    btn.addEventListener('click', () => onPage(parseInt(btn.dataset.page) * limit));
  });
}


// ── Global scroll reveal ───────────────────────────────────────────────────
requestAnimationFrame(() => {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    });
  }, { threshold: 0 }); // threshold 0 = fires as soon as 1px is visible — Safari safe
  document.querySelectorAll('.reveal, .reveal-grid').forEach(el => obs.observe(el));
  // Re-observe after dynamic content loads
  window._reObserve = () => document.querySelectorAll('.reveal:not(.visible), .reveal-grid:not(.visible)').forEach(el => obs.observe(el));
});

// ── PWA Install button — runs on every page ───────────────────────────────
(function initPWAInstall() {
  const _isIOS     = /iphone|ipad|ipod/i.test(navigator.userAgent)
                  || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const _isSafari  = /^((?!chrome|crios|android).)*safari/i.test(navigator.userAgent);
  const _isMacOS   = /macintosh/i.test(navigator.userAgent) && !_isIOS;
  const _isMacSaf  = _isMacOS && _isSafari;
  const _isStand   = window.matchMedia('(display-mode: standalone)').matches
                  || navigator.standalone === true;
  let _deferredPrompt = null;

  function _showInstall() {
    document.querySelectorAll('#pwa-install-wrap').forEach(el => el.style.display = 'block');
  }
  function _hideInstall() {
    document.querySelectorAll('#pwa-install-wrap').forEach(el => el.style.display = 'none');
  }

  if (_isStand) {
    _hideInstall();
  } else if (_isIOS && _isSafari) {
    _showInstall();
  } else if (_isMacSaf) {
    _showInstall();
  } else {
    window.addEventListener('beforeinstallprompt', e => {
      e.preventDefault();
      _deferredPrompt = e;
      _showInstall();
    });
  }

  window.addEventListener('appinstalled', _hideInstall);
  window.matchMedia('(display-mode: standalone)').addEventListener('change', e => {
    if (e.matches) _hideInstall();
  });

  // Handle clicks on any install button on the page
  document.addEventListener('click', async e => {
    if (!e.target.closest('#pwa-install-btn')) return;
    if (_isIOS && _isSafari) {
      if (typeof _showIOSModal === 'function') _showIOSModal();
      return;
    }
    if (_isMacSaf) {
      if (typeof _showMacModal === 'function') _showMacModal();
      return;
    }
    if (!_deferredPrompt) return;
    _hideInstall();
    _deferredPrompt.prompt();
    const { outcome } = await _deferredPrompt.userChoice;
    _deferredPrompt = null;
    if (outcome !== 'accepted') _showInstall();
  });
})();
