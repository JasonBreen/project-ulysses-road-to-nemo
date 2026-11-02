"""Primary-input and personnel worksheet for the external legacy force owner.

Every force/queue comes from the captured actual-source receipt, not a new OOB.
Queue-efficiency units and native mission tempo remain explicitly unverified.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion')]
from script import parse,get
from legacy_foundation import binding_gaps,PROFILES,FOUNDATION,INPUTS


def report():
    manifest=json.loads(FOUNDATION.read_text());profiles=json.loads(PROFILES.read_text())['countries'];snap=json.loads(INPUTS.read_text());countries={}
    D=manifest['defines']
    for tag,row in manifest['countries'].items():
        p=profiles[tag];pol=row['opening_policies']['modifiers'];population=sum(s['manpower'] for s in row['baseline'].values() if tag in s['cores'])
        pool=math.floor(population*max(0,pol.get('conscription',0))*max(0,1+pol.get('conscription_factor',0)))
        cg=math.ceil((row['usable_core_industry_lower']['civilian']+row['usable_core_industry_lower']['military'])*max(0,pol.get('consumer_goods_expected_value',0)*(1+pol.get('consumer_goods_factor',0))))
        trade=max(0,row['usable_core_industry_lower']['civilian']-cg);cases=[]
        for case in row['external_cases']:
            pol=case.get('opening_policies',row['opening_policies'])['modifiers']
            pool=math.floor(population*max(0,pol.get('conscription',0))*max(0,1+pol.get('conscription_factor',0)))
            cg=math.ceil((row['usable_core_industry_lower']['civilian']+row['usable_core_industry_lower']['military'])*max(0,pol.get('consumer_goods_expected_value',0)*(1+pol.get('consumer_goods_factor',0))))
            trade=max(0,row['usable_core_industry_lower']['civilian']-cg)
            inputs=Counter();replacements=[];army_fuel=land=air=naval=air_fuel=naval_fuel=0;equipment_need=Counter();templates={};missing=set()
            gear_fuel={}
            for contract in case['ground_equipment'].values():gear_fuel[contract['archetype']]=max(gear_fuel.get(contract['archetype'],0),contract['stats']['fuel_consumption'])
            for roster in case['source_rosters']:
                tree=parse(snap['countries'][tag]['rosters'][roster['name']]['text'])
                for key,_,template in tree:
                    if key=='division_template':templates[get(template,'name')]=template
                for division in roster['divisions']:
                    template=templates[division['template']]
                    for ident,_,_ in get(template,'regiments',[])+get(template,'support',[]):
                        unit=row['external_unit_contracts'][ident];land+=float(unit['manpower'])
                        need={k:float(v) for k,_,v in unit.get('need',[])};equipment_need.update(need)
                        missing.update(k for k in need if k not in gear_fuel)
                        army_fuel+=max([float(unit.get('fuel_consumption',0)),*[gear_fuel.get(k,0) for k in need]])
                for wing in roster['wings']:
                    eq=case['equipment'][wing['equipment']+'|'+str(wing['version'])]['stats']
                    air+=wing['amount']*eq['manpower'];air_fuel+=wing['amount']*eq['fuel_consumption']
                for ship in roster['ships']:
                    eq=case['equipment'][ship['equipment']+'|'+str(ship['version'])]['stats']
                    naval+=eq['manpower'];naval_fuel+=eq['fuel_consumption']
            for line in case['lines']:
                stats=line['stats'];inputs.update({k:v*line['factories'] for k,v in stats['resources'].items()})
                factor=max(0,1+pol.get('industrial_capacity_dockyard' if line['naval'] else 'industrial_capacity_factory',0)+case['economic_technology_modifiers'].get('industrial_capacity_dockyard' if line['naval'] else 'industrial_capacity_factory',0))
                speed=D['NProduction.BASE_FACTORY_SPEED_NAV' if line['naval'] else 'NProduction.BASE_FACTORY_SPEED_MIL']
                replacements.append(dict(equipment=line['equipment'],version=line['version'],factories=line['factories'],authored_efficiency=line['efficiency'],
                    thirty_day_output_at_reference_half_MIL_efficiency=round(30*speed*line['factories']*(1 if line['naval'] else .5)*factor/stats['build_cost_ic'],4)))
            shortage={k:max(0,v-row['retained_industrial_inputs_conservative'][k]) for k,v in sorted(inputs.items())}
            imports=sum(math.ceil(n*row['trade_terms'][k]['cic']) for k,n in shortage.items() if n)
            tech=case['economic_technology_modifiers'];gain=pol.get('fuel_gain_factor',0)+tech.get('fuel_gain_factor',0)
            state_gain=max(0,1+min(0,pol.get('fuel_gain_factor_from_states',0)+tech.get('fuel_gain_factor_from_states',0)))
            income=(D['NCountry.BASE_FUEL_GAIN']+row['retained_industrial_inputs_conservative']['oil']*D['NCountry.BASE_FUEL_GAIN_PER_OIL']*state_gain)*24*(1+gain)
            daily_army=army_fuel*D['NMilitary.ARMY_FUEL_COST_MULT']*24
            daily_air=air_fuel*D['NAir.FUEL_COST_MULT']*24;daily_navy=naval_fuel*D['NNavy.FUEL_COST_MULT']*24
            total=daily_army+daily_air+daily_navy;fuel_deficit=max(0,total-income)
            oil_imports=math.ceil(fuel_deficit/(24*D['NCountry.BASE_FUEL_GAIN_PER_OIL']*(1+gain)))
            floor=D['NCountry.BASE_FUEL_CAPACITY']*max(0,1+min(0,pol.get('max_fuel_factor',0)+tech.get('max_fuel_factor',0)))
            deployed=math.ceil(land+air+naval);reserve=math.ceil(deployed*.1)
            cases.append(dict(bba=case['bba'],mtg=case['mtg'],lar=case['lar'],nsb=case['nsb'],human_tags=case['human_tags'],
                capability_status=case['capability_status'],resource_inputs=dict(sorted(inputs.items())),industrial_import_deficits=shortage,
                trade_CIV_required=imports,trade_CIV_lower=trade,industrial_trade_CIV_margin=trade-imports,
                replacement_reference=replacements,land_personnel=land,air_personnel=air,naval_personnel=naval,
                core_recruitable_pool_lower=pool,replacement_personnel_reserve=reserve,personnel_headroom=pool-deployed-reserve,
                full_establishment_equipment_need=dict(sorted(equipment_need.items())),missing_enabled_ground_equipment=sorted(missing),
                full_establishment_army_fuel_proxy_per_day=daily_army,full_air_fuel_reference_per_day=daily_air,whole_navy_patrol_reference_per_day=daily_navy,
                fuel_income_lower=income,full_activity_proxy_total=total,full_activity_oil_import_units=oil_imports,
                full_activity_all_import_trade_CIV_margin=trade-imports-math.ceil(oil_imports*row['trade_terms']['oil']['cic']),
                starting_fuel_floor_excluding_positive_storage=floor,
                lower_bound_fuel_days_net_full_proxy=round(floor/fuel_deficit,2) if fuel_deficit else None,
                production_efficiency_unit_status='Primary native OOBs use25/50 convention while effects documentation includes fractional example; no native unit interpretation or observed rate is claimed.'))
        countries[tag]=dict(source_layer='retained force owner plus provisional state/material/logistics calibration',opening_policies=row['opening_policies'],
            core_industry_lower=row['usable_core_industry_lower'],resource_additions=row['resource_additions'],core_population=population,
            sealed_components=[c for c in row['components'] if c.get('sealed_source_exception')],cases=cases)
    return dict(schema=1,universal_sustainable_start_acceptance=False,component_binding_gaps=binding_gaps(),
        release_gaps=snap['release_gaps'],coverage='Actual-source line/force receipts and primary technical inputs; trade delivery, DLC mission availability, efficiency interpretation and natural throughput remain pending.',countries=countries)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();data=report();text=json.dumps(data,indent=2)+'\n';path=HERE/'legacy_sustainment.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Legacy source sustainment report differs')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    for tag,row in data['countries'].items():print(tag,'worst industrial import CIV margin',min(c['industrial_trade_CIV_margin'] for c in row['cases']),'worst personnel headroom',min(c['personnel_headroom'] for c in row['cases']))
