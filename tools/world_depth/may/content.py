"""Malynea (MAY): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party with
elections suspended, popularity split between fascism 50 and neutrality 48 percent), the
unnamed National Administration office, the three 1991 states with their neutral captions,
the map (forest coast, one hill province, one railway, six detached hill islands, cold
winters, land neighbours) and the global flags other mod scripts already set. Official: ACES
Chronicle rows used only as date anchors for distant pressures, each cited by its exact key.
Everything else, including every Malynean choice, office, idea, building, decision and event,
is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='MAY', name='Malynea', root='world', package='may',
                  themes=('logistics', 'shelter', 'ballot'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities fascism 50, neutrality 48, democratic 1, communism 1; stability 0.5 and war support 0.5; three '
           'research slots including tech_mountaineers and early_fighter. The starting leader is the unnamed National '
           'Administration office (MAY_ac_government_office, centrism), whose 1991 holder has not been established. Only '
           'MAY_democratic (Malynea) is localised as a country name. The tree never names a holder; party popularity is read '
           'as context, not as proof of constitutional form (institution civil_administration, capacity 40).',
           'mod/2985041246/history/countries/MAY - Malynea.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; tools/institutions/profiles.json'),
    Source('Mod provenance',
           'Geography: three 1991 states, all category town with four shared slots. 341 (capital, captioned Malynea Capital '
           'District): forest provinces 321, 4010, 5515, 7842 and 7949, plains 1125, hills 3480; 2 civilian, 1 arms, 1 '
           'dockyard (no free slot), infrastructure 2, naval base, supply node and victory point 20 in coastal province 5515 '
           '(captioned Malynea Capital Centre); steel 5, oil 2, rubber 2. 328 (captioned Malynea District B): coastal plains '
           '1698, forest 1935 and 4304; 1 civilian and 2 arms (one free slot), infrastructure 2; steel 4, oil 2, rubber 1. '
           '290 (captioned Malynea District A): six detached hill islands 2243, 2379, 3394, 9931, 9939 and 9940, each with a '
           'naval base and nothing else, infrastructure 0, four free slots, lying far to the west of the mainland with no '
           'other land nearby. One level-2 railway runs 5515-1125-1698. Mainland strategic region 236 has winters well below '
           'freezing with snow and blizzards. Land neighbours computed from map/provinces.bmp: BAL (321) via 1698 and 4304; '
           'SET (356, mountain provinces) via 1935, 3480 and 4304; VLK (359 and 382) via 321, 3480 and 7949. Compass words come '
           'from province centroids. Captions are not used as place names; no place is named.',
           'mod/2985041246/history/states/290-State_290.txt; mod/2985041246/history/states/328-State_328.txt; '
           'mod/2985041246/history/states/341-State_341.txt; mod/2985041246/map/definition.csv; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/supply_nodes.txt; mod/2985041246/map/strategicregions/236-XXX.txt; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; tools/regional_labels/labels.json; '
           'tools/world_capitals/placements.json'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role island civil defense and merchant receiving; 3 civilian, 3 '
           'military and 1 naval factory (the only merchant convoy yard among the civil-defence roles); two infantry '
           'formations (four battalions), infantry-only with no support companies; combat aviation and combat navy '
           'deliberately absent; 152 convoys; stocks of 800 infantry equipment, 560 motorized equipment and 24 trains; '
           'research priority Physical Sustainment. Fiscal figures (GDP 60, growth 3.0) are fictional calibration, not canon '
           'national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/economy_v2/profiles.json; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour context only: Seterano and Valka inherit the same template as Malynea (democratic ruling party, '
           'elections suspended, fascism 50 and neutrality 48 percent). Baltica, read from its own tree, has one railway '
           '797-1235-1628 ending at its harbour on the frontier with Malynea and makes only unilateral offers to its small '
           'neighbours. Malynean offers are unilateral too; no neighbour response or border change is asserted.',
           'mod/2985041246/history/countries/SET - Seterano.txt; mod/2985041246/history/countries/VLK - Valka.txt; '
           'mod/2985041246/history/countries/BAL - Baltica.txt; tools/world_depth/bal/content.py'),
    Source('Official', 'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, '
           'Yuktobania. Used only for the merchant masters leaf, which also requires the mod global flag ac_bwr_cinigrad; no '
           'Malynean role is claimed.', '1991 / 09.02'),
    Source('Official', 'Date anchor: the IAU announces that Ulysses may strike the Earth. Background to the asteroid branch.',
           '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Opening of the wartime charter branch; Malynea takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Date gate of the falling rates focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Date gate of the asteroid branch '
           'opening; where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Date gate of the July vigil focus; no '
           'damage in Malynea is claimed.', '1999 / 07.08'),
    Source('Official', 'Erusea invades the neutral country of San Salvacion and seizes Stonehenge. Background to the Usean '
           'lanes focus, which also requires the mod global flag ac_ucw_war_started; no Malynean role is claimed.',
           '2003 / SUMMER'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_bwr_cinigrad (common/scripted_effects/ac_belkan_record.txt); '
           'belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt); ac_ucw_war_started, '
           'ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory (common/scripted_effects/ac_ucw.txt). Each outcome '
           'reaction is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/common/scripted_effects/ac_belkan_record.txt; mod/2985041246/events/Belka.txt; '
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Malynean focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects. Buildings only in states '
           '290, 328 and 341: the capital state has no free shared slot, so it gains only infrastructure, air base and radar '
           'levels; 328 gains one shared building from a mutually exclusive pair; 290 gains a dockyard and a civilian plant.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the suspended ballot
    IdeaDef('caretaker_rule', 'Caretakers With the Seals', 'A democratic administration governing with the ballot suspended.',
            {'political_power_gain': 0.05, 'stability_factor': -0.04, 'war_support_factor': 0.02}, ('document', 'command')),
    IdeaDef('ballot_promised', 'The Ballot Has a Date', 'The overdue election has a date, and every camp is campaigning for it.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'communications')),
    IdeaDef('board_compact', 'The District Boards Compact', 'Administrators from the three districts agree to govern by published rules.',
            {'political_power_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.02}, ('assembly', 'document')),
    IdeaDef('movement_pressure', 'The Movement in the Streets', 'The national movement marches for a government of readiness.',
            {'war_support_factor': 0.05, 'stability_factor': -0.02}, ('security', 'assembly')),
    IdeaDef('ballot_restored', 'Rolls for Every District', 'Every adult on the mainland and the islands is on a voter roll.',
            {'stability_factor': 0.06, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('board_minutes', 'Minutes in Public', 'The board posts its minutes and reasons at every post office.',
            {'stability_factor': 0.04, 'political_power_factor': 0.08}, ('document', 'scales')),
    IdeaDef('readiness_decrees', 'Readiness by Decree', 'Numbered decrees on rationing, travel, the press and service.',
            {'war_support_factor': 0.08, 'army_core_defence_factor': 0.05, 'stability_factor': -0.02}, ('security', 'command')),
    IdeaDef('charter_court', 'The Charter Court', 'Judges on long terms read the charter when governments disagree with it.',
            {'stability_factor': 0.05, 'political_power_factor': 0.04}, ('scales', 'assembly')),
    IdeaDef('merit_service', 'Examined Civil Servants', 'Posts filled by written examinations marked without names.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.03}, ('document', 'training')),
    # the port and its hulls
    IdeaDef('hull_register', 'The Merchant Hull Register', 'Every merchant hull checked against its line in the register.',
            {'industrial_capacity_dockyard': 0.03, 'naval_coordination': 0.02}, ('navy', 'document')),
    IdeaDef('open_charters', 'Charters Open to Any Shipper', 'Light rules and low fees for any shipper who registers or charters here.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.01}, ('logistics', 'economy')),
    IdeaDef('home_cargo_rule', 'Home Cargoes First', 'Malynean hulls carry Malynean cargo first and foreign cargo with spare tonnage.',
            {'production_speed_buildings_factor': 0.04, 'consumer_goods_factor': -0.02}, ('logistics', 'industry')),
    IdeaDef('pilot_guild', 'Examined Harbour Pilots', 'Examined pilots on a duty roster with a pension fund.',
            {'naval_speed_factor': 0.04, 'navy_org_factor': 0.02}, ('navy', 'medal')),
    IdeaDef('winter_roadstead', 'The Winter Channel Tug', 'A strengthened tug and a marked channel keep the port working through the ice.',
            {'production_speed_infrastructure_factor': 0.08, 'naval_speed_factor': 0.03}, ('navy', 'tools')),
    IdeaDef('lane_watch', 'Listening on the Island Lane', 'Merchant masters carry hydrophones and a reporting code.',
            {'naval_coordination': 0.05, 'air_detection': 0.03}, ('submarine', 'communications')),
    IdeaDef('masters_school', 'The Convoy Masters School', 'Masters learn station-keeping, winter navigation and radio procedure ashore.',
            {'navy_org_factor': 0.05, 'industrial_capacity_dockyard': 0.04}, ('training', 'navy')),
    IdeaDef('ice_channel', 'A Channel Through the Ice', 'The tug runs day and night to keep a winter channel open.',
            {'naval_speed_factor': 0.06, 'production_speed_infrastructure_factor': 0.05}, ('tools', 'logistics')),
    IdeaDef('charter_drive', 'Charter Agents Abroad', 'Port authority agents in foreign ports are winning charters for Malynean hulls.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('diplomacy', 'logistics')),
    # the western islands
    IdeaDef('island_isolation', 'Islands Beyond the Roads', 'Six hill islands that depend on the convoy lane for nearly everything.',
            {'stability_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('refugees', 'navy')),
    IdeaDef('island_radio', 'Harbour Office Radios', 'Every island harbour office can reach the others and the capital at any hour.',
            {'stability_factor': 0.02, 'air_detection': 0.04}, ('communications', 'civil')),
    IdeaDef('island_councils', 'Island Purses', 'Island councils raise their own harbour dues and spend them at home.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.10}, ('assembly', 'economy')),
    IdeaDef('island_prefects', 'Island Prefects', 'A prefect from the capital governs each island with a budget and staff.',
            {'political_power_gain': 0.08, 'production_speed_buildings_factor': 0.04}, ('command', 'civil')),
    IdeaDef('hospital_rota', 'A Surgery Afloat', 'A converted freighter with a surgery sails a fixed round of the islands.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.01}, ('medical', 'navy')),
    IdeaDef('island_deputies', 'Island Seats in the Chamber', 'Island deputies vote together on the lane, the dues and the hospital ship.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('ballot', 'fishing')),
    IdeaDef('supply_run', 'The Extra Supply Run', 'An extra convoy has carried fuel, flour and medicine to the islands.',
            {'stability_factor': 0.03}, ('logistics', 'refugees')),
    # the four battalions
    IdeaDef('thin_service', 'Four Battalions on the Roll', 'An infantry-only civil defence army with no artillery, engineers or aircraft.',
            {'army_core_defence_factor': 0.03, 'training_time_army_factor': 0.05}, ('security', 'document')),
    IdeaDef('forest_screens', 'Screens on the Forest Roads', 'Small units hold the forest junctions and tracks.',
            {'army_defence_factor': 0.05, 'army_core_defence_factor': 0.05}, ('security', 'bridge')),
    IdeaDef('hill_garrison', 'The Southern Hill Garrison', 'A permanent garrison on the one hill province, facing two frontiers.',
            {'army_core_defence_factor': 0.08, 'army_org_factor': 0.03}, ('command', 'security')),
    IdeaDef('shore_lines', 'Lines Along the Capital Shore', 'Trenches, wire and anti-aircraft positions ring the capital port.',
            {'army_core_defence_factor': 0.05, 'static_anti_air_damage_factor': 0.05}, ('security', 'navy')),
    IdeaDef('reserve_cards', 'Reserve Cards', 'Every trained adult holds a card naming a depot, a company and a day.',
            {'training_time_army_factor': -0.10}, ('document', 'training')),
    IdeaDef('winter_drill', 'Drilled in the Long Winter', 'The battalions train on skis, in snow shelters and with frozen trucks.',
            {'attrition': -0.05, 'army_org_factor': 0.04}, ('training', 'shelter')),
    IdeaDef('rail_depots', 'Depots on the One Line', 'Food, fuel and ammunition wait at every station on the railway.',
            {'supply_consumption_factor': -0.05, 'army_speed_factor': 0.03}, ('rail', 'logistics')),
    IdeaDef('frontier_wardens', 'Frontier Wardens', 'Movement volunteers patrol the frontiers and report to the committee.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.04, 'stability_factor': -0.02}, ('security', 'medal')),
    IdeaDef('civil_defence_corps', 'Rescue and Shelter Wardens', 'Firefighters, rescue teams, medics and shelter wardens trained with the army.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.03}, ('shelter', 'medical')),
    IdeaDef('reserve_callout', 'A Year Group at the Depots', 'One year group of reservists is drilling at its depots.',
            {'army_org_factor': 0.04, 'training_time_army_factor': -0.05}, ('training', 'security')),
    # works and resources
    IdeaDef('works_audit', 'The Works Inventory', 'An honest account of what each plant makes, wastes and needs.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('steel_contracts', 'Steel on Long Contracts', 'The capital district mines sell to the domestic works on long contracts.',
            {'industrial_capacity_factory': 0.03}, ('industry', 'tools')),
    IdeaDef('coastal_wells', 'Deepened Coastal Wells', 'Old wells near the coast deepened and linked to a tank farm at the port.',
            {'production_speed_buildings_factor': 0.04}, ('economy', 'tools')),
    IdeaDef('repair_economy', 'The Repair Economy', 'Spare parts and repair contracts for hulls, trucks and machines.',
            {'production_speed_industrial_complex_factor': 0.08, 'repair_speed_factor': 0.08}, ('rebuild', 'tools')),
    IdeaDef('arms_lines', 'The Fourth Arms Line', 'Rifles and trucks for the battalions and for licensed export.',
            {'production_speed_arms_factory_factor': 0.08, 'industrial_capacity_factory': 0.03}, ('missile', 'industry')),
    IdeaDef('rail_overhaul', 'Rolling Stock in the Workshops', 'Engines and wagons are being rebuilt one by one.',
            {'production_speed_infrastructure_factor': 0.10}, ('rail', 'tools')),
    IdeaDef('timber_trade', 'The Timber Board', 'Graded logs, replanting rules and export sales through the port.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.01}, ('economy', 'logistics')),
    IdeaDef('tyre_works', 'The Tyre Works', 'Tyres and belting made from home-grown rubber.',
            {'supply_consumption_factor': -0.03, 'production_factory_max_efficiency_factor': 0.02}, ('industry', 'logistics')),
    IdeaDef('district_power', 'One Grid for Two Districts', 'A power line through the forest joins the frontier district to the capital.',
            {'production_factory_max_efficiency_factor': 0.03, 'production_speed_buildings_factor': 0.03}, ('communications', 'industry')),
    IdeaDef('board_tenders', 'Tenders Under Board Rules', 'Public contracts tendered by written rules and published with the price.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_factor': 0.03}, ('scales', 'economy')),
    # neighbours
    IdeaDef('frontier_survey', 'Three Frontiers Recorded', 'Every crossing, track and customs post on three frontiers is recorded.',
            {'army_core_defence_factor': 0.02, 'political_power_gain': 0.03}, ('document', 'bridge')),
    IdeaDef('equal_distance', 'No Neighbour Favoured', 'The same rules for every neighbour and favours for none.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('scales', 'peace')),
    IdeaDef('neighbour_consults', 'Talks With Small Neighbours', 'Regular meetings offered on weather, fires, crossings and trade.',
            {'stability_factor': 0.02, 'research_speed_factor': 0.03}, ('diplomacy', 'assembly')),
    IdeaDef('sea_orientation', 'Facing the Sea', 'Diplomacy follows the cargo to the ports where Malynean hulls call.',
            {'consumer_goods_factor': -0.03, 'naval_speed_factor': 0.03}, ('diplomacy', 'navy')),
    IdeaDef('fire_watch', 'The Fire Watch', 'Watchtowers along the western forest staffed every dry season.',
            {'stability_factor': 0.02, 'air_detection': 0.03}, ('telescope', 'security')),
    IdeaDef('weather_service', 'Hill Weather Reports', 'Daily forecasts broadcast from stations on the southern hill.',
            {'planning_speed': 0.05, 'attrition': -0.03}, ('telescope', 'communications')),
    IdeaDef('fire_season', 'Fire Season Patrols', 'The towers and fire crews are on full watch before the dry season.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.05}, ('telescope', 'civil')),
    # the Belkan War years
    IdeaDef('war_charter_boom', 'A Wartime Charter Market', 'Neutral tonnage is scarce and Malynean hulls are in demand.',
            {'consumer_goods_factor': -0.03, 'stability_factor': -0.02, 'political_power_gain': 0.05}, ('logistics', 'missile')),
    IdeaDef('neutral_markings', 'Neutral Colours', 'Name, flag and the word neutral painted large on every hull.',
            {'naval_coordination': 0.04, 'stability_factor': 0.02}, ('peace', 'navy')),
    IdeaDef('neutral_port_trade', 'Any Neutral Port', 'Masters may take any charter to a port not at war.',
            {'consumer_goods_factor': -0.04, 'war_support_factor': -0.02}, ('logistics', 'diplomacy')),
    IdeaDef('home_waters', 'Home Waters Only', 'The fleet keeps to the home lanes and distant ports until the peace.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('peace', 'shelter')),
    IdeaDef('foreign_crews', 'Crews From Abroad', 'Foreign sailors fill Malynean berths under one standard of wages and papers.',
            {'industrial_capacity_dockyard': 0.05, 'stability_factor': -0.01}, ('refugees', 'logistics')),
    IdeaDef('home_holds', 'Guaranteed Home Freight', 'The treasury pays owners a fixed wartime rate for home cargo.',
            {'production_speed_buildings_factor': 0.05}, ('economy', 'logistics')),
    IdeaDef('belkan_routes', 'Charter Lanes to Belka', 'Belkan shippers hire neutral tonnage that kept its distance.',
            {'consumer_goods_factor': -0.03, 'research_speed_factor': 0.02}, ('diplomacy', 'economy')),
    IdeaDef('allied_cargoes', 'Reconstruction Cargoes', 'Allied rebuilding agencies charter Malynean hulls for steel and cement.',
            {'industrial_capacity_dockyard': 0.04, 'stability_factor': 0.02}, ('rebuild', 'logistics')),
    # Ulysses
    IdeaDef('impact_dread', 'Waiting for Ulysses', 'Nobody knows where the fragments will fall.',
            {'stability_factor': -0.04, 'war_support_factor': 0.03}, ('meteor', 'telescope')),
    IdeaDef('hill_galleries', 'Galleries in the Hill', 'Shelter galleries cut into the southern hill, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.02}, ('shelter', 'tools')),
    IdeaDef('convoy_evacuation', 'Berth Lists for Evacuation', 'Every merchant hull has an evacuation berth list and a muster day.',
            {'naval_coordination': 0.05, 'stability_factor': 0.03}, ('refugees', 'navy')),
    IdeaDef('firebreaks', 'Firebreaks Through the Forest', 'Wide cleared strips with water points along roads and railway.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.08}, ('civil', 'tools')),
    IdeaDef('island_lifeboats', 'A Boat for Every Islander', 'Every islander has a boat, a muster point and a destination.',
            {'stability_factor': 0.03, 'navy_org_factor': 0.03}, ('refugees', 'fishing')),
    IdeaDef('district_stores', 'A Year of Stores', 'Grain, fuel, medicine and seed for a year in every district.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('shelter', 'economy')),
    IdeaDef('relief_berths', 'Spare Berths for Relief', 'Relief cargo travels at cost on every outbound voyage.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('medical', 'logistics')),
    # the turn of the century
    IdeaDef('graduate_return', 'Graduates Brought Home', 'Paid passage home and a guaranteed post for graduates abroad.',
            {'research_speed_factor': 0.04, 'consumer_goods_factor': 0.02}, ('science', 'logistics')),
    IdeaDef('island_school', 'The Island School', 'A secondary school with boarding for island children.',
            {'research_speed_factor': 0.02, 'stability_factor': 0.02}, ('science', 'civil')),
    IdeaDef('port_shares', 'A Listed Port Authority', 'Investors hold a minority of the port authority.',
            {'industrial_capacity_dockyard': 0.06, 'stability_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('public_port', 'A Public Port Authority', 'The port authority stays public and borrows on long bonds.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('assembly', 'navy')),
    IdeaDef('relief_charters', 'Relief Under Neutral Marks', 'Food, medicine and shelter materials for civilian ports on any side.',
            {'stability_factor': 0.02, 'naval_coordination': 0.03}, ('medical', 'peace')),
    IdeaDef('usean_rebuilding', 'Usean Rebuilding Cargoes', 'Reconstruction agencies in Usea charter trusted neutral hulls.',
            {'industrial_capacity_dockyard': 0.05, 'consumer_goods_factor': -0.02}, ('rebuild', 'navy')),
    IdeaDef('erusean_terms', 'Cargoes on Erusean Terms', 'Usean ports licensed by Erusean authorities.',
            {'consumer_goods_factor': -0.02, 'stability_factor': -0.01, 'political_power_gain': 0.05}, ('document', 'logistics')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('elected_council', 'Council of Ministers of Malynea',
           'A council of ministers chosen by the newly elected chamber, governing collectively, bound to win a vote for every '
           'budget and to hold the next election on the calendar. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('standing_board', 'Standing Board of the Three Districts',
           'A board of administrators from the capital district, the frontier district and the islands, serving fixed terms, '
           'deciding by majority and publishing its reasons, with no party seats and no election. Provisional gameplay office '
           'with no named holder.',
           'neutrality', 'centrism_na'),
    Office('readiness_committee', 'Committee of National Readiness',
           'A committee named by the national movement that governs by numbered decree, with parties suspended and the press '
           'under a censor. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('uncalled_election', 'The Ballot Nobody Called', (
        "The calendar in the cabinet office still shows an election every four years, and the last date it marks passed without "
        "a single polling hall opening. Malynea is governed by a National Administration that calls itself democratic and has "
        "kept the ballot suspended for longer than most young voters can remember. Its officials run the capital port, the forest "
        "districts and the six western islands competently enough that many citizens have stopped asking why.",
        "The opinion surveys explain why the question is dangerous. Half the respondents back the national movement, which wants "
        "a disciplined government of readiness. Almost as many back no party at all and trust the administrators they already "
        "know. The democrats who want the ballot restored are barely one in a hundred, and they know perfectly well that any "
        "election they force would be won by somebody else.",
        "The movement has announced a petition and claims it will gather signatures in every district and on every island. The "
        "administration can publish the election clause now and let the whole country argue about it, or wait to see how many "
        "names the movement really collects before it commits itself to anything. Both choices will be read as a statement of "
        "intent, and both will be quoted for years.",
    ), (
        Option('Publish the election clause in every newspaper.', (Stability(0.02), PP(-15))),
        Option('Wait for the movement to count its signatures.', (PP(20), Event('signature_count', 20))),
    ), picture=2),
    EventDef('signature_count', 'The Signatures Are Counted', (
        "The national movement delivers its petition to the administration in a column of trucks, box after box of signed sheets "
        "from the forest villages, the frontier district and the capital port. Even the island harbours have sent a few hundred "
        "names by the last hull of the month. The organisers announce their total on the steps of the building before the clerks "
        "have opened a single box.",
        "The clerks need three weeks. They find names entered twice, signatures from addresses no register has ever listed and "
        "whole pages filled in by one hand. They also find tens of thousands of genuine signatures from citizens who want "
        "something to change and have been given no other way of saying so. Both findings are true, and each camp intends to "
        "quote only one of them.",
        "The administration must now say what the count means. It can accept the petition as a fair expression of opinion and "
        "move the argument on to what should actually be done, or refer the count to the courts and let judges decide which "
        "names are real. Accepting concedes ground to the movement. Referring buys time and makes the movement angrier, in public "
        "and in the streets.",
    ), (
        Option('Accept the petition as it stands.', (WarSupport(0.03), Stability(-0.02))),
        Option('Refer the count to the courts.', (Stability(0.02), PP(-10))),
    ), picture=2),
    EventDef('hull_census', 'A Register of Hulls', (
        "The inspectors start at the capital port in the first week of the year, when most of the merchant fleet is laid up "
        "against the ice. They walk every deck, open every engine room and compare each hull with its line in the register. By "
        "the time the roadstead thaws they have taken the mail hull out to the island harbours and filled four ledgers with notes.",
        "The register proves generous. Several hulls listed as active are rusting at their moorings, a few were sold abroad "
        "without anyone in the port office noticing, and one exists only on paper. The rest are working ships, many of them old, "
        "crewed by masters who know the island lane and the foreign ports better than any official. For a country with no navy, "
        "they are the nearest thing it has to a fleet.",
        "The port authority now holds an honest list and an awkward question. Owners want the findings kept confidential, because "
        "charterers and insurers pay less for ships they know more about. The districts want them published, because these hulls "
        "carry their fuel and grain. The cabinet must decide who reads the ledgers, and the owners have already asked for a "
        "meeting.",
    ), (
        Option('Publish the register in full.', (Stability(0.02), PP(-10))),
        Option('Show the ledgers to the owners alone.', (PP(25), Stability(-0.01))),
    ), picture=0),
    EventDef('island_mailboat', 'Mail Day in the Islands', (
        "Mail day comes to the western islands once a week in good weather and less often in bad. The whole harbour turns out "
        "when the hull ties up: letters, newspapers, medicines, spare parts and the passengers who have waited on the mainland for "
        "a berth. For a few hours each island is connected to the country it belongs to, and then the hull sails on for the next "
        "harbour.",
        "The officials who ride the mail hull for the survey come back with a long list. No island has a hospital, a secondary "
        "school or a road a truck can climb in winter. Fuel is rationed whenever storms delay the lane. The island councils keep "
        "careful accounts of every promise the capital has made them over the years, and the accounts are not flattering to "
        "anyone.",
        "Islanders want to know what the survey will change. Some want their councils trusted with money of their own; others "
        "would settle for one official in the capital whose job is to answer their letters. The government must decide how to "
        "present the findings, knowing the islands will measure every later decision against whatever it says on this mail day.",
    ), (
        Option('Read the findings aloud in every island harbour.', (Stability(0.03), PP(-15))),
        Option('Send the findings to the ministries first.', (PP(25), Stability(-0.02))),
    ), picture=0),
    EventDef('forest_muster', 'Muster in the Forest', (
        "For the first time in years all four battalions muster together, at a forest camp an hour's drive from the capital port. "
        "The trucks arrive in a long column, a train brings the companies from the frontier district and officers count heads "
        "with clipboards in the cold. Inspectors from the administration walk along the lines and write down everything they see.",
        "What they see is an army built for a narrow job. The rifles are serviceable and the drivers know their trucks. There is "
        "no artillery, no engineer company and no aircraft, and the battalions have trained for guarding roads, escorting fuel "
        "and helping districts through winter storms rather than for fighting anyone. Officers argue over dinner about whether "
        "that is a weakness to fix or a role to perfect.",
        "The government must decide how to describe the muster to the country. It can say plainly that the army is a civil "
        "defence service that carries rifles, and ask the public to build on that, or present the battalions as a fighting force "
        "and accept that part of the promise is hollow. The frontier districts and the neighbours will hear the answer either way.",
    ), (
        Option('Call it a civil defence service, plainly.', (Stability(0.02), XP('army', 10))),
        Option('Present the battalions as a fighting force.', (WarSupport(0.03), PP(-10))),
    ), picture=1),
    EventDef('works_ledger', 'Seven Plants on One Page', (
        "The inventory teams return from both mainland districts with a single page that sums up the nation's industry, "
        "seven plants listed by name, output and payroll, the shipyard among them. Steel and oil come from deposits nearby, "
        "while almost every machine tool, chemical and spare part arrives by sea through the capital port. The page fits on one "
        "desk, and the ministers find that more alarming than reassuring.",
        "The details explain the alarm. The arms lines run below capacity for lack of orders, the civilian plants depend on "
        "imported parts that arrive late every winter, and the shipyard repairs other people's ships far more often than it "
        "builds anything of its own. The plants employ a large share of the mainland's workers, and every manager has a reason why "
        "his plant should be spared any change.",
        "The government wants the inventory to lead to a model for the decade, whether repair and spare parts or more arms lines. "
        "Before choosing, it must decide who sees the page. The managers want it kept inside the ministries. The district "
        "councils, whose voters work in the plants, want it read out and argued over in public before anything is decided.",
    ), (
        Option('Argue it out in public.', (Stability(-0.02), Research('industry', 0.5, 1))),
        Option('Hold the page within the ministries.', (PP(30), Stability(-0.01))),
    ), picture=0),
    EventDef('frontier_walk', 'Three Frontiers on Foot', (
        "The survey teams set out in early summer, when the forest tracks have dried and the hill passes are open. One team "
        "follows the coastal plain and the forest edge toward Baltica. A second climbs the southern hill to the line where the "
        "Seterano mountains begin. A third walks the forest and hills along the frontier with Valka, the longest and least "
        "visited of the three.",
        "They come back with blistered feet and a thick report. The customs posts are few, badly heated and staffed by officers "
        "who have not been relieved in years. Forest tracks cross the frontiers in places no official had seen before. Villages "
        "on both sides of each line marry, trade and quarrel with each other far more than with their own capitals. None of the "
        "frontiers is disputed, and none is well understood.",
        "The cabinet has to decide what to do with what the teams learned. Opening more crossings would help the frontier "
        "villages and trouble the customs office; leaving the frontiers as they are would keep them quiet and poorly watched. "
        "Whatever posture the government adopts toward its neighbours afterwards will rest on the answer it gives here.",
    ), (
        Option('Open more crossings for the frontier villages.', (Stability(0.02), PP(-10))),
        Option('Leave the frontiers as they are.', (PP(20), WarSupport(0.01))),
    ), picture=2),
    EventDef('war_charters', 'The Brokers Work Through the Night', (
        "Late in March 1995 the Belkan War begins, an ocean and a continent away from the cold coast. Malynea has no "
        "frontier anywhere near the fighting and no part in it. Within a week the charter brokers in the capital port are "
        "working through the night, because shippers everywhere have discovered that neutral hulls are suddenly scarce and that "
        "this small country owns a great many of them.",
        "Offers arrive faster than the owners can read them. Some are for grain and fuel bound for neutral ports. Some are for "
        "machine parts whose final destination is vague. A few are plainly for cargo that will end up at the front. Insurers "
        "raise their premiums on every voyage that goes anywhere near the war, and masters ask the port office what the "
        "government expects of them before they put their names to anything.",
        "The cabinet has to answer before the owners answer for it. It can tell the fleet that any lawful charter is acceptable "
        "and let the market sort out the rest, or ask owners to wait until the government writes clear rules on destinations and "
        "cargo. The first answer pays at once. The second may still pay later, and will certainly anger the brokers.",
    ), (
        Option('Any lawful charter is acceptable.', (PP(20), Stability(-0.02))),
        Option('Hold back until the rules are written.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Malynean response is gameplay', picture=0),
    EventDef('falling_sky', 'The Sky Above the Forests', (
        "The warning of December 1994 said only that Ulysses might hit the Earth. The announcement of April 1996 says that it "
        "will. Where the fragments will fall cannot yet be predicted, and the scientists on the radio admit it plainly. Malynea, "
        "like every other country, must now prepare for a danger whose location may not be known until the last weeks.",
        "The civil defence planners spread their maps across the table and see the country's weaknesses at once. The mainland is "
        "almost all forest, which could burn for weeks if hot fragments landed in a dry summer. The six western islands have no "
        "shelter worth the name and no exit except by sea. The only high ground is the southern hill, far from where most people "
        "live. The country's greatest asset is a merchant fleet that could carry thousands, if it were home and fuelled on the "
        "right day.",
        "The public is calmer than the planners expected and more frightened than it admits. Families buy lamps and tinned food, "
        "island councils ask about boats and forest villages ask about fire crews. The government must decide how fast to move "
        "and how much to say, knowing that a plan announced too early may be wrong and a plan announced too late may be useless.",
    ), (
        Option('Announce a plan within the month.', (WarSupport(0.02), Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Study every option before announcing.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Malynean preparations are gameplay',
        picture=1),
    EventDef('roche_vigil', 'A Vigil on the Cold Coast', (
        "Ulysses is due to cross inside the Earth's Roche limit on 8 July 1999. The northern summer night is short and "
        "pale, and in Malynea almost nobody sleeps through it. Civil defence crews sit by their radios in every district, convoys "
        "wait at their quays with crews aboard, and on the six islands families gather beside the boats assigned to them.",
        "Reports arrive from abroad all night, some careful and some wild, and the crisis room in the capital logs every one of "
        "them. A master far out on the island lane radios about lights on the horizon. The weather stations on the southern hill "
        "report nothing they can explain. By the early hours the duty officers have learned to write everything down and to "
        "believe nothing until it is confirmed twice.",
        "At dawn the government must decide what to do with a country that has spent the night waiting. It can keep the "
        "emergency rules in force until the picture is clear, or release the crews and convoys and let people go back to work "
        "while inspectors check every district. Either choice will be second-guessed, whatever the inspectors eventually report.",
    ), (
        Option('Keep the emergency rules for a week.', (WarSupport(0.02), Stability(-0.01))),
        Option('Send everyone back to work.', (Stability(0.02), PP(15))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no damage in Malynea is claimed', picture=1),
    EventDef('ten_year_report', 'Ten Years of Answers', (
        "The report runs to two volumes. It was written by a panel of judges, port officials, island councillors and district "
        "teachers, chosen by lot from lists every camp had agreed to. It covers the decade since the question of the suspended "
        "ballot was first asked, and it is blunt about every government that has held the seals in that time.",
        "The panel lists what the decade built, in roads, quays, drills and schools, and what it left undone. It credits the port "
        "with working through the Belkan War charters and the impact years. It faults successive governments for young graduates "
        "who leave and do not return, for frontier districts that feel forgotten and for decisions that still depend on too few "
        "offices in the capital.",
        "The government can print both volumes as written and spend a season answering for them, or issue its own summary first "
        "and release the full text later. The panel has already said that it will publish its own conclusions if anyone edits "
        "them, which narrows the choice more than the ministers would like. Whatever they decide, the panel's members are already giving interviews.",
    ), (
        Option('Print both volumes as written.', (Stability(0.03), PP(-20))),
        Option('Issue the government summary first.', (PP(30), Stability(-0.02))),
    ), picture=2),
    EventDef('relief_request', 'Manifests Open to Any Inspector', (
        "War on the Usean continent reaches the capital port the way distant wars always do, through the charter brokers. In the "
        "summer of 2003 Erusea seizes Stonehenge in neutral San Salvacion and fighting spreads across Usea. Within weeks relief "
        "agencies are asking for neutral hulls to carry food, medicine and tents to civilian ports, and the usual brokers are "
        "asking for hulls to carry anything at all.",
        "Malynean owners remember the Belkan War charters and draw different lessons from them. Some want the fleet kept well "
        "away from a war that is not Malynea's. Others point out that civilians on every side still need grain and medicine, and "
        "that a neutral fleet with open manifests is exactly what relief agencies cannot find elsewhere. Crews, as ever, ask who "
        "will pay if a hull is lost.",
        "The cabinet must answer the relief agencies first. It can offer Malynean tonnage for relief cargo only, under neutral "
        "markings and open to inspection by any party, or keep every hull off the Usean lanes until the war ends. The first "
        "course carries real risk. The second carries none, and leaves the country nothing to point to afterwards.",
    ), (
        Option('Offer tonnage for relief cargo only.', (WarSupport(0.02), PP(-10))),
        Option('Keep every hull off the Usean lanes.', (Stability(0.02), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Malynean response is gameplay', picture=0),
)

# --- branches ------------------------------------------------------------------------------------
BALLOT = Branch('pol', 'The Election Nobody Called', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_administration_sits', 'The National Administration Sits',
          "Malynea enters 1991 governed by a National Administration that calls itself democratic, keeps an election calendar on "
          "paper and has let no election take place. Its offices run the capital port, the two mainland districts and the western "
          "islands well enough. Asking who gave it the right costs the administration its quiet, and every faction wants an answer.",
          ('document', 'command'), reward=(Idea('caretaker_rule'), Event('uncalled_election'))),
    Focus('pol_election_clause', 'Reading the Election Clause',
          "Lawyers for the administration read the clause that sets an election every four years and the separate clause that "
          "lets the cabinet postpone it. Both are valid and they contradict each other. Publishing the reading forces the choice "
          "the administration has avoided for years: hold the ballot, hand power to the district boards, or let the movement in.",
          ('scales', 'ballot'), after=('pol_administration_sits',),
          reward=(PP(30), Tooltip('Opens three answers to the suspended ballot; only one can be taken.'))),
    Focus('pol_ballot_path', 'Reopen the Polling Halls',
          "The smallest camp in the country, the democrats, asks for the oldest remedy: name a date and hold the election the "
          "calendar already promises. Barely one voter in a hundred names them today, so the ballot would be won by someone else. "
          "They argue that a government chosen by a count still beats one chosen by nobody, whatever the count says.",
          ('ballot', 'assembly'), after=('pol_election_clause',), exclusive=('pol_board_path', 'pol_movement_path'),
          reward=(SwapIdea('caretaker_rule', 'ballot_promised'),)),
    Focus('pol_board_path', 'The District Boards Step Forward',
          "Almost half the country backs no party at all and trusts the administrators who keep the ferries, schools and depots "
          "running. Their spokesmen propose a standing board drawn from the three districts, governing by published rules instead "
          "of manifestos. It would be competent and predictable. Nobody would ever have voted for it, and its critics say so.",
          ('assembly', 'document'), after=('pol_election_clause',), exclusive=('pol_ballot_path', 'pol_movement_path'),
          reward=(SwapIdea('caretaker_rule', 'board_compact'),)),
    Focus('pol_movement_path', 'The Movement Brings Its Petition',
          "Half the respondents in the opinion surveys side with the national movement, which says a small country on a cold "
          "frontier needs discipline more than debate. Its petition asks the administration to hand power to a committee of "
          "national readiness. The movement promises order quickly. It does not say when, or whether, the ballot would return.",
          ('security', 'assembly'), after=('pol_election_clause',), exclusive=('pol_ballot_path', 'pol_board_path'),
          reward=(SwapIdea('caretaker_rule', 'movement_pressure'),)),
    Focus('pol_elected_council', 'The Council of Ministers Sits',
          "The overdue election is held, and a council of ministers chosen by the new chamber takes the seals of government. It "
          "governs collectively and must win a vote for every budget. The administration's officials stay on as civil servants. "
          "The council inherits a country in which its own supporters are a small minority and every other camp is watching.",
          ('ballot', 'document'), after=('pol_ballot_path',), cost=10,
          exclusive=('pol_standing_board', 'pol_readiness_committee'),
          reward=(Regime('elected_council'), Flag('path_ballot'))),
    Focus('pol_standing_board', 'Charter the Standing Board',
          "A written charter creates a standing board of administrators from the capital district, the frontier district and the "
          "islands. Members serve fixed terms, decide by majority and publish their reasons. No party sits on it and no election "
          "chooses it. The board is efficient, and it will be blamed for every bad winter as though it were one person.",
          ('assembly', 'scales'), after=('pol_board_path',), cost=10,
          exclusive=('pol_elected_council', 'pol_readiness_committee'),
          reward=(Regime('standing_board'), Flag('path_board'))),
    Focus('pol_readiness_committee', 'The Committee of National Readiness',
          "The administration steps aside for a committee named by the national movement. Parties are suspended, the press "
          "answers to a censor and the battalions report directly to the committee. The streets are quiet within a week. The "
          "committee calls this calm; its critics, those still free to speak, call it fear, and both agree it will be hard to undo.",
          ('security', 'command'), after=('pol_movement_path',), cost=10,
          exclusive=('pol_elected_council', 'pol_standing_board'),
          reward=(Regime('readiness_committee'), Flag('path_front'))),
    Focus('pol_ballot_rolls', 'Voter Rolls for the Three Districts',
          "The council sends registrars to every forest village, hill farm and island harbour to put each adult on a voter roll. "
          "Island registrars travel by convoy and wait weeks for a return voyage. The rolls cost a year of clerical work and "
          "reveal how many citizens the state had simply lost track of during the years without a ballot.",
          ('document', 'ballot'), after=('pol_elected_council',), exclusive=('pol_board_minutes', 'pol_committee_decrees'),
          reward=(SwapIdea('ballot_promised', 'ballot_restored'),)),
    Focus('pol_board_minutes', 'Minutes at Every Post Office',
          "The board posts its minutes, votes and reasons at every post office in the country within a week of each sitting, "
          "the island harbour offices included. Citizens cannot vote the board out, but they can read exactly what it did and "
          "why. The postings cost little and embarrass the board often, which is why its members accepted them so reluctantly.",
          ('communications', 'document'), after=('pol_standing_board',), exclusive=('pol_ballot_rolls', 'pol_committee_decrees'),
          reward=(SwapIdea('board_compact', 'board_minutes'),)),
    Focus('pol_committee_decrees', 'Readiness Instead of Statutes',
          "The committee governs by numbered decrees on rationing, travel, the press and service with the battalions. Each "
          "decree takes effect on the day it is printed. Officials who object are transferred to the islands. The decrees make "
          "the country quick to command and slow to correct, because nobody left in the room is paid to say no.",
          ('security', 'document'), after=('pol_readiness_committee',), exclusive=('pol_ballot_rolls', 'pol_board_minutes'),
          reward=(SwapIdea('movement_pressure', 'readiness_decrees'),)),
    Focus('pol_charter_court', 'A Court to Read the Charter',
          "Whatever government holds the seals, someone must decide what the charter means when ministers, boards or committees "
          "quarrel with the districts. A small constitutional court of judges with long terms is created to read it. Judges cost "
          "little to pay; their rulings will cost every future government something, and that is the point of having them.",
          ('scales', 'assembly'), after_any=('pol_elected_council', 'pol_standing_board', 'pol_readiness_committee'),
          reward=(Idea('charter_court'),)),
    Focus('pol_merit_service', 'Examinations for the Civil Service',
          "Posts in the port authority, the districts and the ministries have long been filled by recommendation. Open written "
          "examinations replace that habit, with papers marked by examiners who never see a candidate's name. Families who relied "
          "on a word from a cousin lose their advantage. The offices gain clerks chosen because they can do the work.",
          ('training', 'document'), after=('pol_charter_court',), reward=(Idea('merit_service'),)),
))

PORT = Branch('port', 'The Capital Port and Its Hulls', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('port_hull_register', 'Count the Hulls on the Register',
          "Malynea has no war fleet, but its merchant register is long for so small a country, and the capital port lives on hulls "
          "that carry other nations' cargo. Nobody has checked the register against the ships for years. A full count of hulls, "
          "owners and crews costs the port a winter of inspections and tells the government what it actually owns.",
          ('navy', 'document'), reward=(Idea('hull_register'), Event('hull_census'))),
    Focus('port_quay_roads', 'Roads Behind the Quays',
          "Cargo landed in the capital port leaves by one railway or by forest roads that turn to mud every spring and close "
          "under snow every winter. Paved roads from the quays to the depots and the rail yard let trucks move cargo in any "
          "season. The work costs a season of district budgets and several stretches of forest that the sawmills wanted.",
          ('logistics', 'tools'), after=('port_hull_register',), reward=(Build('infrastructure', 1, 0),)),
    Focus('port_open_charter', 'Charters for Any Shipper',
          "One school in the port authority wants Malynean hulls chartered to any shipper who pays, under light rules and low "
          "fees, so that foreign owners register here as well. Freight money would pour in. So would crews from abroad, ships of "
          "doubtful age and the risk that someone else's cargo drags the country's flag into someone else's quarrel.",
          ('logistics', 'economy'), after=('port_hull_register',), exclusive=('port_home_cargo',),
          reward=(Idea('open_charters'), Flag('open_registry'))),
    Focus('port_home_cargo', 'Malynean Cargoes Come First',
          "The other school wants every Malynean hull to carry Malynean steel, timber and fuel first, and foreign cargo only with "
          "spare tonnage. Fewer charters would come in and owners would earn less. The districts would get supplies on time in "
          "every season, and no foreign shipper could leave the islands waiting because a better rate turned up elsewhere.",
          ('logistics', 'industry'), after=('port_hull_register',), exclusive=('port_open_charter',),
          reward=(Idea('home_cargo_rule'), Flag('home_cargo'))),
    Focus('port_pilots', 'A Guild of Harbour Pilots',
          "The approaches to the capital port are shallow in places and dark for much of the winter. The pilots who know them have "
          "trained their own children for generations, with no standards and no pensions. A chartered guild with examinations, a "
          "pension fund and a duty roster costs the port authority money every year and buys it fewer groundings.",
          ('navy', 'medal'), after=('port_quay_roads',), reward=(Idea('pilot_guild'),)),
    Focus('port_winter_roadstead', 'An Open Roadstead in Winter',
          "Ice forms in the roadstead most winters and stays for weeks, closing the port just when the forest districts need fuel "
          "most. The authority buys a strengthened tug, marks a winter channel and writes rules for convoys that use it. The tug "
          "is costly to run and idle half the year, which the treasury will mention at every budget hearing.",
          ('navy', 'tools'), after=('port_quay_roads',), reward=(Idea('winter_roadstead'),)),
    Focus('port_island_slip', 'A Repair Slip in the Islands',
          "Hulls on the island lane break down far from the only yard, which sits in the capital port, and a disabled freighter can "
          "wait a month for a tow. A small repair slip at one of the island harbours keeps the lane working and gives island crews "
          "steady jobs. It costs the capital yard some orders and the port authority some of its control.",
          ('rebuild', 'navy'), after_any=('port_open_charter', 'port_home_cargo'), reward=(Build('dockyard', 1, 290),)),
    Focus('port_roadstead_radar', 'A Radar Above the Roadstead',
          "Convoys enter the roadstead in fog, snow and the long winter dark, guided by lights and the pilots' memories. A single "
          "radar on the shore lets the harbour office see every hull approaching and warn those that stray. It is the first radar "
          "the country has owned, and the battalions have already asked whether they may borrow it.",
          ('radar', 'navy'), after=('port_pilots',), reward=(Build('radar_station', 1, 0),)),
    Focus('port_submarine_word', 'Masters Hear of New Submarines',
          "In September 1991 a political convention in Cinigrad is told of new Yuktobanian submarines, built by the great power "
          "that lies beyond the Baltican frontier. Malynean masters on the island lane begin asking what else shares the sea with them. "
          "The port authority issues hydrophone sets and a reporting code to merchant hulls. The sets are cheap; the unease is not.",
          ('submarine', 'communications'), after=('port_hull_register',),
          requires=(After('1991.9.2'), HasGlobal('ac_bwr_cinigrad')),
          reward=(TimedIdea('lane_watch', 365), Research('naval_equipment', 0.5, 1))),
    Focus('port_masters_school', 'A School for Convoy Masters',
          "Convoy masters learn their trade at sea from older masters, which works until the older masters retire. A school in "
          "the capital port teaches station-keeping, winter navigation, radio procedure and what to do when help does not arrive. "
          "It takes teaching hulls out of service and turns out masters who all know the same rules.",
          ('training', 'navy'), after=('port_winter_roadstead',), reward=(Idea('masters_school'),)),
))

ISLANDS = Branch('isl', 'The Six Western Islands', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('isl_six_harbours', 'Six Harbours Without Roads',
          "Far to the west of the mainland, across open sea, Malynea holds six hill islands. Each has a harbour and a quay, and "
          "none has a road worth the name. Islanders depend on the convoy lane for fuel, mail, doctors and news. Counting what "
          "each island lacks costs nothing but honesty, and the list will embarrass every ministry in the capital.",
          ('refugees', 'navy'), reward=(Idea('island_isolation'), Event('island_mailboat'))),
    Focus('isl_harbour_tracks', 'Tracks Up From the Harbours',
          "The island harbours sit at the foot of steep hills, and the farms and houses climb above them. Graded tracks from each "
          "quay to the upper settlements let a truck replace a mule. Island crews do the work in summer, paid from a capital "
          "budget that would much rather spend the money on the forest roads of the mainland.",
          ('tools', 'civil'), after=('isl_six_harbours',), reward=(Build('infrastructure', 1, 290),)),
    Focus('isl_harbour_radios', 'A Radio in Every Harbour Office',
          "Today an island learns of a storm, a strike or a sick child's evacuation when the next hull ties up. A radio in every "
          "harbour office links the six islands to each other and to the capital port day and night. The sets are cheap, but the "
          "operators must be trained, and that takes a year of courses on the mainland.",
          ('communications', 'civil'), after=('isl_six_harbours',), reward=(Idea('island_radio'),)),
    Focus('isl_own_purse', 'Island Councils Keep a Purse',
          "One answer to the islands' complaints lets each island council raise its own harbour dues and spend them on its own "
          "tracks, clinics and schools. Islanders would set their own priorities. The capital would lose revenue and some of its "
          "control, and the poorest islands would discover exactly how small their purse really is.",
          ('assembly', 'economy'), after=('isl_harbour_radios',), exclusive=('isl_capital_rule',),
          reward=(SwapIdea('island_isolation', 'island_councils'),)),
    Focus('isl_capital_rule', 'Prefects From the Capital Port',
          "The other answer sends a prefect from the capital to each island with a budget, a staff and the authority to settle "
          "disputes. Decisions would come quicker and spending would follow the national plan. Island councils would become "
          "advisory, and islanders would be governed well or badly by people who arrived on the same hull as the mail.",
          ('command', 'civil'), after=('isl_harbour_radios',), exclusive=('isl_own_purse',),
          reward=(SwapIdea('island_isolation', 'island_prefects'),)),
    Focus('isl_cannery', 'A Cannery for the Island Catch',
          "Island boats land more fish in summer than the islands can eat or the lane can carry fresh. A cannery at one of the "
          "harbours preserves the surplus for the mainland and for export. It needs power, tin plate and a reliable hull every "
          "week. It would be the first factory most islanders have ever worked in, and by far the noisiest.",
          ('fishing', 'industry'), after=('isl_harbour_tracks',), reward=(Build('industrial_complex', 1, 290),)),
    Focus('isl_landing_strip', 'A Landing Strip in the Islands',
          "A hull takes days to reach the islands; a light aircraft takes hours. A graded landing strip on a level shoulder of one "
          "island lets the capital fly in doctors and fly out patients, and gives the mail a second route. Malynea owns no "
          "aircraft fit for the work yet, so the strip is a promise as much as a field.",
          ('runway', 'medical'), after=('isl_harbour_tracks',), reward=(Build('air_base', 1, 290),)),
    Focus('isl_hospital_rota', 'The Hospital Ship Rota',
          "No island has a hospital, and an operation means a voyage to the capital port. A converted freighter fitted with a "
          "surgery, beds and a dentist's chair sails a fixed round of the six islands. It takes one hull out of the charter market "
          "for good and puts a doctor within a week's reach of every islander.",
          ('medical', 'navy'), after_any=('isl_own_purse', 'isl_capital_rule'), reward=(Idea('hospital_rota'),)),
    Focus('isl_island_deputies', 'Island Deputies Take Their Seats',
          "With the ballot restored, the islands elect deputies of their own to the new chamber for the first time. They arrive on "
          "the same convoy, sit together and vote as a bloc on anything touching the lane, the harbour dues or the hospital ship. "
          "Ministers find them hard to ignore and harder still to satisfy.",
          ('ballot', 'fishing'), after_any=('isl_own_purse', 'isl_capital_rule'), requires=(HasFlag('path_ballot'),),
          reward=(Idea('island_deputies'), Stability(0.02))),
    Focus('isl_ring_road', 'A Road Around the Island Hills',
          "The tracks from the harbours become roads that circle each island's hills, joining farms, the cannery and the landing "
          "strip. Blasting through rock costs more than any mainland road and takes two summers. When it is done an islander can "
          "cross an island in an hour, and the island economies begin to resemble small mainland districts.",
          ('bridge', 'tools'), after=('isl_cannery',), reward=(Build('infrastructure', 2, 290),)),
    Focus('isl_watch_radar', 'A Watch Radar for the Islands',
          "The islands sit alone in open sea, with no mainland coast to watch their approaches. A radar on the high ground of one "
          "island covers the lane, the landing strip and the harbours, and reports to the capital over the harbour radios. It "
          "warns of squalls as well as strangers, which is the reason islanders accept the noise of its generator.",
          ('radar', 'refugees'), after=('isl_landing_strip',), reward=(Build('radar_station', 1, 290),)),
))

DEFENCE = Branch('def', 'Four Battalions in the Forest', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('def_battalion_roll', 'Count the Four Battalions',
          "The army of Malynea is four infantry battalions in two formations, with rifles, trucks and trains but no artillery, "
          "engineers or aircraft. Its role is civil defence: hold roads, guard the port and help the districts in bad winters. "
          "Counting what the battalions really have costs the officers their excuses and tells the government what it can defend.",
          ('security', 'document'), reward=(Idea('thin_service'), Event('forest_muster'))),
    Focus('def_forest_roads', 'Hold the Forest Roads',
          "The first doctrine fights where the country is strongest: in the forests that cover most of the mainland. Small units "
          "would hold the road junctions, block the tracks and wait for any intruder to tire. It suits infantry without heavy "
          "weapons. It also leaves the open coastal plains and the capital shore to whatever the battalions can spare.",
          ('security', 'bridge'), after=('def_battalion_roll',), exclusive=('def_southern_hill', 'def_capital_shore'),
          reward=(Idea('forest_screens'),)),
    Focus('def_southern_hill', 'Garrison the Southern Hill',
          "The second doctrine looks south, to the one hill province where the mainland meets the mountains of Seterano and the "
          "hills of Valka. A permanent garrison there would watch both frontiers and train in the hardest country. It costs the "
          "forest districts their companies and asks a quarter of the army to winter far from any town.",
          ('command', 'security'), after=('def_battalion_roll',), exclusive=('def_forest_roads', 'def_capital_shore'),
          reward=(Idea('hill_garrison'),)),
    Focus('def_capital_shore', 'Defend the Capital Shore',
          "The third doctrine puts the army where the country's wealth is: the capital port, its quays and the rail yard behind "
          "them. Trenches, wire and anti-aircraft positions would ring the shore, with the battalions billeted close by. The "
          "capital would sleep easier. The frontier districts would see soldiers only on parade days.",
          ('security', 'navy'), after=('def_battalion_roll',), exclusive=('def_forest_roads', 'def_southern_hill'),
          reward=(Idea('shore_lines'),)),
    Focus('def_reserve_cards', 'A Reserve Card for Every Adult',
          "Every adult who has served receives a card naming a depot, a company and a day to report. The cards are printed in the "
          "capital, posted by district and checked once a year. Most will never be used. The few days a year it takes to keep "
          "them current let four battalions become many more within a week.",
          ('document', 'training'), after=('def_battalion_roll',), reward=(Idea('reserve_cards'),)),
    Focus('def_winter_drill', 'Training in the Long Winter',
          "Mainland winters bring snow, blizzards and weeks of darkness, and the battalions have trained mostly in summer. Winter "
          "drills on skis, in snow shelters and with frozen trucks teach them to move when the country is at its hardest. The "
          "first winters cost frostbite, broken engines and letters from parents. Later winters cost less.",
          ('training', 'shelter'), after=('def_reserve_cards',), reward=(Idea('winter_drill'),)),
    Focus('def_rail_depots', 'Depots Along the One Railway',
          "The country's only railway runs from the capital port along the coast toward the Baltican frontier. Depots of food, "
          "fuel and ammunition at each station mean a battalion can move by train and find supplies waiting. The depots cost "
          "money to stock and guard, and they tell anyone with a map where the army expects to fight.",
          ('rail', 'logistics'), after_any=('def_forest_roads', 'def_southern_hill', 'def_capital_shore'),
          reward=(Idea('rail_depots'),)),
    Focus('def_frontier_wardens', 'Wardens on the Frontiers',
          "The readiness committee raises frontier wardens from the movement's own volunteers and posts them to the forest edges "
          "and the southern hill. They patrol, check papers and report to the committee rather than to the army. Officers "
          "distrust them and frontier villages fear them. The committee trusts them completely, which is what worries everyone else.",
          ('security', 'medal'), after=('def_reserve_cards',), requires=(HasFlag('path_front'),),
          reward=(Idea('frontier_wardens'),)),
    Focus('def_civil_corps', 'A Corps for Civil Defence',
          "Civil defence is the army's stated role, so the government gives it a corps of its own: firefighters, rescue teams, "
          "medics and shelter wardens trained alongside the battalions. Reservists who will never carry a rifle can serve here. "
          "The corps costs training time and equipment, and it gives every district people who know what to do first.",
          ('shelter', 'medical'), after=('def_winter_drill',), reward=(Idea('civil_defence_corps'),)),
    Focus('def_engineer_roads', 'Field Engineers for the Frontier',
          "The battalions have no engineers, so roads and bridges in the frontier district depend on civilian contractors who "
          "leave when the weather turns. A small engineer school trains soldiers to build and repair roads, culverts and bridges, "
          "and its first class works on the frontier district's roads. The army gains a skill; the contractors lose a client.",
          ('bridge', 'training'), after=('def_rail_depots',),
          reward=(Build('infrastructure', 1, 328), Research('engineers_tech', 0.5, 1))),
    Focus('def_mountain_companies', 'Mountain Companies for the Passes',
          "The army already teaches a handful of soldiers to climb, a skill kept up from older governments. Mountain companies "
          "drawn from hill-country recruits would serve on the southern hill and the passes toward Seterano and Valka. They need "
          "ropes, skis and patient instructors, and give the army one unit that can go where no truck can follow.",
          ('training', 'command'), after=('def_winter_drill',), reward=(Research('infantry_weapons', 0.5, 1), XP('army', 15))),
))

WORKS = Branch('ind', 'Steel, Oil and the Arms Lines', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('ind_works_inventory', 'What the Seven Plants Make',
          "Malynea's industry is three civilian plants, three arms lines and one shipyard, split between the capital district and "
          "the frontier district. Steel and oil come from the ground nearby; almost everything else arrives by sea. An honest "
          "inventory of what each plant makes, wastes and needs costs the managers their comfortable reports.",
          ('industry', 'document'), reward=(Idea('works_audit'), Event('works_ledger'))),
    Focus('ind_steel_beds', 'Steel From the Capital District',
          "The capital district holds the larger steel deposits, worked by small mines that sell to whoever arrives first. Long "
          "contracts with the domestic works and a survey of the deeper beds would steady both prices and output. Mine owners "
          "lose the freedom to sell abroad when prices rise, and the works lose the excuse that they cannot plan.",
          ('industry', 'tools'), after=('ind_works_inventory',),
          reward=(Idea('steel_contracts'), Research('excavation_tech', 0.5, 1))),
    Focus('ind_coastal_oil', 'Pumping the Coastal Oil',
          "Both mainland districts hold modest oil, pumped by old wells near the coast. The fuel would cover more of the "
          "country's needs if the wells were deepened and linked to a tank farm at the port. The work costs money the treasury "
          "would rather give the port, and the forest around the wells pays a price of its own.",
          ('economy', 'tools'), after=('ind_works_inventory',), reward=(Idea('coastal_wells'),)),
    Focus('ind_repair_first', 'Spare Parts and Repair Yards',
          "One economic model builds on what Malynea already does well: keeping ships, trucks and machines running. A new civilian "
          "plant in the frontier district would make spare parts and run repair contracts for foreign hulls calling at the port. "
          "Growth would be steady and modest. The arms lines would stay as they are, small and short of orders.",
          ('rebuild', 'tools'), after_any=('ind_steel_beds', 'ind_coastal_oil'), exclusive=('ind_fourth_line',),
          reward=(Build('industrial_complex', 1, 328), Idea('repair_economy'))),
    Focus('ind_fourth_line', 'A Fourth Arms Line',
          "The other model adds a fourth arms line in the frontier district, beside the two already there, making rifles and "
          "trucks for the battalions and for export. Arms would become the largest employer outside the port. Orders would depend "
          "on other people's insecurity, and the new hall would stand within sight of the Baltican frontier.",
          ('missile', 'industry'), after_any=('ind_steel_beds', 'ind_coastal_oil'), exclusive=('ind_repair_first',),
          reward=(Build('arms_factory', 1, 328), Idea('arms_lines'))),
    Focus('ind_rolling_stock', 'Rolling Stock for the Single Line',
          "The one railway is short and busy, and its locomotives and wagons are older than most of their drivers. Rebuilding the "
          "rolling stock in the port workshops keeps freight moving from the quays toward the frontier district. Each rebuilt "
          "engine is out of service for months, so the line runs short for a year before it runs better.",
          ('rail', 'tools'), after=('ind_works_inventory',),
          reward=(TimedIdea('rail_overhaul', 365), Research('train_tech', 0.5, 1))),
    Focus('ind_timber', 'Timber From the Forest Districts',
          "Forest covers most of the mainland, and the sawmills that cut it are small and scattered. A timber board grading logs, "
          "setting replanting rules and selling abroad through the port would earn steady foreign money. Mill owners resent the "
          "grading. The forest districts gain wages and the country gains an export that depends on no one's war.",
          ('economy', 'logistics'), after=('ind_coastal_oil',), reward=(Idea('timber_trade'),)),
    Focus('ind_tyre_works', 'Tyres From Malynean Rubber',
          "Both mainland districts yield some rubber, which today leaves the country raw and comes back as imported tyres. A tyre "
          "and belting works would supply the battalions' trucks, the railway and the port cranes. The plant is small, the rubber "
          "is uneven and the first tyres wear quickly. Every set made at home is one fewer bought abroad.",
          ('industry', 'logistics'), after=('ind_steel_beds',),
          reward=(Idea('tyre_works'), Research('synth_resources', 0.5, 1))),
    Focus('ind_district_power', 'Power Lines to the Frontier District',
          "The frontier district's plants run on their own generators, which fail in every hard winter. A power line from the "
          "capital district, cut through the forest beside the railway, would let the plants work through the cold. It costs a "
          "summer of clearing and a winter of complaints about bills, and it makes two districts one grid.",
          ('communications', 'industry'), after=('ind_timber',), reward=(Idea('district_power'),)),
    Focus('ind_board_tenders', 'Contracts Under Board Rules',
          "Under the standing board, every public contract above a modest value is tendered by written rules, scored by examiners "
          "and published with the winning price. Contractors who used to win by knowing the right official must now win by "
          "bidding lower. The rules slow purchases by weeks and save money the board can show in its minutes.",
          ('scales', 'economy'), after=('ind_works_inventory',), requires=(HasFlag('path_board'),),
          reward=(Idea('board_tenders'),)),
    Focus('ind_snow_trucks', 'Trucks Built for Snow',
          "Imported trucks are built for roads that stay dry, and in a Malynean winter they spend more time in workshops than on "
          "the road. Fitting them with heaters, chains, higher clearance and engines that start in deep cold makes them useful in "
          "every season. The work is fiddly and the first designs fail, but the battalions and districts both need them.",
          ('logistics', 'shelter'), after_any=('ind_repair_first', 'ind_fourth_line'),
          reward=(Research('logistics_tech', 0.5, 2),)),
))

NEIGHBOURS = Branch('nbr', 'Baltica, Seterano and Valka', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('nbr_frontier_walk', 'Walking the Land Frontiers',
          "Malynea has three land neighbours: Baltica to the east along the coastal plain and the forest, Seterano to the south "
          "and south-east beyond its mountains, and Valka to the west and south-west through forest and hills. Officials walk "
          "every stretch of the three frontiers and record each crossing, track and customs post. No line changes.",
          ('document', 'bridge'), reward=(Idea('frontier_survey'), Event('frontier_walk'))),
    Focus('nbr_equal_distance', 'Equal Distance From Every Neighbour',
          "The first posture offers every neighbour identical terms at every crossing, one tariff and one set of papers, and no "
          "private understanding with any of them. Nobody can accuse Malynea of favouring one frontier over another. Nobody owes Malynea a "
          "favour either, and a small country without friends must solve every crisis on its own.",
          ('scales', 'peace'), after=('nbr_frontier_walk',), exclusive=('nbr_small_neighbours', 'nbr_sea_first'),
          reward=(Idea('equal_distance'),)),
    Focus('nbr_small_neighbours', 'Talks Among the Small Neighbours',
          "The second posture proposes regular meetings with the governments of Baltica, Seterano and Valka on weather warnings, "
          "frontier crossings, forest fires and trade. Malynea makes the offer and cannot know who will come. Even partial "
          "attendance gives the small countries of the region a place to speak, at the price of larger powers' attention.",
          ('diplomacy', 'assembly'), after=('nbr_frontier_walk',), exclusive=('nbr_equal_distance', 'nbr_sea_first'),
          reward=(Idea('neighbour_consults'),)),
    Focus('nbr_sea_first', 'Face the Sea, Not the Frontiers',
          "The third posture argues that Malynea's future lies on the convoy lanes rather than its land frontiers. Diplomacy would "
          "follow the cargo, with trade offices in the ports where Malynean hulls call and correct but minimal relations next "
          "door. The port would gain friends across the sea. The frontier districts would feel forgotten and say so.",
          ('diplomacy', 'navy'), after=('nbr_frontier_walk',), exclusive=('nbr_equal_distance', 'nbr_small_neighbours'),
          reward=(Idea('sea_orientation'),)),
    Focus('nbr_eastern_railhead', 'The Railhead on the Eastern Plain',
          "The railway from the capital port ends on the eastern coastal plain, a short distance from the Baltican frontier, while "
          "Baltica's own line reaches its harbour on the far side. Malynea improves the roads, yards and sidings at its end of the "
          "gap. Whether the two lines ever meet is for two governments to settle; this answers only Malynea's half.",
          ('rail', 'bridge'), after=('nbr_frontier_walk',), reward=(Build('infrastructure', 1, 328),)),
    Focus('nbr_fire_towers', 'Fire Towers Along the Valka Forest',
          "Forest runs unbroken across the western frontier into Valka, and a summer fire does not stop at a customs post. A line "
          "of watchtowers on the Malynean side, staffed through every dry season, spots smoke early and calls the district fire "
          "crews. The towers cost wages for lonely work and protect timber, villages and the railway alike.",
          ('telescope', 'security'), after=('nbr_frontier_walk',), reward=(Idea('fire_watch'),)),
    Focus('nbr_hill_weather', 'Weather Reports for the Hill Passes',
          "Weather on the southern hill and in the mountains toward Seterano changes faster than anywhere else on the mainland. A "
          "small weather service with stations on the hill and a daily broadcast warns farmers, drivers and the battalions of "
          "storms. Its forecasts are free to anyone who listens, including travellers on the far side of the frontier.",
          ('telescope', 'communications'), after=('nbr_frontier_walk',), reward=(Idea('weather_service'),)),
    Focus('nbr_frontier_radar', 'A Radar Over the Frontier District',
          "Whatever posture the government chooses, the frontier district sits where Baltica and Seterano meet Malynea, with the "
          "railhead and two arms lines inside it. A radar on its higher ground watches the air above all three. It sees aircraft "
          "that would never announce themselves, and it needs a staff the district must house and feed.",
          ('radar', 'security'), after_any=('nbr_equal_distance', 'nbr_small_neighbours', 'nbr_sea_first'),
          reward=(Build('radar_station', 1, 328),)),
))

CHARTERS = Branch('war', 'Hulls for Hire in the Belkan War', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_charter_spring', 'Charter Rates in the Spring of 1995',
          "The Belkan War begins in late March 1995, half a world from the cold coast. Within days the charter market finds that neutral "
          "hulls are scarce and valuable, and offers for Malynean tonnage arrive at rates the port has never seen. Owners are "
          "delighted. The government must decide how a neutral merchant nation behaves when war makes its ships precious.",
          ('logistics', 'missile'), requires=(After('1995.3.25'),),
          reward=(Idea('war_charter_boom'), Event('war_charters'))),
    Focus('war_neutral_colours', 'Neutral Colours on Every Hull',
          "Every Malynean merchant hull has its name, its flag and the word neutral painted large on both sides and lit at night. "
          "Masters carry papers listing the cargo and its destination. None of this guarantees safety. It leaves a belligerent "
          "who sinks a Malynean ship no honest excuse, and gives the government a case to press afterwards.",
          ('peace', 'navy'), after=('war_charter_spring',), reward=(Idea('neutral_markings'),)),
    Focus('war_neutral_ports', 'Sail for Any Neutral Port',
          "The first answer lets masters accept any charter to a port not at war, wherever its cargo may finally end up. Freight "
          "money flows in all spring. Some cargoes will reach the fighting by a second or third hull, and every belligerent's "
          "consul in the capital port will keep a list of the Malynean names that carried them.",
          ('logistics', 'diplomacy'), after=('war_neutral_colours',), exclusive=('war_home_waters',),
          reward=(Idea('neutral_port_trade'),)),
    Focus('war_home_waters', 'Hold the Fleet in Home Waters',
          "The second answer keeps Malynean hulls on the home lanes, the island run and voyages to ports far from the war until a "
          "peace is signed. Owners lose the best rates in a generation and some threaten to reflag abroad. The fleet stays whole, "
          "the islands stay supplied and no Malynean crew dies in a war that belongs to others.",
          ('peace', 'shelter'), after=('war_neutral_colours',), exclusive=('war_neutral_ports',),
          reward=(Idea('home_waters'),)),
    Focus('war_crews_abroad', 'Crews Signed On Abroad',
          "With charters open to any shipper, Malynean hulls now outnumber Malynean sailors, and owners sign crews in foreign "
          "ports to fill the berths. The port authority sets rules for wages, papers and training so that every hull still sails "
          "to one standard. The crews bring skills and languages, and a few bring trouble the harbour police must handle.",
          ('refugees', 'logistics'), after=('war_charter_spring',), requires=(HasFlag('open_registry'),),
          reward=(Idea('foreign_crews'),)),
    Focus('war_home_holds', 'Home Cargoes Fill the Holds',
          "Under the rule that home cargo comes first, the war's high rates are a temptation owners may not accept. Instead the "
          "government guarantees them a fixed rate for carrying Malynean steel, timber and fuel while the war lasts, and the "
          "treasury pays the difference between that rate and the market. The districts never run short.",
          ('economy', 'logistics'), after=('war_charter_spring',), requires=(HasFlag('home_cargo'),),
          reward=(Idea('home_holds'),)),
    Focus('war_after_lumen', 'Rates Fall After the Lumen Treaty',
          "The Belkan War ends in June 1995 with the treaty concluded at Lumen. Charter rates sink over the summer and the offers for "
          "Malynean tonnage dry up. Owners who borrowed against wartime earnings now face their banks. The government must "
          "manage the landing: some help for owners, and no pretence that the boom was ever going to last.",
          ('peace', 'document'), after_any=('war_neutral_ports', 'war_home_waters'), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_charter_boom'), Stability(0.02))),
    Focus('war_belkan_lanes', 'Charter Lanes Toward Belka',
          "Where Belka emerges from the war holding the advantage, its ports start buying again within the year. "
          "Belkan shippers look for neutral tonnage that kept its distance during the fighting, and Malynean hulls qualify. Every "
          "contract will be read by the governments that lost, which keep their own lists of who carried what.",
          ('diplomacy', 'economy'), after=('war_after_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(Idea('belkan_routes'),)),
    Focus('war_allied_cargo', 'Reconstruction Cargoes for the Allies',
          "Where Belka loses the war, the governments that fought it set about rebuilding what the fighting broke. Their "
          "reconstruction agencies charter neutral hulls in large numbers for steel, cement and machinery. Malynean owners can "
          "bid. The contracts carry inspection clauses and pay slowly, but they pay, and none of them carries shells.",
          ('rebuild', 'logistics'), after=('war_after_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Idea('allied_cargoes'),)),
    Focus('war_civil_lessons', 'Lessons for the Civil Defence Service',
          "Officers in the capital collect what they can about the fighting around Belka from newspapers, attaches' letters and "
          "the stories crews bring home. They study how quickly a small country's roads and bridges became targets and how "
          "civilians fared where nobody had planned for them. The findings go into the civil defence manual.",
          ('document', 'shelter'), after=('war_neutral_colours',), reward=(Research('land_doctrine', 0.5, 1), XP('army', 10))),
))

SKY = Branch('sky', 'Ulysses and the Forest Districts', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_falling_sky', 'The Forest Under a Falling Sky',
          "The FCU announcement of April 1996 turns Ulysses from a possibility into a certainty, more than a year after the "
          "first astronomical warning. Nobody can say where the fragments will fall. Malynea has forests that could burn for weeks, islands reachable "
          "only by sea and a civil defence service of four battalions. It must plan for a danger it cannot locate.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),), reward=(Idea('impact_dread'), Event('falling_sky'))),
    Focus('sky_hill_galleries', 'Galleries Under the Southern Hill',
          "The first plan cuts shelter galleries into the rock of the southern hill, the only high ground on the mainland, with "
          "stores, air and water for weeks. It protects whoever reaches it. The hill lies far from the capital port and the "
          "forest villages, so the plan depends on roads and trains still working when everything else has failed.",
          ('shelter', 'tools'), after=('sky_falling_sky',), exclusive=('sky_sea_evacuation',),
          reward=(Idea('hill_galleries'),)),
    Focus('sky_sea_evacuation', 'Evacuation by Convoy',
          "The second plan uses what Malynea has most of: merchant hulls. If the fragments threaten the mainland coast or the "
          "islands, convoys would carry families to safer ports or out to open sea until the danger passes. The plan needs every "
          "hull in home waters on the right day, and some foreign port willing to take them in.",
          ('refugees', 'navy'), after=('sky_falling_sky',), exclusive=('sky_hill_galleries',),
          reward=(Idea('convoy_evacuation'),)),
    Focus('sky_firebreaks', 'Firebreaks Through the Forests',
          "Burning fragments in a dry summer could set the mainland forests alight faster than any crew could respond. Wide "
          "firebreaks cut along the roads and the railway, with water points and fire crews, would slow a blaze and keep escape "
          "routes open. The clearing costs timber the mills wanted to sell and leaves scars that take decades to soften.",
          ('civil', 'tools'), after=('sky_falling_sky',), reward=(Idea('firebreaks'), Build('infrastructure', 1, 0))),
    Focus('sky_island_lifeboats', 'An Evacuation Plan for the Islands',
          "The six western islands have no deep shelter and no way off except by sea. A plan assigns every islander a boat, a "
          "muster point and a destination, and keeps fuel stocked at every quay. The drills are rehearsed each summer. Islanders "
          "do them with grim good humour and a sharp eye on whether the capital really means it.",
          ('refugees', 'fishing'), after=('sky_falling_sky',), reward=(Idea('island_lifeboats'),)),
    Focus('sky_year_stores', 'A Year of Stores in Every District',
          "If the impact closes the sea lanes, the country cannot feed itself for long. Grain, fuel, medicine and seed for a year "
          "are stored in every district and on every island, and rotated as they age. The stores tie up money and warehouse "
          "space the port wanted for cargo. They also let families believe the government has a plan.",
          ('shelter', 'economy'), after_any=('sky_hill_galleries', 'sky_sea_evacuation'), reward=(Idea('district_stores'),)),
    Focus('sky_mail_plane', 'A Mail Plane for the Islands',
          "The planners notice that in any emergency the islands would be days away by hull. A small airfield near the capital and "
          "a light aircraft for mail, doctors and urgent passengers cut that to hours. Malynea has no aircraft of its own, so the "
          "first pilots must train abroad, and the field must be ploughed clear every winter morning.",
          ('runway', 'communications'), after=('sky_island_lifeboats',), reward=(Build('air_base', 1, 0),)),
    Focus('sky_july_vigil', 'Watching the July Sky',
          "The night of 8 July 1999, when Ulysses crosses inside the Earth's Roche limit, finds the civil defence corps on duty, the "
          "convoys waiting at their quays and every radio in the country switched on. This focus records only that the country was as ready as "
          "it could make itself, and what the government chose to tell its people.",
          ('meteor', 'shelter'), after=('sky_year_stores',), requires=(After('1999.7.8'),), reward=(Event('roche_vigil'),)),
    Focus('sky_district_check', 'Inspecting Every District',
          "After the long night the government sends inspectors to every district, island and depot to look for damage, fires and "
          "casualties, and to tell people what they found. Whatever they report, the waiting is over. The emergency rules end, "
          "the stores begin to flow back into the shops and the convoys return to charter work.",
          ('document', 'civil'), after=('sky_july_vigil',), reward=(RemoveIdea('impact_dread'), Stability(0.03))),
    Focus('sky_relief_berths', 'Spare Berths for Relief Cargo',
          "The impact years leave many countries in need, and the convoy fleet has hulls to spare once the emergency rules end. "
          "The government sets aside berths on every outbound voyage for relief cargo such as medicine, tents and grain, carried "
          "at cost. Owners grumble about the lost revenue. The country earns a reputation it could never buy.",
          ('medical', 'logistics'), after=('sky_district_check',), reward=(Idea('relief_berths'),)),
))

CENTURY = Branch('cent', 'Malynea at the Turn of the Century', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_ten_year_report', 'The Ten-Year Report',
          "A decade after the question of the suspended ballot was first asked, an independent panel reports on what the years "
          "built and what they left undone: roads, quays, drills and schools on one side, departures and neglect on the other. "
          "The report becomes the basis of every political argument of the new decade, whoever holds the seals.",
          ('document', 'assembly'), requires=(After('2001.1.1'),), reward=(Event('ten_year_report'), PP(20))),
    Focus('cent_graduate_tickets', 'A Return Ticket for Graduates',
          "Young Malyneans study abroad because the country has no university large enough to train engineers, doctors and ship "
          "officers, and too many stay away. A scheme pays for the voyage home, waives the first years of tax and guarantees a "
          "post in the port, the districts or the hospital service. It is expensive and works slowly.",
          ('science', 'logistics'), after=('cent_ten_year_report',), reward=(Idea('graduate_return'),)),
    Focus('cent_island_school', 'A Secondary School in the Islands',
          "Island children who want more than primary schooling must board in the capital from the age of twelve. A secondary "
          "school in the islands, with teachers rotated from the mainland and boarding for children from the other harbours, keeps "
          "families together. It costs teachers' bonuses and a hull's worth of supplies every year.",
          ('science', 'civil'), after=('cent_ten_year_report',), reward=(Idea('island_school'),)),
    Focus('cent_listed_port', 'Sell Shares in the Port Authority',
          "One proposal sells a minority stake in the port authority to investors and spends the money on dredging, warehouses "
          "and cranes. Private owners would push for efficiency and higher dues. The state would keep control on paper and lose "
          "some of it in practice, and the islands would worry that their lane is nobody's priority.",
          ('economy', 'navy'), after=('cent_ten_year_report',), exclusive=('cent_public_port',), reward=(Idea('port_shares'),)),
    Focus('cent_public_port', 'Keep the Port in Public Hands',
          "The other proposal keeps the port authority wholly public and funds its works from dues and long bonds. Decisions stay "
          "with the government and the districts, and the island lane stays protected. Investment arrives more slowly, the "
          "cranes stay old a little longer and the port competes with rivals that have more money behind them.",
          ('assembly', 'navy'), after=('cent_ten_year_report',), exclusive=('cent_listed_port',), reward=(Idea('public_port'),)),
    Focus('cent_usean_lanes', 'Charter Lanes Into a Usean War',
          "During the summer of 2003 the Erusean seizure of Stonehenge in San Salvacion turns into a continental war across Usea. "
          "Malynea is far from that continent, but its hulls carry cargo on lanes that reach it. The government must decide "
          "whether neutrality means staying away or carrying what civilians on every side still need.",
          ('logistics', 'peace'), after=('cent_ten_year_report',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(Event('relief_request'),)),
    Focus('cent_relief_marks', 'Relief Charters Under Neutral Marks',
          "Malynean hulls offer to carry food, medicine and shelter materials to civilian ports on any side of the Usean war, "
          "under neutral markings and open manifests that any party may inspect. Owners earn little. Crews take real risks on "
          "lanes where submarines and aircraft do not read manifests. The country gains a role no arms contract could buy.",
          ('medical', 'peace'), after=('cent_usean_lanes',), reward=(Idea('relief_charters'),)),
    Focus('cent_isaf_peace', 'Charters After the Allied Peace',
          "In this outcome the war in Usea ends with the ISAF victorious, and the continent turns to rebuilding. Reconstruction "
          "agencies need neutral tonnage for steel, cement and machinery. Malynean hulls that carried relief during the war are "
          "known and trusted on those lanes. The contracts pay slowly, but steadily and for years.",
          ('rebuild', 'navy'), after=('cent_usean_lanes',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(Idea('usean_rebuilding'),)),
    Focus('cent_erusean_peace', 'Cargoes Under Erusean Terms',
          "In this outcome Erusea comes out of the war in control of the continent, and Usean ports reopen under its rules. "
          "Erusean authorities license neutral shippers and set the terms of every call. Malynean hulls can take the licences or "
          "leave the Usean lanes to others. Either way the fleet must decide whose rules it will sail under.",
          ('document', 'logistics'), after=('cent_usean_lanes',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Idea('erusean_terms'),)),
    Focus('cent_era_close', 'What the Districts Ask For Next',
          "The last focus of the era asks the districts, the islands and the port what they want from the coming years, and "
          "prints their answers side by side without editing. The replies disagree on almost everything except the convoy lane. "
          "The government gains no new power from the exercise, only a clear list of what it will be judged on.",
          ('assembly', 'ballot'), after_any=('cent_listed_port', 'cent_public_port'), requires=(After('2005.1.1'),),
          reward=(Stability(0.03), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are written separately.'))),
))

BRANCHES = (BALLOT, PORT, ISLANDS, DEFENCE, WORKS, NEIGHBOURS, CHARTERS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('break_roadstead_ice', 'Break a Channel Through the Ice',
                'Runs the strengthened tug day and night to hold a channel open through the worst of the winter. Repeatable '
                'once a winter.',
                25, (TimedIdea('ice_channel', 90),), requires=(Completed('port_winter_roadstead'),), cooldown=365),
    DecisionDef('island_supply_run', 'An Extra Supply Run to the Islands',
                'Sends an extra convoy of fuel, flour and medicine to the six islands ahead of the storms. Repeatable twice a '
                'year.',
                30, (TimedIdea('supply_run', 120),), requires=(Completed('isl_harbour_radios'),), cooldown=180),
    DecisionDef('reserve_year_group', 'Call a Year Group to the Depots',
                'Brings one year group of reservists to their depots for a fortnight of drill. Employers object; repeatable '
                'once a year.',
                30, (TimedIdea('reserve_callout', 60), XP('army', 10)), requires=(Completed('def_reserve_cards'),),
                cooldown=365),
    DecisionDef('capital_runway', 'Lengthen the Capital Airfield',
                'Extends the runway of the small field near the capital so heavier transports can land. A one-time works '
                'programme.',
                60, (Build('air_base', 1, 0),), requires=(Completed('sky_mail_plane'),)),
    DecisionDef('island_road_finish', 'Finish the Island Hill Roads',
                'Pays island crews for one more summer of blasting and grading on the hill roads. A one-time charge on the '
                'capital budget.',
                50, (Build('infrastructure', 1, 290),), requires=(Completed('isl_ring_road'),)),
    DecisionDef('foreign_charter_agents', 'Send Charter Agents Abroad',
                'Posts port authority agents in foreign ports for a season to win charters for Malynean hulls. Repeatable once '
                'a year.',
                35, (TimedIdea('charter_drive', 120),), requires=(HasFlag('open_registry'),), cooldown=365),
    DecisionDef('dry_season_watch', 'Staff the Fire Towers Early',
                'Puts the forest fire towers and crews on full watch before the dry season begins. Repeatable once a year.',
                20, (TimedIdea('fire_season', 90),), requires=(Completed('nbr_fire_towers'),), cooldown=365),
)
