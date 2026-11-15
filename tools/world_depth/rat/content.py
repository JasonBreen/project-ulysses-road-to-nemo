"""Ratio (RAT): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party at 70
percent popularity with elections not allowed after the vote dated 1 January 1991, fascism 16,
neutrality 11 and communism 3 percent, stability 0.85, war support 0.40), the unnamed National
Administration office and the council-office institution profile, the country names, the five
1991 states with their localised names and victory points, the map facts read from
map/definition.csv, map/provinces.bmp and map/railways.txt, the inherited Ustio-Ratio dispute
over Tyrann Valley, Boikos and the Jeszczed Mountains, and the global flags other mod scripts
already set. Official: ACES Chronicle rows used only as date anchors, each cited by its exact
key. Everything else, including every Ratian choice, office, idea, building, decision and event,
is provisional gameplay. The tree never transfers a state, adds a core or claim, declares war or
makes peace: the dispute's outcomes stay with the inherited Ustio scripts.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='RAT', name='Ratio', root='world', package='rat',
                  themes=('assembly', 'industry', 'security'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no after a last election dated 1 January '
           '1991 (election_frequency 48); popularities democratic 70, fascism 16, neutrality 11, communism 3; stability 0.85 '
           'and war support 0.40; ideas nuke_lvl_1 and generic_defensive_army_1; grand doctrines superior_firepower, '
           'new_fleet_in_being and new_operational_integrity; tech_mountaineers among the starting technology. The starting '
           'leader is the unnamed National Administration office (RAT_ac_government_office, centrism), whose description says '
           'its 1991 holder has not been established; the institution profile is a council office (ac_pol_form_council_office). '
           'The tree never names a holder.',
           'mod/2985041246/history/countries/RAT - Ratio.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/common/scripted_effects/ac_politics.txt; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Geography: 1991 states 306, 388 (capital), 419, 472 and 489. State 388 is Centrum (large city; forest, hills and '
           'mountain; steel 38, oil 12, tungsten 12; three civilian and three military factories, the fuel silo, air base 4). '
           'State 306 is a large city of plains, forest and mountain whose Earth-template caption the regional labels replaced '
           'with Ratio District A; the tree calls it by its largest victory point, Dormakaj (three civilian and three military '
           'factories, air base 6, oil 12, tungsten 13). State 419 is Troton Mountains (city; mountain and hills; steel 26, '
           'chromium 17, tungsten 16; naval bases at Roshniku and Isakas; two dockyards). State 472 is Ratio Valley (rural; five '
           'provinces, two on the coast; one civilian factory). State 489 is Zulian Coast (city; plains and urban; oil 33, steel '
           '31; naval bases including Sukaxhija; two dockyards). Land neighbours from map/provinces.bmp: Ustio (Boikos, against '
           'Dormakaj), Gebet (Dormakaj), Wiesmont (Dormakaj, Centrum, Troton Mountains) and Sapin (Dormakaj, Centrum, Ratio '
           'Valley, Zulian Coast). Railways from map/railways.txt: a level-3 trunk from Gebet through Dormakaj to Centrum, '
           'level-2 lines from Centrum to the Troton Mountains, Ratio Valley and the Zulian Coast, and level-1 links into Boikos, '
           'Wiesmont and Sapin. No other place is named.',
           'mod/2985041246/history/states/306-State_306.txt, 388-State_388.txt, 419-State_419.txt, 472-State_472.txt, '
           '489-State_489.txt; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/map/railways.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: a retained authored army of four tank, four infantry and four motorised '
           'divisions with 300 modern tanks in stock; 11 civilian, 10 military and 4 naval factories; 48 fighters and 12 support '
           'aircraft; three destroyers and one submarine; 200 convoys; fiscal profile GDP 536.79, debt ratio 0.3, collection '
           '0.85. Fictional calibration, not canon national accounts or order of battle.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'The Ustio-Ratio dispute: Tyrann Valley (336), Boikos (365) and the Jeszczed Mountains (376) are owned by Ustio in 1991 '
           'with cores of both countries; Ustio texts say Belka took them from Ratio in its years of expansion, that they stayed '
           'with Ustio after the 1988 review, that their people are mostly Ratian and that Ratio never renounced the claim '
           '(ustio.1, UST_deal, ac_news_event.2). Inherited outcomes: the purchase (UST_deal), Ratio pledging help against Belka '
           '(ustio.6), Ratian partisans and border incidents (UST_vs_RAT_resistance, ustio.7 to ustio.11), the Yuktobanian '
           'referendum proposal (ustio.14), Sapin choosing a side (sapin_diplomacy.1) and the war flagged by first_ustian_war. '
           'The CANON_LEDGER row keeps all of this mod provenance. This tree reads only first_ustian_war and never moves a state, '
           'core or claim, starts a war or ends one.',
           'mod/2985041246/events/Ustio.txt; mod/2985041246/common/national_focus/UST_shared.txt; '
           'mod/2985041246/localisation/english/country_UST_l_english.yml; mod/2985041246/events/Sapin.txt; '
           'mod/2985041246/common/on_actions/ac_on_actions.txt; docs/CANON_LEDGER.md'),
    Source('Mod provenance',
           'Neighbour consistency: no other world-depth spec names Ratio, and Ustio, Gebet, Wiesmont and Sapin have no '
           'world-depth spec. The tree keeps faith with the inherited Ustio texts: Ratio friendly to Ustio and nowhere near '
           'friendly with Belka (UST_deal, UST_ask_ratio_for_help), Ratian partisans outside Centrum control, and the purchase '
           'and referendum answers belonging to Ustio. It claims no action, consent or outcome for any neighbour.',
           'mod/2985041246/localisation/english/country_UST_l_english.yml'),
    Source('Official',
           'Date context: the Republic of Ustio gains its independence. Background to the valleys question only; the Chronicle '
           'says nothing about the dispute.', '1988 / 05.12'),
    Source('Official',
           'Belka sells its eastern territory to neighbouring eastern nations, which the Chronicle does not name. Regional '
           'pressure only; no Ratian purchase from Belka is claimed.', '1991 / 08.29'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Date gate of the war branch; Ratio takes no part.', '1995 / 03.25'),
    Source('Official',
           'An assault on Model, a border city in Gebet. Premise of the Gebet line focus, which also reads the mod flag '
           'ac_bwr_model.', '1995 / 03.27'),
    Source('Official',
           'Nearly all of Ustio falls under Belkan control. Premise of the Ustian front focus, which also reads the mod flag '
           'ac_bwr_monte_rosa.', '1995 / 03.30'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Premise of the fallout focus, which also reads '
           'belka_dropped_nukes; no fallout in Ratio is claimed.', '1995 / 06.06'),
    Source('Official',
           'A treaty is signed in Lumen and the Belkan War ends. Date gate of the stand-down focus, which also waits until '
           'belkan_war_is_happening is clear.', '1995 / 06.20'),
    Source('Official',
           'The President of the FCU announces that Ulysses will impact the Earth. Date gate of the Ulysses branch; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries as aggressor squadrons. Date gate of the '
           'aggressor focus; no individual is named and no hire by Ratio is claimed as fact.', '1998 / 06.19'),
    Source('Official',
           'Ulysses passes through the Roche limit of the Earth. Date gate of the recovery crews focus; no damage in Ratio is '
           'claimed.', '1999 / 07.08'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: first_ustian_war (set by ustio.12, the UST_ratio_war_timer mission and '
           'UST_strike_first; cleared by ustio.19 and ustio.20), ac_bwr_model and ac_bwr_monte_rosa '
           '(common/scripted_effects/ac_belkan_record.txt), belkan_war_is_happening, belka_won_belkan_war, belka_lost_belkan_war '
           'and belka_dropped_nukes (events/Belka.txt and common/decisions/BLK_decisions.txt), and ac_ucw_war_started '
           '(common/scripted_effects/ac_ucw.txt). Outcome reactions are leaf focuses, so no outcome blocks the tree.',
           'mod/2985041246/events/Ustio.txt; mod/2985041246/common/decisions/UST_decisions.txt; '
           'mod/2985041246/common/scripted_effects/ac_belkan_record.txt; mod/2985041246/events/Belka.txt; '
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Ratian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices are '
           'collective and unnamed; no border, core, claim, war, peace, annexation or faction effects; buildings only in the five '
           '1991 states and within their free slots.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the council
    IdeaDef('standing_mandate', 'The Standing Mandate', 'The council governs on the January 1991 vote, and no date is set for the next one.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('assembly', 'document')),
    IdeaDef('district_hearings', 'Seasonal District Hearings','Council members sit in each district every season and take petitions in public.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('civil', 'assembly')),
    IdeaDef('ballot_calendar', 'A Published Ballot Calendar', 'The council has named the day the polls reopen and the rules for standing.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('campaign_season', 'A Season of Campaigning', 'Registered parties canvass the five districts; ministries govern with one eye on the count.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'civil')),
    IdeaDef('open_council', 'The Open Council Charter', 'An elected council answers to the districts, with a court to read its charter.',
            {'stability_factor': 0.07, 'political_power_factor': 0.06, 'research_speed_factor': 0.02}, ('ballot', 'scales')),
    IdeaDef('rotating_chairs', 'Rotating Council Chairs', 'Ministries take turns in the chair, and the council governs without a ballot.',
            {'political_power_gain': 0.15, 'stability_factor': 0.02}, ('assembly', 'command')),
    IdeaDef('presidium_rule', 'Rule by the Presidium', 'Five ministry heads hold the seals, sign the budget and name the prefects.',
            {'political_power_gain': 0.20, 'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('valley_front', 'The Valley Front', 'A nationalist movement built on the lost valleys fills the Dormakaj squares.',
            {'war_support_factor': 0.07, 'stability_factor': -0.04, 'political_power_gain': 0.05}, ('security', 'ballot')),
    IdeaDef('torchlight_marches', 'Monthly Torchlight Marches', 'The Front marches through Centrum every month, and the shops along the route close early.',
            {'war_support_factor': 0.05, 'stability_factor': -0.02}, ('medal', 'security')),
    IdeaDef('restoration_decrees', 'Decrees of Restoration', 'Government by committee decree in the name of the lost valleys.',
            {'war_support_factor': 0.10, 'stability_factor': 0.04, 'army_core_defence_factor': 0.05, 'consumer_goods_factor': 0.04}, ('security', 'command')),
    # the valleys
    IdeaDef('valleys_question', 'The Valleys Question', 'Tyrann Valley, Boikos and the Jeszczed Mountains lie across the Ustian line, and every party has an answer.',
            {'war_support_factor': 0.03, 'stability_factor': -0.02}, ('gate', 'assembly')),
    IdeaDef('kin_offices', 'Offices for Kin Across the Line', 'Papers, pensions and school places for families with relatives in the valleys.',
            {'stability_factor': 0.03, 'political_power_gain': -0.03}, ('refugees', 'document')),
    IdeaDef('purchase_fund', 'The Valleys Purchase Fund', 'Money set aside to buy the valleys back if Ustio ever names a price.',
            {'stability_factor': 0.04, 'political_power_factor': -0.05, 'consumer_goods_factor': 0.02}, ('economy', 'diplomacy')),
    IdeaDef('observer_appeal', 'An Appeal for Observers', 'Ratio asks for a supervised vote in the valleys and promises to accept the count.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('scales', 'diplomacy')),
    IdeaDef('pressed_claim', 'The Claim Pressed', 'The valleys are named in every speech, and the frontier divisions stand ready.',
            {'war_support_factor': 0.07, 'army_core_defence_factor': 0.05, 'stability_factor': -0.03}, ('security', 'gate')),
    IdeaDef('valley_bonds', 'Valley Bonds in Circulation', 'Banks, pension funds and patriotic savers hold the long bonds behind the purchase fund.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('economy', 'document')),
    IdeaDef('resettlement_fund', 'The Resettlement Fund', 'Moving costs paid for anyone who chooses to cross the line and settle on the other side.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('refugees', 'rail')),
    IdeaDef('observer_missions', 'Observer Missions Welcomed', 'Foreign observers travel the Ratian side of the line with open papers.',
            {'stability_factor': 0.04}, ('peace', 'document')),
    IdeaDef('war_budget', 'The War Budget', 'Ratio is fighting Ustio, and every ministry pays for the front first.',
            {'war_support_factor': 0.08, 'production_speed_arms_factory_factor': 0.08, 'consumer_goods_factor': 0.05}, ('security', 'economy')),
    IdeaDef('line_commission', 'The Boikos Line Commission', 'A standing desk with Ustian officials for crossings, rail traffic and incidents.',
            {'stability_factor': 0.05, 'army_core_defence_factor': 0.03}, ('peace', 'gate')),
    # steel
    IdeaDef('furnace_ledger', 'The Furnace Ledger', 'Every furnace, rolling mill and arms hall has been counted and costed.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.05}, ('industry', 'document')),
    IdeaDef('alloy_mills', 'Troton Alloy Mills', 'Chromium and tungsten from the Troton harden Centrum steel at home.',
            {'production_factory_max_efficiency_factor': 0.04, 'industrial_capacity_factory': 0.03}, ('tools', 'industry')),
    IdeaDef('works_councils', 'Shop Councils in the Mills', 'Elected shop councils agree shifts, safety rules and bonuses with management.',
            {'stability_factor': 0.04, 'production_factory_efficiency_gain_factor': 0.02}, ('assembly', 'industry')),
    IdeaDef('armour_plate', 'Armour Plate Contracts', 'The Centrum mills roll plate for the tank parks before anything else.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04}, ('industry', 'security')),
    IdeaDef('rail_steel', 'Rails and Girders First', 'Mill output goes to bridges, rails and the frames of new halls.',
            {'production_speed_infrastructure_factor': 0.12, 'production_speed_industrial_complex_factor': 0.06}, ('rail', 'industry')),
    IdeaDef('ore_trade', 'Ore Down the Valley', 'Troton ore and Centrum billets sold abroad through the Zulian ports.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02, 'production_speed_buildings_factor': 0.03}, ('logistics', 'economy')),
    # rail
    IdeaDef('spine_timetable', 'The Spine Timetable', 'One timetable for the line from the Gebet frontier to the Zulian Coast.',
            {'production_speed_infrastructure_factor': 0.10}, ('rail', 'document')),
    IdeaDef('troop_trains', 'Troop Trains First', 'Military traffic takes the first path on every Ratian line.',
            {'army_speed_factor': 0.04, 'supply_consumption_factor': -0.05}, ('rail', 'security')),
    IdeaDef('passenger_rail', 'Passengers Before Freight', 'Cheap fares and fixed passenger paths on the spine.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('rail', 'civil')),
    IdeaDef('gebet_trunk', 'The Gebet Through-Running Pact', 'Freight crosses into Gebet on the heaviest Ratian line without unloading.',
            {'consumer_goods_factor': -0.03, 'production_speed_buildings_factor': 0.04}, ('rail', 'diplomacy')),
    # coast
    IdeaDef('harbour_board', 'The Board of Three Harbours', 'Roshniku, Isakas and Sukaxhija share one pilotage and customs board.',
            {'navy_org_factor': 0.03, 'consumer_goods_factor': -0.02}, ('navy', 'document')),
    IdeaDef('escort_squadron', 'The Ore Escort Squadron', 'Destroyers organised to shepherd ore carriers and tankers along the coast.',
            {'navy_org_factor': 0.06, 'naval_speed_factor': 0.04}, ('navy', 'logistics')),
    IdeaDef('submarine_school', 'The Roshniku Submarine School', 'Coastal submarine crews trained in home waters.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.04}, ('submarine', 'training')),
    IdeaDef('zulian_leases', 'Zulian Oil Leases', 'The coastal oil fields leased on published terms and fixed royalties.',
            {'production_speed_buildings_factor': 0.05, 'political_power_gain': 0.05}, ('economy', 'tools')),
    # armour
    IdeaDef('tank_parks', 'The Tank Park Registers', 'Every hull in the parks is listed by its true state of repair.',
            {'army_org_factor': 0.03}, ('security', 'document')),
    IdeaDef('gunnery_ranges', 'A Full Live-Fire Season', 'Every tank crew fires its whole annual allowance on the ranges.',
            {'experience_gain_army_factor': 0.10}, ('training', 'security')),
    IdeaDef('armoured_fist', 'The Plains Armour Doctrine', 'The tank divisions are concentrated on the Dormakaj plain.',
            {'army_attack_factor': 0.05, 'army_speed_factor': 0.04}, ('security', 'command')),
    IdeaDef('mountain_bastions', 'Bastions in the Troton', 'Dug-in infantry and engineers hold the passes, with armour behind.',
            {'army_defence_factor': 0.06, 'army_core_defence_factor': 0.06}, ('security', 'shelter')),
    IdeaDef('motor_reserve', 'The Centrum Motor Reserve', 'Motorised divisions held centrally and moved by road and rail.',
            {'planning_speed': 0.10, 'supply_consumption_factor': -0.05}, ('logistics', 'command')),
    IdeaDef('hull_rebuild', 'The Hull Rebuild Programme', 'Older tanks rebuilt with alloy plate from the strategic reserve.',
            {'army_defence_factor': 0.04, 'production_speed_arms_factory_factor': 0.05}, ('tools', 'security')),
    # air
    IdeaDef('air_review', 'The Review of Sixty Airframes', 'The air arm knows what it can defend and what it cannot.',
            {'experience_gain_air_factor': 0.04}, ('air', 'document')),
    IdeaDef('interceptor_wing', 'The Frontier Interceptor Wing', 'Fighters at readiness and ground controllers guarding the frontier airspace.',
            {'air_superiority_efficiency': 0.06, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('support_wing', 'The Armour Support Wing', 'Pilots trained to strike what the tank divisions call in.',
            {'air_mission_efficiency': 0.06, 'experience_gain_air_factor': 0.06}, ('air', 'security')),
    IdeaDef('aggressor_course', 'Two Seasons Against Aggressors','Hired instructors fly against Ratian pilots for two seasons.',
            {'experience_gain_air_factor': 0.10, 'air_superiority_efficiency': 0.03}, ('medal', 'air')),
    # the Belkan War next door
    IdeaDef('war_room', 'The Centrum War Room', 'Staff officers follow the war beyond the western hills around the clock.',
            {'army_core_defence_factor': 0.04, 'war_support_factor': 0.03}, ('command', 'communications')),
    IdeaDef('gebet_alarm', 'Alarm on the Gebet Line', 'Gebet is under attack, and every train from the frontier is searched.',
            {'army_core_defence_factor': 0.05, 'consumer_goods_factor': 0.02}, ('security', 'rail')),
    IdeaDef('trunk_diversion', 'Diverted Trunk Freight', 'Freight rerouted from the Gebet trunk to the spine and the ports.',
            {'production_speed_infrastructure_factor': 0.08, 'consumer_goods_factor': 0.02}, ('logistics', 'rail')),
    IdeaDef('boikos_front_watch', 'Readiness on the Boikos Line', 'The western divisions stand at full readiness facing a front in Ustio.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.03}, ('security', 'gate')),
    IdeaDef('crossing_service', 'The Crossing Reception Service', 'Schools and warehouses at the crossings register, feed and house arrivals.',
            {'stability_factor': 0.02, 'political_power_gain': -0.03}, ('refugees', 'shelter')),
    IdeaDef('supply_corridor', 'The Dormakaj Supply Corridor', 'Food, fuel and medicine sold to Ustio and carried to the line; no Ratian unit crosses.',
            {'production_speed_arms_factory_factor': 0.05, 'war_support_factor': 0.04}, ('logistics', 'diplomacy')),
    IdeaDef('closed_frontier', 'A Closed and Guarded Frontier', 'No transit, no arms sales and every crossing manned.',
            {'army_core_defence_factor': 0.08, 'stability_factor': 0.03}, ('security', 'peace')),
    IdeaDef('hospital_trains', 'Hospital Trains West', 'Ratian doctors bring the wounded and sick out of Boikos by rail.',
            {'stability_factor': 0.03, 'war_support_factor': 0.02}, ('medical', 'rail')),
    IdeaDef('frontier_alert', 'Frontier on Alert', 'The garrisons of every frontier stand to for a season.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.02}, ('security', 'radar')),
    IdeaDef('fallout_watch', 'Daily Fallout Sampling','Air, water and milk sampled daily across the western districts.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02}, ('medical', 'telescope')),
    IdeaDef('wary_neighbour', 'A Wary Western Watch', 'Defence plans now assume a victorious Belka just beyond Ustio.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.04}, ('security', 'command')),
    IdeaDef('rebuild_orders', 'Northern Reconstruction Contracts','Steel, cement and rolling stock sold to rebuild the war-torn north.',
            {'industrial_capacity_factory': 0.05, 'production_speed_industrial_complex_factor': 0.05}, ('rebuild', 'economy')),
    # Ulysses and the new century
    IdeaDef('sky_bulletins', 'Weekly Sky Bulletins', 'A plain bulletin about Ulysses read on the state radio every week.',
            {'stability_factor': 0.03}, ('meteor', 'communications')),
    IdeaDef('hill_cellars', 'The Hill Cellars', 'Old mine galleries and cellars under Centrum shored up and stocked.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.02}, ('shelter', 'civil')),
    IdeaDef('grain_halls', 'Full Grain Halls', 'Three months of grain, fuel and medicine held in state stores.',
            {'stability_factor': 0.04}, ('economy', 'shelter')),
    IdeaDef('evacuation_trains', 'Evacuation Timetables Inland', 'Each city quarter is paired with a numbered train and a hall in the countryside.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'refugees')),
    IdeaDef('shelter_wardens', 'Shelter Wardens in Every Block', 'Elected wardens know the cellars, the frail neighbours and the first-aid kits.',
            {'stability_factor': 0.03, 'static_anti_air_damage_factor': 0.05}, ('shelter', 'security')),
    IdeaDef('fragment_crews', 'Fragment Recovery Crews', 'District crews of engineers, doctors and rail workers stand ready.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.02}, ('rebuild', 'meteor')),
    IdeaDef('usean_orders', 'Ore Orders from a Distant War', 'Shipyards and plants at war on Usea buy Ratian ore and steel.',
            {'industrial_capacity_factory': 0.04, 'consumer_goods_factor': -0.03}, ('economy', 'navy')),
    # decisions
    IdeaDef('ore_contract', 'A Season of Ore Contracts', 'Troton ore and Centrum billets sold forward to foreign buyers.',
            {'consumer_goods_factor': -0.03, 'production_speed_buildings_factor': 0.03}, ('economy', 'logistics')),
    IdeaDef('bond_window', 'The Bond Window', 'Another tranche of valley bonds on sale at the Centrum exchange.',
            {'political_power_gain': 0.10}, ('economy', 'scales')),
    IdeaDef('relief_columns', 'Relief Columns Westward', 'Lorries from the reception halls carry food and medicine to the frontier towns.',
            {'stability_factor': 0.03}, ('refugees', 'logistics')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('elected_council', 'The Elected Council of Ratio',
           'A council chosen at the ballot box by all five districts, governing collectively through ministers answerable to its '
           'majority. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('standing_presidium', 'Presidium of the Standing Council',
           'Five ministry heads who hold the seals, sign the budget and name the district prefects, with the council kept as a '
           'debating chamber. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('restoration_committee', 'Committee of National Restoration',
           'A committee drawn from the nationalist movement and the frontier commands, governing by decree in the name of the '
           'lost valleys. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('council_session', 'A Council Without a Calendar', (
        "The council hall at Centrum fills early on the morning the ministries finally put their own mandate on the agenda. "
        "The January vote of 1991 left the democratic camp with the goodwill of roughly seven Ratians in ten, yet the "
        "administration that vote produced has suspended the next ballot indefinitely, and its ministries pass the chair among "
        "themselves without asking anyone outside the hall.",
        "Three camps take their seats. The liberal wing wants a date for the next ballot printed before the session closes. The "
        "ministry heads argue that rotation has kept the country solvent and calm, and that a campaign would only hand the valley "
        "question to whoever shouts loudest. On the back benches a smaller nationalist group says nothing yet, and waits to see "
        "how the valleys debate goes.",
        "Nobody expects a decision today. The real quarrel is over who writes the options paper the council will vote on next "
        "season. The ministries offer their own legal staff, who know every statute and every shortcut. The district councils "
        "want a drafting commission of their own members, slower and less expert, but much harder to accuse of writing the "
        "answer in advance.",
    ), (
        Option('Give the drafting to the district councils.', (Stability(0.03), PP(-15))),
        Option('Let the ministry lawyers draft it.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('valleys_offer', 'What the Valleys Are Worth', (
        "The map room of the foreign ministry keeps a framed survey of Tyrann Valley, Boikos and the Jeszczed Mountains drawn "
        "before Belka took them, and every visitor is walked past it. The valleys belong to Ustio now. Their towns still speak "
        "Ratian, their markets still trade with Dormakaj, and their families still cross the line for weddings and funerals "
        "whenever the papers allow it.",
        "Three answers circulate in the ministries. The treasury says Ratio is rich enough to buy the valleys back at a price no "
        "sensible government could refuse, and to pay for anyone who wants to move in either direction. Lawyers in the foreign "
        "ministry prefer a supervised vote and a promise to accept the count. The general staff and the nationalist papers say "
        "Ratio should stop asking and start insisting.",
        "Whatever Ratio chooses, the answer will be Ustio's to give, and Ustio is a young republic with its own pride and its "
        "own fears. Partisan violence in the valleys, which nobody in Centrum controls, makes every Ratian statement sound like "
        "a threat to Ustian ears. The council must first decide how loudly it is willing to speak at all.",
    ), (
        Option('Speak softly and keep the files open.', (Stability(0.02), WarSupport(-0.02))),
        Option('Let the newspapers argue it out.', (WarSupport(0.03), Stability(-0.01))),
    ), picture=0),
    EventDef('furnace_count', 'The Furnace Count at Centrum', (
        "The inspectors come back from the mills with notebooks full of figures that do not match the ministry ledgers. "
        "Centrum's furnaces sit on the richest ore in Ratio, and the arms halls built around them account for nearly half of the "
        "national industry. Some furnaces run three shifts. Others have been banked for years while still drawing a maintenance "
        "budget, and two appear in the accounts but nowhere on the ground.",
        "The mill owners call idle capacity insurance, kept warm for orders that may arrive with the next crisis. Their critics "
        "in the council reply that insurance nobody can audit is simply waste. Meanwhile the Troton mines sell raw chromium and "
        "tungsten abroad for a fraction of what alloy steel would fetch, because no one ever built the mills to use them at home.",
        "Three schools are forming around the figures. One wants armour plate for the tank parks, one wants girders for rails "
        "and new factories, and one wants to sell ore and billets to whoever pays best. Before any of them wins, the council "
        "has a smaller matter to settle: whether the owners of banked furnaces keep drawing maintenance money while the larger "
        "argument goes on.",
    ), (
        Option('Stop paying for cold furnaces.', (PP(20), Stability(-0.02))),
        Option('Give the owners a year to relight them.', (Stability(0.02), PP(-15))),
    ), picture=1),
    EventDef('three_harbours', 'Three Harbours, Three Rulebooks', (
        "Captains bound for Ratio must learn three sets of rules. Roshniku, the largest naval harbour, sits below the Troton "
        "cliffs and charges the highest pilotage on the coast. Isakas, a short run along the same shore, keeps its own berthing "
        "lists and its own customs clerks. Sukaxhija on the Zulian Coast handles the oil trade and answers to nobody in Centrum "
        "unless it must.",
        "The navy shares all three harbours with merchant shipping and has long complained that it negotiates berths like a "
        "foreign customer. Ship owners complain about the dues, the delays and the clerks. The harbour masters, each of whom "
        "collects fees that have quietly become a personal income, complain about anyone who proposes a change.",
        "A single board for all three harbours would standardise pilotage, dues and berthing, and give the navy a seat at the "
        "table. It would also end several comfortable careers, and the coastal districts suspect that a board answering to "
        "Centrum will spend their harbour money on the capital. The council must decide how much the harbour masters keep, and "
        "whether they leave quietly or loudly.",
    ), (
        Option('Buy out the harbour masters.', (PP(-20), Stability(0.02))),
        Option('Abolish the private fees by decree.', (PP(20), Stability(-0.02))),
    ), picture=1),
    EventDef('tank_parks', 'Three Hundred Hulls', (
        "The park inspectors start at dawn, before anyone can warm an engine and hide a fault. Ratio's army was built for "
        "firepower on open ground: four tank divisions, four motorised and four of infantry, with some three hundred modern "
        "hulls in the parks. On paper it is one of the heaviest armies in the region for a country of its size.",
        "The inspection tells a more complicated story. Many tanks start on the first try, and many do not. Spares are hoarded "
        "in one division and missing in the next. Crews have fired a fraction of their gunnery allowance to save money, and some "
        "drivers have not driven a full day in a year. The officers knew all of this, and none of them wanted it written down.",
        "The general staff must now decide what kind of army Ratio is maintaining. The armoured school wants the divisions "
        "massed on the Dormakaj plain, the mountain school wants the passes held, and a third group wants a motor reserve at "
        "Centrum. Sooner than any of that, the staff must deal with the crews who failed: send them back to the schools for a "
        "winter and leave their divisions short, or keep them in the ranks and teach them on the job.",
    ), (
        Option('Send the failed crews back to school.', (XP('army', 20), PP(-15))),
        Option('Teach them in the ranks.', (PP(15), XP('army', 5))),
    ), picture=2),
    EventDef('belkan_spring', 'Spring War on Two Frontiers', (
        "News of the Belkan War reaches Centrum before dawn. Belka is fighting on several fronts at once, and two of the "
        "countries beside it, Ustio and Gebet, also share frontiers with Ratio. The war room fills with maps that had been "
        "rolled up for decades, and by midday the first reports arrive of queues forming at the Dormakaj crossings.",
        "Ratio is not at war, and nobody in the council wants it to be. But Ratio has its own memories of Belka, which once took "
        "the valleys now in Ustian hands, and few Ratians wish Belka well. The general staff wants the western divisions at "
        "readiness. The interior ministry wants to know how many people might cross and where they would sleep.",
        "The first decision concerns the crossings. If they stay open, families fleeing the fighting will reach Dormakaj within "
        "days, with all the cost and confusion that brings. If they close, Ratio keeps the war at arm's length and leaves the "
        "families to whatever lies behind them. Either choice will be remembered on both sides of the line for a generation.",
    ), (
        Option('Keep the crossings open.', (Event('crossing_crowds', 7), Stability(-0.01))),
        Option('Close the crossings until the front settles.', (WarSupport(0.02), Stability(0.01))),
    ), picture=2),
    EventDef('crossing_crowds', 'Crowds at the Dormakaj Crossings', (
        "A week after the decision to keep the crossings open, the roads into Dormakaj are lined with cars, carts and people on "
        "foot. Many arrivals come from the valleys and speak Ratian. Others are families from Ustio and Gebet with no tie to "
        "Ratio beyond its nearness. Border police register them as fast as they can and send the rest to schools and sports "
        "halls for the night.",
        "The Dormakaj city council complains that it is carrying a national burden alone. Hospitals run short of beds and the "
        "schools have closed for lack of space. Nationalist papers ask why Ratio is housing Ustians while the valleys remain "
        "Ustian. Parish groups and trade unions organise kitchens, and a few households take strangers into their homes.",
        "The council can spread the arrivals across the country by rail, so that every district carries part of the cost, or "
        "keep them near the frontier where they can return quickly once the fighting moves away. Either way, the crossings have "
        "turned a foreign war into a domestic matter, and the next budget will show it line by line.",
    ), (
        Option('Spread the arrivals across the five districts.', (Stability(0.02), PP(-25))),
        Option('Keep them near the frontier.', (PP(10), Stability(-0.02))),
    ), picture=0),
    EventDef('ulysses_date', 'Ratio Waits for Ulysses', (
        "Word that the FCU now expects Ulysses to hit the Earth reaches Centrum as a few lines on the news wire, and within the "
        "hour nobody in the capital talks about anything else. Ratio cannot check the astronomers' sums for itself. It does have "
        "deep mine galleries, a dense web of railways, a disciplined army and a public that has so far trusted its council.",
        "The first days are untidy. Prices for tinned food and candles double in the Centrum markets. A rumour that the "
        "fragments will fall on the Troton empties two mining towns overnight, until the miners discover that nobody actually "
        "said so. Churches fill, and so do the queues at the banks, as families try to turn savings into something they can "
        "carry.",
        "The council can cap the price of tinned food, candles and lamp oil at once and send inspectors after the shops that "
        "break the cap. That would calm households and enrage merchants who restocked at the new prices. Or it can let the "
        "market find its own level, trusting that panic burns out faster than any regulation can be enforced across five "
        "districts.",
    ), (
        Option('Cap the prices of staples.', (Stability(0.03), PP(-15))),
        Option('Let the market find its level.', (PP(25), Stability(-0.03))),
    ), picture=0),
    EventDef('ceasefire_count', 'Counting the Cost of the Ustian War', (
        "The war between Ratio and Ustio is over, and its terms belong to the generals and diplomats who signed them. In Centrum "
        "the council turns to what is left at home: reservists to pay off and send back to the mills, families to notify, "
        "hospitals full of wounded, and a war budget that must be wound down without collapsing the factories that grew on it.",
        "The nationalist papers want a monument and a day of mourning. The liberal papers want an inquiry into how the line "
        "caught fire in the first place. The ministries want neither, preferring a quiet demobilisation and a short statement. "
        "In the valleys across the line, people on both sides wait to see whether the peace will hold.",
        "Whatever the treaty says about the valleys, Ratio must decide how honestly it tells its own story. A public inquiry "
        "would name failures on every side, including its own. A monument would honour the dead and harden the next generation. "
        "Silence would be cheapest, and would leave the country to remember the war however it chooses, street by street and "
        "family by family.",
    ), (
        Option('Open a public inquiry.', (Stability(0.02), PP(-20))),
        Option('Raise a monument to the fallen.', (WarSupport(0.04), Stability(-0.01))),
        Option('Demobilise quietly.', (PP(25),)),
    ), picture=2),
)

# --- branches ------------------------------------------------------------------------------------
COUNCIL = Branch('council', 'The Council Administration', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('cncl_january_mandate', 'The January Mandate',
          "The ballot papers of New Year's Day 1991 still sit in the council archive, and the democratic camp they returned keeps "
          "the support of about seven Ratians in ten. Even so, the council administration has suspended the next poll with no "
          "date set, and its ministries rotate the chair among themselves. The council must now debate what that January vote "
          "actually authorised, and whether a mandate with no expiry is still a mandate at all.",
          ('assembly', 'ballot'), reward=(Idea('standing_mandate'), Event('council_session'))),
    Focus('cncl_hearings', 'Hearings in the Five Districts',
          "Council members leave Centrum to hold public hearings in Dormakaj, the Troton Mountains, Ratio Valley and the Zulian "
          "Coast. Mill wages and the valleys beyond the Ustian line dominate every session, and some halls turn hostile. The tour "
          "costs the council its comfortable distance from the voters, yet it learns which promises the districts would actually "
          "believe and which they would laugh at.",
          ('civil', 'assembly'), after=('cncl_january_mandate',), reward=(Idea('district_hearings'),)),
    Focus('cncl_ministry_books', 'Open the Ministry Books',
          "With the chair rotating, each ministry has blamed the previous holder for every overspent budget. A council audit "
          "office reads five years of ministry ledgers and publishes the totals, and several senior officials retire before the "
          "figures appear. The exercise costs political comfort and a few loyal servants, but whatever form of government "
          "follows will inherit accounts it can trust.",
          ('scales', 'document'), after=('cncl_january_mandate',), reward=(Flag('books_opened'), PP(-15))),
    Focus('cncl_ballot_date', 'Name the Day of the Ballot',
          "The liberal wing proposes the simplest repair: publish the date of the next general ballot, the rules for standing and "
          "the seats each district will fill. Ministries would then have to campaign instead of rotate. The council loses its "
          "freedom to postpone, and the nationalist minority gains a lawful platform that nobody can deny it once the date is "
          "printed.",
          ('ballot', 'document'), after_any=('cncl_hearings', 'cncl_ministry_books'), cost=10,
          exclusive=('cncl_keep_council', 'cncl_valley_front'), reward=(SwapIdea('standing_mandate', 'ballot_calendar'),)),
    Focus('cncl_keep_council', 'Government by Rotation',
          "The ministries argue that the rotating council has kept Ratio calm and solvent, and that a campaign season would only "
          "hand the valley question to the loudest speakers. They propose to keep the council, write its rotation into law and "
          "postpone the ballot again. Decisions stay quick and quiet, while patience with an unelected council wears thinner "
          "every year it lasts.",
          ('assembly', 'command'), after_any=('cncl_hearings', 'cncl_ministry_books'), cost=10,
          exclusive=('cncl_ballot_date', 'cncl_valley_front'), reward=(SwapIdea('standing_mandate', 'rotating_chairs'),)),
    Focus('cncl_valley_front', 'The Valley Front Takes the Squares',
          "Once the government has pressed the Ratian claim in public, the nationalist sixth of the country no longer sounds like "
          "a fringe. A movement calling itself the Valley Front fills the Dormakaj squares and demands that the council govern "
          "for the lost valleys above all else. Giving it the floor raises war support and costs calm, and the moderates will "
          "not forget who opened the door.",
          ('security', 'ballot'), after_any=('cncl_hearings', 'cncl_ministry_books'), cost=10,
          exclusive=('cncl_ballot_date', 'cncl_keep_council'), requires=(HasFlag('claim_pressed'),),
          reward=(SwapIdea('standing_mandate', 'valley_front'),)),
    Focus('cncl_party_register', 'A Register of Parties',
          "Before the ballot opens, every party must file its statutes, its accounts and the names of its district committees "
          "with an electoral court. The register stops anonymous money flowing into the campaign and gives small parties a legal "
          "footing. Party bosses object to open books, and the court needs a full year to process the filings before anyone may "
          "stand.",
          ('document', 'ballot'), after=('cncl_ballot_date',), reward=(TimedIdea('campaign_season', 365),)),
    Focus('cncl_first_ballot', 'The First Contested Ballot',
          "Every district from Dormakaj to the Zulian Coast opens its polling halls, and the council seats are fought over by "
          "rival lists instead of being handed round by rotation. Clerks of the electoral court sit at every count. The winners form an elected council answerable to the "
          "voters rather than to the ministries. Elected ministers move more slowly than appointed ones did, but they carry far "
          "more authority when they finally move.",
          ('ballot', 'medal'), after=('cncl_party_register',),
          reward=(Regime('elected_council'), SwapIdea('ballot_calendar', 'open_council'))),
    Focus('cncl_presidium', 'A Presidium Holds the Seals',
          "The rotation law gives way to something firmer: a presidium of five ministry heads that holds the seals, signs the "
          "budget and names the district prefects. The council survives as a debating chamber with no vote on money. Government "
          "becomes efficient and predictable, and the democratic majority that voted in January loses any real voice in policy.",
          ('command', 'document'), after=('cncl_keep_council',),
          reward=(Regime('standing_presidium'), SwapIdea('rotating_chairs', 'presidium_rule'))),
    Focus('cncl_restoration', 'A Committee for the Lost Valleys',
          "Leaders of the Valley Front accept seats on a committee that suspends the council and governs by decree until the "
          "valleys return. Courts, newspapers and unions answer to it. Ratio becomes harder, louder and more united on one "
          "question, and far more anxious about every other. Neighbours who once saw a calm republic will now see a nationalist "
          "state on their frontier.",
          ('security', 'command'), after=('cncl_valley_front',),
          reward=(Regime('restoration_committee'), SwapIdea('valley_front', 'restoration_decrees'),
                  Tooltip('No war, claim or border effect; the committee changes only the government at home.'))),
    Focus('cncl_torchlight', 'Torches Through Centrum',
          "The Front schedules a torchlight march through Centrum every month, and attendance climbs with each one. The marches "
          "bring volunteers to the reserve and money to the movement, yet they frighten the mill owners and close the shops along "
          "the route. Police overtime alone strains the city budget, and opponents learn to stay indoors on march nights.",
          ('medal', 'security'), after=('cncl_valley_front',), reward=(TimedIdea('torchlight_marches', 365),)),
    Focus('cncl_settled', 'The Council Settles Its Form',
          "Whatever shape the council has taken, its rules still live in a binder of emergency orders and unwritten custom. A short "
          "basic statute replaces the binder: how ministers are chosen, how a budget passes and when the arrangement must be "
          "reviewed. Drafting it costs a winter of argument. Afterwards every dispute in Centrum opens with a page number instead "
          "of a shouting match.",
          ('scales', 'assembly'), after_any=('cncl_first_ballot', 'cncl_presidium', 'cncl_restoration'),
          reward=(Flag('form_settled'), Stability(0.03))),
))

VALLEYS = Branch('valleys', 'The Valleys Across the Line', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('val_three_valleys', 'Three Valleys Beyond the Line',
          "Belka took Tyrann Valley, Boikos and the Jeszczed Mountains from Ratio in its years of expansion, and they stayed with "
          "Ustio when the republic broke away in 1988. Their people still speak Ratian and many have family in Dormakaj. Ratio "
          "has never renounced the claim. Before it chooses an answer, the council must say aloud that the question is open "
          "again.",
          ('gate', 'assembly'), reward=(Idea('valleys_question'), Event('valleys_offer'))),
    Focus('val_kin_papers', 'Papers for Ratian Kin',
          "Thousands of Ratian families have relatives in the valleys who cannot easily visit, study or inherit across the "
          "Ustian frontier. Offices in Dormakaj issue papers, pay modest pensions to elderly kin and hold school places for "
          "valley children. The scheme costs money every year and Ustio watches it closely, but it keeps the claim humane rather "
          "than armed.",
          ('refugees', 'document'), after=('val_three_valleys',), reward=(Idea('kin_offices'),)),
    Focus('val_disown', 'Disown the Bombers',
          "Some Ratians in the valleys have turned to partisan violence against Ustian rail lines and barracks. The council "
          "condemns the attacks by name, closes the private arms channels that run through Dormakaj and offers Ustio its police "
          "files. Nationalist papers call it betrayal. Without that public line between grievance and bombing, no foreign "
          "mediator will take Ratio seriously.",
          ('scales', 'security'), after=('val_three_valleys',), reward=(Flag('violence_disowned'), Stability(0.02))),
    Focus('val_purchase', 'Buy the Valleys Back',
          "The treasury proposes to settle the matter with money: a fund large enough to pay Ustio well above the value of the "
          "valleys, with clauses that let Ustian residents and firms move home at Ratian expense. It is the most generous answer "
          "and by far the most expensive one. Whether Ustio ever accepts it remains Ustio's own decision.",
          ('economy', 'diplomacy'), after=('val_three_valleys',), cost=10, exclusive=('val_observers', 'val_press'),
          reward=(SwapIdea('valleys_question', 'purchase_fund'), Flag('purchase_path'),
                  Tooltip("No state, core or border change; any transfer is Ustio's answer to the inherited offer."))),
    Focus('val_observers', 'Let the Valleys Be Counted',
          "A second school argues that land should follow the will of the people living on it. Ratio asks for a supervised vote "
          "in the valleys under foreign observers and promises in advance to accept the count, whatever it says. The appeal costs "
          "nothing in money and a great deal in pride, because Tyrann might vote differently from Boikos.",
          ('scales', 'diplomacy'), after=('val_three_valleys',), cost=10, exclusive=('val_purchase', 'val_press'),
          requires=(HasFlag('violence_disowned'),),
          reward=(SwapIdea('valleys_question', 'observer_appeal'),
                  Tooltip('No vote is scripted here; any referendum stays with the inherited Ustio events.'))),
    Focus('val_press', 'Press the Ratian Claim',
          "The hard line says that Ustio holds the valleys only because Belka once did, and that Ratio should say so in every "
          "forum. The claim is pressed in speeches, schoolbooks and frontier exercises. War support rises and the nationalists "
          "cheer. Ustian garrisons in the valleys will treat every Ratian manoeuvre as a threat, and plan accordingly.",
          ('security', 'gate'), after=('val_three_valleys',), cost=10, exclusive=('val_purchase', 'val_observers'),
          reward=(SwapIdea('valleys_question', 'pressed_claim'), Flag('claim_pressed'),
                  Tooltip('No war, wargoal, claim or border effect is scripted by this tree.'))),
    Focus('val_bonds', 'Valley Bonds at the Centrum Exchange',
          "To fill the purchase fund without new taxes, the treasury sells long bonds at the Centrum exchange to banks, pension "
          "funds and patriotic savers. Buyers insist on seeing the audited ministry books first. The bonds raise real money and "
          "tie thousands of households to a peaceful settlement. Interest payments will run for decades whether Ustio sells or "
          "not.",
          ('economy', 'document'), after=('val_purchase',), requires=(HasFlag('books_opened'),),
          reward=(TimedIdea('valley_bonds', 730),)),
    Focus('val_resettlement', 'Moving Costs for Those Who Choose',
          "Any settlement will leave people on the wrong side of the line by their own reckoning. Ratio offers moving costs, "
          "housing grants and job placement to valley families who choose to leave Ustio, and promises the same to Ustians who "
          "wish to go home the other way. The scheme is costly and slow, but it removes the fear of forced moves.",
          ('refugees', 'rail'), after=('val_purchase',), reward=(TimedIdea('resettlement_fund', 730),)),
    Focus('val_counters', 'Neutral Counters Welcome',
          "Foreign observers who might one day count a valley vote are invited to travel the Ratian side of the frontier with "
          "open papers, visit the kin offices and inspect the Dormakaj garrison. The visits are awkward for officers used to "
          "closed bases. They also give outsiders a firsthand reason to believe that Ratio means what it has promised.",
          ('peace', 'document'), after=('val_observers',), reward=(TimedIdea('observer_missions', 730),)),
    Focus('val_boikos_radar', 'A Radar Mast Facing Boikos',
          "Frontier divisions on the Dormakaj plain receive a radar head on the hills facing Boikos and orders to report every "
          "Ustian movement. The post costs little and watches a long stretch of the line. Ustian officers across the valley will "
          "see the mast from their barracks windows, which is partly the reason for building it exactly where it stands.",
          ('radar', 'security'), after=('val_press',), reward=(Build('radar_station', 1, 306), WarSupport(0.03))),
    Focus('val_war_footing', 'If the Line Catches Fire',
          "This focus opens only while Ratio and Ustio are actually at war. The council moves to a war budget: arms lines first, "
          "consumer goods rationed, reservists paid from emergency credit. Nothing decided here starts or ends the fighting. It "
          "decides only how the home districts carry a war that the generals and diplomats are already conducting.",
          ('security', 'economy'), after_any=('val_purchase', 'val_observers', 'val_press'),
          requires=(HasGlobal('first_ustian_war'),), reward=(TimedIdea('war_budget', 365), Flag('ustian_war_lived'))),
    Focus('val_war_ended', 'After the Shooting on the Line',
          "The war with Ustio is over, on whatever terms the generals and diplomats reached. Ratio must count its dead, pay its "
          "reservists home and decide what to tell the families. The war budget is wound down. Nothing in this focus changes the "
          "treaty; it decides only how honestly the country mourns and how quickly it demobilises.",
          ('peace', 'medical'), after=('val_war_footing',), requires=(NotGlobal('first_ustian_war'),),
          reward=(RemoveIdea('war_budget'), Event('ceasefire_count'))),
    Focus('val_quiet_line', 'A Commission for a Quiet Line',
          "While the frontier stays peaceful, Ratio proposes a standing desk with Ustian officials for crossings, rail traffic "
          "and incidents along the line. Neither side gives up its position on the valleys. A patrol that strays or a shot fired "
          "at night now leads first to a telephone call. The council pays for the desk and guards its calm.",
          ('peace', 'gate'), after_any=('val_purchase', 'val_observers', 'val_press'),
          requires=(NotGlobal('first_ustian_war'), NotFlag('ustian_war_lived')), reward=(Idea('line_commission'),)),
))

STEEL = Branch('steel', 'Centrum Steel', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('stl_furnace_count', 'Count the Centrum Furnaces',
          "Centrum sits on the richest steel deposits in Ratio, and its mills feed the arms halls that make up nearly half of the "
          "country's industry. Nobody has recently counted which furnaces work, which idle and which exist only in the accounts. "
          "Inspectors walk every mill and arms hall from Centrum to the Zulian Coast. The owners open their gates politely and "
          "answer the questions rather less so.",
          ('industry', 'document'), reward=(Idea('furnace_ledger'), Event('furnace_count'))),
    Focus('stl_troton_chromium', 'Chromium from the Troton Mines',
          "The Troton Mountains hold chromium and tungsten that Centrum has mostly sold abroad as raw ore. Alloying them at home "
          "turns ordinary steel into tool and armour grades worth several times the price. New mills need power lines up the "
          "mountain valleys and engineers who can run them, and the mining towns want a share of the margin.",
          ('tools', 'industry'), after=('stl_furnace_count',), reward=(Idea('alloy_mills'),)),
    Focus('stl_shop_councils', 'Shop Councils in the Mill Towns',
          "Mill workers in Centrum and on the Zulian Coast elect shop councils that agree shift patterns, safety rules and bonus "
          "schemes with management. Owners complain about lost authority, and some councils make unrealistic demands in their "
          "first year. Strikes become rarer and shorter, and output stops collapsing every time a furnace crew walks out over a "
          "grievance nobody heard.",
          ('assembly', 'industry'), after=('stl_furnace_count',), reward=(Idea('works_councils'),)),
    Focus('stl_plate', 'Plate for the Tank Parks',
          "The defence school wants the mills to roll armour plate first, so that the tank parks never wait for hulls. A new arms "
          "hall in Centrum takes the plate straight from the rolling line. The army gains a domestic armour supply that few "
          "neighbours can match, and civilian builders must queue behind every military order for years.",
          ('industry', 'security'), after_any=('stl_troton_chromium', 'stl_shop_councils'), cost=10,
          exclusive=('stl_girders', 'stl_ore_ports'),
          reward=(SwapIdea('furnace_ledger', 'armour_plate'), Build('arms_factory', 1, 0))),
    Focus('stl_girders', 'Girders Before Guns',
          "The builders' school wants steel for bridges, rails and factory frames instead. A new fabrication hall in Centrum turns "
          "billets into girders for the spine line and the valley towns. Construction everywhere speeds up and the steel stays "
          "at home. The army must buy its next generation of plate abroad or wait for whatever capacity is left over.",
          ('rail', 'industry'), after_any=('stl_troton_chromium', 'stl_shop_councils'), cost=10,
          exclusive=('stl_plate', 'stl_ore_ports'),
          reward=(SwapIdea('furnace_ledger', 'rail_steel'), Build('industrial_complex', 1, 0))),
    Focus('stl_ore_ports', 'Sell Ore Through the Zulian Ports',
          "The trading school argues that Ratio earns most by selling ore and billets to anyone who pays, through the harbours of "
          "the Zulian Coast. The coastal rail approaches are widened for heavy ore trains. Foreign currency flows in and consumer "
          "shelves fill. Ratio becomes a supplier of other nations' industry rather than the builder of its own.",
          ('logistics', 'economy'), after_any=('stl_troton_chromium', 'stl_shop_councils'), cost=10,
          exclusive=('stl_plate', 'stl_girders'),
          reward=(SwapIdea('furnace_ledger', 'ore_trade'), Build('infrastructure', 1, 489))),
    Focus('stl_dormakaj_shops', 'Machine Shops on the Dormakaj Plain',
          "Dormakaj is the largest city in Ratio, and its plain is flat enough to build on cheaply. A machine shop district beside "
          "the main rail yards repairs mill equipment, rolling stock and farm machinery for the whole west of the country. It "
          "employs young people who would otherwise leave for Centrum. It also stands closer to the Ustian line than any other "
          "plant.",
          ('tools', 'civil'), after_any=('stl_plate', 'stl_girders', 'stl_ore_ports'), reward=(Build('industrial_complex', 1, 306),)),
    Focus('stl_tungsten_bits', 'Tungsten Bits for the Drill Crews',
          "Troton tungsten makes some of the hardest drill bits and cutting tools in the region, yet the mines themselves still "
          "drill with imported steel. A small tool works fits Ratian bits to Ratian drills and sells the surplus. Mining becomes "
          "faster and safer underground, and the works trains a cadre of metallurgists that the alloy mills will need.",
          ('tools', 'science'), after=('stl_troton_chromium',),
          reward=(Research('excavation_tech', 0.5, 1), Research('industry', 0.3, 1))),
    Focus('stl_alloy_reserve', 'A Strategic Reserve of Alloy',
          "The mills set aside a reserve of chromium steel billets, stored in rail yards and old mine galleries, for the day "
          "imports stop or a crisis demands armour faster than ore can be dug. The reserve ties up capital that could be earning "
          "interest. If a crisis does come, the armour workshops will not have to begin from empty bins.",
          ('shelter', 'industry'), after=('stl_tungsten_bits',), reward=(Flag('alloy_stock'), PP(-15))),
    Focus('stl_valley_foundry', 'A Foundry in Ratio Valley',
          "Ratio Valley has one small factory and a single free plot beside the line from the Troton to the coast. A foundry there "
          "would cast pump bodies, engine blocks and rail fittings for the whole country. The same plot is the only place on the "
          "valley shore where a slipway could stand, so choosing the foundry closes that door for good.",
          ('industry', 'rebuild'), after_any=('stl_plate', 'stl_girders', 'stl_ore_ports'), exclusive=('cst_valley_slipway',),
          reward=(Build('industrial_complex', 1, 472),)),
))

RAIL = Branch('rail', 'The Spine Line', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('rail_walk', 'Walk the Spine Line',
          "One railway holds Ratio together: the trunk from the Gebet frontier through Dormakaj to Centrum, then on through the "
          "Troton Mountains and Ratio Valley to the Zulian Coast. Engineers walk its whole length and list every weak bridge, "
          "single-track section and overloaded junction. The survey costs a season of work crews and gives the ministries one "
          "shared timetable.",
          ('rail', 'document'), reward=(Idea('spine_timetable'),)),
    Focus('rail_centrum_yards', 'Marshalling Yards at Centrum',
          "Every train between the west and the coast passes through Centrum, and its cramped yards have become the slowest point "
          "on the spine. New sidings, a hump yard and a locomotive depot let freight be sorted without blocking passenger "
          "traffic. Building them means months of diverted trains through the capital, and complaints from every district that "
          "waits.",
          ('rail', 'logistics'), after=('rail_walk',), reward=(Build('infrastructure', 1, 0),)),
    Focus('rail_troton_grades', 'Easing the Troton Grades',
          "South of Centrum the line climbs into the Troton Mountains on grades so steep that heavy ore trains need two "
          "locomotives. Engineers cut new curves and a short tunnel to ease the worst climb. The work is slow, dangerous and "
          "expensive in hard rock. Once it is finished, ore and steel reach the coast in half the time they take today.",
          ('rail', 'tools'), after=('rail_walk',), reward=(Build('infrastructure', 1, 419),)),
    Focus('rail_valley_bridges', 'New Bridges Down the Valley',
          "Below the Troton the line follows Ratio Valley on old timber and iron bridges that flood every spring. Replacing them "
          "with steel spans lifts the line above the water and lets heavier trains reach the coast. Valley towns gain a reliable "
          "connection for the first time, and the army a route that does not wash away each year.",
          ('bridge', 'rail'), after=('rail_troton_grades',), reward=(Build('infrastructure', 1, 472),)),
    Focus('rail_zulian_spur', 'A Spur to the Zulian Quays',
          "The spine stops short of the Zulian quays, so cargo still covers the last stretch by lorry. A spur line runs tracks "
          "onto the wharves themselves, letting ore wagons tip straight into ship holds. Dockers fear for their jobs and the "
          "harbour masters demand a voice in the timetable. The coast finally joins the national network properly.",
          ('logistics', 'navy'), after=('rail_valley_bridges',), reward=(Build('infrastructure', 1, 489),)),
    Focus('rail_troop', 'Troop Trains Take the First Path',
          "The army asks for guaranteed priority on every line: troop and supply trains take the first path, and civil traffic "
          "waits. Mobilisation plans become reliable, and divisions can shift from the coast to the western frontier in days. "
          "Passengers and freight customers pay with delays every time the general staff decides to run an exercise.",
          ('rail', 'security'), after=('rail_centrum_yards',), exclusive=('rail_passenger',), reward=(Idea('troop_trains'),)),
    Focus('rail_passenger', 'Fares the Mill Towns Can Pay',
          "The ministry of works prefers fixed passenger paths and cheap fares, so that mill workers can live in the valley towns "
          "and commute to Centrum. Housing pressure in the capital eases and the smaller towns stop emptying. The army keeps no "
          "guaranteed priority, and its staff officers warn that mobilisation timetables now depend on goodwill.",
          ('civil', 'rail'), after=('rail_centrum_yards',), exclusive=('rail_troop',), reward=(Idea('passenger_rail'),)),
    Focus('rail_gebet_trunk', 'Through Freight to Gebet',
          "The heaviest line in Ratio runs from Dormakaj across the frontier into Gebet, and most of its trains stop at the border "
          "to change crews and papers. A through-running agreement with Gebet lets freight cross without unloading. Customs "
          "revenue falls, Dormakaj traders win a larger market, and the trunk becomes a line both governments have reason to "
          "protect.",
          ('rail', 'diplomacy'), after=('rail_walk',), reward=(Idea('gebet_trunk'), Flag('trunk_open'))),
    Focus('rail_boikos_branch', 'Trains Through to Boikos',
          "A single-track branch still runs from Dormakaj across the Ustian line into Boikos, a relic of the years before Belka "
          "took the valleys. With the purchase offer on the table, Ratio proposes through trains for passengers and mail. It "
          "changes no border. It reconnects families, and gives the valleys a daily reminder of which country is courting them.",
          ('rail', 'peace'), after=('rail_walk',), requires=(HasFlag('purchase_path'),),
          reward=(Flag('boikos_trains'), Tooltip('Through running on the existing branch line only; no state, core or border effect.'))),
    Focus('rail_wagon_works', 'Wagon Works at Dormakaj',
          "Ratio buys most of its locomotives and wagons abroad and repairs them in yards never designed for the work. A wagon "
          "works at Dormakaj builds freight cars from Centrum steel and rebuilds worn locomotives. It brings more industry to the "
          "plain, which pleases the city, and worries planners who can see how close it stands to the frontier.",
          ('rail', 'tools'), after_any=('rail_troop', 'rail_passenger'),
          reward=(Build('industrial_complex', 1, 306), Research('train_tech', 0.5, 1))),
    Focus('rail_dormakaj_junction', 'Rebuild the Dormakaj Junction',
          "Where the Gebet trunk meets the spine, the Dormakaj junction crosses lines on the level, and every crossing train "
          "halts the others. A flyover and new platforms separate the flows. The city loses a district of old warehouses to the "
          "works. Trains for Gebet, Centrum and the Boikos branch stop delaying each other at last.",
          ('bridge', 'logistics'), after=('rail_gebet_trunk',), reward=(Build('infrastructure', 1, 306),)),
))

COAST = Branch('coast', 'Three Harbours and a Coast', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('cst_harbour_board', 'One Board for Three Harbours',
          "Ratian ships work from three small harbours: Roshniku and Isakas below the Troton Mountains, and Sukaxhija on the "
          "Zulian Coast. Each runs its own pilots, dues and berthing rules, and captains complain about all three. A single "
          "harbour board standardises them. Local harbour masters lose their fees, and the navy gains one office to deal with.",
          ('navy', 'document'), reward=(Idea('harbour_board'), Event('three_harbours'))),
    Focus('cst_roshniku_basin', 'Deepen the Roshniku Basin',
          "Roshniku is the largest naval base in the country, but its basin silts up and the destroyers must wait for high water "
          "to leave. Dredgers deepen the channel and engineers lengthen the repair quay. The work keeps the squadron in port for "
          "a season. Afterwards it can sail on any tide and refit without leaving home waters.",
          ('navy', 'tools'), after=('cst_harbour_board',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
    Focus('cst_isakas_watch', 'A Watch Post Above Isakas',
          "The approaches to Isakas and Roshniku pass close under the Troton cliffs, where a radar post can see far out to sea. A "
          "set mounted there, wired straight to the naval duty officer at Roshniku, tracks hulls and aircraft on one screen. It "
          "costs a fraction of a warship. For the first time the navy will know who is approaching before they reach the harbour mouth.",
          ('radar', 'navy'), after=('cst_harbour_board',), reward=(Build('radar_station', 1, 419),)),
    Focus('cst_escorts', 'Escorts for the Ore Ships',
          "The three destroyers are organised as an escort squadron to shepherd ore carriers and tankers along the coast. Crews "
          "train in convoy work, signalling and anti-submarine search. It is a modest role, but it matches what Ratio actually "
          "ships. The admirals who wanted a fighting squadron have to settle for a protective one.",
          ('navy', 'logistics'), after=('cst_roshniku_basin',), exclusive=('cst_submarines',), reward=(Idea('escort_squadron'),)),
    Focus('cst_submarines', 'A School for Coastal Submarines',
          "Ratio has one coastal submarine and almost nobody trained to fight it. A submarine school at Roshniku would train full "
          "crews and develop tactics for the narrow waters off the Troton shore. Submarines deter far larger fleets for little "
          "money. The escorts lose their best officers to the new service, and convoy protection suffers for it.",
          ('submarine', 'training'), after=('cst_roshniku_basin',), exclusive=('cst_escorts',), reward=(Idea('submarine_school'),)),
    Focus('cst_zulian_oil', 'Leases on the Zulian Oil Fields',
          "The Zulian Coast holds the richest oil in Ratio, worked by a handful of old wells. The council offers leases on "
          "published terms, with fixed royalties and a share for the coastal districts. Drillers arrive within a year. The royalty "
          "money funds the harbour works, and coastal deputies begin reminding Centrum, at every budget debate, exactly whose "
          "wells are paying.",
          ('economy', 'tools'), after=('cst_harbour_board',), reward=(Idea('zulian_leases'),)),
    Focus('cst_valley_slipway', 'A Slipway on the Valley Shore',
          "Ratio Valley reaches the sea at two small inlets, and the free plot beside the rail line could take a slipway for patrol "
          "boats and coastal freighters. Shipwrights from Roshniku would train valley workers. Choosing the slipway closes the "
          "plot to the foundry the steel ministry wants, and the valley must accept a smaller, seasonal trade.",
          ('navy', 'rebuild'), after=('cst_harbour_board',), exclusive=('stl_valley_foundry',), reward=(Build('dockyard', 1, 472),)),
    Focus('cst_hull_register', 'A Register of Ratian Hulls',
          "The harbour board compiles a monthly list of every Ratian-flagged ship, its usual cargo lanes and the frequencies its "
          "radio officer keeps. When trouble starts at sea, the naval duty desk can reach every master within hours instead of "
          "waiting for news from foreign ports. Owners dislike the paperwork and suspect the list doubles as a requisition roll.",
          ('document', 'navy'), after_any=('cst_escorts', 'cst_submarines'), reward=(Flag('convoy_register'), XP('navy', 10))),
    Focus('cst_sukaxhija_patrols', 'Patrol Flights from Sukaxhija',
          "Tankers loading off the Zulian Coast need watching from the air as well as the sea. A patrol airfield near Sukaxhija "
          "lets a few aircraft fly regular sweeps along the shore. The air arm resents lending pilots to naval duty. The "
          "leaseholders cover part of the fuel bill, reckoning that an aircraft over their moorings costs less than a lost tanker.",
          ('air', 'navy'), after=('cst_zulian_oil',), reward=(Build('air_base', 1, 489), XP('air', 10))),
))

ARMOUR = Branch('armour', 'The Armoured Service', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('arm_parks', 'Count the Hulls in the Parks',
          "Ratio keeps four tank divisions, four motorised and four of infantry, an army built for a war of firepower on open "
          "ground. The tank parks hold some three hundred modern hulls, but nobody can say how many would start on a winter "
          "morning. A park inspection lists every vehicle by its true state of repair, however embarrassing the totals.",
          ('security', 'document'), reward=(Idea('tank_parks'), Event('tank_parks'))),
    Focus('arm_track_shops', 'Track Shops for Every Division',
          "Tanks break tracks, road wheels and gearboxes faster than anything else, and most divisions send them back to Centrum "
          "for repair. Field track shops in each division let crews mend their own vehicles within days. There are not enough "
          "army mechanics for so many shops, so the first year goes to training fitters recruited from the mill towns.",
          ('tools', 'security'), after=('arm_parks',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('arm_live_fire', 'Live Fire on the Dormakaj Plain',
          "Crews have been firing a fraction of their annual allowance to save money. A full live-fire season on the ranges of the "
          "Dormakaj plain lets every crew shoot what the manual demands. Ammunition stocks fall and the neighbouring farms "
          "complain about the noise. Gunnery scores rise sharply by the end of the season.",
          ('training', 'medal'), after=('arm_parks',), reward=(TimedIdea('gunnery_ranges', 365),)),
    Focus('arm_plains', 'Mass the Armour on the Plain',
          "The armoured school wants the tank divisions massed on the Dormakaj plain, where open ground suits them and where any "
          "threat from the west would arrive. Concentration makes a counterstroke possible within hours. It leaves the mountains "
          "and the coast thinly held, and it places Ratio's best formations in full view of its neighbours.",
          ('security', 'command'), after_any=('arm_track_shops', 'arm_live_fire'), cost=10, exclusive=('arm_passes', 'arm_motor'),
          reward=(SwapIdea('tank_parks', 'armoured_fist'),)),
    Focus('arm_passes', 'Hold the Troton Passes',
          "The mountain school argues that Ratio's best defence is its terrain. Infantry and engineers dig into the passes of the "
          "Troton and the forested hills around Centrum, with armour held behind as a reserve. Any invader would pay dearly for "
          "every valley. The plain and Dormakaj, the largest city, would have to be defended from further back.",
          ('shelter', 'security'), after_any=('arm_track_shops', 'arm_live_fire'), cost=10, exclusive=('arm_plains', 'arm_motor'),
          reward=(SwapIdea('tank_parks', 'mountain_bastions'),)),
    Focus('arm_motor', 'A Motor Reserve at Centrum',
          "A third school would keep the motorised divisions together at Centrum and move them by road and rail to wherever "
          "trouble appears. The reserve can reach the plain, the mountains or the coast within days. It depends entirely on "
          "fuel, trucks and timetables. If the railways are cut, the reserve is stranded far from the fight.",
          ('logistics', 'command'), after_any=('arm_track_shops', 'arm_live_fire'), cost=10, exclusive=('arm_plains', 'arm_passes'),
          reward=(SwapIdea('tank_parks', 'motor_reserve'),)),
    Focus('arm_mountain_companies', 'Mountain Companies in the Troton',
          "The army already runs a mountaineer school, but only a few companies have passed through it. Each infantry division now "
          "forms a mountain company equipped for snow, rock and forest, posted to the passes for whole seasons. Recruits from the "
          "mining towns prove the best climbers. Lowland officers regard the posting as a hardship.",
          ('training', 'shelter'), after=('arm_passes',), reward=(Research('infantry_weapons', 0.5, 1), XP('army', 15))),
    Focus('arm_hull_rebuild', 'Rebuild the Older Hulls',
          "With a reserve of alloy steel in the yards, the workshops can rebuild older tanks instead of scrapping them. New armour "
          "plates, engines and gun mantlets give tired hulls another decade of service. It costs less than buying new and keeps "
          "the workshops busy. The rebuilt tanks still fall short of the newest foreign designs.",
          ('tools', 'rebuild'), after_any=('arm_plains', 'arm_passes', 'arm_motor'), requires=(HasFlag('alloy_stock'),),
          reward=(TimedIdea('hull_rebuild', 730),)),
    Focus('arm_staff_course', 'A Course in Combined Arms',
          "Tank, infantry and gun officers in Ratio rarely plan a battle together until one has started. A six-month combined-arms "
          "course at Centrum mixes them in the same syndicates, over the same maps and on the same muddy exercise grounds. "
          "Divisions lose their best captains for half a year while they attend. Those who return can speak every arm's language.",
          ('command', 'document'), after_any=('arm_plains', 'arm_passes', 'arm_motor'),
          reward=(Research('land_doctrine', 0.5, 1), XP('army', 15))),
    Focus('arm_garrisons', 'Garrisons for Four Frontiers',
          "Ratio borders Ustio, Gebet, Wiesmont and Sapin, yet its army has always watched only the west. Standing garrisons are "
          "assigned to each frontier with fixed rotation schedules, local maps and liaison officers. It costs barracks and "
          "manpower. It also means that no neighbour can be surprised by Ratian movements, or surprise Ratio with its own.",
          ('gate', 'security'), after=('arm_staff_course',), reward=(Flag('frontier_garrisons'), WarSupport(0.02))),
))

AIR = Branch('air', 'Wings over Dormakaj', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_sixty', 'Sixty Airframes and a Plan',
          "Forty-eight fighters and a dozen ground-attack machines make up the whole Ratian air arm, based on the fields of "
          "Dormakaj and Centrum. Its officers want a clear mission before they ask for more. A review of every airframe, pilot and runway sets out what "
          "the air arm can actually defend. The answer is sobering, and the review recommends hard choices.",
          ('air', 'document'), reward=(Idea('air_review'), XP('air', 10))),
    Focus('air_dispersal', 'Dispersal Strips Around Dormakaj',
          "Dormakaj holds the busiest air base in Ratio, and a single strike could destroy most of the air arm on the ground. "
          "Dispersal strips, revetments and fuel caches around the plain let squadrons scatter at the first warning. The farms "
          "lose fields to concrete. The air arm gains the ability to survive a first blow.",
          ('runway', 'air'), after=('air_sixty',), reward=(Build('air_base', 2, 306),)),
    Focus('air_centrum_runway', 'A Long Runway for Centrum',
          "The capital's airfield sits among forested hills, with a short runway that limits heavier aircraft. Lengthening it and "
          "adding hardened hangars makes Centrum a proper second base. The engineering is expensive in such broken ground. It "
          "gives the air arm somewhere to fall back to if the western fields are threatened.",
          ('runway', 'tools'), after=('air_sixty',), reward=(Build('air_base', 1, 0),)),
    Focus('air_interceptors', 'Interceptors for the Western Sky',
          "One school wants the whole fighter force tuned to intercept intruders over the frontier, with aircraft held at "
          "readiness on the runway and controllers on the ground. Ratian skies would be expensive to violate. The ground-support squadron would "
          "wither, leaving the tank divisions without aircraft of their own overhead when they need them most.",
          ('air', 'radar'), after=('air_dispersal',), exclusive=('air_support',), reward=(SwapIdea('air_review', 'interceptor_wing'),)),
    Focus('air_support', 'Wings for the Armour',
          "The other school wants the air arm to fly with the tank divisions, training pilots to strike targets the ground forces "
          "call in. The armour would never fight alone. The interceptor force would thin out, and the cities would rely on "
          "anti-aircraft guns rather than fighters to keep raiders away.",
          ('air', 'security'), after=('air_dispersal',), exclusive=('air_interceptors',), reward=(SwapIdea('air_review', 'support_wing'),)),
    Focus('air_radar_hills', 'Radar on the Western Hills',
          "A radar head on the hills above Dormakaj can see far enough across the frontiers with Ustio, Gebet and Wiesmont to give "
          "the fighters real warning. Linked to the control room at the base, it turns guesswork into interception. The "
          "neighbours will notice the mast and may ask what it watches. The air arm's honest answer is everything.",
          ('radar', 'communications'), after=('air_sixty',), reward=(Build('radar_station', 1, 306), Flag('radar_chain'))),
    Focus('air_aggressors', 'A Contract with an Aggressor Team',
          "Since the Belkan War, some of the best former Belkan airmen sell their skill abroad as aggressor squadrons. A contract "
          "would put such a team in Ratian skies for two seasons, playing the enemy in every exercise, and standards would climb "
          "quickly. Officers who remember what Belka took from Ratio dislike Belkans on the payroll, and the fee is steep.",
          ('medal', 'air'), after_any=('air_interceptors', 'air_support'), requires=(After('1998.6.19'),),
          reward=(TimedIdea('aggressor_course', 730),)),
    Focus('air_ground_crews', 'A School for Ground Crews',
          "Ratian aircraft spend too long on the ground waiting for spares and mechanics. A ground crew school at Centrum trains "
          "armourers, fitters and radar technicians on a two-year course. Sortie rates rise as aircraft return to service faster. "
          "The school competes with industry for exactly the same skilled young people.",
          ('training', 'tools'), after=('air_centrum_runway',), reward=(Research('air_doctrine', 0.5, 1), XP('air', 15))),
))

BELKA = Branch('belka', 'The War Beyond the Western Hills', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_outbreak', 'War Beyond the Western Hills',
          "Late in March 1995 Belka goes to war, and two of its neighbours, Ustio and Gebet, are also neighbours of Ratio. "
          "Ratio itself is not a party. Staff officers are recalled from leave to a map room in the basement of the defence "
          "ministry, and every ministry is told to price a long war on the western frontier before the week is out.",
          ('communications', 'security'), requires=(After('1995.3.25'),), reward=(Idea('war_room'), Event('belkan_spring'))),
    Focus('bw_gebet_line', 'Guns Heard from Model',
          "Belkan forces assault Model, a border city in Gebet, and refugees and rumours both start moving along the trunk line "
          "towards Dormakaj. The frontier with Gebet goes on alert and every train arriving from that side is searched. Trade on "
          "the busiest line in Ratio slows sharply for as long as the fighting lasts.",
          ('security', 'rail'), after=('bw_outbreak',), requires=(HasGlobal('ac_bwr_model'),), reward=(TimedIdea('gebet_alarm', 365),)),
    Focus('bw_trunk_freight', 'Freight Off the Gebet Trunk',
          "The through-running agreement with Gebet now carries war risk with every train. The railway diverts freight to the "
          "spine and the Zulian ports and restricts through traffic into Gebet to essential goods. Dormakaj traders lose their new "
          "market for a while. Rail engineers learn how to reroute a whole economy within a week.",
          ('logistics', 'rail'), after=('bw_gebet_line',), requires=(HasFlag('trunk_open'),),
          reward=(TimedIdea('trunk_diversion', 365),)),
    Focus('bw_ustian_front', 'When the Ustian Front Breaks',
          "Ustio is falling under Belkan control, and the Boikos line that Ratio has watched for years now has Belkan forces close "
          "behind it. The western divisions move to full readiness and reservists in Dormakaj are recalled. Nobody in Centrum "
          "knows whether the Belkans intend to stop at the old frontier.",
          ('security', 'gate'), after=('bw_outbreak',), requires=(HasGlobal('ac_bwr_monte_rosa'),),
          reward=(TimedIdea('boikos_front_watch', 365), WarSupport(0.03))),
    Focus('bw_reception', 'Reception Halls at the Crossings',
          "Families fleeing the fighting reach the Dormakaj crossings with what they could carry. Schools and grain warehouses near "
          "the frontier become reception halls where each arrival gets soup, a cot and a numbered card. Host towns already short "
          "of housing complain loudly, and the bill lands on the interior ministry. The cards at least let scattered relatives "
          "find one another.",
          ('refugees', 'shelter'), after=('bw_outbreak',), reward=(Idea('crossing_service'), Flag('reception_halls'))),
    Focus('bw_supply_ustio', 'Sell Ustio What It Needs',
          "Ratio has no love for Belka, which once took its valleys. The council lets Ratian firms sell food, fuel and medicine to "
          "Ustio and its allies, carried to the frontier by Ratian trains. No Ratian unit crosses any border. Belka will remember "
          "the trade, and the valley nationalists will complain that Ustio is being helped.",
          ('logistics', 'diplomacy'), after=('bw_outbreak',), cost=10, exclusive=('bw_closed',),
          requires=(NotGlobal('first_ustian_war'),),
          reward=(SwapIdea('war_room', 'supply_corridor'), Tooltip('Trade only: no war, faction, volunteer or alliance effect.'))),
    Focus('bw_closed', 'Neither Belka Nor Its Enemies',
          "The council chooses the narrowest path: Ratio sells nothing that shoots or burns to any belligerent, refuses passage to "
          "every foreign column and puts a sentry on every crossing. Exiles from Ustio accuse Centrum of looking away, while "
          "Belkan envoys suspect that the sentries face in only one direction. The western divisions hold their readiness until "
          "the last shot.",
          ('security', 'peace'), after=('bw_outbreak',), cost=10, exclusive=('bw_supply_ustio',),
          reward=(SwapIdea('war_room', 'closed_frontier'),)),
    Focus('bw_hospital_trains', 'Hospital Trains on the Boikos Branch',
          "The branch line into Boikos, reopened for passengers and mail, now carries hospital trains. Ratian doctors bring "
          "wounded and sick civilians out of the war zone to wards in Dormakaj and Centrum. The trains run under medical markings "
          "and carry no soldiers. They earn Ratio a gratitude in the valleys that no speech could buy.",
          ('medical', 'rail'), after=('bw_outbreak',), requires=(HasFlag('boikos_trains'), NotGlobal('first_ustian_war')),
          reward=(TimedIdea('hospital_trains', 365),)),
    Focus('bw_garrisons_stand', 'The Frontier Garrisons Stand To',
          "The standing garrisons assigned to each frontier before the war now earn their keep. They move to a wartime posture "
          "within a day, and liaison officers keep open lines to every neighbouring command. Rotation schedules keep the troops "
          "fresh. The army learns what its peacetime planning was really worth.",
          ('security', 'medal'), after=('bw_outbreak',), requires=(HasFlag('frontier_garrisons'),),
          reward=(TimedIdea('frontier_alert', 180), XP('army', 15))),
    Focus('bw_waldreich_ash', 'Ash from the Waldreich',
          "Reports that Belka has set off nuclear weapons among the Waldreich peaks send every Ratian weather station to hourly "
          "wind soundings. A fallout watch samples air, water and milk across the western districts and publishes the results daily. Most days "
          "show little. The sampling costs money and laboratory time, and it keeps panic from outrunning the facts.",
          ('medical', 'telescope'), after=('bw_outbreak',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(Idea('fallout_watch'),)),
    Focus('bw_guns_silent', 'When the Belkan Guns Fall Silent',
          "The Belkan War ends, and the council stands down the night shifts of the war room and sends the reservists home, "
          "though the frontier stays watchful. Ministries begin counting what the spring cost them: trade lost, crossings "
          "crowded, overtime paid. The war is over, yet its consequences on Ratian frontiers have barely begun.",
          ('peace', 'document'), after=('bw_outbreak',), requires=(After('1995.6.20'), NotGlobal('belkan_war_is_happening')),
          reward=(Stability(0.03), WarSupport(-0.02))),
    Focus('bw_belka_won', 'A Victorious Belka Beyond Ustio',
          "Belka emerges from the war as the victor. For Ratio this means a stronger, prouder neighbour just beyond Ustio, the "
          "same power that once took the valleys. The western divisions are told to plan for a Belka that may want more. The "
          "frontier itself is unchanged, yet from now on each defence budget is drafted against the gloomier forecast.",
          ('security', 'command'), after=('bw_guns_silent',), exclusive=('bw_belka_lost',),
          requires=(HasGlobal('belka_won_belkan_war'),), reward=(Idea('wary_neighbour'),)),
    Focus('bw_belka_lost', 'A Defeated Belka Beyond Ustio',
          "Belka ends the war beaten, and the towns of the north need everything at once. Centrum plate, Ratian cement and Dormakaj "
          "wagons are bought by builders from every side of the old front, and the mills book two years of orders. A few voices "
          "in Dormakaj ask whether a humbled Belka changes anything about the valleys, and the council declines to answer.",
          ('rebuild', 'economy'), after=('bw_guns_silent',), exclusive=('bw_belka_won',),
          requires=(HasGlobal('belka_lost_belkan_war'),), reward=(TimedIdea('rebuild_orders', 540),)),
    Focus('bw_lessons', 'What the Spring War Taught',
          "Ratian staff officers kept a diary of the spring war from their side of the frontier: how fast the front moved, how "
          "much hung on fuel and rail, how civilians clogged every road away from the guns. The diary becomes a staff paper on "
          "supply, dispersal and civil defence, and its first readers on the council do not enjoy a single page of it.",
          ('document', 'command'), after_any=('bw_belka_won', 'bw_belka_lost'),
          reward=(Research('logistics_tech', 0.5, 1), Research('land_doctrine', 0.3, 1))),
))

SKY = Branch('sky', 'Ulysses and the New Century', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_date', 'A Bulletin for the Coming Impact',
          "Ulysses stops being a distant warning in April 1996, when the FCU tells the world that the asteroid will hit the "
          "Earth. Nobody can name the impact sites, and Ratio owns no telescope worth the name. The council orders a "
          "short, plain bulletin read on the state radio every week, so that rumour at least has something to compete with.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),), reward=(Idea('sky_bulletins'), Event('ulysses_date'))),
    Focus('sky_cellars', 'Cellars Under the Centrum Hills',
          "Centrum is built on forested hills riddled with old mine galleries and storage cellars. Engineers survey them, shore up "
          "the safest and stock them with water, lamps and bedding for the districts above. It is cheaper than new bunkers. "
          "Families learn where their nearest gallery entrance is, and some refuse to believe it will matter.",
          ('shelter', 'civil'), after=('sky_date',), reward=(Idea('hill_cellars'),)),
    Focus('sky_grain', 'Fill the Grain Halls',
          "Shoppers strip the shelves every time Ulysses reaches the front page. The council fills state warehouses with enough "
          "flour, lamp oil and medicine for a quarter-year of shortage, and sells the oldest sacks back into the shops each month. "
          "Stockpiling while prices spike costs the treasury dearly. Warehouses visibly full steady the cities better than any "
          "minister on the radio.",
          ('economy', 'shelter'), after=('sky_date',), reward=(TimedIdea('grain_halls', 1095),)),
    Focus('sky_trains', 'Timetables Out of the Cities',
          "The reception halls built during the Belkan War already know how to register, feed and house people in a hurry. The "
          "evacuation plan reuses them, pairing each city quarter with a numbered train and a hall in the countryside. The first "
          "rehearsal leaves a carriage of Centrum pensioners in a valley siding overnight, and the timetables are rewritten twice "
          "before families trust them.",
          ('rail', 'refugees'), after=('sky_date',), cost=10, exclusive=('sky_wardens',), requires=(HasFlag('reception_halls'),),
          reward=(Idea('evacuation_trains'),)),
    Focus('sky_wardens', 'Wardens for Every Block',
          "The opposite plan keeps people at home and below ground. Every city block elects a shelter warden who knows the "
          "cellars, the elderly residents and the first-aid kits. It costs little and asks a great deal of volunteers. Its "
          "weakness is plain to every engineer who signs off on it: a cellar is only ever as safe as the ground above it.",
          ('shelter', 'security'), after=('sky_date',), cost=10, exclusive=('sky_trains',), reward=(Idea('shelter_wardens'),)),
    Focus('sky_valley_towns', 'Valley Towns Take the Evacuees',
          "The evacuation timetables send most city dwellers into Ratio Valley, whose small towns lack the roads and water for so "
          "many. Engineers widen the valley roads and lay mains to the reception halls. Residents complain that their towns are "
          "being treated as a shelter for others. They also gain roads they waited decades for.",
          ('civil', 'rail'), after=('sky_trains',), reward=(Build('infrastructure', 1, 472),)),
    Focus('sky_watch_post', 'Watching the Sky from the Troton',
          "The radar crews of the air arm already watch the western sky. A tracking post high in the Troton, pairing foreign "
          "observatory data with Ratian readings, gives the weekly bulletin numbers of its own. It cannot stop anything falling. "
          "It lets Ratio say what it knows, and when, without waiting for foreign news.",
          ('telescope', 'radar'), after=('sky_date',), requires=(HasFlag('radar_chain'),), reward=(Build('radar_station', 1, 419),)),
    Focus('sky_roche', 'The Night Ulysses Breaks Apart',
          "By the night of 8 July 1999 Ulysses is inside the Roche limit. Whatever its fragments do, recovery crews of engineers, doctors "
          "and rail workers stand ready in every district to clear roads, restore power and treat the injured. Each crew knows "
          "its depot and its radio channel. Nobody yet knows whether they will be needed.",
          ('meteor', 'rebuild'), after=('sky_date',), requires=(After('1999.7.8'),), reward=(TimedIdea('fragment_crews', 730),)),
    Focus('sky_usean_war', 'Orders from a Distant War',
          "Fighting on the far continent of Usea sends buyers hunting for ore, plate and fuel oil wherever they can find them. With "
          "every Ratian hull on the register, the harbour board can route ships away from danger and still take the orders. The mills "
          "run extra shifts. Nobody in Centrum pretends that the demand will outlast the war.",
          ('economy', 'navy'), after=('sky_date',), requires=(HasGlobal('ac_ucw_war_started'), HasFlag('convoy_register')),
          reward=(TimedIdea('usean_orders', 540),)),
    Focus('sky_account', 'Ratio at the Close of 2005',
          "With the era closing, the council prints a short ledger of the nation: mills, rails, harbours, garrisons, and the "
          "valleys question in whatever shape it now has. No pledges are attached to it. The ledger exists so that the next "
          "government, elected or appointed, inherits numbers instead of boasts, and so that Ratians can judge how far the "
          "country has travelled since January 1991.",
          ('document', 'assembly'), after_any=('sky_cellars', 'sky_grain', 'sky_trains', 'sky_wardens'),
          requires=(After('2005.1.1'), HasFlag('form_settled')),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (COUNCIL, VALLEYS, STEEL, RAIL, COAST, ARMOUR, AIR, BELKA, SKY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('ore_season', 'Sign a Season of Ore Contracts',
                'The ministry of mines sells a season of Troton ore and Centrum billets forward to foreign buyers. Repeatable once '
                'a year; the mills forgo some alloy work while the contracts run.',
                40, (TimedIdea('ore_contract', 180),), requires=(Completed('stl_troton_chromium'),), cooldown=365),
    DecisionDef('bond_tranche', 'Reopen the Bond Window',
                'The treasury sells another tranche of valley bonds at the Centrum exchange. Available each year once the first '
                'bonds have sold.',
                50, (TimedIdea('bond_window', 180),), requires=(HasFlag('purchase_path'), Completed('val_bonds')), cooldown=365),
    DecisionDef('frontier_drill', 'Raise the Frontier Alert',
                'The garrisons of every frontier stand to for three months. Repeatable twice a year; the alert burns fuel and '
                'overtime.',
                25, (TimedIdea('frontier_alert', 90),), requires=(After('1995.3.25'),), cooldown=180),
    DecisionDef('send_relief_columns', 'Send Relief Columns West',
                'Lorries from the reception halls carry food and medicine to the frontier towns. Once only; the columns cost '
                'political capital at home.',
                30, (TimedIdea('relief_columns', 180), Stability(0.01)), requires=(HasFlag('reception_halls'),)),
    DecisionDef('headland_radar', 'A Radar on the Zulian Headland',
                'Engineers raise a coastal radar above Sukaxhija for shipping and air traffic. A one-time works programme.',
                60, (Build('radar_station', 1, 489),), requires=(Completed('cst_harbour_board'),)),
    DecisionDef('district_hearing', 'Summon a District Hearing',
                'Council members sit for a week in one district and take petitions in public. Repeatable once a year.',
                20, (Stability(0.02),), requires=(Completed('cncl_hearings'),), cooldown=365),
)
