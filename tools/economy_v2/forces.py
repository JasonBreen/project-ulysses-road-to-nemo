"""Observed operating-cost proxies, with explicit overlap-safe lower bounds.

The captured primary engine contract documents quantity queries, not native
runtime results. Never add legacy aliases to designer-family observations.
Aircraft may carry multiple type tags: total aircraft pays one base and one
maximum role-premium pool, not a sum of possibly overlapping role invoices.
"""
import json
from functools import lru_cache
from pathlib import Path

DATA = json.loads((Path(__file__).with_name('force_observables.json')).read_text())


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t' + line for line in body.splitlines()) + '\n}\n'


@lru_cache(maxsize=1)
def observable_names():
    names = set()
    for family in DATA['armor_families']:
        names.update('num_equipment_in_armies_k@' + ident for ident in [family['parent'], *family['children']])
    for group in DATA['land'].values():
        names.update('num_equipment_in_armies_k@' + ident for ident in group['archetypes'])
    for group in DATA['air_roles'].values():
        names.update('num_deployed_planes_with_type@' + ident for ident in group['types'])
    return names


def snapshot():
    body = '# Equipment counts describe army holdings, never stockpile totals.\nset_variable = { ac_macro_land_armor_k = 0 }\n'
    for family in DATA['armor_families']:
        body += f'set_temp_variable = {{ ac_macro_armor_parent = num_equipment_in_armies_k@{family["parent"]} }}\n'
        body += 'set_temp_variable = { ac_macro_armor_derived = 0 }\n'
        for child in family['children']:
            body += f'add_to_temp_variable = {{ ac_macro_armor_derived = num_equipment_in_armies_k@{child} }}\n'
        body += block('if', 'limit = { check_variable = { ac_macro_armor_derived > ac_macro_armor_parent } }\nset_temp_variable = { ac_macro_armor_parent = ac_macro_armor_derived }')
        body += 'add_to_variable = { ac_macro_land_armor_k = ac_macro_armor_parent }\n'
    body += 'clamp_variable = { var = ac_macro_land_armor_k min = 0 }\n'
    for name, group in DATA['land'].items():
        target = 'ac_macro_land_' + name + '_k'
        body += f'set_variable = {{ {target} = 0 }}\n'
        for ident in group['archetypes']:
            body += f'add_to_variable = {{ {target} = num_equipment_in_armies_k@{ident} }}\n'
        body += f'clamp_variable = {{ var = {target} min = 0 }}\n'
    body += '# Secondary aircraft types overlap. Observe them, but never sum them as tails.\nset_variable = { ac_macro_air_premium_annual = 0 }\n'
    for name, group in DATA['air_roles'].items():
        target = 'ac_macro_air_' + name
        body += f'set_variable = {{ {target} = 0 }}\n'
        for role in group['types']:
            body += block('if', f'limit = {{ check_variable = {{ num_deployed_planes_with_type@{role} > {target} }} }}\nset_variable = {{ {target} = num_deployed_planes_with_type@{role} }}')
        body += f'clamp_variable = {{ var = {target} min = 0 max = ac_macro_planes }}\n'
        body += f'set_temp_variable = {{ ac_macro_role_premium = {target} }}\nmultiply_temp_variable = {{ ac_macro_role_premium = {group["annual_premium"]} }}\n'
        body += block('if', 'limit = { check_variable = { ac_macro_role_premium > ac_macro_air_premium_annual } }\nset_variable = { ac_macro_air_premium_annual = ac_macro_role_premium }')
    return body


def cost_inputs():
    rows = [('ac_macro_personnel', .06), ('num_deployed_planes', DATA['air_base_annual_billion']),
            ('num_ships', .08), ('num_ships_with_type@carrier', .8), ('num_ships_with_type@submarine', .02),
            ('ac_macro_land_armor_k', DATA['armor_annual_billion_per_thousand']),
            ('ac_macro_air_premium_annual', 1)]
    rows += [('ac_macro_land_' + name + '_k', group['annual_billion_per_thousand']) for name, group in DATA['land'].items()]
    return rows
