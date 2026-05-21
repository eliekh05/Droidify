"""Embedded static assets — auto-generated. Do not edit manually."""
style_css = """/* ── Stats fade-in — no IntersectionObserver, fires on load ──────────────── */
.stats-fade {
  /* Default: visible immediately — no animation dependency */
  opacity: 1;
}
/* Only animate if user hasn't requested reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .stats-fade {
    animation: statsFadeIn 500ms ease forwards;
  }
}
@keyframes statsFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: none; }
}

/* ── Stats one-box ───────────────────────────────────────────────────────── */
.stats-box {
  display: flex;
  flex-direction: row;          /* Always horizontal row */
  align-items: stretch;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin: 2rem 0;
  overflow: hidden;
  min-width: 0;
}
.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem .75rem;
  text-align: center;
  min-width: 0;
}
.stat-divider {
  width: 1px;
  background: var(--border);
  flex-shrink: 0;
  align-self: stretch;
}
.stat-value {
  display: block;
  font-size: 1.65rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}
.stat-label {
  display: block;
  font-size: .72rem;
  color: var(--muted);
  margin-top: .35rem;
  line-height: 1.3;
}
@media (max-width: 640px) {
  .stats-box { flex-wrap: wrap; }
  .stat-item { flex: 1 1 calc(50% - 1px); padding: 1rem .5rem; }
  .stat-divider:nth-child(6) { display: none; }
  .stat-value { font-size: 1.35rem; }
  .stat-label { font-size: .68rem; }
  /* 5th item (Android versions) centered on last row */
  .stats-box .stat-item:nth-child(9) {
    flex: 0 0 50%;
    margin: 0 auto;
  }
}

/* Droidify — Pure CSS, no framework dependencies */

/* ── Reset & base ──────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #0b0f14;
  --card:     #121820;
  --card2:    #18212c;
  --border:   #1e2a3a;
  --accent:   #3dd68c;
  --accent2:  #2ab875;
  --text:     #e8eef5;
  --muted:    #8b9cb3;
  --danger:   #f87171;
  --warn:     #fbbf24;
  --info:     #60a5fa;
  --radius:   10px;
  --radius-sm:6px;
  --shadow:   0 2px 12px rgba(0,0,0,.4);
  --transition: 180ms ease;
}

html { scroll-behavior: smooth; }

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  line-height: 1.6;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Layout ────────────────────────────────────────────────────────────────── */
.container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.25rem;
}

main.container { flex: 1; padding-top: 2rem; padding-bottom: 4rem; }

/* ── Header ────────────────────────────────────────────────────────────────── */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--border);
  background: rgba(18, 24, 32, 0.92);
  backdrop-filter: blur(12px);
}

.header-inner {
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 58px;
}
/* Logo always first, flex fills space after nav */
.logo { flex-shrink: 0; }
.nav-toggle { flex-shrink: 0; margin-left: .5rem; }

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -.02em;
  color: var(--text);
}
.logo:hover { text-decoration: none; }
.accent { color: var(--accent); }

nav { display: flex; gap: .25rem; flex-wrap: wrap; }

.nav-link {
  color: var(--muted);
  font-size: .85rem;
  padding: .35rem .65rem;
  border-radius: var(--radius-sm);
  transition: color var(--transition), background var(--transition);
}
.nav-link:hover,
.nav-link.active {
  color: var(--text);
  background: var(--border);
  text-decoration: none;
}
.nav-link.active { color: var(--accent); }

/* ── Hero ──────────────────────────────────────────────────────────────────── */
.hero { text-align: center; padding: 3.5rem 0 2rem; }
.hero h1 {
  font-size: clamp(1.8rem, 5vw, 3rem);
  font-weight: 800;
  letter-spacing: -.03em;
  line-height: 1.15;
}
.hero-sub {
  color: var(--muted);
  max-width: 600px;
  margin: 1rem auto 1.75rem;
  font-size: 1rem;
}

.search-bar {
  display: flex;
  gap: .5rem;
  max-width: 520px;
  margin: 0 auto;
}
.search-bar input { flex: 1; }

/* ── Form elements ─────────────────────────────────────────────────────────── */
input[type="search"],
input[type="text"],
select {
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius-sm);
  padding: .55rem .85rem;
  font-size: .9rem;
  outline: none;
  transition: border-color var(--transition);
  width: 100%;
}
input[type="search"]:focus,
input[type="text"]:focus,
select:focus { border-color: var(--accent); }
select { cursor: pointer; }

button, .btn {
  background: var(--accent);
  color: #0b0f14;
  border: none;
  border-radius: var(--radius-sm);
  padding: .55rem 1.25rem;
  font-size: .9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity var(--transition), background var(--transition);
  white-space: nowrap;
}
button:hover, .btn:hover { opacity: .88; }
button.secondary {
  background: var(--border);
  color: var(--text);
}

/* ── Stats row ─────────────────────────────────────────────────────────────── */


/* ── Sources banner ────────────────────────────────────────────────────────── */
.sources-banner {
  display: flex;
  flex-wrap: wrap;
  gap: .4rem;
  align-items: center;
  margin: 1.25rem 0 2.5rem;
}
.badge {
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: .72rem;
  padding: .2rem .55rem;
  border-radius: 100px;
}
.sources-banner .note {
  color: var(--muted);
  font-size: .75rem;
  margin-left: .25rem;
}

/* ── Sections ──────────────────────────────────────────────────────────────── */
.section { margin-bottom: 3rem; }

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.1rem;
}
.section-header h2 { font-size: 1.2rem; font-weight: 700; }
.see-all { font-size: .85rem; color: var(--accent); }

/* ── Cards ─────────────────────────────────────────────────────────────────── */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
  transition: border-color var(--transition);
}
.card:hover { border-color: rgba(61, 214, 140, .35); }
.card a.card-link {
  display: block;
  color: inherit;
  text-decoration: none;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: .75rem;
  margin-bottom: .5rem;
}
.card-mfr { font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.card-title { font-size: 1.05rem; font-weight: 600; margin: .2rem 0; }
.card-codename { font-family: monospace; font-size: .82rem; color: var(--accent); }
.card-sub { font-size: .82rem; color: var(--muted); margin-top: .4rem; }

/* ── Device grid ───────────────────────────────────────────────────────────── */
.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: .85rem;
}

/* ── Skeleton loading ──────────────────────────────────────────────────────── */
.skeleton {
  background: linear-gradient(90deg, var(--card) 25%, var(--card2) 50%, var(--card) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius);
  min-height: 120px;
}
.skeleton * { opacity: 0; }
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── Filter bar ────────────────────────────────────────────────────────────── */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: .6rem;
  margin: 1.25rem 0;
}
.filter-bar input { flex: 1; min-width: 200px; }
.filter-bar select { min-width: 140px; width: auto; }

/* ── Results meta ──────────────────────────────────────────────────────────── */
.results-meta { font-size: .82rem; color: var(--muted); margin-bottom: .75rem; }

/* ── Page header ───────────────────────────────────────────────────────────── */
.page-header { margin-bottom: 1.25rem; }
.page-header h1 { font-size: 1.8rem; font-weight: 800; }
.page-sub { color: var(--muted); margin-top: .4rem; font-size: .9rem; }
.page-sub a { color: var(--accent); }

/* ── Badges / chips ────────────────────────────────────────────────────────── */
.chip {
  display: inline-block;
  font-size: .72rem;
  padding: .18rem .55rem;
  border-radius: 100px;
  font-weight: 600;
  border: 1px solid transparent;
}
.chip-green  { background: rgba(61,214,140,.12); color: var(--accent); border-color: rgba(61,214,140,.25); }
.chip-blue   { background: rgba(96,165,250,.12); color: var(--info);   border-color: rgba(96,165,250,.25); }
.chip-orange { background: rgba(251,191,36,.12); color: var(--warn);   border-color: rgba(251,191,36,.25); }
.chip-red    { background: rgba(248,113,113,.12);color: var(--danger); border-color: rgba(248,113,113,.25); }
.chip-gray   { background: var(--card2); color: var(--muted); border-color: var(--border); }

/* ── Tags row ──────────────────────────────────────────────────────────────── */
.tags { display: flex; flex-wrap: wrap; gap: .35rem; margin-top: .65rem; }

/* ── Sources tags ──────────────────────────────────────────────────────────── */
.source-tag { font-size: .7rem; color: var(--muted); font-family: monospace; }

/* ── Detail page ───────────────────────────────────────────────────────────── */
.breadcrumb { margin-bottom: 1.5rem; font-size: .85rem; color: var(--muted); }
.breadcrumb a { color: var(--accent); }

.detail-header {
  border: 1px solid var(--border);
  background: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
.detail-mfr { font-size: .75rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.detail-title { font-size: 2rem; font-weight: 800; margin: .35rem 0; }
.detail-codename { font-family: monospace; font-size: 1rem; color: var(--accent); }
.detail-note {
  margin-top: 1rem;
  padding: .7rem 1rem;
  background: rgba(251,191,36,.07);
  border: 1px solid rgba(251,191,36,.2);
  border-radius: var(--radius-sm);
  font-size: .85rem;
  color: rgba(251,191,36,.9);
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: .5rem;
  margin-top: 1.25rem;
}
.spec-item { display: flex; flex-direction: column; gap: .15rem; }
.spec-key  { font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.spec-val  { font-size: .88rem; }

.section-title { font-size: 1.1rem; font-weight: 700; margin: 1.75rem 0 .85rem; }

/* ── ROM list ──────────────────────────────────────────────────────────────── */
.rom-list { display: flex; flex-direction: column; gap: .75rem; }
.rom-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.25rem; }
.rom-header { display: flex; flex-wrap: wrap; align-items: center; gap: .4rem; margin-bottom: .45rem; }
.rom-name { font-weight: 700; font-size: 1.05rem; }
.rom-meta { font-size: .82rem; color: var(--muted); display: flex; flex-wrap: wrap; gap: .75rem; }
.rom-links { display: flex; flex-wrap: wrap; gap: .6rem; margin-top: .7rem; }
.rom-link { font-size: .82rem; color: var(--accent); }
.rom-note { font-size: .8rem; color: rgba(251,191,36,.8); margin-top: .5rem; border-left: 2px solid rgba(251,191,36,.3); padding-left: .6rem; }

/* ── Recovery card ─────────────────────────────────────────────────────────── */
.rec-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.25rem; }

/* ── Tools ─────────────────────────────────────────────────────────────────── */
.tools-section { margin-bottom: 2.5rem; }
.tools-section h2 { font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: .85rem; }
.tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: .85rem; }
.tool-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.1rem 1.25rem; }
.tool-header { display: flex; justify-content: space-between; align-items: flex-start; gap: .5rem; margin-bottom: .5rem; }
.tool-name { font-weight: 700; font-size: 1rem; }
.tool-desc { font-size: .83rem; color: var(--muted); margin-bottom: .75rem; }
.tool-version { font-size: .78rem; font-family: monospace; color: var(--accent); }
.tool-platform { font-size: .72rem; color: var(--muted); }
.tool-links { display: flex; gap: .75rem; flex-wrap: wrap; margin-top: .65rem; }
.tool-link { font-size: .82rem; }

/* ── Android version table ─────────────────────────────────────────────────── */
.table-wrap { overflow-x: auto; border-radius: var(--radius); border: 1px solid var(--border); margin-top: 1rem; }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
thead { background: var(--card); }
th { text-align: left; padding: .7rem 1rem; font-size: .75rem; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); border-bottom: 1px solid var(--border); }
td { padding: .65rem 1rem; border-bottom: 1px solid var(--border); }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--card2); }
.loading-cell { text-align: center; color: var(--muted); padding: 2rem; }

/* ── Pagination ────────────────────────────────────────────────────────────── */
.pagination {
  display: flex;
  gap: .4rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}
.page-btn {
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius-sm);
  padding: .35rem .75rem;
  font-size: .82rem;
  cursor: pointer;
}
.page-btn:hover { border-color: var(--accent); color: var(--accent); opacity: 1; }
.page-btn.active { background: var(--accent); color: #0b0f14; border-color: var(--accent); }

/* ── Version pills ─────────────────────────────────────────────────────────── */
.version-pills { display: flex; flex-wrap: wrap; gap: .5rem; }
.v-pill {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: .5rem .9rem;
  font-size: .82rem;
  transition: border-color var(--transition);
}
.v-pill:hover { border-color: var(--accent); }
.v-pill .v-num { font-weight: 700; color: var(--accent); }
.v-pill .v-name { color: var(--muted); font-size: .75rem; }
.pill { min-width: 80px; min-height: 48px; }

/* ── ROM families cards ────────────────────────────────────────────────────── */
.rom-families { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .75rem; }
.rom-family-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.1rem; }
.rom-family-name { font-weight: 700; font-size: .95rem; margin-bottom: .3rem; }
.rom-family-count { font-size: .78rem; color: var(--muted); }

/* ── Error / empty states ──────────────────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--muted);
}
.error-state {
  background: rgba(248,113,113,.07);
  border: 1px solid rgba(248,113,113,.2);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  color: var(--danger);
  font-size: .88rem;
}

/* ── Footer ────────────────────────────────────────────────────────────────── */
.site-footer {
  border-top: 1px solid var(--border);
  padding: 1.5rem 0;
  font-size: .8rem;
  color: var(--muted);
  text-align: center;
  margin-top: auto;
}
.footer-note { margin-top: .3rem; opacity: .7; }

/* ── Scrollbar ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(61,214,140,.3); }

/* ── Responsive ────────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .header-inner { height: auto; padding: .75rem 0; }
  nav { gap: .15rem; }
  .nav-link { font-size: .78rem; padding: .3rem .45rem; }
  .hero { padding: 2rem 0 1.25rem; }
  /* Stats grid — 2 columns, last card centered */

  .filter-bar { flex-direction: column; }
  .filter-bar select { width: 100%; }
  .detail-title { font-size: 1.5rem; }
}


.btn-github {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  background: var(--card2);
  border: 1.5px solid var(--border);
  color: var(--text);
  padding: .55rem 1.2rem;
  font-size: .9rem;
  border-radius: var(--radius);
  cursor: pointer;
  text-decoration: none;
  transition: border-color 180ms ease, color 180ms ease;
}
.btn-github:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* ── PWA Install button ──────────────────────────────────────────────────── */
.btn-install {
  background: transparent;
  border: 1.5px solid var(--accent);
  color: var(--accent);
  padding: .55rem 1.4rem;
  font-size: .9rem;
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background 180ms ease, color 180ms ease;
}
.btn-install:hover {
  background: var(--accent);
  color: #0b0f14;
  opacity: 1;
}

/* ── Tablet (641px – 1024px) ──────────────────────────────────────────── */
@media (max-width: 1024px) {
  .container { padding: 0 1.25rem; }
    .card-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ── Mobile (max 640px) — extended ───────────────────────────────────── */
@media (max-width: 640px) {
  .card-grid { grid-template-columns: 1fr; }
  .rom-card, .recovery-card, .tool-card { padding: .85rem 1rem; }
  .detail-header { padding: 1.25rem 0; }
  .detail-specs { grid-template-columns: 1fr; }
  table { font-size: .82rem; }
  th, td { padding: .5rem .6rem; }
  .guide-header { flex-direction: column; align-items: flex-start; gap: .5rem; }
  .type-tabs { gap: .3rem; }
  .type-tab { font-size: .75rem; padding: .25rem .65rem; }
  .page-header h1 { font-size: 1.5rem; }
  .btn:not(.btn-github):not(.btn-install) { width: 100%; text-align: center; }
}

/* ── Very small screens (max 380px) ──────────────────────────────────── */
@media (max-width: 380px) {
  .logo { font-size: 1.1rem; }
  .nav-link { font-size: .72rem; padding: .25rem .35rem; }

}

/* Improved placeholder contrast for accessibility */
input::placeholder,
select::placeholder,
textarea::placeholder {
  color: #7a8fa8;
  opacity: 1;
}

/* ── iOS Install Modal ────────────────────────────────────────────────────── */
/* Hero action buttons never go full width */

#ios-install-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
}

.ios-modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,.55);
  backdrop-filter: blur(2px);
}

.ios-modal-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--card);
  border-top: 1px solid var(--border);
  border-radius: 1.25rem 1.25rem 0 0;
  padding: 0 1.25rem 2rem;
  transform: translateY(100%);
  transition: transform 300ms cubic-bezier(.32,.72,0,1);
  max-width: 480px;
  margin: 0 auto;
}

.ios-modal-sheet.ios-modal-open {
  transform: translateY(0);
}

.ios-modal-handle {
  width: 36px;
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  margin: .85rem auto 1.25rem;
}

.ios-modal-header {
  display: flex;
  align-items: center;
  gap: .85rem;
  margin-bottom: 1.5rem;
}

.ios-modal-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  flex-shrink: 0;
}

.ios-modal-title {
  font-weight: 700;
  font-size: 1.05rem;
}

.ios-modal-sub {
  font-size: .8rem;
  color: var(--muted);
  margin-top: .2rem;
}

.ios-modal-close {
  margin-left: auto;
  background: var(--card2);
  border: none;
  color: var(--muted);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: .85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ios-modal-steps {
  display: flex;
  flex-direction: column;
  gap: 0;
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 1.25rem;
}

.ios-modal-divider {
  height: 1px;
  background: var(--border);
}

.ios-modal-step {
  display: flex;
  align-items: center;
  gap: .85rem;
  padding: .9rem 1rem;
}

.ios-step-num {
  width: 26px;
  height: 26px;
  background: var(--accent);
  color: #0b0f14;
  border-radius: 50%;
  font-weight: 700;
  font-size: .8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ios-step-content {
  flex: 1;
}

.ios-step-title {
  font-weight: 600;
  font-size: .9rem;
}

.ios-step-desc {
  font-size: .78rem;
  color: var(--muted);
  margin-top: .15rem;
}

.ios-step-icon {
  color: var(--accent);
  flex-shrink: 0;
}

.ios-modal-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .4rem;
  font-size: .8rem;
  color: var(--muted);
  animation: ios-bounce 1.5s ease-in-out infinite;
}

@keyframes ios-bounce {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(4px); }
}

/* ── Nav action buttons (Install + GitHub) in header ─────────────────────── */
.nav-actions {
  display: flex;
  align-items: center;
  gap: .5rem;
  flex-shrink: 0;
  /* On desktop: push to right end of header */
}
.btn-sm {
  display: inline-flex;
  align-items: center;
  gap: .3rem;
  padding: .4rem .85rem;
  font-size: .82rem;
  font-weight: 600;
  border-radius: 8px;
  white-space: nowrap;
  cursor: pointer;
  text-decoration: none;
  transition: opacity 150ms;
}
.btn-sm:hover { opacity: .85; }
.btn-sm svg { flex-shrink: 0; }
#pwa-install-wrap { display: none; } /* shown by JS when installable */

/* Mobile: nav-actions sit in header row, compact */
@media (max-width: 640px) {
  .nav-actions {
    gap: .3rem;
    flex-direction: row;        /* FORCE horizontal — never stack vertically */
    flex-wrap: nowrap;
    align-items: center;
    /* On mobile, nav is hidden; nav-actions stays visible in header row */
    order: 2; /* logo=0, nav-actions=2, hamburger=3 */
  }
  .nav-actions .btn-sm {
    padding: .35rem .55rem;
    font-size: .75rem;
    flex-shrink: 0;
  }
  #pwa-install-wrap {
    display: flex !important;   /* override inline display:block when JS shows it */
    align-items: center;
  }
  /* Hide text labels on very small screens, keep icons only */
  .btn-sm .btn-label { display: none; }
}
@media (min-width: 641px) {
  .btn-sm .btn-label { display: inline; }
}

/* ── Hamburger menu ───────────────────────────────────────────────────────── */
.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: .4rem;
  margin-left: auto;
}
.nav-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: transform 200ms ease, opacity 200ms ease;
}

@media (max-width: 640px) {
  .nav-toggle { display: flex; order: 3; }
  .nav-actions { order: 2; }
  .logo { order: 1; }

  #main-nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: .5rem 1rem 1rem;
    flex-direction: column;
    gap: .1rem;
    z-index: 200;
  }
  #main-nav.nav-open { display: flex; }
  .nav-link { font-size: .95rem; padding: .6rem .5rem; }

  /* Hamburger → X when open */
  .nav-toggle[aria-expanded="true"] span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  .nav-toggle[aria-expanded="true"] span:nth-child(2) {
    opacity: 0;
  }
  .nav-toggle[aria-expanded="true"] span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }

  .header-inner { position: relative; }
}



/* ── Scroll animations (IntersectionObserver pattern) ──────────────────────── */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  will-change: opacity, transform;
  -webkit-transform: translateY(24px);
  transition: opacity 600ms cubic-bezier(.22,1,.36,1),
              transform 600ms cubic-bezier(.22,1,.36,1),
              -webkit-transform 600ms cubic-bezier(.22,1,.36,1);
}
.reveal.visible {
  opacity: 1;
  transform: none;
  -webkit-transform: none;
}
/* Stagger delay for grid children */
.reveal-grid > * {
  opacity: 0;
  transform: translateY(18px);
  -webkit-transform: translateY(18px);
  will-change: opacity, transform;
  transition: opacity 500ms cubic-bezier(.22,1,.36,1),
              transform 500ms cubic-bezier(.22,1,.36,1),
              -webkit-transform 500ms cubic-bezier(.22,1,.36,1);
}
.reveal-grid.visible > *:nth-child(1) { transition-delay: 0ms;   opacity:1; transform:none; }
.reveal-grid.visible > *:nth-child(2) { transition-delay: 60ms;  opacity:1; transform:none; }
.reveal-grid.visible > *:nth-child(3) { transition-delay: 120ms; opacity:1; transform:none; }
.reveal-grid.visible > *:nth-child(4) { transition-delay: 180ms; opacity:1; transform:none; }
.reveal-grid.visible > *:nth-child(5) { transition-delay: 240ms; opacity:1; transform:none; }
.reveal-grid.visible > *:nth-child(6) { transition-delay: 300ms; opacity:1; transform:none; }
/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .reveal, .reveal-grid > * { transition: none; opacity: 1; transform: none; }
}

/* ── Enhanced Animations & Micro-interactions ───────────────────────────────── */

/* Page entrance animation */
@media (prefers-reduced-motion: no-preference) {
  main.container {
    animation: pageEnter 400ms cubic-bezier(.22,1,.36,1) both;
  }
  @keyframes pageEnter {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: none; }
  }

  /* Hero text stagger */
  .hero h1 {
    animation: heroSlideUp 550ms cubic-bezier(.22,1,.36,1) 80ms both;
  }
  .hero .hero-sub {
    animation: heroSlideUp 550ms cubic-bezier(.22,1,.36,1) 160ms both;
  }
  .hero .search-bar {
    animation: heroSlideUp 550ms cubic-bezier(.22,1,.36,1) 240ms both;
  }
  @keyframes heroSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: none; }
  }

  /* Card hover lift effect */
  .card:hover {
    transform: translateY(-3px) scale(1.01);
    border-color: var(--accent);
    box-shadow: 0 8px 32px rgba(61,214,140,.12);
    transition: transform 220ms cubic-bezier(.22,1,.36,1),
                border-color 220ms ease,
                box-shadow 220ms ease;
  }

  /* Nav link active underline animation */
  .nav-link::after {
    content: '';
    display: block;
    height: 2px;
    background: var(--accent);
    transform: scaleX(0);
    transition: transform 200ms ease;
    border-radius: 2px;
  }
  .nav-link.active::after,
  .nav-link:hover::after {
    transform: scaleX(1);
  }

  /* Button press effect */
  .btn:active, .btn-sm:active, button:active {
    transform: scale(0.97);
    transition: transform 80ms ease;
  }

  /* Search bar focus glow */
  input[type="search"]:focus,
  input[type="text"]:focus {
    box-shadow: 0 0 0 3px rgba(61,214,140,.18);
    border-color: var(--accent);
  }

  /* Stat value pop animation on count-up finish */
  .stat-value {
    transition: color 200ms ease;
  }

  /* Source badge hover */
  .badge {
    transition: background 180ms ease, color 180ms ease, transform 120ms ease;
  }
  .badge:hover {
    background: var(--accent);
    color: #0b0f14;
    transform: scale(1.05);
  }

  /* Section header slide in */
  .section-header {
    animation: fadeSlideLeft 500ms cubic-bezier(.22,1,.36,1) both;
  }
  @keyframes fadeSlideLeft {
    from { opacity: 0; transform: translateX(-12px); }
    to   { opacity: 1; transform: none; }
  }

  /* Chip bounce on hover */
  .chip:hover {
    transform: scale(1.08);
    transition: transform 150ms cubic-bezier(.34,1.56,.64,1);
  }

  /* Version pill hover */
  .v-pill {
    transition: transform 200ms cubic-bezier(.22,1,.36,1),
                background 180ms ease,
                border-color 180ms ease;
  }
  .v-pill:hover {
    transform: translateY(-2px);
    background: var(--card2);
    border-color: var(--accent);
  }

  /* ROM family card hover */
  .rom-family-card {
    transition: transform 200ms cubic-bezier(.22,1,.36,1),
                border-color 180ms ease,
                box-shadow 200ms ease;
  }
  .rom-family-card:hover {
    transform: translateY(-2px);
    border-color: var(--accent);
    box-shadow: 0 4px 16px rgba(61,214,140,.1);
  }

  /* Pagination button animation */
  .page-btn {
    transition: background 150ms ease, transform 120ms ease, color 150ms ease;
  }
  .page-btn:hover:not(.active) {
    transform: scale(1.07);
  }

  /* Logo brand pulse on hover */
  .logo:hover .accent {
    animation: logoPulse 600ms ease;
  }
  @keyframes logoPulse {
    0%   { color: var(--accent); }
    40%  { color: #7ef5b6; }
    100% { color: var(--accent); }
  }

  /* Skeleton shimmer improvement — more visible sweep */
  @keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
  }
  .skeleton {
    background-size: 400px 100%;
    animation: shimmer 1.4s ease-in-out infinite;
  }
}

/* Transition for card — always applied (not just reduced-motion) */
.card {
  transition: transform 220ms cubic-bezier(.22,1,.36,1),
              border-color 220ms ease,
              box-shadow 220ms ease;
}
"""
api_js = """/**
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

// ── Mac Safari install modal ─────────────────────────────────────────────────
function _showMacModal() {
  document.getElementById('mac-install-modal')?.remove();

  const modal = document.createElement('div');
  modal.id = 'mac-install-modal';
  modal.innerHTML = `
    <div class="ios-modal-backdrop" id="mac-modal-backdrop"></div>
    <div class="ios-modal-sheet" role="dialog" aria-modal="true" aria-label="Install Droidify on Mac">
      <div class="ios-modal-handle"></div>
      <div class="ios-modal-header">
        <img src="/icons/icon-192.png" class="ios-modal-icon" alt="Droidify icon" />
        <div>
          <div class="ios-modal-title">Install Droidify</div>
          <div class="ios-modal-sub">Add to your Dock for quick access</div>
        </div>
        <button class="ios-modal-close" id="mac-modal-close" aria-label="Close">✕</button>
      </div>
      <div class="ios-modal-steps">
        <div class="ios-modal-step">
          <div class="ios-step-num">1</div>
          <div class="ios-step-content">
            <div class="ios-step-title">Open the Share menu</div>
            <div class="ios-step-desc">Click the Share icon in the Safari toolbar (the box with an arrow)</div>
          </div>
          <div class="ios-step-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>
              <polyline points="16 6 12 2 8 6"/>
              <line x1="12" y1="2" x2="12" y2="15"/>
            </svg>
          </div>
        </div>
        <div class="ios-modal-divider"></div>
        <div class="ios-modal-step">
          <div class="ios-step-num">2</div>
          <div class="ios-step-content">
            <div class="ios-step-title">Click "Add to Dock"</div>
            <div class="ios-step-desc">Select "Add to Dock" from the share sheet options</div>
          </div>
          <div class="ios-step-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="3"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
          </div>
        </div>
        <div class="ios-modal-divider"></div>
        <div class="ios-modal-step">
          <div class="ios-step-num">3</div>
          <div class="ios-step-content">
            <div class="ios-step-title">Click "Add"</div>
            <div class="ios-step-desc">Confirm in the dialog to add Droidify to your Dock</div>
          </div>
          <div class="ios-step-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
        </div>
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
  document.getElementById('mac-modal-backdrop').addEventListener('click', close);
  document.getElementById('mac-modal-close').addEventListener('click', close);
}

"""
home_js = """/* home.js — Homepage logic */

document.getElementById('search-btn').addEventListener('click', () => {
  const q = document.getElementById('global-search').value.trim();
  if (q) window.location.href = `/devices.html?q=${encodeURIComponent(q)}`;
});
document.getElementById('global-search').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('search-btn').click();
});

async function loadHome() {
  const [devices, roms, recoveries, tools, versions] = await Promise.allSettled([
    api.devices({ limit: 50 }),
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
    // Randomize featured devices on every load
    const shuffled = [...devices.value.devices].sort(() => Math.random() - 0.5).slice(0, 6);
    devGrid.innerHTML = shuffled.map(deviceCardHTML).join('');
    if (window._reObserve) window._reObserve();
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
  // Re-trigger scroll reveal observer for dynamically loaded content
  requestAnimationFrame(() => { if (window._reObserve) window._reObserve(); });

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
  requestAnimationFrame(() => { if (window._reObserve) window._reObserve(); });
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
// Detect iOS major version for feature detection
const _iosMajor = (() => {
  const m = navigator.userAgent.match(/OS (\\d+)_/);
  return m ? parseInt(m[1], 10) : 0;
})();

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
"""
devices_js = """/* devices.js — Device listing page */

const LIMIT = 24;
let currentOffset = 0;
let currentParams = {};

// Read URL params on load
const urlP = new URLSearchParams(window.location.search);
if (urlP.get('q')) document.getElementById('device-search').value = urlP.get('q');
if (urlP.get('manufacturer')) document.getElementById('mfr-filter').value = urlP.get('manufacturer');

async function loadDevices(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;

  const grid = document.getElementById('device-grid');
  grid.innerHTML = Array(6).fill('<div class="card skeleton"></div>').join('');
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.devices({ ...params, limit: LIMIT, offset });
    const { devices, total } = data;

    document.getElementById('results-meta').textContent =
      `${total.toLocaleString()} device${total !== 1 ? 's' : ''}${params.q ? ` for "${params.q}"` : ''}`;

    if (!devices.length) {
      grid.innerHTML = '<div class="empty-state">No devices found. Try a different search.</div>';
      document.getElementById('pagination').innerHTML = '';
      return;
    }

    grid.innerHTML = devices.map(deviceCardHTML).join('');
    requestAnimationFrame(() => { if (window._reObserve) window._reObserve(); });

    renderPagination('pagination', total, offset, LIMIT, newOffset => {
      loadDevices(currentParams, newOffset);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Populate manufacturer filter dynamically on first load
    if (offset === 0 && !params.manufacturer) {
      await populateMfrFilter();
    }
  } catch (err) {
    grid.innerHTML = `<div class="error-state">Error: ${escHtml(err.message)}</div>`;
  }
}

async function populateMfrFilter() {
  // Load a larger sample to get unique manufacturers
  try {
    const data = await api.devices({ limit: 200 });
    const mfrs = [...new Set(data.devices.map(d => d.manufacturer).filter(Boolean))].sort();
    const sel  = document.getElementById('mfr-filter');
    const current = sel.value;
    mfrs.forEach(m => {
      const opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m;
      if (m === current) opt.selected = true;
      sel.appendChild(opt);
    });
  } catch (e) { /* ignore */ }
}

function getParams() {
  return {
    q:            document.getElementById('device-search').value.trim() || undefined,
    manufacturer: document.getElementById('mfr-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => {
  loadDevices(getParams(), 0);
});

document.getElementById('device-search').addEventListener('keydown', e => {
  if (e.key === 'Enter') loadDevices(getParams(), 0);
});

const debouncedSearch = debounce(() => loadDevices(getParams(), 0), 400);
document.getElementById('device-search').addEventListener('input', debouncedSearch);

document.getElementById('mfr-filter').addEventListener('change', () => loadDevices(getParams(), 0));

// Source filter (client-side since API doesn't expose it directly)
document.getElementById('source-filter').addEventListener('change', function() {
  // Will be applied on next load as a filter hint in params
  loadDevices(getParams(), 0);
});

// Initial load
loadDevices({ q: urlP.get('q') || undefined }, 0);
"""
device_detail_js = """/* device-detail.js — Device detail page */

const codename = new URLSearchParams(window.location.search).get('c');
if (!codename) window.location.href = '/devices.html';

document.title = `${codename} — Droidify`;

function romCardHTML(rom) {
  const android = rom.android_base ? `<span>Android ${escHtml(rom.android_base)}</span>` : '';
  const ver     = rom.version_label ? `<span>v${escHtml(rom.version_label)}</span>` : '';
  const maint   = rom.maintainer ? `<span>by ${escHtml(rom.maintainer)}</span>` : '';
  const src     = rom.source ? `<span class="source-tag">via ${escHtml(rom.source)}</span>` : '';

  const links = (rom.download_urls || []).map((u, i) =>
    `<a href="${escHtml(u)}" target="_blank" rel="noopener" class="rom-link">
      Download${(rom.download_urls?.length || 0) > 1 ? ' ' + (i+1) : ''} →
    </a>`
  ).join('');
  const srcLink = rom.source_url
    ? `<a href="${escHtml(rom.source_url)}" target="_blank" rel="noopener" class="rom-link">Source →</a>`
    : '';

  return `
    <div class="rom-card">
      <div class="rom-header">
        <span class="rom-name">${escHtml(rom.name)}</span>
        ${chip(rom.status === 'active' ? 'Active' : 'Discontinued', rom.status === 'active' ? 'green' : 'gray')}
        ${rom.is_official ? chip('Official', 'blue') : chip('Unofficial', 'gray')}
        ${chip('custom ROM', 'gray')}
      </div>
      <div class="rom-meta">${android}${ver}${maint}${src}</div>
      ${rom.description ? `<div class="card-sub" style="margin-top:.4rem">${escHtml(rom.description)}</div>` : ''}
      <div class="rom-links">${srcLink}${links}</div>
    </div>`;
}

function recoveryCardHTML(r) {
  const chip_color = r.recovery === 'OrangeFox' ? 'orange' : 'blue';
  return `
    <div class="rec-card" style="margin-bottom:.6rem">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.4rem">
        <span style="font-weight:600">${chip(r.recovery, chip_color)} ${escHtml(r.model_name || codename)}</span>
        ${r.status !== 'active' ? chip(r.status, 'gray') : ''}
      </div>
      <div style="margin-top:.5rem;display:flex;gap:.75rem;flex-wrap:wrap">
        ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Info →</a>` : ''}
        ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
      </div>
    </div>`;
}

async function loadDevice() {
  const content = document.getElementById('device-content');
  try {
    const d = await api.device(codename);
    document.title = `${d.model_name || codename} — Droidify`;

    const specRows = [
      ['SoC', d.soc],
      ['RAM', d.ram],
      ['CPU', d.cpu],
      ['GPU', d.gpu],
      ['Architecture', d.architecture],
      ['Released', d.released],
    ].filter(([, v]) => v).map(([k, v]) => `
      <div class="spec-item">
        <span class="spec-key">${escHtml(k)}</span>
        <span class="spec-val">${escHtml(v)}</span>
      </div>`).join('');

    const sourceTags = (d.sources || []).map(s => chip(s, 'gray')).join(' ');

    const roms = d.roms || [];
    const recoveries = d.recoveries || [];

    const limitedNote = !d.has_lineageos && roms.length < 2
      ? `<div class="detail-note">⚠ LIMITED ROM ECOSYSTEM — fewer than 2 ROM families found for this device across all indexed sources.</div>`
      : roms.length === 1
        ? `<div class="detail-note">⚠ ONLY ONE VERIFIED ROM FOUND — scraper discovery may be incomplete for this codename.</div>`
        : '';

    content.innerHTML = `
      <div class="detail-header">
        <div class="detail-mfr">${escHtml(d.manufacturer || '')}</div>
        <div class="detail-title">${escHtml(d.model_name || d.codename)}</div>
        <div class="detail-codename">${escHtml(d.codename)}</div>
        <div class="tags" style="margin-top:.65rem">
          ${sourceTags}
          ${d.has_lineageos ? chip('LineageOS', 'green') : ''}
          ${d.has_twrp ? chip('TWRP', 'blue') : ''}
          ${d.has_orangefox ? chip('OrangeFox', 'orange') : ''}
        </div>
        ${specRows ? `<div class="specs-grid" style="margin-top:1.1rem">${specRows}</div>` : ''}
        ${limitedNote}
      </div>

      <div class="section-title">ROMs (${roms.length} found)</div>
      ${roms.length
        ? `<div class="rom-list">${roms.map(romCardHTML).join('')}</div>`
        : '<div class="empty-state">No ROMs found in indexed sources for this device.</div>'}

      <div style="margin-top:1rem">
        <a href="/guides.html?c=${encodeURIComponent(codename)}&m=${encodeURIComponent(d.manufacturer||'')}"
           class="btn" style="display:inline-block">
          📖 View flashing &amp; root guides for ${escHtml(codename)} →
        </a>
      </div>

      ${recoveries.length ? `
        <div class="section-title">Recoveries (${recoveries.length})</div>
        <div>${recoveries.map(recoveryCardHTML).join('')}</div>
      ` : ''}

      <div style="margin-top:1.5rem;font-size:.78rem;color:var(--muted)">
        Data sourced live from: LineageOS · OrangeFox · TWRP · crDroid · GrapheneOS · DivestOS · CalyxOS · /e/OS.
        All sources free, no authentication required.
      </div>`;
  } catch (err) {
    content.innerHTML = `
      <div class="error-state">
        Device "<strong>${escHtml(codename)}</strong>" not found in any indexed source.<br>
        <a href="/devices.html" style="color:var(--accent)">← Back to devices</a>
      </div>`;
  }
}

loadDevice();
"""
roms_js = """/* roms.js — ROM listing page */
const LIMIT = 50;
let currentOffset = 0;
let currentParams = {};

async function loadRoms(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;
  const list = document.getElementById('rom-list');
  list.innerHTML = '<div class="skeleton" style="height:200px"></div>';
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.roms({ ...params, limit: LIMIT, offset });
    document.getElementById('results-meta').textContent =
      `${data.total.toLocaleString()} ROM entries found`;

    if (!data.roms.length) {
      list.innerHTML = '<div class="empty-state">No ROMs found.</div>';
      return;
    }

    list.innerHTML = `<div class="rom-list">${data.roms.map(r => `
      <div class="rom-card">
        <div class="rom-header">
          <span class="rom-name">${escHtml(r.name)}</span>
          ${chip('custom', 'gray')}
          ${r.is_official ? chip('official', 'blue') : ''}
        </div>
        <div class="rom-meta">
          ${r.codename ? `<span>Device: <a href="/device.html?c=${encodeURIComponent(r.codename)}">${escHtml(r.codename)}</a></span>` : ''}
          ${r.android_base ? `<span>Android ${escHtml(r.android_base)}</span>` : ''}
          ${r.version_label ? `<span>Branch: ${escHtml(r.version_label)}</span>` : ''}
          <span class="source-tag">via ${escHtml(r.source)}</span>
        </div>
        <div class="rom-links">
          ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Source →</a>` : ''}
          ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
        </div>
      </div>`).join('')}</div>`;

    renderPagination('pagination', data.total, offset, LIMIT, newOff => {
      loadRoms(currentParams, newOff);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  } catch (err) {
    list.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

function getParams() {
  return {
    q:            document.getElementById('rom-search').value.trim() || undefined,
    android_base: document.getElementById('android-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => loadRoms(getParams(), 0));
document.getElementById('rom-search').addEventListener('keydown', e => { if (e.key === 'Enter') loadRoms(getParams(), 0); });
document.getElementById('android-filter').addEventListener('change', () => loadRoms(getParams(), 0));
document.getElementById('rom-search').addEventListener('input', debounce(() => loadRoms(getParams(), 0), 400));

loadRoms({}, 0);
"""
recoveries_js = """/* recoveries.js — Recovery listing page */
const LIMIT = 50;
let currentOffset = 0;
let currentParams = {};

async function loadRecoveries(params = {}, offset = 0) {
  currentOffset = offset;
  currentParams = params;
  const grid = document.getElementById('rec-grid');
  grid.innerHTML = Array(6).fill('<div class="card skeleton"></div>').join('');
  document.getElementById('results-meta').textContent = 'Loading…';

  try {
    const data = await api.recoveries({ ...params, limit: LIMIT, offset });
    document.getElementById('results-meta').textContent =
      `${data.total.toLocaleString()} recovery entries (TWRP + OrangeFox)`;

    if (!data.recoveries.length) {
      grid.innerHTML = '<div class="empty-state">No recoveries found.</div>';
      return;
    }

    grid.innerHTML = data.recoveries.map(r => {
      const cc = r.recovery === 'OrangeFox' ? 'orange' : 'blue';
      return `<div class="card">
        <div class="card-top">
          <div>
            <div class="card-mfr">${escHtml(r.manufacturer || '')}</div>
            <div class="card-title">${escHtml(r.model_name || r.codename)}</div>
            <div class="card-codename">${escHtml(r.codename)}</div>
          </div>
          ${chip(r.recovery, cc)}
        </div>
        <div class="tags" style="margin-top:.5rem">
          ${chip(r.status === 'active' ? 'Active' : r.status, r.status === 'active' ? 'green' : 'gray')}
        </div>
        <div class="rom-links" style="margin-top:.65rem">
          ${r.source_url ? `<a href="${escHtml(r.source_url)}" target="_blank" rel="noopener" class="rom-link">Info →</a>` : ''}
          ${r.download_url ? `<a href="${escHtml(r.download_url)}" target="_blank" rel="noopener" class="rom-link">Download →</a>` : ''}
        </div>
      </div>`;
    }).join('');

    renderPagination('pagination', data.total, offset, LIMIT, newOff => {
      loadRecoveries(currentParams, newOff);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Populate manufacturer filter
    if (offset === 0 && !params.manufacturer) {
      const mfrs = [...new Set(data.recoveries.map(r => r.manufacturer).filter(Boolean))].sort();
      const sel = document.getElementById('mfr-filter');
      mfrs.forEach(m => {
        const o = document.createElement('option');
        o.value = m; o.textContent = m; sel.appendChild(o);
      });
    }
  } catch (err) {
    grid.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

function getParams() {
  return {
    q:            document.getElementById('rec-search').value.trim() || undefined,
    recovery:     document.getElementById('rec-filter').value || undefined,
    manufacturer: document.getElementById('mfr-filter').value || undefined,
  };
}

document.getElementById('search-btn').addEventListener('click', () => loadRecoveries(getParams(), 0));
document.getElementById('rec-search').addEventListener('keydown', e => { if (e.key === 'Enter') loadRecoveries(getParams(), 0); });
document.getElementById('rec-filter').addEventListener('change', () => loadRecoveries(getParams(), 0));
document.getElementById('mfr-filter').addEventListener('change', () => loadRecoveries(getParams(), 0));
document.getElementById('rec-search').addEventListener('input', debounce(() => loadRecoveries(getParams(), 0), 400));

loadRecoveries({}, 0);
"""
tools_js = """/* tools.js — Tools page */
async function loadTools(category, status) {
  const container = document.getElementById('tools-container');
  container.innerHTML = '<div class="skeleton" style="height:300px"></div>';

  try {
    const data = await api.tools({ category: category || undefined, status: status || undefined });
    const tools = data.tools;
    if (!tools.length) {
      container.innerHTML = '<div class="empty-state">No tools found.</div>';
      return;
    }

    // Group by category
    const groups = {};
    for (const t of tools) {
      (groups[t.category] ??= []).push(t);
    }
    const catOrder = ['root', 'xposed', 'flashing', 'recovery'];
    const sortedCats = [
      ...catOrder.filter(c => groups[c]),
      ...Object.keys(groups).filter(c => !catOrder.includes(c)),
    ];

    container.innerHTML = sortedCats.map(cat => `
      <div class="tools-section">
        <h2>${escHtml(cat)}</h2>
        <div class="tools-grid">
          ${groups[cat].map(t => {
            const status_chip = t.status === 'active'
              ? chip('Active', 'green')
              : chip('Discontinued', 'gray');
            const ver = t.latest_version
              ? `<span class="tool-version">v${escHtml(t.latest_version)}</span>`
              : '';
            const rel = t.release_date
              ? `<span class="tool-platform">${escHtml(t.release_date)}</span>`
              : '';
            const plat = t.platforms?.length
              ? `<span class="tool-platform">Platforms: ${escHtml(t.platforms.join(', '))}</span>`
              : '';
            const links = [
              t.official_url ? `<a href="${escHtml(t.official_url)}" target="_blank" rel="noopener" class="tool-link">Official →</a>` : '',
              ...(t.download_urls || []).slice(0,2).map(u =>
                `<a href="${escHtml(u)}" target="_blank" rel="noopener" class="tool-link">Download →</a>`
              ),
            ].filter(Boolean).join('');

            return `<div class="tool-card">
              <div class="tool-header">
                <span class="tool-name">${escHtml(t.name)}</span>
                ${status_chip}
              </div>
              <div class="tool-desc">${escHtml(t.description || '')}</div>
              <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.4rem">${ver}${rel}${plat}</div>
              <div class="tool-links">${links}</div>
              <div style="margin-top:.4rem;font-size:.72rem;color:var(--muted)">Source: ${escHtml(t.source || '')}</div>
            </div>`;
          }).join('')}
        </div>
      </div>`).join('');
  } catch (err) {
    container.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

document.getElementById('filter-btn').addEventListener('click', () => {
  loadTools(
    document.getElementById('cat-filter').value,
    document.getElementById('status-filter').value,
  );
});
document.getElementById('cat-filter').addEventListener('change', () =>
  loadTools(document.getElementById('cat-filter').value, document.getElementById('status-filter').value));

loadTools();
"""
android_js = """/* android.js — Android versions table with version codes and usage */
let allVersions = [];

async function loadVersions() {
  const tbody = document.getElementById('android-tbody');
  try {
    const data = await api.androidVersions();
    allVersions = data.versions;

    // Show data source
    const src = allVersions[0]?.source || 'unknown';
    const srcLabel = document.getElementById('source-label');
    if (srcLabel) {
      const srcMap = {
        'apilevels.com': '✓ Source: apilevels.com (live)',
        'wikipedia':     '✓ Source: Wikipedia (fallback)',
        'static_fallback': '⚠ Source: static fallback (both live sources failed)',
      };
      srcLabel.textContent = srcMap[src] || `Source: ${src}`;
      srcLabel.style.color = src === 'apilevels.com' ? 'var(--accent)' :
                             src === 'wikipedia' ? 'var(--info)' : 'var(--warn)';
    }

    renderTable(allVersions);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="error-state">${escHtml(err.message)}</td></tr>`;
  }
}

function usageBar(pct) {
  if (pct == null) return '<span style="color:var(--muted)">—</span>';
  const w = Math.min(pct, 100);
  const color = pct > 50 ? 'var(--accent)' : pct > 20 ? 'var(--info)' : 'var(--muted)';
  return `
    <div style="display:flex;align-items:center;gap:.4rem">
      <div style="width:60px;height:6px;background:var(--border);border-radius:3px;overflow:hidden">
        <div style="width:${w}%;height:100%;background:${color};border-radius:3px"></div>
      </div>
      <span style="font-size:.78rem">${pct}%</span>
    </div>`;
}

function renderTable(versions) {
  const tbody = document.getElementById('android-tbody');
  if (!versions.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">No versions match the filter.</td></tr>';
    return;
  }
  tbody.innerHTML = [...versions].reverse().map(v => {
    const statusChip =
      v.status === 'active'  ? chip('Active', 'green') :
      v.status === 'partial' ? chip('Preview', 'orange') :
                               chip('EOL', 'gray');

    const betaBadge = v.is_beta ? ' <sup style="font-size:.65rem;color:var(--warn)">BETA</sup>' : '';

    const vcode = v.version_code
      ? `<code style="font-size:.78rem;color:var(--accent)">${escHtml(v.version_code)}</code>`
      : '<span style="color:var(--muted)">—</span>';

    return `<tr>
      <td><strong>Android ${escHtml(v.version_number)}</strong>${betaBadge}</td>
      <td>${escHtml(v.codename || '—')}</td>
      <td><span style="font-family:monospace;color:var(--info)">${v.api_level}</span></td>
      <td>${vcode}</td>
      <td>${v.release_year || '—'}</td>
      <td>${usageBar(v.cumulative_usage)}</td>
      <td>${statusChip}</td>
    </tr>`;
  }).join('');
}

document.getElementById('filter-btn').addEventListener('click', () => {
  const status = document.getElementById('status-filter').value;
  const minApi = parseInt(document.getElementById('api-min').value) || 0;
  let filtered = allVersions;
  if (status) filtered = filtered.filter(v => v.status === status);
  if (minApi) filtered = filtered.filter(v => v.api_level >= minApi);
  renderTable(filtered);
});

document.getElementById('status-filter').addEventListener('change',
  () => document.getElementById('filter-btn').click());

loadVersions();
"""
guides_js = """/* guides.js — Guides page */

let allGuides = [];
let activeType = '';

const TYPE_COLORS = {
    'install':           'green',
    'upgrade':           'blue',
    'root':              'orange',
    'bootloader-unlock': 'red',
    'recovery':          'blue',
    'backup':            'gray',
    'unbrick':           'red',
};

const TYPE_ICONS = {
    'install':           '📦',
    'upgrade':           '⬆️',
    'root':              '🔓',
    'bootloader-unlock': '🔑',
    'recovery':          '🛠',
    'backup':            '💾',
    'unbrick':           '🆘',
};

function guideCardHTML(guide, index) {
    const icon      = TYPE_ICONS[guide.type] || '📄';
    const chipColor = TYPE_COLORS[guide.type] || 'gray';
    const sections  = guide.sections || [];
    const hasLive   = ['lineageos_wiki','grapheneos_docs'].includes(guide.data_source);

    // Build sections HTML
    let sectionsHTML = '';
    for (const sec of sections) {
        if (!sec.steps || !sec.steps.length) continue;
        sectionsHTML += `<div class="guide-section">
            <h3>${escHtml(sec.title)}</h3>
            <ol class="guide-steps">
                ${sec.steps.map(step => {
                    const isNote = step.startsWith('⚠');
                    return `<li class="${isNote ? 'note-item' : ''}">${escHtml(step)}</li>`;
                }).join('')}
            </ol>
        </div>`;
    }

    const note = guide.notes
        ? `<div class="guide-note">${escHtml(guide.notes)}</div>`
        : '';

    const sourceLink = guide.source_url
        ? `<a href="${escHtml(guide.source_url)}" target="_blank" rel="noopener" class="rom-link" style="margin-top:.85rem;display:inline-block">
             Full guide on ${escHtml(guide.source)} →
           </a>`
        : '';

    const liveBadge = hasLive
        ? chip('Live from wiki', 'green')
        : chip('Compiled guide', 'gray');

    return `
        <div class="guide-card">
            <div class="guide-header" onclick="toggleGuide(${index})">
                <div>
                    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.3rem">
                        <span style="font-size:1.2rem">${icon}</span>
                        <span class="guide-title">${escHtml(guide.title)}</span>
                        ${chip(guide.type, chipColor)}
                        ${liveBadge}
                    </div>
                    <div class="guide-source">Source: ${escHtml(guide.source)}</div>
                </div>
                <span class="guide-toggle" id="toggle-${index}">▼</span>
            </div>
            <div class="guide-body" id="body-${index}">
                ${note}
                ${sectionsHTML || `<ol class="guide-steps">${(guide.steps || []).map(s =>
                    `<li class="${s.startsWith('⚠') ? 'note-item' : ''}">${escHtml(s)}</li>`
                ).join('')}</ol>`}
                ${sourceLink}
            </div>
        </div>`;
}

window.toggleGuide = function(index) {
    const body   = document.getElementById(`body-${index}`);
    const toggle = document.getElementById(`toggle-${index}`);
    if (!body) return;
    const isOpen = body.classList.contains('open');
    body.classList.toggle('open', !isOpen);
    toggle.classList.toggle('open', !isOpen);
};

function renderGuides(guides) {
    const container = document.getElementById('guides-container');
    const filtered  = activeType ? guides.filter(g => g.type === activeType) : guides;

    if (!filtered.length) {
        container.innerHTML = '<div class="empty-state">No guides found for this filter.</div>';
        return;
    }

    container.innerHTML = filtered.map((g, i) => guideCardHTML(g, i)).join('');
}

async function loadGuides(codename, manufacturer) {
    const container = document.getElementById('guides-container');
    const tabs      = document.getElementById('type-tabs');

    container.innerHTML = '<div class="skeleton" style="height:200px;margin-bottom:1rem"></div>'
                        + '<div class="skeleton" style="height:200px;margin-bottom:1rem"></div>'
                        + '<div class="skeleton" style="height:200px"></div>';

    try {
        const params = codename
            ? `/${encodeURIComponent(codename)}${manufacturer ? '?manufacturer=' + encodeURIComponent(manufacturer) : ''}`
            : '';

        const data = codename
            ? await api.get(`/guides/${encodeURIComponent(codename)}`, { manufacturer: manufacturer || undefined })
            : await api.get('/guides');

        allGuides = data.guides || [];
        tabs.style.display = allGuides.length ? 'flex' : 'none';
        renderGuides(allGuides);

    } catch (err) {
        container.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
    }
}

// Type tab filter
document.getElementById('type-tabs').addEventListener('click', e => {
    const tab = e.target.closest('.type-tab');
    if (!tab) return;
    document.querySelectorAll('.type-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    activeType = tab.dataset.type;
    renderGuides(allGuides);
});

// Load device-specific guides
document.getElementById('load-btn').addEventListener('click', () => {
    const codename = document.getElementById('codename-input').value.trim();
    const mfr      = document.getElementById('mfr-select').value;
    if (!codename) {
        loadGuides(null, null);  // load universal guides
    } else {
        loadGuides(codename, mfr);
    }
});

document.getElementById('codename-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('load-btn').click();
});

// Load universal guides on page load
loadGuides(null, null);

// Also check if we came from device page with ?c=codename
const urlParams = new URLSearchParams(window.location.search);
const preloadCodename = urlParams.get('c');
const preloadMfr      = urlParams.get('m');
if (preloadCodename) {
    document.getElementById('codename-input').value = preloadCodename;
    if (preloadMfr) document.getElementById('mfr-select').value = preloadMfr;
    loadGuides(preloadCodename, preloadMfr);
}
"""
manifest_json = """{
  "id": "droidify-android-rom-index",
  "name": "Droidify — Android ROM & Device Index",
  "short_name": "Droidify",
  "description": "Live Android ROM, device, recovery and tool indexer. Browse 1000+ ROMs, 1100+ devices. No signin. No payment.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "display_override": ["standalone", "minimal-ui", "browser"],
  "background_color": "#0b0f14",
  "theme_color": "#3dd68c",
  "orientation": "portrait-primary",
  "lang": "en",
  "dir": "ltr",
  "categories": ["utilities", "technology", "productivity"],
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/favicon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any"
    }
  ],
  "shortcuts": [
    {
      "name": "Devices",
      "short_name": "Devices",
      "description": "Browse Android devices",
      "url": "/devices.html",
      "icons": [{ "src": "/icons/icon-192.png", "sizes": "192x192" }]
    },
    {
      "name": "ROMs",
      "short_name": "ROMs",
      "description": "Browse custom ROMs",
      "url": "/roms.html",
      "icons": [{ "src": "/icons/icon-192.png", "sizes": "192x192" }]
    },
    {
      "name": "Guides",
      "short_name": "Guides",
      "description": "Flashing and rooting guides",
      "url": "/guides.html",
      "icons": [{ "src": "/icons/icon-192.png", "sizes": "192x192" }]
    },
    {
      "name": "Recoveries",
      "short_name": "TWRP",
      "description": "Browse custom recoveries",
      "url": "/recoveries.html",
      "icons": [{ "src": "/icons/icon-192.png", "sizes": "192x192" }]
    }
  ],
  "screenshots": [
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Droidify home screen"
    }
  ],
  "prefer_related_applications": false
}
"""
sw_js = """const STATIC_CACHE = 'droidify-static-v5';
const API_CACHE    = 'droidify-api-v3';

const PRECACHE_URLS = [
  '/','/index.html','/devices.html','/device.html','/roms.html',
  '/recoveries.html','/tools.html','/android.html','/guides.html','/404.html',
  '/css/style.css','/js/api.js','/js/home.js','/js/devices.js',
  '/js/device-detail.js','/js/roms.js','/js/recoveries.js','/js/tools.js',
  '/js/android.js','/js/guides.js','/favicon.svg','/manifest.json',
  '/icons/icon-192.png','/icons/icon-512.png',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  const keep = [STATIC_CACHE, API_CACHE];
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => !keep.includes(k)).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET') return;

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request, API_CACHE));
    return;
  }
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(request) || caches.match('/index.html'))
    );
    return;
  }
  event.respondWith(cacheFirst(request, STATIC_CACHE));
});

async function cacheFirst(req, cacheName) {
  const cached = await caches.match(req);
  if (cached) return cached;
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(cacheName)).put(req, res.clone());
    return res;
  } catch { return new Response('offline', { status: 503 }); }
}

async function networkFirst(req, cacheName) {
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(cacheName)).put(req, res.clone());
    return res;
  } catch {
    return await caches.match(req) ||
      new Response(JSON.stringify({ error: 'offline' }), {
        status: 503, headers: { 'Content-Type': 'application/json' }
      });
  }
}

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});
"""
robots_txt = """User-agent: *
Allow: /

# API endpoints — allow indexing the docs page but not raw JSON
Disallow: /api/

Sitemap: https://your-domain.com/sitemap.xml
"""
favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#0b0f14"/>
  <!-- Android robot head -->
  <circle cx="50" cy="40" r="22" fill="#3dd68c"/>
  <!-- Eyes -->
  <circle cx="42" cy="38" r="3.5" fill="#0b0f14"/>
  <circle cx="58" cy="38" r="3.5" fill="#0b0f14"/>
  <!-- Antenna -->
  <line x1="43" y1="19" x2="37" y2="11" stroke="#3dd68c" stroke-width="3" stroke-linecap="round"/>
  <line x1="57" y1="19" x2="63" y2="11" stroke="#3dd68c" stroke-width="3" stroke-linecap="round"/>
  <circle cx="37" cy="10" r="2.5" fill="#3dd68c"/>
  <circle cx="63" cy="10" r="2.5" fill="#3dd68c"/>
  <!-- Body -->
  <rect x="30" y="62" width="40" height="24" rx="6" fill="#3dd68c"/>
  <!-- Arms -->
  <rect x="16" y="62" width="10" height="20" rx="5" fill="#3dd68c"/>
  <rect x="74" y="62" width="10" height="20" rx="5" fill="#3dd68c"/>
  <!-- Legs -->
  <rect x="34" y="86" width="10" height="10" rx="5" fill="#3dd68c"/>
  <rect x="56" y="86" width="10" height="10" rx="5" fill="#3dd68c"/>
</svg>
"""
icon_192_b64 = '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'
icon_512_b64 = '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fsX5C/jiJTqMuvefZGoBLzu++M9RrogfASsXTTocz8YG8c+tkx3BEGUnmrdNaeX5xXv9kchsrooAIqeZtz4mMM8Z56jwSfbYStkJWAAM4muplB3BEGadJLwzK4t29TGRVaovNm8djq+lyrSxrRSYVy87gmOwABjE22j9bnpm8Lebszd42AHTj0RmKzuhBe4qEx7OIwQ8jRHjx5WAdwIYhwXACIqA4i/uxTUHuMr9UDzGX4cMnWDe2gIix1AEwifPMn5Yn9sx62/c1SHeSWQQZ/xGSKb4PY76hVSCXsPHDBzDaTuiyTCjAKgBZ3xAAfbfcq0U+d0MdsECYAAzPjHLpHiNfXEJtwpPgzOmH4nMZsYqd+F21s6bis9Z/39kYQEg03mbKxwz/UhkNm992JRZOKK34lmZTCfzuedERUcI+FudsWKf7I0FgEynmrzFKZHTuMr9siNQCWABINMpAU5nEk2FGirubcWpOLAAkOkUD3/NiKaCi9zICjwzk/kcdIskkSX4miELsAAQERGVIBYAIiKiEsQCQEREVIJYAIiIiEoQCwAREVEJYgEgIiIqQSwAREREJYgFgIiIqASxABAREZUgFgAiIqISxAJARERUglgAiIiIShALABERUQliASAiIipBLABEREQliAWAiIioBLEAEBERlSAWACIiohLEAkBERFSCWACIiIhKEAsAERFRCWIBICIiKkEsAERERCWIBYCIiKgEsQAQERGVIBYAIiKiEsQCQEREVIJYAIiIiEoQCwAREVEJYgEgIiIqQSwAREREJYgFgIiIqASxABAREZUgFgAiIqISxAJARERUglgAiIiIShALABERUQliASAiIipBLABEREQliAWAiIioBLEAEBERlSAWACIiohLEAkBERFSCWACIiIhKEAuAAfScJjuCofS8s/7/EJU6PZeXHcFQTjvnysICYIB8PA3ouuwYhsnH07IjEJGBtAlnvaa1REZ2BEdgATCCpiM/npKdwhiaDi2VlZ2CiAyUT+egpXOyYxhCS+c4S2kQFgCDpLqGZUcwRGZoHNCcM5tBRAB03THnqGxfTHYEx2ABMEhie7/sCIZI7x6RHYGITJDsGJAdwRDJvc4oMnbAAmCQ8Y17ZEcwRHLXkOwIRGSC8Q27ZUcwRGonz1FGYQEwSOyFLkestJ140RlFhojeLPbcLkdc3pt4iecoo7AAGESLpxFdu1N2jILoeQ3jfHEROVJuNIHYC12yYxREy+Qx8fJe2TEcgwXAQMMPbJYdoSDjG3Y7524GInqb4Qc2yY5QkNj6nY65m8EOWAAMFFu3C+k9xbuIbuSRV2VHICITjT2zA5n+4l1FP/Iwz1FGYgEwkJ7X0HfHOtkxpiU3msDY01tlxyAiE+nZPPp+tV52jGnJDo4jtrZDdgxHYQEw2MijryLVOSg7xpQN/P4FTq0RlYCRBzch3T0qO8aU9f/2OWiZ4l9obScsAAbT8xr2/PvjRbU1cG40gcF7XpQdg4gsoGXy2Hvr47JjTEl2cBxD974sO4bjsACYYOKlPRh+6BXZMSat5ydPI++wvcKJ6PBi63dh9PHXZceYtO4fPMkZShOwAJhk73efQHqv/afZJl7ag+E/b5Edg4gstuffHkWmLyo7xlHF1u/C6JNcn2QGBUDxzFUXES2ZQedX77V1a82NJdF10wPmX65wwOYjRJay4BJifiKFrhvvh5a273X17NAEur7xkOwYTqUrAPjoN5Mktvej68b7bfkGqOc1dH3tfmQGx00/Vj7JR3cSTUU+ac1peeKVHuz+14dsuWZJz+bReeP9yI3EZUdxqqwCgDu/mGjsme3Y+70n7PUC03Xs+fYjiK3vtORwXF9ANDVWPu9+9LHX0PPjv1h2vEnRdHTd8hC3/TVXWgHAs7PJBv+wEXtutcmdAbqO7u8/ieEHrdu1MDs0YdmxiJzA6tLcf+dz6PnRU5Ye83D0vIa9//4YRh97TXYUp8u4ACRlpygFQ/e8CG0ijZlfeicUryolg57LY/ctf8bIo9buppXePQw9r0GoXHNKNBmZfdYvzuu/83nkYinM/MJ5EG455ygtk0fXzfdj7OltUo5fYtIKgDHZKUrFyKOvYscnf4usBdfd3yozEMP2T95p+Zs/sP9Fnd5bvFskE1lJS+csWZtzKMMPbsaOf/pfZCVcd0/vi2LHx37DN3+LCCCtenzBywC0yw5TKrKD4xh+aAu89RH422ssOebok1ux6/o/SH1OgW92DYLHNEg7PlGxSHUOYehPL0k7fqY/hpGHt8DbXAFfa5X5B9R1jDz6KnZ94Y9I7+PnUQt1qR5/4FwAi2UnKSV6Ooexp7chub0fgXn1cEX8phwn1TWErpseQP+v10u/HVFxqah4x3ypGYiKwdjTWxFbt0tqBi2VxegTryPZOYTAMfVwhX2mHCfZMYjOG+/DwO9egJ6x7y3TziS2uKCjX3aMUjX27A5E1+1C1eolqLtyObwzKgwZN7G9H/2/WofRp7fZ5hbE2Ibd0NJ5aesfiIrF+Iv2Wfk+9tRWRJ/dgep3LUXtFcvhbSo3ZNz4673ov2Mdxp7ZYY/F0SVJHxbB8urPQsd3ZUcpeYpA+KQ2VJ63AJGV7VDLpta407tHEF3bgeE/b0GyY8CkkIVpvXk1Ks87VnYMItvS8xpeufBHyEVtuDZbEYisbEfluQsQXjELasg7pW9PdQ0huqYDIw+/iuSu4ntgmtPoELe5dIEOwQImn6Yjtm4XYut2QagKAgsbEJhTD//sWnhqy6CWeaH4PdCzeeTHU8iNJZHaM4xU1zAmNnVLWVg4VcMPbmYBIDqC8Q277fnmDwCajuiaDkTXdEC4VAQXNMA/t+7/zlGhv5+jMjnkJ9LIjiSQ3jOMZNcw4pu7eTuwzShCH3SpOWzXeHeWreh5DfFNPYhv6pEdxVDjG3cj1TkIX5s1ix+Jio2Mu3SmQ8/lMbGpGxObumVHoWnSdPQp4+NDnQC4+oLMp+vovX2t7BREtpSfSCPKW+DIIkJXOhUAGQDW7AlLJW/sqW1IdQ3JjkFkO4P3vIh8io9mIWsoutZ1YPL/ZalJqGToeQ3d339SdgwiW9HSOQz8/gXZMah06OPjod1/LwD6RrlZqJTEnuvE2F841Ul0wMD/Po/caEJ2DCod+4CulAIAAmD1JEt1f+9J5Mf5IEqidG8Ufb/k2hiyVAcAKADgVrSNADSpcaikZAZi2P3tR2THIJKu57tPSN+pk0qM0DcBfy8Ao6OjUQhslZuISs3YU1sxdN8m2TGIpBm89yWMrdkhOwaVGF0XW4C/FwAA0CGelheHStXeWx/D+MbdsmMQWS65cxA9XBBLEui6vhl4QwFQdBYAsp6ezaPzK/civXdUdhQiy2SH49j1xXs49U8yaCGv8irwhgIgtORfwHUAJEEumkTHZ3+PTF9UdhQi02nxNHZ+7i6ke/joW5Jix+Dg4ATwhgIwPj4+DIAXZEmKdM8YdnziTqR7WQLIubR4Gh3X34PEdj6ElWTR/3bgn970FAAh8ID1YYj2S/dGseNjv0Wyg08KI+fJDsex7eO/xcRL9nncL5Ugoaw58I9vKgCajvusT0P0fzIDMWz76K8x9sx22VGIDJPY2oftH/0Vkjvs+ahuKh2qhoMFQLz1L4ORqk5AtFqYh+jtFIH6D5yMhutWQbhV2WmIpm3w7o3o+fFT0DJ52VGIhuLRoVoAOgC87czq9odmC+BEy2MRvZEOTGzqRvTZDoQWN8NdGZSdiGhK0ntH0XXz/Ri8eyP0vC47DhF06H/OppN3Hfj3txUAry+QAHCNlaGIDic3EsfwA5uRG00gOL8Bit8tOxLREeUn0uj/5Vp0fe0BpHaPyI5D9AbKd7PpxEsH/u1tlwAAiGCkahcvA5DdqCEvaq88ETWXHQdXRUB2HKI3yY0mMHDXBgz+YSPyE2nZcYjeDgOGlwAAEn9JREFUStdc+ozk8HDPgT84VAFAMFLzr4D+JetyEU2e4lFRfvaxqL54EYKLmyFU5ejfRGQCLZ1HbF0HRh5+FdF1O6FneZ2fbGtzPDq05I1/cMgCEApVzddV8Zo1mYimzxXxI7xyNsLLZ8I/pw6+1ioIFxcNkjmyQxNI7R5GfMs+jG/cjfjmbu7mR0VCfCceHfyXN/3J4b40GKl+HsBy0zMRGUi4VXjqwlDLfFBDXqhlvkl9n7s6BHdtGdzVIbjCfiheFxSPCi2Th57OITeeQqY/hkxvFLlo0uT/FzRVwqXA0xCBu7oM7qoAXEEfhFeFUBVoyRzy6QxyIwlk+qLI9MUm/aatTaShJTPIxzNI98egxTm1T8VJ05RTkuMDb3ru9GELQKC85iNC139ufiwi6ykeFeFTZqP89HkoO2Em3NWhSX9veu8oxp7djrEntyH+2j4TU9KRuGvKUHnOsQivnIXgwiYoXtekvk/Pa5h4eS+iz+7AyOOvIzcSNzkpkXR749GhFvz99r8DDlsA0NzsD46nugFUmhyMyDKe2jBq338iqi5YOOnZgSOJv7YPA7/fgNEnXgc03uplhbJlrah7/0koW95S8PoPLZPH2JOvof/O57kDJTnZrfHo0Off+oeHLwAAguHqWyHwOfMyEVnDVe5H4z+ejqoLF5mysVByxwC6f/QUxl/oMnxs2i+4pAnN/3Q2ggsajR9c0zH88Bbs+69nkB0cN358Iol0XT8xERt+4a1/fsQCEA7XzMkLfdvRvo7IzqovXoymT50JNew3/VjDf34F3d97greBGUgt86H502eh6sJFgDD3VKTF09j7/Scx/OBmU49DZKHOeHSoHW+Z/gcOsRHQG6XTiRGvN3A8BOaZFo3IJGrIi7abV6Pu6hVQvNZsIBSYU4fK8xYg/koPP0kaILigEbN/eCXKTmgx/c0fAITHhfLT5sA/txbRdbt4Wx8VPV3HD7LpxF8O9XdHnQtVvf5OIcR1hqciMpG3MYK5P/0AQkuaLT+2GvKi8ryFyPRGkdzJ68rTVXnBQrR/+zK4IubP3LyVr6UK5afORmx9J/LjKcuPT2QQTVNyH86lUod8zvpRC0AunezxeANnQ6DF+GxExvO312DOT66CpyEiLYNwKSg/fS7y8QziW3inwFTVvncZZn7hPKmbPLkqgqh4x3yMr+9EbjQhLQdRAR5ORkduO9xfTmo1lNsbGBACVxmXicgc3uYKzLntKrirJn9bn2mEQPjkWdCSWcRf6Tn61xMAoPqy4zHjn8+xZMr/aFS/BxVnHYPY+l0sAVR0NKF/MZdKbj3c30+qAGTTiQ6PL3AJgHrDkhEZzFURwNzb3g9PXVh2lDcJn9iK9L4okh18FvzRlJ8xD61fvdAWb/4HKH43yk+dg7EntiKfyMiOQzQ5OvYlosOfAKAd7ksmO7+m6xpuMCYVkQkUgdabLoa3qVx2krcTAi1fugChpTNkJ7E174wKtN5wIaDY583/AHdNGdpvvRyqj0+jpCIh9B8CyB7pSyZ9Q3Q2k9ju9vvPFRA8i5Ht1H3gZNS86zjZMQ5LqArCJ8/CyMOvQEtx7/i3Ei4Vs3/wXnjq5a3bOBp3VRDumjJEn9khOwrR0cRVPfvBdDp9xH3Lp7TCRhXKvxz9q4is5WkqR8O1q2THOCp3dQgtX7lQdgxbqr1yOQJz62THOKqqCxeh4h3zZccgOjId/x2LxUaO9mVTKgDjo4PPAuLx6aciMt6Mz54z6X3gZYusms03kLfw1JSh/tpTZMeYtBmfO8eQbaSJTJLLK64fTuYLp3yPjcjnPwOAc5hkC8GFTYic0i47xpQ0f/osKAGP7Bi2UffBk4vq2rqrIoCmfzxNdgyiQ9P136TG+rom86VTLgATEyOv6cDPphyKyAT1H1ohO8KUuWvKUHvFMtkxbMFVGUTV6iWyY0xZ1aVL4W2ukB2D6K2yeeH6xmS/eFq7bLj0zFcBMTyd7yUyiqc+gsjK4vr0f0Dd+5ZzFgD7n9NQLJdv3kioCuqvWSk7BtGbCOD2VLR/12S/floFIBaLjUBg0i2DyAyV5y+w5S1jk6GG/fsfbvP/27vXGLnK+47j3+fM7OzO7O7Mem/GxgFC17hQVCVAnTaU5toQEqJUCNJIoOQFtIFEKeSCSJQmRQSklBdRExWUYNILOFLAEQjUhCWQEGoKDjYX29iAr+u18V7mfr+e8/SF7ZRGNrZ3zsxzzpn/5/15nt/6rDy/Ofuc5+lxox+/0HSEJRu9/ALCo4OmYwhxTN227LtO54Il77NZziXvAV5d6vVCtMvvi+nGffjo203RqUkGzhkzHWPJVDjE2BX+LTAiYJT+cTWbnT2dS9rZaLul4e8AOS5LdF14WYzoueOmY7QlOjVJdGrCdAxjhi/x//Eifn6CIQIlY9mNO073orZO2qjkU1vQnNLrBkK4afiiszy1XexSxf/Cn2sY3DB8sf8LQHRqgsjEsOkYoscprb9dLBZPe11e20dtlYci/wjsb3ccIU5HdGrSdARXxNeeYzqCMUF5+jHcw/dQeIBiZ6mQvm8pl7Z/1ubhwxVwvgDotscS4hQNnO3fvx2/nR92v+sEqz9MZNJbhzYtVbRH76HwCK1vZol787hy2HY5n3lKK3WPG2MJcSoiK7y7Z/zpCMWj9I174OjiLousSPj2DY4/5Pe1KMLHFA+W8+mnl3q5KwUAoJIbvBXNDrfGE+KdhAb7TUdwTV8PvkoWigXo/o313v0TXqDSqhX6ejsjuFYAYKamFZ/jJMcPCuEGK+qfrWNPphf3lQ/U/RvqvfsnPEA7t5RKC4vtDOFiAYBKPvWyRt3u5phCHI92grPkJEg/y6kK0s+sg/OjCP+YLhfS69sdxNUCAFDJJ78HTLs9rhBvZ5dqpiO4xqnUTUfoOrl/QixZ1rHsL7gxkOsFAHBCunEtcKADYwsBQHOxZDqCa1ql3vsAaaYCdP+KvXf/hDkKdePp7vh3Ip0oABQKhYyjnc8CjU6ML0R1X9J0BFfolk1zoWg6Rte1shWambLpGK5oHMqajiB6hIJ1pXzyYbfG60gBAKgWMptQ3Nap8UVvq7wxZzqCKxpv5dGt3txNu/L6vOkIrqgfzJiOIHrDrtJA6CtuDtixAgBQzqX+RcG6Ts4helNx8wwEYCFZ+Y1gfAguReF3p3xqqaf18j0UXVPVSn2WhQVXH5t1tAAAlPKpLwHPdnoe0VtauSqlHYdNx2hb6aUZ0xGMyT+/1/dL6HXLprT1kOkYIuiUvrGSS77i9rAdLwBAk5b1t8DBLswlekjml9tNR2iP1hQ29+5a2cZbOUrb3jIdoy3lHXM4FVnqJDpI6x+Uc+kHOjF0NwoA5fLiAsr6FFDoxnyiN2Seeh2n6t//fMvbDtOYz5uOYVTqsa2mI7Ql86udpiOIINNsLBfSt3Zq+K4UAIBybnGrUnwakHdmhCuccp3ko64/FeuazPRrpiMYl316J40Ff34vcBo22adfNx1DBJSCfcoJXU0Hd9ftWgEAKOVSv1WozwNON+cVwbXw0xdx6ks6CMuoVq4qBQDQTZv5BzaZjrEkmenXsAtV0zFEIKm0crii3a1+T6arBQCglE8+pLT+crfnFcHUypRZWO+/D5DFhzZj1+TYDID0Y69S3euvfR207fjy9074QkMpfU2xmNrV6Ym6XgAASoX0vUrxXRNzi+BZePAF6j7ajKWZKrH48BbTMTxD2w4Hv/+Ur94ISD2+lfpB//zOCd+wFeq6Ui71TDcmC3VjkuNp1CrPRAYG+4HLTGUQwaBtTXX3IqNXXIjywRnzs997guqbC6ZjeEpjLk94bIjB81eYjnJSrWyFfbc9gm74709PwtO0hpvK+dSD3ZrQWAEAaNYrv44MxGLApSZzCP9rzBdQIYvh955lOso7yj23m7kf/bfpGJ5U2nKAkQ+sJrxs0HSUd3Tgrl9Qkc1/hNsUt1byqX/t5pRGCwAcKQF90cFxBWtNZxH+Vt56iMHzV9D/rmWmoxxXYz7Pnq9sQPtw0WI3aNuh+NIso5f/CVZ/2HSc40o++goL639nOoYIGI36ViWfurvb8xovAADNWuUJeRIg2qY1uY27SVw6Rd+ot75FOtUGe766gcZbOdNRPK2Vq1LZOcfoX1+AChlZonRCpa2HOHD742jbP2sVhB+of67kk/9kYmZPFACAZr3yVGQgWgP1UdNZhH/ppk3u2V0k3n+uZx4l65bNvm88QulV2TL2VDTm8lR3LTDywT/2TAmo7U+y+x8ewqnImxvCNRrF18r51J2mAnimAAA069X/6e+PJlHqCsD7q7mEJznVJtlnvFEC7FqT/d98lMILwTj4plvqB7PU9iZJfGCN8RJQeWOe3bc8jJ2Xd/6Fa2yN+vtKPnWvyRCeKgAAjXp1c6Q/thfFJwFv/iFQeJ5TbZJ5ciex85bTv8rMmoBWtsLer26g+FLv7vffjtpshuLLB0hcOkUoGjGSobBpP3u+tgG7UDMyvwikmkJdV84n15sO4rkCANCsV7aHI0O/UUp/GoiZziP8SR/dqlWFLQYvPLOrrwiWXp5l980/ozaT7tqcQdRcKJL79RvELlhJZHm8a/Nq22H+J88xe/c0umF3bV4ReBml1JWlfPIJ00HA44/Z4/GJKVvpXwDnmc4i/G3wT1fx7u9cSeTMkY7O45TrHF63keTPX0bbsuO1W1TIYvm17+OM6/8SK9LZ7y3VPYscvPtJStv9fVKh8JYje/vziWIx9abpLMd4ugAADA0tn3TC9iNKyxsCoj1Wf4iJa/6MMz7/54SGBlwdWzdt0k+8xty6jTRTJVfHFv+n/8wRVt70QZZ9eA0od//7aiaLzD+widSjr0h5E+7SbLR05Kpi8XDKdJS383wBOCo8mJi4E/RtpoMI/wvFo0z8zXsYv+q9bT9WbmbKZJ/cweJDW3x7qp0fxc5bzsRnLmHZRy/A6m/viUD59TnSj28l88vtOPK4X7hMwX2lfOrLgOfOLvdLAQBgMD5+LYr7kHUBwgUqZDF88dkkLpsi/v4p+lcmTn6R1tRmUhQ3z5LftJfiizPybdGgcCJK4rLVJP5qNfGLz8aKnXyxoFNvUd5+iOKWA+Se3U1txlNfykRw1FDqpnIu+R+mg5yIrwoAQCwxfrFC/xzUOYajiIAJxaPEVk8SWZEgNDxAaHgAXW9iVxrYhSq12Sy12QxOuW46qjgepYisTBD7o0n6RgcJxQewon3YlQZOsU4jVaR2IE3jcF5Km+i0XVihq8vZhe2mg7wT3xUAgNHR0Xjdse5Fc63pLEIIIcTvKR6M9akvJpNJzy8G8mUBOGZwZOxzWqt7FAyZziKEEKKn5ZTmplIh9TPTQU6VrwsAQDw+sdpWej1ymJAQQggzpp2wvqGaTvvq3VHfF4CjrFhi/AYF3we8sQG8EEKIoMtq+EYln1oH+O6UqKAUAAAGEsvPDWHfD3zIdBYhhBCBtkHZ4S+VSvNJ00GWKlAF4ChrKD52o1bqTsCbB8MLIYTwJ80OlL6lnE8/bTpKuzx5FkCbdKNe3RztD6/TlhUFdQngjTNFhRBC+FUWpb5Zzqeub9are0yHcUMQnwD8P7HE+EUofihbCQshhFiCOlr/KETzjkKhkDEdxk2BLwBHqaHE5FUa57vA+abDCCGE8Lymgn+3LfuuajY7azpMJ/RKATgmNDgydh2a22UnQSGEEMfRQquf2sq6o5Zf2Gc6TCf1WgE4JjIUH7tBK/V14N2mwwghhDBLQ0lp7ret8A9qufkZ03m6oVcLwDHhofj41VpxK3CR6TBCCCG6THMYpX/Yp+wf53K5nOk43dTrBeD3BhNjH0Grm1F8gmC+HSGEEOIIG3jSUfr+ai79X0DTdCATpAD8gejo6CrVsq5XiuuBd5nOI4QQwjX7teY/ddj5t2omc9B0GNOkAJxYKBYf/7hSXAd8CtliWAgh/GgW2OBo/XC1kH7RdBgvkQJwKlatig4V65/U6GuAK4GY6UhCCCFOaBsw7TjWY9Xi4gv4cJ/+bpACcLpWrozFSo0PYenLlVYfA9aYjiSEED0uqdHPgjWtw860307lM0UKQJsGRs44x9KtjymtLkXptRwpBPLvKoQQneEAu0A/j7Kes2z9fLGYetN0KD+SDyqXjYyMjDS1tVbr0Fql9IUcKQRrgKjhaEII4ScazRyKXVqp19B6m9Z621C/tSOZTJZMhwsCKQDdoQZGzjg75DhrtHLOQrMCS01ampWO0pNKM66gTx9ZW9DPkbIwYDizEEK4pQkc+9AuKWhqKABpIKmVSlvotKOZU1rNWFrvLxZHZmBP3VjiHvC/HnYUPb8ZXgoAAAAASUVORK5CYII='
