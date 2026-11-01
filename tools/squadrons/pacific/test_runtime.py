"""New40-scene actual AST, real national/fiscal owners; no native claims."""
import copy
from datetime import date
from decimal import Decimal as D
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from config import ROOT,HERE,campaigns
spec=importlib.util.spec_from_file_location('pacific_personal_actual_owner',HERE/'harness.py')
runtime=importlib.util.module_from_spec(spec);sys.modules[spec.name]=runtime;spec.loader.exec_module(runtime)
World,parse,get=runtime.World,runtime.parse,runtime.get
STORIES=campaigns()


def flag(row,key):return'ac_sqp_'+row['tag'].lower()+'_'+key
def key(row,n):return'ac_sqp.'+str(row['base']+n)
def ending(c,h):return'trusted'if c>=65 and h>=65 else'fractured'if c<45 else'compromised'
def paths(row):
    states={(50,50):()}
    for ch in row['chapters']:
        following={}
        for(c,h),path in states.items():
            for i,o in enumerate(ch['options']):following.setdefault((max(0,min(100,c+o['cohesion'])),max(0,min(100,h+o['credibility']))),path+(i,))
        states=following
    return states


class PacificStories(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines={mode:runtime.initialized(mode)for mode in('full','experimental','disabled')}
        for mode,w in cls.baselines.items():
            for row in STORIES:
                enabled=w.trigger([['ac_econ_enabled','=','yes']],w.countries[row['tag']])
                ready=w.trigger([['ac_econ_ready','=','yes']],w.countries[row['tag']])
                if enabled!=(mode!='disabled')or ready!=(mode!='disabled'):raise AssertionError('Actual fiscal owner fixture is not in its claimed mode: '+mode)
    def world(self,mode='full'):return copy.deepcopy(self.baselines[mode])

    def test_all_core_options_execute_once_with_real_three_mode_owners_untouched(self):
        for mode in self.baselines:
            for row in STORIES:
                for ch in row['chapters']:
                    for i,o in enumerate(ch['options']):
                        w=self.world(mode);ident,c=w.open_scene(row,ch);prior=copy.deepcopy(c);foreign=copy.deepcopy((w.globals,w.wars,w.goals,w.states))
                        w.choose(ident,i,c.tag)
                        self.assertEqual(ch['id'],c.variables['ac_sqp_chapter']);self.assertEqual(50+o['cohesion'],c.variables['ac_sqp_cohesion']);self.assertEqual(50+o['credibility'],c.variables['ac_sqp_credibility'])
                        self.assertIn(flag(row,o['flag']),c.flags);self.assertNotIn('ac_sqp_dispatch_pending',c.flags)
                        self.assertEqual(prior.pp,c.pp);self.assertEqual(prior.equipment,c.equipment);self.assertEqual(prior.ideas,c.ideas)
                        self.assertEqual({k:v for k,v in prior.variables.items()if not k.startswith('ac_sqp_')},{k:v for k,v in c.variables.items()if not k.startswith('ac_sqp_')})
                        self.assertEqual(foreign,(w.globals,w.wars,w.goals,w.states));saved=copy.deepcopy(c)
                        for j in range(len(w.options(ident))):w.choose(ident,j,c.tag,stale=True)
                        self.assertEqual(saved,c)

    def test_every_context_callback_is_exactly_one_and_archive_freezes_external_changes(self):
        for row in STORIES:
            for ch in row['chapters']:
                for callback in(False,True)if ch.get('callback')else(False,):
                    w=self.world();ident,c=w.open_scene(row,ch,callback);expected=[ident+'.d_base'+('_callback'if callback else'')]
                    self.assertEqual(expected,w.descriptions(ident,c.tag));w.choose(ident,0,c.tag)
                    w.globals.update(('ac_cpw_started','ac_cpw_tainted','ac_cpw_prevented','ac_cpw_declaration_withheld'))
                    w.wars.add(frozenset(('OSE','YUK')));c.capitulated=True;c.observables.update(num_deployed_planes=20,deployed_airforce_manpower_k=1)
                    if ch.get('callback'):c.flags.pop(flag(row,ch['callback']['flag']),None)
                    archive=key(row,10000+ch['id']);before=copy.deepcopy((w.countries,w.states,w.globals,w.wars,w.story_queue))
                    self.assertTrue(w.deliver(archive,c.tag));self.assertEqual(expected,w.descriptions(archive,c.tag));w.choose(archive,0,c.tag)
                    self.assertEqual(before,(w.countries,w.states,w.globals,w.wars,w.story_queue))

    def test_live_cpw_capability_negative_and_positive_contexts_then_frozen_archive(self):
        for row in STORIES:
            ch=row['chapters'][15];other='YUK'if row['tag']=='OSE'else'OSE'
            for variant in ch['condition_variants']:
                for fault in(None,'owner_absent','capitulated','no_planes','no_air_personnel','wrong_war'):
                    w=self.world();c=w.countries[row['tag']]
                    if variant['id']in('expanded','owned_flight'):
                        w.globals.add('ac_cpw_started');w.wars.add(frozenset((c.tag,other)))
                    if variant['id']=='expanded':w.globals.add('ac_cpw_tainted')
                    if variant['id']=='withheld':w.globals.add('ac_cpw_declaration_withheld')
                    if variant['id']=='exchange':w.globals.add('ac_cpw_prevented')
                    c.observables.update(num_deployed_planes=10,deployed_airforce_manpower_k=1)
                    if fault=='owner_absent':w.globals.clear()
                    elif fault=='capitulated':c.capitulated=True
                    elif fault=='no_planes':c.observables['num_deployed_planes']=0
                    elif fault=='no_air_personnel':c.observables['deployed_airforce_manpower_k']=0
                    elif fault=='wrong_war':w.wars={frozenset((c.tag,'BLK'))}
                    ident,c=w.open_scene(row,ch,True)
                    expected='cap'if c.capitulated else next((v['id']for v in ch['condition_variants']if w.trigger(parse(v['trigger'].replace('ac_sq_','ac_sqp_')),c)),'base')
                    self.assertEqual([ident+'.d_'+expected+'_callback'],w.descriptions(ident,c.tag))
                    if fault is None:self.assertEqual(variant['id'],expected)
                    if variant['id']=='owned_flight'and fault in('no_planes','no_air_personnel','wrong_war','owner_absent'):self.assertEqual('base',expected)
                    w.choose(ident,0,c.tag);archive=key(row,10016);before=w.descriptions(ident,c.tag)
                    w.wars.clear();w.globals.clear();c.capitulated=not c.capitulated;c.observables.clear()
                    self.assertTrue(w.deliver(archive,c.tag));self.assertEqual(before,w.descriptions(archive,c.tag))

    def test_pending_expiry_and_stale_answer_do_not_apply_or_reissue_old_choice(self):
        for row in STORIES:
            w=self.world();ident,c=w.open_scene(row,row['chapters'][1]);before=copy.deepcopy(c);w.advance(31)
            w.run('ac_sqp_'+c.tag.lower()+'_repair_pending',c.tag)
            self.assertIn(flag(row,'missed_2'),c.flags);self.assertEqual(2,c.variables['ac_sqp_chapter'])
            self.assertEqual(before.variables['ac_sqp_cohesion'],c.variables['ac_sqp_cohesion'])
            saved=copy.deepcopy(c);w.choose(ident,0,c.tag,stale=True);w.run('ac_sqp_'+c.tag.lower()+'_repair_pending',c.tag);self.assertEqual(saved,c)
            w.run('ac_sqp_'+c.tag.lower()+'_dispatch',c.tag);self.assertEqual(1,sum(q[2]==ident for q in w.story_queue))

    def test_pending_act_boundary_and_annexed_stale_event_cannot_clear_new_reservation(self):
        for row in STORIES:
            for n,when in((5,'2000.1.1'),(10,'2009.1.1'),(15,'2010.9.28')):
                w=self.world();ident,c=w.open_scene(row,row['chapters'][n-1]);w.at(when)
                w.run('ac_sqp_'+c.tag.lower()+'_repair_pending',c.tag);self.assertIn(flag(row,'missed_'+str(n)),c.flags)
                self.assertEqual(50,c.variables['ac_sqp_cohesion']);self.assertEqual(50,c.variables['ac_sqp_credibility'])
                w.at(row['chapters'][n]['earliest']);w.run('ac_sqp_'+c.tag.lower()+'_dispatch',c.tag)
                self.assertEqual(n+1,c.variables['ac_sqp_pending_chapter']);before=copy.deepcopy(c)
                w.choose(ident,0,c.tag,stale=True);self.assertEqual(before,c)
            w=self.world();ident,c=w.open_scene(row,row['chapters'][2]);w.story_action('on_annex',other=c.tag)
            w.at(row['chapters'][3]['earliest']);w.run('ac_sqp_'+c.tag.lower()+'_dispatch',c.tag)
            self.assertEqual(4,c.variables['ac_sqp_pending_chapter']);before=copy.deepcopy(c);w.choose(ident,0,c.tag,stale=True);self.assertEqual(before,c)

    def test_training_and_science_variants_require_their_actual_independent_capabilities(self):
        for row in STORIES:
            for number,context in((6,'training_return'),(10,'scientific_method')):
                for fault in(None,'no_planes','no_air_personnel','war','capitulated','no_completion','no_partner'):
                    w=self.world();c=w.countries[row['tag']];c.observables.update(num_deployed_planes=10,deployed_airforce_manpower_k=1)
                    w.globals.add('ac_sp_arkbird_complete');w.countries['YUK'].flags['ac_yuk_arkbird_partner']=None
                    if fault=='no_planes':c.observables['num_deployed_planes']=0
                    elif fault=='no_air_personnel':c.observables['deployed_airforce_manpower_k']=0
                    elif fault=='war':w.wars.add(frozenset((c.tag,'BLK')))
                    elif fault=='capitulated':c.capitulated=True
                    elif fault=='no_completion':w.globals.discard('ac_sp_arkbird_complete')
                    elif fault=='no_partner':w.countries['YUK'].flags.pop('ac_yuk_arkbird_partner')
                    ident,c=w.open_scene(row,row['chapters'][number-1],True)
                    eligible=not c.capitulated and(not w.wars and fault not in('no_planes','no_air_personnel')if number==6 else fault not in('no_completion','no_partner'))
                    expected=[ident+'.d_'+(context if eligible else'base')+'_callback'];self.assertEqual(expected,w.descriptions(ident,c.tag))
                    w.choose(ident,0,c.tag);w.globals.clear();c.observables.clear();c.capitulated=not c.capitulated
                    archive=key(row,10000+number);self.assertTrue(w.deliver(archive,c.tag));self.assertEqual(expected,w.descriptions(archive,c.tag))

    def test_category_static_admission_precedes_startup_but_live_visibility_rejects_clones(self):
        for row in STORIES:
            w=World();c=w.countries[row['tag']];node=w.story_categories['ac_sqp_'+row['tag'].lower()]
            self.assertTrue(w.trigger(get(node,'allowed'),c));self.assertFalse(w.trigger(get(node,'visible'),c))
            w.run('ac_sqp_initialize',c.tag);self.assertTrue(w.trigger(get(node,'visible'),c))
            c.identity+=1000;self.assertTrue(w.trigger(get(node,'allowed'),c));self.assertFalse(w.trigger(get(node,'visible'),c))

    def test_country_identity_clone_disabled_and_rapid_annex_return_fail_closed(self):
        for row in STORIES:
            for fault in('identity','original','current','disabled','annex','subject_annex'):
                w=self.world();ident,c=w.open_scene(row,row['chapters'][2]);c.flags[flag(row,'chapter_1')]=None
                if fault=='identity':c.identity+=1000
                elif fault=='original':c.original_tag='BLK'
                elif fault=='current':c.tag='BLK'
                elif fault=='disabled':w.story_enabled=False
                else:
                    w.story_action('on_annex',other=row['tag'])if fault=='annex'else w.story_action('on_subject_annexed',row['tag'])
                    c.exists=False;c.exists=True
                    self.assertIn(flag(row,'missed_3'),c.flags)
                before=copy.deepcopy((w.countries,w.globals,w.states,w.story_queue));w.choose(ident,0,row['tag'],stale=True)
                w.run('ac_sqp_initialize',row['tag']);self.assertEqual(before,(w.countries,w.globals,w.states,w.story_queue))
                if fault in('identity','original','current'):self.assertFalse(w.deliver(key(row,10001),row['tag']))

    def test_startup_reload_and_late_admission_archive_without_historical_choice_rewards(self):
        for row in STORIES:
            for when,minimum in(('1991.2.1',1),('2000.1.1',5),('2009.1.1',10),('2010.9.28',15),('2021.1.1',0)):
                w=self.world();c=w.countries[row['tag']]
                c.flags={k:v for k,v in c.flags.items()if not k.startswith('ac_sqp_')};c.variables={k:v for k,v in c.variables.items()if not k.startswith('ac_sqp_')}
                w.at(when);w.story_queue=[];w.story_action('on_startup');position=c.variables['ac_sqp_chapter']
                self.assertGreaterEqual(position,minimum);self.assertEqual(50,c.variables['ac_sqp_cohesion']);self.assertEqual(50,c.variables['ac_sqp_credibility'])
                self.assertFalse(any(flag(row,o['flag'])in c.flags for ch in row['chapters']for o in ch['options']));self.assertNotIn('ac_sqp_professional_debrief',c.ideas)
                if when=='2021.1.1':self.assertIn('ac_sqp_late_archive',c.flags);self.assertIn('ac_sqp_closed',c.flags)
                clone=copy.deepcopy(w);w.story_action('on_startup');clone.story_action('on_startup');self.assertEqual(w.countries,clone.countries);self.assertEqual(w.story_queue,clone.story_queue)

    def test_all_three_personal_endings_reachable_with_actual_mixed_choice_path(self):
        for row in STORIES:
            states=paths(row);groups={name:[(scores,path)for scores,path in states.items()if ending(*scores)==name]for name in('trusted','compromised','fractured')}
            self.assertTrue(all(groups.values()));mixed=next((path for _,path in groups['trusted']if len(set(path))>1),None);self.assertIsNotNone(mixed)
            for name,choices in groups.items():
                _,path=next(((score,p)for score,p in choices if len(set(p))>1),choices[0]);w=self.world();c=w.countries[row['tag']]
                for ch,i in zip(row['chapters'],path):
                    w.at(ch['earliest']);w.run('ac_sqp_'+c.tag.lower()+'_dispatch',c.tag);ident=key(row,ch['id']);self.assertTrue(w.deliver(ident,c.tag));w.choose(ident,i,c.tag)
                self.assertEqual(name,ending(c.variables['ac_sqp_cohesion'],c.variables['ac_sqp_credibility']))
                w.at('2023.1.1');w.run('ac_sqp_'+c.tag.lower()+'_finish',c.tag)
                ident=key(row,90+next(i for i,e in enumerate(row['endings'])if e['id']==name));self.assertTrue(w.deliver(ident,c.tag));w.choose(ident,0,c.tag)
                self.assertIn(flag(row,'ending_'+name),c.flags);self.assertIn('ac_sqp_closed',c.flags)
                self.assertEqual(name=='trusted','ac_sqp_professional_debrief'in c.ideas)
                saved=copy.deepcopy(c);w.choose(ident,0,c.tag,stale=True);w.run('ac_sqp_'+c.tag.lower()+'_finish',c.tag);self.assertEqual(saved,c)

    def test_no_reading_ui_refresh_pays_or_advances_and_both_hosts_are_independent(self):
        w=self.world();before=copy.deepcopy((w.countries,w.globals,w.story_queue))
        for _ in range(3):
            for ident,(category,node)in w.story_decisions.items():
                for part in('allowed','visible','available'):w.trigger(get(node,part,[]),w.countries['OSE'])
        self.assertEqual(before,(w.countries,w.globals,w.story_queue))
        for row in STORIES:
            other='YUK'if row['tag']=='OSE'else'OSE';foreign=copy.deepcopy(w.countries[other]);ident,c=w.open_scene(row,row['chapters'][0]);w.choose(ident,0,c.tag);self.assertEqual(foreign,w.countries[other])


if __name__=='__main__':unittest.main(verbosity=2)
