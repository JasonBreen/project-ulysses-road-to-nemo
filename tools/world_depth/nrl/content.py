"""Nordlands (NRL): bespoke national focus tree, era 1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (monarchism ruling, elections suspended,
the disarmed_nation manpower law, the Office of the Crown start leader, grand doctrines and stockpiles),
the country names, the nine 1991 states with their resources and buildings, and land neighbours
computed from the province map. Official: ACES Chronicle rows used only as date anchors for regional
pressure, each cited by its exact key. Everything else, including every Nordlandic choice, office,
idea, building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='NRL', name='Nordlands', root='world', package='nrl',
                  themes=('navy', 'industry', 'assembly'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Nordlands state: monarchism ruling at 54 percent (democratic 26, fascism 10, neutrality 10, communism 0), '
           'elections_allowed = no after a last election on 1991.1.1, stability 0.90, war support 0.10, the disarmed_nation '
           'manpower law, the NRL_ac_government_office start leader (Office of the Crown, holder unidentified), grand doctrines '
           'superior_firepower, fleet_in_being and operational_integrity, and stockpiles of 300 service tanks, 18 fighters, '
           '3 support aircraft, coastal escort and coastal submarine variants, 1000 convoys and 100 trains.',
           'mod/2985041246/history/countries/NRL - Nordlands.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names: Nordlands Principality under monarchism, democratic and neutrality, Nordlands Union and Nordlands '
           'Commune otherwise; adjective Nordlandic. World-start research priority: Physical Sustainment (transport, '
           'equipment replacement and affordable service capacity). Registry row: crown_office institution, 9 owned states, '
           'capital state 292; its fiscal calibration is not used as a canon claim.',
           'mod/2985041246/localisation/english/countries_l_english.yml; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Geography: 1991 states 254 Nord Peninsula (oil 60, steel 16, 3 arms plants, air base), 257 East Granley (oil 31, '
           'aluminium 22, harbour at Eyrarbakki), 277 Norden Forest (4 dockyards, the level-10 naval base, Lundegaard), 292 West '
           'Norden (capital, Aspneset, inland, fuel silo), 318 Hait Mountain (tungsten 14), 342 (Djurseryd and Havnaraas, '
           '3 dockyards), 368 Tenese (Nyboholm, 3 dockyards), 373 Haugaland (oil 13, steel 15, 3 arms plants) and 385 Oregonen '
           '(Skogaholm). Land neighbours FAT (states 75, 295, 297) and WIE (states 326, 372), computed from map/provinces.bmp. '
           'Replaced labels for state 342 and provinces 2825 and 5195 are avoided; no new place is named.',
           'mod/2985041246/history/states; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml'),
    Source('Mod provenance',
           'Campaign hooks read only: belka_dropped_nukes, belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt); '
           'ac_ucw_war_started and ac_ucw_war_averted (common/scripted_effects/ac_ucw.txt). No Nordlandic role is assumed.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Official', 'Date anchor only: Belka sells northern territory to FATO and eastern lands to eastern neighbours. '
           'No Nordlandic border, claim or role follows from it.', '1991 / 08.29'),
    Source('Official', 'Date anchor only: Belkan borders are redrawn.', '1991 / 12.16'),
    Source('Official', 'Date anchor only: the IAU warns that the asteroid Ulysses may strike the Earth.', '1994 / 12.10'),
    Source('Official', 'Date anchor only: the Belkan War breaks out. Nordlands is not claimed as a party.', '1995 / 03.25'),
    Source('Official', 'Date anchor only: seven nuclear devices are used in the Waldreich Mountains; the tree reads the mod '
           'flag belka_dropped_nukes rather than the date.', '1995 / 06.06'),
    Source('Official', 'Date anchor only: a treaty is signed in Lumen and the Belkan War ends; the tree reads the mod flag '
           'belka_lost_belkan_war rather than the date.', '1995 / 06.20'),
    Source('Official', 'Date anchor only: A World With No Boundaries launches a coup.', '1995 / 12.25'),
    Source('Official', 'Date anchor only: the Allied Forces attack the V2 facilities at Avalon Dam and defeat the rebellion.',
           '1995 / 12.31'),
    Source('Official', 'Date anchor only: the FCU President announces that Ulysses will impact the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor only: former top Belkan Air Force pilots are hired by various countries as aggressor '
           'squadrons. Whether Nordlands hires any is a gameplay choice.', '1998 / 06.19'),
    Source('Official', 'Date anchor only: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor only: Osea and Yuktobania agree to convert the Arkbird to clear orbital debris.',
           '1999 / 10.08'),
    Source('Official', 'Context only: Erusea invades the neutral country of San Salvacion; the tree reads the mod flag '
           'ac_ucw_war_started rather than a date.', '2003 / SUMMER'),
    Source('Provisional gameplay',
           'All Nordlandic focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the crown and the diet
    IdeaDef('office_review', 'The Crown Under Review', 'The Office of the Crown is taking stock of its own powers, and every faction waits on the result.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('cabinet_charter', 'The Cabinet Charter', 'A cabinet drawn from the diet runs the ministries; the crown acts on its advice.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'assembly')),
    IdeaDef('privy_seals', 'Seals Kept at Aspneset', 'The Office of the Crown keeps the seals, the budget and senior appointments.',
            {'political_power_gain': 0.20, 'stability_factor': -0.03}, ('command', 'security')),
    IdeaDef('diet_mandate', 'The Diet Mandate', 'The diet chooses the government; the crown keeps ceremony and the oath.',
            {'stability_factor': 0.04, 'research_speed_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'ballot')),
    IdeaDef('harbour_houses', 'Rule of the Harbour Houses', 'Chartered shipping, yard and oil houses govern by commission under crown patronage.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_gain': 0.05, 'stability_factor': -0.03}, ('economy', 'navy')),
    IdeaDef('written_constitution', 'A Written Constitution', 'Cabinet government set down in one ratified text with judicial review.',
            {'stability_factor': 0.08, 'political_power_factor': 0.08}, ('scales', 'document')),
    IdeaDef('codified_office', 'The Codified Privy Office', 'The privy office governs under a single statute that fixes its powers.',
            {'political_power_gain': 0.25, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('district_diet', 'A Diet of Nine Districts', 'Every district returns members in proportion to its people, with a floor for the smallest.',
            {'stability_factor': 0.07, 'research_speed_factor': 0.04}, ('assembly', 'scales')),
    IdeaDef('chartered_houses', 'Houses Under a Price Commission', 'The governing houses publish and cap what they charge for fuel, freight and berths.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.03, 'political_power_gain': 0.05}, ('economy', 'scales')),
    IdeaDef('open_accounts', 'Open Public Accounts', 'Salaries, contracts and grants above a threshold are printed every year.',
            {'political_power_factor': 0.05, 'stability_factor': 0.03}, ('scales', 'document')),
    IdeaDef('jubilee_year', 'The Year of the Renewed Oath', 'Officers of state renewed their oath before the diet.',
            {'stability_factor': 0.05, 'political_power_gain': 0.10}, ('medal', 'assembly')),
    # yards
    IdeaDef('slipway_census', 'The Slipway Census', 'Every slipway, crane and order book on the coast has been counted.',
            {'industrial_capacity_dockyard': 0.03}, ('navy', 'document')),
    IdeaDef('merchant_books', 'Merchant Order Books', 'The yards chase tankers, ferries and coasters for foreign owners.',
            {'industrial_capacity_dockyard': 0.08, 'consumer_goods_factor': -0.02}, ('navy', 'economy')),
    IdeaDef('home_hulls', 'Hulls for the Home Fleet', 'Steady naval orders keep the yards building for the Nordlandic flag.',
            {'industrial_capacity_dockyard': 0.05, 'navy_org_factor': 0.04}, ('navy', 'command')),
    IdeaDef('repair_basins', 'The Repair Basins', 'The coast specialises in overhaul, refit and conversion.',
            {'repair_speed_factor': 0.12, 'industrial_capacity_dockyard': 0.03}, ('tools', 'navy')),
    IdeaDef('yard_schools', 'Yard Apprentice Schools', 'Every yard trains welders, fitters and electricians at shared cost.',
            {'production_factory_efficiency_gain_factor': 0.04, 'industrial_capacity_dockyard': 0.03}, ('training', 'tools')),
    IdeaDef('tanker_yards', 'Tanker Yards of the Coast', 'Mid-sized tankers built quickly and to price for every ocean.',
            {'industrial_capacity_dockyard': 0.10, 'consumer_goods_factor': -0.03}, ('navy', 'economy')),
    IdeaDef('second_series', 'The Second Escort Series', 'A newer escort class with better sensors and longer range.',
            {'industrial_capacity_dockyard': 0.06, 'navy_org_factor': 0.06}, ('navy', 'security')),
    IdeaDef('refit_contracts', 'Refit Contracts', 'Commercial hulls of every flag book the repair basins months ahead.',
            {'repair_speed_factor': 0.15, 'industrial_capacity_dockyard': 0.04}, ('tools', 'economy')),
    # oil
    IdeaDef('peninsula_survey', 'The Peninsula Survey', 'The state knows what lies under the Nord Peninsula before it signs a lease.',
            {'production_speed_buildings_factor': 0.03}, ('economy', 'tools')),
    IdeaDef('crown_wells', 'Crown Wells of the Peninsula', 'A state company holds every lease and pays the treasury directly.',
            {'political_power_gain': 0.05, 'production_speed_industrial_complex_factor': 0.05}, ('command', 'economy')),
    IdeaDef('licensed_fields', 'Licensed Oil Fields', 'Private drillers work auctioned blocks for royalties.',
            {'production_speed_industrial_complex_factor': 0.10, 'stability_factor': -0.02}, ('economy', 'tools')),
    IdeaDef('oil_fund', 'The Oil Savings Fund', 'Modest extraction, with every royalty saved for long-term works.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.02}, ('scales', 'economy')),
    IdeaDef('listed_crown_oil', 'A Listed Crown Oil Company', 'Nordlandic savers hold a minority of the crown oil company.',
            {'production_speed_industrial_complex_factor': 0.08, 'political_power_gain': 0.05}, ('economy', 'command')),
    IdeaDef('royalty_courts', 'Royalty Courts', 'Technical courts settle royalty disputes quickly and in public.',
            {'production_speed_industrial_complex_factor': 0.12, 'stability_factor': 0.02}, ('scales', 'tools')),
    IdeaDef('fund_dividend', 'The Fund Dividend', 'The oil fund pays a yearly dividend into works without touching its capital.',
            {'stability_factor': 0.06, 'consumer_goods_factor': -0.04}, ('scales', 'civil')),
    # service
    IdeaDef('disarmed_footing', 'A Disarmed Footing', 'Almost no conscripts, full depots and no written defence policy.',
            {'stability_factor': 0.02, 'army_core_defence_factor': -0.05}, ('security', 'document')),
    IdeaDef('armour_custodians', 'Custodians of the Service Armour', 'Long-service crews keep the stored tanks able to move.',
            {'army_org_factor': 0.03, 'supply_consumption_factor': -0.05}, ('command', 'tools')),
    IdeaDef('home_guard', 'The District Home Guard', 'Volunteers and former soldiers on district rolls with a rifle and a muster point.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.05}, ('document', 'security')),
    IdeaDef('coast_brigades', 'Volunteer Brigades of the Coast', 'A small, well-paid volunteer force guarding harbours and jetties.',
            {'army_org_factor': 0.05, 'experience_gain_army_factor': 0.08}, ('medal', 'navy')),
    IdeaDef('declared_disarmament', 'A Declared Disarmament', 'Minimal forces, published budgets and open inspection by neighbours.',
            {'stability_factor': 0.06, 'political_power_gain': 0.05}, ('peace', 'diplomacy')),
    IdeaDef('firepower_school', 'The Firepower School', 'Officers plan around guns, armour and supply rather than numbers.',
            {'army_attack_factor': 0.04, 'planning_speed': 0.08}, ('command', 'science')),
    IdeaDef('civil_defence_corps', 'The Civil Defence Corps', 'Rescue teams, firefighters and shelter wardens in every district.',
            {'production_speed_infrastructure_factor': 0.08, 'stability_factor': 0.03}, ('civil', 'shelter')),
    # fleet
    IdeaDef('fleet_waits', 'A Fleet in Being', 'Escorts and submarines stay close to defended harbours and sail when the odds favour them.',
            {'navy_org_factor': 0.04, 'naval_coordination': 0.03}, ('navy', 'command')),
    IdeaDef('sub_screen', 'Submarines Off the Headlands', 'Coastal submarines patrol the approaches to every major harbour.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.05}, ('submarine', 'navy')),
    IdeaDef('escort_groups', 'Escort Groups', 'Escort flotillas shepherd convoys through the approaches.',
            {'naval_speed_factor': 0.05, 'navy_org_factor': 0.06}, ('navy', 'logistics')),
    IdeaDef('mine_belts', 'Controlled Mine Belts', 'Shore-switched minefields can close the harbour channels in hours.',
            {'naval_coordination': 0.05, 'army_core_defence_factor': 0.04}, ('security', 'navy')),
    IdeaDef('convoy_office', 'The Djurseryd Convoy Office', 'Routes, convoys and owners managed from one office ashore.',
            {'naval_coordination': 0.05, 'consumer_goods_factor': -0.02}, ('logistics', 'document')),
    IdeaDef('fleet_review_year', 'The Fleet Review Year', 'The whole fleet sailed together in home waters.',
            {'war_support_factor': 0.04, 'navy_org_factor': 0.03}, ('medal', 'navy')),
    # frontier
    IdeaDef('frontier_desks', 'Frontier Customs Desks', 'Customs desks shared with FATO and Wielvakia.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.05}, ('gate', 'document')),
    IdeaDef('fato_transit', 'The FATO Transit Desk', 'Shared manifests and quicker clearance at the FATO crossings.',
            {'consumer_goods_factor': -0.02, 'production_speed_infrastructure_factor': 0.05}, ('gate', 'rail')),
    IdeaDef('wielvakian_transit', 'The Wielvakian Transit Desk', 'Common hours and common forms on the Wielvakian frontier.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.01}, ('gate', 'diplomacy')),
    IdeaDef('open_crossings', 'Open Crossings', 'Spot checks only, and crossings open around the clock.',
            {'consumer_goods_factor': -0.04, 'production_speed_infrastructure_factor': 0.10}, ('gate', 'economy')),
    IdeaDef('guarded_crossings', 'Guarded Crossings', 'Every vehicle inspected and every crossing staffed by armed customs police.',
            {'army_core_defence_factor': 0.06, 'stability_factor': 0.03}, ('security', 'gate')),
    IdeaDef('frontier_markets', 'Frontier Market Days', 'Weekly markets at the crossings for small traders of three countries.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'civil')),
    IdeaDef('tariff_courts', 'Frontier Tariff Courts', 'Customs disputes decided in days by courts sitting in the frontier districts.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('scales', 'document')),
    IdeaDef('frontier_trade_zone', 'The Frontier Trade Zone', 'Simplified duties and shared warehouses at the crossings.',
            {'consumer_goods_factor': -0.06, 'production_speed_infrastructure_factor': 0.12}, ('economy', 'gate')),
    IdeaDef('frontier_police', 'The Frontier Police Service', 'One trained frontier police with its own school and career ladder.',
            {'army_core_defence_factor': 0.08, 'stability_factor': 0.04}, ('security', 'document')),
    # the Belkan War years
    IdeaDef('war_watch', 'Watch Beyond FATO', 'A watch room in Aspneset and coastal radars on full shifts while Belka is at war.',
            {'air_detection': 0.05, 'war_support_factor': 0.03}, ('radar', 'security')),
    IdeaDef('war_risk_premiums', 'War-Risk Premiums', 'Insurers charge more on every lane near the fighting.',
            {'consumer_goods_factor': 0.03, 'stability_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('closed_roadsteads', 'Closed Roadsteads', 'Harbours closed to belligerent warships except in distress.',
            {'stability_factor': 0.04, 'naval_coordination': 0.03}, ('security', 'navy')),
    IdeaDef('fuel_for_all', 'Bunkers Open to Merchants', 'Fuel and provisions sold to any merchant ship that pays.',
            {'production_speed_industrial_complex_factor': 0.05, 'political_power_gain': 0.10, 'stability_factor': -0.03}, ('economy', 'logistics')),
    IdeaDef('mercy_corridor', 'The Mercy Corridor', 'Nordlandic ships carry the wounded and the displaced under neutral markings.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03}, ('medical', 'navy')),
    IdeaDef('shared_air_notices', 'Shared Notices to Airmen', 'Three neighbours share restricted zones and unidentified traffic reports.',
            {'air_detection': 0.05, 'stability_factor': 0.02}, ('air', 'diplomacy')),
    IdeaDef('fallout_watch', 'Fallout Watch Stations', 'Daily published readings of air, rain and milk in every district.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02}, ('telescope', 'medical')),
    IdeaDef('reserve_bunkers', 'Reserve Bunkers for Neutrals', 'Reserve fuel released at cost to stranded neutral ships.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('economy', 'shelter')),
    IdeaDef('allied_rebuilding', 'Reconstruction Orders', 'Steel, fuel and hulls sold for Allied reconstruction after Lumen.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.01}, ('rebuild', 'industry')),
    IdeaDef('cautious_trade', 'Cautious Trade', 'Trade continues carefully while a stronger Belka settles its gains.',
            {'army_core_defence_factor': 0.05, 'consumer_goods_factor': 0.02}, ('security', 'economy')),
    # air
    IdeaDef('eighteen_fighters', 'Eighteen Fighters', 'A small air arm for air policing and display.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('interceptor_wing', 'The Interceptor Wing', 'Fighters under ground radar control, meeting intruders at the coast.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('sea_patrol_wing', 'The Sea Patrol Wing', 'Long patrols over the merchant lanes and anti-ship training with the fleet.',
            {'air_mission_efficiency': 0.08, 'naval_coordination': 0.03}, ('air', 'navy')),
    IdeaDef('aggressor_school', 'The Aggressor Squadron', 'Hired veterans fly as the enemy in training.',
            {'experience_gain_air_factor': 0.12, 'air_superiority_efficiency': 0.04}, ('medal', 'air')),
    IdeaDef('home_instructors', 'Home Instructors', 'Nordlandic pilots trained abroad return to teach at home.',
            {'experience_gain_air_factor': 0.08, 'stability_factor': 0.02}, ('training', 'air')),
    IdeaDef('air_display_year', 'The Air Display Year', 'Recruiting offices filled after the display over the capital.',
            {'war_support_factor': 0.05, 'experience_gain_air_factor': 0.05}, ('medal', 'runway')),
    # sky
    IdeaDef('sky_watch', 'The Sky Watch Office', 'A small office collecting reports on Ulysses and answering the public.',
            {'air_detection': 0.03, 'stability_factor': 0.02}, ('telescope', 'meteor')),
    IdeaDef('rock_shelters', 'Rock Shelters', 'Stocked shelters under the larger cities and harbour towns.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('evacuation_timetable', 'The Evacuation Timetable', 'Assigned trains, buses and ferries for every coastal district.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.08}, ('logistics', 'civil')),
    IdeaDef('dark_year_stores', 'Stores for a Dark Year', 'A year of grain, seed and fuel held in every district.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.03}, ('shelter', 'economy')),
    IdeaDef('relief_shipping', 'The Relief Shipping Office', 'Chartered hulls carry food and medicine to stricken coasts.',
            {'stability_factor': 0.04, 'political_power_gain': 0.10}, ('medical', 'navy')),
    IdeaDef('shelter_storehouses', 'Shelters as Storehouses', 'Leased shelter tunnels kept ready for civil defence.',
            {'static_anti_air_damage_factor': 0.08, 'production_speed_buildings_factor': 0.04}, ('shelter', 'industry')),
    # districts
    IdeaDef('district_ledger', 'The District Ledger', 'Roads, schools and revenue of the nine districts in one ledger.',
            {'production_speed_infrastructure_factor': 0.08}, ('document', 'civil')),
    IdeaDef('district_councils', 'District Councils', 'Each district spends its own budget on its own works.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.10}, ('assembly', 'ballot')),
    IdeaDef('works_ministry', 'The Ministry of Works', 'One ministry plans every road, school and harbour wall to one standard.',
            {'production_speed_buildings_factor': 0.06, 'political_power_gain': 0.05}, ('command', 'tools')),
    IdeaDef('housing_drive', 'The Aspneset Housing Drive', 'Rental blocks and cheap loans for the capital.',
            {'stability_factor': 0.04, 'production_speed_buildings_factor': -0.03}, ('civil', 'rebuild')),
    IdeaDef('accord_dividend', 'The Accord Dividend', 'A round of works in every district on the accord anniversary.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('peace', 'scales')),
    # sustainment
    IdeaDef('sustainment_plan', 'Physical Sustainment', 'Maintenance, spares and transport before new purchases.',
            {'supply_consumption_factor': -0.04, 'repair_speed_factor': 0.05}, ('tools', 'logistics')),
    IdeaDef('polytechnic', 'The Aspneset Polytechnic', 'Engineers, technicians and mechanics trained at home.',
            {'research_speed_factor': 0.04}, ('science', 'document')),
    IdeaDef('truck_pools', 'District Truck Pools', 'Stored military trucks put to work on public projects.',
            {'supply_consumption_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('logistics', 'civil')),
    IdeaDef('licensed_kits', 'Licensed Equipment Kits', 'Proven foreign designs assembled under licence.',
            {'production_factory_efficiency_gain_factor': 0.05, 'research_speed_factor': 0.02}, ('document', 'industry')),
    IdeaDef('home_designs', 'National Design Offices', 'Trucks, radios and small vessels designed at home.',
            {'research_speed_factor': 0.05, 'production_factory_max_efficiency_factor': 0.03}, ('science', 'tools')),
    IdeaDef('spares_catalogue', 'The National Spares Catalogue', 'Every state machine listed with its parts and repair intervals.',
            {'supply_consumption_factor': -0.06, 'repair_speed_factor': 0.10, 'production_factory_max_efficiency_factor': 0.03}, ('document', 'logistics')),
    # the new century
    IdeaDef('export_drive', 'The Export Order Drive', 'Yards and oil houses plan their order books together.',
            {'industrial_capacity_dockyard': 0.03, 'production_factory_efficiency_gain_factor': 0.03}, ('economy', 'document')),
    IdeaDef('tanker_boom', 'The Tanker Charter Boom', 'Nordlandic tankers chartered to neutral buyers at wartime rates.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.02, 'industrial_capacity_factory': 0.04}, ('economy', 'navy')),
    IdeaDef('home_bunkering', 'Tankers in Home Waters', 'The tanker fleet kept on home and regional routes at stable prices.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('navy', 'peace')),
    IdeaDef('calm_seas', 'A Lean Year at Sea', 'Idle tankers and a treasury that helped their owners through.',
            {'stability_factor': 0.02, 'consumer_goods_factor': 0.02}, ('navy', 'scales')),
    # decisions
    IdeaDef('dues_waived', 'Harbour Dues Waived', 'A season without harbour dues for merchant hulls.',
            {'consumer_goods_factor': -0.03, 'industrial_capacity_dockyard': 0.04}, ('navy', 'economy')),
    IdeaDef('reserve_release', 'Reserve Fuel for Industry', 'Reserve fuel released to factories for a season.',
            {'production_speed_industrial_complex_factor': 0.05}, ('economy', 'industry')),
)

# --- offices -------------------------------------------------------------------------------------
OFFICES = (
    Office('crown_cabinet', 'Crown Cabinet of the Diet',
           'A cabinet drawn from the majority of the elected diet, governing collectively in the name of the crown and bound '
           'to resign when it loses the confidence of the diet. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('privy_office', 'Privy Office of the Crown',
           'The palace secretariat that held the seals in 1991, confirmed as the government: a small council of crown officers '
           'ruling by order, with the diet kept as a consultative body. Provisional gameplay office with no named holder.',
           'monarchism', 'absolutism'),
    Office('diet_government', 'Diet Government of the Principality',
           'An executive elected by and answerable to the diet, with the crown confined to ceremony, honours and the oath of '
           'office. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('harbour_council', 'Council of Harbours and Wells',
           'A council of chartered shipping, yard and oil houses holding the seals under crown patronage and governing through '
           'commissions; elections stay suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('crown_office', 'Who Holds the Seals', (
        "The year opens quietly in Aspneset. An Office of the Crown holds the seals of the principality, the diet returned at "
        "New Year has been given no date to sit, and elections are suspended until the palace decides otherwise. Nordlands is "
        "calm, comfortable and far from any battlefield, and most citizens see no reason to change an arrangement that has "
        "kept it so. More than half of them vote for the crown's friends whenever they are allowed to vote.",
        "Calm is not the same thing as consent. Liberal deputies, backed by roughly a quarter of the electorate, want a cabinet "
        "that answers to the diet. The shipping, yard and oil houses of the coast pay most of the country's taxes and would "
        "prefer to govern through councils of their own. A circle of palace officials believes the Office should simply be "
        "confirmed as the government and stop apologising for its existence.",
        "The secretaries of the Office have drafted a stocktaking of who decides what in the principality. Before it begins, "
        "they want a ruling on how it will be conducted. In public, it will be slow, noisy and a platform for every faction. "
        "Inside the palace, it will be quick, tidy and distrusted from the first day.",
    ), (
        Option('Conduct it in public.', (Stability(0.02), PP(-15))),
        Option('Keep it inside the palace.', (PP(35), Stability(-0.02))),
    ), picture=2),
    EventDef('empty_slipways', 'Half the Slipways Idle', (
        "The slipway census lands on the minister's desk with a blunt summary: the Nordlandic coast has more yard capacity than "
        "it has orders. Eleven dockyards share the work between Norden Forest, the twin harbours of Djurseryd and Havnaraas, "
        "Nyboholm in Tenese and a small yard on the Hait Mountain coast. On an ordinary day a good part of that capacity is "
        "idle, and the census counts cranes that have not lifted anything in months.",
        "The yard owners blame cheap foreign competition and ask for subsidies. The admiralty notes that the fleet's escorts and "
        "submarines are ageing and could keep several yards busy for a decade, if the treasury paid. The unions want any plan "
        "that keeps their members employed and distrust every plan that mentions efficiency. Fitters at the older yards add "
        "that repair work, which pays well and needs fewer slipways, has been neglected for years.",
        "The government has not chosen a model for the yards, and it does not need to choose one today. It does need to decide "
        "what the census means in public. Published in full, it will start a fierce argument about which yards have a future. "
        "Shared only with the owners and the admiralty, it will guide policy quietly while every harbour town assumes the worst.",
    ), (
        Option('Publish the census in full.', (Stability(-0.02), Research('naval_equipment', 0.5, 1))),
        Option('Brief the owners and the admiralty.', (PP(30), XP('navy', 10))),
    ), picture=0),
    EventDef('peninsula_oil', 'Oil Beneath the Peninsula', (
        "The survey teams come back from the Nord Peninsula with maps that change the national budget. The fields under the "
        "peninsula hold more oil than every other Nordlandic field combined, and the smaller fields of East Granley, Haugaland "
        "and the capital district are richer than the old estimates claimed. For a country that has lived from its yards and its "
        "merchant fleet, oil offers a second income that needs no foreign shipowner to stay afloat.",
        "The peninsula itself is thinly settled. It has a single road, an airfield, three arms plants and small towns that are "
        "used to being forgotten. Their councils ask what share of the wealth will stay where it is pumped. The oil houses on "
        "the coast want leases quickly and say the state is too slow to drill. The treasury wants the revenue but fears an "
        "economy that rises and falls with the price of a single product.",
        "Ministers have not chosen how the fields will be owned. They must first decide whether to slow the rush or welcome it. "
        "Whatever they say this month will be read as a signal by every bidder, and speculators are already buying land near "
        "the old wells in the hope of selling it back to whoever drills.",
    ), (
        Option('Slow the rush until the law is written.', (PP(25), Stability(0.01))),
        Option('Open the peninsula to bidders now.', (Research('excavation_tech', 0.5, 1), Stability(-0.01))),
    ), picture=1),
    EventDef('no_conscripts', 'A Country Without Conscripts', (
        "Nordlands raises almost no conscripts. Its manpower law is the lightest any state keeps, and support for war, measured "
        "in any way the ministries care to try, is close to nothing. Yet its depots hold three hundred tanks, thousands of trucks, "
        "artillery for several divisions and equipment for far more soldiers than it employs. The country is disarmed in its "
        "habits and armed in its warehouses.",
        "Nobody planned this. The equipment was bought in years when governments worried more, and the conscripts were released "
        "in years when they worried less. Pacifist deputies want the stores sold or scrapped. The general staff wants a reserve "
        "system that can use them. Harbour towns, which feel exposed, want someone guarding the oil jetties and the naval "
        "harbour, and they do not much mind who.",
        "The defence review must decide what the stores are for before deciding anything else. How it is run will colour the "
        "answer: a review led by officers will be trusted by the army and resented by the diet, while a review open to the "
        "public will produce a broad consensus and very little equipment policy.",
    ), (
        Option('Let the general staff lead.', (XP('army', 15), WarSupport(0.03))),
        Option('Open the review to the public.', (Stability(0.02), PP(-5))),
    ), picture=2),
    EventDef('fleet_in_harbour', 'The Fleet That Stays in Harbour', (
        "The admiralty's new doctrine is printed, and the newspapers have already given it a nickname: the fleet that stays in "
        "harbour. The doctrine says that a small navy deters best by surviving, keeping its escorts and coastal submarines close "
        "to defended bases and sailing only when the odds are good. It is a sensible policy for a country with a long coast, a "
        "large merchant fleet and no wish to fight anyone.",
        "It is also an easy policy to mock. Merchant captains ask who will protect them at sea if the warships stay home. Junior "
        "officers complain that a navy which never sails never learns. The yards point out that a fleet in being still needs "
        "modern hulls, and the treasury points out that modern hulls cost money it would rather not spend on ships designed to "
        "wait.",
        "The admirals must now explain the doctrine to the country and to the diet. They can argue it as a deterrent, which "
        "will please the general staff and frighten no one abroad, or as a shield for trade, which will please the shipowners "
        "and commit the fleet to protecting them whenever they ask.",
    ), (
        Option('Present it as a deterrent.', (XP('navy', 15), WarSupport(0.02))),
        Option('Present it as a shield for trade.', (Stability(0.02), PP(15))),
    ), picture=0),
    EventDef('two_neighbours', 'A Capital on the Frontier', (
        "Few capitals sit as close to their neighbours as Aspneset. The West Norden district touches FATO at the crossings into "
        "Granley Tips and Gangl, and Wielvakia at Farnlands and Vakia. Trains, trucks and day workers cross every morning. Until "
        "now, each crossing has been run by whichever officials happened to be posted there, using forms nobody has revised "
        "in decades.",
        "Neither neighbour has given Nordlands cause for alarm in years, which is exactly why the frontier has been neglected. "
        "Smuggling is modest, delays are long and disputes go to ministries that answer letters slowly. Merchants on all three "
        "sides have learned to pay their way through, and the customs service has learned to let them. East Granley, Hait "
        "Mountain and Oregonen have their own crossings and their own habits.",
        "The government proposes shared customs desks with both neighbours as a first step. Before the desks open, it must "
        "decide how to describe them. Presented as a convenience for traders, they will be welcomed by merchants and ignored by "
        "everyone else. Presented as a security measure, they will reassure the cautious and make both neighbours wonder what "
        "Nordlands has heard.",
    ), (
        Option('Call it a convenience for trade.', (Stability(0.02), PP(-5))),
        Option('Call it a matter of security.', (WarSupport(0.02), PP(20))),
    ), picture=1),
    EventDef('belkan_war', 'War Beyond FATO', (
        "In late March 1995 the Belkan War breaks out. Nordlands has no border with Belka, but FATO does, and FATO shares a long "
        "frontier with West Norden and East Granley. Within hours the watch room in Aspneset is taking calls from frontier "
        "posts, harbour masters and shipping offices that all want to know the same thing: how close will this come?",
        "The first days bring rumours faster than facts. Radio bulletins contradict one another, insurers raise their rates on "
        "every lane near the fighting, and the oil houses ask whether tankers bound for ports near the war should keep sailing. "
        "The frontier commands report heavy traffic on the FATO side of the line, though nobody can say whether it is "
        "refugees, merchants or soldiers.",
        "The government has said nothing yet beyond confirming that Nordlands is not a party to the war. Every faction wants a "
        "statement: the houses want reassurance, the pacifists want a declaration, and the admiralty wants authority to watch "
        "the harbour approaches more closely. The first decision is narrower and harder: how much of the government's own "
        "uncertainty to share with the public.",
    ), (
        Option('Tell the public everything we know.', (WarSupport(0.03), Event('warship_request', 20))),
        Option('Reassure first, explain later.', (Stability(0.02), Event('warship_request', 30))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Nordlandic response is gameplay',
        picture=2),
    EventDef('warship_request', 'Warships at the Harbour Mouth', (
        "A warship of one of the belligerents appears off the Norden Forest coast and signals a request to enter harbour for "
        "fuel and repairs. Its captain reports minor damage and a sick crew member. The ship is armed, its flag is unmistakable, "
        "and its arrival has been noticed by every fishing boat and newspaper on that stretch of coast before the admiralty has "
        "finished reading the signal.",
        "Custom allows a neutral port to admit a belligerent warship in distress for a short time and for limited repairs. It "
        "does not oblige the port to do so, and every hour the ship spends alongside will be read by the other side as a "
        "favour. The harbour master wants instructions. The shipowners want the ship gone before insurers notice. The doctors "
        "want the sick sailor ashore.",
        "Whatever the principality decides will become precedent. Other warships, from either side, will ask for the same "
        "treatment and point to this one when they do. The admiralty has drafted three replies, and the government has a few "
        "hours before the captain stops waiting for an answer and decides the matter alone.",
    ), (
        Option('Admit it for repairs, under strict limits.', (Stability(-0.01), XP('navy', 10))),
        Option('Land the sailor, refuse the ship.', (Stability(0.02), PP(10))),
        Option('Refuse entry outright.', (WarSupport(0.02), PP(-10))),
    ), picture=0),
    EventDef('no_flag_coup', 'Officers Who Serve No Country', (
        "On Christmas Day 1995 a group calling itself A World With No Boundaries launches a coup. Its name is its programme: "
        "a movement that rejects the borders of every state. The Allied Forces answer it, and on the last day of the year they "
        "attack its V2 facilities at Avalon Dam and defeat the rebellion. The news reaches Aspneset in fragments, and none of "
        "the fragments is reassuring.",
        "Nordlands has few officers and fewer secrets, but the coup raises an uncomfortable question. A small, comfortable "
        "officer corps that has never fought might be exactly the kind of body in which such ideas could take root quietly. "
        "The general staff insists that its officers are loyal. The diet's liberals want an inquiry. The palace wants the "
        "matter handled without accusing anyone in particular.",
        "The government can order a quiet review of the officer corps, conducted by the general staff itself, or an open "
        "inquiry by a committee of the diet with powers to question anyone. A quiet review protects reputations and may miss "
        "everything. An open inquiry will find whatever there is to find, and it will humiliate many officers who have done "
        "nothing wrong.",
    ), (
        Option('Order a quiet review by the staff.', (PP(20), XP('army', 10))),
        Option('Open an inquiry by the diet.', (Stability(0.02), WarSupport(-0.02))),
    ), citation='date anchors only, ACES Chronicle rows 1995 / 12.25 and 1995 / 12.31 in tools/lore/chronicle.json; '
                'the Nordlandic response is gameplay', picture=1),
    EventDef('pilots_for_hire', 'Pilots Without an Air Force', (
        "By the summer of 1998 former top pilots of the Belkan Air Force have found new employers. Various countries hire them "
        "to fly as aggressor squadrons, playing the enemy in training so that their own crews learn what a skilled opponent "
        "feels like. Agents for some of these pilots are now in Aspneset, offering a contract the Nordlandic air arm never "
        "imagined being offered.",
        "The air arm's commanders are enthusiastic. Their pilots have never flown against anyone better than each other, and a "
        "few months against veterans would teach them more than years of exercises. The diet is divided. Some deputies object "
        "to paying veterans of a war that frightened the whole region, and others note that the pilots are selling their skill, "
        "not their politics.",
        "The palace wants a decision before the agents take their offer elsewhere. Whatever the government chooses, the air arm "
        "will remember it. A contract buys skill quickly and invites a public argument about whose veterans should teach "
        "Nordlandic pilots. A refusal keeps the argument out of the papers and asks the air arm to build its own teachers, "
        "slowly.",
    ), (
        Option('Open talks with the agents.', (XP('air', 15), PP(-10))),
        Option('Thank them and decline for now.', (Stability(0.02), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1998 / 06.19 in tools/lore/chronicle.json; any Nordlandic contract is gameplay',
        picture=2),
    EventDef('ulysses_north', 'Ulysses Will Strike', (
        "In April 1996 the President of the FCU tells the world that the asteroid Ulysses will strike the Earth and announces "
        "plans to counter it. Nobody can yet say where its fragments will fall. Nordlands has eight coastal districts, one "
        "inland capital and a coastline no wall could protect, and the country wakes to the news that its future depends on "
        "the arithmetic of orbits.",
        "The advisers divide along familiar lines. Engineers propose shelters dug under the larger cities and stocked for weeks. "
        "Planners propose evacuation timetables and early warning, arguing that a few hours of notice, well used, are worth more "
        "than tunnels. The treasury observes that either plan costs as much as a decade of fleet construction, and the yards "
        "observe that their own orders would be the first delayed.",
        "The public mood swings between panic and denial. Places of worship are crowded, shops sell out of tinned food, and some "
        "coastal families talk of moving inland. Before choosing a plan, the government must decide how to speak about a danger "
        "it cannot control: openly and immediately, or calmly and only once its plans are ready.",
    ), (
        Option('Speak openly and prepare at once.', (WarSupport(0.03), Stability(-0.01), Research('construction_tech', 0.5, 1))),
        Option('Keep calm until the plan is ready.', (Stability(0.02), PP(10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; '
                'Nordlandic preparations are gameplay', picture=1),
    EventDef('nine_districts', 'Nine Districts, One Treasury', (
        "The district ledger is finished, and it confirms what everyone outside the capital suspected. West Norden and Norden "
        "Forest hold most of the population and most of the public spending. The Nord Peninsula, which holds most of the oil, "
        "has the fewest schools and the worst roads. Tenese, Oregonen and the twin harbours of Djurseryd and Havnaraas earn much "
        "of the shipping income and complain that it is spent elsewhere.",
        "Every district can read the ledger as a grievance. East Granley and Hait Mountain sit on the frontier and feel watched "
        "rather than served. Haugaland's villages share their roads with oil trucks and arms convoys. The capital district pays "
        "the most tax and is blamed for the most decisions, which its residents consider doubly unfair.",
        "The ministers must decide how the ledger will be used. They could publish it district by district and invite every "
        "council to argue its case in public, or keep it inside the ministries and use it to steer spending quietly. The first "
        "starts a long argument the capital cannot control; the second leaves every district suspecting that it is being "
        "cheated by the others.",
    ), (
        Option('Publish it district by district.', (Stability(0.02), PP(-20))),
        Option('Keep it for the ministries.', (PP(30), Stability(-0.01))),
    ), picture=1),
    EventDef('decade_review', 'The Principality at Ten Years', (
        "Ten years after the crown first took stock of its own powers, an independent commission publishes its review of how "
        "Nordlands governs itself. Its members, drawn by lot from judges, harbour officials and district deputies, were given "
        "access to every ministry. Their report runs to several volumes, and the summary alone is longer than most newspapers "
        "are willing to print.",
        "The findings please nobody completely. The principality is richer, its frontier is quiet and its fleet still exists, "
        "which is all the fleet ever promised. But the commission finds too much power in too few offices, too much revenue in "
        "a handful of houses and districts, and a younger generation that takes the calm for granted. It warns that the "
        "arrangements of the nineties were built for a quiet decade, and the region has not been quiet.",
        "The government must decide how to receive the report. It can publish every volume unedited and accept a season of "
        "hostile commentary, or release an approved summary and let the rest gather dust in the archive. Either way the review "
        "will frame political argument for years, and the factions have already chosen their favourite paragraphs.",
    ), (
        Option('Publish every volume.', (Stability(0.03), PP(-25))),
        Option('Release an approved summary.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('distant_war', 'A War on Another Continent', (
        "Erusea's invasion of the neutral country of San Salvacion starts a war on the Usean continent, an ocean away from "
        "Nordlands. Within weeks the war arrives in Nordlandic harbours in its own way. Freight rates rise, insurers redraw "
        "their maps, and buyers from every neutral country want fuel delivered sooner than the tanker fleet can manage.",
        "Nordlandic shipowners see the best market in a generation. The admiralty sees a merchant fleet about to scatter across "
        "dangerous oceans with no navy able to follow it. The oil houses want to sell as much as the peninsula can pump, and "
        "the treasury wants to know how much of the windfall it may tax before the owners register their ships under other "
        "flags.",
        "The government will soon have to set a tanker policy. For now, it must decide how to describe its position before "
        "newspapers abroad describe it for Nordlands. A firm restatement of neutrality will calm the region and limit the "
        "owners' options. A careful silence will keep every option open and invite every belligerent to wonder. Either way, "
        "the harbour masters want to know by Monday which flags they may refuel and which they must turn away.",
    ), (
        Option('Restate our neutrality publicly.', (Stability(0.02), PP(10))),
        Option('Say nothing until the policy is set.', (PP(25), Stability(-0.01))),
    ), citation='context only, ACES Chronicle row 2003 / SUMMER in tools/lore/chronicle.json; fired by the mod flag '
                'ac_ucw_war_started; the Nordlandic response is gameplay', picture=0),
    EventDef('contraband', 'Contraband on the Frontier Roads', (
        "The frontier police, given a week and every spare officer, sweep the back roads between the guarded crossings. They "
        "find what everyone expected and a little more: trucks of untaxed fuel heading out, cigarettes and electronics coming "
        "in, and a warehouse near the Wielvakian frontier stacked with goods whose papers were signed by officials who should "
        "have known better.",
        "The sweep is a success by any measure the police care about. It is also an embarrassment. Several signatures belong to "
        "customs officers who have served for decades, and one belongs to a district official with friends in the capital. "
        "Merchants on both sides of the frontier are angry that honest trade was held up for a week, and the neighbours' "
        "customs services want to know why they were not told in advance.",
        "The government can prosecute everyone the sweep uncovered, publicly and at once, and accept the political damage. Or "
        "it can settle quietly, dismissing the officials and recovering the taxes without trials. The first shows that the "
        "guarded frontier means what it says. The second keeps the peace with the districts and with both neighbours.",
    ), (
        Option('Prosecute in public.', (Stability(-0.02), WarSupport(0.02))),
        Option('Settle it quietly.', (PP(-15), Stability(0.02))),
    ), picture=1),
)

# --- branches ------------------------------------------------------------------------------------
CROWN = Branch('crown', 'The Crown and the Diet', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('crown_sits', 'The Crown Takes Stock',
          "Nordlands enters 1991 governed by an Office of the Crown that holds the seals at Aspneset while elections stay "
          "suspended. The arrangement is popular and unexamined. A formal stocktaking asks which powers the Office actually uses "
          "and on whose authority, and it costs the palace the comfortable silence it has enjoyed for years.",
          ('command', 'assembly'), reward=(Idea('office_review'), Event('crown_office'))),
    Focus('crown_civil_list', 'Publish the Civil List',
          "Every payment the crown makes, from palace salaries to grants for harbour chapels, goes into a printed civil list "
          "that any newspaper can quote. Courtiers lose a little privacy and some lose their sinecures outright. In exchange the "
          "crown can argue about its future from a position nobody can call secretive.",
          ('scales', 'document'), after=('crown_sits',), reward=(Flag('civil_list_published'), Stability(0.02))),
    Focus('crown_diet_recalled', 'Recall the Sleeping Diet',
          "The diet returned at New Year has no calendar and no budget. Recalling it for a short consultative sitting gives "
          "deputies a room to speak in and a record of what they said. It drains political capital, because the Office must "
          "answer questions it would rather not hear, but it keeps the argument indoors.",
          ('assembly', 'ballot'), after=('crown_sits',), reward=(Flag('diet_summoned'), PP(-20))),
    Focus('crown_cabinet_path', 'Ministers Who Face the Diet',
          "The constitutional camp proposes that the crown keep its throne and its oath while a cabinet drawn from the diet runs "
          "the ministries and answers for the budget. It suits a calm and prosperous country. It also ends the Office's habit of "
          "settling disputes with a quiet telephone call, which many officials will miss.",
          ('ballot', 'assembly'), after=('crown_civil_list', 'crown_diet_recalled'),
          exclusive=('crown_privy_path', 'crown_diet_path', 'crown_houses_path'),
          reward=(SwapIdea('office_review', 'cabinet_charter'),)),
    Focus('crown_privy_path', 'Keep the Seals at Aspneset',
          "Palace officials argue that the present arrangement works and should be confirmed rather than apologised for. The "
          "Office would keep the seals, the budget and appointments, and the diet would advise when asked. Decisions stay "
          "quick. The quarter of the country that votes liberal will treat every one of them as a grievance.",
          ('command', 'security'), after=('crown_civil_list', 'crown_diet_recalled'),
          exclusive=('crown_cabinet_path', 'crown_diet_path', 'crown_houses_path'),
          reward=(SwapIdea('office_review', 'privy_seals'),)),
    Focus('crown_diet_path', 'The Crown Reigns, the Diet Rules',
          "Liberal deputies want more than a cabinet: they want the diet to elect the government outright and the crown to step "
          "back into ceremony, honours and the oath of office. The principality would keep its name and lose its working "
          "monarchy. The palace staff, and many older voters, regard this as a quiet abdication.",
          ('assembly', 'scales'), after=('crown_civil_list', 'crown_diet_recalled'),
          exclusive=('crown_cabinet_path', 'crown_privy_path', 'crown_houses_path'),
          reward=(SwapIdea('office_review', 'diet_mandate'),)),
    Focus('crown_houses_path', 'Let the Harbour Houses Govern',
          "The shipping, yard and oil houses of the coast pay most of the taxes and employ most of the skilled workforce. Their "
          "proposal is a council of chartered houses that governs by commission, with the crown as patron and the diet as a "
          "sounding board. Efficient, certainly. Accountable mainly to balance sheets.",
          ('economy', 'navy'), after=('crown_civil_list', 'crown_diet_recalled'),
          exclusive=('crown_cabinet_path', 'crown_privy_path', 'crown_diet_path'),
          reward=(SwapIdea('office_review', 'harbour_houses'),)),
    Focus('crown_seat_cabinet', 'Seat the Crown Cabinet',
          "A cabinet formed from the diet majority takes the ministries, and the crown is bound to act on its advice. Elections "
          "return on a fixed calendar. The change runs through the office rather than any person. Ministers inherit the credit "
          "for a calm country and the blame for every rise in harbour dues.",
          ('ballot', 'document'), after=('crown_cabinet_path',), cost=10,
          exclusive=('crown_seat_privy', 'crown_seat_diet', 'crown_seat_houses'),
          reward=(Regime('crown_cabinet'), Flag('path_cabinet'))),
    Focus('crown_seat_privy', 'Confirm the Privy Office',
          "The Office of the Crown becomes a standing privy office with written authority over the seals, the budget and senior "
          "appointments. Elections remain suspended and the diet sits only when summoned. Government is fast and narrow. With no "
          "chamber to share decisions, every failure now lands at the palace gate.",
          ('command', 'document'), after=('crown_privy_path',), cost=10,
          exclusive=('crown_seat_cabinet', 'crown_seat_diet', 'crown_seat_houses'),
          reward=(Regime('privy_office'), Flag('path_privy'))),
    Focus('crown_seat_diet', 'Seat the Diet Government',
          "The diet elects an executive that governs in its own name, and the crown withdraws to ceremony and the oath of office. "
          "Elections run on a fixed calendar. The coastal houses lose their private access to the palace, and deputies discover "
          "that running a fleet, a yard sector and an oil field is harder than criticising those who did.",
          ('assembly', 'ballot'), after=('crown_diet_path',), cost=10,
          exclusive=('crown_seat_cabinet', 'crown_seat_privy', 'crown_seat_houses'),
          reward=(Regime('diet_government'), Flag('path_diet'))),
    Focus('crown_seat_houses', 'Charter the Council of Houses',
          "A council of chartered shipping, yard and oil houses takes the seals under the crown's patronage and governs through "
          "commissions staffed by its own managers. Elections stay suspended. Contracts move quickly and the treasury is well "
          "run. Wages, rents and harbour prices are now set by the same people who collect them.",
          ('economy', 'document'), after=('crown_houses_path',), cost=10,
          exclusive=('crown_seat_cabinet', 'crown_seat_privy', 'crown_seat_diet'),
          reward=(Regime('harbour_council'), Flag('path_houses'))),
    Focus('crown_new_oath', 'An Oath for the New Order',
          "Whatever form of government emerged, its officers swear a new oath written for it, read aloud in Aspneset and printed "
          "in every district newspaper. The ceremony costs little and settles a great deal: officials know whom they serve, and "
          "the losing factions know the argument is closed until the next decade.",
          ('peace', 'assembly'), after_any=('crown_seat_cabinet', 'crown_seat_privy', 'crown_seat_diet', 'crown_seat_houses'),
          reward=(Flag('oath_sworn'), Stability(0.03))),
))

YARDS = Branch('yards', 'Slipways of the Northern Coast', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('yards_census', 'Count the Empty Slipways',
          "Eleven dockyards line the Nordlandic coast, spread across Norden Forest, the twin harbours of Djurseryd and "
          "Havnaraas, Nyboholm in Tenese and a small yard on the Hait Mountain shore. Not all of them have work. A census of "
          "slipways, cranes and order books tells the yards what the country can still build and what it should stop "
          "pretending to build.",
          ('navy', 'document'), reward=(Idea('slipway_census'), Event('empty_slipways'))),
    Focus('yards_lundegaard', 'Cranes for Lundegaard',
          "Lundegaard handles the heavy lifts for the Norden Forest yards, but its quay cranes are older than most of the people "
          "who run them, and the roads behind the quay jam at every shift change. New cranes and a widened access road cost a "
          "season of disruption and let the forest yards take larger hulls.",
          ('tools', 'navy'), after=('yards_census',), reward=(Build('infrastructure', 1, 277),)),
    Focus('yards_nyboholm', 'Nyboholm Yard Roads',
          "Nyboholm is the busiest harbour in Tenese and home to three dockyards that share a single road to the interior. "
          "Rebuilding that road and the rail spur beside it lets steel arrive without blocking the fish market. The work is "
          "unglamorous, and it takes trucks off the shipbuilders' delivery lists for most of a year.",
          ('logistics', 'navy'), after=('yards_census',), reward=(Build('infrastructure', 1, 368), XP('navy', 5))),
    Focus('yards_djurseryd', 'A New Basin at Djurseryd',
          "Djurseryd and Havnaraas share a crowded harbour district whose yards still have room for one more basin. Dredging and "
          "walling it costs money the treasury would rather keep, and it takes water from the trawler fleet. In return the coast "
          "gains a slipway long enough for modern hulls, the first new one in years.",
          ('navy', 'rebuild'), after=('yards_census',), reward=(Build('dockyard', 1, 342),)),
    Focus('yards_merchant', 'Order Books from Abroad',
          "The yard owners want to chase merchant orders from abroad: tankers, ferries and coasters built to price and delivered "
          "on time. Order books fill, and wages follow. The navy gets only the space that is left, and the country's best "
          "slipways end up serving whichever foreign owner pays the earliest instalment.",
          ('economy', 'navy'), after_any=('yards_lundegaard', 'yards_nyboholm', 'yards_djurseryd'), cost=10,
          exclusive=('yards_navy', 'yards_repair'),
          reward=(SwapIdea('slipway_census', 'merchant_books'), Flag('yard_model_merchant'))),
    Focus('yards_navy', 'Hulls for Our Own Flag',
          "The admiralty proposes that the yards build first for the home fleet, with steady orders for coastal escorts and "
          "submarines replacing the boom and bust of commercial contracts. Workers gain secure employment and the fleet gains "
          "modern hulls. The treasury pays for every keel, and export income shrinks accordingly.",
          ('navy', 'command'), after_any=('yards_lundegaard', 'yards_nyboholm', 'yards_djurseryd'), cost=10,
          exclusive=('yards_merchant', 'yards_repair'),
          reward=(SwapIdea('slipway_census', 'home_hulls'), Flag('yard_model_navy'))),
    Focus('yards_repair', 'Refit Yards, Not Launch Yards',
          "A third school says the coast should specialise in repair, refit and conversion, which needs fewer slipways, less "
          "capital and more skill. Ships of every flag would call for overhauls. The yards would rarely launch anything new, and "
          "the workforce would shrink toward a smaller corps of highly paid fitters.",
          ('tools', 'rebuild'), after_any=('yards_lundegaard', 'yards_nyboholm', 'yards_djurseryd'), cost=10,
          exclusive=('yards_merchant', 'yards_navy'),
          reward=(SwapIdea('slipway_census', 'repair_basins'), Flag('yard_model_repair'))),
    Focus('yards_skogaholm', 'Tanker Orders for Skogaholm',
          "Skogaholm in Oregonen has a working harbour and no yard of its own. The first merchant contracts justify building one "
          "there, laid out for tankers and coasters rather than warships. Oregonen gains shipbuilding wages for the first time "
          "in a generation, and the navy notes, without enthusiasm, that the new yard was designed around commercial hulls.",
          ('navy', 'economy'), after=('yards_merchant',), reward=(Build('dockyard', 1, 385), Research('naval_equipment', 0.5, 1))),
    Focus('yards_escort_series', 'A Series of Coastal Escorts',
          "Rather than designing each escort from scratch, the yards build a single class in a long series, with the same "
          "engines, guns and depth charges throughout. Crews train once and serve on any hull. Each ship is less refined than a "
          "bespoke design, but the fleet can count on every one of them being ready.",
          ('navy', 'security'), after=('yards_navy',), reward=(XP('navy', 15), Research('naval_equipment', 0.5, 1))),
    Focus('yards_floating_dock', 'A Floating Dock for Oregonen',
          "A floating dock moored off Skogaholm can lift damaged hulls without a permanent basin. It suits the repair model: "
          "cheap to place, easy to tow and able to serve any visiting ship. Oregonen's council wanted a proper yard and says so, "
          "but the dock pays its crews from the first season.",
          ('tools', 'navy'), after=('yards_repair',), reward=(Build('dockyard', 1, 385), PP(-15))),
    Focus('yards_apprentices', 'Apprentices in Every Yard',
          "Every yard is required to train apprentices in welding, fitting and electrical work, with the cost shared between "
          "owners and the state. The first years are expensive and slow, since apprentices waste steel. A decade later the yards "
          "have the skilled hands that older workers had warned would vanish with their retirement.",
          ('training', 'tools'), after_any=('yards_skogaholm', 'yards_escort_series', 'yards_floating_dock'),
          reward=(Idea('yard_schools'),)),
))

OIL = Branch('oil', 'Oil of the Nord Peninsula', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('oil_survey', 'Survey the Peninsula Fields',
          "The Nord Peninsula holds more oil than the rest of Nordlands combined, under a thinly settled landscape with one "
          "airfield and three arms plants. East Granley, Haugaland and the capital district have smaller fields. A full "
          "geological survey tells the state what it owns before anyone signs a lease, and it delays every lease by a year.",
          ('economy', 'tools'), reward=(Idea('peninsula_survey'), Event('peninsula_oil'))),
    Focus('oil_peninsula_road', 'A Road Down the Peninsula',
          "Wells mean nothing without a way to move crews, pipe and pumps. A paved road and a rail spur along the Nord Peninsula "
          "cost more per resident than any other project in the country, because so few people live there. The oil houses offer "
          "to pay a share if they get first use of it.",
          ('logistics', 'rail'), after=('oil_survey',), reward=(Build('infrastructure', 2, 254),)),
    Focus('oil_granley_wells', 'Wells Along East Granley',
          "East Granley sits on oil and the country's only aluminium ore, beside the FATO frontier. Its fields are older and "
          "smaller than the peninsula's but already close to the harbour at Eyrarbakki. Roads to the outlying wells are cheap "
          "and quick, and they keep East Granley from feeling like an afterthought to the peninsula boom.",
          ('tools', 'economy'), after=('oil_survey',), reward=(Build('infrastructure', 1, 257),)),
    Focus('oil_geology_school', 'A School of Petroleum Geology',
          "The survey showed how few Nordlandic geologists exist; most of the field work was done by hired foreign crews. A "
          "school of petroleum geology in the capital trains surveyors, drillers and reservoir engineers at home. It takes years "
          "to graduate the first class, and the oil houses will poach its best students.",
          ('science', 'telescope'), after=('oil_survey',),
          reward=(Research('excavation_tech', 0.5, 1), Research('synth_resources', 0.5, 1))),
    Focus('oil_crown_company', 'A Crown Company for the Wells',
          "A state company holds every lease and pays the treasury directly. Revenue stays at home and drilling follows national "
          "priorities, including the fuel reserve the admiralty keeps asking for. The pace is slower than private drillers would "
          "manage, and the company's managers answer to ministers who know little about oil.",
          ('command', 'economy'), after_any=('oil_peninsula_road', 'oil_granley_wells'), cost=10,
          exclusive=('oil_licences', 'oil_slow_fund'), reward=(Idea('crown_wells'), Flag('oil_model_crown'))),
    Focus('oil_licences', 'Licences for Private Drillers',
          "The fields are auctioned in blocks to private drillers, domestic and foreign, who pay royalties on every barrel. Rigs "
          "arrive within a few seasons and the peninsula fills with crews. The state collects less per barrel than a crown "
          "company would, and the drillers decide which fields are worth working.",
          ('economy', 'tools'), after_any=('oil_peninsula_road', 'oil_granley_wells'), cost=10,
          exclusive=('oil_crown_company', 'oil_slow_fund'), reward=(Idea('licensed_fields'), Flag('oil_model_licensed'))),
    Focus('oil_slow_fund', 'Pump Slowly, Save the Rest',
          "A cautious school proposes modest extraction, with every royalty paid into a savings fund that may be spent only on "
          "long-term works. Little changes on the peninsula and nobody gets rich quickly. Decades from now, the fund may be the "
          "largest asset the principality owns, provided no government raids it first.",
          ('scales', 'economy'), after_any=('oil_peninsula_road', 'oil_granley_wells'), cost=10,
          exclusive=('oil_crown_company', 'oil_licences'), reward=(Idea('oil_fund'), Flag('oil_model_fund'))),
    Focus('oil_refinery', 'A Refinery on the Peninsula',
          "Crude shipped away unrefined earns a fraction of its value. A refinery near the peninsula fields keeps the processing, "
          "and the jobs, at home. It takes the last free industrial plot on the peninsula, and the three arms plants nearby will "
          "have to share power and water with it.",
          ('industry', 'economy'), after_any=('oil_crown_company', 'oil_licences', 'oil_slow_fund'),
          reward=(Build('industrial_complex', 1, 254),)),
    Focus('oil_smelter', 'Power for the Granley Smelters',
          "East Granley's aluminium ore needs cheap power before it is worth anything, and its oil fields can supply it. A "
          "gas-fired plant and a smelter beside it turn two local resources into one export. The smelter takes East Granley's "
          "last industrial plot, and its fumes will not make it popular downwind.",
          ('industry', 'tools'), after=('oil_granley_wells',),
          reward=(Build('industrial_complex', 1, 257), Research('excavation_tech', 0.5, 1))),
    Focus('oil_eyrarbakki', 'Tanker Jetties at Eyrarbakki',
          "Eyrarbakki's harbour was built for fishing boats and coasters. Tanker jetties and a pipeline from the Granley fields let "
          "crude and aluminium leave by sea without passing through the capital's rail yards. The harbour gets busier and "
          "dirtier, and the families who own the waterfront want compensation.",
          ('navy', 'logistics'), after=('oil_smelter',), reward=(Build('infrastructure', 1, 257), XP('navy', 5))),
    Focus('oil_fuel_reserve', 'A Fuel Reserve for Hard Years',
          "Whatever the ownership model, part of the output goes into a strategic reserve stored in tanks beside the capital's "
          "fuel depot. It ties up oil that could have been sold, and the oil houses grumble. If war closes the sea lanes or prices "
          "spike, the country will not run dry in a month.",
          ('shelter', 'economy'), after=('oil_refinery',), reward=(Flag('fuel_reserve'), PP(-25))),
))

SERVICE = Branch('service', 'A Disarmed Principality', 1991, 'FOCUS_FILTER_MANPOWER', (
    Focus('serv_footing', 'What Disarmament Means',
          "Nordlands keeps almost no conscripts and talks little about its army, yet its depots hold hundreds of tanks, thousands "
          "of trucks and enough artillery for several divisions. A disarmed footing without a defence policy is an accident, not "
          "a choice. Writing a policy down will annoy pacifists and generals alike.",
          ('security', 'document'), reward=(Idea('disarmed_footing'), Event('no_conscripts'))),
    Focus('serv_armour_store', 'Three Hundred Tanks in Storage',
          "The service armour sits in sheds with too few mechanics to keep it running. A custodian corps of long-service crews "
          "rotates the vehicles, cannibalises the worst and keeps the rest ready to move. It costs fuel and wages for machines "
          "that may never fight, which is precisely the point of owning them.",
          ('command', 'tools'), after=('serv_footing',), reward=(Idea('armour_custodians'),)),
    Focus('serv_hait_ranges', 'Mountain Ranges at Hait',
          "Hait Mountain faces Wielvakia across the Vakia frontier and offers the steepest training ground for mountain "
          "troops in the country. Access roads, a range and a winter camp let the army practise where it would actually have to fight. Hikers "
          "lose a valley, and the district gains a garrison economy.",
          ('training', 'security'), after=('serv_footing',), reward=(Build('infrastructure', 1, 318), XP('army', 10))),
    Focus('serv_home_guard', 'Rolls of the Home Guard',
          "Every adult who has ever served, and any volunteer who wants to, is listed in district home guard rolls with a rifle, "
          "a muster point and two weekends of training a year. It is cheap and broad. A home guard can defend a town street; it "
          "cannot fight a modern army in open country.",
          ('document', 'security'), after_any=('serv_armour_store', 'serv_hait_ranges'), cost=10,
          exclusive=('serv_volunteers', 'serv_declared'), reward=(SwapIdea('disarmed_footing', 'home_guard'),)),
    Focus('serv_volunteers', 'Volunteer Coast Brigades',
          "A small professional force of volunteer brigades is raised for the coast, where the harbours and oil jetties are, and "
          "paid well enough to keep its soldiers for years. Recruits are scarce in a prosperous country and the wage bill is "
          "steep. What the brigades lack in numbers they make up in training.",
          ('medal', 'navy'), after_any=('serv_armour_store', 'serv_hait_ranges'), cost=10,
          exclusive=('serv_home_guard', 'serv_declared'), reward=(SwapIdea('disarmed_footing', 'coast_brigades'),)),
    Focus('serv_declared', 'Disarmed, and Saying So',
          "A third camp wants Nordlands to make a virtue of its posture: a declared policy of minimal forces, published defence "
          "budgets and an open invitation to neighbours to inspect them. It wins trust abroad and goodwill at home. If a crisis "
          "ever comes, the country will be asking others to keep their promises.",
          ('peace', 'diplomacy'), after_any=('serv_armour_store', 'serv_hait_ranges'), cost=10,
          exclusive=('serv_home_guard', 'serv_volunteers'), reward=(SwapIdea('disarmed_footing', 'declared_disarmament'),)),
    Focus('serv_firepower', 'A School of Massed Fire',
          "The army's doctrine already favours firepower over manpower, which suits a country with guns in storage and few "
          "soldiers. A staff school teaches officers to plan around artillery, armour and supply rather than around numbers. "
          "Places are few, and good officers leave their units for a year to fill them.",
          ('command', 'science'), after=('serv_armour_store',), reward=(Idea('firepower_school'),)),
    Focus('serv_arsenal', 'The Haugaland Arsenal',
          "Haugaland already hosts three arms plants and has its own steel. A fourth line there builds ammunition and spares for "
          "the service armour and the coastal forces, so that maintenance no longer waits on imports. It takes Haugaland's last "
          "free plot, and the pacifist press calls it a broken promise.",
          ('industry', 'security'), after_any=('serv_home_guard', 'serv_volunteers'), reward=(Build('arms_factory', 1, 373),)),
    Focus('serv_mountain_companies', 'Mountain Companies for Hait',
          "Two companies of mountain infantry form at the new Hait ranges, trained to hold passes with light weapons and to move "
          "without roads. They are the only Nordlandic troops the Wielvakian frontier posts will ever see on manoeuvre. The "
          "companies are small, and their winter allowances are the envy of every other unit.",
          ('training', 'gate'), after=('serv_hait_ranges',), reward=(XP('army', 15), Research('infantry_weapons', 0.5, 1))),
    Focus('serv_depots', 'Reserve Depots in Oregonen',
          "Oregonen also faces the Wielvakian frontier but holds almost no military stores. Dispersed depots for fuel, ammunition "
          "and spares there, with roads hard enough for tank transporters, mean that whatever force the country keeps can reach "
          "either end of the border. Councils welcome the jobs and dislike the convoys.",
          ('logistics', 'shelter'), after_any=('serv_home_guard', 'serv_volunteers', 'serv_declared'),
          reward=(Build('infrastructure', 1, 385), Research('logistics_tech', 0.5, 1))),
    Focus('serv_civil_defence', 'Civil Defence Before Divisions',
          "If the country will not field an army, it can at least protect its people. A civil defence corps trains firefighters, "
          "rescue teams and shelter wardens in every district, drawing on volunteers who would never join a military unit. It "
          "costs little, earns broad support, and leaves the generals feeling quietly sidelined.",
          ('civil', 'shelter'), after=('serv_declared',), reward=(Idea('civil_defence_corps'),)),
))

FLEET = Branch('fleet', 'The Fleet That Waits', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('fleet_doctrine', 'A Fleet Kept in Being',
          "Nordlandic naval doctrine holds that a fleet which survives deters better than a fleet which fights. Escorts and "
          "coastal submarines stay close to well-defended harbours and sail only when the odds favour them. Writing the doctrine "
          "down gives the admirals a budget argument, and gives their critics a phrase to mock.",
          ('navy', 'command'), reward=(Idea('fleet_waits'), Event('fleet_in_harbour'))),
    Focus('fleet_approach_radar', 'Radar on the Harbour Approaches',
          "The great naval harbour on the Norden Forest coast is the fleet's main base, and nothing modern watches its "
          "approaches. A coastal radar station near the harbour mouth tracks every hull and aircraft within range. It is the first piece "
          "of the warning net the doctrine depends on, and it is expensive to run.",
          ('radar', 'navy'), after=('fleet_doctrine',), reward=(Build('radar_station', 1, 277),)),
    Focus('fleet_merchant_register', 'Register Every Merchant Hull',
          "The country runs a large merchant fleet but keeps no current list of its ships, crews or routes. A register held by the "
          "admiralty records every hull flying the Nordlandic flag. Owners resent the paperwork. If a war ever closes the sea "
          "lanes, the register will decide which ships come home first.",
          ('document', 'logistics'), after=('fleet_doctrine',), reward=(Flag('merchant_register'), XP('navy', 10))),
    Focus('fleet_nyboholm', 'Nyboholm as a Second Base',
          "A single main base is a single target. Nyboholm in Tenese becomes the fleet's second home, with fuel tanks, a radar "
          "station on its approaches and berths reserved for escorts. Moving ships there costs the main base some prestige and "
          "Tenese some fishing space. Dispersal is the doctrine's oldest rule.",
          ('radar', 'security'), after=('fleet_doctrine',), reward=(Build('radar_station', 1, 368), XP('navy', 10))),
    Focus('fleet_submarines', 'Submarines Off Every Headland',
          "The submarine school wins the argument: coastal submarines are cheap, hard to find and ideal for a fleet that intends "
          "to wait. Boats patrol the approaches to every major harbour. Their crews train for years, their mistakes are rarely "
          "survivable, and the surface officers worry about their own promotions.",
          ('submarine', 'navy'), after_any=('fleet_approach_radar', 'fleet_merchant_register'), cost=10,
          exclusive=('fleet_escorts', 'fleet_mines'), reward=(Idea('sub_screen'),)),
    Focus('fleet_escorts', 'Escort Groups for the Sea Lanes',
          "The escort school argues that Nordlands lives by its merchant fleet and should guard it. Coastal escorts are grouped "
          "into flotillas that shepherd convoys through the approaches and out to sea. The groups need fuel, sea time and "
          "constant drill. They protect trade far better than they protect harbours.",
          ('navy', 'logistics'), after_any=('fleet_approach_radar', 'fleet_merchant_register'), cost=10,
          exclusive=('fleet_submarines', 'fleet_mines'), reward=(Idea('escort_groups'),)),
    Focus('fleet_mines', 'Controlled Mines for the Channels',
          "The cheapest navy is one that never sails. Controlled minefields, laid and switched from shore stations, can close the "
          "harbour channels in hours. They need constant maintenance and a trained shore staff. Fishing captains complain about "
          "restricted waters, and neighbours ask what exactly Nordlands expects to keep out.",
          ('security', 'navy'), after_any=('fleet_approach_radar', 'fleet_merchant_register'), cost=10,
          exclusive=('fleet_submarines', 'fleet_escorts'), reward=(Idea('mine_belts'),)),
    Focus('fleet_boat_school', 'The Submarine School',
          "Submarine crews take longer to train than any other sailors, and a mistake can kill everyone aboard. A dedicated school "
          "with a training boat and a shore simulator shortens the course and lowers the accident rate. It absorbs the best "
          "volunteers in the fleet, which the surface flotillas resent loudly.",
          ('training', 'submarine'), after=('fleet_submarines',), reward=(XP('navy', 20), Research('naval_equipment', 0.5, 1))),
    Focus('fleet_convoy_office', 'A Convoy Office at Djurseryd',
          "Escort groups need someone ashore to plan routes, assemble convoys and talk to shipowners. A convoy office at Djurseryd "
          "does all three, with a direct line to the admiralty. Owners resent the delays while convoys assemble. Insurers, who "
          "have long memories, cut their rates for ships that sail in company.",
          ('logistics', 'document'), after=('fleet_escorts',), reward=(Idea('convoy_office'),)),
    Focus('fleet_shore_stations', 'Shore Stations for the Mines',
          "Controlled minefields are only as good as the stations that watch and fire them. A chain of shore stations with radar "
          "and hydrophones covers the Oregonen approaches first, close to the Wielvakian coast. The stations need crews around the "
          "clock, and the treasury pays for every watch they stand.",
          ('radar', 'security'), after=('fleet_mines',), reward=(Build('radar_station', 1, 385), PP(-10))),
    Focus('fleet_puts_to_sea', 'The Fleet Puts to Sea',
          "Once a year the whole fleet sails together for a week of exercises in home waters, watched by the press and the diet. "
          "It burns fuel and wears out engines, and the admirals stage it with care. A fleet in being still has to show that it "
          "exists, and that it can move when ordered.",
          ('navy', 'medal'), after_any=('fleet_boat_school', 'fleet_convoy_office', 'fleet_shore_stations'),
          reward=(XP('navy', 25), TimedIdea('fleet_review_year', 365))),
))

BORDER = Branch('border', 'Between FATO and Wielvakia', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('bord_capital_frontier', 'A Capital on Two Borders',
          "Aspneset, the capital, sits in West Norden within reach of two frontiers, FATO and Wielvakia. Most of the country's "
          "land trade passes through the capital district. Before choosing any frontier policy, the government sets up customs "
          "desks with both neighbours, which means admitting that it never had a frontier policy at all.",
          ('gate', 'diplomacy'), reward=(Idea('frontier_desks'), Event('two_neighbours'))),
    Focus('bord_fato_desk', 'A Customs Desk with FATO',
          "Trains and trucks from FATO enter at the crossings from Granley Tips and Gangl, where inspections still follow forms "
          "written decades ago. A joint desk with FATO customs officers shares manifests, cuts waiting times and settles disputes "
          "on the spot. It changes no claim. It does require trusting another country's paperwork.",
          ('document', 'gate'), after=('bord_capital_frontier',), reward=(TimedIdea('fato_transit', 730),)),
    Focus('bord_wie_desk', 'A Customs Desk with Wielvakia',
          "The Wielvakian frontier runs past Farnlands and Vakia, touching West Norden, Hait Mountain and Oregonen. Traffic is "
          "lighter than on the FATO side but harder to watch, through mountain roads and small harbours. A shared desk sets "
          "common hours, common forms and a telephone line both sides promise to answer.",
          ('diplomacy', 'document'), after=('bord_capital_frontier',), reward=(TimedIdea('wielvakian_transit', 730),)),
    Focus('bord_belkan_sale', 'Belkan Land Changes Hands',
          "In late August 1991 Belka sells territory in its north to FATO and other lands to its eastern neighbours. A Nordlandic "
          "neighbour has just grown, and routes that once ran to Belka now cross FATO customs. Road works at the East Granley "
          "crossings prepare for traffic that nobody can yet estimate.",
          ('gate', 'scales'), after=('bord_fato_desk',), requires=(After('1991.8.29'),),
          reward=(Build('infrastructure', 1, 257),
                  Tooltip('No claim, core or border change for Nordlands; the sale is a matter between Belka and its neighbours.'))),
    Focus('bord_open', 'Open Crossings, Light Inspections',
          "With customs desks working, the government lowers inspections to spot checks and keeps the crossings open around the "
          "clock. Trade with both neighbours grows quickly and frontier towns prosper. Smuggling grows too, and the police warn "
          "that an open border is easy to cross in both directions when times turn bad.",
          ('gate', 'economy'), after_any=('bord_fato_desk', 'bord_wie_desk'), cost=10, exclusive=('bord_guarded',),
          reward=(SwapIdea('frontier_desks', 'open_crossings'), Flag('frontier_open'))),
    Focus('bord_guarded', 'Guarded Crossings, Full Inspections',
          "The cautious answer keeps every vehicle inspected and every crossing staffed by armed customs police, with hours fixed "
          "and posted. Trade grows more slowly, and frontier merchants complain about queues. The state knows what enters the "
          "country, which may matter more than the price of imports if the region turns unstable.",
          ('security', 'gate'), after_any=('bord_fato_desk', 'bord_wie_desk'), cost=10, exclusive=('bord_open',),
          reward=(SwapIdea('frontier_desks', 'guarded_crossings'), Flag('frontier_guarded'))),
    Focus('bord_through_trains', 'Through Trains Across the Frontier',
          "Open crossings let passenger and freight trains run straight through without changing crews at the border. The "
          "capital's rail yards are rebuilt for through traffic, and the country's hundred locomotives are fitted with the "
          "signalling both neighbours use. Railway unions worry about foreign crews on Nordlandic track.",
          ('rail', 'logistics'), after=('bord_open',), reward=(Build('infrastructure', 1, 292), Research('train_tech', 0.5, 1))),
    Focus('bord_market_days', 'Market Days at the Crossings',
          "Weekly markets at the crossings let farmers, craftsmen and traders from all three countries sell without filing export "
          "papers for small amounts. The markets become social events as much as commercial ones. Tax collectors lose a little "
          "revenue, and frontier towns gain a reason to think kindly of each other.",
          ('economy', 'civil'), after=('bord_open',), reward=(TimedIdea('frontier_markets', 730), Stability(0.02))),
    Focus('bord_vakia_posts', 'Watch Posts on the Vakia Line',
          "Guarded crossings need eyes between them. Watch posts with radar and radio along the Hait Mountain stretch of the "
          "Wielvakian frontier cover the passes where smugglers prefer to walk. The posts are cold, lonely and expensive to "
          "supply. Wielvakian officials ask, politely, whom exactly the posts are meant to watch.",
          ('radar', 'security'), after=('bord_guarded',), reward=(Build('radar_station', 1, 318), WarSupport(0.02))),
    Focus('bord_tariff_courts', 'Tariff Courts for the Frontier',
          "Customs disputes at guarded crossings used to wait months for a ministry ruling. Tariff courts sitting in the frontier "
          "districts decide them in days, with published judgments. Merchants learn the rules and stop bribing clerks. The courts "
          "cost judges' salaries, and the ministry loses a quiet source of influence.",
          ('scales', 'document'), after=('bord_guarded',), reward=(Idea('tariff_courts'),)),
    Focus('bord_quiet_word', 'A Quiet Word with Both Neighbours',
          "Nordlands, FATO and Wielvakia issue a short joint statement: each respects the others' frontiers and will settle "
          "incidents through the customs desks before anything else. It binds nobody to anything more. In a region where borders "
          "are being sold and redrawn, a dull statement about respecting them is worth having.",
          ('peace', 'diplomacy'), after_any=('bord_through_trains', 'bord_market_days', 'bord_vakia_posts', 'bord_tariff_courts'),
          reward=(Flag('neighbour_statement'), Stability(0.03),
                  Tooltip('A statement of mutual respect only; it creates no faction, guarantee or alliance.'))),
))

WAR = Branch('war', 'The Belkan War Beyond FATO', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_news', 'War Breaks Out Beyond FATO',
          "In March 1995 Belka goes to war. Nordlands is not a party and shares no border with Belka, but FATO does, and FATO "
          "shares one with Nordlands. The government opens a watch room at Aspneset and puts the coastal radars on full shifts. "
          "Watching costs fuel, overtime and sleep; ignoring it would cost more.",
          ('communications', 'security'), requires=(After('1995.3.25'),), reward=(Idea('war_watch'), Event('belkan_war'))),
    Focus('war_insurers', 'The Insurers Raise Their Rates',
          "Within days of the outbreak, marine insurers raise war-risk premiums on every route that touches the fighting or the "
          "Allied supply lanes. Nordlandic shipowners pass the cost on to their customers. The government cannot change the "
          "rates, but it can publish them and stop rumour from doing more damage than the war.",
          ('economy', 'navy'), after=('war_news',), reward=(TimedIdea('war_risk_premiums', 365), PP(10))),
    Focus('war_closed', 'Close the Roadsteads to Warships',
          "Nordlandic harbours close to warships of every belligerent except in distress, and merchant ships carrying war cargo "
          "are refused bunkers. The policy is strict and even-handed. Shipping houses lose business to ports that ask fewer "
          "questions, and both sides of the war suspect Nordlands of favouring the other.",
          ('security', 'navy'), after=('war_news',), cost=10, exclusive=('war_fuel', 'war_mercy'),
          reward=(SwapIdea('war_watch', 'closed_roadsteads'),)),
    Focus('war_fuel', 'Fuel for Every Flag',
          "Nordlandic ports sell fuel and provisions to any merchant ship that pays, whatever flag it flies and wherever it is "
          "bound, while warships are still refused. Oil revenue climbs. The houses cheer, the press asks awkward questions about "
          "cargo manifests, and insurers watch Nordlandic tankers more closely than before.",
          ('economy', 'logistics'), after=('war_news',), cost=10, exclusive=('war_closed', 'war_mercy'),
          reward=(SwapIdea('war_watch', 'fuel_for_all'),)),
    Focus('war_mercy', 'A Mercy Corridor by Sea',
          "The government offers Nordlandic ships and harbours to carry the wounded, the displaced and relief supplies for any "
          "side that asks, under neutral markings and with inspections both sides can witness. It is costly and risky for the "
          "crews. It also gives the country a role in the war that nobody can call partisan.",
          ('medical', 'navy'), after=('war_news',), cost=10, exclusive=('war_closed', 'war_fuel'),
          reward=(SwapIdea('war_watch', 'mercy_corridor'),)),
    Focus('war_hull_routing', 'Route Every Nordlandic Hull',
          "The merchant register proves its worth: every Nordlandic ship near the war is known, warned and routed away from the "
          "fighting. A new radar and radio station at Havnaraas tracks the ships home. Owners complain about longer voyages. The "
          "aim is simple: no Nordlandic crew should become a casualty of somebody else's war.",
          ('logistics', 'radar'), after=('war_news',), requires=(HasFlag('merchant_register'),),
          reward=(Build('radar_station', 1, 342), XP('navy', 10))),
    Focus('war_air_notices', 'Joint Notices to Airmen',
          "The quiet statement with FATO and Wielvakia gets its first test. The three countries share notices to airmen about "
          "restricted zones, diverted airliners and unidentified military traffic, so that no civilian aircraft wanders toward "
          "the war by mistake. It is technical work that keeps three nervous air forces from surprising each other.",
          ('air', 'diplomacy'), after=('war_news',), requires=(HasFlag('neighbour_statement'),),
          reward=(TimedIdea('shared_air_notices', 730),)),
    Focus('war_fallout', 'Readings from the Waldreich',
          "When nuclear devices detonate in the Waldreich Mountains, Nordlands is spared the blasts but not the fear. Monitoring "
          "stations in every district measure air, rain and milk, and the results are published daily. The stations cost little "
          "and calm a country that cannot see the thing it is afraid of.",
          ('telescope', 'medical'), after=('war_news',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(Idea('fallout_watch'),)),
    Focus('war_bunker_fuel', 'Bunker Fuel for Stranded Hulls',
          "Neutral ships stranded in Nordlandic harbours by the war cannot buy fuel at any price. The strategic reserve releases "
          "bunker fuel at cost so they can sail home, whatever flag they fly. It drains a reserve built for the country's own "
          "emergencies, and it fills the harbours with grateful captains who will remember who helped.",
          ('economy', 'shelter'), after_any=('war_closed', 'war_fuel', 'war_mercy'), requires=(HasFlag('fuel_reserve'),),
          reward=(TimedIdea('reserve_bunkers', 365),)),
    Focus('war_lumen', 'Peace Signed at Lumen',
          "When the war ends with a treaty signed at Lumen, the Allied nations begin rebuilding what was bombed, and they need "
          "steel, fuel and ships. Nordlandic yards and oil houses bid for the work. The orders are welcome, but they tie the "
          "country's next few years to other people's reconstruction budgets.",
          ('peace', 'rebuild'), after=('war_insurers',), requires=(HasGlobal('belka_lost_belkan_war'),),
          exclusive=('war_belkan_terms',), reward=(TimedIdea('allied_rebuilding', 730), Stability(0.02))),
    Focus('war_belkan_terms', 'A Peace on Belkan Terms',
          "If the war ends on Belkan terms, Nordlands must live with a stronger Belka on the far side of FATO. Trade continues, "
          "carefully. The government raises its watch on the frontier, reviews its stores and keeps its opinions out of the "
          "newspapers, waiting to learn what the new order expects of small neighbours.",
          ('security', 'scales'), after=('war_insurers',), requires=(HasGlobal('belka_won_belkan_war'),),
          exclusive=('war_lumen',), reward=(TimedIdea('cautious_trade', 730), WarSupport(0.03))),
    Focus('war_coup', 'Officers Who Answer to No Flag',
          "At the end of 1995 a group calling itself A World With No Boundaries launches a coup, and the Allied Forces defeat it "
          "at Avalon Dam. A movement that rejects every border is a strange threat to a country that has never questioned its "
          "own. The government asks quietly whether any Nordlandic officer has been listening.",
          ('security', 'command'), after=('war_news',), requires=(After('1995.12.25'),), reward=(Event('no_flag_coup'),)),
    Focus('war_report', 'What the Belkan War Taught',
          "Nordlandic officers study the war closely: how quickly air power decided battles, how exposed harbours and dams proved, "
          "and how a war beyond one neighbour reshaped trade for everyone. A short report recommends better radar, dispersed "
          "airfields and trained instructors. It is cheap advice, and the air arm reads every page.",
          ('command', 'document'), after_any=('war_lumen', 'war_belkan_terms', 'war_coup'),
          reward=(Flag('belkan_lessons'), Research('air_doctrine', 0.5, 1))),
))

AIR = Branch('air', 'An Air Arm of Eighteen', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_eighteen', 'Eighteen Fighters, Three Strikers',
          "The Nordlandic air arm owns eighteen fighters and three ground-support aircraft, flying from fields on the Nord "
          "Peninsula and outside the capital. That is enough for air policing and parades, not for war. Deciding what such a "
          "small force is for comes before any purchase, and every option leaves someone unhappy.",
          ('air', 'runway'), reward=(Idea('eighteen_fighters'), XP('air', 10))),
    Focus('air_peninsula_runway', 'Lengthen the Peninsula Runway',
          "The Nord Peninsula field covers the oil fields and the sea approaches but has a short runway and two hangars. "
          "Lengthening it, hardening the hangars and adding fuel storage makes it the air arm's main base. The work competes "
          "with the oil houses for the peninsula's scarce labour, and the oil houses pay better.",
          ('runway', 'tools'), after=('air_eighteen',), reward=(Build('air_base', 2, 254),)),
    Focus('air_forest_field', 'A Fighter Field in Norden Forest',
          "Norden Forest holds the main naval harbour and a large share of the population, yet no airfield of its own. A new "
          "field there lets fighters cover the fleet's base without flying the length of the country. Clearing the site costs "
          "forest and farmland, and the neighbours dislike the noise.",
          ('air', 'civil'), after=('air_eighteen',), reward=(Build('air_base', 2, 277),)),
    Focus('air_interceptors', 'Interceptors for the Home Sky',
          "The air arm is reorganised around interception: fast climbers, ground radar control and pilots trained to meet "
          "intruders at the coast. It suits a disarmed country that wants only to keep its sky. It does little for the fleet or "
          "the army, and the strike crews find themselves flying training sorties.",
          ('air', 'radar'), after_any=('air_peninsula_runway', 'air_forest_field'), cost=10, exclusive=('air_sea_patrol',),
          reward=(SwapIdea('eighteen_fighters', 'interceptor_wing'),)),
    Focus('air_sea_patrol', 'Patrol Wings over the Sea Lanes',
          "The air arm is reorganised around the sea: long patrols over the merchant lanes, anti-ship training and close work "
          "with the fleet. It suits a country that lives by shipping. It leaves the capital's sky to a handful of fighters, and "
          "the army wonders whether it will ever see an aircraft overhead.",
          ('air', 'navy'), after_any=('air_peninsula_runway', 'air_forest_field'), cost=10, exclusive=('air_interceptors',),
          reward=(SwapIdea('eighteen_fighters', 'sea_patrol_wing'),)),
    Focus('air_radar_chain', 'A Radar Chain for Aspneset',
          "Interception without radar is guesswork. A chain of stations around the capital district feeds a single control room "
          "that can scramble fighters and track them to the frontier. The stations sit close to FATO and Wielvakian airspace, so "
          "their coverage must be explained to both neighbours before it is switched on.",
          ('radar', 'air'), after=('air_interceptors',), reward=(Build('radar_station', 2, 292),)),
    Focus('air_strike_drill', 'Anti-Ship Drill for the Strikers',
          "The three ground-support aircraft and their crews train to hit ships rather than tanks, flying with the fleet in its "
          "exercises. It is a modest force, but a credible one in coastal waters. Crews spend more hours over the sea than any "
          "other Nordlandic airmen, and the attrition in training worries the ministry.",
          ('missile', 'navy'), after=('air_sea_patrol',), reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
    Focus('air_belkan_pilots', 'Belkan Pilots Seek Employers',
          "By the summer of 1998, former top pilots of the Belkan Air Force are being hired by other countries as aggressor "
          "squadrons. Their agents reach Aspneset too. The offer is tempting for a small air arm with no combat experience. It "
          "also raises the question of whose veterans the country wants teaching its pilots.",
          ('air', 'diplomacy'), after_any=('air_radar_chain', 'air_strike_drill'), requires=(After('1998.6.19'),),
          reward=(Event('pilots_for_hire'),)),
    Focus('air_hire_aggressors', 'Hire the Aggressor Squadron',
          "The government signs a contract with a group of former Belkan pilots to fly as an aggressor squadron against "
          "Nordlandic crews. Training quality jumps within months. Some deputies object to paying veterans of a war that "
          "frightened the whole region, and the pilots' fees exceed a Nordlandic general's salary.",
          ('medal', 'air'), after=('air_belkan_pilots',), cost=10, exclusive=('air_own_instructors',),
          reward=(Idea('aggressor_school'),)),
    Focus('air_own_instructors', 'Train Our Own Instructors',
          "The government declines the offer and builds an instructor school of its own, sending its best pilots abroad for "
          "courses and bringing them back to teach. Progress is slower and less dramatic. Every lesson learned stays inside the "
          "air arm, and nobody in the diet has to defend the fees of foreign veterans.",
          ('training', 'air'), after=('air_belkan_pilots',), cost=10, exclusive=('air_hire_aggressors',),
          reward=(Idea('home_instructors'),)),
    Focus('air_display', 'The Aspneset Air Display',
          "With new bases, new training and the lessons of the Belkan War on paper, the air arm holds a public display over the "
          "capital. Recruiting offices fill for the first time in years. The display burns a season's fuel budget in an "
          "afternoon, and the pacifist papers count every litre of it.",
          ('medal', 'runway'), after_any=('air_hire_aggressors', 'air_own_instructors'), requires=(HasFlag('belkan_lessons'),),
          reward=(XP('air', 20), TimedIdea('air_display_year', 365))),
))

SKY = Branch('sky', 'Ulysses Over the North', 1995, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_almanac', 'Ulysses in the Almanac',
          "Since the astronomers' warning of December 1994, the asteroid called Ulysses has appeared in every almanac and "
          "newspaper column. Nordlands has no observatory of note and no plan. A small sky watch office collects foreign reports, "
          "briefs ministers and answers the public's questions. It costs little and keeps rumour from filling the gap.",
          ('telescope', 'meteor'), reward=(Idea('sky_watch'),)),
    Focus('sky_announced', 'Aspneset Hears the FCU Verdict',
          "The FCU President's April 1996 statement turns the asteroid from a column in the almanac into an order of business at "
          "Aspneset. Eight of the nine districts face the sea, and only the capital lies inland. Ministers convene the sky watch, "
          "the harbour masters and the civil engineers, and ask each for a costed plan within the month.",
          ('meteor', 'communications'), after=('sky_almanac',), requires=(After('1996.4.20'),), reward=(Event('ulysses_north'),)),
    Focus('sky_hait_observatory', 'An Observatory Above Hait',
          "The heights of Hait Mountain suit a telescope and a tracking radar. A small observatory there gives Nordlands its own "
          "measurements of the asteroid and, later, of its fragments. The site is hard to reach in winter and expensive to staff. "
          "It also trains engineers in tracking, a skill with many other uses.",
          ('telescope', 'radar'), after=('sky_almanac',), reward=(Build('radar_station', 1, 318), Research('electronics', 0.5, 1))),
    Focus('sky_shelters', 'Rock Shelters Under the Cities',
          "Engineers propose shelters dug under Aspneset, Djurseryd, Nyboholm and the larger harbour towns, stocked for weeks. "
          "Concrete and tunnelling crews are diverted from every other project. If fragments fall near a city, the shelters save "
          "lives that no warning could. If they fall far away, the country has dug tunnels it must maintain for decades.",
          ('shelter', 'civil'), after=('sky_announced',), cost=10, exclusive=('sky_evacuation',),
          reward=(Idea('rock_shelters'), Flag('shelters_dug'))),
    Focus('sky_evacuation', 'An Evacuation Timetable',
          "Planners prefer timetables to tunnels. Every coastal district gets an evacuation plan with assigned trains, buses and "
          "ferries and marked routes inland, rehearsed twice a year. The rehearsals disrupt daily life. If the fragments come with "
          "notice the plan works, and if they come without it the timetable is waste paper.",
          ('logistics', 'civil'), after=('sky_announced',), cost=10, exclusive=('sky_shelters',),
          reward=(Idea('evacuation_timetable'), Flag('evacuation_planned'))),
    Focus('sky_stores', 'Grain and Fuel for a Dark Year',
          "Astronomers warn that a large impact anywhere could darken skies and ruin harvests far away. The state buys grain, "
          "seed and fuel for a full year and stores it in every district. Prices rise while the purchases last, and farmers "
          "grumble that the state bought abroad. Nobody wants to need the stores.",
          ('shelter', 'economy'), after=('sky_announced',), reward=(TimedIdea('dark_year_stores', 1095),)),
    Focus('sky_radio_wardens', 'Radio Wardens in Every District',
          "If the networks fail on the night of the impact, the country still needs to talk. Volunteer radio wardens in every "
          "district, with battery sets and fixed schedules, relay orders and reports to the capital. Amateur radio clubs supply "
          "most of the volunteers, and they enjoy being taken seriously for once.",
          ('communications', 'civil'), after_any=('sky_shelters', 'sky_evacuation'),
          reward=(Research('radar_tech', 0.5, 1), Stability(0.02))),
    Focus('sky_roche', 'Ulysses Crosses the Limit',
          "On 8 July 1999 Ulysses passes through the Earth's Roche limit. Nordlanders follow the night on the radio, from shelters "
          "or along evacuation routes, depending on what their government chose. Whatever falls and wherever it falls, the "
          "country has its plans, its stores and its wardens in place.",
          ('meteor', 'telescope'), after_any=('sky_shelters', 'sky_evacuation'), requires=(After('1999.7.8'),),
          reward=(Stability(0.03), Research('construction_tech', 0.5, 1))),
    Focus('sky_relief', 'Relief Ships for the Stricken',
          "Wherever the fragments have done harm, people need food, medicine and shelter, and Nordlands has ships, fuel and stores "
          "to spare. A relief shipping office charters merchant hulls under neutral markings and loads them from the district "
          "stores. It costs the treasury, and earns goodwill that will outlast the century.",
          ('medical', 'navy'), after=('sky_roche',), reward=(Idea('relief_shipping'),)),
    Focus('sky_debris', 'Tracking Debris in Orbit',
          "After Osea and Yuktobania agree in October 1999 to convert the Arkbird into a platform for clearing debris from "
          "satellite orbits, Nordlandic tracking stations offer their measurements to the effort. It is a modest contribution. "
          "It gives the country's engineers a seat in international work and a reason to keep their equipment current.",
          ('satellite', 'radar'), after=('sky_roche',), requires=(After('1999.10.8'),),
          reward=(Research('rocketry', 0.5, 1), Research('radar_tech', 0.5, 1))),
    Focus('sky_storehouses', 'Shelters into Storehouses',
          "With the night of the Roche limit past, the rock shelters stand empty. Leasing their dry, cool tunnels as storehouses "
          "for food, medicines and archives recovers part of their cost and keeps them maintained. The civil defence services "
          "keep the right to reclaim them within hours, and rehearse doing so every spring.",
          ('shelter', 'industry'), after=('sky_roche',), requires=(HasFlag('shelters_dug'),),
          reward=(SwapIdea('rock_shelters', 'shelter_storehouses'),)),
    Focus('sky_coast_roads', 'Evacuation Roads Kept Open',
          "The evacuation routes built for Ulysses are worth keeping. Oregonen gets the first permanent upgrade, turning temporary "
          "routes inland into proper roads with bridges rated for heavy trucks. It costs money the impact no longer justifies, "
          "and leaves the coastal districts better connected than they have ever been.",
          ('logistics', 'rebuild'), after=('sky_roche',), requires=(HasFlag('evacuation_planned'),),
          reward=(Build('infrastructure', 1, 385),)),
))

LANDS = Branch('lands', 'Nine Districts, One Budget', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('lands_ledger', 'A Ledger of Nine Districts',
          "Nordlands has nine districts of very unequal weight. West Norden and Norden Forest hold most of the people, the Nord "
          "Peninsula holds most of the oil and few residents, and the harbour towns hold most of the yards. A district ledger of "
          "roads, schools and revenue shows who pays and who benefits.",
          ('document', 'civil'), reward=(Idea('district_ledger'), Event('nine_districts'))),
    Focus('lands_forest_lines', 'Commuter Lines for Norden Forest',
          "Norden Forest is the most populous coastal district, and its workers travel long distances between forest towns, the "
          "yards at Lundegaard and the naval harbour. Commuter lines and a ring road cut those journeys. Construction closes roads "
          "for a year; afterward the workforce can reach any yard in under an hour.",
          ('rail', 'civil'), after=('lands_ledger',), reward=(Build('infrastructure', 1, 277), Stability(0.01))),
    Focus('lands_peninsula_ferries', 'Ferries for the Peninsula Towns',
          "The small towns of the Nord Peninsula rely on a single road and an irregular boat service. Regular ferries, rebuilt "
          "piers and a coast road put schools, clinics and markets within reach. Per resident, it is the most expensive service "
          "in the country. It is also how the peninsula stops feeling like an oil camp.",
          ('navy', 'civil'), after=('lands_ledger',), reward=(Build('infrastructure', 1, 254),)),
    Focus('lands_twin_harbours', 'Streets for the Twin Harbours',
          "Djurseryd and Havnaraas grew around their harbours without much planning, and their streets choke on yard traffic and "
          "commuters alike. A joint works programme separates freight from passengers and rebuilds the harbour roads. "
          "Shopkeepers lose trade while the roads are dug up and win it back once the trucks stop parking outside.",
          ('rebuild', 'civil'), after=('lands_ledger',), reward=(Build('infrastructure', 1, 342),)),
    Focus('lands_hait_works', 'Tungsten Works Under Hait',
          "Hait Mountain holds the country's tungsten and some chromium, which until now has left as raw ore. A processing works "
          "near the mines turns it into alloys for tools, drills and armour plate. It fills Hait Mountain's last industrial plot. "
          "Mine dust and truck traffic are the price the district pays.",
          ('industry', 'tools'), after=('lands_ledger',), reward=(Build('industrial_complex', 1, 318),)),
    Focus('lands_councils', 'Councils for Every District',
          "Each district receives an elected council with its own budget for roads, schools and clinics, while the capital keeps "
          "defence, foreign affairs and the currency. Local projects move quickly and local loyalties strengthen. The poorer "
          "districts find their budgets small, and the richer ones resent subsidising them.",
          ('assembly', 'ballot'), after_any=('lands_forest_lines', 'lands_peninsula_ferries', 'lands_twin_harbours'), cost=10,
          exclusive=('lands_works',), reward=(SwapIdea('district_ledger', 'district_councils'), Flag('districts_devolved'))),
    Focus('lands_works', 'One Ministry of Works',
          "A single ministry of works in Aspneset plans every road, school and harbour wall in the country to one national "
          "standard. Projects are coordinated and the poorer districts get their share. Local officials lose control over local "
          "spending, and every pothole in every district becomes the capital's fault.",
          ('command', 'tools'), after_any=('lands_forest_lines', 'lands_peninsula_ferries', 'lands_twin_harbours'), cost=10,
          exclusive=('lands_councils',), reward=(SwapIdea('district_ledger', 'works_ministry'), Flag('districts_central'))),
    Focus('lands_skogaholm', 'Workshops at Skogaholm',
          "Oregonen's council spends its new budget on light industry: workshops at Skogaholm for marine engines, pumps and "
          "electrical gear, near the harbour and the Wielvakian frontier. It is the district's own project, planned by its own "
          "council. The capital doubts the business case and waits to see whether it holds.",
          ('tools', 'civil'), after=('lands_councils',), reward=(Build('industrial_complex', 1, 385),)),
    Focus('lands_haugaland_roads', 'Haugaland Mine Roads',
          "The ministry of works starts with Haugaland, whose oil wells, steel ore and arms plants share narrow roads with village "
          "traffic. Graded mine roads and a heavy-load bridge open the district to modern trucks. The ministry chose the project "
          "on national grounds, and Haugaland's villages were not asked first.",
          ('logistics', 'industry'), after=('lands_works',),
          reward=(Build('infrastructure', 1, 373), Research('construction_tech', 0.5, 1))),
    Focus('lands_capital_housing', 'Housing for Aspneset',
          "Aspneset draws workers from every district and has never built enough homes for them. A housing programme of rental "
          "blocks and cheap loans eases the shortage over several years. Construction crews are pulled from other work, and "
          "landlords lobby hard against it. If it works, rents stop outrunning wages.",
          ('civil', 'rebuild'), after_any=('lands_councils', 'lands_works'),
          reward=(TimedIdea('housing_drive', 730), Stability(0.02))),
    Focus('lands_accord', 'The Districts Accord',
          "Whatever balance of councils and ministry the country settled on, the nine districts sign an accord fixing their shares "
          "of national revenue and the rules for resolving disputes. It is dry reading. It replaces years of annual haggling with "
          "a formula, and lets the treasury forecast district spending a decade ahead.",
          ('peace', 'scales'), after_any=('lands_skogaholm', 'lands_haugaland_roads', 'lands_capital_housing'),
          reward=(Flag('districts_accord'), Stability(0.02))),
))

SUSTAIN = Branch('sustain', 'Repair Before Replace', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('sus_plan', 'The Physical Sustainment Plan',
          "Nordlands owns more equipment than it can afford to replace: trucks, trains, armour, escorts and aircraft bought in "
          "better-funded years. The sustainment plan sets priorities for maintenance, spares and transport so that what exists "
          "keeps working. It is an unglamorous budget, and it competes with every new purchase.",
          ('tools', 'logistics'), reward=(Idea('sustainment_plan'), Research('logistics_tech', 0.5, 1))),
    Focus('sus_polytechnic', 'A Polytechnic at Aspneset',
          "Engineers, technicians and mechanics are trained at a new polytechnic in the capital, with workshops funded by the yards, "
          "the oil houses and the armed services. It takes years to graduate the first class. Its graduates will maintain the "
          "country's machines and, eventually, design some of them.",
          ('science', 'document'), after=('sus_plan',), reward=(Idea('polytechnic'),)),
    Focus('sus_rolling_stock', 'One Hundred Locomotives',
          "The country's hundred locomotives and their wagons are overdue for overhaul, and many lack spare parts. A rolling stock "
          "programme rebuilds engines, standardises couplings and stocks parts in district depots. Freight suffers while engines "
          "are in the shops. Afterward the railways keep schedules the country had almost forgotten.",
          ('rail', 'tools'), after=('sus_plan',), reward=(Research('train_tech', 0.75, 1), PP(-10))),
    Focus('sus_truck_pools', 'Truck Pools in Every District',
          "Thousands of military trucks sit in storage while districts hire private haulers for public works. Pooling the trucks "
          "in district depots, crewed by reservists, puts them to work on roads and relief while keeping them maintained. The "
          "army worries about wear, and private haulers complain about unfair competition.",
          ('logistics', 'civil'), after=('sus_plan',), reward=(TimedIdea('truck_pools', 730),)),
    Focus('sus_licences', 'Build Under Licence',
          "The cheapest way to replace worn equipment is to build proven foreign designs under licence, with Nordlandic factories "
          "assembling kits and slowly making more of the parts themselves. It is quick and reliable. Royalties flow abroad, "
          "resale is restricted, and the country's engineers learn to copy well rather than to invent.",
          ('document', 'industry'), after=('sus_polytechnic',), cost=10, exclusive=('sus_design',), reward=(Idea('licensed_kits'),)),
    Focus('sus_design', 'Our Own Design Offices',
          "The polytechnic's best graduates staff national design offices for trucks, radios and small vessels. Designs take years "
          "and early versions disappoint. In time the country can build equipment suited to its own coast and frontier rather "
          "than to someone else's war, and sell it to others with the same needs.",
          ('science', 'tools'), after=('sus_polytechnic',), cost=10, exclusive=('sus_licences',), reward=(Idea('home_designs'),)),
    Focus('sus_capital_works', 'Repair Works at Aspneset',
          "A large central repair works near the capital's rail yards rebuilds engines, gearboxes and electrical systems for every "
          "service and ministry. It takes the last free industrial plot in West Norden. Centralising repair saves money and builds "
          "expertise, though distant districts wait longer for their vehicles to return.",
          ('industry', 'tools'), after_any=('sus_rolling_stock', 'sus_truck_pools'), reward=(Build('industrial_complex', 1, 292),)),
    Focus('sus_field_engineers', 'Field Engineers from the Polytechnic',
          "Polytechnic students spend a term with army engineers and the ministry of works, building bridges, clearing roads and "
          "repairing harbour walls. They learn practical skills, and the state gets cheap labour on real projects. Professors "
          "complain about lost teaching time, and the engineers complain about the students.",
          ('training', 'tools'), after=('sus_polytechnic',),
          reward=(Research('engineers_tech', 0.5, 1), Research('construction_tech', 0.5, 1))),
    Focus('sus_instrument_labs', 'Instrument Labs for the Fleet',
          "Radar sets, sonars and radios fail more often than hulls do. Instrument laboratories at the polytechnic test, repair "
          "and eventually improve the electronics the fleet and the air arm depend on. The labs need costly equipment and patient "
          "staff, and they produce the first Nordlandic electronic designs worth selling abroad.",
          ('science', 'navy'), after_any=('sus_licences', 'sus_design'), reward=(Research('electronics', 0.5, 2),)),
    Focus('sus_fuel_chemistry', 'Fuel Chemistry Laboratories',
          "The oil fields produce crude that needs careful refining, and the fleet burns fuel it cannot afford to waste. Chemistry "
          "laboratories study refining, lubricants and fuel blends. Their work saves money in small amounts across thousands of "
          "engines, and keeps the refineries from leaning entirely on foreign technical advice.",
          ('science', 'economy'), after=('sus_instrument_labs',),
          reward=(Research('synth_resources', 0.5, 1), Research('industry', 0.5, 1))),
    Focus('sus_spares', 'A Spares Catalogue for Everything',
          "Every vehicle, ship and aircraft the state owns is listed with its parts, suppliers and repair intervals in a single "
          "catalogue. Depots order spares before failures, not after them. Compiling the catalogue takes years of clerical work. "
          "Once finished, it turns the sustainment plan from a promise into a routine.",
          ('document', 'logistics'), after_any=('sus_capital_works', 'sus_instrument_labs'),
          reward=(SwapIdea('sustainment_plan', 'spares_catalogue'),)),
))

CENTURY = Branch('century', 'The Principality at the Millennium', 2001, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_review', 'Ten Years in Review',
          "A decade after the crown first took stock, an independent commission reviews how the principality governs itself and "
          "what its choices have cost. Its members include judges, harbour officials and district deputies chosen by lot. The "
          "review sets the agenda for the new century, and every faction has already drafted its response.",
          ('document', 'assembly'), reward=(Event('decade_review'),)),
    Focus('cent_cabinet', 'The Cabinet Charter in Writing',
          "Ten years of cabinet government become a written constitution: the crown's duties, the cabinet's responsibility, the "
          "diet's powers and the courts' right to review laws. Drafting takes two sessions and several compromises. Once ratified, "
          "no future government can quietly reverse the arrangement without asking the diet first.",
          ('scales', 'ballot'), after=('cent_review',), requires=(HasFlag('path_cabinet'),),
          reward=(SwapIdea('cabinet_charter', 'written_constitution'),)),
    Focus('cent_privy', 'The Privy Office Codified',
          "The privy office's powers, so far exercised by custom and decree, are codified in a single statute. Officials know the "
          "limits of their authority, and the diet knows what it may still question. Codification makes the office harder to "
          "challenge and easier to predict, and both qualities help investors more than ideologues.",
          ('command', 'scales'), after=('cent_review',), requires=(HasFlag('path_privy'),),
          reward=(SwapIdea('privy_seals', 'codified_office'),)),
    Focus('cent_diet', 'A Diet Elected by District',
          "The diet government reforms its own elections so that each of the nine districts returns members in proportion to its "
          "people, with a guaranteed minimum for the smallest. The Nord Peninsula finally has a voice to match its oil. Larger "
          "districts complain about the weighting, and the reform takes a full session to pass.",
          ('ballot', 'scales'), after=('cent_review',), requires=(HasFlag('path_diet'),),
          reward=(SwapIdea('diet_mandate', 'district_diet'),)),
    Focus('cent_houses', 'Houses That Answer for Prices',
          "After a decade of rule by chartered houses, a price commission begins to publish what the houses charge for fuel, "
          "freight and harbour services, and to cap the worst abuses. The houses accept it rather than face anger in the harbour "
          "towns. Profits narrow, legitimacy improves, and both sides claim victory.",
          ('economy', 'scales'), after=('cent_review',), requires=(HasFlag('path_houses'),),
          reward=(SwapIdea('harbour_houses', 'chartered_houses'),)),
    Focus('cent_oath', 'The Oath Renewed Before the Diet',
          "The officers who swore the new oath a decade ago renew it before the diet whose recall began the reforms, in a "
          "ceremony broadcast to every district. It changes no law. It reminds a generation that has known only calm that its "
          "government rests on promises kept in public, and that such promises can lapse.",
          ('medal', 'assembly'), after=('cent_review',), requires=(HasFlag('oath_sworn'), HasFlag('diet_summoned')),
          reward=(TimedIdea('jubilee_year', 365),)),
    Focus('cent_open_accounts', 'Ten Years of the Civil List',
          "Publishing the civil list became a habit, and the habit now extends to every ministry: salaries, contracts and grants "
          "above a modest threshold are printed each year. Officials grumble about journalists. Contractors learn that inflated "
          "invoices will be read by their competitors, and prices quietly fall.",
          ('scales', 'document'), after=('cent_review',), requires=(HasFlag('civil_list_published'),),
          reward=(Idea('open_accounts'),)),
    Focus('cent_district_budgets', 'District Budgets Made Permanent',
          "The district councils have proven their worth, and their budgets are made permanent with a guaranteed share of national "
          "revenue. Tenese uses its first secure allocation to rebuild the coast road beyond Nyboholm. The capital gives up some "
          "control over spending, and the districts gain the confidence to plan beyond one year.",
          ('assembly', 'logistics'), after=('cent_review',), requires=(HasFlag('districts_devolved'),),
          reward=(Build('infrastructure', 1, 368),)),
    Focus('cent_second_works', 'A Second National Works Plan',
          "The ministry of works launches a second national plan, starting with the Tenese coast road, which it plans, funds and "
          "builds from Aspneset to one national standard. The work is fast and uniform. Local complaints are logged, answered by "
          "letter and rarely acted upon, which the ministry calls efficiency.",
          ('command', 'logistics'), after=('cent_review',), requires=(HasFlag('districts_central'),),
          reward=(Build('infrastructure', 1, 368), PP(15))),
    Focus('cent_trade_zone', 'A Frontier Trade Zone',
          "A decade of open crossings has made the frontier districts the most commercial in the country. A trade zone with "
          "simplified duties and shared warehouses at the crossings formalises what traders already do. It changes no border. It "
          "does make Nordlandic prosperity depend on the good behaviour of two neighbours.",
          ('economy', 'gate'), after=('cent_review',), requires=(HasFlag('frontier_open'),),
          reward=(SwapIdea('open_crossings', 'frontier_trade_zone'),)),
    Focus('cent_frontier_police', 'A Frontier Police Service',
          "A decade of guarded crossings has produced a corps of experienced customs police. Merging them into a single frontier "
          "police service, with its own training school and career ladder, makes the arrangement permanent. It costs salaries and "
          "pensions. Smugglers find the frontier harder to cross, and honest traders find it no easier.",
          ('security', 'document'), after=('cent_review',), requires=(HasFlag('frontier_guarded'),),
          reward=(SwapIdea('guarded_crossings', 'frontier_police'),)),
    Focus('cent_accord_holds', 'The Accord Holds',
          "Years after the districts signed their accord, no district has walked out of it and no budget has been held hostage. "
          "The treasury marks the anniversary by funding a modest round of works in every district at once. It is not a dramatic "
          "occasion, and quiet occasions are exactly what the accord was meant to produce.",
          ('peace', 'civil'), after=('cent_review',), requires=(HasFlag('districts_accord'),),
          reward=(TimedIdea('accord_dividend', 730),)),
))

DISTANT = Branch('distant', 'Oil, Hulls and a Distant War', 2002, 'FOCUS_FILTER_INDUSTRY', (
    Focus('dist_books', 'Order Books for a New Century',
          "At the turn of the century the yards and the oil houses review their order books together for the first time, with "
          "the treasury and the admiralty in the room. Each industry learns what the others expect over the next five years. The "
          "exercise is overdue, and several managers discover they have been courting the same customers.",
          ('economy', 'document'), reward=(TimedIdea('export_drive', 730),)),
    Focus('dist_merchant', 'Tankers for a Wider Market',
          "The yards that chose foreign owners a decade ago now have a reputation, and tanker orders arrive from every ocean as "
          "freight rates climb. The yards specialise in mid-sized tankers built quickly and to price. It is good business while "
          "it lasts, and every yard manager knows that booms end.",
          ('navy', 'economy'), after=('dist_books',), requires=(HasFlag('yard_model_merchant'),),
          reward=(SwapIdea('merchant_books', 'tanker_yards'),)),
    Focus('dist_navy', 'A Second Escort Series',
          "The escort class the navy ordered in the nineties is ageing, and the yards that built it are ready for a second class "
          "with better sensors and longer range. Steady naval orders keep the workforce together through any shipping slump. The "
          "treasury pays, as it always has for this model.",
          ('navy', 'security'), after=('dist_books',), requires=(HasFlag('yard_model_navy'),),
          reward=(SwapIdea('home_hulls', 'second_series'), XP('navy', 10))),
    Focus('dist_repair', 'Refits for Foreign Fleets',
          "Merchant hulls worn by long voyages need refits, and the repair basins built in the nineties are among the best "
          "equipped in the region. Owners from many nations book months ahead. The yards accept only commercial hulls, which "
          "keeps the country out of anyone's war and inside everyone's order book.",
          ('tools', 'economy'), after=('dist_books',), requires=(HasFlag('yard_model_repair'),),
          reward=(SwapIdea('repair_basins', 'refit_contracts'),)),
    Focus('dist_crown_oil', 'Shares in the Crown Oil Company',
          "The crown oil company sells a minority of its shares to Nordlandic savers and keeps control with the state. The sale "
          "raises capital for new wells as prices climb, and it gives thousands of families a stake in the peninsula. "
          "Shareholders now attend meetings, and they ask harder questions than ministers ever did.",
          ('economy', 'command'), after=('dist_books',), requires=(HasFlag('oil_model_crown'),),
          reward=(SwapIdea('crown_wells', 'listed_crown_oil'),)),
    Focus('dist_royalties', 'Royalty Courts for the Peninsula',
          "Licensed drillers and the state have argued for a decade over how royalties are measured. Royalty courts with technical "
          "assessors settle disputes quickly and publish their rulings. Drillers pay what they owe more promptly. The peninsula "
          "towns, which receive a share, see their revenues become predictable at last.",
          ('scales', 'tools'), after=('dist_books',), requires=(HasFlag('oil_model_licensed'),),
          reward=(SwapIdea('licensed_fields', 'royalty_courts'),)),
    Focus('dist_fund', 'The Fund Pays Its First Dividend',
          "The oil savings fund has grown large enough to pay a modest annual dividend into long-term works without touching its "
          "capital. The first payment rebuilds schools and harbour walls across the districts. Politicians already argue about "
          "raising the payout, and the fund's trustees already argue back.",
          ('scales', 'civil'), after=('dist_books',), requires=(HasFlag('oil_model_fund'),),
          reward=(SwapIdea('oil_fund', 'fund_dividend'),)),
    Focus('dist_news', 'Erusea Invades San Salvacion',
          "When Erusea invades the neutral country of San Salvacion, a war begins on the Usean continent. It is an ocean away "
          "from Nordlands, yet tanker routes, insurance rates and fuel prices answer to it within weeks. Shipowners call the "
          "admiralty for guidance, and the oil houses call the treasury for permission.",
          ('communications', 'navy'), after=('dist_books',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(Event('distant_war'),)),
    Focus('dist_charter_abroad', 'Charter Our Tankers Abroad',
          "Nordlandic tankers are chartered to carry fuel for neutral buyers far from the fighting, at freight rates the war has "
          "driven up. No cargo goes to a belligerent. Owners have their best years in memory, and the treasury taxes them "
          "accordingly. Crews sail longer routes, and the insurers watch every voyage.",
          ('economy', 'navy'), after=('dist_news',), cost=10, exclusive=('dist_tankers_home',), reward=(Idea('tanker_boom'),)),
    Focus('dist_tankers_home', 'Keep the Tankers in Home Waters',
          "The government asks owners to keep the tanker fleet on home and regional routes, supplying Nordlandic harbours and "
          "neighbours at stable prices. Owners lose the war premium and complain loudly. The country keeps its fuel cheap and its "
          "ships close, and nobody abroad can say that Nordlandic oil fed the war.",
          ('navy', 'peace'), after=('dist_news',), cost=10, exclusive=('dist_charter_abroad',), reward=(Idea('home_bunkering'),)),
    Focus('dist_averted', 'A War That Did Not Come',
          "Talks keep Erusea from war, and the expected surge in freight rates never arrives. Shipowners who bought tankers on "
          "credit are left with idle hulls. The treasury helps them through a lean year, and the admiralty notes with relief that "
          "its convoy plans can stay in their drawers.",
          ('peace', 'scales'), after=('dist_books',), requires=(HasGlobal('ac_ucw_war_averted'),),
          reward=(TimedIdea('calm_seas', 365), Stability(0.02))),
    Focus('dist_close_books', 'The Balance Sheet of 2005',
          "At the end of the programme's first era the treasury prints a balance sheet of the principality: its yards, wells, "
          "frontier, fleet and nine districts, and what each has cost. It is a baseline for whoever governs next. It promises "
          "nothing about the years ahead, which the region has taught everyone to respect.",
          ('document', 'scales'),
          after_any=('dist_charter_abroad', 'dist_tankers_home', 'dist_averted', 'dist_merchant', 'dist_navy', 'dist_repair'),
          requires=(After('2005.1.1'),),
          reward=(Stability(0.03), Tooltip('Closes the 1991 to 2005 programme; later eras are written separately.'))),
))

BRANCHES = (CROWN, YARDS, OIL, SERVICE, FLEET, BORDER, LANDS, SUSTAIN, AIR, WAR, SKY, CENTURY, DISTANT)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('crown_audience', 'A Crown Audience at Aspneset',
                'Open the palace for a day of petitions from every district. Costs political power; improves stability a little, once a year.',
                25, (Stability(0.02),), requires=(Completed('crown_sits'),), cooldown=365),
    DecisionDef('fleet_sortie', 'Sortie the Fleet in Being',
                'Send the fleet to sea for a week of drills. Costs political power and fuel; grants naval experience every half year.',
                35, (XP('navy', 10),), requires=(Completed('fleet_doctrine'),), cooldown=180),
    DecisionDef('harbour_dues', 'Waive Harbour Dues for a Season',
                'Waive dues for merchant hulls to win foreign orders. Costs political power; repeatable once a year.',
                40, (TimedIdea('dues_waived', 120),), requires=(HasFlag('yard_model_merchant'),), cooldown=365),
    DecisionDef('shelter_drill', 'A National Shelter Drill',
                'Rehearse the Ulysses plans in every district. Costs political power and a little calm; raises readiness yearly.',
                30, (WarSupport(0.02), Stability(-0.01)), requires=(Completed('sky_announced'),), cooldown=365),
    DecisionDef('peninsula_strip', 'A Dispersal Strip on the Peninsula',
                'Build a dispersal airstrip near the peninsula oil fields. Costs political power; once only.',
                60, (Build('air_base', 1, 254),), requires=(Completed('air_peninsula_runway'),)),
    DecisionDef('tariff_sweep', 'Sweep the Smuggling Roads',
                'Send the frontier police along the back roads between the guarded crossings for a week. Costs political power; once only.',
                50, (Event('contraband'),), requires=(HasFlag('frontier_guarded'),)),
    DecisionDef('fuel_release', 'Release Reserve Fuel to Industry',
                'Sell part of the strategic fuel reserve to factories for a season. Costs political power; repeatable once a year.',
                20, (TimedIdea('reserve_release', 90),), requires=(HasFlag('fuel_reserve'),), cooldown=365),
)
