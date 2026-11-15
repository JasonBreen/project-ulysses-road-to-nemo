"""Echea (EHE): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections_allowed = no on a 48-month calendar, neutrality 48 and fascism 50
percent popularity), the unnamed starting office, the six 1991 states and their neutral district
captions, the world-start calibration and one global flag another mod script already sets.
Official: ACES Chronicle rows used only as date anchors for distant pressures, each cited by its
exact key. Everything else, including every choice, office, idea, building, decision and event in
Echea, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='EHE', name='Echea', root='world', package='ehe',
                  themes=('navy', 'ballot', 'tools'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots; '
           'tech_mountaineers among the starting technologies; grand doctrines superior_firepower, fleet_in_being and '
           'operational_integrity. The starting leader is the unnamed National Administration office (EHE_ac_government_office, '
           'centrism), whose description says its 1991 holder has not been established. The tree never names a holder.',
           'mod/2985041246/history/countries/EHE - Echea.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 384, 530 (capital), 531, 543, 546 and 572, captioned Echea District A, Capital District, '
           'District C, District D, District E and District F by the neutral regional labels (the capital takes the second '
           'letter, so there is no District B; canonical regional mapping unestablished). Terrain counts from '
           'map/definition.csv: 25 of 49 provinces jungle (A 8, capital 5, D 10, E 2); mountains in the capital, C, E and F; '
           'desert in F (4 of 8) and A (1); coastal provinces in A, the capital, D and E, while C and F are inland. District D '
           'has 12 provinces and no infrastructure, buildings or resources; C (3 provinces) and F (8) have neither '
           'infrastructure nor buildings. The capital (large_city) holds naval base 3, two dockyards, a fuel silo, an air base, '
           'two civilian and two military factories; District A (town) two of each, infrastructure 2 and the supply node of '
           'the logistics centre; District E two civilian and one military factory. Rubber, steel, aluminium and oil lie in A, '
           'the capital and E. Land neighbours AEM (via A and F), SOA (via C and F), CSO (via C and E) and ECH (via E), '
           'computed from map/provinces.bmp. Victory points Echea Capital Centre (5457) and Echea Logistics Centre 2052. No '
           'place outside these captions is named.',
           'mod/2985041246/history/states/384-State_384.txt, 530-State_530.txt, 531-State_531.txt, 543-State_543.txt, '
           '546-State_546.txt, 572-State_572.txt; mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'tools/regional_labels/labels.json; mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role small coastal service; 6 civilian, 5 military and 2 naval '
           'factories; 4 infantry formations (6 battalions); 24 fighters on one air base; 2 coastal escorts; 60 convoys; '
           'two intersecting rail paths; research priority Physical Sustainment (transport, equipment replacement, affordable '
           'service). Fictional fiscal calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses will pass close to the Earth with a chance of impact. Used '
           'only as the premise of the impact committee focus; no Echea role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Used only as the date gate of the arms brokers focus; Echea takes no part '
           'and no Echea role is claimed.', '1995 / 03.25'),
    Source('Official',
           'Date anchor: the President of the FCU announces that Ulysses will impact the Earth and announces plans to counter '
           'it. Used as the date gate of the impact announcement focus; where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Date anchor: the IAU monthly damage estimate is revised to include possible fragments on the eastern part of the '
           'Anean continent. Used as the date gate of the estimate desk focus; Echea is not placed on any continent.',
           '1998 / 07.29'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Used as the date gate of the Roche limit focus '
           'and its event; no damage in Echea is claimed.', '1999 / 07.08'),
    Source('Official',
           'Date anchor: Osea, Emmeria and other nations join in economic sanctions against Estovakia. Used as the date gate '
           'of the contract review focus; whether Echea is among the other nations is not recorded and not claimed.',
           '2002 / 03.20'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air '
           'batteries. Used as the opening of the late-deliveries branch, framed only as pressure on imported spare parts.',
           '2003 / SUMMER'),
    Source('Mod provenance',
           'Campaign hook read only, never set: ac_ucw_outcome_isaf_victory (common/scripted_effects/ac_ucw.txt). The reaction '
           'is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Echea focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in the six 1991 '
           'states.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the lapsed calendar
    IdeaDef('lapsed_calendar', 'The Lapsed Calendar', 'The statutory polling day passed and no new one was named.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('ballot', 'document')),
    IdeaDef('open_press', 'An Open Press Law', 'Any printer may publish on the calendar quarrel; the bloc papers sell best.',
            {'stability_factor': -0.01, 'research_speed_factor': 0.02, 'political_power_factor': 0.04}, ('communications', 'ballot')),
    IdeaDef('licensed_press', 'Printing Licences', 'Printers who inflame the calendar quarrel lose their presses for a season.',
            {'political_power_gain': 0.08, 'stability_factor': 0.02, 'war_support_factor': -0.02}, ('document', 'security')),
    IdeaDef('ballot_guarantees', 'Guarantees for the Ballot', 'A polling day fixed in law that no emergency may move.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'scales')),
    IdeaDef('standing_secretariat', 'A Standing Secretariat', 'Department heads govern by rule while no polling day is set.',
            {'political_power_gain': 0.12, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('bloc_in_ministries', 'The Bloc in the Ministries', 'The nationalist bloc holds the interior and police portfolios.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.05, 'stability_factor': -0.03}, ('security', 'assembly')),
    IdeaDef('polling_season', 'The Polling Season', 'Clerks, locked boxes and boats in every district until the count is done.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('ballot', 'logistics')),
    IdeaDef('restored_calendar', 'The Restored Calendar', 'A cabinet answerable to the chamber, with the next vote already fixed.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'ballot')),
    IdeaDef('secretariat_code', 'The Secretariat Code', 'Published standing orders bind every ministry and every official.',
            {'political_power_gain': 0.15, 'production_speed_buildings_factor': 0.05}, ('document', 'command')),
    IdeaDef('bloc_rallies', 'Bloc Rallies', 'The bloc fills the squares while its terms are written down.',
            {'war_support_factor': 0.05, 'stability_factor': -0.02}, ('security', 'ballot')),
    IdeaDef('bloc_order', 'Order of the Bloc Executive', 'Government by decree with bloc officials beside every district governor.',
            {'stability_factor': 0.06, 'war_support_factor': 0.08, 'consumer_goods_factor': 0.04}, ('security', 'command')),
    IdeaDef('planning_horizon', 'A Planning Horizon', 'Ministries budget five years ahead for the first time since the calendar lapsed.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.03}, ('document', 'economy')),
    # the coastal service
    IdeaDef('coastal_service', 'The Coastal Service', 'Two escorts, one naval base and four coasts to watch.',
            {'naval_coordination': 0.03, 'navy_org_factor': 0.03}, ('navy', 'security')),
    IdeaDef('patrol_flotilla', 'The Patrol Boat Flotilla', 'Small boats in numbers along every coast.',
            {'naval_coordination': 0.06, 'naval_speed_factor': 0.04}, ('navy', 'fishing')),
    IdeaDef('ready_escorts', 'Both Escorts Ready', 'Crews, spares and fuel to sail at a day of notice.',
            {'navy_org_factor': 0.06, 'repair_speed_factor': 0.05}, ('navy', 'tools')),
    IdeaDef('interior_coast_guard', 'Coast Guard of the Interior', 'Lifeboats, permits and harbour police under a civilian minister.',
            {'stability_factor': 0.03, 'naval_coordination': 0.03}, ('security', 'civil')),
    IdeaDef('naval_section', 'Naval Section of the Staff', 'The escorts are planned alongside the battalions.',
            {'planning_speed': 0.06, 'navy_org_factor': 0.04}, ('command', 'navy')),
    IdeaDef('fisheries_watch', 'Fisheries Protection', 'Fishing permits enforced off the jungle coast.',
            {'consumer_goods_factor': -0.02, 'naval_coordination': 0.03}, ('fishing', 'security')),
    IdeaDef('fleet_in_harbour', 'A Fleet in Harbour', 'Two ready escorts that any hostile planner must guard against.',
            {'navy_org_factor': 0.08, 'naval_coordination': 0.04, 'repair_speed_factor': 0.05}, ('navy', 'medal')),
    IdeaDef('licensed_pilots', 'Licensed Harbour Pilots', 'Every merchant ship carries a pilot who knows the channels.',
            {'industrial_capacity_dockyard': 0.04, 'naval_coordination': 0.03}, ('navy', 'document')),
    # the arms lines
    IdeaDef('half_shift_lines', 'Lines on Half Shifts', 'Five arms lines paid for and half idle.',
            {'production_speed_arms_factory_factor': 0.03, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('rifle_exports', 'Rifles for Export', 'Arms lines on full shifts for licensed foreign buyers.',
            {'production_speed_arms_factory_factor': 0.10, 'stability_factor': -0.02}, ('industry', 'diplomacy')),
    IdeaDef('certified_exports', 'Certified Exports', 'Every sale carries a certificate naming its final user.',
            {'production_speed_arms_factory_factor': 0.10, 'political_power_factor': 0.03}, ('document', 'diplomacy')),
    IdeaDef('replacement_stock', 'The Replacement Stock', 'A full set of replacements for every battalion, held in depots.',
            {'army_org_factor': 0.04, 'supply_consumption_factor': -0.04, 'production_speed_arms_factory_factor': 0.05}, ('security', 'industry')),
    IdeaDef('repair_halls', 'The Repair Halls', 'Two arms lines retooled to overhaul and mend.',
            {'repair_speed_factor': 0.10, 'production_speed_industrial_complex_factor': 0.05}, ('tools', 'industry')),
    IdeaDef('one_pattern', 'One Pattern', 'One calibre and one truck model across the army.',
            {'supply_consumption_factor': -0.05, 'production_factory_efficiency_gain_factor': 0.03}, ('document', 'logistics')),
    IdeaDef('broker_season', 'The Brokers Calling', 'Arms brokers telephone from abroad while the Belkan War lasts.',
            {'production_speed_arms_factory_factor': 0.05, 'stability_factor': -0.02}, ('communications', 'industry')),
    IdeaDef('contract_review', 'Contracts Under Review', 'Every supply contract checked for routes to a sanctioned buyer.',
            {'political_power_factor': 0.04, 'stability_factor': 0.02}, ('scales', 'document')),
    # the rubber groves
    IdeaDef('grove_count', 'The Grove Count', 'A tally of every tapped tree and of who claims it.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.03}, ('document', 'economy')),
    IdeaDef('latex_floor_price', 'A Floor Under Latex', 'A buying office guarantees a minimum price in bad years.',
            {'stability_factor': 0.03, 'consumer_goods_factor': 0.02}, ('scales', 'economy')),
    IdeaDef('tapper_cooperatives', 'Tappers Cooperatives', 'Village cooperatives pool latex and run their own sheds.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.05}, ('civil', 'economy')),
    IdeaDef('estate_charters', 'Estate Charters', 'Long leases and export credit for the large estates.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('economy', 'industry')),
    IdeaDef('state_rubber_works', 'The State Rubber Works', 'Latex turned into sheet, belting and tyres at home.',
            {'production_speed_industrial_complex_factor': 0.08, 'political_power_gain': 0.03}, ('industry', 'tools')),
    IdeaDef('replanted_groves', 'Replanted Groves', 'Young stock in place of the oldest rows.',
            {'production_factory_max_efficiency_factor': 0.03, 'stability_factor': 0.02}, ('rebuild', 'economy')),
    # District D
    IdeaDef('district_d_office', 'The District D Office', 'A permanent government office on the jungle coast.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.08}, ('civil', 'logistics')),
    IdeaDef('fever_clinics', 'Fever Clinics', 'A nurse, a medicine store and a radio for each group of coastal villages.',
            {'stability_factor': 0.04, 'attrition': -0.03}, ('medical', 'civil')),
    IdeaDef('steamer_service', 'The Coastal Steamers', 'Subsidised steamers call at every landing on the coast.',
            {'production_speed_buildings_factor': 0.03, 'naval_coordination': 0.02}, ('navy', 'logistics')),
    IdeaDef('land_titles', 'Titles for Cleared Land', 'Families who have farmed a plot for five years may hold it by title.',
            {'stability_factor': 0.03, 'production_speed_industrial_complex_factor': 0.04}, ('scales', 'civil')),
    IdeaDef('wet_season_plan', 'The Wet-Season Plan', 'Food, medicine and boats in place before the rains.',
            {'attrition': -0.05, 'supply_consumption_factor': -0.03}, ('shelter', 'logistics')),
    # the army inland
    IdeaDef('six_battalions', 'Six Battalions', 'A small army mustered and counted.',
            {'army_core_defence_factor': 0.04}, ('training', 'command')),
    IdeaDef('mountain_rifles', 'Mountain Rifles', 'Light companies that live in the passes.',
            {'army_defence_factor': 0.05, 'attrition': -0.05, 'army_core_defence_factor': 0.05}, ('training', 'security')),
    IdeaDef('motor_columns', 'Motor Columns', 'Motorised battalions held in central reserve.',
            {'army_speed_factor': 0.05, 'army_org_factor': 0.04}, ('logistics', 'command')),
    IdeaDef('valley_mule_trains', 'Mule Trains', 'Pack animals and village handlers for every hill company.',
            {'supply_consumption_factor': -0.04, 'stability_factor': 0.01}, ('logistics', 'civil')),
    IdeaDef('hill_staff_school', 'The Hill Staff School', 'Officers trained to plan across mountain, desert and coast.',
            {'planning_speed': 0.08, 'experience_gain_army_factor': 0.06}, ('command', 'document')),
    IdeaDef('frontier_volunteers', 'Bloc Volunteer Companies', 'Unpaid bloc volunteers on frontier duty in District F.',
            {'war_support_factor': 0.04, 'army_core_defence_factor': 0.04, 'stability_factor': -0.02}, ('security', 'ballot')),
    # the air wing
    IdeaDef('one_runway_wing', 'One Runway', 'Twenty-four fighters on a single field.',
            {'experience_gain_air_factor': 0.04}, ('air', 'runway')),
    IdeaDef('capital_sky_wing', 'The Capital Sky Wing', 'Every fighter trained to deny the sky over the core.',
            {'air_superiority_efficiency': 0.06, 'air_defence_factor': 0.04}, ('air', 'security')),
    IdeaDef('rescue_wing', 'The Rescue Wing', 'Light transports and helicopters for rescue and supply.',
            {'air_mission_efficiency': 0.05, 'stability_factor': 0.02}, ('air', 'medical')),
    IdeaDef('mechanics_school', 'The Mechanics School', 'Trained mechanics keep more aircraft flying each day.',
            {'repair_speed_factor': 0.06, 'experience_gain_air_factor': 0.04}, ('tools', 'air')),
    # Ulysses
    IdeaDef('impact_committee', 'The Impact Committee', 'Planners for a threat nobody can locate.',
            {'stability_factor': 0.01, 'air_detection': 0.04}, ('meteor', 'telescope')),
    IdeaDef('mountain_refuges', 'Mountain Refuges', 'Stocked refuges in the District C valleys.',
            {'stability_factor': 0.05, 'static_anti_air_damage_factor': 0.05}, ('shelter', 'meteor')),
    IdeaDef('sea_lift_plan', 'The Sea-Lift Plan', 'Every hull listed and assigned to a landing.',
            {'naval_coordination': 0.05, 'stability_factor': 0.03}, ('navy', 'refugees')),
    IdeaDef('field_hospitals', 'Field Hospitals', 'Blood banks and tented hospitals ready within a day.',
            {'stability_factor': 0.04, 'war_support_factor': 0.02}, ('medical', 'shelter')),
    IdeaDef('drilled_crews', 'Drilled Sea-Lift Crews', 'Merchant and fishing crews who have rehearsed the lift.',
            {'naval_coordination': 0.04, 'navy_org_factor': 0.03}, ('navy', 'training')),
    IdeaDef('spares_hoard', 'Spares Laid Up', 'Two years of engines, tyres and filters in dry sheds.',
            {'repair_speed_factor': 0.05, 'consumer_goods_factor': 0.02}, ('logistics', 'shelter')),
    IdeaDef('impact_timetable', 'The Impact Timetable', 'Quarterly targets for every ministry until the asteroid passes.',
            {'political_power_gain': 0.08, 'stability_factor': 0.02}, ('document', 'meteor')),
    # late deliveries
    IdeaDef('stripped_for_parts', 'Stripped for Parts', 'Part of the fleet grounded so that the rest can run.',
            {'repair_speed_factor': 0.08, 'army_org_factor': -0.02}, ('tools', 'logistics')),
    IdeaDef('forward_spares', 'Spares Bought Forward', 'Two years of parts bought at wartime prices.',
            {'repair_speed_factor': 0.04, 'stability_factor': 0.02, 'consumer_goods_factor': 0.03}, ('economy', 'document')),
    IdeaDef('parts_register', 'The Parts Register', 'One list of every spare part held by every service.',
            {'supply_consumption_factor': -0.03, 'planning_speed': 0.04}, ('document', 'tools')),
    IdeaDef('home_spares', 'Spares Made at Home', 'Common spare parts tooled up in the existing works.',
            {'repair_speed_factor': 0.08, 'production_factory_efficiency_gain_factor': 0.03}, ('tools', 'industry')),
    IdeaDef('order_books', 'Order Books Reopen', 'Foreign suppliers deliver on time again.',
            {'production_factory_efficiency_gain_factor': 0.04, 'stability_factor': 0.02}, ('economy', 'peace')),
    # decisions
    IdeaDef('extra_tapping', 'An Extra Tapping Round', 'Growers paid for one more round before the rains.',
            {'production_factory_efficiency_gain_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'civil')),
    IdeaDef('storm_watch', 'The Storm-Season Watch', 'Lifeboat crews and patrols on alert through the storm months.',
            {'naval_coordination': 0.05, 'stability_factor': 0.01}, ('radar', 'navy')),
    IdeaDef('extra_staff_term', 'An Extra Staff Term', 'Another class of captains through the hill school.',
            {'planning_speed': 0.05, 'experience_gain_army_factor': 0.05}, ('training', 'document')),
    IdeaDef('sheds_inspected', 'Sheds Inspected', 'Spares counted and rotated in every depot.',
            {'repair_speed_factor': 0.05, 'political_power_gain': -0.03}, ('document', 'tools')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('calendar_cabinet', 'Cabinet of the Restored Calendar',
           'A cabinet named by the chamber elected at the postponed vote, governing collectively with the next polling day '
           'fixed in law. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('secretariat', 'The Permanent Secretariat',
           'A collective of department heads holding the seals under published standing orders, with no polling day set. '
           'Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('bloc_executive', 'Executive of the National Bloc',
           'An executive drawn from the leadership of the nationalist bloc, ruling by decree with bloc officials beside every '
           'district governor. Provisional gameplay office with no named holder.',
           'fascism', 'fascism_ideology'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('calendar_due', 'An Election Nobody Scheduled', (
        "The date printed in the statute book came and went without a proclamation. No ballots were printed, no polling "
        "halls were opened, and the National Administration issued only a short notice saying that the calendar would be "
        "reviewed when conditions allowed. Echea has been governed in that conditional tense ever since, by an office that "
        "carries the democratic party's name while almost nobody in the country carries its vote.",
        "The arithmetic is the problem. Nearly half the country stands with the non-aligned establishment of officials, port "
        "owners, estate families and works managers, who value calm above any creed. The other half, by a whisker more, "
        "follows the nationalist bloc, which promises a firmer state and says openly that it would win any honest count. "
        "Each side suspects the Administration of planning to cheat the other.",
        "This morning a group of district notables delivered a sealed letter to the capital centre asking for one thing "
        "only: a date. They do not say which date, or who should win. Ministers must decide whether to answer in public, "
        "where every camp will read the reply and organise around it, or to keep the matter inside the ministries a while "
        "longer.",
    ), (
        Option('Publish the letter and invite petitions.', (Stability(-0.02), PP(-10), Event('calendar_petitions', 20))),
        Option('Acknowledge it privately and wait.', (PP(35), Stability(-0.02))),
    ), picture=1),
    EventDef('calendar_petitions', 'Petitions from Six Districts', (
        "Three weeks after the letter was printed, the post office in the capital centre began to fill with petitions. "
        "They arrived by truck from District A, by fishing boat and canoe from the coast of District D, down the mule tracks "
        "from District C and with hired drivers from the desert hills of District F. Clerks have counted more signatures "
        "than there are names on the old voter rolls.",
        "The petitions do not agree with each other. Bloc committees demand a vote within the year and new rolls drawn up "
        "by their own volunteers. Estate families and port owners ask for a date far enough away to settle the economy "
        "first. Village councils from the jungle coast mostly ask for roads, clinics and a ballot box they can actually "
        "reach.",
        "Whatever the government does with this paper, it has created an expectation. Filing the petitions unanswered would "
        "tell every signer that the letter was a trap; answering them all would take months the ministries do not have. The "
        "Administration's lawyers suggest a middle course, which pleases nobody and may still be the wisest one on offer.",
    ), (
        Option('Answer every district in public.', (Stability(0.03), PP(-25))),
        Option('Publish a summary and a timetable for replies.', (Stability(0.01), PP(10))),
        Option('File them and thank the signers.', (PP(30), Stability(-0.03), WarSupport(0.02))),
    ), picture=1),
    EventDef('coast_two_escorts', 'Two Ships and a Long Coast', (
        "The coastal service's annual report reaches the cabinet with a map folded inside it. The map shows four districts "
        "with sea frontage, a naval base at the capital centre, two coastal escorts and the tracks they actually sailed last "
        "year. The tracks cluster around the capital. Along the jungle shore of District D and the bays of District E there "
        "are long stretches nobody patrolled at all.",
        "Fishermen from those coasts complain of foreign trawlers working inside the limits and of boats lost in storms with "
        "nobody to answer their radios. Merchant masters complain about silted channels and charts drawn generations ago. "
        "Officers complain that half their budget goes on keeping two hulls seaworthy and the other half on fuel for patrols "
        "that cannot cover the coast anyway. Nobody disputes the complaints; everyone disputes the cure.",
        "The report ends with a question rather than a request. Should the service try to be a small navy, or a large coast "
        "guard, or something in between that the country can afford? The cabinet cannot answer that today, but it can decide "
        "what the service does this year while the argument continues.",
    ), (
        Option('Send the escorts on the long patrol.', (XP('navy', 10), PP(-10))),
        Option('Keep them near the capital and save fuel.', (PP(20), Stability(-0.01))),
    ), picture=0),
    EventDef('works_inventory', 'Half Shifts at the Arms Works', (
        "The works office's count is blunt. Five arms lines in District A, the capital and District E can turn out rifles, "
        "support equipment, motor transport and a few fighters a year. The army they supply has six battalions in four "
        "formations, and in most months it orders less than two of those lines could make. The rest of the capacity sits on "
        "half shifts, paid for and idle.",
        "Workers on half shifts are not idle by choice. Their unions want full time or new work. Managers want export "
        "licences, or at least a guaranteed order book. The army wants a stock of replacements it can draw on in a hard "
        "month, and the treasury wants to know why it funds machine halls that make nothing for days at a time.",
        "Three answers are already circulating in the ministries: sell abroad, build ahead, or turn the lines to repair "
        "work. Each has a constituency, and each closes doors the others would open. For now the cabinet must decide only how "
        "to pay for the coming quarter while the real decision is prepared. The unions have asked to be heard before anything is signed.",
    ), (
        Option('Pay full shifts and build stock meanwhile.', (PP(-20), XP('army', 10))),
        Option('Keep the half shifts and save the money.', (PP(25), Stability(-0.02))),
    ), picture=2),
    EventDef('groves_owners', 'Who Owns the Trees', (
        "The agricultural clerks came back from the jungle districts with sunburn, fever and a count nobody expected. Rubber "
        "grows in thousands of small family groves scattered across District A, the capital district and District E, and in "
        "a smaller number of large estates that produce most of the latex actually sold abroad. Ownership turns out to be "
        "murkier than the count.",
        "Many family groves sit on land the estates also claim. Many estates rely on tappers who own a few rows of their own "
        "and sell to whoever pays on the day. Middlemen buy latex forward from desperate families in bad years and sell it at "
        "a profit in good ones. Everyone agrees the system is unfair; everyone disagrees about whom it is unfair to. Some families have tapped the same "
        "trees for three generations without ever seeing a deed.",
        "The clerks' report recommends no model. It does recommend that the government choose one soon, because every season "
        "of uncertainty sees more trees go untapped and more families leave for the capital. Ministers can begin by "
        "protecting the tappers, by reassuring the estates, or by keeping both waiting while the argument is prepared.",
    ), (
        Option('Promise the tappers a hearing first.', (Stability(0.02), PP(-10))),
        Option('Reassure the estate owners.', (PP(20), Stability(-0.01))),
    ), picture=1),
    EventDef('jungle_district', 'A District Without a Road', (
        "The walking team's report runs to three volumes and a box of photographs. District D, it says, is a coast of river "
        "mouths and jungle valleys where most villages are reached by boat or by footpath. There is no graded road, no "
        "factory, no hospital and no permanent government office anywhere in the district. Most villagers have never met an "
        "official who did not want taxes.",
        "The team found reasons for hope as well. Villages trade fish, fruit and handicrafts along the coast; river mouths "
        "make natural harbours; young people want schooling and work and are leaving for the capital to find them. Families "
        "have been clearing jungle plots for decades without papers, and they are anxious to know whether the land is theirs. Several villages have built their own "
        "schoolrooms and are still waiting for a teacher.",
        "The report ends with a plain recommendation: that the government open an office in the district before it does "
        "anything else, so that whatever comes next is planned with the people who will live with it. Ministers already "
        "disagree about roads and boats, and about what any of it will cost.",
    ), (
        Option('Open the district office this year.', (Stability(0.02), PP(-15))),
        Option('Send the report to committee.', (PP(20), Stability(-0.01))),
    ), picture=0),
    EventDef('highland_passes', 'Six Battalions, Two Frontiers', (
        "The muster took a month and told the general staff what it already feared. Of the six battalions, most are "
        "stationed near the capital and the coast, one sits beside the logistics centre in District A, and detachments are "
        "spread thin along the inland frontiers. None could reach the upper valleys of District C in less than three days, "
        "or the far side of the District F hills in less than four.",
        "The inland districts are threatened by nobody today. Their frontiers with Central Sotoa, Sotoa and Aemurraq are "
        "quiet, crossed by traders and herders and checked by customs posts. But the staff plans for decades rather than "
        "for today, and its officers are divided between those who think the hills must be held by troops who live in them "
        "and those who think the real danger lies on the coast.",
        "Before either school wins, the staff needs roads, signals and a doctrine everyone can train to. The cabinet is asked "
        "to approve a programme of surveys, exercises and engineering work. Which doctrine follows is left, for now, to the "
        "officers who will argue about it.",
    ), (
        Option('Approve the full programme.', (XP('army', 15), PP(-15))),
        Option('Approve the surveys only.', (PP(15), XP('army', 5))),
    ), picture=2),
    EventDef('air_one_field', 'All the Wing on One Runway', (
        "The wing commander's briefing to the cabinet uses a single photograph of the capital air base, taken from a light "
        "aircraft at dawn. Every one of the country's twenty-four fighters is visible in it, parked in two neat rows beside "
        "the only runway. The commander points out that a single attack, or a single fuel fire, could end the air arm in an "
        "afternoon.",
        "The wing has other problems. Its pilots fly fewer hours than they need because spare parts are scarce. Its radar is "
        "a set in the control tower that sees little beyond the coast. Its ground crews are good but few, and when an "
        "aircraft breaks, it waits. Meanwhile ministries ask why none of the country's aircraft can fly a doctor to District D. Two "
        "reserve airframes have been robbed of parts so often that they no longer count as aircraft.",
        "The commander asks for money for runways and dispersal first, and a decision about the wing's purpose second. Some "
        "ministers would rather settle the purpose first and buy the concrete afterwards. Either way the wing will need to "
        "change, and the cabinet must choose how much to spend this year to start.",
    ), (
        Option('Fund the runways now.', (XP('air', 10), PP(-20))),
        Option('Ask for a plan before any money.', (PP(15), XP('air', 5))),
    ), picture=0),
    EventDef('sky_certain', 'The Asteroid Will Strike', (
        "When the President of the FCU announces to the world in April 1996 that Ulysses will strike the Earth, the impact "
        "committee's contingency papers stop being contingencies. Nobody in the capital knows where fragments will fall. The "
        "announcement does not say, and the astronomers say only that their estimates will be refined month by month.",
        "Markets react faster than governments. Grain, fuel and shipping insurance rise in every port Echea trades with. "
        "Families with savings buy tinned food and lamp oil; families without savings watch the prices. The nationalist bloc "
        "demands emergency powers for whoever governs, and the port owners demand that nobody panic. Both demands are printed "
        "side by side in the morning papers.",
        "The committee lays two plans before the cabinet. One would move the coastal population inland to refuges in the "
        "mountains of District C; the other would keep people at home and move them by sea if warning came. Both are "
        "expensive and neither can be ready for years. The cabinet is asked first how to speak to the country tonight. Whatever it says will be repeated in "
        "every district by morning.",
    ), (
        Option('Speak plainly: plans, costs and uncertainty.', (Stability(0.03), PP(-15))),
        Option('Promise protection and leave the details to the committee.', (Stability(-0.01), PP(25), WarSupport(0.02))),
    ), picture=1),
    EventDef('roche_night', 'Ulysses Inside the Roche Limit', (
        "In July 1999 the asteroid Ulysses passes through the Roche limit of the Earth. In the capital the impact committee "
        "sits through the night in a basement room with radios, telephones and a wall of charts nobody can update fast "
        "enough. The coastal service has its escorts at sea, the air wing has crews in the cockpits and the field hospitals "
        "are packed on trucks.",
        "Reports arrive out of order and contradict each other. Foreign stations read statements from astronomers, then "
        "retract them. Radio amateurs on the coast of District D report lights over the sea that might be fragments, "
        "aircraft or nothing at all. The committee chair insists that no order be given without two confirmations, and so "
        "for hours almost no orders are given.",
        "By dawn the committee has learned how much its plans depended on information it never had. The question now is "
        "what to keep: the readiness, which costs money every day, or the calm that comes from standing it down. Either choice "
        "will be second-guessed for years. Ministers who sat through the night are already arguing about which of them "
        "was right.",
    ), (
        Option('Keep the readiness for another year.', (WarSupport(0.03), PP(-20))),
        Option('Stand down and count the cost.', (Stability(0.02), PP(15))),
    ), picture=2),
    EventDef('lanes_war', 'Deliveries Postponed Indefinitely', (
        "The letters arrive in the same week from suppliers in three countries. Engine parts for the escorts, radio sets for "
        "the battalions, bearings for the fighter line and replacement spindles for the machine tools in the capital works "
        "will ship late, the letters say, or not at all. Erusea's invasion of San Salvacion has started a war, and every "
        "factory that can build for it has a new customer.",
        "Echea's armed services run on a sustainment doctrine: few machines, kept working for a long time. That doctrine "
        "assumes that parts can be ordered. Within a month the coastal service reports one escort waiting on a pump, the air "
        "wing grounds four fighters for want of hydraulic seals, and truck parks in two districts are cannibalising vehicles "
        "to keep the rest moving.",
        "The treasury and the general staff bring two answers to the cabinet: strip part of the fleet to keep the rest "
        "running, or pay whatever the market demands for parts bought forward. Before either is chosen, ministers must decide "
        "what to tell the services about the months immediately ahead. The services want an answer before the month "
        "is out.",
    ), (
        Option('Order the services to conserve every part.', (Stability(-0.01), XP('army', 5), PP(10))),
        Option('Promise emergency money for the worst shortages.', (PP(-25), Stability(0.02))),
    ), picture=2),
)

# --- branches ------------------------------------------------------------------------------------
CALENDAR = Branch('calendar', 'The Lapsed Election Calendar', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('cal_overdue', 'The Election That Lapsed',
          "Echea's statute book sets a national vote every forty-eight months, and the National Administration has simply let "
          "the date go by without naming another. It governs in the name of a democratic party that almost nobody in the "
          "country now votes for. Opening the question formally costs the Administration its quiet and its excuses, but every "
          "ministry is already waiting for an answer.",
          ('ballot', 'document'), reward=(Idea('lapsed_calendar'), Event('calendar_due'))),
    Focus('cal_rolls', 'Recount the Voter Rolls',
          "Nobody trusts the voter rolls, which were last revised before the calendar lapsed and still list the dead, the "
          "emigrated and the double-registered. Clerks from the capital go district by district with the old ledgers and a new "
          "set of rules. The recount is slow and costly, and whichever camp loses the eventual argument will call it rigged "
          "anyway.",
          ('document', 'assembly'), after=('cal_overdue',), reward=(Flag('rolls_recounted'), PP(-20))),
    Focus('cal_open_press', 'Let the Newspapers Print It',
          "One school in the Administration says the calendar question must be argued where everyone can read it. An open "
          "press law ends the licensing of printers and lets the nationalist papers, the business sheets and the few democratic "
          "pamphlets say what they like. The bloc's papers will outsell everyone else's, and some ministers fear exactly that "
          "outcome.",
          ('communications', 'ballot'), after=('cal_overdue',), exclusive=('cal_licensed_press',), reward=(Idea('open_press'),)),
    Focus('cal_licensed_press', 'Keep the Printing Licences',
          "The other school keeps the old licensing office, which grants and withdraws the right to print. Papers that inflame "
          "the calendar quarrel lose their presses for a season. The streets stay calmer and the Administration's voice stays "
          "louder. It also convinces the nationalist bloc that the government fears an honest count, and the bloc says so at "
          "every rally.",
          ('document', 'security'), after=('cal_overdue',), exclusive=('cal_open_press',), reward=(Idea('licensed_press'),)),
    Focus('cal_set_date', 'Name the Day and Keep It',
          "The plainest answer is to announce a polling day, fix it in law and promise that no emergency will move it. The "
          "establishment fears the nationalist bloc will win a fair count outright, and the democratic camp barely exists to "
          "compete. Ministers who choose the ballot accept that they may be voted out by the people they spent years keeping "
          "out of office.",
          ('ballot', 'scales'), after=('cal_overdue',), cost=10, exclusive=('cal_no_date', 'cal_bloc_terms'),
          reward=(SwapIdea('lapsed_calendar', 'ballot_guarantees'), Flag('path_ballot'))),
    Focus('cal_no_date', 'Govern Without a Polling Day',
          "The second answer comes from inside the ministries. Senior officials propose that the Administration stop calling "
          "itself temporary and become a permanent secretariat of department heads, governing by published rules rather than "
          "by votes. Port owners, estate families and district notables like the predictability. Nobody voted for it, and the "
          "bloc calls it rule by rubber stamp.",
          ('command', 'document'), after=('cal_overdue',), cost=10, exclusive=('cal_set_date', 'cal_bloc_terms'),
          reward=(SwapIdea('lapsed_calendar', 'standing_secretariat'), Flag('path_secretariat'))),
    Focus('cal_bloc_terms', 'Open the Ministries to the Bloc',
          "The third answer accepts the arithmetic. Half the country stands with the nationalist bloc, so the Administration "
          "invites its leaders into the ministries before they take them by other means. The bloc promises discipline, full "
          "shifts at the works and a firm line on the frontiers. Its price is the interior and police portfolios, and it "
          "rarely gives back what it is lent.",
          ('security', 'assembly'), after=('cal_overdue',), cost=10, exclusive=('cal_set_date', 'cal_no_date'),
          reward=(SwapIdea('lapsed_calendar', 'bloc_in_ministries'), Flag('path_bloc'))),
    Focus('cal_polling_clerks', 'Polling Clerks for Six Districts',
          "A fair vote needs a clerk, a locked box and a lamp in every polling hall from the jungle coast to the desert hills. "
          "The Administration trains clerks in the capital and sends them out with the recounted rolls. District D has no "
          "road to half its villages, so many clerks travel by boat. The cost is high and the schedule leaves no slack.",
          ('ballot', 'logistics'), after=('cal_set_date',), requires=(HasFlag('rolls_recounted'),),
          reward=(TimedIdea('polling_season', 365),)),
    Focus('cal_restored_cabinet', 'Seat the Restored Cabinet',
          "When the count is done, the new chamber names a cabinet that answers to it, and the National Administration "
          "dissolves into ordinary ministries. Whatever the result, the calendar runs again, with the next vote already fixed "
          "in law. The cabinet inherits a split country and a thin treasury. It also holds something the old office never had: "
          "a mandate it can show.",
          ('assembly', 'ballot'), after=('cal_polling_clerks',),
          reward=(Regime('calendar_cabinet'), SwapIdea('ballot_guarantees', 'restored_calendar'))),
    Focus('cal_standing_orders', 'Standing Orders for the Ministries',
          "A permanent secretariat needs rules that bind it, or it is only an office that refuses to leave. The department "
          "heads publish standing orders: how budgets are set, how officials are appointed, how complaints reach the top. "
          "Publishing them invites a scrutiny the old Administration avoided. Without them, the secretariat would be the same "
          "lapsed calendar under a grander name.",
          ('document', 'scales'), after=('cal_no_date',), reward=(PP(40), Stability(0.01))),
    Focus('cal_secretariat', 'Seal the Permanent Secretariat',
          "The department heads take the seals collectively and the old office is retired with formal thanks. No polling day "
          "appears anywhere in the new arrangements, though nothing forbids one later. Officials who served the Administration "
          "now serve the secretariat at the same desks with the same files. Predictability is the promise; the bloc in the "
          "street is the risk nobody has solved.",
          ('command', 'scales'), after=('cal_standing_orders',),
          reward=(Regime('secretariat'), SwapIdea('standing_secretariat', 'secretariat_code'))),
    Focus('cal_bloc_pact', 'Put the Bloc Terms in Writing',
          "Before the bloc takes any more portfolios, officials insist that its promises be written down: which ministries it "
          "holds, what happens to serving officials, how long until any election. The bloc's leaders sign a short paper and "
          "treat it as a formality while their supporters rally outside. The paper buys the civil service a few protections. "
          "It also hands the bloc a legal path to everything else.",
          ('document', 'security'), after=('cal_bloc_terms',), reward=(TimedIdea('bloc_rallies', 365), WarSupport(0.02))),
    Focus('cal_bloc_executive', 'Seat the Bloc Executive',
          "The National Administration hands its seals to an executive drawn from the bloc's leadership, which governs by "
          "decree with bloc officials beside every district governor. The ministries keep working; the opposition papers do "
          "not. Supporters fill the capital centre for the ceremony. Officials who signed the written terms learn what a "
          "signature is worth when the other side holds the police.",
          ('security', 'command'), after=('cal_bloc_pact',),
          reward=(Regime('bloc_executive'), SwapIdea('bloc_in_ministries', 'bloc_order'))),
    Focus('cal_answer', 'A Settled Answer at Last',
          "However it was reached, Echea now has a government that can plan beyond the next quarter. Ministries publish "
          "five-year budgets for the first time since the calendar lapsed, and foreign lenders return to the capital with "
          "questions instead of excuses. The quarrel is not over, because the losing camps still exist. It has moved from the "
          "street into the budget.",
          ('document', 'economy'), after_any=('cal_restored_cabinet', 'cal_secretariat', 'cal_bloc_executive'),
          reward=(Idea('planning_horizon'), Stability(0.03))),
))

COAST = Branch('coast', 'The Coastal Service', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('cst_two_escorts', 'Two Escorts, Four Coasts',
          "Four of the six districts touch the sea, from the jungle shore of District A past the capital centre to the long "
          "coast of District D and the bays of District E. The navy that guards them is two coastal escorts, one naval base and "
          "sixty merchant convoys. A service built for this coast must first decide what it can actually do with so little.",
          ('navy', 'security'), reward=(Idea('coastal_service'), Event('coast_two_escorts'))),
    Focus('cst_rescue_posts', 'Lifeboat Posts on the Jungle Shore',
          "The first job of a small coastal service is rescue rather than war. Lifeboat posts with radios and a radar mast go "
          "up along District D, where fishing boats are lost every storm season and no road can bring help. The posts cost "
          "little and win friends in villages that rarely see the capital. They also teach crews the coast in every weather.",
          ('radar', 'navy'), after=('cst_two_escorts',), reward=(Build('radar_station', 1, 543), XP('navy', 10))),
    Focus('cst_chart_shoals', 'Chart the Shoals and Channels',
          "Most charts of the coast were drawn long ago and are wrong about the river mouths, sandbars and channels that shift "
          "from year to year. A survey launch with a small team of hydrographers works the coast district by district. The "
          "work is slow, unglamorous and essential: an escort that runs aground is as lost as one that is sunk.",
          ('document', 'navy'), after=('cst_two_escorts',),
          reward=(Research('naval_equipment', 0.5, 1), Flag('shoals_charted'))),
    Focus('cst_refit_basin', 'A Refit Basin at the Capital',
          "The two dockyards at the capital centre build and repair merchant hulls and have no berth to spare for the escorts. "
          "A third yard dedicated to refits, with a covered shed and a small dry berth, lets the navy keep both ships ready "
          "instead of queuing one behind a merchant job. It takes the last free plot on the capital waterfront.",
          ('tools', 'navy'), after=('cst_two_escorts',), reward=(Build('dockyard', 1, 0),)),
    Focus('cst_patrol_boats', 'A Flotilla of Small Patrol Boats',
          "One school argues that two escorts can never cover four coasts, and that a dozen small patrol boats, cheap to build "
          "and crew, would see far more of the sea. They cannot fight a real warship and spend storms in harbour. They can stop "
          "smugglers, check fishing permits and answer a distress call on the same afternoon it is made.",
          ('navy', 'fishing'), after=('cst_two_escorts',), cost=10, exclusive=('cst_keep_escorts',),
          reward=(SwapIdea('coastal_service', 'patrol_flotilla'),)),
    Focus('cst_keep_escorts', 'Keep Both Escorts Ready',
          "The other school says the escorts are the only real warships the country has, and that splitting the budget across "
          "small boats would leave nothing able to fight. The money goes into crews, spares and fuel so that both escorts can "
          "sail at a day's notice. The coast between their patrols stays empty, and the fishing villages notice.",
          ('navy', 'tools'), after=('cst_two_escorts',), cost=10, exclusive=('cst_patrol_boats',),
          reward=(SwapIdea('coastal_service', 'ready_escorts'),)),
    Focus('cst_interior_guard', 'Coast Guard Under the Interior',
          "Lifeboats, fishing permits and harbour police are civil work, says the interior ministry, and belong to a coast "
          "guard under civilian control. Officers keep their ranks but answer to a minister rather than a general. The service "
          "gains friends in the ports and loses some of its claim on the defence budget whenever money runs short.",
          ('security', 'civil'), after=('cst_rescue_posts',), exclusive=('cst_naval_staff',),
          reward=(Idea('interior_coast_guard'),)),
    Focus('cst_naval_staff', 'A Naval Section on the Staff',
          "The army staff wants the opposite: one chain of command for every armed service, with a naval section planning the "
          "escorts alongside the battalions. Plans for the coast and the frontiers would at last be written together. Rescue "
          "work would come second to readiness, and the ports would see more uniforms and fewer lifeboats.",
          ('command', 'navy'), after=('cst_rescue_posts',), exclusive=('cst_interior_guard',), reward=(Idea('naval_section'),)),
    Focus('cst_fisheries', 'Fisheries Protection Patrols',
          "With a flotilla at sea, the service can enforce the fishing permits that foreign trawlers have long ignored off the "
          "jungle coast. Boardings, fines and the occasional seized net bring revenue and a good deal of local gratitude. They "
          "also bring diplomatic notes from the owners' governments, which the foreign ministry answers with charts and permit "
          "lists.",
          ('fishing', 'security'), after=('cst_patrol_boats',), reward=(Idea('fisheries_watch'), Stability(0.01))),
    Focus('cst_fleet_waits', 'A Fleet That Waits in Harbour',
          "The staff's old doctrine holds that a fleet which might sail can matter as much as one that does. Two ready escorts "
          "in a defended harbour force any hostile planner to guard against them. The doctrine suits a country with two "
          "warships and a long coast. Critics call it a respectable name for staying at anchor, and they are not entirely "
          "wrong.",
          ('navy', 'medal'), after=('cst_keep_escorts',),
          reward=(SwapIdea('ready_escorts', 'fleet_in_harbour'), XP('navy', 15))),
    Focus('cst_pilot_licences', 'Licensed Pilots for Every Harbour',
          "With the new charts printed, every merchant ship entering a national harbour must carry a licensed pilot who knows "
          "the channels. Pilots pay for their licences, ships pay for the pilots, and groundings fall. Shipowners grumble at "
          "the fee. The pilots become the coastal service's eyes in every port, which pleases the service more than the "
          "owners.",
          ('navy', 'document'), after_any=('cst_interior_guard', 'cst_naval_staff'), requires=(HasFlag('shoals_charted'),),
          reward=(Idea('licensed_pilots'),)),
    Focus('cst_quay_e', 'Deepen the Quay in District E',
          "District E has two industrial plants and a bay that only shallow coasters can enter. Dredging the approach and "
          "lengthening the quay lets larger ships load its steel and aluminium directly rather than sending everything by road "
          "to the capital centre. Dredgers are hired abroad at a steep day rate. The road to the capital grows a little "
          "quieter.",
          ('logistics', 'navy'), after=('cst_refit_basin',), reward=(Build('infrastructure', 1, 546),)),
))

WORKS = Branch('works', 'Five Lines for Six Battalions', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('wrk_count_lines', 'Count the Lines and Battalions',
          "Echea runs five arms lines for an army of six battalions, alongside trucks, rail stock and a small fighter line. "
          "Most weeks the arms plants in District A, the capital and District E work half shifts. Before anyone decides what "
          "the lines are for, the works office counts what each can make, what it costs and who actually buys it.",
          ('industry', 'document'), reward=(Idea('half_shift_lines'), Event('works_inventory'))),
    Focus('wrk_sidings', 'New Sidings at the Logistics Centre',
          "Everything the works produce passes through the logistics centre in District A, where one siding and a single "
          "loading ramp turn every delivery into a queue. Two more sidings, a second ramp and a covered yard let trains load "
          "while trucks unload. The rail board pays half. The other half comes from the arms budget, which notices.",
          ('rail', 'logistics'), after=('wrk_count_lines',), reward=(Build('infrastructure', 1, 384),)),
    Focus('wrk_machine_tools', 'Replace the Worn Machine Tools',
          "The lathes and presses in the capital works are older than most of the people running them. Replacing the worst "
          "with modern machine tools raises output per shift and cuts scrap. Imported tools cost foreign currency the treasury "
          "guards closely, and the old machines have friends among foremen who know their quirks. The new ones need training "
          "first.",
          ('tools', 'industry'), after=('wrk_count_lines',), reward=(Research('industry', 0.5, 1), PP(-15))),
    Focus('wrk_export_rifles', 'Sell Rifles to Foreign Buyers',
          "The export school says idle lines are wasted capital and that rifles, mortars and trucks sell abroad to any "
          "government with a licence and the cash. Full shifts would return, wages would rise and the arms budget would partly "
          "pay for itself. Every buyer would tie the country's name to someone else's quarrel, and some buyers would not stay "
          "friendly.",
          ('industry', 'diplomacy'), after=('wrk_count_lines',), cost=10,
          exclusive=('wrk_replacement_stock', 'wrk_repair_lines'), reward=(SwapIdea('half_shift_lines', 'rifle_exports'),)),
    Focus('wrk_replacement_stock', 'A Replacement Stock for Each Unit',
          "The sustainment school wants the lines to build ahead: a full set of replacement rifles, support equipment and "
          "trucks for every battalion, stored in depots and rotated as it ages. The army could lose equipment in a hard month "
          "and still fight the next. The stock ties up steel and money in sheds, and auditors hate inventories that never move.",
          ('security', 'industry'), after=('wrk_count_lines',), cost=10,
          exclusive=('wrk_export_rifles', 'wrk_repair_lines'), reward=(SwapIdea('half_shift_lines', 'replacement_stock'),)),
    Focus('wrk_repair_lines', 'Turn Idle Lines to Repair Work',
          "The repair school says a small country should mend rather than make. Two arms lines are retooled to overhaul trucks, "
          "rifles, radios and aircraft parts, keeping old equipment serviceable for years. Output of new equipment falls. "
          "Spending falls faster, and the skills built in the repair halls are the same ones civilian industry is short of.",
          ('tools', 'logistics'), after=('wrk_count_lines',), cost=10,
          exclusive=('wrk_export_rifles', 'wrk_replacement_stock'), reward=(SwapIdea('half_shift_lines', 'repair_halls'),)),
    Focus('wrk_end_user', 'End-User Certificates',
          "Exports need rules or they become scandals. Every sale now requires a certificate naming the final user, signed by "
          "the buying government and checked by the foreign ministry. Some brokers walk away. The certificates do not make "
          "every sale wise, but they let the works office refuse a buyer without inventing an excuse, and they leave a record.",
          ('document', 'diplomacy'), after=('wrk_export_rifles',), reward=(SwapIdea('rifle_exports', 'certified_exports'),)),
    Focus('wrk_mountain_depot', 'A Mountain Depot in District C',
          "Replacement stock kept beside the factories would be lost with them. The army wants a depot in the District C "
          "mountains, inland and hard to reach, with a small assembly hall where stored rifles and trucks are checked and "
          "refitted. Building it means hauling machinery up the new pass road. Once it is there, the stock is far from any "
          "coast.",
          ('security', 'tools'), after=('wrk_replacement_stock',), requires=(Completed('hgh_pass_road'),),
          reward=(Build('arms_factory', 1, 531),)),
    Focus('wrk_truck_overhaul', 'Overhaul the Army Trucks',
          "The army's trucks are its mobility, and many are too worn for the hill roads. The new repair halls rebuild them in "
          "batches: engines, gearboxes, axles and tyres. A rebuilt truck costs a third of a new one and lasts most of a decade. "
          "The battalions lose a share of their transport while each batch is in the halls.",
          ('logistics', 'tools'), after=('wrk_repair_lines',), reward=(Research('logistics_tech', 0.5, 1), XP('army', 10))),
    Focus('wrk_one_pattern', 'One Calibre and One Truck Pattern',
          "Whatever the lines are for, the army still uses several rifle patterns and truck models bought at different times. "
          "Standardising on one calibre and one truck pattern makes every spare part fit every unit. The transition takes "
          "years, retires good equipment early and annoys every officer attached to the old kit. Supply columns become simpler "
          "to load and plan.",
          ('document', 'logistics'), after_any=('wrk_export_rifles', 'wrk_replacement_stock', 'wrk_repair_lines'),
          reward=(Idea('one_pattern'),)),
    Focus('wrk_broker_calls', 'Brokers Call During the Belkan War',
          "When the Belkan War begins in March 1995, arms brokers telephone the works office from half a dozen capitals asking "
          "what the national lines can deliver and how fast. The country is nowhere near the fighting. The question is whether "
          "the works answer the telephone at all, and how many shifts the answer will cost or keep.",
          ('communications', 'industry'), after=('wrk_count_lines',), requires=(After('1995.3.25'),),
          reward=(TimedIdea('broker_season', 365),)),
    Focus('wrk_sanctions_review', 'Review Contracts Under the Sanctions',
          "In March 2002 Osea, Emmeria and other nations join in economic sanctions against Estovakia. Nothing records whether "
          "Echea is counted among the other nations. The works office reviews every supply and export contract anyway for "
          "components that could reach Estovakia through a broker, because the country's own suppliers will soon be asking "
          "the same questions.",
          ('scales', 'document'), after_any=('wrk_export_rifles', 'wrk_replacement_stock', 'wrk_repair_lines'),
          requires=(After('2002.3.20'),), reward=(TimedIdea('contract_review', 365), PP(-15))),
))

GROVES = Branch('groves', 'The Rubber Groves', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('grv_tree_count', 'Count Every Tapped Tree',
          "Rubber grows across the jungle districts in groves of every size, from a family's few rows behind a village to "
          "estates covering whole valleys. Nobody knows how many trees are tapped, who owns them or where the latex goes. A "
          "count by agricultural clerks, grove by grove, is the first step to any rubber policy and the first quarrel about "
          "one.",
          ('document', 'economy'), reward=(Idea('grove_count'), Event('groves_owners'))),
    Focus('grv_latex_floor', 'A Floor Price for Latex',
          "Latex prices swing with markets far away, and every collapse ruins small tappers who sold their crop forward. A "
          "national buying office promises to purchase latex at a published floor price in bad years and sell from its store in "
          "good ones. The office needs a reserve to start and discipline to keep it. Tappers will remember whether it pays.",
          ('scales', 'economy'), after=('grv_tree_count',), reward=(TimedIdea('latex_floor_price', 730), PP(-20))),
    Focus('grv_coops', 'Tappers and Their Cooperatives',
          "The first model puts the groves in the hands of the people who tap them. Village cooperatives pool latex, run their "
          "own smoking sheds and sell in bulk. Yields stay modest and quality varies from shed to shed. The money stays in the "
          "villages, the districts grow steadier, and the old estate owners lose the cheap labour they have always counted on.",
          ('civil', 'economy'), after=('grv_tree_count',), cost=10, exclusive=('grv_estates', 'grv_state_works'),
          reward=(SwapIdea('grove_count', 'tapper_cooperatives'),)),
    Focus('grv_estates', 'Charter the Estate Companies',
          "The second model backs the large estates, which have capital, improved seedlings and agents abroad. Chartered estate "
          "companies get long leases, export credit and freedom to buy up small groves. Output and quality rise quickly. Many "
          "small tappers become wage workers on land they used to work for themselves, and the districts will not forget who "
          "signed the charters.",
          ('economy', 'industry'), after=('grv_tree_count',), cost=10, exclusive=('grv_coops', 'grv_state_works'),
          reward=(SwapIdea('grove_count', 'estate_charters'),)),
    Focus('grv_state_works', 'A State Rubber Works',
          "The third model skips the argument over ownership and goes downstream. A state rubber works buys latex from anyone "
          "at the floor price and turns it into sheet, belting and tyres at home instead of exporting raw crop. The plant needs "
          "engineers and protection from imports. If it works, the country sells finished goods; if not, the treasury owns a "
          "very expensive shed.",
          ('industry', 'tools'), after=('grv_tree_count',), cost=10, exclusive=('grv_coops', 'grv_estates'),
          reward=(SwapIdea('grove_count', 'state_rubber_works'),)),
    Focus('grv_smoke_sheds', 'Smoking Sheds for the Villages',
          "Cooperatives need somewhere to turn latex into smoked sheet before it spoils. A building programme puts communal "
          "smoking and drying sheds in the jungle villages of District D, with a small processing hall at the main landing. The "
          "sheds use local timber and labour. Together they give District D its first industrial building of any kind.",
          ('rebuild', 'civil'), after=('grv_coops',), reward=(Build('industrial_complex', 1, 543),)),
    Focus('grv_estate_wharf', 'Estate Wharves in District A',
          "The estate companies want their latex on ships rather than in trucks. New wharves and a paved estate road along the "
          "District A coast let them load directly for export. The companies pay part of the cost and expect the rest from the "
          "treasury. Fishing villages along the shore lose some beach to concrete, and the wharf owners decide who else may "
          "use it.",
          ('logistics', 'economy'), after=('grv_estates',), reward=(Build('infrastructure', 1, 384),)),
    Focus('grv_tyre_plant', 'A Tyre and Belting Plant',
          "The state works builds its main plant in District E, beside the existing factories and the steel they already "
          "handle. It makes truck tyres, conveyor belts and hoses for domestic buyers first. The army is the first customer and "
          "the most demanding one. Imported tyres were cheaper; the plant's whole case rests on the years when imports cannot be "
          "had.",
          ('industry', 'logistics'), after=('grv_state_works',), reward=(Build('industrial_complex', 1, 546),)),
    Focus('grv_replant', 'Replant the Ageing Groves',
          "Many trees were planted generations ago and yield less every season. A replanting programme pays growers to cut the "
          "oldest rows and plant new stock, accepting years without latex from those plots. Growers need credit to survive the "
          "gap. The groves that emerge will outproduce the old ones for decades, provided the programme survives several "
          "changes of minister.",
          ('rebuild', 'economy'), after_any=('grv_coops', 'grv_estates', 'grv_state_works'),
          reward=(Idea('replanted_groves'), PP(-20))),
    Focus('grv_blight_lab', 'A Laboratory for Leaf Blight',
          "A single fungal blight could wipe out groves planted from the same stock. A small agricultural laboratory in the "
          "capital district studies leaf diseases, tests resistant stock and trains inspectors to spot infections early. It is "
          "a modest building with a modest staff. Its warning may one day be the difference between a bad season and a ruined "
          "district.",
          ('science', 'medical'), after=('grv_replant',), reward=(Research('synth_resources', 0.5, 1), Stability(0.01))),
))

JUNGLE = Branch('jungle', 'A Road for District D', 1992, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('jun_walk', 'Walk the Length of District D',
          "District D covers more ground than any other district and has had the least investment: a long jungle coast and "
          "river valleys with no road, no factory and no telephone line worth the name. A government team walks and paddles "
          "its length for a season, mapping villages, landings and fever zones. Their report is the first account of the "
          "district anyone in the capital has read.",
          ('logistics', 'civil'), reward=(Idea('district_d_office'), Event('jungle_district'))),
    Focus('jun_fever_clinics', 'Clinics Against the Fevers',
          "The walking team found fever in almost every village, and the nearest hospital is in the capital centre, two days "
          "away by boat. A chain of small clinics, each with a nurse, a medicine store and a radio, brings basic care to the "
          "coast. Staffing them is harder than building them, because few trained nurses want to live so far from a road.",
          ('medical', 'civil'), after=('jun_walk',), reward=(Idea('fever_clinics'),)),
    Focus('jun_coast_road', 'Cut the Coast Road',
          "The road party wants a graded road along the coast from the capital to the far end of District D, with bridges over "
          "every river. Trucks, buses and the army could then reach every village in a day. The road will take years, swallow "
          "budgets and need repairs after every wet season. Once built, it joins District D to the rest of the country for good.",
          ('bridge', 'logistics'), after=('jun_walk',), cost=10, exclusive=('jun_steamers',),
          reward=(Build('infrastructure', 2, 543),)),
    Focus('jun_steamers', 'Coastal Steamers Instead',
          "The harbour party says the sea already connects District D, and that a subsidised steamer service calling at every "
          "landing would serve the coast at a fraction of a road's price. A small yard at the main landing would build and "
          "repair the boats. Steamers are slower than trucks and stop in storms. They also leave the jungle standing.",
          ('navy', 'logistics'), after=('jun_walk',), cost=10, exclusive=('jun_coast_road',),
          reward=(Build('dockyard', 1, 543), Idea('steamer_service'))),
    Focus('jun_road_camps', 'Road Camps and River Bridges',
          "Crews building the coast road live in camps that move with the work, each with a clinic, a store and an engineer's "
          "office. Bridges go in before the road reaches them so that the camps can be supplied from both banks. The army's "
          "engineers lend surveyors and learn jungle building on the way. Every finished bridge shortens the next season's "
          "haul.",
          ('bridge', 'tools'), after=('jun_coast_road',),
          reward=(Build('infrastructure', 1, 543), Research('engineers_tech', 0.5, 1))),
    Focus('jun_landings', 'Timber Landings at the River Mouths',
          "Steamers need somewhere to call. Timber landings with a warehouse, a small crane and a harbour light are built at "
          "each of the main river mouths, where village trade already gathers. Landings flood and rot faster than concrete. "
          "They are cheap enough to rebuild, and each one becomes a market as soon as the first steamer ties up.",
          ('navy', 'civil'), after=('jun_steamers',), reward=(Build('infrastructure', 1, 543), Stability(0.01))),
    Focus('jun_workshop_town', 'A Workshop Town at the Landing',
          "Whichever way the coast is joined, the main landing of District D grows into its first real town. A workshop hall "
          "for engines, boats and trucks gives the district a trade that does not depend on the harvest. Skilled mechanics "
          "must be lured from the capital with housing and higher pay. The workshop's apprentices become the district's first "
          "trained workforce.",
          ('tools', 'civil'), after_any=('jun_coast_road', 'jun_steamers'), reward=(Build('industrial_complex', 1, 543),)),
    Focus('jun_land_titles', 'Titles for Cleared Land',
          "Families clearing jungle plots along the coast have no papers, while estate companies and speculators in the capital "
          "claim the same land. A land office issues titles to families who have farmed a plot for five years, with surveys "
          "paid by the state. Some claims collide and the courts fill with disputes. A title lets a family borrow against land "
          "it can prove is its own.",
          ('scales', 'civil'), after=('jun_walk',), reward=(Idea('land_titles'),)),
    Focus('jun_wet_season', 'Plans for the Wet Season',
          "Every year the rains cut District D into islands for months, and every year the government reacts as though "
          "surprised. A standing wet-season plan places food, medicine and boats before the rains, assigns army trucks to the "
          "worst stretches and publishes which landings stay open. It spends money in dry months on problems that arrive in wet "
          "ones.",
          ('shelter', 'logistics'), after=('jun_fever_clinics',), reward=(Idea('wet_season_plan'),)),
    Focus('jun_district_deputy', 'A Deputy for District D',
          "If the calendar returns, District D must be counted in it. Its villages are so scattered that a single polling "
          "station would leave most of them unheard, so the electoral office allots the district its own deputy and carries "
          "ballot boxes along the coast by boat. The deputy will arrive in the capital with a long list of demands and little "
          "patience.",
          ('ballot', 'civil'), after=('jun_land_titles',), requires=(HasFlag('path_ballot'),),
          reward=(Stability(0.04), PP(-10))),
))

HIGHLANDS = Branch('highlands', 'The Passes and the Desert Hills', 1991, 'FOCUS_FILTER_MANPOWER', (
    Focus('hgh_muster', 'Muster the Six Battalions',
          "The army is four formations and six battalions spread thin between the coast and two inland districts. District C "
          "is mountain and hill on the Sotoa and Central Sotoa frontiers; District F is desert and broken hills facing "
          "Aemurraq and Sotoa. Neither has a graded road. Before any reform, the staff musters every battalion and finds out "
          "what each can actually reach.",
          ('training', 'command'), reward=(Idea('six_battalions'), Event('highland_passes'))),
    Focus('hgh_pass_road', 'A Road Over the District C Passes',
          "District C is three high valleys joined by mule tracks, cut off from the rest of the country whenever rock falls "
          "block the passes. A graded road with retaining walls and culverts links it to District E and the coast. The "
          "engineers estimate two seasons and the treasury estimates three. Once it opens, the valleys can sell what they grow "
          "and the army can reach them.",
          ('bridge', 'command'), after=('hgh_muster',), reward=(Build('infrastructure', 2, 531),)),
    Focus('hgh_desert_track', 'Grade the Track into District F',
          "District F's desert and hills are crossed by tracks that vanish after every sandstorm. Grading a proper track from "
          "District A through the district, with water and a fuel stop every day's drive, gives the frontier garrisons a supply "
          "line and the hill villages a way to market. The work is hot, dull and permanent, which suits the army's engineers.",
          ('logistics', 'security'), after=('hgh_muster',), reward=(Build('infrastructure', 2, 572),)),
    Focus('hgh_firepower', 'Outshoot, Never Outnumber',
          "An army of six battalions will never outnumber anyone, so the staff's doctrine is to outshoot them. Mortars and field "
          "guns are concentrated in a support group that can move to whichever battalion is engaged. Gunners need years of "
          "training and ammunition the works must supply. Infantry officers complain that firepower is being bought with their "
          "manpower.",
          ('missile', 'training'), after=('hgh_muster',), reward=(Research('artillery', 0.5, 1), XP('army', 10))),
    Focus('hgh_mountain_rifles', 'Mountain Rifle Companies',
          "The hill school wants the battalions retrained as mountain rifles: light companies that live in the passes, move on "
          "foot and by mule, and know every ridge on the frontier. Infantry already learn mountaineering in basic training. "
          "Mountain troops are slow to concentrate and poorly placed to defend the coast. On their own ground they are very "
          "hard to dislodge.",
          ('training', 'security'), after=('hgh_muster',), cost=10, exclusive=('hgh_motor_columns',),
          reward=(SwapIdea('six_battalions', 'mountain_rifles'),)),
    Focus('hgh_motor_columns', 'Motor Columns for the Coast',
          "The coast school says the passes defend themselves and the danger lies along the shore, where any landing would "
          "come. It wants the battalions motorised on trucks the works already build, held in central reserve and moved by "
          "road to wherever a threat appears. Columns need roads, fuel and maintenance. Without them, motor infantry is "
          "infantry that waits.",
          ('logistics', 'command'), after=('hgh_muster',), cost=10, exclusive=('hgh_mountain_rifles',),
          reward=(SwapIdea('six_battalions', 'motor_columns'),)),
    Focus('hgh_mule_trains', 'Mule Trains for the Upper Valleys',
          "Mountain companies live or die by their supply, and trucks cannot climb where they patrol. Each company receives a "
          "mule train, handlers hired from the valley villages and fodder stores at the pass huts. Villagers earn steady pay and "
          "the army learns their paths. The trains are slow and need daily care, but they never wait for fuel deliveries.",
          ('logistics', 'civil'), after=('hgh_mountain_rifles',), reward=(Idea('valley_mule_trains'),)),
    Focus('hgh_truck_park', 'A Central Truck Park',
          "Motor columns need a home where trucks are serviced, fuelled and loaded around the clock. A central truck park at the "
          "edge of the capital district, with workshops, a fuel depot and a road to the coast, becomes the army's pivot. Every "
          "column leaves from there. It is also an obvious target, which the staff accepts as the price of speed.",
          ('logistics', 'rail'), after=('hgh_motor_columns',), reward=(Build('infrastructure', 1, 0), XP('army', 10))),
    Focus('hgh_signal_huts', 'Signal Huts on the High Ridges',
          "Radio contact with the valley garrisons fails behind the ridges. A chain of signal huts on the high points, each "
          "with a relay set and a small radar for weather and aircraft, keeps District C talking to the capital. Crews rotate "
          "monthly because the huts are cold, cramped and lonely. The chain also watches the sky above the frontier.",
          ('radar', 'communications'), after=('hgh_pass_road',), reward=(Build('radar_station', 1, 531),)),
    Focus('hgh_depot_f', 'A Workshop Depot in District F',
          "Garrisons in District F wait weeks for spare parts from the coast. A depot at the end of the graded track, with "
          "workshops that can rebuild engines and weapons on site, shortens that wait to days. The depot needs water, power and "
          "staff willing to live in the desert hills. It becomes the district's largest employer the week it opens.",
          ('tools', 'security'), after=('hgh_desert_track',), reward=(Build('industrial_complex', 1, 572),)),
    Focus('hgh_staff_school', 'A Staff School in the Hills',
          "Whichever doctrine wins, the battalions need officers trained to plan operations across mountains, desert and coast "
          "together. A small staff school in the hill country teaches map work, logistics and combined exercises with the air "
          "wing and the coastal service. It takes the best captains away from their units for a year. They return able to run a "
          "campaign.",
          ('command', 'document'), after_any=('hgh_mountain_rifles', 'hgh_motor_columns'), reward=(Idea('hill_staff_school'),)),
    Focus('hgh_bloc_companies', 'Volunteer Companies from the Bloc',
          "With the bloc in the ministries, its youth wings offer volunteer companies for frontier duty in District F. The "
          "volunteers are eager, unpaid and loyal to the bloc first. The staff gains manpower it could not otherwise afford and "
          "loses some control over who guards the frontier. Regular officers are attached to every company, and quietly told to "
          "keep notes.",
          ('security', 'ballot'), after=('hgh_desert_track',), requires=(HasFlag('path_bloc'),),
          reward=(TimedIdea('frontier_volunteers', 730),)),
))

AIR = Branch('air', 'One Field, Twenty-Four Fighters', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('avn_one_field', 'Twenty-Four Fighters, One Runway',
          "The air wing is twenty-four fighters and a handful of reserve airframes on a single air base at the capital. One "
          "damaged runway would ground all of them. Before arguing about missions, the wing's officers press for the basics: a "
          "second runway, somewhere to disperse, and radar that sees farther than the control tower's binoculars.",
          ('air', 'runway'), reward=(Idea('one_runway_wing'), Event('air_one_field'))),
    Focus('avn_second_runway', 'A Crosswind Runway at the Capital',
          "A second runway laid across the first lets the wing fly in crosswinds that ground it today and keeps one strip open "
          "if the other is cratered. Concrete and drainage are expensive in jungle soil and the work closes the field for weeks. "
          "When it reopens, the wing can launch twice as fast and recover in weather that used to divert it.",
          ('runway', 'tools'), after=('avn_one_field',), reward=(Build('air_base', 1, 0),)),
    Focus('avn_dispersal', 'Dispersal Strips in District A',
          "Grass and gravel strips in District A, near the logistics centre, give the fighters somewhere to go if the capital "
          "field is hit. Each strip has a fuel bowser, a tent hangar and a crew that drills twice a year. The strips cost little "
          "to build and a great deal to keep ready. A wing that can disperse is a much harder target.",
          ('runway', 'logistics'), after=('avn_one_field',), reward=(Build('air_base', 1, 384),)),
    Focus('avn_capital_radar', 'Radar on the Heights',
          "Mountains overlook the capital district, and a radar station on the heights would see aircraft long before they "
          "reach the coast. The site is hard to reach and needs its own road and generator. The radar feeds the wing's control "
          "room and the coastal service's plot. The wing finally sees its own sky without depending on reports from ships.",
          ('radar', 'air'), after=('avn_second_runway',), reward=(Build('radar_station', 1, 0),)),
    Focus('avn_capital_sky', 'Fighters for the Capital Sky',
          "The fighter school wants every airframe trained for one mission: denying the sky over the capital and the works. "
          "Pilots fly intercepts and air combat drills and little else. The country gains a credible air defence for its core. "
          "Everything outside that circle, from the jungle coast to the desert hills, sees fighters only on parade days.",
          ('air', 'security'), after=('avn_one_field',), cost=10, exclusive=('avn_rescue_wing',),
          reward=(SwapIdea('one_runway_wing', 'capital_sky_wing'),)),
    Focus('avn_rescue_wing', 'A Transport and Rescue Wing',
          "The service school says a country with no roads to half its villages needs aircraft that carry people more than "
          "aircraft that shoot. Part of the budget buys light transports and helicopters for rescue, medical flights and "
          "supply drops to the interior. Fewer fighters stay on alert. The wing becomes the most popular part of the armed "
          "forces almost overnight.",
          ('air', 'medical'), after=('avn_one_field',), cost=10, exclusive=('avn_capital_sky',),
          reward=(SwapIdea('one_runway_wing', 'rescue_wing'),)),
    Focus('avn_clinic_strips', 'Airstrips for the Clinics',
          "The fever clinics along District D need a way to move the seriously ill. Short airstrips beside the largest clinics "
          "let light transports land on a cleared field, carry patients to the capital and return with medicine. Each strip "
          "needs constant clearing against the jungle. Every evacuation flight is talked about in the district, and remembered "
          "there.",
          ('runway', 'medical'), after=('avn_rescue_wing',), requires=(Completed('jun_fever_clinics'),),
          reward=(Build('air_base', 1, 543),)),
    Focus('avn_gunnery_range', 'A Gunnery Range in District F',
          "Pilots who never fire live rounds cannot be trusted to hit anything. A gunnery and bombing range in the empty desert "
          "of District F, with targets, a scoring hut and a small strip for refuelling, lets the wing train properly without "
          "overflying towns. Ammunition costs rise sharply. So does the share of pilots who pass their gunnery tests.",
          ('air', 'missile'), after=('avn_capital_sky',), reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
    Focus('avn_mechanics', 'Mechanics Before Pilots',
          "A fighter on the ground for want of a part is no fighter at all. The wing opens a school for aircraft mechanics, "
          "trains them on the airframes it actually flies and pays them nearly as much as junior pilots. More aircraft fly each "
          "day. The pilots' mess complains about money spent on spanners; the readiness reports end the argument.",
          ('tools', 'air'), after_any=('avn_capital_sky', 'avn_rescue_wing'), reward=(Idea('mechanics_school'),)),
))

SKY = Branch('sky', 'Under a Named Asteroid', 1995, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_committee', 'A Committee for the Asteroid',
          "In December 1994 the International Astronomical Union announces that the asteroid Ulysses will pass close to the "
          "Earth, with a chance of impact. Nobody can say where anything might fall. The government forms an impact committee "
          "of ministry officials, doctors, engineers and the coastal service, with a mandate to plan against a threat it cannot "
          "locate.",
          ('meteor', 'telescope'), reward=(Idea('impact_committee'),)),
    Focus('sky_certain', 'The FCU Announces the Impact',
          "In April 1996 the President of the FCU tells the world that Ulysses will strike the Earth and sets out plans to "
          "counter it. The committee's contingency papers become a programme overnight. Prices for grain, fuel and insurance "
          "jump in every market the country trades with, and the capital wants to know what the government will actually do.",
          ('meteor', 'communications'), after=('sky_committee',), requires=(After('1996.4.20'),),
          reward=(Event('sky_certain'), Stability(-0.02))),
    Focus('sky_refuges', 'Refuges in the District C Mountains',
          "One plan moves people inland and upward. Refuges dug into the slopes of the District C valleys, stocked with food "
          "and water and reached by the pass road, would shelter coastal families if fragments struck the sea nearby. The "
          "refuges are expensive and far away. Families on the coast ask how they will get there in time.",
          ('shelter', 'meteor'), after=('sky_certain',), cost=10, exclusive=('sky_sea_lift',),
          reward=(SwapIdea('impact_committee', 'mountain_refuges'),)),
    Focus('sky_sea_lift', 'A Sea-Lift for the Coast',
          "The other plan keeps people where they live and moves them by sea if a fragment threatens. Merchant ships, the "
          "coastal service and every fishing boat with an engine are listed, crewed and assigned to a landing. A sea-lift is "
          "cheaper than refuges and uses ships the country already owns. It depends on warning time nobody can promise.",
          ('navy', 'refugees'), after=('sky_certain',), cost=10, exclusive=('sky_refuges',),
          reward=(SwapIdea('impact_committee', 'sea_lift_plan'),)),
    Focus('sky_blood_banks', 'Blood Banks and Field Hospitals',
          "Whatever falls, the injured will need treatment where they are. The health ministry builds blood banks in the "
          "capital and District E, buys tented field hospitals and trains volunteer teams to raise them within a day. Donors "
          "queue outside the first banks. The equipment ages in storage, and every year without an impact makes it harder to "
          "defend in the budget.",
          ('medical', 'shelter'), after=('sky_committee',), reward=(Idea('field_hospitals'),)),
    Focus('sky_refuge_road', 'Widen the Road to the Refuges',
          "Refuges are useless if the road to them jams. The pass road into District C is widened for two lanes of traffic, "
          "with lay-bys, fuel stops and signs marked for evacuation. Practice convoys run each dry season and reveal every "
          "bottleneck. Hill villages gain a better road than they ever expected, built for a reason they hope never to see.",
          ('bridge', 'shelter'), after=('sky_refuges',), requires=(Completed('hgh_pass_road'),),
          reward=(Build('infrastructure', 1, 531),)),
    Focus('sky_lift_drill', 'Rehearse the Sea-Lift',
          "Once a year the coastal service, merchant masters and fishing crews rehearse the sea-lift, loading volunteers at "
          "every landing and sailing them to the capital. The first drill is chaos and the second is merely slow. Each costs "
          "fuel, a week of lost catches and a great deal of overtime. Each also shortens the time a real evacuation would take.",
          ('navy', 'training'), after=('sky_sea_lift',), reward=(TimedIdea('drilled_crews', 365), XP('navy', 10))),
    Focus('sky_estimate_desk', 'Read the Monthly Damage Estimate',
          "From July 1998 the International Astronomical Union's monthly damage estimate includes the possibility of fragments "
          "falling on the eastern part of the Anean continent. The committee sets up a desk to read each estimate on the day it "
          "is published and translate it into orders for the ministries. The estimates keep changing, and so do the orders.",
          ('telescope', 'document'), after=('sky_certain',), requires=(After('1998.7.29'),),
          reward=(Flag('estimate_desk'), Research('electronics', 0.5, 1))),
    Focus('sky_roche', 'A Radio Watch for the Roche Limit',
          "In July 1999 Ulysses passes through the Roche limit. The committee's estimate desk has prepared for this night for "
          "a year: the coastal service is on alert, the field teams are packed and every district office has a radio watch. No "
          "fragment's path is known in advance. By morning the country will know how well its plans hold up.",
          ('meteor', 'shelter'), after=('sky_estimate_desk',), requires=(After('1999.7.8'), HasFlag('estimate_desk')),
          reward=(Event('roche_night'),)),
    Focus('sky_spares_hoard', 'Spares Laid Up Before the Fall',
          "If shipping stops after an impact, the country's ships, trucks and fighters will run on whatever spare parts are "
          "already at home. The committee buys a two-year stock of engines, tyres, filters and radio parts and stores it in dry "
          "sheds away from the coast. The purchase drains foreign currency. It turns the sustainment doctrine into something "
          "physical.",
          ('logistics', 'shelter'), after=('sky_certain',), reward=(Idea('spares_hoard'), PP(-20))),
    Focus('sky_secretariat_tables', 'Timetables from the Secretariat',
          "With the permanent secretariat in charge, impact planning becomes an administrative exercise of the kind department "
          "heads do best. Every ministry receives a timetable listing what it must stock, train and inspect by each quarter "
          "until the asteroid passes. Inspectors check the timetables. The public sees little of this, which is how the "
          "secretariat prefers it.",
          ('document', 'meteor'), after=('sky_committee',), requires=(HasFlag('path_secretariat'),),
          reward=(TimedIdea('impact_timetable', 730),)),
))

LANES = Branch('lanes', 'Late Deliveries in a Distant War', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('lns_san_salvacion', 'Delivery Dates Slip',
          "Erusea's invasion of San Salvacion in the summer of 2003, and its use of the captured Stonehenge railguns against "
          "aircraft, start a war far from these coasts. Within weeks foreign suppliers write that engine parts, radio sets and "
          "machine tools ordered for the works and the armed services will ship late, if at all. Their factories have found "
          "new customers.",
          ('missile', 'document'), requires=(After('2003.6.1'),), reward=(Event('lanes_war'),)),
    Focus('lns_strip_for_parts', 'Strip Two to Keep Ten Running',
          "One answer is to live on what the country already has. A share of the trucks, two of the fighters and the oldest "
          "patrol craft are laid up and stripped for parts, so that everything else keeps moving. The services shrink on paper "
          "for the length of the war. Mechanics learn every component by hand, and nothing waits on a foreign delivery date.",
          ('tools', 'logistics'), after=('lns_san_salvacion',), cost=10, exclusive=('lns_buy_forward',),
          reward=(Idea('stripped_for_parts'),)),
    Focus('lns_buy_forward', 'Buy Spares Forward at Any Price',
          "The other answer is to pay. The treasury signs forward contracts for spare parts and fuel at wartime prices, "
          "guaranteeing two years of supply at a painful cost. Nothing is laid up and every unit keeps its strength. The bill "
          "falls on the budgets for roads, clinics and the works, and the contracts run on even if the war ends early.",
          ('economy', 'document'), after=('lns_san_salvacion',), cost=10, exclusive=('lns_strip_for_parts',),
          reward=(Idea('forward_spares'),)),
    Focus('lns_rail_freight', 'Heavy Freight Moves to Rail',
          "With fuel and truck parts dear, the works and the logistics centre move heavy freight from road to rail wherever "
          "the two rail paths through the country allow. The rail board adds wagons and night trains and a new loop at District "
          "A. Districts without a line still pay the full price of road haulage. Where rail reaches, the savings show in the "
          "first month's accounts.",
          ('rail', 'economy'), after=('lns_san_salvacion',),
          reward=(Research('train_tech', 0.5, 1), Build('infrastructure', 1, 384))),
    Focus('lns_parts_register', 'A National Register of Parts',
          "Nobody can say how many spare pumps, bearings or radio sets the coastal service, the battalions and the air wing hold "
          "between them, because each keeps its own books. A single register lists every part in every store and lets one "
          "service borrow from another. Quartermasters resent the openness. Shortages that once took weeks to solve now take "
          "a telephone call.",
          ('document', 'tools'), after=('lns_san_salvacion',), reward=(TimedIdea('parts_register', 730),)),
    Focus('lns_local_spares', 'Make the Spares at Home',
          "Expensive imports make the case the sustainment school has argued since 1991: build the commonest spare parts at "
          "home. Filters, gaskets, tyres, bearings and simple radio parts are tooled up in the existing works, at a higher unit "
          "cost than peacetime imports. The works gain steady orders. The armed forces gain parts that no distant war can "
          "delay.",
          ('tools', 'industry'), after_any=('lns_strip_for_parts', 'lns_buy_forward'), reward=(Idea('home_spares'),)),
    Focus('lns_order_books', 'Suppliers Reopen Their Books',
          "With the war in Usea recorded as an ISAF victory, foreign factories return to their peacetime customers and "
          "delivery dates begin to mean something again. The import queue for the works and the services shortens month by "
          "month. Ministers are tempted to cancel every wartime measure at once. The treasury argues for keeping half, because "
          "the next shortage will not announce itself either.",
          ('economy', 'peace'), after=('lns_parts_register',), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(TimedIdea('order_books', 365),)),
    Focus('lns_ledger', 'The Ledger Since the Lapsed Vote',
          "In 2005 the government publishes a plain ledger of what has changed since the election calendar lapsed: who governs "
          "and how, which districts gained roads, what the works and the groves produce, how the coast and the frontiers are "
          "guarded. The ledger promises nothing about the decade ahead. It records what was built, and what it cost.",
          ('document', 'scales'), after_any=('lns_local_spares', 'lns_rail_freight'), requires=(After('2005.1.1'),),
          reward=(Stability(0.03), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (CALENDAR, COAST, WORKS, GROVES, JUNGLE, HIGHLANDS, AIR, SKY, LANES)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('tapping_round', 'Pay for an Extra Tapping Round',
                'The buying office pays growers for one more tapping round before the rains. Repeatable once a year; the '
                'trees need rest between rounds.',
                40, (TimedIdea('extra_tapping', 120),), requires=(Completed('grv_latex_floor'),), cooldown=365),
    DecisionDef('storm_watch', 'Stand Up the Storm-Season Watch',
                'Lifeboat crews and patrol craft go on alert for the storm months, at the cost of fuel and crew rest. '
                'Repeatable once a year.',
                35, (TimedIdea('storm_watch', 120), XP('navy', 10)), requires=(Completed('cst_rescue_posts'),), cooldown=365),
    DecisionDef('creek_bridges', 'Bridge the Last Creeks in District D',
                'Engineers bridge the creeks that still cut the coast in the wet season. A one-time works programme.',
                75, (Build('infrastructure', 1, 543),), requires=(Completed('jun_workshop_town'),)),
    DecisionDef('depot_second_hall', 'A Second Hall at the District F Depot',
                'Funds a second workshop hall at the desert depot once the first is running. A one-time charge on the works '
                'budget.',
                90, (Build('industrial_complex', 1, 572),), requires=(Completed('hgh_depot_f'),)),
    DecisionDef('extra_staff_term', 'An Extra Term at the Hill School',
                'Another class of captains passes through the staff school, leaving their units short for six months. '
                'Repeatable once a year.',
                30, (TimedIdea('extra_staff_term', 180), XP('army', 10)), requires=(Completed('hgh_staff_school'),), cooldown=365),
    DecisionDef('sheds_inspection', 'Inspect the Spares Sheds',
                'Inspectors count and rotate the spares in every depot and publish the shortfalls. Repeatable every six '
                'months; quartermasters resent it.',
                25, (TimedIdea('sheds_inspected', 90),), requires=(Completed('wrk_one_pattern'),), cooldown=180),
)
