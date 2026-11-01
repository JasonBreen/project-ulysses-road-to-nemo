"""Actual GUI consumer/definition/header/alpha checks, independent of manifest sizes."""
import json,sys
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from usea_expansion.script import parse,get
from event_style.migration import SPRITES,FONTS,assert_preserved
from event_picture_fit.audit import controls
from event_picture_fit.fit import assert_fits
def definitions(text):
    result={}
    for kind,_,body in get(parse(text),'spriteTypes',[]):
        name=get(body,'name').strip('"')
        if name in result:raise ValueError('Duplicate event sprite '+name)
        result[name]=(kind,body)
    return result
def metadata(body):return {k.lower():v for k,_,v in body if k.lower() not in ('name','texturefile')}
def validate_art(mod=MOD,gfx=None):
    if gfx is None:gfx=(mod/'interface/ac_event_style.gfx').read_text(encoding='utf-8-sig')
    actual=definitions(gfx);primary=json.loads((HERE/'primary.json').read_text())['sprites']
    wanted={new:old for _,_,old,new in SPRITES}
    if set(actual)!=set(wanted):raise ValueError('Wrong scoped event sprite set')
    result=[]
    for name,(kind,body) in actual.items():
        old=primary[wanted[name]]
        if kind!=old['kind'] or metadata(body)!=metadata(old['fields']):raise ValueError('Native sprite metadata changed '+name)
        path=mod/get(body,'texturefile').strip('"')
        with Image.open(path) as source:
            if source.format!='DDS':raise ValueError('Event texture is not DDS')
            image=source.convert('RGBA');w,h=image.size
        frames=int(get(body,'noOfFrames','1'))
        if w%frames:raise ValueError('Nonintegral event frame width '+name)
        expected=[234,119] if name=='GFX_ac_event_agency_office' else old['dimensions']
        if [w,h]!=expected:raise ValueError('Actual consumer texture dimensions changed '+name)
        if name=='GFX_ac_event_country_default':assert_fits('country_event',(w,h))
        if name=='GFX_ac_event_news_default':assert_fits('news_event',(w,h))
        if name=='GFX_ac_event_transparent' and image.getchannel('A').getextrema()!=(0,0):raise ValueError('Technical transparent quad has painted pixels')
        result.append(dict(sprite=name,kind=kind,texture=str(path.relative_to(mod)).replace('\\','/'),dimensions=[w,h],frames=frames,frame_size=[w//frames,h]))
    fonts=[body for kind,_,body in parse(gfx) if kind=='bitmapfont']
    if {get(body,'name').strip('"') for body in fonts}!={'ACEvent16','ACEvent20'}:raise ValueError('Event font aliases differ')
    for font in fonts:
        name=get(font,'name').strip('"');expected='gfx/fonts/ACBriefing'+name.removeprefix('ACEvent')
        if get(font,'path').strip('"')!=expected:raise ValueError('Event font pixels rebound')
    from event_style.review import apertures
    a=apertures(mod)
    if not a['leader']['fully_transparent'] or not a['agency']['inside_body'] or not a['agency']['clear_of_title']:
        raise ValueError('Actual event portrait/agency aperture is obstructed')
    return result
def main():
    text=(MOD/'interface/eventwindow.gui').read_text(encoding='utf-8-sig');assert_preserved(text);controls()
    result=validate_art();print('Event style actual consumers:',len(result),'sprite bindings; original metadata/23-field GUI restoration PASS')
if __name__=='__main__':main()
