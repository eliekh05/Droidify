(function () {
  'use strict';
  const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid=document.getElementById('tools-grid'),input=document.getElementById('search-input'),btn=document.getElementById('search-btn');
  let allTools=[];

  api.tools().then(data=>{
    allTools=data.tools||data;
    render(allTools);
  }).catch(e=>{grid.innerHTML=`<div class="column"><div class="error-state">${esc(e.message)}</div></div>`;});

  function render(tools){
    grid.innerHTML=tools.map((t,i)=>`<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*50}">
      <div class="card">
        <div class="card-content">
          <p class="title is-6 mb-1">${esc(t.name)}</p>
          ${t.description?`<p style="font-size:.82rem;color:var(--muted);margin:.3rem 0;line-height:1.5">${esc(t.description)}</p>`:''}
          ${t.version?`<div class="card-codename">v${esc(t.version)}</div>`:''}
          ${t.download_url?`<a href="${esc(t.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>`:''}
        </div>
      </div>
    </div>`).join('');
    if(window.AOS)AOS.refresh();
  }
  function doSearch(){const q=input.value.trim().toLowerCase();render(q?allTools.filter(t=>(t.name||'').toLowerCase().includes(q)||(t.description||'').toLowerCase().includes(q)):allTools);}
  btn.addEventListener('click',doSearch);
  input.addEventListener('input',doSearch);
})();
