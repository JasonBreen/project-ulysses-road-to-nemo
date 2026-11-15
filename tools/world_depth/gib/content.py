"""Gibraltar (GIB): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (neutrality ruling at 100 percent, elections not allowed,
the unnamed National Administration office), the Gibraltar Mining Zone country name, the two 1991 states West
Gibraltar and East Gibraltar with their buildings, resources, terrain and railway, the startup resource rights held
for Arklith and Aurelia, and the land neighbours computed from the province map. Official: Chronicle rows used only
as date anchors for distant pressure. Everything else, including every choice, office, idea, building, decision and
event in the zone, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='GIB', name='Gibraltar', root='world', package='gib',
                  themes=('tools', 'rail', 'navy'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party neutrality with neutrality popularity 100; election_frequency 48 and '
           'elections_allowed = no; stability and war support 0.5; three research slots; starting technologies include '
           'tech_mountaineers, infantry_at, early_fighter and basic_train. Starting leader GIB_ac_government_office, '
           'localised National Administration (centrism_na), whose description says its 1991 holder has not been '
           'established. Country name for neutrality: Gibraltar Mining Zone. Research focus Physical Sustainment. The tree '
           'never names a holder and never removes or edits these.',
           'mod/2985041246/history/countries/GIB - Gibraltar.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Geography: state 118 West Gibraltar (capital, state_category town, four shared slots with arms_factory 2 and '
           'industrial_complex 1, so one free; infrastructure 2; provinces 897 plains, 1799 and 3350 mountain, 4005 hills, '
           '4463 coastal urban with naval base 8, a supply node and victory point 20 localised Gibraltar City; resources '
           'steel 25, tungsten 23, chromium 19, aluminium 16, oil 2, rubber 2). State 610 East Gibraltar (rural, two shared '
           'slots both used by arms_factory 1 and industrial_complex 1; infrastructure 2; landlocked provinces 2099, 3201 and '
           '3562 plains, 3401 mountain, 4299 hills; supply node 2099; tungsten 21, chromium 14, aluminium 13, steel 10, oil 2, '
           'rubber 1). A level-3 railway runs 4463-897-4005-1799-3401-2099; level-2 lines run from 4463 to Marcil (9660, '
           'Arklith del Sur) and to Aurelian province 2041, and from 2099 toward Llano de Arklith (9652) and Aurelian province '
           '939. Land neighbours ARK to the north (via 140 and 241), AUR to the south (via 49 and 95) and LEA to the east (via '
           '170), sea to the west, computed from map/provinces.bmp and province centroids. Place names only from existing '
           'state and victory point localisation.',
           'mod/2985041246/history/states/118-State_118.txt; mod/2985041246/history/states/610-State_610.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/supply_nodes.txt; mod/2985041246/map/definition.csv'),
    Source('Mod provenance',
           'Startup resource rights: on_startup gives Arklith the resource rights of state 610 (East Gibraltar) and Aurelia '
           'those of state 118 (West Gibraltar). The tree treats these as standing concessions, negotiates only the zone '
           'side of the terms through ideas, and never removes or transfers the rights.',
           'mod/2985041246/common/on_actions/ac_on_actions.txt'),
    Source('Mod provenance',
           'Neighbour context only: the Arklith tree names the Gibraltar Mining Zone on the southern edge of Arklith del Sur, '
           'run by its own mining administration, and offers a haul road toward the Marcil quays if the zone wants one '
           '(ARK_wd_fro_gibraltar_road). Aurelia and Leasath in 1991: democratic ruling party with neutrality 48 and fascism '
           '50 percent popularity, elections suspended. No zone role in any neighbour affair is claimed and no border, '
           'core or faction changes.',
           'tools/world_depth/ark/content.py; mod/2985041246/history/countries/AUR - Aurelia.txt; '
           'mod/2985041246/history/countries/LEA - Leasath.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small territorial and merchant receiving service; 2 civilian '
           'and 3 military factories, no dockyard; 2 infantry formations (4 battalions); stocks of 800 infantry equipment, '
           '560 motorized equipment and 24 trains; 60 convoys; combat air and combat navy deliberately absent; infantry-only '
           'service without engineer or artillery companies. Fiscal calibration GDP 62.978 billion, debt ratio 0.3, '
           'collection 0.85; executive_office institution, capacity 40. Fictional gameplay calibration, not canon '
           'national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/economy_v2/profiles.json; tools/institutions/profiles.json'),
    Source('Official', 'Date anchor: the IAU announces that the asteroid Ulysses may strike the Earth. No zone role is claimed.',
           '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gibraltar takes no part; only price pressure is gameplay.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty signed in Lumen ends the Belkan War.', '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit. No impact in the zone is claimed.',
           '1999 / 07.08'),
    Source('Official', 'Date anchor: the FCU establishes the ISAF and the Usean Continental War follows. No zone role.',
           '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Gibraltar focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation, faction or resource-right effects; no new '
           'place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('charter_review', 'The Charter Under Review',
            'The zone charter has been read aloud, and every faction is drafting amendments.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('document', 'assembly')),
    IdeaDef('holders_compact', 'The Holders at the Table',
            'Concession firms, hauliers and port agents sit with the Administration on every decision.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_gain': 0.05, 'stability_factor': -0.02},
            ('economy', 'assembly')),
    IdeaDef('district_chamber', 'A Chamber in Prospect', 'Both districts are preparing to elect a chamber of their own.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('pit_delegates', 'Delegates from the Pits', 'Shift councils send delegates to every meeting of the Administration.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('tools', 'assembly')),
    IdeaDef('engineers_code', 'The Engineers Code', 'Technical staff are rebuilding the Administration around published standards.',
            {'research_speed_factor': 0.03, 'political_power_gain': 0.05}, ('science', 'document')),
    IdeaDef('payroll_trim', 'A Trimmed Payroll', 'The board has merged offices and sold the vehicles nobody could account for.',
            {'political_power_factor': 0.08, 'stability_factor': -0.02}, ('document', 'economy')),
    IdeaDef('voted_budget', 'The Voted Budget', 'Every line of the zone budget has passed the elected chamber.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'scales')),
    IdeaDef('safety_stewards', 'Stewards Below Ground', 'An elected safety steward on every shift may stop work.',
            {'stability_factor': 0.06, 'production_factory_efficiency_gain_factor': -0.02}, ('security', 'tools')),
    IdeaDef('posted_standards', 'Standards on the Wall', 'Every office and pithead displays the same technical rules.',
            {'production_factory_efficiency_gain_factor': 0.04, 'research_speed_factor': 0.02}, ('document', 'tools')),
    IdeaDef('zone_statute', 'The Zone Statute', 'One written statute says who licenses, who taxes and who governs.',
            {'stability_factor': 0.06, 'political_power_factor': 0.06}, ('scales', 'assembly')),
    # concessions
    IdeaDef('tonnage_books', 'Weighbridge Books', 'Independent clerks record every wagon of ore that leaves the zone.',
            {'political_power_gain': 0.05, 'production_factory_efficiency_gain_factor': 0.02}, ('document', 'tools')),
    IdeaDef('royalty_compact', 'The Royalty Compact', 'Indexed royalties and fixed obligations agreed with the rights holders.',
            {'political_power_gain': 0.10, 'consumer_goods_factor': -0.03}, ('diplomacy', 'economy')),
    IdeaDef('zone_ore_company', 'The Zone Ore Company', 'A public company hauls, sorts and sells the zone share of the ore.',
            {'production_speed_industrial_complex_factor': 0.08, 'political_power_gain': -0.05}, ('economy', 'industry')),
    IdeaDef('royalty_bench', 'The Royalty Bench', 'Grade and payment disputes go to a standing arbitration bench.',
            {'stability_factor': 0.03, 'political_power_factor': 0.05}, ('scales', 'diplomacy')),
    IdeaDef('company_haulage', 'Company Haulage', 'The ore company runs the wagons on the main line.',
            {'production_speed_infrastructure_factor': 0.10, 'production_factory_efficiency_gain_factor': 0.03}, ('rail', 'economy')),
    IdeaDef('graded_tungsten', 'Graded Tungsten', 'Sorting sheds sell tungsten by grade rather than as rubble.',
            {'consumer_goods_factor': -0.03, 'production_factory_max_efficiency_factor': 0.02}, ('tools', 'economy')),
    IdeaDef('chromium_stock', 'The Chromium Shed', 'Chromium is stored dry, counted and held back when prices are poor.',
            {'industrial_capacity_factory': 0.03}, ('industry', 'shelter')),
    IdeaDef('dam_inspectorate', 'The Dam Inspectorate', 'Engineers inspect every tailings embankment each year.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.02}, ('security', 'rebuild')),
    IdeaDef('punctual_royalties', 'Royalties on Schedule', 'Concession income arrives on published dates.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('economy', 'document')),
    # towns
    IdeaDef('town_rolls', 'The Town Rolls', 'A complete roll of households, wells and classrooms in both districts.',
            {'stability_factor': 0.02}, ('document', 'civil')),
    IdeaDef('dust_clinics', 'Dust Clinics', 'Pithead clinics screen lungs and treat injuries.',
            {'stability_factor': 0.04}, ('medical', 'tools')),
    IdeaDef('company_housing', 'Company Housing', 'Firms build and lease homes beside their shafts.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': -0.02}, ('civil', 'economy')),
    IdeaDef('housing_trusts', 'Town Housing Trusts', 'Public trusts own and let homes in every town.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.02}, ('civil', 'assembly')),
    IdeaDef('market_hall', 'The Station Market', 'Farmers from both districts sell under one roof by the station.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('economy', 'rail')),
    IdeaDef('pension_chest', 'The Pension Chest', 'A levy on every tonne pays retired and injured miners.',
            {'stability_factor': 0.04, 'war_support_factor': 0.02}, ('medical', 'economy')),
    # harbour
    IdeaDef('harbour_office', 'The Harbour Office', 'One office surveys and allocates every berth in Gibraltar City.',
            {'consumer_goods_factor': -0.02}, ('navy', 'document')),
    IdeaDef('free_port', 'A Free Harbour', 'Goods landed, stored or repacked in the harbour pay no duty until they move on.',
            {'consumer_goods_factor': -0.05, 'stability_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('bonded_terminal', 'The Bonded Terminal', 'Ore and mining equipment wait under customs seal until they sail.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('security', 'logistics')),
    IdeaDef('pilot_service', 'Pilots of the Western Approaches', 'Licensed pilots bring every ore carrier through the approaches.',
            {'navy_org_factor': 0.04, 'naval_speed_factor': 0.03}, ('navy', 'training')),
    IdeaDef('harbour_patrol', 'Harbour Patrol Launches', 'Police and customs launches cover the waterfront day and night.',
            {'naval_coordination': 0.04}, ('security', 'navy')),
    IdeaDef('return_cargoes', 'Return Cargoes', 'Ore carriers arrive with fuel, cement and machinery instead of ballast.',
            {'consumer_goods_factor': -0.03, 'production_speed_buildings_factor': 0.03}, ('logistics', 'economy')),
    # rail
    IdeaDef('line_inspectors', 'The Line Inspectorate', 'Inspectors walk the ore line and report every defect.',
            {'production_speed_infrastructure_factor': 0.05}, ('rail', 'document')),
    IdeaDef('open_access_line', 'Open Access Track', 'Any licensed operator may run trains for a published fee.',
            {'production_speed_infrastructure_factor': 0.10, 'consumer_goods_factor': -0.02}, ('rail', 'economy')),
    IdeaDef('zone_line_operator', 'One Operator, One Dispatcher', 'A single public operator runs every train on the line.',
            {'supply_consumption_factor': -0.05, 'production_speed_infrastructure_factor': 0.08}, ('command', 'rail')),
    IdeaDef('northern_timetable', 'The Northern Timetable', 'Wagons cross into Arklith on a shared timetable.',
            {'consumer_goods_factor': -0.02}, ('rail', 'diplomacy')),
    IdeaDef('southern_timetable', 'The Southern Timetable', 'Wagons cross into Aurelia on a shared timetable.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.01}, ('diplomacy', 'rail')),
    IdeaDef('signalled_line', 'A Signalled Line', 'Electric block signals protect every section of single track.',
            {'supply_consumption_factor': -0.05, 'planning_speed': 0.05}, ('communications', 'rail')),
    # territorial service
    IdeaDef('territorial_service', 'The Four-Battalion Service', 'Four infantry battalions guard two districts and answer emergencies.',
            {'army_core_defence_factor': 0.04}, ('training', 'security')),
    IdeaDef('pass_guard', 'Guardians of the Passes', 'Prepared posts and cave stores hold the hill passes on foot.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.04}, ('security', 'tools')),
    IdeaDef('motor_column', 'The Motor Column', 'Trucks and trains move a small force to any town on the line in hours.',
            {'army_speed_factor': 0.05, 'army_org_factor': 0.04}, ('logistics', 'security')),
    IdeaDef('rescue_companies', 'Rescue Companies', 'Two service companies trained for flooded and collapsed galleries.',
            {'stability_factor': 0.02, 'training_time_army_factor': -0.05}, ('medical', 'security')),
    IdeaDef('ridge_marches', 'Ridge Marches', 'Battalions march the western ridges in every season.',
            {'experience_gain_army_factor': 0.08, 'attrition': -0.05}, ('training', 'tools')),
    IdeaDef('railhead_depot', 'The Railhead Depot', 'A guarded service depot at the eastern railhead.',
            {'supply_consumption_factor': -0.05}, ('logistics', 'document')),
    IdeaDef('shift_reserve', 'The Shift Reserve', 'Shift workers train with the service for two weeks a year.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.04}, ('training', 'civil')),
    # neighbours
    IdeaDef('frontier_office', 'The Frontier Office', 'One office holds every agreement with the three neighbours.',
            {'political_power_gain': 0.05}, ('diplomacy', 'document')),
    IdeaDef('open_ore_market', 'Ore for Lawful Buyers', 'The zone share of the ore goes to the best lawful bid.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.01}, ('economy', 'diplomacy')),
    IdeaDef('neighbour_contracts', 'Contracts Next Door', 'Long supply contracts with Arklith and Aurelia at fixed prices.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.02}, ('diplomacy', 'scales')),
    IdeaDef('crossing_hours', 'Agreed Crossing Hours', 'Posts on the Leasath frontier keep the same hours and lists.',
            {'stability_factor': 0.02}, ('peace', 'diplomacy')),
    IdeaDef('war_premium', 'Wartime Ore Prices', 'Wartime prices for tungsten and chromium, and wartime insurance with them.',
            {'political_power_gain': 0.15, 'stability_factor': -0.02}, ('economy', 'communications')),
    IdeaDef('price_discipline', 'Price Discipline', 'No war price is ever again budgeted as income.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('peace', 'scales')),
    IdeaDef('neutral_statute', 'Statutory Neutrality', 'Neutrality is written into the law of the zone.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.03}, ('peace', 'document')),
    # Ulysses
    IdeaDef('impact_board', 'The Impact Board', 'Engineers, doctors and railway officials plan for Ulysses together.',
            {'stability_factor': 0.02, 'war_support_factor': 0.02}, ('meteor', 'assembly')),
    IdeaDef('gallery_shelters', 'Gallery Shelters', 'The best worked-out galleries are fitted as shelters.',
            {'static_anti_air_damage_factor': 0.05, 'stability_factor': 0.04}, ('shelter', 'tools')),
    IdeaDef('evacuation_trains', 'Evacuation Trains', 'Every engine and wagon held ready to move a threatened town.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('rail', 'refugees')),
    IdeaDef('stocked_galleries', 'Stocked Galleries', 'Sealed crates of food, water and medicine wait in the deep levels.',
            {'stability_factor': 0.03}, ('shelter', 'logistics')),
    IdeaDef('evacuation_timetable', 'The Last-Week Timetable', 'Every station knows which train leaves first and for whom.',
            {'stability_factor': 0.02, 'planning_speed': 0.05}, ('rail', 'document')),
    IdeaDef('relief_desk', 'The Relief Desk', 'Trains and ships of the zone carry help to neighbours who ask.',
            {'political_power_gain': 0.08, 'stability_factor': 0.02}, ('refugees', 'rail')),
    # the last lot and the school of mines
    IdeaDef('alloy_works', 'The Alloy Works', 'Ferroalloy furnaces run on a long-term power contract.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': 0.02}, ('industry', 'economy')),
    IdeaDef('yard_order_book', 'The Yard Order Book', 'Ore carriers bring their repairs to the harbour yard.',
            {'industrial_capacity_dockyard': 0.05, 'naval_speed_factor': 0.02}, ('navy', 'economy')),
    IdeaDef('licence_panel', 'The Licence Panel', 'A published panel reviews every arms export.',
            {'production_speed_arms_factory_factor': 0.05, 'stability_factor': 0.02}, ('document', 'security')),
    IdeaDef('assay_office', 'The Assay Office', 'A public laboratory certifies the grade of every shipment.',
            {'research_speed_factor': 0.02, 'political_power_gain': 0.05}, ('science', 'document')),
    IdeaDef('mines_school', 'The School of Mines', 'Geology, surveying and metallurgy taught in the zone.',
            {'research_speed_factor': 0.04}, ('science', 'training')),
    IdeaDef('carbide_workshop', 'The Carbide Workshop', 'Local tungsten tipped onto local drill bits.',
            {'production_factory_max_efficiency_factor': 0.03, 'research_speed_factor': 0.02}, ('tools', 'science')),
    # the turn of the century
    IdeaDef('seat_formula', 'The Seat Formula', 'Board seats follow tonnage, employment and royalties paid.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('economy', 'assembly')),
    IdeaDef('settled_chamber', 'A Settled Chamber', 'The district chamber has survived its second election.',
            {'stability_factor': 0.05, 'research_speed_factor': 0.02}, ('ballot', 'civil')),
    IdeaDef('delegate_congress', 'The Delegate Congress', 'Delegates from every shaft, yard and quay meet in full congress.',
            {'stability_factor': 0.05, 'political_power_gain': -0.05, 'production_factory_efficiency_gain_factor': 0.02},
            ('tools', 'ballot')),
    IdeaDef('audited_directorate', 'An Audited Directorate', 'Outside auditors have read the directorate and published their findings.',
            {'political_power_factor': 0.06, 'stability_factor': 0.03}, ('scales', 'science')),
    IdeaDef('renewed_compact', 'The Renewed Compact', 'A second term of the royalty compact with better indexation.',
            {'political_power_gain': 0.10, 'consumer_goods_factor': -0.02}, ('diplomacy', 'document')),
    IdeaDef('renewed_wagons', 'Renewed Wagons', 'A bond-financed wagon fleet for the ore company.',
            {'production_speed_infrastructure_factor': 0.10, 'supply_consumption_factor': -0.03}, ('rail', 'economy')),
    IdeaDef('ore_fund', 'The Ore Fund', 'Part of every year of royalties is saved abroad for lean years.',
            {'stability_factor': 0.04, 'political_power_factor': 0.04}, ('economy', 'scales')),
    IdeaDef('home_works', 'Royalties at Home', 'Royalties are spent each year on schools, clinics and roads.',
            {'consumer_goods_factor': -0.04, 'production_speed_buildings_factor': 0.05}, ('rebuild', 'civil')),
    IdeaDef('second_charter', 'The Second Charter', 'A revised charter sets the questions for the next ten years.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05}, ('document', 'assembly')),
    # decisions
    IdeaDef('ore_rush', 'Extra Ore Trains', 'Every spare engine and wagon is running ore this season.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': -0.02}, ('rail', 'industry')),
    IdeaDef('charter_season', 'Charter Season', 'Ore charters for the season have been auctioned on the register.',
            {'consumer_goods_factor': -0.03}, ('navy', 'economy')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('concession_board', 'Board of the Concession Holders',
           'A governing board of nominees from the operating firms, the ore hauliers and the port agents, ruling the zone '
           'collectively as a managed estate with elections kept off the calendar. Provisional gameplay office with no '
           'named holder.',
           'neutrality', 'oligarchism'),
    Office('district_assembly', 'Elected Council of West and East Gibraltar',
           'A cabinet named by a chamber elected in both districts, governing collectively and answering for its budget on '
           'a fixed electoral calendar. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('pit_councils', 'Federation of Pit Councils',
           'A rotating executive committee chosen by delegates from every shaft, quarry, railyard and quay, governing with '
           'safety placed above output. Provisional gameplay office with no named holder.',
           'communism', 'democratic_socialism'),
    Office('zone_directorate', 'Directorate of Mines and Works',
           'The National Administration reconstituted as a directorate of engineers and auditors appointed on published '
           'criteria, governing by technical order without elections. Provisional gameplay office with no named holder.',
           'neutrality', 'conservatism_na'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('zone_charter', 'The Charter on the Station Steps', (
        "The reading takes most of a morning. From the main station staircase in Gibraltar City, a clerk of the National "
        "Administration reads the zone's founding charter aloud, clause by clause, while ore trains shunt behind the "
        "crowd. Much of the charter concerns rights of way, weighbridges and the duties of shaft owners. Very "
        "little of it concerns who governs, because when it was written nobody thought the question mattered.",
        "It matters now. The operating firms that work the concessions in both districts already make most of the "
        "decisions that shape daily life, from shift patterns to the rent on company houses. The shift councils in the "
        "pits have grown from bargaining committees into something close to local governments. In the port city, "
        "shopkeepers and railwaymen ask why a place with its own harbour, railway and treasury has no vote on any of them.",
        "The Administration has chosen to put the question in the open rather than wait for it to be forced. What it "
        "cannot settle alone is the method: who gets to speak, and for how long. A public inquiry would let every faction speak and would "
        "take a year. A closed commission of senior officials would report within weeks, and nobody outside the room "
        "would trust a word of it.",
    ), (
        Option('Hold a public inquiry.', (Stability(0.02), PP(-15))),
        Option('Appoint a closed commission.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('concession_terms', 'Two Rights, One Weighbridge', (
        "The first month of independent weighbridge records lands on the Administration's table, and the figures do not "
        "match what the firms reported. The gap is not dramatic: a few percent here, a misclassified grade there, a week "
        "when the eastern scales were mysteriously out of order. Added up over a year, it comes to roughly what the zone "
        "would need to run clinics in every pit town.",
        "The ore rights in West Gibraltar are held for Aurelia and those in East Gibraltar for Arklith, and both "
        "arrangements are older than anyone now in office. The operating firms insist the differences are honest errors "
        "of measurement and offer to recalibrate every scale at their own expense. The towns, which heard about the gap "
        "from the railwaymen who load the wagons, want the missing money paid back.",
        "Nothing in the rights themselves is in question, and the Administration has no wish to make it so. The question "
        "is how hard to press. A formal audit of past shipments would recover part of the shortfall and sour relations "
        "with both holders for a season. Accepting the recalibration and starting afresh would keep the peace and write "
        "the past off.",
    ), (
        Option('Order a formal audit of past shipments.', (PP(-20), Event('royalty_audit', 30))),
        Option('Accept recalibration and start afresh.', (Stability(0.01), PP(25))),
    ), picture=1),
    EventDef('royalty_audit', 'The Weighbridge Audit Returns', (
        "The auditors spend a month in the firms' offices and the railway's ledgers, matching every wagon number against "
        "every shipping manifest they can find. Their report is careful and unexciting. Most of the shortfall is real but "
        "small, spread over years of sloppy weighing rather than any single scheme. One haulage contractor, however, "
        "billed the same trains twice through three seasons.",
        "The operating firms accept the findings with visible relief, since the report clears them of the worst rumours. "
        "They offer to settle the measured shortfall in instalments over three years. The contractor's case is different: "
        "the evidence is plain, the sum is large enough to matter and the contractor has friends in both districts who "
        "would much prefer that it went away quietly.",
        "What the audit was for is now the Administration's problem. Pursued in public, the double billing would show the "
        "towns that the weighbridge books have teeth, though the dispute would drag on for months. Settled behind closed "
        "doors, it would recover most of the money at once and leave the impression that the zone still prefers a quiet "
        "life to honest accounts.",
    ), (
        Option('Pursue the double billing in public.', (Stability(0.02), PP(-15))),
        Option('Settle quietly and bank the money.', (PP(40), Stability(-0.01))),
    ), picture=1),
    EventDef('pit_towns', 'The Roll of the Pit Towns', (
        "Clerks who went door to door in both districts bring back the first complete roll of the zone's households in "
        "living memory. Most people live in West Gibraltar, crowded into the port city or into hill towns beside the shafts. "
        "East Gibraltar's settlements are smaller and farther apart, strung along the railway across the plains, and few "
        "of them have changed shape in decades.",
        "The roll puts figures on things the towns had only grumbled about. Several hill towns share one doctor between them. "
        "Many homes belong to the firms that employ the families living in them. Schools close after the morning shift "
        "because no teacher can be found for the afternoon. In the east, wells near the mine drainage are turning bitter, "
        "and families haul water from the station tanks.",
        "The Administration now holds evidence that every faction will quote. The firms will say the towns are better "
        "than they were. The shift councils will say they are worse than anyone admits. Publishing the full roll would "
        "open a quarrel over blame that could run for years. Keeping the details for planning would avoid that argument and "
        "leave the towns guessing what the clerks found.",
    ), (
        Option('Publish the full roll.', (Stability(0.03), PP(-20))),
        Option('Keep the details for planning.', (PP(30), Stability(-0.01))),
    ), picture=0),
    EventDef('ore_ships', 'Eleven Ships at Anchor', (
        "On the morning the harbour survey begins, eleven ore carriers lie at anchor off Gibraltar City waiting for a "
        "berth, some of them for the fifth day. Their owners are paying for every idle hour, and the cost finds its way "
        "back into the price the zone receives for its ore. The harbour master has a long list of reasons, and all of "
        "them are true.",
        "The port was built on a scale the zone has never filled. A large naval base sits mostly idle, kept up for a "
        "fleet that does not exist, while the commercial berths are crowded and short of cranes. Pilots are informal, the "
        "approach charts are old and fog closes the harbour for days every year. Ore arrives by rail faster than the "
        "ships can be loaded.",
        "The survey team must decide where to look first. The naval base has deep water and long quays that could be "
        "turned to commercial use, but converting them means admitting the zone will never need them for anything else. "
        "The commercial berths could be improved where they stand, more cheaply and more slowly. The shipowners want an "
        "answer before next season's charters are signed.",
    ), (
        Option('Open the naval quays to ore ships.', (XP('navy', 10), PP(-10))),
        Option('Improve the commercial berths first.', (Stability(0.01), Research('logistics_tech', 0.5, 1))),
    ), picture=2),
    EventDef('ore_grade', 'Inspectors on the Mountain Grade', (
        "The line inspectors come back from three weeks on foot with notebooks full of bad news. The ore line climbs out "
        "of Gibraltar City through the western hills, crosses the mountain ground between the districts on a steep and "
        "badly drained grade, and runs out across the eastern plains to the railhead. Almost all of the zone's wealth "
        "travels along it, and much of the line is tired.",
        "On the grade, rotten sleepers sit in ballast that washes out with every storm. Culverts are choked with spoil "
        "from old workings. Trains run on paper orders handed between stations, and the telephone between two of those "
        "stations has been dead for a month. The dispatchers have kept traffic moving through skill and luck, and both "
        "are wearing thin.",
        "The report asks for money the zone has not budgeted, and it asks for a decision first: whether the line is a "
        "public road anyone may use or a single machine run by one operator. Before that argument begins, the "
        "Administration has to choose who reads the report first, knowing that commuters ride the same rails as the "
        "ore and will want to know why their trains run late.",
    ), (
        Option('Publish the inspectors report.', (Stability(-0.01), Research('train_tech', 0.5, 1))),
        Option('Brief the firms and the dispatchers only.', (PP(30),)),
    ), picture=1),
    EventDef('service_muster', 'Four Battalions on One Ground', (
        "All four battalions of the territorial service assemble together on a parade ground beside the port railway, "
        "something no officer now serving has seen before. Officers count rifles, trucks and boots, and then count them again. The service exists "
        "to guard two small districts and to help when the mines or the weather turn deadly. It has no aircraft, no "
        "artillery and no engineers of its own.",
        "The muster finds the service in better shape than its critics claimed and worse than its officers hoped. Rifles "
        "are clean and most trucks run, but spare parts are scarce and the trains assigned to the service are shared with "
        "the ore traffic. Many soldiers are miners on short contracts, strong and willing and half trained. Morale is "
        "good whenever there is something useful to do.",
        "The officers want a doctrine, and two are on offer: hold the hills on foot, or move along the railway and roads "
        "by truck. Before choosing, the service has to settle what the zone hears about the muster. A frank public report "
        "might win sympathy and perhaps money. A confidential one would spare the service embarrassment and tell the "
        "neighbours nothing at all.",
    ), (
        Option('Publish a frank report.', (WarSupport(0.03), Stability(-0.01))),
        Option('Keep the findings among the officers.', (XP('army', 15), PP(10))),
    ), picture=2),
    EventDef('three_neighbours', 'Letters from Three Capitals', (
        "The new frontier office opens its files and finds that the zone's foreign relations consist mostly of letters. "
        "Letters from Arklith about wagons and customs hours. Letters from Aurelia about royalties, food shipments and the "
        "port. Letters from Leasath about herders, grass fires and the occasional lost truck. Each was answered by "
        "whichever office happened to receive it, and few of the answers agree.",
        "The zone's position is unusual. Its ore rights are held for the two larger neighbours, one in each district, so "
        "both have a direct interest in calm. Leasath holds no rights and shares only the eastern frontier. The western "
        "sea brings everyone else. Nobody threatens the zone and nobody consults it either; it is treated as an address "
        "that ore comes from.",
        "The office proposes to change that, modestly. It can begin by writing to all three capitals to explain what the "
        "office is and what it will handle, or it can quietly gather the files and learn before announcing anything. "
        "Openness would reassure the neighbours. Discretion would let the zone decide what it wants before others decide "
        "for it.",
    ), (
        Option('Write to all three capitals.', (Stability(0.02), PP(-10))),
        Option('Learn first and announce later.', (PP(30), Stability(-0.01))),
    ), picture=0),
    EventDef('far_war', 'War Metals', (
        "Late in March 1995 the radio bulletins in the station cafes begin to lead with Belka. A war has started there, "
        "far beyond any frontier the zone shares, and Gibraltar has no part in it. Within a week the bulletins matter less "
        "than the telephone, which rings with brokers from cities the port agents have never traded with.",
        "Tungsten and chromium harden armour, gun barrels and machine tools, and the brokers want as much as the zone can "
        "ship. Prices quoted down the line are double the last contract. Some callers are vague about where the ore will "
        "end up. The operating firms are delighted, the shift councils want the windfall shared at the pithead, and marine "
        "underwriters add a war surcharge to every voyage out of Gibraltar City.",
        "The Administration controls only the zone's own share of the ore, but that share is enough to matter. It can "
        "sell at the new prices to any buyer who shows lawful papers, or it can refuse every broker who will not name the "
        "final customer and accept a smaller premium. Whichever it chooses, the brokers will remember, and so will the "
        "neighbours.",
    ), (
        Option('Sell to any buyer with lawful papers.', (PP(40), Stability(-0.02))),
        Option('Refuse brokers who will not name the customer.', (Stability(0.02), WarSupport(-0.01))),
    ), citation='date anchor only, Chronicle row 1995 / 03.25 (tools/lore/chronicle.json); the zone response is gameplay',
        picture=1),
    EventDef('ulysses_notice', 'Ulysses Comes to the Pit Towns', (
        "Ulysses entered the zone's vocabulary with the IAU warning at the end of 1994, as a remote possibility discussed "
        "in the newspapers. The FCU announcement of 20 April 1996 removes the comfort of doubt: impact is certain and "
        "governments are urged to act. Where the pieces will land is still unknown. The zone must ready itself for a blow "
        "whose target is a blank on every map.",
        "In the pit towns the reaction is practical before it is fearful. Miners know more about living underground than "
        "anyone, and within days the cafes are arguing over which old galleries would hold. Railwaymen point out that the "
        "ore line could move a whole town in an afternoon if it had to. Shopkeepers sell out of candles and tinned meat.",
        "The engineers will need months to weigh shelters against evacuation, and either costs more than any project the "
        "zone has attempted. The first decision is about who leads. Engineers appointed from the port city would work to "
        "one plan for both districts. Committees in each town would be slower and closer to the people they mean to "
        "shelter, and harder to overrule later.",
    ), (
        Option('Put the engineers in charge.', (PP(20), Research('construction_tech', 0.5, 1))),
        Option('Let each town form a committee.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, Chronicle rows 1994 / 12.10 and 1996 / 04.20 (tools/lore/chronicle.json); the zone '
                'preparations are gameplay', picture=2),
    EventDef('breakup', 'Streaks Over the Western Ridge', (
        "On 8 July 1999 tidal strain tears Ulysses to pieces as it passes within the Roche limit. Years of preparation "
        "compress into a few days "
        "of radio bulletins, siren tests and nights when whole towns stand outside looking up. The sky watch on the "
        "western ridge reports streaks and flashes it cannot place. The dispatchers keep every engine in steam and every "
        "crew on call.",
        "Bulletins from abroad arrive in pieces, like the asteroid itself, and many of them are frightening. In the zone "
        "the plans meet their test: doors close on the galleries or trains stand ready at every station, and people learn "
        "how long they can bear to wait. The miners, used to danger below ground, are calmer than the clerks who planned "
        "for them.",
        "When the immediate danger passes, standing the zone down becomes the Administration's next problem. It can release "
        "everyone at once and get the pits and the port working again, or keep the preparations in place for weeks in "
        "case later fragments follow. Each choice has a cost, and the neighbours are already asking whether the zone can "
        "spare help.",
    ), (
        Option('Stand down and reopen the pits.', (PP(30), Stability(-0.01))),
        Option('Keep the preparations in place.', (Stability(0.02), WarSupport(0.02))),
    ), citation='date anchor only, Chronicle row 1999 / 07.08 (tools/lore/chronicle.json); no impact in the zone is claimed',
        picture=2),
    EventDef('last_lot', 'Three Bids for One Lot', (
        "The planning office confirms what surveyors have said for years: West Gibraltar has room for one more large "
        "plant on serviced land near the harbour, and East Gibraltar has none. Everything else is hillside, shaft land or "
        "town. Three proposals have arrived for the last lot, and each has backers who believe the zone's future depends "
        "on them.",
        "A smelter would turn the zone's chromium and tungsten into alloys before export, keeping more of the value at "
        "home and burning a great deal of power. A ship repair yard would serve the ore carriers and use the port's idle "
        "deep water. An arms line would supply the territorial service and sell abroad, which the frontier office warns "
        "would test the zone's neutral reputation.",
        "Each bid promises jobs, and each has enemies. The operating firms oppose the smelter, the shipowners favour the "
        "yard and the service quietly lobbies for the arms line. The Administration must first decide how the choice will "
        "be made: at a public hearing where every backer argues in the open, or by its own planners behind closed doors.",
    ), (
        Option('Hold a public hearing on the bids.', (Stability(0.02), PP(-20))),
        Option('Let the planners decide.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('zone_yearbook', 'The First Yearbook of the Zone', (
        "Ten years of weighbridge books, census rolls, clinic records and train logs are bound together into the zone's "
        "first statistical yearbook. Clerks who spent the decade counting wagons and households finally see their numbers "
        "side by side. The result is a thick, plain volume with almost no adjectives in it, and it becomes the most "
        "argued-over book ever printed in Gibraltar City.",
        "The tables tell several stories at once. Tonnage is up and injuries are down. The line carries more with fewer "
        "breakdowns, and the port turns ships around faster. But the richest seams are measurably poorer than in 1991, "
        "the pit towns are older on average, and the zone's income still jumps and falls with prices set in places it "
        "has never seen.",
        "Every faction has found its favourite table. The firms quote output, the shift councils quote injuries and the "
        "towns quote rents. The open question is whether the yearbook becomes an annual publication, open to anyone "
        "who wants to check its claims, or a single volume that served its purpose and need never be repeated. The clerks, "
        "for their part, have already started counting the next year.",
    ), (
        Option('Publish it every year.', (Stability(0.02), PP(-20))),
        Option('Let it stand as a single volume.', (PP(35), Stability(-0.01))),
    ), picture=0),
    EventDef('usean_war', 'Insurers and the Usean War', (
        "The FCU founds the ISAF on 22 August 2003, and the Usean continent is at war, a world away from the "
        "zone. Gibraltar has no stake in the fighting and no forces anywhere near it. Its first contact with the war "
        "arrives by telex: notices from insurers raising premiums on any cargo that might pass near Usean waters.",
        "The hull register, kept for years as a dull clerical chore, suddenly matters. It shows which ships "
        "carrying the zone's ore and imports sail routes that might cross the danger, and which could be sent another way. "
        "Brokers call again with offers for tungsten and chromium, but this time the traders remember how quickly the "
        "last wartime prices vanished.",
        "The Administration can ask the shipowners on the register to avoid every route near the war, accepting longer "
        "voyages and higher costs. Or it can leave routing to the shipowners and their underwriters while it concentrates "
        "on keeping its own ore contracts steady. Neither choice touches the war itself. Both decide what reaches the port city and what "
        "leaves it, and both will be debated in the station cafes until the guns there fall silent.",
    ), (
        Option('Ask registered hulls to keep clear.', (Stability(0.02), PP(-15))),
        Option('Leave routing to the owners.', (PP(25), Stability(-0.01))),
    ), citation='date anchor only, Chronicle row 2003 / 08.22 (tools/lore/chronicle.json); the zone response is gameplay',
        picture=2),
)

# --- branches ------------------------------------------------------------------------------------
ZONE = Branch('zone', 'Who Signs for the Zone', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('zn_charter_read', 'The Charter Read at Gibraltar City',
          "In 1991 the Gibraltar Mining Zone is run by the National Administration, an executive office that answers "
          "to no voter and whose holder appears in no public record. Its founding charter has not been read aloud in a "
          "generation. Reading it in the port city, clause by clause, tells every pit town what the office claims to do and "
          "invites argument about all of it.",
          ('document', 'assembly'), reward=(Idea('charter_review'), Event('zone_charter'))),
    Focus('zn_powers_list', 'Clauses the Office Never Used',
          "Clerks compare the charter with what the Administration actually does. Some powers, such as setting royalties or "
          "licensing new shafts, drifted to the concession firms years ago. Others, like calling a district vote, were never "
          "used at all. Publishing the comparison costs the office some dignity and forces a choice about who should hold "
          "the powers nobody exercises.",
          ('scales', 'document'), after=('zn_charter_read',),
          reward=(PP(30), Tooltip('Opens four answers to who governs the zone; only one can be taken.'))),
    Focus('zn_board_path', 'Seats for the Concession Holders',
          "The operating firms, the ore hauliers and the port agents already decide most of what happens in the zone. One "
          "faction proposes to give them the formal seats as well, so that those who pay the royalties and employ the "
          "miners would govern in their own name. Decisions would follow the order books. Miners and townspeople would have no seat of "
          "their own.",
          ('economy', 'assembly'), after=('zn_powers_list',),
          exclusive=('zn_assembly_path', 'zn_council_path', 'zn_directorate_path'),
          reward=(SwapIdea('charter_review', 'holders_compact'),)),
    Focus('zn_assembly_path', 'Both Districts Elect a Chamber',
          "Townspeople in Gibraltar City and the eastern railhead towns ask for an elected chamber, with seats divided "
          "between West and East Gibraltar and a budget it must approve. Elections have no place on the zone calendar today. "
          "The firms fear royalty politics, the Administration fears losing its staff, and the chamber would inherit every "
          "grievance at once.",
          ('ballot', 'assembly'), after=('zn_powers_list',),
          exclusive=('zn_board_path', 'zn_council_path', 'zn_directorate_path'),
          reward=(SwapIdea('charter_review', 'district_chamber'),)),
    Focus('zn_council_path', 'The Pit Councils Ask for the Keys',
          "Each shaft and quarry has an informal council of shift leaders that bargains over pay, timbering and dust. Their "
          "delegates now ask for more than bargaining: the right to run the zone through a federation of those councils. "
          "Production decisions would be made by the people below ground. Investors would read it as the end of predictable "
          "royalties.",
          ('tools', 'assembly'), after=('zn_powers_list',),
          exclusive=('zn_board_path', 'zn_assembly_path', 'zn_directorate_path'),
          reward=(SwapIdea('charter_review', 'pit_delegates'),)),
    Focus('zn_directorate_path', 'Engineers Instead of Clerks',
          "A smaller camp inside the Administration wants to keep the unelected office but rebuild it around engineers, "
          "surveyors and accountants who publish their standards. Nobody would vote, but everyone could read the rules. It "
          "promises competence without a political fight. It also leaves the miners, the firms and the towns exactly as "
          "voiceless as they were before.",
          ('science', 'document'), after=('zn_powers_list',),
          exclusive=('zn_board_path', 'zn_assembly_path', 'zn_council_path'),
          reward=(SwapIdea('charter_review', 'engineers_code'),)),
    Focus('zn_board_seat', 'Install the Concession Board',
          "The board takes the seals of the Administration and governs collectively through nominees of the operating firms, "
          "hauliers and port agents. No vote is scheduled. Royalty disputes become internal business, settled quickly and "
          "quietly. Power passes to a collective office rather than to any individual, and every bad season will now be "
          "blamed on the board's ledgers.",
          ('economy', 'command'), after=('zn_board_path',), cost=10,
          exclusive=('zn_assembly_seat', 'zn_council_seat', 'zn_directorate_seat'),
          reward=(Regime('concession_board'), Flag('path_board'))),
    Focus('zn_assembly_seat', 'Seat the District Chamber',
          "Voters in both districts elect a chamber, which appoints a cabinet sharing responsibility for every line of "
          "spending. Polling days are set years ahead. The clerks of the old Administration become civil servants of an "
          "elected government. The firms gain an opponent that can be voted out and replaced, which they regard as both a "
          "risk and an opening.",
          ('ballot', 'command'), after=('zn_assembly_path',), cost=10,
          exclusive=('zn_board_seat', 'zn_council_seat', 'zn_directorate_seat'),
          reward=(Regime('district_assembly'), Flag('path_assembly'))),
    Focus('zn_council_seat', 'Federate the Pit Councils',
          "Delegates from every shaft, quarry, railyard and quay form a federation that takes over the Administration's "
          "offices. Its executive is a rotating committee with no named leader, and its first rule is that safety outranks "
          "output. The firms keep their concessions on paper, while their managers now negotiate with the people who used "
          "to take their orders.",
          ('tools', 'command'), after=('zn_council_path',), cost=10,
          exclusive=('zn_board_seat', 'zn_assembly_seat', 'zn_directorate_seat'),
          reward=(Regime('pit_councils'), Flag('path_councils'))),
    Focus('zn_directorate_seat', 'Commission the Directorate of Mines',
          "The National Administration is reconstituted as a directorate of mines and works, staffed by engineers and "
          "auditors appointed on published criteria. It governs by technical order and keeps elections off the calendar. "
          "Collective and unnamed, it promises that every rule will be written down. Critics answer that a written rule is "
          "still a rule nobody voted for.",
          ('science', 'command'), after=('zn_directorate_path',), cost=10,
          exclusive=('zn_board_seat', 'zn_assembly_seat', 'zn_council_seat'),
          reward=(Regime('zone_directorate'), Flag('path_directorate'))),
    Focus('zn_board_payroll', 'The Board Trims the Payroll',
          "Its opening move is an audit of the Administration's payroll, line by line, merging offices and selling vehicles "
          "nobody can account for. Costs drop by the next budget, and the board publishes the savings with some pride. The clerks "
          "who lost posts have long memories, and the pit towns notice that no board member took a cut.",
          ('document', 'economy'), after=('zn_board_seat',),
          exclusive=('zn_chamber_budget', 'zn_council_stewards', 'zn_directorate_standards'),
          reward=(Idea('payroll_trim'),)),
    Focus('zn_chamber_budget', 'Six Weeks Over the Zone Budget',
          "The chamber debates the zone budget in public for six weeks, and the final vote is close. Every royalty line, "
          "every rail subsidy and every clinic grant has a name attached to it. Business slows while deputies argue. When "
          "the budget passes it carries a legitimacy no decree ever had, and the firms find their lobbyists far busier.",
          ('ballot', 'scales'), after=('zn_assembly_seat',),
          exclusive=('zn_board_payroll', 'zn_council_stewards', 'zn_directorate_standards'),
          reward=(Idea('voted_budget'),)),
    Focus('zn_council_stewards', 'Safety Stewards Below Ground',
          "The federation places an elected safety steward on every shift, with authority to stop work when gas, water or "
          "bad timber threatens. Output drops in the first months as old hazards are finally fixed. Injuries drop too. The "
          "firms complain about lost tonnage; the miners stop complaining about funerals, and the federation's support "
          "hardens.",
          ('security', 'tools'), after=('zn_council_seat',),
          exclusive=('zn_board_payroll', 'zn_chamber_budget', 'zn_directorate_standards'),
          reward=(Idea('safety_stewards'),)),
    Focus('zn_directorate_standards', 'Standards Printed and Posted',
          "The directorate prints its technical standards for shafts, rail, harbour work and accounts, and posts them in "
          "every office and at every pithead. Inspectors carry the same booklet as the managers they inspect. Disputes "
          "shrink to questions of measurement. The rules are sound and dull, and people who never voted for them at least "
          "know what they say.",
          ('document', 'tools'), after=('zn_directorate_seat',),
          exclusive=('zn_board_payroll', 'zn_chamber_budget', 'zn_council_stewards'),
          reward=(Idea('posted_standards'),)),
    Focus('zn_zone_statute', 'A Statute for the Mining Zone',
          "Whichever office now governs, the zone needs one written statute that outlasts it: who may license a shaft, who "
          "sets the royalty floor, who declares an emergency and how the next government is chosen. Drafting it takes a "
          "year of quarrelsome sessions. The result is shorter than the old charter and much harder to ignore.",
          ('scales', 'assembly'), cost=10,
          after_any=('zn_board_payroll', 'zn_chamber_budget', 'zn_council_stewards', 'zn_directorate_standards'),
          reward=(Idea('zone_statute'), Stability(0.03))),
))

CONCESSIONS = Branch('concessions', 'Two Concessions, One Zone', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('cn_weighbridge', 'Tonnage Books at the Weighbridge',
          "Every wagon of ore leaving the zone crosses a weighbridge, yet nobody in the Administration keeps a complete "
          "record of what crossed. The firms do, and they report the totals that suit them. Clerks posted at each "
          "weighbridge, with sealed books and a copy sent to the port city every day, give the zone its first independent "
          "count of its own wealth.",
          ('document', 'tools'), reward=(Idea('tonnage_books'), Event('concession_terms'))),
    Focus('cn_west_terms', 'Reading the Western Concession',
          "The ore rights in West Gibraltar are held for Aurelia, and the operating terms were written long before the "
          "present staff arrived. Lawyers read every clause: royalty rates, haulage charges, what happens to tailings and "
          "who repairs the roads. Nothing in the rights changes. What changes is that the Administration finally knows "
          "what it signed.",
          ('scales', 'tools'), after=('cn_weighbridge',),
          reward=(Research('excavation_tech', 0.5, 1), Tooltip('Resource rights in West Gibraltar are unchanged.'))),
    Focus('cn_east_terms', 'Reading the Eastern Concession',
          "East Gibraltar's ore rights are held for Arklith, and its mines feed a line that runs north toward the Llano as "
          "easily as west to the port. The eastern terms are shorter and vaguer than the western ones. A careful reading "
          "finds royalty floors that were never indexed and road duties nobody has enforced since the rails went in.",
          ('scales', 'rail'), after=('cn_weighbridge',),
          reward=(Research('industry', 0.5, 1), Tooltip('Resource rights in East Gibraltar are unchanged.'))),
    Focus('cn_royalty_compact', 'A Royalty Compact with the Holders',
          "One answer accepts the concession model and negotiates a better price for it: indexed royalties, a share of every "
          "new seam and fixed obligations for roads, water and tailings. The holders keep operating, and the zone collects "
          "more and argues less. It ties the budget to foreign order books for another generation in exchange for "
          "predictable money.",
          ('diplomacy', 'economy'), after_any=('cn_west_terms', 'cn_east_terms'), cost=10,
          exclusive=('cn_ore_company',),
          reward=(SwapIdea('tonnage_books', 'royalty_compact'), Flag('model_compact'))),
    Focus('cn_ore_company', 'A Zone Ore Company',
          "The other answer builds a public ore company that takes over haulage, sorting and sales of the zone share, and "
          "bids for minority stakes in the operating firms wherever owners will sell. The rights stay with their holders. "
          "The company keeps more of the value inside the zone, at the price of capital it must borrow and managers it "
          "must train.",
          ('economy', 'industry'), after_any=('cn_west_terms', 'cn_east_terms'), cost=10,
          exclusive=('cn_royalty_compact',),
          reward=(SwapIdea('tonnage_books', 'zone_ore_company'), Flag('model_company'))),
    Focus('cn_royalty_bench', 'An Arbitration Bench for Royalties',
          "Under the compact, disputes over grades, weights and payment dates go to a standing bench of three arbitrators: "
          "one named by the holders, one by the zone and a third drawn at random from a published panel. Hearings are short and "
          "rulings are final. Lawyers lose a profitable trade, and the treasury gains a calendar it can plan around.",
          ('scales', 'diplomacy'), after=('cn_royalty_compact',), exclusive=('cn_company_haulage',),
          reward=(Idea('royalty_bench'),)),
    Focus('cn_company_haulage', 'The Company Takes the Haulage',
          "The ore company buys out the private haulage contracts on the main line and runs the wagons itself. Turnaround "
          "at the port improves once one dispatcher sees the whole line. The company also inherits every broken wagon and "
          "every grudge of the old contractors, and its first annual accounts show a loss its critics quote for years.",
          ('rail', 'economy'), after=('cn_ore_company',), exclusive=('cn_royalty_bench',),
          reward=(Idea('company_haulage'),)),
    Focus('cn_tungsten_grades', 'Grade the Tungsten Before Sale',
          "Tungsten is the richest of the zone's ores and the one most often sold as mixed rubble at the lowest grade. "
          "Sorting sheds at the railheads separate concentrate from waste before loading. Buyers pay more for a known grade. "
          "The sheds need power, water and trained sorters, and the first season's output falls while the crews learn.",
          ('tools', 'economy'), after=('cn_weighbridge',),
          reward=(TimedIdea('graded_tungsten', 730), Research('excavation_tech', 0.5, 1))),
    Focus('cn_chromium_shed', 'A Covered Shed for Chromium',
          "Chromium ore sits in open heaps at the eastern railhead, washing into ditches with every storm and losing weight "
          "to theft. A covered shed with a weighed gate keeps the stock dry and counted. It also lets the zone hold ore back "
          "when prices are poor, which the operating firms call interference and the treasury calls prudence.",
          ('industry', 'shelter'), after=('cn_tungsten_grades',), reward=(Idea('chromium_stock'),)),
    Focus('cn_tailings', 'Inspect the Tailings Dams',
          "Decades of washing ore have left tailings dams above several pit towns, each built by whichever firm needed one at "
          "the time. Engineers walk every embankment and drill test holes. Most are sound; two need buttressing before the "
          "next wet season. The repairs cost money nobody budgeted, and the report gives the towns reason to ask who is "
          "liable.",
          ('security', 'rebuild'), after=('cn_weighbridge',), reward=(Idea('dam_inspectorate'), PP(-15))),
    Focus('cn_royalties_banked', 'Royalties Paid on the Day',
          "Whichever model the zone chose, its income now arrives on a published schedule rather than whenever a firm's "
          "accountants felt generous. The treasury can borrow against it, pay contractors on time and stop begging the port "
          "for advances. Prompt money is not more money, but it changes how every office plans, and late payment becomes "
          "news.",
          ('economy', 'document'), after_any=('cn_royalty_bench', 'cn_company_haulage'),
          reward=(Idea('punctual_royalties'),)),
))

TOWNS = Branch('towns', 'Pit Towns and the Port City', 1992, 'FOCUS_FILTER_STABILITY', (
    Focus('tw_town_rolls', 'Rolls of the Pit Towns',
          "Most people in the zone live in West Gibraltar, around the port city and the hill shafts behind it; East "
          "Gibraltar is thinner, a string of plains settlements along the line. No office holds an accurate list of "
          "households, wells or classrooms. A house-to-house roll costs a season of clerks' time and gives every later plan "
          "its numbers.",
          ('document', 'civil'), reward=(Idea('town_rolls'), Event('pit_towns'))),
    Focus('tw_dust_clinics', 'Dust Clinics at the Pitheads',
          "Older miners cough, and younger ones are learning to. Small clinics at the largest pitheads screen lungs, treat "
          "injuries and keep records the firms never kept. Doctors must be recruited from abroad on high salaries for the "
          "first years. The records will eventually show which shafts are killing people, and that knowledge will not stay "
          "quiet.",
          ('medical', 'tools'), after=('tw_town_rolls',), reward=(Idea('dust_clinics'),)),
    Focus('tw_night_classes', 'Night Classes After the Shift',
          "Classrooms in the pit towns stand empty after dark, while shift workers who want to become electricians, "
          "surveyors or engine drivers have nowhere to learn. Teachers paid by the hour open evening courses in reading "
          "plans, basic chemistry and machine repair. Attendance is uneven and tired. The best students become the foremen "
          "the zone has always imported.",
          ('training', 'civil'), after=('tw_town_rolls',),
          reward=(Flag('night_classes'), Research('construction_tech', 0.5, 1))),
    Focus('tw_company_housing', 'Company Leases for Miners',
          "One housing answer lets the operating firms build and lease homes near their shafts, with rent taken from wages. "
          "Houses go up quickly and the firms keep their workers close. Tenants who lose their jobs lose their homes as "
          "well, and every strike becomes an eviction dispute. The Administration avoids the cost and gives up its say.",
          ('civil', 'economy'), after_any=('tw_dust_clinics', 'tw_night_classes'), exclusive=('tw_housing_trusts',),
          requires=(NotFlag('path_councils'),), reward=(SwapIdea('town_rolls', 'company_housing'),)),
    Focus('tw_housing_trusts', 'Housing Trusts in Every Town',
          "The alternative creates a public housing trust in each town, financed from royalties and governed by tenants and "
          "the town office. Building is slower, and the trusts borrow against future income. A miner who loses a job keeps "
          "a home, which makes miners harder to discipline and easier to keep. The firms see that difference "
          "clearly.",
          ('civil', 'assembly'), after_any=('tw_dust_clinics', 'tw_night_classes'), exclusive=('tw_company_housing',),
          requires=(NotFlag('path_board'),), reward=(SwapIdea('town_rolls', 'housing_trusts'),)),
    Focus('tw_east_water', 'Water Mains for the Eastern Towns',
          "Settlements on the eastern plains still draw water from shallow wells that mine drainage has started to spoil. A "
          "main laid along the rail corridor from cleaner springs in the hills serves the railhead towns first. Digging "
          "beside a working line needs careful scheduling with the dispatchers, and the trench doubles as a better service "
          "road.",
          ('rebuild', 'civil'), after=('tw_town_rolls',), reward=(Build('infrastructure', 1, 610), Stability(0.02))),
    Focus('tw_station_market', 'A Covered Market by the Station',
          "Market traders in Gibraltar City sell from carts in the station square, beside the ore trains, in every kind of "
          "weather. A covered hall with water, drains and stalls for rent gives farmers from both districts a reason to come "
          "in by train. It is a small building. It changes how the port city spends its Saturdays and its wages.",
          ('economy', 'rail'), after=('tw_east_water',), reward=(TimedIdea('market_hall', 730), Stability(0.01))),
    Focus('tw_pension_chest', 'A Pension Chest for Miners',
          "Miners rarely work past fifty, and those who leave the pits with damaged lungs depend on their children. A pension "
          "chest funded by a levy on every tonne gives retired and injured miners a small, certain income. The firms object "
          "to the levy. The towns notice that old men no longer haunt the station square selling their tools.",
          ('medical', 'economy'), after_any=('tw_company_housing', 'tw_housing_trusts'), reward=(Idea('pension_chest'),)),
    Focus('tw_ambulance_strip', 'An Air Ambulance Strip',
          "Serious injuries in the hill shafts still travel to the port city by truck along slow switchback roads. A graded "
          "strip outside Gibraltar City, with a hangar and a fuel store, lets a light aircraft carry the worst cases and fly "
          "specialists in. The zone has no air arm and wants none. It wants a faster road to a surgeon.",
          ('runway', 'medical'), after=('tw_dust_clinics',), reward=(Build('air_base', 1, 0), Stability(0.01))),
))

HARBOUR = Branch('harbour', 'The Harbour at Gibraltar City', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('hb_soundings', 'Soundings off Gibraltar City',
          "Gibraltar City is the zone's only port: a deep harbour on the western coast with a large naval base built for a "
          "fleet the zone does not have. Ore ships anchor offshore for days waiting for a berth. A survey of depths, berths "
          "and cranes shows how much of the harbour is used, how much stands idle and how much has silted up.",
          ('navy', 'document'), reward=(Idea('harbour_office'), Event('ore_ships'))),
    Focus('hb_ore_belt', 'A Covered Belt to the Ore Berth',
          "Ore still reaches the ships by grab cranes and open wagons, spilling dust over the waterfront and losing tonnage "
          "to every gust. A covered conveyor from the railway sidings straight to the main ore berth halves loading time and "
          "clears the air over the old town. The steel for the gantry must be bought abroad, which stings.",
          ('logistics', 'navy'), after=('hb_soundings',),
          reward=(Build('infrastructure', 1, 0), Research('logistics_tech', 0.5, 1))),
    Focus('hb_pilot_service', 'A Pilot Service for the Approaches',
          "Foreign masters bring ore carriers into a harbour they visit twice a year, guided by charts nobody has updated. A "
          "licensed pilot service with its own launches, trained on the approaches and the tides, cuts groundings and "
          "waiting times. Pilot fees add to the cost of calling at the zone, and shipowners mention them in every "
          "negotiation.",
          ('navy', 'training'), after=('hb_soundings',), reward=(Idea('pilot_service'), XP('navy', 10))),
    Focus('hb_hull_register', 'Sixty Hulls on the Register',
          "Around sixty merchant hulls trade under the zone's arrangements, carrying ore out and fuel, food and machinery in. "
          "Their papers are scattered among agents in several ports. A single register in Gibraltar City records each hull, "
          "its crew, its insurance and its usual route. In a quiet year this is paperwork. In a crisis it becomes a map.",
          ('document', 'navy'), after=('hb_soundings',), reward=(Flag('hull_register'), PP(10))),
    Focus('hb_free_port', 'Free Port Status for the Harbour',
          "Declaring the harbour a free port waives duties on goods that land, are stored or are repacked there before "
          "moving on. Traders from neighbouring countries could use Gibraltar City as their own warehouse by the sea. Duty "
          "revenue falls at once, while storage, handling and jobs may grow. Smugglers will certainly notice the change as "
          "well.",
          ('economy', 'navy'), after_any=('hb_ore_belt', 'hb_pilot_service'), cost=10, exclusive=('hb_bonded_terminal',),
          reward=(SwapIdea('harbour_office', 'free_port'),)),
    Focus('hb_bonded_terminal', 'A Bonded Ore Terminal',
          "The narrower answer keeps duties in place but creates a bonded terminal for ore, concentrates and imported mining "
          "equipment, sealed and supervised by customs. Holders and buyers can store and blend cargoes without paying until "
          "they sail. It serves the zone's own trade well and offers neighbours little. Customs officers like it; merchants "
          "find it timid.",
          ('security', 'logistics'), after_any=('hb_ore_belt', 'hb_pilot_service'), cost=10, exclusive=('hb_free_port',),
          reward=(SwapIdea('harbour_office', 'bonded_terminal'),)),
    Focus('hb_harbour_launches', 'Harbour Police Launches',
          "The zone keeps no combat navy and has no plan to build one. It does need boats that can fight a fire, chase a "
          "thief or escort a damaged ship to a berth. A handful of fast launches crewed by harbour police and customs "
          "officers cover the waterfront day and night, and their crews slowly learn the sea.",
          ('security', 'navy'), after=('hb_pilot_service',), reward=(Idea('harbour_patrol'), XP('navy', 5))),
    Focus('hb_approach_radar', 'Radar over the Harbour Approaches',
          "Fog rolls off the western sea for weeks each year, and ore ships wait outside rather than risk the approaches "
          "blind. A shore radar on high ground above the harbour, linked to the pilot station, lets masters come in on "
          "bearings and ranges. Traffic keeps moving in poor weather, and the harbour finally sees what lies offshore.",
          ('radar', 'navy'), after=('hb_harbour_launches',), reward=(Build('radar_station', 1, 0),)),
    Focus('hb_return_cargo', 'Return Cargoes for Ore Ships',
          "Ore carriers arrive at Gibraltar City nearly empty and leave full. Agents in the port now hunt for return cargoes: "
          "fuel, cement, timber, machinery and food the zone imports anyway. Filling empty holds lowers freight rates in both "
          "directions. It also makes the port city a trading place instead of a loading chute, with all the bargaining that "
          "brings.",
          ('logistics', 'economy'), after_any=('hb_free_port', 'hb_bonded_terminal'),
          reward=(TimedIdea('return_cargoes', 1095),)),
))

RAIL = Branch('rail', 'The Ore Line', 1993, 'FOCUS_FILTER_INDUSTRY', (
    Focus('rl_walk_line', 'Walk the Ore Line End to End',
          "One main line carries almost everything the zone produces, climbing from Gibraltar City through the western hills "
          "and mountains and dropping onto the eastern plains at the railhead. Inspectors walk every kilometre with hammers "
          "and notebooks, counting rotten sleepers, cracked rails and washed-out culverts. Their report is the first full "
          "picture of the line in years.",
          ('rail', 'document'), reward=(Idea('line_inspectors'), Event('ore_grade'))),
    Focus('rl_mountain_grade', 'Reballast the Mountain Grade',
          "The steepest section of the line crosses the mountain ground between the two districts, where ballast washes "
          "away each wet season and trains crawl at walking pace. Fresh ballast, new drainage and heavier rail on the grade "
          "let longer trains climb without a second engine. Work trains will block the line on many nights while it is "
          "done.",
          ('rail', 'tools'), after=('rl_walk_line',), reward=(Build('infrastructure', 1, 610), PP(-15))),
    Focus('rl_east_railhead', 'A Railhead Yard in the East',
          "Trains from the eastern mines are made up in a cramped yard where shunting blocks the main line for hours. A larger "
          "railhead yard with loops for full trains and sidings for empties lets the east load without stopping traffic. "
          "The yard also gives the territorial service a place to stage stores if it ever needs one.",
          ('rail', 'logistics'), after=('rl_mountain_grade',),
          reward=(Build('infrastructure', 1, 610), Flag('east_railhead'))),
    Focus('rl_port_sidings', 'Sidings Behind the Port',
          "At the western end, ore trains queue on the main line waiting for berths, and passenger trains queue behind them. "
          "New sidings behind the harbour hold full trains until a ship is ready. The land is cramped and some warehouses "
          "must be moved. The city's commuters will be the first to notice and the last to thank anyone.",
          ('logistics', 'rail'), after=('rl_walk_line',), reward=(Build('infrastructure', 1, 0), Stability(0.01))),
    Focus('rl_open_access', 'Open Access on the Ore Line',
          "Under open access, any licensed operator may run trains on the zone's track by paying a published fee per tonne "
          "and kilometre. Firms that want faster service can buy their own wagons and engines. The Administration becomes a "
          "track owner and timetable keeper. Service improves, and scheduling arguments become a weekly ritual at dispatch.",
          ('rail', 'economy'), after_any=('rl_east_railhead', 'rl_port_sidings'), cost=10, exclusive=('rl_zone_trains',),
          requires=(NotFlag('model_company'),), reward=(SwapIdea('line_inspectors', 'open_access_line'),)),
    Focus('rl_zone_trains', 'One Dispatcher for Every Train',
          "The opposite rule keeps the track and the trains under one public operator, with a single dispatcher who sees "
          "the whole line. Nobody else runs a train. Wagon supply becomes a planning question rather than a market. The firms "
          "lose the ability to buy faster service, and the dispatcher becomes the most powerful clerk in the zone.",
          ('command', 'rail'), after_any=('rl_east_railhead', 'rl_port_sidings'), cost=10, exclusive=('rl_open_access',),
          reward=(SwapIdea('line_inspectors', 'zone_line_operator'),)),
    Focus('rl_arklith_timetable', 'A Shared Timetable with Arklith',
          "Two branch lines leave the zone northward into Arklith, one from the port city toward Marcil and one from the "
          "eastern railhead toward the Llano. Their timetables were set separately and rarely meet. A joint timetable agreed "
          "with Arklith railway officials lets wagons cross without waiting a day at the frontier. Customs must keep the "
          "same hours.",
          ('rail', 'diplomacy'), after=('rl_walk_line',), reward=(TimedIdea('northern_timetable', 1095),)),
    Focus('rl_aurelia_timetable', 'A Shared Timetable with Aurelia',
          "Southward, short lines link the port city and the eastern plains with Aurelian districts across the frontier. "
          "Traffic is lighter than to the north but steadier, mostly food and fuel coming in. Matching timetables with "
          "Aurelian operators and opening a joint freight office at the crossing cuts the number of half-empty wagons "
          "standing idle on both sides.",
          ('diplomacy', 'rail'), after=('rl_walk_line',), reward=(TimedIdea('southern_timetable', 1095),)),
    Focus('rl_block_signals', 'Block Signals on the Single Track',
          "Most of the main line is single track, worked by paper train orders that depend on careful clerks and working "
          "telephones. Electric block signals with track circuits stop two trains entering the same section. Capacity rises "
          "and the worst kind of accident becomes far harder. Signal engineers must be trained, and copper thieves kept "
          "away.",
          ('communications', 'rail'), after_any=('rl_open_access', 'rl_zone_trains'),
          reward=(Idea('signalled_line'), Research('train_tech', 0.5, 1))),
))

SERVICE = Branch('service', 'The Territorial Service', 1993, 'FOCUS_FILTER_ARMY_XP', (
    Focus('sv_muster', 'Muster the Four Battalions',
          "The zone's armed force is a territorial service of four infantry battalions in two formations, with trucks, rifles "
          "and trains but no aircraft, artillery or engineers. Its job is to guard two districts and help when the mines or "
          "the weather turn deadly. A full muster shows who turns up, what works and what has quietly rusted.",
          ('training', 'security'), reward=(Idea('territorial_service'), Event('service_muster'))),
    Focus('sv_rescue_companies', 'Mine Rescue Companies',
          "When a shaft floods or a gallery collapses, the nearest help is usually the next shift, with whatever tools it "
          "carries. Training two companies of the service as mine rescue teams, with breathing sets and a dedicated train, "
          "gives the zone a disciplined response. Soldiers grumble about crawling through mud; families remember who came.",
          ('medical', 'security'), after=('sv_muster',), reward=(Idea('rescue_companies'),)),
    Focus('sv_ridge_marches', 'Marches on the Western Ridges',
          "The western hills and mountains are the zone's natural defence and its least known ground. Battalions march the "
          "ridges in every season, mapping tracks, springs and caves and timing how long it takes to move a company from the "
          "railway to a pass. The marches cost boots and fuel. They make the service at home in its own hills.",
          ('training', 'tools'), after=('sv_muster',), reward=(XP('army', 15), TimedIdea('ridge_marches', 365))),
    Focus('sv_pass_guard', 'Guard the Mountain Passes',
          "One doctrine for a very small force is to hold ground it knows: prepared posts on the passes, stores in caves and "
          "a reserve that walks rather than drives. It suits the hills and the service's lack of heavy weapons. It leaves "
          "the plains of East Gibraltar lightly held and depends on soldiers who can live rough for weeks.",
          ('security', 'tools'), after_any=('sv_rescue_companies', 'sv_ridge_marches'), cost=10,
          exclusive=('sv_motor_column',), reward=(SwapIdea('territorial_service', 'pass_guard'),)),
    Focus('sv_motor_column', 'A Motor Column Along the Line',
          "The other doctrine uses the trucks and the railway to move a small force fast: a motorised column that can reach "
          "any town on the line within hours, backed by trains for heavy loads. It suits the eastern plains and the "
          "service's large truck park. It also ties the force to roads and rails that any storm can cut.",
          ('logistics', 'security'), after_any=('sv_rescue_companies', 'sv_ridge_marches'), cost=10,
          exclusive=('sv_pass_guard',), reward=(SwapIdea('territorial_service', 'motor_column'),)),
    Focus('sv_railhead_stores', 'Service Stores at the Railhead',
          "With a proper railhead yard in the east, the service can keep a reserve of rifles, rations, fuel and tents where "
          "trains can reach it from either end of the line. A guarded depot replaces scattered sheds in town halls and "
          "police stations. Quartermasters gain a single inventory; thieves lose a dozen easy targets.",
          ('logistics', 'document'), after=('sv_muster',), requires=(HasFlag('east_railhead'),),
          reward=(Idea('railhead_depot'),)),
    Focus('sv_shift_reserve', 'A Reserve Drawn from the Shifts',
          "Most young adults in the zone work shifts in the mines, the railyards or the port. A reserve roll lets them train "
          "with the service for two weeks a year, scheduled around their shift patterns with the firms' agreement. The "
          "service gains numbers it could never pay full time. Employers lose a fortnight of labour every year.",
          ('training', 'civil'), after_any=('sv_pass_guard', 'sv_motor_column'), reward=(Idea('shift_reserve'),)),
    Focus('sv_liaison_strip', 'A Liaison Strip in the East',
          "East Gibraltar is a long day by road from the port city. A short gravel strip beside the eastern depot lets a "
          "borrowed light aircraft carry officers, medicine or spare parts across in an hour. The zone still has no combat "
          "air arm, and the strip is not a step toward one; it is a shortcut over the mountains.",
          ('runway', 'logistics'), after=('sv_railhead_stores',), reward=(Build('air_base', 1, 610),)),
    Focus('sv_leasath_posts', 'Observation Posts Toward Leasath',
          "East Gibraltar's frontier with Leasath crosses open hill and plain with few landmarks. The service builds "
          "observation posts with radios and a small radar on the higher ground, staffed in rotation. They report traffic, "
          "weather and grass fires rather than threats. Leasath is told what they are for, and no claim or line moves.",
          ('radar', 'security'), after=('sv_ridge_marches',),
          reward=(Build('radar_station', 1, 610), Tooltip('No claim, core or frontier change.'))),
))

NEIGHBOURS = Branch('neighbours', 'Three Neighbours and the Sea', 1994, 'FOCUS_FILTER_POLITICAL', (
    Focus('nb_one_table', 'Three Frontiers and a Coast',
          "Arklith lies to the north, Aurelia to the south and Leasath to the east, and the western sea carries everything "
          "else. The ore rights in both districts are held for the two largest neighbours. The zone has never set a foreign "
          "policy of its own, only answered letters. A small frontier office now gathers every agreement into one file.",
          ('diplomacy', 'document'), reward=(Idea('frontier_office'), Event('three_neighbours'))),
    Focus('nb_arklith_desk', 'A Standing Desk for Arklith',
          "Arklith holds the eastern ore rights and runs two of the rail links north. Questions about wagons, royalties, "
          "customs and workers crossing for shifts arrive at a dozen offices. A standing desk staffed by officials who know "
          "the Arklith ministries handles all of them. It costs salaries and gives the north a single number to call.",
          ('diplomacy', 'rail'), after=('nb_one_table',), reward=(Flag('arklith_desk'), Stability(0.01))),
    Focus('nb_aurelia_desk', 'A Standing Desk for Aurelia',
          "Aurelia holds the western ore rights, the larger share of the zone's output, and supplies much of the food that "
          "comes in by road. Aurelian business has always gone through the port agents. A standing desk in the "
          "Administration takes it over, with staff who read the Aurelian press and know which ministry decides what.",
          ('diplomacy', 'economy'), after=('nb_one_table',), reward=(Flag('aurelia_desk'), PP(15))),
    Focus('nb_leasath_crossing', 'Crossing Hours with Leasath',
          "Leasath shares only the eastern frontier and holds no rights in the zone, but herders, traders and seasonal "
          "workers cross it daily. Agreed crossing hours, a shared list of permitted goods and a monthly meeting of post "
          "commanders keep small frictions small. The arrangement changes no line on any map and asks nothing of either "
          "capital.",
          ('peace', 'diplomacy'), after=('nb_one_table',),
          reward=(TimedIdea('crossing_hours', 1095), Tooltip('No claim, core or frontier change.'))),
    Focus('nb_every_buyer', 'Ore for Any Lawful Buyer',
          "One stance treats the zone as a neutral market: the share of ore it controls goes to any lawful buyer at the best "
          "price, and no neighbour receives special terms. Prices rise when markets are hot. Relations with the rights "
          "holders cool a little, since they expected to stand first in line for every tonne the pits produce.",
          ('economy', 'diplomacy'), after_any=('nb_arklith_desk', 'nb_aurelia_desk', 'nb_leasath_crossing'), cost=10,
          exclusive=('nb_near_contracts',), reward=(SwapIdea('frontier_office', 'open_ore_market'),)),
    Focus('nb_near_contracts', 'Long Contracts Next Door',
          "The other stance signs long supply contracts with Arklith and Aurelia for the zone's own share, at fixed prices "
          "with modest indexation. Income becomes steady and the neighbours become partners with a stake in calm. In a boom "
          "the zone sells too cheaply. In a slump it is the only seller in the region still being paid.",
          ('diplomacy', 'scales'), after_any=('nb_arklith_desk', 'nb_aurelia_desk', 'nb_leasath_crossing'), cost=10,
          exclusive=('nb_every_buyer',), requires=(HasFlag('arklith_desk'), HasFlag('aurelia_desk')),
          reward=(SwapIdea('frontier_office', 'neighbour_contracts'),)),
    Focus('nb_war_news', 'War News at the Weighbridges',
          "News of war around Belka reaches the zone in late March 1995, from far beyond its frontiers. Gibraltar takes no "
          "part and has no reason to. Yet tungsten and chromium are war metals, and within weeks brokers are telephoning the port with offers nobody "
          "has seen before. The Administration now has to work out how a neutral mining zone behaves when its ore suddenly "
          "matters.",
          ('communications', 'tools'), after=('nb_one_table',), requires=(After('1995.3.25'),),
          reward=(Event('far_war'), WarSupport(0.01))),
    Focus('nb_war_premium', 'A Premium Nobody Planned For',
          "Wartime prices reach the weighbridges for a few months, and the zone's share of the ore earns more than anyone "
          "budgeted. The treasury wants to bank the windfall. The towns want it spent before it disappears. Insurers raise "
          "rates on every ship sailing from Gibraltar City, which eats part of the premium before it ever lands.",
          ('economy', 'communications'), after=('nb_war_news',),
          reward=(TimedIdea('war_premium', 365), Stability(-0.01))),
    Focus('nb_after_lumen', 'Prices Fall After Lumen',
          "Peace is signed at Lumen on 20 June 1995 and the Belkan War is over; the brokers stop calling almost overnight. "
          "Contracts written in the spring at wartime prices are renegotiated or quietly abandoned. The zone counts what the "
          "war earned it and what the fall costs. The Administration resolves never again to budget a war price as income.",
          ('peace', 'scales'), after=('nb_war_premium',), requires=(After('1995.6.20'),),
          reward=(Idea('price_discipline'),)),
    Focus('nb_neutral_statute', 'Neutrality Written Down',
          "Whatever stance it took on its ore, the zone now writes its neutrality into law: no foreign troops on its soil, no "
          "arms sold to parties at war and equal access for lawful trade. It costs nothing to print and something to keep. "
          "Neighbours can now hold the zone to its word, and that is exactly why it is written.",
          ('peace', 'document'), after_any=('nb_every_buyer', 'nb_near_contracts'), reward=(Idea('neutral_statute'),)),
))

SKY = Branch('sky', 'Ulysses and the Old Galleries', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sk_impact_notice', 'The Impact Notice in the Zone',
          "Ulysses has been a newspaper word since the IAU warning of late 1994. In April 1996 the FCU announcement turns "
          "it into a planning problem for every government, this one included, and the landing places of the fragments "
          "are unknown. The Administration gathers engineers, doctors and railway officials and asks a question it has never faced: how do "
          "two small districts shelter everyone?",
          ('meteor', 'assembly'), requires=(After('1996.4.20'),),
          reward=(Idea('impact_board'), Event('ulysses_notice'))),
    Focus('sk_gallery_survey', 'Survey the Worked-Out Galleries',
          "Generations of mining have left kilometres of worked-out galleries under the western hills, some dry and stable, "
          "others flooded or collapsing. Survey teams with lamps and gas meters map which could hold people for days, how "
          "air would reach them and where water would come from. The survey costs a season and several close calls.",
          ('tools', 'shelter'), after=('sk_impact_notice',),
          reward=(Flag('galleries_mapped'), Research('construction_tech', 0.5, 1))),
    Focus('sk_ridge_watch', 'Sky Watch on the Western Ridge',
          "Fragments may come with little warning, and the zone has no air defence and no observatory. A watch post on the "
          "western ridge with a radar, telescopes lent by schools and a telephone wired straight to the port city gives minutes of notice "
          "that sirens can use. Volunteers staff it through the nights, at first with real enthusiasm.",
          ('telescope', 'radar'), after=('sk_impact_notice',),
          reward=(Build('radar_station', 1, 0), WarSupport(0.02))),
    Focus('sk_gallery_shelters', 'Shelters in the Old Galleries',
          "The first plan turns the best galleries into shelters: doors, ventilation fans, latrines, bunks and water tanks, "
          "with marked routes from every western town. Mining crews do the work they know best. It shelters the west well "
          "and the eastern plains poorly, since the galleries lie in the hills, and someone must maintain them afterwards.",
          ('shelter', 'tools'), after_any=('sk_gallery_survey', 'sk_ridge_watch'), cost=10,
          exclusive=('sk_evacuation_trains',), requires=(HasFlag('galleries_mapped'),),
          reward=(SwapIdea('impact_board', 'gallery_shelters'),)),
    Focus('sk_evacuation_trains', 'Evacuation Trains on the Ore Line',
          "The second plan relies on the railway: every engine and wagon in the zone held ready to move people away from "
          "whichever district is threatened, along a line the dispatchers know by heart. It costs less than shelters and "
          "serves both districts. It depends on warning, on the line staying intact and on crews who will drive toward danger.",
          ('rail', 'refugees'), after_any=('sk_gallery_survey', 'sk_ridge_watch'), cost=10,
          exclusive=('sk_gallery_shelters',), reward=(SwapIdea('impact_board', 'evacuation_trains'),)),
    Focus('sk_stock_galleries', 'Stock the Deep Levels',
          "An empty gallery protects nobody for long. Tinned food, medicine, blankets, batteries and water purifiers go down "
          "into the galleries in sealed crates, with a rotation schedule so stores do not spoil unseen. Warehouses in the "
          "port city empty for a season, and prices for some staples rise. Each town learns which gallery is its own.",
          ('shelter', 'logistics'), after=('sk_gallery_shelters',), reward=(TimedIdea('stocked_galleries', 1095),)),
    Focus('sk_last_week', 'A Timetable for the Last Week',
          "The dispatchers draft a special timetable for the days before any impact: which trains go where, in what order, "
          "carrying whom. Every station posts its own page. Practice runs move schools and hospitals at night with few "
          "complaints. The timetable assumes the line will be intact, and the engineers quietly write a second one that "
          "assumes otherwise.",
          ('rail', 'document'), after=('sk_evacuation_trains',), reward=(TimedIdea('evacuation_timetable', 1095),)),
    Focus('sk_breakup_night', 'Sirens on the Breakup Night',
          "When Ulysses goes inside the Roche limit on 8 July 1999 and breaks up, years of waiting end within days. The "
          "zone's plans meet the real thing. Sirens sound, trains stand ready or gallery doors close, and the ridge watch "
          "logs whatever it sees. Wherever "
          "the fragments come down, the zone must now live with what its preparations cost and what they proved.",
          ('meteor', 'shelter'), after_any=('sk_stock_galleries', 'sk_last_week'), requires=(After('1999.7.8'),),
          reward=(Event('breakup'), Stability(0.01))),
    Focus('sk_relief_line', 'Relief Trains for Stricken Neighbours',
          "With the zone's own preparations stood down, the railway and the harbour have spare capacity and an organisation "
          "used to moving people quickly. Relief trains and ships carry blankets, medicine and engineers to neighbours who "
          "ask for help. It costs fuel and stock the zone paid for. It earns a kind of goodwill royalties cannot buy.",
          ('refugees', 'rail'), after=('sk_breakup_night',), reward=(Idea('relief_desk'),)),
))

WORKS = Branch('works', 'The Last Lot and the School of Mines', 1997, 'FOCUS_FILTER_RESEARCH', (
    Focus('lt_last_lot', 'One Free Lot in West Gibraltar',
          "West Gibraltar has a single serviced industrial lot left near the harbour, big enough for one large plant; East "
          "Gibraltar has none at all. Three proposals compete for that last lot: a smelter, a repair yard and an arms line. "
          "Whatever is built will shape the zone's economy for decades, and the losing bids will not get another chance.",
          ('industry', 'scales'), reward=(Event('last_lot'), PP(10))),
    Focus('lt_smelter', 'A Ferroalloy Smelter on the Lot',
          "A smelter would turn the zone's chromium and tungsten into ferroalloys before export, keeping the most valuable "
          "step at home. It needs large amounts of power and skilled furnace crews the zone does not yet have. The operating "
          "firms would rather ship raw ore. The smelter would make the zone a processor rather than only a quarry.",
          ('industry', 'tools'), after=('lt_last_lot',), cost=10, exclusive=('lt_repair_yard', 'lt_arms_line'),
          reward=(Build('industrial_complex', 1, 0),)),
    Focus('lt_repair_yard', 'A Ship Repair Yard on the Lot',
          "A repair yard by the harbour would service the ore carriers and the zone's merchant hulls without sending them "
          "abroad for every hull survey. It suits the port's deep water and its large naval base. Yards are hungry for steel "
          "and skilled welders, and their order books depend on shipping markets the zone cannot control.",
          ('navy', 'tools'), after=('lt_last_lot',), cost=10, exclusive=('lt_smelter', 'lt_arms_line'),
          reward=(Build('dockyard', 1, 0),)),
    Focus('lt_arms_line', 'An Arms Line on the Lot',
          "The third bid is an arms plant making rifles, truck parts and ammunition for the territorial service, with spare "
          "capacity for export. It would make the service self-supplied and employ hundreds. Neighbours would notice a "
          "neutral zone adding arms production, and export licences would test every promise the zone has made about "
          "neutrality.",
          ('security', 'industry'), after=('lt_last_lot',), cost=10, exclusive=('lt_smelter', 'lt_repair_yard'),
          reward=(Build('arms_factory', 1, 0),)),
    Focus('lt_smelter_power', 'Power for the Furnaces',
          "The smelter's furnaces draw more power than the port city uses at night. A long-term power contract, a new "
          "substation and a high-voltage line link the plant to supply it can count on. Households complain when the first "
          "winter's prices rise. The furnace crews, trained abroad, come home to the best-paid jobs in the zone.",
          ('industry', 'economy'), after=('lt_smelter',), exclusive=('lt_yard_orders', 'lt_arms_licences'),
          reward=(Idea('alloy_works'),)),
    Focus('lt_yard_orders', 'Repair Orders from the Ore Fleet',
          "The yard's first order book comes from the ore carriers that already call at Gibraltar City: hull cleaning, "
          "propeller work and classification surveys. Shipowners save days of steaming to foreign yards. The welders learn on "
          "routine jobs before attempting anything larger. Success depends on how many ships the harbour attracts.",
          ('navy', 'economy'), after=('lt_repair_yard',), exclusive=('lt_smelter_power', 'lt_arms_licences'),
          reward=(Idea('yard_order_book'),)),
    Focus('lt_arms_licences', 'Export Licences Under Review',
          "Every export from the new arms line now needs a licence reviewed by a panel that publishes its decisions. Sales to "
          "parties at war are refused. The plant loses some orders and gains a reputation neighbours can trust. The "
          "territorial service receives its rifles first, and the panel's reports become required reading next door.",
          ('document', 'security'), after=('lt_arms_line',), exclusive=('lt_smelter_power', 'lt_yard_orders'),
          reward=(Idea('licence_panel'),)),
    Focus('lt_assay_office', 'An Assay Office of Our Own',
          "Every grade dispute in the zone ends with a sample sent to a laboratory abroad, chosen and paid for by the buyer. "
          "A public assay office in the port city tests samples from every shipment and issues certificates both sides must "
          "accept. Chemists must be hired and equipment imported. Grade disputes shrink from months to days.",
          ('science', 'document'), after=('lt_last_lot',), reward=(Idea('assay_office'),)),
    Focus('lt_mines_school', 'A School of Mines for the Zone',
          "Night classes have shown that the pit towns hold more talent than anyone assumed. A full school of mines, with "
          "courses in geology, surveying, ventilation and metallurgy, turns that talent into engineers. Lecturers come from "
          "abroad at first. Graduates who stay replace the foreign managers the firms have always brought in, and the firms "
          "change too.",
          ('science', 'training'), after=('lt_assay_office',), requires=(HasFlag('night_classes'),),
          reward=(Idea('mines_school'), Research('excavation_tech', 0.5, 1))),
    Focus('lt_carbide_tools', 'Carbide Bits from Local Tungsten',
          "Drill bits and cutting tools tipped with tungsten carbide wear far longer than steel ones, and the zone mines the "
          "tungsten yet imports every bit. A small carbide workshop at the school makes tips for local drills, first as a "
          "teaching exercise and later for sale. It is a modest start in turning ore into finished products.",
          ('tools', 'science'), after=('lt_mines_school',), reward=(Idea('carbide_workshop'),)),
    Focus('lt_gas_detection', 'Gas Detection in Every Gallery',
          "Methane and carbon monoxide still kill miners whose lamps give little warning. The assay laboratory tests "
          "electronic gas detectors and fixes them in the deepest galleries, wired to alarms at the surface. Firms pay for "
          "installation on the main shafts. Accidents fall, and the electronics bench becomes a small trade of its own.",
          ('radar', 'tools'), after=('lt_assay_office',), reward=(Research('electronics', 0.5, 1), Stability(0.02))),
))

CENTURY = Branch('century', 'The Zone at the Century', 2002, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('cy_ledger_decade', 'Ten Years of Weighbridge Books',
          "A decade of weighbridge books, census rolls, clinic records and train logs now exists, and nobody has read them "
          "side by side. The statistics office binds them into the zone's first yearbook: who governs, who keeps the value "
          "of the ore, how the towns live and how the line runs. Every faction prepares to quote it.",
          ('assembly', 'document'), reward=(Event('zone_yearbook'), Stability(0.01))),
    Focus('cy_board_seats', 'The Board Reallocates Its Seats',
          "The concession board's seats were assigned by output when it took office, and the shares have shifted since. New "
          "firms want seats; old ones refuse to give theirs up. The board adopts a formula weighted by tonnage, employment and "
          "royalties paid. It is more defensible than the old allocation and makes every meeting a quarrel about arithmetic.",
          ('economy', 'assembly'), after=('cy_ledger_decade',), requires=(HasFlag('path_board'),),
          exclusive=('cy_chamber_second', 'cy_delegate_congress', 'cy_directorate_audit'),
          reward=(Idea('seat_formula'),)),
    Focus('cy_chamber_second', 'A Second Chamber Election',
          "The district chamber faces its voters again, and the campaign is about royalties, rents and the ore line rather "
          "than whether the chamber should exist. Turnout falls from the first election, which pessimists call apathy and "
          "optimists call normal life. The new cabinet inherits a budget process that works and promises few believed.",
          ('ballot', 'civil'), after=('cy_ledger_decade',), requires=(HasFlag('path_assembly'),),
          exclusive=('cy_board_seats', 'cy_delegate_congress', 'cy_directorate_audit'),
          reward=(Idea('settled_chamber'),)),
    Focus('cy_delegate_congress', 'A Congress of Pit Delegates',
          "The federation of pit councils calls its first full congress in a decade, with delegates from every shaft, yard "
          "and quay. Motions range from shorter shifts to the future of the concessions. The congress keeps the federation "
          "honest and slow. Investors watch the motions closely, and some quietly return when the boldest ones are defeated.",
          ('tools', 'ballot'), after=('cy_ledger_decade',), requires=(HasFlag('path_councils'),),
          exclusive=('cy_board_seats', 'cy_chamber_second', 'cy_directorate_audit'),
          reward=(Idea('delegate_congress'),)),
    Focus('cy_directorate_audit', 'An Outside Audit of the Directorate',
          "The directorate invites auditors from outside the zone to examine its standards, accounts and decisions over ten "
          "years. Their report praises the rulebook and criticises how rarely anyone outside the directorate was consulted. "
          "Publishing it costs face; refusing would cost more, so the directorate prints the report with its replies beside "
          "it.",
          ('scales', 'science'), after=('cy_ledger_decade',), requires=(HasFlag('path_directorate'),),
          exclusive=('cy_board_seats', 'cy_chamber_second', 'cy_delegate_congress'),
          reward=(Idea('audited_directorate'),)),
    Focus('cy_compact_renewal', 'Renewing the Royalty Compact',
          "The royalty compact's first term ends, and both the holders and the zone come to the table with ten years of "
          "data. The zone asks for higher indexation on tungsten and firmer tailings duties. The holders ask for longer "
          "terms. The renewed compact gives each side something and makes the next renewal look easier than this one.",
          ('diplomacy', 'document'), after=('cy_ledger_decade',), requires=(HasFlag('model_compact'),),
          exclusive=('cy_company_wagons',), reward=(Idea('renewed_compact'),)),
    Focus('cy_company_wagons', 'New Wagons for the Ore Company',
          "The ore company has run the haulage for years with wagons that were old when it bought them. A fleet renewal "
          "programme, financed by bonds secured on haulage fees, replaces the worst of them. Turnaround improves and "
          "breakdowns fall. The bonds tie the company to its creditors, who now ask about its accounts every quarter.",
          ('rail', 'economy'), after=('cy_ledger_decade',), requires=(HasFlag('model_company'),),
          exclusive=('cy_compact_renewal',), reward=(Idea('renewed_wagons'),)),
    Focus('cy_usean_freight', 'Freight Rates and a Usean War',
          "In August 2003 the founding of the ISAF signals open war on the Usean continent, far from the zone. Shipping "
          "insurers react before anyone else, raising rates on every route that might touch the war. The hull register shows "
          "which zone-linked ships sail near the danger. Ore prices stir again, and the Administration remembers 1995.",
          ('navy', 'communications'), after=('cy_ledger_decade',),
          requires=(After('2003.8.22'), HasFlag('hull_register')), reward=(Event('usean_war'), PP(15))),
    Focus('cy_ore_fund', 'An Ore Fund for Lean Years',
          "Ore runs out eventually, and prices rise and fall on wars and markets far away. A fund that saves part of every "
          "year's royalties, invested abroad and drawn only by a published rule, protects the zone against both. Every "
          "year's spending is smaller than it could be. The fund's critics ask exactly whom the zone is saving for.",
          ('economy', 'scales'), after=('cy_ledger_decade',), exclusive=('cy_spend_home',), reward=(Idea('ore_fund'),)),
    Focus('cy_spend_home', 'Royalties Spent at Home',
          "The opposite view says the zone's people dug the ore and should see the royalties now: new schools, better "
          "clinics, paved roads and housing. A fund abroad helps nobody living in a pit town today. Spending everything brings "
          "visible results and leaves nothing for the day a seam closes or a price collapses.",
          ('rebuild', 'civil'), after=('cy_ledger_decade',), exclusive=('cy_ore_fund',),
          reward=(Idea('home_works'), Build('infrastructure', 1, 0))),
    Focus('cy_next_charter', 'A Charter for the Next Decade',
          "The yearbook and the arguments it started become the basis for a revised charter, debated in whatever form the "
          "zone's government now allows. It keeps what worked, repairs what the tables showed was broken and sets the "
          "questions for the following ten years: depletion, the concessions, the line and the port.",
          ('document', 'assembly'), after_any=('cy_ore_fund', 'cy_spend_home'),
          reward=(Idea('second_charter'), Stability(0.02))),
))

BRANCHES = (ZONE, CONCESSIONS, TOWNS, HARBOUR, RAIL, SERVICE, NEIGHBOURS, SKY, WORKS, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('extra_ore_trains', 'Run Extra Ore Trains',
                'Every spare engine and wagon runs ore for a season, at the cost of passenger services and track wear. '
                'Repeatable once a year.',
                30, (TimedIdea('ore_rush', 90),), requires=(Completed('rl_walk_line'),), cooldown=365),
    DecisionDef('rescue_drill', 'Hold a Mine Rescue Drill',
                'The rescue companies rehearse a flooded-gallery rescue with the firms own crews. Repeatable every six '
                'months; it costs a shift of output.',
                25, (XP('army', 10), Stability(0.01)), requires=(Completed('sv_rescue_companies'),), cooldown=180),
    DecisionDef('charter_auction', 'Auction the Season Charters',
                'Port agents auction the coming season of ore charters among the hulls on the register. Repeatable once a '
                'year.',
                35, (TimedIdea('charter_season', 120),), requires=(Completed('hb_hull_register'),), cooldown=365),
    DecisionDef('gallery_crates', 'Fresh Crates for the Galleries',
                'Old shelter stores are sold cheaply in the pit towns and replaced with fresh crates. Repeatable every two '
                'years.',
                20, (Stability(0.02),), requires=(Completed('sk_stock_galleries'),), cooldown=730),
    DecisionDef('ambulance_hangar', 'A Second Hangar at the Strip',
                'Adds a second hangar and a longer runway to the air ambulance strip outside Gibraltar City. A one-time '
                'charge on the budget.',
                50, (Build('air_base', 1, 0),), requires=(Completed('tw_ambulance_strip'),)),
    DecisionDef('royalty_advance', 'Draw a Royalty Advance',
                'The treasury borrows against next year of royalties to cover a shortfall. Once only, and the towns notice.',
                10, (PP(60), Stability(-0.02)), requires=(Completed('cn_weighbridge'),)),
)
