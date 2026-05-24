// Droidify API client — same-origin, no framework dependency
const BASE = '';

async function get(path, params = {}) {
  const qs = new URLSearchParams(
    Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ''))
  ).toString();
  const url = `${BASE}/api${path}${qs ? '?' + qs : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API ${res.status}: ${url}`);
  return res.json();
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
