"""Actual-script active-start regressions; no native game or save emulation."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compile as compiler
from placement import derive, topology
from inventory import selected, condition
from technical import Engine
from capabilities import AIR, NAVY, equipment_for, design_for
from worksheet import report
from script import parse, get, walk

ROOT = compiler.ROOT; MOD = compiler.MOD
parser = argparse.ArgumentParser(); parser.add_argument('--reference', type=Path); args, remainder = parser.parse_known_args()
REF = args.reference
MANIFEST = json.loads((HERE / 'foundation.json').read_text())
PROFILES = json.loads((HERE / 'profiles.json').read_text())['countries']
BASELINE = json.loads((HERE / 'baseline_inventory.json').read_text())


def read(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


def cases():
    for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
        yield bba, mtg, ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set())


class ActiveWorldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defs, cls.graph, _, _, _ = topology()

    def test_all61_intake_and_excluded_release_contracts_are_explicit(self):
        self.assertEqual(BASELINE['active'], 61)
        self.assertEqual(len(BASELINE['active_industry_empty']), 25)
        self.assertEqual(len({r['tag'] for r in BASELINE['countries']}), 69)
        self.assertEqual({r['tag'] for r in BASELINE['countries'] if r['classification'] == 'emergent'},
                         {'AWW', 'REC', 'REL', 'SBK', 'SER', 'SHI', 'TER'})
        self.assertNotIn('PLH', PROFILES)
        for tag in PROFILES:
            self.assertEqual(next(r for r in BASELINE['countries'] if r['tag'] == tag)['classification'], 'active')

    def test_real_generators_and_captured_primary_contracts_reproduce_without_game(self):
        self.assertEqual(derive(None), MANIFEST)
        for relative, text in compiler.outputs().items():
            self.assertEqual((MOD / relative).read_text(encoding='utf-8'), text, relative)
        self.assertEqual(report(), json.loads((HERE / 'sustainment.json').read_text()))
        for tag, row in MANIFEST['countries'].items():
            self.assertEqual(row['profile_sha256'], hashlib.sha256(json.dumps(PROFILES[tag], sort_keys=True).encode()).hexdigest())

    def test_individual_inherited_buildings_resources_identity_and_vps_do_not_fall(self):
        capacity = {'town': 4, 'large_town': 5, 'city': 6, 'large_city': 8, 'metropolis': 10, 'megalopolis': 12}
        for tag, row in MANIFEST['countries'].items():
            totals = Counter()
            for ident, old in row['baseline'].items():
                state = get(read(old['path']), 'state'); history = get(state, 'history'); buildings = get(history, 'buildings')
                self.assertEqual(get(history, 'owner'), old['owner'])
                self.assertEqual([v for k, _, v in history if k == 'add_core_of'], old['cores'])
                self.assertEqual(int(get(state, 'manpower')), old['manpower'])
                self.assertEqual([int(k) for k, _, _ in get(state, 'provinces')], old['provinces'])
                self.assertNotEqual(int(ident), 171)
                for key, field in [('civilian', 'industrial_complex'), ('military', 'arms_factory'), ('dockyard', 'dockyard'),
                                   ('air_base', 'air_base'), ('infrastructure', 'infrastructure'), ('fuel_silo', 'fuel_silo')]:
                    amount = int(get(buildings, field, '0'))
                    self.assertGreaterEqual(amount, old['buildings'][key]); totals[key] += amount
                slots = sum(int(get(buildings, key, '0')) for key in ('industrial_complex', 'arms_factory', 'dockyard', 'fuel_silo'))
                self.assertLessEqual(slots, capacity[get(state, 'state_category')] * float(get(state, 'buildings_max_level_factor', '1')))
                resources = {k: float(v) for k, _, v in get(state, 'resources')}
                for resource, value in old['resources'].items():
                    self.assertGreaterEqual(resources[resource], float(value))
                for p, amount in old['ports'].items():
                    self.assertEqual(int(get(get(buildings, p), 'naval_base')), amount)
                points = {v[0][0]: int(v[1][0]) for k, _, v in history if k == 'victory_points'}
                for p, value in old['victory_points'].items():
                    self.assertEqual(points[p], value)
            self.assertEqual({k: totals[k] for k in PROFILES[tag]['target_industry']}, PROFILES[tag]['target_industry'])

    def test_owned_components_ports_spawn_positions_and_no_water_rails(self):
        building_rows = [r.split(';') for r in (MOD / 'map/buildings.txt').read_text().splitlines() if ';' in r]
        spawns = {(int(r[0]), int(r[6])) for r in building_rows if r[1] == 'naval_base_spawn'}
        for tag, row in MANIFEST['countries'].items():
            self.assertEqual(sum(len(c['provinces']) for c in row['components']), len(row['provinces']))
            for component in row['components']:
                owned = set(component['provinces']); reached = {component['root']}
                for route in component['routes']:
                    self.assertEqual(route[0], component['root']); self.assertTrue(set(route) <= owned)
                    for p, q in zip(route, route[1:]):
                        self.assertIn(q, self.graph[p]); self.assertTrue(self.defs[p]['land'] and self.defs[q]['land'])
                    reached.update(route)
                self.assertTrue(set(component['terminals']) <= reached)
                if component['index']:
                    self.assertTrue(component['ports']); self.assertIn(component['root'], component['ports'])
            for port in row['ports']:
                p = port['province']; self.assertIn(p, row['provinces']); self.assertTrue(self.defs[p]['coastal'])
                self.assertTrue(any(self.defs[n]['kind'] == 'sea' and (port['state'], n) in spawns for n in self.graph[p]))
            self.assertEqual(row['routes'], [r for c in row['components'] for r in c['routes']])
            self.assertTrue(set(row['land_deployments']) <= set(row['all_supply_hubs']))

    def test_fcu_landlocked_capital_is_not_replaced_with_a_fictional_coast(self):
        if 'FCU' not in MANIFEST['countries']:
            self.skipTest('FCU owned by another foundation slice')
        row = MANIFEST['countries']['FCU']; component = next(c for c in row['components'] if row['capital_province'] in c['provinces'])
        self.assertFalse(component['ports']); self.assertEqual(row['capital'], 478)
        self.assertEqual(set(row['naval_access_note']['existing_faction_members']), {'AMB', 'UGE', 'SNS', 'DEL'})
        for partner in row['naval_access_note']['existing_faction_members']:
            self.assertIn('add_to_faction = ' + partner, row['country_history_source'])

    def test_four_real_dlc_branches_load_once_and_assign_exact_factory_roles(self):
        for tag, row in MANIFEST['countries'].items():
            p = PROFILES[tag]; results = []
            for bba, mtg, dlcs in cases():
                effects = list(selected(read(row['country_history']), dlcs, tag))
                refs = [v.strip('"') for k, _, v in effects if k in ('set_oob', 'load_oob', 'set_air_oob', 'set_naval_oob')]
                self.assertEqual(len(refs), 3); self.assertEqual(len(set(refs)), 3)
                divisions = planes = ships = 0; assigned = Counter(); actual_types = Counter()
                for name in refs:
                    roster = read('history/units/' + name + '.txt')
                    for key, body in walk(roster):
                        if key == 'division':
                            divisions += 1; self.assertIn(int(get(body, 'location')), row['all_supply_hubs'])
                            self.assertEqual(get(body, 'start_equipment_factor'), '1.0')
                        elif key == 'ship':
                            ships += 1; actual_types[get(body, 'definition')] += 1
                        elif key == 'add_equipment_production':
                            eq = get(body, 'equipment'); kind = get(eq, 'type'); version = get(eq, 'version_name')
                            roles = [role for role in {**p['production'], **p['naval_production']} if equipment_for(role, bba, mtg) == kind and
                                ((not design_for(role, bba, mtg) and not version) or version == '"' + tag + ' ' + design_for(role, bba, mtg)['label'] + '"')]
                            self.assertEqual(len(roles), 1, (kind, version)); assigned[roles[0]] += int(get(body, 'requested_factories'))
                            self.assertEqual(get(eq, 'creator'), tag); self.assertEqual(get(body, 'efficiency'), '50')
                    for state, _, wings in get(roster, 'air_wings', []):
                        count = sum(int(get(body, 'amount')) for _, _, body in wings); planes += count
                        self.assertLessEqual(count, row['placements'][state]['air_base'] * 200)
                self.assertEqual(dict(assigned), {**p['production'], **p['naval_production']})
                self.assertEqual(dict(actual_types), p['navy'])
                results.append((divisions, planes, ships))
                self.assertEqual(get(effects, 'set_convoys'), str(p['convoys']))
                self.assertEqual(get(effects, 'set_fuel_ratio'), '1.0')
            self.assertEqual(len(set(results)), 1)
            self.assertEqual(results[0], (sum(p['formations'].values()), sum(p['air'].values()), sum(p['navy'].values())))

    def test_actual_variant_stock_and_roster_bindings_follow_real_unlock_sequence(self):
        engine = Engine(REF) if REF else None
        for tag, row in MANIFEST['countries'].items():
            for bba, mtg, dlcs in cases():
                key = f'bba{int(bba)}_mtg{int(mtg)}'; tech = set(); variants = {}
                for name, _, body in selected(read(row['country_history']), dlcs, tag):
                    if name == 'set_technology':
                        tech.update(k for k, _, v in body if v == '1')
                    elif name == 'create_equipment_variant':
                        ident = get(body, 'name'); equipment = get(body, 'type'); modules = {k: v for k, _, v in get(body, 'modules')}
                        roles = [r for r, c in row['recipe_contracts'][key].items() if c['equipment'] == equipment and c['modules'] == modules]
                        self.assertTrue(roles, ident)
                        contract = row['recipe_contracts'][key][roles[0]]
                        self.assertIn(contract['equipment_technology'], tech)
                        self.assertTrue(set(contract['module_technologies'].values()) <= tech)
                        variants[ident] = equipment
                    elif name == 'add_equipment_to_stockpile':
                        ident = get(body, 'type'); variant = get(body, 'variant_name')
                        if variant:
                            self.assertEqual(variants[variant], ident)
                        else:
                            self.assertIn(ident, row['gear_archetypes'] | {AIR[r]['legacy']: '' for r in PROFILES[tag]['air']})
                    elif name in ('set_oob', 'set_air_oob', 'set_naval_oob'):
                        roster = read('history/units/' + body.strip('"') + '.txt')
                        for _, _, wings in get(roster, 'air_wings', []):
                            for equipment, _, details in wings:
                                if get(details, 'version_name'):
                                    self.assertEqual(variants[get(details, 'version_name')], equipment)
                        for node, values in walk(roster):
                            if node == 'equipment' and not get(values, 'type'):
                                for equipment, _, details in values:
                                    if get(details, 'version_name'):
                                        self.assertEqual(variants[get(details, 'version_name')], equipment)
                self.assertTrue(set(row['starting_tech'][key]) <= tech)
                if engine:
                    enabled = {'convoy_1'}; modules = set()
                    for t in tech:
                        self.assertIn(t, engine.tech)
                        for section, _, entries in engine.tech[t]:
                            if section == 'enable_equipments': enabled.update(k for k, _, _ in entries)
                            if section == 'enable_equipment_modules': modules.update(k for k, _, _ in entries)
                    for contract in row['recipe_contracts'][key].values():
                        self.assertIn(contract['equipment'], enabled)
                        self.assertTrue(set(contract['modules'].values()) <= modules)

    def test_actual_equipment_needs_have_owned_production_and_replacement_stock(self):
        for tag, row in MANIFEST['countries'].items():
            p = PROFILES[tag]; gear = row['gear_archetypes']; produced = {gear[k] for k in p['production'] if k in gear}
            tree = read(f'history/units/{tag}_ws_land.txt')
            for key, _, template in tree:
                if key != 'division_template': continue
                for subunit, _, _ in get(template, 'regiments') + get(template, 'support'):
                    for need, _, amount in row['unit_contracts'][subunit]['need']:
                        self.assertIn(need, produced, (tag, subunit, need))
                        self.assertTrue(any(gear[k] == need and n > 0 for k, n in p['stocks'].items()))
            history = list(selected(read(row['country_history']), {'By Blood Alone', 'Man the Guns'}, tag))
            stocks = {get(v, 'type'): int(get(v, 'amount')) for k, _, v in history if k == 'add_equipment_to_stockpile'}
            for kind, amount in p['stocks'].items(): self.assertEqual(stocks[kind], amount)

    def test_input_margins_import_constraints_and_army_fuel_uncertainty_are_explicit(self):
        worksheet = report(REF) if REF else report()
        for tag, country in worksheet['countries'].items():
            for case in country['cases']:
                self.assertTrue(all(v >= 0 for v in case['domestic_industrial_margins'].values()))
                if any(k != 'infantry' and n for k, n in PROFILES[tag]['formations'].items()):
                    self.assertGreater(case['daily_army_per_subunit_equipment_stat_proxy'], 0)
                    self.assertGreater(case['daily_army_literal_equipment_sum_stress_scenario'], case['daily_army_per_subunit_equipment_stat_proxy'])
            self.assertTrue(any('aggregation is unverified' in text for text in country['limits']))
        self.assertTrue(any(c['full_operation_proxy_oil_import_units'] > 0 for c in worksheet['countries']['YUK']['cases']))

    def test_new_campaign_only_identity_faction_and_disabled_fiscal_compatibility(self):
        for tag, row in MANIFEST['countries'].items():
            before = parse(row['country_history_source']); after = read(row['country_history'])
            for key in ('capital', 'recruit_character', 'set_party_name', 'set_popularities', 'add_ideas', 'create_faction', 'add_to_faction'):
                self.assertEqual([v for k, _, v in before if k == key], [v for k, _, v in after if k == key], (tag, key))
            for prefix in ('common/on_actions', 'events', 'common/scripted_effects'):
                for path in (MOD / prefix).glob('*.txt'):
                    self.assertNotIn(tag + '_ws_land', path.read_text(encoding='utf-8-sig'))
            text = (MOD / row['country_history']).read_text()
            self.assertNotIn('ac_econ_try', text); self.assertNotIn('ac_macro_try', text)
        for old in BASELINE['countries']:
            if old['tag'] in PROFILES or old['tag'] in {'BLK', 'OSE', 'SAP', 'FAT'}: continue
            path = next((MOD / 'history/countries').glob(old['tag'] + ' - *.txt'))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), old['baseline_history_sha256'], old['tag'])

    def test_ai_roles_and_targets_are_current_and_original_tag_scoped(self):
        for tag, profile in PROFILES.items():
            strategies = read(f'common/ai_strategy/{tag}_world_start.txt')
            for _, _, strategy in strategies:
                self.assertEqual(get(get(strategy, 'allowed'), 'tag'), tag)
                self.assertEqual(get(get(strategy, 'allowed'), 'original_tag'), tag)
                self.assertIn(tag + '_ws_foundation', (MOD / f'common/ai_strategy/{tag}_world_start.txt').read_text())
            templates = read(f'common/ai_templates/{tag}_world_start.txt')
            self.assertEqual(len(templates), sum(n > 0 for n in profile['formations'].values()))
            text = (MOD / f'common/ai_strategy/{tag}_world_start.txt').read_text()
            self.assertNotIn('declare_war_on', text); self.assertNotIn('conquer', text)

    def test_fiscal_marker_rejects_hidden_effects_and_preserves_valid_owner(self):
        with tempfile.TemporaryDirectory() as temp:
            for tag, row in MANIFEST['countries'].items():
                path = Path(temp) / row['country_history']; path.parent.mkdir(parents=True, exist_ok=True)
                source = (MOD / row['country_history']).read_text(); path.write_text(source)
                with patch.object(compiler, 'MOD', Path(temp)):
                    self.assertEqual(compiler.country_output(tag, row, PROFILES[tag]), source)
                    path.write_text(source.replace('set_country_flag = ac_macro_history_eligible', 'add_political_power = 999\nset_country_flag = ac_macro_history_eligible'))
                    with self.assertRaisesRegex(ValueError, 'Unexpected fiscal'):
                        compiler.country_output(tag, row, PROFILES[tag])

    @unittest.skipUnless(REF, 'No read-only installed primary reference supplied')
    def test_actual_primary_contract_recapture_matches_committed_metadata(self):
        self.assertEqual(derive(REF), MANIFEST)
        self.assertEqual(compiler.outputs(REF), compiler.outputs())
        self.assertEqual(report(REF), report())


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]] + remainder, verbosity=2)
