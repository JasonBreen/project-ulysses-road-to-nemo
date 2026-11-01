"""Conventional naval manufacturing, 2006–2020; provisional gameplay values."""
from dataclasses import dataclass

YEARS=(2006,2010,2015,2020)
MTG='Man the Guns'

@dataclass(frozen=True)
class Family:
    id:str
    title:str
    model:str
    archetype:str|None
    parent:str|None
    hull_parent:str|None
    equipment_type:str|None
    legacy_foundation:str|None
    designer_foundation:str|None
    engine:str|None
    native_blueprint:str|None
    description:str

FAMILIES=(
 Family('systems','Naval Systems','',None,None,None,None,None,None,None,None,
  'Develop serviceable propulsion, sensors, fire direction and protective fittings. Shipbuilding still requires dockyards, materials, trained crews and sustained fuel and repair support.'),
 Family('escort','Escort Ships','Service Escort','ship_hull_light','destroyer_4','ship_hull_light_4','screen_ship','advanced_destroyer','advanced_ship_hull_light','light_engine','light',
  'Build a conventional escort with guns, torpedoes, sonar and depth-charge equipment. Screening and convoy protection require delivered ships, trained crews, fuel and the appropriate operational orders.'),
 Family('cruiser','Patrol Cruisers','Patrol Cruiser','ship_hull_cruiser','light_cruiser_4','ship_hull_cruiser_4','screen_ship','advanced_light_cruiser','advanced_ship_hull_cruiser','cruiser_engine','cruiser',
  'Sustain a patrol cruiser with surface armament, local air defense and greater endurance. Its sensors and protective fittings support conventional fleet operations while increasing industrial and operating demands.'),
 Family('fleet','Fleet Combatants','Fleet Combatant','ship_hull_cruiser','heavy_cruiser_4','ship_hull_cruiser_4','capital_ship','advanced_heavy_cruiser','advanced_ship_hull_cruiser','cruiser_engine','cruiser',
  'Build a capital-role cruiser with heavier conventional surface armament and protection. The programme supports fleet operations through gun combat, fire direction and endurance; it does not introduce guided-missile or strategic weapons.'),
 Family('submarine','Patrol Submarines','Patrol Submarine','ship_hull_submarine','submarine_4','ship_hull_submarine_4','submarine','advanced_submarine','advanced_ship_hull_submarine','sub_engine','submarine',
  'Improve a conventional torpedo submarine for patrol and surface interdiction. Endurance and reduced visibility require costly propulsion and hull work, trained crews and maintenance. This programme does not implement submarine-versus-submarine combat.'),
 Family('carrier','Carrier Platforms','Service Carrier','ship_hull_carrier','carrier_4','ship_hull_carrier_3','carrier','advanced_carrier','advanced_ship_hull_carrier','carrier_engine','carrier',
  'Build a carrier platform with researched deck facilities, propulsion and defensive fittings. Its air group must be researched and produced separately through existing eligible carrier-aircraft programmes.'),
)
FAMILY={f.id:f for f in FAMILIES};SHIPS=tuple(f for f in FAMILIES if f.archetype)
TECHS=[dict(id=f'ac_naval_{f.id}_{year}',family=f.id,year=year,tier=t,row=r) for r,f in enumerate(FAMILIES) for t,year in enumerate(YEARS)]

MODULES={
 'light_engine':dict(title='Escort Propulsion',category='light_ship_engine',add=dict(fuel_consumption=9,build_cost_ic=220),step=dict(build_cost_ic=35,fuel_consumption=.5),multiply=dict(naval_speed=.25),multiply_step=dict(naval_speed=.025),resources=dict(chromium=1)),
 'cruiser_engine':dict(title='Cruiser Propulsion',category='cruiser_ship_engine',add=dict(fuel_consumption=18,build_cost_ic=450),step=dict(build_cost_ic=60,fuel_consumption=1),multiply=dict(naval_speed=.25),multiply_step=dict(naval_speed=.025),resources=dict(chromium=1)),
 'sub_engine':dict(title='Submarine Propulsion',category='sub_ship_engine',add=dict(fuel_consumption=4,build_cost_ic=250),step=dict(build_cost_ic=40,fuel_consumption=.25),multiply=dict(naval_speed=.15),multiply_step=dict(naval_speed=.025),resources=dict(chromium=1)),
 'carrier_engine':dict(title='Carrier Propulsion',category='carrier_ship_engine',add=dict(fuel_consumption=26,build_cost_ic=700),step=dict(build_cost_ic=90,fuel_consumption=1),multiply=dict(naval_speed=.2),multiply_step=dict(naval_speed=.025),resources=dict(chromium=1)),
 'escort_battery':dict(title='Dual-Purpose Battery',category='dp_light_battery',add=dict(lg_attack=5,anti_air_attack=4.5,build_cost_ic=200),step=dict(lg_attack=1,anti_air_attack=.5,build_cost_ic=30),average=dict(lg_armor_piercing=8),average_step=dict(lg_armor_piercing=2),resources=dict(steel=1)),
 'cruiser_battery':dict(title='Cruiser Surface Battery',category='ship_light_medium_battery',add=dict(lg_attack=12,build_cost_ic=500),step=dict(lg_attack=2,build_cost_ic=60),average=dict(lg_armor_piercing=18),average_step=dict(lg_armor_piercing=3),resources=dict(steel=1,tungsten=1)),
 'fleet_battery':dict(title='Heavy Surface Battery',category='ship_medium_battery',add=dict(hg_attack=16,build_cost_ic=650),step=dict(hg_attack=3,build_cost_ic=80),average=dict(hg_armor_piercing=36),average_step=dict(hg_armor_piercing=5),resources=dict(steel=1,tungsten=1),equipment_type='capital_ship'),
 'surface_torpedo':dict(title='Surface Torpedo Outfit',category='ship_torpedo',add=dict(torpedo_attack=40,build_cost_ic=240,naval_torpedo_hit_chance_factor=.02),step=dict(torpedo_attack=4,build_cost_ic=30,naval_torpedo_hit_chance_factor=.005),resources=dict(steel=1)),
 'sub_torpedo':dict(title='Submarine Torpedo Outfit',category='ship_torpedo_sub',add=dict(torpedo_attack=30,build_cost_ic=250,naval_torpedo_hit_chance_factor=.02),step=dict(torpedo_attack=5,build_cost_ic=35,naval_torpedo_hit_chance_factor=.005),resources=dict(steel=1)),
 'air_defense':dict(title='Local Air Defense',category='ship_anti_air',add=dict(anti_air_attack=6,build_cost_ic=180),step=dict(anti_air_attack=1,build_cost_ic=25),resources=dict(aluminium=1),equipment_type='anti_air'),
 'fire_control':dict(title='Ship Fire Direction',category='ship_fire_control_system',add=dict(build_cost_ic=100),step=dict(build_cost_ic=20),multiply=dict(lg_attack=.1,hg_attack=.1),multiply_step=dict(lg_attack=.025,hg_attack=.025),resources=dict(aluminium=1)),
 'radar':dict(title='Surface-Search Radar',category='ship_radar',add=dict(surface_detection=20,build_cost_ic=140),step=dict(surface_detection=4,build_cost_ic=25),resources=dict(aluminium=1)),
 'sonar':dict(title='Submarine Search Instruments',category='ship_sonar',add=dict(sub_detection=16,build_cost_ic=100),step=dict(sub_detection=3,build_cost_ic=20),resources=dict(aluminium=1)),
 'depth_charge':dict(title='Depth-Charge Outfit',category='ship_depth_charge',add=dict(sub_attack=22,build_cost_ic=180),step=dict(sub_attack=4,build_cost_ic=25),resources=dict(steel=1)),
 'deck':dict(title='Flight Deck Facilities',category='ship_deck_space',add=dict(carrier_size=6,build_cost_ic=1900,carrier_surface_detection=8,carrier_sub_detection=4),step=dict(carrier_size=1,build_cost_ic=200),crew=600,crew_step=50,resources=dict(steel=1,aluminium=1),equipment_type='capital_ship'),
 'armor':dict(title='Cruiser Protective Scheme',category='ship_cruiser_armor',add=dict(armor_value=14,build_cost_ic=400),step=dict(armor_value=2,build_cost_ic=60),multiply=dict(naval_speed=-.08,max_strength=.1),resources=dict(steel=1,chromium=1)),
}

def tech_id(family,year):return f'ac_naval_{family}_{year}'
def model_id(family,year):return f'ac_naval_{family}_equipment_{year}'
def hull_id(family,year):return f'ac_naval_{family}_hull_{year}'
def module_id(kind,year):return f'ac_naval_{kind}_{year}'
def dependencies(family,tier):
    if family=='systems':return (tech_id('systems',YEARS[tier-1]),) if tier else ('radio','basic_machine_tools','electronic_mechanical_engineering')
    return (tech_id('systems',YEARS[tier]),)+((tech_id(family,YEARS[tier-1]),) if tier else ())
def unlocks(family,year):
    kinds={'systems':('light_engine','cruiser_engine','sub_engine','carrier_engine','air_defense','fire_control','radar','sonar','armor'),
        'escort':('escort_battery','surface_torpedo','depth_charge'),'cruiser':('cruiser_battery',),'fleet':('fleet_battery',),'submarine':('sub_torpedo',),'carrier':('deck',)}[family]
    return tuple(module_id(k,year) for k in kinds)
def recipe(family,year):
    row=FAMILY[family];parts={'fixed_ship_engine_slot':row.engine}
    if family=='submarine':parts['fixed_ship_torpedo_slot']='sub_torpedo'
    elif family=='carrier':parts.update(fixed_ship_deck_slot_1='deck',fixed_ship_anti_air_slot='air_defense',fixed_ship_radar_slot='radar')
    else:
        parts.update(fixed_ship_battery_slot=family+'_battery',fixed_ship_anti_air_slot='air_defense',fixed_ship_radar_slot='radar')
        if family=='escort':parts.update(fixed_ship_fire_control_system_slot='sonar',fixed_ship_torpedo_slot='surface_torpedo',rear_1_custom_slot='depth_charge')
        else:parts.update(fixed_ship_fire_control_system_slot='fire_control',fixed_ship_armor_slot='armor')
    return {k:module_id(v,year) for k,v in parts.items()}
