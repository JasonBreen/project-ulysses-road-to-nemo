"""Silvonia (ESN): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections suspended, neutrality 48 and fascism 50 percent popularity,
tech_mountaineers and early_fighter), the unnamed starting office, the ten 1991 states with
their neutral district captions and hub names, the map facts read from map/definition.csv,
map/provinces.bmp and map/railways.txt, and the global flags other mod scripts already set.
Official: ACES Chronicle rows used only as date anchors for distant pressures, each cited by
its exact key. Everything else, including every Silvonian choice, office, idea, building,
decision and event, is provisional gameplay built on the world-start role of territorial
air defence.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='ESN', name='Silvonia', root='world', package='esn',
                  themes=('radar', 'air', 'rail'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots; '
           'technology including tech_mountaineers, tech_engineers, early_fighter and basic_train; grand doctrines '
           'superior_firepower, fleet_in_being and operational_integrity. The starting leader is the unnamed National '
           'Administration office (ESN_ac_government_office, centrism), whose description says its 1991 holder has not been '
           'established. The tree never names a holder.',
           'mod/2985041246/history/countries/ESN - Silvonia.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 45, 79, 202, 205, 227 (capital), 249, 484, 578, 583 and 588, captioned Silvonia District A, '
           'B, C, D, Capital District, F, G, H, I and J by the neutral regional labels (canonical regional mapping '
           'unestablished). Victory points Silvonia Capital Centre (3418) and Logistics Centres 4222 (District B), 2039 '
           '(District F) and 9655 (District A). The Capital District (large city, four hill provinces) holds four civilian and '
           'two military factories, the only air base and the fuel silo; Districts B (mountain and hills) and F (jungle and '
           'hills, coastal) each hold three civilian and two military factories; all three carry oil, aluminium, rubber and '
           'steel. District A (jungle, plains and marsh, coastal) holds the naval base and two dockyards. Districts C (17 '
           'provinces, mostly plains), D (hills and mountain), G (hills), H (26 provinces, mostly desert), I (mountain and '
           'hills) and J (hills and plains) are towns with no buildings, infrastructure or resources. Land neighbours from '
           'map/provinces.bmp: Yuktobania (B, H), Kaluga (B, D, I), Verusa (C, F, H), Sfaenland (A, G) and Luremia (G, I); '
           'the Capital District and District J touch no frontier. Railways (map/railways.txt) run Capital District - District '
           'B, and Capital District - District J, where they split for District A and District F. No other place is named.',
           'mod/2985041246/history/states/45-State_45.txt and the nine other ESN state files; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role territorial air defense; 10 civilian, 6 military and 2 naval '
           'factories; seven infantry formations of six battalions and an engineer company (two at the Capital Centre, two at '
           'District B, two at District F, one at District A); 48 fighters and 12 support aircraft on the one capital air base, '
           'with 12 fighters and 4 support aircraft in reserve; two coastal escorts in the Maritime Service at District A; 60 '
           'convoys; research priority Physical Sustainment (transport, equipment replacement, affordable service); political '
           'institution civil_administration, capacity 40; fiscal profile GDP 200, debt ratio 0.3, collection 0.85. Fictional '
           'calibration, not canon national accounts or order of battle.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'mod/2985041246/history/units/ESN_ws_land.txt, ESN_ws_air.txt, ESN_ws_navy.txt; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour consistency: no other spec names Silvonia. Glaceland (tools/world_depth/gla/content.py) borders '
           'Sfaenland, Luremia and Kaluga but not Silvonia. This tree builds and governs only on the Silvonian side, charts its '
           'own airspace, and claims no action, consent or outcome for any neighbour.',
           'tools/world_depth/gla/content.py'),
    Source('Official',
           'Date anchor: the International Astronomical Union announces that Ulysses will pass close to Earth with a chance '
           'of impact. Opens the Ulysses branch; no Silvonian role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Opens the distant-war focuses; Silvonia takes no part.', '1995 / 03.25'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Date gate of the fallout sampling focus, '
           'which also reads the mod flag belka_dropped_nukes; no fallout in Silvonia is claimed.', '1995 / 06.06'),
    Source('Official',
           'A treaty is signed in Lumen and the Belkan War ends. Date gate of the stand-down focus.', '1995 / 06.20'),
    Source('Official',
           'The President of the FCU announces that Ulysses will impact the Earth. Date gate of the impact focus; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Former top pilots from the Belkan Air Force are hired by various countries and work as aggressor squadrons. Date '
           'gate and premise of the aggressor instructors focus; no individual is named and no hire by Silvonia is claimed as '
           'fact.', '1998 / 06.19'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Date gate of the night-watch focus; no damage in '
           'Silvonia is claimed.', '1999 / 07.08'),
    Source('Official',
           'Osea and Yuktobania cooperate to convert the Arkbird into a platform for clearing debris from satellite orbits. '
           'Date gate of the orbital watch focus; Silvonia only observes, and no cooperation with it is claimed.',
           '1999 / 10.08'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air '
           'batteries. Opens the railgun study focus and event.', '2003 / SUMMER'),
    Source('Official',
           'The FCU establishes the ISAF. Date gate of the spares contracts focus, which is trade only and changes no faction.',
           '2003 / 08.22'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war, belka_lost_belkan_war and belka_dropped_nukes '
           '(events/Belka.txt and related scripts), ac_ucw_stonehenge_destroyed, ac_ucw_outcome_isaf_victory and '
           'ac_ucw_outcome_erusean_victory (common/scripted_effects/ac_ucw.txt). Each reaction is a leaf focus, so no outcome '
           'blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Silvonian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in the ten '
           '1991 states and within their free slots.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who holds the seals
    IdeaDef('admin_interim', 'The Interim Administration', 'A National Administration with a democratic name governs on a renewed standing order.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('assembly', 'document')),
    IdeaDef('chamber_timetable', 'A Date for the Chamber', 'The chamber will reopen with seats for all ten districts.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('plant_districts_voice', 'Voice of the Plant Districts', 'The owners of the three plant districts expect a share of government.',
            {'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.02}, ('industry', 'assembly')),
    IdeaDef('vigilance_rallies', 'The Vigilance Rallies', 'The movement of the empty districts fills the squares and claims the state.',
            {'war_support_factor': 0.06, 'stability_factor': -0.03, 'political_power_gain': 0.05}, ('security', 'ballot')),
    IdeaDef('shield_officers', 'Officers of the Shield', 'The air staff and the warning service offer to hold the state.',
            {'political_power_gain': 0.10, 'air_detection': 0.05}, ('air', 'command')),
    IdeaDef('reopened_chamber_charter', 'The Ten-District Charter', 'A written charter with an elected chamber, district councils and a court.',
            {'stability_factor': 0.08, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('scales', 'ballot')),
    IdeaDef('plant_compact', 'The Plant Town Compact', 'Published wage tables, housing funds and a training levy in the plant districts.',
            {'production_factory_efficiency_gain_factor': 0.05, 'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('economy', 'scales')),
    IdeaDef('vigilance_wardens', 'Wardens in Every District', 'Movement wardens patrol the streets, guard the depots and keep the rolls.',
            {'war_support_factor': 0.08, 'army_core_defence_factor': 0.05, 'stability_factor': 0.02}, ('security', 'civil')),
    IdeaDef('shield_statute', 'The Shield Statute', 'The council has published its powers and the conditions for handing them back.',
            {'stability_factor': 0.05, 'political_power_gain': 0.10, 'air_superiority_efficiency': 0.04}, ('document', 'radar')),
    # ten districts
    IdeaDef('district_survey', 'The Ten-District Survey', 'A census-backed account of what each district has and lacks.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('document', 'civil')),
    IdeaDef('rail_first', 'Rails Before Roads', 'New transport money extends the rail spine into the empty districts.',
            {'production_speed_infrastructure_factor': 0.15, 'army_speed_factor': 0.03}, ('rail', 'tools')),
    IdeaDef('road_first', 'Gravel to Every Town', 'New transport money grades a little road everywhere before any new track.',
            {'production_speed_infrastructure_factor': 0.12, 'stability_factor': 0.03}, ('logistics', 'civil')),
    # plant districts
    IdeaDef('ore_registry', 'The Ore Registry', 'Every pit, well and plantation inspected and recorded.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.05}, ('document', 'industry')),
    IdeaDef('aluminium_for_wings', 'Aluminium for Wings', 'Home metal reserved for airframes, spares and radar masts.',
            {'production_speed_arms_factory_factor': 0.08, 'repair_speed_factor': 0.05}, ('air', 'industry')),
    IdeaDef('metal_exports', 'Ingots at the Railhead', 'Raw metal sold abroad for the hard currency that buys fuel and engines.',
            {'industrial_capacity_factory': 0.05, 'consumer_goods_factor': -0.03}, ('economy', 'rail')),
    IdeaDef('silo_reserve', 'The Silo Reserve Rule', 'The single fuel silo may never fall below a fixed reserve.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.02}, ('logistics', 'shelter')),
    IdeaDef('district_dividend', 'The Empty-District Dividend', 'A share of plant profits builds schools and wells where there are no plants.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('economy', 'civil')),
    # sustainment
    IdeaDef('repair_depot', 'The Central Repair Depot', 'One depot, one store and one set of records for the whole air arm.',
            {'repair_speed_factor': 0.10, 'production_factory_max_efficiency_factor': 0.02}, ('tools', 'industry')),
    IdeaDef('spares_pool', 'The Spares Pool', 'Spares bought in bulk and issued by serial number against signed requests.',
            {'repair_speed_factor': 0.05, 'air_mission_efficiency': 0.03}, ('logistics', 'tools')),
    IdeaDef('licence_line', 'The Licensed Trainer Line', 'A proven foreign trainer assembled at home under licence.',
            {'production_speed_arms_factory_factor': 0.10, 'production_factory_efficiency_gain_factor': 0.03}, ('document', 'industry')),
    IdeaDef('home_design', 'The Design Office', 'A small office drawing a Silvonian trainer from the ground up.',
            {'research_speed_factor': 0.05, 'political_power_gain': -0.05}, ('science', 'air')),
    # the air arm
    IdeaDef('one_field_wing', 'Sixty Aircraft on One Field', 'The whole air arm on a single small field beside the fuel silo.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('interceptor_doctrine', 'Interceptors First', 'Every fighter based, armed and trained to deny the sky.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('support_doctrine', 'Wings for the Valleys', 'Fighters and support aircraft trained to fight beside the battalions.',
            {'air_mission_efficiency': 0.08, 'army_defence_factor': 0.03}, ('air', 'training')),
    IdeaDef('alert_pairs', 'Two on Alert', 'Two armed fighters waiting at the runway end, day and night.',
            {'air_superiority_efficiency': 0.05, 'experience_gain_air_factor': 0.05}, ('air', 'security')),
    IdeaDef('pilot_school', 'The Hill Pilot School', 'Pilots trained at home for mountain weather and short runways.',
            {'experience_gain_air_factor': 0.08, 'training_time_factor': -0.05}, ('training', 'air')),
    IdeaDef('aggressor_course', 'The Aggressor Course', 'Contract instructors fly against Silvonian pilots in training.',
            {'experience_gain_air_factor': 0.12, 'political_power_gain': -0.05}, ('medal', 'air')),
    IdeaDef('reserve_squadron', 'The Reserve Squadron', 'The stored airframes fly again with instructors and reservists.',
            {'air_defence_factor': 0.05, 'experience_gain_air_factor': 0.03}, ('air', 'rebuild')),
    # the warning net
    IdeaDef('observer_corps', 'The Observer Corps', 'Volunteer observers on hilltops in every district.',
            {'air_detection': 0.05, 'stability_factor': 0.01}, ('telescope', 'communications')),
    IdeaDef('frontier_radar', 'The Frontier Radar Line', 'Radar stations along the passes, the desert and the hills.',
            {'air_detection': 0.10, 'air_superiority_efficiency': 0.03}, ('radar', 'security')),
    IdeaDef('capital_ring', 'The Capital Ring', 'Radar, guns and shelters concentrated around the plants and the air base.',
            {'static_anti_air_damage_factor': 0.10, 'air_defence_factor': 0.05}, ('shelter', 'radar')),
    IdeaDef('gun_belts', 'Gun Belts Around the Plants', 'Overlapping anti-aircraft belts around the capital plants.',
            {'static_anti_air_damage_factor': 0.12, 'stability_factor': 0.02}, ('security', 'industry')),
    IdeaDef('control_bunker', 'The Control Bunker', 'One protected plotting room that sees the whole sky.',
            {'planning_speed': 0.08, 'air_detection': 0.05, 'air_superiority_efficiency': 0.03}, ('shelter', 'command')),
    IdeaDef('plot_room_rule', 'Government from the Plot', 'The council governs from the control bunker itself.',
            {'air_superiority_efficiency': 0.05, 'planning_speed': 0.05, 'stability_factor': -0.02}, ('command', 'radar')),
    # the formations
    IdeaDef('formation_rolls', 'Seven Formations Counted', 'The infantry formations exercised together and counted honestly.',
            {'army_org_factor': 0.03}, ('training', 'document')),
    IdeaDef('mountain_battalions', 'Mountain Battalions', 'Battalions based permanently in the frontier passes.',
            {'army_defence_factor': 0.05, 'attrition': -0.05}, ('training', 'tools')),
    IdeaDef('rail_reserve', 'The Rail Reserve', 'Formations held near the junction, ready to entrain for any frontier.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.05}, ('rail', 'command')),
    IdeaDef('airfield_guards', 'Airfield Guard Companies', 'Dedicated guards for fields, radar posts and fuel stores.',
            {'army_core_defence_factor': 0.08}, ('security', 'runway')),
    IdeaDef('desert_patrols', 'Desert Patrols', 'Motorised patrols on the longest and emptiest frontier.',
            {'army_core_defence_factor': 0.05, 'supply_consumption_factor': -0.05}, ('logistics', 'security')),
    IdeaDef('vigilance_companies', 'Vigilance Companies', 'Part-time movement volunteers guarding bridges and posts in the empty districts.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.04, 'stability_factor': -0.02}, ('security', 'medal')),
    # frontiers and the Belkan War
    IdeaDef('airspace_charts', 'Charted Airspace', 'Agreed reporting points and frequencies on every edge of the sky.',
            {'air_superiority_efficiency': 0.03, 'stability_factor': 0.02}, ('document', 'air')),
    IdeaDef('war_watch', 'Watch on a Distant War', 'Higher readiness while war burns far away.',
            {'air_detection': 0.05, 'war_support_factor': 0.03}, ('communications', 'security')),
    IdeaDef('closed_sky', 'A Closed Sky', 'No aircraft of a belligerent state may cross Silvonia.',
            {'air_superiority_efficiency': 0.05, 'army_core_defence_factor': 0.05}, ('security', 'air')),
    IdeaDef('open_corridors', 'Open Civil Corridors', 'Airlines cross on filed plans; military aircraft are refused.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.03}, ('peace', 'air')),
    IdeaDef('overflight_fees', 'Overflight Fees', 'Rerouted airlines pay to cross Silvonian skies.',
            {'political_power_gain': 0.08, 'air_detection': 0.03}, ('economy', 'air')),
    IdeaDef('fallout_watch', 'The Fallout Watch', 'Weekly published samples of wind and rain.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02}, ('telescope', 'medical')),
    IdeaDef('belkan_orders', 'Belkan Purchasing Missions', 'Orders for metal, rubber and fuel from a victorious Belka.',
            {'production_speed_arms_factory_factor': 0.06, 'stability_factor': -0.02}, ('diplomacy', 'economy')),
    # Ulysses
    IdeaDef('sky_tracking', 'Watchers of the Sky', 'The air staff asked to watch the asteroid as well as the frontiers.',
            {'air_detection': 0.05, 'research_speed_factor': 0.02}, ('telescope', 'meteor')),
    IdeaDef('evacuation_timetable', 'The Evacuation Timetable', 'Trains ready to empty the plant towns into the open districts.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'refugees')),
    IdeaDef('hill_galleries', 'Galleries Under the Hills', 'Shelters cut into the capital hills and sealed cellars under the plants.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.04}, ('shelter', 'civil')),
    IdeaDef('public_drills', 'Drills the Deputies Chose', 'Emergency drills debated and approved district by district.',
            {'stability_factor': 0.05, 'war_support_factor': 0.03}, ('ballot', 'shelter')),
    IdeaDef('orbit_watch', 'Watch on the Orbits', 'Radar crews follow low, fast objects they never trained for.',
            {'air_detection': 0.08, 'research_speed_factor': 0.03}, ('satellite', 'radar')),
    # the millennium
    IdeaDef('life_extension', 'Ten More Years', 'The old fighters rebuilt at the depot to fly another decade.',
            {'repair_speed_factor': 0.10, 'experience_gain_air_factor': 0.04}, ('rebuild', 'air')),
    IdeaDef('new_interceptors', 'The New Interceptor', 'A modern interceptor bought abroad with a long support contract.',
            {'air_superiority_efficiency': 0.08, 'political_power_gain': -0.08}, ('air', 'diplomacy')),
    IdeaDef('railgun_study', 'The Railgun Study', 'Staff officers study a ground weapon that strikes aircraft at long range.',
            {'static_anti_air_damage_factor': 0.08, 'research_speed_factor': 0.02}, ('missile', 'radar')),
    IdeaDef('railgun_lessons', 'Lessons of the Railguns', 'A finished study: even the greatest anti-air weapon can be undone.',
            {'static_anti_air_damage_factor': 0.10, 'air_superiority_efficiency': 0.04, 'research_speed_factor': 0.03}, ('missile', 'document')),
    IdeaDef('isaf_spares', 'Spares for the ISAF', 'Depot work and spares sold to ISAF squadrons; no pilots committed.',
            {'production_speed_arms_factory_factor': 0.08, 'stability_factor': -0.02}, ('diplomacy', 'tools')),
    IdeaDef('no_wings_export', 'Nothing With Wings Leaves', 'No aircraft part, fuel or sheet metal sold to either side.',
            {'stability_factor': 0.04, 'repair_speed_factor': 0.05}, ('peace', 'security')),
    IdeaDef('usean_contracts', 'Advisers on Contract', 'Silvonian radar and observer specialists advise on private contracts.',
            {'experience_gain_air_factor': 0.05, 'political_power_gain': 0.05}, ('diplomacy', 'radar')),
    IdeaDef('erusean_caution', 'A Watchful Shield', 'More radar watch and more alert hours while the victor of Usea is unknown in intent.',
            {'air_detection': 0.05, 'war_support_factor': 0.04}, ('security', 'diplomacy')),
    # decisions
    IdeaDef('alert_drill', 'A National Alert Drill', 'Every post and crew tested against a surprise raid by the air arm itself.',
            {'air_detection': 0.05, 'war_support_factor': 0.02}, ('radar', 'communications')),
    IdeaDef('ledger_inspection', 'Plants Under Inspection', 'Unannounced registry visits keep the owners honest and nervous.',
            {'political_power_factor': 0.08, 'stability_factor': -0.02}, ('document', 'industry')),
    IdeaDef('hangar_day', 'Open Hangar Season', 'Flying displays and recruiting stands at the capital field.',
            {'war_support_factor': 0.03, 'stability_factor': 0.02}, ('medal', 'air')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('reopened_chamber_cabinet', 'Cabinet of the Reopened Chamber',
           'A cabinet chosen by and answerable to a chamber elected from all ten districts, governing collectively on a fixed '
           'election calendar. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('plant_council', 'Council of the Plant Districts',
           'A standing council of owners and managers from the plants of the Capital District, District B and District F, '
           'holding the seals of government with elections still suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'oligarchism'),
    Office('vigilance_directorate', 'Directorate of National Vigilance',
           'A directorate drawn from the nationalist movement of the districts without plants, ruling by decree with a '
           'commissioner beside every district governor. Provisional gameplay office with no named holder.',
           'fascism', 'nativism'),
    Office('shield_council', 'Air Shield Council',
           'A council of senior officers from the air staff, the warning service and the garrisons, holding power under a '
           'declared emergency with no fixed end. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('interim_question', 'Who Holds the Seals', (
        "For three years the ministers of the National Administration have found reasons to leave one item off their "
        "agenda. Now it cannot wait. The standing order that keeps the ballot box locked lapses at the end of the month, and "
        "the ministry lawyers will not draft another renewal unless the ministers vote on it by name. The country is run by a "
        "body with a democratic label and almost no democrats to stand behind it.",
        "Beyond the meeting room the country has split into two nearly equal halves. In the seven districts without plants, a "
        "nationalist movement fills the market squares with people who have never seen a paved road and blame the plant towns "
        "for it. In the Capital District, District B and District F, plant owners, officials and air staff officers want "
        "predictable budgets more than any creed, and suspect the movement of wanting their plants.",
        "The ministers cannot settle the question in one sitting. They can choose how it will be argued: over the state radio, "
        "with every district listening and the movement's speakers given equal hours, or behind ministry doors, where the plant "
        "owners already have chairs and the movement has none. Each half of the country will read the choice as a statement "
        "about which half the Administration fears more.",
    ), (
        Option('Put the debate on the state radio.', (Stability(0.02), WarSupport(0.02), PP(-15))),
        Option('Hold the talks behind ministry doors.', (PP(40), Stability(-0.02))),
    ), picture=0),
    EventDef('ten_districts', 'The Census of Ten Districts', (
        "The census teams return from the ten districts with crates of ledgers, and the figures confirm what every traveller "
        "already knew. The Capital District, four crowded hill provinces, holds four civilian plants, two arms works, the only "
        "air base and the fuel silo. District B in the mountains and District F in the coastal jungle each hold three civilian "
        "plants and two arms works. Between them the three plant districts carry nearly the whole economy.",
        "District A has the naval base, two yards and a marsh that floods the rail embankment every wet season. The remaining "
        "six districts have no plants at all. District C is seventeen provinces of farmland without a road a loaded truck can "
        "use. District H is twenty-six provinces of desert. Districts D and I are mountain towns whose passes close each winter, "
        "District G is hill country, and District J holds the rail junction and little else.",
        "Publication is now the question. A census printed line by line will start a quarrel about fairness that could fill "
        "the next decade of politics, and the movement will read from it at every rally. Kept within the ministries, the same "
        "ledgers will steer the road budget quietly while the empty districts assume the worst of the capital. Whatever the "
        "cabinet decides, the first road money will follow these numbers.",
    ), (
        Option('Print every district figure.', (Stability(0.02), WarSupport(0.01), PP(-20))),
        Option('Keep the figures inside the ministries.', (PP(30), Stability(-0.01))),
    ), picture=2),
    EventDef('ore_count', 'Metal Sold, Metal Bought', (
        "The registry inspectors finish their year in the pits, wells and plantations of the three plant districts. Their "
        "figures for oil, steel ore, bauxite and rubber are higher than the owners reported and lower than the ministries "
        "assumed, which surprises nobody. The surprise is in the trade ledgers compiled alongside: almost all the aluminium "
        "Silvonia smelts leaves the country as ingots on the railway to the coast and the frontier crossings.",
        "In the same years the air arm has bought aluminium parts, sheet and fittings from abroad at prices many times what the "
        "ingots fetched. The depot mechanics have known this for years and joke about it at the bench. The plant owners point "
        "out that foreign buyers pay in hard currency, which buys the fuel and engines Silvonia cannot produce. Both arguments "
        "are true, and both are now printed in the same report.",
        "The cabinet must decide what to do with the report before the newspapers do it for them. A levy on raw metal exports "
        "would push the smelters to sell at home and make the plant owners furious. Leaving the trade alone keeps the hard "
        "currency flowing and leaves the air arm buying back its own metal at foreign prices for another decade.",
    ), (
        Option('Levy raw metal exports.', (PP(-20), Research('industry', 0.5, 1))),
        Option('Leave the trade as it is.', (PP(25), Stability(-0.01))),
    ), picture=2),
    EventDef('grounded_aircraft', 'Grounded for Want of Parts', (
        "The inspection teams spend a month on the capital field, opening every panel on every airframe. Their report is short. "
        "Of the forty-eight fighters and twelve ground-support aircraft listed on the rolls, fewer than two thirds can fly on an "
        "ordinary morning. The rest wait for parts: a hydraulic pump here, a radio there, an engine that went abroad for "
        "overhaul a year ago and has not come back.",
        "The mechanics have kept the fleet flying by moving parts from one grounded aircraft to the next, a practice the "
        "regulations forbid and every squadron depends on. Two airframes have been stripped so thoroughly that only their "
        "serial numbers remain. The pilots fly fewer hours each year than they did a decade ago, and the squadron commanders "
        "have stopped asking for more because they already know the answer.",
        "The air staff gives the government two ways forward. It can formally strip the worst airframes for parts, losing "
        "aircraft from the rolls to keep the rest flying. Or it can order spares abroad at whatever price suppliers ask, "
        "emptying the budget for a year to bring the whole fleet back. Either way, the figures cannot go back into the drawer "
        "they came from.",
    ), (
        Option('Strip the worst airframes for parts.', (XP('air', 15), Stability(-0.01))),
        Option('Order spares abroad at any price.', (PP(-25), XP('air', 25))),
    ), picture=1),
    EventDef('one_field', 'Fire on the Flight Line', (
        "Late on a weekday afternoon a fuel bowser catches fire beside the main taxiway of the capital field. Nobody is killed. "
        "The crew escape, the fire brigade arrives in minutes and the flames are out within the hour. But the taxiway is blocked "
        "by the burned-out truck, the runway is covered in foam, and for the rest of that day and most of the next not one "
        "Silvonian combat aircraft can take off.",
        "Every fighter, every ground-support aircraft and every reserve airframe sits on the same small field in the Capital "
        "District, beside the only fuel silo in the country. The air staff has warned about this for years in reports that "
        "nobody read. This time the newspapers print photographs of the fighters lined up wingtip to wingtip behind the smoke, "
        "and their readers draw their own conclusions.",
        "The government must decide what the fire means. It can treat it as an accident and tighten the safety rules, which "
        "costs little and changes nothing about where the aircraft sit. Or it can treat it as the warning the air staff always "
        "said would come, and start planning dispersal fields in other districts at once, which costs a great deal and will "
        "take years to finish.",
    ), (
        Option('Start planning dispersal fields now.', (PP(-15), XP('air', 10), WarSupport(0.02))),
        Option('Tighten the safety rules and carry on.', (PP(20), Stability(-0.01))),
    ), picture=1),
    EventDef('unknown_contact', 'An Aircraft Nobody Expected', (
        "On a clear morning an observer post on a hilltop in District G telephones the district office to report an aircraft "
        "crossing from the direction of the frontier, high and fast and showing no markings anyone can read through "
        "binoculars. The district office calls the capital. The capital calls the air staff. By the time two fighters take off "
        "from the capital field, forty minutes have passed since the first report.",
        "The fighters find nothing. Two more posts report the same aircraft further north, then the reports stop. It may have "
        "been an airliner off course, a survey flight with a careless navigator or something that had every reason not to file "
        "a flight plan. Nobody in Silvonia can say, because nobody in Silvonia saw it on anything but a pair of binoculars and "
        "a telephone line.",
        "The observers did exactly what they were trained to do and are proud of it. The air staff is less proud: a reporting "
        "chain that takes forty minutes is no chain at all. The ministers can open a formal inquiry, which will embarrass "
        "several offices and produce recommendations that cost money, or thank the observers publicly and let the matter rest.",
    ), (
        Option('Open a formal inquiry.', (Event('contact_inquiry', 14),)),
        Option('Thank the observers and let it rest.', (PP(15), Stability(0.01))),
    ), picture=0),
    EventDef('contact_inquiry', 'Forty Minutes', (
        "The inquiry sits for two weeks in a borrowed classroom in the Capital District and interviews everyone in the chain: "
        "the observers on the hill, the clerk at the district office, the duty officer at the ministry, the pilots who took off "
        "too late. Its findings are blunt. Every person acted correctly by their own rules. The rules themselves added twenty "
        "minutes, and the telephone exchange added the rest.",
        "The observer post had no direct line to the air staff, so its report waited for a district clerk to finish another "
        "call. The ministry duty officer needed approval to wake the air staff, and the air staff needed a second approval to "
        "launch fighters over a frontier district. Nobody on the ground could tell the pilots where to look, because nobody on "
        "the ground knew where the aircraft was by then.",
        "The report recommends direct lines from every post to the air staff, standing authority for the duty officer to "
        "launch the alert fighters, and radar as soon as the country can afford it. The recommendations are cheap except the "
        "last. The government can publish the report as written, or fund the telephone lines quietly and keep the forty "
        "minutes out of the newspapers.",
    ), (
        Option('Publish the report as written.', (Stability(-0.01), XP('air', 15), WarSupport(0.02))),
        Option('Fund the lines and keep it quiet.', (PP(-20), Research('radar_tech', 0.5, 1))),
    ), picture=0),
    EventDef('mountain_exercise', 'Seven Formations in the Snow', (
        "In January the seven infantry formations leave their barracks at the Capital Centre, the logistics centres of District "
        "B and District F and the naval base in District A, and converge on the passes of District B for the first full "
        "exercise in years. Trains carry them to the railhead. From there they march, because the roads into the high valleys "
        "are closed by snow and the trucks cannot follow.",
        "The results are mixed. The formations that started in District B arrive on time and in good order. The battalions from "
        "District F, trained in coastal jungle, arrive with frostbite and the wrong boots. The engineer companies prove better "
        "at clearing roads than anyone expected and worse at bridging, and the radios fail in the cold. Ground-support aircraft "
        "from the capital field fly twice in ten days because of the weather.",
        "The army staff must decide what to buy. Cold-weather equipment for every formation would make the whole army fit for "
        "the mountains at a cost the treasury will feel. Rotating battalions through the passes in turn would spread the "
        "experience cheaply and slowly, and leave some formations unready if a crisis came in winter.",
    ), (
        Option('Equip every formation for the cold.', (PP(-20), XP('army', 20))),
        Option('Rotate battalions through the passes.', (XP('army', 10), Stability(0.01))),
    ), picture=2),
    EventDef('belkan_war', 'Distant Guns, Crowded Skies', (
        "On 25 March 1995 war breaks out around Belka. Silvonia lies far from the fighting and has no stake in it, yet within "
        "days the war reaches its sky. Airlines reroute away from the war zone, and some of the new routes cross Silvonian "
        "airspace. Fuel prices rise on every market. Insurers add war-risk premiums to cargoes that never come near the front.",
        "The air staff reports a doubling of unannounced flights over the frontier districts, most of them civil, some of them "
        "not obviously so. The plant owners report foreign buyers asking for aluminium, steel and fuel in quantities they have "
        "never seen. The movement's newspapers demand that Silvonia keep its distance; the ministries worry that distance will "
        "be expensive.",
        "The government must say something before the air staff starts intercepting airliners on its own initiative. It can "
        "declare that Silvonian airspace is closed to the aircraft of any belligerent and enforce it, or say only that the "
        "ordinary rules of the air apply and leave the details to the ministries. Both statements will be read abroad, in "
        "capitals that rarely think about Silvonia at all.",
    ), (
        Option('Close the sky to every belligerent.', (WarSupport(0.03), PP(-10))),
        Option('Say only that the rules of the air apply.', (PP(25), Stability(0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; the Silvonian response is gameplay', picture=1),
    EventDef('ulysses_will_strike', 'The Asteroid Will Fall', (
        "The warning of late 1994 has become a certainty. On 20 April 1996 the President of the FCU tells the world that "
        "Ulysses will hit, and no astronomer will yet promise which regions the pieces will reach. Silvonia keeps its plants, "
        "its only fuel silo and its only air base within a few hill provinces of the Capital District, and its government has "
        "never prepared for a threat from above that carries no pilot.",
        "Every ministry finds a plan that needs money. The mining engineers of District B propose galleries cut into the "
        "capital's hills. The railway office proposes timetables to empty the plant towns into the open districts. The air "
        "staff proposes to put its radar crews and observers on permanent watch, though they admit they have never tracked "
        "anything so fast or so high.",
        "The public does not wait for the plans. Markets in the capital sell out of water containers and lamp oil, some "
        "families in the plant towns pack for relatives in the empty districts, and the movement holds rallies asking why the "
        "capital gets everything first. The government must decide whether to speak openly and at once, or calmly and slowly.",
    ), (
        Option('Prepare openly and at once.', (WarSupport(0.02), Stability(-0.02))),
        Option('Urge calm and keep working.', (Stability(0.03), PP(-5))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Silvonian preparations are gameplay',
        picture=0),
    EventDef('impact_night', 'The Night the Sky Was Watched', (
        "The date the astronomers fixed arrives on 8 July 1999, when Ulysses crosses the distance at which the Earth's pull "
        "begins to tear it apart. Every radar crew and every hilltop observer in Silvonia is at a post, the alert fighters wait "
        "at the runway end with their pilots strapped in, and the duty officer in the plotting room has orders to report "
        "anything at all. Most of the country spends the night where its plans told it to be.",
        "The plotting room fills with reports: lights in the sky over District H, sounds like thunder in the mountains of "
        "District D, a radar return that comes and goes too fast to plot. Each report is checked against the others, and most "
        "cannot be confirmed. The duty officers learn more about the limits of their net in one night than in eight years of "
        "exercises.",
        "At dawn the ministries begin the slow work of finding out what is true. The air staff wants the emergency measures kept "
        "in force until every district has reported. The plant owners want the workers back on shift. The government must "
        "decide which risk it prefers: a country that stays shut for a week, or one that reopens before it knows.",
    ), (
        Option('Keep the measures until every district reports.', (WarSupport(0.03), Stability(-0.01))),
        Option('Reopen the plants at once.', (Stability(0.02), PP(15))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no Silvonian damage is claimed', picture=0),
    EventDef('railguns_turned', 'Railguns Against Aircraft', (
        "The reports from Usea in mid-2003 are brief and alarming. Erusean troops have occupied San Salvacion, a country that "
        "had declared itself neutral, and the enormous guns of Stonehenge are now firing at aircraft. Usea is a long way off "
        "and Silvonia has no part in the war. Yet under the capital's hills the plotting staff take the news harder than "
        "anyone in government, because every Silvonian plan assumes that aircraft decide who holds the sky.",
        "The staff officers ask the obvious questions and find no comfortable answers. A ground weapon that can strike aircraft "
        "at such ranges makes fighters, radars and alert pairs look like a smaller part of the picture than they were last "
        "year. Others argue that one immense installation is also one immense target, and that a weapon which cannot move can "
        "be studied, avoided and eventually defeated.",
        "The government can commission a full staff study of the new weapon and what it means for Silvonian doctrine, which "
        "will take the best officers away from their posts for a year. Or it can note the news, keep to the existing budget and "
        "wait to see how the war develops before drawing conclusions it may later have to withdraw.",
    ), (
        Option('Commission a full staff study.', (Research('air_doctrine', 0.5, 1), PP(-15))),
        Option('Note it and keep to the budget.', (PP(20),)),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Silvonian response is gameplay', picture=0),
)

# --- branches ------------------------------------------------------------------------------------
POLITICS = Branch('pol', 'The Locked Ballot Box', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('pol_no_following', 'An Office With No Following',
          "In 1991 Silvonia is run by a National Administration that keeps a democratic label while the democratic camp has "
          "almost no voters left. Elections are suspended by standing order. Half the country follows a nationalist movement "
          "rooted in the seven districts without plants; the other half trusts the plant owners, ministries and air staff. "
          "Naming that split in public is the first cost of mending it.",
          ('assembly', 'document'), reward=(Idea('admin_interim'), Event('interim_question'))),
    Focus('pol_order_in_court', 'The Standing Order in Court',
          "The order that locked the ballot box has been renewed every year without debate. The ministers now send it to the "
          "high court for an opinion and promise to print the answer. Whatever the judges decide, every faction must then say "
          "what should replace the order. The Administration gives up the comfort of governing by renewal and gets a public "
          "argument instead.",
          ('scales', 'document'), after=('pol_no_following',),
          reward=(PP(30), Tooltip('Opens four answers to the question of who governs Silvonia; only one can be taken.'))),
    Focus('pol_chamber_path', 'Seats for All Ten Districts',
          "Reformers in the ministries propose to reopen the old chamber with seats apportioned by population across all ten "
          "districts, so that the empty districts are finally counted. Nationalists would win many of those seats, and the "
          "plant towns would lose their quiet hold on the budget. The reformers accept both risks, because a mandate drawn from "
          "every district is far harder to wave away.",
          ('ballot', 'assembly'), after=('pol_order_in_court',),
          exclusive=('pol_plants_path', 'pol_vigilance_path', 'pol_shield_path'),
          reward=(SwapIdea('admin_interim', 'chamber_timetable'),)),
    Focus('pol_plants_path', 'The Plant Towns Want the Seals',
          "The Capital District, District B and District F hold every civilian plant and arms works in the country, most of its "
          "oil, steel and aluminium and nearly all of its tax roll. Their owners and managers propose a council of the three "
          "plant districts to run the state like a works board. The non-aligned half of the country finds this sensible. The "
          "other seven districts hear a closed shop.",
          ('industry', 'assembly'), after=('pol_order_in_court',),
          exclusive=('pol_chamber_path', 'pol_vigilance_path', 'pol_shield_path'),
          reward=(SwapIdea('admin_interim', 'plant_districts_voice'),)),
    Focus('pol_vigilance_path', 'The Movement of the Empty Districts',
          "The nationalist movement draws its crowds from the seven districts that have no plants, few roads and long memories "
          "of being ignored. Its speakers promise Silvonian hands in every plant, Silvonian pilots in every cockpit and no "
          "foreign contractors anywhere. They offer to end the suspended politics by abolishing the contest itself. The plant "
          "owners start moving their savings abroad.",
          ('security', 'ballot'), after=('pol_order_in_court',),
          exclusive=('pol_chamber_path', 'pol_plants_path', 'pol_shield_path'),
          reward=(SwapIdea('admin_interim', 'vigilance_rallies'),)),
    Focus('pol_shield_path', 'The Air Staff Steps Forward',
          "The air staff and the warning service are the most trusted institutions in Silvonia, perhaps because they never stood "
          "for election. Senior officers offer to run the country through a council until the two camps stop shouting, keeping "
          "the ministries as staff sections under military direction. They promise order without a winner. People who spend "
          "their careers planning interceptions may come to treat every argument as a threat.",
          ('air', 'command'), after=('pol_order_in_court',),
          exclusive=('pol_chamber_path', 'pol_plants_path', 'pol_vigilance_path'),
          reward=(SwapIdea('admin_interim', 'shield_officers'),)),
    Focus('pol_chamber_cabinet', 'Seat the Reopened Chamber',
          "The chamber meets in the Capital Centre for the first time since the standing order was signed, with deputies from "
          "every one of the ten districts. It chooses a cabinet that answers to it and fixes a calendar of elections. "
          "Nationalist deputies hold many seats and use every one of them. Budgets now take months to pass, but nobody can say "
          "the government was chosen by nobody.",
          ('ballot', 'document'), after=('pol_chamber_path',), cost=10,
          exclusive=('pol_plant_council', 'pol_vigilance_directorate', 'pol_shield_council'),
          reward=(Regime('reopened_chamber_cabinet'), Flag('gov_chamber'))),
    Focus('pol_plant_council', 'The Plant Council Takes the Seals',
          "Owners and managers from the three plant districts form a standing council and take the seals of government. "
          "Elections stay suspended and the ministries report to the council as departments of a single enterprise. Contracts "
          "are signed quickly and the books balance at last. The seven districts without plants were never asked, and the "
          "council makes little effort to pretend otherwise.",
          ('economy', 'command'), after=('pol_plants_path',), cost=10,
          exclusive=('pol_chamber_cabinet', 'pol_vigilance_directorate', 'pol_shield_council'),
          reward=(Regime('plant_council'), Flag('gov_plants'))),
    Focus('pol_vigilance_directorate', 'The Vigilance Directorate Rules',
          "A directorate drawn from the movement takes executive power and governs by decree. Rival offices close, foreign "
          "managers are sent home from the plants and a movement commissioner sits beside every district governor. Public order "
          "improves at once and the recruiting offices fill. Foreign suppliers of spares and fuel grow wary of a government that "
          "may cancel any contract at a rally.",
          ('security', 'command'), after=('pol_vigilance_path',), cost=10,
          exclusive=('pol_chamber_cabinet', 'pol_plant_council', 'pol_shield_council'),
          reward=(Regime('vigilance_directorate'), Flag('gov_vigilance'))),
    Focus('pol_shield_council', 'Convene the Air Shield Council',
          "Officers of the air staff, the warning service and the garrisons assume power under an emergency of no stated "
          "length. Parties are not banned, only ignored. The radar posts report on schedule and the fighters fly their patrols. "
          "Nobody on the council has a plan for handing power back, and every faction knows that an emergency without an end "
          "date rarely ends by itself.",
          ('radar', 'command'), after=('pol_shield_path',), cost=10,
          exclusive=('pol_chamber_cabinet', 'pol_plant_council', 'pol_vigilance_directorate'),
          reward=(Regime('shield_council'), Flag('gov_shield'))),
    Focus('pol_chamber_charter', 'A Charter Read in Ten Districts',
          "After two sessions of drafting, the chamber passes a written charter. Deputies are elected on a fixed calendar, "
          "ministers can be dismissed by a vote, each district gets a council with money of its own, and a charter court hears "
          "quarrels between them. Copies are read aloud in every district hall, including halls built only last year. The "
          "nationalist bloc wins a strong speakership as the price of its votes.",
          ('scales', 'ballot'), after=('pol_chamber_cabinet',),
          exclusive=('pol_plant_compact', 'pol_vigilance_wardens', 'pol_shield_statute'),
          reward=(SwapIdea('chamber_timetable', 'reopened_chamber_charter'),)),
    Focus('pol_plant_compact', 'Wage Tables for the Plant Towns',
          "To quiet the strikes that follow its first year, the council signs a compact with plant workers in the three "
          "industrial districts: published wage tables, housing funds and a training levy. The owners pay more than they wanted "
          "and gain a calm they could not buy by decree. The seven empty districts notice that the compact covers nobody who "
          "lives there.",
          ('economy', 'scales'), after=('pol_plant_council',),
          exclusive=('pol_chamber_charter', 'pol_vigilance_wardens', 'pol_shield_statute'),
          reward=(SwapIdea('plant_districts_voice', 'plant_compact'),)),
    Focus('pol_vigilance_wardens', 'Wardens on Every Street',
          "The directorate organises its youngest members into wardens who patrol streets, guard depots and keep the shelter "
          "rolls in every district. In the empty districts they bring a presence the state never had. In the plant towns they "
          "watch the managers and report on them, and skilled engineers begin to look for work abroad rather than answer to a "
          "warden.",
          ('security', 'civil'), after=('pol_vigilance_directorate',),
          exclusive=('pol_chamber_charter', 'pol_plant_compact', 'pol_shield_statute'),
          reward=(SwapIdea('vigilance_rallies', 'vigilance_wardens'),)),
    Focus('pol_shield_statute', 'Publish the Shield Statute',
          "Pressed by the plant owners and by foreign suppliers, the council publishes a statute listing its powers, the "
          "emergency it claims to face and the tests it must meet before civilians govern again. Nobody expects those tests to "
          "be passed soon, yet the newspapers measure the council against them every month. The officers win some patience and "
          "lose the right to rule without explaining themselves.",
          ('document', 'radar'), after=('pol_shield_council',),
          exclusive=('pol_chamber_charter', 'pol_plant_compact', 'pol_vigilance_wardens'),
          reward=(SwapIdea('shield_officers', 'shield_statute'),)),
    Focus('pol_settled', 'An Order That Holds',
          "By whichever road Silvonia travelled, the quarrels of the early nineties harden into habit. Deputies, councils or "
          "commissioners now answer the same questions the same way each year, and the plant offices have learned which door "
          "to knock on. Nobody has to love the arrangement. Foreign lenders and the firms that sell engines and radar spares can "
          "price it, and cheaper credit follows.",
          ('peace', 'assembly'),
          after_any=('pol_chamber_charter', 'pol_plant_compact', 'pol_vigilance_wardens', 'pol_shield_statute'),
          reward=(Flag('order_settled'), Stability(0.04))),
))

DISTRICTS = Branch('dist', 'Three Plant Towns and Seven Empty Districts', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dist_census', 'Count the Ten Districts',
          "Silvonia's ten districts are wildly unequal. The Capital District, District B and District F hold all the plants; "
          "District A holds the naval base and the yards; the other six are towns without a single plant, and none of them has a "
          "road worth the name. A census by district settles who lives where, who pays what and where the first road money "
          "ought to go.",
          ('document', 'civil'), reward=(Idea('district_survey'), Event('ten_districts'))),
    Focus('dist_junction', 'The Junction in District J',
          "Every railway in Silvonia except the line to District B passes through District J, where the track from the capital "
          "splits for the yards of District A and the plants of District F. Yet District J itself has no paved road and no "
          "sidings worth the name. Grading its roads and widening its yards relieves the one bottleneck that most trains in the "
          "country must cross.",
          ('rail', 'logistics'), after=('dist_census',), reward=(Build('infrastructure', 1, 588),)),
    Focus('dist_plain_c', 'Roads Across the District C Plain',
          "District C is the largest farming district, seventeen provinces of open plain running to the Verusan frontier, and it "
          "has no road a truck can use in the wet season. Grain reaches the capital late or not at all. Gravel roads across the "
          "plain cost little per kilometre and a great deal in total, and Verusan traders will use them as well.",
          ('logistics', 'civil'), after=('dist_census',), reward=(Build('infrastructure', 1, 202),)),
    Focus('dist_hills_g', 'A Hill Road for District G',
          "District G lies in the hills where Silvonia meets both Sfaenland and Luremia, and its towns are reached by tracks "
          "graded for carts. A proper road from the capital brings mail, doctors and tax collectors within a season. It also "
          "makes the frontier easier to reach for anyone travelling the other way, which the garrison officers point out at "
          "every single meeting.",
          ('bridge', 'logistics'), after=('dist_census',), reward=(Build('infrastructure', 1, 484),)),
    Focus('dist_rails', 'Extend the Rail Spine',
          "The railway already carries the plants' freight from the capital to District B, District F and the coast. The rail "
          "faction wants every new kilometre of transport money to extend that spine into the empty districts, starting with the "
          "desert of District H. Track is slow to lay and costly per kilometre, but a single train moves more than a hundred "
          "trucks and burns far less fuel.",
          ('rail', 'tools'), after_any=('dist_junction', 'dist_plain_c', 'dist_hills_g'), cost=10,
          exclusive=('dist_gravel',), reward=(SwapIdea('district_survey', 'rail_first'), Flag('rails_first'))),
    Focus('dist_gravel', 'Gravel Before Rails',
          "The road faction argues that the empty districts need a little access everywhere rather than a lot of access in one "
          "place. Graded gravel roads can reach every town within a few years for the cost of one rail line. Trucks burn fuel "
          "that Silvonia must ration for its fighters, and the roads wash out in every heavy season, but nobody is left "
          "waiting at the end of a track.",
          ('logistics', 'tools'), after_any=('dist_junction', 'dist_plain_c', 'dist_hills_g'), cost=10,
          exclusive=('dist_rails',), reward=(SwapIdea('district_survey', 'road_first'), Flag('roads_first'))),
    Focus('dist_desert_spur', 'A Rail Spur into District H',
          "District H is twenty-six provinces of desert along the Verusan and Yuktobanian frontiers, larger than the three plant "
          "districts together and almost empty. A rail spur from the capital gives its oases a lifeline and lets a garrison "
          "reach the frontier in hours. Sand drifts over the track every dry season, and the crews that clear it will never be "
          "finished.",
          ('rail', 'bridge'), after=('dist_rails',), requires=(HasFlag('rails_first'),),
          reward=(Build('infrastructure', 2, 578),)),
    Focus('dist_desert_tracks', 'Marked Tracks Across the Desert',
          "Under the road plan, District H gets marked and graded tracks with fuel caches, wells and telephone posts every fifty "
          "kilometres. It is cheap and quick and serves the few herding families and frontier posts well enough. Heavy freight "
          "still cannot cross the desert, and the army complains that a convoy needs three days to reach the far frontier.",
          ('logistics', 'telescope'), after=('dist_gravel',), requires=(HasFlag('roads_first'),),
          reward=(Build('infrastructure', 1, 578), PP(15))),
    Focus('dist_mountain_towns', 'Winter Roads for D and I',
          "District D and District I are mountain country on the Kaluga frontier, and every winter their passes close for weeks. "
          "Townspeople stock up in autumn and hope. Cutting all-weather roads with snow shelters keeps the towns supplied and "
          "lets the frontier posts be relieved on time. The blasting crews must be paid through two winters, and the work is "
          "dangerous.",
          ('bridge', 'civil'), after_any=('dist_rails', 'dist_gravel'),
          reward=(Build('infrastructure', 1, 205), Build('infrastructure', 1, 583))),
    Focus('dist_marsh_causeway', 'A Causeway Through the Marsh',
          "District A's naval base and yards sit behind jungle and marsh, and the line from the junction reaches them over a "
          "single embankment that floods each wet season. Raising a causeway beside the track gives trucks a second route to "
          "the coast and the escorts a second supply line. The marshes swallow fill faster than the engineers predicted, and "
          "the budget swells to match.",
          ('bridge', 'navy'), after=('dist_junction',), reward=(Build('infrastructure', 1, 45),)),
))

INDUSTRY = Branch('ind', 'The Three Plant Districts', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('ind_registry', 'Register Every Pit and Well',
          "Oil, steel ore, bauxite and rubber come from only three districts: the Capital District, District B and District F. "
          "Each plant keeps its own figures and each ministry trusts different ones. A registry of every pit, well and "
          "plantation, inspected in person, costs a year of engineers' time and exposes every owner who has been underreporting "
          "output to the tax office.",
          ('document', 'industry'), reward=(Idea('ore_registry'), Event('ore_count'))),
    Focus('ind_last_plot', 'The Last Plot in the Capital',
          "The Capital District is a crowded city of four hill provinces with room for exactly one more large plant. Every "
          "ministry wants that plot: the air staff for a parts works, the plant owners for a consumer factory, the housing office "
          "for flats. The cabinet gives it to a general works that can switch between civil and defence orders as the years "
          "require.",
          ('industry', 'civil'), after=('ind_registry',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('ind_rubber_f', 'Rubber from the District F Jungle',
          "District F's jungle provinces hold much of the country's rubber, tapped by smallholders who sell to whichever buyer "
          "reaches them first. Agronomists and surveyors from the capital map the plantations, access tracks and yields. Better "
          "tapping and processing could double output within a few years, if the smallholders trust the ministry long enough "
          "to try the new methods.",
          ('tools', 'economy'), after=('ind_registry',), reward=(Research('excavation_tech', 0.5, 1),)),
    Focus('ind_wings', 'Aluminium for Our Own Wings',
          "Silvonia mines bauxite and smelts aluminium in all three plant districts, then sells most of it abroad and buys back "
          "aircraft parts at many times the price. The air staff wants the metal kept at home for airframes, spares and radar "
          "masts. The plants would earn less hard currency and gain a customer that never misses an order or argues about "
          "delivery.",
          ('air', 'industry'), after=('ind_registry',), cost=10, exclusive=('ind_ingots',),
          reward=(Idea('aluminium_for_wings'), Flag('metal_wings'))),
    Focus('ind_ingots', 'Ingots for the Railhead',
          "The plant owners prefer to keep selling ingots, steel billets and crude abroad, loading them at the railheads for the "
          "coast and the frontier crossings. Foreign currency pays for the fuel and engines the air arm cannot make at home. "
          "Prices abroad swing wildly, and in a bad year the treasury discovers how much of the budget depended on them.",
          ('economy', 'rail'), after=('ind_registry',), cost=10, exclusive=('ind_wings',),
          reward=(Idea('metal_exports'), Flag('metal_sales'))),
    Focus('ind_rolling_mill', 'A Rolling Mill at the Junction',
          "Under the wings policy, a rolling mill and press shop rise in District J beside the rail junction, turning ingots from "
          "the plant districts into sheet and extrusions for airframe repair. The district gains its first plant and several "
          "hundred jobs. Skilled hands must be lured from the capital with housing grants that the treasury had not planned for.",
          ('industry', 'rail'), after=('ind_wings',), requires=(HasFlag('metal_wings'),),
          reward=(Build('arms_factory', 1, 588),)),
    Focus('ind_coast_sheds', 'Export Sheds on the District A Quays',
          "Under the export policy, bonded sheds and a loading plant go up beside the yards of District A, so metal can leave by "
          "sea as well as by rail. The marsh coast gains steady work and the yards gain repair business from visiting ships. "
          "Every ton that sails is a ton the air arm will one day have to buy back at a higher price.",
          ('navy', 'economy'), after=('ind_ingots',), requires=(HasFlag('metal_sales'),),
          reward=(Build('industrial_complex', 1, 45),)),
    Focus('ind_silo_rule', 'Keep the Fuel Silo Full',
          "Silvonia has a single fuel silo, in the Capital District, and it feeds the fighters, the trucks and the trains alike. "
          "In a crisis it would run dry within weeks. A rule that the silo must never fall below a fixed reserve forces the "
          "refineries to hold back fuel that could have been sold. The plant owners grumble; the air staff sleeps better.",
          ('logistics', 'shelter'), after=('ind_registry',), reward=(Idea('silo_reserve'),)),
    Focus('ind_plain_works', 'Workshops on the District C Plain',
          "With a road across the District C plain at last, a workshop town can serve the farms with tractor repair, pumps and "
          "grain mills instead of sending every broken machine to the capital. It is the first plant in a district that never "
          "had one. The owners in the old plant districts oppose it as competition, then quietly bid for its contracts.",
          ('tools', 'industry'), after=('ind_registry',), requires=(Completed('dist_plain_c'),),
          reward=(Build('industrial_complex', 1, 202),)),
    Focus('ind_council_dividend', 'A Dividend for the Empty Districts',
          "Under the plant council, the owners agree to pay a share of plant profits into a fund for the seven districts without "
          "industry. The sums are modest and the council decides who receives them, but the money builds schools and wells "
          "where the state never reached. Critics call it a bribe for good behaviour. The empty districts take the money anyway.",
          ('economy', 'civil'), after=('ind_registry',), requires=(HasFlag('gov_plants'),),
          reward=(Idea('district_dividend'),)),
))

WORKS = Branch('works', 'Keeping Sixty Aircraft Flying', 1991, 'FOCUS_FILTER_RESEARCH', (
    Focus('works_airworthy', 'How Many Can Fly Today',
          "The air arm lists forty-eight fighters and twelve ground-support aircraft, but nobody has asked how many could take "
          "off tomorrow morning. A full inspection of every airframe, engine and radio on the capital field answers the "
          "question and embarrasses several officers. Without that answer, every later decision about the air arm is guesswork "
          "dressed up as planning.",
          ('tools', 'air'), reward=(Event('grounded_aircraft'), Research('industry', 0.5, 1))),
    Focus('works_depot', 'The Central Repair Depot',
          "Repairs are done wherever a mechanic happens to be, with parts borrowed from whichever aircraft has been grounded "
          "longest. A central depot beside the capital field, with its own stores, test benches and records, ends the "
          "cannibalising. It takes the best mechanics away from the flight line for a year, and the squadrons resent losing "
          "them.",
          ('tools', 'industry'), after=('works_airworthy',), reward=(Idea('repair_depot'),)),
    Focus('works_spares', 'A Pool of Spares',
          "The depot keeps one pool of spares for the whole air arm, bought in bulk, logged by serial number and issued against "
          "signed requests. Foreign suppliers give better prices for larger orders, and the treasury pays in advance for parts "
          "that may sit on shelves for years. Squadron commanders lose the private stores they used to keep under their desks.",
          ('logistics', 'tools'), after=('works_depot',), reward=(Idea('spares_pool'),)),
    Focus('works_licence', 'A Trainer Built Under Licence',
          "One camp in the ministries wants to buy a licence to assemble a proven foreign trainer and its spares at home. The "
          "design is safe and the tooling arrives in crates with instructions. Royalties flow abroad for every airframe and the "
          "licence forbids exports, but within three years Silvonian hands would be building aircraft that actually fly.",
          ('document', 'industry'), after=('works_depot',), cost=10, exclusive=('works_design',),
          reward=(Idea('licence_line'), Flag('airframe_licence'))),
    Focus('works_design', 'Draw Our Own Trainer',
          "The other camp wants a small design office to draw a Silvonian trainer from the ground up, using home aluminium and "
          "engines bought abroad. It will take longer, fail more often and cost more in its first decade. If it works, the "
          "country owns the drawings, may sell the aircraft to anyone and keeps engineers who know why things break.",
          ('science', 'air'), after=('works_depot',), cost=10, exclusive=('works_licence',),
          reward=(Idea('home_design'), Flag('airframe_design'))),
    Focus('works_assembly_hall', 'An Assembly Hall in District D',
          "The licensed line needs a hall, and District D's mountain valleys offer cheap land, hydropower and distance from the "
          "frontier plains. Assembly jigs arrive by rail and mechanics are trained by the licensor's instructors. The mountain "
          "towns gain their first industry. Every engine still comes from abroad, and arrives when the supplier pleases.",
          ('industry', 'air'), after=('works_licence',), requires=(HasFlag('airframe_licence'),),
          reward=(Build('arms_factory', 1, 205),)),
    Focus('works_test_shop', 'A Test Shop in the Mountains',
          "The design office takes over an engineering shop in District D, with a small wind tunnel, a structures laboratory and "
          "an engine stand. The engineers have room to test without the capital watching every failure. The first prototypes "
          "are late and overweight, and the early test flights make the ministers nervous for reasons the engineers struggle "
          "to explain.",
          ('science', 'tools'), after=('works_design',), requires=(HasFlag('airframe_design'),),
          reward=(Build('industrial_complex', 1, 205), Research('electronics', 0.5, 1))),
    Focus('works_overhaul', 'An Engine Overhaul Line',
          "Engines are the one part Silvonia cannot make and cannot do without. An overhaul line that strips, inspects and "
          "rebuilds them at home, instead of shipping them abroad for months, keeps more aircraft flying and teaches the "
          "engineers what wears out first. The line consumes spares at an alarming rate in its first year, and the depot learns "
          "to count again.",
          ('tools', 'rebuild'), after_any=('works_assembly_hall', 'works_test_shop'),
          reward=(Research('engineers_tech', 0.5, 1), Flag('overhaul_line'))),
    Focus('works_radar_benches', 'Radar Repair Benches',
          "Radar and radio sets fail more often than airframes and are harder to fix, because only a handful of technicians "
          "understand them. Benches at the depot for radar and radio repair, with a training course attached, end the practice "
          "of sending sets abroad for every fault. The course draws the brightest mechanics away from the airframes, which the "
          "squadrons notice.",
          ('radar', 'tools'), after=('works_spares',), reward=(Research('radar_tech', 0.5, 1),)),
))

AIR = Branch('air', 'Sixty Aircraft on One Field', 1991, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_one_field', 'Sixty Aircraft, One Runway',
          "Every combat aircraft Silvonia owns sits on one small field in the Capital District: forty-eight fighters, twelve "
          "ground-support aircraft and the reserve airframes, all beside the only fuel silo. One accident on the runway, one fire "
          "in the fuel store or one well-placed raid would ground the entire air arm at once. Admitting the problem is easy; "
          "paying to solve it is not.",
          ('air', 'runway'), reward=(Idea('one_field_wing'), Event('one_field'))),
    Focus('air_longer_runway', 'Lengthen the Capital Runway',
          "The capital field was built for propeller aircraft, and its short runway limits how much fuel and how many weapons a "
          "fighter can carry. Lengthening it, adding taxiways and building hardened shelters means blasting into the hillside "
          "and closing the field for months while the fighters fly from improvised strips. Afterwards the field can handle any "
          "aircraft the air arm is likely to own.",
          ('runway', 'tools'), after=('air_one_field',), reward=(Build('air_base', 2, 0),)),
    Focus('air_field_b', 'A Dispersal Field in District B',
          "District B's mountain valleys have room for a second field near the logistics centre, close to the Yuktobanian and "
          "Kaluga frontiers. A field there splits the air arm in two so that no single blow can ground it, and puts fighters "
          "nearer the passes. The mountain weather will close it on more days than the planners are willing to admit.",
          ('runway', 'air'), after=('air_one_field',), reward=(Build('air_base', 2, 79),)),
    Focus('air_strip_f', 'A Jungle Strip in District F',
          "District F's coastal jungle needs a strip for the southern approaches and for flights to its plant town. Clearing a "
          "runway through jungle is slow, and the humidity rots anything that is not sealed. The strip covers the coast and the "
          "Verusan frontier, and gives the ground-support aircraft a field close to the valleys where they would have to fight.",
          ('runway', 'civil'), after=('air_one_field',), reward=(Build('air_base', 1, 249),)),
    Focus('air_interceptors', 'Interceptors Above All',
          "The interceptor school argues that Silvonia's whole purpose in the air is to deny its sky to anyone else. Every "
          "fighter should be configured, trained and based for interception, with ground support left to the army's guns. It "
          "suits a territorial air defence. It also leaves the battalions in the mountains alone if anything ever crosses the "
          "frontier on the ground.",
          ('air', 'radar'), after=('air_longer_runway',), cost=10, exclusive=('air_valleys',),
          reward=(Idea('interceptor_doctrine'), Flag('doctrine_intercept'))),
    Focus('air_valleys', 'Wings for the Valley Battalions',
          "The support school points out that Silvonia's frontiers run through mountains and desert, where a battalion with air "
          "support is worth three without. It wants the fighters trained to escort the ground-support aircraft and to strike as "
          "well as intercept. The air arm would become more useful to the army and less certain of holding its own sky.",
          ('air', 'training'), after=('air_longer_runway',), cost=10, exclusive=('air_interceptors',),
          reward=(Idea('support_doctrine'), Flag('doctrine_support'))),
    Focus('air_alert_pairs', 'Two Fighters on Alert',
          "Under the interceptor doctrine, two fighters sit armed and fuelled at the end of the runway day and night, with pilots "
          "in the ready room and ground crews beside them. Reaction time falls from twenty minutes to five. The airframes wear "
          "faster and the pilots on alert duty fly less, but every intruder now meets Silvonian aircraft.",
          ('air', 'security'), after=('air_interceptors',), requires=(HasFlag('doctrine_intercept'),),
          reward=(Idea('alert_pairs'), XP('air', 10))),
    Focus('air_pass_strip', 'A Forward Strip Near the Passes',
          "Under the support doctrine, a short gravel strip in District I's mountain valleys lets ground-support aircraft refuel "
          "and rearm within minutes of the passes they would defend. Pilots train with the battalions on the frontier and learn "
          "the valleys by sight. The strip cannot take fighters in bad weather, and all of its fuel arrives by truck.",
          ('runway', 'training'), after=('air_valleys',), requires=(HasFlag('doctrine_support'),),
          reward=(Build('air_base', 1, 583), XP('air', 10))),
    Focus('air_school', 'The Hill Pilot School',
          "Silvonia has been sending its pilot candidates abroad and losing some of them to foreign airlines. A school at home, "
          "flying from the capital field and later from the dispersal fields, trains pilots for the mountain weather and short "
          "runways they will actually use. Instructors are scarce, and the first classes are painfully small.",
          ('training', 'air'), after=('air_one_field',), reward=(Idea('pilot_school'),)),
    Focus('air_aggressors', 'Contract Aggressor Pilots',
          "From 1998 former Belkan Air Force pilots hire themselves out to foreign air arms as aggressor squadrons. The hill "
          "school could contract a few to fly against its students and squadron pilots, teaching the tactics a real enemy would "
          "use. The fees are high, the instructors are blunt, and deputies ask exactly whom these pilots flew for.",
          ('medal', 'air'), after=('air_school',), requires=(After('1998.6.19'),),
          reward=(TimedIdea('aggressor_course', 730),)),
    Focus('air_reserve_flight', 'Fly the Reserve Airframes',
          "Twelve fighters and four ground-support aircraft have sat in storage since they were delivered, kept as replacements. "
          "With the overhaul line running, the depot can rotate them into a reserve squadron flown by instructors and "
          "reservists. They will wear out sooner, but a reserve that never flies is a reserve nobody knows how to use.",
          ('air', 'rebuild'), after=('air_school',), requires=(HasFlag('overhaul_line'),),
          reward=(Idea('reserve_squadron'),)),
))

NET = Branch('net', 'The Warning Net', 1991, 'FOCUS_FILTER_AIR_XP', (
    Focus('net_observers', 'Observers on the Hilltops',
          "Silvonia has fighters but no radar, so the only warning of an intruder is a farmer's telephone call. A corps of "
          "volunteer observers on hilltops in every district, with binoculars, recognition charts and field telephones to the "
          "capital, costs little and can start at once. It works only by day and in clear weather, which is at least a "
          "beginning.",
          ('telescope', 'communications'), reward=(Idea('observer_corps'), Event('unknown_contact'))),
    Focus('net_first_radar', 'A Radar on the Capital Hills',
          "A single search radar on the highest hill of the Capital District covers the capital, its plants and the only air "
          "base. It needs power, a road, a guard company and technicians who must be trained abroad. The first time it tracks an "
          "airliner across the whole country, the air staff understands what it has been missing for decades.",
          ('radar', 'tools'), after=('net_observers',), reward=(Build('radar_station', 1, 0),)),
    Focus('net_forward', 'Radar Along the Frontiers',
          "One school wants radar stations on the frontiers, where an intruder would first appear: the passes of District B, the "
          "desert of District H, the hills facing Sfaenland and Luremia. Early warning buys the fighters time to climb. Forward "
          "stations are expensive to guard and supply, and they would be the first thing lost in a real war.",
          ('radar', 'security'), after=('net_first_radar',), cost=10, exclusive=('net_ring',),
          reward=(Idea('frontier_radar'), Flag('radar_forward'))),
    Focus('net_ring', 'A Ring Around the Capital',
          "The other school wants every radar, gun and shelter concentrated around the Capital District, where the plants, the "
          "fuel silo and the air base sit within a few hills of each other. A dense ring defends what matters most and is easy "
          "to supply. Intruders would be seen late, and everything outside the ring would be left to the observers.",
          ('shelter', 'radar'), after=('net_first_radar',), cost=10, exclusive=('net_forward',),
          reward=(Idea('capital_ring'), Flag('radar_ring'))),
    Focus('net_station_b', 'A Radar Above the District B Passes',
          "Under the forward plan, a radar station on the ridges of District B watches the mountain approaches from Yuktobania "
          "and Kaluga. Its crews live on the ridge for months at a time, and the access road is closed by snow every winter. "
          "When it works, the capital field gets warning long before anything can reach the plants.",
          ('radar', 'rail'), after=('net_forward',), requires=(HasFlag('radar_forward'),),
          reward=(Build('radar_station', 2, 79),)),
    Focus('net_station_h', 'A Desert Radar in District H',
          "Under the forward plan, a station in the open desert of District H covers the long Verusan and Yuktobanian frontier, "
          "where nothing larger than a herding camp moves for days. Dust ruins the electronics and water must be trucked in. "
          "The station sees farther than any other in the country, and its crews see almost nobody at all.",
          ('radar', 'logistics'), after=('net_forward',), requires=(HasFlag('radar_forward'),),
          reward=(Build('radar_station', 1, 578),)),
    Focus('net_gun_belt', 'Gun Belts Around the Plants',
          "Under the ring plan, anti-aircraft batteries circle the plants of the Capital District in overlapping belts, with "
          "spotters on the rooftops and shelters for the gun crews. Residents wake to practice firing and complain about the "
          "noise. The plants become the hardest targets in the country, and the rest of the country notices the difference.",
          ('security', 'industry'), after=('net_ring',), requires=(HasFlag('radar_ring'),),
          reward=(Idea('gun_belts'),)),
    Focus('net_second_radar', 'More Radar for the Ring',
          "Under the ring plan, further radar sets on the capital's hills cover each other's blind spots and keep watching when "
          "one set is down for repair. The ring now sees in every direction and fighters can be guided from the ground. All of "
          "it sits within a short drive of the city, which keeps it cheap to run and easy to guard.",
          ('radar', 'civil'), after=('net_ring',), requires=(HasFlag('radar_ring'),),
          reward=(Build('radar_station', 2, 0),)),
    Focus('net_bunker', 'The Control Bunker Under the Hills',
          "Radar tracks, observer reports and fighter orders all pass through a single plotting room above ground in the "
          "capital. A control bunker cut into the hills protects that room, adds backup power and radios, and lets one duty "
          "officer see the whole sky. It costs as much as a squadron of fighters and will never appear in a parade.",
          ('shelter', 'command'), after_any=('net_station_b', 'net_station_h', 'net_gun_belt', 'net_second_radar'), cost=10,
          reward=(Idea('control_bunker'),)),
    Focus('net_landlines', 'Landlines to Every Post',
          "The posts report by radio, which jams, fades and can be overheard by anyone with a receiver. Buried landlines along "
          "the railways and roads link every observer post and radar station to the bunker. The cable crews follow the rail "
          "spine and then dig the rest by hand. Once finished, the net speaks without being heard and keeps working through "
          "storms.",
          ('communications', 'rail'), after=('net_bunker',),
          reward=(Research('radar_tech', 0.5, 2), Flag('net_linked'))),
    Focus('net_council_plot', 'The Council Takes the Plot',
          "Under the Air Shield Council, the control bunker becomes the seat of government in all but name: council members take "
          "turns as duty officers and see every track for themselves. Decisions about the sky are made in seconds. Decisions "
          "about schools, wages and roads wait outside the blast door until someone remembers to open it.",
          ('command', 'radar'), after=('net_bunker',), requires=(HasFlag('gov_shield'),),
          reward=(Idea('plot_room_rule'),)),
))

ARMY = Branch('army', 'Seven Formations in the Hills', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('army_winter', 'Winter Exercise in the Passes',
          "Silvonia's seven infantry formations are spread between the Capital Centre, the logistics centres of District B and "
          "District F and the naval base in District A. None has trained above battalion level in years. A winter exercise in "
          "District B's mountains, with all seven moving at once, will show what works and who has been signing paper returns.",
          ('training', 'security'), reward=(Idea('formation_rolls'), Event('mountain_exercise'))),
    Focus('army_mountain', 'Mountain Battalions',
          "The army already holds a mountaineering doctrine on paper. The mountain faction wants it in every formation: skis, "
          "pack animals, cold-weather training and battalions based permanently in the passes of District B, District D and "
          "District I. Such troops would hold the frontier hills against anyone, and they would be slow almost everywhere else.",
          ('training', 'tools'), after=('army_winter',), cost=10, exclusive=('army_rail',),
          reward=(Idea('mountain_battalions'), Flag('army_hills'))),
    Focus('army_rail', 'A Reserve That Travels by Rail',
          "The rail faction wants the seven formations held in the centre, near the junction in District J, with trains ready to "
          "move any of them to any frontier within a day. Fewer troops would sit in the passes. A central reserve covers every "
          "frontier at once, as long as the railway and its timetables survive whatever is coming.",
          ('rail', 'command'), after=('army_winter',), cost=10, exclusive=('army_mountain',),
          reward=(Idea('rail_reserve'), Flag('army_trains'))),
    Focus('army_pass_posts', 'Posts on the Kaluga Passes',
          "Under the mountain plan, permanent posts with heated barracks and supply roads go up on the passes of District I that "
          "face Kaluga and Luremia. Patrols can now stay out through the winter. The posts are expensive and lonely, and the "
          "soldiers stationed there call them the edge of the world in their letters home.",
          ('security', 'bridge'), after=('army_mountain',), requires=(HasFlag('army_hills'),),
          reward=(Build('infrastructure', 1, 583), XP('army', 10))),
    Focus('army_sidings', 'Troop Sidings at the Junction',
          "Under the rail plan, the junction in District J gets military sidings, loading ramps and a depot where each "
          "formation's heavy equipment waits on flatcars. A formation can entrain in hours rather than days. The plant owners "
          "complain that troop trains now have priority over freight on the busiest line in the country.",
          ('rail', 'logistics'), after=('army_rail',), requires=(HasFlag('army_trains'),),
          reward=(Build('infrastructure', 1, 588), XP('army', 10))),
    Focus('army_field_guards', 'Guards for Every Airfield',
          "Every airfield, radar station and fuel store needs guards, and so far the air staff has borrowed them from the "
          "infantry one company at a time. Dedicated guard companies with their own vehicles and anti-aircraft machine guns "
          "free the formations for the frontier and give the air arm guards who know what they are guarding.",
          ('security', 'runway'), after=('army_winter',), reward=(Idea('airfield_guards'),)),
    Focus('army_runway_engineers', 'Engineers Who Mend Runways',
          "Each formation carries an engineer company, trained mostly for bridges and mines. Retraining them to repair cratered "
          "runways, clear wreckage and lay temporary strips makes the dispersal fields far harder to close. The engineers learn "
          "the work quickly, and the air staff soon learns to ask for particular companies by name.",
          ('tools', 'runway'), after=('army_field_guards',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('army_desert_patrol', 'Patrols in the Empty Desert',
          "District H's desert frontier with Verusa and Yuktobania is watched by nobody. Motorised patrols with long-range "
          "radios, water trucks and local guides cover it in rotations of a month each. They find smugglers, lost herders and "
          "once a crashed weather balloon. Above all they tell the government what happens along its longest frontier.",
          ('logistics', 'security'), after=('army_winter',), reward=(Idea('desert_patrols'),)),
    Focus('army_vigilance_volunteers', 'Volunteers of the Movement',
          "Under the directorate, the movement's volunteers form part-time companies in the seven districts without plants, "
          "drilling at weekends and guarding bridges, depots and hilltop posts. They give the empty districts a role in the "
          "defence of the country for the first time. Regular officers distrust units whose loyalty runs to the movement first.",
          ('security', 'medal'), after=('army_winter',), requires=(HasFlag('gov_vigilance'),),
          reward=(Idea('vigilance_companies'),)),
))

FRONTIERS = Branch('fr', 'Five Frontiers and a Distant War', 1991, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('fr_airspace', 'Charting the Airspace Edges',
          "Silvonia borders Yuktobania, Kaluga, Verusa, Sfaenland and Luremia, and none of those frontiers has an agreed line in "
          "the sky. Airliners, survey flights and the odd military aircraft cross without notice. Charting the airspace edges "
          "on the Silvonian side, with reporting points and radio frequencies, costs months of meetings and gives the fighters "
          "rules for every encounter.",
          ('document', 'air'), reward=(Idea('airspace_charts'),)),
    Focus('fr_belkan_war', 'Belka Goes to War, Far Away',
          "On 25 March 1995 war breaks out around Belka. Silvonia is no party to it and lies far from the fighting, but airliners "
          "reroute across distant skies, insurers raise their rates and fuel prices jump. The air staff asks for higher "
          "readiness, the plant owners ask for orders, and the ministries ask what Silvonia intends to say.",
          ('communications', 'security'), after=('fr_airspace',), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war'), TimedIdea('war_watch', 365))),
    Focus('fr_closed_sky', 'Close the Sky to Belligerents',
          "The strict camp wants Silvonian airspace closed to every aircraft of a belligerent state, military or civil, for as "
          "long as the war lasts. The fighters would intercept every unidentified contact. Neutrality would be visible and "
          "enforced. Some airlines would reroute and take their fees with them, and an interception could go wrong at any "
          "moment.",
          ('security', 'air'), after=('fr_belkan_war',), exclusive=('fr_corridors',),
          reward=(Idea('closed_sky'), Flag('sky_closed'))),
    Focus('fr_corridors', 'Civil Corridors Stay Open',
          "The moderate camp wants civil corridors kept open to every airline that files a flight plan, with the military "
          "aircraft of any state refused. Overflight fees keep flowing and the fighters only meet aircraft that stray from the "
          "corridors. Neutrality becomes a matter of paperwork, which suits the ministries and alarms the air staff.",
          ('peace', 'air'), after=('fr_belkan_war',), exclusive=('fr_closed_sky',),
          reward=(Idea('open_corridors'), Flag('sky_open'))),
    Focus('fr_intercept_rules', 'Rules for Meeting Strangers',
          "Closing the sky means the fighters will meet strangers, and the pilots want rules: when to signal, when to shadow, "
          "when to escort a stranger out and who may order anything more. The rules are written by lawyers and pilots in the "
          "same room, which takes longer than either side expected. Every pilot now carries a copy in the cockpit.",
          ('document', 'security'), after=('fr_closed_sky',), requires=(HasFlag('sky_closed'),),
          reward=(XP('air', 20), PP(-10))),
    Focus('fr_overflight_fees', 'A Fee for Every Overflight',
          "With the corridors open, airlines rerouted by the war cross Silvonia daily. A published overflight fee, collected "
          "through the airlines' agents, brings in hard currency the ministries badly need. The capital radar must track every "
          "civil flight it charges, which keeps the crews busier and better trained than any exercise could.",
          ('economy', 'air'), after=('fr_corridors',), requires=(HasFlag('sky_open'),),
          reward=(Idea('overflight_fees'),)),
    Focus('fr_fallout', 'Sampling the Wind for Fallout',
          "In June 1995 the Belkan Army uses seven nuclear devices in the Waldreich Mountains. Nobody in Silvonia can say how far "
          "the fallout will drift. Weather stations and the hill observers start sampling wind and rain, and the ministry "
          "publishes the readings every week. The figures calm the public or frighten it, depending on the week.",
          ('telescope', 'medical'), after=('fr_belkan_war',), requires=(After('1995.6.6'), HasGlobal('belka_dropped_nukes')),
          reward=(Idea('fallout_watch'),)),
    Focus('fr_lumen', 'Standing Down After Lumen',
          "On 20 June 1995 a treaty is signed in Lumen and the Belkan War ends. Silvonia stands down its higher readiness and "
          "counts the cost: fuel burned, hours flown, contracts gained and lost. The air staff writes a report on what a distant "
          "war taught a country that only watched it, and asks that the report not be shelved.",
          ('peace', 'document'), after=('fr_belkan_war',), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_watch'), Stability(0.02))),
    Focus('fr_belka_stands', 'Orders from a Belka That Won',
          "In this outcome Belka has won its war, and its purchasing missions seek metal, rubber and fuel for rearmament and "
          "rebuilding. Silvonian plants could sell everything they make. Other customers watch who supplies Belka, and the air "
          "staff wonders aloud what a victorious Belka will want next.",
          ('diplomacy', 'economy'), after=('fr_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(Idea('belkan_orders'),)),
    Focus('fr_belka_falls', 'How Belka Lost Its Sky',
          "In this outcome Belka has lost its war, and with it a sky its air force once dominated. Silvonian staff officers study "
          "how an air defence that strong was overcome: which radars fell silent first, which fields were struck, which crews "
          "kept flying. The lessons are uncomfortable for a country with one field and very little radar.",
          ('science', 'air'), after=('fr_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Research('air_doctrine', 0.5, 1),)),
))

SKY = Branch('sky', 'The Asteroid on the Plotting Table', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_first_warning', 'The Astronomers Raise a Warning',
          "In December 1994 the world's astronomers announce that a newly tracked asteroid, Ulysses, is coming near and might "
          "hit. Silvonia owns no observatory worth mentioning, but its air staff employs the only people in the country who "
          "watch the sky for a living. The ministries ask the radar crews and hilltop observers, only half joking, to keep an "
          "eye on it as well.",
          ('telescope', 'meteor'), requires=(After('1994.12.10'),), reward=(Idea('sky_tracking'),)),
    Focus('sky_impact_announced', 'The FCU Confirms the Impact',
          "On 20 April 1996 the President of the FCU announces that Ulysses will strike the Earth. Where its fragments will fall "
          "is unknown. Silvonia's plants, fuel silo and air base all sit in a few hill provinces of the capital, and a single "
          "fragment there could end the country's industry. The ministries must decide what to protect first.",
          ('meteor', 'communications'), after=('sky_first_warning',), requires=(After('1996.4.20'),),
          reward=(Event('ulysses_will_strike'),)),
    Focus('sky_empty_capital', 'Plan to Empty the Capital',
          "One plan moves people away from the danger: timetables to empty the capital and the plant towns by rail into the open "
          "districts, with camps, water and food waiting there. The railway can carry the numbers if nothing else moves. The "
          "plan needs the help of districts that have never received anything from the capital, and they remember that.",
          ('rail', 'refugees'), after=('sky_impact_announced',), exclusive=('sky_galleries',),
          reward=(Idea('evacuation_timetable'),)),
    Focus('sky_galleries', 'Galleries Under the Hills',
          "The other plan keeps people where they live and digs: galleries into the hills of the Capital District, sealed cellars "
          "under the plants, stocks of food and water for weeks. Mining crews from District B do the cutting. The galleries "
          "protect the people who matter most to the economy, and the empty districts note who that turns out to be.",
          ('shelter', 'civil'), after=('sky_impact_announced',), exclusive=('sky_empty_capital',),
          reward=(Idea('hill_galleries'),)),
    Focus('sky_tracking_net', 'Radar Crews Track the Fragments',
          "With the warning net linked by landline, radar crews and observers can follow anything that enters Silvonian skies "
          "and pass the plot to the bunker in seconds. They practise on meteors and weather balloons. On the night the asteroid "
          "passes, the net will be the only part of the state that knows where things are falling.",
          ('radar', 'meteor'), after=('sky_impact_announced',), requires=(HasFlag('net_linked'),),
          reward=(Research('radar_tech', 0.5, 2),)),
    Focus('sky_chamber_drills', 'Drills Debated in the Chamber',
          "Under the reopened chamber, the emergency plans are debated in public, district by district, and every deputy insists "
          "that their towns be included. The drills are larger and slower than the ministries wanted. They are also understood "
          "and attended, because the people practising them chose them through their own deputies.",
          ('ballot', 'shelter'), after=('sky_impact_announced',), requires=(HasFlag('gov_chamber'),),
          reward=(Idea('public_drills'),)),
    Focus('sky_roche_watch', 'The Night the Asteroid Breaks',
          "On 8 July 1999 Ulysses passes through the Roche limit of the Earth. Silvonia spends the night under its evacuation "
          "timetables or in its galleries, with the radar crews on duty and the fighters on alert. Every report is checked twice "
          "and contradicted once. Morning brings the work of finding out what actually happened.",
          ('meteor', 'shelter'), after_any=('sky_empty_capital', 'sky_galleries'), requires=(After('1999.7.8'),),
          reward=(Event('impact_night'),)),
    Focus('sky_debris_sweep', 'Watching the Debris Sweep',
          "In October 1999 Osea and Yuktobania cooperate to convert the Arkbird into a platform for clearing debris from "
          "satellite orbits. Silvonia, which borders Yuktobania, has a warning net built to follow things that are low and fast. "
          "Its radar crews learn to track objects they were never trained for, and the air staff files every plot it makes.",
          ('satellite', 'radar'), after=('sky_roche_watch',), requires=(After('1999.10.8'),),
          reward=(Idea('orbit_watch'),)),
))

CENTURY = Branch('cen', 'The Shield at the Millennium', 2001, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('cen_fleet_ten', 'The Fighters Grow Old',
          "By 2001 the fighters that guarded Silvonia through the nineties are worn, outdated or both. Replacing them would cost "
          "more than the treasury collects in a year. Extending their lives would keep a weaker air arm flying for another "
          "decade. The air staff presents both options with a recommendation it is careful never quite to state.",
          ('air', 'document'), requires=(After('2001.1.1'),),
          reward=(Research('air_doctrine', 0.5, 1), Tooltip('Opens the choice between rebuilding the old fighters and buying new ones.'))),
    Focus('cen_life_extension', 'Ten More Years for Old Airframes',
          "The extension programme rebuilds every fighter at the depot: new wiring, new radios, overhauled engines and "
          "reinforced wings. The aircraft will not be modern, but they will be known, maintained and paid for. The money stays at "
          "home in the depot and the overhaul line, and the pilots fly what they already understand.",
          ('rebuild', 'air'), after=('cen_fleet_ten',), cost=10, exclusive=('cen_new_fighters',),
          reward=(Idea('life_extension'),)),
    Focus('cen_new_fighters', 'A New Interceptor from Abroad',
          "The replacement programme buys a modern interceptor abroad, with training, spares and a support contract. Silvonian "
          "pilots would fly aircraft equal to most in the region. The purchase empties the procurement budget for a decade, "
          "binds the country to a single supplier and leaves the depot with far less to do.",
          ('air', 'diplomacy'), after=('cen_fleet_ten',), cost=10, exclusive=('cen_life_extension',),
          reward=(Idea('new_interceptors'),)),
    Focus('cen_railguns', 'Railguns Turned on the Sky',
          "In mid-2003 news arrives from Usea: Erusean forces have overrun San Salvacion, taken the Stonehenge complex and "
          "turned its giant guns against aircraft. For a country whose entire defence rests on owning its own sky, that report "
          "is a professional shock. Officers in the plotting room ask what fighters, radars and alert pairs are worth against a "
          "weapon of such reach.",
          ('missile', 'radar'), after=('cen_fleet_ten',), requires=(After('2003.6.1'),),
          reward=(Event('railguns_turned'), Idea('railgun_study'))),
    Focus('cen_isaf_spares', 'Spares for the ISAF Squadrons',
          "In August 2003 the FCU establishes the ISAF. Its squadrons need spares, fuel and repair work, and Silvonia's depot "
          "and plants could supply some of them without sending a single pilot. The orders would fill the overhaul line. Erusea "
          "would count Silvonia among its enemies' suppliers, and would say so in public.",
          ('diplomacy', 'tools'), after=('cen_railguns',), requires=(After('2003.8.22'),), exclusive=('cen_no_wings',),
          reward=(Idea('isaf_spares'),)),
    Focus('cen_no_wings', 'Nothing With Wings Leaves',
          "The strict camp wants no aircraft part, fuel or aluminium sheet exported to either side while the Usean war lasts, "
          "with inspectors at the railheads and on the quays of District A. The depot loses its most profitable customer. "
          "Silvonia keeps a neutrality that neither side can question, and its own squadrons keep their spares.",
          ('peace', 'security'), after=('cen_railguns',), exclusive=('cen_isaf_spares',),
          reward=(Idea('no_wings_export'),)),
    Focus('cen_railguns_silent', 'When the Railguns Fall Silent',
          "In this outcome the Stonehenge guns have been wrecked and Usean airspace belongs to aircraft again. The Silvonian "
          "study ends with a conclusion its authors did not expect: the weapon that seemed to make air power obsolete was itself "
          "brought down. The air staff rewrites its doctrine papers, and the treasury asks whether the radar budget may now "
          "shrink.",
          ('peace', 'missile'), after=('cen_railguns',), requires=(HasGlobal('ac_ucw_stonehenge_destroyed'),),
          reward=(SwapIdea('railgun_study', 'railgun_lessons'),)),
    Focus('cen_usean_advisers', 'Advisers for a Rebuilt Usean Sky',
          "In this outcome the ISAF has won the war, and Usean states must rebuild their air defences from wreckage. Silvonian "
          "radar and observer specialists could serve abroad on private contracts as advisers, earning fees and experience. The "
          "government permits individual contracts and commits nothing as a state, which keeps the risk small and the gain "
          "modest.",
          ('diplomacy', 'radar'), after=('cen_railguns',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('usean_contracts', 365),)),
    Focus('cen_erusea_holds', 'A Victor Nobody Expected',
          "In this outcome Erusea has won its war, and every air staff in the world draws the same lesson: whoever holds the sky "
          "holds the ground beneath it. Silvonia lies far from Usea, but its officers ask for more radar watch, more alert hours "
          "and less dependence on foreign spares. The ministries grant the first two and wonder how the third could be done.",
          ('security', 'diplomacy'), after=('cen_railguns',), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Idea('erusean_caution'),)),
    Focus('cen_shield_review', 'Fifteen Years Under the Shield',
          "In 2005 the ministries and the air staff sit together to review the shield they have built since 1991: the fields, "
          "the radar posts, the depot, the pilots and the government that pays for all of it. The review is blunt about what "
          "failed and short on promises. Whoever governs Silvonia next inherits its figures instead of its slogans.",
          ('document', 'medal'), after_any=('cen_life_extension', 'cen_new_fighters'),
          requires=(HasFlag('order_settled'), After('2005.1.1')),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; the later eras are written separately.'))),
))

BRANCHES = (POLITICS, DISTRICTS, INDUSTRY, WORKS, AIR, NET, ARMY, FRONTIERS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('alert_exercise', 'A National Alert Exercise',
                'Every observer post, radar crew and alert pair is tested against a surprise raid flown by the air arm itself. '
                'Repeatable once a year; the exercise burns fuel and flying hours.',
                35, (TimedIdea('alert_drill', 90), XP('air', 10)), requires=(Completed('net_observers'),), cooldown=365),
    DecisionDef('reserve_callup', 'Call Up the Reserve Pilots',
                'Reservists trained at the hill school fly a fortnight with the squadrons. Repeatable every six months.',
                30, (XP('air', 15),), requires=(Completed('air_school'),), cooldown=180),
    DecisionDef('desert_airstrip', 'Grade a Desert Airstrip',
                'Engineers grade a gravel strip beside the District H patrol route for patrol and supply flights. A one-time '
                'works programme.',
                75, (Build('air_base', 1, 578),), requires=(Completed('army_desert_patrol'),)),
    DecisionDef('jungle_hardstands', 'Hardstands for the Jungle Strip',
                'Concrete hardstands and sealed stores let the District F strip hold more aircraft through the wet season. '
                'Once only.',
                60, (Build('air_base', 1, 249),), requires=(Completed('air_strip_f'),)),
    DecisionDef('plant_inspection', 'Inspect a Plant Without Warning',
                'Registry inspectors arrive unannounced at one plant and publish what they find. Repeatable every six months; '
                'the owners resent it.',
                25, (TimedIdea('ledger_inspection', 90),), requires=(Completed('ind_registry'),), cooldown=180),
    DecisionDef('open_hangars', 'Open the Hangars to the Public',
                'The capital field opens its hangars for a day of flying displays and recruiting stands. Repeatable once a year.',
                20, (TimedIdea('hangar_day', 60), Stability(0.01)), requires=(Completed('air_one_field'),), cooldown=365),
)
