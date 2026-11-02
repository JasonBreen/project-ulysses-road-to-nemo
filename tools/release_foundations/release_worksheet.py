"""Reproduce release personnel, current-state capacity and maintenance costs.

No dynamic army transfer is replaced by a deterministic roster assumption.
Core capacity/population are conservative bounds; non-core/compliance and
actual transfer selection are explicit open obligations, never zero debt.
"""
import argparse,hashlib,json,math,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/world_starts')]
from script import parse,get
from technical import Engine
from physical import contract

def establishment(name,units):
    path=MOD/'history/units'/(name+'.txt');tree=parse(path.read_text(encoding='utf-8-sig'));templates={};locations=[]
    for key,_,body in tree:
        if key!='division_template':continue
        need=Counter();personnel=0
        for ident,_,_ in get(body,'regiments',[])+get(body,'support',[]):
            data=units[ident];personnel+=float(data['manpower']);need.update({k:float(v) for k,_,v in data.get('need',[])})
        templates[get(body,'name')]=(personnel,need)
    total=Counter();people=0;count=0
    for key,_,body in tree:
        if key!='units':continue
        for kind,_,division in body:
            if kind!='division':continue
            personnel,need=templates[get(division,'division_template')];people+=personnel;total.update(need);count+=1;locations.append(int(get(division,'location')))
    return dict(source=path.relative_to(MOD).as_posix(),sha256=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),formations=count,full_establishment_personnel=people,equipment_need=dict(sorted(total.items())),inherited_locations=locations)

def report(reference=None):
    intake=json.loads((HERE/'intake.json').read_text());physical=contract();path=HERE/'worksheet.json';previous=json.loads(path.read_text()) if path.exists() else None
    if reference:
        engine=Engine(reference);units={}
        for name in ('AWW_land','REC_land'):
            tree=parse((MOD/'history/units'/(name+'.txt')).read_text(encoding='utf-8-sig'))
            for key,_,template in tree:
                if key!='division_template':continue
                for ident,_,_ in get(template,'regiments',[])+get(template,'support',[]):units[ident]=engine.unit(ident)
        units['infantry']=engine.unit('infantry');defines=engine.defines
        modifiers_path=MOD/'common/modifiers/00_static_modifiers.txt';engine.record(modifiers_path)
        non_core={k:float(v) for k,_,v in get(parse(modifiers_path.read_text()),'non_core_controller')}
        terms=json.loads((ROOT/'tools/world_starts/legacy_foundation.json').read_text())['countries']['BLK']['trade_terms']
        source_hashes=dict(sorted(engine.used.items()))
    else:
        units=previous['unit_contracts'];defines=previous['defines'];non_core=previous['non_core_controller_modifiers'];terms=previous['trade_terms'];source_hashes=previous['primary_sources_sha256']
    old={'AWW':establishment('AWW_land',units),'REC':establishment('REC_land',units)}
    blk=json.loads((ROOT/'tools/world_starts/legacy_sustainment.json').read_text())['countries']['BLK']['cases'][0]
    result={}
    for tag,country in intake['countries'].items():
        modifiers=country['opening_policies']['modifiers'];rate=max(0,modifiers.get('conscription',0));factor=max(0,1+modifiers.get('conscription_factor',0));retention=max(0,1-modifiers.get('min_export',0))
        rows=[]
        for case in country['known_cases']:
            pool=math.floor(case['core_population']*rate*factor);core=case['core_industry_lower'];cg=max(0,modifiers.get('consumer_goods_expected_value',0)*(1+modifiers.get('consumer_goods_factor',0)))
            trade=max(0,core['industrial_complex']-math.ceil((core['industrial_complex']+core['arms_factory'])*cg));materials=Counter()
            for ident in case['states']:
                state=country['state_inputs'][str(ident)]
                if tag not in state['cores'] and ident not in case.get('added_cores',[]):continue
                infrastructure=1+state['buildings']['infrastructure']*defines['NBuildings.INFRASTRUCTURE_RESOURCE_BONUS']
                negative=max(0,1+sum(min(0,modifiers.get(k,0)) for k in ('local_resources_factor','resources_factor','resource_gain_efficiency')))
                for resource,amount in state['resources'].items():materials[resource]+=math.floor(amount*infrastructure*retention*negative)
            direct=old.get(tag) if (tag=='AWW' or tag=='REC' and case['id'].startswith('recta_birth')) else None
            people=direct['full_establishment_personnel'] if direct else 0;reserve=math.ceil(people*.1)
            inherited=None
            if tag=='AWW' or tag=='SBK' and case['id']=='south_belka_collapse':
                fractions=[.25] if tag=='AWW' else [.15,.25]
                inherited=dict(fractions=fractions,reference_BLK_1991_land_personnel=blk['land_personnel'],fraction_times_reference=[f*blk['land_personnel'] for f in fractions],
                    limitation='Arithmetic reference only. Actual release date, heterogeneous division selection, casualties and stock fractions remain dynamic; this is not an exact transferred-personnel count or a native transfer guarantee.')
            projections=[]
            for key,roles in physical['cases'].items():
                choices=[]
                for role,recipe in roles.items():
                    naval=role in ('convoy','escort','submarine');inputs=recipe['stats']['resources'];deficits={r:max(0,n-materials[r]) for r,n in inputs.items()}
                    import_civ=sum(math.ceil(n*terms[r]['cic']) for r,n in deficits.items() if n)
                    capacity=core['dockyard'] if naval else core['arms_factory'];speed=defines['NProduction.BASE_FACTORY_SPEED_NAV' if naval else 'NProduction.BASE_FACTORY_SPEED_MIL']
                    choices.append(dict(role=role,equipment=recipe['equipment'],input_resources=inputs,domestic_lower=dict(materials),conditional_import_deficits=deficits,
                        single_line_trade_CIV_required=import_civ,trade_CIV_lower=trade,core_capacity_lower=capacity,
                        source_feasible_if_imports_delivered=bool(capacity>0 and import_civ<=trade),
                        thirty_day_output_at_half_MIL_efficiency=round(30*speed*(1 if naval else .5)*(1+modifiers.get('industrial_capacity_dockyard' if naval else 'industrial_capacity_factory',0))/recipe['stats']['build_cost_ic'],4),
                        deployment_fuel_consumption_per_item=recipe['stats']['fuel_consumption']))
                projections.append(dict(dlc=key,choices=choices,simultaneous_all_roles_claim=False))
            rows.append(dict(id=case['id'],states=case['states'],capital_state=case['capital_state'],capital_province=case['capital_province'],
                core_population=case['core_population'],owned_population=case['owned_population'],raw_industry=case['raw_industry'],usable_core_capacity_lower=core,
                conscription_law=country['opening_policies']['laws']['mobilization_laws'],core_recruitable_pool_lower=pool,
                inherited_direct_roster=direct,direct_roster_personnel=people,direct_roster_replacement_reserve=reserve,
                direct_roster_core_pool_margin=pool-people-reserve,dynamic_army_transfer=inherited,
                four_battalion_template_personnel=4*float(units['infantry']['manpower']),local_security_template_personnel=2*float(units['infantry']['manpower']),new_automatically_deployed_personnel=0,
                core_trade_CIV_lower=trade,replacement_choices=projections,
                personnel_status='Preserved inherited personnel liability; no core/manpower/law grant' if pool-people-reserve<0 else 'Direct roster is within conservative core pool; dynamic transfer and future recruitment remain separate',
                source_liabilities=(['AWW has no cores and disarmed_nation; the original nine formations alone exceed the conservative core pool. OptionA retains its existing weekly_manpower500 idea; optionB does not gain it. Neither gets a new recruitment law or manpower gift.','Only7430 remains controlled after the inherited nineteen BLK controller overrides; airport3269 is enemy-controlled. Other inherited AWW OOB locations are preserved warfront references, not claimed owned deployment sites.'] if tag=='AWW' else [])+
                    (['Armistice grants no SBK cores; non-core capacity and recruitment remain distinct from the defeat settlement.'] if case['id']=='south_belka_armistice' else []),
                funding='No treasury/debt seed. Initial financial cash0; development is available only when current public-owner funds/credit allow it, or through the fiscal-disabled PP route.',
                fuel='No new operational aircraft/ship/motorized formation is granted. Existing army/fuel transfers remain inherited; maintenance production does not certify mission fuel income. Future fuel imports and capacity must be reviewed before deployment.'))
        result[tag]=dict(opening_policies=country['opening_policies'],cases=rows,source_status='Guarded legitimate-release foundation implemented; inherited liabilities and native gates remain',unknown_footprint_status='Bounded owned-capital/local-maintenance fallback; no guessed network/army/deposit grant.')
    return dict(schema=1,countries=result,unit_contracts=units,defines=defines,non_core_controller_modifiers=non_core,trade_terms=terms,primary_sources_sha256=source_hashes,
        universal_sustainable_release_acceptance=False,prices=dict(project_full_billion=.02,project_legacy_FU=20,factory_project_PP=100,network_PP=50,duration_days=90,recipe_certification_PP=5,retired_queue_PP=0),
        rounding='Conservative source arithmetic; core-only capacity/resource/personnel bounds exclude positive compliance and non-core recruitment. Native rounding/mobilization are not established.',
        queue_rule='Automatic queue purchases are retired and inert, including stale direct calls. Paid5PP certification unlocks only the selected DLC technical recipe. Native Production/manual allocation owns current lines; this worksheet describes total core capacity and conditional material/import plans, not live unassigned factories. Historical purchase counters/receipts remain inert data. Conditional imports are not authored guaranteed contracts. Available-factory native observable semantics remain unverified.',
        native='No native release, DLC load, stock transfer, supply delivery, AI pacing, construction, save/reload or fuel acceptance.')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args();data=report(args.reference);text=json.dumps(data,indent=2)+'\n';path=HERE/'worksheet.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Release worksheet differs')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('Release worksheet:',len(data['countries']),'countries; inherited debt and native gates retained')
