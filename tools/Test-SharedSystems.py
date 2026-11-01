"""Execute both real P1 owners together; no fiscal or quote substitute.

The adapter only supplies political observations/effects absent from the macro
interpreter. All commitment, quote, calendar and financial arithmetic runs from
the generated mod source. Decimal execution is not native numeric acceptance.
"""
import copy
from decimal import Decimal as D, ROUND_DOWN
import importlib.util
import json
from pathlib import Path
import sys
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/economy_v2')]
from economy_script import parse, fields
from harness import World as FiscalWorld, Country


class World(FiscalWorld):
    def __init__(self, mode='full', new=True):
        super().__init__(mode, new)
        for folder, library in [('scripted_effects', self.effects), ('scripted_triggers', self.triggers)]:
            source = parse((MOD / 'common' / folder / 'ac_politics.txt').read_text(encoding='utf-8-sig'))
            for key, _, value in source:
                if key in library: raise AssertionError('Conflicting real owner ' + key)
                library[key] = value
        for row in json.loads((ROOT / 'tools/institutions/profiles.json').read_text()):
            c = self.countries[row['tag']]
            c.original_tag = c.tag; c.government = row['inherited_party']; c.pp = D(300); c.ideas = set()
        self.political_actions = fields(parse((MOD / 'common/on_actions/ac_politics.txt').read_text()))['on_actions']

    def number(self, value, context, temp, root, previous):
        if value.startswith('ac_pol_'):
            return temp.get(value, context.variables.get(value, D(0)))
        return super().number(value, context, temp, root, previous)

    def trigger(self, nodes, context, temp=None, root=None, previous=None):
        answers = []
        for key, op, value in nodes:
            if key == 'original_tag': answer = context.original_tag == value
            elif key == 'has_government': answer = context.government == value
            elif key == 'political_power':
                answer = {'>=': context.pp >= D(value), '>': context.pp > D(value), '=': context.pp == D(value)}[op]
            elif key == 'has_idea': answer = value in context.ideas
            else: answer = super().trigger([(key, op, value)], context, temp, root, previous)
            answers.append(answer)
        return all(answers)

    def execute(self, nodes, context, temp=None, root=None, previous=None):
        temp = {} if temp is None else temp; root = context if root is None else root; branch = None
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': branch = False
                elif branch is None: raise AssertionError('Orphaned branch')
                condition = key == 'else' or self.trigger(next(v for k, _, v in value if k == 'limit'), context, temp, root, previous)
                if not branch and condition:
                    self.execute([row for row in value if row[0] != 'limit'], context, temp, root, previous); branch = True
                continue
            branch = None
            if key in ('set_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable', 'divide_variable', 'set_temp_variable', 'multiply_temp_variable') and value[0][0].startswith('ac_pol_'):
                name, _, operand = value[0]; amount = self.number(operand, context, temp, root, previous)
                target = temp if 'temp_variable' in key else context.variables; before = target.get(name, D(0))
                if key.startswith('set_'): target[name] = amount
                elif key.startswith('add_'): target[name] = before + amount
                elif key.startswith('subtract_'): target[name] = before - amount
                elif key.startswith('divide_'): target[name] = before / amount
                else: target[name] = before * amount
            elif key == 'add_political_power': context.pp += D(value)
            elif key in ('add_ideas', 'remove_ideas'):
                (context.ideas.add if key == 'add_ideas' else context.ideas.discard)(value)
            elif key == 'add_timed_idea': context.ideas.add(fields(value)['idea'])
            else: super().execute([(key, op, value)], context, temp, root, previous)

    def initialize_both(self):
        self.action('on_startup')
        for tag in self.countries: self.run('ac_pol_initialize', tag)
        return self

    def weekly(self, tag):
        self.execute(fields(fields(self.political_actions)['on_weekly'])['effect'], self.countries[tag])


class SharedOwners(unittest.TestCase):
    def test_policy_fees_survive_coarse_literal_operand_projection(self):
        # A conservative operand-only stress model; not HOI4 numeric acceptance.
        class CoarseLiteralWorld(World):
            def number(self, value, context, temp, root, previous):
                if re.fullmatch(r'-?\d+(?:\.\d+)?', value):
                    return D(value).quantize(D('.001'), rounding=ROUND_DOWN)
                return super().number(value, context, temp, root, previous)
        for policy, numerator, denominator in [('civic',1,2000), ('district',3,10000)]:
            world = CoarseLiteralWorld().initialize_both()
            country = world.countries['SNS']
            output = country.variables['ac_macro_nominal_gdp']
            world.run('ac_pol_adopt_' + policy, 'SNS')
            applied = country.variables['ac_pol_fiscal_applied']
            self.assertGreater(applied, 0)
            self.assertEqual(output * numerator / denominator, applied)
            world.run('ac_pol_suspend_policy', 'SNS')
            self.assertEqual(0, country.variables['ac_macro_commitments_annual'])

    def test_real_commitment_quote_and_monthly_bill_without_quote_settlement(self):
        w = World().initialize_both(); c = w.countries['SNS']; control = copy.deepcopy(w)
        cash = c.variables['ac_macro_cash']; bill = c.variables['ac_macro_bill']
        w.run('ac_pol_adopt_civic', 'SNS'); applied = c.variables['ac_pol_fiscal_applied']
        self.assertEqual(D('.0005') * c.variables['ac_macro_nominal_gdp'], applied)
        self.assertLess(abs(c.variables['ac_macro_bill'] - bill - applied / 12), D('1e-20'))
        self.assertEqual(cash, c.variables['ac_macro_cash']); self.assertEqual(0, c.variables['ac_macro_settlements'])
        snapshot = copy.deepcopy(c); w.run('ac_pol_sync_fiscal', 'SNS'); self.assertEqual(snapshot, c)
        w.month('SNS'); control.month('SNS')
        # Bills settle in0.001b quanta. The exact smaller obligation remains in
        # the owner's separate milli-unit carry rather than disappearing.
        reference=control.countries['SNS'].variables
        accrued=c.variables['ac_macro_last_bill']+c.variables['ac_macro_bill_carry_milli']/1000
        baseline=reference['ac_macro_last_bill']+reference['ac_macro_bill_carry_milli']/1000
        self.assertLess(abs(accrued-baseline-applied/12),D('1e-20'))
        self.assertEqual(1, c.variables['ac_macro_settlements'])
        w.run('ac_pol_suspend_policy', 'SNS'); self.assertEqual(0, c.variables['ac_macro_commitments_annual'])

    def test_disabled_legacy_and_unmarked_old_save_keep_fiscal_accounts_untouched(self):
        for mode, new in [('disabled', True), ('experimental', True), ('full', False)]:
            w = World(mode, new).initialize_both(); c = w.countries['SNS']
            if mode == 'experimental':
                c.variables.update(ac_econ_treasury=D(23), ac_econ_debt=D(9), ac_econ_arrears=D(2))
            before = {k: v for k, v in c.variables.items() if k.startswith(('ac_macro_', 'ac_econ_'))}
            w.run('ac_pol_adopt_civic', 'SNS'); w.weekly('SNS'); w.run('ac_pol_suspend_policy', 'SNS')
            self.assertEqual(before, {k: v for k, v in c.variables.items() if k.startswith(('ac_macro_', 'ac_econ_'))})
            self.assertEqual(270, c.pp)

    def test_clone_weekly_rebinds_a_real_fiscal_account_and_never_debits_original(self):
        w = World().initialize_both(); original = w.countries['SNS']; w.run('ac_pol_adopt_civic', 'SNS')
        original_snapshot = copy.deepcopy(original); clone = copy.deepcopy(original)
        clone.tag = 'D01'; clone.identity = 900; w.countries['D01'] = clone
        for state in w.states.values():
            if state.owner == 'DEL': state.owner = state.controller = 'D01'
        w.today += 7; w.run('ac_macro_initialize', 'D01'); self.assertEqual(0, clone.variables['ac_macro_cash'])
        w.weekly('D01'); applied = clone.variables['ac_pol_fiscal_applied']
        self.assertGreater(applied, 0); self.assertEqual(applied, clone.variables['ac_macro_commitments_annual'])
        self.assertEqual(900, clone.variables['ac_pol_fiscal_identity'])
        self.assertEqual(29, clone.variables['ac_pol_capacity']); self.assertEqual(original_snapshot, original)
        snapshot = copy.deepcopy(clone); w.weekly('D01'); self.assertEqual(snapshot, clone)
        w.run('ac_pol_suspend_policy', 'D01'); self.assertEqual(0, clone.variables['ac_macro_commitments_annual'])
        self.assertEqual(original_snapshot, original)

    def test_territory_loss_defers_exact_receipt_reversal_until_owner_ready(self):
        w = World().initialize_both(); c = w.countries['SNS']; w.run('ac_pol_adopt_civic', 'SNS')
        applied = c.variables['ac_pol_fiscal_applied']; owned = [s for s in w.states.values() if s.owner == 'SNS']
        for state in owned: state.owner = state.controller = 'ERU'
        w.run('ac_pol_clear_policy', 'SNS'); w.run('ac_pol_sync_fiscal', 'SNS')
        self.assertEqual(applied, c.variables['ac_macro_commitments_annual'])
        for state in owned: state.owner = state.controller = 'SNS'
        w.run('ac_pol_sync_fiscal', 'SNS'); self.assertEqual(0, c.variables['ac_macro_commitments_annual'])
        self.assertEqual(0, c.variables['ac_pol_fiscal_applied'])


if __name__ == '__main__': unittest.main(verbosity=2)
