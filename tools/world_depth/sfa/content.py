"""Sfaenland (SFA): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-labelled
National Administration with elections_allowed = no, popularity split between
fascism and neutrality), the unnamed starting office, the world-foundation force
and industry calibration, the neutral district captions, the railways and weather
of the map, and the global flags other mod scripts already set. Official: ACES
Chronicle rows used only as date anchors for distant pressures, each cited by its
exact key. Everything else, including every Sfaenland choice, office, idea,
building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='SFA', name='Sfaenland', root='world', package='sfa',
                  themes=('rail', 'security', 'scales'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities fascism 50, neutrality 48, democratic 1, communism 1; stability and war support 0.5; three research '
           'slots; tech_mountaineers and early_fighter among the starting technologies; grand doctrines superior_firepower, '
           'new_fleet_in_being and new_operational_integrity. The starting leader is the unnamed National Administration office '
           '(SFA_ac_government_office), whose 1991 holder has not been established. The readiness order, the postponement '
           'notice and every political answer in this tree are provisional gameplay readings of these settings.',
           'mod/2985041246/history/countries/SFA - Sfaenland.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'tools/world_foundation/country_registry.json (SFA row: civil_administration, capacity 40)'),
    Source('Mod provenance',
           'Geography: 1991 states 10, 28, 51, 65, 77, 189, 198 and 497 (capital), captioned Sfaenland District A, B, C, D, '
           'E, F, G and Capital District by the neutral regional labels; victory points Sfaenland Capital Centre (9718) and '
           'Logistics Centres 3621 (District A) and 614 (District B). Industry: the Capital District (city, 10 plains '
           'provinces) holds 3 civilian and 2 arms plants, the fuel silo and the only air base; District A (forest, hills and '
           'mountain, coastal) 2 and 2; District B (large town, forest and plains, coastal) 3 and 2; every shared slot in the '
           'three is filled. District G (plains, forest, marsh and one urban province, coastal) holds the 3 dockyards and the '
           'naval base on province 2778, with one free slot. Districts C (14 provinces, forest and hills, coastal), D (19 '
           'provinces, plains and one urban province, coastal), E (10 provinces, plains and hills) and F (4 provinces, hills '
           'and desert) have no buildings, infrastructure or resources. Oil 14, aluminium 13, steel 21 and rubber 6 lie in '
           'the Capital District and Districts A and B. Level-2 railways run Capital Centre - province 315 (District E) - '
           'District C - Logistics Centre 614, with branches from 315 to Logistics Centre 3621 and through District C to '
           '2778 and on into District G; Districts D and F have no railway. No other place is named and the Earth-template '
           'state captions are not used.',
           'mod/2985041246/history/states (10, 28, 51, 65, 77, 189, 198, 497); '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/definition.csv; tools/regional_labels/labels.json'),
    Source('Mod provenance',
           'Weather and frontiers. Strategic regions 318 (Districts C and E) record no rain in any month; 319 (Capital '
           'District and District F) and 320 (Districts D and G) record heavy rain on up to 40 percent of days; 317 '
           '(Districts A and B) has mid-year rains; no region has snow. Land neighbours computed from map/provinces.bmp: '
           'Glaceland (its Districts A and F) along Districts A, E and F, with province 3621, Logistics Centre 3621, on the '
           'frontier itself; Silvonia (its Districts A and G) along Districts D and F; Luremia (state 231) along District F '
           'only. Coasts on Districts A, B, C, D and G.',
           'mod/2985041246/map/strategicregions/317-XXX.txt, 318-XXX.txt, 319-XXX.txt, 320-XXX.txt; '
           'mod/2985041246/map/provinces.bmp; mod/2985041246/map/definition.csv'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role territorial readiness; 8 civilian, 6 military and 3 naval '
           'factories; six infantry formations of six battalions and an engineer company, two each at the Capital Centre and '
           'Logistics Centres 614 and 3621; 36 fighters and 12 ground-attack aircraft on the capital air base, with 9 '
           'fighters and 4 support aircraft in reserve; the Maritime Service of two coastal escorts and one coastal submarine '
           'at 2778; 60 convoys; stocks of 1440 infantry equipment, 880 motorized equipment, 24 trains and 288 support '
           'equipment; research priority Physical Sustainment. Fiscal profile GDP 160, debt ratio 0.3, collection 0.85, '
           'growth 3, inflation 2 is fictional calibration, not canon national accounts or order of battle.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/economy_v2/profiles.json; '
           'mod/2985041246/history/units/SFA_ws_land.txt, SFA_ws_air.txt, SFA_ws_navy.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour consistency: the Glaceland tree places its four dockyards in its District A beside the Sfaenland '
           'frontier and plans a trade road toward Sfaenland; the Luremia tree describes desert traders taking the road from '
           'Qesi toward Sfaenland and puts customs on its own side; the Silvonia tree builds a hill road in its District G. '
           'This tree builds and governs only on the Sfaenland side, publishes only its own rules, and claims no action, '
           'consent or outcome for any neighbour.',
           'tools/world_depth/gla/content.py; tools/world_depth/lur/content.py; tools/world_depth/esn/content.py'),
    Source('Mod provenance',
           'Campaign hooks read, never set: belka_lost_belkan_war, belka_won_belkan_war and belkan_war_is_happening (Belkan '
           'War); ac_ucw_isaf_formed, ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory (Usean Continental War). '
           'Each alternate outcome keeps its own focus.',
           'mod/2985041246 scripts that set these global flags; tools/national_depth/catalogue.py global_flags()'),
    Source('Official', 'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, '
           'Yuktobania. Gate of the submarine announcement focus; no Sfaenland role is claimed.', '1991 / 09.02'),
    Source('Official', 'Date anchor: the International Astronomical Union announces that Ulysses will pass close to the '
           'Earth with a chance of impact. Gate of the astronomers focus.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gate of the war bulletins focus; Sfaenland takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Earliest date of the stand-down '
           'focus, which also waits until the mod no longer records the war as happening.', '1995 / 06.20'),
    Source('Official', 'Date anchor: the President of the FCU announces that Ulysses will impact the Earth. Gate of the '
           'announcement focus; where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Former top pilots of the Belkan Air Force are hired by various countries as aggressor squadrons. '
           'Date gate of the aggressor focus; whether Sfaenland hires any is a player choice, not a claim.', '1998 / 06.19'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche passage focus; '
           'no damage in Sfaenland is claimed.', '1999 / 07.08'),
    Source('Official', 'Erusea invades San Salvacion and uses the Stonehenge railguns as anti-air batteries. Background to '
           'the Usean lessons focus only.', '2003 / SUMMER'),
    Source('Official', 'Date anchor: the FCU demands Erusean withdrawal and establishes the ISAF. The focus that reacts '
           'waits for the mod flag ac_ucw_isaf_formed and claims no Sfaenland part in the war.', '2003 / 08.22'),
    Source('Official', 'The ISAF attacks Erusean forces anchored at Comberth Harbor. Background to the Usean lessons focus '
           'only; no Sfaenland part is claimed.', '2004 / 11.23'),
    Source('Official', 'Farbanti falls and the Continental War ends with the ISAF accepting surrender. Background to the '
           'reopened lanes focus, which waits for the mod flag ac_ucw_outcome_isaf_victory; the Erusean victory branch '
           'waits for ac_ucw_outcome_erusean_victory instead.', '2005 / 09.19'),
    Source('Provisional gameplay',
           'All Sfaenland focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the readiness order
    IdeaDef('readiness_order', 'The Standing Readiness Order',
            'Garrisons, fuel and railway under one emergency authority, with the vote postponed beside them.',
            {'political_power_gain': 0.10, 'war_support_factor': 0.03, 'stability_factor': -0.03}, ('security', 'document')),
    IdeaDef('camps_study', 'A Season of Questions',
            'University teams ask garrison towns and plant streets what they want from government.',
            {'stability_factor': 0.02, 'political_power_gain': -0.05}, ('assembly', 'scales')),
    IdeaDef('charter_rooms', 'Eight Drafting Rooms',
            'Each district drafts clauses for a charter the capital has promised to sign.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('assembly', 'document')),
    IdeaDef('prefect_rule', 'The Prefects Confirmed',
            'District prefects govern as before, now in their own name and answerable to their peers.',
            {'political_power_gain': 0.15, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('movement_pressure', 'The Movement in the Antechamber',
            'The national movement has been promised a path to the seals and expects it soon.',
            {'war_support_factor': 0.06, 'political_power_gain': 0.10, 'stability_factor': -0.03}, ('medal', 'assembly')),
    IdeaDef('question_time', 'Weekly Questions to Ministers',
            'Every minister answers the chamber each week, and the answers are printed the next morning.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'scales')),
    IdeaDef('prefect_terms', 'Prefects on Rotation', 'No prefect serves more than three years in any one district.',
            {'political_power_gain': 0.15, 'stability_factor': 0.04, 'production_speed_buildings_factor': 0.04},
            ('command', 'scales')),
    IdeaDef('readiness_brigades', 'The Readiness Brigades',
            'Volunteer brigades drill at weekends and build roads on weekdays in every district.',
            {'war_support_factor': 0.08, 'training_time_army_factor': -0.08, 'production_speed_infrastructure_factor': 0.08},
            ('security', 'training')),
    IdeaDef('district_papers', 'Papers in Every District',
            'Licensed district newspapers report what the capital would rather not hear.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('communications', 'document')),
    IdeaDef('open_pay_scales', 'Pay Scales on the Wall', 'Every official pay scale is published, district by district.',
            {'political_power_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.02}, ('scales', 'economy')),
    # the main line
    IdeaDef('freight_ledger', 'The Wagon Ledger', 'Every wagon on the main line is counted and its last journey recorded.',
            {'production_speed_infrastructure_factor': 0.08, 'political_power_gain': -0.03}, ('rail', 'document')),
    IdeaDef('treasury_railway', 'A Treasury Railway', 'One public undertaking sets every fare and spends its surplus on track.',
            {'production_speed_infrastructure_factor': 0.12, 'supply_consumption_factor': -0.05}, ('rail', 'economy')),
    IdeaDef('leased_branches', 'Leased Branch Lines',
            'Freight houses run the branches on public track and set their own timetables.',
            {'production_speed_infrastructure_factor': 0.08, 'consumer_goods_factor': -0.04}, ('rail', 'logistics')),
    IdeaDef('night_freight', 'Night Trains at the Junction',
            'The junction signal box is staffed all night and freight runs after dark.',
            {'production_factory_efficiency_gain_factor': 0.03, 'supply_consumption_factor': -0.05}, ('rail', 'communications')),
    # the plant districts
    IdeaDef('plant_census_file', 'The Plant District Inventory',
            'Every machine, shift and stock in the three plant districts is on file.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('second_shift', 'The Second Shift', 'Capital plants run two shifts, and the plant streets never quite sleep.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.03}, ('industry', 'civil')),
    IdeaDef('alloy_priority', 'Alloy Priority', 'Aluminium sheet, extrusion and casting lead the economy.',
            {'research_speed_factor': 0.03, 'production_factory_max_efficiency_factor': 0.03}, ('industry', 'air')),
    IdeaDef('crude_first', 'Crude Pays First', 'Refined fuel and crude sales fund the rest of the budget.',
            {'political_power_gain': 0.08, 'consumer_goods_factor': -0.03}, ('economy', 'logistics')),
    IdeaDef('girders_first', 'Girders Before Exports',
            'Domestic steel goes into rails, bridges and sheds before any of it is sold abroad.',
            {'production_speed_buildings_factor': 0.08, 'production_speed_infrastructure_factor': 0.05}, ('bridge', 'industry')),
    IdeaDef('wage_boards', 'District Wage Boards', 'Common rates for common jobs in every plant street.',
            {'stability_factor': 0.04, 'production_factory_efficiency_gain_factor': 0.02}, ('scales', 'civil')),
    IdeaDef('proof_house', 'Proof-Fired Batches', 'A sample from every batch of rifles and shells is fired before delivery.',
            {'army_org_factor': 0.03, 'production_factory_efficiency_gain_factor': 0.02}, ('tools', 'security')),
    IdeaDef('export_desks', 'The Export Desks', 'Commercial desks for metal, fuel and machinery look for buyers abroad.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('diplomacy', 'economy')),
    # the districts off the line
    IdeaDef('grain_leases', 'Leases on the Coastal Plain',
            'Large grain leases with credit for tractors and storage on the District D plain.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.03}, ('economy', 'civil')),
    IdeaDef('plain_works', 'A Fourth Plant District', 'Housing, power and works are turning the plain town into an industrial centre.',
            {'production_speed_industrial_complex_factor': 0.08, 'stability_factor': -0.02}, ('industry', 'rebuild')),
    IdeaDef('desert_market', 'The Licensed Desert Market', 'A weighbridge, a clerk and a well at the District F crossing.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('economy', 'diplomacy')),
    IdeaDef('boarding_schools', 'Term-Time Boarding',
            'Children of the plain and the desert corner board at district schools during term.',
            {'research_speed_factor': 0.02, 'stability_factor': 0.02}, ('civil', 'training')),
    # the Maritime Service
    IdeaDef('maritime_roll', 'Maritime Service Roll', 'Two escorts, one submarine and three yards, mustered and counted.',
            {'navy_org_factor': 0.03}, ('navy', 'document')),
    IdeaDef('submarine_flotilla', 'Flotilla of the Harbour Mouths', 'Coastal submarines watch the harbour mouths.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.05}, ('submarine', 'security')),
    IdeaDef('coastal_escorts', 'Escorts for the Coast Lanes', 'Escort groups shepherd the coastal freighters.',
            {'naval_speed_factor': 0.04, 'navy_org_factor': 0.05}, ('navy', 'logistics')),
    IdeaDef('convoy_groups', 'Convoy Groups', 'Every coastal freighter has a group, a route and a harbour of refuge.',
            {'naval_coordination': 0.04, 'consumer_goods_factor': -0.02}, ('logistics', 'document')),
    IdeaDef('naval_bunkers', 'Bunkers at the Naval Base', 'Buried tanks hold months of patrol fuel at District G.',
            {'navy_org_factor': 0.04, 'naval_speed_factor': 0.03}, ('shelter', 'navy')),
    IdeaDef('coast_watchers', 'The Coast Watch', 'Volunteer lookouts report every ship along five coastal districts.',
            {'air_detection': 0.05, 'naval_coordination': 0.03}, ('radar', 'navy')),
    IdeaDef('design_office', 'The Naval Design Office', 'Naval architects draw escorts at home for the District G yards.',
            {'industrial_capacity_dockyard': 0.06, 'research_speed_factor': 0.01}, ('science', 'navy')),
    # the army
    IdeaDef('three_garrisons', 'The Garrison Pairs',
            'The army sits in pairs of formations at three posts and nowhere else.',
            {'army_core_defence_factor': 0.04}, ('security', 'command')),
    IdeaDef('motor_pool', 'The Central Motor Pool', 'One pool, one set of workshops and one fuel allocation for every army truck.',
            {'army_speed_factor': 0.03, 'supply_consumption_factor': -0.05}, ('logistics', 'tools')),
    IdeaDef('home_companies', 'District Home Companies', 'A reserve company in every district without a garrison.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.05}, ('civil', 'security')),
    IdeaDef('line_reserve', 'The Main Line Reserve', 'Formations held together and moved by train, with ramps at every halt.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.08}, ('rail', 'security')),
    IdeaDef('hill_battalions', 'Western Hill Battalions',
            'Two formations trained and equipped for the forest and hills of District A.',
            {'army_attack_factor': 0.04, 'army_org_factor': 0.04, 'attrition': -0.05}, ('training', 'security')),
    IdeaDef('range_season', 'A Year on the Ranges', 'Formations rotate through the live-fire ranges in District E.',
            {'experience_gain_army_factor': 0.10, 'training_time_army_factor': -0.05}, ('training', 'tools')),
    IdeaDef('staff_college', 'The Capital Staff College', 'One method of orders and movement taught to every future commander.',
            {'planning_speed': 0.05, 'experience_gain_army_factor': 0.08}, ('command', 'document')),
    # the air arm
    IdeaDef('single_apron', 'The Single Apron', 'Forty-eight aircraft, one runway and one fuel store.',
            {'experience_gain_air_factor': 0.04, 'air_superiority_efficiency': -0.02}, ('air', 'runway')),
    IdeaDef('capital_interceptors', 'Interceptors for the Plant Districts',
            'The whole fighter force is trained and based to defend the plant districts from the air.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('garrison_wings', 'Wings with the Garrisons', 'Air liaison officers at every garrison and pilots trained in ground attack.',
            {'air_mission_efficiency': 0.08, 'experience_gain_air_factor': 0.06}, ('air', 'security')),
    IdeaDef('airframe_shops', 'Alloy Airframe Shops', 'Grounded aircraft are repaired from domestic aluminium sheet.',
            {'repair_speed_factor': 0.10, 'experience_gain_air_factor': 0.04}, ('tools', 'air')),
    IdeaDef('aggressor_syllabus', 'The Hired Aggressor Syllabus', 'Contract instructors fly against Sfaenland pilots in mock combat.',
            {'experience_gain_air_factor': 0.12, 'air_superiority_efficiency': 0.03}, ('medal', 'air')),
    IdeaDef('home_instructors', 'Home-Trained Instructors', 'An instructor school built around pilots trained abroad.',
            {'experience_gain_air_factor': 0.08, 'air_mission_efficiency': 0.03}, ('training', 'air')),
    # frontiers
    IdeaDef('crossing_gazetteer', 'The Crossing Gazetteer', 'Every road, track and ferry across the three frontiers is listed and mapped.',
            {'stability_factor': 0.02, 'army_core_defence_factor': 0.03}, ('diplomacy', 'document')),
    IdeaDef('fishing_rules', 'Rules for the Shared Banks',
            'Sfaenland boats off District D follow published fishing and lighting rules.',
            {'naval_coordination': 0.03, 'stability_factor': 0.02}, ('fishing', 'navy')),
    IdeaDef('open_transit', 'Transit for Any Cargo',
            'Railway, ports and frontier roads open to every cargo under the ordinary customs rules.',
            {'consumer_goods_factor': -0.04, 'industrial_capacity_factory': 0.03}, ('economy', 'diplomacy')),
    IdeaDef('war_cargo_ban', 'The War Cargo Ban',
            'No arms, ammunition or military fuel for any warring party crosses the country.',
            {'army_core_defence_factor': 0.06, 'stability_factor': 0.03}, ('security', 'scales')),
    IdeaDef('belkan_orders', 'Orders from Belkan Buyers', 'Belkan firms buy aluminium and steel on long contracts.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.01}, ('economy', 'industry')),
    IdeaDef('posted_rules', 'Posted Crossing Rules', 'Hours, duties and papers printed at every crossing post.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('scales', 'diplomacy')),
    # Ulysses
    IdeaDef('ulysses_table', 'The Asteroid Table',
            'Scientists, engineers and district officials meet weekly in the capital to read the Ulysses reports.',
            {'stability_factor': 0.02, 'research_speed_factor': 0.02}, ('telescope', 'meteor')),
    IdeaDef('sky_classes', 'Night Classes in Astronomy',
            'Observers on the dry hills explain the tracking data to their neighbours.',
            {'research_speed_factor': 0.03, 'stability_factor': 0.01}, ('telescope', 'science')),
    IdeaDef('plain_shelters', 'Shelters Beneath the Plant Districts',
            'Concrete shelters under schools and plant yards, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('dispersal_plan', 'The Dispersal Timetable', 'Trains, trucks and camp sites assigned for every plant district.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('refugees', 'rail')),
    IdeaDef('sealed_silo', 'A Full and Sealed Silo', 'The capital fuel silo is kept full and guarded against dust and fire.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.02}, ('shelter', 'logistics')),
    IdeaDef('silo_drawdown', 'Fuel Released from the Silo', 'Garrisons and patrol boats burn silo fuel on a season of manoeuvres.',
            {'army_org_factor': 0.05, 'navy_org_factor': 0.04}, ('logistics', 'training')),
    # the turn of the century
    IdeaDef('decade_accounts', 'Ten Years in Tables',
            'A decade of national accounts, district by district, published in one volume.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('scales', 'document')),
    IdeaDef('district_tax_offices', 'District Tax Offices',
            'Tax is assessed and collected in every district, not only in the plant districts.',
            {'political_power_factor': 0.06, 'stability_factor': -0.02}, ('economy', 'civil')),
    IdeaDef('district_report', 'The Report to the Districts',
            'The government answers for its years in office in a volume sent to every district hall.',
            {'political_power_factor': 0.08, 'stability_factor': 0.05}, ('document', 'assembly')),
    IdeaDef('war_risk_pool', 'State Cover for War Risks',
            'A state insurance pool covers coastal freighters whose private cover was cancelled.',
            {'consumer_goods_factor': -0.04, 'naval_coordination': 0.03}, ('economy', 'navy')),
    IdeaDef('manifest_checks', 'Double Manifest Checks', 'Doubtful cargoes are held until their owners prove where they are going.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.04}, ('document', 'security')),
    IdeaDef('reopened_lanes', 'Lanes Reopened to Usea', 'Freight and insurance on Usean routes return to peacetime terms.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('peace', 'navy')),
    IdeaDef('erusean_terms', 'Trading on Erusean Terms', 'Cargo for Usea passes through ports and rules set by Erusea.',
            {'consumer_goods_factor': 0.02, 'political_power_gain': 0.05, 'stability_factor': -0.02}, ('diplomacy', 'scales')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('district_chamber', 'Cabinet of the Eight-District Chamber',
           'A cabinet chosen by a chamber elected from district lists under the drafted charter, governing collectively and '
           'answering to the chamber every week. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism', elections=True),
    Office('prefect_council', 'Standing Council of District Prefects',
           'The eight district prefects and the heads of the main ministries, sitting as a collective council that governs '
           'without parties and publishes its minutes. Provisional gameplay office with no named holder.',
           'neutrality', 'conservatism_na'),
    Office('garrison_directorate', 'Directorate of the Three Garrisons',
           'A directorate of national movement organisers and garrison officers that governs by decree under the readiness '
           'order. Provisional gameplay office with no named holder.',
           'fascism', 'stratocracy_fascism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('postponement', 'A Notice Due Again', (
        "Every four years the election calendar of Sfaenland comes due, and every four years the National Administration "
        "prints the same notice for the district halls: the vote is postponed while the country remains on its readiness "
        "footing. The clerks have the new notice typeset and waiting. What has changed is that people now ask, loudly and "
        "in public, who decided that readiness and elections cannot live side by side.",
        "The awkward part is arithmetic. The party whose name is printed on the government letterhead could fill one seat "
        "in every hundred. The national movement, which wants the readiness order kept and given to true believers, draws "
        "about as much support as everyone else combined. Nearly all the remainder would rather be governed by the "
        "officials and prefects they already know, without a campaign poster in sight. The Administration rules both camps "
        "and speaks for neither.",
        "The Administration's lawyers have been asked what the readiness order really requires, and they want time to "
        "answer properly. Signing the notice now keeps everything as it was for four more years and spares the cabinet a "
        "hard argument. Holding it back until the opinion is ready signals that the question is open, and once a question "
        "is open in Sfaenland it rarely closes quietly.",
    ), (
        Option('Sign the notice as before.', (PP(35), Stability(-0.02))),
        Option('Hold it until the lawyers report.', (Stability(0.02), Event('lawyers_opinion', 20))),
    ), layer='Mod provenance',
        citation='history/countries/SFA - Sfaenland.txt set_politics and set_popularities; the readiness order, the notice '
                 'and every response are provisional gameplay', picture=1),
    EventDef('lawyers_opinion', 'The Opinion on the Readiness Order', (
        "The opinion arrives as forty typed pages and a two-page summary that every minister reads first. The readiness "
        "order, the lawyers find, was written to keep the garrisons, the fuel silo and the railway under one emergency "
        "authority. Nothing in its text mentions elections. The postponement came from a later instruction that cited the "
        "order without being part of it, and nobody since has asked whether that instruction still applies.",
        "In legal terms the finding is modest. In political terms it is explosive. It means a vote could be held without "
        "touching readiness at all, which delights the small democratic camp and alarms almost everyone else. The movement "
        "reads it as proof that the Administration has been hiding behind paperwork. The prefects read it as a warning that "
        "their quiet arrangement is about to become a public quarrel.",
        "The cabinet can let the opinion speak for itself in every district hall, with the full text pinned beside the old "
        "notices, or circulate it among the ministries while it decides what to do. Publication will make the next four "
        "years louder and more honest. Keeping it inside the ministries buys time, though secrets about the readiness order "
        "have a habit of reaching the garrison towns anyway.",
    ), (
        Option('Pin the full text in every district hall.', (Stability(0.03), PP(-20))),
        Option('Circulate it among the ministries only.', (PP(25), Stability(-0.01))),
    ), picture=2),
    EventDef('junction_report', 'A Junction With No Town', (
        "The wagon census comes back from the main line with a map that the transport ministry pins to its wall. Almost "
        "everything Sfaenland moves travels one route: from the Capital Centre out to the junction in District E, on "
        "through the dry hills of District C and down to the logistics centre in District B, with branches to the plants of "
        "District A and to the naval base in District G. If the junction closes, the country stops.",
        "The junction itself surprises ministers who have never seen it. It is a set of points on a rainless plain, with a "
        "signal box, a water tower and no town of any kind. District E has no road network worth the name, and neither does "
        "District C, though the main line crosses both. Trains wait on the running line because no siding is long enough to "
        "hold them, and crews sleep in their cabs.",
        "The census also shows that freight rates bear no relation to costs. Oil and steel trains subsidise empty passenger "
        "runs, and some wagons have not moved in a year. The figures would be gold to anyone who wanted to bid for the "
        "branches, and an embarrassment to the railway's managers. The ministry must decide whether to publish them or keep "
        "them for its own planning.",
    ), (
        Option('Publish the traffic figures.', (Flag('traffic_published'), PP(-10))),
        Option('Keep them inside the ministry.', (PP(25),)),
    ), picture=0),
    EventDef('no_free_plot', 'Fourteen Plants, Three Districts', (
        "The inventory teams finish their tour of the Capital District and Districts A and B, where every civilian plant "
        "and every arms works in the country stands, together with every barrel of oil, ingot of aluminium and tonne of "
        "steel the country produces. Those three districts also hold every plot zoned for industry, and the teams did not "
        "find a single one of those plots standing empty.",
        "The teams' report is blunt. Machines in the capital stand idle half the day for want of a second shift. District "
        "A, whose logistics centre stands on the Glaceland frontier, makes spare parts that District B needs and ships them "
        "the long way round by rail. None of this is a crisis. But there is no room to grow where the industry is, and the "
        "five districts with room have no industry at all.",
        "Ministers hear two answers in the same meeting. The plant managers want to squeeze more from what already stands: "
        "longer shifts, better tooling, fewer idle hours. The planners want to start building where the land is empty, "
        "beginning with the junction and the plain. Both answers cost money, and the treasury asks which one it is being "
        "asked to fund first.",
    ), (
        Option('Squeeze the plants we have.', (Research('industry', 0.5, 1),)),
        Option('Look beyond the plant districts.', (Research('construction_tech', 0.5, 1),)),
    ), picture=2),
    EventDef('off_the_line', 'Beyond the Railhead', (
        "The survey teams come back sunburnt and caked in mud. District D is nineteen provinces of open coastal plain with "
        "one real town, scattered farms and earth tracks that vanish for months in the wet season. Its coast runs up to "
        "Silvonia, and its people trade more with fishing boats than with the capital. Not one kilometre of railway reaches "
        "it, and the nearest station is a day away by truck in good weather.",
        "District F is smaller and stranger. Four provinces of hills and desert lie at the point where Glaceland, "
        "Silvonia and Luremia all meet Sfaenland, and a road from the Luremian side brings traders and livestock to a market "
        "that nobody in the capital ever licensed. Herders cross the frontiers with the seasons. The district has no post "
        "office, no clinic and no garrison, and the surveyors were the first officials many villagers had met.",
        "Both reports end with costed lists of roads, wells, classrooms and generators and no recommendation at all; the "
        "teams say the order of work is for ministers to settle. The plain has more people and more land. The desert corner "
        "has three frontiers and a trade nobody counts. Ministers are warned that whichever district waits will notice, and "
        "that the movement is already telling both of them that the capital has forgotten they exist.",
    ), (
        Option('Start with the plain.', (Stability(0.02),)),
        Option('Start with the desert corner.', (XP('army', 10), Stability(0.01))),
    ), picture=0),
    EventDef('muster', 'Three Hulls at the Quay', (
        "The muster at the naval base in District G is finished in a single morning, because there is not much to muster. "
        "Two coastal escorts and one coastal submarine lie alongside the quay with their crews, a store of shells and "
        "torpedoes, and the three dockyards that built or repair them. This is the whole of the Maritime Service, and it "
        "answers for a coast that runs along five of the country's eight districts.",
        "The inspectors write down what the hulls cannot do. The escorts can guard a coastal convoy or hunt a submarine, "
        "but not both on the same day. The submarine can watch one harbour mouth at a time. Sixty convoy hulls carry the "
        "country's oil, steel and grain along the coast every week, and none of their masters has been told what to do if "
        "a war began tomorrow. The yards can build one new hull at a time.",
        "Officers at the base divide, as small navies always do, between those who would defend the trade and those who "
        "would make the coast dangerous to approach. Both camps agree that the service needs more than three hulls. "
        "Ministers ask the plainer question first: whether a country of this size should spend scarce money at sea at all.",
    ), (
        Option('Keep the service and give it a plan.', (XP('navy', 15),)),
        Option('Spend on the land first.', (XP('army', 10), PP(15))),
    ), picture=1),
    EventDef('roll_call', 'Six Formations Answer', (
        "The roll call takes a week. In each of the three garrisons, at the Capital Centre and at the logistics centres of "
        "Districts A and B, two infantry formations parade with their six battalions and their engineer company, and "
        "inspectors count rifles, trucks, radios and spare boots. On paper the army is small but complete. On the parade "
        "ground it is smaller, because men on leave, men on courses and men who never reported all appear as gaps.",
        "The map tells a different story from the parade ground. All six formations sit in three places, and two of those "
        "places stand on a frontier or a coast. Five of the eight districts have no garrison at all, including District F, "
        "where three frontiers meet, and District D, the largest district in the country. Reaching either in a hurry would "
        "take trucks the army can barely keep running and roads that do not exist.",
        "The general staff sees three ways forward and argues over all of them: spread soldiers thinly into every district, "
        "keep them together and move them by rail, or make the most of the rough ground in the west. Each answer has its "
        "champions in the officer corps, and each has champions in the movement, which watches the army more closely than "
        "any other institution in the country.",
    ), (
        Option('Publish the roll in full.', (Stability(0.02), XP('army', 5))),
        Option('Keep the gaps between us.', (XP('army', 15), Stability(-0.01))),
    ), picture=1),
    EventDef('one_field', 'One Field, One Target', (
        "The air staff presents its count to the cabinet on a single sheet. Thirty-six fighters and twelve ground-attack "
        "aircraft fly from one air base beside the capital, with nine more fighters and four support aircraft in storage. "
        "There is one fuel store, one control tower, one runway and one repair hangar. In the wet months heavy rain closes "
        "the field for hours at a time, and on those days the whole air arm of Sfaenland sits on the ground.",
        "The pilots are keen and the aircraft serviceable, but the staff's real worry is concentration. An air arm on one "
        "field can be shut down by weather, a fire in the fuel store or a single attack. The other seven districts have no "
        "runway of any kind. District E, beyond the junction, is dry and flat in every month of the year, and the air staff "
        "has already pencilled a site there on its maps.",
        "Then there is the question of purpose. One school would keep every fighter for the defence of the capital and the "
        "plant districts against anything that flies. Another would train the air arm with the army so that it fights "
        "alongside the garrisons. The budget cannot buy both, and ministers who know little about aircraft are being asked "
        "to choose between them.",
    ), (
        Option('Survey the dispersal site now.', (XP('air', 10), PP(-10))),
        Option('Make the one field work first.', (XP('air', 15),)),
    ), picture=1),
    EventDef('three_neighbours', 'Three Neighbours on the Map Table', (
        "The crossing survey is finished, and its maps cover the cabinet table. Glaceland borders three districts, A, E "
        "and F, and the logistics centre in District A sits right on that line, with the Glacelandic yards just across it. "
        "Silvonia faces the coastal plain of District D and the hills of District F. Luremia touches only District F, where "
        "a desert road comes in from the Luremian side and herders follow it with the seasons.",
        "The briefing is less concerned with old quarrels than with everyday traffic. Herders cross District F with the "
        "seasons, fishing boats from both sides share the waters off District D, and trucks queue for hours at the District "
        "A crossing because nobody has fixed when the posts open. Every incident so far has been settled by whichever "
        "officials happened to be on duty that day, with whatever paper they had to hand.",
        "Neighbours have their own governments and their own worries, and Sfaenland can only order its own side of each "
        "line. The survey team proposes to start there: posted rules, staffed crossings and published duties. The movement "
        "complains that this is weakness dressed up as procedure. The prefects reply that a frontier where everyone knows "
        "the rules is the cheapest garrison there is.",
    ), (
        Option('Begin with the busiest crossing.', (Stability(0.02),)),
        Option('Begin with the three-frontier corner.', (XP('army', 10),)),
    ), picture=1),
    EventDef('belkan_war_far', 'A War Read in Freight Rates', (
        "At the end of March 1995 Belka is at war. Sfaenland lies a long way from that war and has no stake in it, and "
        "for a few days the news stays on the foreign pages. Then the costs arrive. Every shipping insurer sends a war-risk "
        "letter, fuel at the pumps goes up within the week, and buyers abroad who never answered Sfaenland's letters begin "
        "asking what its steel and aluminium would cost by the shipload.",
        "The movement fills the capital's halls with rallies about readiness, warning that a world at war has no place for "
        "unready countries. The prefects worry more about the railway, which suddenly has more requests for oil and metal "
        "trains than it can run. Merchant captains ask the Maritime Service whether they should sail at all. Officials who "
        "expected a quiet decade find the whole economy reacting to a war nobody here chose.",
        "The government has to decide what kind of neutral it will be. It can keep the railway, the ports and the frontier "
        "roads open to any cargo under the ordinary rules and take the fees, or it can refuse war cargo for every side and "
        "accept the cost. Either way the decision will be written into shipping papers that others will read, now and long "
        "after the war ends.",
    ), (
        Option('Let the traders decide for now.', (PP(20),)),
        Option('Prepare the customs service for checks.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, Official Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Sfaenland '
                'response is gameplay', picture=2),
    EventDef('impact_announced', 'A Fall Without a Place', (
        "In the spring of 1996 the FCU president declares that the asteroid will strike the planet and that the federation "
        "is getting ready to fight it. With that statement the asteroid table in the capital of Sfaenland stops being a "
        "curiosity. Since the warning of December "
        "1994 it has mostly read foreign bulletins aloud. Overnight every ministry wants a seat at it. Its members say at "
        "once that nobody can tell them where fragments will come down, or whether any will come near the country.",
        "What they can say is where the country is exposed. Almost every plant, every barrel of stored fuel and most of the "
        "population sit in three districts and along one railway. The single fuel silo is at the capital, the single air "
        "base beside it, and the junction that links everything lies on an open plain. The empty districts have room to "
        "spare but no roads, water or shelter for people who might need to go there.",
        "Two plans reach the cabinet within a month. One would dig shelters beneath the capital and the plant districts and "
        "stock them for weeks. The other would plan to move people out into the open districts if a fall were predicted, "
        "using the surveys and the railway. The cabinet is told plainly that the country can afford one of these well, or "
        "both of them badly.",
    ), (
        Option('Brief the districts in full.', (Stability(0.02), PP(-10))),
        Option('Prepare quietly before speaking.', (PP(20), Stability(-0.01))),
    ), citation='date anchors only, Official Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; '
                'where fragments fall is not claimed and the Sfaenland response is gameplay', picture=1),
    EventDef('roche_night', 'A Sky Everyone Watched', (
        "The night of 8 July 1999 is the one Sfaenland has prepared for since the April announcement: Ulysses crosses the "
        "Roche limit and starts to fragment. The asteroid table keeps an open line to all eight district halls and to the "
        "observers on the cloudless hills of Districts C and E. Families listen to the radio bulletins, and in some streets "
        "they listen from the doorways of the new shelters, unsure whether to go in.",
        "The preparations of three years are now judged by results rather than by plans. Shelters that flooded in the wet "
        "season, camp wells that herders had borrowed and fuel drums that went missing from the garrisons all appear in the "
        "reports by morning. So do the officials who stayed at their posts, the railwaymen who kept the junction open and "
        "the volunteers who went from door to door.",
        "By dawn the table has to choose what the country will hear. A frank account of what worked and what failed will cost "
        "some reputations and improve the next emergency plan. A reassuring summary will calm the districts and leave the "
        "failures for the auditors to find later. The ministers who sat up all night are tired, and tired ministers lean "
        "toward reassurance.",
    ), (
        Option('Publish the frank account.', (Stability(0.03), PP(-15))),
        Option('Issue a reassuring summary.', (PP(20), Stability(0.01))),
    ), citation='date anchor only, Official Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no damage in '
                'Sfaenland is claimed and the response is gameplay', picture=1),
    EventDef('century_ledger', 'Numbers Everyone Can Read', (
        "The first ten years of national accounts arrive as a thick volume with a thin summary. Output has grown modestly, "
        "public debt sits at around three tenths of it, and something like fifteen percent of assessed tax was never "
        "collected. The averages hide the districts. The three plant districts pay nearly all the tax and receive most of "
        "the spending, while the rest of the country appears in the tables mainly as columns of small numbers.",
        "The volume is honest about the decade's choices. It shows what the railway cost and earned, what the plant "
        "districts gained or lost from the policies of the 1990s, and how much the Ulysses preparations consumed. It also "
        "shows money that cannot be traced: payments for works never built and allowances paid to officials who were not at "
        "their posts. Those pages are short, and everyone in the capital reads them first.",
        "The government must now decide what the accounts are for. It can make them the basis of every budget, published "
        "each year with the same tables, so that future arguments start from shared numbers. Or it can treat them as a "
        "one-off report and return to old habits. The districts that appear only as small numbers are watching which "
        "choice is made.",
    ), (
        Option('Publish the tables every year.', (Stability(0.02), PP(-10))),
        Option('Treat it as a single report.', (PP(25),)),
    ), picture=2),
    EventDef('usean_war', 'War Over Another Continent', (
        "The founding of the ISAF in August 2003, after the FCU calls on Erusea to quit San Salvacion, turns a crisis over a "
        "seized country and its railguns into a coalition war across the Usean continent and its seas. Sfaenland stands "
        "outside it and expects to stay there. Its ministers have lived through something like this before; they send for "
        "the 1995 files and find the questions much the same, only larger.",
        "Freight insurers cancel policies on Usean routes and rewrite the rest. Fuel prices rise, and buyers once again ask "
        "about Sfaenland's steel, aluminium and oil. Reports of railguns turned against aircraft unsettle the air staff, "
        "whose fields suddenly seem very few. The movement holds rallies about readiness, and the frontier offices ask "
        "whether the cargo rules written in 1995 still apply to a war on another continent.",
        "The government can apply its old answer, whatever it was, and let the Usean war run past the country. Or it can "
        "use the war to reopen questions it has avoided: how many aircraft, how many escorts, how much fuel in the silo. "
        "Ministers know that each of those questions has a price, and that the war gives them a reason to ask but not the "
        "money to answer.",
    ), (
        Option('Apply the 1995 rules again.', (Stability(0.02),)),
        Option('Reopen the defence questions.', (WarSupport(0.03), PP(-15))),
    ), citation='date anchors only, Official Chronicle rows 2003 / SUMMER and 2003 / 08.22 in tools/lore/chronicle.json; '
                'fired only after the mod sets ac_ucw_isaf_formed; no Sfaenland part in the war is claimed', picture=2),
)

# --- branches ------------------------------------------------------------------------------------
POLITICS = Branch('pol', 'The Readiness Order', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_notice', 'The Postponement Notice',
          "Every four years the election calendar of Sfaenland falls due, and every four years the National Administration "
          "posts the same notice in each district hall: the vote waits while the country stays on its readiness footing. "
          "The new notice is typeset and ready. Before it is signed, the Administration asks its own lawyers what the "
          "readiness order really requires, a question nobody has put in writing for years.",
          ('document', 'security'), reward=(Idea('readiness_order'), Event('postponement'))),
    Focus('pol_camps', 'Who Stands Behind the Fifty',
          "Half the country tells pollsters it backs the national movement, and nearly as many want no party in power and "
          "put their faith in the prefects who run the districts. Teams from the capital university spend a season in garrison towns, "
          "plant streets and empty districts asking why. The study costs the Administration a quiet year, and its findings "
          "will please no camp entirely.",
          ('assembly', 'scales'), after=('pol_notice',), reward=(TimedIdea('camps_study', 365),)),
    Focus('pol_rolls', 'Rolls of Residents in Eight Districts',
          "Nobody knows exactly who would be entitled to vote, because the residents' rolls were last checked when the open "
          "districts held even fewer people than they do now. Clerks visit every town and farm with ledgers. The rolls serve "
          "tax offices, school planners and ration clerks as well as any future ballot, which is the argument that finally "
          "wins them a budget line.",
          ('ballot', 'document'), after=('pol_notice',), reward=(Flag('resident_rolls'), Stability(0.01))),
    Focus('pol_path_charter', 'Draft a Charter in the Districts',
          "The democratic camp is tiny but has a plan: a drafting room in each of the eight districts, sending clauses to a "
          "national committee, so that the charter belongs to the districts before the capital signs it. The movement calls "
          "it a scheme for clerks. It is slow, and it invites every local quarrel into the text, which its authors insist "
          "is the whole point.",
          ('assembly', 'ballot'), after=('pol_camps',), cost=10, exclusive=('pol_path_prefects', 'pol_path_movement'),
          reward=(SwapIdea('readiness_order', 'charter_rooms'),)),
    Focus('pol_path_prefects', 'Leave the Districts to the Prefects',
          "The non-party camp wants no constitutional adventure. It would confirm the district prefects, the officials who "
          "already run water, schools and roads, as the government in their own right, answerable to a council of their "
          "peers rather than to voters or to a movement. It is the least disruptive answer and the least inspiring, and it "
          "leaves half the country outside the door.",
          ('command', 'document'), after=('pol_camps',), cost=10, exclusive=('pol_path_charter', 'pol_path_movement'),
          reward=(SwapIdea('readiness_order', 'prefect_rule'),)),
    Focus('pol_path_movement', 'The Movement Asks for the Seals',
          "The national movement is strongest in the garrison towns beside the two logistics centres and in the plant "
          "streets of the capital. Its organisers promise discipline, full readiness and an end to government by "
          "postponement notice. Opening a path to power for it wins half the country at a stroke. The other half fears that "
          "a movement given the seals will never hand them back.",
          ('medal', 'security'), after=('pol_camps',), cost=10, exclusive=('pol_path_charter', 'pol_path_prefects'),
          reward=(SwapIdea('readiness_order', 'movement_pressure'),)),
    Focus('pol_regime_chamber', 'Convene the Chamber of Eight Districts',
          "The finished charter goes before an assembly chosen from the fresh rolls, with one list for each district and a "
          "national list above them, and the Administration hands the seals to a cabinet the chamber chooses. Democrats "
          "begin with almost no supporters of their own. The first sessions are fragile, and every faction outside the hall "
          "waits to see whether the arrangement survives its first budget.",
          ('ballot', 'assembly'), after=('pol_path_charter',), cost=10, requires=(HasFlag('resident_rolls'),),
          exclusive=('pol_regime_prefects', 'pol_regime_movement'),
          reward=(Regime('district_chamber'), Stability(-0.02))),
    Focus('pol_regime_prefects', 'Seat the Council of Prefects',
          "The eight district prefects and the heads of the main ministries sit as a standing council that governs "
          "collectively and publishes its minutes every week. The council promises competent government and an election at "
          "some future date it declines to name. Plant managers and officials are relieved. The movement calls the council "
          "the postponement notice with a permanent address.",
          ('command', 'scales'), after=('pol_path_prefects',), cost=10,
          exclusive=('pol_regime_chamber', 'pol_regime_movement'), reward=(Regime('prefect_council'),)),
    Focus('pol_regime_movement', 'The Garrison Directorate Takes Office',
          "A directorate drawn from the movement and from officers of the three garrisons replaces the Administration and "
          "governs by decree under the very readiness order the movement once mocked. Readiness becomes the purpose of the "
          "state instead of its excuse. The garrison towns celebrate. Officials of the old Administration are asked to sign "
          "declarations of loyalty, and some of the most capable resign.",
          ('security', 'medal'), after=('pol_path_movement',), cost=10,
          exclusive=('pol_regime_chamber', 'pol_regime_prefects'),
          reward=(Regime('garrison_directorate'), WarSupport(0.03))),
    Focus('pol_chamber_questions', 'Question Time Every Week',
          "Ministers answer questions in the chamber every week, and the district papers print the answers the next "
          "morning. It is tiresome for ministers and very popular in the open districts, whose deputies finally have a place "
          "to ask about roads and clinics. Government moves a little more slowly, and it can no longer hide its mistakes "
          "behind the readiness order.",
          ('assembly', 'communications'), after=('pol_regime_chamber',),
          exclusive=('pol_prefects_terms', 'pol_directorate_brigades'),
          reward=(SwapIdea('charter_rooms', 'question_time'),)),
    Focus('pol_prefects_terms', 'Prefects Serve Three-Year Terms',
          "Prefects now rotate between districts every three years, so that no official settles into a district as its "
          "owner and every district gets fresh eyes on its accounts. Rotation breaks local networks, the corrupt ones and "
          "the useful ones alike. The council accepts the loss, because the alternative is eight small fiefdoms that obey "
          "the capital only on paper.",
          ('document', 'scales'), after=('pol_regime_prefects',),
          exclusive=('pol_chamber_questions', 'pol_directorate_brigades'),
          reward=(SwapIdea('prefect_rule', 'prefect_terms'),)),
    Focus('pol_directorate_brigades', 'Readiness Brigades in Every District',
          "The directorate raises readiness brigades of young volunteers in every district: drill at weekends, road work "
          "during the week and a uniform that opens doors to jobs. The brigades bring labour to the empty districts and "
          "parades to the capital. They also put a disciplined body outside the army's chain of command, which the garrison "
          "officers notice and do not forget.",
          ('training', 'security'), after=('pol_regime_movement',),
          exclusive=('pol_chamber_questions', 'pol_prefects_terms'),
          reward=(SwapIdea('movement_pressure', 'readiness_brigades'),)),
    Focus('pol_press', 'Licences for District Newspapers',
          "Most newspapers are printed in the capital and live on Administration notices. Licences for new district papers, "
          "with a small subsidy for newsprint and presses, give the districts a voice whoever governs in the capital. Some "
          "of the papers will be scurrilous and a few will be bought outright. The Administration accepts both risks in "
          "order to hear what the districts actually say.",
          ('communications', 'document'), after=('pol_rolls',), reward=(Idea('district_papers'),)),
    Focus('pol_pay', 'Pay Scales Published for Officials',
          "The Administration's officials are paid on scales that nobody outside the payroll office has seen. Publishing "
          "them district by district reveals prefects who earn more than ministers and clerks who earn less than teachers. "
          "The figures embarrass the Administration and anger officials whose allowances are exposed. They also make "
          "loyalty harder to buy with quiet raises, whoever governs next.",
          ('economy', 'document'), after=('pol_rolls',), reward=(Idea('open_pay_scales'),)),
    Focus('pol_withdrawn', 'The Notice Is Withdrawn',
          "Whichever government now holds the seals, the postponement notice is no longer printed. A chamber, a council or "
          "a directorate governs in its own name and must justify itself on its own terms. The clerks who typeset the "
          "notice every four years find other work. The country loses a familiar excuse and gains a government that has to "
          "answer for what it does.",
          ('peace', 'document'), after_any=('pol_chamber_questions', 'pol_prefects_terms', 'pol_directorate_brigades'),
          reward=(Flag('notice_withdrawn'), Stability(0.03))),
))

LINE = Branch('line', 'The Main Line and Its Junction', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('line_census', 'Count the Wagons on the Main Line',
          "One main line carries almost everything Sfaenland moves: from the Capital Centre to the junction in District E, "
          "on through District C to the logistics centre in District B, with branches to District A and to the naval base "
          "in District G. Nobody has counted the wagons in years. A census of rolling stock, crews and traffic must come "
          "before any railway policy.",
          ('rail', 'document'), reward=(Idea('freight_ledger'), Event('junction_report'))),
    Focus('line_sidings', 'Sidings at the Junction',
          "The junction in District E is a set of points on a rainless plain, with a signal box, a water tower and no town. "
          "Freight for three branches waits on the running line because no siding can hold a full train. Sidings, a "
          "passing loop and a road out to the nearest villages cost little money and a great deal of engineers' time.",
          ('rail', 'tools'), after=('line_census',), reward=(Build('infrastructure', 2, 77),)),
    Focus('line_halts', 'Halts Across District C',
          "Trains run straight through the dry forested hills of District C; there is not one platform between the junction "
          "and the southern coast. Fourteen provinces lie beside the track with no road worth the name. A string of halts with loading platforms and graded "
          "approach roads lets villages put timber and livestock on the train. Each halt also needs a stationmaster willing "
          "to live beside it.",
          ('rail', 'civil'), after=('line_census',),
          reward=(Build('infrastructure', 1, 51), Research('train_tech', 0.5, 1))),
    Focus('line_treasury', 'The Treasury Runs the Railway',
          "One school wants the railway kept as a single public undertaking, its fares set by the treasury and its surplus "
          "spent on track. Planning is simple and every district gets a service whether it pays or not. The railway stays "
          "slow to change and loses money on the quiet branches. The army approves, because it knows exactly whom to call "
          "in a crisis.",
          ('economy', 'rail'), after=('line_sidings',), cost=10, exclusive=('line_lease',),
          reward=(SwapIdea('freight_ledger', 'treasury_railway'),)),
    Focus('line_lease', 'Lease the Branches to Freight Houses',
          "With the traffic figures published, private freight houses can bid for the branches. The track stays public, but "
          "each branch is leased to an operator that sets its own timetable and charges what the cargo will bear. Service "
          "improves quickly where oil and steel pay and withers where they do not. The leases bring revenue now and "
          "arguments about the quiet branches later.",
          ('economy', 'logistics'), after=('line_sidings',), cost=10, exclusive=('line_treasury',),
          requires=(HasFlag('traffic_published'),), reward=(SwapIdea('freight_ledger', 'leased_branches'),)),
    Focus('line_wagon_shops', 'Wagon Shops at the Junction',
          "The public railway builds its own wagon and repair shops beside the new sidings in District E, so that rolling "
          "stock no longer travels to the capital for every overhaul. The shops are the first plant of any kind in the "
          "district. Fitters must be persuaded to move to a dry plain with no town, and housing them costs as much as the "
          "sheds themselves.",
          ('tools', 'rail'), after=('line_treasury',), reward=(Build('industrial_complex', 1, 77),)),
    Focus('line_bonded', 'Bonded Depots on the Southern Line',
          "The freight houses want warehouses where cargo can wait, duty unpaid, until it is sold or shipped. Bonded depots "
          "go up beside the District C halts, close enough to the coast to serve exporters. They create jobs in a district "
          "that has none. Customs officers point out, correctly, that bonded warehouses are also where smuggling most likes "
          "to hide.",
          ('logistics', 'economy'), after=('line_lease',), reward=(Build('industrial_complex', 1, 51),)),
    Focus('line_culverts', 'Culverts for the Capital Plain',
          "The Capital District lies in country where heavy rain falls on many days for much of the year, while the junction "
          "district beyond it sees no rain at all. Washouts on the capital approaches close the line each wet season. New "
          "culverts, raised embankments and drainage ditches keep trains moving when the plain floods, at the price of a "
          "season of single-track working.",
          ('bridge', 'rail'), after=('line_halts',), reward=(Build('infrastructure', 1, 0), Stability(0.01))),
    Focus('line_naval_spur', 'Rebuild the Naval Spur',
          "The branch that leaves the junction in District E and crosses District C to the naval base in District G carries "
          "fuel, shells and spare parts for the Maritime Service. Its bridges were built for lighter trains. Rebuilding them and "
          "relaying the track lets the yards take steel plate by rail instead of by coastal barge, and gives the service a "
          "supply line it can rely on.",
          ('navy', 'rail'), after=('line_halts',), reward=(Build('infrastructure', 1, 198), XP('navy', 10))),
    Focus('line_a_branch', 'Heavier Rail for the District A Branch',
          "The branch from the junction to the logistics centre in District A climbs into forest and hills where the oil, "
          "steel and aluminium of the west are worked. Ore and fuel trains run half loaded because the old rails cannot "
          "carry more weight. Heavier rail and new ballast let full trains reach the plants. The work closes the branch for "
          "a season, and District A's managers complain throughout.",
          ('rail', 'industry'), after=('line_sidings',),
          reward=(Build('infrastructure', 1, 10), Research('construction_tech', 0.5, 1))),
    Focus('line_through', 'Through Trains to the Southern Coast',
          "Whoever runs the railway, the aim is the same: a train loaded at the Capital Centre reaching the logistics "
          "centre in District B without waiting for a free track. Signals, loops and one timetable for the whole network "
          "make it possible. The first through train is a modest event. The second, arriving on schedule, is the real "
          "achievement, and the army takes careful note of it.",
          ('rail', 'communications'), after_any=('line_wagon_shops', 'line_bonded'),
          reward=(Flag('through_trains'), Research('logistics_tech', 0.5, 1))),
))

PLANTS = Branch('plant', 'Three Districts With No Free Plot', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('plant_inventory', 'Every Plot in the Plant Districts',
          "Every one of the eight civilian plants and six arms works in the country stands in the Capital District or in "
          "Districts A and B, and the land zoned for industry there has no empty plot left. New capacity must go elsewhere or "
          "come from working the existing plants harder. An inventory of machines, shifts and stocks in those three "
          "districts tells ministers which course costs less.",
          ('industry', 'document'), reward=(Idea('plant_census_file'), Event('no_free_plot'))),
    Focus('plant_second_shift', 'A Second Shift at the Capital Plants',
          "The capital's plants run one shift and stand idle for the rest of the day. A second shift doubles the hours their "
          "machines work without a single new plot. It needs workers the capital lacks, housing they cannot find and "
          "overtime the plants can barely pay. For two years output rises, and so do the noise and the rents in the plant "
          "streets.",
          ('industry', 'civil'), after=('plant_inventory',), reward=(TimedIdea('second_shift', 730),)),
    Focus('plant_wage_boards', 'Wage Boards for the Plant Streets',
          "Wages are set plant by plant, and the gaps between neighbours on the same street cause stoppages every year. "
          "District wage boards, with managers, workers and an official in the chair, set common rates for common jobs. "
          "Managers lose bargaining power and the boards raise the wage bill. Stoppages become rarer and shorter, which the "
          "second shift badly needs.",
          ('scales', 'civil'), after=('plant_second_shift',), reward=(Idea('wage_boards'),)),
    Focus('plant_alloy', 'Aluminium Before Everything',
          "All three plant districts produce aluminium, and the alloy school wants that metal to lead the economy: rolled "
          "sheet, extrusions and castings for aircraft, vehicles and export. Aluminium needs cheap power and skilled hands, "
          "and it pays well when it sells. It also ties the country's fortunes to world metal prices that nobody in "
          "Sfaenland can influence.",
          ('industry', 'air'), after=('plant_inventory',), cost=10, exclusive=('plant_crude', 'plant_girders'),
          reward=(SwapIdea('plant_census_file', 'alloy_priority'), Flag('econ_alloy'))),
    Focus('plant_crude', 'Let the Crude Pay First',
          "The fuel school notes that the oil of the three plant districts, with the silo at the capital, already keeps the "
          "trains and the army moving. It would refine more, store more and sell the surplus abroad, and use the revenue to "
          "pay for everything else. Oil earns quickly and simply. Plants that do not touch oil must wait their turn for "
          "investment.",
          ('economy', 'logistics'), after=('plant_inventory',), cost=10, exclusive=('plant_alloy', 'plant_girders'),
          reward=(SwapIdea('plant_census_file', 'crude_first'), Flag('econ_crude'))),
    Focus('plant_girders', 'Steel for Girders and Rails',
          "The steel school wants the country's steel kept at home and turned into girders, rails and bridge spans for the "
          "empty districts. Building at home creates work in every district and makes later growth cheaper. Steel sold "
          "abroad would earn more today. The school answers that a country with half its districts unbuilt should build "
          "before it sells.",
          ('bridge', 'industry'), after=('plant_inventory',), cost=10, exclusive=('plant_alloy', 'plant_crude'),
          reward=(SwapIdea('plant_census_file', 'girders_first'),)),
    Focus('plant_cable_works', 'Alloy Cable for the Power Lines',
          "The empty districts need power lines before they can host plants, and aluminium is the metal those lines are "
          "strung with. A wire and cable works beside the junction in District E draws domestic alloy into conductor for "
          "every new line the government plans. The works needs skilled hands from the capital, housing on a plain with no "
          "town, and contracts that only the state can sign.",
          ('tools', 'industry'), after=('plant_alloy',),
          reward=(Build('industrial_complex', 1, 77), Research('industry', 0.5, 1))),
    Focus('plant_refinery', 'A Refinery Beside the Southern Line',
          "Crude from the plant districts goes to a new refinery in District C, beside the main line and near the coast "
          "where tankers could one day load. The site is dry and empty, which suits a plant nobody wants near their homes. "
          "The refinery widens the country's fuel margin and draws a pipeline route that the defence staff immediately asks "
          "to guard.",
          ('industry', 'logistics'), after=('plant_crude',),
          reward=(Build('industrial_complex', 1, 51), Research('synth_resources', 0.5, 1))),
    Focus('plant_bridge_yard', 'Girder Yards on the District D Plain',
          "A fabrication yard on the District D plain cuts and rivets the girders for the bridges and sheds the empty "
          "districts need, close to where they will stand. Steel arrives by truck from the nearest railhead until the plain "
          "has a line of its own. The yard becomes the largest employer the district has known, and its first order is for "
          "its own access road.",
          ('bridge', 'tools'), after=('plant_girders',),
          reward=(Build('industrial_complex', 1, 65), Build('infrastructure', 1, 65))),
    Focus('plant_proof', 'A Proof House for the Arms Works',
          "Rifles, mortar bombs and shells leave the six arms works with nothing but their makers' word that they work. A "
          "proof house on the capital plain test-fires a sample from every batch and publishes the rejection rate of each "
          "works. Managers hate the league table. The formations stop receiving crates in which one round in fifty "
          "misfires, and the Physical Sustainment priority finally has a measure.",
          ('tools', 'security'), after=('plant_inventory',),
          reward=(Idea('proof_house'), Research('artillery', 0.5, 1))),
    Focus('plant_export', 'Export Desks for Metal and Fuel',
          "Whatever the plant districts make first, someone must sell what the country does not use. An export office with "
          "desks for metal, fuel and machinery finds buyers, arranges credit and checks that ships and payments arrive. It "
          "costs salaries and patience. It also gives the country its first commercial agents abroad, which the foreign "
          "ministry would have preferred to control itself.",
          ('diplomacy', 'economy'), after_any=('plant_alloy', 'plant_crude', 'plant_girders'),
          reward=(Idea('export_desks'),)),
))

OPEN = Branch('open', 'The Plain and the Desert Corner', 1992, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('open_survey', 'Survey the Districts Off the Line',
          "Two districts lie beyond the railway altogether. District D is nineteen provinces of coastal plain with one town "
          "and no road network, and District F is four provinces of hills and desert where three frontiers meet. Survey "
          "teams with trucks and pack animals map tracks, wells and villages. Their reports decide where the first public "
          "money goes.",
          ('civil', 'document'), reward=(Flag('plain_surveyed'), Event('off_the_line'))),
    Focus('open_d_road', 'An All-Weather Road Across District D',
          "The District D plain lies in a belt of heavy seasonal rain, and its earth tracks turn to mud for months at a "
          "time. A raised, gravelled road from the plain town toward the Capital District, with bridges over the worst "
          "streams, keeps the district reachable in every season. The road is long, flat and dull, and it costs more than "
          "any other public work of the decade.",
          ('logistics', 'civil'), after=('open_survey',), reward=(Build('infrastructure', 2, 65), PP(-25))),
    Focus('open_f_track', 'A Road Up to the Desert Corner',
          "The only way into District F from the capital is a dirt track that climbs into the hills and fades in the "
          "desert. Grading it into a proper road, with water points a day's drive apart, opens the district to trucks and "
          "officials. It also makes the three-frontier corner far easier to reach from every direction, a point the "
          "garrison officers have written into their own estimates.",
          ('logistics', 'security'), after=('open_survey',), reward=(Build('infrastructure', 2, 189),)),
    Focus('open_town_power', 'Power and Water for the Plain Town',
          "The one town on the District D plain draws water from wells and power from a diesel set that fails in the wet "
          "season. A small power station, a water main and a pumping house make it a place where a clinic, a school and a "
          "workshop can open. Everything else planned for the plain depends on this unglamorous and expensive first step.",
          ('industry', 'civil'), after=('open_d_road',),
          reward=(Build('industrial_complex', 1, 65), Stability(0.01))),
    Focus('open_farms', 'Grain Leases on the Plain',
          "The farming school would lease the District D plain in large blocks to grain growers, with credit for tractors "
          "and storage, and let the district feed the capital. Leases settle people on the land and need no factories. They "
          "also concentrate the plain in a few hands, and the grain still travels by road until a railway reaches the "
          "district.",
          ('economy', 'civil'), after=('open_d_road',), exclusive=('open_works',), reward=(Idea('grain_leases'),)),
    Focus('open_works', 'Plant Towns on the Plain',
          "The industrial school wants the plain town turned into a plant town, with housing estates, a power grid and new "
          "works, so that District D stops exporting its young people to the capital. It costs far more than farm leases "
          "and takes longer to repay. If it works, the country gains a fourth plant district with room still to spare.",
          ('industry', 'rebuild'), after=('open_d_road',), cost=10, exclusive=('open_farms',),
          reward=(Build('industrial_complex', 1, 65), Idea('plain_works'))),
    Focus('open_slip', 'A Slipway on the District D Coast',
          "District D has a long coast and not one yard. A small slipway at the shore nearest the town can build and repair "
          "fishing boats, harbour craft and launches for the Maritime Service. It trains shipwrights outside District G for "
          "the first time. It is small and exposed to the weather, and close enough to the Silvonian frontier that the navy "
          "wants a say in its design.",
          ('navy', 'tools'), after=('open_town_power',), reward=(Build('dockyard', 1, 65),)),
    Focus('open_f_market', 'The Market at the Desert Crossing',
          "Traders coming up the desert road from Luremia have long stopped at a market in District F that no ministry ever "
          "licensed. With the crossing ledger in hand, the government recognises the market: a weighbridge, a customs clerk, "
          "a well and a shaded yard. Trade comes into the open and the district earns a little revenue. Some traders find "
          "the new forms reason enough to stay away.",
          ('economy', 'diplomacy'), after=('open_f_track',), requires=(HasFlag('desert_ledger'),),
          reward=(TimedIdea('desert_market', 1095),)),
    Focus('open_f_posts', 'Watch Posts at the Three-Frontier Corner',
          "District F is the only place where Sfaenland meets Glaceland, Silvonia and Luremia at once, and nothing watches "
          "it except a few herders. A radar post on the highest hill and a small barracks near the crossing put the corner "
          "under observation. Neighbours will see the mast. The defence staff argues that an unwatched corner invites "
          "misunderstanding far more than a visible one.",
          ('radar', 'security'), after=('open_f_track',), reward=(Build('radar_station', 1, 189), XP('army', 5))),
    Focus('open_schools', 'Boarding Schools for the Off-Line Districts',
          "Children in the villages of District D and the hills of District F walk half a day to a school, or do not go at "
          "all. Boarding schools in the plain town and at the desert crossing, with buses where the new roads allow, bring "
          "them in for the term. Parents lose labour on the farms. A generation gains the reading and arithmetic that the "
          "plant districts will want to hire.",
          ('civil', 'training'), after_any=('open_town_power', 'open_f_posts'), reward=(Idea('boarding_schools'),)),
    Focus('open_joined', 'Two Districts on the Timetable',
          "When the plain road and the desert track both carry regular buses, mail vans and trucks, Districts D and F stop "
          "being blank spaces on the ministry maps. Officials can reach them within a day, and their people can reach the "
          "capital. The government marks the moment with a national timetable that, for once, includes every district in "
          "the country.",
          ('rail', 'peace'), after=('open_f_track',), after_any=('open_farms', 'open_works'),
          reward=(Flag('off_line_joined'), Stability(0.02))),
))

SEA = Branch('sea', 'The Maritime Service at District G', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('sea_muster', 'Count the Hulls at District G',
          "Two coastal escorts and a single coastal submarine make up the entire Maritime Service, berthed at the naval base "
          "in District G beside the three dockyards of the country. It guards a coast that runs along five of the eight districts. A full "
          "muster of crews, stores and hulls shows what the service can actually do in a week, and how little it could do "
          "in a war.",
          ('navy', 'document'), reward=(Idea('maritime_roll'), Event('muster'))),
    Focus('sea_slip', 'A Fourth Slip at District G',
          "The three yards at District G can build an escort or a submarine at a time, but not both, and repairs queue "
          "behind new work. A fourth slip on the last free ground beside the naval base lets the yards repair and build at "
          "once. Once it is laid there is no room left in District G for any further yard, and the next one must go "
          "elsewhere.",
          ('navy', 'tools'), after=('sea_muster',), reward=(Build('dockyard', 1, 198),)),
    Focus('sea_cinigrad', 'The Cinigrad Submarine Announcement',
          "In September 1991 a new class of very large submarines is unveiled at a political convention in Cinigrad, "
          "Yuktobania, and an Osean minister mocks the announcement in public. Officers at District G read every report. A "
          "service of three hulls cannot match such ships. It can decide what kind of small navy is useful in a world where "
          "great powers build submarines like these.",
          ('submarine', 'communications'), after=('sea_muster',), requires=(After('1991.9.2'),),
          reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
    Focus('sea_subs', 'Submarines Hold the Approaches',
          "The submarine case is that Sfaenland will never command the sea but can make its own approaches costly to use. "
          "A flotilla of coastal submarines, quiet and cheap to crew, would watch the harbour mouths of Districts B, C and "
          "G. Submarines do little in peacetime that anyone can see. The merchant captains who wanted escorts get none of "
          "them.",
          ('submarine', 'security'), after=('sea_cinigrad',), cost=10, exclusive=('sea_escorts',),
          reward=(SwapIdea('maritime_roll', 'submarine_flotilla'),)),
    Focus('sea_escorts', 'Escorts for the Coastal Convoys',
          "The escort school answers that the country's sixty convoy hulls carry oil, steel and grain along the coast every "
          "week, and that protecting them matters more than threatening anyone. More escorts, better sonar and a convoy "
          "plan keep trade moving in a crisis. Escorts are visible, useful and expensive, and they leave the harbour mouths "
          "to mines and patrol craft.",
          ('navy', 'logistics'), after=('sea_cinigrad',), cost=10, exclusive=('sea_subs',),
          reward=(SwapIdea('maritime_roll', 'coastal_escorts'),)),
    Focus('sea_sub_school', 'A Submarine School at the Naval Base',
          "Submarine crews cannot be trained aboard an escort. A school with a training boat, a diving tank and an attack "
          "trainer turns volunteers into crews within a year. It is expensive for so few graduates, and its instructors are "
          "the service's best officers taken off the boats. Without it, every new submarine would wait at the quay for a "
          "crew that does not exist.",
          ('submarine', 'training'), after=('sea_subs',),
          reward=(XP('navy', 25), Research('naval_equipment', 0.75, 1))),
    Focus('sea_convoy_plan', 'A Convoy Plan for Sixty Hulls',
          "Every coastal freighter is assigned to a convoy group, a route and a harbour of refuge, and its master is trained "
          "in signals. The plan lives in a binder at the naval base and on a wall chart in each port. Shipowners grumble "
          "about paperwork and drills. In a crisis, sixty hulls will move as one fleet under escort rather than as sixty "
          "separate gambles.",
          ('logistics', 'document'), after=('sea_escorts',), reward=(Idea('convoy_groups'),)),
    Focus('sea_bunkers', 'Fuel Bunkers at the Naval Base',
          "With crude paying first, the naval base can store fuel for months of patrols rather than weeks. Buried tanks, a "
          "pump house and a pipe from the railhead keep the Maritime Service at sea when the trains stop. The tanks are an "
          "obvious target and need guarding. Escorts and submarines alike can now plan their patrols by the season instead "
          "of by the delivery.",
          ('shelter', 'navy'), after=('sea_slip',), requires=(HasFlag('econ_crude'),),
          reward=(Idea('naval_bunkers'), Build('infrastructure', 1, 198))),
    Focus('sea_coast_watch', 'Coast Watchers Along Five Districts',
          "Lookouts in lighthouses, fishing villages and hilltops along the coasts of Districts A, B, C, D and G report "
          "every ship they see to the naval base by telephone. A radar set on the District C coast covers the busiest "
          "stretch. The watch costs little and relies on volunteers, and it gives the Maritime Service eyes far beyond its "
          "three hulls.",
          ('radar', 'navy'), after=('sea_muster',), reward=(Idea('coast_watchers'), Build('radar_station', 1, 51))),
    Focus('sea_design_office', 'An Escort Designed at Home',
          "The yards at District G have only ever built foreign designs under licence. A small design office, staffed with "
          "naval architects from the capital university, attempts the first escort drawn at home: modest, robust and suited "
          "to the short seas off the coast. The first design will be heavier and slower than hoped. The second will be "
          "better, and the office will still exist to draw it.",
          ('science', 'navy'), after_any=('sea_sub_school', 'sea_convoy_plan'),
          reward=(Idea('design_office'), Research('naval_equipment', 1.0, 1))),
))

ARMY = Branch('army', 'Six Formations in Three Garrisons', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('army_roll', 'Roll Call at the Three Garrisons',
          "The whole army is six infantry formations. Each has six battalions and an engineer company, and they are "
          "stationed two by two: at the Capital Centre, at the logistics centre of District A and at that of District B. Five "
          "districts have no garrison at all. A roll call of men, rifles, trucks and spares gives the general staff its first "
          "honest picture of the force.",
          ('security', 'document'), reward=(Idea('three_garrisons'), Event('roll_call'))),
    Focus('army_trucks', 'A Motor Pool for Eight Hundred Trucks',
          "The depots hold some eight hundred motor vehicles, scattered among the garrisons and maintained by whoever "
          "happens to be nearby. One motor pool with workshops, mechanics and a fuel allocation keeps them running and lets "
          "the staff move a formation by road in days rather than weeks. Garrison commanders lose trucks they had come to "
          "treat as their own.",
          ('logistics', 'tools'), after=('army_roll',), reward=(Idea('motor_pool'),)),
    Focus('army_home', 'Home Companies for the Empty Districts',
          "One school wants a company of local reservists in every district without a garrison, trained at weekends and "
          "armed from a district armoury. Home companies put soldiers in Districts C to G at little cost and bind those "
          "districts to the army. They are lightly equipped and slow to mobilise, and they could delay a determined attack "
          "but never stop one.",
          ('civil', 'security'), after=('army_roll',), cost=10, exclusive=('army_rail', 'army_hills'),
          reward=(SwapIdea('three_garrisons', 'home_companies'),)),
    Focus('army_rail', 'A Reserve That Rides the Main Line',
          "Another school would keep the six formations concentrated and move them by train to wherever they are needed, "
          "with loading ramps at every halt and rolling stock held ready. The plan rests on the through trains the railway "
          "now runs. It leaves Districts D and F, which no line reaches, covered only by the days it takes to march there.",
          ('rail', 'security'), after=('army_roll',), cost=10, exclusive=('army_home', 'army_hills'),
          requires=(HasFlag('through_trains'),), reward=(SwapIdea('three_garrisons', 'line_reserve'),)),
    Focus('army_hills', 'Hill Battalions for District A',
          "A third school points out that the army already trains mountain troops and that the forest, hills and mountain "
          "of District A are the roughest ground on any frontier. It would convert two formations into hill battalions with "
          "pack transport, radios and their own engineers. Garrisons elsewhere would thin out. The western hills would get "
          "the best soldiers the army has, and the plains would have to trust the railway.",
          ('training', 'security'), after=('army_roll',), cost=10, exclusive=('army_home', 'army_rail'),
          reward=(SwapIdea('three_garrisons', 'hill_battalions'),)),
    Focus('army_engineers', 'Engineer Companies on Road Duty',
          "Each formation's engineer company spends half the year building roads and bridges in districts that lack them, "
          "starting around the junction in District E. Soldiers learn their trade on real work, and villages get roads at "
          "the price of rations. Field training suffers a little. For many villagers the army becomes the only part of the "
          "state they ever meet.",
          ('tools', 'bridge'), after=('army_trucks',), reward=(Build('infrastructure', 1, 77), XP('army', 10))),
    Focus('army_ranges', 'Live-Fire Ranges in District E',
          "The plains and hills of District E see no rain in any month, which makes them the one place in the country where "
          "formations can train year-round without mud. Ranges, a tented camp and a water pipeline turn empty land into a "
          "training area. Herders lose grazing. Formations gain a place to fire live rounds and practise movement at full "
          "scale.",
          ('training', 'tools'), after=('army_trucks',), reward=(TimedIdea('range_season', 730), XP('army', 10))),
    Focus('army_staff', 'A Staff College at the Capital Centre',
          "Officers learn staff work on the job, which means the three garrisons plan in three different ways. A staff "
          "college at the Capital Centre teaches one method of orders, supply and movement to every captain who hopes to "
          "command. Each course takes good officers away from their units. Plans written afterwards can be read by anyone "
          "in the army.",
          ('command', 'document'), after=('army_roll',), reward=(Idea('staff_college'),)),
    Focus('army_arms_works', 'An Arms Works at the Junction',
          "Every arms works stands in the three plant districts, two of those districts on the coast and one on a frontier. "
          "A new works beside the junction in District E, inland and on the railway, builds rifles and mortars where no "
          "landing could quickly reach it. The site has no town and few workers. The general staff considers that a fair "
          "price for depth.",
          ('industry', 'security'), after=('army_staff',), reward=(Build('arms_factory', 1, 77),)),
    Focus('army_exercise', 'The First Three-Garrison Exercise',
          "For the first time all six formations take the field together, moving from their garrisons to an exercise area "
          "under one headquarters. The exercise tests the motor pool, the staff college graduates and whichever doctrine the "
          "army chose. Much goes wrong, as it should. Umpires write a frank report, and the general staff decides to "
          "publish most of it.",
          ('medal', 'training'), after=('army_staff',), after_any=('army_home', 'army_rail', 'army_hills'),
          reward=(XP('army', 25), Flag('field_exercise'))),
))

AIR = Branch('air', 'Forty-Eight Aircraft, One Apron', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_apron', 'Every Aircraft on One Apron',
          "Thirty-six fighters and twelve ground-attack aircraft share a single air base beside the capital, with thirteen "
          "more airframes in storage. One airfield means one fuel store, one control tower and one target. Before anything "
          "else, the air staff counts what can fly today, what waits for parts and what would still be flying if that one "
          "field were shut for a week.",
          ('air', 'runway'), reward=(Idea('single_apron'), Event('one_field'))),
    Focus('air_runway', 'A Longer Runway at the Capital Field',
          "The capital field has one runway, short for loaded aircraft in the heavy rain of the wet months. Lengthening it, "
          "adding a parallel taxiway and laying hardstands lets the wing launch in pairs and recover in bad weather. The "
          "works close the field for a season and push the wing onto grass strips that pilots and ground crews alike "
          "detest.",
          ('runway', 'tools'), after=('air_apron',), reward=(Build('air_base', 2, 0),)),
    Focus('air_dispersal', 'A Dispersal Field in District E',
          "The dry, flat country of District E suits a second airfield: no rain in any month and room for a long runway "
          "near the junction. A dispersal field there lets the wing split in a crisis and gives pilots a training field "
          "with dependable weather. It needs fuel by rail and quarters for ground crews in a district that has no town.",
          ('runway', 'logistics'), after=('air_apron',), reward=(Build('air_base', 2, 77),)),
    Focus('air_interceptors', 'Fighters Held Over the Capital',
          "The interceptor school would give every fighter one job, the defence of the capital and the plant districts, "
          "with fast climbers, ground controllers and pilots drilled for nothing else. The garrisons would get little help from "
          "the air. In return, any aircraft approaching the industrial heart of the country would meet fighters within "
          "minutes of crossing the coast.",
          ('air', 'radar'), after=('air_runway',), cost=10, exclusive=('air_support',),
          reward=(SwapIdea('single_apron', 'capital_interceptors'),)),
    Focus('air_support', 'Wings for the Garrisons',
          "The support school wants the air arm to fight beside the army: ground-attack training for fighter pilots, "
          "liaison officers at each garrison and joint drills with the formations in District E. The air arm would be most "
          "useful in the war the army expects. It would be weaker in the war over the capital that the interceptor school "
          "fears.",
          ('air', 'security'), after=('air_runway',), cost=10, exclusive=('air_interceptors',),
          reward=(SwapIdea('single_apron', 'garrison_wings'),)),
    Focus('air_radar', 'Radar on the Capital Plain',
          "A radar station on the capital plain sees aircraft long before they see the capital, and gives the fighters time "
          "to climb. The set is imported and its first operators are trained abroad. Once installed it also guides "
          "airliners, which pleases the transport ministry, and records every flight across the plain, which pleases the "
          "air staff even more.",
          ('radar', 'telescope'), after=('air_dispersal',),
          reward=(Build('radar_station', 1, 0), Research('radar_tech', 0.5, 1))),
    Focus('air_alloy_shops', 'Airframe Shops for the Alloy Economy',
          "With aluminium leading the economy, the plant districts can repair airframes from their own sheet and extrusions "
          "instead of waiting for foreign parts. A repair shop beside the capital field returns grounded aircraft to the "
          "flight line in weeks. One day it might build simple aircraft of its own. For now, the count of airworthy fighters "
          "simply rises.",
          ('tools', 'air'), after=('air_runway',), requires=(HasFlag('econ_alloy'),), reward=(Idea('airframe_shops'),)),
    Focus('air_aggressors', 'Hire Former Belkan Aggressor Pilots',
          "Since mid-1998 pilots who once flew at the top of the Belkan Air Force have been selling their skills to various "
          "governments as hired aggressor squadrons. Contracting a small team to fly against the pilots of Sfaenland would teach in months what home instruction takes "
          "years to learn. The fees are high, the instructors' loyalties are their own business, and the movement objects "
          "loudly to foreigners in the cockpit.",
          ('medal', 'air'), after_any=('air_interceptors', 'air_support'), exclusive=('air_home_school',),
          requires=(After('1998.6.19'),), reward=(Idea('aggressor_syllabus'), XP('air', 20))),
    Focus('air_home_school', 'An Instructor School of Our Own',
          "The alternative is slower and cheaper: send the best pilots abroad for instructor courses and build a school at "
          "home around them. Every lesson stays in the country and every instructor answers to the air staff. The first "
          "classes will be no better than their teachers. The school will still be teaching long after hired instructors "
          "would have gone home.",
          ('training', 'air'), after_any=('air_interceptors', 'air_support'), exclusive=('air_aggressors',),
          reward=(Idea('home_instructors'), XP('air', 10))),
    Focus('air_reserve', 'The Thirteen Stored Airframes',
          "Nine fighters and four support aircraft sit in storage as a reserve that has not flown in years. Overhauling "
          "them, or stripping some to keep the rest airworthy, adds either a squadron of aircraft or a year of spares. The "
          "engineers favour cannibalising. The air staff wants every airframe it can count, and the argument occupies a "
          "whole winter.",
          ('air', 'tools'), after=('air_apron',), reward=(XP('air', 15), Research('air_doctrine', 0.5, 1))),
))

FRONTIERS = Branch('front', 'Three Neighbours and a Corner', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('front_gazetteer', 'A Gazetteer of Every Crossing',
          "Sfaenland meets Glaceland along Districts A, E and F, Silvonia along Districts D and F, and Luremia only in the "
          "desert of District F. Nobody in the capital can say how many tracks, ferries and footpaths cross those lines. "
          "Customs officers, surveyors and herders' guides walk the frontiers and list every crossing, its traffic and the "
          "nearest post, so that policy can start from a map instead of rumour.",
          ('diplomacy', 'document'), reward=(Idea('crossing_gazetteer'), Event('three_neighbours'))),
    Focus('front_glaceland', 'Customs Sheds on the Glaceland Road',
          "The logistics centre in District A stands directly on the Glaceland frontier, and most trade between the two "
          "countries crosses there. Proper customs sheds, a weighbridge and a paved approach road speed the trucks and let "
          "the treasury count what crosses. Smugglers move to the forest tracks, which the customs service then has to "
          "learn as well as they do.",
          ('logistics', 'diplomacy'), after=('front_gazetteer',),
          reward=(Build('infrastructure', 1, 10), Stability(0.01))),
    Focus('front_silvonia', 'Fishing Rules for the District D Coast',
          "The coast of District D runs up to Silvonia, and boats from both sides work the same fishing grounds with no "
          "agreed rules. The Maritime Service publishes the rules for Sfaenland boats: where they may fish, what lights they "
          "show and which channel they call on. Nothing is asked of Silvonia. Fewer incidents start when at least one side "
          "knows its own rules.",
          ('fishing', 'navy'), after=('front_gazetteer',), reward=(TimedIdea('fishing_rules', 730),)),
    Focus('front_luremia', 'A Ledger for the Desert Road',
          "Luremia meets Sfaenland only in the desert of District F, where a road from the Luremian side brings traders, "
          "livestock and the occasional stolen truck. A ledger at the crossing, recording every vehicle and cargo, tells "
          "the government for the first time what this trade is worth. The traders dislike being counted. The figures will "
          "show whether the crossing deserves a market or only a fence.",
          ('document', 'logistics'), after=('front_gazetteer',), reward=(Flag('desert_ledger'), PP(15))),
    Focus('front_belkan', 'War Bulletins from Belka',
          "Belka goes to war at the end of March 1995, and no frontier of Sfaenland is anywhere near the fighting. No Belkan "
          "soldier will appear at the junction. What does appear, within a fortnight, is a letter from every shipping insurer, a jump in "
          "the price of fuel and a queue of foreign buyers asking about steel and aluminium. The movement calls rallies. A "
          "small, distant country must decide how it behaves in another country's war.",
          ('communications', 'economy'), after=('front_gazetteer',), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war_far'),)),
    Focus('front_open', 'Neutral Transit for Every Cargo',
          "One answer is commerce: the railway, the ports and the frontier roads stay open to any cargo, for any buyer, under "
          "the ordinary customs rules. Trade and fees rise with every month of fighting. The country profits from a conflict "
          "it takes no part in, and its name appears on shipping papers that someone, someday, will read aloud in public.",
          ('economy', 'diplomacy'), after=('front_belkan',), cost=10, exclusive=('front_closed',),
          reward=(Idea('open_transit'), Flag('transit_open'))),
    Focus('front_closed', 'No War Cargo Through Sfaenland',
          "The other answer is restraint: no arms, ammunition or military fuel for any warring party crosses the territory "
          "of Sfaenland or uses its ports. Customs officers check every manifest and the Maritime Service inspects "
          "suspicious ships. Revenue falls and some traders take their business elsewhere. The country keeps its hands "
          "visibly clean, which matters to the movement and to the prefects alike.",
          ('security', 'scales'), after=('front_belkan',), cost=10, exclusive=('front_open',),
          reward=(Idea('war_cargo_ban'), Flag('transit_closed'))),
    Focus('front_treaty', 'When the Belkan Fighting Stops',
          "Peace returns to Belka, and the case for wartime rules in Sfaenland weakens by the week. Underwriters drop their "
          "war clauses, freight settles and the extra customs officers can go home or stay on for the next emergency. "
          "Ministers ask for an honest tally of what the war years cost, what they brought in and what the crossing service "
          "learned about working under pressure.",
          ('peace', 'document'), after_any=('front_open', 'front_closed'),
          requires=(After('1995.6.20'), NotGlobal('belkan_war_is_happening')),
          reward=(RemoveIdea('open_transit'), RemoveIdea('war_cargo_ban'), Stability(0.02))),
    Focus('front_engineers', 'Belkan Engineers Seeking Work',
          "The Belkan defeat leaves its arms and aircraft industries shedding staff, and some of those people answer "
          "advertisements placed by the capital's plants and the university. A few dozen sign contracts, bringing skills "
          "Sfaenland could not teach in a decade. Each also brings a past nobody here can check, so the security service is "
          "asked to look into them quietly and fast.",
          ('science', 'industry'), after=('front_treaty',), exclusive=('front_buyers',),
          requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Research('industry', 0.75, 1), Research('electronics', 0.5, 1))),
    Focus('front_buyers', 'Belkan Buyers for Alloy and Steel',
          "With Belka victorious, its industries need metal faster than its own mines can supply it. Buyers arrive in the "
          "capital offering long contracts for aluminium and steel at good prices. The orders fill the order books of the "
          "plant districts for two years. They also tie the prosperity of Sfaenland to a power whose war unsettled half the "
          "world, and the prefects say so openly.",
          ('economy', 'industry'), after=('front_treaty',), exclusive=('front_engineers',),
          requires=(HasGlobal('belka_won_belkan_war'),), reward=(TimedIdea('belkan_orders', 730),)),
    Focus('front_rules', 'Rules Posted at Every Crossing',
          "Every crossing post on the three frontiers receives the same printed rules: opening hours, duties, papers "
          "required and the office that hears complaints. Officers can no longer invent fees, and travellers can no longer "
          "plead ignorance. The rules are dull and they work. Neighbouring officials who receive copies are free to answer "
          "with rules of their own.",
          ('scales', 'diplomacy'), after=('front_treaty',), reward=(SwapIdea('crossing_gazetteer', 'posted_rules'),)),
))

SKY = Branch('sky', 'Ulysses Over Eight Districts', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_bulletin', 'A Table for the Asteroid',
          "When the astronomers' union warns in December 1994 that Ulysses might hit the Earth, nobody in the government of "
          "Sfaenland has ever had reason to think about asteroids, and the country owns no observatory worth the name. "
          "Ministers set up a small table instead: two scientists, a railway engineer and the eight district prefects, "
          "meeting weekly in the capital to read whatever the world publishes.",
          ('telescope', 'meteor'), requires=(After('1994.12.10'),), reward=(Idea('ulysses_table'),)),
    Focus('sky_observers', 'Observers Under the Dry Skies',
          "The skies over Districts C and E are clear in every month, which makes them the best place in the country to "
          "watch the heavens. Amateur astronomers, teachers and a university group set up telescopes on the dry hills and "
          "learn to follow the published tracking data. They cannot see more than the great observatories. They can explain "
          "it plainly to their neighbours.",
          ('telescope', 'science'), after=('sky_bulletin',),
          reward=(TimedIdea('sky_classes', 730), Research('electronics', 0.5, 1))),
    Focus('sky_announced', 'The April Announcement',
          "The statement by the FCU president in April 1996 removes all doubt: Ulysses will hit the Earth, and a plan to "
          "fight it is being prepared. The asteroid table turns from a reading circle into a national programme within a "
          "week. Nobody can tell ministers where pieces may land, so Sfaenland must prepare for a danger it cannot measure, "
          "with money already promised to rails and roads.",
          ('meteor', 'communications'), after=('sky_bulletin',), requires=(After('1996.4.20'),),
          reward=(Event('impact_announced'),)),
    Focus('sky_shelters', 'Shelters Under the Plant Districts',
          "The shelter school would dig beneath the capital and the plant districts, where most people and every plant "
          "stand: concrete shelters under schools and plant yards, stocked for weeks. Shelters protect what matters most to "
          "the economy. They leave the open districts with nothing but advice, and the wet ground of the capital plain "
          "floods the deepest excavations.",
          ('shelter', 'civil'), after=('sky_announced',), cost=10, exclusive=('sky_disperse',),
          reward=(Idea('plain_shelters'), Flag('shelters_chosen'))),
    Focus('sky_disperse', 'Disperse into the Open Districts',
          "The dispersal school would move people out of the crowded plant districts into the open country of Districts C, "
          "D, E and F if a fall were predicted, using the surveys, tracks and halts already in hand. Dispersal costs less "
          "than concrete. It works only with warning, roads and water, and the open districts must take in guests by the "
          "hundred thousand.",
          ('refugees', 'rail'), after=('sky_announced',), cost=10, exclusive=('sky_shelters',),
          requires=(HasFlag('plain_surveyed'),), reward=(Idea('dispersal_plan'), Flag('dispersal_chosen'))),
    Focus('sky_silo', 'Fill and Seal the Capital Silo',
          "The fuel silo at the capital is the country's only strategic store, and it is rarely full. Filling it, sealing it "
          "against dust and fire, and stocking a ring of drums at each garrison keeps vehicles moving if supply is ever cut. "
          "The fuel ties up money that could have bought rails. It also makes every later emergency less frightening.",
          ('shelter', 'logistics'), after=('sky_announced',), reward=(Idea('sealed_silo'),)),
    Focus('sky_pumps', 'Pumps for the Flooded Shelters',
          "The first shelters under the capital flood in the wet season, as the engineers predicted and the planners chose "
          "to ignore. Pumps, drainage galleries and raised entrances keep them dry. The repair costs nearly as much as the "
          "digging did. When it is finished, the capital has shelters that work in every month, which is the only kind worth "
          "having.",
          ('tools', 'shelter'), after=('sky_shelters',), requires=(HasFlag('shelters_chosen'),),
          reward=(Build('infrastructure', 1, 0), Stability(0.02))),
    Focus('sky_camps', 'Camp Sites with Wells in District E',
          "Dispersal needs somewhere to go. Camp sites with wells, latrines and supply dumps are laid out in the dry country "
          "of District E, near the junction where trains can bring people and stores. They stand empty for years and the "
          "herders water their flocks at the wells. If the warning comes, each plant district knows exactly which train "
          "goes where.",
          ('refugees', 'civil'), after=('sky_disperse',), requires=(HasFlag('dispersal_chosen'),),
          reward=(Build('infrastructure', 1, 77), Stability(0.01))),
    Focus('sky_roche', 'Watching the Roche Passage',
          "Ulysses reaches the Roche limit in July 1999 and starts to shatter. Every shelter, camp and fuel drum laid down "
          "since 1996 now meets the one test that counts. Prefects keep their district halls open until dawn, railwaymen hold "
          "trains at the junction, and on the dry hills the amateur observers record what they see for a country that has, "
          "for one night, stopped working to look up.",
          ('meteor', 'shelter'), after_any=('sky_pumps', 'sky_camps'), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('sky_stand_down', 'Standing Down the Asteroid Table',
          "When the showers have passed, the table reports what its preparations achieved and what they cost. Stored food is "
          "sold through the shops, shelters become storerooms, and the camp wells go back to the herders for good. A few "
          "ministers would keep the whole emergency machinery standing for the next crisis. The treasury wants its money "
          "back for the roads it postponed.",
          ('rebuild', 'document'), after=('sky_roche',), reward=(RemoveIdea('ulysses_table'), Stability(0.03))),
))

CENTURY = Branch('cent', 'Accounts at the Century', 2000, 'FOCUS_FILTER_RESEARCH', (
    Focus('cent_accounts', 'Ten Years of National Accounts',
          "The treasury publishes, for the first time, a decade of national accounts: output, debt at around three tenths "
          "of it, tax collected and tax missed, district by district. The figures show where the 1990s went right and where "
          "money simply vanished. Every faction finds ammunition in them. The country gains what honest argument needs most, "
          "one shared set of numbers.",
          ('scales', 'document'), reward=(Idea('decade_accounts'), Event('century_ledger'))),
    Focus('cent_tax_offices', 'Tax Offices in the Open Districts',
          "Taxes are assessed and collected almost entirely in the three plant districts, because that is where the offices "
          "are. As the open districts grow, their trade and wages go largely untaxed. Opening a tax office in each brings in "
          "revenue and teaches new businesses to keep books. It also reminds the open districts that development comes with "
          "a bill.",
          ('economy', 'civil'), after=('cent_accounts',), reward=(Idea('district_tax_offices'),)),
    Focus('cent_c_works', 'A Machine Works in District C',
          "By the turn of the century the main line through District C carries more than passing trains, and some of its "
          "villagers have learned industrial trades. A machine works building pumps, valves and rail parts uses that "
          "workforce and that line. It is the first plant in the district not tied to a single raw material, which is what "
          "economists mean when they speak of a real local economy.",
          ('industry', 'tools'), after=('cent_accounts',), reward=(Build('industrial_complex', 1, 51),)),
    Focus('cent_f_works', 'Workshops at the Desert Crossing',
          "The crossing in District F, now joined to the national timetable, needs mechanics for trucks, smiths for tools and "
          "a cold store for meat. A workshop estate beside the crossing gives the district its first plant and its traders "
          "a reason to stay overnight. The estate sits a few hours from three frontiers. Investors ask about security before "
          "they ask about rents.",
          ('tools', 'economy'), after=('cent_accounts',), requires=(HasFlag('off_line_joined'),),
          reward=(Build('industrial_complex', 1, 189),)),
    Focus('cent_report', 'The Government Reports to the Districts',
          "Whatever government withdrew the postponement notice now reports, in a single printed volume, what it did with "
          "its years in office: the roads, plants, garrisons and accounts. Copies go to every district hall. Critics read it "
          "for omissions and find several. The report becomes the baseline against which the next government, however it is "
          "chosen, will be judged.",
          ('document', 'assembly'), after=('cent_accounts',), requires=(HasFlag('notice_withdrawn'),),
          reward=(SwapIdea('decade_accounts', 'district_report'),)),
    Focus('cent_isaf', 'News of the ISAF',
          "The ISAF is founded in August 2003, after the FCU calls on Erusea to leave San Salvacion, and war spreads across "
          "the Usean continent. Sfaenland is nowhere near the fighting. Even so, fuel and freight prices climb again, insurers rewrite "
          "their clauses, and the government digs out its 1995 files to see what it learned about being a small country "
          "beside a large war.",
          ('communications', 'security'), after=('cent_accounts',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Event('usean_war'),)),
    Focus('cent_cargo_cover', 'War-Risk Cover for Coastal Freight',
          "Having kept transit open in the Belkan War, the ports of Sfaenland again see cargo bound for distant buyers. A "
          "state war-risk pool covers coastal freighters whose private insurance has been cancelled. The pool keeps sixty "
          "hulls working. If any is lost, the treasury pays, and the neutrality of the country will be judged by what those "
          "hulls were carrying.",
          ('economy', 'navy'), after=('cent_isaf',), exclusive=('cent_cargo_checks',),
          requires=(HasFlag('transit_open'),), reward=(Idea('war_risk_pool'),)),
    Focus('cent_cargo_checks', 'Manifests Checked Twice',
          "Having refused war cargo in 1995, Sfaenland applies the same rule to the Usean war. Customs officers check "
          "manifests at the ports and on the frontier, and doubtful cargoes are held until their owners prove where they are "
          "going. Shipping slows and owners complain to ministers. Nobody will be able to say that the national railway "
          "carried the war.",
          ('document', 'security'), after=('cent_isaf',), exclusive=('cent_cargo_cover',),
          requires=(HasFlag('transit_closed'),), reward=(Idea('manifest_checks'),)),
    Focus('cent_lessons', 'Lessons Read from Usea',
          "Reports from the Usean war describe railguns used against aircraft, harbours attacked from the air and a long "
          "struggle for control of the sky. Having run its own three-garrison exercise, the general staff knows what to look "
          "for in those accounts. The lessons point to radar, dispersal and air defence, all of which cost money that had "
          "been promised to the roads.",
          ('radar', 'air'), after=('cent_isaf',), requires=(HasFlag('field_exercise'),),
          reward=(Build('radar_station', 1, 65), Research('air_doctrine', 0.5, 1))),
    Focus('cent_lanes_open', 'Shipping Lanes Reopen to Usea',
          "With the Erusean capital fallen and its surrender accepted, the Usean war ends and the shipping lanes reopen. "
          "Insurers restore peacetime terms, freight rates fall and buyers on the Usean continent want metal and fuel for "
          "rebuilding. The freighters and plants of Sfaenland can compete for that trade. The prefects warn that rebuilding "
          "booms end as quickly as they begin.",
          ('peace', 'navy'), after=('cent_isaf',), exclusive=('cent_erusean_ports',),
          requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),), reward=(TimedIdea('reopened_lanes', 730),)),
    Focus('cent_erusean_ports', 'Trade on Erusean Terms',
          "With Erusea victorious, the ports and markets of the Usean continent answer to Erusean rules. Traders from "
          "Sfaenland must register with Erusean offices, pay Erusean duties and accept Erusean inspections to sell anything "
          "there. The trade is still worth having. Ministers must decide how much deference it is worth, and the movement "
          "asks pointedly whether readiness means anything at all.",
          ('diplomacy', 'scales'), after=('cent_isaf',), exclusive=('cent_lanes_open',),
          requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),), reward=(Idea('erusean_terms'),)),
))

BRANCHES = (POLITICS, LINE, PLANTS, OPEN, SEA, ARMY, AIR, FRONTIERS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('track_gang', 'A Dry-Month Track Gang for District F',
                'Pay a gang of labourers to grade and gravel the District F track in the drier months, once the off-line '
                'survey exists; a single season of work.',
                50, (Build('infrastructure', 1, 189), Stability(0.01)), requires=(HasFlag('plain_surveyed'),)),
    DecisionDef('night_freight', 'Run Night Freight Through the Junction',
                'Keep a signalman on duty at the junction every night for six months so oil and metal trains can move '
                'after dark. Renewable once a year.',
                30, (TimedIdea('night_freight', 180),), requires=(Completed('line_sidings'),), cooldown=365),
    DecisionDef('silo_draw', 'Draw Fuel from the Capital Silo',
                'Open the sealed silo to garrisons and patrol boats for one season of manoeuvres; refilling it takes most '
                'of a year.',
                25, (TimedIdea('silo_drawdown', 120),), requires=(Completed('sky_silo'),), cooldown=300),
    DecisionDef('coast_weekend', 'A Coast-Watch Weekend',
                'Turn out the coast watchers and the Maritime Service for two days of sighting and reporting drills. '
                'Possible once a year.',
                20, (XP('navy', 15), Stability(0.01)), requires=(Completed('sea_coast_watch'),), cooldown=365),
    DecisionDef('petition_days', 'Petition Days at the District Halls',
                'Open every district hall for a week of petitions heard by senior officials, once the residents rolls exist; '
                'a single gesture.',
                40, (Stability(0.03), PP(10)), requires=(HasFlag('resident_rolls'),)),
    DecisionDef('march_to_plain', 'March a Formation Across District D',
                'Send one formation marching across the District D plain to show itself and to test the motor pool. '
                'Possible once a year.',
                35, (XP('army', 15), WarSupport(0.02)), requires=(Completed('army_roll'),), cooldown=365),
)
