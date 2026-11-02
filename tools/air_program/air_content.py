"""Conventional aviation2006–2020; all specifications are provisional gameplay."""
from dataclasses import dataclass

YEARS=(2006,2010,2015,2020)
LAR='La Resistance';BBA='By Blood Alone'


@dataclass(frozen=True)
class Family:
    id:str
    title:str
    model:str
    archetype:str|None
    parent:str|None
    airframe_parent:str|None
    equipment_type:str|None
    legacy_foundation:str|None
    designer_foundation:str|None
    missions:tuple
    description:str


FAMILIES=(
 Family('systems','Air Systems','',None,None,None,None,None,None,(),
        'Develop serviceable propulsion, flight controls and mission electronics for a new generation of aircraft. Component research supports manufacturing, while industrial capacity, trained crews and fuel remain essential.'),
 Family('fighter','Air Superiority','Service Fighter','small_plane_airframe','jet_fighter_equipment_2','small_plane_airframe_4','fighter','jet_fighter2','modern_small_airframe',('air_superiority','interception','training'),
        'Pair a conventional air-superiority airframe with sustained propulsion, modern armament and maintainable controls. Build and deliver the eligible aircraft, with trained crews, fuel and replacement capacity to keep it operating.'),
 Family('strike','Tactical Strike','Strike Aircraft','small_plane_cas_airframe','CAS_equipment_3','small_plane_airframe_4','cas','CAS3','modern_small_airframe',('cas','training'),
        'Equip a dedicated strike aircraft for conventional battlefield attack. Its ordnance and defensive fit require their own manufacturing capacity, while the aircraft depends on trained crews, fuel and delivered replacement equipment.'),
 Family('maritime','Maritime Strike','Maritime Strike Aircraft','small_plane_naval_bomber_airframe','nav_bomber_equipment_3','small_plane_airframe_4','naval_bomber','naval_bomber3','modern_small_airframe',('naval_bomber','port_strike','training'),
        'Extend maritime patrol endurance and fit conventional attack equipment for ships and ports. Surface sensors support target identification, while each operation requires aircraft, trained crews, fuel and the appropriate mission capability.'),
 Family('transport','Air Transport','Transport Aircraft','transport_plane_equipment','transport_plane_equipment_1',None,'air_transport',None,None,('paradrop','air_supply'),
        'Build a service transport aircraft with improved range and survivability. Production, aircrews and fuel must support each operation. This complete-aircraft programme works with or without the aircraft designer; airborne troops retain their separate training requirements.'),
 Family('surveillance','Air Surveillance','Surveillance Aircraft','medium_plane_scout_plane_airframe','scout_plane_equipment_2','medium_plane_airframe_4','scout_plane','scout_plane2','modern_medium_airframe',('recon','naval_patrol'),
        'Fit a long-range reconnaissance aircraft with optical instruments and reliable flight controls. La Resistance is required for this optional programme. Intelligence gathering depends on the missions, trained crews and aircraft available.'),
)
FAMILY={f.id:f for f in FAMILIES};AIRCRAFT=tuple(f for f in FAMILIES if f.archetype)
TECHS=[dict(id=f'ac_air_{f.id}_{year}',family=f.id,year=year,tier=t,row=r) for r,f in enumerate(FAMILIES) for t,year in enumerate(YEARS)]

# Native module categories and effect grammar; model names/statistics are ours.
# Each default has one engine and one mission armament/camera, so averaged
# weapon statistics have a single contributor. Optional mixed-loadout behavior
# remains separately observable/native, never silently treated as a sum.
MODULES={
 'single_engine':dict(title='Service Jet Powerplant',category='plane_jet_engine_type',add=dict(thrust=32,weight=2,build_cost_ic=20,fuel_consumption=.22),step=dict(thrust=4,build_cost_ic=3,fuel_consumption=.02),multiply=dict(maximum_speed=.6,air_range=-.1,air_agility=.05),multiply_step=dict(maximum_speed=.05),resources=dict(chromium=1)),
 'twin_engine':dict(title='Twin Service Powerplant',category='twin_plane_jet_engine_type',add=dict(thrust=50,weight=4,build_cost_ic=34,fuel_consumption=.5),step=dict(thrust=5,build_cost_ic=4,fuel_consumption=.04),multiply=dict(maximum_speed=.6,air_range=-.1,air_agility=.05),multiply_step=dict(maximum_speed=.05),resources=dict(chromium=1)),
 'fighter_armament':dict(title='Air Combat Package',category='fighter_weapon',add=dict(air_attack=40,weight=4,build_cost_ic=12),step=dict(air_attack=5,build_cost_ic=2),resources=dict(steel=1,tungsten=1),equipment_type='fighter',missions=('air_superiority','interception')),
 'strike_armament':dict(title='Battlefield Ordnance',category='cas_weapon',add=dict(air_ground_attack=36,air_attack=8,weight=6,build_cost_ic=12),step=dict(air_ground_attack=5,air_attack=2,build_cost_ic=2),average=dict(naval_strike_attack=6,naval_strike_targetting=6),average_step=dict(naval_strike_attack=1,naval_strike_targetting=1),resources=dict(steel=1),equipment_type='cas',missions=('cas','attack_logistics','naval_bomber','port_strike')),
 'maritime_armament':dict(title='Maritime Attack Outfit',category='nav_bomber_weapon',add=dict(air_attack=4,weight=7,build_cost_ic=14),step=dict(air_attack=1,build_cost_ic=2),average=dict(naval_strike_attack=24,naval_strike_targetting=10),average_step=dict(naval_strike_attack=4,naval_strike_targetting=2),resources=dict(steel=1),equipment_type='naval_bomber',missions=('naval_bomber','port_strike','naval_patrol')),
 'camera':dict(title='Reconnaissance Instruments',category='recon_camera',add=dict(weight=2,build_cost_ic=8),step=dict(build_cost_ic=1),resources=dict(aluminium=1),equipment_type='scout_plane',missions=('recon',)),
 'flight_controls':dict(title='Mission Flight Controls',category='plane_special_module_air_air_radar',add=dict(air_defence=2,air_agility=4,weight=1,build_cost_ic=4),step=dict(air_defence=.5,air_agility=1,build_cost_ic=1),resources=dict(aluminium=1)),
 'maritime_sensors':dict(title='Maritime Surface Sensors',category='plane_special_module_air_ground_radar',add=dict(surface_detection=10,naval_strike_targetting=2,weight=1,build_cost_ic=4),step=dict(surface_detection=3,naval_strike_targetting=1,build_cost_ic=1),resources=dict(aluminium=1)),
}
# Retain predecessor mission declarations, without inventing DLC equivalence.
# The legacy maritime predecessor includes mine tasks which a bare BBA attack
# loadout does not supply. That difference remains explicit in the worksheet.
LEGACY_MISSIONS={
 'fighter':('air_superiority','interception','training'),
 'strike':('attack_logistics','cas','naval_bomber','port_strike','training'),
 'maritime':('naval_bomber','naval_mines_planting','naval_mines_sweeping','naval_patrol','port_strike','training'),
 'transport':('paradrop','air_supply'),'surveillance':('recon','naval_patrol'),
}
ROLE_PRESENTATION={'fighter':(1,1,'light_plane'),'strike':(2,0,'light_plane'),'maritime':(3,2,'light_plane'),
                   'transport':(12,6,'medium_plane'),'surveillance':(13,7,'scout_plane')}


def tech_id(family,year):return f'ac_air_{family}_{year}'
def model_id(family,year):return f'ac_air_{family}_equipment_{year}'
def frame_id(family,year):return f'ac_air_{family}_airframe_{year}'
def module_id(kind,year):return f'ac_air_{kind}_{year}'


def recipe(family,year):
    if family=='transport':return {}
    return dict(fixed_main_weapon_slot=module_id('camera' if family=='surveillance' else family+'_armament',year),
                engine_type_slot=module_id('twin_engine' if family=='surveillance' else 'single_engine',year),
                special_type_slot_1=module_id('maritime_sensors' if family=='maritime' else 'flight_controls',year))


def unlocks(family,year):
    kinds=('single_engine','twin_engine','flight_controls','maritime_sensors') if family=='systems' else ('camera',) if family=='surveillance' else (family+'_armament',) if family!='transport' else ()
    return tuple(module_id(k,year) for k in kinds)


def common_dependencies(family,tier):
    if family=='systems':return (tech_id('systems',YEARS[tier-1]),) if tier else ('radio','basic_machine_tools','electronic_mechanical_engineering')
    return (tech_id('systems',YEARS[tier]),)+((tech_id(family,YEARS[tier-1]),) if tier else ())
