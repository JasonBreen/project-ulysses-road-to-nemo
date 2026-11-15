"""Verusa (VER): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic-party National
Administration with elections suspended, neutrality 48 and fascism 50 percent popularity,
tech_mountaineers and early_fighter), the country names the mod already gives each party
(Verusan Federation, Verusan Provisional Government), the unnamed starting office, the six
1991 states with their neutral district captions and hub names, the map facts read from
map/definition.csv, map/provinces.bmp and map/railways.txt, the archive Sapin event that
mentions Verusa, and the global flags other mod scripts already set. Official: ACES
Chronicle rows used only as date anchors for distant pressures, each cited by its exact key.
Everything else, including every Verusan choice, office, idea, building, decision and event,
is provisional gameplay built on the world-start role of a land and coastal reserve.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='VER', name='Verusa', root='world', package='ver',
                  themes=('security', 'navy', 'rail'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: ruling party democratic with elections_allowed = no (election_frequency 48); popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; three research slots; '
           'technology including tech_mountaineers, tech_engineers, early_fighter and basic_train; grand doctrines '
           'superior_firepower, fleet_in_being and operational_integrity. The starting leader is the unnamed National '
           'Administration office (VER_ac_government_office, centrism), whose 1991 holder has not been established. The tree '
           'never names a holder.',
           'mod/2985041246/history/countries/VER - Verusa.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names the mod already gives each ruling party: Verusan Federation (democratic), Union of Verusan Republics '
           '(communism), Verusan Provisional Government (neutrality) and Verusan Empire (monarchism). The tree uses only the '
           'Federation and Provisional Government names, as forms of government, and claims no constitutional history.',
           'mod/2985041246/localisation/english/countries_l_english.yml (VER_democratic, VER_neutrality)'),
    Source('Mod provenance',
           'Geography: 1991 states 61 (capital), 83, 88, 89, 91 and 221, captioned Verusa Capital District and Verusa District '
           'B, C, D, E and F by the neutral regional labels (canonical regional mapping unestablished). The Capital District '
           '(large city, nine plains provinces, inland) holds four civilian and two military factories, the only air base, '
           'the only fuel silo and victory point Verusa Capital Centre (2457). District D (large town, seventeen provinces, '
           'mostly jungle with mountain and hills, coastal) holds three civilian and two military factories and Logistics '
           'Centre 5668. District E (large city, nineteen provinces of jungle, hills and mountain, coastal) holds three '
           'civilian and two military factories, three dockyards, the naval base and Logistics Centre 9622. Oil, aluminium, '
           'rubber and steel lie only in those three. Districts B (hills and jungle, coastal), C (plains, inland) and F (plains, '
           'one coastal province) are towns with no buildings or resources. Land neighbours from map/provinces.bmp: Silvonia '
           '(Capital District, B and F, against Silvonia Districts C, F and H) and Yuktobania (C, D and F). District E touches '
           'no neighbour. Railways (map/railways.txt): Capital District - C - D, Capital District - E, and Capital District - '
           'B - E; District F has none. No other place is named.',
           'mod/2985041246/history/states/61-State_61.txt and the five other VER state files; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; tools/regional_labels/labels.json; '
           'mod/2985041246/localisation/english/replace/ac_world_start_hubs_l_english.yml; mod/2985041246/map/railways.txt'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role land and coastal reserve; 10 civilian, 6 military and 3 naval '
           'factories; seven infantry formations of six battalions and an engineer company (three at the Capital Centre, two '
           'at Logistics Centre 5668, two at Logistics Centre 9622); 60 fighters and 12 support aircraft on the capital air base '
           'with 15 fighters and 4 support aircraft in reserve; three coastal escorts and one coastal submarine in the '
           'Maritime Service at province 1456 in District E; 60 convoys; stocks of 1680 infantry, 960 motorised, 336 support '
           'and 28 train equipment; research priority Physical Sustainment; political institution civil_administration, '
           'capacity 40; fiscal profile GDP 120, debt ratio 0.3. Fictional calibration, not canon accounts or order of battle.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'mod/2985041246/history/units/VER_ws_land.txt, VER_ws_air.txt, VER_ws_navy.txt'),
    Source('Mod provenance',
           'Neighbour consistency: the Silvonia spec describes its District C plain running to the Verusan frontier with roads '
           'Verusan traders use, its coastal District F covering the Verusan frontier and its desert District H along the '
           'Verusan and Yuktobanian frontiers, where herders and patrols move. This tree acts only on the Verusan side of both '
           'frontiers and claims no action, consent or outcome for Silvonia or Yuktobania. No other spec names Verusa.',
           'tools/world_depth/esn/content.py'),
    Source('Mod provenance',
           'An archive Sapin diplomacy event says Sapin foreign-policy circles worry about an Osean turn towards Yuktobania and '
           'Verusa as the century ends. Used only as the premise of the Osean envoys focus; no treaty, faction or alliance '
           'follows.',
           'mod/2985041246/events/Sapin.txt (sapin_diplomacy.5); mod/2985041246/localisation/english/country_SAP_l_english.yml'),
    Source('Official',
           'Date anchor: Scinfaxi-class submarines are announced at a political convention in Cinigrad, Yuktobania. Gate of the '
           'submarine study focus; no Yuktobanian action toward Verusa is claimed.', '1991 / 09.02'),
    Source('Official',
           'Date anchor: the International Astronomical Union announces that Ulysses will pass close to Earth with a chance of '
           'impact. Opens the Ulysses branch; no Verusan role is claimed.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Gate of the oil price focuses; Verusa takes no part.', '1995 / 03.25'),
    Source('Official',
           'A treaty is signed in Lumen and the Belkan War ends. Date gate of the post-treaty focus.', '1995 / 06.20'),
    Source('Official',
           'The President of the FCU announces that Ulysses will impact the Earth. Date gate of the shelter choice; where '
           'fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Ulysses passes through the Roche limit of the Earth. Date gate of the night focus; no damage in Verusa is claimed.',
           '1999 / 07.08'),
    Source('Official',
           'Osea and Yuktobania cooperate to convert the Arkbird into a platform for clearing orbital debris. Date gate of a '
           'focus that eases Verusan unease; no Verusan role is claimed.', '1999 / 10.08'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns as anti-air batteries. '
           'Premise of the Usean war event, gated by the mod flag ac_ucw_stonehenge_seized.', '2003 / SUMMER'),
    Source('Official',
           'The FCU establishes the ISAF. Premise of the home insurance focus, gated by the mod flag ac_ucw_isaf_formed; trade '
           'only, no faction change.', '2003 / 08.22'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_ucw_stonehenge_seized and ac_ucw_isaf_formed (common/scripted_effects/'
           'ac_ucw.txt). Both gate leaf focuses, so no outcome blocks the tree.',
           'mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Verusan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; buildings only in the six 1991 '
           'states and within their free slots.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the federation by standing order
    IdeaDef('standing_order_rule', 'Rule by Standing Order', 'The National Administration governs on orders it renews itself every few months.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('document', 'command')),
    IdeaDef('nationalist_squares', 'Crowds in the Market Squares', 'Nationalist rallies fill the squares of the plain districts every week.',
            {'war_support_factor': 0.05, 'stability_factor': -0.02}, ('security', 'ballot')),
    IdeaDef('federal_assembly', 'The Federal Assembly Sits', 'An assembly elected from six districts votes every budget and every law.',
            {'stability_factor': 0.06, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('assembly', 'ballot')),
    IdeaDef('provisional_statute', 'The Provisional Statute', 'A council of officials governs for a fixed term under a written statute.',
            {'political_power_gain': 0.15, 'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.01}, ('document', 'scales')),
    IdeaDef('frontier_mobilisation', 'The Frontier Mobilisation Law', 'Every budget is judged by what it does for the frontier districts.',
            {'war_support_factor': 0.08, 'army_core_defence_factor': 0.05, 'consumer_goods_factor': 0.04}, ('security', 'command')),
    IdeaDef('sunset_clause', 'The Sunset Clause', 'The provisional council has written its own expiry date into law.',
            {'stability_factor': 0.04, 'political_power_factor': 0.05}, ('scales', 'document')),
    IdeaDef('frontier_wardens', 'Wardens of the Frontier Districts', 'A warden from the movement works beside each district governor.',
            {'army_core_defence_factor': 0.04, 'stability_factor': 0.03}, ('security', 'gate')),
    IdeaDef('federal_compact', 'The Six-District Compact', 'Fixed shares of federal revenue, courts and budget for all six districts.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('assembly', 'peace')),
    # the capital on the plain
    IdeaDef('exposed_capital', 'A Capital in the Open', 'Rail, fuel, aircraft and government all wait on one city on an open plain.',
            {'stability_factor': -0.02, 'army_core_defence_factor': 0.02}, ('security', 'civil')),
    IdeaDef('ninety_day_stores', 'Ninety Days of Grain', 'Federal granaries hold a season of food for the capital and its garrison.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('shelter', 'logistics')),
    IdeaDef('second_seat', 'The Standby Ministries', 'Copies of the records and a skeleton government wait in District E.',
            {'stability_factor': 0.04, 'planning_speed': 0.05}, ('command', 'rail')),
    IdeaDef('capital_holds', 'The Capital Holds Its Ground', 'Every ministry stays on the plain and the city is made harder to stop.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.03}, ('security', 'medal')),
    IdeaDef('block_wardens', 'Block Wardens', 'A volunteer warden with a list and a cellar key in every capital block.',
            {'stability_factor': 0.03, 'static_anti_air_damage_factor': 0.05}, ('civil', 'shelter')),
    # the coastal plants
    IdeaDef('coastal_ledger', 'The Coastal Plant Ledger', 'A full count of every plant, plot and well on the coast.',
            {'production_factory_efficiency_gain_factor': 0.02}, ('industry', 'document')),
    IdeaDef('deep_plants', 'Deeper, Not Wider', 'New tools and foremen inside the coastal halls that already exist.',
            {'production_factory_efficiency_gain_factor': 0.05, 'production_factory_max_efficiency_factor': 0.04}, ('tools', 'industry')),
    IdeaDef('spread_plants', 'Plants Beyond the Coast', 'Federal credit for new halls in the districts that have none.',
            {'production_speed_industrial_complex_factor': 0.10, 'production_speed_arms_factory_factor': 0.05}, ('industry', 'rail')),
    IdeaDef('oil_board', 'The Federal Oil Board', 'One board buys the crude, sets the price and sells the surplus.',
            {'political_power_gain': 0.10, 'consumer_goods_factor': -0.03}, ('economy', 'logistics')),
    # the railway
    IdeaDef('coaster_link', 'The Coaster Link', 'Small ships carry oil and steel between the District D and District E harbours.',
            {'production_speed_buildings_factor': 0.05, 'supply_consumption_factor': -0.03}, ('navy', 'logistics')),
    IdeaDef('ballasted_lines', 'Ballasted Lines', 'Standing gangs keep the track firm through the wet season.',
            {'production_speed_infrastructure_factor': 0.10}, ('rail', 'tools')),
    IdeaDef('train_reserve', 'The Train Reserve', 'A share of the trains is kept serviced and out of daily use.',
            {'supply_consumption_factor': -0.05, 'army_speed_factor': 0.03}, ('rail', 'command')),
    # the army
    IdeaDef('mountain_school', 'The Coastal Mountain School', 'A battalion from each formation learns the mountains behind the coast.',
            {'army_attack_factor': 0.03, 'experience_gain_army_factor': 0.05}, ('training', 'tools')),
    IdeaDef('plain_defence', 'Defence on the Plain', 'The formations train to hold the open ground beside both frontiers.',
            {'army_core_defence_factor': 0.08, 'army_defence_factor': 0.04}, ('security', 'gate')),
    IdeaDef('depth_defence', 'Depth Behind the Jungle', 'Delay on the plain, then hold the jungle hills and mountains of the coast.',
            {'attrition': -0.05, 'army_org_factor': 0.05}, ('command', 'shelter')),
    IdeaDef('wheeled_reserve', 'A Wheeled Reserve', 'The formations wait at the coast and move by lorry and train.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.10}, ('logistics', 'command')),
    IdeaDef('reserve_roll', 'The Roll of Former Conscripts', 'Every former soldier listed by district, trade and last unit.',
            {'training_time_army_factor': -0.10}, ('document', 'security')),
    IdeaDef('timetabled_reserve', 'Every Reservist Has a Train', 'Each reservist knows his train, his station and his hour.',
            {'training_time_army_factor': -0.15, 'army_org_factor': 0.04}, ('rail', 'security')),
    # the maritime service
    IdeaDef('hydrophone_watch', 'Listening Huts on the Coast', 'Shore radar and listening huts report every contact near the harbour.',
            {'naval_coordination': 0.06}, ('submarine', 'radar')),
    IdeaDef('freighter_pool', 'The Freighter Pool', 'Sixty freighters sail on one federal schedule the escorts can cover.',
            {'naval_speed_factor': 0.04, 'consumer_goods_factor': -0.02}, ('navy', 'economy')),
    IdeaDef('yard_apprentices', 'The Apprentice Classes', 'A school for hull, engine and electrical work beside the yards.',
            {'industrial_capacity_dockyard': 0.05}, ('tools', 'navy')),
    IdeaDef('fishery_patrol', 'Escorts on the Fishing Grounds', 'The escorts patrol the fishing grounds and help boats in trouble.',
            {'navy_org_factor': 0.04, 'stability_factor': 0.01}, ('fishing', 'navy')),
    # the air arm
    IdeaDef('capital_sky', 'Fighters Over the Capital', 'The air arm exists first to keep hostile aircraft off the capital.',
            {'air_superiority_efficiency': 0.06, 'air_detection': 0.05}, ('air', 'security')),
    IdeaDef('formation_wings', 'Wings for the Formations', 'Fighters and support aircraft train with the army on plain and hill.',
            {'air_mission_efficiency': 0.06, 'experience_gain_air_factor': 0.08}, ('air', 'training')),
    IdeaDef('coastal_flying_school', 'The Coastal Flying School', 'Student pilots learn over the quiet coast, far from both frontiers.',
            {'experience_gain_air_factor': 0.05, 'training_time_factor': -0.05}, ('training', 'air')),
    # the two frontiers
    IdeaDef('silvonian_road', 'Trade on the Silvonian Road', 'Customs, roads and market rules for the frontier beside the capital.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('diplomacy', 'logistics')),
    IdeaDef('northern_watch', 'Watch on the Northern Line', 'Survey markers, patrols and posts along the Yuktobanian frontier.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.03}, ('security', 'gate')),
    IdeaDef('frontier_markets', 'Licensed Markets on the Western Line', 'Licensed markets twice a month in the western frontier towns.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('economy', 'civil')),
    IdeaDef('plain_patrols', 'Patrols on the Open Plain', 'Mounted and motor patrols ride fixed routes between the marker stones.',
            {'army_speed_factor': 0.03, 'army_core_defence_factor': 0.03}, ('security', 'logistics')),
    IdeaDef('herder_passes', 'Seasonal Herder Passes', 'The herders of District F cross with a pass the law recognises.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('document', 'peace')),
    IdeaDef('osean_attention', 'Osean Visitors', 'Osean diplomats call on the capital more often than they used to.',
            {'political_power_gain': 0.05, 'research_speed_factor': 0.02}, ('diplomacy', 'communications')),
    IdeaDef('quiet_north', 'A Quieter Northern Sky', 'Cooperation between Osea and Yuktobania eases the watch on the north.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('peace', 'satellite')),
    # the asteroid
    IdeaDef('sky_watch_office', 'A Budget Line for the Sky', 'A small federal office watches the sky and plans for the worst.',
            {'research_speed_factor': 0.02, 'air_detection': 0.03}, ('telescope', 'document')),
    IdeaDef('permanent_watch', 'The Permanent Sky Watch', 'Observer posts and district stocks kept after the long night.',
            {'research_speed_factor': 0.03, 'air_detection': 0.05}, ('telescope', 'radar')),
    IdeaDef('peak_observers', 'The Peak Observers', 'Volunteer observers with telescopes and radios on the coastal peaks.',
            {'air_detection': 0.08}, ('telescope', 'communications')),
    IdeaDef('impact_nerves', 'Nerves Before the Impact', 'The public waits for fragments nobody can place.',
            {'stability_factor': -0.04, 'war_support_factor': 0.04}, ('meteor', 'civil')),
    IdeaDef('plain_shelters', 'Shelters Under the Plain', 'Concrete shelters built from nothing under the capital and plain towns.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('hill_evacuation', 'The Hill Evacuation Plan', 'Trains, camps and billets to take the plain towns into the coastal hills.',
            {'stability_factor': 0.04, 'planning_speed': 0.05}, ('shelter', 'rail')),
    IdeaDef('district_stocks', 'Stocks in Every District', 'Water, lamp oil, medicine and food for a fortnight in each district office.',
            {'stability_factor': 0.03}, ('logistics', 'shelter')),
    # distant wars and the price of oil
    IdeaDef('war_premium', 'Crude at Wartime Prices', 'Verusan crude sells abroad at prices set by somebody else\'s war.',
            {'political_power_gain': 0.12, 'stability_factor': -0.02}, ('economy', 'navy')),
    IdeaDef('crude_reserve', 'Crude Kept at Home', 'Exports are capped and the tanks at home are full.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.03}, ('logistics', 'industry')),
    IdeaDef('standing_buyers', 'Buyers Who Stayed', 'Wartime buyers kept on long contracts at ordinary prices.',
            {'consumer_goods_factor': -0.03, 'industrial_capacity_factory': 0.03}, ('diplomacy', 'economy')),
    IdeaDef('home_insurance', 'The Home Insurance Pool', 'The treasury insures Verusan freighters and tankers itself.',
            {'naval_speed_factor': 0.03, 'stability_factor': 0.02}, ('scales', 'navy')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('federal_cabinet', 'Cabinet of the Federal Assembly',
           'A cabinet chosen by and answerable to a federal assembly elected from all six districts, governing collectively on '
           'a fixed election calendar under the name of the Verusan Federation. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism', elections=True),
    Office('provisional_council', 'Council of the Provisional Government',
           'A council of senior officials, plant managers and railway engineers governing for a fixed term under a provisional '
           'statute, with no assembly sitting; the mod already names this form the Verusan Provisional Government. Provisional '
           'gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('frontier_committee', 'Committee of the Frontier Districts',
           'A committee drawn from the nationalist movement of the plain districts, ruling by decree with a frontier warden '
           'beside every district governor. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('standing_orders', 'The Renewal Minuted by Name', (
        "The standing order that lets the National Administration govern without an election comes up for renewal again, as "
        "it does every few months, and this time the cabinet secretary has ruled a column beside each minister's name. The "
        "Verusan Federation has six districts, a capital on its western plain and a ruling party almost nobody votes for. Until "
        "now the renewal has passed in silence. Today every minister's answer will be written down.",
        "The figures in the ministers' folders are blunt. Half the country answers to a nationalist movement whose rallies "
        "fill the squares of District C and District F, plain districts on the Yuktobanian frontier with no plant and no "
        "garrison. Nearly all the rest follows no movement at all: officials, plant managers, railway engineers and harbour "
        "masters who want rules that work. The democrats whose name the Administration carries would fit in one hall.",
        "The renewal will pass; nobody doubts that. What the ministers must decide is whether the minutes leave the building. "
        "Published, they show the country a government that knows it is temporary and says so. Kept in the cabinet safe, they "
        "let the Administration choose its successor quietly, at the price of every rumour the capital can invent.",
    ), (
        Option('Publish the minutes.', (Stability(0.02), PP(-15))),
        Option('Keep the minutes in the cabinet safe.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('capital_plain', 'One Junction, One Runway, One Silo', (
        "The staff study arrives on the cabinet table bound in plain grey card. Its first page is a map of the Capital District: "
        "nine provinces of open plain, the Silvonian frontier along its western edge, and the junction where every Verusan "
        "railway line begins. Marked in red are the federation's only air base, its only fuel silo, its largest garrison and "
        "four of its ten plant halls.",
        "The study accuses nobody. Silvonia is a neighbour whose farming district across the line sends traders and grain "
        "carts, and nothing in the files suggests it wishes Verusa harm. The authors simply ask what the federation would do "
        "if its capital stopped working for a week, whatever the cause: fire, flood, a strike, something from the sky. Their "
        "answer is that it would do very little, because everything waits on the capital.",
        "Two replies circulate before the ink is dry. One says the government should prepare a second seat far from the plain, "
        "in the port of District E behind its jungle hills. The other says the capital must be made harder to stop, and that a "
        "government which plans to leave has already half left. The cabinet can begin by putting the study before the public, "
        "or by keeping it inside the staff.",
    ), (
        Option('Publish the study.', (WarSupport(0.03), Stability(-0.01))),
        Option('Keep it inside the staff.', (PP(25),)),
    ), picture=2),
    EventDef('coast_ledger', 'A Waiting List for Land', (
        "The plant survey of Districts D and E comes back with a document nobody expected: a waiting list. Every plot near the "
        "coastal railheads with power, water and a siding already holds a plant hall, an arms works or a yard. Firms that want "
        "to expand have queued for land for years, and some have stopped asking. The coast, which carries all of the "
        "federation's industry outside the capital, has run out of room.",
        "The survey also counts what comes out of the ground. Oil, steel and aluminium are split almost evenly between the "
        "Capital District, District D and District E, with a little rubber in each. Districts B, C and F hold none of it and "
        "no plants either. Their young workers take the train to the coast, where housing is short and the managers pick the "
        "strongest hands first.",
        "The planning office sees three directions: make the existing halls produce more, build new halls in the empty "
        "districts, or organise everything around the oil. Each has champions in the ministries and the districts. Before "
        "choosing, the office must decide whether to publish the waiting list, which would embarrass the coastal managers and "
        "delight the governors of the empty districts.",
    ), (
        Option('Publish the waiting list.', (Stability(0.01), PP(-10))),
        Option('Pass it to the ministries only.', (PP(20), Stability(-0.01))),
    ), picture=1),
    EventDef('rail_junction', 'Every Train Waits at the Capital', (
        "The railway office's survey of the network is short because the network is short. Three lines leave the capital: one "
        "across the District C plain to District D, one straight to the port of District E, and one through the hills of "
        "District B to the same port. There is no line between the two coastal districts, none into District F, and none that "
        "avoids the capital junction.",
        "On an ordinary day the arrangement works. Grain comes in from District C, crude and steel from the coast, and troops "
        "and mail go out in every direction, all of it sorted in one yard. On a bad day, the survey warns, a single derailment "
        "in that yard would stop freight to every district at once. No such stoppage is on record, the authors admit, but no "
        "plan exists for one either.",
        "The office asks for two things. The first is money to keep the existing lines sound through the wet season, when the "
        "hill section in District B always suffers first. The second is a decision on whether the federation needs a route "
        "that avoids the capital, by road or by sea. The cabinet can approve the first at once and argue about the second for "
        "years.",
    ), (
        Option('Send inspectors to the hill section now.', (PP(-10), Event('washout', 20))),
        Option('File the survey for the next budget.', (PP(20), Stability(-0.01))),
    ), picture=2),
    EventDef('washout', 'The Hill Embankment Slips', (
        "The inspectors reach the District B hill section in the middle of the rains and find what they feared. A long "
        "embankment above a jungle ravine has begun to slide, with cracks across the ballast and water forcing through a "
        "culvert built for a smaller stream. Trains still cross it at walking pace. The engineers give it weeks, perhaps less, "
        "before it goes.",
        "Closing the section would send every train between the capital and the port onto the direct line to District E, "
        "which is already busy. Keeping it open while crews rebuild the culvert risks a train and its crew. The district "
        "governor wants the line kept open because the hill towns live on it. The railway office wants it shut, because a "
        "derailment would close it for far longer.",
        "There is a third and dearer answer: bring work trains, gangs and ballast from every line in the federation, rebuild "
        "the culvert by night and run traffic by day. It would spend the railway office's maintenance money for the year and "
        "stop repairs everywhere else. The cabinet must choose before the next heavy rain chooses for it.",
    ), (
        Option('Close the section and rebuild it properly.', (Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Rebuild by night and run by day.', (PP(-30), Stability(0.02))),
        Option('Keep the trains crawling over it.', (PP(15), Stability(-0.03))),
    ), picture=2),
    EventDef('seven_formations', 'Three Garrisons, Three Empty Districts', (
        "The muster takes a month, because every formation must be counted in its own garrison and there are only three "
        "garrisons: the capital holds three formations and each coastal logistics centre holds two. Every formation has six "
        "infantry battalions and an engineer company, rifles for every man, lorries in uncertain condition and very little "
        "artillery. The counting officers sign for each rifle and note each lorry that will not start.",
        "The muster officers also record where the army is not. Not one battalion is quartered in District B, District C or "
        "District F, the three districts that carry most of both frontiers. A unit ordered there travels by rail through the "
        "capital or, for District F, by road, because no railway reaches it. The plain districts know this, and the nationalist "
        "papers print it every week.",
        "The general staff must now tell the government what the army is for. It could be a force that holds the capital on "
        "the plain, a force that holds the coast and gives ground, or a reserve that moves wherever it is needed. The full "
        "report will take months. Its first page, the only one most ministers will read, has to be agreed now.",
    ), (
        Option('Report the gaps honestly.', (WarSupport(0.03), Stability(-0.01))),
        Option('Report readiness and fix the gaps quietly.', (Stability(0.02), XP('army', 10))),
    ), picture=0),
    EventDef('four_hulls', 'Sixty Freighters, Four Warships', (
        "The Maritime Service presents its annual report in person this year, at the government's request. Three coastal "
        "escorts and one coastal submarine, all based at the District E harbour, guard a coast that runs from the hills of "
        "District B past the port to the jungle of District D. Sixty coastal freighters carry grain, crude, steel and passengers "
        "along it and out to markets abroad.",
        "The commanders do not ask for a fleet. They ask for things they consider modest: a second place to repair a hull if "
        "the District E yards are ever out of action, better charts of a coast whose sandbanks have moved since the last "
        "survey, and a ruling on whether their job is to escort freighters or to watch the harbour approaches. Four ships "
        "cannot do both.",
        "The ministers listen politely and then argue among themselves. The coastal districts want the service seen at sea, "
        "the capital wants it cheap, and nobody wants to tell the public that the federation's navy fits in one harbour. The "
        "government can at least decide whether the report is debated in the open or filed.",
    ), (
        Option('Debate the report in the open.', (WarSupport(0.02), PP(-10))),
        Option('File it and fund the yards quietly.', (PP(15), XP('navy', 10))),
    ), picture=1),
    EventDef('frontier_field', 'A Field the Neighbours Can See', (
        "Every Verusan combat aircraft is parked on one air base in the Capital District, sixty fighters and twelve support "
        "aircraft wing to wing on the same aprons. The base shares the capital's fuel silo and its railway junction, which "
        "makes supply easy and makes the whole air arm a single target. From the end of the main runway, the air staff points "
        "out, the Silvonian frontier is a short flight away.",
        "Nobody suggests that Silvonia means harm, and the air staff is careful to say so. Its argument is plainer. An air arm "
        "that one fire, one flood or one accident on a crowded apron can put out of action is not an air arm a federation "
        "should depend on. The staff wants a second field behind the hills of District E and a strip near the District D "
        "logistics centre.",
        "Pilots and their families like living in the capital, and the capital's suppliers like the pilots. Splitting the air "
        "arm means new housing, new fuel tanks and maintenance crews divided between fields. The finance ministry asks what the "
        "first new field would cost. The air staff answers with a number, and the government must decide whether to start "
        "paying it.",
    ), (
        Option('Begin the dispersal at once.', (PP(-20), XP('air', 15))),
        Option('Wait for the next budget.', (PP(20), Stability(0.01))),
    ), picture=0),
    EventDef('two_frontiers', 'Reports from Both Lines', (
        "The survey teams come back from the frontiers with very different notebooks. The western team, working along the "
        "Silvonian frontier beside the capital and through the hills of District B, describes farm carts, traders, a few "
        "smugglers and long queues at the crossing huts. Silvonia's farming district lies across the plain, and much of the "
        "traffic is simply people buying and selling across a line they have always crossed.",
        "The northern team, working along the Yuktobanian frontier through the plain of District C, the open country of "
        "District F and the jungle of District D, describes long stretches where no post stands for days. Nobody has set a "
        "marker stone in living memory. The team found no trouble, but it also found that nobody on the Verusan side would "
        "have known if there had been any.",
        "District F appears in both notebooks, the only district that touches both neighbours and the only one without a "
        "railway. The cabinet has money for one frontier programme at a time. Before it decides which line comes first, it can "
        "publish both reports, or keep the northern one confidential so as not to alarm the plain districts.",
    ), (
        Option('Publish both reports.', (Stability(0.01), WarSupport(0.02))),
        Option('Keep the northern report confidential.', (PP(25), Stability(-0.01))),
    ), picture=0),
    EventDef('impact_announced', 'Where Will the Pieces Fall', (
        "In April 1996 the President of the FCU tells the world that Ulysses will strike the Earth and that plans to counter "
        "it are under way. No astronomer will say where the fragments will land. In Verusa the news comes over the evening "
        "radio, and by morning the capital's shops have sold out of water containers, candles and lamp oil.",
        "The federation's position is awkward. Its capital, its largest garrison and its only air base stand on open plain "
        "with no rock to dig into and no hills to hide behind. Its coast has jungle hills, mountains and old workings that "
        "could shelter thousands, but the coast is reached by three railway lines that all start in the capital. Every plan "
        "anyone drafts begins at that junction.",
        "The ministers must give the public something before the rumours take over. They can announce at once that shelter "
        "plans are being drawn up and ask for patience, which will reassure some families and frighten others. Or they can say "
        "only that the government is studying the matter, which buys time and leaves the field to every rumour in the capital.",
    ), (
        Option('Announce shelter planning at once.', (WarSupport(0.02), Stability(-0.02))),
        Option('Say the matter is under study.', (Stability(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20; Verusan preparations are gameplay',
        picture=2),
    EventDef('roche_night', 'The Junction on the Long Night', (
        "On 8 July 1999 Ulysses passes through the Roche limit and begins to break apart. Verusa spends the night awake. The "
        "district wardens keep their lists by the door, the observer posts on the coastal peaks keep their radios open, and "
        "the capital's railway junction, the hinge of every Verusan emergency plan, runs on the night timetable with every "
        "signal box manned.",
        "The junction is where the night is decided. Families with relatives on the coast crowd the capital station hoping "
        "for seats the timetable reserved for the sick and the old, and stationmasters hold them back with lists and "
        "patience. Freight waits in the sidings so that passenger trains can move, and by morning the coastal plants are short "
        "of crude because nothing heavy has passed through the yard.",
        "When daylight comes nothing on Verusan soil has been confirmed as fallen, and nothing has been ruled out either. The "
        "cabinet must decide whether to keep the night timetable until every district has reported, or release the freight at "
        "once and let the coast restart its plants. Either way, the junction has shown how much depends on it.",
    ), (
        Option('Keep the night timetable until every district reports.', (WarSupport(0.02), PP(-15))),
        Option('Release the freight at once.', (PP(20), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no damage in Verusa is claimed', picture=2),
    EventDef('belkan_prices', 'Premiums on Every Barrel', (
        "On 25 March 1995 war breaks out around Belka, on the far side of the world from the Verusan coast. The first thing "
        "the federation feels is not fear but the telephone. Brokers who never showed interest in Verusan crude ask for "
        "prices, charter rates for tankers climb week by week, and insurers attach war clauses to cargoes that will never pass "
        "near the fighting.",
        "The coastal producers are delighted and the coastal plants are not. Every barrel sold abroad at war prices is a "
        "barrel the plants, the railways and the Maritime Service must now buy at the same price. The capital's fuel silo, the "
        "only one in the federation, holds a modest reserve. The nationalist papers ask why Verusa should profit from somebody "
        "else's war, and the producers ask why it should not.",
        "The government cannot set the world price, but it can decide how much crude leaves the federation. It can let the "
        "buyers take all they want, or cap exports and fill the tanks at home. Either answer sends a message to buyers who "
        "will remember it when the war is over, and to producers who will remember it at every budget.",
    ), (
        Option('Let the buyers have it.', (PP(25), Stability(-0.01))),
        Option('Cap exports for now.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; Verusa takes no part in the war', picture=1),
    EventDef('usean_war', 'Stonehenge and the Freight Market', (
        "The news from Usea in the summer of 2003 is that Erusea has marched into San Salvacion for all its neutrality, taken "
        "Stonehenge, and put the great railguns to work against aircraft. Usea lies a long way from the Verusan coast and the "
        "federation has no part in the war. Within weeks, all the same, the brokers are calling again and the insurers are "
        "rewriting their clauses.",
        "The insurers move first. Rates rise on cargoes anywhere near a sea lane they consider exposed, and the federation's "
        "sixty freighters, which never sail near Usea, are caught in the same clauses as everyone else. Owners on the coast "
        "threaten to lay up their ships. The oil producers, meanwhile, expect another windfall and have begun to say so in "
        "public.",
        "The air staff adds a question of its own: what a weapon that fires on aircraft from the ground means for an air arm "
        "that is small and has few fields. The government cannot answer every question at once. It can order a staff study of "
        "the Usean war, which takes officers from their posts for a year, or leave the war to the brokers and keep its own "
        "budget as it is.",
    ), (
        Option('Order a staff study of the war.', (XP('air', 15), PP(-20))),
        Option('Leave it to the brokers.', (PP(25), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / SUMMER; the Verusan response is gameplay', picture=1),
)

# --- branches ------------------------------------------------------------------------------------
FEDERATION = Branch('fed', 'The Federation by Standing Order', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('fed_orders', 'Government by Standing Order',
          "The National Administration governs the Verusan Federation through standing orders it renews every few months, with "
          "elections suspended and a democratic label that roughly one voter in a hundred supports. The cabinet now minutes "
          "each renewal by name, so every minister must say on paper what should replace the arrangement. The vote settles "
          "nothing yet, but it ends the habit of pretending the question is not there.",
          ('document', 'command'), reward=(Idea('standing_order_rule'), Event('standing_orders'))),
    Focus('fed_petitions', 'Town Councils Ask for a Vote',
          "Town councils in the six districts send petitions asking for a federal assembly with seats for every district. Most "
          "signatures come from the Capital District and the two coastal plant districts, where clerks, dockers and plant "
          "engineers want a say in the budget. Receiving the petitions formally, instead of filing them, costs the "
          "Administration some authority and gives the small democratic camp a document to stand on.",
          ('ballot', 'civil'), after=('fed_orders',), reward=(Flag('councils_petition'), Stability(0.02))),
    Focus('fed_squares', 'The Nationalist Half of the Country',
          "Half of Verusa answers to the nationalist movement, whose rallies fill the market squares of District C and "
          "District F, the plain districts that face Yuktobania with no plant and no garrison of their own. Its speakers want "
          "a government that treats the northern frontier as the first question of state. Letting the rallies run unhindered "
          "costs calm in the towns and shows exactly how many people the movement can bring out.",
          ('security', 'ballot'), after=('fed_orders',),
          reward=(TimedIdea('nationalist_squares', 365), Flag('movement_counted'))),
    Focus('fed_statute', 'Officials Draft a Provisional Statute',
          "The other half of the country is less a movement than a class: ministry officials, plant managers, railway "
          "engineers and harbour masters who want rules that work more than they want a creed. A drafting group from their "
          "ranks writes a statute that would let a council of officials govern for a fixed term with no assembly and no "
          "rallies. Drafting it openly earns them the distrust of both other camps.",
          ('document', 'scales'), after=('fed_orders',), reward=(Flag('statute_drafted'), PP(20))),
    Focus('fed_assembly', 'Reopen the Federal Assembly',
          "The Administration hands power to a federal assembly elected from all six districts, with a cabinet answerable to it "
          "and a fixed election calendar. The democratic camp is tiny, so the first assembly will be full of deputies who never "
          "wanted it and must now learn to bargain inside it. The cost is speed: every budget, garrison posting and road "
          "contract becomes a vote that can be lost.",
          ('assembly', 'ballot'), after=('fed_petitions',), cost=10, exclusive=('fed_provisional', 'fed_committee'),
          requires=(HasFlag('councils_petition'),),
          reward=(Regime('federal_cabinet'), SwapIdea('standing_order_rule', 'federal_assembly'), Flag('path_assembly'))),
    Focus('fed_provisional', 'Proclaim a Provisional Government',
          "The officials' statute takes effect and the Administration gives way to a provisional government: a council of "
          "senior officials and managers ruling for a fixed term while the federation is rebuilt on paper. Decisions come "
          "quickly and the ministries finally get budgets they can plan around. Nobody voted for the council, and the term it "
          "sets itself will be tested the first time it runs out.",
          ('command', 'document'), after=('fed_statute',), cost=10, exclusive=('fed_assembly', 'fed_committee'),
          requires=(HasFlag('statute_drafted'),),
          reward=(Regime('provisional_council'), SwapIdea('standing_order_rule', 'provisional_statute'), Flag('path_provisional'))),
    Focus('fed_committee', 'A Committee for the Frontier Districts',
          "The nationalist movement takes the seals and sets up a committee that governs by decree in the name of the frontier "
          "districts. Its first law places a frontier warden beside every district governor and asks of every budget what it "
          "does for the northern line. The movement brings crowds and conviction into government, and leaves the officials and "
          "the democrats without a chair at all.",
          ('security', 'command'), after=('fed_squares',), cost=10, exclusive=('fed_assembly', 'fed_provisional'),
          requires=(HasFlag('movement_counted'),),
          reward=(Regime('frontier_committee'), SwapIdea('standing_order_rule', 'frontier_mobilisation'), Flag('path_committee'))),
    Focus('fed_first_budget', 'The First Budget Debated in Public',
          "The new assembly reads its first budget line by line in an open chamber, and the deputies from District F point out "
          "that their district has neither a railway nor a graded road. A road grant for District F passes as the price of "
          "their votes for the coastal plant budget. Open budgets are slower and noisier than decrees, and this one starts the "
          "habit of trading districts against each other.",
          ('economy', 'assembly'), after=('fed_assembly',), requires=(HasFlag('path_assembly'),),
          reward=(Build('infrastructure', 1, 221),)),
    Focus('fed_sunset', 'A Sunset Date for the Council',
          "The provisional council writes its own expiry date into the statute, with a review by an elected body when the date "
          "arrives. The clause reassures the towns that the council does not mean to stay forever, and it gives ministers a "
          "deadline that concentrates their minds. Ambitious officials dislike a clock on their power, and every crisis will "
          "tempt the council to wind the clock back.",
          ('scales', 'document'), after=('fed_provisional',), requires=(HasFlag('path_provisional'),),
          reward=(Idea('sunset_clause'),)),
    Focus('fed_wardens', 'Wardens Beside Every Governor',
          "Under the committee each of the six district governors works beside a frontier warden appointed from the movement. "
          "The wardens inspect garrisons, road works and grain stores and report straight to the committee. Frontier projects "
          "in District C and District F, which have waited longest, finally move. The paperwork in every district office "
          "doubles, and every governor becomes a suspect in his own building.",
          ('security', 'gate'), after=('fed_committee',), requires=(HasFlag('path_committee'),),
          reward=(Idea('frontier_wardens'),)),
    Focus('fed_compact', 'Signing the Six-District Compact',
          "Whatever government holds the seals, the six districts sign a compact fixing their shares of federal revenue, the "
          "language of the district courts and the order of the federal budget. The Capital District gives up part of its lead "
          "in road money, and the coastal districts accept that their plant taxes will pay for the plain. It is mostly "
          "bookkeeping, and it stops the federation being renegotiated every year.",
          ('assembly', 'peace'), after_any=('fed_first_budget', 'fed_sunset', 'fed_wardens'),
          reward=(Idea('federal_compact'), Flag('compact_signed'))),
    Focus('fed_district_treasuries', 'District Treasuries for the Empty Towns',
          "The compact's first payment goes to the three districts with no plants at all. District F, which borders both "
          "neighbours and has neither rail nor industry, receives a federal works grant for its first plant hall. The money "
          "comes from the coastal districts, whose representatives will watch the hall's books closely. It is a small plant, "
          "and the first proof that the compact means anything.",
          ('economy', 'civil'), after=('fed_compact',), requires=(HasFlag('compact_signed'),),
          reward=(Build('industrial_complex', 1, 221),)),
))

PLAIN = Branch('plain', 'The Capital on the Open Plain', 1991, 'FOCUS_FILTER_STABILITY', (
    Focus('plain_exposed', 'A Capital With No Hills Around It',
          "The Capital District is nine provinces of open plain, and its western edge is the Silvonian frontier. The federation "
          "keeps there its largest garrison, its only air base, its only fuel silo and the junction of every railway line. "
          "Planners have always called this convenient. A staff study now asks the question nobody wanted printed: what "
          "happens to Verusa if the capital stops working for a week.",
          ('security', 'civil'), reward=(Idea('exposed_capital'), Event('capital_plain'))),
    Focus('plain_ring_road', 'Paving the Capital Ring Road',
          "Traffic from all three railway lines and every district road meets in the centre of the capital, where carts, "
          "lorries and garrison convoys share the same streets. A paved ring around the centre lets freight and troops move "
          "between the lines without crossing the market quarter. The works close streets for a year and anger shopkeepers, "
          "but the capital stops choking every time a long train arrives.",
          ('logistics', 'civil'), after=('plain_exposed',), reward=(Build('infrastructure', 1, 0),)),
    Focus('plain_granaries', 'Granaries Beside the Rail Yards',
          "The capital eats grain from the District C plain and fish from the coast, and both arrive by rail through the same "
          "junction. Federal granaries beside the yards would hold ninety days of flour and preserved food for the city and its "
          "garrison. They need buying, storage and guards, and grain merchants complain that the state is cornering their "
          "trade. A capital that can feed itself for a season is harder to frighten.",
          ('shelter', 'logistics'), after=('plain_exposed',), reward=(Idea('ninety_day_stores'),)),
    Focus('plain_second_seat', 'A Standby Seat in District E',
          "District E is a large port city behind jungle hills, as far from both frontiers as the federation reaches. Standby "
          "ministries there, with copies of the records, a radio link and a skeleton staff, would let the government keep "
          "working if the capital were cut off. The plan admits in public that the capital is exposed, and its merchants read "
          "it as a vote of no confidence in their city.",
          ('command', 'rail'), after_any=('plain_ring_road', 'plain_granaries'), cost=10, exclusive=('plain_hold',),
          reward=(SwapIdea('exposed_capital', 'second_seat'), Flag('seat_in_e'))),
    Focus('plain_hold', 'The Government Stays on the Plain',
          "The opposite answer keeps every ministry in the capital and spends the money on making the city harder to stop: a "
          "larger garrison, radar on the city edge, wardens in every block. Officials and merchants stay where they are and the "
          "capital's pride is spared. The federation keeps every egg in one basket on an open plain, and wagers that a basket "
          "guarded well enough will do.",
          ('security', 'command'), after_any=('plain_ring_road', 'plain_granaries'), cost=10, exclusive=('plain_second_seat',),
          reward=(SwapIdea('exposed_capital', 'capital_holds'), Flag('capital_stays'))),
    Focus('plain_night_trains', 'Records by Night Train',
          "Copies of the land registry, tax rolls, payroll lists and federal court records travel to District E by night train "
          "under guard, a few wagons at a time. The line through the jungle hills needs new sidings and a goods yard at the port "
          "to receive them. Clerks hate the double filing. Within two years every important federal document exists in two "
          "places a day's journey apart.",
          ('rail', 'document'), after=('plain_second_seat',), requires=(HasFlag('seat_in_e'),),
          reward=(Build('infrastructure', 1, 91),)),
    Focus('plain_radar', 'Radar Masts on the City Edge',
          "A radar station on the western edge of the capital watches the open sky over the Silvonian frontier and the "
          "approaches to the only air base. The site needs power lines, a hardened plotting room and crews trained to tell an "
          "airliner from anything else. Silvonian officials will notice the masts. The federation's answer is that the station "
          "watches sky, not ground, and claims nothing beyond the line.",
          ('radar', 'security'), after=('plain_hold',), requires=(HasFlag('capital_stays'),),
          reward=(Build('radar_station', 1, 0),)),
    Focus('plain_last_plot', 'The Last Free Plot in the Capital',
          "The capital's four plant halls and two arms works leave room for exactly one more large building. The planning "
          "office decides it should be a hall for spare parts, lorries and rail equipment, the goods the garrison and the "
          "railways run short of first. The plot goes to the state rather than the highest bidder, which annoys the capital's "
          "builders and closes the last gap for good.",
          ('industry', 'tools'), after=('plain_ring_road',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('plain_block_wardens', 'Wardens for Every City Block',
          "Every block in the capital gets a volunteer warden with a list of residents, a key to the nearest cellar and a "
          "telephone number for the district office. In an emergency the wardens count heads, guide people to cover and report "
          "damage. They cost little beyond training evenings. Some residents welcome a neighbour who knows the plan, and others "
          "dislike a neighbour who keeps a list.",
          ('civil', 'shelter'), after_any=('plain_night_trains', 'plain_radar'), reward=(Idea('block_wardens'),)),
    Focus('plain_plan', 'The Capital Plan Goes to Print',
          "The federal planning office prints the capital plan in full: where the ministries go in an emergency, which roads "
          "stay open, where the grain is kept and which trains leave first. Publishing it tells every resident what to do, and "
          "tells every observer exactly the same. The office judges that a plan the public knows is worth more than a plan only "
          "the ministries understand.",
          ('document', 'civil'), after=('plain_block_wardens',), reward=(Flag('capital_plan_printed'), PP(15))),
))

COAST = Branch('coast', 'Plants of the Jungle Coast', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('coast_ledger', 'Every Coastal Plot Is Spoken For',
          "Districts D and E carry all of the federation's industry outside the capital: three plant halls and two arms works "
          "in each, with the only yards and the only naval base in District E. Both districts are full, and every plot with "
          "power, water and a siding already has a building on it. A plant survey counts what the coast produces and where the "
          "next hall could possibly go.",
          ('industry', 'document'), reward=(Idea('coastal_ledger'), Event('coast_ledger'))),
    Focus('coast_haul_road', 'A Haul Road Through the District D Jungle',
          "District D's oil, steel and aluminium reach the capital by one line that runs back through District C, and the jungle "
          "between the wells and the railhead floods every wet season. A gravelled haul road on a raised bank keeps lorries "
          "moving when the sidings are under water. Building it through seventeen provinces of jungle, mountain and hill is "
          "slow, and the crews lose weeks to rain and fever.",
          ('logistics', 'tools'), after=('coast_ledger',), reward=(Build('infrastructure', 1, 89),)),
    Focus('coast_quays', 'Deeper Quays at the District E Port',
          "The naval base and the three yards of District E share one harbour with the coastal freighters, and the quays are "
          "too shallow for loaded tankers at low water. Dredging the channel and lengthening the quays lets oil and steel leave "
          "by sea instead of waiting for space on the two lines inland. The dredgers are hired from abroad, and the works "
          "disturb the yards for a season.",
          ('navy', 'tools'), after=('coast_ledger',), reward=(Build('infrastructure', 1, 91),)),
    Focus('coast_deepen', 'Deeper Plants, Not More of Them',
          "One school says the coastal plants are full but far from efficient. New machine tools, steadier power and trained "
          "foremen would raise output inside the halls that already exist, with no new plots and no new towns. It is the "
          "cheapest path in land and the dearest in imported machinery. It also leaves Districts B, C and F as empty as they are "
          "now, which their governors will not forget.",
          ('tools', 'industry'), after_any=('coast_haul_road', 'coast_quays'), cost=10, exclusive=('coast_spread', 'coast_oil'),
          reward=(SwapIdea('coastal_ledger', 'deep_plants'), Flag('model_deepen'))),
    Focus('coast_spread', 'Halls for the Empty Districts',
          "A second school wants new plants in the three districts that have none: the hills of District B, the plain of "
          "District C and, in time, District F. Land there is cheap and the towns want work. Every new hall needs roads, power "
          "and a workforce that has never stood at a lathe, and the coastal managers warn that skills do not travel by train "
          "as easily as machinery does.",
          ('industry', 'rail'), after_any=('coast_haul_road', 'coast_quays'), cost=10, exclusive=('coast_deepen', 'coast_oil'),
          reward=(SwapIdea('coastal_ledger', 'spread_plants'), Flag('model_spread'))),
    Focus('coast_oil', 'Oil Before Every Other Industry',
          "A third school says Verusa's real asset is the oil spread between the capital, District D and District E, and that "
          "the federation should organise everything around it. A federal oil board would buy the crude, set the price and sell "
          "the surplus abroad. Revenue arrives quickly and gives the government money to spend. Plants that need cheap fuel at "
          "home will have to bargain with the board like anyone else.",
          ('economy', 'logistics'), after_any=('coast_haul_road', 'coast_quays'), cost=10, exclusive=('coast_deepen', 'coast_spread'),
          reward=(SwapIdea('coastal_ledger', 'oil_board'), Flag('model_oil'))),
    Focus('coast_machine_tools', 'Machine Tools for the Coastal Halls',
          "The deepening programme buys machine tools for the plant halls of Districts D and E and sends foremen abroad to learn "
          "how to set them up. Output per worker rises within two years, though the first year brings breakdowns while crews "
          "learn the new machines. The import bill is heavy, and the tools tie the coast to foreign suppliers for parts and "
          "service.",
          ('tools', 'science'), after=('coast_deepen',), requires=(HasFlag('model_deepen'),),
          reward=(Research('industry', 0.5, 2), PP(-15))),
    Focus('coast_b_works', 'A Works Town in the District B Hills',
          "District B lies between the capital and the District E port, on the line that joins them, with hills, jungle and a "
          "coast but no plant at all. Two plant halls beside the line give its towns work and give the railway freight in both "
          "directions. Housing, water and schools must follow the halls, and managers sent from the coast find local hiring "
          "slower than they promised the ministry.",
          ('industry', 'civil'), after=('coast_spread',), requires=(HasFlag('model_spread'),),
          reward=(Build('industrial_complex', 2, 83),)),
    Focus('coast_c_works', 'Arms Shops on the District C Plain',
          "District C is open plain on the line between the capital and District D, and it faces the Yuktobanian frontier. An "
          "arms shop and a plant hall there would put production close to the plain the army might one day have to hold. "
          "Critics call it an odd way to protect a factory. Supporters answer that District C has waited longer than anyone "
          "for anything at all.",
          ('missile', 'industry'), after=('coast_spread',), requires=(HasFlag('model_spread'),),
          reward=(Build('arms_factory', 1, 88), Build('industrial_complex', 1, 88))),
    Focus('coast_wellheads', 'New Wellheads in Three Districts',
          "The oil board pays for new wellheads and gathering lines in the Capital District, District D and District E, where "
          "the federation's crude is split almost evenly. Survey crews map the fields properly for the first time. Drilling in "
          "jungle and on open plain needs different rigs and different crews, and the board must buy both. More crude reaches "
          "the railheads, and the board's income rises with it.",
          ('economy', 'tools'), after=('coast_oil',), requires=(HasFlag('model_oil'),),
          reward=(Research('excavation_tech', 0.5, 2), PP(25))),
    Focus('coast_rolling_mill', 'A Rolling Mill for Coastal Steel',
          "Verusa mines steel in three districts but ships much of it away as billets and buys back finished plate. A rolling "
          "mill attached to the existing coastal works would finish steel at home for rails, hulls and building frames. The "
          "mill needs more power than the coast can easily spare. Once it runs, the yards, the railways and the builders stop "
          "waiting for imported plate.",
          ('industry', 'rebuild'), after_any=('coast_machine_tools', 'coast_b_works', 'coast_c_works', 'coast_wellheads'),
          reward=(Research('construction_tech', 0.5, 1), XP('navy', 5))),
    Focus('coast_bad_year', 'A Fund Against a Bad Oil Year',
          "Oil revenue swings with prices set far away, and a federation that spends every good year's money will be broke in "
          "the first bad one. A reserve fund takes a share of oil and plant taxes in good years and pays out only when prices "
          "fall. Ministers will be tempted to raid it at every budget. If it survives, the next slump lands on savings rather "
          "than on wages.",
          ('scales', 'economy'), after=('coast_rolling_mill',), reward=(Flag('oil_fund'), PP(-25))),
))

RAIL = Branch('rail', 'Every Line Runs Through the Capital', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('rail_hub', 'Three Lines and One Junction',
          "Verusa has three railway lines and every one of them starts in the capital: one to District C and on to District "
          "D, one straight to District E, and one through District B to District E. District F has no railway at all. A "
          "railway office survey asks what the federation would do if the capital junction stopped, and finds that the honest "
          "answer is very little.",
          ('rail', 'logistics'), reward=(Event('rail_junction'),)),
    Focus('rail_f_road', 'A Graded Road for District F',
          "District F borders both Silvonia and Yuktobania, and it is the only district the railway never reached. Its towns "
          "are joined to the capital by tracks that turn to mud after rain. A graded and drained road from the capital across "
          "the District F plain is the cheapest way to tie the district to the rest of the federation, and the first thing its "
          "councils ask for.",
          ('logistics', 'tools'), after=('rail_hub',), reward=(Build('infrastructure', 2, 221),)),
    Focus('rail_b_cuttings', 'Cuttings Through the District B Hills',
          "The line from the capital through District B to the port climbs through hills with tight curves and a gradient that "
          "halves every train's load. Blasting cuttings and easing the curves lets heavier trains run between the capital and "
          "the coast. The work closes the line for weeks at a time, and freight must go round by the direct line to District E "
          "while the crews are blasting.",
          ('rail', 'tools'), after=('rail_hub',), reward=(Build('infrastructure', 1, 83),)),
    Focus('rail_bypass', 'Roads That Bypass the Capital',
          "One answer to the single junction is a road linking the districts directly, so that District C can reach District E "
          "without passing through the capital. Engineers grade and bridge a route from the District C plain across to the "
          "District E hills. It is a road rather than a railway and carries a fraction of the freight, but it keeps the "
          "federation joined if the capital is cut.",
          ('rail', 'security'), after_any=('rail_f_road', 'rail_b_cuttings'), cost=10, exclusive=('rail_coasters',),
          reward=(Build('infrastructure', 1, 88), Build('infrastructure', 1, 91))),
    Focus('rail_coasters', 'Coasters Between District D and District E',
          "The other answer uses the sea. District D and District E both lie on the coast, and a regular service of small "
          "coasters between their harbours would move oil, steel and stores without touching the capital junction. The ships "
          "are cheap to charter and slow to load. The service depends on calm water and on the Maritime Service keeping the "
          "coastal lanes safe, which it has never yet had to do.",
          ('navy', 'logistics'), after_any=('rail_f_road', 'rail_b_cuttings'), cost=10, exclusive=('rail_bypass',),
          reward=(Idea('coaster_link'),)),
    Focus('rail_wagons', 'Wagons from the District E Shops',
          "The federation's twenty-eight trains run on wagons built abroad, and spare axles take months to arrive. The plant "
          "halls of District E could build simple wagons and spares if they had the drawings, the jigs and a test track. The "
          "first wagons are heavy and slow to assemble. Each one built at home is one fewer order waiting on a foreign "
          "supplier's calendar.",
          ('tools', 'rail'), after=('rail_hub',), reward=(Research('train_tech', 0.75, 1),)),
    Focus('rail_ballast', 'Ballast Against the Wet Season',
          "Jungle rain washes ballast from under the sleepers on every coastal line, and the plain lines sink into mud in the "
          "same months. A standing maintenance programme with quarries, ballast trains and gangs posted along each line keeps "
          "the track firm all year. It costs wages every year with nothing new to show for them, which makes it the first item "
          "finance officials want to cut.",
          ('rail', 'rebuild'), after_any=('rail_f_road', 'rail_b_cuttings'), reward=(Idea('ballasted_lines'),)),
    Focus('rail_reserve_trains', 'Trains Held Back in Reserve',
          "The railway office proposes keeping a share of the federation's trains in reserve, serviced and fuelled but out of "
          "daily service, for emergencies and mobilisation. Freight customers lose capacity they are used to and say so "
          "loudly. In return the army can move a formation from the coast to the plain without cancelling the grain trains, and "
          "the reserve can be released in a crisis.",
          ('rail', 'command'), after=('rail_ballast',), reward=(Idea('train_reserve'),)),
    Focus('rail_timetable', 'A Timetable for the Day of Call-Up',
          "With the network mapped and a second route in place, the railway office writes a sealed timetable for the day the "
          "reserve is called up: which trains run, which stations close to civilians, which formation boards where. The army "
          "and the railway argue for a year about whose needs come first. The finished timetable sits in a safe in the capital, "
          "with a second copy at the coast.",
          ('document', 'rail'), after_any=('rail_bypass', 'rail_coasters'), reward=(Flag('war_timetable'), PP(10))),
))

ARMY = Branch('army', 'Seven Formations in Reserve', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('army_muster', 'Muster of the Seven Formations',
          "Verusa's army is seven infantry formations of six battalions each, every one with an engineer company: three at the "
          "capital, two at the District D logistics centre and two at the District E logistics centre. District B, District C "
          "and District F, which between them hold most of both frontiers, have no garrison at all. A full muster shows the "
          "federation what its army is, and where it is not.",
          ('training', 'command'), reward=(Event('seven_formations'), XP('army', 10))),
    Focus('army_mountain_school', 'A School for the Coastal Mountains',
          "The army already trains a few companies for mountain work, a habit learned in the hill and mountain country behind "
          "the coast. A permanent school in District D would teach climbing, rope bridges and supply by pack animal to a "
          "battalion from every formation in turn. Instructors are scarce and the courses are long. The school gives the "
          "coastal formations ground that few attackers would choose.",
          ('training', 'tools'), after=('army_muster',), reward=(Idea('mountain_school'),)),
    Focus('army_lorries', 'Counting the Army Lorries',
          "The depots list nine hundred and sixty sets of motor equipment, and nobody is sure how many of the lorries behind "
          "those figures actually start. A count by mechanics rather than clerks finds out, repairs what can be repaired and "
          "writes off the rest. The result decides whether the federation could ever move its reserve on wheels, or must keep "
          "marching it from the trains.",
          ('logistics', 'tools'), after=('army_muster',), reward=(Flag('lorries_counted'), Research('engineers_tech', 0.5, 1))),
    Focus('army_forward', 'Hold the Plain at the Frontier',
          "The forward doctrine says the capital is the federation and must be held on the plain itself. The formations would "
          "train to defend the open ground beside both frontiers, with prepared positions, ranges and the superior firepower "
          "that the army's manuals already favour. It suits a country that cannot afford to lose its capital, and it asks "
          "infantry to stand where tanks and aircraft move most freely.",
          ('security', 'gate'), after_any=('army_mountain_school', 'army_lorries'), cost=10, exclusive=('army_depth', 'army_wheels'),
          reward=(Idea('plain_defence'), Flag('doctrine_forward'))),
    Focus('army_depth', 'Fall Back Into the Jungle Hills',
          "The depth doctrine says the plain cannot be held against a serious attack and should not be tried. The formations "
          "would delay on the plain, then fall back into the jungle hills and mountains of Districts D and E, where the plants, "
          "the port and the depots are. The doctrine is honest about the terrain and brutal about the capital, which it treats "
          "as ground to give up and retake.",
          ('command', 'shelter'), after_any=('army_mountain_school', 'army_lorries'), cost=10, exclusive=('army_forward', 'army_wheels'),
          reward=(Idea('depth_defence'), Flag('doctrine_depth'))),
    Focus('army_wheels', 'Put the Reserve on Lorries',
          "The mobile doctrine keeps most formations in the coastal depots and moves them by lorry and train to wherever the "
          "threat appears, on either frontier or on the coast. It needs working lorries, fuel and a staff that can plan "
          "movement fast. It promises one reserve able to do several jobs, and risks a reserve that arrives late, tired and "
          "short of fuel.",
          ('logistics', 'command'), after_any=('army_mountain_school', 'army_lorries'), cost=10, exclusive=('army_forward', 'army_depth'),
          requires=(HasFlag('lorries_counted'),), reward=(Idea('wheeled_reserve'), Flag('doctrine_mobile'))),
    Focus('army_ranges', 'Firing Ranges on the Open Plain',
          "Defending the plain needs gunners who can hit targets at long range across open ground. Ranges on the capital plain "
          "let the formations practise with artillery and machine guns at the distances they would actually fight. Farmers lose "
          "grazing to the ranges and complain about the noise. The army gains gun crews who fire more than a handful of rounds "
          "a year.",
          ('training', 'security'), after=('army_forward',), requires=(HasFlag('doctrine_forward'),),
          reward=(Research('artillery', 0.5, 1), XP('army', 15))),
    Focus('army_hill_depots', 'Depots in the District D Hills',
          "The depth doctrine moves ammunition, fuel and rations out of the capital into depots dug into the hills of District "
          "D, along roads the engineers must build first. The capital's quartermasters lose their stores and their influence. "
          "The formations gain stocks that could survive the loss of the plain and keep a long defence of the coast supplied "
          "for months.",
          ('shelter', 'logistics'), after=('army_depth',), requires=(HasFlag('doctrine_depth'),),
          reward=(Build('infrastructure', 1, 89),)),
    Focus('army_motor_pools', 'Motor Pools at the Logistics Centres',
          "The mobile doctrine needs lorries kept running at the two coastal logistics centres, with mechanics, fuel stores and "
          "a stock of spare parts. Each formation gets a driving school and a fixed allotment of vehicles. The fuel bill climbs, "
          "and whoever sells the crude wants paying. The reserve can now move a formation from the coast to a frontier in days "
          "rather than weeks.",
          ('logistics', 'tools'), after=('army_wheels',), requires=(HasFlag('doctrine_mobile'),),
          reward=(Research('logistics_tech', 0.5, 1), XP('army', 10))),
    Focus('army_roll', 'A Roll of Former Conscripts',
          "Every Verusan who has served is listed by district, trade and last unit on a single roll kept at the district "
          "offices and copied to the capital. Mobilisation that now relies on posters and word of mouth could rely on letters "
          "and lists. The roll needs clerks and a yearly update, and many former soldiers are uneasy about a state that knows "
          "where each of them lives.",
          ('document', 'security'), after=('army_muster',), reward=(Idea('reserve_roll'),)),
    Focus('army_timetable_callup', 'Call-Up by Railway Timetable',
          "The railway office's sealed timetable and the army's roll are joined: each reservist's letter names the train, the "
          "station and the hour. Night rehearsals on one line at a time test the plan without stopping the federation, and the "
          "mistakes are found and fixed in the dark. When the timetable works, a reserve that took a month to gather can be in "
          "its depots inside a week.",
          ('rail', 'security'), after=('army_roll',), requires=(HasFlag('war_timetable'),),
          reward=(SwapIdea('reserve_roll', 'timetabled_reserve'),)),
    Focus('army_federal_staff', 'A Staff for All Six Districts',
          "Whichever doctrine the army chose, it needs a staff that plans for all six districts and not just the capital "
          "garrison. A federal staff with officers from every formation writes the plans, runs the exercises and reports to the "
          "government. Officers who have only served in the capital resent the newcomers. The army gains one set of plans in "
          "place of seven separate habits.",
          ('command', 'document'), after_any=('army_ranges', 'army_hill_depots', 'army_motor_pools'),
          reward=(XP('army', 20), Research('land_doctrine', 0.5, 1))),
))

SEA = Branch('sea', 'Four Hulls at the District E Base', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('sea_four_hulls', 'Three Escorts and a Submarine',
          "The Maritime Service owns three coastal escorts and one coastal submarine, all based at the District E harbour, and "
          "the federation's sixty coastal freighters depend on them. The coast from District B to District D is long, and the "
          "service has never patrolled more than a fraction of it. An inspection of hulls, crews and stores tells the "
          "government what four ships can really do.",
          ('navy', 'submarine'), reward=(Event('four_hulls'), XP('navy', 10))),
    Focus('sea_cinigrad', 'Word of New Submarines from Cinigrad',
          "In September 1991 the Scinfaxi class of submarines is announced at a political convention in Cinigrad, in "
          "Yuktobania. Verusa shares a long land frontier with Yuktobania and owns one submarine and three escorts. Nobody in "
          "the Maritime Service can say what the new boats mean for a small coastal navy, so the staff asks for a proper study "
          "before the newspapers answer the question for it.",
          ('submarine', 'security'), after=('sea_four_hulls',), requires=(After('1991.9.2'),),
          reward=(Research('naval_equipment', 0.5, 1), Flag('submarine_study'))),
    Focus('sea_listening', 'Listening Huts and Shore Radar',
          "One answer watches the water rather than chasing it. Shore radar and listening huts along the District E coast "
          "report every contact near the harbour approaches, and the escorts sail only when there is something to find. The "
          "equipment is imported and the crews take a year to train. The coast becomes harder to approach unseen, though the "
          "service still has only three escorts to answer a report.",
          ('submarine', 'radar'), after=('sea_cinigrad',), cost=10, exclusive=('sea_freighter_pool',),
          requires=(HasFlag('submarine_study'),), reward=(Build('radar_station', 1, 91), Idea('hydrophone_watch'))),
    Focus('sea_freighter_pool', 'One Schedule for Sixty Freighters',
          "The other answer protects trade instead of hunting anything. The sixty coastal freighters are pooled under one "
          "federal schedule and sail in groups along routes the escorts can actually cover. Owners lose the freedom to sail "
          "when it suits them and gain cover the federation underwrites. Cargoes arrive more slowly and more predictably, and "
          "the escorts finally have a job they can do.",
          ('navy', 'economy'), after=('sea_cinigrad',), cost=10, exclusive=('sea_listening',),
          requires=(HasFlag('submarine_study'),), reward=(Idea('freighter_pool'),)),
    Focus('sea_b_slipway', 'A Slipway on the District B Coast',
          "All three of the federation's yards sit in District E beside the naval base, so a single bad night could stop every "
          "repair at once. A slipway on the District B coast, on the railway to the capital, would give the service a second "
          "place to repair and build small hulls. The site needs a breakwater, and skilled hands that District B does not yet "
          "have.",
          ('tools', 'navy'), after=('sea_four_hulls',), reward=(Build('dockyard', 1, 83),)),
    Focus('sea_apprentices', 'Apprentices for the Yards',
          "The District E yards hire welders and fitters trained abroad or by the old hands, and the old hands are retiring. An "
          "apprentice school shared by the District E yards and the new District B slipway trains a class every year in hull "
          "work, engines and electrics. The first classes slow the yards down. Later ones mean the service no longer waits for "
          "foreign contractors.",
          ('tools', 'training'), after=('sea_b_slipway',), reward=(Idea('yard_apprentices'),)),
    Focus('sea_fisheries', 'Fishery Patrols from the Naval Base',
          "Fishing boats from the coastal towns work far out along the coast, where the Maritime Service is rarely seen. "
          "Regular fishery patrols by the escorts enforce the federation's own catch rules, help boats in trouble and give the "
          "crews long days at sea. Fuel and wear cost money. The coast starts to see its navy as something more than a harbour "
          "ornament.",
          ('fishing', 'navy'), after=('sea_four_hulls',), reward=(Idea('fishery_patrol'),)),
    Focus('sea_reserve_crews', 'Reserve Crews for Laid-Up Hulls',
          "The service keeps the names of former sailors, merchant officers and yard workers who could crew requisitioned "
          "freighters or a fourth warship in an emergency. Each spends two weeks a year at sea with the escorts. The scheme "
          "costs training time and berths. In a crisis the Maritime Service would have people who know its ships instead of a "
          "list of strangers.",
          ('document', 'navy'), after_any=('sea_listening', 'sea_freighter_pool'), reward=(XP('navy', 20),)),
    Focus('sea_coast_charts', 'New Charts of the Jungle Coast',
          "The coast between District B and District D is charted from surveys old enough that the sandbanks have moved since. "
          "A survey ship working with the fishery patrols re-charts the approaches, river mouths and anchorages. The work is "
          "slow and unglamorous. The freighters stop running aground, and the escorts learn every inlet they might one day "
          "need.",
          ('document', 'fishing'), after=('sea_fisheries',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
))

AIR = Branch('air', 'One Air Base Beside the Frontier', 1991, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_one_base', 'Seventy-Two Aircraft on One Field',
          "Every combat aircraft Verusa owns, sixty fighters and twelve support aircraft, sits on the single air base in the "
          "Capital District, within easy reach of the Silvonian frontier. The base shares the capital's fuel silo and its "
          "railway junction. Pilots like the convenience. The air staff knows that one runway beside a frontier is one target, "
          "and asks for money to spread out.",
          ('air', 'runway'), reward=(Event('frontier_field'), XP('air', 10))),
    Focus('air_e_field', 'A Field Behind the District E Hills',
          "District E, behind jungle hills and far from both frontiers, has room for a second air base near the port. Runways, "
          "hangars and fuel tanks there would keep aircraft out of reach of a surprise blow against the capital. Building on "
          "jungle ground needs heavy drainage, and from now on the air staff must split its maintenance crews between two "
          "fields.",
          ('runway', 'air'), after=('air_one_base',), reward=(Build('air_base', 2, 91),)),
    Focus('air_d_strip', 'A Jungle Strip in District D',
          "A smaller strip near the District D logistics centre covers the eastern coast and the stretch of the Yuktobanian "
          "frontier that runs into the jungle. It takes only a handful of aircraft at a time and needs constant work to keep "
          "the jungle back. The strip gives the support aircraft a field near the formations that would fight in the hills.",
          ('runway', 'tools'), after=('air_one_base',), reward=(Build('air_base', 1, 89),)),
    Focus('air_capital_sky', 'Interceptors Over the Junction',
          "One policy gives the air arm a single job: keep hostile aircraft away from the capital, its junction and its plants. "
          "Pilots train for interception, and the support aircraft are kept as a small reserve. It suits a federation whose "
          "most valuable ground sits on an open plain beside a frontier, and it leaves the army to fight on the ground with "
          "little help from above.",
          ('air', 'security'), after_any=('air_e_field', 'air_d_strip'), cost=10, exclusive=('air_formation_wings',),
          reward=(Idea('capital_sky'),)),
    Focus('air_formation_wings', 'Aircraft for the Seven Formations',
          "The other policy ties the air arm to the army. Fighters escort the support aircraft, and both train with the "
          "formations in reconnaissance, ground attack and supply drops over the hills and the plain. Pilots spend more time "
          "with soldiers than with each other. The capital's sky would be less well guarded, and the army would never have to "
          "fight alone.",
          ('air', 'training'), after_any=('air_e_field', 'air_d_strip'), cost=10, exclusive=('air_capital_sky',),
          reward=(Idea('formation_wings'),)),
    Focus('air_spares', 'Spares from Verusan Aluminium',
          "Verusa mines aluminium in the Capital District and both coastal districts, yet every airframe part comes from "
          "abroad. A small shop in the capital's plant halls making panels, brackets and simple fittings would keep more "
          "aircraft flying between deliveries. The parts are crude at first and the inspectors reject many of them. Each one "
          "accepted is a part nobody had to wait for.",
          ('industry', 'air'), after=('air_one_base',), reward=(Flag('airframe_spares'), Research('industry', 0.5, 1))),
    Focus('air_reserve_aircraft', 'Nineteen Aircraft in Storage',
          "Fifteen fighters and four support aircraft wait in storage as a reserve, and some of them have not flown in years. "
          "With home-made spares to hand, the air arm overhauls the reserve and puts a rotating share of it back into service "
          "for training. The reserve stops being a line in a ledger and becomes aircraft that can fly in the week they are "
          "needed.",
          ('air', 'document'), after=('air_spares',), requires=(HasFlag('airframe_spares'),), reward=(XP('air', 25),)),
    Focus('air_radar_north', 'Radar Over the District C Plain',
          "The plain of District C faces the Yuktobanian frontier and lies across the northern approach to the capital. A radar "
          "station there would give the air arm warning of aircraft crossing the plain, and give the formations an eye they "
          "have never had. The station watches Verusan sky and the air over the line, and claims nothing on the ground beyond "
          "it.",
          ('radar', 'air'), after_any=('air_capital_sky', 'air_formation_wings'), reward=(Build('radar_station', 1, 88),)),
    Focus('air_school', 'A Flying School Far from the Frontier',
          "Training pilots on a frontier field means every student flight is an incident waiting to happen. A flying school at "
          "the new District E field moves the students to quieter sky over the coast, with instructors drawn from both fighter "
          "and support squadrons. The capital field loses some of its best pilots to teaching. The air arm gains a steady "
          "supply of pilots who learned without an audience.",
          ('training', 'air'), after=('air_e_field',), reward=(Idea('coastal_flying_school'),)),
))

NEIGHBOURS = Branch('nb', 'The Silvonian Road and the Northern Line', 1991, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('nb_survey', 'Surveyors on Both Frontiers',
          "Silvonia meets Verusa along the Capital District, District B and District F, and Yuktobania along Districts C, D "
          "and F; District F alone touches both. Neither frontier has a modern survey on the Verusan side. Teams sent along "
          "each line will report what crosses it, where the posts stand and what the frontier towns want, before the "
          "government decides which line gets its attention first.",
          ('document', 'diplomacy'), reward=(Event('two_frontiers'),)),
    Focus('nb_west_first', 'The Silvonian Frontier Comes First',
          "The western frontier with Silvonia runs beside the capital itself, and its open plain carries farm traffic, traders "
          "and smugglers every day. Putting it first means customs posts, roads and market rules on the Verusan side, so that "
          "trade with Silvonia's farming districts flows legally and visibly. The northern line waits, and the rallies in "
          "District C and District F ask why their frontier always comes second.",
          ('diplomacy', 'civil'), after=('nb_survey',), cost=10, exclusive=('nb_north_first',),
          reward=(Idea('silvonian_road'), Flag('west_first'))),
    Focus('nb_north_first', 'The Northern Line Comes First',
          "The northern frontier with Yuktobania is longer, runs through three districts and faces a neighbour many times "
          "Verusa's size. Putting it first means survey markers, patrols and watch posts on the Verusan side, with the money "
          "taken from the western roads. Yuktobania is asked for nothing and nothing is claimed. The capital's traders grumble "
          "that the west, where the money is made, has been left for later.",
          ('security', 'gate'), after=('nb_survey',), cost=10, exclusive=('nb_west_first',),
          reward=(Idea('northern_watch'), Flag('north_first'))),
    Focus('nb_customs_sheds', 'Customs Sheds at the Capital Crossing',
          "The busiest crossing into Silvonia leaves the capital across the western plain, where lorries, carts and herds "
          "queue at a single hut. Proper customs sheds with a weighbridge, a paved yard and a rest house clear the traffic in "
          "hours. Silvonia's own arrangements are its own affair. On the Verusan side the queue shortens, and the treasury "
          "starts collecting duties it used to lose.",
          ('economy', 'logistics'), after=('nb_west_first',), requires=(HasFlag('west_first'),),
          reward=(Build('infrastructure', 1, 0),)),
    Focus('nb_market_days', 'Market Days in the Frontier Towns',
          "Frontier towns in the Capital District and District B hold licensed market days twice a month, open to traders from "
          "either side who register at the customs sheds. Prices settle, smuggling loses its point, and the towns gain a "
          "reason to look towards the frontier rather than fear it. Officials must police the markets, and the nationalist "
          "papers complain about foreign stalls.",
          ('civil', 'economy'), after=('nb_customs_sheds',), reward=(TimedIdea('frontier_markets', 730),)),
    Focus('nb_markers', 'Marker Stones on the Northern Line',
          "Survey teams set numbered marker stones along the Verusan side of the northern frontier, across the plains of "
          "District C and District F and into the jungle of District D. Each stone is recorded and photographed, and the "
          "register is kept in the capital. The stones claim no new ground. They let a patrol report exactly where it was, "
          "which until now was impossible.",
          ('document', 'gate'), after=('nb_north_first',), requires=(HasFlag('north_first'),),
          reward=(Flag('line_marked'), Stability(0.02))),
    Focus('nb_plain_patrols', 'Mounted Patrols on the Northern Plain',
          "With the line marked, mounted and motor patrols ride the open plains of District C and District F on fixed routes "
          "between the stones. They report herds, smugglers, lost travellers and anything else that crosses. The patrols are "
          "thin on a long frontier and live hard in the dry months. The government learns for the first time what actually "
          "happens along its northern line.",
          ('security', 'logistics'), after=('nb_markers',), requires=(HasFlag('line_marked'),),
          reward=(Idea('plain_patrols'),)),
    Focus('nb_herders', 'Passes for the District F Herders',
          "Herders from the District F plain have always taken their animals across the desert frontier with Silvonia as the "
          "seasons turn, as herders from the other side have done in reverse. A seasonal pass from the district office records "
          "who crosses and when, without asking anyone to stop. It costs clerks at a few remote posts, and turns a habit the "
          "law ignored into one it recognises.",
          ('peace', 'document'), after=('nb_survey',), reward=(Idea('herder_passes'),)),
    Focus('nb_osean_envoys', 'Osean Envoys Call More Often',
          "As the century draws to its close, Osean diplomats appear in the capital more often, asking about the frontiers, "
          "the oil and the neighbours; in Sapin, officials already worry aloud that Osea is turning towards Yuktobania and "
          "Verusa. The federation promises nothing and joins nothing. A federation that is visited can ask for things, though, "
          "and the foreign ministry begins to keep a list.",
          ('diplomacy', 'communications'), after_any=('nb_market_days', 'nb_plain_patrols'), requires=(After('1997.1.1'),),
          reward=(Idea('osean_attention'), Tooltip('No alliance, faction or treaty changes; the envoys only visit.'))),
    Focus('nb_arkbird', 'Osea and Yuktobania Share the Arkbird',
          "In October 1999 Osea and Yuktobania agree to convert the Arkbird into a platform for clearing debris from satellite "
          "orbits. For a federation wedged between a giant neighbour and a distant superpower, cooperation between the two is "
          "worth noting. The foreign ministry recommends easing the watch on the northern line a little and spending the "
          "savings at home, while every post stays manned.",
          ('satellite', 'peace'), after=('nb_survey',), requires=(After('1999.10.8'),),
          reward=(TimedIdea('quiet_north', 730),)),
))

SKY = Branch('sky', 'Ulysses Over the Open Plain', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_warning', 'Ulysses Enters the Federal Budget',
          "Late in 1994 the astronomers give the asteroid a name, Ulysses, and a warning: its path brings it near the Earth, "
          "and it might hit. Verusa owns no observatory worth the word and no civil defence service at all. The cabinet opens a "
          "small budget line for watching the sky and planning for the worst, and asks every ministry to list what it would "
          "need if the worst began to look likely.",
          ('telescope', 'meteor'), requires=(After('1994.12.10'),), reward=(Idea('sky_watch_office'),)),
    Focus('sky_peaks', 'Observers on the Coastal Peaks',
          "The mountains of District D and District E have the clearest night sky in the federation. Observer posts on a few "
          "peaks, with telescopes, radios and trained volunteers, would watch for anything bright, fast or falling and report "
          "it to the capital. They will mostly report meteors, aircraft and weather. The posts also give the air arm a warning "
          "line it never had.",
          ('telescope', 'radar'), after=('sky_warning',), reward=(Idea('peak_observers'),)),
    Focus('sky_announced', 'The Impact Is Certain',
          "In April 1996 the President of the FCU announces that Ulysses will strike the Earth, and nobody can yet say where "
          "the fragments will fall. Verusa's capital sits on open plain with nothing to dig into, while its coast has hills, "
          "mountains and old workings. The government must decide quickly where its people will go if fragments are ever "
          "forecast for the federation.",
          ('meteor', 'communications'), after=('sky_warning',), requires=(After('1996.4.20'),),
          reward=(Event('impact_announced'), TimedIdea('impact_nerves', 540))),
    Focus('sky_dig', 'Dig Shelters Under the Plain',
          "One plan keeps people at home. Shelters dug under the capital and the plain towns, lined with concrete and stocked "
          "with water, would hold the population where it lives and works. The plain has no rock to cut into, so every shelter "
          "must be built from nothing. It is the dearest plan and the least disruptive, and it keeps the capital working through "
          "whatever comes.",
          ('shelter', 'civil'), after=('sky_announced',), cost=10, exclusive=('sky_hills',), reward=(Idea('plain_shelters'),)),
    Focus('sky_hills', 'Evacuate to the Coastal Hills',
          "The other plan moves people. Timetables, camps and requisitioned buildings in the hills of District D and District E "
          "would take the plain towns' population by rail to ground with natural cover. It is cheaper than digging and far more "
          "disruptive, and it depends entirely on three railway lines that all begin in the capital. The coast will have to "
          "house a great many guests.",
          ('shelter', 'rail'), after=('sky_announced',), cost=10, exclusive=('sky_dig',), reward=(Idea('hill_evacuation'),)),
    Focus('sky_stocks', 'Water and Lamp Oil in Every District',
          "Each district office keeps drinking water, lamp oil, medical kits and tinned food for a fortnight, sealed and "
          "checked every quarter. The stocks cost money every year and spoil if nobody rotates them. They also mean that a "
          "district cut off by fragments, flooding or panic can look after itself for two weeks before help arrives from the "
          "capital.",
          ('logistics', 'shelter'), after=('sky_announced',), reward=(Idea('district_stocks'),)),
    Focus('sky_drill', 'A Night Drill for the Whole Federation',
          "With the capital plan in print and a shelter plan chosen, the federation holds one night drill in every district at "
          "once. Sirens sound, trains run to the emergency timetable, wardens count heads and the districts report by radio. "
          "Much goes wrong, and all of it is written down. The public learns that the plan exists outside the ministries, and "
          "some of the fear goes out of the waiting.",
          ('security', 'shelter'), after_any=('sky_dig', 'sky_hills'), requires=(HasFlag('capital_plan_printed'),),
          reward=(RemoveIdea('impact_nerves'), Stability(0.02))),
    Focus('sky_roche', 'Every Post Awake on 8 July',
          "On 8 July 1999 Ulysses passes through the Roche limit and begins to break apart. Every observer post, radar crew and "
          "district warden in Verusa is on duty through the night, and the radio carries reports from the peaks until dawn. "
          "What falls, and where, is the question the whole world is asking, and the federation can only watch its own sky.",
          ('meteor', 'telescope'), after=('sky_announced',), requires=(After('1999.7.8'),), reward=(Event('roche_night'),)),
    Focus('sky_after', 'Accounting for the Long Night',
          "After the night of the Roche limit the district offices report everything their wardens and observers saw, and the "
          "sky watch office sorts fact from rumour. The reports show which plans worked and which existed only on paper. The "
          "office recommends keeping the observer posts and the district stocks for good, at a cost the finance ministry would "
          "rather not carry, and the cabinet agrees.",
          ('document', 'telescope'), after=('sky_roche',), reward=(SwapIdea('sky_watch_office', 'permanent_watch'),)),
))

FAR = Branch('far', 'Distant Wars and the Price of Oil', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('far_belka', 'War Prices Reach the Coast',
          "On 25 March 1995 war breaks out around Belka, a world away from the Verusan coast. Within weeks tanker charters "
          "climb, insurers add war clauses to every cargo, and buyers abroad ask Verusan producers for every barrel the "
          "federation can spare. A war Verusa has no part in has made its crude worth more, and the government must decide what "
          "to do about it.",
          ('economy', 'communications'), requires=(After('1995.3.25'),), reward=(Event('belkan_prices'),)),
    Focus('far_sell', 'Sell the Crude at War Prices',
          "One course sells every barrel buyers will take while the war lasts, at prices the federation has never seen. The "
          "revenue would pay for roads, plants and the air arm's spares. Fuel at home gets dearer, and the coast's own plants "
          "complain. The federation also learns how much of its budget can come to depend on a war that ends whenever other "
          "people decide.",
          ('economy', 'navy'), after=('far_belka',), cost=10, exclusive=('far_hold',),
          reward=(TimedIdea('war_premium', 540), Flag('sold_dear'))),
    Focus('far_hold', 'Keep the Crude for Verusa',
          "The other course caps exports and fills the tanks at home: the capital's fuel silo, the naval base and the depots. "
          "Producers lose the windfall and say so. The federation gains a fuel reserve that would carry it through a blockade "
          "or a slump, and keeps fuel cheap for its own plants and railways while the rest of the world pays war prices.",
          ('logistics', 'shelter'), after=('far_belka',), cost=10, exclusive=('far_sell',),
          reward=(Idea('crude_reserve'), Flag('kept_crude'))),
    Focus('far_lumen', 'After the Treaty of Lumen',
          "On 20 June 1995 a treaty signed in Lumen ends the Belkan War. War clauses lapse, charters fall and the buyers drift "
          "back to their usual suppliers. The federation's windfall, or its reserve, now has to be explained to the public. "
          "The government reviews what the war taught it about a coast that sells oil into a world it cannot influence.",
          ('peace', 'document'), after_any=('far_sell', 'far_hold'), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('war_premium'), Stability(0.02))),
    Focus('far_buyers_stay', 'Buyers Who Came Back',
          "Some of the buyers who found Verusan crude during the war keep buying after it, at ordinary prices but on long "
          "contracts. The coastal producers gain steady customers and the federation gains income it can plan around. The "
          "contracts bind Verusa to deliver even in years when it might rather keep the oil, and the buyers know it.",
          ('diplomacy', 'economy'), after=('far_lumen',), requires=(HasFlag('sold_dear'),), reward=(Idea('standing_buyers'),)),
    Focus('far_reserve_rule', 'A Standing Rule for the Fuel Reserve',
          "Having filled its tanks once, the federation writes a rule: a fixed share of production goes into the reserve every "
          "year and leaves it only by cabinet order. The rule costs producers part of every good year. It also means the next "
          "war abroad, or the next slump, finds the railways and garrisons fuelled for months without any new buying.",
          ('scales', 'logistics'), after=('far_lumen',), requires=(HasFlag('kept_crude'),),
          reward=(Research('synth_resources', 0.5, 1), Stability(0.02))),
    Focus('far_stonehenge', 'Railgun News from San Salvacion',
          "In the summer of 2003 Erusea invades neutral San Salvacion, seizes Stonehenge and turns its railguns against "
          "aircraft. The war is in Usea, a world away, but the shipping lanes, insurers and fuel buyers that set Verusa's oil "
          "price are the same ones. The air staff reads the reports with alarm, and the oil producers read them with interest.",
          ('missile', 'air'), after=('far_lumen',), requires=(HasGlobal('ac_ucw_stonehenge_seized'),),
          reward=(Event('usean_war'),)),
    Focus('far_home_insurance', 'Insure Verusan Cargoes at Home',
          "When the FCU establishes the ISAF and the Usean war widens, foreign insurers raise rates on cargoes in every sea "
          "lane they consider risky, and Verusa's are among them. A federal insurance pool for Verusan freighters and tankers, "
          "backed by the treasury, keeps the coastal trade moving at rates owners can pay. The treasury carries the risk and "
          "hopes the Usean war stays far away.",
          ('scales', 'navy'), after=('far_stonehenge',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Idea('home_insurance'),)),
    Focus('far_slump', 'When War Prices Fall Again',
          "Whenever the Usean war ends, the prices it pushed up will fall, and the wells and plants that hired on the strength "
          "of them will feel it first. The reserve fund set aside in good years now pays wages while prices settle. Drawing on "
          "it is exactly what it was for, and the finance ministry still hates every withdrawal. The coast gets through the "
          "fall without lay-offs.",
          ('economy', 'scales'), after=('far_home_insurance',), requires=(HasFlag('oil_fund'),),
          reward=(Stability(0.03), PP(30))),
))

BRANCHES = (FEDERATION, PLAIN, COAST, RAIL, ARMY, SEA, AIR, NEIGHBOURS, SKY, FAR)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('formation_callout', 'Call Out One Formation',
                'One formation is called out by letter from the roll and moved by rail to a frontier district for a fortnight. '
                'Repeatable once a year; the call-out costs wages and fuel.',
                30, (XP('army', 15), WarSupport(0.01)), requires=(Completed('army_roll'),), cooldown=365),
    DecisionDef('frontier_fair', 'Hold a Frontier Fair',
                'The western frontier towns hold a fair with licensed stalls from both sides of the line. Repeatable once a year.',
                25, (Stability(0.02),), requires=(Completed('nb_market_days'),), cooldown=365),
    DecisionDef('open_granaries', 'Open the Federal Granaries',
                'The capital granaries sell their stores below market price to calm a hungry or frightened city. Once only; the '
                'stores are gone afterwards.',
                20, (Stability(0.05), RemoveIdea('ninety_day_stores')), requires=(Completed('plain_granaries'),)),
    DecisionDef('d_strip_aprons', 'Concrete Aprons for the District D Strip',
                'Concrete aprons and sealed fuel stores let the District D strip hold more aircraft through the wet season. A '
                'one-time works programme.',
                60, (Build('air_base', 1, 89),), requires=(Completed('air_d_strip'),)),
    DecisionDef('coastal_patrol_week', 'A Week of Coastal Patrols',
                'All four hulls sail together along the coast from District B to District D. Repeatable every six months; it '
                'burns fuel the service would rather keep.',
                20, (XP('navy', 10),), requires=(Completed('sea_four_hulls'),), cooldown=180),
    DecisionDef('relay_b_line', 'Relay the District B Hill Line',
                'Work trains relay the hill section of the District B line with heavier rail and new drains. Once only.',
                50, (Build('infrastructure', 1, 83),), requires=(Completed('rail_b_cuttings'),)),
)
