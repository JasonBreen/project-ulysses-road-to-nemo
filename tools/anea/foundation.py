"""Reproducible new-campaign foundation for EMM/EVA; --check is read-only.

Inputs: foundation.json, inherited state/country data and native equipment IDs.
Country history only applies its rosters/industry on a new game. No startup
effect injects old-save armies, factories, technology, manpower or resources.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get, setv, render

NOTE = '# Anea foundation: provisional gameplay; source/placements in tools/anea/foundation.json.\n'
ARMY = [('infantry', 'Territorial Infantry', 8, 10), ('motorized', 'Mobile Infantry', 2, 2), ('mechanized', 'Mechanized Reserve', 2, 2)]
COUNTRY = {'EMM': 'Emmeria', 'EVA': 'Estovakia'}


def block(k, text):
    return k + ' = {\n' + '\n'.join('\t' + s for s in text.splitlines()) + '\n}\n'


def state_output(path, config, hubs, capital_province):
    tree = parse(path.read_text(encoding='utf-8-sig')); state = get(tree, 'state')
    hist = get(state, 'history'); buildings = get(hist, 'buildings')
    for k, v in [('infrastructure', config['infrastructure']), ('industrial_complex', config['civilian']), ('arms_factory', config['military']), ('dockyard', config['dockyard']), ('air_base', config['air_base']), ('fuel_silo', config['fuel_silo'])]:
        setv(buildings, k, str(v))
    for province, level in config['naval_bases'].items():
        existing = get(buildings, province, [])
        setv(existing, 'naval_base', str(level)); setv(buildings, province, existing)
    for province in hubs:
        if province in [int(k) for k, _, _ in get(state, 'provinces')]:
            existing = get(buildings, str(province), [])
            setv(existing, 'supply_node', '1'); setv(buildings, str(province), existing)
    # A state capital needs an unambiguous province to originate supply.
    # Make that province the state's highest VP and attach the hub there.
    # Other hub VPs are neutral numbered logistics centres, not canon cities.
    hist[:] = [n for n in hist if n[0] != 'victory_points' or not any(int(k) in hubs for k, _, _ in n[2] if k.isdigit())]
    for province in hubs:
        if province in [int(k) for k, _, _ in get(state, 'provinces')]:
            hist.append(['victory_points', '=', [[str(province), None, None], ['20' if province == capital_province else '5', None, None]]])
    resources = get(state, 'resources', [])
    for resource, amount in config['resources'].items():
        setv(resources, resource, str(amount))
    slots = config['civilian'] + config['military'] + config['dockyard']
    if slots > 6: setv(state, 'state_category', 'large_city')
    elif slots > 4: setv(state, 'state_category', 'city')
    setv(state, 'buildings_max_level_factor', '1.000')
    return NOTE + render(tree) + '\n'


def template(tag, unit, title):
    regiments = '\n'.join(f'{unit} = {{ x = {x} y = {y} }}' for x in range(3) for y in range(2))
    support = 'engineer = { x = 0 y = 0 }\nartillery = { x = 0 y = 1 }\nlogistics_company = { x = 0 y = 2 }'
    if unit != 'infantry': support += '\nmot_recon = { x = 0 y = 3 }'
    return block('division_template', f'name = "{tag} {title}"\ndivision_names_group = {tag}_AN_{unit.upper()}\n' + block('regiments', regiments) + block('support', support))


def land_oob(tag, row):
    divisions = []; equipment_factory = [('infantry_equipment_1', 5 if tag == 'EMM' else 6), ('motorized_equipment_1', 3), ('support_equipment_1', 2), ('artillery_equipment_1', 2), ('mechanized_equipment_1', 1)]
    # Reserve one/two factories for the separate air branch. Total exactly MIL.
    deployment = row['supply_hubs']
    for unit, title, emm, eva in ARMY:
        for n in range(emm if tag == 'EMM' else eva):
            divisions.append(block('division', f'name = "{n + 1} {title} Division"\nlocation = {deployment[n % len(deployment)]}\ndivision_template = "{tag} {title}"\nstart_experience_factor = 0.25\nstart_equipment_factor = 1.0'))
    production = []
    for equipment, factories in equipment_factory:
        production.append(block('add_equipment_production', block('equipment', f'type = {equipment}\ncreator = {tag}') + f'requested_factories = {factories}\nprogress = 0.25\nefficiency = 50'))
    return NOTE + ''.join(template(tag, u, t) for u, t, _, _ in ARMY) + block('units', ''.join(divisions)) + block('instant_effect', ''.join(production))


def air_oob(tag, row, dlc):
    wings = []
    fighter_total = 160 if tag == 'EMM' else 180
    for n, state in enumerate(row['air_states']):
        fighter = 'small_plane_airframe_1' if dlc else 'fighter_equipment_1'
        cas = 'small_plane_cas_airframe_1' if dlc else 'CAS_equipment_1'
        equipment = fighter if n < 2 else cas
        amount = fighter_total // 2 if n < 2 else 60
        variant = f'\nversion_name = "{tag} Service ' + ('Fighter' if n < 2 else 'Strike') + '"' if dlc else ''
        wings.append(block(str(state), block(equipment, f'owner = {tag}\ncreator = {tag}\namount = {amount}' + variant)))
    # Land roster consumes thirteen/fourteen factories respectively.
    factories = 1 if tag == 'EMM' else 2
    variant = f'\nversion_name = "{tag} Service Fighter"' if dlc else ''
    fighter = 'small_plane_airframe_1' if dlc else 'fighter_equipment_1'
    production = block('add_equipment_production', block('equipment', f'type = {fighter}\ncreator = {tag}' + variant) + f'requested_factories = {factories}\nprogress = 0.25\nefficiency = 50')
    return NOTE + block('air_wings', ''.join(wings)) + block('instant_effect', production)


def navy_oob(tag, row, dlc):
    ships = []
    counts = [('light_cruiser', 1), ('destroyer', 6 if tag == 'EMM' else 4), ('submarine', 2 if tag == 'EMM' else 3)]
    classes = {'light_cruiser': ('ship_hull_cruiser_2', 'light_cruiser_2', 'Patrol Cruiser'), 'destroyer': ('ship_hull_light_2', 'destroyer_2', 'Escort'), 'submarine': ('ship_hull_submarine_2', 'submarine_2', 'Coastal Submarine')}
    port = row['ports'][0]['province']
    for kind, count in counts:
        hull, legacy, title = classes[kind]
        for n in range(count):
            variant = f'\nversion_name = "{tag} {title}"' if dlc else ''
            eq = block(hull if dlc else legacy, f'amount = 1\nowner = {tag}' + variant)
            ships.append(block('ship', f'name = "{tag} {title} {n + 1}"\ndefinition = {kind}\n' + block('equipment', eq)))
    taskforce = block('task_force', f'name = "{tag} Coastal Task Force"\nlocation = {port}\n' + ''.join(ships))
    fleet = block('fleet', f'name = "{tag} Home Fleet"\nnaval_base = {port}\n' + taskforce)
    convoy = block('add_equipment_production', block('equipment', f'type = convoy_1\ncreator = {tag}') + f'requested_factories = {6 if tag == "EMM" else 4}\nprogress = 0.25\nefficiency = 50')
    return NOTE + block('units', fleet) + block('instant_effect', convoy)


def variant(name, kind, modules):
    return block('create_equipment_variant', f'name = "{name}"\ntype = {kind}\n' + block('modules', '\n'.join(f'{k} = {v}' for k, v in modules.items())))


def country_output(tag, row):
    # The political office and democratic group are inherited; no individual,
    # election date, historical term, or biography is invented.
    common = ['infantry_weapons', 'infantry_weapons1', 'tech_support', 'tech_engineers', 'tech_recon', 'tech_logistics_company', 'motorised_infantry', 'mechanised_infantry', 'gw_artillery', 'interwar_antiair', 'basic_train', 'basic_machine_tools', 'construction1', 'electronic_mechanical_engineering', 'fuel_silos', 'fuel_refining']
    text = NOTE + f'capital = {row["capital"]}\nset_research_slots = 3\nset_convoys = 120\nstarting_train_buffer = 2\nset_fuel_ratio = 1.0\n'
    text += block('set_politics', 'ruling_party = democratic\nelections_allowed = no')
    text += block('set_popularities', 'democratic = 60\nneutrality = 25\nfascism = 10\ncommunism = 5' if tag == 'EMM' else 'democratic = 40\nneutrality = 45\nfascism = 10\ncommunism = 5')
    text += f'set_stability = {0.65 if tag == "EMM" else 0.5}\nset_war_support = {0.35 if tag == "EMM" else 0.45}\n'
    text += block('add_ideas', 'volunteer_only\ncivilian_economy\nlimited_exports')
    text += block('set_technology', '\n'.join(k + ' = 1' for k in common))
    text += 'set_grand_doctrine = new_superior_firepower\nset_grand_doctrine = new_fleet_in_being\nset_grand_doctrine = new_operational_integrity\n'
    airtechs = 'aa_lmg = 1\nearly_bombs = 1\naircraft_construction = 1\nengines_1 = 1\nengines_2 = 1\niw_small_airframe = 1\nbasic_small_airframe = 1'
    air = block('set_technology', airtechs)
    air += variant(tag + ' Service Fighter', 'small_plane_airframe_1', {'fixed_main_weapon_slot': 'light_mg_4x', 'engine_type_slot': 'engine_2_1x'})
    air += variant(tag + ' Service Strike', 'small_plane_cas_airframe_1', {'fixed_main_weapon_slot': 'bomb_locks', 'engine_type_slot': 'engine_2_1x'})
    for kind, name in [('small_plane_airframe_1', 'Service Fighter'), ('small_plane_cas_airframe_1', 'Service Strike')]:
        air += block('add_equipment_to_stockpile', f'type = {kind}\namount = 30\nproducer = {tag}\nvariant_name = "{tag} {name}"')
    air += f'set_air_oob = "{tag}_anea_air_bba"\n'
    legacy_air = block('set_technology', 'early_fighter = 1\nfighter1 = 1\nCAS1 = 1')
    for kind in ('fighter_equipment_1', 'CAS_equipment_1'):
        legacy_air += block('add_equipment_to_stockpile', f'type = {kind}\namount = 30\nproducer = {tag}')
    legacy_air += f'set_air_oob = "{tag}_anea_air"\n'
    text += block('if', 'limit = { has_dlc = "By Blood Alone" }\n' + air + block('else', legacy_air))
    navaltechs = ['early_ship_hull_light', 'basic_ship_hull_light', 'early_ship_hull_submarine', 'basic_ship_hull_submarine', 'early_ship_hull_cruiser', 'basic_ship_hull_cruiser', 'basic_battery', 'basic_torpedo', 'basic_depth_charges', 'basic_cruiser_armor_scheme', 'mtg_transport']
    navy = block('set_technology', '\n'.join(k + ' = 1' for k in navaltechs))
    navy += variant(tag + ' Escort', 'ship_hull_light_2', {'fixed_ship_battery_slot': 'ship_light_battery_1', 'fixed_ship_anti_air_slot': 'ship_anti_air_1', 'fixed_ship_fire_control_system_slot': 'ship_fire_control_system_0', 'fixed_ship_engine_slot': 'light_ship_engine_2', 'fixed_ship_torpedo_slot': 'ship_torpedo_1', 'rear_1_custom_slot': 'ship_depth_charge_1'})
    navy += variant(tag + ' Patrol Cruiser', 'ship_hull_cruiser_2', {'fixed_ship_battery_slot': 'ship_light_medium_battery_1', 'fixed_ship_anti_air_slot': 'ship_anti_air_1', 'fixed_ship_fire_control_system_slot': 'ship_fire_control_system_0', 'fixed_ship_engine_slot': 'cruiser_ship_engine_2', 'fixed_ship_armor_slot': 'ship_armor_cruiser_2', 'fixed_ship_secondaries_slot': 'ship_secondaries_1', 'mid_1_custom_slot': 'ship_torpedo_1'})
    navy += variant(tag + ' Coastal Submarine', 'ship_hull_submarine_2', {'fixed_ship_torpedo_slot': 'ship_torpedo_sub_1', 'fixed_ship_engine_slot': 'sub_ship_engine_2'})
    navy += f'set_naval_oob = "{tag}_anea_navy_mtg"\n'
    legacy_navy = block('set_technology', 'early_destroyer = 1\nbasic_destroyer = 1\nearly_light_cruiser = 1\nbasic_light_cruiser = 1\nearly_submarine = 1\nbasic_submarine = 1\ntransport = 1') + f'set_naval_oob = "{tag}_anea_navy"\n'
    text += block('if', 'limit = { has_dlc = "Man the Guns" }\n' + navy + block('else', legacy_navy))
    text += f'set_oob = "{tag}_anea_land"\n'
    for kind, amount in [('infantry_equipment_1', 5000), ('support_equipment_1', 1000), ('artillery_equipment_1', 600), ('motorized_equipment_1', 1500), ('mechanized_equipment_1', 600), ('train_equipment_1', 120)]:
        text += block('add_equipment_to_stockpile', f'type = {kind}\namount = {amount}\nproducer = {tag}')
    # Preserve the starting-government generator's ownership marker verbatim.
    text += '\n# BEGIN EXPANSION START LEADER\n# New campaigns only; provenance: tools/usea_expansion/leaders.json.\nrecruit_character = ' + tag + '_ac_government_office\n# END EXPANSION START LEADER\n'
    return text


def names_output(tag):
    out = NOTE
    for unit, title, _, _ in ARMY:
        out += block(tag + '_AN_' + unit.upper(), f'name = "{title} Division"\nfor_countries = {{ {tag} }}\ncan_use = {{ always = yes }}\ndivision_types = {{ "{unit}" }}\nfallback_name = "%d {title} Division"')
    return out


def ai_output(tag, row):
    # These are additive to the inherited generic ratios, not replacement
    # absolute targets. Avoid adding another unrestricted large-army policy.
    strategies = [('equipment_production_factor', 'infantry', 15), ('equipment_production_factor', 'support', 10), ('equipment_production_factor', 'motorized', 10), ('equipment_production_factor', 'fighter', 15), ('unit_ratio', 'convoy', 15), ('unit_ratio', 'submarine', -5), ('unit_ratio', 'capital_ship', -8)]
    peace = f'allowed = {{ original_tag = {tag} }}\nenable = {{ has_war = no }}\nabort_when_not_enabled = yes\n'
    for typ, ident, value in strategies:
        peace += block('ai_strategy', f'type = {typ}\nid = {ident}\nvalue = {value}')
    peace += block('ai_strategy', 'type = build_building\nid = industrial_complex\nvalue = 25')
    war = f'allowed = {{ original_tag = {tag} }}\nenable = {{ has_war = yes }}\nabort_when_not_enabled = yes\n'
    for typ, ident, value in [('equipment_production_factor', 'infantry', 30), ('equipment_production_factor', 'artillery', 15), ('unit_ratio', 'fighter', 20)]:
        war += block('ai_strategy', f'type = {typ}\nid = {ident}\nvalue = {value}')
    recovery = f'allowed = {{ original_tag = {tag} }}\nenable = {{ has_country_flag = ac_anea_crisis has_war = no }}\nabort_when_not_enabled = yes\n'
    for typ, ident, value in [('equipment_production_factor', 'support', 15), ('equipment_production_factor', 'motorized', 10)]:
        recovery += block('ai_strategy', f'type = {typ}\nid = {ident}\nvalue = {value}')
    for ident in row['industry_states'][:3]:
        recovery += block('ai_strategy', f'type = build_building\nid = infrastructure\ntarget = {ident}\nvalue = 25')
    return NOTE + block(tag + '_anea_peacetime', peace) + block(tag + '_anea_defense', war) + block(tag + '_anea_replacement', recovery)


def research_output(tag):
    body = f'name = {tag}_anea_research_name\ndesc = {tag}_anea_research_desc\nallowed = {{ original_tag = {tag} }}\nenable = {{ always = yes }}\nabort_when_not_enabled = yes\n'
    body += block('research', 'industry = 15\ninfantry_tech = 12\nsupport_tech = 10\nlight_fighter = 10\nelectronics = 6\nmotorized_equipment = 6\ndd_tech = 3')
    body += block('weight', 'factor = 1.0')
    return NOTE + block(tag + '_anea_research', body)


def outputs():
    manifest = json.loads((HERE / 'foundation.json').read_text())
    out = {}; loc = []; all_hubs = []; all_routes = []
    for tag, row in manifest['countries'].items():
        for ident, cfg in row['placements'].items():
            path = next((MOD / 'history/states').glob(ident + '-*.txt'))
            out[path.relative_to(MOD).as_posix()] = state_output(path, cfg, row['supply_hubs'], row['capital_province'])
            loc.append(f' STATE_{ident}:0 "{cfg["name"]}"')
        for province in row['supply_hubs']:
            label = ('Emmerian' if tag == 'EMM' else 'Estovakian') + (' Capital District' if province == row['capital_province'] else f' Logistics Centre {province}')
            loc.append(f' VICTORY_POINTS_{province}:0 "{label}"')
        out[f'history/countries/{tag} - {COUNTRY[tag]}.txt'] = country_output(tag, row)
        out[f'history/units/{tag}_anea_land.txt'] = land_oob(tag, row)
        for dlc in (False, True):
            out[f'history/units/{tag}_anea_air' + ('_bba' if dlc else '') + '.txt'] = air_oob(tag, row, dlc)
            out[f'history/units/{tag}_anea_navy' + ('_mtg' if dlc else '') + '.txt'] = navy_oob(tag, row, dlc)
        out[f'common/units/names_divisions/{tag}_anea.txt'] = names_output(tag)
        out[f'common/ai_strategy/{tag}_anea.txt'] = ai_output(tag, row)
        out[f'common/ai_strategy_plans/{tag}_anea_research.txt'] = research_output(tag)
        all_hubs.extend(row['supply_hubs']); all_routes.extend(row['routes'])
    # Shared numeric map files have explicit append owners. Preserve only
    # declared, validated foreign records while regenerating this family.
    sys.path.insert(0, str(ROOT / 'tools'))
    from shared_logistics import compose
    out.update(compose(ROOT, MOD, owner='anea'))
    out['localisation/english/replace/ac_anea_regions_l_english.yml'] = '\ufeffl_english:\n' + '\n'.join(loc) + '\n'
    out['localisation/english/ac_anea_foundation_l_english.yml'] = '\ufeffl_english:\n' + '\n'.join(f' {tag}_anea_research_name:0 "{COUNTRY[tag]}: Sustainment and Recovery"\n {tag}_anea_research_desc:0 "Maintain industry, defensive aviation, infantry equipment and logistics. These priorities are provisional campaign calibration."' for tag in COUNTRY) + '\n'
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    failures = []
    for relative, source in outputs().items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8').replace('\r\n', '\n') != source:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(source, encoding='utf-8', newline='\n')
    if failures: raise SystemExit('Foundation output differs: ' + ', '.join(failures))
    print('Anea new-campaign foundation: 76 states, 2 country histories, 10 OOBs; output ' + ('consistent' if args.check else 'generated'))


if __name__ == '__main__': main()
