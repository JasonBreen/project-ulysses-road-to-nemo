"""Terentio (TER): bespoke national focus tree, era e1 (1991 to 2005).

Terentio owns nothing on 1 January 1991. It is one of Perbla's crown lands, and this tree
applies only once it exists as a released country; tools/release_foundations owns when and
how that happens, and nothing here assumes a date or a mechanism. Its own states are its
cores, 209 (victory point Karluga, also its history capital) and 571 (captioned Terentio
Desert). Every build stays guarded by owns_state and targets only those two states.

Source layers. Mod provenance: the inherited history file, the Office of the Crown
character, the country names, the core states with their buildings, resources, railways,
weather and place names, the mutual Dakrain claims, the Belkan War outcome flags, and the
Perbla spec (tools/world_depth/pbl/content.py), whose crown-lands and desert branches this
tree never contradicts. Official: a few ACES Chronicle rows used only as date anchors for
regional pressure. Everything else, including every Terentian choice, office, idea,
building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='TER', name='Terentio', root='world', package='ter',
                  themes=('tools', 'civil', 'economy'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Terentio history: monarchism ruling at 70 percent popularity with fascism, democratic and communism at 10 '
           'and neutrality at 0; elections not allowed (frequency 48); stability and war support 0.8; three research slots; no '
           'starting ideas; starting technology of infantry and anti-tank weapons, engineers, light and main battle tanks, '
           'armoured cars, infantry fighting vehicles, motorised rockets, marines and interwar anti-air, with no aircraft '
           'technology. The starting leader is the unnamed Office of the Crown (TER_ac_government_office, '
           'constitutional_monarchy), whose holder has not been established; the tree never names one.',
           'mod/2985041246/history/countries/TER - Terentio.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Principality of Terentio (monarchism), Union of Terentio (democratic), Terentio '
           '(neutrality), Socialist Federation of Terentio (communism) and State of Terentio (fascism). The three political '
           'answers here use the Principality, the plain neutrality name or the Union; no socialist or fascist path is offered.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Release-country scope: TER owns no state in 1991; its cores are 209 and 571 (both owned and cored by PBL) and its '
           'history capital is 209, the capital of the generic core release case in the release intake. Opening laws from the '
           'intake: civilian_economy, export_focus and volunteer_only. tools/release_foundations owns when and how Terentio '
           'exists; this tree assumes neither, and every build targets 209 or 571 under an owns_state guard.',
           'tools/release_foundations/intake.json (TER); tools/world_foundation/country_registry.json (TER); '
           'tools/world_starts/release_inventory.json (TER); docs/WORLD_RELEASE_FOUNDATIONS.md'),
    Source('Mod provenance',
           'Geography. State 209 (captioned North Dakrain; victory point Karluga on urban coastal province 618): state category '
           'city with six shared slots, four arms plants and one civilian plant (one slot free), infrastructure 2, air base 5 '
           'with the airport on plains province 2076, naval base 4 at Karluga, a second urban coastal province (1660), plains '
           'and forest inland, manpower about 3.4 million. State 571 (captioned Terentio Desert): state category town with four '
           'slots all taken by four arms plants, infrastructure 2, no air base, airport and supply node on desert province 3484, '
           'oil 30, aluminium 24, steel 6, rubber 5 and chromium 3, desert, hills and mountain provinces, manpower about ten '
           'thousand. Railways: level-2 lines from Karluga toward Torre Mountain and Sofern; a level-1 line from 2076 through '
           'desert province 516 and mountain province 5878 toward state 112; a level-2 line from the desert railhead (3484) '
           'through the hills toward state 112 and Old Perbla. Land neighbours PBL (112, 173 Faroe, 207 Torre Mountain, 601 Old '
           'Perbla), DAK (114 Trent, 234 Brunies) and ARK (37 Halloma Basin, 252 Eastern Nieblo), computed from '
           'map/provinces.bmp. Strategic region Terentio (41): 21 to 34 degrees, light and occasional heavy rain, no snow or '
           'mud. The supply-hub caption on province 3484 and the Earth-template caption of state 112 are never used as place '
           'names.',
           'mod/2985041246/history/states/209-State_209.txt, 571-State_571.txt; mod/2985041246/map/definition.csv; '
           'mod/2985041246/map/railways.txt; mod/2985041246/map/supply_nodes.txt; mod/2985041246/map/airports.txt; '
           'mod/2985041246/map/strategicregions/41-Terentio.txt; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml'),
    Source('Mod provenance',
           'Claims: TER (like PBL) claims 114 Trent and 234 Brunies, and DAK claims 209 and 571. The tree touches no claim, core '
           'or border; the one Dakrain-facing focus is a fuel sale with an explicit no-claim tooltip.',
           'mod/2985041246/history/states/114-State_114.txt, 234-State_234.txt, 209-State_209.txt, 571-State_571.txt'),
    Source('Mod provenance',
           'Consistency with neighbouring trees: the Perbla tree describes Terentio as the crown land between the desert fields '
           'and the northern coast, whose towns haul water by truck, with oil and bauxite under the desert and arms plants on '
           'the same ground, and a Dakrain dispute over the Terentio frontier. Nothing here narrates which Perblan focuses were '
           'taken before Terentio governs itself, and the subjects of the Relentio, Serenava, Dakrain and Arklith trees (ports, '
           'airfields, casemates, claims offices, frontier wells and the Halloma field) are not reused.',
           'tools/world_depth/pbl/content.py (LANDS and DESERT branches, events four_lands and desert_oil); '
           'tools/world_depth/rel/content.py; tools/world_depth/ser/content.py; tools/world_depth/dak/content.py; '
           'tools/world_depth/ark/content.py'),
    Source('Mod provenance',
           'Campaign hooks read only outcomes the mod already records: belka_lost_belkan_war and belka_won_belkan_war, set by '
           'the Belkan War events. Each is a separate gameplay branch; neither is asserted as history.',
           'mod/2985041246/events/Belka.txt'),
    Source('Official', 'Date anchor only: a jointly financed Osean and Belkan resource company is found to have hidden its losses.',
           '1991 / 08.16'),
    Source('Official', 'Date anchor only: the Belkan War breaks out.', '1995 / 03.25'),
    Source('Official', 'Date anchor only: the treaty signed in Lumen ends the Belkan War.', '1995 / 06.20'),
    Source('Official', 'Date anchor only: A World With No Boundaries launches a coup.', '1995 / 12.25'),
    Source('Official', 'Date anchor only: the announcement that Ulysses will strike the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor only: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor only: the FCU demand to Erusea and the founding of the ISAF in Usea.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Terentian focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, claim, war, annexation or faction effects; no new place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('crown_office_interim', 'An Office Holding the Seals',
            'The crown office keeps the seals while the coast and the desert argue over who should hold them.',
            {'political_power_gain': 0.05, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('coast_majority', 'Seats by Head Count', 'Ministers answer to a chamber in which the coast holds nearly every seat.',
            {'stability_factor': 0.03, 'political_power_factor': 0.04}, ('ballot', 'assembly')),
    IdeaDef('lease_boards_seals', 'The Lease Boards Hold the Seals',
            'Lease-holders, field managers and treasury officials decide; the chamber only advises.',
            {'political_power_gain': 0.15, 'stability_factor': -0.03}, ('economy', 'command')),
    IdeaDef('union_compact', 'The Coast and Desert Compact', 'Oil crews and dock unions press for one Union bound by a revenue formula.',
            {'stability_factor': 0.02, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('assembly', 'scales')),
    IdeaDef('desert_benches', 'Reserved Desert Benches', 'The desert districts hold a fixed block of seats, whatever their head count.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05}, ('ballot', 'civil')),
    IdeaDef('board_ledger', 'The Monthly Board Ledger', 'Every lease payment, pump order and water delivery is printed each month.',
            {'political_power_gain': 0.20, 'stability_factor': 0.01}, ('document', 'economy')),
    IdeaDef('union_formula', 'The Revenue Formula', 'Fixed shares of every royalty go to the desert, the coast and the budget.',
            {'stability_factor': 0.05, 'production_speed_buildings_factor': 0.04, 'political_power_gain': -0.03}, ('scales', 'economy')),
    IdeaDef('printed_orders', 'Orders in Print', 'Every law and lease award is posted in each district within ten days.',
            {'political_power_factor': 0.04, 'stability_factor': 0.02}, ('document', 'communications')),
    IdeaDef('princely_statute', 'The Statute of the Principality', 'One written statute binds the crown office, the chamber and the desert benches.',
            {'stability_factor': 0.08, 'political_power_factor': 0.08}, ('scales', 'document')),
    IdeaDef('board_charter', 'The Board Under Charter', 'Fixed terms, an auditor it cannot dismiss and a chamber it must consult on water.',
            {'political_power_gain': 0.25, 'stability_factor': 0.04}, ('command', 'scales')),
    IdeaDef('union_constitution', 'The Union Constitution', 'Neither half of the country can rewrite the bargain without the other.',
            {'stability_factor': 0.07, 'production_speed_buildings_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'document')),
    # oil
    IdeaDef('lease_fog', 'Leases Nobody Has Read', 'Nobody can say for certain who holds which desert block, or on what terms.',
            {'political_power_gain': -0.05, 'production_speed_buildings_factor': -0.03}, ('document', 'economy')),
    IdeaDef('lease_register', 'The Open Block Register', 'Every desert block has a number, a holder and an expiry date on public record.',
            {'political_power_gain': 0.05, 'production_speed_buildings_factor': 0.04}, ('document', 'scales')),
    IdeaDef('metered_royalty', 'Royalties by the Meter', 'Royalties are paid on sealed wellhead meters instead of the operators own returns.',
            {'political_power_gain': 0.10}, ('economy', 'tools')),
    IdeaDef('audited_operators', 'Audited Operators', 'Every leaseholder files accounts that an outside auditor has checked.',
            {'political_power_factor': 0.04, 'production_factory_efficiency_gain_factor': 0.02}, ('scales', 'economy')),
    IdeaDef('sliding_royalty', 'The Sliding Royalty', 'Private operators pay a royalty that climbs and falls with the crude price.',
            {'political_power_gain': 0.10, 'production_speed_industrial_complex_factor': 0.06}, ('economy', 'scales')),
    IdeaDef('crude_in_kind', 'Royalty Crude in State Tank Cars', 'The state takes its share in barrels and sells or stores them itself.',
            {'industrial_capacity_factory': 0.05, 'political_power_gain': 0.05}, ('logistics', 'economy')),
    IdeaDef('service_fees', 'Drillers on a Barrel Fee', 'Foreign firms drill for a fee, and every barrel above cost stays Terentian.',
            {'production_speed_buildings_factor': 0.06, 'stability_factor': 0.02}, ('tools', 'economy')),
    IdeaDef('flare_capture', 'Gas Instead of Flares', 'Field gas runs the generators in the camps and halls instead of burning in the open.',
            {'production_factory_efficiency_gain_factor': 0.04, 'production_factory_max_efficiency_factor': 0.03}, ('industry', 'tools')),
    IdeaDef('field_school', 'The Desert Field School', 'Young Terentians learn drilling and well control beside the camps.',
            {'research_speed_factor': 0.03}, ('science', 'training')),
    # water
    IdeaDef('truck_water', 'Water by the Truckload', 'Households buy drinking water from haulers at prices that rise every dry month.',
            {'stability_factor': -0.03, 'consumer_goods_factor': 0.03}, ('logistics', 'civil')),
    IdeaDef('posted_tank_price', 'The Posted Tank Price', 'Every water truck carries a painted maximum price, and inspectors check it.',
            {'stability_factor': 0.02}, ('scales', 'civil')),
    IdeaDef('sweet_seawater', 'Seawater Made Drinkable', 'The desalting plant beside the Karluga port fills the city mains.',
            {'stability_factor': 0.04, 'production_speed_industrial_complex_factor': 0.04}, ('civil', 'tools')),
    IdeaDef('fossil_draw', 'The Old Water Pumped', 'Deep bores supply the desert towns, camps and halls without rationing.',
            {'production_speed_buildings_factor': 0.06, 'stability_factor': 0.02}, ('tools', 'civil')),
    IdeaDef('deep_ration', 'The Old Water Rationed', 'Every deep bore is licensed and capped, and the reserve is kept.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('scales', 'tools')),
    IdeaDef('produced_water_reuse', 'Treated Field Water', 'Water brought up with the crude serves the halls, the ore washing and the dust roads.',
            {'production_speed_buildings_factor': 0.04, 'stability_factor': 0.02}, ('rebuild', 'tools')),
    IdeaDef('water_board', 'The Principality Water Board', 'One board runs the mains, the desalting plant, the bores and the truck permits.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.10}, ('civil', 'command')),
    # the desert halls
    IdeaDef('dune_halls', 'Four Halls, Four Ledgers', 'Four desert arms halls, each with its own managers, payroll and books.',
            {'production_factory_efficiency_gain_factor': -0.03, 'production_speed_arms_factory_factor': 0.03}, ('industry', 'document')),
    IdeaDef('desert_works_company', 'The Desert Works Company', 'One public company runs the four desert halls and their buses.',
            {'production_factory_efficiency_gain_factor': 0.04, 'production_speed_arms_factory_factor': 0.05}, ('industry', 'command')),
    IdeaDef('blast_code', 'The Safe Distance Code', 'Magazines, earth banks and storage limits follow a written code.',
            {'stability_factor': 0.03, 'production_factory_max_efficiency_factor': 0.03}, ('security', 'industry')),
    IdeaDef('propellant_export', 'Propellant on Licence', 'Desert propellant and filled rounds sell abroad under signed licences.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04}, ('missile', 'economy')),
    IdeaDef('petrochem_halls', 'The Chemical Halls', 'Former propellant lines make solvents, resins and fertiliser.',
            {'production_speed_industrial_complex_factor': 0.08, 'consumer_goods_factor': -0.03}, ('rebuild', 'industry')),
    IdeaDef('cheap_fertiliser', 'Fertiliser Below Cost', 'The chemical halls sell to the coast farms at a loss to win the market.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('civil', 'economy')),
    # Karluga
    IdeaDef('tanker_queue', 'Tankers at Anchor', 'Tankers wait for days for the one berth that can take them.',
            {'consumer_goods_factor': 0.02, 'naval_coordination': -0.03}, ('navy', 'logistics')),
    IdeaDef('tanker_jetty', 'The Deep-Water Jetty', 'Large tankers load in a single day at the jetty off Karluga.',
            {'industrial_capacity_factory': 0.04, 'naval_coordination': 0.03}, ('navy', 'bridge')),
    IdeaDef('spill_crews', 'Spill Crews on Standby', 'Booms, skimmers and a rehearsed plan guard the beaches and fishing grounds.',
            {'stability_factor': 0.02, 'repair_speed_factor': 0.05}, ('fishing', 'tools')),
    IdeaDef('jetty_watch', 'The Jetty Patrol', 'Fast tenders patrol the loading roads and escort laden tankers to open water.',
            {'navy_org_factor': 0.04, 'naval_coordination': 0.04}, ('navy', 'security')),
    # buyers and neighbours
    IdeaDef('gatewood_buyer', 'First Cargo to Gatewood', 'Perbla buys Terentian crude first, on a long fixed-price contract.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.03}, ('diplomacy', 'rail')),
    IdeaDef('spot_seller', 'Crude at the Posted Price', 'Every cargo goes to whoever pays the market price on the day.',
            {'political_power_gain': 0.08, 'industrial_capacity_factory': 0.03}, ('economy', 'navy')),
    IdeaDef('brunies_fuel', 'Fuel Across the Frontier', 'Terentian crude fuels the mills around Brunies, and no claim has moved.',
            {'stability_factor': 0.02, 'production_speed_buildings_factor': 0.04}, ('diplomacy', 'industry')),
    IdeaDef('basin_data', 'Pressure Logs Shared with Arklith', 'The two oil inspectorates swap well logs and pressure readings.',
            {'research_speed_factor': 0.02, 'stability_factor': 0.01}, ('science', 'diplomacy')),
    # the field guard
    IdeaDef('field_guard', 'The Field Guard', 'A thin guard of soldiers and hired watchmen covers the desert installations.',
            {'army_core_defence_factor': 0.04}, ('security', 'tools')),
    IdeaDef('heat_drill', 'Drilled for the Desert Summer', 'Water discipline and night marches are practised in the hottest months.',
            {'attrition': -0.05, 'army_org_factor': 0.03}, ('training', 'security')),
    IdeaDef('desert_columns', 'Night Columns', 'Light motorised columns move between the fields after dark.',
            {'army_speed_factor': 0.05, 'supply_consumption_factor': -0.05}, ('logistics', 'security')),
    IdeaDef('line_posts', 'Posts on the Lines', 'Wired and lit posts stand at every pumping station and railway bridge.',
            {'army_core_defence_factor': 0.08, 'air_detection': 0.05}, ('security', 'shelter')),
    IdeaDef('pipeline_flights', 'Dawn Pipeline Flights', 'Light aircraft fly the lines every morning and radio the field camps.',
            {'air_detection': 0.08, 'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('crew_reserve', 'The Oil Crew Reserve', 'Field hands train two weeks a year as guides, drivers and mechanics.',
            {'army_core_defence_factor': 0.05, 'training_time_army_factor': -0.08}, ('training', 'tools')),
    # the Belkan War years
    IdeaDef('war_premium', 'Crude at a War Premium', 'Belligerents and neutrals alike bid up every Terentian cargo.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('barrels_held', 'Barrels in Reserve', 'Part of the wartime output stays in tanks at the railhead and the port.',
            {'stability_factor': 0.03, 'war_support_factor': 0.03}, ('logistics', 'shelter')),
    IdeaDef('pumps_flat_out', 'Pumps at Full Stroke', 'Every well is forced to its limit while the premium lasts.',
            {'industrial_capacity_factory': 0.06, 'stability_factor': -0.03}, ('tools', 'industry')),
    IdeaDef('station_guards', 'Guarded Pumping Stations', 'Fences, floodlights and guards stand at every remote station.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.02}, ('security', 'civil')),
    IdeaDef('windfall_fund', 'The Windfall Account', 'The wartime premium sits in an account drawn only by public vote.',
            {'stability_factor': 0.04, 'political_power_factor': 0.05}, ('scales', 'economy')),
    IdeaDef('price_slump', 'After the Premium', 'Buyers renegotiate and budgets shrink once the war price vanishes.',
            {'political_power_gain': -0.05, 'consumer_goods_factor': 0.03}, ('economy', 'document')),
    IdeaDef('reconstruction_bitumen', 'Bitumen for the Rebuilding', 'Heavy crude sells to refiners supplying the postwar road builders.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': 0.01}, ('rebuild', 'economy')),
    IdeaDef('belkan_long_contracts', 'Ten Years Sold to Belka', 'Belkan state buyers hold long crude contracts at a premium.',
            {'political_power_gain': 0.08, 'stability_factor': -0.02}, ('diplomacy', 'economy')),
    # Ulysses
    IdeaDef('impact_dread', 'Every Wellhead a Target', 'Planners list everything that would burn if a fragment fell on Terentio.',
            {'stability_factor': -0.02, 'war_support_factor': 0.02}, ('meteor', 'tools')),
    IdeaDef('valves_fitted', 'Safety Valves Downhole', 'Every producing well can close itself within seconds.',
            {'stability_factor': 0.03, 'production_factory_max_efficiency_factor': 0.02}, ('tools', 'security')),
    IdeaDef('well_fire_crews', 'Well-Fire Crews', 'A standing crew can cap a burning well wherever it is.',
            {'repair_speed_factor': 0.10, 'stability_factor': 0.02}, ('rebuild', 'tools')),
    IdeaDef('sealed_water', 'Sealed Emergency Water', 'A reserve of water is held untouched for the worst week.',
            {'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('railhead_camps', 'Camps Staked Out Inland', 'Tent towns are planned at the railhead in case the coast must be emptied.',
            {'stability_factor': 0.02, 'planning_speed': 0.05}, ('refugees', 'shelter')),
    # the new century
    IdeaDef('propellant_contracts', 'Service Contracts for Propellant', 'Foreign buyers contract the halls for supply, storage and disposal.',
            {'production_speed_arms_factory_factor': 0.08, 'industrial_capacity_factory': 0.05}, ('missile', 'document')),
    IdeaDef('chemical_markets', 'Desert Chemicals Abroad', 'Solvents, resins and fertiliser from the halls sell in foreign markets.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': -0.04}, ('economy', 'industry')),
    IdeaDef('usean_prices', 'Crude Priced by a Usean War', 'War in Usea lifts the price of every Terentian cargo once again.',
            {'political_power_gain': 0.08, 'consumer_goods_factor': 0.02}, ('economy', 'navy')),
    # decisions
    IdeaDef('summer_convoys', 'Summer Water Convoys', 'Extra hired convoys carry water to the hottest districts.',
            {'stability_factor': 0.04}, ('logistics', 'civil')),
    IdeaDef('extra_tank_cars', 'Leased Tank Cars', 'Foreign tank cars clear crude from the desert railhead faster.',
            {'industrial_capacity_factory': 0.03, 'consumer_goods_factor': 0.01}, ('rail', 'logistics')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('princely_ministry', 'Ministry of the Principality of Terentio',
           'A ministry formed by the largest bloc in the chamber, collectively responsible and removable by a vote of the '
           'deputies, governing in the name of the crown office. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('fields_board', 'Board of the Fields and Wells',
           'A board of lease-holders, field managers and senior treasury officials holding the seals by standing order, with '
           'the chamber summoned only to advise. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('union_council', 'Council of the Union of Terentio',
           'A council elected from the chamber of the Union of Terentio on a fixed calendar and bound by the revenue formula '
           'between coast and desert, with the princely title laid aside. Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('two_halves', 'One Coast, One Desert', (
        "The first council of state meets in the harbour offices at Karluga, the only rooms in the principality with enough "
        "chairs and a working telephone exchange. The Office of the Crown opens with a short statement: the seals are kept, "
        "the soldiers are paid and the oil revenue arrives each quarter. What the office does not say is who should decide "
        "how that revenue is spent.",
        "Everyone in the room knows the arithmetic. Nearly all of Terentio's people live on the northern coast, in Karluga "
        "and on the plain behind it. Nearly all of its money comes from the desert, where a few thousand people work the "
        "wells, the bauxite hills and four arms halls built far from any town. The coast speaks of fairness by head count. "
        "The desert speaks of fairness by contribution. Both are quoting real numbers.",
        "No settlement is possible at the first sitting, and nobody pretends otherwise. The council can at least choose its "
        "manner. It may hold its debates in public, with the minutes printed and the desert towns reading every word a week "
        "later, or it may keep them inside the harbour offices until a proposal is ready. Whichever it chooses, the field "
        "towns will judge the coast by it.",
    ), (
        Option('Print every word of the debates.', (Stability(0.02), PP(-10))),
        Option('Keep the council behind closed doors.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('leases_unread', 'The Lease Boxes', (
        "The clerks of the lands office carry the lease files up from the basement in forty cardboard boxes and stack them "
        "along a corridor, because no single room will hold them. Each box holds the history of a few desert blocks: original "
        "grants, renewals typed on headed paper, maps redrawn by hand and letters that change the terms without saying so. "
        "Some blocks appear in two boxes with two different holders.",
        "The operators are polite and worried. A few hold leases that expired years ago and were never renewed in writing; "
        "they kept pumping and paying because nobody asked. Others hold blocks they never drilled, waiting for a better price. "
        "One foreign firm produces a side letter granting it first refusal on every block in the hill country, signed by an "
        "office that no longer exists.",
        "Nobody can read forty boxes in a week, but the ministry must say now how it will treat what it finds. It can honour "
        "every lease that has been paid on, however irregular, and buy calm with the operators. Or it can declare that only "
        "leases confirmed by the new register will stand, and accept a year of lawsuits and nervous investors in return for "
        "a clean slate.",
    ), (
        Option('Honour every lease that has been paid on.', (Stability(0.02), PP(10))),
        Option('Only registered leases will stand.', (PP(30), Stability(-0.03))),
    ), picture=2),
    EventDef('water_sellers', 'The Water Sellers', (
        "The water survey comes back with a map no minister had seen before. Several hundred trucks carry drinking water to "
        "the outer districts of Karluga and to every town in the desert, filling at private bores, at a few municipal taps "
        "and, in one case, at a pipe the survey team politely describes as unexplained. Prices double between the cool months "
        "and the hot ones.",
        "The haulers are not villains. Most own one or two trucks, drive long hours and know their customers by name. A few "
        "large firms own the best bores, set the prices the small haulers follow and lend money to families who fall behind. "
        "In the hottest districts a household spends more on water than on bread, and the survey notes several schools that "
        "send pupils home early on days the truck is late.",
        "Ministers have to decide how to begin. They can call the haulers' associations to the harbour offices and bargain, "
        "trading permits and fuel discounts for steadier prices. Or they can publish the survey in full, names and prices "
        "included, and let public anger soften the large firms before the inspectors arrive. The haulers will remember "
        "either approach for a long time.",
    ), (
        Option('Bargain with the haulers.', (PP(25), Stability(-0.01))),
        Option('Publish the survey in full.', (Stability(0.03), PP(-20))),
    ), picture=1),
    EventDef('halls_report', 'The Halls Beyond the Dunes', (
        "The inventory team spends a month in the desert and returns sunburnt, carrying ledgers and photographs. Four arms "
        "halls stand on the sand, linked by graded tracks and a single water main, each ringed by earth banks and a fence the "
        "wind has half buried. They mix propellant, fill shells and pack charges, and they run on crews who arrive by bus "
        "over the mountain line before dawn.",
        "Two halls work full shifts on export orders signed years ago. One works half time. The fourth has been kept warm for "
        "a war that never came, its machines greased and its stores full. Behind it, in old bunkers, the team found propellant "
        "older than most of the crews, stored in the heat long past the age any manual allows. The hall managers call it "
        "stable. The team's chemist is less sure.",
        "The cabinet must decide how much of the report the public sees. A full release would explain why the halls need "
        "money and why some stock must be destroyed, and it would frighten every family whose breadwinner rides the bus each "
        "morning. A summary for the ministries would keep the crews calm and leave the old stock to a quieter decision.",
    ), (
        Option('Publish it and test the old stock.', (Stability(-0.02), Event('old_propellant', 14))),
        Option('Keep it for the ministries.', (PP(30), Stability(0.01))),
    ), picture=0),
    EventDef('old_propellant', 'The Old Propellant', (
        "Two weeks after the report, chemists from Karluga finish testing the old stock behind the fourth hall. Most of it has "
        "aged badly. Stabiliser levels are low, some casks have sweated, and a few show warm spots that the testers mark with "
        "red paint and refuse to approach without the fire crew standing by. Nobody has been hurt. The chemists would like to "
        "keep it that way.",
        "Every option is unpleasant. The stock could be burned in pits far out on the sand, a few casks a day for months, "
        "under guard and with smoke visible from the field camps. It could be shipped to a foreign disposal firm at great cost "
        "and some risk on the mountain road. Or the worst casks could be burned and the rest re-stabilised and sold cheaply, "
        "which the export office prefers and the chemists do not.",
        "The crews of the fourth hall are watching closely, since the stock is the reason their hall exists. The field camps "
        "nearby want to know how much smoke they will breathe. Whatever the cabinet orders will be read as a statement about "
        "how seriously the principality takes the dangers it was left to manage.",
    ), (
        Option('Burn all of it on the sand.', (Stability(0.02), PP(-20))),
        Option('Burn the worst and sell the rest.', (PP(25), Stability(-0.02))),
    ), picture=0),
    EventDef('tankers_waiting', 'Seven Tankers at Anchor', (
        "On the morning the harbour office counts them, seven tankers lie at anchor off Karluga, waiting for the one berth "
        "that can take them. The berth was built for general cargo and feeds crude through a hose that a single crew must "
        "couple and uncouple by hand. A ship that should load in a day takes three. The rest wait, and their owners charge "
        "for every hour.",
        "Buyers pass those charges back in the price, so every day a tanker waits comes out of the principality's royalties. "
        "The tank farm behind the port is full more often than empty, and tank cars from the desert queue on the sidings for "
        "their turn to unload. Fishing crews say the anchored ships foul their nets, and the beach districts complain about "
        "the smell of every spill, large or small.",
        "A proper tanker jetty would solve most of it, and it costs more than the principality can comfortably borrow. Before "
        "any engineer is hired, the port must decide how to manage the queue it already has. It can give oil absolute priority "
        "at the berth, clearing the tankers and annoying every other shipper, or keep the berth shared and accept the charges "
        "until a jetty exists.",
    ), (
        Option('Give the tankers priority at the berth.', (PP(20), Stability(-0.01))),
        Option('Keep the berth shared for now.', (Stability(0.02), PP(-10))),
    ), picture=2),
    EventDef('deeds_archive', 'Titles in the Gatewood Archives', (
        "The Terentian archivists return from Gatewood with a list rather than a cartload. The Perblan archives were courteous "
        "and thorough. They hold the original land titles of the desert districts, the old survey sheets of the coast plain "
        "and the first lease grants of the oil blocks, all catalogued and well kept. Karluga holds copies of most of them and "
        "originals of very few.",
        "Nothing in the archives is disputed; the question is custody. Perblan officials point out that their staff have "
        "cared for these series for generations and that splitting a series damages it. Terentian lawyers point out that a "
        "lease case in Karluga cannot wait weeks for a certified copy from another capital. Both sides agree that the records "
        "must not be lost or carelessly duplicated, and that the matter is too dull to interest anyone but archivists and "
        "lawyers.",
        "Karluga must decide what to ask for. It can request the originals of the land and lease series, which matter most to "
        "the oil fields, and leave the rest where it is. Or it can ask only for certified copies, leave every original in "
        "Gatewood and seek a standing arrangement to consult them whenever a case demands it.",
    ), (
        Option('Ask for the land and lease originals.', (PP(-15), Stability(0.02))),
        Option('Certified copies and standing access.', (PP(20), Stability(0.01))),
    ), picture=1),
    EventDef('wartime_crude', 'Crude at a War Price', (
        "In the spring of 1995 the long quarrel around Belka becomes open war, and within a week the price of crude has risen "
        "by a third. Terentio is not a party to the war and has no soldiers anywhere near it. Its telephones are another "
        "matter: buyers who haggled for months now call the oil ministry at night, asking how many cargoes Karluga can load "
        "this quarter and offering to pay in advance.",
        "Some callers represent firms in neutral ports. Others are vague about where the crude will end up, and one asks "
        "whether Terentio could deliver to a harbour that the ministry's maps place uncomfortably close to the fighting. The "
        "treasury has already worked out what a summer of war prices would mean: the deficit gone, the water works funded, the "
        "halls paid for a year. Operators in the desert ask permission to run their pumps harder than the engineers like.",
        "The cabinet's first decision is about the money rather than the oil. It can announce that every coin of the premium "
        "will be counted in public and its use decided in the open, inviting a scramble of claims from every district. Or it "
        "can keep the figures inside the treasury until the shape of the war is clearer, and decide quietly what a windfall "
        "is for.",
    ), (
        Option('Count the premium in public.', (Stability(0.01), Event('windfall_petitions', 20))),
        Option('Keep the figures in the treasury.', (PP(30), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Terentian response is gameplay',
        picture=2),
    EventDef('windfall_petitions', 'Sacks of Petitions', (
        "Three weeks after the premium was announced, petitions start arriving at the harbour offices by the sackful. The "
        "desert towns want a water main and paved streets. The outer districts of Karluga want the trucks replaced by pipes. "
        "The halls want their oldest machines replaced, the field guard wants vehicles that do not overheat, and the schools "
        "want roofs. Every petition quotes the published figure, usually rounded up.",
        "Some petitions are thoughtful and costed. Many are not, and a few come from people who have never paid tax on "
        "anything. The newspapers print the best and the worst side by side. The treasury warns that a premium is not an "
        "income: when the war ends, prices will fall, and any promise made now will still need paying afterwards. The "
        "petitioners reply that the treasury always says that.",
        "Ministers must decide how to answer the sacks. They can choose a few large projects and refuse everything else, "
        "disappointing nearly everyone while keeping most of the money whole. Or they can spread small grants across every "
        "district, so that each town sees something built this year, and leave little for the leaner seasons the treasury "
        "expects.",
    ), (
        Option('Fund a few large projects.', (PP(15), Stability(-0.01))),
        Option('Small grants for every district.', (Stability(0.03), PP(-20))),
    ), picture=1),
    EventDef('impact_wells', 'What Would Burn', (
        "The April 1996 announcement that Ulysses will strike the Earth reaches Karluga by radio in the middle of a working "
        "day. By evening the oil ministry has a list on its wall of everything in Terentio that could burn: the producing "
        "wells, the tank farm behind the port, the tanker berth, the desert halls and their magazines. Nobody knows where "
        "fragments will fall, and the list does not depend on it.",
        "The engineers explain what a single strike could do. A burning wellhead in the desert can blaze for months unless "
        "crews with explosives and pumps reach it. A fire at the tank farm would spread into the harbour districts. The halls "
        "are safest left alone, unless the ground shakes. Families on the coast ask whether they should move inland, and the "
        "desert towns ask where the water would come from if they did.",
        "Before any plan is costed, the cabinet must settle its message. It can speak plainly about the wells and the tanks "
        "and ask operators and citizens to prepare for the worst, which will frighten investors and some families. Or it can "
        "speak only of general readiness, keep the engineers' list confidential and work through it quietly while the world "
        "argues about the asteroid.",
    ), (
        Option('Speak plainly about the risks.', (WarSupport(0.02), Stability(-0.02), Research('engineers_tech', 0.5, 1))),
        Option('Speak only of general readiness.', (Stability(0.02),)),
    ), citation='date anchor only, ACES Chronicle row 1996 / 04.20 in tools/lore/chronicle.json; Terentian preparations are gameplay',
        picture=0),
    EventDef('block_round', 'Envelopes at the Lands Office', (
        "The bidding round closes at noon, and the lands office opens the sealed envelopes in front of the press and two "
        "notaries. Bids have come in for most of the offered blocks: some from operators already working the desert, some from "
        "foreign firms the ministry has never dealt with, and one from a consortium whose address turns out to be a law office "
        "in another country.",
        "The best bids promise drilling within a year, local hiring and a signature payment that would close a gap in the "
        "budget. The weaker ones offer more money and fewer commitments. Two firms ask, through intermediaries, whether the "
        "terms might be adjusted after the award; the lands office records both requests in the minutes, which neither firm "
        "had expected. The field towns want to know how many of their people will be hired.",
        "Ministers must choose how to award the blocks. They can take the highest signature payments and spend them at once, "
        "rewarding the firms with the deepest pockets. Or they can weigh drilling commitments and local hiring above cash, "
        "pleasing the field towns and delaying the money. Either way, the next round will be judged by how this one is "
        "remembered.",
    ), (
        Option('Take the highest payments.', (PP(40), Stability(-0.02))),
        Option('Weigh drilling and hiring first.', (Stability(0.02), Research('excavation_tech', 0.5, 1))),
    ), picture=2),
    EventDef('coast_desert_review', 'A Grey Volume with a Fold-Out Map', (
        "The outside panel's account of the principality appears as a single grey volume with a fold-out map. It describes how "
        "much oil Terentio now pumps, what it is paid, what it spends on water and where the money for the halls comes from. "
        "It counts schools, clinics and water trucks in every district, and it records how coast and desert residents answered "
        "when asked whether the other half treats them fairly.",
        "The answers are not flattering. Coast residents think the desert is pampered with oil money; desert residents think "
        "the coast spends it. Both are partly right. The panel praises what has been built where it exists, and warns that the "
        "principality depends on one export, one loading berth and a few hundred skilled crews who could earn more abroad. "
        "Its last chapter asks what happens when the price falls.",
        "Ministers have a week before the volume is debated. They can answer it chapter by chapter, accepting the hostile "
        "headlines that follow each admission. Or they can welcome its praise, send its warnings to committee and hope that the "
        "price of crude stays high long enough for the committee to finish its work.",
    ), (
        Option('Answer every chapter.', (Stability(0.03), PP(-20))),
        Option('Welcome the praise.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('usean_crude', 'A War Price Again', (
        "When the FCU demands in August 2003 that Erusea withdraw from San Salvacion and the ISAF is established, the war in "
        "Usea is a continent away from Karluga. The price of crude moves within days all the same, as it did in 1995. Insurers "
        "add war premiums to every lane that touches Usean waters, and buyers who spent years squeezing Terentian prices start "
        "returning calls.",
        "This time the principality has experience to draw on. The treasury remembers how fast the last premium vanished. The "
        "operators remember which wells suffered from being run too hard. The halls remember export enquiries from buyers who "
        "were vague about their customers. Each memory argues for caution, and the budget office argues, as budget offices do, "
        "that caution is easy while the money is not yet in the account.",
        "The cabinet must set the tone before the first new contracts are signed. It can treat the premium as temporary from "
        "the start, pricing every contract short and banking the surplus. Or it can lock in long contracts at today's prices, "
        "trading some of the upside for years of certainty that will outlast the war, whenever and however it ends.",
    ), (
        Option('Price short and bank the surplus.', (Stability(0.02), PP(10))),
        Option('Lock in long contracts now.', (PP(35), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / 08.22 in tools/lore/chronicle.json; the Terentian response is gameplay',
        picture=2),
)

# --- branches ------------------------------------------------------------------------------------
GOVERN = Branch('gov', 'The Principality and Its Two Halves', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('gov_office_sits', 'The Crown Office Opens at Karluga',
          "Terentio governs itself from Karluga with an Office of the Crown, a council of notables and no settled answer to its "
          "oldest quarrel: the coast holds almost every voter, while the desert holds almost every barrel. Opening that question "
          "in public costs the office its quiet. Leaving it closed would let the oil revenue decide by default.",
          ('command', 'assembly'), reward=(Idea('crown_office_interim'), Event('two_halves'))),
    Focus('gov_apportion', 'Seats by Head or by Barrel',
          "Before anyone can govern, someone must say how much the desert counts. Seats by population would give the Terentio "
          "Desert a handful of deputies; seats weighted by land or revenue would hand it a veto. The clerks print both sums side "
          "by side. The figures settle nothing, but they drag three rival answers into the open at once.",
          ('ballot', 'scales'), after=('gov_office_sits',),
          reward=(PP(25), Tooltip('Three answers open from here, and only one of them can be chosen.'))),
    Focus('gov_coast_path', 'Ministers Answer to the Coast Chamber',
          "The constitutional camp would keep the princely crown and make ministers answer to an elected chamber apportioned by "
          "head count. Karluga and the coast plain would carry nearly every vote, and the crown would sign on advice. It is the "
          "tidiest answer on paper. The field towns call it government by the coast, paid for by the desert.",
          ('ballot', 'assembly'), after=('gov_apportion',), exclusive=('gov_board_path', 'gov_union_path'),
          reward=(SwapIdea('crown_office_interim', 'coast_majority'),)),
    Focus('gov_board_path', 'The Lease Boards Ask for the Seals',
          "The notables who sit on the lease boards and run the field towns argue that a principality living on oil should be "
          "governed by people who understand oil. They want the seals held by a board of lease-holders, field managers and "
          "treasury officials, with the chamber kept for advice. Revenue would be steady. Karluga would have very few votes.",
          ('economy', 'command'), after=('gov_apportion',), exclusive=('gov_coast_path', 'gov_union_path'),
          reward=(SwapIdea('crown_office_interim', 'lease_boards_seals'),)),
    Focus('gov_union_path', 'A Union of the Coast and the Desert',
          "A third camp, strongest among the oil crews and the Karluga dock unions, wants a Union of Terentio: an elected "
          "council, the princely title retired, and a written formula that divides oil revenue between the two halves before "
          "any minister can touch it. The crews cheer. The lease-holders and the officer corps doubt that arithmetic can govern.",
          ('assembly', 'scales'), after=('gov_apportion',), exclusive=('gov_coast_path', 'gov_board_path'),
          reward=(SwapIdea('crown_office_interim', 'union_compact'),)),
    Focus('gov_princely_ministry', 'Seat a Princely Ministry',
          "The largest bloc in the chamber forms a ministry of the Principality of Terentio, collectively responsible and "
          "removable by a vote of the deputies. The crown office signs what the ministers bring and keeps its ceremonial duties. "
          "Ministers inherit the water queues and the royalty disputes on their first morning, and from now on the press knows "
          "exactly whose problems they are.",
          ('ballot', 'document'), after=('gov_coast_path',), cost=10,
          exclusive=('gov_fields_board', 'gov_union_council'), reward=(Regime('princely_ministry'),)),
    Focus('gov_fields_board', 'The Board of Fields and Wells Takes Office',
          "A board of lease-holders, field managers and senior treasury officials takes the seals, and elections are suspended "
          "while it governs by standing order. The chamber survives as an advisory body summoned when the board wishes. "
          "Decisions about pipe, pumps and royalties come quickly. Every dry tap in Karluga will now be blamed on the board and "
          "on nobody else.",
          ('command', 'tools'), after=('gov_board_path',), cost=10,
          exclusive=('gov_princely_ministry', 'gov_union_council'), reward=(Regime('fields_board'),)),
    Focus('gov_union_council', 'Elect the Union Council',
          "The chamber passes the Union law and elects a council from its own benches, with elections fixed on a calendar and "
          "the princely title laid aside with honours. The Union of Terentio governs in the name of both halves. Its council "
          "must win votes on the coast while keeping the desert crews loyal, which is harder than either camp admitted.",
          ('assembly', 'ballot'), after=('gov_union_path',), cost=10,
          exclusive=('gov_princely_ministry', 'gov_fields_board'), reward=(Regime('union_council'),)),
    Focus('gov_desert_benches', 'Reserved Benches for the Desert Districts',
          "The ministry reserves a fixed block of chamber seats for the Terentio Desert, whatever its head count, and pairs "
          "every desert deputy with a coast deputy on the budget committee. Purists call it a rotten-borough rule. It gives the "
          "field towns a voice on water and royalties that cannot simply be outvoted, which was the whole point.",
          ('ballot', 'civil'), after=('gov_princely_ministry',), exclusive=('gov_board_ledger', 'gov_union_formula'),
          reward=(SwapIdea('coast_majority', 'desert_benches'), Flag('path_ministry'))),
    Focus('gov_board_ledger', 'The Board Prints Its Ledger',
          "The board answers its critics with numbers: a monthly ledger of every lease payment, pump order and water delivery, "
          "printed and posted in every district office. A ledger is not a vote, and the coast says so loudly. Still, the board "
          "can now show where the money went, and its members can no longer hide their dealings from one another.",
          ('document', 'economy'), after=('gov_fields_board',), exclusive=('gov_desert_benches', 'gov_union_formula'),
          reward=(SwapIdea('lease_boards_seals', 'board_ledger'), Flag('path_board'))),
    Focus('gov_union_formula', 'The Revenue Formula Becomes Law',
          "The Union council writes its revenue formula into law: fixed shares of every royalty to the desert districts, to "
          "Karluga and to the national budget, before any minister may spend a coin. Ministers lose discretion and lenders gain "
          "a number they can trust. When the price of crude falls, the formula will divide less money with the same precision.",
          ('scales', 'economy'), after=('gov_union_council',), exclusive=('gov_desert_benches', 'gov_board_ledger'),
          reward=(SwapIdea('union_compact', 'union_formula'), Flag('path_union'))),
    Focus('gov_gazette', 'A Gazette Posted in Every District',
          "However Terentio is governed, its orders reach the field towns late or not at all, carried by truck drivers who lose "
          "half the post on the mountain road. A printed gazette of every law, lease award and regulation, posted in each "
          "district office within ten days, gives the desert the same text the coast reads. Printing is cheap; ignorance stops "
          "being an excuse.",
          ('document', 'communications'), after_any=('gov_desert_benches', 'gov_board_ledger', 'gov_union_formula'),
          reward=(Idea('printed_orders'),)),
))

OIL = Branch('oil', 'The Desert Fields', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('oil_lease_boxes', 'Open the Boxes of Desert Leases',
          "The leases for the desert fields were written over many years by many offices, and their terms survive in boxes of "
          "carbon copies: some expired, some renewed by letter, a few granted twice for the same block. Before Terentio sets any "
          "oil policy it has to read them. The reading takes a year and annoys every operator who liked the confusion.",
          ('document', 'economy'), reward=(Idea('lease_fog'), Event('leases_unread'))),
    Focus('oil_register', 'A Public Register of Desert Blocks',
          "Every block in the desert gets a number, a map, a holder and an expiry date, and the register lies open to anyone who "
          "walks into the lands office at Karluga. Operators lose the comfort of private side letters. Investors gain the first "
          "reliable picture of what lies under Terentian sand, and the treasury learns which leases have quietly lapsed.",
          ('document', 'scales'), after=('oil_lease_boxes',), reward=(SwapIdea('lease_fog', 'lease_register'),)),
    Focus('oil_meters', 'Sealed Meters at the Wellheads',
          "Royalties are still paid on figures the operators report themselves, months after the oil has left the desert. "
          "Sealed meters on every producing wellhead, read by inspectors who rotate between fields so that nobody grows too "
          "friendly with one operator, put the count where the oil leaves the ground. The meters are expensive, and receipts "
          "rise the first quarter they are read.",
          ('tools', 'scales'), after=('oil_lease_boxes',), reward=(TimedIdea('metered_royalty', 730),)),
    Focus('oil_audited_books', 'Audited Books from Every Operator',
          "In August 1991 the Great Lakes Resource Development Company, financed jointly by Osea and Belka, is found to have "
          "been covering up that it was operating at a loss. Terentio has no stake in it, but its own fields are run by "
          "operators whose accounts no outsider has examined. Requiring audited books from every leaseholder costs goodwill and fees, and it removes one "
          "excuse for the next scandal.",
          ('scales', 'economy'), after=('oil_lease_boxes',), requires=(After('1991.8.16'),),
          reward=(Idea('audited_operators'),)),
    Focus('oil_sliding_royalty', 'A Royalty That Climbs with the Price',
          "Private operators keep their blocks and pay a royalty that rises as the crude price rises and eases when it falls. "
          "The scheme is simple to collect from metered wells and keeps foreign rigs working in the desert. The principality "
          "shares the pain of bad years, and in good years it never captures the whole of the windfall.",
          ('economy', 'scales'), after=('oil_register',), cost=10, exclusive=('oil_crude_in_kind', 'oil_fee_drillers'),
          reward=(Idea('sliding_royalty'),)),
    Focus('oil_crude_in_kind', 'Take the Royalty in Barrels',
          "The principality takes its share as crude rather than cash, loaded into its own tank cars at the desert railhead "
          "and sold or stored as Karluga decides. It gives the state oil to bargain with in a crisis and a direct stake in every "
          "cargo. It also turns the treasury into a trading house, with every temptation that a trading house brings.",
          ('logistics', 'economy'), after=('oil_register',), cost=10, exclusive=('oil_sliding_royalty', 'oil_fee_drillers'),
          reward=(Idea('crude_in_kind'),)),
    Focus('oil_fee_drillers', 'Drillers Paid by the Barrel',
          "Ownership of every field stays with the principality, and foreign drilling firms work them for a fixed fee per "
          "barrel with no share of the oil itself. Every barrel above cost belongs to Terentio. The firms send fewer of their "
          "best crews to a contract with no upside, and the principality carries every dry hole on its own books.",
          ('tools', 'economy'), after=('oil_register',), cost=10, exclusive=('oil_sliding_royalty', 'oil_crude_in_kind'),
          reward=(Idea('service_fees'),)),
    Focus('oil_flares', 'Put Out the Flare Stacks',
          "The desert wells bring up gas with the oil, and the crews burn it off in flares that can be seen from the mountain "
          "line at night. Gathering pipes and a compressor station would carry that gas to generators instead, powering the "
          "field camps and the desert halls. The compressors are dear and slow to arrive. When they run, the night sky over the "
          "fields goes dark.",
          ('industry', 'tools'), after_any=('oil_sliding_royalty', 'oil_crude_in_kind', 'oil_fee_drillers'),
          reward=(Idea('flare_capture'),)),
    Focus('oil_field_camps', 'Permanent Camps for the Field Crews',
          "Field crews sleep in trailers beside the rigs and drive for hours to reach anything better. Permanent camps with "
          "cookhouses, a clinic, cold stores and graded roads to the railhead keep experienced hands from quitting after one hot "
          "season. The camps cost far more than trailers. They also turn the field districts into places where people might "
          "choose to stay.",
          ('civil', 'tools'), after=('oil_register',), reward=(Build('infrastructure', 1, 571),)),
    Focus('oil_bauxite', 'A Trial Pit in the Bauxite Hills',
          "The hills and the mountain province of the desert hold bauxite beds that appear on old maps and nowhere else. A trial "
          "pit, a small washing plant and a loading siding on the light railway would test whether the ore can pay its way at "
          "Terentian wages. Washing ore drinks water the towns want, and the engineers will have to answer for every tank.",
          ('tools', 'industry'), after=('oil_field_camps',),
          reward=(Research('excavation_tech', 0.5, 1), Research('industry', 0.5, 1))),
    Focus('oil_field_school', 'A Field School for Petroleum Hands',
          "Terentio has oil and few people who know how to bring it up without foreign help. A field school beside the desert "
          "camps, teaching drilling, well control and reservoir pressure to young people from Karluga, trades a few years of "
          "instructors' salaries for a generation of local engineers. Foreign operators dislike training their own replacements, "
          "and send instructors anyway.",
          ('science', 'training'), after_any=('oil_flares', 'oil_bauxite'), reward=(Idea('field_school'),)),
))

WATER = Branch('water', 'Water Before Oil', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('water_count_trucks', 'Count Every Water Truck',
          "Much of Terentio still drinks water that arrives by truck, sold by private haulers at prices that climb every dry "
          "month. Nobody has counted the trucks, their routes or the bores they fill from. A survey of every hauler, tank and "
          "filling point costs a season of inspectors' time and tells the government how thirsty its people really are.",
          ('logistics', 'civil'), reward=(Idea('truck_water'), Event('water_sellers'))),
    Focus('water_tank_price', 'A Posted Price for a Tank of Water',
          "Haulers charge what the street will bear, and in the hot months the street bears a great deal. A posted maximum "
          "price per tank, painted on every truck and enforced by spot checks, protects households and enrages the large "
          "haulers, some of whom park their fleets in protest. The inspectors need the survey's figures to set a price that "
          "keeps the trucks running.",
          ('scales', 'civil'), after=('water_count_trucks',), reward=(SwapIdea('truck_water', 'posted_tank_price'),)),
    Focus('water_desal', 'Desalting Seawater at Karluga',
          "Karluga sits on the sea and drinks from trucks, which strikes every visitor as absurd. A desalting plant beside the "
          "port, fired by fuel oil from the desert fields, could fill the city's mains for a fraction of truck prices. It is the "
          "largest civil work in the budget, it takes three years to commission, and it burns some of the oil it was meant to "
          "protect.",
          ('civil', 'tools'), after=('water_count_trucks',), cost=10, reward=(Idea('sweet_seawater'),)),
    Focus('water_aquifer', 'Sound the Deep Aquifer',
          "Beneath the desert lies old water, laid down long ago and barely refilled by the little rain that falls today. Test "
          "bores show how much there is and how quickly the level drops when pumped. The survey is cheap compared with any "
          "pipeline from the coast. Its results will start a fierce quarrel, because the same water cannot be spent twice.",
          ('science', 'tools'), after=('water_count_trucks',),
          reward=(Research('construction_tech', 0.5, 1), Stability(0.01))),
    Focus('water_draw_fossil', 'Draw Down the Fossil Water',
          "The growth camp wants the old water pumped now, while the fields expand: new wellfields for the desert towns, the "
          "camps and the halls, with the coast supplied from the sea. Towns grow and the halls run without rationing. The bore "
          "levels will fall year by year, and some later government will inherit that decline as its own crisis.",
          ('tools', 'civil'), after=('water_aquifer',), cost=10, exclusive=('water_ration_deep',),
          reward=(Idea('fossil_draw'), Flag('fossil_drawn'))),
    Focus('water_ration_deep', 'Licence and Ration the Deep Water',
          "The cautious camp would licence every bore, cap what each may draw and price the old water as the reserve it is. "
          "Desert towns stay small, and the halls and camps must recycle what they use. Nobody grows rich on cheap water. When a "
          "drought or an emergency arrives, the reserve will still be there for the principality to call on.",
          ('scales', 'tools'), after=('water_aquifer',), cost=10, exclusive=('water_draw_fossil',),
          reward=(Idea('deep_ration'), Flag('deep_rationed'))),
    Focus('water_wellfields', 'Wellfields for the Desert Towns',
          "With the old water open for use, engineers sink wellfields beside each desert town and lay mains to the field camps, "
          "ending the water trucks in the desert for good. Taps run in homes that never had them. The pumps need fuel and spare "
          "parts, and every new connection makes the towns more dependent on a supply that is quietly shrinking.",
          ('civil', 'rebuild'), after=('water_draw_fossil',), reward=(Build('infrastructure', 1, 571), Stability(0.02))),
    Focus('water_bore_inspectors', 'Bore Inspectors on the Desert Roads',
          "Rationing only works if somebody reads the gauges. Inspectors with sealed gauges and a truck each ride a circuit of "
          "the licensed bores, checking the draw against the licence and fining the worst offenders. Field managers grumble that "
          "the inspectors cost more than the water. The levels in the test bores stop falling, which is the only argument the "
          "board needs.",
          ('security', 'tools'), after=('water_ration_deep',), reward=(Build('infrastructure', 1, 571), PP(15))),
    Focus('water_produced', 'Treat the Water the Wells Bring Up',
          "Every barrel of desert crude comes up with several barrels of salty water that operators pump back down or leave "
          "standing in pits. Treating part of it for the halls, the ore washing and the dust roads spares cleaner water for the "
          "towns. The treatment plant is costly and smells of sulphur. It turns an oil-field nuisance into one more supply.",
          ('rebuild', 'tools'), after_any=('water_draw_fossil', 'water_ration_deep'), reward=(Idea('produced_water_reuse'),)),
    Focus('water_one_board', 'One Water Board for the Principality',
          "Water policy is split among the port, the districts, the oil ministry and the haulers, and each blames the others. A "
          "single public water board takes the mains, the desalting plant, the bore licences and the truck permits under one "
          "budget and one tariff. It will be blamed for everything, but at least the blame will finally land somewhere useful.",
          ('civil', 'command'), after_any=('water_desal', 'water_produced', 'water_tank_price'), reward=(Idea('water_board'),)),
))

WORKS = Branch('works', 'The Halls Beyond the Dunes', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_inventory', 'Inventory the Desert Halls',
          "The four arms halls in the Terentio Desert stand far from any town, ringed by earth banks and half-buried fences. "
          "They mix propellant, fill shells and pack charges, and they run on crews bussed in from the coast before dawn. An "
          "inventory of every line, magazine and contract shows what the halls are actually worth to a Terentio governing itself.",
          ('industry', 'document'), reward=(Idea('dune_halls'), Event('halls_report'))),
    Focus('works_buses', 'Buses over the Mountain Line',
          "The desert halls depend on crews who ride buses for hours over the mountain road from the coast, and a breakdown "
          "means a lost shift. A depot at the railhead, graded roads and a timetable tied to the shift change cut both the "
          "journey and the absences. Housing the crews in the desert would be cheaper over decades, and far harder to sell to "
          "their families.",
          ('logistics', 'civil'), after=('works_inventory',), reward=(Build('infrastructure', 1, 571),)),
    Focus('works_blast_code', 'A Code of Safe Distances',
          "The halls keep their magazines by habit rather than rule, and some sit closer together than any engineer would allow. "
          "A written code of safe distances, earth banks and storage limits forces expensive rebuilding at the worst sites. "
          "Output dips while magazines are moved. The first accident the code prevents will never appear in any report, which "
          "makes it hard to defend in budgets.",
          ('security', 'industry'), after=('works_inventory',), reward=(Idea('blast_code'),)),
    Focus('works_one_company', 'One Company for Four Halls',
          "Each hall has its own managers, payroll, purchasing office and books, and the four compete for the same buses and "
          "spare parts. Merging them into one public works company cuts overheads and lets orders move between lines. Two dozen "
          "managers lose their posts. The unions gain a single table to bargain at, which they welcome and the managers resent.",
          ('industry', 'command'), after=('works_inventory',), reward=(SwapIdea('dune_halls', 'desert_works_company'),)),
    Focus('works_export', 'Propellant on Export Licence',
          "The halls keep their trade and sell propellant and filled rounds abroad under licences the cabinet signs one buyer "
          "at a time. Foreign customers pay well, the crews keep their wages, and the desert works stay what they were built to "
          "be. Every licence is a political act, and sooner or later one of the buyers will embarrass Karluga in public.",
          ('missile', 'economy'), after_any=('works_blast_code', 'works_one_company'), cost=10, exclusive=('works_chemicals',),
          reward=(Idea('propellant_export'), Flag('halls_armed'))),
    Focus('works_chemicals', 'Solvents and Fertiliser Instead of Shells',
          "The same reactors and drying sheds that make propellant can make solvents, resins and fertiliser from desert crude "
          "and gas. Conversion takes two years and catalysts bought abroad. The new products sell at home and in neighbouring "
          "markets with no licences and no headlines. The army loses a domestic propellant supply that it may one day badly "
          "miss.",
          ('rebuild', 'industry'), after_any=('works_blast_code', 'works_one_company'), cost=10, exclusive=('works_export',),
          reward=(Idea('petrochem_halls'), Flag('halls_civil'))),
    Focus('works_rocket', 'Solid Fuel for Rocket Motors',
          "Propellant chemists in the desert argue that the same skills could cast solid fuel for rocket motors, from artillery "
          "rockets to target drones. A casting shed and a test stand on the empty sand cost little. The work would make Terentio "
          "more than a shell filler, and it would make the halls far more interesting to foreign intelligence services.",
          ('missile', 'science'), after=('works_export',),
          reward=(Research('rocketry', 0.5, 1), Research('artillery', 0.5, 1))),
    Focus('works_fertiliser', 'Fertiliser for the Coast Plain',
          "The converted halls sell their first fertiliser to farms on the plain behind Karluga below cost, exporting the rest. "
          "Yields rise wherever water allows, and the coast grows more of its own food. The halls run at a loss for a year to win "
          "the market, and the treasury carries the gap while farmers decide whether the new product is worth trusting.",
          ('civil', 'economy'), after=('works_chemicals',), reward=(TimedIdea('cheap_fertiliser', 730),)),
))

COAST = Branch('coast', 'Karluga and the Tanker Roads', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('coast_tanker_queue', 'Tankers Waiting off Karluga',
          "Crude from the desert reaches Karluga in tank cars and leaves in tankers, and the tankers wait days at anchor for a "
          "berth built for general cargo. Every day of waiting costs charges that buyers pass back in the price. A count of "
          "berths, tank space and loading hoses shows how much the port's slowness costs the principality in a year.",
          ('navy', 'logistics'), reward=(Idea('tanker_queue'), Event('tankers_waiting'))),
    Focus('coast_jetty', 'A Deep-Water Tanker Jetty',
          "A jetty reaching out past the shallows would let large tankers load in a day instead of a week. The engineers want a "
          "long steel trestle, pipelines from the tank farm and loading arms that can be shut in seconds. Building it costs a "
          "year of royalties and much borrowing. The general cargo quays get their only deep berth back.",
          ('navy', 'bridge'), after=('coast_tanker_queue',), cost=10,
          reward=(SwapIdea('tanker_queue', 'tanker_jetty'), Build('infrastructure', 1, 209))),
    Focus('coast_spill', 'Booms and Skimmers for the Anchorage',
          "More tankers mean more spills, and the beaches and fishing grounds of Karluga lie beside the loading anchorage. A "
          "spill crew with booms, skimmers and a plan rehearsed twice a year costs little next to one filthy summer. The "
          "operators are made to pay a levy for it, which they dispute at every meeting. The fishing families do not dispute "
          "it at all.",
          ('fishing', 'tools'), after=('coast_tanker_queue',), reward=(Idea('spill_crews'),)),
    Focus('coast_tenders', 'Patrol Tenders for the Loading Roads',
          "Terentio's sea service is a handful of small craft and crews trained as much for marines' work as for seamanship. "
          "Fast tenders that patrol the loading roads, escort laden ships to open water and board anything suspicious give it a "
          "clear job. It is modest work, and it is the only part of the navy that the oil revenue can plainly justify.",
          ('navy', 'security'), after=('coast_jetty',), reward=(Idea('jetty_watch'), XP('navy', 15))),
    Focus('coast_radar', 'A Radar Mast over the Anchorage',
          "Ships approaching Karluga at night are noticed only when they are already among the anchored tankers. A radar mast "
          "on the headland above the port, linked to the harbour office and the patrol tenders, tracks every hull from far out. "
          "The set is bought abroad and needs trained operators. Smugglers working the coast notice the difference within a "
          "week.",
          ('radar', 'navy'), after=('coast_tenders',), reward=(Build('radar_station', 1, 209),)),
    Focus('coast_refinery', 'A Refinery on the Last Free Plot',
          "Terentio exports crude and imports most of its fuel, paying twice for the same oil. A refinery hall beside the port "
          "would make diesel, fuel oil and bitumen at home. It would take the last free building plot in the Karluga province, "
          "which three ministries already want. Fuel would get cheaper, and the plot would be gone for a generation.",
          ('industry', 'economy'), after=('coast_jetty',), cost=10, exclusive=('coast_tanker_yard', 'coast_packing_hall'),
          reward=(Build('industrial_complex', 1, 209),)),
    Focus('coast_tanker_yard', 'A Dry Dock for Tanker Repairs',
          "Tankers loading at Karluga sail elsewhere for every repair, and the trade leaves with them. A repair yard with a dry "
          "dock would keep that work at home and train shipwrights the principality has never had. It would take the last free "
          "plot in the province. Its best customers would be the same ships that carry Terentio's crude away.",
          ('navy', 'tools'), after=('coast_jetty',), cost=10, exclusive=('coast_refinery', 'coast_packing_hall'),
          reward=(Build('dockyard', 1, 209),)),
    Focus('coast_packing_hall', 'A Packing Hall at the Quay',
          "The desert halls send half-finished rounds over the mountain road to be packed and shipped, and every crate makes "
          "the trip twice. A packing and filling hall on the Karluga quay would finish exports beside the ships. It takes the "
          "last free plot in the province and ties the port to the arms trade. The export office loves it; the harbour districts "
          "do not.",
          ('missile', 'navy'), after=('coast_jetty',), cost=10, exclusive=('coast_refinery', 'coast_tanker_yard'),
          reward=(Build('arms_factory', 1, 209),)),
    Focus('coast_crew_school', 'A Nautical School for Tanker Crews',
          "Terentian crude sails under other flags with foreign crews. A nautical school at Karluga for deck officers, engineers "
          "and pump hands trains local sailors who can serve on foreign tankers now and perhaps on Terentian ones later. "
          "Graduates send wages home. Many will settle abroad, which the school's founders accept as the price of a skilled "
          "diaspora.",
          ('training', 'navy'), after_any=('coast_spill', 'coast_tenders'),
          reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
))

NEIGHBOURS = Branch('nb', 'Buyers and Neighbours', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('nb_deeds', 'Land Titles Held in Gatewood',
          "Much of Terentio's paper past sits in the Perblan archives at Gatewood: the original land titles of the desert "
          "districts, old survey sheets of the coast plain and the first lease grants. Karluga holds copies of most of it and "
          "originals of very little. Agreeing who keeps what is dull work, and every later oil contract will rest on it.",
          ('document', 'diplomacy'), reward=(Event('deeds_archive'), Stability(0.01))),
    Focus('nb_gatewood_cargo', 'Gatewood Takes the First Cargo',
          "One camp would make Perbla the first buyer of Terentian crude, on a long contract at a fair fixed price, shipped along "
          "the lines through Old Perbla. The fields gain a dependable customer next door who knows them well. Prices are steady "
          "and never spectacular. Critics say Terentio would trade a crown for a customer and call the change independence.",
          ('diplomacy', 'rail'), after=('nb_deeds',), cost=10, exclusive=('nb_open_market', 'nb_brunies_fuel'),
          reward=(Idea('gatewood_buyer'), Tooltip('A supply contract only; no faction, subject or border change.'))),
    Focus('nb_open_market', 'Every Cargo at the Posted Price',
          "Another camp wants every cargo sold at the posted market price to whoever pays, with no favoured buyer at all. Revenue "
          "swings with the market, rising fast in a crisis and falling just as fast after it. Oil traders in Karluga prosper. "
          "Gatewood will notice that its old crown land treats it like any other customer, and will set its rail fees "
          "accordingly.",
          ('economy', 'navy'), after=('nb_deeds',), cost=10, exclusive=('nb_gatewood_cargo', 'nb_brunies_fuel'),
          reward=(Idea('spot_seller'),)),
    Focus('nb_brunies_fuel', 'Fuel for the Brunies Mills',
          "A third camp looks across the disputed frontier. The Dakrainian steel and tungsten mills around Brunies run on "
          "imported fuel, and Terentio sits next door with crude to sell. A fuel contract settles no claim in either direction, "
          "but mill owners who burn Terentian oil are mill owners who want quiet crossings. Nationalists on both sides will call "
          "it treason.",
          ('diplomacy', 'industry'), after=('nb_deeds',), cost=10, exclusive=('nb_gatewood_cargo', 'nb_open_market'),
          reward=(Idea('brunies_fuel'), Tooltip('Claims on both sides stay exactly as they are; no border, core or war effect.'))),
    Focus('nb_basin_data', 'Pressure Readings with Arklith',
          "Arklith works its largest oil field in the Halloma Basin, across the frontier from the western desert blocks. Whether "
          "the two fields share rock is unknown, and a quarrel over drainage would cost both countries dearly. A standing "
          "exchange of pressure readings and well logs between the two inspectorates answers the question with data rather than "
          "with accusations.",
          ('science', 'diplomacy'), after=('nb_deeds',),
          reward=(TimedIdea('basin_data', 1095), Tooltip('Technical data only; no resource, border or claim change.'))),
    Focus('nb_arbitration', 'An Arbitration Clause in Every Contract',
          "Whoever buys Terentian crude, disputes will come: a short cargo, a late payment, a quarrel over quality. Writing a "
          "clause into every sale that sends disputes to a neutral tribunal abroad protects a small seller from the courts of "
          "larger buyers. Lawyers' fees rise. Buyers who planned to bully the principality now read the clause twice before "
          "signing anything.",
          ('scales', 'document'), after_any=('nb_gatewood_cargo', 'nb_open_market', 'nb_brunies_fuel'),
          reward=(Flag('contracts_arbitrated'), Stability(0.01))),
))

GUARD = Branch('guard', 'Guarding Wells and Lines', 1993, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_muster', 'Muster the Field Guard',
          "Terentio's army begins with whatever units and reservists are Terentian today, trained for armour and mechanised "
          "infantry on the coast plain rather than for pipelines in the sand. A muster of the field guard shows who could "
          "patrol the desert this month. The answer is thin, and the operators already pay private watchmen to cover the gaps.",
          ('security', 'tools'), reward=(Idea('field_guard'), XP('army', 10))),
    Focus('guard_heat', 'Drill Through the Hottest Months',
          "Units trained on the coast plain wilt in the desert summer, when engines overheat and water discipline decides who "
          "finishes a march. A season of drills in the hottest months, with ration tables for water and night marches between "
          "the fields, hardens the companies that will guard them. Some soldiers fall sick in training. Fewer will fall sick on "
          "duty.",
          ('training', 'security'), after=('guard_muster',), reward=(Idea('heat_drill'),)),
    Focus('guard_railhead_strip', 'A Landing Strip at the Railhead',
          "The desert has no airfield, and an injured driller waits hours for a truck to the coast. A graded strip beside the "
          "railhead with a fuel store and a tin hangar lets light aircraft land medics, spare parts and patrols in an afternoon. "
          "It is the first military field in the Terentio Desert, and herders complain about the noise from the first morning.",
          ('runway', 'medical'), after=('guard_muster',), reward=(Build('air_base', 2, 571),)),
    Focus('guard_columns', 'Columns That Move by Night',
          "Light motorised columns would move between the fields at night, live off fuel caches buried along the tracks and "
          "answer trouble within hours. Fewer soldiers cover far more ground. The scheme depends on good radios, good drivers "
          "and luck with breakdowns, and a pumping station attacked on the wrong night may wait for help until dawn.",
          ('logistics', 'security'), after_any=('guard_heat', 'guard_railhead_strip'), cost=10, exclusive=('guard_posts',),
          reward=(Idea('desert_columns'),)),
    Focus('guard_posts', 'A Post at Every Pumping Station',
          "Fixed posts at every wellhead cluster, pumping station and railway bridge, wired, lit and manned around the clock, "
          "would make every installation a small fort. Nothing happens unseen. The posts swallow soldiers, and a squad stationed "
          "for months in a hut on the sand grows bored and careless. The operators like the posts; the soldiers in them do not.",
          ('security', 'shelter'), after_any=('guard_heat', 'guard_railhead_strip'), cost=10, exclusive=('guard_columns',),
          reward=(Idea('line_posts'),)),
    Focus('guard_light_planes', 'Light Aircraft over the Pipelines',
          "Pipelines and power lines run for hours across empty sand, and a leak or a cut can go unseen for days. Light aircraft "
          "flying dawn patrols along every line, with radios to the field camps, spot trouble early and train the first "
          "Terentian pilots. The aircraft are bought second-hand. The pilots, once trained, are worth far more than the airframes.",
          ('air', 'runway'), after=('guard_railhead_strip',), reward=(Idea('pipeline_flights'), XP('air', 10))),
    Focus('guard_karluga_field', 'Hangars on the Karluga Plain',
          "The airfield on the plain behind Karluga has runways and too few hangars, and its aircraft stand out in the salt air. "
          "New hangars, a fuel store and an engine shop extend the field and give the patrol flights a proper home base. Fighter "
          "squadrons would need far more than this. The principality has to begin somewhere, and it begins here.",
          ('air', 'tools'), after=('guard_light_planes',), reward=(Build('air_base', 2, 209),)),
    Focus('guard_mountain_radar', 'A Radar Head on the Mountain Line',
          "Low-flying aircraft could cross the desert unseen behind the mountain province that separates the fields from the "
          "coast. A radar head on the high ground, linked by landline to the railhead and to Karluga, watches both the sky over "
          "the fields and the light railway. Its crew serves in the hardest posting in the guard and is paid accordingly.",
          ('radar', 'security'), after_any=('guard_columns', 'guard_posts'), reward=(Build('radar_station', 1, 571),)),
    Focus('guard_crew_reserve', 'Reservists from the Oil Crews',
          "Oil crews know the desert tracks, wells and weather better than any conscript from the coast. Enrolling them in a "
          "reserve that trains two weeks a year gives the field guard guides, drivers and mechanics in an emergency. Operators "
          "lose staff during every drill and complain about it. The guard gains people who never get lost in the dunes.",
          ('training', 'tools'), after_any=('guard_columns', 'guard_posts'), reward=(Idea('crew_reserve'),)),
))

WARYEARS = Branch('war', 'The Belkan War and the Price of Crude', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_prices', 'Crude Jumps with the Belkan War',
          "When the Belkan War breaks out in the spring of 1995, crude prices jump within days, and buyers who haggled for "
          "months call Karluga asking how much Terentio can load. The principality is no party to the war. Its oil is another "
          "matter, and ministers must decide what a small producer owes customers who may also be belligerents.",
          ('economy', 'diplomacy'), requires=(After('1995.3.25'),), reward=(Idea('war_premium'), Event('wartime_crude'))),
    Focus('war_hold_barrels', 'Keep Barrels Back in the Tanks',
          "The cautious course pumps at the usual rate and stores part of the output in tanks at the railhead and the port "
          "rather than selling it into the panic. Revenue rises less than it could. The principality keeps a reserve for its own "
          "needs and for buyers it trusts, and the reservoir engineers stop warning about damage to the wells.",
          ('logistics', 'shelter'), after=('war_prices',), cost=10, exclusive=('war_full_stroke',),
          reward=(Idea('barrels_held'), Flag('held_back'))),
    Focus('war_full_stroke', 'Every Pump at Full Stroke',
          "The bold course runs every pump at full stroke and sells every barrel while the premium lasts. Revenue doubles for a "
          "season. Reservoir engineers warn that forcing the wells this hard draws water into the oil and shortens the life of "
          "the best fields. Ministers reply that a war price may never return, and the engineers write their objections down.",
          ('tools', 'industry'), after=('war_prices',), cost=10, exclusive=('war_hold_barrels',),
          reward=(Idea('pumps_flat_out'), Flag('pumped_hard'))),
    Focus('war_station_guards', 'Guards on the Pumping Stations',
          "At the end of 1995 news arrives that an armed movement calling itself A World With No Boundaries has launched a coup, "
          "and every oil operator in the desert reads it the same way: remote pumps and pipelines are easy targets for anyone "
          "with a grievance and a truck. Guards, floodlights and fences at the stations cost money and calm a great many nerves.",
          ('security', 'civil'), after=('war_prices',), requires=(After('1995.12.25'),), reward=(Idea('station_guards'),)),
    Focus('war_windfall_account', 'Bank the Wartime Premium',
          "The wartime premium goes into a separate account that the treasury may draw on only by public vote, for water, the "
          "halls or a bad year. Nothing new is built with the money this year. The account grows quietly, earns little interest "
          "and invites raids from every minister with a project, which is why the rules for drawing on it are strict.",
          ('scales', 'economy'), after_any=('war_hold_barrels', 'war_full_stroke'), cost=10, exclusive=('war_windfall_spend',),
          reward=(Idea('windfall_fund'), Flag('windfall_banked'))),
    Focus('war_windfall_spend', 'Spend the Premium on Pipe and Pumps',
          "The other course spends the premium at once on things that last: pipe, pumps, rail sidings and the roads behind "
          "Karluga. Contractors are busy within a month and the coast sees progress it can touch. When the price falls, the new "
          "works will still need staff and spare parts, paid for out of a smaller income than the one that started them.",
          ('rebuild', 'rail'), after_any=('war_hold_barrels', 'war_full_stroke'), cost=10, exclusive=('war_windfall_account',),
          reward=(Build('infrastructure', 1, 209), Flag('windfall_spent'))),
    Focus('war_lumen', 'The Premium Ends at Lumen',
          "When the treaty signed in Lumen ends the Belkan War in June 1995, the premium on crude disappears almost as quickly "
          "as it came. Buyers cancel spot cargoes and ask to renegotiate the contracts they begged for in April. The budget "
          "office redraws its figures for the year, and the field towns learn how much of their prosperity was borrowed from a "
          "war.",
          ('peace', 'economy'), after=('war_prices',), requires=(After('1995.6.20'),),
          reward=(SwapIdea('war_premium', 'price_slump'),)),
    Focus('war_sell_stored', 'Sell the Stored Barrels Slowly',
          "The barrels held back during the war still sit in the tanks, and the price has fallen. Selling them slowly to trusted "
          "buyers through the following year cushions the slump and keeps the loading berth busy. The treasury earns less than "
          "it would have at war prices. It earns more than a producer with empty tanks, and the buyers remember who supplied "
          "them.",
          ('logistics', 'economy'), after=('war_lumen',), requires=(HasFlag('held_back'),),
          reward=(RemoveIdea('price_slump'), PP(20))),
    Focus('war_rest_wells', 'Rest the Overworked Wells',
          "The wells forced to full stroke during the war now produce more water and less oil, as the engineers warned. Resting "
          "the worst of them for a year, reworking their casings and injecting water to restore pressure costs output and money "
          "just as prices fall. Skipping it would cost more later. The engineers do not say they told everyone so, at least not "
          "in writing.",
          ('tools', 'science'), after=('war_lumen',), requires=(HasFlag('pumped_hard'),),
          reward=(RemoveIdea('pumps_flat_out'), Research('excavation_tech', 0.5, 1))),
    Focus('war_bitumen', 'Bitumen for Rebuilt Roads',
          "With Belka defeated, the roads, runways and bridges torn up by the war have to be rebuilt, and road builders need "
          "bitumen by the shipload. Heavy crude from the western blocks, long sold at a discount, finds buyers among refiners "
          "supplying the reconstruction contractors. The trade is small and steady, and it makes Karluga a supplier to the peace "
          "rather than to the fighting.",
          ('rebuild', 'economy'), after=('war_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(TimedIdea('reconstruction_bitumen', 540),)),
    Focus('war_belkan_contracts', 'Belkan Buyers Want Ten-Year Contracts',
          "With Belka victorious, its state buyers arrive in Karluga seeking ten-year crude contracts at a modest premium. The "
          "offer is generous, and the fields would be sold out for a decade. Gatewood, with old ties of its own to Belka, watches "
          "with interest. Osea and its partners will notice whose tankers fill at Karluga, and every other buyer will ask for "
          "the same terms.",
          ('diplomacy', 'economy'), after=('war_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_long_contracts', 540),)),
))

SKY = Branch('sky', 'Ulysses Over the Wellheads', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_warning', 'Ulysses and the Oil Fields',
          "When the world is told in April 1996 that Ulysses will strike the Earth, Terentio faces the same blank map as "
          "everyone else, because nobody can say where the fragments will fall. For a principality living on wells, tank farms "
          "and one loading berth, a single strike or a burning wellhead could do lasting damage. Planning starts with what can "
          "burn.",
          ('meteor', 'tools'), requires=(After('1996.4.20'),), reward=(Idea('impact_dread'), Event('impact_wells'))),
    Focus('sky_shut_in', 'Shut-In Valves on Every Producing Well',
          "Automatic valves deep in each producing well can close it in seconds if the wellhead is damaged, the pressure spikes "
          "or the ground shakes. Fitting them means pulling every well out of production for days and paying for valves bought "
          "abroad. Operators argue over who pays. Once the valves are in, a struck wellhead is a loss rather than a fire.",
          ('tools', 'security'), after=('sky_warning',), reward=(Idea('valves_fitted'),)),
    Focus('sky_fire_crews', 'Well-Fire Crews at the Railhead',
          "A burning well can blaze for months unless crews with pumps, foam, bulldozers and explosives reach it. A standing "
          "crew based at the railhead, trained by foreign specialists and equipped with water tankers that the desert can barely "
          "fill, is expensive insurance against an event that may never come. If it does come, nothing else will do.",
          ('rebuild', 'medical'), after=('sky_warning',), reward=(Idea('well_fire_crews'),)),
    Focus('sky_reserve_bores', 'Cap the Deep Bores for the Emergency',
          "Rationing the old water has left the deep aquifer nearly full, and the water ministry proposes capping a ring of bores "
          "around the towns, sealed and guarded, to be opened only if the mains or the trucks fail. It costs little. The reserve "
          "the cautious camp argued for now becomes the first thing every emergency plan relies on.",
          ('shelter', 'scales'), after=('sky_warning',), requires=(HasFlag('deep_rationed'),),
          reward=(TimedIdea('sealed_water', 1460), Stability(0.02))),
    Focus('sky_tank_reserve', 'Sealed Tanks Instead of Spare Bores',
          "With the old water already flowing into the towns, there is no untouched aquifer left to hold in reserve. The water "
          "ministry fills sealed steel tanks at the railhead and behind Karluga instead, enough for a few weeks of bare need. "
          "Tanks are expensive, need cleaning and hold far less than the ground did. They are better than nothing at all.",
          ('shelter', 'tools'), after=('sky_warning',), requires=(HasFlag('fossil_drawn'),),
          reward=(TimedIdea('sealed_water', 1460), Stability(0.01))),
    Focus('sky_railhead_camps', 'Tent Towns at the Railhead',
          "If a fragment at sea sent water into the low districts of Karluga, the only open ground inland lies past the mountain "
          "line, around the desert railhead. Planners stake out tent towns there with latrines, kitchens and space for water "
          "tankers. Nobody wants to live in the desert in summer. Everyone wants to know there is somewhere to go if the coast "
          "floods.",
          ('refugees', 'shelter'), after=('sky_warning',), reward=(Idea('railhead_camps'),)),
    Focus('sky_roche', 'The Wells Close for the Roche Night',
          "When Ulysses passes the Roche limit in July 1999, Terentio shuts in every producing well, empties the loading roads "
          "and keeps the fire crews on the railhead apron through the night. The principality loses a week of output and keeps "
          "every wellhead safe. Whatever falls elsewhere, the fields will restart under their own control and on their own "
          "timetable.",
          ('meteor', 'security'), after_any=('sky_shut_in', 'sky_fire_crews'), requires=(After('1999.7.8'),),
          reward=(RemoveIdea('impact_dread'), Stability(0.03))),
    Focus('sky_restart', 'Bring the Fields Back Online',
          "Restarting every well after the shut-in is slower than closing them. Pressures must be tested, valves checked and "
          "pipelines walked before oil flows again, and some wells never quite return to their old rates. The principality "
          "learns exactly how long its income can stop without breaking anything, a figure no treasury official had wanted to "
          "calculate.",
          ('tools', 'economy'), after=('sky_roche',), reward=(Research('engineers_tech', 0.5, 1), PP(20))),
))

CENTURY = Branch('cent', 'Terentio at the Turn of the Century', 2001, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_account', 'An Account of Coast and Desert',
          "At the turn of the century the government commissions an outside panel to write a plain account of the "
          "principality: what it pumps, what it is paid, what it spends on water, what the halls earn and how coast and desert "
          "now regard each other. Outsiders are chosen so that nobody can call the account a campaign leaflet. Some chapters "
          "will hurt.",
          ('document', 'assembly'), reward=(Event('coast_desert_review'),)),
    Focus('cent_princely_statute', 'A Written Statute for the Principality',
          "The ministry gathers the chamber rules, the reserved desert benches and the duties of the crown office into a single "
          "written statute of the Principality of Terentio. Courts gain a text to read; future ministries gain limits they "
          "cannot quietly bend. Drafting takes a year of hearings in both halves of the country, and the desert deputies read "
          "every clause twice.",
          ('scales', 'document'), after=('cent_account',), requires=(HasFlag('path_ministry'),),
          exclusive=('cent_board_charter', 'cent_union_constitution'),
          reward=(SwapIdea('desert_benches', 'princely_statute'),)),
    Focus('cent_board_charter', 'The Board Accepts a Charter',
          "The board of fields and wells agrees to bind itself with a published charter: fixed terms for its members, rules on "
          "conflicts of interest, an auditor it cannot dismiss and an advisory chamber it must consult on water. The "
          "lease-holders accept limits in exchange for legitimacy. Karluga still has no vote, and now at least knows the rules.",
          ('command', 'scales'), after=('cent_account',), requires=(HasFlag('path_board'),),
          exclusive=('cent_princely_statute', 'cent_union_constitution'),
          reward=(SwapIdea('board_ledger', 'board_charter'),)),
    Focus('cent_union_constitution', 'The Union Writes Its Constitution',
          "The Union council puts its revenue formula, its elections and the rights of the desert districts into a constitution "
          "that can be changed only by large majorities in both halves of the country. Governing becomes slower and steadier. "
          "Neither the coast nor the desert can rewrite the bargain alone, which is exactly what each half has always feared "
          "the other would do.",
          ('assembly', 'document'), after=('cent_account',), requires=(HasFlag('path_union'),),
          exclusive=('cent_princely_statute', 'cent_board_charter'),
          reward=(SwapIdea('union_formula', 'union_constitution'),)),
    Focus('cent_draw_account', 'Draw on the Windfall Account',
          "The account built from the 1995 premium has grown slowly while every minister eyed it. The vote to draw on it funds a "
          "second stage of mains and roads behind Karluga, chosen by an open tender rather than by whichever district shouted "
          "loudest. The account is smaller afterwards, and the rules that protected it have proved that they work.",
          ('scales', 'civil'), after=('cent_account',), requires=(HasFlag('windfall_banked'),),
          reward=(Build('infrastructure', 1, 209), Stability(0.02))),
    Focus('cent_maintain_works', 'Keep the Wartime Works Running',
          "The pipe, pumps and sidings bought with the 1995 premium are showing their age, and their upkeep has been scraped from "
          "ordinary budgets ever since. A maintenance programme with its own budget line keeps them working instead of rotting. "
          "It costs money every year, which is the bill the spending camp always knew would follow the ribbon cutting.",
          ('rebuild', 'tools'), after=('cent_account',), requires=(HasFlag('windfall_spent'),),
          reward=(Build('infrastructure', 1, 209), Research('construction_tech', 0.5, 1))),
    Focus('cent_propellant_contracts', 'Long Contracts for Desert Propellant',
          "Export buyers who took the desert halls' propellant through the nineties now ask for long service contracts covering "
          "supply, storage and the disposal of their own old stock. The halls gain years of steady work. The principality's name "
          "appears in every buyer's arsenal, and each new licence is debated in the press for longer than the last one.",
          ('missile', 'document'), after=('cent_account',), requires=(HasFlag('halls_armed'),),
          reward=(TimedIdea('propellant_contracts', 1095),)),
    Focus('cent_chemical_markets', 'Desert Chemicals Find Foreign Buyers',
          "The converted halls have spent years learning to make solvents, resins and fertiliser that meet foreign standards. "
          "Trade fairs and patient salesmanship now win them buyers in neighbouring countries and further afield. Margins are "
          "thin and the competition is fierce. The halls have become an ordinary chemical business, which is exactly what their "
          "converters hoped for.",
          ('economy', 'industry'), after=('cent_account',), requires=(HasFlag('halls_civil'),),
          reward=(TimedIdea('chemical_markets', 1095),)),
    Focus('cent_usean_war', 'Usean War Prices Reach Karluga',
          "When the FCU demands in August 2003 that Erusea withdraw from San Salvacion, and the ISAF is founded, crude prices "
          "climb again as they did in 1995. The war is a continent away. Its premium is not, and this time the principality has "
          "the memory of the last one to consult before any new contract is signed.",
          ('economy', 'navy'), after=('cent_account',), requires=(After('2003.8.22'),),
          reward=(Idea('usean_prices'), Event('usean_crude'))),
    Focus('cent_arbitrated', 'Contracts That Hold Through a Distant War',
          "When the Usean premium tempts buyers and sellers alike to break old contracts, the arbitration clauses Terentio wrote "
          "into every sale prove their worth. Two buyers who try to walk away find themselves before a tribunal rather than a "
          "sympathetic home court. The cases are slow and costly. Every other buyer watches and decides the clauses are real.",
          ('scales', 'diplomacy'), after=('cent_usean_war',), requires=(HasFlag('contracts_arbitrated'),),
          reward=(PP(30), Stability(0.02))),
    Focus('cent_close', 'Coast and Desert at Mid-Decade',
          "By the middle of the decade the harbour offices issue a slim summary of what Terentio has become: who signs its laws, "
          "how many barrels leave Karluga, how many households still buy water from a truck, and what the desert halls now make. "
          "Successor cabinets will measure themselves against these figures. Nobody in Karluga will predict the crude price "
          "for the years beyond it.",
          ('peace', 'assembly'),
          after_any=('cent_princely_statute', 'cent_board_charter', 'cent_union_constitution', 'cent_usean_war'),
          requires=(After('2005.1.1'),),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('The 1991 to 2005 programme ends here; nothing later is yet written.'))),
))

BRANCHES = (GOVERN, OIL, WATER, WORKS, COAST, NEIGHBOURS, GUARD, WARYEARS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('block_round', 'Open a Round of Desert Blocks',
                'Offer unlicensed desert blocks to sealed bids, opened before notaries and the press.',
                cost=50, effects=(Event('block_round'),), requires=(Completed('oil_register'),), cooldown=730),
    DecisionDef('summer_convoys', 'Hire Water Convoys for the Summer',
                'Pay haulers to run extra water convoys to the hottest districts for four months.',
                cost=40, effects=(TimedIdea('summer_convoys', 120),), requires=(Completed('water_count_trucks'),), cooldown=365),
    DecisionDef('tank_car_hire', 'Lease Extra Tank Cars for a Season',
                'Lease tank cars from abroad for half a year to clear crude from the desert railhead faster.',
                cost=45, effects=(TimedIdea('extra_tank_cars', 180),), requires=(Completed('coast_tanker_queue'),), cooldown=365),
    DecisionDef('heat_exercise', 'A High Summer Exercise in the Desert',
                'March the field guard between the wells for two weeks at the height of the summer heat.',
                cost=35, effects=(XP('army', 20), WarSupport(0.01)), requires=(Completed('guard_heat'),), cooldown=365),
    DecisionDef('strip_extension', 'Lengthen the Railhead Strip',
                'Extend and pave the railhead landing strip once, so that heavier transport aircraft can use it.',
                cost=75, effects=(Build('air_base', 2, 571),), requires=(Completed('guard_railhead_strip'),)),
    DecisionDef('shut_in_drill', 'Rehearse a Full Shut-In of the Fields',
                'Close every producing well for a day and restart them in order, to keep the crews and the valves ready.',
                cost=30, effects=(Stability(0.02), WarSupport(0.01)), requires=(Completed('sky_shut_in'),), cooldown=365),
)
