"""Technical capability recipes, not named canonical1991 service equipment."""
from armor import ARMOR

AIR = {
    'fighter': dict(modern='small_plane_airframe_1', legacy='fighter_equipment_1', label='Service Fighter',
                    modules={'fixed_main_weapon_slot': 'light_mg_4x', 'engine_type_slot': 'engine_2_1x'}),
    'cas': dict(modern='small_plane_cas_airframe_1', legacy='CAS_equipment_1', label='Service Support',
                modules={'fixed_main_weapon_slot': 'bomb_locks', 'engine_type_slot': 'engine_2_1x'}),
    'tactical': dict(modern='medium_plane_airframe_1', legacy='tac_bomber_equipment_1', label='Service Bomber',
                     modules={'fixed_main_weapon_slot': 'medium_bomb_bay', 'engine_type_slot': 'engine_2_2x'}),
}
NAVY = {
    'destroyer': dict(modern='ship_hull_light_2', legacy='destroyer_2', label='Coastal Escort', modules={
        'fixed_ship_battery_slot': 'ship_light_battery_1', 'fixed_ship_anti_air_slot': 'ship_anti_air_1',
        'fixed_ship_fire_control_system_slot': 'ship_fire_control_system_0', 'fixed_ship_engine_slot': 'light_ship_engine_2',
        'fixed_ship_torpedo_slot': 'ship_torpedo_1', 'rear_1_custom_slot': 'ship_depth_charge_1'}),
    'submarine': dict(modern='ship_hull_submarine_2', legacy='submarine_2', label='Coastal Submarine', modules={
        'fixed_ship_torpedo_slot': 'ship_torpedo_sub_1', 'fixed_ship_engine_slot': 'sub_ship_engine_2'}),
    'light_cruiser': dict(modern='ship_hull_cruiser_2', legacy='light_cruiser_2', label='Patrol Cruiser', modules={
        'fixed_ship_battery_slot': 'ship_light_medium_battery_1', 'fixed_ship_anti_air_slot': 'ship_anti_air_1',
        'fixed_ship_fire_control_system_slot': 'ship_fire_control_system_0', 'fixed_ship_engine_slot': 'cruiser_ship_engine_2',
        'fixed_ship_armor_slot': 'ship_armor_cruiser_2', 'fixed_ship_secondaries_slot': 'ship_secondaries_1',
        'mid_1_custom_slot': 'ship_torpedo_1'}),
    'heavy_cruiser': dict(modern='ship_hull_cruiser_2', legacy='heavy_cruiser_2', label='Heavy Patrol Cruiser', modules={
        'fixed_ship_battery_slot': 'ship_medium_battery_1', 'fixed_ship_anti_air_slot': 'ship_anti_air_1',
        'fixed_ship_fire_control_system_slot': 'ship_fire_control_system_0', 'fixed_ship_engine_slot': 'cruiser_ship_engine_2',
        'fixed_ship_armor_slot': 'ship_armor_cruiser_2', 'fixed_ship_secondaries_slot': 'ship_secondaries_1',
        'mid_1_custom_slot': 'ship_torpedo_1'}),
}
LAND = {'infantry': 'infantry', 'motorized': 'motorized', 'mechanized': 'mechanized', 'armor': 'modern_armor'}
COMMON_TECH = ['infantry_weapons', 'infantry_weapons1', 'tech_support', 'tech_engineers', 'tech_recon',
               'basic_train', 'motorised_infantry', 'gw_artillery', 'basic_machine_tools', 'construction1',
               'electronic_mechanical_engineering', 'fuel_silos', 'fuel_refining']


def equipment_for(role, bba, mtg, nsb=False):
    if role in ARMOR and nsb:
        return ARMOR[role]['modern']
    if role in AIR:
        return AIR[role]['modern' if bba else 'legacy']
    if role in NAVY:
        return NAVY[role]['modern' if mtg else 'legacy']
    return 'convoy_1' if role == 'convoy' else role


def design_for(role, bba, mtg, nsb=False):
    if role in ARMOR and nsb:
        return ARMOR[role]
    if role in AIR and bba:
        return AIR[role]
    if role in NAVY and mtg:
        return NAVY[role]
    return None


def dlc_cases(profile):
    from itertools import product
    for bba, mtg in product((False, True), repeat=2):
        yield bba, mtg, False
        if set(profile['production']) & set(ARMOR): yield bba, mtg, True


def case_key(bba, mtg, nsb=False):
    return f'bba{int(bba)}_mtg{int(mtg)}' + ('_nsb1' if nsb else '')


def supports(profile):
    """Only equip support companies that the standing replacement plan owns."""
    result = []
    if profile['production'].get('support_equipment_1'):
        result.append('engineer')
    if profile['production'].get('artillery_equipment_1'):
        result.append('artillery')
    return result


def retained_tree(row):
    """Preserve inherited armies; apply only ledgered validity corrections."""
    from script import parse, get, setv
    tree = parse(row['retained_land_source'])
    if row['tag'] == 'PBL':
        for key, _, body in tree:
            if key != 'division_template': continue
            support = get(body, 'support', [])
            invalid = [n for n in support if n[0] == 'medium_sp_artillery']
            if invalid:
                if len(invalid) != 1 or get(body, 'name') not in ('"Heavy Infantry"', '"Mechanized Brigade"'):
                    raise ValueError('Unexpected inherited SPG correction scope')
                support.remove(invalid[0])
                get(body, 'regiments').append(['medium_sp_artillery_brigade', '=', [['x', '=', '2'], ['y', '=', '0']]])
        for n, (key, _, body) in enumerate(tree):
            if key == 'division_template':
                setv(body, 'division_names_group', f'PBL_WS_RETAINED_{n}')
    return tree


def divisions(tree):
    """Repeated units blocks are cumulative, as in the inherited PBL roster."""
    return [body for key, _, group in tree if key == 'units' for kind, _, body in group if kind == 'division']


def template_plans(tag, row, profile):
    from collections import Counter
    from script import get
    if profile['mode'] == 'retained_start':
        tree = retained_tree({**row, 'tag': tag})
        counts = Counter(get(body, 'division_template') for body in divisions(tree))
        return [dict(role=f'retained_{n}', name=get(body, 'name').strip('"'), count=counts[get(body, 'name')],
                     regiments=Counter(k for k, _, _ in get(body, 'regiments', [])),
                     support=Counter(k for k, _, _ in get(body, 'support', [])))
                for n, (key, _, body) in enumerate(tree) if key == 'division_template' and counts[get(body, 'name')]]
    return [dict(role=role, name=f'{tag} {role.title()} Formation', count=count,
                 regiments=Counter({'modern_armor': 3, 'motorized': 3} if role == 'armor' else {LAND[role]: profile['infantry_battalions']}),
                 support=Counter(supports(profile) + (['logistics_company'] if role != 'infantry' else [])))
            for role, count in profile['formations'].items() if count]
