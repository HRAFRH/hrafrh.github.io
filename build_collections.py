# Executed by build_portfolio.py after the detailed project library is generated.
collections=json.loads((ROOT/'content/collections.json').read_text(encoding='utf-8'))
platform_media=json.loads((ROOT/'content/platform-media.json').read_text(encoding='utf-8'))
by_id={d['id']:d for d in data}
assert len(collections)==5
assert sorted(m for g in collections for m in g['members'])==sorted(by_id)
parents={m:g for g in collections for m in g['members']}
def platform_figure(src,caption,pre='../../'):
 return '<figure><button data-full="'+pre+e(src)+'" data-alt="'+e(caption)+'" aria-label="Inspect project image"><img src="'+pre+e(src)+'" alt="'+e(caption)+'" loading="lazy"></button><figcaption>'+e(caption)+'</figcaption></figure>'
def platform_card(g,pre=''):
 terms=' '.join([g['title'],g['lead']]+[by_id[m]['title']+' '+by_id[m]['contribution']+' '+' '.join(by_id[m]['tags']) for m in g['members']])
 return '<article class="project platform-card" data-project data-domain="'+g['domain']+'" data-search="'+e(terms)+'"><a href="'+pre+'projects/'+g['id']+'/"><div class="cover"><img src="'+pre+e(g['cover'])+'" alt="'+e(g['caption'])+'" loading="lazy"></div><div class="project-body"><p class="meta">'+e(labels[g['domain']])+' · Design, integration and testing</p><h3>'+e(g['title'])+'</h3><p class="summary">'+e(g['lead'])+'</p><span class="more">Explore the work →</span></div></a></article>'
# Homepage presents the five platforms, rather than isolated tasks.
home=(D/'index.html').read_text(encoding='utf-8')
start=home.index('<section class="section" id="projects">')
end=home.index('<section class="section"><div class="section-title"><h2>Technical documents',start)
home=home[:start]+'<section class="section" id="projects"><div class="section-title"><h2>Engineering projects</h2><a href="projects/">Explore all five →</a></div><p class="section-note">Aircraft, ground robotics, marine systems and avionics. Design, modeling, integration and test work are presented together within each platform portfolio.</p><div class="project-grid">'+''.join(platform_card(g) for g in collections)+'</div></section>'+home[end:]
home=home.replace('Electronics integration and technical coordination at FARASHA SYSTEMS, alongside independent UAV configuration and diagnostics. My project library also includes fixed-wing design development, quadcopter fabrication preparation and surface-vessel system studies.','I work across aircraft, ground robotics and marine systems, connecting airframe and electrical design with autopilot integration, diagnostics and practical test support.')
(D/'index.html').write_text(home,encoding='utf-8')
filters='<button data-domain-filter="" aria-pressed="true">All platforms</button>'+''.join('<button data-domain-filter="'+k+'" aria-pressed="false">'+e(v)+'</button>' for k,v in labels.items())
body='<main id="main" class="wrap"><section class="page-head"><p class="kicker">Design · Build · Integrate · Test</p><h1>Engineering projects</h1><p>Five platform portfolios bring together the aircraft, systems and engineering work behind each area. Explore the builds, modeling, electronics, configuration, reports and test evidence within them.</p></section><div class="filters"><div class="filter-buttons" role="group" aria-label="Filter project domain">'+filters+'</div><input id="project-search" type="search" aria-label="Search projects" placeholder="Search platforms, tools or subsystems"></div><p class="count" id="result-count" role="status" aria-live="polite"></p><section class="section"><div class="project-grid">'+''.join(platform_card(g,'../') for g in collections)+'</div><p class="empty" id="empty" hidden>No matching platforms. Clear the search or choose another category.</p></section></main>'
(D/'projects/index.html').write_text(page('Engineering projects',body,'../'),encoding='utf-8')
for g in collections:
 sections=[]
 for number,m in enumerate(g['members'],1):
  d=by_id[m];figs=[];seen=set()
  for im in d.get('gallery',[]):
   if im['src'] in seen:continue
   seen.add(im['src']);figs.append(platform_figure(im['src'],im['caption']))
  if not figs and d.get('photo_verified') and d.get('image'):
   figs.append(platform_figure(d['image'],d['caption']))
  samples=''.join(platform_figure(x['src'],x['caption']) for x in d.get('work_samples',[]))
  sample_block='<h3>Architecture & design</h3><div class="gallery technical-gallery">'+samples+'</div>' if samples else ''
  gallery='<div class="gallery">'+''.join(figs)+'</div>' if figs else ''
  related=[p for p in papers if p['id'] in d.get('papers',[])]
  documents='<div class="documents">'+''.join(doc(p,'../../') for p in related)+'</div>' if related else ''
  embedded=project_media(d,'../../')
  section='<details class="platform-build" id="'+m+'"'+(' open' if number<=2 else '')+'><summary><span class="build-number">'+str(number).zfill(2)+'</span><span><strong>'+e(d['title'])+'</strong><small>'+e(d['status'])+'</small></span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="build-content"><p class="build-lead">'+e(d['problem'])+'</p><div class="responsibilities"><div><h3>My responsibilities</h3><p>'+e(d['contribution'])+'</p></div><div><h3>Delivery</h3><p>'+e(d['delivery'])+'</p></div></div>'+gallery+sample_block+documents+embedded+'<details class="evidence"><summary>Evidence and validation</summary><p>'+e(d['scope'])+'</p></details><a class="detail-link" href="../'+m+'/">Detailed project record →</a></div></details>'
  sections.append(section)
 extra=''
 if g['id']=='aircraft':
  extra='<section class="section platform-extra" id="fabrication"><p class="kicker">Airframe design & fabrication</p><h2>From printed parts to an integrated airframe</h2><p>Original Cobra VTOL build photographs show structural parts, alignment and avionics integration. These stages sit within the aircraft-development portfolio.</p><div class="gallery">'+''.join(platform_figure(x['src'],x['caption']) for x in platform_media['cobra'])+platform_figure(platform_media['workshop'],'VTOL airframe components laid out for assembly.')+'</div></section>'
 if g['id']=='rotorcraft':
  extra='<section class="section platform-extra" id="bench-build"><p class="kicker">Assembly & integration</p><h2>7-inch Pixhawk build</h2><p>Another build within the multirotor portfolio, shown during assembly and field preparation.</p><div class="gallery">'+''.join(platform_figure(x['src'],x['caption']) for x in platform_media['pixhawk-seven'])+'</div></section>'
 phase_cards=''.join('<article><span>'+str(i+1).zfill(2)+'</span><h3>'+e(t)+'</h3><p>'+e(c)+'</p></article>' for i,(t,c) in enumerate(g['stages']))
 anchors=''.join('<a href="#'+m+'">'+e(by_id[m]['title'])+'</a>' for m in g['members'])
 body='<main id="main" class="wrap platform-page"><header class="case-top"><p class="breadcrumb"><a href="../">Projects</a> / '+e(labels[g['domain']])+'</p><p class="kicker">Platform portfolio</p><h1>'+e(g['title'])+'</h1><p class="lead">'+e(g['lead'])+'</p><figure class="case-cover"><img src="../../'+e(g['cover'])+'" alt="'+e(g['caption'])+'"></figure><p class="caption">'+e(g['caption'])+'</p></header><section class="section"><div class="section-title"><h2>The engineering work</h2></div><div class="engineering-flow">'+phase_cards+'</div><p class="portfolio-scope">This portfolio includes distinct builds and engagements. The delivery and validation reached are identified within each section.</p></section><nav class="chapter-nav" aria-label="Project sections">'+anchors+'</nav><section class="platform-builds"><h2>Platforms & systems</h2><div class="links"><button class="btn" id="expand-builds" type="button">Expand all sections</button><button class="btn" id="collapse-builds" type="button">Collapse all sections</button></div>'+''.join(sections)+'</section>'+extra+'<div class="next"><a href="../">← All engineering projects</a><a href="../../blog/">Engineering notes →</a></div></main>'
 out=D/'projects'/g['id'];out.mkdir(exist_ok=True);(out/'index.html').write_text(page(g['title'],body,'../../'),encoding='utf-8')
# Existing deep links remain useful, and lead back into their parent portfolio.
for m,g in parents.items():
 path=D/'projects'/m/'index.html';s=path.read_text(encoding='utf-8')
 s=s.replace('<a href="../">Projects</a>','<a href="../'+g['id']+'/">'+e(g['title'])+'</a>')
 s=s.replace('<a href="../">← All projects</a>','<a href="../'+g['id']+'/#'+m+'">← '+e(g['title'])+'</a>')
 path.write_text(s,encoding='utf-8')
# Correct navigation on the five additional pages.
for path in [D/'projects/index.html']+[D/'projects'/g['id']/'index.html' for g in collections]:
 s=path.read_text(encoding='utf-8')
 s=re.sub(r'href="([^"]*)index.html#about">About',r'href="\1about/">About',s)
 s=re.sub(r'href="([^"]*)Achraf_Rahibe_CV.pdf">Resume</a>',r'href="\1index.html#resume">Resume</a>',s)
 s=re.sub(r'(<a href="([^"]*)technical-notes/">Documents</a>)',r'<a href="\2blog/">Blog</a>\1',s,count=1)
 path.write_text(s,encoding='utf-8')
with (A/'site.css').open('a',encoding='utf-8') as f:
 f.write('''
.project-grid:has(.platform-card){grid-template-columns:repeat(2,minmax(0,1fr))}.platform-card:last-child{grid-column:1/-1;display:block}.platform-card:last-child>a{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center}.platform-card:last-child .cover{margin:0}.engineering-flow{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:35px}.engineering-flow article{border-top:1px solid var(--line);padding-top:20px}.engineering-flow article>span{font-size:12px;color:var(--accent)}.engineering-flow h3{font-size:18px;margin:12px 0}.engineering-flow p,.portfolio-scope{font-size:13px;color:var(--muted)}.portfolio-scope{margin:28px 0 0;max-width:800px}.chapter-nav{display:flex;flex-wrap:wrap;gap:12px 20px;border-block:1px solid var(--line);padding:20px 0;margin:0 0 45px}.chapter-nav a{font-size:12px}.platform-builds>h2,.platform-extra h2{font:36px/1.25 Georgia,serif;margin:0 0 30px}.platform-build{border-top:1px solid var(--line);margin:0}.platform-build:last-child{border-bottom:1px solid var(--line)}.platform-build>summary{display:flex;align-items:center;gap:22px;padding:25px 0;cursor:pointer;list-style:none}.platform-build>summary::-webkit-details-marker{display:none}.build-number{font-size:12px;color:var(--accent);align-self:flex-start;padding-top:6px}.platform-build>summary strong{display:block;font-size:23px;line-height:1.4;font-weight:500}.platform-build>summary small{display:block;font-size:12px;color:var(--muted);margin-top:7px}.expand-icon{margin-left:auto;color:var(--accent);font-size:27px}.platform-build[open] .expand-icon{transform:rotate(45deg)}.build-content{padding:0 0 40px 42px}.build-lead{max-width:850px;color:var(--muted);font-size:16px}.responsibilities{display:grid;grid-template-columns:1.4fr 1fr;gap:35px;margin:25px 0 35px}.responsibilities h3,.build-content>h3{font-size:16px}.responsibilities p{font-size:14px;color:var(--muted)}.build-content .gallery{margin:25px 0 40px}.build-content .gallery img{height:320px}.technical-gallery img{background:#fff}.evidence{padding:16px 0;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}.evidence summary{cursor:pointer;color:var(--accent)}.detail-link{display:inline-block;margin-top:12px;font-size:12px}.platform-extra{margin-top:55px}.platform-extra>p{max-width:800px;color:var(--muted)}.platform-page .case-cover{margin:30px 0 0}.platform-build .video-grid{margin-top:20px}.platform-build .section{padding-bottom:25px}
@media(max-width:800px){.engineering-flow{grid-template-columns:1fr 1fr}.responsibilities{grid-template-columns:1fr;gap:8px}.platform-card:last-child>a{display:block}.platform-card:last-child{grid-column:auto}}@media(max-width:650px){.project-grid:has(.platform-card){grid-template-columns:1fr}}@media(max-width:500px){.engineering-flow{gap:18px}.engineering-flow h3{font-size:16px}.platform-build>summary{gap:13px}.platform-build>summary strong{font-size:19px}.build-content{padding-left:0}.build-content .gallery img{height:auto;max-height:400px}.chapter-nav{gap:12px}.platform-builds>h2,.platform-extra h2{font-size:29px}}
''')
print('Built five platform portfolios containing all 27 detailed records.')

script=(A/'site.js').read_text(encoding='utf-8').replace("+' projects'","+' platform portfolios'")
script+='''
const buildSections=[...document.querySelectorAll('.platform-build')];
document.getElementById('expand-builds')?.addEventListener('click',()=>buildSections.forEach(section=>section.open=true));
document.getElementById('collapse-builds')?.addEventListener('click',()=>buildSections.forEach(section=>section.open=false));
for(const link of document.querySelectorAll('.chapter-nav a'))link.addEventListener('click',()=>{const section=document.getElementById(link.getAttribute('href').slice(1));if(section)section.open=true;});
'''
(A/'site.js').write_text(script,encoding='utf-8')
