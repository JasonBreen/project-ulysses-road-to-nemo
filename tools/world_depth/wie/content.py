"""Wielvakia (WIE): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (neutrality ruling at 57 percent with
elections not allowed after the vote dated 1 January 1991, democratic 30, fascism 12 and communism 1
percent, stability 0.70, war support 0.80, limited_conscription), the unnamed National Administration
office and the executive-office institution profile, the country names, the four 1991 states with
their localised names, victory points, resources and buildings, FATO's claim on South Gangel, the
Wielvakian Low Lands strategic region, land neighbours computed from map/provinces.bmp and the global
flags other mod scripts already set. Official: ACES Chronicle rows used only as date anchors for
regional pressure, each cited by its exact key. Everything else, including every Wielvakian choice,
office, idea, building, decision and event, is provisional gameplay. The tree never moves a border,
core or claim, declares war, makes peace, annexes or changes a faction.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='WIE', name='Wielvakia', root='world', package='wie',
                  themes=('command', 'economy', 'gate'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party neutrality with elections_allowed = no after a last election dated 1 January '
           '1991 (election_frequency 48); popularities neutrality 57, democratic 30, fascism 12, communism 1; stability 0.70 and '
           'war support 0.80; the limited_conscription law; grand doctrines superior_firepower, new_fleet_in_being and '
           'new_operational_integrity; tech_mountaineers among the starting technology. The starting leader is the unnamed '
           'National Administration office (WIE_ac_government_office, centrism_na), whose description says its 1991 holder has '
           'not been established; the institution profile is an executive office (ac_pol_form_executive_office). Country names: '
           'Republic of Wielvakia (democratic and neutrality), Wielvakian State (fascism). The tree never names a holder.',
           'mod/2985041246/history/countries/WIE - Wielvakia.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml; mod/2985041246/common/scripted_effects/ac_politics.txt; '
           'tools/world_foundation/country_registry.json; tools/institutions/profiles.json'),
    Source('Mod provenance',
           'Geography: 1991 states 325 South Gangel (town; plains; oil 16, steel 8, aluminium 4; one civilian and three military '
           'factories; air base 1; claimed by FATO), 326 Farnlands (town; plains; oil 16, steel 8; one civilian and three military '
           'factories; victory point Nadomlin), 367 Alaoboa (capital; metropolis; plains, mountain and urban; oil 16, steel 18, '
           'tungsten 7, chromium 6; four civilian and four military factories, the fuel silo, air base 5; victory point Mankovce) '
           'and 372 Vakia (city; mountain, forest, desert and hills, the only coast; tungsten 21, chromium 16; two civilian and one '
           'military factory, three dockyards, naval bases of level 5 and 2, air base 6). South Gangel, Farnlands and Alaoboa form '
           'the Wielvakian Low Lands strategic region. Land neighbours from map/provinces.bmp: FATO (Gangl, against South Gangel '
           'and Farnlands), Gebet (Old Gebet and Mersin Flats, against South Gangel and Alaoboa), Ratio (Ratio District A and '
           'Centrum against Alaoboa, Centrum and Troton Mountains against Vakia) and Nordlands (West Norden, Hait Mountain and '
           'Oregonen, against Farnlands and Vakia). Free building slots: one shared slot in Alaoboa and none elsewhere. The '
           'non-ASCII harbour and South Gangel victory point captions and the placeholder logistics-centre captions are not used; '
           'no other place is named.',
           'mod/2985041246/history/states/325-State_325.txt, 326-State_326.txt, 367-State_367.txt, 372-State_372.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; '
           'mod/2985041246/localisation/english/strategic_region_names_l_english.yml; '
           'mod/2985041246/map/strategicregions/108-Wielvakian Low Lands.txt; tools/regional_labels/labels.json'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: a retained authored army of six tank, four infantry and four motorised '
           'divisions with 300 modern tanks in stock; 8 civilian, 11 military and 3 naval factories; 48 fighters and 12 support '
           'aircraft; two destroyers and one submarine; 200 convoys; oil base 48; fiscal profile GDP 338.967, debt ratio 0.3, '
           'collection 0.85. Fictional calibration, not canon national accounts or order of battle.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json'),
    Source('Mod provenance',
           'Neighbour consistency: the Nordlands spec describes the Wielvakian frontier as running past Farnlands and Vakia with '
           'lighter traffic through mountain roads and small harbours, and offers Nordlandic customs desks, watch posts and a '
           'joint statement as Nordlandic choices. This tree keeps to that geography and claims no Nordlandic act. The Ratio '
           'spec, corrected on 15 November 2026 to use the mod name Wielvakia, shares this border and offers only Ratian '
           'garrisons and radar; this tree claims no Ratian act. FATO and Gebet have no world-depth spec; FATO keeps its claim on South '
           'Gangel untouched.',
           'tools/world_depth/nrl/content.py; tools/world_depth/rat/content.py; mod/2985041246/history/states/325-State_325.txt'),
    Source('Official',
           'Context only: the Republic of Gebet gains its independence. Background to the Gebet liaison focus; nothing about '
           'Wielvakia follows from it.', '1988 / 02.08'),
    Source('Official',
           'Date anchor: Belka sells territory in its north to FATO and its eastern territory to neighbouring eastern nations. '
           'Date gate of the South Gangel brief; no Wielvakian purchase, border change or claim is implied.', '1991 / 08.29'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Date gate of the war branch; Wielvakia is not claimed as a party.',
           '1995 / 03.25'),
    Source('Official',
           'An assault on Model, a border city in Gebet, on the eastern front. Premise of the Model focus, which also reads the '
           'mod flag ac_bwr_model; no effect inside Wielvakia is claimed.', '1995 / 03.27'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Premise of the grain store focus, which reads '
           'belka_dropped_nukes; no fallout in Wielvakia is claimed.', '1995 / 06.06'),
    Source('Official',
           'A treaty is signed in Lumen and the Belkan War ends. Date gate of the stand-down focus, which also waits until '
           'belkan_war_is_happening is clear.', '1995 / 06.20'),
    Source('Official',
           'A World With No Boundaries launches a coup. Date gate of the officer oath focus; no Wielvakian involvement is claimed.',
           '1995 / 12.25'),
    Source('Official',
           'The President of the FCU announces that Ulysses will impact the Earth. Date gate of the Ulysses branch; where '
           'fragments fall is never stated for Wielvakia.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries as aggressor squadrons. Date gate of the '
           'aggressor focus; no individual is named and no hire by Wielvakia is claimed as fact.', '1998 / 06.19'),
    Source('Official',
           'The IAU damage estimate is revised to include fragments falling on the eastern part of the Anean continent. Date '
           'gate of the impact drills focus; the estimate names no Wielvakian district.', '1998 / 07.29'),
    Source('Official',
           'Ulysses passes through the Roche limit of the Earth. Date gate of the recovery focus; no damage in Wielvakia is '
           'claimed.', '1999 / 07.08'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_bwr_model (common/scripted_effects/ac_belkan_record.txt, set while Belka is '
           'at war with Gebet), belkan_war_is_happening, belka_won_belkan_war, belka_lost_belkan_war and belka_dropped_nukes '
           '(events/Belka.txt and common/decisions/BLK_decisions.txt). Outcome reactions are leaf focuses, so no outcome blocks '
           'the tree.',
           'mod/2985041246/common/scripted_effects/ac_belkan_record.txt; mod/2985041246/events/Belka.txt; '
           'mod/2985041246/common/decisions/BLK_decisions.txt'),
    Source('Provisional gameplay',
           'All Wielvakian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, claim, war, peace, annexation or faction effects; buildings only in the '
           'four 1991 states and within their free slots.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the executive office
    IdeaDef('office_inventory', 'The Office Takes Stock', 'The National Administration is listing its own powers, decrees and posts before deciding what to keep.',
            {'political_power_gain': 0.10, 'stability_factor': -0.02}, ('document', 'command')),
    IdeaDef('state_councils', 'Quarterly State Councils', 'Advisory councils in each of the four states question their governors every quarter.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('assembly', 'civil')),
    IdeaDef('chamber_charter', 'Charter of the Chamber', 'A chamber elected from the four states is drafting its rules, and the cabinet already answers to it.',
            {'stability_factor': 0.04, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('elected_chamber', 'Deputies of the Four States', 'Deputies from Alaoboa, Vakia, Farnlands and South Gangel make and unmake governments.',
            {'stability_factor': 0.07, 'political_power_factor': 0.06, 'research_speed_factor': 0.03}, ('ballot', 'assembly')),
    IdeaDef('staff_seals', 'Seals at Headquarters', 'The general staff governs as a council until the frontiers are judged settled.',
            {'political_power_gain': 0.15, 'war_support_factor': 0.05, 'stability_factor': -0.03}, ('command', 'security')),
    IdeaDef('staff_budget', 'The Readiness Budget', 'Every ministry request is ranked against the army plan for the year.',
            {'political_power_gain': 0.15, 'production_speed_arms_factory_factor': 0.08, 'consumer_goods_factor': 0.03}, ('command', 'economy')),
    IdeaDef('directorate_order', 'Government by Directorate Decree', 'The directorate governs by decree in the name of the nation.',
            {'war_support_factor': 0.08, 'stability_factor': 0.03, 'consumer_goods_factor': 0.05}, ('security', 'medal')),
    IdeaDef('directorate_leagues', 'The Directorate Leagues', 'Uniformed youth leagues drill in every lowland town and camp in the Vakia hills.',
            {'war_support_factor': 0.10, 'training_time_army_factor': -0.08, 'consumer_goods_factor': 0.04}, ('training', 'medal')),
    IdeaDef('office_statute', 'Statute of the Executive Office', 'The executive office governs under a written statute with a review every four years.',
            {'political_power_gain': 0.10, 'stability_factor': 0.03}, ('document', 'scales')),
    IdeaDef('reviewed_office', 'An Office Under Review', 'The four state councils have questioned the executive office in public and printed their verdict.',
            {'political_power_gain': 0.10, 'stability_factor': 0.05, 'political_power_factor': 0.04}, ('scales', 'assembly')),
    IdeaDef('service_examinations', 'Entrance by Examination', 'Every new civil servant passes a written examination set by a mixed board.',
            {'political_power_factor': 0.06, 'production_factory_efficiency_gain_factor': 0.03}, ('document', 'training')),
    # lowland oil
    IdeaDef('field_survey', 'Three Fields Surveyed', 'The state now knows roughly how much oil lies under the three lowland fields.',
            {'production_speed_buildings_factor': 0.03}, ('economy', 'tools')),
    IdeaDef('national_oil_company', 'One Company for Lowland Crude', 'A single state company drills, pipes, refines and sells all lowland oil.',
            {'political_power_gain': 0.05, 'production_speed_industrial_complex_factor': 0.08}, ('command', 'economy')),
    IdeaDef('lowland_concessions', 'Auctioned Lowland Blocks', 'Private drillers work auctioned blocks and pay royalties on every barrel.',
            {'production_speed_buildings_factor': 0.06, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('regulated_concessions', 'Concessions Under One Code', 'Every licensed driller works to the same safety, wage and abandonment rules.',
            {'production_speed_buildings_factor': 0.08, 'stability_factor': 0.02}, ('scales', 'economy')),
    IdeaDef('oil_revenue_fund', 'The Barrel Fund', 'A fixed share of oil revenue is invested and paid out as a steady yearly sum.',
            {'stability_factor': 0.04, 'political_power_factor': 0.04}, ('scales', 'shelter')),
    # Vakia ore
    IdeaDef('mine_registry', 'Register of the Galleries', 'Every Vakia mine gallery, seam and owner is entered on one register.',
            {'production_speed_buildings_factor': 0.02, 'production_factory_efficiency_gain_factor': 0.02}, ('tools', 'document')),
    IdeaDef('ore_contracts', 'Concentrate for Foreign Smelters', 'Tungsten and chromium concentrate is sold abroad at assayed prices.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('long_ore_contracts', 'Ten-Year Ore Agreements', 'Fixed prices and guaranteed tonnage, reopened for review every three years.',
            {'consumer_goods_factor': -0.05, 'political_power_gain': 0.05, 'stability_factor': 0.02}, ('document', 'economy')),
    IdeaDef('alloy_reserve', 'Ore for the Home Mills', 'Concentrate exports are restricted and domestic mills receive the ore first.',
            {'production_factory_efficiency_gain_factor': 0.04, 'consumer_goods_factor': 0.02}, ('industry', 'security')),
    IdeaDef('plate_mills', 'Plate Rolled from Vakia Chromium', 'The capital mills roll armour plate from domestic alloy.',
            {'production_speed_arms_factory_factor': 0.10, 'production_factory_max_efficiency_factor': 0.04}, ('industry', 'tools')),
    IdeaDef('mine_rescue', 'Gallery Rescue Stations', 'Trained crews can reach any Vakia gallery within an hour of a collapse.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.02}, ('medical', 'shelter')),
    IdeaDef('metallurgy_school', 'The Mining District School', 'Assayers, surveyors and furnace hands are trained where the ore is dug.',
            {'research_speed_factor': 0.03, 'production_factory_efficiency_gain_factor': 0.03}, ('training', 'science')),
    # the armoured army
    IdeaDef('armour_first', 'The Armour Question', 'The general staff must explain in writing what six tank divisions are for.',
            {'army_org_factor': 0.02, 'political_power_gain': -0.05}, ('command', 'document')),
    IdeaDef('fuel_allowance', 'Guaranteed Training Fuel', 'Every tank crew draws a fixed fuel allowance for field training.',
            {'experience_gain_army_factor': 0.08, 'consumer_goods_factor': 0.02}, ('logistics', 'training')),
    IdeaDef('massed_armour', 'The Armoured Fist', 'Six tank divisions held together on the lowland plain.',
            {'army_attack_factor': 0.05, 'army_org_factor': 0.04}, ('command', 'gate')),
    IdeaDef('pass_defence', 'Infantry in the Passes', 'Infantry and mountain troops hold the Vakia passes; the armour waits in reserve.',
            {'army_defence_factor': 0.06, 'army_core_defence_factor': 0.06}, ('security', 'training')),
    IdeaDef('motor_brigades', 'Mixed Motor Brigades', 'Tanks, carriers and guns in brigades that fit both plain and valley.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.08}, ('logistics', 'command')),
    IdeaDef('brigade_trials', 'Valley Brigade Trials', 'The new brigades are tested on mountain roads and lowland tracks.',
            {'experience_gain_army_factor': 0.10, 'training_time_army_factor': -0.08}, ('training', 'logistics')),
    IdeaDef('call_up_register', 'The Call-Up Register', 'Every former conscript is listed by district, skill and unit.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.05}, ('document', 'security')),
    IdeaDef('career_crews', 'Career Tank Crews', 'Long-service crews on career pay keep the same tank for years.',
            {'army_org_factor': 0.06, 'experience_gain_army_factor': 0.10}, ('medal', 'training')),
    IdeaDef('mobilisation_tables', 'Rehearsed Mobilisation Tables', 'Every reservist, train and fuel truck has a slot in the headquarters tables.',
            {'planning_speed': 0.10, 'army_core_defence_factor': 0.04}, ('command', 'rail')),
    # four frontiers
    IdeaDef('frontier_review', 'The Frontier Review', 'Crossing records from all four frontiers are being gathered in Mankovce.',
            {'stability_factor': 0.02}, ('gate', 'document')),
    IdeaDef('northern_posts', 'Posted Hours on the Northern Posts', 'The crossings into Nordlands keep posted hours, bilingual forms and a telephone line.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.02}, ('diplomacy', 'document')),
    IdeaDef('ratian_rail', 'Through Trains to Centrum', 'Trains cross into Ratio without changing crews at the frontier.',
            {'production_speed_infrastructure_factor': 0.08, 'consumer_goods_factor': -0.02}, ('rail', 'gate')),
    IdeaDef('open_frontiers', 'Spot Checks Only', 'Crossings stay open around the clock with inspections by sample.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.01}, ('gate', 'economy')),
    IdeaDef('armed_frontiers', 'Closed Nights on the Frontier', 'Armed customs police staff every crossing, closed from dusk to dawn.',
            {'army_core_defence_factor': 0.05, 'consumer_goods_factor': 0.02}, ('security', 'gate')),
    IdeaDef('convention_proposal', 'A Draft Frontier Convention', 'Wielvakia has offered every neighbour a common text on crossings and incidents.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('peace', 'diplomacy')),
    IdeaDef('frontier_guard', 'The Frontier Guard Corps', 'A uniformed corps patrols between the crossings on all four frontiers.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.03}, ('security', 'medal')),
    IdeaDef('frontier_secretariat', 'The Frontier Secretariat', 'A small office in Mankovce answers frontier complaints from any neighbour.',
            {'stability_factor': 0.05, 'political_power_gain': 0.08}, ('peace', 'document')),
    # the coast
    IdeaDef('coast_command', 'The Vakia Coast Command', 'Two destroyers, one submarine and two harbours under one command.',
            {'navy_org_factor': 0.03}, ('navy', 'command')),
    IdeaDef('slipway_contracts', 'Slipways for Hire', 'The Vakia yards overhaul coasters and ferries of any flag.',
            {'industrial_capacity_dockyard': 0.05, 'repair_speed_factor': 0.08}, ('tools', 'navy')),
    IdeaDef('ore_convoys', 'Escorted Ore Sailings', 'Ore ships leave the Vakia harbours in escorted groups.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.05}, ('navy', 'logistics')),
    IdeaDef('inshore_patrols', 'The Inshore Flotilla', 'Small fast boats patrol the Vakia coast and the harbour mouths.',
            {'naval_speed_factor': 0.05, 'naval_coordination': 0.04}, ('navy', 'security')),
    IdeaDef('fishery_patrols', 'Fishery Protection off Vakia', 'Patrol boats check catches and rescue crews in bad weather.',
            {'stability_factor': 0.02, 'navy_org_factor': 0.03}, ('fishing', 'navy')),
    IdeaDef('vakia_port_fund', 'The Vakia Port Fund', 'A guaranteed share of national revenue for the only coast.',
            {'production_speed_buildings_factor': 0.05, 'industrial_capacity_dockyard': 0.03}, ('navy', 'economy')),
    IdeaDef('naval_school', 'The Harbour Naval School', 'Officers and ratings trained at the main Vakia harbour.',
            {'navy_org_factor': 0.05, 'naval_coordination': 0.03}, ('training', 'navy')),
    # the air arm
    IdeaDef('air_review', 'The Air Arm Review', 'The air arm is deciding what it must defend first.',
            {'experience_gain_air_factor': 0.04}, ('air', 'document')),
    IdeaDef('flying_hours', 'Hours Before Hulls', 'More flying hours for existing pilots before any new aircraft.',
            {'experience_gain_air_factor': 0.10, 'air_mission_efficiency': 0.03}, ('training', 'air')),
    IdeaDef('aggressor_course', 'The Hired Aggressor Course', 'Foreign instructors fly against Wielvakian pilots at the capital field.',
            {'air_superiority_efficiency': 0.06, 'experience_gain_air_factor': 0.10}, ('air', 'medal')),
    IdeaDef('home_instructors', 'Home-Grown Aggressors', 'A unit of Wielvakian squadron leaders writes and flies its own enemy tactics.',
            {'air_superiority_efficiency': 0.05, 'air_mission_efficiency': 0.04}, ('air', 'training')),
    IdeaDef('lowland_air_plan', 'The Low Lands Air Plan', 'One plan links radar, fighters and dispersal fields across the plain.',
            {'air_detection': 0.08, 'air_defence_factor': 0.05}, ('radar', 'air')),
    # the war beyond Gebet
    IdeaDef('war_alert', 'Alert on the Gebet Frontier', 'Frontier commands stay on alert while Belka is at war.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.03}, ('security', 'communications')),
    IdeaDef('refuge_crossings', 'Crossings Open to Families', 'Families from Gebet may cross and register at the frontier towns.',
            {'stability_factor': -0.02, 'political_power_gain': 0.05}, ('refugees', 'gate')),
    IdeaDef('sealed_crossings', 'Sealed Gebet Crossings', 'The Gebet crossings admit only diplomatic and relief traffic.',
            {'war_support_factor': 0.04, 'army_core_defence_factor': 0.03}, ('security', 'gate')),
    IdeaDef('reception_halls', 'Halls for the Arrivals', 'Schools and sports halls in South Gangel house registered arrivals.',
            {'stability_factor': 0.02, 'consumer_goods_factor': 0.03}, ('refugees', 'civil')),
    IdeaDef('gebet_line', 'Two Divisions on the Gebet Line', 'Two divisions hold the frontier opposite Gebet.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.04}, ('security', 'command')),
    IdeaDef('relief_fuel', 'Fuel for Relief Convoys', 'Stored fuel is released at cost for relief convoys of every flag.',
            {'stability_factor': 0.03, 'political_power_factor': 0.04}, ('logistics', 'peace')),
    IdeaDef('grain_seal', 'Sealed Grain Stores', 'Lowland grain from the war months is stored, tested and released only when clean.',
            {'stability_factor': 0.04}, ('medical', 'shelter')),
    IdeaDef('rebuild_contracts', 'Rebuilding Orders for Lowland Mills', 'Lowland factories supply the rebuilding of the war-damaged region.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': -0.02}, ('rebuild', 'industry')),
    IdeaDef('long_watch', 'The Long Watch', 'A victorious Belka lies two frontiers away, and the army stays ready.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.04}, ('security', 'radar')),
    IdeaDef('officer_oath', 'The Renewed Officer Oath', 'Every officer has renewed the oath and declared any foreign association.',
            {'army_org_factor': 0.03, 'stability_factor': 0.02}, ('medal', 'document')),
    # Ulysses
    IdeaDef('impact_watch', 'The Impact Commission', 'A civil defence commission plans for an asteroid whose fragments nobody can place.',
            {'stability_factor': -0.02, 'political_power_gain': 0.05}, ('meteor', 'document')),
    IdeaDef('city_shelters', 'Shelters Under Mankovce', 'Deep shelters under the capital and the lowland towns.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('dispersal_plans', 'Plans to Leave the Cities', 'Every lowland town knows which train, road and village to use.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.08}, ('refugees', 'rail')),
    IdeaDef('gallery_shelters', 'Shelters in the Worked-Out Galleries', 'Disused Vakia mine galleries fitted out as shelters.',
            {'stability_factor': 0.03, 'air_defence_factor': 0.03}, ('shelter', 'tools')),
    IdeaDef('impact_drills', 'Impact Drills', 'Sirens, assembly points and rehearsed routes in every district.',
            {'stability_factor': 0.03, 'planning_speed': 0.05}, ('meteor', 'security')),
    IdeaDef('recovery_teams', 'Teams Kept Ready for Disaster', 'Engineers, medics and heavy plant held ready for any disaster.',
            {'repair_speed_factor': 0.10, 'stability_factor': 0.02}, ('rebuild', 'medical')),
    IdeaDef('regional_recovery', 'Help Across the Frontiers', 'Wielvakian recovery teams work wherever a neighbour asks for them.',
            {'political_power_gain': 0.10, 'stability_factor': 0.03}, ('peace', 'rebuild')),
    # decisions
    IdeaDef('crude_forward', 'Crude Sold Forward', 'A season of lowland crude has been sold before it is pumped.',
            {'political_power_gain': 0.15, 'production_speed_buildings_factor': -0.03}, ('economy', 'document')),
    IdeaDef('autumn_manoeuvres', 'Manoeuvres on the Plain', 'Whole divisions are in the field on the Farnlands range.',
            {'experience_gain_army_factor': 0.10, 'army_org_factor': 0.03}, ('training', 'command')),
    IdeaDef('relief_train', 'The Relief Train', 'A Wielvakian relief train runs to the frontier with food and medicine.',
            {'stability_factor': 0.03}, ('rail', 'medical')),
    IdeaDef('port_calls', 'Foreign Calls at Vakia', 'Visiting merchant ships load and unload under reduced harbour dues.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.01}, ('navy', 'diplomacy')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('chamber_cabinet', 'Cabinet of the Wielvakian Chamber',
           'A cabinet drawn from the majority of a chamber elected in Alaoboa, Vakia, Farnlands and South Gangel, governing '
           'collectively and answerable to the deputies. Provisional gameplay office with no named holder.',
           'democratic', 'centrism', elections=True),
    Office('staff_council', 'Governing Council of the Staff',
           'Senior officers of the general staff sitting as a council, with ministries reporting to them until the frontiers '
           'are judged settled. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
    Office('state_directorate', 'Directorate of the Wielvakian State',
           'A directorate drawn from the nationalist movement and its allies in the frontier districts, governing by decree in '
           'the name of the nation. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('executive_ledger', 'The Ledger of the Executive Office', (
        "The inventory arrives at the cabinet room in Mankovce in eleven bound volumes, each one stamped by a different "
        "ministry. Since the vote dated January 1991 the National Administration has governed without a further ballot on the "
        "calendar, and until now nobody, including the Administration itself, had written down in one place what the office "
        "actually does.",
        "The volumes make uneasy reading. Decrees from earlier governments were never repealed and are still enforced in some "
        "districts and ignored in others. Two ministries license the same oil wells. Several hundred salaried posts have no "
        "recorded duties. The army takes the largest single share of the budget, and the line for schools in Vakia has not "
        "changed in years. Democrats will read the ledger as proof that the office must answer to someone. Officers will read "
        "it as proof that only discipline can repair it, and the nationalist benches will find in it a state gone soft.",
        "Before any of those arguments begins, the cabinet must decide what happens to the volumes themselves. A printed "
        "summary would put the worst pages in every newspaper and start the debate on the public's terms. Kept as a working "
        "paper, the ledger stays a tool for the office to reform itself quietly, provided the clerks who compiled it can be "
        "trusted to keep their copies in their desks.",
    ), (
        Option('Print a summary for the public.', (Stability(0.02), PP(-10))),
        Option('Keep it as an internal working paper.', (PP(30), Event('ledger_pages', 14))),
    ), picture=0),
    EventDef('ledger_pages', 'Ledger Pages in the Morning Papers', (
        "Two weeks after the cabinet chose discretion, a Mankovce daily prints four photographed pages of the inventory on its "
        "front page. They are the worst four the paper could have chosen: the list of posts without duties, with the "
        "ministries that pay them and the totals for each. By noon the opposition benches have copies, and by evening so have "
        "the advisory clubs in every lowland town.",
        "The Administration's press office first calls the pages incomplete, which is true, and then out of context, which "
        "convinces nobody. Officials named in the columns telephone their ministers. Editors in Vakia and Farnlands ask what "
        "else the volumes contain about their districts. Inside the ministries, the clerks who compiled the ledger find "
        "themselves interviewed by security officers about who had access to which drawer.",
        "There are two ways out. The cabinet can confirm the pages, release the rest of the inventory and take the damage in "
        "one blow, hoping that candour now buys patience later. Or it can hunt for the source of the leak, say nothing more "
        "about the contents and wait for the papers to find another story. The second course is quieter, and the clerks will "
        "remember how they were treated.",
    ), (
        Option('Confirm the pages and release the rest.', (Stability(0.02), PP(-20))),
        Option('Find the leak and say nothing more.', (PP(10), Stability(-0.03))),
    ), picture=0),
    EventDef('lowland_wells', 'Three Fields, One Plain', (
        "The seismic crews finish their last lines across the Farnlands plain in the autumn and send their tapes to the "
        "capital for processing. For the first time the government can lay the three lowland fields side by side: South "
        "Gangel beside the FATO frontier, Farnlands near the Nordlandic one, and the field under the plains around Mankovce. "
        "Each holds roughly a third of the country's crude.",
        "The maps also show how badly the fields have been worked. Wells were drilled where the land was cheap rather than "
        "where the oil was thickest. Neighbouring operators pump from the same pocket and race each other to drain it. Water "
        "is creeping into the oldest wells at Farnlands, and the gathering roads in South Gangel close every spring. Much of "
        "what the surveyors need to know is in the drilling logs that private operators have kept for themselves.",
        "The survey board asks the cabinet for one ruling before it writes its report. The logs could be bought from the "
        "operators at a fair price, which costs money and admits that the drillers own what they recorded. Or the "
        "Administration can order the logs handed over as a condition of every licence, which is faster, cheaper and certain "
        "to start a quarrel with the people who actually run the wells.",
    ), (
        Option('Pay the operators for their logs.', (PP(-15), Research('excavation_tech', 0.5, 1))),
        Option('Order the logs handed over.', (PP(10), Stability(-0.02))),
    ), picture=1),
    EventDef('vakia_galleries', 'What the Galleries Hold', (
        "The inspectors come down from the Vakia mountains after a summer underground with a register that runs to several "
        "thousand entries. Tungsten and chromium leave the district in sacks, lorries and rail wagons from dozens of "
        "workings, large and small, cut into hillsides above the forests and the dry valleys near the coast. The ore is "
        "the richest in the country; the record of who may dig it is the poorest.",
        "Roughly one gallery in five has no papers at all. Some are worked by families who have dug the same seam for "
        "generations and never thought to register it. Others were opened by contractors who vanished after the first "
        "good year and left their crews to carry on alone. The inspectors also found flooded workings with miners still "
        "inside them on the day of the visit, and timbering that no engineer would sign.",
        "The ministry must now decide who owns the unpapered seams. Registering them to the crews who work them would settle "
        "the mountains, keep production steady and cost the treasury the fees it might have charged. Auctioning them to the "
        "highest bidder would raise money at once and bring in companies with capital for pumps and timber, and it would put "
        "a great many Vakia families out of the only work they have.",
    ), (
        Option('Register the seams to the crews who work them.', (Stability(0.03), PP(-15))),
        Option('Auction the unpapered seams.', (PP(25), Stability(-0.02))),
    ), picture=1),
    EventDef('armour_question', 'A Paper on Six Divisions', (
        "The general staff delivers its paper on the armour as ordered, forty pages long, and the defence committee reads it "
        "in a single sitting. Wielvakia keeps six tank divisions, four of infantry and four motorised, with some three "
        "hundred modern tanks in the parks and a doctrine built around firepower. Few countries of its size carry so heavy an "
        "armoured share, and the paper does not pretend otherwise.",
        "Its argument is plain. Between the FATO crossings and the Gebet line the Low Lands are open plain, ideal ground for "
        "tanks and poor ground for anything else, and the country's oil, arms halls and capital all sit on that plain. The "
        "armour exists, the staff writes, so that no neighbour can ever think the plain is cheap to take. What the paper does "
        "not settle is how much fuel, ammunition and training that deterrent needs to be real rather than decorative.",
        "The committee must answer with money. Funding the training the paper asks for means pumping lowland crude into tank "
        "engines rather than into export tankers, and it means crews in the field for weeks every year. Sending the paper "
        "back for a cheaper answer keeps the treasury calm and the parks full, and leaves the divisions looking stronger on "
        "parade than they would be in a crisis.",
    ), (
        Option('Fund the training the paper asks for.', (XP('army', 15), PP(-15))),
        Option('Ask the staff for a cheaper answer.', (PP(20), XP('army', 5))),
    ), picture=0),
    EventDef('four_frontiers', 'Four Frontiers on One Desk', (
        "For the first time, the customs records of every Wielvakian crossing lie on the same desk in Mankovce. There are four "
        "frontiers and four ways of doing things. Toward FATO the posts at the Gangl crossings run long queues and short "
        "tempers. Toward Gebet the traffic is local, farmers and market vans. Toward Ratio the trains stop to change crews. "
        "Toward Nordlands the roads climb into the mountains and the harbours are small.",
        "The review finds that each frontier has grown its own habits. Forms differ from post to post, hours are set by "
        "whoever commands the station, and complaints from the other side are answered by letter weeks later or not at all. "
        "South Gangel is the delicate case. FATO maintains a claim to the district, and every delay or rough inspection there "
        "is read on both sides as a statement of some kind.",
        "The frontier directorate can only reform one frontier properly at a time. Starting with the FATO crossings would "
        "address the busiest and most sensitive posts first, at the risk of making a neighbour wonder why it was singled out. "
        "Starting with the quieter frontiers would build procedures where nothing is contentious and carry them to South "
        "Gangel once they have been tested.",
    ), (
        Option('Begin with the FATO crossings.', (WarSupport(0.02), Stability(0.01))),
        Option('Begin with the quieter frontiers.', (Stability(0.02), PP(10))),
    ), picture=2),
    EventDef('vakia_harbours', 'A Fleet of Three Hulls', (
        "The naval review opens on the quay of the larger Vakia harbour with the whole fleet in view: two destroyers and one "
        "submarine, all three alongside at once because there is fuel and crew for only one of them to sail on any given day. "
        "Behind them stand three slipways, a dry dock that needs new gates and a smaller harbour along the coast with a "
        "single pier.",
        "The admirals argue that the coast is the country's only door to the sea and that ore ships, and one day oil tankers, "
        "will use it whatever the navy can do. The army notes that the fleet costs as much each year as an armoured brigade "
        "and has never fired a shot in anger. The treasury asks whether a coast this short needs a fleet at all, or only a "
        "coast guard with good radios.",
        "The first question is a practical one. Keeping both destroyers in commission means two crews at sea in turns, real "
        "training and an empty fuel line in the budget. Laying one up in reserve frees money and lets its crew train ashore "
        "on the slipways and the radar, but a destroyer tied to the quay for a few years rarely sails again without a costly "
        "refit.",
    ), (
        Option('Keep both destroyers at sea.', (XP('navy', 15), PP(-10))),
        Option('Lay one up and train its crew ashore.', (PP(15), XP('navy', 5))),
    ), picture=2),
    EventDef('two_fields', 'Sixty Aircraft, Two Runways', (
        "The air arm's planners spread their maps across the briefing room at the capital field. Wielvakia flies forty-eight "
        "fighters and twelve ground attack aircraft from two main bases, the capital's and the Vakia coast's, with a grass "
        "strip in South Gangel and nothing at all in Farnlands. Pilots log fewer hours a year than their instructors did, and "
        "spares are drawn from one shared store.",
        "Each service wants the air arm for itself. The army wants fighters over the tank divisions on the plain, where any "
        "war on the Low Lands would be decided. The navy wants patrols over the coast and the harbour approaches. The "
        "civil defence office wants the capital covered first, because one raid on Mankovce would do more damage than any "
        "number of raids on fields and harbours.",
        "Sixty aircraft cannot do all three. The planners need a first priority to build the next years around: where the "
        "radar goes first, where the shelters are dug, which squadrons train for which mission. The others will get what is "
        "left over, and every service chief in the room knows that what is left over in an air arm this size is not very much.",
    ), (
        Option('Cover the capital first.', (XP('air', 10), Stability(0.01))),
        Option('Cover the tank divisions first.', (XP('air', 10), WarSupport(0.02))),
        Option('Cover the coast first.', (XP('air', 10), XP('navy', 5))),
    ), picture=0),
    EventDef('gebet_war', 'War Beyond the Gebet Frontier', (
        "The first wire reports reach the situation room under the capital before dawn: Belka has gone to war. Gebet, which "
        "shares a frontier with Belka on one side and with South Gangel and Alaoboa on the other, is a neighbour whose "
        "traders and day workers cross into Wielvakia every morning. Within hours, the telephones at the frontier posts are "
        "ringing with questions nobody can answer.",
        "Wielvakia is not a party to the war, and the government says so in its first statement. But the frontier commands "
        "are on alert, the reservists of the South Gangel garrisons are checking their call-up papers, and the oil terminals "
        "on the plain are suddenly worth guarding. Shopkeepers in the frontier towns report queues for flour, candles and "
        "batteries. The armoured divisions, built for exactly this ground, sit in their parks waiting for orders.",
        "The cabinet's first decision concerns the frontier towns. Preparing them now for families who may cross, with halls, "
        "kitchens and registration desks, would cost money and might itself suggest that the government expects the worst. "
        "Leaving the towns as they are keeps the country calm for the moment, and leaves the mayors to improvise if the war "
        "comes closer to the frontier than anyone hopes.",
    ), (
        Option('Prepare the frontier towns for arrivals.', (Event('frontier_arrivals', 10), Stability(-0.01))),
        Option('Leave the towns as they are for now.', (WarSupport(0.02), Stability(0.01))),
    ), picture=2),
    EventDef('frontier_arrivals', 'The First Arrivals at South Gangel', (
        "Ten days after the halls were readied, the first families from Gebet arrive at the South Gangel crossings by bus, "
        "car and farm cart. Most of them have relatives in Wielvakia and expect to stay for weeks rather than years. They "
        "bring their papers, their savings and stories of roads closed by soldiers, and the frontier police register them at "
        "trestle tables set up in the customs sheds.",
        "The numbers are manageable for now. The difficulty is everything around them. The reception halls are school gyms "
        "whose pupils have nowhere else to go, the district hospital is already short of beds, and local landlords have "
        "doubled their rents overnight. A few lowland politicians complain that Wielvakia is taking on a burden that belongs to "
        "richer countries further from the war.",
        "The district governor asks the capital for a ruling. The arrivals could stay in South Gangel, close to the frontier "
        "and their own homes, housed in halls and spare rooms at public expense. Or they could be moved on to camps on the "
        "edge of the capital, where services are better and the frontier district can return to normal, at the cost of "
        "sending frightened families further from everything they know.",
    ), (
        Option('Keep them in the South Gangel halls.', (Stability(-0.02), PP(15))),
        Option('Move them on to camps near the capital.', (Stability(0.01), PP(-10))),
    ), picture=2),
    EventDef('ulysses_mankovce', 'Mankovce Hears the Asteroid News', (
        "The evening radio carries the FCU President's broadcast into every kitchen in Mankovce: Ulysses is on a collision "
        "course, and a defence against it is being prepared. What the broadcast cannot tell anyone is which countries lie "
        "under the debris. Wielvakia has no telescope of its own to consult, and by the next morning the capital's hardware "
        "shops have sold out of shovels, candles and tinned food.",
        "The civil defence commission meets the same week and discovers how little it has to work with. The capital has no "
        "public shelters worth the name. The lowland towns sit on open plain with nothing to hide under, while the old mine "
        "galleries of Vakia are the deepest holes in the country and belong to private owners. Railway timetables assume that "
        "nobody ever needs to leave a city all at once.",
        "Before it can weigh shelters against evacuation, the commission has a smaller crisis on its desk. Shopkeepers have "
        "doubled their prices on torches, water cans and tinned meat, and the queues outside are growing angrier by the day. "
        "Capping those prices and rationing the scarcest goods would calm the queues, empty the shelves faster and leave the "
        "ministry to find new supplies. Leaving the shops alone lets high prices pull fresh stock in from abroad, at the cost "
        "of a capital convinced that its merchants are profiting from fear.",
    ), (
        Option('Cap prices and ration the scarcest goods.', (Stability(0.02), PP(-10))),
        Option('Let high prices bring in new stock.', (PP(15), Stability(-0.02))),
    ), picture=1),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('admin', 'The Executive Office', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_inventory', 'Inventory of the Executive Office',
          "The National Administration governs from Mankovce as a single executive office, with no ballot on the calendar since "
          "the vote dated January 1991. Before anyone argues about its future, its own clerks list every power it uses, every "
          "decree still in force and every post it fills. The work takes months and embarrasses several ministries.",
          ('document', 'command'), reward=(Idea('office_inventory'), Event('executive_ledger'))),
    Focus('adm_payroll', 'Print the Payroll of the State',
          "The inventory showed that nobody outside the office knows how many people the state employs or what they are paid. "
          "Printing the payroll of every ministry, district office and state company invites ridicule and a few resignations. "
          "It also makes it harder for any later government, whatever its colour, to hide its friends on the books.",
          ('scales', 'document'), after=('adm_inventory',), reward=(Flag('payroll_printed'), Stability(-0.02))),
    Focus('adm_state_councils', 'Advisory Councils in Four States',
          "Alaoboa, Vakia, Farnlands and South Gangel each receive an advisory council of mayors, employers and union delegates "
          "that meets every quarter and may question the state governor in public. The councils have no budget and no veto. "
          "They give regional grievances a room other than the street, and they warn the capital of trouble early.",
          ('assembly', 'civil'), after=('adm_inventory',), reward=(TimedIdea('state_councils', 730),)),
    Focus('adm_chamber', 'Return to a Chamber of Deputies',
          "Three Wielvakians in ten already back the democratic camp. Its leaders propose a chamber elected from the four "
          "states, a cabinet answerable to it and polling on a fixed date. The Administration would surrender its seals within "
          "a year. Officers and lowland industrialists warn that a campaign season would split the country along regional lines.",
          ('ballot', 'assembly'), after_any=('adm_payroll', 'adm_state_councils'), cost=10,
          exclusive=('adm_staff', 'adm_directorate', 'adm_office_stays'),
          reward=(Regime('chamber_cabinet'), SwapIdea('office_inventory', 'chamber_charter'))),
    Focus('adm_staff', 'Seals to the General Staff',
          "In a country where eight people in ten tell pollsters they would back a war, the general staff is the most trusted "
          "institution in the capital. Its senior officers offer to govern as a council until the frontiers are settled, with "
          "ministries reporting to them. Decisions would come quickly. Civilian politics would wait, for years if necessary.",
          ('command', 'security'), after_any=('adm_payroll', 'adm_state_councils'), cost=10,
          exclusive=('adm_chamber', 'adm_directorate', 'adm_office_stays'),
          reward=(Regime('staff_council'), SwapIdea('office_inventory', 'staff_seals'), Flag('rule_staff'))),
    Focus('adm_directorate', 'A Wielvakian State Directorate',
          "The nationalist camp is small, about one voter in eight, but loud in South Gangel, where FATO maintains a claim. It "
          "wants a directorate that governs by decree in the name of the nation and treats every frontier as a grievance. It "
          "promises discipline and pride. It would also teach every neighbour to assume the worst of Wielvakia.",
          ('security', 'medal'), after_any=('adm_payroll', 'adm_state_councils'), cost=10,
          exclusive=('adm_chamber', 'adm_staff', 'adm_office_stays'),
          reward=(Regime('state_directorate'), SwapIdea('office_inventory', 'directorate_order'), Flag('rule_directorate'))),
    Focus('adm_office_stays', 'The Executive Office Endures',
          "The majority that keeps the Administration in place wants nothing dramatic. The executive office stays, but under a "
          "written statute fixing its term, its powers and a public review every four years by the state councils. No ballot is "
          "promised. Reformers call it a polite postponement; administrators call it the first rulebook the office has had.",
          ('document', 'scales'), after_any=('adm_payroll', 'adm_state_councils'), cost=10,
          exclusive=('adm_chamber', 'adm_staff', 'adm_directorate'),
          reward=(SwapIdea('office_inventory', 'office_statute'), PP(25))),
    Focus('adm_polling_day', 'Polling Day in Four States',
          "The chamber's first election runs on one day across Alaoboa, Vakia, Farnlands and South Gangel, counted in public "
          "halls before observers from every party. Turnout is high in the capital and lower in the lowland towns. Losing "
          "candidates complain of boundaries drawn in a hurry, and the winners must now govern beside an opposition that can "
          "vote them out.",
          ('ballot', 'civil'), after=('adm_chamber',), reward=(SwapIdea('chamber_charter', 'elected_chamber'), Stability(0.02))),
    Focus('adm_staff_budget', 'A Budget Drafted at Headquarters',
          "Under the staff council the national budget is drafted by the officers who plan the army's year, with every ministry "
          "request ranked against readiness. Spending becomes predictable and the arms halls receive their orders early. "
          "Schools, clinics and the state councils learn that a well argued request still comes second to fuel and spares.",
          ('command', 'economy'), after=('adm_staff',), reward=(SwapIdea('staff_seals', 'staff_budget'),)),
    Focus('adm_leagues', 'The Directorate Youth Leagues',
          "The directorate organises the young into leagues with uniforms, summer camps in the Vakia hills and evening drill "
          "in the lowland towns. Membership is voluntary on paper and expected in practice. The leagues carry the directorate's "
          "message and feed the army keen recruits, while parents who keep their children home find their permits delayed.",
          ('training', 'medal'), after=('adm_directorate',),
          reward=(SwapIdea('directorate_order', 'directorate_leagues'), WarSupport(0.03))),
    Focus('adm_four_year_review', 'The Four-Year Review',
          "The statute's first review arrives, and the councils of the four states sit together for a week to question the "
          "executive office in public. They cannot dismiss it, but their report is printed and argued over in every newspaper. "
          "Ministers who fail the review are moved quietly. The office learns that a rulebook also produces a scorecard.",
          ('scales', 'assembly'), after=('adm_office_stays',), reward=(SwapIdea('office_statute', 'reviewed_office'), PP(20))),
    Focus('adm_examinations', 'Written Tests for Every Clerk',
          "With the payroll in print, posts filled by family and favour can no longer be denied. Every new entrant to the civil "
          "service now sits a written examination marked by a board that includes outsiders. Patronage networks in every party "
          "lose their easiest currency, and recruitment slows for two years while the boards learn their trade.",
          ('document', 'training'), after_any=('adm_polling_day', 'adm_staff_budget', 'adm_leagues', 'adm_four_year_review'),
          requires=(HasFlag('payroll_printed'),), reward=(Idea('service_examinations'),)),
    Focus('adm_compact', 'A Compact of the Four States',
          "Whatever government sits in Mankovce, the four states sign a short compact fixing their shares of oil revenue, the "
          "seats of state offices and the language of the courts. Vakia, the only coast, wins a guaranteed harbour budget. The "
          "compact settles nothing grand, but it stops every budget year from reopening what the country owes each region.",
          ('peace', 'assembly'), after_any=('adm_polling_day', 'adm_staff_budget', 'adm_leagues', 'adm_four_year_review'),
          reward=(Flag('states_compact'), Stability(0.03))),
))

OIL = Branch('oil', 'Oil of the Low Lands', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('oil_survey', 'Survey the Three Lowland Fields',
          "Wielvakia pumps oil from three fields of roughly equal size, under South Gangel, Farnlands and the plains around the "
          "capital, and no one has measured their reserves with modern methods. Seismic crews and core samples tell the "
          "government what it owns before it decides who should pump it. The survey costs a season and some goodwill.",
          ('economy', 'tools'), reward=(Idea('field_survey'), Event('lowland_wells'))),
    Focus('oil_gathering_lines', 'Gathering Lines in Farnlands',
          "Farnlands wells still send crude to the railhead by tanker truck over farm roads that break up every spring. Buried "
          "gathering lines and a hard road to the Nadomlin railhead cut the truck traffic in half. Farmers object to trenches "
          "across their fields, and the compensation bill is larger than the engineers first estimated.",
          ('logistics', 'tools'), after=('oil_survey',), reward=(Build('infrastructure', 1, 326),)),
    Focus('oil_gangel_roads', 'Hard Roads for South Gangel Wells',
          "The South Gangel field lies beside the FATO frontier, and its access roads were laid for carts. Paving them, adding "
          "bridges strong enough for drilling rigs and lighting the junctions makes the field workable all year. It also makes "
          "the frontier district easier for anyone to reach, which the border police note in their monthly report.",
          ('logistics', 'gate'), after=('oil_survey',), reward=(Build('infrastructure', 1, 325),)),
    Focus('oil_state_company', 'A Single State Oil Company',
          "One school wants all three fields placed under a single state company that drills, pipes, refines and sells, with "
          "its profits paid straight into the budget. It would plan the fields as one system and keep foreign firms out. It "
          "would also become the largest employer in the country, and every government would treat it as a purse.",
          ('command', 'economy'), after_any=('oil_gathering_lines', 'oil_gangel_roads'), cost=10, exclusive=('oil_concessions',),
          reward=(SwapIdea('field_survey', 'national_oil_company'),)),
    Focus('oil_concessions', 'Auction the Lowland Blocks',
          "The rival school wants the fields divided into blocks and auctioned to private drillers, domestic or foreign, who pay "
          "royalties and tax on every barrel. Investment would arrive faster than any budget could supply it. The state would "
          "lose control of how fast the fields are drained, and high bidders may cut corners on safety and wages.",
          ('economy', 'diplomacy'), after_any=('oil_gathering_lines', 'oil_gangel_roads'), cost=10, exclusive=('oil_state_company',),
          reward=(SwapIdea('field_survey', 'lowland_concessions'),)),
    Focus('oil_capital_refinery', 'A Refinery Beside the Capital',
          "The state company's first large project is a refinery on the edge of the capital, fed by pipe from all three fields "
          "and sized for the whole country's fuel. Wielvakia stops shipping crude abroad and buying petrol back. The plant takes "
          "the last open industrial plot in Alaoboa, and the nearest suburb learns what a refinery smells like.",
          ('industry', 'economy'), after=('oil_state_company',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('oil_tank_farms', 'Tank Farms in the Capital Hills',
          "The capital's fuel silo is topped up and new tank farms are dug into the hills beside the city, holding enough fuel "
          "for the army and essential services for a season. Fuel bought for storage earns nothing and ages slowly. If the "
          "region's wars ever close the roads and sea lanes, the country will not run dry within a month.",
          ('shelter', 'economy'), after=('oil_state_company',), reward=(Flag('fuel_reserve_held'), PP(-15))),
    Focus('oil_licence_code', 'Safety Terms for Every Licence',
          "Drillers who won the auctions are now bound by one code covering safety, wages and the sealing of spent wells, "
          "enforced by inspectors paid from a levy on every barrel. The worst operators threaten to leave, and one does. The "
          "rest accept the code once they see that the inspectors also stop rivals from undercutting them with reckless crews.",
          ('scales', 'tools'), after=('oil_concessions',), reward=(SwapIdea('lowland_concessions', 'regulated_concessions'),)),
    Focus('oil_ring_road', 'A Ring Road for the Tankers',
          "Private drillers sell crude to whoever pays best, and most of it leaves by tanker truck through the capital's "
          "streets. A ring road around Mankovce, paid for from the concession levy, keeps the tankers out of the centre and "
          "speeds every other kind of freight. Residents welcome the quiet; shops on the old route lose their passing trade.",
          ('logistics', 'rail'), after=('oil_concessions',), reward=(Build('infrastructure', 1, 367),)),
    Focus('oil_trunk_pipeline', 'The Trunk Pipeline to Vakia',
          "Lowland oil has only one way to the sea, across the mountains to the Vakia harbours. A trunk pipeline through the "
          "passes, with pumping stations and a tank farm at the port, lets Wielvakia load tankers instead of trains. The "
          "mountain route is costly to build and to guard, and the Nordlandic coast nearby will watch the tankers sail.",
          ('logistics', 'navy'), after_any=('oil_capital_refinery', 'oil_tank_farms', 'oil_licence_code', 'oil_ring_road'),
          reward=(Build('infrastructure', 1, 372), Research('logistics_tech', 0.5, 1))),
    Focus('oil_barrel_fund', 'An Oil Revenue Fund',
          "Oil money has always gone straight into the year's budget, rising and falling with the price. With the compact of "
          "the four states fixing each region's share, a revenue fund now takes a set portion of every barrel, invests it and "
          "pays out a steady sum each year. Ministers lose a pot they liked to spend, and the country gains a cushion against "
          "the day crude collapses.",
          ('scales', 'economy'), after_any=('oil_capital_refinery', 'oil_tank_farms', 'oil_licence_code', 'oil_ring_road'),
          requires=(HasFlag('states_compact'),), reward=(Idea('oil_revenue_fund'), PP(-20))),
))

ORE = Branch('ore', 'Tungsten and Chromium of Vakia', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('ore_gallery_count', 'Count the Vakia Mine Galleries',
          "Most of the country's tungsten and chromium comes from galleries cut into the Vakia mountains above the forests and "
          "dry valleys of the coast. Inspectors walk every gallery, record what is worked and what has flooded, and map who "
          "owns which seam. Several owners have no papers at all, and the count must decide what to do about them.",
          ('tools', 'document'), reward=(Idea('mine_registry'), Event('vakia_galleries'))),
    Focus('ore_winter_roads', 'Mine Roads Through the Passes',
          "Ore leaves the Vakia galleries by mule track and narrow lorry roads that close every winter. Graded roads with "
          "retaining walls and avalanche sheds keep the mines working through the cold months. Road crews are scarce, and the "
          "work takes them off every other project in Vakia for two seasons. Mining towns see their first winter wages.",
          ('logistics', 'tools'), after=('ore_gallery_count',), reward=(Build('infrastructure', 1, 372),)),
    Focus('ore_assay_laboratory', 'An Assay Laboratory at Mankovce',
          "Foreign ore buyers set the price by their own assays, and Wielvakian sellers have no means to argue. A national "
          "assay laboratory in the capital tests every shipment and publishes grades that buyers must accept or dispute in "
          "writing. It needs chemists the country barely has, and within a year it pays for itself in better prices.",
          ('science', 'tools'), after=('ore_gallery_count',),
          reward=(Research('excavation_tech', 0.5, 1), Flag('assay_lab_open'))),
    Focus('ore_raw_sales', 'Sell the Ore as It Comes',
          "The simplest policy sells tungsten and chromium concentrate to foreign smelters on long contracts, at the best "
          "price the assay laboratory can defend. Money arrives quickly and the mines expand. The country stays a quarry for "
          "other people's alloy works, and if wars drive prices up, Wielvakia will have sold its future output cheaply.",
          ('economy', 'diplomacy'), after_any=('ore_winter_roads', 'ore_assay_laboratory'), cost=10, exclusive=('ore_home_alloys',),
          reward=(SwapIdea('mine_registry', 'ore_contracts'),)),
    Focus('ore_home_alloys', 'Keep the Ore for Wielvakian Steel',
          "The other policy restricts concentrate exports and directs the ore to domestic mills, where it hardens armour plate, "
          "gun barrels and machine tools. The arms halls gain a supply no foreign buyer can outbid. Mine owners lose their best "
          "customers and say so loudly, and the mills must learn alloy work they have never done at scale.",
          ('industry', 'security'), after_any=('ore_winter_roads', 'ore_assay_laboratory'), cost=10, exclusive=('ore_raw_sales',),
          reward=(SwapIdea('mine_registry', 'alloy_reserve'),)),
    Focus('ore_ten_year_terms', 'Ten-Year Ore Contracts',
          "Foreign smelters offer ten-year contracts at fixed prices in exchange for guaranteed tonnage. The treasury can plan "
          "around the revenue and the mines can borrow against it. If prices rise the buyers win; if they fall Wielvakia does. "
          "Negotiators hold out for a review clause every three years, which costs a long winter of talks.",
          ('document', 'economy'), after=('ore_raw_sales',), reward=(SwapIdea('ore_contracts', 'long_ore_contracts'),)),
    Focus('ore_armour_plate', 'Armour Plate from Lowland Mills',
          "Lowland steel and Vakia chromium meet in the capital's mills, which roll their first armour plate of domestic alloy. "
          "The plate is heavier and slower to make than imported grades, and the first batches fail their tests. By the third "
          "year the tank workshops stop ordering plate from abroad and the repair yards stop waiting on foreign ships.",
          ('industry', 'tools'), after=('ore_home_alloys',), reward=(SwapIdea('alloy_reserve', 'plate_mills'),)),
    Focus('ore_carbide_tools', 'Hard Alloys for Machine Tools',
          "Tungsten carbide tips and chromium tool steels make every lathe and drill in the country faster and longer lived. "
          "Working from the assay laboratory's samples, a small team learns to sinter carbide inserts for domestic workshops. "
          "It is fiddly, costly work with a high reject rate, and every insert made at home is one fewer to import.",
          ('tools', 'science'), after_any=('ore_ten_year_terms', 'ore_armour_plate'), requires=(HasFlag('assay_lab_open'),),
          reward=(Research('industry', 0.75, 1), XP('army', 5))),
    Focus('ore_rescue_stations', 'Rescue Stations in the Galleries',
          "Gallery collapses kill Vakia miners every year, and the nearest rescue team is often a day away. Stations with "
          "breathing sets, trained crews and telephone lines to each mine cut that to an hour. Owners must pay a levy for the "
          "stations and many resent it. Miners' families, who have buried too many, notice who paid and who argued.",
          ('medical', 'shelter'), after=('ore_winter_roads',), reward=(Idea('mine_rescue'),)),
    Focus('ore_mining_school', 'A Mining School in Vakia',
          "Vakia supplies the ore while the capital keeps the engineers. A school in the mining district trains assayers, mine "
          "surveyors and furnace hands where the work is, with places reserved for miners' children. Teachers have to be lured "
          "from the capital with housing and bonuses. In time the district's best graduates need not leave home for skilled work.",
          ('training', 'science'), after_any=('ore_ten_year_terms', 'ore_armour_plate', 'ore_rescue_stations'),
          reward=(Idea('metallurgy_school'),)),
))

ARMOUR = Branch('armour', 'Six Tank Divisions', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('arm_armour_paper', 'Why Six Tank Divisions',
          "Wielvakia fields six tank divisions beside four of infantry and four motorised, an armoured share few neighbours can "
          "match. The tanks burn lowland fuel, wear out lowland roads and absorb most of the army budget. Before another hull is "
          "bought, the general staff must explain in writing what the armour is for and where it would fight.",
          ('command', 'document'), reward=(Idea('armour_first'), Event('armour_question'))),
    Focus('arm_farnlands_range', 'A Tank Range on the Farnlands Plain',
          "Tank crews have trained on cramped grounds where a battalion cannot deploy. A large range on the open Farnlands "
          "plain, with tank roads, firing lanes and a repair camp, lets whole battalions manoeuvre and shoot together. Farmers "
          "who lease the land are paid well and still object to the noise, the dust and the ruts in their tracks.",
          ('training', 'security'), after=('arm_armour_paper',), reward=(Build('infrastructure', 1, 326), XP('army', 10))),
    Focus('arm_fuel_allowance', 'Fuel Allowance for Every Crew',
          "Crews that never drive cannot fight, and Wielvakian tank crews have been rationed to a few days in the field each "
          "year to save fuel. The army now guarantees every crew a fixed training allowance, drawn from the lowland wells "
          "before any crude is exported. The oil budget feels the difference at once; the divisions feel it within a season.",
          ('logistics', 'training'), after=('arm_armour_paper',), reward=(TimedIdea('fuel_allowance', 730),)),
    Focus('arm_massed', 'Mass the Armour on the Low Lands',
          "The armoured school wants all six tank divisions held together on the lowland plain, where the ground suits them and "
          "the fuel is close. An intruder from any frontier would meet a single armoured fist within two days. The doctrine is "
          "simple and powerful, and it leaves Vakia and its mountain passes to the infantry and to hope.",
          ('command', 'gate'), after_any=('arm_farnlands_range', 'arm_fuel_allowance'), cost=10,
          exclusive=('arm_passes', 'arm_motor_brigades'), reward=(SwapIdea('armour_first', 'massed_armour'),)),
    Focus('arm_passes', 'Hold the Passes, Keep a Reserve',
          "The mountain school points out that the Vakia passes carry the main routes from the Ratian and Nordlandic frontiers "
          "to the coast. It wants infantry and mountain troops dug into those passes, with the tanks held back as a central "
          "reserve rather than a striking force. Fewer tanks would need fuel, and the savings could go into exports.",
          ('security', 'training'), after_any=('arm_farnlands_range', 'arm_fuel_allowance'), cost=10,
          exclusive=('arm_massed', 'arm_motor_brigades'), reward=(SwapIdea('armour_first', 'pass_defence'),)),
    Focus('arm_motor_brigades', 'Motor Brigades over Tank Divisions',
          "A third group of officers wants to break the heavy divisions into smaller mechanised brigades mixing tanks, infantry "
          "carriers and guns, able to move on lowland roads and fight in mountain valleys alike. Each brigade would be weaker "
          "alone and quicker everywhere. The reform would take years, and the tank generals see it as an attack on their branch.",
          ('logistics', 'command'), after_any=('arm_farnlands_range', 'arm_fuel_allowance'), cost=10,
          exclusive=('arm_massed', 'arm_passes'), reward=(SwapIdea('armour_first', 'motor_brigades'),)),
    Focus('arm_railhead_parks', 'Repair Parks at the Railheads',
          "Six divisions massed together need workshops close behind them. Repair parks at the lowland railheads can change an "
          "engine overnight and rebuild a gearbox in a day. The parks draw skilled fitters away from civilian garages that pay "
          "better. With them, the armoured fist can stay in the field for longer than a single week.",
          ('tools', 'command'), after=('arm_massed',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('arm_pass_works', 'Fieldworks in the Vakia Passes',
          "Holding the passes needs more than infantry on hillsides. Engineers cut covered positions, ammunition stores and "
          "lateral roads along the main routes from the frontiers to the coast, so defenders can shift between valleys unseen. "
          "The work scars several mountain parks, and the army posts sentries where hikers once picnicked.",
          ('security', 'gate'), after=('arm_passes',), reward=(Build('infrastructure', 1, 372), XP('army', 5))),
    Focus('arm_valley_trials', 'Brigade Trials in the Valleys',
          "The first two mixed brigades spend a year on trial, driving from the Farnlands plain into the Vakia valleys and back "
          "on public roads. Umpires mark every mistake, and the reports are blunt. Several of the tank generals' objections turn "
          "out to be right. The trials cost fuel and pride, and they show what the brigades must still learn.",
          ('training', 'logistics'), after=('arm_motor_brigades',), reward=(TimedIdea('brigade_trials', 730),)),
    Focus('arm_call_up', 'A Register of Former Conscripts',
          "Limited conscription produces a modest intake, but everyone who has served is still on paper somewhere, scattered "
          "across district offices. A single call-up register lists them by skill, district and last unit, updated each year. "
          "Mobilisation that took weeks now takes days, and civil liberties groups dislike a state that knows so much.",
          ('document', 'security'), after_any=('arm_railhead_parks', 'arm_pass_works', 'arm_valley_trials'), cost=10,
          exclusive=('arm_career_crews',), reward=(Idea('call_up_register'),)),
    Focus('arm_career_crews', 'Long-Service Tank Crews',
          "The alternative spends the money on fewer, better soldiers: tank crews signed for long terms on career pay, with "
          "housing and technical courses, who keep the same vehicle for years. Their gunnery and maintenance improve beyond "
          "anything a conscript achieves. The wage bill climbs every year, and the reserve behind them stays thin.",
          ('medal', 'training'), after_any=('arm_railhead_parks', 'arm_pass_works', 'arm_valley_trials'), cost=10,
          exclusive=('arm_call_up',), reward=(Idea('career_crews'),)),
    Focus('arm_mobilisation_tables', 'Mobilisation Tables at Headquarters',
          "Under the staff council, headquarters writes mobilisation tables for every reservist, train and fuel truck in the "
          "country and rehearses them twice a year on the lowland railways. Civil traffic stops for a day each time. The tables "
          "turn a small army with large stores into one that is ready in days, and ministries resent the short notice.",
          ('command', 'rail'), after=('arm_armour_paper',), requires=(HasFlag('rule_staff'),), reward=(Idea('mobilisation_tables'),)),
))

FRONTIERS = Branch('frontiers', 'Four Frontiers', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('bord_frontier_review', 'Four Neighbours, Four Rulebooks',
          "Wielvakia touches FATO, Gebet, Ratio and Nordlands, and each frontier runs by its own forms, hours and habits. "
          "Officers at the Gangl crossings never speak to colleagues on the Nordlandic side. A frontier review gathers every "
          "post's records in Mankovce to learn what crosses, where and how often. Several posts turn out to keep no records.",
          ('gate', 'document'), reward=(Idea('frontier_review'), Event('four_frontiers'))),
    Focus('bord_gangel_brief', 'A Legal Brief on South Gangel',
          "FATO maintains a claim to South Gangel, and when Belka sells its northern lands to FATO in late August 1991 the "
          "neighbour across the Gangl crossings grows larger overnight. The foreign ministry prepares a brief on the claim and "
          "the treaties behind the frontier. It moves no line on any map, but the government will not be caught unprepared.",
          ('scales', 'security'), after=('bord_frontier_review',), requires=(After('1991.8.29'),),
          reward=(Flag('gangel_brief'), Tooltip('No claim, core or border changes; the brief sets out the Wielvakian legal position only.'))),
    Focus('bord_northern_hours', 'Common Hours at the Northern Posts',
          "The crossings from Farnlands and Vakia into Nordlands carry light traffic over mountain roads and through small "
          "harbours. Wielvakian officers there now keep posted hours, use bilingual forms and staff a telephone line for their "
          "Nordlandic counterparts, whatever Nordlands arranges on its own side. Smugglers who relied on confusion notice first.",
          ('diplomacy', 'document'), after=('bord_frontier_review',), reward=(TimedIdea('northern_posts', 730),)),
    Focus('bord_centrum_trains', 'Through Trains into Ratio',
          "Lines from the capital and the Vakia mountains run into Ratio at Centrum and the Troton Mountains, but every train "
          "stops at the frontier to change crews and papers. Through running with shared signalling and joint inspection would "
          "halve the waits. Rail unions fear for their jobs, and the scheme needs Ratian agreement Wielvakia cannot command.",
          ('rail', 'gate'), after=('bord_frontier_review',),
          reward=(TimedIdea('ratian_rail', 730), Research('train_tech', 0.5, 1))),
    Focus('bord_gebet_liaison', 'Liaison Posts on the Gebet Frontier',
          "Gebet, independent since 1988, lies across the frontier from South Gangel and Alaoboa and shares its other frontier "
          "with Belka. Liaison posts with radios and a small radar at the South Gangel junction let the two border services "
          "talk and watch the air. Gebetan officials welcome the contact, and both sides know which sky the radar watches.",
          ('communications', 'gate'), after=('bord_frontier_review',), reward=(Build('radar_station', 1, 325),)),
    Focus('bord_open_crossings', 'Open Frontiers, Quick Crossings',
          "With the review complete, one camp wants every crossing open around the clock with inspections by sample only. "
          "Lowland trade with all four neighbours would grow quickly and frontier towns would prosper. Smuggling would grow "
          "too, and the police warn that an open frontier is just as easy to cross in the other direction when times turn bad.",
          ('gate', 'economy'), after_any=('bord_northern_hours', 'bord_centrum_trains', 'bord_gebet_liaison'), cost=10,
          exclusive=('bord_armed_crossings', 'bord_convention'), reward=(SwapIdea('frontier_review', 'open_frontiers'),)),
    Focus('bord_armed_crossings', 'Armed Posts, Closed Nights',
          "The cautious camp wants every crossing staffed by armed customs police and closed between dusk and dawn, with every "
          "vehicle searched. Traders would queue and complain. The state would know what enters the country, which matters more "
          "than cheap imports in a region where land is being sold and borders redrawn.",
          ('security', 'gate'), after_any=('bord_northern_hours', 'bord_centrum_trains', 'bord_gebet_liaison'), cost=10,
          exclusive=('bord_open_crossings', 'bord_convention'), reward=(SwapIdea('frontier_review', 'armed_frontiers'),)),
    Focus('bord_convention', 'Propose a Frontier Convention',
          "A third camp wants Wielvakia to offer all four neighbours one common text on crossing hours, incident reporting and "
          "the return of stray livestock, vehicles and conscripts. Nobody is obliged to sign. The offer costs diplomats' time "
          "and invites polite refusals, but it shows the region a neighbour that prefers paperwork to patrols.",
          ('peace', 'diplomacy'), after_any=('bord_northern_hours', 'bord_centrum_trains', 'bord_gebet_liaison'), cost=10,
          exclusive=('bord_open_crossings', 'bord_armed_crossings'), reward=(SwapIdea('frontier_review', 'convention_proposal'),
          Tooltip('An offer only; it creates no faction, guarantee or alliance and binds no neighbour.'))),
    Focus('bord_transit_lanes', 'Transit Lanes for Lowland Trucks',
          "Open crossings bring more lorries than the South Gangel roads can carry. Dedicated transit lanes with weigh stations, "
          "truck stops and customs clearance at the depot rather than the frontier keep through traffic moving. Hauliers on "
          "both sides save hours, and the district's villages lose the quiet they had before the lorries came.",
          ('logistics', 'economy'), after=('bord_open_crossings',), reward=(Build('infrastructure', 1, 325), PP(10))),
    Focus('bord_guard_corps', 'A Frontier Guard Corps',
          "Armed crossings need patrols between them. A uniformed frontier guard, drawn from former conscripts and trained in "
          "mountain and plain alike, walks the line between posts on all four frontiers. It costs barracks, vehicles and "
          "wages. Neighbours notice the new uniforms and ask, through the proper channels, what they are meant to stop.",
          ('security', 'medal'), after=('bord_armed_crossings',), reward=(SwapIdea('armed_frontiers', 'frontier_guard'), XP('army', 10))),
    Focus('bord_secretariat', 'A Frontier Secretariat at Mankovce',
          "Whatever answers come back, the convention offer leaves behind a small secretariat in the capital that logs every "
          "frontier complaint from any neighbour and replies within a week. It has no power to settle anything. It does make "
          "Wielvakia the easiest neighbour in the region to talk to, which is worth something when tempers run high.",
          ('peace', 'document'), after=('bord_convention',), reward=(SwapIdea('convention_proposal', 'frontier_secretariat'),)),
    Focus('bord_gangel_rallies', 'Rallies in South Gangel',
          "Under the directorate, the movement holds rallies in the South Gangel towns facing the Gangl crossings, with bands, "
          "banners and speeches about the district's place in the nation. The rallies change no claim and no frontier. They "
          "lift the movement's members, worry the district's traders, and are reported in detail across the line.",
          ('ballot', 'security'), after=('bord_gangel_brief',), requires=(HasFlag('rule_directorate'),),
          reward=(WarSupport(0.04), Tooltip('No claim, core or border changes; the rallies are domestic politics only.'))),
))

COAST = Branch('coast', 'The Vakia Coast', 1992, 'FOCUS_FILTER_NAVY_XP', (
    Focus('cst_naval_review', 'Two Harbours and Three Slipways',
          "Wielvakia's only coast runs along Vakia, where two harbours, one large and one small, shelter two destroyers and a "
          "single submarine beside three working slipways. The same coast carries the country's ore and may one day carry its "
          "oil. A naval review asks whether the fleet exists to fight, to escort, or to show a flag the neighbours can see.",
          ('navy', 'document'), reward=(Idea('coast_command'), Event('vakia_harbours'))),
    Focus('cst_cliff_radar', 'Radar Heads on the Vakia Cliffs',
          "Ships bound for the Vakia harbours are seen only when they round the breakwater. Radar heads on the cliffs above "
          "both harbours, feeding a single plot room, track every hull in range and every aircraft low over the water. The "
          "Nordlandic coast is near enough to appear on the screens, which must be explained before the sets are switched on.",
          ('radar', 'navy'), after=('cst_naval_review',), reward=(Build('radar_station', 1, 372),)),
    Focus('cst_slipway_hire', 'Repair Work for the Slipways',
          "Three slipways cannot build a fleet, but they can repair one. The yards bid for overhaul and conversion work on "
          "coasters, ferries and fishing boats of any flag, keeping welders busy between naval orders. Prices must undercut "
          "larger yards elsewhere in the region, and the navy loses priority on the slipways for two years.",
          ('tools', 'navy'), after=('cst_naval_review',), reward=(TimedIdea('slipway_contracts', 730),)),
    Focus('cst_ore_escorts', 'Convoy Escort for the Ore Trade',
          "One school wants the navy organised around the ore ships: the two destroyers escort groups of merchant hulls out of "
          "Vakia and the submarine trains them to spot a shadow. It turns a token fleet into a working one with a clear task. "
          "It also ties the navy to trade routes that the region's wars may close without asking.",
          ('navy', 'logistics'), after_any=('cst_cliff_radar', 'cst_slipway_hire'), cost=10, exclusive=('cst_inshore_boats',),
          reward=(SwapIdea('coast_command', 'ore_convoys'),)),
    Focus('cst_inshore_boats', 'Patrol Boats for the Inshore Waters',
          "The other school wants small, fast patrol boats built at home for the inshore waters and harbour mouths, with the "
          "destroyers kept as a reserve. Boats are cheap, the slipways can build them and conscripts can crew them. They cannot "
          "go far from the coast, which is precisely where this school thinks the navy belongs.",
          ('navy', 'security'), after_any=('cst_cliff_radar', 'cst_slipway_hire'), cost=10, exclusive=('cst_ore_escorts',),
          reward=(SwapIdea('coast_command', 'inshore_patrols'),)),
    Focus('cst_destroyer_refit', 'Refit the Two Destroyers',
          "Escort work demands ships that can stay at sea for a week. Both destroyers go through the dry dock in turn for new "
          "sonar, radios and engine overhauls, and the dock gates are replaced first so the work can happen at all. For a year "
          "only one escort is available, and the ore shippers are told to keep their sailings in step.",
          ('tools', 'logistics'), after=('cst_ore_escorts',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 15))),
    Focus('cst_fishery_patrols', 'Fishery Patrols off Vakia',
          "The first patrol boats go to work on the fishing grounds, checking catches, chasing trawlers that ignore closed "
          "seasons and towing broken boats home in storms. The fishermen grumble about inspections and cheer the rescues. The "
          "crews learn the coast's every rock and current, which is the training no exercise could provide.",
          ('fishing', 'navy'), after=('cst_inshore_boats',), reward=(TimedIdea('fishery_patrols', 1095), XP('navy', 5))),
    Focus('cst_maritime_patrol', 'Maritime Patrol from the Vakia Field',
          "The Vakia airfield is the largest in the country. Longer runways, a maritime patrol hangar and a fuel store let aircraft "
          "watch the sea lanes far beyond the reach of the cliff radar. The navy and the air arm must share one field and one "
          "budget line, and their first joint planning meetings are not friendly ones.",
          ('air', 'navy'), after_any=('cst_destroyer_refit', 'cst_fishery_patrols'), reward=(Build('air_base', 2, 372),)),
    Focus('cst_port_budget', 'A Harbour Budget for Vakia',
          "The compact of the four states guarantees Vakia a harbour budget, and the first instalment arrives. New cranes, "
          "dredging and a rail spur to the quay let the harbours handle ore, crude and general cargo on one site. The "
          "lowland states watch the spending closely, and the port authority prints its accounts to forestall them.",
          ('navy', 'economy'), after=('cst_naval_review',), requires=(HasFlag('states_compact'),), reward=(Idea('vakia_port_fund'),)),
    Focus('cst_naval_school', 'A Naval School at the Main Harbour',
          "Officers have been trained abroad or not at all, and ratings learn their trades on the job. A naval school at the "
          "main Vakia harbour teaches navigation, engineering and gunnery to both, with a small training vessel of its own. The "
          "school is expensive for a fleet of three hulls, and it is the only way the fleet will ever grow.",
          ('training', 'navy'), after_any=('cst_destroyer_refit', 'cst_fishery_patrols'), reward=(Idea('naval_school'),)),
))

AIR = Branch('air', 'Air Arm of the Low Lands', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count', 'Forty-Eight Fighters, Two Main Fields',
          "The air arm flies forty-eight fighters and a dozen ground attack aircraft from two main fields, the capital's and "
          "the Vakia coast's, with a single grass strip in South Gangel. Pilots fly fewer hours than their instructors did. A "
          "review asks what the air arm should protect first: the capital, the armour on the plain, or the coast.",
          ('air', 'runway'), reward=(Idea('air_review'), Event('two_fields'))),
    Focus('air_nadomlin_field', 'A Dispersal Field near Nadomlin',
          "Farnlands has no military airfield, so every aircraft in that part of the country must fly from the capital. A "
          "dispersal field on the plain near Nadomlin, with hardened shelters and fuel from the local wells, gives the air arm "
          "somewhere to scatter in a crisis. It also puts fighters within minutes of the Nordlandic and FATO frontiers.",
          ('runway', 'logistics'), after=('air_count',), reward=(Build('air_base', 2, 326),)),
    Focus('air_gangel_runway', 'Concrete for the South Gangel Strip',
          "South Gangel's grass strip is the Wielvakian field closest to the FATO and Gebet frontiers. With the legal brief on "
          "the FATO claim written, the government lays a concrete runway, taxiways and blast pens there. It is a modest base, "
          "and it says in the plainest language an air force has that the district is defended.",
          ('runway', 'security'), after=('air_count',), requires=(HasFlag('gangel_brief'),), reward=(Build('air_base', 2, 325),)),
    Focus('air_flying_hours', 'Flying Hours Before New Airframes',
          "New aircraft are expensive and slow to arrive; flying hours are neither. The air arm spends its budget on fuel, "
          "spares and instructors so that every pilot flies twice as often, and postpones any purchase of new airframes. The "
          "fleet ages a little faster, and the pilots who fly it become a good deal better at their work.",
          ('training', 'air'), after=('air_count',), reward=(TimedIdea('flying_hours', 730),)),
    Focus('air_army_support', 'Close Support for the Tank Divisions',
          "The dozen ground attack aircraft have never trained with the armour they are meant to support. Joint exercises on "
          "the Farnlands range, forward air controllers in every tank brigade and a shared radio net teach pilots and tank "
          "commanders to speak the same language. Accidents happen, and every exercise is reviewed in detail.",
          ('air', 'command'), after=('air_count',), reward=(Research('air_doctrine', 0.5, 1), XP('air', 10))),
    Focus('air_capital_control', 'A Control Room at the Capital Field',
          "Interception without radar is guesswork. A radar head and an underground control room at the capital field watch "
          "the approaches to Mankovce from every frontier and scramble fighters with minutes to spare. The room needs crews "
          "around the clock and the radar must be explained to four neighbours before it is switched on.",
          ('radar', 'air'), after=('air_flying_hours',), reward=(Build('radar_station', 1, 367),)),
    Focus('air_capital_pens', 'Blast Pens at the Capital Field',
          "The capital's aircraft stand in rows on open aprons, a target that a single raid could destroy. Concrete blast pens, "
          "a second runway and buried fuel lines turn the field into one that can absorb a strike and keep flying. The work "
          "closes the field in turns for a year, and its squadrons lodge at the Vakia field while it lasts.",
          ('shelter', 'runway'), after=('air_capital_control',), reward=(Build('air_base', 2, 367),)),
    Focus('air_hired_aggressors', 'Hire Foreign Aggressor Instructors',
          "By mid 1998 former top pilots of the Belkan Air Force are working abroad as aggressor instructors for whoever pays. "
          "A short contract would bring a few to the capital field to fly against Wielvakian pilots. Training would improve "
          "quickly. Their past would follow them, and some officers ask what else such instructors might pass on.",
          ('air', 'medal'), after_any=('air_flying_hours', 'air_army_support'), requires=(After('1998.6.19'),), cost=10,
          exclusive=('air_home_aggressors',), reward=(Idea('aggressor_course'),)),
    Focus('air_home_aggressors', 'Train Aggressors at Home',
          "The alternative takes the best squadron leaders off the line for a year to write their own tactics manual and fly "
          "as an enemy unit in borrowed markings. It is slower, and the first course repeats mistakes nobody abroad would make. "
          "It also builds knowledge that belongs to the air arm and cannot leave on the next flight out.",
          ('training', 'medal'), after_any=('air_flying_hours', 'air_army_support'), cost=10,
          exclusive=('air_hired_aggressors',), reward=(Idea('home_instructors'),)),
    Focus('air_lowland_plan', 'An Air Plan for the Low Lands',
          "Fields, radars and squadrons have grown one project at a time. A single air defence plan now ties them together: "
          "which radar feeds which control room, which squadron scatters to which field, and where the anti-aircraft guns "
          "stand. Writing it exposes every gap, and closing them will take the rest of the decade.",
          ('radar', 'document'), after_any=('air_hired_aggressors', 'air_home_aggressors'), reward=(Idea('lowland_air_plan'),)),
))

WAR = Branch('war', 'War Beyond the Gebet Frontier', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_outbreak', 'War Breaks Out Near Gebet',
          "In late March 1995 the Belkan War breaks out. Gebet, across the frontier from South Gangel and Alaoboa, also borders "
          "Belka. Wielvakia is not a party. The government puts the frontier commands on alert, opens a situation room under "
          "the capital and orders the border police to count every vehicle that crosses in either direction.",
          ('security', 'communications'), requires=(After('1995.3.25'),), reward=(Idea('war_alert'), Event('gebet_war'))),
    Focus('war_open_crossings', 'Keep the Gebet Crossings Open',
          "One answer keeps the Gebet crossings open to anyone with papers, and to families without them once they register. "
          "It is the decent course and the costly one. Frontier towns fill, prices rise and the security services worry about "
          "who else might cross among the families. Gebet, at least, will remember who kept the door open.",
          ('refugees', 'gate'), after=('war_outbreak',), cost=10, exclusive=('war_sealed_crossings',),
          reward=(Idea('refuge_crossings'),)),
    Focus('war_sealed_crossings', 'Seal the Gebet Crossings',
          "The other answer closes the crossings to everyone except diplomats and relief convoys until the front settles. "
          "Wielvakia keeps the war at arm's length and the frontier towns stay calm. Families on the far side are left to "
          "whatever lies behind them, and that choice will be remembered on both sides of the line for years.",
          ('security', 'gate'), after=('war_outbreak',), cost=10, exclusive=('war_open_crossings',),
          reward=(Idea('sealed_crossings'),)),
    Focus('war_model_radar', 'Radar for the South Gangel Junction',
          "When Belkan forces assault Model, a border city in Gebet, the fighting comes near enough that the government takes "
          "no chances. A second air defence radar goes to South Gangel and the sirens are tested in a public drill so people "
          "know what they mean. The drill frightens some of the towns it is meant to reassure.",
          ('radar', 'security'), after=('war_outbreak',), requires=(HasGlobal('ac_bwr_model'),),
          reward=(Build('radar_station', 1, 325), WarSupport(0.02))),
    Focus('war_reception_halls', 'Reception Halls in South Gangel',
          "Open crossings need somewhere for families to sleep. Schools, sports halls and a disused barracks in South Gangel "
          "become reception halls with kitchens, clinics and registration desks run by the district and volunteers. Pupils "
          "lose their gyms and taxpayers lose their patience. The halls keep the arrivals off the roads and out of the cold.",
          ('refugees', 'civil'), after=('war_open_crossings',), reward=(TimedIdea('reception_halls', 365),)),
    Focus('war_gebet_line', 'Two Divisions to the Gebet Line',
          "Sealed crossings mean little without troops behind them. Two divisions, one armoured and one motorised, move to "
          "the frontier opposite Gebet and dig in along the roads into South Gangel and Alaoboa. Their fuel and ammunition "
          "come from stocks meant for training, and the divisions left in the parks drill less for a year.",
          ('security', 'command'), after=('war_sealed_crossings',), reward=(TimedIdea('gebet_line', 365), XP('army', 10))),
    Focus('war_relief_fuel', 'Fuel for the Relief Convoys',
          "Relief convoys bound for the war zone cannot buy fuel at any price once they leave the lowland depots. The state "
          "company releases fuel from the capital's tank farms at cost to any relief convoy that asks, whatever flag it flies. "
          "It drains a reserve built for Wielvakian emergencies and earns the country quiet gratitude.",
          ('logistics', 'peace'), after=('war_outbreak',), requires=(HasFlag('fuel_reserve_held'),),
          reward=(TimedIdea('relief_fuel', 365),)),
    Focus('war_grain_stores', 'Seal the Lowland Grain Stores',
          "When nuclear devices are used in the Waldreich Mountains, nobody in the Low Lands knows what the wind might carry. "
          "The government seals the season's grain in the state stores and releases it only after laboratory tests, with "
          "results posted at every market. Farmers wait for their money, and buyers trust what they eat.",
          ('medical', 'shelter'), after=('war_outbreak',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(TimedIdea('grain_seal', 730),)),
    Focus('war_stand_down', 'Stand Down the Frontier Commands',
          "Once the fighting beyond Gebet is over and the news from Belka is of treaties rather than fronts, the frontier "
          "commands stand down. Reservists go home, the situation room is mothballed and the border police return to customs "
          "work. The government publishes what the war months cost in fuel, overtime and lost trade, a large figure for a "
          "country that never fired a shot.",
          ('peace', 'document'), after_any=('war_open_crossings', 'war_sealed_crossings'),
          requires=(After('1995.6.20'), NotGlobal('belkan_war_is_happening')),
          reward=(RemoveIdea('war_alert'), Stability(0.03))),
    Focus('war_reconstruction', 'Lowland Bids for Rebuilding Work',
          "With Belka defeated, the Allied nations and the countries around the war begin to rebuild what was bombed, and they "
          "need steel, fuel, trucks and cement. Lowland factories bid for the orders and win a share. The work is welcome and "
          "temporary, and it draws the factories toward markets that may vanish once the rebuilding ends.",
          ('rebuild', 'industry'), after=('war_stand_down',), requires=(HasGlobal('belka_lost_belkan_war'),),
          exclusive=('war_long_watch',), reward=(TimedIdea('rebuild_contracts', 730),)),
    Focus('war_long_watch', 'A Victorious Belka Two Frontiers Away',
          "Belka has won its war, and the balance of power beyond Gebet has shifted for years to come. Wielvakia shares no "
          "frontier with Belka, but Gebet does, and Gebet shares one with Wielvakia. The army keeps its frontier divisions at higher "
          "readiness and the budget pays for it. Nobody in Mankovce expects the region to settle soon.",
          ('security', 'radar'), after=('war_stand_down',), requires=(HasGlobal('belka_won_belkan_war'),),
          exclusive=('war_reconstruction',), reward=(Idea('long_watch'),)),
    Focus('war_officer_oath', 'A Fresh Oath for the Officers',
          "When A World With No Boundaries launches a coup at the end of 1995, governments across the region start asking whom "
          "their own officers really answer to. Every Wielvakian officer renews the oath of service and declares any foreign "
          "association, and a small board reviews the declarations. Most officers find it insulting, and a few find it alarming.",
          ('medal', 'document'), after=('war_outbreak',), requires=(After('1995.12.25'),), reward=(Idea('officer_oath'),)),
))

SKY = Branch('sky', 'Ulysses over the Low Lands', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_announcement', 'The Asteroid Announcement',
          "Wielvakians learn of the coming impact from the FCU President's broadcast in April 1996, together with the news that "
          "a defence against the asteroid is being planned. Which countries lie in the path of its debris is anybody's guess. "
          "The country owns no observatory, no public shelters and no plan, so a civil defence commission is convened in the "
          "capital within the week and asks for everything at once.",
          ('meteor', 'document'), requires=(After('1996.4.20'),), reward=(Idea('impact_watch'), Event('ulysses_mankovce'))),
    Focus('sky_data_line', 'A Data Line to the Observatories',
          "Without telescopes of its own, Wielvakia depends on what foreign observatories publish. A leased data line and a "
          "small team of astronomers and programmers in the capital receive the orbit updates and turn them into plain advice "
          "for the commission. It is borrowed knowledge, and it arrives hours faster than the newspapers.",
          ('telescope', 'communications'), after=('sky_announcement',),
          reward=(Research('electronics', 0.5, 1), Flag('orbit_updates'))),
    Focus('sky_city_shelters', 'Shelters Under the Capital',
          "One camp wants deep shelters dug under Mankovce and the lowland towns, with ventilation, water and supplies for "
          "weeks. Construction would tear up the streets for two years and swallow the commission's budget. When it is done, "
          "the cities will have somewhere to go that is not a cellar, whatever falls and wherever it lands.",
          ('shelter', 'civil'), after=('sky_announcement',), cost=10, exclusive=('sky_dispersal',),
          reward=(SwapIdea('impact_watch', 'city_shelters'),)),
    Focus('sky_dispersal', 'Plans to Leave the Lowland Towns',
          "The other camp says shelters are useless on an open plain if the danger is fire and blast, and that people should "
          "leave instead. Every lowland town receives a dispersal plan naming trains, roads and host villages in the Vakia "
          "hills. Plans are cheap to write and hard to rehearse, and villagers ask who will feed the guests.",
          ('refugees', 'rail'), after=('sky_announcement',), cost=10, exclusive=('sky_city_shelters',),
          reward=(SwapIdea('impact_watch', 'dispersal_plans'),)),
    Focus('sky_gallery_shelters', 'Lease the Deep Vakia Galleries',
          "Vakia's worked-out mine galleries are the deepest spaces in the country. The commission leases the safest of them "
          "from their owners, shores them, installs lights and air, and stocks them for the mining towns. Owners demand rent "
          "and miners point out which galleries flood. The registry from the gallery count shows which ones are sound.",
          ('shelter', 'tools'), after=('sky_city_shelters',), requires=(Completed('ore_gallery_count'),),
          reward=(Idea('gallery_shelters'),)),
    Focus('sky_evacuation_trains', 'Evacuation Trains on the Lowland Lines',
          "The dispersal plans depend on the railways. Sidings at the Farnlands stations are lengthened, spare carriages are "
          "kept serviceable and timetables are written for moving whole towns in a day. The work improves ordinary rail "
          "service as well, though freight customers complain about carriages kept idle in the sidings.",
          ('rail', 'refugees'), after=('sky_dispersal',), reward=(Build('infrastructure', 1, 326), Research('train_tech', 0.5, 1))),
    Focus('sky_impact_drills', 'Drills for the Fragment Estimate',
          "When the astronomers revise their damage estimate in July 1998 to allow for fragments falling on eastern Anea, the "
          "commission takes the warning as a lesson rather than a reprieve: estimates change. Every district now runs impact "
          "drills twice a year, with sirens, assembly points and rehearsed routes. Attendance falls after the first drill.",
          ('meteor', 'security'), after_any=('sky_city_shelters', 'sky_dispersal'), requires=(After('1998.7.29'),),
          reward=(TimedIdea('impact_drills', 730),)),
    Focus('sky_recovery_teams', 'Standing Recovery Teams',
          "As Ulysses passes the Roche limit in July 1999, the commission turns from shelter to recovery. Engineers, medics "
          "and heavy plant are organised into standing teams, kept ready for whatever the fragments or anything else might do. "
          "They cost wages every year whether or not disaster comes, and in most years it does not.",
          ('rebuild', 'medical'), after_any=('sky_gallery_shelters', 'sky_evacuation_trains', 'sky_impact_drills'),
          requires=(After('1999.7.8'),), reward=(Idea('recovery_teams'),
                                                 Tooltip('No damage in Wielvakia is assumed; the teams stand ready only.'))),
    Focus('sky_help_neighbours', 'Recovery Teams for the Neighbours',
          "The orbit updates keep arriving after the asteroid's passage, and with them reports of where help is needed. The "
          "commission offers its standing teams to any neighbour that asks, travelling with their own fuel and food so that they "
          "burden nobody. The cost falls on the Wielvakian budget; the goodwill, when it comes, falls on Wielvakia.",
          ('peace', 'rebuild'), after=('sky_recovery_teams',), requires=(HasFlag('orbit_updates'),),
          reward=(TimedIdea('regional_recovery', 730),)),
))

BRANCHES = (ADMIN, OIL, ORE, ARMOUR, FRONTIERS, COAST, AIR, WAR, SKY)

DECISIONS = (
    DecisionDef('sell_crude_forward', 'Sell Lowland Crude Forward',
                'The treasury sells a season of lowland crude before it is pumped and spends the money now. Repeatable once a '
                'year; the fields carry less investment while the sale runs.',
                40, (TimedIdea('crude_forward', 180),), requires=(Completed('oil_survey'),), cooldown=365),
    DecisionDef('plain_manoeuvres', 'Hold Manoeuvres on the Plain',
                'Whole divisions take the field on the Farnlands range for three months. Repeatable once a year; the '
                'manoeuvres burn training fuel.',
                30, (TimedIdea('autumn_manoeuvres', 90),), requires=(Completed('arm_farnlands_range'),), cooldown=365),
    DecisionDef('joint_state_session', 'Convene the State Councils Together',
                'The four state councils sit together in the capital for a week of public questions. Repeatable once a year.',
                25, (Stability(0.02),), requires=(Completed('adm_state_councils'),), cooldown=365),
    DecisionDef('nadomlin_radar', 'A Radar Mast at Nadomlin',
                'Engineers raise a radar mast beside the Nadomlin dispersal field to cover the northern frontiers. A one-time '
                'works programme.',
                50, (Build('radar_station', 1, 326),), requires=(Completed('air_nadomlin_field'),)),
    DecisionDef('send_relief_train', 'Send a Relief Train to the Frontier',
                'A train of food and medicine runs to the Gebet frontier for the families on both sides. Once only; it costs '
                'political capital at home.',
                30, (TimedIdea('relief_train', 180), Stability(0.01)), requires=(Completed('war_outbreak'),)),
    DecisionDef('open_harbour_dues', 'Cut the Harbour Dues for a Season',
                'The Vakia harbours halve their dues for visiting merchant ships for six months. Repeatable once a year.',
                35, (TimedIdea('port_calls', 180),), requires=(Completed('cst_naval_review'),), cooldown=365),
)
