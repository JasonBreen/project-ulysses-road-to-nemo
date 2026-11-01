"""Actual naval definitions, captured-primary replay and honest DLC boundaries."""
import argparse
import itertools
import json
from pathlib import Path
import sys
import hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion')]
from script import parse,get
from naval_content import YEARS,MTG,SHIPS,TECHS,tech_id,model_id,hull_id,recipe
from naval_primary import Primary,STATS

def digest(raw):return hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
def read(path):return parse(path.read_text(encoding='utf-8-sig'))
def technologies():return {k:v for k,_,v in get(read(MOD/'common/technologies/ac_naval_program.txt'),'technologies')}
def equipment():return {k:v for k,_,v in get(read(MOD/'common/units/equipment/zz_ac_naval_equipment.txt'),'equipments')}
def modules():return {k:v for k,_,v in get(read(MOD/'common/units/equipment/modules/zz_ac_naval_modules.txt'),'equipment_modules')}

def condition(nodes,day,tech,dlc,yards=20):
    result=[]
    for key,op,value in nodes:
        if key=='OR':answer=any(condition([v],day,tech,dlc,yards) for v in value)
        elif key=='AND':answer=condition(value,day,tech,dlc,yards)
        elif key=='NOT':answer=not condition(value,day,tech,dlc,yards)
        elif key=='has_tech':answer=value in tech
        elif key=='has_dlc':answer=value.strip('"') in dlc
        elif key=='always':answer=value=='yes'
        elif key=='date':
            right=tuple(map(int,value.strip('"').split('.')));answer={'<':day<right,'>':day>right,'=':day==right,'>=':day>=right,'<=':day<=right}[op]
        elif key=='num_of_naval_factories':answer={'>':yards>int(value),'<':yards<int(value),'=':yards==int(value)}[op]
        else:raise ValueError('Uninspected naval source trigger '+key)
        result.append(answer)
    return all(result)

def closure(year,dlc,tech,foundations):
    done=set(foundations);previous=None
    while previous!=done:
        previous=set(done)
        for ident,body in tech.items():
            if condition(get(body,'allow',[]),(year,1,1),done,dlc):done.add(ident)
    return done

def report(reference=None):
    facts=json.loads((HERE/'primary_contract.json').read_text());tech=technologies();gear=equipment();parts=modules();p=Primary.from_capture(facts['catalog'],gear,parts);errors=[];designs={}
    for source,expected in facts['source_sha256'].items():
        if source.startswith('mod/') or reference:
            base=MOD if source.startswith('mod/') else Path(reference)
            if digest((base/source.split('/',1)[1]).read_bytes())!=expected:errors.append('Stale effective primary source: '+source)
    if reference:
        for image in facts['layers'].values():
            if hashlib.sha256((Path(reference)/image['path']).read_bytes()).hexdigest()!=image['raw_sha256']:errors.append('Changed primary image metadata source: '+image['path'])
    for ident,body in gear.items():
        try:
            allowed=set(STATS)|{'year','active','is_buildable','priority','archetype','parent','type','picture','module_slots','can_be_produced','derived_variant_name','resources','default_modules','module_count_limit'}
            if {k for k,_,v in body}-allowed:raise ValueError('Uninspected owned naval field: '+str(sorted({k for k,_,v in body}-allowed)))
            designs[ident]=p.design(ident,complete=True)
            resolved=p.resolve(ident);parent=p.resolve(get(body,'parent'))
            if float(resolved['priority'])<=float(parent['priority']):errors.append('New naval priority does not exceed effective parent: '+ident)
            if get(body,'active')!='no':errors.append('Early active naval equipment: '+ident)
            # Whole recipe must be authored explicitly, including empty optional
            # slots, rather than silently inheriting old batteries/deck modules.
            if set(k for k,_,v in get(body,'default_modules',[]))!=set(designs[ident]['all_slots']):errors.append('Missing explicitly selected default coverage: '+ident)
        except (ValueError,KeyError) as ex:errors.append('Invalid actual naval definition '+ident+': '+str(ex))
    parity=[]
    for f in SHIPS:
        for year in YEARS:
            a=designs.get(model_id(f.id,year));b=designs.get(hull_id(f.id,year))
            if not a or not b:continue
            differences={k:[a['stats'][k],b['stats'][k]] for k in STATS if abs(a['stats'][k]-b['stats'][k])>1e-6}
            if differences or a['resources']!=b['resources'] or a['effective_types']!=b['effective_types']:errors.append('Naval default physical/classification parity mismatch: '+str((f.id,year)))
            role=f.equipment_type
            if role not in a['effective_types'] or (f.id=='fleet' and 'screen_ship' in a['effective_types']):errors.append('Wrong effective ship classification: '+f.id)
            parity.append(dict(family=f.id,year=year,stat_differences=differences,resources=a['resources'],effective_types=a['effective_types'],
                stats=a['stats'],external_module_crew=a['external_module_crew'],same_recipe=a['selected_modules']==b['selected_modules'],
                reference_threshold_margins=dict(sub_attack=a['stats']['sub_attack']-15,sub_detection=a['stats']['sub_detection']-2),native_mission_equivalence=False))
    cases=[]
    for year in (1991,2005,*YEARS):
        for mtg in (False,True):
            dlc={MTG} if mtg else set();done=closure(year,dlc,tech,facts['foundations']);enabled={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipments',[])}
            unlocked={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipment_modules',[])};selected=[]
            for f in SHIPS:
                for when in YEARS:
                    if when>year:continue
                    eligible=[i for i in (model_id(f.id,when),hull_id(f.id,when)) if i in enabled and condition(get(gear[i],'can_be_produced'),(year,1,1),done,dlc)]
                    if len(eligible)!=1:errors.append('Missing/duplicate paid naval route: '+str((year,mtg,f.id,when,eligible)))
                    for ident in eligible:
                        selected.append(ident)
                        if not set(recipe(f.id,when).values())<=unlocked:errors.append('Unresearched selected default: '+ident)
            cases.append(dict(year=year,mtg=mtg,research=sorted(set(tech)&done),eligible_models=selected,source_only=True))
    independent=[]
    for mtg,bba,nsb,lar in itertools.product((False,True),repeat=4):
        dlc={name for name,on in [(MTG,mtg),('By Blood Alone',bba),('No Step Back',nsb),('La Resistance',lar)] if on}
        done=closure(2020,dlc,tech,facts['foundations']);enabled={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipments',[])}
        selected=sorted(i for i,b in gear.items() if i in enabled and condition(get(b,'can_be_produced'),(2020,1,1),done,dlc))
        if len(selected)!=20:errors.append('Independent DLC source-route mismatch')
        independent.append(dict(mtg=mtg,bba=bba,nsb=nsb,lar=lar,models=selected))
    retained=[]
    for filename in ('naval.txt','MTG_naval.txt','MTG_naval_Support.txt'):
        path=MOD/'common/technologies'/filename;nodes=get(read(path),'technologies')
        retained.append(dict(source=path.relative_to(MOD).as_posix(),sha256=digest(path.read_bytes()),technologies=[dict(id=i,year=get(b,'start_year'),folder=get(get(b,'folder',[]),'name')) for i,_,b in nodes]))
    return dict(schema=1,reference_version=facts['reference_version'],native_acceptance=False,tech_count=len(tech),models=len(gear),modules=len(parts),
        cases=cases,independent_DLC_profiles=independent,default_physical_parity=parity,retained_surfaces=retained,errors=errors,
        limits=['Research closure is a source eligibility fixture, not elapsed research time or natural AI behavior.',
            'Bare hulls and explicit complete default recipes are composed exactly once on both routes; native default-module behavior and refit remain untested.',
            'Sonar/detection and depth-charge attack statistics are distinct. Source thresholds do not prove spotting, submarine reveal, escort effectiveness or delivered damage.',
            'MTG-disabled mining, optional mixed averaged batteries, modern carrier air groups, submarine-versus-submarine combat, guided missiles and nuclear/strategic ships are outside this slice.',
            'Carrier capacity is the native carrier_size coefficient times 10; no aircraft or hulls are granted and existing wing eligibility remains unchanged.',
            'Existing ship count/type fiscal proxies remain authoritative; no per-hull maintenance or mission telemetry is invented.',
            'All old naval tabs/IDs, 1991 fleets, variants and production queues remain intact; native 3D entities and older imagery remain presentation backlog.'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--reference',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args();value=report(a.reference)
    path=HERE/'capabilities.json';raw=(json.dumps(value,indent=2)+'\n').encode()
    if a.check:
        if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=raw:raise SystemExit('Stale naval capability worksheet')
    else:path.write_bytes(raw)
    print('NAVAL source: 12 date/MTG cases, 16 independent profiles;',len(value['errors']),'errors')
    for error in value['errors']:print(error)
    if value['errors']:raise SystemExit(1)
