"""Package only the enumerated Pacific originals; initial139 DDS stay intact."""
import argparse
import hashlib
import html
import importlib.util
import io
import json
import math
import sys
import PIL
from PIL import Image,ImageDraw,ImageOps
from config import ROOT,HERE,MOD,campaigns
sys.path.insert(0,str(ROOT/'tools'))
from squadrons.pacific_art.audit import sources
from reconstruction.build_art import BitmapFont
spec=importlib.util.spec_from_file_location('original_story_art_helpers',HERE.parent/'build_art.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def same_png(a,b):
    with Image.open(io.BytesIO(a))as x,Image.open(io.BytesIO(b))as y:return x.size==y.size and x.convert('RGBA').tobytes()==y.convert('RGBA').tobytes()


def loading_cover(path,size=(1920,1080)):
    with Image.open(path)as image:return ImageOps.fit(image.convert('RGBA'),size,method=Image.Resampling.LANCZOS,centering=(.5,.5))


def outputs():
    if PIL.__version__!='11.3.0':raise ValueError('Pinned Pillow11.3.0 required')
    old.OUTPUTS.clear();old.ASSETS.clear();old.SPRITES.clear()
    rows=campaigns();tags={r['tag']for r in rows};plan,ready=sources();ready=[r for r in ready if r['tag']in tags]
    def texture(relative,image,sprite,role,source=None,**metadata):
        if source:source={**source,'record_path':source['path'].with_suffix('.json')}
        old.texture(relative,image,sprite,role,source,**metadata)
    for row in ready:
        ident=row['id'];tag=row['tag'].lower()
        if row['path'].parent.name=='portraits':
            texture('gfx/AC_squadrons_pacific/portraits/'+ident+'.dds',old.contained(row['path'],(156,210)),
                'GFX_ac_sqp_portrait_'+ident,'original personal portrait; explicit export, not a government portrait',row)
            texture('gfx/AC_squadrons_pacific/cast/'+ident+'.dds',old.contained(row['path'],(200,160)),
                'GFX_ac_sqp_cast_'+ident,'original personal cast event card',row)
        elif row['path'].parent.name=='scenes':
            texture('gfx/AC_squadrons_pacific/events/'+ident+'.dds',old.contained(row['path'],(200,160)),
                'GFX_ac_sqp_'+ident,'original personal scene; full-source fit',row)
        else:
            texture('gfx/loadingscreens/ac_sqp_'+tag+'.dds',loading_cover(row['path']),None,
                'independent original loading composition',row,transform='Reviewed centered Lanczos cover1920x1080; preserves supplied panoramic source',safe_area='Exact3440x1440 offline crop separately reviewed; native scale unknown')
            texture('gfx/loadingscreens/ac_sqp_'+tag+'_small.dds',old.contained(row['path'],(192,144)),
                'GFX_ac_sqp_'+tag+'_small','loading rotation thumbnail',row)
    for row in rows:
        tag=row['tag'];image,flag=old.insignia(tag)
        texture('gfx/AC_squadrons_pacific/categories/'+tag.lower()+'.dds',image,'GFX_ac_sqp_category_'+tag.lower(),
            'original story category with established national identity',national_flag=flag.relative_to(MOD).as_posix(),national_flag_sha256=old.digest(flag.read_bytes()),editable_geometry='tools/squadrons/build_art.py:insignia')
        for action in('read','pause','resume','cast'):
            image,flag=old.decision_icon(tag,action)
            texture('gfx/AC_squadrons_pacific/decisions/'+tag.lower()+'_'+action+'.dds',image,
                'GFX_decision_ac_sqp_'+tag.lower()+'_'+action,'native26x29 personal-story action',
                national_flag=flag.relative_to(MOD).as_posix(),national_flag_sha256=old.digest(flag.read_bytes()),editable_geometry='tools/squadrons/build_art.py:decision_icon')
    image=Image.new('RGBA',(75,75));draw=ImageDraw.Draw(image)
    draw.polygon(((8,6),(67,6),(69,60),(37,72),(6,60)),fill=old.NAVY,outline=old.CYAN,width=2)
    draw.rectangle((19,20,53,53),outline=old.WHITE,width=2)
    for y,end in((28,46),(35,42),(42,48)):draw.line((25,y,end,y),fill=old.CYAN,width=2)
    texture('gfx/AC_squadrons_pacific/ideas/professional_debrief.dds',image,'GFX_idea_ac_sqp_professional_debrief','original personal-debrief spirit',editable_geometry='tools/squadrons/pacific/build_art.py:outputs')
    old.put(MOD/'interface/ac_squadrons_pacific.gfx','spriteTypes = {\n'+'\n'.join(old.SPRITES)+'\n}\n')
    old.put(MOD/'common/frontend/backgrounds/ac_sqp_backgrounds.txt',''.join('ac_sqp_'+r['tag'].lower()+' = {}\n'for r in rows))
    old.put(HERE/'assets.json',json.dumps(dict(schema=1,assets=old.ASSETS,selected_sources=len(ready),preserved_initial_textures=139,
        chapter_mapping=[dict(tag=r['tag'],chapter=n,source=r['tag'].lower()+'_scene_'+slot)for r in rows for slot,ids in r['chapters_by_slot'].items()for n in ids],
        endings={r['tag']:r['ending_slots']for r in rows},portrait_exports='156x210 exports have no national leader consumers;200x160 castcards are the runtime country-event surface',native_acceptance=False),indent=2)+'\n')
    font=BitmapFont();evidence=ROOT/'docs/evidence/pacific-stories'
    for row in rows:
        tag=row['tag'].lower();assets=[r for r in old.ASSETS if tag in r['file']or any(p['id']in r['file']for p in row['cast'])]
        sheet=Image.new('RGBA',(1040,55+math.ceil(len(assets)/4)*220),old.NAVY)
        font.draw(sheet,row['title']+' - packaged cards and native row icons',(15,10),1000)
        for i,asset in enumerate(assets):
            x=10+i%4*260;y=50+i//4*220
            with Image.open(io.BytesIO(old.OUTPUTS[MOD/asset['file']]))as image:tile=ImageOps.contain(image.convert('RGBA'),(244,170),Image.Resampling.LANCZOS)
            sheet.alpha_composite(tile,(x+(244-tile.width)//2,y));font.draw(sheet,asset['file'].rsplit('/',1)[1],(x,y+175),245)
        old.put(evidence/(tag+'-packaged.png'),old.encoded(sheet,'PNG'))
    old.put(evidence/'README.md','# Pacific story presentation\n\n'+str(len(old.ASSETS))+' DDS textures;'+str(len(old.SPRITES))+' explicit sprite bindings;'+str(len(ready))+' selected original masters. The two country contact sheets show actual packaged pixels. Portraits and scenes use full-source contain. Independent main loadings use the separately reviewed centered cover; their thumbnails use contain. Original78 masters/139 DDS are protected by legacy_contract.json.156x210 portrait exports are not national leader bindings. Source geometry/pixels only; native rendering remains untested.\n')
    return dict(old.OUTPUTS)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();result=outputs()
    for path,data in result.items():
        if args.check:
            current=path.read_bytes()if path.exists()else b''
            if path.suffix=='.png'and current and same_png(current,data):continue
            if path.suffix in('.json','.gfx','.txt','.md'):current=current.replace(b'\r\n',b'\n')
            if current!=data:raise SystemExit('Stale new story artwork: '+path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Pacific story artwork: '+str(len(old.ASSETS))+' DDS/'+str(len(old.SPRITES))+' bindings; native untested')
