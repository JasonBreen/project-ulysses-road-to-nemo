"""Additive placements on captured active-country state histories.

No owner/core/manpower/province, border, raster, airport or coordinate edits.
Disconnected components receive real owned coastal terminals, never water rails.
"""
import argparse
from collections import Counter, deque
import copy
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools/usea_expansion'), str(ROOT / 'tools/anea'), str(ROOT / 'tools')]
from script import parse, get
from foundation_map import topology, components, shortest
from capabilities import equipment_for, design_for, supports, retained_tree, dlc_cases, case_key, divisions
from technical import Engine
from policies import capture as capture_policies, KEYS as POLICY_KEYS
from inventory import selected

FIELDS = {'civilian': 'industrial_complex', 'military': 'arms_factory', 'dockyard': 'dockyard',
          'infrastructure': 'infrastructure', 'air_base': 'air_base', 'fuel_silo': 'fuel_silo'}


def distances(start, graph, allowed):
    result = {start: 0}; queue = deque([start])
    while queue:
        p = queue.popleft()
        for n in sorted(graph[p] & allowed):
            if n not in result:
                result[n] = result[p] + 1; queue.append(n)
    return result


def separated(states, airports, graph, allowed, first, count):
    chosen = [first] if first in states else [min(states)]
    nearest = distances(airports[chosen[0]], graph, allowed)
    while len(chosen) < min(count, len(states)):
        candidate = max(set(states) - set(chosen), key=lambda i: (nearest[airports[i]], -i))
        chosen.append(candidate); new = distances(airports[candidate], graph, allowed)
        nearest = {p: min(d, new[p]) for p, d in nearest.items()}
    return chosen


def new_rail_rows(routes, inherited):
    """Do not redeclare inherited edges or rely on duplicate-level precedence."""
    seen = set(inherited); rows = []; reused = set()
    for route in routes:
        segment = []
        for a, b in zip(route, route[1:]):
            edge = tuple(sorted((a, b)))
            if edge in seen:
                if edge in inherited: reused.add(edge)
                if len(segment) > 1: rows.append('2 ' + str(len(segment)) + ' ' + ' '.join(map(str, segment)))
                segment = []
            else:
                if not segment: segment.append(a)
                segment.append(b); seen.add(edge)
        if len(segment) > 1: rows.append('2 ' + str(len(segment)) + ' ' + ' '.join(map(str, segment)))
    return rows, [dict(edge=list(edge), level=inherited[edge]) for edge in sorted(reused)]


def base_state(path):
    source = path.read_text(encoding='utf-8-sig'); state = get(parse(source), 'state')
    history = get(state, 'history'); buildings = get(history, 'buildings')
    return {'path': path.relative_to(MOD).as_posix(), 'source': source,
        'owner': get(history, 'owner'), 'cores': [v for k, _, v in history if k == 'add_core_of'],
        'manpower': int(get(state, 'manpower')), 'provinces': [int(k) for k, _, _ in get(state, 'provinces')],
        'buildings': {key: int(get(buildings, field, '0')) for key, field in FIELDS.items()},
        'ports': {str(p): int(get(v, 'naval_base')) for p, _, v in buildings if isinstance(v, list) and get(v, 'naval_base')},
        'resources': {k: v for k, _, v in get(state, 'resources', [])},
        'victory_points': {str(v[0][0]): int(v[1][0]) for k, _, v in history if k == 'victory_points'},
        'category': get(state, 'state_category'), 'max_level_factor': get(state, 'buildings_max_level_factor', '1.000')}


def input_requirements(profile, engine):
    worst = Counter()
    for bba, mtg, nsb in dlc_cases(profile):
        totals = Counter()
        for role, amount in {**profile['production'], **profile['naval_production']}.items():
            design = design_for(role, bba, mtg, nsb)
            stats = engine.stats(equipment_for(role, bba, mtg, nsb), design['modules'].values() if design else ())
            totals.update({k: n * amount for k, n in stats['resources'].items()})
        for key, value in totals.items():
            worst[key] = max(worst[key], value)
    return dict(worst)


def capture_technical(profile, engine, row=None):
    from compile import technologies
    from capabilities import AIR, NAVY, LAND
    cases = {}; tech = {}; economic_tech = {}
    for bba, mtg, nsb in dlc_cases(profile):
        key = case_key(bba, mtg, nsb); tech[key] = technologies(profile, engine, bba, mtg, nsb); cases[key] = {}
        enabled = set(tech[key]); dlcs = ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set()) | ({'No Step Back'} if nsb else set())
        for name, _, body in selected(parse(row['country_history_source']), dlcs, row['tag']):
            if name == 'set_technology':
                for ident, _, value in body:
                    if value == '1': enabled.add(ident)
                    elif value == '0': enabled.discard(ident)
        effects = Counter(); unresolved = []
        for ident in sorted(enabled):
            if ident not in engine.tech: unresolved.append(ident); continue
            engine.record(engine.tech_files[ident])
            effects.update({k: float(v) for k, _, v in engine.tech[ident] if k in POLICY_KEYS})
        economic_tech[key] = dict(modifiers=dict(effects), unresolved_inherited_tech=unresolved)
        for role in sorted(set(profile['production']) | set(profile['naval_production'])):
            ident = equipment_for(role, bba, mtg, nsb); design = design_for(role, bba, mtg, nsb)
            cases[key][role] = {'equipment': ident, 'modules': design['modules'] if design else {},
                'equipment_technology': engine.equipment_tech(ident),
                'module_technologies': {m: engine.module_tech(m) for m in design['modules'].values()} if design else {},
                'stats': engine.stats(ident, design['modules'].values() if design else ()),
                'design_slots': engine.design_slots(ident, design['modules']) if design else {}}
    units = set(LAND[role] for role, count in profile['formations'].items() if count) | set(supports(profile)) if profile['mode'] != 'retained_start' else set()
    if profile['formations'].get('armor'):
        units.add('motorized')
    if profile['mode'] == 'retained_start':
        units = {k for key, _, body in retained_tree(row) if key == 'division_template'
                 for k, _, _ in get(body, 'regiments', []) + get(body, 'support', [])}
    if any(role != 'infantry' and count for role, count in profile['formations'].items()):
        units.add('logistics_company')
    unit_data = {ident: {k: v for k, v in engine.unit(ident).items() if k in ('need', 'fuel_consumption', 'manpower', 'supply_consumption', 'active')}
                 for ident in sorted(units)}
    gear = {ident: engine.resolve(ident, engine.equipment, engine.eq_files)['archetype'] for ident in profile['stocks']}
    if not hasattr(engine, '_start_resource_terms'):
        resources, files = engine.catalog('common/resources', 'resources')
        engine._start_resource_terms = resources, files
    resources, files = engine._start_resource_terms
    trade_terms = {}
    for resource in sorted(set(input_requirements(profile, engine)) | {'oil'}):
        engine.record(files[resource])
        trade_terms[resource] = {k: float(get(resources[resource], k)) for k in ('cic', 'convoys')}
    return {'starting_tech': tech, 'economic_technology_modifiers': economic_tech, 'trade_terms': trade_terms, 'recipe_contracts': cases, 'unit_contracts': unit_data, 'gear_archetypes': gear,
            'gear_stats': {ident: engine.stats(ident) for ident in profile['stocks']},
            'production_inputs_max_DLC': input_requirements(profile, engine)}


def derive(reference):
    profiles = json.loads((HERE / 'profiles.json').read_text())['countries']
    prior = json.loads((HERE / 'foundation.json').read_text()) if (HERE / 'foundation.json').exists() else None
    current = {int(get(get(parse(p.read_text(encoding='utf-8-sig')), 'state'), 'id')): p for p in (MOD / 'history/states').glob('*.txt')}
    states = {i: base_state(path) for i, path in current.items()}
    defs, graph, _, pixels, _ = topology(); engine = Engine(reference) if reference else None
    if not engine and not prior:
        raise ValueError('First technical capture requires a read-only --reference')
    defines = engine.defines if engine else prior['defines']
    airports = {int(k): int(v[0][0]) for k, _, v in parse((MOD / 'map/airports.txt').read_text()) if k.isdigit() and v}
    building_rows = [r.split(';') for r in (MOD / 'map/buildings.txt').read_text().splitlines() if ';' in r]
    spawns = {(int(r[0]), int(r[6])) for r in building_rows if r[1] == 'naval_base_spawn'}
    inherited_nodes = {int(r.split()[1]) for r in (MOD / 'map/supply_nodes.txt').read_text().splitlines() if r.strip()}
    # Once installed, this owner's own rows must not become an inherited input.
    if prior:
        inherited_nodes -= {p for row in prior['countries'].values() for p in row['supply_hubs']}
    old_world = json.loads((ROOT / 'tools/world_foundation/foundation.json').read_text())
    from shared_logistics import declared_owners
    anchor = min((m['map_baselines']['map/railways.txt'] for _, m in declared_owners(ROOT)), key=lambda m: m['lines'])
    inherited_rails = {}
    for line in (MOD / 'map/railways.txt').read_text().splitlines()[:anchor['lines']]:
        level, _, *path = map(int, line.split())
        for a, b in zip(path, path[1:]):
            edge = tuple(sorted((a, b))); inherited_rails[edge] = max(level, inherited_rails.get(edge, 0))
    output = {'schema': 1, 'source_base': '60ec3a6', 'source_layer': 'provisional gameplay on retained mod geography',
              'map_baselines': old_world['map_baselines'], 'countries': {},
              'raster_sha256': hashlib.sha256((MOD / 'map/provinces.bmp').read_bytes()).hexdigest(), 'defines': defines}
    control = get(parse((MOD / 'common/modifiers/00_static_modifiers.txt').read_text()), 'non_core_controller')
    output['non_core_controller_modifiers'] = {k: float(v) for k, _, v in control if k in ('local_factories', 'local_resources', 'local_building_slots_factor')}
    if engine:
        output['reference_version'] = json.loads((Path(reference) / 'launcher-settings.json').read_text())['rawVersion']
        output['fuel_technology_gain'] = sum(float(get(engine.tech[ident], 'fuel_gain_factor', '0')) for ident in ('fuel_silos', 'fuel_refining'))
        for ident in ('fuel_silos', 'fuel_refining'):
            engine.record(engine.tech_files[ident])
        engine.record(MOD / 'common/ideas/_economic.txt')
        engine.record(MOD / 'common/technologies/NSB_armor.txt')
        engine.record(Path(reference) / 'common/technologies/NSB_armor.txt')
        engine.record(MOD / 'common/modifiers/00_static_modifiers.txt')
    else:
        output['reference_version'] = prior['reference_version']
        output['fuel_technology_gain'] = prior['fuel_technology_gain']
    for tag, profile in profiles.items():
        previous = prior['countries'].get(tag) if prior else None
        path = next((MOD / 'history/countries').glob(tag + ' - *.txt'))
        source = previous['country_history_source'] if previous else path.read_text(encoding='utf-8-sig')
        capital = int(get(parse(source), 'capital'))
        ids = sorted(i for i, s in states.items() if s['owner'] == tag)
        if tag == 'PLH' or 171 in ids or not ids:
            raise ValueError('No blanket start grant for placeholder/emergent country: ' + tag)
        baseline = copy.deepcopy(previous['baseline']) if previous else {str(i): states[i] for i in ids}
        if set(map(int, baseline)) != set(ids) or capital not in ids:
            raise ValueError('Owned states/capital changed: ' + tag)
        for i in ids:
            for key in ('owner', 'cores', 'manpower', 'provinces'):
                if states[i][key] != baseline[str(i)][key]:
                    raise ValueError('Protected state identity changed: ' + tag + ':' + str(i))
        owned = {p for i in ids for p in baseline[str(i)]['provinces'] if defs[p]['land']}
        province_state = {p: i for i in ids for p in baseline[str(i)]['provinces']}
        groups = sorted(components(owned, graph), key=lambda g: (-sum(int(pixels[p]) for p in g), min(g)))
        cap_points = baseline[str(capital)]['victory_points']
        cap_p = int(max(cap_points, key=lambda p: (cap_points[p], -int(p)))) if cap_points else airports[capital]
        if cap_p not in owned or cap_p not in baseline[str(capital)]['provinces']:
            raise ValueError('Capital supply origin is not retained owned land')
        main = groups[0]; eligible = [i for i in ids if airports[i] in main]
        core_ids = {i for i in ids if tag in baseline[str(i)]['cores']}
        industrial_eligible = [i for i in eligible if i in core_ids]
        if not industrial_eligible: raise ValueError('No owned-core industrial terminal: ' + tag)
        total_industry = sum(profile['target_industry'].values())
        industry = separated(industrial_eligible, airports, graph, main, capital, max(3, math.ceil(total_industry / 7)))
        row = {'tag': tag, 'capital': capital, 'capital_province': cap_p, 'states': ids, 'provinces': sorted(owned),
            'country_history': path.relative_to(MOD).as_posix(), 'country_history_source': source,
            'baseline': baseline, 'industry_states': industry, 'placements': {}, 'ports': [], 'components': [],
            'supply_hubs': [], 'all_supply_hubs': [], 'routes': [], 'new_victory_points': {}, 'resource_additions': []}
        row['non_core_controller_modifiers'] = output['non_core_controller_modifiers']
        digest = hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest()
        if not engine and previous['profile_sha256'] != digest:
            raise ValueError('Changed profile needs an explicit primary-contract recapture: ' + tag)
        row['profile_sha256'] = digest
        if profile['mode'] == 'retained_start':
            row['retained_land_source'] = previous['retained_land_source'] if previous else (MOD / ('history/units/' + profile['inherited_land_file'] + '.txt')).read_text(encoding='utf-8-sig')
        contracts = capture_technical(profile, engine, row) if engine else {k: copy.deepcopy(previous[k]) for k in
            ('starting_tech', 'economic_technology_modifiers', 'trade_terms', 'recipe_contracts', 'unit_contracts', 'gear_archetypes', 'gear_stats', 'production_inputs_max_DLC')}
        row.update(contracts)
        row['opening_policies'] = capture_policies(source, tag, engine) if engine else copy.deepcopy(previous['opening_policies'])
        row['core_states'] = sorted(core_ids)
        if row['opening_policies']['negative_modifiers'].get('local_factories', 0) < 0:
            raise ValueError('Opening factory-count penalty needs explicit capacity calibration: ' + tag)
        for i in ids:
            old = baseline[str(i)]
            row['placements'][str(i)] = {**copy.deepcopy(old['buildings']), 'naval_bases': copy.deepcopy(old['ports']),
                'resources': copy.deepcopy(old['resources'])}
        cfg = row['placements']
        for key in ('civilian', 'military'):
            remaining = profile['target_industry'][key] - sum(v[key] for v in cfg.values())
            if remaining < 0:
                raise ValueError('Target would remove inherited buildings: ' + tag)
            for n in range(remaining):
                candidates = [i for i in industry if sum(cfg[str(i)][k] for k in ('civilian', 'military', 'dockyard')) < 10]
                if not candidates:
                    raise ValueError('Review industrial capacity distribution: ' + tag)
                i = min(candidates, key=lambda i: (sum(cfg[str(i)][k] for k in ('civilian', 'military', 'dockyard')), industry.index(i)))
                cfg[str(i)][key] += 1
        all_ports = {}
        for index, group in enumerate(groups):
            coasts = sorted(p for p in group if defs[p]['coastal'] and any(defs[n]['kind'] == 'sea' and (province_state[p], n) in spawns for n in graph[p]))
            ports = sorted(int(p) for i in ids for p in cfg[str(i)]['naval_bases'] if int(p) in group)
            if any(p not in coasts for p in ports):
                raise ValueError('Inherited port needs explicit validity review: ' + tag)
            if not ports and coasts:
                root_hint = cap_p if cap_p in group else airports[next(i for i in ids if airports[i] in group)] if any(airports[i] in group for i in ids) else min(group)
                d = distances(root_hint, graph, group); p = min(coasts, key=lambda p: (d[p], p))
                cfg[str(province_state[p])]['naval_bases'][str(p)] = 1; ports = [p]
            if index and not ports:
                raise ValueError('Detached component has no valid receiving port: ' + tag)
            root = cap_p if cap_p in group else ports[0] if ports else min(group)
            row['components'].append({'index': index, 'provinces': sorted(group), 'root': root, 'ports': ports, 'routes': [], 'terminals': []})
            for p in ports:
                all_ports[p] = {'province': p, 'state': province_state[p], 'component': index}
        # Large new dockyard programmes need several real industrial receiving
        # states; do not pile all eighteen yards onto an inherited capital.
        naval_component = next((c for c in row['components'] if c['ports']), None)
        naval_land = set(naval_component['provinces']) if naval_component else set()
        desired_port_states = min(3, max(1, math.ceil(profile['target_industry']['dockyard'] / 6)))
        while len({province_state[p] for p in all_ports if p in naval_land}) < desired_port_states:
            occupied = {province_state[p] for p in all_ports if p in naval_land}
            candidates = [p for p in naval_land if province_state[p] in core_ids and province_state[p] not in occupied and defs[p]['coastal'] and
                any(defs[n]['kind'] == 'sea' and (province_state[p], n) in spawns for n in graph[p])]
            if not candidates:
                break
            p = min(candidates, key=lambda p: (province_state[p] not in industry,
                sum(cfg[str(province_state[p])][k] for k in ('civilian', 'military', 'dockyard')), p))
            cfg[str(province_state[p])]['naval_bases'][str(p)] = 3
            all_ports[p] = {'province': p, 'state': province_state[p], 'component': naval_component['index']}
            naval_component['ports'].append(p)
        row['ports'] = [all_ports[p] for p in sorted(all_ports)]
        naval_ports = [p for p in all_ports if p in naval_land]
        if profile['target_industry']['dockyard'] and not naval_ports:
            raise ValueError('No owned dockyard receiving coast: ' + tag)
        port_states = sorted({province_state[p] for p in naval_ports if province_state[p] in core_ids}, key=lambda i: (-cfg[str(i)]['dockyard'], i))
        dock_additions = profile['target_industry']['dockyard'] - sum(v['dockyard'] for v in cfg.values())
        if dock_additions < 0:
            raise ValueError('Target would remove inherited dockyards: ' + tag)
        for n in range(dock_additions):
            state = min(port_states, key=lambda i: (sum(cfg[str(i)][k] for k in ('civilian', 'military', 'dockyard')), i))
            cfg[str(state)]['dockyard'] += 1
            cfg[str(state)]['infrastructure'] = max(cfg[str(state)]['infrastructure'], profile['infrastructure_floor'])
            if state not in industry:
                industry.append(state)
        if naval_component and cap_p not in naval_land:
            row['naval_access_note'] = {'capital_component_is_landlocked': True,
                'owned_naval_component': naval_component['index'],
                'existing_faction_members': [v for k, _, v in parse(source) if k == 'add_to_faction'],
                'boundary': 'No mainland coast or water rail is invented. Overseas naval supply relies on existing friendly-port/transit rules; native relay acceptance remains pending.'}
        if row['ports']:
            base = max(row['ports'], key=lambda p: (int(p['province'] in main), cfg[str(p['state'])]['naval_bases'][str(p['province'])], -p['province']))
            row['naval_base'] = base['province']
            inherited_port = str(base['province']) in baseline[str(base['state'])]['ports']
            if sum(profile['navy'].values()) and not inherited_port:
                cfg[str(base['state'])]['naval_bases'][str(base['province'])] = max(cfg[str(base['state'])]['naval_bases'][str(base['province'])], 5 if len(owned) > 500 else 3)
        air_states = separated(eligible, airports, graph, main, capital, profile['airfield_count'])[:profile['airfield_count']] if profile['airfield_count'] else []
        row['air_states'] = air_states; row['airports'] = {str(i): airports[i] for i in air_states}
        row['air_deployments'] = []
        for n, i in enumerate(air_states):
            deployment = {'state': i}
            for role, amount in profile['air'].items():
                deployment[role] = amount // len(air_states) + (n < amount % len(air_states))
            row['air_deployments'].append(deployment)
            cfg[str(i)]['air_base'] = max(cfg[str(i)]['air_base'], math.ceil(sum(deployment[r] for r in profile['air']) / 200))
        for n in range(max(0, profile['fuel_silos'] - sum(v['fuel_silo'] for v in cfg.values()))):
            silo_states = list(dict.fromkeys([capital] + industry))
            cfg[str(silo_states[n % len(silo_states)])]['fuel_silo'] += 1
        for i in set(industry + air_states):
            cfg[str(i)]['infrastructure'] = max(cfg[str(i)]['infrastructure'], profile['infrastructure_floor'])
        industrial_hubs = [airports[i] for i in industry[:profile['supply_centres']]]
        for component in row['components']:
            group = set(component['provinces']); root = component['root']
            hubs = list(dict.fromkeys(([cap_p] if cap_p in group else []) + [p for p in industrial_hubs if p in group]))
            inherited_deployments = [int(get(body, 'location')) for body in divisions(retained_tree(row))] if profile['mode'] == 'retained_start' else []
            terminals = list(dict.fromkeys(hubs + component['ports'] + [airports[i] for i in industry + air_states if airports[i] in group] + [p for p in inherited_deployments if p in group]))
            component['terminals'] = terminals; component['supply_hubs'] = hubs
            component['routes'] = [shortest(root, p, graph, group) for p in terminals if p != root]
            row['routes'].extend(component['routes']); row['all_supply_hubs'].extend(hubs)
            row['supply_hubs'].extend(p for p in hubs if p not in inherited_nodes)
        cap_hubs = row['all_supply_hubs'] or [cap_p]
        row['land_deployments'] = [cap_hubs[n % len(cap_hubs)] for n in range(sum(profile['formations'].values()))]
        if profile['mode'] == 'retained_start':
            row['land_deployments'] = [int(get(body, 'location')) for body in divisions(retained_tree(row))]
            if not set(row['land_deployments']) <= owned: raise ValueError('Inherited army has foreign deployment: ' + tag)
        row['railway_rows'], row['reused_inherited_rail_edges'] = new_rail_rows(row['routes'], inherited_rails)
        all_vps = {p for b in baseline.values() for p in b['victory_points']}
        row['new_victory_points'] = {str(p): 20 if p == cap_p else 5 for p in row['all_supply_hubs'] if str(p) not in all_vps}
        needs = row['production_inputs_max_DLC']
        resource_states = [i for i in dict.fromkeys([capital] + industry) if i in core_ids][:3]
        modifiers = row['opening_policies']['modifiers']; negative = row['opening_policies']['negative_modifiers']
        retention = max(0, 1 - modifiers.get('min_export', .5))
        resource_gain_lower = max(0, 1 + sum(negative.get(k, 0) for k in ('local_resources_factor', 'resources_factor', 'resource_gain_efficiency')))
        def retained(resource):
            return sum(math.floor(math.floor(float(v['resources'].get(resource, 0)) * (1 + v['infrastructure'] * defines['NBuildings.INFRASTRUCTURE_RESOURCE_BONUS']) * resource_gain_lower) * retention) for i, v in cfg.items() if int(i) in core_ids)
        for resource, need in sorted(needs.items()):
            n = 0
            while retained(resource) < max(0, math.ceil(need) - profile.get('planned_resource_imports', {}).get(resource, 0)):
                i = resource_states[n % len(resource_states)]; v = cfg[str(i)]
                v['resources'][resource] = float(v['resources'].get(resource, 0)) + 1; n += 1
                if n > profile['resource_addition_caps'].get(resource, 0):
                    raise ValueError('Resource addition exceeds reviewed cap: ' + tag + ':' + resource)
        for n in range(profile['oil_base']):
            v = cfg[str(resource_states[n % len(resource_states)])]
            v['resources']['oil'] = float(v['resources'].get('oil', 0)) + 1
        for i in ids:
            for resource, value in cfg[str(i)]['resources'].items():
                delta = float(value) - float(baseline[str(i)]['resources'].get(resource, 0))
                if delta:
                    row['resource_additions'].append({'state': i, 'resource': resource, 'addition': delta})
        row['retained_industrial_inputs_conservative'] = {r: retained(r) for r in sorted(set(needs) | {'oil'})}
        row['usable_core_industry_lower'] = {key: sum(v[key] for i, v in cfg.items() if int(i) in core_ids) for key in ('civilian', 'military', 'dockyard')}
        row['resource_policy_lower'] = dict(export_fraction=1-retention, negative_resource_factor=resource_gain_lower,
            non_core_resources_counted=0, positive_extraction_bonuses_counted=False,
            note='Known trade and negative idea modifiers applied; non-core output excluded instead of assuming native compliance/rounding.')
        if sum(profile['production'].values()) > row['usable_core_industry_lower']['military']:
            raise ValueError('Production exceeds conservative core MIL capacity: ' + tag)
        if sum(profile['naval_production'].values()) > row['usable_core_industry_lower']['dockyard']:
            raise ValueError('Production exceeds conservative core yard capacity: ' + tag)
        output['countries'][tag] = row
    output['primary_sources_sha256'] = dict(sorted(engine.used.items())) if engine else prior['primary_sources_sha256']
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--reference', type=Path); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    target = HERE / 'foundation.json'; text = json.dumps(derive(args.reference), indent=2) + '\n'
    if args.check:
        if not target.exists() or target.read_text() != text:
            raise SystemExit('Active-world placement manifest differs')
    else:
        target.write_text(text, encoding='utf-8', newline='\n')
    print('Active-world additive placements ' + ('consistent' if args.check else 'generated'))
