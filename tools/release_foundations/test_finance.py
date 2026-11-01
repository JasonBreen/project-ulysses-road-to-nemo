"""Execute the real P1 account owner on legitimate-release/adoption boundaries.

No financial substitute or private-stock writer is supplied by this adapter.
Decimal interpretation is source coverage, not native numeric/save acceptance.
"""
import copy
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/economy_v2'))
from harness import World
from build import RELEASE_HISTORY_TAGS
sys.path.insert(0,str(ROOT/'tools'))
from economy_script import Harness as LegacyWorld,Country as LegacyCountry

STATES=dict(AWW=272,REC=316,REL=173,SBK=302,SER=581,SHI=426,TER=209)
STOCKS=('ac_macro_cash','ac_macro_debt','ac_macro_arrears','ac_macro_commitments_annual','ac_macro_replacement_escrow','ac_macro_settlements')


def assign(world,tag):
    state=world.states[STATES[tag]];before=(state.owner,state.controller)
    state.owner=state.controller=tag
    return state,before


class ReleaseFinance(unittest.TestCase):
    def test_same_day_releases_do_not_seed_cash_debt_or_state_output_twice(self):
        self.assertEqual(set(STATES),set(RELEASE_HISTORY_TAGS))
        for tag in RELEASE_HISTORY_TAGS:
            w=World();w.action('on_startup');c=w.countries[tag]
            state,_=assign(w,tag);before=copy.deepcopy(state.variables)
            w.run('ac_econ_initialize',tag)
            self.assertTrue(w.trigger([['ac_macro_ready','=','yes']],c),tag)
            self.assertEqual(D(0),c.variables['ac_macro_cash'],tag)
            self.assertEqual(D(0),c.variables['ac_macro_debt'],tag)
            self.assertEqual(before,state.variables,tag)
            self.assertGreater(c.variables['ac_macro_real_gdp'],0,tag)

    def test_already_existing_accounts_and_repeat_initialization_preserve_stocks(self):
        w=World();w.action('on_startup');assign(w,'REC');w.run('ac_econ_initialize','REC');c=w.countries['REC']
        for name,value in zip(STOCKS,('7.5','3.25','.125','.08','.005','12')):c.variables[name]=D(value)
        before={name:c.variables[name] for name in STOCKS}
        for _ in range(4):w.run('ac_econ_adopt_release_account','REC');w.run('ac_macro_initialize','REC')
        self.assertEqual(before,{name:c.variables[name] for name in STOCKS})

    def test_secession_moves_realized_output_once_without_transferring_public_financial_stocks(self):
        w=World();w.action('on_startup');state=w.states[316];old=w.countries[state.owner]
        old_gdp=old.variables['ac_macro_real_gdp'];old_stocks={name:old.variables.get(name,D(0)) for name in STOCKS}
        state.owner=state.controller='REC';w.run('ac_econ_adopt_release_account','REC');w.run('ac_macro_quote',old.tag)
        new=w.countries['REC']
        self.assertEqual(old_gdp,old.variables['ac_macro_real_gdp']+new.variables['ac_macro_real_gdp'])
        self.assertEqual(old_stocks,{name:old.variables.get(name,D(0)) for name in STOCKS})
        self.assertEqual((D(0),D(0)),(new.variables['ac_macro_cash'],new.variables['ac_macro_debt']))

    def test_annex_then_rerelease_keeps_account_obligations_and_never_reseeds(self):
        w=World();w.action('on_startup');state,former=assign(w,'SBK');w.run('ac_econ_initialize','SBK');c=w.countries['SBK']
        c.variables.update(ac_macro_cash=D('1.75'),ac_macro_debt=D('2.5'),ac_macro_arrears=D('.25'),ac_macro_commitments_annual=D('.125'))
        before={name:c.variables.get(name,D(0)) for name in STOCKS}
        state.owner,state.controller=former;w.run('ac_econ_initialize','SBK')
        state.owner=state.controller='SBK';w.run('ac_econ_initialize','SBK')
        self.assertEqual(before,{name:c.variables.get(name,D(0)) for name in STOCKS})

    def test_matching_account_identity_can_reattach_without_losing_stocks_or_history(self):
        w=World();w.action('on_startup');assign(w,'REC');w.run('ac_econ_initialize','REC');c=w.countries['REC']
        c.variables.update(ac_macro_cash=D('3.125'),ac_macro_debt=D('9.75'),ac_macro_arrears=D('.1'),ac_macro_settlements=D(7))
        before={name:c.variables.get(name,D(0)) for name in STOCKS}
        del c.flags['ac_macro_initialized'];w.run('ac_econ_adopt_release_account','REC')
        self.assertTrue(w.trigger([['ac_macro_ready','=','yes']],c))
        self.assertEqual(before,{name:c.variables.get(name,D(0)) for name in STOCKS})

    def test_wrong_account_identity_is_locked_without_spending_or_erasing_copied_obligations(self):
        w=World();w.action('on_startup');assign(w,'AWW');c=w.countries['AWW'];donor=w.countries['BLK']
        c.variables=copy.deepcopy(donor.variables);c.flags=copy.deepcopy(donor.flags)
        before={name:c.variables.get(name,D(0)) for name in STOCKS}
        w.run('ac_econ_initialize','AWW');w.run('ac_econ_borrow','AWW');w.run('ac_econ_repay','AWW')
        self.assertFalse(w.trigger([['ac_macro_ready','=','yes']],c))
        self.assertIn('ac_release_financial_identity_review',c.flags)
        self.assertEqual(before,{name:c.variables.get(name,D(0)) for name in STOCKS})

    def test_identity_without_a_complete_supported_account_is_not_a_ready_account(self):
        w=World();w.action('on_startup');assign(w,'REC');c=w.countries['REC']
        c.variables.update(ac_macro_identity=D(c.identity),ac_macro_debt=D('5.25'))
        w.run('ac_econ_adopt_release_account','REC')
        self.assertNotIn('ac_macro_initialized',c.flags)
        self.assertIn('ac_release_financial_identity_review',c.flags)
        self.assertEqual(D('5.25'),c.variables['ac_macro_debt'])
        self.assertNotIn('ac_macro_cash',c.variables)

    def test_missing_identity_and_unsupported_schema_never_erase_existing_obligations(self):
        for fields in [dict(ac_macro_cash=D('1.25'),ac_macro_debt=D(5)),dict(ac_macro_identity=D(45),ac_macro_schema=D(99),ac_macro_cash=D('1.25'),ac_macro_debt=D(5))]:
            w=World();w.action('on_startup');assign(w,'REC');c=w.countries['REC'];c.variables.update(fields);c.flags['ac_macro_initialized']=None;before=copy.deepcopy(c.variables)
            w.run('ac_econ_adopt_release_account','REC');self.assertEqual(before,c.variables)
            self.assertFalse(w.trigger([['ac_macro_ready','=','yes']],c));self.assertIn('ac_release_financial_identity_review',c.flags)

    def test_legacy_release_initialization_does_not_use_the_opening_treasury_seed(self):
        for tag in RELEASE_HISTORY_TAGS:
            w=World(mode='experimental');assign(w,tag);c=w.countries[tag]
            w.run('ac_econ_initialize',tag)
            self.assertIn('ac_econ_initialized',c.flags)
            self.assertEqual(D(0),c.variables.get('ac_econ_treasury',D(0)),tag)
            self.assertEqual(D(0),c.variables.get('ac_econ_debt',D(0)),tag)
            c.variables.update(ac_econ_treasury=D('18.75'),ac_econ_debt=D('7.5'),ac_econ_arrears=D('.5'))
            del c.flags['ac_econ_initialized'];w.run('ac_econ_adopt_release_account',tag)
            self.assertEqual((D('18.75'),D('7.5'),D('.5')),
                tuple(c.variables[key] for key in ('ac_econ_treasury','ac_econ_debt','ac_econ_arrears')))

    def test_ordinary_country_legacy_and_full_opening_contracts_remain_unchanged(self):
        w=World(mode='experimental');w.run('ac_econ_initialize','BLK');c=w.countries['BLK']
        self.assertEqual(c.variables['ac_econ_capacity']*2,c.variables['ac_econ_treasury'])
        w=World();w.action('on_startup');c=w.countries['BLK']
        self.assertEqual(c.variables['ac_macro_nominal_gdp']*D('.02'),c.variables['ac_macro_cash'])
        self.assertEqual(c.variables['ac_macro_nominal_gdp']*c.variables['ac_macro_seed_debt_ratio'],c.variables['ac_macro_debt'])

    def test_legacy_interpreter_executes_real_classification_for_named_and_cloned_release_accounts(self):
        h=LegacyWorld()
        for tag,original in [('REC','REC'),('D01','REC'),('REC','BLK')]:
            country=LegacyCountry(factories=20,tag=tag,original_tag=original)
            h.action('on_startup',[country])
            self.assertIn('ac_econ_initialized',country.flags)
            self.assertEqual(D(0),country.value('ac_econ_treasury'))
        ordinary=LegacyCountry(factories=20,tag='BLK');h.action('on_startup',[ordinary])
        self.assertEqual(D(50),ordinary.value('ac_econ_treasury'))

    def test_disabled_mode_and_nonrelease_public_adoption_are_noops(self):
        for mode,tag in [('disabled','REC'),('full','BLK'),('experimental','BLK')]:
            w=World(mode=mode);c=w.countries[tag];before=copy.deepcopy((c.variables,c.flags))
            w.run('ac_econ_adopt_release_account',tag)
            self.assertEqual(before,(c.variables,c.flags))


if __name__=='__main__':unittest.main(verbosity=2)
