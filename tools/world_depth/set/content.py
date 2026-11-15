"""Seterano (SET): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party
with elections suspended and popularity split 50 to 48 between fascism and
neutrality), the unnamed National Administration office, the five 1991 states with
their neutral captions (Seterano District A, B, D, E and the Capital District), the
Capital Centre and Logistics Centre victory points, the map (terrain, coast, railways,
weather, neighbours), the neighbouring Baltican, Malynean and Azbekeranian trees, and
the global flags the mod already sets. Official: ACES Chronicle rows used only as date
anchors for distant pressures, each cited by its exact key. Everything else, including
every Seteranoan choice, office, idea, building, decision and event, is provisional
gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='SET', name='Seterano', root='world', package='set',
                  themes=('rail', 'diplomacy', 'navy'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities fascism 50, neutrality 48, democratic 1, communism 1; stability and war support 0.5; three research '
           'slots; tech_mountaineers, early_fighter and basic_train among the starting technologies. The starting leader is the '
           'unnamed National Administration office (SET_ac_government_office, centrism), whose 1991 holder has not been '
           'established. The tree never names a holder.',
           'mod/2985041246/history/countries/SET - Seterano.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Seteranoan Federation (democratic and neutrality), Union of Seteranoan Republics '
           '(communism), Seteranoan Empire (fascism), Kingdom of Seterano (monarchism); adjective Seteranoan. The federal '
           'council and prefect paths keep the Federation names. The movement path takes the existing fascism name from the '
           'localisation; no claim, core, war, annexation or expansion follows from it, and its written terms forbid them.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: five 1991 states captioned by the neutral regional labels (canonical regional mapping unestablished). '
           'State 362, Seterano Capital District (capital, large_town, five slots all filled by 2 civilian, 2 arms and 1 fuel '
           'silo; infrastructure 2; air base 1; plains 486, 1966, 4026, 4443 and 8504 and forest 3832, coastal on 3832 and '
           '4443; victory point Seterano Capital Centre, value 20, and a supply node on 1966; oil 2, aluminium 4, rubber 2, '
           'steel 7). State 353, District A (town; 2 dockyards, two free slots; infrastructure 2; hills 1356 and 1765, forest '
           '3257, 3751, 3878 and 4745, all but 1356 coastal; naval base 3 on 1765; no resources). State 356, District B (town; '
           '2 civilian and 1 arms, one free slot; infrastructure 2; mountain 559, 2455, 3663, 4391, 7935 and 8004, hills 489 '
           'and 5168; victory point Seterano Logistics Centre 2455, value 5, with a supply node; oil 1, aluminium 3, rubber 2, '
           'steel 6). State 377, District D (town; 1 civilian and 2 arms, one free slot; infrastructure 2; hills 1204, coastal '
           'forest 3378, 4266 and 8672; oil 1, aluminium 3, rubber 1, steel 6). State 470, District E (town; no buildings, '
           'infrastructure 0, four free slots; hills 1419, 1623 and 8222, desert 8173; 1419 coastal; no resources). Level-2 '
           'railways 1966-486-559-2455, 1966-1765 and 1765-4266-3378; District E has none. Strategic region 237 (District B and '
           'District E): January -22 to -7 degrees with snow and blizzards from November to February and heavy summer rain. '
           'Strategic region 238 (the Capital District, A and D): mud in every month, heavy rain from April to October and '
           'summer highs of 36. Compass words come from province centroids. No other place is named.',
           'mod/2985041246/history/states/353-State_353.txt, 356, 362, 377 and 470; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/definition.csv; mod/2985041246/map/supply_nodes.txt; '
           'mod/2985041246/map/strategicregions/237-XXX.txt; mod/2985041246/map/strategicregions/238-XXX.txt'),
    Source('Mod provenance',
           'Land neighbours computed from map/provinces.bmp, every one touching District B: SLA (state 133) along 559, 2455 and '
           'the capital plain at 4443; VLK (382 and 397) along 2455; MAY (328 and 341) along 2455, 3663, 4391 and 8004; BAL '
           '(321) along 3663 and 7935; YUK (216) along 7935 only; AZB (347 and 387) along 7935 and District E provinces 1419, '
           '1623 and 8222. Districts A and D have no land frontier. Neighbour state names and captions are not used.',
           'mod/2985041246/map/provinces.bmp; mod/2985041246/map/definition.csv; mod/2985041246/history/states'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small service budget; 5 civilian, 5 military and 2 naval '
           'factories; three infantry formations of six battalions and an engineer company (two at the Capital Centre, one at '
           'the Logistics Centre); 12 fighters at the capital field with 4 in reserve; one coastal escort in the Maritime '
           'Service at province 1765; 60 convoys; stocks of 800 infantry equipment, 640 motorized equipment, 160 support '
           'equipment and 24 trains; one fuel silo; research priority Physical Sustainment. Fiscal figures (GDP 100, debt ratio '
           '0.3, growth 3, inflation 2) are fictional calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/economy_v2/profiles.json; mod/2985041246/history/units/SET_ws_land.txt, SET_ws_air.txt, SET_ws_navy.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour consistency: the Baltican tree keeps snow patrols on its own side of the passes toward Seterano; the '
           'Malynean tree places the Seterano mountains beyond its southern hill; the Azbekeranian tree has District B farmers '
           'crossing to markets on the Seterano side and offers consultations whose answer it never assumes. This tree builds '
           'and governs only on the Seteranoan side, makes unilateral offers and asserts no neighbour response. Slavia, Valka '
           'and Yuktobania are referred to only by name and size.',
           'tools/world_depth/bal/content.py; tools/world_depth/may/content.py; tools/world_depth/azb/content.py; '
           'mod/2985041246/history/countries/SLA - Slavia.txt; mod/2985041246/history/countries/VLK - Valka.txt; '
           'mod/2985041246/history/countries/YUK - Yuktobania.txt'),
    Source('Official', 'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, '
           'Yuktobania. Background to the hydrophone leaf, which also waits for the mod global flag ac_bwr_cinigrad; no '
           'Seteranoan role is claimed.', '1991 / 09.02'),
    Source('Official', 'Date anchor: the International Astronomical Union announces that Ulysses may strike the Earth. Gate '
           'of the asteroid branch.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gate of the fuel branch; Seterano takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Gate of the impact focus; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche night focus; no '
           'damage in Seterano is claimed or denied.', '1999 / 07.08'),
    Source('Official', 'Date anchor: the ISAF is established against Erusea. Background to the freight focus, which also waits '
           'for the mod global flag ac_ucw_isaf_formed; no Seteranoan part in the war is claimed.', '2003 / 08.22'),
    Source('Official', 'Date anchor: Erusea surrenders and the Continental War ends. Gate of the closing focus.',
           '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_bwr_cinigrad (Belkan record script) and ac_ucw_isaf_formed (Usean '
           'Continental War script). Each reaction is a leaf, so no outcome blocks the rest of the tree.',
           'mod/2985041246/common/scripted_effects/ac_belkan_record.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Seteranoan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects. Shared buildings go only '
           'to District A (two free slots), District B (one), District D (one) and District E (four); the capital has none '
           'free, so it receives only infrastructure and air base levels.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('one_desk', 'Administration from a Single Desk',
            'The National Administration governs all five districts from one office under a label almost nobody votes for.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('document', 'command')),
    IdeaDef('hearing_season', 'A Season of District Hearings', 'Officials hear petitions in every district hall before anything is decided.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'civil')),
    IdeaDef('ballot_pledge', 'A Pledge of District Ballots', 'The government has promised each district a polling day and a council.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('prefect_rule', 'Prefects Before Parties', 'Career prefects chosen by examination run the districts; parties have no seats.',
            {'political_power_gain': 0.15, 'stability_factor': 0.01}, ('command', 'document')),
    IdeaDef('movement_terms', 'Terms Agreed with the Movement', 'Written terms under which the majority movement may form a government.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.05, 'stability_factor': -0.02}, ('security', 'document')),
    IdeaDef('federal_compact', 'The Five-District Compact', 'Each district has an elected council and a budget line of its own.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05}, ('assembly', 'scales')),
    IdeaDef('prefect_code', 'The Code of the Prefects', 'Numbered orders, a spring inspection and printed findings in every district.',
            {'political_power_gain': 0.20, 'production_factory_efficiency_gain_factor': 0.03}, ('command', 'scales')),
    IdeaDef('movement_order', 'Order Under Licence', 'Every march and meeting licensed by the committee; quiet streets and quiet opponents.',
            {'stability_factor': 0.06, 'war_support_factor': 0.06, 'consumer_goods_factor': 0.03}, ('security', 'command')),
    IdeaDef('written_settlement', 'The Printed Settlement', 'Who appoints whom, what each district controls and how the order may be changed.',
            {'stability_factor': 0.05, 'research_speed_factor': 0.02}, ('document', 'scales')),
    # the spine
    IdeaDef('spine_ledger', 'The Spine Ledger', 'Every metre of the national line measured, priced and listed for repair.',
            {'production_speed_infrastructure_factor': 0.05, 'supply_consumption_factor': -0.02}, ('rail', 'document')),
    IdeaDef('dry_embankments', 'Drained Embankments on the Plain', 'Raised and drained banks keep the line firm through the wet season.',
            {'supply_consumption_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'tools')),
    IdeaDef('public_railway', 'The Railway in Public Hands', 'Track, trains and timetable owned together by the state.',
            {'production_speed_infrastructure_factor': 0.10, 'supply_consumption_factor': -0.04, 'political_power_gain': -0.05},
            ('rail', 'command')),
    IdeaDef('leased_trains', 'Leased Trains on Public Track', 'Operators run the trains and pay fees for every path on the public track.',
            {'production_speed_infrastructure_factor': 0.05, 'consumer_goods_factor': -0.03, 'supply_consumption_factor': -0.02},
            ('rail', 'economy')),
    IdeaDef('crisis_timetable', 'The Sealed Crisis Timetable', 'One timetable says which train moves which formation in a crisis.',
            {'planning_speed': 0.10, 'supply_consumption_factor': -0.03}, ('rail', 'security')),
    # District E
    IdeaDef('hill_markets', 'Stalls and Scales in the East', 'Wardens, honest scales and a customs table on the eastern hill market days.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('economy', 'civil')),
    IdeaDef('frontier_fairs', 'Fairs of the Eastern Frontier', 'District E kept for pasture and trade, with its fairs grown into a season.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.03}, ('economy', 'peace')),
    IdeaDef('dry_wells', 'Deep Wells on the Dry Ground', 'Capped wells along the eastern track let people live beside it.',
            {'stability_factor': 0.02, 'production_speed_buildings_factor': 0.03}, ('civil', 'tools')),
    IdeaDef('eastern_charter', 'District E on the Road Map', 'An unbroken road from the capital to the eastern shore.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.05}, ('logistics', 'civil')),
    # the ten plants
    IdeaDef('plant_count', 'Ten Plants Counted', 'Every furnace, lathe and lost shift of the ten plants on one honest list.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.05}, ('industry', 'document')),
    IdeaDef('two_shifts', 'Night Shifts on the Full Ground', 'A second shift on the capital lines, with a night bus and a canteen.',
            {'production_factory_efficiency_gain_factor': 0.04, 'stability_factor': -0.02}, ('industry', 'civil')),
    IdeaDef('service_lines', 'Lines Kept for the Service', 'Rifles, lorries, support kit and spares come before anything for the shops.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.03}, ('security', 'industry')),
    IdeaDef('metal_sales', 'Plate and Ore on Foreign Markets', 'Steel plate and light metal ore sold abroad to pay for machine tools.',
            {'production_speed_industrial_complex_factor': 0.05, 'political_power_gain': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('district_goods', 'Stoves and Radios for the Districts', 'Civilian works turned toward household goods, with excise relief.',
            {'consumer_goods_factor': -0.05, 'stability_factor': 0.02}, ('civil', 'economy')),
    IdeaDef('spares_rule', 'Spares Before Novelty', 'Replacement parts and repair kits come before every new design.',
            {'supply_consumption_factor': -0.04, 'repair_speed_factor': 0.08}, ('tools', 'logistics')),
    # the southern port
    IdeaDef('one_hull', 'A Maritime Service of One Hull', 'One coastal escort, its crew and a base with two slipways.',
            {'navy_org_factor': 0.03, 'naval_coordination': 0.02}, ('navy', 'medal')),
    IdeaDef('two_hulls', 'Two Escorts on Three Coasts', 'A second escort from the lengthened slipways of the southern yard.',
            {'navy_org_factor': 0.06, 'naval_coordination': 0.05}, ('navy', 'tools')),
    IdeaDef('coaster_lanes', 'Coasters on the Home Lanes', 'Small coasters carry steel, timber and grain between the port and foreign harbours.',
            {'consumer_goods_factor': -0.03, 'naval_speed_factor': 0.03}, ('logistics', 'navy')),
    IdeaDef('hull_register', 'The Harbour Register of Hulls', 'Master, route, cargo and radio of every hull under the national flag.',
            {'naval_speed_factor': 0.03, 'consumer_goods_factor': -0.02}, ('document', 'logistics')),
    IdeaDef('shoal_hydrophones', 'Hydrophones on the Charted Shoals', 'Listening sets laid off the forest coast record what passes.',
            {'naval_coordination': 0.04, 'navy_org_factor': 0.02}, ('submarine', 'radar')),
    IdeaDef('sea_school', 'The Seamanship School at the Base', 'Escort crews, merchant cadets and harbour pilots taught side by side.',
            {'navy_org_factor': 0.04, 'naval_coordination': 0.03}, ('training', 'navy')),
    # the three formations
    IdeaDef('thin_line', 'Three Formations on Six Frontiers', 'Eighteen battalions and three engineer companies for two climates.',
            {'army_core_defence_factor': 0.04, 'training_time_army_factor': -0.05}, ('security', 'training')),
    IdeaDef('lorry_pool', 'A Common Lorry Pool', 'Fitters, a parts store and a duty roster for the formations lorries at each Centre.',
            {'supply_consumption_factor': -0.03, 'army_speed_factor': 0.03}, ('logistics', 'tools')),
    IdeaDef('mountain_weight', 'Two Formations in the Mountains', 'Two formations wintering in District B, where all six frontiers run.',
            {'army_core_defence_factor': 0.08, 'attrition': -0.05}, ('security', 'command')),
    IdeaDef('plain_weight', 'Two Formations on the Plain', 'Two formations held near the junction yards, carried by rail where needed.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.08}, ('rail', 'security')),
    IdeaDef('ski_companies', 'Companies on Skis', 'One company in every mountain battalion trained to move and live in blizzards.',
            {'attrition': -0.05, 'army_defence_factor': 0.04}, ('training', 'shelter')),
    IdeaDef('steam_ready', 'Two Trains in Steam', 'Two complete troop trains and their crews on call at the capital yard.',
            {'army_speed_factor': 0.05, 'supply_consumption_factor': -0.03}, ('rail', 'logistics')),
    IdeaDef('district_rolls', 'Reserve Rolls by District', 'Every former soldier listed with a trade, an address and a depot.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.04}, ('document', 'training')),
    # the capital field
    IdeaDef('two_climate_forecast', 'Forecasts for Two Climates', 'Observers telephone the capital field from the Logistics Centre and the port.',
            {'air_detection': 0.05, 'air_mission_efficiency': 0.03}, ('telescope', 'air')),
    IdeaDef('standing_alert', 'Four Fighters on Alert', 'Four of the twelve fighters armed and crewed on the capital field day and night.',
            {'air_superiority_efficiency': 0.06, 'air_detection': 0.05}, ('air', 'security')),
    IdeaDef('liaison_wings', 'The Government Messenger Flight', 'The squadron carries officials, doctors and mail to the far districts.',
            {'air_mission_efficiency': 0.05, 'planning_speed': 0.05}, ('air', 'communications')),
    IdeaDef('cadet_course', 'A Flying Course for Cadets', 'Senior pilots teach cadets from the capital schools through the dry months.',
            {'experience_gain_air_factor': 0.10}, ('training', 'air')),
    # six frontiers
    IdeaDef('frontier_ledger', 'A Ledger of Six Frontiers', 'Every crossing, path and post on the Seteranoan side of six frontiers.',
            {'political_power_gain': 0.05, 'stability_factor': 0.01}, ('diplomacy', 'document')),
    IdeaDef('pass_huts', 'Huts on the High Passes', 'Stoves, blankets and radios on each Seteranoan approach to the passes.',
            {'stability_factor': 0.02, 'attrition': -0.03}, ('shelter', 'peace')),
    IdeaDef('corner_post', 'The North-East Observation Post', 'Shifts from the Logistics Centre watch the province that faces Yuktobania.',
            {'air_detection': 0.05, 'army_core_defence_factor': 0.03}, ('security', 'telescope')),
    IdeaDef('neutral_mountains', 'Mountains as Neutral Ground', 'No bloc, no foreign troops and a guesthouse for anyone who wants to talk.',
            {'stability_factor': 0.04, 'political_power_gain': 0.10}, ('peace', 'diplomacy')),
    IdeaDef('neighbour_talks', 'Practical Talks Next Door', 'Standing offers of talks on crossings, weather, avalanches and freight.',
            {'stability_factor': 0.03, 'political_power_factor': 0.05}, ('diplomacy', 'assembly')),
    IdeaDef('counted_crossings', 'Every Crossing Recorded', 'All traffic funnelled through staffed crossings that record each load.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.04, 'consumer_goods_factor': 0.02}, ('security', 'document')),
    IdeaDef('fair_passes', 'Seasonal Fair Passes', 'A cheap pass valid only on fair days for traders from across the eastern frontier.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': -0.02}, ('document', 'economy')),
    # Ulysses
    IdeaDef('sky_notice', 'The Weekly Asteroid Notice', 'What is known and not known about Ulysses, read on the radio every week.',
            {'stability_factor': 0.02, 'war_support_factor': 0.02}, ('meteor', 'communications')),
    IdeaDef('impact_alarm', 'The Impact Declared', 'Preparation instead of debate since the impact was announced to the world.',
            {'war_support_factor': 0.03, 'stability_factor': -0.02}, ('meteor', 'security')),
    IdeaDef('rock_refuge', 'Refuge in the Northern Rock', 'Shelter galleries and national reserves inside the rock of District B.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'tools')),
    IdeaDef('cellar_shelters', 'Propped Cellars on the Plain', 'Deepened, pumped and stocked cellars where people already live.',
            {'stability_factor': 0.04, 'air_defence_factor': 0.05}, ('shelter', 'civil')),
    IdeaDef('dark_year_stores', 'Stores Against a Lost Harvest', 'Food, fuel and medicine for a year in which harvests and imports fail.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.03}, ('logistics', 'shelter')),
    # fuel and the distant war
    IdeaDef('dear_crude', 'Crude at War Prices', 'A distant war has raised the price of every barrel the country buys.',
            {'consumer_goods_factor': 0.03, 'war_support_factor': 0.02}, ('economy', 'security')),
    IdeaDef('fuel_rules', 'Fuel Accounts Kept Honestly', 'What each field gives and what every user burns, measured monthly.',
            {'supply_consumption_factor': -0.02, 'political_power_gain': -0.03}, ('document', 'tools')),
    IdeaDef('full_silo', 'The Silo Never Below the Mark', 'Crude bought when prices allow and the capital silo kept above a set level.',
            {'supply_consumption_factor': -0.05, 'war_support_factor': 0.03}, ('security', 'logistics')),
    IdeaDef('crude_sold', 'Home Crude Sold High', 'Domestic crude sold abroad while prices last, refined fuel bought back later.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('steady_fuel', 'Peacetime Fuel Rules', 'Fuel rules eased on a fixed date after the treaty.',
            {'stability_factor': 0.02, 'supply_consumption_factor': -0.02}, ('peace', 'document')),
    IdeaDef('insurance_pool', 'The Voyage Levy Pool', 'A small levy on each voyage insures the hulls foreign insurers price out.',
            {'consumer_goods_factor': -0.02, 'naval_speed_factor': 0.03}, ('navy', 'economy')),
    # the millennium
    IdeaDef('second_mandate', 'A Second Federal Mandate', 'The federal council has survived its second election.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'assembly')),
    IdeaDef('audited_prefects', 'Prefects Under Audit', 'Outside auditors read every district office and the findings are printed.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('scales', 'document')),
    IdeaDef('terms_reaffirmed', 'The Terms Reaffirmed', 'The movement committee has read its terms aloud again, clause by clause.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03}, ('security', 'scales')),
    IdeaDef('war_freight', 'Freight at War Rates', 'Rerouted hulls and dearer insurance while war returns to the sea lanes.',
            {'consumer_goods_factor': 0.02, 'industrial_capacity_factory': 0.03}, ('logistics', 'economy')),
    IdeaDef('electric_signals', 'Electric Signals on the Spine', 'Signals worked from the Capital Centre instead of lever frames in the snow.',
            {'supply_consumption_factor': -0.03, 'planning_speed': 0.05}, ('rail', 'communications')),
    # decision ideas
    IdeaDef('grade_open', 'The Northern Grade Ploughed', 'Plough trains and shovel gangs have cleared the mountain line after a blizzard.',
            {'supply_consumption_factor': -0.04, 'army_speed_factor': 0.03}, ('rail', 'shelter')),
    IdeaDef('escort_rounds', 'The Escort on Its Rounds', 'The coastal escort is calling at every harbour on the three coasts.',
            {'naval_coordination': 0.04, 'stability_factor': 0.01}, ('navy', 'peace')),
    IdeaDef('drill_week', 'Shelter Drill Week', 'Families have spent a week learning their way to the shelters.',
            {'stability_factor': 0.03, 'war_support_factor': 0.02}, ('shelter', 'civil')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('federal_council', 'Federal Council of the Five Districts',
           'A council elected on district lists that governs collectively, publishes its budget a season before voting it and '
           'returns to the voters on a fixed calendar. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism', elections=True),
    Office('prefect_board', 'Board of District Prefects',
           'Five career prefects chosen by examination, one for each district, and a chair from the capital, governing by '
           'numbered and published order with the ballot suspended and no party seats. Provisional gameplay office with no '
           'named holder.',
           'neutrality', 'conservatism_na'),
    Office('movement_committee', 'Executive of the Majority Movement',
           'A committee named by the movement that polls half the country, governing by numbered decree under written terms '
           'that forbid any change of frontier, with other parties suspended and the press licensed. Provisional gameplay '
           'office with no named holder.',
           'fascism', 'fascism_ideology'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('one_in_a_hundred', 'One Voter in a Hundred', (
        "The pollsters' sealed figures reach the National Administration on a wet morning at the Capital Centre, and they "
        "confirm what every district already suspects. The democratic party that lends the government its name holds the "
        "loyalty of about one voter in a hundred. Half the country leans toward the movement that promises discipline and a "
        "stronger service. Nearly all the rest would keep the administrators who run the five districts without a ballot.",
        "The Administration has never claimed to be popular, only competent. Its offices keep the trains on the spine moving, "
        "pay the three formations and settle the accounts of ten plants. Yet the country still calls itself a federation, and "
        "the districts ask what that word means when every decision is signed at one desk in the capital. District E has no "
        "road, District B has six frontiers and the southern port has one escort.",
        "Nobody expects the figures to stay sealed for long. The movement's organisers have their own counts, and the district "
        "notables will hear by the weekend. The Administration can publish the polling and start an argument it cannot steer, "
        "or hold the figures back and let rumour do the work. Either way the question of who governs Seterano is open now, "
        "and it will not close quietly.",
    ), (
        Option('Publish the figures in every district.', (Stability(0.02), PP(-15), Event('movement_petition', 30))),
        Option('Keep the figures inside the Administration.', (PP(30), Event('movement_petition', 14))),
    ), picture=0),
    EventDef('movement_petition', 'Crates of Signatures on the Steps', (
        "A column of buses reaches the Capital Centre before dawn, and by noon the square outside the Administration's offices "
        "is full. The movement has gathered signatures in all five districts on one demand: that the government stop ruling "
        "by file and give the country either a vote or a programme it can read. The organisers carry the petition in wooden "
        "crates and stack them on the steps where the photographers can reach them.",
        "The crowd is orderly and loud. Many have come down from District B, where the mountain towns feel the frontiers "
        "closest and the winters hardest, and many from the capital's own plants, where shifts have been short since spring. "
        "Speakers promise discipline, a service able to watch six frontiers and an end to an administration that answers to "
        "nobody. The police report no damage and a great deal of noise.",
        "The Administration must receive the crates in some form before the buses leave. Accepting them in person concedes "
        "that the movement speaks for half the country. Sending a clerk to sign for them insults the crowd and invites a "
        "second march. Ministers know that whatever is said on the steps today will be repeated in every district as the "
        "government's first answer to the question of who governs.",
    ), (
        Option('Receive the petition in person.', (Stability(0.02), WarSupport(0.02))),
        Option('Send a clerk to sign for the crates.', (PP(25), Stability(-0.02))),
    ), picture=0),
    EventDef('spine_report', 'Notebooks from the Line', (
        "The railway engineers return from their walk with notebooks full of measurements and a short summary on the first "
        "page. Seterano has one spine and two short limbs. The main line climbs north from the Capital Centre across the plain "
        "and into the mountains of District B, ending at the Logistics Centre where three foreign frontiers meet. A second "
        "line runs south to the naval base in District A, and a third follows the coast from there into District D.",
        "Most of the track is sound, the summary says, and very little of it is ready for hard use. The northern grade loses "
        "days to snow every winter and its cuttings fill with drifts overnight. On the plain the embankments soften through "
        "the long wet season. The stations have sidings for a peacetime timetable and nothing more. District E, on the "
        "eastern hills, has no railway at all and no road a lorry driver would trust.",
        "The engineers attach two price lists. One keeps the whole railway in public hands and pays for repairs from the "
        "national budget. The other leases the trains to operators and spends their fees on track. Before either is chosen, "
        "the Administration must decide how widely to share the notebooks, knowing that every district will turn first to "
        "the page about its own station.",
    ), (
        Option('Print the summary for every station.', (Stability(0.02), PP(-10))),
        Option('Keep it for the railway office.', (Research('train_tech', 0.5, 1),)),
    ), picture=0),
    EventDef('empty_district', 'Four Provinces and No Paved Road', (
        "The survey party that went into District E in the spring comes back in the autumn, a month late and two lorries "
        "short. The district is the largest stretch of open ground in the country and the least known. Three of its four "
        "provinces are hills running up to the frontier with Azbekerania. The fourth, inland, is dry ground where the grass "
        "gives out by midsummer and the wells are days apart. There is no factory, no railway and no paved road.",
        "People live there all the same. Herders move between the hills and the dry ground with the seasons, and the hill "
        "market days bring in buyers and sellers from across the frontier as well as from home, most of them carrying no papers. In winter snow "
        "closes the tracks for weeks; in summer rain turns them to mud. The district reaches the sea beside the frontier, "
        "where there is a beach and a few boats but nothing a harbour master would call a landing.",
        "The survey finds room for four new plants and every road the country could afford. It does not say what the "
        "district should become. A factory district would need power, housing and a line from the capital. A market district "
        "would need roads, wells and patience. First the Administration must decide whether the survey belongs to the "
        "ministries or to the people it describes.",
    ), (
        Option('Publish the survey in the district.', (Stability(0.02), PP(-10))),
        Option('Send it to the planning office.', (PP(25),)),
    ), picture=1),
    EventDef('plant_audit', 'Ten Plants and Their Furnaces', (
        "The industrial inspectors have visited every plant in Seterano, and there are only ten of them. Five make civilian "
        "goods and five make arms, spread between the Capital District, the mountains of District B and the coast of "
        "District D. The capital's plants stand on every metre of usable ground the district has, so nothing new can rise "
        "there without something old coming down. District B and District D each have a single plot left.",
        "The inspectors also count the ore. The country digs steel in all three industrial districts and more light metal "
        "than its own plants can use, with a little oil and rubber besides. Much of the steel leaves as plate and billet and "
        "much of the light metal as raw ore, because nobody at home has the furnaces to finish it. What stays makes rifles, "
        "lorries, a few wagons and spares for the only fighters the country owns.",
        "The report ends with a question instead of a recommendation. Seterano can put its ten plants and two free plots "
        "behind the service, behind sales abroad or behind the shops of five districts, and it cannot do all three well. "
        "Before that choice, the Administration must decide whether the plant managers see the figures before the ministers "
        "do, or only afterwards.",
    ), (
        Option('Show the managers first.', (Research('industry', 0.5, 1), PP(-10))),
        Option('Ministers first, managers later.', (PP(30), Stability(-0.01))),
    ), picture=1),
    EventDef('one_escort', 'A Navy of One Hull', (
        "The Maritime Service parades its entire strength at the naval base in District A, and its entire strength is one "
        "coastal escort. The crew is proud, the paint is fresh and the guns are older than most of the sailors. Behind the "
        "escort the two slipways of the southern yard stand half idle, building convoy hulls when there is steel and "
        "repairing fishing boats when there is not.",
        "Seterano has three stretches of coast and no fleet to speak of. The forest shore of District A runs out from the "
        "base, the Capital District has a short shore on the western sea, and District D and District E face the east. Sixty "
        "merchant hulls fly the national flag, most of them small and most owned by firms in the port. Their masters ask the "
        "government for charts and warnings, not for warships.",
        "The service's senior officers want a second escort and then a third. The port firms want the slipways to build "
        "coasters they can sell or sail themselves. The treasury asks why a country with six land frontiers needs a navy at "
        "all. The Administration must answer the officers first, because they have asked in public and the whole port is "
        "watching to see who is listened to.",
    ), (
        Option('Promise the service a second hull.', (XP('navy', 15), WarSupport(0.02))),
        Option('Promise the port its coasters first.', (Stability(0.02), PP(10))),
    ), picture=2),
    EventDef('three_formations', 'Eighteen Battalions and Six Frontiers', (
        "The autumn inspection finds the army exactly where the budget left it. Seterano keeps three infantry formations. "
        "Each has six infantry battalions and its own company of engineers, and two of them live in barracks at the Capital Centre. The third sits at "
        "the Logistics Centre in the mountains of District B, at the end of the railway and within a day's march of three "
        "foreign frontiers. There are lorries for most of them, trains for some and spare rifles in the depots.",
        "The inspectors are not unkind. The troops are fit and the engineers are good at their trade. The arithmetic is "
        "plain all the same: six land frontiers, two climates and three formations. The mountain formation spends its "
        "winters digging out its own barracks; the capital formations spend their summers in the mud of the plain. Nobody "
        "has planned for trouble arriving from two directions at once.",
        "The general staff offers two answers. One puts the army's weight in the mountains, where the frontiers run and a "
        "few trained companies can hold a pass. The other keeps it on the plain around the capital and trusts the railway to "
        "carry it wherever it is needed. Before choosing, the Administration must decide how much of the inspection report "
        "the soldiers themselves will hear.",
    ), (
        Option('Read the findings to every battalion.', (XP('army', 15), Stability(-0.01))),
        Option('Brief the officers only.', (PP(20), WarSupport(0.01))),
    ), picture=0),
    EventDef('six_frontiers', 'Six Neighbours on One Wall', (
        "The foreign office pins its new frontier map to the cabinet room wall, and the ministers count six coloured lines. "
        "Slavia lies to the west, beyond the capital plain and the western mountains. Valka meets the western end of District "
        "B. Malynea lies across the northern mountains and Baltica beyond the north-eastern passes. Yuktobania, many times "
        "Seterano's size, touches a single mountain province in the far north-east. Azbekerania runs down the whole eastern "
        "side to the coast of District E.",
        "Every one of those lines passes through District B. Three of them meet around the Logistics Centre in the west of "
        "the district, and three more meet at that one province in the north-east. Herders, smugglers, skiers and lorry "
        "drivers cross them every week, mostly on paths no customs officer has walked. Some neighbours keep posts and patrols "
        "on their own side of the passes; Seterano has kept fewer on its side. None of the frontiers is disputed in any file "
        "the ministry holds, and few are well understood.",
        "The map changes nothing on the ground. It does show the ministers how small the country is and how many doors it "
        "has. They can treat the mountains as neutral ground, look to the neighbours for practical talks or count and control "
        "every crossing. First they must decide whether the map stays in the cabinet room or goes out to the districts that "
        "live along its lines.",
    ), (
        Option('Send the map to the frontier districts.', (Stability(0.02), PP(-10))),
        Option('Keep the map in the cabinet room.', (PP(25), WarSupport(0.01))),
    ), picture=1),
    EventDef('ulysses_notice', 'A Paragraph Between the Weather and the Trains', (
        "In December 1994 the astronomers' international union warns that Ulysses, an asteroid on a near course, could hit "
        "the Earth. In Seterano the notice arrives as a short paragraph on the evening radio, read between the "
        "weather forecast and the railway timetable, and for a day it is treated as a curiosity. By the end of the week the "
        "ministries are opening letters from every district asking what the government intends to do.",
        "The two climates breed two kinds of fear. In the northern mountains and on the eastern hills people ask about rock "
        "falls, avalanches and roads cut off for a whole winter. In the capital and along the southern coast they ask about "
        "fire, flood and the sea. The engineers note that the mountains are solid rock that could be tunnelled, while the "
        "plain offers only cellars dug into soft and often waterlogged ground.",
        "Nobody can yet say whether the asteroid will strike, still less where. The Administration has to decide how to talk "
        "about a danger it cannot measure. A plain weekly notice would treat the public as adults and invite new questions "
        "every week. A quiet planning office would avoid alarm and leave the rumours to grow on their own. The letters keep "
        "arriving either way, and the postmen have started to carry them in sacks.",
    ), (
        Option('Broadcast a weekly notice.', (Stability(-0.01), WarSupport(0.02))),
        Option('Plan quietly first.', (Stability(0.02),)),
    ), citation='date anchor only, Official Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; the Seteranoan response is '
                'gameplay', picture=1),
    EventDef('roche_night', 'A Summer Night of Waiting', (
        "In July 1999 the asteroid passes inside the distance at which the Earth's pull tears it apart. Across Seterano "
        "families sit up through a warm night on the plain and a cool one in the mountains, radios on, while the shelter "
        "wardens walk their streets. The trains on the spine are held in their stations and the Logistics Centre keeps its "
        "lorries fuelled and its doors open to anyone who comes.",
        "The night brings fear and very little news. The radio repeats what the astronomers have already said and adds "
        "nothing about where the fragments will come down. Wardens report crowded cellars in the capital and empty ones in "
        "the villages, where people prefer to watch the sky from their doorsteps. In District B the mountain galleries fill "
        "early. By morning the wardens have little to report beyond sleepless streets and long queues for bread.",
        "The Administration must decide how to close the alert. Ending it at once would have the plants and the trains "
        "working by noon and would tell the country that the danger is past, which nobody can yet promise. Holding it a few "
        "days longer would cost shifts and patience and look like caution. The neighbours are making the same choice, and "
        "none of them knows any more than Seterano does.",
    ), (
        Option('End the alert at once.', (Stability(0.02), PP(10))),
        Option('Hold the alert a few days more.', (WarSupport(0.02), Stability(-0.01))),
    ), citation='date anchor only, Official Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no damage in Seterano is '
                'claimed or denied', picture=1),
    EventDef('distant_war', 'Crude Prices and a Distant War', (
        "In late March 1995 the long quarrel around Belka becomes a war, and the news reaches Seterano the way it reaches "
        "most small countries: secondhand, late and alarming. The war is far away and Seterano has no part in it. Within a "
        "fortnight it still finds its way into the country, through the price of crude on the world market and the premiums "
        "insurers now charge on every merchant hull at sea.",
        "The fuel office reports that the single silo at the capital holds enough for the service's normal year and not a "
        "great deal more. The country pumps a little crude of its own in three districts, too little to cover the plants, "
        "the trains and the lorries together. The port firms say the masters of the sixty merchant hulls are asking whether "
        "to sail at all, and plant managers ask whether arms orders will rise or fall.",
        "The Administration cannot change the war and it cannot change the market. It can decide what the country is told "
        "and how it spends the crude it has. Rationing early would be prudent and unpopular. Waiting would be popular until "
        "the day the silo runs low. The ministers argue through the night and agree only that the first statement must be "
        "made before the weekend markets open.",
    ), (
        Option('Announce fuel rules now.', (WarSupport(0.02), Stability(-0.02))),
        Option('Reassure first and ration if needed.', (Stability(0.02), WarSupport(-0.01))),
    ), citation='date anchor only, Official Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Seteranoan response is '
                'gameplay', picture=2),
    EventDef('decade_account', 'The Account Without a Foreword', (
        "Early in the new century the statistics office publishes a plain account of the country since 1991. It lists the "
        "five districts, the plants old and new, the spine and its two limbs, the capital field, the escort at the southern "
        "port and the three formations. Beside each it prints what changed and what the change cost. The report carries no "
        "foreword from the government and no photographs, and it sells out in a week.",
        "The account flatters nobody. District E has changed the most and still trails the other four. The capital has grown "
        "upward because it could not grow outward. The six frontiers are calm, but the crossings are busier than the posts "
        "that watch them. The answer the country gave to the question of who governs has held so far, and the account "
        "records, district by district, how many people never accepted it.",
        "The government must decide how to respond. It can let the account stand without comment, which some will read as "
        "confidence and others as indifference. Or it can publish a reply setting out what the next years will bring, which "
        "will be quoted back at every minister who misses a date. The districts are reading in either case, and the movement "
        "and the administrators have both marked their copies.",
    ), (
        Option('Let the account stand alone.', (Stability(0.03), PP(-10))),
        Option('Publish a reply with dates.', (PP(30), Stability(-0.01))),
    ), picture=0),
)

# --- branches ------------------------------------------------------------------------------------
FEDERATION = Branch('fed', 'A Federation Run from One Desk', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('fed_open_files', 'Open the Administration Files',
          "The National Administration governs all five districts from one office in the capital, under a democratic label that "
          "roughly one voter in a hundred supports. Opening its files on budgets, appointments and district spending is the "
          "cheapest way to start an honest argument about who should govern, and the surest way to end a quiet life for "
          "the officials who keep them.",
          ('document', 'assembly'), reward=(Idea('one_desk'), Event('one_in_a_hundred'))),
    Focus('fed_district_roll', 'A Roll of the Five Districts',
          "Clerks list what each district pays in taxes and receives in roads, schools and wages: the crowded Capital District, "
          "the mountains of District B, the port in District A, the coast of District D and the empty hills of District E. The "
          "roll embarrasses the capital and arms every district notable with figures. No settlement of the federation can "
          "be written without it.",
          ('document', 'civil'), after=('fed_open_files',), reward=(Flag('district_roll'), PP(15))),
    Focus('fed_hearings', 'Hearings in Every District Hall',
          "Before deciding anything, the Administration sends a panel of officials to hear petitions in each district. The "
          "movement fills the halls of District B and the capital plants, merchants and administrators dominate the port, and "
          "District E sends herders who have never met a minister. The hearings cost months and patience, and they show the "
          "government a country it has not been listening to.",
          ('assembly', 'civil'), after=('fed_open_files',), reward=(TimedIdea('hearing_season', 365),)),
    Focus('fed_question', 'What the Federation Means',
          "The country calls itself a federation, yet nothing in the way it is governed gives the districts a voice of their "
          "own. The Administration must now decide how that word will be filled: by restoring a ballot district by district, "
          "by appointing professional prefects to run them, or by bringing the movement that polls half the country into "
          "government on agreed terms.",
          ('scales', 'document'), after=('fed_district_roll', 'fed_hearings'),
          reward=(PP(35), Tooltip('Opens three political paths; only one can be taken.'))),
    Focus('fed_path_ballot', 'Return the Ballot to the Districts',
          "The democratic answer restores the vote, district by district, with a federal council elected on district lists. "
          "It honours the name printed on every passport. It also hands an election to a party that one voter in a hundred "
          "supports, facing a movement that half the country follows. The Administration accepts in advance that it may lose "
          "what it has run for years.",
          ('ballot', 'assembly'), after=('fed_question',), exclusive=('fed_path_prefects', 'fed_path_movement'),
          reward=(SwapIdea('one_desk', 'ballot_pledge'),)),
    Focus('fed_path_prefects', 'Prefects Instead of Parties',
          "The administrators' answer keeps the ballot suspended and gives each district a career prefect who answers to a "
          "board in the capital. Budgets are published, appointments are made by examination and parties have no seats. It "
          "suits the forty-eight in a hundred who already trust the Administration, and it gives the other half of the "
          "country nothing to vote for and an obvious target.",
          ('command', 'document'), after=('fed_question',), exclusive=('fed_path_ballot', 'fed_path_movement'),
          reward=(SwapIdea('one_desk', 'prefect_rule'),)),
    Focus('fed_path_movement', 'Terms for the Majority Movement',
          "The third answer invites the movement that polls half the country to name a government on written terms: no change "
          "to any frontier, a defensive service and district courts left alone. Its organisers promise discipline and an end "
          "to rule by file. The Administration would be handing power to a movement whose programme fits on a poster, and "
          "trusting a sheet of paper to hold it.",
          ('security', 'assembly'), after=('fed_question',), exclusive=('fed_path_ballot', 'fed_path_prefects'),
          reward=(SwapIdea('one_desk', 'movement_terms'),)),
    Focus('fed_seat_council', 'Seat the Federal Council',
          "District lists go to the polls, and the council they elect takes the seals of government from the National "
          "Administration. It governs collectively, publishes its budget a season before voting it and must face the voters "
          "again on a fixed calendar. The change runs through the office, not a person, and the council inherits a country in "
          "which its own supporters are few.",
          ('ballot', 'document'), after=('fed_path_ballot',), cost=10,
          exclusive=('fed_seat_prefects', 'fed_seat_movement'), reward=(Regime('federal_council'), Flag('order_ballot'))),
    Focus('fed_seat_prefects', 'Install the Board of Prefects',
          "Five prefects, one for each district, take their posts by examination, and a board in the capital chaired by a "
          "senior administrator holds the seals. The ballot stays suspended. Orders are numbered, dated and printed in every "
          "district hall. The board is competent, slow to anger and slow to change, and its legitimacy rests entirely on "
          "keeping everything working.",
          ('command', 'assembly'), after=('fed_path_prefects',), cost=10,
          exclusive=('fed_seat_council', 'fed_seat_movement'), reward=(Regime('prefect_board'), Flag('order_prefects'))),
    Focus('fed_seat_movement', 'Seals for the Movement Committee',
          "The movement names an executive committee and takes the seals of government under its written terms. Other parties "
          "are suspended, the press works under licence and the country is governed by numbered decree. The committee promises "
          "calm in the districts and a stronger service at home. The terms are all that stands between those promises and "
          "whatever the committee decides to do next.",
          ('security', 'command'), after=('fed_path_movement',), cost=10,
          exclusive=('fed_seat_council', 'fed_seat_prefects'), reward=(Regime('movement_committee'), Flag('order_movement'))),
    Focus('fed_district_budgets', 'Budgets for District Councils',
          "The federal council gives each district an elected council and a budget line of its own for roads, schools and "
          "clinics, drawn from the figures on the district roll. The capital keeps the service, the railway, foreign affairs "
          "and the currency. District E receives more than it pays and the capital pays more than it receives, which the "
          "capital's voters notice at once.",
          ('assembly', 'scales'), after=('fed_seat_council',), requires=(HasFlag('district_roll'),),
          exclusive=('fed_prefect_circuit', 'fed_movement_marches'), reward=(SwapIdea('ballot_pledge', 'federal_compact'),)),
    Focus('fed_prefect_circuit', 'The Prefects Inspect in Spring',
          "Each spring the five prefects travel their districts on a fixed route, inspecting tax offices, road works and "
          "schools and printing what they find. The circuit ends the old habit of sending only good news to the capital. It "
          "costs salaries, train time and goodwill among local notables, who dislike being inspected by officials they never "
          "chose.",
          ('command', 'rail'), after=('fed_seat_prefects',),
          exclusive=('fed_district_budgets', 'fed_movement_marches'), reward=(SwapIdea('prefect_rule', 'prefect_code'),)),
    Focus('fed_movement_marches', 'Marches by Licence Only',
          "The committee licenses every public meeting and march, its own included, and posts stewards around the Capital "
          "Centre on market days. The streets go quiet and the movement's rallies get the best squares. Opponents meet in back "
          "rooms and kitchens. The calm is real and measurable, and it has been bought by telling half the country to stay at "
          "home.",
          ('security', 'civil'), after=('fed_seat_movement',),
          exclusive=('fed_district_budgets', 'fed_prefect_circuit'), reward=(SwapIdea('movement_terms', 'movement_order'),)),
    Focus('fed_settlement', 'A Settlement Written Down',
          "Whichever order now governs, its arrangements are gathered into one printed settlement: who appoints whom, what each "
          "district controls, how the budget passes and how the order itself may be changed. Writing it down costs every "
          "faction some ambiguity it liked. It also lets later governments argue about the wording instead of the "
          "foundations.",
          ('document', 'peace'), after_any=('fed_district_budgets', 'fed_prefect_circuit', 'fed_movement_marches'),
          reward=(Idea('written_settlement'), Stability(0.02))),
))

SPINE = Branch('spine', 'The Spine and Its Two Limbs', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('spine_walk', 'Walk the Spine from Pass to Port',
          "Railway engineers walk every metre of the national line: north from the Capital Centre across the plain and up the "
          "mountain grade to the Logistics Centre, south to the naval base in District A, and along the coast into District D. "
          "Their notebooks will decide where the next decade's money goes. The walk takes a season and cancels two freight "
          "trains a week while it lasts.",
          ('rail', 'document'), reward=(Idea('spine_ledger'), Event('spine_report'))),
    Focus('spine_junction', 'Junction Yards at the Capital Centre',
          "Nearly every train in the country passes through the Capital Centre, and its yard was laid out for a timetable that no "
          "longer exists. New sidings, a turntable and a second platform let northbound and southbound traffic pass without "
          "waiting. The work closes the yard at weekends through a summer of mud and heat, and the plants lose deliveries "
          "while it lasts.",
          ('rail', 'tools'), after=('spine_walk',), reward=(Build('infrastructure', 1, 0),)),
    Focus('spine_snow_sheds', 'Snow Sheds on the Northern Grade',
          "Where the line climbs into the mountains of District B, drifts close the cuttings in a single night and blizzards "
          "halt the trains for days. Timber and concrete sheds over the worst cuttings keep the track open through the "
          "winter. They are costly, ugly and need repairs every spring, and they decide whether the Logistics Centre can be "
          "supplied in January.",
          ('rail', 'shelter'), after=('spine_walk',), reward=(Build('infrastructure', 1, 356),)),
    Focus('spine_embankments', 'Raise the Plain Embankments',
          "On the capital plain the rain falls for half the year and the embankments soften under loaded wagons. Raising and "
          "draining them is plain earthwork, done with shovels and borrowed army lorries. It is the least glamorous project "
          "the railway office has ever proposed, and the one most likely to keep the spine running through a long wet season.",
          ('rail', 'civil'), after=('spine_walk',), reward=(Idea('dry_embankments'),)),
    Focus('spine_coast_ballast', 'Ballast for the Coast Line',
          "The limb from the southern port into District D runs along the forest coast, close enough to the sea that storms "
          "wash out its ballast. New stone, culverts and a sea wall at the worst bends keep freight moving between the port "
          "and the plants of District D. The quarries are inland, so the stone must travel by the line it is meant to "
          "protect.",
          ('rail', 'navy'), after=('spine_walk',), reward=(Build('infrastructure', 1, 377),)),
    Focus('spine_public_line', 'Keep the Line in Public Hands',
          "The railway office proposes that the state own the track, the trains and the timetable together, paying for repairs "
          "from the national budget. Every district would pay the same fares and the service would get the trains it needs at "
          "a day's notice. The budget carries the losses, and the railway office becomes the largest employer in the country.",
          ('rail', 'command'), after_any=('spine_junction', 'spine_snow_sheds', 'spine_coast_ballast'), cost=10,
          exclusive=('spine_lease_trains',), reward=(SwapIdea('spine_ledger', 'public_railway'),)),
    Focus('spine_lease_trains', 'Lease the Trains, Keep the Track',
          "The alternative keeps the track public and leases the trains to operators, who pay a fee for each path they run. "
          "The fees go straight into repairs, and the operators chase freight the state never bothered with. Fares rise on "
          "quiet lines, and the service must bargain for its trains like any other customer when it needs them.",
          ('rail', 'economy'), after_any=('spine_junction', 'spine_snow_sheds', 'spine_coast_ballast'), cost=10,
          exclusive=('spine_public_line',), reward=(SwapIdea('spine_ledger', 'leased_trains'),)),
    Focus('spine_wagon_works', 'Wagon Orders for the Capital Shops',
          "With the whole railway in public hands, the capital's plants receive a standing order for wagons, brake gear and "
          "spare wheels. The order keeps two shops busy for years and trains a generation of fitters. It also ties the plants "
          "to a single customer who pays slowly, and the treasury warns that the order will be the first thing cut in a bad "
          "year.",
          ('tools', 'rail'), after=('spine_public_line',), reward=(Research('train_tech', 0.5, 2),)),
    Focus('spine_track_fund', 'A Track Fund from the Fees',
          "Operators' fees go into a separate track fund that the railway office may spend on nothing else. The first years "
          "pay for new sleepers and signals at the capital end of the line. The fund is small and closely guarded, and it "
          "makes the leased railway popular with engineers and unpopular with ministers who would like to borrow from it.",
          ('economy', 'rail'), after=('spine_lease_trains',), reward=(Build('infrastructure', 1, 0),)),
    Focus('spine_crisis_timetable', 'Mobilisation by the Timetable',
          "The railway office and the general staff write one timetable for a crisis: which trains move which formation, from "
          "which yard, in how many hours. Every station master holds a sealed copy. Exercises run twice a year and delay "
          "freight each time. The spine becomes the country's real defence plan, because it is the only way to move three "
          "formations quickly.",
          ('rail', 'security'), after_any=('spine_wagon_works', 'spine_track_fund'), reward=(Idea('crisis_timetable'),)),
))

EAST = Branch('east', 'District E Has No Road', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('east_survey', 'Send Surveyors into District E',
          "District E is the largest stretch of open ground in Seterano and the least known: three hill provinces along the "
          "eastern frontier and a dry inland province where the wells are far apart. It has no road, no railway and no "
          "factory. A survey party with lorries, maps and a radio is the first step, and the first lorry to come back late is "
          "the first price.",
          ('tools', 'civil'), reward=(Build('infrastructure', 1, 470), Event('empty_district'))),
    Focus('east_graded_track', 'A Graded Track from the Capital',
          "A graded and ditched track from the capital plain across the dry ground to the eastern hills gives District E its "
          "first route a lorry can use in most months. It is gravel, not asphalt, and snow still closes it in deep winter. It "
          "brings doctors, teachers and buyers within a day of the capital for the first time in anyone's memory.",
          ('logistics', 'civil'), after=('east_survey',), reward=(Build('infrastructure', 1, 470),)),
    Focus('east_markets', 'Stalls and Scales for the Hill Markets',
          "On the hill market days, Seteranoan herders and visitors from over the eastern frontier already trade wool, grain "
          "and tools with little paperwork. The district hires market wardens, buys honest scales and seats a customs clerk at a table "
          "rather than behind a barrier. Trade rises and stays visible. Some regulars, used to no paperwork at all, take their "
          "business somewhere quieter.",
          ('economy', 'civil'), after=('east_survey',), reward=(Idea('hill_markets'),)),
    Focus('east_wells', 'Wells on the Dry Ground',
          "The inland province of District E is dry ground where grass gives out by midsummer and herders walk for days "
          "between water. Drilling crews from the capital sink deep wells along the new track and cap them against the winter "
          "frost. The wells cost more than they earn, and they decide whether anyone can live beside the track rather than "
          "merely travel along it.",
          ('civil', 'tools'), after=('east_survey',), reward=(Idea('dry_wells'),)),
    Focus('east_factory_district', 'Plants for the Eastern Hills',
          "The planners propose that District E take the plants the crowded capital cannot hold: two civilian works beside the "
          "new track, with housing for their crews. The district would change faster than any other in the country. Herders "
          "would lose pasture, the track would need upgrading at once and the hill markets would become a factory town's "
          "shops.",
          ('industry', 'civil'), after_any=('east_graded_track', 'east_markets'), cost=10,
          exclusive=('east_market_district',), reward=(Build('industrial_complex', 2, 470), Flag('east_industry'))),
    Focus('east_market_district', 'Keep the East for Fairs and Herds',
          "The opposite plan keeps District E a district of pasture and markets, spending on roads, wells and fairs instead of "
          "plants. Change comes slowly and the district stays poorer than the others for longer. Its people keep their land, "
          "the frontier trade grows in the open, and the capital's industrial planners must look for ground somewhere else.",
          ('economy', 'peace'), after_any=('east_graded_track', 'east_markets'), cost=10,
          exclusive=('east_factory_district',),
          reward=(SwapIdea('hill_markets', 'frontier_fairs'), Build('infrastructure', 1, 470), Flag('east_fairs'))),
    Focus('east_arms_hall', 'An Arms Hall Behind the Hills',
          "With civilian works already standing in District E, the planners add one arms hall behind the hills, away from "
          "every coast and close to no city. It gives the service a plant outside the capital and spreads the country's few "
          "arms lines across more ground. The district gains wages and loses the last of its quiet to the night shift.",
          ('industry', 'security'), after=('east_factory_district',), reward=(Build('arms_factory', 1, 470),)),
    Focus('east_landing', 'A Landing on the Eastern Shore',
          "District E reaches the sea beside the frontier, where a beach and a few boats serve the coast villages. A small yard "
          "and a stone landing let fishing boats and coasters work through the season and give the fairs a sea route to the "
          "southern port. It is a modest yard that will never build a warship, and the port firms resent it all the same.",
          ('fishing', 'navy'), after=('east_market_district',), reward=(Build('dockyard', 1, 470),)),
    Focus('east_shore_road', 'A Road Down to the Eastern Shore',
          "The last piece of the plan is a road from the graded track down through the hills to the shore beside the frontier, "
          "with bridges over the spring torrents. It joins the coast villages to the rest of the country and gives the eastern "
          "frontier a route that does not depend on the snow. District E finally appears on the national road map as an "
          "unbroken line.",
          ('logistics', 'bridge'), after_any=('east_arms_hall', 'east_landing'),
          reward=(Build('infrastructure', 1, 470), Idea('eastern_charter'))),
))

WORKS = Branch('works', 'Ten Plants and Two Free Plots', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_count', 'Count Every Furnace and Lathe',
          "Seterano has ten plants: two civilian and two arms works crowding the Capital District, two civilian works and one "
          "arms works in the mountains of District B, and one civilian and two arms works on the coast of District D. "
          "Inspectors count every furnace, lathe and idle shift. The count annoys managers and costs a season, and it is the "
          "only honest place to start.",
          ('industry', 'document'), reward=(Idea('plant_count'), Event('plant_audit'))),
    Focus('works_double_shifts', 'Two Shifts on the Full Ground',
          "The capital's plants stand on every metre of usable ground the district has, so the only way to make more there is "
          "to work longer. A second shift on the main lines, with a night bus and a canteen, raises output without a single "
          "new wall. Workers earn more and sleep less, and the plain's hot summers make the night shift the popular one.",
          ('industry', 'civil'), after=('works_count',), reward=(TimedIdea('two_shifts', 730),)),
    Focus('works_light_metal', 'Light Metal from Three Districts',
          "The country digs more light metal ore than its own plants can use, from the capital plain, the mountains and the "
          "coast of District D, and most of it leaves raw. A geological office maps the deposits properly and tests what could "
          "be smelted at home if power and furnaces allowed. The survey is cheap; acting on it will not be.",
          ('tools', 'economy'), after=('works_count',), reward=(Research('excavation_tech', 0.5, 1), Flag('metal_mapped'))),
    Focus('works_service_lines', 'The Service Comes First',
          "The first model puts the ten plants behind the service: rifles, lorries, support kit and spares for the twelve "
          "fighters before anything for the shops. It matches the budget the country already keeps and the six frontiers it "
          "has to watch. Shops stay thin, and the plants depend on one customer whose orders follow the political weather.",
          ('security', 'industry'), after_any=('works_double_shifts', 'works_light_metal'), cost=10,
          exclusive=('works_metal_exports', 'works_district_goods'), reward=(SwapIdea('plant_count', 'service_lines'),)),
    Focus('works_metal_exports', 'Plate and Ore for Buyers Abroad',
          "The second model sells what the ground gives: steel plate and light metal ore to foreign buyers, with the earnings "
          "spent on machine tools. It suits a country with more ore than furnaces. It also ties the plants to world prices "
          "that a war on the far side of the oceans can double or halve in a month, and the service waits behind every "
          "export order.",
          ('economy', 'diplomacy'), after_any=('works_double_shifts', 'works_light_metal'), cost=10,
          requires=(HasFlag('metal_mapped'),),
          exclusive=('works_service_lines', 'works_district_goods'), reward=(SwapIdea('plant_count', 'metal_sales'),)),
    Focus('works_district_goods', 'Goods for the Five Districts',
          "The third model turns the civilian works toward stoves, pumps, bicycles and radios for the districts, with excise "
          "relief for the first years. Shops fill in District E and the mountain towns for the first time. The service gets "
          "less and later, the treasury loses revenue, and the plant managers must learn to sell rather than simply deliver.",
          ('civil', 'economy'), after_any=('works_double_shifts', 'works_light_metal'), cost=10,
          exclusive=('works_service_lines', 'works_metal_exports'), reward=(SwapIdea('plant_count', 'district_goods'),)),
    Focus('works_mountain_arsenal', 'An Arms Hall at the Mountain Works',
          "District B has one free plot left beside its mountain works, close to the end of the railway and the Logistics "
          "Centre. An arms hall there puts production near the formation that would need it first. Winters will cost shifts "
          "and every ton of steel must climb the northern grade, but the service gains a second arms centre outside the "
          "capital.",
          ('security', 'tools'), after=('works_service_lines',), reward=(Build('arms_factory', 1, 356),)),
    Focus('works_rolling_mill', 'A Rolling Mill in District D',
          "District D's last free plot goes to a rolling mill that turns raw steel into finished plate and section before it "
          "leaves by sea. The country sells more value and less ore, and the coast limb of the railway gets steady freight. "
          "The mill needs more power than the coast can spare, and it will run short shifts until a new line is strung.",
          ('industry', 'navy'), after=('works_metal_exports',), reward=(Build('industrial_complex', 1, 377),)),
    Focus('works_goods_hall', 'A Goods Hall in the Mountain Towns',
          "The mountain towns of District B have the country's coldest winters and its emptiest shops. A goods hall on the last "
          "free plot beside the mountain works makes stoves, boots and radios where they are needed most, without hauling "
          "them up the northern grade. It is a modest plant, popular in the towns and doubted by planners who wanted that "
          "plot for arms.",
          ('civil', 'industry'), after=('works_district_goods',), reward=(Build('industrial_complex', 1, 356),)),
    Focus('works_spares', 'Spares Before New Equipment',
          "Whatever the plants now make first, the research office sets one rule above it: spares, replacement parts and repair "
          "kits come before new designs. It fits a small service that must keep old equipment working for years. Engineers "
          "grumble about drawings that never leave the office, while lorries, rifles and the twelve fighters stay in service "
          "longer.",
          ('tools', 'logistics'), after_any=('works_mountain_arsenal', 'works_rolling_mill', 'works_goods_hall'),
          reward=(Idea('spares_rule'),)),
))

PORT = Branch('port', 'One Escort at the Southern Port', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('port_muster', 'The Whole Navy on the Quay',
          "The Maritime Service is one coastal escort, its crew and the naval base in District A, with two slipways beside it "
          "that build convoy hulls when steel allows. Mustering it in public, with families on the quay, tells the port that "
          "the country remembers it has a coast. It also shows every visitor exactly how small the navy is.",
          ('navy', 'medal'), reward=(Idea('one_hull'), Event('one_escort'))),
    Focus('port_charts', 'Charts of the Forest Coast',
          "The southern coast is forest down to the waterline, with shoals that the old charts place in the wrong spots. A "
          "survey launch and two seasons of soundings produce charts the merchant masters can trust. The work is slow and the "
          "launch is the escort's only companion at sea. The new charts are sold cheaply to every hull that asks, foreign ones "
          "included.",
          ('navy', 'document'), after=('port_muster',), reward=(Research('naval_equipment', 0.5, 1), Flag('coast_charted'))),
    Focus('port_coast_radar', 'A Radar Mast over the Port',
          "A radar mast on the hills above the naval base watches the approaches to the port and the forest coast on either "
          "side. It is the only electronic eye the Maritime Service owns. Its crew sleep in a hut at the top of the hill, and "
          "the first winter proves that the mud road up to it needs as much care as the set itself.",
          ('radar', 'navy'), after=('port_muster',), reward=(Build('radar_station', 1, 353),)),
    Focus('port_listening', 'Hydrophones After the Cinigrad Notice',
          "In September 1991 Yuktobania announces a new class of submarine at a political convention in Cinigrad. Seterano has "
          "no quarrel with anyone at sea, and its one escort could not hunt a submarine if it found one. The service still asks "
          "for hydrophones laid along the newly charted shoals, so that it at least knows what passes. The request is cheap, "
          "quiet and a little embarrassing.",
          ('submarine', 'radar'), after=('port_charts',), requires=(HasGlobal('ac_bwr_cinigrad'), HasFlag('coast_charted')),
          reward=(Idea('shoal_hydrophones'),)),
    Focus('port_second_escort', 'A Second Escort from the Slipways',
          "The service's officers get their way: the slipways in District A are lengthened, a building hall rises beside them "
          "and a second escort is laid down. The navy doubles in size on paper. The steel comes from plants that would "
          "otherwise make lorries, and the port firms lose the slipway time they had counted on for coasters.",
          ('navy', 'tools'), after_any=('port_charts', 'port_coast_radar'), cost=10, exclusive=('port_coasters',),
          reward=(Build('dockyard', 1, 353), SwapIdea('one_hull', 'two_hulls'))),
    Focus('port_coasters', 'Coasters Before Warships',
          "The port firms get their way instead: the slipways build small coasters to carry steel, timber and grain between "
          "the southern port, District D and foreign harbours, and a goods shed and repair works rise beside the yard. The "
          "escort sails alone for years more. The country gains trade, and the officers gain a grievance they will repeat "
          "at every budget.",
          ('logistics', 'navy'), after_any=('port_charts', 'port_coast_radar'), cost=10, exclusive=('port_second_escort',),
          reward=(Build('industrial_complex', 1, 353), SwapIdea('one_hull', 'coaster_lanes'))),
    Focus('port_hull_register', 'A Register of Sixty Hulls',
          "Sixty merchant hulls fly the national flag, most of them small and owned by firms in the port. A register in the "
          "harbour office records each one's master, route, cargo and radio, and sends out warnings of storms and trouble. "
          "Owners complain about paperwork. When the sea lanes turn dangerous, the register will be the only way to know where "
          "every crew is.",
          ('document', 'logistics'), after_any=('port_second_escort', 'port_coasters'), reward=(Idea('hull_register'),)),
    Focus('port_cranes', 'New Cranes for the Southern Yard',
          "Whichever hulls the yard builds, its cranes are older than its foremen. Two modern travelling cranes and a covered "
          "fitting-out berth let the yard work through the rainy season and handle larger sections. The cranes come from "
          "abroad and are paid for over ten years. The yard becomes a place where hulls are built, not merely assembled.",
          ('tools', 'navy'), after_any=('port_second_escort', 'port_coasters'), reward=(Build('dockyard', 1, 353),)),
    Focus('port_seamanship', 'A Seamanship School at the Base',
          "The base opens a seamanship school for escort crews, merchant officers and harbour pilots, taught by the service's "
          "few senior sailors. Merchant cadets pay fees and escort crews do not. The school spreads the navy's habits into the "
          "merchant fleet and gives the service a way to find recruits beyond the port's own families.",
          ('training', 'navy'), after_any=('port_hull_register', 'port_cranes'), reward=(XP('navy', 25), TimedIdea('sea_school', 730))),
))

GUARD = Branch('guard', 'Three Formations for Six Frontiers', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_inspection', 'Inspect the Three Formations',
          "The army is three infantry formations, every one built from six battalions and a company of engineers, with two "
          "based at the Capital Centre and one at the Logistics Centre in the mountains. An autumn inspection measures their kit, their training and "
          "their lorries against six land frontiers and two climates. The answers will be uncomfortable, and the general staff "
          "asks for them anyway.",
          ('training', 'security'), reward=(Idea('thin_line'), Event('three_formations'))),
    Focus('guard_lorry_pool', 'A Common Pool for the Lorries',
          "The formations hold several hundred lorries between them, each battalion keeping its own in its own way and "
          "repairing them when someone has time. A common pool at each Centre, with fitters, a parts store and a duty roster, "
          "keeps more of them running. Battalion commanders lose control of their own transport and complain loudly until "
          "the day they need it.",
          ('logistics', 'tools'), after=('guard_inspection',), reward=(Idea('lorry_pool'),)),
    Focus('guard_engineers_lent', 'Engineers on the Eastern Track',
          "Each formation has an engineer company that spends most of its time waiting for a war. Lending the companies to "
          "District E for a summer, building culverts and bridges on the new track, trains them on real ground and saves the "
          "road budget. The formations go without their engineers for months, and commanders worry about what happens if "
          "they are needed elsewhere.",
          ('tools', 'security'), after=('guard_inspection',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('guard_mountain_weight', 'Weight on the Mountain Frontier',
          "The first doctrine puts the army's weight in District B, where all six frontiers run and a few trained companies can "
          "hold a pass. A second formation moves up the northern grade to winter quarters at the Logistics Centre. The capital "
          "keeps one formation and the railway, and the mountain towns gain soldiers, noise and custom.",
          ('security', 'command'), after_any=('guard_lorry_pool', 'guard_engineers_lent'), cost=10,
          exclusive=('guard_plain_weight',), reward=(SwapIdea('thin_line', 'mountain_weight'), Flag('doctrine_mountain'))),
    Focus('guard_plain_weight', 'Hold the Centre on the Plain',
          "The second doctrine keeps two formations on the capital plain near the junction yards and trusts the railway to "
          "carry them north, south or east in hours. The mountains keep one formation, and the passes are watched rather than "
          "held. It is cheaper and faster on paper, and it depends entirely on trains running through the snow.",
          ('rail', 'command'), after_any=('guard_lorry_pool', 'guard_engineers_lent'), cost=10,
          exclusive=('guard_mountain_weight',), reward=(SwapIdea('thin_line', 'plain_weight'), Flag('doctrine_plain'))),
    Focus('guard_ski_companies', 'Ski Companies for the Blizzard Months',
          "Seteranoan soldiers already learn mountain craft, but few can move on skis in a blizzard. Each battalion in the "
          "mountains trains one company to ski, live in snow shelters and carry its own supplies for a week. Injuries in "
          "training are frequent and reported in every paper. The companies become the army's pride and its most expensive "
          "soldiers per head.",
          ('training', 'shelter'), after=('guard_mountain_weight',), reward=(Idea('ski_companies'),)),
    Focus('guard_trains_in_steam', 'Two Trains Kept in Steam',
          "Two complete trains, with flat wagons for lorries and coaches for a battalion, stand ready at the capital yard with "
          "their crews on call. Freight loses the stock and the railway loses revenue. In exchange a battalion can be on the "
          "northern grade or at the southern port within hours of an order, whatever the weather is doing on the plain.",
          ('rail', 'logistics'), after=('guard_plain_weight',), reward=(Idea('steam_ready'),)),
    Focus('guard_district_rolls', 'District Rolls of Former Soldiers',
          "Everyone who has served is entered on a reserve roll in their own district, with an address, a trade and a depot to "
          "report to. The rolls let three formations become six in a crisis, at least on paper. Keeping them current costs "
          "clerks and postage every year, and employers dislike losing workers to the annual muster.",
          ('document', 'training'), after_any=('guard_ski_companies', 'guard_trains_in_steam'), reward=(Idea('district_rolls'),)),
    Focus('guard_two_climates', 'An Exercise in Two Climates',
          "For one week in winter and one in the wet season, all three formations move to their crisis positions by the "
          "timetable, through snow in the mountains and mud on the plain. Umpires mark every delay. The exercises cost fuel, "
          "freight and two weeks of plant shifts, and they show what the doctrine chosen years earlier actually delivers.",
          ('command', 'training'), after=('guard_district_rolls',), requires=(After('1996.1.1'),),
          reward=(XP('army', 30), WarSupport(0.02))),
))

SKY = Branch('sky', 'Twelve Fighters at the Capital Field', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('sky_runway', 'A Longer Runway on the Plain',
          "The country's twelve fighters fly from a single field at the capital, with a runway laid for older aircraft and "
          "drains that fail every wet season. Lengthening and draining it, and adding dispersal pads, lets the squadron fly in "
          "most weather and receive larger aircraft. Contractors must work around the squadron's own flying, which slows "
          "everything down.",
          ('runway', 'air'), reward=(Build('air_base', 1, 0),)),
    Focus('sky_forecasters', 'Forecasters at the Capital Field',
          "Pilots at the capital fly between two climates: blizzards over the northern mountains and eastern hills, heavy rain "
          "and heat over the plain and the coast. A forecasting room at the field, with observers telephoning from the "
          "Logistics Centre and the port, gives the squadron a forecast it can plan on. Farmers and the railway use the "
          "forecasts too.",
          ('telescope', 'air'), after=('sky_runway',), reward=(Idea('two_climate_forecast'),)),
    Focus('sky_north_radar', 'Radar Above the Northern Passes',
          "A radar on the high ground of District B looks out over most of the six frontiers at once. It is the most useful "
          "single piece of equipment the air arm could buy and the hardest to keep running: the road to it closes in winter "
          "and its crew must be supplied by sledge. Neighbours will notice it, and the foreign office prepares an explanation.",
          ('radar', 'security'), after=('sky_runway',), reward=(Build('radar_station', 1, 356),)),
    Focus('sky_alert_flight', 'A Flight on Standing Alert',
          "The first plan keeps four of the twelve fighters armed and crewed on the capital field day and night, ready to meet "
          "anything that crosses a frontier without permission. Pilots train for interception and little else. The alert "
          "burns fuel, airframe hours and sleep, and it makes the air arm a small but believable guard over a small country.",
          ('air', 'security'), after_any=('sky_forecasters', 'sky_north_radar'), cost=10, exclusive=('sky_liaison',),
          reward=(Idea('standing_alert'),)),
    Focus('sky_liaison', 'Liaison Flights over the Districts',
          "The second plan makes the squadron the government's fastest messenger: carrying officials, doctors and mail to "
          "District E and the mountain towns, flying weather and frontier reconnaissance and training pilots to land on rough "
          "strips. Interception skills fade. The air arm becomes useful every week instead of ready for one bad day.",
          ('air', 'communications'), after_any=('sky_forecasters', 'sky_north_radar'), cost=10, exclusive=('sky_alert_flight',),
          reward=(Idea('liaison_wings'),)),
    Focus('sky_mountain_strip', 'A Winter Strip at the Logistics Centre',
          "With the army's weight now in the mountains, the air arm lays a short strip beside the Logistics Centre, with a "
          "heated hangar for two aircraft and a snow plough of its own. It is the first airfield outside the capital. Pilots "
          "dread its crosswinds, and the formation at the Centre finally has aircraft within reach in winter.",
          ('runway', 'shelter'), after_any=('sky_alert_flight', 'sky_liaison'), requires=(HasFlag('doctrine_mountain'),),
          reward=(Build('air_base', 1, 356),)),
    Focus('sky_plain_fields', 'Dispersal Fields on the Capital Plain',
          "With the army holding the plain, the air arm spreads its aircraft across grass fields beside the railway near the "
          "capital, each with fuel, a radio and a guard. A single strike could no longer catch the whole squadron on one "
          "runway. The fields flood in the wet season and need drains, and the farmers who own them want rent.",
          ('runway', 'rail'), after_any=('sky_alert_flight', 'sky_liaison'), requires=(HasFlag('doctrine_plain'),),
          reward=(Build('air_base', 2, 0),)),
    Focus('sky_instructors', 'Instructors from the Squadron',
          "The squadron's senior pilots become instructors for a flying course that takes cadets from the capital's schools. "
          "Two trainers are bought abroad and the course runs through the dry months. Front-line flying drops while the "
          "instructors teach. In five years the air arm will have pilots it trained itself, and a reason to ask for more "
          "than twelve aircraft.",
          ('training', 'air'), after_any=('sky_alert_flight', 'sky_liaison'), reward=(XP('air', 25), TimedIdea('cadet_course', 730))),
))

FRONTIERS = Branch('six', 'Six Frontiers Through District B', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('six_map', 'Map the Six Frontiers',
          "Seterano has six land neighbours, and every one of their frontiers runs through the mountains of District B: Slavia, "
          "Valka and Malynea meet near the Logistics Centre in the west, Baltica and Yuktobania touch the north-east, and "
          "Azbekerania runs down the eastern side to the coast of District E. The foreign office maps every crossing, path and "
          "post on its own side. No line moves.",
          ('diplomacy', 'document'), reward=(Idea('frontier_ledger'), Event('six_frontiers'))),
    Focus('six_huts', 'Rescue Huts on the High Passes',
          "The passes of District B close for much of the winter, and travellers caught by blizzards depend on whoever reaches "
          "them first. Rescue huts with stoves, blankets and a radio on each Seteranoan approach, and a volunteer team at the "
          "Logistics Centre, answer calls from either side of the line. The huts cost little and must be restocked by mule "
          "every autumn.",
          ('shelter', 'peace'), after=('six_map',), reward=(Idea('pass_huts'),)),
    Focus('six_yuk_corner', 'The Province Facing Yuktobania',
          "In the far north-east of District B a single mountain province touches Yuktobania, a country many times Seterano's "
          "size, as well as Baltica and Azbekerania. An observation post there, staffed in shifts from the Logistics Centre, "
          "reports weather, aircraft and traffic and says nothing to anyone across the line. The post is lonely, and nobody "
          "volunteers twice.",
          ('security', 'telescope'), after=('six_map',), reward=(Idea('corner_post'),)),
    Focus('six_fair_passes', 'Fair Passes for Eastern Traders',
          "Since District E chose fairs over factories, traders from across the eastern frontier come in larger numbers. A "
          "seasonal pass, issued at the fair grounds for a small fee and valid only on fair days, replaces the old habit of no "
          "paperwork with a little. Regulars grumble, then buy one. The customs office finally learns how much trade crosses "
          "the hills.",
          ('document', 'economy'), after=('six_map',), requires=(HasFlag('east_fairs'),), reward=(Idea('fair_passes'),)),
    Focus('six_neutral_ground', 'Neutral Ground in the Mountains',
          "The first posture declares that Seterano will join no bloc, host no foreign troops and offer its mountains as "
          "neutral ground for talks between any neighbours who want them. A guesthouse at the Logistics Centre is set aside "
          "for the purpose. Nobody may ever use it. The declaration costs nothing but freedom of action, and that is the point "
          "of it.",
          ('peace', 'diplomacy'), after_any=('six_huts', 'six_yuk_corner'), cost=10,
          exclusive=('six_small_neighbours', 'six_counted_crossings'), reward=(Idea('neutral_mountains'),)),
    Focus('six_small_neighbours', 'Practical Talks Across the Passes',
          "The second posture offers every neighbour except Yuktobania regular practical talks on crossings, weather, "
          "avalanches and freight, with no treaty and no common army. Whether anyone comes is their decision. Seterano keeps a "
          "chair at the table and a clerk to take notes, and assumes the largest neighbour will read the minutes.",
          ('diplomacy', 'assembly'), after_any=('six_huts', 'six_yuk_corner'), cost=10,
          exclusive=('six_neutral_ground', 'six_counted_crossings'), reward=(Idea('neighbour_talks'),)),
    Focus('six_counted_crossings', 'Count Every Crossing',
          "The third posture closes every unofficial path and funnels all traffic through staffed crossings that record each "
          "traveller and each load. Smuggling falls, and so does the frontier trade of the mountain and hill towns. The army "
          "takes over the posts in winter. The country knows exactly who enters, and its neighbours learn that Seterano is "
          "watching its doors.",
          ('security', 'document'), after_any=('six_huts', 'six_yuk_corner'), cost=10,
          exclusive=('six_neutral_ground', 'six_small_neighbours'), reward=(Idea('counted_crossings'),)),
    Focus('six_western_road', 'The Road West Across the Plain',
          "The capital district's plain runs west to the Slavian frontier, where the old road narrows to a cart track at the "
          "last village. Rebuilding it as a proper highway with a staffed crossing opens the plain's markets to the west. It "
          "suits an open posture and costs a summer of roadworks in the heat. What happens on the far side is for Slavia to "
          "decide.",
          ('logistics', 'diplomacy'), after_any=('six_neutral_ground', 'six_small_neighbours'),
          reward=(Build('infrastructure', 1, 0),)),
    Focus('six_winter_posts', 'Winter Posts on Every Path',
          "Counting crossings means staffing them in January, when the paths of District B lie under snow and the posts are "
          "cut off for days. Heated posts with radios, stores and a road kept open to each one turn a summer policy into a "
          "year-round one. The army supplies the men and the railway office the snow ploughs, and both send the bill to the "
          "foreign office.",
          ('security', 'shelter'), after=('six_counted_crossings',), reward=(Build('infrastructure', 1, 356),)),
))

ULYSSES = Branch('uly', 'Ulysses over Mountain and Plain', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_notice', 'The Astronomers Notice on the Radio',
          "In December 1994 astronomers warn the world that the asteroid called Ulysses is on a course near the Earth and "
          "could collide with it. The notice reaches Seterano as a paragraph on the evening radio. Within a week every district "
          "is writing to the capital to ask what the government means to do. A plain answer costs little now, and silence "
          "will cost more later.",
          ('meteor', 'communications'), requires=(After('1994.12.10'),), reward=(Idea('sky_notice'), Event('ulysses_notice'))),
    Focus('uly_cellars', 'Count the Cellars of the Capital Plain',
          "The capital plain has soft ground and no rock to tunnel, so its shelters would be its cellars. Wardens walk every "
          "street of the Capital Centre and the plant districts, recording each cellar's size, depth and door. Owners resent "
          "the visits, and the count shows that half the city has nowhere safe to go. That figure must be known before "
          "anything is built.",
          ('shelter', 'document'), after=('uly_notice',), reward=(Flag('cellars_counted'), PP(10))),
    Focus('uly_rock_bores', 'Test Bores in the Northern Rock',
          "The mountains of District B are solid rock, and the railway's tunnel gangs already know how to cut it. Test bores "
          "near the Logistics Centre and the mountain towns show where galleries could be driven quickly and kept dry. The "
          "bores cost little and frighten some villagers, who assume the government knows something it is not telling them.",
          ('tools', 'shelter'), after=('uly_notice',), reward=(Research('excavation_tech', 0.5, 1), Flag('rock_bored'))),
    Focus('uly_impact_declared', 'When the Impact Is Declared',
          "In April 1996 the Federation of Central Usea announces to the world that Ulysses will strike the Earth and sets out "
          "its plans to counter it. Nobody can say where the fragments will fall. In Seterano the question stops being whether "
          "to prepare and becomes how, and with what, and the two climates and two kinds of ground still point to different "
          "answers.",
          ('meteor', 'security'), after_any=('uly_cellars', 'uly_rock_bores'), requires=(After('1996.4.20'),),
          reward=(TimedIdea('impact_alarm', 365),)),
    Focus('uly_galleries', 'Galleries Under the Northern Rock',
          "The first plan drives shelter galleries into the rock of District B and moves the country's reserves of grain, fuel "
          "and records into them, with trains ready to carry families north from the plain. The mountains become the "
          "country's refuge. It is the stronger shelter and the longer journey, and families on the plain wonder whether the "
          "trains would really come.",
          ('shelter', 'tools'), after=('uly_impact_declared',), cost=10, requires=(HasFlag('rock_bored'),),
          exclusive=('uly_plain_cellars',), reward=(Idea('rock_refuge'), Flag('shelters_ready'))),
    Focus('uly_plain_cellars', 'Strengthened Cellars Across the Plain',
          "The second plan shelters people where they live: cellars across the Capital District, District A and District D "
          "are deepened, propped and stocked, with public shelters dug where the count found none. Nobody has to travel. The "
          "shelters are weaker than rock and the soft ground floods in the wet season, so pumps and drains are written into "
          "every contract.",
          ('shelter', 'civil'), after=('uly_impact_declared',), cost=10, requires=(HasFlag('cellars_counted'),),
          exclusive=('uly_galleries',), reward=(Idea('cellar_shelters'), Flag('shelters_ready'))),
    Focus('uly_stores', 'Stores for a Hungry Year',
          "Whatever shelters the country chooses, it needs food, fuel and medicine for a year in which harvests and imports "
          "might fail. Warehouses at both Centres and at the southern port are filled slowly from the market to avoid raising "
          "prices. The stocks tie up money and spoil if forgotten, and they are the difference between a hard year and a "
          "famine.",
          ('logistics', 'shelter'), after_any=('uly_galleries', 'uly_plain_cellars'), reward=(Idea('dark_year_stores'),)),
    Focus('uly_roche', 'A Night Inside the Roche Limit',
          "In July 1999 Ulysses passes within the distance at which the Earth's pull breaks it apart. Seterano holds its trains, "
          "opens its shelters and keeps its wardens on the streets through a long summer night. Nobody knows where the "
          "fragments will come down. Five years of preparation are tested by a single night of waiting by the radio.",
          ('meteor', 'shelter'), after=('uly_stores',), requires=(After('1999.7.8'), HasFlag('shelters_ready')),
          reward=(Event('roche_night'), RemoveIdea('sky_notice'))),
))

FUEL = Branch('fuel', 'One Silo at the Capital', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('fuel_news', 'War in Belka, Prices at Home',
          "In March 1995 war breaks out around Belka, far from Seterano and with no Seteranoan part in it. The war arrives "
          "anyway through the price of crude and the insurance on every merchant hull. The fuel office reports what the single "
          "silo at the capital holds. The cabinet must decide what to tell the country before the prices tell it first.",
          ('communications', 'security'), requires=(After('1995.3.25'),), reward=(Idea('dear_crude'), Event('distant_war'))),
    Focus('fuel_gauge', 'Gauge the Silo and the Wells',
          "The country pumps a little crude in three districts and stores refined fuel in one silo at the capital. Inspectors "
          "measure what each field gives, how much of it can be refined at home and what the plants, trains, lorries and twelve "
          "fighters actually burn. The figures fall short of comfortable. They are also the first honest fuel accounts the "
          "country has kept.",
          ('document', 'tools'), after=('fuel_news',), reward=(TimedIdea('fuel_rules', 365), Research('synth_resources', 0.5, 1))),
    Focus('fuel_hulls_insured', 'Insurance for the Merchant Hulls',
          "Foreign insurers raise premiums on every hull near the open sea lanes, and some small owners at the southern port "
          "cannot pay. A state insurance pool, funded by a small levy on each voyage, covers the masters who would otherwise "
          "lie idle. The levy annoys the large firms. The small ones keep sailing, and the port keeps its crews.",
          ('navy', 'economy'), after=('fuel_news',), reward=(TimedIdea('insurance_pool', 730),)),
    Focus('fuel_full_silo', 'Keep the Silo Full',
          "The first answer buys crude whenever the price allows and never lets the capital silo fall below a set mark, "
          "whatever the plants and trains want. Rationing starts early and lasts longer than the war. The service can always "
          "fly and move. The plants lose shifts to fuel limits, and businesses blame the government for every empty pump.",
          ('security', 'logistics'), after=('fuel_gauge',), cost=10, exclusive=('fuel_sell_crude',),
          reward=(SwapIdea('dear_crude', 'full_silo'),)),
    Focus('fuel_sell_crude', 'Sell the Home Crude Abroad',
          "The second answer sells the country's own crude abroad while prices are high and buys back refined fuel later. The "
          "treasury earns money it badly needs. The silo runs closer to empty than the general staff likes, and if prices stay "
          "high the country will be buying back at a loss what it sold at a profit.",
          ('economy', 'diplomacy'), after=('fuel_gauge',), cost=10, exclusive=('fuel_full_silo',),
          reward=(SwapIdea('dear_crude', 'crude_sold'),)),
    Focus('fuel_lumen_treaty', 'When the Treaty Is Signed in Lumen',
          "In June 1995 a treaty signed in Lumen ends the Belkan War. Crude prices begin to fall and insurers relax their "
          "rates on the merchant lanes. The fuel office recommends keeping the new rules for a year in case the peace does not "
          "hold, while the plants and the port want them gone by autumn. The cabinet picks a date between the two.",
          ('peace', 'document'), after_any=('fuel_full_silo', 'fuel_sell_crude'), requires=(After('1995.6.20'),),
          reward=(Idea('steady_fuel'), Stability(0.02))),
))

CENTURY = Branch('cent', 'The Federation at the Millennium', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_account', 'A Plain Account of Ten Years',
          "The statistics office prepares a plain account of the country since 1991: the five districts, the ten plants and any "
          "new ones, the spine, the airfield, the port and the three formations, with what each change cost. It carries no "
          "foreword from the government. Every faction will find something to quote, and the government will have to answer.",
          ('document', 'assembly'), requires=(After('2001.1.1'),), reward=(Event('decade_account'), PP(20))),
    Focus('cent_council_term', 'The Council Faces the Voters Again',
          "The federal council goes back to the voters, and this time the district lists are longer and the campaigns louder. "
          "A council that survives a second election is no longer an experiment. The movement fields candidates everywhere, "
          "and the council must choose whether to campaign on its record in District E or on the calm of the frontiers.",
          ('ballot', 'assembly'), after=('cent_account',), requires=(HasFlag('order_ballot'),),
          exclusive=('cent_prefect_audit', 'cent_terms_read'), reward=(Idea('second_mandate'),)),
    Focus('cent_prefect_audit', 'The Prefects Invite an Audit',
          "After a decade of numbered orders, the board of prefects invites outside auditors into every district office. The "
          "auditors find careful books, slow decisions and a growing number of citizens who ask why they still cannot vote. "
          "The board prints the findings in full, because publishing is the only legitimacy it has ever claimed.",
          ('scales', 'document'), after=('cent_account',), requires=(HasFlag('order_prefects'),),
          exclusive=('cent_council_term', 'cent_terms_read'), reward=(Idea('audited_prefects'),)),
    Focus('cent_terms_read', 'The Terms Read Aloud Again',
          "The written terms on which the movement took power are read aloud before the districts again, clause by clause. "
          "The committee claims to have kept every one; its critics quietly list the exceptions. Reaffirming the terms costs "
          "the committee freedom it would like to have and buys it more years of grudging consent from the half of the "
          "country that never joined.",
          ('security', 'scales'), after=('cent_account',), requires=(HasFlag('order_movement'),),
          exclusive=('cent_council_term', 'cent_prefect_audit'), reward=(Idea('terms_reaffirmed'),)),
    Focus('cent_second_works', 'A Second Works in District E',
          "The plants beside the eastern track have filled their crews and their order books. A second civilian works on the "
          "remaining free ground gives District E a real industrial town, with housing, a school and a bus to the capital. "
          "Herders who still use the hills watch the town spread toward their pastures and ask the district for limits.",
          ('industry', 'rebuild'), after=('cent_account',), requires=(HasFlag('east_industry'),),
          reward=(Build('industrial_complex', 1, 470),)),
    Focus('cent_fair_town', 'The Fair Ground Becomes a Town',
          "A decade of fairs has turned the market ground on the eastern hills into a town in all but name, with a clinic, a "
          "school and a bank branch. Paving its streets and the lanes to the shore finishes what the fairs began. The district "
          "remains poorer than the capital, but it is no longer the forgotten corner of the country.",
          ('civil', 'economy'), after=('cent_account',), requires=(HasFlag('east_fairs'),),
          reward=(Build('infrastructure', 1, 470),)),
    Focus('cent_signals', 'Electric Signals for the Spine',
          "The spine still runs on signals set by hand from lever frames, and every winter some signalman on the northern grade "
          "is cut off by snow. Electric signalling worked from the Capital Centre lets fewer staff run more trains in all "
          "weather. It is a slow and expensive conversion, done section by section, starting where the snow is worst.",
          ('rail', 'communications'), after=('cent_account',), requires=(After('2002.1.1'),),
          reward=(Research('train_tech', 0.5, 1), Idea('electric_signals'))),
    Focus('cent_isaf_freight', 'Freight Rates in the Usean War',
          "In August 2003 the ISAF is established against Erusea, and war returns to the world's sea lanes far from Seterano. "
          "Freight and insurance rates climb again. The port firms remember 1995 and reroute and insure their hulls within "
          "weeks this time. The country takes no part in the war and still pays for it at every quay.",
          ('logistics', 'economy'), after=('cent_account',),
          requires=(HasGlobal('ac_ucw_isaf_formed'), After('2003.8.22')), reward=(Idea('war_freight'),)),
    Focus('cent_close_programme', 'The Programme Closed in 2005',
          "In September 2005 the Erusean capital falls and the Continental War ends. Shipping lanes calm, freight rates ease "
          "and the port sails on peacetime terms again. The government uses the moment to close the national programme it "
          "began in 1991 and publish what remains undone, district by district. The list is long, and shorter than it was.",
          ('document', 'peace'), after_any=('cent_signals', 'cent_isaf_freight'), requires=(After('2005.9.19'),),
          reward=(Stability(0.03), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (FEDERATION, SPINE, EAST, WORKS, PORT, GUARD, SKY, FRONTIERS, ULYSSES, FUEL, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('clear_grade', 'Plough Out the Northern Grade',
                'Sends plough trains and shovel gangs up the mountain line after a blizzard so the Logistics Centre is supplied. '
                'Repeatable twice a year; freight elsewhere waits while they work.',
                25, (TimedIdea('grade_open', 90),), requires=(Completed('spine_snow_sheds'),), cooldown=180),
    DecisionDef('autumn_fair', 'Proclaim an Autumn Fair in the East',
                'Declares a week of fairs on the eastern hills with free stalls and a band from the capital. Repeatable once a '
                'year.',
                20, (Stability(0.02), PP(15)), requires=(Completed('east_markets'),), cooldown=365),
    DecisionDef('coast_round', 'Send the Escort on Its Rounds',
                'Sends the coastal escort to call at every harbour on the three coasts for a season. Repeatable once a year; '
                'the fuel bill is the service budget.',
                30, (XP('navy', 10), TimedIdea('escort_rounds', 90)), requires=(Completed('port_muster'),), cooldown=365),
    DecisionDef('shelter_week', 'Open the Shelters for a Drill Week',
                'Invites every family to walk to its assigned shelter and spend a night there. Repeatable once a year; the '
                'plants lose shifts.',
                30, (TimedIdea('drill_week', 60),), requires=(HasFlag('shelters_ready'),), cooldown=365),
    DecisionDef('east_strip', 'Mark a Grass Strip in District E',
                'Rolls and marks a grass landing strip beside the graded track for liaison aircraft and medical flights. Done '
                'once; the crews then return to the road.',
                50, (Build('air_base', 1, 470),), requires=(Completed('east_graded_track'),)),
    DecisionDef('corner_mast', 'Raise a Mast at the North-East Post',
                'Adds a radar mast to the observation post in the province facing Yuktobania. Paid for once from the frontier '
                'budget; its crew rotates with the post.',
                60, (Build('radar_station', 1, 356),), requires=(Completed('six_yuk_corner'),)),
)
