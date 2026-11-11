"""Wellow (WEL): bespoke national focus tree, era 1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (a democratic ruling party
with elections disallowed, popularities of 50 fascism, 48 neutrality, 1 democratic and
1 communism), the unnamed National Administration office, the country names in
localisation, the world-start calibration (role, industry, 932 convoys) and the map.
Official: ACES Chronicle rows used only as date anchors for regional pressure; no
Wellowan role in any of them is claimed. Everything else, including every Wellowan
choice, office, idea, building, flag and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='WEL', name='Wellow', root='world', package='wel',
                  themes=('navy', 'logistics', 'assembly'), max_columns=35)

ERAS = ('e1',)
SCHEMA = 2

SOURCES = (
    Source('Mod provenance',
           'Inherited Wellow history: capital state 247; ruling_party democratic with elections_allowed = no; popularities '
           'neutrality 48, fascism 50, democratic 1, communism 1; stability and war support 0.5; leader is the unnamed '
           'WEL_ac_government_office (National Administration), whose 1991 holder is not established. The tree reads these '
           'numbers as political pressure and does not claim when or why the election calendar stopped.',
           'mod/2985041246/history/countries/WEL - Wellow.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Country names per party: Republic of Wellow (democratic), Wellowan Empire (fascism), United Kingdom of Wellow '
           '(neutrality and monarchism), Union of Wellow (communism); adjective Wellowan. The four political answers follow '
           'these names; offices are collective and unnamed.',
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 5, 17, 96, 100, 131, 175, 244, 245, 246, 247 (capital), 248, 250, 253, 255, 264 and 266 on '
           'the wellow continent. States 5 and 244 to 266 form one contiguous main island; 17, 96, 100 and 131 are separate '
           'island districts to the west and 175 a small islet to the southeast. No land neighbours; the nearest foreign coast '
           'is Belka to the south, then FATO and Gebet, computed from map/provinces.bmp. The capital state is the only inland '
           'state. Terrain (hills, marsh, mountain, plains) comes from map/definition.csv. District labels are provisional and '
           'are not used as place names.',
           'mod/2985041246/history/states; mod/2985041246/map/definition.csv; mod/2985041246/map/continent.txt; '
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml'),
    Source('Mod provenance',
           'Starting economy and forces: 16 civilian, 8 military and 6 dockyard levels (the six dockyards all in state 253); air '
           'bases in states 5 and 247; a fuel silo in the capital; oil 44 and steel 38 from states 5, 247 and 250; 932 convoys; '
           'about ten infantry formations, a coastal escort and submarine navy, a small fighter and support air arm; grand '
           'doctrines superior_firepower, fleet_in_being and operational_integrity; role dispersed maritime trade. These are '
           'gameplay calibration, not canon national accounts.',
           'tools/world_foundation/country_registry.json (WEL); tools/world_starts/profiles.json (WEL); '
           'docs/WORLD_STARTS_CALIBRATION.md'),
    Source('Official', 'Date anchor: Belka sells northern territory to FATO and cedes northern islands and the Great Lakes '
           'region to Osea. Used for the strait branch opening; no Wellowan role is claimed.', '1991 / 08.29'),
    Source('Official', 'Date anchor: Belkan borders are redrawn. Used only as the earliest date of a study focus.', '1991 / 12.16'),
    Source('Official', 'Date anchor: the IAU announces that Ulysses may strike the Earth. Wellowan preparations are gameplay.',
           '1994 / 12.10'),
    Source('Official', 'Date anchor: the Belkan War breaks out. Wellow is not a party; its posture is gameplay.', '1995 / 03.25'),
    Source('Official', 'Date anchor: the Belkan Army uses nuclear devices in the Waldreich Mountains. The Wellowan fallout watch '
           'is gameplay and also requires the mod global flag belka_dropped_nukes.', '1995 / 06.06'),
    Source('Official', 'Date anchor: the treaty signed in Lumen ends the Belkan War.', '1995 / 06.20'),
    Source('Official', 'Date anchor: the FCU announces that Ulysses will strike the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor: former top Belkan Air Force pilots are hired by various countries as aggressor squadrons. '
           'The Wellowan offer is gameplay; Wellow is not claimed to be one of those countries.', '1998 / 06.19'),
    Source('Official', 'Date anchor: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor: Osea, Emmeria and other nations join sanctions against Estovakia. Wellow is not claimed '
           'among them; the registry choice is gameplay.', '2002 / 03.20'),
    Source('Official', 'Date anchor: the FCU demands that Erusea withdraw from the railgun complex and San Salvacion, and the '
           'ISAF is established.', '2003 / 08.22'),
    Source('Official', 'Date anchor: Farbanti falls and the Continental War ends; used for the closing review.', '2005 / 09.19'),
    Source('Provisional gameplay',
           'All Wellowan focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects. Campaign hooks read only mod '
           'global flags (belka_dropped_nukes, belka_lost_belkan_war, belka_won_belkan_war).'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the question of government
    IdeaDef('caretaker_mandate', 'The Caretaker Mandate', 'The National Administration governs by ordinance, with no election calendar and almost no party behind it.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('command', 'document')),
    IdeaDef('port_hearings', 'The Port Town Hearings', 'Commissioners have heard every district; the record is public and unflattering.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05}, ('assembly', 'navy')),
    IdeaDef('electoral_rolls', 'Rolls Reopened', 'District clerks are rebuilding the voter rolls for a restored chamber.',
            {'stability_factor': 0.03, 'political_power_gain': -0.05, 'research_speed_factor': 0.02}, ('ballot', 'document')),
    IdeaDef('union_commission', 'The Crown in Commission', 'The union camp proposes a crown exercised collectively by a council of the districts.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('assembly', 'medal')),
    IdeaDef('imperial_petition', 'The Imperial Petition', 'Petition committees of the imperial movement sit in every port town.',
            {'war_support_factor': 0.06, 'stability_factor': -0.02, 'political_power_gain': 0.10}, ('medal', 'security')),
    IdeaDef('standing_ordinances', 'Standing Ordinances', 'Emergency ordinances are being turned into a permanent administrative code.',
            {'political_power_gain': 0.15, 'stability_factor': 0.02}, ('document', 'scales')),
    IdeaDef('open_chamber', 'The Broadcast Chamber', 'Chamber sessions reach every district by radio; ministers answer in public.',
            {'stability_factor': 0.07, 'political_power_factor': 0.05, 'research_speed_factor': 0.02}, ('ballot', 'communications')),
    IdeaDef('union_settlement', 'The Union Settlement', 'Written charters fix each district share of port dues and its council seat.',
            {'stability_factor': 0.08, 'production_speed_infrastructure_factor': 0.10}, ('assembly', 'scales')),
    IdeaDef('imperial_order', 'The Imperial Order', 'Decrees, party newspapers and a fleet the directorate parades at every chance.',
            {'war_support_factor': 0.10, 'stability_factor': 0.04, 'navy_org_factor': 0.05}, ('security', 'navy')),
    IdeaDef('coded_state', 'The Coded Administration', 'An administrative court holds the government to its own written code.',
            {'stability_factor': 0.06, 'political_power_gain': 0.15, 'production_factory_efficiency_gain_factor': 0.03}, ('scales', 'document')),
    # the scattered districts
    IdeaDef('district_survey', 'The District Survey', 'Every pier, road, school and tax office in sixteen districts is on file.',
            {'production_speed_infrastructure_factor': 0.10}, ('document', 'civil')),
    IdeaDef('ferry_compact', 'The Ferry Compact', 'Subsidised ferries link every island district to the main island on fixed days.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.05}, ('navy', 'logistics')),
    IdeaDef('island_councils', 'Island District Councils', 'Elected councils hold budgets for piers, schools and roads in the outer districts.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.15}, ('assembly', 'civil')),
    IdeaDef('island_prefecture', 'The Island Prefecture', 'One prefecture staffed from the capital governs every outer district.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.05}, ('command', 'navy')),
    IdeaDef('winter_ferries', 'Winter Ferry Subsidy', 'Extra sailings keep the islands supplied through the storm season.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.05}, ('navy', 'shelter')),
    # the merchant register
    IdeaDef('merchant_register', 'The Merchant Register', 'More than nine hundred hulls, counted and owing dues to a harbour office.',
            {'consumer_goods_factor': -0.02, 'political_power_gain': 0.05}, ('logistics', 'document')),
    IdeaDef('open_registry', 'The Open Registry', 'Any owner may fly the Wellowan flag for a fee and a light inspection.',
            {'consumer_goods_factor': -0.06, 'stability_factor': -0.02}, ('logistics', 'economy')),
    IdeaDef('national_line', 'The National Line', 'State-held shipping houses run fixed routes with Wellowan crews and yards.',
            {'consumer_goods_factor': -0.03, 'naval_coordination': 0.05, 'industrial_capacity_dockyard': 0.04}, ('navy', 'command')),
    IdeaDef('owners_mutual', 'The Shipowners Mutual', 'Owners pool insurance, repair budgets and a common rate book under supervision.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.03}, ('logistics', 'scales')),
    IdeaDef('convoy_discipline', 'Convoy Discipline', 'Every master carries sealed wartime instructions and knows the assembly ports.',
            {'naval_coordination': 0.05, 'naval_speed_factor': 0.04}, ('navy', 'document')),
    IdeaDef('exchange_commissions', 'Commissions Kept at Home', 'A shipping exchange in the capital keeps charter commissions in Wellowan hands.',
            {'consumer_goods_factor': -0.03, 'political_power_gain': 0.05}, ('economy', 'communications')),
    # oil and steel
    IdeaDef('field_ledger', 'The Field Ledger', 'Every well, mine and furnace is recorded with its output and its losses.',
            {'production_speed_buildings_factor': 0.04}, ('industry', 'document')),
    IdeaDef('home_refining', 'Refined at Home', 'Crude is refined in Wellowan plants; the fleet and the ferries are served first.',
            {'production_speed_industrial_complex_factor': 0.10, 'supply_consumption_factor': -0.05}, ('industry', 'tools')),
    IdeaDef('crude_exports', 'Crude by Tanker', 'Crude sails abroad in Wellowan tankers and finished fuel is bought back.',
            {'consumer_goods_factor': -0.05, 'political_power_gain': 0.05}, ('logistics', 'economy')),
    IdeaDef('steel_plate', 'Steel Before Oil', 'Oil money builds rolling mills, ship plate and rails before new wells.',
            {'production_factory_efficiency_gain_factor': 0.05, 'industrial_capacity_factory': 0.04}, ('industry', 'rail')),
    IdeaDef('fuel_drawn', 'Fuel Drawn from Reserve', 'The capital reserve is open; ferries, heating plants and the fleet draw on it.',
            {'stability_factor': 0.03, 'supply_consumption_factor': -0.08}, ('logistics', 'shelter')),
    # the dockyard district
    IdeaDef('six_slips', 'Six Slips for a Nation', 'Every slip in the dockyard district is contested by the navy, the owners and the repair crews.',
            {'industrial_capacity_dockyard': 0.03}, ('navy', 'tools')),
    IdeaDef('apprentice_intake', 'The Apprentice Intake', 'Four-year apprentices learn riveting and welding beside the retiring crews.',
            {'industrial_capacity_dockyard': 0.05, 'production_speed_buildings_factor': 0.03}, ('training', 'tools')),
    IdeaDef('escort_slips', 'Escorts on the Slips', 'The yards lay down escorts first; merchant work waits.',
            {'industrial_capacity_dockyard': 0.06, 'navy_org_factor': 0.04}, ('navy', 'security')),
    IdeaDef('merchant_slips', 'Merchant Hulls First', 'Coasters, ferries and colliers take the slips; warships wait.',
            {'industrial_capacity_dockyard': 0.05, 'consumer_goods_factor': -0.03}, ('logistics', 'tools')),
    IdeaDef('repair_basins', 'Repair Before New Keels', 'The slips are cleared for repair work that once went to foreign yards.',
            {'repair_speed_factor': 0.12, 'industrial_capacity_dockyard': 0.03}, ('rebuild', 'navy')),
    IdeaDef('standard_hulls', 'One Hull, Many Uses', 'A single standard hull serves as coaster, ferry and patrol vessel.',
            {'industrial_capacity_dockyard': 0.06, 'production_factory_efficiency_gain_factor': 0.03}, ('tools', 'navy')),
    IdeaDef('yard_wage_board', 'The Slipway Wage Board', 'Wages on the slips are set by a board of owners, unions and the ministry.',
            {'stability_factor': 0.03, 'industrial_capacity_dockyard': 0.03}, ('scales', 'tools')),
    # the fleet
    IdeaDef('harbour_fleet', 'The Fleet Kept in Harbour', 'A coastal navy trained to survive rather than to win battles.',
            {'navy_org_factor': 0.04}, ('navy', 'shelter')),
    IdeaDef('sound_patrols', 'Patrols in the Island Sounds', 'Small submarines lie in the channels between the islands.',
            {'naval_coordination': 0.06, 'navy_org_factor': 0.05}, ('submarine', 'navy')),
    IdeaDef('escort_screen', 'The Merchant Lane Screen', 'Escorts organised around the merchant lanes rather than the harbours.',
            {'naval_speed_factor': 0.05, 'naval_coordination': 0.05}, ('navy', 'logistics')),
    IdeaDef('island_squadrons', 'A Squadron for Every Island', 'Each island group keeps its own small squadron and repair crew.',
            {'navy_org_factor': 0.08, 'repair_speed_factor': 0.08}, ('navy', 'rebuild')),
    IdeaDef('imperial_programme', 'The Imperial Naval Programme', 'The directorate funds new escorts and a recruiting drive in every port.',
            {'navy_org_factor': 0.06, 'industrial_capacity_dockyard': 0.05, 'war_support_factor': 0.03}, ('navy', 'medal')),
    # the air arm
    IdeaDef('air_census', 'The Air Arm Count', 'Aircraft, crews and spare parts counted; the flying hours are honest at last.',
            {'experience_gain_air_factor': 0.05}, ('air', 'document')),
    IdeaDef('strait_interceptors', 'Interceptors over the Narrow Sea', 'An air arm built to deny the southern approaches.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('sea_patrol_wing', 'Eyes over the Sea Lanes', 'An air arm built to watch the merchant lanes and the island sounds.',
            {'air_mission_efficiency': 0.08, 'naval_coordination': 0.03}, ('air', 'navy')),
    IdeaDef('aggressor_school', 'The Contract Aggressor School', 'Hired instructors fly as the enemy so that Wellowan pilots learn to fight one.',
            {'experience_gain_air_factor': 0.12, 'air_superiority_efficiency': 0.04}, ('air', 'training')),
    # across the narrow sea
    IdeaDef('strait_watch', 'Watch on the Narrow Sea', 'Radar posts, lookouts and patrol boats face the Belkan coast.',
            {'air_detection': 0.05, 'army_core_defence_factor': 0.05}, ('radar', 'security')),
    IdeaDef('closed_ports', 'Ports Closed to Warships', 'No belligerent warship or military aircraft may use a Wellowan port or field.',
            {'army_core_defence_factor': 0.08, 'stability_factor': 0.04}, ('security', 'peace')),
    IdeaDef('open_ports', 'Neutral Ports, Open Trade', 'Merchant ships of every flag trade freely; war cargo pays a premium.',
            {'consumer_goods_factor': -0.05, 'stability_factor': -0.02}, ('logistics', 'peace')),
    IdeaDef('fallout_watch', 'The Fallout Watch', 'Meteorologists and sampling stations track the winds from the south.',
            {'stability_factor': 0.03, 'air_detection': 0.05}, ('science', 'radar')),
    IdeaDef('postwar_lanes', 'Lanes Reopened', 'Insurers return and the southern routes fill again after the Lumen treaty.',
            {'consumer_goods_factor': -0.04, 'stability_factor': 0.02}, ('logistics', 'peace')),
    IdeaDef('strait_trade', 'Trade Across the Narrow Sea', 'Wellowan ships carry fuel, food and timber to a defeated neighbour.',
            {'consumer_goods_factor': -0.04, 'production_speed_buildings_factor': 0.04}, ('diplomacy', 'logistics')),
    IdeaDef('strait_vigil', 'The Southern Vigil', 'A permanent watch on a victorious neighbour across the narrow sea.',
            {'army_core_defence_factor': 0.10, 'war_support_factor': 0.04}, ('security', 'radar')),
    # the garrison
    IdeaDef('garrison_review', 'The Garrison Review', 'The army knows where it stands and how it would move by sea.',
            {'army_org_factor': 0.03}, ('command', 'document')),
    IdeaDef('district_battalions', 'A Battalion in Every District', 'Every district, island or not, keeps its own trained battalion.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.05}, ('security', 'civil')),
    IdeaDef('sealift_brigades', 'Brigades That Travel by Sea', 'Fewer, better brigades trained to embark on ferries and colliers.',
            {'army_speed_factor': 0.05, 'army_org_factor': 0.05, 'planning_speed': 0.05}, ('training', 'navy')),
    IdeaDef('district_guards', 'District Guards of the Union', 'Guards answerable jointly to the union council and each district.',
            {'army_core_defence_factor': 0.06, 'stability_factor': 0.03}, ('security', 'assembly')),
    # the falling sky
    IdeaDef('sky_watch', 'The Sky Watch', 'Telescopes and radar on the northern lowland report to a standing committee.',
            {'air_detection': 0.08}, ('telescope', 'radar')),
    IdeaDef('grain_reserve', 'The Grain Reserve', 'Granaries on the northern lowland hold a winter of food for the islands.',
            {'stability_factor': 0.05}, ('shelter', 'civil')),
    IdeaDef('impact_year', 'Preparing for the Impact', 'Every district has an impact plan, a shelter list and a ferry schedule.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03}, ('meteor', 'shelter')),
    IdeaDef('relief_charters', 'Relief Charters', 'Owners lend hulls at cost to carry relief wherever the fragments fall.',
            {'stability_factor': 0.03, 'political_power_gain': 0.05}, ('refugees', 'navy')),
    IdeaDef('name_at_sea', 'A Name at Sea', 'Relief voyages in the impact year earned the Wellowan flag a reputation money cannot buy.',
            {'stability_factor': 0.05, 'political_power_gain': 0.10}, ('medal', 'navy')),
    IdeaDef('home_waters', 'Every Hull Home', 'Merchant ships stay in home waters through the danger years.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.03}, ('shelter', 'logistics')),
    IdeaDef('evacuation_plan', 'Ferry Evacuation Plan', 'Coastal and island villages know which ferry takes them inland, and when.',
            {'stability_factor': 0.04, 'supply_consumption_factor': -0.04}, ('refugees', 'navy')),
    # the polytechnic
    IdeaDef('polytechnic', 'The Maritime Polytechnic', 'Engineers, navigators and radio technicians trained at home.',
            {'research_speed_factor': 0.04}, ('science', 'navy')),
    IdeaDef('marine_weather', 'The Marine Weather Service', 'Storm warnings broadcast to every master and ferry captain.',
            {'air_mission_efficiency': 0.05, 'naval_coordination': 0.03}, ('telescope', 'communications')),
    IdeaDef('ministry_labs', 'Ministry Laboratories', 'Research run by the ministries for the fleet, the fields and the ferries.',
            {'research_speed_factor': 0.04, 'political_power_gain': -0.05}, ('science', 'command')),
    IdeaDef('owner_labs', 'Laboratories Paid by the Owners', 'Shipowners and oil firms fund research they can use within years.',
            {'research_speed_factor': 0.03, 'production_factory_max_efficiency_factor': 0.04}, ('science', 'economy')),
    # the distant war
    IdeaDef('sanction_rules', 'Sanctions in the Register', 'Estovakian cargo is barred from Wellowan hulls by registry rule.',
            {'stability_factor': 0.02, 'political_power_gain': 0.05}, ('document', 'diplomacy')),
    IdeaDef('registry_discretion', 'The Register Keeps Its Rules', 'The registry applies its own rules and no foreign sanctions list.',
            {'consumer_goods_factor': -0.03, 'stability_factor': -0.01}, ('logistics', 'scales')),
    IdeaDef('no_war_cargo', 'No Cargo for Either Side', 'No Wellowan hull may carry military cargo to the war over Usea.',
            {'stability_factor': 0.04, 'political_power_gain': 0.05}, ('peace', 'logistics')),
    IdeaDef('war_risk_cover', 'War Risk Cover', 'A state-backed pool insures Wellowan hulls on the Usean routes.',
            {'consumer_goods_factor': -0.04, 'naval_speed_factor': 0.03}, ('economy', 'navy')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('chamber_cabinet', 'Cabinet of the Restored Chamber',
           'A cabinet drawn from the majority of an elected chamber, governing the Republic of Wellow collectively and facing '
           'the chamber on a fixed calendar. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
    Office('union_council', 'Union Council of the Districts',
           'A council of delegates from every district that holds the crown of the United Kingdom of Wellow in commission and '
           'governs collectively; no single crown holder is named. Provisional gameplay office with no named holder.',
           'neutrality', 'conservatism_na'),
    Office('imperial_directorate', 'Imperial Directorate',
           'A directorate of imperial movement committees, retired naval officers and loyal clerks governing a Wellowan Empire '
           'by decree. Provisional gameplay office with no named holder.',
           'fascism', 'ultranationalism'),
    Office('standing_administration', 'Standing Administration of the Republic',
           'The National Administration reconstituted under a written administrative charter, still without elections, '
           'governing collectively and bound by its own court. Provisional gameplay office with no named holder.',
           'democratic', 'centrism'),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('suspended_calendar', 'An Administration Without a Calendar', (
        "The National Administration begins 1991 the way it ended the previous year: governing by ordinance from offices on "
        "the capital plain, with no date set for the next election. Its own party, the one that still calls the country a "
        "republic, polls almost nobody. The ferries run, the ports collect their dues and the fleet keeps its moorings, but "
        "nobody can say on whose mandate any of it happens.",
        "Two great movements fill the space the administration leaves empty. The imperial movement, which wants a Wellowan "
        "Empire with one flag and one fleet, claims about half the electorate and fills the port-town halls with petitioners. "
        "The union camp, which wants the scattered districts bound together as a United Kingdom under a crown held by their "
        "own council, claims nearly all the rest. Both say the administration is a caretaker that has forgotten it was meant "
        "to leave.",
        "Senior officials have prepared a statement for the new year. It can promise that the question of government will be "
        "settled in public, with hearings in every district and a published record, or it can promise only continuity and ask "
        "the country to wait. Neither promise costs anything today. Both will be quoted against the administration for years.",
    ), (
        Option('Promise a public settlement.', (Stability(0.03), PP(-15))),
        Option('Promise continuity and patience.', (PP(35), Stability(-0.02))),
    ), picture=2),
    EventDef('ferry_season', 'The Ferry Season Report', (
        "The district survey comes back as a stack of ledgers from sixteen districts, and the western islands' ledgers arrive "
        "last because the ferry carrying them broke down twice. The main island has its capital plain, its industrial "
        "districts and a dockyard in the south. Beyond it lie four island districts stretching west and a small islet "
        "to the southeast, and most of them have no paved road at all.",
        "The surveyors list the same complaints in different handwriting. Piers built for fishing boats now carry freight. "
        "Schools close when the ferry misses a week. Tax offices have files but no clerks, and some districts have clerks but "
        "no files. On the northern lowland, the largest district of the main island, villages are separated by marshes that "
        "swallow every road the capital has ever paid for.",
        "The surveyors also note that islanders are more patient than the capital deserves. They do not ask for the capital's "
        "wealth, only for a timetable that is kept and a road that lasts. The government must decide how to release the "
        "survey: as a public promise that will be measured every season, or as an internal plan that can be adjusted without "
        "embarrassment.",
    ), (
        Option('Publish it as a promise.', (Stability(0.02), PP(-10))),
        Option('Keep it as a working plan.', (PP(25),)),
    ), picture=0),
    EventDef('nine_hundred_hulls', 'Nine Hundred Hulls', (
        "The harbour clerks finish their count of the merchant register and arrive at a number the government had only "
        "guessed at: more than nine hundred hulls fly the Wellowan flag. They range from ocean tramps and coastal colliers to "
        "ferries, tankers and old trawlers converted to carry freight. Together they earn more foreign currency than every "
        "plant on the main island combined.",
        "The count also finds problems. Some owners registered ships that have since been sold abroad without telling anyone. "
        "Others pay dues on hulls that were scrapped years ago, to keep their place in the queue for fuel rebates. A handful "
        "of entries name owners whose only address is a post office box in a foreign port. Nobody in the harbour offices is "
        "sure how many of the nine hundred actually sail.",
        "The shipowners would like the count kept confidential while they put their own books in order. The newspapers have "
        "heard about the missing hulls and want names. Whatever the government decides will tell the owners whether the "
        "register is a tool of the state or a club they run for themselves, and the owners will remember the answer.",
    ), (
        Option('Publish every name on the register.', (Stability(-0.01), Event('ghost_hulls', 20))),
        Option('Let the owners correct it quietly.', (PP(30), Stability(0.01))),
    ), picture=0),
    EventDef('ghost_hulls', 'The Ghost Hulls', (
        "Three weeks after the register is published, a harbour newspaper prints a list of forty ships that exist only on "
        "paper. Some were lost at sea and never struck off; some were sold and renamed abroad; a few appear to have been "
        "invented outright to collect fuel rebates. The owners named on the list range from small family firms to two of the "
        "largest shipping houses in the capital.",
        "The publication does what the government hoped and what it feared. Honest owners rush to correct their entries, and "
        "the harbour offices are flooded with paperwork for the first time in years. The large houses hire lawyers, and their "
        "friends in the ministries ask whether the register really needed to be printed in full. Foreign insurers, who read "
        "Wellowan newspapers more carefully than anyone expected, quietly raise their premiums.",
        "The prosecutors can pursue the rebate fraud, which would take years and put powerful owners in court, or accept "
        "repayment and a fine, which would close the matter within a season. Either way, the register will be cleaner than it "
        "has been in a generation, and the owners will know the state is reading it.",
    ), (
        Option('Take the fraud to court.', (Stability(0.02), PP(-25))),
        Option('Settle for repayment and fines.', (PP(20), Stability(-0.01))),
    ), picture=1),
    EventDef('western_fields', 'The Western Fields', (
        "The field ledger is complete. It shows three oil-bearing districts on the main island: the western district with "
        "its steel works, the capital plain itself and the northeastern marsh. Between them they hold nearly all the nation's "
        "oil and steel, worked by wells and furnaces built by different owners at different times for different customers. "
        "Nothing about the arrangement was ever planned.",
        "The engineers' summary is blunt. Too much crude leaves the country unrefined, too little steel reaches the dockyard, "
        "and the marsh wells lose a season of output to mud every spring. The capital's single fuel depot holds a few weeks "
        "of supply for the fleet and the ferries, and nobody has written down who decides when to open it. Three schools of "
        "thought have already formed around the ledger, each sure it holds the answer.",
        "Before any model is chosen, the ministry has to decide who will see the ledger. Shared with the owners and the "
        "districts, it will start a long argument about royalties and fairness. Kept inside the ministry, it will guide "
        "policy quietly while every district suspects the others of being favoured.",
    ), (
        Option('Share the ledger with the districts.', (Stability(0.02), Research('excavation_tech', 0.5, 1))),
        Option('Keep it inside the ministry.', (PP(30),)),
    ), picture=1),
    EventDef('yard_quarrel', 'Six Slips, Three Masters', (
        "The dockyard district in the south of the main island has six building slips, and on the morning the inspectors arrive every one "
        "of them is claimed by somebody. The navy wants its escort programme restarted. The shipowners want new coasters and "
        "ferries for the island routes. The repair crews want the slips cleared so they can stop turning damaged ships away "
        "to foreign yards.",
        "The yard managers have a fourth complaint, which is that nobody has asked them. Half their riveters are close to "
        "retirement, their cranes were installed when the current escorts were laid down, and their order book is a pile of "
        "promises from ministries that change their minds every year. They would like a plan that lasts longer than a "
        "budget, and a customer who pays on time.",
        "The government cannot satisfy everyone with six slips. It can let the inspectors fight it out in committee, which "
        "will be slow and will leave every party half satisfied, or it can let the yard managers set the priorities for the "
        "next season while the larger question is settled. Either choice will be read as a signal by the owners and the "
        "admirals alike.",
    ), (
        Option('Let the committee decide.', (Stability(0.01), PP(-10))),
        Option('Trust the yard managers for now.', (Research('naval_equipment', 0.5, 1),)),
    ), picture=0),
    EventDef('belkan_sales', 'Belka Sells Its North', (
        "At the end of August 1991 the news from across the narrow sea arrives in a rush: Belka has sold its northern "
        "territory to FATO, sold eastern lands to its eastern neighbours and ceded northern islands and the Great Lakes region "
        "to the Osean Federation. Shipping agents in the Wellowan ports read the reports twice. Their neighbour to the south "
        "is shrinking, and it is selling land rather than losing it in war.",
        "Nobody in the capital knows what the sales mean for Wellow. Some officials expect new customs posts and new flags on "
        "the far shore, and new rules for every ship that trades there. Others see a neighbour in financial trouble that will "
        "need fuel, ships and credit, and may pay for them badly. A few of the older naval officers simply note that a "
        "neighbour reduced this way may one day want to undo it.",
        "The government must decide how loudly to say anything at all. A formal statement would show that Wellow is watching "
        "and might be read on the far shore as an opinion. Silence keeps every option open and leaves the ports to guess. The "
        "shipowners have already asked which of the new frontiers their masters should prepare for.",
    ), (
        Option('Issue a careful statement.', (Stability(0.02), PP(-10))),
        Option('Say nothing and keep watching.', (PP(25), WarSupport(0.01))),
    ), citation='date anchor only, ACES Chronicle row 1991 / 08.29 in tools/lore/chronicle.json; the Wellowan response is gameplay',
        picture=2),
    EventDef('belkan_war', 'War Across the Narrow Sea', (
        "On 25 March 1995 war breaks out on the continent south of Wellow. The first reports reaching the capital are "
        "fragments: Belkan forces moving, air battles over frontier cities, shipping warnings issued and withdrawn within "
        "hours. Wellow is not a party to any of it, but the narrow sea between the south coast and Belka is suddenly the "
        "busiest and most dangerous water in the region.",
        "The ports react before the ministries do. Shipowners pull their coasters off the southern routes and insurers cancel "
        "war cover overnight. Harbour masters on the south coast report unknown aircraft and warships at the edge of the "
        "coast watch's sight. In the capital, crowds gather outside newspaper offices, and the imperial and union movements "
        "both hold rallies demanding that the government say where it stands.",
        "The cabinet's first decision is smaller than any statement of policy. It must decide whether to put the coast watch, "
        "the reserve crews and the radar posts on a war footing now, before anyone can say which way the fighting will go, or "
        "to keep the ports calm and the ferries running and wait for clearer news.",
    ), (
        Option('Put the coast watch on a war footing.', (WarSupport(0.03), Event('coast_watch_report', 30))),
        Option('Keep the ports calm and wait.', (Stability(0.02), WarSupport(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Wellowan response is gameplay',
        picture=2),
    EventDef('coast_watch_report', 'The First Month of the Watch', (
        "A month after the coast watch went onto a war footing, its commanders send their first report to the capital. Radar "
        "posts and lookouts on the south coast have logged hundreds of aircraft and dozens of warships at the edge of their "
        "range, most of them heading somewhere else. Twice, damaged aircraft crossed the coastline and came down in the hills "
        "before anyone could identify them.",
        "The report is frank about the watch's limits. Its radars cover the southern approaches but not the western islands. "
        "Its reserve crews are tired, and the fuel ration for patrol boats runs out before the end of each week. The watch "
        "also stopped a fishing boat carrying three civilians who had crossed from the far shore, and nobody had a procedure "
        "for what to do with them.",
        "The commanders ask for two things: more patrol fuel, and a rule for people and aircraft that arrive from the war. "
        "The ministries can grant the fuel at the expense of the ferries, or write the rules first and leave the patrol boats "
        "on their ration a little longer.",
    ), (
        Option('Give the watch the fuel.', (XP('navy', 15), Stability(-0.01))),
        Option('Write the rules first.', (Stability(0.02), PP(-10))),
    ), picture=0),
    EventDef('waldreich_light', 'Light over the Southern Mountains', (
        "In the last weeks of the Belkan War instruments on the south coast record something no Wellowan scientist expected "
        "to measure outside a textbook. Within hours the news confirms it: nuclear devices have been used in the Waldreich "
        "Mountains, far to the south in Belka. Nothing was seen from Wellow, but the sensitive instruments recorded the disturbance, and the "
        "meteorologists begin tracking the winds that blow north across the narrow sea toward the south coast and the "
        "fishing grounds.",
        "The capital fills with questions faster than the scientists can answer them. Will anything reach the islands? Are "
        "the fishing grounds safe? Should children stay indoors? The newspapers print wind maps drawn by amateurs, and "
        "pharmacies run out of anything that sounds like protection. The imperial movement demands a national defence against "
        "weapons nobody in Wellow possesses, and the union camp demands a public accounting of every reading.",
        "The meteorologists believe the risk to Wellow is small, but they cannot yet prove it. The government can publish "
        "every reading as it arrives, including the frightening ones, or release only checked summaries once a day. Trust and "
        "calm are both at stake, and the ministers suspect they cannot have both.",
    ), (
        Option('Publish every reading.', (Stability(-0.02), Research('electronics', 0.5, 1))),
        Option('Release checked daily summaries.', (Stability(0.02), PP(-10))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 06.06 in tools/lore/chronicle.json, and only if the mod global flag '
                 'belka_dropped_nukes is set; the Wellowan measurements and response are gameplay',
        picture=2),
    EventDef('one_army_many_islands', 'One Army, Sixteen Districts', (
        "The garrison review lands on the defence minister's desk with a map that every officer in the capital already knew "
        "but nobody had drawn. Most of Wellow's infantry formations sit on the main island, within a day's march of the "
        "capital plain. The four western island districts and the southeastern islet are defended by a few companies, a coast "
        "watch and the hope that nobody tests them.",
        "Moving troops to the islands means ships, and ships belong to the navy or the merchant owners, neither of whom has "
        "planned for it. The northwestern highlands of the main island are mountain country where wheeled transport "
        "struggles, and the northern lowland is half marsh. The army's equipment was bought for a plain, and most of the nation "
        "is not one.",
        "Two schools have formed in the general staff. One wants a battalion raised and kept in every district, so that no "
        "island is ever empty. The other wants fewer, better brigades that travel by sea on the ferries and colliers. The "
        "minister must decide which school writes the next year's training plan while the larger question is argued.",
    ), (
        Option('Let the district school write the plan.', (XP('army', 15), Stability(0.01))),
        Option('Let the sea-lift school write it.', (XP('army', 10), Research('logistics_tech', 0.5, 1))),
    ), picture=1),
    EventDef('ulysses_warning', 'A Rock with a Name', (
        "In December 1994 the International Astronomical Union announces that an asteroid called Ulysses will pass close to "
        "the Earth, with a chance of striking it and causing great devastation. In Wellow the announcement is a radio bulletin "
        "between the shipping forecast and the evening news. By the next morning it is the only subject in the port taverns.",
        "Nobody can yet say where, or whether, anything will fall. The few astronomers in the capital are suddenly the most "
        "quoted people in the country, and they spend most of their interviews explaining what they do not know. Shipowners "
        "ask whether ocean routes will close. Island districts ask whether the ferries will still run. The imperial movement "
        "asks why Wellow has no rockets of its own.",
        "The government must decide how to speak about a danger that may not arrive for years, and may not arrive at all. It "
        "can set up a standing committee to prepare openly, which will keep the subject in the newspapers, or ask the "
        "observatories to report privately until there is something certain to announce. Either way, the shipowners will "
        "want to know before the public does.",
    ), (
        Option('Prepare in the open.', (WarSupport(0.02), Stability(-0.01), Research('construction_tech', 0.5, 1))),
        Option('Let the observatories report privately.', (Stability(0.02),)),
    ), citation='date anchor only, ACES Chronicle row 1994 / 12.10 in tools/lore/chronicle.json; Wellowan preparations are gameplay',
        picture=2),
    EventDef('aggressor_offer', 'Instructors for Hire', (
        "By the summer of 1998 former top pilots of the Belkan Air Force are being hired by various countries to fly as "
        "aggressor squadrons, playing the enemy so that other air arms can learn to fight one. A contracting agent arrives in "
        "the capital with an offer: a squadron of such instructors, with their own aircraft and maintainers, available to the "
        "Wellowan air arm on a three-year contract.",
        "The air staff is tempted. Its pilots have never trained against anyone better than themselves, and the instructors "
        "would expose every weakness in a season. The foreign ministry is not. Hiring former Belkan pilots, whatever their "
        "individual records, will be read on both sides of the narrow sea as a statement, and nobody can say who else these "
        "instructors have worked for.",
        "There is a cheaper middle course: send a handful of Wellowan instructors abroad to train against such squadrons "
        "elsewhere, and bring the lessons home. It is slower and teaches fewer pilots, but it keeps the contract and its "
        "politics out of the capital. The air staff wants an answer before the agent leaves.",
    ), (
        Option('Sign the three-year contract.', (TimedIdea('aggressor_school', 1095), PP(-30))),
        Option('Send our instructors abroad instead.', (XP('air', 25), Research('air_doctrine', 0.5, 1))),
    ), citation='date anchor only, ACES Chronicle row 1998 / 06.19 in tools/lore/chronicle.json; the offer to Wellow is gameplay',
        picture=0),
    EventDef('relief_voyage', 'A Relief Convoy Sails', (
        "The chartered relief convoy assembles in the dockyard district: colliers and coasters loaded with grain, fuel, tents "
        "and medicine, escorted by a single navy escort flying a relief pennant. Crews were found by volunteer lists posted in "
        "every port, and the lists filled faster than the harbour offices could type them up. The owners lent their ships at "
        "cost, and some lent them for nothing.",
        "The voyage is long and the destination uncertain. Ports in the stricken regions have their own priorities, and some "
        "have no working cranes at all. The convoy's masters carry instructions to unload wherever they are allowed, to take "
        "nothing in return and to leave before they become a burden. Insurers have refused to cover the voyage, so the state "
        "carries the risk.",
        "When the convoy returns, the government must decide how to tell the story. It can make the voyage a national "
        "occasion, with ceremonies in every port and a medal for the crews, or let the crews come home quietly and let the "
        "ports tell it themselves. The owners would like the publicity. The crews mostly want sleep.",
    ), (
        Option('Make it a national occasion.', (WarSupport(0.02), Stability(0.02), PP(-15))),
        Option('Let the crews come home quietly.', (Stability(0.03),)),
    ), picture=0),
    EventDef('distant_war', 'Insurers Price a Distant War', (
        "In August 2003 the FCU demands that Erusea withdraw from the railgun complex and San Salvacion, and a new allied "
        "force is established. The war that follows is fought on another continent, far from Wellow's waters. Within a week, "
        "though, the insurers who cover Wellowan hulls have rewritten their premiums for every route that touches Usea.",
        "Owners face a choice between turning down cargo and paying war-risk premiums that eat most of the profit. Some "
        "charterers offer double rates for fuel and supplies bound for the war zone, and do not say whose forces will receive "
        "them. The navy points out that Wellow has no escorts to spare for a voyage that long. The ferries, at least, are "
        "untouched, and the island districts barely notice.",
        "The government cannot stop a distant war, but it can decide what Wellowan ships may carry into it. It can issue a "
        "clear list of forbidden cargo now, or let the register and the insurers sort it out and intervene only when something "
        "goes wrong. The shipowners are lobbying for the second, and the newspapers for the first.",
    ), (
        Option('Issue the cargo list now.', (Stability(0.02), PP(-15))),
        Option('Let the market sort it out.', (PP(20), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2003 / 08.22 in tools/lore/chronicle.json; the Wellowan response is gameplay',
        picture=0),
    EventDef('fifteen_years', 'Fifteen Years of the Register', (
        "In the autumn of 2005, with the war over Usea ended and the ports counting their losses and gains, an independent "
        "panel publishes a review of how Wellow has been governed since 1991. Its members were drawn by lot from the "
        "districts, the shipowners, the dockyard unions and the polytechnic. Its report runs to three volumes and a short "
        "summary that every newspaper prints.",
        "The panel finds a country that kept its ships at sea and its ferries running through a Belkan war, an asteroid and a "
        "distant continent's war, but one that still governs its outer districts from too far away. The register is cleaner, "
        "the yards busier and the fields better managed than they were in 1991. The question of government that opened the "
        "period still divides the port towns, whatever answer the capital has given it.",
        "The government must decide how to receive the report. It can adopt the summary as a programme for the next decade "
        "and accept being measured against it, or thank the panel and leave the volumes on the shelf. Either way, the report "
        "will be quoted in every argument that follows.",
    ), (
        Option('Adopt the summary as a programme.', (Stability(0.03), PP(-20))),
        Option('Thank the panel and move on.', (PP(35),)),
    ), citation='date anchor only, ACES Chronicle row 2005 / 09.19 in tools/lore/chronicle.json; the review is gameplay',
        picture=1),
)

# --- branches ------------------------------------------------------------------------------------
ADMIN = Branch('admin', 'The Suspended Calendar', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('adm_take_stock', 'An Administration Without Voters',
          "The National Administration opens 1991 governing by ordinance, with no election calendar and a party that polls "
          "almost nobody. The imperial movement and the union camp between them hold nearly the whole electorate. Before it "
          "can do anything else, the administration must say in public how long it intends to govern, and on whose authority.",
          ('command', 'ballot'), reward=(Idea('caretaker_mandate'), Event('suspended_calendar'))),
    Focus('adm_ordinance_index', 'Index the Emergency Ordinances',
          "Clerks gather every ordinance issued since the calendar stopped: tariffs, port rules, press licences and district "
          "budgets. Many contradict each other and some were never published at all. Printing the full index costs the "
          "administration its useful vagueness, but every faction now argues from the same book, and the next step can be "
          "argued in the open.",
          ('document', 'scales'), after=('adm_take_stock',),
          reward=(PP(30), Tooltip('Opens four answers to the question of government; only one can be taken.'))),
    Focus('adm_port_hearings', 'Hearings in the Port Towns',
          "Commissioners sail to the port towns of the main island and the western islands to hear what people want from a "
          "government. The halls are crowded and angry, and imperial petitioners outnumber everyone else at most sittings. "
          "The record they bring back is honest, which makes it awkward for whoever governs next, and expensive to ignore.",
          ('assembly', 'navy'), after=('adm_take_stock',), reward=(TimedIdea('port_hearings', 365),)),
    Focus('adm_path_republic', 'Reopen the Electoral Rolls',
          "The administration's own small party argues that a republic which never votes is not a republic. It proposes "
          "rebuilding the rolls district by district and returning power to an elected chamber, accepting that the first "
          "election may hand the chamber to its opponents. The case is principled and risky, and few outside the capital "
          "believe the administration means it.",
          ('ballot', 'document'), after=('adm_ordinance_index',),
          exclusive=('adm_path_union', 'adm_path_imperial', 'adm_path_standing'),
          reward=(SwapIdea('caretaker_mandate', 'electoral_rolls'),)),
    Focus('adm_path_union', 'The Crown Held in Commission',
          "The union camp wants the islands governed as a United Kingdom of Wellow, with the crown exercised collectively by a "
          "council of the districts rather than by any single holder. It promises to keep party quarrels out of the ports. It "
          "also asks the administration to hand the seals to a body nobody has elected, on the strength of a petition.",
          ('assembly', 'medal'), after=('adm_ordinance_index',),
          exclusive=('adm_path_republic', 'adm_path_imperial', 'adm_path_standing'),
          reward=(SwapIdea('caretaker_mandate', 'union_commission'),)),
    Focus('adm_path_imperial', 'Hear the Imperial Petition',
          "Half the electorate, by the administration's own count, backs the movement that wants a Wellowan Empire: one flag, "
          "one fleet and a government that answers to national pride rather than to clerks. Its petition demands power now, "
          "without an election it expects to win anyway. Granting it brings discipline to the ports and fear to everyone "
          "outside the movement.",
          ('medal', 'security'), after=('adm_ordinance_index',),
          exclusive=('adm_path_republic', 'adm_path_union', 'adm_path_standing'),
          reward=(SwapIdea('caretaker_mandate', 'imperial_petition'),)),
    Focus('adm_path_standing', 'Ordinance as Constitution',
          "The senior clerks propose the least dramatic answer: keep governing as before, but turn the emergency ordinances "
          "into a written administrative code with fixed rules and a court to enforce them. Nobody votes and nobody is crowned. "
          "The ports get predictability and the two great movements get nothing, which they will not forgive quickly.",
          ('document', 'command'), after=('adm_ordinance_index',),
          exclusive=('adm_path_republic', 'adm_path_union', 'adm_path_imperial'),
          reward=(SwapIdea('caretaker_mandate', 'standing_ordinances'),)),
    Focus('adm_seat_chamber', 'Seat the Restored Chamber',
          "The rebuilt rolls produce a chamber, and a cabinet drawn from its majority takes the government seals. The change "
          "runs through the office, not a person: ministers govern collectively and face the chamber on a fixed calendar. The "
          "administration's clerks stay on as civil servants, and every ordinance must now survive a vote or lapse.",
          ('ballot', 'assembly'), after=('adm_path_republic',), cost=10,
          exclusive=('adm_union_council', 'adm_imperial_directorate', 'adm_standing_charter'),
          reward=(Regime('chamber_cabinet'), Flag('gov_republic'))),
    Focus('adm_union_council', 'Convene the Union Council',
          "Delegates from every district, main island and western islands alike, form a union council that holds the crown in "
          "commission and governs under the name of the United Kingdom of Wellow. The council decides collectively and prints "
          "its minutes. Elections wait until the council judges the districts settled, and the parties are told to be patient.",
          ('assembly', 'scales'), after=('adm_path_union',), cost=10,
          exclusive=('adm_seat_chamber', 'adm_imperial_directorate', 'adm_standing_charter'),
          reward=(Regime('union_council'), Flag('gov_union'))),
    Focus('adm_imperial_directorate', 'Install the Imperial Directorate',
          "A directorate drawn from the imperial movement's committees, retired naval officers and loyal clerks takes executive "
          "power and proclaims a Wellowan Empire. Decrees replace ordinances, and the party newspapers become the only "
          "newspapers. The directorate promises order in the ports and a fleet to be proud of. It has promised nothing to anyone "
          "who disagrees.",
          ('security', 'command'), after=('adm_path_imperial',), cost=10,
          exclusive=('adm_seat_chamber', 'adm_union_council', 'adm_standing_charter'),
          reward=(Regime('imperial_directorate'), Flag('gov_imperial'))),
    Focus('adm_standing_charter', 'Charter the Standing Administration',
          "The administration reconstitutes itself as a standing body of senior officials under a written charter, still "
          "without elections but now bound by its own code and a court that can strike down its ordinances. It governs "
          "collectively, as before, with no named head. The charter is dull, legalistic and stable, and gives the movements "
          "nothing to celebrate.",
          ('document', 'security'), after=('adm_path_standing',), cost=10,
          exclusive=('adm_seat_chamber', 'adm_union_council', 'adm_imperial_directorate'),
          reward=(Regime('standing_administration'), Flag('gov_standing'))),
    Focus('adm_chamber_wireless', 'Ministers on the Wireless',
          "Chamber sessions are broadcast to every district on state radio, including the western islands, where many voters "
          "have never seen a minister in person. The broadcasts expose quarrels the administration once settled behind closed "
          "doors, and imperial members use the airtime well. Over a season, though, listeners begin to judge ministers by what "
          "they actually say.",
          ('ballot', 'communications'), after=('adm_seat_chamber',),
          exclusive=('adm_district_charters', 'adm_fleet_day', 'adm_ordinance_court'),
          reward=(SwapIdea('electoral_rolls', 'open_chamber'),)),
    Focus('adm_district_charters', 'Charters for the Districts',
          "The union council grants each district a written charter fixing its share of port dues, its local court and its "
          "seat on the council. Western islanders gain guarantees they never had under the ordinances. The capital loses some "
          "revenue and much discretion, and the council spends its first winter arbitrating between rival harbour towns.",
          ('document', 'assembly'), after=('adm_union_council',),
          exclusive=('adm_chamber_wireless', 'adm_fleet_day', 'adm_ordinance_court'),
          reward=(SwapIdea('union_commission', 'union_settlement'),)),
    Focus('adm_fleet_day', 'The Imperial Fleet Day',
          "The directorate stages a fleet day at the dockyard district, with every escort and submarine dressed in flags and "
          "party committees lining the quays. Recruiting offices open beside the brass bands. The spectacle burns fuel the "
          "fleet cannot spare and alarms every shipping agent on the south coast, but it fills the rolls of the naval reserve.",
          ('navy', 'medal'), after=('adm_imperial_directorate',),
          exclusive=('adm_chamber_wireless', 'adm_district_charters', 'adm_ordinance_court'),
          reward=(SwapIdea('imperial_petition', 'imperial_order'), XP('navy', 20))),
    Focus('adm_ordinance_court', 'A Court for the Ordinances',
          "A small administrative court gains the power to strike down ordinances that contradict the code, and its first "
          "judgments go against the administration itself. Senior officials grumble, and shipowners welcome rules they can "
          "finally plan around. The court cannot make the government popular, but it can make it predictable, which the ports "
          "value more.",
          ('scales', 'security'), after=('adm_standing_charter',),
          exclusive=('adm_chamber_wireless', 'adm_district_charters', 'adm_fleet_day'),
          reward=(SwapIdea('standing_ordinances', 'coded_state'),)),
))

DISTRICTS = Branch('districts', 'The Scattered Districts', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('dis_survey', 'Survey the Outer Districts',
          "Ten of Wellow's sixteen districts have no paved roads worth the name, and the western island districts are reached "
          "only by sea. A survey of piers, roads, schools and tax offices costs a season of clerical work and ship time. It "
          "tells the capital, for the first time in years, what the outer districts actually lack and what they pay.",
          ('document', 'civil'), reward=(Idea('district_survey'), Event('ferry_season'))),
    Focus('dis_west_piers', 'Piers for the Western Islands',
          "The western island districts depend on piers built for fishing boats, not freight. Rebuilding the main pier on the "
          "large southwestern island, and the road that runs inland from it, costs steel the yards would rather use. Islanders "
          "gain a reliable link to the main island instead of a fair-weather one, and the coasters stop waiting offshore.",
          ('bridge', 'navy'), after=('dis_survey',), reward=(Build('infrastructure', 2, 96),)),
    Focus('dis_far_west', 'Roads at the Far West',
          "The westernmost island district sits far from every other Wellowan harbour and has always been run by whichever "
          "official the capital could spare. A road between its harbours and a district office with a permanent staff are "
          "modest projects. For the islanders they are proof that the capital, whoever holds it, knows they exist.",
          ('civil', 'tools'), after=('dis_survey',), reward=(Build('infrastructure', 2, 131),)),
    Focus('dis_northwest_island', 'The Northwest Island Road',
          "The large island off the northwest coast has hill country, a few fishing harbours and two old naval moorings. A "
          "coast road joining its harbours lets the catch reach the moorings and the ferries. The work is slow in the hills and "
          "costly in a short building season, but the island finally becomes one place instead of several.",
          ('rail', 'civil'), after=('dis_survey',), reward=(Build('infrastructure', 2, 17),)),
    Focus('dis_southeast_islet', 'An Officer for the Islet',
          "A small hill islet lies off the southeast coast, close to the sea lanes that run toward Belka. It has one naval "
          "mooring and little else. Paving its harbour road and stationing a district officer there costs little and keeps "
          "the islet tied to the main island rather than to the passing traffic. The navy also likes the view.",
          ('security', 'civil'), after=('dis_survey',), reward=(Build('infrastructure', 1, 175), Flag('islet_settled'))),
    Focus('dis_northern_lowland', 'Causeways on the Northern Lowland',
          "The northern lowland is the largest district on the main island, a wide plain broken by marshes, with almost no "
          "roads and no industry at all. Causeways across the worst marshes connect its villages to the capital plain. The "
          "work drains money for years before it pays back, yet the lowland's farms are what feed the capital.",
          ('bridge', 'rebuild'), after=('dis_survey',), reward=(Build('infrastructure', 2, 255),)),
    Focus('dis_ferry_timetable', 'A Ferry Timetable for All',
          "A single timetable links every island district to the main island, with state-subsidised ferries running on fixed "
          "days in every season. Private owners complain that subsidised ferries undercut them; islanders say it is the first "
          "promise from the capital that arrives on schedule. The subsidy is permanent, and so is its bill.",
          ('navy', 'logistics'), after_any=('dis_west_piers', 'dis_far_west', 'dis_northwest_island'),
          reward=(Idea('ferry_compact'), Flag('ferry_network'))),
    Focus('dis_councils', 'Elected Island Councils',
          "Each outer district elects a council with its own budget for piers, schools and roads, while the capital keeps "
          "defence, currency and the fleet. Councils spend money where islanders live rather than where clerks sit. They also "
          "argue with the capital every budget season, and some will elect imperial petitioners whatever the capital prefers.",
          ('assembly', 'ballot'), after=('dis_ferry_timetable',), cost=10, exclusive=('dis_prefecture',),
          reward=(SwapIdea('district_survey', 'island_councils'), Flag('districts_devolved'))),
    Focus('dis_prefecture', 'The Island Prefecture',
          "A single prefecture staffed from the capital governs every outer district under one code, with prefects rotating "
          "between islands every two years. Decisions arrive faster and corruption has fewer corners to hide in. Islanders lose "
          "any say in how their harbours are run, and the prefects become the face of a government most never chose.",
          ('command', 'navy'), after=('dis_ferry_timetable',), cost=10, exclusive=('dis_councils',),
          reward=(SwapIdea('district_survey', 'island_prefecture'), Flag('districts_prefects'))),
    Focus('dis_council_canneries', 'The Councils Build Canneries',
          "The first council budgets go not to monuments but to cold stores and canneries in the fishing harbours of the "
          "western islands. Catches that once spoiled on the quay are packed and shipped. The councils borrow to do it, and the "
          "capital must decide whether to guarantee the debt or let a council fail in public.",
          ('fishing', 'industry'), after=('dis_councils',), exclusive=('dis_prefect_circuit',),
          reward=(Build('industrial_complex', 1, 100),)),
    Focus('dis_prefect_circuit', 'Prefects on the Ferry Circuit',
          "Prefects ride the ferry circuit on a fixed calendar, inspecting tax offices, piers and schools and reporting straight "
          "to the capital. A district depot at the far west stores spare parts and paperwork alike. The circuit costs ship time "
          "and salaries, and it ends the habit of sending only good news from distant harbours.",
          ('command', 'logistics'), after=('dis_prefecture',), exclusive=('dis_council_canneries',),
          reward=(Build('industrial_complex', 1, 131), PP(20))),
))

REGISTER = Branch('register', 'The Merchant Register', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('reg_count_hulls', 'Count the Merchant Hulls',
          "More than nine hundred merchant hulls fly the Wellowan flag, from ocean tramps to coastal colliers, and they earn "
          "more foreign currency than anything the main island makes. Nobody has audited the register in years. Counting every "
          "hull, owner and crew list costs a season of harbour work and shows how much income actually sails home.",
          ('logistics', 'document'), reward=(Idea('merchant_register'), Event('nine_hundred_hulls'))),
    Focus('reg_harbour_offices', 'Harbour Offices in Every Port',
          "Each port gets a harbour office able to register ships, check crews and collect dues on the spot, starting with the "
          "busy marsh ports of the northeast. Owners stop sailing to the capital for paperwork. The offices cost salaries, and "
          "they give the state a clerk on every quay, which some owners welcome and others plainly do not.",
          ('navy', 'document'), after=('reg_count_hulls',), reward=(Build('infrastructure', 1, 250),)),
    Focus('reg_navigation_school', 'Navigation Schools for Crews',
          "Ship officers trained abroad cost foreign wages and leave when better offers arrive. A navigation school beside the "
          "southwestern island moorings trains deck officers and engineers under Wellowan certificates. Four years pass before "
          "the first class sails. Owners pay part of the cost, grumbling, and the fleet slowly stops relying on foreign officers.",
          ('training', 'navy'), after=('reg_count_hulls',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 10))),
    Focus('reg_shipping_exchange', 'A Shipping Exchange in the Capital',
          "Charter brokers in the capital trade freight contracts by telephone and handshake, and foreign brokers take most of "
          "the commission. An exchange with published rates and a settlement office keeps those commissions at home. It needs "
          "a building, a switchboard and rules the brokers dislike, and it earns its keep within two seasons.",
          ('economy', 'communications'), after=('reg_harbour_offices',), reward=(TimedIdea('exchange_commissions', 1095),)),
    Focus('reg_open', 'Open the Registry to Foreigners',
          "The open-registry school wants any owner in the world to register ships under the Wellowan flag for a modest fee and "
          "a light inspection. Fees would pour in and the register might double in a decade. So would the number of rusting "
          "hulls with unknown crews, and every foreign war would find some of its cargo flying Wellowan colours.",
          ('logistics', 'economy'), after_any=('reg_harbour_offices', 'reg_navigation_school'), cost=10,
          exclusive=('reg_national', 'reg_mutual'),
          reward=(SwapIdea('merchant_register', 'open_registry'), Flag('registry_open'))),
    Focus('reg_national', 'A National Line',
          "The national-line school wants the state to buy controlling stakes in the largest shipping houses and run their "
          "ships on fixed routes with Wellowan crews and Wellowan yards. Freight rates would be steady and the slips busy. "
          "Owners who refuse to sell would face higher dues, and the treasury would carry every bad year at sea.",
          ('navy', 'command'), after_any=('reg_harbour_offices', 'reg_navigation_school'), cost=10,
          exclusive=('reg_open', 'reg_mutual'),
          reward=(SwapIdea('merchant_register', 'national_line'), Flag('registry_national'))),
    Focus('reg_mutual', 'The Shipowners Mutual',
          "The owners propose a mutual of their own: a pooled insurance fund, a shared repair budget and a common rate book, run "
          "by the owners under state supervision. It keeps ships in private hands and spreads the risk of a bad season. Critics "
          "note that a mutual run by the biggest owners will look after the biggest owners first.",
          ('scales', 'logistics'), after_any=('reg_harbour_offices', 'reg_navigation_school'), cost=10,
          exclusive=('reg_open', 'reg_national'),
          reward=(SwapIdea('merchant_register', 'owners_mutual'), Flag('registry_mutual'))),
    Focus('reg_agents_abroad', 'Registry Agents Abroad',
          "Registry agents open desks in foreign ports to sign up owners on the spot, and the fees fund a harbour-works company "
          "on the south coast. Inspection lags behind registration. The first casualty report involving a Wellowan-flagged hull "
          "with a foreign crew reaches the newspapers within a year, and the agents are asked awkward questions.",
          ('diplomacy', 'economy'), after=('reg_open',), exclusive=('reg_line_routes', 'reg_hull_pool'),
          reward=(Build('industrial_complex', 1, 244),)),
    Focus('reg_line_routes', 'Fixed Routes for the Line',
          "The national line publishes its first fixed timetable: coastal colliers between the dockyard district and the "
          "western islands, and ocean services on set days. Shippers can finally plan. A slip on the southwestern island takes "
          "the line's repair contracts, and private owners find themselves undercut on every route the line chooses to serve.",
          ('navy', 'rail'), after=('reg_national',), exclusive=('reg_agents_abroad', 'reg_hull_pool'),
          reward=(Build('dockyard', 1, 96),)),
    Focus('reg_hull_pool', 'The Hull Insurance Pool',
          "The mutual's insurance pool pays its first large claims after a storm season, and every member is still afloat. "
          "Premiums stay below what foreign insurers charge. The pool invests its reserves in a repair basin at the eastern "
          "ports, which keeps member ships off foreign slipways and their repair money at home.",
          ('economy', 'rebuild'), after=('reg_mutual',), exclusive=('reg_agents_abroad', 'reg_line_routes'),
          reward=(Build('infrastructure', 1, 248), Research('naval_equipment', 0.5, 2))),
    Focus('reg_convoy_rules', 'Sealed Orders for Every Master',
          "Every registered master receives sealed instructions for a war at sea: assembly ports, signals, escort rendezvous and "
          "the routes to avoid. The rules cost nothing until a war comes near, and then they are worth more than any escort. "
          "Owners complain about the paperwork; naval officers note the rules assume the navy has escorts to send.",
          ('document', 'navy'), after_any=('reg_agents_abroad', 'reg_line_routes', 'reg_hull_pool'),
          reward=(Idea('convoy_discipline'), Flag('convoy_rules'))),
))

FIELDS = Branch('fields', 'Oil and Steel of the Main Island', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('fld_ledger', 'Measure the Western Fields',
          "Most of Wellow's oil and steel comes from the western district of the main island, the capital plain and the "
          "northeastern marshes, worked by plants that were never planned together. A field ledger records every well, mine "
          "and furnace with its output and its losses. It costs a year of surveys and settles arguments politicians prefer open.",
          ('industry', 'document'), reward=(Idea('field_ledger'), Event('western_fields'))),
    Focus('fld_marsh_wells', 'Wells in the Northeastern Marsh',
          "The northeastern marsh district holds a third of the nation's oil under ground that swallows roads every spring. "
          "Plank causeways and pumping stations let crews reach the wells all year. The work is miserable and expensive, but "
          "every barrel that reaches the coast without a detour through the capital saves fuel and freight.",
          ('tools', 'logistics'), after=('fld_ledger',), reward=(Build('infrastructure', 2, 250),)),
    Focus('fld_west_furnaces', 'Ore Roads for the Western Furnaces',
          "The western district's steel works run furnaces that were modern when the yards last expanded. Rebuilding the road "
          "and rail links between mines, furnaces and the western harbour cuts the cost of every ton. New furnaces would need "
          "room the district no longer has, so the money goes into moving ore faster instead.",
          ('rail', 'industry'), after=('fld_ledger',), reward=(Build('infrastructure', 2, 5), Research('excavation_tech', 0.5, 1))),
    Focus('fld_capital_works', 'Works Beside the Capital Plain',
          "The district west of the capital plain has workers, water and a rail line but almost no plants. Two new works there "
          "take the overflow of the capital's crowded industrial quarter, which has no room left to grow. The capital loses some "
          "prestige to its neighbour, and the neighbour gains the noise and the wages.",
          ('industry', 'civil'), after=('fld_ledger',), reward=(Build('industrial_complex', 2, 245),)),
    Focus('fld_refine_home', 'Refine Every Barrel at Home',
          "The refining school says crude sold abroad is wealth given away. It wants every barrel refined in Wellowan plants, "
          "with fuel for the fleet and the ferries first and exports only from the surplus. Refineries are expensive and slow "
          "to build, and until they are finished the treasury earns less from oil than before.",
          ('industry', 'tools'), after_any=('fld_marsh_wells', 'fld_west_furnaces'), cost=10,
          exclusive=('fld_tankers', 'fld_steel_first'), reward=(SwapIdea('field_ledger', 'home_refining'),)),
    Focus('fld_tankers', 'Crude by Tanker',
          "The export school says the merchant fleet and the oil fields were made for each other: load the crude, sail it to "
          "whoever pays most and buy finished fuel back when needed. Revenue arrives quickly and tanker owners prosper. The "
          "fleet's fuel then depends on foreign refineries, and a war at sea could leave the ferries idle.",
          ('logistics', 'economy'), after_any=('fld_marsh_wells', 'fld_west_furnaces'), cost=10,
          exclusive=('fld_refine_home', 'fld_steel_first'),
          reward=(SwapIdea('field_ledger', 'crude_exports'), Flag('fields_export'))),
    Focus('fld_steel_first', 'Spend the Oil on Steel',
          "A third school wants the oil money spent on steel: rolling mills, plate for the yards and rails for the island roads, "
          "with new wells deferred until the mills are running. It promises lasting industry rather than quick income. It also "
          "asks the oil districts to wait while the steel towns are served first, and they resent it.",
          ('industry', 'rail'), after_any=('fld_marsh_wells', 'fld_west_furnaces'), cost=10,
          exclusive=('fld_refine_home', 'fld_tankers'), reward=(SwapIdea('field_ledger', 'steel_plate'),)),
    Focus('fld_refinery', 'A Refinery Beside the Oil District',
          "The district between the western oil fields and the northwestern highlands has room, water and a sheltered harbour. "
          "A refinery there takes crude by pipe from the western wells and sends fuel to the capital by rail. It takes two "
          "years to commission and smells for twenty, and the fleet's tanks finally fill at home.",
          ('industry', 'shelter'), after=('fld_refine_home',), exclusive=('fld_tanker_terminal', 'fld_plate_mill'),
          reward=(Build('industrial_complex', 2, 266),)),
    Focus('fld_tanker_terminal', 'Deepwater Tanker Jetties',
          "Deepwater jetties and storage tanks at the dockyard district let large tankers load without lightering, and a repair "
          "slip on the southeastern coast keeps them sailing. The terminal moves crude faster than any refinery could use it. "
          "The south coast earns harbour dues, as long as the sea lanes stay calm.",
          ('logistics', 'navy'), after=('fld_tankers',), exclusive=('fld_refinery', 'fld_plate_mill'),
          reward=(Build('infrastructure', 1, 253), Build('dockyard', 1, 246))),
    Focus('fld_plate_mill', 'A Plate Mill for the Yards',
          "A plate mill on the southeastern coast rolls ship steel for the dockyard district from western ore, cutting out the "
          "foreign mills that used to supply every hull. Yards gain a domestic supplier whose prices are not always lower. The "
          "oil districts watch their royalties spent on rolling stands and ask when their turn will come.",
          ('industry', 'navy'), after=('fld_steel_first',), exclusive=('fld_refinery', 'fld_tanker_terminal'),
          reward=(Build('industrial_complex', 1, 246), Research('industry', 0.5, 1))),
    Focus('fld_fuel_reserve', 'The Capital Fuel Reserve',
          "The capital already keeps a fuel depot; it becomes a national reserve with written rules for when it may be drawn "
          "and who decides. Ferries, the fleet and the heating plants get guaranteed shares. A reserve that is never touched "
          "looks like waste in good years, and like foresight in every other kind of year.",
          ('shelter', 'logistics'), after_any=('fld_refinery', 'fld_tanker_terminal', 'fld_plate_mill'),
          reward=(Flag('fuel_reserve'), Stability(0.02))),
))

YARDS = Branch('yards', 'The Dockyard District', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('yrd_open_gates', 'Open the Yard Gates',
          "Six building slips in the dockyard district, in the south of the main island, build nearly every Wellowan hull, and the yard has "
          "not been modernised since the current escorts were laid down. The government opens the gates to inspectors from the "
          "navy, the shipowners and the unions at once. Each wants the slips for itself, and there are only six.",
          ('navy', 'tools'), reward=(Idea('six_slips'), Event('yard_quarrel'))),
    Focus('yrd_apprentices', 'Apprentices on the Slipways',
          "Half the riveters and welders in the dockyard district are within ten years of retiring, and their children have "
          "gone to sea or to the capital. A paid apprenticeship of four years, with housing near the slips, fills the gap "
          "slowly. The unions want control of the intake, and the owners want apprentices bound to them for years.",
          ('training', 'tools'), after=('yrd_open_gates',), reward=(TimedIdea('apprentice_intake', 1095),)),
    Focus('yrd_south_cranes', 'New Cranes on the South Quay',
          "The dockyard's cranes lift half what modern hull sections weigh, so every ship is built in small pieces and riveted "
          "slowly. Heavy cranes on the south quay and a widened yard road change the pace of every keel. The order goes "
          "abroad because no Wellowan plant can build them, and the bill arrives in foreign currency.",
          ('tools', 'logistics'), after=('yrd_open_gates',), reward=(Build('infrastructure', 1, 253), Research('naval_equipment', 0.5, 1))),
    Focus('yrd_wage_board', 'A Wage Board for the Slips',
          "Every spring the yard unions and owners fight over wages, and every spring a hull is late. A standing board of owners, "
          "unions and the ministry sets slipway wages for three years at a time. Strikes become rarer and settlements slower, "
          "and the ministry now shares the blame for every disappointed welder.",
          ('scales', 'tools'), after=('yrd_apprentices',), reward=(Idea('yard_wage_board'),)),
    Focus('yrd_escort_priority', 'Escorts on Every Slip',
          "The navy argues that a merchant nation without escorts is a merchant nation waiting to be robbed. It wants the slips "
          "given to escorts for five years, with merchant work fitted in around them. The fleet grows and the owners wait, "
          "buying abroad the coasters their own yards would have built.",
          ('navy', 'security'), after_any=('yrd_apprentices', 'yrd_south_cranes'), cost=10,
          exclusive=('yrd_merchant_priority', 'yrd_repair_priority'), reward=(SwapIdea('six_slips', 'escort_slips'),)),
    Focus('yrd_merchant_priority', 'Merchant Keels First',
          "The owners argue that ferries and coasters earn the money that pays for any navy. They want the slips given to "
          "merchant hulls, with warships built when there is room. The register grows younger and the island routes run on new "
          "ships, while the admirals sail old escorts a few more years.",
          ('logistics', 'tools'), after_any=('yrd_apprentices', 'yrd_south_cranes'), cost=10,
          exclusive=('yrd_escort_priority', 'yrd_repair_priority'), reward=(SwapIdea('six_slips', 'merchant_slips'),)),
    Focus('yrd_repair_priority', 'Repair Before New Keels',
          "The repair crews argue that the cheapest ship is the one already afloat. They want the slips cleared for refits and "
          "repairs that now go to foreign yards, and new construction only when repair work runs out. Ships last longer and the "
          "yard earns steadily, but nothing new slides into the water for years.",
          ('rebuild', 'navy'), after_any=('yrd_apprentices', 'yrd_south_cranes'), cost=10,
          exclusive=('yrd_escort_priority', 'yrd_merchant_priority'), reward=(SwapIdea('six_slips', 'repair_basins'),)),
    Focus('yrd_second_yard', 'A Second Yard Facing Belka',
          "Six slips are not enough for any plan. A second, smaller yard on the southern coast facing Belka takes the overflow, "
          "with two slips for coasters and escorts. It splits skilled workers between two sites and puts a strategic asset "
          "within sight of the narrow sea, which the navy notes with mixed feelings.",
          ('navy', 'industry'), after_any=('yrd_escort_priority', 'yrd_merchant_priority', 'yrd_repair_priority'),
          reward=(Build('dockyard', 2, 244),)),
    Focus('yrd_island_slip', 'A Slip on the Southwestern Island',
          "The southwestern island has the deepest sheltered water outside the main island and a fishing fleet that repairs "
          "its own boats on the beach. A proper slip there builds and mends coasters for the island routes. It brings skilled "
          "work to the islands, and it needs steel shipped across a sea that is not always kind.",
          ('fishing', 'tools'), after=('yrd_second_yard',), reward=(Build('dockyard', 1, 96),)),
    Focus('yrd_standard_hull', 'One Hull, Many Uses',
          "Yard designers propose a single standard hull that can be finished as a coaster, a ferry or a patrol vessel, built "
          "in sections on any slip. Owners lose the bespoke designs they like to boast about. The yards gain speed, spare parts "
          "become interchangeable and the navy can requisition merchant hulls that already fit its fittings.",
          ('tools', 'navy'), after=('yrd_second_yard',), reward=(Idea('standard_hulls'),)),
))

FLEET = Branch('fleet', 'A Fleet Kept in Being', 1991, 'FOCUS_FILTER_NAVY_XP', (
    Focus('flt_muster', 'Muster the Coastal Fleet',
          "Wellow's navy is a coastal force of escorts and small submarines spread across moorings on the main island and the "
          "western islands, trained to survive rather than to win battles. Mustering it in one anchorage for the first time in "
          "years shows what it can do and what it lacks. The fuel bill alone shocks the treasury.",
          ('navy', 'command'), reward=(Idea('harbour_fleet'), XP('navy', 15))),
    Focus('flt_moorings', 'Moorings Across the Western Islands',
          "The western island districts have more naval moorings than any other part of the country, most of them a buoy, a "
          "jetty and a fuel tank. Proper roads to the moorings on the middle island, with stores and a telephone line, let a "
          "squadron actually live there. The work is cheap, and the moorings stop being lines on a chart.",
          ('navy', 'rail'), after=('flt_muster',), reward=(Build('infrastructure', 1, 100), XP('navy', 10))),
    Focus('flt_submariners', 'A School for Submariners',
          "The small submarines are the navy's only weapon an enemy would genuinely fear, and their crews are trained in the "
          "boats themselves, at sea, one crew at a time. A shore school with a diving tank and attack trainers doubles the pace. "
          "It costs a building and a year, and veteran captains resent the classroom.",
          ('submarine', 'training'), after=('flt_muster',), reward=(Research('naval_equipment', 0.5, 1), XP('navy', 20))),
    Focus('flt_sound_patrols', 'Submarines in the Island Sounds',
          "The submarine school says the channels between the islands are Wellow's natural defence: narrow, deep and known only "
          "to Wellowan pilots. Small boats lying in the sounds can make any intruder pay. The doctrine defends the islands well "
          "and the merchant lanes hardly at all, which the shipowners will notice first.",
          ('submarine', 'navy'), after_any=('flt_moorings', 'flt_submariners'), cost=10,
          exclusive=('flt_escort_screen', 'flt_island_squadrons'), reward=(SwapIdea('harbour_fleet', 'sound_patrols'),)),
    Focus('flt_escort_screen', 'Escorts for the Merchant Lanes',
          "The escort school says a navy that guards empty harbours while the merchant fleet sails unprotected has misunderstood "
          "its country. It wants the escorts organised around the merchant lanes and drilled with convoys. The lanes become "
          "safer, and the islands depend more on the army and the coast watch.",
          ('navy', 'logistics'), after_any=('flt_moorings', 'flt_submariners'), cost=10,
          exclusive=('flt_sound_patrols', 'flt_island_squadrons'), reward=(SwapIdea('harbour_fleet', 'escort_screen'),)),
    Focus('flt_island_squadrons', 'A Squadron for Every Island',
          "A third school wants the navy split into small squadrons, each based on its own island group with its own repair "
          "crew, so that no island waits days for help. The squadrons are close to the people they protect. Each is too small "
          "to fight alone, and the admirals fear a navy of parish fleets.",
          ('navy', 'rebuild'), after_any=('flt_moorings', 'flt_submariners'), cost=10,
          exclusive=('flt_sound_patrols', 'flt_escort_screen'), reward=(SwapIdea('harbour_fleet', 'island_squadrons'),)),
    Focus('flt_convoy_drill', 'Convoy Drill with the Owners',
          "With sealed orders in every master's safe, the navy runs its first full convoy exercise: merchant ships assembling "
          "at a southern port, forming columns and sailing under escort while aircraft play the attacker. Owners lose a week of "
          "trading. Masters and escort captains finally learn each other's signals.",
          ('navy', 'training'), after_any=('flt_sound_patrols', 'flt_escort_screen', 'flt_island_squadrons'),
          requires=(HasFlag('convoy_rules'),), reward=(XP('navy', 25), Research('naval_equipment', 0.5, 2))),
    Focus('flt_islet_radar', 'Radar on the Southeastern Islet',
          "The islet off the southeast coast, now with a road and a resident officer, looks straight down the sea lanes toward "
          "Belka. A radar post on its highest hill extends the coast watch far beyond the main island's horizon. Its crews live "
          "in isolation, and the post is the first thing any attacker would destroy.",
          ('radar', 'navy'), after=('flt_muster',), requires=(HasFlag('islet_settled'),),
          reward=(Build('radar_station', 2, 175),)),
    Focus('flt_imperial_programme', 'An Imperial Naval Programme',
          "The directorate funds a naval programme worthy of the empire it proclaimed: new escorts, a recruiting drive in every "
          "port and a training squadron that sails the length of the island chain. Shipyards cheer. The treasury and the "
          "merchant owners, who will pay for it, are not asked for their opinion.",
          ('navy', 'medal'), after_any=('flt_sound_patrols', 'flt_escort_screen', 'flt_island_squadrons'),
          requires=(HasFlag('gov_imperial'),), reward=(TimedIdea('imperial_programme', 1095),)),
    Focus('flt_reserve_crews', 'Reserve Crews from the Merchant Fleet',
          "Merchant officers and ratings who agree to train two weeks a year join a naval reserve, ready to crew escorts and "
          "auxiliaries if war comes. The merchant fleet is the country's largest pool of trained seamen. Owners lose crews for "
          "the drills, and the navy gains men who know the sea better than its own conscripts.",
          ('training', 'navy'), after=('flt_submariners',), reward=(XP('navy', 15), WarSupport(0.02), Research('naval_equipment', 0.5, 1))),
))

AIR = Branch('air', 'Wings over the Narrow Sea', 1991, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count', 'Count the Air Arm',
          "Wellow's air arm has a few dozen fighters and a handful of support aircraft at two fields, one in the western oil "
          "district and one beside the capital. Pilots fly too few hours and spare parts come from abroad. A full count of "
          "aircraft, crews and parts tells the government how much of the air arm actually flies.",
          ('air', 'document'), reward=(Idea('air_census'),)),
    Focus('air_capital_field', 'Lengthen the Capital Runways',
          "The field beside the capital was laid out for aircraft that are now museum pieces. Longer runways, hard stands and a "
          "fuel line from the capital depot let modern fighters operate there in any season. Neighbours complain about the "
          "noise. The air arm finally has one field worthy of the name.",
          ('runway', 'air'), after=('air_count',), reward=(Build('air_base', 2, 0),)),
    Focus('air_south_field', 'A Field Facing the Narrow Sea',
          "Every threat the air staff can imagine comes from the south, yet neither field is on the south coast. A new field "
          "near the southern shore, looking across the narrow sea toward Belka, cuts minutes from every interception. Building "
          "it so close to a neighbour is also a statement, and the foreign ministry asks that it be built quietly.",
          ('runway', 'security'), after=('air_count',), reward=(Build('air_base', 2, 244),)),
    Focus('air_island_strips', 'Grass Strips on the Islands',
          "The air arm marks out grass strips on the northwest island and at the other island districts where the ground "
          "allows, so that aircraft can disperse, refuel or land damaged. The strips need little more than a windsock and a fuel "
          "store. They turn the island chain into a string of emergency fields instead of open sea.",
          ('runway', 'navy'), after=('air_count',), reward=(Build('air_base', 1, 17), Flag('island_airfields'))),
    Focus('air_interceptors', 'Interceptors First',
          "The interceptor school wants every aircraft and every pilot hour spent on one task: stopping hostile aircraft before "
          "they reach the coast. The air arm becomes a shield with radar eyes. It does nothing for the merchant lanes or the "
          "army, and its pilots learn little beyond intercepts.",
          ('air', 'radar'), after_any=('air_capital_field', 'air_south_field'), cost=10, exclusive=('air_sea_patrol',),
          reward=(SwapIdea('air_census', 'strait_interceptors'),)),
    Focus('air_sea_patrol', 'Eyes over the Sea Lanes',
          "The patrol school says the air arm should watch the sea: the merchant lanes, the island sounds and the approaches "
          "to every port. Patrol aircraft and strike crews trained against ships would protect what actually earns the money. "
          "The capital's skies would rely on fewer fighters.",
          ('air', 'navy'), after_any=('air_capital_field', 'air_south_field'), cost=10, exclusive=('air_interceptors',),
          reward=(SwapIdea('air_census', 'sea_patrol_wing'),)),
    Focus('air_parts_works', 'Spare Parts Made at Home',
          "Grounded aircraft wait months for parts shipped from abroad. A small works on the southeastern coast makes tyres, "
          "brakes, filters and simple structural parts under licence. It cannot build an aircraft, but it keeps far more of "
          "them flying, and its machinists learn trades the country has never had.",
          ('tools', 'air'), after=('air_count',), reward=(Build('arms_factory', 1, 246),)),
    Focus('air_capital_radar', 'Radar Around the Capital',
          "The capital sits on an inland plain, which gives it time but also a false sense of safety. A radar ring linked to the "
          "capital field's control room lets fighters scramble with warning rather than by guesswork. It is expensive for a "
          "capital nobody has threatened, which is exactly what the air staff says about every insurance.",
          ('radar', 'command'), after_any=('air_interceptors', 'air_sea_patrol'), reward=(Build('radar_station', 1, 0),)),
    Focus('air_hard_strips', 'Hard Runways on the Islands',
          "The grass strips proved their worth in bad weather and worse landings. The busiest of them, on the southwestern "
          "island, gets a hard runway, a hangar and a permanent ground crew. Island aircraft can now operate year round rather "
          "than in fair seasons only, and the islanders gain an air link to the capital.",
          ('runway', 'rebuild'), after=('air_island_strips',), requires=(HasFlag('island_airfields'),),
          reward=(Build('air_base', 2, 96),)),
    Focus('air_aggressors', 'Train Against the Best',
          "By 1998 former top Belkan Air Force pilots are being hired by various countries as aggressor squadrons. The air "
          "staff sees a chance its pilots will never get otherwise: to fight, in practice, against someone better. The price "
          "is money, and a political question the foreign ministry would rather not answer.",
          ('training', 'air'), after_any=('air_interceptors', 'air_sea_patrol'), requires=(After('1998.6.19'),),
          reward=(Event('aggressor_offer'),)),
))

STRAIT = Branch('strait', 'Across the Narrow Sea', 1991, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('str_coast_watch', 'Watch the Southern Coast',
          "Belka lies across a narrow sea from the south coast, close enough that its aircraft could reach the capital in "
          "minutes. The coast watch has lookouts and a few patrol boats but no radar. A radar post on the southern shore and a "
          "watch roster in every coastal district cost little and tell the capital what crosses the water.",
          ('radar', 'security'), reward=(Idea('strait_watch'), Build('radar_station', 1, 244))),
    Focus('str_belkan_sales', 'Belka Sells Its Northern Lands',
          "In August 1991 Belka sells its northern territory to FATO and cedes northern islands and the Great Lakes region to "
          "Osea. Wellowan shipping agents wake to new flags and new customs posts on familiar coasts. The foreign ministry has to "
          "decide what, if anything, a neutral island nation should say about it.",
          ('diplomacy', 'document'), after=('str_coast_watch',), requires=(After('1991.8.29'),), reward=(Event('belkan_sales'),)),
    Focus('str_new_borders', 'Charts for the New Borders',
          "When Belka's borders are redrawn in December 1991, every Wellowan chart of the far shore becomes wrong overnight. "
          "Hydrographers and customs officers redraw the routes, the ports of entry and the buoyage. The work is unglamorous "
          "and urgent, because a master with the wrong chart can start a diplomatic incident.",
          ('document', 'navy'), after=('str_belkan_sales',), requires=(After('1991.12.16'),),
          reward=(Research('logistics_tech', 0.5, 1), Stability(0.02))),
    Focus('str_war_news', 'Fighting Beyond the Southern Shore',
          "In March 1995 the Belkan War breaks out on the continent to the south. The narrow sea fills with warships and "
          "aircraft, insurers cancel cover and the ports wait for instructions. Wellow is not a party, but the cabinet must "
          "decide how the coast watch, the reserves and the ports respond to a war next door.",
          ('security', 'communications'), after=('str_coast_watch',), requires=(After('1995.3.25'),),
          reward=(Event('belkan_war'),)),
    Focus('str_closed_ports', 'Ports Closed to Warships',
          "The cabinet closes every Wellowan port and field to the warships and military aircraft of all belligerents, and "
          "interns any that arrive. Neutrality becomes a rule rather than a mood. Some merchant trade suffers, both sides are "
          "equally annoyed, and the coast watch must enforce the rule in all weathers.",
          ('security', 'peace'), after=('str_war_news',), cost=10, exclusive=('str_open_ports',),
          reward=(SwapIdea('strait_watch', 'closed_ports'), Flag('posture_closed'))),
    Focus('str_open_ports', 'Neutral Ports, Open Trade',
          "The cabinet keeps every port open to merchant ships of all flags, and lets war cargo through at a premium on dues. "
          "The ports grow rich on a war they are not fighting. Each side suspects the other is supplied through Wellow, and the "
          "coast watch must still keep the warships out.",
          ('logistics', 'peace'), after=('str_war_news',), cost=10, exclusive=('str_closed_ports',),
          reward=(SwapIdea('strait_watch', 'open_ports'), Flag('posture_open'))),
    Focus('str_fallout', 'Measure the Waldreich Fallout',
          "Nuclear devices used in the Waldreich Mountains turn the meteorologists into the most important officials in the "
          "country. Sampling stations on the south coast and the islands track the winds and test rain, fish and milk. "
          "Publishing results calms some fears and stokes others, and the stations will run for years.",
          ('science', 'radar'), after=('str_war_news',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(Idea('fallout_watch'), Event('waldreich_light'))),
    Focus('str_after_lumen', 'After the Lumen Treaty',
          "The treaty signed in Lumen in June 1995 ends the Belkan War. Insurers return, coasters resume the southern routes and "
          "the coast watch stands down its reserve crews. The ports want the wartime rules lifted at once, and the navy wants "
          "them kept a little longer, just in case.",
          ('peace', 'logistics'), after_any=('str_closed_ports', 'str_open_ports'), requires=(After('1995.6.20'),),
          reward=(TimedIdea('postwar_lanes', 730), Stability(0.02))),
    Focus('str_defeated_neighbour', 'Fuel and Timber for Belka',
          "A defeated Belka across the narrow sea needs fuel, timber, food and ships, and has little to pay with. Wellowan "
          "owners can sell on credit, barter or wait. The cabinet backs credit for essential cargo, betting that a neighbour "
          "rebuilt with Wellowan help will remember it.",
          ('diplomacy', 'logistics'), after=('str_after_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          exclusive=('str_victorious_neighbour',), reward=(Idea('strait_trade'),)),
    Focus('str_victorious_neighbour', 'Vigil Toward a Victor',
          "A victorious Belka across the narrow sea is a neighbour with momentum, a hardened air force and new territory. "
          "Nobody in the capital expects it to turn north, but nobody can promise it will not. The coast watch becomes a "
          "permanent command, and the islands' garrisons stay at strength.",
          ('security', 'radar'), after=('str_after_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          exclusive=('str_defeated_neighbour',), reward=(Idea('strait_vigil'),)),
))

GARRISON = Branch('garrison', 'Hills, Marshes and Harbours', 1991, 'FOCUS_FILTER_ARMY_XP', (
    Focus('gar_review', 'Ten Formations for Sixteen Districts',
          "The army fields about ten infantry formations to defend sixteen districts, five of them islands that cannot be "
          "reinforced by road. Most formations sit on the main island near the capital. A review of where they stand, what they "
          "carry and how they would move by sea comes first, and it embarrasses almost everyone involved.",
          ('command', 'document'), reward=(Idea('garrison_review'), Event('one_army_many_islands'))),
    Focus('gar_highland_training', 'Training in the Northwest Highlands',
          "The northwestern highlands of the main island are mountain country where trucks struggle and infantry walks. A "
          "training area there, with a proper road to reach it, teaches companies to move and fight in hills that cover much "
          "of the country. Farmers lose grazing to firing ranges and say so loudly.",
          ('training', 'rail'), after=('gar_review',), reward=(Build('infrastructure', 1, 264), XP('army', 15))),
    Focus('gar_marsh_engineers', 'Engineers for the Marshes',
          "Marshes cover much of the northern lowland and the northeastern oil district, and the army has never trained to "
          "cross them. Engineer companies learn to lay mats, build causeways and bridge channels under pressure. The skills "
          "serve the civil road programme as much as the army, which helps the budget case.",
          ('tools', 'bridge'), after=('gar_review',), reward=(Research('engineers_tech', 0.5, 2),)),
    Focus('gar_battalions', 'A Battalion in Every District',
          "The district school wins: every district, island or not, raises and keeps its own trained battalion, recruited "
          "locally and commanded from its own depot. No island will ever be empty. Battalions on the islands train alone and "
          "cannot easily reinforce each other, and the army as a whole grows more parochial.",
          ('security', 'civil'), after_any=('gar_highland_training', 'gar_marsh_engineers'), cost=10,
          exclusive=('gar_sealift',), reward=(SwapIdea('garrison_review', 'district_battalions'),)),
    Focus('gar_sealift', 'Brigades That Travel by Sea',
          "The sea-lift school wins: fewer, better brigades based on the main island, trained to embark on ferries and colliers "
          "and land at any island harbour within days. The army becomes a mobile reserve. The islands depend on the ships "
          "arriving in time, and the merchant owners on not being requisitioned too often.",
          ('training', 'navy'), after_any=('gar_highland_training', 'gar_marsh_engineers'), cost=10,
          exclusive=('gar_battalions',), reward=(SwapIdea('garrison_review', 'sealift_brigades'),)),
    Focus('gar_rifle_works', 'A Rifle Works West of the Capital',
          "The army buys its rifles, mortars and ammunition abroad and waits for them. A state works in the district west of "
          "the capital makes small arms and shells under licence. It is a modest plant that gives the country a floor of "
          "self-supply, at prices well above what foreign makers charge.",
          ('industry', 'security'), after=('gar_review',), reward=(Build('arms_factory', 1, 245),)),
    Focus('gar_island_depots', 'Depots on the Northwest Island',
          "District battalions on the islands need weapons, food and fuel stored where they serve. A depot on the northwest "
          "island, with a road to its harbour, holds a month of supplies for the island battalions. Islanders gain jobs, and "
          "the army gains a reason to keep the coast road in good repair.",
          ('logistics', 'security'), after=('gar_battalions',), reward=(Build('infrastructure', 1, 17), XP('army', 10))),
    Focus('gar_ferry_exercise', 'Exercises on the Ferry Lines',
          "The sea-lift brigades borrow the subsidised ferries for a week and land a full brigade at the western islands. The "
          "exercise shows how long loading really takes and how few harbours can unload heavy equipment. Ferry passengers are "
          "furious for a week, and the staff learns more than it did in a year.",
          ('navy', 'training'), after=('gar_sealift',), requires=(HasFlag('ferry_network'),),
          reward=(XP('army', 20), Research('logistics_tech', 0.5, 2))),
    Focus('gar_union_guards', 'District Guards for the Union',
          "The union council raises district guards answerable jointly to the council and to each district, recruited locally "
          "and trained by the army. The guards are a bridge between the capital and the districts. The army regards them as "
          "amateurs, and the imperial movement regards them as a council militia.",
          ('security', 'assembly'), after=('gar_review',), requires=(HasFlag('gov_union'),), reward=(Idea('district_guards'),)),
    Focus('gar_southern_positions', 'Positions on the Southern Shore',
          "With war across the narrow sea, the army digs positions along the southern shore and garrisons the beaches nearest "
          "the far coast. Nobody expects a landing, but nobody wants to explain afterwards why there were no trenches. Soldiers "
          "spend a wet season digging and learn a great deal about their own coast.",
          ('security', 'tools'), after_any=('gar_battalions', 'gar_sealift'), requires=(After('1995.3.25'),),
          reward=(XP('army', 20), WarSupport(0.03))),
))

SKY = Branch('sky', 'A Rock Called Ulysses', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_named_danger', 'Astronomers Name a Danger',
          "In December 1994 the International Astronomical Union warns that the asteroid Ulysses may strike the Earth. In Wellow "
          "the news reaches the port taverns before it reaches the ministries. The government has to decide how to speak about "
          "a danger that may be years away, may fall anywhere and may never fall at all.",
          ('meteor', 'communications'), requires=(After('1994.12.10'),), reward=(Event('ulysses_warning'),)),
    Focus('sky_lowland_telescopes', 'Telescopes on the Northern Lowland',
          "The flat northern lowland has dark skies and plenty of room. Telescopes and a tracking radar there, run by a standing "
          "committee of astronomers, give Wellow its own measurements instead of borrowed bulletins. The station costs more than "
          "its science would justify in calmer years, and every newspaper visits it.",
          ('telescope', 'radar'), after=('sky_named_danger',), reward=(Idea('sky_watch'), Build('radar_station', 1, 255))),
    Focus('sky_grain_reserve', 'Granaries for the Bad Years',
          "If fragments disturb the weather, harvests may fail anywhere, and an island nation that imports grain is exposed. "
          "Granaries and a mill on the northern lowland hold a winter of food for the islands. Farmers get a guaranteed buyer, "
          "and the treasury pays for grain it hopes it will never need.",
          ('shelter', 'civil'), after=('sky_named_danger',), reward=(Idea('grain_reserve'), Build('industrial_complex', 1, 255))),
    Focus('sky_impact_announced', 'The Impact Is Announced',
          "In April 1996 the FCU announces to the world that Ulysses will strike the Earth. The question is no longer whether, "
          "but where and how badly. Wellow draws up impact plans for every district, with shelter lists, ferry schedules and "
          "food stocks. Every district office now has a binder nobody wants to open.",
          ('meteor', 'shelter'), after_any=('sky_lowland_telescopes', 'sky_grain_reserve'), requires=(After('1996.4.20'),),
          reward=(TimedIdea('impact_year', 1095),)),
    Focus('sky_relief_fleet', 'Ships for the Stricken Coasts',
          "The owners and the government agree that Wellow's greatest asset in a disaster is its merchant fleet. Hulls are "
          "earmarked to carry relief wherever fragments fall, at cost, with crews from volunteer lists. The country's ships "
          "will be away when the impact comes, which some owners and many islanders find hard to accept.",
          ('refugees', 'navy'), after=('sky_impact_announced',), cost=10, exclusive=('sky_home_waters',),
          reward=(Idea('relief_charters'), Flag('relief_fleet'))),
    Focus('sky_home_waters', 'Every Hull Home for the Impact',
          "The cautious answer brings every Wellowan hull home before the danger window and keeps it there. Ships lie in "
          "sheltered harbours, crews stay with their families and nothing is risked at sea. Foreign charterers take their "
          "business elsewhere, and the fleet's reputation for reliability takes years to recover.",
          ('shelter', 'logistics'), after=('sky_impact_announced',), cost=10, exclusive=('sky_relief_fleet',),
          reward=(Idea('home_waters'),)),
    Focus('sky_ferry_evacuation', 'A Ferry Out for Every Village',
          "If fragments threaten the coasts, the safest place for islanders is inland on the main island. The ferry timetable "
          "gains a hidden twin: an evacuation schedule assigning every coastal village a ferry, a harbour and a destination. "
          "Rehearsals disrupt the islands every summer, and nobody hopes to use it.",
          ('refugees', 'navy'), after=('sky_impact_announced',), requires=(HasFlag('ferry_network'),),
          reward=(TimedIdea('evacuation_plan', 1095),)),
    Focus('sky_roche_night', 'The Night the Rock Breaks',
          "In July 1999 Ulysses passes through the Earth's Roche limit, and the long wait is over. Wellow's telescopes report "
          "what they can see, and the impact plans go from binders to radio bulletins. Whatever falls and wherever it falls, the country that "
          "prepared calmly will recover faster than the one that panicked.",
          ('meteor', 'telescope'), after=('sky_impact_announced',), requires=(After('1999.7.8'),),
          reward=(Stability(0.03), Research('construction_tech', 0.5, 2))),
    Focus('sky_relief_voyages', 'Relief Voyages in the Impact Year',
          "When the impact year comes, the earmarked hulls sail. Wellowan colliers and coasters carry grain, fuel and tents to "
          "stricken ports that will take them, and come home empty. The voyages cost the state its insurance and the owners "
          "their profits, and give Wellow a name at sea that money cannot buy.",
          ('refugees', 'medal'), after=('sky_roche_night',), requires=(HasFlag('relief_fleet'),),
          reward=(SwapIdea('relief_charters', 'name_at_sea'), PP(20))),
    Focus('sky_insurers', 'Who Pays for a Falling Sky',
          "Foreign insurers write impact exclusions into every hull policy, leaving owners uncovered for the one risk everybody "
          "is discussing. A state reinsurance fund backs Wellowan hulls for impact damage at a fixed premium. It may cost the "
          "treasury a fortune or nothing, and nobody can say which until the sky clears.",
          ('economy', 'meteor'), after=('sky_impact_announced',), reward=(Stability(0.02), PP(-20), Research('industry', 0.5, 1))),
))

INSTITUTE = Branch('institute', 'The Maritime Polytechnic', 1993, 'FOCUS_FILTER_RESEARCH', (
    Focus('ins_found', 'Found a Maritime Polytechnic',
          "Wellow sends its engineers, navigators and radio technicians abroad to study, and many never return. A polytechnic in "
          "the capital, with faculties of marine engineering, navigation, radio and geology, keeps them at home. It takes a "
          "decade to earn a reputation, and its first professors have to be hired from foreign universities.",
          ('science', 'navy'), reward=(Idea('polytechnic'),)),
    Focus('ins_marine_weather', 'A Weather Service for Shipping',
          "Storms sink more Wellowan ships than any enemy ever has. A marine weather service with a station and a weather radar "
          "in the northeastern marsh district broadcasts forecasts to every master and ferry captain four times a day. Owners "
          "pay a fee in their dues and soon wonder how they managed without it.",
          ('telescope', 'communications'), after=('ins_found',), reward=(Idea('marine_weather'), Build('radar_station', 1, 250))),
    Focus('ins_radio_beacons', 'Radio Beacons Along the Coasts',
          "Masters still navigate the island sounds by lighthouses and memory. A chain of radio beacons along the main island "
          "and the western islands lets ships fix their position in fog and darkness. The beacons are simple and cheap, and "
          "every hostile navigator would use them too, which the navy points out.",
          ('communications', 'navy'), after=('ins_found',), reward=(Research('electronics', 0.5, 2), Research('radar_tech', 0.5, 1))),
    Focus('ins_ministry_labs', 'Laboratories Under the Ministries',
          "One school wants research run by the ministries: the navy's laboratories, the fields' geologists and the ferries' "
          "engineers, all funded from the budget and set to public priorities. Research follows the state's needs. It also "
          "follows the state's budget cycles, and good engineers dislike forms.",
          ('science', 'command'), after_any=('ins_marine_weather', 'ins_radio_beacons'), cost=10,
          exclusive=('ins_owner_labs',), reward=(Idea('ministry_labs'),)),
    Focus('ins_owner_labs', 'Laboratories Paid by the Owners',
          "The other school wants shipowners and oil firms to fund research they can use within years, with the polytechnic as "
          "their contractor and tax relief as the state's share. Research moves quickly toward profit. Problems nobody can sell "
          "a solution to remain unsolved for a long time.",
          ('science', 'economy'), after_any=('ins_marine_weather', 'ins_radio_beacons'), cost=10,
          exclusive=('ins_ministry_labs',), reward=(Idea('owner_labs'),)),
    Focus('ins_chamber_grants', 'Research Grants Voted by the Chamber',
          "The restored chamber votes research grants in open session, with every deputy arguing for a project in their own "
          "district. Some grants are wasted on prestige. Others reach island schools and small firms that never had a hearing "
          "under the ordinances, and the polytechnic gains friends in every district.",
          ('ballot', 'science'), after=('ins_found',), requires=(HasFlag('gov_republic'),),
          reward=(Research('industry', 0.5, 2), Stability(0.02))),
    Focus('ins_admin_engineers', 'Engineers in the Administration',
          "The standing administration recruits polytechnic graduates straight into its offices, where they plan roads, ports "
          "and power lines by calculation rather than by petition. The administration becomes more competent and more "
          "technical, and its plans arrive with costings attached. Districts that cannot argue in numbers find themselves "
          "ignored more efficiently than before, and say so.",
          ('tools', 'document'), after=('ins_found',), requires=(HasFlag('gov_standing'),),
          reward=(Research('construction_tech', 0.5, 2), PP(25))),
    Focus('ins_district_schools', 'Technical Schools in the Districts',
          "The elected island councils fund technical schools in their own harbour towns, teaching engine repair, radio and "
          "refrigeration. Young islanders no longer have to leave home to learn a trade. The schools are uneven, some excellent "
          "and some poor, because each council runs its own.",
          ('training', 'civil'), after=('ins_found',), requires=(HasFlag('districts_devolved'),),
          reward=(Research('engineers_tech', 0.5, 1), Stability(0.03))),
    Focus('ins_prefect_radio', 'A Radio Net for the Prefects',
          "The island prefecture links every prefect's office by radio to the capital, with daily reports and instructions. "
          "Decisions that once waited for the ferry now take an hour. The net is efficient and impersonal, and islanders learn "
          "that their prefect can no longer claim the capital never answered.",
          ('communications', 'command'), after=('ins_found',), requires=(HasFlag('districts_prefects'),),
          reward=(Research('radar_tech', 0.5, 2), PP(20))),
))

DISTANT = Branch('distant', 'A Distant War, a Near Sea', 2002, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('dst_estovakia', 'Sanctions on Estovakia',
          "In March 2002 Osea, Emmeria and other nations join in economic sanctions against Estovakia, citing corruption. "
          "Wellow is not asked to join, but Wellowan hulls carry cargo to every coast, including Estovakian ones. The registry "
          "has to decide whether foreign sanctions lists bind ships that fly its flag.",
          ('diplomacy', 'scales'), requires=(After('2002.3.20'),), reward=(PP(25), Tooltip('Opens the registry choice on Estovakian cargo.'))),
    Focus('dst_bar_cargo', 'Bar Estovakian Cargo',
          "The registry writes the sanctions into its own rules and bars Wellowan hulls from Estovakian cargo. Owners lose a "
          "route, and Osea and Emmeria note the gesture. The register becomes, in practice, a tool of foreign policy, which "
          "every future government will be tempted to use again.",
          ('document', 'diplomacy'), after=('dst_estovakia',), exclusive=('dst_own_rules',), reward=(Idea('sanction_rules'),)),
    Focus('dst_own_rules', 'The Registry Keeps Its Own Rules',
          "The registry declines to apply any foreign sanctions list and keeps its own rules on cargo and conduct. Owners keep "
          "every route open. Wellow's flag becomes more attractive to some owners and more suspect to some governments, and "
          "inspectors must watch which cargo the flag is carrying.",
          ('logistics', 'scales'), after=('dst_estovakia',), exclusive=('dst_bar_cargo',), reward=(Idea('registry_discretion'),)),
    Focus('dst_usean_war', 'War over Usea',
          "In August 2003 the FCU demands that Erusea withdraw from the railgun complex and San Salvacion, and an allied force "
          "is formed. The war that follows is a continent away, but within a week insurers have rewritten every premium on the "
          "Usean routes and charterers are offering double rates for unnamed cargo.",
          ('communications', 'economy'), requires=(After('2003.8.22'),), reward=(Event('distant_war'),)),
    Focus('dst_no_war_cargo', 'No Military Cargo to Usea',
          "The country that closed its ports to warships in 1995 applies the same rule at sea: no Wellowan hull may carry "
          "military cargo to the war over Usea. Owners lose lucrative charters. The flag keeps its neutrality, and the navy "
          "need not explain why it cannot escort anyone that far.",
          ('peace', 'logistics'), after=('dst_usean_war',), requires=(HasFlag('posture_closed'),), reward=(Idea('no_war_cargo'),)),
    Focus('dst_war_risk', 'War Risk Cover for Usean Runs',
          "The country that kept its ports open in 1995 keeps its ships sailing in 2003. A state-backed war-risk pool insures "
          "Wellowan hulls on the Usean routes at a fixed premium. Freight income rises sharply. If a Wellowan ship is sunk, the "
          "treasury pays, and the newspapers ask what it was carrying.",
          ('economy', 'navy'), after=('dst_usean_war',), requires=(HasFlag('posture_open'),), reward=(Idea('war_risk_cover'),)),
    Focus('dst_flagged_hulls', 'Foreign Owners, Wellowan Flags',
          "The open registry now includes hundreds of foreign-owned hulls, some of them sailing into the war zone on charters "
          "their owners will not describe. Inspectors are sent to the busiest foreign ports to check cargo and crews. The fees "
          "pay for the inspectors, and some owners quietly leave the register.",
          ('document', 'security'), after=('dst_usean_war',), requires=(HasFlag('registry_open'),),
          reward=(Stability(0.02), PP(30), Research('logistics_tech', 0.5, 1))),
    Focus('dst_line_charters', 'The Line Declines the War',
          "The national line receives charter offers for the Usean routes and must decide as a state enterprise what a private "
          "owner would decide for profit. Its board declines military cargo and redeploys the ships to the northern routes the "
          "war has emptied. Its rivals take the risky money, and the line keeps its ships.",
          ('navy', 'peace'), after=('dst_usean_war',), requires=(HasFlag('registry_national'),),
          reward=(Stability(0.03), XP('navy', 15), Research('naval_equipment', 0.5, 1))),
    Focus('dst_mutual_claims', 'The Mutual Pays Its War Claims',
          "Two member ships of the shipowners mutual are damaged on Usean routes, and the pool must pay or fail. It pays, raises "
          "its premiums and tightens its rules on war cargo. The owners who built the mutual discover that sharing risk means "
          "sharing someone else's bad decision.",
          ('economy', 'scales'), after=('dst_usean_war',), requires=(HasFlag('registry_mutual'),),
          reward=(Stability(-0.01), PP(35), Research('industry', 0.5, 1))),
    Focus('dst_tanker_rates', 'Tanker Rates Soar',
          "War over Usea drives tanker rates to heights the crude exporters never imagined, and Wellowan tankers are booked a "
          "year ahead. The oil money floods in. The fleet now buys its own fuel back at wartime prices, and the ferries pay "
          "more for every crossing than they did before the war.",
          ('logistics', 'economy'), after=('dst_usean_war',), requires=(HasFlag('fields_export'),),
          reward=(PP(50), Stability(-0.02), Research('excavation_tech', 0.5, 2))),
    Focus('dst_fuel_hedge', 'Fuel Held Against the War',
          "The capital fuel reserve, built for exactly this kind of year, keeps the ferries and heating plants running at "
          "pre-war prices while world markets swing. Its rules are tested, argued over and upheld. The reserve's managers "
          "finally have an answer for everyone who called it waste.",
          ('shelter', 'logistics'), after=('dst_usean_war',), requires=(HasFlag('fuel_reserve'),),
          reward=(Stability(0.04), Research('synth_resources', 0.5, 1))),
    Focus('dst_fifteen_years', 'The Panel Drawn by Lot',
          "With the war over Usea ended in September 2005, an independent panel drawn by lot reviews how Wellow has governed "
          "itself since 1991: its districts, its register, its yards and its fields. The review promises nothing about the "
          "years ahead. It gives whoever governs next an honest starting point.",
          ('document', 'assembly'), after_any=('dst_bar_cargo', 'dst_own_rules', 'dst_usean_war'), requires=(After('2005.9.19'),),
          reward=(Event('fifteen_years'), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (ADMIN, DISTRICTS, REGISTER, FIELDS, YARDS, FLEET, AIR, STRAIT, GARRISON, SKY, INSTITUTE, DISTANT)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('winter_ferries', 'Subsidise the Winter Ferries',
                'Pay for extra winter sailings to every island district for half a year. Costs political power each season it is used.',
                cost=40, effects=(TimedIdea('winter_ferries', 180),), requires=(HasFlag('ferry_network'),), cooldown=365),
    DecisionDef('draw_fuel_reserve', 'Draw on the Fuel Reserve',
                'Open the capital fuel reserve to the ferries, the fleet and the heating plants for four months.',
                cost=50, effects=(TimedIdea('fuel_drawn', 120),), requires=(HasFlag('fuel_reserve'),), cooldown=365),
    DecisionDef('charter_relief', 'Charter a Relief Convoy',
                'Charter merchant hulls at cost and send a relief convoy under a single navy escort. Once only.',
                cost=60, effects=(Event('relief_voyage'),), requires=(HasFlag('relief_fleet'),)),
    DecisionDef('coast_reserve', 'Call Out the Coast Reserve',
                'Bring the reserve crews of the coast watch and the fleet out for a season of drills.',
                cost=35, effects=(XP('navy', 10), WarSupport(0.02)), cooldown=180),
    DecisionDef('island_airstrip', 'Pave the Far West Airstrip',
                'Lay a hard runway in the westernmost island district so that aircraft can reach the far end of the chain. Once only.',
                cost=75, effects=(Build('air_base', 2, 131),), requires=(HasFlag('island_airfields'),)),
    DecisionDef('dues_amnesty', 'Amnesty for Unpaid Port Dues',
                'Forgive old unpaid harbour dues for owners who register honestly this year. Once only.',
                cost=30, effects=(Stability(0.03), WarSupport(-0.01)), requires=(Completed('reg_harbour_offices'),)),
)
