/* ===== Theme ===== */
(function(){
  const s=localStorage.getItem("theme");
  if(s)document.documentElement.setAttribute("data-theme",s);
  else if(matchMedia("(prefers-color-scheme:dark)").matches)document.documentElement.setAttribute("data-theme","dark");
})();
document.getElementById("theme-toggle").addEventListener("click",()=>{
  const h=document.documentElement;
  const n=h.getAttribute("data-theme")==="dark"?"light":"dark";
  h.setAttribute("data-theme",n);localStorage.setItem("theme",n);
});

/* ===== Font Size Toggle ===== */
(function(){
  const saved=localStorage.getItem("fontsize");
  if(saved)document.documentElement.setAttribute("data-fontsize",saved);
})();
document.getElementById("font-toggle").addEventListener("click",()=>{
  const h=document.documentElement;
  const cur=h.getAttribute("data-fontsize");
  const next=cur==="large"?"":"large";
  if(next)h.setAttribute("data-fontsize",next);
  else h.removeAttribute("data-fontsize");
  localStorage.setItem("fontsize",next);
  document.getElementById("font-label").textContent=next==="large"?"A−":"A+";
});
(function(){
  const s=localStorage.getItem("fontsize");
  if(s==="large")document.getElementById("font-label").textContent="A−";
})();

/* ===== Nav shadow ===== */
const navBar=document.getElementById("nav-bar");
window.addEventListener("scroll",()=>navBar.classList.toggle("scrolled",scrollY>10),{passive:true});

/* ===== Sidebar scroll spy ===== */
const sidebar=document.getElementById("sidebar");
const sbLinks=sidebar?sidebar.querySelectorAll(".sb-link"):[];
const allSections=document.querySelectorAll(".section[id]");

const sbGroups=sidebar?sidebar.querySelectorAll(".sb-group"):[];

function updateSpy(){
  const y=scrollY+180;
  let cur="";
  allSections.forEach(s=>{if(s.offsetTop<=y)cur=s.id});
  sbLinks.forEach(l=>{
    l.classList.toggle("active",l.getAttribute("data-target")===cur);
  });
  sbGroups.forEach(g=>{
    g.classList.toggle("sb-expanded",g.getAttribute("data-section")===cur);
  });
}
window.addEventListener("scroll",updateSpy,{passive:true});
updateSpy();

/* ===== Table Sorting ===== */
document.querySelectorAll(".survey-table").forEach(table=>{
  const headers=table.querySelectorAll("th.sortable");
  let sortCol=-1,sortDir=0;
  headers.forEach((th,ci)=>{
    th.addEventListener("click",()=>{
      if(sortCol===ci)sortDir=(sortDir+1)%3;
      else{sortCol=ci;sortDir=1}
      headers.forEach(h=>h.classList.remove("sort-asc","sort-desc"));
      if(sortDir===1)th.classList.add("sort-asc");
      else if(sortDir===2)th.classList.add("sort-desc");
      const tbody=table.querySelector("tbody");
      const rows=Array.from(tbody.querySelectorAll("tr"));
      if(sortDir===0){
        rows.sort((a,b)=>+(a.dataset.origIdx||0)-+(b.dataset.origIdx||0));
      }else{
        rows.sort((a,b)=>{
          const at=a.children[ci]?.textContent.trim()||"";
          const bt=b.children[ci]?.textContent.trim()||"";
          const an=parseFloat(at),bn=parseFloat(bt);
          let c=!isNaN(an)&&!isNaN(bn)?an-bn:at.localeCompare(bt);
          return sortDir===2?-c:c;
        });
      }
      rows.forEach(r=>tbody.appendChild(r));
    });
  });
  table.querySelectorAll("tbody tr").forEach((r,i)=>r.dataset.origIdx=i);
});

/* ===== Per-table Search ===== */
document.querySelectorAll(".table-search").forEach(input=>{
  const card=input.closest(".table-card");
  const table=card.querySelector(".survey-table");
  const countEl=card.querySelector(".count-visible");
  input.addEventListener("input",()=>{
    const q=input.value.toLowerCase().trim();
    let v=0;
    table.querySelectorAll("tbody tr").forEach(row=>{
      const m=!q||row.textContent.toLowerCase().includes(q);
      row.classList.toggle("hidden",!m);if(m)v++;
    });
    countEl.textContent=v;
  });
});

/* ===== Global Search ===== */
const globalSearch=document.getElementById("global-search");
globalSearch.addEventListener("input",()=>{
  const q=globalSearch.value.toLowerCase().trim();
  document.querySelectorAll(".survey-table").forEach(table=>{
    const countEl=table.closest(".table-card").querySelector(".count-visible");
    let v=0;
    table.querySelectorAll("tbody tr").forEach(row=>{
      if(!q){row.classList.remove("hidden");v++;return}
      const m=row.textContent.toLowerCase().includes(q);
      row.classList.toggle("hidden",!m);if(m)v++;
    });
    countEl.textContent=v;
  });
});

/* ===== Filters ===== */
const filterChips=document.querySelectorAll(".chip[data-filter]");
const handChips=document.querySelectorAll(".chip-toggle[data-hand]");
const yearFilter=document.getElementById("year-filter");

function applyFilters(){
  const activeChip=document.querySelector(".chip.chip-active[data-filter]");
  const filter=activeChip?.dataset.filter||"all";
  const yearVal=yearFilter.value;

  const activeHands=new Set();
  handChips.forEach(c=>{if(c.classList.contains("chip-on"))activeHands.add(c.dataset.hand)});

  document.querySelectorAll(".survey-table").forEach(table=>{
    const countEl=table.closest(".table-card").querySelector(".count-visible");
    let v=0;
    table.querySelectorAll("tbody tr").forEach(row=>{
      let show=true;
      if(filter==="code"&&row.dataset.code!=="true")show=false;
      if(filter==="weights"&&row.dataset.weights!=="true")show=false;
      if(yearVal&&show){
        const ry=row.dataset.year||"";
        if(yearVal==="older"){if(ry&&+ry>2022)show=false}
        else{if(ry&&ry!==yearVal)show=false}
      }
      if(activeHands.size>0&&show){
        const rh=row.dataset.hand||"";
        let handMatch=false;
        activeHands.forEach(h=>{if(rh.includes(h))handMatch=true});
        if(!handMatch)show=false;
      }
      row.classList.toggle("hidden",!show);
      if(show)v++;
    });
    countEl.textContent=v;
  });
}

filterChips.forEach(chip=>{
  chip.addEventListener("click",()=>{
    filterChips.forEach(c=>c.classList.remove("chip-active"));
    chip.classList.add("chip-active");
    globalSearch.value="";
    document.querySelectorAll(".table-search").forEach(s=>s.value="");
    applyFilters();
  });
});

handChips.forEach(chip=>{
  chip.addEventListener("click",()=>{
    chip.classList.toggle("chip-on");
    globalSearch.value="";
    document.querySelectorAll(".table-search").forEach(s=>s.value="");
    applyFilters();
  });
});

yearFilter.addEventListener("change",()=>{
  globalSearch.value="";
  document.querySelectorAll(".table-search").forEach(s=>s.value="");
  applyFilters();
});

/* ===== Detail Panel ===== */
const panel=document.getElementById("detail-panel");
const dpTabs=document.getElementById("dp-tabs");
const dpBody=document.getElementById("dp-body");
const dpMinimize=document.getElementById("dp-minimize");
const dpCloseAll=document.getElementById("dp-close-all");

let detailTabs=[];  // {id, title, html}
let activeTabId=null;
let tabCounter=0;

function renderTabs(){
  dpTabs.innerHTML="";
  detailTabs.forEach(t=>{
    const tab=document.createElement("button");
    tab.className="dp-tab"+(t.id===activeTabId?" active":"");
    tab.innerHTML=`<span></span><span class="dp-tab-close" data-tab-id="${t.id}">&times;</span>`;
    tab.firstElementChild.textContent=t.title;
    tab.addEventListener("click",e=>{
      if(e.target.classList.contains("dp-tab-close")){
        closeTab(+e.target.dataset.tabId);
        return;
      }
      activeTabId=t.id;
      renderTabs();
      showTabContent();
    });
    dpTabs.appendChild(tab);
  });
}

function showTabContent(){
  const t=detailTabs.find(t=>t.id===activeTabId);
  if(t)dpBody.innerHTML=t.html;
  else dpBody.innerHTML="";
}

function closeTab(id){
  detailTabs=detailTabs.filter(t=>t.id!==id);
  if(detailTabs.length===0){
    panel.classList.remove("open","minimized");
    activeTabId=null;
    return;
  }
  if(activeTabId===id)activeTabId=detailTabs[detailTabs.length-1].id;
  renderTabs();showTabContent();
}

function openDetail(url,title){
  panel.classList.add("open");
  panel.classList.remove("minimized");

  const existing=detailTabs.find(t=>t.url===url);
  if(existing){
    activeTabId=existing.id;
    renderTabs();showTabContent();
    return;
  }

  const id=++tabCounter;
  const tab={id,title,url,html:'<p class="dp-p" style="color:var(--text-graphite)">Loading...</p>'};
  detailTabs.push(tab);
  activeTabId=id;
  renderTabs();showTabContent();

  fetch(url).then(r=>{
    if(!r.ok)throw new Error(r.status);
    return r.text();
  }).then(html=>{
    tab.html=html;
    if(activeTabId===id)showTabContent();
  }).catch(()=>{
    tab.html='<p class="dp-p" style="color:var(--badge-no)">Failed to load detail. Use a local server (e.g. <code>python -m http.server</code>) for local preview.</p>';
    if(activeTabId===id)showTabContent();
  });
}

dpMinimize.addEventListener("click",()=>panel.classList.toggle("minimized"));
document.getElementById("dp-maximize").addEventListener("click",()=>{
  panel.classList.toggle("maximized");
  panel.classList.remove("minimized");
});
dpCloseAll.addEventListener("click",()=>{
  detailTabs=[];activeTabId=null;
  panel.classList.remove("open","minimized");
  dpTabs.innerHTML="";dpBody.innerHTML="";
});

document.addEventListener("click",e=>{
  const btn=e.target.closest(".detail-btn");
  if(!btn)return;
  e.preventDefault();
  openDetail(btn.dataset.detail,btn.dataset.title);
});
