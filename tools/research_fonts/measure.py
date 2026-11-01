"""Offline font rectangles/role samples; never a native screenshot."""
import argparse
import importlib.util
import io
import json
from pathlib import Path
import sys

from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/land_program')]
from script import parse
from research_fonts.build import SOURCE,inventory
from research_fonts.policy import BINDINGS
from research_fonts.metrics import envelope,text_ink,fits
from render_review import Atlas
spec=importlib.util.spec_from_file_location('research_fonts_measure_land',ROOT/'tools/land_program/build_ui.py')
land=importlib.util.module_from_spec(spec);spec.loader.exec_module(land)
OUT=ROOT/'docs/evidence/research-fonts'

SAMPLES=[
 ('hoi_36header','2020',80,32),
 ('hoi_33','INFANTRY SYSTEMS',200,62),
 ('hoi_22tech','Electronic engineering',200,122),
 ('hoi_20bs','Service equipment',160,20),
 ('hoi4_typewriter16','Maximum speed',160,20),
 ('hoi4_typewriter16_inverted','+125.5%',100,20),
 ('hoi4_typewriter22','Service buildings',200,20),
 ('hoi_20b','RESEARCH',261,34),
 ('hoi_20bs','Émile Černý',160,20),
 ('hoi4_typewriter16_inverted','ÂÊÎÔÛ ĂŮŴ',160,20),
]


def rgb(color):return tuple(int(color[i:i+2],16)for i in(4,6,8))


def paint(font,canvas,text,x,y,width,height,color):
    lines=font.wrap(text,width)
    if len(lines)*font.height>height:raise ValueError('Review sample exceeds its actual control budget: '+text)
    bounds=text_ink(font,lines)
    if not fits(bounds,width,height):raise ValueError('Review sample ink exceeds its actual control budget: '+text+' '+str(bounds))
    for line in lines:
        cursor=x;previous=None
        for char in line:
            ident=ord(char);row=font.rows[ident];cursor+=font.kern.get((previous,ident),0)
            glyph=font.atlas.crop((row['x'],row['y'],row['x']+row['width'],row['y']+row['height']))
            ink=Image.new('RGBA',glyph.size,(*color,255));ink.putalpha(glyph.getchannel('A'))
            canvas.alpha_composite(ink,(cursor+row['xoffset'],y+row['yoffset']))
            cursor+=row['xadvance'];previous=ident
        y+=font.height
    return dict(lines=len(lines),line_height=font.height,wrapped_height=len(lines)*font.height,
                measured_line_widths=[font.measure(line)for line in lines],ink_bounds=bounds,max_width=width,max_height=height)


def outputs():
    original=parse(SOURCE.read_text(encoding='utf-8-sig'));current=parse(land.TARGET.read_text(encoding='utf-8-sig'))
    if land.normalized(current)!=original:raise ValueError('Original research control geometry/contract changed')
    primary=json.loads((HERE/'primary_contract.json').read_text());fonts={name:Atlas(name)for name in('ACBriefing16','ACBriefing20')}
    shapes={name:envelope(font)for name,font in fonts.items()}
    rows=[];failures=[]
    for row in inventory(original):
        binding=BINDINGS[row['font']];font=fonts[binding.atlas]
        height=int(row['max_height'])if row['max_height']is not None else None
        width=int(row['max_width'])if row['max_width']is not None else None
        text=(row['text']or'').strip('"');year=text if len(text)==4 and text.isdigit()else None
        entry=dict(**row,current_font=binding.name,original_line_height=primary['fonts'][row['font']]['metrics']['lineHeight'],
            current_line_height=font.height,declared_width=width,declared_height=height,
            full_atlas_ink_top=shapes[binding.atlas]['ink_top'],full_atlas_ink_bottom=shapes[binding.atlas]['ink_bottom'],
            year_width=font.measure(year)if year else None,year_ink=text_ink(font,[year])if year else None)
        if height is not None and font.height>height:failures.append(dict(path=row['path'],reason='line height exceeds declared rectangle'))
        if shapes[binding.atlas]['ink_top']<0 or height is not None and shapes[binding.atlas]['ink_bottom']>height:
            failures.append(dict(path=row['path'],reason='actual glyph alpha extends beyond vertical rectangle'))
        if year and font.measure(year)>width:failures.append(dict(path=row['path'],reason='literal year exceeds declared width'))
        if year and not fits(text_ink(font,[year]),width,height):failures.append(dict(path=row['path'],reason='literal year alpha extends beyond rectangle'))
        rows.append(entry)
    canvas=Image.new('RGBA',(1050,140+sum(max(132,h+72)for _,_,_,h in SAMPLES)),(8,22,33,255));draw=ImageDraw.Draw(canvas);body=fonts['ACBriefing16']
    paint(body,canvas,'RESEARCH TYPOGRAPHY / OFFLINE SOURCE REVIEW',24,18,980,40,(218,237,242))
    paint(body,canvas,'Existing authored glyph atlases. Rectangles remain unchanged. This is not a native screenshot.',24,54,980,40,(130,175,194))
    samples=[]
    top=112
    for old,text,width,height in SAMPLES:
        binding=BINDINGS[old];font=fonts[binding.atlas]
        paint(body,canvas,old+' -> '+binding.name,24,top,970,28,(130,175,194))
        origin=(30,top+38);draw.rectangle((origin[0]-1,origin[1]-1,origin[0]+width,origin[1]+height),outline=(87,204,232,255))
        measure=paint(font,canvas,text,*origin,width,height,rgb(binding.color))
        paint(body,canvas,'Budget '+str(width)+' x '+str(height)+' / line '+str(font.height),520,top+46,480,28,(218,237,242))
        samples.append(dict(source_font=old,font=binding.name,text=text,**measure))
        top+=max(132,height+72)
    report=dict(schema=1,coverage='Actual inherited rectangle/atlas measurements and illustrative role samples; not native rendering or all dynamic strings',
        migrated_assignments=len(rows),current_font_assignments=len(inventory(current)),original_gui_contract_preserved=True,
        protected_source_hash_count=1050,declared_text_rectangles=sum(r['declared_height']is not None for r in rows),
        literal_years_checked=sum(r['year_width']is not None for r in rows),
        previous_font_line_overruns=sum(r['declared_height']is not None and r['original_line_height']>r['declared_height']for r in rows),
        findings=failures,controls=rows,samples=samples,atlas_alpha_envelopes=shapes,native_acceptance=False,
        limits=['Dynamic technology/stat strings retain their original maximum rectangles and engine tooltips; no universal dynamic-string fit is claimed.',
            'Both inherited narrative rectangles keep their reviewed scrollbars; a line-height check does not prove native scrolling.',
            'Original language-specific engine fallback fonts are not imported; English source coverage only.',
            'Existing authored atlases have horizontal side bearings (some letters extend one pixel left, fraction slash three); arbitrary dynamic-name clipping needs native coverage and is not certified by the passing vertical/literal checks.',
            'Compact baseline adapters were rejected: shifting the sixteen/twenty-point atlases by minus three/four clips accented capitals above y=0 despite apparently fitting lineHeight/base metadata.',
            'Pixel hinting, state coloring/substitution, UI scaling and input still need separately resumed native acceptance.'])
    if failures:raise ValueError('Research font budget failures: '+str(failures))
    buffer=io.BytesIO();canvas.save(buffer,format='PNG')
    return {OUT/'bounds.json':(json.dumps(report,indent=2)+'\n').encode(),OUT/'font-roles.png':buffer.getvalue()}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,data in outputs().items():
        if a.check:
            old=path.read_bytes()if path.exists()else b''
            if path.suffix=='.json':old=old.replace(b'\r\n',b'\n')
            if old!=data:raise SystemExit('Stale font measurement: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Research font measurements:301 inherited assignments;0 source bounds failures; native untested')
