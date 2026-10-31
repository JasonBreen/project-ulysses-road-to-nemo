"""Primary-definition supply/input/replacement/fuel calibration, not simulation."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get
from capabilities import AIR, NAVY, equipment_for, design_for
from technical import Engine


def report(reference=None):
    engine = Engine(reference) if reference else None
    profiles = json.loads((HERE / 'profiles.json').read_text())['countries']
    manifest = json.loads((HERE / 'foundation.json').read_text()); result = {}
    defines = manifest['defines']
    if reference:
        for relative, digest in manifest['primary_sources_sha256'].items():
            layer, path = relative.split('/', 1); base = MOD if layer == 'mod' else Path(reference)
            if hashlib.sha256((base / path).read_bytes()).hexdigest() != digest:
                raise ValueError('Primary source changed; recapture explicitly before acceptance: ' + relative)
    laws = get(parse((MOD / 'common/ideas/_economic.txt').read_text()), 'ideas')
    economy = get(get(get(laws, 'economy'), 'civilian_economy'), 'modifier')
    gain = float(get(economy, 'fuel_gain_factor', '0'))
    gain += manifest['fuel_technology_gain']
    for tag, profile in profiles.items():
        row = manifest['countries'][tag]; tree = parse((MOD / f'history/units/{tag}_ws_land.txt').read_text())
        templates = {}; template_fuel = {}; template_stress = {}; template_supply = {}; template_manpower = {}
        gear_fuel = {}
        for kind in profile['stocks']:
            archetype = engine.resolve(kind, engine.equipment, engine.eq_files)['archetype'] if engine else row['gear_archetypes'][kind]
            gear_fuel[archetype] = (engine.stats(kind) if engine else row['gear_stats'][kind])['fuel_consumption']
        for key, _, body in tree:
            if key != 'division_template':
                continue
            name = get(body, 'name'); needs = Counter(); fuel = stress = supply = manpower = 0
            for subunit, _, _ in get(body, 'regiments', []) + get(body, 'support', []):
                unit = engine.unit(subunit) if engine else row['unit_contracts'][subunit]
                needs.update({k: float(v) for k, _, v in unit.get('need', [])})
                fuel_values = [gear_fuel.get(k, 0) for k, _, _ in unit.get('need', [])]
                # The primary subunit may omit fuel while its equipment uses
                # fuel. Report an explicit equipment-stat proxy, never zero
                # by omission and never a claim of verified engine aggregation.
                fuel += max([float(unit.get('fuel_consumption', 0)), *fuel_values])
                stress += sum(float(v) * gear_fuel.get(k, 0) for k, _, v in unit.get('need', []))
                supply += float(unit.get('supply_consumption', 0)); manpower += float(unit.get('manpower', 0))
            templates[name] = needs; template_fuel[name] = fuel; template_stress[name] = stress
            template_supply[name] = supply; template_manpower[name] = manpower
        land_need = Counter(); land_fuel = land_stress = land_supply = manpower = 0
        for _, _, division in get(tree, 'units', []):
            name = get(division, 'division_template'); land_need.update(templates[name])
            land_fuel += template_fuel[name]; land_supply += template_supply[name]; manpower += template_manpower[name]
            land_stress += template_stress[name]
        cases = []
        for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
            inputs = Counter(); replacements = {}; stats = {}; air_fuel = naval_fuel = 0
            for plan, naval in [(profile['production'], False), (profile['naval_production'], True)]:
                for role, amount in plan.items():
                    design = design_for(role, bba, mtg)
                    data = engine.stats(equipment_for(role, bba, mtg), design['modules'].values() if design else ()) if engine else row['recipe_contracts'][f'bba{int(bba)}_mtg{int(mtg)}'][role]['stats']
                    stats[role] = data; inputs.update({k: n * amount for k, n in data['resources'].items()})
                    speed = defines['NProduction.BASE_FACTORY_SPEED_NAV' if naval else 'NProduction.BASE_FACTORY_SPEED_MIL']
                    replacements[role] = round(30 * speed * amount * (1 if naval else .5) / data['build_cost_ic'], 4)
            for role, amount in profile['air'].items():
                air_fuel += stats[role]['fuel_consumption'] * amount
            for role, amount in profile['navy'].items():
                naval_fuel += stats[role]['fuel_consumption'] * amount
            daily_air = air_fuel * defines['NAir.FUEL_COST_MULT'] * 24
            daily_navy = naval_fuel * defines['NNavy.FUEL_COST_MULT'] * 24
            daily_army = land_fuel * defines['NMilitary.ARMY_FUEL_COST_MULT'] * 24
            income = (defines['NCountry.BASE_FUEL_GAIN'] + row['retained_industrial_inputs_conservative']['oil'] * defines['NCountry.BASE_FUEL_GAIN_PER_OIL']) * 24 * (1 + gain)
            mobile = daily_army + daily_air + daily_navy
            deficit = max(0, mobile - income)
            cases.append({'bba': bba, 'mtg': mtg, 'equipment_stats': stats,
                'resource_inputs': dict(sorted(inputs.items())),
                'domestic_industrial_margins': {k: row['retained_industrial_inputs_conservative'][k] - v for k, v in sorted(inputs.items())},
                '30_day_reference_replacements_50percent_MIL_no_output_bonus': replacements,
                'daily_reference_air_superiority_CAS_tactical': round(daily_air, 4),
                'daily_reference_whole_navy_patrol': round(daily_navy, 4),
                'daily_army_per_subunit_equipment_stat_proxy': round(daily_army, 4),
                'daily_army_literal_equipment_sum_stress_scenario': round(land_stress * defines['NMilitary.ARMY_FUEL_COST_MULT'] * 24, 4),
                'daily_full_operating_proxy_total': round(mobile, 4),
                'daily_reference_fuel_income_lower': round(income, 4),
                'full_operation_proxy_oil_import_units': math.ceil(deficit / (24 * defines['NCountry.BASE_FUEL_GAIN_PER_OIL'] * (1 + gain))),
                'daily_reference_whole_navy_combat_total': round(daily_army + daily_air + daily_navy * defines['NNavy.IN_COMBAT_FUEL_COST'], 4)})
        result[tag] = {'source_layer': 'provisional gameplay calibration using effective primary technical definitions',
            'initial_land_equipment_need': dict(sorted(land_need.items())), 'initial_land_manpower': manpower,
            'raw_template_supply_reference': round(land_supply, 4),
            'assumed_initial_laws': 'preserved default civilian_economy and export_focus; no trade agreement is invented',
            'resource_additions': row['resource_additions'], 'cases': cases,
            'limits': ['Full operating arithmetic is a sensitivity, not native mission tempo or delivery.',
                'Army fuel aggregation is unverified: proxy takes maximum needed-equipment fuel per subunit; literal count-times-stat is a separate stress scenario, not an engine formula.',
                'Primary air/naval coefficients are verified source inputs; modifiers, doctrine, terrain, damage and scheduling are excluded.',
                'Positive extraction/fuel/output technologies beyond the listed starting fuel gains are excluded.',
                'Normal eligible trade, repairs or lower tempo is needed when operational demand exceeds domestic supply.',
                'Existing faction/naval transit and actual convoy/rail throughput require separate native acceptance.']}
    return {'schema': 1, 'reference_version': manifest['reference_version'],
            'coverage': 'static primary-definition worksheets, not native throughput or sustainable combat-loss guarantees',
            'defines': defines, 'primary_sources_sha256': manifest['primary_sources_sha256'], 'countries': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--reference', type=Path); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    path = HERE / 'sustainment.json'; text = json.dumps(report(args.reference), indent=2) + '\n'
    if args.check:
        if not path.exists() or path.read_text() != text:
            raise SystemExit('Active-world sustainment worksheet differs')
    else:
        path.write_text(text, encoding='utf-8', newline='\n')
    print('Active-world primary sustainment worksheet ' + ('consistent' if args.check else 'generated'))
