from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent;D=ROOT/'docs'
mark=(D/'assets/achraf-rahibe-mark.svg').read_text(encoding='utf-8')
mark=mark.replace('aria-labelledby="ar-title"','aria-hidden="true" focusable="false"').replace('<title id="ar-title">Achraf RAHIBE monogram</title>','')
for p in D.rglob('*.html'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'<a class="brand" href="([^"]*)">.*?</a>',lambda m:'<a class="brand personal-brand" href="'+m.group(1)+'" aria-label="Achraf RAHIBE, home">'+mark+'</a>',s,count=1)
 depth=len(p.relative_to(D).parts)-1;pre='../'*depth
 if 'assets/favicon.svg' not in s:s=s.replace('</head>','<link rel="icon" type="image/svg+xml" href="'+pre+'assets/favicon.svg"></head>')
 s=s.replace('</head>','<style>.personal-brand{display:inline-flex;align-items:center;justify-content:center;min-width:62px;line-height:1}.personal-brand svg{display:block;width:62px;height:38px;overflow:visible}.personal-brand .ar-body{fill:var(--ink)}.personal-brand .ar-wing,.personal-brand .ar-bridge{fill:#87bde8}.personal-brand:hover svg{filter:drop-shadow(0 0 5px #87bde833)}</style></head>') if '.personal-brand svg{' not in s else s
 p.write_text(s,encoding='utf-8')
print('Applied custom AR wing monogram to every portfolio header and added matching favicon.')
