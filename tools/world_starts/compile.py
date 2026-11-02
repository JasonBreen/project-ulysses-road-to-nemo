"""Compile reviewed new active starts; old saves receive no setup callback."""
import argparse
import copy
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools/usea_expansion'), str(ROOT / 'tools')]
from script import parse, get, setv, render
from shared_logistics import compose
from capabilities import AIR, NAVY, LAND, COMMON_TECH, equipment_for, design_for, supports, retained_tree, template_plans, ARMOR, case_key
from technical import Engine

NOTE = '# Active-world foundation: provisional gameplay; tools/world_starts profiles, placements and primary worksheets.\n'
MARKER = '# BEGIN WORLD FOUNDATION'
END = '# END WORLD FOUNDATION'


def block(key, text):
    return key + ' = {\n' + '\n'.join('\t' + line for line in text.splitlines()) + '\n}\n'


def production(tag, role, amount, bba=False, mtg=False, nsb=False):
    design = design_for(role, bba, mtg, nsb)
    equipment = 'type = ' + equipment_for(role, bba, mtg, nsb) + '\ncreator = ' + tag
    if design:
        equipment += '\nversion_name = "' + tag + ' ' + design['label'] + '"'
    #50 is the installed native history/OOB convention (GER/USA_1936), not
    # the fractional example used by the standalone effect documentation.
    return block('add_equipment_production', block('equipment', equipment) + f'requested_factories = {amount}\nprogress = 0.25\nefficiency = 50')


def variant(tag, design):
    return block('create_equipment_variant', f'name = "{tag} {design["label"]}"\ntype = {design["modern"]}\n' +
                 block('modules', '\n'.join(f'{key} = {value}' for key, value in design['modules'].items())))


def technologies(profile, engine, bba, mtg, nsb=False):
    tech = set(COMMON_TECH)
    if any(profile['formations'].get(role) for role in ('motorized', 'mechanized', 'armor')):
        tech.add('tech_logistics_company')
    for unit in profile.get('required_subunits', []):
        if engine.unit(unit).get('active') != 'yes':
            tech.add(engine.unlock(unit, engine.unit_unlocks))
    for old in profile.get('inherited_variants', []):
        tech.add(engine.equipment_tech(old['equipment']))
        tech.update(engine.module_tech(m) for m in old['modules'].values())
    for role in set(profile['production']) | set(profile['naval_production']) | set(profile['stocks']):
        ident = equipment_for(role, bba, mtg, nsb); unlock = engine.equipment_tech(ident)
        if unlock:
            tech.add(unlock)
        design = design_for(role, bba, mtg, nsb)
        if design:
            tech.update(engine.module_tech(m) for m in design['modules'].values())
    for key in tech:
        if key not in engine.tech:
            raise ValueError('Undefined required starting technology: ' + key)
        engine.record(engine.tech_files[key])
    return sorted(tech)


def state_output(row, ident, cfg):
    baseline = row['baseline'][ident]; tree = parse(baseline['source']); state = get(tree, 'state')
    history = get(state, 'history'); buildings = get(history, 'buildings')
    for key, field in [('civilian', 'industrial_complex'), ('military', 'arms_factory'), ('dockyard', 'dockyard'),
                       ('infrastructure', 'infrastructure'), ('air_base', 'air_base'), ('fuel_silo', 'fuel_silo')]:
        if cfg[key] < baseline['buildings'][key]:
            raise ValueError('Inherited building would fall: ' + ident + ':' + key)
        setv(buildings, field, str(cfg[key]))
    for province, level in cfg['naval_bases'].items():
        old = get(buildings, province, []); setv(old, 'naval_base', str(level)); setv(buildings, province, old)
    for province in row['all_supply_hubs']:
        if province in baseline['provinces']:
            old = get(buildings, str(province), []); setv(old, 'supply_node', '1'); setv(buildings, str(province), old)
    for province, points in row['new_victory_points'].items():
        if int(province) in baseline['provinces']:
            history.append(['victory_points', '=', [[province, None, None], [str(points), None, None]]])
    resources = get(state, 'resources', [])
    for key, value in cfg['resources'].items():
        if float(value) < float(baseline['resources'].get(key, 0)):
            raise ValueError('Inherited resource would fall')
        text = str(int(float(value))) if float(value).is_integer() and not isinstance(value, str) else str(value)
        setv(resources, key, text)
    slots = sum(cfg[k] for k in ('civilian', 'military', 'dockyard', 'fuel_silo'))
    caps = {'wasteland': 0, 'enclave': 0, 'tiny_island': 0, 'small_island': 1, 'pastoral': 1,
            'rural': 2, 'large_island': 2, 'town': 4, 'large_town': 5, 'city': 6,
            'large_city': 8, 'metropolis': 10, 'megalopolis': 12}
    category = baseline['category']; factor = float(baseline['max_level_factor'])
    core_multiplier = 1 if baseline['owner'] in baseline['cores'] else 1 + row['non_core_controller_modifiers']['local_building_slots_factor']
    if slots > caps[category] * factor * core_multiplier:
        category = next((k for k in ('town', 'large_town', 'city', 'large_city', 'metropolis', 'megalopolis') if caps[k] * factor * core_multiplier >= slots), 'megalopolis')
        factor = max(factor, math.ceil(slots / (caps[category] * core_multiplier)))
        setv(state, 'state_category', category); setv(state, 'buildings_max_level_factor', f'{factor:.3f}')
    return NOTE + render(tree) + '\n'


def country_output(tag, row, profile, engine=None):
    source = row['country_history_source']
    if profile['mode'] == 'retained_start':
        expected = set(profile['inherited_oob_references'])
        def remove_oob(match):
            if match[1] not in expected: raise ValueError('Unexpected inherited roster reference: ' + match[1])
            return ''
        source = re.sub(r'^\s*(?:set_oob|load_oob|set_air_oob|set_naval_oob)\s*=\s*"([^"\n]+)"\s*$', remove_oob, source, flags=re.M)
    source = re.sub(r'^\s*last_election\s*=\s*"1930\.11\.9"\s*\n', '', source, flags=re.M)
    current = (MOD / row['country_history']).read_text(encoding='utf-8-sig')
    begin, end = '# BEGIN ECONOMY V2 NEW CAMPAIGN', '# END ECONOMY V2 NEW CAMPAIGN'
    if begin in current:
        foreign = current[current.index(begin):current.index(end) + len(end)]
        if current.count(begin) != 1 or current.count(end) != 1 or parse(foreign) != [['set_country_flag', '=', 'ac_macro_history_eligible']]:
            raise ValueError('Unexpected fiscal history marker: ' + tag)
        if begin not in source:
            anchor = '# BEGIN EXPANSION START LEADER'
            source = source.replace(anchor, foreign + '\n\n' + anchor, 1) if anchor in source else source.rstrip() + '\n\n' + foreign + '\n'
    prefix = NOTE + '# BEGIN ACTIVE WORLD UNLOCKS\n'
    # Unlock before any inherited variant declarations or OOB references.
    for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
        limits = ('has_dlc = "By Blood Alone"' if bba else 'NOT = { has_dlc = "By Blood Alone" }')
        limits += '\n' + ('has_dlc = "Man the Guns"' if mtg else 'NOT = { has_dlc = "Man the Guns" }')
        def tech_block(nsb=False):
            tech = technologies(profile, engine, bba, mtg, nsb) if engine else row['starting_tech'][case_key(bba, mtg, nsb)]
            return block('set_technology', '\n'.join(key + ' = 1' for key in tech))
        contents = tech_block()
        if set(profile['production']) & set(ARMOR):
            contents = block('if', 'limit = { has_dlc = "No Step Back" }\n' + tech_block(True) + block('else', contents))
        prefix += block('if', block('limit', limits) + contents)
    prefix += '# END ACTIVE WORLD UNLOCKS\n\n'
    body = f'set_country_flag = {tag}_ws_foundation\nset_convoys = {profile["convoys"]}\nstarting_train_buffer = 1\nset_fuel_ratio = 1.0\n'
    if not any(k == 'set_grand_doctrine' for k, _, _ in parse(source)):
        body += 'set_grand_doctrine = new_superior_firepower\nset_grand_doctrine = new_fleet_in_being\nset_grand_doctrine = new_operational_integrity\n'
    armour_roles = sorted(set(profile['production']) & set(ARMOR))
    if armour_roles:
        modern = ''.join(variant(tag, ARMOR[role]) for role in armour_roles)
        legacy = ''
        for role in armour_roles:
            count = profile['stocks'][role]
            modern += block('add_equipment_to_stockpile', f'type = {ARMOR[role]["modern"]}\namount = {count}\nproducer = {tag}\nvariant_name = "{tag} {ARMOR[role]["label"]}"')
            legacy += block('add_equipment_to_stockpile', f'type = {role}\namount = {count}\nproducer = {tag}')
        body += block('if', 'limit = { has_dlc = "No Step Back" }\n' + modern + block('else', legacy))
    modern = ''.join(variant(tag, AIR[role]) for role, count in profile['air'].items() if count)
    for role, count in profile['air_reserves'].items():
        modern += block('add_equipment_to_stockpile', f'type = {AIR[role]["modern"]}\namount = {count}\nproducer = {tag}\nvariant_name = "{tag} {AIR[role]["label"]}"')
    if profile['air'] or any(r in AIR for r in profile['production']):
        modern += f'set_air_oob = "{tag}_ws_air_bba"\n'
    legacy = ''.join(block('add_equipment_to_stockpile', f'type = {AIR[role]["legacy"]}\namount = {count}\nproducer = {tag}') for role, count in profile['air_reserves'].items())
    if profile['air'] or any(r in AIR for r in profile['production']):
        legacy += f'set_air_oob = "{tag}_ws_air"\n'
        body += block('if', 'limit = { has_dlc = "By Blood Alone" }\n' + modern + block('else', legacy))
    modern = ''.join(variant(tag, NAVY[role]) for role, count in profile['navy'].items() if count)
    if profile['navy'] or profile['naval_production']:
        modern += f'set_naval_oob = "{tag}_ws_navy_mtg"\n'
        body += block('if', 'limit = { has_dlc = "Man the Guns" }\n' + modern + block('else', f'set_naval_oob = "{tag}_ws_navy"'))
    body += f'set_oob = "{tag}_ws_land"\n'
    body += ''.join(block('add_equipment_to_stockpile', f'type = {kind}\namount = {count}\nproducer = {tag}') for kind, count in profile['stocks'].items() if kind not in armour_roles)
    return prefix + source.rstrip() + '\n\n' + MARKER + '\n' + NOTE + body + END + '\n'


def land_output(tag, row, profile):
    def lines():
        text = ''.join(production(tag, kind, count) for kind, count in profile['production'].items() if kind not in AIR and kind not in ARMOR)
        roles = sorted(set(profile['production']) & set(ARMOR))
        if roles:
            modern = ''.join(production(tag, role, profile['production'][role], nsb=True) for role in roles)
            legacy = ''.join(production(tag, role, profile['production'][role]) for role in roles)
            text += block('if', 'limit = { has_dlc = "No Step Back" }\n' + modern + block('else', legacy))
        return text
    if profile['mode'] == 'retained_start':
        tree = retained_tree({**row, 'tag': tag})
        tree = [node for node in tree if node[0] != 'instant_effect']
        return NOTE + render(tree) + '\n' + block('instant_effect', lines())
    templates = ''; divisions = ''; index = 0
    for role, amount in profile['formations'].items():
        if not amount:
            continue
        units = (['modern_armor'] * 3 + ['motorized'] * 3) if role == 'armor' else [LAND[role]] * profile['infantry_battalions']
        regiments = '\n'.join(f'{kind} = {{ x = {n // 3} y = {n % 3} }}' for n, kind in enumerate(units))
        support = '\n'.join(f'{kind} = {{ x = 0 y = {n} }}' for n, kind in enumerate(supports(profile)))
        if role != 'infantry':
            support += '\nlogistics_company = { x = 0 y = 2 }'
        name = tag + ' ' + role.title() + ' Formation'
        templates += block('division_template', f'name = "{name}"\ndivision_names_group = {tag}_WS_{role.upper()}\n' + block('regiments', regiments) + (block('support', support) if support else ''))
        for n in range(amount):
            location = row['land_deployments'][index]; index += 1
            divisions += block('division', f'name = "{tag} {role.title()} Formation {n + 1}"\nlocation = {location}\ndivision_template = "{name}"\nstart_experience_factor = 0.2\nstart_equipment_factor = 1.0')
    return NOTE + templates + block('units', divisions) + block('instant_effect', lines())


def air_output(tag, row, profile, bba):
    states = ''
    for deployment in row['air_deployments']:
        wings = ''
        for role in profile['air']:
            count = deployment[role]
            if not count:
                continue
            detail = f'owner = {tag}\ncreator = {tag}\namount = {count}'
            if bba:
                detail += '\nversion_name = "' + tag + ' ' + AIR[role]['label'] + '"'
            wings += block(equipment_for(role, bba, False), detail)
        states += block(str(deployment['state']), wings)
    lines = ''.join(production(tag, role, count, bba=bba) for role, count in profile['production'].items() if role in AIR)
    return NOTE + block('air_wings', states) + block('instant_effect', lines)


def navy_output(tag, row, profile, mtg):
    tasks = ''; base = row.get('naval_base')
    for role, count in profile['navy'].items():
        ships = ''
        for n in range(count):
            details = f'amount = 1\nowner = {tag}'
            if mtg:
                details += '\nversion_name = "' + tag + ' ' + NAVY[role]['label'] + '"'
            ships += block('ship', f'name = "{tag} {NAVY[role]["label"]} {n + 1}"\ndefinition = {role}\n' + block('equipment', block(equipment_for(role, False, mtg), details)))
        tasks += block('task_force', f'name = "{tag} {role.title()} Service"\nlocation = {base}\n' + ships)
    fleet = block('fleet', f'name = "{tag} Maritime Service"\nnaval_base = {base}\n' + tasks) if tasks else ''
    lines = ''.join(production(tag, role, count, mtg=mtg) for role, count in profile['naval_production'].items())
    return NOTE + (block('units', fleet) if fleet else '') + block('instant_effect', lines)


def ai_output(tag, row, profile):
    allowed = f'allowed = {{ tag = {tag} original_tag = {tag} }}\n'
    base = allowed + f'enable = {{ has_country_flag = {tag}_ws_foundation has_capitulated = no }}\nabort_when_not_enabled = yes\n'
    for role, value in [('infantry', -80), ('armor', -2), ('mountaineers', -4)]:
        base += block('ai_strategy', f'type = role_ratio\nid = {role}\nvalue = {value}')
    total = sum(profile['formations'].values())
    for plan in template_plans(tag, row, profile):
        role, count = plan['role'], plan['count']
        if count:
            base += block('ai_strategy', f'type = role_ratio\nid = {tag}_ws_{role}\nvalue = {round(100 * count / total)}')
    priorities = [('equipment_production_factor', 'infantry', 20), ('build_building', 'infrastructure', 10), ('build_building', 'industrial_complex', 20)]
    if 'fighter' in profile['air']: priorities.append(('unit_ratio', 'fighter', 15))
    if 'convoy' in profile['naval_production']: priorities.append(('unit_ratio', 'convoy', 15))
    if 'destroyer' in profile['navy']: priorities.append(('unit_ratio', 'screen_ship', 10))
    if supports(profile): priorities.append(('equipment_production_factor', 'support', 15))
    for kind, ident, value in priorities:
        base += block('ai_strategy', f'type = {kind}\nid = {ident}\nvalue = {value}')
    peace = allowed + f'enable = {{ has_country_flag = {tag}_ws_foundation has_war = no }}\nabort_when_not_enabled = yes\n'
    peace += block('ai_strategy', f'type = ai_wanted_divisions_factor\nvalue = {-30 if tag == "YUK" else -60}')
    war = allowed + f'enable = {{ has_country_flag = {tag}_ws_foundation has_war = yes }}\nabort_when_not_enabled = yes\n'
    war += block('ai_strategy', 'type = ai_wanted_divisions_factor\nvalue = -15')
    return NOTE + block(tag + '_ws_sustainment', base) + block(tag + '_ws_peace', peace) + block(tag + '_ws_defense', war)


def outputs(reference=None):
    manifest = json.loads((HERE / 'foundation.json').read_text()); profiles = json.loads((HERE / 'profiles.json').read_text())['countries']; engine = Engine(reference) if reference else None
    out = {}; labels = []; research_loc = []
    for tag, row in manifest['countries'].items():
        profile = profiles[tag]
        for ident, cfg in row['placements'].items():
            out[row['baseline'][ident]['path']] = state_output(row, ident, cfg)
        for p in row['new_victory_points']:
            labels.append(f' VICTORY_POINTS_{p}:0 "{profile["name"]} ' + ('Capital Centre' if int(p) == row['capital_province'] else 'Logistics Centre ' + p) + '"')
        out[row['country_history']] = country_output(tag, row, profile, engine)
        out[f'history/units/{tag}_ws_land.txt'] = land_output(tag, row, profile)
        if profile['air'] or any(r in AIR for r in profile['production']):
            for bba in (False, True):
                out[f'history/units/{tag}_ws_air' + ('_bba' if bba else '') + '.txt'] = air_output(tag, row, profile, bba)
        if profile['navy'] or profile['naval_production']:
            for mtg in (False, True):
                out[f'history/units/{tag}_ws_navy' + ('_mtg' if mtg else '') + '.txt'] = navy_output(tag, row, profile, mtg)
        names = ''; templates = ''
        for plan in template_plans(tag, row, profile):
            role = plan['role']
            if profile['mode'] != 'retained_start':
                names += block(tag + '_WS_' + role.upper(), f'name = "{role.title()} Formation"\nfor_countries = {{ {tag} }}\ncan_use = {{ always = yes }}\ndivision_types = {{ "{LAND[role]}" }}\nfallback_name = "%d {role.title()} Formation"')
            regiments = '\n'.join(f'{kind} = {count}' for kind, count in plan['regiments'].items())
            support = '\n'.join(f'{kind} = {count}' for kind, count in plan['support'].items())
            target = block(tag + '_ws_' + role + '_target', 'upgrade_prio = { factor = 1 }\n' + block('target_template', block('regiments', regiments) + (block('support', support) if support else '')))
            templates += block(tag + '_ws_' + role, f'available_for = {{ {tag} }}\nrole = {tag}_ws_{role}\nupgrade_prio = {{ factor = 5 }}\n' + target)
        if profile['mode'] == 'retained_start' and tag == 'PBL':
            for n, (key, _, values) in enumerate(retained_tree(row)):
                if key != 'division_template': continue
                label = get(values, 'name').strip('"')
                names += block(f'PBL_WS_RETAINED_{n}', f'name = "{label}"\nfor_countries = {{ PBL }}\ncan_use = {{ always = yes }}\ndivision_types = {{ ' + ' '.join('"' + unit + '"' for unit in dict((k, None) for k, _, _ in get(values, 'regiments'))) + f' }}\nfallback_name = "%d {label}"')
        if names: out[f'common/units/names_divisions/{tag}_world_start.txt'] = NOTE + names
        out[f'common/ai_templates/{tag}_world_start.txt'] = NOTE + templates
        out[f'common/ai_strategy/{tag}_world_start.txt'] = ai_output(tag, row, profile)
        research = f'name = {tag}_ws_research_name\ndesc = {tag}_ws_research_desc\nallowed = {{ tag = {tag} original_tag = {tag} }}\nenable = {{ has_country_flag = {tag}_ws_foundation }}\nabort_when_not_enabled = yes\n'
        fields = 'industry = 15\ninfantry_tech = 15\nsupport_tech = 12\nelectronics = 5'
        if profile['air']: fields += '\nlight_fighter = 12'
        if profile['navy']: fields += '\ndd_tech = 5'
        if any(role in profile['production'] for role in ARMOR): fields += '\narmor = 10'
        if 'mechanized_equipment_1' in profile['production']: fields += '\ncat_mechanized_equipment = 8'
        research += block('research', fields) + 'weight = { factor = 1 }\n'
        out[f'common/ai_strategy_plans/{tag}_world_start.txt'] = NOTE + block(tag + '_ws_research', research)
        research_loc.extend([f' {tag}_ws_research_name:0 "{profile["name"]}: Physical Sustainment"', f' {tag}_ws_research_desc:0 "Maintain transport, equipment replacement and affordable service capacity. These starting priorities are provisional gameplay calibration."'])
    out.update(compose(ROOT, MOD, owner='world_starts'))
    from armor import outputs as armor_outputs
    out.update(armor_outputs())
    out['localisation/english/replace/ac_world_start_hubs_l_english.yml'] = '\ufeffl_english:\n' + '\n'.join(labels) + '\n'
    out['localisation/english/ac_world_starts_l_english.yml'] = '\ufeffl_english:\n' + '\n'.join(research_loc) + '\n'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--reference', type=Path); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    failures = []
    for relative, text in outputs(args.reference).items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8', newline='\n')
    if failures:
        raise SystemExit('Active-world output differs: ' + ', '.join(failures))
    print('Active-world reviewed start outputs ' + ('consistent' if args.check else 'generated'))
