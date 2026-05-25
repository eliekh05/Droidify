(function () {
  'use strict';
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const tbody   = document.getElementById('android-tbody');
  const sfilt   = document.getElementById('status-filter');
  const apifilt = document.getElementById('api-min');
  const btn     = document.getElementById('filter-btn');
  let allVersions = [];

  api.androidVersions().then(data => {
    allVersions = [...data.versions].reverse();
    render(allVersions);
  }).catch(e => { tbody.innerHTML=`<tr><td colspan="5" class="empty-state">${esc(e.message)}</td></tr>`; });

  function render(versions) {
    if (!versions.length) {
      tbody.innerHTML='<tr><td colspan="5" class="empty-state">No results.</td></tr>';
      return;
    }
    tbody.innerHTML = versions.map(v => {
      const statusClass = v.status==='active'?'tag-green':v.status==='partial'?'tag-orange':'tag-gray';
      const statusLabel = v.status==='active'?'Active':v.status==='partial'?'Preview':'EOL';
      return `<tr>
        <td style="font-weight:600">Android ${esc(v.version_number)}</td>
        <td style="color:var(--muted)">${esc(v.codename||'—')}</td>
        <td style="font-family:var(--font-mono);color:var(--info)">${esc(String(v.api_level||'—'))}</td>
        <td style="color:var(--muted)">${esc(String(v.release_year||'—'))}</td>
        <td><span class="tag ${statusClass}">${statusLabel}</span></td>
      </tr>`;
    }).join('');
  }

  function applyFilter() {
    const status = sfilt.value;
    const minApi = parseInt(apifilt.value) || 0;
    render(allVersions.filter(v => {
      if (status && v.status !== status) return false;
      if (minApi && Number(v.api_level) < minApi) return false;
      return true;
    }));
  }

  btn.addEventListener('click', applyFilter);
  sfilt.addEventListener('change', applyFilter);
})();
