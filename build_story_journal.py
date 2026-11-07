# Rich, evidence-led journal. Run last so shared builders retain their original responsibilities.
from pathlib import Path
import json,html,re,posixpath
ROOT=Path(__file__).resolve().parent;D=ROOT/'docs'
def e(v):return html.escape(str(v).replace('\u2014',', ').replace('\u2013','-'),quote=True)
def load(n):return json.loads((ROOT/'content'/n).read_text(encoding='utf8'))
projects=load('projects.json');by={d['id']:d for d in projects};papers=load('papers.json');paper_by={p['id']:p for p in papers};media=load('story-media.json')
# Preserve existing matched video sources for projects beyond this batch.
for d in projects:
 if d['id'] in media:continue
 f=D/'projects'/d['id']/'index.html'
 if not f.exists():continue
 matches=re.findall(r'<video\b([^>]*)>(.*?)</video>',f.read_text(encoding='utf8'),re.S)
 clips=[]
 for attrs,inside in matches:
  src=re.search(r'(?:^|\s)src="([^"]+)"',attrs) or re.search(r'<source[^>]+src="([^"]+)"',inside)
  if not src:continue
  path=posixpath.normpath('projects/'+d['id']+'/'+src[1]);poster=re.search(r'poster="([^"]+)"',attrs)
  if not (D/path).exists():continue
  clips.append({'file':path,'poster':posixpath.normpath('projects/'+d['id']+'/'+poster[1]) if poster else '', 'title':'Project recording','caption':'Matching recording from the project archive. Only the documented stage is represented.'})
 if clips:media[d['id']]=clips
# Use the existing header, navigation and personal logo, including theme controls.
template=(D/'blog/index.html').read_text(encoding='utf8');prefix=template[:template.index('<main')];suffix=template[template.index('<footer class="footer"'):]
def page(title,body,pre):
 p=prefix;s=suffix
 if pre!='../':p=p.replace('="../','="'+pre);s=s.replace('="../','="'+pre)
 p=re.sub(r'<title>.*?</title>','<title>'+e(title)+' | Achraf RAHIBE</title>',p)
 p=p.replace('</head>','<link rel="stylesheet" href="'+pre+'assets/story-journal.css?v=20261106-local"><link rel="stylesheet" href="'+pre+'assets/delivery-story.css?v=20261107-local"></head>')
 return p+body+s

def image(im,pre):return '<figure class="story-photo"><a href="'+pre+e(im['src'])+'" target="_blank" rel="noopener"><img src="'+pre+e(im['src'])+'" alt="'+e(im['caption'])+'" loading="lazy"></a><figcaption>'+e(im['caption'])+'</figcaption></figure>'
def images(d,pre):
 a=[]
 if d.get('reference_images'):a=d['reference_images'][:1]
 elif d.get('photo_verified'):
  if d.get('image'):a.append({'src':d['image'],'caption':d.get('caption','Project photograph')})
  a+=d.get('gallery',[])
 elif d.get('work_samples'):a=d['work_samples'][:1]
 seen=set();result=[]
 for im in a:
  if im['src'] not in seen and (D/im['src']).exists():result.append(im);seen.add(im['src'])
 return result

def videos(d,pre,limit=None):
 a=media.get(d['id'],[])
 if limit:a=a[:limit]
 return '<section class="story-recordings"><h3>Watch the project</h3><div class="story-video-grid">'+''.join('<figure><video controls playsinline preload="none" controlslist="nodownload noremoteplayback" disablepictureinpicture '+('poster="'+pre+e(v['poster'])+'"' if v.get('poster') else '')+'><source src="'+pre+e(v['file'])+'" type="video/mp4">Your browser does not support inline video.</video><figcaption><strong>'+e(v.get('title','Project recording'))+'</strong><span>'+e(v.get('caption',''))+'</span></figcaption></figure>' for v in a)+'</div></section>' if a else ''

def report(p,pre):
 first=p['images'][0] if p.get('images') else ''
 return '<article class="story-report"><div class="report-heading"><p class="kicker">Inside the report · '+str(p.get('page_count',len(p.get('pages',[]))))+' pages</p><h3>'+e(p['title'])+'</h3><p>'+e(p['description'])+'</p></div>'+('<figure class="report-page"><a href="'+pre+e(p['file'])+'" target="_blank" rel="noopener"><img src="'+pre+e(first)+'" alt="'+e(p['captions'][0])+'" loading="lazy"></a><figcaption>'+e(p['captions'][0])+'</figcaption></figure>' if first else '')+'<details class="pdf-inline" open><summary>Read the PDF here</summary><iframe src="'+pre+e(p['file'])+'#view=FitH" loading="lazy" title="'+e(p['title'])+' PDF"></iframe></details><p class="report-scope">'+e(p['scope'])+'</p><div class="links"><a href="'+pre+e(p['file'])+'" target="_blank" rel="noopener">Open PDF in a full window ↗</a><a href="'+pre+'technical-notes/'+e(p['id'])+'/">Document details →</a></div></article>'
def reports(d,pre,limit=None):
 a=[paper_by[k] for k in d.get('papers',[]) if k in paper_by]
 if limit:a=a[:limit]
 return '<section class="story-reports"><h3>From the project documents</h3>'+''.join(report(p,pre) for p in a)+'</section>' if a else ''

extra=load('project-stories.json');existing=load('blog.json');posts=extra+[p for p in existing if p['id'] not in {x['id'] for x in extra} and p['case']!='inav-fixed-wing']
# Retain all stories, with the current flying-wing and Ranger work at the front.
posts.sort(key=lambda p:0 if p['case']=='inav-fixed-wing' else 1 if p['case']=='vtol' else 2)
def story(post,pre,index=False):
 d=by[post['case']];ims=images(d,pre);parts=[]
 if d['id']=='delivery-drone':
  return delivery_narrative(ROOT,pre,3)+reports(d,pre)
 if ims:parts.append(image(ims[0],pre))
 for i,(heading,paragraph) in enumerate(post['sections']):
  parts.append('<section class="story-chapter"><h3>'+e(heading)+'</h3><p>'+e(paragraph)+'</p></section>')
  if i==0:parts.append(videos(d,pre,2 if index else None))
  if i==1 and len(ims)>1:parts.append('<div class="story-gallery">'+''.join(image(im,pre) for im in ims[1:3] if index)+('' if index else ''.join(image(im,pre) for im in ims[1:5]))+'</div>')
 parts.append(reports(d,pre,1 if index else None))
 return ''.join(parts)
entries=[]
for post in posts:
 d=by[post['case']];entries.append('<article class="blog-card journal-entry immersive-story" data-story data-search="'+e(post['title']+' '+post['intro']+' '+d['title'])+'"><header class="story-heading"><p class="kicker">Engineering field notes · '+e(d['title'])+'</p><h2><a href="'+e(post['id'])+'/">'+e(post['title'])+'</a></h2><p class="story-deck">'+e(post['intro'])+'</p></header>'+story(post,'../',True)+'<div class="links"><a href="'+post['id']+'/">Full story and all media →</a><a href="../projects/'+d['id']+'/">Project record →</a></div></article>')
 out=D/'blog'/post['id'];out.mkdir(exist_ok=True);body='<main id="main" class="wrap story-page"><header class="article-head"><p class="breadcrumb"><a href="../">Blog</a> / Engineering field note</p><h1>'+e(post['title'])+'</h1><p class="lead">'+e(post['intro'])+'</p><p class="blog-meta">Achraf RAHIBE · Project retrospective</p></header><article class="immersive-story">'+story(post,'../../')+'<section class="scope"><h2>Project record</h2><p>'+e(d['scope'])+'</p></section><div class="links"><a href="../../projects/'+d['id']+'/">Project record →</a><a href="../">All stories →</a></div></article></main>';(out/'index.html').write_text(page(post['title'],body,'../../'),encoding='utf8')
body='<main id="main" class="wrap"><header class="blog-head"><h1>Blog</h1><p>Aircraft builds, difficult behaviours and the engineering behind the next test.</p></header><section class="journal-controls"><label for="story-search">Find a story</label><input id="story-search" type="search" placeholder="Search aircraft, tests or tools"><p id="story-count">'+str(len(posts))+' project stories</p></section>'+''.join(entries)+'<p id="story-empty" hidden>No matching stories.</p></main>';(D/'blog/index.html').write_text(page('Blog',body,'../'),encoding='utf8')
# Make report previews visible directly in each project. Existing document-library pages already show their report pages.
for d in projects:
 path=D/'projects'/d['id']/'index.html'
 if not path.exists():continue
 t=path.read_text(encoding='utf8');block=reports(d,'../../')
 if d['id'] in {'fpv-10','multirotor','cube-vtol'}:block=videos(d,'../../')+block
 if block:t=t.replace('<div class="next">','<section class="section inline-evidence" id="inline-documents">'+block+'</section><div class="next">',1)
 t=t.replace('Clips are muted web excerpts; originals remain in the private project archive.','Original field audio is retained in the selected web excerpts. Originals remain in the private project archive.')
 t=t.replace('</head>','<link rel="stylesheet" href="../../assets/story-journal.css?v=20261106-local"></head>');path.write_text(t,encoding='utf8')
# Promote Ranger to a full project card without substituting a photograph of another aircraft.
d=by['inav-fixed-wing'];card='<article class="project showcase-card" data-project data-domain="air" data-search="Ranger INAV yaw fixed wing Blackbox"><a href="{pre}projects/inav-fixed-wing/"><div class="cover report-cover"><img src="{pre}'+e(paper_by['inav-fixed-wing']['images'][0])+'" alt="Ranger yaw investigation: report page, not an aircraft photograph" loading="lazy"></div><div class="project-body"><p class="meta">UAV &amp; UAS · Client support</p><h3>Volantex Ranger: INAV yaw troubleshooting</h3><p class="summary">From persistent right yaw to an aircraft-specific diagnosis, corrective checks and Blackbox guidance.</p><span class="more">Explore this project →</span></div></a></article>'
for path,pre in [(D/'index.html',''),(D/'projects/index.html','../')]:
 t=path.read_text(encoding='utf8');anchor='<div class="project-grid">';start=t.index('id="projects"') if path==D/'index.html' else t.index('id="result-count"');i=t.index(anchor,start)+len(anchor);t=t[:i]+card.replace('{pre}',pre)+t[i:];path.write_text(t,encoding='utf8')
css='''
.immersive-story{max-width:1050px;margin-inline:auto}.story-heading{padding:8px 0 22px}.story-heading h2{font:clamp(28px,3vw,40px)/1.22 Georgia,serif;margin:12px 0 20px}.story-heading h2 a{color:var(--ink);text-decoration:none}.story-deck{font-size:18px;color:var(--muted);max-width:850px}.story-photo{margin:25px 0 32px}.story-photo img{display:block;width:100%;max-height:560px;object-fit:contain;background:var(--bg)}.story-photo figcaption,.story-video-grid figcaption,.report-page figcaption{font-size:12px;line-height:1.6;color:var(--muted);padding-top:12px}.story-chapter{max-width:820px;margin:32px auto}.story-chapter h3{font-size:23px;font-weight:500;margin:0 0 12px}.story-chapter p{font-size:16px;line-height:1.95;color:var(--muted);margin:0}.story-gallery,.story-video-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}.story-gallery .story-photo{margin:10px 0}.story-video-grid figure{margin:0}.story-video-grid video{width:100%;aspect-ratio:auto;max-height:520px;object-fit:contain;background:#111;display:block}.story-video-grid strong,.story-video-grid span{display:block}.story-recordings,.story-reports{border-top:1px solid var(--line);padding-top:25px;margin:40px 0}.story-recordings>h3,.story-reports>h3{font-size:22px;font-weight:500}.story-report{background:var(--card);border:1px solid var(--line);padding:24px;margin:25px 0}.report-heading h3{font-size:23px;margin:12px 0}.report-heading p,.report-scope{color:var(--muted);font-size:14px}.report-page{margin:24px 0}.report-page img{display:block;width:100%;max-height:650px;object-fit:contain;background:#fff}.pdf-inline{border-top:1px solid var(--line);padding-top:16px}.pdf-inline summary{cursor:pointer;color:var(--accent);font-size:14px}.pdf-inline iframe{display:block;width:100%;height:640px;border:0;background:white;margin-top:18px}.story-page{max-width:1120px}.story-page .article-head{padding-bottom:20px}.immersive-story .links{flex-wrap:wrap}.report-cover img{object-fit:contain!important;background:#e9ecef}.journal-entry{margin-bottom:65px}.story-gallery:empty{display:none}@media(max-width:700px){.story-gallery,.story-video-grid{grid-template-columns:1fr}.story-report{padding:16px}.pdf-inline iframe{height:440px}.story-chapter{margin:25px 0}.story-chapter p{font-size:15px}.story-heading h2{font-size:29px}.story-deck{font-size:16px}}
''';(D/'assets/story-journal.css').write_text(css,encoding='utf8')
print('Rich journal:',len(posts),'stories with inline evidence; Ranger promoted on home and Projects.')



# Keep machine-readable showcase metadata consistent with the promoted Ranger card.
sf=ROOT/'content/showcase.json';meta=json.loads(sf.read_text(encoding='utf8'));meta['main_projects']=list(dict.fromkeys(['inav-fixed-wing']+meta['main_projects']));meta['titles']['inav-fixed-wing']='Volantex Ranger: INAV yaw troubleshooting';meta['story_count']=len(posts);sf.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
pp=D/'projects/index.html';t=pp.read_text(encoding='utf8');t=re.sub(r'<a class="support-record" href="inav-fixed-wing/">.*?</a>','',t,flags=re.S);pp.write_text(t,encoding='utf8')

# Promote the current simulation and Cobra entries as separate visible projects.
for path,pre in [(D/'index.html',''),(D/'projects/index.html','../')]:
 t=path.read_text(encoding='utf8');start=t.index('id="projects"') if path==D/'index.html' else t.index('id="result-count"');anchor='<div class="project-grid">';i=t.index(anchor,start)+len(anchor);cards=[]
 for id in ['multirotor-simulation','cobra-vtol']:
  d=by[id];cards.append('<article class="project showcase-card" data-project data-domain="air" data-search="'+e(d['title']+' '+' '.join(d['tags']))+'"><a href="'+pre+'projects/'+id+'/"><div class="cover"><img src="'+pre+e(d['image'])+'" alt="'+e(d['caption'])+'" loading="lazy"></div><div class="project-body"><p class="meta">'+e(d['category'])+'</p><h3>'+e(d['title'])+'</h3><p class="summary">'+e(d['problem'])+'</p><span class="more">Explore this project →</span></div></a></article>')
  t=re.sub(r'<a class="support-record" href="'+id+'/">.*?</a>','',t,flags=re.S)
 t=t[:i]+''.join(cards)+t[i:];path.write_text(t,encoding='utf8')
for d in projects:
 if not d.get('related_projects'):continue
 f=D/'projects'/d['id']/'index.html';t=f.read_text(encoding='utf8');block='<section class="section"><h2>Connected work</h2><div class="links">'+''.join('<a href="../'+id+'/">'+e(by[id]['title'])+' →</a>' for id in d['related_projects'])+'</div></section>';t=t.replace('<div class="next">',block+'<div class="next">',1);f.write_text(t,encoding='utf8')
meta=json.loads(sf.read_text(encoding='utf8'));meta['main_projects']=list(dict.fromkeys(['multirotor-simulation','cobra-vtol']+meta['main_projects']));meta['titles'].update({id:by[id]['title'] for id in ['multirotor-simulation','cobra-vtol']});sf.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
