"""Explicit read-only capture of installed naval technical contracts, no pixels."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion')]
from naval_content import SHIPS,FAMILIES
from naval_primary import Primary,STATS
from script import parse,get,walk

def digest(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def capture(reference):
    reference=Path(reference);p=Primary(reference);out=dict(schema=1,reference_version=json.loads((reference/'launcher-settings.json').read_text())['rawVersion'],
        provenance='Installed primary technical declarations/identifiers/dimensions/hashes only; no engine pixels or native acceptance',families={},blueprints={},layers={},foundations={})
    gfx={}
    for name in ('equipmentdesignerview.gfx','equipmentdesignermodules.gfx'):
        path=reference/'interface'/name;p.record(path)
        for _,body in walk(parse(path.read_text(encoding='utf-8-sig'))):
            key=get(body,'name');texture=get(body,'texturefile',get(body,'textureFile'))
            if key and texture:gfx[key.strip('"')]=texture.strip('"')
    for f in SHIPS:
        body=p.resolve(f.hull_parent);old=p.resolve(f.parent)
        out['families'][f.id]=dict(parent=f.parent,hull_parent=f.hull_parent,archetype=f.archetype,
            parent_priority=old['priority'],hull_priority=body['priority'],slots={k:v for k,_,v in body['module_slots']},
            legacy_slots={k:v for k,_,v in old['module_slots']},module_count_limits=body.get('module_count_limit',[]),
            legacy_default_modules=old.get('default_modules',[]),source_stats={k:body.get(k) for k in STATS})
        path=reference/f'interface/equipmentdesigner/ships/ship_hull_{f.native_blueprint}.gui';p.record(path)
        gui=parse(path.read_text(encoding='utf-8-sig'));container=next(v for _,v in walk(gui) if get(v,'name')=='"equipment_designer_ship_hull_'+f.native_blueprint+'"')
        out['blueprints'][f.id]=container
        for kind,node in walk([['window','=',container]]):
            for key,_,value in node:
                if key.lower() not in ('spritetype','quadtexturesprite'):continue
                sprite=value.strip('"')
                if sprite=='GFX_tiled_window_transparent':continue
                rel=gfx[sprite]
                with Image.open(reference/rel) as im:size=list(im.size)
                out['layers'][sprite]=dict(path=rel,dimensions=size,kind='topview' if get(node,'name')=='"equipment_image"' else 'module_patch',
                    evidence='Exact dimensions/hash only; output art must be original',raw_sha256=hashlib.sha256((reference/rel).read_bytes()).hexdigest())
    required={'radio','basic_machine_tools','electronic_mechanical_engineering'}|{v for f in SHIPS for v in (f.legacy_foundation,f.designer_foundation)}
    for ident in sorted(required):
        if ident not in p.tech:raise ValueError('Missing native foundation '+ident)
        p.record(p.files[('technologies',ident)]);out['foundations'][ident]=p.tech[ident]
    out['native_semantic_modules']={}
    for ident in ('ship_deck_space','ship_sonar_4','ship_depth_charge_4','ship_medium_battery_4','light_ship_engine_4','ship_armor_cruiser_4','ship_torpedo_4','ship_torpedo_sub_4','dp_light_battery_4'):
        p.resolve(ident,'modules');out['native_semantic_modules'][ident]=p.modules[ident]
    ai_file=reference/'common/ai_equipment/generic_naval.txt'
    out['native_design_groups']={k:dict(roles=get(b,'roles'),priority=get(b,'priority')) for k,_,b in parse(ai_file.read_text(encoding='utf-8-sig'))}
    folder_file=reference/'common/technology_tags/00_technology.txt';p.record(folder_file)
    out['native_folder']=get(get(parse(folder_file.read_text(encoding='utf-8-sig')),'technology_folders'),'naval_folder')
    for rel in ('common/units/equipment/modules/00_ship_modules.txt','common/ai_equipment/_documentation.md','common/ai_equipment/generic_naval.txt',
                'common/ai_strategy/default.txt','common/defines/00_defines.lua','documentation/dynamic_variables_documentation.md'):
        p.record(reference/rel)
    out['semantics']=dict(defaults='Native complete ships contain default_modules and zero bare weapon stats; count each selected default once.',
        module_manpower='Native ship_deck_space declares manpower outside add_stats; this is a separate once-only module crew contribution.',
        classification='Native ship_medium_battery modules add capital_ship to the cruiser role. Native deck adds capital_ship to carrier.',
        carrier_size_increment=10,sub_hunter_depth_charge_threshold=15,sub_hunter_detection_threshold=2,
        detection='00_defines.lua:2185–2188 records reworked detection/visibility formula; older preceding formulas are marked deprecated. Not a native result.',
        upkeep='dynamic_variables_documentation.md documents num_ships and num_ships_with_type, including carrier/capital/screen/submarine; commissioned aggregate, not per-hull telemetry.',
        no_equivalence=['Mining missions and MTG-disabled mine behavior','Modern carrier air groups','Submarine-versus-submarine warfare','Missile/nuclear/strategic ships'])
    out['catalog']=dict(equipment={i:p.equipment[i] for i in sorted(p.used['equipment']) if i in p.equipment},
        modules={i:p.modules[i] for i in sorted(p.used['modules'])},duplicates={})
    out['source_sha256']=dict(sorted(p.sources.items()))
    (HERE/'primary_contract.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
    return out

if __name__=='__main__':
    arg=argparse.ArgumentParser();arg.add_argument('reference',type=Path);a=arg.parse_args();out=capture(a.reference)
    print('NAVAL primary:',len(out['families']),'roles,',len(out['layers']),'source image dimensions; no pixels copied')
