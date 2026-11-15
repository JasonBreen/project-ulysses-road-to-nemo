"""Baltica (BAL): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party with
elections every 48 months, the last in November 1987; democratic 70 and neutrality 28
percent popularity; war support 0.70), the unnamed National Administration office, the
single 1991 state with its victory point Silvius, the map (terrain, railway, winter weather,
neighbours) and the global flags other mod scripts already set. Official: ACES Chronicle rows
used only as date anchors for distant pressures, each cited by its exact key. Everything else,
including every Baltican choice, office, idea, building, decision and event, is provisional
gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='BAL', name='Baltica', root='world', package='bal',
                  themes=('security', 'industry', 'ballot'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with elections_allowed = yes, election_frequency 48 and '
           'last_election 1987.11.9, so the next ballot falls due in November 1991; popularities democratic 70, neutrality 28, '
           'fascism 1, communism 1; stability 0.5 and war support 0.70; three research slots including tech_mountaineers and '
           'early_fighter. The starting leader is the unnamed National Administration office (BAL_ac_government_office, '
           'centrism), whose 1991 holder has not been established. The tree never names a holder.',
           'mod/2985041246/history/countries/BAL - Baltica.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Baltican Republic (democratic and neutrality), Baltican Union (communism), Baltican State '
           '(fascism), Grand Duchy of Baltica (monarchism); adjective Baltican. The three political answers all keep the '
           'Republic names; no union, state or grand duchy path is offered.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: one 1991 state, 321 (capital), captioned Baltica, category large_town with five shared slots all filled '
           '(3 arms, 2 civilian); infrastructure 3, air base 1, a naval base in coastal province 1628 and a supply node and '
           'victory point Silvius (value 20) in province 797. Terrain from map/definition.csv: hills (797), plains (1235, 1628, '
           '4771; the last two coastal) and forest (3679). One level-2 railway runs 797-1235-1628. Land neighbours, computed '
           'from map/provinces.bmp: YUK (states 216 and 274) along 797, 1235 and 4771; MAY (328) along 1628 and 3679; SET '
           '(356, mountain provinces) along 797. Sea frontage on 1628 and 4771. '
           'Strategic region 236 has winters well below freezing with snow and blizzards. Neighbour state names and captions '
           'are not used as place names; no place other than Silvius is named.',
           'mod/2985041246/history/states/321-State_321.txt; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/strategicregions/236-XXX.txt; tools/regional_labels/labels.json'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small territorial service; 2 civilian, 3 military and 0 naval '
           'factories; two infantry formations (four battalions), infantry-only civil defence with combat aviation and combat '
           'navy deliberately absent; stocks of 800 infantry equipment, 560 motorized equipment and 24 trains; 60 convoys; oil '
           '4, rubber 2, steel 6; research priority Physical Sustainment (transport, equipment replacement, affordable '
           'service). Fiscal figures are fictional calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/economy_v2/profiles.json; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour context only: Yuktobania starts 1991 with communism ruling at 70 percent popularity and about seventy '
           'states; Malynea and Seterano start with democratic ruling parties and three and five states. No neighbour response '
           'to any Baltican policy is asserted; Baltican offers are unilateral.',
           'mod/2985041246/history/countries/YUK - Yuktobania.txt; mod/2985041246/history/countries/MAY - Malynea.txt; '
           'mod/2985041246/history/countries/SET - Seterano.txt'),
    Source('Official',
           'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, Yuktobania. Used only '
           'for the coast watch leaf, which also requires the mod global flag ac_bwr_cinigrad; no Baltican role is claimed.',
           '1991 / 09.02'),
    Source('Official', 'Date anchor: the IAU announces that Ulysses may strike the Earth. Background to the asteroid branch.',
           '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Opening of the distant-war branch; Baltica takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Nearly all of Ustio falls under Belkan control. Cited only as the example a Baltican staff study '
           'reads; no Baltican role is claimed.', '1995 / 03.30'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Date gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Date gate of the asteroid branch '
           'opening; where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Date gate of the Roche night focus; '
           'no damage in Baltica is claimed.', '1999 / 07.08'),
    Source('Official', 'Osea and Yuktobania cooperate to convert the Arkbird into a debris-clearing platform. Date gate and '
           'premise of the thaw focus; no Baltican role is claimed.', '1999 / 10.08'),
    Source('Official', 'Erusea invades the neutral country of San Salvacion and seizes Stonehenge. Background to the Usean '
           'war focus, which also requires the mod global flag ac_ucw_war_started.', '2003 / SUMMER'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_bwr_cinigrad (common/scripted_effects/ac_belkan_record.txt); '
           'belka_won_belkan_war and belka_lost_belkan_war (events/Belka.txt); ac_ucw_war_started, ac_ucw_war_averted, '
           'ac_ucw_outcome_isaf_victory and ac_ucw_outcome_erusean_victory (common/scripted_effects/ac_ucw.txt). Each reaction '
           'is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/common/scripted_effects/ac_belkan_record.txt; mod/2985041246/events/Belka.txt; '
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Baltican focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in state 321, '
           'which has no free shared slot, so only infrastructure, air base and radar levels are added.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the November ballot
    IdeaDef('expiring_mandate', 'The Expiring Mandate', 'The mandate from the ballot of November 1987 runs out in November 1991.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('ballot', 'document')),
    IdeaDef('public_gallery', 'The Public Gallery', 'Budget debates are open to the press and to anyone who queues for a seat.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'scales')),
    IdeaDef('chamber_mandate', 'Ministers Answer to Deputies', 'A cabinet chosen by the elected chamber, bargaining for every budget.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('works_charter', 'The Works Charter', 'Directors of the works and the harbour claim a share of government.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': 0.05, 'stability_factor': -0.02}, ('industry', 'document')),
    IdeaDef('defence_watch', 'Readiness Before Politics', 'The territorial staff argues that a small country cannot afford a changeable government.',
            {'army_org_factor': 0.04, 'political_power_gain': 0.10, 'stability_factor': -0.03}, ('security', 'command')),
    IdeaDef('ministerial_code', 'The Ministerial Code', 'Written answers within a month, published contracts and a register of gifts.',
            {'stability_factor': 0.08, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('scales', 'document')),
    IdeaDef('works_wage_pact', 'The Wage Pact', 'Wages come before any payment to owners or creditors, with a worker seat on each council.',
            {'stability_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.05, 'consumer_goods_factor': -0.02}, ('industry', 'scales')),
    IdeaDef('readiness_charter', 'The Readiness Charter', 'Published conditions under which the defence council would return power to ministers.',
            {'stability_factor': 0.05, 'army_org_factor': 0.05, 'political_power_gain': 0.10}, ('security', 'document')),
    IdeaDef('audit_office', 'The Republic Audit Office', 'An independent office audits every ministry and every works contract each year.',
            {'political_power_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.03}, ('scales', 'economy')),
    IdeaDef('campaign_season', 'A Campaign Season', 'Ministers campaign, the chamber argues and decisions wait for the count.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'communications')),
    # Silvius and the provinces
    IdeaDef('province_register', 'The Province Register', 'Households, wells, stoves and roads in all five provinces, on one register.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('document', 'civil')),
    IdeaDef('hill_waterworks', 'Water Below the Frost Line', 'Mains laid deep enough that the upper streets no longer queue at frozen cisterns.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.03}, ('civil', 'tools')),
    IdeaDef('dense_hill', 'Silvius Builds Upward', 'Tall blocks and covered walkways keep the capital on its defensible hill.',
            {'production_speed_buildings_factor': 0.05, 'army_core_defence_factor': 0.04, 'stability_factor': 0.01}, ('civil', 'security')),
    IdeaDef('plain_quarter', 'Houses on the Plain', 'Low houses and gardens along the railway, with fast trains to the works.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.05, 'consumer_goods_factor': 0.02}, ('civil', 'rail')),
    IdeaDef('works_heat', 'Heat From the Works', 'Furnace heat piped from the arsenal works into the nearest housing blocks.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.03}, ('industry', 'civil')),
    IdeaDef('winter_volunteers', 'The Snow Volunteers', 'Street brigades, paid in fuel vouchers, dig out what the ploughs miss.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('civil', 'shelter')),
    IdeaDef('snow_brigade_call', 'The Brigades Are Out', 'Every volunteer brigade is clearing lanes, doors and stops this week.',
            {'production_speed_infrastructure_factor': 0.15, 'stability_factor': 0.02}, ('civil', 'tools')),
    IdeaDef('provincial_clinics', 'A Clinic in Every Province', 'A doctor, a radio and a snow vehicle within an hour of every household.',
            {'stability_factor': 0.04, 'war_support_factor': 0.02}, ('medical', 'civil')),
    # the arsenal works
    IdeaDef('arsenal_ledger', 'The Arsenal Ledger', 'Every order, wage and debt of the works, on paper for the first time.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.05}, ('industry', 'document')),
    IdeaDef('common_order_book', 'One Order Book', 'The three arms lines stop underbidding each other for the same foreign contract.',
            {'production_factory_max_efficiency_factor': 0.03, 'consumer_goods_factor': -0.02}, ('document', 'economy')),
    IdeaDef('export_arsenal', 'Arsenal for Export', 'All three arms lines at full rate, selling the surplus to licensed buyers.',
            {'production_speed_arms_factory_factor': 0.10, 'consumer_goods_factor': -0.03}, ('missile', 'economy')),
    IdeaDef('converted_lines', 'Converted Lines', 'Two arms lines retooled for tractors, pumps, wagons and heating plant.',
            {'consumer_goods_factor': -0.05, 'industrial_capacity_factory': -0.03}, ('rebuild', 'industry')),
    IdeaDef('reserve_arsenal', 'The Reserve Arsenal', 'Lines kept below capacity, stocks built for the territorial service, tooling ready to surge.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': 0.03}, ('industry', 'security')),
    IdeaDef('licensed_exports', 'Published Export Licences', 'Every export licence names the buyer, the weapon and the quantity.',
            {'production_speed_arms_factory_factor': 0.12, 'industrial_capacity_factory': 0.04, 'political_power_factor': 0.03}, ('missile', 'document')),
    IdeaDef('civil_order_book', 'Orders at Home', 'Converted lines fill domestic orders for wagons, pumps and boilers.',
            {'consumer_goods_factor': -0.08, 'stability_factor': 0.03}, ('rebuild', 'rail')),
    IdeaDef('surge_arsenal', 'The Surge Arsenal', 'Twice a year the reserve arsenal proves it can wake to full rate in a week.',
            {'industrial_capacity_factory': 0.08, 'production_factory_efficiency_gain_factor': 0.05, 'consumer_goods_factor': 0.02}, ('industry', 'medal')),
    IdeaDef('spares_first', 'Spares First', 'A standing quota of gaskets, axles and barrels keeps the motor pool on the road.',
            {'supply_consumption_factor': -0.05, 'repair_speed_factor': 0.10}, ('tools', 'logistics')),
    IdeaDef('board_quotas', 'Quotas From the Board', 'The board that governs the country also sets the quotas of its factories.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': -0.02}, ('command', 'industry')),
    IdeaDef('works_councils', 'Works Councils', 'An elected council at every plant sees the order book, the safety record and the wage bill.',
            {'stability_factor': 0.04, 'production_factory_efficiency_gain_factor': -0.02}, ('assembly', 'industry')),
    IdeaDef('works_debt_cleared', 'Free of the Old Creditors', 'The debts found by the audit are paid, and with them the conditions on every loan.',
            {'political_power_factor': 0.05, 'industrial_capacity_factory': 0.03}, ('economy', 'scales')),
    IdeaDef('overtime_lines', 'Overtime on Every Line', 'Every line runs extra shifts to clear the order backlog.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'tools')),
    # steel, oil and rubber
    IdeaDef('survey_maps', 'The New Survey Maps', 'Drilling cores and survey maps show what the state can mine and pump.',
            {'production_speed_buildings_factor': 0.03, 'research_speed_factor': 0.02}, ('document', 'tools')),
    IdeaDef('home_inputs', 'Inputs Kept at Home', 'Steel and crude reserved for the works at prices below the world market.',
            {'production_factory_efficiency_gain_factor': 0.04, 'consumer_goods_factor': 0.02}, ('industry', 'logistics')),
    IdeaDef('export_earnings', 'Hard Currency Earnings', 'Surplus steel and crude sold through the harbour at world prices.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': 0.05}, ('economy', 'navy')),
    IdeaDef('fuel_reserve', 'The Buried Fuel Reserve', 'Buried tanks around Silvius hold fuel for two winters.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.02}, ('shelter', 'logistics')),
    IdeaDef('price_board', 'The Price Board', 'One board publishes the domestic prices of fuel and steel each quarter.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('scales', 'economy')),
    # the harbour
    IdeaDef('harbour_register', 'The Harbour Register', 'Every quay, crane and Baltican hull surveyed and listed.',
            {'consumer_goods_factor': -0.02, 'naval_coordination': 0.03}, ('navy', 'document')),
    IdeaDef('ice_tugs', 'Tugs With Ice Bows', 'Two reinforced tugs keep a channel open through the winter.',
            {'naval_speed_factor': 0.03, 'navy_org_factor': 0.04}, ('navy', 'tools')),
    IdeaDef('open_quays', 'Open Quays', 'Low dues, quick inspections and bonded warehouses for every flag.',
            {'consumer_goods_factor': -0.05, 'stability_factor': -0.02}, ('navy', 'economy')),
    IdeaDef('inspected_quays', 'The Inspection Regime', 'Every crate opened or scanned, every manifest matched to the order book.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': -0.02}, ('security', 'navy')),
    IdeaDef('coast_alert', 'Coast Watch Doubled', 'Masters report every unusual contact off the coast for a year.',
            {'naval_coordination': 0.05, 'air_detection': 0.05}, ('submarine', 'radar')),
    IdeaDef('mates_school', 'Baltican Mates and Engineers', 'Merchant officers trained at home, with an ice navigation course.',
            {'naval_coordination': 0.04, 'research_speed_factor': 0.02}, ('training', 'navy')),
    IdeaDef('rail_head_cranes', 'Cranes at the Rail Head', 'Modern cranes and sidings halve the time a hull spends at the quay.',
            {'production_speed_buildings_factor': 0.03, 'consumer_goods_factor': -0.02}, ('rail', 'navy')),
    # the territorial service
    IdeaDef('muster_lessons', 'Lessons of the Winter Muster', 'What one January muster taught the service about itself.',
            {'army_org_factor': 0.03, 'training_time_army_factor': -0.05}, ('training', 'security')),
    IdeaDef('driver_school', 'The Depot Driving School', 'Infantrymen trained as drivers and mechanics for the depot trucks.',
            {'supply_consumption_factor': -0.03, 'army_speed_factor': 0.03}, ('logistics', 'training')),
    IdeaDef('hill_redoubt', 'The Hill Redoubt', 'The service concentrated on Silvius and its hills, with the works inside the perimeter.',
            {'army_core_defence_factor': 0.06, 'army_defence_factor': 0.03}, ('security', 'command')),
    IdeaDef('frontier_screens', 'Frontier Screens', 'Small companies along every land frontier and on the mountain passes.',
            {'army_org_factor': 0.04, 'attrition': -0.05}, ('security', 'radar')),
    IdeaDef('plain_reserve', 'The Plain Reserve', 'A motorised reserve astride the railway on the inland plain.',
            {'army_speed_factor': 0.04, 'planning_speed': 0.05}, ('logistics', 'security')),
    IdeaDef('hill_fortress', 'Stores in the Rock', 'Ammunition, food and medical stores in galleries cut into the hill.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.05, 'supply_consumption_factor': -0.05}, ('shelter', 'security')),
    IdeaDef('mountain_screens', 'Mountain Companies', 'Ski and climbing companies that can live a week in snow caves.',
            {'army_org_factor': 0.06, 'attrition': -0.10, 'experience_gain_army_factor': 0.05}, ('training', 'medal')),
    IdeaDef('motor_reserve', 'The Night Drivers', 'A reserve that can reach any frontier in hours, at night and in snow.',
            {'army_speed_factor': 0.08, 'planning_speed': 0.10}, ('logistics', 'medal')),
    IdeaDef('reserve_register', 'The Reserve Register', 'One register of reservists, matched to the tax rolls and payrolls.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.03}, ('document', 'security')),
    IdeaDef('winter_kit', 'Winter Kit for Every Reservist', 'Layered clothing, felt boots, white smocks and heated tents.',
            {'attrition': -0.08, 'army_org_factor': 0.03}, ('training', 'shelter')),
    IdeaDef('council_inspectors', 'Inspections by the Council', 'The officers who govern also inspect, promote and fund the service.',
            {'army_org_factor': 0.05, 'experience_gain_army_factor': 0.08, 'stability_factor': -0.02}, ('command', 'medal')),
    IdeaDef('reserve_week', 'The Reserve Is Out', 'One year group of reservists is in the depots for a week of winter drill.',
            {'army_org_factor': 0.03, 'army_core_defence_factor': 0.03}, ('training', 'security')),
    IdeaDef('reserve_cadre', 'The Reserve Cadre', 'A core of long-service instructors keeps the reserve current in the new century.',
            {'training_time_army_factor': -0.08, 'experience_gain_army_factor': 0.05}, ('training', 'command')),
    # the airfield
    IdeaDef('interceptor_flight', 'The Interceptor Flight', 'A small flight of interceptors bought abroad to police Baltican skies.',
            {'air_superiority_efficiency': 0.05, 'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('ground_air_defence', 'Guns Over the Hill', 'Anti-aircraft batteries on the hill and around the harbour, tied to radar.',
            {'static_anti_air_damage_factor': 0.10, 'air_defence_factor': 0.04}, ('security', 'radar')),
    IdeaDef('pilot_contracts', 'Cadets on Foreign Courses', 'Baltican cadets trained abroad, returning as instructors.',
            {'experience_gain_air_factor': 0.10, 'air_mission_efficiency': 0.04}, ('air', 'training')),
    IdeaDef('radar_ring', 'The Radar Ring', 'Radar posts on the hills and the coast, linked to one control room.',
            {'static_anti_air_damage_factor': 0.15, 'air_detection': 0.10}, ('radar', 'command')),
    IdeaDef('air_reporting', 'Air Reports Across the Frontiers', 'Unidentified aircraft near the frontiers reported to any neighbour that listens.',
            {'air_detection': 0.08}, ('radar', 'diplomacy')),
    # the neighbours
    IdeaDef('frontier_office', 'The Frontier Desk', 'One desk in the foreign office follows all three land frontiers and the coast.',
            {'political_power_gain': 0.05, 'stability_factor': 0.01}, ('diplomacy', 'document')),
    IdeaDef('long_frontier_trade', 'Trade on the Long Frontier', 'Customs posts open longer and the works sell across the Yuktobanian line.',
            {'consumer_goods_factor': -0.05, 'stability_factor': -0.01}, ('diplomacy', 'economy')),
    IdeaDef('small_republic_talks', 'Talks With the Small Republics', 'Regular consultations offered to Malynea and Seterano on practical matters.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('diplomacy', 'assembly')),
    IdeaDef('even_handed', 'No Favourites', 'The same customs rules and visa terms for every neighbour.',
            {'army_core_defence_factor': 0.04, 'stability_factor': 0.02}, ('scales', 'security')),
    IdeaDef('joint_customs', 'Common Customs Forms', 'Baltican customs accept Yuktobanian forms, so a cleared cargo needs only a seal check.',
            {'consumer_goods_factor': -0.07, 'production_speed_infrastructure_factor': 0.05}, ('logistics', 'document')),
    IdeaDef('neighbour_network', 'The Open Weather Network', 'Frontier weather, fire and avalanche reports broadcast every hour.',
            {'stability_factor': 0.05, 'air_detection': 0.05}, ('communications', 'peace')),
    IdeaDef('declared_neutrality', 'Declared Neutrality', 'No sales to any party in a dispute among neighbours, and no foreign force on Baltican land.',
            {'army_core_defence_factor': 0.08, 'stability_factor': 0.04, 'production_speed_arms_factory_factor': -0.05}, ('peace', 'security')),
    IdeaDef('pass_patrols', 'Patrols on the Passes', 'Huts, radios and rescue teams on the Baltican side of the mountain passes.',
            {'attrition': -0.04, 'stability_factor': 0.02}, ('shelter', 'medical')),
    IdeaDef('attache_corps', 'The Attache Corps', 'Attaches in every neighbouring capital report on armies, harvests and prices.',
            {'planning_speed': 0.05, 'political_power_gain': 0.05}, ('diplomacy', 'communications')),
    # the Belkan War years
    IdeaDef('war_prices', 'War Prices', 'Fuel, grain and insurance cost more while war burns around Belka.',
            {'consumer_goods_factor': 0.04, 'political_power_gain': -0.05}, ('economy', 'missile')),
    IdeaDef('war_embargo', 'No Arms to Belligerents', 'No Baltican arms to any country at war or to any buyer who might resell.',
            {'stability_factor': 0.04, 'production_speed_arms_factory_factor': -0.05}, ('peace', 'scales')),
    IdeaDef('war_orders', 'The Wartime Order Book', 'Licensed buyers from any country not under embargo fill the order book.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04, 'stability_factor': -0.03}, ('missile', 'industry')),
    IdeaDef('war_risk_pool', 'The War Risk Pool', 'The state insures Baltican hulls against war risk at fixed rates.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('navy', 'scales')),
    IdeaDef('belkan_credit', 'Belkan Credit Lines', 'Belkan buyers and banks favour suppliers who stayed out of the war.',
            {'production_speed_arms_factory_factor': 0.06, 'research_speed_factor': 0.02}, ('economy', 'diplomacy')),
    IdeaDef('allied_buyers', 'Buyers From the Allied Side', 'New buyers for parts once bought in Belka, with inspection clauses attached.',
            {'industrial_capacity_factory': 0.04, 'political_power_gain': -0.03}, ('diplomacy', 'industry')),
    # Ulysses
    IdeaDef('impact_planning', 'Planning for Impact', 'Every ministry plans for a strike nobody can locate.',
            {'stability_factor': -0.02, 'war_support_factor': 0.03}, ('meteor', 'document')),
    IdeaDef('rock_shelters', 'Shelter in the Rock', 'Heated galleries in the rock of Silvius, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'meteor')),
    IdeaDef('dispersal_plan', 'The Dispersal Plan', 'Sirens in every village and heated shelters spread across all five provinces.',
            {'stability_factor': 0.03, 'air_detection': 0.08}, ('telescope', 'refugees')),
    IdeaDef('cold_stores', 'The Cold Stores', 'Grain, seed and medicine held across the provinces for a year without imports.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('shelter', 'logistics')),
    IdeaDef('deep_wards', 'Wards Below Ground', 'Operating theatres and critical wards in reinforced basements.',
            {'stability_factor': 0.03, 'surrender_limit': 0.05}, ('medical', 'shelter')),
    IdeaDef('relief_column', 'The Relief Column', 'Trucks, field kitchens, heated tents and medical teams ready to go where invited.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05, 'training_time_army_factor': -0.03}, ('refugees', 'medical')),
    # the new century
    IdeaDef('thaw_budget', 'The Thaw Budget', 'A budget planned on the hope that great-power cooperation lasts.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': -0.02}, ('peace', 'economy')),
    IdeaDef('peace_dividend', 'The Reserve Dividend', 'Shorter reserve service, with the savings spent on schools and housing.',
            {'consumer_goods_factor': -0.05, 'research_speed_factor': 0.03, 'training_time_army_factor': 0.05}, ('civil', 'economy')),
    IdeaDef('steady_reserve', 'A Whole Reserve', 'Full reserve service and winter exercises kept, with savings spent on equipment.',
            {'army_core_defence_factor': 0.06, 'consumer_goods_factor': 0.02}, ('security', 'training')),
    IdeaDef('usean_premiums', 'Usean War Premiums', 'Insurance and freight toward Usea cost more while the war lasts.',
            {'consumer_goods_factor': 0.03, 'stability_factor': -0.02}, ('navy', 'missile')),
    IdeaDef('calm_lanes', 'Calm Lanes to Usea', 'With war averted in Usea, Baltican hulls sail on ordinary premiums.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('navy', 'peace')),
    IdeaDef('usean_rebuild', 'Wagons for Usea', 'Orders for wagons, pumps and spare parts for a rebuilding continent.',
            {'industrial_capacity_factory': 0.04, 'stability_factor': 0.02}, ('rebuild', 'rail')),
    IdeaDef('erusean_terms', 'Under Erusean Trade Terms', 'Access to Usean ports in return for inspections and preferred prices.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': -0.03}, ('diplomacy', 'scales')),
    IdeaDef('graduate_bursaries', 'Bursaries to Stay', 'Student fees repaid for every year a graduate works in Baltica.',
            {'research_speed_factor': 0.04}, ('science', 'training')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('chamber_cabinet', 'Cabinet of the Elected Chamber',
           'A cabinet chosen by the elected chamber of the Baltican Republic and answerable to it, governing collectively with the '
           'election calendar written into ordinary law. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('works_board', 'Board of the National Works',
           'A standing board of the directors of the arsenal works, the civilian plants and the harbour company, holding the '
           'government seals while the chamber hears the budget twice a year. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('defence_council', 'Council of Territorial Defence',
           'A council of senior officers of the territorial service holding executive power for a declared period of readiness, '
           'with the chamber kept for budgets and petitions. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('november_ballot', 'The November Ballot', (
        "In November 1991 the mandate from the ballot of 1987 runs out, and Baltica votes. Polling stations open in schools and "
        "works canteens across the five provinces, with ploughs out on the roads because the first snow has already fallen on "
        "the plain. The National Administration that has governed under the democratic banner will not survive the count in its "
        "present form, and everyone in Silvius knows it.",
        "Seven voters in ten support the democratic parties, which agree that ministers should answer to the chamber and "
        "disagree about almost everything else. Most of the rest follow a non-aligned establishment of works directors, harbour "
        "owners and senior officers who distrust coalitions and prefer competence to debate. Nearly every family has someone on "
        "the reserve list or the works payroll, and both groups expect the next government to remember them.",
        "Before any answer is chosen, the Administration must settle how the result will be received. It can publish the count "
        "from every polling station by the next morning, inviting challenges and recounts, or certify the national result first "
        "and release the local figures once a government has been formed. The four years that follow begin with this choice.",
    ), (
        Option('Publish every count by morning.', (Stability(0.03), PP(-15))),
        Option('Certify the national result first.', (PP(35), Stability(-0.02))),
    ), picture=2),
    EventDef('winter_ledger', 'A Register Taken in Winter', (
        "The register clerks set out in January, because that is when farmers, fishermen and forest crews are at home. They "
        "travel by rail to the harbour, by sledge into the forest province and on foot up the steepest streets of Silvius. Their "
        "ledgers record households, wells, stoves, roads and the distance to the nearest doctor, and the clerks come back with "
        "frostbite and complaints in roughly equal measure.",
        "The figures confirm what everyone suspected and nobody had written down. The capital and its hill hold the works, the "
        "offices and the best roads. The inland plain feeds the country and carries its only railway. The forest province, "
        "on the Malynea frontier, has the worst roads and the darkest winters, and the two coastal plains depend entirely on "
        "the harbour and the weather.",
        "The planners propose to rank the provinces by need and fund roads, clinics and heating in that order. Deputies from "
        "Silvius point out that the works pay most of the taxes. Deputies from the forest point out that their children walk to "
        "school in the dark. The cabinet must decide whether the ranking is printed for everyone to argue over, or used quietly "
        "inside the planning office.",
    ), (
        Option('Print the ranking for everyone.', (Stability(0.02), PP(-15))),
        Option('Use it quietly inside the planning office.', (PP(25), Stability(-0.01))),
    ), picture=0),
    EventDef('arsenal_ledgers', 'What the Works Really Cost', (
        "The auditors have walked every hall of the arsenal works and both civilian plants, and their report is thicker than "
        "anyone expected. The three arms lines employ more people, consume more power and owe more money than the ministries "
        "believed. Some machine tools were bought on foreign credit and never installed. Others have run without maintenance "
        "for so long that much of what they turn out is rejected by the inspectors.",
        "The directors blame irregular orders from buyers who appeared, vanished and reappeared. The works councils blame "
        "managers who kept two sets of books. The territorial service, which takes a large share of the output, discovers that "
        "it has been paying export prices for rifles made a short drive from its own barracks. The foreign creditors will want "
        "to know when they are to be paid.",
        "The government now holds the only honest account of its largest employer. It can share the full report with the works "
        "councils, inviting a hard argument about wages and jobs, or brief only the directors and the creditors and settle the "
        "books privately. The councils have already heard that the report exists, and their members are waiting at the gates "
        "for an answer.",
    ), (
        Option('Share the report with the councils.', (Stability(-0.02), Event('works_walkout', 21))),
        Option('Brief the directors and creditors.', (PP(30), Stability(-0.01))),
    ), picture=0),
    EventDef('works_walkout', 'Silence at the Works Gates', (
        "Three weeks after the audit reaches the works councils, the morning shift at the largest arms line does not go in. The "
        "workers stand at the gates in the snow with flasks of tea and hand-painted signs, and refuse to start the lines until "
        "someone explains why their wages were frozen while machine tools rusted in their crates. By noon the other four plants "
        "have joined them.",
        "The walkout is orderly and almost silent. Nobody breaks a window, and the councils send volunteers to keep the furnaces "
        "warm so that the pipes do not freeze and the housing blocks stay heated. The directors call it blackmail. Deputies from "
        "Silvius call it the predictable result of the audit. Foreign buyers with deliveries due this month telephone the "
        "ministry one after another.",
        "The government cannot leave the works idle for long without losing both its exports and the goodwill of every family "
        "that depends on a works wage. It can open talks at once with the councils present and the full books on the table, or "
        "order each director to settle wage by wage in his own plant. The first is slower and fairer. The second is faster, and "
        "it will be remembered.",
    ), (
        Option('Open talks with the books on the table.', (Stability(0.03), PP(-20))),
        Option('Let each plant settle its own wages.', (PP(15), Stability(-0.02))),
    ), picture=1),
    EventDef('harbour_ice', 'The Harbour Freezes Early', (
        "The cold comes weeks early this year, and before the end of November the harbour is freezing along the quays. A grain "
        "ship and two freighters loaded with machine tools anchor offshore, waiting for a channel that the harbour's old tugs "
        "cannot keep open. The railway from Silvius fills its sidings with wagons that have nowhere to unload.",
        "The harbour master reports that the tugs were built for summer work and that their crews have never been trained for "
        "ice. The shipping lines report that insurers will not cover hulls waiting in drifting ice for more than a few days. In "
        "Silvius bread prices rise while the grain ship's cargo sits within sight of the coast, and the newspapers print a "
        "photograph of it every morning.",
        "The government must get the ships in, and in doing so it will decide what kind of harbour Baltica keeps. It can hire an "
        "icebreaker abroad at whatever price its owners name, or order the tugs out with volunteer crews and accept the risk to "
        "men and hulls. Whatever it chooses this winter will set the harbour's budget for the rest of the decade.",
    ), (
        Option('Hire an icebreaker at any price.', (Stability(0.02), PP(-20))),
        Option('Send the tugs out with volunteers.', (XP('navy', 15), Stability(-0.01))),
    ), picture=0),
    EventDef('muster_in_snow', 'A Muster in January', (
        "At dawn on a January morning every reservist on the territorial service's lists is told to report to the nearest "
        "barracks by noon. The snow on the plain is knee deep and the coastal road is half closed. In Silvius the barracks fill "
        "within hours. On the forest province reservists arrive by sledge, by tractor and on skis, and a good many do not arrive "
        "at all.",
        "By evening the service knows more about itself than it has learned in years. The two infantry formations are real, but "
        "many names on the lists belong to men who have moved away, aged out or died. The depots hold far more trucks than the "
        "formations can drive and too few men licensed to drive them. Coats cut for milder weather send dozens to the infirmary "
        "with frostbite.",
        "The general staff has money for one priority this year. It can spend on the reserve lists and on driving courses, so "
        "that the men who report can be moved, or on winter clothing and heated tents, so that the men who report can stay in "
        "the field. The reservists, who stood in the snow all day waiting for orders, have already said which they would choose.",
    ), (
        Option('Clothe the men first.', (Stability(0.02), XP('army', 10))),
        Option('Fix the lists and train drivers first.', (XP('army', 20), PP(-10))),
    ), picture=0),
    EventDef('frontier_table', 'Three Frontiers and a Coast', (
        "The foreign office spreads its new atlas across a table in Silvius and invites the cabinet to look. The longest line "
        "on the map is the frontier with Yuktobania, running from the hills of Silvius across the inland plain to the sea, "
        "facing a country many times Baltica's size and governed by its communist party. The shorter lines face Malynea, beside "
        "the forest and the harbour plain, and Seterano, whose mountains rise just beyond the capital's hills and close for "
        "much of the winter.",
        "The atlas proposes no change to any of these lines, and nobody at the table wants one. What it shows is how little "
        "Baltica knows about the country on the other side of each. Customs posts on the long frontier keep hours that suit "
        "neither side. The mountain passes have no rescue service. The coast faces an open sea where the only Baltican ships are "
        "merchant hulls.",
        "The cabinet must decide how Baltica will present itself to its neighbours, and the decision cannot wait for perfect "
        "knowledge. It can announce a policy at once and accept that it may need correcting, or send envoys to listen in all "
        "three capitals before saying anything. Every neighbour will read the choice as a statement about itself.",
    ), (
        Option('Announce a policy at once.', (PP(20), Stability(-0.01))),
        Option('Listen in all three capitals first.', (Stability(0.02), PP(-10))),
    ), picture=2),
    EventDef('empty_hangars', 'The Empty Hangars', (
        "The airfield near Silvius has a runway, a tower, two hangars and no aircraft that belong to Baltica. Transport flights "
        "land a few times a week when the weather allows, and foreign aircraft occasionally ask permission to refuel. The ground "
        "crew is a handful of civilians who also clear the snow. The territorial service starts the decade with no air arm and "
        "no plan for one.",
        "Now the question has been asked in the chamber. Officers who watch the neighbours' air forces argue that a country "
        "without aircraft cannot even see who is flying over it, let alone stop them. Treasury officials reply that one flight "
        "of modern fighters would cost more than the service spends in several years. Engineers at the works point out that guns "
        "and radar would cost far less and could be maintained at home.",
        "Before any choice about aircraft, the government must decide what the airfield is for. It can be run as a civil airport "
        "with military uses, funded by landing fees and open to anyone, or as a military field that admits civil flights by "
        "permission. The difference lies in who decides when the gates close, and the airlines have already asked.",
    ), (
        Option('Run it as a civil airport.', (Stability(0.01), PP(10))),
        Option('Run it as a military field.', (XP('air', 15), WarSupport(0.01))),
    ), picture=0),
    EventDef('belkan_war_far', 'A War Beyond the Horizon', (
        "In March 1995 fighting breaks out around Belka, on the far side of the world from Silvius. Baltica is no party to it "
        "and has no frontier anywhere near it, yet within a week the war has a desk in every ministry. Crude and grain cost more "
        "on every foreign exchange, shipping underwriters attach war clauses to any cargo routed near the fighting, and the "
        "works switchboard takes calls from buyers no director has ever met.",
        "For the first time since the audit the arms lines are offered more orders than they can fill. Some deputies say a "
        "lawful order is a lawful order, and that Baltican wages should not wait on other people's peace. Others answer that a "
        "small country selling arms into a war acquires enemies it can never afford. The territorial service quietly asks "
        "whether its own deliveries will now slip to the back of the queue.",
        "The cabinet meets twice in one week. The foreign minister wants a statement that Baltica will judge each order on its "
        "merits. The trade minister wants no statement at all. The chamber, the works councils and the reserve officers all want "
        "to know whether the war will raise wages or prices first, and the government must answer at least that before the "
        "spring is out.",
    ), (
        Option('Promise to judge each order on its merits.', (PP(15), WarSupport(0.02))),
        Option('Freeze fuel and bread prices for the summer.', (Stability(0.03), PP(-15))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Baltican response is gameplay', picture=0),
    EventDef('ulysses_word', 'Ulysses Will Fall', (
        "In April 1996 the FCU tells the world that Ulysses will hit the Earth, sixteen months after astronomers first raised the "
        "possibility. Where its fragments will come down is unknown, and may remain unknown until very late. Baltica has a hill "
        "of solid rock under its capital, winters cold enough to kill anyone left outdoors and a harbour that freezes just when "
        "it is most needed.",
        "The engineers at the works propose cutting shelters into the rock and heating them from the works furnaces. The radio "
        "and weather services propose warning and dispersal instead, arguing that a shelter on the hill is useless to a family "
        "on the forest province if the roads are closed by snow. The doctors want hospitals moved underground. The treasury asks "
        "which of these plans the country can pay for.",
        "The public mood moves faster than the planners. Hardware shops sell out of stoves and lamps, families on the coast talk "
        "about moving in with relatives in Silvius, and places of worship hold evening services every night. The government must "
        "decide whether to speak first about the danger or about the plan, knowing it cannot yet offer much of either.",
    ), (
        Option('Speak first about the plan.', (Stability(0.02), PP(-10))),
        Option('Speak first about the danger.', (WarSupport(0.03), Stability(-0.02), Research('construction_tech', 0.5, 1))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Baltican preparations are gameplay',
        picture=2),
    EventDef('roche_watch', 'The Long July Night', (
        "On 8 July 1999 Ulysses passes through the Roche limit of the Earth. In Baltica nobody sleeps. Families sit in the "
        "galleries, cellars and shelters they spent three years preparing, or on their doorsteps with radios, watching the sky "
        "over the hill of Silvius and the sea beyond the harbour. The trains wait in their stations with crews aboard, ready to "
        "move people if a warning comes.",
        "The radio carries reports from abroad faster than anyone can check them. A merchant master far out at sea describes "
        "lights he cannot explain. The weather service reports nothing unusual, then corrects itself, then corrects itself "
        "again. The crisis room under the capital keeps a log of every report, and by midnight it has stopped trying to separate "
        "rumour from fact and simply writes both down.",
        "At first light the crisis room counts what it knows, which is far less than it needs. Power is on in Silvius, the trains "
        "are running and the harbour master is on the radio. Beyond that every report is partial. Some ministers want the "
        "shelters kept open until the world has a clearer picture. Others want the works restarted at once, because a country "
        "that lives on its factories cannot afford a week of waiting.",
    ), (
        Option('Keep the shelters open for a week.', (WarSupport(0.03), Stability(-0.01))),
        Option('Restart the works at once.', (Stability(0.02), PP(15))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no damage in Baltica is claimed', picture=1),
    EventDef('usean_cargo', 'Charters Toward Usea', (
        "In the summer of 2003 Erusea invades the neutral country of San Salvacion and seizes Stonehenge, and war spreads across "
        "Usea. The continent is far from Baltica's frontiers, but Baltican hulls carry cargo on lanes that reach Usean ports, "
        "and the works sell spare parts to Usean buyers. Within a week underwriters withdraw cover on routes toward the fighting "
        "and raise it on every route nearby.",
        "Baltican masters will not sail toward Usea until they know who carries the loss if a hull goes down. Both sides of the "
        "war telephone the works with orders for trucks, spare parts and ammunition. The chamber, the works councils and the "
        "harbour owners all remember the Belkan War, and all remember it differently: as a season of easy profit, or as a lesson "
        "in how quickly a small supplier becomes a target.",
        "The cabinet has two ways to steady the fleet. It can bar every Baltican hull from Usean waters until the war ends and "
        "compensate the owners for part of their lost income, or let masters sail where their contracts lead with whatever "
        "insurance they can buy. Either way the bill arrives every month the war lasts, and the harbour owners expect an answer "
        "before the autumn sailings.",
    ), (
        Option('Keep every hull out of Usean waters.', (Stability(0.02), PP(-15))),
        Option('Let masters sail where contracts lead.', (PP(25), Stability(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Baltican response is gameplay', picture=1),
)

# --- branches ------------------------------------------------------------------------------------
REPUBLIC = Branch('rep', 'The November Ballot', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('rep_mandate_runs_out', 'The 1987 Mandate Runs Out',
          "Baltica enters 1991 governed by the National Administration, an office under a democratic banner whose mandate dates "
          "from the ballot of November 1987. The next vote falls due in November. Seven voters in ten back the democratic camp "
          "and most of the rest a non-aligned establishment, so the real question is not who wins but what kind of government "
          "the winners will build.",
          ('ballot', 'assembly'), reward=(Idea('expiring_mandate'), Event('november_ballot'))),
    Focus('rep_roll_of_voters', 'Clean the Roll of Voters',
          "Clerks in Silvius compare the electoral roll with the works payrolls, the reserve register and the harbour lists, and "
          "find names that should have been struck years ago beside families who were never added. Correcting the roll before "
          "the vote costs the Administration a season of complaints from every party, but it gives the result a credibility "
          "that no later government could borrow.",
          ('document', 'ballot'), after=('rep_mandate_runs_out',),
          reward=(PP(30), Tooltip('Opens the three answers to the ballot; only one can be taken.'))),
    Focus('rep_open_gallery', 'Open the Chamber Gallery',
          "Budget debates have been held behind closed doors, with the press told the result afterwards. Opening the gallery to "
          "reporters and to anyone willing to queue for a seat lets voters watch deputies bargain over rifles, roads and heating "
          "allowances. Ministers lose the comfort of private compromise and some deals become impossible, but the public begins "
          "to see where its taxes actually go.",
          ('assembly', 'communications'), after=('rep_mandate_runs_out',), reward=(Idea('public_gallery'),)),
    Focus('rep_chamber_path', 'Ministers From the Chamber',
          "The democratic majority proposes the simplest answer: let the newly elected chamber choose a cabinet and hold it to "
          "account, with the Administration dissolved into ordinary ministries. Most voters want exactly that. The works "
          "directors and the defence staff warn that a cabinet built on coalitions will argue over every rifle and every lathe "
          "while a very large neighbour sits on the long frontier.",
          ('ballot', 'scales'), after=('rep_roll_of_voters',), exclusive=('rep_works_path', 'rep_defence_path'),
          reward=(SwapIdea('expiring_mandate', 'chamber_mandate'),)),
    Focus('rep_works_path', 'The Directors Offer a Board',
          "Directors of the arsenal works, the harbour company and the two civilian plants propose another settlement. A board "
          "of the enterprises would govern, with the chamber kept as a consultative body, and judge each policy by whether the "
          "works stay busy and wages are paid. The non-aligned establishment likes the idea. The democratic majority sees a few "
          "managers walking into the state through the factory gate.",
          ('industry', 'command'), after=('rep_roll_of_voters',), exclusive=('rep_chamber_path', 'rep_defence_path'),
          reward=(SwapIdea('expiring_mandate', 'works_charter'),)),
    Focus('rep_defence_path', 'The Defence Staff Steps Forward',
          "Officers of the territorial service argue that a country of one hill, one plain and one harbour, beside a vast "
          "neighbour, cannot afford a government that may change every four years. They offer a defence council to hold the "
          "state, with the chamber kept for budgets and petitions. The idea has more support than the polls suggest, because "
          "nearly every family has someone on the reserve list.",
          ('security', 'command'), after=('rep_roll_of_voters',), exclusive=('rep_chamber_path', 'rep_works_path'),
          reward=(SwapIdea('expiring_mandate', 'defence_watch'),)),
    Focus('rep_chamber_cabinet', 'Swear In the Chamber Cabinet',
          "The chamber elects a cabinet, and the National Administration hands over its seals in a short ceremony in Silvius. "
          "Ministers now answer to deputies, and the election calendar is written into ordinary law instead of being renewed by "
          "habit. Coalition bargaining begins the same afternoon. The works directors and the defence staff keep their posts, "
          "but they now petition a minister instead of sitting beside one.",
          ('ballot', 'medal'), after=('rep_chamber_path',), cost=10,
          exclusive=('rep_works_board', 'rep_defence_council'),
          reward=(Regime('chamber_cabinet'), Flag('path_chamber'))),
    Focus('rep_works_board', 'Seat the Board of the Works',
          "The directors of the arsenal works, the harbour company and the civilian plants take the government seals as a "
          "standing board. The chamber meets twice a year to hear the budget and cannot amend it. Orders are signed in days "
          "rather than months and wages arrive on time. The unions and the democratic camp, who were promised a vote, note that "
          "nobody asked them anything.",
          ('industry', 'scales'), after=('rep_works_path',), cost=10,
          exclusive=('rep_chamber_cabinet', 'rep_defence_council'),
          reward=(Regime('works_board'), Flag('path_works'))),
    Focus('rep_defence_council', 'Convene the Defence Council',
          "Senior officers of the territorial service take executive power for what they call a period of readiness. Parties "
          "are not banned and the chamber still sits, but the council writes the budget and appoints the ministers. Drills run "
          "on schedule and the reserve rolls fill. Nobody on the council has said how long readiness lasts, and that silence is "
          "noticed in every embassy in Silvius.",
          ('command', 'security'), after=('rep_defence_path',), cost=10,
          exclusive=('rep_chamber_cabinet', 'rep_works_board'),
          reward=(Regime('defence_council'), Flag('path_defence'))),
    Focus('rep_chamber_code', 'A Code of Ministerial Duty',
          "The first chamber cabinet writes down what ministers owe the deputies: answers to written questions within a month, "
          "published contracts above a set value and a register of every gift. The opposition turns the code against the "
          "government within weeks. Ministers grumble that half their working day now goes on answering letters, yet public "
          "trust in the cabinet climbs steadily.",
          ('scales', 'document'), after=('rep_chamber_cabinet',),
          exclusive=('rep_board_wages', 'rep_readiness_terms'),
          reward=(SwapIdea('chamber_mandate', 'ministerial_code'),)),
    Focus('rep_board_wages', 'Wages Before Dividends',
          "Pressed by unrest at the gates, the board signs a pact that puts wages ahead of any payment to the enterprises' owners "
          "and creditors. Workers get a written guarantee and a seat on each works council. Directors lose money they had counted "
          "on, and two foreign creditors demand faster repayment. The board keeps its seals and gains a reason for the works to "
          "want it to keep them.",
          ('industry', 'assembly'), after=('rep_works_board',),
          exclusive=('rep_chamber_code', 'rep_readiness_terms'),
          reward=(SwapIdea('works_charter', 'works_wage_pact'),)),
    Focus('rep_readiness_terms', 'Publish the Terms of Readiness',
          "Under pressure from the chamber and from lenders abroad, the defence council publishes the conditions under which "
          "readiness would end and civilian ministers return: a full reserve, a quiet frontier and a balanced budget. Few believe "
          "the conditions will ever be declared met. The document still gives the public a measure to hold the officers to, and "
          "the officers know it.",
          ('security', 'document'), after=('rep_defence_council',),
          exclusive=('rep_chamber_code', 'rep_board_wages'),
          reward=(SwapIdea('defence_watch', 'readiness_charter'),)),
    Focus('rep_republic_holds', 'The Republic Holds Together',
          "By the middle of the decade the quarrel of 1991 has become routine. Whatever answer won, ministries know who signs "
          "their orders, the works know who sets their quotas and the reserve knows who can call it out. Small countries live on "
          "being predictable, and Baltica's neighbours and customers begin to treat it as a settled place where a contract signed "
          "today will still hold next year.",
          ('peace', 'ballot'), after_any=('rep_chamber_code', 'rep_board_wages', 'rep_readiness_terms'),
          reward=(Flag('order_settled'), Stability(0.04))),
    Focus('rep_audit_office', 'An Audit Office for the Republic',
          "The arsenal audit showed what a single honest inspection could find. A permanent audit office, independent of every "
          "ministry and reporting to the chamber, now inspects one ministry and one works contract after another each year. "
          "Officials resent it and several careers end in its reports. The savings it finds in its first three years pay for the "
          "office many times over.",
          ('scales', 'economy'), after=('rep_republic_holds',), reward=(Idea('audit_office'),)),
))

SILVIUS = Branch('hill', 'Silvius on Its Hill', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('hill_five_provinces', 'Ledger of the Five Provinces',
          "Baltica is small enough to cross in a few days: Silvius on its hill, an inland plain, a forest province toward "
          "Malynea and two coastal plains, one of them holding the harbour. Nobody has measured them properly in a generation. A "
          "land and household register takes a winter of work and settles the arguments about which province pays for which "
          "road.",
          ('document', 'civil'), reward=(Idea('province_register'), Event('winter_ledger'))),
    Focus('hill_snow_roads', 'Roads Kept Open Through Winter',
          "For months each year the country lies under snow, and blizzards close the road from Silvius to the coast for days at "
          "a time. Graders, salt stores and plough depots at every junction keep traffic moving through the worst weeks. The "
          "works pay for it through road taxes they resent, and the plough crews become the best-known public servants in the "
          "country.",
          ('logistics', 'tools'), after=('hill_five_provinces',), reward=(Build('infrastructure', 1, 0),)),
    Focus('hill_harbour_line', 'Double Track to the Harbour',
          "A single railway runs from Silvius across the inland plain to the harbour, carrying everything the works send abroad "
          "and much of what the country eats. A second track and new passing loops let freight and passenger trains run without "
          "waiting for each other. The plain loses farmland to embankments, and the project swallows most of the works budget "
          "for two years.",
          ('rail', 'logistics'), after=('hill_five_provinces',), reward=(Build('infrastructure', 1, 0),)),
    Focus('hill_upper_mains', 'Water Mains on the Upper Streets',
          "The upper streets of Silvius still draw water from cisterns filled by pumps that freeze every hard winter. New mains "
          "laid below the frost line, with a pumping station at the foot of the hill, end the bucket queues. Digging through rock "
          "is slow and costly, and the cistern keepers who carried water up the hill lose their trade overnight.",
          ('civil', 'tools'), after=('hill_five_provinces',), reward=(Idea('hill_waterworks'),)),
    Focus('hill_rural_clinics', 'Clinics Beyond the Capital',
          "Outside Silvius the only doctors work at the harbour and in the works infirmary, and in a blizzard a sick child on the "
          "forest province may wait two days for either. A small clinic in each province, with a snow vehicle and a radio, "
          "brings care within an hour of every household. Doctors are scarce and must be paid well to live outside the capital.",
          ('medical', 'civil'), after=('hill_five_provinces',), reward=(Idea('provincial_clinics'),)),
    Focus('hill_build_upward', 'Build Upward on the Hill',
          "One school of planners wants Silvius to stay on its hill, close to the works and easy to defend, with taller housing "
          "blocks, covered walkways against the snow and every service within a short walk. Building upward is cheap in land and "
          "expensive in steel. Residents who like their low old streets object, and the works families who need flats fastest do "
          "not.",
          ('civil', 'security'), after=('hill_upper_mains',), exclusive=('hill_spread_plain',), reward=(Idea('dense_hill'),)),
    Focus('hill_spread_plain', 'A New Quarter on the Plain',
          "The other school wants a new district of low houses and gardens on the inland plain, along the railway to the "
          "harbour, with fast trains to the works. Land is cheap there and the houses can be warm and spacious. The defence staff "
          "points out that a town spread across open ground is harder to protect, and farmers ask where their own fields are "
          "supposed to go.",
          ('civil', 'rail'), after=('hill_upper_mains',), exclusive=('hill_build_upward',), reward=(Idea('plain_quarter'),)),
    Focus('hill_snow_brigades', 'Volunteer Snow Brigades',
          "Every blizzard closes the plain for a day or two, and the plough crews cannot reach every lane. Brigades of volunteers, "
          "organised by street and paid in fuel vouchers, dig out bus stops, clinic doors and the homes of the elderly. The "
          "scheme costs little and makes neighbours of strangers. It also gives the government a list of willing hands that the "
          "territorial service quietly copies.",
          ('civil', 'shelter'), after=('hill_snow_roads',), reward=(Idea('winter_volunteers'),)),
    Focus('hill_works_heat', 'Heat From the Works Chimneys',
          "The arsenal works burn fuel all winter to keep their furnaces hot, and most of that heat leaves through the chimneys. "
          "Piping it into the nearest housing blocks warms thousands of flats for the cost of insulation and pumps. Households "
          "pay less for fuel, and the works gain a public reason to keep running, which their directors mention at every budget "
          "debate.",
          ('industry', 'civil'), after_any=('hill_build_upward', 'hill_spread_plain'), reward=(Idea('works_heat'),)),
))

WORKS = Branch('works', 'The Arsenal Works', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_ledger_open', 'Open the Arsenal Ledgers',
          "Three arms lines and two civilian plants make up nearly all of Baltica's industry, and the arms lines are older, larger "
          "and better paid. Nobody outside the directors' offices knows what they cost or who buys their output. An audit of "
          "every order, wage and debt takes a year, and it will decide which parts of the works the country can afford to keep.",
          ('industry', 'document'), reward=(Idea('arsenal_ledger'), Event('arsenal_ledgers'))),
    Focus('works_orders_book', 'One Order Book for the Works',
          "Each arms line has kept its own order book, its own suppliers and its own salesmen, and they regularly bid against one "
          "another for the same foreign contract. A single order book, kept in Silvius and open to all three lines, ends the "
          "undercutting. Directors lose some freedom and one of them resigns in protest, but the works stop selling below cost.",
          ('document', 'economy'), after=('works_ledger_open',), reward=(Idea('common_order_book'),)),
    Focus('works_councils_elected', 'Works Councils at Every Gate',
          "Each plant elects a council of workers that meets the management monthly and sees the order book, the safety record "
          "and the wage bill. The councils slow some decisions and kill a few bad ones. Strikes, which used to start without "
          "warning at the gates, now start, if at all, after a month of argument that everyone can see coming.",
          ('assembly', 'industry'), after=('works_ledger_open',), reward=(Idea('works_councils'),)),
    Focus('works_export_lines', 'Arms Lines for Export',
          "The first model keeps all three arms lines at full rate and sells what the territorial service cannot use to licensed "
          "foreign buyers. Exports pay for the works and for a large share of the budget. The risk is plain to everyone: Baltica "
          "would live on other countries' quarrels, and every sale to one side of a dispute is remembered by the other.",
          ('missile', 'economy'), after=('works_orders_book',),
          exclusive=('works_civil_conversion', 'works_reserve_arsenal'), reward=(Idea('export_arsenal'),)),
    Focus('works_civil_conversion', 'Two Lines to Civilian Work',
          "The second model converts two of the three arms lines to tractors, pumps, rail wagons and heating plant, which the "
          "country now buys abroad at high prices. Output falls for two years while the lines are retooled, and skilled gunsmiths "
          "must learn new trades. The country ends up less dependent on foreign wars and more dependent on its own customers.",
          ('rebuild', 'industry'), after=('works_orders_book',),
          exclusive=('works_export_lines', 'works_reserve_arsenal'), reward=(Idea('converted_lines'),)),
    Focus('works_reserve_arsenal', 'An Arsenal for Baltica Alone',
          "The third model makes the works an arsenal for Baltica alone. The lines run below capacity in peacetime, building "
          "stocks of rifles, trucks and spare parts for the territorial service, and keep the tooling ready to surge if the "
          "frontier ever turns dangerous. It is the costliest model in peacetime and the most reassuring to a public that "
          "expects to defend itself.",
          ('industry', 'security'), after=('works_orders_book',),
          exclusive=('works_export_lines', 'works_civil_conversion'), reward=(Idea('reserve_arsenal'),)),
    Focus('works_export_licences', 'Licences Signed in Silvius',
          "Every export now needs a licence signed in Silvius and published within a month, naming the buyer, the weapon and the "
          "quantity. Some buyers walk away rather than be named. Those who stay pay more for a supplier whose word is public. The "
          "works lose quick sales and gain long contracts, and the chamber gains a list it can argue about every session.",
          ('missile', 'document'), after=('works_export_lines',),
          exclusive=('works_wagon_orders', 'works_surge_drills'),
          reward=(SwapIdea('export_arsenal', 'licensed_exports'),)),
    Focus('works_wagon_orders', 'Wagons for the Harbour Line',
          "The converted lines win their first large order at home: freight wagons for the railway to the harbour and pumps for "
          "the new water mains. Domestic orders are smaller than arms contracts and paid more slowly. They also keep money inside "
          "Baltica, and the works councils, who feared that conversion meant closure, start to believe in the plan.",
          ('rail', 'rebuild'), after=('works_civil_conversion',),
          exclusive=('works_export_licences', 'works_surge_drills'),
          reward=(SwapIdea('converted_lines', 'civil_order_book'),)),
    Focus('works_surge_drills', 'Surge Drills at the Works',
          "Twice a year the reserve arsenal runs a surge drill: every line called back to full rate for a week, reservists from "
          "the works rolls reporting to their benches and the railway clearing paths for ammunition trains. The drills cost a "
          "week of normal output. They prove the arsenal can wake quickly, and they tell the neighbours so without a word being "
          "said.",
          ('industry', 'medal'), after=('works_reserve_arsenal',),
          exclusive=('works_export_licences', 'works_wagon_orders'),
          reward=(SwapIdea('reserve_arsenal', 'surge_arsenal'),)),
    Focus('works_spare_parts', 'Spare Parts Before New Rifles',
          "The territorial service keeps more trucks than it can run, because many wait for parts the works never make: the "
          "profit is in new rifles, not in gaskets and axles. A standing quota for spare parts, paid at a fixed margin, keeps the "
          "motor pool on the road. Directors call it unglamorous work. The quartermasters call it long overdue.",
          ('tools', 'logistics'), after=('works_orders_book',), reward=(Idea('spares_first'),)),
    Focus('works_board_quotas', 'The Board Sets the Quotas',
          "Under the board of the works, the directors who govern the country also run its factories, and quotas are set in the "
          "same room as the budget. Orders move quickly from ministry to bench. Every dispute between a plant and the public is "
          "now a dispute with the government itself, and the unions learn to petition the board as employer and state at once.",
          ('command', 'industry'), after=('works_orders_book',), requires=(HasFlag('path_works'),),
          reward=(Idea('board_quotas'),)),
    Focus('works_tool_room', 'A Tool Room for All Five Plants',
          "Each of the five plants has kept its own tool room, and none of them can make a precision jig without borrowing a "
          "machine from another. A shared tool room, staffed by the best machinists from every plant, now makes jigs, gauges and "
          "dies for all of them. The plants resent losing their best hands to it, and productivity rises across all of them "
          "within a year.",
          ('tools', 'industry'), after=('works_spare_parts',), reward=(Research('industry', 0.5, 2),)),
    Focus('works_old_debts', 'Pay Off the Old Machine Debts',
          "The audit found debts the works ran up before 1991, mostly to foreign suppliers of machine tools. Paying them off from "
          "five years of earnings, whatever model the country chose, frees the works from creditors who attach conditions to "
          "every new loan. The budget is tight for two years, and the works councils accept a wage freeze to see it done.",
          ('economy', 'scales'), after_any=('works_export_licences', 'works_wagon_orders', 'works_surge_drills'),
          reward=(Idea('works_debt_cleared'),)),
))

ORE = Branch('ore', 'Steel, Oil and Rubber', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('ore_resource_survey', 'What Lies Under the Hill',
          "Baltica records modest steel, oil and rubber, enough to feed part of its own works and little more. The survey maps "
          "in the ministry predate the works themselves. A new survey with drilling rigs and core samples tells the ministries "
          "how long each source will last and how much more could be won with better equipment. The answers are less generous "
          "than the directors hoped.",
          ('document', 'tools'), reward=(Idea('survey_maps'),)),
    Focus('ore_keep_home', 'Steel for Baltican Lathes',
          "The first option keeps every ton of steel and every barrel of crude for the works and the territorial service, at "
          "prices set below the world market. The works gain secure supply and cheap inputs. The treasury loses export earnings "
          "it badly needs, and producers complain that they subsidise the arsenal with every shipment they are forbidden to sell "
          "abroad.",
          ('industry', 'logistics'), after=('ore_resource_survey',), exclusive=('ore_sell_abroad',),
          reward=(Idea('home_inputs'),)),
    Focus('ore_sell_abroad', 'Steel and Crude for Hard Currency',
          "The second option sells what the works do not need to foreign buyers through the harbour, at world prices and in hard "
          "currency. The treasury gains earnings that pay for imported machine tools and food. The works must then buy their own "
          "inputs at the same prices as foreigners, and in a lean year they will be outbid for their own country's steel.",
          ('economy', 'navy'), after=('ore_resource_survey',), exclusive=('ore_keep_home',),
          reward=(Idea('export_earnings'),)),
    Focus('ore_deeper_wells', 'New Rigs for the Old Wells',
          "The wells that supply Baltica's crude were drilled with equipment that cannot reach below the first oil-bearing layer. "
          "New rigs, bought abroad with an engineering contract, reach deeper and slow the decline of the field. They cost more "
          "than the crude they recover in their first three years. After that the field pays for them every year it keeps "
          "flowing.",
          ('tools', 'economy'), after=('ore_resource_survey',), reward=(Research('excavation_tech', 0.5, 1),)),
    Focus('ore_synthetic_rubber', 'Rubber From the Laboratory',
          "The country's own rubber covers only part of what its trucks and plants consume, and imported rubber arrives by sea "
          "when the harbour is not frozen. Chemists at the works propose a small synthetic process using local crude as "
          "feedstock. Output is expensive and modest. It ends the fear that a frozen harbour or a foreign embargo could stop "
          "every truck in the country.",
          ('science', 'industry'), after=('ore_resource_survey',), reward=(Research('synth_resources', 0.5, 1),)),
    Focus('ore_fuel_reserve', 'A Buried Fuel Reserve',
          "A hard winter can close the harbour and the frontier crossings at the same time, and Baltica then has only what it "
          "holds in its tanks. A reserve large enough for two winters, stored in buried tanks around Silvius, keeps heating and "
          "transport running whatever the weather. Filling it takes a year of crude that could otherwise have been sold.",
          ('shelter', 'logistics'), after=('ore_deeper_wells',), reward=(Idea('fuel_reserve'),)),
    Focus('ore_price_board', 'A Price Board for Fuel and Steel',
          "Whatever the country decided about selling abroad, domestic prices for fuel and steel have swung wildly with every "
          "foreign quarrel. A price board publishes quarterly prices for both, with a small fund to smooth the sharpest jumps. "
          "Producers lose some windfall profits and buyers lose some bargains. Everyone gains the ability to plan a year ahead.",
          ('scales', 'economy'), after_any=('ore_keep_home', 'ore_sell_abroad'), reward=(Idea('price_board'),)),
))

HARBOUR = Branch('harbour', 'The Harbour on the Cold Coast', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('harbour_sixty_hulls', 'Sixty Hulls, One Harbour',
          "Baltica keeps no fighting navy, but sixty merchant hulls sail under its flag, and almost all of them load and unload "
          "at one harbour on the coastal plain. The harbour has a single naval berth, a rail head and cranes older than most of "
          "their operators. A survey of every quay and hull tells the ministries what the merchant fleet can actually carry.",
          ('navy', 'document'), reward=(Idea('harbour_register'), Event('harbour_ice'))),
    Focus('harbour_ice_tugs', 'Tugs That Break Ice',
          "In the coldest weeks the harbour freezes along the quays, and ships wait offshore for days while their cargoes of "
          "food and machine tools wait with them. Two heavy tugs with reinforced bows keep a channel open all winter. Their crews "
          "are the closest thing Baltica has to a naval service, and they learn more seamanship in one winter than in years of "
          "summer work.",
          ('navy', 'tools'), after=('harbour_sixty_hulls',), reward=(Idea('ice_tugs'), XP('navy', 15))),
    Focus('harbour_open_quays', 'Open Quays for Every Flag',
          "One plan opens the harbour to every flag on equal terms, with low dues, quick inspections and bonded warehouses for "
          "goods in transit. Traders from all three neighbours and from farther afield are invited to use Baltican quays. Dues "
          "rise with volume. Customs officers warn that a harbour open to everyone is also a harbour where nobody looks closely "
          "at the crates.",
          ('navy', 'economy'), after=('harbour_sixty_hulls',), exclusive=('harbour_every_crate',),
          reward=(Idea('open_quays'),)),
    Focus('harbour_every_crate', 'Every Crate Inspected',
          "The other plan keeps the harbour under a strict regime: every crate opened or scanned, every manifest checked against "
          "the works order book and preference given to Baltican hulls. Traffic grows slowly and dues stay high. The arms works "
          "prefer it, because nothing leaves the country that the government cannot account for, and nothing arrives unseen "
          "either.",
          ('security', 'navy'), after=('harbour_sixty_hulls',), exclusive=('harbour_open_quays',),
          reward=(Idea('inspected_quays'),)),
    Focus('harbour_cinigrad_news', 'Submarines Announced at Cinigrad',
          "In September 1991 Yuktobania announces a new class of submarine at a political convention in Cinigrad, and the news "
          "reaches Silvius with the evening papers. Baltica has no navy to set against anything, but its merchant masters ask what "
          "the announcement means for the lanes off their own coast. The government doubles the coast watch for a year and asks "
          "masters to report every unusual contact.",
          ('submarine', 'radar'), after=('harbour_sixty_hulls',), requires=(HasGlobal('ac_bwr_cinigrad'),),
          reward=(TimedIdea('coast_alert', 365),)),
    Focus('harbour_rail_cranes', 'New Cranes at the Rail Head',
          "Freight arrives at the harbour on the single railway from Silvius and waits for cranes that lift one load in the time "
          "a modern crane lifts four. Replacing them, and laying sidings so wagons can be loaded beside the ships, cuts the time "
          "a hull spends at the quay by half. The cranes are bought abroad and their operators retrained at the harbour's expense.",
          ('rail', 'navy'), after=('harbour_sixty_hulls',), reward=(Idea('rail_head_cranes'),)),
    Focus('harbour_coast_radar', 'Radar on the Coastal Plain',
          "The harbour cannot see beyond the horizon, and in fog or snow it cannot see much closer either. A radar post on the "
          "coastal plain watches the approaches and guides ships into the channel the tugs keep open. The army wants the same set "
          "to watch for aircraft. Sharing it means arguments over the watch schedule, settled by giving each service its own "
          "shifts.",
          ('radar', 'navy'), after_any=('harbour_open_quays', 'harbour_every_crate'), reward=(Build('radar_station', 1, 0),)),
    Focus('harbour_mates_school', 'A School for Merchant Officers',
          "Baltican hulls are officered largely by foreigners, because the country has trained few of its own above the rank of "
          "able seaman. A merchant marine school at the harbour, with a training ship and an ice navigation course, turns out "
          "mates and engineers in three years. Shipping lines must pay for places in the school, which they do while grumbling.",
          ('training', 'navy'), after=('harbour_ice_tugs',), reward=(Idea('mates_school'),)),
))

SERVICE = Branch('guard', 'The Territorial Service', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_winter_muster', 'Muster in the Snow',
          "The territorial service has two infantry formations, a reserve list longer than its barracks and depots holding more "
          "rifles and trucks than the formations could use. Nobody has called the whole reserve out in winter. A full muster in "
          "January, with snow on the plain and the roads half closed, shows what the service can really do and what it only "
          "claims to do.",
          ('security', 'training'), reward=(Idea('muster_lessons'), Event('muster_in_snow'))),
    Focus('guard_depot_drivers', 'More Trucks Than Drivers',
          "The service holds hundreds of trucks in its depots, far more than two infantry formations need, and too few soldiers "
          "licensed to drive them. A driving school at the depot, with winter courses on the coastal road, turns infantrymen into "
          "drivers and mechanics. The trucks start moving, the fuel bill rises and the depots finally learn which vehicles still "
          "run.",
          ('logistics', 'training'), after=('guard_winter_muster',), reward=(Idea('driver_school'),)),
    Focus('guard_hill_redoubt', 'Hold the Hill of Silvius',
          "The first doctrine concentrates the service on Silvius and its hills, with dug-in positions, stored ammunition and "
          "every street mapped for defence. A capital on high ground with the works inside its perimeter can hold for weeks. The "
          "plain, the forest and the coast would be watched rather than held, and the people who live there understand exactly "
          "what that means.",
          ('security', 'command'), after=('guard_winter_muster',),
          exclusive=('guard_frontier_screens', 'guard_plain_reserve'), reward=(Idea('hill_redoubt'),)),
    Focus('guard_frontier_screens', 'Screens in the Forest and Passes',
          "The second doctrine pushes the service out to the frontiers: small companies along the Yuktobanian line from the "
          "hills to the coast, others in the forest facing Malynea, and mountain troops on the passes toward Seterano. The "
          "screens would delay anything that crossed and report "
          "it within minutes. They are thin, cold and lonely, and companies rotate every month to keep morale from freezing along "
          "with the men.",
          ('security', 'radar'), after=('guard_winter_muster',),
          exclusive=('guard_hill_redoubt', 'guard_plain_reserve'), reward=(Idea('frontier_screens'),)),
    Focus('guard_plain_reserve', 'A Motor Reserve on the Plain',
          "The third doctrine uses the trucks the service already owns. A motorised reserve stationed on the inland plain, "
          "astride the railway, could reach any frontier or the harbour within hours. It needs fuel, drivers and roads kept open "
          "in winter. It also leaves the frontiers lightly watched for the first hours of any crisis, as the forest villages "
          "point out at every public meeting.",
          ('logistics', 'security'), after=('guard_winter_muster',),
          exclusive=('guard_hill_redoubt', 'guard_frontier_screens'), reward=(Idea('plain_reserve'),)),
    Focus('guard_rock_galleries', 'Ammunition Galleries in the Hill',
          "Under the redoubt doctrine the service cuts storage galleries into the rock of the hill and fills them with "
          "ammunition, food and medical stores for a long siege. The works deliver to them by a short rail spur. Engineers warn "
          "about damp and the treasury warns about the bill, but the stores are proof against weather and against almost "
          "anything else.",
          ('shelter', 'security'), after=('guard_hill_redoubt',), reward=(SwapIdea('hill_redoubt', 'hill_fortress'),)),
    Focus('guard_mountain_companies', 'Mountain Companies on the Passes',
          "The service already trains a few men for mountain work, and the screens doctrine makes them its elite. Companies "
          "posted to the passes toward Seterano learn to ski, climb and live in snow caves for a week at a time. Recruits "
          "volunteer in larger numbers than expected. Injuries from cold and falls in training are a real cost, and the papers "
          "report every one.",
          ('training', 'medal'), after=('guard_frontier_screens',), reward=(SwapIdea('frontier_screens', 'mountain_screens'),)),
    Focus('guard_night_drives', 'Night Drives Across the Plain',
          "The motorised reserve practises driving to every frontier at night and in snow, with headlights masked and the "
          "railway carrying fuel ahead of the convoys. The first drills end in ditches. By the second winter the reserve reaches "
          "the Malynea frontier in under three hours. Farmers on the plain grow used to trucks passing their houses at two in the "
          "morning.",
          ('logistics', 'medal'), after=('guard_plain_reserve',), reward=(SwapIdea('plain_reserve', 'motor_reserve'),)),
    Focus('guard_reserve_register', 'A Register of the Reserve',
          "The reserve list has been kept on cards in each barracks, and nobody knows how many reservists have moved, aged out or "
          "died. A single register, matched against the tax rolls and the works payrolls, shows who could actually report. The "
          "list shrinks sharply. What remains is a reserve the service can count on, rather than one it merely counts.",
          ('document', 'security'), after=('guard_winter_muster',), reward=(Idea('reserve_register'),)),
    Focus('guard_winter_kit', 'Kit for Twenty Below',
          "The service's uniforms were not cut for Baltican winters, and every January men are sent home with frostbite. "
          "Proper winter kit, with layered clothing, felt boots, white smocks and heated tents, costs more per soldier than a "
          "rifle. It is the first thing reservists ask about at every muster, and the first change they notice when it finally "
          "arrives.",
          ('training', 'shelter'), after=('guard_depot_drivers',), reward=(Idea('winter_kit'),)),
    Focus('guard_council_review', 'The Council Reviews the Service',
          "Under the defence council the territorial service is reviewed by the officers who also govern the country. Inspections "
          "are frequent, promotions follow drill results and budgets arrive on time. The service has never been better funded. It "
          "has also never been so close to politics, and junior officers learn that a poor inspection can end a career faster "
          "than any war.",
          ('command', 'medal'), after=('guard_winter_muster',), requires=(HasFlag('path_defence'),),
          reward=(Idea('council_inspectors'), XP('army', 15))),
    Focus('guard_full_strength', 'The Service at Full Strength',
          "By the late nineties the territorial service has a doctrine, a register that matches its barracks and clothing for the "
          "climate it actually serves in. It is still small. It is no longer a list of names and a depot of trucks, and the "
          "military attaches who watch every autumn exercise report home that Baltica could make any trespass expensive.",
          ('medal', 'security'), after_any=('guard_rock_galleries', 'guard_mountain_companies', 'guard_night_drives'),
          reward=(Flag('service_ready'), XP('army', 20))),
))

AIRFIELD = Branch('air', 'One Airfield, No Squadron', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_empty_field', 'An Airfield Without Aircraft',
          "Baltica has one airfield near Silvius and no aircraft of its own to fly from it. The runway serves a few transport "
          "flights a week and the occasional visiting foreign aircraft. Lengthening it and adding hard standing makes it usable "
          "in all seasons, and forces a question nobody has wanted to ask: should the country ever base fighters there?",
          ('runway', 'air'), reward=(Build('air_base', 1, 0), Event('empty_hangars'))),
    Focus('air_runway_ploughs', 'Runway Ploughs and Heated Lamps',
          "Snow closes the runway for days each winter, and the approach lights freeze. Runway ploughs, de-icing equipment and "
          "heated lamps keep it open in all but the worst blizzards. Transport flights stop cancelling and the mail arrives on "
          "time. The ground crews, trained on equipment borrowed from abroad, become the nucleus of any air service Baltica may "
          "one day build.",
          ('runway', 'tools'), after=('air_empty_field',), reward=(Build('air_base', 1, 0),)),
    Focus('air_interceptor_flight', 'A Flight of Interceptors',
          "One answer is a small flight of interceptors bought abroad, with pilots trained by the seller, to police the "
          "country's skies and escort any intruder away. It would give Baltica combat aviation, which the service of 1991 does "
          "not have. The cost is enormous for a budget this size, and the pilots would need years of training before the flight could "
          "do more than show the flag.",
          ('air', 'runway'), after=('air_empty_field',), exclusive=('air_ground_guns',),
          reward=(Idea('interceptor_flight'), XP('air', 20))),
    Focus('air_ground_guns', 'Guns and Radar Instead of Fighters',
          "The other answer leaves the sky to guns and radar. Anti-aircraft batteries on the hill and around the harbour, tied to "
          "radar posts, cannot chase an intruder but can make any attack costly. The plan costs a fraction of a fighter flight and "
          "uses soldiers the service already has. It also accepts that Baltican skies belong to whoever is willing to fly in "
          "them.",
          ('security', 'radar'), after=('air_empty_field',), exclusive=('air_interceptor_flight',),
          reward=(Idea('ground_air_defence'),)),
    Focus('air_frontier_reports', 'Air Reports Over the Frontiers',
          "Baltica cannot watch its skies alone, so it offers each neighbour the same exchange: every unidentified aircraft any "
          "of them detects near the shared frontiers reported to the others within minutes. The offer goes in identical notes to "
          "all three capitals. It is not an alliance and nobody calls it one, but Baltican reports go out on an open channel "
          "whether or not anyone answers.",
          ('radar', 'diplomacy'), after=('air_empty_field',), reward=(Idea('air_reporting'),)),
    Focus('air_foreign_courses', 'Pilots on Foreign Courses',
          "The interceptor flight needs pilots, and Baltica has no school to train them. Cadets go abroad on courses paid for by "
          "the treasury, and the best return as instructors. It takes five years to build a cadre that can fly in Baltican "
          "winters. Until then the flight depends on foreign instructors, who are expensive and leave whenever their contracts "
          "end.",
          ('air', 'training'), after=('air_interceptor_flight',), reward=(Idea('pilot_contracts'),)),
    Focus('air_radar_ring', 'A Radar Ring Around Silvius',
          "The gun plan depends on seeing aircraft early, so radar posts on the hills around Silvius and on the coastal plain are "
          "linked to one control room under the capital. The ring watches day and night. It sees well beyond Baltica's "
          "frontiers, which the neighbours notice, and the government assures them that it watches the sky and not their "
          "territory.",
          ('radar', 'command'), after=('air_ground_guns',),
          reward=(SwapIdea('ground_air_defence', 'radar_ring'), Build('radar_station', 1, 0))),
    Focus('air_heated_hangars', 'Warm Hangars for Winter Visitors',
          "Foreign transport aircraft that land at Silvius in winter often cannot leave for days, because their engines freeze "
          "overnight. Heated hangars and engine warmers make the airfield a reliable stop for relief and cargo flights. Landing "
          "fees pay for part of the work. The army notes that any hangar warm enough for a visitor is warm enough for aircraft of "
          "its own.",
          ('runway', 'shelter'), after=('air_runway_ploughs',), reward=(Build('air_base', 1, 0),)),
    Focus('air_winter_exercise', 'A Winter Air Exercise',
          "Whichever answer Baltica chose, the airfield hosts a winter exercise each year: transports landing in snow, the "
          "interceptors or the guns tracking practice targets towed by a hired aircraft, and the radar room plotting everything. "
          "The exercise is small. Observers come from abroad, and Baltica learns more about its own weak points in one week than "
          "in a year.",
          ('air', 'medal'), after_any=('air_foreign_courses', 'air_radar_ring'), reward=(XP('air', 25), WarSupport(0.02))),
))

NEIGHBOURS = Branch('nbr', 'Three Neighbours and the Sea', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('nbr_frontier_atlas', 'An Atlas of the Frontiers',
          "Baltica's longest land frontier runs from the hills of Silvius to the sea along Yuktobania, a country many times its "
          "size governed by its communist party. Shorter frontiers face the small republics of Malynea and Seterano, the second "
          "across mountains. The foreign office compiles everything it knows about all three into one atlas, and is alarmed by how thin "
          "the volume turns out to be.",
          ('diplomacy', 'document'), reward=(Idea('frontier_office'), Event('frontier_table'))),
    Focus('nbr_long_frontier_trade', 'Trade Across the Long Frontier',
          "The first posture treats the long frontier as an opportunity. Customs posts open longer hours and Baltican works offer "
          "spare parts and civilian goods to Yuktobanian buyers. Trade grows fast. So does the share of Baltica's income that "
          "depends on one enormous customer, and every policy made in Silvius starts to be weighed against how it will be "
          "received across that line.",
          ('diplomacy', 'economy'), after=('nbr_frontier_atlas',),
          exclusive=('nbr_small_republics', 'nbr_no_favourites'), reward=(Idea('long_frontier_trade'),)),
    Focus('nbr_small_republics', 'Talks With the Small Republics',
          "The second posture looks to the two small republics. Baltica offers Malynea and Seterano regular consultations on "
          "frontier crossings, weather warnings, air reports and trade. Nothing binds anyone and no alliance is proposed. Three "
          "small democracies speaking together on practical matters are harder to ignore than three speaking apart, and the cost "
          "is the suspicion of the largest neighbour.",
          ('diplomacy', 'assembly'), after=('nbr_frontier_atlas',),
          exclusive=('nbr_long_frontier_trade', 'nbr_no_favourites'), reward=(Idea('small_republic_talks'),)),
    Focus('nbr_no_favourites', 'No Favourites on Any Frontier',
          "The third posture treats every neighbour exactly alike: the same customs rules, the same visa terms and no special "
          "arrangement with anyone. Baltica explains its policy in identical notes to all three capitals. It forgoes the trade of "
          "the first posture and the friendships of the second. In return no neighbour can say that Baltica has chosen anyone "
          "against it.",
          ('scales', 'security'), after=('nbr_frontier_atlas',),
          exclusive=('nbr_long_frontier_trade', 'nbr_small_republics'), reward=(Idea('even_handed'),)),
    Focus('nbr_common_forms', 'Yuktobanian Forms at the Posts',
          "Trucks queue for a day at the long frontier while officers on both sides inspect the same cargo. Baltican customs "
          "adopt Yuktobanian forms and inspection standards, so a cargo cleared on the far side needs only a seal check on "
          "Baltica's. The change is technical and unilateral. Some deputies still dislike the idea of a neighbour's paperwork "
          "deciding what crosses into the republic.",
          ('logistics', 'document'), after=('nbr_long_frontier_trade',),
          exclusive=('nbr_open_weather', 'nbr_identical_notes'),
          reward=(SwapIdea('long_frontier_trade', 'joint_customs'),)),
    Focus('nbr_open_weather', 'An Open Weather and Fire Watch',
          "The consultations produce a practical first step. Baltica builds weather stations, forest fire watches and avalanche "
          "posts along its frontiers and broadcasts their reports every hour on an open frequency that anyone across the line may "
          "use. Blizzards and fires do not stop at customs posts. The network costs little and saves lives in its first winter.",
          ('communications', 'peace'), after=('nbr_small_republics',),
          exclusive=('nbr_common_forms', 'nbr_identical_notes'),
          reward=(SwapIdea('small_republic_talks', 'neighbour_network'),)),
    Focus('nbr_identical_notes', 'The Policy of Identical Notes',
          "Baltica turns its even-handed practice into declared policy, read in the chamber and sent to every capital that keeps "
          "an embassy in Silvius. It promises to sell nothing to any party in a dispute among its neighbours and to let no foreign "
          "force cross its land. The declaration is cheap to make and costly to keep, and the arms works resent the orders it "
          "forbids.",
          ('peace', 'security'), after=('nbr_no_favourites',),
          exclusive=('nbr_common_forms', 'nbr_open_weather'),
          reward=(SwapIdea('even_handed', 'declared_neutrality'),)),
    Focus('nbr_pass_patrols', 'Snow Patrols on the Seterano Passes',
          "The mountain passes toward Seterano close for much of the winter, and travellers caught by blizzards depend on whoever "
          "reaches them first. Baltican snow patrols, with huts, radios and rescue teams, keep the Baltican side of the passes "
          "watched all season and answer any call for help from the slopes. The patrols cost little and earn goodwill far beyond "
          "their size.",
          ('shelter', 'medical'), after=('nbr_frontier_atlas',), reward=(Idea('pass_patrols'),)),
    Focus('nbr_attache_corps', 'Attaches in Every Neighbour Capital',
          "Baltica's foreign service has been a handful of diplomats who also handle trade. A small corps of attaches posted to "
          "the three neighbouring capitals reports on armies, harvests, prices and politics, and keeps the government from "
          "learning about its neighbours from foreign newspapers. It costs salaries, housing and secure radio, and it means "
          "Baltica will hear bad news first.",
          ('diplomacy', 'communications'), after=('nbr_frontier_atlas',), reward=(Idea('attache_corps'),)),
))

BELKA = Branch('belka', 'A War Across the World', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('belka_war_news', 'News of the Belkan War',
          "In March 1995 war breaks out around Belka, a world away from Baltica's frontiers. The fighting reaches Silvius through "
          "prices: fuel and grain rise on the foreign exchanges, insurers add premiums to every cargo and arms buyers the works "
          "have never met begin to call. The government must decide how a small arms-making country behaves when someone else's "
          "war is good for business.",
          ('missile', 'communications'), requires=(After('1995.3.25'),),
          reward=(Idea('war_prices'), Event('belkan_war_far'))),
    Focus('belka_no_sales', 'No Arms to the Belligerents',
          "The first answer forbids every export of arms or munitions to any country at war, and to any buyer who might resell to "
          "one. The works lose the largest orders they have seen in years, and some foreign creditors call in loans. In return "
          "Baltica stays out of every belligerent's ledger, and no postwar government can accuse it of arming the other side.",
          ('peace', 'scales'), after=('belka_war_news',), exclusive=('belka_war_orders',), reward=(Idea('war_embargo'),)),
    Focus('belka_war_orders', 'Fill the Wartime Orders',
          "The second answer lets the works sell to any licensed buyer whose government is not under an embargo, and the order "
          "book fills within weeks. Overtime returns to all three arms lines and the treasury collects export taxes it had almost "
          "forgotten. Some cargoes will end up at the front. Everyone in the chamber knows it, and the opposition says so at every "
          "sitting.",
          ('missile', 'industry'), after=('belka_war_news',), exclusive=('belka_no_sales',), reward=(Idea('war_orders'),)),
    Focus('belka_risk_pool', 'A State Pool for War Risk',
          "Insurers abroad raise premiums on every Baltican cargo, whatever its destination, because underwriters cannot tell one "
          "small flag from another at this distance. A state pool that insures Baltican hulls against war risk at fixed rates "
          "keeps the merchant fleet sailing. The treasury carries the risk. If one ship is lost the pool can pay; if several are "
          "lost the budget cannot.",
          ('navy', 'scales'), after=('belka_war_news',), reward=(Idea('war_risk_pool'),)),
    Focus('belka_lumen_treaty', 'The Lumen Treaty Reaches Silvius',
          "In June 1995 a treaty signed in Lumen ends the Belkan War. Prices fall back over the summer, insurers drop their "
          "premiums and the arms buyers stop calling as suddenly as they began. The works must decide what to do with lines that "
          "ran at wartime rates. The government must decide what the war taught a country that took no part in it.",
          ('peace', 'document'), after=('belka_war_news',), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_prices'), Stability(0.02))),
    Focus('belka_staff_study', 'What a Distant War Teaches',
          "Baltican officers read every report of the Belkan War that reaches them, from foreign newspapers, attaches and the "
          "works' own buyers. They study how a small republic was nearly overrun within days of the outbreak, and how fuel depots "
          "and bridges became the first targets. The lessons go into a staff study the territorial service will argue about for "
          "the rest of the decade.",
          ('document', 'command'), after_any=('belka_no_sales', 'belka_war_orders'),
          reward=(Research('land_doctrine', 0.5, 1), XP('army', 10))),
    Focus('belka_belkan_buyers', 'Belka Returns to the Market',
          "In this outcome Belka has come out of the war on the winning side of the peace. Belkan buyers return with long lists "
          "of spare parts and machine tools, and Belkan banks offer credit to suppliers who stayed out of the fighting. The works "
          "can take the orders. Osean buyers will notice which suppliers do, and their governments keep lists of their own.",
          ('economy', 'diplomacy'), after=('belka_lumen_treaty',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(Idea('belkan_credit'),)),
    Focus('belka_allied_buyers', 'Buyers From the Allied Side',
          "In this outcome Belka has lost, and the allied governments shape the peace. Buyers who relied on Belkan suppliers for "
          "spare parts and machine tools look elsewhere, and small neutral works appear on their lists. Their orders arrive with "
          "inspection clauses attached. Baltica can accept them, or keep its works free of foreign inspectors and its order book "
          "thin.",
          ('diplomacy', 'industry'), after=('belka_lumen_treaty',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Idea('allied_buyers'),)),
))

ASTEROID = Branch('sky', 'Ulysses Over the Cold Coast', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_word_from_astronomers', 'Word From the Astronomers',
          "By April 1996 the danger first raised by astronomers in December 1994 is a certainty: the FCU announces that Ulysses "
          "will hit the Earth, without saying where. For Baltica the planning problem is particular. Its capital stands on solid "
          "rock, its winters can kill anyone left in the open and its harbour ices over. Each ministry drafts a scheme, and all "
          "of them reach for one budget.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),), reward=(Idea('impact_planning'), Event('ulysses_word'))),
    Focus('sky_rock_of_silvius', 'Shelters in the Rock of Silvius',
          "The first plan cuts shelter halls into the rock beneath Silvius, heated by the works and stocked for weeks, large "
          "enough to take in families from the plain and the coast as well as the capital. Rock is the best shelter there is. "
          "Cutting it is slow, and everyone outside the capital is told to travel to the hill when the warning comes, whatever "
          "the weather.",
          ('shelter', 'meteor'), after=('sky_word_from_astronomers',), exclusive=('sky_warn_and_disperse',),
          reward=(Idea('rock_shelters'),)),
    Focus('sky_warn_and_disperse', 'Warn Early, Disperse Wide',
          "The second plan spends on warning rather than concrete: observing time bought abroad, sirens in every village and a "
          "dispersal plan that moves people out of large buildings into heated shelters spread across all five provinces. It "
          "saves more lives if the warning comes in time. In midwinter, a dispersal ordered too early could kill people by "
          "itself.",
          ('telescope', 'refugees'), after=('sky_word_from_astronomers',), exclusive=('sky_rock_of_silvius',),
          reward=(Idea('dispersal_plan'),)),
    Focus('sky_cold_stores', 'Grain and Medicine in Store',
          "If fragments fall anywhere near, the harbour could close and the frontier crossings with it, and Baltica buys much of "
          "its grain and medicine abroad. A reserve of grain, seed and medicine, held in cold stores across the provinces, buys "
          "the country a year of self-reliance. Filling it raises food prices for a season, and the shops say so loudly.",
          ('shelter', 'logistics'), after=('sky_word_from_astronomers',), reward=(Idea('cold_stores'),)),
    Focus('sky_deep_wards', 'Hospitals Below Ground',
          "Hospitals are the buildings a country can least afford to evacuate. Moving operating theatres, generators and wards for "
          "the critically ill into reinforced basements in Silvius and at the harbour lets them keep working through any strike "
          "or blizzard. Surgeons lose months while their departments move. The doctors support the plan and complain about the "
          "timetable.",
          ('medical', 'shelter'), after_any=('sky_rock_of_silvius', 'sky_warn_and_disperse'), reward=(Idea('deep_wards'),)),
    Focus('sky_roche_night', 'A Night Spent Underground',
          "Ulysses crosses the Roche limit of the Earth on 8 July 1999, and Baltica spends that night underground or beside a "
          "radio. Three years of preparation come down to hours the government cannot influence at all. Whatever falls, and "
          "wherever it falls, the country will wake to a changed world and to the bill for every scheme it paid for.",
          ('meteor', 'communications'), after=('sky_word_from_astronomers',), requires=(After('1999.7.8'),),
          reward=(Event('roche_watch'), WarSupport(0.02))),
    Focus('sky_relief_column', 'A Relief Column for Others',
          "If Ulysses spares Baltica, others will not be so lucky. The government prepares a relief column of trucks, field "
          "kitchens, heated tents and medical teams from the territorial service, ready to go wherever it is invited. It has no "
          "destination yet and claims none. Keeping it ready costs fuel and men, and offering it ends Baltica's comfortable "
          "distance from other people's disasters.",
          ('refugees', 'medical'), after=('sky_roche_night',), reward=(Idea('relief_column'),)),
))

CENTURY = Branch('century', 'The Turn of the Century', 2000, 'FOCUS_FILTER_POLITICAL', (
    Focus('century_great_power_thaw', 'Osea and Yuktobania in One Project',
          "Osea and Yuktobania announce in October 1999 that they will jointly convert the Arkbird to clear debris from "
          "satellite orbits. To a small republic on the frontier of the larger partner, the technical details matter less than "
          "the handshake. Great powers busy cooperating leave less room for frontier tension, and the government drafts its "
          "budget for the new decade on that hope.",
          ('satellite', 'peace'), requires=(After('1999.10.8'),), reward=(Idea('thaw_budget'),)),
    Focus('century_shorter_service', 'Shorter Reserve Service',
          "One camp argues that the thaw lets Baltica shorten reserve service, release young men to the works and the harbour and "
          "spend the savings on schools and housing. The territorial service would shrink to a training cadre. If the thaw holds, "
          "the country grows richer. If it does not, rebuilding the reserve will take years that a crisis might not allow.",
          ('civil', 'economy'), after=('century_great_power_thaw',), exclusive=('century_whole_reserve',),
          reward=(Idea('peace_dividend'),)),
    Focus('century_whole_reserve', 'Keep the Reserve Whole',
          "The other camp argues that thaws between great powers come and go, while Baltica's frontier stays exactly where it is. "
          "The reserve keeps its full term of service and its winter exercises, and the savings from the thaw go into equipment "
          "rather than schools. The country stays ready, and young men who would rather be working say so at every election.",
          ('security', 'training'), after=('century_great_power_thaw',), exclusive=('century_shorter_service',),
          reward=(Idea('steady_reserve'),)),
    Focus('century_graduates', 'Engineers Who Stay Home',
          "Young engineers trained at the works leave for better pay abroad as soon as their apprenticeships end. Bursaries that "
          "repay a student's fees for every year spent working in Baltica, together with housing near the works, keep a growing "
          "share at home. The scheme is expensive and some graduates leave anyway. Those who stay become the first generation to "
          "run the works without foreign advisers.",
          ('science', 'training'), after=('century_great_power_thaw',), reward=(Idea('graduate_bursaries'),)),
    Focus('century_ballot_2003', 'The Ballot of November 2003',
          "Under the chamber cabinet, Baltica votes again in November 2003, the fourth ballot since the mandate of 1987 expired. "
          "The campaign is fought over the thaw, the reserve, the Usean war and the pensions of the works families. Whoever wins, "
          "the count confirms that the republic changes its governments on schedule and by vote, rather than by crisis.",
          ('ballot', 'assembly'), after=('century_great_power_thaw',),
          requires=(HasFlag('path_chamber'), After('2003.11.1')),
          reward=(TimedIdea('campaign_season', 180), Stability(0.03))),
    Focus('century_usean_charters', 'Charters Refused Toward Usea',
          "When Erusea invades San Salvacion in the summer of 2003 and takes Stonehenge, the war seems a continent away from "
          "Silvius. It reaches Baltica by sea within days: underwriters withdraw cover on the lanes to Usea, buyers on both sides "
          "telephone the works, and Baltican masters turn down charters toward the fighting. Once more a distant war sets the "
          "price of a Baltican winter.",
          ('navy', 'missile'), after=('century_great_power_thaw',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(TimedIdea('usean_premiums', 365), Event('usean_cargo'))),
    Focus('century_usea_averted', 'The Usean Lanes Stay Calm',
          "In this outcome war in Usea has been averted, and the lanes toward Usean ports carry ordinary traffic at ordinary "
          "premiums. Baltican masters accept Usean charters again and the works keep their spare parts customers on the "
          "continent. The government quietly retires the contingency plans it drafted, and the harbour owners ask whether the "
          "war-risk surcharge can be dropped as well.",
          ('navy', 'peace'), after=('century_great_power_thaw',), requires=(HasGlobal('ac_ucw_war_averted'),),
          reward=(TimedIdea('calm_lanes', 365),)),
    Focus('century_usean_wagons', 'Rail Wagons for a Rebuilt Usea',
          "In this outcome the ISAF has won and Usea begins to rebuild its railways, ports and power lines. Baltican works bid "
          "for orders of wagons, pumps and spare parts, the kind of goods they can make without new tooling. Payment stretches "
          "over years. The orders still keep the lines busy at a moment when military buyers everywhere are cutting back.",
          ('rebuild', 'rail'), after=('century_usean_charters',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(Idea('usean_rebuild'),)),
    Focus('century_erusean_offices', 'Erusean Offices in Usean Ports',
          "In this outcome Erusea has won its war, and the trade offices that now run Usean ports set fresh terms for foreign "
          "shippers: inspections at the quay and preferred prices for favoured suppliers. Baltican owners must decide whether "
          "access is worth the conditions. Accepting keeps hulls working. It also binds Baltican trade to authorities that many "
          "older customers distrust.",
          ('diplomacy', 'scales'), after=('century_usean_charters',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Idea('erusean_terms'),)),
    Focus('century_reserve_review', 'The Reserve in a New Century',
          "With the service at full strength and the reserve question settled, the territorial staff turns its best instructors "
          "into a permanent cadre that rotates through every depot. Reservists train on current equipment rather than whatever "
          "the depot happens to hold. The cadre costs career salaries the service has never paid before, and it keeps the reserve "
          "from going stale.",
          ('training', 'command'), after_any=('century_shorter_service', 'century_whole_reserve'),
          requires=(HasFlag('service_ready'),), reward=(Idea('reserve_cadre'), XP('army', 15))),
    Focus('century_independent_audit', 'Baltica Takes Stock in 2005',
          "In 2005 the cabinet office in Silvius commissions independent auditors to examine everything the republic has built "
          "since the ballot of 1991: its laws, its works, its harbour, its reserve and its shelters. The auditors come from the "
          "universities and the courts, not the ministries. Their report closes this era of the programme with figures instead "
          "of slogans, and the next government inherits them.",
          ('document', 'scales'), after_any=('century_shorter_service', 'century_whole_reserve'),
          requires=(HasFlag('order_settled'), After('2005.1.1')),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (REPUBLIC, SILVIUS, WORKS, ORE, HARBOUR, SERVICE, AIRFIELD, NEIGHBOURS, BELKA, ASTEROID, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('snow_brigades_out', 'Call Out the Snow Brigades',
                'Pays the volunteer brigades in fuel vouchers to clear lanes, clinic doors and bus stops through a bad spell. '
                'Repeatable once a winter.',
                25, (TimedIdea('snow_brigade_call', 90),), requires=(Completed('hill_snow_brigades'),), cooldown=365),
    DecisionDef('works_overtime', 'Overtime on All Lines',
                'Runs every line at overtime rates for three months to clear a backlog of orders, at the cost of tired crews. '
                'Repeatable twice a year.',
                35, (TimedIdea('overtime_lines', 90),), requires=(Completed('works_orders_book'),), cooldown=180),
    DecisionDef('second_coast_radar', 'A Second Radar on the Coast',
                'Adds a second radar post to watch the far approaches of the harbour. A one-time charge on the harbour budget.',
                60, (Build('radar_station', 1, 0),), requires=(Completed('harbour_coast_radar'),)),
    DecisionDef('runway_extension', 'Extend the Runway Again',
                'Adds a parallel taxiway and a longer runway so heavy transports can land in winter. A one-time works programme.',
                70, (Build('air_base', 1, 0),), requires=(Completed('air_runway_ploughs'),)),
    DecisionDef('reserve_week', 'A Week With the Reserve',
                'Calls one year group of reservists to the depots for a week of winter drill. Repeatable once a year; '
                'employers complain.',
                30, (TimedIdea('reserve_week', 60), XP('army', 10)), requires=(Completed('guard_reserve_register'),),
                cooldown=365),
    DecisionDef('cold_store_rotation', 'Rotate the Cold Stores',
                'Sells the oldest grain from the cold stores at low prices and refills them from the new harvest. Repeatable '
                'once a year.',
                20, (Stability(0.02),), requires=(Completed('sky_cold_stores'),), cooldown=365),
)
