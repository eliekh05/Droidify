(function () {
  'use strict';
  const LIMIT = 24;
  const esc = s => String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid=document.getElementById('recovery-grid'),metaEl=document.getElementById('results-meta');
  const paginEl=document.getElementById('pagination'),input=document.getElementById('search-input'),btn=document.getElementById('search-btn');
  let currentQ='';

  window.load = async function(offset=0) {
    grid.innerHTML=Array(6).fill('<div class="column is-6-mobile is-4-tablet"><div class="skeleton" style="height:90px"></div></div>').join('');
    try {
      const data=await api.recoveries({q:currentQ||undefined,limit:LIMIT,offset});
      metaEl.className='results-meta';
      metaEl.textContent=`${data.total.toLocaleString()} recovery build${data.total!==1?'s':''}`;
      grid.innerHTML=data.recoveries.length
        ? data.recoveries.map((r,i)=>`<div class="column is-6-mobile is-4-tablet" data-aos="fade-up" data-aos-delay="${Math.min(i,6)*40}">
            <div class="card">
              <div class="card-content">
                <div class="card-mfr">${esc(r.recovery_type||'recovery')}</div>
                <p class="title is-6 mb-1">${esc(r.model_name||r.codename)}</p>
                <div class="card-codename">${esc(r.codename)}</div>
                ${r.download_url?`<a href="${esc(r.download_url)}" target="_blank" rel="noopener" style="font-size:.78rem;color:var(--accent)">Download →</a>`:''}
              </div>
            </div>
          </div>`).join('')
        : '<div class="column"><div class="empty-state">No recoveries found.</div></div>';
      const pages=Math.ceil(data.total/LIMIT),cur=Math.floor(offset/LIMIT);
      if(pages>1){
        let h=`<a class="pagination-previous button${cur===0?' is-disabled':''}" onclick="load(${(cur-1)*LIMIT})">Prev</a>`;
        h+=`<a class="pagination-next button${cur>=pages-1?' is-disabled':''}" onclick="load(${(cur+1)*LIMIT})">Next</a><ul class="pagination-list">`;
        for(let i=Math.max(0,cur-3);i<=Math.min(pages-1,cur+3);i++)
          h+=`<li><a class="pagination-link button${i===cur?' is-current':''}" onclick="load(${i*LIMIT})">${i+1}</a></li>`;
        paginEl.innerHTML=h+'</ul>';
      }
      if(window.AOS)AOS.refresh();
      if(offset)window.scrollTo({top:0,behavior:'smooth'});
    } catch(e){grid.innerHTML=`<div class="column"><div class="error-state">${esc(e.message)}</div></div>`;}
  };
  function doSearch(){currentQ=input.value.trim();load(0);}
  btn.addEventListener('click',doSearch);
  input.addEventListener('keydown',e=>{if(e.key==='Enter')doSearch();});
  load(0);
})();
