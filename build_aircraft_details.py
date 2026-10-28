# Final, project-specific build details after the shared generators.
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parent;D=ROOT/'docs'
def esc(v):return html.escape(str(v),quote=True)
projects=json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
for id in ['fixed-wing','cube-vtol']:
 d=next(x for x in projects if x['id']==id);profile=d['build_profile'];rows=''.join('<div><dt>'+esc(k.replace('_',' ').title())+'</dt><dd>'+esc(v)+'</dd></div>' for k,v in profile.items())
 if id=='fixed-wing':
  text='Printed and assembled Titan Dynamics Tornado V2 airframes, integrating the twin-pusher propulsion, Pixhawk 6C, navigation and onboard wiring. The photographs below follow fabrication, assembly and avionics preparation.'
  note='ABS printing with 3% infill and one perimeter, selected to keep the airframe light while retaining practical rigidity for assembly and handling.'
 else:
  text='The four-lift-motor airframes shown here belong to the 4+1 VTOL development work. Workshop and field-preparation images are presented with the QuadPlane, separately from the two-motor Tornado fixed-wing aircraft.'
  note='The shown airframe builds use ABS, 3% infill and one perimeter.'
 block='<section class="section aircraft-build-details" id="build-details"><div class="section-title"><h2>Fabrication & aircraft integration</h2></div><p>'+esc(text)+'</p><dl class="build-specs">'+rows+'</dl><p class="caption">'+esc(note)+'</p></section>'
 path=D/'projects'/id/'index.html';s=path.read_text(encoding='utf-8');anchor='<section class="section"><div class="section-title"><h2>Project photographs</h2>'
 assert anchor in s,id;s=s.replace(anchor,block+anchor,1);s=s.replace('</head>','<style>.build-specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:20px;padding:24px 0;border-block:1px solid var(--line)}.build-specs dt{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--accent)}.build-specs dd{margin:7px 0 0;font-size:15px}.aircraft-build-details>p{color:var(--muted);max-width:850px}</style></head>');path.write_text(s,encoding='utf-8')
print('Added airframe-specific fabrication and integration details.')
