if (document.querySelector('#papers')) {
const papers=[...document.querySelectorAll('.paper')],year=document.querySelector('#year'),kind=document.querySelector('#kind'),search=document.querySelector('#search'),count=document.querySelector('#result-count'),empty=document.querySelector('#empty'),toggle=document.querySelector('#show-all'),title=document.querySelector('#pub-title');
const fullPage=document.body.dataset.publications==='all';
let expanded=fullPage;
function render(){const query=search.value.trim().toLowerCase(),filtering=query!==''||year.value!=='all'||kind.value!=='all';let visible=0;const selectedMode=!expanded&&!filtering;const ordered=selectedMode?[...papers].sort((a,b)=>Number(a.dataset.rank)-Number(b.dataset.rank)):papers;for(const paper of ordered){const match=(year.value==='all'||paper.dataset.year===year.value)&&(kind.value==='all'||paper.dataset.kind===kind.value)&&paper.textContent.toLowerCase().includes(query)&&(!selectedMode||paper.dataset.selected==='true');paper.hidden=!match;if(match)visible++;document.querySelector('#papers').append(paper);}count.textContent=selectedMode?`${visible} of ${papers.length}`:`${visible} paper${visible===1?'':'s'}`;empty.hidden=visible!==0;title.textContent=selectedMode?'Selected publications':'Publications';toggle.hidden=fullPage||filtering;toggle.textContent=expanded?'Show selected publications':`View all ${papers.length} publications`;toggle.setAttribute('aria-expanded',String(expanded));}
for(const el of [year,kind])el.addEventListener('change',render);search.addEventListener('input',render);toggle.addEventListener('click',()=>{expanded=!expanded;render();});document.querySelector('.tools').hidden=false;render();

}
// Ensure inline autoplay starts once media is available, including WebKit.
for (const video of document.querySelectorAll('video[autoplay]')) {
  video.muted = true;
  video.defaultMuted = true;
  const start = () => { const play = video.play(); if (play) play.catch(() => {}); };
  video.addEventListener('canplay', start, {once: true});
  start();
}
