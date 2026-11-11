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
BUILDINGS = ('industrial_complex', 'arms_factory', 'infrastructure', 'air_base', 'radar_station', 'dockyard')
# Buildings that share a state's slots, and per-state caps of the others (base game 1.19 rules).
SHARED_BUILDINGS = ('industrial_complex', 'arms_factory', 'dockyard', 'synthetic_refinery', 'fuel_silo', 'rocket_site',
                    'nuclear_reactor')
STATE_CAPS = {'infrastructure': 5, 'air_base': 10, 'radar_station': 6}
# Shared slots per state category. The mod does not replace common/state_category, so these are the
# base game's values (1.19); a native check (#8) confirms them in the installed game.
CATEGORY_SLOTS = {'wasteland': 0, 'enclave': 0, 'tiny_island': 0, 'pastoral': 1, 'small_island': 1, 'rural': 2,
                  'town': 4, 'large_town': 5, 'city': 6, 'large_city': 8, 'metropolis': 10, 'megalopolis': 12}
ERAS = {'e1': (1991, 2005), 'e2': (2006, 2020), 'e3': (2021, 2040)}
_CACHE = {}
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
    if not states:
        # A release (REL, SER, TER...) owns nothing in 1991; its tree applies once it exists, on
        # its core states and its history capital. Builds there stay guarded by owns_state.
        for path in (mod / 'history/states').glob('*.txt'):
            text = re.sub(r'#[^\n]*', '', path.read_text(encoding='utf-8-sig', errors='replace'))
            ident = re.search(r'\bid\s*=\s*(\d+)', text)
            if ident and re.search(r'\badd_core_of\s*=\s*%s\b' % tag, text):
                states.add(int(ident[1]))
        if capital is not None:
            states.add(capital)
    return states, capital


def global_flags(mod=MOD):
    """Global flags some mod script sets: the only ones a spec may read (HasGlobal/NotGlobal)."""
    if 'global' not in _CACHE:
        found = set()
        for path in mod.rglob('*.txt'):
            if 'localisation' in path.parts:
                continue
            text = re.sub(r'#[^\n]*', '', path.read_text(encoding='utf-8-sig', errors='replace'))
            found |= set(re.findall(r'\bset_global_flag\s*=\s*\{?\s*(?:flag\s*=\s*)?([A-Za-z0-9_]+)', text))
        _CACHE['global'] = found
    return _CACHE['global']


def state_profile(state, mod=MOD):
    """(slots, existing shared buildings, other building levels, coastal) of a state, from its history."""
    if 'states' not in _CACHE:
        coastal = set()
        for row in (mod / 'map/definition.csv').read_text(encoding='utf-8-sig', errors='replace').splitlines():
            cells = row.split(';')
            if len(cells) > 5 and cells[0].isdigit() and cells[5] == 'true':
                coastal.add(int(cells[0]))
        states = {}
        for path in (mod / 'history/states').glob('*.txt'):
            text = re.sub(r'#[^\n]*', '', path.read_text(encoding='utf-8-sig', errors='replace'))
            ident = re.search(r'\bid\s*=\s*(\d+)', text)
            if not ident:
                continue
            category = re.search(r'\bstate_category\s*=\s*([a-z_]+)', text)
            provinces = re.search(r'\bprovinces\s*=\s*\{([^}]*)\}', text)
            buildings = re.search(r'\bbuildings\s*=\s*\{(.*?)\n\t*\}', text, re.S)
            levels = {}
            if buildings:
                body = re.sub(r'\d+\s*=\s*\{[^}]*\}', '', buildings[1])    # province-level buildings
                for key, value in re.findall(r'([a-z_]+)\s*=\s*(\d+)', body):
                    levels[key] = levels.get(key, 0) + int(value)
            extra = sum(int(v) for v in re.findall(r'add_extra_state_shared_building_slots\s*=\s*(\d+)', text))
            members = {int(p) for p in provinces[1].split()} if provinces else set()
            slots = CATEGORY_SLOTS.get(category[1] if category else 'rural', 2) + extra
            shared = sum(levels.get(k, 0) for k in SHARED_BUILDINGS)
            states[int(ident[1])] = (slots, shared, levels, bool(members & coastal))
        _CACHE['states'] = states
    return _CACHE['states'].get(state)


def era_need(tag, era, own_prefix, root=ROOT):
    """Focuses a spec must supply for one era: the manifest target minus what other owners delivered."""
    import json
    manifest = json.loads((root / 'tools/world_campaigns/manifest.json').read_text(encoding='utf-8'))
    for country in manifest['countries']:
        if country['tag'] == tag:
            row = next(e for e in country['eras'] if e['era'] == era)
            others = [i for i in row['delivered_ids'] if not i.startswith(own_prefix)]
            return max(0, row['target'] - len(others)), row['target']
    raise ValueError('%s is not in the national-campaign manifest' % tag)


def chronicle_keys(root=ROOT):
    import json
    return {row['key'] for row in json.loads((root / 'tools/lore/chronicle.json').read_text(encoding='utf-8'))['entries']}
