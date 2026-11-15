"""Dakrain (DAK): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (democratic ruling party at 48 percent
with communism at 32, a last election dated 1 January 1991 and elections not allowed, stability
0.8 and war support 0.5), the inherited presidential character, the country names, the two 1991
states and their place names, the claims recorded in the state histories, the world-start
profile, and the Perbla and Arklith specs, whose Dakrain commissions this tree mirrors and never
contradicts. Official: a handful of ACES Chronicle rows used only as date anchors for regional
pressure. Everything else, including every Dakrainian choice, office, idea, building and event,
is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='DAK', name='Dakrain', root='world', package='dak',
                  themes=('air', 'tools', 'scales'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Dakrain state: ruling party democratic with popularities democratic 48, communism 32, monarchism 10, '
           'neutrality 10 and fascism 0; last_election 1991.1.1, election_frequency 48 and elections_allowed = no; stability '
           '0.8 and war support 0.5; three research slots; tech_mountaineers, infantry_at and infantry_manpats; country names '
           'Republic of Dakrain (democratic and neutrality), Dakrainian SSR, Dakrainian State and Principality of Dakrain. '
           'The tree never removes or edits these.',
           'mod/2985041246/history/countries/DAK - Dakrain.txt; mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Inherited leader DAK_malis_tacal, a country_leader with ideology conservatism whose name field carries a presidential '
           'title with a marshal rank. The tree neither names nor removes the character; every new government is an unnamed '
           'collective office reached through a Regime focus.',
           'mod/2985041246/common/characters/DAK.txt; tools/world_foundation/country_registry.json (DAK leader_representation)'),
    Source('Mod provenance',
           'Geography: 1991 states 114 Trent (city; victory point Oderin with naval base 2; two arms factories, two industrial '
           'complexes, one dockyard, infrastructure 3, one air base) and 234 Brunies (capital; large city; victory points West '
           'Trent and Bell Town, naval base 5 at Bell Town; steel 16 and tungsten 9; three arms factories, two industrial '
           'complexes, one dockyard, a fuel silo, infrastructure 4, five air bases). Claims: PBL and TER claim 114 and 234; DAK '
           'claims 209 North Dakrain (victory point Karluga) and 571 Terentio Desert, both owned by PBL with TER cores. Land '
           'neighbours PBL (via 209 and 571), ARK (via 252 Eastern Nieblo) and LEA (via 70), computed from map/provinces.bmp; '
           'both states are coastal plains with urban centres. Warm, wet weather with heavy rain and mud from strategic region '
           '39. The supply-hub captions in ac_world_start_hubs are placeholders and are never used as place names.',
           'mod/2985041246/history/states/114-State_114.txt, 234-State_234.txt, 209-State_209.txt, 571-State_571.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; '
           'mod/2985041246/map/strategicregions/39-Dakrain.txt; mod/2985041246/map/definition.csv'),
    Source('Mod provenance',
           'World start: role small coastal and air defense; 4 civilian, 5 military and 2 dockyards; four infantry formations, '
           '24 fighters, one destroyer and 60 convoys; DAK Service Fighter and DAK Coastal Escort variants; stocks of 960 '
           'infantry, 720 motorized, 24 train and 192 support equipment; research priority Physical Sustainment (transport, '
           'equipment replacement and affordable service capacity).',
           'tools/world_starts/profiles.json (DAK); docs/WORLD_STARTS_CALIBRATION.md; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml (DAK_ws_research_name)'),
    Source('Mod provenance',
           'Neighbour consistency: the Perbla tree acknowledges the Dakrain dispute over the Terentio frontier with a joint '
           'commission on crossings, wells and customs and no border effect (PBL_wd_lands_dakrain_commission); the Arklith tree '
           'holds a valley commission and seasonal markets at the Dakrain crossings (ARK_wd_fro_dakrain_valley, '
           'ARK_wd_fro_valley_markets). Perbla holds historical_friends ties to Belka. This tree opens matching Dakrainian desks '
           'and never assumes which neighbour focuses were taken or what Perbla does in the Belkan War.',
           'tools/world_depth/pbl/content.py; tools/world_depth/ark/content.py; mod/2985041246/common/on_actions/ac_on_actions.txt'),
    Source('Mod provenance',
           'Campaign hooks read only outcomes the mod already records: belka_won_belkan_war and belka_lost_belkan_war, set by '
           'the Belkan War events, and ac_ucw_war_started, set by the Usean Continental War effects. Each is a separate gameplay '
           'branch; none is asserted as history.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Official', 'Date anchor only: the IAU warns that the asteroid Ulysses may strike the Earth.', '1994 / 12.10'),
    Source('Official', 'Date anchor only: the Belkan War breaks out. No Dakrainian role is claimed.', '1995 / 03.25'),
    Source('Official', 'Date anchor only: the FCU announces that Ulysses will strike the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor only: former Belkan Air Force pilots are hired abroad as aggressor squadrons. No '
           'Dakrainian contract is claimed.', '1998 / 06.19'),
    Source('Official', 'Date anchor only: Ulysses passes through the Roche limit. No fragment fall in Dakrain is claimed.',
           '1999 / 07.08'),
    Source('Official', 'Date anchor only: the FCU establishes the ISAF and the Usean Continental War follows. No Dakrainian '
           'role is claimed.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Dakrainian focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; '
           'offices are collective and unnamed; claims stay claims, with no border, core, war, annexation or faction effects; '
           'no new place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the suspended ballot
    IdeaDef('ballot_suspended', 'The Suspended Ballot', 'No ballot stands on the calendar; the terms of the suspension are '
            'published and contested.', {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('ballot', 'document')),
    IdeaDef('round_table', 'The Round Table', 'The left bloc holds a fixed seat to argue wages, rents and the ballot.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'diplomacy')),
    IdeaDef('princely_patrons', 'Princely Patrons', 'Mill and estate families of the princely party back the presidency.',
            {'political_power_gain': 0.10}, ('medal', 'economy')),
    IdeaDef('garrison_inquiry', 'The Garrison Inquiry', 'Garrison commanders have told an inquiry what they expect of government.',
            {'army_org_factor': 0.03, 'political_power_gain': -0.05}, ('command', 'document')),
    IdeaDef('republic_mandate', 'The Reopened Polls', 'Ministers answer to an elected chamber and the presidency is one office '
            'among several.', {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'civil')),
    IdeaDef('guardianship', 'Presidential Guardianship', 'A council of state governs on a published programme while the ballot '
            'stays suspended.', {'political_power_gain': 0.20, 'stability_factor': -0.03}, ('command', 'ballot')),
    IdeaDef('councils_mandate', 'The Councils Mandate', 'Elected works councils send delegates to a federal committee.',
            {'stability_factor': 0.04, 'production_factory_efficiency_gain_factor': 0.04, 'political_power_gain': -0.05},
            ('industry', 'assembly')),
    IdeaDef('marshals_order', 'Order of the Marshals', 'Senior commanders hold the seals, the treasury and the frontier.',
            {'war_support_factor': 0.06, 'army_org_factor': 0.04, 'stability_factor': 0.03}, ('security', 'command')),
    IdeaDef('chamber_hearings', 'Budget Hearings', 'Every figure in the budget is defended on the record.',
            {'political_power_factor': 0.05, 'production_speed_buildings_factor': -0.03}, ('scales', 'ballot')),
    IdeaDef('decree_terms', 'Decrees with Expiry Dates', 'Every decree lapses unless the advisory chamber reviews it.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('document', 'command')),
    IdeaDef('mill_councils', 'Councils in the Mills', 'Every large workplace elects a council with a say over shifts and safety.',
            {'production_factory_efficiency_gain_factor': 0.06, 'stability_factor': 0.02}, ('industry', 'ballot')),
    IdeaDef('republic_constitution', 'Constitution of the Republic', 'One written constitution; no ballot can be suspended by '
            'decree.', {'stability_factor': 0.08, 'political_power_factor': 0.08, 'research_speed_factor': 0.02},
            ('scales', 'ballot')),
    IdeaDef('council_statute', 'Statute of the Council of State', 'The presidency governs by written statute rather than habit.',
            {'political_power_gain': 0.25, 'war_support_factor': 0.04}, ('command', 'document')),
    IdeaDef('council_federation', 'Charter of the Councils', 'Council practice is written into a federal charter.',
            {'stability_factor': 0.06, 'production_factory_efficiency_gain_factor': 0.06, 'consumer_goods_factor': -0.03},
            ('assembly', 'document')),
    IdeaDef('marshals_code', 'The Public Order Code', 'The directorate rules by a published code with a right of appeal.',
            {'stability_factor': 0.08, 'war_support_factor': 0.08, 'army_org_factor': 0.05}, ('security', 'document')),
    IdeaDef('wage_accord', 'The Spring Wage Accord', 'Unions, owners and the ministry fix mill wages together each spring.',
            {'stability_factor': 0.05, 'production_factory_max_efficiency_factor': 0.04}, ('economy', 'assembly')),
    # claims and crossings
    IdeaDef('claims_office', 'The Claims Office', 'Every treaty, survey and complaint about the frontier sits in one archive.',
            {'political_power_gain': 0.05, 'war_support_factor': 0.03}, ('scales', 'document')),
    IdeaDef('kin_desk', 'The Family Visits Desk', 'A consular desk handles family visits, pensions and papers across the line.',
            {'stability_factor': 0.03}, ('refugees', 'civil')),
    IdeaDef('nieblo_passes', 'Grazing Passes', 'Seasonal grazing passes and posted crossing hours toward Eastern Nieblo.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('peace', 'logistics')),
    IdeaDef('claim_in_law', 'A Claim in Statute', 'The claims on North Dakrain and the Terentio Desert are written into law.',
            {'war_support_factor': 0.06, 'army_core_defence_factor': 0.05, 'stability_factor': -0.02}, ('scales', 'security')),
    IdeaDef('quiet_claim', 'A Quiet Claim', 'The claims stay on record and off the agenda.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.03}, ('peace', 'document')),
    IdeaDef('frontier_guard', 'The Desert Line Guard', 'One guard for the line facing North Dakrain and the Terentio Desert.',
            {'army_core_defence_factor': 0.08, 'experience_gain_army_factor': 0.05}, ('security', 'training')),
    IdeaDef('wells_commission', 'The Wells Commission', 'A standing desk for wells, customs hours, herds and truck permits.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.08}, ('peace', 'tools')),
    IdeaDef('crossing_markets', 'Licensed Market Days', 'Market days under inspection at the main crossings.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('economy', 'peace')),
    IdeaDef('claim_rally', 'The Claim White Paper', 'Rallies in Brunies on the tenth year of the claim statute.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.05}, ('medal', 'scales')),
    IdeaDef('quiet_crossings', 'Routine Crossings', 'A decade of quiet crossings toward Perbla.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.02}, ('peace', 'economy')),
    IdeaDef('crossing_fair', 'The Crossing Fair', 'A licensed fair at the frontier for one season.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('economy', 'diplomacy')),
    # steel and tungsten
    IdeaDef('mill_survey', 'The Furnace Count', 'Every mill, shaft and arms hall in Brunies has been counted.',
            {'production_factory_efficiency_gain_factor': 0.03}, ('industry', 'document')),
    IdeaDef('steel_combine', 'The Brunies Steel Combine', 'One state combine with one order book and one wage scale.',
            {'production_speed_arms_factory_factor': 0.08, 'political_power_gain': 0.05}, ('command', 'industry')),
    IdeaDef('mill_shares', 'Mill Shares', 'The mills sell shares at home and abroad under disclosure rules.',
            {'production_factory_max_efficiency_factor': 0.04, 'production_speed_industrial_complex_factor': 0.08},
            ('economy', 'scales')),
    IdeaDef('tungsten_tooling', 'Tungsten Tooling', 'Cutting tools and dies made from Brunies tungsten.',
            {'production_factory_efficiency_gain_factor': 0.05, 'research_speed_factor': 0.02}, ('tools', 'industry')),
    IdeaDef('mine_safety', 'Shaft Rescue Stations', 'Rescue crews and breathing sets at every working shaft.',
            {'stability_factor': 0.04}, ('medical', 'tools')),
    IdeaDef('ore_contracts', 'Tungsten Abroad', 'Multi-year contracts for a share of Brunies tungsten.',
            {'political_power_gain': 0.10, 'industrial_capacity_factory': 0.04}, ('economy', 'diplomacy')),
    IdeaDef('tungsten_auction', 'A Tungsten Lot Sold', 'Proceeds from a single tungsten auction.',
            {'political_power_gain': 0.15}, ('economy', 'tools')),
    # harbours
    IdeaDef('harbour_board', 'The Joint Harbour Board', 'One board sets dues and plans works for Bell Town and Oderin.',
            {'production_speed_infrastructure_factor': 0.08, 'naval_coordination': 0.03}, ('navy', 'scales')),
    IdeaDef('free_port', 'The Bell Town Free Port', 'A bonded zone for storing and re-exporting foreign goods.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': 0.05}, ('economy', 'logistics')),
    IdeaDef('naval_harbour', 'Bell Town Naval Harbour', 'The best berths are reserved for the navy and the hulls it expects.',
            {'navy_org_factor': 0.06, 'repair_speed_factor': 0.08}, ('navy', 'security')),
    IdeaDef('escort_rota', 'The Escort Rota', 'One hull on patrol, one in training and one in refit.',
            {'navy_org_factor': 0.05, 'naval_speed_factor': 0.04}, ('navy', 'training')),
    IdeaDef('convoy_pool', 'The Hull Pool', 'Merchant owners share bookings, crews and repair slots.',
            {'industrial_capacity_dockyard': 0.05, 'consumer_goods_factor': -0.02}, ('logistics', 'navy')),
    IdeaDef('repair_berths', 'Repair Berths', 'Bell Town repairs passing ships with its own crane and parts store.',
            {'repair_speed_factor': 0.10, 'industrial_capacity_dockyard': 0.05}, ('tools', 'navy')),
    IdeaDef('fishing_coops', 'Fishing Cooperatives', 'Oderin crews sell their own catch through a cooperative hall.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('fishing', 'civil')),
    # the air wing
    IdeaDef('service_wing', 'The Service Fighter Wing', 'Two dozen Service Fighters and a plan to keep them flying.',
            {'experience_gain_air_factor': 0.05, 'air_superiority_efficiency': 0.03}, ('air', 'document')),
    IdeaDef('interceptor_net', 'The Interceptor Net', 'Every fighter tied to the radar chain over the ports.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.08}, ('air', 'radar')),
    IdeaDef('dispersed_fields', 'Dispersed Fields', 'The wing spread across strips and road sections in the plain.',
            {'air_mission_efficiency': 0.05, 'repair_speed_factor': 0.08, 'air_defence_factor': 0.05}, ('runway', 'security')),
    IdeaDef('contract_instructors', 'Contract Instructors', 'Hired instructors fly as aggressors against the wing.',
            {'experience_gain_air_factor': 0.12, 'stability_factor': -0.02}, ('training', 'air')),
    IdeaDef('home_school', 'The National Flying School', 'The best pilots of the wing teach the rest.',
            {'experience_gain_air_factor': 0.06, 'training_time_factor': -0.05}, ('training', 'medal')),
    # sustainment
    IdeaDef('sustainment_first', 'Sustainment First', 'Transport, spares and replacements before new units.',
            {'supply_consumption_factor': -0.05, 'repair_speed_factor': 0.05}, ('logistics', 'document')),
    IdeaDef('rain_manoeuvres', 'Manoeuvres in the Rains', 'Exercises held in the wet season, mud and all.',
            {'attrition': -0.05, 'army_speed_factor': 0.03}, ('training', 'logistics')),
    IdeaDef('conscript_levy', 'The Universal Year', 'A year of service for every fit young adult, then reserve duty.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.05}, ('training', 'security')),
    IdeaDef('volunteer_core', 'The Volunteer Core', 'Fewer soldiers on proper pay who stay longer.',
            {'army_org_factor': 0.06, 'experience_gain_army_factor': 0.08}, ('medal', 'training')),
    IdeaDef('replacement_depots', 'Replacement Depots', 'Stocked depots behind the Trent front rotate men and equipment.',
            {'supply_consumption_factor': -0.08, 'army_org_factor': 0.03}, ('logistics', 'tools')),
    IdeaDef('muster_drills', 'District Musters', 'Reservists muster by district once a year.',
            {'army_core_defence_factor': 0.05, 'training_time_army_factor': -0.05}, ('document', 'security')),
    IdeaDef('sergeant_school', 'The Sergeants School', 'Long-service sergeants trained in Brunies.',
            {'army_org_factor': 0.04, 'experience_gain_army_factor': 0.10}, ('medal', 'command')),
    IdeaDef('antitank_teams', 'Tungsten Anti-Tank Teams', 'Infantry teams train with home-made penetrator rounds.',
            {'army_defence_factor': 0.05, 'army_core_defence_factor': 0.05}, ('missile', 'tools')),
    # the northern war
    IdeaDef('war_desk', 'The War Desk', 'A desk in Brunies follows the northern war and the neighbours.',
            {'war_support_factor': 0.03, 'political_power_gain': 0.05}, ('communications', 'command')),
    IdeaDef('strict_neutrality', 'Strict Neutrality', 'No arms, fuel or port services for any belligerent.',
            {'stability_factor': 0.04, 'army_core_defence_factor': 0.05}, ('peace', 'scales')),
    IdeaDef('osean_freight', 'Quays Open to Osean Freight', 'Osean lines bunker and repair at Bell Town.',
            {'consumer_goods_factor': -0.03, 'industrial_capacity_dockyard': 0.04}, ('diplomacy', 'logistics')),
    IdeaDef('contraband_searches', 'Contraband Searches', 'Cargoes bound for the war zone are searched at the quays.',
            {'stability_factor': 0.02, 'naval_coordination': 0.03}, ('security', 'navy')),
    IdeaDef('perbla_watch', 'Eyes on the Perblan Line', 'Frontier companies on high alert facing North Dakrain.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.04}, ('security', 'radar')),
    IdeaDef('price_boards', 'Price Boards', 'Posted maximum prices for bread, cooking fuel and kerosene.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.03}, ('economy', 'civil')),
    IdeaDef('postwar_orders', 'Postwar Orders', 'Rebuilding abroad fills the Brunies order books.',
            {'production_speed_arms_factory_factor': 0.08, 'industrial_capacity_factory': 0.04}, ('industry', 'diplomacy')),
    IdeaDef('northern_shadow', 'The Northern Shadow', 'A victorious Belka and a Perbla that counts it a friend.',
            {'war_support_factor': 0.06, 'army_core_defence_factor': 0.06, 'consumer_goods_factor': 0.02}, ('security', 'command')),
    # Ulysses
    IdeaDef('sky_desk', 'The Ulysses Desk', 'The civil defence office plans for a threat without an address.',
            {'stability_factor': 0.02, 'research_speed_factor': 0.02}, ('meteor', 'document')),
    IdeaDef('storm_drains', 'Cleared Storm Drains', 'Bell Town and Oderin drain their streets in heavy rain.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.05}, ('civil', 'tools')),
    IdeaDef('mill_shelters', 'Shelters Under the Mills', 'Reinforced mill basements stocked for weeks.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.03}, ('shelter', 'industry')),
    IdeaDef('evacuation_timetables', 'Evacuation Timetables', 'Every district has a train and a reception village.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'refugees')),
    IdeaDef('evacuation_berths', 'Evacuation Berths', 'Berths at Bell Town held for evacuation ships.',
            {'stability_factor': 0.03, 'naval_coordination': 0.03}, ('navy', 'refugees')),
    IdeaDef('relief_stocks', 'Relief Stocks', 'Grain, cooking fuel and medicine for three lean months.',
            {'stability_factor': 0.05}, ('economy', 'shelter')),
    IdeaDef('relief_office', 'The Relief Office', 'A permanent civil defence secretariat in Brunies.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('refugees', 'medical')),
    # the turn of the century
    IdeaDef('usean_charters', 'Charters for Peaceful Cargo', 'Grain, medicine and machinery carried under strict rules.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('logistics', 'economy')),
    IdeaDef('home_routes', 'Hulls Kept Close to Home', 'Dakrainian hulls keep far from the fighting.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('navy', 'peace')),
    IdeaDef('defence_review', 'The Century Defence Review', 'Doctrine rewritten from a distant war and a decade of mud.',
            {'planning_speed': 0.10, 'army_defence_factor': 0.04}, ('command', 'scales')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('republic_cabinet', 'Cabinet of the Restored Republic',
           'A cabinet formed by the majority of a freely elected chamber, governing collectively, with the presidency reduced '
           'to a fixed-term office of state. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('presidential_council', 'Council of State of the Presidency',
           'A council of state named by the presidency, governing on a published programme while the ballot stays suspended and '
           'the chamber sits as an advisory body. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism'),
    Office('workers_federation', 'Federal Committee of the Works Councils',
           'A committee elected by delegates of the mill, dock and depot councils, holding the ministries in place of the '
           'presidency. Provisional gameplay office with no named holder.',
           'communism', 'democratic_socialism'),
    Office('marshals_directorate', 'Directorate of Marshals',
           'A directorate of senior commanders holding the seals, the treasury and the frontier, with the parties kept as '
           'advisory bodies. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('ballot_question', 'The Ballot in the Drawer', (
        "The decree is short and the reaction is long. Dakrain voted on the first day of 1991, the democratic parties took "
        "nearly half the count and the left bloc close to a third, and no further ballot now stands on the calendar. The "
        "presidency, held by an officer with a marshal's rank, governs a stable country with a conservative cabinet, and it has "
        "published the terms on which the suspension rests.",
        "Publishing them has brought every camp into the open. Liberal deputies and the port newspapers want the polling "
        "stations reopened within the year. The conservative majority prefers a council of state with a programme and no "
        "campaign. The left bloc, strong in the Brunies mills and on the Bell Town docks, speaks of councils instead of "
        "ministries. A circle of senior commanders says little in public and a great deal in the officers' mess.",
        "Nothing is settled today. What the presidency decides now is how the argument will be held: in the chamber and the "
        "press, where every faction can be heard and every promise is recorded, or inside the ministries and barracks of "
        "Brunies, where decisions come faster and grudges last longer. Whichever way it goes, the camp left outside will "
        "remember who closed the door.",
    ), (
        Option('Publish the hearings in full.', (Stability(0.02), PP(-15))),
        Option('Keep the hearings behind closed doors.', (PP(35), Stability(-0.02))),
        Option('Ask the garrisons for their view first.', (XP('army', 15), WarSupport(0.02), PP(-5))),
    ), citation='history/countries/DAK - Dakrain.txt set_politics and set_popularities; every response is gameplay',
        picture=2),
    EventDef('claims_map', 'Lines Drawn by Others', (
        "The claims office opens in Brunies with three filing cabinets and a problem of definitions. Dakrainian schoolbooks "
        "show North Dakrain, the province around Karluga, and the Terentio Desert as Dakrainian land held by Perbla. The claims "
        "recorded for Perbla mark Trent and Brunies as Perblan, and the claims recorded for Terentio mark them too. Every party "
        "has paperwork. Nobody is moving any posts.",
        "The frontier itself is less grand than the maps. Herders cross with their flocks, water trucks run between wells "
        "that ignore the line, and smugglers carry fuel and cigarettes in both directions. Families in Trent have cousins in "
        "Karluga. The frontier police arrest some travellers and wave through others, depending on the day, the officer and the "
        "size of the gift.",
        "Before any policy is written, the office must decide what it is for. It can serve as an archive and a diplomatic "
        "desk, keeping the claim alive on paper and the crossings calm. Or it can become the voice of the claim, with maps for "
        "every classroom and statements for every anniversary. The first course reassures Gatewood. The second reassures the "
        "officers in Brunies.",
    ), (
        Option('Make it an archive and a desk.', (Stability(0.02), PP(-10))),
        Option('Make it the voice of the claim.', (WarSupport(0.03), PP(20))),
    ), citation='state histories 114, 234, 209 and 571 (add_claim_by); no border, core or war effect', picture=2),
    EventDef('furnace_count', 'The Furnace Count', (
        "The inspectors come back from Brunies with a report thicker than any budget. The province holds all of "
        "Dakrain's steel and tungsten, two civilian works, three arms halls and the mills that feed them. Some furnaces run "
        "around the clock on modern controls. Others are older than the men who tend them and survive because nobody has dared "
        "to close them.",
        "The tungsten shafts are worse. Their maps are old, their ventilation fails in the hot months and their escape "
        "galleries flood after heavy rain. Wages are decent by Dakrainian standards and the unions are strong, which is why "
        "the shafts still work at all. The owners say any improvement must be paid by the state. The unions answer that the "
        "state has been saying the same thing for years.",
        "The report offers two broad directions: fold the mills into a single state combine with one order book, or open them "
        "to investors and let capital find the best furnaces. Before either can be argued, the ministry must decide who reads "
        "the report first: the owners, who will dispute every figure, or the unions, who will quote every figure back at "
        "them.",
    ), (
        Option('Give it to the owners first.', (PP(25), Research('industry', 0.3, 1))),
        Option('Give it to the unions first.', (Stability(0.02), PP(-10))),
    ), picture=1),
    EventDef('two_harbours', 'Two Harbour Councils', (
        "Bell Town and Oderin have been rivals for longer than either has had a proper breakwater. Bell Town is the deeper "
        "port, close to the capital province, its quays shared by freighters and the navy's lone escort. Oderin, on the "
        "Trent coast, is busier and shallower, crowded with coasters, fishing boats and the small repair yards that serve "
        "them.",
        "Each port council has a plan, and each plan requires the other port to wait. Bell Town wants its channel dredged and "
        "its quays lengthened for larger ships. Oderin wants a slipway and a cold store. Both want the shipping lines and both "
        "accuse the other of stealing them with lower dues. The ministry has funded a little of everything, and neither port "
        "is satisfied.",
        "A joint harbour board would set dues and plan works for both, but only if both councils accept equal seats and a "
        "chair named in Brunies. The ministry must decide how to bring them to the table: with money for each port's first "
        "project, or with a deadline after which the board is formed whether the councils like it or not.",
    ), (
        Option('Bring them in with money.', (PP(-20), Stability(0.03))),
        Option('Set a deadline.', (PP(25), XP('navy', 10))),
    ), picture=0),
    EventDef('wing_review', 'The Wing on Parade', (
        "The air staff's review begins with a parade and ends with a list. Twenty-four Service Fighters fly past the Brunies "
        "fields in good order, a credit to their crews. Behind the hangars the list tells the rest: engines past their overhaul "
        "dates, radios cannibalised to keep others working, and a dozen pilots who have not flown a night sortie in a year.",
        "The wing is all the air defence Dakrain has. Two port cities, an inland capital province and a frontier facing a "
        "larger neighbour depend on it, and the army asks for support the wing cannot give. The navy asks for patrols over the "
        "coast. The frontier companies want reconnaissance. Every request is reasonable. Granted together, they would ground "
        "the wing within a season.",
        "The staff offers two broad doctrines for the coming years: concentrate on interception over the ports, tied to radar, "
        "or disperse the wing across the plain so that it survives a first blow. Before choosing, the government must decide "
        "whether to publish the review, inviting public pressure for funds, or to keep it within the staff and the ministry.",
    ), (
        Option('Publish the review.', (WarSupport(0.02), PP(-10))),
        Option('Keep it within the staff.', (XP('air', 15), PP(10))),
    ), picture=0),
    EventDef('wet_season_trial', 'Columns in the Mud', (
        "The general staff's count of trucks, rifles and trains is barely finished when the first exercise of the year sends "
        "two infantry formations across the plain behind Trent in the wet season. The plan expects them at the frontier road "
        "in two days. They arrive in five, after leaving a trail of bogged trucks, flooded field kitchens and radios drowned in "
        "their crates.",
        "The umpires' report is blunt. The army was organised for dry ground and fine weather, and its supply columns depend "
        "on two roads that turn to rivers in heavy rain. The reserve stocks counted in the depots are real, but nobody can move "
        "them quickly. Replacement crews for broken trucks exist only on paper. The officers who planned the exercise expect to "
        "be blamed.",
        "The staff can treat the result as a scandal, removing the planners and promising reform, or as a lesson, keeping the "
        "officers and sending them back into the mud with orders to try again. A scandal would satisfy the press and the "
        "chamber. A lesson would keep experienced men in post who now know exactly what failed and why.",
    ), (
        Option('Treat it as a scandal.', (PP(20), Stability(-0.01))),
        Option('Treat it as a lesson.', (XP('army', 20), PP(-10))),
    ), picture=1),
    EventDef('northern_war', 'War Beyond the Northern Horizon', (
        "Word of war reaches Brunies by radio before dawn. Belka has gone to war far to the north, and by midday the shipping "
        "agents at Bell Town are quoting new insurance rates. Dakrain has no part in the quarrel and no treaty that would draw "
        "it in. Its concern is closer to home: Perbla, across the frontier, counts Belka among its oldest friends.",
        "The war desk assembles what it can. Northern routes will be dangerous for months; fuel and grain prices will rise; "
        "some lines will look for neutral harbours to bunker and repair. The frontier companies facing North Dakrain report no "
        "change across the line, so far. Perbla's government has said nothing in public. Its newspapers have said a great "
        "deal.",
        "The presidency must decide how Dakrain speaks in the first days. A firm statement of neutrality, repeated in every "
        "capital, would reassure Gatewood and the shipping lines. A quieter course, saying little and watching closely, keeps "
        "every option open but leaves the neighbours to guess. Either way, the frontier companies will be told to keep their "
        "eyes open and their reports short.",
    ), (
        Option('Declare neutrality in every capital.', (Stability(0.02), Event('perbla_mood', 21))),
        Option('Say little and watch.', (WarSupport(0.03), Event('perbla_mood', 14))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Dakrainian response is '
                'gameplay', picture=0),
    EventDef('perbla_mood', 'Gatewood Answers', (
        "Some weeks into the war, the frontier desk receives a note from Perbla, handed over by a junior official at a crossing "
        "near the Terentio Desert as if it were a customs form. It commits to nothing. It speaks of friendship with Belka, of "
        "respect for neighbours and of Perbla's own frontiers, and it says nothing at all about what Perbla will do.",
        "In Brunies the note is read three ways. The officers read a warning and ask for the frontier companies to stay on "
        "alert until the war ends. The traders read reassurance and ask for the crossings to stay open. The claims office "
        "reads an opening to remind Gatewood that Dakrain has a long memory too, and is told firmly that this is not the "
        "season.",
        "The government must choose how to answer. A courteous reply, confirming Dakrain's neutrality and proposing that "
        "frontier officials keep talking, would calm the crossings. A cooler reply, acknowledging the note and nothing more, "
        "would signal that Dakrain will watch its frontier however friendly the words. Both answers will be read closely in "
        "Gatewood, and both will be remembered.",
    ), (
        Option('Reply with courtesy.', (Stability(0.02), PP(-10))),
        Option('Reply coolly and keep watching.', (WarSupport(0.02), XP('army', 15))),
    ), citation='mod/2985041246/common/on_actions/ac_on_actions.txt (PBL historical_friends with BLK); no Perblan decision is '
                'asserted', picture=2),
    EventDef('ulysses_date', 'A Date for the Asteroid', (
        "The December 1994 warning was a matter for astronomers and newspaper columnists. The April 1996 announcement is a "
        "matter for every government. The asteroid called Ulysses will strike the Earth, and nobody can say where its "
        "fragments will fall. In Brunies the civil defence office, until now a single floor of clerks and fire inspectors, is "
        "told to plan for it.",
        "Its planners face a threat with no address. Most Dakrainians live in West Trent, Bell Town and Oderin, on a low "
        "plain with no hills to hide behind and rivers that flood in the wet season. The mills have deep basements, the "
        "railways reach every district and the ports have ships. None of these was built with a falling sky in mind, and "
        "none of them is cheap to adapt.",
        "Two schools form quickly. One wants shelters, dug into the mill basements and city cellars and stocked for weeks. "
        "The other wants timetables, trains and reception villages to empty the cities when a warning comes. Before choosing, "
        "the government must decide how to speak to the public: frankly, with the full uncertainty, or reassuringly, with "
        "plans before details.",
    ), (
        Option('Speak frankly.', (WarSupport(0.02), Stability(-0.02))),
        Option('Reassure first.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; the '
                'Dakrainian response is gameplay', picture=2),
    EventDef('roche_night', 'The Night of the Fragments', (
        "On the night the asteroid crosses the Roche limit, every siren in Dakrain is tested at dusk and then falls silent. "
        "The shelters and stations are staffed, the sky watch reports every hour, and the radio carries nothing but bulletins. "
        "In the port cities people stand on rooftops to watch the sky. In the mill districts many go below without being "
        "told.",
        "The bulletins carry news from abroad rather than from home: reports of fragments and fires in distant places, each "
        "one checked against the next before it is read aloud. The civil defence office keeps its own counsel and its own "
        "lists. Whatever falls on Dakrain, if anything does, the plans written since 1996 will meet it with what they have.",
        "By morning the government must decide what comes next. It can keep the country on alert for weeks, shelters manned "
        "and trains ready, until the danger is certainly past, at a cost to work and patience. Or it can stand down the larger "
        "measures and keep only the sky watch and the relief stocks, trusting that the worst night is over.",
    ), (
        Option('Stay on alert for weeks.', (Stability(-0.01), WarSupport(0.03))),
        Option('Stand down the larger measures.', (Stability(0.03), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no fragment fall in Dakrain is '
                'claimed', picture=2),
    EventDef('decade_review', 'The Panel Drawn by Lot', (
        "The review panel meets in a converted mill hall in Brunies: fifteen citizens drawn by lot from both provinces, a "
        "staff of clerks and a mandate to ask anything. For three months it hears ministers, mill owners, union delegates, "
        "harbour councils, officers and frontier families. Its sessions are broadcast in full, and the audiences surprise the "
        "broadcasters.",
        "The testimony is uneven. The mills claim credit for a decade of growth and the unions for a decade of safer shafts. "
        "The air staff points to a wing that can fly in the rain, the harbours to their order books and the claims office to "
        "a frontier that stayed quiet. Every witness has a version, and every version leaves something out.",
        "The panel's report will shape the politics of the new decade. The government can adopt it in full, accepting its "
        "criticism along with its praise, or receive it with thanks and adopt what suits. Full adoption binds the government "
        "to reforms it did not write. Selective adoption keeps its freedom and invites the charge that the panel was theatre "
        "from the start.",
    ), (
        Option('Adopt it in full.', (Stability(0.03), PP(-25))),
        Option('Adopt what suits.', (PP(30), Stability(-0.02))),
    ), picture=2),
    EventDef('usean_freight', 'Rates for a Distant War', (
        "The shipping agents at Bell Town hear of war in Usea from the wire services before the ministries hear of it from "
        "their embassies. Insurance rates for routes near the Usean coast double within a week. Charter offers arrive for "
        "grain, machinery and medical stores, some at rates no Dakrainian owner has seen in a decade.",
        "Dakrain has no part in the war, and its government means to keep it that way. Its merchant fleet is small, pooled "
        "and modestly insured. A single ship lost near the fighting would be a national story; a season of high charter rates "
        "would pay off the pool's debts. The owners want permission, the crews want a choice and their families want them "
        "home.",
        "The ministry must decide how to answer the owners. It can allow charters under strict rules on cargo and routes, and "
        "let crews volunteer, or it can ask every Dakrainian-flagged hull to stay well clear of Usean waters until the war "
        "ends. The first earns money and accepts risk. The second costs money and keeps everyone home, which in a small port "
        "country is its own kind of argument.",
    ), (
        Option('Allow strict charters.', (PP(20), Stability(-0.01))),
        Option('Keep the hulls clear.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 2003 / 08.22 in tools/lore/chronicle.json; fired only after the mod flag '
                'ac_ucw_war_started; the Dakrainian response is gameplay', picture=0),
)

# --- branches ------------------------------------------------------------------------------------
BALLOT = Branch('ballot', 'The Suspended Ballot', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_last_ballot', 'The Last Ballot on the Calendar',
          "Dakrain's last recorded vote fell on the first day of 1991, and no further ballot stands on the calendar. The "
          "presidency, held by an officer with a marshal's rank, governs with a democratic majority and a left bloc that took "
          "nearly a third of the count. Printing the terms of the suspension invites every party to contest them in public.",
          ('ballot', 'document'), reward=(Idea('ballot_suspended'), Event('ballot_question'))),
    Focus('pol_left_talks', 'Round Table with the Left Bloc',
          "The communist bloc polled close to a third of the country and runs the strongest unions in the Brunies mills and "
          "on the Bell Town docks. A round table gives its delegates a fixed seat to argue wages, rents and the ballot itself. "
          "The presidency gains a channel to the shop floors and loses the pretence that the left can simply be ignored.",
          ('assembly', 'diplomacy'), after=('pol_last_ballot',),
          reward=(TimedIdea('round_table', 540), Flag('left_seated'))),
    Focus('pol_officer_mess', 'Questions in the Officers Mess',
          "Half the country tells pollsters it would back the army in a crisis, and the officer corps sees itself as the "
          "keeper of the republic rather than its servant. A commission of inquiry asks the garrison commanders what they "
          "expect of the next government. Their answers are frank, and some of them read more like terms than like advice.",
          ('command', 'security'), after=('pol_last_ballot',), reward=(TimedIdea('garrison_inquiry', 365), XP('army', 15))),
    Focus('pol_princely_party', 'The Princely Loyalists',
          "One voter in ten still answers to the old princely party, whose name survives in the title the country would carry "
          "under a throne. Its members hold no seats of consequence but sit on the boards of several mills and estates. Hearing "
          "their petition costs little, and the presidency learns which families would back a strong executive if the polls "
          "stay shut.",
          ('medal', 'assembly'), after=('pol_last_ballot',), reward=(TimedIdea('princely_patrons', 365),)),
    Focus('pol_path_republic', 'Reopen the Polling Stations',
          "Liberal deputies and most of the press want the suspension lifted and a full ballot held within the year, with "
          "ministers answerable to an elected chamber. It is the course most voters say they expect. The presidency would "
          "become one office among several, and the officers who prized its freedom of action would have to accept a civilian "
          "minister above them.",
          ('ballot', 'civil'), after_any=('pol_left_talks', 'pol_officer_mess', 'pol_princely_party'),
          exclusive=('pol_path_presidency', 'pol_path_councils', 'pol_path_marshals'),
          reward=(SwapIdea('ballot_suspended', 'republic_mandate'),)),
    Focus('pol_path_presidency', 'A Presidency Above the Parties',
          "The conservative majority proposes keeping the ballot suspended while a council of state chosen by the presidency "
          "governs on a published programme. The argument is stability: the frontier is disputed, the mills need investment "
          "and elections invite promises no treasury can keep. Opponents note that every suspended ballot calls itself "
          "temporary on the day it begins.",
          ('command', 'ballot'), after_any=('pol_left_talks', 'pol_officer_mess', 'pol_princely_party'),
          exclusive=('pol_path_republic', 'pol_path_councils', 'pol_path_marshals'),
          reward=(SwapIdea('ballot_suspended', 'guardianship'),)),
    Focus('pol_path_councils', 'Power to the Works Councils',
          "The left bloc offers its own answer: elected councils in every mill, dock and depot, sending delegates to a federal "
          "committee that replaces the presidency. Production plans would be argued on the shop floor and the budget voted by "
          "delegates. Property owners and the officer corps warn that they will not stay quiet, and the liberal press is not "
          "far behind them.",
          ('industry', 'assembly'), after_any=('pol_left_talks', 'pol_officer_mess', 'pol_princely_party'),
          exclusive=('pol_path_republic', 'pol_path_presidency', 'pol_path_marshals'),
          reward=(SwapIdea('ballot_suspended', 'councils_mandate'),)),
    Focus('pol_path_marshals', 'The Marshals Step Forward',
          "A group of senior commanders proposes to formalise what the presidency's rank already implies: a directorate of "
          "marshals holding the seals, the budget and the frontier, with the parties kept as advisory bodies. Decisions would be "
          "fast and the army content. The left bloc, the press and many democrats would consider the republic finished in all "
          "but name.",
          ('security', 'command'), after_any=('pol_left_talks', 'pol_officer_mess', 'pol_princely_party'),
          exclusive=('pol_path_republic', 'pol_path_presidency', 'pol_path_councils'),
          reward=(SwapIdea('ballot_suspended', 'marshals_order'),)),
    Focus('pol_seat_cabinet', 'Seat an Elected Cabinet',
          "Polling stations reopen across Trent and Brunies, and the new chamber forms a cabinet answerable to its majority. "
          "The presidency becomes an office of state with a fixed term and narrow powers. Turnout in the port districts is high "
          "and noisy. The cabinet inherits a disputed frontier, a demanding officer corps and a budget nobody has audited in "
          "years.",
          ('ballot', 'scales'), after=('pol_path_republic',), cost=10,
          exclusive=('pol_seat_council', 'pol_seat_committee', 'pol_seat_directorate'),
          reward=(Regime('republic_cabinet'), Flag('path_republic'))),
    Focus('pol_seat_council', 'The Council of State Sits',
          "A council of state named by the presidency takes over the ministries and publishes a five-year programme in place "
          "of an election manifesto. The chamber continues to meet as an advisory body, its sessions broadcast but its votes "
          "not binding. Investors approve of the calm. The unions and the liberal press begin counting how long temporary lasts.",
          ('command', 'document'), after=('pol_path_presidency',), cost=10,
          exclusive=('pol_seat_cabinet', 'pol_seat_committee', 'pol_seat_directorate'),
          reward=(Regime('presidential_council'), Flag('path_presidency'))),
    Focus('pol_seat_committee', 'The Federal Committee Convenes',
          "Delegates from the mill, dock and depot councils elect a federal committee that takes the ministries from the "
          "presidency. Managers keep their posts but answer to council votes on wages and output. Several mill owners move "
          "their accounts abroad within the week. The committee governs a country where a third cheered and much of the rest "
          "is waiting to see.",
          ('assembly', 'industry'), after=('pol_path_councils',), cost=10,
          exclusive=('pol_seat_cabinet', 'pol_seat_council', 'pol_seat_directorate'),
          reward=(Regime('workers_federation'), Flag('path_councils'))),
    Focus('pol_seat_directorate', 'Marshals Hold the Seals',
          "The directorate of marshals assumes the seals, the treasury and command of the frontier companies. Civil ministries "
          "remain, staffed by the same officials under military supervisors. The parties keep their offices and lose their "
          "purpose. Order is visible on every street corner in Brunies, and so is its price, in the silence of papers that used "
          "to argue.",
          ('security', 'medal'), after=('pol_path_marshals',), cost=10,
          exclusive=('pol_seat_cabinet', 'pol_seat_council', 'pol_seat_committee'),
          reward=(Regime('marshals_directorate'), Flag('path_marshals'))),
    Focus('pol_open_chamber', 'Budget Hearings in the Open Chamber',
          "The first elected budget is argued line by line: steel subsidies, frontier posts, airfields and the price of bread "
          "in Bell Town. Ministers who used to sign quietly must now defend each figure on the record. The hearings run long "
          "and the press loves them. Spending slows for a season, and the public finally sees where its money went.",
          ('scales', 'ballot'), after=('pol_seat_cabinet',),
          exclusive=('pol_decree_terms', 'pol_mill_councils', 'pol_officer_prefects'),
          reward=(TimedIdea('chamber_hearings', 730),)),
    Focus('pol_decree_terms', 'Decrees That Expire',
          "To answer the charge that it rules without limit, the council of state attaches an expiry date to every decree, "
          "after which the advisory chamber must review it. The rule is self-imposed and could be withdrawn at will. It still "
          "forces the ministries to justify their orders twice, and a few orders quietly lapse because nobody bothered to "
          "defend them.",
          ('document', 'command'), after=('pol_seat_council',),
          exclusive=('pol_open_chamber', 'pol_mill_councils', 'pol_officer_prefects'),
          reward=(TimedIdea('decree_terms', 730),)),
    Focus('pol_mill_councils', 'A Council in Every Mill',
          "Every mill, shaft and dock with more than a few dozen workers elects a council with a say over shifts, safety and "
          "the use of profits. Output dips while the councils learn the books, then recovers as waste becomes visible to the "
          "people who used to be blamed for it. Managers resign in small numbers, and their successors are elected.",
          ('industry', 'ballot'), after=('pol_seat_committee',),
          exclusive=('pol_open_chamber', 'pol_decree_terms', 'pol_officer_prefects'),
          reward=(Idea('mill_councils'),)),
    Focus('pol_officer_prefects', 'Officers in the Prefectures',
          "Serving officers replace civilian prefects across Trent and are told to finish the works the old councils left "
          "pending. The first project is the road and rail spur behind Oderin, stalled for years in tender disputes. "
          "Contractors who once negotiated now take orders. The work is done on time, and complaints about it have nowhere to "
          "go.",
          ('security', 'rail'), after=('pol_seat_directorate',),
          exclusive=('pol_open_chamber', 'pol_decree_terms', 'pol_mill_councils'),
          reward=(Build('infrastructure', 1, 114), PP(15))),
))

CLAIMS = Branch('claims', 'Claims and Crossings', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('fro_two_maps', 'Two Maps of the Same Frontier',
          "Dakrainian school maps mark North Dakrain and the Terentio Desert as lost provinces, while the claims recorded for "
          "Perbla and for Terentio mark Trent and Brunies in turn. Nobody is moving a post. A claims office in Brunies gathers "
          "every treaty, survey and complaint into one archive, so that the government at least knows what it is arguing "
          "about.",
          ('scales', 'document'), reward=(Idea('claims_office'), Event('claims_map'))),
    Focus('fro_karluga_families', 'Families on Both Sides of Karluga',
          "Many households in Trent have relatives around Karluga, across the line in North Dakrain, and visiting them means "
          "queues, fees and the occasional arrest for carrying the wrong papers. A consular desk for family visits, pension "
          "transfers and lost documents asks nothing of Perbla except stamps. It eases a daily grievance without advancing or "
          "conceding any claim.",
          ('refugees', 'civil'), after=('fro_two_maps',), reward=(Idea('kin_desk'),)),
    Focus('fro_gatewood_line', 'A Telephone to Gatewood',
          "Herders, smugglers and water trucks cross the Terentio frontier every day, and every incident climbs to the "
          "ministries before anyone speaks to Perbla. A standing line between frontier officials in Brunies and their "
          "counterparts in Gatewood lets a seized truck or a stray patrol be settled by a call. It changes nobody's claim. It "
          "does admit that the other side exists.",
          ('communications', 'diplomacy'), after=('fro_two_maps',),
          reward=(Flag('gatewood_line'), Stability(0.02),
                  Tooltip('No claim, core or border changes; the line handles incidents at the crossings only.'))),
    Focus('fro_nieblo_passes', 'Herding Passes Toward Eastern Nieblo',
          "Brunies meets Arklith along the valleys running down from Eastern Nieblo, where herders and ore trucks share tracks "
          "older than either state. Seasonal grazing passes issued at the Dakrainian end, with posted crossing hours, suit the "
          "arrangements the Arklith valley towns ask for. Customs earns little. The valley villages lose a winter's worth of "
          "quarrels with the frontier police.",
          ('peace', 'logistics'), after=('fro_two_maps',), reward=(TimedIdea('nieblo_passes', 1095),)),
    Focus('fro_leasath_posts', 'Observation Posts Facing Leasath',
          "The short frontier with Leasath at the edge of Brunies has never been in dispute, but Leasath's own politics are "
          "restless and Dakrain prefers early notice to surprises. A radar post and a pair of observation towers above the "
          "frontier road report to the capital every morning. The posts cost little, provoke nobody and are quietly "
          "reassuring to the garrison towns.",
          ('radar', 'security'), after=('fro_two_maps',), reward=(Build('radar_station', 1, 234), XP('army', 10))),
    Focus('fro_claim_statute', 'Write the Claim into Law',
          "Nationalist deputies want the claims on North Dakrain and the Terentio Desert written into statute, with a ministry "
          "to keep them alive in schools, maps and diplomatic notes. The law moves no post on the ground. It hardens opinion "
          "at home, and the officer corps likes it. Gatewood will read it as hostile, and every crossing will become slightly "
          "harder.",
          ('scales', 'security'), after_any=('fro_karluga_families', 'fro_gatewood_line'), cost=10,
          exclusive=('fro_claim_drawer',),
          reward=(SwapIdea('claims_office', 'claim_in_law'), Flag('claim_pressed'),
                  Tooltip('The claims stay claims; no border, core or war effect.'))),
    Focus('fro_claim_drawer', 'Leave the Claim in a Drawer',
          "The other view keeps the claims on record and stops talking about them. Maps stay as they are, but ministers decline "
          "to raise the frontier abroad and schools teach it as history rather than grievance. Trade with Perbla gets easier "
          "and the crossings calmer. Nationalist deputies call it surrender by instalments, and many officers quietly agree.",
          ('peace', 'document'), after_any=('fro_karluga_families', 'fro_gatewood_line'), cost=10,
          exclusive=('fro_claim_statute',),
          reward=(SwapIdea('claims_office', 'quiet_claim'), Flag('claim_shelved'))),
    Focus('fro_desert_guard', 'A Guard for the Desert Line',
          "With the claim in statute, the frontier police and the army's border companies merge into one guard for the line "
          "facing North Dakrain and the Terentio Desert, with a radar head above the desert road. Patrols are better trained "
          "and more visible. Perblan officers across the line notice the change at once and double their own patrols in reply.",
          ('security', 'training'), after=('fro_claim_statute',),
          reward=(Idea('frontier_guard'), Build('radar_station', 1, 234))),
    Focus('fro_wells_commission', 'Wells and Customs Commission',
          "With the claim set aside in practice, frontier officials propose a standing commission with Perbla on what actually "
          "troubles the crossings: shared wells, customs hours, stray herds and truck permits. Dakrain staffs its side whether "
          "or not Gatewood fills every seat. No line moves and none is meant to. Disputes over water stop reaching the "
          "ministries.",
          ('peace', 'tools'), after=('fro_claim_drawer',), requires=(HasFlag('gatewood_line'),),
          reward=(Idea('wells_commission'),)),
    Focus('fro_market_days', 'Licensed Fairs at the Frontier Posts',
          "Whatever the claim policy, the frontier towns live from exchange. Licensed market days at the main crossings toward "
          "Perbla and Arklith let wool, tools, fuel and fruit change hands under inspection rather than in the dark. Smugglers "
          "lose part of their trade to honest stalls. Customs receipts stay modest, and the frontier towns prefer them to the "
          "alternative.",
          ('economy', 'peace'), after_any=('fro_desert_guard', 'fro_wells_commission'),
          reward=(TimedIdea('crossing_markets', 1095),)),
))

STEEL = Branch('steel', 'Brunies Steel and Tungsten', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('stl_walk_mills', 'Walk Every Furnace in Brunies',
          "Brunies holds all of Dakrain's steel and tungsten and most of its factories, yet nobody in the ministries can "
          "say which furnaces earn money and which survive on habit. Inspectors walk every mill, shaft and arms hall in the "
          "province and publish the count. The survey costs a year of friction with owners who preferred not to be counted.",
          ('industry', 'document'), reward=(Idea('mill_survey'), Event('furnace_count'))),
    Focus('stl_tungsten_seams', 'Map the Tungsten Seams',
          "The tungsten under Brunies is worked from a few old shafts with maps that predate most of the miners. A survey with "
          "modern drilling charts the seams properly and shows which deposits can be reached cheaply. Owners object to sharing "
          "the results. Without them every investor would be guessing, and the tool works and munitions lines would be planned "
          "blind.",
          ('tools', 'science'), after=('stl_walk_mills',),
          reward=(Research('excavation_tech', 0.5, 1), Flag('seams_mapped'))),
    Focus('stl_ore_rail', 'An Ore Line to Bell Town',
          "Ore and finished steel leave the mills by a single-track line and a road that floods every wet season. Doubling the "
          "track to the Bell Town quays and raising the embankments above the flood mark lets the mills ship in any weather. It "
          "is the largest civil works contract in years, and every mill owner wants the sidings near his own gate.",
          ('rail', 'logistics'), after=('stl_walk_mills',), reward=(Build('infrastructure', 1, 234),)),
    Focus('stl_one_combine', 'Fold the Mills into One Combine',
          "The ministry proposes merging the Brunies mills and shafts into one state combine with a single order book, a single "
          "wage scale and the government as owner. Duplication disappears and arms orders get priority. So does every "
          "inefficiency the combine's managers prefer to hide. Private owners would be paid in bonds and would not forgive it.",
          ('command', 'industry'), after_any=('stl_tungsten_seams', 'stl_ore_rail'), cost=10,
          exclusive=('stl_mill_shares',), reward=(SwapIdea('mill_survey', 'steel_combine'),)),
    Focus('stl_mill_shares', 'Sell Shares in the Mills',
          "The alternative keeps the mills independent and invites capital in: shares sold at home and abroad, a stock register "
          "in Brunies and rules on disclosure. Investment arrives where returns are highest, which is not always where the army "
          "wants it. Foreign owners would hold part of the country's only heavy industry, and the left bloc says so loudly.",
          ('economy', 'scales'), after_any=('stl_tungsten_seams', 'stl_ore_rail'), cost=10,
          exclusive=('stl_one_combine',), reward=(SwapIdea('mill_survey', 'mill_shares'),)),
    Focus('stl_munitions_hall', 'A Munitions Hall for the Combine',
          "With one order book, the combine can plan a new munitions hall beside the West Trent works without asking anyone's "
          "leave. A small coastal and air defence state needs shells, cartridges and spares more than it needs export steel. "
          "The hall fills the last free plot in the province, so whatever comes after must fit inside existing walls.",
          ('missile', 'industry'), after=('stl_one_combine',), exclusive=('stl_partner_furnace',),
          reward=(Build('arms_factory', 1, 234),)),
    Focus('stl_partner_furnace', 'A Foreign Partner for the Furnaces',
          "A foreign steelmaker buys a stake in the largest Brunies mill and pays for a modern furnace hall in return for a share "
          "of the output. Productivity jumps and the hall turns out sheet and pipe that sell abroad. The plot it occupies was "
          "the last free one in the province. Dakrain's steel now answers in part to a board that meets elsewhere.",
          ('diplomacy', 'industry'), after=('stl_mill_shares',), exclusive=('stl_munitions_hall',),
          reward=(Build('industrial_complex', 1, 234),)),
    Focus('stl_tool_works', 'Tungsten Tool Works',
          "Exporting raw tungsten earns little; cutting tools, drill bits and dies made from it earn far more. A tool works in "
          "Brunies, staffed by graduates of the mill schools, turns part of the ore into finished tooling for the province's own "
          "factories first. Imports of foreign tools fall. The works needs steady ore, and the shafts must keep pace with it.",
          ('tools', 'industry'), after=('stl_tungsten_seams',), reward=(Idea('tungsten_tooling'),)),
    Focus('stl_rescue_stations', 'Rescue Stations at the Shafts',
          "The furnace count found shafts with no rescue equipment, flooded escape galleries and ventilation that fails in the "
          "hot months. Rescue stations at every working shaft, with trained crews and breathing sets, are the unions' first "
          "demand and the owners' last priority. The government pays. Accidents fall, and so does the left bloc's best "
          "argument against the owners.",
          ('medical', 'tools'), after=('stl_walk_mills',), reward=(Idea('mine_safety'),)),
    Focus('stl_tungsten_abroad', 'Tungsten Contracts Abroad',
          "Tungsten is scarce in many arms industries, and buyers abroad pay in hard currency. Multi-year contracts for a fixed "
          "share of Brunies output bring steady revenue and a little diplomatic weight. The tool works and munitions lines must "
          "accept what remains. Every tonne sold abroad is one that cannot be used at home if the frontier ever turns hot.",
          ('economy', 'diplomacy'), after_any=('stl_munitions_hall', 'stl_partner_furnace'),
          reward=(TimedIdea('ore_contracts', 730),)),
    Focus('stl_home_rails', 'Rails Rolled in Brunies',
          "Every rail on the ore line was imported. The mills can roll their own, given a new set of rollers and a contract "
          "long enough to justify buying them. Rolling rails at home keeps money in Brunies and lets the railway plan "
          "replacements without waiting on foreign mills. Quality will lag at first, and engineers will inspect every batch.",
          ('rail', 'industry'), after=('stl_ore_rail',), reward=(Research('train_tech', 0.5, 1), Flag('home_rails'))),
))

HARBOURS = Branch('harbours', 'Bell Town and Oderin', 1992, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('prt_two_harbours', 'Two Harbours Under One Board',
          "Dakrain has two working harbours: Bell Town, the deeper port serving the capital province and the navy, and Oderin, "
          "the busier commercial quay of Trent. They compete for every dredging budget and every shipping line. A joint harbour "
          "board would set dues and plan works for both, if the two port councils can be persuaded to share a single table.",
          ('navy', 'scales'), reward=(Idea('harbour_board'), Event('two_harbours'))),
    Focus('prt_bell_dredging', 'Dredge the Bell Town Channel',
          "Silt carried by the wet-season rivers narrows the Bell Town channel every year, and larger freighters wait offshore "
          "for the tide. A dredging programme with a permanent crew and a spoil ground down the coast keeps the channel at "
          "depth. It is endless work rather than a single project. Without it, every plan to grow the port is wishful "
          "thinking.",
          ('navy', 'tools'), after=('prt_two_harbours',),
          reward=(Flag('channel_dredged'), Research('naval_equipment', 0.3, 1))),
    Focus('prt_oderin_slip', 'A Slipway at Oderin',
          "The Oderin quay repairs fishing boats and coasters but cannot build anything larger. A new slipway and fitting shop "
          "would let Trent build its own small hulls: coastal escorts, tugs and ferries. It takes the last free plot in the "
          "province and draws welders away from other trades. The port council has asked for it since before the ballot was "
          "suspended.",
          ('navy', 'industry'), after=('prt_two_harbours',), reward=(Build('dockyard', 1, 114),)),
    Focus('prt_harbour_police', 'Harbour Police Against the Smugglers',
          "Smuggled fuel, cigarettes and weapons move through both harbours under the noses of underpaid customs men. A harbour "
          "police with its own launches and searchers, and a mandate across both ports, breaks the easiest routes. Some "
          "officials lose side incomes and a few lose their posts. The port councils welcome the change in public and "
          "complain about it in private.",
          ('security', 'navy'), after=('prt_two_harbours',), reward=(Flag('harbour_police'), Stability(0.01))),
    Focus('prt_free_port', 'Bell Town as a Free Port',
          "One plan turns Bell Town into a free port: a bonded zone where foreign goods can be stored, repacked and re-exported "
          "without duty. Shipping lines would call more often and warehouses would fill. Customs officers distrust the idea, "
          "and the mill owners fear cheap foreign steel slipping out of the zone into the home market.",
          ('economy', 'logistics'), after=('prt_bell_dredging',), cost=10, exclusive=('prt_naval_harbour',),
          reward=(SwapIdea('harbour_board', 'free_port'),)),
    Focus('prt_naval_harbour', 'Bell Town for the Navy First',
          "The other plan reserves the best berths at Bell Town for the coastal escort and the hulls meant to follow it, and "
          "moves commercial traffic to Oderin. The navy gains a protected base with fuel, magazines and repair crews close at hand. Merchants "
          "lose the deeper channel and say so. The port council must accept that its harbour has become a military one.",
          ('navy', 'security'), after=('prt_bell_dredging',), cost=10, exclusive=('prt_free_port',),
          reward=(SwapIdea('harbour_board', 'naval_harbour'),)),
    Focus('prt_escort_rota', 'A Rota for the Coastal Escorts',
          "Dakrain's navy is a single coastal escort of destroyer size and whatever the yards add to it. A rota written now for "
          "the squadron to come keeps one hull on patrol, one in training and one in refit, so the coast is never unwatched "
          "and no ship is worked to exhaustion. Until the new hulls arrive, the lone escort's crew trains for all three roles.",
          ('navy', 'training'), after_any=('prt_free_port', 'prt_naval_harbour'),
          reward=(Idea('escort_rota'), XP('navy', 10))),
    Focus('prt_hull_pool', 'Pooling the Sixty Hulls',
          "Dakrain's sixty merchant hulls belong to a dozen owners who compete for the same cargoes and leave ships idle in "
          "between. A voluntary pool shares bookings, crews and repair slots, with the state guaranteeing a minimum charter rate "
          "in lean months. Fewer ships sail empty. Owners grumble about the paperwork and keep joining once they see the "
          "receipts.",
          ('logistics', 'navy'), after=('prt_oderin_slip',), reward=(TimedIdea('convoy_pool', 730),)),
    Focus('prt_repair_berths', 'Repair Berths for Passing Ships',
          "With the free port drawing more traffic, ship owners ask for repairs that do not require a voyage home. The Bell "
          "Town quays add two repair berths, a floating crane and a parts store. The work pays well and trains welders who "
          "will be useful if the navy ever needs them in a hurry. Pilots begin recommending Bell Town to passing masters.",
          ('tools', 'navy'), after=('prt_free_port',), reward=(Idea('repair_berths'),)),
    Focus('prt_fishing_coops', 'Fishing Cooperatives at Oderin',
          "The Oderin fishing fleet sells its catch through middlemen who set prices on the quay each morning. Cooperatives with "
          "their own cold store and auction hall let crews sell directly and borrow against future catches. Middlemen resist "
          "and some boats stay out. Within two seasons the cooperatives handle most of the catch, and the boats are better kept.",
          ('fishing', 'civil'), after=('prt_oderin_slip',), reward=(TimedIdea('fishing_coops', 1095),)),
))

WING = Branch('wing', 'The Air Defence Wing', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count_wing', 'Twenty-Four Fighters and a Plan',
          "Dakrain's air arm is two dozen Service Fighters, a handful of reserve airframes and the hardstands of the Brunies "
          "fields, with one more field in Trent. It is enough to show the flag and not enough to defend two port cities. The "
          "air staff is asked for a plan that a small country can afford and still fly in the wet season.",
          ('air', 'document'), reward=(Idea('service_wing'), Event('wing_review'))),
    Focus('air_brunies_hardstands', 'Hardstands at the Brunies Fields',
          "The main fields around Brunies flood in heavy rain and their dispersal areas turn to mud. Concrete hardstands, drained "
          "taxiways and covered revetments let the wing operate through the wet season and survive a surprise raid. The concrete "
          "comes from the Brunies works, which pleases the mill owners and strains the air budget.",
          ('runway', 'air'), after=('air_count_wing',), reward=(Build('air_base', 2, 234),)),
    Focus('air_coast_chain', 'A Radar Chain on the Coast',
          "Ships and aircraft approaching Oderin and Bell Town are seen from the quays only when they are close enough to be "
          "heard. Two radar posts on the Trent coast, linked by landline to the air operations room, give the wing minutes of "
          "warning instead of seconds. The posts also watch shipping, which the customs service finds more useful than the air "
          "staff expected.",
          ('radar', 'navy'), after=('air_count_wing',), reward=(Build('radar_station', 2, 114),)),
    Focus('air_spares_first', 'Spares Before New Airframes',
          "The wing could buy a few new fighters or keep every existing one flying for a decade. The air staff chooses spares: "
          "engines, tyres, radios and the tools to fit them, stored in dry sheds out of the rain. Availability rises from half "
          "the wing to most of it. Newspaper photographs of shiny new aircraft will have to wait.",
          ('tools', 'air'), after=('air_count_wing',), reward=(Flag('spares_stocked'), Research('air_doctrine', 0.5, 1))),
    Focus('air_interceptors', 'Interceptors Over the Ports',
          "One school in the air staff wants every fighter tied to the radar chain and held at readiness near the two harbours, "
          "able to climb and intercept within minutes. It is the cheapest way to make the ports costly to attack. It leaves the "
          "frontier and the army with little air support, and the generals in Brunies say so.",
          ('air', 'radar'), after_any=('air_brunies_hardstands', 'air_coast_chain'), cost=10,
          exclusive=('air_dispersal',), reward=(SwapIdea('service_wing', 'interceptor_net'),)),
    Focus('air_dispersal', 'Fields Hidden in the Plain',
          "The other school assumes the main fields would be hit first and spreads the wing across grass strips, road sections "
          "and farm fields throughout Trent, with fuel and ammunition cached at each. Aircraft would survive a first strike and "
          "keep flying. Readiness suffers, maintenance gets harder, and pilots spend more time driving than flying.",
          ('runway', 'security'), after_any=('air_brunies_hardstands', 'air_coast_chain'), cost=10,
          exclusive=('air_interceptors',), reward=(SwapIdea('service_wing', 'dispersed_fields'),)),
    Focus('air_scramble_room', 'A Five-Minute Scramble',
          "Interception depends on time, so the wing builds an operations room in Brunies tied to two new inland radars and the "
          "coast chain. Pilots on alert sit in their cockpits, not in crew rooms. The target is airborne within five minutes of "
          "a warning. Crews resent the long alert shifts, and admit after the first drills that the system works.",
          ('radar', 'communications'), after=('air_interceptors',), reward=(Build('radar_station', 2, 234),)),
    Focus('air_grass_strips', 'Grass Strips Across Trent',
          "Engineers survey the flat farmland of Trent for strips that drain well and lease them from farmers, with "
          "compensation for lost harvests. Each gets a fuel bladder, an ammunition pit and a radio hut. The strips appear on no "
          "public map. Farmers grumble about the noise and are paid on time, which in Trent counts as a fair arrangement.",
          ('runway', 'logistics'), after=('air_dispersal',), reward=(Build('air_base', 3, 114),)),
    Focus('air_hired_instructors', 'Instructors on Contract',
          "By 1998 former Belkan Air Force pilots are working abroad as aggressor squadrons for whoever will pay. Dakrain could "
          "hire contract instructors to fly against its own pilots and teach what only hard training teaches. The instruction "
          "would be the best the wing has ever had. Questions about whose loyalties those instructors keep would never quite go "
          "away.",
          ('training', 'air'), after_any=('air_scramble_room', 'air_grass_strips'), requires=(After('1998.6.19'),),
          exclusive=('air_home_school',), reward=(TimedIdea('contract_instructors', 1095),)),
    Focus('air_home_school', 'A Flying School of Our Own',
          "The alternative trains instructors at home: the best pilots of the wing rotate through a national flying school and "
          "write the syllabus as they go. Progress is slower, and mistakes are repeated before they are learned. The school "
          "answers to nobody abroad, and its graduates build a tradition the country owns, which matters to the officer corps "
          "more than speed.",
          ('training', 'medal'), after_any=('air_scramble_room', 'air_grass_strips'),
          exclusive=('air_hired_instructors',), reward=(Idea('home_school'),)),
))

COLUMNS = Branch('columns', 'Keep the Columns Moving', 1991, 'FOCUS_FILTER_MANPOWER', (
    Focus('sus_count_stocks', 'Count Every Truck and Rifle',
          "The army's reserve stores hold under a thousand sets of infantry equipment, some seven hundred trucks and two dozen "
          "trains, and nobody has checked them against the books in years. The general staff puts physical sustainment first: "
          "transport, spares and replacements before any new unit. The count begins in every depot, and some shortfalls are "
          "embarrassing.",
          ('logistics', 'document'), reward=(Idea('sustainment_first'), Event('wet_season_trial'))),
    Focus('sus_rain_manoeuvres', 'Manoeuvres in the Rains',
          "The plains turn to mud for months each year, and every exercise so far has been held in the dry season for "
          "convenience. The staff now schedules manoeuvres in the rains, with trucks bogging down, radios failing and supply "
          "columns arriving late. The first exercises are humiliating. The lessons are written down, and the second round goes "
          "better.",
          ('training', 'logistics'), after=('sus_count_stocks',), reward=(TimedIdea('rain_manoeuvres', 730),)),
    Focus('sus_replacement_depots', 'Replacement Depots in Trent',
          "Losses in a war would be replaced from depots that today exist only on paper. Proper depots behind the Trent front, "
          "with stocks of equipment, spare parts and trained replacements rotating through them, would keep formations fighting "
          "rather than waiting. The depots tie up equipment that could be issued now. The staff argues that is the whole point.",
          ('logistics', 'tools'), after=('sus_count_stocks',), reward=(Idea('replacement_depots'),)),
    Focus('sus_rail_spurs', 'Rail Spurs to the Northern Line',
          "Trent faces North Dakrain across open country, and reinforcing it today means trucks on a single road. With rails "
          "now rolled in Brunies, the army can afford spurs from the coastal line toward the northern frontier, with sidings to "
          "unload a battalion in a night. Farmers lose strips of land and gain a station.",
          ('rail', 'security'), after=('sus_count_stocks',), requires=(HasFlag('home_rails'),),
          reward=(Build('infrastructure', 1, 114),)),
    Focus('sus_universal_year', 'Keep a Universal Year',
          "One camp in the general staff wants a year of service for every fit young adult, followed by reserve duty into "
          "middle age. It fills the four formations with trained men and makes the frontier credible in the eyes of the "
          "neighbours. It also takes workers from the mills and docks every year, and the employers' associations object.",
          ('training', 'security'), after=('sus_rain_manoeuvres',), exclusive=('sus_volunteer_core',),
          reward=(Idea('conscript_levy'),)),
    Focus('sus_volunteer_core', 'A Volunteer Core',
          "The other camp prefers fewer soldiers who stay longer: volunteers on proper pay, trained to maintain their own trucks "
          "and weapons, with a small reserve behind them. The army would be smaller and better. The frontier would rely on "
          "quality rather than numbers, and the mills would keep their workers. Recruiters warn that pay must keep up with the "
          "docks.",
          ('medal', 'training'), after=('sus_rain_manoeuvres',), exclusive=('sus_universal_year',),
          reward=(Idea('volunteer_core'),)),
    Focus('sus_mud_engineers', 'Engineers for Mud and Bridges',
          "The rain exercises showed that trucks stop where bridges wash out and roads dissolve. An engineer battalion trained "
          "in temporary bridging, corduroy roads and drainage would keep columns moving. Its tools are cheap and its training "
          "slow. Engineers have other uses too, and the civil ministries are already asking to borrow them.",
          ('bridge', 'tools'), after=('sus_rain_manoeuvres',),
          reward=(Research('engineers_tech', 0.5, 1), Flag('mud_engineers'))),
    Focus('sus_district_musters', 'Reserve Musters by District',
          "Reservists in Trent and Brunies are listed by district, each with a muster point, a railway station and an assigned "
          "formation. Annual musters test the lists and catch the dead, the emigrated and the forgotten. Employers must release "
          "men for a week each year. Mobilisation that took weeks on paper now takes days in practice.",
          ('document', 'security'), after=('sus_universal_year',), reward=(TimedIdea('muster_drills', 730),)),
    Focus('sus_career_sergeants', 'Career Sergeants',
          "A volunteer army lives or dies by its sergeants. Long-service contracts, a sergeants school in Brunies and a pension "
          "at twenty years give the best soldiers a reason to stay. Officers lose some of their monopoly on judgement. Units "
          "become steadier, and young lieutenants learn more from their sergeants than from their manuals.",
          ('medal', 'command'), after=('sus_volunteer_core',), reward=(TimedIdea('sergeant_school', 730),)),
    Focus('sus_tungsten_cores', 'Tungsten Cores for Anti-Tank Rounds',
          "The infantry's anti-tank teams fire imported rounds that cost more than the soldiers who carry them. With the "
          "tungsten seams mapped, the munitions lines can make penetrator cores at home, and teams train with live rounds rather "
          "than counting them. An armoured column crossing the open plain would meet a well-supplied defence, which is the heart "
          "of the army's doctrine.",
          ('missile', 'tools'), after=('sus_replacement_depots',), requires=(HasFlag('seams_mapped'),),
          reward=(TimedIdea('antitank_teams', 730), Research('infantry_weapons', 0.3, 1))),
))

NORTHWAR = Branch('northwar', 'War in the North', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_news', 'War News from the North',
          "In March 1995 the Belkan War breaks out far to the north. Dakrain is not a party and has no wish to become one, but "
          "Perbla across the frontier counts Belka among its oldest friends, and every shipping line in the region recalculates "
          "its routes. The government opens a war desk in Brunies to follow the fighting and, more closely, the neighbours.",
          ('communications', 'command'), requires=(After('1995.3.25'),), reward=(Idea('war_desk'), Event('northern_war'))),
    Focus('war_neutral_ports', 'Neutral in Word and Port',
          "Dakrain declares strict neutrality: no arms, fuel or port services for any belligerent, with inspections to enforce "
          "it. It is the safest course for a small country between a Belkan friend and the Osean coast. Trade suffers as some "
          "lines avoid the inspections. Nobody abroad thanks Dakrain for it, and nobody has reason to resent it either.",
          ('peace', 'scales'), after=('war_news',), exclusive=('war_osean_quays',),
          reward=(SwapIdea('war_desk', 'strict_neutrality'),)),
    Focus('war_osean_quays', 'Open Quays for Osean Freight',
          "Osean freight lines ask for bunkering and repairs at Bell Town while the war disrupts their usual routes. Agreeing "
          "earns money and Osean goodwill without sending a soldier anywhere or signing any alliance. It also tells Perbla, "
          "which counts Belka among its friends, which way Dakrain leans. The frontier will be watched more closely from both "
          "sides.",
          ('diplomacy', 'logistics'), after=('war_news',), exclusive=('war_neutral_ports',),
          reward=(SwapIdea('war_desk', 'osean_freight'), Tooltip('No faction, alliance or war effect.'))),
    Focus('war_contraband', 'Contraband Searches at the Quays',
          "With war at sea in the north, contraband finds new routes through small ports far from the fighting. The harbour "
          "police, already trained against smugglers, search cargoes bound for the war zone and seize what the rules forbid. "
          "Shipowners complain of delays. The searches protect Dakrain's standing and keep its harbours off anyone's target "
          "list.",
          ('security', 'navy'), after=('war_news',), requires=(HasFlag('harbour_police'),),
          reward=(TimedIdea('contraband_searches', 365),)),
    Focus('war_perbla_watch', 'Eyes on the Perblan Frontier',
          "Perbla's old friendship with Belka could pull it toward the war, and the frontier facing North Dakrain would be the "
          "first place anyone noticed. The frontier companies go to a higher alert, observation posts are manned around the "
          "clock and reserve officers keep their bags packed. It is precaution rather than provocation, and Gatewood is told so.",
          ('security', 'radar'), after=('war_news',), reward=(TimedIdea('perbla_watch', 540),)),
    Focus('war_price_boards', 'Price Boards for Fuel and Bread',
          "A distant war still reaches the shops. Fuel and grain prices rise as shipping reroutes, and hoarding starts in Bell "
          "Town within a fortnight. Price boards in every district post maximum prices for bread, cooking fuel and kerosene, "
          "and fine merchants who exceed them. Black markets appear at the margins. Most households are grateful, and the left "
          "bloc claims credit.",
          ('economy', 'civil'), after=('war_news',), reward=(TimedIdea('price_boards', 365),)),
    Focus('war_belka_defeated', 'Belka Loses Its War',
          "Belka comes out of the war defeated, and the demand for rebuilding across the north reaches the Brunies order books "
          "within months. Steel, pipe and spare parts sell well. Perbla mourns its friend's defeat in its newspapers and keeps "
          "its own counsel. Dakrain's frontier companies report a quiet line and ask how long the alert must last.",
          ('industry', 'diplomacy'), after_any=('war_neutral_ports', 'war_osean_quays'),
          requires=(HasGlobal('belka_lost_belkan_war'),), exclusive=('war_belka_prevails',),
          reward=(TimedIdea('postwar_orders', 540),)),
    Focus('war_belka_prevails', 'Belka Wins Its War',
          "Belka comes out of the war the victor, and its friends speak with new confidence. Perbla's newspapers celebrate; its "
          "officers visit the frontier more often. Nothing changes on the ground, but Dakrain's planners must now assume a "
          "stronger north and a neighbour proud of its old alliance. The frontier companies are told to stay alert.",
          ('security', 'command'), after_any=('war_neutral_ports', 'war_osean_quays'),
          requires=(HasGlobal('belka_won_belkan_war'),), exclusive=('war_belka_defeated',),
          reward=(Idea('northern_shadow'), WarSupport(0.03))),
    Focus('war_distant_lessons', 'Lessons of a Distant War',
          "Whatever its outcome, the war in the north was watched closely by every staff officer in Brunies. Air power decided "
          "battles, small armies were overrun in days and neutral ports became prizes. A study group writes up what Dakrain's "
          "forces would have faced in such a war. The report is sobering, and the general staff insists it be read in full.",
          ('document', 'command'), after_any=('war_belka_defeated', 'war_belka_prevails'),
          reward=(Research('land_doctrine', 0.5, 1), Flag('war_lessons'))),
))

ULYSSES = Branch('ulysses', 'Under Ulysses', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_impact_announced', 'An Impact Without an Address',
          "The December 1994 warning about the asteroid Ulysses turned into a certainty in April 1996, when the FCU announced "
          "that it will strike the Earth. Nobody can yet say where its fragments will fall. Most Dakrainians live in West Trent, "
          "Bell Town and Oderin on a low coastal plain, and the government begins planning against a threat with no address.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),), reward=(Idea('sky_desk'), Event('ulysses_date'))),
    Focus('sky_storm_drains', 'Storm Drains for the Port Cities',
          "Whatever Ulysses brings, Bell Town and Oderin already flood in every heavy rain, and a city that cannot drain its "
          "streets cannot evacuate them. The army engineers trained for the mud help the city works departments clear and "
          "enlarge the storm drains. It is unglamorous work, and it protects against the next ordinary storm as well as the "
          "extraordinary one.",
          ('civil', 'tools'), after=('sky_impact_announced',), requires=(HasFlag('mud_engineers'),),
          reward=(Idea('storm_drains'),)),
    Focus('sky_mill_cellars', 'Shelters Under the Mill Floors',
          "The Brunies mills stand on deep foundations and thick basements. Reinforced and stocked, they could shelter the mill "
          "districts and keep key furnaces banked rather than abandoned. The work is expensive, and the owners want compensation "
          "for lost floor space. If fragments fall near a mill town its people will be underground; if not, the cellars become "
          "storerooms.",
          ('shelter', 'industry'), after=('sky_impact_announced',), cost=10, exclusive=('sky_leave_cities',),
          reward=(Idea('mill_shelters'),)),
    Focus('sky_leave_cities', 'Timetables for Leaving the Cities',
          "The cheaper plan accepts that no basement survives a direct hit and plans to move people instead. Every district "
          "gets a train, a departure time and a reception village inland. Rehearsals strand thousands at the wrong station "
          "before the timetables settle. Villages complain of the burden. Families at least know where they would go, which "
          "steadies the cities.",
          ('rail', 'refugees'), after=('sky_impact_announced',), cost=10, exclusive=('sky_mill_cellars',),
          reward=(Idea('evacuation_timetables'),)),
    Focus('sky_radar_watch', 'Radar Crews Watch the Sky',
          "Dakrain has no observatory of note, but its radar crews and a few university physicists can share foreign bulletins "
          "and their own readings. A sky watch post on the Trent coast, with a new radar head and a direct line to the civil "
          "defence office, issues a plain bulletin every week. Rumours lose force when facts arrive on schedule.",
          ('radar', 'telescope'), after=('sky_impact_announced',), reward=(Build('radar_station', 1, 114),)),
    Focus('sky_lean_months', 'Grain and Fuel for the Lean Months',
          "Markets will panic whenever fragments fall, wherever they fall. The state buys grain, cooking fuel and medicine to "
          "fill the silos and depots for three months of shortage, and releases old stock cheaply in rotation. Treasury officials "
          "dislike buying at the top of a nervous market. The public notices the full silos, and hoarding eases.",
          ('economy', 'shelter'), after=('sky_impact_announced',), reward=(TimedIdea('relief_stocks', 1095),)),
    Focus('sky_harbour_berths', 'Berths Held for Evacuation Ships',
          "With the Bell Town channel dredged, deep-draught ships can enter at any tide, and the civil defence office reserves "
          "berths for evacuation vessels during the danger months. Coastal villages that no railway reaches are assigned ships "
          "and muster points. Shipping lines lose some quay time and are compensated. The plan finally covers the people the "
          "timetables missed.",
          ('navy', 'refugees'), after_any=('sky_mill_cellars', 'sky_leave_cities'), requires=(HasFlag('channel_dredged'),),
          reward=(TimedIdea('evacuation_berths', 1095),)),
    Focus('sky_roche_night', 'The Night Ulysses Breaks Up',
          "On 8 July 1999 the asteroid crosses the Roche limit and begins to come apart. Every plan drafted since 1996 now "
          "meets the real thing. Sirens are tested, shelters and trains stand ready, and the sky watch reports through the "
          "night. Dakrain can do no more than it has prepared. What remains is to keep order and wait for morning.",
          ('meteor', 'shelter'), after_any=('sky_mill_cellars', 'sky_leave_cities'), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('sky_relief_office', 'A Relief Office for Strangers',
          "Wherever the fragments fell, the months after bring ships seeking safe harbour, travellers stranded by cancelled "
          "routes and insurers rethinking every coast. A relief office in Brunies handles arrivals, claims and the return of "
          "stocks to market. Its first year is chaotic. It becomes the permanent civil defence secretariat the country never "
          "had before.",
          ('refugees', 'medical'), after=('sky_roche_night',), reward=(Idea('relief_office'),)),
))

CENTURY = Branch('century', 'The Republic at the Century', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('mil_ten_years', 'Ten Years Since the Last Ballot',
          "A decade after the vote of 1991, a review panel drawn by lot from both provinces asks what the years built and what "
          "they cost: the government chosen, the mills, the harbours, the air wing and the frontier. Its hearings are public. "
          "The report will frame every argument of the new decade, and every faction prepares its testimony.",
          ('document', 'scales'), reward=(Event('decade_review'),)),
    Focus('mil_republic_constitution', 'A Constitution for the Republic',
          "The elected chamber consolidates a decade of statutes into one constitution: fixed terms, a court to read it and a "
          "presidency limited to ceremony and command in war. Ratification needs both provinces, and Trent bargains hard for "
          "its port revenues. Once it passes, no future government can suspend a ballot by decree.",
          ('scales', 'ballot'), after=('mil_ten_years',), requires=(HasFlag('path_republic'),),
          exclusive=('mil_council_statute', 'mil_councils_charter', 'mil_order_code'),
          reward=(SwapIdea('republic_mandate', 'republic_constitution'),)),
    Focus('mil_council_statute', 'The Statute of the Council of State',
          "Ten years of temporary government become a written statute: the council of state, its powers, the advisory chamber's "
          "agenda and the conditions under which a ballot would return. Critics call it a cage with the key inside. Foreign "
          "lenders call it predictability and price their loans accordingly. The presidency's authority is now law rather than "
          "habit.",
          ('command', 'document'), after=('mil_ten_years',), requires=(HasFlag('path_presidency'),),
          exclusive=('mil_republic_constitution', 'mil_councils_charter', 'mil_order_code'),
          reward=(SwapIdea('guardianship', 'council_statute'),)),
    Focus('mil_councils_charter', 'The Councils Write Their Charter',
          "The federal committee turns a decade of improvised council practice into a charter: how delegates are chosen, how "
          "plans are voted and how a mill can recall its managers. Some councils resist rules from above, and the charter "
          "passes anyway. The federation stops depending on the enthusiasm of its founders to keep running.",
          ('assembly', 'document'), after=('mil_ten_years',), requires=(HasFlag('path_councils'),),
          exclusive=('mil_republic_constitution', 'mil_council_statute', 'mil_order_code'),
          reward=(SwapIdea('councils_mandate', 'council_federation'),)),
    Focus('mil_order_code', 'The Directorate Publishes Its Code',
          "After a decade of orders and emergency powers, the directorate publishes a code of public order defining what it may "
          "do, what it will not do and how citizens can appeal. The code is strict, but it is written. Courts regain a narrow "
          "role. The officer corps accepts limits it set for itself, and the country learns where the lines are.",
          ('security', 'document'), after=('mil_ten_years',), requires=(HasFlag('path_marshals'),),
          exclusive=('mil_republic_constitution', 'mil_council_statute', 'mil_councils_charter'),
          reward=(SwapIdea('marshals_order', 'marshals_code'),)),
    Focus('mil_claim_white_paper', 'The Claim at Ten Years',
          "A decade after the claim was written into law, its ministry publishes a white paper on North Dakrain and the Terentio "
          "Desert, restating every argument for the record. Patriotic societies rally in Brunies. Nothing on the ground "
          "changes, as the government insists in every foreign capital. Perbla reads the paper carefully and files a reply of "
          "its own.",
          ('medal', 'scales'), after=('mil_ten_years',), requires=(HasFlag('claim_pressed'),),
          exclusive=('mil_quiet_decade',),
          reward=(TimedIdea('claim_rally', 365), Tooltip('No claim, core or border changes; the paper restates the claim only.'))),
    Focus('mil_quiet_decade', 'Ten Years of Quiet Crossings',
          "The claim has stayed in its drawer for a decade, and the crossings toward Perbla have become routine. Frontier towns "
          "trade, families visit and disputes over wells end at a desk rather than a ministry. Nationalists still mark the "
          "anniversary of the drawer every year. The government counts the customs receipts and lets them march.",
          ('peace', 'economy'), after=('mil_ten_years',), requires=(HasFlag('claim_shelved'),),
          exclusive=('mil_claim_white_paper',), reward=(TimedIdea('quiet_crossings', 730),)),
    Focus('mil_wage_accord', 'A Wage Accord for the Mills',
          "The round table opened in the early nineties has become a habit, and the unions, the mill owners and the ministry "
          "now meet every spring to fix wages for the year. Strikes fall to a fraction of their old number. The accord binds "
          "every party to a compromise none of them loves. Investors find Brunies a calmer place to put money.",
          ('economy', 'assembly'), after=('mil_ten_years',), requires=(HasFlag('left_seated'),),
          reward=(Idea('wage_accord'),)),
    Focus('mil_wing_decade', 'The Wing After Ten Years',
          "With spares stocked and pilots trained, the wing ends the decade with more aircraft flying than at any time since "
          "1991. The air staff asks for one more field in Trent to spread its readiness across both provinces. It is a modest "
          "request, granted with less argument than usual because the wing kept its earlier promises.",
          ('air', 'medal'), after=('mil_ten_years',), requires=(HasFlag('spares_stocked'),),
          reward=(Build('air_base', 1, 114), XP('air', 15))),
    Focus('mil_defence_review', 'A Defence Review for the Century',
          "The study of the northern war and a decade of rain manoeuvres feed a full defence review. Its authors rewrite the "
          "army's plans for a short, hard defence of the plain: fewer promises, more depots, closer work with the air wing and "
          "faster decisions at the top. Some senior officers lose favourite projects. Most of the staff welcome the clarity.",
          ('command', 'scales'), after=('mil_ten_years',), requires=(HasFlag('war_lessons'),),
          reward=(Idea('defence_review'),)),
    Focus('mil_usean_freight', 'The Usean War and the Freight Rates',
          "In 2003 war returns to Usea, and the FCU founds the ISAF to fight it. Dakrain has no part in it and wants none. Its "
          "shipping lines feel the war at once in freight rates, insurance and charter offers for routes near the fighting. "
          "The government must decide what Dakrainian-flagged hulls may carry, and where.",
          ('communications', 'logistics'), after=('mil_ten_years',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(Event('usean_freight'),)),
    Focus('mil_peaceful_cargo', 'Charters for Grain and Machinery',
          "Lines may carry grain, medicine and machinery to economies disrupted by the war, under strict manifest rules and with "
          "no military cargo at all. The pooled fleet earns well, and the repair berths fill with ships on longer routes. Crews "
          "face real risk near contested waters, and the government asks for volunteers rather than ordering anyone to sail.",
          ('logistics', 'economy'), after=('mil_usean_freight',), exclusive=('mil_home_routes',),
          reward=(TimedIdea('usean_charters', 730),)),
    Focus('mil_home_routes', 'Keep the Hulls Close to Home',
          "The government asks every Dakrainian-flagged ship to keep to routes far from the fighting, with harbour dues waived "
          "in compensation. Some owners comply and some reflag elsewhere. The fleet earns less and loses nobody. Crews spend "
          "more time at home, and the port towns say publicly that this is the price they would choose to pay.",
          ('navy', 'peace'), after=('mil_usean_freight',), exclusive=('mil_peaceful_cargo',),
          reward=(TimedIdea('home_routes', 730),)),
))

BRANCHES = (BALLOT, STEEL, COLUMNS, CLAIMS, HARBOURS, WING, NORTHWAR, ULYSSES, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('tungsten_lot', 'Auction a Tungsten Lot',
                'A lot of Brunies tungsten goes to foreign buyers at auction. Earns political capital for half a year at the cost '
                'of ore the tool works wanted.', 30, (TimedIdea('tungsten_auction', 180),),
                requires=(Completed('stl_tungsten_seams'),), cooldown=365),
    DecisionDef('desert_patrol', 'Patrol the Desert Line',
                'Frontier companies walk the line facing North Dakrain and the Terentio Desert for a week. Gains army experience; '
                'no claim, core or border changes.', 25, (XP('army', 10), WarSupport(0.01)),
                requires=(Completed('fro_two_maps'),), cooldown=180),
    DecisionDef('brunies_runways', 'Lengthen the Brunies Runways',
                'The main Brunies fields gain longer runways and more hardstands. A one-time investment for the air wing.',
                50, (Build('air_base', 2, 234),), requires=(Completed('air_brunies_hardstands'),)),
    DecisionDef('siren_drill', 'Sirens and Shelter Drill',
                'Every district rehearses its warning, its shelters and its trains for one day. Calms the public at the cost of a '
                'day of work.', 20, (Stability(0.02),), requires=(Completed('sky_impact_announced'),), cooldown=365),
    DecisionDef('escort_exercise', 'Escort Exercise off Bell Town',
                'The escort crews and harbour pilots rehearse closing the approaches to Bell Town and Oderin. Gains naval experience at the cost of '
                'a day of port traffic.', 25, (XP('navy', 10), Stability(-0.01)),
                requires=(Completed('prt_escort_rota'),), cooldown=180),
    DecisionDef('crossing_fair', 'License a Crossing Fair',
                'Frontier officials license a season-long fair at a crossing toward Perbla. Costs political power to organise and '
                'eases trade for a year.', 35, (TimedIdea('crossing_fair', 365),), requires=(HasFlag('gatewood_line'),)),
)
