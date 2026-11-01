"""Actual-source national contracts, real P1 money/capacity and release owners.

These are source/Decimal observations, not engine, pacing or native saves.
"""
import copy
from datetime import date
from decimal import Decimal as D
from itertools import product
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from content import FOCUSES,COUNTRIES,POLICIES
import build
from programmes import ALLOCATIONS,STANDING
from obligations import WARRANTS,CASES
from narrative import SCENES
from owner_harness import baseline,World,get,parse,MOD,ROOT

def enable(w,tag='FAT'):
    c=w.countries[tag]
    for row in FOCUSES:
        if row.tag==tag:
            c.flags[row.id+'_done']=None
            if row.kind=='capability':c.flags['ac_fsb_'+row.hook]=None
    c.flags['ac_fsb_invoice_verified']=None
    return c

def flag(c,key):return key in c.flags
def account(c):return {k:v for k,v in c.variables.items() if k.startswith(('ac_macro_','ac_econ_'))}

class CampaignOwners(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.baselines={mode:baseline(mode) for mode in ('full','experimental','disabled')}
    def world(self,mode='full'):return copy.deepcopy(self.baselines[mode])

    def test_initializer_never_grants_forces_industry_stock_or_public_money(self):
        for mode in self.baselines:
            w=self.world(mode)
            for tag in ('FAT','SBK'):
                c=w.countries[tag];before=copy.deepcopy(c);states=copy.deepcopy(w.states);armies=copy.deepcopy(w.armies)
                for _ in range(3):w.run('ac_fsb_initialize',tag)
                self.assertEqual(before,c);self.assertEqual(states,w.states);self.assertEqual(armies,w.armies)

    def test_every_paid_action_reaches_actual_payment_and_capacity_in_three_modes(self):
        free={'suspend_warrants','sweep_warrants','public_interest','interruption_review'}
        for row in (r for r in FOCUSES if r.kind=='action' and r.hook not in free):
            for mode in self.baselines:
                with self.subTest(action=row.hook,mode=mode):
                    w=self.world(mode);c=enable(w,row.tag);before=account(c);pp=c.pp;cap=c.variables['ac_pol_capacity'];stock=copy.deepcopy(c.equipment)
                    self.assertTrue(w.choose(row.tag+'_fsb_'+row.hook,row.tag))
                    self.assertEqual(pp-20,c.pp)
                    expected_cap=cap+3 if row.hook=='invoice_audit' else cap+4 if row.hook in ('local_reconciliation','commitment_review') else cap-2
                    self.assertEqual(expected_cap,c.variables['ac_pol_capacity'])
                    if mode=='full':self.assertEqual(before['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash'])
                    elif mode=='experimental':self.assertEqual(before['ac_econ_treasury']-2,c.variables['ac_econ_treasury'])
                    else:self.assertEqual(before,account(c))
                    for kind,amount in ALLOCATIONS[row.hook][2].items():self.assertEqual(stock[kind]-amount,c.equipment[kind])
                    snapshot=copy.deepcopy(c)
                    self.assertFalse(w.choose(row.tag+'_fsb_'+row.hook,row.tag))
                    self.assertEqual(snapshot,c)

    def test_cash_arrears_capacity_stock_and_control_fail_without_charges(self):
        for failure in ('cash','arrears','capacity','stock','occupation','capitulation','identity'):
            w=self.world();c=enable(w,'SBK')
            if failure=='cash':c.variables['ac_macro_cash']=D('.001')
            elif failure=='arrears':c.variables['ac_macro_arrears']=D('.001')
            elif failure=='capacity':c.variables['ac_pol_capacity']=D(1)
            elif failure=='stock':c.equipment['support_equipment']=9
            elif failure=='occupation':w.states[302].controller='BLK'
            elif failure=='capitulation':c.capitulated=True
            else:c.original_tag='BLK'
            before=copy.deepcopy(c);self.assertFalse(w.choose('SBK_fsb_workshop_round','SBK'),failure);self.assertEqual(before,c)

    def test_shift_choices_cannot_stack_and_repeat_after_real_cooldown_only(self):
        w=self.world();c=enable(w)
        self.assertTrue(w.choose('FAT_fsb_extra_shift','FAT'))
        self.assertFalse(w.choose('FAT_fsb_rest_interval','FAT'))
        w.advance(91);self.assertFalse(w.choose('FAT_fsb_rest_interval','FAT'))
        w.advance(90);self.assertTrue(w.choose('FAT_fsb_rest_interval','FAT'))
        self.assertNotIn('ac_fsb_fat_extra_shift',c.ideas)

    def test_stock_warrants_require_consent_then_move_actual_stock_exactly_once(self):
        for partner,kind in product(('GEB','REC','OSE'),WARRANTS):
            w=self.world();c=enable(w);receiver=w.countries[partner];_,equipment,quantity,_=WARRANTS[kind]
            before=c.equipment[equipment];received=receiver.equipment[equipment]
            request='FAT_fsb_request_'+partner.lower()+'_'+kind;dispatch='FAT_fsb_deliver_'+partner.lower()+'_'+kind
            self.assertTrue(w.choose(request,'FAT'));self.assertEqual(before,c.equipment[equipment])
            self.assertFalse(w.choose(dispatch,'FAT'))
            self.assertTrue(w.choose(partner+'_fsb_reply_'+partner.lower()+'_'+kind+'_accept',partner))
            self.assertEqual(before,c.equipment[equipment]);self.assertEqual(received,receiver.equipment[equipment])
            self.assertTrue(w.choose(dispatch,'FAT'));self.assertEqual(before-quantity,c.equipment[equipment]);self.assertEqual(received+quantity,receiver.equipment[equipment])
            snapshot=(copy.deepcopy(c),copy.deepcopy(receiver));w.run(dispatch+'_apply','FAT')
            self.assertEqual(snapshot,(c,receiver));self.assertEqual(0,c.variables['ac_fsb_warrants_open'])

    def test_domestic_reserve_boundary_and_receiver_revocation_are_real(self):
        w=self.world();c=enable(w);c.equipment['infantry_equipment']=899
        w.choose('FAT_fsb_request_geb_infantry','FAT');w.choose('GEB_fsb_reply_geb_infantry_accept','GEB')
        self.assertFalse(w.choose('FAT_fsb_deliver_geb_infantry','FAT'))
        c.equipment['infantry_equipment']=900;self.assertTrue(w.choose('GEB_fsb_reply_geb_infantry_revoke','GEB'))
        self.assertFalse(w.choose('FAT_fsb_deliver_geb_infantry','FAT'));self.assertEqual(900,c.equipment['infantry_equipment'])

    def test_open_slot_ceiling_counts_pending_and_accepted_and_never_exceeds_three(self):
        w=self.world();c=enable(w)
        for cap in ('second_warrant','third_warrant'):c.flags.pop('ac_fsb_'+cap,None)
        self.assertTrue(w.choose('FAT_fsb_request_geb_infantry','FAT'))
        self.assertFalse(w.choose('FAT_fsb_request_rec_support','FAT'))
        c.flags['ac_fsb_second_warrant']=None;self.assertTrue(w.choose('FAT_fsb_request_rec_support','FAT'))
        w.choose('GEB_fsb_reply_geb_infantry_accept','GEB');self.assertFalse(w.choose('FAT_fsb_request_ose_mobility','FAT'))
        c.flags['ac_fsb_third_warrant']=None;self.assertTrue(w.choose('FAT_fsb_request_ose_mobility','FAT'))
        self.assertFalse(w.choose('FAT_fsb_request_rec_mobility','FAT'));self.assertEqual(3,c.variables['ac_fsb_warrants_open'])

    def test_invalid_partner_expiry_annexation_war_subject_and_stale_apply_close_without_reward(self):
        for failure in ('expiry','war','sender_subject','receiver_subject','capitulation','annexation','clone'):
            w=self.world();c=enable(w);receiver=w.countries['GEB'];w.choose('FAT_fsb_request_geb_infantry','FAT');w.choose('GEB_fsb_reply_geb_infantry_accept','GEB')
            before=copy.deepcopy(c.equipment)
            if failure=='expiry':w.advance(91)
            elif failure=='war':c.wars.add('GEB')
            elif failure=='sender_subject':c.subject_of='BLK'
            elif failure=='receiver_subject':receiver.subject_of='BLK'
            elif failure=='capitulation':receiver.capitulated=True
            elif failure=='clone':receiver.original_tag='BLK'
            else:
                for state in w.states.values():
                    if state.owner=='GEB':state.owner=state.controller='BLK'
            w.run('ac_fsb_warrant_tick','FAT');w.run('FAT_fsb_deliver_geb_infantry_apply','FAT')
            self.assertEqual(before,c.equipment,failure);self.assertEqual(0,c.variables['ac_fsb_deliveries']);self.assertEqual(0,c.variables['ac_fsb_warrants_open'])

    def test_refusal_grants_no_stock_or_money_and_domestic_alternative_pays(self):
        w=self.world();c=enable(w);w.choose('FAT_fsb_request_rec_infantry','FAT');before=account(c);stocks=copy.deepcopy(c.equipment)
        self.assertTrue(w.choose('REC_fsb_reply_rec_infantry_refuse','REC'));self.assertEqual(stocks,c.equipment);self.assertEqual(before,account(c))
        self.assertTrue(w.choose('FAT_fsb_refused_reserve','FAT'));self.assertEqual(stocks['infantry_equipment']-100,c.equipment['infantry_equipment']);self.assertEqual(before['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash'])

    def test_joint_inspection_is_an_extra_receiver_choice_not_an_automatic_reward(self):
        w=self.world();c=enable(w);w.choose('FAT_fsb_request_ose_support','FAT');receiver=w.countries['OSE'];cap=receiver.variables['ac_pol_capacity']
        self.assertTrue(w.choose('OSE_fsb_reply_ose_support_inspect','OSE'));self.assertEqual(cap-2,receiver.variables['ac_pol_capacity'])
        self.assertNotIn('ac_fsb_receiving_inspection',receiver.ideas)
        self.assertTrue(w.choose('FAT_fsb_deliver_ose_support','FAT'));self.assertIn('ac_fsb_receiving_inspection',receiver.ideas)

    def test_all_case_options_are_costed_and_only_the_actual_resolved_case_awards(self):
        for kind,(_,_,options) in CASES.items():
            for option,*_ in options:
                w=self.world();c=enable(w,'SBK');self.assertTrue(w.choose('SBK_fsb_open_'+kind,'SBK'));before=account(c);stocks=copy.deepcopy(c.equipment)
                c.flags['ac_fsb_verified_receipts']=None;c.flags['ac_fsb_indexed_archive']=None
                if option in ('ration','limited'):c.flags['ac_fsb_resident_consent']=None
                self.assertTrue(w.choose('SBK_fsb_resolve_'+kind+'_'+option,'SBK'),(kind,option))
                self.assertEqual(before['ac_macro_cash']-D('.002'),c.variables['ac_macro_cash']);self.assertEqual(1,c.variables['ac_fsb_cases_resolved'])
                self.assertIn('ac_fsb_case_'+kind+'_'+option,c.ideas);self.assertEqual(0,c.variables['ac_fsb_cases_open'])
                snapshot=copy.deepcopy(c);w.run('SBK_fsb_resolve_'+kind+'_'+option+'_apply','SBK');self.assertEqual(snapshot,c)

    def test_case_slot_expiry_obsolete_closure_and_interruption_never_pay_completion(self):
        w=self.world();c=enable(w,'SBK');c.flags.pop('ac_fsb_second_case')
        self.assertTrue(w.choose('SBK_fsb_open_property','SBK'));self.assertFalse(w.choose('SBK_fsb_open_utilities','SBK'))
        c.flags['ac_fsb_second_case']=None;self.assertTrue(w.choose('SBK_fsb_open_utilities','SBK'));self.assertFalse(w.choose('SBK_fsb_open_stores','SBK'))
        self.assertTrue(w.choose('SBK_fsb_close_property','SBK'));self.assertEqual(0,c.variables['ac_fsb_cases_resolved'])
        w.advance(120);w.run('ac_fsb_case_tick','SBK');self.assertEqual(0,c.variables['ac_fsb_cases_open']);self.assertEqual(0,c.variables['ac_fsb_cases_resolved'])
        before=copy.deepcopy(c);w.run('SBK_fsb_resolve_utilities_repair_apply','SBK');self.assertEqual(before,c)

    def test_appeal_replaces_old_benefit_and_is_once_per_case(self):
        w=self.world();c=enable(w,'SBK');w.choose('SBK_fsb_open_property','SBK');w.choose('SBK_fsb_resolve_property_protected','SBK')
        self.assertIn('ac_fsb_case_property_protected',c.ideas);self.assertTrue(w.choose('SBK_fsb_appeal_property','SBK'));self.assertNotIn('ac_fsb_case_property_protected',c.ideas)
        self.assertTrue(w.choose('SBK_fsb_resolve_property_interim','SBK'));self.assertFalse(w.choose('SBK_fsb_appeal_property','SBK'))
        self.assertEqual({'ac_fsb_case_property_interim'},{i for i in c.ideas if i.startswith('ac_fsb_case_property_')})

    def test_adviser_consent_subject_permission_and_domestic_refusal_route(self):
        for subject in (None,'OSE','BLK'):
            w=self.world();c=enable(w,'SBK');c.subject_of=subject
            self.assertEqual(subject!='BLK',w.choose('SBK_fsb_request_adviser','SBK'))
            if subject!='BLK':
                self.assertTrue(w.choose('OSE_fsb_refuse_sbk_adviser','OSE'));self.assertIn('ac_fsb_adviser_refused',c.flags)
            self.assertTrue(w.choose('SBK_fsb_domestic_inspection','SBK'));self.assertIn('ac_fsb_sbk_domestic_inspection',c.ideas)

    def test_standing_exact_snapshot_cleanup_deferred_after_actual_sbk_reintegration(self):
        w=self.world();c=enable(w,'SBK');base=c.variables.get('ac_macro_commitments_annual',D(0));cash=c.variables['ac_macro_cash'];debt=c.variables['ac_macro_debt']
        for action in ('civil_charter','maintenance_account','service_account'):self.assertTrue(w.choose('SBK_fsb_'+action,'SBK'))
        applied=c.variables['ac_fsb_fiscal_applied'];self.assertGreater(applied,0);self.assertEqual(base+applied,c.variables['ac_macro_commitments_annual'])
        for _ in range(3):w.run('ac_fsb_sync_commitments','SBK')
        self.assertEqual(base+applied,c.variables['ac_macro_commitments_annual'])
        w.choose('SBK_fsb_open_property','SBK');w.armies['SBK']=5;w.armies['BLK']=20
        self.assertTrue(w.fire('south_belka.5','SBK'));self.assertEqual((25,0),(w.armies['BLK'],w.armies['SBK']))
        self.assertEqual(0,c.variables['ac_fsb_cases_open']);self.assertIn('ac_fsb_fiscal_dirty',c.flags);self.assertEqual(applied,c.variables['ac_fsb_fiscal_applied'])
        self.assertFalse(any(k.endswith('_standing') and k.startswith('ac_fsb_') for k in c.flags))
        w.states[302].owner=w.states[302].controller='SBK';stocks=copy.deepcopy(c.equipment);w.run('ac_fsb_weekly','SBK')
        self.assertEqual(base,c.variables['ac_macro_commitments_annual']);self.assertEqual(0,c.variables['ac_fsb_fiscal_applied']);self.assertEqual(stocks,c.equipment);self.assertEqual(debt,c.variables['ac_macro_debt'])

    def test_real_collapse_and_both_treaty_footprints_keep_original_transfers_and_owned_capitals(self):
        for entry in ('south_belka.2','south_belka.3','south_belka.4','belka_dlp_war.101','belka_dlp_war.103'):
            w=World();w.action('on_startup');w.release_action('on_startup');w.armies['BLK']=40
            # This explicitly observes an absent-before-init country, matching
            # the real release owner rather than giving an old save start loot.
            if entry.startswith('south_'):self.assertTrue(w.fire(entry,'BLK'))
            else:
                # Treaty events contain wider existing war effects. Execute the
                # protected actual SBK state/capital fragment, checked separately
                # against the full owner's immutable operation signature.
                source=w.event_definitions[entry];fragment=[]
                for key,value in __import__('release_harness').walk(source):
                    if key=='SBK':fragment.append(('SBK','=',value))
                self.assertTrue(fragment);w.execute(fragment,w.countries['BLK'])
            w.run('ac_fsb_initialize','SBK');c=w.countries['SBK'];self.assertEqual('SBK',w.states[w.capitals['SBK']].owner)
            before=(copy.deepcopy(c.equipment),w.armies['SBK']);w.run('ac_fsb_weekly','SBK');self.assertEqual(before,(c.equipment,w.armies['SBK']))

    def test_idle_handoff_reads_actual_generic_regional_and_continuous_guards(self):
        w=self.world();c=w.countries['SBK'];c.tree='ac_regional_foundation'
        trigger_body=w.triggers['ac_pol_previous_tree_idle']+w.triggers['ac_pol_legacy_idle'];ids={value for key,value in __import__('release_harness').walk(trigger_body) if key=='has_completed_focus'}
        self.assertGreater(len(ids),36)
        for ident in ids:
            c.selected=ident;c.progress=D(0);self.assertFalse(w.choose('SBK_fsb_adopt_campaign','SBK'),ident)
            c.progress=D('.25');self.assertFalse(w.choose('SBK_fsb_adopt_campaign','SBK'),ident)
        c.selected=None;c.progress=D(0);self.assertTrue(w.choose('SBK_fsb_adopt_campaign','SBK'));self.assertEqual(COUNTRIES['SBK']['tree'],c.tree)
        c.tree='unknown_bespoke';self.assertFalse(w.choose('SBK_fsb_adopt_campaign','SBK'))

    def test_all_focus_alternatives_are_reachable_without_foreign_consent(self):
        for tag in COUNTRIES:
            rows=[r for r in FOCUSES if r.tag==tag];pairs=[(r.suffix,r.exclusive) for r in rows if r.exclusive and r.suffix<r.exclusive]
            reached=set()
            for picks in product((0,1),repeat=len(pairs)):
                w=self.world('disabled');c=w.countries[tag];w.today=date(2013,2,1).toordinal();excluded={pair[1-pick] for pair,pick in zip(pairs,picks)}
                for row in rows:
                    if row.suffix in excluded:continue
                    self.assertTrue(w.complete(row.id,tag),(tag,picks,row.id));reached.add(row.id)
            self.assertEqual({r.id for r in rows},reached)

    def test_scene_options_charge_once_and_stale_interrupted_expired_choices_are_inert(self):
        for number,tag,when in [(1,'FAT',(1991,2,1)),(9,'FAT',(2008,2,1)),(101,'SBK',(2010,2,1)),(110,'SBK',(2013,2,1))]:
            w=self.world();c=w.countries[tag];w.today=date(*when).toordinal();w.run('ac_fsb_scene_'+str(number)+'_queue',tag);before=c.variables['ac_macro_cash']
            self.assertTrue(w.fire('ac_fsb.'+str(number),tag));self.assertEqual(before-D('.002'),c.variables['ac_macro_cash'])
            snapshot=copy.deepcopy(c);w.fire('ac_fsb.'+str(number),tag,stale=True);self.assertEqual(snapshot,c)
        w=self.world();c=w.countries['FAT'];w.run('ac_fsb_scene_1_queue','FAT');w.run('ac_fsb_interrupt','FAT');before=copy.deepcopy(c);w.fire('ac_fsb.1','FAT',stale=True);self.assertEqual(before,c)
        w.run('ac_fsb_scene_1_queue','FAT');self.assertEqual(before,c);self.assertIn('ac_fsb_scene_1_cancelled',c.flags)
        w=self.world();w.today=date(2008,1,1).toordinal();c=w.countries['FAT'];before=account(c);w.run('ac_fsb_scene_1_queue','FAT');self.assertNotIn('ac_fsb_scene_1_pending',c.flags);self.assertIn('ac_fsb_scene_1_archived',c.flags);self.assertEqual(before,account(c))

    def test_quote_ui_does_not_settle_or_write_history_and_reload_does_not_repeat(self):
        w=self.world();c=enable(w,'SBK');w.choose('SBK_fsb_maintenance_account','SBK');settlements=c.variables['ac_macro_settlements'];history=c.variables['ac_macro_history_count']
        snapshot=copy.deepcopy(w)
        for _ in range(3):w.run('ac_macro_quote','SBK');w.run('ac_fsb_weekly','SBK')
        self.assertEqual(settlements,c.variables['ac_macro_settlements']);self.assertEqual(history,c.variables['ac_macro_history_count'])
        restored=copy.deepcopy(snapshot);restored.run('ac_fsb_weekly','SBK');self.assertEqual(c.variables['ac_macro_commitments_annual'],restored.countries['SBK'].variables['ac_macro_commitments_annual'])

    def test_sbk_requires_release_registration_and_adopts_existing_saves_without_grants(self):
        w=World(new=False);w.states[302].owner=w.states[302].controller='SBK';c=w.countries['SBK']
        w.run('ac_fsb_initialize','SBK');self.assertNotIn('ac_fsb_initialized',c.flags)
        before=(copy.deepcopy(c.equipment),w.armies['SBK'],copy.deepcopy(w.buildings),account(c))
        w.release_action('on_startup');w.run('ac_fsb_initialize','SBK')
        self.assertIn('ac_fsb_initialized',c.flags);self.assertIn('ac_release_adopted_existing',c.flags)
        self.assertEqual(before[0],c.equipment);self.assertEqual(before[1],w.armies['SBK']);self.assertEqual(before[2],w.buildings)
        self.assertNotIn('ac_macro_cash',c.variables)

    def test_all_twenty_scenes_offer_two_costed_choices_and_an_unfunded_close(self):
        for number,(_,first,last,*_) in SCENES.items():
            for choice in (0,1,2):
                w=self.world();tag='FAT' if number<100 else 'SBK';c=w.countries[tag]
                w.today=(date(*map(int,first.split('.'))).toordinal()+1) if first else date(1991,2,1).toordinal()
                w.run('ac_fsb_scene_'+str(number)+'_queue',tag);money=c.variables['ac_macro_cash'];pp=c.pp
                self.assertTrue(w.fire('ac_fsb.'+str(number),tag,choice),(number,choice))
                self.assertIn('ac_fsb_scene_'+str(number)+'_seen',c.flags)
                self.assertEqual(pp-(15 if choice==0 else 5 if choice==1 else 0),c.pp)
                self.assertEqual(money-(D('.002') if choice==0 else 0),c.variables['ac_macro_cash'])

    def test_active_adviser_visit_stops_on_war_and_subject_callbacks(self):
        for interrupted in ('war','subject','receiver_annex'):
            w=self.world();c=enable(w,'SBK');w.choose('SBK_fsb_request_adviser','SBK');self.assertTrue(w.choose('OSE_fsb_accept_sbk_adviser','OSE'))
            self.assertIn('ac_fsb_sbk_limited_adviser',c.ideas)
            if interrupted=='war':c.wars.add('OSE');w.run('ac_fsb_adviser_tick','SBK')
            elif interrupted=='subject':c.subject_of='BLK';w.fsb_action('on_puppet','SBK')
            else:w.fsb_action('on_annex','BLK','OSE')
            self.assertNotIn('ac_fsb_sbk_limited_adviser',c.ideas,interrupted);self.assertNotIn('ac_fsb_adviser_visit',c.flags)

    def test_removed_standing_policy_can_be_costed_again_without_double_commitment(self):
        w=self.world();c=enable(w,'SBK');initial=c.variables['ac_macro_commitments_annual'];w.choose('SBK_fsb_maintenance_account','SBK');delta=c.variables['ac_fsb_fiscal_applied']
        self.assertTrue(w.choose('SBK_fsb_public_interest','SBK'));self.assertEqual(initial,c.variables['ac_macro_commitments_annual']);cash=c.variables['ac_macro_cash']
        self.assertTrue(w.choose('SBK_fsb_maintenance_account','SBK'));self.assertEqual(cash-D('.002'),c.variables['ac_macro_cash']);self.assertEqual(initial+delta,c.variables['ac_macro_commitments_annual'])

    def test_only_latest_earned_policy_family_can_be_reinstated_after_interruption(self):
        w=self.world();c=w.countries['FAT'];c.flags['FAT_nat_civilian_priority_done']=None;c.flags['FAT_nat_essential_quota_done']=None
        self.assertFalse(w.choose('FAT_fsb_restore_civilian_priority','FAT'));self.assertTrue(w.choose('FAT_fsb_restore_essential_quota','FAT'))
        self.assertIn('ac_fsb_fat_essential_quota',c.ideas);self.assertNotIn('ac_fsb_fat_civilian_priority',c.ideas)
        self.assertFalse(w.choose('FAT_fsb_restore_essential_quota','FAT'))

    def test_last_day_of_historical_act_is_archived_at_exact_boundary(self):
        w=self.world();c=w.countries['FAT'];w.today=date(1995,1,1).toordinal();before=account(c)
        w.run('ac_fsb_scene_1_queue','FAT');self.assertIn('ac_fsb_scene_1_archived',c.flags);self.assertNotIn('ac_fsb_scene_1_pending',c.flags);self.assertEqual(before,account(c))

    def test_native_branch_adapter_preserves_nested_legacy_and_sibling_conditionals(self):
        w=self.world();c=w.countries['FAT']
        w.execute(parse('if = { limit = { always = no } set_country_flag = wrong else = { set_country_flag = nested_right } } if = { limit = { always = yes } if = { limit = { always = no } set_country_flag = wrong } else = { set_country_flag = sibling_right } }'),c)
        self.assertNotIn('wrong',c.flags);self.assertIn('nested_right',c.flags);self.assertIn('sibling_right',c.flags)

if __name__=='__main__':unittest.main()
