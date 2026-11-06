"""Original campaign diagrams and controls. No installed-mod or game pixels.

The editable masters are this compositor and the existing Ulysses glyph library.
PNG sources are exported beside the DDS delivery manifest. --check is read-only.
"""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from ac_campaigns.catalogue import NATIONS, OPERATIONS
from ac_campaigns.narrative import SCENES
from ac_campaigns.build import compile_content

spec=importlib.util.spec_from_file_location('campaign_original_glyphs',ROOT/'tools/usea_expansion/build_art.py')
glyphs=importlib.util.module_from_spec(spec);spec.loader.exec_module(glyphs)
BG=(8,22,33,255);EDGE=(43,78,99,255);CYAN=(93,208,223,255);GOLD=(230,181,95,255)


def compose(size,subject,stage=0):
    w,h=size;im=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,w-2,h-2),radius=max(2,w//12),fill=BG,outline=EDGE,width=max(1,w//70))
    if w>100:
        for x in range(12,w-12,16):d.line((x,8,x,h-9),fill=(18,40,54,255))
        for y in range(12,h-12,16):d.line((8,y,w-9,y),fill=(18,40,54,255))
        # A distinct original briefing diagram for each subject; its geometry is
        # illustrative, never a claimed canonical map or equipment silhouette.
        glyphs.glyph(im,subject,(w*.12,h*.15,w*.62,h*.68),CYAN)
        d.line((w*.74,h*.24,w*.9,h*.24,w*.9,h*.76,w*.74,h*.76),fill=GOLD,width=2)
        glyphs.glyph(im,'document',(w*.76,h*.36,w*.13,h*.22),GOLD)
    else:
        inset=max(3,int(w*.16));glyphs.glyph(im,subject,(inset,inset,w-2*inset,h-2*inset),CYAN)
        if w>=75:
            for i in range(6):
                x=round(w*.16+i*w*.12);d.rectangle((x,h-7,x+3,h-4),fill=GOLD if i==stage else EDGE)
    return im


def outputs():
    files={};records=[];sprites=[]
    content,manifest=compile_content()
    roles={}
    for row in manifest['focuses']:
        n=next(n for n in NATIONS if n.tag==row['tag']);kind=n.themes[row['lane']]
        roles['GFX_'+row['id']]=(row['id'],(96,96),kind,'focus',('register','policy_a','policy_b','prepared','review','account').index(row['id'].split('_',3)[3]))
    for n in NATIONS:roles['GFX_ac_camp_'+n.tag.lower()]=('ac_camp_'+n.tag.lower(),(100,100),n.themes[0],'category',0)
    # Inventory actual consumers rather than guessing from a naming family.
    import re
    for name in re.findall(r'picture = (\w+)',content['common/ideas/ac_campaigns.txt']):roles['GFX_idea_'+name]=(name,(75,75),'scales','idea',0)
    for name in re.findall(r'icon = (\w+)',content['common/decisions/ac_campaigns.txt']):
        match=next((o for o in OPERATIONS if name.startswith('ac_camp_'+o.key+'_')),None)
        roles['GFX_decision_'+name]=(name,(26,29),match.glyph if match else 'document','decision',0)
    for kind in sorted({r.get('glyph','document') for r in SCENES}|{o.glyph for o in OPERATIONS}|{'peace'}):
        roles['GFX_ac_camp_event_'+kind]=('ac_camp_event_'+kind,(210,176),kind,'event',0)
    for sprite,(key,size,kind,role,stage) in sorted(roles.items()):
        im=compose(size,kind,stage);dds=io.BytesIO();im.save(dds,format='DDS');data=dds.getvalue()
        relative='gfx/AC_campaigns/'+role+'/'+key+'.dds';files[MOD/relative]=data
        master=io.BytesIO();im.save(master,format='PNG');masterpath=HERE/'source'/role/(key+'.png');files[masterpath]=master.getvalue()
        sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+relative+'" noOfFrames = 1 }')
        if role=='focus':sprites.append('spriteType = { name = "'+sprite+'_shine" texturefile = "'+relative+'" noOfFrames = 1 }')
        records.append(dict(sprite=sprite,path=relative,role=role,width=size[0],height=size[1],sha256=hashlib.sha256(data).hexdigest(),source_layer='original authored geometry',master=str(masterpath.relative_to(ROOT)).replace('\\','/')))
    files[MOD/'interface/ac_campaigns.gfx']=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
    files[HERE/'assets.json']=(json.dumps(dict(schema=1,assets=records,native_acceptance=False),indent=2)+'\n').encode()
    return files


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();bad=[];out=outputs()
    for path,data in out.items():
        old=path.read_bytes() if path.exists() else b''
        equal=old==data
        if path.suffix=='.png' and old:
            with Image.open(io.BytesIO(old)) as x,Image.open(io.BytesIO(data)) as y:equal=x.size==y.size and x.convert('RGBA').tobytes()==y.convert('RGBA').tobytes()
        if a.check:
            if not equal:bad.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Stale AC04/AC5 art: '+', '.join(bad))
    print(f'Original AC04/AC5 art: {len(out)} outputs; '+('consistent' if a.check else 'generated'))


if __name__=='__main__':main()
