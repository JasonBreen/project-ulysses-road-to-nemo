"""Offline UI projection for review, never a screenshot/native acceptance claim."""
from pathlib import Path
import json
import re
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'
OUT=ROOT/'docs/evidence/package0-focus'
NAVY=(8,22,33,255);WHITE=(218,237,242,255);CYAN=(93,208,223,255);EDGE=(45,85,104,255)
FONT=ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'


def main():
    text=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text()
    metrics={int(values['id']):{k:int(v) for k,v in values.items()}
             for line in text.splitlines() if line.startswith('char id=')
             for values in [dict(re.findall(r'(\w+)=(-?\d+)',line))]}
    atlas=Image.open(MOD/'gfx/fonts/ACBriefing16.dds').convert('RGBA')
    def width(s):return sum(metrics[ord(c)]['xadvance'] for c in s)
    def wrap(s):
        lines=['']
        for word in s.split():
            if lines[-1] and width(lines[-1]+' '+word)>147:lines.append(word)
            else:lines[-1]=(lines[-1]+' '+word).strip()
        return lines
    def caption(canvas,title,x,y,height):
        lines=wrap(title)
        top=y+max(0,(height-len(lines)*18)//2)
        for line in lines:
            cursor=x+(147-width(line))//2
            for char in line:
                m=metrics[ord(char)]
                glyph=atlas.crop((m['x'],m['y'],m['x']+m['width'],m['y']+m['height']))
                canvas.alpha_composite(glyph,(cursor+m['xoffset'],top+m['yoffset']))
                cursor+=m['xadvance']
            top+=18
    image=Image.new('RGBA',(1120,760),NAVY)
    draw=ImageDraw.Draw(image)
    label=ImageFont.truetype(str(FONT),18);small=ImageFont.truetype(str(FONT),14)
    draw.text((28,22),'FOCUS SCREEN REPAIR — OFFLINE GEOMETRY PROJECTION',font=label,fill=CYAN)
    draw.text((28,52),'Shipped font glyphs and textures; this is not native rendering evidence.',font=small,fill=WHITE)
    cases=[('Before: 40px caption; exclusion crosses text',90,170,40,50,68),
           ('After: 54px caption; separate exclusion channel',620,170,54,64,16)]
    records=json.loads((HERE/'focus_art.json').read_text())
    for heading,origin_x,origin_y,text_height,frame_height,exclusive_centre in cases:
        draw.text((origin_x-55,100),heading,font=small,fill=WHITE)
        for offset,ident,title in [(0,'FCU_exp_liaison_offices','Guarantee the Equal-Member Compact'),
                                   (192,'FCU_exp_treaty_audit','Empower the Common Fund')]:
            record=next(row for row in records if row['id']==ident)
            with Image.open(MOD/record['asset']) as icon:
                image.alpha_composite(icon.convert('RGBA'),(origin_x+offset+40,origin_y-56))
            x=origin_x+offset+5;y=origin_y+40
            draw.rectangle((x,y,x+163,y+frame_height-1),fill=NAVY,outline=EDGE,width=1)
            caption(image,title,origin_x+offset+15,origin_y+44,text_height)
        centre_x=origin_x+184;centre_y=origin_y+exclusive_centre
        draw.line((origin_x+169,centre_y,origin_x+199,centre_y),fill=CYAN,width=2)
        draw.polygon([(centre_x,centre_y-12),(centre_x+12,centre_y),(centre_x,centre_y+12),(centre_x-12,centre_y)],fill=NAVY,outline=CYAN)
        draw.line((centre_x-4,centre_y-4,centre_x+4,centre_y+4),fill=CYAN,width=1)
        draw.line((centre_x-4,centre_y+4,centre_x+4,centre_y-4),fill=CYAN,width=1)
    draw.text((35,350),'Before: direction-sensitive 2px segment joins',font=small,fill=WHITE)
    draw.text((565,350),'After: aligned 2px rectangular strips',font=small,fill=WHITE)
    before=Image.new('RGBA',(16,16))
    b=ImageDraw.Draw(before);b.line((8,8,0,8),fill=CYAN,width=2);b.line((8,8,16,8),fill=CYAN,width=2)
    with Image.open(MOD/'gfx/interface/ac_expansion/ui/GFX_focus_link_left_right.dds') as strip:
        after=strip.crop((0,0,16,16)).convert('RGBA')
    for x,tile in ((35,before),(565,after)):
        row=Image.new('RGBA',(128,16))
        for i in range(8):row.alpha_composite(tile,(i*16,0))
        image.alpha_composite(row.resize((448,56),Image.Resampling.NEAREST),(x,390))
    lines=['Normal node: 96px icon ends at local y40; 64px caption frame spans y40–104.',
           'Caption: three 18px lines fit y44–98. Row pitch 160px; exclusion marker ends before y44.',
           'Continuous entries: positive icon offsets; 172px row pitch; 352px scrollable body.',
           'ERU/FCU opening panel: 770×456 at (2016,16), to the right of the tree.',
           'Lower-resolution access relies on the retained outer pan/scroll controls; native check pending.']
    for i,line in enumerate(lines):draw.text((35,490+i*34),line,font=small,fill=WHITE)
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'focus-geometry-and-seams.png';image.save(target)
    print(target.relative_to(ROOT).as_posix())


if __name__=='__main__':main()
