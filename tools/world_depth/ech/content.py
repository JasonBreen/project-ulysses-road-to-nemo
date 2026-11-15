"""Echinata (ECH): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections suspended, neutrality 48 and fascism 50 percent popularity),
the unnamed starting office, the seven 1991 states with their neutral district captions,
the country names in countries_l_english.yml, and the global flags other mod scripts already
set. Official: ACES Chronicle rows used only as date anchors for distant pressures, each
cited by its exact key. Everything else, including every Echinatan choice, office, idea,
building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='ECH', name='Echinata', root='world', package='ech',
                  themes=('navy', 'tools', 'assembly'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots and '
           'tech_mountaineers. The starting leader is the unnamed National Administration office (ECH_ac_government_office, '
           'centrism), whose description says its 1991 holder has not been established. Institution profile '
           'civil_administration, capacity 40; party is context, not proof of constitutional form. Country names include '
           'the Echinatan Republic and, for the fascism party, the Echinatan People\'s State. The tree never names a holder.',
           'mod/2985041246/history/countries/ECH - Echinata.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; tools/institutions/profiles.json; '
           'tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Geography: 1991 states 56, 537, 574 (capital), 577, 579, 585 and 586, captioned Echinata District A, District B, '
           'Capital District, District D, District E, District F and District G by the neutral regional labels (canonical '
           'regional mapping unestablished). Victory points: the capital centre (405) and the logistics centres in District A '
           '(474) and District B (1390). Terrain from map/definition.csv: desert capital with no coast; jungle coast in A; '
           'plains, hills, mountain and marsh in B; marsh and plain coast in D; plain and jungle coast in E; landlocked plain, '
           'hills and mountain in F; plain and hill coast in G. All plants (9 civilian, 6 military) stand in 56, 537 and 574, '
           'which have no free shared slots; the two dockyards and the level 3 naval base are in 579; naval bases also in 56 '
           'and 577; the only air base and the fuel silo are in 574; 577, 585 and 586 have no infrastructure. Land neighbours '
           'CSO (Central Sotoa, via 537, 574 and 585), EHE (Echea, via 537) and SOA (Sotoa, via 574 and 586), computed from '
           'map/provinces.bmp. No place outside these captions is named.',
           'mod/2985041246/history/states/56-State_56.txt, 537-State_537.txt, 574-State_574.txt, 577-State_577.txt, '
           '579-State_579.txt, 585-State_585.txt, 586-State_586.txt; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role coastal service capacity; 9 civilian, 6 military and 2 naval '
           'factories; 5 infantry formations (6 battalions); 48 fighters and 12 support aircraft on one air base; 3 coastal '
           'escorts; 84 convoys; civilian economy, export focus and volunteer only laws; grand doctrines superior firepower, '
           'fleet in being and operational integrity; research priority Physical Sustainment (transport, equipment '
           'replacement, affordable service). Fictional fiscal calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; tools/world_starts/sustainment.json; docs/WORLD_STARTS_CALIBRATION.md; '
           'tools/economy_v2/profiles.json; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses will pass close to the Earth with a chance of impact. '
           'Used only as the opening of the asteroid branch; no Echinatan role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Used only as the opening of the freight branch; Echinata takes no part '
           'and no Echinatan role is claimed.', '1995 / 03.25'),
    Source('Official',
           'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Used as the date gate of the review focus.',
           '1995 / 06.20'),
    Source('Official',
           'Date anchor: the FCU announces that Ulysses will impact the Earth. Used as the date gate of the shelter focus; '
           'where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries and work as aggressor squadrons. Used '
           'as the date gate and premise of the instructor contract focus; no individual is named and no hire by Echinata '
           'is claimed as fact.', '1998 / 06.19'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Used as the date gate of the close-pass focus '
           'and event; no damage in Echinata is claimed.', '1999 / 07.08'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air '
           'batteries. Used as the opening of the Usean war branch; no Echinatan role is claimed.', '2003 / SUMMER'),
    Source('Official',
           'Farbanti falls, the ISAF accepts the Erusean surrender and the Continental War ends. Background only; the '
           'outcome focuses read the mod outcome flags instead of assuming this ending.', '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt), '
           'ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory (common/scripted_effects/ac_ucw.txt). Each '
           'reaction is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Echinatan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects; frontier and trade '
           'focuses change no claim and commit no forces abroad.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the suspended ballot
    IdeaDef('orders_review', 'Orders Under Review',
            'The emergency orders that suspend elections are being read and argued in public for the first time.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('document', 'scales')),
    IdeaDef('ballot_calendar', 'A Date on the Calendar', 'An election date is fixed and the party lists are open again.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('service_mandate', 'The Services Mandate', 'The service chiefs govern openly and publish their accounts.',
            {'political_power_gain': 0.15, 'production_factory_efficiency_gain_factor': 0.03}, ('command', 'tools')),
    IdeaDef('square_pledge', 'Pledge of the Square', 'The national movement holds the initiative in the streets and the ministries.',
            {'war_support_factor': 0.06, 'political_power_gain': 0.10, 'stability_factor': -0.02}, ('security', 'assembly')),
    IdeaDef('open_chamber', 'The Open Chamber', 'An elected chamber the coastal districts helped to choose, sitting in public.',
            {'stability_factor': 0.07, 'research_speed_factor': 0.03, 'political_power_factor': 0.05}, ('assembly', 'ballot')),
    IdeaDef('graded_service', 'Graded Public Service', 'Every post is filled by examination and a published service record.',
            {'political_power_gain': 0.20, 'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.02},
            ('document', 'training')),
    IdeaDef('state_discipline', "Discipline of the People's State", 'Wardens on every block and quotas in every plant.',
            {'war_support_factor': 0.08, 'stability_factor': 0.05, 'consumer_goods_factor': 0.04}, ('security', 'civil')),
    IdeaDef('settled_administration', 'The Ordinary Statute', 'An ordinary law on public emergencies replaces the 1991 orders.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('scales', 'peace')),
    # roads
    IdeaDef('survey_crews', 'Survey Crews in the Field', 'Engineers map every route, ford and harbour in the seven districts.',
            {'production_speed_infrastructure_factor': 0.10}, ('document', 'logistics')),
    IdeaDef('coast_road_board', 'The Coast Road Board', 'One board builds and keeps the highway that joins the port districts.',
            {'production_speed_infrastructure_factor': 0.15, 'supply_consumption_factor': -0.03}, ('logistics', 'navy')),
    IdeaDef('interior_rail_office', 'The Interior Rail Office', 'A rail office runs the line from the main port to the desert capital.',
            {'production_speed_infrastructure_factor': 0.10, 'supply_consumption_factor': -0.05}, ('rail', 'command')),
    IdeaDef('works_councils', 'District Works Councils', 'Each district owns the upkeep of the roads it was given.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.02}, ('assembly', 'tools')),
    IdeaDef('road_votes', 'Road Votes', 'District voters choose the next road project from a published list.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('ballot', 'logistics')),
    IdeaDef('open_tenders', 'Open Road Tenders', 'Every road contract is tendered in public and awarded on price and record.',
            {'production_speed_infrastructure_factor': 0.15, 'political_power_gain': 0.05}, ('scales', 'logistics')),
    IdeaDef('labour_brigades', 'Labour Brigades', 'Movement brigades grade roads on fixed quotas.',
            {'production_speed_infrastructure_factor': 0.20, 'stability_factor': -0.03}, ('tools', 'security')),
    # the coast
    IdeaDef('coaster_lines', 'The Coaster Lines', 'Old coasters, lighters and small tankers carry most freight between the districts.',
            {'naval_speed_factor': 0.03}, ('navy', 'logistics')),
    IdeaDef('state_line', 'The State Coastal Line', 'One state line runs every district harbour on a fixed timetable.',
            {'industrial_capacity_dockyard': 0.05, 'navy_org_factor': 0.04}, ('navy', 'command')),
    IdeaDef('licensed_carriers', 'Licensed Coastal Carriers', 'Private coasters trade under licence and carry state freight at set rates.',
            {'consumer_goods_factor': -0.03, 'naval_speed_factor': 0.04}, ('economy', 'navy')),
    IdeaDef('harbour_pilots', 'The Pilot Service', 'Paid pilots and apprentices keep the marsh harbour open.',
            {'naval_coordination': 0.04}, ('navy', 'training')),
    IdeaDef('escort_screen', 'The Convoy Escort Screen', 'Three escorts kept on convoy duty in fixed patrol boxes.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.04}, ('navy', 'security')),
    IdeaDef('convoy_code', 'The Coastal Convoy Code', 'Merchant masters and escorts share one signal book and one set of rules.',
            {'naval_coordination': 0.05, 'naval_speed_factor': 0.03}, ('logistics', 'communications')),
    IdeaDef('winter_convoy', 'Winter Convoy at Sea', 'The escorts shepherd the coasters through the stormy months.',
            {'navy_org_factor': 0.05, 'consumer_goods_factor': -0.02}, ('navy', 'logistics')),
    # plants
    IdeaDef('full_floors', 'Full Plant Floors', 'The three plant districts have no industrial land left to build on.',
            {'production_factory_efficiency_gain_factor': 0.03, 'production_speed_industrial_complex_factor': -0.05},
            ('industry', 'document')),
    IdeaDef('dispersal_grants', 'Dispersal Grants', 'Cheap credit and free land for plants built outside the old plant districts.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': 0.02}, ('economy', 'civil')),
    IdeaDef('refinery_towns', 'Refinery Towns', 'Small refineries near the wells turn crude into exported fuel.',
            {'industrial_capacity_factory': 0.05, 'production_speed_buildings_factor': 0.05}, ('industry', 'economy')),
    IdeaDef('light_metals', 'Home Light Metals', 'Local aluminium and steel are smelted and rolled at home.',
            {'production_factory_max_efficiency_factor': 0.05, 'industrial_capacity_dockyard': 0.04}, ('industry', 'science')),
    IdeaDef('export_ledger', 'The Export Ledger', 'Finished goods sold abroad under inspected contracts.',
            {'industrial_capacity_factory': 0.04, 'political_power_gain': 0.05}, ('economy', 'diplomacy')),
    # sustainment
    IdeaDef('parts_registry', 'The Parts Registry', 'One register of every spare part held by any service.',
            {'repair_speed_factor': 0.05}, ('tools', 'document')),
    IdeaDef('depot_workshops', 'District Depot Workshops', 'A repair workshop in every district, staffed from the services.',
            {'repair_speed_factor': 0.10, 'supply_consumption_factor': -0.03}, ('tools', 'logistics')),
    IdeaDef('standard_patterns', 'Standard Patterns', 'One approved pattern for every common part across the services.',
            {'production_factory_efficiency_gain_factor': 0.04, 'supply_consumption_factor': -0.04}, ('document', 'industry')),
    IdeaDef('open_suppliers', 'Open Suppliers', 'Equipment bought from whichever maker is cheapest and quickest.',
            {'production_speed_arms_factory_factor': 0.05, 'repair_speed_factor': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('service_college', 'The Service Engineering College', 'Engineers trained to redesign, test and certify parts.',
            {'research_speed_factor': 0.04}, ('science', 'training')),
    IdeaDef('truck_parks', 'Rebuilt Truck Parks', 'Covered parks, fuel points and a repair line for the army trucks.',
            {'army_speed_factor': 0.03, 'supply_consumption_factor': -0.03}, ('logistics', 'rebuild')),
    IdeaDef('silo_reserve', 'The Silo Reserve Rule', 'The capital silo is refilled before any export cargo is loaded.',
            {'supply_consumption_factor': -0.04, 'consumer_goods_factor': 0.02}, ('economy', 'shelter')),
    IdeaDef('long_runs', 'Long Production Runs', 'Home lines make standard spares in long runs.',
            {'production_factory_max_efficiency_factor': 0.04}, ('industry', 'tools')),
    IdeaDef('parts_catalogue', 'Catalogue of Equivalents', 'A tested list of which foreign part fits which machine.',
            {'repair_speed_factor': 0.08, 'research_speed_factor': 0.02}, ('document', 'diplomacy')),
    IdeaDef('parts_amnesty', 'Parts Amnesty', 'Hoarded spares may be returned to the depots without penalty.',
            {'repair_speed_factor': 0.10}, ('tools', 'scales')),
    # the army
    IdeaDef('battalion_rolls', 'The Battalion Rolls', 'An honest return of six volunteer battalions.',
            {'army_org_factor': 0.03}, ('training', 'document')),
    IdeaDef('frontier_rifles', 'Rifles at the Posts', 'Rifle companies live at the frontier posts and know every ford.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.03}, ('security', 'training')),
    IdeaDef('truck_reserve', 'The Motor Reserve', 'Most of the army waits in the capital district, ready to drive.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.08}, ('logistics', 'command')),
    IdeaDef('gun_doctrine', 'The Gunnery Creed', 'More guns per battalion and live fire in every exercise.',
            {'army_attack_factor': 0.04, 'experience_gain_army_factor': 0.05}, ('missile', 'training')),
    IdeaDef('hill_drill', 'Mountain Drill Season', 'A season of rope work and hill gunnery in District B.',
            {'army_org_factor': 0.04, 'experience_gain_army_factor': 0.05}, ('training', 'tools')),
    IdeaDef('reserve_law', 'The Volunteer Reserve', 'Former volunteers kept on a register with a yearly fortnight of training.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.05}, ('document', 'security')),
    # the air wing
    IdeaDef('desert_wing', 'The Desert Wing', 'Every aircraft flies from one base in the capital district.',
            {'experience_gain_air_factor': 0.04}, ('runway', 'air')),
    IdeaDef('coast_patrol', 'Coast Patrol Wing', 'Aircraft trained to find ships and cover the coasters.',
            {'air_mission_efficiency': 0.06, 'naval_coordination': 0.03}, ('air', 'navy')),
    IdeaDef('interceptor_screen', 'Capital Interceptor Screen', 'Fighters kept close to the capital, the silo and the plants.',
            {'air_superiority_efficiency': 0.06, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('engine_pool', 'The Engine Pool', 'One rotation of standard engines overhauled in one shop.',
            {'air_mission_efficiency': 0.04, 'experience_gain_air_factor': 0.05}, ('tools', 'air')),
    IdeaDef('aggressor_lessons', 'Aggressor Lessons', 'Contract instructors fly as adversaries against the wing.',
            {'experience_gain_air_factor': 0.10, 'air_superiority_efficiency': 0.03}, ('medal', 'air')),
    # the asteroid years
    IdeaDef('skywatch_bureau', 'The Skywatch Bureau', 'One office translates, checks and publishes foreign asteroid bulletins.',
            {'stability_factor': 0.02, 'air_detection': 0.03}, ('telescope', 'communications')),
    IdeaDef('district_stores', 'District Stores', 'Grain, medicine and fuel held in every district.',
            {'stability_factor': 0.04}, ('shelter', 'economy')),
    IdeaDef('scattered_stores', 'Stores in Every Town', 'Reserves kept in town halls and harbour sheds across the country.',
            {'stability_factor': 0.06, 'consumer_goods_factor': 0.02}, ('refugees', 'civil')),
    IdeaDef('capital_vault', 'The Desert Vault', 'One deep, guarded vault holds the national reserve.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('shelter', 'command')),
    IdeaDef('capital_shelters', 'Capital Shelters', 'Public shelters beneath the squares of the capital centre.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.02}, ('shelter', 'civil')),
    IdeaDef('district_wardens', 'Coastal Wardens', 'Volunteer wardens with radios and sirens in every coastal town.',
            {'stability_factor': 0.03, 'army_core_defence_factor': 0.03}, ('civil', 'communications')),
    IdeaDef('emergency_service', 'The Emergency Service', 'A standing emergency service built on the asteroid archive.',
            {'stability_factor': 0.04, 'research_speed_factor': 0.02}, ('document', 'telescope')),
    IdeaDef('drill_readiness', 'Siren Drill Readiness', 'Every district has just rehearsed its sirens and shelters.',
            {'stability_factor': 0.02, 'static_anti_air_damage_factor': 0.05}, ('civil', 'security')),
    # the Belkan War abroad
    IdeaDef('war_rates', 'War-Risk Freight', 'Foreign charterers bid high for any hull while insurers add war clauses.',
            {'industrial_capacity_dockyard': 0.04, 'consumer_goods_factor': 0.03}, ('economy', 'navy')),
    IdeaDef('neutral_hulls', 'Neutral Hulls', 'No Echinatan hull carries cargo for a belligerent.',
            {'stability_factor': 0.04, 'naval_coordination': 0.02}, ('peace', 'navy')),
    IdeaDef('wartime_charters', 'Wartime Charters', 'Owners charter hulls to any buyer outside declared war zones.',
            {'industrial_capacity_dockyard': 0.06, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('neutral_voyages', 'Voyages Under Neutral Colours', 'State hulls carry grain and medicine on neutral routes.',
            {'navy_org_factor': 0.04, 'stability_factor': 0.02}, ('navy', 'peace')),
    IdeaDef('insurance_pool', 'The Coaster Insurance Pool', 'A treasury-backed pool insures private coasters against war risk.',
            {'naval_speed_factor': 0.03, 'consumer_goods_factor': -0.02}, ('scales', 'economy')),
    IdeaDef('belkan_market', 'A Belkan Market', 'Commercial sales of fuel and metal to postwar Belka.',
            {'industrial_capacity_factory': 0.04}, ('diplomacy', 'economy')),
    IdeaDef('rebuild_contracts', 'Rebuilding Contracts', 'Small, steady contracts for fuel, shipping and repair after the war.',
            {'production_speed_buildings_factor': 0.05, 'industrial_capacity_factory': 0.03}, ('rebuild', 'diplomacy')),
    # the Usean war abroad
    IdeaDef('usean_watch', 'Watching the Usean War', 'Analysts follow the war for its effect on trade, fuel and the air.',
            {'war_support_factor': 0.03, 'air_detection': 0.03}, ('communications', 'missile')),
    IdeaDef('relief_record', 'A Record of Relief Voyages', 'Relief cargoes carried under supervision earn goodwill abroad.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('peace', 'medical')),
    IdeaDef('charter_boom', 'The Second Charter Boom', 'Wartime charter money returns to the port districts.',
            {'industrial_capacity_dockyard': 0.06, 'consumer_goods_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('fuel_windfall', 'Wartime Fuel Premium', 'Refined fuel sells abroad at a premium.',
            {'industrial_capacity_factory': 0.06, 'stability_factor': -0.01}, ('industry', 'economy')),
    IdeaDef('metal_orders', 'Distant Metal Orders', 'Rolled aluminium and steel sell to neutral yards and repair shops.',
            {'production_factory_max_efficiency_factor': 0.05, 'industrial_capacity_factory': 0.03}, ('industry', 'diplomacy')),
    IdeaDef('usean_rebuilding', 'Usean Rebuilding Trade', 'Shipping and fuel contracts in the rebuilding Usean ports.',
            {'industrial_capacity_dockyard': 0.05, 'production_speed_buildings_factor': 0.05}, ('rebuild', 'economy')),
    IdeaDef('erusean_terms', 'Commercial Terms with Erusea', 'Trade kept open without endorsing the conquest.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': -0.05}, ('diplomacy', 'scales')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('elected_council', 'Elected Council of Ministers',
           'A council of ministers drawn from the lists that win the restored ballot, governing collectively and answerable '
           'to an elected chamber. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('services_board', 'Board of the National Services',
           'A board of senior chiefs from the ports, depots, plants and frontier commands, governing collectively under a '
           'written charter while elections stay suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('state_executive', "Executive of the People's State",
           'The executive committee of the national movement, governing collectively by decree with other parties '
           'suspended. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('suspended_ballot', 'Orders Nobody Has Read', (
        "The National Administration convenes in the capital centre to hear its own emergency orders read into the record. "
        "The orders were drafted in haste to suspend elections for what was meant to be a short season, and they have been "
        "renewed quietly ever since. Few ministers have read them in full. The clerk takes most of the morning, and the "
        "public gallery fills as word spreads through the city.",
        "Outside the hall the country is split almost evenly. The national movement holds the squares and claims half of "
        "every opinion count; the non-aligned establishment of service chiefs, depot managers and harbour boards claims most "
        "of the rest. The democratic club that lent the Administration its label could fit its members in the gallery. Each "
        "camp hears in the orders what it wants to hear: a lawful pause, a stolen vote or an opportunity.",
        "The Administration cannot settle the country's future in one sitting, but it can decide what happens to the record "
        "of this one. Printing the full text will invite every camp to argue it in public. Filing it with the ministries "
        "keeps the argument quiet a while longer. Sending copies to the service chiefs and the movement's leaders at once "
        "would at least prove that nobody is being kept in the dark.",
    ), (
        Option('Print the orders in full.', (Stability(0.02), PP(-15), Event('gallery_crowds', 10))),
        Option('File them with the ministries.', (PP(35), Stability(-0.02))),
        Option('Send copies to every camp.', (PP(15), WarSupport(0.01))),
    ), picture=2),
    EventDef('gallery_crowds', 'Crowds in the Public Gallery', (
        "Ten days after the orders were printed, the public gallery of the capital centre is full every morning before the "
        "doors officially open. Students, dockworkers from District E and delegations from the movement's district branches "
        "queue in the heat to watch officials explain clauses they had forgotten writing. Newspapers print the orders beside "
        "cartoons, and radio stations on the coast read them aloud for listeners without a newspaper.",
        "The crowds are mostly orderly, but the gallery has become a stage. Movement speakers time their applause, members of "
        "the democratic club heckle, and the service chiefs send junior officers to take notes. A scuffle on the third day "
        "ends with two arrests and a long argument about whether the gallery should be closed. The ministries report that "
        "their own staff are leaving work early to join the queue.",
        "The presiding officer must set rules for the gallery before the hearings begin in earnest. Open seating keeps faith "
        "with the decision to publish and turns every hearing into theatre. Tickets drawn by lot in every district would cool "
        "the room and make the capital share its seats with the coast. Closing the gallery and broadcasting the sessions "
        "would end the crowds and the scuffles, along with the sense of being present.",
    ), (
        Option('Keep the gallery open to all.', (Stability(0.02), WarSupport(0.02))),
        Option('Draw tickets by lot in every district.', (Stability(0.03), PP(-10))),
        Option('Close the gallery and broadcast.', (PP(20), Stability(-0.01))),
    ), picture=2),
    EventDef('district_returns', 'Seven District Returns', (
        "The survey teams return to the capital with notebooks, photographs and sunburn. Three districts, the capital "
        "district, District A and District B, have graded roads, plants and logistics centres, even if the roads are older "
        "than the trucks that use them. The other four might belong to another country. District D is marsh and plain reached "
        "mostly by boat; District F is a landlocked crossroads of dirt tracks; District G has open plain and a frontier with "
        "Sotoa but no paved road.",
        "District E is the exception among the four. It holds the main naval base and the only shipyards and has roads of a "
        "sort, but they serve the port rather than the country. The survey map shows a coastal state whose interior is held "
        "together mainly by habit. Freight between the two logistics centres travels by sea, and a truck from the capital to "
        "the District G coast needs most of a week in the wet season.",
        "The engineers' report ends with two options and a warning. A coastal highway would serve the ports and the coasters; "
        "a rail line through the interior would serve the capital and the fuel silo. The country cannot afford both in this "
        "decade. The warning is that roads without maintenance last only a few seasons, and every district will ask who pays "
        "for the repairs.",
    ), (
        Option('Publish the map in every district.', (Stability(0.02), PP(-10))),
        Option('Give the report to the engineers alone.', (PP(20), Research('construction_tech', 0.5, 1))),
    ), picture=1),
    EventDef('coaster_manifests', 'What the Coasters Carry', (
        "The harbour offices finish counting the coasters, lighters and small tankers that work the Echinatan coast, and the "
        "totals surprise everyone. The country has more convoy hulls than its size suggests, most of them old, privately "
        "owned and registered under a tangle of local licences. Many are older than their masters. Together they carry the "
        "bulk of the freight that moves between the seven districts.",
        "The manifests show what the roads cannot. Fuel from the capital's wells travels by truck to the coast and then by sea "
        "to the plant districts; grain from District G sails to District A because no road goes there; machine parts leave "
        "District E for every other harbour. If the coasters stopped for a month, so would most of the economy. The navy's "
        "three escorts are all the protection they have.",
        "Owners want tax relief to replace their hulls. The navy wants the right to requisition them in a crisis. The "
        "treasury wants to know why a country with a fuel surplus pays so much to keep its shipping afloat. The ministers "
        "must decide how to present the findings: as a national asset the state must protect, or as a private trade it has "
        "neglected and must now help.",
    ), (
        Option('Call the coasters a national asset.', (WarSupport(0.02), XP('navy', 10))),
        Option('Offer the owners tax relief.', (PP(-15), Stability(0.02))),
    ), picture=0),
    EventDef('full_plants', 'No Room on the Plant Floors', (
        "The industry ministry's inspectors report that every plant in the capital district, District A and District B stands "
        "on land with no room left to grow. New machinery can replace old, but no new hall can rise without demolishing a "
        "neighbourhood. The three districts hold all of the country's factories and all of its mined oil, aluminium and "
        "steel. The other four districts hold none of either.",
        "Plant managers propose to keep investing where the workforce, the logistics centres and the sidings already are, "
        "squeezing more out of each hall. Officials from the coastal districts answer that the country has concentrated its "
        "whole industry in three places, and that any shock, from a strike to a falling sky, would stop it at once. Both "
        "sides produce charts, and both sets of charts are convincing.",
        "The cabinet has to decide which argument to back before the dispersal fund is drafted. Backing the managers means "
        "efficiency and speed now. Backing the districts means new towns, new roads and a decade of growing pains. Whatever "
        "it chooses, the export trade will keep shipping crude and ore abroad until somebody builds the plants to work them "
        "at home.",
    ), (
        Option('Back the plant managers.', (Research('industry', 0.5, 1), PP(10))),
        Option('Back the coastal districts.', (Stability(0.02), PP(-10))),
    ), picture=1),
    EventDef('parts_count', 'The Inventory Comes In', (
        "The registry teams finish the first national inventory of spare parts, and the result is both reassuring and "
        "absurd. The country owns most of the parts its services have been begging for; they are simply in the wrong place, "
        "labelled with another service's codes. An army depot in District A holds engine parts the air wing has been "
        "importing. The naval stores in District E hold truck tyres the army has been rationing.",
        "The inventory also shows how much equipment is waiting for repair rather than broken beyond it. Trucks, radios and "
        "boat engines sit in sheds for want of a single part or a mechanic trained to fit it. The government's research "
        "priority is physical sustainment, meaning transport that runs, worn equipment replaced and service the country can "
        "afford. On paper it already has the means. In practice it has three services that do not share.",
        "The ministers can order the parts redistributed at once, which will anger every service that loses stock, or create "
        "a joint office to manage them, which will take a year to build. Either way the inventory has made it impossible to "
        "pretend that the shortages were caused by a lack of money alone.",
    ), (
        Option('Redistribute the parts at once.', (Stability(-0.01), XP('army', 10), XP('air', 10))),
        Option('Build a joint parts office first.', (PP(-10), Research('logistics_tech', 0.5, 1))),
    ), picture=0),
    EventDef('battalion_returns', 'Six Battalions on the Roll', (
        "The army's first complete return in years arrives on the defence ministry's desk. Six volunteer battalions, grouped "
        "in five formations, hold three land frontiers and a long coast. Their rifles and trucks are adequate and well "
        "stored. Their soldiers are fewer than the establishment tables claim, and the shortfall is worst in the companies "
        "posted farthest from the capital district.",
        "The returns also record what the army does well. Its firepower doctrine is taken seriously, its gunners train hard, "
        "and it holds a respectable stock of motor vehicles for a small force. Its weaknesses are distance and fuel: the "
        "frontiers with Central Sotoa, Echea and Sotoa are days apart by road, and the roads are poor. A battalion sent to "
        "the wrong frontier would arrive too late to matter.",
        "The general staff asks the government how the army should be shaped for the decade ahead. One school wants "
        "companies living on the frontiers; another wants a mobile reserve in the capital district. First the ministers must "
        "decide whether the returns are published, so that recruits know what they are joining, or kept inside the ministry "
        "so that no neighbour gains an accurate count.",
    ), (
        Option('Publish the returns.', (Stability(0.01), PP(-10), XP('army', 10))),
        Option('Keep them inside the ministry.', (PP(20), WarSupport(0.01))),
    ), picture=1),
    EventDef('one_runway', 'One Runway in the Desert', (
        "The air wing's commanders bring their basing review to the defence ministry. Every fighter and support aircraft in "
        "the country flies from one base in the capital district, in the desert interior. The base is well defended and "
        "close to the fuel silo. It is also a long flight from District D, District E and District G, the coastal districts "
        "that see most of the country's shipping.",
        "The review records that most patrols over the coast spend more time in transit than on station, and that a fighter "
        "launched to meet an intruder over the main anchorage would arrive after the intruder had gone home. Pilots fly fewer "
        "hours than they should because fuel is dear and distances are long. The maintenance crews are excellent and few, "
        "and they all work in one place.",
        "The commanders propose a second field near the main naval base, and they disagree about what the wing should do "
        "once it has one. The navy wants patrol aircraft; the capital wants interceptors. The ministers must decide how much "
        "the wing may spend on runways before it has settled its own doctrine, and how long they are prepared to argue with "
        "the admirals.",
    ), (
        Option('Fund the second field first.', (XP('air', 15), PP(-10))),
        Option('Settle the doctrine first.', (PP(15), Research('air_doctrine', 0.5, 1))),
    ), picture=0),
    EventDef('asteroid_notice', "The Astronomers' Bulletin", (
        "On 10 December 1994 the International Astronomical Union announces that the asteroid Ulysses will pass close to the "
        "Earth, with a chance of impact. The news reaches Echinata as wire copy and short-wave bulletins. The country has no "
        "observatory and no space agency, and the first anxious questions arrive at the ministries before anyone there has "
        "read the bulletin in full.",
        "By the next morning the rumours have outrun the facts. Coastal towns hear that the sea will rise; the capital hears "
        "that the desert will burn. Grain and fuel prices jump in the district markets, and the movement's newspapers ask why "
        "the government has said nothing. The harbour masters of District E report families asking about passage abroad "
        "without knowing where they intend to go.",
        "The government decides to set up a small bureau to translate, check and publish the foreign bulletins, so that the "
        "country has one source of information. The ministers must decide how the bureau speaks: plainly and often, at the "
        "risk of feeding fear, or sparingly and only with confirmed facts, at the risk of leaving the rumours unanswered for "
        "days at a time.",
    ), (
        Option('Publish every bulletin plainly.', (Stability(-0.01), WarSupport(0.02))),
        Option('Speak only on confirmed facts.', (PP(15), Stability(0.01))),
    ), citation='date anchor only, ACES Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; the Echinatan response is gameplay',
        picture=2),
    EventDef('roche_night', 'The Night of the Pass', (
        "On 8 July 1999 Ulysses passes through the Roche limit of the Earth. In Echinata the government keeps every radio "
        "station on the air through the night, the wardens walk their streets and the shelters beneath the capital centre "
        "open their doors. Few people sleep. The tracking posts in the District F hills report what they can see, which is "
        "less than everyone hoped.",
        "Nothing in the bureau's bulletins says where fragments will fall, and the government does not pretend to know. What "
        "it can do is keep the stores open, the coasters in harbour and the trucks fuelled. By dawn the main concern is no "
        "longer the sky but the markets, where traders want to know whether the emergency rules on prices will stay in "
        "force.",
        "The ministers meet at first light. Keeping the emergency measures for another season would steady prices and "
        "reassure the districts, at a cost the treasury can barely carry. Lifting them at once would restore normal trade "
        "and tell the country that the government believes the worst has passed, which it cannot yet know for certain.",
    ), (
        Option('Keep the emergency measures.', (Stability(0.03), PP(-20))),
        Option('Lift them at once.', (PP(20), Stability(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no Echinatan damage is claimed',
        picture=2),
    EventDef('belkan_freight', 'Freight Quotes from a Distant War', (
        "On 25 March 1995 the Belkan War breaks out. In Echinata the first sign of it is a telex from a foreign shipbroker "
        "offering triple rates for any coaster able to cross open water. By the end of the week insurers have added war-risk "
        "clauses to every policy, fuel prices have jumped, and the harbour offices in District E are full of owners asking "
        "what the law allows them to carry.",
        "Echinata has no part in the war and no wish to acquire one. It does have a coaster fleet larger than its size "
        "suggests, a fuel surplus and a trade law that encourages selling abroad. Every one of those becomes a question "
        "overnight: who may charter Echinatan hulls, who may buy Echinatan fuel, and who will protect either if something "
        "goes wrong at sea.",
        "The government must set a shipping policy before the owners set one for it. It can forbid service to belligerents "
        "and accept the lost income, or allow charters outside declared war zones and accept the risk to its reputation. In "
        "the meantime it can at least decide whether the harbour offices publish interim rules immediately or wait for the "
        "cabinet to agree.",
    ), (
        Option('Publish interim rules at once.', (Stability(0.02), PP(-10))),
        Option('Wait for the cabinet.', (PP(15), WarSupport(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Echinatan response is gameplay',
        picture=0),
    EventDef('usean_war', 'War News from Usea', (
        "In the summer of 2003 Erusea invades the neutral country of San Salvacion and seizes Stonehenge, turning its "
        "railguns into anti-air batteries. The news reaches Echinata in fragments through the wire services, and then "
        "through the markets: fuel prices rise, shipping insurers rewrite their clauses and foreign buyers begin asking "
        "about Echinatan hulls and metals.",
        "The government has no reason to take a side and every reason to understand what the war will do to trade. The "
        "lanes that carry Echinatan exports will shift, and the countries that buy its fuel and metal will change their "
        "orders. Officials who remember the Belkan War know which questions come first: who may charter, who may buy, and "
        "who pays when a cargo is lost.",
        "The ministers must decide how loudly to speak. A public declaration of strict neutrality would reassure traders, "
        "insurers and the coaster crews. Silence would keep every option open while the course of the war is unknown. Either "
        "way, the export ledger and the coaster owners will push the government towards the money, and the harbour offices "
        "need written rules before the first charter request reaches them.",
    ), (
        Option('Declare strict neutrality.', (Stability(0.02), PP(10))),
        Option('Say nothing for now.', (PP(25), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER in tools/lore/chronicle.json; the Echinatan response is gameplay',
        picture=1),
)

# --- focuses -------------------------------------------------------------------------------------
BALLOT = Branch('ballot', 'The Suspended Ballot', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('ballot_orders', 'Read the Emergency Orders Aloud',
          "Echinata is governed by a National Administration that sits under a democratic banner while elections stay "
          "suspended under emergency orders nobody outside the ministries has read in full. Reading those orders aloud in "
          "the capital centre costs the Administration its comfortable silence, yet it is the only way to ask, in public, "
          "who should govern next.",
          ('document', 'assembly'), reward=(Idea('orders_review'), Event('suspended_ballot'))),
    Focus('ballot_hearings', 'Hearings in the Capital Centre',
          "Public hearings let every camp state its case before a panel of senior judges and career officials. The "
          "establishment of the services, the national movement that claims half the country and the tiny democratic club "
          "all receive equal time. The hearings are slow and expensive, and they make it impossible to postpone a decision "
          "any longer.",
          ('assembly', 'scales'), after=('ballot_orders',),
          reward=(PP(30), Tooltip('Opens the three answers to the suspended ballot; only one can be taken.'))),
    Focus('ballot_date', 'Name a Date for the Ballot',
          "The smallest camp makes the boldest offer: fix an election date, restore the party lists and let the voters "
          "decide what the Administration could not. The democratic club has almost no members, but many officials privately "
          "prefer a lawful vote to a crowd. Setting the date weakens the ministries at once and hands the movement a campaign "
          "it may well win.",
          ('ballot', 'document'), after=('ballot_hearings',), exclusive=('ballot_services', 'ballot_square'),
          reward=(SwapIdea('orders_review', 'ballot_calendar'),)),
    Focus('ballot_services', 'Let the Services Govern',
          "The non-aligned establishment runs the ports, the depots, the plants and the frontier posts, and it proposes to "
          "govern openly instead of through a borrowed party label. A board of senior service chiefs would hold the "
          "executive and publish its accounts while elections stay suspended. It is competent and colourless, and it asks "
          "the country to trust administrators rather than voters.",
          ('command', 'tools'), after=('ballot_hearings',), exclusive=('ballot_date', 'ballot_square'),
          reward=(SwapIdea('orders_review', 'service_mandate'),)),
    Focus('ballot_square', 'Answer the Crowds in the Square',
          "Half the country now follows a national movement that fills the squares and promises discipline, pride and an "
          "end to government by clerks. Its leaders demand the executive for themselves, without the election they might "
          "win anyway. Handing them the initiative calms the streets quickly, but every official, judge and editor who "
          "opposed them will be counted.",
          ('security', 'assembly'), after=('ballot_hearings',), exclusive=('ballot_date', 'ballot_services'),
          reward=(SwapIdea('orders_review', 'square_pledge'),)),
    Focus('ballot_council', 'Seat an Elected Council',
          "Elections are held on the promised date and the winning lists form a council of ministers answerable to an "
          "elected chamber. The change runs through the office rather than any person: the council governs collectively and "
          "can be voted out. The movement takes many seats and contests every bill, so the council governs by coalition from "
          "its first day.",
          ('ballot', 'assembly'), after=('ballot_date',), cost=10, exclusive=('ballot_board', 'ballot_executive'),
          reward=(Regime('elected_council'), Flag('path_ballot'))),
    Focus('ballot_board', 'Charter the Services Board',
          "A written charter places the executive in a board of service chiefs drawn from the ports, depots, plants and "
          "frontier commands. The board governs collectively, publishes quarterly accounts and keeps elections suspended "
          "until a review it schedules itself. Nobody voted for it, which the movement repeats daily, so the board must earn "
          "its tenure through delivery alone.",
          ('command', 'document'), after=('ballot_services',), cost=10, exclusive=('ballot_council', 'ballot_executive'),
          reward=(Regime('services_board'), Flag('path_board'))),
    Focus('ballot_executive', "Proclaim the People's State",
          "The movement's executive committee takes power and proclaims the Echinatan People's State. Parties outside the "
          "movement are suspended, the services answer to political commissioners and the press reports to a bureau. The "
          "streets go quiet and the plants meet their quotas, while trading partners abroad watch the new government very "
          "carefully and price the risk into every contract.",
          ('security', 'command'), after=('ballot_square',), cost=10, exclusive=('ballot_council', 'ballot_board'),
          reward=(Regime('state_executive'), Flag('path_movement'))),
    Focus('ballot_boat_polls', 'Polling Stations Afloat',
          "District D and District G have almost no roads, so their voters have never reached a polling station without a "
          "day on foot. The electoral office charters coasters as floating polling stations that call at every harbour and "
          "landing. Turnout on the coast doubles, the council gains a legitimacy the capital alone could not give it, and the "
          "bill falls on the transport budget.",
          ('ballot', 'navy'), after=('ballot_council',), reward=(SwapIdea('ballot_calendar', 'open_chamber'),)),
    Focus('ballot_grades', 'Graded Examinations for Officials',
          "The board replaces patronage with graded examinations for every post from harbour clerk to deputy minister. "
          "Promotions follow scores and service records, published district by district. Old networks lose their hold on the "
          "depots, and capable officials from the coastal districts finally rise. The examinations are slow to organise, and "
          "the people they displace do not forgive easily.",
          ('document', 'training'), after=('ballot_board',), reward=(SwapIdea('service_mandate', 'graded_service'),)),
    Focus('ballot_wardens', 'Block Wardens of the Movement',
          "The executive appoints a warden for every block of flats and every village, responsible for ration cards, siren "
          "drills and reports on dissent. The wardens make the state visible in places the old Administration never reached. "
          "They also make neighbours wary of each other, and a country that informs on itself soon stops telling its rulers "
          "anything uncomfortable.",
          ('security', 'civil'), after=('ballot_executive',), reward=(SwapIdea('square_pledge', 'state_discipline'),)),
    Focus('ballot_orders_lapse', 'The Emergency Orders Lapse',
          "By the millennium the emergency orders of 1991 have outlived their purpose under every kind of government. Letting "
          "them lapse formally, and replacing them with an ordinary statute on public emergencies, ends a decade of "
          "improvisation. Whoever governs loses a convenient tool, but courts, investors and district officials finally know "
          "which rules will still apply next year.",
          ('peace', 'document'), after_any=('ballot_boat_polls', 'ballot_grades', 'ballot_wardens'),
          requires=(After('2000.1.1'),), reward=(Idea('settled_administration'), Stability(0.03))),
))

ROADS = Branch('roads', 'Roads for the Unpaved Districts', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('roads_survey', 'Survey the Seven Districts',
          "Echinata has seven districts and only three of them have anything like a road network. District D, District F "
          "and District G appear on the map as blank interiors crossed by tracks. A survey of every route, ford and harbour "
          "costs a season of work by engineers the army would rather keep, but no road can be built without it.",
          ('document', 'civil'), reward=(Idea('survey_crews'), Event('district_returns'))),
    Focus('roads_f_crossroads', 'Grade the District F Crossroads',
          "District F is landlocked, part plain and part hill, and touches five of the other districts, so nearly every overland "
          "journey across the country passes through it on dirt. Grading its central crossroads and gravelling the approaches "
          "is cheap engineering with an outsized effect. The district also borders Central Sotoa, and its customs huts have "
          "never had a paved approach.",
          ('logistics', 'tools'), after=('roads_survey',), reward=(Build('infrastructure', 1, 585),)),
    Focus('roads_d_causeway', 'Causeways Across the D Marshes',
          "District D is half marsh and half plain, and its coastal villages travel by boat because carts sink. Raised "
          "causeways between the harbour and the plain villages turn a three-day trip into an afternoon. Causeways cost a "
          "great deal per kilometre and flood in the worst seasons, but they are the first road the district has ever had.",
          ('bridge', 'civil'), after=('roads_survey',), reward=(Build('infrastructure', 1, 577),)),
    Focus('roads_g_plains', 'A Plains Road Through District G',
          "District G is open plain and low hills along the coast, facing Sotoa across a frontier of fields. Its farms sell "
          "to whichever buyer can reach them, which is usually a foreign one. A graded plains road from its coast to the "
          "capital district brings its produce into the national market and gives the government a reason to be seen there.",
          ('logistics', 'civil'), after=('roads_survey',), reward=(Build('infrastructure', 1, 586),)),
    Focus('roads_coast_highway', 'One Highway Along the Coast',
          "The first answer to the road budget is a coastal highway linking the port districts in one chain, from the "
          "jungle coast of District A to the plains of District G. It serves the harbours, the fishing towns and the coaster "
          "trade. It also leaves the interior on dirt tracks for another decade, and the capital district complains loudly.",
          ('logistics', 'navy'), after_any=('roads_d_causeway', 'roads_g_plains'), cost=10, exclusive=('roads_interior_rail',),
          reward=(SwapIdea('survey_crews', 'coast_road_board'), Flag('roads_coastal'))),
    Focus('roads_interior_rail', 'Rails Through the Interior',
          "The second answer runs a railway from the main port in District E through the District F crossroads to the "
          "desert capital, carrying fuel, ore and equipment overland. Rail suits the sustainment mission and the rolling "
          "stock the army already holds. It costs more than any road, it serves fewer towns, and the coastal districts see "
          "none of it.",
          ('rail', 'industry'), after=('roads_f_crossroads',), cost=10, exclusive=('roads_coast_highway',),
          reward=(SwapIdea('survey_crews', 'interior_rail_office'), Flag('roads_rail'))),
    Focus('roads_highway_bridges', 'Bridges for the Coast Highway',
          "The coast highway crosses every creek and estuary between the port districts, and ferries still carry trucks over "
          "the widest of them. Replacing the ferries with low bridges in District D and District G closes the last gaps. "
          "Engineers warn that storm surges will test every span, so the bridge office spends on deep foundations rather "
          "than length.",
          ('bridge', 'navy'), after=('roads_coast_highway',),
          reward=(Build('infrastructure', 1, 577), Build('infrastructure', 1, 586))),
    Focus('roads_rail_spur', 'A Spur to the Capital Silo',
          "The interior line ends in the capital district, where the national fuel silo and the only air base stand. A "
          "short spur straight into the silo yard lets tank wagons unload without trucks. The railway also opens a "
          "locomotive workshop that trains the first generation of national rail mechanics. The spur costs little; the "
          "workshop costs a great deal.",
          ('rail', 'tools'), after=('roads_interior_rail',),
          reward=(Build('infrastructure', 1, 0), Research('train_tech', 0.5, 1))),
    Focus('roads_logistics_link', 'Link the Two Logistics Centres',
          "The logistics centres in District A and District B were built to supply garrisons, not each other, and freight "
          "between them still goes by sea. Paving the roads that lead out of both, whatever shape the main network takes, "
          "joins the two oldest industrial districts by land. It is mostly gravel and culverts, and it ends a quiet rivalry "
          "between their depot chiefs.",
          ('logistics', 'rail'), after_any=('roads_highway_bridges', 'roads_rail_spur'),
          reward=(Build('infrastructure', 1, 56), Build('infrastructure', 1, 537))),
    Focus('roads_works_councils', 'Works Councils in Every District',
          "With a skeleton network finally in place, each district receives a standing works council with its own road "
          "budget and a duty to maintain what was built. Maintenance is the dull half of every road programme and the half "
          "most governments forget. The councils argue with the capital over money every year, but potholes now have an "
          "owner.",
          ('assembly', 'tools'), after=('roads_logistics_link',), reward=(Idea('works_councils'),)),
    Focus('roads_votes', 'Road Votes in the Districts',
          "Under the elected council, each district votes on its next road project from a list the engineers have costed. "
          "Turnout is low and the campaigns are fierce, especially in District F, where every village wants the next "
          "junction. The votes slow the programme for a season and leave every finished road with a constituency that "
          "defends its upkeep.",
          ('ballot', 'logistics'), after=('roads_works_councils',), requires=(HasFlag('path_ballot'),),
          reward=(TimedIdea('road_votes', 730), Build('infrastructure', 1, 585))),
    Focus('roads_tenders', 'Road Contracts by Open Tender',
          "The services board puts every road contract out to public tender, with the price, the winner and the engineer's "
          "inspection report printed in the official gazette. Contractors with friends in the old ministries lose work to "
          "cheaper firms from the coastal districts. Roads get built faster and slightly worse, and the board publishes that "
          "too.",
          ('scales', 'logistics'), after=('roads_works_councils',), requires=(HasFlag('path_board'),),
          reward=(TimedIdea('open_tenders', 730), PP(20))),
    Focus('roads_brigades', 'Movement Labour Brigades',
          "The People's State raises labour brigades of young movement members to grade roads on fixed quotas, housed in "
          "camps along the routes. The brigades are fast, cheap and loud with slogans. Their roads are rougher than an "
          "engineer would accept, and farmers whose fields are crossed without compensation remember who sent the brigades.",
          ('tools', 'security'), after=('roads_works_councils',), requires=(HasFlag('path_movement'),),
          reward=(TimedIdea('labour_brigades', 365), Build('infrastructure', 1, 585))),
))

COAST = Branch('coast', 'The Coastal Service', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('coast_cargoes', 'Count the Coaster Cargoes',
          "Echinata moves more of its freight by sea than by land, on a fleet of coasters, lighters and small tankers that "
          "call at every district harbour. Nobody has counted what they carry, who owns them or how old they are. A full "
          "count costs the harbour offices a year of paperwork and tells the government whether its coastal service is a "
          "fleet or a museum.",
          ('navy', 'document'), reward=(Idea('coaster_lines'), Event('coaster_manifests'))),
    Focus('coast_e_yards', 'Overhaul the District E Yards',
          "The main naval base in District E holds the country's only shipyards: two slipways working at half pace with "
          "machine tools older than their crews. Overhauling them and adding a third slip lets the yards keep the coaster "
          "fleet and the escorts working at once. The money comes out of the plant budget, and the inland districts notice.",
          ('tools', 'navy'), after=('coast_cargoes',), reward=(Build('dockyard', 1, 579),)),
    Focus('coast_pilots', 'Pilots for the Marsh Harbour',
          "The District D harbour sits behind shifting mudbanks that only local pilots know, and half of them are close to "
          "retirement. A pilot service with apprentices, charts and paid stations keeps the marsh coast open to the coasters "
          "and to the navy's escorts. It is a small investment in people rather than steel, and it pays only if the harbour "
          "stays busy.",
          ('navy', 'training'), after=('coast_cargoes',), reward=(TimedIdea('harbour_pilots', 730), XP('navy', 10))),
    Focus('coast_state_line', 'A State Coastal Line',
          "The government buys out the ageing private coasters and runs them as one state line on fixed timetables between "
          "every district harbour. Freight costs become predictable, the yards gain steady orders and the navy can "
          "requisition hulls in a crisis. The line will lose money in its first years, and owners who sold to it will "
          "lobby against it for decades.",
          ('navy', 'command'), after_any=('coast_e_yards', 'coast_pilots'), cost=10, exclusive=('coast_licensed',),
          reward=(SwapIdea('coaster_lines', 'state_line'), Flag('coast_state'))),
    Focus('coast_licensed', 'License the Private Coasters',
          "The alternative keeps the coasters private but licenses them, setting safety rules, insurance minimums and a duty "
          "to carry state freight at agreed rates. Owners keep their profits and their freedom to trade abroad, and the "
          "treasury pays nothing up front. The coast stays served by whoever finds it profitable, which leaves the poorest "
          "harbours waiting longest.",
          ('economy', 'navy'), after_any=('coast_e_yards', 'coast_pilots'), cost=10, exclusive=('coast_state_line',),
          reward=(SwapIdea('coaster_lines', 'licensed_carriers'), Flag('coast_private'))),
    Focus('coast_escorts', 'Three Escorts, One Coastline',
          "The navy has three escorts to guard a coastline that runs past five districts, and its doctrine already assumes "
          "it will never meet a battle fleet. Concentrating the escorts on convoy duty, with fixed patrol boxes off the main "
          "harbours, turns the fleet's weakness into a routine. The admirals lose their dream of cruisers, and the coasters "
          "gain a predictable guard.",
          ('navy', 'security'), after=('coast_cargoes',), reward=(Idea('escort_screen'), XP('navy', 15))),
    Focus('coast_d_slipway', 'A Slipway in District D',
          "The state line needs a second repair yard closer to the marsh harbour, so that its coasters stop sailing to "
          "District E for every refit. A slipway and workshop beside the District D naval base costs the line a year of "
          "profits. It also brings the first industrial wages the district has ever seen, which the line advertises heavily.",
          ('rebuild', 'navy'), after=('coast_state_line',), reward=(Build('dockyard', 1, 577),)),
    Focus('coast_g_slips', 'Private Slips on the G Coast',
          "Licensed owners pool their money for a repair yard on the District G coast, near the farms that fill their holds. "
          "The government offers the land and a tax holiday in exchange for a duty to repair the escorts at cost. The yard "
          "is small and privately run, and it gives the plains coast its first industrial anchor.",
          ('economy', 'tools'), after=('coast_licensed',), reward=(Build('dockyard', 1, 586),)),
    Focus('coast_convoy_code', 'A Code for Coastal Convoys',
          "Every coaster master, state or private, receives the same signal book, the same convoy rules and the same radio "
          "frequencies as the escorts. Night drills off the main port teach merchant crews to keep station without lights. "
          "It costs little but time, and in any future crisis the navy and the merchant fleet will already speak one "
          "language.",
          ('logistics', 'navy'), after_any=('coast_d_slipway', 'coast_g_slips'), reward=(Idea('convoy_code'),)),
    Focus('coast_anchorage_radar', 'Radar Over the Main Anchorage',
          "The anchorage at the District E base has no radar beyond what the escorts carry, so ships approaching at night "
          "are seen only when they are close. A shore radar on the headland gives the harbour command hours of warning and a "
          "picture of coastal traffic. It is the first permanent sensor on the coast, and the air staff wants its feed too.",
          ('radar', 'navy'), after=('coast_escorts',),
          reward=(Build('radar_station', 1, 579), Research('naval_equipment', 0.5, 1))),
))

PLANTS = Branch('plants', 'Beyond the Three Plant Districts', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('plants_full', 'No Free Floor in the Plant Districts',
          "Every plant Echinata owns stands in the capital district, District A or District B, and each of those districts "
          "has filled its industrial land. New machinery can only replace old machinery there, and the other four districts "
          "have no plants at all. Admitting that growth must happen elsewhere is the first step, and the established plant "
          "towns hate hearing it.",
          ('industry', 'document'), reward=(Idea('full_floors'), Event('full_plants'))),
    Focus('plants_grants', 'Grants to Build Beyond the Three',
          "A dispersal fund offers cheap credit and free land to any firm that builds outside the three plant districts. "
          "Managers grumble about moving away from the old logistics centres, and the fund draws money from the established "
          "towns. In exchange the country gains new industrial towns, which are also harder to stop with a single strike or "
          "disaster.",
          ('economy', 'civil'), after=('plants_full',), reward=(SwapIdea('full_floors', 'dispersal_grants'),)),
    Focus('plants_f_works', 'A Works Town at the Crossroads',
          "District F sits at the junction of every overland route, which makes it the natural home of the first new works "
          "town. Its land is cheap, its hills give shelter and its people need wages. The first plant there makes pumps, "
          "pipes and truck parts for the rest of the country, though everything it needs still arrives over unfinished roads.",
          ('industry', 'logistics'), after=('plants_grants',), reward=(Build('industrial_complex', 1, 585),)),
    Focus('plants_e_shops', 'Machine Shops Beside the E Yards',
          "The main port district has shipyards but no machine shops, so every part the yards need is ordered from the "
          "capital and shipped back down the coast. A machine shop beside the yards cuts that journey to the length of a "
          "street. It takes the last free industrial land at the port, which the harbour masters had hoped to keep for "
          "warehouses.",
          ('tools', 'industry'), after=('plants_grants',), reward=(Build('industrial_complex', 1, 579),)),
    Focus('plants_d_works', 'Workshops for the Marsh Coast',
          "District D has a naval base, a harbour and almost nothing else. A cluster of workshops making nets, small engines "
          "and boat fittings for the coasters gives the marsh villages wages that do not depend on the season. The workshops "
          "are modest and slow to pay back, but they are the first step towards District D sharing in the national economy.",
          ('tools', 'civil'), after_any=('plants_f_works', 'plants_e_shops'), reward=(Build('industrial_complex', 1, 577),)),
    Focus('plants_refining', 'Refinery Towns',
          "Oil comes out of the ground in all three plant districts and leaves the country mostly as crude. The refining "
          "model builds small refineries near the wells and in the new works towns, so that Echinata exports fuel rather "
          "than crude and keeps the margin. Refineries are dirty, slow to build and exposed to price swings, and they make "
          "the country a fuel seller.",
          ('industry', 'economy'), after_any=('plants_f_works', 'plants_e_shops'), cost=10, exclusive=('plants_metals',),
          reward=(Idea('refinery_towns'), Flag('model_refining'))),
    Focus('plants_metals', 'Light Metals from Local Ore',
          "Aluminium ore and steel are mined beside the oil, and both leave the country unworked. The light-metals model "
          "puts the credit into smelting and rolling, feeding the yards, the truck lines and eventually aircraft repair. "
          "Smelters swallow electricity and skilled workers, and the payoff takes most of a decade, but the metal stays at "
          "home.",
          ('industry', 'science'), after_any=('plants_f_works', 'plants_e_shops'), cost=10, exclusive=('plants_refining',),
          reward=(Idea('light_metals'), Flag('model_metals'))),
    Focus('plants_highway_plant', 'Plants Along the New Highway',
          "With the coast highway open, firms can build along it and ship by road or by sea. The dispersal fund pays for a "
          "plant on the District G coast where the highway meets the farmland. It is cheaper than building inland because "
          "materials arrive by coaster, and it ties a frontier district to the national economy.",
          ('industry', 'navy'), after=('plants_grants',), requires=(HasFlag('roads_coastal'),),
          reward=(Build('industrial_complex', 1, 586),)),
    Focus('plants_railhead', 'A Plant at the Railhead',
          "The interior line brings fuel, ore and machines to the District F crossroads by the trainload. A second plant "
          "beside the railhead uses that advantage to assemble trucks and rolling stock for the line itself. Railway towns "
          "grow fast and loud, and this one will need housing, schools and a police post the district never budgeted for.",
          ('rail', 'industry'), after=('plants_grants',), requires=(HasFlag('roads_rail'),),
          reward=(Build('industrial_complex', 1, 585),)),
    Focus('plants_exports', 'Finished Goods for Export',
          "The trade law already favours exports, but the country exports crude and ore. Contracts for finished goods, "
          "refined fuel or rolled metal depending on the model chosen, earn foreign currency at better margins. Buyers demand "
          "quality checks the plants have never had to pass, so the first contracts arrive with inspectors and penalty "
          "clauses.",
          ('economy', 'diplomacy'), after_any=('plants_refining', 'plants_metals'), reward=(Idea('export_ledger'),)),
))

SUSTAIN = Branch('sustain', 'Physical Sustainment', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('sus_count', 'Count Every Spare Part',
          "The army, the navy and the air wing all report shortages of parts that turn out to be sitting in another "
          "service's depot. A national registry of every spare part, engine and tyre held anywhere in the country costs "
          "months of inventory work. It reveals what the services really own and makes the case for sustainment as one "
          "national programme rather than three quarrels.",
          ('tools', 'document'), reward=(Idea('parts_registry'), Event('parts_count'))),
    Focus('sus_depots', 'Depot Workshops in Each District',
          "Equipment that breaks in District G is hauled to the capital for repair, because no other district has a "
          "workshop able to do the job. A depot workshop in each district, staffed by technicians from the services, keeps "
          "trucks, boats and radios working where they are. It adds a payroll the treasury did not plan for and saves many "
          "long journeys.",
          ('tools', 'logistics'), after=('sus_count',), reward=(SwapIdea('parts_registry', 'depot_workshops'),)),
    Focus('sus_one_pattern', 'One Pattern for Every Part',
          "The standardising school wants one approved pattern for every common part: one truck, one radio and one engine "
          "family across the services. Home plants could then make the parts in long runs, and mechanics would learn a "
          "single system. Standardisation costs years of procurement discipline and offends every service that likes its "
          "own equipment.",
          ('document', 'industry'), after=('sus_depots',), exclusive=('sus_any_maker',),
          reward=(Idea('standard_patterns'), Flag('parts_standard'))),
    Focus('sus_any_maker', 'Buy From Any Maker',
          "The pragmatic school argues that a small country cannot dictate patterns to the world's manufacturers. It would "
          "buy whatever is cheapest and available, and keep a catalogue of interchangeable parts from many makers. The "
          "services get equipment faster and cheaper, at the price of mechanics who must know a dozen systems.",
          ('economy', 'diplomacy'), after=('sus_depots',), exclusive=('sus_one_pattern',),
          reward=(Idea('open_suppliers'), Flag('parts_mixed'))),
    Focus('sus_college', 'A College for Service Engineers',
          "Echinata has mechanics but few engineers who can redesign a part, test a substitute or certify a repair. A "
          "service engineering college attached to the capital's plants trains them for all three services and the civil "
          "depots. It takes a decade to repay its cost, and its first graduates are quickly hired away by exporters.",
          ('science', 'training'), after=('sus_count',), reward=(Idea('service_college'), Research('engineers_tech', 0.5, 1))),
    Focus('sus_truck_parks', 'Rebuild the Truck Parks',
          "The army keeps its trucks in open parks where half of them wait for parts and the rest wait for drivers. "
          "Rebuilding the parks with covered sheds, fuel points and a dedicated repair line returns most of the fleet to "
          "service. Drivers and mechanics are scarce in a volunteer army, so the parks also become the army's first trade "
          "school.",
          ('logistics', 'rebuild'), after=('sus_depots',),
          reward=(TimedIdea('truck_parks', 730), Research('logistics_tech', 0.5, 1))),
    Focus('sus_silo', 'Keep the Capital Silo Full',
          "The single fuel silo in the capital district is the reserve for the trucks, the aircraft and the escorts, and it "
          "is rarely more than half full. A standing rule obliges the state oil buyers to refill it before any export cargo "
          "is loaded. Exporters lose some sales in tight months, while the services finally gain the fuel to train and move.",
          ('economy', 'shelter'), after=('sus_truck_parks',), reward=(Idea('silo_reserve'),)),
    Focus('sus_home_lines', 'Home Lines for Standard Parts',
          "With the patterns fixed, the plants in the three industrial districts retool lines to make spares in long runs "
          "instead of single batches. Domestic supply replaces many imports, and lead times fall from months to weeks. The "
          "retooling interrupts normal production for a season and binds the services to the chosen patterns for years.",
          ('industry', 'tools'), after=('sus_one_pattern',),
          reward=(TimedIdea('long_runs', 730), Research('industry', 0.5, 1))),
    Focus('sus_equivalents', 'A Catalogue of Equivalents',
          "Buying from many makers only works if mechanics know which foreign part fits which machine. A central catalogue "
          "of tested equivalents, updated every quarter and copied to every depot, turns a jumble of suppliers into a usable "
          "market. Testing costs money and the occasional ruined engine, but it ends a great deal of guesswork.",
          ('document', 'diplomacy'), after=('sus_any_maker',),
          reward=(TimedIdea('parts_catalogue', 730), Research('electronics', 0.5, 1))),
))

ARMY = Branch('army', 'The Six Battalions', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('army_returns', 'The Battalion Returns',
          "The army is six volunteer battalions spread across three land frontiers and five coastal districts, and its "
          "returns are years out of date. A full return of soldiers, weapons, trucks and training records shows what the "
          "battalions can really do. The answer is unflattering, but it ends the habit of planning with units that exist "
          "only on paper.",
          ('training', 'document'), reward=(Idea('battalion_rolls'), Event('battalion_returns'))),
    Focus('army_frontiers', 'Three Frontiers, Six Battalions',
          "Echinata borders Central Sotoa, Echea and Sotoa, and its frontiers cross desert, hills and plain where customs "
          "huts are the only sign of the state. Assigning each battalion a frontier sector, with a passable road to its post, "
          "gives the army a map of its duties. It changes no claim on either side, and it leaves the coast almost unguarded.",
          ('security', 'logistics'), after=('army_returns',), reward=(Build('infrastructure', 1, 537), XP('army', 10))),
    Focus('army_rifles', 'Frontier Rifle Companies',
          "The first school would split the battalions into rifle companies living at the frontier posts, knowing every ford "
          "and hill. They would hold ground and watch the crossings without needing trucks or fuel. Companies tied to one "
          "post are hard to move in a crisis elsewhere, and soldiers posted for years in the desert tend to leave the army.",
          ('security', 'training'), after=('army_frontiers',), exclusive=('army_motor',),
          reward=(SwapIdea('battalion_rolls', 'frontier_rifles'),)),
    Focus('army_motor', 'A Motor Reserve at the Capital',
          "The second school keeps most of the army in a motorised reserve in the capital district, using the trucks "
          "already in stock, with only observation posts at the frontiers. The reserve can reach any district within days "
          "if the roads hold. It burns fuel the country could export, and it leaves the frontiers watched rather than held.",
          ('logistics', 'command'), after=('army_frontiers',), exclusive=('army_rifles',),
          reward=(SwapIdea('battalion_rolls', 'truck_reserve'),)),
    Focus('army_guns', 'More Guns per Battalion',
          "The army's doctrine already favours firepower over manpower, which suits a country with few soldiers. Turning "
          "that preference into practice means more guns per battalion, live-fire training and an artillery school. Shells "
          "are expensive, so every exercise becomes a budget argument, but a small army that hits hard is taken seriously.",
          ('missile', 'training'), after=('army_returns',), reward=(Idea('gun_doctrine'), Research('artillery', 0.5, 1))),
    Focus('army_hills', 'Mountain Drill in District B',
          "District B and District F hold the only mountains and hills in the country, and the army keeps mountaineering "
          "instructors on its books with little use for them. A season of mountain drill in District B each year teaches "
          "rope work, hill gunnery and night marches. The drill is cheap and popular with recruits, and hard on the old "
          "trucks.",
          ('training', 'tools'), after=('army_guns',), reward=(TimedIdea('hill_drill', 365), XP('army', 10))),
    Focus('army_sotoa_posts', 'Posts on the Sotoa Frontier',
          "The rifle companies on the District G frontier with Sotoa live in tents and rented farmhouses. Permanent posts "
          "with barracks, wells and a road to the coast make the posting bearable. The posts claim nothing beyond the line "
          "and coordinate openly with the customs service, but they make the frontier a place where the state actually lives.",
          ('security', 'civil'), after=('army_rifles',), reward=(Build('infrastructure', 1, 586), Stability(0.02))),
    Focus('army_motor_depot', 'A Motor Depot for the Reserve',
          "A reserve that moves by truck needs its own workshops, fuel and spares close at hand. A motor depot with a small "
          "assembly line at the District F crossroads, a day's drive from every district, refurbishes trucks and makes spare "
          "parts for the reserve. It takes industrial land the works town wanted, and the reserve's fuel bill rises again.",
          ('logistics', 'industry'), after=('army_motor',), reward=(Build('arms_factory', 1, 585),)),
    Focus('army_reserve_law', 'A Volunteer Reserve Law',
          "Every soldier who leaves the battalions is lost to the army the day the kit is handed in. A reserve law keeps "
          "former volunteers on a register with a yearly fortnight of training and a modest retainer. The reserve costs a "
          "steady sum each year and gives a small army a second line it could not otherwise afford.",
          ('document', 'security'), after_any=('army_sotoa_posts', 'army_motor_depot'), reward=(Idea('reserve_law'),)),
))

AIR = Branch('air', 'The Desert Airfield', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_runway', 'One Runway for Seven Districts',
          "The air wing flies its fighters and support aircraft from a single base in the desert capital district, far from "
          "the coast it is meant to protect. Every patrol over District D or District G spends most of its fuel getting "
          "there. Reviewing the wing's basing costs nothing but pride, and it opens a long argument about where aircraft "
          "belong.",
          ('runway', 'air'), reward=(Idea('desert_wing'), Event('one_runway'))),
    Focus('air_port_field', 'A Field Beside the Main Port',
          "A second air base beside the District E naval base puts aircraft within minutes of the main anchorage and the "
          "busiest coastal lanes. Land is found on the plain behind the port, and the runway is laid in a season. The "
          "capital loses its monopoly on the air wing, and the navy gains neighbours it must learn to share fuel with.",
          ('runway', 'navy'), after=('air_runway',), reward=(Build('air_base', 2, 579),)),
    Focus('air_patrol', 'Coast Patrol Squadrons',
          "One answer reshapes the air wing around the sea: support aircraft and fighters trained to find ships, escort "
          "convoys and cover the coasters. Patrol work is long, dull and hard on airframes, and it suits a navy built to "
          "stay in being rather than to fight. The capital's skies would be guarded by radar and little else.",
          ('air', 'navy'), after=('air_port_field',), exclusive=('air_intercept',),
          reward=(SwapIdea('desert_wing', 'coast_patrol'),)),
    Focus('air_intercept', 'Interceptors for the Capital',
          "The other answer keeps the fighters at home, quick to climb and close to the capital, the silo and the plant "
          "districts they protect. Interception needs radar, fast alerts and well-trained pilots rather than long-range "
          "endurance. The coast would see the wing's aircraft only when an emergency justified the fuel.",
          ('air', 'radar'), after=('air_port_field',), exclusive=('air_patrol',),
          reward=(SwapIdea('desert_wing', 'interceptor_screen'),)),
    Focus('air_frontier_radar', 'Radar on the District B Hills',
          "The hills of District B look over the frontiers with Central Sotoa and Echea, and a radar there sees further than "
          "any post in the desert. The station gives the air wing early warning on the land approaches and some coverage of "
          "the coast. Its technicians complain that the hills have no road worth the name.",
          ('radar', 'security'), after=('air_runway',), reward=(Build('radar_station', 1, 537), XP('air', 10))),
    Focus('air_engine_pool', 'One Engine Pool for the Wing',
          "With standard patterns adopted across the services, the air wing pools its engines in one rotation, overhauled in "
          "one shop. Aircraft spend fewer days grounded waiting for parts, and mechanics specialise. The pool is efficient "
          "and fragile, because one bad batch of engines can ground the whole wing at once.",
          ('tools', 'air'), after_any=('air_patrol', 'air_intercept'), requires=(HasFlag('parts_standard'),),
          reward=(TimedIdea('engine_pool', 730), XP('air', 10))),
    Focus('air_two_shops', 'Two Shops for Two Engines',
          "Buying from many makers left the wing with two engine families and no shared tooling. Rather than force one out, "
          "the wing adds a second maintenance shop and hardstands at the capital base, each shop keeping one family. "
          "Duplication costs money, but it means no single fault can ground every aircraft at the same time.",
          ('tools', 'runway'), after_any=('air_patrol', 'air_intercept'), requires=(HasFlag('parts_mixed'),),
          reward=(Build('air_base', 1, 0), XP('air', 15))),
    Focus('air_aggressors', 'Contract Aggressor Instructors',
          "Former top pilots of the Belkan Air Force now work for various countries as aggressor squadrons, and the air "
          "staff asks whether Echinata should hire such instructors. A contract would bring hard training against "
          "experienced adversaries. The price is high and the instructors bring their own loyalties, so any contract is short "
          "and closely supervised.",
          ('medal', 'air'), after=('air_runway',), requires=(After('1998.6.19'),),
          reward=(TimedIdea('aggressor_lessons', 365), XP('air', 20))),
))

SKY = Branch('sky', 'The Asteroid Years', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_notice', "Read the Astronomers' Notice",
          "The International Astronomical Union warns that the asteroid Ulysses will pass close to the Earth with a chance "
          "of impact. Echinata has no observatory of its own and learns everything from foreign bulletins. A small bureau to "
          "translate, check and publish those bulletins costs little, and it gives the public one source instead of a "
          "hundred rumours.",
          ('meteor', 'telescope'), requires=(After('1994.12.10'),),
          reward=(Idea('skywatch_bureau'), Event('asteroid_notice'))),
    Focus('sky_stores', 'Grain and Fuel in Every District',
          "If the worst forecasts come true, roads may close and harbours may silt, and every district will need to feed "
          "itself for weeks. A stockpile of grain, medicine and fuel in each district costs a great deal to fill and keep. "
          "It is also the most visible thing the government can do, and visibility is what frightened people ask for.",
          ('shelter', 'economy'), after=('sky_notice',), reward=(Idea('district_stores'),)),
    Focus('sky_scatter', 'Scatter the Stores to the Towns',
          "One school would scatter the reserves into every town hall and harbour shed, so that nothing depends on a single "
          "depot. Dispersal means more theft, more spoilage and more clerks to count it all. It also means that a town cut "
          "off from the capital can still feed itself, which matters most in the roadless districts.",
          ('refugees', 'civil'), after=('sky_stores',), exclusive=('sky_vault',),
          reward=(SwapIdea('district_stores', 'scattered_stores'),)),
    Focus('sky_vault', 'One Deep Vault in the Desert',
          "The other school would dig one deep, guarded vault in the desert of the capital district, holding the national "
          "reserve under a single command. One vault is cheaper, easier to guard and harder to steal from. Its contents "
          "reach the coast only if the roads and the coasters still work when they are needed.",
          ('shelter', 'command'), after=('sky_stores',), exclusive=('sky_scatter',),
          reward=(SwapIdea('district_stores', 'capital_vault'),)),
    Focus('sky_shelters', 'Shelters Beneath the Capital Centre',
          "Once the FCU announces that Ulysses will strike the Earth, the capital centre begins digging public shelters "
          "beneath its squares and government buildings. Engineers reinforce cellars, stock them and mark the routes. The "
          "work disrupts the city for years and costs a fortune, and nobody can say how much of it will be needed.",
          ('shelter', 'civil'), after=('sky_notice',), requires=(After('1996.4.20'),), reward=(Idea('capital_shelters'),)),
    Focus('sky_wardens', 'Wardens for the Coastal Towns',
          "The coastal towns are the hardest to warn: scattered, roadless and linked mostly by radio. A corps of volunteer "
          "wardens with radios, sirens and evacuation plans gives each town a person responsible for acting when the warning "
          "comes. Wardens are unpaid and keen at first, and tired after a few years of drills.",
          ('civil', 'communications'), after=('sky_stores',), reward=(Idea('district_wardens'),)),
    Focus('sky_tracking', 'Tracking Posts in the District F Hills',
          "The hills of District F give a clear horizon far from coastal haze, and the bureau sets up tracking posts there "
          "with telescopes, radar and radio links to the capital. The posts confirm foreign bulletins and watch the night "
          "sky for fragments. They also give the air wing a radar picture over the interior.",
          ('telescope', 'radar'), after=('sky_notice',), reward=(Build('radar_station', 1, 585),)),
    Focus('sky_close_pass', 'The Night of the Close Pass',
          "Ulysses passes through the Roche limit of the Earth, and every warning the bureau has issued since the first "
          "notice meets the night it was written for. The government must keep the districts calm, the stores open and the "
          "radio on, whatever the sky does. Every plan made in five years is tested at once.",
          ('meteor', 'shelter'), after=('sky_shelters',), requires=(After('1999.7.8'),), reward=(Event('roche_night'),)),
    Focus('sky_archive', 'An Archive of the Asteroid Years',
          "After the pass, the bureau gathers every warning, drill record and stockpile ledger into one archive, with a "
          "frank report on what worked and what failed. The archive becomes the basis of a standing emergency service that "
          "outlives the asteroid. It costs a few clerks and the embarrassment of an honest report.",
          ('document', 'telescope'), after=('sky_close_pass',), reward=(SwapIdea('skywatch_bureau', 'emergency_service'),)),
))

BELKAN = Branch('belkan', 'Freight in the Belkan War', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_rates', 'Freight Rates in a Belkan Spring',
          "The Belkan War breaks out abroad, and its first effect in Echinata is on freight. Insurers raise their rates, "
          "foreign charterers bid for any hull that floats and fuel prices jump. The coaster owners sense profit, the import "
          "merchants sense ruin, and the government must decide how its shipping behaves while other nations fight.",
          ('economy', 'navy'), requires=(After('1995.3.25'),),
          reward=(TimedIdea('war_rates', 365), Event('belkan_freight'))),
    Focus('bw_neutral', 'Neutral Hulls Only',
          "One answer forbids Echinatan hulls from carrying cargo for any belligerent and enforces the rule through the "
          "harbour offices. Neutral shipping keeps the country out of every blockade argument and clear of the war's "
          "insurers. Owners lose the most lucrative charters of the decade, and they say so loudly in the capital.",
          ('peace', 'navy'), after=('bw_rates',), exclusive=('bw_charters',),
          reward=(Idea('neutral_hulls'), Flag('neutral_record'))),
    Focus('bw_charters', 'Hulls for Hire in Wartime',
          "The other answer lets owners charter their ships to any buyer, belligerent or not, provided the voyage avoids "
          "declared war zones. Charter money floods into the port districts and the yards fill with refits. The country "
          "earns foreign currency, along with the lasting suspicion of whichever side loses.",
          ('economy', 'diplomacy'), after=('bw_rates',), exclusive=('bw_neutral',),
          reward=(Idea('wartime_charters'), Flag('charter_record'))),
    Focus('bw_state_colours', 'State Hulls Under Neutral Colours',
          "The state coastal line can serve neutral relief and trade routes under the national flag, carrying grain and "
          "medicine rather than munitions. Its masters receive strict cargo rules and a naval liaison officer on every "
          "voyage. The voyages earn little, but they establish the line abroad as an honest carrier.",
          ('navy', 'peace'), after_any=('bw_neutral', 'bw_charters'), requires=(HasFlag('coast_state'),),
          reward=(TimedIdea('neutral_voyages', 365), XP('navy', 10))),
    Focus('bw_insurance', 'An Insurance Pool for the Coasters',
          "Private owners cannot afford the war-risk premiums foreign insurers now charge. A national insurance pool, backed "
          "by the treasury and funded by owner contributions, keeps the licensed coasters sailing. The treasury takes on a "
          "risk it cannot measure, and the owners accept rules about where they may sail.",
          ('scales', 'economy'), after_any=('bw_neutral', 'bw_charters'), requires=(HasFlag('coast_private'),),
          reward=(Idea('insurance_pool'),)),
    Focus('bw_lumen', 'After the Lumen Signing',
          "A treaty is signed in Lumen and the Belkan War ends. Freight rates fall back, charters dry up and the war-risk "
          "clauses lapse. The government reviews what its shipping policy cost and earned, and decides which wartime rules "
          "should become permanent. The review, rather than the war, is what Echinata will remember.",
          ('peace', 'document'), after_any=('bw_neutral', 'bw_charters'), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_rates'), Stability(0.03))),
    Focus('bw_belka_won', 'Selling to a Victorious Belka',
          "If the war ends with Belka holding its gains, the Belkan economy becomes a market that many traders are reluctant "
          "to serve. Echinatan firms can sell fuel and metal there with little competition, at the price of being remembered "
          "by the other side. The government lets the trade proceed but keeps it strictly commercial.",
          ('diplomacy', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_market', 730),)),
    Focus('bw_belka_lost', 'Contracts for the Rebuilding',
          "If Belka loses the war, the countries recovering from it need fuel, ships and engineers for years of rebuilding. "
          "Echinatan firms bid for small contracts in fuel supply, coastal shipping and machine repair. The contracts are "
          "modest but steady, and they introduce the country's firms to buyers they had never reached.",
          ('rebuild', 'diplomacy'), after=('bw_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(TimedIdea('rebuild_contracts', 730),)),
))

USEAN = Branch('usean', 'The Usean War from Afar', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('uc_stonehenge', 'Stonehenge in Erusean Hands',
          "Erusea invades the neutral country of San Salvacion and seizes Stonehenge, turning its railguns into anti-air "
          "batteries. The news reaches Echinata through foreign wires and the price of fuel. A war in Usea will reshape "
          "trade routes, insurance and arms markets everywhere, and the government needs a posture before its traders choose "
          "one for it.",
          ('missile', 'communications'), requires=(After('2003.6.1'),), reward=(Idea('usean_watch'), Event('usean_war'))),
    Focus('uc_relief', 'Relief Voyages to Usea',
          "The neutral record from the Belkan years lets Echinatan hulls carry relief cargo to Usean ports under "
          "international supervision. The voyages are small, risky and widely reported. They earn the country goodwill at "
          "little cost, though the crews sail into waters where nobody fully controls the sky.",
          ('peace', 'medical'), after=('uc_stonehenge',), requires=(HasFlag('neutral_record'),), reward=(Idea('relief_record'),)),
    Focus('uc_charter_boom', 'The Charter Boom Returns',
          "Owners who chartered hulls during the Belkan War know the trade and its buyers, and the Usean war revives demand "
          "for any ship available. The government applies the old charter rules and taxes the profits for the yards. Money "
          "flows into the port districts again, along with questions about which side each cargo serves.",
          ('economy', 'navy'), after=('uc_stonehenge',), requires=(HasFlag('charter_record'),),
          reward=(TimedIdea('charter_boom', 365), XP('navy', 10))),
    Focus('uc_fuel', 'Fuel for a Wartime Market',
          "The refinery towns now earn their keep. Wartime demand pushes fuel prices up, and Echinatan refined fuel finds "
          "buyers at a premium. Contracts bar sales to belligerent armed forces, a clause some buyers find ways around. The "
          "refineries run three shifts and the export ledger records the best year in its short history.",
          ('industry', 'economy'), after=('uc_stonehenge',), requires=(HasFlag('model_refining'),),
          reward=(TimedIdea('fuel_windfall', 365),)),
    Focus('uc_metal', 'Rolled Metal for Distant Yards',
          "The light-metals plants find buyers among shipbuilders and aircraft repairers in neutral countries trading with "
          "the war's participants. Rolled aluminium and steel sell at prices the smelter founders never imagined. The plants "
          "expand within their existing sites, hire every metallurgist they can find and argue about how long it will last.",
          ('industry', 'diplomacy'), after=('uc_stonehenge',), requires=(HasFlag('model_metals'),),
          reward=(TimedIdea('metal_orders', 365),)),
    Focus('uc_plains_radar', 'An Air Watch on the Plains Coast',
          "The war has shown how much a single air-defence complex can change a conflict, and the air staff asks where "
          "Echinata is blind. The answer is the District G coast and the Sotoa frontier. A radar station on the plains "
          "coast closes that gap, at the cost of technicians the other stations can barely spare.",
          ('radar', 'security'), after=('uc_stonehenge',),
          reward=(Build('radar_station', 1, 586), Research('radar_tech', 0.5, 1))),
    Focus('uc_isaf_victory', 'Trade After Farbanti',
          "If the war ends with the Erusean surrender, the Usean continent faces years of rebuilding and its shipping lanes "
          "reopen. Echinatan firms bid for coastal shipping and fuel supply contracts in the rebuilding ports. Buyers favour "
          "countries that stayed neutral or carried relief, which is where earlier choices start to pay.",
          ('rebuild', 'economy'), after=('uc_stonehenge',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('usean_rebuilding', 730),)),
    Focus('uc_erusean_victory', 'Terms with a Victorious Erusea',
          "If the war ends with Erusea prevailing, every Echinatan cargo bound for Usea must deal with a government that won "
          "its war and keeps what it seized. Echinata negotiates commercial terms that keep its ships trading without "
          "endorsing the conquest. It is uncomfortable "
          "diplomacy, and every camp at home will say the government conceded too much, whatever the terms actually say about "
          "tariffs, ports and fuel.",
          ('diplomacy', 'scales'), after=('uc_stonehenge',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(TimedIdea('erusean_terms', 730), PP(25))),
    Focus('uc_review', 'The Programme Reviewed at 2005',
          "As the Usean war ends or settles, the government reviews the programme begun in 1991: the ballot, the roads, the "
          "coast, the plants and the sustainment service. The review costs a season of hearings and frank reports from every "
          "district. What it records will shape the decisions of the next fifteen years.",
          ('document', 'assembly'), after_any=('uc_relief', 'uc_charter_boom', 'uc_fuel', 'uc_metal', 'uc_plains_radar'),
          requires=(After('2005.1.1'),),
          reward=(Stability(0.03), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (BALLOT, ROADS, COAST, PLANTS, SUSTAIN, ARMY, AIR, SKY, BELKAN, USEAN)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('coaster_convoy', 'Sail the Winter Coaster Convoy',
                'The escorts shepherd the coasters through the stormy months on a fixed timetable. Repeatable once a year; '
                'it costs fuel and crew rest.',
                40, (TimedIdea('winter_convoy', 120), XP('navy', 10)), requires=(Completed('coast_escorts'),), cooldown=365),
    DecisionDef('causeway_works', 'Raise a Second Marsh Causeway',
                'Engineers raise a second causeway across the District D marshes. A one-time works programme.',
                75, (Build('infrastructure', 1, 577),), requires=(Completed('roads_d_causeway'),)),
    DecisionDef('crossroads_plant', 'Fund a Second Crossroads Plant',
                'The dispersal fund pays for another plant in the District F works town. A one-time charge on the fund.',
                100, (Build('industrial_complex', 1, 585),), requires=(Completed('plants_f_works'),)),
    DecisionDef('parts_amnesty', 'Declare a Parts Amnesty',
                'Units may return hoarded spares to the district depots without penalty for ninety days. Repeatable every '
                'six months; commanders resent the audits that follow.',
                25, (TimedIdea('parts_amnesty', 90),), requires=(Completed('sus_depots'),), cooldown=180),
    DecisionDef('siren_drill', 'Sound the District Sirens',
                'Every district runs a full siren and shelter drill on the same morning. Repeatable once a year; it costs '
                'a working day.',
                30, (TimedIdea('drill_readiness', 90), Stability(0.01)), requires=(Completed('sky_wardens'),), cooldown=365),
    DecisionDef('liaison_officers', 'Exchange Frontier Liaison Officers',
                'The army offers liaison officers to the neighbouring frontier commands so that incidents are settled by '
                'telephone. Once only; it changes no claim.',
                50, (Stability(0.02), XP('army', 10)), requires=(Completed('army_frontiers'),)),
)
