(function () {
  'use strict';
  const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid=document.getElementById('guides-grid'),input=document.getElementById('codename-input'),btn=document.getElementById('search-btn');

  async function doSearch(){
    const q=input.value.trim();
    if(!q)return;
    grid.innerHTML='<div class="column"><div style="padding:2rem;text-align:center"><div class="spinner"></div></div></div>';
    try{
      const data=await api.guides(q);
      const guides=data.guides||[];
      if(!guides.length){grid.innerHTML=`<div class="column"><div class="empty-state">No guides found for "${esc(q)}".</div></div>`;return;}
      grid.innerHTML=guides.map((g,i)=>`<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*50}">
        <div class="card">
          <div class="card-content">
            <div class="card-mfr">${esc(g.guide_type||g.category||'guide')}</div>
            <p class="title is-6 mb-1">${esc(g.title)}</p>
            ${g.description?`<p style="font-size:.82rem;color:let(--muted);margin:.3rem 0;line-height:1.5">${esc(g.description)}</p>`:''}
            ${g.url?`<a href="${esc(g.url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:let(--accent)">Read guide →</a>`:''}
          </div>
        </div>
      </div>`).join('');
      if(window.AOS)AOS.refresh();
    }catch(e){
      grid.innerHTML=`<div class="column"><div class="empty-state">${e.message.includes('404')?`No guides for "${esc(q)}".`:esc(e.message)}</div></div>`;
    }
  }
  btn.addEventListener('click',doSearch);
  input.addEventListener('keydown',e=>{if(e.key==='Enter')doSearch();});
})();
