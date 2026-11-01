"""Offline source-coordinate event review, never a native screenshot.

No dynamic height/anchor reflow is simulated. The four drawings retain literal
authored anchors, dimensions, frame selection, atlas ink and bounded text clips.
"""
import argparse,hashlib,io,json,math,re,sys
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from event_style.migration import report,assert_preserved
from event_picture_fit.fit import same_review_png
from usea_expansion.script import parse,get,walk
from land_program.render_review import Atlas
OUT=ROOT/'docs/evidence/event-style'
FONTS={name:Atlas('ACBriefing'+str(size)) for name,size in [('ACEvent16',16),('ACEvent20',20),('ACBriefing16',16),('ACBriefing20',20)]}
def unquote(value):return value.strip('"') if isinstance(value,str) else value
def load(path):return parse(path.read_text(encoding='utf-8-sig'))
def named(tree):
    result={}
    def visit(rows,path=()):
        name=unquote(get(rows,'name'));path+=((name,) if name else ())
        if name:
            if path in result:raise ValueError('Duplicate named control '+str(path))
            result[path]=rows
        for _,_,value in rows:
            if isinstance(value,list):visit(value,path)
    visit(tree);return result
def locs():
    result={}
    for file in sorted((MOD/'localisation').rglob('*english.yml'),key=lambda p:('replace' in p.parts,p.as_posix())):
        for key,value in re.findall(r'^\s*([^\s:#]+):\d*\s+"((?:\\.|[^"\\\r\n])*)"\s*(?:#[^\r\n]*)?$',file.read_text(encoding='utf-8-sig'),re.M):
            result[key]=value.replace('\\n','\n').replace('\\"','"')
    return result
def visible(text):return re.sub(r'§.', '',text)
def options(value):
    if isinstance(value,str):return [unquote(value)]
    if isinstance(value,list):return [unquote(v) for k,_,v in value if k=='text' and isinstance(v,str)]
    return []
def geometry(body):
    p=get(body,'position',[])
    return dict(x=float(get(p,'x','0')),y=float(get(p,'y','0')),width=int(get(body,'maxWidth','0')),height=int(get(body,'maxHeight','0')),
                font=unquote(get(body,'font','ACBriefing16')),scrollbar=unquote(get(body,'scrollbarType')))
def metrics(text,body):
    g=geometry(body);font=FONTS[g['font']];clean=visible(text);missing=sorted(set(c for c in clean if ord(c) not in font.rows and c!='\n'))
    dynamic=bool(re.search(r'\[[^\]]+\]|\$[^$]+\$',clean))
    if missing:return dict(**g,text=clean,missing_glyphs=missing,dynamic=dynamic,lines=None,clipped=None)
    try:lines=font.wrap(clean,g['width']);long_word=False
    except ValueError:lines=clean.split('\n');long_word=True
    ink=[]
    for n,line in enumerate(lines):
        x=0;previous=None
        for char in line:
            ident=ord(char);v=font.rows[ident];x+=font.kern.get((previous,ident),0)
            tile=font.atlas.crop((v['x'],v['y'],v['x']+v['width'],v['y']+v['height']));bbox=tile.getchannel('A').getbbox()
            if bbox:ink.append((x+v['xoffset']+bbox[0],n*font.height+v['yoffset']+bbox[1],x+v['xoffset']+bbox[2],n*font.height+v['yoffset']+bbox[3]))
            x+=v['xadvance'];previous=ident
    bounds=[min(v[0] for v in ink),min(v[1] for v in ink),max(v[2] for v in ink),max(v[3] for v in ink)] if ink else [0,0,0,0]
    clipped=long_word or bounds[0]<0 or bounds[1]<0 or bounds[2]>g['width'] or bounds[3]>g['height']
    return dict(**g,text=clean,missing_glyphs=[],dynamic=dynamic,lines=lines,line_height=font.height,ink_bounds=bounds,
                required_line_box_height=len(lines)*font.height,clipped=clipped,accessible_by_scroll=bool(g['scrollbar']) and clipped)

def measurement():
    tree=load(MOD/'interface/eventwindow.gui');controls=named(tree);strings=locs();rows=[];unresolved=[];ignored=[]
    type_template={'country_event':'EventWindow','news_event':'EventWindow_News','unit_leader_event':'EventWindow_leader','operative_leader_event':'EventWindow_Operative'}
    for file in sorted((MOD/'events').glob('*.txt')):
        try:events=load(file)
        except ValueError as error:ignored.append(dict(file=file.name,error=str(error)));continue
        for kind,_,body in events:
            if kind not in type_template:continue
            if get(body,'hidden')=='yes' or get(body,'hide_window')=='yes':continue
            template=type_template[kind];ident=unquote(get(body,'id'))
            for field,part,name in [('title','top_Window','Title'),('desc','midsection','Description')]:
                for key in options(get(body,field)):
                    if key not in strings:unresolved.append(dict(id=ident,event_type=kind,field=field,key=key));continue
                    path=(template,part,name);m=metrics(strings[key],controls[path]);rows.append(dict(id=ident,file=file.name,event_type=kind,field=field,key=key,path=list(path),**m))
    counts={template:sum(row['path'][0]==template for row in rows) for template in type_template.values()}
    proxies=[]
    # There are no authored leader/operative events in this payload. Stress their
    # unchanged fields using actual country text, explicitly not a reachable bind.
    for template in ('EventWindow_leader','EventWindow_Operative'):
        if counts[template]:continue
        for field,part,name in [('title','top_Window','Title'),('desc','midsection','Description')]:
            candidates=[r for r in rows if r['field']==field and not r['dynamic'] and not r['missing_glyphs']]
            worst=max(candidates,key=lambda row:max((FONTS['ACBriefing20' if field=='title' else 'ACBriefing16'].measure(line) for line in row['text'].split('\n')),default=0) if field=='title' else len(row['text']))
            proxies.append(dict(template=template,source_event=worst['id'],key=worst['key'],field=field,
                coverage='Actual English country/news text stress only; no current leader/operative consumer',**metrics(worst['text'],controls[(template,part,name)])))
    static_title_clips=[r for r in rows if r['field']=='title' and not r['dynamic'] and r['clipped']]
    static_body_clips=[r for r in rows if r['field']=='desc' and not r['dynamic'] and r['clipped'] and not r['accessible_by_scroll']]
    return dict(schema=1,coverage='Actual authored English event text; dynamic substitutions are unresolved at runtime; source geometry/bitmap alpha, not native wrap or reflow',
        template_text_counts=counts,measured_fields=len(rows),static_title_clips=static_title_clips,unscrollable_static_body_clips=static_body_clips,
        scrollable_overlength_bodies=sum(bool(r.get('accessible_by_scroll')) for r in rows),
        dynamic_text_fields=sum(r['dynamic'] for r in rows),missing_glyph_fields=[r for r in rows if r['missing_glyphs']],
        unresolved_localization=unresolved,unparsed_inherited_event_files=ignored,leader_template_stress=proxies,fields=rows)

def apertures(mod=MOD):
    with Image.open(mod/'gfx/AC_event_style/leader_frame.dds') as image:frame=image.convert('RGBA').getchannel('A')
    # World-relative scaled positions derived independently from the actual GUI.
    controls=named(load(mod/'interface/eventwindow.gui'));base=('EventWindow_leader','midsection','leader_picture_container')
    leader=controls[base+('leader',)];border=controls[base+('leader_frame',)]
    def p(body):return [float(get(get(body,'position'),'x')),float(get(get(body,'position'),'y'))]
    a=p(leader);b=p(border);ls=float(get(leader,'scale'));fs=float(get(border,'scale'))
    rect=[(a[0]-b[0])/fs,(a[1]-b[1])/fs,(a[0]-b[0]+156*ls)/fs,(a[1]-b[1]+210*ls)/fs]
    integer=[math.floor(rect[0]),math.floor(rect[1]),math.ceil(rect[2]),math.ceil(rect[3])]
    clear=frame.crop(tuple(integer)).getextrema()==(0,0)
    agency=controls[('EventWindow_Operative','top_Window','agency_insignia')];ap=p(agency);rect_agency=ap+[ap[0]+117,ap[1]+119]
    return dict(leader=dict(portrait_source=[156,210],frame_source=[172,232],portrait_scale=ls,frame_scale=fs,
        portrait_in_frame=rect,conservative_integer_aperture=integer,fully_transparent=clear),
        agency=dict(frame_source=[117,119],bounds=rect_agency,body_width=528,title_top=170,
                    inside_body=rect_agency[2]<=528,clear_of_title=rect_agency[3]<=170),
        operative_portrait=dict(source=[156,210],scale=.7,rotation=.05,
            limitation='Literal rotation preserved; native units/pivot and dynamic portrait dimensions unaccepted'),
        layout='Existing zero-height leader roots and engine section reflow are retained, not simulated')

def all_sprites():
    result={}
    for file in sorted((MOD/'interface').glob('*.gfx')):
        for kind,_,body in get(load(file),'spriteTypes',[]):
            if not isinstance(body,list) or get(body,'texturefile') is None:continue
            name=unquote(get(body,'name'));result[name]=(kind,body)
    return result
def paint_text(canvas,text,body,x,y):
    m=metrics(text,body);font=FONTS[m['font']];layer=Image.new('RGBA',(m['width'],m['height']))
    if not m['missing_glyphs']:
        # Draw full text then clip only to the actual source control aperture.
        big=Image.new('RGBA',(m['width']+1,max(m['height'],m.get('required_line_box_height',0))+font.height))
        try:font.draw(big,m['text'],0,0,m['width'],big.height)
        except ValueError:pass
        layer=big.crop((0,0,m['width'],m['height']))
    canvas.alpha_composite(layer,(int(x),int(y)));ImageDraw.Draw(canvas).rectangle((x,y,x+m['width'],y+m['height']),outline='#315d72')
    return m
def render_template(template,data):
    tree=load(MOD/'interface/eventwindow.gui');controls=named(tree);root=controls[(template,)];sprites=all_sprites()
    canvas=Image.new('RGBA',(660,820),'#06111a');font=FONTS['ACBriefing16'];font.draw(canvas,'OFFLINE SOURCE COORDINATES / '+template,12,8,636,36)
    candidates=[r for r in data['fields'] if r['path'][0]==template and r['field']=='desc' and not r['dynamic'] and not r['missing_glyphs']]
    desc=max(candidates,key=lambda r:len(r['text']),default=None)
    if desc is None:
        proxy=next(r for r in data['leader_template_stress'] if r['template']==template and r['field']=='desc')
        desc=next(r for r in data['fields'] if r['id']==proxy['source_event'] and r['key']==proxy['key'])
    title=next(r for r in data['fields'] if r['id']==desc['id'] and r['field']=='title')
    chosen={'title':title,'desc':desc};labels=[]
    def visit(body,origin,path):
        p=get(body,'position',[]);x=origin[0]+float(get(p,'x','0'));y=origin[1]+float(get(p,'y','0'))
        name=unquote(get(body,'name'));path+=((name,) if name else ())
        for key in ('spriteType','quadTextureSprite'):
            sprite=unquote(get(body,key))
            if not sprite or sprite not in sprites:continue
            kind,definition=sprites[sprite];image=Image.open(MOD/unquote(get(definition,'texturefile'))).convert('RGBA')
            frames=int(get(definition,'noOfFrames','1'));fw=image.width//frames;frame=int(get(body,'frame','1'))-1
            image=image.crop((fw*frame,0,fw*(frame+1),image.height))
            # Default source initial frame; no animation/reflow is simulated.
            scale=float(get(body,'scale','1'))
            if scale!=1:image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
            if kind=='corneredTileSpriteType':
                size=get(definition,'size');dw=int(get(size,'x'));dh=int(get(size,'y'))
                if name=='Background':
                    parent=controls.get(path[:-1]);ps=get(parent,'size',[]) if parent else []
                    dw=int(get(ps,'width',str(dw)));dh=max(1,int(get(ps,'height',str(dh))))
                if sprite.endswith('_transparent'):image=Image.new('RGBA',(max(1,dw),max(1,dh)))
                else:
                    tile=image;image=Image.new('RGBA',(max(1,dw),max(1,dh)))
                    for ty in range(0,image.height,tile.height):image.alpha_composite(tile,(0,ty))
            canvas.alpha_composite(image,(round(x),round(y)))
        if name in ('Title','Description'):
            field='title' if name=='Title' else 'desc';labels.append((body,x,y,chosen[field]['text']))
        elif name in ('leader_fullname','leader_codename'):
            labels.append((body,x,y,'Government Office' if name=='leader_fullname' else 'Public Service'))
        for _,_,value in body:
            if isinstance(value,list) and get(value,'name') is not None:visit(value,(x,y),path)
    # Root x/y is a screen-centering anchor, not an internal content offset.
    for _,_,body in root:
        if isinstance(body,list) and get(body,'name') is not None:visit(body,(35,48),(template,))
    for body,x,y,text in labels:paint_text(canvas,text,body,x,y)
    note='Sample '+str(desc['id'])+'. Literal anchors only; native section sizing, options and dynamic names remain untested.'
    font.draw(canvas,note,12,744,636,60)
    out=io.BytesIO();canvas.save(out,format='PNG');return out.getvalue()

def generated():
    text=(MOD/'interface/eventwindow.gui').read_text(encoding='utf-8-sig');assert_preserved(text)
    data=measurement();data['apertures']=apertures();data['restoration']=report(text)
    files={'measurements.json':(json.dumps(data,indent=2)+'\n').encode()}
    names=('EventWindow','EventWindow_News','EventWindow_leader','EventWindow_Operative')
    for name in names:files[name+'.png']=render_template(name,data)
    from event_style.build_art import SIZES
    from PIL import ImageOps
    preview=Image.new('RGBA',(1080,960),'#081621');label=FONTS['ACBriefing16']
    for index,key in enumerate(SIZES):
        x=(index%3)*360;y=(index//3)*240
        label.draw(preview,key,x+8,y+6,344,36)
        source=Image.open(MOD/f'gfx/AC_event_style/{key}.dds').convert('RGBA')
        if key=='operative_background':source=source.crop((0,0,528,596))
        source.thumbnail((344,190),Image.Resampling.LANCZOS);preview.alpha_composite(source,(x+8,y+40))
    raw=io.BytesIO();preview.save(raw,format='PNG');files['assets.png']=raw.getvalue()
    strip=Image.open(MOD/'gfx/AC_event_style/operative_background.dds').convert('RGBA')
    contact=Image.new('RGBA',(960,4*210),'#081621')
    for frame in range(24):
        x=(frame%6)*160;y=(frame//6)*210;label.draw(contact,'Frame '+str(frame+1),x+8,y+4,144,20)
        thumb=strip.crop((frame*528,0,(frame+1)*528,596)).resize((150,169),Image.Resampling.LANCZOS)
        contact.alpha_composite(thumb,(x+5,y+30))
    raw=io.BytesIO();contact.save(raw,format='PNG');files['operative-frames.png']=raw.getvalue()
    html='<!doctype html><meta charset="utf-8"><title>Offline event style review</title><style>body{background:#081621;color:#daedf2;font:17px sans-serif;max-width:1400px;margin:auto}img{max-width:100%;border:1px solid #315d72}section{display:inline-block;vertical-align:top;width:49%}code{color:#63ccdf}</style><h1>Offline event-window source review</h1><p>Actual delivered textures, literal source controls, selected frames and shipped bitmap glyphs. This is a reconstruction, not a native screenshot. Native dynamic section sizing, rotation, scrolling, option reflow, animation and agency slicing remain unaccepted.</p>'
    html+='<p>The original GUI capture and fit apertures are unchanged. Leader/operative drawings use actual English country text as a labelled stress proxy: this source contains no authored events of those types. Long descriptions are clipped only to their existing source apertures; the country/news scroll controls remain present.</p>'
    html+='<p>Actual static title clips: '+str(len(data['static_title_clips']))+'. Unscrollable actual static body clips: '+str(len(data['unscrollable_static_body_clips']))+'. See <a href="measurements.json">full metrics, dynamic limitations and restoration proof</a>.</p>'
    for name in names:html+='<section><h2>'+name+'</h2><img src="'+name+'.png" alt="Offline '+name+' literal source controls"></section>'
    html+='<h2>Original texture package</h2><img src="assets.png" alt="All12 original delivered textures, operative first frame"><h2>All24 operative states</h2><img src="operative-frames.png" alt="Every actual operative frame">'
    files['gallery.html']=(html+'\n').encode();return files
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    files=generated()
    for name,data in files.items():
        path=OUT/name
        if a.check:
            good=path.is_file() and (same_review_png(path.read_bytes(),data) if name.endswith('.png') else path.read_bytes().replace(b'\r\n',b'\n')==data)
            if not good:raise SystemExit('Offline event style review differs: '+name)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    m=json.loads(files['measurements.json']);print('Offline event metrics:',m['measured_fields'],'fields;',len(m['static_title_clips']),'static title clips;',len(m['unscrollable_static_body_clips']),'unscrollable static body clips; no native claim')
    if m['static_title_clips'] or m['unscrollable_static_body_clips']:raise SystemExit('Real current localized text needs separately reviewed layout repair')
if __name__=='__main__':main()
