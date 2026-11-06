"""Actual-script Sotoan scenarios with the real fiscal and institution owners.

Engine event delivery, timer dispatch, input and save serialization remain native
acceptance work. Unknown executable syntax fails rather than passing silently.
"""
import copy
from decimal import Decimal as D
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(HERE))
from content import COUNTRIES
from coverage import inventory, report

spec = importlib.util.spec_from_file_location('wc_real_shared_owners', ROOT / 'tools/Test-SharedSystems.py')
shared = importlib.util.module_from_spec(spec); spec.loader.exec_module(shared)
from economy_script import parse, fields


def read(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


class World(shared.World):
    def __init__(self, mode='full', new=True):
        super().__init__(mode, new)
        for folder, library in [('scripted_triggers', self.triggers), ('scripted_effects', self.effects)]:
            for path in (MOD / 'common' / folder).glob('ac_wc_*.txt'):
                library.update(fields(parse(path.read_text(encoding='utf-8-sig'))))
        self.focuses = {}; self.decisions = {}; self.dialogues = {}; self.from_country = None
        self.wars = set(); self.queue = []
        for path in (MOD / 'common/national_focus').glob('ac_wc_*.txt'):
            for _, _, tree in parse(path.read_text()):
                self.focuses.update({fields(n)['id']: n for k, _, n in tree if k == 'focus'})
        for path in (MOD / 'common/decisions').glob('ac_wc_*.txt'):
            for _, _, category in parse(path.read_text()): self.decisions.update(fields(category))
        for path in (MOD / 'events').glob('ac_wc_*.txt'):
            self.dialogues.update({next(v for k, _, v in n if k=='id'): n for k, _, n in parse(path.read_text()) if k == 'country_event'})
        for c in self.countries.values():
            c.subject = False; c.exists = True; c.focuses = set(); c.cooldowns = {}; c.opinions = []; c.tree = 'generic_focus'
            c.active_focus = None; c.active_progress = 0; c.experience = D(0)
        self.initialize_both()

    def trigger(self, nodes, context, temp=None, root=None, previous=None):
        result = []
        for key, op, value in nodes:
            if key == 'is_subject': answer = context.subject == (value == 'yes')
            elif key == 'exists': answer = context.exists == (value == 'yes')
            elif key == 'has_completed_focus': answer = value in context.focuses
            elif key == 'has_focus_tree': answer = value == context.tree
            elif key == 'has_shine_effect_on_focus': answer = value == context.active_focus
            elif key == 'focus_progress':
                data = {k:v for k, _, v in value}
                answer = context.active_focus == data['focus'] and context.active_progress > float(data['progress'])
            elif key == 'has_war_with': answer = frozenset((context.tag, value)) in self.wars
            elif key in self.countries: answer = self.countries[key].exists and self.trigger(value, self.countries[key], temp, root, context)
            elif key == 'FROM': answer = self.from_country is not None and self.trigger(value, self.from_country, temp, root, context)
            else: answer = super().trigger([(key, op, value)], context, temp, root, previous)
            result.append(answer)
        return all(result)

    def execute(self, nodes, context, temp=None, root=None, previous=None):
        branch = None
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': branch = False
                elif branch is None: raise ValueError('Orphan branch')
                condition = key == 'else' or self.trigger(next(v for k, _, v in value if k=='limit'), context, temp, root, previous)
                if not branch and condition:
                    self.execute([row for row in value if row[0] != 'limit'], context, temp, root, previous); branch = True
                continue
            branch = None
            if key == 'FROM': self.execute(value, self.from_country, temp, root, context)
            elif key in self.countries:
                if self.countries[key].exists: self.execute(value, self.countries[key], temp, root, context)
            elif key == 'country_event': self.queue.append((context.tag, fields(value)['id'], previous.tag if previous else context.tag))
            elif key in ('army_experience', 'navy_experience', 'air_experience'): context.experience += D(value)
            elif key == 'add_opinion_modifier': context.opinions.append(fields(value))
            elif key == 'load_focus_tree': context.tree = fields(value)['tree']
            else: super().execute([(key, op, value)], context, temp, root, previous)

    def complete(self, ident, tag):
        c = self.countries[tag]; node = self.focuses[ident]
        assert ident not in c.focuses
        for key, _, body in node:
            if key == 'prerequisite': assert any(v in c.focuses for _, _, v in body)
            elif key == 'mutually_exclusive': assert not any(v in c.focuses for _, _, v in body)
        assert self.trigger(fields(node)['available'], c), ident
        c.focuses.add(ident); self.execute(fields(node)['completion_reward'], c)

    def option(self, event, tag, option, sender=None):
        self.from_country = self.countries[sender] if sender else None
        node = next(n for k, _, n in self.dialogues[event] if k == 'option' and fields(n)['name'] == option)
        assert self.trigger(fields(node).get('trigger', []), self.countries[tag]), option
        self.execute([r for r in node if r[0] not in ('name', 'trigger', 'ai_chance')], self.countries[tag])

    def decide(self, ident, tag):
        node = fields(self.decisions[ident]); c = self.countries[tag]
        assert self.today >= c.cooldowns.get(ident, 0)
        assert self.trigger(node['visible'], c) and self.trigger(node['available'], c), ident
        assert c.pp >= D(node['cost'])
        c.pp -= D(node['cost']); self.execute(node['complete_effect'], c)
        c.cooldowns[ident] = self.today + int(node['days_re_enable'])


class Campaigns(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.base = World()

    def found_government(self, w, tag, policy=0):
        key = f'{tag}_wc_e1_{COUNTRIES[tag][0].slug}'
        w.complete(key+'_open',tag); w.option('ac_wc_'+tag.lower()+'.1',tag,'ac_wc_'+tag.lower()+'.1.p'+str(policy))
        w.complete(key+f'_p{policy}_0',tag); w.complete(key+f'_p{policy}_1',tag)
        w.decide(key+'_operate',tag); w.today += 90
        w.execute(fields(w.decisions[key+'_operate'])['remove_effect'],w.countries[tag])
        w.complete(key+f'_p{policy}_2',tag)

    def test_all_96_routes_require_real_payment_and_timer_result_and_do_not_replay(self):
        for tag, chapters in COUNTRIES.items():
            for index, chapter in enumerate(chapters):
                for policy in range(3):
                    with self.subTest(tag=tag, chapter=chapter.slug, policy=policy):
                        w = copy.deepcopy(self.base); c = w.countries[tag]; key = f'{tag}_wc_e1_{chapter.slug}'
                        c.variables['ac_macro_cash'] = D(1)
                        if index > 0: self.found_government(w,tag)
                        w.complete(key+'_open', tag)
                        w.option('ac_wc_'+tag.lower()+'.'+str(index+1), tag, 'ac_wc_'+tag.lower()+'.'+str(index+1)+'.p'+str(policy))
                        w.complete(key+f'_p{policy}_0', tag); w.complete(key+f'_p{policy}_1', tag)
                        with self.assertRaises(AssertionError): w.complete(key+f'_p{policy}_2', tag)
                        pp = c.pp; cash = c.variables['ac_macro_cash']
                        w.decide(key+'_operate', tag)
                        self.assertEqual(pp-D(25), c.pp); self.assertEqual(cash-D('.02'), c.variables['ac_macro_cash'])
                        w.execute(fields(w.decisions[key+'_operate'])['complete_effect'], c)
                        self.assertEqual(cash-D('.02'), c.variables['ac_macro_cash'])
                        with self.assertRaises(AssertionError): w.decide(key+'_operate', tag)
                        w.today += 90
                        w.execute(fields(w.decisions[key+'_operate'])['remove_effect'], c)
                        self.assertIn(key+'_done', c.flags)
                        w.complete(key+f'_p{policy}_2', tag)
                        self.assertIn(tag+'_wc_'+chapter.domain+'_'+str(policy), c.ideas)
                        if index == 0:
                            self.assertIn(f'{tag}_wc_government_{policy}',c.ideas)
                            self.assertIn(f'{tag}_wc_route_{policy}',c.flags)
                        snapshot = copy.deepcopy((c.variables, c.flags, c.ideas, c.pp))
                        w.execute(fields(w.focuses[key+f'_p{policy}_2'])['completion_reward'], c)
                        w.execute(fields(w.decisions[key+'_operate'])['remove_effect'], c)
                        self.assertEqual(snapshot, (c.variables, c.flags, c.ideas, c.pp))

    def test_shortfalls_unready_accounts_and_interrupted_work_fail_closed(self):
        for failure in ('cash', 'arrears', 'unready', 'capitulation', 'territory', 'occupation'):
            w = copy.deepcopy(self.base); c = w.countries['SOA']; key = 'SOA_wc_e1_authority'
            c.variables['ac_macro_cash'] = D(1)
            w.complete(key+'_open', 'SOA'); w.option('ac_wc_soa.1', 'SOA', 'ac_wc_soa.1.p0')
            w.complete(key+'_p0_0', 'SOA'); w.complete(key+'_p0_1', 'SOA')
            if failure in ('cash', 'arrears', 'unready'):
                if failure == 'cash': c.variables['ac_macro_cash'] = D('.019')
                elif failure == 'arrears': c.variables['ac_macro_arrears'] = D(1)
                else: c.flags.pop('ac_macro_initialized')
                before = copy.deepcopy((c.variables, c.flags, c.pp))
                with self.assertRaises(AssertionError): w.decide(key+'_operate', 'SOA')
                self.assertEqual(before, (c.variables, c.flags, c.pp))
            else:
                w.decide(key+'_operate', 'SOA'); w.today += 90
                if failure == 'capitulation': c.capitulated = True
                else:
                    for state in w.states.values():
                        if state.owner == 'SOA':
                            state.controller = 'CSO'
                            if failure == 'territory': state.owner = 'CSO'
                w.execute(fields(w.decisions[key+'_operate'])['remove_effect'], c)
                self.assertNotIn(key+'_done', c.flags); self.assertIn(key+'_failed', c.flags)

    def test_disabled_and_experimental_modes_do_not_activate_or_charge_macro(self):
        for mode in ('disabled', 'experimental'):
            w = World(mode); c = w.countries['CSO']; key = 'CSO_wc_e1_voice'
            w.complete(key+'_open', 'CSO'); w.option('ac_wc_cso.1', 'CSO', 'ac_wc_cso.1.p1')
            w.complete(key+'_p1_0', 'CSO'); w.complete(key+'_p1_1', 'CSO')
            before = copy.deepcopy(c.variables)
            w.decide(key+'_operate', 'CSO')
            self.assertEqual(before, c.variables); self.assertIn(key+'_running', c.flags)

    def test_expired_services_renew_at_cost_once_and_sector_alternatives_do_not_stack(self):
        w = copy.deepcopy(self.base); c = w.countries['CSO']; key = 'CSO_wc_e1_voice'
        c.variables['ac_macro_cash'] = D(1)
        w.complete(key+'_open','CSO'); w.option('ac_wc_cso.1','CSO','ac_wc_cso.1.p1')
        w.complete(key+'_p1_0','CSO'); w.complete(key+'_p1_1','CSO')
        w.decide(key+'_operate','CSO'); w.today += 90
        w.execute(fields(w.decisions[key+'_operate'])['remove_effect'],c)
        w.complete(key+'_p1_2','CSO')
        with self.assertRaises(AssertionError): w.decide(key+'_renew','CSO')
        w.today += 365; cash = c.variables['ac_macro_cash']; pp = c.pp
        w.decide(key+'_renew','CSO')
        self.assertEqual(cash-D('.02'),c.variables['ac_macro_cash']); self.assertEqual(pp-D(25),c.pp)
        w.execute(fields(w.decisions[key+'_renew'])['complete_effect'],c)
        self.assertEqual(cash-D('.02'),c.variables['ac_macro_cash'])
        self.assertEqual({'CSO_wc_civil_1'}, {i for i in c.ideas if i.startswith('CSO_wc_civil_')})
        self.assertIn('CSO_wc_government_1',c.ideas)

    def test_expired_or_capitulated_dialogues_cannot_select_and_can_reopen(self):
        for invalid in ('expiry', 'capitulation'):
            w = copy.deepcopy(self.base); c = w.countries['SOA']; w.complete('SOA_wc_e1_authority_open', 'SOA')
            if invalid == 'expiry': w.today += 61
            else: c.capitulated = True
            with self.assertRaises(AssertionError): w.option('ac_wc_soa.1', 'SOA', 'ac_wc_soa.1.p2')
            # A stale already-visible option's effects also revalidate.
            node = next(n for k, _, n in w.dialogues['ac_wc_soa.1'] if k == 'option' and fields(n)['name'].endswith('.p2'))
            w.execute([r for r in node if r[0] not in ('name','trigger','ai_chance')], c)
            self.assertNotIn('SOA_wc_e1_authority_choice_2', c.flags)
            c.capitulated = False; w.today += 61
            w.decide('SOA_wc_e1_authority_reopen', 'SOA')
            w.option('ac_wc_soa.1', 'SOA', 'ac_wc_soa.1.p0')

    def test_bilateral_accept_refuse_expiry_subject_war_and_duplicate_replies(self):
        for result in ('accept', 'refuse', 'expiry', 'subject', 'war', 'annexed', 'capitulated'):
            w = copy.deepcopy(self.base); c = w.countries['SOA']; target = w.countries['CSO']
            c.focuses.add('SOA_wc_e1_central_p0_1')
            w.decide('SOA_wc_contact_cso', 'SOA')
            if result == 'expiry': w.today += 46
            elif result == 'subject': target.subject = True
            elif result == 'war': w.wars.add(frozenset(('SOA','CSO')))
            elif result == 'annexed': c.exists = False; c.capitulated = True
            elif result == 'capitulated': target.capitulated = True
            if result in ('accept', 'refuse'):
                w.option('ac_wc_relations.1', 'CSO', 'ac_wc_relations.1.'+result, 'SOA')
                self.assertIn('SOA_wc_contact_cso_'+('accepted' if result=='accept' else 'refused'), c.flags)
                self.assertEqual(1 if result == 'accept' else 0, len(c.opinions))
                with self.assertRaises(AssertionError): w.option('ac_wc_relations.1','CSO','ac_wc_relations.1.accept','SOA')
            else:
                with self.assertRaises(AssertionError): w.option('ac_wc_relations.1','CSO','ac_wc_relations.1.accept','SOA')
                w.option('ac_wc_relations.1','CSO','ac_wc_relations.1.close','SOA')
                self.assertFalse(c.opinions)

    def test_actual_idle_migration_preserves_completions_and_blocks_continuous_work(self):
        w = copy.deepcopy(self.base); c = w.countries['SOA']; c.focuses.add('army_effort')
        for selected in ('equipment_effort','continuous_air_production'):
            c.active_focus = selected; c.active_progress = .25
            # The fixture must use a shipped focus name for the generic idle owner.
            if selected == 'continuous_air_production':
                self.assertIn(selected, (MOD/'common/scripted_triggers/ac_politics.txt').read_text())
            with self.assertRaises(AssertionError): w.decide('SOA_wc_adopt','SOA')
        c.active_focus = None; w.decide('SOA_wc_adopt','SOA')
        self.assertEqual('ac_wc_soa_tree', c.tree); self.assertIn('army_effort', c.focuses)

    def test_generation_provenance_counts_and_truthful_global_gaps(self):
        for script in ('build.py','build_art.py','coverage.py'):
            result = subprocess.run([sys.executable,'-B',str(HERE/script),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,(result.stdout+result.stderr)[-3000:])
        data = report(); self.assertEqual(22920, data['summary']['target'])
        self.assertEqual(68,len(data['countries']))
        self.assertEqual(sum(max(0,e['target']-e['delivered_count']) for r in data['countries'] for e in r['eras']),data['summary']['remaining_actual'])
        for tag, expected in [('SOA',240),('CSO',80)]:
            row = next(r for r in data['countries'] if r['tag']==tag)
            self.assertGreaterEqual(row['eras'][0]['delivered_count'],expected)
            self.assertEqual(0,row['eras'][0]['remaining_actual'])
        for path in (MOD/'common/national_focus').glob('ac_wc_*.txt'):
            self.assertNotRegex(path.read_text(),r'transfer_state|add_core_of|create_unit|declare_war_on')
        text = (MOD/'localisation/english/ac_world_campaigns_l_english.yml').read_text(encoding='utf-8-sig')
        self.assertTrue((MOD/'localisation/english/ac_world_campaigns_l_english.yml').read_bytes().startswith(b'\xef\xbb\xbf'))
        for ident in self.base.focuses:
            self.assertIn(ident+':0',text); self.assertIn(ident+'_desc:0',text)

    def test_inventory_credits_shared_descendants_once_and_excludes_orphans(self):
        sources = [('fixture.txt', '''shared_focus = { id = SOA_old_root x = 0 y = 0 }
shared_focus = { id = SOA_old_child prerequisite = { focus = SOA_old_root } }
shared_focus = { id = SOA_orphan }
focus_tree = { id = first shared_focus = SOA_old_root }
focus_tree = { id = second shared_focus = SOA_old_root }''')]
        rows = inventory(sources)
        self.assertEqual({'SOA_old_root','SOA_old_child'},{r['id'] for r in rows})
        self.assertTrue(all(r['imported_by']==['first','second'] for r in rows))
        with self.assertRaises(ValueError): inventory([('bad.txt','focus_tree = { id = broken shared_focus = missing }')])


if __name__ == '__main__': unittest.main(verbosity=2)
