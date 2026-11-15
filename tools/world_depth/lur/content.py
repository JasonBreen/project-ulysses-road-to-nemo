"""Luremia (LUR): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party
with elections suspended and popularity split 50 to 48 between democratic and
neutrality), the unnamed National Administration office, the two 1991 states with
their existing captions Olastetten, Qesi and Knadorf, the map (terrain, railways,
weather, neighbours) and the global flag the Usean war script already sets.
Official: ACES Chronicle rows used only as date anchors for distant pressures, each
cited by its exact key. Everything else, including every Luremian choice, office,
idea, building, decision and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='LUR', name='Luremia', root='world', package='lur',
                  themes=('shelter', 'rail', 'ballot'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 politics: ruling_party democratic with elections_allowed = no and election_frequency 48; '
           'popularities democratic 50, neutrality 48, fascism 1, communism 1; stability and war support 0.5; three research '
           'slots; tech_mountaineers and early_fighter among the starting technologies. The starting leader is the unnamed '
           'National Administration office (LUR_ac_government_office, centrism), whose 1991 holder has not been established. '
           'The tree never names a holder.',
           'mod/2985041246/history/countries/LUR - Luremia.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Luremian Republic (democratic and neutrality), Luremian Commune (communism), Luremian Free '
           'State (fascism), Grand Duchy of Luremia (monarchism); adjective Luremian. All three political answers in this tree '
           'keep the Republic names; no commune, free state or grand duchy path is offered.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: two 1991 states, both category town with four shared slots and every slot filled. State 226 (capital, '
           'captioned Olastetten): 2 civilian and 2 arms plants, infrastructure 3, air base 1, provinces 218 (hills, victory '
           'point Knadorf, value 20), 824 (mountain), 1005 (hills), 1301 (mountain) and 5053 (hills); supply nodes on 218 and '
           '824; oil 2, rubber 2, steel 3. State 231 (captioned Qesi): 3 civilian and 1 arms plant, infrastructure 3, no air '
           'base, desert provinces 556 and 5620, supply node on 556; oil 2, rubber 1, steel 3. No province is coastal. Level-2 '
           'railways 218-824 and 218-1005-556. Strategic region 275 holds every Luremian province, with temperatures of 20 to '
           '35 degrees in every month, heavy rain on 40 to 50 percent of days and full mud. Land neighbours computed from '
           'map/provinces.bmp: KLG (states 73 and 138) along 218, 824, 1301 and 5053; GLA (52 and 576) along 556, 1005 and '
           '5053; SFA (189) along 556 and 5620; ESN (484 and 583) along 1301 and 5620. The placeholder captions on provinces '
           '824 and 556 are not used as place names, and no other place is named.',
           'mod/2985041246/history/states/226-State_226.txt; mod/2985041246/history/states/231-State_231.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/definition.csv; mod/2985041246/map/strategicregions/275-XXX.txt; tools/regional_labels/labels.json'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role landlocked civil defense; 5 civilian, 3 military and 0 naval '
           'factories; three infantry formations of four battalions in all, with combat aviation and combat navy '
           'deliberately absent; stocks of 800 infantry equipment, 640 motorized equipment and 24 trains; 60 convoys; oil '
           'base 4; research priority Physical Sustainment. Fiscal figures (GDP 108, debt ratio 0.3, collection 0.85, growth '
           '3, inflation 2) are fictional calibration, not canon national accounts.',
           'tools/world_starts/profiles.json; docs/WORLD_STARTS_CALIBRATION.md; tools/world_foundation/country_registry.json; '
           'tools/economy_v2/profiles.json; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Mod provenance',
           'Neighbour context only: all four neighbours start 1991 with a democratic ruling party and elections_allowed = no. '
           'Kaluga has democratic popularity 61; Sfaenland, Silvonia and Glaceland have fascism at 50 percent popularity. The Glaceland tree describes herders and foresters from its Districts F and J crossing into Luremia '
           'along old valley paths; this tree only registers the Luremian side of those crossings and asserts no neighbour '
           'response to any Luremian policy.',
           'mod/2985041246/history/countries/KLG - Kaluga.txt; mod/2985041246/history/countries/SFA - Sfaenland.txt; '
           'mod/2985041246/history/countries/ESN - Silvonia.txt; mod/2985041246/history/countries/GLA - Glaceland.txt; '
           'tools/world_depth/gla/content.py'),
    Source('Official', 'Date anchor: the International Astronomical Union announces that Ulysses may strike the Earth. Gate '
           'of the sky bulletin focus; no Luremian role is claimed.', '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Gate of the distant-war branch; Luremia takes no part.',
           '1995 / 03.25'),
    Source('Official', 'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Gate of the treaty focus.',
           '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will impact the Earth. Gate of the announcement focus; '
           'where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit of the Earth. Gate of the Roche night focus; no '
           'damage in Luremia is claimed.', '1999 / 07.08'),
    Source('Official', 'Date anchor: the ISAF is established against Erusea. Background to the freight focus, which also waits '
           'for the mod global flag ac_ucw_isaf_formed; no Luremian part in the war is claimed.', '2003 / 08.22'),
    Source('Official', 'Date anchor: Erusea surrenders and the Continental War ends. Gate of the closing freight focus.',
           '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: ac_ucw_isaf_formed (Usean Continental War script) and belka_lost_belkan_war '
           '(Belkan War events). Each reaction is a leaf or late focus, so no outcome blocks the rest of the tree.',
           'mod/2985041246/common/scripted_effects/ac_ucw.txt; mod/2985041246/events/Belka.txt'),
    Source('Provisional gameplay',
           'All Luremian focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects. Both states have no free '
           'shared slot, so only infrastructure, air base and radar levels are added.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the withheld ballot
    IdeaDef('held_ballot', 'The Withheld Ballot',
            'The National Administration governs under a democratic name while the vote stays suspended and the country stays split.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('ballot', 'document')),
    IdeaDef('ballot_date', 'A Date for the Ballot', 'The Administration has promised the chamber a polling day and is held to it.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'assembly')),
    IdeaDef('standing_admin', 'Administrators, Not Parties', 'Ministries run by career officials who answer to a published programme.',
            {'political_power_gain': 0.15, 'stability_factor': 0.01}, ('command', 'document')),
    IdeaDef('readiness_first', 'Readiness Ahead of the Ballot', 'The civil defence staff argues that the vote can wait until the shelters are ready.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.10, 'stability_factor': -0.02}, ('shelter', 'security')),
    IdeaDef('chamber_rules', 'Standing Orders of the Chamber', 'Fixed polling days, a written order of business and a budget the deputies must pass.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('assembly', 'scales')),
    IdeaDef('timetable_government', 'Government to a Timetable', 'Every ministry publishes the dates by which its decisions will be taken.',
            {'political_power_gain': 0.20, 'production_factory_efficiency_gain_factor': 0.03}, ('rail', 'document')),
    IdeaDef('warden_network', 'Wardens in Every Street', 'Shelter wardens report on supplies, roofs and rumours to the directorate.',
            {'stability_factor': 0.06, 'war_support_factor': 0.06, 'consumer_goods_factor': 0.03}, ('security', 'civil')),
    IdeaDef('two_province_settlement', 'The Two-Province Settlement', 'A written division of revenue and offices between Olastetten and Qesi.',
            {'stability_factor': 0.06, 'political_power_factor': 0.05}, ('scales', 'assembly')),
    # Olastetten
    IdeaDef('highland_roll', 'The Highland Roll', 'Every road, spring, terrace and school in the five Olastetten provinces, on one register.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('document', 'civil')),
    IdeaDef('terrace_crews', 'Terrace Crews', 'Paid crews rebuild hill terraces and stone drains before the heavy rains return.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.03}, ('tools', 'civil')),
    IdeaDef('knadorf_drains', 'Storm Drains of Knadorf', 'Culverts and channels carry the rain off the capital streets instead of through them.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.05}, ('civil', 'rebuild')),
    IdeaDef('upward_city', 'Knadorf Builds Upward', 'Taller blocks on the old plots, so the capital grows without taking the terraces.',
            {'production_factory_efficiency_gain_factor': 0.03, 'stability_factor': -0.01}, ('rebuild', 'industry')),
    IdeaDef('ribbon_towns', 'Towns Along the Line', 'New housing strung along both railway lines out of Knadorf.',
            {'production_speed_infrastructure_factor': 0.10, 'supply_consumption_factor': -0.03}, ('rail', 'civil')),
    IdeaDef('station_markets', 'Station Market Days', 'Farmers and traders sell from the platforms at Knadorf twice a week.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('economy', 'rail')),
    # Qesi
    IdeaDef('qesi_ledger', 'The Qesi Ledger', 'Output, breakdowns and lost shifts in the four desert plants, counted honestly.',
            {'production_factory_efficiency_gain_factor': 0.02, 'political_power_gain': -0.05}, ('industry', 'document')),
    IdeaDef('cool_shifts', 'Dawn and Dusk Shifts', 'The Qesi plants work early and late and stand idle in the worst heat of the day.',
            {'production_factory_max_efficiency_factor': 0.03, 'stability_factor': 0.02}, ('industry', 'civil')),
    IdeaDef('desert_crude', 'Crude Under the Desert', 'A mapped and metered oil field feeding the plants beside it.',
            {'production_speed_buildings_factor': 0.04, 'supply_consumption_factor': -0.03}, ('economy', 'tools')),
    IdeaDef('rail_steel', 'Qesi Rail Steel', 'Qesi steel rolled into rail, sleeper plates and bridge girders.',
            {'production_speed_infrastructure_factor': 0.15, 'production_factory_efficiency_gain_factor': 0.02}, ('rail', 'industry')),
    IdeaDef('plate_steel', 'Plate for the Arms Line', 'Qesi steel reserved for the arms plants and their replacement orders.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.03}, ('industry', 'security')),
    IdeaDef('qesi_cisterns', 'The Qesi Cisterns', 'Covered cisterns fill in the rains and serve the desert towns through the dry weeks.',
            {'stability_factor': 0.04, 'production_speed_buildings_factor': 0.03}, ('civil', 'shelter')),
    # the eight plants
    IdeaDef('full_ground', 'Every Slot Taken', 'Every slot of usable industrial ground in both provinces is already built on.',
            {'production_factory_efficiency_gain_factor': 0.03}, ('industry', 'document')),
    IdeaDef('replacement_lines', 'Lines for Replacement Kit', 'The arms plants make spares and replacement equipment before anything new.',
            {'production_speed_arms_factory_factor': 0.08, 'supply_consumption_factor': -0.03}, ('industry', 'tools')),
    IdeaDef('machine_shops', 'Machine Tools Before Munitions', 'Workshops build presses, lathes and pumps for every other plant.',
            {'production_speed_industrial_complex_factor': 0.10, 'research_speed_factor': 0.02}, ('tools', 'industry')),
    IdeaDef('rolling_stock_works', 'Rolling Stock Works', 'Wagon and locomotive repair grows into wagon and locomotive building.',
            {'production_speed_infrastructure_factor': 0.10, 'industrial_capacity_factory': 0.04}, ('rail', 'industry')),
    IdeaDef('depot_spares', 'Spares in Every Depot', 'Each supply depot holds a stock of parts for the equipment it serves.',
            {'supply_consumption_factor': -0.05, 'army_org_factor': 0.02}, ('logistics', 'tools')),
    IdeaDef('night_apprentices', 'Night-Shift Apprentices', 'Young workers learn the trades on the night shifts of all eight plants.',
            {'production_factory_efficiency_gain_factor': 0.04, 'stability_factor': 0.01}, ('training', 'industry')),
    # rail and freight
    IdeaDef('national_timetable', 'One National Timetable', 'Both lines out of Knadorf run to one published timetable.',
            {'supply_consumption_factor': -0.03, 'production_speed_infrastructure_factor': 0.05}, ('rail', 'document')),
    IdeaDef('charter_register', 'The Charter Register', 'Luremian cargo contracts in foreign harbours, recorded and insured from Knadorf.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.01}, ('logistics', 'document')),
    IdeaDef('through_running', 'Through-Running Wagons', 'Luremian wagons travel loaded into foreign yards and come back loaded.',
            {'consumer_goods_factor': -0.04, 'political_power_gain': -0.05}, ('rail', 'diplomacy')),
    IdeaDef('transshipment_yards', 'Frontier Transshipment', 'Cargo changes trains in Luremian yards just inside every frontier.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('rail', 'logistics')),
    IdeaDef('engine_sheds', 'The Knadorf Engine Sheds', 'Covered sheds where every locomotive is stripped and overhauled on a cycle.',
            {'supply_consumption_factor': -0.03, 'repair_speed_factor': 0.08}, ('rail', 'tools')),
    IdeaDef('export_engines', 'Engines for Export', 'Locomotives built at home are sold to the railways that already carry Luremian wagons.',
            {'industrial_capacity_factory': 0.04, 'consumer_goods_factor': -0.02}, ('rail', 'economy')),
    IdeaDef('yard_towns', 'The Yard Towns', 'The frontier transshipment yards have grown into small towns with steady work.',
            {'stability_factor': 0.05, 'consumer_goods_factor': -0.03}, ('civil', 'logistics')),
    # the four battalions
    IdeaDef('thin_battalions', 'Four Battalions, Two Provinces', 'A very small army spread across hills, mountains and desert.',
            {'army_core_defence_factor': 0.04, 'training_time_army_factor': -0.05}, ('security', 'training')),
    IdeaDef('pass_garrisons', 'Garrisons in the Passes', 'Companies dug into the mountain passes of Olastetten.',
            {'army_core_defence_factor': 0.10, 'army_defence_factor': 0.05}, ('security', 'command')),
    IdeaDef('rail_reserve', 'Battalions Kept on the Trains', 'A reserve kept on its trains, able to reach either province in a day.',
            {'army_speed_factor': 0.05, 'planning_speed': 0.10}, ('rail', 'security')),
    IdeaDef('shelter_companies', 'Shelter Companies', 'Every town keeps a trained company for rescue, shelter duty and local defence.',
            {'stability_factor': 0.03, 'army_core_defence_factor': 0.05, 'training_time_army_factor': -0.10}, ('shelter', 'training')),
    IdeaDef('mud_drill', 'Drilled for the Mud', 'Marches, supply runs and digging practised in rain and mud.',
            {'attrition': -0.05, 'army_org_factor': 0.03}, ('training', 'logistics')),
    IdeaDef('line_depots', 'Depots on the Line', 'Replacement depots sited at the stations of both railway lines.',
            {'supply_consumption_factor': -0.05, 'repair_speed_factor': 0.08}, ('logistics', 'rail')),
    # the airfield
    IdeaDef('weather_office', 'The Airfield Weather Office', 'Forecasts of rain and cloud from the Knadorf field, for farms, railways and pilots.',
            {'air_detection': 0.05, 'research_speed_factor': 0.01}, ('telescope', 'runway')),
    IdeaDef('flying_school', 'A Leased Flying School', 'Leased trainers and contract instructors teach the first Luremian pilots.',
            {'experience_gain_air_factor': 0.10, 'air_mission_efficiency': 0.03}, ('air', 'training')),
    IdeaDef('ridge_observers', 'Observers on the Ridges', 'Volunteer posts on the high ground report every aircraft by telephone.',
            {'air_detection': 0.10, 'static_anti_air_damage_factor': 0.05}, ('radar', 'security')),
    # frontiers
    IdeaDef('frontier_liaison', 'Frontier Liaison Offices', 'One office for each of the four neighbours, at the main crossing.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('diplomacy', 'document')),
    IdeaDef('desert_customs', 'Customs on the Desert Road', 'Posts on the Qesi crossings collect duties and count the traffic.',
            {'political_power_gain': 0.05, 'consumer_goods_factor': -0.02}, ('document', 'logistics')),
    IdeaDef('declared_neutrality', 'Neutral in the Statute Book', 'Permanent neutrality written into law, with an army sized to defend it.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.04}, ('peace', 'scales')),
    IdeaDef('unwritten_options', 'Nothing Promised in Writing', 'Friendly words to every neighbour and a signature for none.',
            {'political_power_gain': 0.10, 'war_support_factor': 0.03}, ('diplomacy', 'command')),
    IdeaDef('frontier_monitors', 'Frontier Monitors', 'Analysts in Knadorf read the press and radio of all four neighbours every day.',
            {'political_power_factor': 0.05, 'stability_factor': 0.02}, ('communications', 'document')),
    IdeaDef('grazing_fees', 'Seasonal Grazing Fees', 'Registered herders pay a small fee for each season on the valley pastures.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('scales', 'civil')),
    # Ulysses
    IdeaDef('sky_bulletin', 'The Sky Bulletin', 'A weekly broadcast of what is known, and not known, about the asteroid.',
            {'stability_factor': 0.02, 'war_support_factor': 0.02}, ('meteor', 'communications')),
    IdeaDef('rock_galleries', 'Galleries in the Rock', 'Shelters cut into the hills and mountains of Olastetten.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.04}, ('shelter', 'tools')),
    IdeaDef('deep_galleries', 'The Deep Galleries', 'Ventilated, stocked galleries under Knadorf with room for most of the capital.',
            {'static_anti_air_damage_factor': 0.15, 'stability_factor': 0.05}, ('shelter', 'civil')),
    IdeaDef('evacuation_trains', 'Evacuation by Rail', 'A plan to move whole towns by train between the two provinces.',
            {'stability_factor': 0.04, 'supply_consumption_factor': -0.03}, ('rail', 'refugees')),
    IdeaDef('evacuation_drilled', 'Timetables for Leaving', 'Every town knows its train, its platform and its hour.',
            {'stability_factor': 0.06, 'army_speed_factor': 0.03, 'supply_consumption_factor': -0.03}, ('rail', 'shelter')),
    IdeaDef('shelter_stores', 'Ninety Days of Stores', 'Grain, water and medicine kept for three months in every district.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.03}, ('shelter', 'economy')),
    # distant wars
    IdeaDef('fuel_cards', 'Fuel Ration Cards', 'Fuel sold by card while wartime prices stay high.',
            {'stability_factor': -0.02, 'supply_consumption_factor': -0.05}, ('document', 'economy')),
    IdeaDef('spares_licence', 'Spares for Distant Buyers', 'Licensed sales of spare parts to buyers far from any war zone.',
            {'production_speed_arms_factory_factor': 0.08, 'stability_factor': -0.02}, ('industry', 'diplomacy')),
    IdeaDef('rifles_home', 'Every Rifle Stays Home', 'No military exports of any kind while wars are being fought.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.02}, ('peace', 'security')),
    IdeaDef('war_clause_desk', 'The War-Clause Desk', 'A ministry desk that negotiates insurance war clauses for Luremian cargo.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('logistics', 'scales')),
    IdeaDef('peace_rates', 'Peacetime Freight Rates', 'Insurance and charter rates fall back as the Usean war ends.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('economy', 'peace')),
    # decision ideas
    IdeaDef('drain_crews', 'Drain Crews Out', 'Crews clear every culvert and gutter ahead of the next heavy rain.',
            {'production_speed_infrastructure_factor': 0.10, 'stability_factor': 0.01}, ('tools', 'civil')),
    IdeaDef('gallery_week', 'Gallery Week', 'Families spend a week learning their way around the shelters.',
            {'war_support_factor': 0.03, 'stability_factor': 0.01}, ('shelter', 'training')),
    IdeaDef('reserve_train_run', 'The Reserve Train Is Out', 'A reserve company rides the lines on an exercise timetable.',
            {'army_speed_factor': 0.04, 'experience_gain_army_factor': 0.05}, ('rail', 'training')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('republic_chamber', 'Cabinet of the Republic Chamber',
           'A cabinet formed from the majority of an elected chamber, governing collectively and answering to deputies on a '
           'fixed polling calendar. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('standing_administration', 'The Standing National Administration',
           'The National Administration made permanent as a non-party government of career officials working to a published '
           'programme, with the ballot left suspended. Provisional gameplay office with no named holder.',
           'neutrality', 'centrism_na'),
    Office('defence_directorate', 'Directorate of Civil Defence',
           'A directorate of civil defence officers, army staff and shelter administrators that governs by order until it '
           'declares the country ready. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('even_split', 'Two Points Apart', (
        "The cabinet secretary reads the agenda aloud in the old council room at Knadorf, and the first item is the cabinet "
        "itself. The National Administration has governed under a democratic banner with the ballot suspended, and the most "
        "recent polling puts the democratic parties at one half of the country and the non-party administrators only two "
        "points behind. Neither camp can claim the country. Both can claim to be its larger part on a good day.",
        "The democrats want the polling day restored and the chamber sitting again before the year is out. The "
        "administrators answer that a country of two provinces, eight plants and four battalions needs steady management "
        "more than it needs campaigns. A smaller group from the civil defence staff says nothing in the meeting and a great "
        "deal in the corridors: that the vote matters less than the readiness of the shelters, the depots and the trains.",
        "Today the cabinet decides only how the argument will be heard. A public hearing in the council room would be broadcast "
        "and quoted for months. Written submissions would be quieter, slower and easier to steer. The provincial delegations "
        "from Olastetten and Qesi have already booked rooms in the capital for the week.",
    ), (
        Option('Hold the hearing in public.', (Stability(0.02), PP(-10), Event('ballot_petition', 20))),
        Option('Ask for written submissions.', (PP(30), Stability(-0.01))),
    ), picture=2),
    EventDef('ballot_petition', 'Signatures on the Station Wall', (
        "Three weeks after the public hearing, volunteers set up folding tables on the platforms at Knadorf and at the Qesi "
        "junction and begin collecting signatures for a polling day. The lists are pinned to boards along the station walls "
        "so that anyone waiting for a train can read the names. By the end of the first week the boards run the length of "
        "both platforms, and the railway asks politely where it is supposed to put its timetables.",
        "Administration officials point out that a petition is not a vote and that the same people may have signed twice. "
        "The petition organisers reply that they would be happy to have the matter settled by a vote. Newspapers in both "
        "provinces print daily totals. In the hill towns the lists fill with families who have never signed anything; in the "
        "desert plants the shift committees sign as blocks.",
        "The cabinet must now decide what to do with the boards. Accepting the petition formally would oblige the "
        "Administration to answer it in writing within the month. Thanking the organisers and moving the tables off railway "
        "property would be lawful and would look, to half the country, like exactly what it is.",
    ), (
        Option('Accept the petition and answer in writing.', (Stability(0.03), PP(-15))),
        Option('Move the tables off railway property.', (PP(25), Stability(-0.02))),
    ), picture=2),
    EventDef('highland_returns', 'Notebooks from the Hills', (
        "The survey teams come down from the Olastetten hills with wet notebooks and very muddy boots. They have walked all "
        "five provinces of the capital state: the hills around Knadorf, the hill province on the line to Qesi, the hill "
        "country along the Glacelandic and Kalugan frontiers, and the two mountain provinces where the railway climbs to its "
        "depot and the passes run toward Silvonia.",
        "Their findings are more about water than about anything else. The rain here is heavy on close to half the days of "
        "the year and the ground is never really dry. Terraces built by earlier generations are slipping, village roads turn "
        "to mud by noon, and the storm channels under Knadorf were sized for a much smaller town. The mountain depot has a "
        "railway, a supply store and no clinic within half a day by road.",
        "The surveyors offer no single plan. They price terraces, drains, clinics and housing separately and leave the choice "
        "to the cabinet. The hill towns want the money spent where they live; the capital wants its own streets fixed first. "
        "The notebooks are already being quoted in both arguments.",
    ), (
        Option('Fix the hill villages first.', (Stability(0.02), PP(-10))),
        Option('Fix the capital first.', (PP(20), Research('construction_tech', 0.5, 1))),
    ), picture=1),
    EventDef('desert_works', 'Four Plants on the Sand', (
        "Qesi is the smaller of the two provinces and holds half the country's industry: three civilian plants and one arms "
        "works on desert ground at the far end of the railway from Knadorf. The ledger team sent from the capital spends a "
        "month on the shop floors and comes back with figures that nobody in the ministry disputes and nobody likes.",
        "The heat is the first problem. Shop floors reach temperatures at which machines and people both fail, and the plants "
        "lose most of every afternoon. The rain is the second: when it comes, it falls hard on ground that cannot absorb it, "
        "and the access roads flood within the hour. The third is distance. Every spare part, every engineer and every "
        "payroll comes down a single line through the hills, and a washout anywhere on it stops all four plants.",
        "The plant managers want the ledger kept inside the ministry until they have had a chance to answer it. The shift "
        "committees want it read aloud in the canteens, because they have been saying the same things for years. The cabinet "
        "has to choose who reads it first.",
    ), (
        Option('Read it in the canteens.', (Stability(0.02), PP(-10))),
        Option('Give the managers a month to answer.', (PP(20), Research('industry', 0.5, 1))),
    ), picture=1),
    EventDef('no_spare_ground', 'Not One Free Plot', (
        "The planning office in Knadorf finishes its map of industrial land and pins it to the wall of the cabinet room. "
        "Every usable plot in both provinces is coloured in. Olastetten holds two civilian plants and two arms works; Qesi "
        "holds three civilian plants and one arms works. There is no ground left in either province on which a new plant "
        "could be built without first pulling an old one down.",
        "The consequence is simple and unwelcome. Luremia cannot grow its industry by adding halls, as larger countries do. "
        "It can only make the halls it has work better: more output per shift, fewer breakdowns, better tools and a clearer "
        "idea of what each plant is for. The ministers who hoped to open a new works before the next budget fold their "
        "speeches away.",
        "Three schools of thought are already forming. One wants the arms works kept busy making replacement equipment for "
        "the battalions. One wants the plants to build machine tools for each other. A third points at the twenty-four trains "
        "the country owns and asks why it does not build its own wagons and engines. First the cabinet must decide whether to "
        "publish the map.",
    ), (
        Option('Publish the map with the budget.', (Stability(0.01), Research('industry', 0.5, 1))),
        Option('Keep it for the planning office.', (PP(25),)),
    ), picture=1),
    EventDef('landlocked_freight', 'Freight Without a Harbour', (
        "Luremia has no coast. Everything it buys from beyond its four neighbours arrives in a foreign harbour, is loaded "
        "onto a foreign train or truck and crosses a frontier before it reaches a Luremian railway. The national register "
        "nevertheless lists sixty convoys of chartered cargo space, all of it loading and unloading in other countries' "
        "ports, and the ministry pays for all of it.",
        "The freight office lays out what this costs. Every delay at a foreign quay, every strike at a foreign yard and every "
        "change in a neighbour's customs rules lands on Luremian shelves within a fortnight. The country owns twenty-four "
        "trains and two lines out of Knadorf, one climbing to the mountain depot and one running through the hills to the "
        "desert junction at Qesi. Both lines were laid for a smaller economy.",
        "Railway officers want a single national timetable before anything else, so that at least the trains under Luremian "
        "control run when they say they will. The freight office wants to start with the foreign contracts, where the money "
        "is lost. The cabinet decides where the first year of effort goes, and which office explains the choice to the "
        "plants.",
    ), (
        Option('Start with our own timetable.', (Stability(0.02), Research('train_tech', 0.5, 1))),
        Option('Start with the foreign contracts.', (PP(15), Stability(0.01))),
    ), picture=1),
    EventDef('battalion_count', 'Roll Call for a Small Army', (
        "The general staff calls the roll of the Luremian army and the answer fits on a single sheet of paper: four infantry "
        "battalions in three formations, trained for territorial defence, with no aircraft, no warships and no engineers. "
        "The depots hold eight hundred sets of infantry equipment, six hundred and forty motor vehicles and the twenty-four "
        "trains the army shares with the railway.",
        "The officers present the roll without apology. The army was never meant to fight a neighbour alone; it was meant to "
        "hold ground, guard the depots and help the towns when the rain or anything else brings disaster. In mud that never "
        "dries and heat that never breaks, even that modest task is hard. Half the vehicles spend the rainy weeks parked, and "
        "the mountain companies rely on mules and boots.",
        "The staff asks the cabinet for a doctrine. It can hold the mountain passes, keep a reserve on the trains, or turn every "
        "town into a trained shelter company. Before any choice, the staff wants to know whether the roll will be read out in "
        "the chamber or kept on file.",
    ), (
        Option('Read the roll in public.', (WarSupport(0.03), Stability(-0.01))),
        Option('Keep it on file.', (XP('army', 20),)),
    ), picture=0),
    EventDef('airfield_question', 'What the Airfield Is For', (
        "Luremia has one air base, at Knadorf, and no combat aircraft at all. The runway is used by a handful of transport "
        "and mail flights, a crop sprayer and the occasional foreign charter. The control tower doubles as the only place in "
        "the country with instruments good enough to forecast rain, and farmers phone it every morning to ask whether to cut "
        "hay.",
        "A study from the transport ministry asks what the field should become. Some officers want a flying school, with "
        "leased trainers and foreign instructors, so that the country at least has pilots if it ever needs them. Others want "
        "money spent on observers and radar instead, so that Luremia can see any aircraft over its hills even if it cannot "
        "meet them. The weather service wants to be left alone.",
        "Nobody proposes buying fighters; the budget would not survive it and nobody can say what they would be for. The "
        "question for the cabinet is narrower: whether to treat the airfield as a military asset or a civil one while the "
        "argument goes on. The answer decides which ministry pays for the runway drains, and which one gets to say no "
        "the next time a foreign charter asks to land in a storm.",
    ), (
        Option('Treat it as a military asset.', (XP('air', 15), PP(-10))),
        Option('Keep it civil for now.', (Stability(0.02), Research('radar_tech', 0.5, 1))),
    ), picture=0),
    EventDef('four_frontiers', 'Four Neighbours Around a Small Country', (
        "The new liaison officers present their first joint report. Luremia touches four countries and no sea. Kaluga lies "
        "beyond the forests that close in on Knadorf and the two mountain provinces. Glaceland meets both provinces, its frontier districts "
        "reaching the hill country of Olastetten and the desert junction at Qesi. Sfaenland faces the two desert provinces. "
        "Silvonia meets one mountain province and one desert province, in the far corner of the country.",
        "The officers stress how much of this frontier is managed by habit. Herders and foresters cross the valley paths in "
        "season, desert traders take the road toward Sfaenland without much paperwork, and the posts in the Silvonia corner "
        "are rarely visited by anyone from the capital. None of the four neighbours is holding elections at present. In three "
        "of them nationalist movements command half the voters; in Kaluga the democratic parties hold a clear majority.",
        "The cabinet is asked to agree a tone for all four relationships before it settles any one of them. It can introduce "
        "the liaison offices through a published statement, or through quiet letters to each capital. Either way, the offices "
        "open their doors next month.",
    ), (
        Option('Publish a statement.', (Stability(0.02), PP(-10))),
        Option('Send quiet letters.', (PP(25),)),
    ), picture=2),
    EventDef('impact_word', 'Fragments Will Fall Somewhere', (
        "The FCU announcement of April 1996 leaves no room for hope that Ulysses will miss. The astronomers' warning of "
        "December 1994 hardens into a certainty, and the only remaining question, where the fragments will fall, is the one "
        "nobody can answer. The Knadorf radio repeats the announcement every hour, then stops repeating it and starts "
        "taking calls instead.",
        "Luremia is a country whose small army was built for civil defence and whose capital sits among hills and mountains of "
        "solid rock. The engineers say the obvious thing: cut galleries into the hills and stock them. The railway officers "
        "say the other obvious thing: a country with two provinces and two lines can move whole towns by train, toward "
        "whichever province looks safer when the time comes. Each group thinks the other's plan is a fantasy.",
        "The public is ahead of the planners. Hardware shops in Knadorf run out of lamps and water drums, and families in the "
        "hill towns begin clearing their cellars without being told to. The cabinet must decide what it says first: the "
        "danger, or the plan it does not yet have.",
    ), (
        Option('Speak first about the plan.', (Stability(0.02), PP(-10))),
        Option('Speak first about the danger.', (WarSupport(0.03), Stability(-0.02), Research('construction_tech', 0.5, 1))),
    ), citation='date anchors only, Official Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; '
                'where fragments fall is not claimed and the Luremian response is gameplay', picture=0),
    EventDef('roche_night', 'A Night Underground', (
        "Ulysses crosses the Roche limit on 8 July 1999, and Luremia spends the night ready to move. Trains wait at every "
        "platform with crews aboard and engines warm, the shelter wardens walk their streets with lists, and the radio at Knadorf stays on "
        "the air all night reading the same short bulletin every quarter hour. Nobody knows what the night will bring to "
        "these hills, and nobody pretends to.",
        "Families who prepared go where they planned to go: into the galleries, onto the evacuation trains, or down into their "
        "own cellars with water and a radio. Families who did not prepare stand in the street and watch the sky. At the Qesi "
        "plants the night shift keeps working because the managers cannot think what else to tell it. The battalions wait at "
        "their depots for orders that may never come.",
        "By dawn the cabinet must decide how long to keep the country in this state. Standing down too early risks being "
        "wrong in front of everyone. Staying mobilised for weeks costs wages, harvests and patience. The wardens want an "
        "answer they can give the people on their lists by breakfast.",
    ), (
        Option('Keep the shelters open for a week.', (WarSupport(0.03), Stability(-0.02))),
        Option('Stand down as the reports allow.', (Stability(0.03), PP(-15))),
    ), citation='date anchor only, Official Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; no damage in Luremia is '
                'claimed and the response is gameplay', picture=0),
    EventDef('belkan_prices', 'The Belkan War Reaches the Shops', (
        "In March 1995 war breaks out around Belka. No Luremian frontier touches it and no Luremian has any part in it, yet "
        "within a fortnight its effects are on the shelves in Knadorf. Fuel costs more, imported machinery costs more, and "
        "the charter contracts in foreign harbours arrive with new war clauses that the freight office has to read twice to "
        "understand.",
        "The arms works receive letters from buyers they have never heard of, asking about spare parts and replacement kit. "
        "Some ministers see orders that would keep the night shifts busy. Others see a small country making enemies it can "
        "never afford, and remind the cabinet that every rifle sold abroad is a rifle the four battalions do not have.",
        "The cabinet meets twice in one week. It must decide whether to calm prices first or settle the question of exports "
        "first, knowing that it cannot do both at once and that the newspapers will report whichever it chooses as the "
        "government's real priority. In Qesi the shift committees have already asked whether the night shifts will be "
        "kept, and in the hill towns the bakers have raised the price of bread by a tenth to cover the cost of fuel for "
        "their ovens.",
    ), (
        Option('Calm the prices first.', (Stability(0.02), PP(-15))),
        Option('Settle the export question first.', (PP(20), WarSupport(0.02))),
    ), citation='date anchor only, Official Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Luremian response '
                'is gameplay', picture=2),
    EventDef('usean_freight', 'War Clauses Again', (
        "In August 2003 the ISAF is formed to oppose Erusea, and the war in Usea becomes the business of every freight "
        "office in the world. Luremia has no frontier in Usea and takes no side, but its charter cargoes cross the same oceans "
        "as everyone else's. Within a week the insurers send new war clauses and new rates, and two charter owners ask to "
        "be released from their contracts.",
        "The war-clause desk in Knadorf has seen this before, during the Belkan War, and its officials know the order in which "
        "things go wrong: premiums first, then delays, then empty shelves. They propose to reroute what can be rerouted, "
        "stock what can be stocked and accept that some prices will rise. The plant managers want guaranteed deliveries of "
        "spares. The shops want guaranteed deliveries of everything.",
        "The cabinet must decide how much of the extra cost to carry itself. Subsidising the new premiums would keep prices "
        "steady and drain the treasury. Passing them on would be honest, quick and unpopular in both provinces. The desk "
        "warns that the war could last for years, and that a subsidy begun now will be very hard to withdraw before "
        "it ends.",
    ), (
        Option('Carry the premiums for a year.', (Stability(0.02), PP(-20))),
        Option('Pass the costs on.', (PP(20), Stability(-0.02))),
    ), citation='date anchor only, Official Chronicle row 2003 / 08.22 in tools/lore/chronicle.json, with the mod flag '
                'ac_ucw_isaf_formed; no Luremian part in the war is claimed', picture=1),
)

# --- branches ------------------------------------------------------------------------------------
BALLOT = Branch('vote', 'Fifty Against Forty-Eight', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('vote_split', 'Two Points Between the Camps',
          "Luremia opens 1991 under a National Administration that carries a democratic name while the ballot stays "
          "suspended, and the country is almost evenly divided: half back the democratic parties and nearly as many back the "
          "non-party administrators. Putting the government itself on the cabinet agenda costs the Administration its quiet "
          "months, but it lets every camp be heard before anyone decides.",
          ('ballot', 'assembly'), reward=(Idea('held_ballot'), Event('even_split'))),
    Focus('vote_terms', 'Publish the Terms of Office',
          "The Administration prints the legal basis on which it governs: the emergency powers it uses, the statute that "
          "still prescribes a vote every four years, and the clause under which that vote was set aside. Publishing it hands "
          "the opposition a text to argue over. It also makes plain that some choice about the ballot can no longer be put off.",
          ('document', 'scales'), after=('vote_split',),
          reward=(PP(30), Tooltip('Opens three answers to the suspended ballot; only one can be taken.'))),
    Focus('vote_chamber_path', 'The Chamber Must Sit Again',
          "The democratic camp asks for the plain thing: restore polling day, seat the chamber and make ministers answer to "
          "it. Its strength lies in the hill towns and the Knadorf offices. The cost is a government that must bargain for "
          "every budget in a country split almost down the middle, and that could lose the first vote it calls.",
          ('ballot', 'civil'), after=('vote_terms',), exclusive=('vote_admin_path', 'vote_shelter_path'),
          reward=(SwapIdea('held_ballot', 'ballot_date'),)),
    Focus('vote_admin_path', 'Administrators Without Parties',
          "The neutral camp argues that a country of two provinces and eight plants needs competent management more than "
          "campaigns, and that the Administration should become a permanent non-party government with a published programme. "
          "Decisions would come faster and quarrel less. Half the country would be told, politely, that its preferred "
          "parties are not needed.",
          ('command', 'document'), after=('vote_terms',), exclusive=('vote_chamber_path', 'vote_shelter_path'),
          reward=(SwapIdea('held_ballot', 'standing_admin'),)),
    Focus('vote_shelter_path', 'Readiness Ahead of the Ballot',
          "Officers of the civil defence staff argue that the army exists to protect towns from disaster, and that the vote "
          "should wait until shelters, depots and trains are ready for the worst. Their argument carries weight in a country "
          "built for civil defence. It carries much less with families who notice that readiness never seems to arrive.",
          ('shelter', 'security'), after=('vote_terms',), exclusive=('vote_chamber_path', 'vote_admin_path'),
          reward=(SwapIdea('held_ballot', 'readiness_first'),)),
    Focus('vote_chamber_seat', 'Seat the Republic Chamber',
          "Polling day is held, the chamber sits, and a cabinet drawn from its majority takes the seals of government. The "
          "change runs through the office, not a person: the cabinet governs collectively and answers to deputies. The "
          "Administration's officials stay in post and learn to brief ministers who can be voted out.",
          ('assembly', 'ballot'), after=('vote_chamber_path',), cost=10,
          exclusive=('vote_admin_seat', 'vote_shelter_seat'), reward=(Regime('republic_chamber'), Flag('gov_chamber'))),
    Focus('vote_admin_seat', 'Make the Administration Permanent',
          "The National Administration is reconstituted as a standing non-party government of career officials. Elections "
          "remain suspended, and the programme the government publishes each year takes the place of a manifesto. Ministries "
          "gain continuity and lose the excuse of an election. Every failure now belongs to the officials who run them.",
          ('command', 'scales'), after=('vote_admin_path',), cost=10,
          exclusive=('vote_chamber_seat', 'vote_shelter_seat'),
          reward=(Regime('standing_administration'), Flag('gov_admin'))),
    Focus('vote_shelter_seat', 'Install the Civil Defence Directorate',
          "A directorate of civil defence officers, army staff and shelter administrators takes executive power and governs "
          "by order. It promises to hand power back once it judges the country ready. It brings real competence in "
          "emergencies, and a habit of treating every public question as one, which wears on the country faster than any "
          "storm.",
          ('security', 'shelter'), after=('vote_shelter_path',), cost=10,
          exclusive=('vote_chamber_seat', 'vote_admin_seat'),
          reward=(Regime('defence_directorate'), Flag('gov_directorate'))),
    Focus('vote_calendar', 'A Ballot Every Four Years',
          "With the chamber seated, deputies write standing orders that fix polling day on the four-year cycle the old statute "
          "always required, set a deadline for each budget and give the opposition a weekly hour to question ministers. "
          "Governing becomes slower and more public. Both provinces can now see who promised what.",
          ('ballot', 'document'), after=('vote_chamber_seat',), requires=(HasFlag('gov_chamber'),),
          exclusive=('vote_timetable', 'vote_wardens'), reward=(SwapIdea('ballot_date', 'chamber_rules'),)),
    Focus('vote_timetable', 'Government Run to a Timetable',
          "The standing Administration borrows the habits of the railway: every ministry publishes a timetable of the "
          "decisions it will take and the dates it will take them by, and late decisions are listed in the newspapers. "
          "Officials hate the lists. Citizens who cannot vote at least get a schedule they can hold the government to.",
          ('rail', 'document'), after=('vote_admin_seat',), requires=(HasFlag('gov_admin'),),
          exclusive=('vote_calendar', 'vote_wardens'), reward=(SwapIdea('standing_admin', 'timetable_government'),)),
    Focus('vote_wardens', 'A Warden on Every Street',
          "The directorate appoints a shelter warden for every street in Knadorf and every village in the hills and the "
          "desert. Wardens count supplies, inspect roofs and cellars and report on the mood of their neighbours. Preparation "
          "improves quickly. So does the directorate's knowledge of who complains, which is exactly what its critics feared.",
          ('security', 'civil'), after=('vote_shelter_seat',), requires=(HasFlag('gov_directorate'),),
          exclusive=('vote_calendar', 'vote_timetable'), reward=(SwapIdea('readiness_first', 'warden_network'),)),
    Focus('vote_settlement', 'One Settlement for Two Provinces',
          "Whatever government holds the seals, Olastetten and Qesi still argue about revenue, posts in the ministries and "
          "who pays for the railway between them. A written settlement fixes the shares for a decade. It costs both "
          "provinces a few cherished grievances and ends an argument that has outlasted every government before it.",
          ('scales', 'assembly'), after_any=('vote_calendar', 'vote_timetable', 'vote_wardens'),
          reward=(Idea('two_province_settlement'), Stability(0.02))),
))

HILLS = Branch('hills', 'Knadorf and the Olastetten Hills', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('hill_roll', 'Walk the Five Highland Provinces',
          "Olastetten is the capital state: Knadorf and two other hill provinces, plus two mountain provinces, one carrying "
          "the railway to its depot. Nobody in the capital holds a reliable register of its roads, springs or schools. Survey "
          "teams on foot spend a rainy season walking every valley, and the ministries pay for their boots and their patience.",
          ('document', 'civil'), reward=(Idea('highland_roll'), Event('highland_returns'))),
    Focus('hill_terraces', 'Terraces Against the Rain',
          "Heavy rain falls on nearly half the days of the year, and the old terraces on the Olastetten hillsides are "
          "slipping. Paid crews rebuild the stone walls and the drains between them before each wet spell. It is slow, "
          "manual work that produces nothing new, only keeps the fields from sliding into the valleys.",
          ('tools', 'civil'), after=('hill_roll',), reward=(TimedIdea('terrace_crews', 730),)),
    Focus('hill_drains', 'Storm Drains Under Knadorf',
          "The channels under the capital were dug for a much smaller town, and every heavy storm sends water down the main "
          "streets and into the plant basements. Engineers propose wider culverts and a relief channel to the valley floor. "
          "Streets will be dug up for two seasons, and shopkeepers will complain about every week of it.",
          ('civil', 'rebuild'), after=('hill_roll',), reward=(Idea('knadorf_drains'),)),
    Focus('hill_clinic', 'A Clinic at the Mountain Depot',
          "The mountain province where the railway climbs to its supply depot has workers, soldiers and families, and no "
          "clinic within half a day by road. A small clinic beside the depot, staffed in rotation from Knadorf, serves all "
          "of them. Doctors dislike the posting. The depot crews notice that somebody finally thought of them.",
          ('medical', 'rail'), after=('hill_roll',), reward=(Flag('mountain_clinic'), Stability(0.02))),
    Focus('hill_upward', 'Knadorf Builds Upward',
          "One school of planners wants the capital to grow upward: taller blocks on the old plots, so that new housing does "
          "not take the terraced fields around the town. It keeps the farms and the short walk to work. It also means "
          "crowded streets, higher rents and drains that have to carry even more water.",
          ('rebuild', 'industry'), after_any=('hill_terraces', 'hill_drains'), cost=10, exclusive=('hill_ribbon',),
          reward=(Idea('upward_city'),)),
    Focus('hill_ribbon', 'Towns Strung Along the Railway',
          "The other school wants new housing strung along both railway lines out of Knadorf, with halts every few "
          "kilometres and roads graded between them. Families get gardens and cheaper rents; the railway gets passengers. "
          "The terraced fields beside the line are lost, and every commuter now depends on a timetable.",
          ('rail', 'civil'), after_any=('hill_terraces', 'hill_drains'), cost=10, exclusive=('hill_upward',),
          reward=(Idea('ribbon_towns'), Build('infrastructure', 1, 226))),
    Focus('hill_rope_teams', 'Rope Teams for the Mountains',
          "The new clinic at the depot handles the injured once they arrive; the problem is getting them there. Volunteers "
          "from the mountain villages form rope teams for rescue on the passes and the slopes above the line, trained by the "
          "army's mountain companies. They work for little and are known by name in every village.",
          ('medical', 'security'), after=('hill_clinic',), reward=(Flag('rope_teams_set'), XP('army', 10))),
    Focus('hill_markets', 'Market Days at Knadorf Station',
          "However the capital grows, its farmers and traders need a place to sell. The railway opens the platforms at "
          "Knadorf twice a week for market stalls, with produce arriving on the morning trains from both lines. Ticket "
          "inspectors find the arrangement chaotic. Families find the bread cheaper and the gossip better.",
          ('economy', 'rail'), after_any=('hill_upward', 'hill_ribbon'), reward=(TimedIdea('station_markets', 1095),)),
))

QESI = Branch('qesi', 'Qesi in the Heat', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('qesi_count', 'Four Plants on Desert Ground',
          "Qesi, two desert provinces at the far end of the line from Knadorf, holds three civilian plants and one arms works, "
          "half the country's industry. Nobody in the capital knows how much of each shift is lost to heat, floods and "
          "missing parts. A ledger team spends a month on the shop floors and counts it, to the managers' discomfort.",
          ('industry', 'document'), reward=(Idea('qesi_ledger'), Event('desert_works'))),
    Focus('qesi_channels', 'Flood Channels Through the Sand',
          "Desert ground cannot drink the heavy rain, so every storm turns the access roads into rivers within the hour. "
          "Engineers cut lined channels and raised causeways across the worst stretches between the plants and the "
          "railhead. The work is costly in a province with little else to spend on, and it ends the flooded afternoons.",
          ('tools', 'logistics'), after=('qesi_count',), reward=(Build('infrastructure', 1, 231),)),
    Focus('qesi_shifts', 'Dawn and Dusk Shifts',
          "Shop floors in Qesi reach temperatures at which machines and workers both fail. The plants move to early and late "
          "shifts and stand idle in the worst of the afternoon. Output per hour rises and families adjust their days around "
          "the new hours. The managers lose the long single shift they were used to supervising.",
          ('industry', 'civil'), after=('qesi_count',), reward=(TimedIdea('cool_shifts', 1095),)),
    Focus('qesi_crude', 'Meter the Desert Crude',
          "The oil under Qesi has been pumped for years without anyone measuring what comes out or what is wasted. Metering "
          "every wellhead and piping the crude straight to the plants beside it costs money the province would rather spend "
          "on water. It also tells the treasury, for the first time, what the desert actually produces.",
          ('economy', 'tools'), after=('qesi_count',),
          reward=(TimedIdea('desert_crude', 1095), Research('excavation_tech', 0.5, 1))),
    Focus('qesi_rails', 'Roll Rails in Qesi',
          "One proposal sends Qesi steel to the railway: rails, sleeper plates and bridge girders for both lines out of "
          "Knadorf. Every washout repaired with home-rolled rail is a washout repaired without waiting for a foreign "
          "delivery. The arms works lose their first claim on the steel, and their managers say so loudly.",
          ('rail', 'industry'), after_any=('qesi_channels', 'qesi_shifts'), cost=10, exclusive=('qesi_plate',),
          reward=(SwapIdea('qesi_ledger', 'rail_steel'),)),
    Focus('qesi_plate', 'Armour Plate from Qesi Steel',
          "The other proposal reserves Qesi steel for the arms plants in both provinces, so that the replacement orders for "
          "the battalions never wait on imported plate. The arms lines run steadily and the army trusts its supply. The "
          "railway goes on buying foreign rail, and every washout takes as long to repair as it always did.",
          ('industry', 'security'), after_any=('qesi_channels', 'qesi_shifts'), cost=10, exclusive=('qesi_rails',),
          reward=(SwapIdea('qesi_ledger', 'plate_steel'),)),
    Focus('qesi_junction', 'The Junction Yard at Qesi',
          "The line from Knadorf ends at a desert junction close to both the Glaceland and the Sfaenland frontiers. Its "
          "yard is a single siding and a water tower. Extra sidings, a turning loop and a graded road to the plants let "
          "trains unload in hours instead of days, and make the junction worth stopping at.",
          ('rail', 'logistics'), after=('qesi_channels',),
          reward=(Build('infrastructure', 1, 231), Research('train_tech', 0.5, 1))),
    Focus('qesi_water', 'Cisterns for the Desert Towns',
          "The towns around the Qesi plants either flood or thirst, depending on the week. Covered cisterns filled in the "
          "rains and drawn down in the dry spells give them water all year. The cisterns are expensive to line and seal. "
          "They are also the first project in years that the desert towns asked for themselves.",
          ('civil', 'shelter'), after_any=('qesi_rails', 'qesi_plate'), reward=(Idea('qesi_cisterns'),)),
))

WORKS = Branch('works', 'Eight Plants and Not One Free Plot', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('works_full', 'Every Plot Already Built On',
          "Olastetten holds two civilian plants and two arms works, Qesi three civilian plants and one arms works, and there "
          "is no free industrial ground in either province. Luremia cannot grow by adding halls. A planning office maps every "
          "plot and every machine, so that whatever comes next makes the existing eight plants work harder.",
          ('industry', 'document'), reward=(Idea('full_ground'), Event('no_spare_ground'))),
    Focus('works_calendar', 'A Maintenance Calendar for Eight Plants',
          "Breakdowns in Luremian plants are fixed when they happen, which in the rainy weeks means constantly. A shared "
          "maintenance calendar stops each line on a planned day, replaces worn parts before they fail and records what "
          "broke. Output falls on the planned days. It falls less on all the others.",
          ('tools', 'document'), after=('works_full',), reward=(Research('industry', 0.5, 1), PP(-10))),
    Focus('works_replacement', 'Lines for Replacement Kit',
          "The first school wants the arms works to concentrate on what the four battalions actually wear out: rifles, "
          "boots, motor parts and radios. New equipment can wait; replacements cannot. The army gets a supply it can rely "
          "on, and the plants give up any hope of selling something new to anyone else.",
          ('industry', 'security'), after=('works_calendar',), cost=10,
          exclusive=('works_machinery', 'works_rolling'),
          reward=(SwapIdea('full_ground', 'replacement_lines'), Flag('model_replacement'))),
    Focus('works_machinery', 'Machine Tools Before Munitions',
          "The second school wants the plants to build presses, lathes and pumps for one another, so that the eight plants "
          "stop importing the machines they run on. It is patient, technical work that pays off slowly. The army notices "
          "that its replacement orders now queue behind a lathe for the plant next door.",
          ('tools', 'industry'), after=('works_calendar',), cost=10,
          exclusive=('works_replacement', 'works_rolling'),
          reward=(SwapIdea('full_ground', 'machine_shops'), Flag('model_machinery'))),
    Focus('works_rolling', 'Wagons and Engines at Home',
          "The third school points at the twenty-four trains the country owns and every wagon it rents abroad, and asks why "
          "the repair shops do not grow into builders. A country with two railway lines and no coast lives by rolling stock. "
          "The shops will need years to make their first engine, and the arms lines shrink to make room.",
          ('rail', 'industry'), after=('works_calendar',), cost=10,
          exclusive=('works_replacement', 'works_machinery'),
          reward=(SwapIdea('full_ground', 'rolling_stock_works'), Flag('model_rolling'))),
    Focus('works_depot_spares', 'Spare Parts in Every Depot',
          "With the arms works making replacements, the army stocks each supply depot with the parts for the equipment it "
          "serves, from rifle springs to truck axles. The stores cost money to fill and space to keep dry. A broken vehicle "
          "in the hills is now a morning's repair rather than a month's wait.",
          ('logistics', 'tools'), after=('works_replacement',), requires=(HasFlag('model_replacement'),),
          reward=(Idea('depot_spares'),)),
    Focus('works_toolroom', 'A National Toolroom',
          "The machine-tool school opens a shared toolroom in Knadorf where precision gauges, dies and fixtures are made "
          "for every plant in both provinces. Engineers who used to wait for foreign deliveries now walk down the street. "
          "The toolroom swallows the best machinists in the country, and the plants that lose them grumble.",
          ('tools', 'science'), after=('works_machinery',), requires=(HasFlag('model_machinery'),),
          reward=(Research('industry', 0.5, 2), Research('construction_tech', 0.5, 1))),
    Focus('works_first_engine', 'The First Luremian Locomotive',
          "After years of rebuilding other people's engines, the rolling-stock shops finish a locomotive of their own, "
          "assembled at Knadorf from home-made parts and imported components. It is heavy, slow and very reliable on the "
          "mountain grade. The crowd at its first run is larger than any political rally of the decade.",
          ('rail', 'medal'), after=('works_rolling',), requires=(HasFlag('model_rolling'),),
          reward=(Research('train_tech', 0.5, 2), Flag('home_locomotive'))),
    Focus('works_apprentices', 'Apprentices on the Night Shift',
          "Whatever the plants now make, they need skilled hands, and the young leave for neighbouring countries to find "
          "training. Every plant takes apprentices on its night shift, paired with a senior worker and paid a modest wage. "
          "Night output dips while they learn. Five years later the plants are training their own foremen.",
          ('training', 'industry'), after_any=('works_replacement', 'works_machinery', 'works_rolling'),
          reward=(Idea('night_apprentices'),)),
))

RAIL = Branch('rail', 'Two Lines and No Coast', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('rail_timetable', 'One Timetable for Both Lines',
          "Luremia has two railway lines out of Knadorf, one up to the mountain depot and one through the hills to the "
          "desert junction at Qesi, and they keep separate timetables written by separate offices. A single national "
          "timetable, published and kept, is the cheapest improvement the country can make. It costs the two offices their "
          "independence.",
          ('rail', 'document'), reward=(Idea('national_timetable'), Event('landlocked_freight'))),
    Focus('rail_grade', 'Regrade the Mountain Line',
          "The line to the mountain depot climbs a grade so steep that trains split in two to make it, and every heavy rain "
          "washes ballast off the curves. Engineers ease the worst curves, add drainage under the track and rebuild two "
          "embankments. The line closes for a summer, and the depot is supplied by mule while it is shut.",
          ('rail', 'bridge'), after=('rail_timetable',), reward=(Build('infrastructure', 1, 226),)),
    Focus('rail_trains', 'Twenty-Four Trains to Keep Running',
          "The country owns twenty-four trains, and any one of them out of service is a measurable share of national "
          "capacity. A census of engines and wagons records age, condition and the spares each needs. The census shows how "
          "many trains run on borrowed time, which the railway knew and the treasury did not.",
          ('rail', 'tools'), after=('rail_timetable',), reward=(Research('train_tech', 0.5, 1), Stability(0.01))),
    Focus('rail_charters', 'Sixty Convoys Without a Coast',
          "Luremia's national register lists sixty convoys of chartered cargo space, every one loading in a foreign harbour. "
          "The contracts were signed by different ministries on different terms. A single charter register in Knadorf "
          "renegotiates them together, insures them together and knows where every cargo is. Shipping agents lose some "
          "comfortable margins.",
          ('logistics', 'document'), after=('rail_timetable',), reward=(Idea('charter_register'),)),
    Focus('rail_through', 'Our Wagons into Foreign Yards',
          "One freight policy sends Luremian wagons loaded across the frontier and brings them back loaded, so that cargo "
          "never changes trains. Where foreign railways accept them, goods move faster and cheaper. The wagons then spend weeks in yards beyond any "
          "Luremian control, and the railway must trust other countries' shunters with its scarce stock.",
          ('rail', 'diplomacy'), after_any=('rail_grade', 'rail_trains'), cost=10, exclusive=('rail_transship',),
          reward=(SwapIdea('national_timetable', 'through_running'),)),
    Focus('rail_transship', 'Change Trains at the Frontier',
          "The other policy builds transshipment yards just inside each frontier, where foreign cargo moves onto Luremian "
          "wagons and the reverse. Every crossing costs a day of handling. The yards employ hundreds, the country's wagons "
          "never leave home, and customs officers inspect everything that crosses in a place they control.",
          ('logistics', 'security'), after_any=('rail_grade', 'rail_trains'), cost=10, exclusive=('rail_through',),
          reward=(SwapIdea('national_timetable', 'transshipment_yards'),)),
    Focus('rail_sheds', 'Engine Sheds at Knadorf',
          "Locomotives in Luremia are repaired in the open, in the rain, wherever they happen to break down. Covered engine "
          "sheds at Knadorf with pits, cranes and a stores room let every engine be stripped and overhauled on a fixed "
          "cycle. The sheds are expensive, and they double the working life of each engine.",
          ('rail', 'shelter'), after=('rail_trains',), reward=(Idea('engine_sheds'), Research('logistics_tech', 0.5, 1))),
    Focus('rail_engines_abroad', 'Engines Built at Home, Run Abroad',
          "With a Luremian locomotive proven on the mountain grade and Luremian wagons already running into foreign yards, "
          "the railway puts its engines up for sale to foreign lines. Any buyer will take years to persuade, and each contract "
          "that does arrive keeps the rolling-stock shops working through the lean years.",
          ('rail', 'economy'), after=('rail_through',), requires=(HasFlag('home_locomotive'),),
          reward=(TimedIdea('export_engines', 1095),)),
    Focus('rail_yard_towns', 'The Frontier Yards Hire Locally',
          "The transshipment yards hire their crews from the villages around each crossing, and housing, shops and schools "
          "follow the wages. Within a few years each yard is the centre of a small town. The towns depend entirely on "
          "freight, and every slow month at the frontier is felt at once in their shops.",
          ('civil', 'logistics'), after=('rail_transship',),
          reward=(SwapIdea('transshipment_yards', 'yard_towns'),)),
))

GUARD = Branch('guard', 'Four Battalions for Two Provinces', 1992, 'FOCUS_FILTER_ARMY_XP', (
    Focus('guard_muster', 'Call the Roll of Four Battalions',
          "The Luremian army is four infantry battalions in three formations, trained for territorial defence, with no "
          "aircraft and no engineers. Before choosing what it should become, the staff calls a full muster in both provinces "
          "and counts men, rifles, vehicles and boots. The count is short, honest and a little embarrassing.",
          ('security', 'training'), reward=(Idea('thin_battalions'), Event('battalion_count'))),
    Focus('guard_climbers', 'Mountain Companies from the Hills',
          "The army already teaches mountain warfare, and the volunteer rope teams on the passes now give it recruits who "
          "know the slopes. Each battalion forms a mountain company drawn from the hill villages, trained on the routes the "
          "rope teams use. The companies are small and proud, and they cannot be moved quickly to the desert.",
          ('training', 'security'), after=('guard_muster',), requires=(HasFlag('rope_teams_set'),),
          reward=(Research('land_doctrine', 0.5, 1), XP('army', 15))),
    Focus('guard_passes', 'Hold the Highland Passes',
          "The first doctrine digs the army into the mountain passes of Olastetten, where a single company can hold a "
          "valley against far larger numbers. The battalions stay in fixed posts with stored ammunition. Qesi, flat and far "
          "from the passes, is left to its police and its plant guards, and its deputies notice.",
          ('security', 'command'), after=('guard_muster',), cost=10,
          exclusive=('guard_rail_reserve', 'guard_shelter_companies'),
          reward=(SwapIdea('thin_battalions', 'pass_garrisons'), Flag('guard_doctrine'))),
    Focus('guard_rail_reserve', 'A Reserve That Rides the Trains',
          "The second doctrine keeps the battalions on their trains, with motor vehicles loaded on flat wagons, able to reach "
          "either end of either line in a day. It uses the country's one real advantage, its railway. It also means the "
          "army is only as good as the timetable, and a washout can strand it.",
          ('rail', 'security'), after=('guard_muster',), cost=10,
          exclusive=('guard_passes', 'guard_shelter_companies'),
          reward=(SwapIdea('thin_battalions', 'rail_reserve'), Flag('guard_doctrine'))),
    Focus('guard_shelter_companies', 'A Shelter Company in Every Town',
          "The third doctrine turns the army toward what it was always meant for: every town gets a trained company for "
          "rescue, shelter duty and local defence, with reservists drawn from the town itself. The country is better "
          "protected against disaster than against any army. Training never stops, and neither does the paperwork.",
          ('shelter', 'training'), after=('guard_muster',), cost=10,
          exclusive=('guard_passes', 'guard_rail_reserve'),
          reward=(SwapIdea('thin_battalions', 'shelter_companies'), Flag('guard_doctrine'))),
    Focus('guard_mud', 'Drill for the Mud Months',
          "Rain falls on nearly half the days of the year and the roads are rarely dry, yet the army still trains as though "
          "they were. Exercises move into the wet weeks: marches in mud, supply runs on flooded tracks and digging in "
          "waterlogged ground. Soldiers hate it. Vehicles break, and the staff learns which ones.",
          ('training', 'logistics'), after=('guard_muster',), reward=(Idea('mud_drill'),)),
    Focus('guard_guns', 'Guns for a Small Army',
          "Army doctrine favours firepower over numbers, because Luremia will never have the numbers. A few batteries trained "
          "to fire from the hills, with observers on the ridgelines, multiply what four battalions can hold. The guns come "
          "from abroad and are dear, and the crews take two years to train properly.",
          ('missile', 'command'), after=('guard_mud',), reward=(Research('artillery', 0.5, 1), XP('army', 20))),
    Focus('guard_line_depots', 'Replacement Depots on the Line',
          "Whichever doctrine the staff chose, the battalions need replacements close at hand. Depots at the stations of "
          "both railway lines hold equipment, rations and fuel for a month of operations. Stations get busier and harder to "
          "guard. The army gets a supply chain that runs on the one network the country actually controls.",
          ('logistics', 'rail'), after_any=('guard_passes', 'guard_rail_reserve', 'guard_shelter_companies'),
          requires=(HasFlag('guard_doctrine'),), reward=(Idea('line_depots'),)),
))

SKY = Branch('sky', 'One Airfield in the Rain', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('sky_weather', 'A Weather Office at the Airfield',
          "The only air base in Luremia, at Knadorf, has no combat aircraft and a tower full of instruments that farmers "
          "rely on for rain forecasts. Turning the tower into a proper weather office, with trained forecasters and a radio "
          "bulletin, serves the farms, the railway and any future pilot at once. It postpones the harder question.",
          ('telescope', 'runway'), reward=(Idea('weather_office'), Event('airfield_question'))),
    Focus('sky_runway', 'Drain the Knadorf Runway',
          "The runway at Knadorf floods in heavy rain and closes for days at a time. Engineers lay drainage beneath it, "
          "lengthen it and pave a second apron for transport aircraft. The work takes a dry season that the farmers would "
          "rather have used for harvest traffic. The field becomes usable all year.",
          ('runway', 'tools'), after=('sky_weather',), reward=(Build('air_base', 1, 226),)),
    Focus('sky_trainers', 'Lease Trainers for a Flying School',
          "One faction wants a flying school: leased trainer aircraft, contract instructors and a first class of Luremian "
          "pilots. It would give the country people who can fly, even without aircraft to fight with. The leases are "
          "expensive, the instructors foreign, and the first graduates have nothing to fly when they finish.",
          ('air', 'training'), after=('sky_runway',), cost=10, exclusive=('sky_observers',),
          reward=(Idea('flying_school'), Flag('sky_school'))),
    Focus('sky_observers', 'Observers on Every Ridge',
          "The other faction would rather see than fly. Volunteer observer posts on the high ground, linked by telephone to "
          "a radar set at Knadorf, would report every aircraft over Luremian hills. It is cheap, practical and uses the "
          "terrain. It gives the country nothing to send up if it ever sees something it dislikes.",
          ('radar', 'security'), after=('sky_runway',), cost=10, exclusive=('sky_trainers',),
          reward=(Idea('ridge_observers'), Build('radar_station', 1, 226))),
    Focus('sky_dry_days', 'Flying Days in the Dry Weeks',
          "The flying school schedules its training into the drier weeks of the year and builds a second hangar row and "
          "fuel store so that every clear day is used. Instructors fly long hours and students solo sooner. When the rain "
          "returns, the classroom takes over, and the hangars hold aircraft nobody owns.",
          ('air', 'runway'), after=('sky_trainers',), requires=(HasFlag('sky_school'),),
          reward=(Build('air_base', 1, 0), XP('air', 20))),
    Focus('sky_mast', 'Radar Above the Mountain Depot',
          "A radar set on the mountain above the railway depot can see across the frontiers in a way nothing at Knadorf can. "
          "The mast needs a road, a power line and a crew who will live on a mountain. Neighbours are told in advance what it "
          "is for, and the weather office claims a share of its data.",
          ('radar', 'telescope'), after=('sky_runway',),
          reward=(Build('radar_station', 1, 226), Research('radar_tech', 0.5, 1))),
    Focus('sky_qesi_strip', 'An Emergency Strip at Qesi',
          "Qesi has no airfield at all, and when the line from Knadorf washes out the desert province is cut off. A graded "
          "emergency strip near the plants, with a fuel store and a windsock, lets transport aircraft land medicine and "
          "spares in a crisis. Most weeks nothing lands there except dust.",
          ('runway', 'medical'), after=('sky_runway',), reward=(Build('air_base', 1, 231), XP('air', 10))),
))

FOUR = Branch('four', 'Four Neighbours and No Shore', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('four_offices', 'Liaison Offices on Four Frontiers',
          "Luremia touches Kaluga, Glaceland, Sfaenland and Silvonia and no sea at all, and its relations with each have been "
          "handled by whichever ministry had a problem that week. A liaison office at the main crossing toward each "
          "neighbour, with its own staff and files, gives every frontier a known door. The offices cost little and promise "
          "less.",
          ('diplomacy', 'document'), reward=(Idea('frontier_liaison'), Event('four_frontiers'))),
    Focus('four_kaluga', 'Forest Wardens on the Kaluga Line',
          "The frontier with Kaluga runs through the forest beyond Knadorf and the two mountain provinces, and fires, poachers and lost "
          "walkers cross it without asking. Luremian forest wardens patrol their own side and keep a telephone number for "
          "their counterparts. No claim or line changes. Incidents get a phone call instead of a protest note.",
          ('peace', 'security'), after=('four_offices',),
          reward=(Flag('kaluga_wardens'), Tooltip('No border or claim changes; the wardens patrol the Luremian side only.'))),
    Focus('four_valleys', 'Our Side of the Valley Paths',
          "Herders and foresters from the Glacelandic frontier districts have crossed into the Olastetten hills along the "
          "valley paths for generations. Luremian village councils start a register of who comes, when and with how many "
          "animals, and offer a named contact for disputes. The register is Luremian paperwork only; it moves no line on any map.",
          ('document', 'civil'), after=('four_offices',),
          reward=(Flag('herder_register'), Stability(0.02),
                  Tooltip('No border or claim changes; the register covers grazing and timber on the Luremian side.'))),
    Focus('four_desert_road', 'Customs on the Desert Road',
          "Desert traders have taken the road from Qesi toward Sfaenland for years with little paperwork. Customs posts at "
          "the crossings now collect duty and count the traffic. Revenue rises and the plants learn what actually comes in. "
          "Traders lose a day at the post, and some of them find other roads.",
          ('document', 'logistics'), after=('four_offices',), reward=(TimedIdea('desert_customs', 1095),)),
    Focus('four_silvonia', 'The Silvonia Corner',
          "Silvonia meets Luremia in the far corner of the country, along one mountain province and one desert province "
          "that the capital rarely visits. A radar post and a small army camp near the desert crossing put the corner on "
          "the map of the ministries. Soldiers posted there count the days to their next leave by train.",
          ('radar', 'security'), after=('four_offices',), reward=(Build('radar_station', 1, 231), XP('army', 10))),
    Focus('four_neutral', 'Neutrality in the Statute Book',
          "One answer to four neighbours is to write permanent neutrality into law: no alliance, no foreign bases and an "
          "army sized to defend the country and nothing more. It reassures every neighbour equally and binds every future "
          "government. It also closes options that a small country might one day badly want.",
          ('peace', 'scales'), after_any=('four_kaluga', 'four_valleys', 'four_desert_road', 'four_silvonia'), cost=10,
          exclusive=('four_unwritten',), reward=(SwapIdea('frontier_liaison', 'declared_neutrality'),)),
    Focus('four_unwritten', 'Promise Nothing in Writing',
          "The other answer is to stay friendly with all four neighbours while signing nothing that limits Luremia's freedom. "
          "Diplomats say warm words in every capital and initial no texts. The country keeps every option open. Its "
          "neighbours keep guessing, and some of them find guessing tiresome.",
          ('diplomacy', 'command'), after_any=('four_kaluga', 'four_valleys', 'four_desert_road', 'four_silvonia'),
          cost=10, exclusive=('four_neutral',), reward=(SwapIdea('frontier_liaison', 'unwritten_options'),)),
    Focus('four_monitors', 'When the Neighbours Do Not Vote',
          "None of Luremia's four neighbours is holding elections, and in three of them nationalist movements hold half the "
          "voters. Any turn in their politics could reach the frontier quickly. A small office in Knadorf reads their "
          "press and listens to their radio every day. The wardens on the Kaluga line already know the habit.",
          ('communications', 'document'), after_any=('four_neutral', 'four_unwritten'),
          requires=(HasFlag('kaluga_wardens'),), reward=(Idea('frontier_monitors'),)),
    Focus('four_grazing', 'Seasonal Grazing Fees',
          "With the herders registered, the village councils charge a small fee for each season on Luremian pastures and "
          "spend it on wells and path repairs. Herders grumble and pay, because the paths are better. The fees are "
          "Luremian rules on Luremian land and change nothing about who may cross.",
          ('scales', 'civil'), after=('four_valleys',), requires=(HasFlag('herder_register'),),
          reward=(TimedIdea('grazing_fees', 1095),)),
))

ROCK = Branch('rock', 'Ulysses and the Olastetten Rock', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('rock_bulletin', 'The Sky Bulletin from Knadorf',
          "In December 1994 astronomers announce that the asteroid Ulysses may strike the Earth. Luremia can do nothing about "
          "the asteroid and a great deal about rumour. The Knadorf radio starts a weekly bulletin saying plainly what is "
          "known and what is not. The bulletin costs airtime and political nerve.",
          ('meteor', 'communications'), requires=(After('1994.12.10'),), reward=(Idea('sky_bulletin'), PP(-10))),
    Focus('rock_impact', 'When the Impact Is Announced',
          "In April 1996 the FCU announces that Ulysses will strike the Earth. Where the fragments will fall is not known and "
          "may not be known until late. A country whose army exists for civil defence now has to decide what civil defence "
          "means against a falling sky. The cabinet sits through the night.",
          ('meteor', 'command'), after=('rock_bulletin',), requires=(After('1996.4.20'),), reward=(Event('impact_word'),)),
    Focus('rock_galleries_path', 'Cut Galleries into the Hills',
          "The engineers propose shelter in the rock: galleries cut into the hills and mountains of Olastetten, close to the "
          "towns, ventilated and stocked. The rock is solid and the work is hard. Qesi, flat and far away, would have to "
          "send its people up the line to reach them.",
          ('shelter', 'tools'), after=('rock_impact',), cost=10, exclusive=('rock_rail_path',),
          reward=(Idea('rock_galleries'), Flag('rock_shelters'))),
    Focus('rock_rail_path', 'Disperse by Rail Between Provinces',
          "The railway officers propose movement instead of concrete: a plan to carry whole towns by train from one province "
          "to the other, toward whichever looks safer when the warnings come. It uses the two lines the country already has. "
          "It depends on warnings arriving in time and on the lines surviving the rain.",
          ('rail', 'refugees'), after=('rock_impact',), cost=10, exclusive=('rock_galleries_path',),
          reward=(Idea('evacuation_trains'), Flag('rail_evacuation'))),
    Focus('rock_deep', 'The Deep Galleries Under Knadorf',
          "The largest galleries are driven beneath the capital itself, with ventilation shafts, water tanks and room for "
          "most of Knadorf's families. Tunnelling crews work in shifts for three years. The spoil goes into the railway "
          "embankments. When finished, the galleries are the largest public work the country has ever paid for.",
          ('shelter', 'civil'), after=('rock_galleries_path',), requires=(HasFlag('rock_shelters'),),
          reward=(SwapIdea('rock_galleries', 'deep_galleries'),)),
    Focus('rock_leaving', 'Timetables for Leaving',
          "Every town gets an evacuation timetable: which train, which platform, which hour, and which families. The "
          "timetables are posted in schools and rehearsed twice a year, in daylight and in the dark. Rehearsals disrupt the "
          "freight schedule and annoy the plant managers, who lose a shift each time. On the third rehearsal every train "
          "leaves on time, and the towns stop treating the exercise as a holiday.",
          ('rail', 'shelter'), after=('rock_rail_path',), requires=(HasFlag('rail_evacuation'),),
          reward=(SwapIdea('evacuation_trains', 'evacuation_drilled'),)),
    Focus('rock_stores', 'Ninety Days of Stores',
          "Whatever the plan, people will need food, water and medicine if the worst happens. Every district lays in grain, "
          "water and medical supplies for three months, rotated each year. The stores are expensive to fill and dull to "
          "guard. They are also the only part of the plan that every faction supports.",
          ('shelter', 'economy'), after=('rock_impact',), reward=(TimedIdea('shelter_stores', 1460),)),
    Focus('rock_clinics', 'Mountain Clinics Join the Plan',
          "The clinic at the mountain depot becomes the model for the emergency plan: small medical posts at every station "
          "and shelter, stocked and staffed in rotation from Knadorf. Doctors are scarce and the rotations are long, and the "
          "capital hospital loses staff for weeks at a time. Every town now knows where to take its injured.",
          ('medical', 'shelter'), after=('rock_impact',), requires=(HasFlag('mountain_clinic'),),
          reward=(Stability(0.03), Research('construction_tech', 0.5, 1))),
    Focus('rock_rehearsal', 'The Battalions Rehearse the Night',
          "The battalions, whatever doctrine they now follow, rehearse their part in the emergency plan: guarding stores, "
          "directing crowds and keeping roads and platforms clear in the dark. The rehearsals run at night, in the rain, "
          "with towns watching. Officers learn that civilians follow calm orders and ignore shouted ones.",
          ('training', 'shelter'), after_any=('rock_galleries_path', 'rock_rail_path'), requires=(HasFlag('guard_doctrine'),),
          reward=(XP('army', 15), WarSupport(0.02))),
    Focus('rock_roche', 'Waiting Out the Roche Night',
          "On 8 July 1999 Ulysses passes through the Roche limit. Luremia spends the night as it planned to: in galleries, "
          "on trains or in cellars, with wardens on the streets and the radio on the air. What falls, and where, is not "
          "known in advance. By morning the cabinet must decide how long to wait.",
          ('meteor', 'shelter'), after_any=('rock_deep', 'rock_leaving', 'rock_stores'), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('rock_daylight', 'Open the Galleries to Daylight',
          "Once the fragment showers have ended, the country counts what its preparations cost and what they achieved. "
          "Stores are released to the shops, the trains go back to freight and the weekly bulletin closes. Some officials "
          "want the emergency apparatus kept forever. Most families just want to sleep upstairs again.",
          ('rebuild', 'civil'), after=('rock_roche',), reward=(RemoveIdea('sky_bulletin'), Stability(0.03))),
))

FAR = Branch('far', 'Wars Beyond Every Frontier', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('far_belka', 'Prices from the Belkan War',
          "In March 1995 war breaks out around Belka. No Luremian frontier touches it, but fuel, machinery and freight "
          "insurance all cost more within weeks, and the arms works receive letters from unfamiliar buyers. The cabinet "
          "studies what the war will cost a small country that only wants to buy and sell in peace.",
          ('diplomacy', 'economy'), requires=(After('1995.3.25'),), reward=(Event('belkan_prices'),)),
    Focus('far_rations', 'Ration Cards for Fuel',
          "With fuel prices climbing, the ministry issues ration cards for private motoring so that the plants, the railway "
          "and the army keep their supply. Queues form at every filling station. The cards are unpopular, fair and "
          "temporary, and the ministry promises they will go the day prices fall.",
          ('document', 'economy'), after=('far_belka',), reward=(TimedIdea('fuel_cards', 365),)),
    Focus('far_spares', 'Spares for Buyers Far from War',
          "The arms works want to answer the new letters by selling spare parts and replacement kit to buyers far from any "
          "war zone, under licence and with end-user checks. Orders would fill the night shifts. Every licence is a "
          "judgement call, and a mistaken one could follow Luremia for decades.",
          ('industry', 'diplomacy'), after=('far_belka',), cost=10, exclusive=('far_rifles',),
          reward=(Idea('spares_licence'),)),
    Focus('far_rifles', 'Every Rifle Stays at Home',
          "The opposite answer forbids every military export while wars are being fought anywhere. The arms works keep "
          "their output for the four battalions and their reserves. Night shifts are cut, and managers complain about lost "
          "orders. Nobody abroad has any reason to think of Luremia as a supplier.",
          ('peace', 'security'), after=('far_belka',), cost=10, exclusive=('far_spares',),
          reward=(Idea('rifles_home'),)),
    Focus('far_lumen', 'The Lumen Treaty Read Aloud',
          "When word comes that the Belkan War is over and a treaty has been signed in Lumen, the Knadorf radio reads the "
          "news at noon and the ministry withdraws the fuel ration cards within the month, as it promised. Prices fall "
          "slowly. The cabinet keeps its study of what the war cost, because the next distant war will cost the same.",
          ('peace', 'document'), after=('far_belka',), requires=(After('1995.6.20'), HasGlobal('belka_lost_belkan_war')),
          reward=(RemoveIdea('fuel_cards'), Stability(0.02))),
    Focus('far_clause_desk', 'A Desk for War Clauses',
          "The Belkan War taught the freight office that insurers write war clauses faster than ministries can read them. A "
          "permanent desk in Knadorf negotiates those clauses for every Luremian charter, tracks premiums and finds "
          "alternative routes. It is a small office with an unglamorous job and a long memory.",
          ('logistics', 'scales'), after_any=('far_spares', 'far_rifles'), requires=(After('2001.1.1'),),
          reward=(Idea('war_clause_desk'),)),
    Focus('far_isaf', 'Freight Rates and the ISAF',
          "When the ISAF is formed to oppose Erusea, the war in Usea becomes a freight problem for every country with cargo "
          "on the oceans. Luremia has no frontier in Usea and takes no side, but its charters face new clauses within a "
          "week. The war-clause desk is ready for exactly this.",
          ('logistics', 'communications'), after=('far_clause_desk',), requires=(HasGlobal('ac_ucw_isaf_formed'),),
          reward=(Event('usean_freight'),)),
    Focus('far_rates_fall', 'Charter Rates Come Down',
          "Once the fighting in Usea is over, however it has ended, insurers withdraw their war clauses one contract at a "
          "time and charter rates drift back toward their old levels. The desk in Knadorf stays open, renamed and smaller, "
          "because Luremia has learned that distant wars always find their way back to its shelves.",
          ('economy', 'peace'), after=('far_isaf',), requires=(After('2005.9.19'),),
          reward=(SwapIdea('war_clause_desk', 'peace_rates'),)),
))

BRANCHES = (BALLOT, HILLS, QESI, WORKS, RAIL, GUARD, SKY, FOUR, ROCK, FAR)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('drain_crews', 'Clear the Drains Before the Rains',
                'Sends paid crews to clear every culvert and gutter in Knadorf ahead of the next heavy rain. Repeatable once a year.',
                25, (TimedIdea('drain_crews', 120),), requires=(Completed('hill_drains'),), cooldown=365),
    DecisionDef('gallery_week', 'Open the Galleries for a Week',
                'Invites families into the rock shelters for a week of drills and familiarisation. Repeatable once a year; '
                'the plants lose some shifts.',
                30, (TimedIdea('gallery_week', 60),), requires=(HasFlag('rock_shelters'),), cooldown=365),
    DecisionDef('hardstands', 'Lay Hardstands at Knadorf Field',
                'Concrete parking pads and a taxiway beside the drained Knadorf runway, so that aircraft are not left '
                'standing in mud through the rains. Done once; the crews then return to the roads.',
                60, (Build('air_base', 1, 0),), requires=(Completed('sky_runway'),)),
    DecisionDef('qesi_mast', 'Raise a Radar Mast over Qesi',
                'Raises a radar mast beside the Qesi emergency strip so the desert approaches are watched as well as the '
                'hills. Paid for once out of the airfield money.',
                60, (Build('radar_station', 1, 231),), requires=(Completed('sky_qesi_strip'),)),
    DecisionDef('reserve_train', 'Run the Reserve Train',
                'Sends one reserve company along both lines on an exercise timetable for three months. Repeatable once a year; '
                'freight runs late while it does.',
                35, (TimedIdea('reserve_train_run', 90), XP('army', 10)), requires=(Completed('guard_rail_reserve'),),
                cooldown=365),
    DecisionDef('market_week', 'A Frontier Market Week',
                'Opens the liaison offices to traders from all four neighbours for a market week. Repeatable once a year.',
                20, (Stability(0.02), PP(10)), requires=(Completed('four_offices'),), cooldown=365),
)
