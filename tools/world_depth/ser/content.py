"""Serenava (SER): bespoke national focus tree, era e1 (1991 to 2005).

Serenava owns nothing on 1 January 1991. It is one of Perbla's crown lands, and this tree
applies only once it exists as a released country; tools/release_foundations owns when and
how that happens, and nothing here assumes a date or a mechanism. Its own states are its
core (581, captioned Serenava) plus its history capital (236, captioned Sofern, which is a
Relentio core). Every build stays guarded by owns_state and targets only state 581.

Source layers. Mod provenance: the inherited history file, the Office of the Crown
character, the country names, the core state with its buildings, bunkers, ports, railways,
weather and place names, the Belkan War and Usean war outcome flags, and the Perbla spec
(tools/world_depth/pbl/content.py), whose crown-lands, border and air branches this tree
never contradicts. Official: a few ACES Chronicle rows used only as date anchors for
regional pressure. Everything else, including every Serenavian choice, office, idea,
building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='SER', name='Serenava', root='world', package='ser',
                  themes=('runway', 'gate', 'security'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Serenava history: monarchism ruling at 70 percent popularity with fascism, democratic and communism at 10 '
           'and neutrality at 0; elections not allowed (frequency 48); stability and war support 0.8; three research slots; no '
           'starting ideas; starting technology of battle tanks, infantry fighting vehicles, motorised rockets, marines and '
           'interwar anti-air, with no aircraft technology. The starting leader is the unnamed Office of the Crown '
           '(SER_ac_government_office, constitutional_monarchy), whose holder has not been established; the tree never names one.',
           'mod/2985041246/history/countries/SER - Serenava.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Principality of Serenava (monarchism), Republic of Serenava (democratic and neutrality), '
           'Socialist Federation of Serenava (communism), Serenavian State (fascism); adjective Serenavian. The three political '
           'answers here keep the Principality or the Republic names; no socialist or fascist path is offered.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Release-country scope: SER owns no state in 1991; its only core is 581 (owned and cored by PBL) and its history '
           'capital is 236 (a PBL and REL core). The generic core release case in the release intake places the capital in 581 '
           'at province 5535 and does not retain 236. tools/release_foundations owns when and how Serenava exists; this tree '
           'assumes neither, and every build targets 581 under an owns_state guard. The release network-repair decision is '
           'hidden because the footprint is already connected, so no branch is built around network repair. Opening laws from '
           'the intake: civilian_economy, export_focus and volunteer_only.',
           'tools/release_foundations/intake.json (SER); tools/release_foundations/network.py; '
           'tools/world_foundation/country_registry.json (SER); tools/world_starts/release_inventory.json (SER); '
           'docs/WORLD_RELEASE_FOUNDATIONS.md'),
    Source('Mod provenance',
           'Geography of state 581 (captioned Serenava): state category large_city with eight shared slots, three civilian and '
           'two arms plants (three slots free), infrastructure 3, air base 10 (at its cap) with the airport on forest province '
           '9499, naval base 4 at Serdonia (5535, victory point 35) and naval base 5 at Karnaca (2999, victory point 30), level-5 '
           'bunkers on plains provinces 2257 (inland, on the rail line to the Osean state 544, captioned Wadsworth), 9475 and '
           '11343 (both coastal). Twelve provinces of plains and forest with two urban ports; supply nodes on 2999, 5535 and '
           '9499; level-2 railways to Gatewood Forest (389, via Baleton), Old Perbla (601), Faroe (173, via Driscol) and North '
           'Relentio (597, via Fraeport). Strategic region South Osean Gate (34): 18 to 35 degrees, light and heavy rain, mud, '
           'no snow. Place names come only from existing state, victory point and strategic region localisation.',
           'mod/2985041246/history/states/581-State_581.txt; mod/2985041246/map/definition.csv; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/supply_nodes.txt; mod/2985041246/map/airports.txt; '
           'mod/2985041246/map/strategicregions/34-South Osean Gate.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; '
           'mod/2985041246/localisation/english/strategic_region_names_l_english.yml'),
    Source('Mod provenance',
           'Consistency with the approved Perbla tree: Serenava as the crown land facing Osea, with the giant airfields, the '
           'bunker lines and the garrison towns and their workshops. Nothing here narrates which Perblan focuses were taken '
           'before Serenava governs itself, and nothing reuses the Relentio tree (tools/world_depth/rel/content.py).',
           'tools/world_depth/pbl/content.py (LANDS, HEAVY, BORDER and AIR branches); tools/world_depth/rel/content.py'),
    Source('Mod provenance',
           'Campaign hooks read only outcomes the mod already records: belka_lost_belkan_war and belka_won_belkan_war, set by '
           'the Belkan War events, and ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory, set by the Usean war '
           'script. Each is a separate gameplay branch; none is asserted as history.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Official', 'Date anchor only: the Ulysses close-approach warning.', '1994 / 12.10'),
    Source('Official', 'Date anchor only: the Belkan War breaks out.', '1995 / 03.25'),
    Source('Official', 'Date anchor only: the announcement that Ulysses will strike the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor only: former Belkan Air Force pilots are hired by various countries as aggressor squadrons.',
           '1998 / 06.19'),
    Source('Official', 'Date anchor only: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor only: the FCU demand to Erusea and the founding of the ISAF in Usea.', '2003 / 08.22'),
    Source('Official', 'Date anchor only: Farbanti falls and Erusea surrenders, ending the Continental War.', '2005 / 09.19'),
    Source('Provisional gameplay',
           'All Serenavian focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; no new place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('diet_unsettled', 'A Diet Without Standing Orders',
            'The diet sits and the crown office keeps the seals, but nobody has agreed what the deputies may decide.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('assembly', 'document')),
    IdeaDef('princely_course', 'The Princely Course',
            'Ministers come from the diet benches and the Office of the Crown signs on their advice.',
            {'stability_factor': 0.04, 'political_power_factor': 0.06}, ('ballot', 'command')),
    IdeaDef('garrison_course', 'Garrison Primacy',
            'The commandants of the garrison towns press to hold the seals of a frontier state.',
            {'political_power_gain': 0.15, 'war_support_factor': 0.04, 'stability_factor': -0.02}, ('security', 'command')),
    IdeaDef('township_course', 'The Township Movement',
            'Harbour wards and forest districts campaign for a republic of townships without a crown.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('assembly', 'civil')),
    IdeaDef('district_audiences', 'Open Audiences in the Districts',
            'Princely ministers hear complaints in drill halls, fish markets and forest schools.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05}, ('ballot', 'civil')),
    IdeaDef('prefect_commandants', 'Garrison Prefects',
            'Serving commandants run the districts around their garrisons under one signature.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02, 'army_core_defence_factor': 0.04}, ('command', 'security')),
    IdeaDef('open_budgets', 'Budgets on the Notice Board',
            'Every township posts its budget line by line before it receives state funds.',
            {'stability_factor': 0.03, 'political_power_factor': 0.05}, ('scales', 'civil')),
    IdeaDef('princely_constitution', 'The Princely Statute in Force',
            'One printed text says what the crown office signs alone and what needs the diet.',
            {'stability_factor': 0.07, 'political_power_factor': 0.08}, ('scales', 'command')),
    IdeaDef('garrison_code', 'The Garrison Ordinance in Force',
            'The council rules by a published ordinance that any citizen may read and appeal against.',
            {'political_power_gain': 0.20, 'war_support_factor': 0.06, 'army_core_defence_factor': 0.04}, ('security', 'document')),
    IdeaDef('republic_charter', 'The Ratified Township Charter',
            'A short charter fixes the court, the township shares of revenue and the rules for amendment.',
            {'stability_factor': 0.06, 'research_speed_factor': 0.03, 'consumer_goods_factor': -0.03}, ('assembly', 'scales')),
    IdeaDef('examined_service', 'A Service by Examination',
            'Clerks recruited by open examination now hold the senior posts of every ministry.',
            {'political_power_factor': 0.06, 'stability_factor': 0.03}, ('document', 'training')),
    # the airfields
    IdeaDef('idle_hangars', 'Hangars Without Squadrons',
            'Runways and shelters sized for a large air arm, maintained every month for a state with no aircraft.',
            {'political_power_gain': -0.05, 'air_detection': 0.03}, ('runway', 'document')),
    IdeaDef('cargo_fields', 'Freight on the Forest Field',
            'Freight airlines lease hangars and an overhaul trade grows on the military aprons.',
            {'production_speed_buildings_factor': 0.05, 'consumer_goods_factor': -0.03}, ('runway', 'economy')),
    IdeaDef('air_guard', 'The Serenavian Air Guard',
            'A few interceptor squadrons and trained controllers to watch a frontier sky.',
            {'air_superiority_efficiency': 0.06, 'experience_gain_air_factor': 0.08}, ('air', 'security')),
    IdeaDef('cargo_concourse', 'The Pine Concourse',
            'Cargo moves from aircraft to wagons in a long shed beside the forest field.',
            {'production_speed_buildings_factor': 0.08, 'consumer_goods_factor': -0.05, 'industrial_capacity_factory': 0.03},
            ('logistics', 'runway')),
    IdeaDef('guard_wing', 'Dawn Alert Wing',
            'Armed interceptor pairs wait at every dawn with crews asleep beside them.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.08, 'experience_gain_air_factor': 0.08}, ('air', 'radar')),
    IdeaDef('aggressor_school', 'The Aggressor Syllabus',
            'Hired instructors teach Serenavian crews to fight an opponent who knows how to win.',
            {'experience_gain_air_factor': 0.12, 'air_mission_efficiency': 0.04}, ('training', 'air')),
    IdeaDef('hangar_rent', 'Hangar Rents for a Season',
            'A row of outer hangars rented to private operators for one season.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('economy', 'runway')),
    # the casemate belt
    IdeaDef('belt_survey', 'The Casemate Survey',
            'Every gallery, door and gun port of the belt counted and graded.',
            {'army_core_defence_factor': 0.03}, ('security', 'document')),
    IdeaDef('belt_static', 'Concrete in Depth',
            'Gun crews in every casemate, infantry behind them and tanks held close.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.04}, ('security', 'shelter')),
    IdeaDef('armour_reserve', 'Armour Behind the Belt',
            'Small casemate crews delay; an armoured reserve strikes where the line breaks.',
            {'army_speed_factor': 0.05, 'army_attack_factor': 0.04, 'army_org_factor': 0.03}, ('command', 'security')),
    IdeaDef('volunteer_regiments', 'Volunteer Frontier Regiments',
            'Long-service volunteers from the garrison towns on family housing and civil job guarantees.',
            {'training_time_army_factor': -0.08, 'experience_gain_army_factor': 0.06}, ('medal', 'training')),
    IdeaDef('frontier_reserve', 'The Garrison Town Reserve',
            'Former volunteers on reserve rolls, training two weeks each summer.',
            {'training_time_army_factor': -0.12, 'army_core_defence_factor': 0.06, 'experience_gain_army_factor': 0.06},
            ('medal', 'civil')),
    IdeaDef('casemate_marines', 'Shore Casemate Marines',
            'Marine companies hold the shore casemates and rehearse counter-landings on the beaches.',
            {'army_defence_factor': 0.03, 'naval_coordination': 0.03}, ('navy', 'security')),
    IdeaDef('track_depots', 'Forest Track Depots',
            'Engine and track spares hidden under the trees behind the belt.',
            {'army_speed_factor': 0.04, 'supply_consumption_factor': -0.05}, ('tools', 'logistics')),
    # the workshops
    IdeaDef('workshop_ledger', 'Workshops on One Sheet',
            'Three civilian works and two arms halls, counted, and almost all of them living on army orders.',
            {'production_factory_efficiency_gain_factor': 0.02}, ('industry', 'document')),
    IdeaDef('apprentices', 'Apprentices at the Bench',
            'Paid trainee benches in every hall, certified by the state.',
            {'research_speed_factor': 0.02, 'production_factory_max_efficiency_factor': 0.03}, ('training', 'tools')),
    IdeaDef('civil_workshops', 'Workshops for Town Goods',
            'The halls make pumps, cable, tools and tinned food for many buyers.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': -0.03}, ('rebuild', 'industry')),
    IdeaDef('armour_arsenal', 'The Overhaul Trade',
            'Foreign armies send engines and running gear to Serenavian halls for overhaul.',
            {'production_speed_arms_factory_factor': 0.10, 'repair_speed_factor': 0.08}, ('tools', 'industry')),
    IdeaDef('civil_upgrade', 'Workshop Goods Abroad',
            'Garrison-town tools and household goods sold with export credit at foreign fairs.',
            {'production_speed_industrial_complex_factor': 0.12, 'consumer_goods_factor': -0.05}, ('economy', 'industry')),
    IdeaDef('arsenal_upgrade', 'Long Overhaul Contracts',
            'Multi-year refit contracts with armies that run older armour.',
            {'production_speed_arms_factory_factor': 0.12, 'industrial_capacity_factory': 0.05}, ('tools', 'document')),
    IdeaDef('export_house', 'The Serdonia Export House',
            'A joint sales office that takes Serenavian samples to foreign buyers.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': 0.01}, ('economy', 'diplomacy')),
    # the junction
    IdeaDef('freight_count', 'The Junction Tally',
            'A month of wagons counted at every yard where the lines meet.',
            {'production_speed_infrastructure_factor': 0.08}, ('rail', 'document')),
    IdeaDef('open_gate', 'The Open Gate Tariff',
            'One published transit tariff, clearance on the train and no searches without cause.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': 0.05}, ('gate', 'economy')),
    IdeaDef('guarded_gate', 'The Guarded Gate',
            'Every wagon crossing the frontier is sealed, logged and inspected.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.03}, ('gate', 'security')),
    IdeaDef('bonded_wagons', 'Sealed Wagons in Transit',
            'Bonded freight crosses Serenava unopened when its seals arrive intact.',
            {'consumer_goods_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'economy')),
    IdeaDef('customs_brigade', 'Brigades of the Frontier Customs',
            'Former soldiers with trucks, dogs and radios patrol between the crossings.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('security', 'gate')),
    IdeaDef('junction_board', 'One Timetable for Four Lines',
            'A single board runs the timetable, the dispatch room and the budget of every line.',
            {'planning_speed': 0.05, 'production_speed_infrastructure_factor': 0.10}, ('rail', 'command')),
    IdeaDef('gravel_gangs', 'Gravel Gangs on the Plains',
            'Paid gangs regravel the village roads before the rains.',
            {'production_speed_infrastructure_factor': 0.10}, ('tools', 'civil')),
    # the harbours
    IdeaDef('twin_harbours', 'Two Harbours, Two Ledgers',
            'Serdonia and Karnaca keep separate books and chase the same small trade.',
            {'navy_org_factor': 0.03, 'naval_coordination': 0.02}, ('navy', 'document')),
    IdeaDef('fishing_cooperatives', 'Crews Who Sell Together',
            'Crews sell together through their own ice plants and auction halls.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('fishing', 'economy')),
    IdeaDef('harbour_board', 'One Board for the Coast',
            'Common dues, one investment budget and one set of pilots for both harbours.',
            {'production_speed_buildings_factor': 0.04, 'naval_coordination': 0.03}, ('navy', 'command')),
    IdeaDef('rival_dues', 'Rival Harbour Dues',
            'Each harbour sets its own fees and competes for every coaster.',
            {'consumer_goods_factor': -0.03, 'stability_factor': -0.01}, ('navy', 'scales')),
    IdeaDef('harbour_patrol', 'The Karnaca Flotilla',
            'Patrol craft from Karnaca watch the fishing grounds and the shore casemates.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.04}, ('navy', 'security')),
    IdeaDef('minesweepers', 'Coastal Sweeping Crews',
            'Two patrol craft fitted and drilled to clear the coastal lanes.',
            {'naval_speed_factor': 0.03, 'naval_coordination': 0.04}, ('navy', 'tools')),
    # neighbours
    IdeaDef('gatewood_standards', 'Perblan Gauge and Standards',
            'One rail gauge, Perblan technical norms and matched customs rates.',
            {'production_speed_infrastructure_factor': 0.08, 'stability_factor': 0.03}, ('rail', 'diplomacy')),
    IdeaDef('osean_traders', 'Osean Trade Missions',
            'Osean buyers and technical standards welcomed at the frontier offices.',
            {'consumer_goods_factor': -0.04, 'industrial_capacity_factory': 0.03}, ('diplomacy', 'economy')),
    IdeaDef('even_frontier', 'Equal Distance from All',
            'One tariff for every neighbour and envoys of equal rank in every capital.',
            {'political_power_gain': 0.08, 'army_core_defence_factor': 0.04}, ('peace', 'scales')),
    # the Belkan War years
    IdeaDef('frontier_alert', 'The Frontier on Alert',
            'Posts doubled, patrols lengthened and leave cancelled while war burns beyond Osea.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.04, 'consumer_goods_factor': 0.03}, ('security', 'communications')),
    IdeaDef('transit_closed', 'Closed to Belligerent Trains',
            'No soldier, weapon or military store for any party crosses the junction.',
            {'stability_factor': 0.04, 'army_core_defence_factor': 0.04}, ('gate', 'peace')),
    IdeaDef('relief_trains', 'Marked Relief Trains',
            'Food, medicine and civilian goods for anyone, marked and searched at the crossing.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'medical')),
    IdeaDef('stand_to', 'Regiments Standing To',
            'Crews at their posts and reserves called while the war lasts.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.03}, ('security', 'training')),
    IdeaDef('fuel_ration', 'Fuel on Ration Cards',
            'Stored aviation spirit and diesel released at a controlled price.',
            {'stability_factor': 0.04, 'supply_consumption_factor': -0.03}, ('economy', 'logistics')),
    IdeaDef('neutral_freight', 'Neutral Air Freight',
            'Civil cargo flights under large neutral markings on filed routes.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': -0.01}, ('runway', 'peace')),
    IdeaDef('osean_drawdown', 'A Quieter Plain',
            'Osean columns gone home and the crossings back to their old routines.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.02}, ('peace', 'gate')),
    IdeaDef('osean_buildup', 'A Hardened Plain',
            'New fortifications and cold offices on the far side of the frontier.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.04, 'consumer_goods_factor': 0.03}, ('security', 'gate')),
    # Ulysses
    IdeaDef('sky_dread', 'The Asteroid Over Serdonia',
            'Every district plans for fragments that may fall anywhere.',
            {'stability_factor': -0.03, 'war_support_factor': 0.02}, ('meteor', 'shelter')),
    IdeaDef('public_casemates', 'Families in the Casemates',
            'Every household has a gallery, a warden and a route to the concrete.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('forest_shelters', 'Forest Shelter Trenches',
            'Timber-roofed trenches near every town, with the casemates kept for the regiments.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.02}, ('shelter', 'tools')),
    IdeaDef('hangar_depots', 'Relief Stores in the Hangars',
            'Grain, blankets, generators and medicine kept dry under hangar concrete.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('shelter', 'logistics')),
    IdeaDef('skyward_radar', 'Radars Turned Skyward',
            'Field radar sets retuned to watch the upper sky for falling rock.',
            {'air_detection': 0.08, 'research_speed_factor': 0.02}, ('radar', 'meteor')),
    IdeaDef('warden_rota', 'The Warden Rota',
            'A trained warden for every gallery, with lists, keys and rules.',
            {'stability_factor': 0.04, 'planning_speed': 0.05}, ('shelter', 'document')),
    # the new century
    IdeaDef('wartime_fuel', 'Fuel at Wartime Prices',
            'A distant war has made every litre dearer at the field, the harbours and the junction.',
            {'consumer_goods_factor': 0.03, 'stability_factor': -0.02}, ('economy', 'logistics')),
    IdeaDef('fuel_hedge', 'The Fuel Reserve Policy',
            'The state buys fuel when prices dip and sells when they spike.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('economy', 'scales')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('princely_cabinet', 'Cabinet of the Principality',
           'A cabinet chosen from the majority of the Serenavian diet that governs collectively in the name of the Principality '
           'and resigns when the deputies withdraw their confidence. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('garrison_council', 'Council of Frontier Commandants',
           'A council of serving commandants from the garrison towns that keeps the state seal, the treasury and the frontier '
           'posts, ruling by ordinance and calling the diet only when it wishes. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
    Office('township_executive', 'Executive of the Serenavian Townships',
           'An executive chosen by the diet of the Republic of Serenava at set intervals, with the princely office retired and '
           'the township councils keeping their own budgets. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('diet_drill_hall', 'The Diet in a Drill Hall', (
        "The first full sitting of the Serenavian diet takes place in a drill hall at Serdonia, because the only rooms large "
        "enough for every deputy were built for soldiers. Rifle racks have been carried out and benches carried in, and the "
        "painted lines for parade still show beneath the borrowed carpets. The Office of the Crown sends a written greeting "
        "and a short list of what it already handles: the seals, the garrison payroll and the frontier posts.",
        "The deputies arrive with very different instructions. Members from the garrison towns want the commandants heard on "
        "every budget, since the regiments employ half the inland districts. The harbour wards of Serdonia and Karnaca want "
        "customs and fishing rules settled before anything else. The forest districts want roads, schools and a voice that is "
        "not drowned out by uniforms or ships. Most deputies sit with the monarchist majority, and even they disagree about "
        "how much the crown office should do on its own.",
        "Before any law can pass, the diet has to agree how it will work at all. One proposal borrows a complete set of "
        "standing orders from an older chamber and adopts it in a single day, giving the clerks a rulebook they already know. "
        "The other asks the deputies to write their own, slowly and clause by clause, so that every district can see its "
        "interests in the procedure itself.",
    ), (
        Option('Adopt the borrowed standing orders.', (PP(30), Stability(-0.01))),
        Option('Write our own rules, clause by clause.', (Stability(0.03), PP(-15))),
    ), picture=2),
    EventDef('hangar_count', 'Hangars Built for Someone Else', (
        "The inspectors who walk the forest airfield need three full days to finish. Runways long enough for heavy transports "
        "cut through the pines, taxiways branch off to hardened shelters, and the fuel farms could keep a large air arm flying "
        "for weeks. The lights work and the doors open. Almost nothing parked inside belongs to Serenava, whose inventory lists "
        "tanks, rocket batteries and marines but not one combat aircraft of its own.",
        "The fields were laid out by older governments for a much larger air arm, and their scale reflects that purpose rather "
        "than any budget Serenava can now carry. Keeping the concrete patched, the drains clear and the radar sets warm costs "
        "money every month, whether or not anything takes off. Local contractors have lived on that maintenance for years, and "
        "their foremen have already asked the diet to keep the work coming.",
        "The inspectors hand the ministry a blunt first choice. Most of the outer shelters could be mothballed at once, cutting "
        "the monthly bill and accepting that reopening them later will be slow and costly. Or the whole complex could be kept "
        "in working order while the state decides what its fields are for, paying for a readiness it cannot yet use.",
    ), (
        Option('Mothball the outer shelters.', (PP(25), Stability(-0.01))),
        Option('Keep every runway open.', (PP(-20), XP('air', 10))),
    ), picture=0),
    EventDef('belt_concrete', 'Concrete Along the Line', (
        "The survey teams start at the inland casemates, where the rail line leaves the plains for Osea, and finish at the two "
        "groups of shore casemates on the coastal plain. The concrete is thick and mostly sound. The wiring is not, several "
        "periscopes have fogged beyond use, and a number of ammunition rooms turn out to be full of ploughs and seed sacks left "
        "by farmers who have treated the bunkers as barns for years.",
        "Whoever poured the belt expected an Osean army on the plains one day, and its size dwarfs anything Serenava's volunteer "
        "regiments could ever man. Commandants say that empty casemates invite trouble and that a frontier state must look ready even when it "
        "is not. Treasury officials answer that every manned casemate is a salary, a ration and a fuel bill. The farmers simply "
        "want their barns back before the rains.",
        "The survey closes on a question the army cannot settle by itself. The belt can be treated as a living defence line, "
        "with crews, drills and repairs that never stop. Or it can be held as a reserve of concrete, sealed and checked twice "
        "a year, until the government knows what the frontier will actually demand of it.",
    ), (
        Option('Crew the casemates.', (WarSupport(0.03), PP(-15))),
        Option('Seal them and check twice a year.', (PP(20), Stability(0.01))),
    ), picture=2),
    EventDef('workshop_floor', 'The Workshop Floor Count', (
        "The industry clerks finish their count of the garrison-town workshops on a wet afternoon, and the result fits on one "
        "sheet of paper. Three civilian works make tools, cable, tinned goods and spare parts. Two arms halls overhaul tank "
        "engines, rebuild running gear and fill shells for the regiments. Between them they employ most of the skilled hands "
        "inland, and almost every order in their books carries an army stamp.",
        "That dependence is the whole difficulty. A regiment that stops buying can empty a street of shops within a season. The "
        "halls are well equipped for repairing heavy vehicles and poorly equipped for anything a family would buy. Foremen say "
        "their workers could learn new lines within a year; bankers say nobody will lend a coin for conversion until the state "
        "says plainly what it wants the workshops to become.",
        "The clerks offer two ways to release their sheet. It can be published with the payroll figures and the army share of "
        "the orders, starting a public argument that will run until the choice is made. Or it can go to the ministries alone, "
        "so officials settle the matter among themselves while rumours spread through every garrison town.",
    ), (
        Option('Publish the payroll and the order book.', (Stability(-0.02), Research('industry', 0.5, 1))),
        Option('Send the count to the ministries only.', (PP(30), Stability(-0.01))),
    ), picture=1),
    EventDef('junction_freight', 'Freight at the Junction', (
        "For a month the railway clerks at every Serenavian yard write down each wagon that passes. Trains run toward Gatewood "
        "by way of Baleton, into Old Perbla past the forest field, through Karnaca to Driscol and Fraeport, and across the "
        "plains to the Osean frontier. Serenava sits where all of those lines cross, and the tally shows how much of the "
        "traffic is merely passing through on its way somewhere else.",
        "Through-freight pays Serenava little under the old rates. It wears out the track, blocks the level crossings in the "
        "garrison towns and fills the yards every night. Yet shippers on every side rely on the junction, and a small state "
        "that makes itself useful to its neighbours enjoys a kind of security that no casemate can provide. In the rainy "
        "months the roads beside the lines turn to mud, and the railway becomes the only dependable way to move anything.",
        "The clerks want to know what their tally is for. Used as the basis for a new transit tariff, it would raise revenue "
        "and irritate every neighbour at once. Used only to plan repairs and sidings, it would keep goodwill on all sides and "
        "leave the junction paying for its own wear.",
    ), (
        Option('Draft a transit tariff from the tally.', (PP(25), Stability(-0.01))),
        Option('Use it to plan repairs only.', (Stability(0.02), PP(-10))),
    ), picture=1),
    EventDef('two_harbours', 'Serdonia and Karnaca Compare Books', (
        "The harbour masters of Serdonia and Karnaca are summoned to bring their accounts to the same table for the first time "
        "anyone can remember. Serdonia is the larger town, with the busier markets and the older quays. Karnaca has the deeper "
        "naval berths and the railway toward Driscol and Fraeport. Each town has always believed the other was favoured, and "
        "the books, laid side by side, give both of them some evidence.",
        "Both harbours handle fish, coastal freight and the stores for the shore casemates. Neither has the dredgers, tugs or "
        "haul-out to service a real ship, so serious repairs go abroad and the money goes with them. The naval berths stand "
        "half empty because Serenava owns few vessels to fill them. Above all, the fishing crews complain that they are "
        "charged landing fees twice, once at each harbour, whenever weather forces them to switch ports.",
        "The cooperatives of both towns now demand that the double fees end and that past payments be returned. Refunding "
        "everything would win the fleets over and drain the harbour accounts for a year. Abolishing the fees from next season "
        "only would cost far less and leave a grievance that every fishing family can recite.",
    ), (
        Option('Refund the double fees.', (PP(-20), Stability(0.03))),
        Option('Abolish them from next season.', (PP(10), Stability(0.01))),
    ), picture=2),
    EventDef('envoy_rounds', 'Four Calls in One Week', (
        "Serenava's first envoys travel by rail, since the rail is what ties the state to everyone around it. In a single week "
        "they call at Gatewood, at the offices that govern the Relentian ports and the Terentio towns, whoever those offices "
        "now answer to, and at the Osean frontier administration across the plains. Each call opens with the same dull and "
        "necessary questions: customs seals on through-trains, radio frequencies for the field towers and fishing limits off "
        "Karnaca.",
        "Gatewood receives the envoys correctly and asks about the airfields and the casemates before anything else. The "
        "officials from the Relentian ports want the Karnaca line kept running at any price. Terentio's people ask mostly "
        "about freight rates and empty return wagons. The Osean officials are courteous, curious and careful, and they ask "
        "nothing at all about the past, which the envoys find more unsettling than any complaint.",
        "On their return the envoys report that every neighbour wants something from Serenava and that no two want the same "
        "thing. Ministers can answer with one published line of policy for all of them, or deal with each neighbour "
        "separately and quietly, accepting that four private answers may not match when they are compared.",
    ), (
        Option('Publish one policy for every neighbour.', (Stability(0.02), PP(-15))),
        Option('Handle each neighbour separately.', (PP(25),)),
    ), picture=1),
    EventDef('war_beyond_line', 'The War Beyond the Line', (
        "When the Belkan War breaks out in March 1995, Serenava has no stake in the fighting, but Osea does, and Osea lies "
        "directly across the plains from the inland casemates. Within days the frontier posts report heavier traffic on the Osean side: fuel "
        "trucks, ambulances and trains running at night with their windows blacked out. Radio sets in the garrison towns pick "
        "up military chatter that nobody in Serenava was ever meant to hear.",
        "Serenava's own position is uncomfortable. The giant airfields and the casemate belt were built facing Osea, and Osean "
        "officers know every one of them by heart. A neutral state with that much concrete pointed at a belligerent has to "
        "prove that it means no harm, while a frontier state with so small an army must also prove that it cannot be pushed "
        "around. The monarchist benches call for calm; the garrison towns call for every regiment to stand to.",
        "On the fourth day an Osean liaison officer arrives at the inland crossing with a polite letter. Osea asks to place "
        "observers at the frontier posts for the duration of the war, to reassure its commanders that nothing will move "
        "against them from Serenavian soil. Accepting would calm the line and look like a favour to one side. Refusing would "
        "keep Serenava visibly its own master and leave the Osean commanders guessing.",
    ), (
        Option('Accept the observers at the posts.', (Stability(0.02), Event('observers_posted', 20))),
        Option('Refuse, and invite them to watch from their side.', (WarSupport(0.03), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; every Serenavian and Osean '
                'action described is gameplay', picture=2),
    EventDef('observers_posted', 'Observers at the Inland Post', (
        "Twenty days after the letter, four Osean officers and a radio operator share a hut with Serenavian customs staff at "
        "the inland crossing. They eat in the post canteen, sign the visitors book every morning and file reports that nobody "
        "in Serenava is allowed to read. The arrangement is awkward, and both sides go to some lengths to keep it polite.",
        "In the garrison towns the observers become a favourite topic of argument. Some residents are relieved: as long as the "
        "Oseans can see for themselves, nobody across the plains will mistake a Serenavian exercise for an attack. Others "
        "resent foreign uniforms on their soil while a war burns beyond Osea, and the commandants complain that the observers "
        "count every truck, every gun and every soldier who goes on leave.",
        "The Osean liaison now proposes a second step: a direct telephone line from the inland post to the nearest Osean "
        "frontier headquarters, manned at both ends day and night. Such a line would let a misunderstanding be settled in "
        "minutes. It would also tie the daily routine of Serenava's frontier to an Osean switchboard for as long as the line "
        "exists.",
    ), (
        Option('Install the direct line.', (Stability(0.03), PP(-10))),
        Option('Keep contact through the observers only.', (PP(20), WarSupport(0.01))),
    ), picture=2),
    EventDef('asteroid_casemates', 'The Asteroid and the Casemates', (
        "Since December 1994 astronomers had spoken of a close pass. In April 1996 the talk ends: Ulysses is coming, it will "
        "hit, and the impact zones are a matter of guesswork for months to come. Serenava owns no observatory worth the name "
        "and no rocket, satellite or telescope with which to follow the danger. What it owns instead is rare among small "
        "states, a belt of reinforced casemates and a forest airfield full of hardened shelters.",
        "Within a week, families from Serdonia and Karnaca are seen walking out to the shore casemates with blankets and tinned "
        "food to test the doors. Commandants want the bunkers kept for the regiments; mayors want them opened to children and "
        "the elderly. The airfield contractors offer to fit out the hangars as relief stores, at a price. In the harbour towns "
        "candles, batteries and bottled water double in cost before the month is out.",
        "Before choosing how to use the concrete, ministers have to tell a frightened public something. A full statement of "
        "what is known and unknown would include the uncomfortable fact that the casemates cannot shelter everyone. A short "
        "announcement that planning is under way would buy calm, at the risk of being accused later of hiding the arithmetic.",
    ), (
        Option('Publish the arithmetic.', (Stability(-0.02), WarSupport(0.02), Research('construction_tech', 0.5, 1))),
        Option('Ask for patience while plans are drawn.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; the '
                'Serenavian reaction is gameplay', picture=0),
    EventDef('roche_watch', 'Radar Watch on the Roche Night', (
        "On the night Ulysses passes the Roche limit in July 1999, the radar sets on the Serenavian fields are pointed upward "
        "for the first time in their working lives. Operators trained to track low-flying aircraft now report streaks, flashes "
        "and phantom returns, very few of which mean anything. Each report travels by telephone to a control room where tired "
        "officials must decide whether to wake the districts.",
        "In the shelters, families listen to the radio and wait. Some sleep; many cannot. Rail crews keep the evacuation trains "
        "warm at the junction, and the forest districts hold their fire wardens on duty in case burning debris lands among the "
        "pines. Rumour runs faster than any report: a fire at sea, a radio station gone silent, a train missing somewhere "
        "between Karnaca and the forest field.",
        "By dawn the control room has logged dozens of alarms and confirmed very few of them, and the observatories abroad "
        "cannot yet say when the danger will end. Ministers can keep the full alert in force until foreign agencies declare the "
        "sky clear, or release most of the shelters and keep only the radar crews and the fire wardens on watch.",
    ), (
        Option('Hold the full alert.', (WarSupport(0.02), Stability(-0.02))),
        Option('Release the shelters and keep the watch.', (Stability(0.03),)),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; the Serenavian watch is '
                'gameplay', picture=0),
    EventDef('aggressor_offer', 'Instructors Who Once Flew for Belka', (
        "In the summer of 1998 a small agency writes to the Serenavian air staff offering instructors for hire. Its pilots are "
        "former Belkan Air Force aviators, some of the most capable the war produced, now selling their experience to any air "
        "arm that will pay. Air arms across the world are already hiring such pilots to fly as aggressors against their own "
        "crews. The letter is short, professional and accompanied by a price list.",
        "The offer is tempting. Serenava's fields have more runway than pilots, and its training staff has never flown against "
        "an opponent who knows how to win. The instructors would bring their own methods, fly against Serenavian crews over "
        "the forest field and leave behind a syllabus that would take a decade to build at home. Their fee is high, and they "
        "want it in foreign currency.",
        "The price is more than money. Hiring former Belkan aviators will be noticed in Osea, just across the plains, and the "
        "harbour deputies worry about what Osean buyers will think. The air staff argues that a neutral state may hire whomever "
        "it pleases. The foreign office replies that neutrality is judged by neighbours rather than by lawyers.",
    ), (
        Option('Sign the instructors for two seasons.', (TimedIdea('aggressor_school', 730), Event('aggressor_review', 45))),
        Option('Decline with thanks.', (PP(20), Stability(0.01))),
    ), citation='date anchor only, ACES Chronicle row 1998 / 06.19 in tools/lore/chronicle.json; any Serenavian hiring is '
                'gameplay', picture=0),
    EventDef('aggressor_review', 'The First Aggressor Report', (
        "After six weeks of mock combat over the forest field, the hired instructors hand in their first written assessment. "
        "It is not kind. Serenavian crews fly carefully and shoot late; they trust the ground controllers too much and their "
        "own eyes too little. Several sorties ended with every trainee shot down before the instructors had burned half "
        "their fuel.",
        "In its own way the report is also generous. The instructors praise the ground crews, the fuel discipline and the "
        "radar controllers, and they write that the crews who survived the first weeks are learning faster than any group "
        "they have trained elsewhere. They ask for more flying hours, more targets and permission to train over the sea off "
        "Karnaca, where the coastal radar can follow every engagement.",
        "The air staff must now choose whether to keep the programme narrow, confined to the forest field and the hours "
        "already agreed, or widen it as the instructors ask. A wider programme would cost more fuel, wear out more airframes "
        "and draw more attention from neighbours who already watch every flight Serenava makes. A narrow programme would "
        "finish on time and leave the crews only half taught.",
    ), (
        Option('Widen the programme.', (XP('air', 25), PP(-15))),
        Option('Keep it within the agreed hours.', (XP('air', 10), Stability(0.01))),
    ), picture=0),
    EventDef('frontier_stock', 'The Frontier Takes Stock', (
        "A panel of deputies, commandants, harbour masters and railway clerks is asked to describe what Serenava has become "
        "since it began governing itself. Their report is plain. The diet sits under rules it wrote or borrowed, the junction "
        "carries more freight than before, and the workshops sell to more buyers than the army alone. The casemate belt still "
        "stands, crewed or sealed, and the great airfields still dwarf everything else on the map.",
        "The panel is just as plain about failures. The forest districts still feel that decisions are taken in Serdonia and "
        "paid for by them. Young engineers leave for jobs in larger countries and seldom return. Too much of the economy "
        "depends on traffic through the junction and on contracts tied to the airfields, and either could vanish with a "
        "decision taken in some other capital.",
        "Ministers now have to receive the report somehow. Every finding could go to the diet for debate, with a written reply "
        "to each, inviting a hard year of criticism. Or the recommendations that suit the government could be adopted at once "
        "and the rest filed away, keeping the political year quiet and leaving the hardest problems for whoever governs next.",
    ), (
        Option('Debate every finding in the diet.', (Stability(0.03), PP(-20))),
        Option('Adopt what suits us and file the rest.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('usean_fuel', 'Fuel Bills from a Distant War', (
        "War returns to the news in August 2003, this time on the far continent of Usea, where the FCU demands that Erusea "
        "withdraw and founds the ISAF. Serenava has no part in that quarrel and no forces anywhere near it. Its fuel merchants, "
        "however, read the shipping news before anything else, and by the end of the week the price of aviation spirit at the "
        "forest field has jumped sharply.",
        "The airfields feel it first, as freight operators and training staff alike ask the treasury for fuel credit. The "
        "harbour towns feel it next, when the fishing crews find their diesel dearer every time they fill up. In the garrison "
        "towns the workshops discover that spare parts ordered from abroad now arrive late and cost more, because every "
        "supplier is busy with orders from larger buyers.",
        "The ministry can draw down the fuel farms built for a far larger air arm, selling stored fuel to local users at a "
        "controlled price until the market settles. Or it can leave the stocks untouched, as a reserve against a worse crisis "
        "closer to home, and let prices do their unpleasant work. The fuel farm managers say they can deliver either way "
        "within a week.",
    ), (
        Option('Release fuel from the farms.', (Stability(0.02), PP(-15))),
        Option('Hold the stocks untouched.', (PP(20), WarSupport(0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / 08.22 in tools/lore/chronicle.json; the Serenavian fuel response is '
                'gameplay', picture=1),
    EventDef('border_market', 'Market Day at the Crossing', (
        "Once a season the inland crossing closes to freight for a day and opens to traders. Farmers from the plains bring fruit "
        "and timber, workshop cooperatives bring tools and cable, and buyers arrive from the Osean side and from the old crown "
        "lands with cash and order books. Customs staff set up trestle tables across the road, and the casemates above the "
        "crossing look down on what is, for one day, a fairground.",
        "The markets are popular and untidy. Smugglers use the crowds, prices are argued over in several accents, and the "
        "commandants dislike open gates on the most sensitive stretch of the frontier. Yet the trade is real, the stalls sell "
        "out by evening, and for a day the garrison towns see foreign customers rather than foreign uniforms on the far side "
        "of the barrier.",
        "This season the traders ask for a second day and a covered hall, so that rain no longer spoils the stalls. The customs "
        "office can grant both and collect a modest fee for the hall, or keep the market to a single day and keep the frontier "
        "routine as undisturbed as possible. The commandant at the crossing has already made a preference known.",
    ), (
        Option('Grant the second day and the hall.', (Stability(0.02), PP(-10))),
        Option('Keep it to a single day.', (PP(15),)),
    ), picture=1),
)

# --- branches ------------------------------------------------------------------------------------
GOVERN = Branch('gov', 'The Diet of Serenava', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('gov_diet_sits', 'The Serenavian Diet Sits',
          "Serenava governs itself through the Office of the Crown and a diet whose deputies come from the garrison towns, the "
          "harbour wards of Serdonia and Karnaca and the forest districts between them. The monarchist camp holds a large "
          "majority, yet nobody has written down what the diet may decide. Convening it now costs the crown office its quiet.",
          ('assembly', 'ballot'), reward=(Idea('diet_unsettled'), Event('diet_drill_hall'))),
    Focus('gov_deputy_roll', 'A Roll of Seats by District',
          "Before the diet can argue about power it must agree on who sits in it. Clerks draw up a roll of seats by district, "
          "weighing the populous harbour wards against the garrison towns and the thinly settled forests. Every allocation "
          "offends somebody. The finished roll exposes three rival answers to the question of who should govern Serenava.",
          ('document', 'civil'), after=('gov_diet_sits',),
          reward=(PP(25), Tooltip('Three paths follow; choosing one closes the other two.'))),
    Focus('gov_princely_path', 'The Crown Office Signs on Advice',
          "The monarchist majority wants to keep the Principality and bind it to the diet: ministers chosen from the benches, "
          "budgets voted by deputies and the Office of the Crown signing what its cabinet advises. Most deputies already expect "
          "this answer. It also ends the crown office's habit of settling frontier questions by letter without consulting anyone.",
          ('ballot', 'command'), after=('gov_deputy_roll',), exclusive=('gov_garrison_path', 'gov_township_path'),
          reward=(SwapIdea('diet_unsettled', 'princely_course'),)),
    Focus('gov_garrison_path', 'Commandants Ask for the Seals',
          "The commandants of the garrison towns argue that a frontier state with a casemate belt and airfields of this size "
          "cannot wait on deputies when a crisis comes. Their proposal hands the state seal, the treasury and the "
          "frontier posts to a council of senior officers. Decisions would come quickly, and the diet would shrink into a place for petitions.",
          ('security', 'command'), after=('gov_deputy_roll',), exclusive=('gov_princely_path', 'gov_township_path'),
          reward=(SwapIdea('diet_unsettled', 'garrison_course'),)),
    Focus('gov_township_path', 'Townships Without a Prince',
          "A smaller camp in the harbour wards and the forest districts proposes a Republic of Serenava governed by an executive "
          "elected from the diet, with the princely office retired. Its supporters say a state of townships needs no crown. The "
          "garrison towns distrust the idea, and the monarchist majority will not soon forgive the deputies who carry it.",
          ('assembly', 'civil'), after=('gov_deputy_roll',), exclusive=('gov_princely_path', 'gov_garrison_path'),
          reward=(SwapIdea('diet_unsettled', 'township_course'),)),
    Focus('gov_princely_cabinet', 'Seat the Princely Cabinet',
          "The majority benches form a princely cabinet that holds the seals as a body and answers to the diet for each of them. "
          "No single minister can act without colleagues, and a lost vote of confidence brings the whole cabinet down. Elections "
          "return to the calendar. The commandants lose the private line to the crown office they have used for years.",
          ('ballot', 'assembly'), after=('gov_princely_path',), cost=10,
          exclusive=('gov_garrison_council', 'gov_township_executive'),
          reward=(Regime('princely_cabinet'), Flag('path_princely'))),
    Focus('gov_garrison_council', 'The Commandants Take the Seals',
          "Senior frontier commandants form a council that keeps the state seal, the treasury and the frontier posts and rules by "
          "ordinance, suspending elections for as long as it sits. The diet survives as a body the council consults when it chooses. Orders "
          "move fast along a chain of command, and from now on every failure of the state will wear a uniform.",
          ('command', 'security'), after=('gov_garrison_path',), cost=10,
          exclusive=('gov_princely_cabinet', 'gov_township_executive'),
          reward=(Regime('garrison_council'), Flag('path_garrison'))),
    Focus('gov_township_executive', 'Elect the Township Executive',
          "By a narrow vote the diet adopts a founding text for a republic and names an executive from among its members, sending "
          "the princely office to ceremony and the archives. The Republic of Serenava holds elections at set intervals. The "
          "harbour wards celebrate. "
          "The garrison towns watch warily, and the executive must persuade the officer corps that a republic can hold a frontier.",
          ('ballot', 'civil'), after=('gov_township_path',), cost=10,
          exclusive=('gov_princely_cabinet', 'gov_garrison_council'),
          reward=(Regime('township_executive'), Flag('path_township'))),
    Focus('gov_district_audiences', 'Ministers on the District Circuit',
          "The princely cabinet sends its ministers on a circuit of every district in turn, holding open audiences in drill "
          "halls, fish markets and forest schools. Complaints are written down and answered within a season. The circuit eats "
          "ministerial time and fills the papers with petty grievances, but it convinces outlying districts that the "
          "Principality hears them too.",
          ('ballot', 'rail'), after=('gov_princely_cabinet',), reward=(TimedIdea('district_audiences', 365),)),
    Focus('gov_commandant_prefects', 'Commandants as District Prefects',
          "The council appoints serving commandants as prefects of the districts around their garrisons, joining civil and "
          "military authority under a single signature. Roads, schools and police answer to officers who already know the "
          "ground. Administration turns brisk and uniform, while mayors and teachers resent taking orders from people trained "
          "to command regiments rather than towns.",
          ('command', 'civil'), after=('gov_garrison_council',), reward=(TimedIdea('prefect_commandants', 365),)),
    Focus('gov_township_budgets', 'Township Budgets on Public Boards',
          "Every township in the Republic posts its budget on a public board and in the local paper, line by line, before the "
          "executive may release its share of state funds. Small frauds grow harder and quarrels grow louder. Councils spend "
          "weeks defending the price of a culvert, yet citizens begin to trust that tax money arrives where it was promised.",
          ('scales', 'civil'), after=('gov_township_executive',), reward=(TimedIdea('open_budgets', 365),)),
    Focus('gov_clerk_exams', 'Examinations for Frontier Clerks',
          "Whatever form of government Serenava chose, it still needs clerks who can run customs posts, payrolls and land "
          "registers. Open examinations replace letters of recommendation for every junior post, and successful candidates are "
          "sent where they are needed rather than where they were born. The commandants dislike civilian testing, but the "
          "service begins to staff itself.",
          ('document', 'training'), after_any=('gov_district_audiences', 'gov_commandant_prefects', 'gov_township_budgets'),
          reward=(Flag('state_clerks'), PP(15))),
))

FIELDS = Branch('fields', 'The Giant Airfields', 1991, 'FOCUS_FILTER_AIR_XP', (
    Focus('fields_count', 'Count the Hangars and Fuel Farms',
          "Serenava holds the giant airfields that older governments built facing Osea, with runways, hardened shelters and fuel "
          "farms sized for a far larger air arm, yet its own inventory lists armour, rockets and marines and no combat aircraft "
          "at all. Counting what the fields hold, and what they cost each month, is the first honest step.",
          ('runway', 'document'), reward=(Idea('idle_hangars'), Event('hangar_count'))),
    Focus('fields_fuel_farms', 'Earth Banks Around the Fuel Farms',
          "The fuel farms beside the forest field are the largest stores of aviation spirit for many miles, and they sit behind "
          "thin fences. Engineers raise earth banks around the tanks, reline the pipes to the dispersal stands and fit new "
          "valves. The work buys nothing visible this year. It turns a standing liability into a reserve the state can draw on "
          "in a crisis.",
          ('shelter', 'logistics'), after=('fields_count',), reward=(Flag('fuel_banked'), Research('construction_tech', 0.5, 1))),
    Focus('fields_tower', 'A Civil Tower for the Forest Field',
          "The forest field has military approach radar but no civil control tower, so private and freight flights must ask the "
          "duty officer for leave to land. A proper tower with its own radar and radio watch makes the field usable by civil "
          "operators. It also gives the air staff a second pair of eyes over the forest districts and the frontier beyond them.",
          ('radar', 'runway'), after=('fields_count',), reward=(Build('radar_station', 1, 581), Research('radar_tech', 0.5, 1))),
    Focus('fields_cargo', 'Freight Wings for the Forest Field',
          "One school says the fields should earn their keep as a civil hub: freight airlines leasing hangars, overnight parcel "
          "flights and an overhaul trade for foreign operators. Revenue would replace maintenance bills. Serenava would remain "
          "without fighters of its own, and its airspace would rest on the goodwill of neighbours and on treaties nobody has "
          "yet written.",
          ('runway', 'economy'), after=('fields_count',), cost=10, exclusive=('fields_guard',),
          reward=(SwapIdea('idle_hangars', 'cargo_fields'), Flag('fields_freight'))),
    Focus('fields_guard', 'Raise a Serenavian Air Guard',
          "The other school says that a frontier state with this much runway must have an air arm of its own, however small: a "
          "few squadrons of interceptors, trained controllers and pilots drawn from the regiments. Buying and training them "
          "will consume years of budget. In return Serenava could watch and defend its own sky instead of hoping nobody tests it.",
          ('air', 'security'), after=('fields_count',), cost=10, exclusive=('fields_cargo',),
          reward=(SwapIdea('idle_hangars', 'air_guard'), Flag('air_guard_raised'))),
    Focus('fields_concourse', 'A Freight Concourse Under the Pines',
          "Freight operators want a concourse where cargo moves straight from aircraft to trucks and trains without crossing the "
          "military aprons. A long shed beside the forest field, linked to the junction by a rail spur, does exactly that. It is "
          "costly and slow to build. Once open, it draws parcel and spare-part traffic that never touches the casemate roads.",
          ('logistics', 'runway'), after=('fields_cargo',), reward=(SwapIdea('cargo_fields', 'cargo_concourse'),)),
    Focus('fields_alert_pairs', 'Alert Pairs at Dawn',
          "The air guard keeps a pair of armed interceptors ready on the forest field at every dawn, with crews sleeping beside "
          "their aircraft and controllers at the scopes. Readiness of this kind wears out airframes and patience alike. It also "
          "means that any intruder over Serenava will be met within minutes by aircraft carrying a Serenavian roundel.",
          ('air', 'radar'), after=('fields_guard',), reward=(SwapIdea('air_guard', 'guard_wing'), XP('air', 10))),
    Focus('fields_control_room', 'One Control Room for Every Field',
          "Civil and military traffic over the fields has been handled from separate huts with separate telephones. A single "
          "control room, fed by new radar sets on the forest edge, puts freight flights, training sorties and intruders on one "
          "display. The two staffs must learn to share a room and a rulebook, and the sky above Serenava holds fewer surprises.",
          ('radar', 'command'), after=('fields_tower',), after_any=('fields_concourse', 'fields_alert_pairs'),
          reward=(Build('radar_station', 2, 581),)),
    Focus('fields_aggressors', 'Aggressor Instructors for Hire',
          "From the summer of 1998, air arms abroad are hiring former Belkan Air Force pilots as aggressor instructors. The new "
          "control room gives Serenava a training airspace where such people could work. Whether to hire them is a hard "
          "question for a neutral state on the Osean frontier, and the air staff wants an answer before the offers go elsewhere.",
          ('training', 'air'), after=('fields_control_room',), requires=(After('1998.6.19'),),
          reward=(Event('aggressor_offer'),)),
))

BELT = Branch('belt', 'The Casemate Belt', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('belt_walk', 'Walk the Casemate Line',
          "Serenava inherits a casemate belt out of all proportion to its army: one heavy group on the plains where the rail line "
          "runs toward Osea, and two more on the coastal plain. Survey teams walk every gallery, test every door and count every "
          "gun port. The survey itself is cheap; deciding what to do with so much concrete is not.",
          ('security', 'document'), reward=(Idea('belt_survey'), Event('belt_concrete'))),
    Focus('belt_volunteers', 'Volunteer Regiments for the Frontier',
          "Serenava raises its army by volunteering, not conscription, and the garrison towns supply most recruits. Regular pay, "
          "housing for families and a guaranteed civil job after twelve years make enlistment attractive. The regiments stay "
          "small but professional. The price is a payroll that grows every year and a recruiting map that barely touches the "
          "harbour wards.",
          ('medal', 'training'), after=('belt_walk',), reward=(Idea('volunteer_regiments'),)),
    Focus('belt_tank_school', 'A Tank School on the Open Plains',
          "The regiments own modern battle tanks, infantry fighting vehicles and rocket batteries, but crews learn their trade in "
          "whatever field a farmer will lend. A permanent school on the plains behind the casemates gives them ranges, repair "
          "pits and a doctrine written for the ground they would defend. The farmers want compensation and get it.",
          ('training', 'command'), after=('belt_walk',), reward=(Research('land_doctrine', 0.5, 1), XP('army', 15))),
    Focus('belt_hold', 'Garrison the Casemates in Depth',
          "The static school says the belt is Serenava's greatest military asset and should be crewed in depth: gun crews in "
          "every casemate, infantry in the trenches behind them and the tanks held close for counterattacks. Any attacker would "
          "pay heavily for each kilometre. The regiments would be tied to the concrete and of little use anywhere else.",
          ('security', 'shelter'), after_any=('belt_volunteers', 'belt_tank_school'), cost=10, exclusive=('belt_mobile',),
          reward=(SwapIdea('belt_survey', 'belt_static'),)),
    Focus('belt_mobile', 'Tanks Behind the Concrete',
          "The mobile school says the casemates should only delay an attacker, held by small crews, while the real defence is an "
          "armoured reserve behind them that strikes wherever a breach opens. It suits the regiments' tanks and rocket batteries "
          "far better. It needs fuel, spare parts and trained commanders, and it leaves the shore casemates thinly manned.",
          ('command', 'security'), after_any=('belt_volunteers', 'belt_tank_school'), cost=10, exclusive=('belt_hold',),
          reward=(SwapIdea('belt_survey', 'armour_reserve'),)),
    Focus('belt_casemate_radar', 'Radar Above the Inland Casemates',
          "Crewed casemates are blind beyond their gun ports. A radar mast raised on a rise behind the inland group gives the "
          "crews early warning of anything moving on the plains or low in the sky, and wires them to the forest field's "
          "controllers. Osea will notice the new mast. The commandants count that as a benefit rather than a cost.",
          ('radar', 'security'), after=('belt_hold',), reward=(Build('radar_station', 1, 581), WarSupport(0.02))),
    Focus('belt_track_depots', 'Track Depots Behind the Belt',
          "A mobile reserve stands or falls on its spares. Drawing on the pool the workshops now keep, the army builds track and "
          "engine depots in the forest behind the belt, each stocked for a week of fighting and hidden under the trees. Depots "
          "tie up money in idle stock. They also keep the tanks moving when a road is cut.",
          ('tools', 'logistics'), after=('belt_mobile',), requires=(HasFlag('spares_pool'),), reward=(Idea('track_depots'),)),
    Focus('belt_shore_marines', 'Marines for the Shore Casemates',
          "The shore casemates face the sea, and the army has always treated them as an afterthought. Marine companies trained "
          "for coastal fighting take them over, rehearsing landings and counter-landings on the beaches nearby. The marines "
          "draw recruits from the tank regiments and quarrel with the harbour masters about closed beaches, but the coast "
          "finally has its own defenders.",
          ('navy', 'security'), after=('belt_walk',), reward=(Idea('casemate_marines'),)),
    Focus('belt_garrison_reserve', 'A Reserve from the Garrison Towns',
          "Veterans who leave the volunteer regiments go onto a reserve roll in their home garrison towns and report for two "
          "weeks of training each year. In a crisis the regiments could double within a fortnight. Employers lose workers "
          "every summer and grumble about it. The reserve costs little in peacetime and changes every sum an attacker would do.",
          ('medal', 'civil'), after=('belt_volunteers',), reward=(SwapIdea('volunteer_regiments', 'frontier_reserve'),)),
    Focus('belt_plains_manoeuvre', 'The Plains Manoeuvre',
          "Once a year the whole army takes the field on the plains behind the casemates, testing whichever defence the staff "
          "has chosen against an imagined attack across the frontier. Osean observers are invited, so nobody mistakes the "
          "exercise for anything else. The manoeuvre burns fuel and spoils a season of crops, and it shows the staff where its "
          "plans fail.",
          ('command', 'medal'), after_any=('belt_casemate_radar', 'belt_track_depots'),
          reward=(Flag('belt_tested'), XP('army', 20))),
))

WORKS = Branch('works', 'Garrison Town Workshops', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_count', 'Count the Garrison Workshops',
          "The garrison towns host three civilian works and two arms halls, built to repair, supply and feed the regiments. They "
          "employ most of the skilled hands inland and live almost entirely on army orders. Before any plan is drawn, clerks "
          "count machines, payrolls and contracts. The count annoys managers who prefer vague numbers, and it settles nothing yet.",
          ('industry', 'document'), reward=(Idea('workshop_ledger'), Event('workshop_floor'))),
    Focus('works_power', 'Power Lines to the Workshop District',
          "The garrison towns have long asked for a workshop district of their own, and some of its ground is already cleared. "
          "Finishing the substations and power lines lets a new civilian works open there. The money goes to contractors the "
          "diet does not entirely trust. The jobs go to towns that have waited a long time for something other than barracks.",
          ('industry', 'tools'), after=('works_count',), reward=(Build('industrial_complex', 1, 581),)),
    Focus('works_apprentices', 'Apprentice Benches in Every Hall',
          "Skilled fitters in the workshops are ageing, and their trade has always passed from hand to hand without schools or "
          "papers. A state apprenticeship puts trainee benches in every hall, pays a small wage and certifies the results. "
          "Output dips while masters teach instead of working. In time the halls will have enough trained hands to try new lines.",
          ('training', 'tools'), after=('works_count',), reward=(Idea('apprentices'),)),
    Focus('works_civil', 'Town Goods Instead of Track Links',
          "Converters among the managers and the diet would have the workshops make goods that families and farms buy: pumps, cable, tools, tinned food "
          "and bicycle frames, sold in the harbour towns and through the junction. Orders would come from many customers rather "
          "than one. Workers would need retraining, the regiments would lose some repair capacity, and the arms hall managers "
          "would fight it.",
          ('rebuild', 'industry'), after=('works_power',), cost=10, exclusive=('works_armour',),
          reward=(SwapIdea('workshop_ledger', 'civil_workshops'), Flag('model_civil'))),
    Focus('works_armour', 'Keep the Turret Shops Turning',
          "The arsenal camp says the workshops already do one thing well, which is keeping armoured vehicles running, and should "
          "sell that skill abroad. Foreign armies would send engines and running gear for overhaul at Serenavian rates. The halls "
          "keep their skills and the regiments keep their repairs. The state becomes a contractor to other armies, with all that "
          "implies.",
          ('tools', 'industry'), after=('works_power',), cost=10, exclusive=('works_civil',),
          reward=(SwapIdea('workshop_ledger', 'armour_arsenal'), Flag('model_armour'))),
    Focus('works_civil_hall', 'A New Hall for Household Goods',
          "The first converted orders sell well enough to justify a new hall. Built beside the junction so that goods load "
          "straight onto wagons, it makes stoves, pumps and wire for the harbour towns and beyond. The hall needs credit that "
          "the treasury must guarantee. Its opening is the first ceremony in the garrison towns without a military band.",
          ('rebuild', 'civil'), after=('works_civil',), reward=(Build('industrial_complex', 1, 581), Stability(0.01))),
    Focus('works_armour_hall', 'A Refit Hall for Foreign Armour',
          "Overhaul contracts from abroad outgrow the old arms halls, so the state builds a refit hall with heavy cranes, an "
          "engine test bed and a siding long enough for tank transporters. Foreign inspectors will walk its floors, and some "
          "buyers will be governments the diet would rather not name. The hall pays wages no civilian works can match.",
          ('industry', 'rail'), after=('works_armour',), reward=(Build('arms_factory', 1, 581),)),
    Focus('works_spares', 'A Common Pool of Spare Parts',
          "Each workshop has kept its own spares, hoarded against the next army order, so a missing bearing in one town can idle "
          "a line while three sit unused in the next. A common pool with one catalogue and one depot ends the hoarding. "
          "Managers lose a private cushion. The regiments and the halls gain a supply that answers within a day.",
          ('tools', 'document'), after=('works_apprentices',), reward=(Flag('spares_pool'), Research('industry', 0.5, 1))),
    Focus('works_export_house', 'An Export House at Serdonia',
          "Serenava trades under an export-led policy, yet its workshops have nobody abroad to sell for them. An export house "
          "at Serdonia, run jointly by the state and the workshop owners, takes samples to foreign fairs, handles letters of "
          "credit and quotes prices in foreign currency. It costs a year of salaries before the first contract arrives.",
          ('economy', 'diplomacy'), after_any=('works_civil_hall', 'works_armour_hall'), reward=(TimedIdea('export_house', 365),)),
))

GATE = Branch('gate', 'The Junction at the Gate', 1992, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('gate_tally', 'Tally the Junction Freight',
          "Serenava sits where the rail lines from Gatewood, Old Perbla, the Relentian towns of Driscol and Fraeport and the "
          "Osean frontier all meet, in the region the maps call the South Osean Gate. Nobody knows how much freight crosses it or "
          "what it pays. Clerks at every yard log each wagon for a month and add up the result.",
          ('rail', 'document'), reward=(Idea('freight_count'), Event('junction_freight'))),
    Focus('gate_mud_roads', 'Gravel for the Rainy Season',
          "Warm rains turn the plains roads to mud for months each year, and the villages beside the rail lines are cut off "
          "whenever the trains are full. Gravelled roads from the junction to the forest districts let trucks move in every "
          "season. The work is unglamorous and expensive, and it is the first thing most rural voters will notice.",
          ('tools', 'civil'), after=('gate_tally',), reward=(Build('infrastructure', 1, 581),)),
    Focus('gate_karnaca_sidings', 'New Sidings at the Karnaca Yards',
          "Karnaca's yards serve the naval berths, the line toward Driscol and Fraeport and the inland junction, and they jam "
          "whenever two of those trains arrive at once. New sidings and a second loading road let freight wait without blocking "
          "the main line. The harbour gains land it badly needs for warehouses, and the rail crews gain a few hours of sleep.",
          ('rail', 'navy'), after=('gate_tally',), reward=(Build('infrastructure', 1, 581), Stability(0.01))),
    Focus('gate_open', 'An Open Tariff at the Frontier',
          "One answer makes the junction the cheapest and quickest way through the region: a single published transit tariff, "
          "customs clearance on the moving train and no searches without cause. Traffic and fees would rise together. The "
          "commandants warn that an open gate on the Osean frontier is also open to smugglers and to anyone who wants to watch.",
          ('gate', 'economy'), after=('gate_tally',), cost=10, exclusive=('gate_guarded',),
          reward=(SwapIdea('freight_count', 'open_gate'),)),
    Focus('gate_guarded', 'Inspection Sheds at Every Crossing',
          "The other answer treats every wagon that crosses the frontier as a security question: inspection sheds at the "
          "crossings, sealed wagons and customs officers trained by the army. Shippers would pay in time rather than fees, and "
          "some traffic would go around Serenava altogether. What remained would be traffic the state knows about, cargo by cargo.",
          ('gate', 'security'), after=('gate_tally',), cost=10, exclusive=('gate_open',),
          reward=(SwapIdea('freight_count', 'guarded_gate'),)),
    Focus('gate_bonded_wagons', 'Bonded Wagons Through Serenava',
          "Now that the neighbours accept a common customs seal, bonded wagons can cross Serenava from one frontier to another "
          "without being opened, provided their seals arrive intact. Inspectors check paperwork instead of cargo and the trains "
          "barely stop. Transit revenue rises quickly. So does the temptation for any official to overlook a broken seal.",
          ('rail', 'economy'), after=('gate_open',), requires=(HasFlag('seal_accord'),), reward=(Idea('bonded_wagons'),)),
    Focus('gate_customs_brigades', 'Customs Brigades on the Plains',
          "Inspection sheds need staff who can search a wagon properly and chase a smuggler across open fields. Customs brigades "
          "recruited from former soldiers, with trucks, dogs and radios, patrol the plains between the crossings. They cost more "
          "than clerks and behave less politely. Smuggling falls sharply, and the brigades become the face of the state there.",
          ('security', 'gate'), after=('gate_guarded',), reward=(Idea('customs_brigade'),)),
    Focus('gate_junction_board', 'One Board for Four Lines',
          "The rail lines that meet in Serenava were run by separate offices that rarely spoke to each other. A junction board "
          "with one timetable, one dispatch room and one budget takes them all over. Railway managers lose their small kingdoms. "
          "The trains run closer to time, and the state finally knows what each line costs and what it earns.",
          ('rail', 'command'), after_any=('gate_mud_roads', 'gate_karnaca_sidings'), reward=(Idea('junction_board'),)),
))

HARBOURS = Branch('harb', 'Serdonia and Karnaca', 1993, 'FOCUS_FILTER_NAVY_XP', (
    Focus('harb_compare', 'Serdonia and Karnaca Open Their Books',
          "Serenava's coast has two harbours that have never cooperated. Serdonia is the larger town, with the busier market and "
          "older quays; Karnaca has the deeper naval berths and the rail line toward Driscol and Fraeport. Bringing their "
          "accounts to one table shows how much both lose by competing for the same small trade. Neither harbour master enjoys it.",
          ('navy', 'document'), reward=(Idea('twin_harbours'), Event('two_harbours'))),
    Focus('harb_fishing', 'Cooperatives for the Fishing Fleets',
          "The fishing boats of both harbours sell to a handful of dealers who set the price every morning. State credit for "
          "fishing cooperatives, with their own ice plants, auction halls and diesel stores, lets crews sell together. Dealers "
          "lose their grip and complain to every deputy they know. The fleets gain steadier incomes and a reason to modernise.",
          ('fishing', 'economy'), after=('harb_compare',), reward=(Idea('fishing_cooperatives'),)),
    Focus('harb_slipway', 'A Repair Slipway at Karnaca',
          "Karnaca has naval berths but nowhere to haul out a hull, so every serious repair goes abroad, and the money with it. "
          "A slipway with a winch house, workshops and a small crane lets the harbour repair patrol craft, trawlers and coasters "
          "at home. It needs shipwrights the town does not yet have; the inland workshops will supply the first of them.",
          ('navy', 'tools'), after=('harb_compare',), reward=(Build('dockyard', 1, 581), XP('navy', 5))),
    Focus('harb_one_board', 'A Single Board for Both Harbours',
          "One plan joins Serdonia and Karnaca under a single harbour board with common dues, one investment budget and one set "
          "of pilots. Ships would choose the berth that suits them and pay the same either way. Each town fears it will be the "
          "one that loses traffic. The board would finally let Serenava plan its coast as a whole.",
          ('navy', 'command'), after=('harb_fishing',), exclusive=('harb_rival_dues',), reward=(Idea('harbour_board'),)),
    Focus('harb_rival_dues', 'Let the Harbours Compete on Dues',
          "The rival plan lets each harbour set its own dues and keep its own revenue, competing openly for every fishing boat "
          "and coaster. Competition would push fees down and service up. It would also duplicate investment, start a price war "
          "between neighbouring towns and leave the state with two half-built harbours instead of one finished coast.",
          ('navy', 'scales'), after=('harb_fishing',), exclusive=('harb_one_board',), reward=(Idea('rival_dues'),)),
    Focus('harb_patrol', 'A Patrol Flotilla at Karnaca',
          "With a slipway to keep them running, Karnaca can base a small flotilla of patrol craft to watch the fishing grounds, "
          "escort the coasters and support the shore casemates. The boats are modest, and their crews come from the marines and "
          "the fishing fleets. The flotilla is far too small to fight a navy, and large enough to make the coast a Serenavian one.",
          ('navy', 'security'), after=('harb_slipway',), reward=(SwapIdea('twin_harbours', 'harbour_patrol'),)),
    Focus('harb_coast_radar', 'A Radar Mast Above Serdonia',
          "Serdonia's approaches have no radar of their own, and ships are tracked by binoculars and radio calls. A radar mast on "
          "the hill behind the town sweeps the approaches, the fishing grounds and the beaches near the shore casemates. "
          "Residents who preferred the view object. The coast gains a picture of every ship that comes near.",
          ('radar', 'navy'), after=('harb_compare',), reward=(Build('radar_station', 1, 581), XP('navy', 10))),
    Focus('harb_sweepers', 'Sweepers for the Coastal Approaches',
          "Any war in the region could leave mines in the coastal lanes, and Serenava has no means of clearing them. Two of the "
          "patrol craft are fitted with sweeping gear and their crews trained to use it, with regular practice off both "
          "harbours. It is dull, dangerous work. It means the harbours can reopen quickly after a crisis without waiting for "
          "foreign help.",
          ('navy', 'tools'), after=('harb_patrol',), reward=(Idea('minesweepers'), XP('navy', 10))),
))

NEIGHBOURS = Branch('nb', 'Neighbours Down Every Line', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('nb_envoys', 'Envoys on the Morning Trains',
          "Serenava's first envoys travel by rail, because the rail links the state to every neighbour. In a single week they "
          "call at Gatewood, at the offices that run the Relentian ports and the Terentio towns, and at the Osean frontier "
          "administration. They carry practical questions rather than grand proposals. The trip costs little, and what they hear "
          "will shape the whole foreign policy.",
          ('diplomacy', 'rail'), reward=(Event('envoy_rounds'), PP(10))),
    Focus('nb_through_seals', 'One Customs Seal for Through-Trains',
          "Through-trains are stopped and searched at every frontier along the junction lines, sometimes three times in one "
          "journey. Serenava proposes a common customs seal that every neighbour would honour, with joint inspection of any "
          "wagon whose seal is broken. Negotiating it takes months of patient meetings. Once signed, it makes Serenava the "
          "easiest crossing in the region for honest freight.",
          ('document', 'gate'), after=('nb_envoys',),
          reward=(Flag('seal_accord'), Tooltip('No claim, core or border changes; the seal covers customs procedure only.'))),
    Focus('nb_karnaca_line', 'Keep the Karnaca Line Running',
          "The rail line from Karnaca toward Driscol and Fraeport carries fish, workshop goods and commuters every day. Serenava "
          "offers to share the cost of its track, signals and crossing staff with whichever government holds the far end. The "
          "agreement changes no frontier and claims nothing. It keeps two stretches of the same coast in daily touch.",
          ('rail', 'navy'), after=('nb_envoys',),
          reward=(Stability(0.02), Tooltip('No claim, core or border changes; the agreement covers track, signals and staff only.'))),
    Focus('nb_gatewood', 'Gauge and Standards with Gatewood',
          "One camp wants Serenava to keep the closest possible ties with Perbla: shared rail gauge, shared technical standards, "
          "matching customs rates and ministers who meet their Perblan counterparts every quarter in Gatewood. Old supply chains keep working and spare parts keep "
          "fitting. Critics in the harbour wards answer that a state which copies every Perblan rule has only changed the name "
          "on its stamps.",
          ('rail', 'diplomacy'), after_any=('nb_through_seals', 'nb_karnaca_line'), cost=10,
          exclusive=('nb_osea', 'nb_even'), reward=(Idea('gatewood_standards'),)),
    Focus('nb_osea', 'Osean Buyers Welcome',
          "Another camp looks across the plains. Osea is the largest market within reach, and its buyers already ask for "
          "Serenavian timber, fish and overhaul work. Opening the frontier offices to Osean trade missions and accepting Osean "
          "technical standards would bring orders quickly. In the garrison towns, many will ask why the casemates still face "
          "the customers.",
          ('diplomacy', 'economy'), after_any=('nb_through_seals', 'nb_karnaca_line'), cost=10,
          exclusive=('nb_gatewood', 'nb_even'), reward=(Idea('osean_traders'),)),
    Focus('nb_even', 'Equal Distance from Every Capital',
          "The third camp wants Serenava to belong to nobody: one tariff for all, no preferred standards and envoys of equal "
          "rank in every neighbouring capital. It makes the state predictable and hard to pressure. It also wins no special "
          "friend, and every neighbour will suspect that the others are quietly getting a better deal.",
          ('peace', 'scales'), after_any=('nb_through_seals', 'nb_karnaca_line'), cost=10,
          exclusive=('nb_gatewood', 'nb_osea'), reward=(Idea('even_frontier'),)),
    Focus('nb_consulates', 'Consulates in Serdonia',
          "Whichever course the government chose, neighbours need somewhere in Serenava to issue visas, register freight agents "
          "and help their citizens in trouble. The state offers buildings in Serdonia to any neighbour willing to open a "
          "consulate, on equal terms. The consulates bring visitors, rents and a steady flow of information in both "
          "directions, some of it unwelcome.",
          ('diplomacy', 'document'), after_any=('nb_gatewood', 'nb_osea', 'nb_even'),
          reward=(PP(20), Tooltip('Consulates register visitors and freight agents; no treaty, faction or border change.'))),
    Focus('nb_terentio_freight', 'Freight Rates with Terentio',
          "Terentio's towns buy timber and workshop goods from Serenava and send little back, so wagons return empty over a long "
          "route. A standing rate agreement fills the return wagons with whatever Terentio can send, at a discount the railway "
          "absorbs. The junction clerks grumble about the loss. The trade, small as it is, keeps a distant neighbour friendly.",
          ('rail', 'economy'), after=('nb_envoys',), reward=(Research('train_tech', 0.5, 1), PP(15))),
))

WARYEARS = Branch('war', 'The Belkan War Across the Plains', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_news', 'News Reaches the Inland Crossing',
          "The Belkan War that breaks out in March 1995 does not involve Serenava, but Osea, directly across the plains, is "
          "fighting it. Frontier posts report military convoys beyond the barrier, and the garrison towns hear the "
          "news before Serdonia does. The government puts the frontier on alert, which costs fuel, overtime and a great deal "
          "of nervous energy.",
          ('communications', 'security'), requires=(After('1995.3.25'),),
          reward=(Idea('frontier_alert'), Event('war_beyond_line'))),
    Focus('war_transit_closed', 'No Belligerent Trains Through the Gate',
          "The strict reading of neutrality closes the junction to every train carrying soldiers, weapons or military stores "
          "for any party to the war, inspected at the crossings and turned back if in doubt. No side can accuse Serenava of "
          "helping its enemy. Freight income falls, neighbours protest, and the customs posts become the busiest offices in "
          "the state.",
          ('gate', 'peace'), after=('war_news',), cost=10, exclusive=('war_relief_trains',),
          reward=(SwapIdea('frontier_alert', 'transit_closed'),)),
    Focus('war_relief_trains', 'Relief Trains Only, Marked and Searched',
          "The looser reading keeps the junction open to trains carrying food, medicine and civilian goods for anyone, clearly "
          "marked and searched at the crossing, while still refusing military cargo. Trade survives and the junction keeps its "
          "name for reliability. Every belligerent will suspect the searches are lax for its enemies, and every mistake will "
          "be reported abroad.",
          ('rail', 'medical'), after=('war_news',), cost=10, exclusive=('war_transit_closed',),
          reward=(SwapIdea('frontier_alert', 'relief_trains'),)),
    Focus('war_stand_to', 'The Regiments Stand To',
          "Having tested its plans on the plains, the army now puts them into force: crews in the casemates or tanks in their "
          "hides, reserves called for a short spell and patrols along every kilometre of the frontier. Standing to costs wages "
          "and harvests. It also tells every commander across the line that Serenava has a plan and the means to carry it out.",
          ('security', 'training'), after=('war_news',), requires=(HasFlag('belt_tested'),),
          reward=(TimedIdea('stand_to', 180), XP('army', 10))),
    Focus('war_fuel_ration', 'Draw on the Banked Fuel',
          "War abroad drives up fuel prices at home, and shippers begin to hoard. The earth-banked farms beside the forest field "
          "hold enough to steady the market for months. Releasing fuel under ration cards keeps trucks, tractors and fishing "
          "boats moving at a fair price. Every litre sold now is a litre the air staff will not have later.",
          ('economy', 'logistics'), after=('war_news',), requires=(HasFlag('fuel_banked'),),
          reward=(TimedIdea('fuel_ration', 365),)),
    Focus('war_air_patrols', 'Patrols Along the Frontier Sky',
          "With fighting so close, the air guard flies standing patrols along the frontier, keeping well inside Serenavian "
          "airspace and reporting every foreign aircraft that comes near. Pilots gain more real flying in a month than in a year "
          "of training. Each sortie eats fuel and engine life, and one navigation error could turn careful neutrality into "
          "an incident.",
          ('air', 'communications'), after=('war_news',), requires=(HasFlag('air_guard_raised'),),
          reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
    Focus('war_neutral_freight', 'Freight Flights Under Neutral Colours',
          "Freight operators at the forest field find wartime demand for civilian air cargo, and the state allows it under strict "
          "rules: large neutral markings, filed routes that avoid every war zone and inspection of every load. Revenue rises "
          "sharply. A single aircraft caught with military cargo would cost the field its licence and the state its credibility.",
          ('runway', 'peace'), after=('war_news',), requires=(HasFlag('fields_freight'),),
          reward=(TimedIdea('neutral_freight', 365),)),
    Focus('war_hangar_reception', 'Reception Halls in the Hangars',
          "People fleeing the war may reach Serenava by road, rail or sea, and the state has no reception centres. Empty hangars "
          "among the outer shelters are cleaned, heated and fitted with beds, kitchens and clinics. They are far from "
          "comfortable, but they are dry and secure. Their cost, and their guests, become a fierce subject in the diet.",
          ('refugees', 'runway'), after=('war_news',), reward=(Flag('hangar_reception'), Stability(-0.02))),
    Focus('war_osean_drawdown', 'Osean Columns Go Home',
          "With Belka defeated, the military traffic on the Osean side of the frontier thins and the reservists across the "
          "plains go home. Serenava can relax its alert and return the crossings to their normal routines. Trade with Osea "
          "resumes on better terms than before. The commandants warn that a victorious Osea will feel less need to court small "
          "neighbours.",
          ('peace', 'gate'), after_any=('war_transit_closed', 'war_relief_trains'), exclusive=('war_osean_buildup',),
          requires=(HasGlobal('belka_lost_belkan_war'),), reward=(Idea('osean_drawdown'),)),
    Focus('war_osean_buildup', 'Osea Digs In Across the Plains',
          "With Belka victorious, Osea does not stand down. Fresh fortifications appear across the plains, Osean reconnaissance "
          "flights skirt the frontier and the frontier offices turn cold and formal. Serenava must keep its own alert in force "
          "for years, with all the cost that entails. The garrison towns gain work and the harbour wards lose good customers.",
          ('security', 'gate'), after_any=('war_transit_closed', 'war_relief_trains'), exclusive=('war_osean_drawdown',),
          requires=(HasGlobal('belka_won_belkan_war'),), reward=(Idea('osean_buildup'),)),
))

SKY = Branch('sky', 'Ulysses and the Concrete', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_announcement', 'The Impact Warning Reaches Serdonia',
          "In April 1996 the world learns that Ulysses will hit, and the news reaches Serenava like everywhere else, with no hint "
          "of which regions the fragments will strike. A small state has no means of its own to watch the sky. It does "
          "have a casemate belt and hardened hangars, and frightened families are already asking who will be let inside.",
          ('meteor', 'shelter'), requires=(After('1996.4.20'),), reward=(Idea('sky_dread'), Event('asteroid_casemates'))),
    Focus('sky_public_casemates', 'Open the Casemates to Families',
          "The civil answer opens the casemates to the public: every family in the harbour towns and on the plains is assigned a "
          "gallery, a shelter warden and a route to reach it. The regiments lose their fighting positions for as long as the "
          "danger lasts. The public gains the strongest shelter in the region, and the army gains unwanted housekeeping.",
          ('shelter', 'civil'), after=('sky_announcement',), exclusive=('sky_forest_trenches',),
          reward=(Idea('public_casemates'), Flag('casemates_public'))),
    Focus('sky_forest_trenches', 'Shelter Trenches in the Forests',
          "The military answer keeps the casemates for the regiments and digs covered shelter trenches in the forests near every "
          "town, roofed with timber and earth. They are cheaper, closer to home and far weaker than concrete. Families complain "
          "that the soldiers have kept the safe places for themselves, while the army keeps its defences ready for what follows.",
          ('shelter', 'tools'), after=('sky_announcement',), exclusive=('sky_public_casemates',),
          reward=(Idea('forest_shelters'), Flag('casemates_military'))),
    Focus('sky_hangar_stores', 'Stock the Empty Hangars',
          "The hangars already fitted to receive war refugees become relief stores for the impact: grain, tinned food, blankets, "
          "generators and medicine for weeks, kept dry under the concrete and close to the rail spur. Stocking them ties up "
          "money and invites theft. When the roads close, Serenava will have supplies in the one place built to survive attack.",
          ('logistics', 'shelter'), after=('sky_announcement',), requires=(HasFlag('hangar_reception'),),
          reward=(Idea('hangar_depots'),)),
    Focus('sky_radars_up', 'Turn the Field Radars Skyward',
          "The radar sets on the airfields were built to find aircraft, not falling rock, but engineers can tilt and retune a few "
          "of them to watch the upper sky. The results are crude and full of false returns. They are also Serenava's own, and "
          "they give the warning network a few minutes of notice that no foreign bulletin could provide.",
          ('radar', 'meteor'), after=('sky_announcement',), reward=(Idea('skyward_radar'),)),
    Focus('sky_evac_trains', 'Timetables for a Night of Departures',
          "If a fragment threatens the harbour towns, people must leave quickly, and the junction is the fastest way out. The "
          "railway clerks write evacuation timetables for every station, keep empty trains parked on sidings overnight and "
          "rehearse the routes with volunteers. Freight suffers during rehearsals. The timetables mean a crowd can become a "
          "column in hours.",
          ('rail', 'refugees'), after=('sky_announcement',), reward=(Flag('evac_timetable'), Research('train_tech', 0.5, 1))),
    Focus('sky_warden_rota', 'A Warden for Every Gallery',
          "Shared casemates need rules: who sleeps where, how water is rationed, who settles quarrels and who checks the air "
          "filters. A warden is appointed for every gallery, trained by the army and paid by the township. Wardens become small "
          "authorities with lists and keys. When the night comes, the galleries will be crowded but not lawless.",
          ('shelter', 'document'), after=('sky_public_casemates',), requires=(HasFlag('casemates_public'),),
          reward=(TimedIdea('warden_rota', 730),)),
    Focus('sky_trench_drills', 'Drills in the Forest Trenches',
          "Shelter trenches only work if families know where theirs is and can reach it in the dark. Army engineers run night "
          "drills in every forest district, timing each street and fixing the worst routes. Farmers lose sleep and tempers. The "
          "drills also teach the engineers lessons about earthworks that the regiments will use long after the asteroid passes.",
          ('tools', 'training'), after=('sky_forest_trenches',), requires=(HasFlag('casemates_military'),),
          reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('sky_roche_night', 'Watch Night over the Forest Field',
          "In July 1999 the asteroid passes Earth's Roche limit, and every plan Serenava has made is tested at once. Wardens open "
          "the shelters, trains wait on the sidings and the field radars sweep the sky all night. Nobody knows what the next "
          "hours will bring, and the government must keep a frightened state calm until dawn.",
          ('meteor', 'radar'), after_any=('sky_hangar_stores', 'sky_radars_up'),
          requires=(After('1999.7.8'), HasFlag('evac_timetable')), reward=(Event('roche_watch'),)),
    Focus('sky_lessons', 'What the Long Watch Taught',
          "Once the worst nights have passed, a committee of wardens, rail crews and radar operators writes down what worked and "
          "what did not: which shelters leaked, which trains ran late and which rumours did the most harm. The report is "
          "unflattering, and acting on it costs another season of repairs. Serenava ends the decade knowing how its people behave "
          "under threat.",
          ('document', 'civil'), after=('sky_roche_night',), reward=(RemoveIdea('sky_dread'), Stability(0.03))),
))

CENTURY = Branch('cent', 'Serenava at the Century', 2001, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_stock', 'Serenava Takes Its Own Measure',
          "At the turn of the century a mixed panel of deputies, commandants, harbour masters and railway clerks is asked to "
          "measure what Serenava has built since it began governing itself, and what it has left undone. The report will set "
          "the agenda for the next decade, so every faction lobbies the panel. Commissioning it costs little except nerves.",
          ('document', 'assembly'), reward=(Event('frontier_stock'), Stability(0.01))),
    Focus('cent_princely_statute', 'Write the Princely Statute',
          "Years of princely cabinets have produced a pile of conventions, precedents and letters but no single text. The cabinet "
          "and the diet now write a statute setting out what the Office of the Crown may sign alone, what needs the cabinet and "
          "what needs the deputies. Drafting it reopens old fights. Once printed, it settles them for a generation.",
          ('scales', 'command'), after=('cent_stock',), requires=(HasFlag('path_princely'),),
          exclusive=('cent_garrison_ordinance', 'cent_township_charter'),
          reward=(SwapIdea('princely_course', 'princely_constitution'),)),
    Focus('cent_garrison_ordinance', 'Publish the Garrison Ordinance',
          "The council of commandants has governed by single orders, each issued as a problem arose. Its staff now gathers them "
          "into one published ordinance that every district can read: what the council decides, what the prefects decide and "
          "how a citizen may appeal. Publishing it limits the council's freedom and makes its rule predictable, which most "
          "citizens prefer.",
          ('security', 'document'), after=('cent_stock',), requires=(HasFlag('path_garrison'),),
          exclusive=('cent_princely_statute', 'cent_township_charter'),
          reward=(SwapIdea('garrison_course', 'garrison_code'),)),
    Focus('cent_township_charter', 'Ratify the Township Charter',
          "The Republic's founding charter was written in a hurry and amended by the executive whenever it proved inconvenient. "
          "A convention of every township rewrites it with a court to interpret it, a fixed share of revenue for each township "
          "and strict rules for amendment. The convention takes a year and embarrasses several ministers. The result is short "
          "enough to teach in schools.",
          ('assembly', 'scales'), after=('cent_stock',), requires=(HasFlag('path_township'),),
          exclusive=('cent_princely_statute', 'cent_garrison_ordinance'),
          reward=(SwapIdea('township_course', 'republic_charter'),)),
    Focus('cent_clerk_posts', 'Examined Clerks Take Senior Posts',
          "The first clerks recruited by open examination have now served long enough for senior posts. Promoting them by merit "
          "rather than patronage reshapes every ministry. Older officials who rose by favour resent the change, and a few resign "
          "loudly. The service that emerges is younger, more competent and much harder for any faction to capture.",
          ('training', 'document'), after=('cent_stock',), requires=(HasFlag('state_clerks'),),
          reward=(Idea('examined_service'),)),
    Focus('cent_town_goods', 'Town Goods Find Foreign Buyers',
          "Years of converted production have given the garrison-town workshops a range of tools, pumps and household goods that "
          "sell beyond Serenava. The state now backs them with export credit and stands at foreign fairs. Competition from "
          "larger countries is fierce and margins are thin. Success would free the workshops from the army for the first time.",
          ('economy', 'industry'), after=('cent_stock',), requires=(HasFlag('model_civil'),), exclusive=('cent_refit_abroad',),
          reward=(SwapIdea('civil_workshops', 'civil_upgrade'),)),
    Focus('cent_refit_abroad', 'Long Refit Contracts Abroad',
          "The refit trade has made Serenava a known name among armies that run older armour and cannot afford new vehicles. The "
          "state now signs long overhaul contracts with several of them, guaranteeing work for years. Some contracts are with "
          "governments the diet prefers not to discuss in public. The halls are full, and the garrison towns grow rich on other "
          "people's wars.",
          ('tools', 'diplomacy'), after=('cent_stock',), requires=(HasFlag('model_armour'),), exclusive=('cent_town_goods',),
          reward=(SwapIdea('armour_arsenal', 'arsenal_upgrade'),)),
    Focus('cent_usean_fuel', 'Fuel Prices and the Usean War',
          "War breaks out on the continent of Usea in the summer of 2003, far from Serenava, but fuel and freight markets feel it "
          "at once. The forest field, the fishing fleets and the junction all depend on imported fuel. The government studies how "
          "far prices may climb and what the stored reserves can do. Serenava has no part in the war, and wants none.",
          ('economy', 'logistics'), after=('cent_stock',), requires=(After('2003.8.22'),),
          reward=(Idea('wartime_fuel'), Event('usean_fuel'))),
    Focus('cent_rates_ease', 'Prices Ease After Farbanti',
          "With Farbanti fallen, Erusea's surrender accepted and the war in Usea over, fuel markets calm and shipping settles. Serenava "
          "lifts its emergency fuel measures and lets prices find their level. Workshops and freight operators recover their "
          "margins. Officials who wanted the reserves released early claim vindication; those who held them note that the next "
          "war may last longer.",
          ('peace', 'economy'), after=('cent_usean_fuel',), exclusive=('cent_rates_stay',),
          requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),), reward=(RemoveIdea('wartime_fuel'), Stability(0.03))),
    Focus('cent_rates_stay', 'Prices Stay High Without a Peace',
          "With Erusea victorious in Usea, the markets do not calm. Shipping lanes stay uncertain, fuel stays dear and some "
          "suppliers never return. Serenava turns its emergency measures into a standing fuel reserve policy, buying when prices "
          "dip and selling when they spike. The policy costs storage and capital, and it shields the state from the next shock.",
          ('scales', 'logistics'), after=('cent_usean_fuel',), exclusive=('cent_rates_ease',),
          requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),), reward=(SwapIdea('wartime_fuel', 'fuel_hedge'),)),
))

BRANCHES = (GOVERN, FIELDS, BELT, WORKS, GATE, HARBOURS, NEIGHBOURS, WARYEARS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('hangar_rent', 'Rent Out a Row of Hangars',
                'Lease a row of outer hangars to private operators for half a year, trading readiness for rent.',
                cost=40, effects=(TimedIdea('hangar_rent', 180),), requires=(Completed('fields_count'),), cooldown=365),
    DecisionDef('casemate_drill', 'A Night Drill in the Casemates',
                'Call the casemate crews out for a night of alarms, gun drills and gas-door checks along the whole belt.',
                cost=30, effects=(XP('army', 15), WarSupport(0.01)), requires=(Completed('belt_walk'),), cooldown=365),
    DecisionDef('gravel_gangs', 'Send Gravel Gangs Before the Rains',
                'Pay village gangs to regravel the plains roads for four months before the wet season closes them.',
                cost=45, effects=(TimedIdea('gravel_gangs', 120),), requires=(Completed('gate_tally'),), cooldown=365),
    DecisionDef('crossing_market', 'A Market Day at the Inland Crossing',
                'Close the inland crossing to freight for a day and open it to traders from both sides of the frontier.',
                cost=25, effects=(Event('border_market'),), requires=(Completed('nb_envoys'),), cooldown=730),
    DecisionDef('shore_radar', 'A Radar Set for the Shore Casemates',
                'Buy one radar set for the shore casemates, once, and wire it to the Serdonia mast.',
                cost=75, effects=(Build('radar_station', 1, 581),), requires=(Completed('harb_coast_radar'),)),
    DecisionDef('landing_drill', 'Landing Drills off Karnaca',
                'Put the patrol flotilla and the casemate marines through a week of landings and counter-landings.',
                cost=35, effects=(XP('navy', 15), XP('army', 5)), requires=(Completed('harb_patrol'),), cooldown=365),
)
