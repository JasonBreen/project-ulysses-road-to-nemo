"""One-time review capture; refuses to replace an existing preservation record."""
import hashlib,json,sys,subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from event_picture_fit.audit import MOD,controls
from usea_expansion.script import parse,get

HERE=Path(__file__).resolve().parent
target=HERE/'contract.json'
if target.exists():raise SystemExit('Refusing to recapture the original fit/provenance contract')
def sha(path):
    raw=path.read_bytes()
    if path.suffix in ('.py','.txt','.gui','.gfx','.json','.md'):raw=raw.replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()
originals={}
for relative in ('tools/reconstruction/source','tools/superpowers/source','source/artwork/fato_south_belka',
 'tools/anea/sources','tools/squadrons/sources','mod/2985041246/gfx/event_pictures',
 'mod/2985041246/gfx/AC_anea/events','mod/2985041246/gfx/AC_squadrons'):
    for p in (ROOT/relative).rglob('*'):
        if p.is_file():originals[p.relative_to(ROOT).as_posix()]=sha(p)
masters=[]
for manifest in ('tools/reconstruction/assets.json','tools/superpowers/assets.json','tools/fato_south_belka/assets.json'):
    for row in json.loads((ROOT/manifest).read_text())['assets']:
        if row['role'] not in ('event illustration','original narrative illustration'):continue
        p=MOD/row['file']
        with Image.open(p) as image:
            masters.append(dict(file=row['file'],sprite=row['sprite'],source=row.get('master',row.get('source')),
                old_size=list(image.size),old_sha256=sha(p),old_rgba_sha256=hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()))
assert len(masters)==40
event_sources={r:(MOD/r).read_text(encoding='utf-8-sig') for r in ('events/ac_anea.txt','events/ac_ucw.txt')}
military={}
for family,key,count in [('land_program','protected_sources_sha256',1050),('air_program','sources',1107),('naval_program','sources',1110)]:
    p=ROOT/'tools'/family/'preserved_sources.json';data=json.loads(p.read_text());assert len(data[key])==count
    overlap=[name for name in data[key] if name.removeprefix('mod/2985041246/') in event_sources]
    assert not overlap
    military[p.relative_to(ROOT).as_posix()]=dict(sha256=sha(p),protected_count=count,changed_event_overlap=overlap)
primary_root=Path(r'G:\steamlbirary\steamapps\common\Hearts of Iron IV')
primary={}
for family,filename in [('country_event','report_event_001.dds'),('news_event','news_event_001.dds')]:
    p=primary_root/'gfx/event_pictures'/filename
    with Image.open(p) as image:size=list(image.size)
    primary[family]=dict(path='gfx/event_pictures/'+filename,width=size[0],height=size[1],sha256=sha(p))
primary['gui']=dict(path='interface/eventwindow.gui',sha256=sha(primary_root/'interface/eventwindow.gui'))
launcher=json.loads((primary_root/'launcher-settings.json').read_text())
primary['version_source']=dict(path='launcher-settings.json',sha256=sha(primary_root/'launcher-settings.json'),rawVersion=launcher['rawVersion'])
focus=json.loads(subprocess.check_output(['git','show','a85d783038e113a3ee8fec8c6a4dea9a2e22b143:tools/anea/focus_art.json'],cwd=ROOT))
record=dict(schema=1,base_commit='a85d783038e113a3ee8fec8c6a4dea9a2e22b143',
    scope='Event fit only; inherited masters, country art and military captures remain protected; no native acceptance',
    primary_reference_version=launcher['rawVersion'],primary=primary,controls=controls(),
    protected_gui_sha256=sha(MOD/'interface/eventwindow.gui'),protected_sources=originals,
    military_captures=military,country_repairs=masters,original_event_sources=event_sources,
    original_anea_focus_sha256={r['asset']:r['sha256'] for r in focus})
target.write_bytes((json.dumps(record,indent=2)+'\n').encode());print('Captured40 prior country bindings;',len(originals),'protected original files; all3 military maps exclude the2 changed event files.')
