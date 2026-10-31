"""Actual-script macro accounting, policy, save and physical-production checks.

Offline coverage only. This is not Paradox parsing, fixed-point or native QA.
"""
import copy, hashlib, json, re, subprocess, sys, unittest
from datetime import date
from decimal import Decimal as D
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/economy_v2'))
from harness import World, Country, parse as actual_parse
from build import CATEGORIES, PRESETS, MARKER, build, history_marker
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get,walk


def worth(country):
    v=country.variables
    return v.get('ac_macro_cash',D(0))+v.get('ac_macro_replacement_escrow',D(0))-v.get('ac_macro_debt',D(0))-v.get('ac_macro_arrears',D(0))


class Macro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=World();cls.base.action('on_startup')

    def world(self,tag='SNS'):
        w=copy.deepcopy(self.base);return w,w.countries[tag]

    def close(self,a,b):self.assertLess(abs(a-b),D('1e-18'))

    def test_69_profiles_and_state_output_are_not_canon_claims(self):
        data=json.loads((ROOT/'tools/economy_v2/profiles.json').read_text())
        histories={p.name[:3] for p in (MOD/'history/countries').glob('*.txt')}
        self.assertEqual(69,len(histories));self.assertEqual(histories,{p['tag'] for p in data['profiles']})
        self.assertEqual(len(data['states']),len({s['id'] for s in data['states']}))
        for p in data['profiles']:self.assertIn('fictional',p['source_layer'])
        for tag,c in self.base.countries.items():
            owned=any(s.owner==tag for s in self.base.states.values())
            self.assertEqual(owned,'ac_macro_initialized' in c.flags,tag)
            if not owned:self.assertFalse(c.variables,tag)

    def test_refresh_startup_and_reload_never_reseed_cash_or_settle(self):
        w,c=self.world();before=copy.deepcopy(c.variables)
        for _ in range(4):w.run('ac_macro_initialize','SNS');w.run('ac_macro_quote','SNS')
        self.assertEqual(before,c.variables)
        w.month('SNS');snapshot=copy.deepcopy(w)
        w.action('on_startup');w.action('on_monthly',['SNS'])
        self.assertEqual(snapshot.countries['SNS'].variables,w.countries['SNS'].variables)
        self.assertEqual(1,c.variables['ac_macro_settlements'])

    def test_disabled_and_old_save_full_mode_have_no_fiscal_writes(self):
        public=('ac_macro_initialize','ac_macro_quote','ac_macro_settle_month','ac_macro_borrow','ac_macro_repay','ac_macro_try_spend','ac_macro_receive','ac_macro_change_commitment','ac_macro_apply_disruption','ac_macro_fund_replacements','ac_macro_cancel_replacements')
        for mode,new in [('disabled',True),('full',False)]:
            w=World(mode,new);before=copy.deepcopy(w.countries['SNS'])
            for name in public:w.run(name,'SNS',dict(ac_macro_transaction_amount=D('1'),ac_macro_commitment_delta=D('1'),ac_macro_disruption_delta=D('.5')))
            self.assertEqual(before,w.countries['SNS'])

    def test_monthly_owner_rejects_unauthorized_or_duplicate_calls(self):
        w,c=self.world();before=worth(c);w.today=date(1991,2,1).toordinal()
        w.run('ac_macro_settle_month','SNS');self.assertEqual(before,worth(c))
        w.action('on_monthly',['SNS']);settled=copy.deepcopy(c.variables)
        w.action('on_monthly',['SNS']);self.assertEqual(settled,c.variables)

    def test_release_first_calendar_settlement_is_independent_of_startup(self):
        for released_on in ((1991,2,28),(1991,3,1)):
            w,_=self.world();w.today=date(*released_on).toordinal()
            w.countries['NSO']=Country('NSO',901)
            state=next(s for s in w.states.values() if s.owner=='DEL')
            state.owner=state.controller='NSO'
            reloaded=copy.deepcopy(w);reloaded.action('on_startup')
            for candidate in (w,reloaded):candidate.month('NSO',1991,3)
            first=w.countries['NSO'];other=reloaded.countries['NSO']
            self.assertEqual(first.variables,other.variables)
            self.assertEqual(first.flags,other.flags)
            self.assertEqual(1,first.variables['ac_macro_settlements'])
            self.assertGreater(first.variables['ac_macro_last_bill'],0)
            before=copy.deepcopy(first);w.action('on_startup');w.action('on_monthly',['NSO'])
            self.assertEqual(before,w.countries['NSO'])
        # The original 1991 opening is quote/setup only, even if the engine
        # invokes a monthly callback on the bookmark date.
        opening,_=self.world();before=copy.deepcopy(opening.countries['SNS'])
        opening.action('on_monthly',['SNS'])
        self.assertEqual(before,opening.countries['SNS'])

    def test_cash_debt_arrears_accounting_conserves_monthly_financial_position(self):
        w,c=self.world();c.variables.update(ac_macro_cash=D('0'),ac_macro_debt=D('139'),ac_macro_commitments_annual=D('2000'))
        before=worth(c);w.month('SNS')
        self.close(worth(c)-before,c.variables['ac_macro_last_revenue']-c.variables['ac_macro_last_bill'])
        self.assertGreater(c.variables['ac_macro_arrears'],0);self.assertEqual(0,c.variables['ac_macro_cash'])
        self.assertGreaterEqual(c.variables['ac_macro_debt'],139)

    def test_partial_credit_never_forgives_debt_after_output_loss(self):
        w,c=self.world();c.variables.update(ac_macro_cash=D('0'),ac_macro_debt=D('139'),ac_macro_commitments_annual=D('2000'))
        w.month('SNS');debt=c.variables['ac_macro_debt']
        w.run('ac_macro_apply_disruption','SNS',dict(ac_macro_disruption_delta=D('.75')))
        self.assertEqual(debt,c.variables['ac_macro_debt']);self.assertEqual(0,c.variables['ac_macro_credit_room'])
        w.run('ac_macro_borrow','SNS');self.assertEqual(debt,c.variables['ac_macro_debt'])

    def test_tax_lanes_categories_and_presets_are_independent_and_guarded(self):
        for lane in ('income','business','consumption'):
            w,c=self.world();other={k:v for k,v in c.variables.items() if k.endswith('_tax') and lane not in k}
            w.run('ac_macro_'+lane+'_tax_up','SNS');after=c.variables['ac_macro_'+lane+'_tax']
            w.run('ac_macro_'+lane+'_tax_up','SNS');self.assertEqual(after,c.variables['ac_macro_'+lane+'_tax'])
            self.assertEqual(other,{k:v for k,v in c.variables.items() if k in other})
        for category in CATEGORIES:
            w,c=self.world();w.run('ac_macro_'+category+'_up','SNS')
            self.assertEqual(2,c.variables['ac_macro_budget_'+category])
            self.assertEqual([D(1)]*4,[c.variables['ac_macro_budget_'+other] for other in CATEGORIES if other!=category])
        for preset,values in PRESETS.items():
            w,c=self.world();w.run('ac_macro_preset_'+preset,'SNS')
            self.assertEqual(tuple(map(D,values)),tuple(c.variables['ac_macro_budget_'+name] for name in CATEGORIES))

    def test_each_budget_category_has_a_delivered_tradeoff(self):
        low,lc=self.world();high,hc=self.world()
        lc.variables['ac_macro_budget_administration']=D(0);hc.variables['ac_macro_budget_administration']=D(2)
        low.run('ac_macro_quote','SNS');high.run('ac_macro_quote','SNS')
        self.assertGreater(hc.variables['ac_macro_revenue'],lc.variables['ac_macro_revenue'])
        for category,indicator in [('services','ac_macro_service_modifier'),('education','ac_macro_research_modifier'),('development','ac_macro_construction_modifier'),('defense','ac_macro_readiness')]:
            low,lc=self.world();high,hc=self.world();lc.variables['ac_macro_budget_'+category]=D(0);hc.variables['ac_macro_budget_'+category]=D(2)
            low.month('SNS');high.month('SNS');self.assertGreater(hc.variables[indicator],lc.variables[indicator],category)

    def test_inflation_does_not_mint_real_output_cash_or_equipment(self):
        w,c=self.world();real=c.variables['ac_macro_real_gdp'];cash=c.variables['ac_macro_cash'];state_values={s.ident:s.variables['ac_macro_real_output'] for s in w.states.values()}
        c.variables['ac_macro_price_index']=D(200);w.run('ac_macro_quote','SNS')
        self.assertEqual(real,c.variables['ac_macro_real_gdp']);self.assertEqual(real*2,c.variables['ac_macro_nominal_gdp'])
        self.assertEqual(cash,c.variables['ac_macro_cash']);self.assertFalse(c.equipment)
        self.assertEqual(state_values,{s.ident:s.variables['ac_macro_real_output'] for s in w.states.values()})

    def test_actual_capacity_changes_affect_growth_without_creating_factories(self):
        baseline,bc=self.world();expanded,ec=self.world()
        ec.observables['num_of_controlled_factories']=5
        baseline.month('SNS');expanded.month('SNS')
        self.close(ec.variables['ac_macro_growth']-bc.variables['ac_macro_growth'],D(1))
        self.assertEqual(5,ec.observables['num_of_controlled_factories'])
        expanded.month('SNS',1991,3)
        self.assertEqual(0,ec.variables['ac_macro_capacity_growth'])

    def test_occupation_transfers_output_once_without_transferring_financial_stocks(self):
        w,c=self.world();other=w.countries['DEL'];before_cash=(c.variables['ac_macro_cash'],other.variables['ac_macro_cash'])
        world_total=sum(country.variables.get('ac_macro_real_gdp',D(0)) for country in w.countries.values())
        state=next(s for s in w.states.values() if s.owner=='SNS');state.controller='DEL'
        w.run('ac_macro_quote','SNS');w.run('ac_macro_quote','DEL')
        self.close(world_total,sum(country.variables.get('ac_macro_real_gdp',D(0)) for country in w.countries.values()))
        self.assertEqual(before_cash,(c.variables['ac_macro_cash'],other.variables['ac_macro_cash']))
        self.assertLess(other.variables['ac_macro_tax_base'],other.variables['ac_macro_nominal_gdp'])

    def test_clone_identity_and_late_release_receive_no_historical_cash(self):
        w,c=self.world();clone=copy.deepcopy(c);clone.tag='D01';clone.identity=900;w.countries['D01']=clone
        clone.flags['ac_macro_crisis']=None
        state=next(s for s in w.states.values() if s.owner=='SNS');state.owner=state.controller='D01'
        w.today=date(1996,1,1).toordinal();w.run('ac_macro_initialize','D01')
        self.assertEqual(0,clone.variables['ac_macro_cash']);self.assertEqual(0,clone.variables['ac_macro_debt'])
        self.assertNotIn('ac_macro_history_eligible',clone.flags)
        self.assertNotIn('ac_macro_crisis',clone.flags)
        released=Country('NSO',901);w.countries['NSO']=released
        state=next(s for s in w.states.values() if s.owner=='DEL');output=state.variables['ac_macro_real_output'];state.owner=state.controller='NSO'
        w.run('ac_macro_initialize','NSO')
        self.assertEqual(0,released.variables['ac_macro_cash']);self.assertEqual(0,released.variables['ac_macro_debt'])
        self.assertEqual(output,state.variables['ac_macro_real_output'])

    def test_upkeep_observes_real_forces_and_war_costs_without_reserving_factories(self):
        w,c=self.world();before=copy.deepcopy(c.observables)
        c.observables.update(deployed_army_manpower_k=100,deployed_navy_manpower_k=10,deployed_airforce_manpower_k=20,num_deployed_planes=50,num_ships=10)
        w.run('ac_macro_quote','SNS');peace=c.variables['ac_macro_upkeep'];c.war=True;w.run('ac_macro_quote','SNS')
        self.close(c.variables['ac_macro_upkeep'],peace*D('1.5'));self.assertEqual(10,c.observables['num_ships']);self.assertFalse(c.equipment)

    def test_replacements_wait_for_actual_native_production_and_never_grant_twice(self):
        w,c=self.world();before=worth(c);w.run('ac_macro_fund_replacements','SNS');after=c.variables['ac_macro_cash']
        self.close(before,worth(c));w.run('ac_macro_fund_replacements','SNS');self.assertEqual(after,c.variables['ac_macro_cash'])
        w.month('SNS');self.assertEqual(D('.005'),c.variables['ac_macro_replacement_escrow'])
        c.observables['total_equipment_produced_infantry']=100;w.month('SNS',1991,3)
        self.assertEqual(0,c.variables['ac_macro_replacement_escrow']);self.assertFalse(c.equipment)
        equipment=copy.deepcopy(c.equipment);w.run('ac_macro_replacement_cycle','SNS');self.assertEqual(equipment,c.equipment)

    def test_cancel_refunds_escrow_once_and_commitments_add_remove_exactly(self):
        w,c=self.world();before=worth(c);w.run('ac_macro_fund_replacements','SNS');w.run('ac_macro_cancel_replacements','SNS')
        self.close(before,worth(c));cash=c.variables['ac_macro_cash'];w.run('ac_macro_cancel_replacements','SNS');self.assertEqual(cash,c.variables['ac_macro_cash'])
        base=c.variables['ac_macro_bill'];w.run('ac_macro_change_commitment','SNS',dict(ac_macro_commitment_delta=D('1.2')))
        self.close(c.variables['ac_macro_bill']-base,D('.1'))
        w.run('ac_macro_change_commitment','SNS',dict(ac_macro_commitment_delta=D('-1.2')));self.close(c.variables['ac_macro_bill'],base)

    def test_shared_programme_payment_and_policy_transactions_recheck_cash(self):
        w,c=self.world();before=c.variables['ac_macro_cash'];w.run('ac_econ_pay_programme','SNS')
        self.assertEqual(before-D('.002'),c.variables['ac_macro_cash'])
        self.assertIn('ac_macro_transaction_succeeded',c.flags)
        c.variables['ac_macro_cash']=D('.001');w.run('ac_econ_pay_programme','SNS')
        self.assertEqual(D('.001'),c.variables['ac_macro_cash']);self.assertNotIn('ac_macro_transaction_succeeded',c.flags)
        w.run('ac_macro_try_spend','SNS',dict(ac_macro_transaction_amount=D('-1')))
        self.assertEqual(D('.001'),c.variables['ac_macro_cash'])

    def test_spend_result_cannot_survive_disabled_or_landless_retry(self):
        for interruption in ('disabled','landless'):
            w,c=self.world();w.run('ac_macro_try_spend','SNS',dict(ac_macro_transaction_amount=D('.001')))
            self.assertIn('ac_macro_transaction_succeeded',c.flags);cash=c.variables['ac_macro_cash']
            if interruption=='disabled':w.mode='disabled'
            else:
                for state in w.states.values():
                    if state.owner=='SNS':state.owner=state.controller='DEL'
            w.run('ac_macro_try_spend','SNS',dict(ac_macro_transaction_amount=D('.001')))
            self.assertNotIn('ac_macro_transaction_succeeded',c.flags);self.assertEqual(cash,c.variables['ac_macro_cash'])

    def test_existing_experimental_contract_and_balances_are_not_converted(self):
        w=World('experimental',False);c=w.countries['SNS'];c.flags['ac_econ_initialized']=None
        c.variables.update(ac_econ_treasury=D(17),ac_econ_procurement_escrow=D(5),ac_econ_procurement_weeks=D(2))
        w.run('ac_econ_initialize','SNS');self.assertEqual(17,c.variables['ac_econ_treasury'])
        w.run('ac_econ_weekly_settlement','SNS');w.run('ac_econ_weekly_settlement','SNS')
        self.assertEqual(100,c.equipment['infantry_equipment_0'])
        w.run('ac_econ_cancel_procurement','SNS');self.assertEqual(100,c.equipment['infantry_equipment_0'])
        self.assertNotIn('ac_macro_initialized',c.flags)

    def test_warning_crisis_and_recovery_follow_funded_months(self):
        w,c=self.world();c.variables.update(ac_macro_cash=D(0),ac_macro_debt=D(140),ac_macro_commitments_annual=D(3000))
        for month in (2,3,4):w.month('SNS',1991,month)
        self.assertIn('ac_macro_warning',c.flags);self.assertIn('ac_macro_crisis',c.flags)
        c.variables['ac_macro_commitments_annual']=D(0)
        w.run('ac_macro_receive','SNS',dict(ac_macro_transaction_amount=D(10000)))
        for month in (5,6,7):w.month('SNS',1991,month)
        self.assertNotIn('ac_macro_crisis',c.flags);self.assertEqual(0,c.variables['ac_macro_arrears'])
        self.assertEqual(1,w.events.count(('SNS','ac_macro.2')))

    def test_long_run_all_country_budgets_and_ai_are_bounded(self):
        w=copy.deepcopy(self.base)
        for c in w.countries.values():c.ai=True
        for year in range(1991,2021):
            for month in range(1,13):
                if year==1991 and month==1:continue
                w.today=date(year,month,1).toordinal();w.action('on_monthly')
        for tag,c in w.countries.items():
            if 'ac_macro_initialized' not in c.flags:continue
            for variable in ('ac_macro_cash','ac_macro_debt','ac_macro_arrears','ac_macro_nominal_gdp'):
                self.assertGreaterEqual(c.variables[variable],0,(tag,variable));self.assertLess(c.variables[variable],D(1000000),(tag,variable))
            self.assertGreaterEqual(c.variables['ac_macro_readiness'],0);self.assertLessEqual(c.variables['ac_macro_readiness'],100)


class SourceAndUI(unittest.TestCase):
    def test_macro_pages_are_exclusive_and_inactive_controls_do_not_act(self):
        logic=get(get(actual_parse((MOD/'common/scripted_guis/ac_macro_economy.txt').read_text()),'scripted_gui'),'ac_macro_economy_screen')
        triggers={key:body for key,_,body in get(logic,'triggers')}
        manifest=json.loads((MOD/'gfx/interface/ac_macro/manifest.json').read_text())
        for ready in (False,True):
            w=copy.deepcopy(Macro.base) if ready else World('disabled')
            c=w.countries['SNS']
            for page in range(5):
                c.variables['ac_macro_ui_page']=D(page)
                for name,(*_,control_page) in manifest['positions'].items():
                    if control_page is not None:self.assertEqual(ready and page==control_page,w.trigger(triggers[name+'_visible'],c),(name,page,ready))
                for key,condition in triggers.items():
                    if key.endswith('_click_enabled') and key!='macro_close_click_enabled' and not ready:self.assertFalse(w.trigger(condition,c),key)
    def test_generated_outputs_and_composable_history_markers(self):
        subprocess.run([sys.executable,'-B',str(ROOT/'tools/economy_v2/build.py'),'--check'],check=True,capture_output=True)
        for path in (MOD/'history/countries').glob('*.txt'):
            text=path.read_text(encoding='utf-8-sig');self.assertEqual(1,text.count(MARKER));self.assertEqual(text,history_marker(text))
            if '# BEGIN EXPANSION START LEADER' in text:self.assertLess(text.index(MARKER),text.index('# BEGIN EXPANSION START LEADER'))

    def test_five_pages_direct_controls_keyboard_and_frame_art(self):
        gui=parse((MOD/'interface/ac_macro_economy.gui').read_text());window=next(n for _,n in walk(gui) if get(n,'name')=='"ac_macro_economy_screen"')
        self.assertFalse(any(k=='containerWindowType' for k,_,v in window))
        manifest=json.loads((MOD/'gfx/interface/ac_macro/manifest.json').read_text())
        for name,(x,y,width,height,page) in manifest['positions'].items():self.assertLessEqual(x+width,860,name);self.assertLessEqual(y+height,640,name)
        for row in manifest['assets']:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as im:self.assertEqual((row['width'],row['height']),im.size);self.assertEqual(0,im.width%row['frames'])
        self.assertIn('shortcut = "ESCAPE"',(MOD/'interface/ac_macro_economy.gui').read_text())
        logic=(MOD/'common/scripted_guis/ac_macro_economy.txt').read_text()
        for lane in ('income','business','consumption'):
            for direction in ('up','down'):self.assertIn('ac_macro_'+lane+'_tax_'+direction+' = yes',logic)
        for page in range(5):self.assertIn('ac_macro_ui_page = '+str(page),logic)

    def test_all_new_localization_and_public_symbols_resolve(self):
        raw=(MOD/'localisation/english/ac_macro_l_english.yml').read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        keys=set(re.findall(r'^\s+([A-Za-z0-9_.]+):\d*',raw.decode('utf-8-sig'),re.M))
        gui=(MOD/'interface/ac_macro_economy.gui').read_text()
        for key in re.findall(r'(?:text|buttonText)\s*=\s*"(AC_MACRO_\w+)"',gui):self.assertIn(key,keys)
        effects=(MOD/'common/scripted_effects/ac_macro_effects.txt').read_text()
        self.assertNotIn('add_offsite_building',effects);self.assertNotIn('add_equipment_to_stockpile',effects)
        self.assertNotIn('transfer_state',effects);self.assertNotIn('set_politics',effects)
        rules=(MOD/'common/game_rules/ac_economy_rules.txt').read_text();self.assertRegex(rules,r'default\s*=\s*\{\s*name\s*=\s*full')
        self.assertIn('name = experimental',rules);self.assertIn('name = disabled',rules)


if __name__=='__main__':unittest.main(verbosity=2)
