"""The vetted vocabulary a bespoke spec may use.

Every modifier, building type and technology category here is already used by
shipped mod content (measured 6 November 2026), so the compiler never writes a
key the mod has not exercised. Ranges keep one idea from dominating a country.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'

# modifier -> largest absolute value one idea may carry
MODIFIERS = {
    'stability_factor': 0.10, 'political_power_gain': 0.30, 'political_power_factor': 0.15,
    'war_support_factor': 0.10, 'consumer_goods_factor': 0.10, 'research_speed_factor': 0.08,
    'production_factory_efficiency_gain_factor': 0.10, 'production_factory_max_efficiency_factor': 0.08,
    'production_speed_buildings_factor': 0.10, 'production_speed_infrastructure_factor': 0.20,
    'production_speed_industrial_complex_factor': 0.15, 'production_speed_arms_factory_factor': 0.15,
    'industrial_capacity_factory': 0.10, 'industrial_capacity_dockyard': 0.10, 'civilian_factory_use': 2,
    'army_org_factor': 0.10, 'army_core_defence_factor': 0.10, 'army_attack_factor': 0.08,
    'army_defence_factor': 0.08, 'army_speed_factor': 0.08, 'planning_speed': 0.15,
    'supply_consumption_factor': 0.10, 'repair_speed_factor': 0.15, 'training_time_factor': 0.15,
    'training_time_army_factor': 0.15, 'attrition': 0.10, 'surrender_limit': 0.10,
    'experience_gain_army_factor': 0.15, 'experience_gain_air_factor': 0.15,
    'air_mission_efficiency': 0.10, 'air_superiority_efficiency': 0.10, 'air_detection': 0.15,
    'air_defence_factor': 0.10, 'static_anti_air_damage_factor': 0.15, 'naval_coordination': 0.10,
    'naval_speed_factor': 0.08, 'navy_org_factor': 0.10,
}
BUILDINGS = ('industrial_complex', 'arms_factory', 'infrastructure', 'air_base', 'radar_station')
TECH_CATEGORIES = ('industry', 'electronics', 'artillery', 'infantry_weapons', 'land_doctrine', 'air_doctrine',
                   'construction_tech', 'naval_equipment', 'radar_tech', 'logistics_tech', 'rocketry',
                   'excavation_tech', 'engineers_tech', 'train_tech', 'synth_resources')
FILTERS = ('FOCUS_FILTER_POLITICAL', 'FOCUS_FILTER_RESEARCH', 'FOCUS_FILTER_INDUSTRY', 'FOCUS_FILTER_STABILITY',
           'FOCUS_FILTER_WAR_SUPPORT', 'FOCUS_FILTER_MANPOWER', 'FOCUS_FILTER_ARMY_XP', 'FOCUS_FILTER_NAVY_XP',
           'FOCUS_FILTER_AIR_XP', 'FOCUS_FILTER_INTERNAL_AFFAIRS')
XP_KINDS = {'army': 'army_experience', 'air': 'air_experience', 'navy': 'navy_experience'}
LAYERS = ('Official', 'Mod provenance', 'Provisional gameplay')


def subjects():
    import sys
    sys.path.insert(0, str(ROOT / 'tools/usea_depth'))
    import seams
    return seams.SUBJECTS


def ideologies(mod=MOD):
    """party -> set of its sub-ideologies, read from the mod's ideology file."""
    text = (mod / 'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig', errors='replace')
    result, depth, party = {}, 0, None
    for line in text.splitlines():
        code = line.split('#', 1)[0]
        match = re.match(r'\s*([a-z_]+)\s*=\s*\{', code)
        if match and depth == 1:
            party = match[1]
            result[party] = set()
        elif match and depth == 3 and party:
            result[party].add(match[1])
        depth += code.count('{') - code.count('}')
    for party in result:
        result[party].discard('hidden_modifier')
    return result


def own_states(tag, mod=MOD):
    """The country's 1991 states and its capital, from history files."""
    states = set()
    for path in (mod / 'history/states').glob('*.txt'):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        owner = re.search(r'\bowner\s*=\s*([A-Z0-9]{3})', text)
        ident = re.search(r'\bid\s*=\s*(\d+)', text)
        if owner and ident and owner[1] == tag:
            states.add(int(ident[1]))
    capital = None
    for path in (mod / 'history/countries').glob(tag + ' *.txt'):
        match = re.search(r'^\s*capital\s*=\s*(\d+)', path.read_text(encoding='utf-8-sig', errors='replace'), re.M)
        capital = int(match[1]) if match else None
    return states, capital
