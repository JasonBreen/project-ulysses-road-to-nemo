"""Romny (RMN): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party at 1
percent popularity, with fascism at 50 and neutrality at 48, governing through an unnamed
National Administration with elections suspended), the six 1991 states with their buildings,
resources and neutral captions, the map facts read from map/definition.csv, map/provinces.bmp
and map/railways.txt, and the global flags other mod scripts already set. Official: ACES
Chronicle rows used only as date anchors for distant pressures, each cited by its exact key.
Everything else, including every choice, office, idea, building, decision and event in Romny,
is provisional gameplay built on the world-start role of limited air and territorial guard.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='RMN', name='Romny', root='world', package='rmn',
                  themes=('ballot', 'logistics', 'security'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities fascism 50, neutrality 48, democratic 1, communism 1; stability and war support 0.5; three research '
           'slots; technology including tech_mountaineers, tech_engineers, early_fighter and basic_train; grand doctrines '
           'superior_firepower, new_fleet_in_being and new_operational_integrity. The starting leader is the unnamed National '
           'Administration office (RMN_ac_government_office, centrism), whose description says its 1991 holder has not been '
           'established. Country name Romny. The tree never names a holder and reads the party figures as context, not as '
           'proof of constitutional form.',
           'mod/2985041246/history/countries/RMN - Romny.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; tools/world_foundation/country_registry.json '
           '(RMN row: civil_administration, capacity 40)'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role limited air and territorial guard; 5 civilian, 5 military and no '
           'naval factories; 4 infantry formations of six battalions, each with an engineer company, two at the capital centre '
           '(9428) and two at the logistics centre (3787); 12 fighters on the capital air base with 4 in reserve; no combat '
           'navy by design; 60 convoys; stocks of 960 infantry, 720 motorized, 24 train and 192 support equipment; research '
           'priority Physical Sustainment (transport, equipment replacement, affordable service). Fiscal profile GDP 120, debt '
           'ratio 0.3, collection 0.85, growth 3, inflation 2 is fictional gameplay calibration, not national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'mod/2985041246/history/units/RMN_ws_land.txt; mod/2985041246/history/units/RMN_ws_air.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 85 (capital, large town, captioned Romny Capital District; victory point Romny Capital '
           'Centre 9428 with naval base 1; 2 civilian, 2 military, fuel silo 1, air base 1, infrastructure 2; steel 4, aluminium '
           '4, oil 2, rubber 2; plains, coastal; every shared slot in use), 536 (Romny District B; Romny Logistics Centre 3787; '
           '2 civilian, 1 military, infrastructure 2; steel 4, aluminium 3, rubber 2, oil 1; plains, coastal), 541 (marsh, '
           'inland; 1 civilian, 2 military, infrastructure 2; steel 4, aluminium 3, rubber 1, oil 1), 549 (plains, coastal; no '
           'buildings, infrastructure or resources), 561 (Romny District E; plains, coastal; empty) and 573 (Romny District F; '
           'plains, coastal; empty). States 541 and 549 keep inherited Earth-template names, which this tree does not use; they '
           'are called the marsh district and the rail-corner district by function. Railways (map/railways.txt): level-2 lines '
           '9428 to 3787 through province 1143 of state 549, and 9428 to 9236 in state 541; no line crosses a frontier. Land '
           'neighbours from map/provinces.bmp: Yuktobania (536, 541, 561) and Kaluga (561). The capital district borders all '
           'five other districts. No other place is named.',
           'mod/2985041246/history/states/85-State_85.txt and the five other RMN state files; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt'),
    Source('Mod provenance',
           'Neighbour consistency: Kaluga (tools/world_depth/klg/content.py) describes Romny and Yuktobania meeting its junction '
           'district. This tree acts only on the Romny side of that corner (District E) and claims no action, consent or '
           'outcome for Kaluga or Yuktobania.',
           'tools/world_depth/klg/content.py'),
    Source('Official',
           'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, Yuktobania. Gate of the '
           'coast-watch focus; no Romny role is claimed and no person is named.', '1991 / 09.02'),
    Source('Official',
           'Date anchor: the International Astronomical Union announces that Ulysses will pass close to Earth with a chance of '
           'impact. Opens the asteroid branch; no Romny role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Gate of the wartime commodity price focus; Romny takes no part.',
           '1995 / 03.25'),
    Source('Official',
           'Date anchor: the President of the FCU announces that Ulysses will impact the Earth. Gate of the impact focus and '
           'its event; where fragments fall is never stated for Romny.', '1996 / 04.20'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit. Gate of the Roche-limit focus; no impact in Romny is claimed.',
           '1999 / 07.08'),
    Source('Official',
           'Date anchor: Osea and Yuktobania cooperate to convert the Arkbird into a debris-clearing platform. Gate of the '
           'credit focus, read only as a change in lending mood; Romny has no part in the project.', '1999 / 10.08'),
    Source('Official',
           'Date anchor: the FCU demands that Erusea withdraw from San Salvacion and establishes the ISAF. The freight focus '
           'waits for the mod flag ac_ucw_isaf_formed and claims no Romny part in the war.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices are '
           'collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the three camps
    IdeaDef('borrowed_colours', 'Colours Without a Following',
            'The Administration governs under democratic colours that one citizen in a hundred supports.',
            {'political_power_gain': 0.05, 'stability_factor': -0.04}, ('ballot', 'document')),
    IdeaDef('rights_charter', 'The Entrenched Draft', 'A charter of rights and courts written before any ballot is opened.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('scales', 'document')),
    IdeaDef('notables_bench', 'The Notables Agreement', 'District notables, managers and co-operative boards share the seals.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05}, ('assembly', 'document')),
    IdeaDef('movement_pledge', 'The Movement Pledge', 'Half the country is promised a government that matches its numbers.',
            {'war_support_factor': 0.06, 'political_power_gain': 0.10, 'stability_factor': -0.02}, ('security', 'ballot')),
    IdeaDef('charter_court', 'Judges of the Charter', 'A court with fixed terms may strike down any law that breaches the charter.',
            {'stability_factor': 0.08, 'political_power_factor': 0.06}, ('scales', 'assembly')),
    IdeaDef('rotating_bench', 'A Bench That Rotates', 'One seat in three on the bench is refilled from fresh district lists each spring.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05, 'production_speed_infrastructure_factor': 0.05},
            ('assembly', 'civil')),
    IdeaDef('labour_columns', 'Movement Road Columns', 'Drill clubs turned into labour columns that cut roads across the plains.',
            {'production_speed_infrastructure_factor': 0.15, 'war_support_factor': 0.05, 'stability_factor': -0.02},
            ('tools', 'security')),
    IdeaDef('works_councils', 'Shop Floor Councils', 'Elected councils in every works with a say over shifts, safety and canteens.',
            {'stability_factor': 0.03, 'production_factory_efficiency_gain_factor': 0.02}, ('assembly', 'industry')),
    # the empty districts
    IdeaDef('district_survey', 'Stakes on Empty Ground', 'Survey pegs and chains across the three empty districts.',
            {'production_speed_infrastructure_factor': 0.08}, ('tools', 'document')),
    IdeaDef('planned_towns', 'Ministry Town Plans', 'Towns built to one pattern where the survey finds water and soil.',
            {'production_speed_industrial_complex_factor': 0.10, 'production_speed_infrastructure_factor': 0.08,
             'political_power_gain': -0.05}, ('civil', 'document')),
    IdeaDef('homestead_grants', 'Homestead Titles', 'Title to any surveyed plot farmed for five years, with tools on credit.',
            {'production_speed_infrastructure_factor': 0.12, 'stability_factor': 0.03}, ('civil', 'economy')),
    IdeaDef('district_boards', 'Boards from the District Lists', 'Local boards decide where the next well, school and road spur goes.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.04}, ('assembly', 'civil')),
    # the works
    IdeaDef('works_inventory', 'Ten Works on One Sheet', 'Every factory, order and idle shift listed in one inventory.',
            {'production_factory_efficiency_gain_factor': 0.02}, ('industry', 'document')),
    IdeaDef('spares_first', 'The Replacement Doctrine', 'Arms works turned toward barrels, tyres, springs and radios on the shelf.',
            {'repair_speed_factor': 0.10, 'supply_consumption_factor': -0.04}, ('tools', 'logistics')),
    IdeaDef('motor_works', 'Motor Halls of the Plains', 'Truck assembly at the logistics centre for farms, towns and the guard.',
            {'production_speed_arms_factory_factor': 0.10, 'army_speed_factor': 0.03}, ('logistics', 'industry')),
    IdeaDef('civil_halls', 'Halls Turned Civil', 'Arms halls in the marsh district retooled for household goods.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': -0.03}, ('rebuild', 'industry')),
    IdeaDef('replacement_depots', 'One Catalogue of Parts', 'Parts depots on the railway, stocked from one agreed catalogue.',
            {'repair_speed_factor': 0.15, 'supply_consumption_factor': -0.06}, ('logistics', 'document')),
    IdeaDef('truck_and_tyre', 'Home Tyres on Home Trucks', 'Trucks from the logistics centre roll on home latex and home steel.',
            {'production_speed_arms_factory_factor': 0.15, 'army_speed_factor': 0.04}, ('logistics', 'economy')),
    IdeaDef('household_lines', 'Household Goods Lines', 'Stoves, pumps, bicycles and lamps sold from the converted halls.',
            {'production_speed_industrial_complex_factor': 0.15, 'consumer_goods_factor': -0.05}, ('economy', 'civil')),
    IdeaDef('apprentice_benches', 'The Three-Year Bench', 'Apprentices paid to learn on real orders beside a master.',
            {'training_time_factor': -0.05, 'production_factory_max_efficiency_factor': 0.03}, ('training', 'tools')),
    # what the ground gives
    IdeaDef('resource_ledger', 'The Ground Ledger', 'Every deposit and grove priced, district by district.',
            {'production_speed_buildings_factor': 0.03}, ('document', 'economy')),
    IdeaDef('raw_exports', 'Raw Cargo at the Quay', 'Ore, bauxite and latex sold raw to whoever pays most.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': 0.05}, ('economy', 'navy')),
    IdeaDef('home_stock', 'Home Works Buy First', 'Export quotas keep raw materials for the works at a fixed price.',
            {'industrial_capacity_factory': 0.04, 'production_factory_max_efficiency_factor': 0.02}, ('industry', 'scales')),
    IdeaDef('graded_cargo', 'Graded and Weighed', 'Public scales and published grades for every cargo at the capital quay.',
            {'consumer_goods_factor': -0.05, 'political_power_gain': 0.08}, ('scales', 'navy')),
    IdeaDef('war_premium', 'Wartime Latex Premium', 'Rubber and aluminium sell high while a distant war lasts.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': -0.01}, ('economy', 'diplomacy')),
    IdeaDef('auction_season', 'Auction Season at the Quay', 'The latex crop sold by open auction under the public scales.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('economy', 'scales')),
    # the guard
    IdeaDef('guard_garrisons', 'Two Garrisons Only', 'Four formations split between the capital centre and the logistics centre.',
            {'army_org_factor': 0.02, 'planning_speed': 0.05}, ('security', 'command')),
    IdeaDef('marsh_anchor', 'Anchored on the Marsh', 'Prepared positions in the one district the ground itself defends.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.04}, ('security', 'tools')),
    IdeaDef('motor_columns', 'A Guard on Wheels', 'Every formation carried by truck, with drivers trained and fuel allotted.',
            {'army_speed_factor': 0.06, 'army_attack_factor': 0.03}, ('logistics', 'security')),
    IdeaDef('district_rolls', 'District Reserve Rolls', 'Trained reservists in every district, rifles held at the district office.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.04}, ('document', 'security')),
    IdeaDef('registered_clubs', 'Clubs on the Guard Register', 'Movement drill clubs trained by guard instructors under guard rules.',
            {'training_time_army_factor': -0.08, 'war_support_factor': 0.03}, ('training', 'security')),
    IdeaDef('crossing_drill', 'Ditch and Stream Drill', 'Engineers trained with pontoons and ditching machines for flat wet ground.',
            {'attrition': -0.05, 'army_speed_factor': 0.03}, ('bridge', 'training')),
    # the air arm
    IdeaDef('one_field_wing', 'The Single Squadron', 'Twelve fighters and one runway beside the capital quay.',
            {'experience_gain_air_factor': 0.04}, ('air', 'runway')),
    IdeaDef('frontier_patrol', 'The Line Patrol', 'Fighters on regular patrol along the frontier with Yuktobania and Kaluga.',
            {'air_mission_efficiency': 0.06, 'air_detection': 0.08}, ('air', 'radar')),
    IdeaDef('capital_umbrella', 'Umbrella over the Quay', 'Fighters held at readiness over the capital, the quay and the fuel silo.',
            {'air_superiority_efficiency': 0.08, 'air_defence_factor': 0.05}, ('air', 'shelter')),
    IdeaDef('ground_crews', 'Mechanics Who Stay', 'Long contracts, housing and a pension for the field crews.',
            {'repair_speed_factor': 0.08, 'experience_gain_air_factor': 0.05}, ('tools', 'air')),
    # the frontier
    IdeaDef('frontier_desk', 'Desk for the Long Line', 'One office in the capital follows every post and hut on the frontier.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('diplomacy', 'document')),
    IdeaDef('customs_service', 'Inspectors in Every Hut', 'Customs huts on the plain staffed every day, with telephones and ledgers.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('gate', 'document')),
    IdeaDef('good_neighbour', 'Letters Across the Line', 'Regular letters and a standing offer of talks to the large neighbour.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.03}, ('diplomacy', 'peace')),
    IdeaDef('many_customers', 'Customers in Every Direction', 'Trade spread so thinly that no single buyer matters too much.',
            {'political_power_factor': 0.05, 'stability_factor': 0.03}, ('economy', 'diplomacy')),
    IdeaDef('watchers', 'Towers Along the Posts', 'Observation towers and logged crossings along the whole frontier.',
            {'army_core_defence_factor': 0.06, 'air_detection': 0.05}, ('security', 'telescope')),
    IdeaDef('junction_liaison', 'Someone at the Telephone', 'A liaison desk at District E answers every complaint within a day.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('communications', 'diplomacy')),
    IdeaDef('coast_watch', 'Skippers on Coast Watch', 'Fishing skippers and lighthouse keepers report anything unusual offshore.',
            {'naval_coordination': 0.03, 'air_detection': 0.05}, ('fishing', 'submarine')),
    IdeaDef('trade_fair', 'Fair Season at the Centre', 'An autumn fair for foreign buyers in the logistics centre sheds.',
            {'consumer_goods_factor': -0.03, 'production_speed_buildings_factor': 0.04}, ('economy', 'logistics')),
    IdeaDef('thaw_credit', 'Bonds at Longer Terms', 'Lenders quote longer terms while the great powers cooperate.',
            {'production_speed_buildings_factor': 0.05, 'consumer_goods_factor': -0.02}, ('economy', 'peace')),
    IdeaDef('crossing_sweep', 'Crossings Swept at Night', 'A week of inspectors and patrols on every crossing after dark.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('gate', 'security')),
    # the asteroid years
    IdeaDef('sky_watch', 'Weekly Asteroid Bulletins', 'Foreign bulletins on Ulysses translated and read on the radio each week.',
            {'stability_factor': 0.02}, ('meteor', 'communications')),
    IdeaDef('earth_shelters', 'Shelters Under the Streets', 'Earth-covered shelters dug for every street in the towns.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('marsh_dispersal', 'Reception Camps Inland', 'Trains, trucks and camps to move coastal families to the marsh district.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('refugees', 'rail')),
    IdeaDef('grain_pits', 'Two Seasons Underground', 'Lined grain pits in every district, filled at harvest price.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('economy', 'shelter')),
    IdeaDef('siren_code', 'The National Siren Code', 'One siren code and one telephone tree for all six districts.',
            {'stability_factor': 0.02, 'air_detection': 0.04}, ('communications', 'radar')),
    IdeaDef('reserve_wards', 'Wards in the School Halls', 'Stored beds and a roster of retired nurses ready to open in a day.',
            {'stability_factor': 0.03, 'war_support_factor': 0.02}, ('medical', 'civil')),
    # the turn of the century
    IdeaDef('decade_accounts', 'The Decade Volume', 'One account of the country in 1991 and in 2000, district by district.',
            {'political_power_factor': 0.05}, ('document', 'scales')),
    IdeaDef('open_accounts', 'Accounts in the Papers', 'The decade volume printed in weekly instalments with readers answered.',
            {'political_power_factor': 0.06, 'stability_factor': 0.03}, ('communications', 'document')),
    IdeaDef('second_session', 'The Review Session', 'The chamber reviews the entrenched articles after ten years.',
            {'stability_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'scales')),
    IdeaDef('bench_tour', 'The Bench on Tour', 'The bench reads its accounts aloud in every district hall.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05}, ('assembly', 'logistics')),
    IdeaDef('decree_codes', 'Decrees into Codes', 'A decade of decrees consolidated into codes, the harshest quietly dropped.',
            {'stability_factor': 0.04, 'political_power_factor': 0.05}, ('document', 'security')),
    IdeaDef('far_war_freight', 'Insured Against a Far War', 'State cover for coasters and cargo on routes toward a distant war.',
            {'consumer_goods_factor': -0.02, 'supply_consumption_factor': -0.03}, ('logistics', 'scales')),
    IdeaDef('second_programme', 'The Second Programme', 'A costed national programme to run past 2005.',
            {'production_speed_buildings_factor': 0.05, 'research_speed_factor': 0.02}, ('document', 'industry')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('constituent_cabinet', 'Cabinet Under the Entrenched Charter',
           'A cabinet answerable to the chamber elected under the entrenched charter, governing collectively and bound by the '
           'judgments of the charter court. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('district_bench', 'Bench of the Six Districts',
           'A governing bench of notables drawn from the published district lists, deciding by majority with no parties and '
           'no national campaign. Provisional gameplay office with no named holder.',
           'neutrality', 'conservatism_na'),
    Office('movement_executive', 'Executive Committee of the National Movement',
           'An executive committee of the national movement governing by decree, with the movement halls serving as its '
           'offices. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('canvass', 'The Canvass Returns', (
        "The canvassers come back from the six districts in the first weeks of the year with notebooks, tally sheets and "
        "sore feet. Their count is simple to state and hard to read aloud. Half of the country's adults say they follow the "
        "national movement. Nearly as many want government by non-party notables and administrators. One in a hundred backs "
        "the democratic colours under which the National Administration governs, and another one in a hundred the labour left.",
        "The Administration has run Romny with its election calendar shut. It has kept the works open, the guard paid and "
        "the capital quay busy, but it has not built a following of any size. The national movement fills halls beside the "
        "arms works and the logistics centre, while the notables run the co-operatives, the district offices and most of the "
        "trade without belonging to any party at all.",
        "Neither camp is a majority on its own, and neither will accept the other's government willingly. Before any minister "
        "proposes what Romny should become, the cabinet must decide what to do with the count itself. Printed in full, it "
        "tells both camps exactly how strong they are. Filed with the cabinet, it guides the Administration for a season and "
        "leaks within the year.",
    ), (
        Option('Print every tally sheet.', (Stability(0.02), PP(-20))),
        Option('File the count with the cabinet.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('movement_rally', 'A Rally at the Logistics Centre', (
        "On a Sunday in spring the national movement fills the yard of the logistics centre with marchers from every hall "
        "in the country. They arrive by truck, by train and on foot, carrying banners for work, order and the nation. "
        "Speakers stand on a flatbed wagon and demand that the Administration hand the seals to the half of Romny that, in "
        "their words, actually believes in something.",
        "The officials sent to watch from the back rows report a crowd that is disciplined, sober and young. Many marchers "
        "are arms workers; many more are farm sons from districts with no road and no prospects. The drill clubs keep order "
        "with whistles. The speeches attack the notables as a club of managers and the Administration as a government "
        "borrowed from nobody.",
        "The rally breaks up peacefully at dusk, and a written list of demands reaches the cabinet the next morning. "
        "Ministers must decide how the state answers. It can receive the movement's delegation in public, as one camp among "
        "others, or decline to meet it and let the papers reply. A third voice in the cabinet wants the drill clubs asked to "
        "register with the guard. Every hall will know the answer by Friday.",
    ), (
        Option('Receive the delegation in public.', (WarSupport(0.02), Stability(-0.01), PP(-10))),
        Option('Decline, and let the papers answer.', (Stability(0.02), WarSupport(-0.02))),
        Option('Ask the drill clubs to register with the guard.', (XP('army', 10), WarSupport(0.01))),
    ), picture=2),
    EventDef('empty_districts', 'Pegs Across Empty Ground', (
        "The survey crews return from the three empty districts with chains, pegs, soil samples and a shared sense of "
        "disbelief. The registers say each district holds about as many people as the capital district. On the ground the "
        "crews found scattered farms, fishing hamlets, cart tracks and almost nothing a ministry would call a town. No "
        "factory, paved road or recorded mineral lies in any of them.",
        "The rail-corner district is crossed by the capital line at one corner and served by none of it. District E, at the "
        "frontier junction, meets Yuktobania and Kaluga across open plain and turns to mud every spring. District F runs "
        "along the coast for a long way with no landing deeper than a fishing slip. All three are flat, mostly dry and "
        "fertile in patches, and all three have been governed by letter.",
        "The crews recommend roads before anything else, and two settlement schools are already quarrelling over what should "
        "follow. Before choosing, the cabinet must decide how far it trusts the registers. Their population figures decide "
        "grants, reserve rolls and school budgets. If they are wrong, every plan built on them is wrong as well, and the "
        "empty districts will be planned for people who may not be there.",
    ), (
        Option('Recount the three districts first.', (PP(-15), Stability(0.02))),
        Option('Plan on the registers as they stand.', (PP(25), Research('construction_tech', 0.5, 1))),
    ), picture=0),
    EventDef('ten_works', 'The Works Sheet Is Read', (
        "The inventory team lays one long sheet across the cabinet table. Ten works are listed on it, five making arms and "
        "five making everything else. The arms works in the capital district, District B and the marsh district build "
        "rifles, trucks, rail wagons and support equipment for four guard formations. Each has its own ministry desk, its "
        "own suppliers and its own idea of what a full order book looks like.",
        "The sheet shows idle shifts in every arms works between orders, and shortages in every civil works during them. "
        "Trucks leave the line faster than the guard has drivers to use them, and hundreds sit in the depots. Rail wagons "
        "are built to three different coupling standards. The civil works, meanwhile, import parts the arms works could "
        "make in an afternoon if anyone asked them.",
        "Three schools are already circulating memoranda: spares and sustainment, motor works for the plains, or a shift of "
        "half the halls to civil goods. The works managers want the sheet kept confidential until a model is chosen. The "
        "treasury wants it put in front of the movement and the notables, who both claim to speak for the workers on those "
        "idle shifts.",
    ), (
        Option('Show the sheet to both camps.', (Stability(-0.01), Research('industry', 0.5, 1))),
        Option('Keep it with the managers.', (PP(30),)),
    ), picture=1),
    EventDef('ground_ledger', 'Latex, Bauxite and Rock', (
        "The ledger of Romny's resources arrives in two volumes, one geological and one agricultural. Steel ore lies in the "
        "capital district, District B and the marsh district in roughly equal measure. Bauxite follows the same three "
        "districts. There is a little oil and, more unusually for a country this size, a working crop of rubber in groves "
        "tapped by tenants who rarely see a written contract.",
        "The empty districts have nothing recorded at all, which the geologists suspect means nobody has looked. Most of "
        "what is mined or tapped leaves through the capital quay as raw cargo, weighed by the buyers' own clerks and priced "
        "in foreign money. The works at home buy imported steel shapes, and tyres made from latex that may well have left "
        "Romny the season before.",
        "The cabinet must decide what the ledger is for. The trading school wants it printed for foreign buyers as a "
        "catalogue. The industrial school wants it kept as a planning document for quotas and home works. The planters want "
        "to know whether either school intends to replant the groves, and the miners want pumps before they hear any more "
        "promises.",
    ), (
        Option('Print it as a catalogue for buyers.', (PP(20), Stability(-0.01))),
        Option('Keep it as a planning document.', (Research('excavation_tech', 0.5, 1),)),
    ), picture=1),
    EventDef('flat_ground', 'Where the Guard Sleeps', (
        "The guard's own review is shorter than the cabinet expected and blunter than the commanders wanted. Four "
        "formations of six battalions, each with an engineer company, are split between the capital centre and the "
        "logistics centre in District B. They have rifles, support equipment and hundreds of trucks in the depots. They have "
        "no posting in the marsh district or District E, the two other districts that face Yuktobania.",
        "Romny's ground offers little to a defender. The capital district and four of the others are open plain, cut by "
        "drains and slow streams. Only the marsh district breaks the pattern, with ground soft enough to stop a column. The "
        "guard's training manual, meanwhile, was written for mountain warfare, and its instructors still teach rope work on "
        "the drill ground beside the quay.",
        "Nobody in the review describes any neighbour as a threat. It simply notes that a guard sitting in two garrisons can "
        "protect the capital and the logistics centre, and nothing else. One school of officers wants to dig in on the "
        "marsh; another wants the whole guard on wheels. First, the commanders must decide how much of the review leaves "
        "their offices.",
    ), (
        Option('Brief the cabinet in full.', (Stability(-0.01), XP('army', 15))),
        Option('Keep the review inside the guard.', (PP(20), WarSupport(0.01))),
    ), picture=1),
    EventDef('one_squadron', 'The Air Arm Is Counted', (
        "The air arm's count fits on a single page. Twelve fighters stand on the capital field beside the quay, with four "
        "more airframes in reserve and a fuel silo that serves the field, the works and the guard's trucks alike. There is "
        "one runway, one control hut and one telephone line to the ministry. On a clear day the whole air arm can be seen "
        "from the end of the runway.",
        "The pilots are well trained and few. The mechanics are better trained and fewer, because the freight companies pay "
        "them more. Flying hours are rationed by fuel, and fuel is rationed by the treasury. The fighters can reach the "
        "frontier with Yuktobania and Kaluga in minutes, but nobody on the ground would see them coming or going, because "
        "Romny has no radar at all.",
        "Two schools argue about what the air arm is for. One wants it patrolling the frontier, where it can learn and be "
        "seen. The other wants it held over the capital, where everything valuable sits. Before either wins, the commanders "
        "want more money, and the treasury wants to know what the money would buy that twelve fighters cannot already do.",
    ), (
        Option('Fund more flying hours.', (XP('air', 15), PP(-15))),
        Option('Hold the budget and train on the ground.', (PP(15), Research('air_doctrine', 0.5, 1))),
    ), picture=2),
    EventDef('large_neighbour', 'The Line on the Plain', (
        "The officials who walk the frontier come back with a long report. Three districts face Yuktobania: District B with "
        "its logistics centre, the marsh district with its arms works, and District E, where Kaluga also meets the line. The "
        "frontier runs mostly across open plain, marked by stone posts, ditches and the occasional customs hut. No railway "
        "crosses it, and the roads that do are cart tracks.",
        "The report describes farms split by the line, families with relatives on both sides, smugglers who move tyres and "
        "spirits at night, and customs huts staffed one day in three. Nothing in it suggests hostility from anyone. It does "
        "suggest that Romny has never decided how to live beside a neighbour many times its size, and that each district "
        "office has improvised its own answer.",
        "Three schools are already pressing the cabinet: friendship and trade with Yuktobania written into letters, trade "
        "spread so widely that no buyer matters too much, or watchtowers and patrols along the posts. Before any of them is "
        "heard, the cabinet must decide whether the report goes back to the districts that live on the line, or stays in the "
        "capital with the people who will choose for them.",
    ), (
        Option('Send the report to the frontier districts.', (Stability(0.02), PP(-10))),
        Option('Keep it in the capital.', (PP(25), Stability(-0.01))),
    ), picture=1),
    EventDef('impact_announced', 'The Plain Has No Caves', (
        "The radio carries the FCU President's announcement in the afternoon, and by evening every district office has a "
        "queue. Ulysses will strike the Earth. Nobody can say where its fragments will fall, and Romny has no observatory, "
        "no satellite and no partner who can tell it more than the bulletins already say. The cabinet meets at night in the "
        "capital and the lights stay on until dawn.",
        "The country's geography offers little comfort. Five of its six districts touch the sea along a low coast, and all "
        "but the marsh district are open plain with no hills, caves or cuttings to hide in. Engineers propose to dig "
        "shelters under every street. Planners propose to move families inland to the marsh district instead. Both plans "
        "cost more than the works budget, and neither can be finished quickly.",
        "The public mood swings between panic and a stubborn refusal to believe it. Grain disappears from the shops, prayer "
        "halls fill, and the movement's halls hold meetings about order and duty that draw far beyond their usual members. "
        "The cabinet must decide how to speak to the country tonight, before either camp speaks for it.",
    ), (
        Option('Speak plainly and announce the plans.', (WarSupport(0.02), Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Promise calm and plan quietly.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1996 / 04.20; the response in Romny is gameplay', picture=2),
    EventDef('decade_audit', 'The Volume on the Table', (
        "The first full account of the country since 1991 runs to six hundred pages and weighs as much as a brick. It "
        "compares Romny at the start of the decade with Romny now, district by district: kilometres of road, works with a "
        "roof, guard posts, harvests, debts, schools and the camp that holds the seals. Its authors were drawn from the "
        "treasury, the statistical office and the district offices.",
        "Its findings flatter nobody completely. The empty districts are less empty, and in places still empty. The works "
        "are busier, but the arms halls still swing between idle shifts and rush orders. The frontier is calm and the guard "
        "better placed than it was. The camp that governs has its achievements, and the camps that do not have their "
        "grievances printed on the same pages.",
        "The cabinet must decide who reads it first. Sent to the district offices, it will be argued over in every town hall "
        "before ministers have finished their own copies. Sent to the leaders of the camps, it will be argued over in private "
        "and quoted selectively in public. The figures will be the same either way; the argument that follows will not.",
    ), (
        Option('Send it to the district offices first.', (Event('audit_answer', 30), Stability(0.01))),
        Option('Send it to the camp leaders first.', (PP(30), Stability(-0.02))),
    ), picture=0),
    EventDef('audit_answer', 'Letters to the Accounts', (
        "A month after the volume reaches the district offices, the replies begin to arrive in sacks. Farmers in the "
        "rail-corner district dispute the harvest tables. Works councils in the marsh district send corrected shift counts. "
        "A schoolteacher in District F writes forty pages on the children who walk an hour to class, with a map drawn by her "
        "pupils pinned to the back.",
        "Not every letter is useful, and some are simply angry. The movement halls send form letters by the hundred, each "
        "with the same three complaints. Notables send polite notes defending the figures their own offices supplied. Yet "
        "the statistical office finds dozens of genuine errors and several hamlets missing from the registers, and admits "
        "the volume was wrong in ways the capital could never have seen.",
        "The cabinet must decide what to do with the corrections. A second, corrected edition would take another year and "
        "concede that the first was flawed. A supplement listing the errors could be printed in weeks, but would bury the "
        "best letters in small type. Either way, the people who wrote in will be watching to see whether anyone in the "
        "capital read them.",
    ), (
        Option('Print a corrected edition.', (Stability(0.03), PP(-20))),
        Option('Print a supplement of errors.', (PP(15), Stability(0.01))),
    ), picture=0),
)

# --- branches ------------------------------------------------------------------------------------
POLITICS = Branch('politics', 'Fifty, Forty-Eight and One', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_canvass', 'The Winter Canvass',
          "Romny enters 1991 governed by an unnamed National Administration that carries democratic colours while the "
          "election calendar stays shut. Canvassers sent through all six districts come back with a hard count: half the "
          "country follows the national movement, nearly half wants non-party government, and one citizen in a hundred "
          "backs the colours the Administration wears. Nobody can govern well without knowing that.",
          ('ballot', 'document'), reward=(Idea('borrowed_colours'), Event('canvass'))),
    Focus('pol_movement_halls', 'Inside the Movement Halls',
          "The national movement meets in rented halls beside the arms works and the logistics centre, where its speakers "
          "promise discipline, work and pride to young men who drill on Sundays. Sending officials to sit in the back rows "
          "and read the pamphlets costs nothing but nerve. It tells the Administration what half its citizens actually want "
          "before anyone sits down to bargain with them.",
          ('assembly', 'security'), after=('pol_canvass',), reward=(Event('movement_rally'), Flag('movement_read'))),
    Focus('pol_notables', 'The Non-Party Lists',
          "The other great camp has no party at all. It is a loose web of district notables, co-operative boards, works "
          "managers and retired prefects who want competent government and no ideology. Publishing the names on their "
          "informal lists makes them visible for the first time, and answerable. Several notables would much rather have "
          "stayed comfortably out of sight.",
          ('document', 'assembly'), after=('pol_canvass',), reward=(Flag('lists_published'), Stability(0.02))),
    Focus('pol_papers', 'Licences for District Papers',
          "Romny has one official gazette and a handful of movement sheets printed on borrowed presses. Licensing a weekly "
          "paper in every district, under a single press law, lets each camp argue in print rather than in halls and on "
          "street corners. The papers will attack the Administration from both sides at once, and the censors who once read "
          "everything lose their jobs.",
          ('communications', 'document'), after=('pol_canvass',), reward=(Flag('press_law'), PP(-10))),
    Focus('pol_works_councils', 'Elected Councils in the Works',
          "Half of Romny's factories make arms, and their workforces are the national movement's best recruiting ground. "
          "Elected works councils with a say over shifts, safety and canteens give those workers a channel that does not "
          "run through a movement hall. Managers lose some control of their own floors, and the movement accuses the "
          "Administration of buying its members with soup.",
          ('assembly', 'industry'), after=('pol_movement_halls',), reward=(Idea('works_councils'),)),
    Focus('pol_path_charter', 'Write the Charter First',
          "A small circle of jurists inside the Administration proposes the slow road: write a charter of rights, courts and "
          "a single chamber, entrench it, and only then open the ballot. The democratic colours would finally mean "
          "something. Both great camps would fight the draft clause by clause, and the Administration would govern unloved "
          "for years while they did.",
          ('scales', 'document'), after=('pol_papers',), cost=10, exclusive=('pol_path_bench', 'pol_path_movement'),
          reward=(SwapIdea('borrowed_colours', 'rights_charter'),)),
    Focus('pol_path_bench', 'Hand the Seals to the Notables',
          "The non-party camp asks for what it already half has: a governing bench of district notables, chosen from the "
          "lists, ruling without parties and without a national campaign. Works managers, co-operative boards and prefects "
          "would openly run the country they already run informally. It is calm and competent. The movement, with half the "
          "country behind it, would be shut out by design.",
          ('assembly', 'document'), after=('pol_notables',), cost=10, exclusive=('pol_path_charter', 'pol_path_movement'),
          reward=(SwapIdea('borrowed_colours', 'notables_bench'),)),
    Focus('pol_path_movement', 'Open the Door to the Movement',
          "Half the country follows the national movement, and its leaders say a government that ignores half its people "
          "has no right to the seals. Letting the movement form an executive would match power to numbers. It would also "
          "hand the state to a movement that distrusts courts, papers and the non-party half of Romny, and that the frontier "
          "commanders already watch carefully.",
          ('security', 'ballot'), after=('pol_movement_halls',), cost=10, exclusive=('pol_path_charter', 'pol_path_bench'),
          reward=(SwapIdea('borrowed_colours', 'movement_pledge'),)),
    Focus('pol_regime_republic', 'Proclaim the Constituent Republic',
          "The charter is ratified by a constituent assembly elected under its own rules, and a cabinet answerable to the "
          "new chamber takes the seals from the Administration. The change runs through the office, not a person. The first "
          "chamber is fractious, with movement and non-party deputies outnumbering the charter's authors, and every vote is a "
          "lesson in losing gracefully.",
          ('ballot', 'scales'), after=('pol_path_charter',), cost=10,
          exclusive=('pol_regime_bench', 'pol_regime_movement'),
          reward=(Regime('constituent_cabinet'), Flag('rule_republic'))),
    Focus('pol_regime_bench', 'Seat the Bench of Districts',
          "Each district sends notables from its list to a governing bench that sits in the capital and decides by majority, "
          "with no parties and no national campaign. The Administration's officials become the bench's clerks. Decisions "
          "are quick and practical. The national movement calls the bench a club of managers, and its halls fill every week "
          "the bench is in session.",
          ('assembly', 'command'), after=('pol_path_bench',), cost=10,
          exclusive=('pol_regime_republic', 'pol_regime_movement'),
          reward=(Regime('district_bench'), Flag('rule_bench'))),
    Focus('pol_regime_movement', 'The Movement Executive Takes the Seals',
          "An executive committee of the national movement takes the seals and governs by decree, with the halls as its "
          "offices and the Sunday drill clubs as its stewards. Elections stay shut. The arms districts celebrate. The "
          "non-party half of the country goes quiet in public, and lenders, neighbours and the frontier staff all start "
          "reading the executive's statements twice.",
          ('security', 'command'), after=('pol_path_movement',), cost=10,
          exclusive=('pol_regime_republic', 'pol_regime_bench'),
          reward=(Regime('movement_executive'), Flag('rule_movement'))),
    Focus('pol_charter_court', 'Seat the Charter Court',
          "The republic appoints a charter court of judges with fixed terms who can strike down any law that breaches the "
          "entrenched articles. Movement deputies object that unelected judges now outrank the chamber. The court's first "
          "judgments are cautious and narrowly argued. They still prove that the charter binds whoever holds the cabinet, "
          "which was the whole point of writing it first.",
          ('scales', 'assembly'), after=('pol_regime_republic',),
          exclusive=('pol_bench_rotation', 'pol_movement_columns'),
          reward=(SwapIdea('rights_charter', 'charter_court'),)),
    Focus('pol_bench_rotation', 'One Seat in Three Rotates',
          "Critics say the bench is a closed club, and they are partly right. A rule that one seat in three rotates each "
          "spring, filled from fresh district lists, brings in younger managers and co-operative officers. Some veterans lose "
          "their seats and sulk. The bench becomes less cosy and more legitimate, though it still has no place for the "
          "movement's half of the country.",
          ('assembly', 'civil'), after=('pol_regime_bench',),
          exclusive=('pol_charter_court', 'pol_movement_columns'),
          reward=(SwapIdea('notables_bench', 'rotating_bench'),)),
    Focus('pol_movement_columns', 'Labour Columns for the Plains',
          "The executive turns the drill clubs into labour columns that spend each summer cutting roads and drains across "
          "the empty districts. Young men gain pay, uniforms and a purpose, and the roads arrive faster than any ministry "
          "could manage. The columns answer to the movement, not the ministries, and each one is a body in the field that "
          "the guard does not command.",
          ('tools', 'security'), after=('pol_regime_movement',),
          exclusive=('pol_charter_court', 'pol_bench_rotation'),
          reward=(SwapIdea('movement_pledge', 'labour_columns'),)),
))

DISTRICTS = Branch('districts', 'Half the Map Unbuilt', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dist_stakes', 'Stake Out the Empty Districts',
          "Three of Romny's six districts hold no road worth the name, no factory and no recorded mineral: the district the "
          "capital railway clips on its way to the logistics centre, District E at the frontier junction, and District F on "
          "the coast. Each still counts a large population on paper. Survey crews with pegs and chains go out first, because "
          "nobody can build on land nobody has measured.",
          ('tools', 'civil'), reward=(Idea('district_survey'), Event('empty_districts'))),
    Focus('dist_rail_corner', 'Halts Along the Rail Corner',
          "The level-two line from the capital to the logistics centre cuts across one corner of the rail-corner district "
          "and stops nowhere in it. Building halts, sidings and a gravel road from the track inland gives the district its "
          "first link to anywhere. The railway objects to stops that slow its freight, and the district asks why nobody "
          "thought of this sooner.",
          ('rail', 'civil'), after=('dist_stakes',), reward=(Build('infrastructure', 1, 549),)),
    Focus('dist_junction_road', 'A Road Out to the Junction',
          "District E is the only part of Romny that touches both Yuktobania and Kaluga, yet no railway reaches it and its "
          "tracks turn to mud every spring. A graded road from the capital district to the frontier corner gives traders, "
          "inspectors and the guard a way in. It also makes the junction easier to reach from the other side, which the "
          "frontier staff notes in writing.",
          ('logistics', 'gate'), after=('dist_stakes',), reward=(Build('infrastructure', 1, 561),)),
    Focus('dist_coast_road', 'The District F Shore Road',
          "District F is a long stretch of coastal plain with no town of any size and no road along its shore. A shore road "
          "from the capital district gives fishing hamlets a way to market and the survey crews a way to work. It is the "
          "cheapest of the three district roads, because the ground is flat and dry, and also the least urgent of them.",
          ('fishing', 'logistics'), after=('dist_stakes',), reward=(Build('infrastructure', 1, 573),)),
    Focus('dist_planned_towns', 'Towns Drawn in the Capital',
          "The planning school wants the state to build towns to a single pattern: a square, a works, a school, housing in "
          "rows and a road or rail link, placed where the survey says water and soil are good. Towns rise quickly and look "
          "alike. Settlers go where the plan sends them, and the treasury carries the whole cost and all of the blame.",
          ('civil', 'document'), after_any=('dist_rail_corner', 'dist_junction_road', 'dist_coast_road'), cost=10,
          exclusive=('dist_homesteads',), reward=(SwapIdea('district_survey', 'planned_towns'),)),
    Focus('dist_homesteads', 'Land to Whoever Ploughs It',
          "The other school would rather give land away. Any family that farms a surveyed plot for five years receives title "
          "to it, with tools on credit and a road promised within reach. Settlement is slower and patchier, and the plots "
          "follow good soil rather than any plan. It costs the treasury far less, and the settlers owe the state nothing "
          "beyond their taxes.",
          ('civil', 'economy'), after_any=('dist_rail_corner', 'dist_junction_road', 'dist_coast_road'), cost=10,
          exclusive=('dist_planned_towns',), reward=(SwapIdea('district_survey', 'homestead_grants'),)),
    Focus('dist_rail_corner_works', 'A Works Hall at the Rail Corner',
          "The first planned town rises beside the new halts at the rail corner, and its square faces a works hall built "
          "before the houses are finished. The hall makes pipe, fittings and window frames for the next towns. Workers come "
          "from the capital on contract, and the district finally has something to point at on a map besides survey pegs.",
          ('industry', 'rail'), after=('dist_planned_towns',), reward=(Build('industrial_complex', 1, 549),)),
    Focus('dist_shore_mill', 'A Co-operative Mill on the Shore',
          "Homestead families along the District F shore pool their first harvests to build a mill and repair shop beside "
          "the shore road. The state lends the machinery and the families own the building. It is small and slow to pay "
          "back. It is also the first factory in Romny that belongs to the people who work in it, which both great camps "
          "notice at once.",
          ('industry', 'fishing'), after=('dist_homesteads',), reward=(Build('industrial_complex', 1, 573),)),
    Focus('dist_boards', 'District Boards from the Lists',
          "With the non-party lists now public, each empty district can draw a small board from the notables who actually "
          "live there. The boards decide where the next well, school and road spur goes, and answer for it at an open "
          "meeting every quarter. The capital loses some control of its own programme, and gains people on the ground who "
          "will defend it.",
          ('assembly', 'civil'), after_any=('dist_planned_towns', 'dist_homesteads'), requires=(HasFlag('lists_published'),),
          reward=(Idea('district_boards'),)),
    Focus('dist_small_yard', 'A Boat Yard for District F',
          "Romny owns no dockyard at all; its single naval base serves freighters and coasters at the capital quay. "
          "A small yard on the District F shore, building and repairing coasters and fishing boats, gives the country its "
          "first hull trade. The yard will never build warships. It will keep the convoy fleet repaired without queuing for "
          "foreign berths.",
          ('navy', 'tools'), after=('dist_coast_road',), reward=(Build('dockyard', 1, 573),)),
    Focus('dist_settled_census', 'Count the Settled Districts',
          "Some years after the first pegs went in, census clerks return to the three empty districts and count what has "
          "changed: households, wells, schools, fields under plough and workshops with a roof. The figures will decide the "
          "next budget. They will also show whether the chosen model worked, and the losing school is already preparing its "
          "objections to the method.",
          ('document', 'civil'), after_any=('dist_rail_corner_works', 'dist_shore_mill'),
          reward=(Flag('districts_settled'), Research('construction_tech', 0.5, 1))),
))

WORKS = Branch('works', 'Half the Factories Make Arms', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_sheet', 'Put the Ten Works on One Sheet',
          "Romny has ten factories of any size, and five of them make arms: rifles, trucks, rail wagons and support "
          "equipment for a guard of four formations. They sit in the capital district, District B and the marsh district, "
          "each run from its own ministry desk. One inventory sheet, with costs, orders and idle shifts, is the first view "
          "anyone has had of the whole.",
          ('industry', 'document'), reward=(Idea('works_inventory'), Event('ten_works'))),
    Focus('works_marsh_drains', 'Drain the Marsh Works Yards',
          "The two arms works in the marsh district stand on ground that floods each spring, and their yards turn to black "
          "mud that swallows trucks to the axle. Draining the yards and raising the access road on a causeway is unglamorous "
          "work. Shifts stop losing days to water, and the railway spur from the capital stops sinking a little further "
          "every year.",
          ('tools', 'industry'), after=('works_sheet',), reward=(Build('infrastructure', 1, 541),)),
    Focus('works_centre_sheds', 'Sheds at the Logistics Centre',
          "The logistics centre in District B is where two guard formations sit and where most finished equipment waits for "
          "collection. It has too few covered sheds, so trucks and wagons rust in the open. New sheds, loading ramps and a "
          "paved apron make the centre a working depot. The money comes from the works budget, and the works managers "
          "complain about it.",
          ('logistics', 'tools'), after=('works_sheet',), reward=(Build('infrastructure', 1, 536),)),
    Focus('works_spares', 'A Shelf of Spare Barrels',
          "The sustainment school says a small guard does not need new rifles every year; it needs barrels, tyres, springs "
          "and radios on the shelf when old ones fail. Turning the arms works toward replacement parts keeps every formation "
          "working longer at lower cost. Output looks small on paper, and the movement calls it a factory programme for a "
          "country that has given up.",
          ('tools', 'logistics'), after_any=('works_marsh_drains', 'works_centre_sheds'), cost=10,
          exclusive=('works_motor', 'works_civil'), reward=(SwapIdea('works_inventory', 'spares_first'),)),
    Focus('works_motor', 'Trucks for Flat Country',
          "The motor school points at the plains: a country this flat should move on wheels, and its arms works already turn "
          "out trucks. A new assembly hall at the logistics centre would build many more, with engines and axles made at "
          "home. The trucks would serve farms and towns as well as the guard, provided the fuel to run them can be found.",
          ('logistics', 'industry'), after_any=('works_marsh_drains', 'works_centre_sheds'), cost=10,
          exclusive=('works_spares', 'works_civil'),
          reward=(SwapIdea('works_inventory', 'motor_works'), Build('arms_factory', 1, 536))),
    Focus('works_civil', 'Turn Half the Halls Civil',
          "The civil school wants the balance moved. Half the factories make arms for a country at peace with everyone, "
          "while shops in the capital import pumps, stoves and bicycles. Converting halls in the marsh district to household "
          "goods would fill those shelves. The guard would lose capacity it may want back, and arms workers would need to "
          "learn new trades.",
          ('rebuild', 'industry'), after_any=('works_marsh_drains', 'works_centre_sheds'), cost=10,
          exclusive=('works_spares', 'works_motor'),
          reward=(SwapIdea('works_inventory', 'civil_halls'), Build('industrial_complex', 1, 541))),
    Focus('works_depots', 'Parts Depots Along the Line',
          "Spare parts are only useful where the trucks break down. Depots at the capital centre, the logistics centre and "
          "the marsh works, each stocked from the same catalogue, put a replacement within a day of any formation. The "
          "catalogue takes a year to agree, because every ministry desk used its own part numbers, and some still insist "
          "theirs were better.",
          ('logistics', 'document'), after=('works_spares',), reward=(SwapIdea('spares_first', 'replacement_depots'),)),
    Focus('works_tyre_line', 'A Tyre and Axle Line',
          "Romny grows rubber and imports almost every tyre it fits. A tyre and axle line beside the new truck hall uses home "
          "latex and home steel, so a truck built at the logistics centre rolls on parts made in the same district. The line "
          "needs foreign moulds and foreign chemists for its first years, and their fees are high.",
          ('economy', 'logistics'), after=('works_motor',), reward=(SwapIdea('motor_works', 'truck_and_tyre'),)),
    Focus('works_household', 'Stoves, Pumps and Bicycles',
          "The converted halls start with goods that need little new tooling: cast stoves, hand pumps, bicycle frames and "
          "pressure lamps. They sell out in the capital within weeks and reach the empty districts by the new roads. Margins "
          "are thin, the import merchants protest to the ministry, and the halls must keep learning faster than their "
          "competitors abroad.",
          ('economy', 'civil'), after=('works_civil',), reward=(SwapIdea('civil_halls', 'household_lines'),)),
    Focus('works_apprentices', 'Apprentice Benches in Every Works',
          "Every works keeps a bench of apprentices who learn on real orders under a master for three years, paid a wage "
          "from the first week. The scheme costs output, because masters teach instead of making, and some apprentices leave "
          "as soon as they qualify. Without it, Romny's works will still be run by men who learned their trade before 1991.",
          ('training', 'tools'), after=('works_sheet',), reward=(Idea('apprentice_benches'),)),
    Focus('works_wagon_shop', 'Rebuild the Wagon Shops',
          "Romny's works build rail wagons as well as rifles, and its stock of trains is small and old. Rebuilding the wagon "
          "shops at the capital centre for steel-bodied wagons with one coupling standard serves every model, whatever the "
          "works now make. The shops will sit idle between orders, which the treasury dislikes, and be busy when the line "
          "needs them, which the railway likes.",
          ('rail', 'tools'), after_any=('works_depots', 'works_tyre_line', 'works_household'),
          reward=(Research('train_tech', 0.5, 2),)),
))

GROUND = Branch('ground', 'Rubber, Alloy and Ore', 1993, 'FOCUS_FILTER_RESEARCH', (
    Focus('res_ledger', 'Count What the Ground Gives',
          "Romny's resources sit in three districts only: steel ore, bauxite, a little oil and rubber groves in the capital "
          "district, District B and the marsh district. The empty districts have none recorded. A full geological and "
          "agricultural ledger, district by district, prices every deposit and grove. It shows a country richer in rubber "
          "than in almost anything else, and poorer in reliable buyers.",
          ('document', 'economy'), reward=(Idea('resource_ledger'), Event('ground_ledger'))),
    Focus('res_groves', 'Replant the Rubber Groves',
          "Many rubber trees in the capital district and District B are past their best, tapped too hard for too long by "
          "tenants with no reason to replant. A replanting scheme with grove roads, nurseries and a guaranteed price for new "
          "latex will cut output for several years before it raises it. The tenants want the guarantee in writing, and so "
          "does the treasury.",
          ('economy', 'civil'), after=('res_ledger',), reward=(Build('infrastructure', 1, 0), Stability(0.01))),
    Focus('res_sell_raw', 'Sell Raw from the Capital Quay',
          "The trading school says Romny should do what it does best and sell ore, bauxite and latex raw through the capital "
          "quay to whoever pays most. The money comes quickly and nobody needs to build new factories. Every price swing "
          "abroad becomes a budget crisis at home, though, and the country stays a supplier of other people's industries.",
          ('economy', 'navy'), after=('res_groves',), cost=10, exclusive=('res_keep_home',),
          reward=(SwapIdea('resource_ledger', 'raw_exports'),)),
    Focus('res_keep_home', 'Feed the Home Works First',
          "The industrial school wants raw materials kept at home under export quotas, so that Romny's own works buy them "
          "first and at a fixed price. Factories gain a secure supply and the country gains finished goods to sell. "
          "Exporters lose margin and complain to every minister, and the quotas invite smuggling across the long frontier "
          "with Yuktobania.",
          ('industry', 'scales'), after=('res_groves',), cost=10, exclusive=('res_sell_raw',),
          reward=(SwapIdea('resource_ledger', 'home_stock'),)),
    Focus('res_quay_scales', 'Public Scales on the Capital Quay',
          "Raw cargo is only as valuable as its weight and grade, and cargo at the capital quay has been weighed by the "
          "buyers' own clerks. Public scales, a grading office and published prices for each shipment stop the quiet "
          "short-weighting that has cost exporters dearly. Buyers threaten to go elsewhere. Few do, because the cargo is "
          "good and the alternatives lie farther away.",
          ('scales', 'navy'), after=('res_sell_raw',), reward=(SwapIdea('raw_exports', 'graded_cargo'),)),
    Focus('res_smelter', 'An Alumina Smelter at the Rail Corner',
          "Bauxite from the marsh district and District B leaves the country as rock. A smelter beside the new halts at the "
          "rail corner, fed by rail from both deposits, would turn it into alumina and then metal for the truck and wagon "
          "shops. It needs a great deal of power and patience, and its first years will run at a loss.",
          ('industry', 'rail'), after=('res_keep_home',), reward=(Build('industrial_complex', 1, 549),)),
    Focus('res_war_prices', 'Latex Prices in a Distant War',
          "In the spring of 1995 war breaks out around Belka, far from Romny's frontiers. Within weeks the price of rubber "
          "and aluminium jumps as buyers stock up against shortages. Romny takes no part in the war and wants none. Whether "
          "it should sell into the price spike or hold stock for its own works is a question the cabinet must settle this "
          "season.",
          ('economy', 'diplomacy'), after=('res_ledger',), requires=(After('1995.3.25'),),
          reward=(TimedIdea('war_premium', 365),)),
    Focus('res_marsh_pits', 'Deeper Pits in the Marsh',
          "The marsh district's ore lies under waterlogged ground that the old pits never reached below a few metres. Pumps, "
          "timbering and a small school for pit engineers would open the deeper seams. The work is dangerous and slow, the "
          "pumps burn fuel the country must buy, and the engineers learn methods that will serve every later mine in Romny.",
          ('tools', 'document'), after=('res_ledger',), reward=(Research('excavation_tech', 0.5, 2),)),
    Focus('res_synthetic', 'Latex from the Laboratory',
          "Natural rubber is Romny's best card, and the chemists in the capital want to know how long it will stay one. "
          "Small trials in synthetic latex, run with the tyre makers, teach the country what its competitors might do. "
          "Planters fear the research will undercut them. The chemists answer that it is better to learn the threat in a "
          "laboratory than to meet it in the market.",
          ('science', 'economy'), after_any=('res_quay_scales', 'res_smelter'), reward=(Research('synth_resources', 0.5, 2),)),
))

GUARD = Branch('guard', 'A Guard for Flat Ground', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_review', 'Two Garrisons for Six Districts',
          "Romny's territorial guard is four infantry formations of six battalions, each with an engineer company. Two sit "
          "at the capital centre and two at the logistics centre in District B. None is stationed in the marsh district or "
          "District E, though both face Yuktobania. A review of where the guard sits, and why, is overdue and will "
          "embarrass several commanders.",
          ('security', 'command'), reward=(Idea('guard_garrisons'), Event('flat_ground'))),
    Focus('guard_mountain_manual', 'Retire the Mountain Manual',
          "The guard still trains from a mountain warfare manual, though Romny's highest ground is a railway embankment. A "
          "rewritten manual for open plain, ditches, marsh and river lines teaches what soldiers will actually face. The "
          "mountain instructors protest that their skills are rare and worth keeping, and a few are kept on to teach "
          "climbing to the engineers.",
          ('document', 'training'), after=('guard_review',), reward=(Research('land_doctrine', 0.5, 1),)),
    Focus('guard_marsh_anchor', 'Anchor the Line on the Marsh',
          "The fixed-defence school wants the guard dug in where the ground helps: the marsh district, the one stretch of "
          "Romny that is not open plain. Prepared positions and a causeway road behind them would give a small army a place "
          "to hold. The plains to either side would be watched rather than defended, and the districts there know it.",
          ('security', 'tools'), after=('guard_review',), cost=10, exclusive=('guard_wheels',),
          reward=(SwapIdea('guard_garrisons', 'marsh_anchor'), Build('infrastructure', 1, 541))),
    Focus('guard_wheels', 'Put the Guard on Wheels',
          "The mobile school points to the depots: Romny holds hundreds of trucks in stock while its infantry walks. Putting "
          "every formation on wheels, with drivers trained and fuel allotted, would let two garrisons reach any district in "
          "a day. The trucks would wear out faster and the fuel bill would climb, but the plains would stop being a "
          "weakness.",
          ('logistics', 'security'), after=('guard_review',), cost=10, exclusive=('guard_marsh_anchor',),
          reward=(SwapIdea('guard_garrisons', 'motor_columns'),)),
    Focus('guard_district_rolls', 'Reserve Rolls in Every District',
          "Every district keeps a roll of trained reservists who can report to the nearest garrison within three days, with "
          "their rifles held at the district office. The rolls bring the empty districts into the guard for the first time. "
          "Clerks must be paid, rifles counted and reservists drilled each year, and some district officials resent the "
          "extra duty.",
          ('document', 'security'), after=('guard_review',), reward=(Idea('district_rolls'),)),
    Focus('guard_drill_clubs', 'Bring the Drill Clubs Under the Guard',
          "The national movement's Sunday drill clubs train young men with old rifles and no officers. Registering every "
          "club with the guard, under guard instructors and guard rules, turns an unofficial militia into a reserve the "
          "state commands. The movement's leaders call it theft of their members. Many members are glad of real training and "
          "a proper range.",
          ('training', 'security'), after=('guard_district_rolls',), requires=(HasFlag('movement_read'),),
          reward=(Idea('registered_clubs'),)),
    Focus('guard_junction_company', 'A Company at the Junction',
          "District E touches two neighbours and has never had a soldier stationed in it. A single company in a barracks "
          "near the junction road, rotated every six months from the capital garrisons, gives the guard eyes on the frontier "
          "corner and the district a reason to believe it belongs to the country. Neighbours will notice the barracks, and "
          "the frontier staff must explain it.",
          ('security', 'gate'), after=('guard_district_rolls',), reward=(Flag('junction_company'), XP('army', 15))),
    Focus('guard_batteries', 'Guns Before More Battalions',
          "The guard's doctrine already favours firepower over numbers, which suits a country that cannot raise many "
          "battalions. Buying and training a few modern batteries, with observers at every formation headquarters, "
          "multiplies what the infantry can hold. The guns cost more than a battalion, and their crews take two years to "
          "train properly.",
          ('missile', 'command'), after_any=('guard_marsh_anchor', 'guard_wheels'), reward=(Research('artillery', 0.5, 1),)),
    Focus('guard_engineers', 'Engineers for Ditches and Bridges',
          "Each formation's engineer company spends most of its time on parade. Retraining them for the real terrain, with "
          "pontoons, ditching machines and demolition kits, lets the guard cross the marsh streams and the drains of the "
          "plains, and deny them to anyone else. The engineers also start building culverts for the district roads, which "
          "the ministries gladly accept.",
          ('bridge', 'training'), after=('guard_mountain_manual',), reward=(Idea('crossing_drill'),)),
    Focus('guard_map_games', 'Map Games for the Plains',
          "The general staff runs a winter of map games on the plains: columns, depots, river lines and the long frontier, "
          "played out on tables in the capital. Officers from every formation take turns on both sides. The games expose "
          "supply gaps nobody wanted to see. The staff shares the lessons inside the guard and keeps the umpires' notes "
          "locked away.",
          ('command', 'document'), after_any=('guard_batteries', 'guard_engineers'),
          reward=(Research('logistics_tech', 0.5, 1), XP('army', 10))),
))

AIR = Branch('air', 'Twelve Fighters and One Apron', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_apron', 'Twelve on the Capital Field',
          "Romny's air arm is twelve fighters on the capital field with four more in reserve, all flown from a single runway "
          "beside the quay. It exists to guard the sky over a small country, and it can barely guard the capital. Counting "
          "pilots, mechanics, fuel and flying hours shows how thin it is before anyone decides what it is for.",
          ('air', 'runway'), reward=(Idea('one_field_wing'), Event('one_squadron'))),
    Focus('air_second_field', 'A Second Field at the Logistics Centre',
          "The logistics centre in District B already handles freight from the capital line, and its flat ground needs little "
          "preparation for a runway. A second field there, with fuel tanks and a dispersal apron, means a single accident or "
          "a single storm can no longer ground the whole air arm. The field also brings the fighters nearer the frontier.",
          ('runway', 'logistics'), after=('air_apron',), reward=(Build('air_base', 2, 536),)),
    Focus('air_coast_radar', 'Radar on the Capital Coast',
          "The air arm sees only what its pilots see. A radar post on the capital coast, linked by telephone to the field, "
          "gives the fighters minutes of warning instead of seconds. The equipment is foreign and its operators must be "
          "trained abroad. Once it works, the air arm can stop flying standing patrols that it cannot afford.",
          ('radar', 'navy'), after=('air_apron',), reward=(Build('radar_station', 1, 0),)),
    Focus('air_line_patrol', 'Patrols Along the Line',
          "One school wants the fighters flying regular patrols along the Yuktobanian and Kalugan frontiers, watching for "
          "strays, smugglers' aircraft and anything the radar misses. The patrols build airmanship and show the flag. They "
          "also burn fuel and airframes, and a fighter near a frontier is always one navigation error away from a diplomatic "
          "incident.",
          ('air', 'radar'), after_any=('air_second_field', 'air_coast_radar'), cost=10, exclusive=('air_capital_cover',),
          reward=(SwapIdea('one_field_wing', 'frontier_patrol'),)),
    Focus('air_capital_cover', 'Cover the Capital First',
          "The other school says twelve fighters cannot guard a long frontier and should not try. They should sit at "
          "readiness over the capital, the quay and the fuel silo, the targets that matter most, and fly only when the radar "
          "calls them. The pilots fly fewer hours. The outer districts learn that the air arm is not for them.",
          ('air', 'shelter'), after_any=('air_second_field', 'air_coast_radar'), cost=10, exclusive=('air_line_patrol',),
          reward=(SwapIdea('one_field_wing', 'capital_umbrella'),)),
    Focus('air_junction_radar', 'A Radar Mast at the Junction',
          "Patrols along the frontier need eyes on the ground ahead of them. A radar mast in District E, covering the corner "
          "where Romny meets Yuktobania and Kaluga, tells the patrols where to look. Its crew lives far from the capital in a "
          "district with no comforts, and the posting quickly becomes the least wanted in the air arm.",
          ('radar', 'gate'), after=('air_line_patrol',), reward=(Build('radar_station', 1, 561),)),
    Focus('air_longer_runway', 'Extend the Field Beside the Quay',
          "Keeping every fighter at readiness over the capital means the capital field must handle them all, plus transports "
          "and visitors. A longer runway, hardened shelters and a second taxiway let the field launch the whole squadron at "
          "once. The quay loses some warehouse ground to the extension, and the merchants who rented it lose their leases.",
          ('runway', 'shelter'), after=('air_capital_cover',), reward=(Build('air_base', 2, 0),)),
    Focus('air_mechanics', 'Mechanics on Long Contracts',
          "Romny trains good mechanics and then loses them to the freight companies and the truck works, which pay better. "
          "Long contracts with housing, a pension and a bonus for every year served keep crews at the field. The air arm's "
          "budget strains. Aircraft that fly when called are worth more than a squadron waiting for parts and people.",
          ('tools', 'air'), after=('air_apron',), reward=(Idea('ground_crews'),)),
    Focus('air_club_scholarships', 'Flying Club Scholarships',
          "The country has a handful of private flying clubs at the capital and the logistics centre. Scholarships that pay "
          "a club's fees in exchange for five years of reserve service give the air arm a pipeline of pilots who have "
          "already flown solo. Most club members are children of the notables, and the movement complains about privilege in "
          "the cockpit.",
          ('training', 'air'), after=('air_mechanics',), reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
))

FRONTIER = Branch('frontier', 'A Small Country on a Long Line', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('front_walk', 'Walk the Yuktobanian Frontier',
          "Three of Romny's districts face Yuktobania: District B, the marsh district and District E, where Kaluga also meets "
          "the line. No railway crosses the frontier, and most of it runs across open plain marked by posts and ditches. "
          "Officials who walk its length for the first time return with notes on crossings, farms split by the line and "
          "customs huts nobody staffs.",
          ('diplomacy', 'document'), reward=(Idea('frontier_desk'), Event('large_neighbour'))),
    Focus('front_customs_huts', 'Staff the Customs Huts',
          "The customs huts along the plain are staffed one day in three, if at all. Putting inspectors in every hut, with "
          "telephones and a ledger, ends the easy smuggling of tyres, spirits and fuel across the line. Smugglers move to "
          "the fields between the huts, and farm families who cross daily for work or kin now need passes to do it.",
          ('gate', 'document'), after=('front_walk',), reward=(Idea('customs_service'),)),
    Focus('front_good_neighbour', 'Good Neighbour Letters',
          "One school says Romny's safety lies in friendship with the giant next door: regular letters from Romny's frontier "
          "offices, a standing offer to talk, and trade terms that make Romny useful to Yuktobania. Markets may open and the "
          "frontier stays calm. Critics warn that a small country that leans too far toward one neighbour soon finds it "
          "cannot stand up straight.",
          ('diplomacy', 'peace'), after=('front_walk',), cost=10,
          exclusive=('front_many_customers', 'front_watch_posts'), reward=(SwapIdea('frontier_desk', 'good_neighbour'),)),
    Focus('front_many_customers', 'No Single Patron',
          "A second school would spread Romny's trade so thinly that no buyer matters too much. Rubber goes to one market, "
          "ore to another and trucks to a third, with the foreign ministry keeping a ledger of every customer's share. "
          "Contracts are smaller and harder to win. In return, Romny can refuse anyone without fearing for its budget.",
          ('economy', 'diplomacy'), after=('front_walk',), cost=10,
          exclusive=('front_good_neighbour', 'front_watch_posts'), reward=(SwapIdea('frontier_desk', 'many_customers'),)),
    Focus('front_watch_posts', 'A Watch Along the Posts',
          "The third school trusts neither friendship nor trade. It wants observation towers along the posts, guard patrols "
          "in the frontier districts and every crossing logged. Nothing about it is hostile, and the frontier staff insists "
          "so in writing. Neighbours will still read a line of towers as a message, and farmers will live with soldiers in "
          "their fields.",
          ('security', 'telescope'), after=('front_walk',), cost=10,
          exclusive=('front_good_neighbour', 'front_many_customers'), reward=(SwapIdea('frontier_desk', 'watchers'),)),
    Focus('front_junction_desk', 'A Liaison Desk at District E',
          "With a guard company now stationed near the junction, the foreign ministry adds a small liaison desk beside its "
          "barracks. Its officials answer every complaint from across the line within a day, whether about strayed cattle, "
          "a lost lorry or an aircraft heard at night. Romny proposes nothing and claims nothing there. It simply makes sure "
          "someone picks up the telephone.",
          ('communications', 'diplomacy'), after=('front_customs_huts',), requires=(HasFlag('junction_company'),),
          reward=(Idea('junction_liaison'),)),
    Focus('front_cinigrad_news', 'News from the Cinigrad Convention',
          "In September 1991 a political convention in Cinigrad hears Yuktobania unveil a new class of submarine. Romny "
          "keeps no navy and wants none, yet five of its six districts face the sea and its trade moves by coaster from the "
          "capital quay. Fishing skippers, lighthouse keepers and the harbour police form a coast watch that reports anything "
          "odd offshore.",
          ('submarine', 'fishing'), after=('front_walk',), requires=(After('1991.9.2'),),
          reward=(TimedIdea('coast_watch', 730),)),
    Focus('front_trade_fair', 'A Buyers Fair at the Logistics Centre',
          "Every autumn the logistics centre clears two sheds and invites buyers from any country to inspect trucks, tyres, "
          "ore and latex on the spot. Freight, lodging and a customs desk are provided free. The fair is cheap to run and "
          "loud to advertise. Whether it brings one large buyer or many small ones depends on which school the cabinet has "
          "chosen.",
          ('economy', 'logistics'), after_any=('front_good_neighbour', 'front_many_customers'),
          reward=(TimedIdea('trade_fair', 365),)),
    Focus('front_thaw_bonds', 'Borrow While the Powers Agree',
          "News arrives in October 1999 that Osea and Yuktobania will cooperate to convert the Arkbird into a platform "
          "clearing debris from satellite orbits. Romny has no part in it. The treasury's interest is narrower: lenders who "
          "once priced every Romny bond as frontier risk now quote longer terms. The cabinet borrows while the mood lasts "
          "and spends it on the districts.",
          ('economy', 'peace'), after_any=('front_good_neighbour', 'front_many_customers', 'front_watch_posts'),
          requires=(After('1999.10.8'),), reward=(Idea('thaw_credit'),)),
))

SKY = Branch('sky', 'Ulysses over Open Plain', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_bulletins', 'Bulletins on the Asteroid',
          "Late in 1994 word comes from the International Astronomical Union: the asteroid named Ulysses will pass near the "
          "Earth and may strike it. Romny owns no telescope able to follow it. Translating foreign bulletins and reading them "
          "on the national radio every week keeps rumour in check, and keeps the asteroid at every supper table, which some "
          "ministers think unwise.",
          ('meteor', 'communications'), requires=(After('1994.12.10'),), reward=(Idea('sky_watch'),)),
    Focus('sky_announcement', 'An Impact Without a Place',
          "In April 1996 the FCU President says publicly that Ulysses will hit the Earth and announces plans to counter it. "
          "Where the fragments come down is anyone's guess, and Romny cannot work it out alone. The cabinet must plan for an "
          "unplaced danger in a country of open plain with little natural cover, five coastal districts and a long, low "
          "shoreline.",
          ('meteor', 'document'), after=('sky_bulletins',), requires=(After('1996.4.20'),),
          reward=(Event('impact_announced'),)),
    Focus('sky_earth_shelters', 'Earth Shelters in Every Town',
          "A plain has no caves or cuttings to hide in, so the engineers propose to dig. Earth-covered shelters with timber "
          "roofs and concrete doors, one for every street in the capital and the district towns, would hold families for "
          "days. Digging them employs thousands and costs a fortune. Nobody knows whether they would stand up to what is "
          "coming.",
          ('shelter', 'civil'), after=('sky_announcement',), cost=10, exclusive=('sky_inland_dispersal',),
          reward=(SwapIdea('sky_watch', 'earth_shelters'),)),
    Focus('sky_inland_dispersal', 'Move the Coast to the Marsh',
          "The marsh district is the only part of Romny that does not touch the sea. Planners who distrust the coast in any "
          "disaster propose dispersal instead of shelters: trains and trucks to carry families from the coastal districts "
          "to reception camps around the marsh works. The plan costs far less, and depends on warning time, roads and fuel "
          "that may not exist.",
          ('refugees', 'rail'), after=('sky_announcement',), cost=10, exclusive=('sky_earth_shelters',),
          reward=(SwapIdea('sky_watch', 'marsh_dispersal'),)),
    Focus('sky_grain', 'Grain Pits for Two Seasons',
          "Whatever falls, harvests and imports may fail for a season or two. Lined grain pits in every district, filled "
          "from the state buying office at harvest price, would feed the country through a bad year. The pits take land and "
          "labour. Farmers grumble at the fixed price, and the movement accuses the Administration of hoarding grain for its "
          "friends.",
          ('economy', 'shelter'), after=('sky_announcement',), reward=(Idea('grain_pits'),)),
    Focus('sky_sirens', 'One Siren Code for Six Districts',
          "Each district sounds its sirens differently, and some have none. A single national code, with sirens on every "
          "works roof and a telephone tree from the capital radio, would tell every household the same thing at the same "
          "moment. Installing it is cheap. Teaching six districts to obey it, rather than climb on roofs to look, is the hard "
          "part.",
          ('communications', 'radar'), after=('sky_bulletins',), reward=(Idea('siren_code'),)),
    Focus('sky_reserve_wards', 'Reserve Wards in the School Halls',
          "The capital hospital has fewer beds than a single bad week would need. Reserve wards in school halls and works "
          "canteens, with stored beds, dressings and a roster of retired nurses, can open within a day of the sirens. "
          "Doctors call the plan improvised, which it is. It is still better than turning the injured away at the gate.",
          ('medical', 'civil'), after_any=('sky_earth_shelters', 'sky_inland_dispersal'), reward=(Idea('reserve_wards'),)),
    Focus('sky_roche_night', 'All Night by the Radio',
          "On 8 July 1999 Ulysses passes through Earth's Roche limit. In Romny the sirens are tested at dusk, the shelters "
          "or reception camps are opened, and the radio stays on all night with foreign bulletins read in turn. Nobody in "
          "the cabinet knows what the coming weeks hold for the country. They know only that every plan is being tested at "
          "once.",
          ('meteor', 'shelter'), after_any=('sky_earth_shelters', 'sky_inland_dispersal'), requires=(After('1999.7.8'),),
          reward=(Flag('sky_passed'), Stability(0.03))),
    Focus('sky_tally', 'Count the Cost of Preparing',
          "When the skies clear, the ministries count what the impact years cost Romny in money, harvests, shelters dug and "
          "trust spent. Whatever the fragments did elsewhere, every district has paid for preparation. A frank tally tells "
          "the next government which measures earned their price. It also shows which ones were bought to calm a frightened "
          "public, and the press will want both lists.",
          ('document', 'scales'), after=('sky_grain',), requires=(HasFlag('sky_passed'),),
          reward=(Research('construction_tech', 0.5, 1), Stability(0.02))),
))

DECADE = Branch('decade', 'The Turn of the Century Accounts', 2000, 'FOCUS_FILTER_RESEARCH', (
    Focus('dec_audit', 'Ten Years of Accounts',
          "A decade after the winter canvass, the treasury and the statistical office prepare one volume comparing Romny in "
          "1991 with Romny in 2000: roads, works, garrisons, harvests, debts and votes, if any were cast. It is the first "
          "full account of the country anyone has attempted. Every camp will quote it, and the government must first decide "
          "who sees it.",
          ('document', 'scales'), reward=(Idea('decade_accounts'), Event('decade_audit'))),
    Focus('dec_republic', 'A Second Charter Session',
          "The republic's charter promised a review session after ten years, and the chamber now holds it. Movement and "
          "non-party deputies arrive with amendments to the entrenched articles. Most fail, a few pass, and the court approves "
          "the method. The session proves the charter can change without breaking, and costs a season of legislative "
          "business and a great deal of patience.",
          ('assembly', 'scales'), after=('dec_audit',), requires=(HasFlag('rule_republic'),),
          exclusive=('dec_bench', 'dec_movement'), reward=(Idea('second_session'),)),
    Focus('dec_bench', 'The Bench Reports to the Districts',
          "After a decade in office, the bench of districts tours every district and reads its accounts aloud in public "
          "halls, answering questions from anyone who stands up. Movement members stand up often. The tour is exhausting and "
          "occasionally rough. It gives a government without elections something close to a mandate, renewed in person, one "
          "hall at a time.",
          ('assembly', 'logistics'), after=('dec_audit',), requires=(HasFlag('rule_bench'),),
          exclusive=('dec_republic', 'dec_movement'), reward=(Idea('bench_tour'),)),
    Focus('dec_movement', 'The Executive Reviews Its Decrees',
          "Ten years of rule by decree have left a shelf of orders that contradict each other. The movement executive appoints "
          "a commission to consolidate them into codes, and quietly drops the harshest. The halls call it softening; the "
          "ministries call it housekeeping. Lenders and neighbours read the new codes closely, and the non-party half of the "
          "country reads them most closely of all.",
          ('document', 'security'), after=('dec_audit',), requires=(HasFlag('rule_movement'),),
          exclusive=('dec_republic', 'dec_bench'), reward=(Idea('decree_codes'),)),
    Focus('dec_published', 'The Accounts in Weekly Instalments',
          "The district papers licensed under the press law each print the decade volume in weekly instalments, with a page "
          "for readers' letters. The letters are angry, specific and occasionally right. Ministries must answer the best of "
          "them in print. Officials hate the exercise. The public, for the first time, argues about Romny's choices from the "
          "same set of figures.",
          ('communications', 'document'), after=('dec_audit',), requires=(HasFlag('press_law'),),
          reward=(SwapIdea('decade_accounts', 'open_accounts'),)),
    Focus('dec_far_war', 'Freight Rates in a Far War',
          "In August 2003 the FCU demands that Erusea withdraw from San Salvacion and establishes the ISAF. The war on the "
          "Usean continent is far from Romny, but freight insurers raise their rates on every route toward Usean waters, and "
          "buyers there delay their payments. Covering the coasters' insurance costs the treasury money. Romny takes no side "
          "and says so plainly.",
          ('logistics', 'scales'), after=('dec_audit',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Idea('far_war_freight'),)),
    Focus('dec_district_e_works', 'A Works Hall for District E',
          "The last empty district to get a factory is District E, at the frontier junction. A works hall beside the junction "
          "road, building truck bodies and farm trailers, gives the district wages and the frontier corner a settled town "
          "around it. The site is exposed and the planners know it. Leaving District E empty for another decade would cost "
          "more.",
          ('industry', 'gate'), after=('dec_audit',), requires=(HasFlag('districts_settled'),),
          reward=(Build('industrial_complex', 1, 561),)),
    Focus('dec_second_programme', 'Draft the Second Programme',
          "With the century turned, the ministries draft a second national programme to run past 2005. It takes the decade "
          "volume, the district census and the works sheet and asks one question of every line: did it pay? The drafting "
          "committee includes every camp willing to sit, and the arguments are long. The programme that emerges is modest, "
          "costed and widely read.",
          ('document', 'industry'), after_any=('dec_republic', 'dec_bench', 'dec_movement', 'dec_published', 'dec_far_war',
                                               'dec_district_e_works'),
          requires=(After('2003.1.1'),), reward=(Idea('second_programme'),)),
))

BRANCHES = (POLITICS, DISTRICTS, WORKS, GROUND, GUARD, AIR, FRONTIER, SKY, DECADE)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('district_road_season', 'A Dry Season of Road Gangs',
                'Send the road gangs back to the rail-corner district for one dry season; adds a road level there once.',
                50, (Build('infrastructure', 1, 549), Stability(0.01)), requires=(Completed('dist_rail_corner'),)),
    DecisionDef('latex_auction', 'Hold the Latex Auction at the Quay',
                'Auction the season of latex at the capital quay in open bidding; it can be held once a year.',
                30, (TimedIdea('auction_season', 120),), requires=(Completed('res_groves'),), cooldown=365),
    DecisionDef('plains_manoeuvres', 'Call Autumn Manoeuvres on the Plains',
                'Exercise both garrisons across the open districts with the engineers and the reserve rolls; it can be repeated each year.',
                40, (XP('army', 15), WarSupport(0.01)), requires=(Completed('guard_district_rolls'),), cooldown=365),
    DecisionDef('crossing_sweep', 'Order a Night Sweep of the Crossings',
                'Put inspectors and guard patrols on every frontier crossing for a week of nights; it can be repeated each half year.',
                25, (TimedIdea('crossing_sweep', 90),), requires=(Completed('front_customs_huts'),), cooldown=180),
    DecisionDef('siren_test', 'Sound the Noon Siren Test',
                'Test every siren and telephone tree in the six districts at the same minute; it can be repeated within the year.',
                15, (Stability(0.02),), requires=(Completed('sky_sirens'),), cooldown=300),
    DecisionDef('canvass_again', 'Send the Canvassers Out Again',
                'Repeat the winter canvass now that the district lists are public, to see how the camps have moved; once only.',
                30, (PP(20), Stability(0.01)), requires=(Completed('pol_canvass'), HasFlag('lists_published'))),
)
