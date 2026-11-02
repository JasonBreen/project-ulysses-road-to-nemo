"""Effective-primary land capability and physical production worksheet.

No research/production/mission behavior is emulated as native acceptance.
Refresh technical facts explicitly with --reference; ordinary checks are offline.
"""
import argparse
from collections import Counter
import hashlib
import json
import itertools
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/world_starts')]
from script import parse,get,walk
from technical import Engine
from land_content import YEARS,FAMILIES,TECHS,MODULES,model_id,chassis_id,module_id,recipe

STATS=('build_cost_ic','fuel_consumption','manpower','maximum_speed','reliability','defense','breakthrough','hardness','armor_value','soft_attack','hard_attack','ap_attack','air_attack')
PRIMARY_NOTES=(
 'common/units/equipment/infantry.txt','common/units/equipment/tank_chassis.txt','common/units/equipment/x_tank_chassis.txt',
 'common/units/equipment/modules/00_tank_modules.txt','common/technologies/support.txt','common/technologies/infantry.txt',
 'common/ai_equipment/_documentation.md','common/ai_equipment/generic_tank.txt','common/ai_templates/_documentation.md',
 'common/ai_strategy/default.txt','interface/countrytechtreeview.gui','interface/tank_modules_icons.gfx','interface/subuniticons.gfx','interface/texticons.gfx')


def digest(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def load(path):return parse(path.read_text(encoding='utf-8-sig'))
def new_techs():return {k:v for k,_,v in get(load(MOD/'common/technologies/ac_land_program.txt'),'technologies')}
def new_equipment():return {k:v for k,_,v in get(load(MOD/'common/units/equipment/zz_ac_land_equipment.txt'),'equipments')}
def new_modules():return {k:v for k,_,v in get(load(MOD/'common/units/equipment/modules/zz_ac_land_modules.txt'),'equipment_modules')}


def actual_stats(engine,ident,modules=()):
    body=engine.resolve(ident,engine.equipment,engine.eq_files)
    result={k:float(body.get(k,0)) for k in STATS};resources=Counter({k:float(v) for k,_,v in body.get('resources',[])})
    factor={k:float(v) for k,_,v in body.get('module_add_stats_multiplier',[])};multipliers=Counter()
    for module in modules:
        row=engine.resolve(module,engine.modules,engine.module_files)
        for k,_,v in row.get('add_stats',[]):
            if k in result:result[k]+=float(v)*(1+factor.get(k,0))
        for k,_,v in row.get('multiply_stats',[]):
            if k in result:multipliers[k]+=float(v)
        for k,_,v in row.get('add_resources',[])+row.get('build_cost_resources',[]):resources[k]+=float(v)
    result={k:round(v*(1+multipliers[k]),6) for k,v in result.items()}
    return dict(stats=result,resources=dict(resources))


def capture(reference):
    reference=Path(reference);engine=Engine(reference);techs=new_techs();equipment=new_equipment();modules=new_modules()
    facts=dict(schema=1,reference_version=json.loads((reference/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        scope='Primary technical syntax and equipment definitions; authored values are provisional gameplay, not official ACES specifications.',
        defines=engine.defines,equipment={},modules={},units={},existing_prerequisites={},default_designs={},optional_designs={})
    for ident,source in equipment.items():
        resolved=engine.resolve(ident,engine.equipment,engine.eq_files)
        parent=get(source,'parent');parent_values=engine.resolve(parent,engine.equipment,engine.eq_files) if parent else {}
        facts['equipment'][ident]=dict(archetype=resolved.get('archetype'),type=resolved.get('type'),year=resolved.get('year'),
            is_archetype=get(source,'is_archetype','no'),is_buildable=get(source,'is_buildable'),active=get(source,'active'),
            priority=resolved.get('priority'),parent=parent,parent_priority=parent_values.get('priority'),
            can_be_produced=resolved.get('can_be_produced'),technology=engine.equipment_tech(ident) if get(source,'is_archetype')!='yes' else None,
            **actual_stats(engine,ident))
    for ident in modules:
        resolved=engine.resolve(ident,engine.modules,engine.module_files)
        facts['modules'][ident]=dict(category=resolved.get('category'),technology=engine.module_tech(ident),
            add_stats=resolved.get('add_stats',[]),build_cost_resources=resolved.get('build_cost_resources',[]),
            allowed_module_categories=resolved.get('allowed_module_categories',[]),allow_equipment_type=resolved.get('allow_equipment_type'))
    for family in ('mbt','tracked_artillery'):
        for year in YEARS:
            ident=chassis_id(family,year);source=equipment[ident];defaults={k:v for k,_,v in get(source,'default_modules')}
            slots=engine.design_slots(ident,defaults)
            facts['default_designs'][ident]=dict(modules=defaults,slots=slots,**actual_stats(engine,ident,defaults.values()))
            optional={**defaults,'special_type_slot_1':module_id('optics',year),'special_type_slot_2':module_id('protected_radio',year)}
            facts['optional_designs'][ident]=dict(modules=optional,slots=engine.design_slots(ident,optional),**actual_stats(engine,ident,optional.values()),
                limitation='Additional optics/radio require their separate surveillance/electronic-support research; optional recipe is not the parity baseline.')
    for ident in ('ac_land_surveillance_company','ac_land_electronic_support_company','infantry','recon','mot_recon','signal_company','logistics_company','engineer','maintenance_company','modern_armor','medium_sp_artillery_brigade'):
        facts['units'][ident]=engine.unit(ident)
    for ident,body in techs.items():
        for prerequisite,_,_ in get(body,'dependencies',[]):
            if prerequisite in techs:continue
            if prerequisite not in engine.tech:raise ValueError('Unresolved existing foundation: '+prerequisite)
            engine.record(engine.tech_files[prerequisite]);facts['existing_prerequisites'][prerequisite]=engine.tech[prerequisite]
    for ident in ('infantry_equipment_3','mechanized_equipment_3','modern_tank_equipment_1','medium_tank_artillery_equipment_1','support_equipment_1','motorized_equipment_1'):
        facts['equipment'][ident]=dict(archetype=engine.resolve(ident,engine.equipment,engine.eq_files).get('archetype'),**actual_stats(engine,ident))
    # Inventory the still-reachable inherited surfaces precisely. Adding a new
    # dated page does not replace these older native/inherited technologies.
    land_folders=('infantry_folder','support_folder','armour_folder','artillery_folder','electronics_folder','nsb_armour_folder')
    facts['retained_land_surfaces']={}
    for folder in land_folders:
        rows=[]
        for ident,body in sorted(engine.tech.items()):
            if get(get(body,'folder',[]),'name')!=folder:continue
            path=engine.tech_files[ident];engine.record(path)
            rows.append(dict(id=ident,start_year=get(body,'start_year'),source=('mod/' if path.is_relative_to(MOD) else 'reference/')+path.relative_to(MOD if path.is_relative_to(MOD) else reference).as_posix(),
                disposition='Retained unchanged; pre-1950 date and inherited naming remain explicit conversion backlog' if float(get(body,'start_year',1991))<1950 else 'Retained unchanged; this additive packet does not replace it'))
        facts['retained_land_surfaces'][folder]=dict(available=folder!='nsb_armour_folder',technologies=rows,
            disposition='Hidden compatibility folder; fully commented NSB_armor.txt supplies no reachable old designer tree' if folder=='nsb_armour_folder' else 'Still reachable through the retained engine-bound tab; not retired by LAND')
    for relative in PRIMARY_NOTES:engine.record(reference/relative)
    # Effective category tags and source modifiers underpin UI and support effects.
    engine.record(MOD/'common/technology_tags/00_technology.txt')
    engine.record(MOD/'common/technologies/support.txt')
    facts['existing_support_technologies']={k:v for k,_,v in get(load(MOD/'common/technologies/support.txt'),'technologies') if isinstance(v,list)}
    facts['source_sha256']={name:digest(((MOD if name.startswith('mod/') else reference)/name.split('/',1)[1]).read_bytes()) for name in sorted(engine.used)}
    (HERE/'primary_contract.json').write_bytes((json.dumps(facts,indent=2)+'\n').encode('utf-8'))


def condition(nodes,day,research,dlc,stocks=None,mil=20):
    stocks=stocks or {};answers=[]
    for name,op,value in nodes:
        key=name.lower()
        if key=='date':
            point=tuple(map(int,value.strip('"').split('.')));answer=day>point if op=='>' else day<point
        elif key=='has_tech':answer=value in research
        elif key=='has_dlc':answer=value.strip('"') in dlc
        elif key in ('not','or','and'):
            options=[condition([node],day,research,dlc,stocks,mil) for node in value]
            answer=not all(options) if key=='not' else any(options) if key=='or' else all(options)
        elif key=='always':answer=value=='yes'
        elif key=='num_of_military_factories':answer=mil>float(value) if op=='>' else mil<float(value)
        elif key=='has_equipment':
            answer=all(stocks.get(item,0)>float(count) if sign=='>' else stocks.get(item,0)<float(count) for item,sign,count in value)
        else:raise ValueError('Uninspected land trigger: '+name)
        answers.append(answer)
    return all(answers)


def researched_by(year,techs,foundations):
    research=set(foundations);day=(year,1,1);changed=True
    while changed:
        changed=False
        for ident,body in techs.items():
            if ident not in research and condition(get(body,'allow',[]),day,research,set()):research.add(ident);changed=True
    return research


def report(reference=None):
    facts=json.loads((HERE/'primary_contract.json').read_text());techs=new_techs();equipment=new_equipment();modules=new_modules();errors=[]
    if reference:
        for name,expected in facts['source_sha256'].items():
            base=MOD if name.startswith('mod/') else Path(reference)
            if digest((base/name.split('/',1)[1]).read_bytes())!=expected:raise ValueError('Primary source changed: '+name)
    # Capture includes the generated equipment/module source; stale facts fail
    # even when no installed reference is present.
    for name,expected in facts['source_sha256'].items():
        if name.startswith('mod/') and digest((MOD/name.split('/',1)[1]).read_bytes())!=expected:errors.append('Stale effective mod fact: '+name)
    technologies=set(techs)|set(facts['existing_prerequisites'])
    for ident,body in techs.items():
        year=int(get(body,'start_year'));cost=float(get(body,'research_cost'))
        if year not in (2006,2010,2015,2020) or not 1<=cost<=4:errors.append('Invalid dated research commitment: '+ident)
        if get(get(body,'folder'),'name')!='ac_land_folder':errors.append('Unreachable folder binding: '+ident)
        for required,_,_ in get(body,'dependencies',[]):
            if required not in technologies:errors.append('Missing prerequisite: '+required)
        for child in [get(v,'leads_to_tech') for k,_,v in body if k=='path']:
            if child not in techs:errors.append('Missing research path: '+str(child))
        for model,_,_ in get(body,'enable_equipments',[]):
            if model not in equipment:errors.append('Missing manufactured equipment: '+model)
        for component,_,_ in get(body,'enable_equipment_modules',[]):
            if component not in modules:errors.append('Missing component: '+component)
    cases=[]
    for year in (1991,2005,2006,2010,2015,2020):
        research=researched_by(year,techs,facts['existing_prerequisites'])
        enabled={ident for tech in research if tech in techs for ident,_,_ in get(techs[tech],'enable_equipments',[])}
        enabled_modules={ident for tech in research if tech in techs for ident,_,_ in get(techs[tech],'enable_equipment_modules',[])}
        for nsb in (False,True):
            dlc={'No Step Back'} if nsb else set();families=[]
            for family in FAMILIES:
                for tier,when in enumerate(YEARS):
                    if when>year:continue
                    ids=[model_id(family.id,when)]+([chassis_id(family.id,when)] if family.id in ('mbt','tracked_artillery') else [])
                    eligible=[ident for ident in ids if ident in enabled and condition(get(equipment[ident],'can_be_produced',[]),(year,1,1),research,dlc)]
                    if len(eligible)!=1:errors.append('Ambiguous/missing DLC equipment route: '+str((family.id,when,nsb,eligible)));continue
                    ident=eligible[0];design=facts['default_designs'].get(ident);stats=design or facts['equipment'][ident]
                    if design and not set(design['modules'].values())<=enabled_modules:errors.append('Default design before component unlock: '+ident)
                    if stats['stats']['build_cost_ic']<=0 or any(v<0 for v in stats['resources'].values()):errors.append('Unfunded equipment: '+ident)
                    families.append(dict(family=family.id,year=when,equipment=ident,
                        route='Researched modular chassis; create a design before native production' if design else 'Complete equipment available for native production',
                        default_modules=design['modules'] if design else {},**{k:stats[k] for k in ('stats','resources')},
                        one_MIL_30day_reference_50percent_efficiency=round(30*facts['defines']['NProduction.BASE_FACTORY_SPEED_MIL']*.5/stats['stats']['build_cost_ic'],6)))
            cases.append(dict(year=year,nsb=nsb,research=sorted(research-set(facts['existing_prerequisites'])),equipment=families))
    parity=[]
    for family in ('mbt','tracked_artillery'):
        for year in YEARS:
            legacy=facts['equipment'][model_id(family,year)];design=facts['default_designs'][chassis_id(family,year)]
            differences={k:round(design['stats'][k]-legacy['stats'][k],6) for k in STATS if abs(design['stats'][k]-legacy['stats'][k])>1e-6}
            if differences or design['resources']!=legacy['resources']:errors.append('Default physical-route parity mismatch: '+str((family,year,differences)))
            parity.append(dict(family=family,year=year,stats_differences=differences,resources_equal=design['resources']==legacy['resources']))
    company_costs=[]
    for ident in ('ac_land_surveillance_company','ac_land_electronic_support_company'):
        unit=facts['units'][ident]
        for year in YEARS:
            needs={k:float(v) for k,_,v in unit['need']};cost=0;inputs=Counter()
            for archetype,amount in needs.items():
                model=(model_id('surveillance',year) if archetype=='ac_land_sensor_equipment' else
                       model_id('electronic_support',year) if archetype=='ac_land_electronic_equipment' else
                       model_id('support',year) if archetype=='support_equipment' else model_id('logistics',year))
                gear=facts['equipment'][model];cost+=gear['stats']['build_cost_ic']*amount
                inputs.update({r:v*amount for r,v in gear['resources'].items()})
            company_costs.append(dict(unit=ident,year=year,needs=needs,manpower=float(unit['manpower']),
                manufacturing_IC_reference=round(cost,4),material_weight_reference=dict(inputs),
                note='Material weight is equipment-count times per-line resource coefficients for comparing packages; actual resources are continuous per assigned factory, not consumed per vehicle.'))
    independent=[]
    research=researched_by(2020,techs,facts['existing_prerequisites'])
    for flags in itertools.product((False,True),repeat=4):
        names=('No Step Back','By Blood Alone','Man the Guns','La Resistance');dlc={name for name,value in zip(names,flags) if value}
        eligible=sorted(ident for ident,body in equipment.items() if get(body,'is_archetype')!='yes' and condition(get(body,'can_be_produced',[]),(2020,1,1),research,dlc))
        independent.append(dict(dlc=dict(zip(names,flags)),eligible_2020_models=eligible,source_only=True))
        if len(eligible)!=32:errors.append('Independent DLC combination lacks one route per dated family: '+str(flags))
    return dict(schema=1,source_layer='Provisional gameplay, effective native technical syntax and offline arithmetic',
        native_acceptance=False,reference_version=facts['reference_version'],tech_count=len(techs),
        equipment_models=sum(get(v,'is_archetype')!='yes' for v in equipment.values()),module_count=len(modules),
        cases=cases,independent_DLC_profiles=independent,default_route_parity=parity,optional_modular_designs=facts['optional_designs'],supplied_company_packages=company_costs,
        retained_land_surfaces=facts['retained_land_surfaces'],errors=errors,
        limits=['Research creates unlocks, never stockpiles, divisions, factories, borders, wars or calendar reinitialization.',
            'Designer/legacy parity is an explicit default recipe and source-stat comparison, not native designer operation or every optional configuration.',
            'Existing1991 equipment, 3D models, attachments and other legacy presentation remain separate backlog.',
            'Air/naval weapons, strategic projects, agencies, operational air jamming and map-wide intelligence are outside this land packet.',
            'Research/production AI is source-authored; natural selection, XP use, queue retention, deployed upgrade behavior and pacing remain native acceptance.',
            'Research search has no existing/native reference binding; new folder retains real native scrolling and inherited keyboard controls.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.reference and not args.check:capture(args.reference)
    value=report(args.reference);text=json.dumps(value,indent=2)+'\n';path=HERE/'capabilities.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Land capability worksheet stale')
    else:path.write_bytes(text.encode('utf-8'))
    print('Land source capability audit:',len(value['cases']),'date/DLC profiles;',len(value['errors']),'errors')
    for error in value['errors']:print(error)
    if value['errors']:raise SystemExit(1)
