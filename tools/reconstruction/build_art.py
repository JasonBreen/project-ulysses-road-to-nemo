"""Reproducible original glyph compositions; no installed media or baked captions.

Focus masters, event masters and this vector compiler are editable sources.
All runtime row icons use the native26x29 aperture, separately from categories.
"""
import argparse
from collections import Counter
import base64
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

import PIL
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/usea_expansion')]
from reconstruction.content import BRANCHES,COUNTRY_NAMES,focus_id,branch_id
from reconstruction.build import outputs as content_outputs
from usea_expansion.script import parse,get
from event_picture_fit.fit import contain as fit_event
from event_picture_fit.bitmap import BitmapFont

LIBRARY=ROOT/'tools/usea_expansion/build_art.py'
spec=importlib.util.spec_from_file_location('reconstruction_original_glyphs',LIBRARY)
glyphs=importlib.util.module_from_spec(spec);spec.loader.exec_module(glyphs)
NAVY=(8,22,33,255);LIGHT=(222,238,243,255);EDGE=(43,78,99,255);GOLD=(194,165,97,255)
ACCENT={'NPT':(89,207,224,255),'REC':(112,199,186,255),'SAP':(137,192,230,255),'GEB':(115,188,208,255)}
THEMES={'NPT':('navy','radar'),'REC':('rebuild','document'),'SAP':('assembly','air'),'GEB':('gate','tools')}
ARRANGEMENTS=[((26,25,119,111),(126,112,45,46)),((23,40,93,109),(111,58,65,75)),
              ((55,26,110,113),(26,116,46,44)),((45,26,104,94),(65,122,66,42)),
              ((26,29,109,100),(110,102,61,59)),((41,76,111,84),(73,24,47,45))]


def encoded(image,kind='DDS'):
    output=io.BytesIO();image.save(output,format=kind);return output.getvalue()


def frame(tag,settled=False):
    image=Image.new('RGBA',(192,192));d=ImageDraw.Draw(image);a=ACCENT[tag]
    shapes={'NPT':[(28,14),(162,14),(178,40),(175,145),(147,175),(45,175),(15,145),(14,40)],
            'REC':[(26,18),(163,18),(179,33),(179,154),(157,175),(35,175),(14,154),(14,33)],
            'SAP':[(96,9),(173,39),(177,138),(151,172),(41,172),(15,138),(19,39)],
            'GEB':[(34,13),(158,13),(178,35),(178,151),(155,177),(37,177),(14,151),(14,35)]}
    shape=shapes[tag];d.polygon(shape,fill=NAVY);d.line(shape+[shape[0]],fill=a,width=3)
    if tag=='NPT':d.arc((35,131,157,178),0,180,fill=EDGE,width=2)
    elif tag=='REC':d.line((36,165,73,165),fill=EDGE,width=2);d.line((120,165,156,165),fill=EDGE,width=2)
    elif tag=='SAP':d.line((47,163,145,163),fill=EDGE,width=2)
    else:d.line((36,156,36,165,75,165),fill=EDGE,width=2);d.line((117,165,156,165,156,156),fill=EDGE,width=2)
    if settled:d.line((52,176,140,176),fill=GOLD,width=3);d.polygon([(87,172),(96,165),(105,172),(96,180)],fill=GOLD)
    return image


def composition(tag,primary,secondary,layout=0,settled=False):
    image=frame(tag,settled);a,b=ARRANGEMENTS[layout%len(ARRANGEMENTS)]
    glyphs.glyph(image,primary,a,LIGHT);glyphs.glyph(image,secondary,b,ACCENT[tag])
    return image


def row_icon(tag,subject,cancel=False):
    image=Image.new('RGBA',(104,116));d=ImageDraw.Draw(image)
    d.rounded_rectangle((5,5,98,110),radius=11,fill=NAVY,outline=ACCENT[tag],width=5)
    glyphs.glyph(image,subject,(18,19,68,75),LIGHT)
    if cancel:d.line((22,95,81,25),fill=GOLD,width=7)
    return image.resize((26,29),Image.Resampling.LANCZOS)


def event_image(tag,subjects):
    image=Image.new('RGBA',(640,260),NAVY);d=ImageDraw.Draw(image);a=ACCENT[tag]
    d.rounded_rectangle((8,8,631,251),radius=8,outline=a,width=3)
    for x in range(32,625,24):d.line((x,24,x,235),fill=(18,40,54,255),width=1)
    for y in range(34,240,24):d.line((25,y,615,y),fill=(18,40,54,255),width=1)
    d.line((35,218,606,218),fill=EDGE,width=2)
    glyphs.glyph(image,subjects[0],(70,32,187,169),LIGHT)
    glyphs.glyph(image,subjects[1],(361,55,149,145),a)
    d.line((272,128,338,128),fill=a,width=3);d.polygon([(338,128),(327,121),(327,135)],fill=a)
    d.line((70,232,257,232),fill=GOLD,width=2)
    return image


def outputs():
    if PIL.__version__!='11.3.0':raise SystemExit('Reproducible art requires Pillow11.3.0; current '+PIL.__version__)
    result={};assets=[];sprites=[];previews=[];used=Counter();by_branch={branch_id(b):b for b in BRANCHES}
    def texture(relative,image,sprite,role,tag,**metadata):
        data=encoded(image);result[MOD/relative]=data
        low,high=image.getchannel('A').getextrema()
        assets.append(dict(file=relative,sprite=sprite,role=role,tag=tag,width=image.width,height=image.height,
                           frames=1,frame_width=image.width,alpha_min=low,alpha_max=high,format='DDS RGBA8',
                           sha256=hashlib.sha256(data).hexdigest(),source_layer='original procedural Ulysses glyph composition',**metadata))
        sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+relative+'" }')
        previews.append((role,metadata.get('title',sprite),image))
    for b in BRANCHES:
        for i,(primary,secondary) in enumerate(b.subjects):
            ident=focus_id(b,i);key=(b.tag,primary,secondary);arrangement=used[key];used[key]+=1
            if arrangement>=len(ARRANGEMENTS):raise ValueError('Add deliberate arrangement for repeated subjects: '+str(key))
            master=composition(b.tag,primary,secondary,arrangement,settled=i==5)
            result[HERE/'source/focus'/f'{ident}.png']=encoded(master,'PNG')
            relative=f'gfx/AC_reconstruction/focus/{ident}.dds';name='GFX_ac_rc_focus_'+ident
            texture(relative,master.resize((96,96),Image.Resampling.LANCZOS),name,'focus',b.tag,
                    id=ident,title=b.titles[i],primary=primary,secondary=secondary,arrangement=arrangement,master=f'tools/reconstruction/source/focus/{ident}.png')
            sprites.append('spriteType = { name = "'+name+'_shine" texturefile = "'+relative+'" }')
    focus_assets=[r for r in assets if r['role']=='focus']
    if len(focus_assets)!=60 or len({r['sha256']for r in focus_assets})!=60:raise ValueError('Sixty distinct focus compositions required')
    content=content_outputs();ideas=get(get(parse(content['common/ideas/ac_reconstruction.txt']),'ideas'),'country')
    for ident,_,body in ideas:
        tag=ident[:3];branch=next((b for key,b in by_branch.items()if ident.startswith(key+'_')),None)
        if branch:
            if '_service_'in ident:index=0 if '_service_1_'in ident else 3
            elif '_reply_'in ident:index=1 if '_public_'in ident else 2
            else:index=1 if '_civil_policy_'in ident else 2
            primary,secondary=branch.subjects[index]
        else:
            primary,secondary=THEMES[tag];index=4 if '_opening_'in ident else 5
            if '_ministerial_'in ident or '_readiness_'in ident:primary,secondary=secondary,primary
        image=composition(tag,primary,secondary,index,settled=ident.endswith('_settled'))
        texture(f'gfx/AC_reconstruction/ideas/{ident}.dds',image.resize((75,75),Image.Resampling.LANCZOS),
                'GFX_idea_'+ident,'idea',tag,id=ident,primary=primary,secondary=secondary)
    if len(ideas)!=96:raise ValueError('Expected all96 policy/service/narrative spirits')
    for tag in COUNTRY_NAMES:
        image=composition(tag,*THEMES[tag],3)
        texture(f'gfx/AC_reconstruction/categories/{tag.lower()}.dds',image.resize((100,100),Image.Resampling.LANCZOS),
                'GFX_ac_rc_category_'+tag.lower(),'category',tag,title=COUNTRY_NAMES[tag])
    for category,_,entries in parse(content['common/decisions/ac_reconstruction.txt']):
        for ident,_,body in entries:
            tag=ident[:3];branch=next((b for key,b in by_branch.items()if ident.startswith(key+'_')),None)
            subject=branch.subjects[0 if ident.endswith('_1') else 3][0] if branch else 'document'
            image=row_icon(tag,subject,cancel='cancel_service'in ident)
            texture(f'gfx/AC_reconstruction/decisions/{ident}.dds',image,'GFX_decision_ac_rc_'+ident,'decision row',tag,id=ident)
    for tag in COUNTRY_NAMES:
        image=event_image(tag,THEMES[tag]);ident=tag.lower()+'_national'
        result[HERE/'source/events'/f'{ident}.png']=encoded(image,'PNG')
        texture(f'gfx/AC_reconstruction/events/{ident}.dds',fit_event(image),'GFX_ac_rc_event_'+ident,'event illustration',tag,
                title=COUNTRY_NAMES[tag]+': National Review',master=f'tools/reconstruction/source/events/{ident}.png',
                transform='Full-source Lanczos contain to210x176; opaque navy padding; no crop or content edit')
    for b in BRANCHES:
        ident=branch_id(b);image=event_image(b.tag,b.subjects[0]);result[HERE/'source/events'/f'{ident}.png']=encoded(image,'PNG')
        texture(f'gfx/AC_reconstruction/events/{ident}.dds',fit_event(image),'GFX_ac_rc_event_'+ident,'event illustration',b.tag,
                title=b.titles[0],master=f'tools/reconstruction/source/events/{ident}.png',
                transform='Full-source Lanczos contain to210x176; opaque navy padding; no crop or content edit')
    result[MOD/'interface/ac_reconstruction.gfx']=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
    manifest=dict(schema=1,pillow='11.3.0',source_layer='original provisional artwork; no engine/DLC/remote pixels or baked text',
        vector_sources=['tools/reconstruction/build_art.py','tools/reconstruction/content.py','tools/usea_expansion/build_art.py',
                        'tools/event_picture_fit/fit.py','tools/event_picture_fit/bitmap.py'],
        event_packaging_helper_sha256=hashlib.sha256((ROOT/'tools/event_picture_fit/fit.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        glyph_library_sha256=hashlib.sha256(LIBRARY.read_bytes()).hexdigest(),
        framing='Shared navy/cyan family, country-specific structural frames and subject pairs; restrained gold marks settled policies.',
        native='Not rendered in HOI4; native viewport/input acceptance remains pending',assets=assets)
    result[HERE/'assets.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    font=BitmapFont()
    for tag,name in COUNTRY_NAMES.items():
        rows=[(b,i)for b in BRANCHES if b.tag==tag for i in range(6)]
        gallery=Image.new('RGBA',(1120,70+220*(len(rows)//6)),NAVY);font.draw(gallery,name+': Reconstruction Continuations',(24,18),1000)
        for n,(b,i)in enumerate(rows):
            x=25+(n%6)*183;y=62+(n//6)*220
            data=result[MOD/f'gfx/AC_reconstruction/focus/{focus_id(b,i)}.dds'];icon=Image.open(io.BytesIO(data)).convert('RGBA')
            gallery.alpha_composite(icon,(x+25,y));font.draw(gallery,b.titles[i],(x,y+110),153)
        result[HERE/'gallery'/f'{tag.lower()}-focuses.png']=encoded(gallery,'PNG')
    cards=[]
    for role,title,image in previews:
        uri=base64.b64encode(encoded(image,'PNG')).decode()
        cards.append('<figure><img alt="" src="data:image/png;base64,'+uri+'"><figcaption>'+html.escape(role+': '+title)+'</figcaption></figure>')
    page='<!doctype html><meta charset="utf-8"><title>Reconstruction original artwork</title><style>body{background:#081621;color:#daedf2;font:16px sans-serif;margin:28px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:18px}figure{margin:0;padding:16px;border:1px solid #34596b}img{max-width:100%;height:110px;object-fit:contain;display:block;margin:auto}figcaption{margin-top:14px;line-height:1.4}</style><h1>Reconstruction continuations</h1><p>Original procedural briefing compositions. Runtime textures and editable masters are byte-pinned in assets.json. Native HOI4 rendering is untested.</p><main>'+''.join(cards)+'</main>'
    result[HERE/'gallery/index.html']=page.encode()
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();failures=[];out=outputs()
    for path,data in out.items():
        if a.check:
            if not path.exists()or path.read_bytes()!=data:failures.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if failures:raise SystemExit('Reconstruction artwork differs: '+', '.join(failures))
    print('Reconstruction original artwork:',len([p for p in out if p.suffix=='.dds']),'DDS; '+('consistent'if a.check else'generated'))


if __name__=='__main__':main()
