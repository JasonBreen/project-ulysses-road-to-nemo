"""Verify actual native-shaped naval control/texture consumers and defaults."""
import copy
import json
from pathlib import Path
import sys
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion')]
from script import parse,get,walk,setv
from naval_content import SHIPS,YEARS,hull_id,recipe
from naval_ui import layer_name

def scalar(v):return v.strip('"') if isinstance(v,str) else v
def load(path):return parse(path.read_text(encoding='utf-8-sig'))
def named(tree,name):return next(b for _,b in walk(tree) if scalar(get(b,'name'))==name)
def pos(body):return {k:int(v) for k,_,v in get(body,'position',[])}

def blueprint_contracts(gui=None,gfx=None,mod=MOD):
    mod=Path(mod);gui=load(mod/'interface/equipmentdesigner/ships/ac_naval_blueprints.gui') if gui is None else gui
    gfx=load(mod/'interface/ac_naval_art.gfx') if gfx is None else gfx
    sprites={scalar(get(b,'name')):b for _,_,b in get(gfx,'spriteTypes')};facts=json.loads((HERE/'primary_contract.json').read_text());rows=[];images={}
    from audit import equipment,modules
    from naval_primary import Primary
    p=Primary.from_capture(facts['catalog'],equipment(),modules())
    for f in SHIPS:
        for year in YEARS:
            ident=hull_id(f.id,year);window=named(gui,'equipment_designer_'+ident);original=facts['blueprints'][f.id]
            restored=copy.deepcopy(window);setv(restored,'name',get(original,'name'))
            old_nodes=list(walk([['window','=',original]]));new_nodes=list(walk([['window','=',restored]]))
            if len(new_nodes)!=len(old_nodes):raise ValueError('Missing native naval blueprint control structure: '+ident)
            for (old_kind,old),(kind,body) in zip(old_nodes,new_nodes):
                if kind!=old_kind or get(body,'name')!=get(old,'name'):raise ValueError('Native naval control binding/order changed: '+ident)
                for field,_,value in old:
                    if field.lower() not in ('spritetype','quadtexturesprite'):continue
                    old_sprite=scalar(value);current=scalar(get(body,field))
                    expected='GFX_ac_naval_empty' if old_sprite=='GFX_tiled_window_transparent' else 'GFX_SD_'+ident if get(old,'name')=='"equipment_image"' else layer_name(old_sprite)
                    if current!=expected:raise ValueError('Wrong actual naval sprite consumer: '+ident+':'+str(current))
                    definition=sprites[current];frames=int(get(definition,'noOfFrames','1'));scale=float(get(body,'scale','1'))
                    path=mod/scalar(get(definition,'texturefile'))
                    expected_dims=(1,1) if old_sprite=='GFX_tiled_window_transparent' else tuple(facts['layers'][old_sprite]['dimensions'])
                    if path not in images:
                        with Image.open(path) as image:images[path]=(image.size,image.convert('RGBA').getchannel('A').getbbox())
                    (width,height),aperture=images[path]
                    if frames<1 or width%frames or (width/frames*scale,height*scale)!=expected_dims:raise ValueError('Actual naval DDS/frame/scale dimensions mismatch: '+current)
                    point=pos(body)
                    if aperture and (point.get('x',0)+aperture[0]*scale<0 or point.get('y',0)+aperture[1]*scale<0 or point.get('x',0)+aperture[2]*scale>512 or point.get('y',0)+aperture[3]*scale>260):raise ValueError('Naval alpha aperture exceeds real control: '+current)
                    setv(body,field,value)
            if restored!=original:raise ValueError('Native naval blueprint geometry/control property changed: '+ident)
            # Validate the actual selected module's category has both normal
            # and highlight controls, not merely a sprite in a manifest.
            slotroot=named([['window','=',window]],'module_slots');selected=[]
            for slot,module in recipe(f.id,year).items():
                category=p.resolve(module,'modules')['category'];slotnode=named([['root','=',slotroot]],slot)
                normal=named([['slot','=',slotnode]],category)
                try:highlight=named([['slot','=',slotnode]],category+'@highlight')
                except StopIteration:
                    # A few installed native fire-control alternatives use
                    # literal @highlight; its exact structural binding above
                    # remains preserved and checked against primary.
                    highlight=named([['slot','=',slotnode]],'@highlight')
                normal_images=[b for k,b in walk([['category','=',normal]]) if k=='iconType']
                high_images=[b for k,b in walk([['category','=',highlight]]) if k=='iconType']
                if not normal_images or not high_images:raise ValueError('Missing selected naval category image/highlight: '+slot)
                selected.append(dict(slot=slot,module=module,category=category,normal=[scalar(get(b,'spriteType')) for b in normal_images],highlight=[scalar(get(b,'spriteType')) for b in high_images]))
            rows.append(dict(id=ident,control='equipment_designer_'+ident,container=[512,260],dimensions=[508,248],sprite='GFX_SD_'+ident,
                texture=scalar(get(sprites['GFX_SD_'+ident],'texturefile')),selected_categories=selected,primary_structure_preserved=True))
    return rows

def default_composite(row):
    """Actual default-category images at actual shipped positions, offline."""
    gui=load(MOD/'interface/equipmentdesigner/ships/ac_naval_blueprints.gui');window=named(gui,row['control']);sprites={scalar(get(b,'name')):b for _,_,b in get(load(MOD/'interface/ac_naval_art.gfx'),'spriteTypes')}
    canvas=Image.new('RGBA',(512,260),(8,22,33,255))
    def paste(body):
        point=pos(body);definition=sprites[scalar(get(body,'spriteType'))]
        with Image.open(MOD/scalar(get(definition,'texturefile'))) as image:canvas.alpha_composite(image.convert('RGBA'),(point['x'],point['y']))
    paste(named([['window','=',window]],'equipment_image'))
    root=named([['window','=',window]],'module_slots')
    for selected in row['selected_categories']:
        slot=named([['root','=',root]],selected['slot']);category=named([['slot','=',slot]],selected['category'])
        for kind,body in walk([['category','=',category]]):
            if kind=='iconType':paste(body)
    return canvas
