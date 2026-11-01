"""Actual selected OOB personnel versus retained core population and start laws.

This is source arithmetic, not native mobilization timing or a manpower grant.
Non-core recruitment, future growth, weekly manpower and unexecuted policies
are excluded. Existing army debt is exposed, never removed by this inspector.
"""
import argparse
from collections import Counter
import json
import hashlib
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools/usea_expansion'), str(HERE)]
from script import parse, get, walk
from inventory import selected
from capabilities import divisions, dlc_cases, case_key
from policies import capture as capture_policies, history_signature
from technical import Engine


def read_tree(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


def read_source(relative):
    return (MOD / relative).read_text(encoding='utf-8-sig')


def report(reference=None):
    profiles = json.loads((HERE / 'profiles.json').read_text())['countries']
    manifest = json.loads((HERE / 'foundation.json').read_text())
    for relative, expected in manifest['primary_sources_sha256'].items():
        if relative.startswith('mod/') and hashlib.sha256((MOD / relative[4:]).read_bytes()).hexdigest() != expected:
            raise ValueError('Effective modifier/technical source changed; explicit recapture required: ' + relative)
    engine = Engine(reference) if reference else None
    output = {}
    for tag, p in profiles.items():
        row = manifest['countries'][tag]; core = other = 0
        for ident, baseline in row['baseline'].items():
            state = get(read_tree(baseline['path']), 'state'); history = get(state, 'history')
            if get(history, 'owner') != tag: raise ValueError('Personnel ownership changed: ' + tag)
            cores = [v for k, _, v in history if k == 'add_core_of']
            population = int(get(state, 'manpower'))
            if tag in cores: core += population
            else: other += population
        history_source = read_source(row['country_history'])
        policy = capture_policies(history_source, tag, engine) if engine else row['opening_policies']
        if engine and policy != row['opening_policies']:
            raise ValueError('Captured start policies differ from actual history: ' + tag)
        modifiers = policy['modifiers']
        rate = max(0, modifiers.get('conscription', 0))
        factor = max(0, 1 + modifiers.get('conscription_factor', 0))
        pool = math.floor(core * rate * factor)
        cases = []
        for bba, mtg, nsb in dlc_cases(p):
            dlcs = ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set()) | ({'No Step Back'} if nsb else set())
            key = case_key(bba, mtg, nsb); contracts = row['recipe_contracts'][key]
            effects = list(selected(parse(history_source), dlcs, tag)); variants = {}
            if history_signature(history_source, tag, dlcs) != policy['history_policy_signature']:
                raise ValueError('Changed or DLC-dependent history policy needs explicit recapture: ' + tag)
            for kind, _, body in effects:
                if kind == 'create_equipment_variant':
                    variants[get(body, 'name')] = (get(body, 'type'), {k: v for k, _, v in get(body, 'modules', [])})
                if kind in ('add_manpower', 'set_manpower'):
                    raise ValueError('Explicit initial manpower effect needs separate audited semantics: ' + tag)
            def crew(equipment, version):
                if version:
                    defined, modules = variants[version]
                    if defined != equipment: raise ValueError('Personnel variant equipment mismatch')
                    choices = [c for c in contracts.values() if c['equipment'] == equipment and c['modules'] == modules]
                else:
                    choices = [c for c in contracts.values() if c['equipment'] == equipment and not c['modules']]
                if not choices: raise ValueError('No primary crew contract for actual equipment: ' + tag + ':' + equipment)
                values = {c['stats']['manpower'] for c in choices}
                if len(values) != 1: raise ValueError('Ambiguous primary crew contract')
                return values.pop()
            land = air = naval = 0
            formation_count = plane_count = ship_count = 0
            for kind, _, name in effects:
                if kind not in ('set_oob', 'load_oob', 'set_air_oob', 'set_naval_oob'): continue
                tree = read_tree('history/units/' + name.strip('"') + '.txt')
                templates = {}
                for node, _, values in tree:
                    if node != 'division_template': continue
                    label = get(values, 'name')
                    if label in templates: raise ValueError('Duplicate personnel template: ' + tag)
                    templates[label] = sum(float(row['unit_contracts'][unit]['manpower']) for unit, _, _ in get(values, 'regiments', []) + get(values, 'support', []))
                for division in divisions(tree):
                    land += templates[get(division, 'division_template')]; formation_count += 1
                for node, values in walk(tree):
                    if node == 'air_wings':
                        for _, _, wings in values:
                            for equipment, _, body in wings:
                                count = int(get(body, 'amount')); plane_count += count
                                air += count * crew(equipment, get(body, 'version_name'))
                    elif node == 'ship':
                        for equipment, _, body in get(values, 'equipment'):
                            count = int(get(body, 'amount', '1')); ship_count += count
                            naval += count * crew(equipment, get(body, 'version_name'))
            deployed = math.ceil(land + air + naval)
            reserve = math.ceil(deployed * p['replacement_personnel_reserve_fraction'])
            cases.append(dict(bba=bba, mtg=mtg, nsb=nsb, formations=formation_count, aircraft=plane_count, ships=ship_count,
                land_personnel=land, air_personnel=air, naval_personnel=naval, deployed_personnel=deployed,
                replacement_reserve=reserve, pool_after_deployment_and_reserve=pool-deployed-reserve))
        deficient = min(case['pool_after_deployment_and_reserve'] for case in cases) < 0
        declared = p.get('inherited_personnel_debt')
        if declared and p['mode'] != 'retained_start': raise ValueError('A new army cannot waive manpower debt: ' + tag)
        status = 'inherited_reinforcement_debt' if deficient and declared else 'unapproved_personnel_deficit' if deficient else 'source_budget_pass'
        if declared and not deficient: raise ValueError('Stale inherited personnel debt declaration: ' + tag)
        output[tag] = dict(core_population=core, non_core_population_excluded=other, law=policy['laws'].get('mobilization_laws'),
            conscription=rate, conscription_factor=factor-1, core_recruitable_pool_lower=pool,
            reserve_fraction=p['replacement_personnel_reserve_fraction'], status=status,
            inherited_debt=declared, cases=cases)
    counts = Counter(r['status'] for r in output.values())
    return dict(schema=1, universal_sustainable_start_acceptance=False,
                known_source_liabilities=[tag for tag, row in output.items() if row['status'] != 'source_budget_pass'],
                coverage='Actual selected history/OOBs, primary unit/equipment personnel, retained core population and literal history law/idea modifiers. Native mobilization and reinforcement delivery remain pending.',
                summary=dict(counts), countries=output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--reference', type=Path); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    result = report(args.reference); text = json.dumps(result, indent=2) + '\n'; path = HERE / 'personnel.json'
    if result['summary'].get('unapproved_personnel_deficit'): raise SystemExit('Unapproved personnel deficit: inspect the actual force/law source')
    if args.check:
        if not path.exists() or path.read_text() != text: raise SystemExit('Actual personnel worksheet differs')
    else:
        path.write_text(text, encoding='utf-8', newline='\n')
    print('Actual personnel source budget:', result['summary'])
