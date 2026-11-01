"""Actual-source force-cost proxies and captured primary engine contracts.

The optional installed-file check verifies syntax/definition provenance only.
Synthetic observed quantities are not native telemetry, DLC activation, OOB
affordability or balance acceptance.
"""
import argparse
import copy
from decimal import Decimal as D, ROUND_DOWN
import hashlib
import json
from pathlib import Path
import sys
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools/economy_v2'), str(ROOT / 'tools/usea_expansion')]
from harness import World
from forces import DATA, observable_names
from script import parse, get

ENGINE = None


class Forces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = World(); cls.base.action('on_startup')

    def world(self):
        world = copy.deepcopy(self.base)
        return world, world.countries['SNS']

    def quote_annual(self, values):
        world, country = self.world(); country.observables.update(values)
        world.run('ac_macro_quote', 'SNS')
        return world, country, country.variables['ac_macro_upkeep'] * 12

    def near(self, expected, actual):
        self.assertLess(abs(D(str(expected)) - actual), D('1e-18'))

    def test_captured_queries_are_unique_concrete_archetypes_or_documented_roles(self):
        queries = []
        for family in DATA['armor_families']:
            queries += ['num_equipment_in_armies_k@' + ident for ident in [family['parent'], *family['children']]]
        for group in DATA['land'].values():
            queries += ['num_equipment_in_armies_k@' + ident for ident in group['archetypes']]
        for group in DATA['air_roles'].values():
            queries += ['num_deployed_planes_with_type@' + ident for ident in group['types']]
        self.assertEqual(len(queries), len(set(queries)))
        self.assertEqual(set(queries), observable_names())
        self.assertTrue(DATA['limitations'])
        self.assertTrue(all(row['path'].startswith(('engine://', 'mod://')) for row in DATA['sources']))
        self.assertEqual(['mod://common/units/equipment/zz_ac_land_equipment.txt'],
                         [row['path'] for row in DATA['sources'] if row['path'].startswith('mod://')])
        for row in DATA['sources']:
            if not row['path'].startswith('mod://'): continue
            path = MOD / row['path'].split('://', 1)[1]
            self.assertEqual(row['sha256_normalized_lf'], hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest())
            authored = {ident for ident, _, body in get(parse(path.read_text(encoding='utf-8-sig')), 'equipments')
                        if get(body, 'is_archetype') == 'yes'}
            self.assertEqual({'ac_land_sensor_equipment', 'ac_land_electronic_equipment'}, authored)
        source = (MOD / 'common/scripted_effects/ac_macro_effects.txt').read_text()
        self.assertNotIn('num_equipment@', source)
        self.assertNotIn('num_equipment_in_armies_k@light_tank_equipment', source)
        self.assertNotIn('num_deployed_planes_with_type@fighter_equipment', source)

    def test_each_land_equipment_group_changes_the_actual_quote_without_goods(self):
        cases = [({'num_equipment_in_armies_k@infantry_equipment': 1}, '.0005'),
                 ({'num_equipment_in_armies_k@motorized_equipment': 1}, '.04'),
                 ({'num_equipment_in_armies_k@mechanized_equipment': 1}, '.08'),
                 ({'num_equipment_in_armies_k@support_equipment': 1}, '.003'),
                 ({'num_equipment_in_armies_k@artillery_equipment': 1}, '.01'),
                 ({'num_equipment_in_armies_k@medium_tank_chassis': 1}, '.2')]
        for observations, expected in cases:
            world, country, annual = self.quote_annual(observations)
            self.near(expected, annual)
            self.assertFalse(country.equipment)
            self.assertEqual(0, country.variables['ac_macro_settlements'])
            self.assertEqual(0, country.variables['ac_macro_history_count'])
            country.war = True; world.run('ac_macro_quote', 'SNS')
            self.near(D(expected) * D('1.5'), country.variables['ac_macro_upkeep'] * 12)

    def test_small_upkeep_rate_survives_coarse_literal_operand_projection(self):
        # Stress only literal operand resolution, not native variable arithmetic.
        # Actual engine precision/range/rounding remains a separate native gate.
        class CoarseLiteralWorld(World):
            def number(self, value, context, temp, root, previous):
                if re.fullmatch(r'-?\d+(?:\.\d+)?', value):
                    return D(value).quantize(D('.001'), rounding=ROUND_DOWN)
                return super().number(value, context, temp, root, previous)
        world = CoarseLiteralWorld(); world.action('on_startup')
        country = world.countries['SNS']
        country.observables['num_equipment_in_armies_k@infantry_equipment'] = 1
        world.run('ac_macro_quote', 'SNS')
        self.near('.0005', country.variables['ac_macro_upkeep'] * 12)
        self.assertEqual(0, country.variables['ac_macro_settlements'])

    def test_armor_parent_and_derived_queries_do_not_double_charge_the_family(self):
        world, country, annual = self.quote_annual({
            'num_equipment_in_armies_k@medium_tank_chassis': 1,
            'num_equipment_in_armies_k@medium_tank_artillery_chassis': 1})
        self.near('.2', annual)
        self.assertEqual(1, country.variables['ac_macro_land_armor_k'])
        country.observables['num_equipment_in_armies_k@medium_tank_destroyer_chassis'] = 1
        world.run('ac_macro_quote', 'SNS')
        self.near('.4', country.variables['ac_macro_upkeep'] * 12)
        self.assertEqual(2, country.variables['ac_macro_land_armor_k'])
        # A legacy-name alias, even if a synthetic observer supplies it, is not
        # queried again alongside the captured current family.
        before = country.variables['ac_macro_upkeep']
        country.observables['num_equipment_in_armies_k@medium_tank_equipment'] = 100
        world.run('ac_macro_quote', 'SNS'); self.assertEqual(before, country.variables['ac_macro_upkeep'])

    def test_every_captured_armor_family_and_role_signal_is_consumed(self):
        for family in DATA['armor_families']:
            for ident in [family['parent'], *family['children']]:
                _, _, annual = self.quote_annual({'num_equipment_in_armies_k@' + ident: 1})
                self.near('.2', annual)
        for group in DATA['air_roles'].values():
            for ident in group['types']:
                _, _, annual = self.quote_annual({'num_deployed_planes': 1, 'num_deployed_planes_with_type@' + ident: 1})
                self.near(D('.008') + D(str(group['annual_premium'])), annual)

    def test_fighter_cas_bomber_and_transport_have_distinct_bounded_role_allowances(self):
        for role, expected in [('fighter', '.010'), ('cas', '.009'), ('tactical_bomber', '.014'),
                               ('strategic_bomber', '.018'), ('air_transport', '.012')]:
            world, country, annual = self.quote_annual({'num_deployed_planes': 1, 'num_deployed_planes_with_type@' + role: 1})
            self.near(expected, annual)
            self.assertFalse(country.equipment)
            self.assertEqual(0, country.variables['ac_macro_history_count'])
        _, _, unknown = self.quote_annual({'num_deployed_planes': 1})
        self.near('.008', unknown)

    def test_overlapping_secondary_aircraft_roles_pay_one_base_and_one_premium_pool(self):
        values = {'num_deployed_planes': 1}
        values.update({name: 1 for name in observable_names() if name.startswith('num_deployed_planes_with_type@')})
        world, country, annual = self.quote_annual(values)
        self.near('.018', annual)
        self.near('.010', country.variables['ac_macro_air_premium_annual'])
        country.observables['num_deployed_planes_with_type@strategic_bomber'] = 1000
        world.run('ac_macro_quote', 'SNS')
        self.near('.018', country.variables['ac_macro_upkeep'] * 12)
        self.assertEqual(1, country.variables['ac_macro_air_strategic'])
        # Mixed fleets are deliberately a conservative allowance, not an
        # invented per-tail partition of overlapping role observations.
        _, _, mixed = self.quote_annual({'num_deployed_planes': 2,
            'num_deployed_planes_with_type@strategic_bomber': 1,
            'num_deployed_planes_with_type@air_transport': 1})
        self.near('.026', mixed)

    def test_personnel_and_hulls_remain_separate_and_defense_cannot_evade_upkeep(self):
        world, country, annual = self.quote_annual({
            'deployed_army_manpower_k': 100, 'deployed_navy_manpower_k': 10,
            'deployed_airforce_manpower_k': 20, 'num_deployed_planes': 50,
            'num_deployed_planes_with_type@fighter': 50,
            'num_ships': 10, 'num_ships_with_type@carrier': 1,
            'num_ships_with_type@submarine': 2})
        self.near('9.94', annual)  #130*.06 +50*.01 +10*.08 +.8 +2*.02
        country.variables['ac_macro_budget_defense'] = D(0)
        world.run('ac_macro_quote', 'SNS')
        self.assertGreaterEqual(country.variables['ac_macro_spending_defense_milli'], country.variables['ac_macro_upkeep_milli'])
        before = copy.deepcopy(country.observables)
        world.month('SNS'); self.assertEqual(before, country.observables)
        self.assertFalse(country.equipment)

    def test_primary_installed_contract_snapshot_when_provided(self):
        if ENGINE is None: self.skipTest('Read-only installed reference not provided; captured contract remains testable offline')
        for row in DATA['sources']:
            authored = row['path'].startswith('mod://')
            path = (MOD if authored else ENGINE) / row['path'].split('://', 1)[1]
            data = path.read_bytes().replace(b'\r\n', b'\n') if authored else path.read_bytes()
            self.assertEqual(row['sha256_normalized_lf' if authored else 'sha256'], hashlib.sha256(data).hexdigest(), row['path'])
        document = (ENGINE / 'documentation/dynamic_variables_documentation.md').read_text()
        self.assertIn('### num_equipment_in_armies_k', document)
        self.assertIn('### num_deployed_planes_with_type', document)
        modules = (ENGINE / 'common/units/equipment/modules/00_plane_modules.txt').read_text()
        self.assertIn('add_equipment_type = cas', modules)
        archetypes = set()
        for row in DATA['sources']:
            if not row['path'].split('://', 1)[1].startswith('common/units/equipment/') or not row['path'].endswith('.txt'): continue
            base = MOD if row['path'].startswith('mod://') else ENGINE
            tree = parse((base / row['path'].split('://', 1)[1]).read_text(encoding='utf-8-sig'))
            archetypes.update(ident for ident, _, body in get(tree, 'equipments', []) if get(body, 'is_archetype') == 'yes')
            archetypes.update(ident for ident, _, _ in get(tree, 'duplicate_archetypes', []))
        for query in observable_names():
            if query.startswith('num_equipment_in_armies_k@'):
                self.assertIn(query.split('@')[1], archetypes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--engine', type=Path)
    args, remaining = parser.parse_known_args(); ENGINE = args.engine
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
