"""Original reproducible aircraft/module/blueprint geometry and RGBA DDS."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path

import PIL
from PIL import Image,ImageDraw
from air_content import YEARS,FAMILIES,AIRCRAFT,MODULES,tech_id,model_id,frame_id,module_id

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
NAVY=(8,22,33,255);CYAN=(93,208,223,255);WHITE=(218,237,242,255);MID=(38,91,111,255)
OUTPUT={};ASSETS=[];SPRITES=[]


def digest(raw):return hashlib.sha256(raw).hexdigest()
def encode(im,format='DDS'):
    stream=io.BytesIO();im.convert('RGBA').save(stream,format=format);return stream.getvalue()
def put(path,data):OUTPUT[ROOT/path]=data.encode('utf-8') if isinstance(data,str) else data


class Drawing:
    def __init__(self,width=256,height=128):self.width=width;self.height=height;self.ops=[]
    def line(self,points,color=CYAN,width=2):self.ops.append(('line',points,color,width))
    def polygon(self,points,fill=NAVY,outline=CYAN,width=2):self.ops.append(('polygon',points,fill,outline,width))
    def ellipse(self,bounds,fill=NAVY,outline=CYAN,width=2):self.ops.append(('ellipse',bounds,fill,outline,width))
    def rectangle(self,bounds,fill=NAVY,outline=CYAN,width=2):self.ops.append(('rectangle',bounds,fill,outline,width))
    def image(self,size):
        scale=4;im=Image.new('RGBA',(self.width*scale,self.height*scale));draw=ImageDraw.Draw(im)
        for kind,points,*attrs in self.ops:
            coords=[(round(x*scale),round(y*scale)) for x,y in points] if kind in ('line','polygon') else [round(v*scale) for v in points]
            if kind=='line':draw.line(coords,fill=attrs[0],width=round(attrs[1]*scale),joint='curve')
            else:getattr(draw,kind)(coords,fill=attrs[0],outline=attrs[1],width=round(attrs[2]*scale))
        im.thumbnail(size,Image.Resampling.LANCZOS);result=Image.new('RGBA',size);result.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
        result.putdata([(0,0,0,0) if a<4 else (r,g,b,a) for r,g,b,a in result.getdata()])
        return result
    def svg(self):
        def color(v):return 'none' if v is None else '#%02x%02x%02x'%v[:3]
        rows=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}">']
        for kind,p,*a in self.ops:
            if kind in ('line','polygon'):
                points=' '.join(f'{x},{y}' for x,y in p)
                rows.append(f'<polyline points="{points}" fill="none" stroke="{color(a[0])}" stroke-width="{a[1]}" stroke-linejoin="round"/>' if kind=='line' else f'<polygon points="{points}" fill="{color(a[0])}" stroke="{color(a[1])}" stroke-width="{a[2]}"/>')
            else:
                x,y,r,b=p;attrs=f'fill="{color(a[0])}" stroke="{color(a[1])}" stroke-width="{a[2]}"'
                rows.append(f'<rect x="{x}" y="{y}" width="{r-x}" height="{b-y}" {attrs}/>' if kind=='rectangle' else f'<ellipse cx="{(x+r)/2}" cy="{(y+b)/2}" rx="{(r-x)/2}" ry="{(b-y)/2}" {attrs}/>')
        return '\n'.join(rows+['</svg>'])+'\n'


def aircraft(family,t):
    d=Drawing();center=128
    if family=='systems':
        d.ellipse((26,25,109,108),NAVY,WHITE,3);d.ellipse((42,41,93,92),MID,CYAN,3)
        for n in range(6+t):
            import math
            angle=n*6.283185/(6+t);x=67.5+32*math.cos(angle);y=66.5+32*math.sin(angle)
            d.line([(67.5,66.5),(round(x,3),round(y,3))],CYAN,3)
        d.rectangle((122,29,226,100),NAVY,CYAN,3)
        for n in range(t+2):d.rectangle((134+n*18,45,145+n*18,63),MID,WHITE,2)
        d.line([(133,84),(215,84)],WHITE,3);return d
    if family=='fighter':
        d.polygon([(128,7),(135,35),(137,53),(218,95-t*3),(207,103),(140,83),(141,105),(166+t*3,118),(136,116),(128,106),(120,116),(90-t*3,118),(115,105),(116,83),(49,103),(38,95-t*3),(119,53),(121,35)],NAVY,CYAN,2.8)
        d.ellipse((124,31,132,50),MID,WHITE,2)
        d.line([(128,55),(128,105)],WHITE,2)
        d.line([(113,87),(102-t*3,103),(119,106)],CYAN,2)
        d.line([(143,87),(154+t*3,103),(137,106)],CYAN,2)
    elif family=='strike':
        d.polygon([(128,8),(138,35),(140,60),(221,76+t*2),(221,89),(140,83),(139,105),(167,114),(167,121),(129,114),(89,121),(89,114),(117,105),(116,83),(35,89),(35,76+t*2),(116,60),(118,35)],NAVY,WHITE,2.5)
        d.ellipse((123,33,133,53),MID,CYAN,2)
        for x in (74,99,157,182):d.rectangle((x,77,x+5,96+t),NAVY,CYAN,2)
        d.line([(128,59),(128,107)],CYAN,2)
    elif family=='maritime':
        d.polygon([(128,6),(137,30),(138,63),(232,83-t*2),(232,94),(139,79),(137,109),(165,116),(165,122),(128,116),(91,122),(91,116),(119,109),(117,79),(24,94),(24,83-t*2),(118,63),(119,30)],NAVY,CYAN,2.5)
        d.ellipse((123,29,133,46),MID,WHITE,2)
        d.rectangle((122,87,134,108),NAVY,WHITE,2)
        for x in (83,167):d.ellipse((x,71,x+7,102+t),NAVY,WHITE,2)
        d.line([(129,48),(129,71)],WHITE,2)
    elif family=='transport':
        d.polygon([(128,5),(141,21),(143,55),(237,73),(237,87),(142,75),(139,109),(174,116),(174,123),(128,117),(82,123),(82,116),(117,109),(114,75),(19,87),(19,73),(113,55),(115,21)],NAVY,WHITE,2.5)
        d.line([(122,23),(134,23)],CYAN,3);d.line([(120,34),(136,34)],CYAN,2)
        for x in (72,169):d.rectangle((x,65,x+13,95),NAVY,CYAN,2);d.line([(x+2,91),(x+11,91)],WHITE,2)
        for n in range(t+2):d.line([(122,46+n*13),(134,46+n*13)],CYAN,2)
        d.rectangle((121,101,135,112),MID,CYAN,2)
    elif family=='surveillance':
        d.polygon([(128,5),(136,24),(137,54),(241,69-t),(241,80),(138,69),(137,108),(169,118),(169,123),(128,116),(87,123),(87,118),(119,108),(118,69),(15,80),(15,69-t),(119,54),(120,24)],NAVY,CYAN,2.5)
        for x in (71,172):d.rectangle((x,57,x+12,88),NAVY,WHITE,2)
        d.ellipse((121,31,135,43),MID,WHITE,2);d.ellipse((122,86,134,100),NAVY,WHITE,2)
        d.line([(128,47),(128,78)],WHITE,2)
        for n in range(t+1):d.line([(143+n*13,62),(143+n*13,72)],WHITE,2)
    else:raise ValueError(family)
    if t>=1:d.line([(116,33),(110,45),(115,55)],CYAN,2);d.line([(140,33),(146,45),(141,55)],CYAN,2)
    if t>=2:d.rectangle((124,71,132,78+t),MID,WHITE,2)
    if t>=3:d.line([(128,8),(128,18)],WHITE,3)
    return d


def component(kind,t):
    d=Drawing(128,128)
    if kind in ('single_engine','twin_engine'):
        centers=(43,85) if kind=='twin_engine' else (64,)
        for x in centers:
            d.ellipse((x-20,33,x+20,75),NAVY,WHITE,2.5);d.ellipse((x-11,43,x+11,65),MID,CYAN,2)
            d.line([(x-18,73),(x-12,103),(x+12,103),(x+18,73)],CYAN,2.5)
            for n in range(t+2):d.line([(x-9,80+n*5),(x+9,80+n*5)],WHITE,1.5)
    elif kind=='fighter_armament':
        d.rectangle((20,58,81,77),NAVY,CYAN,3);d.rectangle((73,60,113,68),NAVY,WHITE,2)
        d.ellipse((31,19,68,52),NAVY,WHITE,2);d.line([(49,13),(49,57)],CYAN,2);d.line([(25,36),(75,36)],CYAN,2)
        for n in range(t+1):d.line([(26+n*12,82),(26+n*12,101)],CYAN,3)
    elif kind in ('strike_armament','maritime_armament'):
        d.line([(18,24),(110,24)],WHITE,4)
        for x in ((38,85) if kind=='strike_armament' else (63,)):
            d.polygon([(x,35),(x+9,49),(x+9,91),(x,105),(x-9,91),(x-9,49)],NAVY,CYAN,2)
            d.line([(x-12,82),(x+12,82)],WHITE,2)
            if kind=='maritime_armament':d.line([(x-18,59),(x,67),(x+18,59)],WHITE,3)
            for n in range(t+1):d.line([(x-5,54+n*7),(x+5,54+n*7)],CYAN,1.5)
    elif kind=='camera':
        d.rectangle((21,30,108,98),NAVY,CYAN,3);d.ellipse((42,39,96,91),MID,WHITE,3);d.ellipse((54,51,84,79),NAVY,CYAN,2)
        for n in range(t+1):d.rectangle((27+n*12,18,34+n*12,31),NAVY,WHITE,2)
    elif kind=='flight_controls':
        d.rectangle((16,28,111,102),NAVY,CYAN,3);d.ellipse((27,43,66,82),MID,WHITE,2)
        d.line([(34,64),(46,56),(59,66)],WHITE,2);d.line([(73,43),(102,43)],CYAN,3)
        for n in range(t+2):d.rectangle((74,55+n*10,98,59+n*10),MID,WHITE,1.5)
    elif kind=='maritime_sensors':
        d.polygon([(25,31),(100,31),(86,65),(64,79),(39,65)],NAVY,WHITE,3)
        d.line([(64,45),(64,105)],CYAN,3);d.line([(39,106),(89,106)],WHITE,3)
        for n in range(t+1):d.line([(21+n*7,80),(31+n*7,88)],CYAN,2)
    else:raise ValueError(kind)
    return d


def texture(path,im,role,source=None,frames=1,**meta):
    raw=encode(im);put('mod/2985041246/'+path,raw);low,high=im.getchannel('A').getextrema()
    row=dict(file=path,width=im.width,height=im.height,frames=frames,frame_width=im.width//frames,format='DDS RGBA8',alpha_min=low,alpha_max=high,sha256=digest(raw),role=role,**meta)
    if source:row.update(source=source,source_sha256=digest(OUTPUT[ROOT/source]))
    ASSETS.append(row);return path
def bind(name,path,frames=1,**metadata):SPRITES.append(dict(name=name,asset=path,frames=frames,**metadata))


def generate():
    global OUTPUT,ASSETS,SPRITES
    OUTPUT={};ASSETS=[];SPRITES=[]
    if PIL.__version__!='11.3.0':raise ValueError('Use CI-pinned Pillow11.3.0 for reproducible DDS')
    for family in FAMILIES:
        for tier,year in enumerate(YEARS):
            drawing=aircraft(family.id,tier);source=f'tools/air_program/source/art/{family.id}_{year}.svg';put(source,drawing.svg())
            icon=texture(f'gfx/AC_air/research/{family.id}_{year}.dds',drawing.image((112,40)),'original research composition',source,family=family.id,year=year)
            bind('GFX_'+tech_id(family.id,year)+'_medium',icon)
            if family.id=='systems':continue
            large=texture(f'gfx/AC_air/equipment/{family.id}_{year}.dds',drawing.image((192,96)),'original equipment composition',source,family=family.id,year=year)
            bind('GFX_'+model_id(family.id,year),large);bind('GFX_'+model_id(family.id,year)+'_medium',icon)
            if family.airframe_parent:
                bind('GFX_'+frame_id(family.id,year),large);bind('GFX_'+frame_id(family.id,year)+'_medium',icon)
                blueprint=drawing.image((508,248));draw=ImageDraw.Draw(blueprint)
                draw.line((8,124,500,124),fill=MID,width=1);draw.line((254,5,254,242),fill=MID,width=1)
                blueprint_path=texture(f'gfx/AC_air/blueprints/{family.id}_{year}.dds',blueprint,'original designer blueprint overlay',source,family=family.id,year=year)
                bind('GFX_TC_'+frame_id(family.id,year),blueprint_path)
    for kind in MODULES:
        for tier,year in enumerate(YEARS):
            drawing=component(kind,tier);source=f'tools/air_program/source/art/module_{kind}_{year}.svg';put(source,drawing.svg())
            path=texture(f'gfx/AC_air/modules/{kind}_{year}.dds',drawing.image((64,64)),'original designer module composition',source,component=kind,year=year)
            bind('GFX_EMI_'+module_id(kind,year),path)
    tab=Image.new('RGBA',(356,30));draw=ImageDraw.Draw(tab)
    for index,color in enumerate((CYAN,WHITE,MID,(151,183,225,255))):
        x=index*89;draw.rectangle((x,0,x+88,29),fill=NAVY,outline=color,width=2);draw.line((x+7,25,x+81,25),fill=color,width=1)
    path=texture('gfx/AC_air/ui/tab.dds',tab,'original four-frame research tab',frames=4);bind('GFX_ac_air_folder_tab',path,4)
    sheet=Image.new('RGBA',(96,96),NAVY);draw=ImageDraw.Draw(sheet);draw.line((0,0,95,0),fill=MID);draw.line((0,0,0,95),fill=MID)
    path=texture('gfx/AC_air/ui/sheet.dds',sheet,'original tiled briefing background');bind('GFX_ac_air_sheet',path,tiled=True)
    gfx='spriteTypes = {\n'
    for row in SPRITES:
        gfx+=(f' corneredTileSpriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" size = {{ x = 96 y = 96 }} borderSize = {{ x = 0 y = 0 }} tilingCenter = yes }}\n' if row.get('tiled') else
              f' spriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" noOfFrames = {row["frames"]} }}\n')
    put('mod/2985041246/interface/ac_air_art.gfx',gfx+'}\n')
    manifest=dict(schema=1,provenance='Original editable code-native geometry; no installed/external pixels or national portraits. Related complete/designer defaults intentionally share their physical aircraft art.',
        source='tools/air_program/build_art.py',source_sha256=digest(Path(__file__).read_bytes().replace(b'\r\n',b'\n')),pillow='11.3.0',assets=ASSETS,sprites=SPRITES)
    put('tools/air_program/assets.json',json.dumps(manifest,indent=2)+'\n');gallery()
    return OUTPUT


def gallery():
    # Use actual shipped glyphs for platform-independent review labels.
    import re
    source=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text();metrics={}
    for line in source.splitlines():
        if line.startswith('char '):
            row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};metrics[row['id']]=row
    atlas=Image.open(MOD/'gfx/fonts/ACBriefing16.dds').convert('RGBA')
    def label(canvas,text,x,y):
        for char in text:
            m=metrics[ord(char)];tile=atlas.crop((m['x'],m['y'],m['x']+m['width'],m['y']+m['height']))
            canvas.alpha_composite(tile,(x+m['xoffset'],y+m['yoffset']));x+=m['xadvance']
    for basename,roles,w,h in [('equipment-gallery',{'original equipment composition'},310,140),('technical-gallery',{'original research composition','original designer module composition'},310,112),('blueprint-gallery',{'original designer blueprint overlay'},570,300)]:
        rows=[r for r in ASSETS if r['role'] in roles];cols=2 if basename=='blueprint-gallery' else 4
        canvas=Image.new('RGBA',(cols*w,50+((len(rows)+cols-1)//cols)*h),NAVY);label(canvas,'OFFLINE ORIGINAL AVIATION ART / '+basename,12,10)
        for index,row in enumerate(rows):
            x=(index%cols)*w;y=(index//cols)*h+45;im=Image.open(io.BytesIO(OUTPUT[MOD/row['file']])).convert('RGBA')
            canvas.alpha_composite(im,(x+12,y+3));label(canvas,Path(row['file']).stem,x+12,y+h-25)
        put('docs/evidence/air-program/'+basename+'.png',encode(canvas,'PNG'))
    page='<html><meta charset="utf-8"><title>Original aviation technical art</title><style>body{background:#081621;color:#daedf2;font:16px sans-serif}img{max-width:100%}</style><h1>Original aviation: offline asset review</h1><p>Editable geometric compositions, not native designer screenshots or mission evidence. No national leader images or official hardware claims.</p>'
    for name in ('equipment-gallery','technical-gallery','blueprint-gallery'):page+='<h2>'+html.escape(name)+'</h2><img src="'+name+'.png" alt="'+name+'">'
    put('docs/evidence/air-program/art-index.html',page+'</html>\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();outputs=generate()
    for path,raw in outputs.items():
        if args.check:
            old=path.read_bytes() if path.exists() else b''
            if path.suffix=='.png' and old:
                with Image.open(io.BytesIO(old)) as a,Image.open(io.BytesIO(raw)) as b:
                    if a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes():continue
            if path.suffix in ('.json','.gfx','.svg','.html'):old=old.replace(b'\r\n',b'\n')
            if old!=raw:raise SystemExit('Stale aviation artwork: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    print('Aviation art:',len(ASSETS),'DDS /',len(SPRITES),'sprites;', 'consistent' if args.check else 'packaged')
