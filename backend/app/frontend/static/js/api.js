/**
 * Droidify API client — pure JS, no framework.
 * Communicates with the FastAPI backend.
 */

// API is always same-origin — FastAPI serves both frontend and /api/*
const API_BASE = '';

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


// ── Motion system ────────────────────────────────────────────────────────────
(function() {
  const prefersMotion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersMotion) document.documentElement.classList.add('js-anim');

  // ── Scroll reveal via IntersectionObserver ──────────────────────────────
  // Works in all browsers — no animation-timeline needed
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    const observe = () => {
      document.querySelectorAll('.reveal, .reveal-grid').forEach(el => {
        revealObserver.observe(el);
      });
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', observe);
    } else {
      observe();
    }

    // Re-observe after dynamic content is added (grid updates)
    window._reObserve = () => {
      document.querySelectorAll('.reveal, .reveal-grid').forEach(el => {
        if (!el.classList.contains('visible')) {
          revealObserver.observe(el);
        }
      });
    };
  } else {
    // Fallback: show everything immediately
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.reveal, .reveal-grid').forEach(el => {
        el.classList.add('visible');
      });
    });
  }

  function showAll() {
    document.querySelectorAll('.reveal, .reveal-grid').forEach(el => el.classList.add('visible'));
  }
  setTimeout(showAll, 800); // hard failsafe

  if (!('IntersectionObserver' in window)) { showAll(); window._reObserve = showAll; return; }

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0 });

  function observeAll() {
    document.querySelectorAll('.reveal:not(.visible),.reveal-grid:not(.visible)').forEach(el => obs.observe(el));
  }
  observeAll();
  requestAnimationFrame(observeAll);
  setTimeout(observeAll, 150);
  window._reObserve = observeAll;
})();

// ── Wild number counter ───────────────────────────────────────────────────────
window._rollNumber = function(el, target, duration) {
  if (!el || isNaN(target)) return;
  duration = duration || 1400;
  const prefersMotion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!prefersMotion) { el.textContent = target.toLocaleString(); return; }

  const start = performance.now();
  const startVal = 0;
  // Easing: ease out expo
  function ease(t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); }

  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const current = Math.round(ease(progress) * (target - startVal) + startVal);
    // Slot-machine digit roll effect
    const str = current.toLocaleString();
    el.innerHTML = str.split('').map((ch, i) =>
      /\d/.test(ch)
        ? '<span class="stat-digit" style="animation-delay:' + (i*30) + 'ms;display:inline-block;">' + ch + '</span>'
        : '<span style="display:inline-block;">' + ch + '</span>'
    ).join('');
    if (progress < 1) requestAnimationFrame(frame);
    else el.textContent = target.toLocaleString();
  }
  requestAnimationFrame(frame);
};

// ── PWA Install ──────────────────────────────────────────────────────────────
(function() {
  const ua      = navigator.userAgent;
  const isIOS   = /iphone|ipad|ipod/i.test(ua) || (navigator.platform==='MacIntel' && navigator.maxTouchPoints>1);
  const isSaf   = /safari/i.test(ua) && !/chrome|crios|chromium|android|fxios|gsa/i.test(ua);
  const isMacOS = /macintosh/i.test(ua) && !isIOS;
  const isMacSaf= isMacOS && isSaf;
  const isChrome= /chrome/i.test(ua) && !/edge|opr/i.test(ua);
  const isEdge  = ua.toLowerCase().indexOf('edg/') !== -1;
  function isStand() {
    return matchMedia('(display-mode:standalone)').matches ||
           matchMedia('(display-mode:fullscreen)').matches ||
           navigator.standalone===true;
  }
  let deferred=null, installed=false;
  function show() {
    if (installed || isStand()) return;
    document.querySelectorAll('#pwa-install-wrap').forEach(el => {
      if (el.querySelector('.btn-install')) {
        el.style.display = 'flex';
        return;
      }
      // Determine button label based on platform
      let label = '⬇ Install App';
      if (isIOS && isSaf) label = '⬇ Add to Home Screen';
      else if (isMacSaf) label = '⬇ Install on Mac';

      const btn = document.createElement('button');
      btn.className = 'btn-install';
      btn.id = 'pwa-install-btn';
      btn.textContent = label;
      btn.setAttribute('aria-label', 'Install Droidify as an app');
      el.appendChild(btn);
      el.style.display = 'flex';
      el.style.alignItems = 'center';
      el.style.gap = '8px';

      btn.addEventListener('click', async () => {
        if (!btn.id) return;
        if (isIOS && isSaf) { if (typeof _showIOSModal === 'function') _showIOSModal(); return; }
        if (isMacSaf)       { if (typeof _showMacModal === 'function') _showMacModal(); return; }
        if (deferred) {
          hide(); deferred.prompt();
          const { outcome } = await deferred.userChoice; deferred = null;
          if (outcome !== 'accepted') show();
        } else {
          alert('To install: open your browser menu and choose "Install app" or "Add to Home Screen".');
        }
      });
    });
  }
  function hide() { document.querySelectorAll('#pwa-install-wrap').forEach(el => el.style.display = 'none'); }
  if (isStand()) { hide(); return; }
  show(); // Always show — hide only after actual install
  if (isChrome||isEdge) {
    addEventListener('beforeinstallprompt', e=>{ e.preventDefault(); deferred=e; });
  }
  addEventListener('appinstalled', ()=>{ installed=true; hide(); });
  matchMedia('(display-mode:standalone)').addEventListener('change', e=>{ if(e.matches){installed=true;hide();} });
  document.addEventListener('click', async e=>{
    if (!e.target.closest('#pwa-install-btn')) return;
    if (isIOS&&isSaf) { if(typeof _showIOSModal==='function') _showIOSModal(); return; }
    if (isMacSaf)     { if(typeof _showMacModal==='function') _showMacModal(); return; }
    if (deferred) {
      hide(); deferred.prompt();
      const {outcome} = await deferred.userChoice; deferred=null;
      if (outcome!=='accepted') show();
    } else { alert('To install: open your browser menu and choose "Install app" or "Add to Home Screen".'); }
  });
})();

function _showMacModal() {
  document.getElementById('mac-install-modal')?.remove();
  const d=document.createElement('div'); d.id='mac-install-modal';
  d.innerHTML=`<div class="ios-modal-backdrop" id="mac-bd"></div><div class="ios-modal-sheet" role="dialog" aria-modal="true"><div class="ios-modal-handle"></div><div class="ios-modal-header"><img src="/icons/icon-192.png" class="ios-modal-icon" alt="Droidify"/><div><div class="ios-modal-title">Install Droidify</div><div class="ios-modal-sub">Add to Mac Dock</div></div><button class="ios-modal-close" id="mac-cls">✕</button></div><div class="ios-modal-steps"><div class="ios-modal-step"><div class="ios-step-num">1</div><div class="ios-step-content"><div class="ios-step-title">Click File in the menu bar</div><div class="ios-step-desc">Top-left of screen, then choose Add to Dock</div></div></div><div class="ios-modal-divider"></div><div class="ios-modal-step"><div class="ios-step-num">2</div><div class="ios-step-content"><div class="ios-step-title">Choose "Add to Dock"</div></div></div><div class="ios-modal-divider"></div><div class="ios-modal-step"><div class="ios-step-num">3</div><div class="ios-step-content"><div class="ios-step-title">Click "Add"</div></div></div></div></div>`;
  document.body.appendChild(d);
  requestAnimationFrame(()=>d.querySelector('.ios-modal-sheet').classList.add('ios-modal-open'));
  const close=()=>{d.querySelector('.ios-modal-sheet').classList.remove('ios-modal-open');setTimeout(()=>d.remove(),300);};
  document.getElementById('mac-bd').addEventListener('click',close);
  document.getElementById('mac-cls').addEventListener('click',close);
}