"""Narrow NSB history unlocks, not a restoration of the disabled armor tree.

Definitions and module slots are selected from installed1.19.4.1 technical data.
All recipes are provisional service-role calibration, not canonical vehicles.
The three otherwise unresearchable bridge technologies are granted only when
the new-country history actually fields that role with No Step Back enabled.
"""
from pathlib import Path

ARMOR = {
    'modern_tank_equipment_1': dict(modern='modern_tank_chassis_1', legacy='modern_tank_equipment_1',
        label='Service Armour', technology='ac_ws_nsb_modern_support', subunit='modern_armor', modules={
            'turret_type_slot': 'tank_modern_tank_turret', 'main_armament_slot': 'tank_medium_cannon_2',
            'suspension_type_slot': 'tank_torsion_bar_suspension', 'armor_type_slot': 'tank_welded_armor',
            'engine_type_slot': 'tank_diesel_engine'}),
    'light_tank_equipment_1': dict(modern='light_tank_chassis_1', legacy='light_tank_equipment_1',
        label='Light Service Armour', technology='ac_ws_nsb_light_support', subunit='light_armor', modules={
            'turret_type_slot': 'tank_light_one_man_tank_turret', 'main_armament_slot': 'tank_small_cannon',
            'suspension_type_slot': 'tank_bogie_suspension', 'armor_type_slot': 'tank_riveted_armor',
            'engine_type_slot': 'tank_gasoline_engine'}),
    'medium_tank_artillery_equipment_1': dict(modern='medium_tank_artillery_chassis_1', legacy='medium_tank_artillery_equipment_1',
        label='Tracked Service Artillery', technology='ac_ws_nsb_artillery_support', subunit='medium_sp_artillery_brigade', modules={
            'turret_type_slot': 'tank_medium_fixed_superstructure_turret', 'main_armament_slot': 'tank_medium_howitzer',
            'suspension_type_slot': 'tank_bogie_suspension', 'armor_type_slot': 'tank_riveted_armor',
            'engine_type_slot': 'tank_gasoline_engine'}),
}


def outputs():
    from compile import block
    text = '# Provisional service-role compatibility; tools/world_starts/armor.py.\n'
    loc = '\ufeffl_english:\n'
    for role, design in ARMOR.items():
        body = 'research_cost = 1\nstart_year = 1991\nallow = { always = no }\n'
        body += block('enable_equipments', design['modern'])
        body += block('enable_equipment_modules', '\n'.join(design['modules'].values()))
        body += block('enable_subunits', design['subunit'])
        text += block(design['technology'], body)
        loc += f' {design["technology"]}:0 "{design["label"]} Baseline"\n {design["technology"]}_desc:0 "A technical compatibility baseline for the starting service role. Provisional gameplay calibration."\n'
    return {'common/technologies/ac_ws_armour_support.txt': block('technologies', text),
            'localisation/english/ac_ws_armour_support_l_english.yml': loc}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2] / 'mod/2985041246'
    for relative, text in outputs().items():
        (root / relative).write_text(text, encoding='utf-8', newline='\n')
