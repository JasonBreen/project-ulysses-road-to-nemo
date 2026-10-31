"""Approved provisional accounting policy; not a claim about native precision.

Cash settlements use a 0.001-billion quantum. Forecasts accrue in milli-units
(one unit =0.001b), retaining a separate fractional receipt and obligation carry.
Only authorized monthly settlement consumes those carries. Scale small bases
before policy fractions/division; scale large bases after reducing them so the
ordinary 2020 scenario avoids gratuitously large intermediates. Native rounding,
range and precision still require engine probes; lost upstream precision cannot
be reconstructed by this accounting owner.
"""
import forces


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t' + line for line in body.splitlines()) + '\n}\n'


def monthly_milli(target, source, factors=(), divisor=12):
    body = f'set_variable = {{ {target} = {source} }}\nset_temp_variable = {{ ac_macro_scaled_early = 0 }}\n'
    body += block('if', f'limit = {{ check_variable = {{ {target} < 1000 }} }}\n'
                  f'multiply_variable = {{ {target} = 1000 }}\nset_temp_variable = {{ ac_macro_scaled_early = 1 }}')
    body += ''.join(f'multiply_variable = {{ {target} = {factor} }}\n' for factor in factors)
    body += f'divide_variable = {{ {target} = {divisor} }}\n'
    body += block('if', f'limit = {{ check_variable = {{ ac_macro_scaled_early = 0 }} }}\nmultiply_variable = {{ {target} = 1000 }}')
    return body


def display(target, source):
    return f'set_variable = {{ {target} = {source} }}\ndivide_variable = {{ {target} = 1000 }}\n'


def initialize():
    return ''.join('set_variable = { ac_macro_' + name + ' = 0 }\n' for name in (
        'revenue_carry_milli', 'bill_carry_milli', 'last_revenue_accrued_milli', 'last_bill_accrued_milli'))


def quote(shares, refresh_forces=True):
    body = 'set_variable = { ac_macro_revenue_milli = 0 }\n'
    for tax, share in [('income', .55), ('business', .25), ('consumption', .65)]:
        target = 'ac_macro_revenue_' + tax + '_milli'
        body += monthly_milli(target, 'ac_macro_tax_base', (share, 'ac_macro_' + tax + '_tax', 'ac_macro_effective_collection'))
        body += f'add_to_variable = {{ ac_macro_revenue_milli = {target} }}\n'
        body += display('ac_macro_revenue_' + tax, target)
    body += display('ac_macro_revenue', 'ac_macro_revenue_milli')
    body += 'set_variable = { ac_macro_operating_milli = 0 }\n'
    for category, share in shares.items():
        target = 'ac_macro_spending_' + category + '_milli'
        body += f'''set_temp_variable = {{ ac_macro_category_factor = ac_macro_budget_{category} }}
multiply_temp_variable = {{ ac_macro_category_factor = 0.25 }}
add_to_temp_variable = {{ ac_macro_category_factor = 0.75 }}
'''
        body += monthly_milli(target, 'ac_macro_nominal_gdp', (share, 'ac_macro_category_factor'))
        body += f'add_to_variable = {{ ac_macro_operating_milli = {target} }}\n'
    force_body = '''set_temp_variable = { ac_macro_personnel = deployed_army_manpower_k }
add_to_temp_variable = { ac_macro_personnel = deployed_navy_manpower_k }
add_to_temp_variable = { ac_macro_personnel = deployed_airforce_manpower_k }
set_temp_variable = { ac_macro_war_factor = 1 }
if = { limit = { has_war = yes } set_temp_variable = { ac_macro_war_factor = 1.5 } }
set_variable = { ac_macro_upkeep_milli = 0 }
'''
    force_body += forces.snapshot()
    for source, factor in forces.cost_inputs():
        force_body += monthly_milli('ac_macro_force_part_milli', source, (factor, 'ac_macro_war_factor'))
        force_body += 'add_to_variable = { ac_macro_upkeep_milli = ac_macro_force_part_milli }\n'
    if refresh_forces:
        body += force_body
    body += display('ac_macro_upkeep', 'ac_macro_upkeep_milli')
    body += '''if = { limit = { check_variable = { ac_macro_upkeep_milli > ac_macro_spending_defense_milli } }
 subtract_from_variable = { ac_macro_operating_milli = ac_macro_spending_defense_milli }
 set_variable = { ac_macro_spending_defense_milli = ac_macro_upkeep_milli }
 add_to_variable = { ac_macro_operating_milli = ac_macro_spending_defense_milli }
}
'''
    for category in shares:
        body += display('ac_macro_spending_' + category, 'ac_macro_spending_' + category + '_milli')
    body += display('ac_macro_operating', 'ac_macro_operating_milli')
    body += '''set_variable = { ac_macro_debt_ratio = 0 }
if = { limit = { check_variable = { ac_macro_nominal_gdp > 0 } }
 set_variable = { ac_macro_debt_ratio = ac_macro_debt }
 divide_variable = { ac_macro_debt_ratio = ac_macro_nominal_gdp }
}
set_variable = { ac_macro_interest_rate = ac_macro_policy_rate }
if = { limit = { check_variable = { ac_macro_debt_ratio > 0.6 } } add_to_variable = { ac_macro_interest_rate = 2 } }
if = { limit = { check_variable = { ac_macro_debt_ratio > 1 } } add_to_variable = { ac_macro_interest_rate = 3 } }
if = { limit = { check_variable = { ac_macro_arrears > 0 } } add_to_variable = { ac_macro_interest_rate = 3 } }
'''
    body += monthly_milli('ac_macro_interest_milli', 'ac_macro_debt', ('ac_macro_interest_rate',), 1200)
    body += display('ac_macro_interest', 'ac_macro_interest_milli')
    body += monthly_milli('ac_macro_commitment_month_milli', 'ac_macro_commitments_annual')
    body += '''set_variable = { ac_macro_bill_milli = ac_macro_operating_milli }
add_to_variable = { ac_macro_bill_milli = ac_macro_interest_milli }
add_to_variable = { ac_macro_bill_milli = ac_macro_commitment_month_milli }
'''
    body += display('ac_macro_bill', 'ac_macro_bill_milli')
    body += '''set_variable = { ac_macro_balance = ac_macro_revenue }
subtract_from_variable = { ac_macro_balance = ac_macro_bill }
'''
    return body


def settle():
    body = '# Accrual includes sub-quantum flows; cash and billed arrears use whole0.001b quanta.\n'
    for field in ('revenue', 'bill'):
        body += f'''set_variable = {{ ac_macro_last_{field}_accrued_milli = ac_macro_{field}_milli }}
set_temp_variable = {{ ac_macro_to_settle = ac_macro_{field}_milli }}
add_to_temp_variable = {{ ac_macro_to_settle = ac_macro_{field}_carry_milli }}
set_temp_variable = {{ ac_macro_whole_quanta = ac_macro_to_settle }}
round_temp_variable = ac_macro_whole_quanta
'''
        # Round then correct any upward result: floor for nonnegative accruals,
        # independent of which nearest-integer tie convention the engine uses.
        body += block('if', 'limit = { check_variable = { ac_macro_whole_quanta > ac_macro_to_settle } }\nsubtract_from_temp_variable = { ac_macro_whole_quanta = 1 }')
        body += f'''set_variable = {{ ac_macro_{field}_carry_milli = ac_macro_to_settle }}
subtract_from_variable = {{ ac_macro_{field}_carry_milli = ac_macro_whole_quanta }}
set_variable = {{ ac_macro_last_{field} = ac_macro_whole_quanta }}
divide_variable = {{ ac_macro_last_{field} = 1000 }}
'''
    return body
