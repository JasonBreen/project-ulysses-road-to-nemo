"""Execute SP96 AST with both actual P1 owners; no fiscal/readiness substitute.

Engine observations, focus completions, queued delivery and timed-idea expiry
are adapter concerns. Reservation, price, allocation, timer and narrative logic
execute from generated source. Decimal/deepcopy results are offline evidence.
"""
import copy
from datetime import date
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('snp_actual_shared',ROOT/'tools/Test-SharedSystems.py')
shared=importlib.util.module_from_spec(spec);sys.modules[spec.name]=shared;spec.loader.exec_module(shared)
parse,fields=shared.parse,shared.fields
from superpowers.content import BRANCHES,focus_id
from superpowers.mechanics import COUNTRIES,SERVICES,LATER_PARENT
from superpowers.build import bid,prerequisites


def get(nodes,key,default=None):return next((v for k,_,v in nodes if k==key),default)


class World(shared.World):
    def __init__(self,mode='full',new=True):
        super().__init__(mode,new)
        for folder,library in [('scripted_effects',self.effects),('scripted_triggers',self.triggers)]:
            for key,_,value in parse((MOD/'common'/folder/'ac_superpower_programmes.txt').read_text(encoding='utf-8-sig')):
                if key in library:raise ValueError('Conflicting national owner '+key)
                library[key]=value
        self.snp_actions=get(parse((MOD/'common/on_actions/ac_superpower_programmes.txt').read_text()),'on_actions')
        self.focuses={get(v,'id'):v for k,_,v in parse((MOD/'common/national_focus/ac_superpower_programmes.txt').read_text())if k=='shared_focus'}
        self.events_by_id={get(v,'id'):v for k,_,v in parse((MOD/'events/ac_superpower_programmes.txt').read_text())if k=='country_event'}
        self.custom=parse((MOD/'common/custom_localization/ac_superpower_programmes.txt').read_text())
        for c in self.countries.values():c.completed=set();c.timed_ideas={}

    def number(self,value,context,temp,root,previous):
        if value.startswith('ac_snp_'):return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        answers=[]
        for key,op,value in nodes:
            if key=='has_completed_focus':answer=value in context.completed
            elif key=='custom_trigger_tooltip':answer=self.trigger([r for r in value if r[0]!='tooltip'],context,temp,root,previous)
            elif key in self.countries:answer=self.trigger(value,self.countries[key],temp,root,context)
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            answers.append(answer)
        return all(answers)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={}if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key in('if','else_if','else'):
                if key=='if':branch=False
                elif branch is None:raise ValueError('Orphan national branch')
                condition=key=='else'or self.trigger(get(value,'limit'),context,temp,root,previous)
                if not branch and condition:self.execute([r for r in value if r[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable','set_temp_variable','add_to_temp_variable','subtract_from_temp_variable','multiply_temp_variable')and value[0][0].startswith('ac_snp_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root,previous);target=temp if'temp_variable'in key else context.variables;before=target.get(name,D(0))
                if key.startswith('set_'):target[name]=amount
                elif key.startswith('add_'):target[name]=before+amount
                elif key.startswith('subtract_'):target[name]=before-amount
                elif key.startswith('multiply_'):target[name]=before*amount
                else:target[name]=before/amount
            elif key=='add_timed_idea':
                data=fields(value);context.ideas.add(data['idea']);context.timed_ideas[data['idea']]=self.today+int(data['days'])
            elif key=='remove_ideas':context.ideas.discard(value);context.timed_ideas.pop(value,None)
            elif key=='country_event':
                data=fields(value);self.events.append((context.tag,data['id'],self.today+int(data.get('days',0))))
            elif key=='hidden_effect':self.execute(value,context,temp,root,previous)
            elif key=='show_ideas_tooltip':pass # Presentation only; ideas are applied by the owned hidden effect.
            elif key in self.countries or key in('FROM','ROOT'):
                target=previous if key=='FROM'else root if key=='ROOT'else self.countries[key]
                self.execute(value,target,temp,root,context)
            else:super().execute([(key,op,value)],context,temp,root,previous)

    def advance(self,days):
        self.today+=days
        for c in self.countries.values():
            for name,expiry in list(c.timed_ideas.items()):
                if expiry<=self.today:c.timed_ideas.pop(name);c.ideas.discard(name)

    def snp_action(self,name,tag=None,other=None):
        self.execute(get(get(self.snp_actions,name),'effect'),self.countries.get(tag),root=self.countries.get(tag),previous=self.countries.get(other))

    def complete(self,ident,tag,elapsed=False):
        node=self.focuses[ident];c=self.countries[tag]
        if elapsed:self.advance(int(get(node,'cost'))*7)
        if not self.trigger(get(node,'available'),c):raise AssertionError('Unavailable focus '+ident)
        self.execute(get(node,'completion_reward'),c);c.completed.add(ident)

    def event(self,ident,tag):
        node=self.events_by_id[ident];c=self.countries[tag]
        if not self.trigger(get(node,'trigger',[]),c):return False
        self.execute(get(node,'immediate',[]),c);return True

    def custom_text(self,name,tag):
        node=next(v for k,_,v in self.custom if k=='defined_text'and get(v,'name')==name)
        for key,_,value in node:
            if key=='text'and self.trigger(get(value,'trigger',[]),self.countries[tag]):return get(value,'localization_key')
        return None


class SuperpowerProgrammes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines={mode:World(mode).initialize_both()for mode in('full','experimental','disabled')}
        for mode,w in cls.baselines.items():
            w.snp_action('on_startup')
            for tag in COUNTRIES:
                c=w.countries[tag];c.variables['ac_pol_capacity']=D(40)
                if mode=='experimental':c.flags['ac_econ_initialized']=None;c.variables.update(ac_econ_treasury=D(100),ac_econ_arrears=D(0))

    def ready(self,s=None,mode='full'):
        s=s or SERVICES[0];w=copy.deepcopy(self.baselines[mode]);c=w.countries[s.branch.tag]
        if s.branch.opens=='2006.1.1':
            w.today=date(2006,1,1).toordinal()
            c.completed.update(prerequisites(s.branch,0))
        for i in([0]if s.index==0 else[0,1,3]):w.complete(focus_id(s.branch,i),c.tag)
        return w,c

    def test_all_32_scopes_pay_real_owners_once_in_three_fiscal_modes(self):
        for s in SERVICES:
            for mode in self.baselines:
                with self.subTest(scope=s.id,mode=mode):
                    w,c=self.ready(s,mode);before=copy.deepcopy(c);w.run(s.id+'_start',c.tag)
                    self.assertEqual(before.pp-35,c.pp);self.assertEqual(36,c.variables['ac_pol_capacity'])
                    if mode=='full':self.assertEqual(before.variables['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash'])
                    elif mode=='experimental':self.assertEqual(before.variables['ac_econ_treasury']-2,c.variables['ac_econ_treasury'])
                    else:self.assertEqual({k:v for k,v in before.variables.items()if k.startswith(('ac_macro_','ac_econ_'))},{k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))})
                    snapshot=copy.deepcopy(c);w.run(s.id+'_start',c.tag);self.assertEqual(snapshot,c)
                    self.assertIn(s.id+'_spirit',c.ideas);w.advance(89);w.run(s.id+'_finish',c.tag);self.assertNotIn(s.id+'_completed',c.flags)
                    w.advance(1);self.assertTrue(w.event(s.event,c.tag));self.assertEqual(1,c.variables['ac_snp_completed'])
                    self.assertIn(bid(s.branch)+'_service_completed',c.flags);snapshot=copy.deepcopy(c)
                    w.event(s.event,c.tag);w.run(s.id+'_finish',c.tag);self.assertEqual(snapshot,c)
                    w.run(s.id+'_start',c.tag);self.assertEqual(snapshot,c)
                    w.advance(90);w.run(s.id+'_start',c.tag);self.assertEqual(before.pp-70,c.pp)

    def test_ose_weighted_portfolio_has_three_units_and_releases_exact_receipts(self):
        protected=next(s for s in SERVICES if s.branch.tag=='OSE'and s.index==1 and s.branch.key=='appropriations')
        civil=next(s for s in SERVICES if s.branch.key=='productive_capacity'and s.index==0)
        third=next(s for s in SERVICES if s.branch.key=='continental_transport'and s.index==0)
        w,c=self.ready(protected)
        for s in(civil,third):w.complete(focus_id(s.branch,0),c.tag)
        w.run(protected.id+'_start',c.tag);self.assertEqual(2,c.variables['ac_snp_ose_used'])
        w.run(civil.id+'_start',c.tag);self.assertEqual(3,c.variables['ac_snp_ose_used']);before=copy.deepcopy(c)
        w.run(third.id+'_start',c.tag);self.assertEqual(before,c)
        w.run(protected.id+'_cancel',c.tag);self.assertEqual(1,c.variables['ac_snp_ose_used']);before=copy.deepcopy(c)
        w.run(protected.id+'_cancel',c.tag);self.assertEqual(before,c)
        w.run(third.id+'_start',c.tag);self.assertEqual(2,c.variables['ac_snp_ose_used'])

    def test_all_scopes_reject_cost_and_eligibility_failures_with_no_reward_or_stale_receipt(self):
        for s in SERVICES:
            for reason in('pp','capacity','cash','arrears','capitulated','no_control','locked'):
                w,c=self.ready(s)
                if reason=='pp':c.pp=D(34)
                elif reason=='capacity':c.variables['ac_pol_capacity']=D(3)
                elif reason=='cash':c.variables['ac_macro_cash']=D('.001')
                elif reason=='arrears':c.variables['ac_macro_arrears']=D(1)
                elif reason=='capitulated':c.capitulated=True
                elif reason=='no_control':
                    for state in w.states.values():
                        if state.owner==c.tag:state.controller='ERU'
                else:c.completed.discard(focus_id(s.branch,0 if s.index==0 else 3))
                c.flags['ac_snp_payment_authorized']=None;c.flags['ac_macro_transaction_succeeded']=None
                before=copy.deepcopy(c);before.flags.pop('ac_snp_payment_authorized')
                w.run(s.id+'_start',c.tag);self.assertEqual(before,c,(s.id,reason))
        for mode,stock,value in(('experimental','ac_econ_treasury',1),('experimental','ac_econ_arrears',1)):
            w,c=self.ready(mode=mode);c.variables[stock]=D(value);before=copy.deepcopy(c)
            w.run(SERVICES[0].id+'_start',c.tag);self.assertEqual(before,c)

    def test_timer_needs_the_current_start_record_and_ninety_actual_elapsed_days(self):
        for s in SERVICES:
            w,c=self.ready(s);w.run(s.id+'_start',c.tag);w.advance(30)
            # Fault injection does not substitute a business rule: execute the
            # actual hidden callback with an erroneously early stored due date.
            c.variables[s.prefix+'_due']=D(w.today);w.event(s.event,c.tag)
            self.assertNotIn(s.id+'_completed',c.flags);self.assertIn(s.id+'_active',c.flags)
            c.variables.pop(s.prefix+'_started');before=copy.deepcopy(c)
            self.assertFalse(w.event(s.event,c.tag));self.assertEqual(before,c)

    def test_fresh_completion_receipt_is_published_only_by_the_actual_successful_period(self):
        for s in SERVICES:
            w,c=self.ready(s);key=s.prefix+'_last_completed_started'
            self.assertNotIn(key,c.variables)
            w.run(s.id+'_start',c.tag);first=c.variables[s.prefix+'_started'];w.advance(90)
            w.event(s.event,c.tag)
            self.assertEqual(first,c.variables[key]);self.assertEqual(w.today,c.variables[s.prefix+'_last_completed_on'])
            self.assertEqual(w.number('THIS.id',c,{},c,None),c.variables[s.prefix+'_last_completed_identity'])
            self.assertEqual(1,c.variables[s.prefix+'_start_serial']);self.assertEqual(1,c.variables[s.prefix+'_last_completed_serial'])
            receipt={k:v for k,v in c.variables.items()if k.startswith(s.prefix+'_last_completed_')}
            w.advance(90);w.run(s.id+'_start',c.tag);w.advance(90)
            # A cancellation at the due boundary is not a successful completion,
            # even when the historic completed flag and elapsed90 remain true.
            w.run(s.id+'_cancel',c.tag);self.assertIn(s.id+'_completed',c.flags)
            self.assertEqual(receipt,{k:v for k,v in c.variables.items()if k.startswith(s.prefix+'_last_completed_')})
            w.run(s.id+'_start',c.tag);second=c.variables[s.prefix+'_started'];w.advance(90);w.event(s.event,c.tag)
            self.assertEqual(second,c.variables[key]);self.assertGreater(second,first);self.assertEqual(3,c.variables[s.prefix+'_last_completed_serial'])

    def test_ose_support_controls_price_access_standing_and_bounded_paid_recovery(self):
        for n,lane in((0,'public'),(1,'security')):
            s=SERVICES[n]
            for score,pp,spends in((64,34,False),(65,30,True)):
                w,c=self.ready(s);c.variables['ac_snp_ose_'+lane]=D(score);c.pp=D(pp);w.run('ac_snp_reconcile',c.tag)
                before=copy.deepcopy(c);w.run(s.id+'_start',c.tag)
                self.assertEqual(spends,s.id+'_active'in c.flags)
                if spends:self.assertEqual(0,c.pp);self.assertIn('ac_snp_ose_'+lane+'_standing',c.ideas)
                else:self.assertEqual(before,c)
            w,c=self.ready(s);c.variables['ac_snp_ose_'+lane]=D(29);w.run('ac_snp_reconcile',c.tag);before=copy.deepcopy(c)
            w.run(s.id+'_start',c.tag);self.assertEqual(before,c)
            fee_before={k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))}
            w.run('ac_snp_ose_'+lane+'_consultation',c.tag)
            self.assertEqual(37,c.variables['ac_snp_ose_'+lane]);self.assertEqual(before.pp-20,c.pp);self.assertEqual(38,c.variables['ac_pol_capacity'])
            self.assertEqual(fee_before,{k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))})
            snap=copy.deepcopy(c);w.run('ac_snp_ose_'+lane+'_consultation',c.tag);self.assertEqual(snap,c)
            w.advance(30);c.variables['ac_snp_ose_'+lane]=D(49);w.run('ac_snp_ose_'+lane+'_consultation',c.tag);self.assertEqual(50,c.variables['ac_snp_ose_'+lane])

    def test_yuk_allocation_sum_reservations_and_paid_shifts_preserve_active_work(self):
        a=next(s for s in SERVICES if s.branch.key=='allocation'and s.index==0)
        b=next(s for s in SERVICES if s.branch.key=='industrial_orders'and s.index==0)
        w,c=self.ready(a);w.complete(focus_id(b.branch,0),c.tag)
        w.run(a.id+'_start',c.tag);w.run(b.id+'_start',c.tag)
        self.assertEqual(50,c.variables['ac_snp_yuk_civil_used']);self.assertEqual(2,c.variables['ac_snp_yuk_offices'])
        before=copy.deepcopy(c);w.run('ac_snp_yuk_shift_command',c.tag);self.assertEqual(before,c)
        w.run('ac_snp_yuk_shift_civil',c.tag);self.assertEqual(before.pp-15,c.pp)
        self.assertEqual((60,40),(c.variables['ac_snp_yuk_civil'],c.variables['ac_snp_yuk_command']))
        self.assertIn('ac_snp_yuk_civil_standing',c.ideas);self.assertIn(a.id+'_spirit',c.ideas)
        w.advance(30);w.run(a.id+'_cancel',c.tag);c.completed.add('YUK_army_reform_complete');before_pp=c.pp
        w.run('ac_snp_yuk_shift_command',c.tag);self.assertEqual(before_pp-10,c.pp)
        self.assertEqual((50,50),(c.variables['ac_snp_yuk_civil'],c.variables['ac_snp_yuk_command']));self.assertNotIn('ac_snp_yuk_civil_standing',c.ideas)
        self.assertEqual(25,c.variables['ac_snp_yuk_civil_used'])

    def test_ai_can_pay_to_restore_a_blocked_lane_and_stops_at_service_threshold(self):
        decisions={ident:node for _,_,rows in parse((MOD/'common/decisions/ac_superpower_programmes.txt').read_text())for ident,_,node in rows}
        def weight(w,c,node):
            score=D(get(node,'base','1'))
            for key,_,modifier in node:
                if key=='modifier'and w.trigger([r for r in modifier if r[0]!='factor'],c):score*=D(get(modifier,'factor'))
            return score
        for index,lane in enumerate(('public','security')):
            w,c=self.ready(SERVICES[index]);c.pp=D(500)
            c.variables.update(ac_snp_ose_public=D(0),ac_snp_ose_security=D(0));w.run('ac_snp_reconcile',c.tag)
            node=decisions['ac_snp_ose_'+lane+'_consultation'];ai=get(node,'ai_will_do')
            self.assertFalse(w.trigger(w.triggers[SERVICES[index].id+'_can_start'],c))
            for points in (0,8,16,24):
                self.assertEqual(points,c.variables['ac_snp_ose_'+lane]);self.assertGreater(weight(w,c,ai),0)
                self.assertTrue(w.trigger(get(node,'available'),c));before=copy.deepcopy(c)
                w.execute(get(node,'complete_effect'),c)
                self.assertEqual(before.pp-20,c.pp);self.assertEqual(before.variables['ac_pol_capacity']-2,c.variables['ac_pol_capacity'])
                self.assertFalse(w.trigger(get(node,'available'),c));w.advance(30)
            self.assertEqual(32,c.variables['ac_snp_ose_'+lane]);self.assertEqual(0,weight(w,c,ai))
            self.assertTrue(w.trigger(w.triggers[SERVICES[index].id+'_can_start'],c))
            self.assertTrue(w.trigger(get(node,'available'),c)) # Player can still repair toward fifty.
            before=copy.deepcopy(c);c.pp=D(19);self.assertFalse(w.trigger(get(node,'available'),c))
            c.pp=before.pp;c.variables['ac_pol_capacity']=D(1);self.assertFalse(w.trigger(get(node,'available'),c))

    def test_war_interrupts_ordinary_work_and_allows_reduced_domestic_continuity(self):
        for s in SERVICES:
            w,c=self.ready(s);w.run(s.id+'_start',c.tag);w.advance(37);paid=c.pp
            # Primary hook can precede the observed has_war change.
            w.snp_action('on_war_relation_added',c.tag,'ERU')
            self.assertNotIn(s.id+'_active',c.flags);self.assertEqual(37,c.variables[s.prefix+'_elapsed']);self.assertEqual(paid,c.pp)
            c.war=True;w.run(s.id+'_start',c.tag);self.assertIn(s.id+'_domestic_spirit',c.ideas);self.assertIn(s.id+'_wartime',c.flags)
            w.snp_action('on_war_relation_added',c.tag,'BLK');self.assertIn(s.id+'_active',c.flags)
            w.advance(90);self.assertTrue(w.event(s.event,c.tag));self.assertIn(bid(s.branch)+'_last_domestic',c.flags)
            self.assertEqual(1,c.variables['ac_snp_completed'])

    def test_stale_timers_cannot_finish_or_clear_restarted_work_before_or_after_its_due_date(self):
        for s in SERVICES:
            w,c=self.ready(s);w.run(s.id+'_start',c.tag);w.advance(30);w.run(s.id+'_cancel',c.tag);w.advance(1);w.run(s.id+'_start',c.tag)
            self.assertEqual(30,c.variables['ac_snp_last_interrupted_days']);self.assertEqual(s.id+'_interrupted_record',w.custom_text('ac_snp_interruption_text',c.tag))
            started=c.variables[s.prefix+'_started'];w.advance(59);before=copy.deepcopy(c)
            self.assertFalse(w.event(s.event,c.tag));self.assertEqual(before,c)
            w.advance(32);before=copy.deepcopy(c)
            self.assertFalse(w.event(s.event,c.tag));self.assertEqual(before,c)
            self.assertEqual(started,c.variables[s.prefix+'_started']);self.assertNotIn(s.id+'_completed',c.flags)
            w.run('ac_snp_weekly',c.tag);self.assertEqual(1,c.variables['ac_snp_completed'])
            self.assertEqual(0,c.variables['ac_snp_ose_used']if c.tag=='OSE'else c.variables['ac_snp_yuk_offices'])

    def test_annex_capitulation_subject_annex_and_weekly_invalidity_cancel_without_repayment(self):
        for hook in('on_annex','on_capitulation_immediate','on_subject_annexed','weekly_land','weekly_control','weekly_cap'):
            for s in SERVICES:
                w,c=self.ready(s);w.run(s.id+'_start',c.tag);w.advance(45);paid=c.pp
                if hook=='on_annex':w.snp_action(hook,'ERU',c.tag)
                elif hook.startswith('weekly'):
                    if hook=='weekly_cap':c.capitulated=True
                    else:
                        for state in w.states.values():
                            if state.owner==c.tag:
                                state.controller='ERU'
                                if hook=='weekly_land':state.owner='ERU'
                    w.run('ac_snp_weekly',c.tag)
                    c.capitulated=False
                else:w.snp_action(hook,c.tag)
                w.advance(60);w.event(s.event,c.tag);w.run(s.id+'_finish',c.tag)
                self.assertNotIn(s.id+'_active',c.flags);self.assertNotIn(s.id+'_completed',c.flags);self.assertEqual(paid,c.pp)
                self.assertEqual(45,c.variables[s.prefix+'_elapsed'])

    def test_all_focus_paths_and_late_national_conclusions_preserve_inherited_outcomes(self):
        for tag in COUNTRIES:
            for choice in(1,2):
                w=copy.deepcopy(self.baselines['full']);c=w.countries[tag];c.subject=True
                c.flags.update(YUK_fp_intervened=None,ac_yuk_arkbird_partner=None)
                c.ideas.add('yuk_reformed_field_command');inherited={k:v for k,v in c.flags.items()if not'_snp_'in k}
                w.today=date(2021,1,1).toordinal()
                for b in[b for b in BRANCHES if b.tag==tag]:
                    for i in(0,choice,3):w.complete(focus_id(b,i),tag)
                    s=next(s for s in SERVICES if s.branch==b and s.index==choice-1)
                    w.run(s.id+'_start',tag);w.advance(90);self.assertTrue(w.event(s.event,tag))
                    for i in(4,5):w.complete(focus_id(b,i),tag)
                    for i in(0,choice,3,4,5):
                        before=copy.deepcopy(c);w.run(focus_id(b,i)+'_apply',tag);self.assertEqual(before,c)
                    opposite=3-choice;before=copy.deepcopy(c);w.run(focus_id(b,opposite)+'_apply',tag);self.assertEqual(before,c)
                number=70+list(COUNTRIES).index(tag);self.assertIn('ac_snp_message_'+str(number)+'_sent',c.flags)
                w.run('ac_snp_message_'+str(number)+'_reply_0',tag);self.assertIn(tag+'_snp_final_civil',c.flags)
                # The public spending API publishes its transaction result;
                # that receipt is an authorized fiscal mutation, not an outcome.
                self.assertEqual(inherited,{k:v for k,v in c.flags.items()if not'_snp_'in k and k!='ac_macro_transaction_succeeded'});self.assertIn('yuk_reformed_field_command',c.ideas)
                self.assertEqual(8,c.variables['ac_snp_completed'])

    def test_all_narrative_options_are_once_only_and_reject_expiry_interruptions_and_clones(self):
        w=copy.deepcopy(self.baselines['full']);messages={k:v for k,v in w.events_by_id.items()if get(v,'hidden')!='yes'}
        self.assertEqual(36,len(messages));self.assertEqual(68,len(w.events_by_id))
        for ident,node in messages.items():
            number=ident.split('.')[1];token='ac_snp_message_'+number;tag=next(v for k,_,v in w.triggers[token+'_answerable']if k=='tag')
            for option in[v for k,_,v in node if k=='option']:
                live=copy.deepcopy(w);c=live.countries[tag];c.flags[token+'_pending']=None;c.flags[token+'_window']=live.today+60
                action=[r for r in option if r[0]not in('name','ai_chance')]
                live.execute(action,c);self.assertIn(token+'_answered',c.flags);before=copy.deepcopy(c);live.execute(action,c);self.assertEqual(before,c)
                for invalid in('expired','annexed','clone','other_participant'):
                    bad=copy.deepcopy(w);target=bad.countries[tag];target.flags[token+'_pending']=None;target.flags[token+'_window']=bad.today+(0 if invalid=='expired'else 60)
                    if invalid=='annexed':bad.snp_action('on_annex','ERU',tag)
                    elif invalid=='clone':target.tag='D01'
                    elif invalid=='other_participant':target.tag=target.original_tag='YUK'if tag=='OSE'else'OSE'
                    before=copy.deepcopy(target);bad.execute(action,target);self.assertEqual(before,target,(ident,invalid))

    def test_record_clones_and_wrong_participant_cannot_rebind_focus_service_or_receipt(self):
        for s in SERVICES:
            w,c=self.ready(s);w.run(s.id+'_start',c.tag);w.advance(90);original=copy.deepcopy(c)
            for current,origin in(('D01',c.tag),(c.tag,'ZZZ'),('YUK'if c.tag=='OSE'else'OSE','YUK'if c.tag=='OSE'else'OSE')):
                clone=copy.deepcopy(c);clone.tag=current;clone.original_tag=origin;w.countries[current]=clone
                before=copy.deepcopy(clone);w.event(s.event,current);w.run(s.id+'_finish',current);self.assertEqual(before,clone)
                for i in range(6):
                    clone.flags.pop(focus_id(s.branch,i)+'_done',None);snapshot=copy.deepcopy(clone);w.run(focus_id(s.branch,i)+'_apply',current);self.assertEqual(snapshot,clone)
            self.assertEqual(original,c)

    def test_repeat_startup_copied_reload_and_late_initialization_grant_no_historical_resources(self):
        for year in(1991,2006,2021,2030):
            w=World('disabled',new=False).initialize_both();w.today=date(year,1,1).toordinal()
            before={t:(c.pp,copy.deepcopy(c.equipment),{k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))})for t,c in w.countries.items()}
            w.snp_action('on_startup');snapshot=copy.deepcopy(w.countries)
            w.snp_action('on_startup');self.assertEqual(snapshot,w.countries)
            for t,c in w.countries.items():self.assertEqual(before[t],(c.pp,c.equipment,{k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))}))
        w,c=self.ready();s=SERVICES[0];w.run(s.id+'_start',c.tag);w.advance(44);w.run('ac_snp_weekly',c.tag)
        restored=copy.deepcopy(w);restored.snp_action('on_startup');self.assertEqual(c,restored.countries[c.tag])
        for world in(w,restored):world.advance(46);world.event(s.event,c.tag);world.run('ac_snp_weekly',c.tag)
        self.assertEqual(w.countries[c.tag],restored.countries[c.tag])


if __name__=='__main__':unittest.main(verbosity=2)
