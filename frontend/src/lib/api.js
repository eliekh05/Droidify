// Droidify API client — same-origin, no framework dependency
const BASE = '';

async function get(path, params = {}, timeoutMs = 8000) {
  const qs = new URLSearchParams(
    Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ''))
  ).toString();
  const url = `${BASE}/api${path}${qs ? '?' + qs : ''}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`API ${res.status}: ${url}`);
    return res.json();
  } catch (e) {
    clearTimeout(timer);
    if (e.name === 'AbortError') throw new Error(`Request timed out: ${path}`);
    throw e;
  }
}

export const api = {
  health:          ()       => get('/health'),
  devices:         (p = {}) => get('/devices', p),
  device:          (code)   => get(`/devices/${code}`),
  roms:            (p = {}) => get('/roms', p),
  romsForDevice:   (code)   => get(`/devices/${code}/roms`),
  recoveries:      (p = {}) => get('/recoveries', p),
  tools:           ()       => get('/tools'),
  androidVersions: ()       => get('/android-versions'),
  guides:          (codename) => get(`/guides/${codename}`),
};
