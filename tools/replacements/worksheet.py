"""Actual six-country replacement inputs and bounded offline fuel sensitivities.

--reference deliberately refreshes cached technical facts. Ordinary --check
requires no installed game and never changes another component's receipts.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/world_starts')]
from script import parse,get,walk
from inventory import selected,condition
from technical import Engine
from policies import capture as capture_policies,history_signature,KEYS

TAGS=('EMM','EVA','SNS','AMB','UGE','DEL')
MATRIX=[(b,m,n) for b in (False,True) for m in (False,True) for n in (False,True)]
NAVAL={'convoy_1','destroyer_2','submarine_2','light_cruiser_2'}


def digest(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def json_digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(path):return parse(path.read_text(encoding='utf-8-sig'))
def history(tag):return next((MOD/'history/countries').glob(tag+' - *.txt'))
def dlcs(b,m,n):return {name for name,on in zip(('By Blood Alone','Man the Guns','No Step Back'),(b,m,n)) if on}
def key(equipment,modules):return equipment+':'+json_digest(modules)
def is_naval(equipment):return equipment in NAVAL or equipment.startswith('ship_hull_')


def selected_sources(tag,b,m,n):
    effects=list(selected(load(history(tag)),dlcs(b,m,n),tag))
    rosters={value.strip('"'):load(MOD/'history/units'/(value.strip('"')+'.txt'))
             for kind,_,value in effects if kind in ('set_oob','set_air_oob','set_naval_oob')}
    return effects,rosters


def capture(reference):
    engine=Engine(reference);recipes={};unit_rows={};gear={};policies={};techs={};research={}
    def recipe(equipment,modules=None):
        modules=modules or {};ident=key(equipment,modules)
        if ident not in recipes:
            recipes[ident]=dict(equipment=equipment,modules=modules,stats=engine.stats(equipment,modules.values()),
                archetype=engine.resolve(equipment,engine.equipment,engine.eq_files)['archetype'],
                can_be_produced=engine.resolve(equipment,engine.equipment,engine.eq_files).get('can_be_produced'),
                equipment_technology=engine.equipment_tech(equipment),
                module_technologies={module:engine.module_tech(module) for module in modules.values()},
                slots=engine.design_slots(equipment,modules) if modules else {})
        return recipes[ident]
    for tag in TAGS:
        source=history(tag).read_text(encoding='utf-8-sig')
        for b,m,n in MATRIX:
            effects,rosters=selected_sources(tag,b,m,n);variants={};enabled=set()
            policies[tag]=capture_policies(source,tag,engine,dlcs(b,m,n))
            for kind,_,body in effects:
                if kind=='set_technology':
                    for ident,_,value in body:
                        if value=='1':enabled.add(ident)
                        elif value=='0':enabled.discard(ident)
                elif kind=='create_equipment_variant':
                    modules={slot:module for slot,_,module in get(body,'modules',[]) if module!='empty'}
                    variants[(get(body,'type'),get(body,'name'))]=modules;recipe(get(body,'type'),modules)
                elif kind=='add_equipment_to_stockpile':
                    equipment=get(body,'type');version=get(body,'variant_name')
                    row=recipe(equipment,variants[(equipment,version)] if version else {})
                    gear[row['archetype']]=equipment
            mods=Counter()
            for ident in sorted(enabled):
                if ident not in engine.tech:raise ValueError('Unresolved selected technology: '+tag+':'+ident)
                engine.record(engine.tech_files[ident]);mods.update({k:float(v) for k,_,v in engine.tech[ident] if k in KEYS})
            techs[tag+':'+str((b,m,n))]=dict(mods)
            research[tag+':'+str((b,m,n))]=sorted(enabled)
            for tree in rosters.values():
                for kind,body in walk(tree):
                    if kind=='division_template':
                        for unit,_,_ in get(body,'regiments',[])+get(body,'support',[]):
                            resolved=engine.unit(unit)
                            unit_rows[unit]={k:resolved[k] for k in ('need','fuel_consumption','supply_consumption','manpower') if k in resolved}
                    elif kind=='ship':
                        equipment,_,details=get(body,'equipment')[0];version=get(details,'version_name')
                        recipe(equipment,variants[(equipment,version)] if version else {})
                    elif kind=='add_equipment_production':
                        details=get(body,'equipment');equipment=get(details,'type');version=get(details,'version_name')
                        row=recipe(equipment,variants[(equipment,version)] if version else {})
                        gear.setdefault(row['archetype'],equipment)
                for _,_,wings in get(tree,'air_wings',[]):
                    for equipment,_,details in wings:
                        version=get(details,'version_name');recipe(equipment,variants[(equipment,version)] if version else {})
    resources,files=engine.catalog('common/resources','resources');terms={}
    for resource,body in resources.items():
        engine.record(files[resource]);terms[resource]={k:float(get(body,k)) for k in ('cic','convoys')}
    facts={'schema':1,'reference_version':json.loads((Path(reference)/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        'classification':'Effective technical source capture; no engine loading or native behavior acceptance',
        'defines':engine.defines,'recipes':recipes,'units':unit_rows,'gear_by_archetype':gear,
        'policies':policies,'economic_technology_modifiers':techs,'selected_technology':research,'trade_terms':terms}
    facts['sources']={name:digest(((MOD if name.startswith('mod/') else Path(reference))/name.split('/',1)[1]).read_bytes()) for name in sorted(engine.used)}
    (HERE/'primary_contract.json').write_text(json.dumps(facts,indent=2)+'\n',encoding='utf-8',newline='\n')


def states_by_country():
    result={tag:[] for tag in TAGS}
    for path in sorted((MOD/'history/states').glob('*.txt')):
        state=get(load(path),'state');hist=get(state,'history');tag=get(hist,'owner')
        if tag not in result:continue
        result[tag].append((path,state,hist,get(hist,'buildings',[])))
    return result


def scenario(lines,recipes,retained,capacity,policy,tech,contract):
    inputs=Counter();rates={};defines=contract['defines']
    for line in lines:
        row=recipes[line['recipe']];stats=row['stats'];amount=line['factories'];naval=is_naval(row['equipment'])
        inputs.update({r:amount*v for r,v in stats['resources'].items()})
        field='industrial_capacity_dockyard' if naval else 'industrial_capacity_factory'
        factor=max(0,1+min(0,policy.get(field,0)+tech.get(field,0)))
        speed=defines['NProduction.BASE_FACTORY_SPEED_NAV' if naval else 'NProduction.BASE_FACTORY_SPEED_MIL']
        rates[row['equipment']]=rates.get(row['equipment'],0)+30*speed*amount*(1 if naval else .5)*factor/stats['build_cost_ic']
    deficits={r:max(0,v-retained.get(r,0)) for r,v in sorted(inputs.items())}
    cg=max(0,policy.get('consumer_goods_expected_value',0)*(1+policy.get('consumer_goods_factor',0)))
    available=max(0,capacity['civilian']-math.ceil((capacity['civilian']+capacity['military'])*cg))
    import_civ=sum(math.ceil(v*contract['trade_terms'][r]['cic']) for r,v in deficits.items() if v)
    return dict(resource_inputs=dict(inputs),domestic_margins={r:retained.get(r,0)-v for r,v in inputs.items()},
        industrial_import_deficits=deficits,industrial_import_CIV_rounded_per_resource=import_civ,
        CIV_after_rounded_consumer_goods=available,industrial_import_CIV_margin=available-import_civ,
        industrial_import_convoys_reference=sum(math.ceil(v*contract['trade_terms'][r]['convoys']) for r,v in deficits.items() if v),
        thirty_day_replacement_reference_50percent_MIL_no_positive_output_bonus={r:round(v,4) for r,v in rates.items()})


def case(tag,b,m,n,contract,states):
    effects,rosters=selected_sources(tag,b,m,n);enabled=set();variants={};stocks=Counter();deployed=Counter();lines=[];errors=[]
    policy=contract['policies'][tag]['modifiers'];negative=contract['policies'][tag]['negative_modifiers']
    tech=contract['economic_technology_modifiers'][tag+':'+str((b,m,n))]
    def recipe(equipment,version=None):
        if version and (equipment,version) not in variants:raise ValueError('Variant before definition: '+equipment+':'+version)
        ident=key(equipment,variants.get((equipment,version),{}));row=contract['recipes'].get(ident)
        if row is None:raise ValueError('Uncaptured selected recipe: '+equipment+':'+str(version))
        needed={row['equipment_technology'],*row['module_technologies'].values()}-{None}
        if not needed<=enabled:raise ValueError('Recipe before technology: '+equipment+':'+str(sorted(needed-enabled)))
        availability=row.get('can_be_produced')
        if isinstance(availability,list):
            ideas={v['idea'] for v in contract['policies'][tag]['active_ideas']}
            def predicates(nodes):
                result=[]
                for k,op,v in nodes:
                    if k in ('has_idea','has_tech'):
                        result.append(['always','=', 'yes' if v in (ideas if k=='has_idea' else enabled) else 'no'])
                    else:result.append([k,op,predicates(v) if isinstance(v,list) else v])
                return result
            if not condition(predicates(list(selected(availability,dlcs(b,m,n),tag))),dlcs(b,m,n),tag,()):
                raise ValueError('Selected recipe fails actual production gate: '+equipment)
        elif availability=='no':raise ValueError('Selected equipment not producible: '+equipment)
        return ident,row
    for kind,_,body in effects:
        if kind=='set_technology':enabled.update(k for k,_,v in body if v=='1')
        elif kind=='create_equipment_variant':
            equipment=get(body,'type');version=get(body,'name')
            variants[(equipment,version)]={slot:module for slot,_,module in get(body,'modules',[]) if module!='empty'}
            recipe(equipment,version)
        elif kind=='add_equipment_to_stockpile':
            equipment=get(body,'type');ident,row=recipe(equipment,get(body,'variant_name'));stocks[ident]+=int(get(body,'amount'))
        elif kind in ('set_oob','set_air_oob','set_naval_oob'):
            tree=rosters[body.strip('"')]
            for node,details in walk(tree):
                if node=='add_equipment_production':
                    eq=get(details,'equipment');ident,row=recipe(get(eq,'type'),get(eq,'version_name'))
                    count=int(get(details,'requested_factories'));assert count>0,'Zero-capacity line'
                    lines.append(dict(recipe=ident,equipment=row['equipment'],factories=count))
                elif node=='ship':
                    equipment,_,eq=get(details,'equipment')[0];ident,_=recipe(equipment,get(eq,'version_name'));deployed[ident]+=1
            for _,_,wings in get(tree,'air_wings',[]):
                for equipment,_,eq in wings:
                    ident,_=recipe(equipment,get(eq,'version_name'));deployed[ident]+=int(get(eq,'amount'))
    if sorted(enabled)!=contract['selected_technology'][tag+':'+str((b,m,n))]:errors.append('Selected research changed; recapture economic modifiers')
    if history_signature(history(tag).read_text(encoding='utf-8-sig'),tag,dlcs(b,m,n))!=contract['policies'][tag]['history_policy_signature']:
        errors.append('Opening policies changed; recapture actual modifiers')
    fielded={contract['recipes'][ident]['equipment'] for ident in deployed}
    missing=fielded-{v['equipment'] for v in lines}
    allowed=set()
    if tag in ('SNS','AMB'):allowed.add('ship_hull_submarine_2' if m else 'submarine_2')
    if tag in ('UGE','DEL'):allowed.add('ship_hull_light_2' if m else 'destroyer_2')
    if tag=='AMB':allowed.add('small_plane_airframe_1' if b else 'fighter_equipment_1')
    if missing!=allowed:errors.append('Deployed replacement role gap differs from approved manual rotations: '+str(sorted(missing^allowed)))
    capacity=Counter();retained=Counter();source_hashes={};infra=contract['defines']['NBuildings.INFRASTRUCTURE_RESOURCE_BONUS']
    retention=max(0,1-policy.get('min_export',.5))
    extraction=max(0,1+sum(negative.get(k,0) for k in ('local_resources_factor','resources_factor','resource_gain_efficiency')))
    for path,state,hist,buildings in states:
        source_hashes[path.relative_to(ROOT).as_posix()]=digest(path.read_bytes())
        if tag not in [v for k,_,v in hist if k=='add_core_of']:continue
        for role,field in [('civilian','industrial_complex'),('military','arms_factory'),('dockyard','dockyard')]:
            capacity[role]+=int(get(buildings,field,'0'))
        for resource,_,value in get(state,'resources',[]):
            retained[resource]+=math.floor(math.floor(float(value)*(1+int(get(buildings,'infrastructure','0'))*infra)*extraction)*retention)
    for role in list(capacity):capacity[role]=math.floor(capacity[role]*max(0,1+min(0,negative.get('local_factories',0))))
    mil=sum(v['factories'] for v in lines if not is_naval(v['equipment']));yards=sum(v['factories'] for v in lines if is_naval(v['equipment']))
    if mil>capacity['military'] or yards>capacity['dockyard']:errors.append('Opening production exceeds core capacity')
    base=scenario(lines,contract['recipes'],retained,capacity,policy,tech,contract)
    if base['industrial_import_CIV_margin']<0:errors.append('Opening industrial imports exceed conservative CIV budget')
    rotations=[];switches=[]
    def rotation_option(current,target):
        candidate=next((ident for ident in deployed if contract['recipes'][ident]['equipment']==target),None)
        if candidate is None:raise ValueError('Manual target has no eligible fielded recipe: '+target)
        switches.append(dict(from_equipment=current,to_equipment=target,recipe=candidate))
    if tag in ('SNS','AMB'):rotation_option('ship_hull_light_2' if m else 'destroyer_2','ship_hull_submarine_2' if m else 'submarine_2')
    if tag in ('UGE','DEL'):rotation_option('convoy_1','ship_hull_light_2' if m else 'destroyer_2')
    if tag=='AMB':rotation_option('small_plane_cas_airframe_1' if b else 'CAS_equipment_1','small_plane_airframe_1' if b else 'fighter_equipment_1')
    # Include Amber switching both lines at once, as well as either alone.
    for mask in range(1,1<<len(switches)):
        alternate=[dict(v) for v in lines];chosen=[v for i,v in enumerate(switches) if mask & (1<<i)]
        for switch in chosen:
            changed=next(v for v in alternate if v['equipment']==switch['from_equipment'])
            changed.update(recipe=switch['recipe'],equipment=switch['to_equipment'])
        rotations.append(dict(switches=chosen,implementation='Manual Production-screen switch; no automatic AI rotation',
            **scenario(alternate,contract['recipes'],retained,capacity,policy,tech,contract)))
    for rotation in rotations:
        if rotation['industrial_import_CIV_margin']<0:errors.append('Documented rotation imports exceed conservative CIV budget')
    air=navy=0
    for ident,count in deployed.items():
        row=contract['recipes'][ident];burn=row['stats']['fuel_consumption']*count
        if is_naval(row['equipment']):navy+=burn
        else:air+=burn
    army_proxy=army_stress=0;land_need=Counter()
    land=next(tree for name,tree in rosters.items() if '_land' in name)
    templates={get(body,'name'):body for kind,body in walk(land) if kind=='division_template'}
    for kind,body in walk(land):
        if kind!='division':continue
        template=templates[get(body,'division_template')]
        for subunit,_,_ in get(template,'regiments',[])+get(template,'support',[]):
            unit=contract['units'][subunit];needs={k:float(v) for k,_,v in unit.get('need',[])};land_need.update(needs)
            fuels={k:contract['recipes'][key(contract['gear_by_archetype'][k],{})]['stats']['fuel_consumption'] for k in needs if k in contract['gear_by_archetype']}
            army_proxy+=max([float(unit.get('fuel_consumption',0)),*fuels.values()])
            army_stress+=sum(needs[k]*v for k,v in fuels.items())
    d=contract['defines'];daily_army=army_proxy*d['NMilitary.ARMY_FUEL_COST_MULT']*24
    daily_air=air*d['NAir.FUEL_COST_MULT']*24;daily_navy=navy*d['NNavy.FUEL_COST_MULT']*24
    gain=max(0,1+policy.get('fuel_gain_factor',0)+tech.get('fuel_gain_factor',0))
    state_gain=max(0,1+min(0,policy.get('fuel_gain_factor_from_states',0)+tech.get('fuel_gain_factor_from_states',0)))
    income=(d['NCountry.BASE_FUEL_GAIN']+retained['oil']*d['NCountry.BASE_FUEL_GAIN_PER_OIL']*state_gain)*24*gain
    daily=daily_army+daily_air+daily_navy;deficit=max(0,daily-income)
    fuel_import=math.ceil(deficit/(24*d['NCountry.BASE_FUEL_GAIN_PER_OIL']*gain)) if deficit and gain else 0
    fuel_civ=math.ceil(fuel_import*contract['trade_terms']['oil']['cic'])
    stock_floor=d['NCountry.BASE_FUEL_CAPACITY']*max(0,1+min(0,policy.get('max_fuel_factor',0)+tech.get('max_fuel_factor',0)))
    reserves={contract['recipes'][ident]['equipment']:amount for ident,amount in stocks.items()}
    airborne={contract['recipes'][ident]['equipment']:amount for ident,amount in deployed.items() if not is_naval(contract['recipes'][ident]['equipment'])}
    source_hashes[history(tag).relative_to(ROOT).as_posix()]=digest(history(tag).read_bytes())
    for name in rosters:source_hashes['mod/2985041246/history/units/'+name+'.txt']=digest((MOD/'history/units'/(name+'.txt')).read_bytes())
    return dict(tag=tag,bba=b,mtg=m,nsb=n,rosters=list(rosters),source_sha256=source_hashes,
        selected_research=sorted(enabled),production=lines,MIL=mil,yards=yards,core_capacity=dict(capacity),
        conservatively_retained_resources=dict(retained),opening_policies=contract['policies'][tag],
        **base,manual_rotations=rotations,aircraft_deployed=airborne,starting_reserves=reserves,
        stored_replacement_hulls=0,initial_land_equipment_need=dict(land_need),
        fuel_sensitivity=dict(daily_army_equipment_per_subunit_proxy=round(daily_army,4),
            daily_army_literal_equipment_sum_stress=round(army_stress*d['NMilitary.ARMY_FUEL_COST_MULT']*24,4),
            daily_full_air_reference=round(daily_air,4),daily_whole_navy_patrol_reference=round(daily_navy,4),
            daily_full_proxy_total=round(daily,4),daily_fuel_income_lower=round(income,4),
            extra_oil_import_units_at_full_proxy=fuel_import,extra_fuel_import_CIV=fuel_civ,
            industrial_and_full_proxy_fuel_import_CIV_margin=base['industrial_import_CIV_margin']-fuel_civ,
            fuel_stock_floor_excluding_positive_silos=stock_floor,
            full_proxy_zero_income_stock_days=round(stock_floor/daily,3) if daily else None),
        reserve_loss_sensitivity_2percent_per_month=dict(classification='Illustrative loss assumption, not an observed native rate',
            air_reserve_months={e:round(reserves.get(e,0)/(count*.02),4) for e,count in airborne.items()}),errors=errors)


def report(reference=None):
    contract=json.loads((HERE/'primary_contract.json').read_text())
    if reference:
        for name,expected in contract['sources'].items():
            base=MOD if name.startswith('mod/') else Path(reference)
            if digest((base/name.split('/',1)[1]).read_bytes())!=expected:raise ValueError('Primary source changed: '+name)
    states=states_by_country();cases=[case(tag,b,m,n,contract,states[tag]) for tag in TAGS for b,m,n in MATRIX]
    return dict(schema=1,evidence='Actual selected script and effective primary-definition worksheet; no native acceptance',
        primary_contract_sha256=digest((HERE/'primary_contract.json').read_bytes()),cases=cases,
        limitations=['NSB on/off is enumerated; these six starts field no tank battalions and add no armor-designer route.',
            'Reconnaissance DLC mission behavior is outside this slice; no specialist reconnaissance wings are added.',
            'Replacement arithmetic assumes50percentMIL efficiency independent of unresolved native history efficiency units; excludes positive output bonuses, MIO, damage and losses.',
            'Army fuel is explicitly an equipment-stat proxy plus a separate literal-equipment stress bound; native aggregation and opening unit-tank transfers are unverified.',
            'Fuel demand is a full-roster sensitivity, not a claim that every unit operates continuously or receives delivered fuel.',
            'Imports require eligible willing suppliers and functioning transport; arithmetic CIV capacity does not establish a trade agreement or native delivery.',
            'Manual rotations are instructions, not implemented AI automation. Fielded ships are not stored replacement hulls.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.reference and not args.check:capture(args.reference)
    result=report(args.reference);text=json.dumps(result,indent=2)+'\n';path=HERE/'worksheet.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Replacement worksheet stale')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    errors=[(row['tag'],row['bba'],row['mtg'],row['nsb'],e) for row in result['cases'] for e in row['errors']]
    print('Replacement actual-source profiles',len(result['cases']),'errors',len(errors))
    for item in errors:print(item)
    if errors:raise SystemExit(1)
