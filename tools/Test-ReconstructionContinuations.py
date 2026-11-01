"""Run the actual reconstruction AST with the real P1 fiscal/political owners.

The adapter supplies engine observations, dates, focus completion, event queues
and timed-idea expiry only. It contains no service/payment/choice implementation.
Decimal arithmetic and deepcopy reloads are offline evidence, not native saves.
"""
import copy
from datetime import date
from decimal import Decimal as D
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('reconstruction_real_shared',ROOT/'tools/Test-SharedSystems.py')
shared=importlib.util.module_from_spec(spec);sys.modules[spec.name]=shared;spec.loader.exec_module(shared)
parse,fields=shared.parse,shared.fields
from reconstruction.content import BRANCHES,COUNTRY_NAMES,focus_id,branch_id
from reconstruction import build


class World(shared.World):
    def __init__(self,mode='full'):
        super().__init__(mode)
        for folder,library in [('scripted_effects',self.effects),('scripted_triggers',self.triggers)]:
            for key,_,value in parse((MOD/'common'/folder/'ac_reconstruction.txt').read_text(encoding='utf-8-sig')):
                if key in library:raise ValueError('Conflicting owner '+key)
                library[key]=value
        self.rc_actions=fields(parse((MOD/'common/on_actions/ac_reconstruction.txt').read_text()))['on_actions']
        self.focuses={fields(v)['id']:v for k,_,v in parse((MOD/'common/national_focus/ac_reconstruction_continuations.txt').read_text()) if k=='shared_focus'}
        self.messages={next(x for k,_,x in v if k=='id'):v for k,_,v in parse((MOD/'events/ac_reconstruction.txt').read_text()) if k=='country_event'}
        self.custom=parse((MOD/'common/custom_localization/ac_reconstruction.txt').read_text())
        for c in self.countries.values():c.completed=set();c.timed_ideas={}
        # Recta is released only in this fixture, never by the package. It needs
        # owned land before the real political and fiscal owners initialize.
        next(s for s in self.states.values() if s.owner=='DEL').owner='REC'
        next(s for s in self.states.values() if s.owner=='REC').controller='REC'

    def number(self,value,context,temp,root,previous):
        if value.startswith(('ac_rc_','NPT_rc_','REC_rc_','SAP_rc_','GEB_rc_')):
            return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        results=[]
        for key,op,value in nodes:
            if key=='has_completed_focus':answer=value in context.completed
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            results.append(answer)
        return all(results)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key in ('if','else_if','else'):
                if key=='if':branch=False
                elif branch is None:raise ValueError('Orphan reconstruction branch')
                condition=key=='else' or self.trigger(next(v for k,_,v in value if k=='limit'),context,temp,root,previous)
                if not branch and condition:
                    self.execute([r for r in value if r[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in ('set_variable','add_to_variable','subtract_from_variable') and value[0][0].startswith('ac_rc_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root,previous)
                if key=='set_variable':context.variables[name]=amount
                elif key=='add_to_variable':context.variables[name]=context.variables.get(name,D(0))+amount
                else:context.variables[name]=context.variables.get(name,D(0))-amount
            elif key=='add_timed_idea':
                data=fields(value);context.ideas.add(data['idea']);context.timed_ideas[data['idea']]=self.today+int(data['days'])
            elif key=='remove_ideas':context.ideas.discard(value);context.timed_ideas.pop(value,None)
            elif key=='country_event':
                data=fields(value);self.events.append((context.tag,data['id'],self.today+int(data.get('days',0))))
            elif key in self.countries or key in ('FROM','ROOT'):
                target=previous if key=='FROM' else root if key=='ROOT' else self.countries[key]
                self.execute(value,target,temp,root,context)
            else:super().execute([(key,op,value)],context,temp,root,previous)

    def advance(self,days):
        self.today+=days
        for c in self.countries.values():
            for ident,expiry in list(c.timed_ideas.items()):
                if expiry<=self.today:c.ideas.discard(ident);c.timed_ideas.pop(ident)

    def rc_action(self,name,tag=None,other=None):
        node=fields(fields(self.rc_actions)[name])['effect']
        self.execute(node,self.countries.get(tag),root=self.countries.get(tag),previous=self.countries.get(other))

    def complete(self,ident,tag):
        c=self.countries[tag];node=self.focuses[ident]
        if not self.trigger(fields(node)['available'],c):raise AssertionError('Unavailable focus '+ident)
        self.execute(fields(node)['completion_reward'],c);c.completed.add(ident)

    def custom_text(self,name,tag):
        node=next(v for k,_,v in self.custom if k=='defined_text' and next(x for k,_,x in v if k=='name')==name)
        for key,_,value in node:
            if key=='text' and self.trigger(fields(value).get('trigger',[]),self.countries[tag]):return fields(value)['localization_key']
        return None


class ReconstructionRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines={mode:World(mode).initialize_both() for mode in ('full','experimental','disabled')}
        for mode,w in cls.baselines.items():
            w.today=date(2006,1,1).toordinal();w.rc_action('on_startup')
            for tag in COUNTRY_NAMES:
                c=w.countries[tag];c.variables['ac_pol_capacity']=D(40)
                if mode=='experimental':
                    c.flags['ac_econ_initialized']=None;c.variables.update(ac_econ_treasury=D(100),ac_econ_arrears=D(0))

    def ready(self,branch=None,mode='full',service=0):
        branch=branch or BRANCHES[0];w=copy.deepcopy(self.baselines[mode]);c=w.countries[branch.tag]
        c.completed.add(branch.entry)
        for n in ([0] if service==0 else [0,1,3]):w.complete(focus_id(branch,n),branch.tag)
        return w,c

    def test_all_twenty_services_pay_both_real_owners_once_in_three_modes(self):
        for b,n,ident in build.SERVICES:
            for mode in self.baselines:
                with self.subTest(service=ident,mode=mode):
                    w,c=self.ready(b,mode,n);before=copy.deepcopy(c)
                    w.run(ident+'_start',b.tag)
                    self.assertEqual(before.pp-35,c.pp);self.assertEqual(36,c.variables['ac_pol_capacity'])
                    if mode=='full':self.assertEqual(before.variables['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash'])
                    elif mode=='experimental':self.assertEqual(before.variables['ac_econ_treasury']-2,c.variables['ac_econ_treasury'])
                    else:self.assertEqual({k:v for k,v in before.variables.items() if k.startswith(('ac_macro_','ac_econ_'))},{k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_'))})
                    self.assertIn(ident+'_spirit',c.ideas);snapshot=copy.deepcopy(c)
                    w.run(ident+'_start',b.tag);self.assertEqual(snapshot,c)
                    other=next(s for other_b,_,s in build.SERVICES if other_b.tag==b.tag and s!=ident)
                    w.run(other+'_start',b.tag);self.assertEqual(snapshot,c)
                    w.advance(89);w.run(ident+'_finish',b.tag);self.assertNotIn(ident+'_completed',c.flags)
                    w.advance(1);w.run(ident+'_finish',b.tag)
                    self.assertEqual(1,c.variables['ac_rc_completed_services']);self.assertIn(branch_id(b)+'_service_completed',c.flags)
                    self.assertNotIn(ident+'_spirit',c.ideas);snapshot=copy.deepcopy(c)
                    w.run(ident+'_finish',b.tag);w.run(ident+'_start',b.tag);self.assertEqual(snapshot,c)
                    w.advance(90);w.run(ident+'_start',b.tag);self.assertEqual(before.pp-70,c.pp)

    def test_cost_shortfalls_and_stale_payment_receipt_never_authorize(self):
        for b,n,ident in build.SERVICES:
            for reason in ('pp','capacity','cash','arrears','war','cap','no_land','not_unlocked'):
                w,c=self.ready(b,service=n)
                if reason=='pp':c.pp=D(34)
                elif reason=='capacity':c.variables['ac_pol_capacity']=D(3)
                elif reason=='cash':c.variables['ac_macro_cash']=D('.001')
                elif reason=='arrears':c.variables['ac_macro_arrears']=D(1)
                elif reason=='war':c.war=True
                elif reason=='cap':c.capitulated=True
                elif reason=='no_land':
                    for s in w.states.values():
                        if s.owner==b.tag:s.owner=s.controller='ERU'
                else:c.completed.discard(focus_id(b,0 if n==0 else 3))
                c.flags['ac_rc_payment_authorized']=None;c.flags['ac_macro_transaction_succeeded']=None
                before=copy.deepcopy(c);w.run(ident+'_start',b.tag)
                self.assertEqual(before,c,(ident,reason));self.assertNotIn(ident+'_spirit',c.ideas)

    def test_every_branch_both_policies_and_service_review_settlement(self):
        for b in BRANCHES:
            for choice in (1,2):
                w,c=self.ready(b);tag=b.tag;w.complete(focus_id(b,choice),tag)
                opposite=3-choice;before=copy.deepcopy(c);w.run(focus_id(b,opposite)+'_apply',tag);self.assertEqual(before,c)
                w.complete(focus_id(b,3),tag)
                self.assertFalse(w.trigger(fields(w.focuses[focus_id(b,4)])['available'],c))
                ident=branch_id(b)+'_service_1';w.run(ident+'_start',tag);w.advance(90);w.run('ac_rc_weekly',tag)
                w.complete(focus_id(b,4),tag);w.complete(focus_id(b,5),tag)
                policy=focus_id(b,choice)+'_spirit';self.assertNotIn(policy,c.ideas);self.assertIn(policy+'_settled',c.ideas)
                before=copy.deepcopy(c);w.run(focus_id(b,5)+'_apply',tag);self.assertEqual(before,c)

    def test_known_interruption_hooks_prevent_rapid_restore_completion(self):
        for hook in ('on_annex','on_capitulation_immediate','on_subject_annexed','on_war_relation_added'):
            for b,n,ident in build.SERVICES:
                w,c=self.ready(b,service=n);w.run(ident+'_start',b.tag);w.advance(37)
                paid=c.pp
                if hook=='on_annex':w.rc_action(hook,'ERU',b.tag)
                elif hook=='on_war_relation_added':w.rc_action(hook,'ERU',b.tag)
                else:w.rc_action(hook,b.tag)
                # Land/status may be restored before the next weekly callback;
                # the real hook's cancellation is already durable.
                w.advance(60);w.run('ac_rc_weekly',b.tag);w.run(ident+'_finish',b.tag)
                self.assertNotIn(ident+'_completed',c.flags);self.assertNotIn(ident+'_spirit',c.ideas)
                self.assertEqual(37,c.variables['ac_rc_last_delivered_days']);self.assertEqual(paid,c.pp)
                self.assertEqual(0,c.variables['ac_rc_completed_services'])

    def test_weekly_invalidity_cancellation_and_player_cancel_retain_cost(self):
        for condition in ('war','cap','annex','cancel'):
            w,c=self.ready();ident=build.SERVICES[0][2];w.run(ident+'_start',c.tag);paid=c.pp;w.advance(21)
            if condition=='war':c.war=True
            elif condition=='cap':c.capitulated=True
            elif condition=='annex':
                for s in w.states.values():
                    if s.owner==c.tag:s.owner=s.controller='ERU'
            if condition=='cancel':w.run('ac_rc_interrupt_service',c.tag)
            else:w.run('ac_rc_weekly',c.tag)
            self.assertEqual(21,c.variables['ac_rc_last_delivered_days']);self.assertEqual(paid,c.pp)
            self.assertNotIn('ac_rc_service_active',c.flags);self.assertNotIn(ident+'_completed',c.flags)

    def test_current_and_original_identity_clones_are_inert(self):
        w,c=self.ready();ident=build.SERVICES[0][2];w.run(ident+'_start',c.tag);snapshot=copy.deepcopy(c)
        clone=copy.deepcopy(c);clone.tag='D01';clone.identity=900;w.countries['D01']=clone
        for suffix in ('_start','_finish'):w.run(ident+suffix,'D01')
        w.run('ac_rc_weekly','D01');w.run('ac_rc_interrupt','D01');self.assertEqual(copy.deepcopy(snapshot),c)
        self.assertEqual(snapshot.variables,clone.variables)
        clone.tag=c.tag;clone.original_tag='ZZZ';w.countries[c.tag]=clone;before=copy.deepcopy(clone)
        w.run('ac_rc_weekly',c.tag);w.run(ident+'_finish',c.tag);self.assertEqual(before,clone)

    def test_copied_records_cannot_rebind_a_branch_to_another_participant(self):
        for b,n,ident in build.SERVICES:
            w,c=self.ready(b,service=n);w.run(ident+'_start',b.tag);w.advance(90)
            other=next(tag for tag in COUNTRY_NAMES if tag!=b.tag)
            impostor=copy.deepcopy(c);impostor.tag=impostor.original_tag=other;impostor.identity=999
            w.countries[other]=impostor;before=copy.deepcopy(impostor)
            w.run(ident+'_finish',other)
            self.assertEqual(before,impostor)
            for index in range(6):
                impostor.completed.add(b.entry)
                impostor.flags.pop(focus_id(b,index)+'_done',None)
                snapshot=copy.deepcopy(impostor);w.run(focus_id(b,index)+'_apply',other)
                self.assertEqual(snapshot,impostor,(ident,index))

    def test_before_2006_is_inert_and_2021_2030_late_chains_have_no_historical_grants(self):
        w=World().initialize_both();before=copy.deepcopy(w.countries['NPT']);w.rc_action('on_startup');self.assertEqual(before,w.countries['NPT'])
        for year in (2006,2021,2030):
            for b in BRANCHES:
                w=copy.deepcopy(self.baselines['full']);w.today=date(year,2,1).toordinal();c=w.countries[b.tag]
                c.completed.add(b.entry);balance={k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_'))};equipment=copy.deepcopy(c.equipment)
                for _ in range(3):w.rc_action('on_startup');w.run('ac_rc_weekly',b.tag)
                self.assertEqual(balance,{k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_'))});self.assertEqual(equipment,c.equipment)
                w.complete(focus_id(b,0),b.tag);w.complete(focus_id(b,1),b.tag);w.complete(focus_id(b,3),b.tag)
                ident=branch_id(b)+'_service_2';w.run(ident+'_start',b.tag);w.advance(90);w.run('ac_rc_weekly',b.tag)
                w.complete(focus_id(b,4),b.tag);w.complete(focus_id(b,5),b.tag)
                self.assertIn(focus_id(b,5)+'_done',c.flags)

    def test_sapin_gebet_peace_fallback_never_bypasses_existing_postwar_contract(self):
        for b in [b for b in BRANCHES if b.tag in ('SAP','GEB')]:
            w=copy.deepcopy(self.baselines['full']);c=w.countries[b.tag];node=fields(w.focuses[focus_id(b,0)])
            self.assertTrue(w.trigger(node['available'],c));w.globals.add('ac_postwar_contract_started')
            self.assertFalse(w.trigger(node['available'],c));c.completed.add(b.entry);self.assertTrue(w.trigger(node['available'],c))
        for b in [b for b in BRANCHES if b.tag in ('NPT','REC')]:
            w=copy.deepcopy(self.baselines['full']);c=w.countries[b.tag]
            self.assertFalse(w.trigger(fields(w.focuses[focus_id(b,0)])['available'],c))

    def test_all_28_messages_reply_once_expire_and_reject_clones(self):
        w=copy.deepcopy(self.baselines['full']);self.assertEqual(28,len(w.messages))
        for ident,node in w.messages.items():
            options=[v for k,_,v in node if k=='option'];number=ident.split('.')[1];token='ac_rc_message_'+number
            tag=next(v for k,_,v in w.triggers[token+'_answerable'] if k=='tag')
            for index,option in enumerate(options):
                live=copy.deepcopy(w);c=live.countries[tag];c.flags[token+'_pending']=None;c.flags[token+'_window']=live.today+60
                action=[row for row in option if row[0] not in ('name','ai_chance')]
                self.assertTrue(live.trigger(next(v for k,_,v in node if k=='trigger'),c));live.execute(action,c)
                self.assertIn(token+'_answered',c.flags);before=copy.deepcopy(c);live.execute(action,c);self.assertEqual(before,c)
                self.assertTrue(any(key.endswith('_spirit') for key in c.ideas) or int(number)>=30)
                for invalid in ('expired','annexed','cloned','original','capitulated'):
                    bad=copy.deepcopy(w);target=bad.countries[tag];target.flags[token+'_pending']=None;target.flags[token+'_window']=bad.today+(0 if invalid=='expired' else 60)
                    if invalid=='annexed':bad.rc_action('on_annex','ERU',tag)
                    elif invalid=='cloned':target.tag='D01'
                    elif invalid=='original':target.original_tag='ZZZ'
                    elif invalid=='capitulated':target.capitulated=True
                    before=copy.deepcopy(target);bad.execute(action,target);self.assertEqual(before,target,(ident,index,invalid))

    def test_narrative_dispatch_callbacks_and_unanswered_final_do_not_block(self):
        for b in BRANCHES:
            w,c=self.ready(b);opening=1+list(COUNTRY_NAMES).index(b.tag);policy=10+list(BRANCHES).index(b)
            self.assertIn('ac_rc_message_'+str(opening)+'_sent',c.flags)
            w.complete(focus_id(b,1),b.tag);self.assertIn('ac_rc_message_'+str(policy)+'_sent',c.flags)
            self.assertEqual(branch_id(b)+'_report_callback_unanswered',w.custom_text(branch_id(b)+'_report_callback',b.tag))
            w.run('ac_rc_message_'+str(policy)+'_reply_0',b.tag)
            self.assertEqual(branch_id(b)+'_report_callback_public',w.custom_text(branch_id(b)+'_report_callback',b.tag))
            count=len(w.events);w.run('ac_rc_narrative_tick',b.tag);self.assertEqual(count,len(w.events))
            w.advance(61);w.run('ac_rc_message_'+str(opening)+'_reply_1',b.tag)
            self.assertNotIn(b.tag+'_rc_opening_ministerial',c.flags)
            # Completion is service-owned; an unanswered invitation is optional.
            ident=branch_id(b)+'_service_1';w.complete(focus_id(b,3),b.tag);w.run(ident+'_start',b.tag);w.advance(90);w.run('ac_rc_weekly',b.tag)
            w.complete(focus_id(b,4),b.tag);w.complete(focus_id(b,5),b.tag)
            self.assertIn('ac_rc_message_'+str(30+list(BRANCHES).index(b))+'_sent',c.flags)

    def test_offline_reload_mid_period_and_repeated_startup_are_identical(self):
        w,c=self.ready();ident=build.SERVICES[0][2];w.run(ident+'_start',c.tag);w.advance(44);w.run('ac_rc_weekly',c.tag)
        restored=copy.deepcopy(w);restored.rc_action('on_startup');self.assertEqual(c,restored.countries[c.tag])
        for world in (w,restored):world.advance(49);world.run('ac_rc_weekly',c.tag);world.run('ac_rc_weekly',c.tag)
        self.assertEqual(w.countries[c.tag],restored.countries[c.tag]);self.assertEqual(1,c.variables['ac_rc_completed_services'])

    def test_all_four_national_conclusions_are_reached_after_2020_with_optional_messages_unanswered(self):
        for tag in COUNTRY_NAMES:
            w=copy.deepcopy(self.baselines['full']);w.today=date(2021,1,1).toordinal();c=w.countries[tag]
            c.subject=True # Engine observation: domestic services allow subjects.
            branches=[b for b in BRANCHES if b.tag==tag]
            for b in branches:
                c.completed.add(b.entry)
                for i in (0,2,3):w.complete(focus_id(b,i),tag)
                ident=branch_id(b)+'_service_2';w.run(ident+'_start',tag);w.advance(90);w.run('ac_rc_weekly',tag)
                for i in (4,5):w.complete(focus_id(b,i),tag)
                if b!=branches[-1]:w.advance(90)
            number=50+list(COUNTRY_NAMES).index(tag);token='ac_rc_message_'+str(number)
            self.assertIn(token+'_sent',c.flags);self.assertEqual(tag+'_rc_opening_callback_unanswered',w.custom_text(tag+'_rc_opening_callback',tag))
            w.run(token+'_reply_1',tag);self.assertIn(tag+'_rc_final_readiness',c.flags)
            before=copy.deepcopy(c);w.run(token+'_reply_0',tag);w.run('ac_rc_weekly',tag)
            self.assertEqual(before,c)

    def test_direct_payment_result_clears_before_failed_retry_and_never_spends_when_inactive(self):
        w,c=self.ready();w.run('ac_rc_pay_programme',c.tag)
        self.assertIn('ac_rc_payment_authorized',c.flags);c.capitulated=True
        before_pp=c.pp;balances={k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_','ac_pol_'))}
        w.run('ac_rc_pay_programme',c.tag)
        self.assertNotIn('ac_rc_payment_authorized',c.flags);self.assertEqual(before_pp,c.pp)
        self.assertEqual(balances,{k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_','ac_pol_'))})

    def test_displayed_programme_fee_follows_the_real_active_fiscal_route(self):
        for mode,key in [('full','ac_rc_fee_macro'),('experimental','ac_rc_fee_legacy'),('disabled','ac_rc_fee_none')]:
            w,c=self.ready(mode=mode);self.assertEqual(key,w.custom_text('ac_rc_fee_text',c.tag))
            # Readiness belongs to the actual fiscal account, not this owner's
            # separate capitulation eligibility. A missing handshake is inactive.
            c.flags.pop('ac_macro_initialized',None);c.flags.pop('ac_econ_initialized',None)
            self.assertEqual('ac_rc_fee_none',w.custom_text('ac_rc_fee_text',c.tag))


if __name__=='__main__':unittest.main(verbosity=2)
