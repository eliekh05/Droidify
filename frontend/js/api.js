/**
 * Droidify API client
 * Same-origin fetch with AbortController timeout
 */
const BASE = '';

async function get(path, params = {}, timeoutMs = 8000) {
  const qs = new URLSearchParams(
    Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ''))
  ).toString();
  const url = `${BASE}/api${path}${qs ? '?' + qs : ''}`;

  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);

  try {
    const res = await fetch(url, { signal: ctrl.signal });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
    return res.json();
  } catch (e) {
    clearTimeout(timer);
    if (e.name === 'AbortError') throw new Error(`Request timed out: ${path}`);
    throw e;
  }
}

const api = {
  health:          ()              => get('/health'),
  devices:         (p = {})       => get('/devices', p),
  device:          (code, ms)     => get(`/devices/${encodeURIComponent(code)}`, {}, ms || 20000),
  roms:            (p = {})       => get('/roms', p),
  recoveries:      (p = {})       => get('/recoveries', p),
  tools:           ()              => get('/tools'),
  androidVersions: ()              => get('/android-versions'),
  guides:          (codename)     => get(`/guides/${encodeURIComponent(codename)}`),
};
