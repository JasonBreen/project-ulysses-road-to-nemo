"""State/logistics support for the separate four-country legacy force owner.

This compiler never writes a country history, OOB, stock grant, force name or AI
file. Its captured force receipts must match the integrated legacy component
before its source-binding acceptance gate can pass.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(HERE), str(ROOT/'tools/usea_expansion'), str(ROOT/'tools')]
from script import parse, get, walk
from technical import Engine
from placement import derive
from compile import state_output
from shared_logistics import compose

PROFILES = HERE/'legacy_profiles.json'; FOUNDATION = HERE/'legacy_foundation.json'; INPUTS = HERE/'legacy_inputs.json'
REVIEWED_SOURCE_UPDATES = json.loads((ROOT/'tools/history_data_cleanup_updates.json').read_text())['files']
SETTINGS = {
    'BLK': dict(oil_base=64, fuel_silos=2, supply_centres=12, planned_resource_imports={'rubber': 21},
        excluded_new_target_states=[309],
        sealed_components=[dict(provinces=[1939,5906,7545,7569,7570,7595,7603],
            reason='Inherited impassable-adjacency enclosure in state309, without sea coast/spawn. No new force/industry or invented receiving port.')]),
    'OSE': dict(oil_base=0, fuel_silos=3, supply_centres=16,
                planned_resource_imports={'steel': 64, 'chromium': 48, 'rubber': 32}),
    'SAP': dict(oil_base=24, fuel_silos=1, supply_centres=8, planned_resource_imports={}),
    'FAT': dict(oil_base=16, fuel_silos=1, supply_centres=8,
                planned_resource_imports={'steel': 8, 'chromium': 8, 'rubber': 8}),
}


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def source_receipt_matches(relative, expected, path):
    if not path.exists(): return False
    actual = digest(path); repair = REVIEWED_SOURCE_UPDATES.get(relative)
    return actual == expected or bool(repair and expected == repair['old_normalized_sha256']
                                      and actual == repair['new_normalized_sha256'])


def intake(source):
    manifest_path = source/'tools/world_legacy/manifest.json'; manifest = json.loads(manifest_path.read_text())
    receipts = {manifest['primary_contract']:digest(source/manifest['primary_contract'])}; profiles = {}; snapshots = {}
    for tag, calibration in SETTINGS.items():
        country = next((source/'mod/2985041246/history/countries').glob(tag+' - *.txt'))
        receipts[country.relative_to(source).as_posix()] = digest(country)
        cases = [c for c in manifest['cases'] if c['tag'] == tag]
        if not cases or any(c['errors'] for c in cases): raise ValueError('Legacy owner has no clean actual-source cases: ' + tag)
        land = set(); ports = set(); air = Counter(); rosters = {}
        for case in cases:
            case_air = Counter()
            for roster in case['rosters']:
                path = source/roster['source']; text = path.read_text(encoding='utf-8-sig')
                if digest(path) != roster['sha256']: raise ValueError('Stale external roster receipt: ' + str(path))
                receipts[roster['source']] = digest(path); rosters[roster['name']] = dict(source=roster['source'], text=text)
                land.update(row['location'] for row in roster['divisions'])
                for wing in roster['wings']:
                    if str(wing['state']).isdigit(): case_air[str(wing['state'])] += wing['amount']
                for key, body in walk(parse(text)):
                    if key == 'fleet': ports.add(int(get(body, 'naval_base')))
            for state, count in case_air.items(): air[state] = max(air[state], count)
        totals = Counter()
        for path in (MOD/'history/states').glob('*.txt'):
            state = get(parse(path.read_text(encoding='utf-8-sig')), 'state'); history = get(state, 'history')
            if get(history, 'owner') != tag: continue
            buildings = get(history, 'buildings')
            totals.update({k: int(get(buildings, field, '0')) for k, field in [('civilian','industrial_complex'),('military','arms_factory'),('dockyard','dockyard')]})
        profiles[tag] = dict(name=country.stem.split(' - ',1)[1], role='retained legacy forces; state/logistics owner only',
            mode='external_owner', target_industry=dict(totals), formations={}, air={}, navy={}, production={}, naval_production={}, stocks={}, air_reserves={},
            convoys=0, airfield_count=0, infantry_battalions=0, infrastructure_floor=2,
            resource_addition_caps=dict(steel=160, aluminium=64, chromium=160, tungsten=32, rubber=64),
            required_land_deployments=sorted(land), required_naval_ports=sorted(ports), required_air_bases=dict(sorted(air.items())),
            source_layer='retained archive force identities; provisional material and logistics calibration',
            status='state/logistics implemented; exact legacy-source binding and DLC/native gates remain explicit', **calibration)
        snapshots[tag] = dict(cases=cases, rosters=rosters, history_source=country.read_text(encoding='utf-8-sig'))
    result = dict(schema=1, component_manifest='tools/world_legacy/manifest.json', component_manifest_sha256=digest(manifest_path),
        component_inputs_sha256=dict(sorted(receipts.items())), release_gaps=manifest['release_gaps'],
        core_profiles=manifest['core_profiles'], lar_disabled_gap_profiles=manifest['lar_disabled_gap_profiles'],
        unprojected_nsb=any(not isinstance(case['nsb'],bool) for case in manifest['cases']), countries=snapshots)
    INPUTS.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    PROFILES.write_text(json.dumps(dict(schema=1, countries=profiles),indent=2)+'\n',encoding='utf-8',newline='\n')


def capture(tag, profile, engine, row):
    snapshot = json.loads(INPUTS.read_text())['countries'][tag]
    cases = []; maximum = Counter(); requested = Counter(); trade_resources = {'oil'}
    unit_ids = {unit for roster in snapshot['rosters'].values() for key, _, body in parse(roster['text']) if key=='division_template'
                for unit, _, _ in get(body,'regiments',[]) + get(body,'support',[])}
    units = {ident: {k:v for k,v in engine.unit(ident).items() if k in ('need','manpower','fuel_consumption','supply_consumption')}
             for ident in sorted(unit_ids)}
    for case in snapshot['cases']:
        variants = {v['name']:v for v in case['variants']}; inputs = Counter(); lines = []
        for roster in case['rosters']:
            for line in roster['production']:
                modules = variants[line['version']]['modules'] if line['version'] else {}
                stats = engine.stats(line['equipment'], modules.values())
                inputs.update({k:n*line['factories'] for k,n in stats['resources'].items()})
                lines.append({**line, 'modules':modules, 'stats':stats,
                    'archetype':engine.resolve(line['equipment'],engine.equipment,engine.eq_files).get('archetype'),
                    'naval':'navy' in roster['name'].lower()})
        requested['mil'] = max(requested['mil'], case['requested_capacity']['mil'])
        requested['yards'] = max(requested['yards'], case['requested_capacity']['yards'])
        for key,value in inputs.items(): maximum[key] = max(maximum[key],value)
        trade_resources.update(inputs)
        # Selected source tech is recorded by its force owner; unresolved
        # component-only bridge IDs are exposed until the dependency is merged.
        effects = Counter(); unresolved = []
        for ident in case['selected_technology']:
            if ident not in engine.tech: unresolved.append(ident); continue
            engine.record(engine.tech_files[ident])
            from policies import KEYS
            effects.update({k:float(v) for k,_,v in engine.tech[ident] if k in KEYS})
        equipment = {}
        for roster in case['rosters']:
            for gear in roster['wings']+roster['ships']:
                version = gear.get('version'); modules = variants[version]['modules'] if version else {}
                key = gear['equipment']+'|'+str(version)
                equipment[key] = dict(equipment=gear['equipment'], version=version, modules=modules,
                    stats=engine.stats(gear['equipment'], modules.values()))
        needs = {k for unit in units.values() for k,_,_ in unit.get('need',[])}
        enabled = {k for ident in case['selected_technology'] if ident in engine.tech
                   for k,_,_ in get(engine.tech[ident],'enable_equipments',[])}
        enabled.update(stock['equipment'] for stock in case['stockpiles'])
        ground = {}
        for ident in sorted(enabled):
            if ident not in engine.equipment:continue
            body=engine.resolve(ident,engine.equipment,engine.eq_files);archetype=body.get('archetype')
            if archetype in needs:
                ground[ident]=dict(archetype=archetype,stats=engine.stats(ident))
        from policies import capture as capture_policies
        dlcs=({'By Blood Alone'} if case['bba'] else set())|({'Man the Guns'} if case['mtg'] else set())|({'La Resistance'} if case['lar'] else set())|({'No Step Back'} if case['nsb'] is True else set())
        actual_policies=capture_policies(snapshot.get('history_source',row['country_history_source']),tag,engine,dlcs,case['human_tags'])
        cases.append(dict(bba=case['bba'], mtg=case['mtg'], lar=case['lar'], human_tags=case['human_tags'],
            nsb=case['nsb'], capability_status=case['capability_status'], source_rosters=case['rosters'],
            lines=lines, equipment=equipment, ground_equipment=ground, stockpiles=case['stockpiles'],opening_policies=actual_policies,
            economic_technology_modifiers=dict(effects), unresolved_component_technology=unresolved,
            division_count=case['division_count'], aircraft_count=case['aircraft_count'], ship_count=case['ship_count']))
    resources, files = engine.catalog('common/resources','resources'); terms = {}
    for resource in sorted(trade_resources):
        engine.record(files[resource]);terms[resource]={k:float(get(resources[resource],k)) for k in ('cic','convoys')}
    return dict(external_cases=cases, external_unit_contracts=units, external_requested_capacity=dict(requested),
                production_inputs_max_DLC=dict(sorted(maximum.items())), trade_terms=terms)


def outputs(manifest):
    out = {}
    for row in manifest['countries'].values():
        for ident,cfg in row['placements'].items():out[row['baseline'][ident]['path']] = state_output(row,ident,cfg)
    out.update(compose(ROOT,MOD,owner='world_legacy_logistics'))
    labels=[]
    for tag,row in manifest['countries'].items():
        for province in row['new_victory_points']:labels.append(f' VICTORY_POINTS_{province}:0 "{tag} Logistics Centre {province}"')
    out['localisation/english/replace/ac_world_legacy_hubs_l_english.yml']='\ufeffl_english:\n'+'\n'.join(labels)+'\n'
    return out


def binding_gaps():
    snapshot=json.loads(INPUTS.read_text());gaps=[];path=ROOT/snapshot['component_manifest']
    if not path.exists():return ['Legacy force component not yet integrated']
    if digest(path)!=snapshot['component_manifest_sha256']:gaps.append('Legacy manifest receipt changed')
    actual=json.loads(path.read_text())
    for tag,country in snapshot['countries'].items():
        if country['cases']!=[case for case in actual.get('cases',[]) if case['tag']==tag]:
            gaps.append('Legacy selected-case snapshot differs: '+tag)
        histories=[relative for relative in snapshot['component_inputs_sha256'] if relative.startswith('mod/2985041246/history/countries/'+tag+' - ')]
        history = ROOT/histories[0] if len(histories)==1 else None
        exact_history = history and history.exists() and country['history_source']==history.read_text(encoding='utf-8-sig')
        reviewed_history = history and source_receipt_matches(histories[0],snapshot['component_inputs_sha256'][histories[0]],history)
        if not (exact_history or reviewed_history):
            gaps.append('Legacy history snapshot differs: '+tag)
        for roster in country['rosters'].values():
            source=ROOT/roster['source']
            if not source.exists() or roster['text']!=source.read_text(encoding='utf-8-sig'):
                gaps.append('Legacy roster snapshot differs: '+roster['source'])
    for relative,expected in snapshot['component_inputs_sha256'].items():
        path=ROOT/relative
        if not source_receipt_matches(relative,expected,path):gaps.append('Legacy source receipt differs: '+relative)
    if FOUNDATION.exists():
        foundation=json.loads(FOUNDATION.read_text())
        unresolved={ident for row in foundation['countries'].values() for case in row['external_cases'] for ident in case['unresolved_component_technology']}
        if unresolved:gaps.append('Unresolved component technology: '+', '.join(sorted(unresolved)))
        for relative,expected in foundation['primary_sources_sha256'].items():
            if relative.startswith('mod/'):
                path=ROOT/'mod/2985041246'/relative.removeprefix('mod/')
                if not path.exists() or digest(path)!=expected:gaps.append('Effective mod technical receipt differs: '+relative)
    return gaps


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--capture-source',type=Path);parser.add_argument('--check',action='store_true');parser.add_argument('--require-integrated-owner',action='store_true');args=parser.parse_args()
    if args.capture_source:
        if args.check:raise SystemExit('Capture and check are separate actions')
        intake(args.capture_source)
    result=derive(args.reference,PROFILES,FOUNDATION,capture);text=json.dumps(result,indent=2)+'\n'
    if args.check:
        if not FOUNDATION.exists() or FOUNDATION.read_text()!=text:raise SystemExit('Legacy physical manifest differs')
    else:FOUNDATION.write_text(text,encoding='utf-8',newline='\n')
    for relative,text in outputs(result).items():
        path=MOD/relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=text:raise SystemExit('Legacy physical output differs: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
    gaps=binding_gaps()
    if args.require_integrated_owner and gaps:raise SystemExit('; '.join(gaps))
    print('Legacy physical source outputs consistent' if args.check else 'Legacy physical source outputs generated')
    print('External owner binding:',gaps or 'exact receipts match')
