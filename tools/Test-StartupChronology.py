"""Actual selected startup consumers, independent of a local HOI4 installation."""
from __future__ import annotations

import json
import copy
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from economy_script import parse
from compatibility import variant_order as owner


TECH = '''technologies = {
 air_baseline = { enable_equipments = { aircraft_1 } enable_equipment_modules = { gun_1 } }
 sea_baseline = { enable_equipments = { hull_1 } enable_equipment_modules = { engine_1 } }
 land_baseline = { enable_equipments = { chassis_1 } enable_equipment_modules = { turret_1 } }
 legacy_baseline = { enable_equipments = { legacy_1 } }
}'''


def unlocks():
    result = {'equipment': {}, 'modules': {}}
    for tech, row in owner.unlock_rows(TECH).items():
        for family, identifiers in row.items():
            for identifier in identifiers:
                result[family].setdefault(identifier, set()).add(tech)
    return result


def design(kind, name, module=''):
    parts = f'type = {kind} name = "{name}"'
    if module:
        parts += f' modules = {{ slot = {module} }}'
    return 'create_equipment_variant = { ' + parts + ' }'


AIR = 'air_wings = { 1 = { aircraft_1 = { amount = 1 creator = AAA version_name = "Patrol" } } }'
SEA = 'units = { fleet = { task_force = { ship = { equipment = { hull_1 = { creator = AAA version_name = "Escort" } } } } } }'
LAND = 'add_equipment_production = { equipment = { type = chassis_1 creator = AAA version_name = "Service" } requested_factories = 1 }'


class StartupChronology(unittest.TestCase):
    def inspect(self, history, units=None, dlcs=(), ai=None):
        units = {'air': AIR, 'sea': SEA, 'land': LAND, **(units or {})}
        return owner.inspect_history('AAA', parse(history), lambda name: parse(units[name]),
            unlocks(), {'convoy_1'}, set(dlcs), ai or {'AAA': False, 'BBB': True}, {'AAA', 'BBB'})

    def test_independent_air_then_naval_declarations_precede_own_consumer(self):
        history = 'set_technology = { air_baseline = 1 } ' + design('aircraft_1', 'Patrol', 'gun_1')
        history += ' set_air_oob = air set_technology = { sea_baseline = 1 } '
        history += design('hull_1', 'Escort', 'engine_1') + ' set_naval_oob = sea'
        result = self.inspect(history)
        self.assertEqual([], result['errors'])
        self.assertEqual(2, result['explicit_equipment_uses'])

    def test_moving_actual_used_design_after_air_consumer_fails(self):
        result = self.inspect('set_technology = { air_baseline = 1 } set_air_oob = air ' + design('aircraft_1', 'Patrol'))
        self.assertTrue(any('before its selected declaration' in row for row in result['errors']))

    def test_land_oob_production_requires_actual_prior_design_and_research(self):
        result = self.inspect('set_oob = land set_technology = { land_baseline = 1 } ' + design('chassis_1', 'Service'))
        self.assertEqual(2, len(result['errors']))
        self.assertTrue(all(row.startswith('land:production:') for row in result['errors']))
        self.assertIn('before required research', result['errors'][0])
        self.assertIn('before its selected declaration', result['errors'][1])
        fixed = self.inspect('set_technology = { land_baseline = 1 } ' + design('chassis_1', 'Service') + ' set_oob = land')
        self.assertEqual([], fixed['errors'])

    def test_oob_instant_effect_selects_nsb_or_legacy_production_in_same_context(self):
        history = '''if = { limit = { has_dlc = "Synthetic Land Designer" }
            set_technology = { land_baseline = 1 } ''' + design('chassis_1', 'Service', 'turret_1') + '''
        } else = { set_technology = { legacy_baseline = 1 } }
        set_oob = conditional_land'''
        oob = '''instant_effect = { if = { limit = { has_dlc = "Synthetic Land Designer" }
        ''' + LAND + ''' else = { add_equipment_production = {
            equipment = { type = legacy_1 creator = AAA } requested_factories = 1
        } } } }'''
        for dlcs in ((), ('Synthetic Land Designer',)):
            result = self.inspect(history, {'conditional_land': oob}, dlcs)
            self.assertEqual([], result['errors'])
            self.assertEqual(1, result['explicit_equipment_uses'])
            # A real movement before the selected unlock and declaration must
            # fail; the inactive sibling's needs must not contribute errors.
            moved = 'set_oob = conditional_land ' + history.replace('set_oob = conditional_land', '')
            errors = self.inspect(moved, {'conditional_land': oob}, dlcs)['errors']
            self.assertTrue(errors)
            if dlcs:
                self.assertTrue(any('before its selected declaration' in row for row in errors))
                self.assertTrue(all('legacy_1' not in row for row in errors))
            else:
                self.assertEqual(1, len(errors))
                self.assertIn('legacy_1', errors[0])

    def test_oob_instant_flags_persist_and_unknown_oob_selector_fails(self):
        history = 'set_technology = { land_baseline = 1 } ' + design('chassis_1', 'Service')
        history += ' set_oob = flag_land if = { limit = { has_country_flag = oob_seen } set_oob = land }'
        result = self.inspect(history, {'flag_land': 'instant_effect = { set_country_flag = oob_seen }'})
        self.assertEqual(1, result['explicit_equipment_uses'])
        with self.assertRaisesRegex(ValueError, 'Unsupported startup selector'):
            self.inspect('set_oob = unknown', {'unknown': 'instant_effect = { if = { limit = { unavailable_telemetry = yes } ' + LAND + ' } }'})

    def test_stockpile_and_country_production_check_their_actual_point_of_use(self):
        history = 'set_technology = { land_baseline = 1 } '
        history += 'add_equipment_to_stockpile = { type = chassis_1 variant_name = "Service" producer = AAA amount = 1 } '
        history += LAND + ' ' + design('chassis_1', 'Service')
        errors = self.inspect(history)['errors']
        self.assertEqual(2, len(errors))
        self.assertTrue(errors[0].startswith('country stockpile:'))
        self.assertTrue(errors[1].startswith('country production:'))

    def test_research_required_at_use_not_at_unused_declaration(self):
        history = design('aircraft_1', 'Patrol', 'gun_1') + ' set_technology = { air_baseline = 1 } set_air_oob = air '
        history += design('unrelated_future_hull', 'Unconsumed Design', 'future_module')
        self.assertEqual([], self.inspect(history)['errors'])
        missing = self.inspect(design('aircraft_1', 'Patrol', 'gun_1') + ' set_air_oob = air set_technology = { air_baseline = 1 }')
        self.assertEqual(2, len(missing['errors']))
        self.assertTrue(all('before required research' in row for row in missing['errors']))

    def test_dlc_branches_do_not_make_inactive_designs_available(self):
        history = '''set_technology = { air_baseline = 1 legacy_baseline = 1 }
        if = { limit = { has_dlc = "Synthetic Air Designer" }
        ''' + design('aircraft_1', 'Patrol') + ' set_air_oob = air } else = { set_air_oob = legacy }'
        units = {'legacy': 'air_wings = { 1 = { legacy_1 = { amount = 1 } } }'}
        self.assertEqual([], self.inspect(history, units, ('Synthetic Air Designer',))['errors'])
        self.assertEqual([], self.inspect(history, units)['errors'])
        invalid = history + ' set_air_oob = air'
        self.assertTrue(any('before its selected declaration' in row for row in self.inspect(invalid, units)['errors']))

    def test_selected_ai_flags_and_foreign_ai_scope_have_consistent_identity(self):
        history = '''set_technology = { air_baseline = 1 }
        if = { limit = { BBB = { is_ai = yes } } set_country_flag = use_patrol }
        if = { limit = { has_country_flag = use_patrol is_ai = no }
        ''' + design('aircraft_1', 'Patrol') + ' set_air_oob = air }'
        self.assertEqual(1, self.inspect(history)['explicit_equipment_uses'])
        self.assertEqual(0, self.inspect(history, ai={'AAA': True, 'BBB': True})['explicit_equipment_uses'])
        self.assertEqual(0, self.inspect(history, ai={'AAA': False, 'BBB': False})['explicit_equipment_uses'])

    def test_nested_else_and_sibling_else_if_choose_only_one_branch(self):
        history = '''set_technology = { air_baseline = 1 }
        if = { limit = { always = no } set_air_oob = missing
            else_if = { limit = { always = no } set_air_oob = missing }
            else = { ''' + design('aircraft_1', 'Patrol') + ''' } }
        if = { limit = { always = no } set_air_oob = missing }
        else_if = { limit = { NOT = { always = no } } set_air_oob = air }
        else = { set_air_oob = missing }'''
        self.assertEqual([], self.inspect(history)['errors'])

    def test_missing_named_or_foreign_design_is_not_a_runtime_decision_exemption(self):
        errors = self.inspect('set_technology = { air_baseline = 1 } set_air_oob = air')['errors']
        self.assertTrue(any('no country-history or loaded-OOB declaration' in row for row in errors))
        foreign = AIR.replace('creator = AAA', 'creator = BBB')
        errors = self.inspect('set_technology = { air_baseline = 1 } ' + design('aircraft_1', 'Patrol') + ' set_air_oob = imported', {'imported': foreign})['errors']
        self.assertTrue(any('explicit cross-country startup proof' in row for row in errors))

    def test_unknown_selector_or_nested_military_wrapper_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported startup selector'):
            self.inspect('if = { limit = { fictional_permission = yes } set_air_oob = air }')
        errors = self.inspect('unsupported_effect = { set_air_oob = air }')['errors']
        self.assertEqual(['Unsupported nested startup military wrapper unsupported_effect'], errors)

    def test_repeated_unlock_lists_and_same_path_override_use_effective_facts(self):
        repeated = owner.unlock_rows('technologies = { base = { enable_equipment_modules = { } enable_equipment_modules = { module_0 } } }')
        self.assertEqual(['module_0'], repeated['base']['modules'])
        with tempfile.TemporaryDirectory() as scratch:
            mod = Path(scratch)
            (mod / 'common/technologies').mkdir(parents=True)
            (mod / 'common/technologies/base.txt').write_text('technologies = { mod_base = { enable_equipments = { mod_1 } } }')
            contract = {'fallback_files': {'common/technologies/base.txt': {'technologies': owner.unlock_rows(TECH)}}}
            effective = owner.catalog(mod, contract)
            self.assertEqual({'mod_base'}, effective['equipment']['mod_1'])
            self.assertNotIn('aircraft_1', effective['equipment'])

    def test_explicit_inherent_convoy_baseline_cannot_override_new_authored_lock(self):
        history = parse('add_equipment_to_stockpile = { type = convoy_1 amount = 1 }')
        result = owner.inspect_history('AAA', history, lambda _: [], unlocks(), {'convoy_1'}, set(), {'AAA': False}, {'AAA'})
        self.assertEqual([], result['errors'])
        locked = unlocks()
        locked['equipment']['convoy_1'] = {'new_convoy_lock'}
        result = owner.inspect_history('AAA', history, lambda _: [], locked, {'convoy_1'}, set(), {'AAA': False}, {'AAA'})
        self.assertTrue(any('before required research' in row for row in result['errors']))

    def test_all_selected_dlc_ai_cases_are_reported_without_native_claims(self):
        with tempfile.TemporaryDirectory() as scratch:
            mod = Path(scratch)
            for folder in ('common/technologies', 'history/countries', 'history/units'):
                (mod / folder).mkdir(parents=True)
            (mod / 'common/technologies/base.txt').write_text(TECH)
            (mod / 'history/units/land.txt').write_text(LAND)
            (mod / 'history/countries/AAA - Synthetic.txt').write_text('''if = { limit = { has_dlc = "Synthetic Land Designer" }
            set_technology = { land_baseline = 1 } ''' + design('chassis_1', 'Service') + ' set_oob = land }')
            result = owner.inspect_mod(mod, {'fallback_files': {}, 'always_available_equipment': []})
            self.assertEqual(4, len(result['cases']))
            self.assertEqual(0, result['error_count'])
            self.assertEqual(2, sum(row['explicit_equipment_uses'] for row in result['cases']))
            self.assertIn('not native', result['evidence'])

    def test_actual_amb_history_allows_independent_families_and_detects_moved_use(self):
        mod = ROOT / 'mod/2985041246'
        contract = json.loads((ROOT / 'tools/compatibility/research_contract.json').read_text())
        tree = parse(next((mod / 'history/countries').glob('AMB *')).read_text(encoding='utf-8-sig'))
        catalog = owner.catalog(mod, contract)
        reader = lambda name: parse((mod / 'history/units' / (name + '.txt')).read_text(encoding='utf-8-sig'))
        def inspect(source):
            return owner.inspect_history('AMB', source, reader, catalog, set(contract['always_available_equipment']),
                {'By Blood Alone', 'Man the Guns'}, {'AMB': False}, {'AMB'})
        self.assertEqual([], inspect(tree)['errors'])
        def naval(source):
            return next(body for kind, _, body in source if kind == 'if' and
                ('has_dlc', '=', 'Man the Guns') in owner.get(body, 'limit', []))
        late_design = copy.deepcopy(tree)
        branch = naval(late_design)
        index = next(i for i, row in enumerate(branch) if row[0] == 'create_equipment_variant')
        moved = branch.pop(index)
        branch.append(moved)
        errors = inspect(late_design)['errors']
        self.assertTrue(any('before its selected declaration' in row and 'AMB_wf_navy_mtg' in row for row in errors))
        late_research = copy.deepcopy(tree)
        branch = naval(late_research)
        index = next(i for i, row in enumerate(branch) if row[0] == 'set_technology')
        branch.append(branch.pop(index))
        errors = inspect(late_research)['errors']
        self.assertTrue(any('before required research' in row and 'AMB_wf_navy_mtg' in row for row in errors))


if __name__ == '__main__':
    unittest.main(verbosity=2)
