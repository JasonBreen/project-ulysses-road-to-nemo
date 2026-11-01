"""Original navy/cyan ship, component and transparent designer-layer masters."""
import argparse
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import sys
import PIL
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/air_program'),str(ROOT/'tools/land_program')]
spec=importlib.util.spec_from_file_location('naval_vector_primitives',ROOT/'tools/air_program/build_art.py')
vector=importlib.util.module_from_spec(spec);spec.loader.exec_module(vector)
from naval_content import YEARS,FAMILIES,SHIPS,MODULES,tech_id,model_id,hull_id,module_id
from naval_ui import layer_name
Drawing=vector.Drawing;NAVY=vector.NAVY;CYAN=vector.CYAN;WHITE=vector.WHITE;MID=vector.MID
OUTPUT={};ASSETS=[];SPRITES=[]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def put(path,data):OUTPUT[ROOT/path]=data.encode() if isinstance(data,str) else data
def encode(im,format='DDS'):
    s=io.BytesIO();im.convert('RGBA').save(s,format=format);return s.getvalue()
def fit_subject(drawing,size):
    image=drawing.image((drawing.width,drawing.height));box=image.getchannel('A').getbbox()
    if not box:raise ValueError('Empty original naval subject')
    image=image.crop((max(0,box[0]-4),max(0,box[1]-4),min(image.width,box[2]+4),min(image.height,box[3]+4)))
    image.thumbnail(size,Image.Resampling.LANCZOS);out=Image.new('RGBA',size);out.alpha_composite(image,((size[0]-image.width)//2,(size[1]-image.height)//2))
    out.putdata([(0,0,0,0) if a<4 else (r,g,b,a) for r,g,b,a in out.getdata()]);return out
def bind(name,path,frames=1,**extra):SPRITES.append(dict(name=name,asset=path,frames=frames,**extra))
def texture(path,im,role,source=None,frames=1,**extra):
    raw=encode(im);put('mod/2985041246/'+path,raw);lo,hi=im.getchannel('A').getextrema()
    row=dict(file=path,width=im.width,height=im.height,frames=frames,frame_width=im.width//frames,alpha_min=lo,alpha_max=hi,
        alpha_bbox=list(im.getchannel('A').getbbox()) if im.getchannel('A').getbbox() else None,format='DDS RGBA8',sha256=digest(raw),role=role,**extra)
    if source:row.update(source=source,source_sha256=digest(OUTPUT[ROOT/source]))
    ASSETS.append(row);return path

def ship(family,t,bare=False):
    d=Drawing(508,248)
    if family=='systems':
        d.ellipse((40,60,170,190),NAVY,WHITE,3);d.ellipse((65,85,145,165),NAVY,CYAN,3)
        for n in range(5+t):
            import math
            a=n*6.283185/(5+t);d.line([(105,125),(105+55*math.cos(a),125+55*math.sin(a))],CYAN,3)
        d.rectangle((215,62,450,186),NAVY,CYAN,3)
        for n in range(3+t):d.rectangle((230+n*31,86,248+n*31,108),MID,WHITE,2)
        d.line([(230,148),(280,148),(300,128),(325,148),(435,148)],WHITE,3);return d
    wide={'escort':25,'cruiser':36,'fleet':44,'submarine':20,'carrier':56}[family]+t
    stern=32+(4-t)*3;bow=476-t*2;cy=124
    d.polygon([(stern,cy-wide*.7),(80,cy-wide),(390,cy-wide),(bow,cy),(390,cy+wide),(80,cy+wide),(stern,cy+wide*.7)],NAVY,CYAN,3)
    if family=='carrier':
        d.rectangle((80,80-t,416,166+t),NAVY,WHITE,2);d.line([(94,125),(390,125)],CYAN,2)
        d.rectangle((238,64,300+t*8,88),MID,CYAN,2)
        for n in range(4+t):d.line([(105+n*35,92),(120+n*35,92)],WHITE,2)
        d.line([(378,89),(401,105),(378,121)],CYAN,2)
    elif family=='submarine':
        d.ellipse((165,106-t,314,142+t),NAVY,WHITE,2);d.rectangle((232,95,275+t*3,113),MID,CYAN,2)
        d.line([(stern-12,111),(stern+13,124),(stern-12,137)],WHITE,2)
        for n in range(2+t):d.line([(110+n*27,117),(110+n*27,131)],MID,2)
    else:
        d.rectangle((210,101-t,298+t*6,147+t),MID,WHITE,2)
        for x in (175,300):d.rectangle((x,109,x+22,139),NAVY,CYAN,2)
        d.line([(253,79),(253,169)],CYAN,2);d.line([(233,93),(273,93)],WHITE,3)
        for n in range(2+t):d.line([(221+n*12,107),(221+n*12,139)],CYAN,1.5)
        if not bare:
            for x in ((117,367) if family=='fleet' else (127,369) if family=='cruiser' else (355,)):
                d.ellipse((x-13,111,x+13,137),NAVY,WHITE,2)
                d.line([(x+3,119),(x+34+t*2,119)],CYAN,3);d.line([(x+3,129),(x+34+t*2,129)],CYAN,3)
    for n in range(t+1):d.line([(83+n*17,cy-wide+5),(83+n*17,cy-wide+11)],WHITE,2)
    return d

def component(kind,t):
    d=Drawing(128,128);c=CYAN
    if 'engine' in kind:
        pods={'light_engine':1,'cruiser_engine':2,'sub_engine':1,'carrier_engine':3}[kind]
        for pod in range(pods):
            yy=32+(pod*29 if pods>1 else 18);height=22 if pods>1 else 38
            d.rectangle((20,yy,91,yy+height),NAVY,WHITE,2);d.ellipse((76,yy,106,yy+height),MID,CYAN,2)
            for n in range(3+t):d.line([(29+n*9,yy+3),(29+n*9,yy+height-3)],CYAN,1.5)
            d.line([(94,yy+height/2),(117,yy+height/2)],WHITE,2)
        if kind=='sub_engine':d.line([(109,33),(116,69),(109,103)],WHITE,3);d.ellipse((7,45,24,88),NAVY,CYAN,2)
    elif kind in ('radar','sonar'):
        d.ellipse((27,24,101,98),NAVY,CYAN,3);d.line([(64,61),(93,35-t*2)],WHITE,3)
        if kind=='sonar':
            d.line([(17,89),(35,82),(53,89),(71,82),(89,89),(108,82)],WHITE,2)
        else:d.line([(64,64),(64,113)],CYAN,3)
        for n in range(t+1):d.ellipse((51-n*7,48-n*7,77+n*7,74+n*7),None,MID,1.5)
    elif kind in ('surface_torpedo','sub_torpedo'):
        for n in range(2+(kind=='sub_torpedo')):
            y=35+n*25;d.polygon([(17,y),(91,y),(111,y+7),(91,y+14),(17,y+14)],NAVY,WHITE,2)
            for k in range(t+1):d.line([(27+k*11,y+2),(27+k*11,y+12)],CYAN,1.5)
    elif kind=='depth_charge':
        d.rectangle((18,32,110,100),NAVY,CYAN,3)
        for n in range(3+t):
            x=28+n*12;d.rectangle((x,42,x+7,88),MID,WHITE,1.5)
    elif kind=='deck':
        d.polygon([(26,18),(98,18),(109,107),(18,107)],NAVY,WHITE,3)
        d.line([(63,26),(63,100)],CYAN,2)
        for n in range(3+t):d.line([(32,35+n*12),(50,35+n*12)],CYAN,2)
        d.rectangle((85,39,104,70),MID,CYAN,2)
    elif kind=='armor':
        for n in range(3):d.polygon([(22+n*7,25+n*17),(100+n*2,25+n*17),(91+n*2,55+n*17),(15+n*7,55+n*17)],NAVY,WHITE if n%2 else CYAN,2)
        for n in range(t+1):d.line([(36+n*11,38),(32+n*11,47)],MID,2)
    elif kind=='fire_control':
        d.rectangle((24,26,102,99),NAVY,CYAN,3);d.ellipse((40,41,86,87),NAVY,WHITE,2)
        d.line([(63,33),(63,94)],CYAN,2);d.line([(32,64),(95,64)],CYAN,2)
        for n in range(t+1):d.rectangle((26+n*16,106,34+n*16,113),MID,WHITE,1)
    else:
        barrels={'escort_battery':2,'cruiser_battery':3,'fleet_battery':2,'air_defense':4}[kind]
        d.polygon([(20,54),(72,44),(87,62),(72,85),(20,81)],NAVY,WHITE,3)
        for n in range(barrels):d.line([(65,52+n*8),(119-t*2 if kind=='fleet_battery' else 112-t*2,52+n*8)],CYAN,5 if kind=='fleet_battery' else 3)
        for n in range(t+1):d.line([(26+n*10,61),(26+n*10,75)],MID,2)
    return d

def patch(sprite,dimensions):
    w,h=dimensions;d=Drawing(w,h);highlight='highlight' in sprite;c=WHITE if highlight else CYAN
    fill=MID if highlight else NAVY;cx=w/2;cy=h/2;rx=min(w*.35,30);ry=min(h*.22,16)
    label=sprite.lower()
    if any(v in label for v in ('battery','secondar','anti_air')):
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill,c,1.5)
        for n in range(2+(sum(map(ord,sprite.removesuffix('@highlight')))%2)):
            yy=cy-6+n*6;d.line([(cx,yy),(min(w-1,cx+rx+8),yy)],c,2)
    elif 'torpedo' in label or 'depth' in label or 'mine' in label:
        for n in range(3):d.rectangle((cx-rx+n*rx*.65,cy-ry,cx-rx+n*rx*.65+max(2,rx*.35),cy+ry),fill,c,1)
    elif 'radar' in label or 'sonar' in label:
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),None,c,1.5);d.line([(cx,cy),(cx+rx*.7,cy-ry*.7)],c,1.5)
    elif 'deck' in label or 'armor' in label:
        d.polygon([(cx-rx,cy-ry),(cx+rx,cy-ry),(cx+rx*.8,cy+ry),(cx-rx,cy+ry)],fill,c,1.5)
        d.line([(cx,cy-ry),(cx,cy+ry)],c,1)
    else:
        d.rectangle((cx-rx,cy-ry,cx+rx,cy+ry),fill,c,1.5)
        for n in range(3):d.line([(cx-rx+3+n*rx*.6,cy-ry+3),(cx-rx+3+n*rx*.6,cy+ry-3)],c,1)
    return d

def generate():
    global OUTPUT,ASSETS,SPRITES
    OUTPUT={};ASSETS=[];SPRITES=[]
    if PIL.__version__!='11.3.0':raise ValueError('Use CI-pinned Pillow11.3.0')
    for f in FAMILIES:
        for tier,year in enumerate(YEARS):
            drawing=ship(f.id,tier);source=f'tools/naval_program/source/art/{f.id}_{year}.svg';put(source,drawing.svg())
            icon=texture(f'gfx/AC_naval/research/{f.id}_{year}.dds',fit_subject(drawing,(112,40)),'original research composition',source,family=f.id,year=year)
            bind('GFX_'+tech_id(f.id,year)+'_medium',icon)
            if f.id=='systems':continue
            large=texture(f'gfx/AC_naval/equipment/{f.id}_{year}.dds',fit_subject(drawing,(192,96)),'original equipment composition',source,family=f.id,year=year)
            for ident in (model_id(f.id,year),hull_id(f.id,year)):
                bind('GFX_'+ident,large);bind('GFX_'+ident+'_medium',icon)
            bare=ship(f.id,tier,True);source=f'tools/naval_program/source/art/blueprint_{f.id}_{year}.svg';put(source,bare.svg())
            view=texture(f'gfx/AC_naval/blueprints/{f.id}_{year}.dds',bare.image((508,248)),'original bare ship topview',source,family=f.id,year=year)
            bind('GFX_SD_'+hull_id(f.id,year),view)
    for kind in MODULES:
        for tier,year in enumerate(YEARS):
            drawing=component(kind,tier);source=f'tools/naval_program/source/art/module_{kind}_{year}.svg';put(source,drawing.svg())
            path=texture(f'gfx/AC_naval/modules/{kind}_{year}.dds',drawing.image((64,64)),'original designer module composition',source,component=kind,year=year)
            bind('GFX_EMI_'+module_id(kind,year),path)
    facts=json.loads((HERE/'primary_contract.json').read_text())
    for sprite,row in sorted(facts['layers'].items()):
        if row['kind']=='topview':continue
        ident=layer_name(sprite);drawing=patch(sprite,row['dimensions']);source='tools/naval_program/source/art/'+ident+'.svg';put(source,drawing.svg())
        path=texture('gfx/AC_naval/layers/'+ident+'.dds',drawing.image(tuple(row['dimensions'])),'original normal/highlight category patch',source,consumer_category=sprite,primary_dimensions=row['dimensions'])
        bind(ident,path)
    tab=Image.new('RGBA',(356,30));draw=ImageDraw.Draw(tab)
    for i,c in enumerate((CYAN,WHITE,MID,(151,183,225,255))):draw.rectangle((i*89,0,i*89+88,29),NAVY,c,2)
    path=texture('gfx/AC_naval/ui/tab.dds',tab,'original four-frame research tab',frames=4);bind('GFX_ac_naval_folder_tab',path,4)
    sheet=Image.new('RGBA',(96,96),NAVY);draw=ImageDraw.Draw(sheet);draw.line((0,0,95,0),MID);draw.line((0,0,0,95),MID)
    path=texture('gfx/AC_naval/ui/sheet.dds',sheet,'original tiled briefing background');bind('GFX_ac_naval_sheet',path,tiled=True)
    path=texture('gfx/AC_naval/ui/empty.dds',Image.new('RGBA',(1,1)),'deliberately transparent technical background');bind('GFX_ac_naval_empty',path)
    gfx='spriteTypes = {\n'
    for row in SPRITES:
        gfx+=(f' corneredTileSpriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" size = {{ x = 96 y = 96 }} borderSize = {{ x = 0 y = 0 }} tilingCenter = yes }}\n' if row.get('tiled') else f' spriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" noOfFrames = {row["frames"]} }}\n')
    put('mod/2985041246/interface/ac_naval_art.gfx',gfx+'}\n')
    manifest=dict(schema=1,provenance='Original procedural ship/component/slot geometry and editable SVG masters; no installed/external pixels. Complete and designer defaults intentionally share physical ship imagery.',
        source='tools/naval_program/build_art.py',source_sha256=digest(Path(__file__).read_bytes().replace(b'\r\n',b'\n')),pillow='11.3.0',assets=ASSETS,sprites=SPRITES)
    put('tools/naval_program/assets.json',json.dumps(manifest,indent=2)+'\n');gallery()
    return OUTPUT

def gallery():
    spec=importlib.util.spec_from_file_location('naval_shipped_font_atlas',ROOT/'tools/land_program/render_review.py')
    review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)
    font=review.Atlas('ACBriefing16')
    for name,roles,w,h,cols in [('equipment-gallery',{'original equipment composition'},260,132,4),('technical-gallery',{'original research composition','original designer module composition'},260,106,4),('blueprint-gallery',{'original bare ship topview'},530,290,2),('slot-gallery',{'original normal/highlight category patch'},220,340,6)]:
        rows=[r for r in ASSETS if r['role'] in roles];canvas=Image.new('RGBA',(cols*w,42+((len(rows)+cols-1)//cols)*h),NAVY)
        font.draw(canvas,'OFFLINE ORIGINAL NAVAL ART / '+name,8,8,cols*w-16,24)
        for i,row in enumerate(rows):
            x=i%cols*w;y=42+i//cols*h
            with Image.open(io.BytesIO(OUTPUT[MOD/row['file']])) as image:
                tile=image.convert('RGBA');tile.thumbnail((w-12,h-30));canvas.alpha_composite(tile,(x+6,y))
            budget=76 if name=='slot-gallery' else 25
            label=Path(row['file']).stem.removeprefix('GFX_ac_naval_layer_SM_').replace('_',' ')
            font.draw(canvas,label,x+6,y+h-budget-2,w-12,budget)
        put('docs/evidence/naval-program/'+name+'.png',encode(canvas,'PNG'))
    page='<html><meta charset="utf-8"><title>Original naval technical art</title><style>body{background:#081621;color:#daedf2;font:16px sans-serif}img{max-width:100%}</style><h1>OFFLINE original naval artwork</h1><p>Original geometric masters and native-shaped category apertures; not native designer, mission or fleet evidence.</p>'
    for name in ('equipment-gallery','technical-gallery','blueprint-gallery','slot-gallery'):page+='<h2>'+html.escape(name)+'</h2><img src="'+name+'.png" alt="'+name+'">'
    put('docs/evidence/naval-program/art-index.html',page+'</html>\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();outputs=generate()
    for path,raw in outputs.items():
        if a.check:
            old=path.read_bytes() if path.exists() else b''
            if path.suffix=='.png' and old:
                with Image.open(io.BytesIO(old)) as x,Image.open(io.BytesIO(raw)) as y:
                    if x.size==y.size and x.convert('RGBA').tobytes()==y.convert('RGBA').tobytes():continue
            if path.suffix in ('.json','.gfx','.svg','.html'):old=old.replace(b'\r\n',b'\n')
            if old!=raw:raise SystemExit('Stale original naval artwork: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    print('NAVAL original art:',len(ASSETS),'DDS /',len(SPRITES),'bindings;', 'consistent' if a.check else 'generated')
