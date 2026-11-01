"""Actual entry scripts and real account/institution owners at release boundaries."""
import copy
from decimal import Decimal as D
import json
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from release_harness import World,ROOT,MOD,parse,get,walk


class Lifecycle(unittest.TestCase):
    def test_aww_both_options_keep_quarter_transfer_and_nine_birth_formations_once(self):
        for option in (0,1):
            with self.subTest(option=option):
                w=World();w.release_action('on_startup');w.armies['BLK']=40
                w.countries['BLK'].equipment={'infantry_equipment_1':1000};w.fuel['BLK']=D(100)
                self.assertTrue(w.fire('awwnb.1','BLK',option))
                self.assertEqual((30,10),(w.armies['BLK'],w.armies['AWW']))
                self.assertTrue(w.fire('awwnb.2','BLK'))
                self.assertEqual((30,19),(w.armies['BLK'],w.armies['AWW']))
                self.assertEqual(272,w.capitals['AWW']);self.assertEqual('AWW',w.controller(7430))
                self.assertEqual('BLK',w.controller(3269))
                for ident in ('awwnb.1','awwnb.2'):w.fire(ident,'BLK',stale=True)
                self.assertEqual((30,19),(w.armies['BLK'],w.armies['AWW']))
                self.assertEqual((D(75),D(25)),(w.fuel['BLK'],w.fuel['AWW']))
                self.assertEqual(250,w.countries['AWW'].equipment['infantry_equipment_1'])

    def test_aww_expired_birth_window_cannot_replay_on_monthly_or_stale_callback(self):
        w=World();w.release_action('on_startup');w.armies['BLK']=40;w.fire('awwnb.1','BLK')
        w.countries['AWW'].flags.pop('ac_release_awaiting_legacy_army',None)
        w.release_action('on_monthly','AWW')
        self.assertFalse(w.fire('awwnb.2','BLK'));w.fire('awwnb.2','BLK',stale=True)
        self.assertEqual(10,w.armies['AWW'])

    def test_annex_before_aww_callback_closes_old_window_on_rerelease(self):
        w=World();w.release_action('on_startup');w.armies['BLK']=40;w.fire('awwnb.1','BLK')
        w.release_action('on_annex','BLK','AWW')
        w.states[272].owner=w.states[272].controller='BLK'
        w.states[272].owner=w.states[272].controller='AWW';w.release_action('on_release_as_free','AWW','BLK')
        self.assertFalse(w.fire('awwnb.2','BLK'));w.fire('awwnb.2','BLK',stale=True)
        self.assertEqual(10,w.armies['AWW']);self.assertEqual(30,w.armies['BLK'])

    def test_four_dormant_core_release_hooks_do_not_spawn_a_country_or_army(self):
        intake=json.loads((ROOT/'tools/release_foundations/intake.json').read_text())
        for tag in ('REL','SER','SHI','TER'):
            for action in ('on_release_as_free','on_release_as_puppet'):
                with self.subTest(tag=tag,action=action):
                    w=World();w.release_action('on_startup')
                    self.assertFalse(any(s.owner==tag for s in w.states.values()))
                    case=next(c for c in intake['countries'][tag]['known_cases'] if c['id']=='generic_core_release')
                    for ident in case['states']:w.states[ident].owner=w.states[ident].controller=tag
                    w.release_action(action,tag,'ERU')
                    self.assertEqual(case['capital_state'],w.capitals[tag]);self.assertEqual(0,w.armies[tag])
                    self.assertIn('ac_release_administration_registered',w.countries[tag].flags)
                    before=copy.deepcopy(w.countries[tag].equipment)
                    w.release_action(action,tag,'ERU');w.release_action('on_monthly',tag)
                    self.assertEqual(before,w.countries[tag].equipment)

    def test_foreign_clone_placeholder_and_occupied_country_do_not_register(self):
        for tag in ('REC','TER'):
            w=World();w.release_action('on_startup');state=316 if tag=='REC' else 209
            w.states[state].owner=tag;w.states[state].controller='BLK';w.countries[tag].capitulated=True
            w.release_action('on_release_as_free',tag,'BLK')
            self.assertNotIn('ac_release_administration_registered',w.countries[tag].flags)
        w=World();w.release_action('on_startup');w.states[171].owner=w.states[171].controller='REC'
        w.release_action('on_release_as_free','REC','BLK')
        self.assertNotIn('ac_release_administration_registered',w.countries['REC'].flags)
        w.states[316].owner=w.states[316].controller='REC';w.countries['REC'].original_tag='BLK'
        w.release_action('on_release_as_free','REC','BLK')
        self.assertNotIn('ac_release_administration_registered',w.countries['REC'].flags)

    def test_first_init_adopts_existing_countries_without_forces_or_stock_changes(self):
        w=World(new=False);w.states[316].owner=w.states[316].controller='REC';w.armies['REC']=7;w.countries['REC'].equipment={'infantry_equipment_1':123}
        c=w.countries['REC'];c.variables.update(ac_econ_treasury=D(17),ac_econ_debt=D(5));before=copy.deepcopy((w.armies,c.equipment))
        w.release_action('on_startup')
        self.assertIn('ac_release_REC_adopted',w.globals)
        self.assertEqual(316,w.capitals['REC'])
        self.assertEqual(before,(w.armies,c.equipment))
        self.assertEqual((D(17),D(5)),(c.variables['ac_econ_treasury'],c.variables['ac_econ_debt']))
        self.assertFalse(w.fire('recta.1','GEB'))
        w.fire('recta.1','GEB',stale=True)
        self.assertEqual(before,(w.armies,c.equipment))

    def test_recta_birth_keeps_ten_formations_and_current_shared_once_receipt(self):
        w=World();w.release_action('on_startup');w.research['GEB']={'infantry_weapons','basic_train'}
        self.assertTrue(w.fire('recta.1','GEB'))
        self.assertEqual(10,w.armies['REC']);self.assertEqual(345,w.capitals['REC'])
        self.assertIn('infantry_weapons',w.research['REC'])
        w.fire('recta.1','GEB',stale=True)
        self.assertEqual(10,w.armies['REC'])

    def test_treaty_recta_uses_owned_316_and_does_not_replay_birth(self):
        w=World();w.release_action('on_startup')
        for ident in (293,316):w.states[ident].owner=w.states[ident].controller='REC'
        # This calls the country owner from the actual foreign event scope.
        w.execute(parse('REC = { ac_release_observe_country = yes }'),w.countries['BLK'])
        self.assertEqual(316,w.capitals['REC']);self.assertEqual(0,w.armies['REC'])
        self.assertIn('ac_release_administration_registered',w.countries['REC'].flags)
        w.fire('recta.1','GEB',stale=True)
        self.assertEqual(0,w.armies['REC']);self.assertNotEqual('REC',w.states[345].owner)

    def test_south_belka_group_transfers_once_across_different_stale_events(self):
        w=World();w.release_action('on_startup');w.armies['BLK']=40;w.countries['BLK'].equipment={'infantry_equipment_1':1000};w.fuel['BLK']=D(100)
        self.assertTrue(w.fire('south_belka.2','BLK'))
        self.assertEqual((30,10),(w.armies['BLK'],w.armies['SBK']))
        self.assertEqual((750,250),(w.countries['BLK'].equipment['infantry_equipment_1'],w.countries['SBK'].equipment['infantry_equipment_1']))
        for ident in ('south_belka.3','south_belka.4','south_belka.2'):w.fire(ident,'BLK',stale=True)
        self.assertEqual((30,10),(w.armies['BLK'],w.armies['SBK']))
        self.assertEqual((D(75),D(25)),(w.fuel['BLK'],w.fuel['SBK']))

    def test_south_treaty_uses_owned_590_and_never_claims_foreign_capital(self):
        w=World();w.release_action('on_startup')
        for ident in (228,584,590,270,331):w.states[ident].owner=w.states[ident].controller='SBK'
        w.execute(parse('SBK = { ac_release_observe_country = yes }'),w.countries['BLK'])
        self.assertEqual(590,w.capitals['SBK']);self.assertNotEqual('SBK',w.states[302].owner)
        w.armies['BLK']=40;w.fire('south_belka.4','BLK',stale=True)
        self.assertEqual((40,0),(w.armies['BLK'],w.armies['SBK']))


if __name__=='__main__':unittest.main(verbosity=2)
