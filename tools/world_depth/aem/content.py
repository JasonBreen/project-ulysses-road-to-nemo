"""Aemurraq (AEM): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections suspended, neutrality 48 and fascism 50 percent popularity),
the unnamed starting office, the five 1991 states and their neutral district captions, and
the global flags other mod scripts already set. Official: ACES Chronicle rows used only as
date anchors for distant pressures, each cited by its exact key. Everything else, including
every Aemurraqi choice, office, idea, building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='AEM', name='Aemurraq', root='world', package='aem',
                  themes=('logistics', 'assembly', 'security'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots and '
           'tech_mountaineers. The starting leader is the unnamed National Administration office (AEM_ac_government_office, '
           'centrism), whose description says its 1991 holder has not been established. The tree never names a holder.',
           'mod/2985041246/history/countries/AEM - Aemurraq.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 160, 433, 451 (capital), 468 and 502, captioned Aemurraq District A, District B, Capital '
           'District, District D and District E by the neutral regional labels (canonical regional mapping unestablished); '
           'victory points Aemurraq Capital Centre (3496) and Aemurraq Logistics Centre 1330. Terrain counts from '
           'map/definition.csv: desert in every district, hills and jungle in 433 and 468, plains in 468. State 468 has 27 '
           'provinces, no infrastructure, no buildings and no resources. Naval base and two dockyards in 160. Land neighbours '
           'AZB, EHE and SOA computed from map/provinces.bmp. No place outside these captions is named.',
           'mod/2985041246/history/states/160-State_160.txt, 433-State_433.txt, 451-State_451.txt, 468-State_468.txt, '
           '502-State_502.txt; mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'tools/regional_labels/labels.json; mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role merchant route security; 7 civilian, 5 military and 2 naval '
           'factories; 4 infantry formations (6 battalions); 36 fighters on one air base; 2 coastal escorts; 60 convoys; '
           'civilian economy, export focus and volunteer only laws; research priority Physical Sustainment (transport, '
           'equipment replacement, affordable service). Fictional fiscal calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; tools/world_starts/sustainment.json; docs/WORLD_STARTS_CALIBRATION.md; '
           'tools/economy_v2/profiles.json; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses may strike the Earth. Used only as background to the '
           'Ulysses branch; no Aemurraqi role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Used only as the opening of the distant-war branch; Aemurraq takes no '
           'part and no Aemurraqi role is claimed.', '1995 / 03.25'),
    Source('Official',
           'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Used as the date gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official',
           'Date anchor: the FCU announces that Ulysses will impact the Earth. Used as the date gate of the Ulysses branch '
           'opening; where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries and work as aggressor squadrons. '
           'Used as the date gate and premise of the contract instructors focus; no individual is named and no hire by '
           'Aemurraq is claimed as fact.', '1998 / 06.19'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Used as the date gate of the Roche night event; '
           'no damage in Aemurraq is claimed.', '1999 / 07.08'),
    Source('Official',
           'Date anchor: Erusea stops taking in refugees. Used as the date gate of the harbour reception focus, framed as a '
           'pressure the government expects rather than a recorded arrival.', '2000 / 04.21'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air '
           'batteries. Used as the opening of the Usean war branch.', '2003 / SUMMER'),
    Source('Official',
           'The FCU establishes the ISAF. Used as the date gate of the fuel contracts focus, which is trade only and changes '
           'no faction.', '2003 / 08.22'),
    Source('Official',
           'Farbanti falls, the ISAF accepts the Erusean surrender and the Continental War ends. Background only; the '
           'outcome focuses read the mod outcome flags instead of assuming this ending.', '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt), '
           'ac_ucw_stonehenge_destroyed, ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory '
           '(common/scripted_effects/ac_ucw.txt). Each reaction is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Aemurraqi focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in the '
           'five 1991 states.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the caretaker question
    IdeaDef('caretaker_mandate', 'The Caretaker Mandate', 'An administration without a party governs on renewed emergency orders.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('assembly', 'document')),
    IdeaDef('constituent_promise', 'A Constituent Promise', 'An elected assembly will write the constitution the suspended elections were meant to serve.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('board_charters', 'Charters of the Export Boards', 'The oil, steel, aluminium and shipping boards claim a share of government.',
            {'production_factory_efficiency_gain_factor': 0.03, 'consumer_goods_factor': -0.03, 'stability_factor': -0.02}, ('economy', 'assembly')),
    IdeaDef('movement_squares', 'The Movement in the Squares', 'The nationalist movement fills the squares and presses its claim to the state.',
            {'war_support_factor': 0.06, 'stability_factor': -0.03, 'political_power_gain': 0.05}, ('security', 'ballot')),
    IdeaDef('route_officers', 'Officers of the Routes', 'Officers of the route services stand ready to hold the state.',
            {'political_power_gain': 0.10, 'army_org_factor': 0.04}, ('command', 'security')),
    IdeaDef('written_constitution', 'The Written Constitution', 'A ratified constitution with an elected chamber, district councils and a common court.',
            {'stability_factor': 0.08, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('scales', 'document')),
    IdeaDef('open_ledgers', 'Open Board Ledgers', 'Every board contract, price and royalty is published each year.',
            {'political_power_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.05, 'consumer_goods_factor': -0.03}, ('scales', 'economy')),
    IdeaDef('movement_brigades', 'Movement Brigades', 'Brigades of young movement members repair roads and guard depots in every district.',
            {'production_speed_infrastructure_factor': 0.15, 'war_support_factor': 0.06, 'stability_factor': 0.02}, ('civil', 'security')),
    IdeaDef('transition_timetable', 'The Transition Timetable', 'Published conditions under which the command council would hand power back.',
            {'stability_factor': 0.05, 'political_power_gain': 0.10, 'army_org_factor': 0.04}, ('command', 'document')),
    # the five districts
    IdeaDef('district_compact', 'The District Compact', 'A census-backed understanding among the five districts.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('assembly', 'logistics')),
    IdeaDef('district_councils', 'Elected District Councils', 'Each district has an elected council, its own works office and a budget line.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.15}, ('ballot', 'civil')),
    IdeaDef('capital_prefects', 'Prefects of the Capital', 'Prefects from the capital run every district on one code.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.05}, ('command', 'logistics')),
    IdeaDef('interior_council', 'The Interior Council', 'District D keeps a share of whatever is found beneath it.',
            {'stability_factor': 0.04, 'production_speed_industrial_complex_factor': 0.05}, ('assembly', 'civil')),
    # oil, steel and aluminium
    IdeaDef('fuel_ledger', 'The Fuel Ledger', 'One account of every well, pipeline and depot in the country.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.05}, ('document', 'industry')),
    IdeaDef('export_houses', 'Chartered Export Houses', 'Crude, steel and aluminium sold abroad through chartered houses.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': -0.03}, ('economy', 'logistics')),
    IdeaDef('home_refining', 'Refined at Home', 'Crude kept at home for refineries and smelters under protected prices.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': 0.02}, ('industry', 'tools')),
    IdeaDef('state_oil_office', 'The State Oil Office', 'One office sets output, prices and investment for every well.',
            {'political_power_gain': 0.05, 'production_speed_buildings_factor': 0.05}, ('command', 'industry')),
    IdeaDef('export_contracts', 'Twenty-Year Contracts', 'Long supply contracts guarantee tonnage and foreign currency.',
            {'industrial_capacity_factory': 0.08, 'consumer_goods_factor': -0.05}, ('economy', 'document')),
    IdeaDef('refined_exports', 'Refined Fuel Abroad', 'Aemurraqi refineries sell finished fuel rather than crude.',
            {'production_speed_industrial_complex_factor': 0.15, 'production_factory_max_efficiency_factor': 0.04}, ('industry', 'economy')),
    IdeaDef('oil_plan', 'The First Oil Plan', 'A published plan for output, reserves and investment.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.08, 'stability_factor': 0.02}, ('command', 'document')),
    IdeaDef('fuel_price_bands', 'Fuel Price Bands', 'A reserve fund smooths domestic fuel prices within published bands.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('scales', 'economy')),
    # merchant routes
    IdeaDef('route_service', 'The Route Security Service', 'Convoy desks, harbour police and escort crews in one service.',
            {'naval_coordination': 0.04, 'navy_org_factor': 0.04}, ('navy', 'logistics')),
    IdeaDef('convoy_escorts', 'Escorts with the Cargo', 'Every convoy sails with at least one armed ship.',
            {'navy_org_factor': 0.06, 'naval_coordination': 0.05}, ('navy', 'security')),
    IdeaDef('approach_patrols', 'Patrols on the Approaches', 'The escorts guard the home approaches and leave the open sea to insurers.',
            {'naval_speed_factor': 0.05, 'naval_coordination': 0.04, 'air_detection': 0.05}, ('navy', 'radar')),
    IdeaDef('insurance_pool', 'The Shipping Insurance Pool', 'A national pool insures the merchant fleet at home.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('scales', 'navy')),
    IdeaDef('flag_standards', 'Standards of the Flag', 'Ships under the national flag meet inspected standards for crews and radios.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.06, 'consumer_goods_factor': -0.02}, ('navy', 'document')),
    # garrisons
    IdeaDef('volunteer_garrisons', 'The Volunteer Garrisons', 'A small volunteer army counted district by district.',
            {'army_core_defence_factor': 0.05}, ('training', 'security')),
    IdeaDef('hill_companies', 'Hill and Jungle Companies', 'Companies that train each season in the hills and jungle.',
            {'army_defence_factor': 0.04, 'attrition': -0.05}, ('training', 'tools')),
    IdeaDef('district_militia', 'District Militias', 'Part-time volunteers who guard depots, bridges and wells at home.',
            {'army_core_defence_factor': 0.10, 'training_time_army_factor': -0.10}, ('security', 'civil')),
    IdeaDef('long_service', 'Long-Service Regulars', 'A small army of career volunteers moved by truck and rail.',
            {'army_org_factor': 0.06, 'experience_gain_army_factor': 0.10}, ('medal', 'training')),
    # air
    IdeaDef('service_wing', 'The Service Fighter Wing', 'Thirty-six fighters with their own staff and maintenance plan.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('interceptor_wing', 'The Interceptor Wing', 'Fighters on alert to deny the sky over the capital.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('patrol_wing', 'The Route Patrol Wing', 'Long-range patrols over sea lanes and frontier roads.',
            {'air_mission_efficiency': 0.06, 'naval_coordination': 0.03}, ('air', 'navy')),
    IdeaDef('contract_instructors', 'Contract Instructors', 'Hired aggressor instructors fly against the wing in training.',
            {'experience_gain_air_factor': 0.12, 'political_power_gain': -0.05}, ('air', 'training')),
    # the Belkan War abroad
    IdeaDef('war_premium', 'The War Premium', 'Wartime oil prices and war-risk insurance reach every cargo.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('open_order_book', 'An Open Order Book', 'Arms and fuel sold to any buyer who pays in cash.',
            {'production_speed_arms_factory_factor': 0.10, 'stability_factor': -0.02}, ('industry', 'diplomacy')),
    IdeaDef('arms_embargo', 'No Arms to Belligerents', 'Fuel and civilian goods flow; weapons contracts stop.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('peace', 'scales')),
    IdeaDef('windfall_fund', 'The Windfall Fund', 'Wartime oil revenue banked against the years of low prices.',
            {'stability_factor': 0.03, 'political_power_factor': 0.05}, ('economy', 'scales')),
    IdeaDef('export_licences', 'Published Arms Licences', 'Every arms export licensed, with buyer and end use published.',
            {'production_speed_arms_factory_factor': 0.12, 'political_power_factor': 0.03}, ('document', 'industry')),
    IdeaDef('neutral_reputation', 'Clean Hands', 'A reputation as a supplier with no enemies.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05}, ('peace', 'diplomacy')),
    IdeaDef('belkan_orders', 'Belkan Purchasing Missions', 'Orders for fuel, aluminium and shipping from a victorious Belka.',
            {'consumer_goods_factor': -0.03, 'industrial_capacity_factory': 0.03}, ('diplomacy', 'economy')),
    # Ulysses
    IdeaDef('sky_watch', 'Watch on the Sky', 'Ministries plan for an impact whose location nobody can name.',
            {'air_detection': 0.05, 'stability_factor': 0.01}, ('telescope', 'meteor')),
    IdeaDef('deep_cisterns', 'Cisterns and Shelters', 'Sealed cisterns and shelters under the capital and district towns.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('warning_net', 'The Warning Net', 'Tracking stations, sirens and a radio chain in every district.',
            {'air_detection': 0.10, 'planning_speed': 0.05}, ('radar', 'meteor')),
    IdeaDef('staple_reserve', 'The Staple Reserve', 'Grain, medicine and fuel stored in the districts.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('logistics', 'civil')),
    IdeaDef('open_drills', 'Public Evacuation Drills', 'Rehearsed in public, with deputies taking part.',
            {'stability_factor': 0.05, 'war_support_factor': 0.03}, ('ballot', 'shelter')),
    IdeaDef('board_grain', 'Board Grain Contracts', 'Emergency stores bought forward and held by the boards.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'logistics')),
    IdeaDef('brigade_stores', 'Brigade-Guarded Stores', 'Movement brigades dig cisterns and keep the shelter rolls.',
            {'war_support_factor': 0.05, 'stability_factor': 0.03}, ('security', 'logistics')),
    IdeaDef('officer_shelters', 'Duty Officers for the Shelters', 'Garrison officers run evacuation tables and shelters.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.03}, ('command', 'shelter')),
    IdeaDef('harbour_reception', 'Reception at the Harbour', 'Ships carrying displaced families may land at the harbour district.',
            {'political_power_gain': 0.08, 'stability_factor': -0.02}, ('refugees', 'navy')),
    # war in Usea
    IdeaDef('war_risk', 'Usean War Risk', 'Insurers price the Usean war into every cargo.',
            {'consumer_goods_factor': 0.03, 'industrial_capacity_factory': 0.03}, ('navy', 'economy')),
    IdeaDef('isaf_contracts', 'ISAF Supply Contracts', 'Fuel and steel sold to the ISAF quartermasters; no troops committed.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.01}, ('diplomacy', 'logistics')),
    IdeaDef('neutral_flag', 'A Flag Both Navies Respect', 'Nothing loaded in Aemurraq may reach either army.',
            {'stability_factor': 0.04, 'naval_coordination': 0.03}, ('peace', 'navy')),
    IdeaDef('cash_cargoes', 'Cash Cargoes', 'Civilian buyers in any port, paid in advance, no questions asked.',
            {'industrial_capacity_factory': 0.06, 'stability_factor': -0.03}, ('economy', 'navy')),
    IdeaDef('war_freight', 'War Freight Charters', 'Export houses charter every spare hull at wartime rates.',
            {'industrial_capacity_factory': 0.04, 'naval_coordination': 0.02}, ('logistics', 'economy')),
    IdeaDef('refinery_overtime', 'Refineries on Overtime', 'Three shifts at every refinery while the war lasts.',
            {'production_factory_efficiency_gain_factor': 0.05}, ('industry', 'tools')),
    IdeaDef('state_quota', 'Wartime Oil Quotas', 'The oil office allocates home, reserve and foreign shares.',
            {'political_power_gain': 0.08, 'stability_factor': 0.01}, ('command', 'economy')),
    IdeaDef('reconstruction_orders', 'Reconstruction Orders', 'Steel and fuel for rebuilding the Usean coast, on long credit.',
            {'production_speed_industrial_complex_factor': 0.08, 'consumer_goods_factor': -0.02}, ('rebuild', 'diplomacy')),
    IdeaDef('cautious_trade', 'Terms with Erusea', 'Cargoes reach Usea on terms set by a victorious Erusea.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.02}, ('diplomacy', 'scales')),
    # decisions
    IdeaDef('escorted_season', 'An Escorted Season', 'The route service escorts the busiest months of the export year.',
            {'naval_coordination': 0.05, 'consumer_goods_factor': -0.02}, ('navy', 'logistics')),
    IdeaDef('fuel_release', 'Reserve Fuel Released', 'Reserve fuel sold at band prices to calm a spike.',
            {'stability_factor': 0.04}, ('logistics', 'scales')),
    IdeaDef('inspected_ministries', 'Ministries Under Inspection', 'Unannounced inspections keep officials honest and nervous.',
            {'political_power_factor': 0.08, 'stability_factor': -0.02}, ('document', 'command')),
    IdeaDef('market_days', 'Market Days at the Crossings', 'Traders from both sides of the line meet at the frontier posts.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'peace')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('constituent_cabinet', 'Cabinet of the Constituent Assembly',
           'A cabinet chosen by and answerable to an elected constituent assembly, governing collectively while elections '
           'return to a fixed calendar. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('board_council', 'Council of the Export Boards',
           'A standing council of the chairmen of the oil, steel, aluminium and shipping boards, holding the government seals '
           'with elections still suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('resolve_directorate', 'Directorate of National Resolve',
           'A directorate drawn from the nationalist movement, ruling by decree with movement officials beside every district '
           'governor. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
    Office('route_command', 'Route Security Command Council',
           'A council of senior officers from the route security services, the frontier garrisons and the air wing, holding '
           'power for a declared transition. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('caretaker_question', 'A Mandate Nobody Voted For', (
        "The National Administration meets in the capital centre with an agenda its members have postponed for years. The "
        "emergency orders that suspended elections are due for renewal, and for the first time the ministry lawyers will not "
        "countersign them without a recorded cabinet vote. Aemurraq is governed by an office that sits under a democratic "
        "banner while the democratic camp itself barely registers in any count of public opinion.",
        "Outside, the country has split almost exactly in two. Half answers to a nationalist movement that fills the squares "
        "and promises discipline, pride and an end to government by clerks. The other half belongs to a non-aligned "
        "establishment of export boards, senior officials and district notables who care more about stable prices than about "
        "any creed. Neither half trusts the Administration, and neither has yet found a lawful way to replace it.",
        "The ministers cannot settle the country's future at one sitting. They can decide how the argument will be "
        "conducted: in public, with the press in the gallery and the movement's speakers given airtime on the state radio, "
        "or inside the ministries, where the export boards already keep their chairs. Whatever they choose will be read as a "
        "signal by both halves of the country, and by every foreign buyer of Aemurraqi oil.",
    ), (
        Option('Argue it in public, on the radio.', (Stability(0.02), WarSupport(0.02), PP(-15))),
        Option('Keep it inside the ministries.', (PP(40), Stability(-0.02))),
        Option('Invite the boards and the movement to talks.', (PP(15), Stability(0.01))),
    ), picture=1),
    EventDef('district_ledgers', 'Five Districts Report', (
        "The census teams return from the five districts with trucks full of ledgers and a list of grievances longer than "
        "the ledgers. The Capital District holds most of the civilian plants, the only air base and the fuel silo, and "
        "complains that it pays most of the taxes. District E, with its arms and civilian plants, calls its single road a "
        "scandal. District B points to the logistics centre and asks why its hill roads were laid out for mules.",
        "The harbour district on the coast has the naval base and the yards and wants a road that does not flood every "
        "winter. District D is the strangest return of all: the largest district by far, twenty-seven provinces of desert, "
        "hill, jungle and plain with a long coastline, and no paved road, no plant and no resource the old surveys ever "
        "recorded. Its delegates arrived late because there was no way to arrive early.",
        "The ministers must decide how to present the census. Printed in full, it will start a long quarrel about fairness "
        "among the five districts that no ministry can steer. Held inside the ministries, it will quietly shape the budget "
        "while every district assumes the worst about the others. Either way, the figures for District D will decide the "
        "road budget for the rest of the decade.",
    ), (
        Option('Print every district figure.', (Stability(0.03), PP(-20))),
        Option('Brief only the ministries.', (PP(35), Stability(-0.01))),
    ), picture=0),
    EventDef('fuel_audit', 'What the Wells Really Pump', (
        "The inspectors sent to every well, pipeline and depot have finished, and their figures do not match anyone's. "
        "Output from District B, District E and the Capital District is higher than the export boards reported and lower "
        "than the ministries assumed. Several pipelines carry no meters at all. The fuel silo in the capital, which the "
        "army counts on for its trucks and fighters, is less than half full on most days of the year.",
        "Everyone has an explanation. The boards blame old equipment and honest rounding. The ministries blame the boards. "
        "Plant managers in District E say they have been buying fuel back from exporters at foreign prices because the "
        "domestic allocation never arrived. The movement's newspapers print the gap between the two sets of figures on "
        "their front pages and invite readers to guess where the difference went.",
        "The government now holds the only honest account of the country's oil, and must decide what to do with it. It "
        "can use the audit to reopen every export licence, which will take years and enrage the boards, or let the boards "
        "correct their own books in exchange for a quiet settlement. The figures will not stay secret either way.",
    ), (
        Option('Reopen every export licence.', (PP(-20), Research('industry', 0.5, 1))),
        Option('Let the boards correct their books.', (PP(30), Stability(-0.01))),
    ), picture=0),
    EventDef('missing_tanker', 'A Tanker Overdue', (
        "A tanker loaded at the harbour district misses its reporting call two days out. The convoy desk at the trade "
        "ministry assumes the navy is handling it; the navy assumes the harbour police have heard from the owners; the "
        "harbour police assume the ship has simply switched off its radio to save power. For two days nobody looks. Then "
        "the owners telephone the capital and ask, politely, whether anyone knows where their ship is.",
        "The tanker turns up drifting with engine failure, its crew safe and its cargo intact. The search that found it "
        "was organised by merchant masters on the radio rather than by any office of the state. Foreign underwriters raise "
        "their premiums on Aemurraqi cargoes the following week, and the masters' association writes an open letter "
        "asking which of the three offices is responsible for them at sea.",
        "The new route security service is supposed to answer that question, and this is its first test. The government "
        "can publish a full inquiry naming every failure, which will embarrass three ministries at once, or settle quietly "
        "with the owners and the underwriters. The masters will judge the new service by the choice, and they talk to "
        "every crew in the fleet.",
    ), (
        Option('Publish the inquiry and its failures.', (Stability(-0.01), XP('navy', 15))),
        Option('Settle quietly with the owners.', (PP(25),)),
    ), picture=2),
    EventDef('muster_day', 'Muster Day in Five Districts', (
        "For the first time in years, every volunteer on the army rolls is called to report on a single day. In the "
        "Capital District the barracks overflow and the trucks run out of seats. In District B the hill companies arrive "
        "early, in good order and short of boots. In District D, where the rolls list hundreds of names, a few dozen men "
        "walk in from the interior and ask where everyone else is.",
        "By evening the figures are clear and uncomfortable. The four formations exist, but two of them are far below "
        "strength, and the stocks of rifles, trucks and support equipment would not outfit even the men who did report. "
        "Officers who had signed paper returns for years avoid each other in the mess. The quartermasters, who always "
        "knew, are quietly pleased that someone has finally asked them.",
        "The general staff must report to the government, and the government must decide what the public hears. Publishing "
        "the real strength will shake confidence and invite the movement's newspapers to ask who was paid for soldiers who "
        "never existed. Reporting the paper strength keeps calm for now and leaves the army as hollow as it was this "
        "morning.",
    ), (
        Option('Publish the true strength.', (Stability(-0.02), XP('army', 20))),
        Option('Report the paper strength.', (PP(20), WarSupport(0.02))),
    ), picture=1),
    EventDef('belkan_war', 'Prices of a Distant War', (
        "In March 1995 war breaks out around Belka. Aemurraq is no party to it and its frontiers are nowhere near the "
        "fighting, yet within days the war is present in every ministry. Oil prices jump on the foreign exchanges. "
        "Underwriters add war-risk premiums to routes near the fighting and to any ship whose cargo might be resold. "
        "Buyers the export boards have never met begin calling with large orders and few questions.",
        "The arms plants in District E and the capital see overtime for the first time in years. The movement's speakers "
        "say the country should take every order it can get, since the belligerents will not thank anyone for staying "
        "poor. The establishment worries about foreign memories and about ships being stopped at sea. Several embassies "
        "ask, in identical language, what Aemurraq intends to sell and to whom.",
        "The government must answer before the boards answer for it. It can declare at once that Aemurraq takes no side, "
        "which costs nothing today and may cost orders tomorrow, or say only that existing contracts will be honoured, "
        "which keeps every option open and satisfies nobody abroad. Either statement will be read in capitals that "
        "Aemurraq's ministers have rarely visited.",
    ), (
        Option('Declare that Aemurraq takes no side.', (Stability(0.02), PP(10))),
        Option('Say only that contracts will be honoured.', (PP(30), WarSupport(0.02))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Aemurraqi response is gameplay', picture=1),
    EventDef('ulysses_announced', 'The Asteroid Will Strike', (
        "Astronomers warned in December 1994 that the asteroid Ulysses might pass close enough to strike the Earth. In "
        "April 1996 the warning becomes an announcement: it will strike, and nations must prepare. Nobody can yet say where "
        "the fragments will fall. Aemurraq has a crowded capital, towns that depend on a few wells, a merchant fleet spread "
        "across distant routes and no experience of planning for anything this large.",
        "Every ministry discovers a plan that needs money. Engineers want shelters and sealed cisterns under the towns. "
        "Radar and observatory specialists want a warning net that can clear a district in hours. The export boards want "
        "to know whether their ships should stay in port. The treasury points out that any of these plans costs as much as "
        "a decade of road building, and that the roads are not finished.",
        "The public reaction arrives before any plan does. Markets in the capital sell out of water containers, places of "
        "worship fill and some families in the harbour district talk of moving inland. The government must decide how to "
        "speak about a danger it cannot control: openly and at once, accepting a rush on the markets, or calmly and slowly, "
        "accepting that preparation will lag.",
    ), (
        Option('Prepare openly and at once.', (WarSupport(0.02), Stability(-0.02), Event('market_run', 20))),
        Option('Urge calm and keep working.', (Stability(0.03),)),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Aemurraqi preparations are gameplay',
        picture=2),
    EventDef('market_run', 'Queues at the Grain Markets', (
        "Three weeks after the government began preparing in public, the markets break. Grain, flour, water containers "
        "and fuel cans sell out in the capital by noon each day, and prices for staples double within a fortnight. District "
        "towns at the end of long roads run out entirely. Traders who can afford to wait hold back stock, and everyone "
        "knows who they are.",
        "The movement blames exporters for shipping grain money abroad. The export boards blame the ministries for frightening "
        "the public. Crews from foreign ships in the harbour district buy whatever is left and sail away with it. The "
        "district councils, where they exist, send telegrams to the capital that grow shorter and angrier as the week goes "
        "on.",
        "The cabinet has two tools and little time. It can fix the price of staples and ration them by household, which "
        "needs clerks, inspectors and patience the country has not shown before. Or it can let prices run, import as fast "
        "as the ships can carry, and trust that high prices will draw new supply into the country before tempers break in the "
        "queues outside the market halls.",
    ), (
        Option('Fix staple prices and ration.', (Stability(0.03), PP(-25))),
        Option('Let prices run and import more.', (Stability(-0.02), PP(15))),
    ), picture=0),
    EventDef('roche_night', 'The Night Ulysses Passed', (
        "On 8 July 1999 the asteroid Ulysses passes through the Roche limit of the Earth. In Aemurraq the night is spent "
        "listening. Families gather around radios in the capital and the district towns, the warning chain reports every "
        "hour whether or not there is anything to report and the shelters, where they exist, hold more people than their "
        "designers ever imagined.",
        "Merchant masters on distant routes report by radio what they can see and hear from their bridges, which is mostly "
        "rumour relayed from other ships. The route service logs every call. Officials in the capital try to separate what "
        "is known from what is feared, and find that the line moves every few minutes. Nobody in the government sleeps, and "
        "nobody pretends to.",
        "By morning the country is still standing and still frightened. Whatever has fallen, and wherever it has fallen, the "
        "markets, the sea lanes and the insurers will carry the consequences to Aemurraq for years. The government must "
        "decide whether to keep its emergency measures in force while the world takes stock, or to stand the districts "
        "down and let ordinary life resume.",
    ), (
        Option('Keep the emergency measures in force.', (WarSupport(0.03), Stability(-0.01))),
        Option('Stand the districts down.', (Stability(0.03), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no Aemurraqi damage is claimed', picture=2),
    EventDef('usean_war', 'War Comes to Usea', (
        "In the summer of 2003 Erusea invades the neutral country of San Salvacion, seizes Stonehenge and begins using its "
        "railguns as anti-air batteries. Usea is far from Aemurraq's districts, but Usean ports buy Aemurraqi steel and "
        "Usean lanes carry Aemurraqi oil. By the time the ministers meet, insurers have already suspended cover on several "
        "routes and doubled it on the rest.",
        "Masters of the merchant fleet refuse Usean charters until someone tells them who will pay if their ships are lost. "
        "Buyers on both sides of the war call the export boards with orders larger than anything since the Belkan War, "
        "and the boards forward the calls to the cabinet without comment. The movement and the establishment, for once, "
        "agree on something: the country should not send soldiers. They agree on nothing else.",
        "The government must set Aemurraq's posture before every ship in the fleet sets its own. Keeping all cargoes away "
        "from Usean waters is safe and expensive. Sailing wherever the contracts lead is profitable and dangerous. Every "
        "later choice about whom to supply will follow from what the ministers say this week.",
    ), (
        Option('Keep every cargo away from Usean waters.', (Stability(0.02), PP(-10))),
        Option('Sail where the contracts are.', (PP(30), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Aemurraqi response is gameplay', picture=1),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('admin', 'The Caretaker Administration', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_no_party', 'A Government Without a Party',
          "Aemurraq enters 1991 governed by the National Administration, a body of ministers and senior officials that sits "
          "under a democratic banner yet commands about one voter in a hundred. Elections are suspended, and the public "
          "divides almost evenly between a nationalist movement and a non-aligned establishment. Naming that problem openly "
          "costs the ministers their quiet, but every later reform starts here.",
          ('assembly', 'document'), reward=(Idea('caretaker_mandate'), Event('caretaker_question'))),
    Focus('adm_mandate_audit', 'Audit the Emergency Orders',
          "Lawyers from the ministries read every order that keeps the elections suspended: the original emergency acts, the "
          "extensions, the clauses nobody has tested in court. Their study shows the mandate rests on habit more than law. "
          "Publishing that finding makes the Administration look weaker for a season, and it forces each faction to say "
          "what it would put in the mandate's place.",
          ('document', 'scales'), after=('adm_no_party',),
          reward=(PP(35), Tooltip('Opens the four answers to the caretaker question; only one can be taken.'))),
    Focus('adm_constituent_path', 'Call a Constituent Assembly',
          "The reform wing of the Administration proposes an elected assembly with a single task: to write the constitution "
          "that the suspended elections were supposed to serve. The democratic camp is tiny, so the seats would fill with "
          "nationalists and the non-aligned establishment. Ministers accept that risk, because a mandate written by voters "
          "is the only one the street cannot simply dismiss.",
          ('ballot', 'assembly'), after=('adm_mandate_audit',),
          exclusive=('adm_boards_path', 'adm_resolve_path', 'adm_command_path'),
          reward=(SwapIdea('caretaker_mandate', 'constituent_promise'),)),
    Focus('adm_boards_path', 'Seat the Export Boards',
          "Aemurraq lives on oil, steel and aluminium sold abroad, and the chartered boards that handle those exports already "
          "employ more clerks than several ministries. Their chairmen propose to govern through a council of boards, judging "
          "each policy by whether it keeps cargoes moving. The establishment likes the idea. The nationalist half of the "
          "country sees a cartel walking into the state.",
          ('economy', 'assembly'), after=('adm_mandate_audit',),
          exclusive=('adm_constituent_path', 'adm_resolve_path', 'adm_command_path'),
          reward=(SwapIdea('caretaker_mandate', 'board_charters'),)),
    Focus('adm_resolve_path', 'The Movement Claims the State',
          "Half the public follows the nationalist movement, which calls the Administration a committee of clerks guarding "
          "exporters' profits. Its leaders offer to end the suspension of politics by ending politics as a contest: one "
          "movement, one programme, every district disciplined from the capital. Their rallies fill the squares quickly, and "
          "their opponents fill the boards' offices just as fast.",
          ('security', 'ballot'), after=('adm_mandate_audit',),
          exclusive=('adm_constituent_path', 'adm_boards_path', 'adm_command_path'),
          reward=(SwapIdea('caretaker_mandate', 'movement_squares'),)),
    Focus('adm_command_path', 'The Route Officers Step In',
          "Officers of the services that guard the convoys, pipelines and frontier roads argue that only they stand outside "
          "both camps. They propose a command council to hold the state until the factions calm down, with the ministries "
          "kept on as staff. It promises order without a winner, and it leaves a country run by people trained to secure "
          "routes rather than to persuade voters.",
          ('command', 'security'), after=('adm_mandate_audit',),
          exclusive=('adm_constituent_path', 'adm_boards_path', 'adm_resolve_path'),
          reward=(SwapIdea('caretaker_mandate', 'route_officers'),)),
    Focus('adm_constituent_cabinet', 'Seat the Constituent Cabinet',
          "The assembly is elected, sits in the capital and chooses a cabinet answerable to it, while elections return to a "
          "fixed calendar. Government passes from a single office to a body of ministers who can be voted out. Nationalist "
          "deputies hold many seats and use them loudly; the cabinet must bargain for every budget, yet it carries a mandate "
          "no earlier government could claim.",
          ('ballot', 'document'), after=('adm_constituent_path',), cost=10,
          exclusive=('adm_board_council', 'adm_resolve_directorate', 'adm_route_command'),
          reward=(Regime('constituent_cabinet'), Flag('path_constituent'))),
    Focus('adm_board_council', 'Convene the Council of Boards',
          "Chairmen of the oil, steel, aluminium and shipping boards form a standing council and take the government seals. "
          "Elections stay suspended, and ministries report to the council as if they were export departments. Contracts are "
          "signed faster than ever and the budget balances. Voters, who were never consulted, notice that the council answers "
          "mainly to its own ledgers.",
          ('economy', 'command'), after=('adm_boards_path',), cost=10,
          exclusive=('adm_constituent_cabinet', 'adm_resolve_directorate', 'adm_route_command'),
          reward=(Regime('board_council'), Flag('path_boards'))),
    Focus('adm_resolve_directorate', 'Install the Resolve Directorate',
          "A directorate drawn from the nationalist movement takes executive power and rules by decree. Opposition offices "
          "close, the district councils are dissolved and a movement official sits beside every governor. Public order "
          "improves in the first months and recruiting offices fill. Exporters and foreign buyers grow cautious, because a "
          "government that answers to rallies can change its mind overnight.",
          ('security', 'command'), after=('adm_resolve_path',), cost=10,
          exclusive=('adm_constituent_cabinet', 'adm_board_council', 'adm_route_command'),
          reward=(Regime('resolve_directorate'), Flag('path_resolve'))),
    Focus('adm_route_command', 'Form the Route Command Council',
          "Senior officers from the route security services, the frontier garrisons and the air wing assume power for a "
          "declared transition. Parties are not banned, but they are not consulted either. Convoys sail on schedule and the "
          "frontier roads stay open. The council has no plan for handing power back, and every faction knows that a "
          "transition without a date rarely ends on its own.",
          ('command', 'medal'), after=('adm_command_path',), cost=10,
          exclusive=('adm_constituent_cabinet', 'adm_board_council', 'adm_resolve_directorate'),
          reward=(Regime('route_command'), Flag('path_command'))),
    Focus('adm_constituent_text', 'Ratify the Written Constitution',
          "The assembly finishes a written constitution after two years of drafting: an elected chamber, a cabinet answerable "
          "to it, district councils with their own budgets and a court to settle quarrels among them. Ratification costs a "
          "hard season of bargaining with nationalist deputies, who extract a strong speakership. The text is imperfect, but "
          "it is the first one Aemurraq has voted for.",
          ('scales', 'document'), after=('adm_constituent_cabinet',),
          exclusive=('adm_board_ledgers', 'adm_resolve_brigades', 'adm_command_timetable'),
          reward=(SwapIdea('constituent_promise', 'written_constitution'),)),
    Focus('adm_board_ledgers', 'Publish the Board Ledgers',
          "Facing complaints that the council governs for its own members, the boards publish annual ledgers showing every "
          "contract, price and royalty they handle. The disclosure embarrasses several chairmen and loses the council some "
          "private deals. It also gives the public a reason to believe that export revenue reaches the treasury, which is "
          "the only argument a government of boards can make.",
          ('scales', 'economy'), after=('adm_board_council',),
          exclusive=('adm_constituent_text', 'adm_resolve_brigades', 'adm_command_timetable'),
          reward=(SwapIdea('board_charters', 'open_ledgers'),)),
    Focus('adm_resolve_brigades', 'Movement Brigades in the Districts',
          "The directorate organises the movement's younger members into brigades that repair roads, guard depots and parade "
          "on national days in every district. They bring energy and cheap labour to places the ministries never reached. "
          "They also watch their neighbours and report on them, and the export boards quietly move their best clerks abroad "
          "rather than work under brigade supervisors.",
          ('civil', 'security'), after=('adm_resolve_directorate',),
          exclusive=('adm_constituent_text', 'adm_board_ledgers', 'adm_command_timetable'),
          reward=(SwapIdea('movement_squares', 'movement_brigades'),)),
    Focus('adm_command_timetable', 'A Timetable for the Transition',
          "Pressed by exporters and foreign buyers, the command council publishes the conditions under which it would hand "
          "power to civilians: stable prices, secure routes and a census of voters. Nobody believes the dates, but the "
          "conditions become a public yardstick. The officers gain patience from the street and lose the freedom to rule "
          "without ever explaining themselves.",
          ('command', 'document'), after=('adm_route_command',),
          exclusive=('adm_constituent_text', 'adm_board_ledgers', 'adm_resolve_brigades'),
          reward=(SwapIdea('route_officers', 'transition_timetable'),)),
    Focus('adm_settled', 'The Caretaker Years End',
          "Whichever answer the country chose, the arguments of the early nineties give way to routine. Ministries know whom "
          "they serve, the districts know whom to petition and the export boards know whom to lobby or obey. A settled order "
          "is not necessarily a popular one. It is, at least, one that foreign buyers and neighbours can predict, and that "
          "alone lowers the price of everything.",
          ('peace', 'assembly'),
          after_any=('adm_constituent_text', 'adm_board_ledgers', 'adm_resolve_brigades', 'adm_command_timetable'),
          reward=(Flag('order_settled'), Stability(0.04))),
))

DISTRICTS = Branch('districts', 'Five Districts, One Capital', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dist_census', 'Census of the Five Districts',
          "Aemurraq is five districts: the Capital District, the harbour district on the coast, the hill and jungle country of "
          "District B with its logistics centre, the plant towns of District E and the vast, roadless District D. Nobody in "
          "the capital has counted their wells, schools or tax rolls properly. A census takes a full season and ends most "
          "arguments about who is owed what.",
          ('document', 'civil'), reward=(Idea('district_compact'), Event('district_ledgers'))),
    Focus('dist_capital_roads', 'Ring Roads Around the Capital',
          "The Capital District holds most of the civilian plants, the only air base and the fuel silo, yet its roads are "
          "those of a small desert town. Widening the ring roads around the capital centre lets trucks reach the plants "
          "without crossing the markets. The works close the main streets for a year, and merchants complain every single "
          "day the barriers stay up.",
          ('logistics', 'civil'), after=('dist_census',), reward=(Build('infrastructure', 1, 0),)),
    Focus('dist_logistics_centre', 'The Logistics Centre on Three Shifts',
          "District B's logistics centre supplies half the country, but the roads that feed it climb through hills and jungle "
          "on routes graded for pack animals. Paving the climbs and adding passing bays lets the centre run three shifts. "
          "The district gains jobs and the army gains a dependable depot, though jungle maintenance will eat a slice of every "
          "future works budget.",
          ('logistics', 'rail'), after=('dist_census',), reward=(Build('infrastructure', 1, 433),)),
    Focus('dist_district_e', 'A Second Road for District E',
          "District E has two civilian plants, two arms plants and the steel and oil to feed them, but its towns sit at the end "
          "of a single road. Plant managers want a second route so that one washout cannot halt production for a week. The "
          "district's notables want housing first. The ministry pays for the road and promises the housing later, as "
          "ministries do.",
          ('industry', 'bridge'), after=('dist_census',), reward=(Build('infrastructure', 1, 502),)),
    Focus('dist_interior_trunk', 'A Trunk Road into District D',
          "District D is the largest district by far, twenty-seven provinces of desert, hill, jungle and plain, and it has no "
          "developed roads at all. A trunk road from the capital into the interior is the most expensive single project the "
          "ministries have ever attempted. It will take two years, swallow the road budget and decide whether the interior "
          "ever joins the rest of the country.",
          ('logistics', 'tools'), after=('dist_census',), cost=10, reward=(Build('infrastructure', 2, 468),)),
    Focus('dist_councils', 'A Council for Each District',
          "Each district receives an elected council with its own budget line, its own works office and a governor answerable "
          "to the council rather than to the capital. Local projects move faster, and District D finally has a body that "
          "speaks for it. The capital loses the ability to shift money between districts freely, and every budget becomes a "
          "negotiation among five.",
          ('ballot', 'civil'), after_any=('dist_capital_roads', 'dist_logistics_centre', 'dist_district_e'), cost=10,
          exclusive=('dist_prefects',),
          reward=(SwapIdea('district_compact', 'district_councils'), Flag('districts_devolved'))),
    Focus('dist_prefects', 'Prefects from the Capital',
          "The opposite answer sends prefects from the capital to run every district on one code, one tax rate and one "
          "calendar of works. Decisions get faster, and money moves to wherever the ministries judge it is needed, usually "
          "the interior. District notables lose their old influence, and they will remember who took it the first time a "
          "prefect makes an expensive mistake.",
          ('command', 'logistics'), after_any=('dist_capital_roads', 'dist_logistics_centre', 'dist_district_e'), cost=10,
          exclusive=('dist_councils',),
          reward=(SwapIdea('district_compact', 'capital_prefects'), Flag('districts_central'))),
    Focus('dist_interior_workshops', 'Workshops for the Interior',
          "With the trunk road open, the ministries place a workshop town in District D to repair trucks, pumps and "
          "generators for the interior. It is a small plant by the standards of District E, but it is the first in a district "
          "that has never had one. Skilled workers must be persuaded to move inland, and their housing costs more than the "
          "machines.",
          ('tools', 'industry'), after=('dist_interior_trunk',), reward=(Build('industrial_complex', 1, 468),)),
    Focus('dist_d_wells', 'Wells Along the Trunk Road',
          "Settlers, drivers and road crews follow the trunk road inland, and they need water before anything else. Boring "
          "wells at regular stages along the route turns a line on the map into a string of halts with fuel, water and a "
          "telephone. Without wells nobody stays. With them, the interior begins to fill, slowly and unevenly, along the "
          "road.",
          ('civil', 'tools'), after=('dist_interior_trunk',), reward=(Build('infrastructure', 1, 468),)),
    Focus('dist_interior_council', 'The Interior Speaks for Itself',
          "The new District D council meets for the first time in a schoolhouse on the trunk road, with delegates who "
          "travelled two days to attend. Its first demand is that the interior keep a share of any oil or minerals found "
          "beneath it. Granting that costs the treasury future revenue, but it ties the interior's notables to the national "
          "order rather than against it.",
          ('assembly', 'civil'), after_any=('dist_interior_workshops', 'dist_d_wells'), requires=(HasFlag('districts_devolved'),),
          reward=(Idea('interior_council'),)),
    Focus('dist_interior_survey', 'Prefect Survey of the Interior',
          "Prefects drive the trunk road to its end and then continue by truck and on foot to map every settlement in "
          "District D. Their survey sets road priorities by population and freight rather than by which notable shouts "
          "loudest. It is efficient and resented in equal measure. The ministries gain a plan for the interior that nobody "
          "there was asked to approve.",
          ('document', 'logistics'), after_any=('dist_interior_workshops', 'dist_d_wells'), requires=(HasFlag('districts_central'),),
          reward=(Build('infrastructure', 1, 468), PP(20))),
    Focus('dist_accord', 'The Accord of Five Districts',
          "Whichever arrangement the country chose, the five districts sign a short accord fixing their revenue shares, the "
          "order of road works for the decade and the right of each district to appeal to a common court. It is a dry "
          "document and it ends years of petitions. Later governments can plan without reopening the question of who pays "
          "for whom.",
          ('scales', 'assembly'), after_any=('dist_interior_council', 'dist_interior_survey'),
          reward=(Flag('districts_settled'), Stability(0.03))),
))

OIL = Branch('oil', 'Oil, Steel and Aluminium', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('oil_fuel_ledger', 'The National Fuel Ledger',
          "Oil from District B, District E and the Capital District feeds a single fuel silo and a civilian economy that burns "
          "more than anyone measures. The ministries keep no common account of who pumps, who refines and who exports. A "
          "national ledger costs a year of inspectors' visits to every well and depot, and it shows the export boards exactly "
          "how much they have been undercounting.",
          ('document', 'industry'), reward=(Idea('fuel_ledger'), Event('fuel_audit'))),
    Focus('oil_ore_survey', 'Count the Steel and Bauxite',
          "Steel ore and bauxite come out of the same three districts as the oil, often from pits opened decades ago and never "
          "surveyed properly. Geologists from the capital map the seams, the water tables and the haul roads. The survey "
          "costs little in money but takes the best engineers away from production for a season, and it settles which pits "
          "deserve investment.",
          ('telescope', 'tools'), after=('oil_fuel_ledger',), reward=(Research('excavation_tech', 0.5, 1),)),
    Focus('oil_smelter', 'Rebuild the Smelter Line',
          "Bauxite from the hill pits and power from the oil fields make aluminium the natural third export, but the old "
          "smelter line runs at half capacity on worn equipment. Rebuilding it with modern cells doubles output and supplies "
          "workshops at home. The power bill rises sharply, and each summer the ministry must decide whether cheap power goes "
          "to the smelter or the towns.",
          ('industry', 'rebuild'), after=('oil_ore_survey',),
          reward=(Research('industry', 0.5, 1), Flag('smelter_running'))),
    Focus('oil_export_houses', 'Chartered Export Houses',
          "One school holds that Aemurraq should do what it already does well: sell crude, steel and aluminium abroad through "
          "chartered houses with long contracts and guaranteed tonnage. The houses bring foreign currency quickly and ask "
          "little of the treasury. Their critics answer that a country selling raw materials stays poor, and that one bad "
          "price year would empty the budget.",
          ('economy', 'logistics'), after=('oil_fuel_ledger',), cost=10,
          exclusive=('oil_refine_home', 'oil_state_office'),
          reward=(SwapIdea('fuel_ledger', 'export_houses'), Flag('model_export'))),
    Focus('oil_refine_home', 'Refine It at Home',
          "Engineers and the plant managers of District E argue for keeping the crude at home and selling fuel, rolled steel "
          "and finished aluminium instead. That means new refineries, smelters and years of protected prices before the plants "
          "pay for themselves. Exporters lose volume in the meantime. If it works, Aemurraq sells finished goods rather than "
          "holes in the ground.",
          ('industry', 'tools'), after=('oil_fuel_ledger',), cost=10,
          exclusive=('oil_export_houses', 'oil_state_office'),
          reward=(SwapIdea('fuel_ledger', 'home_refining'), Flag('model_refining'))),
    Focus('oil_state_office', 'The State Oil Office',
          "A third proposal puts every well, pipeline and export licence under a single state office that sets output, prices "
          "and investment by plan. Revenue flows straight to the treasury and the boards lose their private deals. The office "
          "would be slow, and its directors would answer to whichever government held the capital, for better or for worse.",
          ('command', 'industry'), after=('oil_fuel_ledger',), cost=10,
          exclusive=('oil_export_houses', 'oil_refine_home'),
          reward=(SwapIdea('fuel_ledger', 'state_oil_office'), Flag('model_state'))),
    Focus('oil_terminal_works', 'Terminal Works at the Harbour',
          "The export houses pay for a bulk terminal in the harbour district, with storage tanks, ore sheds and a works yard "
          "that services the loading cranes and pipelines. It is the first industrial site on that coast beyond the naval "
          "yards. The houses insist on long berthing rights in return, which the navy grants with visible reluctance.",
          ('logistics', 'navy'), after=('oil_export_houses',), reward=(Build('industrial_complex', 1, 160),)),
    Focus('oil_refinery', 'A Refinery for District D',
          "The refining school wins a site in District D, on open ground close enough to the oil districts for pipelines and "
          "far enough from the capital to spread the jobs. Construction runs late and over budget, as refineries always do. "
          "Once running, it turns crude that used to leave by tanker into fuel for Aemurraq's own trucks, ships and aircraft.",
          ('industry', 'logistics'), after=('oil_refine_home',), reward=(Build('industrial_complex', 1, 468),)),
    Focus('oil_state_pipeline', 'A State Pipeline to the Silo',
          "The state oil office lays a pipeline and a chain of depots from the oil districts to the capital, so that the silo "
          "never again depends on trucks queuing at the wells. It is plain engineering and plain politics: whoever controls "
          "the valves controls the capital's fuel. The office makes sure the valves answer to it alone.",
          ('command', 'logistics'), after=('oil_state_office',),
          reward=(Build('infrastructure', 1, 0), Research('logistics_tech', 0.5, 1))),
    Focus('oil_long_contracts', 'Twenty-Year Supply Contracts',
          "With the terminal working, the export houses sign supply contracts that run for twenty years, with tonnage, price "
          "formulas and penalties fixed in advance. Foreign buyers gain certainty and Aemurraq gains steady currency. The "
          "price formulas look generous in a bad year and painful in a good one, and every later government inherits them.",
          ('document', 'economy'), after=('oil_terminal_works',), reward=(SwapIdea('export_houses', 'export_contracts'),)),
    Focus('oil_refined_exports', 'Refined Fuel for Export',
          "The District D refinery produces more than the country can burn, and the surplus goes abroad as finished fuel at "
          "several times the price of crude. Export houses that once sold barrels now sell tanker loads of diesel and aviation "
          "fuel. Protected prices at home can begin to fall. Foreign refiners who lost a supplier complain, and they buy anyway.",
          ('economy', 'industry'), after=('oil_refinery',), reward=(SwapIdea('home_refining', 'refined_exports'),)),
    Focus('oil_first_plan', 'Publish the First Oil Plan',
          "The state oil office publishes its first plan: output targets by district, a reserve held in the silo, investment "
          "by year and the share of revenue that goes to the treasury. Private traders dismiss it as wishful arithmetic. The "
          "plan's real value is that it exists in public, so the office can be judged against its own numbers.",
          ('document', 'command'), after=('oil_state_pipeline',), reward=(SwapIdea('state_oil_office', 'oil_plan'),)),
    Focus('oil_price_bands', 'Price Bands for Fuel at Home',
          "Domestic fuel prices swing with every foreign crisis, and each swing reaches bread and bus fares within a week. "
          "Price bands let the ministry absorb small shocks from a reserve fund and pass large ones on gradually. The system "
          "costs money in calm years and political courage in bad ones, when the bands must be widened and everyone notices.",
          ('scales', 'economy'), after_any=('oil_long_contracts', 'oil_refined_exports', 'oil_first_plan'),
          reward=(Idea('fuel_price_bands'),)),
))

SEA = Branch('sea', 'Merchant Route Security', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('sea_route_service', 'The Route Security Service',
          "Sixty merchant ships fly Aemurraq's flag, carrying oil, steel and aluminium to foreign buyers, while the navy owns "
          "two coastal escorts. The convoy desks, harbour police and escort crews belong to three different ministries. "
          "Merging them into a single route security service gives every cargo one office to call. The ministries lose staff "
          "and budget, and say so loudly.",
          ('navy', 'logistics'), reward=(Idea('route_service'), Event('missing_tanker'))),
    Focus('sea_third_slip', 'A Third Slip at the Naval Yard',
          "The naval yard in the harbour district can build two hulls at a time and repair little else. A third slip, with "
          "cranes heavy enough for tankers, lets the yard maintain the merchant fleet without sending ships abroad for every "
          "overhaul. It takes the last good waterfront in the district, and the export houses grumble that their own plans "
          "have just lost a berth.",
          ('navy', 'tools'), after=('sea_route_service',), reward=(Build('dockyard', 1, 160),)),
    Focus('sea_coast_road', 'The Coast Road to the Yards',
          "The harbour district reaches the capital by a road that floods in winter and narrows to one lane at the passes. "
          "Rebuilding it lets fuel, steel and crews reach the yards in a day rather than three. It is a modest project beside "
          "the interior trunk road, and it matters more to the navy than any new ship it could buy this decade.",
          ('logistics', 'bridge'), after=('sea_route_service',), reward=(Build('infrastructure', 1, 160),)),
    Focus('sea_headland_radar', 'Headland Radar Above the Harbour',
          "Merchant masters report ships shadowing them just beyond sight of the coast, and the route service has no way to "
          "see what they describe. Radar on the headlands above the harbour covers the approaches day and night. The sets are "
          "imported, the crews need a year of training and the first winter storms knock half of them out, but the coast is "
          "no longer blind.",
          ('radar', 'navy'), after=('sea_coast_road',), reward=(Build('radar_station', 1, 160),)),
    Focus('sea_escorts', 'An Escort in Every Convoy',
          "One doctrine says escorts belong with the cargo: every convoy sails with at least one armed ship, and merchant "
          "masters follow the escort's orders. It protects the ships that matter, wherever they go. It also means the navy is "
          "always at sea, always tired and never massed, and the coast is guarded by whatever happens to be in harbour.",
          ('navy', 'security'), after=('sea_headland_radar',), cost=10, exclusive=('sea_patrols',),
          reward=(Idea('convoy_escorts'), Flag('sea_escort'))),
    Focus('sea_patrols', 'Patrol the Home Approaches',
          "The other doctrine keeps the escorts near home, patrolling the approaches every Aemurraqi ship must cross, and "
          "leaves the open sea to the masters and their insurers. Patrols are cheaper and keep the fleet concentrated. Ships "
          "far from home are on their own, and the export houses ask whether their premiums now pay for a navy that never "
          "leaves sight of land.",
          ('navy', 'radar'), after=('sea_headland_radar',), cost=10, exclusive=('sea_escorts',),
          reward=(Idea('approach_patrols'), Flag('sea_patrol'))),
    Focus('sea_insurance_pool', 'A Shipping Insurance Pool',
          "Foreign underwriters price Aemurraqi cargoes as if every voyage were a gamble, and the premiums eat the margin on "
          "bulk exports. A national pool, backed by the treasury and the export houses together, insures the merchant fleet "
          "at home. It keeps foreign currency in the country. It also means that one bad year at sea lands directly on the "
          "national budget.",
          ('scales', 'navy'), after=('sea_route_service',), reward=(Idea('insurance_pool'),)),
    Focus('sea_escort_hulls', 'Escort Hulls from Our Own Slips',
          "With the third slip working, the yard lays down escort hulls to its own design: simple ships with good radios and "
          "enough range for the export routes. They are slower and lighter than foreign designs and far cheaper to keep at "
          "sea. The naval staff learns more from building two hulls at home than it ever learned from buying ten abroad.",
          ('navy', 'industry'), after=('sea_third_slip',), after_any=('sea_escorts', 'sea_patrols'),
          reward=(Research('naval_equipment', 0.5, 1), XP('navy', 15))),
    Focus('sea_masters_school', 'A School for Merchant Masters',
          "Masters and mates of the merchant fleet learned their trade aboard foreign ships, and they follow foreign signal "
          "books. A school in the harbour district trains them in national convoy procedures, radio discipline and damage "
          "control. Courses take officers off ships for months at a time. In return, the route service can order a convoy by "
          "radio and expect every master to understand.",
          ('training', 'navy'), after=('sea_insurance_pool',),
          reward=(Research('logistics_tech', 0.5, 1), XP('navy', 15))),
    Focus('sea_flag_rules', 'Rules for Ships Under Our Flag',
          "Ships registered under Aemurraq's flag must now meet national standards for crews, radios and maintenance, inspected "
          "at the harbour each year. Some owners re-register abroad rather than pay for the repairs. Those who stay gain "
          "cheaper cover from the pool and priority in the escort schedule, and the flag begins to mean something to foreign "
          "harbour masters.",
          ('document', 'navy'), after=('sea_masters_school',), reward=(SwapIdea('route_service', 'flag_standards'),)),
))

ARMY = Branch('army', 'The Volunteer Garrisons', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('army_rolls', 'Call the Volunteer Rolls',
          "The army is a volunteer force of four formations with six battalions' worth of trained men, equipped from small "
          "stocks of rifles and trucks. Nobody has counted how many volunteers would actually report if called. A muster "
          "across all five districts costs a week of pay and transport, and reveals which garrisons exist only in the "
          "returns.",
          ('training', 'security'), reward=(Idea('volunteer_garrisons'), Event('muster_day'))),
    Focus('army_hill_companies', 'Hill and Jungle Companies',
          "District B and District D hold the only hills and jungle in a desert country, and the land frontier runs partly "
          "through them. Infantry trained for open sand moves badly there. Raising companies that train in the hills each "
          "season, with the mountaineering instructors already on the army's books, gives the garrisons a skill that costs "
          "time rather than money.",
          ('training', 'tools'), after=('army_rolls',), reward=(Idea('hill_companies'),)),
    Focus('army_frontier_posts', 'Posts on Three Frontiers',
          "Aemurraq shares land frontiers with Azbekerania, Echea and Sotoa, and the crossings are watched by customs huts "
          "rather than soldiers. Small army posts at the main crossings, linked by track to the logistics centre, give early "
          "warning of trouble and somewhere to stop smugglers. The posts claim nothing beyond the line. They only make the "
          "line visible.",
          ('security', 'diplomacy'), after=('army_rolls',),
          reward=(Build('infrastructure', 1, 433), XP('army', 10))),
    Focus('army_militia', 'A Militia in Every District',
          "One answer to a small army is a large reserve: every district raises a militia of part-time volunteers who drill on "
          "weekends and guard depots, bridges and wells in a crisis. It is cheap and popular in the towns. Militia officers owe "
          "their posts to district notables, and a militia trained to guard its own district rarely wants to leave it.",
          ('security', 'civil'), after=('army_rolls',), exclusive=('army_regulars',),
          reward=(SwapIdea('volunteer_garrisons', 'district_militia'),)),
    Focus('army_regulars', 'Long-Service Regulars',
          "The other answer keeps the army small and makes it better: long-service volunteers on career pay, trained to move "
          "quickly between districts by truck and rail. Regulars cost several times as much per soldier as militia, and "
          "recruitment is slow in a country where the oil fields pay better. What the army lacks in numbers it gains in "
          "readiness.",
          ('medal', 'training'), after=('army_rolls',), exclusive=('army_militia',),
          reward=(SwapIdea('volunteer_garrisons', 'long_service'),)),
    Focus('army_trucks', 'Trucks Before Tanks',
          "The army's research priority has always been plain: transport, replacement equipment and service it can afford. "
          "The general staff makes it formal, spending a small procurement budget on trucks, spare parts and rifles rather "
          "than heavy armour it could neither fuel nor repair. Officers who wanted prestige are disappointed. Every formation "
          "keeps moving with what the country can make.",
          ('logistics', 'tools'), after_any=('army_militia', 'army_regulars'),
          reward=(Research('logistics_tech', 0.5, 1), Research('infantry_weapons', 0.5, 1))),
    Focus('army_arms_works', 'Small Arms Works in District D',
          "District D gains a small arms works that turns District E steel into rifles, mortars and spare parts close to the "
          "interior garrisons. It saves the long haul from the older arms plants and spreads defence jobs into the poorest "
          "district. The works would also make a tempting target in any war, which the general staff notes and the ministry "
          "ignores.",
          ('industry', 'security'), after=('army_trucks',), reward=(Build('arms_factory', 1, 468),)),
    Focus('army_staff_college', 'A Staff College for the Garrisons',
          "Officers of the garrisons learned staff work on the job and abroad, each in a different school. A national staff "
          "college in the capital teaches one method for planning, supply and orders. The first classes are small and the "
          "instructors are borrowed from the route service. The army gains officers who write orders the same way, which "
          "matters more than any new rifle.",
          ('training', 'document'), after=('army_trucks',),
          reward=(XP('army', 25), Research('land_doctrine', 0.5, 1))),
))

AIR = Branch('air', 'The Service Fighter Wing', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_service_wing', 'Thirty-Six Service Fighters',
          "The air arm flies thirty-six service fighters from a single air base in the Capital District, with pilots trained "
          "abroad and spares bought one crate at a time. It can defend the capital for a short while and do little else. "
          "Making it a wing with its own staff, budget and maintenance plan is the first step toward an air arm that lasts.",
          ('air', 'runway'), reward=(Idea('service_wing'),)),
    Focus('air_capital_field', 'Lengthen the Capital Air Base',
          "The capital's air base has one runway, a handful of shelters and fuel delivered by truck from the silo. Lengthening "
          "the runway, adding dispersal pads and piping fuel in directly lets the whole wing operate together and receive "
          "heavier transports. The works close the base for months, while the fighters borrow a desert strip and their pilots "
          "complain constantly.",
          ('runway', 'tools'), after=('air_service_wing',), reward=(Build('air_base', 2, 0),)),
    Focus('air_coast_strip', 'A Patrol Strip on the Coast',
          "Merchant ships leaving the harbour district pass beyond the fighters' reach within an hour. A patrol strip on the "
          "coast lets the wing cover the first leg of every route and lets the route service call for help that might "
          "actually arrive. The strip is basic: a runway, a fuel bladder and tents. It doubles the time an aircraft can stay "
          "over the lanes.",
          ('runway', 'navy'), after=('air_service_wing',), reward=(Build('air_base', 1, 160),)),
    Focus('air_ground_control', 'Ground Control for the Capital',
          "Fighters cannot intercept what nobody can see. A ground control station beside the capital air base tracks aircraft "
          "across the Capital District and talks the wing onto them by radio. The set is the most expensive single item the "
          "air arm owns, and its controllers must be trained abroad. Without it, the alert crews would simply be guessing.",
          ('radar', 'air'), after=('air_capital_field',), reward=(Build('radar_station', 1, 0),)),
    Focus('air_interceptors', 'An Interceptor Wing',
          "One school wants the wing to own the sky over the capital and the plants: fast-climbing fighters, ground control "
          "and alert crews at five minutes' readiness. It is the classic answer for a small air arm guarding a valuable "
          "capital. It leaves the coast and the sea lanes to the navy and the route service, who notice and complain in "
          "writing.",
          ('air', 'radar'), after_any=('air_capital_field', 'air_coast_strip'), cost=10, exclusive=('air_route_patrol',),
          reward=(Idea('interceptor_wing'),)),
    Focus('air_route_patrol', 'A Route Patrol Wing',
          "The other school wants long-range aircraft that patrol the sea lanes and frontier roads, reporting shadows to the "
          "route service and covering convoys on their first day out. Patrol work builds endurance and navigation rather than "
          "dogfighting. The capital keeps fewer fighters on alert, which the ministers dislike every time they hear engines "
          "overhead.",
          ('air', 'navy'), after_any=('air_capital_field', 'air_coast_strip'), cost=10, exclusive=('air_interceptors',),
          reward=(Idea('patrol_wing'),)),
    Focus('air_parts_line', 'Airframe Parts from Our Aluminium',
          "With the smelter line rebuilt, the wing's maintenance depot begins making its own airframe panels, brackets and "
          "ducting from Aemurraqi aluminium. Spares that once took months to arrive are cut and riveted in the capital. The "
          "parts are heavier than the originals and need constant inspection, but the wing no longer grounds aircraft for "
          "want of a bracket.",
          ('tools', 'air'), after_any=('air_interceptors', 'air_route_patrol'), requires=(HasFlag('smelter_running'),),
          reward=(Research('industry', 0.5, 1), XP('air', 20))),
    Focus('air_aggressors', 'Contract Instructors for the Wing',
          "Former top pilots of the Belkan Air Force are now hired by various countries to fly as aggressor squadrons. The "
          "wing can hire such instructors to fly against its own pilots in training. Their fees are high and their politics "
          "are their own business. Pilots who survive a month against them learn more than a year of ordinary drills could "
          "teach.",
          ('medal', 'air'), after=('air_service_wing',), requires=(After('1998.6.19'),),
          reward=(Idea('contract_instructors'),)),
))

BELKA = Branch('belka', 'The Belkan War Abroad', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_news', 'War Breaks Out Around Belka',
          "In March 1995 war breaks out around Belka, far from Aemurraq's frontiers. Its first effects arrive through the "
          "markets rather than the sky: oil prices jump, insurers add war-risk premiums to routes near the fighting and "
          "unfamiliar buyers start calling the export boards. The ministers must decide quickly whether this war is someone "
          "else's misfortune or Aemurraq's opportunity.",
          ('communications', 'diplomacy'), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war'), TimedIdea('war_premium', 365))),
    Focus('bw_sell_all', 'Sell to Any Buyer Who Pays',
          "The export boards argue that oil and rifles are commodities like any other, and that refusing buyers only hands the "
          "business to someone else. Selling to every party that pays in cash fills the arms plants in District E and the "
          "treasury alike. Every buyer's enemy will remember who supplied the shells, and some of those enemies have long "
          "memories.",
          ('economy', 'missile'), after=('bw_news',), exclusive=('bw_embargo',),
          reward=(Idea('open_order_book'), Flag('war_sales'))),
    Focus('bw_embargo', 'No Arms to Any Belligerent',
          "The opposing view holds that a small country with a large merchant fleet survives by being nobody's arsenal. An "
          "embargo on arms to every belligerent keeps fuel and civilian goods flowing but stops every weapons contract. The "
          "arms plants lose orders and their workers lose overtime. Aemurraqi ships, in return, are less likely to be stopped "
          "and searched at sea.",
          ('peace', 'scales'), after=('bw_news',), exclusive=('bw_sell_all',),
          reward=(Idea('arms_embargo'), Flag('war_embargo'))),
    Focus('bw_windfall', 'Bank the Wartime Windfall',
          "High wartime oil prices bring more revenue in one season than in the two years before. The ministry can spend it at "
          "once on roads and wages, or bank it in a stabilisation fund for the years when prices fall again. Spending wins "
          "votes and the fund wins nothing visible. The ministers bank most of it, knowing nobody will thank them.",
          ('economy', 'scales'), after_any=('bw_sell_all', 'bw_embargo'), reward=(Idea('windfall_fund'),)),
    Focus('bw_lumen', 'The Treaty Signed at Lumen',
          "A treaty signed in Lumen in June 1995 ends the Belkan War. Oil prices drift back down and the insurers cut their "
          "war-risk premiums on most routes. The export boards want the wartime prices back; the ministries want to know how "
          "much of the boom was real. The end of the war is a relief and a budget problem at the same time.",
          ('peace', 'document'), after=('bw_windfall',), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_premium'), Stability(0.03))),
    Focus('bw_arms_audit', 'Account for the Arms Sales',
          "With the war over, foreign governments ask who sold what to whom, and Aemurraq's arms plants appear in several "
          "answers. Licensing every future arms export, with buyer, quantity and end use published each year, turns an "
          "embarrassment into a system. The plants keep most of their customers. A few of the more discreet buyers take their "
          "business elsewhere.",
          ('document', 'industry'), after=('bw_lumen',), requires=(HasFlag('war_sales'),),
          reward=(SwapIdea('open_order_book', 'export_licences'),)),
    Focus('bw_clean_hands', 'A Reputation for Clean Hands',
          "The embargo held for the whole war, and foreign ministries noticed. Aemurraqi ships were searched less often, its "
          "diplomats were welcomed as neutral hosts and the export boards found buyers who wanted a supplier with no enemies. "
          "The arms plants are still short of orders. The country, however, has earned a reputation that no later government "
          "could buy.",
          ('peace', 'diplomacy'), after=('bw_lumen',), requires=(HasFlag('war_embargo'),),
          reward=(SwapIdea('arms_embargo', 'neutral_reputation'),)),
    Focus('bw_belka_lost', 'Machine Tools at Bargain Prices',
          "In this outcome Belka has lost the war, and its defeat leaves factories, machine tools and trained staff looking for "
          "new customers abroad. Aemurraq's ministries can buy surplus machinery cheaply and offer contracts to engineers "
          "willing to relocate. The bargains are real. So is the risk that the victors will see the country as a refuge for "
          "the losing side.",
          ('tools', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Research('industry', 0.5, 1), PP(15))),
    Focus('bw_belka_won', 'Orders from a Victorious Belka',
          "In this outcome Belka has won the war, and its ministries need fuel, aluminium and shipping for their own "
          "reconstruction. Purchasing missions arrive with long lists and prompt payment. Accepting the orders fills "
          "Aemurraq's tankers. It also places the country among Belka's suppliers at the moment Belka's defeated neighbours "
          "are deciding whom to remember.",
          ('diplomacy', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_orders', 365),)),
))

ULYSSES = Branch('ulysses', 'Under the Ulysses Warning', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_announcement', 'The Asteroid Is Coming',
          "Astronomers warned in December 1994 that the asteroid Ulysses might strike the Earth. In April 1996 the warning "
          "becomes an announcement: it will strike, and nations must prepare. Nobody can say where fragments will fall. "
          "Aemurraq has deserts, a crowded capital and a merchant fleet at sea, and every ministry suddenly has a plan that "
          "needs money.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),),
          reward=(Idea('sky_watch'), Event('ulysses_announced'))),
    Focus('uly_cisterns', 'Cisterns and Deep Shelters',
          "Engineers propose shelters cut beneath the capital and the district towns, with sealed cisterns holding weeks of "
          "water. In a desert country, water is the first thing to fail after any disaster. The plan is slow and enormously "
          "expensive. It protects people who reach the shelters in time, and does nothing for anyone caught on the open "
          "road.",
          ('shelter', 'civil'), after=('uly_announcement',), cost=10, exclusive=('uly_warning_net',),
          reward=(Idea('deep_cisterns'),)),
    Focus('uly_warning_net', 'A Warning Net Across the Districts',
          "Radar and observatory specialists propose a warning net instead: tracking stations, sirens in every town and a "
          "radio chain that can clear a district within hours, with its main tracking post in District D. Warning is cheaper "
          "than concrete and covers the roads and the sea. It depends entirely on accurate tracking, and on people believing "
          "the sirens at three in the morning.",
          ('radar', 'meteor'), after=('uly_announcement',), cost=10, exclusive=('uly_cisterns',),
          reward=(Idea('warning_net'), Build('radar_station', 1, 468))),
    Focus('uly_staple_reserve', 'A Reserve of Grain and Fuel',
          "In a desert country, grain and clean water run short first after any disruption, and most of the oil leaves by "
          "sea. A national reserve of grain, medicine and fuel, held in the districts rather than the capital, buys weeks of "
          "breathing space. Filling the stores pushes up market prices just as the public is already nervous, and the "
          "markets notice.",
          ('logistics', 'civil'), after_any=('uly_cisterns', 'uly_warning_net'), reward=(Idea('staple_reserve'),)),
    Focus('uly_open_drills', 'Rehearse the Evacuation in Public',
          "The constituent cabinet takes its preparations to the chamber, publishing every plan and rehearsing evacuations in "
          "public with deputies taking part. The first drills are clumsy and the press mocks them. By the third, towns know "
          "their routes and shelters, and the cabinet has turned a frightening subject into a civic duty the nationalist "
          "deputies cannot easily attack.",
          ('ballot', 'shelter'), after=('uly_staple_reserve',), requires=(HasFlag('path_constituent'),),
          reward=(Idea('open_drills'),)),
    Focus('uly_board_grain', 'The Boards Buy Forward',
          "The council of boards treats the asteroid as a supply problem and solves it the way the boards solve everything: "
          "with contracts. Grain, medicine and water containers are bought forward on long terms and stored in board "
          "warehouses near every district town. The stores are efficient and well guarded, and the boards alone decide when "
          "and to whom they are released.",
          ('economy', 'logistics'), after=('uly_staple_reserve',), requires=(HasFlag('path_boards'),),
          reward=(Idea('board_grain'),)),
    Focus('uly_brigade_stores', 'Brigades Guard the Stores',
          "The directorate hands preparation to the movement brigades, who dig cisterns, stack sandbags and guard the reserve "
          "depots with evident enthusiasm. Volunteers sign up faster than the depots can use them. The brigades also keep "
          "the shelter rolls, and families with the wrong neighbours or the wrong opinions find their names lower down the "
          "list.",
          ('security', 'logistics'), after=('uly_staple_reserve',), requires=(HasFlag('path_resolve'),),
          reward=(Idea('brigade_stores'),)),
    Focus('uly_officer_shelters', 'Officers Run the Shelters',
          "The command council treats the impact as a military emergency and runs it like one. Officers draw up evacuation "
          "tables, garrisons rehearse road control and every district receives a duty officer with authority over the "
          "shelters. The drills are punctual and thorough. Civilians obey because they must, and the council learns how much "
          "it enjoys running the civilian state.",
          ('command', 'shelter'), after=('uly_staple_reserve',), requires=(HasFlag('path_command'),),
          reward=(Idea('officer_shelters'),)),
    Focus('uly_roche_night', 'Listening Through the Roche Night',
          "On 8 July 1999 Ulysses passes through the Roche limit of the Earth. For Aemurraq the night is spent listening: to "
          "shortwave bulletins, to the warning chain and to merchant masters reporting by radio from distant routes. Whatever "
          "falls, wherever it falls, the country will feel it through the markets and the sea lanes for years afterwards.",
          ('meteor', 'communications'), after=('uly_staple_reserve',), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('uly_harbour_reception', 'Ships Seeking Harbour',
          "When Erusea stops taking in refugees in April 2000, the route service expects ships carrying displaced families to "
          "try any harbour that might admit them, including the harbour district. Admitting them strains housing and the "
          "reserve stores. Turning them away saves money and costs the country its standing with every merchant master who "
          "watches a ship leave again.",
          ('refugees', 'navy'), after=('uly_roche_night',), requires=(After('2000.4.21'),),
          reward=(Idea('harbour_reception'),)),
    Focus('uly_district_stores', 'Reserve Depots in Every District',
          "The district accord fixes revenue shares, so the reserve can finally be spread fairly: a depot in each district, "
          "sized by population and distance from the capital. District E's depot needs a better road to reach its plant towns, "
          "and the accord pays for it. The capital loses its monopoly on emergency stores, which is what the other four "
          "districts wanted.",
          ('logistics', 'shelter'), after=('uly_staple_reserve',), requires=(HasFlag('districts_settled'),),
          reward=(Build('infrastructure', 1, 502), Stability(0.02))),
))

USEA = Branch('usea', 'War Across the Sea in Usea', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('uc_san_salvacion', 'War Reaches San Salvacion',
          "In the summer of 2003 Erusea invades the neutral country of San Salvacion, seizes Stonehenge and begins using its "
          "railguns as anti-air batteries. Usea lies far from Aemurraq's districts, yet Usean ports buy its steel and Usean "
          "lanes carry its oil. Insurers move before governments do, and within weeks every cargo bound for Usean waters "
          "costs more to send.",
          ('missile', 'communications'), requires=(After('2003.6.1'),),
          reward=(Event('usean_war'), TimedIdea('war_risk', 730))),
    Focus('uc_isaf_fuel', 'Fuel Contracts with the ISAF',
          "In August 2003 the FCU establishes the ISAF to oppose Erusea. Its quartermasters need fuel, steel and shipping, and "
          "they pay on time. Signing supply contracts fills the plants and the tankers without sending a single Aemurraqi "
          "soldier. Erusea will regard every such cargo as hostile, and Aemurraqi ships near its coast will be treated "
          "accordingly.",
          ('diplomacy', 'logistics'), after=('uc_san_salvacion',), requires=(After('2003.8.22'),),
          exclusive=('uc_neutral_flag', 'uc_cash_cargoes'), reward=(Idea('isaf_contracts'),)),
    Focus('uc_neutral_flag', 'No Cargo for Either Side',
          "The neutral camp wants nothing loaded in Aemurraq to reach either army: no fuel for the ISAF, no steel for Erusea, "
          "and inspectors on the wharf to make sure of it. Merchant masters gain a flag that both navies have reason to "
          "respect. The export boards lose the most profitable contracts of the decade and say so at every opportunity.",
          ('peace', 'navy'), after=('uc_san_salvacion',),
          exclusive=('uc_isaf_fuel', 'uc_cash_cargoes'), reward=(Idea('neutral_flag'),)),
    Focus('uc_cash_cargoes', 'Cash Cargoes for Any Port',
          "A third view treats the war as a market: Aemurraq sells fuel and steel to civilian buyers in any port that pays in "
          "advance, and asks nothing about where the cargo goes next. Revenue rises fast and the plants run overtime. Both "
          "sides suspect Aemurraq of supplying the other, and the insurers price that suspicion into every single voyage.",
          ('economy', 'navy'), after=('uc_san_salvacion',),
          exclusive=('uc_isaf_fuel', 'uc_neutral_flag'), reward=(Idea('cash_cargoes'),)),
    Focus('uc_war_freight', 'Export Houses Chase War Freight',
          "The chartered export houses, built for long contracts and steady tonnage, discover that wartime freight pays three "
          "times the peacetime rate. They charter every spare hull and fill them with crude and ore. The houses grow rich and "
          "royalties rise with them. The merchant fleet ages faster than anyone planned, because nobody will take a ship out "
          "of service.",
          ('logistics', 'economy'), after=('uc_san_salvacion',), requires=(HasFlag('model_export'),),
          reward=(Idea('war_freight'),)),
    Focus('uc_refinery_overtime', 'Refineries on Three Shifts',
          "Usean buyers want refined fuel rather than crude, and the refining programme is ready for them. The plants move to "
          "three shifts, paying overtime and squeezing maintenance into the margins. Output and revenue climb together. "
          "Engineers warn that equipment run this hard for two years will need a long and expensive rest once the war is "
          "over.",
          ('industry', 'tools'), after=('uc_san_salvacion',), requires=(HasFlag('model_refining'),),
          reward=(Idea('refinery_overtime'),)),
    Focus('uc_state_quota', 'Wartime Quotas from the Oil Office',
          "The state oil office allocates wartime sales by quota: so much for home use, so much for the reserve and so much "
          "for foreign contracts at prices it sets itself. Private traders call it a monopoly in a uniform. It keeps domestic "
          "fuel cheap while the world pays war prices, and it puts more revenue under ministerial control than ever before.",
          ('command', 'economy'), after=('uc_san_salvacion',), requires=(HasFlag('model_state'),),
          reward=(Idea('state_quota'),)),
    Focus('uc_escort_run', 'Escorts on the Usean Run',
          "Under the escort doctrine, every convoy bound for Usean waters sails with an armed Aemurraqi ship that turns back at "
          "the edge of the war zone. The escorts log more sea time in two years than in the previous decade. Crews are "
          "exhausted and hulls need refits, but masters keep sailing because someone is sailing with them.",
          ('navy', 'security'), after_any=('uc_isaf_fuel', 'uc_neutral_flag', 'uc_cash_cargoes'),
          requires=(HasFlag('sea_escort'),), reward=(TimedIdea('escorted_season', 365), XP('navy', 20))),
    Focus('uc_home_approaches', 'Close Guard on the Approaches',
          "Under the patrol doctrine, the navy tightens its watch on the approaches to the harbour district and leaves distant "
          "routes to the insurers. A second radar post on the headlands and constant patrols keep the coast safe from any "
          "raider the war sends wandering. Masters bound for Usea are alone beyond the horizon, and their association says "
          "so weekly.",
          ('radar', 'security'), after_any=('uc_isaf_fuel', 'uc_neutral_flag', 'uc_cash_cargoes'),
          requires=(HasFlag('sea_patrol'),), reward=(Build('radar_station', 1, 160), XP('navy', 15))),
    Focus('uc_railguns_silent', 'The Railguns Fall Silent',
          "In this outcome Stonehenge has been destroyed and its railguns no longer command the Usean sky. Insurers cut their "
          "war-risk rates on the routes nearest the fighting, and masters who refused Usean charters begin to accept them. "
          "Aemurraq drops its surcharge on Usean cargoes, which pleases the export boards and costs the treasury a useful "
          "source of revenue.",
          ('peace', 'missile'), after=('uc_san_salvacion',), requires=(HasGlobal('ac_ucw_stonehenge_destroyed'),),
          reward=(RemoveIdea('war_risk'), Stability(0.02))),
    Focus('uc_rebuilding_orders', 'Orders for the Rebuilding',
          "In this outcome the war ends with the ISAF victorious, and rebuilding begins along the battered Usean coast. Ports, "
          "bridges and power lines need steel, aluminium and fuel by the shipload. Aemurraq's boards and plants bid for the "
          "contracts beside larger exporters. The orders are welcome, but payment stretches over years and the creditors "
          "are nearly bankrupt themselves.",
          ('rebuild', 'diplomacy'), after=('uc_san_salvacion',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('reconstruction_orders', 365),)),
    Focus('uc_erusea_terms', 'Trading with a Victorious Erusea',
          "In this outcome Erusea has won its war, and the Usean lanes now run past ports under Erusean control. Its trade "
          "offices invite foreign suppliers to sign new terms, with inspection rights and preferred prices. Signing keeps "
          "Aemurraqi cargoes moving into Usea. It also ties the country's largest new customer to a government many of its old "
          "customers distrust.",
          ('diplomacy', 'scales'), after=('uc_san_salvacion',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Idea('cautious_trade'),)),
    Focus('uc_fifteen_years', 'An Account of Fifteen Years',
          "As the war in Usea winds down, the government publishes a plain account of fifteen years: how Aemurraq is governed, "
          "what its districts produced, how its ships fared and what the asteroid and two distant wars cost. The account "
          "promises nothing about the next era. It records where the country stands, so whoever governs next starts from "
          "figures rather than slogans.",
          ('document', 'assembly'), after_any=('uc_isaf_fuel', 'uc_neutral_flag', 'uc_cash_cargoes'),
          requires=(HasFlag('order_settled'), After('2005.1.1')),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (ADMIN, DISTRICTS, OIL, SEA, ARMY, AIR, BELKA, ULYSSES, USEA)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('escort_season', 'Escort the Export Season',
                'The route service escorts the busiest four months of the export year, at the cost of fuel and crew rest. '
                'Repeatable once a year.',
                40, (TimedIdea('escorted_season', 120), XP('navy', 10)), requires=(Completed('sea_route_service'),), cooldown=365),
    DecisionDef('fuel_reserve_release', 'Open the Fuel Reserve',
                'Sells part of the fuel reserve at band prices to calm a domestic price spike. Once only; the reserve takes '
                'years to refill.',
                50, (Stability(0.04), TimedIdea('fuel_release', 180)), requires=(Completed('oil_price_bands'),)),
    DecisionDef('interior_grading', 'Grade the Interior Tracks',
                'Road crews grade and gravel the side tracks off the District D trunk road. A one-time works programme.',
                75, (Build('infrastructure', 1, 468),), requires=(Completed('dist_interior_trunk'),)),
    DecisionDef('second_interior_plant', 'Commission a Second Interior Plant',
                'Funds a second workshop plant in District D once the first is running. A one-time charge on the works budget.',
                100, (Build('industrial_complex', 1, 468),), requires=(Completed('dist_interior_workshops'),)),
    DecisionDef('ministry_inspection', 'Inspect a Ministry Unannounced',
                'Inspectors arrive at one ministry without warning and publish what they find. Repeatable every six months; '
                'officials resent it.',
                25, (TimedIdea('inspected_ministries', 90),), requires=(Completed('adm_mandate_audit'),), cooldown=180),
    DecisionDef('crossing_market_days', 'Market Days at the Crossings',
                'The frontier posts host open market days for traders from both sides of the line. Repeatable once a year.',
                30, (TimedIdea('market_days', 120), Stability(0.01)), requires=(Completed('army_frontier_posts'),), cooldown=365),
)
