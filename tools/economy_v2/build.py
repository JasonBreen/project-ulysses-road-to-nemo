"""Original Ulysses macroeconomy authoring and deterministic packaging.

Country GDP, policy coefficients and prices are fictional gameplay calibration.
The legacy experimental economy remains a separate mode with unchanged stocks.
"""
from __future__ import annotations
import argparse, copy, hashlib, io, json, re, sys
from decimal import Decimal
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT/'tools/usea_expansion'))
from script import parse, render, get, setv, walk
import ledger, money, claims

MARKER = '# BEGIN ECONOMY V2 NEW CAMPAIGN\n# New histories only; old saves are never reseeded.\nset_country_flag = ac_macro_history_eligible\n# END ECONOMY V2 NEW CAMPAIGN\n'
CATEGORIES = ('administration', 'services', 'education', 'development', 'defense')
SHARES = dict(administration=.015, services=.05, education=.03, development=.02, defense=.03)
PRESETS = dict(balanced=(1,1,1,1,1), development=(1,1,2,2,0), relief=(1,2,1,1,0), mobilization=(1,0,0,1,2), stabilization=(1,0,0,0,0))
# These inherited histories own no country at the 1991 start. A later legitimate
# release receives the existing state's output, not a second opening balance.
RELEASE_HISTORY_TAGS = ('AWW','REC','REL','SBK','SER','SHI','TER')
RELEASE_ACCOUNT_REQUIRED = ('cash','debt','arrears','commitments_annual','replacement_escrow','replacement_target',
                            'revenue_carry_milli','bill_carry_milli','last_settlement','settlements',
                            'history_count','history_last_recorded')
LEGACY_FILES = ('common/scripted_effects/ac_economy_effects.txt',
                'common/scripted_effects/ac_economy_policy_effects.txt',
                'common/scripted_triggers/ac_economy_triggers.txt',
                'common/dynamic_modifiers/ac_economy_modifiers.txt')


def block(name, body):
    return name+' = {\n'+'\n'.join('\t'+line for line in body.splitlines())+'\n}\n'


def capture_inputs():
    legacy = {file:(MOD/file).read_text(encoding='utf-8-sig') for file in LEGACY_FILES}
    (HERE/'legacy_contract.json').write_text(json.dumps(dict(base='1f04456750b6e17a900cbfa407fddc3a4e96f3d5',
                         source_layer='existing MD-inspired economy, retained under its scoped CC-BY-SA notice', files=legacy), indent=2)+'\n')
    states = []
    for path in sorted((MOD/'history/states').glob('*.txt')):
        state = get(parse(path.read_text(encoding='utf-8-sig')), 'state', [])
        hist = get(state, 'history', [])
        owner = get(hist, 'owner', '').strip('"')
        if not owner: continue
        buildings = get(hist, 'buildings', [])
        states.append(dict(id=int(get(state,'id')), owner=owner, population=int(get(state,'manpower','0')),
                           civilians=int(get(buildings,'industrial_complex','0')),
                           military=int(get(buildings,'arms_factory','0'))))
    overrides = dict(OSE=20000,YUK=17000,BLK=4200,ERU=3000,FCU=6500,NPT=180,REC=120,
                     EMM=1100,EVA=650,SNS=140,AMB=90,UGE=130,DEL=110)
    profiles = []
    for path in sorted((MOD/'history/countries').glob('*.txt')):
        tag = path.name[:3]; owned = [s for s in states if s['owner']==tag]
        population = sum(s['population'] for s in owned)
        gdp = overrides.get(tag, round(max(.1,population/1_000_000*20+sum(s['civilians']*12+s['military']*8 for s in owned)),3))
        profiles.append(dict(tag=tag, history=path.relative_to(MOD).as_posix(), gdp_billion=gdp,
                             debt_ratio=.30, collection=.85, growth=3.0, inflation=2.0,
                             source_layer='user-approved fictional gameplay calibration; not canon national accounts',
                             calibration='explicit major/actor profile' if tag in overrides else 'inherited population and industry proxy'))
    source = dict(schema=2, units='billions of abstract fiscal units, constant-1991 real output; no canon currency or GDP claim',
                  profiles=profiles, states=states)
    (HERE/'profiles.json').write_text(json.dumps(source, indent=2)+'\n')


def legacy_and_adapters():
    source = json.loads((HERE/'legacy_contract.json').read_text())['files']
    effects = {key for file,text in source.items() if '/scripted_effects/' in file for key,_,_ in parse(text)}
    triggers = {key for file,text in source.items() if '/scripted_triggers/' in file for key,_,_ in parse(text)}
    renamed = {name:name.replace('ac_econ_', 'ac_econ_legacy_',1) for name in effects|triggers}
    pattern = re.compile(r'\b('+'|'.join(sorted(renamed,key=len,reverse=True))+r')\b')
    out = {file:pattern.sub(lambda m:renamed[m[0]],text) for file,text in source.items()}
    dispatch = dict(ac_econ_initialize='ac_macro_initialize', ac_econ_refresh_budget='ac_macro_quote',
                    ac_econ_borrow='ac_macro_borrow',ac_econ_repay='ac_macro_repay',
                    ac_econ_order_infantry='ac_macro_fund_replacements',ac_econ_cancel_procurement='ac_macro_cancel_replacements',
                    ac_econ_set_low_tax='ac_macro_tax_low',ac_econ_set_standard_tax='ac_macro_tax_standard',
                    ac_econ_set_high_tax='ac_macro_tax_high',ac_econ_set_basic_services='ac_macro_preset_balanced',
                    ac_econ_set_reconstruction='ac_macro_preset_relief')
    wrappers = '# Stable public API; full-mode calls dispatch to the monthly owner.\n'
    for name in sorted(effects):
        target = dispatch.get(name)
        if name == 'ac_econ_initialize':
            wrappers += block(name,block('if','limit = { ac_econ_release_history = yes }\nac_econ_adopt_release_account = yes')+
                              block('else_if','limit = { ac_macro_mode = yes }\nac_macro_initialize = yes')+
                              block('else',renamed[name]+' = yes'))
        elif target:
            wrappers += block(name, block('if','limit = { ac_macro_mode = yes }\n'+target+' = yes')+
                              block('else',renamed[name]+' = yes'))
        else:
            wrappers += block(name,block('if','limit = { ac_macro_mode = no }\n'+renamed[name]+' = yes'))
    wrappers += block('ac_econ_adopt_release_account',block('if','limit = { ac_econ_release_history = yes }\n'+
        block('if','limit = { ac_macro_mode = yes }\nac_macro_initialize = yes')+
        block('else_if','limit = { ac_econ_legacy_enabled = yes }\n'+
            block('if','limit = { NOT = { has_country_flag = ac_econ_initialized } }\nset_country_flag = ac_econ_initialized\n'+
                block('if','limit = { NOT = { has_variable = ac_econ_tax_level } }\nset_variable = { ac_econ_tax_level = 1 }')+
                block('if','limit = { NOT = { has_variable = ac_econ_civilian_level } }\nset_variable = { ac_econ_civilian_level = 0 }'))+
            'ac_econ_legacy_refresh_budget = yes')))
    wrappers += block('ac_econ_pay_programme',block('if','limit = { ac_macro_ready = yes }\nset_temp_variable = { ac_macro_transaction_amount = 0.002 }\nac_macro_try_spend = yes')+
                      block('else_if','limit = { ac_econ_legacy_ready = yes check_variable = { ac_econ_arrears = 0 } check_variable = { ac_econ_treasury >= 2 } }\nsubtract_from_variable = { ac_econ_treasury = 2 }'))
    out['common/scripted_effects/ac_economy_compat.txt'] = wrappers
    mapping = dict(ac_econ_enabled='ac_macro_mode',ac_econ_ready='ac_macro_ready',ac_econ_can_borrow='ac_macro_can_borrow',
                   ac_econ_can_repay='ac_macro_can_repay',ac_econ_can_produce='ac_macro_can_produce',ac_econ_can_order='ac_macro_can_fund_replacements')
    out['common/scripted_triggers/ac_economy_compat.txt'] = '\n'.join(block(name,'OR = { '+renamed[name]+' = yes '+mapping[name]+' = yes }') for name in sorted(triggers))
    out['common/scripted_triggers/ac_economy_compat.txt'] += block('ac_econ_can_pay_programme',
             'OR = { AND = { ac_macro_ready = yes check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_cash >= 0.002 } } AND = { ac_econ_legacy_ready = yes check_variable = { ac_econ_arrears = 0 } check_variable = { ac_econ_treasury >= 2 } } }')
    out['common/scripted_triggers/ac_economy_compat.txt'] += block('ac_econ_release_history',
        block('OR','\n'.join('tag = '+tag+'\noriginal_tag = '+tag for tag in RELEASE_HISTORY_TAGS)))
    # Public release-development transaction: the caller never writes money.
    #20FU and0.02b are separate calibrated prices, not a currency conversion.
    wrappers += block('ac_econ_try_fund_release_project',
        'clr_country_flag = ac_econ_release_project_funded\n'+block('if','limit = { ac_econ_release_history = yes }\n'+
            block('if','limit = { ac_macro_ready = yes }\nset_temp_variable = { ac_macro_transaction_amount = 0.02 }\nac_macro_try_spend = yes\n'+
                block('if','limit = { has_country_flag = ac_macro_transaction_succeeded }\nset_country_flag = ac_econ_release_project_funded'))+
            block('else_if','limit = { ac_econ_legacy_ready = yes check_variable = { ac_econ_arrears = 0 } check_variable = { ac_econ_treasury >= 20 } }\nsubtract_from_variable = { ac_econ_treasury = 20 }\nset_country_flag = ac_econ_release_project_funded')+
            block('else_if','limit = { ac_econ_enabled = no }\nset_country_flag = ac_econ_release_project_funded')))
    out['common/scripted_effects/ac_economy_compat.txt'] = wrappers
    out['common/scripted_triggers/ac_economy_compat.txt'] += block('ac_econ_can_fund_release_project',
        'ac_econ_release_history = yes\nOR = { ac_econ_enabled = no AND = { ac_macro_ready = yes check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_cash >= 0.02 } } AND = { ac_econ_legacy_ready = yes check_variable = { ac_econ_arrears = 0 } check_variable = { ac_econ_treasury >= 20 } } }')
    return out


def release_account_presence(effects):
    """Every persisted fresh-account field is evidence; UI selection is not.

    Read the actual initializer, including expanded ledger/money fields. Adding
    a future account receipt cannot silently reopen destructive fresh admission.
    No historical intake/capture is repinned by this generated inventory.
    """
    initialization=get(get(parse(effects),'ac_macro_initialize'),'else_if')
    variables={name for kind,body in walk(initialization) if kind=='set_variable' for name,_,_ in body if name.startswith('ac_macro_')}
    variables.discard('ac_macro_ui_page')
    flags=set(re.findall(r'\b(?:set|clr)_country_flag\s*=\s*(ac_macro_\w+)',render(initialization)))
    flags.discard('ac_macro_history_eligible')
    flags.add('ac_release_financial_identity_review')
    return sorted(variables),sorted(flags)


def macro_triggers(effects=None):
    variables,flags=release_account_presence(effects or economic_effects())
    presence=block('ac_macro_release_account_present',block('OR',
        '\n'.join('has_variable = '+name for name in variables)+'\n'+
        '\n'.join('has_country_flag = '+name for name in flags)))
    complete=block('ac_macro_release_account_complete','''has_variable = ac_macro_identity
check_variable = { var = ac_macro_identity value = THIS.id compare = equals }
check_variable = { ac_macro_schema = 2 }
'''+ '\n'.join('has_variable = ac_macro_'+field for field in RELEASE_ACCOUNT_REQUIRED))
    return presence+complete+'''# Full mode is default for new histories. Saved legacy rule values remain valid.
ac_macro_mode = { has_game_rule = { rule = ac_economy option = full } }
ac_macro_ready = { ac_macro_mode = yes has_country_flag = ac_macro_initialized check_variable = { var = ac_macro_identity value = THIS.id compare = equals } any_owned_state = { always = yes } OR = { ac_econ_release_history = no AND = { ac_macro_release_account_complete = yes NOT = { has_country_flag = ac_release_financial_identity_review } } } }
ac_macro_can_borrow = { ac_macro_ready = yes check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_credit_room >= ac_macro_loan_size } }
ac_macro_can_repay = { ac_macro_ready = yes check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_cash > 0 } check_variable = { ac_macro_debt > 0 } }
ac_macro_can_produce = { ac_macro_ready = yes has_capitulated = no num_of_military_factories > 0 }
ac_macro_can_fund_replacements = { ac_macro_can_produce = yes has_tech = infantry_weapons check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_replacement_escrow = 0 } check_variable = { ac_macro_cash >= 0.005 } }
ac_macro_can_change_policy = { ac_macro_ready = yes NOT = { has_country_flag = ac_macro_policy_cooldown } }
'''


def profile_effects(data):
    profile_code = ''; state_code = ''
    for row in data['profiles']:
        profile_code += block('if', 'limit = { original_tag = '+row['tag']+' }\n'+
            '\n'.join('set_variable = { ac_macro_'+key+' = '+str(row[value])+' }' for key,value in
            [('seed_gdp','gdp_billion'),('seed_debt_ratio','debt_ratio'),('collection','collection'),('base_growth','growth'),('inflation','inflation')]))
        owned = [s for s in data['states'] if s['owner']==row['tag']]
        weights = {s['id']:max(1,s['population'])+2_000_000*(s['civilians']+s['military']) for s in owned}
        total = sum(weights.values()) or 1
        for state in owned:
            amount = Decimal(str(row['gdp_billion']))*Decimal(weights[state['id']])/Decimal(total)
            state_code += block(str(state['id']),block('if','limit = { NOT = { has_variable = ac_macro_real_output } }\nset_variable = { ac_macro_real_output = '+format(amount.quantize(Decimal('.000001')),'f')+' }\nset_variable = { ac_macro_disruption = 0 }'))
    return block('ac_macro_profile',profile_code)+block('ac_macro_seed_states',state_code)


def economic_effects():
    e = {}
    def effect(name, body):e[name]=block(name,body)
    def guard(body):return block('if','limit = { ac_macro_ready = yes }\n'+body)
    init = '''limit = { ac_macro_mode = yes any_owned_state = { always = yes } NOT = { ac_macro_ready = yes } OR = { AND = { has_country_flag = ac_macro_history_eligible date < 1991.1.2 } has_global_flag = ac_macro_world_started } }
if = { limit = { has_variable = ac_macro_identity NOT = { check_variable = { var = ac_macro_identity value = THIS.id compare = equals } } }
 clr_country_flag = ac_macro_history_eligible
 clr_country_flag = ac_macro_warning
 clr_country_flag = ac_macro_crisis
 clr_country_flag = ac_macro_transaction_succeeded
 clr_country_flag = ac_macro_policy_cooldown
 clr_country_flag = ac_macro_monthly_authorized
}
set_country_flag = ac_macro_initialized
clr_country_flag = ac_macro_ledger_authorized
set_variable = { ac_macro_schema = 2 }
set_variable = { ac_macro_identity = THIS.id }
set_variable = { ac_macro_ui_page = 0 }
set_variable = { ac_macro_price_index = 100 }
set_variable = { ac_macro_income_tax = 0.20 }
set_variable = { ac_macro_business_tax = 0.20 }
set_variable = { ac_macro_consumption_tax = 0.05 }
set_variable = { ac_macro_base_growth = 3 }
set_variable = { ac_macro_inflation = 2 }
set_variable = { ac_macro_collection = 0.85 }
set_variable = { ac_macro_policy_rate = 4 }
set_variable = { ac_macro_readiness = 70 }
set_variable = { ac_macro_funding = 1 }
set_variable = { ac_macro_growth = 3 }
set_variable = { ac_macro_growth_lag = 0 }
set_variable = { ac_macro_cash = 0 }
set_variable = { ac_macro_debt = 0 }
set_variable = { ac_macro_arrears = 0 }
set_variable = { ac_macro_commitments_annual = 0 }
set_variable = { ac_macro_replacement_escrow = 0 }
set_variable = { ac_macro_replacement_target = 0 }
set_variable = { ac_macro_settlements = 0 }
set_variable = { ac_macro_last_revenue = 0 }
set_variable = { ac_macro_last_bill = 0 }
set_variable = { ac_macro_last_paid = 0 }
set_variable = { ac_macro_last_borrowed = 0 }
set_variable = { ac_macro_last_arrears_added = 0 }
set_variable = { ac_macro_last_arrears_paid = 0 }
set_variable = { ac_macro_stress_months = 0 }
set_variable = { ac_macro_warning_months = 0 }
set_variable = { ac_macro_warning_months_left = 0 }
set_variable = { ac_macro_recovery_months = 0 }
set_variable = { ac_macro_readiness_modifier = -0.03 }
set_variable = { ac_macro_service_modifier = 0 }
set_variable = { ac_macro_research_modifier = 0 }
set_variable = { ac_macro_construction_modifier = 0 }
# No settlement has occurred. Startup/reload timing must not skip the first
# scheduled accounting boundary for a released country or a new identity.
set_variable = { ac_macro_last_settlement = 0 }
set_variable = { ac_macro_last_factories = num_of_controlled_factories }
'''
    init += ledger.initialize() + money.initialize()
    init += '\n'.join('set_variable = { ac_macro_budget_'+c+' = 1 }' for c in CATEGORIES)+'\n'
    init += '''ac_macro_profile = yes
if = { limit = { has_country_flag = ac_macro_history_eligible date < 1991.1.2 ac_econ_release_history = no }
 ac_macro_seed_states = yes
 set_global_flag = ac_macro_world_started
 ac_macro_quote = yes
 set_variable = { ac_macro_cash = ac_macro_nominal_gdp }
 multiply_variable = { ac_macro_cash = 0.02 }
 set_variable = { ac_macro_debt = ac_macro_nominal_gdp }
 multiply_variable = { ac_macro_debt = ac_macro_seed_debt_ratio }
}
ac_macro_quote = yes
'''
    # A surviving released-country account may lose only its initialization flag
    # during an adoption/migration. Reattach its matching identity without
    # resetting cash, debt, contracts, carry or settled history. A mismatched
    # identity is locked for review instead of spending copied stocks or wiping
    # an archived obligation. Ordinary-country initialization stays unchanged.
    release_adoption='''limit = { ac_macro_mode = yes ac_econ_release_history = yes any_owned_state = { always = yes } ac_macro_release_account_present = yes NOT = { ac_macro_ready = yes } }
if = { limit = { ac_macro_release_account_complete = yes }
 set_country_flag = ac_macro_initialized
 clr_country_flag = ac_release_financial_identity_review
 ac_macro_quote = yes
}
else = { set_country_flag = ac_release_financial_identity_review }
'''
    effect('ac_macro_initialize',block('if',release_adoption)+block('else_if',init))
    quote = '''set_variable = { ac_macro_real_gdp = 0 }
set_variable = { ac_macro_potential_gdp = 0 }
set_variable = { ac_macro_tax_base = 0 }
set_variable = { ac_macro_civilian_factories = num_of_civilian_factories }
set_variable = { ac_macro_factory_capacity = num_of_controlled_factories }
set_variable = { ac_macro_military_factories = num_of_military_factories }
set_variable = { ac_macro_dockyards = num_of_naval_factories }
set_variable = { ac_macro_army_k = deployed_army_manpower_k }
set_variable = { ac_macro_navy_k = deployed_navy_manpower_k }
set_variable = { ac_macro_air_k = deployed_airforce_manpower_k }
set_variable = { ac_macro_planes = num_deployed_planes }
set_variable = { ac_macro_ships = num_ships }
set_variable = { ac_macro_infantry_produced = total_equipment_produced_infantry }
every_controlled_state = {
 if = { limit = { has_variable = ac_macro_real_output }
  add_to_variable = { PREV.ac_macro_potential_gdp = ac_macro_real_output }
  set_temp_variable = { ac_macro_state_output = ac_macro_real_output }
  set_temp_variable = { ac_macro_state_factor = 1 }
  subtract_from_temp_variable = { ac_macro_state_factor = ac_macro_disruption }
  multiply_temp_variable = { ac_macro_state_output = ac_macro_state_factor }
  add_to_variable = { PREV.ac_macro_real_gdp = ac_macro_state_output }
  if = { limit = { NOT = { is_owned_by = PREV } } multiply_temp_variable = { ac_macro_state_output = 0.35 } }
  add_to_variable = { PREV.ac_macro_tax_base = ac_macro_state_output }
 }
}
set_variable = { ac_macro_nominal_gdp = ac_macro_real_gdp }
set_temp_variable = { ac_macro_price_multiplier = ac_macro_price_index }
divide_temp_variable = { ac_macro_price_multiplier = 100 }
multiply_variable = { ac_macro_nominal_gdp = ac_macro_price_multiplier }
multiply_variable = { ac_macro_tax_base = ac_macro_price_multiplier }
set_variable = { ac_macro_output_gap = 0 }
if = { limit = { check_variable = { ac_macro_potential_gdp > 0 } }
 set_variable = { ac_macro_output_gap = ac_macro_real_gdp }
 divide_variable = { ac_macro_output_gap = ac_macro_potential_gdp }
 multiply_variable = { ac_macro_output_gap = -1 }
 add_to_variable = { ac_macro_output_gap = 1 }
}
set_variable = { ac_macro_effective_collection = ac_macro_budget_administration }
multiply_variable = { ac_macro_effective_collection = 0.1 }
add_to_variable = { ac_macro_effective_collection = 0.9 }
multiply_variable = { ac_macro_effective_collection = ac_macro_collection }
multiply_variable = { ac_macro_effective_collection = ac_macro_funding }
clamp_variable = { var = ac_macro_effective_collection min = 0.1 max = 0.98 }
'''
    quote += money.quote(SHARES)
    quote += '''set_variable = { ac_macro_credit_limit = ac_macro_nominal_gdp }
set_variable = { ac_macro_credit_room = ac_macro_credit_limit }
subtract_from_variable = { ac_macro_credit_room = ac_macro_debt }
clamp_variable = { var = ac_macro_credit_room min = 0 }
set_variable = { ac_macro_loan_size = ac_macro_nominal_gdp }
multiply_variable = { ac_macro_loan_size = 0.005 }
clamp_variable = { var = ac_macro_loan_size min = 0.001 }
set_variable = { ac_macro_defense_funding = 1 }
if = { limit = { check_variable = { ac_macro_upkeep_milli > 0 } }
 set_variable = { ac_macro_defense_funding = ac_macro_spending_defense_milli }
 divide_variable = { ac_macro_defense_funding = ac_macro_upkeep_milli }
 clamp_variable = { var = ac_macro_defense_funding min = 0 max = 1 }
}
multiply_variable = { ac_macro_defense_funding = ac_macro_funding }
# Compatibility quote aliases are display-only in full mode, never write owners.
set_variable = { ac_econ_treasury = ac_macro_cash }
set_variable = { ac_econ_debt = ac_macro_debt }
set_variable = { ac_econ_arrears = ac_macro_arrears }
set_variable = { ac_econ_revenue = ac_macro_revenue }
set_variable = { ac_econ_spending = ac_macro_operating }
set_variable = { ac_econ_balance = ac_macro_balance }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = ac_macro_economy_modifier } } } add_dynamic_modifier = { modifier = ac_macro_economy_modifier } }
'''
    effect('ac_macro_quote',guard(quote))
    settle = '''limit = { ac_macro_ready = yes date > 1991.1.31 has_country_flag = ac_macro_monthly_authorized check_variable = { ac_macro_last_settlement < date } }
clr_country_flag = ac_macro_monthly_authorized
set_variable = { ac_macro_last_settlement = date }
ac_macro_quote = yes
''' + money.settle() + '''set_variable = { ac_macro_last_borrowed = 0 }
set_variable = { ac_macro_last_arrears_added = 0 }
set_variable = { ac_macro_last_arrears_paid = 0 }
set_variable = { ac_macro_previous_arrears = ac_macro_arrears }
add_to_variable = { ac_macro_cash = ac_macro_last_revenue }
if = { limit = { check_variable = { ac_macro_cash < ac_macro_last_bill } }
 set_temp_variable = { ac_macro_financing = ac_macro_last_bill }
 subtract_from_temp_variable = { ac_macro_financing = ac_macro_cash }
 if = { limit = { check_variable = { ac_macro_financing > ac_macro_credit_room } } set_temp_variable = { ac_macro_financing = ac_macro_credit_room } }
 add_to_variable = { ac_macro_cash = ac_macro_financing }
 add_to_variable = { ac_macro_debt = ac_macro_financing }
 set_variable = { ac_macro_last_borrowed = ac_macro_financing }
}
set_variable = { ac_macro_last_paid = ac_macro_last_bill }
if = { limit = { check_variable = { ac_macro_last_paid > ac_macro_cash } } set_variable = { ac_macro_last_paid = ac_macro_cash } }
subtract_from_variable = { ac_macro_cash = ac_macro_last_paid }
set_variable = { ac_macro_last_arrears_added = ac_macro_last_bill }
subtract_from_variable = { ac_macro_last_arrears_added = ac_macro_last_paid }
add_to_variable = { ac_macro_arrears = ac_macro_last_arrears_added }
set_variable = { ac_macro_funding = 1 }
if = { limit = { check_variable = { ac_macro_last_bill > 0 } }
 set_variable = { ac_macro_funding = ac_macro_last_paid }
 divide_variable = { ac_macro_funding = ac_macro_last_bill }
}
if = { limit = { check_variable = { ac_macro_cash > 0 } check_variable = { ac_macro_arrears > 0 } }
 set_temp_variable = { ac_macro_payment = ac_macro_cash }
 if = { limit = { check_variable = { ac_macro_payment > ac_macro_arrears } } set_temp_variable = { ac_macro_payment = ac_macro_arrears } }
 subtract_from_variable = { ac_macro_cash = ac_macro_payment }
 subtract_from_variable = { ac_macro_arrears = ac_macro_payment }
 set_variable = { ac_macro_last_arrears_paid = ac_macro_payment }
}
add_to_variable = { ac_macro_settlements = 1 }
ac_macro_real_cycle = yes
ac_macro_crisis_cycle = yes
ac_macro_replacement_cycle = yes
ac_macro_ai_policy = yes
ac_macro_quote = yes
'''
    settle = settle.replace('ac_macro_quote = yes\n',
                            'ac_macro_quote = yes\n' + claims.allocate() + money.quote(SHARES, refresh_forces=False) + ledger.snapshot(), 1)
    settle = settle.replace('ac_macro_ai_policy = yes\nac_macro_quote = yes',
                            'ac_macro_ai_policy = yes\n' + ledger.record() + 'ac_macro_quote = yes', 1)
    effect('ac_macro_settle_month',block('if',settle))
    real = '''set_variable = { ac_macro_growth = ac_macro_base_growth }
set_temp_variable = { ac_macro_capacity_change = ac_macro_factory_capacity }
subtract_from_temp_variable = { ac_macro_capacity_change = ac_macro_last_factories }
set_variable = { ac_macro_capacity_growth = ac_macro_capacity_change }
clamp_variable = { var = ac_macro_capacity_growth min = -5 max = 5 }
multiply_variable = { ac_macro_capacity_growth = 0.2 }
add_to_variable = { ac_macro_growth = ac_macro_capacity_growth }
set_variable = { ac_macro_last_factories = ac_macro_factory_capacity }
set_temp_variable = { ac_macro_development_effect = ac_macro_budget_development }
multiply_temp_variable = { ac_macro_development_effect = 0.3 }
add_to_temp_variable = { ac_macro_development_effect = ac_macro_budget_education }
multiply_temp_variable = { ac_macro_development_effect = 0.3 }
multiply_temp_variable = { ac_macro_development_effect = ac_macro_funding }
# Smooth investment benefits; they do not appear immediately on a policy click.
multiply_variable = { ac_macro_growth_lag = 0.8 }
multiply_temp_variable = { ac_macro_development_effect = 0.2 }
add_to_variable = { ac_macro_growth_lag = ac_macro_development_effect }
add_to_variable = { ac_macro_growth = ac_macro_growth_lag }
if = { limit = { check_variable = { ac_macro_income_tax > 0.25 } } add_to_variable = { ac_macro_growth = -1 } }
if = { limit = { check_variable = { ac_macro_funding < 0.9 } } add_to_variable = { ac_macro_growth = -2 } }
if = { limit = { has_war = yes } add_to_variable = { ac_macro_growth = -3 } }
if = { limit = { has_country_flag = ac_macro_crisis } add_to_variable = { ac_macro_growth = -2 } }
if = { limit = { check_variable = { ac_macro_policy_rate > 4 } } add_to_variable = { ac_macro_growth = -0.25 } }
clamp_variable = { var = ac_macro_growth min = -20 max = 10 }
set_temp_variable = { ac_macro_growth_factor = ac_macro_growth }
divide_temp_variable = { ac_macro_growth_factor = 1200 }
add_to_temp_variable = { ac_macro_growth_factor = 1 }
every_controlled_state = {
 if = { limit = { has_variable = ac_macro_real_output OR = { NOT = { has_variable = ac_macro_state_last_cycle } check_variable = { ac_macro_state_last_cycle < date } } }
  # Productive growth/repair belongs to the state and this accounting boundary.
  # A controller change between country callbacks must not apply it twice.
  set_variable = { ac_macro_state_last_cycle = date }
  set_temp_variable = { ac_macro_state_growth_factor = PREV.ac_macro_growth }
  divide_temp_variable = { ac_macro_state_growth_factor = 1200 }
  add_to_temp_variable = { ac_macro_state_growth_factor = 1 }
  multiply_variable = { ac_macro_real_output = ac_macro_state_growth_factor }
  set_temp_variable = { ac_macro_state_repair = PREV.ac_macro_budget_development }
  add_to_temp_variable = { ac_macro_state_repair = 1 }
  multiply_temp_variable = { ac_macro_state_repair = 0.005 }
  multiply_temp_variable = { ac_macro_state_repair = PREV.ac_macro_funding }
  subtract_from_variable = { ac_macro_disruption = ac_macro_state_repair }
  clamp_variable = { var = ac_macro_disruption min = 0 max = 0.75 }
 }
}
set_temp_variable = { ac_macro_inflation_gap = 2 }
subtract_from_temp_variable = { ac_macro_inflation_gap = ac_macro_inflation }
multiply_temp_variable = { ac_macro_inflation_gap = 0.1 }
add_to_variable = { ac_macro_inflation = ac_macro_inflation_gap }
if = { limit = { has_war = yes } add_to_variable = { ac_macro_inflation = 0.15 } }
set_temp_variable = { ac_macro_supply_pressure = ac_macro_output_gap }
multiply_temp_variable = { ac_macro_supply_pressure = 0.3 }
add_to_variable = { ac_macro_inflation = ac_macro_supply_pressure }
if = { limit = { check_variable = { ac_macro_policy_rate > 4 } } add_to_variable = { ac_macro_inflation = -0.1 } }
if = { limit = { check_variable = { ac_macro_policy_rate < 4 } } add_to_variable = { ac_macro_inflation = 0.1 } }
clamp_variable = { var = ac_macro_inflation min = -5 max = 25 }
set_temp_variable = { ac_macro_price_factor = ac_macro_inflation }
divide_temp_variable = { ac_macro_price_factor = 1200 }
add_to_temp_variable = { ac_macro_price_factor = 1 }
multiply_variable = { ac_macro_price_index = ac_macro_price_factor }
set_temp_variable = { ac_macro_readiness_delta = ac_macro_budget_defense }
add_to_temp_variable = { ac_macro_readiness_delta = 6 }
multiply_temp_variable = { ac_macro_readiness_delta = ac_macro_funding }
add_to_temp_variable = { ac_macro_readiness_delta = -6 }
add_to_variable = { ac_macro_readiness = ac_macro_readiness_delta }
clamp_variable = { var = ac_macro_readiness min = 0 max = 100 }
set_variable = { ac_macro_readiness_modifier = ac_macro_readiness }
divide_variable = { ac_macro_readiness_modifier = 1000 }
add_to_variable = { ac_macro_readiness_modifier = -0.1 }
set_variable = { ac_macro_service_modifier = ac_macro_budget_services }
multiply_variable = { ac_macro_service_modifier = 0.01 }
multiply_variable = { ac_macro_service_modifier = ac_macro_funding }
add_to_variable = { ac_macro_service_modifier = -0.01 }
set_variable = { ac_macro_construction_modifier = ac_macro_budget_development }
multiply_variable = { ac_macro_construction_modifier = 0.025 }
multiply_variable = { ac_macro_construction_modifier = ac_macro_funding }
add_to_variable = { ac_macro_construction_modifier = -0.025 }
set_variable = { ac_macro_research_modifier = ac_macro_budget_education }
multiply_variable = { ac_macro_research_modifier = 0.015 }
multiply_variable = { ac_macro_research_modifier = ac_macro_funding }
add_to_variable = { ac_macro_research_modifier = -0.015 }
'''
    effect('ac_macro_real_cycle',guard(real))
    crisis = '''# The warning begins after two failed settlements. Its three correction
# months begin with the next scheduled settlement, not the warning's own month.
if = { limit = { has_country_flag = ac_macro_warning }
 add_to_variable = { ac_macro_warning_months = 1 }
 set_variable = { ac_macro_warning_months_left = 3 }
 subtract_from_variable = { ac_macro_warning_months_left = ac_macro_warning_months }
 clamp_variable = { var = ac_macro_warning_months_left min = 0 max = 3 }
}
if = { limit = { check_variable = { ac_macro_funding < 0.9 } }
 add_to_variable = { ac_macro_stress_months = 1 }
 set_variable = { ac_macro_recovery_months = 0 }
 if = { limit = { check_variable = { ac_macro_stress_months > 1 } NOT = { has_country_flag = ac_macro_warning } }
  set_country_flag = ac_macro_warning
  set_variable = { ac_macro_warning_months = 0 }
  set_variable = { ac_macro_warning_months_left = 3 }
  country_event = { id = ac_macro.1 days = 1 }
 }
 if = { limit = { has_country_flag = ac_macro_warning check_variable = { ac_macro_warning_months > 2 } NOT = { has_country_flag = ac_macro_crisis } }
  set_country_flag = ac_macro_crisis
  country_event = { id = ac_macro.2 days = 1 }
 }
}
else = {
 set_variable = { ac_macro_stress_months = 0 }
 if = { limit = { OR = { check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_arrears < ac_macro_previous_arrears } } }
  add_to_variable = { ac_macro_recovery_months = 1 }
 }
 else = { set_variable = { ac_macro_recovery_months = 0 } }
 if = { limit = { check_variable = { ac_macro_recovery_months > 2 } }
  clr_country_flag = ac_macro_warning
  set_variable = { ac_macro_warning_months = 0 }
  set_variable = { ac_macro_warning_months_left = 0 }
  if = { limit = { has_country_flag = ac_macro_crisis } clr_country_flag = ac_macro_crisis country_event = { id = ac_macro.3 days = 1 } }
 }
}
'''
    effect('ac_macro_crisis_cycle',guard(crisis))
    effect('ac_macro_borrow','ac_macro_quote = yes\n'+block('if','limit = { ac_macro_can_borrow = yes }\nadd_to_variable = { ac_macro_cash = ac_macro_loan_size }\nadd_to_variable = { ac_macro_debt = ac_macro_loan_size }\nac_macro_quote = yes'))
    effect('ac_macro_repay',block('if','''limit = { ac_macro_can_repay = yes }
set_temp_variable = { ac_macro_payment = ac_macro_loan_size }
if = { limit = { check_variable = { ac_macro_payment > ac_macro_cash } } set_temp_variable = { ac_macro_payment = ac_macro_cash } }
if = { limit = { check_variable = { ac_macro_payment > ac_macro_debt } } set_temp_variable = { ac_macro_payment = ac_macro_debt } }
subtract_from_variable = { ac_macro_cash = ac_macro_payment }
subtract_from_variable = { ac_macro_debt = ac_macro_payment }
ac_macro_quote = yes'''))
    # A result flag is per-call diagnostic state, not an inactive fiscal write.
    # Always clear it before readiness so a previous success cannot be reused.
    effect('ac_macro_try_spend','clr_country_flag = ac_macro_transaction_succeeded\n'+guard('''if = { limit = { check_variable = { ac_macro_transaction_amount >= 0.001 } check_variable = { ac_macro_arrears = 0 } check_variable = { ac_macro_cash >= ac_macro_transaction_amount } }
 subtract_from_variable = { ac_macro_cash = ac_macro_transaction_amount }
 set_country_flag = ac_macro_transaction_succeeded
}
ac_macro_quote = yes'''))
    effect('ac_macro_receive',guard('''if = { limit = { check_variable = { ac_macro_transaction_amount > 0 } }
 add_to_variable = { ac_macro_cash = ac_macro_transaction_amount }
}
ac_macro_quote = yes'''))
    effect('ac_macro_change_commitment',guard('''add_to_variable = { ac_macro_commitments_annual = ac_macro_commitment_delta }
clamp_variable = { var = ac_macro_commitments_annual min = 0 }
ac_macro_quote = yes'''))
    effect('ac_macro_apply_disruption',guard('''set_variable = { ac_macro_pending_disruption = ac_macro_disruption_delta }
clamp_variable = { var = ac_macro_pending_disruption min = 0 max = 0.75 }
every_controlled_state = {
 if = { limit = { has_variable = ac_macro_real_output }
  add_to_variable = { ac_macro_disruption = PREV.ac_macro_pending_disruption }
  clamp_variable = { var = ac_macro_disruption min = 0 max = 0.75 }
 }
}
ac_macro_quote = yes'''))
    effect('ac_macro_fund_replacements',block('if','''limit = { ac_macro_can_fund_replacements = yes }
subtract_from_variable = { ac_macro_cash = 0.005 }
set_variable = { ac_macro_replacement_escrow = 0.005 }
set_variable = { ac_macro_replacement_target = total_equipment_produced_infantry }
add_to_variable = { ac_macro_replacement_target = 100 }
ac_macro_quote = yes'''))
    effect('ac_macro_cancel_replacements',guard('''if = { limit = { check_variable = { ac_macro_replacement_escrow > 0 } }
 add_to_variable = { ac_macro_cash = ac_macro_replacement_escrow }
 set_variable = { ac_macro_replacement_escrow = 0 }
}
ac_macro_quote = yes'''))
    effect('ac_macro_replacement_cycle',block('if','''limit = { ac_macro_can_produce = yes check_variable = { ac_macro_replacement_escrow > 0 } check_variable = { ac_macro_replacement_target <= total_equipment_produced_infantry } }
set_variable = { ac_macro_replacement_escrow = 0 }
add_to_variable = { ac_macro_readiness = 2 }
clamp_variable = { var = ac_macro_readiness min = 0 max = 100 }
# The native queue already produced the equipment. Never grant another stockpile.
'''))
    for title, rates in [('low',(.16,.16,.04)),('standard',(.20,.20,.05)),('high',(.26,.24,.08))]:
        body = 'limit = { ac_macro_can_change_policy = yes }\n'+''.join(f'set_variable = {{ ac_macro_{name}_tax = {rate} }}\n' for name,rate in zip(('income','business','consumption'),rates))
        body += 'set_country_flag = { flag = ac_macro_policy_cooldown days = 30 }\nac_macro_quote = yes'
        effect('ac_macro_tax_'+title,block('if',body))
    for lane,maximum in [('income',.4),('business',.35),('consumption',.15)]:
        for direction,delta in [('up',.02),('down',-.02)]:
            effect('ac_macro_'+lane+'_tax_'+direction,block('if',f'''limit = {{ ac_macro_can_change_policy = yes }}
add_to_variable = {{ ac_macro_{lane}_tax = {delta} }}
clamp_variable = {{ var = ac_macro_{lane}_tax min = 0 max = {maximum} }}
set_country_flag = {{ flag = ac_macro_policy_cooldown days = 30 }}
ac_macro_quote = yes'''))
    for preset, values in PRESETS.items():
        body = 'limit = { ac_macro_can_change_policy = yes }\n'+''.join(f'set_variable = {{ ac_macro_budget_{name} = {level} }}\n' for name,level in zip(CATEGORIES,values))
        body += 'set_country_flag = { flag = ac_macro_policy_cooldown days = 30 }\nac_macro_quote = yes'
        effect('ac_macro_preset_'+preset,block('if',body))
    for c in CATEGORIES:
        for direction,delta in [('up',1),('down',-1)]:
            effect('ac_macro_'+c+'_'+direction,block('if',f'limit = {{ ac_macro_can_change_policy = yes }}\nadd_to_variable = {{ ac_macro_budget_{c} = {delta} }}\nclamp_variable = {{ var = ac_macro_budget_{c} min = 0 max = 2 }}\nset_country_flag = {{ flag = ac_macro_policy_cooldown days = 30 }}\nac_macro_quote = yes'))
    for direction,delta in [('up',2),('down',-2)]:
        effect('ac_macro_policy_rate_'+direction,block('if',f'limit = {{ ac_macro_can_change_policy = yes }}\nadd_to_variable = {{ ac_macro_policy_rate = {delta} }}\nclamp_variable = {{ var = ac_macro_policy_rate min = 2 max = 8 }}\nset_country_flag = {{ flag = ac_macro_policy_cooldown days = 30 }}\nac_macro_quote = yes'))
    effect('ac_macro_ai_policy',block('if','''limit = { ac_macro_ready = yes is_ai = yes }
if = { limit = { check_variable = { ac_macro_funding < 0.95 } }
 if = { limit = { check_variable = { ac_macro_income_tax < 0.26 } } ac_macro_tax_high = yes }
 else = { ac_macro_preset_stabilization = yes }
}
else_if = { limit = { has_war = yes } ac_macro_preset_mobilization = yes }
else_if = { limit = { check_variable = { ac_macro_arrears > 0 } } ac_macro_preset_balanced = yes }
else = {
 set_temp_variable = { ac_macro_reserve = ac_macro_bill }
 multiply_temp_variable = { ac_macro_reserve = 3 }
 if = { limit = { check_variable = { ac_macro_cash > ac_macro_reserve } } ac_macro_repay = yes }
}
'''))
    return '# Original macroeconomic gameplay; amounts in billions of abstract units.\n'+''.join(e.values())


def rules():
    return '''ac_economy = {
 name = ac_economy_rule group = ac_economy_rule_group
 default = { name = full text = ac_economy_full desc = ac_economy_full_desc }
 option = { name = disabled text = ac_economy_disabled desc = ac_economy_disabled_desc }
 option = { name = experimental text = ac_economy_experimental desc = ac_economy_experimental_desc }
}
'''


def build():
    data = json.loads((HERE/'profiles.json').read_text())
    out = legacy_and_adapters()
    out['common/scripted_effects/ac_macro_profiles.txt'] = profile_effects(data)
    out['common/scripted_effects/ac_macro_effects.txt'] = economic_effects()
    out['common/scripted_effects/ac_macro_ledger.txt'] = ledger.effects()
    out['common/scripted_triggers/ac_macro_triggers.txt'] = macro_triggers(out['common/scripted_effects/ac_macro_effects.txt'])
    out['common/game_rules/ac_economy_rules.txt'] = rules()
    out['common/on_actions/ac_macro_on_actions.txt'] = '''on_actions = {
 on_startup = { effect = { every_country = { limit = { ac_macro_mode = yes } ac_macro_initialize = yes } } }
 on_monthly = { effect = { ac_macro_initialize = yes if = { limit = { ac_macro_ready = yes } set_country_flag = ac_macro_monthly_authorized ac_macro_settle_month = yes clr_country_flag = ac_macro_monthly_authorized } } }
}
'''
    out['common/dynamic_modifiers/ac_macro_modifiers.txt'] = '''ac_macro_economy_modifier = {
 enable = { ac_macro_ready = yes }
 stability_factor = ac_macro_service_modifier
 production_speed_buildings_factor = ac_macro_construction_modifier
 research_speed_factor = ac_macro_research_modifier
 army_org_factor = ac_macro_readiness_modifier
 air_mission_efficiency = ac_macro_readiness_modifier
}
'''
    out['events/ac_macro_events.txt'] = 'add_namespace = ac_macro\n'+''.join(block('country_event',f'''id = ac_macro.{i}
title = ac_macro.{i}.t desc = ac_macro.{i}.d picture = GFX_report_event_bad_news_1
is_triggered_only = yes
trigger = {{ ac_macro_ready = yes }}
option = {{ name = ac_macro.{i}.a }}''') for i in (1,2,3))
    from ui import build_ui
    out.update(build_ui())
    return out


def history_marker(text):
    text = re.sub(r'# BEGIN ECONOMY V2 NEW CAMPAIGN\n.*?# END ECONOMY V2 NEW CAMPAIGN\n?', '', text, flags=re.S)
    # Other new-campaign authors may own a trailing setup section even when a
    # country already has a recruited leader. Keep eligibility before that
    # foreign section so its generator and this one do not move it each turn.
    anchor = next((marker for marker in ('# BEGIN EXPANSION START LEADER', '# BEGIN WORLD FOUNDATION', '# BEGIN LEGACY WORLD START STOCKS') if marker in text), None)
    if anchor is not None:
        prefix, suffix = text.split(anchor, 1)
        return prefix.rstrip()+'\n\n'+MARKER+'\n'+anchor+suffix
    return text.rstrip()+'\n\n'+MARKER


def main():
    p=argparse.ArgumentParser(); p.add_argument('--capture-inputs',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    HERE.mkdir(parents=True,exist_ok=True)
    if a.capture_inputs: capture_inputs()
    out = build()
    for row in json.loads((HERE/'profiles.json').read_text())['profiles']:
        out[row['history']] = history_marker((MOD/row['history']).read_text(encoding='utf-8-sig'))
    for rel,text in out.items():
        target=MOD/rel
        data_bytes = text if isinstance(text,bytes) else text.encode('utf-8')
        if a.check:
            if not target.exists() or target.read_bytes().replace(b'\r\n',b'\n')!=data_bytes.replace(b'\r\n',b'\n'):
                raise SystemExit('Economy v2 output differs: '+rel)
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data_bytes)
    print('Full macroeconomy generated; legacy mode remains separate; native acceptance pending.')


if __name__=='__main__':main()
