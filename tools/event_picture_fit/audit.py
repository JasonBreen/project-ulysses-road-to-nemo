"""Resolve actual requested event consumers to sprites, DDS frames and GUI bounds.

Scope is explicit. This is not native rendering or an all-event closure claim.
Additional event files can be supplied by later campaign owners.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from usea_expansion.script import parse,get
from event_picture_fit.fit import MOD,SIZES,assert_fits

DEFAULT_EVENTS = ['events/'+name+'.txt' for name in (
    'ac_reconstruction','ac_superpower_programmes','ac_fato_south_belka',
    'ac_anea','ac_anea_narrative','ac_ucw','ac_squadrons')]
PICTURE_CONTROLS={
    ('EventWindow','bottom_Window','event_picture'):('country_event',(5,5),'options_grid',215),
    ('EventWindow_News','top_Window','event_picture'):('news_event',(59,91),'Title',260),
}

def scalar(value):
    if not isinstance(value,str):raise ValueError('Dynamic event-picture syntax requires a separately reviewed consumer contract')
    return value.strip('"')

def controls(mod=MOD):
    found=[];named={}
    def walk(nodes,parents=()):
        for kind,_,body in nodes:
            if not isinstance(body,list):continue
            name=get(body,'name');path=parents+((scalar(name),) if name else ())
            if name:
                if path in named:raise ValueError('Duplicate required GUI control path: '+str(path))
                named[path]=body
            if name and scalar(name)=='event_picture':found.append((path,body))
            walk(body,path)
    walk(parse((mod/'interface/eventwindow.gui').read_text(encoding='utf-8-sig')))
    result={}
    for path,body in found:
        contract=PICTURE_CONTROLS.get(path)
        if contract is None:raise ValueError('Unreviewed required event_picture control path: '+str(path))
        kind,expected_position,sibling,expected_edge=contract
        position=get(body,'position');x=float(get(position,'x'));y=float(get(position,'y'))
        if (x,y)!=expected_position:raise ValueError('Reviewed event_picture position changed: '+str(path))
        def upper_left(node):
            values=[scalar(value)for key,_,value in node if key.casefold()=='orientation']
            if len(values)>1 or (values and values!=['UPPER_LEFT']):
                raise ValueError('Unsupported event control Orientation: '+str(path))
        upper_left(body)
        if kind in result:raise ValueError('Ambiguous event_picture binding: '+kind)
        if get(body,'size') is not None:raise ValueError('Unexpected event-picture size override')
        scale=float(get(body,'scale','1'))
        if scale!=1:raise ValueError('Event-picture native scale contract changed')
        result[kind]=dict(path=list(path),position=[x,y],scale=scale,default_sprite=scalar(get(body,'spriteType')))
        obstacle=named.get(path[:-1]+(sibling,))
        if obstacle is None:raise ValueError('Missing required event sibling control: '+sibling)
        upper_left(obstacle)
        obstacle_position=get(obstacle,'position')
        edge=float(get(obstacle_position,'x' if kind=='country_event' else 'y'))
        if edge!=expected_edge:raise ValueError('Reviewed event sibling bounds changed')
        result[kind]['right_obstacle' if kind=='country_event' else 'lower_obstacle']=edge
    if set(result)!=set(SIZES):raise ValueError('Missing required country/news event_picture control')
    return result

def sprites(mod=MOD):
    result={};duplicates=set()
    for file in sorted((mod/'interface').glob('*.gfx')):
        for _,_,body in get(parse(file.read_text(encoding='utf-8-sig')),'spriteTypes',[]):
            if not isinstance(body,list) or get(body,'texturefile') is None:continue
            name=scalar(get(body,'name'))
            if name in result:duplicates.add(name)
            result[name]=dict(texture=scalar(get(body,'texturefile')),frames=int(get(body,'noOfFrames','1')),
                definition=file.relative_to(mod).as_posix())
    return result,duplicates

def audit(event_paths=DEFAULT_EVENTS,mod=MOD):
    geometry=controls(mod);bindings,duplicates=sprites(mod);rows=[];implicit=[]
    for relative in event_paths:
        for kind,_,body in parse((mod/relative).read_text(encoding='utf-8-sig')):
            if kind not in SIZES:continue
            ident=scalar(get(body,'id'));picture=get(body,'picture')
            if picture is None:
                implicit.append(dict(file=relative,id=ident,hidden=get(body,'hidden')=='yes' or get(body,'hide_window')=='yes'))
                continue
            picture=scalar(picture)
            if picture in duplicates:raise ValueError('Conflicting requested sprite definitions: '+picture)
            if picture not in bindings:raise ValueError('Unresolved requested event picture: '+picture)
            binding=bindings[picture];path=mod/binding['texture']
            if not path.is_file():raise ValueError('Missing requested texture: '+str(path))
            with Image.open(path) as image:
                if image.format!='DDS':raise ValueError('Requested event picture is not DDS: '+str(path))
                size=image.size
            frame=assert_fits(kind,size,geometry[kind]['scale'],binding['frames'])
            x,y=geometry[kind]['position']
            rows.append(dict(file=relative,id=ident,event_type=kind,picture=picture,**binding,width=size[0],height=size[1],
                scale=geometry[kind]['scale'],frame_size=list(frame),bounds=[x,y,x+frame[0],y+frame[1]],
                aperture=list(SIZES[kind])))
    return dict(schema=1,coverage='Actual explicit picture consumers in the listed files only; offline source geometry, no native claim',
        event_files=list(event_paths),controls=geometry,explicit_consumers=len(rows),
        counts=dict(Counter(r['event_type'] for r in rows)),implicit_picture_events=implicit,consumers=rows)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--events',action='append');p.add_argument('--output',type=Path);a=p.parse_args()
    report=audit(a.events or DEFAULT_EVENTS)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print('Event picture consumers:',report['explicit_consumers'],'fit actual unscaled controls;',len(report['implicit_picture_events']),'implicit-picture events separately recorded; no native claim.')

if __name__=='__main__':main()
