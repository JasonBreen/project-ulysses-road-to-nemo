"""Expand the locked writer brief into exact generation prompts before calls."""
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / 'plan.json').read_text())
brief = (HERE / 'brief.md').read_text()
plan['assets'] = [a for a in plan['assets'] if a['file'].startswith('portraits/')]
scene_section = brief.split('## Sixteen concrete scene masters\n', 1)[1].split('## Two independent loading masters', 1)[0]
entries = re.split(r'(?m)^\d+\. ', scene_section.strip())[1:]
assert len(entries) == 16
chapters = {1:[1,2,6],2:[3,7,12,16],3:[4,8,13,17],4:[5,9,11,14,18],5:[10,15,19,20]}
ending_names = {6:'trusted',7:'compromised',8:'fractured'}
base = ('Use case: illustration-story. Create ONE original wide 16:9 painted-realistic aviation editorial illustration for an authored Strangereal supporting-cast story. '
        'Subtle visible painted texture, realistic practical interiors and natural skin/light, restrained navy/cyan cloth and architecture. '
        'Grounded everyday service work in an anonymous place, conventional 1991-2020 machinery, no recognizable aircraft type or Earth landmark. '
        'Make the important narrative subjects readable in the central 60 percent width and central 75 percent height for a later 200x160 event-card crop. '
        'Compose distinct depth and light, not a collage or game screenshot. Fill the whole frame; no borders, letterboxing or UI. ')
constraints = (' No readable text, lettering, numerals, pseudo-writing, insignia, badge, seal, logo, flag, watermark, signature, yellow stripe, yellow overlay, strategic weapon, '
               'airborne aircraft, battle, explosion, blood, grave, corpse, named national leader or established Ace Combat cameo. All papers, labels, boards, screens and clothing are unmarked. '
               'Do not assert a national victory, peace, defeat, surrender, occupation or compulsory historical outcome. Natural soft warm lamps are allowed; no artificial yellow graphic artifacts.')
casts = {
 'OSE': 'For these ending silhouettes show four experienced adults only from behind, heads turned away so no face is identifiable: a woman with short dark-brown hair in a plain dark-blue flight suit; a warm dark-brown-skinned man with short tightly curled black hair in slate clothing; a fair-skinned woman with short auburn hair in navy maintenance clothes; a medium-brown-skinned woman with a black low bun in a dark control-room shirt. Age-neutral adult silhouettes must fit conclusions after 2020. ',
 'YUK': 'For these ending silhouettes show four experienced adults only from behind, heads turned away so no face is identifiable: a light-skinned woman with jaw-length straight black hair in faded blue-grey flight clothing; a light-olive-skinned man with short dark-blond hair in charcoal flight clothing; a brown-skinned woman with short tight black curls in faded grey-blue work clothes; a warm light-brown-skinned man with dark wavy hair in a navy shirt. Age-neutral adult silhouettes must fit conclusions after 2020. '
}
for i, text in enumerate(entries):
    tag = 'OSE' if i < 8 else 'YUK'; slot = i % 8 + 1
    match = re.match(r'\*\*(.+?)\*\*\s*(.*)', text.strip(), re.S)
    title, subject = match.groups(); subject = re.sub(r'\s+', ' ', subject).strip()
    # Faces are deliberately hidden in all endings, so portrait identity is not improvised.
    if slot >= 6:
        subject = subject.replace('mostly from behind/three-quarter view', 'strictly from behind').replace('mostly from behind', 'strictly from behind')
        subject += ' ' + casts[tag] + 'Keep all faces obscured rather than creating younger faces or mixing identities.'
    asset_id = f'{tag.lower()}_scene_{slot}'
    plan['assets'].append(dict(id=asset_id, tag=tag, kind='original story narrative scene', file=f'scenes/{asset_id}.png',
        title=title, subject=subject, chapters=chapters.get(slot,[]), ending=ending_names.get(slot),
        prompt=base+'Scene: '+title+'. '+subject+constraints, transparent_background=False, generation_references=[], status='planned'))
loading_section = brief.split('## Two independent loading masters\n',1)[1]
entries = re.split(r'(?m)^- ', loading_section.strip())[1:]
assert len(entries) == 2
for tag,text in zip(('OSE','YUK'),entries):
    match = re.match(r'\*\*(.+?)\*\*\s*(.*)', text.strip(), re.S)
    title,subject = match.groups(); subject=re.sub(r'\s+',' ',subject).strip()
    asset_id = tag.lower()+'_loading'
    prompt = (base.replace('central 60 percent width and central 75 percent height for a later 200x160 event-card crop',
        'central 50 percent width and middle 55 percent height for a conservative 3440:1440 center-cover loading crop')+
        'This is a separately composed full-bleed cinematic loading-screen master, never a widened event crop. '
        'Keep whole important aircraft, vehicle and worker silhouettes inside the crop-safe middle height. '
        'Calm low-detail foreground/sky may carry later loading text, but paint no text now. '+title+'. '+subject+constraints)
    plan['assets'].append(dict(id=asset_id,tag=tag,kind='original independent loading screen',file=f'loading/{asset_id}.png',
        title=title,subject=subject,prompt=prompt,transparent_background=False,generation_references=[],status='planned'))
assert len(plan['assets']) == 26
(HERE/'plan.json').write_bytes((json.dumps(plan,indent=2)+'\n').encode())
for row in plan['assets']:
    target=HERE.parent/'sources'/row['file'];meta=target.with_suffix('.json')
    if not meta.exists():
        meta.parent.mkdir(parents=True,exist_ok=True)
        info={**row,'file':target.name,'source_layer':plan['source_layer'],'generator':'built-in image_gen','brief_sha256':plan['brief_sha256']}
        meta.write_bytes((json.dumps(info,indent=2)+'\n').encode())
print('Prepared',len(plan['assets']),'exact prompts; no images generated or overwritten.')
