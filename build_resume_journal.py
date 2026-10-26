# Resume and build-journal presentation; uses only the owner's verified profile.
r=json.loads((ROOT/'content/resume.json').read_text(encoding='utf-8'))
home=(D/'index.html').read_text(encoding='utf-8')
old_start=home.index('<section class="section" id="resume">')
old_end=home.index('</main>',old_start)
old_resume=home[old_start:old_end]
education=old_resume[old_resume.index('<h4>Education</h4>'):old_resume.index('<h4>Experience</h4>')]
experience=''.join('<div class="resume-block"><div class="resume-line"><strong>'+e(row['title'])+'</strong><span>'+e(row['dates'])+'</span></div><p class="org">'+e(row['company'])+'</p><ul>'+''.join('<li>'+e(b)+'</li>' for b in row['bullets'])+'</ul></div>' for row in r['experience'])
project_entries=''.join('<div class="resume-block"><div class="resume-line"><strong>'+e(project['title'])+'</strong></div><p class="resume-tools">'+e(project['tools'])+'</p><ul>'+''.join('<li>'+e(b)+'</li>' for b in project['bullets'])+'</ul></div>' for project in r['projects'])
tech=''.join('<p><strong>'+e(label)+':</strong> '+e(body)+'</p>' for label,body in r['skills'])
resume_html='<section class="section" id="resume"><h2 class="resume-title">Resume</h2><div class="resume-sheet"><div class="resume-header"><h3>Achraf RAHIBE</h3><a class="btn" href="Achraf_Rahibe_CV.pdf" download>Download one-page CV ↓</a></div><p class="resume-role">UAV &amp; Avionics Systems Engineer</p><div class="resume-contact"><a href="tel:+212620323768">+212 620 323 768</a><a href="mailto:achrafrahibpro@gmail.com">achrafrahibpro@gmail.com</a><a href="https://www.linkedin.com/in/achraf-rahib1">LinkedIn</a><a href="projects/">Engineering projects</a></div>'+education+'<h4>Professional experience</h4>'+experience+'<h4>Engineering projects</h4>'+project_entries+'<h4>Technical skills</h4><div class="resume-skills">'+tech+'<p><strong>Languages:</strong> Arabic native, English and French fluent, German basic.</p></div></div></section>'
home=home[:old_start]+resume_html+home[old_end:]
groups=[
 ('CAD & Simulation',[('Onshape','Parametric CAD','layers'),('AutoCAD Electrical','Electrical documentation','layers'),('Gazebo / SITL','Aircraft mission simulation','plane'),('Gmsh','Mesh preparation','layers')]),
 ('Manufacturing',[('3D printing','FDM airframe parts','tool'),('CNC preparation','Part files and workshop guides','tool'),('Build planning','BOMs, tooling and assembly','file')]),
 ('Electronics & Embedded',[('STM32 / ESP32 / Arduino','Embedded platforms','chip'),('Raspberry Pi','Companion-computer interfaces','chip'),('Jetson Nano / Orin Nano','Embedded compute','chip'),('KiCad / Altium','PCB review and integration familiarity','chip'),('CAN / UART / SPI / I2C','System communications','radio'),('ESC / VESC / BMS','Power and motor interfaces','battery')]),
 ('Programming & Robotics',[('C / C++','Embedded development','code'),('Python','Analysis and scripting','code'),('Linux','Embedded workflows','chip'),('Git','Version control','code'),('ArduPilot / PX4 / INAV','Autopilot configuration','plane'),('Mission Planner / QGC','Missions, logs and tuning','chart')]),
 ('Vision & Automation',[('YOLOv8 / ByteTrack','Detection and tracking workflows','code'),('RTSP / GStreamer','Video transport','radio'),('A8C gimbal camera','USV first-person video','chip'),('Siemens PLCs','TIA Portal and WinCC','tool')]),
 ('Design & Communication',[('Photoshop','Photo editing','ps'),('Illustrator','Vector graphics','ai'),('Technical writing','Engineering and service documentation','file')])]
new_skills='<section class="section skills-band" id="skills"><div class="section-title"><h2>Skills</h2></div><div class="skills">'+''.join('<div><h3>'+e(title)+'</h3><div class="skill-items">'+''.join(skill(*x) for x in items)+'</div></div>' for title,items in groups)+'</div></section>'
a=home.index('<section class="section skills-band"');b=home.index('<section class="section" id="resume">',a)
home=home[:a]+new_skills+home[b:]
home=home.replace('surface vessels. My work','unmanned surface vehicles. My work')
(D/'index.html').write_text(home,encoding='utf-8')
# A visual, first-person build journal with the update itself readable inline.
parents={m:g for g in json.loads((ROOT/'content/collections.json').read_text(encoding='utf-8')) for m in g['members']}
ordered=sorted(posts,key=lambda p:0 if p['case']=='usv' else 1)
entries=[]
for post in ordered:
 d=next(x for x in data if x['id']==post['case']);image_src='';caption=''
 if d.get('reference_images'):
  image_src=d['reference_images'][0]['src'];caption=d['reference_images'][0]['caption']
 elif d.get('photo_verified'):
  image_src=d['image'];caption=d['caption']
 elif d.get('work_samples'):
  image_src=d['work_samples'][0]['src'];caption=d['work_samples'][0]['caption']
 visual='<figure class="blog-image"><img src="../'+e(image_src)+'" alt="'+e(caption)+'" loading="lazy"></figure>' if image_src else ''
 copy=''.join('<p>'+e(paragraph)+'</p>' for heading,paragraph in post['sections'][:2])
 parent=parents[d['id']]
 entries.append('<article class="blog-card journal-entry"><div class="blog-heading"><h2>'+e(post['title'])+'</h2><time datetime="2026-10-26">26 October 2026</time></div><p class="journal-deck">'+e(post['intro'])+'</p>'+visual+'<div class="journal-copy">'+copy+'</div><p class="blog-meta">Project retrospective</p><div class="links"><a href="../projects/'+parent['id']+'/#'+d['id']+'">View the project →</a><a href="'+post['id']+'/">Read the full engineering note →</a></div></article>')
body='<main id="main" class="wrap"><header class="blog-head"><h1>Blog</h1><p>Build notes, integration work and field testing.</p></header>'+''.join(entries)+'</main>'
bp=D/'blog/index.html';bp.write_text(page('Blog',body,'../'),encoding='utf-8')
# The shared page helper uses the original navigation, so update this generated page.
s=bp.read_text(encoding='utf-8');s=s.replace('href="../index.html#about">About','href="../about/">About').replace('href="../Achraf_Rahibe_CV.pdf">Resume</a>','href="../index.html#resume">Resume</a>').replace('<a href="../technical-notes/">Documents</a>','<a href="../blog/">Blog</a><a href="../technical-notes/">Documents</a>',1);bp.write_text(s,encoding='utf-8')
with (A/'site.css').open('a',encoding='utf-8') as f:
 f.write('\n.resume-role{color:var(--muted);font-size:17px;margin:16px 0 0}.resume-block .resume-tools{color:var(--accent);font-size:13px;margin:8px 0}.journal-deck{font-size:16px;color:var(--accent);margin:0 0 25px}.journal-copy{max-width:900px}.journal-copy p{font-size:15px;line-height:1.9;color:var(--muted);margin:18px 0}.journal-entry .blog-heading h2{font-size:26px;line-height:1.35}.journal-entry .links{margin-bottom:0}.journal-entry .blog-image{height:440px}.skill-logo.brand-tile img{padding:0}.resume-line strong{max-width:75%}@media(max-width:700px){.journal-entry .blog-image{height:280px}.journal-entry .blog-heading h2{font-size:23px}.resume-line strong{max-width:100%}}\n')
print('Updated shared web resume, six skill categories and 14 illustrated journal entries.')
