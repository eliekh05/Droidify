"""Embedded HTML pages — auto-generated. Do not edit manually."""

index = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Live Android ROM, device and tool indexer. Search ROMs, recoveries, root tools and flashing guides for any Android device." />
  <title>Droidify — Android ROM & Device Index</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>


<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link active" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>

<main class="container">

  <!-- Hero -->
  <section class="hero reveal">
    <h1>Android ecosystem, indexed live</h1>
    <p class="hero-sub">
      Devices, ROMs, recoveries, and tools — fetched in real time from
      LineageOS, Wikipedia, OrangeFox, TWRP, GitHub and more.
      Zero hardcoded data. No signin. No payment.
    </p>
    <div class="search-bar">
      <input
        id="global-search"
        type="search"
        placeholder="Search device, codename or manufacturer…"
        autocomplete="off"
        spellcheck="false"
      />
      <button id="search-btn">Search</button>
    </div>

  </section>

  <!-- Stats row (live) -->
  <section class="stats-box stats-fade" id="stats-row">
    <div class="stat-item skeleton" id="stat-devices">
      <span class="stat-value">—</span>
      <span class="stat-label">Devices indexed</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item skeleton" id="stat-roms">
      <span class="stat-value">—</span>
      <span class="stat-label">ROM builds</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item skeleton" id="stat-recoveries">
      <span class="stat-value">—</span>
      <span class="stat-label">Recovery devices</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item skeleton" id="stat-tools">
      <span class="stat-value">—</span>
      <span class="stat-label">Tools tracked</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item skeleton" id="stat-android">
      <span class="stat-value">—</span>
      <span class="stat-label">Android versions</span>
    </div>
  </section>

  <!-- Sources badge -->
  <div class="sources-banner reveal">
    <span class="badge">LineageOS API</span>
    <span class="badge">Wikipedia</span>
    <span class="badge">OrangeFox API</span>
    <span class="badge">TWRP</span>
    <span class="badge">GrapheneOS</span>
    <span class="badge">GitHub API</span>
    <span class="badge">crDroid</span>
    <span class="badge">DivestOS</span>
    <span class="badge">CalyxOS</span>
    <span class="badge">/e/OS</span>
    <span class="note">All free · No signin · Live data</span>
  </div>

  <!-- Featured devices grid -->
  <section class="section">
    <div class="section-header">
      <h2>Featured devices</h2>
      <a href="/devices.html" class="see-all">Browse all →</a>
    </div>
    <div class="device-grid reveal-grid" id="featured-devices">
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
    </div>
  </section>

  <!-- Latest Android versions -->
  <section class="section">
    <div class="section-header">
      <h2>Android versions</h2>
      <a href="/android.html" class="see-all">Full history →</a>
    </div>
    <div class="version-pills reveal-grid" id="android-pills">
      <div class="pill skeleton"></div>
      <div class="pill skeleton"></div>
      <div class="pill skeleton"></div>
      <div class="pill skeleton"></div>
      <div class="pill skeleton"></div>
    </div>
  </section>

  <!-- Popular ROMs overview -->
  <section class="section">
    <div class="section-header">
      <h2>ROM families</h2>
      <a href="/roms.html" class="see-all">Search ROMs →</a>
    </div>
    <div class="rom-families reveal-grid" id="rom-families">
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
      <div class="card skeleton"></div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="container">
    <p>Droidify — Live Android ecosystem indexer · Free &amp; open sources only · No signin required</p>
    <p class="footer-note">Data sourced from: LineageOS · OrangeFox · TWRP · GrapheneOS · GitHub · crDroid · Evolution X · HavocOS · DerpFest · 20+ ROM projects via SourceForge · PitchBlack · SkyHawk · unofficialTWRP · DivestOS · CalyxOS · /e/OS</p>
  </div>
</footer>

<script src="/js/api.js"></script>
<script src="/js/home.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

devices = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Browse and search over 1,100 Android devices. Find custom ROMs, recoveries and root guides for your device." />
  <title>Devices — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>


<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link active" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>

<main class="container">
  <div class="page-header">
    <h1>Devices</h1>
    <p class="page-sub">Live device index from LineageOS, OrangeFox, TWRP, and 20+ ROM projects. No signin needed.</p>
  </div>

  <!-- Filters -->
  <div class="filter-bar">
    <input
      id="device-search"
      type="search"
      placeholder="Model name, codename, or manufacturer…"
      autocomplete="off"
    />
    <select id="mfr-filter">
      <option value="">All manufacturers</option>
    </select>
    <select id="source-filter">
      <option value="">All sources</option>
      <option value="lineageos">LineageOS</option>
      <option value="orangefox">OrangeFox</option>
      <option value="twrp">TWRP</option>
    </select>
    <button id="search-btn">Search</button>
  </div>

  <!-- Results info -->
  <div class="results-meta" id="results-meta"></div>

  <!-- Device grid -->
  <div class="device-grid" id="device-grid">
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
    <div class="card skeleton"></div>
  </div>

  <!-- Pagination -->
  <div class="pagination" id="pagination"></div>
</main>

<footer class="site-footer">
  <div class="container">
    <p>Droidify — Live data from LineageOS · OrangeFox · TWRP · No hardcoded device list</p>
  </div>
</footer>

<script src="/js/api.js"></script>
<script src="/js/devices.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

device = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Android device detail — specs, available ROMs, recoveries and flashing guides." />
  <title>Device — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>


<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link active" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>

<main class="container" id="device-main">
  <div class="breadcrumb">
    <a href="/devices.html">← All devices</a>
  </div>

  <div id="device-content">
    <!-- Filled by JS -->
    <div class="card skeleton" style="height: 200px; margin-bottom: 1.5rem;"></div>
    <div class="card skeleton" style="height: 300px;"></div>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <p>Droidify — Live data · No hardcoded device information</p>
  </div>
</footer>

<script src="/js/api.js"></script>
<script src="/js/device-detail.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

roms = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Browse custom Android ROMs including LineageOS, GrapheneOS, crDroid, CalyxOS, Ubuntu Touch and Kali NetHunter." />
  <title>ROMs — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link active" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
<main class="container">
  <div class="page-header">
    <h1>ROMs</h1>
    <p class="page-sub">Live ROM index from LineageOS Download API (281 devices) and GrapheneOS. Data fetched in real time.</p>
  </div>
  <div class="filter-bar">
    <input id="rom-search" type="search" placeholder="Search ROM name or device codename…" autocomplete="off" />
    <select id="android-filter">
      <option value="">All Android versions</option>
      <option value="16">Android 16</option>
      <option value="15">Android 15</option>
      <option value="14">Android 14</option>
      <option value="13">Android 13</option>
      <option value="12">Android 12</option>
      <option value="11">Android 11</option>
      <option value="10">Android 10</option>
    </select>
    <button id="search-btn">Search</button>
  </div>
  <div class="results-meta" id="results-meta"></div>
  <div id="rom-list"></div>
  <div class="pagination" id="pagination"></div>
</main>
<footer class="site-footer"><div class="container"><p>Droidify — LineageOS API · GrapheneOS · No hardcoded ROM list</p></div></footer>
<script src="/js/api.js"></script>
<script src="/js/roms.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

recoveries = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Find TWRP and OrangeFox recovery for your Android device. Direct download links." />
  <title>Recoveries — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link active" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
<main class="container">
  <div class="page-header">
    <h1>Custom Recoveries</h1>
    <p class="page-sub">TWRP (896 devices) and OrangeFox (159 devices) — fetched live from official APIs. No auth required.</p>
  </div>
  <div class="filter-bar">
    <input id="rec-search" type="search" placeholder="Codename, model, or manufacturer…" autocomplete="off" />
    <select id="rec-filter">
      <option value="">All recoveries</option>
      <option value="TWRP">TWRP</option>
      <option value="OrangeFox">OrangeFox</option>
    </select>
    <select id="mfr-filter">
      <option value="">All manufacturers</option>
    </select>
    <button id="search-btn">Search</button>
  </div>
  <div class="results-meta" id="results-meta"></div>
  <div class="device-grid" id="rec-grid"></div>
  <div class="pagination" id="pagination"></div>
</main>
<footer class="site-footer"><div class="container"><p>Droidify — TWRP · OrangeFox · Live recovery index</p></div></footer>
<script src="/js/api.js"></script>
<script src="/js/recoveries.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

tools = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Android root tools and flashing utilities — Magisk, KernelSU, APatch, Odin, Heimdall, SP Flash Tool and more." />
  <title>Tools — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link active" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
<main class="container">
  <div class="page-header">
    <h1>Root, Recovery &amp; Flashing Tools</h1>
    <p class="page-sub">Latest versions fetched live from GitHub (unauthenticated). Magisk, KernelSU, APatch, LSPosed, Heimdall, and more.</p>
  </div>
  <div class="filter-bar">
    <select id="cat-filter">
      <option value="">All categories</option>
      <option value="root">Root</option>
      <option value="xposed">Xposed / Zygisk</option>
      <option value="flashing">Flashing</option>
      <option value="recovery">Recovery</option>
    </select>
    <select id="status-filter">
      <option value="">All statuses</option>
      <option value="active">Active</option>
      <option value="discontinued">Discontinued</option>
    </select>
    <button id="filter-btn">Filter</button>
  </div>
  <div id="tools-container"></div>
</main>
<footer class="site-footer"><div class="container"><p>Droidify — GitHub API (unauthenticated) · Live tool versions · No hardcoded data</p></div></footer>
<script src="/js/api.js"></script>
<script src="/js/tools.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

android = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Complete Android version history from Android 1.0 to the latest preview. API levels, version codes and usage stats." />
  <title>Android Versions — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link active" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
<main class="container">
  <div class="page-header">
    <h1>Android Version History</h1>
    <p class="page-sub">
      Fetched live from
      <a href="https://apilevels.com" target="_blank" rel="noopener">apilevels.com</a>
      (primary) with
      <a href="https://en.wikipedia.org/wiki/Android_version_history" target="_blank" rel="noopener">Wikipedia</a>
      fallback. Android 1.0 (2008) → Android 17 Preview (2026). Includes cumulative usage data.
    </p>
  </div>

  <div class="filter-bar">
    <select id="status-filter">
      <option value="">All statuses</option>
      <option value="active">Active (supported)</option>
      <option value="partial">Preview / Beta</option>
      <option value="unsupported">EOL / Unsupported</option>
    </select>
    <input id="api-min" type="number" placeholder="Min API level" min="1" max="40" style="width:140px" />
    <button id="filter-btn">Filter</button>
    <span id="source-label" style="font-size:.78rem;color:var(--muted);margin-left:.5rem"></span>
  </div>

  <div class="table-wrap">
    <table id="android-table">
      <thead>
        <tr>
          <th>Version</th>
          <th>Codename</th>
          <th>API</th>
          <th>Version Code</th>
          <th>Year</th>
          <th>Usage</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody id="android-tbody">
        <tr><td colspan="7" class="loading-cell">Fetching from apilevels.com…</td></tr>
      </tbody>
    </table>
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <p>Droidify — Data from <a href="https://apilevels.com" target="_blank">apilevels.com</a> · <a href="https://en.wikipedia.org/wiki/Android_version_history" target="_blank">Wikipedia</a> · No hardcoded version data</p>
  </div>
</footer>
<script src="/js/api.js"></script>
<script src="/js/android.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

guides = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Step-by-step Android guides — unlock bootloader, install recovery, root, flash ROM, backup and unbrick." />
  <title>Guides — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <style>
    .guide-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 1rem; overflow: hidden; }
    .guide-header { padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: .75rem; cursor: pointer; user-select: none; }
    .guide-header:hover { background: var(--card2); }
    .guide-title { font-weight: 700; font-size: 1rem; }
    .guide-source { font-size: .75rem; color: var(--muted); }
    .guide-toggle { color: var(--muted); font-size: 1.1rem; transition: transform 180ms ease; }
    .guide-body { display: none; padding: 0 1.25rem 1.25rem; border-top: 1px solid var(--border); }
    .guide-body.open { display: block; }
    .guide-toggle.open { transform: rotate(180deg); }
    .guide-note { background: rgba(251,191,36,.07); border: 1px solid rgba(251,191,36,.25); border-radius: var(--radius-sm); padding: .65rem 1rem; font-size: .83rem; color: rgba(251,191,36,.9); margin: .85rem 0; }
    .guide-section { margin-top: 1rem; }
    .guide-section h3 { font-size: .85rem; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); margin-bottom: .6rem; }
    .guide-steps { list-style: none; padding: 0; counter-reset: step; }
    .guide-steps li { counter-increment: step; display: flex; gap: .75rem; align-items: flex-start; padding: .45rem 0; border-bottom: 1px solid var(--border); font-size: .88rem; }
    .guide-steps li:last-child { border-bottom: none; }
    .guide-steps li::before { content: counter(step); min-width: 24px; height: 24px; background: var(--card2); border: 1px solid var(--border); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .72rem; font-weight: 700; color: var(--accent); flex-shrink: 0; margin-top: .1rem; }
    .guide-steps li.note-item { font-style: italic; color: var(--muted); }
    .guide-steps li.note-item::before { content: "⚠"; background: rgba(251,191,36,.1); border-color: rgba(251,191,36,.3); color: var(--warn); }
    .type-tabs { display: flex; flex-wrap: wrap; gap: .4rem; margin: 1.25rem 0; }
    .type-tab { background: var(--card); border: 1px solid var(--border); color: var(--muted); border-radius: 100px; padding: .3rem .85rem; font-size: .82rem; cursor: pointer; transition: all 180ms ease; }
    .type-tab:hover, .type-tab.active { background: var(--accent); border-color: var(--accent); color: #0b0f14; font-weight: 600; }
  </style>
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link active" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>

<main class="container">
  <div class="page-header">
    <h1>Flashing &amp; Modding Guides</h1>
    <p class="page-sub">
      Step-by-step guides for flashing ROMs, rooting, unlocking bootloaders,
      installing recoveries, backing up, and unbricking. Search by device for
      device-specific guides from LineageOS Wiki.
    </p>
  </div>

  <!-- Device search -->
  <div class="filter-bar">
    <input id="codename-input" type="search" placeholder="Device codename (e.g. panther, j7elte, alioth)…" autocomplete="off" />
    <select id="mfr-select">
      <option value="">Manufacturer (optional)</option>
      <option value="Google">Google</option>
      <option value="Samsung">Samsung</option>
      <option value="Xiaomi">Xiaomi</option>
      <option value="OnePlus">OnePlus</option>
      <option value="Motorola">Motorola</option>
      <option value="Sony">Sony</option>
      <option value="Fairphone">Fairphone</option>
    </select>
    <button id="load-btn">Load guides</button>
  </div>

  <!-- Type filter tabs -->
  <div class="type-tabs" id="type-tabs" style="display:none">
    <button class="type-tab active" data-type="">All</button>
    <button class="type-tab" data-type="install">Install ROM</button>
    <button class="type-tab" data-type="upgrade">Upgrade</button>
    <button class="type-tab" data-type="root">Root</button>
    <button class="type-tab" data-type="bootloader-unlock">Bootloader Unlock</button>
    <button class="type-tab" data-type="recovery">Recovery</button>
    <button class="type-tab" data-type="backup">Backup</button>
    <button class="type-tab" data-type="unbrick">Unbrick</button>
  </div>

  <div id="guides-container"></div>
</main>

<footer class="site-footer">
  <div class="container">
    <p>Droidify — Guides from LineageOS Wiki · GrapheneOS · Magisk · KernelSU · OEM documentation</p>
  </div>
</footer>

<script src="/js/api.js"></script>
<script src="/js/guides.js"></script>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
</body>
</html>
"""

page_404 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Page not found — Droidify Android ecosystem indexer." />
  <title>Page Not Found — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#3dd68c" />
  <script>
    // Safari "Request Desktop Site" fix
    // In desktop mode Safari reports a wider viewport — detect and force desktop layout
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      // If not iOS/iPadOS skip
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      // Desktop mode: innerWidth will be ~980px or more (Safari default desktop width)
      // Mobile mode: innerWidth matches device CSS width (usually 390px or similar)
      if (window.innerWidth >= 960) {
        // Already in desktop mode — keep it that way
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>
<style>
  /* ── Loading splash screen (inline — runs before style.css) ── */
  #ls{position:fixed;inset:0;background:#0b0f14;display:flex;align-items:center;justify-content:center;z-index:99999;transition:opacity 400ms ease,visibility 400ms ease;overflow:hidden}
  #ls.ls-hide{opacity:0;visibility:hidden;pointer-events:none}
  .ls-bg{position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .ls-ring{position:absolute;border-radius:50%;border:1px solid rgba(61,214,140,.08);animation:lsRP 3s ease-in-out infinite}
  .ls-ring:nth-child(1){width:220px;height:220px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:0s}
  .ls-ring:nth-child(2){width:340px;height:340px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.4s}
  .ls-ring:nth-child(3){width:460px;height:460px;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:.8s}
  @keyframes lsRP{0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}50%{opacity:.7;transform:translate(-50%,-50%) scale(1.04)}}
  .ls-particle{position:absolute;width:3px;height:3px;background:#3dd68c;border-radius:50%;opacity:0;animation:lsFL var(--d,4s) ease-in-out var(--delay,0s) infinite}
  @keyframes lsFL{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) scale(1.5)}}
  .ls-inner{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:1}
  .ls-icon-bg{width:72px;height:72px;background:#121820;border:1.5px solid #1e2a3a;border-radius:18px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;margin-bottom:20px;animation:lsIP 600ms cubic-bezier(.34,1.56,.64,1) both}
  @keyframes lsIP{from{opacity:0;transform:scale(.5) rotate(-8deg)}to{opacity:1;transform:scale(1) rotate(0)}}
  .ls-icon-shine{position:absolute;inset:0;background:linear-gradient(135deg,rgba(61,214,140,.15) 0%,transparent 60%);border-radius:inherit}
  .ls-icon-d{font-size:32px;font-weight:800;color:#3dd68c;font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.04em;line-height:1;position:relative;z-index:1}
  .ls-logo{font-size:2.1rem;font-weight:800;letter-spacing:-.04em;color:#e8eef5;font-family:system-ui,-apple-system,sans-serif;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 200ms both;margin-bottom:6px}
  .ls-logo .accent{color:#3dd68c}
  .ls-tag{font-size:.72rem;color:#4a6080;font-family:system-ui,-apple-system,sans-serif;letter-spacing:.12em;text-transform:uppercase;animation:lsFU 500ms cubic-bezier(.22,1,.36,1) 320ms both;margin-bottom:28px}
  @keyframes lsFU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
  .ls-bar-wrap{width:140px;height:2px;background:#1a2535;border-radius:2px;overflow:hidden;animation:lsFU 400ms ease 420ms both;margin-bottom:14px}
  .ls-bar{height:100%;width:0%;background:#3dd68c;border-radius:2px;animation:lsBAR 1800ms cubic-bezier(.4,0,.2,1) 500ms forwards;box-shadow:0 0 8px rgba(61,214,140,.5)}
  @keyframes lsBAR{0%{width:0%}30%{width:45%}60%{width:72%}85%{width:88%}100%{width:100%}}
  .ls-dots{display:flex;gap:5px;animation:lsFU 400ms ease 520ms both}
  .ls-dot{width:4px;height:4px;background:#3dd68c;border-radius:50%;opacity:.3;animation:lsDT 1.2s ease-in-out infinite}
  .ls-dot:nth-child(2){animation-delay:.2s}
  .ls-dot:nth-child(3){animation-delay:.4s}
  @keyframes lsDT{0%,80%,100%{opacity:.2;transform:scale(1)}40%{opacity:1;transform:scale(1.4)}}
</style>
</head>
<body>
<div id="ls" aria-hidden="true" role="presentation">
  <div class="ls-bg">
    <div class="ls-ring"></div><div class="ls-ring"></div><div class="ls-ring"></div>
  </div>
  <div class="ls-inner">
    <div class="ls-icon-bg">
      <div class="ls-icon-shine"></div>
      <div class="ls-icon-d">D</div>
    </div>
    <div class="ls-logo"><span class="accent">Droid</span>ify</div>
    <div class="ls-tag">Android ecosystem</div>
    <div class="ls-bar-wrap"><div class="ls-bar"></div></div>
    <div class="ls-dots"><div class="ls-dot"></div><div class="ls-dot"></div><div class="ls-dot"></div></div>
  </div>
</div>
<script>
(function(){
  var bg=document.querySelector('.ls-bg');
  for(var i=0;i<12;i++){
    var p=document.createElement('div');
    p.className='ls-particle';
    p.style.cssText='left:'+(20+Math.random()*60)+'%;bottom:'+(10+Math.random()*40)+'%;--d:'+(3+Math.random()*3)+'s;--delay:'+(Math.random()*2)+'s';
    bg.appendChild(p);
  }
})();
</script>

<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
      <a href="/" class="nav-link" data-page="home">Home</a>
      <a href="/devices.html" class="nav-link" data-page="devices">Devices</a>
      <a href="/roms.html" class="nav-link" data-page="roms">ROMs</a>
      <a href="/recoveries.html" class="nav-link" data-page="recoveries">Recoveries</a>
      <a href="/tools.html" class="nav-link" data-page="tools">Tools</a>
      <a href="/android.html" class="nav-link" data-page="android">Android</a>
      <a href="/guides.html" class="nav-link" data-page="guides">Guides</a>
    </nav>
    <div class="nav-actions">
      <div id="pwa-install-wrap" style="display:none">
        <button id="pwa-install-btn" type="button" class="btn btn-install btn-sm">
          ⬇ Install
        </button>
      </div>
      <a href="https://github.com/eliekh05/Droidify" target="_blank" rel="noopener" class="btn btn-github btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836a9.59 9.59 0 0 1 2.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>
<main class="container" style="display:flex;align-items:center;justify-content:center;min-height:60vh">
  <div style="text-align:center">
    <div style="font-size:4rem;margin-bottom:1rem">🤖</div>
    <h1 style="font-size:2rem;font-weight:800;margin-bottom:.5rem">404 — Page Not Found</h1>
    <p style="color:var(--muted);margin-bottom:1.5rem">
      This page doesn't exist. Try searching for a device or ROM instead.
    </p>
    <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap">
      <a href="/" class="btn">← Home</a>
      <a href="/devices.html" class="btn" style="background:var(--border);color:var(--text)">Browse Devices</a>
    </div>
  </div>
</main>
<footer class="site-footer">
  <div class="container"><p>Droidify — Android Ecosystem Indexer</p></div>
</footer>
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script>
// ── Hamburger menu ──────────────────────────────────────────────────────────
const _navToggle = document.getElementById('nav-toggle');
const _mainNav   = document.getElementById('main-nav');
if (_navToggle && _mainNav) {
  _navToggle.addEventListener('click', () => {
    const open = _mainNav.classList.toggle('nav-open');
    _navToggle.setAttribute('aria-expanded', open);
  });
  _mainNav.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', () => {
      _mainNav.classList.remove('nav-open');
      _navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Loading screen ──────────────────────────────────────────────────────────
(function() {
  const screen = document.getElementById('ls');
  if (!screen) return;
  let _hidden = false;
  const hide = () => {
    if (_hidden) return;
    _hidden = true;
    screen.classList.add('ls-hide');
    setTimeout(() => screen.remove(), 450);
  };
  // Hide 800ms after DOM is ready (works on mobile too)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  // Hide immediately if opened as local file (no server)
  if (window.location.protocol === 'file:') { hide(); }
  // Failsafe — force hide after 4s on slow connections
  setTimeout(hide, 4000);
})();
</script>
  <script src="/js/api.js"></script>
</body>
</html>
"""

