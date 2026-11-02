"""Actual new GUI/sprite consumers, not manifest-only image dimensions."""
from pathlib import Path
import sys
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get,walk
from air_content import AIRCRAFT,YEARS,frame_id


def scalar(value):return value.strip('"') if isinstance(value,str) else value
def named(tree,name):return next(body for _,body in walk(tree) if scalar(get(body,'name'))==name)
def load(path):return parse(path.read_text(encoding='utf-8-sig'))


def blueprint_contracts(gui=None,gfx=None,mod=MOD):
    mod=Path(mod);gui=load(mod/'interface/equipmentdesigner/planes/ac_air_blueprints.gui') if gui is None else gui
    gfx=load(mod/'interface/ac_air_art.gfx') if gfx is None else gfx
    sprites={scalar(get(body,'name')):body for _,_,body in get(gfx,'spriteTypes')};rows=[]
    for family in AIRCRAFT:
        if not family.airframe_parent:continue
        for year in YEARS:
            ident=frame_id(family.id,year);window=named(gui,'equipment_designer_'+ident)
            dimensions=get(window,'size');expected=(int(get(dimensions,'width')),int(get(dimensions,'height')))
            if expected!=(508,248):raise ValueError('Aircraft blueprint control differs from primary508x248 contract: '+ident)
            overlay=named([['window','=',window]],'equipment_image_overlay');sprite=scalar(get(overlay,'spriteType'));definition=sprites[sprite]
            if sprite!='GFX_TC_'+ident:raise ValueError('Wrong aircraft blueprint consumer binding: '+ident)
            scale=float(get(overlay,'scale','1'));frames=int(get(definition,'noOfFrames','1'))
            path=mod/scalar(get(definition,'texturefile'))
            with Image.open(path) as im:
                if frames<1 or im.width%frames:raise ValueError('Invalid aircraft blueprint frame width')
                actual=(im.width/frames*scale,im.height*scale)
            point=get(overlay,'position')
            if actual!=expected or (get(point,'x'),get(point,'y'))!=('0','0'):raise ValueError('Actual aircraft blueprint DDS/control bounds mismatch: '+ident)
            rows.append(dict(id=ident,control='equipment_designer_'+ident,sprite=sprite,texture=path.relative_to(mod).as_posix(),dimensions=list(actual),frames=frames,scale=scale))
    return rows
