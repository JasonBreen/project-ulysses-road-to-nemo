"""Execute release maintenance/development against the real account owners."""
import copy,json,sys,unittest
from decimal import Decimal as D
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from release_harness import World,ROOT,MOD,parse,get,walk

def release(w,tag='REC',states=(316,)):
    w.release_action('on_startup')
    for ident in states:w.states[ident].owner=w.states[ident].controller=tag
    w.release_action('on_release_as_free',tag,'GEB')
    return w.countries[tag]

class Physical(unittest.TestCase):
    def test_new_release_transport_and_templates_once_but_existing_saves_receive_neither(self):
        w=World();c=release(w);self.assertEqual({'train_equipment_1':2,'motorized_equipment_1':12,'convoy_1':6},c.equipment)
        self.assertEqual(0,w.armies['REC']);self.assertIn('infantry_weapons1',w.research['REC'])
        before=copy.deepcopy((c.equipment,w.native_log))
        for _ in range(3):w.release_action('on_release_as_free','REC','GEB');w.release_action('on_monthly','REC')
        self.assertEqual(before,(c.equipment,w.native_log))
        old=World(new=False);old.states[316].owner=old.states[316].controller='REC';old.release_action('on_startup')
        self.assertEqual({},old.countries['REC'].equipment)
        self.assertFalse(any(n[0]=='load_oob' for n in old.native_log))

    def test_registered_account_and_kit_are_not_recreated_after_annex_rerelease(self):
        w=World();c=release(w);c.equipment={'infantry_equipment_1':17};w.release_action('on_annex','BLK','REC')
        w.states[316].owner=w.states[316].controller='BLK';w.states[316].owner=w.states[316].controller='REC'
        w.release_action('on_release_as_free','REC','BLK');self.assertEqual({'infantry_equipment_1':17},c.equipment)

    def test_actual_dlc_certification_unlocks_recipes_without_capacity_or_resource_grants(self):
        contract=json.loads((HERE/'physical_contract.json').read_text())
        for bba,mtg in product((False,True),repeat=2):
            dlcs=(['By Blood Alone'] if bba else [])+(['Man the Guns'] if mtg else [])
            w=World(dlcs=dlcs);c=release(w,'REL',(173,207,236,597));c.observables.update(num_of_military_factories=0,num_of_naval_factories=0);c.pp=D(1000)
            physical=copy.deepcopy((w.buildings,w.resource_balances,c.equipment,w.armies,w.production))
            for role,row in contract['cases'][f'bba{int(bba)}_mtg{int(mtg)}'].items():
                w.run('ac_release_REL_certify_'+role,'REL');self.assertIn('ac_release_REL_licensed_'+role+f'_bba{int(bba)}_mtg{int(mtg)}',w.globals)
                self.assertTrue(set(row['technologies'])<=w.research['REL'])
                if row['modules']:
                    variant=w.variants['REL']['REL Release '+role];self.assertEqual(row['equipment'],get(variant,'type'));self.assertEqual(row['modules'],{k:v for k,_,v in get(variant,'modules')})
                before=copy.deepcopy((w.variants,c.pp,w.research));w.run('ac_release_REL_certify_'+role,'REL');self.assertEqual(before,(w.variants,c.pp,w.research))
            self.assertEqual(D(950),c.pp);self.assertEqual(physical,(w.buildings,w.resource_balances,c.equipment,w.armies,w.production))

    def test_retired_queue_ids_are_inert_with_busy_deleted_and_historical_lines(self):
        from physical import TAGS,ROLES
        for old_receipts in (False,True):
            w=World();c=release(w);c.observables.update(num_of_military_factories=1,num_of_naval_factories=1)
            c.variables.update(ac_release_reserved_mil=D(99),ac_release_reserved_yards=D(99))
            w.production['REC']=[parse('equipment = { type = infantry_equipment_1 creator = REC } requested_factories = 1')]
            if old_receipts:
                w.globals.update('ac_release_'+tag+'_queue_'+role for tag in TAGS for role in ROLES)
                w.production['REC']=[]  # Manual deletion does not reset history.
            before=copy.deepcopy((c,w.globals,w.production,w.buildings,w.resource_balances,w.research,w.variants,w.native_log))
            for tag in TAGS:
                for role in ROLES:w.run('ac_release_'+tag+'_queue_'+role,'REC')
            w.run('ac_release_quote_maintenance_capacity','REC')
            self.assertEqual(before,(c,w.globals,w.production,w.buildings,w.resource_balances,w.research,w.variants,w.native_log))
            self.assertTrue(w.trigger([('ac_release_REC_can_certify_fighter','=','yes')],c))
            category=get(parse((MOD/'common/decisions/ac_release_maintenance.txt').read_text()),'ac_release_REC_maintenance')
            for role in ROLES:
                decision=get(category,'ac_release_REC_queue_'+role)
                self.assertFalse(w.trigger(get(decision,'visible'),c));self.assertFalse(w.trigger(get(decision,'available'),c))

    def test_maintenance_registration_preserves_inert_historical_purchase_counters(self):
        w=World(new=False);w.states[316].owner=w.states[316].controller='REC';w.release_action('on_startup');c=w.countries['REC']
        c.variables.update(ac_release_reserved_mil=D(9),ac_release_reserved_yards=D(4));w.globals.add('ac_release_REC_queue_rifles')
        w.run('ac_release_REC_prepare_maintenance','REC')
        self.assertEqual(D(9),c.variables['ac_release_reserved_mil']);self.assertEqual(D(4),c.variables['ac_release_reserved_yards']);self.assertIn('ac_release_REC_queue_rifles',w.globals)
        for folder in ('scripted_effects','scripted_triggers'):
            text=(MOD/'common'/folder/'ac_release_maintenance.txt').read_text()
            self.assertNotIn('ac_release_reserved_',text);self.assertNotIn('ac_release_free_',text);self.assertNotIn('add_equipment_production',text)

    def test_public_fee_rechecks_fractional_boundary_and_rejects_nonrelease(self):
        for mode,stock,amount in [('full','ac_macro_cash',D('.02')),('experimental','ac_econ_treasury',D(20))]:
            w=World(mode);c=release(w);c.variables[stock]=amount-D('.00001')
            w.run('ac_econ_try_fund_release_project','REC');self.assertNotIn('ac_econ_release_project_funded',c.flags)
            self.assertEqual(amount-D('.00001'),c.variables[stock]);c.variables[stock]=amount
            w.run('ac_econ_try_fund_release_project','REC');self.assertIn('ac_econ_release_project_funded',c.flags);self.assertEqual(D(0),c.variables[stock])
            before=copy.deepcopy(w.countries['BLK'].variables);w.run('ac_econ_try_fund_release_project','BLK');self.assertEqual(before,w.countries['BLK'].variables)

    def test_factory_projects_cost_once_take_ninety_days_and_recheck_owned_core_slots(self):
        for mode in ('full','experimental','disabled'):
            w=World(mode);c=release(w);c.pp=D(300);c.variables.update(ac_macro_cash=D('.04'),ac_econ_treasury=D(40))
            before=w.buildings[316].get('industrial_complex',0)
            w.run('ac_release_REC_start_civilian','REC');self.assertEqual(D(200),c.pp)
            w.run('ac_release_REC_start_civilian','REC');self.assertEqual(D(200),c.pp)
            w.fire('ac_release.102','REC');self.assertEqual(before,w.buildings[316].get('industrial_complex',0))
            w.today+=90;w.fire('ac_release.102','REC');self.assertEqual(before+1,w.buildings[316]['industrial_complex'])
            w.fire('ac_release.102','REC');w.today+=40;w.run('ac_release_REC_start_civilian','REC');self.assertEqual(D(200),c.pp)

    def test_lost_state_slot_capitulation_and_annex_interrupt_without_refund_or_free_build(self):
        for interruption in ('state','slot','capitulation','annex'):
            w=World();c=release(w);c.variables['ac_macro_cash']=D('.04');before=copy.deepcopy(w.buildings)
            w.run('ac_release_REC_start_military','REC')
            if interruption=='state':w.states[316].owner=w.states[316].controller='BLK'
            elif interruption=='slot':w.free_slots[316]=0
            elif interruption=='capitulation':c.capitulated=True
            else:w.release_action('on_annex','BLK','REC')
            w.today+=90;w.fire('ac_release.103','REC')
            self.assertEqual(before,w.buildings);self.assertEqual(D('.02'),c.variables['ac_macro_cash'])
            self.assertNotIn('ac_release_REC_military_built',w.globals)

    def test_stale_callback_cannot_finish_a_retried_project_early(self):
        w=World();c=release(w);c.variables['ac_macro_cash']=D('.06');before=w.buildings[316].get('arms_factory',0)
        w.run('ac_release_REC_start_military','REC');w.today+=10;w.run('ac_release_REC_cancel_military','REC')
        w.today+=30;w.run('ac_release_REC_start_military','REC');w.today+=50
        w.fire('ac_release.103','REC');self.assertEqual(before,w.buildings[316].get('arms_factory',0))
        w.today+=40;w.fire('ac_release.103','REC');self.assertEqual(before+1,w.buildings[316]['arms_factory'])
        self.assertEqual(D('.02'),c.variables['ac_macro_cash'])

    def test_no_core_liability_is_not_repaired_by_free_core_or_manpower_law(self):
        w=World();c=release(w,'AWW',(272,));before=copy.deepcopy(w.core_states);c.variables['ac_macro_cash']=D(10)
        self.assertFalse(w.trigger(parse('ac_release_can_invest = yes'),c));w.run('ac_release_AWW_start_military','AWW')
        self.assertEqual(before,w.core_states);self.assertNotIn('ac_release_AWW_military_active',c.flags)
        source=''.join((MOD/'common/scripted_effects'/name).read_text() for name in ('ac_release_foundations.txt','ac_release_maintenance.txt'))
        self.assertNotIn('add_manpower',source);self.assertNotIn('add_core_of',source);self.assertNotIn('set_popularities',source)

    def test_paid_network_builds_only_missing_owned_edges_after_ninety_days(self):
        contract=json.loads((HERE/'physical_contract.json').read_text())['networks']['countries']
        for tag,cases in contract.items():
            for case in cases:
                if not case['missing_edges']:continue
                with self.subTest(tag=tag,case=case['id']):
                    w=World();c=release(w,tag,case['states']);c.variables['ac_macro_cash']=D('.04')
                    for p in case['controlled_exclusions']:w.province_controllers[p]='BLK'
                    w.run('ac_release_'+tag+'_start_network',tag)
                    self.assertIn('ac_release_'+tag+'_network_active',c.flags)
                    event='ac_release.'+str(200+list(contract).index(tag));w.fire(event,tag);self.assertEqual([],w.railways)
                    w.today+=90;w.fire(event,tag)
                    self.assertEqual({tuple(edge) for edge in case['missing_edges']},{tuple(path) for owner,level,path in w.railways})
                    before=copy.deepcopy((w.railways,c.pp,c.variables['ac_macro_cash']));w.fire(event,tag);w.run('ac_release_'+tag+'_start_network',tag)
                    self.assertEqual(before,(w.railways,c.pp,c.variables['ac_macro_cash']))

    def test_network_interrupts_on_lost_route_and_unknown_shapes_have_no_guessed_path(self):
        w=World();c=release(w,'REL',(173,207,236,597));c.variables['ac_macro_cash']=D('.04');w.run('ac_release_REL_start_network','REL')
        data=json.loads((HERE/'physical_contract.json').read_text())['networks']['countries']['REL'][0]
        w.province_controllers[data['missing_edges'][0][0]]='ERU';w.release_action('on_monthly','REL');w.today+=90;w.fire('ac_release.202','REL')
        self.assertEqual([],w.railways);self.assertNotIn('ac_release_REL_network_done',w.globals);self.assertEqual(D('.02'),c.variables['ac_macro_cash'])
        w=World();c=release(w,'REL',(316,));c.variables['ac_macro_cash']=D(10)
        self.assertFalse(w.trigger(parse('ac_release_REL_known_network = yes'),c));w.run('ac_release_REL_start_network','REL')
        self.assertEqual([],w.railways);self.assertEqual(D(10),c.variables['ac_macro_cash'])

    def test_network_never_redeclares_a_newly_built_higher_level_edge(self):
        w=World();c=release(w,'REL',(173,207,236,597));c.variables['ac_macro_cash']=D('.04');w.run('ac_release_REL_start_network','REL')
        case=json.loads((HERE/'physical_contract.json').read_text())['networks']['countries']['REL'][0];edge=tuple(case['missing_edges'][0]);w.railway_levels[edge]=4
        w.today+=90;w.fire('ac_release.202','REL');self.assertEqual(4,w.railway_levels[edge]);self.assertNotIn(edge,{tuple(path) for _,_,path in w.railways})

    def test_only_existing_office_identity_adapts_to_puppet_government(self):
        for tag,states in [('REL',(173,207,236,597)),('REC',(316,)),('SHI',(426,447,607))]:
            w=World();w.countries[tag].government='fascism';release(w,tag,states)
            roles=[n for n in w.native_log if n[0]=='add_country_leader_role']
            if tag=='REL':self.assertEqual('REL_ac_government_office',get(roles[0][2],'character'))
            else:self.assertEqual(tag+'_ac_release_government_office',get(roles[0][2],'character'))

    def test_interpreter_does_not_execute_inner_else_under_a_failed_outer_guard(self):
        w=World();c=w.countries['REC']
        w.execute(parse('if = { limit = { always = no } if = { limit = { always = no } set_country_flag = inner_yes } else = { set_country_flag = inner_no } }'),c)
        self.assertNotIn('inner_no',c.flags)
        w.execute(parse('if = { limit = { always = no } set_country_flag = nested_yes else = { set_country_flag = nested_no } }'),c)
        self.assertIn('nested_no',c.flags)

    def test_manual_rotation_certifies_without_a_factory_or_duplicate_variant(self):
        w=World(dlcs=['By Blood Alone']);c=release(w);c.observables['num_of_military_factories']=0
        before=copy.deepcopy(c.equipment);w.run('ac_release_REC_certify_fighter','REC');self.assertEqual([],w.production['REC']);self.assertEqual(before,c.equipment)
        self.assertIn('REC Release fighter',w.variants['REC']);count=len(w.variants['REC']);pp=c.pp
        w.run('ac_release_REC_certify_fighter','REC');self.assertEqual((count,pp),(len(w.variants['REC']),c.pp))
        c.observables['num_of_military_factories']=1;w.resource_balances['REC'].update(aluminium=100,rubber=100)
        w.run('ac_release_REC_queue_fighter','REC');self.assertEqual([],w.production['REC']);self.assertEqual(count,len(w.variants['REC']))
        # Explicit manual Production observation, outside the decision owner.
        row=json.loads((HERE/'physical_contract.json').read_text())['cases']['bba1_mtg0']['fighter']
        w.execute(parse('add_equipment_production = { equipment = { type = '+row['equipment']+' creator = REC version_name = "REC Release fighter" } requested_factories = 1 efficiency = 50 progress = 0 }'),c)
        self.assertEqual(1,len(w.production['REC']))

    def test_moved_before_research_or_variant_consumer_is_rejected(self):
        w=World(dlcs=['By Blood Alone']);c=release(w);row=json.loads((HERE/'physical_contract.json').read_text())['cases']['bba1_mtg0']['fighter']
        fragment=parse('add_equipment_production = { equipment = { type = '+row['equipment']+' creator = REC version_name = "REC Release fighter" } requested_factories = 1 efficiency = 50 progress = 0 }')
        with self.assertRaisesRegex(ValueError,'before required research'):w.execute(fragment,c)
        w.research['REC'].update(row['technologies'])
        with self.assertRaisesRegex(ValueError,'before selected variant'):w.execute(fragment,c)

    def test_actual_decision_bindings_execute_hidden_owners_and_localized_requirements(self):
        w=World(dlcs=['By Blood Alone']);c=release(w);c.variables['ac_macro_cash']=D('.04');c.observables['num_of_military_factories']=1;w.resource_balances['REC'].update(aluminium=100,rubber=100)
        category=get(parse((MOD/'common/decisions/ac_release_maintenance.txt').read_text()),'ac_release_REC_maintenance')
        for ident in ('ac_release_REC_certify_fighter','ac_release_REC_develop_civilian','ac_release_REC_cancel_civilian'):
            decision=get(category,ident)
            self.assertTrue(w.trigger(get(decision,'visible'),c),ident)
            self.assertTrue(w.trigger(get(decision,'available',[]),c),ident)
            self.assertTrue(any(k=='custom_effect_tooltip' for k,_,_ in get(decision,'complete_effect')))
            w.execute(get(decision,'complete_effect'),c)
        retired=get(category,'ac_release_REC_queue_fighter');self.assertFalse(w.trigger(get(retired,'visible'),c));self.assertFalse(w.trigger(get(retired,'available'),c))
        before=copy.deepcopy((c.pp,w.globals,w.production));w.execute(get(retired,'complete_effect'),c);self.assertEqual(before,(c.pp,w.globals,w.production))
        self.assertEqual([],w.production['REC']);self.assertNotIn('ac_release_project_active',c.flags);self.assertEqual(D('.02'),c.variables['ac_macro_cash'])

    def test_monthly_owner_recovers_a_paid_due_project_without_replaying_a_callback(self):
        w=World();c=release(w);c.variables['ac_macro_cash']=D('.04');before=w.buildings[316].get('arms_factory',0)
        w.run('ac_release_REC_start_military','REC');w.today+=91
        # Drop the queued callback fixture: monthly supervision must still
        # finish once, after the actual wait flag expires and target recheck.
        w.events=[];w.release_action('on_monthly','REC');self.assertEqual(before+1,w.buildings[316]['arms_factory'])
        w.release_action('on_monthly','REC');w.fire('ac_release.103','REC');self.assertEqual(before+1,w.buildings[316]['arms_factory']);self.assertEqual(D('.02'),c.variables['ac_macro_cash'])

if __name__=='__main__':unittest.main(verbosity=2)
