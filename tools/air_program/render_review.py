"""Reconstruct actual AIR research controls/fonts/sprites offline, not natively."""
import argparse
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/land_program')]
spec=importlib.util.spec_from_file_location('air_actual_font_atlas',ROOT/'tools/land_program/render_review.py')
land_review=importlib.util.module_from_spec(spec);spec.loader.exec_module(land_review)
from presentation import load,named,scalar,blueprint_contracts
from air_content import tech_id
from script import get,walk


def point(body):return {k:int(v) for k,_,v in get(body,'position')}
def strings():return {k:v for k,v in re.findall(r'^\s*(\w+):0\s+"([^"]*)"',(MOD/'localisation/english/ac_air_program_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}


def render():
    gui=load(MOD/'interface/countrytechtreeview.gui');folder=named(gui,'ac_air_folder');content=named(folder,'ac_air_scroll_content')
    card=named(load(MOD/'interface/ac_air_techtree.gui'),'techtree_ac_air_folder_item');size=get(content,'size')
    canvas=Image.new('RGBA',(int(get(size,'width')),int(get(size,'height'))),(8,22,33,255));sheet=Image.open(MOD/'gfx/AC_air/ui/sheet.dds').convert('RGBA')
    for y in range(0,canvas.height,sheet.height):
        for x in range(0,canvas.width,sheet.width):canvas.alpha_composite(sheet,(x,y))
    fonts={name:land_review.Atlas(name) for name in ('ACBriefing16','ACBriefing20')};loc=strings();findings=[]
    def text(body,origin=(0,0),value=None):
        pos=point(body);key=scalar(get(body,'text',''));value=value if value is not None else loc.get(key,key)
        try:fonts[scalar(get(body,'font'))].draw(canvas,value,pos['x']+origin[0],pos['y']+origin[1],int(get(body,'maxWidth')),int(get(body,'maxHeight')))
        except ValueError as error:findings.append(str(error))
    for kind,body in walk(content):
        if kind.lower()=='instanttextboxtype':text(body)
    sprites={r['name']:r for r in json.loads((HERE/'assets.json').read_text())['sprites']};rectangles=[]
    techs=get(load(MOD/'common/technologies/ac_air_program.txt'),'technologies')
    for index,(ident,_,body) in enumerate(techs):
        family=ident.removeprefix('ac_air_').rsplit('_',1)[0];grid=named(folder,tech_id(family,2006)+'_tree');gp=point(grid);fp=get(get(body,'folder'),'position');slots=get(grid,'slotsize')
        x=gp['x']+int(get(fp,'x'))*int(get(slots,'width'));y=gp['y']+int(get(fp,'y'))*int(get(slots,'height'));dimensions=get(card,'size');w=int(get(dimensions,'width'));h=int(get(dimensions,'height'))
        rectangles.append(dict(id=ident,x=x,y=y,width=w,height=h))
        state=('available','researched','unavailable')[index%3];background=Image.open(MOD/f'gfx/interface/ac_expansion/ui/GFX_technology_{state}_item_bg.dds').convert('RGBA')
        if background.size!=(w,h):findings.append('Actual state texture exceeds card bounds: '+ident)
        canvas.alpha_composite(background,(x,y));text(named(card,'Name'),(x,y),loc[ident])
        image=Image.open(MOD/sprites['GFX_'+ident+'_medium']['asset']).convert('RGBA');pos=point(named(card,'Icon'))
        canvas.alpha_composite(image,(x+pos['x']-image.width//2,y+pos['y']-image.height//2))
        if x<0 or y<0 or x+w>canvas.width or y+h>canvas.height:findings.append('Node outside declared scroll content: '+ident)
    for index,a in enumerate(rectangles):
        for b in rectangles[index+1:]:
            if a['x']<b['x']+b['width'] and a['x']+a['width']>b['x'] and a['y']<b['y']+b['height'] and a['y']+a['height']>b['y']:findings.append('Research card intersection: '+a['id']+'/'+b['id'])
    report=dict(evidence='OFFLINE reconstruction using actual shipped AIR controls, font atlas, localization and DDS. Illustrative research states; not native game acceptance.',
        native_acceptance=False,node_rectangles=rectangles,blueprints=blueprint_contracts(),display_cases=[],findings=findings)
    parent=named(gui,'countrytechtreeview');tab=named(gui,'ac_air_folder_tab');manifest=json.loads((HERE/'assets.json').read_text());tab_asset=next(r for r in manifest['assets'] if r['file'].endswith('/tab.dds'))
    for width,height,scale in [(3440,1440,1),(1920,1080,1),(2560,1440,1.25)]:
        logical=[width/scale,height/scale];top=point(parent)['y']+point(folder)['y']+13;available=logical[1]-top-24;scroll=max(0,canvas.height-available)
        case=dict(display=[width,height],scale=scale,logical=logical,vertical_scroll_range=scroll,
                  last_node_reachable=max(r['y']+r['height'] for r in rectangles)-scroll<=available,
                  tab_inside=point(parent)['x']+point(tab)['x']+tab_asset['frame_width']<=logical[0])
        report['display_cases'].append(case)
        if not case['last_node_reachable'] or not case['tab_inside']:findings.append('Logical viewport cannot reach new controls: '+str(case))
    result=Image.new('RGBA',(canvas.width,canvas.height+42),(8,22,33,255));result.alpha_composite(canvas,(0,42))
    fonts['ACBriefing16'].draw(result,'OFFLINE SOURCE RECONSTRUCTION / illustrative states / not a native screenshot',12,8,1220,24)
    return result,report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();im,report=render()
    stream=io.BytesIO();im.save(stream,format='PNG');outputs={ROOT/'docs/evidence/air-program/research-page.png':stream.getvalue(),ROOT/'docs/evidence/air-program/research-page.json':(json.dumps(report,indent=2)+'\n').encode()}
    for path,data in outputs.items():
        if args.check:
            old=path.read_bytes() if path.exists() else b''
            if path.suffix=='.png' and old:
                with Image.open(io.BytesIO(old)) as a,Image.open(io.BytesIO(data)) as b:
                    if a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes():continue
            if path.suffix=='.json':old=old.replace(b'\r\n',b'\n')
            if old!=data:raise SystemExit('Stale aviation research review: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('AIR source reconstruction:',len(report['node_rectangles']),'research cards /16blueprints;',len(report['findings']),'findings')
    for finding in report['findings']:print(finding)
    if report['findings']:raise SystemExit(1)
