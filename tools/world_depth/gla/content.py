"""Glaceland (GLA): bespoke national focus tree, 1991 to 2005 (era e1).

Source layers. Mod provenance: the inherited history file (a democratic-labelled
National Administration with elections suspended, popularity split between
neutrality and fascism), the starting office card, the world-foundation force and
industry calibration, the provisional district labels and the 1991 state layout.
Official: five ACES Chronicle rows used only as anchors for world pressure (the
Ulysses warnings, Roche-limit passage and break-up, and the formation of the ISAF). Everything
else, including every Glacelandic choice, office, idea, building and event, is
provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='GLA', name='Glaceland', root='world', package='gla',
                  themes=('navy', 'assembly', 'logistics'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Glaceland state: ruling_party democratic with elections_allowed = no; popularities neutrality 48, '
           'fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots; tech_mountaineers; '
           'grand doctrines superior_firepower, fleet_in_being and operational_integrity; starting office '
           'GLA_ac_government_office (National Administration), whose 1991 holder is not established. The tree reads these '
           'as political pressures and never edits them.',
           'mod/2985041246/history/countries/GLA - Glaceland.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'tools/world_foundation/country_registry.json (GLA row: civil_administration, capacity 40)'),
    Source('Mod provenance',
           'World-foundation calibration, itself labelled provisional gameplay: 12 civilian plants, 6 arms works and 4 '
           'dockyards; 8 infantry formations; 72 fighters and 12 ground-attack aircraft on 2 airfields; 5 escorts and 2 '
           'submarines; 108 convoys; 4 supply centres; role dispersed coastal support; starting research priority Physical '
           'Sustainment. Fiscal profile GDP 200, debt ratio 0.3, collection 0.85, growth 3, inflation 2 is fictional '
           'gameplay calibration, not national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/economy_v2/profiles.json; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 9, 26, 35, 41, 50 (capital), 52, 87, 129, 172 and 576, labelled District A, B, C, D, '
           'Capital District, F, G, H, I and J. All industry sits in 50, 26, 87 and 172, the dockyards in 9; states 35, 41, '
           '52, 129 and 576 have no infrastructure or industry. State 35 is detached from the mainland and province 9991 '
           '(state 129) is an outlying naval post. Land neighbours SFA (via 9 and 52), LUR (52, 576) and KLG (576), computed '
           'from map/provinces.bmp. Terrain counts from map/definition.csv. No new place names.',
           'mod/2985041246/history/states; mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; tools/world_capitals/placements.json'),
    Source('Official',
           'Date anchor only: the International Astronomical Union announces that Ulysses may strike the Earth. No '
           'Glacelandic role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor only: the impact of Ulysses is announced worldwide. Glacelandic preparations are gameplay.',
           '1996 / 04.20'),
    Source('Official',
           'Date anchor only: Ulysses passes through the Roche limit. What falls near Glaceland is not claimed.',
           '1999 / 07.08'),
    Source('Official',
           'Ulysses broke into fragments as it passed into the atmosphere; used only to say the asteroid broke apart. No '
           'Stonehenge content and no impact site is used.', 'Super Weapons, Stonehenge'),
    Source('Official',
           'Date anchor only: the ISAF is established against Erusea. The focus that reacts to it waits for the mod flag '
           'ac_ucw_isaf_formed and claims no Glacelandic part in the war.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Glacelandic focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the suspended ballot
    IdeaDef('provisional_mandate', 'The Provisional Mandate',
            'The National Administration governs under a democratic name while the ballot stays suspended.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('document', 'ballot')),
    IdeaDef('ballot_pledge', 'The Ballot Pledge', 'A dated, public promise that the vote will return.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('board_mandate', 'Government Without Parties', 'Examined officials run the state against published targets.',
            {'political_power_gain': 0.15, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('petition_mandate', 'The Petition Mandate', 'The nationalist movement has been promised the seals.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.10, 'stability_factor': -0.02}, ('medal', 'assembly')),
    IdeaDef('open_chamber', 'An Answerable Chamber', 'Ministers answer to the chamber and a court checks them both.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'scales')),
    IdeaDef('merit_service', 'The Examined Service', 'Every post filled by open written examination.',
            {'political_power_factor': 0.08, 'production_factory_efficiency_gain_factor': 0.03}, ('document', 'training')),
    IdeaDef('directorate_order', 'Order of the Directorate', 'The national programme is read aloud in every workplace.',
            {'war_support_factor': 0.08, 'stability_factor': 0.04, 'consumer_goods_factor': 0.04}, ('security', 'medal')),
    IdeaDef('civic_returns', 'Returns on the Shelf', 'What every district said is in every public library.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('document', 'civil')),
    # the empty districts
    IdeaDef('district_survey', 'The District Survey', 'Every road, track and jetty in the empty districts is costed.',
            {'production_speed_infrastructure_factor': 0.10}, ('document', 'logistics')),
    IdeaDef('district_quotas', 'A Plant in Every District', 'Protected credit for one modern plant per district.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': 0.02}, ('industry', 'civil')),
    IdeaDef('core_corridor', 'The Core Corridor', 'Credit flows to the capital and Districts B, G and I.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': -0.02}, ('rail', 'industry')),
    IdeaDef('night_shifts', 'Second and Third Shifts', 'The core plants run around the clock.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'economy')),
    # oil, steel and the treasury
    IdeaDef('collection_drive', 'The Collection Drive', 'Auditors chase the fifteen in every hundred the treasury misses.',
            {'political_power_factor': 0.05}, ('scales', 'economy')),
    IdeaDef('fuel_export', 'Crude for Export', 'Most crude is sold abroad under long contracts.',
            {'consumer_goods_factor': -0.05, 'production_speed_buildings_factor': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('home_refining', 'Refined at Home', 'Crude stays in the country and fuels the core plants.',
            {'industrial_capacity_factory': 0.05, 'production_factory_max_efficiency_factor': 0.03}, ('industry', 'tools')),
    IdeaDef('mill_retooling', 'Retooling the Mills', 'District B mills are down for new stands and furnaces.',
            {'production_factory_max_efficiency_factor': 0.04, 'production_speed_buildings_factor': -0.05}, ('tools', 'industry')),
    IdeaDef('light_metal', 'Light Metal Contracts', 'Smelted aluminium goes first to airframe and vehicle work.',
            {'production_speed_arms_factory_factor': 0.08, 'experience_gain_air_factor': 0.03}, ('air', 'industry')),
    IdeaDef('arms_order_book', 'One Order Book', 'Six arms works scheduled as one producer.',
            {'production_factory_efficiency_gain_factor': 0.05, 'production_speed_arms_factory_factor': 0.05}, ('missile', 'document')),
    IdeaDef('strategic_stock', 'The Strategic Stock', 'A second fuel reserve dug into the hills.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.02}, ('security', 'economy')),
    IdeaDef('export_fund', 'The Stabilisation Fund', 'Export revenue saved in good years and spent in bad ones.',
            {'stability_factor': 0.05, 'consumer_goods_factor': -0.05, 'production_speed_buildings_factor': 0.05}, ('economy', 'scales')),
    IdeaDef('chemical_lines', 'Chemical Lines', 'Refinery by-products become plastics and fertiliser.',
            {'industrial_capacity_factory': 0.08, 'production_factory_max_efficiency_factor': 0.05}, ('industry', 'science')),
    IdeaDef('fuel_drawdown', 'Drawing the Reserve', 'Fuel released from the strategic stock for a season.',
            {'supply_consumption_factor': -0.08, 'army_org_factor': 0.03}, ('logistics', 'security')),
    # the coast
    IdeaDef('coast_register', 'The Coast Register', 'Every hull, crew and berth on one register.',
            {'naval_coordination': 0.03}, ('navy', 'document')),
    IdeaDef('escort_command', 'Convoy Escort Command', 'Escort groups organised around the merchant lanes.',
            {'navy_org_factor': 0.06, 'naval_speed_factor': 0.04}, ('navy', 'logistics')),
    IdeaDef('sub_patrol', 'Coastal Submarine Patrol', 'Quiet boats on the mountain coasts.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.04}, ('submarine', 'navy')),
    IdeaDef('coast_guard', 'Fishery and Customs Guard', 'Cutters, boarding teams and rescue crews on every coast.',
            {'stability_factor': 0.03, 'naval_coordination': 0.04}, ('fishing', 'security')),
    IdeaDef('fleet_renewal', 'Fleet Renewal Credit', 'Old coasters scrapped and replaced from the District A yards.',
            {'naval_speed_factor': 0.05, 'industrial_capacity_dockyard': 0.05}, ('logistics', 'navy')),
    # District C
    IdeaDef('c_charter', 'The District C Charter', 'District C runs its own local affairs within Glaceland.',
            {'stability_factor': 0.05, 'political_power_gain': -0.05}, ('document', 'navy')),
    IdeaDef('c_commissioner', 'The Resident Commissioner', 'One official signs for every ministry in District C.',
            {'political_power_gain': 0.05, 'production_speed_buildings_factor': 0.05}, ('command', 'navy')),
    IdeaDef('ferry_subsidy', 'Ferry Fare Subsidy', 'The treasury pays part of every District C ferry ticket.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('navy', 'civil')),
    # the army
    IdeaDef('district_battalions', 'District Battalions', 'Each district raises a battalion of local reservists.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.05}, ('security', 'training')),
    IdeaDef('mountain_corps', 'The Mountain Corps', 'One mobile corps of long-service mountain infantry.',
            {'army_attack_factor': 0.04, 'experience_gain_army_factor': 0.08, 'attrition': -0.05}, ('training', 'medal')),
    IdeaDef('forward_stores', 'Forward Stores', 'War stocks held toward each land frontier.',
            {'supply_consumption_factor': -0.05, 'army_core_defence_factor': 0.03}, ('logistics', 'rail')),
    IdeaDef('muster_season', 'Muster Weekends', 'District battalions train in their own valleys every month.',
            {'training_time_army_factor': -0.08, 'army_org_factor': 0.03}, ('training', 'civil')),
    IdeaDef('volunteer_companies', 'Volunteer Companies', 'Movement volunteers attached to the regular formations.',
            {'army_core_defence_factor': 0.05, 'stability_factor': -0.02}, ('medal', 'security')),
    # the air arm
    IdeaDef('two_fields', 'Two Fields, One Air Arm', 'Every aircraft in the country flies from two airfields.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('dispersed_wings', 'Dispersed Wings', 'Squadrons scattered to forest strips in the mountain districts.',
            {'air_superiority_efficiency': 0.05, 'air_detection': 0.05}, ('air', 'logistics')),
    IdeaDef('hardened_fields', 'Hardened Fields', 'Concrete shelters and buried fuel at the two fields.',
            {'air_defence_factor': 0.08, 'experience_gain_air_factor': 0.05}, ('shelter', 'runway')),
    IdeaDef('air_watch', 'The Air Watch Service', 'Civilian observers report aircraft from every district.',
            {'air_detection': 0.10, 'static_anti_air_damage_factor': 0.05}, ('telescope', 'security')),
    IdeaDef('joint_exercises', 'Joint Exercises', 'Ground-attack crews and infantry observers train together.',
            {'air_mission_efficiency': 0.05, 'experience_gain_army_factor': 0.03}, ('missile', 'air')),
    IdeaDef('home_overhaul', 'Overhaul at Home', 'Major aircraft overhauls done in the arms works.',
            {'experience_gain_air_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.02}, ('tools', 'air')),
    # Ulysses
    IdeaDef('sky_watch', 'The Sky Watch Committee', 'Astronomers, engineers and district officials watch Ulysses.',
            {'research_speed_factor': 0.02, 'stability_factor': -0.02}, ('telescope', 'meteor')),
    IdeaDef('reserve_stores', 'A Year in Store', 'A year of fuel, grain and medicine spread across ten depots.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.03}, ('security', 'economy')),
    IdeaDef('inland_refuges', 'Inland Refuges', 'Camps, water and roads ready in the interior districts.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.10}, ('refugees', 'shelter')),
    # the land frontiers
    IdeaDef('border_desks', 'Border Desks', 'One foreign ministry desk for each land neighbour.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('diplomacy', 'document')),
    IdeaDef('open_frontiers', 'Open Frontiers', 'Low tariffs and fast crossings on all three land frontiers.',
            {'consumer_goods_factor': -0.05, 'production_speed_infrastructure_factor': 0.08}, ('economy', 'diplomacy')),
    IdeaDef('licensed_frontiers', 'Licensed Frontiers', 'Trade under quota, inspection and licence.',
            {'political_power_gain': 0.10, 'army_core_defence_factor': 0.04}, ('security', 'scales')),
    # the new century
    IdeaDef('applied_institutes', 'The Applied Institutes', 'Engineering and electronics institutes in the capital.',
            {'research_speed_factor': 0.05}, ('science', 'telescope')),
    IdeaDef('renewed_mandate', 'The Answered Ledger', 'The government has answered the decade ledger in public.',
            {'political_power_gain': 0.10, 'stability_factor': 0.03}, ('scales', 'document')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('elected_council', 'Elected Council of Ministers',
           'A council of ministers drawn from a newly elected chamber, governing collectively and answerable to that chamber '
           'for every budget. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('admin_board', 'Standing Administrative Board',
           'A standing board of examined senior officials with fixed terms and published targets, governing without parties '
           'while the ballot stays suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('national_directorate', 'National Directorate',
           'A directorate formed by the leadership council of the nationalist movement, ruling by decree with rival parties '
           'suspended. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('suspended_ballot', 'The Suspended Ballot', (
        "The National Administration that governs Glaceland in 1991 carries a democratic name and a suspended election "
        "calendar. Its officials run ten districts, eighteen plants, a small navy and a smaller air arm, and they do it "
        "competently enough that few people ask who appointed them. When the question is finally asked aloud, in the "
        "capital's press and in district halls from A to J, nobody in the Administration has a ready answer.",
        "The pollsters' figures make the problem sharper. Barely one citizen in a hundred supports the party whose name the "
        "government carries. Close to half want the country run by non-party administrators, as it effectively already is. "
        "The other half answers to a nationalist movement that promises discipline, a stronger coast and an end to "
        "government by clerks. Democrats and communists together could fill a meeting hall, not a chamber.",
        "The Administration must decide how the question will be argued before it can decide how it will be answered. "
        "District hearings would take a season and invite every grievance in the country into the record. A decision "
        "inside the Administration would be faster and quieter, and would confirm everything its critics say about it. "
        "Both choices will be remembered when the seals change hands.",
    ), (
        Option('Hold hearings in every district.', (Stability(0.02), Event('district_returns', 30))),
        Option('Settle it inside the Administration.', (PP(30), Stability(-0.02))),
    ), layer='Mod provenance',
        citation='history/countries/GLA - Glaceland.txt set_politics and set_popularities; the hearings and every response '
                 'are provisional gameplay', picture=1),
    EventDef('district_returns', 'Returns from the Districts', (
        "The hearing clerks return from the ten districts with crates of transcripts. The core districts, the capital and "
        "Districts B, G and I, talk about wages, rents and the plants. The empty districts talk about roads they have never had, clinics "
        "a day's travel away and young people who leave for the core and do not come back. District C, across the water, "
        "talks mostly about the ferries.",
        "On the constitutional question the returns are as divided as the polls. Officials and managers want a board that "
        "keeps things running. Farmers and plant workers split between the nationalist petition and a scattering of voices "
        "who want a real vote. Almost every district asks first to be consulted again, and many hearings closed with a vote "
        "of thanks to the clerks for coming at all.",
        "The Administration now holds the returns and must decide what to do with them. Publishing every transcript would "
        "show the country to itself, flaws included, and hand the opposition a library of quotations. A summary would be "
        "tidier and safer. Officials who sat through the hearings warn privately that a summary will be read as the "
        "Administration editing the districts out of their own record.",
    ), (
        Option('Publish every return.', (Flag('returns_published'), Stability(0.02))),
        Option('Publish an approved summary.', (PP(25), Stability(-0.01))),
    ), picture=1),
    EventDef('empty_districts', 'Half a Country Without Roads', (
        "The survey teams come back from Districts C, D, F, H and J with photographs that surprise even the ministers who "
        "sent them. Half of Glaceland has no paved road network and no factory of any kind. Villages are joined by farm "
        "tracks, forest roads and boats. The frontier districts facing Sfaenland, Luremia and Kaluga could not move a "
        "convoy to their own border posts in a wet week.",
        "The other half of the country is a different place. The capital and Districts B, G and I hold all twelve civilian "
        "plants and all six arms works, the logistics centres and nearly all the oil, steel and aluminium. District A holds "
        "the four dockyards. The core is busy, crowded and increasingly expensive to live in, and every year it draws the "
        "young out of the empty districts.",
        "The survey's authors refuse to recommend a solution. They price roads, plants, schools and clinics for each empty "
        "district and leave the choice to the government: spread industry outward at a higher cost, or concentrate it where "
        "it already works and connect the rest by road. The empty districts are watching to see whether the survey becomes "
        "a programme or a report on a shelf.",
    ), (
        Option('Roads first, everywhere.', (Research('construction_tech', 0.5, 1),)),
        Option('Start with the frontier districts.', (XP('army', 10), Stability(0.01))),
    ), picture=2),
    EventDef('collection_gap', 'The Collection Gap', (
        "The treasury's auditors present a short report with a long appendix. Glaceland collects roughly eighty-five of "
        "every hundred owed in tax. Public debt stands near a third of national output. Growth is steady at around three "
        "percent and inflation is low, so nothing is on fire. But the gap compounds every year, and the debt grows a little "
        "faster than the economy that must carry it.",
        "The missing fifteen are not hidden in one place. Some is evaded by firms in the core, some is never assessed in the "
        "empty districts where the nearest tax office is a day's travel away, and some is simply lost between ministries "
        "that keep separate accounts. The oil districts pay royalties under formulas older than most of the wells. Nobody "
        "has ever audited all of it at once.",
        "The auditors want powers to inspect firms, district offices and ministries alike. The ministries object to being "
        "audited by the treasury, and the firms object to everything. The government must decide whether to publish the "
        "report or keep it for internal use, knowing that publication makes every later tax measure easier to defend and "
        "every later scandal harder to bury.",
    ), (
        Option('Publish the auditors report.', (Stability(0.02), PP(-15))),
        Option('Keep it for the cabinet.', (PP(30), Stability(-0.01))),
    ), picture=1),
    EventDef('long_coast', 'A Long Coast and Five Escorts', (
        "The naval register is finished, and it fits on two pages. Glaceland has five escorts, two coastal submarines and a "
        "merchant fleet of about a hundred and eight hulls, many of them older than their crews. The main naval base and all "
        "four dockyards stand in District A, beside the Sfaenland frontier. District C's small post and the jetty on "
        "District H's islet complete the list.",
        "Against that list stands the coast itself. Seven of the ten districts touch the sea, and the coastline is several "
        "times longer than all three land frontiers together. The merchant fleet carries most of the country's trade and "
        "every passenger to District C. Fishermen, smugglers and the occasional foreign survey ship use the same waters, "
        "and most of the time nobody official sees any of them.",
        "The admirals agree on the problem and on nothing else. Some want the escorts organised around the convoys, some "
        "want submarines hidden along the mountain coasts, and some want a guard service for what actually happens at sea "
        "every day. The government is asked first for a simpler decision: whether the navy's weakness is admitted in public "
        "or kept as a matter for the defence staff.",
    ), (
        Option('Admit it and ask for support.', (WarSupport(0.03), PP(-15))),
        Option('Keep it inside the defence staff.', (PP(20),)),
        Option('Send the escorts on a coastal tour.', (XP('navy', 15), Stability(0.01))),
    ), picture=0),
    EventDef('across_water', 'Across the Water', (
        "District C lies across the water from the rest of Glaceland: twenty-two provinces of plains and low hills, with a "
        "small naval post and a harbour town. It has no paved roads and no plants. Its farmers grow food the mainland "
        "imports, its fishermen work the surrounding waters, and every ton of anything moves by ship. When storms close the "
        "crossing, the district lives on whatever is in its warehouses.",
        "The islanders' complaints are practical and old. Ferry fares are high and timetables unreliable. Mainland officials "
        "arrive for a week and leave before learning the names of the villages. Doctors are scarce, spare parts take weeks, "
        "and young people who cross to study in the capital rarely return. Yet the district is loyal in its own stubborn "
        "way, and asks mainly to be remembered.",
        "The government must decide how District C is to be governed within Glaceland. A charter would let the islanders run "
        "their own local affairs, at the price of a partner the capital cannot simply instruct. A resident commissioner would "
        "get things built faster, at the price of goodwill. Nothing about the district's place in the country is in "
        "question; only the manner of its government is.",
    ), (
        Option('Cut the ferry fares this season.', (Stability(0.02), PP(-10))),
        Option('Send an inspection mission first.', (PP(15),)),
    ), picture=2),
    EventDef('hill_country', 'Hill Country and Eight Formations', (
        "The army's staff map is pinned to a public wall of the defence ministry for the first time. It shows eight infantry "
        "formations spread across a country that is mostly forest, hill and mountain, with marsh along some coasts and dry "
        "plains around the capital. It shows three land frontiers, one of them longer than the other two combined, and a "
        "district across the water that no formation can reach on foot.",
        "The inventories are honest too: nearly two thousand sets of infantry equipment, about a thousand motor vehicles, a "
        "few hundred sets of support equipment and a modest stock of trains. Some of the infantry already trains as "
        "mountaineers. Doctrine prefers firepower, because the country will never have numbers. The staff says plainly that "
        "it can hold some valleys well and most of the country not at all.",
        "Two schools are forming inside the officer corps. One wants a battalion in every district, raised from local "
        "reservists. The other wants a single professional mountain corps that moves to the threat. Before either wins, the "
        "government must decide whether the staff map stays on the public wall or goes back into a safe, knowing that the "
        "neighbours' attaches read the newspapers too.",
    ), (
        Option('Leave the map on the wall.', (Stability(0.01), WarSupport(0.03))),
        Option('Return it to the safe.', (PP(20), XP('army', 10))),
    ), picture=1),
    EventDef('two_fields_report', 'Every Aircraft on Two Fields', (
        "The air staff's report opens with a sentence the ministers will remember: every aircraft Glaceland owns stands on "
        "one of two airfields. Seventy-two fighters and twelve ground-attack aircraft are divided between the field beside "
        "the capital and the field in District B. Both are known to every map-maker in the region. A single well-planned "
        "strike on a clear morning could end the air arm before it flew.",
        "The report is equally blunt about everything else. Radar coverage barely reaches beyond the two fields. Pilots fly "
        "too few hours because fuel is rationed by budget rather than by supply, even though the country pumps its own oil. "
        "Major overhauls are done abroad and take months. The air arm is proud and capable in small numbers, and it knows "
        "exactly how small those numbers are.",
        "The staff offers two remedies that cannot both be afforded. The country could scatter its squadrons across forest "
        "strips in the mountain districts, or bury them in concrete at the two fields it already has. The ministers must "
        "first decide something easier: whether the air staff may speak publicly about the risk, or whether the report stays "
        "among the people who already lose sleep over it.",
    ), (
        Option('Let the air staff brief the press.', (WarSupport(0.03), Stability(-0.01))),
        Option('Keep the report classified.', (PP(20),)),
    ), picture=0),
    EventDef('ulysses_warning', 'Ulysses Will Strike', (
        "In April 1996 the world is told that the asteroid Ulysses will strike the Earth and that nations should prepare. "
        "Since the astronomers' announcement of December 1994, Glaceland's committee of astronomers and engineers has "
        "watched quietly; now its reports lead every bulletin. Nobody can say where fragments will fall. Glaceland, like "
        "every country, must prepare for a danger whose place and scale remain a guess.",
        "The committee divides into two camps. One wants reserves: a year of fuel, grain and medicine in depots across all "
        "ten districts, so that whatever falls, the country can feed and fuel itself. The other wants refuges: most districts "
        "and most plants lie on the coast, while Districts D and F and the capital lie inland, and moving people is cheaper "
        "than storing a year of food.",
        "Public mood swings between calm and fright. Shops in the capital run short of bottled water and candles, and "
        "coastal families ask relatives inland whether they have a spare room. The treasury warns that either programme "
        "costs as much as the defence budget. Before choosing, the government must decide how to speak about a danger it "
        "cannot control: plainly and often, or calmly and rarely.",
    ), (
        Option('Speak plainly and often.', (WarSupport(0.02), Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Speak calmly and rarely.', (Stability(0.03),)),
    ), citation='date anchors only, Official Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; '
                'the Glacelandic response is gameplay', picture=2),
    EventDef('roche_limit', 'Ulysses Breaks Apart', (
        "In July 1999 Ulysses passes through the Earth's Roche limit and begins to break apart. The committee in the capital "
        "sits through the night beside its radios and telephones, and district officials stand by in every hall from A to J. "
        "Whatever Glaceland prepared over the past three years, reserves or refuges, is now tested against something that "
        "does not negotiate.",
        "The first hours are filled with rumours that travel faster than the official bulletins. Coastal towns report lights "
        "in the sky that may be fragments or may be aircraft. Telephone exchanges jam. Some families leave for the interior "
        "without waiting for any order, while others refuse to leave at all. The ferries to District C are held in harbour, "
        "and the district follows the night by radio like everyone else.",
        "By dawn the government must decide how to manage the days that follow. It can keep the emergency apparatus fully "
        "mobilised until the danger is certainly past, at a heavy cost in lost work, or stand most of it down as soon as the "
        "reports allow and accept the risk of being wrong. Either way, the country will remember how its government behaved "
        "on this night.",
    ), (
        Option('Keep everything mobilised.', (WarSupport(0.03), Stability(-0.02))),
        Option('Stand down as the reports allow.', (Stability(0.03), PP(-15))),
    ), citation='date anchor only, Official Chronicle row 1999 / 07.08, with the break-up from Super Weapons, Stonehenge, '
                'in tools/lore/chronicle.json; what falls near Glaceland is not claimed and the response is gameplay', picture=0),
    EventDef('three_neighbours', 'Three Frontiers, Three Desks', (
        "The new foreign ministry desks deliver their first joint briefing. Sfaenland shares the longest land frontier with "
        "Glaceland, along District A and District F, and is the nearest market for the core plants. Luremia faces District F "
        "and the forests of District J. Kaluga touches only a short stretch of District J's mountains. Each relationship has "
        "its own history of small disputes and quiet cooperation.",
        "The briefing is candid about how little the capital knows. Customs posts on the frontiers are understaffed, the "
        "roads to them are poor, and most local cooperation, on grazing, timber, water and lost travellers, has been arranged "
        "by district officials who never told the ministries. The desks expect every neighbour to watch what Glaceland now "
        "does with its own empty frontier districts.",
        "Two schools are forming in the ministry. One wants open frontiers with low tariffs and fast crossings, turning the "
        "empty frontier districts into trade corridors. The other wants trade under licence, keeping those districts as "
        "buffers. First, though, the government must decide how to introduce the new desks to the neighbours: with a public "
        "conference or with quiet letters.",
    ), (
        Option('Host a frontier conference.', (Stability(0.02), PP(-15))),
        Option('Send quiet letters.', (PP(20),)),
    ), picture=1),
    EventDef('decade_commission', 'A Commission Drawn by Lot', (
        "Ten years after the National Administration opened its books, a commission drawn by lot from the district rolls "
        "publishes its ledger of the decade. It counts roads laid in the empty districts and plants opened outside the core, "
        "hulls launched in District A, aircraft kept flying, preparations made against Ulysses and money owed abroad. It also "
        "counts what was promised and never delivered.",
        "The ledger pleases nobody completely. The core districts are richer and so are some of the empty ones, but the gap "
        "between them has narrowed less than the speeches claimed. The navy and air arm are better organised and still "
        "small. The treasury collects more of what it is owed, though not all of it. District C still waits for its ferries "
        "in bad weather.",
        "Whoever holds the seals in 2001 must answer the ledger in public. A full answer, chapter by chapter, would admit "
        "failures and give critics a decade of material. A short statement of thanks would look confident and evasive at "
        "the same time. The commission has already said it will publish any reply in full beside its own findings.",
    ), (
        Option('Answer every chapter.', (Stability(0.03), PP(-20))),
        Option('Thank the commission briefly.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('usean_war', 'War in Usea', (
        "When the ISAF coalition is formed to oppose Erusea, war spreads across Usea. Glaceland is not a party to it and "
        "has no wish to become one. Yet within days of the news, shipping insurers raise their premiums, freight rates "
        "climb and fuel prices move on every market where Glaceland buys and sells. A war elsewhere arrives in Glacelandic "
        "ledgers before it arrives in Glacelandic newspapers.",
        "Merchant owners ask the government what to do. Some of their ships sail routes that touch waters near the war; most "
        "do not, but insurers do not distinguish. Exporters worry about contracts and importers about prices. The small "
        "navy worries about being asked to protect anything at all. The oil districts, for once, expect higher prices to "
        "help rather than hurt.",
        "The government sets up a freight watch to track rates and advise shippers, and must now decide how far to go. It "
        "could advise owners to avoid any route near the war, at a cost to trade, or leave the choice to owners and their "
        "insurers and accept the risk of a Glacelandic ship caught in the crossfire. Neutrality, the foreign ministry "
        "reminds everyone, is a policy that must be practised daily.",
    ), (
        Option('Advise owners to avoid the war zone.', (Stability(0.02), PP(-10))),
        Option('Leave it to owners and insurers.', (PP(20), WarSupport(-0.01))),
    ), citation='date anchor only, Official Chronicle row 2003 / 08.22 in tools/lore/chronicle.json; fired only after the '
                'mod sets ac_ucw_isaf_formed; no Glacelandic part in the war is claimed', picture=2),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('admin', 'The Suspended Ballot', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_open_books', 'The Administration Opens Its Books',
          "Glaceland enters 1991 under a National Administration that governs in the name of a democratic party while the "
          "vote itself stays suspended. Pollsters find barely one voter in a hundred behind that party; the rest split between "
          "non-party administrators and a nationalist movement. Opening the government's own files to the press is the first "
          "honest step, and an embarrassing one for every official named in them.",
          ('document', 'assembly'), reward=(Idea('provisional_mandate'), Event('suspended_ballot'))),
    Focus('adm_three_drafts', 'Three Drafts of a Constitution',
          "Lawyers in the Capital District are asked to draft three answers to one question: who holds the seals once the "
          "provisional mandate lapses. One draft restores the ballot, one keeps a non-party board, and one hands power to the "
          "nationalist movement. Drafting costs months of attention, and every faction will claim the draft it prefers as "
          "the true voice of the country.",
          ('scales', 'document'), after=('adm_open_books',),
          reward=(PP(40), Tooltip('Opens three constitutional paths; only one can be taken.'))),
    Focus('adm_ballot_path', 'Restore the Ballot Box',
          "The smallest party in the country holds the biggest title, and its remaining members argue that only a real vote "
          "can cure that. Restoring the ballot means a fixed election calendar, an independent count and a campaign the "
          "Administration may well lose. The pledge reassures foreign creditors and frightens every official who has never "
          "faced a voter.",
          ('ballot', 'assembly'), after=('adm_three_drafts',), exclusive=('adm_board_path', 'adm_petition_path'),
          reward=(SwapIdea('provisional_mandate', 'ballot_pledge'),)),
    Focus('adm_board_path', 'Administration Without Parties',
          "Nearly half the country tells pollsters it wants competent management rather than party contests. The non-party "
          "camp proposes that the Administration become a permanent board of senior officials, chosen by examination and "
          "answerable to published targets. Decisions would be fast and predictable. Nobody could vote the board out, and "
          "that is precisely the objection its critics raise.",
          ('command', 'document'), after=('adm_three_drafts',), exclusive=('adm_ballot_path', 'adm_petition_path'),
          reward=(SwapIdea('provisional_mandate', 'board_mandate'),)),
    Focus('adm_petition_path', 'The Nationalist Petition',
          "The nationalist movement leads every survey and delivers a petition demanding power. It promises discipline in the "
          "empty districts, a stronger coast and an end to what it calls government by clerks. Accepting the petition puts "
          "a mass movement behind the state. It also hands that movement the state, with very few ways to take it back.",
          ('medal', 'assembly'), after=('adm_three_drafts',), exclusive=('adm_ballot_path', 'adm_board_path'),
          reward=(SwapIdea('provisional_mandate', 'petition_mandate'),)),
    Focus('adm_council_regime', 'Seat the Elected Council',
          "Elections are held on the published calendar, and a council of ministers drawn from the new chamber takes the "
          "seals from the Administration. The council governs collectively and answers to the chamber for every budget. "
          "Parties that barely existed in 1991 must now form a government, and the officials who ran the country must learn "
          "to take instructions from them.",
          ('ballot', 'document'), after=('adm_ballot_path',), cost=10,
          exclusive=('adm_board_regime', 'adm_directorate_regime'),
          reward=(Regime('elected_council'), Flag('gov_council'))),
    Focus('adm_board_regime', 'Charter the Administrative Board',
          "A short charter turns the National Administration into a standing board of examined officials with fixed terms "
          "and published targets. Elections remain suspended, and party activity continues as debate rather than as a route "
          "to office. The board can plan a decade ahead. It also owns every failure, because there is nobody else left to "
          "blame.",
          ('command', 'scales'), after=('adm_board_path',), cost=10,
          exclusive=('adm_council_regime', 'adm_directorate_regime'),
          reward=(Regime('admin_board'), Flag('gov_board'))),
    Focus('adm_directorate_regime', 'The Directorate Takes the Seals',
          "The movement's leadership council receives the seals and forms a directorate that rules by decree until it "
          "chooses otherwise. Rival parties are suspended and district officials swear loyalty to the national programme. "
          "The directorate promises order quickly and delivers it in the towns. Foreign partners grow cautious, and dissent "
          "moves out of the newspapers into private rooms.",
          ('medal', 'command'), after=('adm_petition_path',), cost=10,
          exclusive=('adm_council_regime', 'adm_board_regime'),
          reward=(Regime('national_directorate'), Flag('gov_directorate'))),
    Focus('adm_council_court', 'A Court Above the Council',
          "The new chamber creates a constitutional court able to strike down any ministerial order that exceeds the law. "
          "Ministers complain that they have barely taken office before being checked, and some judgments land at awkward "
          "moments. In return the losing parties accept each election result, which is worth more to a young chamber than "
          "any single policy it could pass.",
          ('scales', 'assembly'), after=('adm_council_regime',), exclusive=('adm_board_exams', 'adm_directorate_programme'),
          reward=(SwapIdea('ballot_pledge', 'open_chamber'),)),
    Focus('adm_board_exams', 'Examinations for Every Post',
          "Every post in the board's service, from district clerk to deputy director, is filled by open written examination "
          "instead of patronage. Old appointees sit the same papers as school leavers. Many fail and leave bitter. The service "
          "that remains is smaller, younger and better at arithmetic, and the board can point to the results whenever anyone "
          "accuses it of favouritism.",
          ('training', 'document'), after=('adm_board_regime',), exclusive=('adm_council_court', 'adm_directorate_programme'),
          reward=(SwapIdea('board_mandate', 'merit_service'),)),
    Focus('adm_directorate_programme', 'The Programme Read Aloud',
          "The directorate publishes its national programme and orders it read aloud in schools, barracks and district "
          "offices every week. Workplaces form programme committees that report on morale and output. Public life becomes "
          "uniform and loud. Output in the core plants rises for a season, while the quieter half of the country learns to "
          "keep its views to itself.",
          ('communications', 'medal'), after=('adm_directorate_regime',), exclusive=('adm_council_court', 'adm_board_exams'),
          reward=(SwapIdea('petition_mandate', 'directorate_order'),)),
    Focus('adm_returns_library', 'Returns in Every Library',
          "The published district returns are bound into volumes and placed in every public library from District A to "
          "District J. Teachers use them in civics lessons and local papers mine them for stories. Officials dislike being "
          "quoted back to themselves. Citizens who can read what their own district said are slower to believe rumours about "
          "what the capital ignored.",
          ('document', 'civil'), after=('adm_open_books',), requires=(HasFlag('returns_published'),),
          reward=(TimedIdea('civic_returns', 730),)),
))

DISTRICTS = Branch('districts', 'The Five Empty Districts', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dis_survey', 'Survey the Roadless Districts',
          "Half of Glaceland's ten districts have no paved road network and not a single factory: C across the water, the "
          "small inland District D, the frontier districts F and J, and forested District H. Every plant in the country sits "
          "in the capital or in Districts B, G and I. A survey team drives, walks and sails through the empty half to price "
          "what joining it would take.",
          ('document', 'logistics'), reward=(Idea('district_survey'), Flag('districts_surveyed'), Event('empty_districts'))),
    Focus('dis_road_f', 'A Road Through District F',
          "District F is the frontier district facing both Sfaenland and Luremia, yet its plains and dry hills are crossed "
          "only by farm tracks. A graded trunk road from the capital to the border posts would serve the market towns and any "
          "column that must reach the frontier in a hurry. Paving it swallows a full year of the interior's construction "
          "budget.",
          ('rail', 'security'), after=('dis_survey',), reward=(Build('infrastructure', 2, 52),)),
    Focus('dis_road_d', 'Hill Tracks of District D',
          "District D is the smallest district, a few valleys of hills and dry ground wedged between the capital and Districts "
          "G, H and I. Its tracks already carry traffic between those four places, badly. Grading them into a real road "
          "network costs little and shortens half the country's inland journeys. Its villages ask why it took a survey to "
          "notice them.",
          ('tools', 'civil'), after=('dis_survey',), reward=(Build('infrastructure', 1, 41), Stability(0.01))),
    Focus('dis_road_h', 'Logging Roads into District H',
          "District H is forest, hill and mountain along the coast, with an outlying naval post on a separate islet. Loggers "
          "and the navy both want a road, for different reasons. A road along the valley floors would open timber to the "
          "plants of District I and give the coast service a way in. Objections from the forest villages are heard and mostly "
          "overruled.",
          ('logistics', 'tools'), after=('dis_survey',), reward=(Build('infrastructure', 1, 129),)),
    Focus('dis_road_j', 'Mountain Passes in District J',
          "District J borders both Luremia and Kaluga through forest and mountain country, and no road crosses it that a truck "
          "driver would trust in winter. Engineers propose bridges, cut passes and avalanche sheds along a single route. It "
          "is slow, costly work that the frontier guard has requested for years, and it will be finished long after the "
          "ministers who approve it.",
          ('bridge', 'security'), after=('dis_survey',), reward=(Build('infrastructure', 1, 576), XP('army', 10))),
    Focus('dis_councils', 'District Councils Stand for Election',
          "Under the elected council, each of the ten districts elects its own council with a budget for roads, schools and "
          "clinics. The empty districts finally have a voice that the capital must answer. Councils quarrel with ministries "
          "and with each other, and some spend their first budgets on town halls. Still, the people of District J now know "
          "exactly whom to blame.",
          ('ballot', 'civil'), after=('dis_survey',), requires=(HasFlag('gov_council'),),
          reward=(Build('infrastructure', 1, 129), Stability(0.04))),
    Focus('dis_prefects', 'Prefects for the Empty Districts',
          "The board sends examined prefects to Districts C, D, F, H and J with authority over every ministry's local office. "
          "Each prefect reports monthly against published targets for roads, schooling and clinics. Local notables resent "
          "officials who were not born in the district. The prefects answer that they were chosen for competence, and the "
          "monthly figures mostly back them.",
          ('command', 'rail'), after=('dis_survey',), requires=(HasFlag('gov_board'),),
          reward=(Build('infrastructure', 1, 41), PP(25))),
    Focus('dis_brigades', 'Labour Brigades on the Roads',
          "The directorate sends brigades of young movement volunteers to build roads in the empty districts, housed in camps "
          "and paid in rations and pocket money. The roads appear quickly and some will need rebuilding within a decade. The "
          "brigades bring the movement's songs and banners into every valley, which is as much the purpose as the gravel."
          " Local farmers watch them warily.",
          ('rebuild', 'medal'), after=('dis_survey',), requires=(HasFlag('gov_directorate'),),
          reward=(Build('infrastructure', 1, 52), WarSupport(0.02))),
    Focus('dis_spread', 'A Plant in Every District',
          "One school of planners insists that every district deserves at least one modern plant, built with public credit "
          "and protected for a decade. Plants in the empty districts would employ people where they live and spread industry "
          "beyond the reach of a single strike. They would also be smaller, slower and dearer to supply than another hall in "
          "the core.",
          ('industry', 'civil'), after_any=('dis_road_f', 'dis_road_d', 'dis_road_h', 'dis_road_j'), cost=10,
          exclusive=('dis_core',), reward=(SwapIdea('district_survey', 'district_quotas'),)),
    Focus('dis_core', 'Grow the Core Corridor',
          "The opposing school wants every spare credit to flow into the corridor between the capital and Districts B, G and "
          "I, where roads, power and workers already exist. Output per worker would rise fastest there. The empty districts "
          "would get roads and schools but not factories, and their young people would keep moving to the core in search of "
          "work.",
          ('rail', 'industry'), after_any=('dis_road_f', 'dis_road_d', 'dis_road_h', 'dis_road_j'), cost=10,
          exclusive=('dis_spread',), reward=(SwapIdea('district_survey', 'core_corridor'), Build('infrastructure', 1, 50))),
    Focus('dis_plant_f', 'Grain Mills of District F',
          "The first protected plant opens on District F's plains, milling grain and building farm machinery for the frontier "
          "towns. It sits close enough to the Sfaenland border that ministers argue about the wisdom of it. Its workers argue "
          "only about wages. Within a year the district has a payroll it never had before and a reason to keep its young.",
          ('industry', 'tools'), after=('dis_spread',), reward=(Build('industrial_complex', 1, 52),)),
    Focus('dis_plant_j', 'Timber Works in District J',
          "District J's forests feed a new timber and joinery works in the valley nearest the coast, served by the new "
          "mountain road. It makes prefabricated housing panels for the whole country. The works run below capacity in their "
          "first winters because snow closes the road, which proves the engineers right about avalanche sheds and the "
          "accountants right about cost.",
          ('tools', 'rebuild'), after=('dis_spread', 'dis_road_j'), reward=(Build('industrial_complex', 1, 576),)),
    Focus('dis_plant_dh', 'Workshops for Districts D and H',
          "Two smaller workshops follow, one in District D's hill valleys and one in District H's coastal forest. Each repairs "
          "trucks, boats and machinery for its own district rather than producing for the national market. They are modest. "
          "They also mean that a broken pump in District H no longer waits three weeks for a part sent out from the capital.",
          ('tools', 'industry'), after=('dis_spread',),
          reward=(Build('industrial_complex', 1, 41), Build('industrial_complex', 1, 129))),
    Focus('dis_core_shifts', 'Round-the-Clock Core Plants',
          "With credit concentrated in the corridor, the core plants of the capital and Districts B, G and I add second and "
          "third shifts instead of new halls. Housing for incoming workers goes up quickly and badly. Output climbs, and so do "
          "rents. The empty districts send their young along the new roads, and their councils send angry letters along the "
          "same roads.",
          ('industry', 'economy'), after=('dis_core',), reward=(TimedIdea('night_shifts', 730),)),
))

TREASURY = Branch('treasury', 'Oil, Steel and the Treasury', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('tre_gap', 'Fifteen in Every Hundred',
          "Treasury auditors estimate that Glaceland collects about eighty-five of every hundred it is owed in tax, and that "
          "public debt already stands near a third of national output. Growth is steady and inflation low, so the gap is a "
          "slow leak rather than a flood. Closing it means auditing firms, districts and ministries at once, and all three "
          "will complain.",
          ('scales', 'economy'), reward=(Idea('collection_drive'), Event('collection_gap'))),
    Focus('tre_oil_fields', 'Three Oil Districts',
          "Every barrel Glaceland pumps comes from three places: the Capital District and Districts B and I. The wells are "
          "shallow and old, and the country's one fuel depot sits in the capital. A field survey prices new pumps, gathering "
          "lines and storage, and asks the question the rest of the branch must answer: sell the oil abroad or burn it at "
          "home?",
          ('economy', 'tools'), after=('tre_gap',),
          reward=(Research('excavation_tech', 0.5, 1), Tooltip('Opens the choice between export and home refining.'))),
    Focus('tre_export', 'Crude for Foreign Buyers',
          "The export school would sell most of the crude abroad under long contracts, using the foreign currency to buy "
          "machinery and pay down the debt. Revenue arrives quickly and the treasury's arithmetic improves. The plants at home "
          "keep importing refined fuel at world prices, and a fall in those prices would hit both sides of the national ledger "
          "at once.",
          ('economy', 'diplomacy'), after=('tre_oil_fields',), cost=10, exclusive=('tre_refine',),
          reward=(SwapIdea('collection_drive', 'fuel_export'), Flag('model_export'))),
    Focus('tre_refine', 'Keep the Crude at Home',
          "The refining school would keep the crude in Glaceland, enlarge the capital's fuel depot and build refining and "
          "chemical capacity beside the oil districts. The core plants would run on their own fuel. Foreign currency would come "
          "more slowly and the debt would wait. In return, an embargo or a price shock abroad would matter far less to the "
          "country.",
          ('industry', 'tools'), after=('tre_oil_fields',), cost=10, exclusive=('tre_export',),
          reward=(SwapIdea('collection_drive', 'home_refining'), Flag('model_refine'))),
    Focus('tre_mills_b', 'The Rolling Mills of District B',
          "District B is the largest town outside the capital, with steel and aluminium, three civilian plants and two arms "
          "works. Its rolling mills run on old machinery. New mill stands and an electric furnace would lift quality enough to "
          "supply the District A yards without imports. The work disrupts output for a season and the arms works lose their "
          "priority on steel.",
          ('industry', 'scales'), after=('tre_gap',),
          reward=(TimedIdea('mill_retooling', 365), Research('industry', 0.5, 1))),
    Focus('tre_aluminium', 'Aluminium for Airframes',
          "The capital and Districts B and I hold enough bauxite and power to smelt aluminium for light airframes and vehicle "
          "bodies. A smelter contract with the arms works would let the air arm repair its own fighters instead of waiting for "
          "foreign parts. The smelters drink electricity, and households in District I notice the evening brownouts long "
          "before any new aircraft.",
          ('air', 'industry'), after=('tre_mills_b',), reward=(Idea('light_metal'),)),
    Focus('tre_order_book', 'One Book for Six Arms Works',
          "Glaceland's six arms works, two each in the capital and District B and one each in Districts G and I, buy their "
          "materials separately and compete for the same skilled workers. A single order book would schedule them as one "
          "producer, with each works specialising. Managers lose autonomy and some lose their posts. The army finally learns "
          "what it can actually get.",
          ('missile', 'document'), after=('tre_gap',), reward=(Idea('arms_order_book'),)),
    Focus('tre_tanker_berth', 'A Tanker Berth for District A',
          "Export crude needs a deep tanker berth, and the only yards and large harbour in the country are in District A "
          "beside the Sfaenland frontier. Dredging a berth and laying a pipeline from the oil districts is a large contract the "
          "yards would gladly take. Sfaenland watches a strategic pipeline being laid along its frontier and asks polite "
          "questions.",
          ('navy', 'economy'), after=('tre_export',), reward=(Build('infrastructure', 1, 9), PP(-20))),
    Focus('tre_debt', 'Retire the Debt Early',
          "Export receipts go first to the national debt, which stood near a third of output when the decade began. Every bond "
          "retired early lowers the interest bill and lifts the country's credit. Ministers who wanted new hospitals and roads "
          "must wait. Bankers in every neighbouring capital notice that Glaceland, for once, pays its bills ahead of "
          "schedule.",
          ('scales', 'diplomacy'), after=('tre_export',), reward=(PP(50), Stability(0.02))),
    Focus('tre_refinery_f', 'Refinery Halls in District F',
          "Refinery halls rise on the plains of District F, a short pipeline from the capital's wells, where there is flat "
          "land and room for tanks. The refinery employs the frontier district and fuels the core plants. Placing it near the "
          "Sfaenland border troubles the defence staff; the planners answer that the wells it serves sit in the capital next "
          "door.",
          ('industry', 'logistics'), after=('tre_refine',), reward=(Build('industrial_complex', 1, 52), Stability(0.01))),
    Focus('tre_second_depot', 'A Second Fuel Depot',
          "The capital holds Glaceland's only fuel depot, which means a single fire, strike or air raid could empty every tank "
          "in the country. A second depot dug into the hills would hold a reserve for the army, the air arm and the coastal "
          "escorts. It takes steel and concrete from the core plants and pays nothing until the day it is needed.",
          ('security', 'economy'), after=('tre_refine',), reward=(Idea('strategic_stock'),)),
))

COAST = Branch('coast', 'Five Escorts and a Long Coast', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('coa_register', 'Count the Hulls',
          "Glaceland's navy amounts to five escorts and two coastal submarines guarding a coastline far longer than its land "
          "frontiers, beside a merchant fleet of about a hundred and eight hulls. Its main base and all four dockyards are in "
          "District A, with small posts in District C and on District H's islet. A register of hulls, crews and berths is the "
          "first honest picture.",
          ('navy', 'document'), reward=(Idea('coast_register'), Event('long_coast'))),
    Focus('coa_slipways', 'The Four Slipways of District A',
          "District A's four slipways have built nothing larger than a coaster in years and spend most of their time on "
          "repairs. Modern cranes, a covered hall and apprentices trained in welding rather than riveting would let the yards "
          "build their own escorts. The yards sit beside the Sfaenland frontier, which makes them both valuable and exposed.",
          ('tools', 'navy'), after=('coa_register',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
    Focus('coa_escort', 'Convoy Escort Command',
          "The escort school wants the five escorts organised around the merchant fleet: fixed lanes between the coastal "
          "districts and District C, escort groups on rotation and merchant captains trained to sail in company. It protects "
          "the trade the country lives on. It leaves long stretches of empty coast watched only by fishermen and whatever the "
          "air arm can spare.",
          ('navy', 'logistics'), after=('coa_register',), cost=10, exclusive=('coa_subs', 'coa_guard'),
          reward=(SwapIdea('coast_register', 'escort_command'), Flag('coast_command_set'))),
    Focus('coa_subs', 'Two Submarines, Many Inlets',
          "The submarine school argues that two quiet boats along the mountain coasts of Districts H and J would deter a "
          "landing more cheaply than escorts could. Doctrine already prefers a fleet that stays in being to one that seeks "
          "battle. Submarines cannot escort merchant ships or show a flag in harbour, and the merchant captains say so loudly "
          "and often.",
          ('submarine', 'navy'), after=('coa_register',), cost=10, exclusive=('coa_escort', 'coa_guard'),
          reward=(SwapIdea('coast_register', 'sub_patrol'), Flag('coast_command_set'))),
    Focus('coa_guard', 'A Fishery and Customs Guard',
          "A third school says Glaceland's real problems at sea are smuggling, illegal fishing and ships in distress, not "
          "foreign fleets. It would turn part of the navy into a guard service with cutters, boarding teams and rescue "
          "stations in every coastal district. The guard would be popular and useful every single day. In a real war it would "
          "be outclassed.",
          ('fishing', 'security'), after=('coa_register',), cost=10, exclusive=('coa_escort', 'coa_subs'),
          reward=(SwapIdea('coast_register', 'coast_guard'), Flag('coast_command_set'))),
    Focus('coa_escort_hulls', 'Escorts from Our Own Slipways',
          "With a command built around convoys, the District A yards receive a standing order for new escorts on a modest, "
          "steady schedule. The yards would rather have one large order and then a gap; the navy wants a hull every year so "
          "that crews and builders stay employed. A new slipway on District H's coast spreads the work and the risk.",
          ('navy', 'tools'), after=('coa_escort',), reward=(Build('dockyard', 1, 129), XP('navy', 15))),
    Focus('coa_sub_pen', 'A Submarine Pen in District J',
          "The submarine base goes into District J's coast, where the mountains come down to the sea and the shoreline offers "
          "cover. A small yard for submarine maintenance is cut beside it. The work is slow and the district's new road carries "
          "most of the material. Observers across the Luremian and Kalugan frontiers take careful note of the construction "
          "traffic.",
          ('submarine', 'shelter'), after=('coa_subs',), reward=(Build('dockyard', 1, 576), Research('naval_equipment', 0.5, 1))),
    Focus('coa_rescue', 'Rescue Stations on Every Coast',
          "The guard builds rescue and customs stations along every coastal district, each with a cutter, a radio mast and a "
          "crew trained for storms. Fishing communities that saw the navy as a distant institution now see sailors pulling "
          "their neighbours from the water. Smugglers move their landings elsewhere, which is exactly the point.",
          ('medical', 'fishing'), after=('coa_guard',), reward=(Build('radar_station', 1, 9), Stability(0.03))),
    Focus('coa_islet', 'The Islet Post of District H',
          "District H's naval post stands on a separate islet offshore, with one jetty and a handful of sailors who rotate "
          "every month. It is the country's most exposed outpost and its best listening point. A longer jetty, a radio station "
          "and a resident crew turn a lonely rotation into a proper post. The crews' families promptly ask for a school.",
          ('navy', 'security'), after=('coa_register',), reward=(Build('radar_station', 1, 129), XP('navy', 10))),
    Focus('coa_merchant', 'A Hundred and Eight Hulls',
          "The merchant fleet carries most of the country's trade and all of its traffic to District C, and many of its ships "
          "are older than their captains. A replacement credit lets owners scrap the worst and order new coasters from the "
          "District A yards, keeping the fleet and the yards alive together. Owners must accept naval inspection in return.",
          ('logistics', 'navy'), after=('coa_slipways',), reward=(Idea('fleet_renewal'),)),
))

ISLAND = Branch('island', 'District C Across the Water', 1993, 'FOCUS_FILTER_STABILITY', (
    Focus('isl_crossing', 'The Crossing to District C',
          "District C lies across the water from the rest of Glaceland: twenty-two provinces of plains and hills with a small "
          "naval post and not one paved road or factory. Everything its people need arrives by ship, and everything they "
          "produce leaves the same way. The crossing is the district's lifeline, and in bad weather its isolation is "
          "complete.",
          ('navy', 'civil'), reward=(Event('across_water'), Build('infrastructure', 1, 35))),
    Focus('isl_farm_roads', 'Farm Roads Across District C',
          "District C's plains grow food the rest of the country imports, but crops spoil waiting for carts on dirt tracks. A "
          "network of farm roads from the fields to the harbour turns harvests into cargo. The work is easy by mainland "
          "standards, on flat ground over short distances, and the district takes it as the first sign that the capital "
          "remembers it.",
          ('logistics', 'civil'), after=('isl_crossing',), reward=(Build('infrastructure', 2, 35),)),
    Focus('isl_charter', 'A Charter for District C',
          "Islanders have long run their own affairs out of necessity. A charter would recognise a District C assembly with "
          "powers over local roads, schools, fisheries and ferry fares, while defence, currency and foreign affairs stay with "
          "the national government. The district gains pride and patience; the capital gains a partner it cannot simply "
          "instruct.",
          ('document', 'assembly'), after=('isl_crossing',), cost=10, exclusive=('isl_direct',),
          reward=(Idea('c_charter'), Flag('c_home_rule'),
                  Tooltip('No border, core or sovereignty change; District C remains part of Glaceland.'))),
    Focus('isl_direct', 'Governed from the Capital',
          "The alternative sends a resident commissioner with full authority over every ministry office in District C, backed "
          "by a budget the capital controls. Projects move faster when one official can sign for all of them. Islanders who "
          "already feel distant will now feel ruled. Success depends on whether the money arrives faster than the "
          "resentment.",
          ('command', 'navy'), after=('isl_crossing',), cost=10, exclusive=('isl_charter',),
          reward=(Idea('c_commissioner'), Flag('c_direct_rule'))),
    Focus('isl_harbour', 'The District C Harbour Works',
          "Whatever command the navy has chosen, it needs a working harbour across the water. The District C post gains a "
          "slipway for ferries and fishing boats, so the district can repair its own hulls instead of waiting weeks for a "
          "berth in District A. Mainland yard owners object to the competition, and the islanders build it anyway.",
          ('navy', 'tools'), after=('isl_crossing',), requires=(HasFlag('coast_command_set'),),
          reward=(Build('dockyard', 1, 35),)),
    Focus('isl_cannery', 'Canneries and Mills of District C',
          "With roads to the harbour, District C can process its own grain and fish instead of shipping them raw. A cannery "
          "and a flour mill are built with public credit near the harbour. Prices for the district's farmers rise and mainland "
          "importers pay a little more. For the first time, District C sells finished goods rather than raw cargo.",
          ('fishing', 'industry'), after=('isl_farm_roads',), reward=(Build('industrial_complex', 1, 35),)),
    Focus('isl_assembly', 'The First District C Assembly',
          "The chartered assembly meets for the first time in the harbour town, and its first act is to set ferry fares lower "
          "than the ministry wanted. Its second is to ask for a share of fishing licence revenue. Ministers grumble. Turnout "
          "in District C is the highest in the country, and its loyalty to the national government rises with it.",
          ('assembly', 'ballot'), after=('isl_charter',), requires=(HasFlag('c_home_rule'),),
          reward=(Build('infrastructure', 1, 35), Stability(0.03))),
    Focus('isl_building_season', 'The Commissioner Builds',
          "The commissioner uses full authority to run one building season: roads, a clinic, a radio mast and quarters for the "
          "naval post, all tendered at once to mainland contractors. The work finishes ahead of schedule. Islanders note that "
          "few of the jobs went to islanders, and the commissioner's office becomes the most guarded building in the "
          "district.",
          ('command', 'rebuild'), after=('isl_direct',), requires=(HasFlag('c_direct_rule'),),
          reward=(Build('radar_station', 1, 35), PP(25))),
    Focus('isl_airstrip', 'An Airstrip for District C',
          "Ships take a day; aircraft take an hour. A paved airstrip on District C's plains lets mail, doctors and the air arm "
          "reach the district in seasons when the ferries cannot sail. The strip doubles as a dispersal field for fighters, "
          "which pleases the air staff more than the islanders. It is cheap to build on flat ground and costly to keep "
          "staffed.",
          ('runway', 'civil'), after=('isl_farm_roads',), reward=(Build('air_base', 1, 35),)),
))

ARMY = Branch('army', 'Hill and Forest Battalions', 1993, 'FOCUS_FILTER_ARMY_XP', (
    Focus('arm_staff_map', 'Eight Formations, Ten Districts',
          "The army has eight infantry formations to cover ten districts, three land neighbours and a district across the "
          "water. Most of the country is forest, hill or mountain, where a formation moves at a walking pace. Mapping which "
          "formation could reach which border, and how fast, shows the gaps nobody wanted written down. The map becomes the "
          "army's argument for everything that follows.",
          ('security', 'document'), reward=(Event('hill_country'), XP('army', 10))),
    Focus('arm_mountaineers', 'The Mountaineer School',
          "Some infantry already trains as mountaineers, but each formation does it its own way. A national mountaineer "
          "school in the mountains of District J standardises climbing, cold-weather survival and movement through forest, "
          "and its graduates return to their formations as instructors. The school competes with the frontier guard for the "
          "same hardy recruits, and the guard usually loses.",
          ('training', 'medal'), after=('arm_staff_map',), reward=(Research('land_doctrine', 0.5, 1), XP('army', 15))),
    Focus('arm_district', 'A Battalion for Every District',
          "The territorial school wants each district to raise and keep its own battalion of local reservists who know every "
          "valley and track. Defence would be everywhere at once and an invasion expensive in every province. Battalions would "
          "train only a few weeks a year, and a district battalion is better at holding its own hills than at going anywhere "
          "else.",
          ('security', 'training'), after=('arm_staff_map',), cost=10, exclusive=('arm_corps',),
          reward=(Idea('district_battalions'), Flag('army_territorial'))),
    Focus('arm_corps', 'A Single Mountain Corps',
          "The professional school wants the eight formations rebuilt around one mobile mountain corps of long-service "
          "soldiers, able to move by rail and truck to whichever frontier is threatened. It would be a fine force for its size. "
          "It would also leave large parts of the country without troops until the corps arrived, and arrival depends on "
          "roads.",
          ('medal', 'training'), after=('arm_staff_map',), cost=10, exclusive=('arm_district',),
          reward=(Idea('mountain_corps'), Flag('army_mobile'))),
    Focus('arm_depots', 'Depots at the Logistics Centres',
          "The logistics centres in Districts B, G and I and the capital hold the army's supplies, laid out for peacetime "
          "convenience. Restocking them for war, with a forward store toward each land frontier, locks up equipment that could "
          "be issued. The army has nearly two thousand sets of infantry equipment and about a thousand vehicles to place.",
          ('logistics', 'rail'), after=('arm_staff_map',), reward=(Idea('forward_stores'), Research('logistics_tech', 0.5, 1))),
    Focus('arm_muster', 'District Muster Weekends',
          "Every district battalion musters for one weekend a month and two weeks each summer, in its own valleys. Employers "
          "must release reservists and are paid compensation from the defence budget. The weekends become social occasions "
          "as much as drills. In time each district knows its own ground, officers and shelters, which is the whole point of "
          "the territorial school.",
          ('training', 'civil'), after=('arm_district',), requires=(HasFlag('army_territorial'),),
          reward=(TimedIdea('muster_season', 1095), XP('army', 15))),
    Focus('arm_troop_trains', 'Troop Trains for the Corps',
          "A mobile corps is only as fast as its trains. The army buys priority on the national rail network, builds loading "
          "ramps at the logistics centres and keeps trains ready to move at a day's notice. Freight customers lose some slots. "
          "The corps can now reach any land frontier within hours, provided the rails and bridges are intact.",
          ('rail', 'logistics'), after=('arm_corps',), requires=(HasFlag('army_mobile'),),
          reward=(Research('train_tech', 0.5, 1), Build('infrastructure', 1, 50))),
    Focus('arm_volunteers', 'Volunteer Companies of the Movement',
          "The directorate forms volunteer companies from movement members and attaches them to the regular formations for "
          "border watch and internal security. They are eager, poorly trained and loyal to the movement first. Officers resent "
          "them and are told to train them anyway. They add numbers to the frontier and a second chain of command to every "
          "barracks.",
          ('medal', 'security'), after=('arm_staff_map',), requires=(HasFlag('gov_directorate'),),
          reward=(Idea('volunteer_companies'), WarSupport(0.03))),
    Focus('arm_frontier_posts', 'Watch Posts on the Land Borders',
          "Whichever school prevailed, the borders with Sfaenland, Luremia and Kaluga need permanent posts linked by telephone "
          "and radio to the nearest formation. The posts are small and visible, meant to watch rather than fight. Neighbours "
          "are told in advance to avoid misunderstanding. A frontier that can be seen being watched is rarely tested.",
          ('security', 'diplomacy'), after_any=('arm_district', 'arm_corps'),
          reward=(Flag('frontier_posts'), XP('army', 10))),
    Focus('arm_firepower', 'Guns Before Numbers',
          "Army doctrine already favours firepower over numbers, because Glaceland will never have the numbers. Batteries "
          "trained to fire in forest and mountain country, with observers on the ridgelines, would let a small force hold a "
          "valley against a larger one. The guns are expensive and must be hauled up roads that in many districts do not yet "
          "exist.",
          ('missile', 'training'), after=('arm_mountaineers',), reward=(Research('artillery', 0.5, 1), XP('army', 10))),
))

AIR = Branch('air', 'Two Airfields', 1994, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count', 'Seventy-Two Fighters, Two Fields',
          "Glaceland's air arm flies seventy-two fighters and a dozen ground-attack aircraft from exactly two airfields, one "
          "beside the capital and one in District B. Every aircraft in the country could be caught on the ground by a single "
          "bad morning. The air staff writes this down plainly for the first time and asks the government which risk it "
          "prefers.",
          ('air', 'runway'), reward=(Idea('two_fields'), Event('two_fields_report'))),
    Focus('air_disperse', 'Scatter the Squadrons',
          "The dispersal school would build simple strips in the forests and hills of Districts H and J, each able to hold a "
          "squadron under camouflage. No single strike could destroy the air arm. Ground crews would be spread thin, "
          "maintenance would suffer, and pilots would spend more hours on the road between strips than in the air.",
          ('air', 'logistics'), after=('air_count',), cost=10, exclusive=('air_harden',),
          reward=(SwapIdea('two_fields', 'dispersed_wings'), Build('air_base', 1, 129), Build('air_base', 1, 576))),
    Focus('air_harden', 'Harden the Two Fields',
          "The hardening school would keep the air arm at its two fields but bury it: concrete shelters for every aircraft, "
          "buried fuel lines and runways that can be patched within hours. Maintenance stays efficient and crews stay "
          "together. Everything still depends on two places that any enemy can find on a map.",
          ('shelter', 'runway'), after=('air_count',), cost=10, exclusive=('air_disperse',),
          reward=(SwapIdea('two_fields', 'hardened_fields'), Build('air_base', 1, 50), Build('air_base', 1, 26))),
    Focus('air_radar', 'A Coastal Radar Chain',
          "Radar coverage ends a short distance beyond the two airfields. Stations along the coast of District A and on the "
          "capital's approaches would give fighters warning in time to take off. Radar posts are cheap next to fighters and "
          "useless without them. Technicians must be trained from scratch, because the country has never needed many.",
          ('radar', 'air'), after=('air_count',), reward=(Build('radar_station', 1, 9), Build('radar_station', 1, 50))),
    Focus('air_pilot_hours', 'Pilot Hours Before Airframes',
          "Seventy-two fighters mean little if pilots fly only a few hours a month. The air staff proposes buying fuel and "
          "flying hours before any new aircraft, with a pilot school at the District B field. Fuel comes from the country's "
          "own wells, which makes the plan cheaper here than in most places. Airframes wear out faster and the parts bill "
          "grows.",
          ('training', 'air'), after=('air_count',), reward=(XP('air', 25), Research('air_doctrine', 0.5, 1))),
    Focus('air_ground_attack', 'A Dozen Ground-Attack Aircraft',
          "The twelve ground-attack aircraft are the army's only air support, and they have rarely trained with the army at "
          "all. Joint exercises in the forests and hills, with forward observers from the infantry, teach both services to "
          "work together. Each exercise costs fuel and now and then an aircraft. The army finally learns what the air arm can "
          "do for it.",
          ('missile', 'air'), after=('air_pilot_hours',), reward=(TimedIdea('joint_exercises', 1095), XP('air', 10))),
    Focus('air_watch_service', 'Observers in Every District',
          "Civilian volunteers in every district report aircraft by telephone to a plotting room in the capital, filling the "
          "gaps between radar stations. Farmers, foresters and fishermen learn silhouettes from printed cards. The service "
          "costs almost nothing and makes the whole country part of its own air defence, though it also produces a steady "
          "stream of false alarms about seagulls.",
          ('telescope', 'security'), after=('air_radar',), reward=(Idea('air_watch'),)),
    Focus('air_overhaul', 'Repair Shops at the Arms Works',
          "Glaceland's fighters go abroad for major overhauls, which takes months and foreign currency. Repair shops attached "
          "to the arms works of the capital and District B would keep most aircraft at home. The shops take floor space from "
          "the arms lines and need engineers the country does not yet have. Each aircraft repaired at home is one more "
          "available.",
          ('tools', 'air'), after_any=('air_disperse', 'air_harden'), reward=(TimedIdea('home_overhaul', 1095),)),
))

ULYSSES = Branch('ulysses', 'Under the Ulysses Warning', 1995, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_bulletin', 'The Astronomers Bulletin',
          "Since the international astronomers' announcement of December 1994, Glaceland's newspapers print the asteroid "
          "Ulysses beside the weather. Nobody can say whether fragments will fall, or where. The government forms a committee "
          "of astronomers, engineers and district officials to follow the reports and advise what a small coastal country "
          "could do. Its first advice is to stop the rumours.",
          ('telescope', 'meteor'), reward=(Idea('sky_watch'), Stability(0.01))),
    Focus('uly_tracking', 'A Share in the Tracking Data',
          "Glaceland has no large telescope, but its universities can process the tracking data the major observatories "
          "publish. A small computing group in the capital trains students to calculate fragment paths themselves, so the "
          "government need not rely on foreign summaries. The group is cheap, the training lasts, and its first forecasts are "
          "no more certain than anyone else's.",
          ('telescope', 'science'), after=('uly_bulletin',),
          reward=(Research('electronics', 0.5, 1), Research('radar_tech', 0.5, 1))),
    Focus('uly_announced', 'The Committee Goes Public',
          "In April 1996 the world is told that Ulysses will strike the Earth and that nations must prepare. The committee's "
          "quiet monitoring becomes a national programme overnight. Ministers face a choice between storing what the country "
          "will need and moving people away from what they fear. Either answer costs as much as the defence budget, and the "
          "treasury says so.",
          ('meteor', 'communications'), after=('uly_bulletin',), requires=(After('1996.4.20'),),
          reward=(Event('ulysses_warning'),)),
    Focus('uly_stores', 'A Year of Fuel and Grain',
          "The storage school would fill depots, granaries and cisterns with a year of fuel, grain and medicine, spread across "
          "the districts so that no single fall could destroy the reserve. The country's own oil makes the fuel cheap. Grain "
          "must be bought abroad at prices that rise every month the asteroid stays in the news.",
          ('security', 'economy'), after=('uly_announced',), cost=10, exclusive=('uly_refuges',),
          reward=(Idea('reserve_stores'), Flag('ulysses_stores'))),
    Focus('uly_refuges', 'Refuges in the Interior',
          "The evacuation school notes that most districts and most plants lie on the coast, while Districts D and F and the "
          "capital lie inland. It would prepare refuges, water and camp roads in the interior and evacuation timetables for "
          "every coastal town. Moving people costs less than storing a year of food. It works only if the warning comes in "
          "time.",
          ('refugees', 'shelter'), after=('uly_announced',), cost=10, exclusive=('uly_stores',),
          requires=(HasFlag('districts_surveyed'),),
          reward=(Idea('inland_refuges'), Flag('ulysses_refuges'), Build('infrastructure', 1, 41))),
    Focus('uly_district_depots', 'Ten District Depots',
          "The reserve is divided among ten district depots, each holding its share under the eye of local officials. "
          "Inventories are published so that hoarding by officials can be spotted. Keeping grain fresh means rotating it "
          "through the shops every year, which turns the reserve into a modest subsidy on bread that nobody in the districts "
          "minds.",
          ('logistics', 'civil'), after=('uly_stores',), requires=(HasFlag('ulysses_stores'),),
          reward=(Stability(0.03), Research('logistics_tech', 0.5, 1))),
    Focus('uly_timetables', 'Timetables for the Coastal Towns',
          "Every coastal town receives a timetable assigning its people to trains, buses and roads toward a named inland "
          "refuge. The first full drill in District G jams every road into the capital and planners rewrite the timetables. "
          "The second drill runs faster. People begin to believe the plan might work, and the interior districts begin to "
          "resent the traffic.",
          ('rail', 'refugees'), after=('uly_refuges',), requires=(HasFlag('ulysses_refuges'),),
          reward=(Build('infrastructure', 1, 52), Stability(0.02))),
    Focus('uly_roche', 'The Night of the Roche Limit',
          "In July 1999 Ulysses passes through the Earth's Roche limit and begins to break apart. Whatever Glaceland prepared "
          "is now tested by the only judge that matters. The committee sits through the night in the capital, district "
          "officials stand by their telephones, and every radio in the country is tuned to the same bulletin.",
          ('meteor', 'shelter'), after_any=('uly_district_depots', 'uly_timetables'), requires=(After('1999.7.8'),),
          reward=(Event('roche_limit'),)),
    Focus('uly_count', 'Counting What Fell',
          "Once the fragment showers end, the committee counts the cost: what fell near Glaceland, what fell elsewhere and what "
          "the preparations actually achieved. Reserves are released, refuges stood down and depots put to other uses. Some "
          "ministers want to keep the emergency apparatus permanently; others want its budget back for roads.",
          ('rebuild', 'document'), after=('uly_roche',), reward=(RemoveIdea('sky_watch'), Stability(0.04))),
))

FRONTIER = Branch('frontier', 'Sfaenland, Luremia and Kaluga', 1996, 'FOCUS_FILTER_POLITICAL', (
    Focus('fro_desks', 'A Desk for Each Neighbour',
          "Glaceland shares land borders with three countries: Sfaenland along District A and District F, Luremia along "
          "District F and District J, and Kaluga on a short stretch of District J's mountains. Each relationship has been "
          "handled by whichever ministry happened to have a problem. A foreign ministry desk for each neighbour, with its own "
          "staff and files, ends the improvisation.",
          ('diplomacy', 'document'), reward=(Idea('border_desks'), Event('three_neighbours'))),
    Focus('fro_sfaenland_road', 'The Sfaenland Trade Road',
          "Sfaenland is the longest land frontier and the nearest market. A paved crossing from District A's yards and a second "
          "through District F would carry steel, fuel and machinery one way and food the other. Customs officers must be hired "
          "and trained on both sides. The road also makes the frontier easier to cross for everyone else.",
          ('logistics', 'diplomacy'), after=('fro_desks',),
          reward=(Build('infrastructure', 1, 9), Build('infrastructure', 1, 52))),
    Focus('fro_luremia', 'Valley Agreements with Luremia',
          "Herders and foresters in Districts F and J cross into Luremia every season along valley paths their families have "
          "used for generations. A short agreement on grazing, timber and water gives both sides a procedure for disputes instead "
          "of shouting matches at the posts. No line on any map changes. The agreement is dull, and dull agreements last.",
          ('peace', 'scales'), after=('fro_desks',),
          reward=(Stability(0.03), Tooltip('No border or claim changes; the agreement covers grazing, timber and water.'))),
    Focus('fro_kaluga', 'A Telephone Line to Kaluga',
          "The Kaluga frontier is short, mountainous and nearly forgotten, which is exactly why an incident there could grow "
          "before either capital noticed. A direct line between the frontier posts, a maintained track to reach them and a "
          "yearly meeting of their commanders cost almost nothing. The line rings mostly about lost hikers, the best possible "
          "result.",
          ('communications', 'diplomacy'), after=('fro_desks',), requires=(HasFlag('frontier_posts'),),
          reward=(Build('infrastructure', 1, 576), PP(15))),
    Focus('fro_open', 'Open Trade on Every Frontier',
          "One faction in the foreign ministry wants the land frontiers fully open: low tariffs, fast customs and long-term "
          "contracts with all three neighbours. The empty frontier districts would become trade corridors. Producers in the "
          "core plants would face competition they have never known, and a neighbour's crisis would reach Glacelandic markets "
          "the next morning.",
          ('economy', 'diplomacy'), after=('fro_desks',), cost=10, exclusive=('fro_guarded',),
          reward=(SwapIdea('border_desks', 'open_frontiers'), Flag('frontier_open'))),
    Focus('fro_guarded', 'Trade on Guarded Terms',
          "The other faction prefers trade under licence: quotas, inspections and contracts approved one at a time, with the "
          "frontier districts kept as buffers rather than corridors. Domestic plants stay protected and the government keeps "
          "a hand on every crossing. Neighbours find Glaceland a correct but difficult partner, and smugglers find the licences "
          "a business opportunity.",
          ('security', 'scales'), after=('fro_desks',), cost=10, exclusive=('fro_open',),
          reward=(SwapIdea('border_desks', 'licensed_frontiers'), Flag('frontier_guarded'))),
    Focus('fro_market_towns', 'Markets in the Frontier Towns',
          "With tariffs low, the market towns of Districts F and J fill with traders from all three neighbours on market days. "
          "Warehouses and inns open where there were only farms. The frontier towns grow faster than the capital for the "
          "first time. The core plants lose some sales to imports and win others in markets they had never reached.",
          ('economy', 'civil'), after=('fro_open',), requires=(HasFlag('frontier_open'),),
          reward=(Build('industrial_complex', 1, 52),)),
    Focus('fro_bonded', 'Bonded Warehouses at the Crossings',
          "Every licensed crossing gets a bonded warehouse where goods wait under customs seal until their papers clear. "
          "Revenue at the frontier rises sharply and traders complain about delays measured in days. The treasury, still "
          "chasing the fifteen in every hundred it fails to collect, is delighted, and the frontier guard knows exactly what "
          "is crossing.",
          ('document', 'logistics'), after=('fro_guarded',), requires=(HasFlag('frontier_guarded'),),
          reward=(Build('industrial_complex', 1, 576), PP(20))),
))

CENTURY = Branch('century', 'Accounts for a New Century', 2001, 'FOCUS_FILTER_RESEARCH', (
    Focus('cen_ledger', 'The Ten-Year Ledger',
          "A decade after the Administration opened its books, an independent commission compares the Glaceland of 2001 with "
          "the Glaceland of 1991: roads in the empty districts, plants outside the core, the navy and the air arm, the "
          "preparations made against Ulysses. Its members are drawn by lot from the district rolls, and its report spares nobody.",
          ('scales', 'document'), reward=(Event('decade_commission'),)),
    Focus('cen_answer', 'Answer the Ledger in Public',
          "The commission's sharpest chapter concerns government itself. Whichever order took the seals in the nineties has "
          "now governed long enough to be judged on its record rather than its promises. The government answers the chapter "
          "in public, line by line. Every critic in the country writes a reply, and the government is stronger for having "
          "invited them.",
          ('assembly', 'communications'), after=('cen_ledger',), reward=(TimedIdea('renewed_mandate', 1095),)),
    Focus('cen_institutes', 'Applied Institutes in the Capital',
          "Glaceland's three research programmes have always been spread thin across ministries. Two applied institutes, one "
          "for engineering and one for electronics and radio, would concentrate them in the capital with university partners. "
          "They need staff who mostly left for posts abroad. Bringing them home costs salaries well above the civil service "
          "scale, which the unions resent.",
          ('science', 'telescope'), after=('cen_ledger',), reward=(Idea('applied_institutes'),)),
    Focus('cen_radio_relay', 'Radio Relays to Every District',
          "District offices still rely on telephone lines strung along roads that did not exist ten years ago. A national radio "
          "relay network, with masts on the mountains of District J and the ridges of District H, links every district office, "
          "depot and post without wires. Weather and terrain make the work slow. Once finished, a storm no longer cuts "
          "District C off from the news.",
          ('communications', 'satellite'), after=('cen_institutes',), reward=(Research('electronics', 0.5, 2), Stability(0.01))),
    Focus('cen_export_fund', 'What the Crude Bought',
          "A decade of crude sold abroad has paid down debt and bought machinery, but it has also tied the budget to world "
          "prices. The commission recommends a stabilisation fund that saves export revenue in good years and spends it in bad "
          "ones. Ministers lose the freedom to spend windfalls. The country gains a cushion against the next price collapse.",
          ('economy', 'scales'), after=('cen_ledger',), requires=(HasFlag('model_export'),),
          reward=(SwapIdea('fuel_export', 'export_fund'),)),
    Focus('cen_chemicals', 'What the Refineries Built',
          "A decade of refining at home has made Glaceland self-sufficient in fuel for its plants, army and navy, but the "
          "refineries need modernising and their chemicals business is small. The commission recommends plastics and "
          "fertiliser lines to use the by-products. The work is technical and unglamorous, and it keeps the oil districts "
          "employed for another generation.",
          ('industry', 'science'), after=('cen_ledger',), requires=(HasFlag('model_refine'),),
          reward=(SwapIdea('home_refining', 'chemical_lines'),)),
    Focus('cen_usean_war', 'Freight Rates and the Usean War',
          "When the ISAF coalition is formed to oppose Erusea, the war is not Glaceland's, but freight rates, insurance "
          "premiums and fuel prices move within days. Merchant owners ask whether to keep sailing distant routes. The "
          "government sets up a freight watch to advise shippers and track prices, and the foreign ministry repeats at every "
          "briefing that Glaceland takes no side.",
          ('logistics', 'communications'), after=('cen_ledger',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Event('usean_war'),)),
))

BRANCHES = (ADMIN, DISTRICTS, TREASURY, COAST, ISLAND, ARMY, AIR, ULYSSES, FRONTIER, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('summer_road_season', 'A Summer Road Season in District J',
                'Pay for one extra summer of road crews on the District J mountain route, once the district survey exists.',
                50, (Build('infrastructure', 1, 576), Stability(0.01)), requires=(HasFlag('districts_surveyed'),)),
    DecisionDef('ferry_fares', 'Subsidise the District C Ferries',
                'Pay part of every District C ferry ticket for a year; it can be renewed each year.',
                30, (TimedIdea('ferry_subsidy', 365),), requires=(Completed('isl_crossing'),), cooldown=365),
    DecisionDef('fuel_draw', 'Draw on the Strategic Stock',
                'Release fuel from the second depot for a season of exercises; the stock refills before it can be drawn again.',
                25, (TimedIdea('fuel_drawdown', 120),), requires=(Completed('tre_second_depot'),), cooldown=240),
    DecisionDef('coast_exercise', 'A Combined Coast Exercise',
                'Run the navy and air arm through a joint exercise along the coastal districts; it can be repeated each year.',
                35, (XP('navy', 20), XP('air', 10)), requires=(HasFlag('coast_command_set'),), cooldown=365),
    DecisionDef('district_accounts', 'Publish the District Accounts',
                'Publish what every district received and spent since the survey; a one-time act of transparency.',
                40, (Stability(0.03), PP(10)), requires=(Completed('dis_survey'),)),
    DecisionDef('sky_drill', 'A National Sky-Watch Drill',
                'Rehearse the Ulysses warning procedures in every district; it can be repeated each year.',
                25, (WarSupport(0.02), Stability(0.01)), requires=(Completed('uly_bulletin'),), cooldown=365),
)
