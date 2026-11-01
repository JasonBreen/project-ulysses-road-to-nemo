"""Original SP96 briefing artwork; deterministic DDS and editable PNG masters.

Uses only the original repository glyph library and shipped briefing bitmap
glyphs for gallery labels. No engine/DLC/remote pixels, text or portraits.
"""
import argparse
import base64
from collections import Counter
import hashlib
import html
import io
import json
from pathlib import Path
import sys

import PIL
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from superpowers.content import BRANCHES,focus_id
from superpowers.mechanics import COUNTRIES,SERVICES,SUBJECTS
from superpowers.build import output,bid
from reconstruction.build_art import BitmapFont,glyphs
from usea_expansion.script import parse,get

NAVY=(8,22,33,255);LIGHT=(222,238,243,255);GOLD=(190,166,104,255);GRID=(20,43,57,255)
ACCENT={'OSE':(98,207,234,255),'YUK':(111,197,207,255)}
STAGES=('document','civil','command','communications','scales','peace')
LAYOUTS=[((25,24,116,119),(133,45,38,45),(128,119,39,44)),
 ((23,40,106,111),(130,28,42,48),(129,119,40,43)),
 ((49,22,111,115),(23,121,44,44),(125,125,42,39)),
 ((27,26,113,110),(132,45,38,44),(118,120,48,43)),
 ((47,43,112,108),(23,24,43,45),(24,124,44,41)),
 ((35,24,115,113),(131,47,38,42),(76,130,39,36))]


def encode(image,kind='DDS'):
    buffer=io.BytesIO();image.save(buffer,format=kind);return buffer.getvalue()


def source_digest(name):
    data=(ROOT/name).read_bytes()
    if Path(name).suffix in('.py','.fnt'):data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()


def frame(tag,settled=False):
    image=Image.new('RGBA',(192,192));d=ImageDraw.Draw(image);color=ACCENT[tag]
    shape=([(28,13),(164,13),(179,29),(173,147),(146,177),(46,177),(19,147),(13,29)]if tag=='OSE'else
           [(23,19),(169,19),(180,31),(180,158),(159,177),(33,177),(12,158),(12,31)])
    d.polygon(shape,fill=NAVY);d.line(shape+[shape[0]],fill=color,width=3)
    if tag=='OSE':
        d.line((30,145,49,162,67,162),fill=GRID,width=3);d.line((125,162,143,162,162,145),fill=GRID,width=3)
    else:
        d.line((30,164,62,164),fill=GRID,width=2);d.line((30,169,62,169),fill=GRID,width=2)
        d.line((131,164,163,164),fill=GRID,width=2);d.line((131,169,163,169),fill=GRID,width=2)
    if settled:d.line((47,179,145,179),fill=GOLD,width=3);d.polygon(((91,175),(96,170),(101,175),(96,180)),fill=GOLD)
    return image


def composition(tag,primary,secondary,stage=0,settled=False,domestic=False):
    image=frame(tag,settled);a,b,c=LAYOUTS[stage%6]
    glyphs.glyph(image,primary,a,LIGHT);glyphs.glyph(image,secondary,b,ACCENT[tag]);glyphs.glyph(image,'civil'if domestic else STAGES[stage%6],c,ACCENT[tag])
    if domestic:
        d=ImageDraw.Draw(image);d.line((59,182,133,182),fill=ACCENT[tag],width=2)
    return image


def row_icon(tag,subject,cancel=False,protected=False):
    image=Image.new('RGBA',(104,116));d=ImageDraw.Draw(image);color=ACCENT[tag]
    d.rounded_rectangle((5,5,98,110),radius=9,fill=NAVY,outline=color,width=5)
    glyphs.glyph(image,subject,(19,20,67,73),LIGHT)
    if protected:d.line((26,101,78,101),fill=color,width=4)
    if cancel:d.line((22,95,81,25),fill=GOLD,width=7)
    return image.resize((26,29),Image.Resampling.LANCZOS)


def event_image(tag,primary,secondary):
    image=Image.new('RGBA',(640,260),NAVY);d=ImageDraw.Draw(image);color=ACCENT[tag]
    d.rounded_rectangle((8,8,631,251),radius=8,outline=color,width=3)
    for x in range(32,625,24):d.line((x,25,x,235),fill=GRID,width=1)
    for y in range(35,240,24):d.line((25,y,615,y),fill=GRID,width=1)
    glyphs.glyph(image,primary,(52,38,155,165),LIGHT);glyphs.glyph(image,secondary,(430,43,146,153),color)
    d.line((220,105,330,105,330,158,410,158),fill=color,width=3)
    d.polygon(((410,158),(398,152),(398,164)),fill=color)
    glyphs.glyph(image,'document',(273,36,65,68),LIGHT)
    d.line((37,220,603,220),fill=GRID,width=2)
    if tag=='OSE':
        for x in(238,284,330):d.rectangle((x,193,x+28,206),outline=color,width=2)
    else:
        d.line((247,188,247,211,365,211,365,188),fill=color,width=3);d.line((306,188,306,211),fill=color,width=2)
    return image


def outputs():
    if PIL.__version__!='11.3.0':raise SystemExit('Reproducible artwork requires Pillow11.3.0; current '+PIL.__version__)
    result={};assets=[];sprites=[];previews=[];content=output()
    branches={bid(b):b for b in BRANCHES};services={s.id:s for s in SERVICES}
    def texture(relative,image,sprite,role,tag,**metadata):
        data=encode(image);result[MOD/relative]=data;low,high=image.getchannel('A').getextrema()
        assets.append(dict(file=relative,sprite=sprite,role=role,tag=tag,width=image.width,height=image.height,frames=1,frame_width=image.width,
             alpha_min=low,alpha_max=high,format='DDS RGBA8',sha256=hashlib.sha256(data).hexdigest(),source_layer='original procedural briefing composition',**metadata))
        sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+relative+'" }');previews.append((role,metadata.get('title',sprite),image))
    for b in BRANCHES:
        for i in range(6):
            ident=focus_id(b,i);primary,secondary=SUBJECTS[b.key];master=composition(b.tag,primary,secondary,i,settled=i==5)
            source=f'tools/superpowers/source/focus/{ident}.png';result[ROOT/source]=encode(master,'PNG')
            relative=f'gfx/AC_superpowers/focus/{ident}.dds';sprite='GFX_ac_snp_focus_'+ident
            texture(relative,master.resize((96,96),Image.Resampling.LANCZOS),sprite,'focus',b.tag,id=ident,title=b.titles[i],primary=primary,secondary=secondary,stage=i,art_direction=list(b.motifs),master=source)
            sprites.append('spriteType = { name = "'+sprite+'_shine" texturefile = "'+relative+'" }')
    focus=[a for a in assets if a['role']=='focus']
    if len(focus)!=96 or len({a['sha256']for a in focus})!=96:raise ValueError('All96 focus compositions must be distinct')
    ideas=get(get(parse(content['common/ideas/ac_superpower_programmes.txt']),'ideas'),'country')
    for ident,_,node in ideas:
        tag='OSE'if ident.startswith(('OSE_','ac_snp_ose_'))else'YUK'
        b=next((b for key,b in branches.items()if ident.startswith(key+'_')),None)
        if b:
            primary,secondary=SUBJECTS[b.key]
            if '_civil_policy'in ident:stage=1
            elif '_protected_policy'in ident:stage=2
            else:stage=0 if '_service_1_'in ident else 3
        else:
            primary,secondary=('assembly','command')if tag=='OSE'else('economy','assembly')
            stage=1 if'_civil'in ident or'_public'in ident else 2
        image=composition(tag,primary,secondary,stage,settled=ident.endswith('_settled'),domestic='_domestic_'in ident).resize((75,75),Image.Resampling.LANCZOS)
        texture(f'gfx/AC_superpowers/ideas/{ident}.dds',image,'GFX_idea_'+ident,'idea',tag,id=ident,primary=primary,secondary=secondary)
    for tag in COUNTRIES:
        subjects=('assembly','document')if tag=='OSE'else('economy','command')
        image=composition(tag,*subjects,stage=4).resize((100,100),Image.Resampling.LANCZOS)
        texture(f'gfx/AC_superpowers/categories/{tag.lower()}.dds',image,'GFX_ac_snp_category_'+tag.lower(),'category',tag,title=COUNTRIES[tag])
    for category,_,entries in parse(content['common/decisions/ac_superpower_programmes.txt']):
        tag='OSE'if'_ose_'in category else'YUK'
        for ident,_,node in entries:
            service=services.get(ident.removesuffix('_cancel'))
            subject=SUBJECTS[service.branch.key][0]if service else'civil'if'civil'in ident or'public'in ident else'command'
            image=row_icon(tag,subject,cancel=ident.endswith('_cancel'),protected=bool(service and service.index==1))
            texture(f'gfx/AC_superpowers/decisions/{ident}.dds',image,'GFX_decision_'+get(node,'icon'),'decision row',tag,id=ident)
    for tag,name in COUNTRIES.items():
        subjects=('assembly','document')if tag=='OSE'else('economy','command');image=event_image(tag,*subjects);ident=tag.lower()+'_national';source=f'tools/superpowers/source/events/{ident}.png'
        result[ROOT/source]=encode(image,'PNG');texture(f'gfx/AC_superpowers/events/{ident}.dds',image,'GFX_ac_snp_event_'+ident,'event illustration',tag,title=name+': National Register',master=source)
    for b in BRANCHES:
        ident=bid(b);image=event_image(b.tag,*SUBJECTS[b.key]);source=f'tools/superpowers/source/events/{ident}.png';result[ROOT/source]=encode(image,'PNG')
        texture(f'gfx/AC_superpowers/events/{ident}.dds',image,'GFX_ac_snp_event_'+ident,'event illustration',b.tag,title=b.titles[0],master=source)
    result[MOD/'interface/ac_superpower_programmes.gfx']=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
    sources=['tools/superpowers/build_art.py','tools/superpowers/mechanics.py','tools/superpowers/content.py','tools/superpowers/build.py','tools/superpowers/narrative.py','tools/reconstruction/build_art.py','tools/usea_expansion/build_art.py',
             'mod/2985041246/gfx/fonts/ACBriefing16.fnt','mod/2985041246/gfx/fonts/ACBriefing16.dds']
    manifest=dict(schema=1,pillow='11.3.0',source_layer='Original procedural artwork; abstract programme framing, not official national crests',
        source_hashes={p:source_digest(p)for p in sources},
        source_hash_normalization='Python and FNT text use CRLF-normalized LF bytes; DDS dependencies and delivered textures retain raw byte hashes.',
        framing='Navy/cyan national structures; branch subject pairs plus stage subject; restrained gold settlement highlight; transparent icon corners.',
        native='Not rendered in HOI4; native viewport and input acceptance pending',assets=assets)
    result[HERE/'assets.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    profile=dict(schema=1,name='SP96 original resources only; explicit base-only source scenario, not active-DLC or full-conversion acceptance',
        enabled_dlc=[],provider_overrides=[],payload_overrides=[],provenance=[dict(path=a['file'],provider='mod',sha256=a['sha256'],classification='authored',
         reason='Original procedural SP96 composition with retained vector compiler and editable masters; exact resource only.',
         evidence='tools/superpowers/assets.json; tools/superpowers/build_art.py; tools/superpowers/source/')for a in assets])
    result[HERE/'audit_profile.json']=(json.dumps(profile,indent=2)+'\n').encode()
    font=BitmapFont()
    for tag,name in COUNTRIES.items():
        country=[b for b in BRANCHES if b.tag==tag]
        for phase,branches_in_sheet in(('foundation',country[:4]),('continuation',country[4:])):
            image=Image.new('RGBA',(1120,950),NAVY);font.draw(image,name+': '+phase.title()+' Programmes',(24,18),1050)
            for row,b in enumerate(branches_in_sheet):
                for i in range(6):
                    x=25+i*183;y=62+row*220;data=result[MOD/f'gfx/AC_superpowers/focus/{focus_id(b,i)}.dds']
                    image.alpha_composite(Image.open(io.BytesIO(data)).convert('RGBA'),(x+25,y));font.draw(image,b.titles[i],(x,y+110),153)
            result[HERE/'gallery'/f'{tag.lower()}-{phase}.png']=encode(image,'PNG')
    cards=[]
    for role,title,image in previews:
        uri=base64.b64encode(encode(image,'PNG')).decode();cards.append('<figure><img alt="" src="data:image/png;base64,'+uri+'"><figcaption>'+html.escape(role+': '+title)+'</figcaption></figure>')
    page='<!doctype html><meta charset="utf-8"><title>Original superpower programme artwork</title><style>body{background:#081621;color:#deedf3;font:16px sans-serif;margin:28px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:18px}figure{margin:0;padding:16px;border:1px solid #34596b}img{max-width:100%;height:110px;object-fit:contain;display:block;margin:auto}figcaption{margin-top:14px;line-height:1.4}</style><h1>National programme artwork</h1><p>Original procedural briefing compositions, source masters and byte-pinned DDS textures. No native HOI4 rendering acceptance.</p><main>'+''.join(cards)+'</main>'
    result[HERE/'gallery/index.html']=page.encode()
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();bad=[];result=outputs()
    for path,data in result.items():
        if a.check:
            if not path.exists()or path.read_bytes()!=data:bad.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Superpower artwork differs: '+', '.join(bad))
    print('SP96 original artwork:',sum(p.suffix=='.dds'for p in result),'DDS; '+('consistent'if a.check else'generated'))

if __name__=='__main__':main()
