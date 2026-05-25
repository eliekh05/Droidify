(function () {
  'use strict';
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const tbody = document.getElementById('android-tbody');

  api.androidVersions().then(data => {
    const versions = [...data.versions].reverse();
    tbody.innerHTML = versions.map((v, i) => {
      const cls = v.status==='active'?'tag-green':v.status==='partial'?'tag-orange':'tag-gray';
      const lbl = v.status==='active'?'ACTIVE':v.status==='partial'?'PREVIEW':'EOL';
      return `<tr class="reveal" style="transition-delay:${Math.min(i,12)*40}ms">
        <td style="font-weight:600">Android ${esc(v.version_number)}</td>
        <td style="color:var(--muted)">${esc(v.codename||'—')}</td>
        <td style="font-family:var(--mono);color:var(--info)">${esc(String(v.api_level||'—'))}</td>
        <td style="color:var(--muted)">${esc(String(v.release_year||'—'))}</td>
        <td><span class="tag ${cls}">${lbl}</span></td>
      </tr>`;
    }).join('');
    if (window._reObserve) window._reObserve();
  }).catch(e => {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">${esc(e.message)}</td></tr>`;
  });
})();
