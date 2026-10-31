"""Execute shipped Anea contracts offline. This is not HOI4/native evidence.

Unknown script fails closed. Deepcopy reloads cover state persistence in this
model, not engine serialization. Scheduling is tested with actual day windows.
"""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools'))
from economy_script import parse, fields
spec = importlib.util.spec_from_file_location('anea_ucw', ROOT / 'tools/Test-ContinentalWar.py')
ucw = importlib.util.module_from_spec(spec);sys.modules[spec.name] = ucw;spec.loader.exec_module(ucw)


def load(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


class World(ucw.World):
    def __init__(self, when='1991.1.1', fiscal=False, councils=False):
        super().__init__(when, fiscal=fiscal)
        self.councils = councils
        for tag in ('EMM', 'EVA', 'NEC', 'OSE'):
            self.countries[tag] = ucw.Country(tag)
        for country in self.countries.values():
            country.political_power = 300.0
            country.active_focus = None
            country.experience = {'army_experience': 0, 'air_experience': 0, 'navy_experience': 0}
        self.effects.update(ucw.mapping(load('common/scripted_effects/ac_anea.txt')))
        self.triggers.update(ucw.mapping(load('common/scripted_triggers/ac_anea.txt')))
        self.events.update({ucw.mapping(v)['id']: (k, v) for k, _, v in load('events/ac_anea.txt') if k in ('country_event', 'news_event')})
        campaign = MOD / 'common/scripted_effects/ac_anea_campaign.txt'
        if campaign.exists(): self.effects.update(ucw.mapping(load('common/scripted_effects/ac_anea_campaign.txt')))
        narrative = MOD / 'events/ac_anea_narrative.txt'
        if narrative.exists(): self.events.update({ucw.mapping(v)['id']: (k, v) for k, _, v in load('events/ac_anea_narrative.txt') if k == 'country_event'})
        self.effects.setdefault('ac_anea_campaign_weekly', [])
        for category, _, rows in load('common/decisions/ac_anea.txt'):
            self.decisions.update({k: v for k, _, v in rows})
        self.daily = ucw.mapping(load('common/on_actions/ac_anea.txt')[0][2])

    def trigger(self, nodes, country):
        answers = []
        for key, operator, value in nodes:
            if key == 'political_power':
                answers.append({'=': country.political_power == float(value), '>': country.political_power > float(value), '<': country.political_power < float(value), '>=': country.political_power >= float(value), '<=': country.political_power <= float(value)}[operator])
            elif key == 'has_focus_tree': answers.append(country.tree == value)
            elif key == 'has_completed_focus': answers.append(value in country.focuses)
            elif key == 'has_shine_effect_on_focus': answers.append(country.active_focus == value)
            elif key == 'focus_progress':
                data = {k: v for k, _, v in value};progress = 1 if data['focus'] in country.focuses else .5 if country.active_focus == data['focus'] else 0
                answers.append(progress > float(data['progress']))
            elif key == 'check_variable' and value[0][1] in ('>=', '<='):
                name, comparison, operand = value[0];left, right = self.number(name, country), self.number(operand, country)
                answers.append(left >= right if comparison == '>=' else left <= right)
            else: answers.append(super().trigger([(key, operator, value)], country))
        return all(answers)

    def execute(self, nodes, country):
        # Preserve ordered if/else chains; dispatch simple commands back to the
        # subclass so exact political accounting is tested inside nested scopes.
        branch = None
        for key, operator, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': branch = False
                elif branch is None: raise AssertionError('Orphaned ' + key)
                condition = key == 'else' or self.trigger(ucw.mapping(value)['limit'], country)
                if not branch and condition:
                    self.execute([n for n in value if n[0] != 'limit'], country);branch = True
            else:
                branch = None
                if key == 'add_political_power': country.political_power += float(value)
                elif key in ('army_experience', 'air_experience', 'navy_experience'): country.experience[key] += float(value)
                else: super().execute([(key, operator, value)], country)

    def advance(self, days):
        for _ in range(days):
            self.today += 1
            for tag in ('EMM', 'EVA', 'NEC'):
                if self.countries[tag].exists:
                    self.execute(ucw.mapping(self.daily['on_daily_' + tag])['effect'], self.countries[tag])

    def init(self):
        for tag in ('EMM', 'EVA'): self.run('ac_anea_init', tag)
        return self


def accord(monitored=True, when='2000.1.10'):
    world = World().init();world.today = ucw.day(when)
    for tag in ('EMM', 'EVA'): world.run('ac_anea_resolve_crisis', tag)
    eva = world.countries['EVA']
    if monitored: eva.flags['EVA_an_audited_distribution'] = None
    else: eva.flags['EVA_an_command_distribution'] = None
    world.run('ac_anea_offer_aid', 'EMM');world.choose('ac_anea.1', 0, 'EVA')
    return world


class AneaSystems(unittest.TestCase):
    def test_generated_system_matches(self):
        subprocess.run([sys.executable, '-B', 'tools/anea/build_system.py', '--check'], cwd=ROOT, check=True, capture_output=True)

    def test_initialization_once_and_separate_owners(self):
        w = World();w.countries['EMM'].variables['ac_pwi_recovery'] = 73;w.countries['EVA'].variables['ac_ucw_pressure'] = 19
        w.globals.update(('ac_ucw_outcome_erusean_victory', 'ac_postwar_ready'))
        w.init();w.countries['EMM'].variables['ac_anea_preparedness'] = 23
        before = copy.deepcopy(w)
        w.init();self.assertEqual(before.countries, w.countries);self.assertEqual(before.globals, w.globals)
        self.assertEqual(73, w.countries['EMM'].variables['ac_pwi_recovery']);self.assertEqual(19, w.countries['EVA'].variables['ac_ucw_pressure'])

    def test_crisis_floor_and_caps_for_every_preparedness_value(self):
        for prep in range(101):
            w = World().init();w.today = ucw.day('1999.7.8')
            for tag, base, div, cap in [('EMM', 70, 5, 90), ('EVA', 15, 4, 40)]:
                c = w.countries[tag];c.variables['ac_anea_preparedness'] = prep
                w.run('ac_anea_resolve_crisis', tag)
                self.assertEqual(min(cap, base + prep // div), c.variables['ac_anea_recovery'], (tag, prep))
                before = copy.deepcopy(c);w.run('ac_anea_resolve_crisis', tag);self.assertEqual(before, c)

    def test_bounds(self):
        for amount, expected in [(-300, 0), (500, 100), (37, 37)]:
            w = World().init();c = w.countries['EMM']
            c.variables.update(ac_anea_preparedness=amount, ac_anea_recovery=amount);w.run('ac_anea_bound', 'EMM')
            self.assertEqual(expected, c.variables['ac_anea_preparedness']);self.assertEqual(expected, c.variables['ac_anea_recovery'])

    def test_preparation_costs_cooldown_expiry_and_training_separation(self):
        w = World().init();c = w.countries['EMM']
        w.run('ac_anea_prepare', 'EMM');self.assertEqual(275, c.political_power);self.assertEqual(3, c.variables['ac_anea_preparedness'])
        w.run('ac_anea_prepare', 'EMM');self.assertEqual(275, c.political_power)
        w.run('ac_anea_train', 'EMM');self.assertEqual(0, c.experience['army_experience'])
        w.advance(180);w.run('ac_anea_train', 'EMM');self.assertEqual(6, c.experience['army_experience']);self.assertEqual(3, c.variables['ac_anea_preparedness'])
        w.advance(180);w.run('ac_anea_prepare', 'EMM');self.assertEqual(6, c.variables['ac_anea_preparedness'])
        w.today = ucw.day('1999.7.8');before = copy.deepcopy(c);w.run('ac_anea_prepare', 'EMM');self.assertEqual(before, c)

    def test_offer_once_and_replies_are_once_only(self):
        w = accord();self.assertIn('ac_anea_accord', w.globals)
        before = copy.deepcopy(w.countries);w.choose('ac_anea.1', 1, 'EVA');w.run('ac_anea_offer_aid', 'EMM')
        self.assertEqual(before, w.countries);self.assertIn('ac_anea_accord', w.globals)
        self.assertEqual(1, len(w.queue))

    def test_offer_refusal_expiry_and_invalid_queued_replies(self):
        for failure in ('refusal', 'expired', 'war', 'annexed', 'donor_annexed', 'subject', 'capitulated'):
            with self.subTest(failure=failure):
                w = World().init();w.today = ucw.day('2000.1.10');w.run('ac_anea_offer_aid', 'EMM')
                if failure == 'refusal': w.choose('ac_anea.1', 1, 'EVA')
                elif failure == 'expired': w.advance(60)
                elif failure == 'war': w.wars.add(frozenset(('EMM', 'EVA')))
                elif failure == 'annexed': w.countries['EVA'].exists = False
                elif failure == 'donor_annexed': w.countries['EMM'].exists = False
                elif failure == 'subject': w.countries['EVA'].subject = True
                elif failure == 'capitulated': w.countries['EMM'].capitulated = True
                w.choose('ac_anea.1', 0, 'EVA');w.advance(1)
                self.assertNotIn('ac_anea_accord', w.globals);self.assertNotIn('ac_anea_offer_pending', w.globals)

    def test_exact_service_cost_delivery_renewal_and_reload(self):
        w = accord();e, v = w.countries['EMM'], w.countries['EVA'];base = v.variables['ac_anea_recovery']
        w.run('ac_anea_authorize_service', 'EMM');self.assertEqual(275, e.political_power);self.assertEqual(285, v.political_power)
        w.run('ac_anea_authorize_service', 'EMM');self.assertEqual(275, e.political_power)
        w.advance(59);self.assertEqual(base, v.variables['ac_anea_recovery'])
        w.advance(1);self.assertEqual(base + 4, v.variables['ac_anea_recovery'])
        w = copy.deepcopy(w);w.advance(120);e, v = w.countries['EMM'], w.countries['EVA']
        self.assertEqual(base + 12, v.variables['ac_anea_recovery']);self.assertEqual(1, e.variables['ac_anea_monitored_cycles'])
        self.assertNotIn('ac_anea_service_active', w.globals);self.assertNotIn('ac_anea_relief_burden', e.ideas)
        w.run('ac_anea_authorize_service', 'EMM');self.assertEqual(275, e.political_power)
        w.advance(180);w.run('ac_anea_authorize_service', 'EMM');self.assertEqual(250, e.political_power)
        w.advance(180);self.assertEqual(2, e.variables['ac_anea_monitored_cycles']);self.assertEqual(base + 24, v.variables['ac_anea_recovery'])

    def test_authorization_rechecks_affordability(self):
        for tag, amount in [('EMM', 24), ('EVA', 14), ('EMM', 24.5), ('EVA', 14.5)]:
            w = accord();w.countries[tag].political_power = amount;before = copy.deepcopy(w.countries)
            w.run('ac_anea_authorize_service', 'EMM');self.assertEqual(before, w.countries);self.assertNotIn('ac_anea_service_active', w.globals)
        w = accord();w.countries['EMM'].political_power = 25;w.countries['EVA'].political_power = 15
        w.run('ac_anea_authorize_service', 'EMM')
        self.assertEqual(0, w.countries['EMM'].political_power);self.assertEqual(0, w.countries['EVA'].political_power)

    def test_domestic_fractional_cost_and_shared_allocation_guard(self):
        w = accord();c = w.countries['EVA'];c.political_power = 34.5
        before = copy.deepcopy(c);w.run('ac_anea_repair', 'EVA');self.assertEqual(before, c)
        c.political_power = 35;w.run('ac_anea_repair', 'EVA');self.assertEqual(0, c.political_power)
        c.political_power = 100;before = copy.deepcopy(c);w.run('ac_anea_train', 'EVA');self.assertEqual(before, c)

    def test_command_distribution_freezes_then_reform_can_reopen(self):
        w = accord(False);v = w.countries['EVA'];base = v.variables['ac_anea_recovery']
        w.run('ac_anea_authorize_service', 'EMM');w.advance(180)
        self.assertEqual(base + 6, v.variables['ac_anea_recovery']);self.assertIn('ac_anea_aid_frozen', w.globals)
        self.assertEqual(0, w.countries['EMM'].variables['ac_anea_monitored_cycles'])
        w.run('ac_anea_resume_aid', 'EMM');self.assertIn('ac_anea_aid_frozen', w.globals)
        v.flags['EVA_an_audited_distribution'] = None;w.run('ac_anea_resume_aid', 'EMM');self.assertNotIn('ac_anea_aid_frozen', w.globals)
        paid = w.countries['EMM'].political_power;w.run('ac_anea_resume_aid', 'EMM');self.assertEqual(paid, w.countries['EMM'].political_power)

    def test_distribution_change_mid_service_cannot_count_as_monitored(self):
        w = accord();w.run('ac_anea_authorize_service', 'EMM');w.advance(60)
        w.countries['EVA'].flags.pop('EVA_an_audited_distribution');w.advance(60)
        w.countries['EVA'].flags['EVA_an_audited_distribution'] = None;w.advance(60)
        self.assertEqual(0, w.countries['EMM'].variables['ac_anea_monitored_cycles']);self.assertIn('ac_anea_aid_frozen', w.globals)

    def test_audit_dropped_between_deliveries_invalidates_monitoring(self):
        w = accord();w.run('ac_anea_authorize_service', 'EMM');w.advance(20)
        w.countries['EVA'].flags.pop('EVA_an_audited_distribution');w.advance(1)
        w.countries['EVA'].flags['EVA_an_audited_distribution'] = None;w.advance(159)
        self.assertEqual(0, w.countries['EMM'].variables['ac_anea_monitored_cycles'])

    def test_national_aid_policies_have_operational_consequences(self):
        w = accord(False);w.countries['EMM'].flags['EMM_an_conditional_aid'] = None
        w.run('ac_anea_authorize_service', 'EMM');self.assertNotIn('ac_anea_service_active', w.globals)
        w.countries['EVA'].flags['EVA_an_audited_distribution'] = None
        w.run('ac_anea_authorize_service', 'EMM');self.assertIn('ac_anea_service_active', w.globals)
        w.countries['EVA'].flags.pop('EVA_an_audited_distribution');w.advance(1)
        self.assertNotIn('ac_anea_service_active', w.globals);self.assertIn('ac_anea_aid_frozen', w.globals)
        w = accord();w.run('ac_anea_authorize_service', 'EMM');w.countries['EVA'].flags['EVA_an_self_reliance'] = None;w.advance(1)
        self.assertNotIn('ac_anea_accord', w.globals);self.assertNotIn('ac_anea_service_active', w.globals)

    def test_interruption_retains_paid_and_delivered_and_cleans_all_modifiers(self):
        for failure in ('war', 'donor_subject', 'recipient_subject', 'donor_annexed', 'recipient_annexed', 'donor_capitulated', 'recipient_capitulated'):
            with self.subTest(failure=failure):
                w = accord();w.run('ac_anea_authorize_service', 'EMM');w.advance(60)
                e, v = w.countries['EMM'], w.countries['EVA'];delivered = v.variables['ac_anea_recovery'];paid = e.political_power
                if failure == 'war': w.wars.add(frozenset(('EMM', 'EVA')))
                else:
                    side, mode = failure.split('_');c = e if side == 'donor' else v
                    setattr(c, {'subject': 'subject', 'annexed': 'exists', 'capitulated': 'capitulated'}[mode], mode != 'annexed')
                w.advance(180);self.assertEqual(delivered, v.variables['ac_anea_recovery']);self.assertEqual(paid, e.political_power)
                self.assertNotIn('ac_anea_service_active', w.globals);self.assertNotIn('ac_anea_accord', w.globals)
                if e.exists: self.assertNotIn('ac_anea_relief_burden', e.ideas)
                if v.exists: self.assertNotIn('ac_anea_monitored_service', v.ideas)

    def test_sanctions_review_actual_outcomes_and_reconsideration(self):
        for alternative in (False, True):
            w = accord();w.today = ucw.day('2002.3.20')
            if alternative:
                w.countries['EMM'].variables['ac_anea_monitored_cycles'] = 2;w.countries['EVA'].variables['ac_anea_recovery'] = 40
            w.run('ac_anea_review_sanctions', 'EMM');w.run('ac_anea_review_sanctions', 'EMM')
            self.assertIn('ac_anea_sanctions_reviewed', w.globals);self.assertEqual(1, len(w.news))
            self.assertIn('ac_anea_sanctions_avoided' if alternative else 'ac_anea_sanctions_active', w.globals)
            self.assertEqual('ac_anea.11' if alternative else 'ac_anea.10', w.news[0][2])
            if not alternative:
                w.countries['EMM'].variables['ac_anea_monitored_cycles'] = 2;w.countries['EVA'].variables['ac_anea_recovery'] = 40
                w.run('ac_anea_reconsider_sanctions', 'EMM');w.run('ac_anea_reconsider_sanctions', 'EMM')
                self.assertNotIn('ac_anea_sanctions_active', w.globals);self.assertEqual(2, len(w.news))

    def test_each_alternative_requirement_is_necessary(self):
        for missing in ('audit', 'cycles', 'recovery', 'accord', 'partner'):
            w = accord();w.countries['EMM'].variables['ac_anea_monitored_cycles'] = 2;w.countries['EVA'].variables['ac_anea_recovery'] = 40
            if missing == 'audit': w.countries['EVA'].flags.pop('EVA_an_audited_distribution')
            if missing == 'cycles': w.countries['EMM'].variables['ac_anea_monitored_cycles'] = 1
            if missing == 'recovery': w.countries['EVA'].variables['ac_anea_recovery'] = 39
            if missing == 'accord': w.globals.discard('ac_anea_accord')
            if missing == 'partner': w.countries['EVA'].subject = True
            self.assertFalse(w.trigger(w.triggers['ac_anea_alternative_eligible'], w.countries['EMM']), missing)

    def test_bureau_nec_accept_refusal_expiry_and_interruption(self):
        for response in ('accept', 'refuse', 'expire', 'ineligible'):
            w = accord();w.today = ucw.day('2004.2.1');w.run('ac_anea_found_bureau', 'EMM');w.run('ac_anea_found_bureau', 'EMM')
            self.assertEqual(1, sum(ident == 'ac_anea.20' for _, _, ident in w.queue))
            if response == 'accept': w.choose('ac_anea.20', 0, 'NEC')
            elif response == 'refuse': w.choose('ac_anea.20', 1, 'NEC')
            elif response == 'expire': w.advance(60);w.choose('ac_anea.20', 0, 'NEC')
            else: w.countries['NEC'].subject = True;w.choose('ac_anea.20', 0, 'NEC');w.advance(1)
            self.assertIn('ac_anea_bureau', w.globals)
            self.assertEqual(response == 'accept', 'ac_anea_bureau' in w.countries['NEC'].ideas)
            w.wars.add(frozenset(('EMM', 'EVA')));w.advance(1)
            self.assertNotIn('ac_anea_bureau', w.globals);self.assertNotIn('ac_anea_bureau', w.countries['NEC'].ideas)

    def test_late_init_phase_boundaries_no_retroactive_rewards(self):
        for when in ('1992.1.1', '1996.4.20', '1998.7.29', '1999.7.8', '2000.3.11', '2002.3.20', '2004.2.1', '2006.1.1'):
            w = World(when).init();self.assertIn('ac_anea_late_init', w.countries['EMM'].flags)
            for tag, neutral in [('EMM', 70), ('EVA', 15)]:
                c = w.countries[tag]
                self.assertEqual(0, c.variables['ac_anea_preparedness'])
                self.assertEqual(neutral if when >= '1999.7.8' else 0, c.variables['ac_anea_recovery'])
            w.run('ac_anea_offer_aid', 'EMM');w.run('ac_anea_review_sanctions', 'EMM')
            if w.today >= ucw.day('2000.3.11'): self.assertFalse(w.queue)
            if w.today >= ucw.day('2002.3.20'): self.assertFalse(w.news)

    def test_old_save_entry_waits_for_generic_focus_and_preserves_state(self):
        w = World('2004.1.1').init();c = w.countries['EMM'];c.tree = 'generic_focus'
        generic = next(n for k, _, n in load('common/national_focus/generic.txt') if k == 'focus_tree')
        first = next(ucw.mapping(n)['id'] for k, _, n in generic if k == 'focus')
        c.active_focus = first
        effect = ucw.mapping(w.decisions['EMM_an_enter_campaign'])['complete_effect'];w.execute(effect, c)
        self.assertEqual('generic_focus', c.tree)
        c.active_focus = None;c.focuses.add(first);before = copy.deepcopy(c.variables);w.execute(effect, c)
        self.assertEqual('ac_anea_emm_tree', c.tree);self.assertEqual(before, c.variables);self.assertIn(first, c.focuses)

    def test_disabled_optional_systems_and_post2005_delivery(self):
        for fiscal in (False, True):
            for councils in (False, True):
                w = accord();w.fiscal = fiscal;w.councils = councils;w.today = ucw.day('2005.12.1')
                w.run('ac_anea_authorize_service', 'EMM');w.advance(180)
                self.assertEqual(1, w.countries['EMM'].variables['ac_anea_monitored_cycles'])
                w.run('ac_anea_authorize_service', 'EMM');self.assertNotIn('ac_anea_service_active', w.globals)


if __name__ == '__main__': unittest.main(verbosity=2)
