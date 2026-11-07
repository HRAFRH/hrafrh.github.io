# Shared delivery narrative, used by the project and blog so the account stays consistent.
import html,json
from pathlib import Path

def delivery_narrative(root,pre,heading=3):
 root=Path(root);record=json.loads((root/'content/delivery-story.json').read_text(encoding='utf8'));clips=json.loads((root/'content/story-media.json').read_text(encoding='utf8'))['delivery-drone'];pics={Path(x['src']).stem:x for x in record['pictures']}
 def esc(x):return html.escape(str(x).replace('\u2014',', ').replace('\u2013','-'),quote=True)
 def photos(keys):
  return '<div class="delivery-photo-grid">'+''.join('<figure><a href="'+pre+esc(pics[k]['src'])+'" target="_blank" rel="noopener"><img src="'+pre+esc(pics[k]['src'])+'" alt="'+esc(pics[k]['caption'])+'" loading="lazy"></a><figcaption><strong>'+esc(pics[k]['title'])+'</strong><span>'+esc(pics[k]['caption'].split('. ',1)[-1])+'</span></figcaption></figure>' for k in keys)+'</div>'
 def video(indices):
  return '<div class="delivery-video-grid">'+''.join('<figure><video controls playsinline controlslist="nodownload noremoteplayback" disablepictureinpicture preload="none" poster="'+pre+esc(clips[i]['poster'])+'"><source src="'+pre+esc(clips[i]['file'])+'" type="video/mp4">Your browser does not support inline video playback.</video><figcaption><strong>'+esc(clips[i]['title'])+'</strong><span>'+esc(clips[i]['caption'])+'</span></figcaption></figure>' for i in indices)+'</div>'
 body=[]
 for i,(title,text) in enumerate(record['sections']):
  body.append('<section class="delivery-chapter"><h'+str(heading)+'>'+esc(title)+'</h'+str(heading)+'><p>'+esc(text)+'</p>')
  if i==0:body.append(photos(['arabic-video-support','aircraft-ground'])+video([0]))
  if i==1:
   body.append('<dl class="delivery-specs">'+''.join('<div><dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd></div>' for k,v in record['specifications'])+'</dl>'+photos(['cuav-controller','siyi-ground-unit','siyi-rear'])+video([3,5]))
  if i==2:body.append(video([1,2]))
  if i==3:body.append(photos(['charger','battery-32ah','battery-20ah'])+video([4]))
  if i==4:body.append(photos(['mission-battery-chart']))
  if i==5:
   body.append('<div class="delivery-photo-grid"><figure><img src="'+pre+'media/delivery-drone/mission-profile.webp" alt="Location-free mission distance and altitude review" loading="lazy"><figcaption>Distance and altitude review from the matching long-distance mission.</figcaption></figure><figure><img src="'+pre+'media/delivery-drone/gripper-modes.webp" alt="Gripper commands and flight-mode sequence" loading="lazy"><figcaption>Logged release commands and flight modes. Commands do not directly measure payload mass.</figcaption></figure></div>')
  body.append('</section>')
 return '<div class="delivery-narrative">'+''.join(body)+'</div>'
