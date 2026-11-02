"""Run partner paid actions against both real P1 owners.

No fiscal readiness, payment, capacity or quotation substitute is installed.
The adapter adds only the national variable domain to the existing shared-owner
executor. Fixture completion flags isolate contract integration from the separate
chronological focus tests. This is offline Decimal execution, not native QA.
"""
import copy
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scopes import SCOPES

owner = ROOT / 'tools/Test-SharedSystems.py'
if not owner.exists():
    raise SystemExit('Actual shared-system owners must be integrated before this gate can run')
spec = importlib.util.spec_from_file_location('partners_real_p1', owner)
shared = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = shared
spec.loader.exec_module(shared)
parse, fields = shared.parse, shared.fields


class World(shared.World):
    def __init__(self, mode='full'):
        super().__init__(mode)
        for folder, library in [('scripted_effects', self.effects), ('scripted_triggers', self.triggers)]:
            path = MOD / 'common' / folder / 'ac_usean_partners.txt'
            for key, _, value in parse(path.read_text(encoding='utf-8-sig')):
                if key in library:
                    raise ValueError('Conflicting national API owner: ' + key)
                library[key] = value

    def number(self, value, context, temp, root, previous):
        if value.startswith('ac_up_'):
            return temp.get(value, context.variables.get(value, D(0)))
        return super().number(value, context, temp, root, previous)

    def execute(self, nodes, context, temp=None, root=None, previous=None):
        temp = {} if temp is None else temp
        root = context if root is None else root
        branch = None
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': branch = False
                elif branch is None: raise ValueError('Orphaned national branch')
                condition = key == 'else' or self.trigger(next(v for k, _, v in value if k == 'limit'), context, temp, root, previous)
                if not branch and condition:
                    self.execute([row for row in value if row[0] != 'limit'], context, temp, root, previous)
                    branch = True
                continue
            branch = None
            if key in ('set_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable',
                       'set_temp_variable', 'add_to_temp_variable', 'subtract_from_temp_variable', 'multiply_temp_variable') and value[0][0].startswith('ac_up_'):
                name, _, operand = value[0]
                amount = self.number(operand, context, temp, root, previous)
                target = temp if 'temp_variable' in key else context.variables
                before = target.get(name, D(0))
                if key.startswith('set_'): target[name] = amount
                elif key.startswith('add_'): target[name] = before + amount
                elif key.startswith('subtract_'): target[name] = before - amount
                else: target[name] = before * amount
            else:
                super().execute([(key, op, value)], context, temp, root, previous)


RESOURCES = {'contacts': 'ac_up_sns_contact_records', 'protection': 'ac_up_sns_protection_records',
             'slots': 'ac_up_amber_slots', 'cases': 'ac_up_del_cases'}


class RealNationalContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines = {mode: World(mode).initialize_both() for mode in ('full', 'experimental', 'disabled')}

    def ready(self, scope, mode='full'):
        world = copy.deepcopy(self.baselines[mode]); country = world.countries[scope.tag]
        country.flags['ac_up_initialized'] = None
        country.variables['ac_pol_capacity'] = D(40)
        country.variables.update(ac_up_uge_limit=D(4), ac_up_uge_used=D(0))
        for suffix in scope.requirements:
            country.flags[scope.tag + '_up_' + suffix + '_done'] = None
        for name in RESOURCES.values(): country.variables[name] = D(4)
        if mode == 'experimental':
            country.flags['ac_econ_initialized'] = None
            country.variables.update(ac_econ_treasury=D(10), ac_econ_arrears=D(0), ac_econ_debt=D(3))
        return world, country

    def test_actual_tree_selection_weights_prefer_current_national_host_to_regional(self):
        world = self.baselines['full']
        def tree(relative):
            return next(body for kind, _, body in parse((MOD/relative).read_text(encoding='utf-8-sig'))
                        if kind == 'focus_tree')
        def weight(node, country):
            rules = next(body for key, _, body in node if key == 'country')
            total = D(next(value for key, _, value in rules if key == 'factor'))
            for key, _, modifier in rules:
                if key != 'modifier':
                    continue
                conditions = [row for row in modifier if row[0] not in ('add', 'factor')]
                if world.trigger(conditions, country):
                    for field, _, value in modifier:
                        if field == 'add': total += D(value)
                        elif field == 'factor': total *= D(value)
            return total
        regional = tree('common/national_focus/ac_regional_foundation.txt')
        national = {tag: tree('common/national_focus/'+tag+'.txt') for tag in ('SNS','AMB','UGE','DEL')}
        for tag, own_tree in national.items():
            country = copy.deepcopy(world.countries[tag])
            self.assertEqual(5, weight(regional, country), tag)
            self.assertEqual(40, weight(own_tree, country), tag)
            self.assertGreater(weight(own_tree, country), weight(regional, country), tag)
            self.assertEqual([tag], [owner for owner, candidate in national.items() if weight(candidate, country)>0])
            # The actual current-tag and original-tag guards both matter. A
            # civil-war clone sharing the original identity gets no national
            # priority; neither does another identity occupying the current tag.
            country.tag = 'D01'
            self.assertEqual(0, weight(own_tree, country), (tag, 'changed current tag'))
            country.tag = tag; country.original_tag = 'ZZZ'
            self.assertEqual(0, weight(own_tree, country), (tag, 'changed original tag'))

    def test_enabled_unready_accounts_cannot_start_any_partner_programme(self):
        for scope in SCOPES:
            for mode,fault in (('full','identity'),('full','initialized'),('full','wrong_identity'),('experimental','initialized')):
                with self.subTest(scope=scope.id,mode=mode,fault=fault):
                    world,country=self.ready(scope,mode)
                    if fault=='identity':country.variables.pop('ac_macro_identity')
                    elif fault=='wrong_identity':country.variables['ac_macro_identity']=D(-1)
                    else:country.flags.pop('ac_macro_initialized'if mode=='full'else'ac_econ_initialized')
                    self.assertTrue(world.trigger([('ac_econ_enabled','=','yes')],country))
                    self.assertFalse(world.trigger([('ac_econ_ready','=','yes')],country))
                    before=copy.deepcopy(vars(country));world.run(scope.id+'_start',scope.tag)
                    self.assertEqual(before,vars(country))

    def test_all_29_scopes_pay_real_owners_once_in_each_fiscal_mode(self):
        self.assertEqual(29, len(SCOPES))
        for scope in SCOPES:
            for mode in self.baselines:
                with self.subTest(scope=scope.id, mode=mode):
                    world, country = self.ready(scope, mode)
                    before_cash = country.variables.get('ac_macro_cash', D(0))
                    before_legacy = country.variables.get('ac_econ_treasury', D(0))
                    before_pp = country.pp
                    before_financial = {k: v for k, v in country.variables.items() if k.startswith(('ac_macro_', 'ac_econ_'))}
                    world.run(scope.id + '_start', scope.tag)
                    self.assertEqual(before_pp - 25, country.pp)
                    self.assertEqual(38, country.variables['ac_pol_capacity'])
                    if mode == 'full': self.assertEqual(before_cash - D('.002'), country.variables['ac_macro_cash'])
                    elif mode == 'experimental': self.assertEqual(before_legacy - 2, country.variables['ac_econ_treasury'])
                    else: self.assertEqual(before_financial, {k: v for k, v in country.variables.items() if k.startswith(('ac_macro_', 'ac_econ_'))})
                    self.assertIn(scope.id + '_spirit', country.ideas)
                    self.assertIn('ac_up_scope_active', country.flags)
                    if scope.resource == 'occupied_slot': self.assertEqual(1, country.variables['ac_up_uge_used'])
                    else: self.assertEqual(3, country.variables[RESOURCES[scope.resource]])
                    snapshot = copy.deepcopy(country)
                    world.run(scope.id + '_start', scope.tag)
                    self.assertEqual(snapshot, country)

    def test_real_affordability_arrears_capacity_and_capitulation_block_all_scopes(self):
        for scope in SCOPES:
            for failure in ('cash', 'arrears', 'capacity', 'capitulation'):
                world, country = self.ready(scope)
                if failure == 'cash': country.variables['ac_macro_cash'] = D('.001')
                elif failure == 'arrears': country.variables['ac_macro_arrears'] = D('.001')
                elif failure == 'capacity': country.variables['ac_pol_capacity'] = D(0)
                else: country.capitulated = True
                snapshot = copy.deepcopy(country)
                world.run(scope.id + '_start', scope.tag)
                self.assertEqual(snapshot, country, (scope.id, failure))

    def test_authorization_does_not_settle_or_add_a_history_observation(self):
        for tag in ('SNS', 'AMB', 'UGE', 'DEL'):
            scope = next(row for row in SCOPES if row.tag == tag)
            world, country = self.ready(scope)
            world.run(scope.id + '_start', tag)
            self.assertEqual(0, country.variables['ac_macro_settlements'])
            self.assertEqual(0, country.variables['ac_macro_history_count'])
            for _ in range(3): world.run('ac_macro_quote', tag)
            self.assertEqual(0, country.variables['ac_macro_history_count'])
            world.month(tag)
            self.assertEqual(1, country.variables['ac_macro_history_count'])
            snapshot = copy.deepcopy(country)
            world.action('on_monthly', [tag])
            self.assertEqual(snapshot, country)


if __name__ == '__main__':
    unittest.main(verbosity=2)
