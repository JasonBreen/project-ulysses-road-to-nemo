"""Nihon (NIH): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a monarchism ruling party at zero
popularity, with the national movement at 50 and the non-aligned establishment at 48 percent,
elections not allowed, an inherited constitutional_monarchy crown character), the crown_office
institution profile, the eight 1991 states with their neutral district captions, the country
names in countries_l_english.yml, the starting units and the global flags other mod scripts
already set. Official: ACES Chronicle rows used only as date anchors for distant pressures,
each cited by its exact key. Everything else, including every Nihonian choice, office, idea,
building, decision and event, is provisional gameplay. Nothing here is drawn from any real
country.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='NIH', name='Nihon', root='world', package='nih',
                  themes=('navy', 'logistics', 'command'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party monarchism with elections_allowed = no (election_frequency 48); '
           'popularities fascism 50, neutrality 48, democratic 1, communism 1, monarchism 0; stability and war support 0.5; '
           'three research slots including tech_mountaineers and early_fighter. The leader is the inherited crown character '
           'NIH_emperor_yamato (constitutional_monarchy), recorded by the registry as a named inherited individual whose '
           'official term is not certified; the tree refers only to the throne and the crown office and never names a new '
           'holder. Institution profile crown_office, capacity 40; party is context, not proof of constitutional form. '
           'Country names: Empire of Nihon (monarchism and fascism), Nihonian State (neutrality), Republic of Nihon '
           '(democratic), People\'s Republic of Nihon (communism).',
           'mod/2985041246/history/countries/NIH - Nihon.txt; mod/2985041246/common/characters/NIH.txt; '
           'mod/2985041246/localisation/english/countries_l_english.yml; tools/institutions/profiles.json; '
           'tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Geography: eight 1991 states. Main island: 165 (capital, megalopolis, captioned Nihon Capital District; hills, '
           'jungle and one mountain province; 4 civilian, 2 arms, 4 dockyards and the fuel silo, so one free shared slot; '
           'naval base 3, air base 1, infrastructure 2; victory point Nihon Capital Centre); 251 (District E, large town, '
           'jungle and hills; 3 civilian and 2 arms with no free slot; air base 1; logistics centre 1792); 582 (District H, '
           'large town, jungle; 3 civilian and 2 arms with no free slot; no air base; logistics centre 9531); 130 (District '
           'B, town, jungle and two hill provinces, nothing built, infrastructure 0, four free slots). The capital, E and H '
           'hold all the oil (28), steel (24), aluminium (13) and rubber (6). Level-2 railways join the capital to E and to '
           'H only. Outer districts, each a coastal town with four free slots and no land link: 84 (District A, two jungle '
           'provinces, one naval base, southwest of the main island); 239 (District D, ten jungle provinces, every one '
           'coastal, five naval bases); 524 (District G, two plains provinces, two naval bases, add_claim_by = SOA, far '
           'nearer the Sotoan coast than the capital); 431 (nine plains and hill provinces, all coastal, one naval base, far '
           'to the north and nearer Malynea and Monstrua than the capital). State 431 has only an Earth-template caption '
           'and no neutral label, so the tree calls it the northern outlier, a description and not a name. No land '
           'neighbours; Sotoa lies across the eastern sea and the Usean coast beyond the western sea, computed from '
           'map/provinces.bmp province centroids with the map wrap.',
           'mod/2985041246/history/states/84-State_84.txt, 130-State_130.txt, 165-State_165.txt, 239-State_239.txt, '
           '251-State_251.txt, 431-State_431.txt, 524-State_524.txt, 582-State_582.txt; mod/2985041246/map/definition.csv; '
           'mod/2985041246/map/railways.txt; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role island service network; 10 civilian, 6 military and 4 naval '
           'factories; six infantry formations in pairs at the capital centre and the two logistics centres; 72 fighters and '
           '12 support aircraft split between the capital and District E air bases; the NIH Maritime Service of five '
           'coastal escorts and two coastal submarines at the capital naval base; 248 convoys; civilian economy, export '
           'focus and volunteer only laws; grand doctrines superior firepower, fleet in being and operational integrity; '
           'research priority Physical Sustainment. Fiscal figures (GDP 160, growth 3.0) are fictional calibration, not '
           'canon national accounts.',
           'tools/world_starts/profiles.json; tools/world_starts/sustainment.json; docs/WORLD_STARTS_CALIBRATION.md; '
           'tools/economy_v2/profiles.json; mod/2985041246/history/units/NIH_ws_land.txt, NIH_ws_air.txt, NIH_ws_navy.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses will pass close to the Earth with a chance of impact. '
           'Opens the asteroid branch; no Nihonian role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Opens the distant-wars branch; Nihon takes no part.', '1995 / 03.25'),
    Source('Official',
           'Date anchor: rebel forces in the Skully Islands of southern Usea are defeated. Used only as the date gate of the '
           'southern lane focus; no person is named and no Nihonian role is claimed.', '1995 / 12.31'),
    Source('Official',
           'Date anchor: the FCU announces that Ulysses will impact the Earth. Gate of the impact focus and event; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Date anchor: a coup is carried out across Usea and the rebels are defeated by Unified Command. Gate of the coup '
           'focus and event; no Nihonian role is claimed.', '1997 / 05.30'),
    Source('Official',
           'Date anchor: the FCU completes Stonehenge in a desert region of neutral San Salvacion. Gate of the railgun study '
           'focus.', '1998 / 06.19'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche limit focus and event; no '
           'damage in Nihon is claimed.', '1999 / 07.08'),
    Source('Official',
           'Erusea invades San Salvacion and seizes Stonehenge. Background for the 2003 crisis focus, which is written so '
           'that the mod may still avert the war; the war focus reads the mod flag instead.', '2003 / SUMMER'),
    Source('Official',
           'Date anchor: the ISAF establishes its headquarters in North Point. Gate of the tanker run focus; no Nihonian '
           'forces are committed.', '2004 / 09.16'),
    Source('Official',
           'Farbanti falls and the Continental War ends. Background only; the outcome focuses read the mod outcome flags.',
           '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt); '
           'ac_ucw_war_started, ac_ucw_war_averted, ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory '
           '(common/scripted_effects/ac_ucw.txt). Each reaction is a leaf or late focus, so no outcome blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Nihonian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects. The District G focuses '
           'answer the Sotoan claim with civil administration only and change no claim; wartime trade focuses commit no '
           'forces abroad.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the throne
    IdeaDef('throne_inquiry', "The Throne's Inquiry",
            'Every camp has been asked in writing who should govern the islands, and every camp is answering.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('chamber_promise', 'The Promised Chamber', 'A date is set for an elected island chamber; the movement campaigns against it.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('houses_at_court', 'Shipping Houses at Court', 'Shipowners, refinery directors and harbour boards hold the ministries.',
            {'political_power_gain': 0.10, 'industrial_capacity_dockyard': 0.04}, ('economy', 'command')),
    IdeaDef('movement_ministries', 'The Movement in the Ministries',
            'The national movement staffs the ministries, the police and the radio in the name of the throne.',
            {'war_support_factor': 0.06, 'political_power_gain': 0.10, 'stability_factor': -0.03}, ('security', 'assembly')),
    IdeaDef('island_seats', 'A Bench for the Outer Districts', 'Reserved chamber seats for District A, District D, District G and the north.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'navy')),
    IdeaDef('directory_accounts', 'Quarterly Directory Accounts', 'Freight, fuel, wages and contracts published house by house.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_gain': 0.10}, ('document', 'economy')),
    IdeaDef('harbour_wardens', 'Wardens on the Quays', 'Movement wardens check papers, cargoes and crews at every landing.',
            {'stability_factor': 0.05, 'war_support_factor': 0.05, 'consumer_goods_factor': 0.03}, ('security', 'civil')),
    IdeaDef('court_household', 'A Working Court', 'The throne keeps an office, not a household sized for a richer century.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': -0.02}, ('scales', 'command')),
    IdeaDef('settled_throne', 'The Crown Statute', 'One written law sets what the throne may sign, refuse and delay.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05}, ('scales', 'document')),
    # the eight districts
    IdeaDef('circuit_reports', 'Reports from the Circuit', 'Engineers, clerks and a doctor have visited every landing in the country.',
            {'production_speed_infrastructure_factor': 0.08}, ('navy', 'document')),
    IdeaDef('crown_ferries', 'The Crown Ferry Service', 'A state service sails to every district each week at fixed fares.',
            {'production_speed_infrastructure_factor': 0.12, 'supply_consumption_factor': -0.03}, ('navy', 'command')),
    IdeaDef('island_carriers', 'Licensed Island Carriers', 'Private carriers keep the routes on condition of fixed outer-island calls.',
            {'consumer_goods_factor': -0.03, 'production_speed_infrastructure_factor': 0.08}, ('economy', 'navy')),
    IdeaDef('island_timetable', 'The Eight-District Timetable', 'One printed sheet joins the ferries to the two capital rail lines.',
            {'supply_consumption_factor': -0.04, 'stability_factor': 0.02}, ('logistics', 'document')),
    IdeaDef('g_district_office', 'The District G Office', 'A clerk, a postmaster, a nurse and a magistrate on the plains district.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('civil', 'scales')),
    IdeaDef('ferry_crews', 'Salaried Ferry Crews', 'Ferry crews on fixed salaries with pensions and a hall in every home port.',
            {'navy_org_factor': 0.03, 'stability_factor': 0.02}, ('civil', 'navy')),
    IdeaDef('ferry_inspectors', 'The Ferry Inspectorate', 'Unannounced inspectors count calls, fares and lifejackets.',
            {'production_speed_infrastructure_factor': 0.05, 'political_power_gain': 0.05}, ('scales', 'security')),
    IdeaDef('wet_season_round', 'The Wet-Season Round', 'Ferries and escorts keep the outer calls through the storm months.',
            {'naval_coordination': 0.03, 'stability_factor': 0.02}, ('navy', 'logistics')),
    # the merchant fleet
    IdeaDef('merchant_register', 'The Island Hull Register', 'Owner, tonnage, age and crew of every hull on one register.',
            {'industrial_capacity_dockyard': 0.03}, ('navy', 'document')),
    IdeaDef('hiring_halls', 'Public Hiring Halls', 'Every berth, rate and complaint posted in the three main ports.',
            {'navy_org_factor': 0.03, 'training_time_factor': -0.05}, ('training', 'navy')),
    IdeaDef('home_flag_fleet', 'The Home Flag Fleet', 'Every hull registered, crewed and repaired at home, and callable in a crisis.',
            {'industrial_capacity_dockyard': 0.06, 'navy_org_factor': 0.03}, ('navy', 'command')),
    IdeaDef('open_registry', 'The Open Island Registry', 'Foreign owners fly the island flag for low fees and few questions.',
            {'political_power_gain': 0.10, 'consumer_goods_factor': -0.03}, ('diplomacy', 'economy')),
    IdeaDef('hull_mutual', 'The Capital Hull Mutual', 'Island shipowners insure one another at cost under a treasury guarantee.',
            {'naval_speed_factor': 0.03, 'consumer_goods_factor': -0.02}, ('scales', 'navy')),
    IdeaDef('lane_watch', 'The Shore Radio Watch', 'Every master reports by radio and every silence raises an alarm.',
            {'naval_coordination': 0.04, 'air_detection': 0.03}, ('communications', 'navy')),
    IdeaDef('cadet_school', 'The Merchant Cadet School', 'Mates, engineers and radio officers trained to one standard.',
            {'navy_org_factor': 0.04}, ('training', 'document')),
    IdeaDef('registry_fees', 'Registry Fee Receipts', 'Hard-currency registration fees from foreign owners.',
            {'political_power_gain': 0.10, 'industrial_capacity_factory': 0.03}, ('economy', 'document')),
    IdeaDef('register_audited', 'A Freshly Audited Register', 'Paper hulls struck off and subsidies recovered this year.',
            {'political_power_factor': 0.05}, ('document', 'scales')),
    # wells and plant towns
    IdeaDef('well_ledger', 'The Well Ledger', 'Every well, seam and mill on the main island surveyed and costed.',
            {'production_speed_buildings_factor': 0.04}, ('economy', 'document')),
    IdeaDef('hill_refinery', 'The Hill Refinery', 'Capital crude refined at home below the hills instead of shipped abroad.',
            {'production_speed_buildings_factor': 0.05, 'supply_consumption_factor': -0.02}, ('industry', 'tools')),
    IdeaDef('retooled_towns', 'The Retooled Plant Towns', 'New tools, new lines and longer runs in District E and District H.',
            {'production_factory_efficiency_gain_factor': 0.05, 'production_factory_max_efficiency_factor': 0.04}, ('tools', 'industry')),
    IdeaDef('island_steel', 'Island-Rolled Plate', 'Ship plate and rail rolled at home from main island ore.',
            {'industrial_capacity_factory': 0.04, 'industrial_capacity_dockyard': 0.03}, ('industry', 'economy')),
    IdeaDef('light_metal_shops', 'The Light Metal Shops', 'Island aluminium extruded and sheeted for airframes and ferries.',
            {'production_factory_max_efficiency_factor': 0.04, 'experience_gain_air_factor': 0.03}, ('air', 'industry')),
    IdeaDef('three_shift_rota', 'The Three-Shift Rota', 'The plant towns work three shifts, seven days a week.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'assembly')),
    IdeaDef('estate_rubber', 'Replanted Hill Estates', 'The rubber estates are replanted and paid through the lean years.',
            {'production_factory_efficiency_gain_factor': 0.03}, ('economy', 'civil')),
    # the maritime service
    IdeaDef('service_list', 'Seven Hulls on the List', 'The Maritime Service mustered, sound and stretched thin.',
            {'navy_org_factor': 0.03}, ('navy', 'medal')),
    IdeaDef('lane_escorts', 'Escort Groups on the Lanes', 'Escorts grouped with the merchant hulls on the busiest routes.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.05}, ('navy', 'logistics')),
    IdeaDef('strait_submarines', 'The Strait Flotilla', 'Submarines on patrol stations between the districts.',
            {'naval_coordination': 0.04, 'naval_speed_factor': 0.04}, ('submarine', 'security')),
    IdeaDef('escort_drills', 'Drills with the Masters', 'Escorts and merchant masters exercise together at sea.',
            {'naval_coordination': 0.04, 'navy_org_factor': 0.03}, ('training', 'navy')),
    IdeaDef('naval_reserve', 'The Merchant Naval Reserve', 'Merchant officers hold reserve commissions in the Maritime Service.',
            {'training_time_factor': -0.05, 'navy_org_factor': 0.03}, ('document', 'navy')),
    IdeaDef('harbour_booms', 'The Harbour Boom', 'Nets, a boom and a guard boat at the capital naval harbour.',
            {'navy_org_factor': 0.04, 'army_core_defence_factor': 0.03}, ('security', 'navy')),
    # the air wings
    IdeaDef('two_wings', 'Two Wings, Short Legs', 'Two capable air wings that cannot reach the outer districts.',
            {'experience_gain_air_factor': 0.04}, ('air', 'runway')),
    IdeaDef('capital_interceptors', 'The Home Interceptor Screen', 'Fighters on short alert over the capital, the yards and the plant towns.',
            {'air_superiority_efficiency': 0.07, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('lane_patrol', 'The Lane Patrol Wing', 'Support aircraft and fighters that shadow intruders and sweep the trade lanes.',
            {'air_mission_efficiency': 0.06, 'naval_coordination': 0.04}, ('air', 'navy')),
    IdeaDef('wet_season_flying', 'Wet-Season Flying Rules', 'Instrument approaches and alternate fields for the storm months.',
            {'air_mission_efficiency': 0.04, 'experience_gain_air_factor': 0.05}, ('air', 'training')),
    # the battalions
    IdeaDef('hill_battalions', 'Battalions in Three Towns', 'Six volunteer battalions in pairs at the capital and two logistics centres.',
            {'army_org_factor': 0.03}, ('training', 'security')),
    IdeaDef('jungle_school', 'The District B Jungle School', 'Navigation, river crossing and patrol under the canopy.',
            {'army_org_factor': 0.03, 'experience_gain_army_factor': 0.05}, ('training', 'civil')),
    IdeaDef('district_garrisons', 'District Rifle Companies', 'Rifle companies live in every district, outer islands included.',
            {'army_core_defence_factor': 0.08}, ('security', 'civil')),
    IdeaDef('sailing_reserve', 'The Sailing Reserve', 'Battalions kept together with requisition rights on the ferries.',
            {'army_speed_factor': 0.04, 'planning_speed': 0.08}, ('logistics', 'navy')),
    IdeaDef('embark_drill', 'Night Embarkation Drill', 'A battalion boards the ferries before dawn twice a year.',
            {'planning_speed': 0.05, 'experience_gain_army_factor': 0.05}, ('logistics', 'training')),
    IdeaDef('volunteer_pay', 'Twelve-Year Pay Scales', 'Housing, a trade course and a pension for volunteers who stay.',
            {'training_time_army_factor': -0.08, 'consumer_goods_factor': 0.02}, ('economy', 'training')),
    IdeaDef('depot_spares', 'Ninety-Day Depots', 'Every garrison town holds ninety days of spares, rotated against the humidity.',
            {'repair_speed_factor': 0.06, 'supply_consumption_factor': -0.03}, ('tools', 'logistics')),
    # the falling star
    IdeaDef('star_bulletins', 'The Asteroid Bulletin Bureau', 'Every foreign bulletin translated, checked and published.',
            {'stability_factor': 0.02, 'air_detection': 0.02}, ('telescope', 'document')),
    IdeaDef('mountain_observatory', 'The Summit Observatory', 'Island astronomers confirm foreign reports from the capital mountain.',
            {'research_speed_factor': 0.03, 'air_detection': 0.03}, ('telescope', 'science')),
    IdeaDef('hill_shelters', 'Shelters in the Capital Hills', 'Deep shelters behind the capital, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('island_stores', 'Stores in Eight Districts', 'Grain, fuel, medicine and water kept in every district.',
            {'stability_factor': 0.05, 'supply_consumption_factor': -0.02}, ('refugees', 'shelter')),
    IdeaDef('shelter_galleries', 'Linked Shelter Galleries', 'Galleries join the capital shelter halls through the hills.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.02}, ('shelter', 'tools')),
    IdeaDef('store_ships', 'The Anchored Reserve Hulls', 'Old hulls stocked with grain and water in the outer bays.',
            {'stability_factor': 0.03, 'naval_coordination': 0.02}, ('navy', 'refugees')),
    IdeaDef('tide_gauges', 'The Tide Gauge Line', 'Gauges in every district harbour wired to the capital.',
            {'stability_factor': 0.02, 'naval_coordination': 0.02}, ('fishing', 'communications')),
    IdeaDef('emergency_board', 'The Standing Emergency Board', 'Wardens, radio nets, shelters and stores under one statute.',
            {'stability_factor': 0.04, 'political_power_factor': 0.03}, ('document', 'medical')),
    IdeaDef('bells_rehearsed', 'Shelter Bells Rehearsed', 'Every district has just rung its bells and filled its shelters.',
            {'stability_factor': 0.02, 'static_anti_air_damage_factor': 0.05}, ('civil', 'shelter')),
    # wars beyond the horizon
    IdeaDef('war_premiums', 'Northern War Clauses', 'Underwriters add war clauses to any voyage near northern waters.',
            {'consumer_goods_factor': 0.03, 'industrial_capacity_dockyard': 0.03}, ('communications', 'missile')),
    IdeaDef('clean_cargo', 'The Clean Cargo Rule', 'No island hull carries cargo for an army at war.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('peace', 'navy')),
    IdeaDef('any_buyer', 'Charters for Any Buyer', 'Open charters for any client, taxed at the quay, with war zones excluded.',
            {'industrial_capacity_dockyard': 0.06, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('belkan_victor_terms', 'Ordinary Cargo for Belka', 'Commercial terms with the victorious Belkan ports, no endorsement.',
            {'consumer_goods_factor': -0.02, 'industrial_capacity_dockyard': 0.03}, ('diplomacy', 'scales')),
    IdeaDef('clause_lifted', 'The War Clause Struck', 'Northern premiums fall back toward peacetime rates.',
            {'industrial_capacity_dockyard': 0.04, 'consumer_goods_factor': -0.02}, ('scales', 'navy')),
    IdeaDef('southern_watch', 'Plotting the Southern Lanes', 'Every hull on the lanes to the Usean coast is plotted.',
            {'naval_coordination': 0.04, 'war_support_factor': 0.02}, ('security', 'navy')),
    IdeaDef('evacuee_berths', 'Passage for Usean Families', 'Berths at cost on scheduled sailings and a reception hall on the quay.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('refugees', 'medical')),
    IdeaDef('coup_premiums', 'Coup-Season Charter Rates', 'Disrupted Usean ports pay any price for a hull.',
            {'industrial_capacity_dockyard': 0.05, 'stability_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('railgun_study', 'The Railgun Range Tables', 'The air staff plots every published figure on the railgun battery.',
            {'air_detection': 0.05, 'research_speed_factor': 0.02}, ('missile', 'radar')),
    # the continental war
    IdeaDef('crisis_desk', 'The Usean Crisis Desk', 'Analysts read the Usean wires day and night.',
            {'war_support_factor': 0.03, 'air_detection': 0.03}, ('communications', 'missile')),
    IdeaDef('usean_war_rates', 'Usean War Cover', 'Insurers quote Usean cover by the week and fuel prices jump.',
            {'industrial_capacity_dockyard': 0.04, 'consumer_goods_factor': 0.03}, ('missile', 'economy')),
    IdeaDef('neutral_lanes', 'Lights Burning on the Lanes', 'Published routes and lit hulls carry no cargo for either side.',
            {'stability_factor': 0.04, 'naval_coordination': 0.03}, ('peace', 'navy')),
    IdeaDef('allied_fuel', 'Tanker Contracts with the Allies', 'Refined fuel sold on commercial terms to the allied supply ports.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'diplomacy')),
    IdeaDef('relief_voyages', 'Island Relief Sailings', 'Food, medicine and water carried to cut-off Usean ports.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('medical', 'peace')),
    IdeaDef('north_point_run', 'The North Point Tanker Run', 'Island tankers sail darkened in groups on the long run.',
            {'industrial_capacity_dockyard': 0.05, 'war_support_factor': 0.02}, ('navy', 'industry')),
    IdeaDef('quiet_lanes', 'Lanes Without a War', 'The crisis ends without war and Usean calls resume.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.03}, ('peace', 'scales')),
    IdeaDef('reopened_ports', 'Rebuilding Charters in Usea', 'Island hulls and cranes chartered for the damaged Usean harbours.',
            {'industrial_capacity_dockyard': 0.05, 'production_speed_buildings_factor': 0.05}, ('rebuild', 'economy')),
    IdeaDef('erusean_terms', 'Berthing Rights from Erusea', 'Tariffs and berths for ordinary trade, without recognition.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': -0.05}, ('diplomacy', 'scales')),
    IdeaDef('island_programme', 'The Bound Volume of Accounts', 'Every district has written down what changed since 1991.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('document', 'assembly')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('crown_cabinet', 'Crown Cabinet of the Island Chamber',
           'A cabinet formed from the majority of an elected island chamber, governing collectively in the name of the throne, '
           'which signs on ministerial advice. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('harbour_directory', 'Directory of the Shipping Houses',
           'A directory of shipowners, refinery directors and harbour board chairs, governing collectively under a charter '
           'signed by the throne while elections stay suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('movement_committee', 'Standing Committee of the National Movement',
           'The standing committee of the national movement, holding the seals of government and ruling collectively by '
           'decree with other parties suspended. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('throne_question', 'Questions from the Throne Hall', (
        "The crown office publishes its inquiry on the first working morning of the year, and by noon every newspaper in the "
        "capital has printed the questions in full. They are short: who should hold the ministries, who should choose them, "
        "and what the throne should keep for itself. They are also the first questions the court has put to the country in "
        "living memory. Nihon has a throne, eight districts and a large merchant fleet, but the party that once spoke for the "
        "crown has no following left to count.",
        "The answers are already known in outline. The national movement claims half the country and holds the squares of "
        "the two plant towns. The shipping houses, refinery companies and harbour boards hold most of the rest, together with "
        "the district commissioners and the clerks who keep the islands running. A handful of democratic and socialist "
        "circles meet in rented rooms and ask for a vote that nobody expects to be granted.",
        "The court must now decide how the inquiry will be heard. An open session lets every camp speak in the throne hall "
        "with the press watching, and risks turning the hall into a stage. Keeping the inquiry inside the court protects the "
        "throne's dignity and its freedom to choose. Sending the questions out to the districts first would slow everything "
        "down, yet it would show that the outer islands count.",
    ), (
        Option('Hear every camp in open session.', (Stability(0.02), PP(-15), Event('square_answer', 14))),
        Option('Keep the inquiry behind the court doors.', (PP(35), Stability(-0.02))),
        Option('Send the questions to the districts first.', (PP(15), Stability(0.01))),
    ), citation='history/countries/NIH - Nihon.txt set_politics and set_popularities; every response is gameplay',
        picture=2),
    EventDef('square_answer', 'The Movement Answers in the Squares', (
        "Two weeks after the open session begins, the national movement gives its answer outside the throne hall instead of "
        "inside it. Columns march from the works gates of District E and District H to their logistics centres, carrying "
        "banners that ask for the ministries in the throne's name. The marches are disciplined and loud, and they disperse at "
        "dusk without a single broken window, which worries the commissioners more than a riot would have.",
        "The shipping houses reply with a statement printed in every capital newspaper and signed by owners, refinery "
        "directors and harbour board chairs, warning that disorder on the quays will drive charterers to foreign flags. The "
        "democratic circles hold a meeting in a rented hall that the police count at four hundred people. Every camp claims "
        "that the marches prove its own point, and the throne hall fills with petitions by the end of the week.",
        "The court must respond before the next sitting. It can invite the movement's speakers to address the throne hall "
        "directly and so bring the argument indoors. It can ask the commissioners to license marches and keep them away from "
        "the quays, which the movement will call censorship. Or it can say nothing, let the session continue as planned and "
        "hope the squares tire before the hall does.",
    ), (
        Option('Invite the movement into the hall.', (WarSupport(0.02), PP(-10))),
        Option('License the marches away from the quays.', (Stability(0.02), WarSupport(-0.01))),
        Option('Let the session run its course.', (PP(20), Stability(-0.01))),
    ), citation='follow-up to the throne inquiry; every response is gameplay', picture=0),
    EventDef('island_returns', 'What the Survey Ship Found', (
        "The survey ship returns to the capital after a season among the outer districts, its hold full of soil samples, "
        "harbour soundings and petitions. The engineers' report is blunt. The main island has two rail lines, three logistics "
        "centres and every plant in the country. The outer districts have anchorages and very little else, and District B, "
        "which shares the main island with the capital, has no road at all.",
        "District D turns out to be ten separate islets, each with its own landing, its own well and its own quarrel with the "
        "next. District A has a single anchorage that silts up every wet season. District G is two plain provinces that trade "
        "more with the Sotoan coast than with the capital, and Sotoa still maintains its claim to them. The northern outlier "
        "sees a ship from the capital so rarely that its commissioner keeps the sailing dates from memory.",
        "The report ends with a choice of emphasis. The engineers would begin with roads and jetties where people already "
        "live. The commissioners would begin with a regular ferry, arguing that a road nobody can reach is worth nothing. The "
        "treasury would begin with whatever is cheapest, and asks that the report stay unpublished until the money is found.",
    ), (
        Option('Publish the report in every district.', (Stability(0.02), PP(-10))),
        Option('Give it to the engineers and the treasury.', (PP(20), Research('construction_tech', 0.5, 1))),
    ), citation='state histories 84, 130, 239, 431 and 524; the Sotoan claim is add_claim_by = SOA in 524; no border effect',
        picture=1),
    EventDef('hull_count', 'Hulls Nobody Had Counted', (
        "The harbour boards deliver the merchant register after five months, bound in three volumes. Two hundred and "
        "forty-eight hulls fly the island flag. Some are modern tankers on long charters abroad; many are coasters that have "
        "carried the same cargoes between the same districts for thirty years. A few exist only on paper, kept on the "
        "register for the subsidies their owners still collect every quarter.",
        "The register shows how completely the islands depend on their fleet. Every barrel of crude exported, every sack of "
        "grain sent to the outer districts and every crate of parts shipped to the plant towns travels on one of these hulls. "
        "If the fleet stopped for a month the country would stop with it. The Maritime Service, with five escorts and two "
        "submarines, could protect only a handful of them at any one time.",
        "The shipowners want the register kept confidential, since it shows who has been collecting subsidies for hulls that "
        "no longer sail. The Maritime Service wants a copy for its war plans. The treasury wants every paper hull struck off at "
        "once and the money recovered. The ministry must decide what the register is for before deciding who may read it.",
    ), (
        Option('Strike off the paper hulls and recover the money.', (PP(25), Stability(-0.02))),
        Option('Give the Maritime Service a private copy.', (XP('navy', 15), PP(5))),
        Option('Publish the register in full.', (Stability(0.02), PP(-10))),
    ), citation='world-start calibration of 248 convoys and the NIH Maritime Service; every response is gameplay', picture=0),
    EventDef('plant_towns', 'Two Valleys on One Map', (
        "The industrial survey arrives as a single large map, and the map tells the story at a glance. Every well, mill and "
        "plant in Nihon stands in three districts of the main island. The Capital District holds the largest share beside "
        "its yards and fuel silo, while District E and District H each hold three civilian works and two arms works in narrow "
        "valleys served by one rail line apiece.",
        "The plant towns have no ground left to build on. Their valleys are packed with works, housing and spoil heaps, and "
        "every expansion means demolishing something else. District B, next door on the same island, is empty jungle and hill "
        "without a road. The outer districts have room but no power, no rail and no workforce. Meanwhile the country's oil, "
        "steel and light metal leave as raw cargo because the works that could process them have nowhere to stand.",
        "Ministers divide along familiar lines. The shipping houses would rather new works stayed near the ports they serve. "
        "The national movement wants new works wherever new workers can be organised. The engineers want the existing plants "
        "modernised before anything new is built. They agree only that the map should not be shown to foreign buyers.",
    ), (
        Option('Pin the map on the cabinet room wall.', (PP(20), Research('industry', 0.5, 1))),
        Option('Show the map to the plant town councils.', (Stability(0.02), PP(-5))),
    ), citation='state histories 165, 251 and 582 (buildings and resources); every response is gameplay', picture=1),
    EventDef('service_muster', 'Seven Ships and Eight Districts', (
        "The Maritime Service parades every hull it owns in the capital's naval harbour on a clear morning: five coastal "
        "escorts and two coastal submarines, painted, crewed and dressed overall. The crowd on the quay is large and proud. "
        "The officers on the reviewing stand are quieter, because they know that seven ships must cover the coasts of eight "
        "districts and a merchant fleet of nearly two hundred and fifty hulls.",
        "After the parade the service chiefs hand the government a paper. The escorts are sound but old, and their crews are "
        "kept at strength only by cancelled leave. The submarines are newer and their officers want more of them. The "
        "capital's four slipways are shared with the ferry builders and the shipping houses, so a warship refit waits in the "
        "same queue as a coaster with a cracked shaft.",
        "The paper asks a single question: is the service meant to guard the merchant lanes, or to make the island straits "
        "impassable to an intruder? It cannot do both with seven hulls. Until the government answers, the chiefs write, every "
        "refit and every recruit is an expense without a purpose, and the best young officers will keep leaving for the "
        "merchant bridges that pay twice as much.",
    ), (
        Option('Promise an answer within the year.', (XP('navy', 10), PP(-10))),
        Option('Order a refit schedule first.', (Research('naval_equipment', 0.5, 1), PP(10))),
    ), citation='mod/2985041246/history/units/NIH_ws_navy.txt; every response is gameplay', picture=2),
    EventDef('falling_star', 'A Name in the Wire Copy', (
        "The wire copy arrives in the capital on an ordinary evening and is nearly filed with the shipping notices. The "
        "International Astronomical Union announces that an asteroid named Ulysses will pass close to the Earth in the "
        "coming years, with a chance of impact and great devastation. The night editor of the largest capital newspaper "
        "reads it twice, telephones a teacher of astronomy and decides to run it on the front page.",
        "By morning the story is everywhere. In the plant towns workers ask whether their families should move into the "
        "hills. In the outer districts fishermen ask whether the sea will rise. The national movement accuses the government "
        "of hiding the truth, while the shipping houses ask whether the insurers already know more. The ministries have no "
        "astronomer of their own and no plan for any kind of danger from the sky.",
        "The government must decide how to speak about something it does not yet understand. It can publish every foreign "
        "bulletin in a plain translation and let people judge. It can wait for island experts and say nothing until they "
        "report. Or it can announce a commission at once, which reassures many people and promises answers it cannot yet give.",
    ), (
        Option('Publish every bulletin in plain words.', (Stability(0.02), PP(-10))),
        Option('Wait for island experts.', (PP(20), Stability(-0.02))),
        Option('Announce a commission today.', (Stability(0.03), PP(-20))),
    ), citation='date anchor only, ACES Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; the Nihonian response is '
                'gameplay', picture=0),
    EventDef('impact_word', 'The Impact Will Come', (
        "The FCU announces to the world that Ulysses will strike the Earth and that it has plans to counter the impact. The "
        "statement is calm and technical, and in Nihon it lands like a storm warning without a forecast. Nobody in the "
        "capital can say where the fragments will fall, how many there will be, or whether the islands will see anything "
        "at all.",
        "Within days, prices for tinned food, bottled water and fuel cans double in the capital markets. The commissioners of "
        "the outer districts send telegrams asking whether ferries will be held in reserve for them. The plant town councils "
        "ask whether the works should stop. The shipping houses report that foreign charterers are already suspending long "
        "contracts until the danger has passed.",
        "The government cannot prevent the impact, only decide how the country will prepare for it. Ministers can dig into the "
        "hills behind the capital and bring people to shelter, or spread stores and small shelters across every district and "
        "accept weaker protection everywhere. Either plan will take years and most of the money the islands can spare. The "
        "first decision is how to stop the panic buying in the markets.",
    ), (
        Option('Ration staples until the markets calm.', (Stability(0.02), PP(-10))),
        Option('Let prices find their own level.', (PP(15), Stability(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 1996 / 04.20 in tools/lore/chronicle.json; where fragments fall is never '
                'stated', picture=2),
    EventDef('roche_night', 'A Night Without Sleep', (
        "Ulysses passes through the Roche limit of the Earth and begins to break apart. Over the main island the night is "
        "clear, and over the outer districts it is cloudy. Radio stations broadcast foreign reports every quarter hour. "
        "Shelter wardens stand at every entrance, store ship crews raise steam in their anchorages, and tide gauge keepers "
        "sit beside their instruments with a lamp and a telephone.",
        "The capital's telephone exchange has never carried so many calls. Families ring relatives in the outer districts, "
        "commissioners ring the ministries and the ministries ring the observatory, which can only repeat what the foreign "
        "wires say. By dawn the wires carry long lists of places abroad that will need help, and nobody in the capital can "
        "yet say what the coming days will bring to the islands themselves.",
        "The morning brings a choice about what the shelters and stores are for now. Some ministers want them kept full for "
        "months in case more fragments arrive. Others want part of the reserve loaded onto hulls for countries that were "
        "struck. The commissioners want their wardens thanked by name of district before anything else is decided.",
    ), (
        Option('Keep the reserve full at home.', (Stability(0.03),)),
        Option('Load relief hulls for stricken ports.', (PP(15), XP('navy', 10))),
        Option('Thank the wardens in every district.', (Stability(0.02), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no damage in Nihon is claimed',
        picture=0),
    EventDef('belkan_news', 'Premiums from the North', (
        "The Belkan War breaks out on the far side of the ocean, and Nihon learns of it first from its insurers. Within a "
        "week every underwriter that covers island hulls sends a letter adding a war clause to any voyage touching northern "
        "waters. Tanker owners on long charters to the north ask whether to turn back. Fuel prices in the capital markets rise "
        "before the first newspaper map of the fighting is printed.",
        "No Nihonian interest is at stake in the war itself. The country has no forces abroad, no alliance with either side "
        "and no claim on anything being fought over. But a fleet that earns its living carrying other people's cargo cannot "
        "stay out of a war's economy, only choose how to take part in it. Charterers are already offering rates that would "
        "have been unthinkable a month ago.",
        "The ministry must set rules before the owners set their own. It could forbid any cargo for armies at war and accept "
        "the loss of the richest charters. It could permit any charter outside declared war zones and tax the profits. Until "
        "it decides, the masters at sea are signalling their owners for instructions every night, and the owners are "
        "telephoning the ministry every morning.",
    ), (
        Option('Hold every hull in port for a week.', (Stability(0.02), PP(-10))),
        Option('Let the owners decide for now.', (PP(20), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; Nihon takes no part',
        picture=1),
    EventDef('usean_coup', 'Usean Harbours Go Silent', (
        "A coup breaks out across Usea, and for several days the shore radio watch in the capital hears nothing from a string "
        "of Usean harbours that normally report every hour. Island hulls in those ports signal that the quays are closed, "
        "crews are confined aboard and the local officials have vanished from their offices. Unified Command defeats the "
        "rebels in the end, but the islands learn that only from foreign broadcasts.",
        "At home, the families of crews queue outside the shipping offices of the capital and District E. The shipping houses "
        "ask the government to send the Maritime Service to bring their hulls out; the service replies that its escorts "
        "would need weeks to arrive and could not enter a harbour without permission from someone in charge. The national "
        "movement demands action and does not say what kind.",
        "The government can do little in Usea itself. It can pay the crews' wages to their families until the hulls return and "
        "make the shipowners repay the treasury later. It can send a single escort to wait outside the Usean lanes as a signal "
        "of concern. Or it can tell the families the truth: that the crews are safest staying aboard, and that patience is all "
        "the islands can offer.",
    ), (
        Option('Pay the crews from the treasury.', (Stability(0.03), PP(-20))),
        Option('Send one escort toward the Usean lanes.', (XP('navy', 15), WarSupport(0.02))),
        Option('Tell the families to wait.', (PP(15), Stability(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 1997 / 05.30 in tools/lore/chronicle.json; no Nihonian role is claimed',
        picture=2),
    EventDef('usean_crisis', 'The Railgun Quarrel', (
        "By the summer of 2003 the quarrel over Stonehenge, the railgun complex in neutral San Salvacion, dominates every "
        "foreign broadcast heard in the capital. The crisis desk reads the wires day and night. Shipping agents report that "
        "Usean ports are filling with soldiers and emptying of charterers, and that insurers have begun to quote Usean cover "
        "by the week instead of by the year.",
        "Nihon has no stake in the railguns and no forces anywhere near Usea. It does have a fleet that carries fuel, grain and "
        "parts to Usean ports, a refinery that sells to Usean buyers and an air staff that has studied the battery's reach "
        "since it was built. If the quarrel becomes a war, all three will be drawn into it whatever the government wishes.",
        "Before anything is decided in Usea, the government can prepare its own people. It can recall the island hulls from "
        "Usean waters now, at the cost of their charters. It can warn the owners and leave the decision to them. Or it can "
        "quietly fill the fuel silo and the shelters, which costs money and says nothing to anyone abroad or at home.",
    ), (
        Option('Recall the hulls from Usean waters.', (Stability(0.02), PP(-15))),
        Option('Warn the owners and leave it to them.', (PP(20),)),
        Option('Fill the silo and say nothing.', (WarSupport(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER in tools/lore/chronicle.json; whether war follows is read '
                'from the mod flags', picture=0),
)

# --- branches ------------------------------------------------------------------------------------
THRONE = Branch('throne', 'A Throne Without a Party', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('th_inquiry', 'The Throne Asks Who Governs',
          "Nihon is ruled from a throne whose own party has no following at all. Half the country marches with the national "
          "movement and almost all the rest trusts the shipping houses, harbour boards and refinery companies that run the "
          "islands day to day. The crown office opens a formal inquiry into who should govern, knowing that every answer will "
          "cost it some of its standing.",
          ('command', 'document'), reward=(Idea('throne_inquiry'), Event('throne_question'))),
    Focus('th_commissioners', 'Hear the District Commissioners',
          "Eight district commissioners hold the islands together, from the Capital District to the plains of District G and "
          "the northern outlier. Each is called to the throne hall to say what their district would accept. The hearings take "
          "most of a season and expose how differently the main island and the outer districts see the crown, but no "
          "settlement can stand without them.",
          ('assembly', 'civil'), after=('th_inquiry',),
          reward=(PP(30), Tooltip('Opens the three answers to the inquiry; only one can be taken.'))),
    Focus('th_charter', 'Promise an Elected Chamber',
          "The smallest camp in Nihon proposes the largest change: a written charter under which the throne reigns and "
          "ministers answer to an elected island chamber. Its democratic sponsors barely register in any count, yet many "
          "officials quietly prefer a lawful vote to an angry square. Promising the chamber weakens the court at once and "
          "hands the national movement a campaign it could well win.",
          ('ballot', 'document'), after=('th_commissioners',), exclusive=('th_houses', 'th_movement'),
          reward=(SwapIdea('throne_inquiry', 'chamber_promise'),)),
    Focus('th_houses', 'Seat the Shipping Houses',
          "The non-aligned establishment already runs the hulls, the harbours, the wells and the refineries, and it asks to "
          "run the ministries openly. Shipowners, refinery directors and harbour boards would govern as a directory in the "
          "throne's name, with no ballot and with published accounts. They are competent and cautious, and they would govern "
          "an island economy as a balance sheet.",
          ('economy', 'command'), after=('th_commissioners',), exclusive=('th_charter', 'th_movement'),
          reward=(SwapIdea('throne_inquiry', 'houses_at_court'),)),
    Focus('th_movement', 'Open the Ministries to the Movement',
          "The national movement fills the squares of the plant towns and claims half of every opinion count. Its leaders "
          "offer the throne loyalty in exchange for the ministries, the police and the radio. Accepting would quiet the streets "
          "of District E and District H within weeks, but the shipping houses, the editors and the small democratic circles "
          "would all be watched from then on.",
          ('security', 'assembly'), after=('th_commissioners',), exclusive=('th_charter', 'th_houses'),
          reward=(SwapIdea('throne_inquiry', 'movement_ministries'),)),
    Focus('th_chamber', 'Convene the Island Chamber',
          "Elections are held under the new charter and a cabinet forms from the chamber majority, governing collectively in "
          "the name of the throne. The change runs through an office rather than a person, and the cabinet can be voted out "
          "at the next count. The national movement wins many seats and contests every bill, so the first cabinet governs as "
          "a nervous coalition.",
          ('assembly', 'ballot'), after=('th_charter',), cost=10, exclusive=('th_directory', 'th_committee'),
          reward=(Regime('crown_cabinet'), Flag('path_chamber'))),
    Focus('th_directory', 'Charter the Shipping Directory',
          "A charter signed by the throne places the executive in a directory of shipowners, refinery directors and harbour "
          "board chairs. The directory governs collectively, keeps elections suspended and promises quarterly accounts in the "
          "capital press. The national movement calls it government by invoice, and the directory must prove with freight "
          "figures and fuel prices that it deserves to stay.",
          ('command', 'economy'), after=('th_houses',), cost=10, exclusive=('th_chamber', 'th_committee'),
          reward=(Regime('harbour_directory'), Flag('path_directory'))),
    Focus('th_committee', 'The Movement Takes the Seals',
          "The standing committee of the national movement receives the seals of government and proclaims the Empire of Nihon "
          "a state of discipline. Other parties are suspended, the commissioners answer to movement inspectors and the press "
          "reports to a bureau. The plant towns cheer, the outer islands go quiet, and foreign shipping agents begin pricing a "
          "new kind of risk into every charter.",
          ('security', 'command'), after=('th_movement',), cost=10, exclusive=('th_chamber', 'th_directory'),
          reward=(Regime('movement_committee'), Flag('path_movement'))),
    Focus('th_island_seats', 'Seats for the Outer Islands',
          "The first chamber was elected almost entirely on the main island, because the polling stations of District A, "
          "District D and District G opened late or not at all. A reserved bench for the outer districts, with ballots carried "
          "by ferry, gives the small islands a voice in the capital. The bench costs the cabinet its slim majority on every "
          "close vote.",
          ('ballot', 'navy'), after=('th_chamber',), requires=(HasFlag('path_chamber'),), reward=(Idea('island_seats'),)),
    Focus('th_accounts', 'Freight Figures on the Front Page',
          "The directory keeps its promise and prints its accounts every quarter: freight carried, fuel refined, wages paid and "
          "contracts awarded, house by house. The figures are dull and they are true, which is new. Readers in the plant towns "
          "learn exactly which shipowner won which contract, and the directory learns how much candour costs when a quarter "
          "goes badly.",
          ('document', 'economy'), after=('th_directory',), requires=(HasFlag('path_directory'),),
          reward=(Idea('directory_accounts'),)),
    Focus('th_wardens', 'Wardens on Every Quay',
          "Movement wardens take posts on every quay and ferry landing, checking papers, cargo manifests and the politics of "
          "crews. Smuggling falls, and so does the gossip that used to cross the islands faster than the mail. The harbours run "
          "to time under the wardens, while foreign masters complain of searches, delays and fees that appear on no published "
          "schedule.",
          ('security', 'civil'), after=('th_committee',), requires=(HasFlag('path_movement'),), reward=(Idea('harbour_wardens'),)),
    Focus('th_household', 'Trim the Court Household',
          "The court keeps residences, a garage of state cars, a ceremonial guard and a household staff sized for a richer "
          "century, all paid from the island treasury. Cutting the household to a working office saves money every year and "
          "shows every camp that the throne will share the cost of whatever comes next. Several older courtiers resign rather "
          "than serve in a smaller hall.",
          ('scales', 'command'), after=('th_commissioners',), reward=(Idea('court_household'),)),
    Focus('th_statute', 'The Throne Within the Law',
          "Whatever government now holds the seals, the throne's own position needs one written statute: what the crown may "
          "sign, refuse and delay, and what it may never do. Drafting it takes a full session and forces the government of the "
          "day to define its own limits too. The finished law disappoints every faction a little and is likely to outlast each "
          "of them.",
          ('scales', 'document'), after_any=('th_island_seats', 'th_accounts', 'th_wardens'), requires=(After('1996.1.1'),),
          reward=(Idea('settled_throne'),)),
))

ISLANDS = Branch('islands', 'Eight Districts at Sea', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('isl_circuit', 'Sail the Commissioners Circuit',
          "Nihon is one main island of four districts and four outer districts scattered across open water, one of them so far "
          "north that it lies nearer Malynea and Monstrua than the capital. A survey ship carrying engineers, clerks and a "
          "doctor visits every landing in turn. The voyage ties up the only spare hull in the capital yards for a full season.",
          ('navy', 'document'), reward=(Idea('circuit_reports'), Event('island_returns'))),
    Focus('isl_b_track', 'A Hill Road into District B',
          "District B shares the main island with the capital and District H, yet it has no road, no rail, no plant and no "
          "harbour works of any kind. Its jungle valleys and two hill ridges have kept it a district of footpaths and river "
          "boats. A graded road from the capital through the hills is the first public work the district has ever been given.",
          ('logistics', 'tools'), after=('isl_circuit',), reward=(Build('infrastructure', 1, 130),)),
    Focus('isl_d_jetties', 'Jetties Along the D Chain',
          "District D is ten jungle islets, every one with a shoreline and none with a road worth the name. Five of them already "
          "hold small naval anchorages, yet goods still come ashore by rowing boat. Concrete jetties and a short coastal track "
          "on each islet let ferries unload in an hour instead of a day, at a cost the treasury will feel for years.",
          ('bridge', 'navy'), after=('isl_circuit',), reward=(Build('infrastructure', 1, 239),)),
    Focus('isl_a_berth', 'A Deep Berth in District A',
          "District A is two jungle provinces on the southwestern fringe of the country, served by one anchorage that cannot "
          "take anything larger than a coaster. Dredging a deep berth and grading the road behind it brings the district "
          "within reach of a regular ferry. The engineers warn that the silt comes back every wet season and the dredger will "
          "have to return.",
          ('navy', 'tools'), after=('isl_circuit',), reward=(Build('infrastructure', 1, 84),)),
    Focus('isl_outlier', 'Water and Wireless for the North',
          "The northern outlier is nine plain and hill provinces with a single anchorage and towns that live on rainwater "
          "tanks and a radio set that works when the weather allows. Cisterns, a graded road between the harbour and the hill "
          "farms and a proper wireless station tie it back to the rest of the country. Every bag of cement for the work must "
          "travel days by sea.",
          ('communications', 'civil'), after=('isl_circuit',), reward=(Build('infrastructure', 1, 431),)),
    Focus('isl_g_claim', 'Answer the Sotoan Claim on Paper',
          "Sotoa maintains a claim on District G, two plain provinces with two anchorages that lie far closer to the Sotoan "
          "coast than to the Capital District. The ministry answers with documents rather than guns: land registers, tax rolls, "
          "school records and harbour logs proving continuous civil administration. The answer changes no claim and moves no "
          "troops, and Sotoa is free to ignore it.",
          ('diplomacy', 'document'), after=('isl_circuit',),
          reward=(Flag('g_answered'), Stability(0.01), Tooltip('Changes no claim, core or border.'))),
    Focus('isl_g_office', 'A Civil Office in District G',
          "A district office with a clerk, a postmaster, a nurse and a magistrate gives the residents of District G something "
          "the claim papers cannot: daily proof that the capital remembers them. The office pays pensions, registers boats and "
          "hears small disputes over moorings and fishing grounds. It costs little, and it is watched closely from across the "
          "strait.",
          ('civil', 'scales'), after=('isl_g_claim',), requires=(HasFlag('g_answered'),),
          reward=(Idea('g_district_office'), Build('infrastructure', 1, 524))),
    Focus('isl_crown_ferries', 'A Crown Ferry Service',
          "The first answer to the island question is a state ferry service with fixed fares, fixed calls and a guaranteed "
          "sailing to every district each week, profitable or not. The outer islands cheer and the treasury pays for every "
          "empty cabin. The shipping houses, which carried island passengers at whatever price the season allowed, lose a trade "
          "they had always considered their own.",
          ('navy', 'command'), after_any=('isl_d_jetties', 'isl_a_berth'), cost=10, exclusive=('isl_carriers',),
          reward=(SwapIdea('circuit_reports', 'crown_ferries'), Flag('ferry_crown'))),
    Focus('isl_carriers', 'License the Island Carriers',
          "The second answer leaves the ferries with the private carriers but ties their licences to obligations: a minimum "
          "number of calls at District A, District D, District G and the northern outlier, and capped fares on the poorest "
          "routes. It costs the treasury almost nothing. It depends instead on inspectors who will be offered money by every "
          "carrier they inspect.",
          ('economy', 'navy'), after_any=('isl_d_jetties', 'isl_a_berth'), cost=10, exclusive=('isl_crown_ferries',),
          reward=(SwapIdea('circuit_reports', 'island_carriers'), Flag('ferry_licensed'))),
    Focus('isl_ferry_halls', 'Ferry Pensions and Crew Halls',
          "A state service needs state crews, so the ferry board recruits deckhands and engineers on fixed salaries with "
          "pensions and a hall in every home port. Turnover falls and the boats sail on time. The shipping houses complain that "
          "the board poaches their best men, and the wage bill becomes the largest single line in the ferry budget.",
          ('civil', 'navy'), after=('isl_crown_ferries',), requires=(HasFlag('ferry_crown'),), reward=(Idea('ferry_crews'),)),
    Focus('isl_inspectors', 'Inspectors on the Ferry Quays',
          "Licences mean nothing unless someone checks them, so a small inspectorate rides the ferries unannounced and counts "
          "calls, fares and lifejackets. Carriers who skip their outer-island calls lose routes to rivals at the next tender. "
          "The inspectors are paid well enough to refuse most bribes, which makes them expensive, unpopular with the carriers "
          "and essential to the whole arrangement.",
          ('scales', 'security'), after=('isl_carriers',), requires=(HasFlag('ferry_licensed'),),
          reward=(Idea('ferry_inspectors'),)),
    Focus('isl_timetable', 'One Timetable for Eight Districts',
          "Whoever runs the boats, the islands need one published timetable that connects the ferries with the two rail lines "
          "out of the capital. A single printed sheet, posted in every post office, lets a farmer in District D plan a trip to "
          "the District E logistics centre. Agreeing that sheet means locking rival operators and railway clerks in one room "
          "until they finish.",
          ('logistics', 'document'), after_any=('isl_ferry_halls', 'isl_inspectors'), reward=(Idea('island_timetable'),)),
))

HULLS = Branch('hulls', 'Two Hundred and Forty-Eight Hulls', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('hl_register', 'Count Every Hull on the Register',
          "For a country with ten civilian plants, Nihon owns a remarkable merchant fleet: two hundred and forty-eight convoy "
          "hulls, from ocean tankers to island coasters. Nobody has counted them properly in years. The harbour boards of the "
          "capital, District E and District H are ordered to produce one register of owner, tonnage, age and crew for every "
          "hull, whatever the shipowners think of it.",
          ('navy', 'document'), reward=(Idea('merchant_register'), Event('hull_count'))),
    Focus('hl_halls', 'Hiring Halls for Seamen',
          "Crews for the island fleet are hired in waterfront bars by agents who take a cut of every wage. Public hiring halls "
          "in the three main ports post every berth, every rate and every complaint against a master. Seamen get fairer "
          "contracts and owners get crews who can be traced, while the agents lose a living and organise against the halls.",
          ('training', 'navy'), after=('hl_register',), reward=(Idea('hiring_halls'),)),
    Focus('hl_home_flag', 'Every Hull Under the Home Flag',
          "One answer keeps the whole fleet registered in Nihon, crewed mostly by island seamen and repaired in island yards, "
          "so that every hull can be called home in an emergency. Owners pay higher wages and higher taxes than a flag of "
          "convenience would charge. In return the state promises them repair work, cargo preference and protection on the "
          "lanes.",
          ('navy', 'command'), after=('hl_register',), cost=10, exclusive=('hl_open_registry',),
          reward=(SwapIdea('merchant_register', 'home_flag_fleet'), Flag('fleet_home'))),
    Focus('hl_open_registry', 'Rent the Flag to Foreign Owners',
          "The other answer opens the island registry to foreign owners who want a neutral flag, low fees and few questions. "
          "Registration money flows into the treasury and the fleet list grows on paper. Many of those hulls will never call at "
          "a Nihonian port, and in a crisis their owners will sail wherever the charter pays best.",
          ('diplomacy', 'economy'), after=('hl_register',), cost=10, exclusive=('hl_home_flag',),
          reward=(SwapIdea('merchant_register', 'open_registry'), Flag('fleet_open'))),
    Focus('hl_mutual', 'A Hull Mutual in the Capital',
          "Most island shipowners insure with foreign underwriters who raise premiums at the first rumour of trouble anywhere on "
          "the ocean. A mutual association in the capital, backed by a treasury guarantee, lets owners insure one another at "
          "cost. It keeps premium money at home, though a single bad storm season could empty the fund in a month.",
          ('scales', 'navy'), after=('hl_register',), reward=(Idea('hull_mutual'),)),
    Focus('hl_lane_radio', 'Radio Watch on the Trade Lanes',
          "Masters on the long lanes report their position by radio once a day, if they remember to. A shore watch in the "
          "Capital District logs every report, plots every hull and raises the alarm when one goes silent. It saves crews in "
          "storms and gives the Maritime Service a picture of the lanes it never had, at the price of a large night staff.",
          ('communications', 'navy'), after=('hl_halls',), reward=(Idea('lane_watch'),)),
    Focus('hl_cadets', 'A Merchant Cadet School',
          "The fleet is old and so are its officers. A cadet school in the capital trains mates, engineers and radio officers "
          "to one standard, with sea time on government hulls. The first classes are small and their fees are covered by a levy "
          "on the shipowners. Within a decade the school will decide who commands most of the hulls that carry the island "
          "trade.",
          ('training', 'document'), after=('hl_halls',), reward=(Idea('cadet_school'), XP('navy', 10))),
    Focus('hl_d_yard', 'Repair Berths in the D Chain',
          "A home-flag fleet needs home repairs, and the capital slipways are already full with the Maritime Service. A repair "
          "yard on the sheltered water inside the District D chain takes coasters and tankers off the waiting list. It brings "
          "skilled work to islets that have never had any, although every plate and rivet the yard uses must arrive by sea.",
          ('tools', 'navy'), after=('hl_home_flag',), requires=(HasFlag('fleet_home'),), reward=(Build('dockyard', 1, 239),)),
    Focus('hl_fees', 'Registry Fees for the Treasury',
          "Foreign owners pay their registration fees in hard currency every year, and the treasury discovers a revenue line "
          "that needs no plant and no crew. The fees fund the hull mutual and the cadet school. Critics point out that the money "
          "rests on a reputation for asking few questions, which a single scandal at sea could destroy overnight.",
          ('economy', 'document'), after=('hl_open_registry',), requires=(HasFlag('fleet_open'),),
          reward=(TimedIdea('registry_fees', 730),)),
    Focus('hl_tankers', 'Tankers for the Refinery Coast',
          "Crude from the wells of the main island leaves by tanker, and most of those tankers are older than their masters. "
          "Designing a standard island tanker, sized for the capital berths and the outer anchorages alike, gives the yards a "
          "long production run. The design office borrows engineers from the Maritime Service, which wants them back before its "
          "own refits begin.",
          ('navy', 'industry'), after_any=('hl_mutual', 'hl_lane_radio'), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 5))),
))

PLANTS = Branch('plants', 'Wells and Plant Towns', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('pl_wells', 'Map the Main Island Wells',
          "All of Nihon's oil, steel, aluminium and rubber comes from three districts of the main island: the Capital District, "
          "District E and District H. Their plants share the same valleys as the wells and the mills, and every building plot "
          "in the two plant towns is already taken. A survey of every well, seam and mill decides where the next decade of "
          "industry can go.",
          ('economy', 'document'), reward=(Idea('well_ledger'), Event('plant_towns'))),
    Focus('pl_refinery', 'A Refinery Below the Capital Hills',
          "Crude from the capital fields is shipped abroad and bought back as fuel, which leaves the single fuel silo half empty "
          "whenever prices jump. Expanding the old topping plant below the capital hills into a real refinery keeps more of the "
          "value at home. It also concentrates the country's fuel in one place that any planner could find on a map.",
          ('industry', 'tools'), after=('pl_wells',), reward=(Idea('hill_refinery'), Research('synth_resources', 0.5, 1))),
    Focus('pl_b_works', 'New Works in District B',
          "The first industrial answer moves new building into District B, the empty district on the main island, where land "
          "is cheap and every plot is free. Two works go up near the new hill road, drawing workers from the crowded plant "
          "towns. The cost is high, the district has no rail, and every part for the works must come in by truck or boat.",
          ('industry', 'civil'), after=('pl_wells',), cost=10, exclusive=('pl_retool',),
          reward=(Build('industrial_complex', 2, 130), Flag('plants_spread'))),
    Focus('pl_retool', 'Retool the Old Plant Towns',
          "The second answer leaves the map alone and makes the existing works in District E and District H run better: new "
          "tools, new lines, new foremen and longer runs. It is cheaper than building and quicker to pay back. It also tightens "
          "the country's dependence on two valleys of the main island and the single rail line that serves each of them.",
          ('tools', 'industry'), after=('pl_wells',), cost=10, exclusive=('pl_b_works',),
          reward=(Idea('retooled_towns'), Flag('plants_deepen'))),
    Focus('pl_b_second', 'A Second Works Town in District B',
          "The first District B works bring a settlement with them: houses, a clinic, a market and a bus to the capital. A "
          "second works town further along the hill road follows, this time partly financed by shipping houses that want an "
          "inland supplier. District B begins to look like part of the main island rather than its forgotten interior.",
          ('civil', 'industry'), after=('pl_b_works',), requires=(HasFlag('plants_spread'),),
          reward=(Build('industrial_complex', 1, 130),)),
    Focus('pl_shifts', 'Three Shifts in the Plant Towns',
          "Retooled lines pay off only if they never stop, so the works of District E and District H move to three shifts, "
          "seven days a week. Output rises sharply. So do accidents, absences and the anger of families who see their workers "
          "only on the station platform at shift change. The national movement and the shipping houses both claim to speak for "
          "those workers.",
          ('industry', 'assembly'), after=('pl_retool',), requires=(HasFlag('plants_deepen'),), reward=(Idea('three_shift_rota'),)),
    Focus('pl_steel', 'Rolling Mills for Island Steel',
          "The main island digs enough steel ore for its own needs and exports most of it raw because the mills are too small "
          "to roll plate. A rolling mill sized for ship plate and rail gives the yards and the railways a domestic supply. The "
          "mill needs power the grid barely has, and the ore exporters lose their best customers to it.",
          ('industry', 'economy'), after_any=('pl_b_second', 'pl_shifts'), reward=(Idea('island_steel'),)),
    Focus('pl_metal', 'Light Metal for the Airframe Shops',
          "Aluminium from the capital and the two plant towns is shipped abroad as ingot. A light-metal shop that extrudes and "
          "sheets it at home supplies the air wings' repair lines and the ferry builders. It is a small industry with a large "
          "electricity bill, and the first works in the country to make parts for anything that flies.",
          ('air', 'industry'), after=('pl_steel',), reward=(Idea('light_metal_shops'),)),
    Focus('pl_capital_plot', 'One Free Plot in the Capital',
          "The Capital District has room for exactly one more large building among its plants, yards and silo, and the "
          "ministries argue over it for a year. Giving it to an arms works means spare parts for six battalions and two air "
          "wings without waiting for foreign shipments. It also means the capital's last free ground goes to guns rather than "
          "goods.",
          ('missile', 'industry'), after=('pl_refinery',), reward=(Build('arms_factory', 1, 0),)),
    Focus('pl_rubber', 'Rubber from the Hill Estates',
          "The country's modest rubber supply comes from hill estates that were planted generations ago and never replanted. "
          "Replanting with new stock and new tapping schedules takes years before a single tree gives latex. The ministry pays "
          "the estates through the lean years in return for a fixed share of the crop, which the truck and tyre makers badly "
          "need.",
          ('economy', 'civil'), after=('pl_wells',), reward=(TimedIdea('estate_rubber', 1095),)),
))

SERVICE = Branch('service', 'The Maritime Service', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('ms_muster', 'Muster the Maritime Service',
          "The Maritime Service is five coastal escorts and two coastal submarines based on the capital's naval harbour, "
          "guarding a merchant fleet of nearly two hundred and fifty hulls and the coasts of eight districts. A full muster "
          "shows ships in good order and crews stretched thin. The service asks the government to decide what such a small "
          "navy is actually for.",
          ('navy', 'medal'), reward=(Idea('service_list'), Event('service_muster'))),
    Focus('ms_slipways', 'Audit the Capital Slipways',
          "The capital's four slipways build for the Maritime Service, the ferry operators and the shipping houses at once, and "
          "nobody has ever ranked their orders. An audit of every keel, crane and delayed contract produces the first honest "
          "yard schedule. The escorts' refits move to the front of the queue, and the merchant owners object loudly.",
          ('tools', 'document'), after=('ms_muster',), reward=(Research('naval_equipment', 0.5, 2),)),
    Focus('ms_escorts', 'Escort Groups for the Lanes',
          "One doctrine treats the Maritime Service as a convoy force: escorts grouped with the merchant hulls on the busiest "
          "lanes and trained to shepherd, screen and rescue. It suits a country whose wealth floats. It also commits nearly "
          "every warship to the long routes and leaves the home straits to patrol boats and the weather.",
          ('navy', 'logistics'), after=('ms_muster',), cost=10, exclusive=('ms_submarines',),
          reward=(SwapIdea('service_list', 'lane_escorts'), Flag('navy_escort'))),
    Focus('ms_submarines', 'Submarines Off Every Strait',
          "The other doctrine leaves the merchant fleet's protection to treaties and insurers and spends instead on submarines "
          "that deny the island straits to any intruder. Two boats become a flotilla on patrol stations between the districts. "
          "It fits the grand doctrine of a fleet in being, and it tells the shipowners plainly that their hulls sail without "
          "escort.",
          ('submarine', 'security'), after=('ms_muster',), cost=10, exclusive=('ms_escorts',),
          reward=(SwapIdea('service_list', 'strait_submarines'), Flag('navy_submarine'))),
    Focus('ms_heights_radar', 'Radar on the Capital Heights',
          "The capital's naval harbour can see only as far as a lookout with binoculars. A radar station on the heights above "
          "the harbour covers the approaches, the anchorage and the air above both. It needs imported parts and foreign-trained "
          "technicians, and the air wings and the Maritime Service immediately argue about who controls the screen.",
          ('radar', 'navy'), after=('ms_slipways',), reward=(Build('radar_station', 1, 0),)),
    Focus('ms_drills', 'Escort Drills with Merchant Masters',
          "Escort groups are only as good as the masters they protect, so the Maritime Service sails exercises with real "
          "merchant hulls: zigzag courses, darkened ships and rescue drills. Shipowners lose a few days of freight for every "
          "exercise. In return their crews learn what to do when a warship signals, and the escorts learn how slowly a laden "
          "tanker turns.",
          ('training', 'navy'), after=('ms_escorts',), requires=(HasFlag('navy_escort'),),
          reward=(Idea('escort_drills'), XP('navy', 15))),
    Focus('ms_a_pens', 'Submarine Berths in District A',
          "District A sits on the southwestern edge of the country, beside deep water and far from the capital's crowded "
          "harbour. A small submarine berth and repair shop there shortens every patrol and keeps the flotilla where it is "
          "hardest to watch. The district gains wages, and a restricted zone on a shore it used to fish from freely.",
          ('submarine', 'tools'), after=('ms_submarines',), requires=(HasFlag('navy_submarine'),),
          reward=(Build('dockyard', 1, 84),)),
    Focus('ms_reserve', 'A Merchant Naval Reserve',
          "Cadet-school officers and seamen from the hiring halls are offered a reserve commission: a few weeks a year aboard "
          "the Maritime Service in return for a retainer. In a crisis the service could triple its trained crews overnight. "
          "The shipowners worry that their best officers will spend every crisis on warships instead of on their own bridges.",
          ('document', 'navy'), after=('ms_slipways',), requires=(Completed('hl_cadets'),), reward=(Idea('naval_reserve'),)),
    Focus('ms_boom', 'A Boom Across the Naval Harbour',
          "Whatever doctrine the service follows, the capital's naval harbour holds all its ships for most of the year and has "
          "no defence against a small boat or a midget submarine. Anti-submarine nets, a boom across the entrance and a guard "
          "boat on watch every night close that gap. Ferry captains grumble about the extra half hour at the boom gate.",
          ('security', 'navy'), after_any=('ms_drills', 'ms_a_pens'), reward=(Idea('harbour_booms'),)),
))

AIR = Branch('air', 'Two Island Air Wings', 1992, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_wings', 'Inspect the Two Air Wings',
          "Nihon's air arm is seventy-two fighters and twelve support aircraft divided between two fields, one in the Capital "
          "District and one in District E. Neither field can reach the outer districts and return with fuel to spare. An "
          "inspection of airframes, engines and pilots finds a capable force with very short legs, guarding a country that is "
          "mostly sea.",
          ('air', 'runway'), reward=(Idea('two_wings'), XP('air', 10))),
    Focus('air_h_field', 'An Airfield for District H',
          "District H holds nearly a third of the main island's industry and has no airfield at all. A field on the flat ground near "
          "its logistics centre spreads the air wings across three bases instead of two and puts fighters over the plant town "
          "within minutes. The ground is jungle and must be cleared, drained and paved before the first landing.",
          ('runway', 'tools'), after=('air_wings',), reward=(Build('air_base', 2, 582),)),
    Focus('air_wet_rules', 'Flying Rules for the Wet Season',
          "For months of every year the islands sit under rain, low cloud and violent squalls, and the air wings simply stop "
          "flying. New rules for instrument approaches, alternate fields and weather briefings keep at least some aircraft "
          "airborne in all but the worst storms. Pilots train harder, and the accident rate rises before it falls.",
          ('air', 'training'), after=('air_wings',), reward=(Idea('wet_season_flying'),)),
    Focus('air_interceptors', 'Interceptors over the Capital',
          "One school wants the fighters kept close to home: the capital, the yards, the silo and the plant towns, defended by "
          "interceptors on short alert. It is the cheapest way to protect what matters most. It also means the outer districts "
          "and the merchant lanes will see a friendly aircraft only on the national holiday.",
          ('air', 'radar'), after=('air_wet_rules',), exclusive=('air_patrol',),
          reward=(SwapIdea('two_wings', 'capital_interceptors'),)),
    Focus('air_patrol', 'Patrol Wings over the Lanes',
          "The other school trains the support aircraft and a share of the fighters to find ships, shadow intruders and cover "
          "convoys near the islands. It suits a country that lives by its hulls. The training is long, the fuel bill is large, "
          "and the capital's own sky becomes the job of whatever is left on the ground.",
          ('air', 'navy'), after=('air_wet_rules',), exclusive=('air_interceptors',),
          reward=(SwapIdea('two_wings', 'lane_patrol'),)),
    Focus('air_e_radar', 'Radar on the District E Ridge',
          "The District E airfield sits below hills that hide every approach from the west. A radar station on the ridge above "
          "the field gives the fighters warning in minutes rather than seconds. The ridge road must be cut first, and the "
          "station's crew will live on a hilltop in the rain for most of the year.",
          ('radar', 'air'), after=('air_h_field',), reward=(Build('radar_station', 1, 251),)),
    Focus('air_d_strip', 'A Landing Strip in the D Chain',
          "The islets of District D lie between the main island and the eastern lanes, and a single strip on the largest of "
          "them lets aircraft refuel halfway across. The strip is short, the crosswinds are bad and the fuel arrives by barge. "
          "It is still the first place beyond the main island where a Nihonian aircraft can land.",
          ('runway', 'navy'), after_any=('air_interceptors', 'air_patrol'), reward=(Build('air_base', 1, 239),)),
    Focus('air_north_ground', 'A Landing Ground in the North',
          "The northern outlier is the most isolated district in the country, and in an emergency a ship from the capital takes "
          "days to reach it. A grass landing ground near its harbour lets a transport bring medicine, officials or a repair crew "
          "in hours. In wartime it would also be the most exposed field Nihon possesses.",
          ('runway', 'civil'), after=('air_d_strip',), requires=(Completed('isl_outlier'),), reward=(Build('air_base', 1, 431),)),
    Focus('air_support', 'Close Support for the Hill Battalions',
          "The twelve support aircraft have never trained with the army, which would fight, if it ever fought, in jungle "
          "valleys where targets vanish under the canopy. Joint exercises with the battalions in District E teach pilots to "
          "find smoke markers and soldiers to call them in. Both services complain that the other is too slow, which is how "
          "they learn.",
          ('missile', 'training'), after_any=('air_interceptors', 'air_patrol'),
          reward=(Research('air_doctrine', 0.5, 1), XP('air', 10))),
))

ARMY = Branch('army', 'Battalions in the Jungle Hills', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('ar_towns', 'Walk the Three Garrison Towns',
          "The army is six volunteer battalions in pairs at the capital centre and the two logistics centres of District E and "
          "District H. None is stationed in District B or anywhere off the main island. An inspection by the general staff, on "
          "foot and by boat, finds disciplined units trained for a country they mostly cannot reach.",
          ('training', 'security'), reward=(Idea('hill_battalions'),
                                            Tooltip('The battalions stay where they are; this focus moves no units.'))),
    Focus('ar_jungle', 'A Jungle School in District B',
          "Most of Nihon's land is jungle, and its battalions train mostly on parade grounds and roads. A jungle school in the "
          "empty valleys of District B runs courses in navigation, river crossing, patrolling and survival under the canopy. "
          "The school uses the hill road as its supply line, and its graduates come back thin, sunburnt and far more capable.",
          ('training', 'civil'), after=('ar_towns',), reward=(Idea('jungle_school'),)),
    Focus('ar_pay', 'Pay That Keeps Volunteers',
          "The army is volunteer only, and it loses its best soldiers to the shipping houses and the plant towns, which pay more "
          "for the same skills. A new pay scale with housing, a trade course and a pension after twelve years keeps them. It "
          "costs the treasury every year, and the national movement demands to know why soldiers must be bought.",
          ('economy', 'training'), after=('ar_towns',), reward=(Idea('volunteer_pay'),)),
    Focus('ar_companies', 'Rifle Companies for the Districts',
          "One answer spreads the army thin and visible: a rifle company in every district, from District A to the northern "
          "outlier, living among the people it would defend. The outer islands feel protected for the first time. The "
          "battalions lose their cohesion, and no commander can gather more than a few companies in one place quickly.",
          ('security', 'civil'), after=('ar_jungle',), cost=10, exclusive=('ar_sailing',),
          reward=(Idea('district_garrisons'), Flag('army_garrison'))),
    Focus('ar_sailing', 'A Reserve That Sails',
          "The other answer keeps the battalions together on the main island and gives them the means to move: requisition "
          "rights on ferries, loading drills on every quay and a staff that plans each embarkation. The outer islands would "
          "wait days for help, yet when it came it would be a whole battalion. The plan depends on the merchant fleet being in "
          "port.",
          ('logistics', 'navy'), after=('ar_jungle',), cost=10, exclusive=('ar_companies',),
          reward=(Idea('sailing_reserve'), Flag('army_mobile'))),
    Focus('ar_lines', 'Company Lines in District A',
          "Companies in the outer districts need barracks, a well, a radio hut and a road from the landing to the lines. The "
          "army engineers begin in District A, on the far southwestern fringe, and spend two seasons away from the "
          "main island. The barracks become the largest buildings on the shore and their canteen becomes the busiest shop.",
          ('rebuild', 'security'), after=('ar_companies',), requires=(HasFlag('army_garrison'),),
          reward=(Build('infrastructure', 1, 84),)),
    Focus('ar_embark', 'Embarkation Drill on the Quays',
          "Twice a year a battalion is called out at night, marched to the capital quays and loaded onto requisitioned ferries "
          "before dawn. The first drill takes eleven hours and loses a field kitchen in the harbour. By the fourth the battalion "
          "is aboard in under five, and the ferry operators have learned to keep one hull ready.",
          ('logistics', 'training'), after=('ar_sailing',), requires=(HasFlag('army_mobile'),),
          reward=(Idea('embark_drill'), XP('army', 10))),
    Focus('ar_depots', 'Stock the Garrison Depots',
          "The country's research priority is physical sustainment: keeping trucks running, rifles replaced and service "
          "affordable. The army turns that priority into depots stocked for ninety days in each garrison town, with spares for "
          "the trucks, the trains and the radios. Stock that sits too long rots in the humidity, so every depot rotates it on a "
          "strict calendar.",
          ('tools', 'logistics'), after_any=('ar_lines', 'ar_embark'), reward=(Idea('depot_spares'),)),
    Focus('ar_engineers', 'Engineers for the Wet Season',
          "Every wet season washes out bridges, buries roads and floods the garrison towns, and the army is the only body with "
          "the trucks and the discipline to clear them. An engineer company with bridging kit and earthmovers turns that habit "
          "into a duty. The battalions resent losing their best mechanics to a unit that mostly digs.",
          ('tools', 'rebuild'), after=('ar_pay',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 5))),
))

STAR = Branch('star', 'Under the Falling Star', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('st_bulletin', 'Translate the Asteroid Bulletin',
          "Astronomers announce that the asteroid Ulysses will pass close to the Earth, with a real chance of striking it. The "
          "news reaches Nihon as foreign wire copy that few officials can judge. A small bureau in the capital translates, "
          "checks and publishes every bulletin, so that rumours in the plant towns meet facts before they turn into panic.",
          ('telescope', 'document'), requires=(After('1994.12.10'),), reward=(Idea('star_bulletins'), Event('falling_star'))),
    Focus('st_observatory', 'An Observatory on the Capital Mountain',
          "The Capital District rises to a single mountain province above its hills, the highest ground in the country. A "
          "modest observatory on the summit will never find an asteroid first, but it lets island astronomers confirm foreign "
          "reports and train students of their own. The summit road is steep, and the instruments are expensive and imported.",
          ('telescope', 'science'), after=('st_bulletin',), reward=(Idea('mountain_observatory'),)),
    Focus('st_tide_gauges', 'Tide Gauges on Every Coast',
          "If a fragment ever falls into the ocean, the danger to an island country comes as a wave, not a crater. Tide gauges "
          "in every district harbour, wired to the capital, can show a sudden rise long before it reaches the next coast. The "
          "gauges themselves are cheap. Keeping their lines working through every wet season is not.",
          ('fishing', 'communications'), after=('st_bulletin',), reward=(Idea('tide_gauges'),)),
    Focus('st_impact_word', 'Word That Ulysses Will Strike',
          "Two years after the first warning, the FCU tells the world that the asteroid will hit and that it means to counter "
          "the strike. No government can yet say where the pieces will land. Nihon must now get ready for a danger that may "
          "never touch its coasts, paying for shelters and stores out of a budget already stretched by ferries and roads.",
          ('meteor', 'communications'), after=('st_bulletin',), requires=(After('1996.4.20'),),
          reward=(Event('impact_word'), Tooltip('Opens the two shelter plans; only one can be taken.'))),
    Focus('st_hill_shelters', 'Shelters Under the Capital Hills',
          "One plan digs into the hills behind the capital: deep shelters for a large share of the main island's people, with "
          "stores, water and generators for weeks. It protects the most people for each unit of money spent. It also asks the "
          "outer districts to trust that a ferry will arrive in time to bring them to shelter.",
          ('shelter', 'civil'), after=('st_impact_word',), cost=10, exclusive=('st_dispersal',),
          reward=(Idea('hill_shelters'), Flag('shelter_central'))),
    Focus('st_dispersal', 'Stores on Every Island',
          "The other plan accepts that nobody knows where fragments will fall and spreads the risk instead: grain, fuel, "
          "medicine and water stored in every district, with a small shelter in every town. No single strike could destroy the "
          "national reserve. Each district shelter is shallower and weaker, and the stores must be guarded in eight places "
          "instead of one.",
          ('refugees', 'shelter'), after=('st_impact_word',), cost=10, exclusive=('st_hill_shelters',),
          reward=(Idea('island_stores'), Flag('shelter_dispersed'))),
    Focus('st_galleries', 'Tunnels Between the Shelter Halls',
          "The capital shelters were dug as separate halls, and engineers now link them with galleries so that people, water "
          "and power can move between them if one entrance collapses. The work runs through the hills for two years. It turns "
          "the shelters into a small underground town that the ministries quietly plan to use for themselves.",
          ('shelter', 'tools'), after=('st_hill_shelters',), requires=(HasFlag('shelter_central'),),
          reward=(Idea('shelter_galleries'),)),
    Focus('st_store_ships', 'Store Ships at Anchor',
          "Old merchant hulls from the register are stripped, stocked with grain and water and anchored in the sheltered bays of "
          "the outer districts. A ship can move away from a threatened coast, or toward a stricken one, faster than any "
          "warehouse. Their owners are paid a retainer for hulls that will never carry another cargo.",
          ('navy', 'refugees'), after=('st_dispersal',), requires=(HasFlag('shelter_dispersed'),),
          reward=(TimedIdea('store_ships', 1095),)),
    Focus('st_roche', 'Watch Through the Roche Night',
          "Ulysses passes through the Roche limit and begins to break apart. Every shelter, store ship and tide gauge in Nihon is "
          "manned through the night while radio stations relay foreign reports hour by hour. Whatever the sky brings to other "
          "countries, the island government is judged tonight by whether its people knew where to go.",
          ('meteor', 'civil'), after_any=('st_galleries', 'st_store_ships'), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'), Stability(0.02))),
    Focus('st_board', 'A Standing Emergency Board',
          "The asteroid years leave behind an organisation nobody wants to dismantle: wardens, radio nets, shelter plans and "
          "stores in every district. A standing emergency board takes them over under one statute, with a budget for storms, "
          "floods and fires as well as the sky. Its first real test will be the next wet season.",
          ('document', 'medical'), after=('st_roche',), reward=(Idea('emergency_board'),)),
))

FAR = Branch('far', 'Wars Beyond the Horizon', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('fw_belkan', 'Word of War in Belka',
          "The Belkan War breaks out on the far side of the ocean, and the first effect in Nihon is a letter from every foreign "
          "underwriter raising premiums on hulls bound anywhere near the north. No Nihonian interest is at stake in the "
          "fighting. Yet the island economy lives on freight, fuel and insurance, and all three move with the war.",
          ('communications', 'missile'), requires=(After('1995.3.25'),), reward=(Idea('war_premiums'), Event('belkan_news'))),
    Focus('fw_clean_cargo', 'No Cargo for the Belligerents',
          "One posture forbids any Nihonian hull to carry cargo for an army at war, on pain of losing its registration. It "
          "costs the fleet the best-paying charters of the decade. It also earns the island flag a reputation that insurers, "
          "ports and neutral governments will remember long after this war has ended.",
          ('peace', 'navy'), after=('fw_belkan',), exclusive=('fw_any_buyer',),
          reward=(SwapIdea('war_premiums', 'clean_cargo'), Flag('posture_clean'))),
    Focus('fw_any_buyer', 'Charters for Any Paying Buyer',
          "The other posture lets owners charter their hulls to whoever pays, provided the voyage avoids declared war zones, "
          "and taxes the profit. "
          "Money pours into the shipping houses and the capital yards. Every cargo that later turns out to have served a "
          "belligerent becomes an argument at home and a mark against the island flag abroad.",
          ('economy', 'diplomacy'), after=('fw_belkan',), exclusive=('fw_clean_cargo',),
          reward=(SwapIdea('war_premiums', 'any_buyer'), Flag('posture_open'))),
    Focus('fw_belka_won', 'Trading with a Victorious Belka',
          "If the war ends with Belka victorious, the northern ports answer to a government that won its war, and the island "
          "shipowners must decide whether to trade with it at all. The ministry negotiates commercial terms for ordinary cargo "
          "only, with no endorsement of the outcome. Critics at home say that any terms at all are terms with a conqueror.",
          ('diplomacy', 'scales'), after_any=('fw_clean_cargo', 'fw_any_buyer'), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_victor_terms', 730),)),
    Focus('fw_belka_lost', 'The War Clause Is Struck',
          "If the war ends with Belka defeated and a treaty signed, the underwriters strike the war clause from northern "
          "policies and premiums drift back toward normal. The hull mutual passes the saving to its members at once. Owners "
          "who chartered to belligerents find that some ports now ask awkward questions about their earlier voyages.",
          ('scales', 'navy'), after_any=('fw_clean_cargo', 'fw_any_buyer'), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(TimedIdea('clause_lifted', 730),)),
    Focus('fw_skully', 'Gunfire off Southern Usea',
          "Rebel forces hold a base in the Skully Islands of southern Usea until FCU forces and Unified Command eliminate it at "
          "the end of the year. The fighting is far from Nihon, but the lanes to the Usean coast pass through waters where armed "
          "rebels operated. The shore watch begins plotting every hull on those lanes, whatever its flag.",
          ('security', 'navy'), after_any=('fw_clean_cargo', 'fw_any_buyer'), requires=(After('1995.12.31'),),
          reward=(Idea('southern_watch'),)),
    Focus('fw_coup', 'Coup Season in the Usean Ports',
          "A coup breaks out across Usea, and rebel forces are defeated by Unified Command. For a few weeks nobody knows which "
          "Usean ports are open, which governments will honour their debts and which crews will be detained. Island hulls caught "
          "in Usean harbours wait for orders, and their families queue at the capital shipping offices for news.",
          ('command', 'refugees'), after=('fw_skully',), requires=(After('1997.5.30'),), reward=(Event('usean_coup'), WarSupport(0.01))),
    Focus('fw_evacuees', 'Berths for Usean Families',
          "The clean-cargo rule makes Nihonian hulls welcome where others are searched, and families leaving the troubled Usean "
          "ports ask them for passage. The government offers berths on scheduled sailings at cost and a reception hall on the "
          "capital quay. The numbers are small and the gratitude is large, while the movement complains about foreigners on "
          "public ships.",
          ('refugees', 'medical'), after=('fw_coup',), requires=(HasFlag('posture_clean'),), reward=(Idea('evacuee_berths'),)),
    Focus('fw_coup_rates', 'Charter Rates in the Coup Season',
          "Owners who chartered freely during the Belkan years now carry anything the disrupted Usean ports will pay for, at "
          "rates that rise every week the coup season lasts. The tax on charter profits funds the capital yards for a year. The "
          "Maritime Service warns that some of these hulls are sailing into harbours where nobody knows who is in charge.",
          ('economy', 'navy'), after=('fw_coup',), requires=(HasFlag('posture_open'),), reward=(TimedIdea('coup_premiums', 365),)),
    Focus('fw_railgun', 'A Railgun Battery in San Salvacion',
          "The FCU completes Stonehenge, a battery of enormous railguns in a desert region of neutral San Salvacion. Nihon's air "
          "staff studies every published figure on its range and rate of fire. A weapon that can reach the sky over a whole "
          "region is a new fact of life for any country that depends on aircraft and open lanes.",
          ('missile', 'radar'), after=('fw_coup',), requires=(After('1998.6.19'),), reward=(Idea('railgun_study'),)),
))

USEA = Branch('usea', 'The Usean War at Sea', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('cw_crisis', 'The San Salvacion Crisis',
          "By the summer of 2003 the Usean powers are quarrelling over Stonehenge, the railgun complex in neutral San "
          "Salvacion, and the lanes to the Usean coast fill with rumours. Whether the quarrel becomes a war will be decided in "
          "Usea, not in Nihon. The island government opens a crisis desk to follow it and to settle what its fleet will do "
          "either way.",
          ('missile', 'communications'), requires=(After('2003.6.1'),), reward=(Idea('crisis_desk'), Event('usean_crisis'))),
    Focus('cw_war', 'Erusea Takes the Railguns',
          "Erusea invades San Salvacion, seizes Stonehenge and turns its railguns on the sky as anti-air batteries. The Usean war "
          "the crisis desk feared has begun. Insurers cancel Usean cover overnight, fuel prices jump and the shore watch counts "
          "how many island hulls are in Usean waters. Every shipowner in the capital wants to know what the government will "
          "allow.",
          ('missile', 'security'), after=('cw_crisis',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(TimedIdea('usean_war_rates', 730),)),
    Focus('cw_averted', 'A Usean Crisis Without War',
          "If the Usean crisis ends without war, the crisis desk closes and the lanes reopen on ordinary terms. Insurers cut "
          "their premiums, fuel prices ease and the shipping houses resume their regular Usean calls. The government must "
          "explain why it spent money preparing for a war that never came, and whether it would do the same again.",
          ('peace', 'scales'), after=('cw_crisis',), requires=(HasGlobal('ac_ucw_war_averted'),),
          reward=(TimedIdea('quiet_lanes', 730),)),
    Focus('cw_g_radar', 'Air Watch over District G',
          "District G lies closer to the Sotoan coast than any other Nihonian district, beside the busiest lanes of the eastern "
          "sea. A radar station on its plains watches the air and the shipping alike and warns the main island of anything "
          "approaching from that side. It changes no claim, but it does tell everyone across the strait that the district is "
          "watched.",
          ('radar', 'security'), after=('cw_crisis',), reward=(Build('radar_station', 1, 524),)),
    Focus('cw_neutral', 'Neutral Lanes Around Usea',
          "One course keeps every Nihonian hull out of the war: no cargo for either side, routes published in advance and lights "
          "burning at night so that every patrol can identify the island flag. It gives up the war's richest charters. It also "
          "lets island ships keep sailing where others are sunk or seized.",
          ('peace', 'navy'), after=('cw_war',), exclusive=('cw_fuel',), reward=(Idea('neutral_lanes'), Flag('lanes_neutral'))),
    Focus('cw_fuel', 'Fuel for the Allied Ports',
          "The other course sells refined fuel and charters tankers to the ports supplying the forces arrayed against Erusea, "
          "under commercial contracts that commit no Nihonian forces and change no alliance. The refinery and the tanker owners "
          "have their best years since the Belkan War. Erusean patrols may treat every tanker under the island flag as a target.",
          ('industry', 'diplomacy'), after=('cw_war',), exclusive=('cw_neutral',),
          reward=(Idea('allied_fuel'), Flag('lanes_fuel'))),
    Focus('cw_relief', 'Relief Voyages Under the Island Flag',
          "Neutral lanes make relief possible. Island hulls carry food, medicine and water to Usean ports cut off by the "
          "fighting, under international supervision and with their manifests published. Every voyage is dangerous and is "
          "reported in every Nihonian newspaper. The sailings win the country goodwill at little cost, though the crews know "
          "how exposed a lit hull is.",
          ('medical', 'peace'), after=('cw_neutral',), requires=(HasFlag('lanes_neutral'),), reward=(Idea('relief_voyages'),)),
    Focus('cw_north_point', 'Tankers on the North Point Run',
          "With the allied headquarters established at North Point, the fuel contracts concentrate on one long run to its "
          "harbours. Island tankers sail in groups with lights out and radios silent for days. Each voyage pays like "
          "three ordinary ones, each loss is mourned in the capital, and the plant towns argue about whose sons crew the tankers.",
          ('navy', 'industry'), after=('cw_fuel',), requires=(HasFlag('lanes_fuel'), After('2004.9.16')),
          reward=(TimedIdea('north_point_run', 365),)),
    Focus('cw_isaf_won', 'Usean Ports Reopen',
          "If the war ends with the Erusean surrender, the Usean ports reopen for rebuilding and need every hull, crane and "
          "tanker they can charter. Nihonian shipowners bid for coastal and fuel contracts in the damaged harbours. Buyers "
          "remember who carried relief and who carried fuel, and the earlier choice of the island government decides who is "
          "welcome first.",
          ('rebuild', 'economy'), after_any=('cw_neutral', 'cw_fuel'), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('reopened_ports', 730),)),
    Focus('cw_erusea_won', 'Terms with the Erusean Victors',
          "If the war ends with Erusea prevailing, every island cargo bound for Usea must pass through ports governed by the "
          "victors. The ministry negotiates tariffs and berthing rights for ordinary trade without recognising what Erusea "
          "seized. It keeps the hulls moving, and every faction at home says the price was far too high.",
          ('diplomacy', 'scales'), after_any=('cw_neutral', 'cw_fuel'), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(TimedIdea('erusean_terms', 730), PP(20))),
    Focus('cw_accounts', 'Every District Writes It Down',
          "Fourteen years after the programme began, every district commissioner, board and service chief sends the capital a "
          "written account of what changed on their island and what did not. The ministries bind the accounts into one volume "
          "and debate it for a session. The volume settles nothing by itself, but every camp will quote it for years to come.",
          ('document', 'assembly'), after_any=('cw_relief', 'cw_north_point', 'cw_averted', 'cw_g_radar', 'cw_isaf_won',
                                                'cw_erusea_won'),
          requires=(After('2005.1.1'),),
          reward=(Idea('island_programme'), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (THRONE, ISLANDS, HULLS, PLANTS, SERVICE, AIR, ARMY, STAR, FAR, USEA)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('wet_round', 'Sail the Wet-Season Round',
                'Each outer-district call is kept even in the worst weather, with an escort sailing in company. It can be '
                'ordered again after a year, and every round burns fuel the treasury would rather sell.',
                35, (TimedIdea('wet_season_round', 120), XP('navy', 10)), requires=(Completed('isl_timetable'),), cooldown=365),
    DecisionDef('b_hill_road', 'Pave the District B Hill Road',
                'Engineers pave the graded hill road into District B and bridge its worst river crossing. Done once; the road '
                'gangs then return to the ministry.',
                75, (Build('infrastructure', 1, 130),), requires=(Completed('isl_b_track'),)),
    DecisionDef('north_works', 'A Works Shed for the North',
                'The treasury pays for a repair and assembly works beside the northern anchorage. It is paid for once, and every '
                'machine must travel days by sea.',
                100, (Build('industrial_complex', 1, 431),), requires=(Completed('isl_outlier'),)),
    DecisionDef('shelter_bells', 'Ring the Shelter Bells',
                'Wardens ring the bells at dawn and every town walks to its shelter with a stopwatch running. It may be repeated '
                'after twelve months; the plants lose a shift each time.',
                25, (TimedIdea('bells_rehearsed', 90), Stability(0.01)), requires=(Completed('st_impact_word'),), cooldown=365),
    DecisionDef('register_audit', 'Audit the Hull Register',
                'The harbour boards check every entry on the merchant register and strike off hulls that no longer sail. It can '
                'be ordered again a year later, and shipowners resent every visit.',
                30, (TimedIdea('register_audited', 180),), requires=(Completed('hl_register'),), cooldown=365),
    DecisionDef('sotoan_harbour_talks', 'Invite Sotoan Harbour Officials',
                'Harbour officials from Sotoa are invited to District G so that mooring and fishing disputes can be settled by '
                'telephone. It can be done only once, and no claim or border changes.',
                50, (Stability(0.02), PP(15)), requires=(Completed('isl_g_office'),)),
)
