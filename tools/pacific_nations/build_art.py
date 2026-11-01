"""Original national artwork and portable galleries from authored vector glyphs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys

import PIL
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from pacific_nations.model import HERE,MOD,countries
from pacific_nations.build import outputs as content_outputs
from superpowers.build_art import frame,row_icon,event_image,encode,ACCENT,NAVY,LIGHT,GOLD,glyphs
from reconstruction.build_art import BitmapFont
from usea_expansion.script import parse,get

LAYOUTS=[((26,23,115,112),(129,93,43,46),(52,135,42,34)),
 ((27,38,105,109),(129,26,43,45),(121,128,45,37)),
 ((51,25,108,110),(23,116,44,45),(131,137,38,31)),
 ((28,26,111,109),(131,58,40,42),(87,136,42,33)),
 ((48,41,111,104),(24,24,42,46),(24,127,46,38)),
 ((34,24,111,108),(127,107,44,46),(64,138,41,29)),
 ((43,41,111,107),(24,23,42,43),(127,125,42,35)),
 ((33,27,111,111),(129,82,42,42),(66,141,46,28))]
STAGES=('document','civil','command','communications','scales','assembly','security','peace')


def digest(path):
    data=path.read_bytes()
    if path.suffix in('.py','.fnt'):data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()


def composition(tag,motifs,stage=0,settled=False):
    image=frame(tag,settled);a,b,c=LAYOUTS[stage%8]
    glyphs.glyph(image,motifs[0],a,LIGHT);glyphs.glyph(image,motifs[1],b,ACCENT[tag]);glyphs.glyph(image,STAGES[stage%8],c,ACCENT[tag])
    return image


def same_png(before,after):
    try:
        with Image.open(io.BytesIO(before))as a,Image.open(io.BytesIO(after))as b:
            return a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
    except (OSError,ValueError):return False


def outputs():
    if PIL.__version__!='11.3.0':raise ValueError('Exact DDS packaging requires Pillow11.3.0')
    result={};content,_=content_outputs();font=BitmapFont()
    for module in countries():
        tag=module.TAG;stem='ac_snc_'+tag.lower();assets=[];sprites=[]
        def texture(relative,image,sprite,role,**metadata):
            data=encode(image);result[MOD/relative]=data;low,high=image.getchannel('A').getextrema()
            assets.append(dict(file=relative,sprite=sprite,role=role,width=image.width,height=image.height,frames=1,frame_width=image.width,
                alpha_min=low,alpha_max=high,sha256=hashlib.sha256(data).hexdigest(),source_layer='original authored vector composition',**metadata))
            sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+relative+'" }')
        for b in module.BRANCHES:
            for i,(title,description)in enumerate(b.steps):
                ident=b.focus(i);image=composition(tag,b.motifs,i,b.suffixes[i]=='settlement');master=HERE/'source'/tag/'focus'/(ident+'.png');result[master]=encode(image,'PNG')
                relative='gfx/AC_pacific_nations/'+tag+'/focus/'+ident+'.dds';sprite='GFX_ac_snc_focus_'+ident
                texture(relative,image.resize((96,96),Image.Resampling.LANCZOS),sprite,'focus',id=ident,title=title,motifs=b.motifs,stage=b.suffixes[i],master=master.relative_to(ROOT).as_posix())
                sprites.append('spriteType = { name = "'+sprite+'_shine" texturefile = "'+relative+'" }')
        if len({a['sha256']for a in assets})!=sum(len(b.steps)for b in module.BRANCHES):raise ValueError('Every new focus must have its own composition')
        ideas=get(get(parse(content['common/ideas/'+stem+'.txt']),'ideas'),'country')
        for ident,_,node in ideas:
            b=next((b for b in module.BRANCHES if ident.startswith(b.id)),None)
            if b:motifs=b.motifs;stage=1 if'_civil_'in ident else 2 if'_protected_'in ident else 5 if'_public_return_'in ident else 6
            else:
                number=int(ident.split('_message_')[1].split('_')[0]);b=module.BRANCHES[number%10]if 10<=number<26 else module.BRANCHES[0]
                motifs=b.motifs;stage=5 if'_public_'in ident else 6
            image=composition(tag,motifs,stage,ident.endswith('_settled')).resize((75,75),Image.Resampling.LANCZOS)
            texture('gfx/AC_pacific_nations/'+tag+'/ideas/'+ident+'.dds',image,'GFX_idea_'+ident,'idea',id=ident)
        image=composition(tag,('assembly','document')if tag=='OSE'else('economy','command'),4).resize((100,100),Image.Resampling.LANCZOS)
        texture('gfx/AC_pacific_nations/'+tag+'/category.dds',image,'GFX_ac_snc_category_'+tag.lower(),'category')
        for _,_,rows in parse(content['common/decisions/'+stem+'.txt']):
            for ident,_,node in rows:
                b=next(b for b in module.BRANCHES if ident.startswith(b.id))
                texture('gfx/AC_pacific_nations/'+tag+'/rows/'+ident+'.dds',row_icon(tag,b.motifs[0]),'GFX_decision_'+get(node,'icon'),'decision row',id=ident)
        for kind,_,node in parse(content['events/'+stem+'.txt']):
            if kind!='country_event':continue
            number=int(get(node,'id').split('.')[1]);branch=module.BRANCHES[number%10]if 10<=number<26 else module.BRANCHES[0]
            image=event_image(tag,*branch.motifs)
            if number>=20:
                draw=ImageDraw.Draw(image);draw.line((240,216,400,216),fill=GOLD,width=3);glyphs.glyph(image,'scales',(289,111,61,65),ACCENT[tag])
            master=HERE/'source'/tag/'events'/(str(number)+'.png');result[master]=encode(image,'PNG')
            texture('gfx/AC_pacific_nations/'+tag+'/events/'+str(number)+'.dds',image,get(node,'picture'),'event illustration',id=get(node,'id'),master=master.relative_to(ROOT).as_posix())
        result[MOD/'interface'/(stem+'.gfx')]=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
        dependencies=[HERE/'build_art.py',HERE/'model.py',HERE/'build.py',HERE/(tag.lower()+'.py'),ROOT/'tools/superpowers/build_art.py',ROOT/'tools/reconstruction/build_art.py',ROOT/'tools/usea_expansion/build_art.py',MOD/'gfx/fonts/ACBriefing16.fnt',MOD/'gfx/fonts/ACBriefing16.dds']
        manifest=dict(schema=1,country=tag,pillow='11.3.0',assets=assets,source_layer='Original national briefing compositions, not official emblems',
            dependencies={path.relative_to(ROOT).as_posix():digest(path)for path in dependencies},hash_rule='Python/FNT source normalizes CRLF to LF; DDS and delivered textures use raw bytes.',native_acceptance=False)
        result[HERE/('assets_'+tag+'.json')]=(json.dumps(manifest,indent=2)+'\n').encode()
        profile=dict(schema=1,name=tag+' national continuation original art; explicit base-only static scenario',enabled_dlc=[],provider_overrides=[],payload_overrides=[],provenance=[dict(path=a['file'],provider='mod',sha256=a['sha256'],classification='authored',reason='Original vector composition with editable sources; exact file only',evidence='tools/pacific_nations/assets_'+tag+'.json; tools/pacific_nations/source/'+tag)for a in assets])
        result[HERE/('audit_'+tag+'.json')]=(json.dumps(profile,indent=2)+'\n').encode()
        gallery=Image.new('RGBA',(1280,120+len(module.BRANCHES)*205),NAVY);font.draw(gallery,module.NAME+': Continuing National Reviews',(25,20),1220)
        for row,b in enumerate(module.BRANCHES):
            for i,(title,_)in enumerate(b.steps):
                x=23+i*157;y=73+row*205;ident=b.focus(i);data=result[MOD/f'gfx/AC_pacific_nations/{tag}/focus/{ident}.dds']
                with Image.open(io.BytesIO(data))as icon:gallery.alpha_composite(icon.convert('RGBA'),(x+23,y))
                font.draw(gallery,title,(x,y+106),145)
        result[HERE/'gallery'/(tag+'.png')]=encode(gallery,'PNG')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,data in outputs().items():
        if args.check:
            before=path.read_bytes()if path.exists()else b''
            match=same_png(before,data)if path.suffix=='.png'else before.replace(b'\r\n',b'\n')==data if path.suffix in('.json','.gfx')else before==data
            if not match:raise SystemExit('Stale national artwork: '+path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Original national compositions packaged; native presentation untested')
