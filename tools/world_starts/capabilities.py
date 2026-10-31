"""Technical capability recipes, not named canonical1991 service equipment."""

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


def equipment_for(role, bba, mtg):
    if role in AIR:
        return AIR[role]['modern' if bba else 'legacy']
    if role in NAVY:
        return NAVY[role]['modern' if mtg else 'legacy']
    return 'convoy_1' if role == 'convoy' else role


def design_for(role, bba, mtg):
    if role in AIR and bba:
        return AIR[role]
    if role in NAVY and mtg:
        return NAVY[role]
    return None


def supports(profile):
    """Only equip support companies that the standing replacement plan owns."""
    result = []
    if profile['production'].get('support_equipment_1'):
        result.append('engineer')
    if profile['production'].get('artillery_equipment_1'):
        result.append('artillery')
    return result
