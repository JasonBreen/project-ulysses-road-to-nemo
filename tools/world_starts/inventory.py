"""Branch-sensitive active-world foundation inventory; no native claims.

Four BBA/MTG projections are evaluated explicitly, with additional FATO/Osean
AI contexts recorded. Unknown history conditions fail closed, not as false.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'tools/usea_expansion'), str(ROOT / 'tools/anea')]
from script import parse, get, walk
from foundation_map import topology, components


def condition(nodes, dlcs, current, human_tags, flags=None):
    values = []
    for key, _, value in nodes:
        name = key.lower()
        if name == 'has_dlc':
            result = value.strip('"') in dlcs
        elif name in ('and', 'or', 'not'):
            children = [condition([n], dlcs, current, human_tags, flags) for n in value]
            result = any(children) if name == 'or' else not all(children) if name == 'not' else all(children)
        elif name == 'always':
            result = value == 'yes'
        elif name == 'is_ai':
            result = (current not in human_tags) == (value == 'yes')
        elif name in ('tag', 'original_tag'):
            result = value == current
        elif name == 'has_country_flag' and isinstance(value, str) and flags is not None:
            result = value in flags.get(current, set())
        elif re.fullmatch('[A-Z]{3}', key) and isinstance(value, list):
            result = condition(value, dlcs, key, human_tags, flags)
        else:
            raise ValueError('Uninspected history condition: ' + key)
        values.append(result)
    return all(values)


def selected(nodes, dlcs, current, human_tags=(), flags=None):
    if flags is None: flags = {}
    previous = None
    for key, op, value in nodes:
        if key == 'if':
            chosen = condition(get(value, 'limit', []), dlcs, current, human_tags, flags)
            previous = chosen
            if chosen:
                yield from selected([n for n in value if n[0] not in ('limit', 'else', 'else_if')], dlcs, current, human_tags, flags)
            else:
                alternatives = [n for n in value if n[0] in ('else_if', 'else')]
                for kind, _, body in alternatives:
                    if kind == 'else' or condition(get(body, 'limit', []), dlcs, current, human_tags, flags):
                        yield from selected([n for n in body if n[0] != 'limit'], dlcs, current, human_tags, flags)
                        previous = True
                        break
        elif key in ('else', 'else_if'):
            if previous is None:
                raise ValueError('Orphan history alternative')
            if not previous and (key == 'else' or condition(get(value, 'limit', []), dlcs, current, human_tags, flags)):
                yield from selected([n for n in value if n[0] != 'limit'], dlcs, current, human_tags, flags)
                previous = True
        else:
            previous = None
            if key == 'set_country_flag': flags.setdefault(current, set()).add(value)
            elif key == 'clr_country_flag': flags.setdefault(current, set()).discard(value)
            yield key, op, value


def read(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


def roster(name, tag, province_owner, state_owner):
    path = MOD / 'history/units' / (name + '.txt')
    if not path.exists():
        return {'file': name, 'error': 'missing'}
    try:
        tree = parse(path.read_text(encoding='utf-8-sig'))
    except (ValueError, IndexError) as error:
        return {'file': name, 'error': str(error)}
    divisions = []; ships = []; aircraft = Counter(); production = Counter(); types = Counter(); invalid = []
    for key, body in walk(tree):
        if key == 'division':
            p = int(get(body, 'location', '0')); divisions.append({'name': get(body, 'name'), 'location': p, 'template': get(body, 'division_template')})
            if province_owner.get(p) != tag:
                invalid.append({'kind': 'land deployment', 'province': p, 'owner': province_owner.get(p)})
        elif key == 'division_template':
            types.update(k for k, _, _ in get(body, 'regiments', []))
        elif key == 'ship':
            ships.append({'name': get(body, 'name'), 'definition': get(body, 'definition'), 'equipment': get(body, 'equipment')})
        elif key == 'fleet':
            p = int(get(body, 'naval_base', '0'))
            if province_owner.get(p) != tag:
                invalid.append({'kind': 'naval base', 'province': p, 'owner': province_owner.get(p)})
        elif key == 'add_equipment_production':
            production[get(get(body, 'equipment', []), 'type', 'unknown')] += int(get(body, 'requested_factories', '0'))
    for state, _, wings in get(tree, 'air_wings', []):
        for kind, _, details in wings:
            aircraft[kind] += int(get(details, 'amount', '0'))
        if state.strip('"').isdigit() and state_owner.get(int(state.strip('"'))) != tag:
            invalid.append({'kind': 'air deployment', 'state': int(state), 'owner': state_owner.get(int(state))})
    return {'file': name, 'divisions': len(divisions), 'division_details': divisions,
        'regiment_types': dict(sorted(types.items())), 'aircraft': dict(sorted(aircraft.items())),
        'ships': len(ships), 'ship_names': [s['name'].strip('"') for s in ships],
        'ship_definitions': dict(Counter(s['definition'] for s in ships)),
        'production': dict(sorted(production.items())), 'invalid_placements': invalid}


def inspect():
    registry = json.loads((ROOT / 'tools/world_foundation/country_registry.json').read_text())
    defs, graph, _, _, _ = topology()
    states = {}; province_owner = {}; state_owner = {}
    for path in sorted((MOD / 'history/states').glob('*.txt')):
        body = get(parse(path.read_text(encoding='utf-8-sig')), 'state'); history = get(body, 'history', [])
        ident = int(get(body, 'id')); tag = get(history, 'owner'); provinces = [int(k) for k, _, _ in get(body, 'provinces', [])]
        states[ident] = {'body': body, 'history': history, 'provinces': provinces, 'owner': tag}
        state_owner[ident] = tag; province_owner.update({p: tag for p in provinces})
    rows = []
    for existing in registry['countries']:
        tag = existing['tag']; history = read(existing['history'])
        owned = {p for i in existing['owned_states'] for p in states[i]['provinces'] if defs[p]['land']}
        groups = components(owned, graph)
        coasts = [p for p in owned if defs[p]['coastal'] and any(defs[n]['kind'] == 'sea' for n in graph[p])]
        cases = []
        for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
            dlcs = ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set())
            effects = list(selected(history, dlcs, tag)); refs = [v.strip('"') for k, _, v in effects if k in ('set_oob', 'load_oob', 'set_air_oob', 'set_naval_oob')]
            rosters = [roster(name, tag, province_owner, state_owner) for name in refs]
            cases.append({'bba': bba, 'mtg': mtg, 'rosters': rosters,
                'technology': sorted({t for k, _, body in effects if k == 'set_technology' for t, _, v in body if v == '1'}),
                'divisions': sum(r.get('divisions', 0) for r in rosters), 'planes': sum(sum(r.get('aircraft', {}).values()) for r in rosters),
                'ships': sum(r.get('ships', 0) for r in rosters), 'errors': [r for r in rosters if 'error' in r]})
        later = sorted({m[1].strip('"') for path in list((MOD / 'events').glob('*.txt')) + list((MOD / 'common/on_actions').glob('*.txt'))
            for m in re.findall(r'\b(load_oob|set_oob|set_air_oob|set_naval_oob)\s*=\s*("[^"]+"|\w+)', path.read_text(encoding='utf-8-sig')) if m[1].strip('"').startswith(tag + '_')})
        other_contexts = []
        if tag == 'FAT':
            for case in cases:
                dlcs = ({'By Blood Alone'} if case['bba'] else set()) | ({'Man the Guns'} if case['mtg'] else set())
                effects = list(selected(history, dlcs, tag, human_tags=('BLK',)))
                refs = [v.strip('"') for k, _, v in effects if k in ('set_oob', 'load_oob', 'set_air_oob', 'set_naval_oob')]
                rosters = [roster(name, tag, province_owner, state_owner) for name in refs]
                other_contexts.append({'context': 'BLK controlled by human', 'bba': case['bba'], 'mtg': case['mtg'],
                    'rosters': rosters, 'divisions': sum(r.get('divisions', 0) for r in rosters)})
        rows.append({'tag': tag, 'name': existing['name'], 'classification': existing['start_classification'],
            'states': existing['owned_states'], 'land_provinces': len(owned), 'components': len(groups),
            'coastal_provinces': len(coasts), 'buildings': existing['buildings'], 'resources': existing['resources'],
            'capital': existing['capital_state'], 'cases': cases, 'later_or_startup_rosters_not_auto_granted': later,
            'other_start_contexts': other_contexts,
            'baseline_history_sha256': hashlib.sha256((MOD / existing['history']).read_bytes()).hexdigest()})
    return {'schema': 1, 'evidence': 'Actual country histories and selected OOBs; source-only, not native execution',
        'base': '60ec3a6', 'countries': rows, 'active': sum(r['classification'] == 'active' for r in rows),
        'active_industry_empty': [r['tag'] for r in rows if r['classification'] == 'active' and not sum(r['buildings'].get(k, 0) for k in ('industrial_complex', 'arms_factory', 'dockyard'))]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--output', type=Path); args = parser.parse_args()
    report = inspect()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Active starts:', report['active'], '; industry-empty:', len(report['active_industry_empty']))
