"""Package reviewed font aliases using existing authored briefing atlases only."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/usea_expansion')]
from script import parse,get
from research_fonts.policy import BINDINGS

SOURCE=ROOT/'tools/land_program/source/research_base.gui'
PRIMARY=HERE/'primary_contract.json'


def digest(path, text=False):
    data=path.read_bytes()
    return hashlib.sha256(data.replace(b'\r\n',b'\n') if text else data).hexdigest()


def inventory(tree,path='gui'):
    rows=[]
    for index,(key,op,value)in enumerate(tree):
        if not isinstance(value,list):continue
        name=get(value,'name','').strip('"') if isinstance(get(value,'name',''),str)else''
        address=path+'/'+key+(':'+name if name else'')+'['+str(index)+']'
        for field,_,alias in value:
            if field.lower()in('font','buttonfont')and isinstance(alias,str):
                rows.append(dict(path=address,field=field,font=alias.strip('"'),name=name,
                    max_width=get(value,'maxWidth'),max_height=get(value,'maxHeight'),text=get(value,'text'),
                    fixed_size=get(value,'fixedsize'),format=get(value,'format')))
        rows.extend(inventory(value,address))
    return rows


def capture(reference):
    """Identifiers, metrics and hashes; never capture engine glyph pixels."""
    reference=Path(reference);core=reference/'interface/core.gfx'
    source=parse(core.read_text(encoding='utf-8-sig'));found={}
    def visit(nodes):
        for kind,_,body in nodes:
            if not isinstance(body,list):continue
            name=get(body,'name','').strip('"')
            if kind=='bitmapfont'and name in BINDINGS:
                if name in found:raise ValueError('Ambiguous primary default font '+name)
                value=get(body,'path');paths=[value.strip('"')]if value else[k.strip('"')for k,_,v in get(body,'fontfiles')]
                fnt=reference/(paths[0]+'.fnt');raw=fnt.read_text(encoding='utf-8-sig')
                metrics={k:int(v)for k,v in re.findall(r'(lineHeight|base|scaleW|scaleH)=(\d+)',raw)}
                codes={code:[int(k)for k,_,v in rgb]for code,_,rgb in get(body,'textcolors',[])}
                found[name]=dict(source='engine://interface/core.gfx',source_sha256=digest(core),
                    primary_paths=['engine://'+p for p in paths],primary_color=get(body,'color'),text_colors=codes,
                    metrics=metrics,metrics_source='engine://'+fnt.relative_to(reference).as_posix(),metrics_source_sha256=digest(fnt))
            else:visit(body)
    visit(source)
    if set(found)!=set(BINDINGS):raise ValueError('Primary font aliases missing: '+str(set(BINDINGS)-set(found)))
    report=dict(schema=1,version=json.loads((reference/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        coverage='Read-only primary default English font names, state-color values and metrics only; no glyph images or complete font files copied.',
        language='English. Installed Japanese/Russian/Polish overrides are not imported or claimed supported by this package.',fonts=found)
    PRIMARY.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')


def outputs():
    primary=json.loads(PRIMARY.read_text());fonts=[];records=[];atlases={}
    for old,binding in BINDINGS.items():
        fact=primary['fonts'][old]
        codes=' '.join(code+' = { '+' '.join(map(str,rgb))+' }'for code,rgb in fact['text_colors'].items())
        fonts.append('bitmapfont = { name = "'+binding.name+'" path = "gfx/fonts/'+binding.atlas+'" color = '+binding.color+' textcolors = { '+codes+' } }')
        records.append(dict(original=old,name=binding.name,atlas=binding.atlas,color=binding.color,
            primary_color=fact['primary_color'],text_colors=fact['text_colors'],purpose=binding.purpose))
        if binding.atlas not in atlases:
            fnt=MOD/'gfx/fonts'/(binding.atlas+'.fnt');dds=MOD/'gfx/fonts'/(binding.atlas+'.dds')
            text=fnt.read_text()
            with Image.open(dds)as image:size=image.size
            if re.search(r'page id=0 file="([^"]+)"',text)[1]!=dds.name:raise ValueError('Unresolved authored font atlas page '+binding.atlas)
            atlases[binding.atlas]=dict(fnt=fnt.relative_to(ROOT).as_posix(),fnt_normalized_sha256=digest(fnt,True),
                texture=dds.relative_to(ROOT).as_posix(),texture_raw_sha256=digest(dds),width=size[0],height=size[1],
                line_height=int(re.search(r'common lineHeight=(\d+)',text)[1]),glyphs=int(re.search(r'chars count=(\d+)',text)[1]),
                source='tools/usea_expansion/build_fonts.py; tools/usea_expansion/fonts.json; bundled DINish Regular OFL source',
                source_layer='Existing original mod-authored briefing atlas; no engine font pixels')
    manifest=dict(schema=1,source_layer='Reviewed original briefing font aliases; no new glyph pixels or global engine-alias overrides',
        captured_gui_normalized_sha256=digest(SOURCE,True),protected_1050_sources_manifest='tools/land_program/preserved_sources.json',
        original_font_assignments=len(inventory(parse(SOURCE.read_text()))),bindings=records,atlases=atlases,
        hash_normalization='FNT/source text normalizes CRLF to LF; DDS texture hashes remain raw.',native_acceptance=False)
    profile=dict(schema=1,name='Research-font resources only; explicit base-only scenario, not native DLC activation',
        enabled_dlc=[],provider_overrides=[],payload_overrides=[],provenance=[])
    for row in atlases.values():
        for key in('fnt','texture'):
            path=ROOT/row[key]
            profile['provenance'].append(dict(path=path.relative_to(MOD).as_posix(),provider='mod',sha256=digest(path),
                classification='authored',reason='Existing original DINish briefing atlas/metrics, reused without engine font pixels; exact file only.',
                evidence='tools/research_fonts/assets.json; tools/usea_expansion/build_fonts.py; tools/usea_expansion/fonts.json'))
    return {MOD/'interface/ac_research_fonts.gfx':('bitmapfonts = {\n'+'\n'.join(fonts)+'\n}\n').encode(),
            HERE/'assets.json':(json.dumps(manifest,indent=2)+'\n').encode(),
            HERE/'audit_profile.json':(json.dumps(profile,indent=2)+'\n').encode()}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture-reference',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.capture_reference:capture(a.capture_reference)
    for path,data in outputs().items():
        if a.check:
            if not path.exists()or path.read_bytes().replace(b'\r\n',b'\n')!=data:raise SystemExit('Stale research font binding: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Research fonts:12 reviewed aliases;301 captured assignments;2 existing authored atlases; '+('consistent'if a.check else'packaged'))
