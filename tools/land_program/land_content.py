"""Provisional 2006–2020 land capability design; no canonical model claims."""
from dataclasses import dataclass

YEARS=(2006,2010,2015,2020)

# Actual complete optional AI target: six infantry, engineer, logistics and
# both specialist companies. Minima are compared with captured unit needs by
# regression; specialist buffers intentionally exceed a single detachment.
AI_TARGET_TECHS=('ac_land_surveillance_2006','ac_land_electronic_support_2006','tech_engineers','tech_logistics_company')
AI_TARGET_STOCKS=dict(ac_land_sensor_equipment=101,ac_land_electronic_equipment=121,
    infantry_equipment=610,support_equipment=80,motorized_equipment=26)


@dataclass(frozen=True)
class Family:
    id:str
    title:str
    equipment_title:str
    categories:tuple
    foundations:tuple
    description:str


FAMILIES=(
 Family('infantry','Infantry Systems','Service Rifle',('infantry_weapons','infantry_tech'),('infantry_weapons2',),
        'Revised sights, ammunition handling and maintainable weapon assemblies improve the infantry equipment that must be manufactured and delivered. Better performance carries higher industrial and material costs.'),
 Family('mobility','Protected Mobility','Protected Carrier',('motorized_equipment','cat_mechanized_equipment'),('mechanised_infantry',),
        'Protected troop carriers combine improved survivability with more reliable running gear. Existing mechanized formations can use the new equipment; production, fuel and replacement requirements remain physical costs.'),
 Family('mbt','Battle Platforms','Battle Platform',('armor','cat_modern_armor'),('basic_machine_tools','ac_land_mobility_2006'),
        'A conventional battle platform combines protection, a stabilized gun and a serviceable power train. Manufacture the eligible complete vehicle or create a researched modular design; neither route supplies free tanks.'),
 Family('tracked_artillery','Tracked Fire Support','Tracked Fire Support',('armor','artillery'),('artillery2','ac_land_mbt_2006'),
        'Tracked artillery exchanges some protection and assault capability for sustained fire support. The vehicle, gun and ammunition chain require separate industrial capacity; this is conventional artillery, without strategic-weapon effects.'),
 Family('support','Combat Services','Service Workshop Set',('support_tech','engineers_tech'),('tech_support','tech_engineers2'),
        'Maintainable engineering and workshop equipment supports field repairs and prepared positions. New equipment must reach the units, while trained engineering and maintenance practices improve their limited support capabilities.'),
 Family('logistics','Distribution Systems','Distribution Truck',('support_tech','logistics_tech','motorized_equipment'),('tech_logistics_company3','motorised_infantry'),
        'Reliable distribution vehicles and better load planning reduce avoidable supply and fuel demands in logistics companies. They do not create railway capacity, delivered fuel, resources or equipment without production.'),
 Family('surveillance','Field Surveillance','Field Sensor Set',('electronics','recon_tech','support_tech'),('radio','tech_recon2'),
        'Field sensors support a dedicated reconnaissance company with crews, vehicles and manufactured instruments. Its battlefield awareness replaces competing reconnaissance support; it does not reveal the strategic map or guarantee intelligence.'),
 Family('electronic_support','Electronic Support','Electronic Support Set',('electronics','signal_company_tech','support_tech'),('radio','tech_signal_company2'),
        'Tactical electronic support combines direction finding and resilient communications. A supplied specialist company improves local coordination, replacing competing signal support; strategic intelligence, air jamming and radar suppression remain separate capabilities.'),
)
FAMILY={row.id:row for row in FAMILIES}
TECHS=[dict(id=f'ac_land_{row.id}_{year}',family=row.id,year=year,tier=tier,row=index)
       for index,row in enumerate(FAMILIES) for tier,year in enumerate(YEARS)]

# Every module uses an installed engine category/slot contract. Values are
# authored calibration, not real-world specifications or canonical technology.
MODULES={
 'gun':dict(title='Stabilized Cannon',category='tank_heavy_main_armament',stats=dict(soft_attack=38,hard_attack=40,ap_attack=150,build_cost_ic=8,reliability=-.08),step=dict(soft_attack=3,hard_attack=4,ap_attack=15,build_cost_ic=1),resources=dict(tungsten=2,steel=1)),
 'turret':dict(title='Crewed Battle Turret',category='tank_modern_turret_type',stats=dict(breakthrough=45,defense=5,build_cost_ic=5),step=dict(breakthrough=3,defense=1,build_cost_ic=.5),resources=dict(steel=1)),
 'protection':dict(title='Composite Protection',category='tank_armor_type',stats=dict(armor_value=65,build_cost_ic=5,reliability=-.03),step=dict(armor_value=12,build_cost_ic=1),resources=dict(chromium=1)),
 'powertrain':dict(title='Service Power Train',category='tank_engine_type',stats=dict(maximum_speed=4,fuel_consumption=4.5,build_cost_ic=3),step=dict(maximum_speed=.2,fuel_consumption=-.1,build_cost_ic=.5),resources=dict(steel=1)),
 'running_gear':dict(title='Service Running Gear',category='tank_suspension_type',stats=dict(reliability=.08,build_cost_ic=2),step=dict(reliability=.01,build_cost_ic=.25),resources={}),
 'artillery_turret':dict(title='Artillery Mount',category='tank_medium_turret_type',stats=dict(breakthrough=-10,defense=3,build_cost_ic=3),step=dict(defense=1,build_cost_ic=.5),resources=dict(steel=1)),
 'howitzer':dict(title='Conventional Howitzer',category='tank_heavy_main_armament',stats=dict(soft_attack=65,hard_attack=5,ap_attack=60,build_cost_ic=8,reliability=-.08),step=dict(soft_attack=5,hard_attack=1,ap_attack=5,build_cost_ic=1),resources=dict(tungsten=2,steel=1)),
 'optics':dict(title='Field Optics',category='tank_special_module',stats=dict(ap_attack=5,defense=1,build_cost_ic=1),step=dict(ap_attack=2,build_cost_ic=.25),resources=dict(aluminium=1)),
 'protected_radio':dict(title='Protected Tactical Radio',category='tank_radio_module',stats=dict(breakthrough=4,defense=2,build_cost_ic=1),step=dict(breakthrough=1,build_cost_ic=.25),resources=dict(aluminium=1)),
}


def module_id(kind,year):return f'ac_land_{kind}_{year}'
def model_id(family,year):return f'ac_land_{family}_equipment_{year}'
def chassis_id(family,year):return f'ac_land_{family}_chassis_{year}'


def recipe(family,year):
    return {
      'turret_type_slot':module_id('turret' if family=='mbt' else 'artillery_turret',year),
      'main_armament_slot':module_id('gun' if family=='mbt' else 'howitzer',year),
      'suspension_type_slot':module_id('running_gear',year),
      'armor_type_slot':module_id('protection',year),
      'engine_type_slot':module_id('powertrain',year),
    }


def models(family,year):
    ids=[model_id(family,year)]
    if family in ('mbt','tracked_artillery'):ids.append(chassis_id(family,year))
    return ids


def module_unlocks(family,year):
    kinds={'mbt':('gun','turret','protection','powertrain','running_gear'),
           'tracked_artillery':('artillery_turret','howitzer'),
           'surveillance':('optics',),'electronic_support':('protected_radio',)}.get(family,())
    return [module_id(kind,year) for kind in kinds]


def prerequisites(family,tier):
    year=YEARS[tier];required=[]
    if tier:required.append(f'ac_land_{family}_{YEARS[tier-1]}')
    else:required.extend(FAMILY[family].foundations)
    if family=='tracked_artillery' and tier:required.append(f'ac_land_mbt_{year}')
    return required
