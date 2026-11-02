"""Offline before/after rows using actual GUI, DDS frames and font atlases."""
import argparse
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

from PIL import Image,ImageDraw
from bounds import ROOT,MOD,TEMPLATES,inspect,named,geometry,parse,get,scalar,Audit

sys.path.insert(0,str(ROOT/'tools/economy_v2'))
spec=importlib.util.spec_from_file_location('decision_bitmap_font',ROOT/'tools/economy_v2/render_review.py')
font_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(font_module)
HERE=Path(__file__).resolve().parent;OUT=ROOT/'docs/evidence/decision-rows'
NAVY=(8,22,33,255);WHITE=(218,237,242,255);CYAN=(93,208,223,255);RED=(218,111,111,255)


def encode(im):
    stream=io.BytesIO();im.save(stream,format='PNG');return stream.getvalue()


def build():
    source=json.loads((HERE/'source/before_bindings.json').read_text());before=source['bindings']
    current=inspect();old=inspect(overrides=before)
    if current['problems']:raise ValueError('Current actual row bounds fail: '+str(current['problems'][:3]))
    gui=parse((MOD/'interface/countrydecisionview.gui').read_text(encoding='utf-8-sig'))
    strings={}
    for path in sorted((MOD/'localisation/english').rglob('*.yml')):
        strings.update(re.findall(r'^\s*([^\s:#]+):\d*\s+"((?:\\.|[^"\\])*)"',path.read_text(encoding='utf-8-sig'),re.M))
    font=font_module.AtlasFont('ACBriefing16')
    # Delivered row background: first of its actual three512x104frames.
    import tempfile
    with tempfile.TemporaryDirectory() as empty:
        audit=Audit(MOD,Path(empty));definition,_=audit.definition('sprite','GFX_ac_dec_decision_item_bg')
        resource=audit.vfs.resource(scalar(get(definition['node'],'texturefile')),definition['source']);asset=audit.vfs._files[resource['path']][1]
        with Image.open(io.BytesIO(asset.read_bytes())) as strip:
            frames=int(get(definition['node'],'noOfFrames','1'));frame_width=strip.width//frames
            background=strip.convert('RGBA').crop((0,0,frame_width,strip.height))
    outputs={};panel=600;stride=170;text_findings=[];before_text_findings=[]
    for template in TEMPLATES:
        canvas=Image.new('RGBA',(panel*2,90+stride*len(before)),NAVY);draw=ImageDraw.Draw(canvas)
        font.draw(canvas,'OFFLINE SOURCE RECONSTRUCTION / BEFORE AND AFTER / not a native screenshot',12,8,1170,24)
        font.draw(canvas,template+' / actual first background frame / illustrative localized titles',12,34,1170,24)
        for index,sprite in enumerate(before):
            row=next(r for r in current['consumers'] if r['sprite']==sprite);y=90+index*stride
            label=sprite.removeprefix('GFX_decision_')
            title=re.sub(r'\[[^\]]+\]','Illustrative State',strings.get(row['id'],row['id'])).replace('\\n',' ')
            for column,(texture,frames,heading) in enumerate([(before[sprite]['texture'],before[sprite]['frames'],'BEFORE'),(row['texture'],row['frames'],'AFTER')]):
                left=column*panel;origin=(left+40,y+42)
                font.draw(canvas,heading+' / '+label,left+12,y,570,30)
                canvas.alpha_composite(background,origin)
                with Image.open(MOD/texture) as strip:
                    icon=strip.convert('RGBA').crop((0,0,strip.width//frames,strip.height))
                layout=geometry(gui,template,icon.width,icon.height)
                x,top,width,height=layout['icon_rect']
                if layout['icon_scale']!=1:icon=icon.resize((round(width),round(height)),Image.Resampling.LANCZOS)
                canvas.alpha_composite(icon,(origin[0]+round(x),origin[1]+round(top)))
                node=named(gui,template);title_node=named([['template','=',node]],'name_text');point=get(title_node,'position')
                shown=row['id'] if column==0 and row['id'] in source['missing_english_decision_keys'] else title
                text_layout=font.draw(canvas,shown,origin[0]+int(get(point,'x')),origin[1]+int(get(point,'y')),int(get(title_node,'maxWidth')),int(get(title_node,'maxHeight')))
                if text_layout['clipped'] or text_layout['horizontal_overflow']:
                    (text_findings if column else before_text_findings).append(dict(template=template,sprite=sprite,title=shown,layout=text_layout))
                color=RED if layout['failures'] else CYAN
                draw.rectangle((origin[0]+round(x),origin[1]+round(top),origin[0]+round(x+width),origin[1]+round(top+height)),outline=color,width=1)
                draw.line((origin[0]+layout['title_x'],origin[1],origin[0]+layout['title_x'],origin[1]+104),fill=CYAN)
                font.draw(canvas,f'{icon.width}x{icon.height} frame / '+('crosses source bounds' if layout['failures'] else 'inside source bounds'),left+40,y+148,540,20)
        outputs[OUT/(template+'.png')]=encode(canvas)
    affected={(r['id'],r['sprite']) for r in old['problems']}
    report=dict(base_commit=source['base_commit'],evidence='Offline reconstruction; source rectangles and first background frames, not native rendering or input evidence',
        actual_row_variants=len(current['consumers']),before_affected_active_variants=len(affected),before_problems=old['problems'],after_problems=current['problems'],
        inherited_art_preserved='263original Anea/institutions textures plus13 former row-texture bindings are byte-pinned in source contracts',
        templates={name:geometry(gui,name,26,29) for name in TEMPLATES},text_findings=text_findings,before_text_findings=before_text_findings,
        restored_english_decision_keys=source['missing_english_decision_keys'],missing_font_glyphs=sorted(font.missing),
        actual_consumers=[{k:r[k] for k in ('id','source','family','sprite','texture','binding','width','height','frames','frame_width')} for r in current['consumers']],
        limits=['All conditional alternatives and conservative defaults are inspected; this does not establish gameplay reachability.',
                'Source categories/ headers are not treated as rows even when an audit fallback-family label is shared.',
                'Native half-pixel alignment, visibility, selection, flag substitution, display scaling and input remain untested.'])
    outputs[OUT/'consumer-bounds.json']=(json.dumps(report,indent=2)+'\n').encode()
    page='<html><meta charset="utf-8"><title>Offline decision row repair review</title><style>body{background:#081621;color:#daedf2;font:16px sans-serif}img{max-width:100%}</style><h1>Decision rows: offline source reconstruction</h1><p>Actual shipped controls, font atlas, first background frame, localized sample titles and original DDS. Red/cyan bounding guides are review annotations, never delivered artwork. This is not a native screenshot.</p><p>'+str(len(current['consumers']))+'active row variants inspected; '+str(len(affected))+'previously oversized active variants; zero current source-bound failures.</p>'
    for name in TEMPLATES:page+='<h2>'+html.escape(name)+'</h2><img src="'+name+'.png" alt="Before and after '+name+'">'
    outputs[OUT/'index.html']=(page+'</html>\n').encode()
    if text_findings or font.missing:raise ValueError('Actual font/text reconstruction findings: '+str(text_findings or font.missing))
    return outputs,report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();outputs,report=build()
    for path,data in outputs.items():
        if args.check:
            old=path.read_bytes() if path.exists() else b''
            if path.suffix in ('.html','.json'):old=old.replace(b'\r\n',b'\n')
            if old!=data:raise SystemExit('Stale decision-row review artifact: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Offline decision rows:',report['actual_row_variants'],'variants;',report['before_affected_active_variants'],'before;0after bounds failures')
