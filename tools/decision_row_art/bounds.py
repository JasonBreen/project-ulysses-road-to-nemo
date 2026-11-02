"""Measure actual decision consumers against shipped engine row controls."""
from pathlib import Path
import io
import sys
import tempfile

from PIL import Image

ROOT=Path(__file__).resolve().parents[2];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/overhaul'))
from audit_consumers import Audit
from build_decisions_ui import parse,get,scalar,walk

TEMPLATES=('decision_item','targeted_decision_item','timed_decision_item')
ROW_FAMILIES={'decision','decision_default','conditional_decision_icon','conditional_decision_default'}


def named(tree,name):return next(body for _,body in walk(tree) if scalar(get(body,'name'))==name)


def geometry(gui,template,width,height,frames=1):
    node=named(gui,template);icon=named([['template','=',node]],'icon');title=named([['template','=',node]],'name_text')
    if frames<1 or width%frames:raise ValueError('Invalid actual sprite frame width')
    scale=float(get(icon,'scale','1'));w=width/frames*scale;h=height*scale
    x=float(get(get(icon,'position'),'x'));y=float(get(get(icon,'position'),'y'))
    if get(icon,'centerposition')=='yes':x-=w/2;y-=h/2
    title_x=float(get(get(title,'position'),'x'));bottom=float(get(get(node,'size'),'height'))
    failures=[]
    if x<0 or y<0:failures.append('icon crosses row top/left')
    if x+w>title_x:failures.append('icon enters title column')
    if y+h>bottom:failures.append('icon crosses row bottom')
    return dict(template=template,icon_scale=scale,centered=get(icon,'centerposition')=='yes',
        icon_rect=[x,y,w,h],title_x=title_x,row_height=bottom,failures=failures)


def inspect(mod=MOD,engine=None,overrides=None):
    """No manifest exemptions: load every active authored row's real DDS/GFX.

    Overrides are used only to reconstruct the recorded pre-fix bindings in
    offline evidence. Ordinary validation has no override or allow-list path.
    """
    mod=Path(mod).resolve();overrides=overrides or {};rows=[];problems=[]
    with tempfile.TemporaryDirectory() as empty:
        audit=Audit(mod,Path(engine) if engine else Path(empty))
        gui=parse((mod/'interface/countrydecisionview.gui').read_text(encoding='utf-8-sig'))
        for consumer in audit.decision_consumers():
            # Category fallback roots can share the audit's default-family
            # label; their actual source directory proves they are headers.
            if consumer['consumer_family'] not in ROW_FAMILIES or '/categories/' in consumer['consumer']:continue
            name=consumer['name'];definition,conflicts=audit.definition('sprite',name)
            if not definition or conflicts:
                problems.append(dict(id=consumer['owner'],sprite=name,problem='missing/conflicting actual sprite definition'));continue
            if definition['kind'].lower() not in ('spritetype','textspritetype'):
                problems.append(dict(id=consumer['owner'],sprite=name,problem='unverified row sprite kind: '+definition['kind']));continue
            body=definition['node'];texture=scalar(get(body,'texturefile',''));frames=int(get(body,'noOfFrames','1'))
            if name in overrides:texture=overrides[name]['texture'];frames=overrides[name]['frames']
            resource=audit.vfs.resource(texture,definition['source'])
            if resource['status']!='mod_asset':
                problems.append(dict(id=consumer['owner'],sprite=name,problem='actual row texture is not mod-resolved'));continue
            asset=audit.vfs._files[resource['path']][1]
            try:
                with Image.open(io.BytesIO(asset.read_bytes())) as im:width,height=im.size
                layouts=[geometry(gui,template,width,height,frames) for template in TEMPLATES]
            except (OSError,ValueError) as error:
                problems.append(dict(id=consumer['owner'],sprite=name,problem=str(error)));continue
            row=dict(id=consumer['owner'],source=consumer['consumer'],family=consumer['consumer_family'],sprite=name,
                texture=asset.path.relative_to(mod).as_posix(),binding=definition['source'],sprite_kind=definition['kind'],width=width,height=height,
                frames=frames,frame_width=width/frames,templates=layouts)
            rows.append(row)
            for layout in layouts:
                for failure in layout['failures']:problems.append(dict(id=row['id'],sprite=name,template=layout['template'],problem=failure))
    problems.extend(dict(source=entry['source'],problem='Decision source parse failure: '+entry['error'])
                    for entry in audit.parse_failures
                    if entry['origin']=='mod' and entry['source'].startswith('common/decisions/'))
    return dict(coverage='Actual authored decision row consumers, all conditional alternatives/defaults, actual DDS frame sizes and shipped GUI scale/bounds. Offline only.',
        consumers=rows,problems=problems)
