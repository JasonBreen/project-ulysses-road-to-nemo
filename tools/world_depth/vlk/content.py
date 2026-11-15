"""Valka (VLK): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party with
elections suspended and no recorded last election, popularity split 50 to 48 between
fascism and neutrality), the unnamed National Administration office, the party-specific
country names, the five 1991 states with their neutral captions (Valka District A, C, D, E
and the Capital District), the Capital Centre victory point, the map (terrain, coast,
railways, weather, neighbours), the neighbouring Aquitorian, Malynean, Monstruan, Seteranoan
and Slavian trees, and the global flags the mod already sets. Official: ACES Chronicle rows
used only as date anchors for distant pressures, each cited by its exact key. Everything
else, including every Valkan choice, office, idea, building, decision and event, is
provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='VLK', name='Valka', root='world', package='vlk',
                  themes=('scales', 'rail', 'civil'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with election_frequency 48, elections_allowed = no and no '
           'last_election recorded; popularities fascism 50, neutrality 48, democratic 1, communism 1; stability and war '
           'support 0.5; three research slots; tech_mountaineers, tech_engineers, early_fighter, motorised_infantry and '
           'basic_train among the starting technologies. The starting leader is the unnamed National Administration office '
           '(VLK_ac_government_office, centrism), whose 1991 holder has not been established. The tree never names a holder; '
           'the fascism and neutrality popularities are called the nationalist camp and the non-aligned camp.',
           'mod/2985041246/history/countries/VLK - Valka.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Valkan Union (democratic, neutrality and communism), Valkan Reich (fascism), Kingdom of '
           'Valka (monarchism); adjective Valkan. The elected national-list path takes the existing fascism name from the '
           'localisation; its pledge keeps the ballot calendar and the frontiers, and no claim, core, war, annexation or '
           'faction follows from any path.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: five 1991 states, all state_category town (four shared slots each), captioned by the neutral regional '
           'labels. State 380, Valka Capital District (capital; 2 industrial complexes and 1 arms factory, one free slot; '
           'infrastructure 2; plains 307, 4257 and 8243, hills 1132, coastal forest 5140 and 8134; victory point Valka Capital '
           'Centre 307, value 20, with the only supply node; oil 2, rubber 2, steel 4). State 359, District A (no shared '
           'buildings; infrastructure 0; coastal forest 4250 and 5148; naval base 1 at 4250; no resources). State 382, '
           'District C (1 industrial complex and 1 arms factory; infrastructure 2; inland forest 369 and hills 8112 and 8221; '
           'oil 1, rubber 1, steel 3). State 397, District D (no shared buildings; infrastructure 0; mountain 720, hills 1637, '
           '4621 and 8257, forest 8487; coastal; no resources). State 414, District E (1 industrial complex and 1 arms '
           'factory; infrastructure 2; coastal forest and hills 143, 1066, 1955, 4267, 8553 and 8599; oil 1, rubber 1, steel '
           '3). No aluminium, chromium or tungsten anywhere. Level-2 railways 307-4250 (the northern spur) and '
           '307-369-8112-8257-4267 (the trunk). Strategic region 234 (the Capital District, A and C): January -22 to -7 '
           'degrees with snow and blizzards from November to February and heavy rain from June to August. Strategic region '
           '235 (D and E): mud in every month, heavy rain from January to May, hot dry summers and light snow possible in '
           'winter. Compass words come from province centroids. No other place is named.',
           'mod/2985041246/history/states/359-State_359.txt, 380, 382, 397 and 414; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/definition.csv; mod/2985041246/map/supply_nodes.txt; '
           'mod/2985041246/map/strategicregions/234-XXX.txt; mod/2985041246/map/strategicregions/235-XXX.txt'),
    Source('Mod provenance',
           'Land neighbours computed from map/provinces.bmp: MAY (state 341) along 321 and 7949 from District A and 3480 and '
           '7949 from District C, to the north and north-east; SET (356) along mountain 2455 from 8112 and 8257, to the east; '
           'SLA (133) along plains 11348 from 8257, to the east of District D; MST (422) along plains 1428 from 1637, to the '
           'south-west; AQU (435) along hills 5806 from 1637 and 4257 and plains 8331 from 4257 and 8243, to the south and '
           'south-west. Four of the five touch District D; District E has no land frontier. Sea provinces 10722 and 10147 off '
           'the Capital District, 10147 and 11143 off District A, 10014 (the bay shared with Monstrua and Aquitoria) and 10632 '
           'off District D, and 10014, 10541, 10559 and 10632 off District E. The Seteranoan level-2 railway ends at 2455, '
           'beside 8257 on the Valkan trunk; no railway crosses any Valkan frontier.',
           'mod/2985041246/map/provinces.bmp; mod/2985041246/map/definition.csv; mod/2985041246/map/railways.txt; '
           'mod/2985041246/history/states'),
    Source('Mod provenance',
           'Neighbours as inherited: Monstrua ruled by its fascism party at 90 percent with elections suspended since November '
           '1987; Aquitoria a monarchism government with its chamber unelected since 1987; Slavia ruled by its neutrality party '
           'with elections suspended since 1987; Malynea and Seterano with the same 50 to 48 split as Valka. Neighbour '
           'consistency: the Aquitorian tree has Valkan lorries crossing its northern coastal plain toward its capital port; '
           'the Monstruan tree has Colana touching Valka at a single plains crossing near the coast and may court the Valkan '
           'nationalist camp in print; the Slavian tree puts Valka west of a line of hills crossed by shepherds; the Seteranoan '
           'tree has Valka meeting the western end of its District B; the Malynean tree has forest running unbroken across its '
           'western frontier into Valka. This tree builds and governs only on the Valkan side, makes unilateral offers and '
           'never assumes a neighbour response.',
           'mod/2985041246/history/countries/MST - Monstrua.txt; AQU - Aquitoria.txt; SLA - Slavia.txt; MAY - Malynea.txt; '
           'SET - Seterano.txt; tools/world_depth/aqu/content.py; tools/world_depth/mst/content.py; '
           'tools/world_depth/sla/content.py; tools/world_depth/set/content.py; tools/world_depth/may/content.py'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small civil-defense service; 4 civilian and 3 military factories, '
           'no dockyard; two infantry formations of four battalions at the Capital Centre, with no engineer, artillery or '
           'support companies; combat air and combat navy deliberately absent; 60 convoys; no airfield; stocks of 800 infantry '
           'equipment, 560 motorized equipment and 24 trains; opening laws civilian_economy, export_focus and volunteer_only; '
           'research priority Physical Sustainment. Fiscal figures (GDP 100, debt ratio 0.3, collection 0.85, growth 3, '
           'inflation 2) and the civil_administration institution at capacity 40 are fictional calibration, not canon national '
           'accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/world_starts/sustainment.json; tools/economy_v2/profiles.json; tools/institutions/profiles.json; '
           'mod/2985041246/history/units/VLK_ws_land.txt; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official', 'Date anchor: the IAU announces that Ulysses will pass close to the Earth and may strike it. Gate of '
           'the asteroid branch; no Valkan role is claimed.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gate of the distant-wars branch; Valka takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Gate of the announcement focus; '
           'where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche night focus; no '
           'damage in Valka is claimed or denied.', '1999 / 07.08'),
    Source('Official', 'Date anchor: the FCU establishes the ISAF. Gate of the Usean freight focus, which also waits for the '
           'mod global flag ac_ucw_isaf_formed; no Valkan part in the war is claimed.', '2003 / 08.22'),
    Source('Official', 'Farbanti falls, Erusea surrenders and the Continental War ends. Background to the closing war focus, '
           'which waits for the mod outcome flag ac_ucw_outcome_isaf_victory instead of assuming this ending.',
           '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_ucw_isaf_formed and ac_ucw_outcome_isaf_victory (Usean Continental War '
           'script). Each reaction sits on a leaf, so no outcome blocks the rest of the tree.',
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Valkan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects. Shared buildings go to the '
           'Capital District (its one free slot), District A (two of four), District D (two of four) and District E (one of '
           'two); infrastructure stays at level 4 or below in every state.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the even split
    IdeaDef('split_country', 'The Country at Two Points',
            'Fifty for the nationalist camp, forty-eight for the non-aligned camp and one for the label the government sits under.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('scales', 'ballot')),
    IdeaDef('nonaligned_hearing', 'Offices Open to the Directors',
            'Ministry officials sit in the offices of district directors and works boards, taking notes.',
            {'stability_factor': 0.02, 'production_factory_efficiency_gain_factor': 0.02}, ('assembly', 'economy')),
    IdeaDef('nationalist_hearing', 'Halls Open to the Organisers',
            'Ministry officials attend nationalist meetings in rented halls and answer questions from the floor.',
            {'war_support_factor': 0.03, 'political_power_gain': -0.03}, ('assembly', 'security')),
    IdeaDef('ballot_called', 'Rolls Printed, Halls Open',
            'A national ballot has been called; every list may stand and every district counts its own votes.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'civil')),
    IdeaDef('ballot_drawer', 'The Ballot Left in the Drawer',
            'The vote stays suspended and the government governs against the wishes of the larger half.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('document', 'command')),
    IdeaDef('caretaker_accounts', 'Competence Instead of Campaigns',
            'The National Administration publishes its accounts every quarter in place of a mandate.',
            {'political_power_gain': 0.10, 'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.01},
            ('document', 'scales')),
    IdeaDef('list_pledge', 'The Pledge of the National List',
            'Frontiers where they are, a defensive service, judges left alone and the next ballot on its date.',
            {'stability_factor': 0.04, 'war_support_factor': 0.04}, ('document', 'peace')),
    IdeaDef('both_camps_cabinet', 'Ministers of Both Halves',
            'A cabinet that needs two thirds of the chamber, so it is built across the split.',
            {'stability_factor': 0.06, 'political_power_gain': -0.05}, ('assembly', 'diplomacy')),
    IdeaDef('posted_resolutions', 'Resolutions on Every Office Door',
            'The directors post each week what they decided, how they voted and why.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('document', 'civil')),
    IdeaDef('ballot_date_set', 'A Ballot Date in Print',
            'The National Administration has printed the day of the next national ballot and means to keep it.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('ballot', 'document')),
    IdeaDef('lot_clerks', 'Clerks Chosen by Lot',
            'Every count is run by clerks drawn by lot from both camps and paid by the courts.',
            {'stability_factor': 0.03, 'political_power_factor': 0.05}, ('scales', 'ballot')),
    # the trunk line
    IdeaDef('track_book', 'The Book of the Trunk Line',
            'Every section of the trunk and the spur measured, priced and listed for repair.',
            {'production_speed_infrastructure_factor': 0.05, 'supply_consumption_factor': -0.02}, ('rail', 'document')),
    IdeaDef('plough_wagons', 'Plough Wagons at the Yard',
            'Snow fences, plough wagons and a standing crew keep the northern line open through the blizzards.',
            {'attrition': -0.03, 'supply_consumption_factor': -0.02}, ('rail', 'shelter')),
    IdeaDef('dry_ballast', 'Stone and Ditches Under the Track',
            'Culverts and crushed stone keep the southern track firm through the wet months.',
            {'production_speed_infrastructure_factor': 0.05, 'army_speed_factor': 0.02}, ('rail', 'tools')),
    IdeaDef('steel_paths', 'Night Paths for Steel',
            'The best paths on the timetable belong to steel trains bound for the quay and the frontier.',
            {'production_factory_efficiency_gain_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'rail')),
    IdeaDef('service_paths', 'Paths Held for the Service',
            'A sealed timetable can carry both formations to any district within a day.',
            {'army_speed_factor': 0.04, 'planning_speed': 0.08}, ('rail', 'security')),
    IdeaDef('signal_wires', 'Wire Along the Whole Trunk',
            'Every signal box and halt is on one telephone line to the controllers at the capital.',
            {'planning_speed': 0.05, 'supply_consumption_factor': -0.02}, ('communications', 'rail')),
    # steel without alloys
    IdeaDef('ore_ledger', 'Three Empty Columns',
            'Ore, oil and rubber are listed; aluminium, chromium and tungsten are not, because there are none.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('steady_wells', 'Steadier Capital Wells',
            'New pumps and a gathering line steady the small output of the capital oil field.',
            {'production_speed_buildings_factor': 0.03, 'supply_consumption_factor': -0.02}, ('economy', 'tools')),
    IdeaDef('one_line_per_hall', 'One Line for Each Hall',
            'Each of the three arms halls builds one product on long runs from a shared tool store.',
            {'production_speed_arms_factory_factor': 0.05, 'production_factory_max_efficiency_factor': 0.02},
            ('industry', 'security')),
    IdeaDef('plate_exports', 'Valkan Plate Abroad',
            'Steel plate and bar sold to foreign yards for the currency that buys alloys.',
            {'production_speed_industrial_complex_factor': 0.08, 'political_power_gain': 0.05}, ('economy', 'navy')),
    IdeaDef('home_finishing', 'Finished in the Union',
            'Every bar finished at home into rails, pipe and tools, with softer edges for want of alloys.',
            {'production_speed_industrial_complex_factor': 0.05, 'consumer_goods_factor': -0.03,
             'production_factory_max_efficiency_factor': -0.02}, ('tools', 'industry')),
    IdeaDef('alloy_barter', 'Ore Traded for Alloys',
            'Long barter contracts swap ore and pig iron for the hard metals the works lack.',
            {'production_factory_max_efficiency_factor': 0.04, 'research_speed_factor': 0.02, 'political_power_gain': -0.05},
            ('diplomacy', 'industry')),
    IdeaDef('alloy_testing', 'Every Cargo Tested',
            'A laboratory at the capital assays every barter shipment before the works pays for it.',
            {'production_factory_max_efficiency_factor': 0.03, 'research_speed_factor': 0.02}, ('science', 'industry')),
    IdeaDef('ingot_reserve', 'A Season of Ingots in Stock',
            'Finished ingots and bar enough to keep the arms halls working for a season.',
            {'production_speed_arms_factory_factor': 0.05, 'industrial_capacity_factory': 0.03}, ('security', 'industry')),
    # the service
    IdeaDef('eight_battalions', 'A Service of Eight Battalions',
            'Two infantry formations at the Capital Centre, drilled for floods, snow, fire and order.',
            {'army_core_defence_factor': 0.03, 'stability_factor': 0.01}, ('security', 'training')),
    IdeaDef('flood_companies', 'Companies for the Floods',
            'Boats, pumps and sandbag stores at the southern halts, with companies trained to use them.',
            {'stability_factor': 0.02, 'attrition': -0.03}, ('civil', 'training')),
    IdeaDef('cold_drilled', 'Drilled for the Cold',
            'Both formations have wintered on the northern roads and come back able to live in a blizzard.',
            {'attrition': -0.05, 'army_org_factor': 0.03}, ('training', 'shelter')),
    IdeaDef('district_companies', 'Soldiers in Every District',
            'A company quartered near each district office and each southern frontier.',
            {'army_core_defence_factor': 0.08, 'stability_factor': 0.02}, ('security', 'civil')),
    IdeaDef('rail_reserve', 'The Reserve on Rails',
            'Both formations kept together at the capital and moved by the trunk line wherever they are needed.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.10, 'army_org_factor': 0.03}, ('rail', 'command')),
    IdeaDef('climbing_course', 'The Mountain Course',
            'A summer course on the District D mountain gives every battalion a few soldiers who can climb.',
            {'army_defence_factor': 0.03, 'experience_gain_army_factor': 0.05}, ('training', 'medal')),
    IdeaDef('pioneer_platoons', 'Pioneer Platoons',
            'A platoon in each battalion trained in bridging, demolition and pumping.',
            {'repair_speed_factor': 0.08, 'production_speed_infrastructure_factor': 0.05}, ('tools', 'training')),
    IdeaDef('district_volunteer_lists', 'Lists Kept by District Offices',
            'Former soldiers and willing civilians listed by trade and address in every district.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.03}, ('document', 'training')),
    IdeaDef('lorry_companies', 'A Lorry Company for Each Formation',
            'Crewed lorries, fitters and a fuel allowance take the battalions beyond the railheads.',
            {'army_speed_factor': 0.04, 'supply_consumption_factor': -0.02}, ('logistics', 'security')),
    IdeaDef('rescue_flight', 'The Rescue and Liaison Flight',
            'Light aircraft at the capital field carry doctors, mail and spotters to every district.',
            {'air_mission_efficiency': 0.05, 'stability_factor': 0.02}, ('air', 'medical')),
    IdeaDef('fighter_flight', 'The Early Fighter Flight',
            'A capital field and a pilot school for a small flight of early fighters.',
            {'air_superiority_efficiency': 0.06, 'experience_gain_air_factor': 0.08}, ('air', 'security')),
    IdeaDef('tented_hospitals', 'Hospitals in Canvas',
            'Two tented field hospitals packed at the capital with surgeons on a call list.',
            {'stability_factor': 0.03, 'attrition': -0.03}, ('medical', 'civil')),
    # three shores
    IdeaDef('sixty_convoys', 'Sixty Convoys and No Warship',
            'Every Valkan freighter registered by master, cargo and route; none of them armed.',
            {'naval_speed_factor': 0.02, 'consumer_goods_factor': -0.02}, ('navy', 'document')),
    IdeaDef('capital_lighters', 'Lighters on the Capital Shore',
            'Small lighters and a landing stage unload ships anchored off the harbourless capital coast.',
            {'consumer_goods_factor': -0.02, 'production_speed_buildings_factor': 0.03}, ('logistics', 'navy')),
    IdeaDef('south_landings', 'Landings on the Southern Bay',
            'Concrete landing stages, an ice house and a road to the halt for the southern fishing villages.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('fishing', 'navy')),
    IdeaDef('coast_watch', 'Cutters of the Coast Watch',
            'Armed cutters crewed by volunteers patrol three shores for smugglers, wrecks and poachers.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.04}, ('navy', 'security')),
    IdeaDef('freighter_credit', 'Credit for Valkan Freighters',
            'State credit for new hulls and training for merchant officers.',
            {'naval_speed_factor': 0.04, 'consumer_goods_factor': -0.04}, ('economy', 'navy')),
    IdeaDef('storm_warnings', 'Storm Warnings Twice a Day',
            'A coastal radio station reads weather from observers on all three shores.',
            {'naval_coordination': 0.03, 'stability_factor': 0.01}, ('communications', 'navy')),
    IdeaDef('headland_lights', 'Keepers on the Southern Headlands',
            'Three lit headlands on the District E coast, each with a resident keeper.',
            {'naval_speed_factor': 0.03, 'navy_org_factor': 0.02}, ('telescope', 'navy')),
    # five frontiers
    IdeaDef('five_frontiers_desk', 'An Office for Five Frontiers',
            'One frontier office keeps every crossing, post and track on the Valkan side of five lines.',
            {'political_power_gain': 0.05, 'stability_factor': 0.01}, ('diplomacy', 'document')),
    IdeaDef('southern_post', 'The Southern Plain Post',
            'A staffed post and weighbridge where carts and lorries cross toward Monstrua.',
            {'consumer_goods_factor': -0.02, 'army_core_defence_factor': 0.02}, ('economy', 'security')),
    IdeaDef('frontier_lorry_park', 'The Frontier Lorry Park',
            'A lorry park and one inspection shed at the Valkan end of the coastal plain road.',
            {'consumer_goods_factor': -0.03, 'supply_consumption_factor': -0.02}, ('logistics', 'diplomacy')),
    IdeaDef('hill_wardens', 'Wardens on the Eastern Hills',
            'Two wardens walk the shepherds tracks toward Slavia, counting flocks and finding the lost.',
            {'stability_factor': 0.02, 'army_core_defence_factor': 0.02}, ('peace', 'security')),
    IdeaDef('northern_firebreaks', 'Firebreaks in the Northern Forest',
            'Cut breaks, water tanks and a watch roster along the forest frontier with Malynea.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.03}, ('civil', 'peace')),
    IdeaDef('transit_toll', 'A Toll on Through Freight',
            'Foreign freight crossing the Union pays a transit toll in hard currency.',
            {'political_power_gain': 0.10, 'consumer_goods_factor': 0.02}, ('economy', 'gate')),
    IdeaDef('transit_at_cost', 'Transit at Published Cost',
            'One tariff for all five neighbours, set at what the handling costs.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('logistics', 'peace')),
    IdeaDef('trunk_reserved', 'The Trunk Kept for the Union',
            'Foreign freight moves on the trunk and the frontier roads only by permit.',
            {'army_speed_factor': 0.03, 'supply_consumption_factor': -0.03, 'consumer_goods_factor': 0.02},
            ('security', 'rail')),
    IdeaDef('toll_receipts', 'Toll Money for the Frontier Districts',
            'Half of every toll goes back to the districts where the posts stand.',
            {'political_power_gain': 0.10, 'stability_factor': 0.03}, ('scales', 'economy')),
    IdeaDef('depot_towns', 'Depots at the Crossings',
            'Warehouses, inns and repair shops grow up beside the busiest frontier posts.',
            {'consumer_goods_factor': -0.05, 'stability_factor': 0.03}, ('logistics', 'civil')),
    IdeaDef('permit_office', 'The Freight Permit Office',
            'One office at the capital issues every permit for foreign freight and checks it on arrival.',
            {'army_core_defence_factor': 0.05, 'supply_consumption_factor': -0.03, 'political_power_gain': 0.05},
            ('document', 'security')),
    IdeaDef('mountain_watch', 'Observers on the Mountain',
            'Two observers and a radio on the shoulder of the District D mountain.',
            {'air_detection': 0.05, 'army_core_defence_factor': 0.02}, ('telescope', 'security')),
    IdeaDef('neighbour_desk', 'Replies Within Ten Days',
            'Every letter from a neighbouring government is answered by one desk inside ten days.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('diplomacy', 'communications')),
    # Ulysses
    IdeaDef('impact_office', 'The Impact Office',
            'Engineers, doctors, railwaymen and officers planning for a strike nobody can yet place.',
            {'stability_factor': 0.02, 'research_speed_factor': 0.02}, ('meteor', 'telescope')),
    IdeaDef('rock_galleries', 'Galleries in the Mountain',
            'Shelter galleries driven into the solid rock of the District D mountain.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'tools')),
    IdeaDef('hall_cellars', 'Cellars Under the Public Halls',
            'Propped and pumped cellars beneath schools, offices and canteens in every town.',
            {'stability_factor': 0.04, 'air_defence_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('evacuation_timetable', 'The Sealed Evacuation Timetable',
            'A timetable that empties any threatened district by rail toward the others.',
            {'stability_factor': 0.03, 'planning_speed': 0.05}, ('rail', 'refugees')),
    IdeaDef('shelter_priority', 'Shelter Work Before All Else',
            'Steel props, pumps and cement go to the impact office first.',
            {'production_speed_buildings_factor': 0.08, 'consumer_goods_factor': 0.03}, ('shelter', 'industry')),
    IdeaDef('dark_year_depots', 'A Year in the District Depots',
            'Seed, fuel and medicine for a year in every district depot, rotated so nothing spoils.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('logistics', 'shelter')),
    IdeaDef('sunday_sirens', 'Sirens Tested on Sundays',
            'One national alarm, wired from the capital to every district office and works roof.',
            {'air_detection': 0.05, 'stability_factor': 0.01, 'static_anti_air_damage_factor': 0.05},
            ('communications', 'shelter')),
    IdeaDef('roche_watch', 'The Watch After the Roche Night',
            'Shelters manned and trains held ready while the fragments of Ulysses come down.',
            {'stability_factor': 0.03, 'war_support_factor': 0.03}, ('meteor', 'security')),
    IdeaDef('relief_trains', 'Two Relief Trains Made Up',
            'Tents, medicine, pumps and engineers on two trains kept ready at the capital.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.02}, ('rail', 'medical')),
    # distant wars
    IdeaDef('war_premiums', 'Premiums for a Distant War',
            'Insurers charge war rates on every Valkan hull, whatever its route.',
            {'consumer_goods_factor': 0.03, 'production_speed_buildings_factor': -0.03}, ('economy', 'navy')),
    IdeaDef('hull_pool', 'The State Hull Pool',
            'A state pool carries part of the war risk on Valkan freighters.',
            {'consumer_goods_factor': -0.02, 'naval_speed_factor': 0.03, 'political_power_gain': -0.05}, ('navy', 'scales')),
    IdeaDef('owners_risk', 'Owners Carry the Risk',
            'Shipowners price the war risk themselves and pass it on to every cargo.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': 0.02}, ('document', 'navy')),
    IdeaDef('peace_buyers', 'Steel for Buyers at Peace',
            'No Valkan plate or bar is sold to any party at war.',
            {'stability_factor': 0.04, 'industrial_capacity_factory': -0.02}, ('peace', 'scales')),
    IdeaDef('any_buyer', 'Orders from Every Buyer',
            'Valkan works fill any order that is paid for, whoever places it.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('economy', 'industry')),
    IdeaDef('treaty_trade', 'Trade After the Treaty',
            'Premiums ease and foreign buyers return once the Belkan War is over.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('peace', 'economy')),
    IdeaDef('winter_fuel_stock', 'Winter Fuel in the Tanks',
            'Fuel bought in the cheap months and stored before the northern winter closes in.',
            {'supply_consumption_factor': -0.04, 'war_support_factor': 0.02}, ('logistics', 'security')),
    IdeaDef('usean_rates', 'Freight at Usean War Rates',
            'Rerouted shipping and dearer insurance while war is fought on another continent.',
            {'consumer_goods_factor': 0.02, 'industrial_capacity_factory': 0.03}, ('logistics', 'economy')),
    IdeaDef('rebuilding_orders', 'Rails Sold for Reconstruction',
            'Steel and rails ordered for reconstruction after the Continental War.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': 0.02}, ('rebuild', 'economy')),
    # the turn of the century
    IdeaDef('decade_audit', 'The Decade Audit',
            'A panel from both camps has counted what ten years built against what was promised.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('scales', 'document')),
    IdeaDef('list_second_term', 'The List Seeks a Second Term',
            'The national list has gone back to the voters on the date it promised.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03}, ('ballot', 'security')),
    IdeaDef('rule_renewed', 'The Two-Thirds Rule Renewed',
            'The chamber has voted to keep the rule that forces cabinets across the split.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('assembly', 'scales')),
    IdeaDef('director_rotation', 'Directors Serve Five Years',
            'No director sits on the council for more than five years at a time.',
            {'political_power_gain': 0.10, 'research_speed_factor': 0.02}, ('command', 'document')),
    IdeaDef('date_kept', 'The Promised Ballot Held',
            'The National Administration held the ballot on the day it printed.',
            {'stability_factor': 0.05, 'political_power_gain': -0.03}, ('ballot', 'civil')),
    IdeaDef('college_places', 'Engineers from the Capital Colleges',
            'More engineering places at the capital colleges, with bursaries for every district.',
            {'research_speed_factor': 0.04}, ('science', 'training')),
    IdeaDef('second_tally', 'A Second Count Published',
            'A second national count of party sympathy, run by the clerks of both camps.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('ballot', 'scales')),
    # decision ideas
    IdeaDef('spur_cleared', 'The Spur Ploughed Clear',
            'Plough wagons have cleared the northern spur and the first section of the trunk after a blizzard.',
            {'supply_consumption_factor': -0.04, 'army_speed_factor': 0.03}, ('rail', 'shelter')),
    IdeaDef('track_drained', 'Southern Track Drained',
            'Drain gangs have cleared the culverts under the southern section.',
            {'supply_consumption_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'tools')),
    IdeaDef('fire_roster', 'The Firebreak Roster Manned',
            'Crews and water tanks stand at the northern firebreaks through a dry spell.',
            {'stability_factor': 0.02}, ('civil', 'shelter')),
    IdeaDef('plate_season', 'A Season of Plate Sold',
            'A season of plate auctioned abroad keeps the works busy and the treasury paid.',
            {'industrial_capacity_factory': 0.04, 'political_power_gain': 0.05}, ('economy', 'industry')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('national_list', 'Cabinet of the National List',
           'A cabinet named by the nationalist list after it wins a national ballot, governing as an elected government bound '
           'to the election calendar and to a chamber in which the non-aligned camp holds nearly half the seats. Provisional '
           'gameplay office with no named holder.',
           'fascism', 'ultranationalism', elections=True),
    Office('union_assembly', 'Cross-Camp Cabinet of the Union Assembly',
           'A cabinet that takes office only with two thirds of the elected chamber behind it, so its ministers come from '
           'both camps and its chair from the centre. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('directors_council', 'Council of the Union Directors',
           'A council of district, works, cooperative and bank directors governing by published weekly resolution with the '
           'ballot suspended and no party seats. Provisional gameplay office with no named holder.',
           'neutrality', 'conservatism_na'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('even_split', 'The Tally in a Sealed Envelope', (
        "The tally reaches the Administration in a sealed envelope from the statistics office at the Capital Centre, and the "
        "ministers read it twice to be sure. Out of every hundred Valkans asked, fifty lean toward the nationalist camp and "
        "forty-eight toward the non-aligned camp, which wants no party at all in charge. One supports the democratic label "
        "under which the government sits, and one the communists.",
        "The figures surprise nobody who has attended a public meeting in the last year, but seeing them printed changes "
        "their weight. The nationalists can now say that they are the larger half. The non-aligned camp can reply that the "
        "larger half is larger by two points and no more. The Administration can say nothing about its own support that "
        "would not sound like a joke at its own expense.",
        "What the ministers decide this morning is not who will govern, but who will know the numbers first. Released to "
        "the newspapers, the tally will start an argument across all five districts that the government cannot steer. Kept "
        "inside the building, it will leak within the month, and the government will then have to explain why it hid what "
        "everyone had already guessed.",
    ), (
        Option('Release the tally to every newspaper.', (Stability(-0.01), PP(-10), Event('camp_delegations', 20))),
        Option('Keep it inside the Administration.', (PP(25), Event('camp_delegations', 40))),
    ), picture=0),
    EventDef('camp_delegations', 'Two Delegations on One Staircase', (
        "Within weeks of the tally both camps send delegations to the Administration, and by an accident of scheduling they "
        "arrive on the same morning. The nationalist delegation brings district organisers, a petition thick with "
        "signatures and a demand for a ballot within the year. The non-aligned delegation brings works directors, "
        "cooperative chairs and a typed request that nothing be decided in haste.",
        "The two groups wait on the same staircase outside the cabinet room for most of an hour. Nobody shouts. Several of "
        "them know each other from the same towns, the same works and in a few cases the same families. A press photographer "
        "catches them standing two steps apart, and by evening the picture is on the front page of every paper in the Union.",
        "Ministers must decide how to receive them. Seeing both together would tell the country that the government stands "
        "between the camps rather than with either. Seeing them separately would let each speak freely, and invite each to "
        "suspect what was said to the other. Whatever the cabinet chooses, both delegations will describe the meeting to "
        "their own supporters before the cabinet secretary has typed the minutes.",
    ), (
        Option('Receive both delegations together.', (Stability(0.02), PP(-10))),
        Option('Hear each delegation alone.', (PP(20), WarSupport(0.01))),
    ), picture=2),
    EventDef('track_report', 'The Engineers Come Back from the Line', (
        "The railway engineers return from the trunk line with notebooks full of measurements and a summary that fits on one "
        "page. The northern section, from the Capital Centre through District C, is sound but loses whole days each winter "
        "to snow. The southern section, through the hills of District D to the railhead in District E, is sinking in places "
        "where water stands under the ballast for most of the year.",
        "The spur to District A is the worst of all. It was laid quickly through forest, it has no graded road beside it, "
        "and its last stretch stops short of the quay, so every load is carried the final distance by hand cart. The "
        "engineers also note what everyone at the yard already knows: both lines begin at the same crowded junction at the "
        "Capital Centre, and every fault anywhere in the Union ends up there.",
        "The report prices each repair and leaves the order of work to the ministers. Spending first in the north keeps the "
        "capital and the port moving through the winter. Spending first in the south saves the line where it is failing "
        "fastest. Either way, the engineers warn, the Union has one railway, and any year spent repairing one end is a year "
        "the other end waits.",
    ), (
        Option('Begin with the northern winter.', (Research('train_tech', 0.5, 1), Stability(0.01))),
        Option('Begin with the southern mud.', (Research('construction_tech', 0.5, 1), PP(10))),
    ), picture=1),
    EventDef('alloy_gap', 'The Missing Columns', (
        "The ministry of works prints its resource list with a column for each metal and fuel the works use, and three of "
        "those columns are empty from top to bottom. The Union has iron ore in three districts, a little oil and rubber in the "
        "same three, and no aluminium, chromium or tungsten anywhere. Every hard tool edge, light engine part and alloy "
        "spring in the country has come from abroad.",
        "Works managers have lived with this for years by buying small lots when prices allow and making do when they do "
        "not. The arms halls use softer steel than they would like and replace their cutting tools twice as often as foreign "
        "plants. The export traders point out that Valkan ore and plate sell well, and that the money could buy alloys if "
        "anybody planned for it instead of hoping.",
        "Three answers circulate before the list has even been distributed: sell the steel abroad for currency, finish all of "
        "it at home and accept softer tools, or trade ore directly for alloys under barter. Each has advocates in the "
        "ministry and in both political camps. First, the ministers must decide whether the works managers see the list "
        "now, or only once a policy has been chosen for them.",
    ), (
        Option('Send the list to every works manager.', (Research('industry', 0.5, 1), PP(-10))),
        Option('Hold it until a policy is ready.', (PP(25), Stability(-0.01))),
    ), picture=1),
    EventDef('service_review', 'Eight Battalions on the Square', (
        "The inspection of the service ends with a parade on the square at the Capital Centre, and the parade is short. Two "
        "formations of four infantry battalions each march past the reviewing stand with rifles, lorries and field "
        "kitchens, and nothing else. There are no guns, no engineers and no aircraft overhead, because the Union owns none "
        "of those things and never has.",
        "The inspectors' report is kinder than the parade suggests. The battalions are well drilled for the work they "
        "actually do: filling sandbags in the southern spring, digging out snowbound trains in the northern winter, "
        "searching forests for lost walkers and keeping order at the occasional riot. The soldiers are volunteers, most of "
        "them from the districts they serve, and their morale is good.",
        "The difficulty is that the report has two kinds of reader. The nationalist camp reads it as proof that the Union "
        "cannot defend itself and asks for a larger service. The non-aligned camp reads it as proof that the service is "
        "exactly the right size for a country that intends no wars. The Administration must decide which of those readings "
        "it will repeat in public.",
    ), (
        Option('Praise the service for what it does.', (Stability(0.02), XP('army', 10))),
        Option('Admit what it cannot do.', (WarSupport(0.03), PP(-10))),
    ), picture=2),
    EventDef('north_harbour', 'Freight Without a Fleet', (
        "The new register of hulls is the first complete list the Union has ever kept of the ships that sail under its "
        "flag. Sixty convoys of freighters carry ore, plate and timber out and fuel and machine tools home. Not one of them "
        "is armed, and the Union owns no warship of any kind. Its single naval base is a quay in a forest inlet in District "
        "A, at the end of the northern spur.",
        "The register shows how the shipping actually moves. Steel from the capital goes north by rail to the quay. Much of "
        "the road freight from the Capital District crosses the frontier toward an Aquitorian port, because the capital's "
        "own shore has no harbour, only an anchorage and a beach where small boats land. The southern coasts of District D "
        "and District E have fishing beaches and nothing that can berth a freighter.",
        "Shipowners dislike having their routes and cargoes written down, and some suspect a new tax. The harbour master in "
        "District A wants the list made public so that foreign buyers know Valkan ships exist. The ministers must decide "
        "whether the register is a commercial notice or an internal file, knowing that foreign insurers will ask to see it "
        "whichever they choose.",
    ), (
        Option('Publish the register as a notice to buyers.', (Research('naval_equipment', 0.5, 1), PP(-5))),
        Option('Keep it as an internal file.', (PP(20), XP('navy', 10))),
    ), picture=1),
    EventDef('hinge_report', 'Four Neighbours Around One District', (
        "The frontier office lays its survey on the cabinet table as a single sheet with five coloured lines. Malynea runs "
        "along the northern forest. Seterano meets the Union across the eastern mountain, and Slavia across the hills beside "
        "it. Monstrua and Aquitoria lie to the south-west, one beyond a plains crossing and the other beyond a coastal plain "
        "and a line of hills. Four of the five lines touch District D.",
        "The office has added a column the ministers did not ask for: how each neighbour is governed. Monstrua is run by a "
        "movement that polls nine voters in ten. Aquitoria is a crown government whose chamber has not been elected since "
        "1987, and Slavia an administration whose ballot has been suspended since the same year. Malynea and Seterano show "
        "the same near-even split between nationalist and non-aligned voters as the Union itself.",
        "No file records a quarrel over any of these lines, and nothing on the sheet is disputed. What the survey does show "
        "is that every current in Valkan politics has a neighbour that looks like it, and that each camp will want frontier "
        "policy to lean toward its own likeness. The ministers must decide whether to say that aloud or let the camps work "
        "it out for themselves.",
    ), (
        Option('Say plainly that policy will not follow party.', (Stability(0.02), PP(-10))),
        Option('Let each camp draw its own lessons.', (PP(20), WarSupport(0.01))),
    ), picture=0),
    EventDef('sky_notice', 'The Impact Office Meets', (
        "The bulletin arrives on the late radio of 10 December 1994. The International Astronomical Union has calculated "
        "that Ulysses, a body few people in the Union had heard of a month before, will come close to the planet, and it "
        "will not rule out a hit. Before dawn the Administration has an impact office working from two borrowed rooms at "
        "the Capital Centre: engineers, doctors, railwaymen and two officers lent by the service.",
        "The first meeting establishes how little the office knows. Nobody can say where fragments might fall, when, or how "
        "many. The Union's two climates complicate every plan: the north is frozen for months and the south is wet underfoot "
        "all year. Its one mountain is solid rock in District D. Its one railway would have to carry everything and "
        "everyone, and it already struggles in snow and in mud.",
        "Before any plan is drafted, the office must decide what to tell the public. Sharing every uncertainty would be "
        "honest, and would frighten many people who can do nothing with the knowledge. Saying little until there is a plan "
        "would keep the districts calm and risk the impression that the government is hiding something. The radio stations "
        "are already asking for a statement.",
    ), (
        Option('Share everything the office knows.', (Stability(-0.02), WarSupport(0.02), Research('construction_tech', 0.5, 1))),
        Option('Speak once there is a plan.', (Stability(0.02), PP(-5))),
    ), citation='date anchor only, ACES Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; the Valkan response is gameplay',
        picture=2),
    EventDef('freight_war', 'Premiums on a Peaceful Lane', (
        "In late March 1995 war breaks out around Belka, a long way from any Valkan shore. Within days the marine insurers "
        "who cover Valkan freighters raise their premiums on every voyage, whether or not the route passes near the "
        "fighting. Shipowners in District A forward the new rates to the ministry with a short note asking what the "
        "government means to do about them.",
        "The effects spread quickly. Foreign buyers of Valkan plate ask for longer delivery times. Imported fuel costs more "
        "to land, which the trunk line, the works and the two formations all feel within the month. Some buyers abroad ask "
        "quietly whether the Union would sell steel to parties at war, and at what price. Newspapers in both camps argue "
        "about whether a small country can stay out of a war's economy as easily as its battles.",
        "The government has no say over the war and little over the insurers. What it can decide is whether the state "
        "carries part of the new risk, and what kind of customer the Union will sell to while the fighting lasts. Before "
        "either, ministers must settle how to speak about a war that has nothing to do with Valka and is already in every "
        "price.",
    ), (
        Option('Promise help with the premiums.', (Stability(0.02), PP(-15))),
        Option('Tell owners to price the risk themselves.', (PP(20), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Valkan response is gameplay',
        picture=1),
    EventDef('decade_audit', 'What Ten Years Built', (
        "The audit panel, drawn equally from both camps with a judge in the chair, publishes its findings on the state of the "
        "Union after a decade. Its members walked the trunk line, the works, the shelters, the frontier posts and the "
        "northern quay, and counted what was built against what was promised. They disagree about almost everything except "
        "the arithmetic, which they sign together.",
        "The findings please nobody completely. The line runs better than it did, but District E still waits longest for "
        "every train. The works make more, still without alloys of their own. The service is better trained and still very "
        "small. The political order, whichever it is, has lasted, yet the split between the camps is almost as even as it "
        "was on the morning the first tally was printed.",
        "The government has two ways to respond. Adopting the findings whole means announcing a programme for the next ten "
        "years and being judged against every line of it. Thanking the panel and passing its recommendations to a standing "
        "committee is quieter, and the committee rooms of the Union are already full of such recommendations. The panel "
        "members have let it be known that they will talk to the newspapers whichever course is chosen.",
    ), (
        Option('Accept the findings in full.', (Stability(0.03), PP(-20))),
        Option('Send them to committee.', (PP(30), Stability(-0.02))),
    ), picture=0),
)

# --- branches ------------------------------------------------------------------------------------
SPLIT = Branch('pol', 'A Union Split Down the Middle', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_tally', 'Counting the Two Camps',
          "The Administration orders a plain count of party sympathy in all five districts, and the totals give it no comfort. "
          "The nationalist camp holds fifty voters in a hundred, the non-aligned camp forty-eight, and the democratic label "
          "under which the government itself sits holds one. Ordering the count costs the comfortable fiction that the Union "
          "is undecided; it is decided twice over, in opposite directions.",
          ('scales', 'ballot'), reward=(Idea('split_country'), Event('even_split'))),
    Focus('pol_nonaligned_rooms', 'Hear the Non-Aligned Camp',
          "The non-aligned camp is less a party than a habit: district directors, cooperative boards, works managers and town "
          "clerks who want the Union run competently and otherwise left alone. Officials spend a season in their offices "
          "asking what they would accept. The answer is continuity and budgets on time. Listening costs attention, and tells "
          "the nationalists exactly whom the government consults first.",
          ('assembly', 'document'), after=('pol_tally',), reward=(TimedIdea('nonaligned_hearing', 365),)),
    Focus('pol_nationalist_rooms', 'Hear the Nationalist Camp',
          "Half the country leans toward the nationalist camp, whose organisers meet in rented halls, sports clubs and the back "
          "rooms of the capital works. The Administration sends officials to listen rather than to argue. The camp wants a "
          "ballot it expects to win, a firmer service and fewer foreign goods in the shops. Hearing it openly lends the camp a "
          "standing it has never been granted.",
          ('assembly', 'security'), after=('pol_tally',), reward=(TimedIdea('nationalist_hearing', 365),)),
    Focus('pol_two_points', 'Two Points Decide It',
          "Every option the ministers can draft turns on the same two points of the tally. A ballot held tomorrow would very "
          "probably give the government to the nationalist list. Keeping the ballot suspended leaves the Union governed "
          "against the wishes of half its voters by a label almost nobody supports. The cabinet must choose which of those "
          "two risks it is prepared to live with.",
          ('scales', 'document'), after=('pol_nonaligned_rooms', 'pol_nationalist_rooms'),
          reward=(PP(30), Tooltip('Opens the ballot path and the suspension path; only one can be taken.'))),
    Focus('pol_call_ballot', 'Call the National Ballot',
          "The first answer honours the election calendar the Union keeps on paper. Rolls are printed, polling halls opened "
          "and every list allowed to stand. The Administration accepts that it is probably organising its own replacement, "
          "and that the count may hand the seals to the nationalist camp. What it gains is a government nobody can call "
          "illegitimate, whatever that government then chooses to do.",
          ('ballot', 'assembly'), after=('pol_two_points',), exclusive=('pol_keep_drawer',),
          reward=(SwapIdea('split_country', 'ballot_called'),)),
    Focus('pol_keep_drawer', 'Keep the Ballot in the Drawer',
          "The second answer leaves the vote suspended. The non-aligned camp, which trusts administrators more than candidates, "
          "prefers it, and the government can keep the works and the trunk line running without a campaign season. The price "
          "is plain to everyone: half the country is told its majority will not be counted, and its organisers will repeat "
          "that sentence at every meeting.",
          ('document', 'command'), after=('pol_two_points',), exclusive=('pol_call_ballot',),
          reward=(SwapIdea('split_country', 'ballot_drawer'),)),
    Focus('pol_list_cabinet', 'The Winning List Takes Office',
          "The nationalist list wins the ballot narrowly and names a cabinet that takes the seals from the National "
          "Administration. It governs as an elected government, bound to the calendar that brought it in and answerable to a "
          "chamber where the non-aligned camp holds nearly half the seats. The change runs through the office, not a person. "
          "Almost half the country watches its new government with dread.",
          ('ballot', 'security'), after=('pol_call_ballot',), cost=10, exclusive=('pol_two_thirds',),
          reward=(Regime('national_list'), Flag('order_list'))),
    Focus('pol_two_thirds', 'A Cabinet Needs Two Thirds',
          "Before the polls open, the Administration and the smaller lists push through one rule: no cabinet takes office "
          "without two thirds of the chamber behind it. Neither camp can reach that alone, so the government that emerges is "
          "a coalition across the split with a chair from the centre. It is slow and quarrelsome by design. The nationalist "
          "camp calls the rule a theft of its narrow majority.",
          ('assembly', 'scales'), after=('pol_call_ballot',), cost=10, exclusive=('pol_list_cabinet',),
          reward=(Regime('union_assembly'), Flag('order_assembly'))),
    Focus('pol_directors', 'The District Directors Govern',
          "With the ballot kept in the drawer, the non-aligned camp's own figures step forward: directors of the five district "
          "offices, the works, the cooperatives and the banks. They form a council that governs by published resolution, with "
          "no party seats and no election. It is competent and unelected, and it rests on forty-eight voters in a hundred "
          "while the other fifty are told to wait.",
          ('command', 'economy'), after=('pol_keep_drawer',), cost=10, exclusive=('pol_caretaker',),
          reward=(Regime('directors_council'), Flag('order_directors'))),
    Focus('pol_caretaker', 'The Administration Holds On',
          "The quietest answer changes nobody. The National Administration keeps the seals under its democratic label, the "
          "ballot stays suspended and no council is formed. Ministers promise competence instead of politics and publish their "
          "accounts every quarter to prove it. Both camps are left waiting, which the Administration counts as an "
          "achievement and both camps count as an insult.",
          ('document', 'scales'), after=('pol_keep_drawer',), cost=10, exclusive=('pol_directors',),
          reward=(SwapIdea('ballot_drawer', 'caretaker_accounts'), Flag('order_caretaker'))),
    Focus('pol_list_pledge', 'A Pledge Read in Every Hall',
          "The nationalist cabinet knows that nearly half the country fears it. To answer that fear it reads a short pledge in "
          "every district hall: the frontiers stay where they are, the service stays defensive, the next ballot keeps its "
          "date and the courts keep their judges. The pledge disappoints some of its own supporters, who wanted more. It buys "
          "a measure of calm from everyone else.",
          ('document', 'peace'), after=('pol_list_cabinet',),
          exclusive=('pol_cross_cabinet', 'pol_weekly_resolutions', 'pol_ballot_date'),
          reward=(SwapIdea('ballot_called', 'list_pledge'),)),
    Focus('pol_cross_cabinet', 'Ministers from Both Camps',
          "The two-thirds rule produces what it was meant to: a cabinet in which ministers from the nationalist list and the "
          "non-aligned camp sit at one table, with a chair from the centre to break ties. Every budget is a negotiation and "
          "every appointment a trade. Decisions come slowly. When they do come, hardly anybody in the Union can claim to have "
          "been left out of them.",
          ('assembly', 'diplomacy'), after=('pol_two_thirds',),
          exclusive=('pol_list_pledge', 'pol_weekly_resolutions', 'pol_ballot_date'),
          reward=(SwapIdea('ballot_called', 'both_camps_cabinet'),)),
    Focus('pol_weekly_resolutions', 'Resolutions Posted Weekly',
          "The directors' council posts its resolutions every week on the door of each district office, with the reasons and "
          "the vote beside them. Nobody elected the council, so it tries to earn trust through visible reasoning instead. The "
          "notices are dull and widely read. Nationalist organisers copy them too, and circle every line that seems to favour "
          "the works over the towns.",
          ('document', 'civil'), after=('pol_directors',),
          exclusive=('pol_list_pledge', 'pol_cross_cabinet', 'pol_ballot_date'),
          reward=(SwapIdea('ballot_drawer', 'posted_resolutions'),)),
    Focus('pol_ballot_date', 'A Date for the Next Ballot',
          "Holding on cannot last forever, and the Administration knows it. It prints the date of the next national ballot "
          "four years ahead, with rolls, rules and counting procedures attached, and promises to keep it. Both camps begin "
          "organising at once. The government gains a clear term in which to work and loses any chance of postponing again "
          "without breaking its printed word.",
          ('ballot', 'document'), after=('pol_caretaker',),
          exclusive=('pol_list_pledge', 'pol_cross_cabinet', 'pol_weekly_resolutions'),
          reward=(SwapIdea('caretaker_accounts', 'ballot_date_set'),)),
    Focus('pol_lot_clerks', 'Count Clerks Drawn by Lot',
          "Whatever order now governs, every future count of votes, petitions or referendums will be run by clerks drawn by "
          "lot from both camps and paid by the courts rather than the government. Each camp grumbles that the other will "
          "cheat; neither can say the count itself is rigged. The office costs salaries and training, and its value lies in "
          "the next close tally, whenever that comes.",
          ('scales', 'ballot'), after_any=('pol_list_pledge', 'pol_cross_cabinet', 'pol_weekly_resolutions', 'pol_ballot_date'),
          reward=(Idea('lot_clerks'),)),
))

LINE = Branch('line', 'One Track, Two Winters', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('line_walk', 'Walk the Trunk to District E',
          "One trunk line carries almost everything that moves in the Union: east from the Capital Centre through the forests "
          "and hills of District C, south across the hills of District D and on to the coast of District E, with a single spur "
          "north to the naval base in District A. Engineers walk every section and price its repair. Freight waits on the "
          "sidings while they do.",
          ('rail', 'document'), reward=(Idea('track_book'), Event('track_report'))),
    Focus('line_spur_roads', 'Roads Beside the Northern Spur',
          "District A has a railway spur and a naval base but not a single graded road; its forest villages reach the line on "
          "foot, or by sledge in winter. Grading roads from the spur into the forest gives the district a way to move goods "
          "that does not depend on one train a day. Crews can work only between the snows, and the budget outlasts every "
          "season.",
          ('logistics', 'civil'), after=('line_walk',), reward=(Build('infrastructure', 2, 359),)),
    Focus('line_district_d_roads', 'Roads Off the Line in District D',
          "The trunk crosses District D on a single hill province and leaves the rest of the district without a graded road, "
          "including the mountain and the southern shore. Four of the Union's five land frontiers touch this district. "
          "Grading roads from the line toward the coast and the mountain is slow work in mud that never fully dries, and the "
          "graders sink as often as they move.",
          ('logistics', 'tools'), after=('line_walk',), reward=(Build('infrastructure', 2, 397),)),
    Focus('line_ploughs', 'Plough Wagons for the North',
          "North of the capital the winter is long: snow and blizzards from November to February and frost well into spring, "
          "burying the spur and the first section of the trunk for days at a time. Plough wagons, snow fences and a standing "
          "crew at the Capital Centre keep the line open through the worst weeks. They stand idle for eight months a year, "
          "which the treasury notices.",
          ('rail', 'shelter'), after=('line_spur_roads',), reward=(Idea('plough_wagons'),)),
    Focus('line_drains', 'Drains Under the Southern Ballast',
          "South of District C the climate turns: heavy rain from January to May, baked summers and mud in every month. Water "
          "pools under the ballast and the track sinks out of true. Culverts, ditches and crushed stone along the southern "
          "section keep trains running at speed. The work is filthy and never finished, because the mud returns with every "
          "spring.",
          ('rail', 'tools'), after=('line_district_d_roads',), reward=(Idea('dry_ballast'),)),
    Focus('line_capital_yard', 'A Second Track at the Capital Yard',
          "Both lines start at the Capital Centre, so every delay anywhere in the Union ends up in one crowded yard. A second "
          "through track, longer sidings and a proper goods shed let trains pass instead of queueing. The works take land from "
          "the yard's edge and close two streets for a year. The supply office calls the yard the narrowest point in the "
          "country, and it is right.",
          ('rail', 'civil'), after=('line_walk',), reward=(Build('infrastructure', 1, 0),)),
    Focus('line_district_c_sidings', 'Sidings at the District C Works',
          "District C holds a works and an arms hall on the trunk, yet all its loading happens at a single siding shared with "
          "passenger trains. Separate sidings and a loading ramp let the works ship plate and lorries without blocking the "
          "line. The district gains faster freight, and the arms hall gains a place to load its output away from the "
          "passenger platform and its onlookers.",
          ('industry', 'rail'), after=('line_capital_yard',), reward=(Build('infrastructure', 1, 382),)),
    Focus('line_end_e', 'Where the Line Ends in District E',
          "The trunk ends in the hills of District E, the only district with no land frontier at all. Its works and arms hall, "
          "its forests and its southern coast all depend on the last stretch of line. Extending sidings and graded roads from "
          "the railhead to the shore turns a terminus into a working district. Without them, District E stays the place "
          "where the Union simply stops.",
          ('rail', 'logistics'), after=('line_district_d_roads',), reward=(Build('infrastructure', 1, 414),)),
    Focus('line_steel_timetable', 'A Timetable Built for Steel',
          "With the track repaired, the Union must decide what its timetable is for. The first answer gives freight the night "
          "paths: steel from three districts runs to the northern quay and toward the frontier on fixed slots, and the works "
          "plan around the trains. Passengers and the service take whatever paths are left, and in a crisis the service would "
          "have to wait its turn.",
          ('economy', 'rail'), after_any=('line_ploughs', 'line_drains'), cost=10, exclusive=('line_service_timetable',),
          reward=(SwapIdea('track_book', 'steel_paths'),)),
    Focus('line_service_timetable', 'A Timetable Kept for the Service',
          "The second answer reserves standing paths for the two formations: a sealed timetable that can move both from the "
          "Capital Centre to any district within a day. Freight runs around those paths, and the works lose a few slots every "
          "week to reserved trains that often run empty. A country with no air arm and few roads would gain a way to put its "
          "whole army wherever the rails go.",
          ('rail', 'security'), after_any=('line_ploughs', 'line_drains'), cost=10, exclusive=('line_steel_timetable',),
          reward=(SwapIdea('track_book', 'service_paths'),)),
    Focus('line_telephones', 'Telephones in Every Signal Box',
          "The trunk still runs on timetable and written orders, so a fallen tree in District C can stop trains in District E "
          "for hours before anyone knows why. A telephone wire beside the track, with a set in every signal box and halt, lets "
          "controllers at the Capital Centre follow the whole line at once. Copper thieves will test it, and controllers will "
          "finally know where their trains are.",
          ('communications', 'rail'), after_any=('line_steel_timetable', 'line_service_timetable'),
          reward=(Idea('signal_wires'), Research('train_tech', 0.5, 1))),
))

STEEL = Branch('steel', 'Steel Without Alloys', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('steel_count', 'Ore, Wells and What Is Missing',
          "The ministry of works lists what the Union digs and pumps. Iron ore for steel lies in the Capital District, District "
          "C and District E, with modest oil and rubber in the same three. Of aluminium, chromium and tungsten there is none "
          "at all. The list is short and honest, and it tells the works that every hard alloy and light metal must be bought "
          "abroad or done without.",
          ('industry', 'document'), reward=(Idea('ore_ledger'), Event('alloy_gap'))),
    Focus('steel_capital_wells', 'Pumps for the Capital Oil Wells',
          "The Capital District holds the largest of the Union's small oil deposits, worked by old pumps that lose almost as "
          "much as they lift. New pumps, a gathering line to the yard and a storage tank add little volume but make it steady. "
          "The two formations, the trains and the works all burn the same fuel, and every barrel not imported is a barrel the "
          "treasury keeps.",
          ('economy', 'tools'), after=('steel_count',),
          reward=(TimedIdea('steady_wells', 730), Research('excavation_tech', 0.5, 1))),
    Focus('steel_arms_halls', 'The Three Arms Halls',
          "The Union has three arms halls, one each in the Capital District, District C and District E, building rifles, lorries "
          "and rolling stock for a service of eight battalions. They run below capacity and compete for the same tool steel. "
          "Giving each hall one product line and a shared tool store ends the competition. The halls lose some independence "
          "and gain longer, cheaper runs.",
          ('industry', 'security'), after=('steel_count',), reward=(Idea('one_line_per_hall'),)),
    Focus('steel_household', 'Household Steel for Five Districts',
          "Most Valkan homes still cook, heat and pump water with whatever the local smith can make. A works at the capital "
          "turning surplus plate into stoves, pipe, water tanks and roofing for every district sells cheaply and quickly. The "
          "arms halls lose some steel to it. Families in the frozen north and the wet south notice the difference long before "
          "any minister mentions it.",
          ('civil', 'industry'), after=('steel_count',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('steel_plate_exports', 'Plate for Foreign Yards',
          "The export school argues that Valkan steel is worth most as plate and bar sold abroad, through the northern quay and "
          "across the coastal plain, for hard currency to buy the alloys the Union lacks. Prices are set by strangers and fall "
          "in bad years. The works would grow around the port, and the inland districts would supply ore and little else.",
          ('economy', 'navy'), after_any=('steel_capital_wells', 'steel_arms_halls'), cost=10,
          exclusive=('steel_home_finishing', 'steel_alloy_barter'), reward=(SwapIdea('ore_ledger', 'plate_exports'),)),
    Focus('steel_home_finishing', 'Finish Every Bar at Home',
          "The second school wants every bar of Valkan steel finished inside the Union: pipe, rails, roofing, tools and lorry "
          "frames for the districts' own needs. New works would go to District D, which has none, close to the southern "
          "frontiers and their markets. Output stays at home and prices stay steady. Without imported alloys, the tools will "
          "be softer and wear out sooner.",
          ('tools', 'industry'), after_any=('steel_capital_wells', 'steel_arms_halls'), cost=10,
          exclusive=('steel_plate_exports', 'steel_alloy_barter'), reward=(SwapIdea('ore_ledger', 'home_finishing'),)),
    Focus('steel_alloy_barter', 'Ore for Alloys by Barter',
          "A third school proposes trading ore and pig iron directly for chromium, tungsten and light metals under long barter "
          "contracts, with no cash changing hands. It promises the alloys that would let the works make better tools and "
          "engines. Barter partners know exactly how badly the Union needs them, however, and contracts written from weakness "
          "are rarely generous.",
          ('diplomacy', 'industry'), after_any=('steel_capital_wells', 'steel_arms_halls'), cost=10,
          exclusive=('steel_plate_exports', 'steel_home_finishing'), reward=(SwapIdea('ore_ledger', 'alloy_barter'),)),
    Focus('steel_north_mill', 'A Rolling Mill at the Naval Base',
          "Export plate needs a rolling mill close to the ships. District A, with the naval base and the spur, has room for one "
          "on cleared forest ground beside the quay. The mill brings wages to a district that has never had a works. It also "
          "ties the northern economy to foreign buyers, whose orders arrive by telegram and can vanish the same way.",
          ('industry', 'navy'), after=('steel_plate_exports',), reward=(Build('industrial_complex', 1, 359),)),
    Focus('steel_district_d_works', 'Machine Works for District D',
          "District D has four frontiers, one mountain and no industry. Two finishing works beside the trunk, making rails, "
          "pipe and tools for the districts, give it wages and a reason for every train to stop there. Building in permanent "
          "mud is expensive, and the works will need roads and drains before they need orders. Once running, they serve the "
          "north and south alike.",
          ('tools', 'rail'), after=('steel_home_finishing',), reward=(Build('industrial_complex', 2, 397),)),
    Focus('steel_alloy_school', 'A Metallurgy School at the Capital',
          "Bartered alloys are wasted if nobody knows how to use them. A metallurgy school beside the capital works trains "
          "furnace crews and engineers in alloy steels, heat treatment and testing, with a laboratory that assays every barter "
          "shipment. It costs salaries for scarce teachers. It also catches the first short-weighted cargo before the works "
          "pays for it.",
          ('science', 'industry'), after=('steel_alloy_barter',),
          reward=(Idea('alloy_testing'), Research('industry', 0.5, 2))),
    Focus('steel_district_e_hall', 'A Second Hall in District E',
          "District E sits at the end of the trunk with one works, one arms hall and the shortest route to the southern sea. A "
          "second arms hall beside the first, sharing its tool store and siding, raises output of rifles and lorries without "
          "building in a new district. It also concentrates production at the far end of the only line, where one washed-out "
          "culvert can cut it off.",
          ('security', 'tools'), after=('steel_arms_halls',), reward=(Build('arms_factory', 1, 414),)),
    Focus('steel_ingot_reserve', 'An Ingot Reserve at the Yard',
          "Whichever school prevailed, the works keep a reserve of finished ingots and bar in a fenced yard at the Capital "
          "Centre, enough to keep the arms halls working for a season if ore or alloys stop. The stock earns nothing while it "
          "sits. The service likes it, the treasury dislikes it, and the works managers quietly borrow from it whenever the "
          "trains run late.",
          ('security', 'industry'), after_any=('steel_north_mill', 'steel_district_d_works', 'steel_alloy_school'),
          reward=(Idea('ingot_reserve'),)),
))

GUARD = Branch('guard', 'Eight Battalions for Floods and Snow', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_muster', 'Both Formations at the Capital Centre',
          "The Union's whole army is two infantry formations of four battalions each, quartered at the Capital Centre, with no "
          "engineers, no guns and no support companies. It was shaped for civil defence: floods, fires, snow and public order. "
          "A full inspection tells the Administration what it actually has, and the answer will disappoint anyone who imagined "
          "a frontier force.",
          ('security', 'training'), reward=(Idea('eight_battalions'), Event('service_review'))),
    Focus('guard_flood_companies', 'Flood Companies for the South',
          "From January to May the southern districts take heavy rain, and the mud that follows never quite dries. Training two "
          "companies in each formation for flood work, with boats, pumps and sandbag stores at the District D and District E "
          "halts, puts the service where the danger comes every year. Soldiers learn the ground. The capital loses a few "
          "companies every spring.",
          ('civil', 'training'), after=('guard_muster',), reward=(Idea('flood_companies'),)),
    Focus('guard_blizzard_drill', 'Blizzard Drills in the North',
          "Winter in the north brings blizzards from November to February, and a battalion caught on the spur road in a storm "
          "becomes a rescue job for somebody else. Drills in deep snow, tents rated for the cold and skis issued to each "
          "company teach the service to move and survive in it. The kit costs money and the drills cost frostbite. Both "
          "formations come back hardened.",
          ('training', 'shelter'), after=('guard_muster',), reward=(TimedIdea('cold_drilled', 365), XP('army', 20))),
    Focus('guard_district_companies', 'Companies Quartered by District',
          "The first doctrine spreads the battalions across the country, with a company quartered near each district office "
          "and each southern frontier. Help reaches a flood or a fire in hours rather than a day, and every district sees its "
          "own soldiers. The formations lose their cohesion as fighting units, and no commander could gather all eight "
          "battalions quickly for anything larger.",
          ('security', 'civil'), after_any=('guard_flood_companies', 'guard_blizzard_drill'), cost=10,
          exclusive=('guard_rail_reserve',), reward=(SwapIdea('eight_battalions', 'district_companies'),)),
    Focus('guard_rail_reserve', 'A Reserve That Rides the Trunk',
          "The second doctrine keeps both formations together at the Capital Centre and trusts the trunk line to carry them "
          "wherever they are needed. They train as complete formations and keep their officers in one mess. Every district "
          "now depends on the trains running, and the furthest district of all, at the end of the line, waits longest for "
          "help.",
          ('rail', 'command'), after_any=('guard_flood_companies', 'guard_blizzard_drill'), cost=10,
          exclusive=('guard_district_companies',), reward=(SwapIdea('eight_battalions', 'rail_reserve'),)),
    Focus('guard_mountain_course', 'Climbing Courses on the Mountain',
          "The service has long taught a few soldiers to climb, and the Union has exactly one mountain, in District D, above "
          "four frontiers. A climbing course there, with instructors, a hut and a summer camp, gives each battalion a handful "
          "of soldiers who can work on rock and in snow. They are useful in rescues and on the high frontier. The course runs "
          "only in the dry months.",
          ('training', 'medal'), after_any=('guard_district_companies', 'guard_rail_reserve'),
          reward=(Idea('climbing_course'), Research('land_doctrine', 0.5, 1))),
    Focus('guard_pioneers', 'Engineers Trained from Nothing',
          "Not one battalion has an engineer company, yet every flood, landslide and fallen bridge the service meets is "
          "engineering work. A school at the Capital Centre trains a pioneer platoon for each battalion in bridging, "
          "demolition and pumping, using whatever the works can supply. Skilled sappers take years. Until they exist, the "
          "service fights floods with shovels and goodwill.",
          ('tools', 'training'), after_any=('guard_district_companies', 'guard_rail_reserve'),
          reward=(Idea('pioneer_platoons'), Research('engineers_tech', 0.75, 1))),
    Focus('guard_volunteer_lists', 'Volunteer Lists by District',
          "The service takes volunteers only, and in a real crisis it would need far more than eight battalions. Lists of "
          "former soldiers and willing civilians, kept by each district office with an address and a trade, would let it "
          "double its strength in weeks instead of months. Clerks must renew them every year. Nationalists call the lists too "
          "timid, and the non-aligned camp calls them quite enough.",
          ('document', 'training'), after=('guard_muster',), reward=(Idea('district_volunteer_lists'),)),
    Focus('guard_lorries', 'A Lorry Company per Formation',
          "The arms halls have built more lorries than the service can crew. Assigning a lorry company to each formation, with "
          "fitters and a fuel allowance, lets battalions reach beyond the railheads on roads the trains never touch. Fuel is "
          "scarce and partly imported, and every kilometre driven on exercise is paid for by the treasury, which counts each "
          "one.",
          ('logistics', 'security'), after=('guard_volunteer_lists',), reward=(Idea('lorry_companies'),)),
    Focus('guard_rescue_flight', 'A Rescue Flight Before Fighters',
          "The Union has no airfield and no aircraft, although its engineers studied early fighter designs years ago. The first "
          "answer builds a small field at the capital for a rescue and liaison flight: light aircraft carrying doctors, mail "
          "and spotters to floods, fires and blizzards. It is a modest beginning. It defends nothing, and it will be busy in "
          "every month of the year.",
          ('air', 'medical'), after_any=('guard_mountain_course', 'guard_pioneers', 'guard_lorries'),
          exclusive=('guard_fighter_flight',), reward=(Build('air_base', 1, 0), Idea('rescue_flight'))),
    Focus('guard_fighter_flight', 'A Flight of Early Fighters',
          "The second answer builds a proper field at the capital and a pilot school for a small flight of early fighters, on "
          "designs the engineers already understand. It gives the Union a way to challenge an intruder over its own sky. The "
          "cost is high for so small a country, and the aircraft will mostly sit on the ground waiting for a threat that may "
          "never arrive.",
          ('air', 'security'), after_any=('guard_mountain_course', 'guard_pioneers', 'guard_lorries'),
          exclusive=('guard_rescue_flight',), reward=(Build('air_base', 2, 0), Idea('fighter_flight'), XP('air', 20))),
    Focus('guard_tented_hospitals', 'Tented Hospitals for Emergencies',
          "Floods, fires and blizzards injure civilians far more often than war has ever injured Valkan soldiers. Two tented "
          "field hospitals, stored at the capital with surgeons and nurses on a call list, can be on a train within hours and "
          "open in any district a day later. They cost money every year to stock and staff. The first time they are used, "
          "nobody will ask why.",
          ('medical', 'civil'), after=('guard_flood_companies',), reward=(Idea('tented_hospitals'),)),
))

COAST = Branch('coast', 'Three Shores, One Naval Base', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('coast_sixty', 'Sixty Freighters Under One Flag',
          "The Union has three shores and a single naval base, at the forest port of District A in the north. It has no "
          "warships at all, but sixty convoys of freighters sail under its flag, carrying ore, steel and timber out and fuel "
          "and machinery home. A register of their masters, cargoes and routes is the first step toward any maritime policy, "
          "and shipowners resent the questions.",
          ('navy', 'document'), reward=(Idea('sixty_convoys'), Event('north_harbour'))),
    Focus('coast_quay', 'A Longer Quay in District A',
          "The naval base in District A is a single quay in a forest inlet, and the spur line ends a few hundred metres short "
          "of it. Lengthening the quay and laying rails to its edge lets steel trains unload straight into ships. Forest is "
          "cleared for the yard. Winter storms still close the inlet for days, and the harbour master asks for a tug before "
          "any more berths are promised.",
          ('navy', 'rail'), after=('coast_sixty',), reward=(Build('infrastructure', 1, 359),)),
    Focus('coast_capital_lighters', 'Lighters Along the Capital Shore',
          "The Capital District faces the western sea along a forested shore but has no harbour of its own, so ships calling "
          "there anchor offshore and unload into small boats. Most of the capital's freight goes north by the spur or by road "
          "across the frontier toward an Aquitorian port. A fleet of lighters and a landing stage make the shortest route "
          "cheaper.",
          ('logistics', 'navy'), after=('coast_sixty',), reward=(Idea('capital_lighters'),)),
    Focus('coast_south_landings', 'Landing Stages on the Southern Bay',
          "The southern coasts of District D and District E open onto the bay that Valka shares with Monstrua and Aquitoria, "
          "and onto the sea further east. Fishing boats work from beaches there, hauled up by hand. Concrete landing stages, "
          "an ice house and a road to the nearest halt give the southern villages a steady trade. The bay is also where any "
          "foreign patrol would be seen first.",
          ('fishing', 'navy'), after=('coast_sixty',), reward=(Idea('south_landings'),)),
    Focus('coast_cutters', 'Cutters for a Coast Watch',
          "The first answer gives the Union a small coast watch: armed cutters crewed by volunteers from the service, patrolling "
          "the three shores for smugglers, wrecks and poachers. It is the nearest thing to a navy the country can afford. "
          "Cutters cost fuel, crews and a repair shop. They would not stop a warship, and nobody pretends they are meant to.",
          ('navy', 'security'), after_any=('coast_quay', 'coast_capital_lighters', 'coast_south_landings'),
          exclusive=('coast_freighters',), reward=(SwapIdea('sixty_convoys', 'coast_watch'), XP('navy', 15))),
    Focus('coast_freighters', 'Freighters Before Cutters',
          "The second answer spends the maritime budget on the merchant fleet instead: credit for new freighters and training "
          "for merchant officers. Ore and steel reach buyers faster and fuel comes home cheaper. The three shores remain "
          "watched only by fishermen and lighthouse keepers, which the service considers a risk and the shipowners consider "
          "a saving.",
          ('economy', 'navy'), after_any=('coast_quay', 'coast_capital_lighters', 'coast_south_landings'),
          exclusive=('coast_cutters',), reward=(SwapIdea('sixty_convoys', 'freighter_credit'),)),
    Focus('coast_slipway', 'A Slipway Beside the Quay',
          "Every Valkan hull is repaired abroad, because the Union has no dockyard anywhere. A slipway beside the District A "
          "quay, with a crane and a plate shop fed by the spur, can repair freighters and build small craft. Skilled "
          "shipwrights must be hired from foreign yards at first. The slipway gives the northern port a second trade besides "
          "loading steel.",
          ('tools', 'navy'), after_any=('coast_cutters', 'coast_freighters'), reward=(Build('dockyard', 1, 359),)),
    Focus('coast_storm_radio', 'Storm Warnings by Radio',
          "Three shores face three different seas, and the weather that wrecks a fishing fleet in the south rarely matches what "
          "is falling on the north. A coastal radio station at the capital, broadcasting storm warnings twice a day from "
          "observers at every landing, gives masters time to run for shelter. The observers must be paid all year. The "
          "fishing villages are listening within a week.",
          ('communications', 'navy'), after=('coast_south_landings',), reward=(Idea('storm_warnings'),)),
    Focus('coast_headlands', 'Lights on the Southern Headlands',
          "The southern coast of District E is hills and forest falling straight into the sea, and its headlands are unlit. "
          "Wrecks there are a seasonal certainty. Three lights with resident keepers, supplied by the new landing roads, make "
          "the coast navigable at night and give fishermen a fixed mark. Keepers are hard to find for such lonely posts; the "
          "lights burn regardless.",
          ('telescope', 'navy'), after=('coast_storm_radio',),
          reward=(Idea('headland_lights'), Research('naval_equipment', 0.5, 1))),
))

HINGE = Branch('hinge', 'Four Frontiers Meet in District D', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('hinge_map', 'Five Neighbours, One Survey',
          "The frontier office maps every land frontier the Union has: Malynea along the northern forest, Seterano across the "
          "eastern mountain, Slavia over the eastern hills, and Monstrua and Aquitoria to the south-west across plain and hill. "
          "Four of the five touch District D. Only District E has no frontier at all. The survey records crossings on the "
          "Valkan side and claims nothing beyond it.",
          ('diplomacy', 'document'), reward=(Idea('five_frontiers_desk'), Event('hinge_report'))),
    Focus('hinge_plains_post', 'Our Post at the Plains Crossing',
          "The frontier with Monstrua touches District D at one coastal hill province, facing a crossing onto the plain beyond. "
          "Carts and small lorries use it daily. A staffed customs post, a weighbridge and a graded road from the post to the "
          "trunk make that trade lawful and visible on the Valkan side. Whatever stands at the far end of the crossing is "
          "Monstrua's own business.",
          ('economy', 'security'), after=('hinge_map',),
          reward=(Build('infrastructure', 1, 397), TimedIdea('southern_post', 730))),
    Focus('hinge_lorry_park', 'Lorry Parks at the Aquitorian Line',
          "Valkan lorries already cross the coastal plain into Aquitoria to reach a port there, and they queue at the Valkan "
          "post for hours. A lorry park, a single inspection shed and longer opening hours on the Valkan side halve the wait. "
          "Ministers cannot know what Aquitoria will do at its own post, and do not ask; the Valkan half of the queue is "
          "theirs to fix.",
          ('logistics', 'diplomacy'), after=('hinge_map',),
          reward=(Build('infrastructure', 1, 0), TimedIdea('frontier_lorry_park', 730))),
    Focus('hinge_hill_wardens', 'Shepherds on the Eastern Hills',
          "The hills between District D and Slavia are crossed by shepherds, labourers and the occasional smuggler on tracks no "
          "map shows. Rather than close them, the Union posts two wardens who walk the tracks, count flocks and help anyone "
          "caught out in the winter rain. The wardens come to know the ground better than any patrol could. The Slavian side "
          "of the hills is Slavia's affair.",
          ('peace', 'security'), after=('hinge_map',), reward=(Idea('hill_wardens'),)),
    Focus('hinge_firebreaks', 'Firebreaks Along the Malynean Forest',
          "The northern forest of District A and District C continues across the frontier into Malynea without a break, and "
          "in a dry spell a fire on either side threatens both. Firebreaks cut on the Valkan side, with water tanks and a "
          "watch roster for the risky weeks, give fire crews a line to hold. Cutting them costs timber the works would "
          "have sold, and the gain is invisible when it works.",
          ('civil', 'peace'), after=('hinge_map',), reward=(Idea('northern_firebreaks'),)),
    Focus('hinge_transit_toll', 'A Toll on Foreign Freight',
          "The first posture treats the Union's position between five neighbours as an asset. Foreign freight crossing Valka by "
          "road or on the trunk pays a transit toll at the frontier posts, collected in hard currency. The treasury gains a "
          "steady income. Each neighbour gains a reason to route around the Union where it can, and traders on every side "
          "learn to resent the toll booth.",
          ('economy', 'gate'), after_any=('hinge_plains_post', 'hinge_lorry_park', 'hinge_hill_wardens', 'hinge_firebreaks'),
          cost=10, exclusive=('hinge_transit_cost', 'hinge_trunk_reserved'),
          reward=(SwapIdea('five_frontiers_desk', 'transit_toll'), Flag('posture_toll'))),
    Focus('hinge_transit_cost', 'Transit at Cost for Every Neighbour',
          "The second posture charges foreign freight only what its handling costs, at every post and on every train, and "
          "publishes the same tariff for all five neighbours. The treasury gains little directly. Traders route through the "
          "Union because it is cheap and predictable, and the frontier districts fill with depots, inns and repair shops. A "
          "neighbour may object to the goods its rival moves.",
          ('logistics', 'peace'), after_any=('hinge_plains_post', 'hinge_lorry_park', 'hinge_hill_wardens', 'hinge_firebreaks'),
          cost=10, exclusive=('hinge_transit_toll', 'hinge_trunk_reserved'),
          reward=(SwapIdea('five_frontiers_desk', 'transit_at_cost'), Flag('posture_open'))),
    Focus('hinge_trunk_reserved', 'The Trunk for Valkan Freight Only',
          "The third posture keeps the trunk and the frontier roads for Valkan goods and travellers, with foreign freight "
          "allowed only by permit. It protects the line's capacity for the service and the works, and keeps the Union clear of "
          "other countries' quarrels over what moves where. Frontier districts lose trade they had. Neighbours conclude that "
          "the Union prefers its doors narrow.",
          ('security', 'rail'), after_any=('hinge_plains_post', 'hinge_lorry_park', 'hinge_hill_wardens', 'hinge_firebreaks'),
          cost=10, exclusive=('hinge_transit_toll', 'hinge_transit_cost'),
          reward=(SwapIdea('five_frontiers_desk', 'trunk_reserved'), Flag('posture_closed'))),
    Focus('hinge_toll_receipts', 'Toll Receipts for the Frontier Districts',
          "Tolls collected at the posts in District D and the Capital District flow to the treasury in the capital, and the "
          "frontier districts complain that they bear the queues while others spend the money. Paying half of every toll back "
          "to the district where it was collected answers them. The treasury loses half its new income and gains two "
          "districts that defend the toll.",
          ('scales', 'economy'), after_any=('hinge_transit_toll', 'hinge_transit_cost', 'hinge_trunk_reserved'),
          requires=(HasFlag('posture_toll'),), exclusive=('hinge_depot_towns', 'hinge_permit_office'),
          reward=(SwapIdea('transit_toll', 'toll_receipts'),)),
    Focus('hinge_depot_towns', 'Depot Towns at the Crossings',
          "Cheap transit draws freight, and freight needs warehouses, fuel, inns and fitters. The Union grades land beside the "
          "busiest posts in District D for depots and leases it on easy terms. Small towns grow where there were only customs "
          "huts. They bring wages to the hills, and also the smuggling, quarrels and late nights that come with every road "
          "junction.",
          ('logistics', 'civil'), after_any=('hinge_transit_toll', 'hinge_transit_cost', 'hinge_trunk_reserved'),
          requires=(HasFlag('posture_open'),), exclusive=('hinge_toll_receipts', 'hinge_permit_office'),
          reward=(SwapIdea('transit_at_cost', 'depot_towns'), Build('infrastructure', 1, 397))),
    Focus('hinge_permit_office', 'A Permit Office at the Capital',
          "Permits for foreign freight need one office that issues them, records every load and checks it at the frontier on "
          "the way out. The office sits beside the capital yard and answers to the service as well as the treasury. Traders "
          "wait days for a stamp. The Union knows exactly what crosses it, which is the point and also the complaint.",
          ('document', 'security'), after_any=('hinge_transit_toll', 'hinge_transit_cost', 'hinge_trunk_reserved'),
          requires=(HasFlag('posture_closed'),), exclusive=('hinge_toll_receipts', 'hinge_depot_towns'),
          reward=(SwapIdea('trunk_reserved', 'permit_office'),)),
    Focus('hinge_mountain_watch', 'A Watch Post on the Mountain',
          "The single mountain in District D overlooks four frontiers at once. A small watch post on its shoulder, with a "
          "telescope, a radio and a hut for two observers, sees weather coming over the hills and traffic on every approach. "
          "It costs little but a lonely rota. The post changes nothing on any frontier; it simply means the Union learns "
          "things a day earlier.",
          ('telescope', 'security'), after=('hinge_hill_wardens',), reward=(Idea('mountain_watch'),)),
    Focus('hinge_letter_desk', 'A Desk That Answers Neighbours',
          "Neighbouring governments write now and then about floods, fires, stray herds or a lorry held at a post, and their "
          "letters sit for weeks in the wrong ministry. One desk at the capital, with a clerk assigned to each neighbour and a "
          "promise to answer within ten days, ends that. The Union offers nothing new by it. It simply stops being the "
          "neighbour that never replies.",
          ('diplomacy', 'communications'), after_any=('hinge_toll_receipts', 'hinge_depot_towns', 'hinge_permit_office'),
          reward=(Idea('neighbour_desk'),)),
))

SKY = Branch('sky', 'Ulysses Over the Union', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_notice', 'The December Warning',
          "The astronomers' warning of December 1994 says that the asteroid Ulysses will come close to the planet and might "
          "hit it, and says nothing about where. Within the week the Administration forms an impact office of engineers, "
          "doctors and officers of the service and gives it one question to answer: where in the Union could people survive "
          "a strike nearby.",
          ('meteor', 'telescope'), requires=(After('1994.12.10'),), reward=(Idea('impact_office'), Event('sky_notice'))),
    Focus('sky_ground_survey', 'Which Ground Will Hold',
          "Engineers test the ground in every district for shelter digging. The north is frozen for months and its forest soil "
          "lies thin over rock. The south is wet, with mud in every month and water close beneath. The mountain in District D "
          "is solid stone with a road only to its foot. Each answer carries a different bill, and every district argues for "
          "its own.",
          ('tools', 'meteor'), after=('sky_notice',), reward=(Research('construction_tech', 0.5, 1),)),
    Focus('sky_galleries', 'Galleries in the District D Rock',
          "The first plan drives shelter galleries into the mountain of District D, where solid rock would stand above any "
          "blast. Each gallery would hold thousands with stores for weeks. They lie far from the capital and the north, so the "
          "plan depends on trains reaching them in time. Building in the mountain takes years and every rail wagon the works "
          "can spare.",
          ('shelter', 'tools'), after=('sky_ground_survey',), cost=10, exclusive=('sky_hall_cellars', 'sky_evacuation'),
          reward=(SwapIdea('impact_office', 'rock_galleries'),)),
    Focus('sky_hall_cellars', 'Strong Cellars Under Public Halls',
          "The second plan deepens and props the cellars of schools, district offices and works canteens in every town, so "
          "people shelter close to home. It is cheaper per head and needs no warning by train. In the north the digging stops "
          "when the ground freezes; in the south the pumps never stop. The cellars would not survive a direct strike, and "
          "nobody pretends otherwise.",
          ('shelter', 'civil'), after=('sky_ground_survey',), cost=10, exclusive=('sky_galleries', 'sky_evacuation'),
          reward=(SwapIdea('impact_office', 'hall_cellars'),)),
    Focus('sky_evacuation', 'Evacuation Trains on the Trunk',
          "The third plan relies on warning and distance: sealed timetables that empty any threatened district by rail toward "
          "the others, using every carriage and goods wagon in the Union. It costs the least in concrete and the most in "
          "organisation. It also assumes somebody will know where fragments are falling in time to choose a direction. The "
          "railwaymen ask who will warn them.",
          ('rail', 'refugees'), after=('sky_ground_survey',), cost=10, exclusive=('sky_galleries', 'sky_hall_cellars'),
          reward=(SwapIdea('impact_office', 'evacuation_timetable'),)),
    Focus('sky_impact_declared', 'Priority for the Shelter Works',
          "The FCU's statement of April 1996 removes any doubt that Ulysses will hit the planet, though not where. For the "
          "impact office, drawing gives way to digging. The works take priority orders for steel props and pumps, every "
          "district office posts its shelter list and the trains carry cement before coal. Tinned food and lamp oil double in "
          "price within a week, and the shops ration both.",
          ('meteor', 'industry'), after_any=('sky_galleries', 'sky_hall_cellars', 'sky_evacuation'),
          requires=(After('1996.4.20'),), reward=(TimedIdea('shelter_priority', 730), Stability(-0.02))),
    Focus('sky_depots', 'A Dark Year in the Depots',
          "If dust from the impact dims the sky for a season, harvests could fail far from any crater. Each district depot "
          "stores seed, fuel and medicine for a year, rotated so that nothing spoils. The stores cost warehouse space and "
          "constant accounting. Families resent seeing grain locked away while prices rise, and every depot needs guards "
          "around the clock.",
          ('logistics', 'shelter'), after=('sky_impact_declared',), reward=(Idea('dark_year_depots'),)),
    Focus('sky_sirens', 'Sirens on Every District Office',
          "Warning is worth nothing if it cannot reach people. Sirens on every district office and works roof, wired to the "
          "capital and tested on the first Sunday of each month, give the Union a single alarm. The tests annoy everybody. The "
          "service, the railway and the shelters all need the same few minutes of notice, and the sirens are how they will "
          "get it.",
          ('communications', 'shelter'), after=('sky_notice',), reward=(Idea('sunday_sirens'),)),
    Focus('sky_roche_night', 'Shelters Open on the Roche Night',
          "When Ulysses crosses the Roche limit in July 1999 and starts to come apart, the Union is as ready as years of "
          "digging allowed. The shelters open, the trains stand on their sealed timetables and the service waits at the "
          "capital with the field hospitals packed. What the night brings to Valkan ground is not known to anyone who plans "
          "for it, and the plan must hold either way.",
          ('meteor', 'security'), after=('sky_impact_declared',), requires=(After('1999.7.8'),),
          reward=(TimedIdea('roche_watch', 365), Stability(0.02))),
    Focus('sky_relief_trains', 'Relief Trains for Wherever It Fell',
          "Whatever fell, somebody nearby will need help, whether in a Valkan district or across a frontier. The impact office "
          "keeps two relief trains made up at the capital, with tents, medicine, pumps and engineers, ready to run to the end "
          "of any line. Offering them abroad is a separate decision for a later day. At home, they mean no district waits for "
          "a committee.",
          ('rail', 'medical'), after=('sky_roche_night',), reward=(Idea('relief_trains'),)),
))

WARS = Branch('wars', 'Distant Wars on the Freight Bill', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('wars_premiums', 'Insurance in a Distant War',
          "In March 1995 war breaks out around Belka, far from Valkan waters, and insurers raise premiums on every hull at sea. "
          "Valkan freighters carry ore and steel on lanes that touch no front and pay the higher rates all the same. The steel "
          "price abroad will now move for reasons nobody in the Union controls, and the government must decide who carries "
          "the cost.",
          ('economy', 'navy'), requires=(After('1995.3.25'),),
          reward=(TimedIdea('war_premiums', 730), Event('freight_war'))),
    Focus('wars_hull_pool', 'A State Pool for Hull Insurance',
          "The first answer creates a state pool that carries part of the war risk on Valkan freighters at a fixed premium, "
          "backed by the treasury. Owners keep sailing and buyers keep their delivery dates. The pool will pay out if a "
          "Valkan hull is lost anywhere near the fighting. Ministers are betting that none will be, and the opposition camp "
          "says so in print.",
          ('navy', 'scales'), after=('wars_premiums',), exclusive=('wars_owners_risk',), reward=(Idea('hull_pool'),)),
    Focus('wars_owners_risk', 'Owners Carry Their Own Risk',
          "The second answer leaves the war risk where the insurers put it. Shipowners raise their freight rates, foreign "
          "buyers pay more for Valkan plate and some cargoes simply wait in port. The treasury keeps its money for the line "
          "and the shelters. Owners in District A call the decision a betrayal and quietly reflag two freighters elsewhere.",
          ('document', 'navy'), after=('wars_premiums',), exclusive=('wars_hull_pool',),
          reward=(Idea('owners_risk'), PP(20))),
    Focus('wars_peace_buyers', 'Steel Only for Buyers at Peace',
          "Foreign buyers ask whether the Union will sell plate and bar to parties at war. The first answer is no: Valkan steel "
          "goes only to buyers at peace, checked by the export office before every contract. Orders fall, and the works "
          "notice. The Union keeps a reputation that both of its political camps can defend, for once, in the same words.",
          ('peace', 'scales'), after_any=('wars_hull_pool', 'wars_owners_risk'), exclusive=('wars_any_buyer',),
          reward=(Idea('peace_buyers'),)),
    Focus('wars_any_buyer', 'Orders from Any Buyer Who Pays',
          "The second answer fills any order that is paid for in advance, whoever places it, and leaves the use of the steel to "
          "the buyer. The works run full shifts and the treasury collects export duty. The Union becomes a supplier to other "
          "countries' wars at one remove, and some of its own citizens will find that harder to live with than the money.",
          ('economy', 'industry'), after_any=('wars_hull_pool', 'wars_owners_risk'), exclusive=('wars_peace_buyers',),
          reward=(Idea('any_buyer'),)),
    Focus('wars_treaty', 'After the Treaty in Lumen',
          "The Belkan War ends with the treaty at Lumen in June 1995. Premiums come down slowly, over a year rather than a "
          "week, and buyers who held back return with their orders. The ministry uses the lull to renegotiate long contracts "
          "for fuel and alloys while sellers are eager. Nobody in the Union expects the peace to make every price fall at "
          "once.",
          ('peace', 'economy'), after_any=('wars_peace_buyers', 'wars_any_buyer'), requires=(After('1995.6.20'),),
          reward=(TimedIdea('treaty_trade', 365), Stability(0.01))),
    Focus('wars_fuel_tanks', 'Fuel Tanks Full by November',
          "The war taught the ministry that fuel prices can double in a week. Tanks at the capital yard and the northern quay, "
          "filled in the cheap months and kept full before the northern winter, give the trunk line, the works and the service "
          "a reserve. The tanks tie up money and need guards. They also mean a distant war no longer stops a Valkan train.",
          ('logistics', 'security'), after=('wars_treaty',), reward=(Idea('winter_fuel_stock'),)),
    Focus('wars_usean_rates', 'Surcharges from the Usean War',
          "In August 2003 the FCU establishes the ISAF and war spreads across Usea, on another continent entirely. Shipping is "
          "rerouted, insurers raise their rates again and some buyers of Valkan plate ask for faster delivery at higher "
          "prices. The Union has been here before. Its tanks are full and its export rules are written, and the works can "
          "plan around the disruption.",
          ('logistics', 'economy'), after=('wars_fuel_tanks',),
          requires=(After('2003.8.22'), HasGlobal('ac_ucw_isaf_formed')), reward=(TimedIdea('usean_rates', 730),)),
    Focus('wars_rebuilding', 'Rails for the Rebuilding',
          "With the Continental War over and the ISAF's victory recorded, reconstruction on Usea will need steel, rails and "
          "pipe in quantity. The ministry offers Valkan products through ordinary tenders, at ordinary prices, and sends its "
          "catalogue to every buyer that asks. Orders arrive slowly. The works welcome steady customers who are building "
          "rather than fighting.",
          ('rebuild', 'economy'), after=('wars_usean_rates',),
          requires=(After('2005.9.19'), HasGlobal('ac_ucw_outcome_isaf_victory')), reward=(TimedIdea('rebuilding_orders', 730),)),
))

CENTURY = Branch('cent', 'The Union at Two Thousand', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_audit', 'An Audit of the Decade',
          "At the turn of the century the government commissions an audit of what ten years have built: the line, the works, "
          "the shelters, the frontier posts and the northern quay. Auditors drawn from both camps, with a judge in the chair, "
          "read every ledger. Their report will be quoted for years. Paying for that honesty costs a season of political "
          "quiet.",
          ('scales', 'document'), reward=(Idea('decade_audit'), Event('decade_audit'))),
    Focus('cent_list_term', 'The List Goes Back to the Voters',
          "The national list promised that the next ballot would keep its date, and the date has arrived. The cabinet campaigns "
          "on its record and the non-aligned camp on its fears. Whatever the count, the list has shown that it will face the "
          "voters it once said it could trust. Its own hardliners think the risk was unnecessary.",
          ('ballot', 'security'), after=('cent_audit',), requires=(HasFlag('order_list'),),
          exclusive=('cent_rule_renewed', 'cent_director_terms', 'cent_date_kept'), reward=(Idea('list_second_term'),)),
    Focus('cent_rule_renewed', 'Renew the Two-Thirds Rule',
          "The two-thirds rule was written for one chamber, and the next chamber must decide whether to keep it. Both camps "
          "have learned to work inside it, and both have reasons to want it gone. The chamber votes to renew it for another "
          "decade by a margin that itself crosses the split. The vote is slow to arrange and widely trusted.",
          ('assembly', 'scales'), after=('cent_audit',), requires=(HasFlag('order_assembly'),),
          exclusive=('cent_list_term', 'cent_director_terms', 'cent_date_kept'), reward=(Idea('rule_renewed'),)),
    Focus('cent_director_terms', 'Five-Year Terms for Directors',
          "The directors' council has governed for years without an election, and some of its members have never left it. A "
          "rule limiting each director to five years on the council brings in younger managers from the works and the "
          "districts. Experience walks out with the old members. The council gains a way to change without a ballot.",
          ('command', 'document'), after=('cent_audit',), requires=(HasFlag('order_directors'),),
          exclusive=('cent_list_term', 'cent_rule_renewed', 'cent_date_kept'), reward=(Idea('director_rotation'),)),
    Focus('cent_date_kept', 'The Printed Date Arrives',
          "The National Administration printed a ballot date years ago and both camps have spent the interval organising. The "
          "date comes, the halls open and the clerks count. Whoever wins, the Administration has kept its word, which is more "
          "than either camp expected. Several of its own ministers are relieved to hand the problem on at last.",
          ('ballot', 'civil'), after=('cent_audit',), requires=(HasFlag('order_caretaker'),),
          exclusive=('cent_list_term', 'cent_rule_renewed', 'cent_director_terms'), reward=(Idea('date_kept'),)),
    Focus('cent_passing_loops', 'Passing Loops on the Trunk',
          "Ten years of repairs have made the trunk reliable, and reliability has filled it. Trains now wait at District C for "
          "others to clear the single track ahead. Passing loops at the works sidings and the hill halts let two trains meet "
          "without stopping. The loops are cheap next to doubling the line, and they buy another decade before anyone has to "
          "think about that.",
          ('rail', 'industry'), after=('cent_audit',), reward=(Build('infrastructure', 1, 382),)),
    Focus('cent_colleges', 'Engineering Places at the Colleges',
          "The capital colleges train doctors, lawyers and engineers, and the works complain there are never enough of the "
          "last. More engineering places, with bursaries for students from every district, would supply the line, the works "
          "and the service at once. The colleges need laboratories and teachers. The first graduates take five years to "
          "arrive.",
          ('science', 'training'), after=('cent_audit',),
          reward=(Idea('college_places'), Research('electronics', 0.5, 1))),
    Focus('cent_second_tally', 'The Tally Taken Again',
          "A decade after the first count, the clerks drawn by lot take a second national tally of party sympathy, district by "
          "district, and publish it the same day. Nobody can call it the government's number. The result tells the Union "
          "whether ten years have healed the split, deepened it or merely moved it. All three camps prepare their statements in "
          "advance.",
          ('ballot', 'scales'), after_any=('cent_list_term', 'cent_rule_renewed', 'cent_director_terms', 'cent_date_kept'),
          reward=(Idea('second_tally'),)),
))

BRANCHES = (SPLIT, LINE, STEEL, GUARD, COAST, HINGE, SKY, WARS, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('plough_run', 'Send the Plough Wagons Up the Spur',
                'Put the plough wagons and a shovel crew on the northern spur after a blizzard. Costs political power; repeatable '
                'each winter.', 25, (TimedIdea('spur_cleared', 60),), requires=(Completed('line_ploughs'),), cooldown=120),
    DecisionDef('drain_gangs', 'Put Drain Gangs on the Southern Track',
                'Clear the culverts under the southern section before the rains. Costs political power; repeatable twice a year.',
                30, (TimedIdea('track_drained', 120),), requires=(Completed('line_drains'),), cooldown=180),
    DecisionDef('fire_roster', 'Man the Firebreaks Through a Dry Spell',
                'Station crews and water tanks at the northern firebreaks for a season. Costs political power; repeatable yearly.',
                20, (TimedIdea('fire_roster', 120),), requires=(Completed('hinge_firebreaks'),), cooldown=365),
    DecisionDef('flood_callout', 'Call the Flood Companies Out',
                'Send the flood companies to the southern halts ahead of the rains. Costs political power; repeatable twice a year.',
                25, (Stability(0.02), XP('army', 10)), requires=(Completed('guard_flood_companies'),), cooldown=180),
    DecisionDef('plate_auction', 'Auction a Season of Plate Abroad',
                'Sell a season of surplus plate to foreign yards by auction. Costs political power; repeatable once a year.',
                35, (TimedIdea('plate_season', 180),), requires=(Completed('steel_count'),), cooldown=365),
    DecisionDef('dredge_inlet', 'Dredge the Northern Inlet',
                'Dredge the forest inlet in District A so that larger freighters can reach the quay. Costs political power; once '
                'only.', 60, (Build('infrastructure', 1, 359), Research('naval_equipment', 0.5, 1)),
                requires=(Completed('coast_quay'),)),
)
