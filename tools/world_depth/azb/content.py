"""Azbekerania (AZB): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections suspended, neutrality 48 and fascism 50 percent popularity,
grand doctrines and starting technology), the unnamed starting office, the ten 1991 states
with their neutral district captions, the map facts read from map/definition.csv,
map/provinces.bmp and map/railways.txt, and the global flags other mod scripts already set.
Official: ACES Chronicle rows used only as date anchors for distant pressures, each cited by
its exact key. Everything else, including every Azbekeranian choice, office, idea, building,
decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='AZB', name='Azbekerania', root='world', package='azb',
                  themes=('training', 'rail', 'industry'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots; '
           'technology including tech_mountaineers, tech_engineers, early_fighter and basic_train; grand doctrines '
           'superior_firepower, fleet_in_being and operational_integrity. The starting leader is the unnamed National '
           'Administration office (AZB_ac_government_office), whose description says its 1991 holder has not been established. '
           'The tree never names a holder. Country names by ideology (Republic of Azbekerania and others) are inherited and unchanged.',
           'mod/2985041246/history/countries/AZB - Azbekerania.txt; mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 347, 387, 407, 417, 421, 434, 452 (capital), 473, 477 and 493, captioned Azbekerania '
           'District A, B, C, D, E, F, Capital District, H, I and J by the neutral regional labels (canonical regional mapping '
           'unestablished). Victory points Azbekerania Capital Centre (2565), Logistics Centre 3101 (District A) and Logistics '
           'Centre 1750 (District C). Districts A, C and the Capital District are cities, each with four civilian and two military '
           'factories and oil, aluminium, rubber and steel; the other seven are towns with no buildings, infrastructure or resources. '
           'The capital holds the naval base, two dockyards and the fuel silo. Terrain from map/definition.csv: forest and hills in A, '
           'plains in B, C, D, F, I and the Capital District, hills and one mountain province in E, hills and desert in H, desert in J; '
           'coastal districts B, C, Capital, I and J; District I has eleven provinces. Land neighbours computed from map/provinces.bmp: '
           'Yuktobania (Districts A, C, D, E and I), Seterano (A and B) and Aemurraq (Capital District, H and J); District F alone '
           'touches no frontier and no sea. The only railway (map/railways.txt) runs Capital District - District D - District C - '
           'District A. No place outside these captions is named.',
           'mod/2985041246/history/states/347-State_347.txt and the nine other AZB state files; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role continental reserve; 12 civilian, 6 military and 2 naval factories; '
           'eight infantry formations of six battalions and an engineer company, based at the capital and the two logistics centres; '
           '72 fighters and 12 support aircraft split between the capital and District A; two coastal escorts in the Maritime '
           'Service; 60 convoys; civilian economy, export focus and volunteer only laws; research priority Physical Sustainment '
           '(transport, equipment replacement, affordable service); political institution civil_administration, capacity 40. '
           'Fictional calibration, not canon national accounts or order of battle.',
           'tools/world_starts/empty_calibration_draft.json; tools/world_starts/sustainment.json; docs/WORLD_STARTS_CALIBRATION.md; '
           'tools/world_foundation/country_registry.json; mod/2985041246/history/units/AZB_ws_land.txt, AZB_ws_air.txt, AZB_ws_navy.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour consistency: Aemurraq (tools/world_depth/aem/content.py) records land frontiers with Azbekerania, Echea and '
           'Sotoa and posts on its own side. This tree only builds and governs on the Azbekeranian side, offers consultations whose '
           'acceptance it never assumes, and claims no Aemurraqi action or outcome.',
           'tools/world_depth/aem/content.py'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses may pass close to the Earth with a chance of impact. Background '
           'to the Ulysses branch only.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Opens the Belkan War branch; Azbekerania takes no part.', '1995 / 03.25'),
    Source('Official',
           'Nearly all of the Republic of Ustio falls under Belkan control. Used as the date gate and premise of the staff study '
           'focus; no Azbekeranian involvement is claimed.', '1995 / 03.30'),
    Source('Official',
           'Ustio enters an alliance with Osea and begins its resistance. Date gate of the outside-help lesson; no alliance is '
           'created for Azbekerania.', '1995 / 04.01'),
    Source('Official',
           'The Allied Forces liberate Ustio\'s capital Directus. Date gate of the liberation study focus.', '1995 / 05.13'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Background to the fallout focus, which also '
           'reads the mod flag belka_dropped_nukes; no fallout in Azbekerania is claimed.', '1995 / 06.06'),
    Source('Official',
           'A treaty is signed in Lumen and the Belkan War ends. Date gate of the treaty focus.', '1995 / 06.20'),
    Source('Official',
           'The FCU announces that Ulysses will impact the Earth. Date gate of the Ulysses branch; where fragments fall is never '
           'stated.', '1996 / 04.20'),
    Source('Official',
           'Ulysses passes through the Roche limit of the Earth. Date gate of the Roche night focus and event; no damage in '
           'Azbekerania is claimed.', '1999 / 07.08'),
    Source('Official',
           'Osea and Yuktobania cooperate to convert the Arkbird into a platform for clearing debris from satellite orbits. '
           'Background to the satellite focus, which reads the mod flag ac_sp_arkbird_complete; no Azbekeranian role is claimed.',
           '1999 / 10.08'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air batteries. '
           'Background to the air-defence study, which reads the mod flag ac_ucw_war_started.', '2003 / SUMMER'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war, belka_lost_belkan_war and belka_dropped_nukes '
           '(events/Belka.txt); ac_sp_arkbird_complete (common/scripted_effects/ac_special_projects.txt); ac_ucw_war_started, '
           'ac_ucw_war_averted and ac_ucw_stonehenge_destroyed (common/scripted_effects/ac_ucw.txt). Each reaction is a leaf '
           'focus or a side line, so no outcome blocks the closing focus.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_special_projects.txt; '
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Azbekeranian focuses, ideas, offices, buildings, flags, decisions and events in this spec, including the framing of '
           'the fascist half of opinion as reservists\' leagues and the neutral half as the non-party civil establishment. No named '
           'people; offices are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in the '
           'ten 1991 states.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the suspended republic
    IdeaDef('suspended_calendar', 'The Suspended Calendar', 'An election calendar on the statute book that nobody is allowed to use.',
            {'political_power_gain': 0.08, 'stability_factor': -0.04}, ('ballot', 'document')),
    IdeaDef('official_gazette', 'The Official Gazette', 'Every decree printed and posted in all ten districts within a week.',
            {'political_power_factor': 0.05, 'stability_factor': 0.01}, ('document', 'communications')),
    IdeaDef('convention_call', 'A Convention Called', 'Delegates from ten districts are writing the electoral law.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('assembly', 'ballot')),
    IdeaDef('clerks_rule', 'Rule by the Permanent Secretaries', 'The civil service governs openly in its own name.',
            {'political_power_factor': 0.08, 'stability_factor': -0.02}, ('document', 'command')),
    IdeaDef('league_pressure', 'The Leagues on the March', 'Reservists\' leagues parade weekly and demand a national front.',
            {'war_support_factor': 0.06, 'army_org_factor': 0.03, 'stability_factor': -0.03}, ('training', 'ballot')),
    IdeaDef('ballot_republic', 'A Republic That Votes', 'General ballots across all ten districts on a fixed calendar.',
            {'stability_factor': 0.08, 'political_power_factor': 0.05}, ('ballot', 'scales')),
    IdeaDef('results_tables', 'Quarterly Results Tables', 'Every ministry judged each quarter on published figures.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_factor': 0.05}, ('document', 'economy')),
    IdeaDef('muster_state', 'The Muster Roll State', 'Every adult on a reserve roll kept by a block warden.',
            {'war_support_factor': 0.08, 'training_time_army_factor': -0.10, 'stability_factor': -0.02}, ('security', 'training')),
    # three cities and seven towns
    IdeaDef('three_city_state', 'A Country of Three Cities', 'All industry and every paved road sit in three of ten districts.',
            {'stability_factor': -0.02, 'production_speed_infrastructure_factor': 0.05}, ('civil', 'logistics')),
    IdeaDef('town_charters', 'Chartered Towns', 'Seven elected town councils with a fixed share of city revenue.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.10}, ('ballot', 'civil')),
    IdeaDef('city_wardens', 'City Wardenships', 'The three cities administer the seven towns as their own.',
            {'production_speed_buildings_factor': 0.06, 'political_power_gain': 0.05}, ('command', 'civil')),
    IdeaDef('town_clinics', 'Clinics, Schools and Water Towers', 'Town budgets spent on the services that keep people at home.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('medical', 'civil')),
    IdeaDef('engineer_circuits', 'The Engineers\' Circuit', 'City engineers inspect and repair the towns every month.',
            {'production_speed_infrastructure_factor': 0.15}, ('tools', 'logistics')),
    # industry
    IdeaDef('city_output_ledger', 'The Three-City Ledger', 'One account of what the three industrial districts produce and ship.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.03}, ('document', 'industry')),
    IdeaDef('hard_currency_exports', 'Hard-Currency Exports', 'Oil, steel and aluminium sold abroad under the export law.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': -0.03}, ('economy', 'navy')),
    IdeaDef('through_rates', 'Through Rates to the Wharf', 'One bill of lading from plant gate to ship\'s hold.',
            {'industrial_capacity_factory': 0.07, 'consumer_goods_factor': -0.04}, ('rail', 'economy')),
    IdeaDef('motor_programme', 'The Motor Programme', 'Trucks, tyres and spares made at home behind protected prices.',
            {'production_speed_arms_factory_factor': 0.10, 'consumer_goods_factor': 0.02}, ('industry', 'logistics')),
    IdeaDef('dispersal_plan', 'The Dispersal Plan', 'New plants go inland, away from the Yuktobanian frontier.',
            {'production_speed_industrial_complex_factor': 0.10, 'production_factory_efficiency_gain_factor': -0.02}, ('industry', 'security')),
    IdeaDef('rolled_sheet', 'Sheet Rolled at Home', 'Aluminium leaves the mills as sheet rather than ingot.',
            {'production_factory_max_efficiency_factor': 0.03, 'research_speed_factor': 0.02}, ('tools', 'industry')),
    IdeaDef('quarterly_census', 'The Quarterly Output Census', 'Output, stocks and orders filed by every plant each quarter.',
            {'production_factory_max_efficiency_factor': 0.04, 'political_power_gain': -0.03}, ('document', 'scales')),
    # the continental reserve
    IdeaDef('reserve_cadre', 'The Reserve Cadre', 'Eight formations that have never moved together.',
            {'army_org_factor': 0.03, 'training_time_army_factor': -0.05}, ('training', 'command')),
    IdeaDef('frontier_screen', 'The Frontier Screen', 'Battalions posted forward along the Yuktobanian frontier.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.03}, ('security', 'training')),
    IdeaDef('depth_reserve', 'The Reserve in Depth', 'The army held together inland, ready to move by road and rail.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.10}, ('rail', 'command')),
    IdeaDef('hill_battalions', 'The Hill Battalions', 'Two battalions with mules, light guns and winter kit for District E.',
            {'army_attack_factor': 0.03, 'attrition': -0.05}, ('training', 'tools')),
    IdeaDef('paid_reserve', 'Paid Reservists', 'Former soldiers drill two weeks a year and answer a call-up within days.',
            {'training_time_army_factor': -0.10, 'consumer_goods_factor': 0.02}, ('medal', 'training')),
    IdeaDef('town_companies', 'Town Companies', 'Part-time volunteers guarding the roads and depots of their own town.',
            {'army_core_defence_factor': 0.08}, ('security', 'civil')),
    IdeaDef('home_built_trucks', 'Trucks of Our Own Pattern', 'Formations equipped with domestic trucks they can repair themselves.',
            {'supply_consumption_factor': -0.05, 'army_speed_factor': 0.04}, ('logistics', 'tools')),
    # frontiers
    IdeaDef('frontier_unease', 'Three Frontiers, No Policy', 'Each frontier district improvises its own relations with the far side.',
            {'stability_factor': -0.02, 'war_support_factor': 0.03}, ('diplomacy', 'security')),
    IdeaDef('frontier_commerce', 'Commerce Across the Frontier', 'Freight and customs houses make every incident expensive.',
            {'industrial_capacity_factory': 0.04, 'war_support_factor': -0.03}, ('economy', 'diplomacy')),
    IdeaDef('armed_neutrality', 'Armed Neutrality', 'No alliance, no favours and a reserve visibly ready.',
            {'army_core_defence_factor': 0.06, 'war_support_factor': 0.05, 'consumer_goods_factor': 0.02}, ('security', 'peace')),
    IdeaDef('neighbour_consultations', 'Standing Consultations', 'Regular offers of talks on incidents, smuggling and freight.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('diplomacy', 'assembly')),
    IdeaDef('liaison_desk', 'The Incident Liaison Desk', 'A telephone that answers at any hour when something happens on the line.',
            {'stability_factor': 0.03, 'planning_speed': 0.03}, ('communications', 'peace')),
    IdeaDef('attache_reports', 'Attache Reports', 'Trained observers in three neighbouring capitals.',
            {'planning_speed': 0.08, 'research_speed_factor': 0.01}, ('diplomacy', 'document')),
    IdeaDef('frontier_standing_orders', 'Frontier Standing Orders', 'Written rules for who may fire, cross and sign on the frontier.',
            {'army_org_factor': 0.04, 'stability_factor': 0.02}, ('document', 'security')),
    # air
    IdeaDef('split_wings', 'Two Wings Under One Command', 'Seventy-two fighters on two fields with one maintenance plan.',
            {'experience_gain_air_factor': 0.05, 'air_superiority_efficiency': 0.02}, ('air', 'command')),
    IdeaDef('single_wing', 'One Wing at the Crossroads', 'The whole fighter force on one inland base.',
            {'air_superiority_efficiency': 0.08, 'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('scattered_strips', 'Scattered Strips', 'Pairs and fours of fighters spread across rough town strips.',
            {'air_mission_efficiency': 0.05, 'air_defence_factor': 0.06}, ('runway', 'civil')),
    IdeaDef('support_flights', 'Support Flights for the Formations', 'Twelve support aircraft working with the reserve on the ground.',
            {'air_mission_efficiency': 0.06, 'army_attack_factor': 0.02}, ('air', 'training')),
    IdeaDef('night_alert', 'Night Alert Pairs', 'Fighters on radar warning from dusk until dawn.',
            {'air_detection': 0.10, 'air_superiority_efficiency': 0.03}, ('air', 'radar')),
    # the maritime service
    IdeaDef('two_escort_service', 'A Service of Two Escorts', 'Two coastal escorts and sixty merchant hulls on two coasts.',
            {'naval_coordination': 0.03, 'navy_org_factor': 0.03}, ('navy', 'document')),
    IdeaDef('ore_convoy_escorts', 'Escorted Ore Convoys', 'The escorts sail with the export convoys on their outward legs.',
            {'navy_org_factor': 0.06, 'naval_coordination': 0.04}, ('navy', 'logistics')),
    IdeaDef('coast_watchers', 'Coastwatchers Ashore', 'Headland watchers and radio huts on both coasts.',
            {'air_detection': 0.05, 'naval_coordination': 0.05}, ('radar', 'navy')),
    IdeaDef('lifeboat_stations', 'Lifeboat Stations', 'Volunteer rescue crews paid by a levy on cargo.',
            {'stability_factor': 0.02, 'navy_org_factor': 0.03}, ('navy', 'medical')),
    # the Belkan War abroad
    IdeaDef('war_nerves', 'War Nerves', 'A distant war fills the newspapers and the staff war room.',
            {'war_support_factor': 0.04, 'stability_factor': -0.02}, ('communications', 'security')),
    IdeaDef('city_bastions', 'The City Bastions', 'Every formation committed to the frontier cities from the first hour.',
            {'army_defence_factor': 0.06, 'army_core_defence_factor': 0.05}, ('security', 'industry')),
    IdeaDef('elastic_plan', 'Ground for Time', 'Fall back, keep the army whole, strike when the attacker is stretched.',
            {'army_speed_factor': 0.06, 'planning_speed': 0.10}, ('command', 'logistics')),
    IdeaDef('worth_helping', 'Worth Helping', 'Exercises, airfields and officers ready to work with foreign friends.',
            {'political_power_gain': 0.05, 'research_speed_factor': 0.02}, ('diplomacy', 'runway')),
    IdeaDef('ustio_notes', 'The Ustio Notes', 'Staff studies of a small republic overrun and recovered.',
            {'planning_speed': 0.08}, ('document', 'command')),
    IdeaDef('fallout_counters', 'Radiation Counters', 'Counters in every district office and engineers trained to read them.',
            {'stability_factor': 0.02, 'attrition': -0.03}, ('science', 'medical')),
    IdeaDef('demolition_plans', 'Bridges Marked for Demolition', 'Charges stored near every bridge between frontier and crossroads.',
            {'army_core_defence_factor': 0.05, 'planning_speed': 0.05}, ('bridge', 'security')),
    IdeaDef('raised_readiness', 'Raised Readiness', 'The reserve held at higher readiness for a year.',
            {'army_org_factor': 0.05, 'consumer_goods_factor': 0.03}, ('training', 'security')),
    # Ulysses
    IdeaDef('impact_committee', 'The Impact Committee', 'Ten districts asking the capital what to do.',
            {'stability_factor': -0.02, 'political_power_gain': 0.05}, ('meteor', 'assembly')),
    IdeaDef('hill_galleries', 'Galleries in the Hills', 'Shelters cut into the high ground of District E.',
            {'static_anti_air_damage_factor': 0.06, 'stability_factor': 0.04}, ('shelter', 'tools')),
    IdeaDef('coastal_thinning', 'The Coast Thinned Out', 'Families, records and spare machinery moved inland.',
            {'stability_factor': 0.03, 'production_factory_efficiency_gain_factor': -0.03}, ('refugees', 'logistics')),
    IdeaDef('rescue_corps', 'The Rescue Corps', 'Eight formations trained to dig, clear, carry and feed.',
            {'stability_factor': 0.05, 'army_org_factor': -0.05}, ('medical', 'training')),
    IdeaDef('full_silo', 'A Full Silo', 'The capital fuel silo kept full against the impact years.',
            {'stability_factor': 0.02, 'supply_consumption_factor': -0.05}, ('logistics', 'shelter')),
    IdeaDef('voted_shelter_plan', 'A Shelter Plan Voted by All', 'An evacuation plan every district voted for.',
            {'stability_factor': 0.05}, ('ballot', 'shelter')),
    IdeaDef('printed_rations', 'Ration Cards on File', 'Cards for every household, printed before they are needed.',
            {'stability_factor': 0.03, 'political_power_factor': 0.03}, ('document', 'civil')),
    IdeaDef('warden_shelters', 'Wardens at the Shelters', 'Block wardens keep the shelter lists, street by street.',
            {'war_support_factor': 0.05, 'stability_factor': 0.02}, ('security', 'shelter')),
    IdeaDef('town_radios', 'Radios in the Town Offices', 'A set, a generator and an operator in every town.',
            {'stability_factor': 0.02, 'planning_speed': 0.03}, ('communications', 'civil')),
    # the new century
    IdeaDef('millennium_census', 'The Census of 2000', 'The second full count of people, plants and roads.',
            {'political_power_factor': 0.04, 'research_speed_factor': 0.02}, ('document', 'civil')),
    IdeaDef('satellite_rentals', 'Rented Satellite Links', 'Broadcast and telephone capacity rented on cleared orbits.',
            {'research_speed_factor': 0.03}, ('satellite', 'communications')),
    IdeaDef('city_batteries', 'Batteries Over the Cities', 'Guns and fire-control radar around the three cities.',
            {'static_anti_air_damage_factor': 0.12, 'air_detection': 0.05}, ('missile', 'radar')),
    IdeaDef('wing_renewal', 'The Wing Renewal', 'New airframes for both wings over five years.',
            {'air_superiority_efficiency': 0.06, 'consumer_goods_factor': 0.02}, ('air', 'industry')),
    IdeaDef('export_truck_orders', 'Trucks for Export', 'The motor works sells abroad at wartime prices.',
            {'industrial_capacity_factory': 0.05}, ('logistics', 'economy')),
    IdeaDef('war_ore_prices', 'Metal at War Prices', 'Ore and metal cargoes sold into a wartime market.',
            {'industrial_capacity_factory': 0.06, 'stability_factor': -0.01}, ('economy', 'navy')),
    IdeaDef('inland_overflow', 'Inland Plants on Overflow', 'Dispersed plants take orders the cities cannot fill.',
            {'production_factory_efficiency_gain_factor': 0.05}, ('industry', 'tools')),
    # decisions
    IdeaDef('class_called', 'A Reserve Class at Drill', 'One year group of reservists called to the drill grounds.',
            {'army_org_factor': 0.05, 'consumer_goods_factor': 0.02}, ('training', 'medal')),
    IdeaDef('silo_release', 'Silo Fuel Released', 'Fuel from the capital silo sold to calm the pumps.',
            {'stability_factor': 0.04}, ('logistics', 'economy')),
    IdeaDef('liaison_calm', 'A Quiet Season on the Line', 'Liaison days settle grievances before they become incidents.',
            {'stability_factor': 0.03}, ('peace', 'diplomacy')),
    IdeaDef('wing_exercise', 'Both Wings Exercised', 'A joint exercise of the two fighter wings and the radar plot.',
            {'experience_gain_air_factor': 0.10}, ('air', 'training')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('district_convention', 'Cabinet of the Ten-District Convention',
           'A cabinet chosen by delegates elected from all ten districts, governing collectively and answerable to the convention '
           'until general ballots return on a fixed calendar. Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
    Office('civil_directorate', 'Directorate of the Permanent Secretaries',
           'A directorate of senior career officials holding the government seals in the name of the civil service, with ministerial '
           'posts left vacant and elections under review. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('reserve_front', 'Council of the Reserve Front',
           'A council of senior reserve officers at the head of the merged reservists\' leagues, ruling by decree with a muster roll '
           'for every citizen. Provisional gameplay office with no named holder.',
           'fascism', 'stratocracy_fascism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('calendar_question', 'An Election Nobody May Hold', (
        "The statute book of the Republic of Azbekerania still prints a general ballot every forty-eight months, with dates, "
        "polling rules and the duties of district returning officers set out in full. None of it has been used under the "
        "present suspension. The National Administration governs under the democratic banner, but when the interior ministry "
        "quietly polls the districts, the democrats register at one voter in a hundred.",
        "The rest of the country has sorted itself into two blocs of nearly equal size. One is the reservists' leagues: former "
        "soldiers of the eight formations, their families and the towns that send them, who want the state run like a "
        "mobilisation table. The other is the civil establishment of the three industrial cities, career officials and district "
        "notables who belong to no party and distrust anyone who does. Each bloc believes the suspension favours the other.",
        "The Administration cannot answer the calendar question in a single sitting. It can choose who gets to argue about it "
        "first. A public hearing gives the leagues a stage and the establishment a grievance. A ministerial review keeps both "
        "out of the room. Inviting both to a round table satisfies neither, but it keeps them talking rather than marching.",
    ), (
        Option('Hold public hearings in all ten districts.', (Stability(0.02), WarSupport(0.02), PP(-15))),
        Option('Refer it to a ministerial review.', (PP(40), Stability(-0.02))),
        Option('Seat the leagues and the establishment together.', (PP(15), Stability(0.01))),
    ), picture=1),
    EventDef('town_survey', 'The Seven Towns Report', (
        "The survey parties return from the seven towns after a season on tracks that their trucks were never built for. Their "
        "reports agree on the essentials. District B, District D, District E, District F, District H, District I and District J "
        "have no paved road, no factory and no resource any geologist has recorded. Schools and clinics depend on what each "
        "town can raise for itself, which is usually very little.",
        "The details differ. District I is bigger than any of the three cities' districts and takes days to cross. District E "
        "climbs into hills and the republic's only mountain country along the Yuktobanian frontier. District J is desert running down to a coast "
        "with no harbour. District F is small and quiet and sits in the middle of everything. District B has a coast and a "
        "frontier with Seterano and nothing to connect them.",
        "The ministers must decide what to do with the findings. Publishing them district by district will start an argument "
        "between the three cities and the seven towns that no ministry can control. Filing them inside the ministries will let "
        "the road budget follow the figures quietly, while every town assumes it was cheated. Either way the towns now know "
        "that someone in the capital has looked.",
    ), (
        Option('Publish every district return.', (Stability(0.03), PP(-20))),
        Option('Keep the returns for the road budget.', (PP(35), Stability(-0.01))),
    ), picture=0),
    EventDef('output_ledger', 'Three Cities, One Set of Books', (
        "The ledger clerks finish adding up the three industrial districts and find that nobody had ever done it before. The "
        "Capital District, District A and District C each run four civilian plants and two arms plants and each draws on its "
        "own oil, steel, aluminium and rubber. Together they are the whole of the republic's industry. Separately, each city "
        "has been negotiating with foreign buyers as if the other two did not exist.",
        "The export law sends a large share of everything abroad, and the ledger shows how much of the remainder is lost "
        "between plant gates and the customs sheds. Rubber is the tightest figure: barely enough for the army's tyres if none "
        "is sold. Fuel is the strangest, because the capital's silo is rarely more than half full while the cities export "
        "crude oil every week of the year.",
        "The ministers can use the ledger to force the three city chambers into a single trade policy, which will take years "
        "and set the cities against the capital. Or they can hand each chamber its own figures and let the cities tidy their "
        "books quietly. The figures will reach the newspapers whichever course is chosen, and the leagues already have a reporter "
        "asking about the silo.",
    ), (
        Option('Force a single trade policy.', (PP(-20), Research('industry', 0.5, 1))),
        Option('Let each city tidy its own books.', (PP(30), Stability(-0.01))),
    ), picture=2),
    EventDef('reserve_muster', 'Eight Formations on the Road', (
        "For one week every formation of the army leaves its barracks at the same time. Three march out of the Capital Centre, "
        "three from the logistics centre in District A and two from the logistics centre in District C. Their orders are simple: "
        "reach an assembly area at the inland crossroads in District F, report strength and return. Nobody has attempted it "
        "before, and the staff suspects why.",
        "The road from the capital is graded only for part of the way. Trucks from District A must come round by rail through "
        "District D, and the line can carry one formation at a time. Two formations arrive on schedule, four arrive late, and "
        "two never leave their railheads because the wagons went somewhere else. The engineer companies spend more of the week "
        "repairing culverts than any of them expected.",
        "The chief of staff carries the timings to the Administration in person. They show a continental reserve that cannot "
        "yet reach the middle of its own country inside a week. Releasing them hands the leagues an argument and the city "
        "chambers a scandal about money spent on trucks that sat at railheads. Releasing only photographs of the closing "
        "parade, with bands and a fly-past from the capital wing, keeps spirits high and leaves every road as poor as before.",
    ), (
        Option('Release the timings.', (Stability(-0.02), XP('army', 20))),
        Option('Release the parade photographs.', (PP(20), WarSupport(0.02))),
    ), picture=0),
    EventDef('three_neighbours', 'A Map with Three Frontiers', (
        "The foreign ministry's new frontier map takes up a whole wall of the cabinet room. A long red line marks the frontier "
        "with Yuktobania, running past five districts and close to two of the three industrial cities. A shorter line marks "
        "Seterano along District A and District B. A third runs with Aemurraq past the Capital District, District H and District "
        "J, closer to the capital than any minister had quite realised.",
        "Each frontier has been handled by whoever happened to live near it. Customs officers in District C keep their own "
        "arrangements with their counterparts across the line. Farmers in District B cross to markets on the Seterano side and "
        "come back without paperwork. The garrison in the capital has never planned for a frontier only a short drive from the "
        "cabinet room. None of these habits has ever been written down.",
        "The cabinet is asked for a single policy and finds it has three different problems. The ministers can start with the "
        "largest neighbour and accept that the other frontiers wait, or start with the frontier nearest the capital, or simply "
        "publish the map and ask the districts what they want. The map itself changes nothing on the ground; it only shows the "
        "ministers what they had not looked at.",
    ), (
        Option('Begin with the Yuktobanian frontier.', (WarSupport(0.02), PP(15))),
        Option('Begin with the frontier nearest the capital.', (Stability(0.02), PP(10))),
        Option('Publish the map and consult the districts.', (Stability(0.03), PP(-10))),
    ), picture=1),
    EventDef('frontier_incident', 'Shots in the Dark in District D', (
        "A night patrol near a crossing in District D meets a party of armed men moving without lights. Somebody fires; the "
        "patrol returns fire; the party scatters into the dark. At dawn the patrol finds two abandoned packs full of tinned food "
        "and cigarettes, a wounded man who will not give his name and a set of tyre tracks running toward the line. Nobody is "
        "dead, which everyone agrees is lucky.",
        "By noon the incident has three explanations. The patrol commander says smugglers. The district notables say deserters "
        "from some army looking for work. The leagues' newspapers say something far worse and print a map with arrows on it. "
        "The frontier authorities across the line, contacted by telephone, say they know nothing and would like the wounded man "
        "returned.",
        "The cabinet must decide how large to make the incident. A full inquiry with outside observers will take months and "
        "satisfy the careful. A quiet handover of the wounded man will end it in a day and anger the leagues. A loud protest will "
        "please the newspapers and commit the republic to a story it cannot prove. Whatever is chosen, the patrols on every "
        "frontier will learn from it what the capital expects of them.",
    ), (
        Option('Open a full inquiry with observers.', (PP(-15), Event('incident_inquiry', 21))),
        Option('Hand the wounded man back quietly.', (Stability(0.02), WarSupport(-0.02))),
        Option('Protest loudly through the ministry.', (WarSupport(0.03), Stability(-0.02))),
    ), picture=1),
    EventDef('incident_inquiry', 'The Inquiry Reports', (
        "Three weeks after the shooting in District D the inquiry delivers its report. It is shorter than anyone expected. The "
        "armed party were smugglers carrying food and cigarettes, and the first shot came from a nervous patrol member who saw "
        "a flashlight and thought it was a weapon. The wounded man was a hired porter. The tyre tracks belonged to a farm truck "
        "on the Azbekeranian side.",
        "The observers sign the report without reservation. The leagues' newspapers, which had printed arrows on maps, print a "
        "correction on an inside page. The patrol commander is moved to a training post and his men are retrained in night "
        "procedures. The district notables in District D, who had been sure it was deserters, say very little and buy the "
        "patrol a meal.",
        "The cabinet now holds an unusual thing: a frontier incident settled entirely by evidence. It can publish the report "
        "in full as an example of how incidents should be handled, at the cost of embarrassing its own army. Or it can thank the "
        "observers privately and file the report, keeping the patrols' pride intact and the lesson inside the general staff "
        "where it may or may not be read.",
    ), (
        Option('Publish the report in full.', (Stability(0.03), WarSupport(-0.01))),
        Option('File it with the general staff.', (PP(20), XP('army', 10))),
    ), picture=0),
    EventDef('belkan_dispatches', 'The Staff Opens a War Room', (
        "In March 1995 a war begins around Belka. Azbekerania has no part in it and no frontier near it, yet within a week "
        "the general staff has opened a war room in the Capital Centre with a wall map, a radio and a duty officer at every "
        "hour. The room exists to answer one question that nobody asks aloud in the cabinet: what happens to a small republic "
        "when the countries around it go to war?",
        "Dispatches arrive from attaches, newspapers and shortwave bulletins, contradictory and late. The leagues demand that "
        "the reserve be called up at once, on the principle that nobody was ever criticised for being ready. The civil "
        "establishment answers that calling up the reserve would empty the plants in the three cities in the middle of a "
        "price boom. Both sides cite the same dispatches.",
        "The cabinet must give the war room a purpose. It can be a study cell that reports quietly to the staff and costs "
        "nothing in public. Or it can be the visible centre of a raised alert, with the formations brought to readiness and the "
        "newspapers briefed each week. The first keeps the plants running; the second tells every neighbour that Azbekerania is "
        "watching.",
    ), (
        Option('A quiet study cell.', (PP(20), Stability(0.01))),
        Option('A raised alert, briefed weekly.', (WarSupport(0.04), Stability(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Azbekeranian response is gameplay', picture=0),
    EventDef('impact_announced', 'Ten Districts Ask What to Do', (
        "In April 1996 the long-feared announcement is made: Ulysses will strike the Earth, a danger astronomers first raised "
        "in December 1994. Which regions will be hit is not yet known to anyone. Within a day every district office in "
        "Azbekerania has telephoned the capital for instructions, and the capital has discovered that it has none to read "
        "out.",
        "The questions are practical. The capital and District C want to know whether their coasts are safe. The seven towns "
        "want to know whether anyone will bring them food if the roads fail. The general staff wants to know whether the "
        "reserve should prepare for war or for disaster, since it cannot do both well. The trade ministry wants to know whether "
        "exports will be held back, and is told to wait.",
        "Before any plan, the cabinet must decide how to speak. It can announce preparations at once and in full, accepting "
        "queues at the markets and a rush of families from the coast inland. Or it can urge calm while the ministries work, "
        "accepting that the plan will arrive late and that rumours will fill the gap. The coastal districts will feel the "
        "choice first.",
    ), (
        Option('Announce everything at once.', (WarSupport(0.02), Stability(-0.02), Event('coast_rumours', 14))),
        Option('Urge calm while the ministries work.', (Stability(0.03),)),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Azbekeranian preparations are gameplay',
        picture=1),
    EventDef('coast_rumours', 'A Rumour on the Coast', (
        "Two weeks after the government announced its preparations, a rumour spreads along the coast from the capital to "
        "District C: the fragments will fall into the sea, and the sea will come ashore. Nobody can say where it started. By the "
        "weekend the coast road inland is jammed with cars, carts and trucks, and the evacuation timetables nobody has written "
        "yet are already overdue.",
        "In District F and District D the arrivals overwhelm towns that have never housed visitors. Prices for rooms and bread "
        "triple. Some families sleep in schools and some in their vehicles. In the capital, half-empty streets encourage looting "
        "in a few warehouses near the naval harbour, and the police ask the garrison for help. The leagues offer their members "
        "as volunteers before anyone has asked.",
        "The cabinet has two ways to respond, neither good. It can deploy the formations to direct traffic, guard the empty "
        "streets and run feeding stations, which works and puts soldiers on every corner. Or it can broadcast the astronomers' "
        "own statements every hour and trust that facts will slowly outrun fear, which is slower and leaves the inland towns to "
        "cope alone for a while.",
    ), (
        Option('Put the formations on the roads.', (Stability(0.02), WarSupport(0.02), PP(-20))),
        Option('Broadcast the astronomers every hour.', (Stability(-0.01), PP(10))),
    ), picture=1),
    EventDef('roche_night', 'A Night with the Trucks Running', (
        "Ulysses crosses the Roche limit on 8 July 1999. Azbekerania meets the night with its engines running: the formations "
        "are drawn up beside their trucks at the Capital Centre and both logistics centres, the evacuation trains are parked "
        "in the District D sidings, and an operator sits awake in every district office with orders to report each hour, even "
        "if only to say that the hour passed.",
        "Most of what reaches the capital is noise. Foreign stations contradict one another, amateur operators relay what other "
        "amateurs claim to have heard, and the duty officers in the plotting room stop chalking rumours on the board after the "
        "first few hours. In the seven towns, families crowd into the town offices around radio sets that arrived only months "
        "earlier and listen in near silence.",
        "Morning comes and the ten districts are intact, tired and uneasy. Wherever the fragments came down, the consequences "
        "will travel to Azbekerania by slower roads: prices, insurance, debris reports and people on the move. The cabinet must "
        "choose between holding the formations beside their trucks for weeks while the reports settle, or releasing them to "
        "barracks and asking the districts to open their shops and schools as usual.",
    ), (
        Option('Keep the formations on alert.', (WarSupport(0.03), Stability(-0.01))),
        Option('Send them back to barracks.', (Stability(0.03), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no damage in Azbekerania is claimed', picture=2),
    EventDef('usean_lesson', 'What the Railguns Teach', (
        "Erusea's invasion of neutral San Salvacion in the summer of 2003, and its seizure of the Stonehenge railguns for use "
        "against aircraft, reach the ten districts as newspaper columns about a faraway continent. The Azbekeranian air staff "
        "reads them differently, because the war poses the one question its two small wings have never answered: what becomes "
        "of an air force when the sky itself is defended from the ground?",
        "The staff splits at once. One group argues that the railguns prove the value of air defence from the ground: guns and "
        "radar are cheaper than fighters, harder to destroy and never need a pilot. The other group answers that ground defences "
        "only deny the sky directly above them, and that a country with seventy-two fighters cannot afford to stop renewing "
        "them for a decade while it buys guns.",
        "The cabinet is asked for money before the war in Usea has run its course, and before anyone knows how it will end. It "
        "can fund a study that waits for the result. Or it can let both schools prepare competing programmes now, accepting "
        "that one of them will lose a budget fight it has been promised it might win. Either way, the air staff will argue "
        "about this war for years.",
    ), (
        Option('Fund a study and wait for the result.', (PP(20), Research('radar_tech', 0.5, 1))),
        Option('Let both schools draft programmes.', (XP('air', 20), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Azbekeranian response is gameplay', picture=2),
)

# --- branches ------------------------------------------------------------------------------------
POLITICS = Branch('pol', 'The Suspended Republic', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_frozen_calendar', 'The Frozen Election Calendar',
          "The Republic of Azbekerania keeps a general ballot every forty-eight months in its statutes, and the calendar is "
          "suspended. A National Administration governs under the democratic banner with almost no democrats behind it, while "
          "the reservists' leagues and the non-party civil establishment each claim about half the public. Reopening the "
          "calendar exposes the Administration to both camps, and nothing else in the republic moves until it is answered.",
          ('ballot', 'document'), reward=(Idea('suspended_calendar'), Event('calendar_question'))),
    Focus('pol_office_inventory', 'An Inventory of the Offices',
          "Before anyone argues over who should govern, the Administration needs to know what it governs with. Inspectors list "
          "every ministry, district office and city bureau, and find a civil service stretched thin across ten districts, "
          "strong in the capital and nearly absent in the towns. The inventory embarrasses departments that exist mainly as "
          "letterheads, and it hands every faction the same figures to fight over.",
          ('document', 'scales'), after=('pol_frozen_calendar',),
          reward=(PP(30), Tooltip('Opens three answers to the calendar question; only one can be taken.'))),
    Focus('pol_gazette', 'Print Every Decree',
          "The Administration has governed by decrees that were read aloud in the capital and seldom printed in the towns. A "
          "single official gazette, posted in every district office within a week of signature, makes the rules knowable to "
          "anyone who can read. It costs paper, a printing works and a staff of proof-readers. It also lets the leagues' "
          "lawyers find every contradiction between one decree and the next.",
          ('document', 'communications'), after=('pol_frozen_calendar',), reward=(Idea('official_gazette'),)),
    Focus('pol_convention_path', 'Delegates from Ten Districts',
          "The reform wing proposes that each of the ten districts elect delegates to a convention with one task: write an "
          "electoral law the republic will actually use. The democratic camp is nearly empty, so the delegates will come from "
          "the leagues and the civil establishment. The Administration accepts the gamble, because a law drafted by elected "
          "delegates cannot be waved away as one more decree.",
          ('assembly', 'ballot'), after=('pol_office_inventory',),
          exclusive=('pol_directorate_path', 'pol_league_path'),
          reward=(SwapIdea('suspended_calendar', 'convention_call'),)),
    Focus('pol_directorate_path', 'The Civil Service Keeps the Seals',
          "Senior officials argue that the civil service is the only institution both camps still obey, and that it should "
          "govern openly instead of sheltering behind an empty party label. Ministries would answer to a directorate of "
          "permanent secretaries, judged on results rather than votes. The establishment is reassured. The leagues call it "
          "government by filing cabinet and promise to empty the cabinets.",
          ('document', 'command'), after=('pol_office_inventory',),
          exclusive=('pol_convention_path', 'pol_league_path'),
          reward=(SwapIdea('suspended_calendar', 'clerks_rule'),)),
    Focus('pol_league_path', 'The Reserve Leagues Demand a Say',
          "Half the public belongs to or votes with the reservists' leagues, associations of men who served in the formations "
          "and believe the republic should be run with the discipline of a mobilisation table. Their leaders propose a national "
          "front that would merge the leagues with the state. Their parades are orderly and huge, and they already march in "
          "step with the army.",
          ('training', 'ballot'), after=('pol_office_inventory',),
          exclusive=('pol_convention_path', 'pol_directorate_path'),
          reward=(SwapIdea('suspended_calendar', 'league_pressure'),)),
    Focus('pol_convention_cabinet', 'Seat the Convention Cabinet',
          "The convention adopts its electoral law and chooses a cabinet answerable to the delegates until the first general "
          "ballot. Government passes from a single office to a body that can be removed. League delegates hold a large bloc "
          "and use it to delay budgets, while the civil establishment sulks in the ministries. Still, the cabinet holds a "
          "mandate the National Administration never had.",
          ('ballot', 'assembly'), after=('pol_convention_path',), cost=10,
          exclusive=('pol_directorate_seat', 'pol_front_seat'),
          reward=(Regime('district_convention'), Flag('path_convention'))),
    Focus('pol_directorate_seat', 'Install the Civil Directorate',
          "A directorate of permanent secretaries takes the government seals, with ministerial posts left vacant and their "
          "duties given to career officials. Elections stay suspended on the grounds that the calendar is under review, which "
          "it will be for years. Contracts are signed on time and budgets close on schedule. Nobody in the directorate has "
          "ever had to make a speech, and it shows.",
          ('command', 'document'), after=('pol_directorate_path',), cost=10,
          exclusive=('pol_convention_cabinet', 'pol_front_seat'),
          reward=(Regime('civil_directorate'), Flag('path_directorate'))),
    Focus('pol_front_seat', 'Proclaim the Reserve Front',
          "The leagues merge into a single reserve front that takes executive power by decree, led by a council of senior "
          "reserve officers. Parties are absorbed into the front or closed. Recruiting offices fill within a week and street "
          "crime falls. District notables and city chambers grow careful and quiet, because a government built on mobilisation "
          "tables will always need a reason to mobilise.",
          ('security', 'command'), after=('pol_league_path',), cost=10,
          exclusive=('pol_convention_cabinet', 'pol_directorate_seat'),
          reward=(Regime('reserve_front'), Flag('path_front'))),
    Focus('pol_first_ballot', 'The First General Ballot',
          "With the law in force, the convention cabinet calls a general ballot in all ten districts. Polling stations in the "
          "seven towns need trucks, clerks and sealed boxes that the Administration never bought. The leagues win many seats, "
          "the civil establishment wins more, and the democrats gain a foothold. The result settles little about policy and a "
          "great deal about how policy is now made.",
          ('ballot', 'scales'), after=('pol_convention_cabinet',),
          exclusive=('pol_results_tables', 'pol_muster_rolls'),
          reward=(SwapIdea('convention_call', 'ballot_republic'),)),
    Focus('pol_results_tables', 'Results Tables for Every Ministry',
          "The directorate publishes a results table for each ministry every quarter: roads graded, plants commissioned, rifles "
          "delivered, complaints answered. Ministries that miss their figures lose budget to those that meet them. Officials "
          "learn to game the tables at once, and the directorate learns to change the tables faster. The public finally sees "
          "what its government does, if not why.",
          ('document', 'economy'), after=('pol_directorate_seat',),
          exclusive=('pol_first_ballot', 'pol_muster_rolls'),
          reward=(SwapIdea('clerks_rule', 'results_tables'),)),
    Focus('pol_muster_rolls', 'Every Citizen on a Muster Roll',
          "The front extends the reserve muster roll from former soldiers to every adult, with a block warden in each street "
          "to keep it current. Mobilisation becomes a civic ritual and an instrument of surveillance in one stroke. Volunteers "
          "for road gangs and depot guards appear in numbers the Administration never managed. People missing from the roll "
          "discover that their absence has been noticed.",
          ('security', 'training'), after=('pol_front_seat',),
          exclusive=('pol_first_ballot', 'pol_results_tables'),
          reward=(SwapIdea('league_pressure', 'muster_state'),)),
    Focus('pol_settled', 'The Calendar Question Closed',
          "Whichever answer prevailed, Azbekerania stops arguing about who governs and starts arguing about what to govern for. "
          "Ministries know their masters, the districts know where to send petitions and foreign consulates know whom to call. "
          "An answer that half the country dislikes is still an answer, and it costs far less to live with than a calendar "
          "nobody is permitted to use.",
          ('peace', 'ballot'), after_any=('pol_first_ballot', 'pol_results_tables', 'pol_muster_rolls'),
          reward=(Flag('republic_settled'), Stability(0.04))),
))

DISTRICTS = Branch('dist', 'Three Cities and Seven Towns', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dist_seven_towns', 'The Seven Towns Without Roads',
          "Every civilian plant, arms plant, air base and paved road in Azbekerania sits in three districts: the Capital "
          "District, District A and District C. The other seven, B, D, E, F, H, I and J, hold most of the land and many of the "
          "people, but no plant, no surveyed resource and no paved road. Surveying them properly is the first step toward a "
          "country that is more than three cities.",
          ('civil', 'logistics'), reward=(Idea('three_city_state'), Event('town_survey'))),
    Focus('dist_line_halts', 'Halts on the Capital Line',
          "The republic's only railway runs from the Capital District across District D to District C and on to District A, "
          "carrying ore and fuel between the cities without stopping in between. Halts, sidings and a goods yard in District D "
          "let the line serve the country it crosses. The freight timetable slows for a season, and the city plants complain "
          "about every late wagon.",
          ('rail', 'civil'), after=('dist_seven_towns',), reward=(Build('infrastructure', 1, 417),)),
    Focus('dist_f_crossroads', 'District F, the Inland Crossroads',
          "District F is small, three provinces of plain and hill, and it is the only district that touches neither a foreign "
          "frontier nor the sea. Roads from the capital and from Districts D, E, H and I could all meet there. Grading them "
          "into one crossroads makes District F the natural home for depots, workshops and anything the republic would rather "
          "keep away from its borders.",
          ('logistics', 'bridge'), after=('dist_seven_towns',),
          reward=(Build('infrastructure', 2, 434), Flag('crossroads_open'))),
    Focus('dist_i_coast_road', 'A Road the Length of District I',
          "District I is the largest district on the map, eleven provinces of plain with a stretch of the southern coast at one "
          "end and the Yuktobanian frontier at the other, and it has no paved road at all. A single graded road along its "
          "length links coast, frontier and crossroads. It is a long and dull project that ties up the road crews for two full "
          "seasons.",
          ('logistics', 'civil'), after=('dist_seven_towns',), reward=(Build('infrastructure', 2, 477),)),
    Focus('dist_e_switchbacks', 'Switchbacks into District E',
          "District E is the hill and mountain country along a long stretch of the Yuktobanian frontier, and the steepest "
          "ground in Azbekerania, where every road must climb. Switchback roads and stone bridges open its valleys to trucks for the "
          "first time. The engineers need explosives and patience, the treasury needs patience too, and the frontier garrisons "
          "gain a way to reach their own posts.",
          ('bridge', 'tools'), after=('dist_seven_towns',), reward=(Build('infrastructure', 2, 421),)),
    Focus('dist_b_shore', 'The District B Shore Road',
          "District B lies on the coast beside District C, with plains that run to the Seterano frontier and no road better "
          "than a farm track. A shore road linking it to District C ends the district's isolation and gives the Seterano "
          "crossings a route to the rest of the country. It costs little and changes much, which is probably why it waited "
          "so long.",
          ('logistics', 'navy'), after=('dist_line_halts',), reward=(Build('infrastructure', 2, 387),)),
    Focus('dist_southern_tracks', 'Tracks Across the Southern Desert',
          "Districts H and J are hill and desert country along the frontier with Aemurraq, and District J is desert all the "
          "way down to its coast. Graded tracks link both to the Capital District for the first time. Sand fills them within a "
          "season unless crews keep clearing them, so the road ministry acquires a permanent budget line it will never be able "
          "to cut.",
          ('logistics', 'tools'), after=('dist_i_coast_road',),
          reward=(Build('infrastructure', 1, 493), Build('infrastructure', 1, 473))),
    Focus('dist_town_charters', 'Charters for the Seven Towns',
          "One answer to the imbalance gives each of the seven towns a charter: an elected council, its own works office and a "
          "fixed share of the revenue the three cities earn. The towns gain a voice and a budget line. The cities lose the "
          "freedom to spend their own revenue where they choose, and their chambers warn that charters have never built a "
          "single plant.",
          ('ballot', 'civil'), after_any=('dist_f_crossroads', 'dist_i_coast_road', 'dist_e_switchbacks'), cost=10,
          exclusive=('dist_city_wardens',),
          reward=(SwapIdea('three_city_state', 'town_charters'), Flag('towns_chartered'))),
    Focus('dist_city_wardens', 'Each City Wards Its Towns',
          "The other answer divides the seven towns among the three industrial cities, whose offices then run the towns' "
          "roads, schools and clinics as their own. It is efficient and quick, because the cities already have engineers and "
          "money. It also turns seven towns into dependencies of three cities they never chose, and the town notables will "
          "remember who took their offices.",
          ('command', 'civil'), after_any=('dist_f_crossroads', 'dist_i_coast_road', 'dist_e_switchbacks'), cost=10,
          exclusive=('dist_town_charters',),
          reward=(SwapIdea('three_city_state', 'city_wardens'), Flag('towns_wardened'))),
    Focus('dist_town_budgets', 'Town Budgets Voted Locally',
          "The chartered towns vote their first budgets, and most spend the money on the same three things: a clinic, a school "
          "and a water tower. None of it raises output. All of it keeps people in the towns rather than drifting to the three "
          "cities. The finance ministry grumbles about duplicated works, and the councils learn how far their revenue share "
          "really stretches.",
          ('medical', 'civil'), after=('dist_town_charters',), requires=(HasFlag('towns_chartered'),),
          reward=(Idea('town_clinics'),)),
    Focus('dist_engineer_circuit', 'City Engineers Ride the Circuit',
          "Engineers from the three cities ride a monthly circuit through the towns in their wardship, inspecting roads, wells "
          "and pumps and ordering repairs on the spot. Work is done quickly and to city standards. The towns are grateful and "
          "resentful in roughly equal measure, since every repair arrives with a city official who expects to be thanked for "
          "it.",
          ('tools', 'logistics'), after=('dist_city_wardens',), requires=(HasFlag('towns_wardened'),),
          reward=(Idea('engineer_circuits'),)),
    Focus('dist_crossroads_plant', 'A Plant at the Crossroads',
          "With roads meeting in District F, the ministry places the first plant ever built outside the three cities at the "
          "crossroads: a works for repairing and machining trucks, pumps and rail wagons. Skilled workers must be coaxed away "
          "from the cities, and their housing costs more than the lathes. If it works, the towns stop being a place industry "
          "merely drives through.",
          ('industry', 'civil'), after=('dist_f_crossroads',), requires=(HasFlag('crossroads_open'),),
          reward=(Build('industrial_complex', 1, 434),)),
    Focus('dist_revenue_formula', 'Revenue Shares for Ten Districts',
          "Whichever arrangement governs the towns, the ten districts sign a fixed formula for sharing revenue, road money and "
          "emergency stores for the rest of the decade. It is a table of percentages that nobody loves. It also ends the yearly "
          "quarrel over whether three cities subsidise seven towns or exploit them, so later governments can plan without "
          "reopening it.",
          ('scales', 'assembly'), after_any=('dist_town_budgets', 'dist_engineer_circuit'),
          reward=(Flag('districts_balanced'), Stability(0.03))),
))

INDUSTRY = Branch('ind', 'Rubber, Steel and Motor Works', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('ind_city_ledger', 'What the Three Cities Make',
          "Azbekerania's economy is three industrial districts, each with four civilian plants, two arms plants and its own "
          "oil, steel, aluminium and rubber. Nobody has ever added their figures together. One output ledger shows how much of "
          "each city's production leaves the country under the export law, how much stays at home and how much vanishes "
          "between plant gate and customs shed.",
          ('document', 'industry'), reward=(Idea('city_output_ledger'), Event('output_ledger'))),
    Focus('ind_rubber_study', 'The Rubber Question',
          "Rubber is the scarcest line in all three city ledgers: enough for tyres, hoses and seals if it stays at home, a minor "
          "export if it does not. Chemists and plant managers study how far synthetic blends can stretch it. The study takes a "
          "year of the best engineers' time, and it decides what the motor plants and the air arm can promise for the decade.",
          ('science', 'industry'), after=('ind_city_ledger',),
          reward=(Research('synth_resources', 0.5, 1), Flag('rubber_studied'))),
    Focus('ind_export_law', 'Hold to the Export Law',
          "The trade ministry argues that the export law serves the republic well: oil, steel and aluminium sold abroad at "
          "world prices for hard currency that buys what the plants cannot make. Keeping it means investing in the capital's "
          "wharves and in freight, not in new domestic industry. Critics answer that the seven towns will still be waiting for "
          "a factory when the oil runs out.",
          ('economy', 'navy'), after=('ind_city_ledger',), cost=10,
          exclusive=('ind_motor_path', 'ind_dispersal_path'),
          reward=(SwapIdea('city_output_ledger', 'hard_currency_exports'), Flag('model_export'))),
    Focus('ind_motor_path', 'A National Motor Works',
          "Plant managers in the three cities propose to turn their steel, aluminium and rubber into trucks, tyres and spare "
          "parts at home. The army wants transport before anything else, and the towns need trucks for the new roads. Protected "
          "prices would keep imported vehicles out for a decade. Exports fall in the meantime, and the trade ministry counts "
          "every cargo it loses.",
          ('industry', 'logistics'), after=('ind_city_ledger',), cost=10,
          exclusive=('ind_export_law', 'ind_dispersal_path'),
          reward=(SwapIdea('city_output_ledger', 'motor_programme'), Flag('model_motor'))),
    Focus('ind_dispersal_path', 'Move the Plants Away from the Line',
          "Two of the three industrial cities, District A and District C, sit on the Yuktobanian frontier. The general staff "
          "proposes to build every new plant inland, in District F, District H and the other towns, so that one bad night on "
          "the frontier cannot halve the republic's output. It is the most expensive way to grow and the safest, and the city "
          "chambers hate it.",
          ('industry', 'security'), after=('ind_city_ledger',), cost=10,
          exclusive=('ind_export_law', 'ind_motor_path'),
          reward=(SwapIdea('city_output_ledger', 'dispersal_plan'), Flag('model_dispersal'))),
    Focus('ind_capital_wharf', 'Bulk Wharves at the Capital Centre',
          "Exports leave through the capital's naval harbour, where warships and ore carriers queue for the same berths. A bulk "
          "wharf with ore sheds, fuel tanks and its own works yard separates trade from the navy and doubles loading capacity. "
          "It takes the last free industrial ground in the Capital District, so nothing else will be built there for a long "
          "time.",
          ('navy', 'industry'), after=('ind_export_law',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('ind_through_rates', 'Through Rates to the Wharf',
          "With the wharf open, the railway offers through rates from the plants of District A and District C straight to the "
          "capital's berths, with one bill of lading and no handling in between. Ore and metal reach the ships within a day. "
          "The towns along the line watch the trains pass faster than ever and stop no more often than they did before.",
          ('rail', 'economy'), after=('ind_capital_wharf',),
          reward=(Research('train_tech', 0.5, 1), SwapIdea('hard_currency_exports', 'through_rates'))),
    Focus('ind_truck_line', 'Truck Assembly on the Line',
          "The motor works places its first truck assembly hall in District D, beside the railway between the capital and "
          "District C, where steel and rubber arrive by rail and finished trucks leave by road. The first models copy foreign "
          "designs on local tyres. They are heavy, simple and repairable with hand tools, which is exactly what the reserve "
          "formations asked for.",
          ('logistics', 'rail'), after=('ind_motor_path',), reward=(Build('arms_factory', 1, 417),)),
    Focus('ind_tyre_plant', 'A Tyre and Hose Plant',
          "Tyres wear out faster than any other part of a truck, and every imported tyre costs hard currency. A tyre and hose "
          "plant in District B, close to the new shore road, turns city rubber and imported blends into tyres for the motor "
          "works and the army. The district gains its first factory jobs, and the small rubber export ends for good.",
          ('industry', 'tools'), after=('ind_motor_path',), requires=(HasFlag('rubber_studied'),),
          reward=(Build('industrial_complex', 1, 387),)),
    Focus('ind_district_h_works', 'Workshops in District H',
          "The dispersal programme's first site is District H, hill and desert country on the Aemurraq frontier and far from "
          "the Yuktobanian line. A machine shop and a small arms works rise beside the new desert tracks. Water must be trucked "
          "in and the workforce housed from nothing. The general staff calls the cost insurance; the city chambers call it "
          "exile.",
          ('security', 'tools'), after=('ind_dispersal_path',), reward=(Build('arms_factory', 1, 473),)),
    Focus('ind_district_f_works', 'Fabrication at the Crossroads',
          "A second dispersal site follows in District F, where a fabrication plant takes orders that would otherwise go to the "
          "frontier cities. The plant is small and its unit costs are high. In return, the republic now has industry in a "
          "district that no foreign army could reach without first crossing another district, and the staff sleeps a little "
          "better.",
          ('industry', 'logistics'), after=('ind_district_h_works',), reward=(Build('industrial_complex', 1, 434),)),
    Focus('ind_rolled_sheet', 'Aluminium Rolled at Home',
          "Aluminium is the third metal in every city ledger, and most of it leaves as ingots. A rolling line inside the "
          "capital's existing plants turns ingot into sheet for truck bodies, aircraft panels and roofing. It needs no new "
          "plant, only new machines and steadier electricity, and it gives the air arm spares that do not wait on import "
          "licences.",
          ('tools', 'industry'), after_any=('ind_through_rates', 'ind_truck_line', 'ind_district_f_works'),
          reward=(Research('industry', 0.5, 1), Idea('rolled_sheet'))),
    Focus('ind_output_census', 'An Output Census Each Quarter',
          "By the middle of the decade the three cities and the new sites file a common census of output, stocks and orders "
          "every quarter. Planners can finally see a shortage coming instead of reading about it in the newspapers. Plant "
          "managers resent the paperwork and fill it in anyway, because the census now decides who gets steel when there is "
          "not enough to go round.",
          ('document', 'scales'), after=('ind_rolled_sheet',), reward=(Idea('quarterly_census'),)),
))

RESERVE = Branch('res', 'The Continental Reserve', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('res_eight_formations', 'Muster the Eight Formations',
          "The army is eight infantry formations, each of six battalions with an engineer company, quartered at the Capital "
          "Centre and the two logistics centres in District A and District C. It is called a continental reserve, yet nobody "
          "has moved more than one formation at a time. A full muster tests the trucks, the rail timetable and the officers in "
          "one uncomfortable week.",
          ('training', 'command'), reward=(Idea('reserve_cadre'), Event('reserve_muster'))),
    Focus('res_firepower', 'Firepower Before Numbers',
          "The army's doctrine already prizes superior firepower over mass, which suits a volunteer force that cannot grow "
          "quickly. The staff writes that preference into training: more mortars and field guns per battalion, and gun crews "
          "drilled until they can fire without officers. Guns cost far more than riflemen and the procurement budget is small, "
          "so the formations will stay few, and heavy.",
          ('missile', 'training'), after=('res_eight_formations',),
          reward=(Research('artillery', 0.5, 1), XP('army', 15))),
    Focus('res_engineers', 'Engineers Who Build Roads',
          "Every formation carries an engineer company, and the seven towns need roads more than anything. Lending the "
          "engineers to the district road programme in peacetime keeps them practised and gives the towns skilled crews for "
          "nothing. Training for bridging under fire suffers. The army earns a reputation in the towns it never had, and the "
          "road ministry gains workers it does not pay.",
          ('bridge', 'training'), after=('res_eight_formations',),
          reward=(Research('engineers_tech', 0.5, 1), Build('infrastructure', 1, 417))),
    Focus('res_screen', 'Screen the Long Frontier',
          "One school wants the formations forward, a screen of battalions along the Yuktobanian frontier in Districts A, C, D, "
          "E and I, with the cities behind them. Any incursion meets soldiers within hours. The screen is thin everywhere and "
          "strong nowhere, and it puts most of the army within sight of a far larger neighbour, which that neighbour is bound "
          "to notice.",
          ('security', 'training'), after=('res_eight_formations',), cost=10, exclusive=('res_depth',),
          reward=(Idea('frontier_screen'), Flag('doctrine_screen'))),
    Focus('res_depth', 'Keep the Reserve in Depth',
          "The other school keeps the formations together at the inland crossroads and the capital, with only observation "
          "posts on the frontier. Nothing on the line is held for long, but the whole army can arrive anywhere within days by "
          "road and rail. The doctrine depends on roads still being built and on frontier districts accepting that they will "
          "be defended late.",
          ('rail', 'command'), after=('res_eight_formations',), cost=10, exclusive=('res_screen',),
          reward=(Idea('depth_reserve'), Flag('doctrine_depth'))),
    Focus('res_hill_battalions', 'Hill Battalions for District E',
          "The army already trains a few mountaineers, and District E is where they matter most: hills climbing to the "
          "republic's only mountain country, right on the frontier. Converting two battalions into hill troops, with mules, light guns and their own winter "
          "kit, gives the reserve a force for the only ground where trucks fail. The specialists cost more and are useful "
          "almost nowhere else.",
          ('training', 'tools'), after_any=('res_screen', 'res_depth'), reward=(Idea('hill_battalions'),)),
    Focus('res_rail_tables', 'Mobilisation Tables for the Line',
          "The railway from the capital to District A is the fastest way to move a formation, and nobody has written down how. "
          "Staff officers draw up tables for every formation, train and siding, and rehearse them at night so the freight "
          "timetable suffers least. The tables are dull, secret and essential. Once written, they also show how few wagons "
          "the republic owns.",
          ('rail', 'document'), after_any=('res_screen', 'res_depth'),
          reward=(Research('train_tech', 0.5, 2), Flag('rail_tables'))),
    Focus('res_frontier_barracks', 'Barracks Behind the Ridges',
          "Under the screen doctrine, battalions posted to District E need somewhere to live that is not a tent. Barracks in "
          "the valleys behind the ridges, with a road to each post, keep the screen in place through winter. Soldiers "
          "complain about the isolation and the cold. The frontier districts like having the army as neighbours, and the "
          "local shops like it even more.",
          ('security', 'civil'), after=('res_screen',), requires=(HasFlag('doctrine_screen'),),
          reward=(Build('infrastructure', 1, 421), XP('army', 10))),
    Focus('res_crossroads_depot', 'The Crossroads Depot',
          "Under the depth doctrine, the reserve needs a single place to draw ammunition, spares and fuel on its way to "
          "wherever it is sent. A depot and repair works at the District F crossroads holds them, with sidings for the trucks "
          "and a small ammunition line. It concentrates the republic's stores in one place, which the staff accepts as the "
          "price of speed.",
          ('logistics', 'security'), after=('res_depth',), requires=(HasFlag('doctrine_depth'), HasFlag('crossroads_open')),
          reward=(Build('arms_factory', 1, 434),)),
    Focus('res_paid_reserve', 'Paid Reservists, Called Each Year',
          "Former soldiers sign on as paid reservists who drill two weeks a year and answer a call-up within days. The reserve "
          "grows without touching the volunteer principle, and the formations could double within a month. The payroll is "
          "permanent and rises every year. Employers in the three cities complain each summer when their best workers vanish "
          "to the drill grounds.",
          ('medal', 'training'), after=('res_engineers',), exclusive=('res_town_companies',),
          reward=(Idea('paid_reserve'),)),
    Focus('res_town_companies', 'Town Companies for Local Defence',
          "Each of the seven towns raises a company of part-time volunteers to guard its own roads, bridges and depots, "
          "trained by the army's engineers. It costs little and brings the army into districts that have rarely seen it. The "
          "companies will defend their own towns stubbornly and decline to go anywhere else, which the general staff notes and "
          "the towns applaud.",
          ('security', 'civil'), after=('res_engineers',), exclusive=('res_paid_reserve',),
          reward=(Idea('town_companies'),)),
    Focus('res_staff_course', 'A Staff for Moving Armies',
          "A continental reserve is only as good as the staff that moves it. A small staff course in the capital trains officers "
          "in march tables, road control, supply and orders for whole formations rather than battalions. The first classes come "
          "from the logistics centres, where moving things is already a trade. The army gains planners who think in days and "
          "distances.",
          ('command', 'document'), after=('res_rail_tables',),
          reward=(XP('army', 25), Research('land_doctrine', 0.5, 1))),
    Focus('res_home_trucks', 'Trucks of the Army\'s Own Pattern',
          "With the motor works producing, the formations trade their imported trucks for domestic ones built to the army's own "
          "pattern. Every formation gains vehicles it can repair from its own stores. The first deliveries have weak axles and "
          "the drivers say so, loudly, until the second batch arrives. The reserve can now move by road without waiting for an "
          "import licence.",
          ('logistics', 'training'), after=('res_rail_tables',), requires=(HasFlag('model_motor'),),
          reward=(Idea('home_built_trucks'),)),
))

FRONTIER = Branch('fr', 'Beside Yuktobania', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('fr_three_frontiers', 'Mapping Three Frontiers',
          "Azbekerania's land frontiers run with three neighbours. Yuktobania, far larger than the republic, touches five "
          "districts, two of them home to industrial cities. Seterano borders District A and District B. Aemurraq meets the "
          "Capital District, District H and District J. The foreign ministry has never set one policy for all three, and the "
          "frontier districts have been left to improvise.",
          ('diplomacy', 'document'), reward=(Idea('frontier_unease'), Event('three_neighbours'))),
    Focus('fr_trade_path', 'Freight Across the Long Frontier',
          "One policy treats the long frontier as a market. Azbekerania sells steel, rubber and aluminium to buyers on the "
          "Yuktobanian side and buys machinery and fuel in return, through customs houses at the main crossings. Commerce makes "
          "incidents costly for both sides. It also ties the republic's plants to a single large customer whose decisions it "
          "cannot influence at all.",
          ('economy', 'diplomacy'), after=('fr_three_frontiers',), cost=10,
          exclusive=('fr_armed_path', 'fr_consult_path'),
          reward=(SwapIdea('frontier_unease', 'frontier_commerce'), Flag('posture_trade'))),
    Focus('fr_armed_path', 'Armed and Beholden to Nobody',
          "Another policy declares armed neutrality: no alliance, no special trade, and a reserve visibly ready to make any "
          "incursion costly. It costs nothing in foreign favours and a great deal in budget. Every neighbour knows exactly where "
          "the republic stands. Some of them will read readiness as hostility, however carefully the foreign ministry words "
          "its notes.",
          ('security', 'peace'), after=('fr_three_frontiers',), cost=10,
          exclusive=('fr_trade_path', 'fr_consult_path'),
          reward=(SwapIdea('frontier_unease', 'armed_neutrality'), Flag('posture_armed'))),
    Focus('fr_consult_path', 'Consult Seterano and Aemurraq',
          "A third policy looks first to the two neighbours other than Yuktobania. The foreign ministry offers Seterano and "
          "Aemurraq regular consultations on frontier incidents, smuggling and freight, with no treaty and no common army. "
          "Consultations commit nobody to anything and cost little. Whether the neighbours send anyone is their own decision; "
          "the republic can only keep the chairs out.",
          ('diplomacy', 'assembly'), after=('fr_three_frontiers',), cost=10,
          exclusive=('fr_trade_path', 'fr_armed_path'),
          reward=(SwapIdea('frontier_unease', 'neighbour_consultations'), Flag('posture_consult'))),
    Focus('fr_customs_houses', 'Customs Houses on the Frontier',
          "The trade policy needs crossings that clear freight in hours rather than days. Customs houses with weighbridges, "
          "sidings and warehouses go up at the main Yuktobanian crossings in District C. Clerks learn foreign forms and foreign "
          "languages. Smugglers lose their best years, and honest traders begin to treat the frontier as a place to do business "
          "rather than to wait.",
          ('economy', 'logistics'), after=('fr_trade_path',), requires=(HasFlag('posture_trade'),),
          reward=(Build('infrastructure', 1, 407),)),
    Focus('fr_listening_posts', 'Listening Posts in the Hills',
          "Armed neutrality needs eyes. Radar and radio listening posts on the hills of District E watch the frontier airspace "
          "and the roads beyond the line, reporting to the capital day and night. The equipment is imported and the crews take "
          "a year to train. Nothing they hear will be shared with anyone, which is the point of the policy and its main "
          "weakness.",
          ('radar', 'security'), after=('fr_armed_path',), requires=(HasFlag('posture_armed'),),
          reward=(Build('radar_station', 1, 421),)),
    Focus('fr_liaison_desk', 'A Liaison Desk for Incidents',
          "The consultations produce one practical result: a liaison desk in the capital, staffed at every hour, with a "
          "telephone number for each neighbour's frontier authorities in case they choose to call. Stray herds, lost patrols and "
          "smugglers' quarrels can be settled by telephone before they become diplomatic notes. The desk has no power of its "
          "own. It only makes misunderstanding slower.",
          ('communications', 'peace'), after=('fr_consult_path',), requires=(HasFlag('posture_consult'),),
          reward=(Idea('liaison_desk'),)),
    Focus('fr_attaches', 'Attaches in Three Capitals',
          "The republic has rarely posted soldiers to its embassies. Military attaches in the three neighbouring capitals give "
          "the general staff trained observers who can tell an exercise from a mobilisation and a rumour from a report. It "
          "costs three good officers the formations can ill spare. It also invites the neighbours to send attaches in return "
          "and to watch just as closely.",
          ('diplomacy', 'command'), after=('fr_three_frontiers',), reward=(Idea('attache_reports'),)),
    Focus('fr_district_d_shots', 'Shots Near a District D Crossing',
          "On a frontier this long, something eventually happens. A night patrol in District D exchanges shots with armed men "
          "who may be smugglers, deserters or something else, and nobody can say which side of the line the first shot came "
          "from. How the republic handles its first serious incident will define its frontier policy more than any declaration "
          "the ministry could print.",
          ('security', 'communications'), after_any=('fr_customs_houses', 'fr_listening_posts', 'fr_liaison_desk'),
          reward=(Event('frontier_incident'),)),
    Focus('fr_standing_orders', 'Frontier Rules in Writing',
          "After the first incident the government writes its frontier rules down: who may fire, who must be told, who may "
          "cross to talk and who signs what afterwards. The rules bind only Azbekeranian soldiers and officials, but they make "
          "the republic predictable to anyone watching. Officers on the line gain clarity and lose discretion, which some of "
          "them had enjoyed.",
          ('document', 'security'), after=('fr_district_d_shots',), reward=(Idea('frontier_standing_orders'),)),
))

AIR = Branch('air', 'Two Wings, Two Fields', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_two_wings', 'Seventy-Two Fighters on Two Fields',
          "The air arm flies seventy-two service fighters and twelve support aircraft, split evenly between the capital's air "
          "base and the field in District A. Each half has its own mechanics, spares and habits, and the two have never flown "
          "a joint exercise. Putting them under one command with one maintenance plan is cheap, overdue and resisted by both "
          "base commanders.",
          ('air', 'command'), reward=(Idea('split_wings'),)),
    Focus('air_field_c', 'An Air Base for District C',
          "District C holds a third of the republic's industry and a logistics centre on the Yuktobanian frontier, but no "
          "airfield. A new base on its plains gives the fighters a third field and puts the frontier city under its own air "
          "cover. It also parks combat aircraft within easy view of the frontier, which the foreign ministry asks to be "
          "described as purely defensive.",
          ('runway', 'industry'), after=('air_two_wings',), reward=(Build('air_base', 2, 407),)),
    Focus('air_field_a', 'Shelters at the District A Field',
          "The District A field lies in forest and hill country close to two frontiers, with its aircraft parked in the open. "
          "Earth-covered shelters, a longer runway and a fuel line from the logistics centre let its half of the wing survive "
          "a surprise and fly again within hours. The forest hides the shelters well, and the runway extension takes a great "
          "deal of the forest.",
          ('runway', 'shelter'), after=('air_two_wings',), reward=(Build('air_base', 2, 347),)),
    Focus('air_radar_plot', 'One Radar Plot for Both Wings',
          "The two wings have never shared a picture of the sky. Two radar sets, one beside the capital air base and one at the "
          "District A field, feed a single plotting room in the Capital Centre. Pilots scramble toward a contact instead of "
          "toward a hope. The plot covers the cities well and the towns poorly, and the staff keeps a list of every gap.",
          ('radar', 'air'), after_any=('air_field_c', 'air_field_a'),
          reward=(Build('radar_station', 1, 0), Build('radar_station', 1, 347))),
    Focus('air_one_field', 'Gather the Wing at the Crossroads',
          "One school wants both halves of the wing moved to a single new base at the District F crossroads, out of sight of "
          "every frontier and within reach of all of them. Concentration simplifies maintenance and training and makes the "
          "wing harder to surprise. It also leaves the cities with fighters an hour away instead of overhead, and the city "
          "chambers protest.",
          ('runway', 'command'), after_any=('air_field_c', 'air_field_a'), cost=10, exclusive=('air_town_strips',),
          reward=(Build('air_base', 2, 434), SwapIdea('split_wings', 'single_wing'))),
    Focus('air_town_strips', 'Fighter Strips in the Towns',
          "The other school scatters the fighters across rough strips in the towns, a pair here and four there, so that no "
          "single blow can ground the arm. Pilots learn to fly from grass and dirt, and mechanics learn to work from trucks. "
          "Readiness falls and spares go missing between strips. Whatever survives a first night, though, will still fly the "
          "next morning.",
          ('runway', 'civil'), after_any=('air_field_c', 'air_field_a'), cost=10, exclusive=('air_one_field',),
          reward=(Build('air_base', 1, 477), Build('air_base', 1, 387), SwapIdea('split_wings', 'scattered_strips'))),
    Focus('air_support_flights', 'Support Aircraft for the Formations',
          "The twelve support aircraft have always flown as an afterthought to the fighters. Assigning them to the reserve "
          "formations, with radio teams on the ground and joint exercises each season, gives the army its only air support and "
          "the support pilots a purpose. The fighter commanders lose aircraft they had been quietly using as trainers, and "
          "they notice.",
          ('air', 'training'), after_any=('air_one_field', 'air_town_strips'), reward=(Idea('support_flights'),)),
    Focus('air_tyres_seals', 'Tyres and Seals for the Wings',
          "Aircraft are grounded more often by worn tyres and leaking hydraulic seals than by anything an enemy does. The rubber "
          "study gives the air arm's workshops recipes for both, from the republic's own rubber and imported blends. Home-made "
          "seals need replacing sooner than foreign ones, but they arrive in days instead of months, and readiness climbs with "
          "every delivery.",
          ('tools', 'air'), after_any=('air_one_field', 'air_town_strips'), requires=(HasFlag('rubber_studied'),),
          reward=(XP('air', 20), Research('industry', 0.5, 1))),
    Focus('air_night_pairs', 'Night Alert Pairs',
          "The fighters have only ever flown in daylight from either field. Training pairs of pilots to stand alert at night, "
          "take off on radar warning and land on lit runways turns the arm into a round-the-clock service. Night flying costs "
          "aircraft in its first year, as it does everywhere. The capital's sky stops being empty between dusk and dawn.",
          ('air', 'radar'), after=('air_radar_plot',), reward=(Idea('night_alert'),)),
))

SEA = Branch('sea', 'The Maritime Service', 1993, 'FOCUS_FILTER_NAVY_XP', (
    Focus('sea_two_escorts', 'Two Escorts and Sixty Convoys',
          "The maritime service is two coastal escorts at the capital's naval harbour and sixty merchant hulls that carry the "
          "republic's exports. Its coast comes in two pieces: one shared by the Capital District, District C and District B, "
          "the other along District I and District J. The service has never patrolled the second. Counting what it owns comes "
          "before deciding what it is for.",
          ('navy', 'document'), reward=(Idea('two_escort_service'),)),
    Focus('sea_southern_yard', 'A Yard on the Southern Coast',
          "All repair work happens at the capital, so any ship on the southern coast must sail round to reach it. A small yard "
          "on the District I shore, with one slip and a repair basin, gives the southern coast its own service base and the "
          "merchant fleet a second place to haul out. Shipwrights must be recruited from the capital, and few volunteer.",
          ('navy', 'tools'), after=('sea_two_escorts',), reward=(Build('dockyard', 1, 477),)),
    Focus('sea_j_landing', 'A Landing for District J',
          "District J's desert coast has no harbour worth the name, only open beaches. A concrete landing with a road to the "
          "desert tracks lets coastal ships unload supplies for the southern towns without the long haul from the capital. It "
          "is a modest work, mostly concrete and sand. It also gives the maritime service a refuelling point on the southern "
          "coast.",
          ('navy', 'logistics'), after=('sea_southern_yard',), reward=(Build('infrastructure', 1, 493),)),
    Focus('sea_convoy_escort', 'Escorts with the Ore Convoys',
          "One doctrine keeps the two escorts with the merchant convoys on their outward legs, so the export trade is never "
          "unguarded where it is most exposed. The convoys sail on time and their insurers notice. The coasts themselves are "
          "watched by nobody while the escorts are away, and the escort crews spend more nights at sea than any other sailors "
          "in the republic.",
          ('navy', 'logistics'), after=('sea_two_escorts',), cost=10, exclusive=('sea_coast_watch',),
          reward=(Idea('ore_convoy_escorts'),)),
    Focus('sea_coast_watch', 'Watch the Coasts from Ashore',
          "The other doctrine keeps the escorts at home and watches both coasts from land: coastwatchers on the headlands, "
          "radio huts on the beaches, a radar set on the District I shore and a plotting table at the naval harbour. Merchant "
          "convoys sail alone beyond the horizon. Both coasts, however, are watched every hour of the year.",
          ('radar', 'navy'), after=('sea_two_escorts',), cost=10, exclusive=('sea_convoy_escort',),
          reward=(Idea('coast_watchers'), Build('radar_station', 1, 477))),
    Focus('sea_escort_design', 'An Escort of Our Own Design',
          "The capital's two dockyards have built merchant hulls and repaired the escorts, but never designed a warship. A "
          "simple coastal escort to the service's own specification, slow but seaworthy and cheap to crew, teaches the yard "
          "and the naval staff more than any purchase could. The first hull takes twice as long as planned; the second, only "
          "half again as long.",
          ('navy', 'industry'), after_any=('sea_convoy_escort', 'sea_coast_watch'),
          reward=(Research('naval_equipment', 0.5, 1), XP('navy', 15))),
    Focus('sea_lifeboats', 'Lifeboat Stations on Both Coasts',
          "Nobody in Azbekerania is responsible for a ship in trouble off its own coast; the escorts are too few and usually "
          "elsewhere. Lifeboat stations at the capital, in District C and on the southern coast, crewed by volunteers and paid "
          "for by a levy on cargo, give both coasts a rescue service. Masters pay a small fee per voyage and stop complaining "
          "after the first winter.",
          ('navy', 'medical'), after_any=('sea_convoy_escort', 'sea_coast_watch'), reward=(Idea('lifeboat_stations'),)),
))

BELKA = Branch('bw', 'The Ustio Lesson', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_dispatches', 'Dispatches from the Belkan War',
          "In March 1995 war breaks out around Belka. Azbekerania is far from the fighting and party to none of it, but the "
          "general staff reads every dispatch as if it were addressed to the republic. A small country with larger neighbours "
          "is watching how a war among bigger powers treats the states caught between them. The newspapers ask whether the "
          "reserve is ready; so does the cabinet.",
          ('communications', 'command'), requires=(After('1995.3.25'),),
          reward=(Event('belkan_dispatches'), TimedIdea('war_nerves', 365))),
    Focus('bw_ustio_week', 'The Week That Took Ustio',
          "By 30 March 1995 nearly all of the Republic of Ustio has fallen under Belkan control, within days of the war "
          "beginning. For the Azbekeranian staff the lesson is uncomfortable and precise: a small republic can lose almost all "
          "of its ground in less than a week. Every plan the reserve owns is reopened, and the planners stop sleeping at "
          "home.",
          ('document', 'security'), after=('bw_dispatches',), requires=(After('1995.3.30'),),
          reward=(Flag('ustio_studied'), PP(15))),
    Focus('bw_hold_cities', 'Hold the Frontier Cities at Any Cost',
          "The first answer says the republic cannot lose District A or District C even for a week, because together they hold "
          "two thirds of its industry. Every formation would be committed to their defence from the first hour, with fieldworks "
          "around both cities and stores for a siege. The plan protects the plants and leaves the seven towns to fend for "
          "themselves.",
          ('security', 'industry'), after=('bw_ustio_week',), cost=10, exclusive=('bw_trade_ground', 'bw_worth_helping'),
          reward=(Idea('city_bastions'),)),
    Focus('bw_trade_ground', 'Trade Ground for Time',
          "The second answer accepts that frontier districts may be lost for a while and plans to keep the army whole rather "
          "than spend it at the line. Formations would fall back on the crossroads and the capital, dropping bridges behind "
          "them, and strike when the attacker is stretched. It is cold arithmetic, and the frontier districts are not "
          "expected to like it.",
          ('command', 'logistics'), after=('bw_ustio_week',), cost=10, exclusive=('bw_hold_cities', 'bw_worth_helping'),
          reward=(Idea('elastic_plan'),)),
    Focus('bw_worth_helping', 'Become Worth Helping',
          "The third answer notes that Ustio did not resist alone: within days it entered an alliance with Osea. Azbekerania "
          "has no alliance and this focus creates none. It invests instead in being easy to help: foreign officers invited to "
          "exercises, airfields built to common standards and staff officers who speak the languages of possible friends.",
          ('diplomacy', 'runway'), after=('bw_ustio_week',), cost=10, exclusive=('bw_hold_cities', 'bw_trade_ground'),
          requires=(After('1995.4.1'),), reward=(Idea('worth_helping'),)),
    Focus('bw_directus', 'The Liberation of Directus',
          "In May 1995 the Allied Forces liberate Ustio's capital, and the staff revises its notes again. Ground lost in days "
          "was regained in weeks, but by allied forces rather than by Ustio alone. Planners in the Capital Centre draw the conclusion "
          "for a republic of eight formations: any plan must hold long enough for the world to decide whether it cares.",
          ('document', 'command'), after=('bw_dispatches',), requires=(After('1995.5.13'), HasFlag('ustio_studied')),
          reward=(Idea('ustio_notes'),)),
    Focus('bw_waldreich', 'Seven Flashes in the Waldreich',
          "In this campaign the war has turned nuclear: the Belkan Army has used seven nuclear devices in the Waldreich "
          "Mountains. Whether anything carried on the wind as far as Azbekerania is a question only instruments can answer, "
          "and the republic owns almost none. It buys radiation counters for every district office and trains the engineer "
          "companies to read them, at a price nobody argues about.",
          ('science', 'medical'), after=('bw_dispatches',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(Idea('fallout_counters'),)),
    Focus('bw_lumen_treaty', 'The Staff War Room Closes',
          "A treaty signed in Lumen on 20 June 1995 ends the Belkan War. The staff closes its war room, the newspapers move on "
          "and the cabinet asks whether the emergency spending can stop. The staff replies that the war ended but its lesson "
          "did not, and asks to keep its revised plans funded. The cabinet splits the difference, as cabinets generally do.",
          ('peace', 'document'), after=('bw_dispatches',), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_nerves'), Stability(0.02))),
    Focus('bw_thick_screen', 'The Screen Thickened',
          "The Belkan War convinced the frontier school that a screen too thin to hold is only a tripwire. The staff thickens it "
          "where it matters most: more battalions around District A and District C, fewer elsewhere, and reserve stocks moved "
          "closer to the line. The screen grows strong where the plants are and frankly symbolic where the towns are.",
          ('security', 'logistics'), after_any=('bw_hold_cities', 'bw_trade_ground', 'bw_worth_helping'),
          requires=(HasFlag('doctrine_screen'),), reward=(Build('infrastructure', 1, 347), XP('army', 15))),
    Focus('bw_marked_bridges', 'Bridges Marked for Demolition',
          "The depth school takes from the Belkan War the conviction that an attacker must be slowed before the reserve "
          "strikes. Engineers survey every bridge and culvert between the frontier and the crossroads, mark each for "
          "demolition and store the charges nearby under guard. It is grim, cheap work, and the frontier districts learn which "
          "bridges their own army means to blow.",
          ('bridge', 'security'), after_any=('bw_hold_cities', 'bw_trade_ground', 'bw_worth_helping'),
          requires=(HasFlag('doctrine_depth'),), reward=(Idea('demolition_plans'),)),
    Focus('bw_belkan_victory', 'Reading a Belkan Victory',
          "Where the war has ended with Belka victorious, the staff takes the gloomiest reading available: the republic should "
          "count on nobody's rescue but its own. The cabinet agrees to hold the reserve at higher readiness for a year. "
          "Neighbours notice the extra drills and the night convoys, and their attaches ask polite questions that the ministry "
          "answers politely.",
          ('training', 'security'), after=('bw_lumen_treaty',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('raised_readiness', 365),)),
    Focus('bw_belkan_defeat', 'Reading a Belkan Defeat',
          "Where the war has ended in Belkan defeat, the staff concludes that outside help can matter if a defender holds long "
          "enough to receive it. Plans keep their hope of rescue, and the cabinet trims the emergency budget. Cautious officers "
          "write dissenting memoranda about the risks of relying on others, which are filed with great care and read by almost "
          "nobody.",
          ('document', 'peace'), after=('bw_lumen_treaty',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(PP(25), Research('land_doctrine', 0.5, 1))),
))

ULYSSES = Branch('uly', 'Ulysses Over the Ten Districts', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('uly_no_miss', 'The Asteroid Will Not Miss',
          "The warning of December 1994 became a certainty in April 1996, when the impact of Ulysses was announced to the "
          "world. Where fragments will fall is unknown. Azbekerania has a capital on the sea, a coastal city on the frontier, "
          "seven towns with few roads and a reserve trained only for war. Every district office telephones the capital to ask "
          "what it should do.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),),
          reward=(Idea('impact_committee'), Event('impact_announced'))),
    Focus('uly_galleries', 'Galleries in the District E Hills',
          "Engineers propose galleries cut into the hills of District E, which rise to the republic's only mountain country, "
          "deep enough to shelter people from the capital and the cities for weeks. The galleries would protect "
          "everyone who reached them and nobody who did not. The work is slow, the hills sit on the frontier and the road there "
          "is barely finished.",
          ('shelter', 'tools'), after=('uly_no_miss',), cost=10, exclusive=('uly_thin_coast', 'uly_rescue_corps'),
          reward=(Idea('hill_galleries'),)),
    Focus('uly_thin_coast', 'Thin Out the Coastal Cities',
          "Planners propose moving families, records and spare machinery from the coast at the capital and District C to the "
          "inland towns before the impact, so that anything striking the coast finds fewer people in its path. It is cheap in "
          "concrete and expensive in politics. The towns must house strangers, and the cities must send their own families "
          "away.",
          ('refugees', 'logistics'), after=('uly_no_miss',), cost=10, exclusive=('uly_galleries', 'uly_rescue_corps'),
          reward=(Idea('coastal_thinning'),)),
    Focus('uly_rescue_corps', 'The Reserve Becomes a Rescue Corps',
          "The general staff offers the formations themselves: eight formations of soldiers with trucks, engineers and radios, "
          "retrained to dig, clear, carry and feed rather than to fight. The army becomes a rescue corps for as long as the "
          "danger lasts. Its readiness for war falls measurably, and the frontier school records its objection in writing.",
          ('medical', 'training'), after=('uly_no_miss',), cost=10, exclusive=('uly_galleries', 'uly_thin_coast'),
          reward=(Idea('rescue_corps'),)),
    Focus('uly_fill_silo', 'Fill the Capital Fuel Silo',
          "The capital's fuel silo is the republic's only strategic store of fuel, and under the civilian economy it is rarely "
          "full. Filling it before the impact means buying abroad at high prices or holding back exports when they would earn "
          "most. The trade ministry objects to both. Every plan for the night itself, however, assumes trucks and generators "
          "that will need fuel.",
          ('logistics', 'shelter'), after_any=('uly_galleries', 'uly_thin_coast', 'uly_rescue_corps'),
          reward=(Idea('full_silo'),)),
    Focus('uly_evacuation_trains', 'Evacuation Trains on the Only Line',
          "The reserve's mobilisation tables already say how to move eight formations by rail. Rewritten for families instead "
          "of battalions, they become evacuation timetables for the only line, from the capital through District D to District "
          "C and District A. The halts in District D become reception points. The tables are rehearsed once by night and mostly "
          "work.",
          ('rail', 'refugees'), after=('uly_fill_silo',), requires=(HasFlag('rail_tables'),),
          reward=(Build('infrastructure', 1, 417),)),
    Focus('uly_convention_debate', 'The Convention Debates the Sky',
          "The convention cabinet takes the impact to the delegates, who spend a week arguing over which districts get shelters "
          "first. The debate is slow, bitter and broadcast in full. It ends in a published plan that every district has voted "
          "for and none fully likes. People who heard the argument trust the plan more than a decree could ever have made them.",
          ('ballot', 'shelter'), after=('uly_fill_silo',), requires=(HasFlag('path_convention'),),
          reward=(Idea('voted_shelter_plan'),)),
    Focus('uly_ration_cards', 'Ration Cards Printed in Advance',
          "The directorate treats the impact as an administrative problem and solves it administratively: ration cards for every "
          "household, printed and filed in each district office, ready to issue the moment supplies fail. Nobody will queue for "
          "them in a panic, because they already exist. The cards also record every household's members and address, which "
          "some households find more alarming than the asteroid.",
          ('document', 'civil'), after=('uly_fill_silo',), requires=(HasFlag('path_directorate'),),
          reward=(Idea('printed_rations'),)),
    Focus('uly_block_wardens', 'Block Wardens for the Shelters',
          "The reserve front assigns its block wardens to the shelters: each warden knows who lives in each street, which "
          "shelter they go to and in what order. The drills are punctual and complete. Families whose loyalty the front doubts "
          "find their places at the back of the list, and they learn not to complain where a warden might hear them.",
          ('security', 'shelter'), after=('uly_fill_silo',), requires=(HasFlag('path_front'),),
          reward=(Idea('warden_shelters'),)),
    Focus('uly_town_radios', 'A Radio in Every Town Office',
          "The seven towns hear national news days late, by newspaper or rumour. Under the revenue formula, every town office "
          "receives a radio set, a generator and an operator trained to relay bulletins and report damage. The sets cost "
          "little; the operators cost more. Whatever happens on the night, the capital will at least hear about it from the "
          "towns themselves.",
          ('communications', 'civil'), after=('uly_fill_silo',), requires=(HasFlag('districts_balanced'),),
          reward=(Idea('town_radios'),)),
    Focus('uly_july_night', 'The Eighth of July, 1999',
          "On 8 July 1999 Ulysses passes through the Roche limit of the Earth. In Azbekerania the formations wait beside their "
          "trucks in the capital and the cities, the evacuation trains stand in the District D sidings and every district "
          "office keeps a radio operator awake. Nobody knows yet where anything will fall. Everyone knows these nights will be "
          "remembered.",
          ('meteor', 'communications'), after=('uly_fill_silo',), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('uly_sky_bill', 'What the Sky Cost at Home',
          "When the sky clears, the government counts what the impact years cost at home: money spent on shelters and stores, "
          "plants idled for drills, exports held back and formations kept from training. Whatever fell elsewhere, the domestic "
          "bill is real and must be paid. The ministries draw up one account, and the cabinet decides which emergency measures "
          "to keep.",
          ('scales', 'meteor'), after=('uly_july_night',), reward=(RemoveIdea('impact_committee'), Stability(0.03))),
))

CENTURY = Branch('cen', 'Ten Districts at the Millennium', 1999, 'FOCUS_FILTER_RESEARCH', (
    Focus('cen_census', 'The Census of the Year 2000',
          "The turn of the century gives the government a reason to count everything again: people, plants, roads, trucks, "
          "rifles and debts in all ten districts. The surveys of the early nineties found three cities and seven empty towns. "
          "The new count will show whether a decade of roads, plants and arguments has changed that, and every faction is "
          "already rehearsing its explanation.",
          ('document', 'civil'), requires=(After('2000.1.1'),), reward=(Idea('millennium_census'),)),
    Focus('cen_cleared_orbit', 'Satellites Over a Cleared Orbit',
          "In October 1999 Osea and Yuktobania began converting the Arkbird into a platform for clearing debris from satellite "
          "orbits, and in this campaign the conversion is finished. With the orbits swept, the republic's broadcasting and "
          "telephone engineers can rent satellite capacity with some confidence. Azbekerania contributed nothing to the work "
          "and benefits anyway, as small states often do.",
          ('satellite', 'communications'), after=('cen_census',), requires=(HasGlobal('ac_sp_arkbird_complete'),),
          reward=(Research('electronics', 0.5, 1), Idea('satellite_rentals'))),
    Focus('cen_railgun_study', 'Railguns Over a Distant Desert',
          "In the summer of 2003 war comes to Usea: Erusea seizes Stonehenge in San Salvacion and turns its railguns on the "
          "sky. Usea is far from the ten districts, but the air staff studies the war closely, because it asks whether a small "
          "air force can be denied the sky by guns on the ground. The cabinet wonders how long two small wings would last.",
          ('missile', 'radar'), after=('cen_census',), requires=(HasGlobal('ac_ucw_war_started'),),
          reward=(Event('usean_lesson'),)),
    Focus('cen_city_batteries', 'Guns and Radar Before Fighters',
          "One lesson is that air defence from the ground is cheaper than fighters and harder to destroy. The republic buys "
          "anti-aircraft guns and fire-control radar for the three cities and puts the next fighter purchase on hold. The "
          "cities sleep better under their batteries. The pilots, told to wait another decade for new aircraft, sleep rather "
          "worse.",
          ('missile', 'industry'), after=('cen_railgun_study',), cost=10, exclusive=('cen_wing_renewal',),
          reward=(Build('radar_station', 1, 407), Idea('city_batteries'))),
    Focus('cen_wing_renewal', 'Renew Both Fighter Wings',
          "The other lesson is that guns deny only the sky above themselves, and that fighters remain the one weapon that can "
          "go where the danger is. The cabinet funds a renewal of both wings, with new airframes over five years and pilots "
          "trained to fight in defended airspace. It is the costliest decision of the decade, and every year of it will be "
          "argued.",
          ('air', 'industry'), after=('cen_railgun_study',), cost=10, exclusive=('cen_city_batteries',),
          reward=(Research('air_doctrine', 0.5, 2), Idea('wing_renewal'))),
    Focus('cen_truck_exports', 'Wartime Orders for Our Trucks',
          "Armies at war use up trucks and tyres faster than any peacetime market, and buyers far from Usea start placing "
          "orders wherever they find capacity. The motor works can sell abroad for the first time, at prices that repay its "
          "protected decade. The reserve formations, promised the next batch, watch the trucks leave by sea and write to the "
          "cabinet.",
          ('logistics', 'economy'), after=('cen_railgun_study',), requires=(HasFlag('model_motor'),),
          reward=(TimedIdea('export_truck_orders', 540),)),
    Focus('cen_metal_prices', 'Ore Cargoes at Wartime Prices',
          "War raises the price of every metal, and the export path left the republic ready to sell into that market. Ore and "
          "aluminium leave the capital's wharves at prices nobody had seen in years. The trade ministry reports record "
          "receipts. The towns ask why record receipts never seem to reach them, and the leagues' newspapers print the question "
          "weekly.",
          ('economy', 'navy'), after=('cen_railgun_study',), requires=(HasFlag('model_export'),),
          reward=(TimedIdea('war_ore_prices', 540),)),
    Focus('cen_inland_overflow', 'Inland Plants Take the Overflow',
          "Foreign demand swells while the war lasts, and the city plants cannot fill every order. The dispersed works in "
          "District H and District F take the overflow, running second shifts for the first time. Their unit costs fall as "
          "volume rises. For once the dispersal programme looks less like insurance and more like a sound investment.",
          ('industry', 'tools'), after=('cen_railgun_study',), requires=(HasFlag('model_dispersal'),),
          reward=(TimedIdea('inland_overflow', 540),)),
    Focus('cen_accord_dividend', 'The War That Never Came',
          "In this campaign the war in Usea never began: the quarrel over refugees and the railgun battery ended in a "
          "continental accord. Insurers relax, metal prices sag and the air staff's study of ground defences loses its urgency. "
          "The cabinet spends the savings on roads in District B, a district that never had a lobby as effective as a distant "
          "war.",
          ('peace', 'logistics'), after=('cen_census',), requires=(HasGlobal('ac_ucw_war_averted'),),
          reward=(Build('infrastructure', 1, 387),)),
    Focus('cen_stonehenge_broken', 'The Batteries at Stonehenge Broken',
          "In this campaign Stonehenge has been destroyed, and with it the strongest argument that guns on the ground can own "
          "the sky. The air staff revises its study: ground defences can be broken by an air force willing to pay for it. Both "
          "schools in the cabinet claim the result proves them right, which keeps the budget quarrel alive for another year.",
          ('missile', 'air'), after=('cen_railgun_study',), requires=(HasGlobal('ac_ucw_stonehenge_destroyed'),),
          reward=(Research('air_doctrine', 0.5, 1), XP('air', 15))),
    Focus('cen_reserve_handover', 'The Reserve Changes Generations',
          "By 2005 the officers who mustered the eight formations in the early nineties are retiring, and the reserve passes to "
          "men who learned their trade in its newer tables, depots and roads. The handover is marked by a parade in the Capital "
          "Centre and a quieter review of what the republic still lacks. Whoever governs next inherits an army that knows its "
          "own country.",
          ('medal', 'training'), after=('cen_census',), requires=(HasFlag('republic_settled'), After('2005.1.1')),
          reward=(Stability(0.03), WarSupport(0.03),
                  Tooltip('Ends the 1991 to 2005 programme; later decades are not yet written.'))),
))

BRANCHES = (POLITICS, DISTRICTS, INDUSTRY, RESERVE, FRONTIER, AIR, SEA, BELKA, ULYSSES, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('call_reserve_class', 'Call a Reserve Class to Drill',
                'One year group of reservists reports for a month of drill, at the cost of their wages and their employers\' '
                'patience. Repeatable once a year.',
                35, (TimedIdea('class_called', 120), XP('army', 10)), requires=(Completed('res_eight_formations'),), cooldown=365),
    DecisionDef('grade_district_h', 'Grade the District H Tracks',
                'Road crews grade and gravel the side tracks off the desert route into District H. A one-time works programme.',
                60, (Build('infrastructure', 1, 473),), requires=(Completed('dist_southern_tracks'),)),
    DecisionDef('release_silo_fuel', 'Release Fuel from the Silo',
                'Sells part of the capital silo at controlled prices to calm a fuel shortage. Once only; refilling takes years.',
                50, (Stability(0.03), TimedIdea('silo_release', 180)), requires=(Completed('uly_fill_silo'),)),
    DecisionDef('frontier_liaison_day', 'Hold a Frontier Liaison Day',
                'District officials meet across the line to settle grazing, smuggling and lost-property grievances. Repeatable '
                'every six months.',
                25, (TimedIdea('liaison_calm', 90),), requires=(Completed('fr_three_frontiers'),), cooldown=180),
    DecisionDef('second_truck_hall', 'Open a Second Truck Hall',
                'Funds a second assembly hall beside the first in District D. A one-time charge on the motor programme.',
                90, (Build('arms_factory', 1, 417),), requires=(Completed('ind_truck_line'),)),
    DecisionDef('joint_wing_exercise', 'Exercise Both Wings Together',
                'Both fighter wings and the radar plot fly a week-long joint exercise. Repeatable once a year; it burns fuel.',
                30, (TimedIdea('wing_exercise', 90), XP('air', 10)), requires=(Completed('air_two_wings'),), cooldown=365),
)
