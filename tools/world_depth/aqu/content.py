"""Aquitoria (AQU): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a crown government with the
chamber unelected since November 1987, monarchism 50, democratic 21, communism 21 and
neutrality 8 percent popularity), the unnamed Office of the Crown, the party-specific
country names, the single 1991 state with its four provinces, and the global flags other
mod scripts already set. Official: ACES Chronicle rows used only as date anchors for
distant pressures, each cited by its exact key. Everything else, including every
Aquitorian choice, office, idea, building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='AQU', name='Aquitoria', root='world', package='aqu',
                  themes=('medal', 'navy', 'rail'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party monarchism; last_election 1987.11.9, election_frequency 48, elections_allowed = '
           'no; popularities monarchism 50, democratic 21, communism 21, neutrality 8; stability and war support 0.5; three '
           'research slots; tech_mountaineers, early_fighter and basic_train among the starting technologies. The starting '
           'leader is the unnamed Office of the Crown (AQU_ac_government_office, constitutional_monarchy), whose description '
           'says its 1991 holder has not been established. Party names: Kingdom of Aquitoria (monarchism, neutrality, '
           'fascism), Aquitorian Republic (democratic), Aquitorian Commune (communism). The tree never names a holder.',
           'mod/2985041246/history/countries/AQU - Aquitoria.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: one 1991 state, 435 (capital, state_category city, six shared slots), captioned Aquitoria. Provinces: '
           '2238 coastal plains with naval base 1, a supply node and victory point 20 (its localised name carries a non-ASCII '
           'letter, so the tree calls it the capital port); 8331 coastal plains; 8435 plains with a supply node and victory '
           'point 5, captioned Aquitoria Logistics Centre 8435; 5806 hills. A level-2 railway joins 2238 and 8435 only. '
           'Buildings: infrastructure 5 (the cap), 3 industrial complexes and 3 arms factories (all six shared slots used), no '
           'air base, dockyard or fuel silo. Resources oil 4, steel 5, rubber 2. Land neighbours MST (via 784, 1428, 8526) and '
           'VLK (via 1637, 4257, 8243) computed from map/provinces.bmp; sea province 10722 off 2238 and 8331. Compass words '
           'come from province centroids. No place outside these captions is named.',
           'mod/2985041246/history/states/435-State_435.txt; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/supply_nodes.txt; mod/2985041246/map/definition.csv; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Neighbours as inherited: Monstrua ruled by its fascism party with 90 percent popularity and elections suspended; '
           'Valka ruled by its democratic party with neutrality 48 and fascism 50 percent popularity and elections suspended. '
           'The tree describes them only through these figures and never changes their borders, cores or factions.',
           'mod/2985041246/history/countries/MST - Monstrua.txt; mod/2985041246/history/countries/VLK - Valka.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small territorial service; 3 civilian and 3 military factories, no '
           'dockyard; 2 infantry formations (4 battalions); stocks of 800 infantry equipment, 560 motorized equipment and 24 '
           'trains; 60 convoys; combat air and combat navy deliberately absent; infantry-only service without engineer or '
           'artillery companies; research priority Physical Sustainment. Fiscal calibration GDP 72 billion, debt ratio 0.3, '
           'collection 0.85, growth 3.0, inflation 2.0; crown_office institution, capacity 40. Fictional gameplay calibration, '
           'not canon national accounts.',
           'tools/world_starts/profiles.json; tools/economy_v2/profiles.json; tools/institutions/profiles.json; '
           'docs/WORLD_STARTS_CALIBRATION.md; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses may strike the Earth. Background to the asteroid branch '
           'only; no Aquitorian role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Used as the date gate of the distant-war branch; Aquitoria takes no part.',
           '1995 / 03.25'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Background to the radiation watch focus, '
           'which also reads the mod flag belka_dropped_nukes; no effect on Aquitoria is claimed.', '1995 / 06.06'),
    Source('Official',
           'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Used as the date gate of the peace focus.',
           '1995 / 06.20'),
    Source('Official',
           'Date anchor: the FCU announces that Ulysses will impact the Earth. Used as the date gate of the asteroid branch; '
           'where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries and work as aggressor squadrons. Date '
           'gate and premise of the aggressor instructors focus; no individual is named and no Aquitorian hire is claimed as '
           'fact.', '1998 / 06.19'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Date gate of the Roche night focus and event; no '
           'damage in Aquitoria is claimed.', '1999 / 07.08'),
    Source('Official',
           'Date anchor: Erusea stops taking in refugees. Date gate of the refugee berths focus, framed as an expected pressure '
           'rather than a recorded arrival.', '2000 / 04.21'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air batteries. '
           'Opening of the Usean war branch.', '2003 / SUMMER'),
    Source('Official',
           'The FCU establishes the ISAF. Date gate of the ISAF cargo focus, which is trade only and changes no faction.',
           '2003 / 08.22'),
    Source('Official',
           'Farbanti falls, the ISAF accepts the Erusean surrender and the Continental War ends. Background only; the outcome '
           'focuses read the mod outcome flags instead of assuming this ending.', '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war, belka_lost_belkan_war and belka_dropped_nukes '
           '(events/Belka.txt); ac_ucw_stonehenge_destroyed, ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory '
           '(common/scripted_effects/ac_ucw.txt). Each reaction is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Aquitorian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in state '
           '435 (air base and radar, the only free capacity there).'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the 1987 question
    IdeaDef('crown_office_rule', 'Orders of the Crown Office', 'The crown governs alone on orders renewed each year since the chamber closed in 1987.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('medal', 'document')),
    IdeaDef('petition_office', 'The Petition Office', 'Clerks at the palace gate read and answer every petition.',
            {'stability_factor': 0.02, 'political_power_factor': 0.05}, ('document', 'medal')),
    IdeaDef('open_registers', 'Open Party Registers', 'Loyalists, democrats and communists may register members and print newspapers.',
            {'stability_factor': 0.02, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('compact_promise', 'Promise of a Compact', 'The crown has promised to share government with a reopened chamber.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('scales', 'medal')),
    IdeaDef('republican_clubs', 'The Republican Clubs', 'Democratic clubs gather signatures for a republic in every ward.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03, 'research_speed_factor': 0.02}, ('ballot', 'assembly')),
    IdeaDef('dock_councils', 'Councils on the Docks', 'Workers on the quay and in the halls elect councils that claim a voice in government.',
            {'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.03}, ('assembly', 'tools')),
    IdeaDef('privy_seals', 'The Seals Stay with the Crown', 'Hardline courtiers hold that the crown alone may govern.',
            {'political_power_gain': 0.15, 'stability_factor': -0.03}, ('medal', 'security')),
    IdeaDef('responsible_ministry', 'A Ministry Answerable to the Chamber', 'Ministers chosen by the chamber govern; the crown signs on their advice.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05}, ('assembly', 'scales')),
    IdeaDef('republican_charter', 'The Republican Charter', 'A written charter: an elected president, one chamber, a court and a free press.',
            {'stability_factor': 0.06, 'research_speed_factor': 0.03, 'political_power_gain': -0.05}, ('document', 'ballot')),
    IdeaDef('council_economy', 'The Council Economy', 'Workers councils read the books and set the shifts of every firm.',
            {'production_factory_efficiency_gain_factor': 0.06, 'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('assembly', 'industry')),
    IdeaDef('privy_decrees', 'Code of Privy Decrees', 'A permanent code of decrees issued by the privy council.',
            {'political_power_gain': 0.20, 'stability_factor': 0.03, 'war_support_factor': 0.04}, ('document', 'security')),
    # the four provinces
    IdeaDef('ward_survey', 'The Province Survey', 'Houses, wells and tax rolls of the four provinces have been counted.',
            {'stability_factor': 0.02, 'production_speed_buildings_factor': 0.05}, ('document', 'civil')),
    IdeaDef('port_water', 'Mains for the Port Wards', 'The older wards of the capital port have water through the summer.',
            {'stability_factor': 0.03}, ('civil', 'tools')),
    IdeaDef('rent_board', 'The Rent Board', 'A board caps and reviews leases on the northern coastal plain.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('scales', 'civil')),
    IdeaDef('hill_schools', 'Schools in the Hills', 'Secondary schools keep hill families in the eastern province.',
            {'research_speed_factor': 0.02, 'stability_factor': 0.02}, ('science', 'civil')),
    IdeaDef('elected_wards', 'Elected Province Councils', 'Each province has an elected council and a budget line of its own.',
            {'stability_factor': 0.05, 'production_speed_buildings_factor': 0.08}, ('ballot', 'civil')),
    IdeaDef('crown_commissioner', 'The City Commissioner', 'One appointed commissioner runs the works of all four provinces.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.08}, ('command', 'civil')),
    IdeaDef('open_budgets', 'Budgets on the Hall Doors', 'Province budgets are published and debated in open session.',
            {'stability_factor': 0.04, 'political_power_factor': 0.03}, ('scales', 'ballot')),
    IdeaDef('works_plan', 'The Commissioner Works Plan', 'One ranked plan for housing and drainage across the kingdom.',
            {'production_speed_buildings_factor': 0.08, 'political_power_gain': 0.05}, ('document', 'command')),
    # the six plants
    IdeaDef('crowded_works', 'No Spare Ground', 'Every industrial site in the state is taken; growth must come from the halls already built.',
            {'production_factory_efficiency_gain_factor': 0.02, 'consumer_goods_factor': 0.02}, ('industry', 'document')),
    IdeaDef('home_fuel', 'Fuel Refined at Home', 'Enough crude is held back to run the refinery at full draw.',
            {'supply_consumption_factor': -0.05}, ('industry', 'logistics')),
    IdeaDef('crown_firms', 'Chartered Crown Firms', 'Private managers hold crown charters and guaranteed state orders.',
            {'production_speed_arms_factory_factor': 0.08, 'political_power_gain': 0.05}, ('medal', 'industry')),
    IdeaDef('shop_coops', 'Shop-Floor Cooperatives', 'Each plant is owned by its workforce and run by elected managers.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.02}, ('assembly', 'tools')),
    IdeaDef('open_tender', 'Management by Tender', 'Foreign firms manage the halls under contract.',
            {'production_factory_max_efficiency_factor': 0.04, 'consumer_goods_factor': -0.03}, ('economy', 'diplomacy')),
    IdeaDef('charter_orders', 'Ten-Year Crown Orders', 'Fixed-price state orders for rifles, trucks and steel plate.',
            {'production_speed_arms_factory_factor': 0.12, 'industrial_capacity_factory': 0.04}, ('document', 'industry')),
    IdeaDef('shift_councils', 'Shift Councils', 'Elected councils set rotas, training and maintenance in every hall.',
            {'production_factory_efficiency_gain_factor': 0.08, 'stability_factor': 0.03}, ('assembly', 'industry')),
    IdeaDef('foreign_lines', 'Foreign Machine Lines', 'Modern presses and lines installed in the old halls.',
            {'production_factory_max_efficiency_factor': 0.06, 'research_speed_factor': 0.02}, ('tools', 'economy')),
    IdeaDef('retooled_halls', 'A Hall Refitted Each Year', 'A rolling refit programme keeps every slot producing more.',
            {'industrial_capacity_factory': 0.06}, ('tools', 'industry')),
    # the capital port
    IdeaDef('convoy_register', 'The Convoy Register', 'Owners, cargoes and routes of the sixty convoys reported by radio each day.',
            {'naval_coordination': 0.04}, ('navy', 'document')),
    IdeaDef('pilots_guild', 'The Harbour Pilots Guild', 'Chartered pilots with training, fees and a duty roster.',
            {'naval_speed_factor': 0.03, 'navy_org_factor': 0.03}, ('navy', 'training')),
    IdeaDef('posted_tariffs', 'Posted Tariffs on the Quay', 'One customs house with printed tariffs and receipts.',
            {'political_power_factor': 0.05, 'consumer_goods_factor': -0.02}, ('scales', 'navy')),
    IdeaDef('free_port', 'The Free Port', 'No duty on transit goods; the quay runs for volume.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.01}, ('economy', 'navy')),
    IdeaDef('bonded_stores', 'Bonded Crown Warehouses', 'Imported fuel, grain and steel held under licence in crown sheds.',
            {'political_power_gain': 0.05, 'supply_consumption_factor': -0.03}, ('logistics', 'medal')),
    IdeaDef('port_accounts', 'Published Port Accounts', 'Tonnage, fees, losses and delays printed every year.',
            {'stability_factor': 0.02, 'naval_coordination': 0.03, 'political_power_factor': 0.03}, ('document', 'navy')),
    # the territorial service
    IdeaDef('territorial_service', 'The Territorial Service', 'Two infantry formations, four battalions, counted on one muster day.',
            {'army_core_defence_factor': 0.05}, ('training', 'security')),
    IdeaDef('hill_drill', 'Hill Drill', 'Every battalion trains a season on the eastern ridges.',
            {'army_defence_factor': 0.03, 'attrition': -0.05}, ('training', 'tools')),
    IdeaDef('hill_line', 'The Hill Line', 'Battalions assigned to prepared positions where the two frontiers meet.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.04}, ('security', 'bridge')),
    IdeaDef('wheeled_reserve', 'A Reserve on Wheels', 'The battalions held together near the logistics centre, moved by truck.',
            {'army_speed_factor': 0.06, 'army_org_factor': 0.04}, ('logistics', 'training')),
    IdeaDef('stocked_hills', 'Magazines in the Slopes', 'Stores and water cut into the hills behind each position.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.06, 'supply_consumption_factor': -0.05}, ('security', 'shelter')),
    IdeaDef('rail_reserve', 'Reserve by Rail', 'Troop trains and ramps let a battalion entrain within the hour.',
            {'army_speed_factor': 0.08, 'army_org_factor': 0.05, 'planning_speed': 0.05}, ('rail', 'training')),
    # two neighbours
    IdeaDef('frontier_customs', 'Two Customs Frontiers', 'Customs posts face Monstrua and Valka across the eastern hills.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.01}, ('diplomacy', 'security')),
    IdeaDef('valka_freight', 'Valkan Freight by Road', 'Valkan trucks cross the northern plain to the capital port on one manifest.',
            {'consumer_goods_factor': -0.03}, ('logistics', 'diplomacy')),
    IdeaDef('southern_market', 'The Southern Market Post', 'Lawful trade with the Monstruan hills through one customs post.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('economy', 'peace')),
    IdeaDef('valka_ties', 'Close Ties with Valka', 'Shared customs and a standing channel between the two cabinets.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.03}, ('diplomacy', 'peace')),
    IdeaDef('monstrua_terms', 'Terms with Monstrua', 'Quiet frontier talks and closed doors for Monstruan exiles.',
            {'army_core_defence_factor': 0.04, 'political_power_gain': 0.05, 'stability_factor': -0.02}, ('diplomacy', 'security')),
    IdeaDef('equal_distance', 'Equal Distance', 'The same tariffs, visits and refusals for both neighbours.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('scales', 'diplomacy')),
    IdeaDef('valka_students', 'Places in Valkan Colleges', 'Aquitorian students of engineering, medicine and law study in Valka.',
            {'research_speed_factor': 0.03}, ('science', 'diplomacy')),
    IdeaDef('quiet_south', 'A Quiet Southern Frontier', 'Patrols on agreed schedules; no incidents in the newspapers.',
            {'army_core_defence_factor': 0.06, 'political_power_gain': 0.05, 'stability_factor': 0.01}, ('peace', 'security')),
    IdeaDef('neutral_venue', 'Neutral Ground at the Port', 'Valkan and Monstruan officials meet in Aquitorian halls.',
            {'stability_factor': 0.05, 'political_power_gain': 0.08}, ('peace', 'diplomacy')),
    IdeaDef('frontier_commission', 'Frontier Commission of Three', 'A joint commission walks the line each spring.',
            {'stability_factor': 0.03, 'army_core_defence_factor': 0.03}, ('document', 'peace')),
    # air
    IdeaDef('air_office', 'The Air Office', 'A small office drafting the plan, budget and training of a future air arm.',
            {'experience_gain_air_factor': 0.05}, ('air', 'document')),
    IdeaDef('capital_flight', 'The Capital Fighter Flight', 'A dozen fighters on alert over the port and the arms halls.',
            {'air_superiority_efficiency': 0.06, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('liaison_flight', 'The Liaison Flight', 'Transports and light aircraft carrying officers, medicine and parts.',
            {'air_mission_efficiency': 0.05, 'supply_consumption_factor': -0.03}, ('air', 'logistics')),
    IdeaDef('hired_aggressors', 'Hired Aggressor Instructors', 'Contract instructors fly against the kingdom pilots in training.',
            {'experience_gain_air_factor': 0.12, 'political_power_gain': -0.05}, ('air', 'training')),
    # the Belkan War far away
    IdeaDef('war_freight_rates', 'Wartime Freight Rates', 'Charter rates and war clauses follow every cargo.',
            {'industrial_capacity_factory': 0.03, 'stability_factor': -0.02}, ('navy', 'economy')),
    IdeaDef('cash_orders', 'Cash Orders at the Halls', 'Rifles and rounds sold to any buyer who pays in cash.',
            {'production_speed_arms_factory_factor': 0.08, 'stability_factor': -0.02}, ('industry', 'missile')),
    IdeaDef('arms_closed', 'Halls Closed to Belligerents', 'Fuel and food sail; no weapons leave for the war.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.01}, ('peace', 'scales')),
    IdeaDef('export_licences', 'Licensed Arms Exports', 'Every arms export licensed with its buyer and end use published.',
            {'production_speed_arms_factory_factor': 0.10, 'political_power_factor': 0.03}, ('document', 'industry')),
    IdeaDef('clean_flag', 'A Flag with No Enemies', 'Aquitorian ships face fewer searches and win neutral charters.',
            {'stability_factor': 0.04, 'naval_coordination': 0.03}, ('peace', 'navy')),
    IdeaDef('radiation_watch', 'Radiation Watch at the Quay', 'Meters and inspectors check cargo from the war zone.',
            {'stability_factor': 0.02, 'air_detection': 0.05}, ('radar', 'medical')),
    IdeaDef('belkan_agents', 'Belkan Purchasing Agents', 'Orders for fuel, steel and trucks from a victorious Belka.',
            {'industrial_capacity_factory': 0.03, 'consumer_goods_factor': -0.02}, ('diplomacy', 'economy')),
    # the asteroid
    IdeaDef('asteroid_watch', 'Watch on Ulysses', 'Ministries plan for an impact nobody can place.',
            {'stability_factor': 0.01, 'air_detection': 0.05}, ('meteor', 'telescope')),
    IdeaDef('port_shelters', 'Shelters Beneath the Port', 'Shelters with sealed water under the capital port and the arms halls.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'navy')),
    IdeaDef('hill_evacuation', 'Routes into the Hills', 'Marked routes, trucks and trains to empty the coast on warning.',
            {'stability_factor': 0.03, 'planning_speed': 0.05}, ('refugees', 'rail')),
    IdeaDef('centre_stores', 'Depots at the Logistics Centre', 'Grain, medicine, fuel and water held at the kingdom crossroads.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('logistics', 'shelter')),
    IdeaDef('province_depots', 'A Depot in Each Province', 'Emergency stores spread by population across the four provinces.',
            {'stability_factor': 0.05, 'supply_consumption_factor': -0.04}, ('logistics', 'civil')),
    IdeaDef('chamber_drills', 'Drills Voted by the Chamber', 'Public evacuation drills with deputies of every camp taking part.',
            {'stability_factor': 0.05, 'war_support_factor': 0.02}, ('ballot', 'shelter')),
    IdeaDef('civic_wardens', 'Wardens of the Republic', 'Volunteer street wardens and first-aid posts in every ward.',
            {'stability_factor': 0.03, 'war_support_factor': 0.04}, ('civil', 'medical')),
    IdeaDef('council_rations', 'Council Rations', 'Grain, fuel and water rationed by household and posted on every door.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.02}, ('assembly', 'logistics')),
    IdeaDef('privy_curfew', 'The Privy Curfew', 'A night curfew and licensed movement between provinces.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('security', 'command')),
    IdeaDef('refugee_berths', 'Refugee Berths', 'Ships carrying displaced families may tie up at the quay.',
            {'political_power_gain': 0.05, 'stability_factor': -0.02}, ('refugees', 'navy')),
    # the Usean war far away
    IdeaDef('usean_premium', 'The Usean War Premium', 'Insurers price the Usean war into every Aquitorian voyage.',
            {'consumer_goods_factor': 0.02, 'industrial_capacity_factory': 0.03}, ('navy', 'missile')),
    IdeaDef('isaf_cargo', 'Cargo for the ISAF', 'Fuel, trucks and steel plate for ISAF depots; no troops committed.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.01}, ('diplomacy', 'logistics')),
    IdeaDef('closed_quay', 'A Quay Closed to War Cargo', 'Inspectors check that nothing loaded here reaches either army.',
            {'stability_factor': 0.04, 'naval_coordination': 0.02}, ('peace', 'navy')),
    IdeaDef('paying_freight', 'Freight for Paying Ports', 'Civilian buyers anywhere, paid in advance, no questions asked.',
            {'industrial_capacity_factory': 0.06, 'stability_factor': -0.03}, ('economy', 'navy')),
    IdeaDef('firm_overtime', 'Crown Firms on Three Shifts', 'Chartered firms take wartime contracts abroad.',
            {'production_speed_arms_factory_factor': 0.10, 'political_power_gain': 0.05}, ('industry', 'medal')),
    IdeaDef('coop_war_vote', 'War Work by Vote', 'Each cooperative hall votes whether to take wartime orders.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.02}, ('ballot', 'industry')),
    IdeaDef('tender_contracts', 'Contracts from Foreign Boardrooms', 'Foreign managers bid for wartime work for the tendered halls.',
            {'production_factory_max_efficiency_factor': 0.05, 'political_power_gain': -0.05}, ('economy', 'industry')),
    IdeaDef('transit_surge', 'Sheds Full of Transit Cargo', 'Cargo routed around the war is landed and reshipped at the port.',
            {'consumer_goods_factor': -0.04, 'naval_coordination': 0.02}, ('navy', 'logistics')),
    IdeaDef('steady_prices', 'Prices Held from Bond', 'Bonded fuel and grain released at steady prices.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.01}, ('scales', 'logistics')),
    IdeaDef('usean_rebuilding', 'Steel for Usean Rebuilding', 'Long-credit orders for ports, bridges and power lines in Usea.',
            {'production_speed_arms_factory_factor': 0.05, 'industrial_capacity_factory': 0.03}, ('rebuild', 'diplomacy')),
    IdeaDef('erusean_licence', 'The Erusean Shipping Licence', 'Aquitorian ships unload in Usea under Erusean inspection.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('diplomacy', 'scales')),
    # decisions
    IdeaDef('convoy_week_drill', 'Convoy Week', 'Every convoy reports on schedule and sails in company.',
            {'naval_coordination': 0.05}, ('navy', 'communications')),
    IdeaDef('field_exercise', 'Field Exercise in the Hills', 'Battalions manoeuvre on the eastern ridges.',
            {'army_org_factor': 0.04}, ('training', 'command')),
    IdeaDef('audience_day', 'Audience Day', 'Petitioners heard in person at the palace gate.',
            {'stability_factor': 0.03}, ('medal', 'peace')),
    IdeaDef('fair_days', 'Fair Days on the Southern Road', 'Open fair days at the southern customs post.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('economy', 'peace')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('compact_ministry', 'Ministry of the Crown Compact',
           'A ministry chosen by and answerable to the reopened chamber, governing under a written compact in which the crown '
           'keeps its title and seals but signs on the advice of its ministers. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('republic_council', 'Provisional Council of the Republic',
           'A collective council governing the Aquitorian Republic while its first presidential and chamber elections are '
           'prepared, the crown having withdrawn from government. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('commune_executive', 'Executive of the Councils',
           'An executive elected by delegates of the dock, shop and depot councils, governing the Aquitorian Commune and '
           'answerable to the councils rather than to a chamber. Provisional gameplay office with no named holder.',
           'communism', 'democratic_socialism'),
    Office('privy_council', 'Privy Council of the Crown',
           'A council appointed by the crown that holds every seal of government and rules by decree, with the chamber '
           'dissolved. Provisional gameplay office with no named holder.',
           'monarchism', 'absolutism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('locked_chamber', 'The Chamber Doors Stay Shut', (
        "The chamber of Aquitoria has not sat since the elections of November 1987. Its doors are locked, its benches lie "
        "under dust sheets and the Office of the Crown has governed alone through orders renewed each year by the palace "
        "lawyers. This year the lawyers have asked, for the first time, that a council of ministers sign the renewal "
        "alongside the crown.",
        "Outside the palace the kingdom is split in a way the old orders never anticipated. Half of the country remains "
        "loyal to the crown and expects it to go on governing. The other half is divided almost equally between democrats, "
        "who want the chamber reopened and a constitution written, and communists, who want the docks and arms halls run by "
        "the people who work in them. A small non-aligned remainder wants only lower prices.",
        "The ministers cannot settle the kingdom's future at a single sitting, but they must decide how the question will "
        "be handled. They can renew the orders quietly and let the matter rest another year, invite the three camps to argue "
        "it in public, or let the petitioners gathered at the palace gate in for a hearing that will certainly not stay "
        "polite.",
    ), (
        Option('Renew the orders quietly.', (PP(35), Stability(-0.02))),
        Option('Let the three camps argue in public.', (Stability(0.02), PP(-10))),
        Option('Open the gate to the petitioners.', (PP(10), Event('petition_night', 7))),
    ), picture=0),
    EventDef('petition_night', 'A Night at the Palace Gate', (
        "A week after the gate was opened, the crowd of petitioners has not gone home. Dock workers, tenant farmers from the "
        "northern plain and shopkeepers from the capital port camp on the palace square with blankets, lanterns and copies of "
        "the 1987 election lists. Their requests range from the price of bread to the abolition of the crown, written on "
        "the same sheets of paper.",
        "The palace guard is small and unused to crowds. Its officers ask whether they should clear the square before the "
        "night shifts at the arms halls finish and swell the numbers further. Loyalist notables send messages urging "
        "firmness. Democratic and communist organisers, who did not call the crowd, are working hard to take credit for it "
        "before the other camp can.",
        "The crown office must decide before midnight. It can receive a delegation chosen by the crowd itself, which would "
        "make the gathering a precedent every later petitioner will cite, or have the guard clear the square gently and "
        "promise written replies to every sheet. Either choice will be retold in every ward of the kingdom by morning, "
        "with the details improved at each telling.",
    ), (
        Option('Receive a delegation from the square.', (Stability(0.03), PP(-20))),
        Option('Clear the square and promise replies.', (PP(25), Stability(-0.02), WarSupport(0.01))),
    ), picture=0),
    EventDef('ward_returns', 'Four Provinces Report', (
        "The surveyors return from the four provinces with crates of ledgers. The capital port on the western coast holds "
        "most of the kingdom's people, its arms halls and civilian plants, its naval berth and one of its two supply nodes. "
        "Its wards complain that they pay most of the taxes and receive water only on alternate days each summer.",
        "The northern coastal plain reports tenant farmers paying rents fixed generations ago and drainage ditches nobody "
        "has cleared since. The southern plain around the logistics centre is the kingdom's crossroads, with the second "
        "supply node and the far end of the railway, and its traders want more of the freight money that passes through. "
        "The eastern hills, which touch both Monstrua and Valka, report the fewest people, the poorest schools and the "
        "longest stretch of frontier.",
        "Publishing the survey in full will start a quarrel among the provinces that no ministry can steer, because every "
        "figure will be read as an insult by somebody. Keeping it inside the ministries will shape the budget quietly while "
        "each province assumes the worst of the others. The government must choose before the newspapers obtain a copy of "
        "their own.",
    ), (
        Option('Publish every province figure.', (Stability(0.02), PP(-15))),
        Option('Keep the survey for the ministries.', (PP(30), Stability(-0.01))),
    ), picture=1),
    EventDef('works_census', 'Six Plants Counted', (
        "The census of the kingdom's works is the first in a generation. Inspectors visit the three civilian plants and the "
        "three arms halls, count every press and lathe, time every shift and read every maintenance log they can find. They "
        "also walk the edges of the industrial ground and confirm what managers have long said: there is no spare land left "
        "for a seventh plant.",
        "The findings are mixed. Some lines run well above their rated output because foremen have quietly rebuilt them over "
        "the years. Others stand idle for days while parts arrive by sea. Steel from the kingdom's own mines is good, oil is "
        "modest and rubber is scarce. The arms halls make rifles and trucks the army can use, though rarely as many as it "
        "orders.",
        "The ministers must decide how much of this to share with the owners, the unions and the press. Publishing the census "
        "will embarrass managers and give the unions arguments for years. Sharing it only with the owners keeps the peace in "
        "the halls and leaves the workers guessing. The plants will run the same tomorrow either way; the politics will not.",
    ), (
        Option('Publish the census.', (Research('industry', 0.5, 1), Stability(-0.01))),
        Option('Share it only with the owners.', (PP(30),)),
    ), picture=2),
    EventDef('quay_strike', 'The Quay Stops Work', (
        "Three days after the convoy register is announced, the stevedores on the capital quay stop work. They are not "
        "against the register itself. They object to the clause requiring them to report every cargo they handle, which they "
        "read, correctly, as the end of the small private trade that has topped up dock wages for decades.",
        "Ships wait at anchor off the coast and their owners telephone the palace hourly. Shipping agents warn that charters "
        "will move to other ports if the quay is not working by the end of the week. The communist organisers, who have "
        "members in every gang, insist that the strike belongs to the dockers alone; the loyalist papers insist it was "
        "planned in a back room.",
        "The port office can drop the reporting clause and let the register cover ships but not the men who unload them, or "
        "keep the clause and offer the gangs a wage rise to replace what they will lose. Either way, the dockers will have "
        "learned that the kingdom's trade stops when they stop, and they will not forget the lesson "
        "when the next quarrel with the port office comes round.",
    ), (
        Option('Drop the reporting clause.', (Stability(0.02), PP(-10))),
        Option('Keep the clause and raise dock wages.', (PP(-20), Research('logistics_tech', 0.5, 1))),
    ), picture=0),
    EventDef('muster_count', 'Muster Day for Four Battalions', (
        "Every soldier of the territorial service is called to report on the same morning. The battalions in the capital "
        "port fill their barracks squares by eight. The hill battalion arrives on foot from the eastern ridges, short of "
        "boots and long on complaints. The trucks, all five hundred and sixty of them on paper, are lined up and counted in "
        "the yards of the logistics centre.",
        "The tally taken at dusk is sobering. Both formations exist and both are understrength. Fewer than half of the trucks "
        "start on the first attempt. The rifles are sound but the reserve of ammunition would last a week of serious fighting "
        "at most. There is no artillery to count and no aircraft to inspect, which spares the general staff two separate "
        "embarrassments.",
        "The war ministry drafts two reports. One gives the true count and asks for money; it would shake loyalist confidence "
        "and hand the crown's critics an easy headline. The other repeats the figures printed every year since 1987 and asks "
        "for nothing. Ministers must decide which report goes to the press and which goes into the safe.",
    ), (
        Option('Publish the true count.', (Stability(-0.02), XP('army', 20))),
        Option('Repeat the printed figures.', (PP(20), WarSupport(0.02))),
    ), picture=2),
    EventDef('neighbour_notes', 'Notes from Two Capitals', (
        "Within a month of each other, envoys from Monstrua and Valka call at the crown office with notes that say much the "
        "same thing in very different tones. Each wants to know where Aquitoria stands on frontier patrols, on the exiles who "
        "cross the eastern hills and on the freight that passes through the logistics centre. Neither asks directly about the "
        "other neighbour; both clearly mean it.",
        "The Monstruan note is short and formal, written by a government whose movement faces no organised rival at home. "
        "The Valkan note is longer and friendlier, from a government whose own public is divided almost evenly between a "
        "nationalist camp and a non-aligned one. Aquitorian loyalists, democrats and communists each read the two notes and "
        "find exactly what they feared.",
        "The crown office must answer both before rumours answer for it. It can send identical replies promising good "
        "neighbourliness and nothing more, or answer each in its own register, warmly to Valka and correctly to Monstrua. The "
        "replies will be read in both capitals line by line, and kept on file for a long time by "
        "clerks who will quote them back whenever a frontier quarrel flares.",
    ), (
        Option('Send identical replies to both.', (Stability(0.02), PP(-5))),
        Option('Answer each in its own register.', (PP(25), WarSupport(0.01))),
    ), picture=1),
    EventDef('air_question', 'Should the Kingdom Fly?', (
        "The new air office presents its first paper to the ministers. Aquitoria has no air base, no combat aircraft and a "
        "handful of pilots trained abroad. Its research staff studied early fighter designs years ago and filed the reports. "
        "Freight companies already ask why air cargo for the kingdom must land somewhere else and travel the last stretch "
        "by truck.",
        "The paper sets out the costs plainly. A first runway would take farmland at the edge of the capital port. A radar set "
        "and a control tower would cost more than the hangars. Aircraft must be bought abroad, along with spares, fuel and "
        "instructors. The army notes that the same money would put every truck back on the road and buy a year of "
        "ammunition.",
        "The ministers must decide how the plan is presented. Announced as a matter of national pride, it will draw "
        "volunteers and applause and set expectations that a few aircraft cannot meet. Presented as a quiet transport "
        "project, it will draw little attention and few recruits. Either way the runway gets built; the question is what "
        "the kingdom expects of it.",
    ), (
        Option('Announce an air arm for the kingdom.', (WarSupport(0.03), PP(-10))),
        Option('Call it a transport project.', (PP(20), XP('air', 10))),
    ), picture=2),
    EventDef('belkan_war', 'The War Reaches the Freight Market', (
        "War breaks out around Belka on 25 March 1995. Aquitoria has no part in it and no frontier near it, but the war "
        "reaches the capital port within days through the freight market. Charter rates double, insurers add war clauses to "
        "routes they consider exposed, and buyers the port office has never heard of call asking for fuel, trucks and rifles.",
        "The arms halls receive more enquiries in a week than in the previous year. Loyalist newspapers argue that the kingdom "
        "should sell to whoever pays, since nobody will thank it for staying poor. Democrats and communists, for once in "
        "agreement, warn that crates with Aquitorian markings will be found on battlefields and remembered. Foreign embassies "
        "ask, politely and in nearly identical words, what the kingdom intends.",
        "The crown office must say something before the arms halls decide for it. A declaration of strict neutrality costs "
        "nothing today and may cost orders tomorrow. A statement that existing contracts will be honoured keeps every option "
        "open and satisfies nobody abroad. Whatever is said now will be quoted back to the kingdom for years, "
        "by friends and critics alike.",
    ), (
        Option('Declare strict neutrality.', (Stability(0.02), PP(10))),
        Option('Say only that contracts stand.', (PP(25), WarSupport(0.02))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Aquitorian response is gameplay', picture=0),
    EventDef('asteroid_quay', 'The Announcement Reaches the Quay', (
        "In December 1994 astronomers warned that the asteroid Ulysses might strike the Earth. In April 1996 the warning "
        "becomes an announcement: it will strike, and nations must prepare. Nobody can say where the fragments will fall. In "
        "Aquitoria the news arrives on the evening radio, and by morning the queues outside the grain merchants on the quay "
        "reach the harbour wall.",
        "Ministries produce plans overnight. Engineers want shelters beneath the capital port. Planners want evacuation "
        "routes into the eastern hills. The port office wants to know whether ships should stay at sea or come home. The "
        "treasury points out that any of these plans costs more than the kingdom spends on its army in a year, and that the "
        "army also has requests.",
        "Before any plan is approved, the government must decide how to speak to a frightened public. It can announce "
        "preparations openly and at once, accepting a rush on the markets, or urge calm while the ministries work, accepting "
        "that the public will hear rumours before it hears plans. The quay will judge the choice within a day, and the grain "
        "merchants will judge it within the hour.",
    ), (
        Option('Announce preparations at once.', (WarSupport(0.02), Stability(-0.02))),
        Option('Urge calm and work quietly.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Aquitorian preparations are gameplay',
        picture=0),
    EventDef('roche_night', 'A Long Night on the Radio', (
        "On 8 July 1999 the asteroid Ulysses passes through the Roche limit of the Earth. In Aquitoria nobody sleeps. "
        "Families sit beside radios in the dock wards and the hill villages, the port office logs every call from ships at "
        "sea and the soldiers guarding the depots at the logistics centre listen to the same bulletins as everyone else.",
        "Rumours move faster than facts. One report places fragments in the sea; another, an hour later, places them on "
        "another continent entirely. The port office separates what is known from what is feared and finds the line moving "
        "every few minutes. Ministers spend the night in the government offices above the quay, waiting for a telephone call that may never come, "
        "and sending clerks down to the harbour every hour for news the radio has not yet carried.",
        "By morning the kingdom is still standing and still frightened. Whatever has fallen, and wherever it fell, the "
        "consequences will reach Aquitoria through freight rates, refugees and prices for years. Ministers must choose "
        "between holding the depots, curfews and drills in place until the damage abroad is known, and releasing the "
        "provinces to work, trade and sleep normally again.",
    ), (
        Option('Hold the emergency measures.', (WarSupport(0.03), Stability(-0.01))),
        Option('Release the provinces to normal life.', (Stability(0.03), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no Aquitorian damage is claimed', picture=2),
    EventDef('usean_war', 'War in Usea, Prices on the Quay', (
        "Erusea's invasion of neutral San Salvacion in the summer of 2003 puts the railguns of Stonehenge in Erusean hands, "
        "and they are soon firing at aircraft. Usea is a long way from the capital port, but freight and fuel prices respond "
        "within days, and the convoy register shows a dozen Aquitorian ships on routes that touch Usean waters.",
        "Shipowners hold their vessels in port until the government tells them whom the kingdom will supply. The arms halls "
        "receive enquiries from buyers on both sides. The three political camps, whatever government now holds the seals, "
        "agree that no Aquitorian soldier should go to Usea. They agree on very little else, least of all on whether the "
        "kingdom should profit from the war.",
        "The government must give the shipowners an answer this week. Keeping every Aquitorian hull out of Usean waters is "
        "safe and expensive. Letting each owner decide for himself is profitable and dangerous. Later choices about whom to "
        "supply will follow from this first answer, and so will the rates the insurers charge. The shipowners have "
        "made clear that if the government says nothing, they will each make their own choice by the end of the month.",
    ), (
        Option('Keep every hull out of Usean waters.', (Stability(0.02), PP(-10))),
        Option('Let each owner decide.', (PP(25), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Aquitorian response is gameplay', picture=1),
)

# --- branches ------------------------------------------------------------------------------------
CROWN = Branch('crown', 'The Chamber Shut Since 1987', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('cr_locked_chamber', 'A Chamber Shut Since 1987',
          "Aquitoria last elected a chamber in November 1987, and the Office of the Crown has governed alone since the "
          "elections were suspended. Half the kingdom still answers to the crown, while democrats and communists each claim "
          "about a fifth. Admitting that the arrangement is temporary costs the palace its comfortable silence, but no reform "
          "can begin until someone says it aloud.",
          ('medal', 'assembly'), reward=(Idea('crown_office_rule'), Event('locked_chamber'))),
    Focus('cr_gate_petitions', 'Petitions at the Palace Gate',
          "Clerks of the crown office open the sacks of petitions that have piled up at the palace gate since the chamber "
          "closed: dock pay, rents on the northern plain, grazing rights in the eastern hills. Reading and answering them "
          "takes a season of staff time. The replies tell every camp what the crown already knows about its grievances, "
          "and what it intends to ignore.",
          ('document', 'medal'), after=('cr_locked_chamber',), reward=(PP(25), TimedIdea('petition_office', 365))),
    Focus('cr_three_camps', 'Rolls of the Three Camps',
          "Crown loyalists, democrats and communists have kept informal membership rolls since 1987, the way banned clubs "
          "always do. Letting each camp register openly, with offices and newspapers, shows the palace how strong its rivals "
          "really are. The registers end the polite fiction that only the crown has followers, and they hand the police a "
          "list nobody fully trusts.",
          ('ballot', 'document'), after=('cr_locked_chamber',), reward=(TimedIdea('open_registers', 730),)),
    Focus('cr_path_compact', 'A Compact of Crown and Chamber',
          "Moderate courtiers propose a written compact: the crown keeps its title, its seals and its veto over war, while a "
          "reopened chamber chooses the ministers who run the budget. Loyalists accept it as the price of quiet. Democrats "
          "call it half a reform and communists call it a costume change, yet the compact asks no camp to give up everything "
          "at once.",
          ('scales', 'medal'), after=('cr_gate_petitions', 'cr_three_camps'),
          exclusive=('cr_path_republic', 'cr_path_commune', 'cr_path_privy'),
          reward=(SwapIdea('crown_office_rule', 'compact_promise'),)),
    Focus('cr_path_republic', 'The Republican Petition',
          "Democratic clubs from the capital port and the northern plain collect signatures for a republic: an elected head "
          "of state, a written constitution and a crown retired to private life. The petition grows fastest among clerks, "
          "teachers and shipping agents. Loyalists treat it as treason in a polite hand, and the palace guard begins counting "
          "the signatures with obvious unease.",
          ('ballot', 'assembly'), after=('cr_gate_petitions', 'cr_three_camps'),
          exclusive=('cr_path_compact', 'cr_path_commune', 'cr_path_privy'),
          reward=(SwapIdea('crown_office_rule', 'republican_clubs'),)),
    Focus('cr_path_commune', 'Councils on the Docks',
          "Communist organisers argue that the port, the arms halls and the logistics centre already run on the labour of a "
          "few thousand workers who are never consulted. They propose councils on every dock and shop floor that would elect "
          "a common executive. The idea spreads through the night shifts, and owners on the quay start hiring private "
          "watchmen for their sheds.",
          ('assembly', 'tools'), after=('cr_gate_petitions', 'cr_three_camps'),
          exclusive=('cr_path_compact', 'cr_path_republic', 'cr_path_privy'),
          reward=(SwapIdea('crown_office_rule', 'dock_councils'),)),
    Focus('cr_path_privy', 'The Crown Keeps the Seals',
          "Hardline courtiers want no chamber at all. They propose that a privy council appointed by the crown hold every seal "
          "of government, issue decrees and settle the question of 1987 by declaring it closed. Loyalists in the hill province "
          "applaud. The democrats and communists, who together match the loyalists in number, are told that patience is now "
          "a civic duty.",
          ('medal', 'security'), after=('cr_gate_petitions', 'cr_three_camps'),
          exclusive=('cr_path_compact', 'cr_path_republic', 'cr_path_commune'),
          reward=(SwapIdea('crown_office_rule', 'privy_seals'),)),
    Focus('cr_compact_ministry', 'Seat the Compact Ministry',
          "The chamber reopens under the compact and elects a ministry answerable to it, with elections returning on a fixed "
          "calendar. The crown now signs the budget it once wrote. Loyalist deputies hold the largest bloc, but they must "
          "bargain with democrats and communists over every line, and ministers can fall on a single lost vote in a crowded "
          "hall.",
          ('assembly', 'scales'), after=('cr_path_compact',), cost=10,
          exclusive=('cr_republic_council', 'cr_commune_executive', 'cr_privy_council'),
          reward=(Regime('compact_ministry'), Flag('path_compact'))),
    Focus('cr_republic_council', 'Proclaim the Aquitorian Republic',
          "The crown withdraws from government, and a provisional council governs while the first presidential and chamber "
          "elections are prepared. The flag stays, the seals are recut and the palace becomes a public building. Loyalists, "
          "still half of the country, form the largest opposition any new republic could face, and they intend to win the "
          "very first ballot.",
          ('ballot', 'peace'), after=('cr_path_republic',), cost=10,
          exclusive=('cr_compact_ministry', 'cr_commune_executive', 'cr_privy_council'),
          reward=(Regime('republic_council'), Flag('path_republic'))),
    Focus('cr_commune_executive', 'Elect the Council Executive',
          "Dock, shop and depot councils send delegates to a common executive that takes the government seals, and the "
          "kingdom becomes the Aquitorian Commune. Wages and shift rotas are now political questions settled in open "
          "meetings. Shipowners and loyalist landholders in the hills refuse to recognise the executive, and the new "
          "government has little patience for their refusal.",
          ('assembly', 'industry'), after=('cr_path_commune',), cost=10,
          exclusive=('cr_compact_ministry', 'cr_republic_council', 'cr_privy_council'),
          reward=(Regime('commune_executive'), Flag('path_commune'))),
    Focus('cr_privy_council', 'The Privy Council Takes the Seals',
          "A council appointed by the crown takes every seal and rules by decree, with the chamber dissolved for good and the "
          "1987 rolls burned in the palace yard. Decisions arrive quickly and without debate. Order in the streets improves "
          "within months, while democrats and communists move their meetings into kitchens and back rooms where the police "
          "must work harder to follow them.",
          ('command', 'medal'), after=('cr_path_privy',), cost=10,
          exclusive=('cr_compact_ministry', 'cr_republic_council', 'cr_commune_executive'),
          reward=(Regime('privy_council'), Flag('path_privy'))),
    Focus('cr_compact_budget', 'The First Voted Budget',
          "For the first time since 1987 a budget passes the chamber after a public debate, with amendments from every bloc "
          "and a crown signature at the end. It is late, crowded with compromises and smaller than the treasury wanted. It is "
          "also the first budget any Aquitorian taxpayer can trace to a vote, which makes collecting it noticeably easier.",
          ('economy', 'scales'), after=('cr_compact_ministry',),
          reward=(SwapIdea('compact_promise', 'responsible_ministry'),)),
    Focus('cr_republic_charter', 'Write the Republican Charter',
          "The provisional council drafts a charter fixing the presidency, a single chamber, an independent court and the "
          "rights of the press. Loyalist deputies force a clause protecting crown property and pensions. Ratification by "
          "public vote passes with a margin narrow enough to worry everyone. The republic now rests on a text rather than on "
          "the mood of a crowd.",
          ('document', 'ballot'), after=('cr_republic_council',),
          reward=(SwapIdea('republican_clubs', 'republican_charter'),)),
    Focus('cr_commune_books', 'Councils Read the Company Books',
          "The executive orders every firm on the quay and in the arms halls to open its accounts to the workers councils. "
          "Managers who stay keep their posts but lose their secrets. Several shipowners reflag their vessels abroad "
          "overnight. The councils discover that the kingdom's firms were neither as poor nor as rich as either side had "
          "always claimed.",
          ('document', 'industry'), after=('cr_commune_executive',),
          reward=(SwapIdea('dock_councils', 'council_economy'),)),
    Focus('cr_privy_decrees', 'Decrees Under the Privy Seal',
          "The privy council replaces emergency orders with a permanent code of decrees covering the press, assembly, wages "
          "and the frontier. Officials finally know what the law is, because the council wrote all of it. Foreign buyers "
          "welcome the predictability. Aquitorians who disagree learn that the code has an answer for them too, and that it "
          "is rarely gentle.",
          ('document', 'security'), after=('cr_privy_council',),
          reward=(SwapIdea('privy_seals', 'privy_decrees'),)),
    Focus('cr_question_closed', 'The 1987 Question Is Closed',
          "Whatever answer the kingdom chose, the argument that began when the chamber was shut gives way to ordinary "
          "government. Ministries know whom they serve and petitioners know where to go. The losing camps have not vanished, "
          "and some will spend the next decade organising. For the first time since 1987, though, outsiders can predict who "
          "will sign tomorrow's orders.",
          ('peace', 'assembly'),
          after_any=('cr_compact_budget', 'cr_republic_charter', 'cr_commune_books', 'cr_privy_decrees'),
          reward=(Flag('crown_question_closed'), Stability(0.04))),
))

CITY = Branch('city', 'Four Provinces, One Crowded State', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('city_four_provinces', 'Survey the Four Provinces',
          "Aquitoria is a single crowded state of four provinces: the capital port on the western coast, a coastal plain "
          "running north toward Valka, the eastern hills where both frontiers meet and the southern plain around the logistics "
          "centre. Surveyors count houses, wells and tax rolls in each. Every province will learn exactly what the others "
          "receive, and few will like it.",
          ('document', 'civil'), reward=(Idea('ward_survey'), Event('ward_returns'))),
    Focus('city_port_water', 'New Water Mains for the Port',
          "The capital port grew faster than its pipes, and the older wards still share standpipes that run dry each summer. "
          "Laying new mains under the existing roads keeps the streets open while the works go on underground. It is "
          "unglamorous and costly. Fewer summers of queues at the standpipes will win the government more loyalty than any "
          "parade on the quay.",
          ('civil', 'tools'), after=('city_four_provinces',), reward=(Idea('port_water'),)),
    Focus('city_rent_board', 'Rents on the Northern Plain',
          "Tenant farmers on the coastal plain north of the capital pay rents fixed before anyone now living was born, to "
          "landholders who mostly live in the port. A rent board with powers to cap and review leases eases the worst cases. "
          "Landholders call it confiscation by arithmetic, and several of them sit uncomfortably close to the crown office.",
          ('scales', 'civil'), after=('city_four_provinces',), reward=(TimedIdea('rent_board', 730),)),
    Focus('city_hill_schools', 'Schools for the Eastern Hills',
          "Villages in the eastern hills send their children down to the plain for secondary school, and most of them never "
          "return. Building schools in the hill province keeps families together and gives the frontier a population that "
          "stays. Teachers must be paid a hardship allowance to go, and the allowance comes out of the port's own budget.",
          ('science', 'civil'), after=('city_four_provinces',), reward=(Idea('hill_schools'),)),
    Focus('city_councils', 'Elected Councils for Each Province',
          "Each of the four provinces receives an elected council with its own budget line and a say over local works. The "
          "southern plain and the eastern hills finally gain voices the port must hear. The capital loses the ability to move "
          "money freely between provinces, and every budget becomes a negotiation among four councils with long memories.",
          ('ballot', 'civil'), after_any=('city_port_water', 'city_rent_board', 'city_hill_schools'), cost=10,
          exclusive=('city_commissioner',),
          reward=(SwapIdea('ward_survey', 'elected_wards'), Flag('wards_elected'))),
    Focus('city_commissioner', 'A Commissioner for the Whole City',
          "The alternative places all four provinces under one commissioner appointed from the capital, with a single works "
          "office and a single rulebook. Decisions get faster and money moves to wherever the commissioner judges the need is "
          "greatest. Notables in the hills and on the plain lose influence they have held for generations, and they will not "
          "forget who took it.",
          ('command', 'civil'), after_any=('city_port_water', 'city_rent_board', 'city_hill_schools'), cost=10,
          exclusive=('city_councils',),
          reward=(SwapIdea('ward_survey', 'crown_commissioner'), Flag('wards_commissioned'))),
    Focus('city_council_budgets', 'Province Budgets in Public',
          "The provincial councils post their budgets on the doors of their halls and debate them in open session. The hill "
          "province wins a clinic, the southern plain a market hall, the northern plain a drainage scheme. Spending slows "
          "while every line is argued, but residents can see where their taxes went, and the arguments move off the streets.",
          ('scales', 'ballot'), after_any=('city_councils', 'city_commissioner'), requires=(HasFlag('wards_elected'),),
          reward=(Idea('open_budgets'),)),
    Focus('city_commission_plan', 'The Commissioner Ranks the Works',
          "The commissioner publishes a single works plan for the whole kingdom, ranking projects by traffic, population and "
          "cost rather than by which notable shouts loudest. Housing for dock workers rises first, then the drainage of the "
          "northern plain. It is efficient and it is resented. Nobody in the provinces was asked to approve the priorities "
          "they now live with.",
          ('document', 'command'), after_any=('city_councils', 'city_commissioner'), requires=(HasFlag('wards_commissioned'),),
          reward=(Idea('works_plan'),)),
    Focus('city_charter', 'A Charter for Four Provinces',
          "Whichever arrangement the kingdom chose, the four provinces sign a short charter fixing revenue shares, the order "
          "of public works and the right to appeal to a common court. The document is dry, and it ends a decade of petitions. "
          "Future governments can plan the state without first reopening the question of who pays for whom.",
          ('scales', 'assembly'), after_any=('city_council_budgets', 'city_commission_plan'),
          reward=(Flag('city_settled'), Stability(0.03))),
))

WORKS = Branch('works', 'Six Plants and No Room', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('wk_full_slots', 'Six Plants and No Spare Ground',
          "Aquitoria's three civilian plants and three arms halls fill every industrial site the crowded state can offer, and "
          "the roads around them are already as good as engineers can make them. Growth cannot come from new ground. A census "
          "of every plant, shift and machine shows where the existing works lose time, power and steel.",
          ('industry', 'document'), reward=(Idea('crowded_works'), Event('works_census'))),
    Focus('wk_ore_assay', 'Assay the Steel and Oil Seams',
          "The state mines steel ore, pumps a modest amount of oil and gathers a little rubber, yet nobody has surveyed the "
          "seams since the plants were built. Geologists map the deposits, the water tables and the haul routes. Their "
          "findings settle which pits deserve investment and which should quietly close before they swallow any more of the "
          "works budget.",
          ('telescope', 'tools'), after=('wk_full_slots',), reward=(Research('excavation_tech', 0.5, 1),)),
    Focus('wk_refinery', 'Run the Refinery at Full Draw',
          "The kingdom already knows how to refine fuel, yet its small refinery runs below capacity because crude leaves by "
          "tanker before anyone bids for it at home. Holding back enough oil to run the refinery at full draw keeps the truck "
          "pool and the trains moving on domestic fuel. Export earnings fall, and the tanker brokers complain at length.",
          ('industry', 'logistics'), after=('wk_full_slots',), reward=(Idea('home_fuel'),)),
    Focus('wk_crown_firms', 'Chartered Crown Firms',
          "One school wants each plant chartered as a crown firm: privately managed, protected from foreign competition and "
          "guaranteed the state's arms and steel orders in return for obeying the palace on prices. Managers like the "
          "certainty. Critics answer that a firm with a guaranteed buyer has no reason to improve, and the crown becomes its "
          "own captive customer.",
          ('medal', 'industry'), after_any=('wk_ore_assay', 'wk_refinery'), cost=10,
          exclusive=('wk_coops', 'wk_tender'),
          reward=(SwapIdea('crowded_works', 'crown_firms'), Flag('works_charter'))),
    Focus('wk_coops', 'Cooperatives on the Shop Floor',
          "Union leaders propose turning each plant into a cooperative owned by its workforce, with elected managers and "
          "profits shared by shift. Output may suffer while workers learn to run the books. Absenteeism and strikes, the "
          "plagues of the arms halls since the chamber closed, would become the cooperatives' own problem rather than the "
          "crown's.",
          ('assembly', 'tools'), after_any=('wk_ore_assay', 'wk_refinery'), cost=10,
          exclusive=('wk_crown_firms', 'wk_tender'),
          reward=(SwapIdea('crowded_works', 'shop_coops'), Flag('works_coop'))),
    Focus('wk_tender', 'Open the Works to Tender',
          "A third view invites foreign firms to bid for management contracts in the existing plants, bringing machine lines, "
          "methods and credit they cannot bring in new buildings. The works modernise fastest this way. Profits leave the "
          "kingdom with the managers, and every patriotic newspaper in the port prints the names of the foreign directors.",
          ('economy', 'diplomacy'), after_any=('wk_ore_assay', 'wk_refinery'), cost=10,
          exclusive=('wk_crown_firms', 'wk_coops'),
          reward=(SwapIdea('crowded_works', 'open_tender'), Flag('works_tender'))),
    Focus('wk_charter_orders', 'Ten-Year Orders for the Firms',
          "With the firms chartered, the crown signs ten-year orders for rifles, trucks and steel plate at fixed prices. The "
          "arms halls run steady shifts for the first time in years. Fixed prices look generous when steel is cheap and "
          "ruinous when it is dear, and every later government inherits the contracts along with their clauses.",
          ('document', 'industry'), after=('wk_crown_firms',), reward=(SwapIdea('crown_firms', 'charter_orders'),)),
    Focus('wk_shift_councils', 'Shift Councils Set the Rotas',
          "Each cooperative elects shift councils that set rotas, training and maintenance schedules. Workers who once hid "
          "broken machines now report them, because the repair bill is shared. Meetings eat into production hours and some "
          "councils vote themselves holidays the plants cannot afford. Within two years the cooperative halls run cleaner "
          "lines than they did under owners.",
          ('assembly', 'industry'), after=('wk_coops',), reward=(SwapIdea('shop_coops', 'shift_councils'),)),
    Focus('wk_foreign_lines', 'Foreign Lines in Old Halls',
          "The foreign managers rip out the oldest presses and install modern lines in the same halls, working through nights "
          "and holidays to finish. Output per worker rises sharply. Half the old hands are retrained and the rest retire early "
          "on settlements the treasury pays. The halls look nothing like they did, and neither do the wage packets.",
          ('tools', 'economy'), after=('wk_tender',), reward=(SwapIdea('open_tender', 'foreign_lines'),)),
    Focus('wk_retool', 'Retool Instead of Rebuild',
          "Whatever the ownership, the lesson of the decade is the same: a kingdom with no spare ground grows by retooling the "
          "plants it has. Engineers draw up a rolling programme that refits one hall each year without halting the others. "
          "It costs steady money and patience, and it keeps every slot in the state producing more than it did.",
          ('tools', 'industry'), after_any=('wk_charter_orders', 'wk_shift_councils', 'wk_foreign_lines'),
          reward=(Idea('retooled_halls'),)),
))

PORT = Branch('port', 'The Capital Port', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('port_convoy_register', 'Register the Sixty Convoys',
          "Sixty merchant convoys sail from the capital port under the Aquitorian flag, yet the kingdom owns no warships and "
          "keeps no record of where most of its merchant hulls are at any moment. A register of owners, cargoes and routes, "
          "reported by radio each day, gives the port office its first real picture of the trade that pays the kingdom's "
          "bills.",
          ('navy', 'document'), reward=(Idea('convoy_register'), Event('quay_strike'))),
    Focus('port_pilots', 'The Harbour Pilots Guild',
          "Every large ship entering the capital port takes on a local pilot, and the pilots have worked for decades as a "
          "loose fraternity with their own customs and fees. Chartering them as a guild with formal training, a published "
          "tariff and a duty roster makes the harbour safer at night. It also gives the guild leverage it will certainly use.",
          ('navy', 'training'), after=('port_convoy_register',), reward=(Idea('pilots_guild'), XP('navy', 10))),
    Focus('port_customs', 'One Customs House on the Quay',
          "Customs, harbour dues and the port police answer to three different ministries, and shipmasters pay small bribes to "
          "all three. Merging them into one customs house on the quay, with posted tariffs and printed receipts, ends most of "
          "the bribery and some of the revenue that quietly depended on it. Merchants notice the difference within a season.",
          ('scales', 'navy'), after=('port_convoy_register',), reward=(TimedIdea('posted_tariffs', 730),)),
    Focus('port_shore_radar', 'Radar Above the Northern Shore',
          "Merchant masters report unlit vessels loitering off the northern coastal plain at night, and the port office has "
          "no way to see them. A radar post above the shore covers the approaches to the capital and the plain. The equipment "
          "is imported and the crews take a year to train, but the coast is no longer watched only by fishermen.",
          ('radar', 'navy'), after=('port_pilots',), reward=(Build('radar_station', 1, 0),)),
    Focus('port_tugs', 'Tugs and a Salvage Crew',
          "When a freighter grounds at the harbour mouth the port must borrow tugs from abroad and wait days for them. A small "
          "salvage service with its own tugs, divers and pumps clears the channel within hours. The boats are second-hand and "
          "the divers are trained by the pilots guild, which is pleased to be needed and says so at every meeting.",
          ('tools', 'navy'), after=('port_pilots',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
    Focus('port_declare_free', 'Declare a Free Port',
          "One camp wants the capital port declared free: no duties on goods landed for transit, sheds open to any trader and "
          "the quay run for volume rather than revenue. Shipping agents from both neighbours would route cargo through "
          "Aquitoria. The treasury loses its tariff income and must hope that wharf fees and wages make up the difference.",
          ('economy', 'navy'), after_any=('port_pilots', 'port_customs'), cost=10, exclusive=('port_bonded_sheds',),
          reward=(Idea('free_port'), Flag('port_free'))),
    Focus('port_bonded_sheds', 'Bonded Crown Warehouses',
          "The other camp prefers bonded warehouses owned by the crown, where imported fuel, grain and steel are stored and "
          "released by licence. The state earns storage fees and keeps a reserve within reach of the palace. Traders complain "
          "about the paperwork and the queues. The reserve, however, means the kingdom never again runs dry because one "
          "tanker was late.",
          ('logistics', 'medal'), after_any=('port_pilots', 'port_customs'), cost=10, exclusive=('port_declare_free',),
          reward=(Idea('bonded_stores'), Flag('port_bonded'))),
    Focus('port_pays_its_way', 'A Port That Pays Its Way',
          "Whether free or bonded, the capital port now publishes its accounts each year: tonnage landed, fees collected, ships "
          "lost and delays logged. The figures show the port covering its own upkeep for the first time in memory. They also "
          "show how much of the kingdom's food and fuel arrives by sea, a fact that worries the army more than the merchants.",
          ('document', 'navy'), after_any=('port_declare_free', 'port_bonded_sheds'), reward=(Idea('port_accounts'),)),
))

ARMY = Branch('army', 'The Territorial Service', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('army_muster', 'Two Formations at Muster',
          "Aquitoria's army is a territorial service of two infantry formations, four battalions in all, armed from stores of "
          "eight hundred sets of infantry kit and several hundred trucks. It has no artillery, no engineers and no aircraft. "
          "Calling every soldier to muster on one day shows the general staff what the kingdom can actually field.",
          ('training', 'security'), reward=(Idea('territorial_service'), Event('muster_count'))),
    Focus('army_hill_drill', 'Mountain Drill in the Eastern Hills',
          "The eastern hill province touches both Monstrua and Valka, and it is the only high ground in the kingdom. The army "
          "already keeps mountain instructors on its books. Rotating every battalion through a season of hill drill teaches "
          "soldiers the ground they would actually defend. The cost is time away from the port garrisons and the city.",
          ('training', 'tools'), after=('army_muster',), reward=(Idea('hill_drill'),)),
    Focus('army_trucks', 'Keep the Trucks Running',
          "Five hundred and sixty trucks are the army's real strength, carrying both formations and their supplies across a "
          "state small enough to cross in a morning. Half of them sit in workshops waiting for parts. A maintenance programme "
          "with a parts depot at the logistics centre puts most of them back on the road, which matters more than any new "
          "weapon.",
          ('logistics', 'tools'), after=('army_muster',), reward=(Research('logistics_tech', 0.5, 1), XP('army', 10))),
    Focus('army_hill_line', 'Hold the Hill Line',
          "One doctrine digs the army into the eastern hills where the two frontiers meet, with prepared positions, stocked "
          "bunkers and battalions assigned to their own ridges. It turns a small force into a hard obstacle. It also leaves the "
          "capital port and the southern plain guarded by whatever the hills can spare, which in a crisis is very little.",
          ('security', 'bridge'), after_any=('army_hill_drill', 'army_trucks'), cost=10, exclusive=('army_wheeled_reserve',),
          reward=(Idea('hill_line'), Flag('doctrine_hills'))),
    Focus('army_wheeled_reserve', 'A Reserve on Wheels',
          "The other doctrine keeps the battalions together near the logistics centre and moves them by truck and train to "
          "wherever trouble appears. Distances inside the kingdom are short enough that a motorised reserve can reach any "
          "frontier crossing in hours. It demands constant drill and fuel, and it trusts that warning will come in time.",
          ('logistics', 'training'), after_any=('army_hill_drill', 'army_trucks'), cost=10, exclusive=('army_hill_line',),
          reward=(Idea('wheeled_reserve'), Flag('doctrine_reserve'))),
    Focus('army_bunkers', 'Magazines Cut into the Slopes',
          "The hill line needs stores that survive the first week of any crisis, so work crews borrowed from the plants cut "
          "magazines and water tanks into the slopes behind each battalion position. The digging takes two summers. "
          "Afterward a battalion cut off in the hills can hold out for a month without a single truck reaching it.",
          ('security', 'shelter'), after_any=('army_hill_line', 'army_wheeled_reserve'), requires=(HasFlag('doctrine_hills'),),
          reward=(SwapIdea('hill_line', 'stocked_hills'),)),
    Focus('army_troop_trains', 'Troop Trains to the Coast',
          "The reserve doctrine depends on the twenty-four trains the army keeps and the short railway between the logistics "
          "centre and the capital port. Timetables, loading ramps and a military platform at each end let a full battalion "
          "entrain in under an hour. Civilian freight waits whenever the army drills, and the railway office counts every "
          "delay.",
          ('rail', 'training'), after_any=('army_hill_line', 'army_wheeled_reserve'), requires=(HasFlag('doctrine_reserve'),),
          reward=(SwapIdea('wheeled_reserve', 'rail_reserve'), Research('train_tech', 0.5, 1))),
    Focus('army_staff_course', 'A Staff Course for Captains',
          "Captains of the territorial service learned staff work abroad or not at all, and orders from different battalions "
          "read like letters from different armies. A short staff course at the capital teaches one method for planning, "
          "supply and signals. The classes are small and the instructors are borrowed from the port office, but the orders "
          "begin to match.",
          ('command', 'document'), after_any=('army_bunkers', 'army_troop_trains'),
          reward=(XP('army', 25), Research('land_doctrine', 0.5, 1))),
))

NEIGHBOURS = Branch('neighbours', 'Between Monstrua and Valka', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('nb_two_frontiers', 'Two Frontiers Meet in the Hills',
          "Aquitoria borders Monstrua to the south and Valka to the north and east, and the two frontiers meet in its eastern "
          "hill province. Monstrua is governed by a nationalist movement with almost no rivals; Valka by a government "
          "whose own public is split down the middle. The kingdom must decide how it means to live between them.",
          ('diplomacy', 'security'), reward=(Idea('frontier_customs'), Event('neighbour_notes'))),
    Focus('nb_valka_freight', 'Through Freight from Valka',
          "Valkan trucks cross the northern coastal plain to reach the capital port, but every load is unpacked twice, once at "
          "each customs post. A single manifest and a shared inspection shed halve the delay. Valkan traders gain an easy road "
          "to the sea, and Monstruan newspapers notice which way the freight now runs and say so in print.",
          ('logistics', 'diplomacy'), after=('nb_two_frontiers',), reward=(TimedIdea('valka_freight', 730),)),
    Focus('nb_monstrua_road', 'The Market Road South',
          "Hill farmers from the Monstruan side bring produce to markets on the southern plain, whatever their governments "
          "say. Paving the market road and opening a customs post turns a smuggling trail into lawful trade. "
          "Monstruan officials welcome the revenue, and they station more uniformed men at their end of the post than trade "
          "alone would explain.",
          ('economy', 'peace'), after=('nb_two_frontiers',), reward=(TimedIdea('southern_market', 730),)),
    Focus('nb_lean_valka', 'Lean Toward Valka',
          "Valka is the neighbour whose freight already crosses the northern plain and whose government keeps a democratic "
          "banner. Closer ties mean shared customs, student places and a standing channel between the two cabinets. Monstrua "
          "will read every handshake as a choice against it. No alliance is signed and no faction joined; the lean is in trade "
          "and tone alone.",
          ('diplomacy', 'peace'), after_any=('nb_valka_freight', 'nb_monstrua_road'),
          exclusive=('nb_terms_monstrua', 'nb_equal_distance'), reward=(Idea('valka_ties'), Flag('lean_valka'))),
    Focus('nb_terms_monstrua', 'Terms with Monstrua',
          "Monstrua's movement governs without rivals and values respect above trade. Terms with Monstrua mean prompt answers "
          "to its complaints about exiles, closed doors for its opposition and quiet frontier talks. The southern hills calm "
          "down. Aquitorian democrats and communists, who have their own reasons to fear such a neighbour, protest loudly in "
          "the port.",
          ('diplomacy', 'security'), after_any=('nb_valka_freight', 'nb_monstrua_road'),
          exclusive=('nb_lean_valka', 'nb_equal_distance'), reward=(Idea('monstrua_terms'), Flag('lean_monstrua'))),
    Focus('nb_equal_distance', 'Equal Distance from Both',
          "The third answer treats both neighbours exactly alike: the same tariffs, the same visits, the same refusals. "
          "Aquitoria becomes the place where Valkan and Monstruan officials can meet on neutral ground. Equal distance wins no "
          "friends, and each neighbour suspects the kingdom of favouring the other, yet it never forces the crown to choose.",
          ('scales', 'diplomacy'), after_any=('nb_valka_freight', 'nb_monstrua_road'),
          exclusive=('nb_lean_valka', 'nb_terms_monstrua'), reward=(Idea('equal_distance'), Flag('lean_equal'))),
    Focus('nb_valka_colleges', 'Places in Valkan Colleges',
          "Closer ties with Valka open places in its colleges to Aquitorian students of engineering, medicine and law, paid "
          "for jointly by both treasuries. A generation of young professionals will return with Valkan habits and Valkan "
          "friends. Loyalists worry about the ideas they will bring home; Monstruan diplomats simply note the numbers and file "
          "them.",
          ('science', 'diplomacy'), after_any=('nb_lean_valka', 'nb_terms_monstrua', 'nb_equal_distance'),
          requires=(HasFlag('lean_valka'),), reward=(Idea('valka_students'),)),
    Focus('nb_quiet_south', 'A Quiet Southern Frontier',
          "Under the terms with Monstrua, patrols on both sides of the southern hills keep to agreed schedules and frontier "
          "incidents stop appearing in the newspapers. Trade through the logistics centre grows. The price is paid by "
          "Monstruan exiles in Aquitoria, who find themselves watched, and by Aquitorian opposition papers, which find "
          "themselves warned.",
          ('peace', 'security'), after_any=('nb_lean_valka', 'nb_terms_monstrua', 'nb_equal_distance'),
          requires=(HasFlag('lean_monstrua'),), reward=(SwapIdea('monstrua_terms', 'quiet_south'),)),
    Focus('nb_neutral_ground', 'Talks on Neutral Ground',
          "Equal distance makes Aquitoria the obvious venue when Valkan and Monstruan officials need to talk without being "
          "seen to visit each other. Delegations meet in a hall at the capital port, with Aquitorian clerks taking the "
          "minutes. The kingdom earns nothing directly. It gains a habit of being useful to both, which may matter in a "
          "harder decade.",
          ('peace', 'diplomacy'), after_any=('nb_lean_valka', 'nb_terms_monstrua', 'nb_equal_distance'),
          requires=(HasFlag('lean_equal'),), reward=(SwapIdea('equal_distance', 'neutral_venue'),)),
    Focus('nb_joint_commission', 'A Frontier Commission of Three',
          "Whatever the lean, the frontier itself needs tending: markers fall, streams shift and herders wander. A standing "
          "commission with members from all three governments walks the line each spring and settles small disputes before "
          "they reach a ministry. It claims nothing beyond the existing frontier and moves no marker, and its very dullness is "
          "its value.",
          ('document', 'peace'), after_any=('nb_valka_colleges', 'nb_quiet_south', 'nb_neutral_ground'),
          reward=(Idea('frontier_commission'),)),
))

AIR = Branch('air', 'An Air Arm from Nothing', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_no_airfield', 'A Kingdom Without an Airfield',
          "Aquitoria has no air base, no combat aircraft and only a few pilots, all of them trained abroad. Its research staff "
          "studied early fighter designs years ago and never bought one. Founding an air office that drafts a plan, a budget "
          "and a training scheme is the first step. Whether the kingdom should fly at all is still being argued.",
          ('air', 'document'), reward=(Idea('air_office'), Event('air_question'))),
    Focus('air_first_field', 'Lay Down the First Runway',
          "The air office chooses farmland at the edge of the capital port for the kingdom's first runway, with hangars, a "
          "fuel store and a short taxiway. The tenants who worked that land are compensated, though not generously. Once the "
          "runway opens, the kingdom can receive transport flights and train pilots at home instead of sending them away.",
          ('runway', 'tools'), after=('air_no_airfield',), reward=(Build('air_base', 2, 0),)),
    Focus('air_tower_radar', 'Tower and Radar at the Field',
          "A runway without a tower and a radar set is only a strip of concrete. Air traffic control and a search radar beside "
          "the field let the kingdom track flights crossing its small airspace and guide its own aircraft home in bad weather. "
          "The radar crew must be trained abroad, and the set itself costs more than the hangars did.",
          ('radar', 'runway'), after=('air_first_field',), reward=(Build('radar_station', 1, 0),)),
    Focus('air_fighter_flight', 'A Fighter Flight for the Capital',
          "One school wants a small flight of fighters on alert over the capital port and the arms halls, flown by the best "
          "pilots the kingdom can train. A dozen aircraft cannot win a war, but they can make an intruder think twice. The "
          "flight will eat most of the air budget, leaving nothing for transport or liaison work.",
          ('air', 'radar'), after=('air_first_field',), cost=10, exclusive=('air_liaison_flight',),
          reward=(Idea('capital_flight'),)),
    Focus('air_liaison_flight', 'Transport and Liaison Flight',
          "The other school wants transports and light liaison aircraft that carry officers, medicine and spare parts between "
          "the port, the logistics centre and the eastern hills. It fits the army's priority of sustainment better than "
          "fighters. The sky stays undefended, and the air office must explain to every minister why it bought aircraft that "
          "cannot shoot.",
          ('air', 'logistics'), after=('air_first_field',), cost=10, exclusive=('air_fighter_flight',),
          reward=(Idea('liaison_flight'),)),
    Focus('air_aggressors', 'Hire Aggressor Instructors',
          "Former top pilots of the Belkan Air Force are now hired by various countries to fly as aggressor squadrons. The "
          "kingdom's handful of pilots could learn more in a month against such instructors than in years of solo practice. "
          "The fees are high, and nobody in the air office asks too closely about the instructors' politics or their pasts.",
          ('medal', 'air'), after_any=('air_fighter_flight', 'air_liaison_flight'), requires=(After('1998.6.19'),),
          reward=(Idea('hired_aggressors'),)),
    Focus('air_dispersal', 'Dispersal Aprons and a Longer Strip',
          "A single runway can be closed by one burst tyre or one well-placed bomb. Lengthening it and adding dispersal aprons "
          "on the far side of the field lets heavier transports land and spreads the aircraft apart. The extension swallows "
          "another strip of farmland, and the tenants association files its second protest in five years.",
          ('runway', 'logistics'), after_any=('air_fighter_flight', 'air_liaison_flight'), reward=(Build('air_base', 1, 0), XP('air', 15))),
))

BELKA = Branch('belka', 'The Belkan War from the Quay', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_outbreak', 'Freight Rates Jump Overnight',
          "When war breaks out around Belka in March 1995, the first news reaches the capital port through the freight market "
          "rather than the radio: charter rates double, insurers add war clauses and buyers nobody has met ask for fuel and "
          "rifles. Aquitoria is nowhere near the fighting, yet its ledgers feel the war at once.",
          ('communications', 'navy'), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war'), TimedIdea('war_freight_rates', 365))),
    Focus('bw_cash_buyers', 'Cash Buyers at the Arms Halls',
          "The arms halls could sell every rifle and round they make to buyers who pay in cash and ask nothing about end use. "
          "Taking the orders fills three shifts and the treasury together. Every buyer's enemy will remember the markings on "
          "the crates, and some of those enemies may still be powerful when this war is long over.",
          ('industry', 'missile'), after=('bw_outbreak',), exclusive=('bw_closed_halls',),
          reward=(Idea('cash_orders'), Flag('war_sold'))),
    Focus('bw_closed_halls', 'No Rifles for Any Belligerent',
          "The opposite course embargoes arms to every party in the war while fuel and food continue to sail. The arms halls "
          "lose their busiest year in a decade, and their workers lose overtime they had already spent. Aquitorian ships, in "
          "exchange, are less likely to be stopped and searched by navies that remember who stayed out.",
          ('peace', 'scales'), after=('bw_outbreak',), exclusive=('bw_cash_buyers',),
          reward=(Idea('arms_closed'), Flag('war_refused'))),
    Focus('bw_fallout_watch', 'Radiation Meters on the Quay',
          "In this outcome nuclear devices have been used in the Belkan War, and every cargo from the war zone arrives under "
          "suspicion. The port office installs radiation meters at the quay, trains inspectors and publishes daily readings. "
          "Nothing alarming may ever be found. The readings calm the dock wards, and the meters stay in place long after the "
          "war.",
          ('radar', 'medical'), after=('bw_outbreak',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(Idea('radiation_watch'),)),
    Focus('bw_lumen', 'Peace News from Lumen',
          "A treaty signed in Lumen on 20 June 1995 ends the Belkan War. Freight rates sink back toward their old levels and "
          "insurers drop most war clauses. The arms halls must decide what to do with orders that will never be paid, and the "
          "port office must explain to shipowners why the boom ended faster than it began.",
          ('peace', 'document'), after_any=('bw_cash_buyers', 'bw_closed_halls'), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_freight_rates'), Stability(0.02))),
    Focus('bw_answer_crates', 'Answer for the Wartime Crates',
          "After the war, foreign ministries ask who supplied the weapons found on battlefields around Belka, and some crates "
          "carry Aquitorian markings. Licensing every future arms export, with buyer and end use published, turns an "
          "embarrassment into a rule. The halls keep their honest customers. The discreet ones, who paid best, take their "
          "business somewhere else.",
          ('document', 'industry'), after=('bw_lumen',), requires=(HasFlag('war_sold'),),
          reward=(SwapIdea('cash_orders', 'export_licences'),)),
    Focus('bw_credit_staying_out', 'Credit for Staying Out',
          "The embargo held for the whole war, and the shipping registries noticed. Aquitorian ships face fewer inspections, "
          "the port wins charters from owners who want a flag with no enemies and the crown gains a reputation it could not "
          "have bought. The arms halls are still short of work, but the quay is busier than ever.",
          ('peace', 'navy'), after=('bw_lumen',), requires=(HasFlag('war_refused'),),
          reward=(SwapIdea('arms_closed', 'clean_flag'),)),
    Focus('bw_belkan_agents', 'Purchasing Agents from Belka',
          "In this outcome Belka has won its war, and Belkan purchasing agents arrive at the capital port with lists of fuel, "
          "steel and trucks for rebuilding. They pay promptly. Accepting the orders fills the plants, and it also marks the "
          "kingdom as Belka's supplier just as Belka's beaten neighbours decide whose ships to welcome.",
          ('diplomacy', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_agents', 365),)),
    Focus('bw_surplus_tools', 'Surplus Machine Tools at Auction',
          "In this outcome Belka has lost its war, and surplus machine tools from Belkan plants that will never reopen come up "
          "for auction. Aquitoria's crowded halls cannot hold new plants, but they can hold better machines. Buying at auction "
          "refreshes the lines cheaply. Engineers must learn unfamiliar equipment from manuals in a language few of them read.",
          ('tools', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Research('industry', 0.5, 1), PP(10))),
))

ULYSSES = Branch('ulysses', 'The Asteroid and the Port', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_announced', 'Ulysses Will Strike',
          "The warning of December 1994 becomes an announcement in April 1996: the asteroid Ulysses will strike the Earth, and "
          "nobody can yet say where its fragments will fall. Aquitoria is one crowded state with a port, two plains and a "
          "range of hills. Every ministry produces a plan at once, and every plan needs money the treasury does not have.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),),
          reward=(Idea('asteroid_watch'), Event('asteroid_quay'))),
    Focus('uly_port_shelters', 'Shelters Beneath the Capital Port',
          "Engineers propose cutting shelters beneath the capital port and the arms halls, with sealed water tanks and stores "
          "for a fortnight. The port is where most Aquitorians live and work, so most of them could reach a shelter in minutes. "
          "The plan is slow, expensive and useless to anyone caught on the open plain when fragments fall.",
          ('shelter', 'navy'), after=('uly_announced',), cost=10, exclusive=('uly_hill_routes',),
          reward=(Idea('port_shelters'),)),
    Focus('uly_hill_routes', 'Evacuation Routes to the Hills',
          "Planners propose instead that the coast be emptied on warning: marked routes, trucks and trains to carry the "
          "population into the eastern hills, where camps and stores would wait. Evacuation is cheaper than concrete and "
          "protects people from the sea as well as the sky. It depends on warning arriving in time and on people obeying.",
          ('refugees', 'rail'), after=('uly_announced',), cost=10, exclusive=('uly_port_shelters',),
          reward=(Idea('hill_evacuation'),)),
    Focus('uly_centre_stores', 'Stores at the Logistics Centre',
          "Grain, medicine, fuel and water containers are gathered into depots at the logistics centre, the one place in the "
          "kingdom with good roads in every direction. Filling the depots drives up prices in the port markets just as people "
          "are already frightened. Emptying them, if the day comes, will be the hardest supply task the army ever faces.",
          ('logistics', 'shelter'), after_any=('uly_port_shelters', 'uly_hill_routes'), reward=(Idea('centre_stores'),)),
    Focus('uly_chamber_drills', 'Drills Voted by the Chamber',
          "The compact ministry puts every preparation to the chamber, publishes the plans and rehearses evacuations with "
          "deputies from all three camps taking part. The first drills are clumsy and the press mocks them. By the third, each "
          "ward knows its route and shelter, and the opposition finds it hard to attack plans it voted for.",
          ('ballot', 'shelter'), after=('uly_centre_stores',), requires=(HasFlag('path_compact'),),
          reward=(Idea('chamber_drills'),)),
    Focus('uly_republic_wardens', 'Volunteer Wardens of the Republic',
          "The republic asks citizens to prepare themselves: volunteer wardens in every street, first-aid courses in the "
          "schools and shelters dug by neighbourhood associations. Enthusiasm runs high in the port and lower in the loyalist "
          "hills. The result is uneven, energetic and cheap, and it gives the young republic something to do besides argue "
          "about its own origins.",
          ('civil', 'medical'), after=('uly_centre_stores',), requires=(HasFlag('path_republic'),),
          reward=(Idea('civic_wardens'),)),
    Focus('uly_commune_rations', 'Council Rations for Every Household',
          "The commune hands preparation to the councils, which ration grain, fuel and water containers by household and post "
          "the lists on every door. Hoarding becomes almost impossible and queues disappear. So does choice. Families who "
          "preferred their own arrangements discover that the councils count everything, including how often a neighbour "
          "complains.",
          ('assembly', 'logistics'), after=('uly_centre_stores',), requires=(HasFlag('path_commune'),),
          reward=(Idea('council_rations'),)),
    Focus('uly_privy_curfew', 'A Curfew Under the Privy Seal',
          "The privy council treats the asteroid as a question of order. A night curfew, licensed movement between provinces "
          "and soldiers posted at every depot keep the streets calm and the stores intact. Drills run punctually because "
          "attendance is compulsory. Aquitorians learn how quickly an emergency becomes a habit when the council finds it "
          "convenient.",
          ('security', 'command'), after=('uly_centre_stores',), requires=(HasFlag('path_privy'),),
          reward=(Idea('privy_curfew'),)),
    Focus('uly_province_depots', 'A Depot in Every Province',
          "The charter of four provinces fixes revenue shares, so the reserve can finally be spread fairly: a depot in each "
          "province, sized by population. The hill province receives a depot it never expected and the northern plain its "
          "first cold store. The logistics centre loses its monopoly on emergency supplies, which is what the other provinces "
          "wanted.",
          ('logistics', 'civil'), after=('uly_centre_stores',), requires=(HasFlag('city_settled'),),
          reward=(SwapIdea('centre_stores', 'province_depots'),)),
    Focus('uly_roche_night', 'Awake Through the Roche Night',
          "On 8 July 1999 the asteroid Ulysses passes through the Roche limit of the Earth. Aquitorians spend the night beside "
          "radios, in shelters or on the evacuation roads, depending on what their government prepared. The port office logs "
          "every report from ships at sea. Whatever falls and wherever it falls, the kingdom will feel it for years.",
          ('meteor', 'communications'), after=('uly_centre_stores',), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('uly_refugee_berths', 'Berths for Refugee Ships',
          "Erusea closes its doors to refugees on 21 April 2000, and the port office expects the consequences to arrive by "
          "sea. Crowded vessels may soon appear off the capital asking for berths, water and a place ashore. Accepting them "
          "fills the dock wards and draws on the emergency depots. Refusing them is cheap, and every shipmaster on the quay "
          "will remember it.",
          ('refugees', 'navy'), after=('uly_roche_night',), requires=(After('2000.4.21'),),
          reward=(Idea('refugee_berths'),)),
))

USEA = Branch('usea', 'The Usean War at a Distance', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('uw_railguns', 'Railguns Seized in San Salvacion',
          "Erusea's invasion of neutral San Salvacion in the summer of 2003 puts the railguns of Stonehenge in Erusean hands, "
          "and they are soon firing at aircraft. Usea lies far from Aquitoria, yet freight rates, insurance and fuel prices "
          "follow the war to the capital port within weeks. Shipowners refuse Usean charters until the government states its "
          "position.",
          ('missile', 'communications'), requires=(After('2003.6.1'),),
          reward=(Event('usean_war'), TimedIdea('usean_premium', 730))),
    Focus('uw_isaf_cargo', 'Cargo for the ISAF Depots',
          "The FCU establishes the ISAF in August 2003, and its quartermasters need fuel, trucks and steel plate delivered to "
          "distant depots. Contracts with the ISAF fill the arms halls and the convoys without committing a single Aquitorian "
          "soldier. Erusea will treat every such cargo as hostile, and ships bound for the ISAF sail knowing it.",
          ('diplomacy', 'logistics'), after=('uw_railguns',), requires=(After('2003.8.22'),),
          exclusive=('uw_closed_to_war', 'uw_paying_freight'), reward=(Idea('isaf_cargo'),)),
    Focus('uw_closed_to_war', 'No War Cargo Leaves the Quay',
          "The cautious answer closes the capital port to any cargo bound for either army, with inspectors on the quay to check "
          "manifests and seals. Shipowners lose the richest charters of the decade. The flag, however, stays clean in Usean "
          "waters, and crews sail without wondering which navy will decide they are a target.",
          ('peace', 'navy'), after=('uw_railguns',),
          exclusive=('uw_isaf_cargo', 'uw_paying_freight'), reward=(Idea('closed_quay'),)),
    Focus('uw_paying_freight', 'Freight for Any Paying Port',
          "A third answer sells to civilian buyers in any port that pays in advance and asks nothing about where the cargo goes "
          "after that. The arms halls and the convoys stay busy and the treasury fills. Both sides suspect the kingdom of "
          "feeding the other, and insurers charge for that suspicion on every single voyage.",
          ('economy', 'navy'), after=('uw_railguns',),
          exclusive=('uw_isaf_cargo', 'uw_closed_to_war'), reward=(Idea('paying_freight'),)),
    Focus('uw_crown_firm_orders', 'Crown Firms Take Wartime Orders',
          "The chartered crown firms, guaranteed their home orders, now bid for wartime contracts abroad as well. The arms "
          "halls add a third shift and recruit on the northern plain. Profits climb and so does the palace's share. When the "
          "war ends, the firms will expect the crown to find them buyers, as it always has.",
          ('industry', 'medal'), after=('uw_railguns',), requires=(HasFlag('works_charter'),),
          reward=(TimedIdea('firm_overtime', 730),)),
    Focus('uw_coop_vote', 'Cooperatives Vote on War Work',
          "Each cooperative hall must decide by vote whether to take wartime orders. Most accept, some refuse and two split "
          "into rival councils for a month. The halls that accept work longer hours for higher shares; the halls that refuse "
          "retool for civilian goods. The arguments are loud, public and settled without a single strike.",
          ('ballot', 'industry'), after=('uw_railguns',), requires=(HasFlag('works_coop'),),
          reward=(TimedIdea('coop_war_vote', 730),)),
    Focus('uw_tender_bids', 'Foreign Managers Chase Contracts',
          "The foreign managers running the tendered halls see the war as a market and bid for every contract their head "
          "offices can find. Output rises quickly on the modern lines. Decisions about whom to supply are now taken partly in "
          "foreign boardrooms, and Aquitorian ministers learn about some of the contracts from the newspapers.",
          ('economy', 'industry'), after=('uw_railguns',), requires=(HasFlag('works_tender'),),
          reward=(TimedIdea('tender_contracts', 730),)),
    Focus('uw_transit_sheds', 'Transit Sheds Overflow',
          "The free port fills with cargo routed around the war: goods that cannot travel by the old Usean lanes are landed, "
          "stored and reshipped through the capital. Wharf fees and wages soar and the sheds overflow onto the streets. Customs "
          "officers, with nothing to tax, simply count the ships and wonder how long it will last.",
          ('navy', 'logistics'), after=('uw_railguns',), requires=(HasFlag('port_free'),),
          reward=(TimedIdea('transit_surge', 365),)),
    Focus('uw_bonded_prices', 'The Bonded Reserve Holds Prices',
          "With freight and fuel prices climbing everywhere, the crown's bonded warehouses release stored fuel and grain at "
          "steady prices. Bread and bus fares in the capital barely move while prices elsewhere double. Traders who hoped to "
          "profit from the shortage are disappointed. The reserve empties faster than planned, and refilling it at wartime "
          "prices will hurt.",
          ('scales', 'logistics'), after=('uw_railguns',), requires=(HasFlag('port_bonded'),),
          reward=(TimedIdea('steady_prices', 365), Stability(0.02))),
    Focus('uw_stonehenge_quiet', 'Stonehenge Goes Quiet',
          "In this outcome the railgun complex has been destroyed, and the Usean sky is no longer closed to aircraft. Insurers "
          "trim their war clauses on the nearest routes and shipowners begin accepting Usean charters again. The kingdom drops "
          "its wartime surcharge, which pleases the merchants and removes a convenient source of revenue.",
          ('peace', 'missile'), after=('uw_railguns',), requires=(HasGlobal('ac_ucw_stonehenge_destroyed'),),
          reward=(RemoveIdea('usean_premium'), Stability(0.02))),
    Focus('uw_usean_rebuilding', 'Steel for Usean Rebuilding',
          "In this outcome the ISAF has won, and rebuilding begins across Usea. Ports, bridges and power lines need steel plate, "
          "trucks and fuel. Aquitorian firms bid beside much larger exporters and win a modest share. Payment stretches over "
          "years, and the governments placing the orders have little money of their own to spend.",
          ('rebuild', 'diplomacy'), after=('uw_railguns',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('usean_rebuilding', 365),)),
    Focus('uw_erusean_licence', 'Shipping Under Erusean Licence',
          "In this outcome Erusea has won, and Erusean harbour masters now decide which foreign ships may unload in Usea. Their "
          "trade offices offer Aquitorian shippers a licence in exchange for inspections and favourable prices. Accepting keeps "
          "the convoys sailing to Usean ports. Customers elsewhere, who remember the railguns, may wonder whose side the "
          "kingdom is on.",
          ('diplomacy', 'scales'), after=('uw_railguns',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Idea('erusean_licence'),)),
    Focus('uw_kingdom_ledger', 'A Ledger for 1991 to 2005',
          "With the Usean war winding down, the government's statisticians assemble a single printed ledger covering fifteen "
          "years: the constitution as it now stands, output from the six plants, earnings of the port, and the price of the "
          "asteroid years and two faraway wars. It makes no promises about what comes next, only about what has been.",
          ('document', 'medal'), after_any=('uw_isaf_cargo', 'uw_closed_to_war', 'uw_paying_freight'),
          requires=(HasFlag('crown_question_closed'), After('2005.1.1')),
          reward=(Stability(0.03), PP(40), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (CROWN, CITY, WORKS, PORT, ARMY, NEIGHBOURS, AIR, BELKA, ULYSSES, USEA)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('convoy_week', 'Hold a Convoy Week',
                'Every convoy reports on schedule and sails in company for a season of drills with the port office. '
                'Repeatable once a year.',
                35, (TimedIdea('convoy_week_drill', 90), XP('navy', 10)), requires=(Completed('port_convoy_register'),),
                cooldown=365),
    DecisionDef('hill_exercise', 'Exercise on the Eastern Ridges',
                'The territorial service manoeuvres for a fortnight on the eastern ridges. Repeatable every six months; it '
                'costs fuel and boots.',
                30, (XP('army', 15), TimedIdea('field_exercise', 60)), requires=(Completed('army_hill_drill'),), cooldown=180),
    DecisionDef('crown_audience', 'Open Audience at the Gate',
                'The crown hears petitioners in person for a day at the palace gate. Repeatable every six months while a '
                'crown still governs.',
                20, (Stability(0.01), TimedIdea('audience_day', 90)),
                requires=(Completed('cr_gate_petitions'), NotFlag('path_republic'), NotFlag('path_commune')), cooldown=180),
    DecisionDef('second_apron', 'Commission a Second Hangar Row',
                'Funds a second row of hangars and an apron at the crown airfield. A one-time charge on the air budget.',
                75, (Build('air_base', 1, 0),), requires=(Completed('air_first_field'),)),
    DecisionDef('southern_fair', 'Fair Days on the Southern Road',
                'The southern customs post hosts open fair days for traders from both sides. Repeatable once a year.',
                30, (TimedIdea('fair_days', 120), Stability(0.01)), requires=(Completed('nb_monstrua_road'),), cooldown=365),
    DecisionDef('refinery_turnaround', 'Strip Down the Refinery',
                'Shuts the refinery for a month of inspection and repair, and records what the engineers learn. Once only.',
                50, (Research('synth_resources', 0.5, 1),), requires=(Completed('wk_refinery'),)),
)
