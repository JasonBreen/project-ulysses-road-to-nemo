"""Offline UI projection for review, never a screenshot/native acceptance claim.

No arguments: write the geometry projection and the continuous-focus layout
review. --layouts writes only the layout review; --check compares it (JSON and
HTML byte for byte, PNGs by size and RGBA).
"""
from pathlib import Path
import argparse
import html
import io
import json
import re
import sys
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'
OUT=ROOT/'docs/evidence/package0-focus'
NAVY=(8,22,33,255);WHITE=(218,237,242,255);CYAN=(93,208,223,255);EDGE=(45,85,104,255)
FONT=ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'
RED=(214,72,64,255);DIM=(20,44,58,255);BAND=(12,32,45,255)
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'tools'))
import focus_layout  # noqa: E402
from event_picture_fit.fit import same_review_png  # noqa: E402

# Declared panels before the 5 November 2026 repair; generic_focus declared none.
BEFORE={'ac_ucw_eru_tree':(1200,1700),'ac_ucw_fcu_tree':(1300,1700),
        'ac_anea_emm_tree':(50,2100),'ac_anea_eva_tree':(50,2100),'generic_focus':None}
SCALE=4


def atlas_font():
    text=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text()
    metrics={int(values['id']):{k:int(v) for k,v in values.items()}
             for line in text.splitlines() if line.startswith('char id=')
             for values in [dict(re.findall(r'(\w+)=(-?\d+)',line))]}
    return metrics,Image.open(MOD/'gfx/fonts/ACBriefing16.dds').convert('RGBA')


def write_text(canvas,font,x,y,text,colour=WHITE):
    metrics,atlas=font
    for char in text:
        m=metrics.get(ord(char),metrics[ord('?')])
        glyph=atlas.crop((m['x'],m['y'],m['x']+m['width'],m['y']+m['height']))
        if colour!=WHITE:
            tint=Image.new('RGBA',glyph.size,colour);tint.putalpha(glyph.getchannel('A'));glyph=tint
        canvas.alpha_composite(glyph,(x+m['xoffset'],y+m['yoffset']))
        x+=m['xadvance']


def layout_records():
    geometry=focus_layout.gui_geometry();trees=focus_layout.resolved_tree_positions()
    records=[]
    for tree,info in sorted(focus_layout.tree_definitions().items()):
        positions=trees[tree];panel=info['panel']
        before=BEFORE.get(tree,panel)
        records.append({'tree':tree,'file':info['file'],'nodes':len(positions),'panel':list(panel) if panel else None,
                        'rule':list(focus_layout.panel_position(positions,geometry)),
                        'overlaps':focus_layout.overlaps(positions,panel,geometry) if panel else None,
                        'clearance_px':focus_layout.clearance(positions,panel,geometry) if panel else None,
                        'repaired':tree in BEFORE,'before':list(before) if before else None,
                        'before_overlaps':focus_layout.overlaps(positions,before,geometry) if before else None})
    return geometry,trees,records


def layout_png(record,positions,geometry,font):
    rects={ident:focus_layout.node_rect(x,y,geometry) for ident,(x,y) in positions.items()}
    panels=[tuple(record['panel'])]+([tuple(record['before'])] if record['before'] else [])
    boxes=list(rects.values())+[focus_layout.panel_rect(p,geometry) for p in panels]
    left=min(b[0] for b in boxes)-48;top=min(b[1] for b in boxes)-288
    right=max(b[2] for b in boxes)+48;bottom=max(b[3] for b in boxes)+48
    def q(x,y):return int((x-left)//SCALE),int((y-top)//SCALE)
    image=Image.new('RGBA',(int((right-left)//SCALE)+1,int((bottom-top)//SCALE)+1),NAVY)
    draw=ImageDraw.Draw(image)
    band_top=record['panel'][1];band_bottom=band_top+geometry['panel'][1]
    draw.rectangle((*q(left,band_top),*q(right,band_bottom)),fill=BAND)
    bad=set(record['before_overlaps'] or ())
    for ident,rect in sorted(rects.items()):
        draw.rectangle((*q(rect[0],rect[1]),*q(rect[2],rect[3])),fill=RED if ident in bad else DIM,outline=EDGE)
    if record['before']:
        draw.rectangle((*q(*focus_layout.panel_rect(record['before'],geometry)[:2]),*q(*focus_layout.panel_rect(record['before'],geometry)[2:])),outline=RED,width=2)
    after=focus_layout.panel_rect(record['panel'],geometry)
    draw.rectangle((*q(after[0],after[1]),*q(after[2],after[3])),outline=CYAN,width=3)
    write_text(image,font,8,6,record['tree']+'  ('+record['file']+')')
    before='none declared' if not record['before'] else '%d, %d: %d overlapping nodes (red)'%(record['before'][0],record['before'][1],len(bad))
    write_text(image,font,8,24,'Before: '+before,RED)
    write_text(image,font,8,42,'After: %d, %d: %d overlaps, %s px clear (cyan)'%(record['panel'][0],record['panel'][1],len(record['overlaps']),
               int(record['clearance_px']) if record['clearance_px'] is not None else '-'),CYAN)
    return image


def layout_html(records):
    rows=[]
    for r in records:
        rows.append('<tr%s><td><code>%s</code></td><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%d</td><td>%s</td></tr>'%(
            ' class="repaired"' if r['repaired'] else '',html.escape(r['tree']),html.escape(r['file']),r['nodes'],
            'none' if not r['before'] else '%d, %d (%d overlaps)'%(r['before'][0],r['before'][1],len(r['before_overlaps'])),
            '%d, %d'%tuple(r['panel']),len(r['overlaps']),'-' if r['clearance_px'] is None else int(r['clearance_px'])))
    images=''.join('<figure><img src="layout-%s.png" alt="%s layout"><figcaption>%s</figcaption></figure>\n'%(r['tree'],r['tree'],r['tree'])
                   for r in records if r['repaired'])
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Continuous-focus layout</title>\n'
            '<style>body{background:#081621;color:#daedf2;font-family:sans-serif;margin:16px}td,th{border:1px solid #2d5568;padding:4px 8px}'
            'table{border-collapse:collapse}.repaired{color:#5dd0df}img{max-width:100%;border:1px solid #2d5568}</style></head><body>\n'
            '<h1>Continuous-focus panel layout (offline geometry)</h1>\n'
            '<p>Resolved node footprints against the declared continuous_focus_position. Not native rendering evidence.</p>\n'
            '<table><tr><th>Tree</th><th>File</th><th>Nodes</th><th>Before</th><th>Panel</th><th>Overlaps</th><th>Clearance px</th></tr>\n'
            +'\n'.join(rows)+'\n</table>\n'+images+'</body></html>\n')


def layouts(check=False):
    geometry,trees,records=layout_records();font=atlas_font()
    outputs={'layout.json':(json.dumps({'geometry':{k:list(v) for k,v in geometry.items()},'trees':records},indent=2)+'\n').encode(),
             'index.html':layout_html(records).encode()}
    for r in records:
        if r['repaired']:
            buffer=io.BytesIO();layout_png(r,trees[r['tree']],geometry,font).save(buffer,'PNG',optimize=True)
            outputs['layout-'+r['tree']+'.png']=buffer.getvalue()
    stale=[]
    for name,data in outputs.items():
        target=OUT/name
        if check:
            old=target.read_bytes() if target.exists() else b''
            if not (same_review_png(old,data) if name.endswith('.png') else old.replace(b'\r\n',b'\n')==data):stale.append(name)
        else:
            OUT.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    if check and stale:raise SystemExit('Stale layout review: '+', '.join(stale))
    print('Layout review: %d trees, %d images %s'%(len(records),len(outputs)-2,'consistent' if check else 'written'))


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
           'ERU/FCU opening panel: 770×456 at (2016,16); every tree: see layout.json and index.html.',
           'Lower-resolution access relies on the retained outer pan/scroll controls; native check pending.']
    for i,line in enumerate(lines):draw.text((35,490+i*34),line,font=small,fill=WHITE)
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'focus-geometry-and-seams.png';image.save(target)
    print(target.relative_to(ROOT).as_posix())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--layouts',action='store_true')
    arguments=parser.parse_args()
    if not (arguments.check or arguments.layouts):main()
    layouts(arguments.check)
