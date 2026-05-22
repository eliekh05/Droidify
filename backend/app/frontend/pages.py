"""
frontend/pages.py
=================
All HTML pages built from a single _page() template function.
Each page only defines what's unique to it — title, description,
active nav item, JS files, and body content.
"""
from __future__ import annotations

# ── Loading splash (shared inline CSS + HTML) ─────────────────────────────────
_SPLASH_CSS = """
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
"""

_SPLASH_HTML = """
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
"""

# ── Nav items ─────────────────────────────────────────────────────────────────
_NAV_ITEMS = [
    ("home",       "/",                "Home"),
    ("devices",    "/devices.html",    "Devices"),
    ("roms",       "/roms.html",       "ROMs"),
    ("recoveries", "/recoveries.html", "Recoveries"),
    ("tools",      "/tools.html",      "Tools"),
    ("android",    "/android.html",    "Android"),
    ("guides",     "/guides.html",     "Guides"),
]

def _nav(active: str) -> str:
    links = "\n".join(
        f'      <a href="{href}" class="nav-link{" active" if key == active else ""}" data-page="{key}">{label}</a>'
        for key, href, label in _NAV_ITEMS
    )
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="accent">Droid</span>ify</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav id="main-nav">
{links}
      <a href="https://github.com/eliekh05/Droidify" class="btn-github" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        GitHub
      </a>
    </nav>
  </div>
</header>"""

_FOOTER = """<footer class="site-footer">
  <div class="container">
    <p>Droidify &mdash; Live Android ecosystem indexer &middot; Free &amp; open sources only &middot; No signin required &middot; <a href="/privacy.html" style="color:var(--muted);text-decoration:underline">Privacy</a></p>
  </div>
</footer>"""

_DISMISS_JS = """
<script>
// ── Loading screen dismiss ───────────────────────────────────────────────────
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
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(hide, 800));
  } else {
    setTimeout(hide, 800);
  }
  if (window.location.protocol === 'file:') { hide(); }
  setTimeout(hide, 4000);
})();
// ── Nav toggle ───────────────────────────────────────────────────────────────
const _nt = document.getElementById('nav-toggle');
const _nm = document.getElementById('main-nav');
if (_nt && _nm) {
  _nt.addEventListener('click', () => {
    const open = _nm.classList.toggle('nav-open');
    _nt.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}
// ── Service Worker ───────────────────────────────────────────────────────────
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js").then(reg => {
    if ("sync" in reg) {
      navigator.serviceWorker.addEventListener("message", e => {
        if (e.data?.type === "SYNC_COMPLETE") {
          const q = document.getElementById("global-search") || document.getElementById("search-input");
          if (q && q.value) q.dispatchEvent(new Event("input"));
        }
      });
    }
    if ("periodicSync" in reg) {
      reg.periodicSync.register("droidify-refresh", { minInterval: 24 * 60 * 60 * 1000 }).catch(() => {});
    }
  }).catch(() => {});
}
</script>"""

_SAFARI_FIX = """  <script>
    (function() {
      var vp = document.querySelector('meta[name=viewport]');
      if (!vp) return;
      if (!/iphone|ipad|ipod/i.test(navigator.userAgent) &&
          !(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return;
      if (window.innerWidth >= 960) {
        vp.setAttribute('content', 'width=' + window.innerWidth + ', initial-scale=1.0');
      }
    })();
  </script>"""


def _page(
    *,
    title: str,
    description: str,
    active: str,
    body: str,
    js: list[str],
    extra_head: str = "",
) -> str:
    """Single template for every page."""
    js_tags = "\n".join(f'<script src="/js/{f}"></script>' for f in js)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <title>{title}</title>
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="manifest" href="/manifest.json" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <meta name="theme-color" content="#3dd68c" />
{_SAFARI_FIX}
<style>{_SPLASH_CSS}</style>
{extra_head}
</head>
<body>
{_SPLASH_HTML}
{_nav(active)}
{body}
{_FOOTER}
{js_tags}
{_DISMISS_JS}
</body>
</html>"""


# ── Pages ─────────────────────────────────────────────────────────────────────

def _index_body() -> str:
    return """<main class="container">
  <section class="hero">
    <h1 class="hero-title"><span class="accent">Droid</span>ify</h1>
    <p class="hero-sub">Devices, ROMs, recoveries, and tools &mdash; fetched in real time from LineageOS, Wikipedia, OrangeFox, TWRP, GitHub and more. Zero hardcoded data. No signin. No payment.</p>
    <div class="search-bar hero-search">
      <input type="search" id="global-search" placeholder="Search device, codename or manufacturer..." autocomplete="off" />
      <button class="btn-primary" id="search-btn">Search</button>
    </div>
    <div id="pwa-install-wrap"></div>
  </section>

  <div class="sources-banner reveal">
    <div class="badges" id="source-badges">
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
    </div>
    <span class="sources-note">All free &middot; No signin &middot; Live data</span>
  </div>

  <section class="section">
    <div class="section-header">
      <h2>Featured devices</h2>
      <a href="/devices.html" class="section-link">Browse all &rarr;</a>
    </div>
    <div class="reveal-grid" id="featured-devices"></div>
  </section>

  <section class="section">
    <div class="section-header">
      <h2>Stats</h2>
    </div>
    <div class="stats-box reveal" id="stats-box">
      <div class="stat-item"><div class="stat-value" id="stat-devices">—</div><div class="stat-label">Devices indexed</div></div>
      <div class="stat-item"><div class="stat-value" id="stat-roms">—</div><div class="stat-label">ROM builds</div></div>
      <div class="stat-item"><div class="stat-value" id="stat-recoveries">—</div><div class="stat-label">Recovery builds</div></div>
      <div class="stat-item"><div class="stat-value" id="stat-tools">—</div><div class="stat-label">Tools listed</div></div>
      <div class="stat-item"><div class="stat-value" id="stat-android">—</div><div class="stat-label">Android versions</div></div>
    </div>
  </section>

  <section class="section">
    <div class="section-header">
      <h2>ROM families</h2>
      <a href="/roms.html" class="section-link">Browse all &rarr;</a>
    </div>
    <div class="reveal-grid" id="rom-families"></div>
  </section>

  <section class="section">
    <div class="section-header">
      <h2>Android versions</h2>
      <a href="/android.html" class="section-link">Full history &rarr;</a>
    </div>
    <div id="android-pills" class="android-pills reveal"></div>
    <div class="reveal-grid" id="android-versions"></div>
  </section>
</main>"""


def _devices_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>Devices</h1>
    <p class="page-sub">Browse and search over 1,100 Android devices</p>
  </div>
  <div class="filters-bar">
    <input type="search" id="search-input" placeholder="Search device, codename or manufacturer..." autocomplete="off" />
    <select id="brand-filter"><option value="">All brands</option></select>
    <select id="rom-filter"><option value="">All ROM support</option><option value="lineageos">LineageOS</option><option value="grapheneos">GrapheneOS</option><option value="twrp">TWRP</option></select>
    <button class="btn-primary" id="search-btn">Search</button>
  </div>
  <div id="results-meta"></div>
  <div class="reveal-grid" id="device-grid"></div>
  <div id="pagination"></div>
</main>"""


def _device_body() -> str:
    return """<main class="container">
  <div id="device-detail">
    <div class="card skeleton" style="height:200px"></div>
  </div>
</main>"""


def _roms_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>ROMs</h1>
    <p class="page-sub">Browse custom Android ROMs across all supported devices</p>
  </div>
  <div class="filters-bar">
    <input type="search" id="search-input" placeholder="Search ROM name..." autocomplete="off" />
    <select id="android-filter"><option value="">All Android versions</option></select>
    <select id="type-filter"><option value="">All types</option><option value="official">Official</option><option value="unofficial">Unofficial</option></select>
    <button class="btn-primary" id="search-btn">Search</button>
  </div>
  <div id="results-meta"></div>
  <div class="reveal-grid" id="rom-grid"></div>
  <div id="pagination"></div>
</main>"""


def _recoveries_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>Recoveries</h1>
    <p class="page-sub">TWRP, OrangeFox, SHRP and more</p>
  </div>
  <div class="filters-bar">
    <input type="search" id="search-input" placeholder="Search device or recovery..." autocomplete="off" />
    <select id="recovery-filter"><option value="">All recoveries</option><option value="twrp">TWRP</option><option value="orangefox">OrangeFox</option></select>
    <button class="btn-primary" id="search-btn">Search</button>
  </div>
  <div id="results-meta"></div>
  <div class="reveal-grid" id="recovery-grid"></div>
  <div id="pagination"></div>
</main>"""


def _tools_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>Tools</h1>
    <p class="page-sub">Root, flash, and Android development tools</p>
  </div>
  <div class="filters-bar">
    <input type="search" id="search-input" placeholder="Search tools..." autocomplete="off" />
    <select id="category-filter"><option value="">All categories</option></select>
    <button class="btn-primary" id="search-btn">Search</button>
  </div>
  <div class="reveal-grid" id="tools-grid"></div>
</main>"""


def _android_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>Android versions</h1>
    <p class="page-sub">Complete Android release history</p>
  </div>
  <div class="reveal-grid" id="android-grid"></div>
</main>"""


def _guides_body() -> str:
    return """<main class="container">
  <div class="page-header">
    <h1>Guides</h1>
    <p class="page-sub">Flashing, rooting, and Android modding guides</p>
  </div>
  <div class="filters-bar">
    <input type="search" id="search-input" placeholder="Search guides..." autocomplete="off" />
    <select id="category-filter"><option value="">All categories</option></select>
    <button class="btn-primary" id="search-btn">Search</button>
  </div>
  <div class="reveal-grid" id="guides-grid"></div>
</main>"""


def _privacy_body() -> str:
    return """<main class="container">
  <div class="page-header" style="margin-bottom:2rem">
    <h1>Privacy Policy</h1>
    <p class="page-sub">Last updated: May 2026</p>
  </div>
  <div style="max-width:720px;display:flex;flex-direction:column;gap:1.5rem">
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">What Droidify is</h2>
      <p style="color:var(--muted);line-height:1.7">Droidify is a read-only Android ROM and device indexer. It fetches public data from upstream sources and serves it through a web interface. It has no user accounts, authentication, or user-generated content.</p>
    </section>
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">Data we do not collect</h2>
      <ul style="color:var(--muted);line-height:1.9;padding-left:1.25rem">
        <li>No personal information</li>
        <li>No cookies &mdash; session or persistent</li>
        <li>No analytics or tracking scripts</li>
        <li>No advertising</li>
        <li>No device fingerprinting</li>
        <li>No location data</li>
        <li>No payment information</li>
      </ul>
    </section>
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">What the server sees</h2>
      <p style="color:var(--muted);line-height:1.7">Like any web server, Droidify's host receives your IP address and User-Agent string as part of the HTTP request. These are standard web logs retained by the hosting provider. Droidify itself does not store, process, or analyse these logs.</p>
    </section>
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">Cookies &amp; local storage</h2>
      <p style="color:var(--muted);line-height:1.7">Droidify sets no cookies and writes nothing to localStorage, sessionStorage, or IndexedDB.</p>
    </section>
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">Third-party links</h2>
      <p style="color:var(--muted);line-height:1.7">Device and ROM pages link to external sources (LineageOS, SourceForge, GitHub, TWRP, OrangeFox, etc.). These sites have their own privacy policies. Droidify has no control over or affiliation with them.</p>
    </section>
    <section>
      <h2 style="font-size:1.1rem;font-weight:700;margin-bottom:.6rem">Contact</h2>
      <p style="color:var(--muted);line-height:1.7">Questions can be raised via <a href="https://github.com/eliekh05/Droidify/issues" target="_blank" rel="noopener">GitHub Issues</a>.</p>
    </section>
    <div style="margin-top:1rem;padding:.85rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);font-size:.82rem;color:var(--muted)">
      Short version: Droidify collects nothing about you. It reads public Android ROM data and shows it to you.
    </div>
  </div>
</main>"""


# ── Public page strings ────────────────────────────────────────────────────────

index = _page(
    title="Droidify — Android ROM & Device Index",
    description="Live Android ROM, device and tool indexer. Search ROMs, recoveries, root tools and flashing guides for any Android device.",
    active="home",
    body=_index_body(),
    js=["api.js", "home.js"],
)

devices = _page(
    title="Devices — Droidify",
    description="Browse and search over 1,100 Android devices. Find custom ROMs, recoveries and guides for your device.",
    active="devices",
    body=_devices_body(),
    js=["api.js", "devices.js"],
)

device = _page(
    title="Device — Droidify",
    description="Custom ROMs, recoveries and guides for your Android device.",
    active="devices",
    body=_device_body(),
    js=["api.js", "device-detail.js"],
)

roms = _page(
    title="ROMs — Droidify",
    description="Browse custom Android ROMs including LineageOS, GrapheneOS, crDroid, Evolution X and more.",
    active="roms",
    body=_roms_body(),
    js=["api.js", "roms.js"],
)

recoveries = _page(
    title="Recoveries — Droidify",
    description="Browse TWRP, OrangeFox, SHRP and other custom Android recoveries.",
    active="recoveries",
    body=_recoveries_body(),
    js=["api.js", "recoveries.js"],
)

tools = _page(
    title="Tools — Droidify",
    description="Android root, flash, and development tools.",
    active="tools",
    body=_tools_body(),
    js=["api.js", "tools.js"],
)

android = _page(
    title="Android versions — Droidify",
    description="Complete Android version history from Android 1.0 to the latest release.",
    active="android",
    body=_android_body(),
    js=["api.js", "android.js"],
)

guides = _page(
    title="Guides — Droidify",
    description="Android flashing, rooting and modding guides for popular devices.",
    active="guides",
    body=_guides_body(),
    js=["api.js", "guides.js"],
)


def privacy() -> str:
    return _page(
        title="Privacy Policy — Droidify",
        description="Droidify privacy policy — no tracking, no cookies, no user data collected.",
        active="",
        body=_privacy_body(),
        js=["api.js"],
    )


page_404 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>404 — Droidify</title>
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh">
  <div style="text-align:center">
    <div style="font-size:4rem;font-weight:800;color:var(--accent)">404</div>
    <p style="color:var(--muted);margin:.5rem 0 1.5rem">Page not found</p>
    <a href="/" class="btn-primary">Go home</a>
  </div>
</body>
</html>"""
