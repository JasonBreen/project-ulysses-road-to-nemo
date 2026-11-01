"""Reproducible technical compositions and packaging of eight imagegen masters.

Creative scene pixels come only from the retained, individually reviewed
masters. Code draws focus/idea/compact-row symbols, never substitutes a collage
for original narrative art. Use pinned Pillow11.3.0; --check never writes.
"""
import argparse
import base64
from collections import Counter
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import textwrap
import PIL
from PIL import Image,ImageDraw,ImageFont,ImageOps
from content import FOCUSES,COUNTRIES
import build

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
SOURCE=ROOT/'source/artwork/fato_south_belka';NAVY=(8,22,33,255);WHITE=(219,236,240,255)
ACCENT={'FAT':(97,204,222,255),'SBK':(147,202,179,255)}
LIBRARY=ROOT/'tools/usea_expansion/build_art.py'
spec=importlib.util.spec_from_file_location('fsb_original_glyphs',LIBRARY);symbols=importlib.util.module_from_spec(spec);spec.loader.exec_module(symbols)
LAYOUTS=[((26,31,110,110),(116,112,50,47)),((65,24,105,113),(24,114,50,48)),((25,68,113,101),(120,26,47,49)),((22,29,100,106),(110,83,62,69)),((47,24,109,94),(62,123,70,43)),((31,36,98,111),(115,83,52,57)),((61,59,108,106),(23,23,54,54)),((28,25,110,96),(114,104,56,56))]

def sha(data):return hashlib.sha256(data).hexdigest()
def encode(image):
    stream=io.BytesIO();image.save(stream,format='DDS');return stream.getvalue()
def composition(tag,subjects,variant=0):
    im=Image.new('RGBA',(192,192));d=ImageDraw.Draw(im);accent=ACCENT.get(tag,ACCENT['FAT'])
    outline=([(23,18),(163,18),(179,47),(171,145),(141,173),(49,173),(17,145),(13,48)] if tag=='FAT' else [(32,15),(160,15),(179,34),(179,151),(155,177),(37,177),(13,151),(13,34)])
    d.polygon(outline,fill=NAVY);d.line(outline+[outline[0]],fill=accent,width=3)
    d.line((35,155,52,164,74,164),fill=(40,78,94,255),width=2);d.line((119,164,142,164,156,152),fill=(40,78,94,255),width=2)
    primary,secondary=LAYOUTS[variant%len(LAYOUTS)]
    symbols.glyph(im,subjects[0],primary,WHITE);symbols.glyph(im,subjects[1],secondary,accent)
    return im

def outputs():
    if PIL.__version__!='11.3.0':raise ValueError('Pinned Pillow11.3.0 required; found '+PIL.__version__)
    build.outputs();out={};assets=[];sprites=[];focus_rows=[];used=Counter()
    def texture(path,im,sprite,role,**meta):
        data=encode(im);out[MOD/path]=data;alpha=list(im.getchannel('A').getextrema())
        row=dict(file=path,sprite=sprite,role=role,width=im.width,height=im.height,frame_width=im.width,frame_height=im.height,frames=1,format='DDS RGBA8',alpha_min=alpha[0],alpha_max=alpha[1],sha256=sha(data),**meta)
        assets.append(row);sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+path+'" }');return row
    for row in FOCUSES:
        pair=(row.tag,row.subjects);variant=used[pair];used[pair]+=1
        if variant>=len(LAYOUTS):raise ValueError('Add a deliberate layout for '+str(pair))
        im=composition(row.tag,row.subjects,variant).resize((96,96),Image.Resampling.LANCZOS)
        path='gfx/AC_fato_south_belka/focus/'+row.id+'.dds';name='GFX_ac_fsb_focus_'+row.id
        asset=texture(path,im,name,'original subject-led focus composition',focus=row.id,subjects=row.subjects,composition=variant,phase=row.phase+1)
        sprites.append('spriteType = { name = "'+name+'_shine" texturefile = "'+path+'" }');focus_rows.append((row,im,asset))
    if len({r[2]['sha256'] for r in focus_rows})!=96:raise ValueError('Unrelated focus compositions must be distinct')
    # Use the actual owning focus/decision subject; scene policy cards use the
    # focus that commissioned their event, not an arbitrary generic portrait.
    for ident in build.IDEAS:
        related=next((r for r in FOCUSES if (r.kind in ('policy','action') and ident=='ac_fsb_'+r.tag.lower()+'_'+r.hook) or (r.kind=='scene' and ident.startswith('ac_fsb_scene_'+r.hook+'_'))),None)
        tag=related.tag if related else ('SBK' if ident.startswith(('ac_fsb_case','ac_fsb_sbk')) else 'FAT')
        subjects=related.subjects if related else (('scales','document') if tag=='SBK' else ('logistics','diplomacy'))
        # Different policy choices intentionally use different spatial emphasis.
        variant=1 if ident.endswith('_b') else (2 if 'interim' in ident or 'limited' in ident else 4)
        im=composition(tag,subjects,variant).resize((75,75),Image.Resampling.LANCZOS)
        texture('gfx/AC_fato_south_belka/ideas/'+ident+'.dds',im,'GFX_idea_ac_fsb_'+ident,'national policy or case outcome artwork',idea=ident,subjects=subjects)
    for tag,items in build.DECISIONS.items():
        themes=('scales','civil') if tag=='SBK' else (('industry','document') if tag=='FAT' else ('diplomacy','document'))
        category='ac_fsb_'+tag.lower()+'_programmes';im=composition(tag,themes,1).resize((100,100),Image.Resampling.LANCZOS)
        a=texture('gfx/AC_fato_south_belka/category/'+tag+'.dds',im,'GFX_decision_category_'+category,'category artwork',tag=tag)
        sprites.append('spriteType = { name = "GFX_'+category+'" texturefile = "'+a['file']+'" }')
        for icon in sorted(set(re.findall(r'icon = (\w+)', ''.join(items)))):
            theme=('scales','document') if icon.endswith('docket') else (('logistics','diplomacy') if icon.endswith('warrant') else themes)
            # Independent compact rendering: no category-size alias in rows.
            iconim=composition(tag,theme,2).resize((26,29),Image.Resampling.LANCZOS)
            texture('gfx/AC_fato_south_belka/decision/'+icon+'.dds',iconim,'GFX_decision_'+icon,'compact decision-row artwork',tag=tag,alpha_requirement='transparent outer corners, opaque motif')
    records=json.loads((SOURCE/'prompts.json').read_text(encoding='utf-8'))['masters']
    if len(records)!=8:raise ValueError('Eight independent original scene masters required')
    source_receipts=[]
    for record in records:
        path=SOURCE/record['file']
        with Image.open(path) as master:
            if master.width<1500 or master.width/master.height<2:raise ValueError('Wide high-resolution master required')
            if not record['prompt'] or 'visually inspected' not in record['status']:raise ValueError('Prompt/review provenance required')
            # Preserve the entire scene with opaque navy padding as needed.
            im=Image.new('RGBA',(450,150),NAVY);fitted=ImageOps.contain(master.convert('RGBA'),im.size,Image.Resampling.LANCZOS);im.alpha_composite(fitted,((450-fitted.width)//2,(150-fitted.height)//2))
            ident=path.stem
            row=texture('gfx/AC_fato_south_belka/events/'+ident+'.dds',im,'GFX_ac_fsb_event_'+ident,'original narrative illustration',source=path.relative_to(ROOT).as_posix(),source_sha256=sha(path.read_bytes()),transform='Lanczos contain; centered opaque navy padding; no semantic edit',event_uses=record['event_uses'])
            source_receipts.append(dict(file=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),width=master.width,height=master.height,prompt_record='source/artwork/fato_south_belka/prompts.json',scene=record['scene'],review=record['status']))
    out[MOD/'interface/ac_fato_south_belka.gfx']=('spriteTypes = {\n'+ '\n'.join(sprites)+'\n}\n').encode()
    sources=[HERE/n for n in ('content.py','build.py','programmes.py','obligations.py','narrative.py','build_art.py')]+[LIBRARY,SOURCE/'prompts.json']
    manifest=dict(schema=1,source_layer='original code-native technical art and original imagegen narrative fiction',renderer='Pillow11.3.0',focus_compositions=96,narrative_masters=8,source_hashes={p.relative_to(ROOT).as_posix():sha(p.read_text(encoding='utf-8').replace('\r\n','\n').encode()) for p in sources},masters=source_receipts,assets=assets,native='pending')
    out[HERE/'assets.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    sheet=Image.new('RGBA',(1200,10*134),NAVY);d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'),10)
    for index,(r,im,_) in enumerate(focus_rows):
        x,y=index%10*120,index//10*134;sheet.alpha_composite(im,(x+12,y+1));d.text((x+4,y+100),r.tag+' '+r.title[:19],font=font,fill=WHITE);d.text((x+4,y+113),r.kind,font=font,fill=ACCENT[r.tag])
    stream=io.BytesIO();sheet.save(stream,format='PNG');out[HERE/'focus-review.png']=stream.getvalue()
    for tag,cfg in COUNTRIES.items():
        rows=[item for item in focus_rows if item[0].tag==tag];by_id={r.id:r for r,_,_ in rows};width=(max(r.x for r,_,_ in rows)+5)*96;height=(max(r.y for r,_,_ in rows)+2)*110
        svg=['<svg xmlns="http://www.w3.org/2000/svg" width="'+str(width)+'" height="'+str(height)+'" viewBox="0 0 '+str(width)+' '+str(height)+'"><rect width="100%" height="100%" fill="#081621"/><g fill="#daedf2" font-family="sans-serif"><text x="30" y="28" font-size="18">'+html.escape(cfg['name'])+': offline prerequisite schematic</text><text x="30" y="49" font-size="12">Declared focus positions and real artwork. Schematic spacing; not a native screenshot. Hover a node for its full purpose.</text></g>']
        for r,_,_ in rows:
            for group in r.requirements:
                for parent in group:
                    p=by_id[tag+'_nat_'+parent];x1,y1=p.x*96,p.y*110+70;x2,y2=r.x*96,r.y*110-25
                    svg.append('<path d="M '+str(x1)+' '+str(y1)+' C '+str(x1)+' '+str((y1+y2)//2)+' '+str(x2)+' '+str((y1+y2)//2)+' '+str(x2)+' '+str(y2)+'" fill="none" stroke="#3e8195" stroke-width="2"'+(' stroke-dasharray="5 4"'if len(group)>1 else '')+'/>')
        for r,im,_ in rows:
            x,y=r.x*96,r.y*110;buf=io.BytesIO();im.save(buf,format='PNG');png=base64.b64encode(buf.getvalue()).decode()
            svg.append('<g><title>'+html.escape(r.id+' | '+r.title+' | '+r.purpose)+'</title><rect x="'+str(x-105)+'" y="'+str(y-24)+'" width="210" height="99" rx="8" fill="#0c2331" stroke="#427c8b"/><image href="data:image/png;base64,'+png+'" x="'+str(x-101)+'" y="'+str(y-17)+'" width="64" height="64"/>')
            for n,line in enumerate(textwrap.wrap(r.title,21)):
                svg.append('<text x="'+str(x-32)+'" y="'+str(y+n*15)+'" font-family="sans-serif" font-size="12" fill="#daedf2">'+html.escape(line)+'</text>')
            svg.append('<text x="'+str(x-95)+'" y="'+str(y+61)+'" font-family="sans-serif" font-size="10" fill="#8cbdc9">'+str(r.cost*7)+' days | '+r.kind+'</text></g>')
        svg.append('</svg>');out[HERE/(tag+'-focus-layout.svg')]=''.join(svg).encode()
    return out,manifest

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out,manifest=outputs();bad=[]
    for path,data in out.items():
        if a.check:
            if not path.exists() or path.read_bytes()!=data:bad.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Stale FAT/SBK artwork:\n'+'\n'.join(bad))
    print(('Checked' if a.check else 'Packaged'),len(manifest['assets']),'textures, 96 focus compositions, 8 scene masters')
if __name__=='__main__':main()
