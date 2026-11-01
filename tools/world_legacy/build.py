"""Compile bounded repairs from retained 60ec3a6 military setup sources.

History-only setup: no startup/monthly effect grants forces to existing saves.
--reference captures effective primary facts; ordinary --check uses the retained
technical contract, so offline CI never needs an installed game.
"""
import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get, setv, walk, render
from primary import Primary
sys.path.insert(0,str(ROOT/'tools/world_starts'))
from armor import ARMOR

TAGS = ('BLK', 'OSE', 'SAP', 'FAT')
BUDGETS = {'BLK': (45,12), 'OSE': (50,23), 'SAP': (8,8), 'FAT': (12,6)}
FLAG = 'ac_world_legacy_setup_loaded'
OUTPUTS = {}
TRANSPORT_TECH = '''# Compatibility only: effective mod air_techs.txt omits the installed transport unlock.
# Source: installed common/technologies/air_techs.txt, first transport technology.
# No research button or new aircraft; granted only by repaired new histories.
technologies = {
 ac_wl_transport_support = {
  enable_equipments = { transport_plane_equipment_1 }
  allow = { always = no }
  research_cost = 1
  start_year = 1991
 }
}
'''


def normalized_hash(data):
    return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()


def put(relative, data):
    if isinstance(data,str) and relative.startswith('history/units/'):
        data=re.sub(r'\A[ \t]+\n','\n',data)
        data=re.sub(r'(?m)^}[ \t]+$','}',data)
        data=re.sub(r'(?m)^(\s*name = "1st Task Force")[ \t]+$',r'\1',data)
        data=re.sub(r'(?m)^(\s*creator\s*=\s*"[^"]+")[ \t]+$',r'\1',data)
    OUTPUTS[MOD / relative] = data.encode() if isinstance(data, str) else data


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t'+line for line in body.splitlines()) + '\n}\n'


def read_source(folder, name):
    text = (HERE / 'baseline' / folder / name).read_text(encoding='utf-8-sig')
    if name == 'FAT_navy.txt':
        text = text.replace('name = "1st Task Force""', 'name = "1st Task Force"')
    return text


def condition(nodes, dlcs, tag, human=(), loaded=False):
    values=[]
    for key,_,value in nodes:
        lower=key.lower()
        if lower=='has_dlc': answer=value.strip('"') in dlcs
        elif lower=='has_country_flag':
            if value != FLAG: raise ValueError('Unexpected setup guard '+value)
            answer=loaded
        elif lower in ('not','or','and'):
            answers=[condition([n],dlcs,tag,human,loaded) for n in value]
            answer=any(answers) if lower=='or' else not all(answers) if lower=='not' else all(answers)
        elif lower=='is_ai': answer=(tag not in human)==(value=='yes')
        elif re.fullmatch('[A-Z]{3}',key): answer=condition(value,dlcs,key,human,loaded)
        elif lower=='always':answer=value=='yes'
        else:raise ValueError('Unknown history predicate '+key)
        values.append(answer)
    return all(values)


def selected(nodes, dlcs, tag, human=(), loaded=False):
    previous=None
    for key,op,value in nodes:
        if key=='if':
            chosen=condition(get(value,'limit',[]),dlcs,tag,human,loaded);previous=chosen
            if chosen:
                yield from selected([n for n in value if n[0] not in ('limit','else','else_if')],dlcs,tag,human,loaded)
            else:
                for kind,_,body in [n for n in value if n[0] in ('else','else_if')]:
                    if kind=='else' or condition(get(body,'limit',[]),dlcs,tag,human,loaded):
                        yield from selected([n for n in body if n[0]!='limit'],dlcs,tag,human,loaded);previous=True;break
        elif key in ('else','else_if'):
            if previous is None:raise ValueError('Orphan history branch')
            if not previous and (key=='else' or condition(get(value,'limit',[]),dlcs,tag,human,loaded)):
                yield from selected([n for n in value if n[0]!='limit'],dlcs,tag,human,loaded);previous=True
        else:
            previous=None;yield key,op,value


def equipment_nodes(tree):
    for kind,body in walk(tree):
        if kind in ('create_equipment_variant','add_equipment_to_stockpile'):
            yield get(body,'type')
        elif kind=='add_equipment_production':yield get(get(body,'equipment',[]),'type')
        elif kind=='ship':
            for equipment,_,_ in get(body,'equipment',[]):yield equipment
    for _,_,wings in get(tree,'air_wings',[]):
        for equipment,_,_ in wings:yield equipment


def all_sources():
    for row in json.loads((HERE/'intake.json').read_text())['files']:
        yield row,parse(read_source('countries' if '/countries/' in row['file'] else 'units',Path(row['file']).name))


def capture(reference):
    primary=Primary(reference);equipment=set();modules=set()
    for _,tree in all_sources():
        equipment.update(equipment_nodes(tree))
        for kind,body in walk(tree):
            if kind=='create_equipment_variant':modules.update(v for _,_,v in get(body,'modules',[]) if v!='empty')
    equipment.update(('scout_plane_equipment_1','train_equipment_1','support_equipment_1',
                      'infantry_equipment_1','motorized_equipment_1','artillery_equipment_1',
                      'destroyer_1','destroyer_2','light_cruiser_1','light_cruiser_2',
                      'heavy_cruiser_1','heavy_cruiser_2','battleship_1','battleship_2',
                      'carrier_1','carrier_2','submarine_1','submarine_2'))
    for recipe in ARMOR.values():
        equipment.update((recipe['legacy'],recipe['modern']))
        modules.update(recipe['modules'].values())
    modules.add('ship_armor_cruiser_2')
    result=dict(schema=1,reference='Installed HOI4 primary definitions; source-only facts, no native validation',
        equipment={ident:primary.equipment_row(ident) for ident in sorted(equipment)},
        modules={ident:primary.module_row(ident) for ident in sorted(modules)},
        sources=primary.sources,
        lar=dict(legacy_tech='scout_plane1',legacy_allow_branch=get(primary.tech['scout_plane1'],'allow_branch'),
                 camera_tech=primary.unlock('recon_camera','modules'),
                 camera_allow_branch=get(primary.tech[primary.unlock('recon_camera','modules')],'allow_branch'),
                 status='La Resistance-disabled reconnaissance mission capability is an explicit release gap; equipment existence or force-granted technology does not prove mission availability.'))
    # An explicit owned compatibility bridge, rather than pretending the omitted
    # installed transport technology survives the effective mod file override.
    result['equipment']['transport_plane_equipment_1']['technology']='ac_wl_transport_support'
    result['equipment']['transport_plane_equipment_1']['compatibility_owner']='common/technologies/ac_world_legacy_support.txt'
    result['production_context_sources']={relative:normalized_hash((Path(reference)/relative).read_bytes()) for relative in (
        'documentation/effects_documentation.md','history/units/USA_1936.txt','history/units/GER_1936.txt')}
    result['production_context_note']='Standalone ship-effect example uses efficiency0.1; native infantry OOB examples use efficiency50. Preserve inherited history values, use50 for new lines; native numeric interpretation unverified.'
    result['deployment_context_sources']={'history/units/AFG_1936_nsb.txt':normalized_hash((Path(reference)/'history/units/AFG_1936_nsb.txt').read_bytes())}
    (HERE/'primary_contract.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')


def variant_map(history, dlcs, tag):
    return {(get(body,'type'),get(body,'name')):body for key,_,body in selected(history,dlcs,tag) if key=='create_equipment_variant'}


def clean_production(tree):
    for kind,body in walk(tree):
        if kind=='add_equipment_production':
            for key in ('progress',):
                value=float(get(body,key,'0'))
                if value>1:setv(body,key,format(value/100,'.8g'))


def ensure_instant(tree):
    body=get(tree,'instant_effect')
    if body is None:
        body=[];tree.append(['instant_effect','=',body])
    return body


def add_line(tree,tag,equipment,version=None,factories=1):
    details=f'equipment = {{ type = {equipment} creator = {tag} '+(f'version_name = {version} ' if version else '')+'}\n'
    details+=f'requested_factories = {factories}\nprogress = 0\nefficiency = 50'
    ensure_instant(tree).extend(parse(block('add_equipment_production',details)))


def preserve_unmodified_blocks(original,newtree):
    """Keep complete troop/ship declarations and their comments byte-stable."""
    oldtree=parse(original)
    tokens=list(re.finditer(r'"(?:\\.|[^"\\])*"|\#[^\n]*|[{}=]|[^\s{}=]+',original))
    spans=[];depth=0;start=None;name=None
    for match in tokens:
        token=match.group()
        if token.startswith('#'):continue
        if depth==0 and start is None:
            start=match.start();name=token
        if token=='{':depth+=1
        elif token=='}':
            depth-=1
            if depth==0:spans.append((name,start,match.end()));start=None
    indexed={};replacements=[]
    for name,begin,end in spans:
        ordinal=indexed.get(name,0);indexed[name]=ordinal+1
        old=[n for n in oldtree if n[0]==name][ordinal]
        choices=[n for n in newtree if n[0]==name]
        if ordinal>=len(choices):raise ValueError('Unexpected removed top-level block '+name)
        if old!=choices[ordinal]:replacements.append((begin,end,render([choices[ordinal]])))
    for begin,end,text in reversed(replacements):original=original[:begin]+text+original[end:]
    for name,_,body in newtree:
        if name not in indexed:original+='\n'+render([[name,'=',body]])+'\n'
    assert parse(original)==newtree,'Localized block replacement lost syntax'
    return original


def project_navy(tag,history,tree):
    legacy=variant_map(history,set(),tag);designer=variant_map(history,{'Man the Guns'},tag)
    old_names={name:equipment for equipment,name in legacy}
    definitions={}
    for kind,body in walk(tree):
        if kind=='ship':
            for equipment,_,details in get(body,'equipment',[]):
                definitions[(equipment,get(details,'version_name'))]=get(body,'definition')
    replacements={};supplements=[]
    for (equipment,name),body in designer.items():
        tier=re.search(r'_(\d)$',equipment);tier=min(2,max(1,int(tier[1]))) if tier else 1
        role=definitions.get((equipment,name))
        if not role:
            if 'submarine' in equipment:role='submarine'
            elif 'carrier' in equipment:role='carrier'
            elif 'light' in equipment:role='destroyer'
            elif 'heavy' in equipment:role='battleship'
            else:
                weapon=get(get(body,'modules',[]),'fixed_ship_battery_slot','')
                role='light_cruiser' if 'light_medium' in weapon else 'heavy_cruiser'
        target=old_names.get(name,role+'_'+str(tier))
        replacements[(equipment,name)]=target
        if name not in old_names:
            supplements.extend(parse(block('create_equipment_variant',f'name = {name}\ntype = {target}\nupgrades = {{ ship_reliability_upgrade = 1 }}')))
    for kind,body in walk(tree):
        if kind=='ship':
            for entry in get(body,'equipment',[]):entry[0]=replacements[(entry[0],get(entry[2],'version_name'))]
        elif kind=='add_equipment_production':
            equipment=get(body,'equipment',[]);key=(get(equipment,'type'),get(equipment,'version_name'))
            setv(equipment,'type',replacements[key])
    return tree,supplements


def prepare_rosters(tag,history):
    names=[tag+'_'+s for s in ('land','air','air_dlc','navy','navy_dlc')]
    if tag=='FAT':names.append('FAT_land_vs_ai')
    trees={name:parse(read_source('units',name+'.txt')) for name in names}
    for tree in trees.values():clean_production(tree)
    if tag=='FAT':
        for name in ('FAT_land','FAT_land_vs_ai'):
            for kind,body in walk(trees[name]):
                if kind=='add_equipment_production' and get(get(body,'equipment',[]),'type')=='modern_tank_equipment_1':setv(body,'requested_factories','2')
    if tag=='SAP':
        for kind,body in walk(trees['SAP_land']):
            if kind=='add_equipment_production' and get(get(body,'equipment',[]),'type')=='modern_tank_equipment_1':setv(body,'requested_factories','1')
    if tag=='BLK':
        instant=ensure_instant(trees['BLK_navy_dlc']);matches=[n for n in instant if n[0]=='add_equipment_production' and get(get(n[2],'equipment',[]),'version_name')=='"Zerstörer 1934A Class"']
        assert len(matches)==3
        setv(matches[0][2],'amount','8');instant.remove(matches[1])
    if tag in ('SAP','FAT'):
        variants=variant_map(history,{'Man the Guns'},tag)
        eq,name=next((e,n) for e,n in variants if 'light' in e)
        add_line(trees[tag+'_navy_dlc'],tag,eq,name,2 if tag=='SAP' else 1)
    if tag in ('SAP','FAT'):
        add_line(trees[tag+'_air'],tag,'fighter_equipment_1')
        variants=variant_map(history,{'By Blood Alone'},tag)
        eq,name=next((e,n) for e,n in variants if e=='small_plane_airframe_1')
        add_line(trees[tag+'_air_dlc'],tag,eq,name)
    # Supply replacements use currently unassigned MIL in the two large starts.
    if tag in ('BLK','OSE'):
        for equipment in ('train_equipment_1','support_equipment_1','artillery_equipment_1','anti_air_equipment_1'):
            add_line(trees[tag+'_land'],tag,equipment)
    # Preserve every pre-existing legacy wing, adding only the specialist gap.
    scout_variants=[]
    if tag in ('BLK','OSE'):
        legacy_wings=get(trees[tag+'_air'],'air_wings')
        for state,_,wings in get(trees[tag+'_air_dlc'],'air_wings',[]):
            scouts=[copy.deepcopy(n) for n in wings if 'scout_plane' in n[0]]
            if scouts:
                for n in scouts:n[0]='scout_plane_equipment_1'
                legacy_wings.append([state,'=',scouts])
        designer=variant_map(history,{'By Blood Alone'},tag)
        for (equipment,name),body in designer.items():
            if 'scout_plane' in equipment:
                scout_variants.extend(parse(block('create_equipment_variant',f'name = {name}\ntype = scout_plane_equipment_1\nupgrades = {{ plane_range_upgrade = 1 }}')))
    projected,supplements=project_navy(tag,history,copy.deepcopy(trees[tag+'_navy_dlc']))
    trees[tag+'_navy_1991_legacy']=projected
    armor_roles=set()
    for name in [n for n in names if '_land' in n]:
        original=trees[name];templates={get(v,'name'):v for k,v in walk(original) if k=='division_template'}
        present={role for role,recipe in ARMOR.items() if any(recipe['subunit'] in [k for k,_,_ in get(v,'regiments',[])] for v in templates.values())}
        armor_roles.update(present)
        # Retained Belkan/Osean tracked artillery previously had no replacement
        # line. Belka reallocates one of its fifteen tank factories; Osea has
        # spare MIL. Keep all industrial budgets and standing formations.
        queued={get(get(v,'equipment'),'type') for k,v in walk(original) if k=='add_equipment_production'}
        for role in sorted(present-queued):
            if tag=='BLK':
                donor=next(v for k,v in walk(original) if k=='add_equipment_production' and get(get(v,'equipment'),'type')=='modern_tank_equipment_1')
                setv(donor,'requested_factories',str(int(get(donor,'requested_factories'))-1))
            add_line(original,tag,role)
        modern=copy.deepcopy(original)
        for kind,body in walk(modern):
            if kind=='add_equipment_production':
                equipment=get(body,'equipment');ident=get(equipment,'type')
                if ident in ARMOR:
                    recipe=ARMOR[ident];setv(equipment,'type',recipe['modern']);setv(equipment,'version_name','"'+tag+' '+recipe['label']+'"')
            elif kind=='division':
                template=templates[get(body,'division_template')];regiments=[k for k,_,_ in get(template,'regiments',[])]
                forced=[]
                for role in sorted(present):
                    recipe=ARMOR[role]
                    if recipe['subunit'] in regiments:
                        forced.append([recipe['modern'],'=',parse(f'owner = {tag}\ncreator = {tag}\nversion_name = "{tag} {recipe["label"]}"')])
                if forced:setv(body,'force_equipment_variants',forced)
        trees[name+'_nsb']=modern
    return trees,supplements,scout_variants,sorted(armor_roles)


def requirements(effects,rosters,contract):
    equipment=set();modules=set()
    for key,_,body in effects:
        if key=='create_equipment_variant':
            equipment.add(get(body,'type'));modules.update(v for _,_,v in get(body,'modules',[]) if v!='empty')
        elif key=='add_equipment_to_stockpile':equipment.add(get(body,'type'))
    for tree in rosters:equipment.update(equipment_nodes(tree))
    tech=set()
    for ident in equipment:
        if ident not in contract['equipment']:raise ValueError('Uncaptured equipment '+ident)
        found=contract['equipment'][ident]['technology']
        if found:tech.add(found)
        elif ident!='convoy_1':raise ValueError('Missing primary equipment unlock '+ident)
    for ident in modules:
        found=contract['modules'][ident]['technology']
        if found:tech.add(found)
        else:raise ValueError('Missing primary module unlock '+ident)
    return sorted(tech)


def stocks(tag,airtree):
    body=''
    for equipment,amount in [('infantry_equipment_1',3000),('support_equipment_1',300),('artillery_equipment_1',100),('anti_air_equipment_1',100),('motorized_equipment_1',400),('train_equipment_1',50)]:
        body+=block('add_equipment_to_stockpile',f'type = {equipment}\namount = {amount}\nproducer = {tag}')
    counts=Counter()
    for _,_,wings in get(airtree,'air_wings',[]):
        for equipment,_,details in wings:counts[(equipment,get(details,'version_name'))]+=int(get(details,'amount'))
    for (equipment,version),count in sorted(counts.items(),key=lambda n:str(n[0])):
        text=f'type = {equipment}\namount = {max(2,(count+9)//10)}\nproducer = {tag}\n'
        if version:text+='variant_name = '+version+'\n'
        body+=block('add_equipment_to_stockpile',text)
    return body


def compile_tag(tag,contract):
    filename=next((HERE/'baseline/countries').glob(tag+' - *.txt')).name
    original=read_source('countries',filename)
    # The original bookmark erroneously selected the designer navy in both arms.
    if tag=='OSE':original=original.replace('set_naval_oob = "OSE_navy_dlc"\n\t}', 'set_naval_oob = "OSE_navy_1991_legacy"\n\t}')
    else:original=original.replace('set_naval_oob = "'+tag+'_navy"','set_naval_oob = "'+tag+'_navy_1991_legacy"')
    # Earliest effective mod research unlocks cruiser armor2, not the obsolete1.
    original=original.replace('ship_armor_cruiser_1','ship_armor_cruiser_2')
    if tag=='OSE':
        original=re.sub(r'(name\s*=\s*"P-3 Orion"[^\n]*\n\s*type\s*=\s*)large_plane_airframe_0',
                        r'\1large_plane_maritime_patrol_plane_airframe_0',original)
    history=parse(original);trees,supplements,scouts,armor_roles=prepare_rosters(tag,parse(read_source('countries',filename)))
    supplement=block('if','limit = { NOT = { has_dlc = "Man the Guns" } }\n'+render(supplements)) if supplements else ''
    if scouts:supplement+=block('if','limit = { NOT = { has_dlc = "By Blood Alone" } }\n'+render(scouts))
    armor=''
    for role in armor_roles:
        recipe=ARMOR[role]
        armor+=block('create_equipment_variant',f'name = "{tag} {recipe["label"]}"\ntype = {recipe["modern"]}\n'+
                     block('modules','\n'.join(slot+' = '+module for slot,module in recipe['modules'].items())))
    supplement+=block('if','limit = { has_dlc = "No Step Back" }\n'+armor)
    stocks_common=stocks(tag,parse('air_wings = {}'))
    tail=block('if',f'limit = {{ NOT = {{ has_country_flag = {FLAG} }} }}\n'+stocks_common+
        block('if','limit = { has_dlc = "By Blood Alone" }\n'+stocks(tag,trees[tag+'_air_dlc']).replace(stocks_common,'')+
              block('else',stocks(tag,trees[tag+'_air']).replace(stocks_common,'')))+
        block('if','limit = { has_dlc = "No Step Back" }\n'+''.join(block('add_equipment_to_stockpile',
            f'type = {ARMOR[role]["modern"]}\namount = 100\nproducer = {tag}\nvariant_name = "{tag} {ARMOR[role]["label"]}"') for role in armor_roles)+
            block('else',''.join(block('add_equipment_to_stockpile',f'type = {role}\namount = 100\nproducer = {tag}') for role in armor_roles)))+
        f'set_country_flag = {FLAG}')
    original=re.sub(r'(?m)^(\s*)set_oob\s*=\s*"('+tag+r'_land(?:_vs_ai)?)"',
        lambda m:'\n'+m[1]+block('if','limit = { has_dlc = "No Step Back" }\n'+
        'set_oob = "'+m[2]+'_nsb"\n'+block('else','set_oob = "'+m[2]+'"')),original)
    # Guard each loader while leaving all original country and politics code intact.
    original=re.sub(r'(?m)^(\s*)((?:set_oob|set_air_oob|set_naval_oob)\s*=\s*"[^"]+")',
        lambda m:m[1]+f'if = {{ limit = {{ NOT = {{ has_country_flag = {FLAG} }} }} '+m[2]+' }',original)
    provisional=supplement+original+'\n# BEGIN LEGACY WORLD START STOCKS (new histories only)\n'+tail+'# END LEGACY WORLD START STOCKS\n'
    provisional_tree=parse(provisional)
    cases=[];techblocks=''
    for bba,mtg,nsb in [(b,m,n) for b,m in [(False,False),(True,False),(False,True),(True,True)] for n in (False,True)]:
        dlcs=({'By Blood Alone'} if bba else set())|({'Man the Guns'} if mtg else set())|({'No Step Back'} if nsb else set())
        effects=list(selected(provisional_tree,dlcs,tag));names=[v.strip('"') for k,_,v in effects if k in ('set_oob','set_air_oob','set_naval_oob')]
        required=requirements(effects,[trees[n] for n in names],contract)
        required=sorted(set(required)|{contract['equipment'][ARMOR[role]['modern'] if nsb else role]['technology'] for role in armor_roles})
        condition_text=('' if bba else 'NOT = { ')+'has_dlc = "By Blood Alone"'+('' if bba else ' }')+'\n'
        condition_text+=('' if mtg else 'NOT = { ')+'has_dlc = "Man the Guns"'+('' if mtg else ' }')
        condition_text+='\n'+('' if nsb else 'NOT = { ')+'has_dlc = "No Step Back"'+('' if nsb else ' }')
        techblocks+=block('if',block('limit',condition_text)+block('set_technology','\n'.join(t+' = 1' for t in required)))
        cases.append(dict(bba=bba,mtg=mtg,nsb=nsb,required_technology=required,rosters=names))
    payload='# Generated dependency prelude; mod provenance and provisional gameplay, not canonical forces.\n'+techblocks+'# END LEGACY DEPENDENCY PRELUDE\n'+provisional
    put('history/countries/'+filename,payload)
    for name,tree in trees.items():
        # Keep the unused divergent OSE legacy definition byte-for-byte retained.
        if name==tag+'_navy':
            if tag=='FAT':put('history/units/'+name+'.txt',read_source('units',name+'.txt'))
            continue
        if name==tag+'_navy_1991_legacy' or name.endswith('_nsb'):
            contract_note='original formations and experience retained' if name.endswith('_nsb') else 'original hull names retained'
            payload='# Generated compatibility projection; '+contract_note+'.\n'+render(tree)+'\n'
        else:
            payload=preserve_unmodified_blocks(read_source('units',name+'.txt'),tree)
        put('history/units/'+name+'.txt',payload)
    return cases


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--reference',type=Path);args=parser.parse_args()
    if args.reference:
        if args.check:raise SystemExit('Capture is a deliberate separate source update, not --check')
        capture(args.reference)
    put('common/technologies/ac_world_legacy_support.txt',TRANSPORT_TECH)
    put('localisation/english/ac_world_legacy_l_english.yml',
        '\ufeffl_english:\n ac_wl_transport_support:0 "Transport Aircraft Compatibility"\n'
        ' ac_wl_transport_support_desc:0 "A technical starting baseline for the inherited transport aircraft. Provisional compatibility calibration; no new aircraft or historical claim."\n')
    contract=json.loads((HERE/'primary_contract.json').read_text())
    results={tag:compile_tag(tag,contract) for tag in TAGS}
    OUTPUTS[HERE/'compiled_cases.json']=(json.dumps(results,indent=2)+'\n').encode()
    changed=[]
    for path,data in OUTPUTS.items():
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=data.replace(b'\r\n',b'\n'):changed.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if changed:raise SystemExit('Stale legacy outputs: '+', '.join(changed))
    print('Legacy generated outputs consistent' if args.check else 'Generated legacy repairs:',len(OUTPUTS))


if __name__=='__main__':main()
