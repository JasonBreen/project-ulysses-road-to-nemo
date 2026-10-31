"""Offline campaign contracts; this executes shipped scripts, not the HOI4 engine."""
import copy
import importlib.util
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/anea'))
from content import FOCUSES, POLICIES
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get, walk

spec = importlib.util.spec_from_file_location('anea_campaign_ucw', ROOT / 'tools/Test-ContinentalWar.py')
ucw = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ucw
spec.loader.exec_module(ucw)


def load(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


class World(ucw.World):
    """Existing tested script subset plus the national bundle.

    Bilateral owner effects are deliberately not simulated here. Its public
    offer trigger is false in this isolated national test; aid execution is
    covered by the separate shared-owner suite.
    """
    def __init__(self, when='1991.1.1', fiscal=False):
        super().__init__(when, fiscal=fiscal)
        for tag in ('EMM', 'EVA', 'NEC'):
            self.countries[tag] = ucw.Country(tag)
        self.focuses = {}
        for tag in ('EMM', 'EVA'):
            c = self.countries[tag]
            c.flags['ac_anea_initialized'] = None
            c.variables.update(ac_anea_preparedness=0, ac_anea_recovery=0)
            tree = get(load(f'common/national_focus/{tag}.txt'), 'focus_tree')
            self.focuses.update({get(v, 'id'): v for k, _, v in tree if k == 'focus'})
        self.effects.update({k: v for k, _, v in load('common/scripted_effects/ac_anea_campaign.txt')})
        self.effects['ac_anea_bound'] = parse('clamp_variable = { var = ac_anea_preparedness min = 0 max = 100 } clamp_variable = { var = ac_anea_recovery min = 0 max = 100 }')
        self.triggers.update({
            'ac_anea_active': parse('OR = { original_tag = EMM original_tag = EVA } has_capitulated = no has_country_flag = ac_anea_initialized'),
            'ac_anea_can_offer': parse('always = no'),
        })
        self.events.update({get(v, 'id'): (k, v) for k, _, v in load('events/ac_anea_narrative.txt') if k == 'country_event'})
        self.technology_categories = set(re.findall(r'^\s*(\w+)\s*$', (MOD / 'common/technology_tags/00_technology.txt').read_text(), re.M))

    def execute(self, nodes, country):
        # Extend only the harness's narrow research-category assertion. The
        # reward and bonus data still come from committed Clausewitz scripts.
        for key, op, value in nodes:
            if key == 'add_tech_bonus':
                data = ucw.fields(value)
                assert data['category'] in self.technology_categories, data
                assert int(data['uses']) == 1 and 0 < float(data['bonus']) <= 1
                country.bonuses.append(data)
            else:
                super().execute([[key, op, value]], country)


class CampaignContracts(unittest.TestCase):
    def test_exact_counts_graph_and_resolved_positions(self):
        w = World()
        self.assertEqual(Counter(EMM=54, EVA=54), Counter(i[:3] for i in w.focuses))
        self.assertEqual({(t, p): 18 for t in ('EMM', 'EVA') for p in ('foundation', 'warning', 'recovery')}, dict(Counter((r.tag, r.phase) for r in FOCUSES)))
        seen = set()
        for ident, node in w.focuses.items():
            position = (ident[:3], int(get(node, 'x')), int(get(node, 'y')))
            self.assertNotIn(position, seen, ident)
            seen.add(position)
            for key, _, value in node:
                if key in ('prerequisite', 'mutually_exclusive'):
                    for _, _, other in value:
                        self.assertIn(other, w.focuses, (ident, other))
                        self.assertEqual(ident[:3], other[:3])
                        if key == 'prerequisite':
                            self.assertLess(int(get(w.focuses[other], 'y')), int(get(node, 'y')))
                        else:
                            reverse = get(w.focuses[other], 'mutually_exclusive', [])
                            self.assertIn(ident, [v for _, _, v in reverse])
            self.assertIn(get(node, 'cost'), ('5', '10'))

    def test_all_focus_rewards_revalidate_and_execute_once(self):
        for row in FOCUSES:
            for fiscal in (False, True):
                with self.subTest(focus=row.id, fiscal=fiscal):
                    when = '1991.1.1' if row.phase == 'foundation' else '1998.10.1' if row.phase == 'warning' else '2005.6.1'
                    w = World(when, fiscal=fiscal)
                    c = w.countries[row.tag]
                    if row.phase == 'recovery':
                        c.flags['ac_anea_crisis'] = None
                    reward = get(w.focuses[row.id], 'completion_reward')
                    c.capitulated = True
                    before = copy.deepcopy(c)
                    w.execute(reward, c)
                    self.assertEqual(before, c)
                    c.capitulated = False
                    w.execute(reward, c)
                    self.assertIn(row.id + '_done', c.flags)
                    after = copy.deepcopy(c)
                    w.execute(reward, c)
                    self.assertEqual(after, c)

    def test_both_policy_alternatives_join_and_remain_exclusive(self):
        for tag, first, second, join in [('EMM','civil_priority','defence_priority','annual_compact'), ('EVA','audited_distribution','command_distribution','district_liaisons')]:
            for choice, rejected in ((first,second),(second,first)):
                w = World()
                c = w.countries[tag]
                w.complete(tag + '_an_national_account', tag)
                w.complete(tag + '_an_' + ('budget_review' if tag == 'EMM' else 'allocation_review'), tag)
                w.complete(tag + '_an_' + choice, tag)
                self.assertFalse(w.focus_available(tag + '_an_' + rejected, tag))
                self.assertTrue(w.focus_available(tag + '_an_' + join, tag))
                self.assertIn(tag + '_an_' + choice, c.flags)
                self.assertNotIn(tag + '_an_' + rejected, c.flags)

    def test_recovery_conclusion_needs_all_four_lanes_but_no_partner(self):
        for tag in ('EMM','EVA'):
            for unavailable in ('refused','war','annexed','subject'):
                with self.subTest(tag=tag, unavailable=unavailable):
                    w = World('2006.1.16')
                    c = w.countries[tag]
                    c.flags['ac_anea_crisis'] = None
                    other = w.countries['EVA' if tag == 'EMM' else 'EMM']
                    if unavailable == 'war': w.wars.add(frozenset(('EMM','EVA')))
                    if unavailable == 'annexed': other.exists = False
                    if unavailable == 'subject': other.subject = True
                    w.globals.update(('ac_anea_offer_refused','ac_anea_aid_frozen','ac_anea_sanctions_active'))
                    final = tag + '_an_recovery_assessment'
                    prerequisites = [v for k, _, v in w.focuses[final] if k == 'prerequisite']
                    self.assertEqual(4, len(prerequisites))
                    self.assertFalse(w.focus_available(final, tag))
                    # Follow the actual independent recovery graph, without any
                    # preparation, foundation or foreign acceptance prerequisites.
                    pending = [r for r in FOCUSES if r.tag == tag and r.phase == 'recovery' and r.id != final]
                    changed = True
                    while changed:
                        changed = False
                        for row in pending:
                            if row.id not in c.focuses and w.focus_available(row.id, tag):
                                w.complete(row.id, tag)
                                changed = True
                    self.assertTrue(w.focus_available(final, tag))
                    w.complete(final, tag)
                    self.assertIn(tag + '_an_assessment_ready', c.flags)
                    w.run('ac_anea_campaign_weekly', tag)
                    assessment = 'ac_anea.' + ('108' if tag == 'EMM' else '208')
                    self.assertIn((w.today + 1,tag,assessment), w.queue)
                    self.assertTrue(w.trigger(get(w.events[assessment][1], 'trigger'), c))
                    w.choose(assessment, tag=tag, option=0)
                    snapshot = copy.deepcopy(c)
                    w.choose(assessment, tag=tag, option=1)
                    self.assertEqual(snapshot, c)

    def test_preparation_expiry_bypass_and_evergreen_military(self):
        for row in FOCUSES:
            if row.phase != 'warning': continue
            w = World('2004.1.1')
            c = w.countries[row.tag]
            c.flags['ac_anea_crisis'] = None
            node = w.focuses[row.id]
            before = copy.deepcopy(c)
            if 'date < 1999.7.8' in row.available:
                self.assertFalse(w.trigger(get(node, 'available'), c), row.id)
                self.assertFalse(w.trigger(get(node, 'bypass'), c), row.id)
                c.flags['ac_anea_late_crisis'] = None
                self.assertTrue(w.trigger(get(node, 'bypass'), c), row.id)
                w.execute(get(node, 'completion_reward'), c)
                self.assertEqual(before.variables, c.variables)
                self.assertNotIn(row.id + '_done', c.flags)
            else:
                self.assertIsNone(get(node, 'bypass'), row.id)
                self.assertTrue(w.trigger(get(node, 'available'), c), row.id)
                self.assertNotIn('ac_anea_preparedness', row.reward)

    def test_narratives_preserve_actual_outcomes_and_late_phase_guards(self):
        w = World('2004.1.1')
        self.assertEqual(16, len([i for i in w.events if i.startswith('ac_anea.')]))
        for tag in ('EMM','EVA'):
            c = w.countries[tag]
            c.flags.update({k:None for k in ('ac_anea_crisis','ac_anea_late_init','ac_anea_late_crisis','ac_anea_warning_past','ac_anea_risk_revised_past','ac_anea_aid_past','ac_anea_sanctions_past',tag+'_an_opening_ready',tag+'_an_allocation_ready')})
            for index in range(1,8):
                ident = 'ac_anea.' + str((100 if tag=='EMM' else 200)+index)
                self.assertFalse(w.trigger(get(w.events[ident][1], 'trigger'), c), ident)
            w.run('ac_anea_campaign_weekly', tag)
        self.assertFalse(w.queue)
        text = (MOD/'events/ac_anea_narrative.txt').read_text()
        self.assertNotRegex(text, r'(set|clr)_global_flag\s*=\s*ac_anea_(sanctions|accord|service|offer|bureau)')
        for tag, ident in (('EMM','ac_anea.107'),('EVA','ac_anea.207')):
            descs = [v for k,_,v in w.events[ident][1] if k=='desc']
            self.assertEqual(4,len(descs))
            for outcome in ('ac_anea_sanctions_active','ac_anea_sanctions_avoided','ac_anea_sanctions_lifted',None):
                w.globals.clear()
                if outcome: w.globals.add(outcome)
                active = [d for d in descs if w.trigger(get(d,'trigger'),w.countries[tag])]
                self.assertEqual(1,len(active))

    def test_campaign_dispatch_once_and_option_rewards_once(self):
        for tag in ('EMM','EVA'):
            w = World('1998.10.1')
            c = w.countries[tag]
            for flag in ('ac_anea_warning','ac_anea_risk_revised',tag+'_an_opening_ready',tag+'_an_allocation_ready'):
                c.flags[flag] = None
            w.run('ac_anea_campaign_weekly',tag)
            self.assertEqual(4,len(w.queue))
            w.run('ac_anea_campaign_weekly',tag)
            self.assertEqual(4,len(w.queue))
            for _,_,ident in list(w.queue):
                w.choose(ident,tag=tag,option=0)
                snapshot = copy.deepcopy(c)
                w.choose(ident,tag=tag,option=1)
                self.assertEqual(snapshot,c,ident)
            w.queue.clear()
            w.run('ac_anea_campaign_weekly',tag)
            self.assertFalse(w.queue)

    def test_localization_policies_and_generated_output(self):
        data = (MOD/'localisation/english/ac_anea_campaign_l_english.yml').read_bytes()
        self.assertTrue(data.startswith(b'\xef\xbb\xbf'))
        keys = re.findall(r'^\s+([\w.]+):\d+ ',data.decode('utf-8-sig'),re.M)
        self.assertEqual(len(keys),len(set(keys)))
        for row in FOCUSES:
            self.assertIn(row.id,keys)
            self.assertIn(row.id+'_desc',keys)
            self.assertGreaterEqual(len(row.desc.split()),35,row.id)
        for ident in POLICIES:
            self.assertIn(ident,keys)
            self.assertIn(ident+'_desc',keys)
        subprocess.run([sys.executable,'-B',str(ROOT/'tools/anea/build_campaign.py'),'--check'],cwd=ROOT,check=True)


if __name__ == '__main__':
    unittest.main()
