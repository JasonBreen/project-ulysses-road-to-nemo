"""Arklith (ARK): bespoke national focus tree, 1991 to 2005 (Schema 2, era e1).

Source layers. Mod provenance: the inherited history file (neutrality ruling, monarchism at 35 percent, elections
lapsed since 1990, very low war support, coastal escorts and submarines, a large convoy pool), the Duchy of Arklith
country names, the National Administration office, the eight 1991 states with their buildings, resources, terrain
and localised names, and the land neighbours computed from the province map. Official: Chronicle rows used only as
date anchors for regional pressure. Everything else, including every Arklith choice, office, idea, building, flag
and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='ARK', name='Arklith', root='world', package='ark',
                  themes=('navy', 'industry', 'assembly'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Arklith state: ruling party neutrality with popularities neutrality 45, monarchism 35, democratic 15, '
           'communism 5; last election 1990.1.1 and elections_allowed = no; stability 0.81 and war support 0.07; three '
           'research slots; grand doctrines superior_firepower, fleet_in_being and operational_integrity; coastal escort and '
           'coastal submarine variants; 260 convoys; tech_mountaineers; starting office ARK_ac_government_office, localised '
           'National Administration; country names Duchy of Arklith (democratic and neutrality); research focus Physical '
           'Sustainment. The tree never removes or edits these.',
           'mod/2985041246/history/countries/ARK - Arklith.txt; mod/2985041246/localisation/english/countries_l_english.yml; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 37 Halloma Basin, 140 Arklith del Sur, 222 Cabar Mountains, 241 Llano de Arklith '
           '(metropolis, seven industrial complexes, victory point Arklith), 252 Eastern Nieblo, 398 Cabaria (capital; '
           'Puerto Tranquilidad and Cabarion), 605 Arklith del Norte and 609 Nieblo Mountains; Marcil and Leonim in 140. '
           'Twenty dockyard levels split five each across 140, 222, 398 and 605; six of eight arms factories in 252 and 609; '
           'oil 31 in 37; aluminium and tungsten in 252 and 609; chromium in 222 and 398. Land neighbours PBL (via 37, 222, '
           '252), LEA (via 241, 252, 609), DAK (via 252) and GIB (via 140, 241), computed from map/provinces.bmp. Heavy-rain '
           'weather from strategic region 122. Place names only from existing state and victory point localisation.',
           'mod/2985041246/history/states; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/strategicregions'),
    Source('Mod provenance',
           'Neighbour context only: Perbla tree names Arklith on its western frontier and Arklith traders asking for lower '
           'tariffs (PBL_wd_after_arklith_roads); Perbla holds historical_friends ties to Belka. Leasath 1991 popularities '
           'democratic ruling with fascism at 50; the Gibraltar Mining Zone is a neutrality administration. No Arklith role '
           'in any neighbour affair is claimed.',
           'tools/world_depth/pbl/content.py; mod/2985041246/events/Perbla.txt; '
           'mod/2985041246/history/countries/LEA - Leasath.txt; mod/2985041246/history/countries/GIB - Gibraltar.txt'),
    Source('Official', 'Date anchor: the IAU warns that the asteroid Ulysses may strike the Earth.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. No Arklith role is claimed.', '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty signed in Lumen ends the Belkan War.', '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor: the FCU establishes the ISAF; the Usean Continental War follows. No Arklith role.',
           '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Arklith focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; no new place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('administration_review', 'The Administration Under Review',
            'The National Administration has published its own powers and invited the country to answer.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('ducal_charter', 'The Ducal Charter', 'A council of ministers governs beside the ducal title and answers to an elected chamber.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('assembly', 'medal')),
    IdeaDef('household_seals', 'Seals of the Household', 'The ducal household holds the seals of state and names the ministers.',
            {'political_power_gain': 0.20, 'stability_factor': -0.03}, ('command', 'medal')),
    IdeaDef('board_of_houses', 'The Board of the Houses', 'Nominees of the yards, shipping lines and mines sit above the ministries.',
            {'production_factory_efficiency_gain_factor': 0.05, 'consumer_goods_factor': 0.03, 'political_power_gain': 0.05},
            ('economy', 'assembly')),
    IdeaDef('civic_mandate', 'The Civic Mandate', 'An elected civic assembly governs; the ducal title is ceremonial.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('chamber_budget', 'A Voted Budget', 'Every line of the national budget has passed an elected chamber.',
            {'political_power_factor': 0.05, 'stability_factor': 0.03}, ('scales', 'ballot')),
    IdeaDef('houses_audit', 'The Board Audit', 'State services run on the board ledgers, trimmed of everything that did not pay.',
            {'production_factory_efficiency_gain_factor': 0.04, 'stability_factor': -0.02}, ('document', 'economy')),
    IdeaDef('ducal_constitution', 'The Ducal Constitution', 'One written text binds the council, the chamber and the ducal title.',
            {'stability_factor': 0.08, 'political_power_factor': 0.08}, ('document', 'medal')),
    IdeaDef('household_code', 'The Household Code', 'The household prerogatives are written, published and enforced.',
            {'political_power_gain': 0.25, 'war_support_factor': 0.04, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('houses_charter', 'Charter of the Great Houses', 'The board of the houses governs under a published charter with term limits.',
            {'production_factory_efficiency_gain_factor': 0.06, 'production_factory_max_efficiency_factor': 0.04,
             'consumer_goods_factor': 0.03}, ('economy', 'document')),
    IdeaDef('civic_constitution', 'The Civic Constitution', 'The civic assembly, its committee and the courts work under one text.',
            {'stability_factor': 0.07, 'research_speed_factor': 0.04}, ('ballot', 'scales')),
    # port and plain
    IdeaDef('ministries_on_llano', 'Ministries on the Llano', 'The economic ministries sit beside the factories of the metropolis.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': -0.02}, ('industry', 'command')),
    IdeaDef('harbour_ministries', 'Ministries by the Harbour', 'Every ministry stays in Cabaria within sight of the yards.',
            {'political_power_gain': 0.08, 'industrial_capacity_dockyard': 0.03}, ('navy', 'command')),
    IdeaDef('paired_ministries', 'Two-City Government', 'Trade on the coast, industry on the plain, and a cabinet on the train.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('rail', 'assembly')),
    # yards
    IdeaDef('slipway_ledger', 'The Slipway Ledger', 'Every berth, crane and order book on the coast has been inspected.',
            {'industrial_capacity_dockyard': 0.03}, ('navy', 'document')),
    IdeaDef('yard_apprentices', 'Yard Apprentices', 'A public welding school feeds the four coastal yards.',
            {'industrial_capacity_dockyard': 0.03, 'research_speed_factor': 0.01}, ('training', 'tools')),
    IdeaDef('hull_exports', 'Hulls for Export', 'The yards build merchant hulls for foreign owners on state credit.',
            {'industrial_capacity_dockyard': 0.07, 'consumer_goods_factor': -0.02}, ('navy', 'economy')),
    IdeaDef('naval_programme', 'The Naval Programme', 'Navy orders keep every berth working.',
            {'industrial_capacity_dockyard': 0.05, 'navy_org_factor': 0.05}, ('navy', 'command')),
    IdeaDef('refit_trade', 'The Refit Trade', 'Repair and refit at published prices for any passing ship.',
            {'repair_speed_factor': 0.12, 'industrial_capacity_dockyard': 0.04}, ('tools', 'navy')),
    IdeaDef('hull_contracts', 'Long Hull Contracts', 'Series orders from foreign lines, booked years ahead.',
            {'industrial_capacity_dockyard': 0.10, 'consumer_goods_factor': -0.03}, ('navy', 'diplomacy')),
    IdeaDef('standing_squadron', 'The Standing Squadron', 'A permanent escort squadron built and kept in home yards.',
            {'industrial_capacity_dockyard': 0.06, 'navy_org_factor': 0.08, 'naval_coordination': 0.04}, ('navy', 'medal')),
    IdeaDef('refit_network', 'The Refit Network', 'Repair yards on every stretch of the western coast, sharing parts and crews.',
            {'repair_speed_factor': 0.15, 'industrial_capacity_dockyard': 0.06}, ('tools', 'logistics')),
    IdeaDef('yard_credit', 'Yard Credit Line', 'Short-term state credit for idle berths bidding on new work.',
            {'industrial_capacity_dockyard': 0.05, 'production_speed_buildings_factor': 0.03}, ('economy', 'navy')),
    IdeaDef('trusted_yards', 'Yards That Pay Their Suppliers', 'The guarantee fund has met a real default and held.',
            {'industrial_capacity_dockyard': 0.04, 'stability_factor': 0.02}, ('scales', 'navy')),
    # merchant fleet
    IdeaDef('seafarers_college', 'The Seafarers College', 'Officers and engineers examined to a standard foreign insurers accept.',
            {'naval_speed_factor': 0.03, 'navy_org_factor': 0.03}, ('training', 'navy')),
    IdeaDef('open_register', 'An Open Register', 'Foreign owners fly the Arklith flag for low fees.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.02}, ('document', 'economy')),
    IdeaDef('inspected_register', 'An Inspected Register', 'The open register now boards and inspects every foreign-owned hull.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('document', 'security')),
    IdeaDef('national_line', 'The National Line', 'Scheduled sailings by domestic hulls with domestic crews.',
            {'consumer_goods_factor': -0.02, 'naval_coordination': 0.05}, ('navy', 'logistics')),
    IdeaDef('harbour_tariff', 'One Harbour Tariff', 'One published scale of dues for every harbour on the coast.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('scales', 'logistics')),
    # navy
    IdeaDef('kept_in_being', 'A Fleet Kept in Being', 'Escorts kept intact, ready and threatening rather than risked.',
            {'navy_org_factor': 0.04, 'repair_speed_factor': 0.08}, ('navy', 'security')),
    IdeaDef('lane_patrols', 'Patrols on the Lanes', 'Escorts at sea along the busiest merchant routes.',
            {'naval_speed_factor': 0.05, 'navy_org_factor': 0.05}, ('navy', 'logistics')),
    IdeaDef('guarded_approaches', 'Guarded Approaches', 'Mines, booms, radar and submarines outside every major harbour.',
            {'naval_coordination': 0.06, 'army_core_defence_factor': 0.04}, ('submarine', 'security')),
    # highlands
    IdeaDef('nieblo_survey', 'The Nieblo Survey', 'The highland seams and shafts have been mapped and priced.',
            {'production_speed_buildings_factor': 0.04}, ('tools', 'document')),
    IdeaDef('highland_authority', 'The Highland Authority', 'One public authority runs the mines, smelters and arms halls of the Nieblo.',
            {'production_speed_arms_factory_factor': 0.08, 'political_power_gain': 0.05}, ('industry', 'command')),
    IdeaDef('highland_leases', 'Highland Leases', 'Commercial houses work the Nieblo seams for royalties.',
            {'production_speed_industrial_complex_factor': 0.08, 'stability_factor': -0.02}, ('economy', 'tools')),
    IdeaDef('miners_compact', 'The Miners Compact', 'Pay, safety and housing agreed at one table for the mountain towns.',
            {'stability_factor': 0.04, 'industrial_capacity_factory': 0.03}, ('peace', 'tools')),
    # basin
    IdeaDef('halloma_field_study', 'The Halloma Field Study', 'Pressure, reserves and pumps of the basin field are on record.',
            {'production_speed_buildings_factor': 0.03, 'production_speed_industrial_complex_factor': 0.03}, ('economy', 'document')),
    IdeaDef('crude_exports', 'Crude for Export', 'Halloma crude leaves unrefined through the Cabaria terminals.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('economy', 'logistics')),
    IdeaDef('fuel_depots', 'Coastal Fuel Depots', 'Halloma diesel and fuel oil stored at every coastal base.',
            {'repair_speed_factor': 0.08, 'naval_speed_factor': 0.03}, ('logistics', 'navy')),
    # llano
    IdeaDef('llano_works_council', 'The Llano Works Council', 'Owners, unions and the city plan the metropolis together.',
            {'production_factory_efficiency_gain_factor': 0.04}, ('industry', 'assembly')),
    IdeaDef('llano_college', 'The Arklith Technical College', 'Engineers trained at home for the Llano works.',
            {'research_speed_factor': 0.03}, ('science', 'training')),
    IdeaDef('household_goods', 'Household Goods First', 'The Llano works turn toward the domestic shopper.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.03}, ('economy', 'civil')),
    IdeaDef('capital_goods', 'Capital Goods First', 'The Llano works make the machines other industries depend on.',
            {'production_factory_max_efficiency_factor': 0.05, 'consumer_goods_factor': 0.02}, ('tools', 'industry')),
    IdeaDef('sustainment_institute', 'The Sustainment Institute', 'Research devoted to keeping equipment running.',
            {'research_speed_factor': 0.05, 'repair_speed_factor': 0.05}, ('science', 'tools')),
    IdeaDef('standard_parts', 'National Parts Standard', 'One national standard for fasteners, bearings and fittings.',
            {'production_factory_max_efficiency_factor': 0.04, 'supply_consumption_factor': -0.05}, ('tools', 'document')),
    IdeaDef('housing_drive', 'The Housing Drive', 'Apartment blocks rising beside the Llano works.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': -0.03}, ('civil', 'rebuild')),
    # army
    IdeaDef('garrison_workshops', 'Garrison Workshops', 'A repair shop and parts store in every garrison.',
            {'attrition': -0.05, 'supply_consumption_factor': -0.04}, ('tools', 'security')),
    IdeaDef('mountain_corps', 'The Nieblo Mountain Corps', 'The best units trained to hold the highland passes.',
            {'army_defence_factor': 0.05, 'army_core_defence_factor': 0.05}, ('security', 'training')),
    IdeaDef('llano_reserve', 'The Llano Reserve', 'A motorised reserve on the plain for every frontier.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.08}, ('logistics', 'command')),
    IdeaDef('volunteer_service', 'A Volunteer Service', 'Long-service volunteers on decent pay.',
            {'training_time_army_factor': -0.10, 'experience_gain_army_factor': 0.06}, ('medal', 'training')),
    IdeaDef('territorial_militia', 'Territorial Militias', 'Part-time militias guarding their own provinces.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.04}, ('security', 'civil')),
    IdeaDef('sustainment_doctrine', 'The Sustainment Doctrine', 'Fight close to home, keep everything running, never outrun supply.',
            {'supply_consumption_factor': -0.08, 'attrition': -0.08, 'army_org_factor': 0.03}, ('document', 'logistics')),
    # air
    IdeaDef('small_air_arm', 'A Small Air Arm', 'Two dozen fighters and an honest count of what flies.',
            {'experience_gain_air_factor': 0.05}, ('air', 'document')),
    IdeaDef('sea_lane_wing', 'The Sea Lane Wing', 'Patrol aircraft and fighters watching the western lanes.',
            {'air_detection': 0.08, 'naval_coordination': 0.03}, ('air', 'navy')),
    IdeaDef('highland_screen', 'The Highland Screen', 'Fighters and radar guarding the inland frontiers.',
            {'air_superiority_efficiency': 0.06, 'air_defence_factor': 0.05}, ('air', 'radar')),
    IdeaDef('sustained_air_arm', 'A Sustained Air Arm', 'Spares at every field and aircraft that fly when called.',
            {'experience_gain_air_factor': 0.06, 'air_mission_efficiency': 0.05}, ('air', 'tools')),
    # frontiers
    IdeaDef('frontier_desks', 'Four Frontier Desks', 'One office in Cabaria follows all four frontiers.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('diplomacy', 'document')),
    IdeaDef('open_frontiers', 'Open Crossings', 'Low tariffs, quick inspections and transit for neighbours.',
            {'consumer_goods_factor': -0.03, 'stability_factor': -0.01}, ('diplomacy', 'logistics')),
    IdeaDef('watchful_neutrality', 'Watchful Neutrality', 'Courteous to all neighbours, committed to none, posts manned all year.',
            {'army_core_defence_factor': 0.06, 'stability_factor': 0.03}, ('security', 'peace')),
    IdeaDef('valley_markets', 'Valley Markets', 'Seasonal markets at the Dakrain crossings under commission oversight.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.01}, ('peace', 'economy')),
    # the Belkan War years
    IdeaDef('crisis_office', 'The Crisis Office', 'A room in Cabaria that follows the war hour by hour.',
            {'political_power_gain': 0.05, 'war_support_factor': 0.03}, ('communications', 'command')),
    IdeaDef('war_risk_pool', 'The War-Risk Pool', 'State cover for Arklith hulls that insurers will not take.',
            {'stability_factor': 0.02, 'industrial_capacity_dockyard': 0.02}, ('scales', 'navy')),
    IdeaDef('neutral_carriers', 'Neutral Carriers', 'Arklith ships carry any lawful cargo for any buyer.',
            {'consumer_goods_factor': -0.04, 'war_support_factor': -0.03}, ('logistics', 'peace')),
    IdeaDef('closed_harbours', 'Closed Harbours', 'No belligerent warship or war cargo enters an Arklith port.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('security', 'navy')),
    IdeaDef('escorted_sailings', 'Escorted Sailings', 'Small convoys under navy escort near dangerous waters.',
            {'naval_coordination': 0.05, 'war_support_factor': 0.02}, ('navy', 'security')),
    IdeaDef('postwar_freight', 'Postwar Freight', 'Reconstruction cargoes keep the lines and yards busy.',
            {'industrial_capacity_dockyard': 0.05, 'consumer_goods_factor': -0.03}, ('rebuild', 'logistics')),
    IdeaDef('frontier_unease', 'Unease on the Frontiers', 'Reserves refreshed and watches doubled while the continent settles.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.04}, ('security', 'diplomacy')),
    # Ulysses
    IdeaDef('sky_watch', 'The Sky Watch', 'Astronomers, physicists and radar crews reporting to one room.',
            {'air_detection': 0.08}, ('telescope', 'radar')),
    IdeaDef('city_shelters', 'Shelters Under the Cities', 'Deep shelters stocked for weeks beneath the main cities.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('dispersal_plans', 'The Dispersal Plans', 'Routes, reception towns and transport to empty the cities.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.10}, ('refugees', 'rail')),
    IdeaDef('relief_bureau', 'The Relief Bureau', 'One office for arrivals, claims and returned shelter stocks.',
            {'stability_factor': 0.04}, ('refugees', 'medical')),
    IdeaDef('relief_voyages', 'Relief Voyages', 'Reserve hulls carrying food and medicine abroad.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('medical', 'navy')),
    # the millennium
    IdeaDef('usean_charters', 'Charters for Peaceful Cargo', 'Lawful bulk cargoes carried for an economy disrupted by war.',
            {'consumer_goods_factor': -0.04, 'industrial_capacity_dockyard': 0.04}, ('logistics', 'economy')),
    IdeaDef('home_waters', 'Home Waters', 'The merchant fleet kept close to home until the Usean war ends.',
            {'stability_factor': 0.03, 'naval_coordination': 0.04}, ('navy', 'peace')),
    IdeaDef('open_contracts', 'Published Contracts', 'Every large state contract published with price and supplier.',
            {'political_power_factor': 0.04, 'stability_factor': 0.03}, ('scales', 'document')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('ducal_council', 'Ducal Council of Ministers',
           'A council of ministers named under the ducal title and confirmed by a chamber elected from the national rolls; '
           'the duke signs on its advice. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('ducal_household', 'Household Cabinet of the Duchy',
           'A cabinet appointed by the ducal household that holds the seals, the budget and the officer lists, with any '
           'chamber kept as an advisory body. Provisional gameplay office with no named holder.',
           'monarchism', 'absolutism'),
    Office('houses_board', 'Board of the Great Houses',
           'A board of nominees from the shipbuilders, shipping lines and mining concerns that sets the budget and directs the '
           'National Administration as its secretariat. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('civic_assembly', 'Executive Committee of the Civic Assembly',
           'An executive committee chosen by a civic assembly elected from the national rolls, with the ducal title kept as a '
           'ceremonial honour. Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('who_governs', 'Who Governs the Duchy', (
        "The National Administration has governed Arklith since the vote of 1990, and it has done so competently enough that "
        "few people ask by what right. The ministries in Cabaria run, the yards launch their hulls and the Llano factories keep "
        "their shifts. Yet the Duchy has no election on its calendar, and the administration's own lawyers concede that its "
        "mandate rests more on habit than on any written grant.",
        "Publishing the administration's powers has brought every faction into the open. Loyalists of the ducal house, still "
        "about a third of the country by the old measures, want the title to mean something again, either beside a council of "
        "ministers or above it. The owners of the yards, shipping lines and Nieblo mines want a board that runs the state the "
        "way they run their companies. A smaller but organised camp in the Llano and the port unions wants an elected assembly "
        "and nothing else.",
        "Nothing has been decided yet. What the administration chooses today is how the argument will be held: openly, with "
        "the press and the provinces watching, or quietly in the corridors of Cabaria, where the great houses and the ducal "
        "household already have friends. Either choice will be remembered by the camp it disappoints.",
    ), (
        Option('Hold the argument in public.', (Stability(0.02), PP(-15))),
        Option('Keep it inside the ministries.', (PP(35), Stability(-0.02))),
    ), picture=2),
    EventDef('port_and_plain', 'Port and Plain', (
        "Ask in Cabaria where the country's future lies and the answer points to the harbours: Puerto Tranquilidad and "
        "Cabarion, the yards along the coast, the merchant fleet that carries Arklith's name to foreign ports. Ask in the city "
        "of Arklith on the Llano and the answer is the factories, the seven great works and the workshops around them, and a "
        "population larger than any coastal province can claim.",
        "The state has never resolved which of the two it serves first. Officials commute by the coast railway, files go "
        "missing between offices, and both regions are convinced the other receives the larger share of the budget. Planners "
        "have drawn up three answers: move the economic ministries inland, keep everything by the harbour, or split the "
        "government between them and accept the cost of running it from two cities.",
        "Before any of those plans is chosen, the government must decide how to frame the question. It can treat it as a "
        "technical matter of efficiency, to be settled by surveys of traffic and cost, or as a political bargain between two "
        "regions that both believe they carry the country. The surveys will be quicker. The bargain will last longer.",
    ), (
        Option('Let the surveys decide.', (Research('construction_tech', 0.5, 1),)),
        Option('Bargain with both regions.', (Stability(0.03), PP(-20))),
    ), picture=0),
    EventDef('order_book', 'The Order Book', (
        "The inspectors' report on the twenty slipways reads like a ship's log of the last decade. Some berths at Arklith del "
        "Norte and Arklith del Sur have worked without a pause; others on the Cabar coast have built nothing larger than a tug "
        "in three years. Cranes, welding gear and dry docks vary from modern to museum pieces, often in the same yard. "
        "Payrolls are full everywhere, because no yard owner wants to be the first to dismiss skilled hands.",
        "The order book itself is thin. Foreign shipping companies have plenty of yards to choose from, and Arklith wins "
        "contracts mainly on price, with the state's credit making up the difference. The navy has ordered little beyond "
        "maintenance. Repair work comes and goes with the passing traffic. Every owner has a plan to fix this, and every plan "
        "requires the treasury.",
        "The government must decide how much of the report to release. Published in full, it will show foreign buyers exactly "
        "where the yards are weak, and give the unions a clear view of which berths are at risk. Kept within the ministry and "
        "the owners' association, it will guide a quieter reform, at the cost of rumours along the coast that something is "
        "being hidden.",
    ), (
        Option('Publish it for the yards and the unions.', (Stability(-0.02), Research('naval_equipment', 0.5, 1))),
        Option('Share it with the owners only.', (PP(30), XP('navy', 10))),
    ), picture=0),
    EventDef('under_whose_flag', 'Under Whose Flag', (
        "The shipping office has finished its count of the merchant fleet, and the results surprise even its own clerks. "
        "Several hundred ships carry the Arklith flag, far more than a country of eight provinces could load with its own "
        "trade. Some are owned and crewed at home and call at Puerto Tranquilidad every month. Many more belong to foreign "
        "companies that registered here for low fees and have never seen the coast.",
        "The foreign-owned hulls pay their dues on time and ask for little. They also bring risk: old ships, crews of uncertain "
        "training and owners whose other business is not always visible. A single disaster at sea involving an Arklith-flagged "
        "ship would land on the Duchy's reputation regardless of who owned it. Meanwhile, the domestic lines complain that the "
        "open register undercuts them on every route they sail.",
        "Two opinions dominate the shipping office. One says the register is a business like any other and should be run for "
        "revenue, with inspections tight enough to avoid scandal. The other says a flag should mean something, and that a "
        "smaller, national fleet would serve the country better in a crisis. Before choosing, the office must decide whom to "
        "consult.",
    ), (
        Option('Consult the foreign owners as well.', (PP(25), Stability(-0.01))),
        Option('Consult only the domestic lines and crews.', (Stability(0.02), XP('navy', 10))),
    ), picture=2),
    EventDef('highland_ledger', 'The Highland Ledger', (
        "The survey teams come down from the Nieblo with crates of core samples and notebooks full of warnings. The aluminium "
        "and tungsten seams of both highland provinces are richer than the old maps suggested, especially in the eastern "
        "valleys. The shafts that reach them are in worse condition than anyone admitted: ventilation that fails in the warm "
        "months, props past their age and escape routes that end in rock.",
        "The highland towns depend on the mines and the arms plants beside them, which together employ most working adults in "
        "some valleys. Wages are low, prices are high and the roads to the Llano close for days at a time in the rains. The "
        "mining families have learned not to expect much from Cabaria. Their delegates have nonetheless travelled down with "
        "the survey, to make sure the report is read.",
        "Two proposals are already circulating. The state could bring every mine and plant under one public authority, or "
        "lease the seams to the commercial houses for investment and royalties. Before either can be argued, the government "
        "must decide what it says to the delegates who are waiting in the corridor, and whether it promises them anything now.",
    ), (
        Option('Promise safety first, output second.', (Stability(0.03), PP(-15))),
        Option('Promise investment and jobs.', (PP(20), Research('excavation_tech', 0.5, 1))),
    ), picture=1),
    EventDef('llano_works', 'The Works Council Meets', (
        "For the first time, the owners of the seven great works on the Llano, the unions that organise their shifts and the "
        "city council of Arklith sit in one room with a single agenda. The meeting is stiff. Owners speak of energy prices and "
        "foreign competition; union delegates speak of housing, overtime and the workers who arrive each week from the "
        "highlands and the coast. The city's officials mostly take notes.",
        "Beneath the formalities, everyone knows what the plain needs. Its machine tools are old, its engineers are few and "
        "its power supply falters whenever several works run full shifts at once. The works make almost everything the "
        "country uses, from buses to rifles to pump housings, and almost none of it is made as well as it could be. Foreign "
        "buyers have noticed.",
        "The council's first decision is about its own character. It can become a planning body with access to the ministries "
        "and a budget of its own, or remain a forum where problems are aired and settled by the parties themselves. A planning "
        "body would move faster and carry the state's weight. A forum would keep the government at arm's length from wages "
        "and prices.",
    ), (
        Option('Make it a planning body.', (PP(-20), Research('industry', 0.5, 1))),
        Option('Keep it a forum.', (Stability(0.02), PP(20))),
    ), picture=1),
    EventDef('army_counts', 'The Army Counts Its Rifles', (
        "The general staff's audit runs to several volumes, and the summary is blunt. Arklith has an army sized for a small "
        "country with no enemies, which is what it believes itself to be. Garrisons in every province maintain their barracks "
        "and parade grounds. The mountain detachment in the Nieblo trains hard. Elsewhere, trucks wait for parts, artillery "
        "waits for crews and many soldiers have not fired a live round in a year.",
        "Public interest is close to nil. War support sits near the bottom of every measure the ministries track, and most "
        "voters, asked about defence, mention the navy's escorts protecting the merchant fleet before they mention the army at "
        "all. The officers know that any request for money will be compared with the yards, the highlands and the metropolis, "
        "and lose.",
        "The staff therefore proposes to begin with what costs least: repair, reorganisation and honest planning. The question "
        "is how loudly to say so. A public report would invite debate and perhaps support. A confidential one would avoid "
        "alarming anyone and keep the army's weaknesses away from foreign eyes, at the price of another decade of indifference.",
    ), (
        Option('Publish an honest summary.', (WarSupport(0.03), Stability(-0.01))),
        Option('Keep the audit confidential.', (XP('army', 20), PP(10))),
    ), picture=2),
    EventDef('four_frontiers', 'Four Frontiers', (
        "The frontier review lays the country's borders out on a single table in the foreign office in Cabaria. To the east, "
        "Perbla, beyond the Halloma Basin and the Cabar hills, a larger kingdom with old friends of its own. To the south, "
        "Leasath along the edge of the Llano and the Nieblo passes. Past Eastern Nieblo, Dakrain. On the southern edge of "
        "Arklith del Sur, the Gibraltar Mining Zone and its mining administration.",
        "None of these frontiers is in dispute, and the review does not propose to change any of them. What it finds is that "
        "each is managed by a different ministry, under different rules, with different priorities. Customs officials at the "
        "Halloma crossings work to one code; border police in the Nieblo passes to another. Nobody in Cabaria has ever asked "
        "whether the four policies make sense together.",
        "The review's authors offer two broad directions: open the crossings to trade and transit, or keep them courteous but "
        "watchful and promise nothing to anyone. Before that choice, the government must decide how much to say to the "
        "neighbours about the review itself. Openness would reassure them. Discretion would keep options available.",
    ), (
        Option('Inform every neighbour.', (Stability(0.02), PP(-10))),
        Option('Keep the review internal.', (PP(25), XP('army', 10))),
    ), picture=2),
    EventDef('belkan_war_news', 'War Beyond Perbla', (
        "In March 1995 the Belkan War breaks out. Arklith has no part in it and no treaty that could draw it in. Yet the news "
        "lands hard in Cabaria. Perbla, on the eastern frontier, has old ties to Belka, and nobody knows how far its sympathies "
        "will go. Arklith-flagged ships sail in waters that are suddenly dangerous, and the crisis office opens with more "
        "questions than staff.",
        "Within days the practical effects arrive. Foreign insurers raise premiums on any hull bound anywhere near the "
        "fighting. Shippers who usually book space months ahead call daily for news. Rumours spread in the Halloma Basin that "
        "the Perbla frontier will close, though nothing on the ground suggests it. In the Llano, factories that buy foreign "
        "parts begin hoarding.",
        "The administration must decide what it will tell the country. It can speak frankly about the risks to shipping and "
        "trade, which may cause a run on stores and a rush to reflag ships. Or it can reassure first and explain later, "
        "accepting that if things go badly the public will remember being told all was well. The crisis office has drafted "
        "both statements and waits for a signature.",
    ), (
        Option('Speak frankly about the risks.', (WarSupport(0.03), Stability(-0.02), Event('insurers_rates', 14))),
        Option('Reassure first.', (Stability(0.02), Event('insurers_rates', 21))),
    ), citation='date anchor only, Chronicle row 1995 / 03.25; the Arklith response is gameplay', picture=0),
    EventDef('insurers_rates', 'The Insurers Raise the Rates', (
        "Two weeks into the war, the foreign insurance syndicates that cover most of Arklith's merchant fleet publish new "
        "rates. War-risk premiums on routes near the fighting rise several times over; some routes are excluded altogether. "
        "Owners of older ships find themselves uninsurable at any price. Several masters radio from foreign ports that they "
        "will not sail until someone tells them who pays if they are sunk.",
        "The shipping lines come to Cabaria in a body. They want the state to guarantee their hulls, or at least to share the "
        "risk, and they point out that a fleet idling in harbour pays no dues and buys no fuel. The treasury answers that a "
        "guarantee is a blank cheque written on a war it cannot control. Both are right, which makes the meeting long.",
        "There are middle courses. The state could cover only domestic-owned ships, or only routes it judges safe, or only "
        "hulls that sail under navy escort. Each would leave someone unprotected and angry. The crisis office recommends a "
        "decision within the week, before the masters abroad make it for the government by selling their ships.",
    ), (
        Option('Guarantee the domestic lines.', (PP(-25), Stability(0.03))),
        Option('Leave the risk with the owners.', (PP(20), Stability(-0.02))),
        Option('Cover only escorted sailings.', (XP('navy', 15), WarSupport(0.02))),
    ), citation='date anchor only, Chronicle row 1995 / 03.25; the insurance crisis is gameplay', picture=0),
    EventDef('ulysses_announced', 'A Date in the Sky', (
        "In December 1994 astronomers warned that the asteroid called Ulysses could strike the Earth. In April 1996 the "
        "warning becomes an announcement: it will. Governments are told to prepare. Nobody can yet say where the fragments "
        "will fall, or how many there will be, or whether a coast, a plain or a mountain range is the safer place to be.",
        "In Arklith the news arrives on the evening broadcasts and reaches the morning markets as panic. Bottled water and "
        "tinned food sell out in Cabaria and the city of Arklith. Churches and union halls fill. The sky watch, a handful of "
        "amateur astronomers and radar crews, is suddenly asked questions it cannot answer. Foreign bulletins contradict each "
        "other daily, and every radio phone-in has a caller who claims to know where the fragments will land. The ports report "
        "families booking passage abroad without any idea where abroad would be safer.",
        "The government has two tasks. The first is to plan, and engineers are already drafting proposals for shelters "
        "beneath the cities or for evacuation to the highlands and the basin. The second is to keep the country calm while it "
        "plans. How much uncertainty the government admits in public will shape whether people trust the plans when they come.",
    ), (
        Option('Admit what nobody knows.', (Stability(-0.02), WarSupport(0.02))),
        Option('Promise a plan within the month.', (Stability(0.02), PP(-20))),
    ), citation='date anchors only, Chronicle rows 1994 / 12.10 and 1996 / 04.20; the Arklith response is gameplay', picture=1),
    EventDef('ulysses_overhead', 'Ulysses Overhead', (
        "In July 1999 Ulysses passes through the Earth's Roche limit and begins to break apart. In Arklith, sirens are tested "
        "at noon, ships in the reserve raise steam and the sky watch moves its reports from weekly to hourly. Families who "
        "rehearsed their routes check them again. The broadcasts carry foreign bulletins, then local ones, then foreign ones "
        "again.",
        "The plans written since 1996 are about to be judged. Shelters stand stocked, or reception towns stand ready, "
        "depending on what the government chose. Neither plan can do anything about where the fragments fall. Both depend on "
        "people trusting the instructions they receive in the next hours, and on officials resisting the temptation to "
        "improvise. In the Llano works, managers ask whether to bank the furnaces. In the highlands, miners ask whether to "
        "stay underground. Every question reaches Cabaria at once, and the crisis office answers them in order.",
        "The government's last decision before the night is simple and difficult. It can order the plans into effect now, on "
        "the strength of uncertain warnings, accepting the disruption if nothing comes. Or it can wait for clear warnings and "
        "act on them, accepting the risk that clear warnings may come too late to matter. Neither choice will look wise to "
        "everyone in the morning.",
    ), (
        Option('Put the plans into effect tonight.', (Stability(-0.02), WarSupport(0.03))),
        Option('Wait for clear warning.', (Stability(0.02), PP(15))),
    ), citation='date anchor only, Chronicle row 1999 / 07.08; no fragment fall in Arklith is claimed', picture=1),
    EventDef('decade_review', 'Ten Years On', (
        "The review panel, drawn by lot from all eight provinces, delivers its report at the turn of the century. It is long, "
        "careful and in places harsh. It credits the decade with order and growth: the yards are busier, the Llano works more "
        "modern, the highland towns safer. It faults the state for deciding too much in Cabaria and explaining too little "
        "everywhere else.",
        "Each camp reads the report for its own purposes. Supporters of the government chosen in the early nineties find "
        "praise; its opponents find enough criticism to quote for years. The yards and the shipping lines read the chapter on "
        "credit and guarantees with particular care. The Llano reads the chapter on industry and asks why its name appears so "
        "rarely in the recommendations.",
        "The government must decide what to do with the report. It can adopt its recommendations wholesale, binding itself to "
        "a programme it did not write. It can thank the panel and choose selectively. Or it can submit the report to the "
        "provinces for comment, which will take months and produce a second, louder argument. The panel members, at least, "
        "have already gone home.",
    ), (
        Option('Adopt the recommendations.', (Stability(0.03), PP(-25))),
        Option('Choose selectively.', (PP(30),)),
        Option('Send it to the provinces.', (Stability(0.02), PP(-10), WarSupport(-0.01))),
    ), picture=2),
    EventDef('yard_default', 'A Buyer Walks Away', (
        "A foreign shipping company with two hulls half built on Arklith berths announces that it cannot pay. Its creditors "
        "abroad have seized its accounts, its directors have stopped answering letters and the hulls sit on the slipways with "
        "their plating unfinished. Suppliers who delivered steel, engines and wiring want their money. The yard wants to know "
        "who will pay its welders next month.",
        "This is the case the yards have always feared and rarely planned for. A default on one contract can ripple through "
        "dozens of small suppliers in the coastal provinces, some of whom have no other customer. The question in the ministry "
        "is not whether the state will help, but how, and how much it will expect back when the hulls are finally sold.",
        "Options are limited. The state can buy the hulls, finish them and sell them itself, taking the risk and any profit. "
        "It can lend the yard enough to finish them and leave the sale to the owners. Or it can let the yard and its suppliers "
        "settle among themselves, as any other business would, and accept the closures that follow.",
    ), (
        Option('Buy and finish the hulls.', (PP(-30), Stability(0.03))),
        Option('Lend to the yard.', (PP(-10), Stability(0.01))),
        Option('Let the market settle it.', (PP(20), Stability(-0.03))),
    ), picture=0),
    EventDef('usean_freight', 'Freight for a Distant War', (
        "In August 2003 the FCU founds the ISAF to fight Erusea on the Usean continent, and the war that follows touches every "
        "shipping market in the world. Arklith has no part in it. Its lines feel it within weeks: charter rates for bulk "
        "carriers rise, insurers redraw their maps and buyers who had hesitated over new hulls sign contracts to secure "
        "capacity before prices rise further.",
        "The shipping office reports offers from many directions. Some are innocent: grain, machinery, building materials for "
        "economies disrupted by the fighting. Others are less clear, with cargo descriptions that could cover almost anything. "
        "The yards report a rush of repair work from ships diverted onto longer routes. In Cabaria, the old debates of 1995 "
        "return as if they had never ended.",
        "The government must set the terms. It can let the lines take every lawful cargo, with inspections to keep them "
        "honest, or ask them to keep their ships closer to home until the war is over. Either way, it must decide quickly, "
        "because the lines are already signing contracts and the masters are already at sea.",
    ), (
        Option('Take every lawful cargo.', (PP(25), Stability(-0.01))),
        Option('Keep the ships close to home.', (Stability(0.02), XP('navy', 10))),
    ), citation='date anchor only, Chronicle row 2003 / 08.22; the Arklith response is gameplay', picture=0),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('admin', 'The National Administration', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_take_stock', 'The Administration Takes Stock',
          "Arklith enters 1991 governed by the National Administration, a standing executive that has run the Duchy since the "
          "last vote in 1990 and holds no election on its calendar. Stability is high and enthusiasm is low. Before any reform, "
          "the administration publishes what it does and on whose authority, which invites every faction to answer back.",
          ('command', 'document'), reward=(Idea('administration_review'), Event('who_governs'))),
    Focus('adm_electoral_rolls', 'Dust Off the Electoral Rolls',
          "The rolls used in 1990 sit in provincial offices from Marcil to the Halloma Basin, already out of date. Clerks "
          "recount voters house by house and post the lists in every town hall. The work costs a season of paperwork and "
          "commits nobody to an election, but it removes the excuse that a vote could not be organised at short notice.",
          ('ballot', 'document'), after=('adm_take_stock',), reward=(Flag('rolls_compiled'), Stability(0.02))),
    Focus('adm_ducal_title', 'What the Ducal Title Means',
          "Arklith is styled a duchy, and roughly a third of the country still looks to the ducal house as the source of "
          "legitimate government. Nobody has written down which powers the title carries today. Jurists in Cabaria draft the "
          "inventory: appointments, pardons, the seal on treaties, the right to call a vote. Every faction reads it as an "
          "opening bid.",
          ('medal', 'scales'), after=('adm_take_stock',),
          reward=(PP(30), Tooltip('Opens four paths for the government of the Duchy; only one can be taken.'))),
    Focus('adm_council_path', 'A Council Beside the Duke',
          "Moderate loyalists propose that the ducal house keep its title and its seal while a council of ministers governs, "
          "answerable to a chamber elected from the new rolls. It is the compromise most provinces can live with. The National "
          "Administration loses its freedom to act alone, and the ducal house trades its long silence for a formal role.",
          ('assembly', 'medal'), after=('adm_electoral_rolls', 'adm_ducal_title'),
          exclusive=('adm_household_path', 'adm_board_path', 'adm_assembly_path'),
          reward=(SwapIdea('administration_review', 'ducal_charter'),)),
    Focus('adm_household_path', 'The Household Takes the Seal',
          "The ducal household argues that a duchy should be governed by its duke, and that the 1990 vote showed how little "
          "the parties had to offer. It asks for the seals of state, the officer lists and the budget, with ministers chosen by "
          "and answerable to the household. Decisions would come quickly; dissent would have no formal home.",
          ('command', 'medal'), after=('adm_electoral_rolls', 'adm_ducal_title'),
          exclusive=('adm_council_path', 'adm_board_path', 'adm_assembly_path'),
          reward=(SwapIdea('administration_review', 'household_seals'),)),
    Focus('adm_board_path', 'The Houses Want the Board',
          "The owners of the yards, the shipping lines and the Nieblo mines already fund much of the state through taxes and "
          "loans. They propose a governing board drawn from the great commercial houses, keeping the administration but placing "
          "their own nominees above its senior civil servants. Efficiency is promised loudly. Fairness is not mentioned at all.",
          ('economy', 'assembly'), after=('adm_electoral_rolls', 'adm_ducal_title'),
          exclusive=('adm_council_path', 'adm_household_path', 'adm_assembly_path'),
          reward=(SwapIdea('administration_review', 'board_of_houses'),)),
    Focus('adm_assembly_path', 'Let the Rolls Decide',
          "Reformers in the Llano metropolis and the port unions want an elected civic assembly to govern in its own name, "
          "leaving the ducal title as an honour without office. They are a minority, about one voter in seven by the old count, "
          "but they are organised, and the refreshed rolls give them a platform the administration cannot quietly withdraw.",
          ('ballot', 'assembly'), after=('adm_electoral_rolls', 'adm_ducal_title'),
          exclusive=('adm_council_path', 'adm_household_path', 'adm_board_path'),
          reward=(SwapIdea('administration_review', 'civic_mandate'),)),
    Focus('adm_council_regime', 'Seat the Ducal Council',
          "The ducal council takes the seals from the National Administration. Ministers are named by the council, confirmed "
          "by the elected chamber and sworn before the duke, who signs on their advice. The change runs through an office, not "
          "a personality. The administration's senior staff stay on as civil servants, uneasy but still employed.",
          ('assembly', 'document'), after=('adm_council_path',), cost=10,
          exclusive=('adm_household_regime', 'adm_board_regime', 'adm_assembly_regime'),
          reward=(Regime('ducal_council'), Flag('path_council'))),
    Focus('adm_household_regime', 'Household Government',
          "A cabinet appointed by the ducal household takes over the ministries. Elections stay off the calendar and the "
          "chamber, if it meets at all, merely advises. Provincial governors are replaced by household commissioners. The "
          "arrangement is clear about who decides, which reassures investors in the yards and worries everyone who expected the "
          "new rolls to be used.",
          ('command', 'security'), after=('adm_household_path',), cost=10,
          exclusive=('adm_council_regime', 'adm_board_regime', 'adm_assembly_regime'),
          reward=(Regime('ducal_household'), Flag('path_household'))),
    Focus('adm_board_regime', 'The Board of the Great Houses',
          "A board of nominees from the shipbuilders, shipping lines and mining concerns sits above the ministries and sets the "
          "budget. The National Administration becomes its secretariat. Decisions are businesslike and fast. Wages, port fees "
          "and mine safety become matters for the board's discretion, and the unions on the coast notice before anyone else.",
          ('economy', 'command'), after=('adm_board_path',), cost=10,
          exclusive=('adm_council_regime', 'adm_household_regime', 'adm_assembly_regime'),
          reward=(Regime('houses_board'), Flag('path_board'))),
    Focus('adm_assembly_regime', 'Convene the Civic Assembly',
          "Voters on the refreshed rolls elect a civic assembly, which chooses an executive committee to govern. The ducal "
          "title remains, with ceremonial duties only. Turnout is uneven: high on the Llano and in the ports, thin in the Nieblo "
          "highlands. The committee inherits a stable country with almost no habit of open argument, and must learn one fast.",
          ('ballot', 'scales'), after=('adm_assembly_path',), cost=10,
          exclusive=('adm_council_regime', 'adm_household_regime', 'adm_board_regime'),
          reward=(Regime('civic_assembly'), Flag('path_assembly'))),
    Focus('adm_council_budget', 'A Budget Voted in the Chamber',
          "For the first time in years an elected chamber votes the spending plan item by item, with yard subsidies, highland "
          "roads and harbour fees argued in public. The session runs long and the press reports every quarrel. Ministers lose "
          "the comfort of quiet agreement, and the provinces finally see what Cabaria spends on them.",
          ('scales', 'ballot'), after=('adm_council_regime',),
          exclusive=('adm_household_commissioners', 'adm_board_ledgers', 'adm_assembly_charter'),
          reward=(TimedIdea('chamber_budget', 730),)),
    Focus('adm_household_commissioners', 'Commissioners in the Provinces',
          "Household commissioners arrive in each province with orders to finish what local councils left undone. In Eastern "
          "Nieblo the first of them starts on the road the mining towns have petitioned for since the eighties. Commissioners "
          "answer to Cabaria alone, so local notables lose their voice, though the roads at last get built on schedule.",
          ('command', 'rail'), after=('adm_household_regime',),
          exclusive=('adm_council_budget', 'adm_board_ledgers', 'adm_assembly_charter'),
          reward=(Build('infrastructure', 1, 252), PP(15))),
    Focus('adm_board_ledgers', 'The Board Reads the Ledgers',
          "The board's first act is to read the state's books as if they were a company's. Loss-making ferry routes, idle "
          "depots and overstaffed offices are listed for sale or closure. The savings are real and quickly reinvested in the "
          "yards. The cuts fall on small towns and junior clerks, who were never consulted and will not forget it.",
          ('document', 'economy'), after=('adm_board_regime',),
          exclusive=('adm_council_budget', 'adm_household_commissioners', 'adm_assembly_charter'),
          reward=(TimedIdea('houses_audit', 730),)),
    Focus('adm_assembly_charter', 'A Written Civic Charter',
          "The assembly drafts a charter fixing its own powers, the executive committee's term and the ceremonial duties of "
          "the ducal title. Ratification means bargaining with every province, and the highland delegates extract guarantees "
          "on mining royalties before they sign. The text is long and imperfect, and it finally gives the courts something to "
          "interpret.",
          ('document', 'assembly'), after=('adm_assembly_regime',),
          exclusive=('adm_council_budget', 'adm_household_commissioners', 'adm_board_ledgers'),
          reward=(Stability(0.05), PP(-30))),
))

PORT = Branch('port', 'Port and Plain', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('prt_two_centres', 'Two Centres of Gravity',
          "Government sits in Cabaria, beside the harbours of Puerto Tranquilidad and Cabarion, while the largest city and most "
          "of the factories lie inland on the Llano de Arklith. Ministries travel, files travel, and so do grievances. Ending "
          "the confusion means choosing which centre the state should serve first, and both will count the cost carefully.",
          ('rail', 'command'), reward=(Event('port_and_plain'), Stability(0.01))),
    Focus('prt_rail_survey', 'Survey the Coast Railway',
          "Freight from the Llano reaches the Cabaria docks on a line laid long ago for smaller trains. The survey counts every "
          "bridge, siding and level crossing between the plain and the sea. The first works double the worst stretch near the "
          "capital. It costs money the yards wanted, but every hull and every crate rides this line sooner or later.",
          ('rail', 'document'), after=('prt_two_centres',), reward=(Build('infrastructure', 1, 398),)),
    Focus('prt_llano_road', 'The Llano Trunk Road',
          "Trucks leaving the factories of the metropolis share one crowded highway with farm carts and buses. A widened trunk "
          "road across the Llano de Arklith, with bypasses around the worst market towns, cuts hours from every delivery. The "
          "heavy rains test the new surface in its first year, and engineers learn where they should have dug deeper drains.",
          ('logistics', 'bridge'), after=('prt_two_centres',), reward=(Build('infrastructure', 1, 241),)),
    Focus('prt_ministries_inland', 'Move the Ministries Inland',
          "Planners propose moving the economic ministries to the Llano metropolis, where the factories, unions and most "
          "voters already are. Cabaria would keep the formal seat of government but lose the daily traffic of contracts. The "
          "port elite objects loudly. Industry gains ministers who can see a production line from their office windows.",
          ('industry', 'command'), after_any=('prt_rail_survey', 'prt_llano_road'), cost=10,
          exclusive=('prt_ministries_coast', 'prt_ministries_split'), reward=(Idea('ministries_on_llano'),)),
    Focus('prt_ministries_coast', 'Keep Every Ministry in Cabaria',
          "The opposite answer keeps every ministry by the harbour and brings the Llano to Cabaria instead, with a fast daily "
          "train for officials and a liaison office in the metropolis. Coordination stays tight and the yards keep their "
          "privileged access. The plain sees its own concerns handled by visitors, and its mayors begin keeping score.",
          ('navy', 'command'), after_any=('prt_rail_survey', 'prt_llano_road'), cost=10,
          exclusive=('prt_ministries_inland', 'prt_ministries_split'), reward=(Idea('harbour_ministries'),)),
    Focus('prt_ministries_split', 'Split the Ministries',
          "A third plan divides the state: trade, shipping and foreign affairs stay on the coast, while industry, labour and "
          "education move to the Llano. Each region gets a share of the jobs and the prestige. The price is a government "
          "permanently on the train, duplicated offices and a cabinet that meets in two cities by turns.",
          ('rail', 'assembly'), after_any=('prt_rail_survey', 'prt_llano_road'), cost=10,
          exclusive=('prt_ministries_inland', 'prt_ministries_coast'), reward=(Idea('paired_ministries'),)),
    Focus('prt_llano_quarter', 'A Government Quarter Inland',
          "The ministries that moved inland take over an old warehouse district on the edge of the city of Arklith. Officials "
          "now meet factory managers over lunch rather than by appointment. Contracts move faster and so do complaints. Some "
          "senior staff refuse to leave the coast and retire early, taking decades of memory with them.",
          ('industry', 'civil'), after=('prt_ministries_inland',),
          exclusive=('prt_harbour_offices', 'prt_ministers_train'),
          reward=(Research('industry', 0.5, 1), PP(15))),
    Focus('prt_harbour_offices', 'Harbour Offices Expand',
          "With every ministry staying in Cabaria, the harbour quarter grows to house them, and the yard owners win a new "
          "berth at Puerto Tranquilidad as part of the bargain. The capital becomes busier and more expensive. Visitors from "
          "the Llano find their way to the right office more easily, though not always to a sympathetic one.",
          ('navy', 'civil'), after=('prt_ministries_coast',),
          exclusive=('prt_llano_quarter', 'prt_ministers_train'), reward=(Build('dockyard', 1, 398),)),
    Focus('prt_ministers_train', 'The Ministers Train',
          "A government split between two cities needs a reliable link. A dedicated morning and evening service runs between "
          "Cabaria and the metropolis, and the line through Arklith del Norte is upgraded so the journey takes under two "
          "hours. Cabinet papers are read on board. Commuters on the same line notice their own trains running later.",
          ('rail', 'logistics'), after=('prt_ministries_split',),
          exclusive=('prt_llano_quarter', 'prt_harbour_offices'), reward=(Build('infrastructure', 1, 605),)),
    Focus('prt_provincial_councils', 'Provincial Councils Meet',
          "Whatever the address of the ministries, the eight provinces from the Cabar Mountains to Arklith del Sur receive "
          "councils with small budgets for roads, clinics and schools, chosen in the way the national order allows. They are "
          "modest bodies with modest powers. Complaints now have a local address, and trouble is heard before it spreads.",
          ('assembly', 'civil'), after_any=('prt_llano_quarter', 'prt_harbour_offices', 'prt_ministers_train'),
          reward=(Flag('councils_seated'), Stability(0.02))),
))

YARDS = Branch('yards', 'Twenty Slipways', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('yrd_count_slipways', 'Count the Twenty Slipways',
          "Twenty building berths line the four coastal provinces, five each at Cabaria, the Cabar coast, Arklith del Norte "
          "and Arklith del Sur. Together they are the largest employer outside the Llano factories. An inspection of every "
          "berth, crane and order book shows which yards are full, which are idle and which survive only on state credit.",
          ('navy', 'document'), reward=(Idea('slipway_ledger'), Event('order_book'))),
    Focus('yrd_crane_renewal', 'Renew the Gantry Cranes',
          "Several gantry cranes on the del Norte berths date from before most of their operators were born. Replacing them "
          "with heavier lifting gear lets the yard handle larger hull blocks and cuts weeks from each build. The bill is high "
          "and the old crane drivers resent the new controls, but the yard takes orders it once turned away.",
          ('tools', 'navy'), after=('yrd_count_slipways',), reward=(Build('dockyard', 1, 605),)),
    Focus('yrd_welders', 'A School for Welders',
          "Yard foremen complain that skilled welders leave for foreign yards as soon as they are trained. A public school "
          "beside the Cabarion berths takes apprentices from all four coastal provinces, pays a stipend and binds graduates to "
          "three years of home service. It costs the treasury steadily and pays off slowly, in hulls that pass inspection.",
          ('training', 'tools'), after=('yrd_count_slipways',), reward=(Idea('yard_apprentices'),)),
    Focus('yrd_hulls_export', 'Hulls for Foreign Owners',
          "The yards bid for merchant hulls ordered by foreign shipping companies, offering low prices backed by state "
          "credit. Order books fill and berths run continuously. The country becomes a supplier to other nations' fleets, "
          "exposed to every swing in freight rates abroad, and its own navy waits in line behind paying customers.",
          ('navy', 'economy'), after_any=('yrd_crane_renewal', 'yrd_welders'), cost=10,
          exclusive=('yrd_naval_programme', 'yrd_refit_trade'),
          reward=(SwapIdea('slipway_ledger', 'hull_exports'), Flag('yards_export'))),
    Focus('yrd_naval_programme', 'A Naval Programme First',
          "The navy argues that a coast this long, with harbours this busy, needs more than a handful of coastal escorts. A "
          "programme of corvettes, patrol craft and submarines would keep every berth working on state orders. Yard income "
          "becomes predictable. The bill lands on the budget every year, and the commercial lines lose their repair slots.",
          ('navy', 'command'), after_any=('yrd_crane_renewal', 'yrd_welders'), cost=10,
          exclusive=('yrd_hulls_export', 'yrd_refit_trade'),
          reward=(SwapIdea('slipway_ledger', 'naval_programme'), Flag('yards_navy'))),
    Focus('yrd_refit_trade', 'Repair and Refit for All',
          "A third school says new hulls are a crowded market and repairs are not. Dry docks and fitting-out quays would serve "
          "any ship that passes the western coast, at fixed and published prices. Margins are thin but reliable, and the "
          "skills transfer to wartime damage control. The yards give up the prestige of launching ships.",
          ('tools', 'economy'), after_any=('yrd_crane_renewal', 'yrd_welders'), cost=10,
          exclusive=('yrd_hulls_export', 'yrd_naval_programme'),
          reward=(SwapIdea('slipway_ledger', 'refit_trade'), Flag('yards_refit'))),
    Focus('yrd_export_credit', 'Export Credit for Hull Buyers',
          "Foreign buyers want financing as much as steel. A state credit office in Marcil lends to shipping companies that "
          "order hulls from Arklith yards, secured on the ships themselves. Two berths at Arklith del Sur are lengthened for "
          "the first contracts. Defaults will come in a bad year, and the treasury will carry them.",
          ('economy', 'diplomacy'), after=('yrd_hulls_export',),
          exclusive=('yrd_escort_class', 'yrd_dry_docks'), reward=(Build('dockyard', 1, 140),)),
    Focus('yrd_escort_class', 'A Domestic Escort Class',
          "Naval architects design a coastal escort that the yards can build in series, using the hull lines of the existing "
          "patrol craft and domestic guns where possible. The first keel is laid at Arklith del Sur with a ceremony the navy "
          "enjoys more than the treasury. Series production lowers the unit price after the costly first hull.",
          ('navy', 'medal'), after=('yrd_naval_programme',),
          exclusive=('yrd_export_credit', 'yrd_dry_docks'),
          reward=(Build('dockyard', 1, 140), Research('naval_equipment', 0.5, 1))),
    Focus('yrd_dry_docks', 'Dry Docks on the Cabar Coast',
          "The Cabar coast has deep water close to shore and chromium mines in the hills behind it, which makes it a natural "
          "place for heavy repair. Two dry docks large enough for any merchant ship on the western routes are cut into the "
          "shoreline. Owners pay for speed and certainty; the yard pays for its machinery for a decade.",
          ('tools', 'bridge'), after=('yrd_refit_trade',),
          exclusive=('yrd_export_credit', 'yrd_escort_class'), reward=(Build('dockyard', 1, 222),)),
    Focus('yrd_guarantee_fund', 'A Guarantee Fund for the Yards',
          "Shipbuilding runs on long contracts and short cash. A guarantee fund, paid into by every yard and backed by the "
          "treasury, covers suppliers when a buyer defaults mid-build. Owners grumble at the levy. Suppliers stop demanding "
          "payment in advance, and smaller yards can bid for contracts that used to go only to the largest.",
          ('scales', 'navy'), after_any=('yrd_export_credit', 'yrd_escort_class', 'yrd_dry_docks'),
          reward=(Flag('yard_guarantee'), PP(-25))),
))

FLEET = Branch('fleet', 'The Merchant Flag', 1992, 'FOCUS_FILTER_STABILITY', (
    Focus('flt_count_flag', 'Count the Merchant Flag',
          "Several hundred merchant ships fly the Arklith flag, a large fleet for a country of eight provinces. Many are old, "
          "some are registered here only for the low fees, and a few have not called at Puerto Tranquilidad in years. Before "
          "setting maritime policy, the shipping office counts which hulls are truly Arklith's and who crews them.",
          ('logistics', 'document'), reward=(Event('under_whose_flag'), PP(10))),
    Focus('flt_seafarers_college', 'The Seafarers College',
          "Officers and engineers for the merchant fleet have trained abroad or aboard, with no national standard. A "
          "seafarers college at Puerto Tranquilidad sets examinations recognised by foreign insurers, which lowers premiums for "
          "ships crewed by its graduates. The navy borrows its classrooms in winter, and the college needs old hulls to train on.",
          ('training', 'navy'), after=('flt_count_flag',), reward=(Idea('seafarers_college'),)),
    Focus('flt_open_register', 'Keep the Register Open',
          "Low fees and light inspection attract foreign owners, who register their ships in Arklith and pay tonnage dues to "
          "Cabaria. The income is steady and costs almost nothing to collect. Arklith's name appears on ships it does not "
          "control, crewed by people it has never met, and every accident at sea becomes partly its embarrassment.",
          ('document', 'economy'), after=('flt_count_flag',), exclusive=('flt_national_line',),
          reward=(Idea('open_register'),)),
    Focus('flt_national_line', 'Found a National Line',
          "The alternative tightens the register and gathers the best domestic hulls into a national line with regular "
          "sailings from Cabaria and Marcil. Foreign owners leave for cheaper flags and the dues fall. In exchange, the "
          "country gains a fleet it can count on in a crisis, crewed by its own seafarers and maintained in its own yards.",
          ('navy', 'logistics'), after=('flt_count_flag',), exclusive=('flt_open_register',),
          reward=(Idea('national_line'),)),
    Focus('flt_quay_inspectors', 'Inspectors on Every Quay',
          "Two groundings and a fire in harbour push the open register to hire inspectors who board every foreign-owned ship "
          "at its first Arklith call. Some owners leave rather than pay for repairs. Those who stay keep the dues coming, and "
          "harbour pilots stop refusing to bring certain hulls alongside after dark.",
          ('security', 'document'), after=('flt_open_register',), exclusive=('flt_scheduled_sailings',),
          reward=(SwapIdea('open_register', 'inspected_register'),)),
    Focus('flt_scheduled_sailings', 'Scheduled Sailings Abroad',
          "The national line publishes a timetable: weekly sailings linking Cabaria, Marcil and Leonim with foreign ports, "
          "whatever the cargo. Shippers in the Llano can plan around fixed dates for the first time. Empty sailings cost money "
          "in slow months, and the quay roads at Arklith del Sur are widened so trucks can meet the ships.",
          ('logistics', 'navy'), after=('flt_national_line',), exclusive=('flt_quay_inspectors',),
          reward=(Build('infrastructure', 1, 140),)),
    Focus('flt_harbour_tariff', 'One Tariff for All Harbours',
          "Each harbour on the coast charges its own dues, set by local custom and local friendships. A single published tariff "
          "for berthing, pilotage and storage now applies from the Cabar coast to Leonim. Some harbour boards lose income and "
          "lobby hard. Shippers stop haggling, and smaller ports win traffic they used to lose to the capital.",
          ('scales', 'logistics'), after_any=('flt_quay_inspectors', 'flt_scheduled_sailings'),
          reward=(Idea('harbour_tariff'),)),
    Focus('flt_laid_up_reserve', 'A Reserve of Laid-Up Hulls',
          "Rather than scrap the oldest ships, the shipping office lays up a dozen in sheltered water off Cabarion with "
          "skeleton crews and a maintenance budget. In normal years they cost money and look like rust. In a crisis they can "
          "carry grain, fuel or evacuees within weeks, which is far cheaper than chartering at emergency rates.",
          ('navy', 'shelter'), after=('flt_seafarers_college',), reward=(Flag('hull_reserve'), PP(-15))),
))

NAVY = Branch('navy', 'The Coastal Squadrons', 1993, 'FOCUS_FILTER_NAVY_XP', (
    Focus('nav_squadron_review', 'Review the Coastal Squadrons',
          "The navy is a coastal force of light escorts and a few submarines, based at Puerto Tranquilidad, Cabarion, Marcil "
          "and Leonim. Its doctrine is to stay intact and threaten, never to seek battle. A review of every hull's readiness, "
          "from engines to ammunition stocks, tells the admirals how much of that threat is real and how much is paint.",
          ('navy', 'document'), reward=(Idea('kept_in_being'), XP('navy', 10))),
    Focus('nav_lane_patrols', 'Patrol the Shipping Lanes',
          "With hundreds of merchant ships under the flag, one school of officers wants the escorts at sea, shadowing the "
          "busiest lanes off the western coast and meeting convoys at the edge of territorial waters. Fuel and wear rise "
          "steeply. Merchant captains see grey hulls on the horizon, and insurers take note of a navy that actually sails.",
          ('navy', 'logistics'), after=('nav_squadron_review',), exclusive=('nav_harbour_approaches',),
          reward=(Idea('lane_patrols'),)),
    Focus('nav_harbour_approaches', 'Hold the Harbour Approaches',
          "The other school keeps the escorts close and makes the harbour mouths themselves hard to enter: mine stores, boom "
          "nets, coastal radar and submarines on station outside each major port. It burns less fuel and protects the yards "
          "directly. Merchant ships beyond the horizon must look after themselves until they reach the guarded water.",
          ('submarine', 'security'), after=('nav_squadron_review',), exclusive=('nav_lane_patrols',),
          reward=(Idea('guarded_approaches'),)),
    Focus('nav_far_tender', 'A Tender for Distant Patrols',
          "Escorts on long patrols return to port every few days to refuel, which wastes half their time at sea. A converted "
          "merchant hull from the laid-up reserve becomes a fleet tender, carrying fuel, spares and a small workshop. The "
          "escorts stay out twice as long. A single tender is also a single target, and the admirals know it.",
          ('carrier', 'logistics'), after=('nav_lane_patrols',), requires=(HasFlag('hull_reserve'),),
          exclusive=('nav_headland_radar',), reward=(XP('navy', 20), Research('naval_equipment', 0.5, 1))),
    Focus('nav_headland_radar', 'Radar Above Marcil and Leonim',
          "Radar sets on the headlands above Marcil and Leonim watch every approach to the southern harbours day and night. "
          "Operators train with the harbour pilots so that a stranger on the screen is identified within minutes. The stations "
          "need power lines, roads and relief crews in bad weather, and the rains test all three.",
          ('radar', 'navy'), after=('nav_harbour_approaches',), exclusive=('nav_far_tender',),
          reward=(Build('radar_station', 1, 140),)),
    Focus('nav_submarine_school', 'Training the Submarine Crews',
          "Arklith's few coastal submarines are crewed by sailors who learned from older crews and from manuals in foreign "
          "languages. A training flotilla based at Cabarion standardises drills, escapes and torpedo handling, using one boat "
          "as a permanent classroom. Fewer patrol hours is the price of crews who know what to do when something fails underwater.",
          ('submarine', 'training'), after=('nav_squadron_review',),
          reward=(XP('navy', 15), Research('naval_equipment', 0.75, 1))),
    Focus('nav_convoy_exercise', 'Exercise with the Merchants',
          "Once a year the navy and the merchant fleet rehearse a crisis: ships gather off Cabaria, sail in convoy along the "
          "coast and practise signals, zigzags and emergency dispersal. Shipping lines lose a few days of trade each time. "
          "Masters learn the navy's signals, the navy learns how slowly a laden freighter turns, and both trust each other more.",
          ('navy', 'communications'), after_any=('nav_far_tender', 'nav_headland_radar', 'nav_submarine_school'),
          reward=(Flag('convoy_drill'), XP('navy', 10))),
))

HIGHLANDS = Branch('highlands', 'The Nieblo Highlands', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('hil_survey', 'Survey the Nieblo Seams',
          "Most of the country's arms plants and nearly all of its aluminium and tungsten sit in the Nieblo highlands, where "
          "mining towns cling to valleys that see the sun late and lose it early. No modern survey says how much ore remains or "
          "how safe the shafts are. Geologists and inspectors spend two seasons underground before anyone decides anything.",
          ('tools', 'document'), reward=(Idea('nieblo_survey'), Event('highland_ledger'))),
    Focus('hil_shaft_safety', 'Shaft Safety Inspectors',
          "The survey found ventilation that fails in summer, timber props past their age and escape routes blocked by spoil. "
          "A corps of mine inspectors with power to close a shaft on the spot is hired from among retired foremen. Output dips "
          "while faults are fixed. Accidents fall, and families stop gathering at the pithead every time a siren sounds.",
          ('security', 'tools'), after=('hil_survey',), reward=(Flag('shafts_inspected'), Stability(0.03))),
    Focus('hil_mountain_road', 'The Nieblo Mountain Road',
          "Ore and finished arms leave the Nieblo Mountains on a single road with hairpins that defeat heavy trucks in the "
          "rains. Engineers cut a new grade along the valley floor, with tunnels through two spurs and bridges built for heavy "
          "loads. It is the most expensive road in the country per kilometre, and soon the busiest.",
          ('bridge', 'logistics'), after=('hil_survey',), reward=(Build('infrastructure', 1, 609),)),
    Focus('hil_authority', 'One Highland Authority',
          "The state gathers the mines, smelters and arms plants of both Nieblo provinces under one highland authority, with a "
          "single budget and a single wage scale. Investment can be planned across the whole range rather than shaft by shaft. "
          "Private owners are bought out at prices they call insulting. The authority becomes the mountains' largest employer.",
          ('industry', 'command'), after_any=('hil_shaft_safety', 'hil_mountain_road'), cost=10,
          exclusive=('hil_leases',), reward=(SwapIdea('nieblo_survey', 'highland_authority'),)),
    Focus('hil_leases', 'Lease the Seams to the Houses',
          "The alternative leases each seam to commercial houses for twenty years in exchange for royalties and investment "
          "commitments. Capital arrives quickly, new shafts open and the treasury collects without managing anything. The "
          "houses decide which towns grow and which close, and miners deal with distant boards rather than their government.",
          ('economy', 'tools'), after_any=('hil_shaft_safety', 'hil_mountain_road'), cost=10,
          exclusive=('hil_authority',), reward=(SwapIdea('nieblo_survey', 'highland_leases'),)),
    Focus('hil_aluminium_works', 'Aluminium Works in the East',
          "Bauxite from the eastern valleys has always left the country as raw ore. The highland authority builds a reduction "
          "works near the mines of Eastern Nieblo, drawing on the local oil wells for power. Ingots instead of ore mean more "
          "value kept at home and a domestic metal supply for aircraft parts, at the price of a decade of debt.",
          ('industry', 'air'), after=('hil_authority',), exclusive=('hil_lease_arsenal',),
          reward=(Build('industrial_complex', 1, 252),)),
    Focus('hil_lease_arsenal', 'A Leased Arsenal Line',
          "One of the leaseholders proposes to add a modern arms line beside its new shafts in Eastern Nieblo, selling light "
          "weapons to the army and to approved foreign buyers. The state gains jobs and a domestic supplier without spending a "
          "coin. It also gains a private arms maker on a frontier shared with three neighbours, with interests of its own.",
          ('missile', 'economy'), after=('hil_leases',), exclusive=('hil_aluminium_works',),
          reward=(Build('arms_factory', 1, 252),)),
    Focus('hil_tungsten_tools', 'Tungsten for Machine Tools',
          "Tungsten from the Nieblo seams is sold abroad as concentrate and bought back as cutting tools at many times the "
          "price. A small tool works in the Nieblo Mountains turns concentrate into drill bits and lathe tools for the Llano "
          "factories. The plant is modest; the lesson that ore can be finished at home matters more than its output.",
          ('tools', 'industry'), after_any=('hil_authority', 'hil_leases'),
          reward=(Build('industrial_complex', 1, 609), Research('industry', 0.5, 1))),
    Focus('hil_nieblo_power', 'Power Lines over the Passes',
          "Mines and arms halls in the Nieblo run on local diesel generators that fail in the cold months. A high-voltage line "
          "from the Llano grid crosses the passes to Eastern Nieblo, carried on towers that line crews must reach on foot. "
          "Factories gain steady power; the line becomes the first thing a storm or a saboteur would cut.",
          ('industry', 'bridge'), after=('hil_mountain_road',),
          reward=(Build('infrastructure', 1, 252), Research('construction_tech', 0.5, 1))),
    Focus('hil_miners_compact', 'A Compact with the Miners',
          "Miners' delegates, the managers of the seams and the safety inspectors sign a compact on pay, shifts and housing for "
          "the mountain towns. Strikes become rarer because grievances now have a table. Wages rise faster than output for a "
          "few years. The highlands stop being the place the coast forgets until something goes wrong underground.",
          ('peace', 'tools'), after=('hil_tungsten_tools',), requires=(HasFlag('shafts_inspected'),),
          reward=(Idea('miners_compact'),)),
))

BASIN = Branch('basin', 'Halloma Oil and Timber', 1993, 'FOCUS_FILTER_INDUSTRY', (
    Focus('bas_field_study', 'Study the Halloma Field',
          "The Halloma Basin holds the largest oil field in the country, under forest and farmland on the Perbla frontier. "
          "Wells were drilled piecemeal by small operators, and much of the crude leaves by truck. A field study maps pressure, "
          "reserves and the condition of every pump. Without it, any plan for the basin is only a guess.",
          ('economy', 'document'), reward=(Idea('halloma_field_study'), Research('excavation_tech', 0.5, 1))),
    Focus('bas_refine_home', 'Refine at Halloma',
          "A refinery in the basin turns crude into diesel and fuel oil for the yards, the fishing fleets and the army's "
          "trucks. Imports of refined fuel fall, and the basin gains skilled jobs. Refineries are expensive, dirty and slow to "
          "pay back. Neighbouring farms complain about the smell, and the local fire brigade doubles its training.",
          ('industry', 'tools'), after=('bas_field_study',), cost=10, exclusive=('bas_crude_exports',),
          reward=(Build('industrial_complex', 1, 37),)),
    Focus('bas_crude_exports', 'Crude Through Cabaria',
          "The cheaper course moves crude to the coast and sells it unrefined to foreign buyers from the Cabaria terminals. "
          "Revenue arrives quickly and the treasury needs it. The country keeps importing refined fuel at prices set elsewhere, "
          "and the basin stays a place where oil is pumped and then leaves for someone else to process.",
          ('economy', 'logistics'), after=('bas_field_study',), cost=10, exclusive=('bas_refine_home',),
          reward=(Idea('crude_exports'),)),
    Focus('bas_fuel_depots', 'Fuel Depots for the Coast',
          "Diesel and fuel oil from the new refinery are stored in depots at every coastal base from the Cabar coast to "
          "Leonim, so the escorts and the yards no longer wait for imported tankers. The depots need guards and fire crews. "
          "Ships refuel at home, faster and cheaper, and the navy stops rationing its patrol hours in the dry months.",
          ('logistics', 'navy'), after=('bas_refine_home',), exclusive=('bas_pipeline',),
          reward=(TimedIdea('fuel_depots', 1095),)),
    Focus('bas_pipeline', 'The Basin Pipeline',
          "A pipeline from the Halloma field to the Cabaria terminals replaces the tanker trucks that crowd the northern "
          "roads. Construction crews follow the existing routes through the forest, and the line opens after two dry seasons. "
          "Trucking firms lose their best contract. Crude moves faster and more cheaply, and the roads grow safer.",
          ('logistics', 'bridge'), after=('bas_crude_exports',), exclusive=('bas_fuel_depots',),
          reward=(Build('infrastructure', 1, 37),)),
    Focus('bas_forestry_office', 'A Forestry Office for the Basin',
          "The basin forests supply pit props for the Nieblo mines, scaffolding for the yards and timber for the housing the "
          "Llano still lacks. Logging is unregulated and the best stands near the roads are gone. A forestry office sets "
          "quotas, replants cleared land and licenses sawmills, which costs the loggers this year and saves them in twenty.",
          ('civil', 'tools'), after=('bas_field_study',), reward=(Research('construction_tech', 0.5, 1), PP(15))),
    Focus('bas_end_flaring', 'End the Gas Flaring',
          "Operators in the basin burn off the gas that comes up with the crude because nobody pays for it. Capturing it for "
          "the Halloma towns and the nearest factories costs compressors and pipe, and the operators want the state to pay. "
          "The flares go dark one by one, and the basin towns get gas heating for the first time.",
          ('civil', 'economy'), after_any=('bas_fuel_depots', 'bas_pipeline'),
          reward=(Stability(0.02), Research('excavation_tech', 0.5, 1))),
))

LLANO = Branch('llano', 'The Llano Metropolis', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('lla_works_council', 'The Llano Works Council',
          "Seven large works and hundreds of small shops make the city of Arklith the country's industrial heart. Owners, "
          "unions and the city council meet only when something has already gone wrong. A standing works council brings them "
          "to one table every month to plan power, transport and training together. It slows nothing down except surprises.",
          ('industry', 'assembly'), reward=(Idea('llano_works_council'), Event('llano_works'))),
    Focus('lla_machine_tools', 'Machine Tools for the Plain',
          "Many Llano workshops still run lathes bought second-hand a generation ago. A state leasing scheme lets shops "
          "replace them with modern machine tools and repay from the extra output. Larger works lose their monopoly on "
          "precision jobs. The first year floods the plain with half-trained operators; by the second the scrap rate halves.",
          ('tools', 'industry'), after=('lla_works_council',),
          reward=(Build('industrial_complex', 1, 241), Research('industry', 0.5, 1))),
    Focus('lla_technical_college', 'A Technical College for Arklith',
          "Engineers for the Llano factories are trained abroad or not at all. A technical college in the city of Arklith "
          "offers degrees in mechanical, electrical and chemical engineering with placements in the local works. It costs a "
          "steady budget and takes years to graduate its first class. The factories stop poaching each other's graduates.",
          ('science', 'training'), after=('lla_works_council',), reward=(Idea('llano_college'),)),
    Focus('lla_household_goods', 'Goods for Every Household',
          "The works council proposes that the Llano turn toward refrigerators, radios, bicycles and buses for the domestic "
          "market, with tax relief for families who buy local. Shops fill and wages feel larger. The yards and the army find "
          "the plain's best engineers busy with kitchen appliances, and exporters complain the home market makes factories lazy.",
          ('economy', 'civil'), after_any=('lla_machine_tools', 'lla_technical_college'), cost=10,
          exclusive=('lla_capital_goods',), reward=(SwapIdea('llano_works_council', 'household_goods'),)),
    Focus('lla_capital_goods', 'Machines That Make Machines',
          "The other camp wants the plain to make pumps, engines, rail stock and machine tools: the equipment that other "
          "industries depend on. Investment goes to heavy plant and long training. Households wait longer for their comforts. "
          "In return, the country can repair and replace its own equipment instead of waiting on foreign suppliers.",
          ('tools', 'industry'), after_any=('lla_machine_tools', 'lla_technical_college'), cost=10,
          exclusive=('lla_household_goods',), reward=(SwapIdea('llano_works_council', 'capital_goods'),)),
    Focus('lla_bus_works', 'Buses and Trucks from the Llano',
          "A converted works on the edge of Arklith builds buses for every province and light trucks for farms and mines. "
          "Domestic models are heavier and plainer than imports, and drivers grumble about the gearboxes. Spare parts are cheap "
          "and always in stock, and the mountain towns finally get buses designed for their roads.",
          ('logistics', 'civil'), after=('lla_household_goods',), exclusive=('lla_rail_stock',),
          reward=(Build('industrial_complex', 1, 241),)),
    Focus('lla_rail_stock', 'Rolling Stock Built at Home',
          "The coast railway and the Llano lines run on locomotives and wagons bought abroad over decades, in six incompatible "
          "types. A rolling stock works in the metropolis builds a single standard wagon and a heavy freight locomotive under "
          "licence. Delivery is slow at first, and every unit can be repaired with parts made a few streets away.",
          ('rail', 'industry'), after=('lla_capital_goods',), exclusive=('lla_bus_works',),
          reward=(Build('industrial_complex', 1, 241), Research('train_tech', 0.5, 1))),
    Focus('lla_sustainment_institute', 'The Sustainment Institute',
          "The technical college opens an institute devoted to keeping things running: maintenance schedules, spare-part "
          "standards and repair methods for everything from buses to coastal escorts. Foreign partners rarely sell such "
          "research. Results appear as fewer breakdowns rather than new inventions, which makes the institute hard to defend in "
          "budget debates.",
          ('science', 'tools'), after_any=('lla_bus_works', 'lla_rail_stock'), after=('lla_technical_college',),
          reward=(SwapIdea('llano_college', 'sustainment_institute'),)),
    Focus('lla_housing', 'Housing for the Factory Districts',
          "Workers drawn to the metropolis from the highlands and the coast crowd into districts built for half their number. "
          "A housing programme builds apartment blocks near the works, financed by long state loans to the city. Builders "
          "compete with the factories for labour. New tenants arrive faster than the blocks rise, but the worst districts empty.",
          ('civil', 'rebuild'), after=('lla_works_council',), reward=(TimedIdea('housing_drive', 1095),)),
    Focus('lla_standard_parts', 'One Standard for Spare Parts',
          "Every ministry, the army and the yards buy spare parts to their own specifications, so a bolt for a bus does not "
          "fit a truck from the same works. The institute publishes national standards for fasteners, bearings, fittings and "
          "hoses, and state buyers must follow them. Suppliers retool reluctantly. Warehouses shrink and repairs speed up.",
          ('document', 'tools'), after=('lla_sustainment_institute',), reward=(Idea('standard_parts'),)),
))

ARMY = Branch('army', 'Service and Sustainment', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('arm_count_army', 'A Small Army Counts Itself',
          "The army keeps barracks in every province, a mountain detachment in the Nieblo and almost no public interest in its "
          "affairs. War support sits near the bottom of any measure the ministries use. Before asking for anything, the general "
          "staff audits its own stocks: rifles, trucks, artillery, spare parts and the soldiers who could actually be fielded.",
          ('security', 'document'), reward=(Event('army_counts'), XP('army', 10))),
    Focus('arm_repair_shops', 'Repair Shops in Every Garrison',
          "Trucks and guns that break down wait months for parts from a central depot near Cabaria. Each garrison now gets its "
          "own repair shop with mechanics, a small parts store and authority to cannibalise wrecks. Inventory costs rise and "
          "accountants complain about duplication. Vehicles return to service in days instead of seasons.",
          ('tools', 'security'), after=('arm_count_army',), reward=(Idea('garrison_workshops'),)),
    Focus('arm_mountain_corps', 'The Nieblo Mountain Corps',
          "Three frontiers meet in the Nieblo highlands, and the general staff proposes that the army's best units train to "
          "fight there: mountain infantry, pack transport and light artillery that can be carried up a slope. The corps would "
          "hold the passes against any intruder. The Llano and the coast would be guarded by reservists only.",
          ('security', 'training'), after=('arm_count_army',), cost=10, exclusive=('arm_llano_reserve',),
          reward=(Idea('mountain_corps'),)),
    Focus('arm_llano_reserve', 'A Mobile Reserve on the Llano',
          "The rival plan concentrates the army on the open plain around the metropolis, motorised and ready to move by road "
          "or rail to any province within days. One central reserve covers every frontier at once, on paper. In the highlands "
          "it would arrive late and tired, and the mountain towns doubt anyone would come at all.",
          ('logistics', 'command'), after=('arm_count_army',), cost=10, exclusive=('arm_mountain_corps',),
          reward=(Idea('llano_reserve'),)),
    Focus('arm_pack_artillery', 'Pack Artillery for the Passes',
          "Field guns that need a road are useless above the Nieblo valleys. The corps adopts light mountain guns that break "
          "down into mule and truck loads, with crews drilled to reassemble them on a ridge in under an hour. Range and weight "
          "of shell are modest. The guns arrive where heavier artillery could only watch from below.",
          ('missile', 'training'), after=('arm_mountain_corps',), exclusive=('arm_motor_pool',),
          reward=(Research('artillery', 0.5, 1), XP('army', 15))),
    Focus('arm_motor_pool', 'A Motor Pool for the Reserve',
          "A reserve that moves by road needs trucks, fuel and drivers who know every route. The army leases trucks from the "
          "Llano works in peacetime and keeps a depot of its own on the edge of the plain, with paved loading yards beside the "
          "trunk highway. Army and manufacturers find the tie convenient until a crisis tests it.",
          ('logistics', 'tools'), after=('arm_llano_reserve',), exclusive=('arm_pack_artillery',),
          reward=(Build('infrastructure', 1, 241),)),
    Focus('arm_volunteer_army', 'A Volunteer Army',
          "With war support this low, compulsion would be resented in every province. The general staff proposes a smaller "
          "army of long-service volunteers on decent pay, with skills civilian employers value when they leave. Recruitment "
          "posters go up in the Llano and the highlands. The force shrinks in numbers and grows in competence.",
          ('medal', 'training'), after=('arm_repair_shops',), exclusive=('arm_territorial_militia',),
          reward=(Idea('volunteer_service'),)),
    Focus('arm_territorial_militia', 'Territorial Militias',
          "The alternative asks every province to raise a part-time militia, drilling on weekends and guarding its own towns, "
          "bridges and harbours in an emergency. It is cheap and keeps the army visible in daily life. Training is thin and "
          "equipment basic. Every province gains a reason to care about defence, and neighbours notice the armed civilians.",
          ('security', 'civil'), after=('arm_repair_shops',), exclusive=('arm_volunteer_army',),
          reward=(Idea('territorial_militia'),)),
    Focus('arm_sustainment_doctrine', 'A Doctrine of Sustainment',
          "The general staff writes down what a small country can actually do: fight close to home, keep every vehicle running "
          "and never outrun its supplies. The doctrine favours firepower over manoeuvre and the integrity of units over bold "
          "thrusts. It is not exciting reading. It is honest about the army's size, which earlier plans never were.",
          ('document', 'logistics'), after_any=('arm_volunteer_army', 'arm_territorial_militia'),
          reward=(SwapIdea('garrison_workshops', 'sustainment_doctrine'), Research('land_doctrine', 0.5, 1))),
))

AIR = Branch('air', 'The Air Arm', 1994, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count_squadrons', 'Count the Fighter Squadrons',
          "Two dozen fighters and a handful of support aircraft make up the air arm, spread across fields at Cabaria, the "
          "Halloma Basin, Arklith del Sur and the Llano. Pilots fly too few hours and spares arrive late. The air staff's "
          "first task is to work out how many aircraft could fly on any given morning, and the answer is uncomfortable.",
          ('air', 'document'), reward=(Idea('small_air_arm'), XP('air', 10))),
    Focus('air_sea_lanes', 'Wings over the Sea Lanes',
          "The air arm could serve the merchant fleet: patrol aircraft and fighters based on the coast, watching the shipping "
          "lanes and the harbour approaches, working alongside the navy's escorts. Coastal fields get the money. The interior "
          "and the highland frontiers would rely on the army's own guns if anything came over the mountains.",
          ('air', 'navy'), after=('air_count_squadrons',), cost=10, exclusive=('air_highland_screen',),
          reward=(Idea('sea_lane_wing'),)),
    Focus('air_highland_screen', 'A Screen over the Highlands',
          "The rival plan builds a fighter screen over the inland frontiers, with fields in the Nieblo foothills and radar on "
          "the ridges, so that nothing crosses from any neighbour unseen. It protects the arms plants and the metropolis. The "
          "coast keeps what it has, which is not much, and the shipping lines ask who will watch their lanes.",
          ('air', 'radar'), after=('air_count_squadrons',), cost=10, exclusive=('air_sea_lanes',),
          reward=(Idea('highland_screen'),)),
    Focus('air_norte_field', 'A Field at Arklith del Norte',
          "Arklith del Norte has busy coastal waters between the capital and Marcil but no airfield. A new field on the "
          "coastal plain gives patrol aircraft a base halfway down the coast. Farmers lose land and the rains delay the runway "
          "twice. When it opens, aircraft can reach any point on the western lanes within the hour.",
          ('runway', 'navy'), after=('air_sea_lanes',), exclusive=('air_nieblo_field',),
          reward=(Build('air_base', 2, 605),)),
    Focus('air_capital_radar', 'Radar over Puerto Tranquilidad',
          "The busiest harbour in the country has no radar of its own beyond what the ships carry. A station on the hills "
          "above Puerto Tranquilidad tracks aircraft and shipping across the northern approaches and reports to the coastal "
          "wing. Its operators learn to separate fishing boats from intruders, which takes most of a year.",
          ('radar', 'air'), after=('air_sea_lanes',), exclusive=('air_ridge_radar',),
          reward=(Build('radar_station', 1, 398),)),
    Focus('air_nieblo_field', 'A Field in the Nieblo Foothills',
          "The Nieblo Mountains have no airfield, only a strip used by mail planes. Engineers level a plateau in the foothills "
          "for a fighter field with hardened shelters. The approach is difficult in cloud and the pilots who train there earn "
          "reputations. Fighters based in the foothills can meet anything crossing the passes before it reaches the Llano.",
          ('runway', 'security'), after=('air_highland_screen',), exclusive=('air_norte_field',),
          reward=(Build('air_base', 2, 609),)),
    Focus('air_ridge_radar', 'Radar on the Nieblo Ridges',
          "A radar post on the highest reachable ridge of the Nieblo looks across three frontiers at once. Supplies go up by "
          "cable car and, in winter, on the backs of the crew. The view on the screen is the widest in the country. Keeping "
          "the set running in the cold demands a relief rota that the air arm can barely staff.",
          ('radar', 'security'), after=('air_highland_screen',), exclusive=('air_capital_radar',),
          reward=(Build('radar_station', 1, 609),)),
    Focus('air_flying_school', 'A Flying School at Cabaria',
          "Pilots learn on operational fighters, which wastes airframes and fuel. A flying school at the Cabaria field with "
          "simple trainers and instructors drawn from the squadrons gives every new pilot two hundred hours before touching a "
          "fighter. Squadron strength dips while instructors teach. Graduates arrive knowing how to fly in coastal weather.",
          ('training', 'air'), after=('air_count_squadrons',), reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
    Focus('air_spares_pipeline', 'A Spares Pipeline for Aircraft',
          "Half the grounded aircraft on any morning wait for one missing part. The air arm sets up a spares pipeline with "
          "stock held at each field, overhaul contracts with the Llano works and a rule that no airframe is cannibalised "
          "without written approval. Availability rises month by month, and warehouses fill with parts that may never be used.",
          ('tools', 'air'), after_any=('air_norte_field', 'air_nieblo_field'),
          reward=(SwapIdea('small_air_arm', 'sustained_air_arm'),)),
))

FRONTIERS = Branch('frontiers', 'Four Frontiers', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('fro_one_map', 'Four Frontiers on One Map',
          "Arklith touches four neighbours: Perbla beyond the Halloma Basin and the Cabar hills, Leasath along the southern "
          "edge of the Llano and the Nieblo, Dakrain past Eastern Nieblo, and the Gibraltar Mining Zone south of Arklith del "
          "Sur. The foreign office has never set one policy for all four. A review puts them on one map and asks what each "
          "crossing is for.",
          ('diplomacy', 'document'), reward=(Idea('frontier_desks'), Event('four_frontiers'))),
    Focus('fro_perbla_customs', 'Customs Posts on the Perbla Road',
          "Most trade with Perbla crosses at the Halloma Basin on roads built for farm carts. New customs posts with covered "
          "inspection bays, and a resurfaced road to the frontier, cut waiting times for trucks in both directions. Arklith's "
          "traders press for lower tariffs in any deal. The posts are small buildings with a large effect on basin markets.",
          ('logistics', 'diplomacy'), after=('fro_one_map',), reward=(Build('infrastructure', 1, 37),)),
    Focus('fro_leasath_watch', 'Watch on the Southern Passes',
          "Leasath shares the longest frontier, along the southern Llano and the Nieblo passes, and its own politics are "
          "restless, with a nationalist movement that polls as strongly as its government. Arklith has no quarrel to pursue "
          "there. It does want early notice if anything changes, so observation posts on the passes report daily to Cabaria.",
          ('radar', 'diplomacy'), after=('fro_one_map',), reward=(Build('radar_station', 1, 252), XP('army', 10))),
    Focus('fro_dakrain_valley', 'A Valley Commission with Dakrain',
          "Eastern Nieblo's valleys run into Dakrain, and herders, ore trucks and smugglers use the same tracks. A joint valley "
          "commission meets each season to settle grazing, water rights and crossing hours. It has no power over claims and "
          "wants none. Small disputes stop climbing to the ministries, and the valley towns trade a little more openly.",
          ('peace', 'document'), after=('fro_one_map',),
          reward=(Flag('valley_commission'), Stability(0.02),
                  Tooltip('No claim, core or frontier change; the commission settles grazing, water and crossing hours.'))),
    Focus('fro_gibraltar_road', 'A Haul Road to the South',
          "The Gibraltar Mining Zone on the southern edge is run by its own mining administration. A graded haul road from the "
          "frontier toward the Marcil quays, with weighbridges and a customs yard, would offer the zone a shorter route to the "
          "sea if its administration wants one. Ore trucks would break up the surface every wet season, and maintenance grows.",
          ('logistics', 'tools'), after=('fro_one_map',), reward=(Build('infrastructure', 1, 140),)),
    Focus('fro_open_crossings', 'Frontiers Open for Trade',
          "One view says a small trading country lives by its crossings: lower tariffs, faster inspections and transit rights "
          "for neighbours' goods heading to the western ports. Traffic and revenue grow. So does smuggling, and the border "
          "police warn that open roads carry more than freight. The ports welcome every new truck from inland.",
          ('diplomacy', 'logistics'), cost=10,
          after_any=('fro_perbla_customs', 'fro_leasath_watch', 'fro_dakrain_valley', 'fro_gibraltar_road'),
          exclusive=('fro_neutral_watchful',), reward=(SwapIdea('frontier_desks', 'open_frontiers'),)),
    Focus('fro_neutral_watchful', 'Neutral and Watchful',
          "The other view keeps every crossing courteous and every treaty unsigned. Arklith promises nothing to anyone, buys "
          "arms from several suppliers and keeps its frontier posts manned in every season. It avoids entanglement in any "
          "neighbour's troubles. It also forgoes the trade friendlier frontiers would bring, and the basin traders say so.",
          ('security', 'peace'), cost=10,
          after_any=('fro_perbla_customs', 'fro_leasath_watch', 'fro_dakrain_valley', 'fro_gibraltar_road'),
          exclusive=('fro_open_crossings',), reward=(SwapIdea('frontier_desks', 'watchful_neutrality'),)),
    Focus('fro_transit_cabar', 'Transit Through the Cabar Hills',
          "Inland shippers ask to move goods through Arklith to the western harbours under bond, without paying duty twice. A "
          "transit agreement and a bonded warehouse zone on the Cabar coast make it possible, with the road through the hills "
          "improved for heavy trucks. Dock work grows. Customs officers must now trust paperwork stamped abroad.",
          ('logistics', 'navy'), after=('fro_open_crossings',), exclusive=('fro_frontier_police',),
          reward=(Build('infrastructure', 1, 222), PP(20))),
    Focus('fro_frontier_police', 'A Frontier Police Corps',
          "Customs men and soldiers have shared the frontier posts badly for years. A single frontier police corps, trained "
          "for searches, patrols and observation, takes over every crossing and the high ground between them, with a radar "
          "post above the Halloma road. Soldiers return to barracks, and the corps guards its independence jealously.",
          ('security', 'radar'), after=('fro_neutral_watchful',), exclusive=('fro_transit_cabar',),
          reward=(Build('radar_station', 1, 37), XP('army', 10))),
    Focus('fro_valley_markets', 'Markets at the Valley Crossings',
          "With the valley commission meeting regularly, the mining towns of Eastern Nieblo and their neighbours across the "
          "Dakrain line hold seasonal markets at the crossings. Wool, tools and produce change hands under the commission's "
          "eye. The trade is small in national terms. For the valley towns it separates a hard winter from a bearable one.",
          ('peace', 'economy'), after_any=('fro_transit_cabar', 'fro_frontier_police'),
          requires=(HasFlag('valley_commission'),), reward=(TimedIdea('valley_markets', 1095),)),
))

WARYEARS = Branch('waryears', 'The Belkan War Years', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_crisis_office', 'A Crisis Office in Cabaria',
          "In March 1995 the Belkan War breaks out far from Arklith's own frontiers. Arklith is not a party and has no wish to "
          "become one, but Perbla across the eastern frontier has old ties to Belka, and Arklith ships trade in seas the war now "
          "touches. The administration opens a crisis office in Cabaria to follow events hour by hour.",
          ('communications', 'command'), reward=(Idea('crisis_office'), Event('belkan_war_news'))),
    Focus('war_state_pool', 'A State War-Risk Pool',
          "Foreign insurers raise premiums on every ship that sails near the war, and some refuse cover altogether. A state "
          "war-risk pool insures Arklith-flagged hulls at fixed rates, backed by the treasury and the lines' own contributions. "
          "If a ship is lost, the pool pays and the treasury bleeds. Until then, the fleet keeps sailing while others wait.",
          ('scales', 'navy'), after=('war_crisis_office',), reward=(Idea('war_risk_pool'),)),
    Focus('war_trade_all', 'Carry Lawful Cargo for All',
          "As a neutral, Arklith may carry non-military goods for any buyer, and freight rates have doubled. Shipping lines want "
          "permission to take every legal cargo they can find. The treasury likes the revenue. Each sailing risks a ship, a "
          "crew and an incident that could pull the country into a quarrel, and every belligerent will read the manifests.",
          ('logistics', 'peace'), after=('war_crisis_office',), cost=10, exclusive=('war_close_ports',),
          reward=(Idea('neutral_carriers'),)),
    Focus('war_close_ports', 'Close the Ports to Belligerents',
          "The cautious course closes Arklith ports to warships and war cargoes of every belligerent, and bans Arklith ships "
          "from the war zones until the fighting ends. The fleet loses the richest freight in years and some owners reflag "
          "elsewhere. Nobody can accuse the Duchy of helping either side, and the coast stays quiet.",
          ('security', 'navy'), after=('war_crisis_office',), cost=10, exclusive=('war_trade_all',),
          reward=(Idea('closed_harbours'),)),
    Focus('war_manifests', 'Inspectors for Every Manifest',
          "Neutral trade is only neutral if the cargoes are what the papers say. Customs inspectors open containers at random "
          "in every port, and masters must sign declarations that their holds carry no munitions. Shipping lines complain "
          "about delays. When a foreign navy stops an Arklith ship at sea, the papers stand up and the ship sails on.",
          ('document', 'security'), after=('war_trade_all',), exclusive=('war_coast_alert',),
          reward=(Stability(0.03), Tooltip('Every outbound cargo is checked against the neutrality rules.'))),
    Focus('war_coast_alert', 'The Coast on Alert',
          "With the ports closed, the escorts and the harbour defences must turn away warships and enforce the ban. Radar "
          "crews watch the approaches day and night, and a new station at Arklith del Norte covers the gap north of Marcil. "
          "Sailors serve long watches. The coast learns what a neutral's readiness looks like when it must be enforced.",
          ('radar', 'security'), after=('war_close_ports',), exclusive=('war_manifests',),
          reward=(Build('radar_station', 1, 605), XP('navy', 10))),
    Focus('war_escorted_convoys', 'Neutral Convoys Under Escort',
          "Merchant masters who sailed in the annual exercise ask for escorts through the waters nearest the war. The navy "
          "forms small convoys off Cabaria, escorting them to the edge of the danger zone and meeting them on return. The "
          "escorts are few and stretched thin. The arrangement works, and its reputation travels among shipowners.",
          ('navy', 'communications'), after=('war_state_pool',), requires=(HasFlag('convoy_drill'),),
          reward=(TimedIdea('escorted_sailings', 365), XP('navy', 15))),
    Focus('war_postwar_freight', 'Freight After the Treaty',
          "The war ends with Belka defeated and a treaty signed at Lumen. Rebuilding across the region needs steel, cement, "
          "timber and ships to carry them, and freight markets stay busy for years. Arklith's yards and lines compete for the "
          "work with every neutral flag afloat, and owners argue about how long the boom can last.",
          ('rebuild', 'logistics'), after_any=('war_manifests', 'war_coast_alert', 'war_escorted_convoys'),
          requires=(HasGlobal('belka_lost_belkan_war'),), exclusive=('war_frontier_unease',),
          reward=(TimedIdea('postwar_freight', 730),)),
    Focus('war_frontier_unease', 'A Continent Off Balance',
          "Against most predictions, the war ends with Belka on top, and Perbla next door has reason to celebrate its old "
          "friend's success. Arklith has no cause to fear either country directly, yet the balance of the continent has "
          "shifted and nobody can say where it settles. Reserve officers are recalled for refresher training.",
          ('security', 'diplomacy'), after_any=('war_manifests', 'war_coast_alert', 'war_escorted_convoys'),
          requires=(HasGlobal('belka_won_belkan_war'),), exclusive=('war_postwar_freight',),
          reward=(TimedIdea('frontier_unease', 730),)),
))

SKY = Branch('sky', 'Ulysses Preparations', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_announcement', 'The Sky Has a Date',
          "The 1994 warning about Ulysses became a certainty in April 1996, when the FCU told the world to expect an impact. "
          "Where the fragments will come down is anyone's guess. Arklith keeps its government and harbours on an exposed coast "
          "and its factories on an open plain, so the administration starts planning for a threat with no address.",
          ('meteor', 'telescope'), reward=(Event('ulysses_announced'), PP(10))),
    Focus('sky_watch_room', 'A National Sky Watch',
          "Arklith has no great telescope of its own, but amateur astronomers, college physicists and the air arm's radar "
          "crews can share what they see. A national sky watch gathers foreign bulletins, local observations and radar reports "
          "in one room in Cabaria and issues a plain summary every week. Rumours weaken when facts arrive on schedule.",
          ('telescope', 'radar'), after=('sky_announcement',), reward=(Idea('sky_watch'),)),
    Focus('sky_shelters', 'Deep Shelters for Three Cities',
          "Engineers propose deep shelters beneath the metropolis on the Llano, the capital and the southern ports, stocked "
          "with water, food and medicine for weeks. The digging disrupts streets for years and the cost is enormous. If "
          "fragments fall on a city, people underground will live. If they fall elsewhere, the shelters become costly cellars.",
          ('shelter', 'civil'), after=('sky_announcement',), cost=10, exclusive=('sky_dispersal',),
          reward=(Idea('city_shelters'),)),
    Focus('sky_dispersal', 'Plans to Empty the Cities',
          "The cheaper plan accepts that no shelter is deep enough for a direct hit and prepares to move people instead: "
          "evacuation routes, reception towns in the highlands and the basin, fuel reserves and a fleet of buses and ships. "
          "It needs warning time and discipline. It also needs the countryside to welcome the cities, which is not guaranteed.",
          ('refugees', 'rail'), after=('sky_announcement',), cost=10, exclusive=('sky_shelters',),
          reward=(Idea('dispersal_plans'),)),
    Focus('sky_shelter_stores', 'Stores for the Shelters',
          "Shelters without supplies are traps. Contracts go to canning works and pharmacies for stocks rotated every two "
          "years, and a new packing plant at Arklith del Sur supplies the southern shelters and ships. Rotation sells old stock "
          "cheaply to the public, which proves popular. The plant keeps working long after the asteroid leaves the news.",
          ('medical', 'industry'), after=('sky_shelters',), exclusive=('sky_reception_towns',),
          reward=(Build('industrial_complex', 1, 140),)),
    Focus('sky_reception_towns', 'Reception Towns in the Highlands',
          "Highland and basin towns are assigned partner districts in the cities and plan to receive them: schools become "
          "dormitories, halls become clinics, and roads into the Nieblo are widened for buses. Rehearsals are awkward and some "
          "towns resent the burden. Families learn where they would go, which turns panic into a timetable.",
          ('refugees', 'civil'), after=('sky_dispersal',), exclusive=('sky_shelter_stores',),
          reward=(Build('infrastructure', 1, 609),)),
    Focus('sky_evacuation_ships', 'Reserve Hulls on Evacuation Duty',
          "The laid-up merchant hulls off Cabarion are surveyed, repaired and assigned to evacuation duty, each with a home "
          "port, a crew roster and a destination. Coastal towns that cannot be reached quickly by road now have a ship. "
          "Keeping the reserve seaworthy costs more each year, and the shipping office stops calling it a waste.",
          ('navy', 'refugees'), after_any=('sky_shelters', 'sky_dispersal'), requires=(HasFlag('hull_reserve'),),
          reward=(Stability(0.03), XP('navy', 10), Tooltip('The laid-up reserve hulls are assigned to evacuation duty.'))),
    Focus('sky_roche', 'Ulysses Overhead',
          "In July 1999 Ulysses passes through the Earth's Roche limit and begins to break apart. Every plan written since 1996 "
          "is now tested against reality. Sirens are checked, shelters and reception towns go on standby and the sky watch "
          "reports hourly. The country can do no more than it has done; what remains is to wait and keep order.",
          ('meteor', 'shelter'), after_any=('sky_shelter_stores', 'sky_reception_towns'), requires=(After('1999.7.8'),),
          reward=(Event('ulysses_overhead'),)),
    Focus('sky_relief_bureau', 'Counting the Damage and Debts',
          "Whatever fell, and wherever it fell, the months after the passage bring insurers reassessing every coast, ships "
          "seeking safe harbour and a public that wants to know what the preparations cost. A relief bureau in Cabaria handles "
          "arrivals, claims and the return of stocks to the market. It is the first such office, and the country keeps it.",
          ('refugees', 'medical'), after=('sky_roche',), reward=(Idea('relief_bureau'),)),
))

MILLENNIUM = Branch('millennium', 'The Duchy at the Millennium', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('mil_review', 'A Decade of the New Order',
          "Ten years after the National Administration first published its powers, the government commissions a review of what "
          "the decade built and what it cost: the order chosen in Cabaria, the yards, the highlands, the Llano and the "
          "frontiers. Its panel draws members from every province by lot. Its report will set the terms of politics.",
          ('document', 'ballot'), reward=(Event('decade_review'),)),
    Focus('mil_ducal_constitution', 'The Ducal Constitution',
          "The council consolidates its charter, the chamber's rules and the ducal prerogatives into one written "
          "constitution, signed by the duke and ratified by the chamber. Disputes that once needed private mediation go to a "
          "court. Every clause costs a negotiation. The result is a duchy whose government nobody needs to guess about.",
          ('document', 'medal'), after=('mil_review',), requires=(HasFlag('path_council'),),
          exclusive=('mil_household_code', 'mil_houses_charter', 'mil_civic_constitution'),
          reward=(SwapIdea('ducal_charter', 'ducal_constitution'),)),
    Focus('mil_household_code', 'The Household Code',
          "A decade of household government has run on custom and verbal instruction. The cabinet now publishes a code listing "
          "each prerogative of the ducal house, each power lent to ministers and the narrow agenda left to the advisory "
          "chamber. Opponents read it as a cage with a printed key. Foreign lenders read it as a contract they can price.",
          ('command', 'document'), after=('mil_review',), requires=(HasFlag('path_household'),),
          exclusive=('mil_ducal_constitution', 'mil_houses_charter', 'mil_civic_constitution'),
          reward=(SwapIdea('household_seals', 'household_code'),)),
    Focus('mil_houses_charter', 'A Charter for the Great Houses',
          "After a decade of complaints that the board governs like a cartel, the great houses accept a published charter: "
          "term limits for nominees, rules on conflicts of interest and an annual report to a public audit office. Some houses "
          "leave the board rather than open their books. Those who stay gain a legitimacy money could not buy.",
          ('economy', 'document'), after=('mil_review',), requires=(HasFlag('path_board'),),
          exclusive=('mil_ducal_constitution', 'mil_household_code', 'mil_civic_constitution'),
          reward=(SwapIdea('board_of_houses', 'houses_charter'),)),
    Focus('mil_civic_constitution', 'The Civic Constitution',
          "The civic assembly turns its first charter into a full constitution with a bill of rights, an independent court "
          "and fixed terms for the executive committee. The ducal title is written in as a ceremonial office with no veto. "
          "Ratification takes two sessions. Arklith ends the decade with rules that outlast any single majority.",
          ('ballot', 'scales'), after=('mil_review',), requires=(HasFlag('path_assembly'),),
          exclusive=('mil_ducal_constitution', 'mil_household_code', 'mil_houses_charter'),
          reward=(SwapIdea('civic_mandate', 'civic_constitution'),)),
    Focus('mil_rolls_ballot', 'Provincial Ballots on the Rolls',
          "The electoral rolls refreshed in the early nineties have been kept current, and the provincial councils have had "
          "a decade of practice. Councils are now chosen by ballot from the national rolls in every province, whatever the "
          "national order. Turnout in the highlands surprises everyone. Local politics finally has local voters.",
          ('ballot', 'civil'), after=('mil_review',), requires=(HasFlag('rolls_compiled'), HasFlag('councils_seated')),
          reward=(Stability(0.04), PP(-20), Tooltip('Provincial councils are chosen by ballot from the national rolls.'))),
    Focus('mil_yards_review', 'The Yards After Ten Years',
          "The yards enter the century busier than they began the last one, and more exposed. A review walks every berth again, "
          "this time measuring order books, debts and the health of the small suppliers along the coast. Its authors warn that "
          "one failed buyer could test every promise the state has made, and within weeks one does.",
          ('navy', 'scales'), after=('mil_review',), reward=(Event('yard_default', 20),)),
    Focus('mil_hull_contracts', 'Long Contracts for Hulls',
          "The export yards move from single orders to series contracts, building whole classes of hulls for foreign lines "
          "over many years. Berths plan a decade ahead and suppliers invest with confidence. The yards are now bound to the "
          "health of distant shipping companies, and every downturn abroad arrives in Marcil a few months later.",
          ('navy', 'diplomacy'), after=('mil_yards_review',), requires=(HasFlag('yards_export'),),
          exclusive=('mil_standing_squadron', 'mil_refit_network'), reward=(SwapIdea('hull_exports', 'hull_contracts'),)),
    Focus('mil_standing_squadron', 'A Standing Escort Squadron',
          "The naval programme matures into a standing squadron of domestically built escorts with a fixed replacement "
          "cycle, so that a new hull leaves the yards every year whatever the budget mood. The navy finally plans beyond one "
          "election or one cabinet. The treasury loses a lever it used to pull every lean year.",
          ('navy', 'medal'), after=('mil_yards_review',), requires=(HasFlag('yards_navy'),),
          exclusive=('mil_hull_contracts', 'mil_refit_network'), reward=(SwapIdea('naval_programme', 'standing_squadron'),)),
    Focus('mil_refit_network', 'A Refit Network on the Coast',
          "The refit trade grows from a few quays into a network: repair yards on every stretch of the western coast sharing "
          "parts, crews and booking systems, so a damaged ship goes to the nearest free dock. Owners know the prices in "
          "advance. The yards never launch a famous ship, and never lack work either.",
          ('tools', 'logistics'), after=('mil_yards_review',), requires=(HasFlag('yards_refit'),),
          exclusive=('mil_hull_contracts', 'mil_standing_squadron'), reward=(SwapIdea('refit_trade', 'refit_network'),)),
    Focus('mil_guarantee_tested', 'The Guarantee Fund Holds',
          "The yards guarantee fund, mocked for a decade as a levy on success, pays the suppliers of the failed buyer within a "
          "month. Not one small firm on the coast closes because of the default. Owners stop complaining about the levy, and "
          "foreign lenders begin offering the yards better terms on the strength of the fund.",
          ('scales', 'navy'), after=('mil_yards_review',), requires=(HasFlag('yard_guarantee'),),
          reward=(Idea('trusted_yards'),)),
    Focus('mil_usean_war', 'War on the Usean Continent',
          "In 2003 war returns to the Usean continent, and the FCU founds the ISAF to fight it. Arklith is a world away and "
          "has no part in it. Its shipping lines, insurers and yards feel it at once: freight rates rise, charter demand jumps "
          "and every route near Usea becomes a calculation. The shipping office convenes the lines to decide an answer.",
          ('communications', 'logistics'), after=('mil_review',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(Event('usean_freight'),)),
    Focus('mil_peaceful_charters', 'Charters for Peaceful Cargo',
          "The lines take grain, machinery and building materials for economies disrupted by the war, under strict rules on "
          "what may be carried and where. Inspectors check every manifest, as they learned to in 1995. Revenue is strong and "
          "the yards gain repair work from ships on longer routes. The risk to crews remains real.",
          ('logistics', 'economy'), after=('mil_usean_war',), exclusive=('mil_home_waters',),
          reward=(TimedIdea('usean_charters', 730),)),
    Focus('mil_home_waters', 'Keep the Fleet in Home Waters',
          "The government asks the lines to keep their ships on routes far from the fighting until the war ends, offering "
          "port fee relief in return. Some lines comply and some reflag. The fleet earns less and loses no one. In the ports, "
          "crews home for longer spells are grateful, and the merchant families say so publicly.",
          ('navy', 'peace'), after=('mil_usean_war',), exclusive=('mil_peaceful_charters',),
          reward=(TimedIdea('home_waters', 730),)),
    Focus('mil_llano_review', 'The Llano at the Millennium',
          "The metropolis has grown by a third since 1991, and its works have changed what they make. A review by the works "
          "council and the technical college asks which plants have a future in the new century. A new hall on the edge of "
          "Arklith goes to the strongest of them. The weakest learn that state orders will not last forever.",
          ('industry', 'scales'), after=('mil_review',), reward=(Build('industrial_complex', 1, 241),)),
    Focus('mil_basin_tools', 'Drilling Tools Made in the Basin',
          "The Halloma Basin enters the century with its oil better mapped and its forests better managed than before. A works "
          "for drilling equipment and pumps, built beside the field, keeps the maintenance money in the basin rather than "
          "paying foreign service firms. Operators sign long contracts. The basin begins making tools it once bought.",
          ('tools', 'economy'), after=('mil_review',), reward=(Build('industrial_complex', 1, 37),)),
    Focus('mil_open_contracts', 'Publish the State Contracts',
          "Yard credits, mining leases, road contracts and shelter supplies have all been awarded with little public scrutiny "
          "for a decade. An act requires every state contract above a modest value to be published with its price, supplier "
          "and delivery date. Suppliers who relied on quiet arrangements object. The next tenders come in noticeably cheaper.",
          ('scales', 'document'), after=('mil_review',), reward=(Idea('open_contracts'),)),
))

BRANCHES = (ADMIN, PORT, YARDS, HIGHLANDS, LLANO, FLEET, ARMY, BASIN, NAVY, FRONTIERS, AIR, WARYEARS, SKY, MILLENNIUM)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('yard_credit_line', 'Open a Yard Credit Line',
                'The treasury lends to idle berths for six months so they can bid on new contracts. Costs political power and ties '
                'up state credit.', 50, (TimedIdea('yard_credit', 180),), requires=(Completed('yrd_count_slipways'),),
                cooldown=365),
    DecisionDef('harbour_drill', 'Harbour Defence Drill',
                'Escorts, pilots and harbour crews rehearse closing the approaches to Puerto Tranquilidad. Gains naval experience '
                'at the cost of a day of port traffic.', 25, (XP('navy', 10), WarSupport(0.01)),
                requires=(Completed('nav_squadron_review'),), cooldown=180),
    DecisionDef('highland_road_crews', 'Highland Road Crews',
                'Road crews widen the valley road into Eastern Nieblo before the rains. A one-time works programme paid from the '
                'national budget.', 60, (Build('infrastructure', 1, 252),), requires=(Completed('hil_mountain_road'),)),
    DecisionDef('shelter_rotation', 'Rotate the Shelter Stocks',
                'Old shelter supplies are sold cheaply and replaced with fresh stock, which keeps the shelters credible and the '
                'public reassured.', 20, (Stability(0.02),), requires=(Completed('sky_shelters'),), cooldown=730),
    DecisionDef('capital_runways', 'Lengthen the Cabaria Runways',
                'The main field in Cabaria gains longer runways and new hardstands. A one-time investment for the air arm.',
                50, (Build('air_base', 2, 398),), requires=(Completed('air_count_squadrons'),)),
    DecisionDef('relief_voyage', 'Send a Relief Voyage',
                'A reserve hull sails with food and medicine for a stricken foreign port. Costs political power and earns goodwill '
                'at home.', 40, (TimedIdea('relief_voyages', 180),), requires=(Completed('sky_roche'),), cooldown=365),
    DecisionDef('freight_levy', 'War-Risk Freight Levy',
                'A temporary levy on charter profits earned during the Usean war funds the treasury. Unpopular with the lines.',
                10, (PP(60), Stability(-0.02)), requires=(Completed('mil_usean_war'),)),
)
