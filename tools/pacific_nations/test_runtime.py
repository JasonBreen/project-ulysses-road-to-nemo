"""Execute fresh-work, identity and lifecycle contracts with all real owners."""
import copy
from datetime import date
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from pacific_nations.harness import World,initialized,snp,get,parse
from pacific_nations.model import MOD,countries,branches
from pacific_nations.build import prefix
from superpowers.content import BRANCHES as SNP_BRANCHES,focus_id
from superpowers.mechanics import SERVICES
from superpowers.build import prerequisites


def finish_service(w,s):
    c=w.countries[s.branch.tag]
    if w.trigger([['has_country_flag','=',s.id+'_cooldown']],c):w.advance(90)
    before=copy.deepcopy(c);w.run(s.id+'_start',c.tag)
    if s.id+'_active'not in c.flags:raise AssertionError('Actual programme failed '+s.id)
    w.advance(90)
    if not w.event(s.event,c.tag):raise AssertionError('Actual callback failed '+s.event)
    return before


class NationalRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.baselines={mode:initialized(mode)for mode in('full','experimental','disabled')}

    def ready(self,b,choice=1,mode='full'):
        w=copy.deepcopy(self.baselines[mode]);c=w.countries[b.tag];w.today=date(2021,1,1).toordinal()
        parent=next(row for row in SNP_BRANCHES if row.tag==b.tag and row.key==b.parent)
        # Focus-completion observations represent the already-earned parent tree;
        # its funded period/payment/completion still executes the actual owner.
        c.completed.update(prerequisites(parent,0))
        for i in(0,choice,3):w.complete(focus_id(parent,i),b.tag)
        service=next(s for s in SERVICES if s.branch==parent and s.index==choice-1)
        finish_service(w,service)
        for i in(4,5):w.complete(focus_id(parent,i),b.tag)
        module=next(m for m in countries()if m.TAG==b.tag)
        if b==module.BRANCHES[-1]:
            for before in module.BRANCHES[:2]:c.flags[before.id+'_review_done']=None
        w.complete(b.focus(0),b.tag);w.complete(b.focus(choice),b.tag)
        if len(b.steps)>4:w.complete(b.id+'_protocol',b.tag)
        return w,c,service

    def answer(self,w,tag,number,choice):
        name=prefix(tag)+'_message_'+str(number)+'_reply_'+str(choice)
        w.run(name,tag)

    def test_every_country_focus_path_requires_fresh_real_funded_work_in_all_fiscal_modes(self):
        visited=set()
        for b in branches():
            for choice in(1,2):
                for mode in self.baselines:
                    w,c,s=self.ready(b,choice,mode);inherited={k:v for k,v in c.flags.items()if k.startswith(('YUK_fp_','ac_yuk_'))}
                    if len(b.steps)>4:
                        self.assertFalse(w.trigger(w.triggers[b.id+'_fresh_work'],c))
                        before=finish_service(w,s)
                        self.assertEqual(before.pp-(30 if b.tag=='OSE'and before.variables['ac_snp_ose_'+('public'if choice==1 else'security')]>=65 else 35),c.pp)
                        self.assertEqual(before.variables['ac_pol_capacity']-4,c.variables['ac_pol_capacity'])
                        if mode=='full':self.assertEqual(before.variables['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash'])
                        elif mode=='experimental':self.assertEqual(before.variables['ac_econ_treasury']-2,c.variables['ac_econ_treasury'])
                        else:self.assertEqual({k:v for k,v in before.variables.items()if k.startswith(('ac_macro_','ac_econ_'))},{k:v for k,v in c.variables.items()if k.startswith(('ac_macro_','ac_econ_'))})
                        w.complete(b.id+'_review',b.tag)
                        if len(b.steps)==8:w.complete(b.focus(5 if choice==1 else 6),b.tag)
                    w.complete(b.id+'_settlement',b.tag)
                    for i in([0,choice,3,4,5 if choice==1 else 6,7]if len(b.steps)==8 else[0,choice,3,4,5]if len(b.steps)==6 else[0,choice,3]):
                        ident=b.focus(i);visited.add(ident);before=copy.deepcopy(c);w.run(ident+'_apply',b.tag);self.assertEqual(before,c)
                    self.assertEqual(inherited,{k:v for k,v in c.flags.items()if k.startswith(('YUK_fp_','ac_yuk_'))})
                    other=b.focus(3-choice);before=copy.deepcopy(c);w.run(other+'_apply',b.tag);self.assertEqual(before,c)
        self.assertEqual({b.focus(i)for b in branches()for i in range(len(b.steps))},visited)

    def test_cancelled_due_period_and_other_branch_receipts_cannot_replace_fresh_evidence(self):
        for b in branches():
            if len(b.steps)==4:continue
            w,c,s=self.ready(b);old=c.variables[s.prefix+'_last_completed_started'];w.advance(90);w.run(s.id+'_start',b.tag);w.advance(90);w.run(s.id+'_cancel',b.tag)
            self.assertIn(s.id+'_completed',c.flags);self.assertEqual(90,c.variables[s.prefix+'_elapsed'])
            self.assertEqual(old,c.variables[s.prefix+'_last_completed_started']);self.assertFalse(w.trigger(w.triggers[b.id+'_fresh_work'],c))
            before=copy.deepcopy(c);w.run(b.id+'_review_apply',b.tag);self.assertEqual(before,c)
            wrong=next(other for other in SERVICES if other.branch.tag==b.tag and other.branch.key!=b.parent)
            c.variables[wrong.prefix+'_last_completed_started']=D(w.today);c.variables[wrong.prefix+'_last_completed_on']=D(w.today)
            self.assertFalse(w.trigger(w.triggers[b.id+'_fresh_work'],c))

    def test_interruption_and_rapid_return_require_paid_present_day_renewal(self):
        for hook in('on_annex','on_capitulation_immediate','on_subject_annexed'):
            for b in branches():
                if len(b.steps)==4:continue
                w,c,s=self.ready(b);w.advance(90);w.run(s.id+'_start',b.tag);w.advance(31)
                w.national_action(b.tag,hook,'ERU'if hook=='on_annex'else b.tag,b.tag if hook=='on_annex'else None)
                self.assertNotIn(b.id+'_request_open',c.flags)
                before=copy.deepcopy(c);w.run(b.id+'_review_apply',b.tag);self.assertEqual(before,c)
                w.run(b.id+'_renew',b.tag);self.assertEqual(before.pp-10,c.pp);self.assertEqual(before.variables['ac_pol_capacity']-2,c.variables['ac_pol_capacity'])
                renewed=c.variables[prefix(b.tag)+'_'+b.key+'_requested'];snapshot=copy.deepcopy(c);w.run(b.id+'_renew',b.tag);self.assertEqual(snapshot,c)
                w.advance(59);w.event(s.event,b.tag)
                self.assertLess(c.variables[s.prefix+'_last_completed_started'],renewed);self.assertFalse(w.trigger(w.triggers[b.id+'_fresh_work'],c))
                finish_service(w,s);self.assertTrue(w.trigger(w.triggers[b.id+'_fresh_work'],c))

    def test_renewal_cost_failures_fresh_receipt_identity_and_subject_domestic_use(self):
        for b in branches():
            if len(b.steps)==4:continue
            w,c,s=self.ready(b);w.run(prefix(b.tag)+'_interrupt',b.tag)
            for reason in('pp','capacity','capitulated','no_control'):
                bad=copy.deepcopy(w);target=bad.countries[b.tag]
                if reason=='pp':target.pp=D(9)
                elif reason=='capacity':target.variables['ac_pol_capacity']=D(1)
                elif reason=='capitulated':target.capitulated=True
                else:
                    for state in bad.states.values():
                        if state.owner==b.tag:state.controller='ERU'
                before=copy.deepcopy(target);bad.run(b.id+'_renew',b.tag);self.assertEqual(before,target)
            c.subject=True;w.run(b.id+'_renew',b.tag);finish_service(w,s)
            self.assertTrue(w.trigger(w.triggers[b.id+'_fresh_work'],c))
            c.variables[s.prefix+'_last_completed_identity']+=D(100)
            self.assertFalse(w.trigger(w.triggers[b.id+'_fresh_work'],c))

    def test_every_national_message_option_is_once_only_and_expires_without_benefit(self):
        for module in countries():
            tag=module.TAG;p=prefix(tag)
            w=copy.deepcopy(self.baselines['full']);c=w.countries[tag]
            messages={ident:node for ident,node in w.events_by_id.items()if ident.startswith(p+'.')}
            self.assertEqual(14,len(messages))
            for ident,node in messages.items():
                number=int(ident.split('.')[1]);token=p+'_message_'+str(number)
                for choice in(0,1):
                    live=copy.deepcopy(w);target=live.countries[tag];target.flags[token+'_pending']=None;target.flags[token+'_window']=live.today+60
                    live.run(token+'_reply_'+str(choice),tag);self.assertIn(token+'_answered',target.flags)
                    before=copy.deepcopy(target);live.run(token+'_reply_'+str(choice),tag);self.assertEqual(before,target)
                    for failure in('expired','annexed','clone','identity'):
                        bad=copy.deepcopy(w);target=bad.countries[tag];target.flags[token+'_pending']=None;target.flags[token+'_window']=bad.today+(0 if failure=='expired'else 60)
                        if failure=='annexed':bad.national_action(tag,'on_annex','ERU',tag)
                        elif failure=='clone':target.tag='D01'
                        elif failure=='identity':target.variables[p+'_identity']+=1
                        before=copy.deepcopy(target);bad.run(token+'_reply_'+str(choice),tag);self.assertEqual(before,target,(ident,failure))

    def test_verification_public_api_requires_real_choice_and_fresh_assessment(self):
        for module in countries():
            b=module.BRANCHES[1 if module.TAG=='OSE'else 0]
            for choice in(1,2):
                w,c,s=self.ready(b,choice);index=module.BRANCHES.index(b)
                if module.TAG=='YUK':c.ideas.add('yuk_reformed_field_command'if choice==1 else'yuk_expeditionary_command')
                name='ac_snc_'+module.TAG.lower()+'_verification_earned'
                self.assertFalse(w.trigger(w.triggers[name],c));self.answer(w,b.tag,10+index,choice-1)
                finish_service(w,s);w.complete(b.id+'_review',b.tag);self.answer(w,b.tag,20+index,choice-1)
                if len(b.steps)==8:w.complete(b.focus(5 if choice==1 else 6),b.tag)
                w.complete(b.id+'_settlement',b.tag);self.assertTrue(w.trigger(w.triggers[name],c))
                c.flags.pop(prefix(b.tag)+'_message_'+str(10+index)+'_public',None)
                c.flags.pop(prefix(b.tag)+'_message_'+str(20+index)+'_staff',None)
                self.assertFalse(w.trigger(w.triggers[name],c))

    def test_late_initialization_reload_and_cloned_tags_cannot_reseed_or_replay(self):
        for year in(1991,2006,2011,2025):
            w=World('disabled',new=False).initialize_both();w.today=date(year,1,1).toordinal();w.snp_action('on_startup')
            for module in countries():
                tag=module.TAG;c=w.countries[tag];before=(c.pp,copy.deepcopy(c.equipment),{k:v for k,v in c.variables.items()if not k.startswith('ac_snc_')})
                w.national_action(tag,'on_startup');snapshot=copy.deepcopy(c);w.national_action(tag,'on_startup');w.run(prefix(tag)+'_weekly',tag);self.assertEqual(snapshot,c)
                self.assertEqual(before,(c.pp,c.equipment,{k:v for k,v in c.variables.items()if not k.startswith('ac_snc_')}))
                self.assertFalse(any('_message_'in key for key in c.flags))
        b=branches()[0];w,c,s=self.ready(b);restored=copy.deepcopy(w);restored.national_action(b.tag,'on_startup');self.assertEqual(c,restored.countries[b.tag])
        for world in(w,restored):finish_service(world,s);world.complete(b.id+'_review',b.tag)
        self.assertEqual(w.countries[b.tag],restored.countries[b.tag])
        c=w.countries[b.tag];c.tag='D01';before=copy.deepcopy(c)
        for name in(prefix(b.tag)+'_weekly',b.id+'_renew',b.id+'_settlement_apply'):w.run(name,b.tag)
        self.assertEqual(before,c)


if __name__=='__main__':unittest.main(verbosity=2)
