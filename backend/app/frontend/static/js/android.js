/* android.js — Android versions table with version codes and usage */
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