"""Original code-native compositions; no game or external image pixels.

Shared framing is intentional. Every focus has a unique semantic motif pair;
national mandates incorporate the existing national flag identity. DDS output
is uncompressed RGBA, one frame, with deliberate transparent icon apertures.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import re
from pathlib import Path

from PIL import Image,ImageDraw,ImageOps,__version__ as PILLOW_VERSION
from content import FOCUSES,CHOICES,IDEAS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'
spec=importlib.util.spec_from_file_location('institution_geometry',ROOT/'tools/usea_expansion/build_art.py')
geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
NAVY=geometry.NAVY;CYAN=geometry.CYAN;WHITE=geometry.WHITE;GOLD=geometry.GOLD


def composition(size,motifs,side='civil',flag=None):
    # Render at4x for controlled antialiasing while preserving clear subject
    # silhouettes. The final icons carry no numbers or tiny title text.
    scale=4;w,h=size;image=Image.new('RGBA',(w*scale,h*scale));draw=ImageDraw.Draw(image)
    def p(values):return [(round(x*w*scale/100),round(y*h*scale/100)) for x,y in values]
    draw.polygon(p([(8,8),(92,8),(92,86),(50,98),(8,86)]),fill=NAVY,outline=CYAN,width=scale)
    draw.line(p([(17,18),(37,18)]),fill=CYAN,width=scale)
    draw.line(p([(63,18),(83,18)]),fill=CYAN,width=scale)
    accent=CYAN if side=='civil' else GOLD
    primary,secondary=motifs
    geometry.glyph(image,primary,(int(w*scale*.12),int(h*scale*.20),int(w*scale*.54),int(h*scale*.56)),WHITE)
    draw.rectangle((int(w*scale*.57),int(h*scale*.48),int(w*scale*.89),int(h*scale*.84)),fill=NAVY)
    geometry.glyph(image,secondary,(int(w*scale*.58),int(h*scale*.49),int(w*scale*.29),int(h*scale*.33)),accent)
    if flag:
        with Image.open(flag) as original:
            stamp=ImageOps.contain(original.convert('RGBA'),(int(w*scale*.33),int(h*scale*.17)),Image.Resampling.LANCZOS)
        image.alpha_composite(stamp,(int(w*scale*.34),int(h*scale*.04)))
    return image.resize(size,Image.Resampling.LANCZOS)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if PILLOW_VERSION!='11.3.0':raise SystemExit('Institution art packaging requires Pillow==11.3.0 (CI pin); detected '+PILLOW_VERSION)
    outputs={};assets=[];bindings=[];focus_images=[]
    def asset(ident,size,motifs,sprites,side='civil',flag=None,role='original code-native institutional composition'):
        image=composition(size,motifs,side,flag)
        stream=io.BytesIO();image.save(stream,format='DDS');raw=stream.getvalue()
        path='gfx/AC_politics/'+ident+'.dds';outputs[MOD/path]=raw
        source={'kind':'original authored geometry','source':'tools/institutions/build_art.py','motifs':list(motifs)}
        if flag:source.update(flag=flag.relative_to(MOD).as_posix(),flag_sha256=hashlib.sha256(flag.read_bytes()).hexdigest())
        assets.append(dict(file=path,width=size[0],height=size[1],frames=1,alpha='transparent outer aperture; opaque navy icon field',sha256=hashlib.sha256(raw).hexdigest(),sprite_bindings=sprites,provenance=source,role=role))
        for sprite in sprites:bindings.append('spriteType = { name = "'+sprite+'" texturefile = "'+path+'" noOfFrames = 1 }')
        return image
    for focus in FOCUSES:
        focus_images.append((focus,asset('focus_'+focus.suffix,(96,96),focus.motifs,['GFX_ac_pol_focus_'+focus.suffix])))
    for suffix,(_,_,_,motifs) in IDEAS.items():asset('idea_'+suffix,(64,64),motifs,['GFX_idea_ac_pol_'+suffix])
    for tag,*_,motifs in CHOICES:
        flag=MOD/'gfx/flags'/(tag+'.tga')
        if not flag.exists():flag=None
        for side in ('civil','reserve'):
            asset('idea_'+tag+'_'+side,(64,64),motifs if side=='civil' else tuple(reversed(motifs)),['GFX_idea_'+tag+'_pol_'+side],side,flag)
    asset('category_institutions',(100,100),('assembly','tools'),['GFX_decision_category_ac_pol_institutions','GFX_decision_ac_pol_institutions'])
    # A symbolic case-file illustration supports the21 national reviews. It is
    # a deliberate shared interface picture, not21 purported narrative scenes.
    event=Image.new('RGBA',(200,160),NAVY);draw=ImageDraw.Draw(event)
    draw.rectangle((7,7,192,152),outline=CYAN,width=1)
    geometry.glyph(event,'assembly',(18,20,102,112),WHITE)
    geometry.glyph(event,'document',(112,60,65,82),CYAN)
    stream=io.BytesIO();event.save(stream,format='DDS');raw=stream.getvalue();path='gfx/AC_politics/event_review.dds'
    outputs[MOD/path]=raw
    assets.append(dict(file=path,width=200,height=160,frames=1,alpha='fully opaque event canvas',sha256=hashlib.sha256(raw).hexdigest(),sprite_bindings=['GFX_ac_pol_event_review'],provenance={'kind':'original authored geometry','source':'tools/institutions/build_art.py','motifs':['assembly','document']},role='shared symbolic institutional review card'))
    bindings.append('spriteType = { name = "GFX_ac_pol_event_review" texturefile = "'+path+'" noOfFrames = 1 }')
    outputs[MOD/'interface/ac_politics.gfx']=('spriteTypes = {\n'+'\n'.join(bindings)+'\n}\n').encode()
    outputs[HERE/'assets.json']=(json.dumps(assets,indent=2)+'\n').encode()
    # Editable source is this code plus semantic content. The review gallery
    # labels all36 compositions but is not engine-rendered acceptance evidence.
    # Use the shipped original bitmap atlas for identical gallery pixels on
    # Linux/Windows rather than relying on a platform FreeType build.
    font_text=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text()
    metrics={int(values['id']):{key:int(value) for key,value in values.items()}
             for line in font_text.splitlines() if line.startswith('char id=')
             for values in [dict(re.findall(r'(\w+)=(-?\d+)',line))]}
    atlas=Image.open(MOD/'gfx/fonts/ACBriefing16.dds').convert('RGBA')
    gallery=Image.new('RGBA',(1200,840),NAVY);draw=ImageDraw.Draw(gallery)
    for i,(focus,image) in enumerate(focus_images):
        x=(i%6)*200;y=(i//6)*140
        gallery.alpha_composite(image,(x+52,y+8))
        title=focus.suffix.replace('_',' ');cursor=x+(200-sum(metrics[ord(c)]['xadvance'] for c in title))//2
        for char in title:
            m=metrics[ord(char)];glyph=atlas.crop((m['x'],m['y'],m['x']+m['width'],m['y']+m['height']))
            gallery.alpha_composite(glyph,(cursor+m['xoffset'],y+110+m['yoffset']));cursor+=m['xadvance']
    target=ROOT/'docs/evidence/institutions/focus-gallery.png'
    stream=io.BytesIO();gallery.save(stream,format='PNG');outputs[target]=stream.getvalue()
    for path,data in outputs.items():
        if args.check:
            if not path.exists():raise SystemExit('Missing institutional art output: '+str(path))
            actual=path.read_bytes()
            if path.suffix=='.png':
                # Pillow PNG encoders can differ by version; pixels are the
                # authoritative gallery content, while DDS hashes remain exact.
                with Image.open(io.BytesIO(actual)) as a,Image.open(io.BytesIO(data)) as b:
                    if a.size!=b.size or a.convert('RGBA').tobytes()!=b.convert('RGBA').tobytes():raise SystemExit('Institution gallery differs')
            else:
                if path.suffix in ('.gfx','.json'):actual=actual.replace(b'\r\n',b'\n')
                if actual!=data:raise SystemExit('Institution art output differs: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Institutions artwork:',len(assets),'DDS;',len(bindings),'sprites;', 'verified' if args.check else 'packaged')


if __name__=='__main__':main()
