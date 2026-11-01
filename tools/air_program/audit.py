"""Captured primary aviation contracts and explicit DLC capability boundaries."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
from air_primary import Primary,STATS,tokens
from air_content import YEARS,FAMILIES,AIRCRAFT,FAMILY,TECHS,MODULES,BBA,LAR,tech_id,model_id,frame_id,recipe,common_dependencies
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get,walk

NOTES=('common/units/equipment/plane_airframes.txt','common/units/equipment/x_plane_airframes.txt','common/units/equipment/quad_engine_airframe.txt',
       'common/units/equipment/modules/00_plane_modules.txt','interface/equipmentdesigner/planes/plane_blueprints_generic.gui','interface/plane_modules_icons.gfx',
       'common/ai_equipment/_documentation.md','common/ai_equipment/generic_planes.txt','common/ai_strategy/default.txt','documentation/dynamic_variables_documentation.md')


def digest(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def tree(path):return parse(path.read_text(encoding='utf-8-sig'))
def technologies():return {k:v for k,_,v in get(tree(MOD/'common/technologies/ac_air_program.txt'),'technologies')}
def equipment():return {k:v for k,_,v in get(tree(MOD/'common/units/equipment/zz_ac_air_equipment.txt'),'equipments')}
def modules():return {k:v for k,_,v in get(tree(MOD/'common/units/equipment/modules/zz_ac_air_modules.txt'),'equipment_modules')}


def capture(reference):
    reference=Path(reference);p=Primary(reference);tech=technologies();gear=equipment();parts=modules()
    facts=dict(schema=1,reference_version=json.loads((reference/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        coverage='Effective loose-file equipment/GUI/AI contracts and provisional gameplay statistics; no native engine or DLC activation evidence',
        equipment={},modules={},designs={},foundations={},native_predecessors={},native_duplicate_roles={})
    for ident,source in gear.items():
        body=p.resolve(ident);parent=get(source,'parent');old=p.resolve(parent) if parent else {}
        facts['equipment'][ident]=dict(archetype=body.get('archetype'),equipment_type=body.get('type'),priority=body.get('priority'),
            parent=parent,parent_priority=old.get('priority'),active=get(source,'active'),is_buildable=get(source,'is_buildable'),
            air_map_icon_frame=body.get('air_map_icon_frame'),interface_overview_category_index=body.get('interface_overview_category_index'),
            interface_category=body.get('interface_category'),group_by=body.get('group_by'),sprite=body.get('sprite'),
            **p.stats(ident))
    for ident in parts:facts['modules'][ident]=p.resolve(ident,'modules')
    for family in AIRCRAFT:
        facts['native_predecessors'][family.id]=dict(id=family.parent,**p.stats(family.parent))
        for year in YEARS:
            if not family.airframe_parent:continue
            ident=frame_id(family.id,year);selected=recipe(family.id,year)
            facts['designs'][ident]=dict(modules=selected,contract=p.design(ident,selected),**p.stats(ident,selected))
    required={'radio','basic_machine_tools','electronic_mechanical_engineering','photo_reconnaisance'}
    required.update(v for f in AIRCRAFT for v in (f.legacy_foundation,f.designer_foundation) if v)
    for ident in sorted(required):
        if ident not in p.tech:raise ValueError('Missing inherited aviation foundation '+ident)
        p.record(p.files[('technologies',ident)]);facts['foundations'][ident]=p.tech[ident]
    for ident in ('small_plane_cas_airframe_1','small_plane_naval_bomber_airframe_1','medium_plane_scout_plane_airframe_4'):
        body=p.resolve(ident);facts['native_duplicate_roles'][ident]={k:body.get(k) for k in ('type','archetype','air_superiority','air_map_icon_frame','forbid_mission_type')}
    # A vocabulary extracted from primary/effective pre-existing declarations,
    # never from our own new definitions, cannot bless a misspelled new token.
    vocabulary=set()
    for definitions,section in ((p.equipment,'equipments'),(p.modules,'equipment_modules')):
        for ident,body in definitions.items():
            if ident.startswith('ac_air_'):continue
            source=p.files[(section,ident)]
            if source.is_relative_to(MOD):continue
            for key,_,value in body:
                if key in ('allow_mission_type','forbid_mission_type'):vocabulary.update(tokens(value));p.record(source)
    facts['native_mission_vocabulary']=sorted(vocabulary)
    for path in NOTES:p.record(reference/path)
    blueprints=tree(reference/'interface/equipmentdesigner/planes/plane_blueprints_generic.gui')
    parents={f.airframe_parent for f in AIRCRAFT if f.airframe_parent}
    facts['designer_blueprint_controls']={}
    for parent in sorted(parents):
        body=next(v for _,v in walk(blueprints) if get(v,'name')=='"equipment_designer_'+parent+'"')
        facts['designer_blueprint_controls'][parent]=dict(size=get(body,'size'),required_image_control='equipment_image_overlay',
            image_control=next(v for _,v in walk([['window','=',body]]) if get(v,'name')=='"equipment_image_overlay"'))
    facts['transport_owner']=dict(hidden_starting_bridge='ac_wl_transport_support',source='common/technologies/ac_world_legacy_support.txt',
        disposition='Retained without changes; new public transport research does not require this history-only grant',
        native_archetype='transport_plane_equipment',route='One complete-aircraft route with or without BBA; no invented modular transport chassis')
    facts['replay_catalog']=dict(equipment={k:p.equipment[k] for k in sorted(p.used['equipment']) if k in p.equipment},
        modules={k:p.modules[k] for k in sorted(p.used['modules']) if k in p.modules},
        duplicates={k:p.duplicates[k] for k in sorted(p.used['equipment']) if k in p.duplicates})
    facts['source_sha256']=dict(sorted(p.sources.items()))
    (HERE/'primary_contract.json').write_bytes((json.dumps(facts,indent=2)+'\n').encode())


def condition(nodes,day,research,dlc,stocks=None,mil=30):
    stocks=stocks or {};answers=[]
    for key,op,value in nodes:
        lower=key.lower()
        if lower=='date':
            point=tuple(map(int,value.strip('"').split('.')));answer=day>point if op=='>' else day<point if op=='<' else day==point
        elif lower=='has_tech':answer=value in research
        elif lower=='has_dlc':answer=value.strip('"') in dlc
        elif lower in ('not','or','and'):
            tests=[condition([node],day,research,dlc,stocks,mil) for node in value]
            answer=not all(tests) if lower=='not' else any(tests) if lower=='or' else all(tests)
        elif lower=='always':answer=value=='yes'
        elif lower=='num_of_military_factories':answer=mil>int(value) if op=='>' else mil<int(value)
        elif lower=='has_equipment':answer=all(stocks.get(k,0)<float(v) if sign=='<' else stocks.get(k,0)>float(v) for k,sign,v in value)
        else:raise ValueError('Uninspected aviation trigger: '+key)
        answers.append(answer)
    return all(answers)


def closure(year,dlc,tech,foundations):
    done=set(foundations);changed=True
    while changed:
        changed=False
        for ident,body in tech.items():
            if ident not in done and condition(get(body,'allow',[]),(year,1,1),done,dlc):done.add(ident);changed=True
    return done


def report(reference=None):
    facts=json.loads((HERE/'primary_contract.json').read_text());tech=technologies();gear=equipment();parts=modules();errors=[]
    for name,expected in facts['source_sha256'].items():
        if name.startswith('mod/') or reference:
            base=MOD if name.startswith('mod/') else Path(reference)
            if digest((base/name.split('/',1)[1]).read_bytes())!=expected:errors.append('Stale effective primary source: '+name)
    replay=Primary.from_capture(facts['replay_catalog'],gear,parts)
    for ident in gear:
        try:
            actual=replay.stats(ident)
            if get(gear[ident],'is_buildable')=='yes' and (not actual['resources'] or any(v<=0 for v in actual['resources'].values())):errors.append('Non-positive complete aircraft material requirement: '+ident)
            if actual['stats']!=facts['equipment'][ident]['stats'] or actual['resources']!=facts['equipment'][ident]['resources']:errors.append('Current equipment differs from captured effective contract: '+ident)
            if ident in facts['designs']:
                selected=facts['designs'][ident]['modules'];replay.design(ident,selected)
                if replay.stats(ident,selected)!= {k:facts['designs'][ident][k] for k in ('stats','resources','declared_missions','forbidden_missions','average_contributors')}:errors.append('Current design differs from captured effective contract: '+ident)
        except (ValueError,KeyError) as error:errors.append('Invalid actual aviation definition '+ident+': '+str(error))
    for ident,body in tech.items():
        year=int(get(body,'start_year'));required={k for k,_,_ in get(body,'dependencies',[])}
        if year not in YEARS or float(get(body,'research_cost'))<=0:errors.append('Invalid dated research commitment: '+ident)
        if not required<=set(tech)|set(facts['foundations']):errors.append('Missing dependency: '+ident)
        if get(get(body,'folder'),'name')!='ac_air_folder':errors.append('Unbound aviation folder: '+ident)
        if not {k for k,_,_ in get(body,'enable_equipments',[])}<=set(gear):errors.append('Missing physical equipment unlock: '+ident)
        if not {k for k,_,_ in get(body,'enable_equipment_modules',[])}<=set(parts):errors.append('Missing manufactured component: '+ident)
    parity=[]
    for family in AIRCRAFT:
        for year in YEARS:
            ident=model_id(family.id,year);row=facts['equipment'][ident]
            if row['is_buildable']!='yes' or row['active']!='no' or float(row['priority'])<=float(row['parent_priority'] or 0):errors.append('Invalid complete model availability/priority: '+ident)
            if row['stats']['build_cost_ic']<=0 or row['stats']['fuel_consumption']<=0 or row['stats']['manpower']<=0:errors.append('Unfunded model: '+ident)
            if not row['resources'] or any(v<=0 for v in row['resources'].values()):errors.append('Non-positive captured aircraft material requirement: '+ident)
            if not set(family.missions)<=set(row['declared_missions']):errors.append('Missing expected source mission: '+ident)
            if not set(row['declared_missions']+row['forbidden_missions'])<=set(facts['native_mission_vocabulary']):errors.append('Unknown mission token: '+ident)
            if not family.airframe_parent:continue
            frame=frame_id(family.id,year);design=facts['designs'][frame];body=facts['equipment'][frame]
            if body['is_buildable']!='no' or body['active']!='no' or float(body['priority'])<=float(body['parent_priority'] or 0):errors.append('Invalid designer chassis availability/priority: '+frame)
            differences={k:[row['stats'][k],design['stats'][k]] for k in STATS if abs(row['stats'][k]-design['stats'][k])>1e-6}
            if differences or row['resources']!=design['resources']:errors.append('Default physical recipe parity mismatch: '+frame)
            if design['stats']['thrust']<design['stats']['weight'] or design['stats']['thrust']<=0:errors.append('Insufficient default thrust: '+frame)
            if not set(family.missions)<=set(design['declared_missions']):errors.append('Missing default source mission: '+frame)
            parity.append(dict(family=family.id,year=year,stats_differences=differences,resources_equal=row['resources']==design['resources'],
                legacy_missions=row['declared_missions'],designer_default_missions=design['declared_missions'],
                shared_source_missions=sorted(set(row['declared_missions'])&set(design['declared_missions'])),
                legacy_only_source_missions=sorted(set(row['declared_missions'])-set(design['declared_missions'])),
                native_mission_equivalence=False))
    cases=[]
    for year in (1991,2005,*YEARS):
        for bba,lar in itertools.product((False,True),repeat=2):
            dlc=({BBA} if bba else set())|({LAR} if lar else set());done=closure(year,dlc,tech,facts['foundations'])
            enabled={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipments',[])}
            unlocked_modules={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipment_modules',[])}
            selected=[]
            for family in AIRCRAFT:
                for when in YEARS:
                    if when>year:continue
                    candidates=[model_id(family.id,when)]+([frame_id(family.id,when)] if family.airframe_parent else [])
                    eligible=[i for i in candidates if i in enabled and condition(get(gear[i],'can_be_produced',[]),(year,1,1),done,dlc)]
                    expected=0 if family.id=='surveillance' and not lar else 1
                    if len(eligible)!=expected:errors.append('Missing/ambiguous paid route: '+str((year,bba,lar,family.id,when,eligible)))
                    for ident in eligible:
                        design=facts['designs'].get(ident);row=design or facts['equipment'][ident]
                        if design and not set(design['modules'].values())<=unlocked_modules:errors.append('Unresearched default component: '+ident)
                        selected.append(dict(family=family.id,year=when,id=ident,route='Researched modular design; native XP/design/production still required' if design else 'Complete manufactured aircraft',
                            stats=row['stats'],resources=row['resources'],declared_source_missions=row['declared_missions']))
            cases.append(dict(year=year,bba=bba,lar=lar,research=sorted(set(tech)&done),eligible_models=selected,
                surveillance='LaR-gated equipment/research route; native mission untested' if lar else 'Unavailable; no mission-equivalence fallback is invented'))
    independent=[]
    for bba,lar,mtg,nsb in itertools.product((False,True),repeat=4):
        dlc={name for name,on in [(BBA,bba),(LAR,lar),('Man the Guns',mtg),('No Step Back',nsb)] if on}
        done=closure(2020,dlc,tech,facts['foundations']);enabled={k for t in done if t in tech for k,_,_ in get(tech[t],'enable_equipments',[])}
        models=sorted(i for i,b in gear.items() if i in enabled and condition(get(b,'can_be_produced',[]),(2020,1,1),done,dlc))
        if len(models)!=(20 if lar else 16):errors.append('Independent DLC source-route count mismatch')
        independent.append(dict(bba=bba,lar=lar,mtg=mtg,nsb=nsb,eligible_2020_models=models,source_only=True))
    retained=[]
    for filename in ('air_techs.txt','bba_air_techs.txt'):
        source=MOD/'common/technologies'/filename
        rows=[dict(id=ident,start_year=get(body,'start_year'),folder=get(get(body,'folder',[]),'name')) for ident,_,body in get(tree(source),'technologies',[])]
        retained.append(dict(source=source.relative_to(MOD).as_posix(),source_sha256=digest(source.read_bytes()),technologies=rows,
            disposition='Retained with original IDs, equipment unlocks and labels; date relabelling alone is not a completed hardware/presentation conversion.'))
    return dict(schema=1,reference_version=facts['reference_version'],native_acceptance=False,tech_count=len(tech),model_count=len(gear),module_count=len(parts),
        cases=cases,independent_DLC_profiles=independent,default_physical_parity=parity,errors=errors,
        retained_aviation_surfaces=retained,
        limitations=['Immediate research closure is a source eligibility fixture, not elapsed research time or natural AI progression.',
            'Legacy maritime predecessors retain mining declarations. Bare BBA attack designs do not provide equivalent mine equipment; no universal mission parity is claimed.',
            'LaR-disabled reconnaissance remains an explicit capability gap, including inherited 1991 specialist wings. This packet makes no retroactive grants or mission workaround.',
            'Declared recon/naval-patrol/air-supply/paradrop/logistics mission tokens do not prove hardcoded DLC availability, active missions or delivered effects.',
            'Default source statistics use one contributor per averaged weapon stat. Mixed optional averaged configurations require native aggregation acceptance.',
            'Airborne early warning, air-to-air refueling, ASW attacks, strategic bombing, stealth, carrier aviation, helicopters, drones, missiles and 3D entities remain outside this conventional slice.',
            'The existing broad upkeep owner bills deployed-aircraft base plus one maximum role-premium pool. No per-wing telemetry or new fiscal model is introduced.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.reference and not args.check:capture(args.reference)
    result=report(args.reference);raw=(json.dumps(result,indent=2)+'\n').encode();path=HERE/'capabilities.json'
    if args.check:
        if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=raw:raise SystemExit('Stale aviation capability worksheet')
    else:path.write_bytes(raw)
    print('Aviation source capability:',len(result['cases']),'date/core-DLC cases,16independent DLC profiles;',len(result['errors']),'errors')
    for error in result['errors']:print(error)
    if result['errors']:raise SystemExit(1)
