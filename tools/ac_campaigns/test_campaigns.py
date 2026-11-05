"""Execute the actual generated campaign scripts with the real fiscal owners.

The adapter supplies engine observations and bilateral white-peace behavior.
It is fail-closed and provides no native parsing, battle or save proof.
"""
import copy
from collections import Counter
from datetime import date
from decimal import Decimal as D
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from ac_campaigns.catalogue import NATIONS, OPERATIONS
from ac_campaigns.narrative import SCENES
from ac_campaigns.build import compile_content
from economy_script import parse,fields

spec=importlib.util.spec_from_file_location('actual_waves_for_campaigns',ROOT/'tools/content_waves/test_waves.py')
base=importlib.util.module_from_spec(spec);sys.modules[spec.name]=base;spec.loader.exec_module(base)


class World(base.World):
    PREFIXES=base.World.PREFIXES+('ac_camp_','ac_ucw_')

    def __init__(self,mode='full'):
        super().__init__(mode)
        for folder,library in (('scripted_effects',self.effects),('scripted_triggers',self.triggers)):
            for name in ('ac_campaigns','ac_ucw'):
                for key,_,value in parse((MOD/f'common/{folder}/{name}.txt').read_text(encoding='utf-8-sig')):
                    if key in library:raise AssertionError('Duplicated owner '+key)
                    library[key]=value
        self.messages.update({next(x for key,_,x in v if key=='id'):v for k,_,v in parse((MOD/'events/ac_campaigns.txt').read_text()) if k=='country_event'})
        self.focuses.update({fields(v)['id']:v for k,_,v in parse((MOD/'common/national_focus/ac_campaigns.txt').read_text())})
        self.decisions={k:v for _,_,rows in parse((MOD/'common/decisions/ac_campaigns.txt').read_text()) for k,_,v in rows}
        self.globals.add('ac_camp_enabled')

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        answers=[]
        for key,op,value in nodes:
            if key.isdigit():
                answer=self.trigger(value,self.states[int(key)],temp,root,context)
            elif key=='is_controlled_by':
                target=context.tag if value=='THIS' else root.tag if value=='ROOT' else value
                answer=context.controller==target
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            answers.append(answer)
        return all(answers)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        pending=[]
        for key,op,value in nodes:
            if key=='custom_effect_tooltip':continue
            if key in ('white_peace','add_stability'):
                if pending:super().execute(pending,context,temp,root,previous);pending=[]
                if key=='white_peace':self.wars.discard(frozenset((context.tag,value)))
                else:context.stability=max(D(0),min(D(1),context.stability+D(value)))
            else:pending.append((key,op,value))
        if pending:super().execute(pending,context,temp,root,previous)

    def complete(self,ident,tag):
        node=self.focuses[ident];c=self.countries[tag]
        for key,_,value in node:
            if key=='prerequisite' and not any(v in c.completed for k,_,v in value if k=='focus'):raise AssertionError('Prerequisite '+ident)
            if key=='mutually_exclusive' and any(v in c.completed for k,_,v in value if k=='focus'):raise AssertionError('Exclusive '+ident)
        super().complete(ident,tag)

    def decide(self,ident,tag):
        node=self.decisions[ident];c=self.countries[tag]
        for key in ('allowed','visible','available'):
            if not self.trigger(fields(node)[key],c):raise AssertionError('Unavailable decision '+ident)
        self.execute(fields(node)['complete_effect'],c)


def world(mode='full'):
    w=World(mode).initialize_both()
    for n in NATIONS:
        c=w.countries[n.tag];c.variables['ac_pol_capacity']=D(100)
        c.variables['num_deployed_planes']=D(100);c.variables['deployed_airforce_manpower_k']=D(1)
        c.observables['num_deployed_planes']=D(100);c.observables['deployed_airforce_manpower_k']=D(1)
        if mode=='experimental':
            c.flags['ac_econ_initialized']=None
            c.variables.update(ac_econ_treasury=D(100),ac_econ_arrears=D(0))
        w.run('ac_camp_initialize',n.tag)
    w.today=date(2010,9,29).toordinal()
    return w


def prepare(w,tag,lane=0,choice='a'):
    for suffix in ('register','policy_'+choice,'prepared'):w.complete(f'{tag}_camp_{lane}_{suffix}',tag)


class Campaigns(unittest.TestCase):
    def test_generated_content_and_art_are_current(self):
        for script in ('build.py','build_art.py'):
            subprocess.run([sys.executable,'-B',str(HERE/script),'--check'],cwd=ROOT,check=True,capture_output=True)

    def test_all_contracts_localize_and_assets_resolve(self):
        out,manifest=compile_content();ids=[r['id'] for r in manifest['focuses']]
        self.assertEqual(186,len(ids));self.assertEqual(16,len({r['tag'] for r in manifest['focuses']}));self.assertEqual(len(ids),len(set(ids)))
        loc=out['localisation/english/ac_campaigns_l_english.yml'];self.assertTrue(loc.startswith('\ufeffl_english:'))
        assets={r['sprite'] for r in json.loads((HERE/'assets.json').read_text())['assets']}
        for folder in ('national_focus','ideas','decisions'):
            source=out[f'common/{folder}/ac_campaigns.txt']
            for icon in re.findall(r'(?:icon|picture) = (\w+)',source):
                expected=icon if icon.startswith('GFX_') else ('GFX_idea_' if folder=='ideas' else 'GFX_decision_')+icon
                self.assertIn(expected,assets)
        for ident in ids:self.assertIn(' '+ident+':0 ',loc);self.assertIn(' '+ident+'_desc:0 ',loc)
        all_localization='\n'.join(p.read_text(encoding='utf-8-sig') for p in (MOD/'localisation/english').glob('*.yml'))
        key_counts=Counter(re.findall(r'^[ \t]+([\w.]+):(?:[0-9]+)?[ \t]+"',all_localization,re.M))
        for key in re.findall(r'^ (\w[\w.]*):0 ',loc,re.M):
            self.assertEqual(1,key_counts[key],key)

    def test_pilot_has_twelve_long_scenes_six_real_choices(self):
        rows=[s for s in SCENES if 1<=s['id']<=12]
        self.assertEqual(12,len(rows));self.assertEqual(6,sum(len(s['options'])==2 for s in rows))
        self.assertTrue(all(len(s['body'].split())>=200 for s in rows))

    def test_prerequisites_and_policy_alternatives_are_real(self):
        w=world();self.assertRaises(AssertionError,w.complete,'OSE_camp_0_prepared','OSE')
        prepare(w,'OSE');self.assertRaises(AssertionError,w.complete,'OSE_camp_0_policy_b','OSE')
        self.assertRaises(AssertionError,w.complete,'OSE_camp_0_review','OSE')

    def test_additive_lanes_clear_actual_inherited_focus_imports(self):
        folder=MOD/'common/national_focus';definitions={};trees={}
        for path in folder.glob('*.txt'):
            roots=parse(path.read_text(encoding='utf-8-sig'));trees[path.name]=[body for kind,_,body in roots if kind=='focus_tree']
            focuses=[body for kind,_,body in roots if kind=='shared_focus']
            focuses += [v for tree in trees[path.name] for k,_,v in tree if k=='focus']
            for body in focuses:
                row={k:v for k,_,v in body if k in ('id','x','y','relative_position_id')};definitions[row['id']]=row
        def x(ident,seen=()):
            self.assertNotIn(ident,seen);row=definitions[ident]
            return D(row.get('x','0'))+(x(row['relative_position_id'],seen+(ident,)) if row.get('relative_position_id') in definitions else D(0))
        for nation in NATIONS:
            names=[{'SBK':'ac_fsb_sbk.txt','FAT':'ac_fsb_fat.txt'}.get(nation.tag,nation.tag+'.txt')]
            if nation.tag=='BLK':names.append('ac_belkan_campaign.txt')
            for name in names:
                for tree in trees[name]:
                    ids=[v for k,_,v in tree if k=='shared_focus']+[next(v for k,_,v in body if k=='id') for key,_,body in tree if key=='focus']
                    added=[i for i in ids if i.startswith(nation.tag+'_camp_')];inherited=[i for i in ids if i not in added]
                    self.assertTrue(added,name)
                    self.assertGreaterEqual(min(x(i) for i in added)-max((x(i) for i in inherited),default=D(0)),D(4),name)

    def test_actual_funded_start_charges_once_in_every_fiscal_mode(self):
        for mode in ('full','experimental','disabled'):
            w=world(mode);prepare(w,'OSE');c=w.countries['OSE'];pp=c.pp;cap=c.variables['ac_pol_capacity']
            w.decide('ac_camp_contact_start','OSE');self.assertIn('ac_camp_contact_active',c.flags)
            self.assertEqual(pp-25,c.pp);self.assertEqual(cap-2,c.variables['ac_pol_capacity'])
            snapshot=copy.deepcopy(c);w.run('ac_camp_contact_start','OSE');self.assertEqual(snapshot,c)

    def test_shortfalls_and_unready_fiscal_owner_never_authorize(self):
        for resource in ('political','capacity','fiscal'):
            w=world();prepare(w,'OSE');c=w.countries['OSE']
            if resource=='political':c.pp=D(24)
            elif resource=='capacity':c.variables['ac_pol_capacity']=D(1)
            else:c.variables['ac_macro_cash']=D(0)
            w.run('ac_camp_contact_start','OSE');self.assertNotIn('ac_camp_contact_active',c.flags)

    def test_maturation_is_not_instant_completion_and_result_is_once_only(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE')
        w.run('ac_camp_contact_tick','OSE');self.assertNotIn('ac_camp_contact_success',w.globals)
        w.advance(14);w.run('ac_camp_contact_tick','OSE');self.assertIn('ac_camp_contact_success',w.globals)
        snapshot=copy.deepcopy(w.countries['OSE']);w.run('ac_camp_contact_finish','OSE');self.assertEqual(snapshot,w.countries['OSE'])
        w.complete('OSE_camp_0_review','OSE')

    def test_cancellation_preserves_spent_cost_and_blocks_replay(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE');pp=w.countries['OSE'].pp
        w.decide('ac_camp_contact_cancel','OSE');w.advance(60);w.run('ac_camp_contact_tick','OSE')
        self.assertIn('ac_camp_contact_cancelled',w.globals);self.assertNotIn('ac_camp_contact_success',w.globals)
        self.assertEqual(pp,w.countries['OSE'].pp);self.assertRaises(AssertionError,w.decide,'ac_camp_contact_start','OSE')

    def test_actual_loss_of_relation_interrupts_instead_of_completing(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE');w.wars.add(frozenset(('OSE','YUK')))
        w.advance(14);w.run('ac_camp_contact_tick','OSE');self.assertIn('ac_camp_contact_interrupted',w.globals)
        self.assertNotIn('ac_camp_contact_success',w.globals)

    def test_return_after_annexation_does_not_revive_reservation(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE');w.run('ac_camp_interrupt','OSE')
        w.advance(30);w.run('ac_camp_contact_tick','OSE');self.assertNotIn('ac_camp_contact_success',w.globals)
        self.assertNotIn('ac_camp_busy',w.countries['OSE'].flags)

    def test_copied_civil_war_identity_is_not_a_participant(self):
        w=world();c=copy.deepcopy(w.countries['OSE']);c.tag='D99';c.identity=999;w.countries[c.tag]=c
        self.assertFalse(w.trigger(w.triggers['ac_camp_eligible'],c))
        snapshot=copy.deepcopy(c);w.run('ac_camp_weekly_ose',c.tag);self.assertEqual(snapshot,c)

    def test_read_only_result_and_archive_do_not_replay_rewards(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE');w.advance(14);w.run('ac_camp_contact_tick','OSE')
        before=copy.deepcopy(w.countries['OSE']);w.decide('ac_camp_contact_record_success','OSE');self.assertEqual(before,w.countries['OSE'])
        w.run('ac_camp_scene_102_dispatch','OSE');w.option('ac_camp.102','a','OSE')
        snapshot=copy.deepcopy(w.countries['OSE']);w.option('ac_camp.3102','b','OSE');self.assertEqual(snapshot,w.countries['OSE'])

    def test_pending_scene_expires_without_inventing_a_choice(self):
        w=world();prepare(w,'OSE');w.run('ac_camp_scene_102_dispatch','OSE');w.advance(31);w.run('ac_camp_scene_102_expire','OSE')
        c=w.countries['OSE'];self.assertIn('ac_camp_scene_102_unanswered',c.flags)
        self.assertNotIn('OSE_camp_public_account',c.flags);self.assertRaises(AssertionError,w.option,'ac_camp.102','a','OSE')
        w.option('ac_camp.102','z','OSE')

    def test_real_early_choices_reach_the_clinic_callbacks(self):
        for civil,military in (('a','a'),('b','b')):
            w=world();w.globals.update(('ac_ucw_war_started','ac_ucw_isaf_formed'));w.states[310].controller='ERU'
            for ident,tag,option in [(1,'SNS',civil),(2,'ERU',military),(3,'FCU','a'),(4,'SNS','a'),(5,'ERU','a'),(6,'FCU','a'),(7,'SNS','a'),(8,'ERU','a'),(9,'FCU','a'),(10,'SNS','a'),(11,'ERU','a'),(12,'FCU','a')]:
                w.advance(7);w.run(f'ac_camp_scene_{ident}_dispatch',tag);w.option(f'ac_camp.{ident}',option,tag)
            self.assertIn('ac_camp_clinic_civil_permission',w.globals)
            self.assertEqual(civil=='b','ac_camp_clinic_private_list' in w.globals)
            self.assertEqual(military=='a','ac_camp_clinic_military_permission' in w.globals)
            for ident,tag in ((1,'SNS'),(2,'ERU'),(12,'FCU')):
                snapshot=copy.deepcopy(w.countries[tag]);w.option(f'ac_camp.{3000+ident}','a',tag);self.assertEqual(snapshot,w.countries[tag])

    def test_character_fate_closes_once_and_cannot_be_backfilled(self):
        for rescued in (False,True):
            w=world();w.today=date(2010,11,29).toordinal();w.globals.add('ac_cpw_started');w.wars.add(frozenset(('OSE','YUK')))
            if rescued:w.globals.add('ac_camp_rescue_cover_success')
            w.run('ac_camp_character_tick','OSE');fate='ac_camp_chopper_preserved' if rescued else 'ac_camp_chopper_lost'
            self.assertIn(fate,w.globals);snapshot=set(w.globals);w.globals.add('ac_camp_rescue_cover_success');w.run('ac_camp_character_tick','OSE')
            self.assertIn(fate,w.globals);self.assertEqual(snapshot|{'ac_camp_rescue_cover_success'},w.globals)

    def test_earned_peace_requires_both_principals_and_rechecks_third_parties(self):
        for third_party in (False,True):
            w=world();w.globals.update(('ac_cpw_started','ac_camp_harling_success','ac_camp_nikanor_success','ac_camp_solg_success'));w.wars.add(frozenset(('OSE','YUK')))
            w.decide('OSE_camp_peace_offer','OSE')
            if third_party:w.wars.add(frozenset(('OSE','ERU')))
            if third_party:
                self.assertRaises(AssertionError,w.option,'ac_camp.2900','a','YUK');self.assertIn(frozenset(('OSE','YUK')),w.wars)
            else:
                w.option('ac_camp.2900','a','YUK');self.assertNotIn(frozenset(('OSE','YUK')),w.wars)
                self.assertIn('ac_camp_negotiated_peace',w.globals);self.assertIn('ac_cpw_ended',w.globals)

    def test_expired_peace_never_ends_war(self):
        w=world();w.globals.update(('ac_cpw_started','ac_camp_harling_success','ac_camp_nikanor_success','ac_camp_solg_success'));w.wars.add(frozenset(('OSE','YUK')))
        w.decide('OSE_camp_peace_offer','OSE');w.advance(15);w.run('ac_cpw_campaign_peace_accept','YUK')
        self.assertIn(frozenset(('OSE','YUK')),w.wars);self.assertNotIn('ac_cpw_ended',w.globals)
        self.assertRaises(AssertionError,w.option,'ac_camp.2900','b','YUK')
        before=set(w.globals);w.option('ac_camp.2900','z','YUK');self.assertEqual(before,w.globals)
        self.assertNotIn('ac_camp_peace_refused',w.globals)

    def test_owner_dates_do_not_create_a_successful_rescue(self):
        w=world();w.today=date(2010,12,31).toordinal();w.globals.add('ac_cpw_started');w.wars.add(frozenset(('OSE','YUK')))
        w.run('ac_cpw_stage_tick','YUK');self.assertNotIn('ac_cpw_stage_harling',w.globals);self.assertNotIn('ac_cpw_stage_solg',w.globals)

    def test_network_success_is_an_explicit_alternative_without_a_new_war(self):
        for exposed in (False,True):
            w=world();w.globals.update(('ac_cpw_ended','ac_camp_reckoning_success','ac_camp_seizure_success'))
            if exposed:w.globals.add('ac_camp_witness_success')
            before=set(w.wars);w.run('ac_camp_character_tick','BLK');self.assertEqual(before,w.wars)
            self.assertIn('ac_camp_network_exposed_ending' if exposed else 'ac_camp_network_success_ending',w.globals)

    def test_second_carrier_strike_and_recall_are_reciprocal_even_when_both_are_pending(self):
        for winner,loser in (('naval_reserve','second_submarine'),('second_submarine','naval_reserve')):
            w=world('disabled');w.today=date(2010,11,14).toordinal()
            w.globals.update(('ac_cpw_started','ac_camp_submarine_success','ac_camp_denial_success'));w.wars.add(frozenset(('OSE','YUK')))
            prepare(w,'OSE',2);prepare(w,'YUK',1,'b')
            tags={'second_submarine':'OSE','naval_reserve':'YUK'}
            for key in (winner,loser):w.decide('ac_camp_'+key+'_start',tags[key])
            w.advance(7);w.run('ac_camp_'+winner+'_tick',tags[winner]);w.run('ac_camp_'+loser+'_tick',tags[loser])
            self.assertIn('ac_camp_'+winner+'_success',w.globals);self.assertNotIn('ac_camp_'+loser+'_success',w.globals)
            w.advance(15);w.run('ac_camp_'+loser+'_tick',tags[loser]);self.assertIn('ac_camp_'+loser+'_failed',w.globals)
            self.assertRaises(AssertionError,w.decide,'ac_camp_'+loser+'_start',tags[loser])

    def test_battery_dispositions_have_distinct_guarded_results(self):
        for option,expected in (('a','ac_ucw_stonehenge_destroyed'),('b','ac_ucw_stonehenge_disabled'),('c','ac_ucw_stonehenge_recaptured')):
            w=world();w.globals.update(('ac_ucw_stonehenge_seized','ac_camp_battery_success'));w.countries['FCU'].flags['ac_camp_battery_choice_pending']=None
            w.states[310].controller='ERU'
            if option=='c':
                self.assertRaises(AssertionError,w.option,'ac_camp.2400',option,'FCU');w.states[310].controller='SNS'
            w.option('ac_camp.2400',option,'FCU');self.assertIn(expected,w.globals)
            self.assertEqual(option=='a','ac_ucw_stonehenge_destroyed' in w.globals)
            snapshot=set(w.globals);w.run('ac_ucw_campaign_battery_destroyed','FCU');self.assertEqual(snapshot,w.globals)

    def test_every_operation_has_a_real_paid_path_and_deadline(self):
        for o in OPERATIONS:
            with self.subTest(operation=o.key):
                w=world('disabled');c=w.countries[o.tag]
                # Emergent countries receive a physical-owner fixture, never a
                # runtime force grant. It makes the real political owner eligible.
                if not any(s.owner==o.tag for s in w.states.values()):
                    candidate=next(s for s in w.states.values() if s.owner not in ('OSE','YUK','ERU','FCU','SNS'))
                    candidate.owner=candidate.controller=o.tag;w.run('ac_pol_initialize',o.tag);c.variables['ac_pol_capacity']=D(100)
                y,m,d=map(int,o.after.split('.'));w.today=date(y,m,d).toordinal()+1
                w.globals.update(('ac_ucw_war_started','ac_ucw_isaf_formed','ac_cpw_started'))
                w.wars.add(frozenset(('OSE','YUK')))
                if o.campaign=='peace':w.wars.clear()
                if o.campaign=='aftermath' or o.key=='megalith':w.globals.add('ac_ucw_outcome_isaf_victory')
                if o.previous:w.globals.add('ac_camp_'+o.previous+'_success')
                if o.key=='relief':w.globals.update(('ac_camp_clinic_civil_permission','ac_camp_clinic_military_permission','ac_camp_clinic_sponsorship'))
                if o.key=='occupation':w.states[310].controller='ERU'
                if o.key=='liberation':w.states[310].controller='SNS'
                if o.key in ('foothold','evacuation'):
                    next(s for s in w.states.values() if 'YUK' in s.cores).controller='OSE'
                if o.key=='landing':next(s for s in w.states.values() if 'ERU' in s.cores).controller='FCU'
                if o.key=='joint_fleet':prepare(w,'YUK',3)
                if o.key=='arkbird':w.globals.add('ac_cpw_arkbird_committed')
                if o.key in ('battery','engineers','liberation'):w.globals.add('ac_ucw_stonehenge_seized')
                if o.key=='megalith':w.globals.add('ac_ucw_megalith_active')
                prepare(w,o.tag,o.lane,'b' if '_policy_b' in o.condition else 'a')
                from ac_campaigns.catalogue import PARTNERS
                if o.key in PARTNERS:w.globals.add('ac_camp_'+o.key+'_accepted')
                payer=w.countries['FCU'] if o.key=='relief' else c
                pp=payer.pp;w.decide('ac_camp_'+o.key+'_start',o.tag);self.assertEqual(pp-25,payer.pp)
                w.advance(o.days);w.run('ac_camp_'+o.key+'_tick',o.tag)
                self.assertIn('ac_camp_'+o.key+'_success',w.globals)

    def test_occupied_clinic_uses_consented_sponsor_without_bypassing_capacity_owner(self):
        w=world();w.globals.update(('ac_ucw_war_started','ac_ucw_isaf_formed'));w.states[310].controller='ERU';prepare(w,'SNS')
        for ident,tag in ((1,'SNS'),(2,'ERU'),(3,'FCU')):
            w.run(f'ac_camp_scene_{ident}_dispatch',tag);w.option(f'ac_camp.{ident}','a',tag)
        w.countries['SNS'].capitulated=True
        before=copy.deepcopy(w.countries['SNS'].variables);pp=w.countries['FCU'].pp;capacity=w.countries['FCU'].variables['ac_pol_capacity']
        w.decide('ac_camp_relief_start','SNS');self.assertEqual(pp-25,w.countries['FCU'].pp)
        self.assertEqual(capacity-2,w.countries['FCU'].variables['ac_pol_capacity']);self.assertEqual(before,w.countries['SNS'].variables)
        w.advance(7);w.run('ac_camp_relief_tick','SNS');self.assertIn('ac_camp_relief_success',w.globals)

    def test_private_patient_list_can_still_reach_a_limited_arrangement(self):
        w=world();w.globals.update(('ac_ucw_war_started','ac_ucw_isaf_formed'));w.states[310].controller='ERU';prepare(w,'SNS')
        for ident,tag,choice in ((1,'SNS','b'),(2,'ERU','b'),(3,'FCU','a')):
            w.run(f'ac_camp_scene_{ident}_dispatch',tag);w.option(f'ac_camp.{ident}',choice,tag)
        w.decide('ac_camp_relief_start','SNS');w.advance(21);w.run('ac_camp_relief_tick','SNS')
        self.assertIn('ac_camp_relief_limited',w.globals);self.assertNotIn('ac_camp_relief_success',w.globals)
        self.assertNotIn('ac_camp_relief_failed',w.globals);w.complete('SNS_camp_0_review','SNS')

    def test_capture_bonus_follows_real_control(self):
        w=world();w.globals.add('ac_camp_battery_success');w.countries['FCU'].flags['ac_camp_battery_choice_pending']=None;w.states[310].controller='SNS'
        w.option('ac_camp.2400','c','FCU');self.assertIn('ac_camp_recaptured_battery',w.countries['FCU'].ideas)
        w.states[310].controller='ERU';w.run('ac_ucw_campaign_battery_custody_tick','FCU')
        self.assertNotIn('ac_camp_recaptured_battery',w.countries['FCU'].ideas)

    def test_late_entry_does_not_invent_personal_history(self):
        w=world();c=w.countries['OSE'];c.flags.pop('ac_camp_initialized',None);w.today=date(2012,1,1).toordinal()
        w.globals.add('ac_cpw_started');w.run('ac_camp_initialize','OSE');w.run('ac_camp_character_tick','OSE')
        self.assertNotIn('ac_camp_chopper_lost',w.globals);self.assertNotIn('ac_camp_chopper_preserved',w.globals)

    def test_prevented_wars_leave_the_national_account_reachable(self):
        for tag,closed in (('SNS','ac_ucw_war_averted'),('OSE','ac_cpw_prevented')):
            w=world();prepare(w,tag);w.globals.add(closed);w.complete(tag+'_camp_0_review',tag);w.complete(tag+'_camp_0_account',tag)

    def test_network_ending_waits_for_a_real_settlement(self):
        w=world();w.globals.update(('ac_camp_reckoning_success','ac_camp_seizure_success'));w.run('ac_camp_character_tick','BLK')
        self.assertNotIn('ac_camp_network_settled',w.globals)

    def test_stale_foreign_offer_has_a_harmless_close(self):
        w=world();snapshot=copy.deepcopy(w.countries['FCU']);w.option('ac_camp.2003','z','FCU')
        self.assertEqual(snapshot,w.countries['FCU'])

    def test_deadline_cannot_be_backfilled_by_late_completion(self):
        w=world();prepare(w,'OSE');w.decide('ac_camp_contact_start','OSE')
        pp=w.countries['OSE'].pp;w.advance(43)
        w.run('ac_camp_contact_finish','OSE');self.assertNotIn('ac_camp_contact_success',w.globals)
        w.run('ac_camp_contact_tick','OSE');self.assertIn('ac_camp_contact_failed',w.globals)
        self.assertEqual(pp,w.countries['OSE'].pp)

    def test_live_flight_scenes_require_their_current_context(self):
        for absent in ('war','aircraft'):
            w=world();w.globals.add('ac_camp_recon_success')
            if absent!='war':w.globals.add('ac_ucw_war_started')
            if absent=='aircraft':w.countries['FCU'].observables['num_deployed_planes']=D(0)
            w.run('ac_camp_scene_77_dispatch','FCU')
            self.assertNotIn('ac_camp_scene_77_delivered',w.countries['FCU'].flags)
        w=world();w.globals.update(('ac_camp_recon_success','ac_ucw_war_started'))
        w.run('ac_camp_scene_77_dispatch','FCU');self.assertIn('ac_camp_scene_77_delivered',w.countries['FCU'].flags)
        w=world();w.globals.add('ac_camp_island_success');w.run('ac_camp_scene_74_dispatch','OSE')
        self.assertNotIn('ac_camp_scene_74_delivered',w.countries['OSE'].flags)
        w.globals.add('ac_cpw_started');w.run('ac_camp_scene_74_dispatch','OSE')
        self.assertIn('ac_camp_scene_74_delivered',w.countries['OSE'].flags)

    def test_refused_peace_can_be_renewed_at_a_real_cost_without_erasing_history(self):
        w=world();w.globals.update(('ac_cpw_started','ac_camp_harling_success','ac_camp_nikanor_success','ac_camp_solg_success'))
        w.wars.add(frozenset(('OSE','YUK')));w.decide('OSE_camp_peace_offer','OSE');w.option('ac_camp.2900','b','YUK')
        c=w.countries['OSE'];pp=c.pp;cap=c.variables['ac_pol_capacity']
        w.decide('OSE_camp_peace_renew','OSE')
        self.assertEqual(pp-25,c.pp);self.assertEqual(cap-2,c.variables['ac_pol_capacity'])
        self.assertIn('ac_camp_peace_refused',w.globals);self.assertIn('ac_camp_peace_window',c.flags)
        self.assertIn(frozenset(('OSE','YUK')),w.wars)
        w.option('ac_camp.2900','b','YUK');self.assertRaises(AssertionError,w.decide,'OSE_camp_peace_renew','OSE')
        w.advance(31);w.decide('OSE_camp_peace_renew','OSE');w.option('ac_camp.2900','a','YUK')
        self.assertIn('ac_camp_negotiated_peace',w.globals);self.assertIn('ac_camp_peace_refused',w.globals)

    def test_only_registered_megalith_changes_restore_to_the_unchanged_capture(self):
        from usea_expansion.script import parse as ordered_parse,get
        from event_picture_fit.proof import assert_picture_only,restore
        from ac_campaigns.event_migration import MIGRATIONS
        contract=json.loads((ROOT/'tools/event_picture_fit/contract.json').read_text())
        relative='events/ac_ucw.txt';current=ordered_parse((MOD/relative).read_text())
        self.assertEqual(ordered_parse(contract['original_event_sources'][relative]),restore(relative,current))
        for row in MIGRATIONS:
            mutated=copy.deepcopy(current);body=next(v for k,_,v in mutated if k=='country_event' and get(v,'id')==row['event'])
            if row['parent']:body=get(body,row['parent'])
            body.append(['add_political_power','=','1'])
            with self.assertRaisesRegex(ValueError,'Non-picture'):assert_picture_only(relative,mutated)
        mutated=copy.deepcopy(current);body=next(v for k,_,v in mutated if k=='country_event' and get(v,'id')=='ac_ucw.61')
        get(body,'trigger').append(['always','=','yes'])
        with self.assertRaisesRegex(ValueError,'Non-picture'):assert_picture_only(relative,mutated)

    def test_all_six_pilot_choices_receive_frozen_specific_callbacks_and_silence_is_neutral(self):
        def description(w,event,tag):
            selected=[]
            for key,_,value in w.messages[event]:
                if key!='desc':continue
                if isinstance(value,str):selected.append(value)
                elif w.trigger(fields(value).get('trigger',[]),w.countries[tag]):selected.append(fields(value)['text'])
            self.assertEqual(1,len(selected));return selected[0]
        for choice in ('a','b','unanswered'):
            w=world();w.globals.add('ac_ucw_war_started');w.states[310].controller='ERU'
            for row in [s for s in SCENES if 1<=s['id']<=12]:
                ident,tag=row['id'],row['tag'];w.run(f'ac_camp_scene_{ident}_dispatch',tag)
                self.assertIn(f'ac_camp_scene_{ident}_delivered',w.countries[tag].flags)
                if ident>=7:
                    expected=f'ac_camp.{ident}.desc'+('' if choice=='unanswered' else '.v'+str(int(choice=='b')))
                    self.assertEqual(expected,description(w,f'ac_camp.{ident}',tag))
                if choice=='unanswered' and ident<=6:
                    w.advance(31);w.run(f'ac_camp_scene_{ident}_expire',tag)
                else:w.option(f'ac_camp.{ident}',choice if ident<=6 else 'a',tag)
                w.advance(8)
            for row in [s for s in SCENES if 7<=s['id']<=12]:
                ident,tag=row['id'],row['tag'];before=description(w,f'ac_camp.{ident}',tag)
                origin=ident-6;c=w.countries[tag]
                c.flags.pop(f'ac_camp_scene_{origin}_choice_0',None);c.flags.pop(f'ac_camp_scene_{origin}_choice_1',None)
                c.flags[f'ac_camp_scene_{origin}_choice_1' if choice=='a' else f'ac_camp_scene_{origin}_choice_0']=None
                archived=description(w,f'ac_camp.{3000+ident}',tag)
                self.assertEqual(before.replace(f'ac_camp.{ident}.',f'ac_camp.{3000+ident}.'),archived)

    def test_forbidden_state_mutations_absent(self):
        out,_=compile_content();source='\n'.join(out.values())
        self.assertNotRegex(source,r'\b(?:transfer_state|add_state_core|set_country_leader|create_unit|add_equipment_to_stockpile|declare_war_on)\s*=')
        self.assertNotIn('set_global_flag = ac_sp_',source)


if __name__=='__main__':unittest.main(verbosity=2)
