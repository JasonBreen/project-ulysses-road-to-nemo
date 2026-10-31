"""Actual national-focus/shared-owner integration in the offline script model.

The preferred-option helper takes the largest authored AI weight. These are
scripted branch checks, not stochastic/natural AI or native campaign evidence.
"""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
spec = importlib.util.spec_from_file_location('anea_integration_systems', ROOT/'tools/Test-AneaSystems.py')
systems = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = systems
spec.loader.exec_module(systems)
ucw = systems.ucw
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import get


class World(systems.World):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for tag in ('EMM','EVA'):
            tree = get(systems.load(f'common/national_focus/{tag}.txt'),'focus_tree')
            self.focuses.update({get(v,'id'):v for k,_,v in tree if k=='focus'})
            # Affordability is a separate owner test. Supply a finite starting
            # political budget here; do not invent daily economic/PP production.
            self.countries[tag].political_power = 1000

    def execute(self,nodes,country):
        if not any(k=='add_tech_bonus' for k,_,_ in nodes):
            return super().execute(nodes,country)
        # Focus/narrative research rewards contain scalar commands, not a mixed
        # ordered if/else chain. Preserve the parent executor for all branches.
        assert not any(k in ('else','else_if') for k,_,_ in nodes)
        for key,op,value in nodes:
            if key=='add_tech_bonus':
                data = ucw.fields(value)
                assert data['category'] in ('industry','electronics','naval_equipment')
                assert int(data['uses'])==1 and 0<float(data['bonus'])<=1
                country.bonuses.append(data)
            else:
                super().execute([(key,op,value)],country)

    def focus(self,tag,suffix,timed=False):
        ident = tag+'_an_'+suffix
        if timed:
            assert self.focus_available(ident,tag),ident
            self.advance(int(get(self.focuses[ident],'cost'))*7)
        self.complete(ident,tag)

    def story(self,tag,index,option=None):
        self.run('ac_anea_campaign_weekly',tag)
        ident = 'ac_anea.'+str((100 if tag=='EMM' else 200)+index)
        assert self.trigger(get(self.events[ident][1],'trigger'),self.countries[tag]),ident
        self.choose(ident, self.preferred(ident,tag) if option is None else option, tag)

    def calendar(self):
        for tag in ('EMM','EVA'):
            self.run('ac_anea_calendar',tag)


def foundation(world,audited=False):
    world.init()
    for tag in ('EMM','EVA'):
        world.focus(tag,'national_account')
        world.focus(tag,'budget_review' if tag=='EMM' else 'allocation_review')
        world.focus(tag,'civil_priority' if tag=='EMM' else 'audited_distribution' if audited else 'command_distribution')
        world.story(tag,1)
        world.story(tag,2)
    return world


class AneaIntegration(unittest.TestCase):
    def test_preferred_historical_narratives_reach_frozen_aid_and_sanctions(self):
        w = foundation(World())
        for when,index in [('1996.4.20',3),('1998.9.20',4),('1999.7.8',5)]:
            w.today = ucw.day(when)
            w.calendar()
            for tag in ('EMM','EVA'):w.story(tag,index)
        self.assertIn('EVA_an_command_distribution',w.countries['EVA'].flags)
        self.assertNotIn('EVA_an_audited_distribution',w.countries['EVA'].flags)
        w.today = ucw.day('2000.1.10')
        w.calendar()
        self.assertIn('ac_anea_offer_pending',w.globals)
        w.choose('ac_anea.1',w.preferred('ac_anea.1','EVA'),'EVA')
        self.assertIn('ac_anea_accord',w.globals)
        for tag in ('EMM','EVA'):w.story(tag,6)
        w.calendar()  # AI authorises the first service using the actual owner.
        self.assertIn('ac_anea_service_active',w.globals)
        w.advance(180)
        self.assertIn('ac_anea_aid_frozen',w.globals)
        self.assertEqual(0,w.countries['EMM'].variables['ac_anea_monitored_cycles'])
        w.today = ucw.day('2002.3.20')
        w.calendar()
        self.assertIn('ac_anea_sanctions_active',w.globals)
        self.assertNotIn('ac_anea_sanctions_avoided',w.globals)
        self.assertIn('ac_anea.10',w.news_ids())
        for tag in ('EMM','EVA'):w.story(tag,7)
        self.assertIn('EVA_an_command_distribution',w.countries['EVA'].flags)

    def test_actual_audited_and_conditional_focuses_earn_alternative(self):
        for fiscal,councils in [(False,False),(True,False),(False,True),(True,True)]:
            with self.subTest(fiscal=fiscal,councils=councils):
                w = foundation(World(fiscal=fiscal,councils=councils),audited=True)
                for tag in ('EMM','EVA'):w.countries[tag].ai=False
                w.today = ucw.day('1999.7.8')
                w.calendar()
                w.focus('EMM','civil_account',timed=True)
                w.focus('EVA','crisis_returns',timed=True)
                w.focus('EVA','water_recovery',timed=True)
                w.today = ucw.day('2000.1.10')
                w.run('ac_anea_offer_aid','EMM')
                w.choose('ac_anea.1',0,'EVA')
                for tag,steps in [('EMM',('aid_review','conditional_assistance')),('EVA',('aid_position','monitored_access'))]:
                    for suffix in steps:w.focus(tag,suffix,timed=True)
                self.assertIn('EMM_an_conditional_aid',w.countries['EMM'].flags)
                self.assertIn('EVA_an_audited_distribution',w.countries['EVA'].flags)
                self.assertIn('EVA_an_aid_open',w.countries['EVA'].flags)
                before = w.countries['EVA'].variables['ac_anea_recovery']
                w.run('ac_anea_authorize_service','EMM')
                w.advance(180)
                w = copy.deepcopy(w)
                w.advance(180)
                w.run('ac_anea_authorize_service','EMM')
                w.advance(180)
                self.assertEqual(before+24,w.countries['EVA'].variables['ac_anea_recovery'])
                self.assertEqual(2,w.countries['EMM'].variables['ac_anea_monitored_cycles'])
                self.assertTrue(w.trigger(w.triggers['ac_anea_alternative_eligible'],w.countries['EMM']))
                self.assertLess(w.today,ucw.day('2002.3.20'))
                w.today = ucw.day('2002.3.20')
                w.calendar()
                self.assertIn('ac_anea_sanctions_avoided',w.globals)
                self.assertNotIn('ac_anea_sanctions_active',w.globals)
                self.assertIn('ac_anea.11',w.news_ids())
                self.assertNotIn('ac_anea.10',w.news_ids())

    def test_self_reliance_focus_withdraws_existing_service_and_bureau(self):
        w = foundation(World(),audited=True)
        for tag in ('EMM','EVA'):w.countries[tag].ai=False
        w.today=ucw.day('1999.7.8');w.calendar()
        w.today=ucw.day('2000.1.10')
        w.run('ac_anea_offer_aid','EMM');w.choose('ac_anea.1',0,'EVA')
        w.today=ucw.day('2004.2.1')
        w.run('ac_anea_found_bureau','EMM')
        w.run('ac_anea_authorize_service','EMM')
        self.assertIn('ac_anea_bureau',w.globals)
        self.assertIn('ac_anea_service_active',w.globals)
        for suffix in ('crisis_returns','aid_position','domestic_self_reliance'):
            w.focus('EVA',suffix)
        w.advance(1)
        self.assertNotIn('ac_anea_accord',w.globals)
        self.assertNotIn('ac_anea_service_active',w.globals)
        self.assertNotIn('ac_anea_bureau',w.globals)
        for tag in ('EMM','EVA','NEC'):
            self.assertNotIn('ac_anea_bureau',w.countries[tag].ideas)

    def test_annexation_then_release_cleans_stale_service_ideas(self):
        for missing in ('EMM','EVA'):
            with self.subTest(missing=missing):
                w = foundation(World(),audited=True)
                for tag in ('EMM','EVA'):w.countries[tag].ai=False
                w.today=ucw.day('1999.7.8');w.calendar()
                w.today=ucw.day('2000.1.10')
                w.run('ac_anea_offer_aid','EMM');w.choose('ac_anea.1',0,'EVA')
                w.run('ac_anea_authorize_service','EMM');w.advance(60)
                paid = w.countries[missing].political_power
                delivered = w.countries['EVA'].variables['ac_anea_recovery']
                w.countries[missing].exists=False
                w.advance(1)
                self.assertNotIn('ac_anea_service_active',w.globals)
                w.countries[missing].exists=True
                w.advance(1)
                self.assertEqual(paid,w.countries[missing].political_power)
                self.assertEqual(delivered,w.countries['EVA'].variables['ac_anea_recovery'])
                for tag in ('EMM','EVA'):
                    for idea in ('ac_anea_relief_burden','ac_anea_monitored_service'):
                        self.assertNotIn(idea,w.countries[tag].ideas)

    def test_selected_zero_progress_focus_still_defers_opt_in_tree_entry(self):
        class ZeroProgressWorld(World):
            def trigger(self,nodes,country):
                # Exact source of the original gap: selected focus reports 0,
                # while the engine-documented shine reflects current work.
                if len(nodes)==1 and nodes[0][0]=='focus_progress':
                    _,op,threshold=next(n for n in nodes[0][2] if n[0]=='progress')
                    return {'>':0>float(threshold),'=':0==float(threshold),'<':0<float(threshold)}[op]
                return super().trigger(nodes,country)
        for tag in ('EMM','EVA'):
            w = ZeroProgressWorld('2000.1.1').init()
            c = w.countries[tag]
            c.tree='generic_focus';c.active_focus='army_effort'
            self.assertFalse(w.available(tag+'_an_enter_campaign',tag))
            effect = get(w.decisions[tag+'_an_enter_campaign'],'complete_effect')
            w.execute(effect,c)
            self.assertEqual('generic_focus',c.tree)
            c.active_focus=None
            self.assertTrue(w.available(tag+'_an_enter_campaign',tag))


if __name__=='__main__':
    unittest.main(verbosity=2)
