"""Original editable technical geometry. Pillow11.3 packages deterministic DDS.

No game pixels, external artwork or raster masters are inputs. Python geometry
is authoritative; SVG exports retain every editable shape for art review.
"""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import sys

import PIL
from PIL import Image,ImageDraw,ImageFont
from land_content import FAMILIES,YEARS,MODULES,module_id,model_id,chassis_id

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
NAVY=(8,22,33,255);CYAN=(93,208,223,255);WHITE=(218,237,242,255);MID=(38,91,111,255)
OUTPUT={};ASSETS=[];SPRITES=[];SOURCES={}


def digest(data):return hashlib.sha256(data).hexdigest()
def encode(im,fmt='DDS'):
    stream=io.BytesIO();im.save(stream,format=fmt);return stream.getvalue()
def put(path,data):OUTPUT[ROOT/path]=data.encode('utf-8') if isinstance(data,str) else data


class Drawing:
    def __init__(self):self.ops=[]
    def line(self,points,color=CYAN,width=4):self.ops.append(('line',points,color,width))
    def polygon(self,points,fill=NAVY,outline=CYAN,width=3):self.ops.append(('polygon',points,fill,outline,width))
    def rectangle(self,box,fill=NAVY,outline=CYAN,width=3):self.ops.append(('rectangle',box,fill,outline,width))
    def ellipse(self,box,fill=NAVY,outline=CYAN,width=3):self.ops.append(('ellipse',box,fill,outline,width))
    def image(self,size):
        scale=4;im=Image.new('RGBA',(256*scale,128*scale));d=ImageDraw.Draw(im)
        for op in self.ops:
            kind,points=op[:2]
            scaled=[(x*scale,y*scale) for x,y in points] if kind in ('line','polygon') else [v*scale for v in points]
            if kind=='line':d.line(scaled,fill=op[2],width=op[3]*scale,joint='curve')
            else:getattr(d,kind)(scaled,fill=op[2],outline=op[3],width=op[4]*scale)
        im.thumbnail(size,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',size)
        canvas.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
        # Lanczos unpremultiplication can create bright arbitrary RGB values
        # at alpha1. Remove that invisible fringe rather than shipping yellow
        # edge specks around deliberately transparent briefing geometry.
        canvas.putdata([(0,0,0,0) if a<4 else (r,g,b,a) for r,g,b,a in canvas.getdata()])
        return canvas
    def svg(self):
        def color(v):return 'none' if v is None else '#%02x%02x%02x'%v[:3]
        rows=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 128">']
        for op in self.ops:
            kind,p=op[:2]
            if kind=='line':rows.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="none" stroke="{color(op[2])}" stroke-width="{op[3]}" stroke-linejoin="round"/>')
            elif kind=='polygon':rows.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{color(op[2])}" stroke="{color(op[3])}" stroke-width="{op[4]}"/>')
            else:
                a,b,c,d=p;attrs=f'fill="{color(op[2])}" stroke="{color(op[3])}" stroke-width="{op[4]}"'
                rows.append(f'<rect x="{a}" y="{b}" width="{c-a}" height="{d-b}" {attrs}/>' if kind=='rectangle' else f'<ellipse cx="{(a+c)/2}" cy="{(b+d)/2}" rx="{(c-a)/2}" ry="{(d-b)/2}" {attrs}/>')
        return '\n'.join(rows+['</svg>'])+'\n'


def wheels(d,points,r=10):
    for x,y in points:d.ellipse((x-r,y-r,x+r,y+r),NAVY,CYAN,3)


def subject(family,tier,technical=False):
    d=Drawing();t=tier
    if family=='infantry':
        d.polygon([(22,61),(58,48),(151,48),(164,55),(218,55),(218,63),(163,65),(147,77),(91,77),(72,69),(42,75)])
        d.polygon([(99,76),(122,76),(118,103),(101,98)])
        d.line([(75,67),(68,90),(80,94)],WHITE,4);d.line([(48,48),(141,48)],WHITE,3)
        d.rectangle((102,35,132+3*t,45),NAVY,WHITE,3)
        d.line([(146,68),(159,86)],CYAN,4)
        for n in range(t+1):d.line([(151+n*12,49),(151+n*12,61)],WHITE,2)
        if t>1:d.rectangle((163,69,184+4*t,77),MID,CYAN,2)
    elif family in ('mobility','mbt','tracked_artillery'):
        d.polygon([(23,76),(42,57),(183,57),(214,75),(205,97),(35,97)])
        wheels(d,[(x,96) for x in (48,78,108,138,168,195)],8)
        if family=='mobility':
            d.polygon([(54,57),(66,35),(173,35),(191,57)],NAVY,WHITE,3)
            d.rectangle((77,40,101,52),MID,WHITE,2);d.rectangle((110,40,134,52),MID,WHITE,2)
            d.line([(153,37),(157,18+t*3)],WHITE,3)
        else:
            if family=='mbt':
                d.polygon([(65,57),(81,31),(145,31),(168,48),(152,60)],NAVY,WHITE,3)
                d.polygon([(153,42),(230,38-t*2),(233,45-t*2),(158,50)],NAVY,CYAN,3)
            else:
                d.polygon([(68,58),(70,24),(135,24),(163,56)],NAVY,WHITE,3)
                d.polygon([(140,31),(228,13+t*2),(232,20+t*2),(147,42)],NAVY,CYAN,4)
                for x in range(82,126,12):d.line([(x,31),(x,49)],CYAN,2)
        for n in range(t+1):d.rectangle((58+n*27,65,78+n*27,78),MID,CYAN,2)
        if t>=1:d.rectangle((120,22,137+3*t,29),MID,CYAN,2)
        if t>=2:d.line([(51,57),(49,21),(60,21)],WHITE,3)
        if technical:
            d.line([(26,109),(212,109)],MID,2)
            for x in (48,108,168):d.line([(x,102),(x,116)],WHITE,2)
    elif family=='support':
        d.rectangle((54,43,178,103),NAVY,CYAN,4);d.rectangle((84,25,147,43),NAVY,WHITE,3)
        d.line([(58,65),(174,65)],WHITE,3);d.rectangle((108,57,126,73),MID,CYAN,3)
        d.line([(174,28),(204,59),(213,49),(184,19)],WHITE,5)
        for n in range(t+1):d.line([(72+n*24,78),(72+n*24,93)],CYAN,3)
    elif family=='logistics':
        d.rectangle((28,36,150,83),NAVY,CYAN,4)
        d.polygon([(153,49),(179,49),(205,69),(205,92),(152,92)],NAVY,WHITE,3)
        d.polygon([(163,55),(176,55),(193,69),(163,69)],MID,CYAN,2)
        wheels(d,[(59,94),(113,94),(179,94)],12)
        for n in range(t+1):d.line([(45+n*23,43),(45+n*23,75)],WHITE,2)
        if t>=2:d.rectangle((152,38,183,45),MID,CYAN,3)
    elif family=='surveillance':
        d.line([(67,89),(67,24)],WHITE,4)
        d.ellipse((33,16,98,53),NAVY,CYAN,4);d.line([(67,34),(97,21)],WHITE,3)
        d.line([(47,104),(67,84),(87,104)],CYAN,4)
        d.rectangle((119,46,214,101),NAVY,WHITE,4);d.rectangle((130,57,202,87),MID,CYAN,2)
        for n in range(t+1):d.line([(142+n*15,64),(142+n*15,79)],WHITE,3)
        if t>=1:d.ellipse((146,20,161+5*t,35+2*t),NAVY,CYAN,3)
    elif family=='electronic_support':
        d.rectangle((67,49,176,104),NAVY,CYAN,4);d.rectangle((79,63,125,83),MID,WHITE,3)
        d.line([(158,50),(158,13)],WHITE,4);d.line([(148,25),(158,14),(170,25)],CYAN,3)
        d.line([(40,65),(28,77),(40,89)],WHITE,3);d.line([(202,65),(215,77),(202,89)],WHITE,3)
        for n in range(t+1):d.ellipse((136+n*9,67,141+n*9,73),CYAN,CYAN,1)
        if t>=2:d.rectangle((87,33,121+5*t,43),NAVY,WHITE,3)
    else:raise ValueError(family)
    return d


def component(kind,tier):
    d=Drawing();t=tier
    if kind in ('gun','howitzer'):
        angle=0 if kind=='gun' else 18
        d.rectangle((37,52,98,86),NAVY,WHITE,4)
        d.polygon([(91,57),(226,50-angle),(227,62-angle),(92,72)],NAVY,CYAN,4)
        d.line([(62,86),(44,105),(117,105),(82,86)],CYAN,4)
        for n in range(t+1):d.line([(110+n*22,53-angle*.25),(110+n*22,64-angle*.25)],WHITE,3)
    elif kind in ('turret','artillery_turret'):
        roof=26 if kind=='turret' else 15
        d.polygon([(37,87),(60,roof),(155,roof),(194,65),(180,94)],NAVY,CYAN,4)
        d.line([(51,98),(185,98)],WHITE,4)
        for n in range(t+1):d.rectangle((76+n*23,roof+10,89+n*23,roof+24),MID,WHITE,2)
    elif kind=='protection':
        for n in range(3+t):
            x=38+n*16;y=24+n*7
            d.polygon([(x,y),(x+94,y),(x+112,y+42),(x+50,y+70),(x-10,y+42)],NAVY,CYAN if n%2 else WHITE,3)
    elif kind=='powertrain':
        d.rectangle((43,45,194,95),NAVY,CYAN,4)
        for n in range(3+t):d.rectangle((54+n*22,25,70+n*22,45),MID,WHITE,3)
        d.ellipse((103,57,138,89),NAVY,WHITE,3);d.line([(193,61),(220,61),(220,94)],WHITE,4)
    elif kind=='running_gear':
        d.rectangle((31,39,224,99),NAVY,CYAN,4);wheels(d,[(x,70) for x in (54,94,134,174,207)],13)
        for n in range(t+1):d.line([(56+n*39,47),(79+n*39,85)],WHITE,3)
    elif kind=='optics':
        d.polygon([(44,39),(165,39),(192,59),(192,92),(44,92)],NAVY,CYAN,4)
        for n in range(2+t):d.ellipse((57+n*27,51,76+n*27,80),MID,WHITE,3)
        d.line([(67,28),(67,15),(172,15),(172,28)],CYAN,3)
    elif kind=='protected_radio':
        d.rectangle((55,48,187,104),NAVY,CYAN,4);d.line([(168,48),(168,14)],WHITE,4)
        d.rectangle((68,61,127,87),MID,WHITE,3)
        for n in range(t+1):d.line([(137+n*10,62),(137+n*10,88)],CYAN,3)
        d.line([(193,22),(210,35),(193,48)],CYAN,3)
    else:raise ValueError(kind)
    return d


def binding(name,asset,frames=1):
    SPRITES.append(dict(name=name,asset=asset,frames=frames))


def texture(path,im,role,frames=1,source=None,**meta):
    data=encode(im.convert('RGBA'));put('mod/2985041246/'+path,data)
    alpha=im.getchannel('A')
    row=dict(file=path,width=im.width,height=im.height,frames=frames,frame_width=im.width//frames,
        format='DDS RGBA8',alpha_min=alpha.getextrema()[0],alpha_max=alpha.getextrema()[1],sha256=digest(data),role=role,**meta)
    if source:row['source']=source;row['source_sha256']=digest(OUTPUT[ROOT/source])
    ASSETS.append(row);return path


def generate():
    global OUTPUT,ASSETS,SPRITES,SOURCES
    OUTPUT={};ASSETS=[];SPRITES=[];SOURCES={}
    if PIL.__version__!='11.3.0':raise RuntimeError('Use the CI-pinned Pillow11.3.0 for byte-reproducible DDS')
    for family in FAMILIES:
        for tier,year in enumerate(YEARS):
            drawing=subject(family.id,tier);svg=f'tools/land_program/source/art/{family.id}_{year}.svg';put(svg,drawing.svg())
            small=texture(f'gfx/AC_land/research/{family.id}_{year}.dds',drawing.image((112,40)),'original research composition',source=svg,family=family.id,year=year)
            large=texture(f'gfx/AC_land/equipment/{family.id}_{year}.dds',drawing.image((192,96)),'original equipment composition',source=svg,family=family.id,year=year)
            binding(f'GFX_ac_land_{family.id}_{year}_medium',small)
            ident=model_id(family.id,year)
            for name,target in [(f'GFX_{ident}',large),(f'GFX_{ident}_medium',small)]:binding(name,target)
            if family.id in ('mbt','tracked_artillery'):
                for suffix,target in [('',large),('_medium',small)]:binding('GFX_'+chassis_id(family.id,year)+suffix,target)
    for kind in MODULES:
        for tier,year in enumerate(YEARS):
            drawing=component(kind,tier);svg=f'tools/land_program/source/art/module_{kind}_{year}.svg';put(svg,drawing.svg())
            asset=texture(f'gfx/AC_land/modules/{kind}_{year}.dds',drawing.image((64,64)),'original designer module composition',source=svg,component=kind,year=year)
            binding('GFX_EMI_'+module_id(kind,year),asset)
    for family in ('surveillance','electronic_support'):
        for size,frame in [('medium',(76,42)),('small',(30,12))]:
            strip=Image.new('RGBA',(frame[0]*2,frame[1]));drawing=subject(family,1)
            normal=drawing.image(frame);strip.alpha_composite(normal,(0,0))
            selected=normal.copy()
            selected.putdata([(*((NAVY if b>90 and g>80 else WHITE)[:3]),a) for r,g,b,a in normal.getdata()])
            strip.alpha_composite(selected,(frame[0],0))
            source=f'tools/land_program/source/art/{family}_2010.svg'
            asset=texture(f'gfx/AC_land/counters/{family}_{size}.dds',strip,'original support counter selection strip',frames=2,source=source)
            binding('GFX_unit_ac_land_'+family+'_company_icon_'+size,asset,2)
    for archetype,family in [('ac_land_sensor_equipment','surveillance'),('ac_land_electronic_equipment','electronic_support')]:
        binding('GFX_'+archetype,f'gfx/AC_land/equipment/{family}_2006.dds')
        binding('GFX_'+archetype+'_medium',f'gfx/AC_land/research/{family}_2006.dds')
    tab=Image.new('RGBA',(89*4,30))
    for state,color in enumerate((CYAN,WHITE,MID,(151,183,225,255))):
        d=ImageDraw.Draw(tab);x=89*state;d.rectangle((x,0,x+88,29),fill=NAVY,outline=color,width=2);d.line((x+7,25,x+81,25),fill=color,width=1)
    asset=texture('gfx/AC_land/ui/land_tab.dds',tab,'original four-frame research tab',frames=4)
    binding('GFX_ac_land_folder_tab',asset,4)
    sheet=Image.new('RGBA',(96,96),NAVY);d=ImageDraw.Draw(sheet)
    d.line((0,0,95,0),fill=MID,width=1);d.line((0,0,0,95),fill=MID,width=1)
    asset=texture('gfx/AC_land/ui/sheet.dds',sheet,'original tiled briefing sheet')
    SPRITES.append(dict(name='GFX_ac_land_sheet',asset=asset,frames=1,tiled=True))
    gfx='spriteTypes = {\n'
    for row in SPRITES:
        if row.get('tiled'):
            gfx+=f' corneredTileSpriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" size = {{ x = 96 y = 96 }} borderSize = {{ x = 0 y = 0 }} tilingCenter = yes }}\n'
        else:gfx+=f' spriteType = {{ name = "{row["name"]}" texturefile = "{row["asset"]}" noOfFrames = {row["frames"]} }}\n'
    gfx+='}\n';put('mod/2985041246/interface/ac_land_art.gfx',gfx)
    code=Path(__file__).read_bytes().replace(b'\r\n',b'\n')
    manifest=dict(schema=1,provenance='Original code-native geometry; no installed or external pixels. Python geometry is editable master; SVGs are reproducible editable exports.',
        source='tools/land_program/build_art.py',source_sha256=digest(code),pillow='11.3.0',
        reference_shapes='Counter dimensions76x42 and30x12 per frame, two frames, inspected from installed1.19.4.1 rangers-support bindings; no pixels copied.',
        reference_frame_contracts={'interface/subuniticons.gfx:GFX_unit_rangers_support_icon_medium':dict(width=152,height=42,frames=2),
                                   'interface/texticons.gfx:GFX_unit_rangers_support_icon_small':dict(width=60,height=12,frames=2)},
        assets=ASSETS,sprites=SPRITES)
    put('tools/land_program/assets.json',json.dumps(manifest,indent=2)+'\n')
    gallery()
    return OUTPUT


def gallery():
    font=ImageFont.truetype(str(ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'),16)
    rows=[]
    for row in ASSETS:
        if row['role'] in ('original research composition','original designer module composition','original support counter selection strip'):rows.append(row)
    cols=4;w=310;h=116
    canvas=Image.new('RGBA',(cols*w,((len(rows)+cols-1)//cols)*h+55),NAVY);d=ImageDraw.Draw(canvas)
    d.text((16,12),'OFFLINE ASSET REVIEW / ORIGINAL LAND ART',font=font,fill=WHITE)
    for index,row in enumerate(rows):
        x=(index%cols)*w;y=(index//cols)*h+50;im=Image.open(io.BytesIO(OUTPUT[MOD/row['file']])).convert('RGBA')
        if 'counter' in row['role']:im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
        canvas.alpha_composite(im,(x+8,y+5));label=Path(row['file']).stem
        d.text((x+8,y+88),label,font=font,fill=WHITE)
    put('docs/evidence/land-program/asset-gallery.png',encode(canvas,'PNG'))
    equipment=[row for row in ASSETS if row['role']=='original equipment composition']
    large=Image.new('RGBA',(4*310,8*146+55),NAVY);draw=ImageDraw.Draw(large)
    draw.text((16,12),'OFFLINE EQUIPMENT COMPOSITIONS / ORIGINAL LAND ART',font=font,fill=WHITE)
    for index,row in enumerate(equipment):
        x=(index%4)*310;y=(index//4)*146+50
        large.alpha_composite(Image.open(io.BytesIO(OUTPUT[MOD/row['file']])).convert('RGBA'),(x+8,y+5))
        draw.text((x+8,y+112),Path(row['file']).stem,font=font,fill=WHITE)
    put('docs/evidence/land-program/equipment-gallery.png',encode(large,'PNG'))
    body='<html><meta charset="utf-8"><title>Land artwork offline review</title><style>body{background:#081621;color:#daedf2;font:16px sans-serif}img{max-width:100%}</style><h1>Offline original-art review</h1><p>Technical artwork only. This is not a native research-screen screenshot or engine acceptance.</p><img src="asset-gallery.png" alt="All research, module and counter compositions"><ul>'
    body+='<img src="equipment-gallery.png" alt="All32 complete-equipment compositions">'
    for row in ASSETS:body+='<li>'+html.escape(row['file'])+f' — {row["width"]}×{row["height"]}, {row["frames"]}frame(s)</li>'
    put('docs/evidence/land-program/asset-gallery.html',body+'</ul></html>')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=generate()
    for path,data in outputs.items():
        if args.check:
            existing=path.read_bytes() if path.exists() else b''
            if path.suffix.lower() in ('.json','.svg','.html','.gfx'):existing=existing.replace(b'\r\n',b'\n')
            if existing!=data:raise SystemExit('Stale land art: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Land art',len(ASSETS),'textures /',len(SPRITES),'sprite bindings:', 'consistent' if args.check else 'packaged')
