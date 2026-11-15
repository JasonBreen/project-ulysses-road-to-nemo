"""Kaluga (KLG): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party at 61
percent popularity governing through a National Administration with elections suspended),
the unnamed starting office, the five 1991 states with their buildings, resources and neutral
captions, the map facts read from map/definition.csv, map/provinces.bmp and map/railways.txt,
the two Yuktobanian-held states that carry Kalugan cores in inherited history, and the global
flags other mod scripts already set. Official: ACES Chronicle rows used only as date anchors
for distant pressures, each cited by its exact key. Everything else, including every Kalugan
choice, office, idea, building, decision and event, is provisional gameplay built on the
world-start role of limited coastal defence.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='KLG', name='Kaluga', root='world', package='klg',
                  themes=('rail', 'navy', 'ballot'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities democratic 61, neutrality 20, communism 11, fascism 8; stability and war support 0.5; three research '
           'slots; technology including tech_mountaineers, tech_engineers, early_fighter and basic_train; grand doctrines '
           'superior_firepower, fleet_in_being and operational_integrity. The starting leader is the unnamed National '
           'Administration office (KLG_ac_government_office, centrism), whose description says its 1991 holder has not been '
           'established. Country names Republic of Kaluga (democratic and neutrality). The tree never names a holder.',
           'mod/2985041246/history/countries/KLG - Kaluga.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; tools/world_foundation/country_registry.json '
           '(KLG row: civil_administration, capacity 40)'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role limited coastal defense; 6 civilian, 5 military and 2 naval '
           'factories; 4 infantry formations (6 battalions) with replacement-backed engineers; 24 fighters on the single '
           'capital air base with 6 in reserve; one destroyer (the KLG Coastal Escort variant); 60 convoys; 2 supply centres; '
           'research priority Physical Sustainment (transport, equipment replacement, affordable service). Fiscal profile GDP '
           '100, debt ratio 0.3, collection 0.85, growth 3, inflation 2 is fictional gameplay calibration, not national '
           'accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 23 (capital, large city, captioned Kaluga Capital District; victory point Kaluga Capital '
           'Centre 1721; naval base 3 at province 1890; 2 civilian, 2 military, 2 dockyards, air base 1, fuel silo 1; steel 7, '
           'aluminium 4, oil 2, rubber 2), 73 (Kaluga District B; forest 6, plains 3, hills 1, marsh 1; no buildings, '
           'infrastructure or resources), 138 (forest 11, marsh 3; 2 civilian, 1 military; steel 6, aluminium 3, oil 2, rubber '
           '1), 569 (plains 10, hills 1, mountain 1; 2 civilian, 2 military; logistics centre at 1858; steel 6, aluminium 3, oil '
           '2, rubber 2) and 570 (Kaluga District E; plains 9, hills 1, mountain 1; no buildings, infrastructure or resources). '
           'States 138 and 569 keep inherited Earth-template names, which this tree does not use; all five states are called by '
           'function in the text. Every state is coastal. Railways (map/railways.txt): level-2 lines 1721 to 1858 through 570, '
           '1721 to 9645 through 73, and the capital spur to 1890; no line crosses a frontier. Land neighbours from '
           'map/provinces.bmp: Silvonia (23, 73, 569, 570), Luremia (73, 138), Glaceland (138), Romny (569) and Yuktobania '
           '(569, via its state 515). No other place is named.',
           'mod/2985041246/history/states/23-State_23.txt and the four other KLG state files; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt'),
    Source('Mod provenance',
           'Yuktobanian-owned states 515 and 555 carry add_core_of = KLG in inherited history, and the world-start calibration '
           'keeps their identities. The tree treats them only as a question of how the republic speaks about its old '
           'registers: no claim, core, border, war or ownership effect anywhere.',
           'mod/2985041246/history/states/515-State_515.txt; mod/2985041246/history/states/555-State_555.txt; '
           'docs/WORLD_STARTS_CALIBRATION.md'),
    Source('Mod provenance',
           'Neighbour consistency: Glaceland (tools/world_depth/gla/content.py) describes the Kaluga frontier as a short '
           'mountain stretch of its District J and offers a frontier telephone line; Silvonia (tools/world_depth/esn/content.py) '
           'faces Kaluga with hill and mountain districts and has no agreed airspace line with any neighbour. This tree acts '
           'only on the Kalugan side and claims no action, consent or outcome for any neighbour.',
           'tools/world_depth/gla/content.py; tools/world_depth/esn/content.py'),
    Source('Official',
           'Date anchor: Yuktobania announces a new class of submarine to the world. Premise of the submarine watch focus; no '
           'Kalugan role is claimed and no person is named.', '1991 / 09.02'),
    Source('Official',
           'Date anchor: the International Astronomical Union announces that Ulysses will pass close to Earth with a chance of '
           'impact. Opens the Ulysses branch; no Kalugan role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Gate of the distant-war focus; Kaluga takes no part.', '1995 / 03.25'),
    Source('Official',
           'Date anchor: the President of the FCU announces that Ulysses will impact the Earth. Gate of the impact focus; '
           'where fragments fall is never stated for Kaluga.', '1996 / 04.20'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit. Gate of the Roche-limit focus.', '1999 / 07.08'),
    Source('Official',
           'In 1999 Ulysses strikes the Usean continent and inflicts catastrophic damage; used only as distant news in the '
           'Roche-limit focus. No fall in or near Kaluga is claimed.', 'Abstracts, ACE COMBAT 04: shattered skies'),
    Source('Official',
           'The Arkbird is a joint Osean and Yuktobanian project to clear fragments of Ulysses; premise of the debris watch '
           'focus, which claims no Kalugan part in it.', 'Super Weapons, Arkbird'),
    Source('Official',
           'Date anchor: Osea and Yuktobania cooperate to convert the Arkbird into a debris-clearing platform. Gate of the '
           'thaw focus, read as a change in the climate for a small neighbour of Yuktobania.', '1999 / 10.08'),
    Source('Official',
           'Date anchor: the FCU establishes the ISAF. The focus that reacts to it waits for the mod flag ac_ucw_isaf_formed '
           'and claims no Kalugan part in the war.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Kalugan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the locked calendar
    IdeaDef('suspended_calendar', 'The Locked Calendar',
            'A popular majority party gives its name to an Administration that has not faced a vote.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('ballot', 'document')),
    IdeaDef('decree_gazette', 'The Decree Gazette', 'Every decree issued since the suspension is printed and indexed.',
            {'political_power_factor': 0.04, 'stability_factor': 0.02}, ('document', 'communications')),
    IdeaDef('election_writ', 'The Election Writ', 'A fixed date for elections to a single chamber.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('presidential_charter', 'The Presidential Charter', 'A draft charter for a directly elected president.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('medal', 'ballot')),
    IdeaDef('caretaker_mandate', 'Administration on Probation', 'The Administration governs on published targets while the vote waits.',
            {'political_power_gain': 0.15, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('chamber_committees', 'Committees of the Chamber', 'Standing committees read every large contract.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05}, ('assembly', 'scales')),
    IdeaDef('direct_mandate', 'Government by Order', 'The president governs through countersigned orders.',
            {'political_power_gain': 0.15, 'war_support_factor': 0.04}, ('medal', 'command')),
    IdeaDef('standing_council', 'The Quarterly Sheet', 'Targets and results for every ministry, published each quarter.',
            {'political_power_factor': 0.08, 'production_factory_efficiency_gain_factor': 0.03}, ('document', 'scales')),
    IdeaDef('labour_compact', 'The Mill Compact', 'Wage rounds and inspections agreed with the unions; no sudden strikes.',
            {'stability_factor': 0.05, 'industrial_capacity_factory': -0.03}, ('tools', 'assembly')),
    # the line
    IdeaDef('spine_timetable', 'One Timetable', 'Every train on the line runs to a single published timetable.',
            {'production_speed_infrastructure_factor': 0.10}, ('rail', 'document')),
    IdeaDef('settler_credit', 'Settler Credit', 'Cheap loans and fares for families moving to the empty districts.',
            {'production_speed_infrastructure_factor': 0.10, 'production_speed_industrial_complex_factor': 0.08}, ('civil', 'rail')),
    IdeaDef('reserve_leases', 'Reserve Land Leases', 'Timber, peat and grazing leases on state land along the line.',
            {'production_speed_infrastructure_factor': 0.12, 'political_power_gain': 0.05}, ('economy', 'rail')),
    IdeaDef('freight_tariff', 'The Flat Freight Tariff', 'One price per tonne and kilometre from end to end.',
            {'production_factory_efficiency_gain_factor': 0.03, 'supply_consumption_factor': -0.03}, ('rail', 'economy')),
    # steel
    IdeaDef('mill_census', 'The Furnace Census', 'Every furnace, stand and pit counted and costed.',
            {'production_factory_max_efficiency_factor': 0.02}, ('industry', 'document')),
    IdeaDef('ingot_exports', 'Ingots for Export', 'Plain ingots shipped from the capital harbour on long contracts.',
            {'consumer_goods_factor': -0.04, 'production_speed_buildings_factor': 0.05}, ('economy', 'navy')),
    IdeaDef('rolled_at_home', 'Rolled at Home', 'Sheet, rail and wire finished inside the country under protection.',
            {'industrial_capacity_factory': 0.05, 'production_factory_max_efficiency_factor': 0.03}, ('industry', 'tools')),
    IdeaDef('hull_plate', 'Hull Plate Contracts', 'The mills roll marine plate for the capital yards.',
            {'industrial_capacity_dockyard': 0.08, 'production_speed_buildings_factor': 0.03}, ('navy', 'industry')),
    IdeaDef('mill_credit', 'The Mill Bank', 'State credit against mill order books, with open accounts.',
            {'production_speed_industrial_complex_factor': 0.10, 'political_power_gain': -0.05}, ('economy', 'industry')),
    IdeaDef('light_alloy', 'Light Alloy Works', 'Home aluminium cast into frames and parts for the arms works.',
            {'production_speed_arms_factory_factor': 0.08, 'research_speed_factor': 0.02}, ('industry', 'science')),
    IdeaDef('fuel_book', 'The Fuel Book', 'Every barrel from six small fields allocated in one ledger.',
            {'supply_consumption_factor': -0.05, 'stability_factor': -0.01}, ('logistics', 'document')),
    IdeaDef('price_floor', 'A Floor Under Steel', 'A guaranteed minimum price for mill output this season.',
            {'stability_factor': 0.02, 'production_factory_efficiency_gain_factor': 0.02}, ('scales', 'industry')),
    # the harbour
    IdeaDef('harbour_board', 'The Harbour Board', 'One board for berths, pilots, dredging and the naval quay.',
            {'naval_coordination': 0.03, 'stability_factor': 0.01}, ('navy', 'command')),
    IdeaDef('submarine_watch', 'Watch on the Approaches', 'Listening buoys and fishing-boat reports on every approach.',
            {'naval_coordination': 0.05, 'air_detection': 0.05}, ('submarine', 'radar')),
    IdeaDef('mine_flotilla', 'Mines and Fast Boats', 'Controlled minefields and a patrol flotilla guard the harbour.',
            {'naval_coordination': 0.08, 'navy_org_factor': 0.04}, ('navy', 'security')),
    IdeaDef('escort_pair', 'The Escort Squadron', 'Three escorts: one at sea, one in refit, one training.',
            {'navy_org_factor': 0.06, 'naval_speed_factor': 0.05}, ('navy', 'logistics')),
    IdeaDef('fishery_patrol', 'The Fishery Patrol', 'Cutters and boarding crews on every coast.',
            {'stability_factor': 0.03, 'naval_coordination': 0.03}, ('fishing', 'security')),
    IdeaDef('convoy_pool', 'The Convoy Pool', 'Every Kalugan hull, crew and cargo on one list.',
            {'supply_consumption_factor': -0.04, 'naval_speed_factor': 0.03}, ('logistics', 'navy')),
    # the army
    IdeaDef('four_formations', 'One Staff, Four Formations', 'A single staff, supply office and training plan.',
            {'army_org_factor': 0.03, 'planning_speed': 0.05}, ('command', 'training')),
    IdeaDef('territorial_companies', 'District Companies', 'Local companies in every district, trained on their own ground.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.08}, ('security', 'civil')),
    IdeaDef('field_brigade', 'The Railway Brigade', 'One concentrated brigade able to reach any district in a day.',
            {'army_attack_factor': 0.04, 'army_speed_factor': 0.05, 'experience_gain_army_factor': 0.06}, ('rail', 'training')),
    IdeaDef('engineer_school', 'The Engineer School', 'Bridge, rail and demolition specialists for every formation.',
            {'production_speed_infrastructure_factor': 0.05, 'army_org_factor': 0.03}, ('tools', 'training')),
    IdeaDef('spares_depots', 'Spares Depots', 'Barrels, tyres, radios and engine parts held beside the railway.',
            {'supply_consumption_factor': -0.05, 'repair_speed_factor': 0.10}, ('logistics', 'tools')),
    IdeaDef('forest_fieldcraft', 'Forest Fieldcraft', 'Infantry trained in marsh, forest and winter living.',
            {'attrition': -0.05, 'army_defence_factor': 0.04}, ('training', 'security')),
    # the air arm
    IdeaDef('single_field', 'Thirty Aircraft on One Apron', 'Every fighter in the republic flies from a single field.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('interceptor_watch', 'Interceptor Watch', 'Fighters trained first to defend the capital sky.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'security')),
    IdeaDef('sea_patrol_wing', 'Sea Patrol Wing', 'Fighters trained to patrol the sea lanes with the coast command.',
            {'air_mission_efficiency': 0.06, 'naval_coordination': 0.04}, ('air', 'navy')),
    IdeaDef('observer_corps', 'Listeners on the Hills', 'Volunteer observers report every engine they hear.',
            {'air_detection': 0.10, 'static_anti_air_damage_factor': 0.05}, ('telescope', 'security')),
    IdeaDef('pilot_ladder', 'The Pilot Ladder', 'Gliding clubs to fighter conversion, with bonded service.',
            {'experience_gain_air_factor': 0.10, 'training_time_factor': -0.05}, ('training', 'air')),
    # the neighbours
    IdeaDef('frontier_staff', 'The Frontier Staff', 'One staff in the capital follows all five land frontiers.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('diplomacy', 'document')),
    IdeaDef('timber_accord', 'The Timber Accord', 'Agreed rules for logs, replanting and fire watch on the forest frontier.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.02}, ('diplomacy', 'tools')),
    IdeaDef('quiet_registers', 'Quiet Registers', 'The old registers rest in the archive; ministers decline questions.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('document', 'peace')),
    IdeaDef('open_registers', 'Registers on the Record', 'An annual statement notes the old registers without demands.',
            {'war_support_factor': 0.04, 'political_power_gain': 0.05}, ('document', 'medal')),
    IdeaDef('big_market', 'The Big Market Next Door', 'Long export contracts across the Yuktobanian frontier.',
            {'consumer_goods_factor': -0.05, 'production_speed_buildings_factor': 0.04}, ('economy', 'gate')),
    IdeaDef('spread_orders', 'Orders Among Five', 'No neighbour may take more than a fixed share of exports.',
            {'stability_factor': 0.04, 'political_power_factor': 0.04}, ('scales', 'diplomacy')),
    IdeaDef('distant_war_watch', 'A Distant War', 'Higher insurance, dearer fuel and a tighter coast watch.',
            {'war_support_factor': 0.03, 'army_core_defence_factor': 0.04}, ('communications', 'security')),
    IdeaDef('market_days', 'Market Days at the Halls', 'Reduced duties at the customs halls for a season.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('gate', 'economy')),
    # the asteroid
    IdeaDef('sky_bulletin', 'The Weekly Sky Digest', 'A weekly digest of international data on the asteroid.',
            {'stability_factor': 0.02}, ('meteor', 'communications')),
    IdeaDef('cellar_shelters', 'Cellars and Cuttings', 'Reinforced cellars and fitted railway cuttings in every town.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'rail')),
    IdeaDef('dispersal_plan', 'Trains Out of the Capital', 'Trains, routes and reception places for leaving the capital.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('refugees', 'rail')),
    IdeaDef('grain_reserve', 'The Two-Winter Store', 'Grain, salt and preserved fish stored in every district.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.02}, ('economy', 'shelter')),
    IdeaDef('evac_rehearsal', 'Boats on Standby', 'Lifeboat crews on a standby rota for the impact years.',
            {'stability_factor': 0.03, 'naval_coordination': 0.03}, ('medical', 'navy')),
    IdeaDef('calm_broadcasts', 'Calm on the Airwaves', 'Plain instructions repeated every hour on every station.',
            {'stability_factor': 0.04, 'war_support_factor': -0.02}, ('communications', 'civil')),
    IdeaDef('debris_watch', 'The Debris Watch', 'Observers, radar crews and international data watch for falling debris.',
            {'air_detection': 0.05, 'stability_factor': 0.03}, ('meteor', 'radar')),
    # the ledger years
    IdeaDef('national_ledger', 'The National Ledger', 'One statistical office and one set of definitions.',
            {'political_power_factor': 0.05, 'research_speed_factor': 0.03}, ('document', 'economy')),
    IdeaDef('data_exchange', 'The Data Exchange', 'The ministries share figures over leased lines.',
            {'research_speed_factor': 0.04, 'planning_speed': 0.05}, ('communications', 'science')),
    IdeaDef('thaw_trade', 'Trade in the Thaw', 'Cheaper credit and longer contracts in a calmer decade.',
            {'production_speed_buildings_factor': 0.05, 'consumer_goods_factor': -0.03}, ('economy', 'peace')),
    IdeaDef('shipping_cover', 'Wartime Shipping Cover', 'State reinsurance for freighters trading toward a war zone.',
            {'consumer_goods_factor': -0.03, 'naval_coordination': 0.03}, ('logistics', 'scales')),
    IdeaDef('coast_plan', 'The Coast Programme', 'The next programme spends first on harbour, yards and escorts.',
            {'industrial_capacity_dockyard': 0.06, 'navy_org_factor': 0.05}, ('navy', 'document')),
    IdeaDef('interior_plan', 'The Interior Programme', 'The next programme spends first on roads, towns and frontier works.',
            {'production_speed_infrastructure_factor': 0.12, 'army_core_defence_factor': 0.05}, ('civil', 'document')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('chamber_cabinet', 'Cabinet of the Kalugan Chamber',
           'A cabinet chosen by the largest bloc in a newly elected single chamber, governing collectively and defending every '
           'budget on the floor of the house. Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
    Office('elected_presidency', 'Office of the Elected President',
           'A president chosen by direct national vote for a fixed term, heading a small cabinet office, with a chamber that '
           'passes and amends the budget. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism', elections=True),
    Office('admin_council', 'Standing Council of Administrators',
           'A council of senior administrators with fixed terms and published quarterly targets, governing while the election '
           'calendar stays suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('no_ballot', 'Six in Ten, and No Vote', (
        "The survey commissioned by the National Administration lands on ministers' desks in a plain grey cover. Six "
        "citizens in ten back the democratic party whose colours the Administration wears. A fifth would rather be governed "
        "by non-party administrators. About one in nine supports the labour socialists, and fewer than one in ten the "
        "nationalist circle. On paper the republic has a clear majority. In law it has no date on which that majority may vote.",
        "The figures cut in two directions at once. The majority party's own branches ask why a government that borrows "
        "their name keeps the calendar locked. The Administration's senior officials answer that they have kept the railway, "
        "the yards and the mills running through lean years, and that a campaign now would turn every budget line into a "
        "slogan. Both sides quote the same tables, often on the same page.",
        "Before anyone can decide what the republic should become, the Administration must decide what to do with the survey "
        "itself. Publishing it in full would put the question to the whole country at once. Circulating it only inside the "
        "ministries would buy a season of quiet and confirm every suspicion about who really governs Kaluga.",
    ), (
        Option('Publish every table.', (Stability(0.02), PP(-20))),
        Option('Keep it inside the ministries.', (PP(40), Stability(-0.02))),
    ), picture=2),
    EventDef('one_line', 'A Report on the Line', (
        "The survey team returns from the railway with photographs, soil samples and a list of every structure between the "
        "forest mills and the junction works. The line is level-two track nearly everywhere: sound enough for the traffic of "
        "1991 and not a wagon more. Bridges over the marsh streams carry weight limits nobody enforces. The passing loops on "
        "the plains are too far apart, and the capital yard is the worst bottleneck of all.",
        "The report also describes what the line passes through. Between the capital and the forest mills lie woods and "
        "marsh with no road, no halt and no factory. Between the capital and the junction lie open plains in the same "
        "condition. Two of the republic's five districts are, in practical terms, scenery seen from a carriage window, and "
        "the few people who live there reach the state by walking to the track.",
        "Ministers must choose where the first money goes. The railway's engineers want the capital yard rebuilt before "
        "anything else. District councils want halts and loops so that someone can finally board a train in the empty "
        "districts. The treasury wants one figure and one programme, and would prefer both to be small.",
    ), (
        Option('The capital yard comes first.', (Research('train_tech', 0.5, 1),)),
        Option('Start with the empty districts.', (Stability(0.02), PP(-10))),
    ), picture=0),
    EventDef('three_furnaces', 'Three Districts, One Steel Trade', (
        "The furnace census counts every blast furnace, converter, rolling stand and ore pit in the republic. The capital "
        "district smelts the most, from ore that arrives by rail and coke that arrives by sea. The forest mill district runs "
        "smaller furnaces on its own ore, with boilers older than the Administration. The junction works beside the "
        "logistics centre combine a modest steelworks with the busiest arms plants in the country.",
        "What the census finds is not one industry but three, each with its own buyers, debts and habits. Nearly all of "
        "their output leaves as plain ingots, and nearly every finished steel product the republic uses is bought abroad. "
        "Aluminium follows the same pattern on a smaller scale. The mill owners blame freight costs, the railway blames the "
        "owners, and the ministry blames both in the same memorandum.",
        "Three schools are already circulating proposals: sell more ingots abroad, build rolling stands to finish steel at "
        "home, or turn the mills toward plate for the capital's two yards. Before they argue, the ministry must decide how "
        "hard to press the owners who hid figures from its inspectors.",
    ), (
        Option('Fine the owners who hid figures.', (Stability(-0.01), Research('industry', 0.5, 1))),
        Option('Let the census close the matter.', (PP(25),)),
    ), picture=0),
    EventDef('one_harbour', 'Three Logbooks, One Harbour', (
        "The harbour board's first inspection finds the capital harbour run by three authorities at once. The transport "
        "ministry assigns berths, the navy controls the naval quay and the dredged channel, and the trade ministry licenses "
        "pilots and tugs. Each keeps its own logbook. A freighter waiting for a berth can be told to move by one office and "
        "to stay put by another on the same afternoon.",
        "The harbour matters far more than its size suggests. It holds the republic's only naval base, both of its yards, "
        "the fuel silo and almost all of its merchant traffic. The lone escort and the patrol craft share quays with ore "
        "carriers and fishing boats. Every district touches the sea, but none of the other four has a naval base or a yard, "
        "so whatever happens to this harbour happens to the whole country's trade.",
        "The board can take over everything at once and face three angry ministries, or take berths and pilots first and "
        "leave the naval quay to the navy for now. The navy has already sent a long letter explaining why its quay is a "
        "special case.",
    ), (
        Option('Take everything at once.', (PP(-25), XP('navy', 10))),
        Option('Leave the naval quay to the navy for now.', (PP(15),)),
    ), picture=1),
    EventDef('long_frontier', 'Four Formations, Five Frontiers', (
        "The general staff's first readiness report is short and blunt. The army consists of four infantry formations with "
        "attached engineers, stocked with enough rifles, trucks and support equipment for its present size. All of them are "
        "based near the capital or along the railway. None of them is anywhere near most of the republic's land frontiers, "
        "which run for long stretches through woods, marsh and open plain.",
        "Silvonia faces four of the five districts, its side of the line rising into hill country. Luremia faces the woods, "
        "Glaceland a short stretch beyond the forest mills, and Romny and Yuktobania meet the junction district. None of "
        "these neighbours is hostile today. The report notes only that if one of them ever were, the army could defend the "
        "capital or one district, but never both at once.",
        "Two schools of officers draw opposite conclusions. One wants the formations broken into district companies so that "
        "every frontier has someone watching it. The other wants them gathered into one brigade on the railway, able to "
        "reach any district within a day. Before choosing, the staff must decide whether its report goes to the public or "
        "stays inside the army.",
    ), (
        Option('Publish the report.', (WarSupport(0.02), PP(-10))),
        Option('Keep it inside the staff.', (XP('army', 15),)),
    ), picture=0),
    EventDef('one_runway', 'Thirty Aircraft, One Strip of Concrete', (
        "The air staff's report opens with a single photograph: the capital airfield at dawn, every fighter in the republic "
        "lined up on one apron. Twenty-four aircraft are in service and six more stand in reserve. They share one runway, one "
        "fuel farm, one control tower and one repair hangar. The photograph was taken to impress visitors. Read beside the "
        "report, it alarms them.",
        "The report lists what could close the field: a fuel fire, a crashed aircraft on the runway, a storm that floods the "
        "taxiways, or an attack. Any of them would ground the whole air arm for days. Pilots fly too few hours because fuel "
        "is tight, and several of the best have already left for airline cockpits abroad, taking years of training with "
        "them.",
        "The air staff asks for three things: a second airfield, more flying hours and a clear decision on what the fighters "
        "are for. The treasury can fund one of the three this year. The navy, which wants the fighters over the sea, and the "
        "capital, which wants them overhead, have both begun to lobby, each with a map of its own.",
    ), (
        Option('Fund flying hours first.', (XP('air', 15),)),
        Option('Save for a second field.', (PP(20),)),
    ), picture=1),
    EventDef('five_frontiers', 'Five Neighbours on One Map', (
        "The foreign ministry's new frontier staff pins its first map to the wall. Silvonia runs along four of the five "
        "districts, the longest frontier by far. Luremia faces the woods and the forest mills. Glaceland touches a short "
        "stretch beyond the forest mills. At the junction district, Romny and Yuktobania meet Kaluga within a short distance "
        "of the logistics centre. No railway crosses any of these lines.",
        "The files behind the map are thin. Customs posts report to the finance ministry, frontier police to the interior "
        "ministry, and the army keeps its own notes. Local officials have settled countless small matters, from stray cattle "
        "to lost travellers, without telling anyone in the capital. Two districts held by Yuktobania still appear in "
        "inherited registers as Kalugan, a fact every minister knows and none mentions aloud.",
        "The staff's first recommendation concerns who should own the frontiers in future. Placed under the foreign "
        "ministry, they would be handled as diplomacy, by people trained to avoid incidents. Placed under the interior "
        "ministry, they would be handled as policing, by people trained to stop smuggling. Each ministry has already sent "
        "its case.",
    ), (
        Option('The foreign ministry owns the frontiers.', (Stability(0.02),)),
        Option('The interior ministry owns the frontiers.', (PP(20), WarSupport(0.01))),
    ), picture=2),
    EventDef('warning_star', 'A Warning from the Astronomers', (
        "The astronomers' warning of December 1994 reaches Kaluga on a foreign wire in the small hours: Ulysses, an asteroid "
        "found that autumn, will pass near the Earth and might hit it. By breakfast the capital's radio stations are reading "
        "out distances and percentages that nobody in the studio can explain. Shops near the harbour sell out of candles "
        "and tinned fish before noon, and the queues are quiet rather than angry.",
        "The republic has no observatory able to follow the asteroid and no scientists who can confirm or dispute what the "
        "wire services say. University physicists can read the international data, but slowly. District councils telephone "
        "the capital for instructions that nobody has written. The railway asks whether it should plan for evacuations, and "
        "the harbour board asks the same question about ships. Teachers want to know what to tell their classes on Monday.",
        "The government must decide how to speak. It can publish a weekly bulletin of whatever the international bodies "
        "release, plainly and without comment, or say little until the picture is clearer and avoid feeding fear. Silence "
        "is easier for a week and much harder for a year.",
    ), (
        Option('Publish everything plainly every week.', (Stability(0.02), PP(-15))),
        Option('Say little until the figures are clear.', (PP(25), Stability(-0.02))),
    ), picture=0),
    EventDef('impact_year', 'The Year the Impact Was Confirmed', (
        "The April 1996 statement from the President of the FCU leaves no room for hope that Ulysses will miss. It offers "
        "nothing a Kalugan minister can use about where the fragments will come down, or in which month. Within days the "
        "capital's banks see queues, filling stations ration petrol, and families in the plains and woods districts write "
        "to relatives in the capital offering spare rooms.",
        "Ministers meet every day. The railway reports that it could move tens of thousands of people out of the capital in "
        "a week if it stopped carrying freight. The army's engineers report that the deep cuttings on the forest line could "
        "shelter a few thousand. The treasury reports that it cannot pay for everything at once and that lenders are "
        "already nervous about a small country's bonds.",
        "Two proposals reach the cabinet table within the month: concrete shelters in every town, or plans to disperse the "
        "capital by rail. Before choosing, ministers can order a full count of every cellar, cutting and public building "
        "that could serve as shelter, which would take a month, or decide on what they already know and start digging "
        "at once.",
    ), (
        Option('Order the shelter count.', (PP(-10), Event('shelter_count', 30))),
        Option('Decide on what we know.', (PP(20), Stability(-0.02))),
    ), picture=0),
    EventDef('shelter_count', 'What the Shelter Count Found', (
        "The shelter count comes back after a month of inspectors climbing into cellars and walking the railway cuttings. "
        "The capital has hundreds of cellars, most of them damp and unreinforced, and a handful of public buildings with "
        "basements deep enough to matter. The cuttings on the forest line are better than anyone expected. The plains and "
        "woods districts have almost nothing, because they have almost no buildings at all.",
        "The count also finds something the cabinet never asked about. Dozens of private firms and better-off households "
        "have already dug their own shelters, a few of them excellent and most of them unregistered. At the junction, a "
        "cooperative of rail workers has roofed a disused goods cutting at its own expense. Inspectors report more goodwill "
        "and more improvisation than any plan had assumed, and rather less paperwork than the law requires.",
        "Ministers can register the private shelters and open them to the public in an emergency, adding space quickly and "
        "angering their owners, or leave them alone and build public shelters from scratch. Either way, the shelter and "
        "dispersal schools now have real numbers to argue over, and neither will like all of them.",
    ), (
        Option('Register private shelters for public use.', (Stability(0.02), PP(-15))),
        Option('Leave them be and build our own.', (PP(10), WarSupport(0.01))),
    ), picture=0),
    EventDef('ledger_years', 'Ten Years of Figures', (
        "The new statistical office publishes its first national ledger, gathering a decade of figures that ministries had "
        "kept in their own drawers. Rail tonnage, steel output, fishery catches, harbour calls, school places and clinic "
        "visits appear side by side for the first time, measured the same way. Some figures flatter the republic. Others "
        "show that the empty districts are still largely empty, whatever the settlers and leaseholders were promised.",
        "The ledger settles arguments that have run for years. It shows which mills earned their credit and which did not, "
        "how much freight the line really carries and how many ships the convoy pool actually controls. It also shows that "
        "every ministry has been counting slightly differently, and that some returns were optimistic in ways that can no "
        "longer be hidden.",
        "The government must decide what to do with the uncomfortable pages. Publishing the whole ledger would expose "
        "ministries and contractors who padded their returns. Publishing only national totals would protect reputations and "
        "leave the arguments open. The next programme will be built on whichever version the republic chooses to believe, "
        "and the statisticians have already said which one they would sign.",
    ), (
        Option('Publish the whole ledger.', (Stability(-0.01), Research('industry', 0.5, 1))),
        Option('Publish the totals only.', (PP(30),)),
    ), picture=2),
)

# --- branches ------------------------------------------------------------------------------------
POLITICS = Branch('politics', 'A Majority Without a Ballot', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_count', 'Count the Silent Majority',
          "Kaluga enters 1991 governed by a National Administration that wears the democratic party's colours while the "
          "election calendar stays locked. Unlike its neighbours, that party is genuinely popular: six citizens in ten back "
          "it. Commissioning an honest public survey of its support is cheap, but it turns a quiet embarrassment into a "
          "published fact the Administration must then answer.",
          ('ballot', 'document'), reward=(Idea('suspended_calendar'), Event('no_ballot'))),
    Focus('pol_roll', 'An Electoral Roll from Nothing',
          "No national electoral roll has been kept since the calendar was locked. Clerks must register voters in the "
          "capital, the two mill districts and the two empty districts, where some hamlets can be reached only by rail and "
          "footpath. The roll takes a year and a great deal of overtime. Without it, every later promise about a ballot "
          "remains talk.",
          ('document', 'rail'), after=('pol_count',), reward=(Flag('roll_compiled'), PP(-15))),
    Focus('pol_minority', 'Hearings for the Other Four in Ten',
          "Four citizens in ten do not back the majority party: a fifth want non-party administrators, about one in nine "
          "leans to the labour socialists, and a small nationalist circle complains loudest. Public hearings in every "
          "district give them a formal voice before any constitution is drafted. They cost time and patience, and take the "
          "sting out of later charges of a rigged settlement.",
          ('assembly', 'scales'), after=('pol_count',), reward=(Flag('minority_heard'), Stability(0.02))),
    Focus('pol_gazette', 'Print Every Decree Since 1991',
          "Since the vote was locked away, the Administration has governed by decree, and many decrees were never printed. "
          "A gazette gathers every one of them into public volumes, from tariff changes to officer appointments. Some read "
          "badly in daylight. Printing them ends the rumour trade and gives the courts a text to work from, at the price of "
          "a bruising month in the press.",
          ('document', 'communications'), after=('pol_count',), reward=(Idea('decree_gazette'),)),
    Focus('pol_writ', 'Fix a Date for the Chamber',
          "The majority party's own members want the simplest answer: a fixed date for elections to a single chamber, which "
          "would then choose a cabinet. Their party would probably win, and its rivals know it. Setting the date reassures "
          "lenders and neighbours that the republic means its name, and binds the Administration to surrender the seals on "
          "a day it cannot move.",
          ('ballot', 'assembly'), after=('pol_roll',), exclusive=('pol_presidency', 'pol_caretaker'),
          requires=(HasFlag('roll_compiled'),), reward=(SwapIdea('suspended_calendar', 'election_writ'),)),
    Focus('pol_presidency', 'A President Chosen by Every Voter',
          "A second camp inside the majority party fears a chamber of quarrelling factions in a country this small. It "
          "proposes a president elected directly by the whole country for a fixed term, with a weaker chamber to pass the "
          "budget. The office would be strong and visible. It would also let one election decide almost everything for "
          "years at a stretch.",
          ('medal', 'ballot'), after=('pol_roll',), exclusive=('pol_writ', 'pol_caretaker'),
          reward=(SwapIdea('suspended_calendar', 'presidential_charter'),)),
    Focus('pol_caretaker', 'The Administration Stays at Its Desk',
          "The non-party camp argues that the Administration already runs the line, the yards and the mills competently, and "
          "that an election now would only reward slogans. It proposes a standing council of senior administrators that "
          "governs on published targets while the calendar stays locked. The majority party would be furious, and six "
          "citizens in ten would remember who silenced them.",
          ('command', 'document'), after=('pol_roll',), exclusive=('pol_writ', 'pol_presidency'),
          reward=(SwapIdea('suspended_calendar', 'caretaker_mandate'),)),
    Focus('pol_chamber_regime', 'Seat the First Elected Chamber',
          "Polling day passes without serious incident, and the new chamber chooses a cabinet from its largest bloc. The "
          "cabinet governs collectively and must defend every budget on the floor of the house. Officials who answered only "
          "to the Administration for years now take instructions from ministers who campaigned against them, and the first "
          "months are tense on both sides of every desk.",
          ('assembly', 'ballot'), after=('pol_writ',), cost=10,
          exclusive=('pol_president_regime', 'pol_council_regime'), reward=(Regime('chamber_cabinet'),)),
    Focus('pol_president_regime', 'Swear In the First President',
          "The first direct presidential vote goes to a second round, and the winner takes office with a national mandate "
          "and a small chamber that can only amend the budget. The presidency gathers the ministries under one office in "
          "the capital. Supporters call it decisive government for a small republic; opponents note that the losing half of "
          "the country has no seat at the table.",
          ('medal', 'command'), after=('pol_presidency',), cost=10,
          exclusive=('pol_chamber_regime', 'pol_council_regime'), reward=(Regime('elected_presidency'),)),
    Focus('pol_council_regime', 'Charter the Standing Council',
          "A short charter turns the Administration into a standing council of administrators with fixed terms, published "
          "targets and an annual report read aloud in public. Party activity continues, but it no longer leads to office. "
          "The council can plan a decade of rail and harbour work without an electoral cycle. It also owns every failure, "
          "and the majority it set aside does not forget.",
          ('command', 'scales'), after=('pol_caretaker',), cost=10,
          exclusive=('pol_chamber_regime', 'pol_president_regime'), reward=(Regime('admin_council'),)),
    Focus('pol_committees', 'Committees That Read Contracts',
          "The chamber creates standing committees for the railway, the yards and the treasury, each able to summon officials "
          "and read any contract above a set value. Ministers lose afternoons to hearings, and some projects slow while "
          "committees argue. The public sees where its money goes, and contractors learn that a quiet word with one minister "
          "no longer settles a tender.",
          ('assembly', 'document'), after=('pol_chamber_regime',), exclusive=('pol_direct_mandate', 'pol_council_targets'),
          reward=(SwapIdea('election_writ', 'chamber_committees'),)),
    Focus('pol_direct_mandate', 'Government by Presidential Order',
          "The president governs through orders countersigned by a small cabinet office, and the ministries learn to move "
          "quickly. Rail timetables, harbour budgets and frontier postings change within weeks rather than seasons. The "
          "chamber can delay an order but rarely stop it. Critics in the press warn that a later president could use the same "
          "powers for worse ends, and they are not wrong.",
          ('command', 'communications'), after=('pol_president_regime',), exclusive=('pol_committees', 'pol_council_targets'),
          reward=(SwapIdea('presidential_charter', 'direct_mandate'),)),
    Focus('pol_council_targets', 'Targets Published Every Quarter',
          "The council publishes a quarterly sheet of targets and results for every ministry: kilometres of track relaid, "
          "tonnes rolled, ships kept at sea, clinics opened. Missed targets cost administrators their posts. The sheets are "
          "dull to read and impossible to ignore. They are the council's answer to the question of legitimacy: if it cannot "
          "be voted out, it can at least be measured.",
          ('document', 'scales'), after=('pol_council_regime',), exclusive=('pol_committees', 'pol_direct_mandate'),
          reward=(SwapIdea('caretaker_mandate', 'standing_council'),)),
    Focus('pol_labour', 'A Compact with the Mill Unions',
          "The labour socialists are a small party but a strong presence in the mill districts and the capital yards. A "
          "compact with the unions fixes wage rounds, safety inspections and a grievance board in exchange for no unannounced "
          "strikes for three years. Employers grumble about the inspectors. A republic with three steel districts and two "
          "yards cannot afford a summer of stoppages.",
          ('tools', 'assembly'), after=('pol_minority',), requires=(HasFlag('minority_heard'),),
          reward=(Idea('labour_compact'),)),
))

LINE = Branch('line', 'One Line Through Five Districts', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('rail_walk', 'Walk the Line End to End',
          "One level-two railway carries almost everything Kaluga moves: from the forest mills through the empty woods to the "
          "capital, and from the capital across the empty plains to the junction works. No line crosses any frontier. A "
          "survey team walks every kilometre, logging bridges, culverts and sidings. Acting on its report will be costly, "
          "and nothing can be planned without it.",
          ('rail', 'document'), reward=(Idea('spine_timetable'), Event('one_line'))),
    Focus('rail_capital_yard', 'Rebuild the Capital Freight Yard',
          "Every wagon between the two halves of the country passes through the capital's freight yard, where shunting crews "
          "still couple by hand and the harbour spur jams twice a day. New points, a second hump and lighting for night work "
          "cost a season of disruption. Once finished, the yard can turn trains round in hours rather than a full day.",
          ('rail', 'tools'), after=('rail_walk',), reward=(Build('infrastructure', 1, 0),)),
    Focus('rail_sidings', 'Passing Loops on the Plains',
          "The section across the empty plains district is single track with long gaps between passing loops, so one late "
          "train delays everything behind it. Engineers lay new loops and a gravel road beside the line for maintenance "
          "gangs. The district has no factories to serve yet, which makes the money hard to defend in the budget. It also "
          "makes the district reachable for the first time.",
          ('rail', 'logistics'), after=('rail_walk',), reward=(Build('infrastructure', 1, 570),)),
    Focus('rail_forest_halts', 'Halts in the Empty Woods',
          "Trains to the forest mills pass straight through the woods and marsh of the district beside the capital without "
          "stopping, because there is nowhere to stop. Halts, access tracks and a timber loading bay give the district its "
          "first link to anything. Foresters and surveyors can now reach the interior, and smugglers working the Luremian "
          "frontier notice the new tracks as well.",
          ('logistics', 'civil'), after=('rail_walk',), reward=(Build('infrastructure', 1, 73),)),
    Focus('rail_settle', 'Settle the Two Empty Districts',
          "The settlement school wants towns in both empty districts: housing, a works estate on each new siding and cheap "
          "credit for families who move out from the crowded capital. Settled districts would carry their share of the "
          "economy and of the frontier. It is the costlier answer, and a decade will pass before the new towns repay a "
          "fraction of what they cost.",
          ('civil', 'rail'), after_any=('rail_sidings', 'rail_forest_halts'), cost=10, exclusive=('rail_reserve',),
          reward=(SwapIdea('spine_timetable', 'settler_credit'), Flag('districts_settled'))),
    Focus('rail_reserve', 'Keep the Empty Districts in Reserve',
          "The reserve school argues that two districts without roads are also two districts without debts. It proposes "
          "leasing timber, peat and grazing rights instead of building towns, with the state keeping title and the railway "
          "serving the leases. Revenue arrives quickly and cheaply. The districts stay empty, which suits the treasury and "
          "worries officers who must defend frontiers nobody lives near.",
          ('economy', 'rail'), after_any=('rail_sidings', 'rail_forest_halts'), cost=10, exclusive=('rail_settle',),
          reward=(SwapIdea('spine_timetable', 'reserve_leases'), Flag('reserve_land'))),
    Focus('rail_works_town', 'A Works Town on the New Loops',
          "The first settlement rises beside the new passing loops on the plains: a works estate, a school and a plant making "
          "rail fittings and farm machinery. Families arrive on subsidised fares from the capital. The plant runs at a loss "
          "in its first years, and the town council complains about water. Within a decade it is the district's reason to "
          "exist.",
          ('industry', 'civil'), after=('rail_settle',), reward=(Build('industrial_complex', 1, 570),)),
    Focus('rail_sawmill_town', 'A Sawmill Town at the Halt',
          "The woods district gets its town at the busiest of the new halts, built around a sawmill, a joinery works and a "
          "timber drying shed. Timber that once rode the whole line to the forest mills is now cut where it grows. The marsh "
          "makes foundations expensive and the first winters are hard. Settlers who stay become the district's first "
          "voters.",
          ('tools', 'civil'), after=('rail_settle',), reward=(Build('industrial_complex', 1, 73),)),
    Focus('rail_leases', 'Timber and Peat Leases at Auction',
          "Leases for timber, peat and summer grazing go to public auction in blocks along the new tracks, with replanting "
          "and drainage conditions written into every contract. Bidders build their own access roads to reach their blocks. "
          "The treasury collects quickly, though inspectors must ride out each season to see whether the conditions are kept "
          "or quietly ignored.",
          ('economy', 'tools'), after=('rail_reserve',), reward=(Build('infrastructure', 1, 73), PP(25))),
    Focus('rail_frontier_road', 'A Road to the Silvonian Crossing',
          "The plains district meets Silvonia, but the only road to the crossing is a farm track that floods every spring. A "
          "paved road from the nearest loop to the customs post lets trucks, ambulances and patrols reach the frontier in any "
          "season. Silvonian hills rise on the far side, and what happens there is not for Kaluga to decide. This side, at "
          "least, will be passable.",
          ('logistics', 'gate'), after=('rail_sidings',), reward=(Build('infrastructure', 1, 570), Stability(0.01))),
    Focus('rail_flat_tariff', 'One Tariff from End to End',
          "Freight charges on the line still follow a patchwork of old district rates, so a wagon of ore pays three separate "
          "tariffs between the junction works and the capital yards. A single flat tariff per tonne and kilometre simplifies "
          "billing and helps the districts farthest from the capital. The railway loses some revenue, and capital merchants "
          "lose an advantage they had long stopped noticing.",
          ('rail', 'economy'), after_any=('rail_capital_yard', 'rail_sidings', 'rail_forest_halts'),
          reward=(Idea('freight_tariff'),)),
    Focus('rail_doubling', 'Double Track Through the Capital',
          "Whatever became of the empty districts, both halves of the line now carry more trains than the single track "
          "through the capital can pass. Doubling the capital section, with a new bridge over the harbour spur, removes the "
          "worst bottleneck in the country. It closes the line on weekends for a year. Every district feels the delay, and "
          "every district gains when it ends.",
          ('rail', 'bridge'), after_any=('rail_works_town', 'rail_sawmill_town', 'rail_leases'), cost=10,
          reward=(Build('infrastructure', 1, 0), Research('train_tech', 0.5, 1))),
))

STEEL = Branch('steel', 'Steel in Three Districts', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('steel_census', 'Count Every Furnace',
          "Three districts dig and smelt steel: the capital, the forest mills and the junction works. Nobody has compared their "
          "furnaces, costs or order books since the Administration took office. A census of every furnace, rolling stand and "
          "ore pit tells the ministry what the country can actually make. Owners resent the inspectors; the figures will "
          "shape every decision that follows.",
          ('industry', 'document'), reward=(Idea('mill_census'), Event('three_furnaces'))),
    Focus('steel_ingots', 'Ship the Ingots Abroad',
          "The export school says Kaluga should do what it already does cheaply: smelt ingots and ship them from the capital "
          "harbour to whoever pays. Contracts would be long and foreign currency would arrive quickly. Finished goods would "
          "still be imported at someone else's margin, and the mills would stay at the bottom of every supply chain they "
          "join.",
          ('economy', 'navy'), after=('steel_census',), cost=10, exclusive=('steel_rolling', 'steel_plate'),
          reward=(SwapIdea('mill_census', 'ingot_exports'),)),
    Focus('steel_rolling', 'Roll and Finish at Home',
          "The finishing school wants ingots rolled into sheet, rail and wire inside the country, so that Kalugan factories "
          "and the railway buy Kalugan steel. It needs new rolling stands and protected prices for a decade. Domestic "
          "industry would deepen and jobs would multiply. Export earnings fall meanwhile, and the treasury must carry the gap "
          "until the stands pay for themselves.",
          ('industry', 'tools'), after=('steel_census',), cost=10, exclusive=('steel_ingots', 'steel_plate'),
          reward=(SwapIdea('mill_census', 'rolled_at_home'),)),
    Focus('steel_plate', 'Hull Plate for the Capital Slips',
          "The shipbuilding school points to the two yards on the capital harbour and asks why their plate comes from abroad. "
          "It proposes turning the mills toward marine plate and sections, guaranteed by yard contracts. The navy and the "
          "merchant owners would gain a domestic supplier. Everything would then ride on two small yards, a narrow footing "
          "for a whole steel trade.",
          ('navy', 'industry'), after=('steel_census',), cost=10, exclusive=('steel_ingots', 'steel_rolling'),
          reward=(SwapIdea('mill_census', 'hull_plate'),)),
    Focus('steel_ore_road', 'Ore Roads to the Junction Ramps',
          "Ingot exports need ore and coke moving fast, and the junction district's pits reach the railway by crumbling "
          "roads. Paving the haul roads and widening the loading ramps at the logistics centre lets ore trains leave full "
          "every day. The work is cheap beside a new mill. It also serves the junction's frontier traffic, which customs "
          "officers will be glad of.",
          ('logistics', 'industry'), after=('steel_ingots',), reward=(Build('infrastructure', 1, 569),)),
    Focus('steel_rolling_mill', 'A Rolling Mill Among the Pines',
          "The forest mill district has ore, wood-fired boilers and one free plot beside the railway. A rolling mill there "
          "turns local ingots into rail and wire for the line itself. The plant sits on marsh ground and needs costly piling. "
          "Once running, it means the railway can relay its own track with steel that never left the country.",
          ('industry', 'rail'), after=('steel_rolling',), reward=(Build('industrial_complex', 1, 138),)),
    Focus('steel_plate_shop', 'A Plate Shop by the Slipways',
          "The last free plot on the capital waterfront becomes a plate shop and a third building berth, so that marine plate "
          "rolled at home goes straight from the mill train to the slipway. Space in the capital is precious, and the harbour "
          "board wanted the plot for warehouses. Instead it builds hulls, which the coastal defence plans have wanted since "
          "1991.",
          ('navy', 'tools'), after=('steel_plate',), reward=(Build('dockyard', 1, 0),)),
    Focus('steel_credit', 'A Bank for Mill Credit',
          "Whichever course the mills took, all of them need credit that private banks will not give a small country's heavy "
          "industry. A state mill bank lends against order books, with rates set by the ministry and accounts open to "
          "inspection. Bad loans will happen, and the treasury will carry them. The aim is that no mill closes because one "
          "customer paid late.",
          ('economy', 'industry'), after_any=('steel_ore_road', 'steel_rolling_mill', 'steel_plate_shop'),
          reward=(Idea('mill_credit'),)),
    Focus('steel_alloy', 'Light Alloy for the Arms Works',
          "Kaluga has aluminium as well as steel, most of it in the capital and forest districts, and almost all of it leaves "
          "the country raw. A light alloy works beside the junction arms plants would supply frames for vehicles, aircraft "
          "parts and small arms. It is a modest venture with a long learning curve, and the first castings will be scrapped "
          "by the dozen.",
          ('industry', 'science'), after=('steel_census',), reward=(Idea('light_alloy'),)),
    Focus('steel_fuel_book', 'Six Small Wells and One Silo',
          "The country pumps a little oil from six modest fields and stores it in a single silo at the capital. A fuel book "
          "allocates every barrel among the railway, the mills, the fleet and the airfield, with a reserve only the cabinet "
          "can release. Industry complains about rationing in peacetime. The fleet and fighters would complain far louder if "
          "the silo ran dry.",
          ('logistics', 'document'), after=('steel_census',), reward=(Idea('fuel_book'),)),
    Focus('steel_arms_line', 'An Arms Line on the Plains',
          "With a works town now standing on the plains, the ministry places a small arms line there to build mortars, "
          "machine guns and vehicle parts with alloy from the junction works. Moving some arms production away from the "
          "capital and the frontier junction is sound planning. It also gives the new town a second employer, and gives the "
          "army a reason to defend it.",
          ('missile', 'civil'), after=('steel_alloy',), requires=(HasFlag('districts_settled'),),
          reward=(Build('arms_factory', 1, 570),)),
))

HARBOUR = Branch('harbour', 'One Harbour, One Escort', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('port_board', 'A Board for the Capital Harbour',
          "The capital harbour holds the country's only naval base, its two yards and nearly all its merchant traffic, and "
          "three ministries each believe they run it. A single harbour board takes over berths, pilots, dredging and the "
          "naval quay. The ministries lose their small empires. Ships stop waiting for permission from offices that do not "
          "speak to each other.",
          ('navy', 'command'), reward=(Idea('harbour_board'), Event('one_harbour'))),
    Focus('port_new_submarines', 'A New Class of Submarine',
          "In September 1991 Yuktobania announced a new class of submarine to the world. Kaluga's navy is one escort and a "
          "handful of patrol craft, and its whole coast faces open water. Officers ask what one large submarine could do to "
          "the capital harbour. A watch on the approaches, using listening buoys and fishing-boat reports, is the cheapest "
          "answer anyone can offer.",
          ('submarine', 'radar'), requires=(After('1991.9.2'),), reward=(TimedIdea('submarine_watch', 730),)),
    Focus('port_mines', 'Mines and Patrol Boats',
          "The mine school argues that one escort cannot defend five districts of coast, but controlled minefields and a "
          "flotilla of fast patrol boats can make the harbour approaches dangerous for anyone. Mines are cheap and quiet. "
          "They also turn fishing grounds into closed water, and every fishing family on the coast will feel the new charts.",
          ('navy', 'security'), after=('port_board',), cost=10, exclusive=('port_escorts',),
          reward=(SwapIdea('harbour_board', 'mine_flotilla'),)),
    Focus('port_escorts', 'A Squadron of Three Escorts',
          "The escort school wants the lone destroyer joined by two more, built or bought, so that one is always at sea, one "
          "in refit and one training. A squadron could escort convoys, chase contacts and show the flag along the long coast. "
          "It is far dearer than mines, and three small ships remain small against any serious navy.",
          ('navy', 'logistics'), after=('port_board',), cost=10, exclusive=('port_mines',),
          reward=(SwapIdea('harbour_board', 'escort_pair'),)),
    Focus('port_patrol_yard', 'A Patrol Craft Yard in the Woods',
          "Patrol boats and minelayers need a yard away from the crowded capital. A sheltered inlet in the woods district, "
          "already reached by the new halts, can take a small slipway and a mine store under the trees. The marsh ground is "
          "soft and access is poor. Dispersal means one strike on the capital no longer ends the flotilla.",
          ('navy', 'tools'), after=('port_mines',), reward=(Build('dockyard', 1, 73),)),
    Focus('port_escort_slips', 'Two Hulls on the Capital Slips',
          "The two new escorts are laid down on the capital slips to a modest design the yards can actually finish. The navy "
          "wants more guns; the yards want fewer changes. Engineers learn hull work and crews train on the first ship while the "
          "second is still on the ways. It is slow and expensive, and it is a fleet built at home.",
          ('navy', 'industry'), after=('port_escorts',), reward=(Research('naval_equipment', 0.5, 2), XP('navy', 15))),
    Focus('port_fishery', 'A Fishery Patrol on Every Coast',
          "All five districts touch the sea, and the fishing fleets of several countries work the same grounds. Cutters with "
          "boarding crews enforce catch limits, check papers and tow broken boats home. The patrol earns little and burns "
          "fuel. It gives the coast a visible state presence and keeps small quarrels between fishermen from reaching the "
          "foreign ministry.",
          ('fishing', 'security'), after=('port_board',), reward=(Idea('fishery_patrol'),)),
    Focus('port_convoy', 'Pool the Sixty Freighters',
          "Sixty freighters and coasters sail under Kalugan registry, owned by dozens of firms that never share information. "
          "A convoy pool lists every hull, crew and cargo, and routes them together when the sea lanes turn dangerous. Owners "
          "dislike the paperwork. In a crisis the republic will know where every ship is and what each can carry.",
          ('logistics', 'navy'), after=('port_board',), reward=(Idea('convoy_pool'),)),
    Focus('port_lifeboats', 'Lifeboat Crews Along the Coast',
          "Volunteer lifeboat crews already exist in a few villages, trained by fishermen and paid from collection boxes. The "
          "harbour board funds stations, boats and radios in every district so that a crew can reach any stretch of coast "
          "within an hour. The crews are cheap, proud and indispensable in a storm, or in any emergency that empties a "
          "coastal town.",
          ('medical', 'navy'), after=('port_fishery',), reward=(Flag('lifeboat_crews'), Stability(0.02))),
    Focus('port_exercise', 'The First Joint Harbour Exercise',
          "Whatever the navy chose, the harbour board runs its first exercise combining warships, coast guns, fighters from "
          "the capital field and the lifeboat crews. Signals fail, a patrol boat runs aground and the fighters arrive late. "
          "Every error is written down. The second exercise goes better, and a standing coast command grows out of the "
          "wreckage of the first.",
          ('command', 'navy'), after_any=('port_patrol_yard', 'port_escort_slips'),
          reward=(Flag('harbour_command'), XP('navy', 20))),
    Focus('port_coast_radar', 'Radar Over the Harbour Mouth',
          "The exercise showed that nobody could see past the harbour breakwater at night. A radar station on the headland "
          "covers the approaches and feeds the coast command. It is an old design bought second-hand, and its crews keep it "
          "alive with spare parts from three countries. It still sees farther than any lookout ever did.",
          ('radar', 'navy'), after=('port_exercise',), reward=(Build('radar_station', 1, 0),)),
))

ARMY = Branch('army', 'Four Formations on a Long Border', 1993, 'FOCUS_FILTER_ARMY_XP', (
    Focus('army_staff', 'One Staff for Four Formations',
          "The army is four infantry formations with engineers attached, enough to hold the capital and little more. Each "
          "formation keeps its own stores, maps and habits. A single general staff, with one supply office and one training "
          "plan, turns four garrisons into an army. Senior officers lose their independence, and the staff's first readiness "
          "report makes uncomfortable reading.",
          ('command', 'training'), reward=(Idea('four_formations'), Event('long_frontier'))),
    Focus('army_territorial', 'A Company in Every District',
          "The territorial school splits the formations into companies stationed in every district, recruited locally and "
          "trained on their own woods, marsh and plains. Every district would have defenders who know its ground. Nobody "
          "could attack anything, and the companies would be thin. For a country with four formations, the school argues, "
          "being everywhere is the only realistic aim.",
          ('security', 'civil'), after=('army_staff',), cost=10, exclusive=('army_brigade',),
          reward=(SwapIdea('four_formations', 'territorial_companies'),)),
    Focus('army_brigade', 'One Field Brigade on the Railway',
          "The field school wants the formations concentrated into one brigade with trucks and rail wagons, based at the "
          "capital and able to move to any district along the line within a day. Its punch would be real. Districts would be "
          "watched by police and customs until the brigade arrived, and every officer knows how much can happen in a day.",
          ('rail', 'training'), after=('army_staff',), cost=10, exclusive=('army_territorial',),
          reward=(SwapIdea('four_formations', 'field_brigade'),)),
    Focus('army_armouries', 'Armouries for the District Companies',
          "Companies in five districts need rifles, ammunition and repair benches close at hand rather than in the capital. A "
          "small arms works in the woods district, near the new halts, supplies the companies along the forest frontiers and "
          "repairs what they break. Spreading production costs efficiency. It also lets the woods companies fight for weeks "
          "without a train from the capital.",
          ('missile', 'security'), after=('army_territorial',), reward=(Build('arms_factory', 1, 73),)),
    Focus('army_brigade_trucks', 'Trucks and Flatcars for the Brigade',
          "The brigade's speed depends on vehicles and wagons the army does not yet have. Buying trucks and reserving flatcars "
          "on the railway gives the brigade its promised mobility. Drivers and loaders must be trained, and the railway "
          "resents losing wagons. Exercises show the brigade reaching the junction in eighteen hours, which the staff calls a "
          "success and the junction calls slow.",
          ('logistics', 'rail'), after=('army_brigade',), reward=(Research('logistics_tech', 0.5, 1), XP('army', 20))),
    Focus('army_engineers', 'Engineers Before Infantry',
          "Kaluga's formations already lean on attached engineers, and the research staff's priority is sustainment rather "
          "than new weapons. An engineer school trains bridge, rail and demolition specialists who can keep the line open or "
          "close it to an enemy. Infantry officers complain that their best recruits are taken. Engineers also build in "
          "peacetime, which the treasury likes.",
          ('tools', 'training'), after=('army_staff',), reward=(Idea('engineer_school'),)),
    Focus('army_spares', 'Spares Before New Rifles',
          "The army's stock of rifles, trucks and support equipment is adequate, but its spare parts are not. Depots for "
          "barrels, tyres, radios and engine parts, kept beside the railway, mean equipment is repaired instead of written off. "
          "New weapons would look better on parade. Spares keep the four formations able to move, which is the sustainment "
          "priority the staff was given.",
          ('logistics', 'tools'), after=('army_staff',), reward=(Idea('spares_depots'),)),
    Focus('army_reserve_woods', 'Fieldcraft in the Leased Woods',
          "Where the empty districts stayed as reserve land, the army negotiates training areas inside the timber and peat "
          "leases. Infantry learn marsh crossings, forest navigation and winter living in country nobody else uses. "
          "Leaseholders complain about blank rounds near their stacks. The army gains ground it can train on all year, and "
          "soldiers who know the forest frontiers.",
          ('training', 'security'), after=('army_staff',), requires=(HasFlag('reserve_land'),),
          reward=(Idea('forest_fieldcraft'),)),
    Focus('army_frontier_posts', 'Posts Facing the Silvonian Hills',
          "Four of the five districts touch Silvonia, whose side of the frontier rises into hill and mountain country. Small "
          "observation posts on the Kalugan side, linked by telephone and reached by a road from the junction district, let "
          "the army watch rather than guess. Silvonian patrols will see them. They are placed to be seen, and nothing about "
          "them is offensive.",
          ('security', 'gate'), after_any=('army_territorial', 'army_brigade'),
          reward=(Build('infrastructure', 1, 569), Flag('frontier_posts'))),
    Focus('army_staff_ride', 'A Staff Ride Along the Railway',
          "Staff officers ride the railway from the forest mills to the junction works, stopping at every bridge and cutting "
          "to plan how they would defend it, repair it and if necessary destroy it. The ride produces a book of demolition "
          "and repair plans for the whole line. It is the closest thing Kaluga has to a war plan, and it costs only train "
          "fares.",
          ('bridge', 'command'), after=('army_engineers',), reward=(Research('land_doctrine', 0.5, 1), XP('army', 15))),
))

AIR = Branch('air', 'Twenty-Four Fighters, One Runway', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_one_field', 'Every Fighter on One Runway',
          "All twenty-four fighters, with six more in reserve, fly from a single airfield at the capital. One closed runway, "
          "one fuel fire or one storm grounds the entire air arm. The air staff writes this down plainly for the first time "
          "and asks for money. The report is accurate, and the treasury reads it with the enthusiasm it keeps for every "
          "expensive truth.",
          ('air', 'runway'), reward=(Idea('single_field'), Event('one_runway'))),
    Focus('air_capital_runway', 'A Longer Runway at the Capital',
          "The capital runway is too short for loaded fighters on hot days, and its taxiways flood. Lengthening it and adding "
          "hardstands and a second taxiway costs little compared to a new field. It does nothing about having only one "
          "airfield. It does mean every sortie from that one field can leave with full fuel and weapons.",
          ('runway', 'tools'), after=('air_one_field',), reward=(Build('air_base', 1, 0),)),
    Focus('air_junction_field', 'A Second Field at the Junction',
          "The junction district has flat ground, the railway and the logistics centre, and it lies at the opposite end of "
          "the country from the forest mills. A second airfield there means a strike on the capital no longer grounds the air "
          "arm. It is the most expensive item in the air budget, and the junction district welcomes the jobs.",
          ('runway', 'rail'), after=('air_one_field',), cost=10, reward=(Build('air_base', 2, 569),)),
    Focus('air_interceptors', 'Interceptors for the Capital Sky',
          "The interception school wants the fighters trained and equipped above all to meet intruders over the capital, its "
          "harbour and its yards. Pilots would fly scrambles, night intercepts and ground-controlled approaches. The rest of "
          "the country would see fighters only passing overhead. A republic with one city worth bombing, the school argues, "
          "should defend that city first.",
          ('air', 'security'), after=('air_one_field',), exclusive=('air_sea_patrol',),
          reward=(SwapIdea('single_field', 'interceptor_watch'),)),
    Focus('air_sea_patrol', 'Fighters over the Sea Lanes',
          "The maritime school points out that every district is coastal and that the navy has one escort. It wants the "
          "fighters trained for sea patrol, ship identification and work with the coast command. Pilots would spend long "
          "hours over water. The capital would rely on its guns and on whichever fighters happened to be home when trouble "
          "came.",
          ('air', 'navy'), after=('air_one_field',), exclusive=('air_interceptors',),
          reward=(SwapIdea('single_field', 'sea_patrol_wing'),)),
    Focus('air_hill_radar', 'Radar Above the Capital',
          "Interceptors need warning, and the capital's few hills offer the only high ground. A radar station on the highest "
          "of them feeds a control room at the airfield, where controllers guide pilots onto targets. Radar crews are hard to "
          "train and harder to keep. Without them, interceptors are guessing, and guessing pilots run out of fuel.",
          ('radar', 'air'), after=('air_interceptors',), reward=(Build('radar_station', 1, 0), XP('air', 10))),
    Focus('air_ship_spotting', 'Spotting for the Coast Command',
          "Fighter pilots train with the coast command to identify ships by silhouette, report positions in the navy's grid "
          "and guide escorts or patrol boats onto contacts. The training is tedious and the pilots would rather dogfight. "
          "After a season, the coast command can see fifty kilometres out to sea whenever a fighter is airborne, which "
          "changes every patrol plan.",
          ('air', 'logistics'), after=('air_sea_patrol',), reward=(Research('air_doctrine', 0.5, 1), XP('air', 15))),
    Focus('air_forest_strip', 'A Dispersal Strip in the Forest',
          "A grass strip cut in the forest mill district gives fighters somewhere to land if both main fields close. It has "
          "fuel bowsers, camouflage nets and a hut for ground crew, and little else. Pilots dislike the short run and the "
          "trees. In an emergency, though, the forest strip keeps a flight in the air while the larger fields are repaired.",
          ('runway', 'shelter'), after_any=('air_interceptors', 'air_sea_patrol'), reward=(Build('air_base', 1, 138),)),
    Focus('air_observers', 'Observers on the Frontier Hills',
          "Radar cannot see everything, least of all low aircraft crossing from the hill country beyond the Silvonian "
          "frontier. An observer corps of volunteers with binoculars, telephones and recognition charts reports every engine "
          "it hears. The corps costs almost nothing. It also gives retired soldiers and farmers a real part in defending their "
          "district, which pays off in other ways.",
          ('telescope', 'security'), after=('air_junction_field',), reward=(Idea('observer_corps'),)),
    Focus('air_pilot_ladder', 'A Ladder for Young Pilots',
          "Kaluga trains few pilots and loses many of them to airlines abroad. A ladder from gliding clubs through basic "
          "flying to fighter conversion, with bonded service in return, keeps the cockpits filled. Gliding clubs need fields "
          "and instructors. The bond is resented by pilots who later want airline pay, but it keeps the six reserve fighters "
          "crewed.",
          ('training', 'air'), after=('air_one_field',), reward=(Idea('pilot_ladder'),)),
))

NEIGHBOURS = Branch('neighbours', 'Five Neighbours, No Rail Across', 1994, 'FOCUS_FILTER_POLITICAL', (
    Focus('nbr_map', 'Five Frontiers on One Wall Map',
          "Kaluga touches five countries: Silvonia along four districts, Luremia beside the woods, Glaceland on a short "
          "stretch beyond the forest mills, and Romny and Yuktobania at the junction district. Each frontier has been handled "
          "by whichever ministry had a problem there. The foreign ministry gathers them onto one map and one staff, and finds "
          "files missing for half of them.",
          ('diplomacy', 'document'), reward=(Idea('frontier_staff'), Event('five_frontiers'))),
    Focus('nbr_silvonia', 'Customs Halls Facing Silvonia',
          "The army's frontier posts showed how little the civil state had on its longest frontier. Customs halls on the main "
          "crossings, with a proper road to the woods district crossing, replace sheds and barriers. Silvonia's own "
          "arrangements are its business. On the Kalugan side, travellers and trucks now meet a single office, a weighbridge "
          "and fixed opening hours.",
          ('gate', 'civil'), after=('nbr_map',), requires=(HasFlag('frontier_posts'),),
          reward=(Build('infrastructure', 1, 73), Stability(0.01))),
    Focus('nbr_glaceland', 'Someone to Answer Glaceland',
          "The Glacelandic frontier beyond the forest mills is short and rarely mentioned in the capital. If a post on the far "
          "side ever calls, someone on the Kalugan side should pick up. The ministry staffs a small post with a telephone and "
          "a vehicle, and asks the forest district police to report anything unusual. It is the cheapest diplomacy the "
          "republic does.",
          ('communications', 'gate'), after=('nbr_map',),
          reward=(Stability(0.02), Tooltip('No border, claim or treaty change; staffs the Kalugan side of the frontier only.'))),
    Focus('nbr_luremia', 'Timber Talks with Luremia',
          "Luremia faces both the woods district and the forest mills, and timber crosses that frontier in both directions "
          "with little paperwork. Talks on felling, replanting, fire watch and customs for logs give the forest districts a "
          "predictable trade. Some mill owners lose cheap Luremian timber. The forest police gain a counterpart to call when "
          "a fire jumps the line.",
          ('diplomacy', 'tools'), after=('nbr_map',), reward=(TimedIdea('timber_accord', 1095),)),
    Focus('nbr_junction', 'Where Three Frontiers Meet',
          "At the junction district Kaluga meets Romny, Yuktobania and Silvonia within a short distance. Freight, smuggling "
          "and rumour all pass through it. A joint customs office at the logistics centre, with inspectors who speak the "
          "neighbours' languages, gives the government eyes on the busiest corner of the country. It also makes the junction "
          "a place neighbours expect to negotiate.",
          ('gate', 'logistics'), after=('nbr_map',), reward=(PP(20), Flag('junction_customs'))),
    Focus('nbr_registers', 'Two Districts in the Old Registers',
          "Inherited registers still list two districts now held by Yuktobania as Kalugan. Nobody in government expects to "
          "change that, and nobody wants to be the minister who erases them. The foreign ministry drafts a paper on how the "
          "republic should speak about the registers in public. The paper is careful, and every faction reads it for the one "
          "sentence it fears.",
          ('document', 'scales'), after=('nbr_map',),
          reward=(PP(25), Tooltip('Opens a choice of public wording only; no claim, core or border changes.'))),
    Focus('nbr_shelve', 'Let the Old Registers Rest',
          "The quiet school proposes that the republic say nothing further: the registers stay in the archive, ministers "
          "decline questions, and relations with Yuktobania proceed on present facts. Nationalists call it surrender. Trade "
          "officials call it common sense. Yuktobania, which notices everything said on its frontiers, notices that nothing "
          "is being said at all.",
          ('peace', 'document'), after=('nbr_registers',), exclusive=('nbr_keep',),
          reward=(Idea('quiet_registers'), Tooltip('No claim, core or border changes.'))),
    Focus('nbr_keep', 'Keep the Registers on the Record',
          "The record school wants the registers noted in an annual government statement, without demands or deadlines, so "
          "that no later government can say the matter was dropped. It costs nothing in arms and something in goodwill. "
          "Yuktobanian diplomats will read every statement. At home, the small nationalist circle loses its favourite charge "
          "against the government.",
          ('document', 'medal'), after=('nbr_registers',), exclusive=('nbr_shelve',),
          reward=(Idea('open_registers'), Tooltip('A statement only; no claim, core, border or war changes.'))),
    Focus('nbr_big_market', 'Sell into the Big Market Next Door',
          "Yuktobania's market dwarfs Kaluga's, and the junction district sits right beside it. The trade school wants steel, "
          "timber and rail fittings sold across that frontier on long contracts. The mills would run full. The republic would "
          "also depend on a single giant buyer whose politics it cannot influence and whose orders could stop with one "
          "signature.",
          ('economy', 'gate'), after=('nbr_junction',), exclusive=('nbr_own_course',), reward=(Idea('big_market'),)),
    Focus('nbr_own_course', 'Spread the Orders Among Five',
          "The balance school wants no neighbour to take more than a fixed share of Kalugan exports, with trade offices "
          "courting Silvonia, Luremia, Glaceland and Romny as well as Yuktobania. Growth would be slower and salesmen busier. "
          "No single capital could squeeze the republic by cancelling orders, and that independence is worth the margin to "
          "its advocates.",
          ('scales', 'diplomacy'), after=('nbr_junction',), exclusive=('nbr_big_market',), reward=(Idea('spread_orders'),)),
    Focus('nbr_belkan_war', 'Freight Rates and a Faraway War',
          "In March 1995 war breaks out around Belka, far from Kaluga's coast. Insurers raise rates on every freighter, fuel "
          "prices climb and the convoy pool asks whether any Kalugan ships are near the fighting. The government declares it "
          "has no part in the war and tightens its own coast watch. Nobody expects the war to arrive; everyone pays for it.",
          ('communications', 'security'), after=('nbr_map',), requires=(After('1995.3.25'),),
          reward=(TimedIdea('distant_war_watch', 180),)),
    Focus('nbr_thaw', 'A Thaw Between the Giants',
          "In October 1999 Osea and Yuktobania agree to convert the Arkbird into a platform for clearing orbital debris. For a "
          "small neighbour of Yuktobania, the two great powers working together changes insurance, credit and trade forecasts "
          "almost overnight. Kalugan officials study what the cooperation means for frontier trade, and plan to profit "
          "modestly from a calmer decade.",
          ('peace', 'diplomacy'), after_any=('nbr_big_market', 'nbr_own_course'), requires=(After('1999.10.8'),),
          reward=(Flag('thaw_noted'), Stability(0.03))),
))

ASTEROID = Branch('asteroid', 'Ulysses over Five Districts', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('star_warning', 'The Astronomers Raise the Alarm',
          "In December 1994 word comes from the international astronomers that Ulysses, an asteroid found only weeks before, "
          "may strike the planet. Kaluga owns no telescope able to follow it and no scientist able to check the sums. A weekly "
          "sky bulletin, compiled from foreign releases and read on every station, lets citizens hear the state before they "
          "hear the rumour mill.",
          ('meteor', 'communications'), requires=(After('1994.12.10'),),
          reward=(Idea('sky_bulletin'), Event('warning_star'))),
    Focus('star_tracking', 'A Desk for Borrowed Data',
          "Kaluga cannot track the asteroid, but its university physicists can read data from those who do. A small desk "
          "translates international orbital updates into plain briefings for ministers and district councils. Its staff are "
          "underpaid and overworked. Their briefings stop at least one minister from repeating a newspaper's wilder estimate "
          "in public.",
          ('telescope', 'science'), after=('star_warning',), reward=(Research('electronics', 0.5, 1), Stability(0.01))),
    Focus('star_impact', 'Impact Is Confirmed',
          "In April 1996 the President of the FCU announces worldwide that Ulysses will strike the Earth. Where its fragments "
          "will fall is not yet known to anyone. Kalugan families start hoarding flour and fuel, and the capital's banks see "
          "queues. The government has days to decide how to plan for a disaster whose size and place it cannot know.",
          ('meteor', 'document'), after=('star_warning',), requires=(After('1996.4.20'),), reward=(Event('impact_year'),)),
    Focus('star_cellars', 'Cellars and Rail Cuttings',
          "The shelter school proposes reinforcing cellars in every town and fitting out railway cuttings and tunnels as "
          "shelters stocked with water, lamps and blankets. Everyone would have somewhere to go within minutes. It is a huge "
          "amount of concrete for a small country, and if the fragments fall far away the money will look wasted.",
          ('shelter', 'rail'), after=('star_impact',), cost=10, exclusive=('star_dispersal',),
          reward=(Idea('cellar_shelters'),)),
    Focus('star_dispersal', 'Move Families Away from the Capital',
          "The dispersal school notes that the country's only harbour, airfield, yards and largest mills share one coastal "
          "city. It proposes plans to move families by rail to the plains and woods districts if a fall is predicted nearby, "
          "with reception places, kitchens and school desks waiting. It is cheaper than concrete, far harder to carry out, "
          "and wholly dependent on warning time.",
          ('refugees', 'rail'), after=('star_impact',), cost=10, exclusive=('star_cellars',),
          reward=(Idea('dispersal_plan'),)),
    Focus('star_cutting_works', 'Roofing the Forest Cuttings',
          "The deepest cuttings on the line run through the forest mill district, where the railway passes between rock and "
          "earth banks. Engineers roof sections of them, add drainage and lay a service road so that supplies can reach the "
          "shelters if the line is blocked. Trains slow to walking pace during the work, and the mills lose a season of "
          "shipments.",
          ('shelter', 'tools'), after=('star_cellars',), reward=(Build('infrastructure', 1, 138),)),
    Focus('star_reception', 'Reception Centres on the Plains',
          "Dispersal needs somewhere to go. Reception centres along the plains section of the line, with kitchens, field "
          "hospitals, wells and a road from every halt, can hold capital families in their tens of thousands for weeks. In "
          "normal years they serve as schools and markets. Few believe they will ever be full, and nobody wants to find out "
          "unprepared.",
          ('refugees', 'civil'), after=('star_dispersal',),
          reward=(Build('infrastructure', 1, 570), Tooltip('In ordinary years the centres serve as schools and markets.'))),
    Focus('star_grain', 'Grain for Two Winters',
          "If an impact anywhere closed the sea lanes, food imports would be the first thing to stop. A state reserve of "
          "grain, salt and preserved fish for two winters, stored in rail-served warehouses in every district, guards against "
          "a closed sea. Farmers like the guaranteed purchases. Taxpayers pay for warehouses they hope never to empty.",
          ('economy', 'shelter'), after=('star_impact',), reward=(Idea('grain_reserve'),)),
    Focus('star_lifeboat_standby', 'Lifeboat Crews on Standby',
          "The lifeboat stations funded by the harbour board go onto a standby rota for the impact years, with fuel, radios "
          "and evacuation plans for every coastal village. Crews rehearse taking people off beaches and out of flooded "
          "harbours. Volunteers give up their weekends. If the sea rises anywhere on the coast, boats will already be there.",
          ('medical', 'navy'), after=('star_impact',), requires=(HasFlag('lifeboat_crews'),),
          reward=(TimedIdea('evac_rehearsal', 730),)),
    Focus('star_roche', 'A Night in Cellars and Cuttings',
          "In July 1999 Ulysses passes through the Roche limit. Kalugans spend the night in cellars, cuttings and reception "
          "centres, or on rooftops watching the sky. Government broadcasts repeat the same plain instructions every hour. "
          "Reports from the Usean continent soon describe catastrophic damage there. At home the task is to keep people calm, "
          "fed and told the truth.",
          ('meteor', 'shelter'), after_any=('star_cellars', 'star_dispersal'), requires=(After('1999.7.8'),),
          reward=(TimedIdea('calm_broadcasts', 180), Stability(0.02))),
    Focus('star_debris', 'A Debris Watch for the Century',
          "Fragments of Ulysses remain in orbit after 1999, and the great powers are building ways to clear them. The sky "
          "bulletin becomes a standing debris watch, linking the observer corps, the radar crews and international data so "
          "that any fall near the coast is reported within minutes. It is a small office with a long brief, and the radar "
          "crews finally have something to watch.",
          ('meteor', 'radar'), after=('star_roche',), reward=(SwapIdea('sky_bulletin', 'debris_watch'),)),
))

LEDGER = Branch('ledger', 'The Ledger Years', 2001, 'FOCUS_FILTER_RESEARCH', (
    Focus('cent_ledger', 'A Ledger of the Whole Republic',
          "Ten years after 1991, the ministries keep their figures in a dozen incompatible formats, from rail tonnage to "
          "fishery catches. A national ledger brings them into one statistical office with one set of definitions. It is "
          "dull, essential work. Every later plan, from the next rail budget to the next naval programme, will rest on numbers "
          "that finally agree.",
          ('document', 'economy'), reward=(Idea('national_ledger'), Event('ledger_years'))),
    Focus('cent_exchange', 'Wire the Ministries Together',
          "The ministries now use computers, but each in its own building with its own system. A data exchange connects them "
          "over leased lines, so the harbour board, the railway and the treasury see the same figures on the same day. "
          "Installation runs over budget and older officials resist it. The exchange saves weeks on every decision that "
          "involves more than one ministry.",
          ('communications', 'science'), after=('cent_ledger',), reward=(Idea('data_exchange'),)),
    Focus('cent_engineers', 'Engineers for the Next Decade',
          "The universities turn out lawyers and teachers in plenty, but too few engineers for the rail, steel and harbour "
          "work the republic has started. Scholarships, a technical college in the capital and bonded places for graduates "
          "who stay at home raise the numbers. Results take years. The college is the one institution every faction agrees "
          "the next decade needs.",
          ('science', 'training'), after=('cent_exchange',),
          reward=(Research('industry', 0.5, 1), Research('electronics', 0.75, 1))),
    Focus('cent_transit', 'A Transit Office at the Junction',
          "The junction customs office handles more freight every year, and lorries queue for a day at peak times. A transit "
          "office with bonded sidings, a truck park and wider roads lets goods cross between neighbours through Kalugan "
          "territory under seal. It earns fees and keeps traffic moving. It also makes the junction a crossroads its "
          "neighbours rely on.",
          ('gate', 'rail'), after=('cent_ledger',), requires=(HasFlag('junction_customs'),),
          reward=(Build('infrastructure', 1, 569), PP(15))),
    Focus('cent_thaw_trade', 'Trade in a Calmer Decade',
          "With the great powers cooperating, credit is cheaper and insurers relax. Kalugan exporters use the calmer years to "
          "sign multi-year contracts and refinance mill debts at lower rates. The ministry warns that calm years end. For "
          "now, order books are fuller than at any time since 1991, and the treasury can repay some of what the mill bank "
          "lent.",
          ('economy', 'peace'), after=('cent_ledger',), requires=(HasFlag('thaw_noted'),),
          reward=(TimedIdea('thaw_trade', 730),)),
    Focus('cent_usean_war', 'War Across the Sea in Usea',
          "In August 2003 the FCU establishes the ISAF to confront Erusea over the Usean crisis. Kaluga is far from it, but "
          "freight rates jump and some Kalugan ships trade with Usean ports. The convoy pool needs new terms, insurers demand "
          "state cover and the government repeats that it takes no side. Distance limits the damage without removing it.",
          ('logistics', 'scales'), after=('cent_ledger',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Idea('shipping_cover'),)),
    Focus('cent_convoy_routes', 'Reroute the Usean Traders',
          "The coast command, formed after the harbour exercises, takes charge of every Kalugan ship trading toward Usea. "
          "Ships are routed away from contested waters, given radio schedules and recalled if the fighting moves near their "
          "ports. Owners lose cargoes and fees. The command's aim is narrow: no Kalugan crew becomes a casualty of a war the "
          "republic is not part of.",
          ('navy', 'communications'), after=('cent_usean_war',), requires=(HasFlag('harbour_command'),),
          reward=(XP('navy', 15), Research('naval_equipment', 0.5, 1))),
    Focus('cent_coast_first', 'Coast First in the Next Programme',
          "Planning for the next programme begins, and the coast school wants its money spent on the harbour, the yards, the "
          "escorts and the coast command. Every district touches the sea, it argues, and the sea is where trade and danger "
          "both arrive. Inland roads and frontier works would wait. Officers on the Silvonian frontier read the draft with "
          "dismay.",
          ('navy', 'document'), after_any=('cent_engineers', 'cent_transit', 'cent_thaw_trade'), cost=10,
          exclusive=('cent_interior_first',), reward=(Idea('coast_plan'),)),
    Focus('cent_interior_first', 'Interior First in the Next Programme',
          "The interior school wants the next programme spent on roads, towns and frontier works: the empty districts, the "
          "forest frontiers and the junction. Every frontier Kaluga has is a land frontier, it argues, and the districts "
          "beside them still lack proper roads. The harbour and yards would wait. The navy, already the smallest service, "
          "protests loudest.",
          ('civil', 'gate'), after_any=('cent_engineers', 'cent_transit', 'cent_thaw_trade'), cost=10,
          exclusive=('cent_coast_first',), reward=(Idea('interior_plan'),)),
    Focus('cent_account', 'The Republic Takes Stock in 2005',
          "In 2005 the government publishes a plain account of fifteen years: the constitution it chose, the line it rebuilt, "
          "the mills, the harbour, the five frontiers and the years under the asteroid. The account is a baseline for whoever "
          "governs next. It makes no promises about the decade ahead, which the republic will plan when it arrives.",
          ('document', 'assembly'), after_any=('cent_coast_first', 'cent_interior_first'), requires=(After('2005.1.1'),),
          reward=(Stability(0.03), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (POLITICS, LINE, STEEL, HARBOUR, ARMY, AIR, NEIGHBOURS, ASTEROID, LEDGER)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('winter_track_season', 'A Winter Track Season on the Plains',
                'Keep the track gangs on the plains section through one winter; adds a road level in the plains district once.',
                50, (Build('infrastructure', 1, 570), Stability(0.01)), requires=(Completed('rail_sidings'),)),
    DecisionDef('steel_price_floor', 'Set a Floor Under Steel Prices',
                'Guarantee the mills a minimum price for six months when export prices fall; it can be renewed each year.',
                35, (TimedIdea('price_floor', 180),), requires=(Completed('steel_census'),), cooldown=365),
    DecisionDef('coast_command_drill', 'Call a Coast Command Night Drill',
                'Run warships, fighters and lifeboats through a night drill on the harbour approaches; it can be repeated each year.',
                30, (XP('navy', 15), XP('air', 10), Stability(0.01)), requires=(HasFlag('harbour_command'),), cooldown=365),
    DecisionDef('frontier_market_days', 'Open Frontier Market Days',
                'Open the customs halls for a season of market days at reduced duties; it can be repeated each year.',
                25, (TimedIdea('market_days', 120),), requires=(Completed('nbr_map'),), cooldown=365),
    DecisionDef('town_shelter_drill', 'A Shelter Drill in Every Town',
                'Rehearse the asteroid warning and shelter routine in every district; it can be repeated within the year.',
                20, (Stability(0.02), WarSupport(0.01)), requires=(Completed('star_warning'),), cooldown=300),
    DecisionDef('post_the_roll', 'Post the Roll in Every Town Hall',
                'Display the new electoral roll in every town hall for public correction; a one-time act of trust.',
                30, (Stability(0.03),), requires=(HasFlag('roll_compiled'),)),
)
