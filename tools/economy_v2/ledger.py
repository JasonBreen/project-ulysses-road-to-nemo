"""Persistent monthly results and read-only graph frames for economy v2.

Only the authorized settlement calls record. UI and quotation never shift the
ring or fabricate a historical payment. Twelve retained observations are monthly
accounting boundaries, not an assertion that a late-created account existed in
1991. Graphs use discrete engine-supported sprite frames, not dynamic geometry.
The approved 0.001b monthly quantum and separate fractional milli-unit carries
are implemented in money.py and retained here as accrued and settled values;
this is provisional gameplay accounting, not a canon currency or a claim that
the native engine preserves every upstream fractional calculation.
"""

FIELDS = {
    'real': 'ac_macro_last_real_gdp',
    'nominal': 'ac_macro_last_nominal_gdp',
    'prices': 'ac_macro_last_prices',
    'revenue': 'ac_macro_last_revenue',
    'bill': 'ac_macro_last_bill',
    'paid': 'ac_macro_last_paid',
    'borrowed': 'ac_macro_last_borrowed',
    'arrears_added': 'ac_macro_last_arrears_added',
    'arrears_paid': 'ac_macro_last_arrears_paid',
    'cash': 'ac_macro_cash',
    'debt': 'ac_macro_debt',
    'arrears': 'ac_macro_arrears',
    'funding': 'ac_macro_last_funding',
    'sequence': 'ac_macro_settlements',
    'net': 'ac_macro_last_balance',
    'revenue_accrued_milli': 'ac_macro_last_revenue_accrued_milli',
    'bill_accrued_milli': 'ac_macro_last_bill_accrued_milli',
    'revenue_carry_milli': 'ac_macro_revenue_carry_milli',
    'bill_carry_milli': 'ac_macro_bill_carry_milli',
    'escrow': 'ac_macro_replacement_escrow',
}


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t' + line for line in body.splitlines()) + '\n}\n'


def initialize():
    body = 'set_variable = { ac_macro_history_count = 0 }\nset_variable = { ac_macro_history_last_recorded = 0 }\n'
    for name in ('real_gdp', 'nominal_gdp', 'prices', 'funding', 'balance'):
        body += 'set_variable = { ac_macro_last_' + name + ' = 0 }\n'
    for i in range(12):
        for field in FIELDS:
            body += f'set_variable = {{ ac_macro_history_{i}_{field} = 0 }}\n'
        for field in ('output', 'net_positive', 'net_negative'):
            body += f'set_variable = {{ ac_macro_graph_{i}_{field} = 1 }}\n'
    return body


def snapshot():
    return '''# Preserve the annual bases used to bill this settlement, not the next forecast.
set_variable = { ac_macro_last_real_gdp = ac_macro_real_gdp }
set_variable = { ac_macro_last_nominal_gdp = ac_macro_nominal_gdp }
set_variable = { ac_macro_last_prices = ac_macro_price_index }
'''


def effects():
    body = '''limit = {
 ac_macro_ready = yes
 has_country_flag = ac_macro_ledger_authorized
 check_variable = { ac_macro_history_last_recorded < ac_macro_settlements }
}
clr_country_flag = ac_macro_ledger_authorized
set_variable = { ac_macro_history_last_recorded = ac_macro_settlements }
set_variable = { ac_macro_last_funding = ac_macro_funding }
set_variable = { ac_macro_last_balance = ac_macro_last_revenue }
subtract_from_variable = { ac_macro_last_balance = ac_macro_last_bill }
'''
    # Copy oldest first so the source is not overwritten by the preceding move.
    for i in range(11, 0, -1):
        for field in FIELDS:
            body += f'set_variable = {{ ac_macro_history_{i}_{field} = ac_macro_history_{i - 1}_{field} }}\n'
    for field, source in FIELDS.items():
        body += f'set_variable = {{ ac_macro_history_0_{field} = {source} }}\n'
    body += '''add_to_variable = { ac_macro_history_count = 1 }
clamp_variable = { var = ac_macro_history_count min = 0 max = 12 }
set_variable = { ac_macro_graph_output_max = 0.001 }
set_variable = { ac_macro_graph_net_max = 0.001 }
'''
    for i in range(12):
        body += block('if', f'limit = {{ check_variable = {{ ac_macro_history_count > {i} }} }}\n' +
            block('if', f'limit = {{ check_variable = {{ ac_macro_history_{i}_real > ac_macro_graph_output_max }} }}\nset_variable = {{ ac_macro_graph_output_max = ac_macro_history_{i}_real }}') +
            f'set_temp_variable = {{ ac_macro_graph_absolute = ac_macro_history_{i}_net }}\n' +
            block('if', 'limit = { check_variable = { ac_macro_graph_absolute < 0 } }\nmultiply_temp_variable = { ac_macro_graph_absolute = -1 }') +
            block('if', 'limit = { check_variable = { ac_macro_graph_absolute > ac_macro_graph_net_max } }\nset_variable = { ac_macro_graph_net_max = ac_macro_graph_absolute }'))
    for i in range(12):
        inner = f'''set_variable = {{ ac_macro_graph_{i}_output = ac_macro_history_{i}_real }}
divide_variable = {{ ac_macro_graph_{i}_output = ac_macro_graph_output_max }}
multiply_variable = {{ ac_macro_graph_{i}_output = 32 }}
round_variable = ac_macro_graph_{i}_output
add_to_variable = {{ ac_macro_graph_{i}_output = 1 }}
set_variable = {{ ac_macro_graph_{i}_net_positive = 1 }}
set_variable = {{ ac_macro_graph_{i}_net_negative = 1 }}
'''
        for direction, comparison, sign in (('positive', '>', 1), ('negative', '<', -1)):
            inner += block('if', f'limit = {{ check_variable = {{ ac_macro_history_{i}_net {comparison} 0 }} }}\n' +
                f'''set_variable = {{ ac_macro_graph_{i}_net_{direction} = ac_macro_history_{i}_net }}
divide_variable = {{ ac_macro_graph_{i}_net_{direction} = ac_macro_graph_net_max }}
multiply_variable = {{ ac_macro_graph_{i}_net_{direction} = {32 * sign} }}
round_variable = ac_macro_graph_{i}_net_{direction}
add_to_variable = {{ ac_macro_graph_{i}_net_{direction} = 1 }}''')
        for field in ('output', 'net_positive', 'net_negative'):
            inner += f'clamp_variable = {{ var = ac_macro_graph_{i}_{field} min = 1 max = 33 }}\n'
        body += block('if', f'limit = {{ check_variable = {{ ac_macro_history_count > {i} }} }}\n' + inner)
    return block('ac_macro_record_ledger', block('if', body))


def record():
    return '''# Private receipt: this month may create one historical record.
set_country_flag = ac_macro_ledger_authorized
ac_macro_record_ledger = yes
clr_country_flag = ac_macro_ledger_authorized
'''
