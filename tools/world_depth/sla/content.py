"""Slavia (SLA): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (the neutrality party ruling with
70 percent popularity, elections suspended since the vote of November 1987, stability 0.4
and war support 0.9), the unnamed National Administration office, the party-specific
country names, the single 1991 state of Lhesk with its one coastal province, the map
(terrain, coast, weather, neighbours), the neighbouring Seteranoan tree and the global
flags the mod already sets. Official: ACES Chronicle rows used only as date anchors for
distant pressures, each cited by its exact key. Everything else, including every Slavian
choice, office, idea, building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='SLA', name='Slavia', root='world', package='sla',
                  themes=('security', 'industry', 'navy'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party neutrality with last_election 1987.11.9, election_frequency 48 and '
           'elections_allowed = no; popularities neutrality 70, communism 23, fascism 6, democratic 1; stability 0.4 and war '
           'support 0.90; three research slots; tech_mountaineers, early_fighter and basic_train among the starting '
           'technologies. The starting leader is the unnamed National Administration office (SLA_ac_government_office, '
           'centrism_na), whose description says its 1991 holder has not been established. The tree never names a holder. '
           'The overdue ballot of November 1991 is read from the inherited calendar, not from any canon source.',
           'mod/2985041246/history/countries/SLA - Slavia.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Slavian Republic (neutrality), Slavian Federation (democratic), Slavian Federative '
           'Socialist Republic (communism); adjective Slavian. The federal path takes the democratic name and the works path '
           'the communist name; the managers and defence paths keep the Republic. No claim, core, war or annexation follows '
           'from any path.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: one 1991 state, 133, localised Lhesk (capital; state_category large_city, eight shared slots, all filled '
           'by 5 arms factories, 2 industrial complexes and 1 fuel silo; infrastructure 3; air base 1; no radar). One province, '
           '11348, coastal plains, with naval base 1, a supply node and victory point Lhesk, value 20. Resources oil 4, '
           'aluminium 6, rubber 3, steel 9. Strategic region 235: heavy rain likely from January to May, almost none from June '
           'to September with highs of 36 to 37, mud in every month and light snow possible from December to February. Land '
           'neighbours computed from map/provinces.bmp: VLK (state 397, hills 8257) to the west; SET (state 356, mountains '
           '2455 and 559) to the north and north-east and SET (state 362, plains 4443) on a very short eastern contact; sea '
           'province 10632 to the south. Compass words come from province centroids. No other place is named; neighbour state '
           'captions are not used.',
           'mod/2985041246/history/states/133-State_133.txt; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/definition.csv; '
           'mod/2985041246/map/provinces.bmp; mod/2985041246/map/strategicregions/235-XXX.txt; '
           'mod/2985041246/map/supply_nodes.txt; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Neighbours as inherited: Valka ruled by its democratic party with elections suspended and popularity neutrality '
           '48, fascism 50; Seterano with five 1991 states. Neighbour consistency: the Seteranoan tree places Slavia to its '
           'west beyond its capital plain, touches it only through its own mountain district and capital plain, rebuilds only '
           'its own side of the western road and leaves the far side for Slavia to decide. This tree builds and governs only '
           'on the Slavian side, makes unilateral offers, and never asserts a neighbour response.',
           'mod/2985041246/history/countries/VLK - Valka.txt; mod/2985041246/history/countries/SET - Seterano.txt; '
           'tools/world_depth/set/content.py'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role single-province territorial air guard; 2 civilian and 5 military '
           'factories, no dockyard; two infantry formations of four battalions, each with an engineer company, at province '
           '11348; 12 fighters at state 133 with 4 in reserve; combat navy deliberately absent (territorial defence and '
           'merchant receiving only); 60 convoys; one fuel silo; stocks of 800 infantry equipment, 560 motorized equipment, '
           '160 support equipment and 24 trains; research priority Physical Sustainment. Fiscal figures (GDP 84, debt ratio '
           '0.3, collection 0.85, growth 3, inflation 2) and the executive_office institution at capacity 40 are fictional '
           'calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/economy_v2/profiles.json; '
           'tools/institutions/profiles.json; mod/2985041246/history/units/SLA_ws_land.txt, SLA_ws_air.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official', 'Date anchor: the IAU announces that Ulysses will pass close to the Earth and may strike it. Gate of '
           'the asteroid branch; no Slavian role is claimed.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gate of the distant-wars branch; Slavia takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Gate of the impact focus; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Former top pilots of the Belkan Air Force are hired by various countries as aggressor squadrons. '
           'Date gate and premise of the aggressor focus; nobody is named and no Slavian hire is asserted as fact.',
           '1998 / 06.19'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche night focus and '
           'event; no damage in Slavia is claimed or denied.', '1999 / 07.08'),
    Source('Official', 'Erusea invades San Salvacion and seizes Stonehenge. Background to the Usean war event only.',
           '2003 / SUMMER'),
    Source('Official', 'Date anchor: the FCU establishes the ISAF. Gate of the Usean war focus, which also waits for the '
           'mod global flag ac_ucw_isaf_formed; no Slavian part is claimed.', '2003 / 08.22'),
    Source('Official', 'Farbanti falls, Erusea surrenders and the Continental War ends. Background to the closing war '
           'focus, which waits for the mod outcome flag ac_ucw_outcome_isaf_victory instead of assuming this ending.',
           '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt); '
           'ac_ucw_isaf_formed and ac_ucw_outcome_isaf_victory (common/scripted_effects/ac_ucw.txt). Each reaction sits on a '
           'leaf or a short closing chain, so no outcome blocks the rest of the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Slavian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects. Every shared slot in Lhesk is '
           'already filled, so buildings are limited to infrastructure (two levels), air base and radar station levels in '
           'the capital state.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the overdue ballot
    IdeaDef('caretaker_mandate', 'A Mandate Past Its Term',
            'The National Administration governs on a mandate whose four-year term ran out in November 1991.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('ballot', 'document')),
    IdeaDef('canteen_forums', 'Questions at Shift Change',
            'Officials answer the workforce in the canteens of the halls and the docks every month.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'industry')),
    IdeaDef('ballot_calendar', 'A Published Polling Calendar',
            'Polling day, rolls and counting rules are printed a year ahead of every vote.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('managers_compact', 'Compact of the Directors',
            'Directors of the halls, the harbour and the banks agree one budget with the government.',
            {'production_factory_efficiency_gain_factor': 0.04, 'stability_factor': -0.02}, ('economy', 'command')),
    IdeaDef('works_delegates', 'Delegates from the Shop Floor',
            'Elected delegates of the arms halls and docks sit beside the ministers.',
            {'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': 0.02, 'political_power_gain': -0.05},
            ('assembly', 'tools')),
    IdeaDef('defence_ordinance', 'Ordinance of Defence',
            'Civil ministries take their priorities from the general staff.',
            {'war_support_factor': 0.05, 'army_core_defence_factor': 0.05, 'stability_factor': -0.02}, ('security', 'command')),
    IdeaDef('federal_law', 'Two Readings a Month Apart',
            'Every federal bill is read twice and printed in the newspapers between readings.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05}, ('assembly', 'scales')),
    IdeaDef('board_targets', 'Monthly Targets for Each Director',
            'Output, cost and harbour tonnage are posted for every director, every month.',
            {'production_factory_efficiency_gain_factor': 0.06, 'political_power_gain': 0.05}, ('economy', 'document')),
    IdeaDef('open_books', 'Accounts Open to the Workforce',
            'Each hall, works and dock publishes its books to the people who work in it.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.04, 'consumer_goods_factor': -0.02},
            ('document', 'assembly')),
    IdeaDef('reserve_roll', 'One Roll for Every Adult',
            'Every adult in the republic has an assignment, an assembly point and a yearly drill.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.08, 'stability_factor': -0.02},
            ('training', 'security')),
    IdeaDef('settlement_text', 'A Constitution Sold at Kiosks',
            'The settled form of government, printed and sold for the price of a newspaper.',
            {'stability_factor': 0.05, 'political_power_factor': 0.04}, ('document', 'peace')),
    # the single province
    IdeaDef('street_ledger', 'Register of Streets and Drains',
            'Every block, well and drain of the single province entered in one register.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.01}, ('document', 'civil')),
    IdeaDef('summer_cisterns', 'Cisterns Filled in the Rains',
            'Rooftop and street cisterns keep water flowing from June to September.',
            {'stability_factor': 0.03}, ('civil', 'shelter')),
    IdeaDef('worker_flats', 'Flats Beside the Halls',
            'New flats on hall land cut the journey to work for shift crews.',
            {'stability_factor': 0.02, 'production_factory_efficiency_gain_factor': 0.02}, ('rebuild', 'civil')),
    IdeaDef('ward_committees', 'Committees in Every Ward',
            'Each ward of Lhesk elects a committee with a small budget of its own.',
            {'stability_factor': 0.05, 'production_speed_buildings_factor': 0.05, 'political_power_gain': -0.05},
            ('ballot', 'civil')),
    IdeaDef('city_manager_office', 'Office of the City Manager',
            'One appointed manager holds authority over every street, pipe and permit.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.08}, ('command', 'civil')),
    IdeaDef('ward_purses', 'Ward Budgets in Print',
            'Ward committees spend a fixed share of the city budget and publish every item.',
            {'stability_factor': 0.06, 'production_speed_buildings_factor': 0.08, 'political_power_gain': -0.05},
            ('scales', 'civil')),
    IdeaDef('manager_schedule', 'One Ranked List of Works',
            'Drains, housing and roads are built in the order the city manager sets.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.10, 'stability_factor': -0.01},
            ('document', 'command')),
    IdeaDef('constituency_offices', 'A Member in Every Ward',
            'Each ward elects a member of the federal chamber who keeps an office on its street.',
            {'stability_factor': 0.04, 'political_power_factor': 0.03}, ('ballot', 'assembly')),
    IdeaDef('street_charter', 'Charter of the City Streets',
            'Streets, water, markets and transport belong to the city; defence and money stay national.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.10}, ('document', 'scales')),
    # the arms halls
    IdeaDef('hall_inventory', 'Seven Buildings Counted',
            'Every press, lathe and payroll in the five arms halls and two civil works is on record.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('rolled_plate', 'Plate Rolled at Home',
            'Slavian ore is rolled into plate at the civil works instead of sold raw.',
            {'production_factory_max_efficiency_factor': 0.03, 'consumer_goods_factor': -0.02}, ('industry', 'tools')),
    IdeaDef('civil_retooling', 'Civil Lines Under Arms Hall Roofs',
            'Two arms halls run protected civil lines for pumps, vans and tram parts.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': -0.03, 'war_support_factor': -0.03},
            ('rebuild', 'industry')),
    IdeaDef('licensed_exports', 'Rifles Sold Under Licence',
            'Every line busy with orders from governments on a published licence list.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04, 'stability_factor': -0.02},
            ('missile', 'economy')),
    IdeaDef('garrison_arsenal', 'Halls Working for the City',
            'All five halls build reserves for the republic and sell nothing abroad.',
            {'army_core_defence_factor': 0.06, 'production_factory_max_efficiency_factor': 0.04}, ('security', 'industry')),
    IdeaDef('van_orders', 'Vans for Shops and Wards',
            'A plain delivery van stamped out on the old rifle frames sells across the city.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('logistics', 'rebuild')),
    IdeaDef('end_user_office', 'Certificates for Every Crate',
            'Buyers and end uses of every arms export are named and published once a year.',
            {'political_power_factor': 0.04, 'production_speed_arms_factory_factor': 0.05}, ('document', 'navy')),
    IdeaDef('hall_magazines', 'Dry Magazines Under the Floors',
            'Reserve rifles and rounds stored in ventilated cellars below the arms halls.',
            {'army_core_defence_factor': 0.06, 'supply_consumption_factor': -0.04}, ('shelter', 'security')),
    IdeaDef('council_prices', 'Prices Set by Hall Councils',
            'Each hall council prices its own contracts; a national council settles disputes.',
            {'production_factory_efficiency_gain_factor': 0.05, 'consumer_goods_factor': -0.02}, ('assembly', 'economy')),
    IdeaDef('cool_hour_shifts', 'Lathes at Night in Summer',
            'Heavy work moves to the night and early morning through the hot months.',
            {'production_factory_max_efficiency_factor': 0.03, 'stability_factor': 0.01}, ('tools', 'civil')),
    IdeaDef('silo_reserve', 'The Silo Never Below Half',
            'Fuel bought ahead of need and the local wells pumped to keep the silo full.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.01}, ('logistics', 'shelter')),
    IdeaDef('decade_audit', 'The Second Hall Inventory',
            'Ten years of hall figures compared line by line and published in full.',
            {'production_factory_efficiency_gain_factor': 0.04, 'research_speed_factor': 0.02}, ('industry', 'scales')),
    # the harbour
    IdeaDef('harbour_office', 'One Counter for the Harbour',
            'Berths, pilots, dues and the convoy list handled by a single office.',
            {'naval_coordination': 0.03, 'political_power_gain': 0.03}, ('navy', 'document')),
    IdeaDef('dredged_channel', 'A Channel Kept Deep',
            'The harbour mouth is dredged on contract every few years against the silt.',
            {'naval_speed_factor': 0.03, 'consumer_goods_factor': -0.01}, ('tools', 'navy')),
    IdeaDef('fuel_jetty', 'A Buried Fuel Line',
            'Imported fuel lands at a jetty and runs underground to the silo.',
            {'supply_consumption_factor': -0.03, 'naval_coordination': 0.02}, ('logistics', 'navy')),
    IdeaDef('transit_wharf', 'Foreign Cargo on the Quay',
            'Goods bound for other countries landed at Lhesk and sent on by road.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.01}, ('economy', 'logistics')),
    IdeaDef('home_cargo', 'Slavian Ships Never Wait',
            'Berths go first to the republic\'s own fuel, food, steel and parts.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('security', 'logistics')),
    IdeaDef('coast_watchers', 'Radios in the Fishing Fleet',
            'Fishing crews and sailors report sightings at sea for a small fee.',
            {'air_detection': 0.05, 'naval_coordination': 0.03}, ('fishing', 'communications')),
    IdeaDef('mates_classes', 'Evening Classes at the Quay',
            'Local sailors qualify as mates and masters without going abroad.',
            {'navy_org_factor': 0.04, 'naval_speed_factor': 0.02}, ('training', 'navy')),
    IdeaDef('dues_formula', 'Dues Posted on the Door',
            'Harbour dues follow a published formula of tonnage, berth time and cargo class.',
            {'political_power_factor': 0.05, 'naval_coordination': 0.02}, ('scales', 'navy')),
    # the two formations
    IdeaDef('territorial_muster', 'Two Formations Counted',
            'Every rifle, truck and reservist card of the army is on one muster roll.',
            {'army_core_defence_factor': 0.04, 'war_support_factor': 0.02}, ('training', 'security')),
    IdeaDef('street_schools', 'Mock Streets by the Halls',
            'Battalions rotate through a training block of houses, cellars and courtyards.',
            {'army_defence_factor': 0.04, 'experience_gain_army_factor': 0.05}, ('training', 'civil')),
    IdeaDef('block_defence', 'A Fortress of Streets',
            'Prepared positions in cellars, courtyards and the halls themselves.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.05}, ('security', 'shelter')),
    IdeaDef('approach_screen', 'Light Screens Forward',
            'Screens on the western hills, northern foothills and eastern road.',
            {'army_speed_factor': 0.06, 'planning_speed': 0.08}, ('logistics', 'security')),
    IdeaDef('household_levy', 'One Defender per Household',
            'Every household provides a trained adult to a weekend company.',
            {'training_time_army_factor': -0.12, 'surrender_limit': 0.05}, ('civil', 'training')),
    IdeaDef('linked_cellars', 'Passages Under the Streets',
            'Cellars knocked through so defenders can move below ground.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.08, 'attrition': -0.05}, ('shelter', 'tools')),
    IdeaDef('crossroads_reserve', 'Trucks Loaded at the Crossroads',
            'A central reserve kept fuelled and loaded, able to reach any approach in time.',
            {'army_speed_factor': 0.08, 'planning_speed': 0.10, 'army_org_factor': 0.04}, ('logistics', 'command')),
    IdeaDef('neighbourhood_companies', 'Companies Drawn by Street',
            'Neighbours drill together, with elected sergeants and a known armoury.',
            {'training_time_army_factor': -0.15, 'surrender_limit': 0.08, 'stability_factor': 0.02}, ('assembly', 'security')),
    IdeaDef('officer_school', 'Officers Trained for Mud and Streets',
            'A harbour school teaches command for the republic\'s own ground.',
            {'experience_gain_army_factor': 0.08, 'army_org_factor': 0.04}, ('command', 'training')),
    IdeaDef('staff_college', 'Planners for the Board',
            'Officers trained in budgets and administration as well as operations.',
            {'planning_speed': 0.08, 'experience_gain_army_factor': 0.05}, ('document', 'command')),
    # the air guard
    IdeaDef('air_guard', 'Sixteen Airframes on One Field',
            'Twelve fighters and four in reserve watch the sky over a single province.',
            {'air_superiority_efficiency': 0.03, 'experience_gain_air_factor': 0.05}, ('air', 'document')),
    IdeaDef('alert_pairs', 'Two Fighters Always Armed',
            'A pair of fighters waits at the runway end, crewed, at every hour.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'security')),
    IdeaDef('flying_school', 'Pilots Trained at Home',
            'Training hours come before alert hours while a flying school fills the cockpits.',
            {'experience_gain_air_factor': 0.12, 'air_mission_efficiency': 0.03}, ('training', 'air')),
    IdeaDef('coast_strips', 'Road Strips and Hidden Bowsers',
            'Straight stretches of the coast road serve as emergency runways.',
            {'air_mission_efficiency': 0.05, 'static_anti_air_damage_factor': 0.05}, ('runway', 'logistics')),
    IdeaDef('revetments', 'Earth Walls Round the Fighters',
            'Blast walls and nets protect every parking place on the field.',
            {'static_anti_air_damage_factor': 0.08, 'air_defence_factor': 0.05}, ('shelter', 'air')),
    IdeaDef('airframe_shop', 'Spares from the Airframe Shop',
            'Panels, ribs and simple spares made from Slavian aluminium.',
            {'air_mission_efficiency': 0.04, 'production_factory_max_efficiency_factor': 0.02}, ('tools', 'air')),
    IdeaDef('aggressor_contract', 'Contract Aggressors Overhead',
            'Hired instructors fly against the guard\'s pilots in exercises.',
            {'experience_gain_air_factor': 0.10, 'political_power_gain': -0.05}, ('air', 'medal')),
    # the frontiers
    IdeaDef('frontier_office', 'Survey of the Two Frontiers',
            'Every road, track and post on the Slavian side of both frontiers is mapped.',
            {'stability_factor': 0.01, 'army_core_defence_factor': 0.03}, ('diplomacy', 'document')),
    IdeaDef('hill_posts', 'Posts on the Shepherd Tracks',
            'Staffed posts on the western tracks count who crosses and when.',
            {'army_core_defence_factor': 0.04, 'stability_factor': 0.01}, ('security', 'peace')),
    IdeaDef('flood_gauges', 'Gauges Along the Foothills',
            'Stream gauges and a telephone line warn the city of floods from the mountains.',
            {'stability_factor': 0.02, 'planning_speed': 0.05}, ('telescope', 'civil')),
    IdeaDef('east_crossing', 'A Lit Crossing on the Plain',
            'The Slavian end of the eastern road is paved, lit and staffed.',
            {'consumer_goods_factor': -0.02, 'army_speed_factor': 0.03}, ('logistics', 'diplomacy')),
    IdeaDef('no_bloc', 'Ready, and Allied to Nobody',
            'No alliance, no foreign troops and no territory lent to any war.',
            {'army_core_defence_factor': 0.08, 'political_power_gain': 0.05}, ('peace', 'security')),
    IdeaDef('open_gates', 'Crossings Open to Traders',
            'Minimal paperwork for anyone crossing with goods or looking for work.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('economy', 'diplomacy')),
    IdeaDef('crossing_permits', 'Paper for Every Journey',
            'Informal paths closed; every crossing needs a permit checked both ways.',
            {'stability_factor': 0.03, 'army_core_defence_factor': 0.04, 'consumer_goods_factor': 0.02}, ('document', 'security')),
    # the asteroid
    IdeaDef('impact_committee', 'The Impact Committee Sits Daily',
            'Ministries plan together for an impact nobody can yet place.',
            {'stability_factor': 0.01, 'air_detection': 0.05}, ('meteor', 'telescope')),
    IdeaDef('deep_shelters', 'Pumped Shelters in Wet Ground',
            'Deep shelters under the old quarter, linked to the cellars and stocked with water.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.04}, ('shelter', 'meteor')),
    IdeaDef('evacuation_berths', 'Ships Held for the Worst Case',
            'Berths, fuel and boarding lists reserved for moving people out to sea.',
            {'stability_factor': 0.03, 'naval_coordination': 0.04}, ('navy', 'refugees')),
    IdeaDef('corridor_lists', 'A Request Left Open',
            'The republic has asked its neighbours about shelter overland and awaits any answer.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('refugees', 'diplomacy')),
    IdeaDef('shelter_pumps', 'A Standing Pump Service',
            'Spare engines, fuel and crews keep every shelter dry through the wet season.',
            {'static_anti_air_damage_factor': 0.12, 'stability_factor': 0.05}, ('tools', 'shelter')),
    IdeaDef('boarding_drills', 'Every Family Knows Its Berth',
            'Wards rehearse the walk to their assigned berths with one bag each.',
            {'stability_factor': 0.05, 'naval_coordination': 0.05}, ('refugees', 'navy')),
    IdeaDef('route_lists', 'Routes and Columns by Household',
            'Every household holds a route, a vehicle and an assembly point in case an offer comes.',
            {'stability_factor': 0.04, 'planning_speed': 0.05, 'political_power_gain': 0.05}, ('document', 'refugees')),
    IdeaDef('impact_stockpiles', 'Water, Grain and Medicine Laid By',
            'Emergency stocks bought for the years before the asteroid arrives.',
            {'stability_factor': 0.04, 'supply_consumption_factor': -0.03}, ('meteor', 'logistics')),
    IdeaDef('sky_log', 'A Log of the Night Sky',
            'Volunteer watchers record bright objects and pass genuine meteors abroad.',
            {'air_detection': 0.08, 'research_speed_factor': 0.02}, ('telescope', 'fishing')),
    # distant wars
    IdeaDef('war_premium', 'Premiums on Every Slavian Hull',
            'Fuel, freight and insurance all cost more while the Belkan War lasts.',
            {'consumer_goods_factor': 0.03, 'stability_factor': -0.02}, ('communications', 'diplomacy')),
    IdeaDef('wartime_licences', 'Orders Paid in Advance',
            'Licensed buyers, including parties to the war, fill the order books.',
            {'production_speed_arms_factory_factor': 0.08, 'stability_factor': -0.02}, ('missile', 'economy')),
    IdeaDef('arms_shut', 'No Rifles Leave for the War',
            'Fuel and food may sail; weapons may not, to any party at war.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.01}, ('peace', 'scales')),
    IdeaDef('belkan_orders', 'Contracts from Belkan Agents',
            'Civil orders for steel, trucks and spares from a victorious Belka.',
            {'industrial_capacity_factory': 0.04, 'consumer_goods_factor': -0.02}, ('diplomacy', 'industry')),
    IdeaDef('belkan_engineers', 'Vetted Engineers from Belka',
            'A few Belkan technicians on contract in the halls and the air guard.',
            {'research_speed_factor': 0.04, 'experience_gain_air_factor': 0.03}, ('science', 'diplomacy')),
    IdeaDef('usean_contracts', 'Overtime from the Usean War',
            'Licensed orders connected with the war in Usea, certified at the quay.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'economy')),
    IdeaDef('relief_cargo', 'Convoys for Relief Only',
            'Food, medicine and building materials for civilian agencies in Usea.',
            {'stability_factor': 0.04, 'naval_coordination': 0.02}, ('medical', 'navy')),
    # the new century
    IdeaDef('second_count', 'Two Counts Side by Side',
            'Figures for 1991 and 2001 compared street by street and hall by hall.',
            {'research_speed_factor': 0.03, 'stability_factor': 0.02}, ('document', 'civil')),
    IdeaDef('apprentice_scheme', 'Three Years at Lathe and Desk',
            'Apprentices split their time between the halls and a technical school.',
            {'research_speed_factor': 0.02, 'production_factory_efficiency_gain_factor': 0.03}, ('training', 'industry')),
    IdeaDef('surplus_budgets', 'Three Budgets in Surplus',
            'Wards, halls and the defence staff receive less while the debt is paid down.',
            {'political_power_factor': 0.05, 'stability_factor': -0.02, 'consumer_goods_factor': 0.02}, ('economy', 'scales')),
    IdeaDef('hall_labs', 'A Research Room in Every Hall',
            'Engineers and apprentices improve the products and processes of their own hall.',
            {'research_speed_factor': 0.05}, ('science', 'industry')),
    # decisions
    IdeaDef('canteen_week', 'A Week of Canteen Hearings',
            'Ministers answer the night and day shifts in person.',
            {'stability_factor': 0.02}, ('assembly', 'civil')),
    IdeaDef('range_fortnight', 'A Fortnight on the Ranges',
            'Battalions fire their annual courses on the coastal ranges.',
            {'army_org_factor': 0.04}, ('training', 'command')),
    IdeaDef('scramble_week', 'Scrambles at Unannounced Hours',
            'The air guard launches against surprise drills set by the radar crews.',
            {'air_superiority_efficiency': 0.04}, ('air', 'radar')),
    IdeaDef('drains_flushed', 'Drains Cleared for the Rains',
            'Every storm drain flushed and inspected before the wet season.',
            {'production_speed_infrastructure_factor': 0.10, 'stability_factor': 0.01}, ('tools', 'civil')),
    IdeaDef('fuel_release', 'Silo Fuel at Fixed Prices',
            'Fuel from the silo sold to households and lorries at a fixed price.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'logistics')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('federal_council', 'Federal Council of the Slavian Federation',
           'A council chosen by the chamber elected on the overdue ballot, governing collectively and answering to that '
           'chamber for every budget and appointment. Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
    Office('managers_board', 'Board of Managers of the Republic',
           'A board of the directors of the arms halls, civil works, harbour and banks, governing the republic as one budget '
           'with elections suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('works_council', 'Federative Council of the Works',
           'A council of delegates elected by the halls, civil works and docks, governing the Slavian Federative Socialist '
           'Republic and answerable to the works councils. Provisional gameplay office with no named holder.',
           'communism', 'democratic_socialism'),
    Office('defence_board', 'Defence Board of the Slavian Republic',
           'A board of senior officers governing under an ordinance of defence, with parties suspended and civil ministries '
           'taking their priorities from the general staff. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('overdue_ballot', 'The Calendar in the Cabinet Room', (
        "A printed electoral calendar hangs in the Administration's cabinet room, issued in 1987 and never replaced. Someone "
        "has ringed the ninth of November 1991 in red ink. Under the inherited four-year rule, that is when the Slavian "
        "Republic should next vote. Nobody in the room admits to the ink, and nobody has taken the calendar off its nail.",
        "Since that last vote the Administration has governed by ordinary decree, and most of Lhesk has let it. Seven in ten "
        "voters still back the non-aligned label it governs under. Almost a quarter vote communist, most of them on the floors "
        "of the arms halls and the docks. A handful follow the nationalists and hardly anyone the democrats. Public order is "
        "brittle, yet readiness to fight for the city is very high, a mixture each minister explains in a different way.",
        "Nothing has to be settled today, but the date is only months away and editors can read a calendar too. The cabinet "
        "can extend its own mandate by quiet decree, announce a public review of how the republic should be governed, or "
        "send officials into the shift-change canteens to ask the workforce directly. The last course will begin an "
        "argument the Administration cannot finish on its own.",
    ), (
        Option('Extend the mandate by decree.', (PP(35), Stability(-0.02))),
        Option('Announce a public review.', (Stability(0.02), PP(-10))),
        Option('Send officials to the canteens.', (PP(-5), Event('canteen_night', 10))),
    ), picture=0),
    EventDef('canteen_night', 'Questions Until Dawn', (
        "The officials sent to the canteens expected an hour of polite questions. At the largest arms hall the night shift "
        "keeps them until sunrise. Workers climb onto benches to speak, the kitchen staff stop serving to listen, and a "
        "delegate reads out demands written on the back of a production chart: published wages, safe ventilation, a vote on "
        "the overdue ballot and a seat for the halls in whatever government comes next.",
        "Not everyone in the room agrees. Older foremen want the managers left alone to run the halls as they always have. "
        "Younger fitters want the councils to take the halls over outright. A few reservists say the city should put its "
        "defences in order before it argues about anything else at all. The officials write every word down, and by morning "
        "their notebooks hold the four quarrels the republic will spend the coming years having.",
        "The managers have already heard what happened and want the notebooks treated as confidential. The delegates want "
        "them printed in full. The Administration now owns a night it neither planned nor can undo, and must "
        "choose between the two demands, knowing that the halls will judge its answer long before any minister has finished explaining it.",
    ), (
        Option('Print the notebooks in full.', (Stability(0.02), PP(-15))),
        Option('Keep the notebooks for the cabinet.', (PP(30), Stability(-0.02))),
    ), picture=0),
    EventDef('one_city', 'A Survey Walked in One Season', (
        "The survey teams finish their walk of Slavia in a single season, something few countries anywhere could say. They "
        "have measured every street, counted every flat, tested every well and lifted every drain cover in the republic. On "
        "every sheet they drew, the republic, the province and the city of Lhesk turn out to be one place, running from the "
        "foot of the western hills to the harbour on the southern shore.",
        "The report is blunt. The old drains were laid for a smaller city and overflow every wet season, and the plain stays "
        "muddy in every month of the year. Water pressure collapses on summer afternoons, when the heat reaches the high "
        "thirties and no rain has fallen for weeks. Arms workers live far from the halls and lose hours each week on "
        "crowded buses. Market streets have grown up without licences, inspectors or drains of their own.",
        "The ministers now hold a complete picture of their country, and so do the newspapers, which received copies through "
        "an error nobody will own. The government must decide who will act on the findings: committees elected in each "
        "ward, which would be slow and popular, or one office with authority over every street, which would be quick and "
        "answerable to nobody close at hand.",
    ), (
        Option('Promise the wards a say.', (Stability(0.02), PP(-10))),
        Option('Promise one office for the works.', (PP(25), Stability(-0.01))),
    ), picture=0),
    EventDef('arms_halls', 'Clipboards in the Arms Halls', (
        "The inventory teams walk the five arms halls with clipboards and a camera, and the managers walk beside them the "
        "whole way. After the harbour sheds, the halls are the largest buildings in Lhesk, and in most families someone works "
        "a shift in one. Two civil works across the city make nearly everything else the republic produces, from rolled "
        "plate to tram spares, and neither has seen new machines in years.",
        "Every building plot zoned for industry in the province is taken, and there is nowhere else to put another, because "
        "the province is the whole country. Whatever the republic wants from its industry in the next decade must come from "
        "what these seven buildings make and how well they make it. The teams find idle lathes, presses booked twice over "
        "and an export order book that leans on a handful of foreign buyers.",
        "The managers want the findings treated as commercial secrets. The works delegates want them pinned to the canteen "
        "walls. The defence staff asks only for a list of what the halls could turn out in a month if the city were "
        "threatened. The cabinet must choose who reads the inventory first, and that choice will colour every argument "
        "about the halls that follows.",
    ), (
        Option('Pin the findings in the canteens.', (Stability(0.01), Research('industry', 0.5, 1))),
        Option('Brief the managers in confidence.', (PP(30), WarSupport(0.01))),
        Option('Hand the defence staff the first copy.', (WarSupport(0.03), XP('army', 10))),
    ), picture=1),
    EventDef('quay_morning', 'One Counter at Six in the Morning', (
        "At six in the morning the new harbour office opens its doors for the first time, and a line of ship agents is "
        "already waiting on the quay. Until now each of them dealt with four ministries for berths, pilots, dues and the "
        "convoy list, and each ministry kept its own hours and its own forms. The harbour office has one counter, one ledger "
        "and a clock on the wall. By noon the line is longer than when it started.",
        "The quay is long and the naval base is small. There are no warships and nobody in the republic is asking for any. "
        "What the harbour handles is cargo: fuel for the silo, food, steel plate, machine parts and the crates the arms halls "
        "sell abroad. Sixty convoys sail under Slavian registration. Silt washed off the plain narrows the channel every "
        "spring, and the larger ships already wait outside for the tide.",
        "The office must settle its first priority. It can clear the backlog by working through the night, which exhausts "
        "the clerks and pleases the agents, or close the counter for a week to write proper rules, which angers everyone now "
        "and spares them later. Either way, the harbour has a single address for the first time, and every complaint will "
        "now arrive at it.",
    ), (
        Option('Work through the night.', (Stability(0.01), XP('navy', 10))),
        Option('Close for a week and write the rules.', (PP(25), Stability(-0.01))),
    ), picture=2),
    EventDef('muster_day', 'The Whole Army on One Field', (
        "Both infantry formations of the Slavian army stand on the parade ground together for the first time in years: four "
        "battalions in each, an engineer company with each formation and trucks parked in rows behind them. The entire army "
        "of the republic fits on one field. Families crowd the railings, the harbour sirens sound at noon, and behind the "
        "ceremony clerks count every rifle, helmet and reservist card.",
        "The count describes a people that expects to defend itself and has thought less about how. Nine in ten citizens "
        "tell pollsters they would fight for Lhesk if it came to that. The formations still train in open fields, though any "
        "real fighting would be in streets and cellars. Their trucks sink into the plain every wet season, and the engineers "
        "have plans of the city but none of the three land approaches beyond it.",
        "The defence staff wants the muster repeated every year as a public show of readiness. The treasury answers that a "
        "full muster closes the harbour road for a day and costs a week of hall output while reservists queue for their "
        "cards. The Administration must decide whether readiness is something Slavia displays to itself and its neighbours, "
        "or something it simply keeps.",
    ), (
        Option('Make the muster a yearly holiday.', (WarSupport(0.03), Stability(0.01), PP(-15))),
        Option('Muster quietly, one battalion at a time.', (XP('army', 15), PP(10))),
    ), picture=0),
    EventDef('three_frontiers', 'A Thin Folder of Frontiers', (
        "The frontier office delivers its survey in a single folder, and the ministers notice at once how thin it is. Valka "
        "lies to the west behind a line of hills crossed by shepherds' tracks. Seterano's mountains rise along the whole "
        "north, and Seterano's plain meets Slavia again in the east along a stretch so short that a lorry is across it in "
        "minutes. To the south there is only the sea.",
        "Every one of these frontiers is quiet, and no file in the office records a quarrel over any of them. Each is also "
        "poorly known on the Slavian side. Valka is governed under its democratic label with elections suspended, before an electorate "
        "split almost evenly between non-aligned and nationalist camps. Seterano is larger, with frontiers of its own to "
        "watch. Neither has asked the republic for anything, and the republic has asked nothing of either.",
        "Nothing on the ground is altered by the folder. What it reveals is how few doors the republic has: two land neighbours, one easy "
        "road, one harbour. Before choosing whether to stand apart, open those doors or watch them closely, the government "
        "must decide what to tell the shepherds and drivers who cross the hills every week and have never once been asked "
        "for a paper.",
    ), (
        Option('Post notices on every track.', (Stability(0.02), PP(-10))),
        Option('Say nothing until the posts are built.', (PP(20), WarSupport(0.01))),
    ), picture=0),
    EventDef('asteroid_news', 'Nowhere Inland to Go', (
        "In December 1994 the International Astronomical Union warns that an asteroid named Ulysses is heading near enough to "
        "the planet that a collision cannot be ruled out. The warning reaches Lhesk on the late radio news. Before dawn the "
        "Administration has convened an impact committee, and its first question is one most countries answer without "
        "thinking: if the worst is forecast, where will the people go?",
        "Slavia has no inland. The republic is a single province, a city on a plain between hills, mountains and the sea. "
        "Every evacuation plan the committee finds in foreign handbooks begins by moving families away from the coast to "
        "towns further inside the country. There are no such towns. Any refuge must be underground, at sea or across a "
        "frontier, and each of those depends on something the committee does not have: concrete, ships or a neighbour's "
        "consent.",
        "Nobody knows where fragments might fall, and it may be years before anybody does. The committee could say so plainly "
        "and risk alarm, or work quietly until it has a plan worth announcing. Shops on the harbour road are already selling "
        "out of bottled water, and the ward offices are taking calls from families who want to know whether they ought to "
        "leave the republic now.",
    ), (
        Option('Tell the city the plain truth.', (Stability(-0.02), WarSupport(0.03), Research('construction_tech', 0.5, 1))),
        Option('Work quietly until there is a plan.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, Official Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; the Slavian response '
                'is gameplay', picture=2),
    EventDef('roche_night', 'A Long Night of Radios', (
        "On 8 July 1999 Ulysses comes inside the Roche limit, the distance within which the pull of the planet can tear a "
        "body apart. In Lhesk the impact committee has been awake since the previous afternoon. Shelters, berths and route "
        "lists stand ready, the harbour road is closed to lorries, and the air guard's radar crews watch screens that were "
        "built to find aircraft rather than anything falling from far higher up.",
        "The city listens to the radio in courtyards and on flat roofs, because July nights are too hot for indoors. Reports "
        "from abroad are confused and contradict each other from one bulletin to the next. Some families have gone down to "
        "the shelters or out to the quay without being told to; most have stayed at home. The committee's own instructions "
        "say to act only on confirmed information, and by midnight it has very little.",
        "Whatever the night brings, the committee must issue a statement by morning. It can set out everything it did and "
        "why, mistakes included, or publish a short notice that the city is calm and the plans worked as intended. Readers "
        "will compare either version with what they saw from their own windows. The committee has two drafts on the table "
        "and one hour before the presses run.",
    ), (
        Option('Publish the full account.', (Stability(0.02), PP(-15))),
        Option('Issue the short notice.', (PP(25), Stability(-0.01))),
    ), citation='date anchor only, Official Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no damage in Slavia is '
                'claimed or denied', picture=2),
    EventDef('belkan_war_news', 'Premiums Before Headlines', (
        "The Belkan War begins in late March 1995, a long way from Lhesk. The first the republic hears of it is a news bulletin; "
        "the second is a telephone call from a shipping insurer raising every premium on the Slavian register. By the end "
        "of the week fuel costs more at the silo, freight rates have jumped, and foreign buyers are asking whether the arms "
        "halls could fill a large order quickly.",
        "Slavia has no part in the war and no frontier anywhere near it. Most of the city follows the news with the uneasy "
        "distance of people who have watched other countries fight on television before. The arms workers follow it more "
        "closely, because orders mean overtime. The defence staff follows it most closely of all, studying what the fighting "
        "shows about air power over cities and how long small countries can stay out of the way.",
        "The Administration must decide how the republic will speak about the war. A plain statement of neutrality now would "
        "steady the markets and disappoint the halls. A statement that says only that Slavia is watching would keep every "
        "option open and every buyer interested. Whichever is chosen will be read abroad as the republic's position for as "
        "long as the fighting lasts.",
    ), (
        Option('Declare neutrality at once.', (Stability(0.02), PP(10))),
        Option('Say only that Slavia is watching.', (PP(25), WarSupport(0.02))),
    ), citation='date anchor only, Official Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Slavian response '
                'is gameplay', picture=1),
    EventDef('usean_war', 'The Usean War Reaches the Quay', (
        "In the summer of 2003 Erusea seizes the Stonehenge railguns in San Salvacion, and in August the FCU forms the ISAF "
        "to oppose it. War spreads across Usea. In Lhesk the harbour office hears of it from the insurers before the "
        "newspapers can explain it. Premiums on every Slavian convoy rise overnight, and some charterers cancel voyages "
        "toward Usean waters altogether.",
        "The war is far away and the republic is not part of it. Its effects arrive by sea and by telephone: dearer fuel at "
        "the silo, buyers asking about rifles and trucks, families with relatives in Usean ports queuing at the harbour "
        "office for news. The halls remember the Belkan War and what they decided then. So do the buyers, who know exactly "
        "what kind of seller Slavia turned out to be eight years ago.",
        "The cabinet meets to set a course for a war that may last for years. Some ministers want the convoys kept out of "
        "Usean waters entirely until the fighting ends. Others point out that the convoys are how the republic earns its "
        "living, and that masters know their own risks. Before any policy is written, the cabinet must decide what it will "
        "tell the crews.",
    ), (
        Option('Keep the convoys out of the war zone.', (Stability(0.02), PP(-10))),
        Option('Let each master decide with full information.', (XP('navy', 15), Stability(-0.01))),
    ), citation='date anchors only, Official Chronicle rows 2003 / SUMMER and 2003 / 08.22 in tools/lore/chronicle.json; the '
                'Slavian response is gameplay', picture=2),
    EventDef('millennium_review', 'One Volume, Two Decades of Figures', (
        "The second count of the republic is finished, and for the first time Slavia can lay two complete pictures of itself "
        "side by side, taken ten years apart. The clerks have counted the same streets, flats, halls and berths and bound the "
        "figures in one heavy volume. A city-state has nowhere to hide its numbers, and this volume hides none of them.",
        "Some lines have improved and some have not moved at all. The government that emerged from the quarrel over the "
        "overdue ballot has had a decade to show what it can do. The halls still employ most working adults. The harbour "
        "handles more cargo or less, depending on choices made years ago. Young Slavians still leave for work abroad, and "
        "most who stay still begin their working lives at sixteen in an arms hall.",
        "The ministers must decide how the volume reaches the public. Sold at the kiosks like a newspaper, it would "
        "arm the opposition, the councils and every foreign correspondent at once. Sent first to the wards for comment, it "
        "would arrive later with the city's replies bound in, and be called delayed by everyone in a hurry. Either way, the "
        "figures will frame the next argument about the republic.",
    ), (
        Option('Sell the volume at every kiosk.', (Stability(0.02), PP(-20))),
        Option('Send it to the wards first.', (PP(30), Stability(-0.02))),
    ), picture=1),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('adm', 'The Ballot Due in November', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_due', 'The Calendar Runs Out',
          "The last national vote in Slavia was held on 9 November 1987, and the inherited four-year calendar puts the next one "
          "in November 1991. The National Administration has governed without calling it and without saying why. Before "
          "anyone argues about the answer, the Administration must admit in public that the question exists, and that "
          "admission alone costs it authority.",
          ('ballot', 'document'), reward=(Idea('caretaker_mandate'), Event('overdue_ballot'))),
    Focus('adm_canteens', 'Hearings in the Works Canteens',
          "Most Slavian voters work a shift in an arms hall, a civil works or the harbour, so the Administration sends officials "
          "to the canteens at shift change. They answer questions over the noise of the lunch queue and write down every "
          "complaint. The hearings are cheap and humbling, and they reach people no party office has ever bothered to visit.",
          ('assembly', 'industry'), after=('adm_due',), reward=(Idea('canteen_forums'),)),
    Focus('adm_rolls', 'Correct the Electoral Rolls',
          "The rolls compiled for 1987 still list the dead, the emigrated and families who moved across the city years ago. A "
          "team of clerks checks every block against the housing and ration registers. Whatever form of government follows, it "
          "will need to know who lives in the republic. The clerks also learn which blocks stopped answering letters long ago.",
          ('document', 'civil'), after=('adm_due',), reward=(Flag('rolls_corrected'), Stability(0.02))),
    Focus('adm_four_answers', 'Four Answers on the Table',
          "By the end of the hearings four answers have hardened. Some want the overdue ballot held and a federation built on "
          "it. The managers of the halls and the harbour want to govern as a board. The works delegates want the councils to "
          "take the keys. The defence staff, trusted by a city that expects to fight, offers itself. Only one answer can win.",
          ('scales', 'assembly'), after=('adm_canteens', 'adm_rolls'),
          reward=(PP(30), Tooltip('Opens four constitutional paths; only one can be taken.'))),
    Focus('adm_ballot_path', 'Hold the Overdue Ballot',
          "The first answer is the simplest to explain and the hardest to carry out: hold the vote that fell due in November, on "
          "rolls the clerks have corrected, and let a chamber of the Slavian Federation form the government. Only a sliver of "
          "voters backs the democratic party today, so the Administration would hand power to institutions that barely exist.",
          ('ballot', 'assembly'), after=('adm_four_answers',),
          exclusive=('adm_board_path', 'adm_works_path', 'adm_defence_path'),
          reward=(SwapIdea('caretaker_mandate', 'ballot_calendar'),)),
    Focus('adm_board_path', 'The Managers Offer a Board',
          "Directors of the five arms halls, the two civil works, the harbour and the banks propose to govern the republic as "
          "one board, setting budgets the way a company does and choosing ministers for competence. Output would rise and "
          "decisions would come quickly. Ordinary Slavians would see their country run by the people who already sign their "
          "wage packets.",
          ('economy', 'command'), after=('adm_four_answers',),
          exclusive=('adm_ballot_path', 'adm_works_path', 'adm_defence_path'),
          reward=(SwapIdea('caretaker_mandate', 'managers_compact'),)),
    Focus('adm_works_path', 'The Councils Ask for the Keys',
          "Close to a quarter of the city votes communist, and that strength is packed onto the shop floors of the arms halls. "
          "Its delegates propose a federation of works councils, each hall and dock electing its share of one national council. "
          "Workers would hold real power for the first time. The managers and the defence staff would lose theirs, and are "
          "already saying so.",
          ('assembly', 'tools'), after=('adm_four_answers',),
          exclusive=('adm_ballot_path', 'adm_board_path', 'adm_defence_path'),
          reward=(SwapIdea('caretaker_mandate', 'works_delegates'),)),
    Focus('adm_defence_path', 'The General Staff Offers Itself',
          "Nine in ten Slavians say they would defend the city if it came to that, and the defence staff reads the figure as a "
          "mandate. It offers a board of senior officers to govern under an ordinance of defence, with civil ministries taking "
          "their priorities from the general staff. The city would be ready for anything except argument, which it would no "
          "longer be allowed.",
          ('security', 'command'), after=('adm_four_answers',),
          exclusive=('adm_ballot_path', 'adm_board_path', 'adm_works_path'),
          reward=(SwapIdea('caretaker_mandate', 'defence_ordinance'),)),
    Focus('adm_federal_council', 'A Council Chosen by the Chamber',
          "The chamber elected on the overdue ballot chooses a federal council to govern collectively, and the Slavian "
          "Federation takes the place of the old republic. The change runs through the office, not a person. The council "
          "answers to the chamber for every budget and appointment, and inherits an arms economy and a defence staff it has "
          "never once commanded.",
          ('ballot', 'scales'), after=('adm_ballot_path',), cost=10,
          exclusive=('adm_managers_board', 'adm_works_federation', 'adm_defence_board'),
          reward=(Regime('federal_council'), Flag('path_federal'))),
    Focus('adm_managers_board', 'Install the Board of Managers',
          "The board of managers takes the seals of government and the Administration's clerks become its staff. Elections stay "
          "suspended while the board publishes quarterly accounts in their place. It is a government that knows exactly what "
          "every hall produces and very little about what every household needs. The office governs collectively; no single "
          "person holds it.",
          ('economy', 'document'), after=('adm_board_path',), cost=10,
          exclusive=('adm_federal_council', 'adm_works_federation', 'adm_defence_board'),
          reward=(Regime('managers_board'), Flag('path_board'))),
    Focus('adm_works_federation', 'Proclaim the Federation of the Works',
          "Delegates of the halls, the civil works and the docks convene as a federative council and proclaim the Slavian "
          "Federative Socialist Republic. Managers may stay on as employees of the councils if they accept the terms. The "
          "council governs collectively under rules of its own making. Production meetings replace board meetings, and the "
          "very first of them runs past midnight.",
          ('assembly', 'industry'), after=('adm_works_path',), cost=10,
          exclusive=('adm_federal_council', 'adm_managers_board', 'adm_defence_board'),
          reward=(Regime('works_council'), Flag('path_works'))),
    Focus('adm_defence_board', 'Swear In the Defence Board',
          "A board of senior officers takes its oath before both infantry formations on the parade ground and assumes "
          "executive power under the ordinance of defence. Parties are suspended for a duration the ordinance does not define. "
          "The board governs collectively and names no chief. Readiness is now the republic's constitution, and that "
          "constitution reads like a staff manual.",
          ('security', 'medal'), after=('adm_defence_path',), cost=10,
          exclusive=('adm_federal_council', 'adm_managers_board', 'adm_works_federation'),
          reward=(Regime('defence_board'), Flag('path_defence'))),
    Focus('adm_two_readings', 'Every Law Read Twice',
          "The federal chamber adopts one simple rule: each bill is read twice, a month apart, and printed in the newspapers "
          "between the readings. Laws pass slowly and lobbyists get a month to complain. In return nobody in Lhesk can claim a "
          "law was sprung on them, which matters in a republic that had not voted since 1987.",
          ('document', 'assembly'), after=('adm_federal_council',),
          exclusive=('adm_board_wall', 'adm_open_books', 'adm_reserve_roll'),
          reward=(SwapIdea('ballot_calendar', 'federal_law'),)),
    Focus('adm_board_wall', 'Targets on the Board Room Wall',
          "Each director's targets for output, cost and harbour tonnage go up on the board room wall and into print every "
          "month. Directors who miss them twice are replaced. The method rewards whatever can be counted and ignores whatever "
          "cannot, so housing and schools fall behind the halls. The managers call that focus; their critics call it neglect.",
          ('economy', 'scales'), after=('adm_managers_board',),
          exclusive=('adm_two_readings', 'adm_open_books', 'adm_reserve_roll'),
          reward=(SwapIdea('managers_compact', 'board_targets'),)),
    Focus('adm_open_books', 'Open the Books of Every Hall',
          "Every hall, works and dock publishes its accounts to the people who work in it, line by line, including what the "
          "former managers were paid. Delegates spend weeks learning to read a balance sheet. Waste falls once everyone can see "
          "it, and so does the comfort of those who used to hide it. Foreign creditors politely ask for copies as well.",
          ('document', 'tools'), after=('adm_works_federation',),
          exclusive=('adm_two_readings', 'adm_board_wall', 'adm_reserve_roll'),
          reward=(SwapIdea('works_delegates', 'open_books'),)),
    Focus('adm_reserve_roll', 'Every Adult on the Reserve Roll',
          "The board enters every adult in the republic on a single reserve roll, with an assignment, an assembly point and a "
          "yearly drill. In a country of one province the roll is short enough to keep current by hand. It turns the city's "
          "eagerness to fight into organised readiness, at the price of a population that always feels half on duty.",
          ('training', 'security'), after=('adm_defence_board',),
          exclusive=('adm_two_readings', 'adm_board_wall', 'adm_open_books'),
          reward=(SwapIdea('defence_ordinance', 'reserve_roll'),)),
    Focus('adm_settled', 'The Settlement in Print',
          "Whichever answer prevailed, the government prints a short text explaining who governs, how they are chosen and how "
          "the arrangement may be changed. Copies sell at every kiosk in the city for the price of a newspaper. It ends years of "
          "rumour about what the Administration intended, and hands the next quarrel a document to argue over.",
          ('document', 'peace'), after_any=('adm_two_readings', 'adm_board_wall', 'adm_open_books', 'adm_reserve_roll'),
          reward=(Idea('settlement_text'), Stability(0.03))),
))

CITY = Branch('city', 'A Republic of One Province', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('city_ledger', 'Survey Every Street of Lhesk',
          "Slavia is a single province, and that province is the city of Lhesk and the plain around it. There are no regions to "
          "balance, only streets, blocks, drains and wells, and nobody has counted them in a generation. A survey team walks the "
          "whole republic in one season. Every complaint the canteens raise can now be checked against a map.",
          ('document', 'civil'), reward=(Idea('street_ledger'), Event('one_city'))),
    Focus('city_drains', 'Storm Drains Before the Rains',
          "From January to May heavy rain sweeps in off the sea, and the plain never properly dries; mud is a fact of life in "
          "every month. The worst streets flood each spring and lorries bog down outside the arms halls. Clearing and widening "
          "the storm drains is dull engineering that every household notices, and it costs a season of torn-up roads.",
          ('tools', 'civil'), after=('city_ledger',), reward=(Build('infrastructure', 1, 0),)),
    Focus('city_cisterns', 'Cisterns for the Dry Months',
          "Between June and September the rain stops and the afternoon heat climbs into the high thirties. The city mains lose "
          "pressure every afternoon and the upper floors run dry. Rooftop and street cisterns, filled in the wet season and "
          "drawn down through the summer, cost little and need constant inspection. The alternative is a summer of queues at "
          "the standpipes.",
          ('civil', 'shelter'), after=('city_ledger',), reward=(Idea('summer_cisterns'),)),
    Focus('city_flats', 'Flats Within Walking Distance',
          "Workers in the arms halls live in crowded blocks across the city and lose an hour each way on buses that crawl "
          "through the mud. New flats on empty lots beside the halls shorten the journey and ease the crowding. The lots belong "
          "to the halls, which were keeping them for an expansion that the full slot count says will never come.",
          ('rebuild', 'civil'), after=('city_ledger',), reward=(Idea('worker_flats'),)),
    Focus('city_wards', 'Elected Ward Committees',
          "Using the corrected electoral rolls, each ward of Lhesk elects a committee with a small budget for its own drains, "
          "lamps and markets. The committees are slow and noisy, and some will be captured by whoever turns out on a wet "
          "evening. Unless the national ballot comes first, they will be the first bodies anyone in Slavia has elected since 1987.",
          ('ballot', 'civil'), after_any=('city_drains', 'city_cisterns'), cost=10, exclusive=('city_manager',),
          requires=(HasFlag('rolls_corrected'),), reward=(SwapIdea('street_ledger', 'ward_committees'),)),
    Focus('city_manager', 'One Manager for the Whole City',
          "The opposite answer appoints a single city manager with authority over every street, pipe and permit, answerable to "
          "the national government rather than to the wards. In a country that is one city, the manager is in effect a second "
          "prime minister for daily life. Works go faster and complaints have one address, which may or may not reply.",
          ('command', 'civil'), after_any=('city_drains', 'city_cisterns'), cost=10, exclusive=('city_wards',),
          reward=(SwapIdea('street_ledger', 'city_manager_office'),)),
    Focus('city_ward_purses', 'Ward Purses and Ward Accounts',
          "Committees that survive their first year receive a fixed share of the city budget and must publish what they spend "
          "it on. Some build playgrounds, some fix roofs and one buys a fire engine. Waste becomes visible and local, which "
          "makes it easier to stop. The national ministries lose a little control over the street, and grumble about it.",
          ('scales', 'civil'), after=('city_wards',), reward=(SwapIdea('ward_committees', 'ward_purses'),)),
    Focus('city_works_schedule', 'The Manager Ranks the Works',
          "The city manager publishes one ranked schedule of works for the whole republic: drains first, then housing, then "
          "roads, then everything else. Projects move up the list only by the manager's decision. The schedule is efficient and "
          "infuriating. Wards with priorities of their own learn to lobby a single office, and the office learns to say no.",
          ('document', 'command'), after=('city_manager',), reward=(SwapIdea('city_manager_office', 'manager_schedule'),)),
    Focus('city_trams', 'Trams Along the Harbour Road',
          "A tram line on the road between the harbour and the arms halls carries shift workers on rails instead of through mud. "
          "Laying it means a year of diversions and a loan the treasury dislikes. Once running it moves more people than the "
          "buses ever did, and it keeps moving in the wet season when the buses stall.",
          ('rail', 'civil'), after_any=('city_ward_purses', 'city_works_schedule'),
          reward=(Build('infrastructure', 1, 0), Stability(0.01))),
    Focus('city_federal_seats', 'Wards Send Members to the Chamber',
          "Under the Federation each ward of Lhesk becomes a constituency and sends its own member to the federal chamber. "
          "Members can be found at their ward office on a weekday, which suits voters and exhausts members. A commission must "
          "draw the boundaries, and every party watches its pencil. Local grievances now reach the chamber by name.",
          ('ballot', 'assembly'), after=('city_ledger',), requires=(HasFlag('path_federal'),),
          reward=(Idea('constituency_offices'),)),
    Focus('city_charter', 'The Charter of Lhesk',
          "The city government and the national government are, in practice, the same people, and the charter finally says "
          "where one ends and the other begins. Streets, markets, water and transport go to the city; defence, money, the "
          "harbour and foreign affairs stay national. Lawyers will argue about the edges for years. The middle is settled.",
          ('document', 'scales'), after=('city_trams',), reward=(Idea('street_charter'),)),
))

ARSENAL = Branch('ars', 'Five Arms Halls, Two Civil Works', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('ars_inventory', 'Inventory of the Arms Halls',
          "Five arms halls dominate Slavian industry, against only two civil works, and every building slot in the province is "
          "taken. The republic cannot grow by building; it can only change what its halls make and how well they make it. An "
          "inventory of every press, lathe, payroll and order book comes first, and the managers dislike outsiders counting.",
          ('industry', 'document'), reward=(Idea('hall_inventory'), Event('arms_halls'))),
    Focus('ars_steel', 'Steel from the Plain',
          "Slavia mines enough steel for its own halls and some to spare, but sells most of the ore raw and buys back finished "
          "plate. A contract that sends the ore to the civil works for rolling keeps more of the value at home. The civil works "
          "must turn away other orders to take it, and with no free slots nothing new can be built to help.",
          ('industry', 'tools'), after=('ars_inventory',), reward=(TimedIdea('rolled_plate', 1095),)),
    Focus('ars_light_metal', 'Aluminium for the Air Guard',
          "The republic's aluminium deposits are modest but real, and the air guard's fighters need panels, ribs and spares "
          "that now come from abroad. A small airframe shop inside one of the arms halls reworks the metal into parts. It takes "
          "floor space from the rifle lines and needs sheet-metal workers the city must train. The guard promises to buy all of it.",
          ('air', 'industry'), after=('ars_inventory',), reward=(Flag('light_metal'),)),
    Focus('ars_civil_lines', 'Civil Lines in the Rifle Halls',
          "One school of thought says a city at peace does not need five arms halls. It proposes running civil lines inside two "
          "of them, building pumps, vans, stoves and tram parts under a protected price. The halls keep their workers and their "
          "roofs. The defence staff loses capacity it may want back, and the export houses lose their best product.",
          ('rebuild', 'industry'), after_any=('ars_steel', 'ars_light_metal'), cost=10,
          exclusive=('ars_licensed_sales', 'ars_garrison_halls'), reward=(SwapIdea('hall_inventory', 'civil_retooling'),)),
    Focus('ars_licensed_sales', 'Rifles for Licensed Buyers',
          "The export school says the halls are the republic's one comparative advantage and should sell to any government the "
          "cabinet licenses. Credit, a sales office at the harbour and a published licence list would keep every line busy. "
          "Revenue arrives quickly. So does the question every Slavian abroad will hear: whose wars are the rifles from Lhesk in?",
          ('missile', 'economy'), after_any=('ars_steel', 'ars_light_metal'), cost=10,
          exclusive=('ars_civil_lines', 'ars_garrison_halls'), reward=(SwapIdea('hall_inventory', 'licensed_exports'),)),
    Focus('ars_garrison_halls', 'An Arsenal for the City Alone',
          "The third school keeps all five halls on the republic's own orders, building reserves for the two formations and the "
          "air guard instead of selling abroad or converting. The city would never run short of rifles or shells. It would also "
          "pay for stock that sits in sheds, and the halls would lose the discipline of customers who can say no.",
          ('security', 'industry'), after_any=('ars_steel', 'ars_light_metal'), cost=10,
          exclusive=('ars_civil_lines', 'ars_licensed_sales'), reward=(SwapIdea('hall_inventory', 'garrison_arsenal'),)),
    Focus('ars_vans', 'Delivery Vans Off the Rifle Lines',
          "The first civil order is a light delivery van built on a frame the old rifle presses can stamp out. Shopkeepers, ward "
          "committees and the harbour office all want one. The vans are plain and a little overweight. They prove the halls can "
          "make something other than weapons, and they bring peacetime wages into households that only knew war work.",
          ('logistics', 'rebuild'), after=('ars_civil_lines',), reward=(TimedIdea('van_orders', 730),)),
    Focus('ars_end_users', 'End-User Certificates at the Quay',
          "Every crate of rifles leaving the harbour now carries a certificate naming its buyer and end use, checked by customs "
          "and published once a year. Some buyers go elsewhere rather than sign. The certificates cannot stop resale, but they "
          "let the republic state what it intended, and refuse anyone who lied to it the last time.",
          ('document', 'navy'), after=('ars_licensed_sales',), reward=(Idea('end_user_office'),)),
    Focus('ars_magazines', 'Magazines Beneath the Halls',
          "Stock built for the city's own reserve goes into magazines dug under the arms halls, dry, ventilated and guarded. A "
          "formation cut off in its own neighbourhood could draw rifles and rounds without crossing the city. The digging takes "
          "a year and the halls work around the noise. These are the most expensive cellars in Lhesk.",
          ('shelter', 'security'), after=('ars_garrison_halls',), reward=(Idea('hall_magazines'),)),
    Focus('ars_council_prices', 'The Councils Price the Contracts',
          "Under the Federation of the Works the council of each hall sets the price of its own contracts, and a national "
          "council settles disputes between halls. Prices fall where workers find waste and rise where they find danger. "
          "Foreign buyers must now bargain with elected delegates instead of managers, and a few of them say they prefer it.",
          ('assembly', 'economy'), after=('ars_inventory',), requires=(HasFlag('path_works'),), reward=(Idea('council_prices'),)),
    Focus('ars_cool_shifts', 'Shifts in the Cool Hours',
          "In July and August the arms halls are ovens by noon; output drops while accidents climb. Moving heavy work to the "
          "night and early morning, with a long break through the afternoon heat, costs night allowances and upsets every "
          "family's routine. The halls run cooler and safer, and the city learns to sleep through the sound of lathes.",
          ('tools', 'civil'), after=('ars_steel',), reward=(Idea('cool_hour_shifts'),)),
    Focus('ars_silo', 'Never Let the Silo Run Low',
          "Slavia pumps a little oil from the plain and stores its fuel in a single silo. In a crisis that silo is the "
          "republic's whole margin. Keeping it full means buying ahead of need and working the local wells harder. The treasury "
          "dislikes paying for fuel that sits still; the defence staff dislikes the thought of it standing empty.",
          ('logistics', 'shelter'), after=('ars_inventory',), reward=(Idea('silo_reserve'),)),
    Focus('ars_ten_years', 'The Halls After Ten Years',
          "Ten years after the first inventory the treasury repeats it hall by hall and sets the two side by side. The "
          "comparison shows which model the republic chose and what the choice cost in jobs, debt and readiness. It is "
          "published in full. Whatever the managers think of the figures, the next government will start from numbers, not slogans.",
          ('industry', 'scales'), after_any=('ars_vans', 'ars_end_users', 'ars_magazines'), requires=(After('2001.1.1'),),
          reward=(TimedIdea('decade_audit', 1095), Research('industry', 0.5, 1))),
))

HARBOUR = Branch('hbr', 'A Harbour Without a Fleet', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('hbr_office', 'A Harbour Office for the Republic',
          "Slavia has a naval base, a long quay and sixty convoys on its register, but no warships, and it has never asked for "
          "any; the harbour belongs to cargo. A single harbour office takes over berths, pilots, dues and the convoy list from "
          "four ministries that each did a quarter of the job. The ministries are not grateful to lose them.",
          ('navy', 'document'), reward=(Idea('harbour_office'), Event('quay_morning'))),
    Focus('hbr_channel', 'Dredge the Harbour Mouth',
          "Every wet season the rain carries silt off the plain into the harbour mouth, and every summer the channel is a little "
          "shallower. Larger ships now wait for the tide or anchor outside. A dredging contract restores the depth, and it must "
          "be renewed every few years. The cost is permanent, and so is the alternative, which is fewer ships.",
          ('tools', 'navy'), after=('hbr_office',), reward=(Idea('dredged_channel'),)),
    Focus('hbr_fuel_jetty', 'A Fuel Jetty to the Silo',
          "Imported fuel now comes ashore by hose and crosses the city by tanker lorry to reach the silo. A dedicated jetty and "
          "pipeline would land it directly and keep the tankers off the streets. It is a modest engineering job with an obvious "
          "target painted on it, and the defence staff asks for the line to be buried, which doubles the price.",
          ('logistics', 'navy'), after=('hbr_office',), reward=(Idea('fuel_jetty'),)),
    Focus('hbr_breakwater_radar', 'Radar on the Breakwater',
          "A surface radar at the end of the breakwater lets the harbour office see ships coming in through fog and rain, and "
          "lets the air guard see anything flying low over the water. It is the republic's first look beyond its own shore. The "
          "set is second-hand and its operators learn on the job. Ships stop arriving unannounced.",
          ('radar', 'navy'), after=('hbr_channel',), reward=(Build('radar_station', 1, 0),)),
    Focus('hbr_transit', 'Transit Cargo Through Lhesk',
          "The harbour could earn its keep handling cargo bound for other countries, landed at Lhesk and sent on by road. Transit "
          "fees would pay for the dredging and the office alike. The quay would fill with other people's goods and the city's "
          "roads with other people's lorries, and the republic's own imports would queue behind them in busy months.",
          ('economy', 'logistics'), after_any=('hbr_channel', 'hbr_fuel_jetty'), cost=10, exclusive=('hbr_home_first',),
          reward=(Idea('transit_wharf'),)),
    Focus('hbr_home_first', 'The Republic\'s Cargo First',
          "The other answer gives priority on every berth to the republic's own fuel, food, steel and parts, with transit "
          "accepted only when there is room. Ships carrying Slavian cargo never wait. Revenue is lower, and shippers looking for "
          "a dependable transit port go elsewhere. In a crisis the city knows its own supplies will be first ashore.",
          ('security', 'logistics'), after_any=('hbr_channel', 'hbr_fuel_jetty'), cost=10, exclusive=('hbr_transit',),
          reward=(Idea('home_cargo'),)),
    Focus('hbr_coast_watch', 'Coast Watchers in Fishing Boats',
          "Without warships the republic's eyes at sea are the fishing crews and weekend sailors who go out every day. A "
          "volunteer coast watch gives them radios, a reporting card and a small fee for each sighting. Reports are patchy and "
          "often wrong. They are also nearly free, and they reach water no radar on the breakwater can see.",
          ('fishing', 'communications'), after=('hbr_breakwater_radar',),
          reward=(Idea('coast_watchers'), Flag('coast_watch'))),
    Focus('hbr_mates', 'Classes for Mates and Masters',
          "Slavian convoys depend on officers trained abroad, and the good ones leave for foreign lines. Evening classes for "
          "mates and masters at the harbour office let local sailors qualify at home. Foreign insurers must recognise the "
          "certificates, which takes a year of letters. The republic gains ship's officers who live in Lhesk and sail for it.",
          ('training', 'navy'), after_any=('hbr_transit', 'hbr_home_first'), reward=(Idea('mates_classes'), XP('navy', 10))),
    Focus('hbr_dues_formula', 'Harbour Dues by Formula',
          "The board of managers replaces bargained harbour dues with a published formula based on tonnage, berth time and "
          "cargo class. Shippers who used to haggle lose their discounts; newcomers gain certainty. The board revises the "
          "formula once a year and posts it on the harbour office door. Revenue rises and favouritism has nowhere to hide.",
          ('scales', 'navy'), after=('hbr_office',), requires=(HasFlag('path_board'),), reward=(Idea('dues_formula'),)),
))

GUARD = Branch('grd', 'Two Formations Inside the City', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('grd_muster', 'Muster of the Two Formations',
          "The army of Slavia is two infantry formations of four battalions each, every formation with an engineer company in "
          "support, all stationed in Lhesk because there is nowhere else to put them. A full muster on the parade ground counts "
          "every rifle, truck and reservist. The count runs short in some places and long in others, and both are news.",
          ('training', 'security'), reward=(Idea('territorial_muster'), Event('muster_day'))),
    Focus('grd_street_schools', 'Street-Fighting Schools',
          "Any war fought for Slavia would be fought in the streets of Lhesk, yet the formations train mostly in open fields. "
          "The engineers build a mock block of houses, cellars and courtyards on waste ground near the halls, and every "
          "battalion rotates through it. The training is slow, loud and hard on the neighbours, who complain about blanks at dawn.",
          ('training', 'civil'), after=('grd_muster',), reward=(Idea('street_schools'),)),
    Focus('grd_engineers', 'Engineers Survey the Approaches',
          "The engineer companies walk the three land approaches to the city on the Slavian side: the hills toward Valka in the "
          "west, the foot of the Seteranoan mountains in the north and the short plain road toward Seterano in the east. They "
          "map culverts, bridges and ground that turns to mud. No line is moved and nothing is built across a frontier.",
          ('tools', 'security'), after=('grd_muster',),
          reward=(Flag('approaches_mapped'), Research('engineers_tech', 0.5, 1))),
    Focus('grd_every_block', 'Every Block a Strongpoint',
          "The first doctrine accepts that two formations cannot hold a frontier and plans to hold the city instead, block by "
          "block, with prepared positions in cellars, courtyards and the arms halls themselves. An attacker would have to take "
          "Lhesk street by street. The plan writes off the approaches and asks the population to live inside a fortress.",
          ('security', 'shelter'), after_any=('grd_street_schools', 'grd_engineers'), cost=10,
          exclusive=('grd_screen', 'grd_household_levy'), reward=(Idea('block_defence'),)),
    Focus('grd_screen', 'Screens on the Three Approaches',
          "The second doctrine posts light screens on the western hills, the northern foothills and the eastern road, with the "
          "main body held centrally on trucks to reinforce whichever approach is threatened. It depends on the engineers' maps "
          "and on roads that survive the wet season. It keeps the fighting outside the city, provided the screens hold.",
          ('logistics', 'security'), after_any=('grd_street_schools', 'grd_engineers'), cost=10,
          exclusive=('grd_every_block', 'grd_household_levy'), requires=(HasFlag('approaches_mapped'),),
          reward=(Idea('approach_screen'),)),
    Focus('grd_household_levy', 'A Levy of Every Household',
          "The third doctrine trusts the city's readiness more than its regulars. Every household provides one trained adult to "
          "a neighbourhood company, armed from the halls and drilled at weekends. The formations become a hard core inside a "
          "mass of part-time soldiers. Training is thin, but the numbers are large for a country this size, and every street "
          "has defenders.",
          ('civil', 'training'), after_any=('grd_street_schools', 'grd_engineers'), cost=10,
          exclusive=('grd_every_block', 'grd_screen'), reward=(Idea('household_levy'),)),
    Focus('grd_cellars', 'Knock Through the Cellars',
          "Engineers open passages between the cellars of neighbouring buildings so that defenders can move beneath the streets. "
          "Owners are compensated, and some are still not pleased. The passages double as shelters and storerooms, which helps "
          "the case. A plan of the whole network is kept by the defence staff and by nobody else.",
          ('shelter', 'tools'), after=('grd_every_block',), reward=(SwapIdea('block_defence', 'linked_cellars'),)),
    Focus('grd_crossroads', 'A Reserve at the Crossroads',
          "The central reserve takes over a depot at the main crossroads of the city, with trucks fuelled and loaded and drivers "
          "sleeping on site. It can reach any of the three approaches before a screen is overrun, if the roads are passable. "
          "Fuel use climbs and the depot never sleeps. The screens finally believe someone is coming to help them.",
          ('logistics', 'command'), after=('grd_screen',), reward=(SwapIdea('approach_screen', 'crossroads_reserve'),)),
    Focus('grd_companies', 'Companies by Neighbourhood',
          "The levy is organised into companies by neighbourhood, so that people drill beside those they live beside and would "
          "fight beside. Officers come from the formations; sergeants are elected. Local loyalty makes the companies cohesive "
          "and sometimes stubborn. Every neighbourhood now knows its assembly point, its armoury and its company's number.",
          ('assembly', 'security'), after=('grd_household_levy',),
          reward=(SwapIdea('household_levy', 'neighbourhood_companies'),)),
    Focus('grd_officer_school', 'An Officer School by the Harbour',
          "Slavian officers have trained abroad or learned on the job. A school in old harbour buildings now teaches tactics, "
          "logistics and command for the republic's own conditions: mud, streets and three short approaches. The first classes "
          "are small and the instructors tired. Within a few years the formations will be led by officers trained for this ground.",
          ('command', 'training'), after_any=('grd_cellars', 'grd_crossroads', 'grd_companies'), reward=(Idea('officer_school'),)),
    Focus('grd_staff_college', 'A Staff College Under the Board',
          "With the defence board in government, the general staff becomes the planning office of the state and needs more "
          "planners than it has. A staff college trains officers in budgets, supply and administration as well as operations. "
          "Graduates go to ministries as often as to battalions. The college makes the board competent, and its grip harder to loosen.",
          ('document', 'command'), after=('grd_muster',), requires=(HasFlag('path_defence'),), reward=(Idea('staff_college'),)),
))

AIR = Branch('air', 'The Territorial Air Guard', 1992, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count', 'Count the Air Guard',
          "The air guard of Slavia is twelve fighters on one field with four more in reserve, enough to watch the sky over a "
          "single province and little more. A count of pilots, mechanics, spares and fuel shows how many can actually fly on "
          "an ordinary morning. The answer is fewer than twelve, and the guard would prefer that nobody printed it.",
          ('air', 'document'), reward=(Idea('air_guard'),)),
    Focus('air_second_runway', 'A Second Runway Inland',
          "One runway means a single bomb or a burst tyre closes the whole air guard. A second runway on the inland edge of the "
          "plain, with taxiways and fuel points, lets the fighters keep flying if the first is out of action. The ground is soft "
          "in the wet season and must be drained deep before any concrete is poured. The work is costly and permanent.",
          ('runway', 'tools'), after=('air_count',), reward=(Build('air_base', 2, 0),)),
    Focus('air_radar_ring', 'Radars on the Three Approaches',
          "The air guard can only intercept what it can see, and today it sees mostly what pilots report by radio. Radar sets "
          "covering the western hills, the northern mountains and the sea give warning of anything approaching. The mountains "
          "mask part of the northern view. The sets need crews, power and spares, all of which compete with the halls.",
          ('radar', 'air'), after=('air_count',), reward=(Build('radar_station', 2, 0),)),
    Focus('air_alert', 'Pairs on Five-Minute Alert',
          "The first answer keeps two fighters armed and crewed at the end of the runway at every hour, ready to launch within "
          "five minutes of a radar contact. It is the most visible protection the guard can give the city. It wears out "
          "airframes and pilots faster than any other posture, and leaves little time or fuel for training.",
          ('air', 'security'), after_any=('air_second_runway', 'air_radar_ring'), cost=10,
          exclusive=('air_school', 'air_dispersal'), reward=(Idea('alert_pairs'),)),
    Focus('air_school', 'A Flying School Before More Fighters',
          "The second answer accepts a thinner alert and puts the guard's hours into training, opening a flying school that "
          "produces Slavian pilots instead of hiring them. In five years the guard would have twice the pilots for the same "
          "aircraft. Meanwhile the sky over Lhesk would be watched less closely than the defence staff would like.",
          ('training', 'air'), after_any=('air_second_runway', 'air_radar_ring'), cost=10,
          exclusive=('air_alert', 'air_dispersal'), reward=(Idea('flying_school'),)),
    Focus('air_dispersal', 'Strips Along the Coast Road',
          "The third answer scatters the guard along straight stretches of the coast road, widened and marked as emergency strips "
          "with fuel bowsers hidden nearby. No attacker could destroy the guard on the ground in a single raid. The strips are "
          "crude and the road must close whenever they are used. Drivers learn to look up before overtaking.",
          ('runway', 'logistics'), after_any=('air_second_runway', 'air_radar_ring'), cost=10,
          exclusive=('air_alert', 'air_school'), reward=(Idea('coast_strips'), Build('air_base', 2, 0))),
    Focus('air_revetments', 'Revetments for Every Fighter',
          "Earth and concrete revetments around each parking place protect the fighters from blast and splinters, and nets hide "
          "them from a casual glance. The work uses spoil from the storm drains and labour from the engineers. It is "
          "unglamorous, and it is the cheapest way to be sure the guard still exists an hour into a war.",
          ('shelter', 'air'), after_any=('air_alert', 'air_school', 'air_dispersal'), reward=(Idea('revetments'),)),
    Focus('air_airframe_shop', 'Airframe Parts Made in Lhesk',
          "The airframe shop in the arms hall begins delivering panels, ribs and simple spares to the guard. Fighters that "
          "waited weeks for parts from abroad are flying again in days. The shop cannot build an aircraft and does not try. It "
          "gives the guard a home supply of whatever breaks most often, and mechanics who understand the metal.",
          ('tools', 'air'), after=('air_count',), requires=(HasFlag('light_metal'),), reward=(Idea('airframe_shop'),)),
    Focus('air_aggressors', 'Hired Aggressor Pilots',
          "Former Belkan Air Force aces are selling their skills abroad, and several governments now employ them as aggressor "
          "squadrons that play the enemy in training. The guard could take a few on contract to hunt its own pilots over the "
          "sea. Nobody is named and nothing is signed until the defence staff has vetted the terms. The lessons would be harsh, "
          "costly and remembered.",
          ('air', 'medal'), after_any=('air_alert', 'air_school', 'air_dispersal'), requires=(After('1998.6.19'),),
          reward=(TimedIdea('aggressor_contract', 730),)),
))

FRONTIERS = Branch('fr', 'Hills, Passes and a Short Plain', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('fr_map', 'Three Frontiers and One Shore',
          "Slavia touches only two countries. Valka lies to the west across a line of hills. Seterano's mountains rise along the "
          "whole north, and a short stretch of plain meets Seterano again in the east. The south is open sea. The frontier "
          "office maps every road, track and post on the Slavian side. No line moves and no claim is made.",
          ('diplomacy', 'document'), reward=(Idea('frontier_office'), Event('three_frontiers'))),
    Focus('fr_hill_posts', 'Posts Facing the Western Hills',
          "The western frontier runs through hills where shepherds, smugglers and day labourers cross with little paperwork. "
          "Staffed posts on the main tracks, manned in shifts from the city, record the traffic and turn nobody back without "
          "cause. The posts are lonely and wet for half the year. They give the republic its first honest count of who comes "
          "and goes.",
          ('security', 'peace'), after=('fr_map',), reward=(Idea('hill_posts'),)),
    Focus('fr_flood_watch', 'Flood Gauges Below the Mountains',
          "Rain falling on the mountains to the north drains across the plain toward the sea, and in a wet spring the streams "
          "rise faster than the city can react. Gauges and a telephone line along the foot of the mountains, on the Slavian "
          "side, give hours of warning. The same gauges measure the silt that later fills the harbour mouth.",
          ('telescope', 'civil'), after=('fr_map',), reward=(Idea('flood_gauges'),)),
    Focus('fr_plain_road', 'Our End of the Eastern Road',
          "The road east across the plain toward Seterano is the one easy land route out of the republic. The Slavian section "
          "is narrow, unlit and floods each spring. Rebuilding it properly, with a staffed crossing, costs little next to the "
          "halls. What Seterano does with its own side of the road is for Seterano to decide.",
          ('logistics', 'diplomacy'), after=('fr_map',), reward=(Idea('east_crossing'),)),
    Focus('fr_no_bloc', 'Armed and in No Bloc',
          "The first posture declares that Slavia will join no alliance, host no foreign troops and lend its ground to nobody's "
          "war, while keeping its formations and air guard ready. It suits a city that would fight but does not want to. "
          "Larger powers may find the declaration convenient or irritating. Either way it costs Slavia only its options.",
          ('peace', 'security'), after_any=('fr_hill_posts', 'fr_flood_watch', 'fr_plain_road'), cost=10,
          exclusive=('fr_open_gates', 'fr_permits'), reward=(Idea('no_bloc'),)),
    Focus('fr_open_gates', 'Open Gates for Trade',
          "The second posture opens every staffed crossing to traders and travellers with the least possible paperwork, and "
          "invites the neighbours to do likewise without asking anything in return. Markets near the crossings would grow and "
          "the harbour would gain inland customers. Smuggling would grow too, and the frontier office would have to live with it.",
          ('economy', 'diplomacy'), after_any=('fr_hill_posts', 'fr_flood_watch', 'fr_plain_road'), cost=10,
          exclusive=('fr_no_bloc', 'fr_permits'), reward=(Idea('open_gates'),)),
    Focus('fr_permits', 'A Permit for Every Crossing',
          "The third posture closes the informal paths and requires a permit for every crossing, issued at the posts and "
          "checked on the way out and back. Smuggling falls and the frontier office knows exactly who is in the republic. Day "
          "labourers and shepherds lose a living. The neighbours learn that Slavia watches its doors, as intended.",
          ('document', 'security'), after_any=('fr_hill_posts', 'fr_flood_watch', 'fr_plain_road'), cost=10,
          exclusive=('fr_no_bloc', 'fr_open_gates'), reward=(Idea('crossing_permits'),)),
    Focus('fr_talks_offer', 'An Offer of Practical Talks',
          "Whatever posture it chose, the republic writes to Valka and Seterano offering regular talks on floods, crossings, "
          "fires and stray livestock, with no treaty and no conditions. Whether either neighbour sends anyone is theirs to "
          "decide. The offer is a letter and a reserved room. It shows that Slavia expects to live beside them for a long time.",
          ('diplomacy', 'peace'), after_any=('fr_no_bloc', 'fr_open_gates', 'fr_permits'),
          reward=(Flag('talks_offered'), Stability(0.02))),
))

ULYSSES = Branch('uly', 'Ulysses Over a Single Province', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_notice', 'The Asteroid Warning',
          "In December 1994 the astronomers' union warns that an asteroid named Ulysses is coming near the planet and could hit "
          "it. Nobody can say where fragments might fall. For most countries the first plan is to move people inland. Slavia has no "
          "inland. The Administration forms an impact committee and admits on its first day that the usual answers do not fit.",
          ('meteor', 'telescope'), requires=(After('1994.12.10'),), reward=(Idea('impact_committee'), Event('asteroid_news'))),
    Focus('uly_shelters', 'Shelters Under the Old Quarter',
          "If the people cannot leave the city, the city can go underground. Deep shelters under the old quarter, linked to the "
          "cellars and stocked with water for weeks, would hold much of the population. Digging in wet ground near the sea is "
          "slow and costly, and the pumps must run every day. Once built, the shelters serve in any war as well.",
          ('shelter', 'meteor'), after=('uly_notice',), cost=10, exclusive=('uly_ships', 'uly_corridors'),
          reward=(Idea('deep_shelters'),)),
    Focus('uly_ships', 'Berths for an Evacuation Fleet',
          "The republic's sixty convoys could, in an emergency, carry part of the population out to sea or to any port willing "
          "to take them. Reserving berths, fuel and boarding lists turns that possibility into a plan. Ships cost money to keep "
          "idle, and every destination depends on someone else. The plan also needs warning time nobody can promise.",
          ('navy', 'refugees'), after=('uly_notice',), cost=10, exclusive=('uly_shelters', 'uly_corridors'),
          reward=(Idea('evacuation_berths'),)),
    Focus('uly_corridors', 'Ask for Corridors Overland',
          "Using the channel its frontier talks opened, the republic asks Valka and Seterano whether Slavian families could "
          "shelter on their side of the hills and mountains if an impact were forecast near Lhesk. It asks; it assumes no "
          "answer. Lists of families, routes and assembly points are drawn up anyway, so that any answer can be acted on fast.",
          ('refugees', 'diplomacy'), after=('uly_notice',), cost=10, exclusive=('uly_shelters', 'uly_ships'),
          requires=(HasFlag('talks_offered'),), reward=(Idea('corridor_lists'),)),
    Focus('uly_pumps', 'Pump Crews for the Shelters',
          "Shelters dug below the water table flood without pumps, and pumps fail without crews. A standing pump service with "
          "spare engines, fuel and a duty roster keeps every shelter dry through the wet season. It is a permanent payroll for a "
          "disaster that may never come. The crews also clear flooded streets each spring, which wins them friends.",
          ('tools', 'shelter'), after=('uly_shelters',), reward=(SwapIdea('deep_shelters', 'shelter_pumps'),)),
    Focus('uly_boarding', 'Boarding Drills by Ward',
          "Each ward practises walking to its assigned berth with one bag per person, timed by harbour officials with "
          "stopwatches. The first drill takes three times as long as planned and blocks the harbour road for an afternoon. Later "
          "drills improve. Families come to know their berth number the way they know their own address.",
          ('refugees', 'navy'), after=('uly_ships',), reward=(SwapIdea('evacuation_berths', 'boarding_drills'),)),
    Focus('uly_lists', 'Family Lists for the Routes',
          "Every household is assigned a route, a vehicle or a column and an assembly point, in case a neighbour agrees to take "
          "them. The lists are revised every season as families move and children are born. Nobody knows whether they will "
          "ever be used. Keeping them makes the impact committee the best-informed office in the republic.",
          ('document', 'refugees'), after=('uly_corridors',), reward=(SwapIdea('corridor_lists', 'route_lists'),)),
    Focus('uly_impact', 'The Impact Is Confirmed',
          "In April 1996 the FCU president tells every nation that Ulysses is going to hit and that a plan to counter it exists. "
          "Where the fragments will come down is still unknown. The impact committee moves from planning to rehearsal, every ministry adds "
          "an asteroid line to its budget, and stocks of water, grain and medicine are bought and stored.",
          ('meteor', 'logistics'), after=('uly_notice',), requires=(After('1996.4.20'),),
          reward=(TimedIdea('impact_stockpiles', 1300),)),
    Focus('uly_breakwater_watch', 'Watchers on the Breakwater',
          "The volunteer coast watch takes on a new duty: logging bright objects in the night sky and reporting them to the "
          "impact committee, helped by a sky-search radar on the breakwater. Most reports are aircraft, satellites or planets. "
          "A few are real meteors and go to foreign observatories. The watchers become the republic's only astronomers.",
          ('telescope', 'fishing'), after=('uly_impact',), requires=(HasFlag('coast_watch'),),
          reward=(Idea('sky_log'), Build('radar_station', 1, 0))),
    Focus('uly_roche', 'Standby Through the Roche Night',
          "In July 1999 Ulysses crosses the Roche limit and comes close enough for the pull of the planet to matter. The impact "
          "committee keeps every shelter, berth and route list on standby through the night. Whatever the morning brings, the republic will have to explain afterwards "
          "what it did and why. The committee prepares two statements in advance and hopes to need neither.",
          ('meteor', 'shelter'), after=('uly_impact',), requires=(After('1999.7.8'),), reward=(Event('roche_night'),)),
))

WARS = Branch('war', 'Distant Wars and Near Prices', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_belka', 'The Belkan War on the Radio',
          "Late in March 1995 fighting begins in the Belkan War, a long way from Lhesk. Slavia is not a party and its frontiers stay quiet. "
          "Within a week fuel prices, freight rates and insurance premiums move, and foreign buyers ring the arms halls. The war "
          "arrives in the republic as a set of prices and a set of telephone calls, and both need answers.",
          ('communications', 'diplomacy'), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war_news'), Idea('war_premium'))),
    Focus('war_sell_licensed', 'Sell on Licence in Wartime',
          "The halls can sell rifles and rounds to any buyer the republic licenses, parties to the war included, under the "
          "end-user rules already on the books. The orders are large and paid in advance. Every crate will be photographed by "
          "somebody. Slavia would profit from a war it has no part in, and be remembered for it by both sides.",
          ('missile', 'economy'), after=('war_belka',), cost=10, exclusive=('war_embargo',),
          reward=(Idea('wartime_licences'), Flag('sales_open'))),
    Focus('war_embargo', 'No Arms to Warring Parties',
          "The republic declares that no weapons will leave Lhesk for any party to the war while it lasts. Fuel and food may "
          "sail; rifles may not. The halls lose orders and the workers lose overtime. The republic gains a clean record in a war "
          "it did not choose, and a reason for buyers on every side to trust its neutrality afterwards.",
          ('peace', 'scales'), after=('war_belka',), cost=10, exclusive=('war_sell_licensed',),
          reward=(Idea('arms_shut'), Flag('sales_closed'))),
    Focus('war_lumen', 'The Treaty Signed in Lumen',
          "The Belkan War is over by the end of June 1995, closed by a treaty at Lumen. Freight and fuel prices start to fall, slowly, and the arms "
          "enquiries dry up. The treasury reviews what the war cost the republic and what it earned. Whatever the halls chose, "
          "there are now a few months of figures showing how a distant war reaches a port city.",
          ('document', 'peace'), after=('war_belka',), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_premium'), Stability(0.02))),
    Focus('war_belka_won', 'Bids for Belkan Rebuilding',
          "In this world Belka has come out of the war on top, and its purchasing agents are looking for steel, trucks and spares "
          "to rebuild and rearm. Slavian halls can bid for the civil orders. The contracts are welcome and politically loaded, "
          "and the republic must decide how closely to tie its industry to a victorious power far away.",
          ('diplomacy', 'industry'), after=('war_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_orders', 730),)),
    Focus('war_belka_lost', 'Belkan Engineers Seek Work',
          "With Belka defeated, engineers and technicians from its industries look for work abroad, and a few write to the "
          "Slavian halls. Hiring them would bring skills the republic lacks, above all in aircraft and electronics. It would also "
          "draw scrutiny from the victors, and the defence staff insists on vetting each applicant before any contract.",
          ('science', 'diplomacy'), after=('war_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(TimedIdea('belkan_engineers', 730), Research('electronics', 0.5, 1))),
    Focus('war_usea', 'Insurers Hear of Usea First',
          "In August 2003 the ISAF is formed against Erusea after the seizure of Stonehenge, and war spreads across Usea. "
          "Slavia is far from it, but the freight lanes, insurers and arms buyers are not. The harbour office and the halls feel "
          "the war before the newspapers explain it. The republic has two years of prices and choices ahead.",
          ('communications', 'navy'), after=('war_lumen',), requires=(HasGlobal('ac_ucw_isaf_formed'), After('2003.8.22')),
          reward=(Event('usean_war'),)),
    Focus('war_usea_contracts', 'Contracts for the Usean Market',
          "Having sold on licence in the Belkan War, the halls take the same course again: civil and military orders from "
          "licensed buyers connected with the Usean war, paid in advance and certified at the quay. Shifts lengthen and overtime "
          "returns. So do the photographers, and this time they know exactly where to stand.",
          ('industry', 'economy'), after=('war_usea',), requires=(HasFlag('sales_open'),), reward=(Idea('usean_contracts'),)),
    Focus('war_relief_cargo', 'Relief Cargo for Usea',
          "Having refused arms to the Belkan War, the republic keeps its word in the Usean one and offers its convoys for relief "
          "cargo instead: food, medicine and building materials consigned to civilian agencies. The voyages are long and earn "
          "little, and crews take real risks in contested waters. Slavia's name for neutrality survives another war.",
          ('medical', 'navy'), after=('war_usea',), requires=(HasFlag('sales_closed'),), reward=(Idea('relief_cargo'),)),
    Focus('war_continental_end', 'The Continental War Ends',
          "With Farbanti fallen and the surrender of Erusea accepted by the ISAF, the Continental War is over. Slavian freight "
          "rates ease and the insurers relax. The treasury writes a second account of how a distant war reached Lhesk, ten years after the first. "
          "Comparing the two shows whether the republic has learned to live with wars it does not fight.",
          ('document', 'navy'), after=('war_usea',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(Stability(0.03), Research('logistics_tech', 0.5, 1))),
))

CENTURY = Branch('cent', 'The Republic at Two Thousand', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_count', 'Count the Republic Again',
          "Ten years after the street survey the republic counts itself again: households, jobs, wages, flats, rifles and ships. "
          "The comparison shows what the decade changed and what it left alone. A city-state can be counted completely, which "
          "is both its advantage and its embarrassment, and every figure will be quoted by someone who dislikes the government.",
          ('document', 'civil'), reward=(Idea('second_count'), Event('millennium_review'))),
    Focus('cent_apprentices', 'Apprentices at the Lathes',
          "Young Slavians who once went straight into the arms halls at sixteen now take three-year apprenticeships split "
          "between a hall and a technical school. Output dips slightly while they learn. The halls gain machinists who can set "
          "up their own work, and the republic gains citizens who could find a job somewhere other than a rifle line.",
          ('training', 'industry'), after=('cent_count',), reward=(Idea('apprentice_scheme'),)),
    Focus('cent_debt', 'Pay Down the Treasury Debt',
          "The treasury carries a debt of about three tenths of the republic's yearly output, inherited and rolled over through "
          "the nineties. Three budgets in surplus would cut it sharply. Wards, halls and the defence staff would all receive "
          "less in the meantime. The prize is a republic that can borrow in a crisis without asking anyone's leave.",
          ('economy', 'scales'), after=('cent_count',), reward=(TimedIdea('surplus_budgets', 1095),)),
    Focus('cent_hall_labs', 'Research Rooms in the Halls',
          "Each arms hall sets aside a room and a small budget for research into its own products and processes, staffed by "
          "engineers and the best apprentices. The rooms produce mostly small improvements and the occasional patent. They are "
          "the first research the republic does for itself instead of buying abroad, and they cost the halls some profit.",
          ('science', 'industry'), after=('cent_apprentices',), reward=(Idea('hall_labs'),)),
    Focus('cent_account', 'The Republic Since 1991 in Tables',
          "At the close of 2005 the government sets out in one plain report what the republic has become since 1991: the form "
          "of its government, the output of its halls, the record of its harbour and air guard, and its conduct through the "
          "asteroid years and the distant wars. The report makes no forecasts. Its tables become the starting line for whoever "
          "holds office next.",
          ('document', 'assembly'), after_any=('cent_debt', 'cent_hall_labs'), requires=(After('2005.1.1'),),
          reward=(Stability(0.04), Tooltip('Closes the 1991 to 2005 programme; later eras are written separately.'))),
))

BRANCHES = (ADMIN, CITY, ARSENAL, HARBOUR, GUARD, AIR, FRONTIERS, ULYSSES, WARS, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('canteen_day', 'Reopen the Canteen Hearings',
                'Ministers spend a week answering the night and day shifts in the canteens of the halls and docks. Repeatable '
                'every six months.',
                25, (Stability(0.01), TimedIdea('canteen_week', 90)), requires=(Completed('adm_canteens'),), cooldown=180),
    DecisionDef('range_course', 'Send the Battalions to the Ranges',
                'Each battalion fires its annual course on the coastal ranges. Repeatable every six months; it costs '
                'ammunition from the halls.',
                30, (XP('army', 15), TimedIdea('range_fortnight', 60)), requires=(Completed('grd_muster'),), cooldown=180),
    DecisionDef('scramble_call', 'Call an Unannounced Scramble',
                'The radar crews set a surprise contact and the air guard launches against it. Repeatable once a year.',
                30, (XP('air', 15), TimedIdea('scramble_week', 60)), requires=(Completed('air_count'),), cooldown=365),
    DecisionDef('main_runway', 'Lengthen the Main Runway',
                'Extends the original runway and its apron for heavier aircraft. A one-time charge on the air budget.',
                75, (Build('air_base', 1, 0),), requires=(Completed('air_second_runway'),)),
    DecisionDef('drain_flush', 'Flush the Drains Before January',
                'Crews flush and inspect every storm drain ahead of the wet season. Repeatable once a year.',
                25, (TimedIdea('drains_flushed', 150), Stability(0.01)), requires=(Completed('city_drains'),), cooldown=365),
    DecisionDef('silo_release', 'Release Silo Fuel at a Fixed Price',
                'Sells fuel from the silo to households and lorries at a fixed price for a season. Repeatable once a year.',
                40, (TimedIdea('fuel_release', 120),), requires=(Completed('ars_silo'),), cooldown=365),
)
