"""Offline reconstruction of the new scroll content, using shipped controls/art.

Not a native screenshot. Dates/states are illustrative; geometry, fonts,
localized labels and texture dimensions come from the actual candidate.
"""
import argparse
import io
import json
from pathlib import Path
import re
import sys

from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get,walk


def unquote(v):return v.strip('"') if isinstance(v,str) else v
def load(path):return parse(path.read_text(encoding='utf-8-sig'))
def named(tree,name):return next(body for _,body in walk(tree) if isinstance(body,list) and unquote(get(body,'name'))==name)
def pos(body):return {k:int(v) for k,_,v in get(body,'position',[])}
def locs():
    source=(MOD/'localisation/english/ac_land_program_l_english.yml').read_text(encoding='utf-8-sig')
    return {key:value.replace('\\n','\n') for key,value in re.findall(r'^\s*(\w+):\d*\s+"(.*)"$',source,re.M)}


def same_review_png(first,second):
    """Require exact review pixels while allowing platform PNG compression."""
    with Image.open(io.BytesIO(first)) as old,Image.open(io.BytesIO(second)) as new:
        return old.size==new.size and old.convert('RGBA').tobytes()==new.convert('RGBA').tobytes()


class Atlas:
    def __init__(self,name):
        source=(MOD/'gfx/fonts'/(name+'.fnt')).read_text();self.rows={};self.kern={}
        self.height=int(re.search(r'common lineHeight=(\d+)',source)[1])
        self.atlas=Image.open(MOD/'gfx/fonts'/re.search(r'page id=0 file="([^"]+)"',source)[1]).convert('RGBA')
        for line in source.splitlines():
            fields={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
            if line.startswith('char '):self.rows[fields['id']]=fields
            elif line.startswith('kerning '):self.kern[(fields['first'],fields['second'])]=fields['amount']
    def measure(self,text):
        width=0;previous=None
        for char in text:
            ident=ord(char)
            if ident not in self.rows:raise ValueError('Missing shipped font glyph: '+char)
            width+=self.kern.get((previous,ident),0)+self.rows[ident]['xadvance'];previous=ident
        return width
    def wrap(self,text,width):
        rows=[]
        for paragraph in text.split('\n'):
            line=''
            for word in paragraph.split():
                candidate=line+' '+word if line else word
                if line and self.measure(candidate)>width:rows.append(line);line=word
                else:line=candidate
                if self.measure(line)>width:raise ValueError('Unbreakable label exceeds real text bounds: '+line)
            rows.append(line)
        return rows
    def draw(self,image,text,x,y,width,height):
        rows=self.wrap(text,width)
        if len(rows)*self.height>height:raise ValueError('Actual font wraps beyond control height: '+text)
        for line in rows:
            cursor=x;previous=None
            for char in line:
                ident=ord(char);row=self.rows[ident];cursor+=self.kern.get((previous,ident),0)
                glyph=self.atlas.crop((row['x'],row['y'],row['x']+row['width'],row['y']+row['height']))
                ink=Image.new('RGBA',glyph.size,(218,237,242,255));ink.putalpha(glyph.getchannel('A'))
                image.alpha_composite(ink,(cursor+row['xoffset'],y+row['yoffset']))
                cursor+=row['xadvance'];previous=ident
            y+=self.height


def render():
    gui=load(MOD/'interface/countrytechtreeview.gui');templates=load(MOD/'interface/ac_land_techtree.gui')
    folder=named(gui,'ac_land_folder');content=named(folder,'ac_land_scroll_content');card=named(templates,'techtree_ac_land_folder_item')
    dimensions={k:int(v) for k,_,v in get(content,'size') if k in ('width','height')}
    canvas=Image.new('RGBA',(dimensions['width'],dimensions['height']),(8,22,33,255))
    fonts={name:Atlas(name) for name in ('ACBriefing16','ACBriefing20')};strings=locs()
    sheet=Image.open(MOD/'gfx/AC_land/ui/sheet.dds').convert('RGBA')
    for y in range(0,canvas.height,sheet.height):
        for x in range(0,canvas.width,sheet.width):canvas.alpha_composite(sheet,(x,y))
    findings=[]
    def draw_text(body,origin=(0,0),value=None):
        point=pos(body);key=unquote(get(body,'text',''));value=value if value is not None else strings.get(key,key)
        font=fonts[unquote(get(body,'font'))]
        try:font.draw(canvas,value,point['x']+origin[0],point['y']+origin[1],int(get(body,'maxWidth')),int(get(body,'maxHeight')))
        except ValueError as error:findings.append(str(error))
    for kind,body in walk(content):
        if kind.lower()=='instanttextboxtype':draw_text(body)
    techs=get(load(MOD/'common/technologies/ac_land_program.txt'),'technologies')
    manifest=json.loads((HERE/'assets.json').read_text());sprites={r['name']:r for r in manifest['sprites']}
    rectangles=[]
    for index,(ident,_,body) in enumerate(techs):
        family,year=ident.removeprefix('ac_land_').rsplit('_',1)
        grid=named(folder,'ac_land_'+family+'_2006_tree');gp=pos(grid);fp=get(get(body,'folder'),'position')
        x=gp['x']+int(get(fp,'x'))*int(get(get(grid,'slotsize'),'width'));y=gp['y']+int(get(fp,'y'))*int(get(get(grid,'slotsize'),'height'))
        rectangles.append(dict(id=ident,x=x,y=y,width=183,height=84))
        state=('available','researched','unavailable')[index%3]
        bg=Image.open(MOD/f'gfx/interface/ac_expansion/ui/GFX_technology_{state}_item_bg.dds').convert('RGBA');canvas.alpha_composite(bg,(x,y))
        draw_text(named(card,'Name'),(x,y),strings[ident])
        icon=Image.open(MOD/sprites['GFX_'+ident+'_medium']['asset']).convert('RGBA');point=pos(named(card,'Icon'))
        canvas.alpha_composite(icon,(x+point['x']-icon.width//2,y+point['y']-icon.height//2))
        if x<0 or y<0 or x+183>canvas.width or y+84>canvas.height:findings.append('Node outside scroll content: '+ident)
    banner=Image.new('RGBA',(canvas.width,canvas.height+42),(8,22,33,255));banner.alpha_composite(canvas,(0,42))
    fonts['ACBriefing16'].draw(banner,'OFFLINE SOURCE RECONSTRUCTION / illustrative states / not a native screenshot',12,8,1220,24)
    report=dict(evidence='Offline reconstruction of actual shipped new content, fonts and sprite bindings; not native GUI acceptance',
        node_rectangles=rectangles,findings=findings,display_cases=[])
    parent=named(gui,'countrytechtreeview');tabs=named(gui,'folder_tabs');tab=named(tabs,'ac_land_folder_tab')
    for width,height,scale in [(3440,1440,1),(1920,1080,1),(2560,1440,1.25)]:
        logical=[width/scale,height/scale];page_top=pos(parent)['y']+pos(folder)['y']+13
        available=logical[1]-page_top-24;scroll=max(0,canvas.height-available)
        frame=dict(display=[width,height],scale=scale,logical=logical,content=list(canvas.size),vertical_scroll_range=scroll,
                   last_node_reachable=max(r['y']+r['height'] for r in rectangles)-scroll<=available,
                   tab_inside=pos(parent)['x']+pos(tab)['x']+89<=logical[0])
        report['display_cases'].append(frame)
        if not frame['last_node_reachable'] or not frame['tab_inside']:findings.append('Viewport geometry failed: '+str(frame))
    return banner,report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    image,report=render();stream=io.BytesIO();image.save(stream,format='PNG')
    files={ROOT/'docs/evidence/land-program/research-page.png':stream.getvalue(),ROOT/'docs/evidence/land-program/research-page.json':(json.dumps(report,indent=2)+'\n').encode()}
    for path,data in files.items():
        if args.check:
            existing=path.read_bytes() if path.exists() else b''
            if path.suffix=='.png' and existing and same_review_png(existing,data):continue
            if path.suffix=='.json':existing=existing.replace(b'\r\n',b'\n')
            if existing!=data:raise SystemExit('Stale land review artifact: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Land source GUI reconstruction:',len(report['node_rectangles']),'nodes;',len(report['findings']),'findings')
    for finding in report['findings']:print(finding)
    if report['findings']:raise SystemExit(1)
