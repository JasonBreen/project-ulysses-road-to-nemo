"""Chopinburg (CHO): bespoke national tree, 1991-2020.

Everything here is provisional gameplay built on the inherited 1991 history and
state files. Official Usea dates appear only as dated pressures; no Chopinburg
outcome is claimed from them.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='CHO', name='Chopinburg', root='usea', package='minors_a',
                  themes=('industry', 'navy', 'assembly'), max_columns=23)

SOURCES = (
    Source('Provisional gameplay',
           'Every Chopinburg focus, idea, office and event is provisional gameplay. It is grounded in the inherited 1991 '
           'history (suspended elections, CNEA membership, capital state 4), the six 1991 states and their resources and '
           'buildings, and the world-start calibration (coastal dispersal role, three destroyers, one submarine, '
           'forty-eight fighters). No Chopinburg-specific official source exists for 1991-2020.',
           'history/countries/CHO - Chopinburg.txt; history/states 4, 32, 459, 512, 520, 539; '
           'tools/world_foundation/country_registry.json (CHO); tools/world_starts/profiles.json (CHO)'),
    Source('Mod provenance',
           'District captions B, C, E and F come from the regional label pass; state 512 has no district caption and is '
           'called the desert hinterland in text. The flats weather (heavy rain, mud) is read from strategic region 71.',
           'mod/2985041246/localisation/english/replace/ac_world_regional_labels_l_english.yml; '
           'mod/2985041246/map/strategicregions/71-Chopinburg Flats.txt'),
    Source('Official',
           'Usea-wide dates used only as dated pressures and focus gates; the Chopinburg response to each is provisional.',
           'Chronicle, 1995 / 12.31; 1996 / 04.20; 1997 / 05.30; 1998 / 06.19; 1999 / 07.08; 2000 / 04.21; '
           '2003 / SUMMER; 2003 / 08.22 (rows in docs/USEAN_CONTINENTAL_WAR.md)'),
    Source('Mod provenance',
           'The Chronicle 2019 / 05.30 row mentions Chopinburg airspace but gives Chopinburg no political status; the ledger '
           'keeps that place name unmapped to the CHO tag, so this tree does not use it.',
           'tools/lore/chronicle.json, Chronicle 2019 / 05.30 conflicts note'),
)

# --- ideas -------------------------------------------------------------------------------------
IDEAS = (
    IdeaDef('unmandated_ministries', 'Ministries Without a Mandate',
            'The National Administration acts quickly by decree, but nobody voted for it and the districts know it.',
            {'political_power_gain': 0.10, 'stability_factor': -0.04}, ('document', 'assembly')),
    IdeaDef('charter_rolls', 'Charter Rolls',
            'Voter registers in every district and a ballot on the calendar. Decrees give way to debate.',
            {'stability_factor': 0.04, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('performance_tables', 'Ministry Performance Tables',
            'Published targets for every ministry, with officials replaced for repeated misses.',
            {'political_power_factor': 0.08, 'production_speed_buildings_factor': 0.04}, ('document', 'economy')),
    IdeaDef('rally_halls', 'Rally Halls',
            'The nationalist movement holds public halls and seats on district committees.',
            {'war_support_factor': 0.06, 'stability_factor': -0.02}, ('assembly', 'security')),
    IdeaDef('charter_defended', 'The Charter Defended',
            'Ballots held on time through the 1997 emergency make the charter harder to suspend again.',
            {'stability_factor': 0.06, 'political_power_gain': 0.05}, ('ballot', 'scales')),
    IdeaDef('performance_audit', 'Audited Directorate',
            'The administration polices its own contracts with the army and publishes the results.',
            {'political_power_factor': 0.10, 'army_org_factor': 0.03}, ('scales', 'document')),
    IdeaDef('rally_discipline', 'Disciplined Rally Squads',
            'Movement volunteers serve under the coast watch chain of command, without private uniforms.',
            {'war_support_factor': 0.06, 'stability_factor': 0.02}, ('security', 'command')),
    IdeaDef('open_budget', 'Open District Budget',
            'One budget book, printed by district, read and argued over in every district office.',
            {'stability_factor': 0.03, 'production_speed_infrastructure_factor': 0.10}, ('economy', 'document')),
    IdeaDef('state_rubber_board', 'State Rubber Board',
            'The state buys, grades and sells all latex from District C under one mark.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('economy', 'industry')),
    IdeaDef('grower_cooperatives', 'Grower Cooperatives',
            'District C growers grade, store and sell their own latex; the state collects export duty.',
            {'stability_factor': 0.04, 'consumer_goods_factor': -0.02}, ('civil', 'economy')),
    IdeaDef('grove_leases', 'Leased Groves',
            'Outside buyers hold long leases on whole blocks of District C groves.',
            {'production_speed_buildings_factor': 0.08, 'political_power_factor': -0.05}, ('document', 'economy')),
    IdeaDef('flood_wardens', 'Flood Wardens',
            'Rain gauges and wardens in every district of the flats record where water gathers.',
            {'production_speed_infrastructure_factor': 0.10}, ('tools', 'civil')),
    IdeaDef('drained_flats', 'Drainage Authority',
            'A permanent drainage authority keeps the flats usable in every season.',
            {'production_speed_infrastructure_factor': 0.15, 'supply_consumption_factor': -0.04}, ('bridge', 'tools')),
    IdeaDef('plateau_smelters', 'Plateau Smelters',
            'District F ships finished metal and fuel instead of ore and crude.',
            {'production_factory_efficiency_gain_factor': 0.06, 'stability_factor': -0.02}, ('industry', 'tools')),
    IdeaDef('ore_trains', 'Ore Trains',
            'Raw ore and crude run down from the plateau to the capital works.',
            {'production_speed_industrial_complex_factor': 0.08, 'production_speed_infrastructure_factor': 0.05},
            ('rail', 'industry')),
    IdeaDef('modern_plateau_mills', 'Modern Plateau Mills',
            'Rebuilt furnaces and rolling lines keep District F competitive.',
            {'production_factory_efficiency_gain_factor': 0.08, 'production_factory_max_efficiency_factor': 0.04},
            ('industry', 'science')),
    IdeaDef('double_ore_line', 'Double-Tracked Ore Line',
            'Two tracks and modern wagons carry District F output to the capital.',
            {'production_speed_industrial_complex_factor': 0.10, 'production_speed_infrastructure_factor': 0.10},
            ('rail', 'logistics')),
    IdeaDef('plains_homesteads', 'Plains Homesteads',
            'Families farm drained District B land on the way to holding title.',
            {'stability_factor': 0.04, 'production_speed_buildings_factor': -0.03}, ('civil', 'rebuild')),
    IdeaDef('district_b_state_farms', 'District B State Farms',
            'Large ministry farms with hired crews feed the capital and the army.',
            {'consumer_goods_factor': -0.03, 'stability_factor': -0.02}, ('economy', 'logistics')),
    IdeaDef('district_grants', 'District Grants Formula',
            'Development grants follow a published formula instead of favours.',
            {'production_speed_buildings_factor': 0.06}, ('scales', 'economy')),
    IdeaDef('air_instructors', 'Air Arm Instructors',
            'Instructors and a fixed training syllabus for the small fighter force.',
            {'experience_gain_air_factor': 0.10, 'training_time_factor': -0.05}, ('air', 'training')),
    IdeaDef('air_mechanics_school', 'Air Arm Mechanics School',
            'Apprentice mechanics keep more fighters serviceable on any given day.',
            {'experience_gain_air_factor': 0.12, 'air_mission_efficiency': 0.04}, ('tools', 'air')),
    IdeaDef('fighter_screen', 'Interceptor Screen',
            'Fighters trained to meet hostile aircraft over home territory under ground control.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('maritime_strike', 'Coastal Strike Wing',
            'Fighters trained to carry bombs and rockets against ships off the coast.',
            {'air_mission_efficiency': 0.08, 'naval_coordination': 0.04}, ('air', 'navy')),
    IdeaDef('pilot_service', 'Harbour Pilot Service',
            'Trained pilots for the four naval harbours of District C and District E.',
            {'navy_org_factor': 0.05, 'naval_speed_factor': 0.03}, ('navy', 'training')),
    IdeaDef('escort_convoys', 'Convoy Escort Doctrine',
            'Destroyers and armed merchant ships escort the coastal convoys.',
            {'naval_coordination': 0.08, 'navy_org_factor': 0.03}, ('navy', 'logistics')),
    IdeaDef('offshore_pickets', 'Offshore Pickets',
            'The submarine and patrol craft watch the far approaches.',
            {'naval_coordination': 0.04, 'naval_speed_factor': 0.05}, ('submarine', 'radar')),
    IdeaDef('shelter_levy', 'Shelter Levy',
            'A special levy funds shelters, sirens and reserves built by national ministries.',
            {'stability_factor': 0.05, 'consumer_goods_factor': 0.04}, ('shelter', 'economy')),
    IdeaDef('shelter_compact', 'Treaty Council Shelter Compact',
            'Shared designs, engineers and warning data with other Treaty Council members.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': 0.05, 'political_power_factor': -0.05},
            ('shelter', 'diplomacy')),
    IdeaDef('strategic_reserve', 'Grain and Fuel Reserve',
            'National stores of grain, medicine and fuel on the plateau and in the capital.',
            {'supply_consumption_factor': -0.05, 'stability_factor': 0.02}, ('logistics', 'shelter')),
    IdeaDef('coup_alert', 'Coup Alert',
            'Every unit must report its loyalty; the capital watches its own army.',
            {'stability_factor': -0.04, 'army_core_defence_factor': 0.08}, ('security', 'command')),
    IdeaDef('army_loyalty_board', 'Army Loyalty Board',
            'A standing commission reviews unit commanders and their orders.',
            {'army_org_factor': 0.05, 'stability_factor': 0.02}, ('scales', 'command')),
    IdeaDef('professional_army', 'Professional Army Code',
            'A written professional code replaces emergency rule over the army.',
            {'army_org_factor': 0.08, 'training_time_army_factor': -0.08}, ('medal', 'training')),
    IdeaDef('civil_oversight', 'Civilian Oversight Board',
            'The army answers to a civilian board that publishes its orders.',
            {'stability_factor': 0.04, 'army_org_factor': -0.03}, ('scales', 'security')),
    IdeaDef('civil_service_code', 'Civil Service Code',
            'Oversight of the army is written into a permanent civil service code.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('document', 'scales')),
    IdeaDef('mutiny_code_rules', 'Written Mutiny Code',
            'A published code defines mutiny, its judges and its penalties.',
            {'army_org_factor': 0.04, 'surrender_limit': 0.05}, ('document', 'command')),
    IdeaDef('council_air_watch', 'Treaty Council Air Watch',
            'Radar reports and debris tracks shared with other Treaty Council members.',
            {'air_detection': 0.10, 'political_power_factor': -0.05}, ('radar', 'diplomacy')),
    IdeaDef('declared_neutral_airspace', 'Declared Neutral Airspace',
            'No foreign military aircraft may use Chopinburg airspace.',
            {'stability_factor': 0.03, 'air_defence_factor': 0.05}, ('air', 'peace')),
    IdeaDef('diplomatic_channels', 'Open Channels',
            'Trade missions and liaison officers keep talks open with every Usean government.',
            {'political_power_gain': 0.15}, ('diplomacy', 'communications')),
    IdeaDef('capital_air_defence', 'Capital Air Defence Ring',
            'Anti-air batteries around the capital, fed by the radar posts.',
            {'static_anti_air_damage_factor': 0.12, 'air_defence_factor': 0.05}, ('missile', 'radar')),
    IdeaDef('relief_fund', 'Relief Fund',
            'Money moved from other budgets into relief stores, hospitals and roads.',
            {'production_speed_buildings_factor': 0.05, 'stability_factor': 0.02}, ('medical', 'economy')),
    IdeaDef('relief_command', 'Relief Command',
            'Emergency powers, ration cards and relief posts in every district.',
            {'stability_factor': 0.03, 'political_power_gain': -0.10}, ('medical', 'command')),
    IdeaDef('harbour_camp_system', 'Harbour Camps',
            'Organised camps for displaced people at the District C and District E harbours.',
            {'stability_factor': -0.03, 'political_power_gain': 0.10}, ('refugees', 'navy')),
    IdeaDef('inland_dispersal', 'Inland Dispersal',
            'Displaced people move quickly to small reception points in every district.',
            {'stability_factor': 0.03, 'production_speed_buildings_factor': -0.05}, ('refugees', 'logistics')),
    IdeaDef('field_hospital_network', 'Field Hospitals',
            'Tent and school hospitals spread medical care across the flats.',
            {'stability_factor': 0.04}, ('medical', 'shelter')),
    IdeaDef('austerity_ledger', 'Lean Budget',
            'New projects cut, salaries frozen and district grants delayed.',
            {'consumer_goods_factor': -0.04, 'stability_factor': -0.03}, ('economy', 'scales')),
    IdeaDef('balanced_ledger', 'Balanced Ledger',
            'A balanced budget with the finance ministry holding a veto over new spending.',
            {'consumer_goods_factor': -0.02, 'political_power_factor': 0.05}, ('scales', 'economy')),
    IdeaDef('debt_moratorium', 'Rescheduled Relief Debts',
            'Relief loans spread over a decade at a higher total cost.',
            {'political_power_gain': 0.10}, ('document', 'economy')),
    IdeaDef('coast_neutrality', 'Armed Coastal Neutrality',
            'A full guard on the coast, harbours and airspace; no side may use them.',
            {'army_core_defence_factor': 0.08, 'war_support_factor': 0.05}, ('security', 'peace')),
    IdeaDef('quiet_logistics', 'Quiet Logistics',
            'Fuel, rubber and repair work sold to the coalition while staying formally outside the war.',
            {'production_speed_arms_factory_factor': 0.10, 'stability_factor': -0.03}, ('logistics', 'industry')),
    IdeaDef('wartime_trade', 'Trade With Every Side',
            'Rubber, fuel and repairs sold to any buyer through neutral brokers.',
            {'production_speed_buildings_factor': 0.08, 'war_support_factor': -0.05}, ('economy', 'navy')),
    IdeaDef('war_rationing', 'Fuel and Tyre Rationing',
            'Private fuel and tyres rationed to keep the services supplied.',
            {'supply_consumption_factor': -0.05, 'stability_factor': -0.03}, ('logistics', 'document')),
    IdeaDef('recovery_programme', 'Recovery Compact',
            'A ten-year programme for harbours, plateau, districts and government.',
            {'production_speed_buildings_factor': 0.08, 'stability_factor': 0.02}, ('rebuild', 'document')),
    IdeaDef('steady_growth', 'Compact Results',
            'The compact programme becomes the normal way of government.',
            {'production_factory_max_efficiency_factor': 0.04, 'stability_factor': 0.03}, ('rebuild', 'economy')),
    IdeaDef('technical_college', 'National Technical College',
            'Engineers, controllers and chemists trained at home.',
            {'research_speed_factor': 0.05}, ('science', 'training')),
    IdeaDef('graduate_service', 'Graduate Public Service',
            'Technically trained graduates in the ministries and district offices.',
            {'research_speed_factor': 0.06, 'political_power_factor': 0.05}, ('science', 'document')),
)

# --- offices -----------------------------------------------------------------------------------
OFFICES = (
    Office('charter_council', 'Charter Council',
           'An elected collective council that took the ministries from the National Administration and restored the '
           'charter election calendar. It governs by majority vote and answers to the national ballot.',
           'democratic', 'centrism', elections=True),
    Office('administrative_directorate', 'Administrative Directorate',
           'A board of senior administrators that governs by published plan and targets, with elections suspended.',
           'neutrality', 'oligarchism'),
    Office('renewal_committee', 'National Renewal Committee',
           'A committee drawn from the leadership of the nationalist movement, governing without elections.',
           'fascism', 'ultranationalism'),
    Office('defence_directorate', 'Coastal Defence Directorate',
           'A directorate of senior officers and security officials seated after the 1997 coup to hold the coast.',
           'neutrality', 'stratocracy'),
    Office('recovery_assembly', 'Recovery Assembly',
           'An assembly chosen at the first open national election after the war years, charged with the recovery compact.',
           'democratic', 'social_democracy', elections=True),
    Office('governors_council', 'Council of District Governors',
           'The six district governors, governing together under the recovery compact with elections still suspended.',
           'neutrality', 'conservatism_na'),
)

# --- events ------------------------------------------------------------------------------------
EVENTS = (
    EventDef('administration_audit', 'The Administration Audit', (
        "The audit began in the finance ministry, where clerks carried ledgers up from basement stores that had not been "
        "opened since the election calendar was suspended. Within a month the auditors had found offices with more staff on "
        "paper than chairs at their desks, district grants approved by officials who no longer held their posts, and "
        "contracts renewed year after year without a single tender.",
        "The findings travelled faster than the auditors. In the capital, nationalist speakers read the worst entries aloud "
        "in their halls and demanded a cleaner state. Senior administrators answered that the ministries had kept the "
        "country fed, paid and defended through difficult years, and that a handful of bad ledgers did not make a failed "
        "government. The district delegates waiting in the capital mostly asked when the roads would come.",
        "The National Administration now has to decide what the audit is for. It can publish everything and let the public "
        "judge, accepting the damage to its own standing. It can keep the findings inside government and repair the worst "
        "offices quietly. Either way, the audit has ended the comfortable assumption that nobody would ever look.",
    ), (Option('Publish the full audit.', (Stability(-0.02), PP(60))),
        Option('Repair the worst offices quietly.', (Stability(0.02), PP(20)))), picture=1),
    EventDef('rubber_census', 'The Grove Census', (
        "The surveyors spent the dry weeks walking the District C groves with tally books, measuring tapes and a letter of "
        "authority that few growers had ever seen. They counted trees row by row, noted which were tapped and which had been "
        "abandoned, and asked each family who owned the land. Many families did not know; others knew very well and refused "
        "to say.",
        "The result surprised the capital. The groves are larger and older than the ministry records claimed, and a real "
        "share of the latex leaves through small coves and private jetties rather than the three harbours. Some growers are "
        "prosperous and well organised. Many more sell to middlemen at whatever price is offered on the day, and owe money "
        "to the same men.",
        "The census can be published grove by grove, giving growers the same figures the state holds and inviting arguments "
        "over every number. Or it can stay in the ministry, where it becomes a tool for setting quotas and prices that nobody "
        "outside can check. Either choice will shape the trade on the rubber coast for years.",
    ), (Option('Publish the census, grove by grove.', (Flag('census_public'), Stability(0.02))),
        Option('Keep the figures inside the ministry.', (Flag('census_sealed'), PP(40)))), picture=0),
    EventDef('plateau_survey', 'Ore Samples From the Plateau', (
        "The drilling teams spent a hot season on the District F plateau, sinking cores beside the old workings and along "
        "the dry valleys between the mining towns. Their samples went first to a field laboratory in a borrowed schoolroom, "
        "then down the slow plateau railway to the capital, where the mines ministry laid them out on long tables and argued "
        "over them for weeks. Some of the cores broke on the way down and had to be drilled again.",
        "The seams are good. Oil, aluminium ore and iron are all present in quantities that justify investment for decades, "
        "though the richest deposits lie deeper than the current workings and will need pumps, power and proper "
        "engineering. Water is the binding limit. Every new works on the plateau will compete with the mining towns for the "
        "same scarce wells.",
        "The survey turns a vague hope into a concrete choice. The country can build its processing works on the plateau, "
        "beside the seams, or carry the raw material down to the capital where power and labour already exist. Before that "
        "choice, the ministry must decide how to spend the first money the survey has justified.",
    ), (Option('Fund deeper drilling first.', (Research('excavation_tech', 0.5, 1),)),
        Option('Fund new wells for the mining towns first.', (Stability(0.02), PP(15)))), picture=2),
    EventDef('empty_districts', 'Two Districts Without Roads', (
        "The survey teams came back from District B and the desert hinterland with notebooks full of what was missing. "
        "District B has good flat soil that floods in the rains, a scattering of farms, and tracks that close for weeks at a "
        "time. The hinterland has sand, scrub, a few herding families and almost no water away from the coast.",
        "Neither district has a works, an airfield or a paved road. Both send delegates to the capital who ask, every year, "
        "why the state collects taxes there and builds nothing in return. Officials answer that money spent where nobody "
        "lives is money wasted. The delegates reply that nobody will live there until the money is spent.",
        "The survey cannot settle that argument, but it can decide where the first road goes. District B is close to the "
        "capital and could feed it. The hinterland is larger, emptier and harder, but it lies across the routes between the "
        "coast and the plateau. The ministry has money for one start this year, and the other district will have to wait. "
        "Its delegates have already said they will remember which district was chosen.",
    ), (Option('Start with the District B plains.', (Build('infrastructure', 1, 32),)),
        Option('Start with the desert hinterland.', (Build('infrastructure', 1, 512),))), picture=2),
    EventDef('yard_inventory', 'The Yards in District E', (
        "The inspectors counted three dockyards in District E, each with slipways laid down for a different generation of "
        "ships. One yard still builds small merchant hulls. One repairs the navy's destroyers and its single submarine. The "
        "third mostly waits for work, its cranes kept turning by a skeleton crew who remember busier years.",
        "The navy's own figures were worse than expected. Spare parts for the destroyers come from abroad and arrive late. "
        "The submarine spends more time in the yard than at sea. The merchant fleet that carries the country's trade along "
        "the coast is old, and many of its masters have never sailed in company with a warship. The coast is long and the "
        "force watching it is small. Several officers privately call the navy a coast guard with a few warships attached.",
        "The inventory leaves the admiralty with a choice about what to fix first. It can spend the yards' limited capacity "
        "refitting the ships it already has, or drawing up modern designs for escorts the country may build later. Neither "
        "choice will satisfy the officers who want both, and the budget allows only one.",
    ), (Option('Refit the ships we have.', (XP('navy', 15),)),
        Option('Draw up new escort designs.', (Research('naval_equipment', 0.5, 1),))), picture=0),
    EventDef('ulysses_warning', 'The Asteroid Warning', (
        "The announcement from Central Usea on 20 April 1996 reached the ministries by wire before it reached the "
        "newspapers, and for a few hours officials argued over what to say. By evening the radio stations had the story "
        "anyway. The asteroid Ulysses would strike the Earth, its fragments could fall anywhere, and nobody in the capital "
        "could say what that meant for a small coastal country.",
        "The next morning the queues began: at banks, at grocers, at the fuel depot beside the air base. Meeting halls "
        "filled every evening. The flood wardens, who had spent years measuring rain, found themselves answering questions "
        "about orbits. The ministries had plans for floods, storms and the occasional fire, but none for something falling "
        "out of the sky. Several districts asked the capital for instructions that nobody had yet written.",
        "The government now has to decide how it will speak about the danger in the years before the pass. Telling people "
        "everything the astronomers know builds trust but feeds fear with every revised forecast. Releasing only confirmed "
        "figures keeps the markets calmer but invites rumours. Either way, the shelters, stores and drills must start now.",
    ), (Option('Tell the public everything the astronomers know.', (Flag('open_warning'), Stability(-0.02))),
        Option('Release only what the ministries can confirm.', (Flag('managed_warning'), Stability(0.02)))),
        citation='the date is from Chronicle, 1996 / 04.20; the national response is not sourced', picture=1),
    EventDef('coup_news', 'News of the May Coup', (
        "On 30 May 1997 news reached the capital that a coup had broken out across Usea. The reports were confused and "
        "contradictory: units declaring for one side or another, airfields closed, radio stations silent. Unified Command "
        "was moving against the plotters, but nobody in the ministries could say how far the coup had spread or who might "
        "be part of it.",
        "The government's first act was to call every army unit and ask it to report. Most did within hours. Some took a "
        "day, citing broken telephones and absent commanders; a few reported only after senior officers drove out to see "
        "them in person. No shots were reported in Chopinburg, but nobody in the ministries slept well either. "
        "Rumours of secret meetings in the officers' clubs circulated for days, and none could be confirmed or denied.",
        "Now the government must decide how to hold the army until the crisis passes. It can confine units to barracks "
        "until each one has reported and been checked, which is safe but leaves the streets without soldiers. Or it can keep "
        "loyal units visible in the capital's streets, which reassures some people and frightens others.",
    ), (Option('Confine every unit to barracks until it reports.', (Flag('barracks_confined'), Stability(0.02))),
        Option('Keep loyal units in the capital streets.', (Flag('army_in_streets'), WarSupport(0.03)))),
        citation='the date is from Chronicle, 1997 / 05.30; the national response is not sourced', picture=1),
    EventDef('directorate_seated', 'The Directorate Takes the Ministries', (
        "The Coastal Defence Directorate took over the ministries on a quiet morning. Its members, senior officers and "
        "security officials, arrived in civilian clothes and met the permanent secretaries one by one. Orders went out by "
        "telephone: the election calendar suspended, district councils advisory only, and every ministry required to report "
        "its readiness for further emergencies.",
        "The capital reacted with a mixture of relief and unease. Shopkeepers welcomed the promise of order after weeks of "
        "rumour. Lawyers and journalists noticed that the first decree had no end date. In the districts, governors waited "
        "to see whether the new government would listen to them or simply send instructions down the wire. "
        "The nationalist halls, the business chambers and the old administrators all sent letters of congratulation, "
        "each hoping for something different in return.",
        "The Directorate must now decide how to present itself. It can publish a date by which it will hand power back, "
        "which reassures the public but sets a deadline that will be hard to meet. Or it can govern without a date and rely "
        "on results to justify itself, which leaves every critic free to say it never intends to leave.",
    ), (Option('Publish a date for handing back power.', (Stability(0.03),)),
        Option('Govern without a date.', (PP(50), Stability(-0.02)))), picture=1),
    EventDef('stonehenge_debate', 'The Railgun Debate', (
        "Central Usea completed Stonehenge on 19 June 1998: eight railguns in a desert region of neutral San Salvacion, "
        "built by an international project to break up the fragments of Ulysses before they reached the ground. The capital "
        "newspapers printed diagrams of the guns, and for a few days the country argued about little else.",
        "The air arm and the ministries split. One side argued that the railguns made national air defence spending "
        "wasteful: no small country could do better than the guns, and the money would save more lives in hospitals and "
        "stores. The other side pointed out that nobody could promise which fragments the guns would hit, or whether a small "
        "coast like this one would be covered at all. The flood wardens, asked for their view, said only that they had "
        "never seen a forecast that was never wrong.",
        "The government has to settle the budget before the debate becomes a political fight. Trusting the railguns frees "
        "money for relief. Planning as if they will miss keeps money in roofs, radar and drills. Either choice will be "
        "judged harshly by whoever turns out to have been wrong after the pass.",
    ), (Option('Trust the railguns and fund relief.', (Flag('trust_railguns'), PP(30))),
        Option('Plan as if the guns will miss.', (Flag('plan_for_misses'), Stability(-0.01)))),
        citation='Stonehenge completion is Chronicle, 1998 / 06.19; the national debate is not sourced', picture=2),
    EventDef('impact_night', 'The Night of the Fragments', (
        "On 8 July 1999 Ulysses passed the Roche limit and broke apart. Through the night the radar operators, flood wardens "
        "and harbour masters reported what they could see and hear: bright streaks over the sea, distant flashes, radio "
        "static. By morning the reports from across Usea described damaged towns, closed ports and roads crowded with "
        "families. The first radio messages from the harbours spoke of high water and broken windows, and then the lines "
        "went quiet for several hours.",
        "The country's own preparations were tested at once. Shelters opened, the hospitals called in volunteers and the "
        "harbour masters counted which ships could still sail. Messages arrived from coastal towns asking for food, water "
        "and tents, and from abroad asking whether the harbours could receive boats carrying people with nowhere else to go.",
        "The government must decide who leads the relief effort. Sending the army to the coast puts lorries, engineers and "
        "discipline where they are needed most, but places soldiers in charge of civilian streets. Placing relief in the "
        "districts' hands keeps it local and accountable, but leaves weaker districts struggling with tasks they have never "
        "faced.",
    ), (Option('Send the army to the coast.', (Flag('army_relief'), XP('army', 10))),
        Option('Put the districts in charge of relief.', (Flag('district_relief'), Stability(0.02)))),
        citation='the date is from Chronicle, 1999 / 07.08; the national response is not sourced', picture=0),
    EventDef('war_summer', 'War Comes to Usea', (
        "In the summer of 2003 Erusea invaded neutral San Salvacion and seized Stonehenge, turning the railguns built against "
        "asteroid fragments on aircraft instead. On 22 August Central Usea founded ISAF to resist. In the capital the news "
        "arrived as a series of shocks: closed air routes, shipping insurance rising by the day, and foreign diplomats "
        "asking where the country stood.",
        "The government has no intention of sending its small forces into a continental war. But neutrality is not simple "
        "when the warring sides need fuel, rubber, repairs and airspace, and when any harbour on the coast could shelter a "
        "damaged ship. The air arm, the coast watch and the harbour masters all ask for orders, and the treasury asks what "
        "the war will cost.",
        "The first orders concern the country's own forces. The government can mobilise only the coast guard and the naval "
        "reserve, keeping the economy running and the army at peace strength. Or it can call up the army reserve as well, "
        "showing every side that the country will defend itself, at the price of workers taken from farms and works.",
    ), (Option('Mobilise the coast guard and naval reserve.', (XP('navy', 15),)),
        Option('Call up the army reserve as well.', (XP('army', 20), WarSupport(0.02)))),
        citation='Chronicle, 2003 / SUMMER and 2003 / 08.22; the national response is not sourced', picture=0),
    EventDef('war_ledger', 'The War Accounts', (
        "The war accounts were published in the autumn of 2005: fuel rationed, reservists paid, ships insured, harbours "
        "guarded, aircraft scrambled. The figures showed a country that had spent heavily to stay outside a war fought "
        "across its own continent. Each district received its own page of the report, and each page started its own "
        "arguments.",
        "Supporters of the wartime posture pointed to the harbours that kept working and the soldiers who stayed at home. "
        "Critics pointed to the cost, the black markets in the harbour towns and the reputation the posture had earned "
        "abroad. Both sides agreed that the country had changed during the war years, and neither agreed how. "
        "The newspapers printed both views side by side and sold more copies than in any month of the war.",
        "With rationing ending and reservists going home, the government has to decide what to do with the wartime "
        "machinery. It can keep part of it, the guard posts, the convoy rules and the reserve stores, as a standing "
        "precaution. Or it can dismantle all of it, release the money for recovery and trust that the continent's wars are "
        "over.",
    ), (Option('Keep a standing precaution.', (WarSupport(0.03), XP('army', 10))),
        Option('Dismantle it and fund recovery.', (Stability(0.03), PP(40)))), picture=2),
    EventDef('recovery_vote', 'The Recovery Compact', (
        "The draft compact ran to forty pages and took six months to write. Its authors, drawn from the ministries, the "
        "districts and the political groups of the day, listed what the country needed within ten years: rebuilt harbours, "
        "a modern plateau, settled empty districts, a technical college, and a government the next generation would accept "
        "as legitimate.",
        "The arguments were familiar. District C wanted the rubber trade restored first. District F wanted its mills "
        "modernised. District E wanted yard contracts, and District B wanted roads and schools for its farms. The capital "
        "wanted all of it, paid for by someone else. Every faction found something to dislike, which the authors took as a "
        "sign of balance. The draft was printed in every district newspaper, and the letters pages filled for weeks.",
        "The final question is how the compact becomes binding. It can be put to a national vote, which gives it legitimacy "
        "but risks a rejection that would set recovery back years. Or the six district governors can sign it as an "
        "agreement among the districts, which is faster and more certain but leaves ordinary citizens as spectators.",
    ), (Option('Put the compact to a national vote.', (Flag('compact_vote'), Stability(0.03))),
        Option('Let the district governors sign it.', (Flag('compact_signed'), PP(40)))), picture=1),
)

# --- branches ----------------------------------------------------------------------------------
BRANCHES = (
    Branch('charter', 'The Suspended Charter', 1991, 'FOCUS_FILTER_POLITICAL', (
        Focus('admin_audit', 'Audit the National Administration',
              "Chopinburg enters 1991 under a National Administration that governs with the election calendar suspended and "
              "a public split between loyal administrators and a loud nationalist movement. Before anyone argues about the "
              "next government, the ministries must show what they spend and who they employ. The audit costs months of "
              "goodwill inside the civil service.",
              ('document', 'assembly'), reward=(Event('administration_audit'), Idea('unmandated_ministries'))),
        Focus('ministry_rolls', 'Publish the Ministry Payrolls',
              "The audit found offices whose staff lists had not been checked since before the charter was suspended. "
              "Printing every ministry payroll in the capital papers exposes absent clerks and double salaries. It will "
              "anger senior officials who built careers on quiet arrangements, but it gives later budgets a figure the "
              "public can test.",
              ('document', 'economy'), after=('admin_audit',), reward=(Flag('payrolls_published'), Stability(0.02))),
        Focus('district_delegates', 'Hear the District Delegates',
              "Five districts outside the capital send delegates who have rarely been heard in the ministries. District C "
              "wants harbour money, District E wants yard contracts, District F wants a fair price for its ore, and the two "
              "empty districts want roads at all. Listening commits the administration to answers it cannot yet afford.",
              ('assembly', 'civil'), after=('admin_audit',), reward=(Flag('delegates_heard'), PP(30))),
        Focus('charter_ballot', 'Restore the Charter Ballot',
              "Lift the suspension and set a date for the first national ballot in years. The administration hands its "
              "future to voters who have had little practice, and the nationalist halls will campaign hard. The ministries "
              "lose their ability to act by decree, but the government gains a mandate the districts can recognise.",
              ('ballot', 'document'), after=('ministry_rolls', 'district_delegates'),
              exclusive=('keep_administration', 'answer_rally'), cost=10,
              reward=(SwapIdea('unmandated_ministries', 'charter_rolls'), Flag('charter_path'))),
        Focus('keep_administration', 'Keep the Administration Seated',
              "Leave the election calendar suspended and make the ministries earn their authority through results instead. "
              "A board of senior administrators would set targets, publish them and answer for misses. It is efficient and "
              "predictable, and it keeps the nationalist halls away from power, but it asks the districts to accept rule "
              "they never voted for.",
              ('command', 'document'), after=('ministry_rolls', 'district_delegates'),
              exclusive=('charter_ballot', 'answer_rally'), cost=10,
              reward=(SwapIdea('unmandated_ministries', 'performance_tables'), Flag('directorate_path'))),
        Focus('answer_rally', 'Answer the National Rally',
              "The nationalist movement fills halls in the capital and the harbour towns while the administration fills "
              "only its offices. Bringing the movement inside government would give the state a mass following and a ready "
              "supply of volunteers. The price is a louder, harder politics, and districts that never joined the rallies "
              "will feel shut out.",
              ('assembly', 'security'), after=('ministry_rolls', 'district_delegates'),
              exclusive=('charter_ballot', 'keep_administration'), cost=10,
              reward=(SwapIdea('unmandated_ministries', 'rally_halls'), Flag('rally_path'))),
        Focus('district_rolls', 'Voter Rolls in Every District',
              "No ballot is credible until every district has a register. Clerks travel to the jungle harbours of District "
              "C, the yards of District E and the empty plains of District B, often by boat or on foot after the rains. The "
              "registration drive is slow and expensive, but it is the part of the charter people will actually see.",
              ('ballot', 'civil'), after=('charter_ballot',),
              reward=(Stability(0.03), Tooltip('Registers are posted in the capital and in all five outer districts.'))),
        Focus('charter_council', 'Convene the Charter Council',
              "With the registers posted and the ballot counted, a Charter Council of elected members takes over the "
              "ministries from the National Administration. It is a collective body, slow to agree and quick to argue, and "
              "it will hold regular elections from now on. Its first budget will be the first one voters can punish.",
              ('ballot', 'assembly'), after=('district_rolls',), cost=10,
              reward=(Regime('charter_council'), Stability(0.04))),
        Focus('ministry_scorecards', 'Scorecards for Every Ministry',
              "Each ministry receives three targets a year and a public scorecard showing whether it met them. Road miles in "
              "District B, harbour tonnage in District C and yard hours in District E are counted and printed. Officials "
              "who miss twice are replaced. The system rewards measurable work and quietly neglects anything hard to count.",
              ('document', 'scales'), after=('keep_administration',), reward=(PP(50), Research('industry'))),
        Focus('admin_directorate', 'Seat the Administrative Directorate',
              "The board of senior administrators becomes the government in name as well as fact. An Administrative "
              "Directorate replaces the old National Administration, keeps elections suspended and governs by published "
              "plan. It answers to its own targets rather than to voters, which makes it steady in good years and brittle "
              "when the targets fail.",
              ('command', 'assembly'), after=('ministry_scorecards',), cost=10,
              reward=(Regime('administrative_directorate'), PP(40))),
        Focus('rally_halls_open', 'Rally Halls in the Capital',
              "The movement is given the use of public halls in the capital and the harbour towns, along with a place on "
              "district committees. Attendance becomes a path to jobs and promotion. Volunteers sign up for the coast watch "
              "and the reserve, while shopkeepers and clerks who stay away learn to keep their opinions private.",
              ('assembly', 'medal'), after=('answer_rally',), reward=(WarSupport(0.04), Stability(-0.02),
                      Tooltip('Movement volunteers fill the coast watch and army reserve rolls.'))),
        Focus('renewal_committee', 'Seat the National Renewal Committee',
              "A National Renewal Committee drawn from the movement's leadership takes the ministries and dissolves the old "
              "administration. It promises discipline, work on the coast and pride in the districts, and it has no "
              "intention of holding elections. Trading partners will treat the country more warily, and dissent at home "
              "will have fewer outlets.",
              ('security', 'assembly'), after=('rally_halls_open',), cost=10,
              reward=(Regime('renewal_committee'), WarSupport(0.03))),
        Focus('district_budget', 'A Budget Every District Can Read',
              "Whatever government now sits in the capital, the districts expect to see their share. A single budget book, "
              "printed by district rather than by ministry, shows how much goes to the rubber coast, the plateau, the yards "
              "and the empty plains. Arguments become sharper but shorter, and every later programme has a baseline.",
              ('economy', 'document'), after_any=('charter_council', 'admin_directorate', 'renewal_committee'),
              reward=(Idea('open_budget'), PP(25))),
    )),

    Branch('rubber', 'The Rubber Coast', 1991, 'FOCUS_FILTER_INDUSTRY', (
        Focus('grove_census', 'Count the District C Groves',
              "District C holds most of the country's rubber, spread across jungle groves behind three small harbours. "
              "Nobody in the capital knows how many trees are tapped, who owns them or how much latex leaves without paying "
              "duty. A census of every grove, made by surveyors on foot during the dry weeks, is the first step to a policy.",
              ('document', 'industry'), reward=(Event('rubber_census'),)),
        Focus('rubber_board', 'A State Rubber Board',
              "The state buys all latex at a fixed price, grades it in the harbour sheds and sells it abroad under one mark. "
              "Revenue flows straight to the treasury and the factories get a reliable supply. Growers lose the right to "
              "bargain, and smuggling will rise whenever the fixed price falls behind the market.",
              ('economy', 'industry'), after=('grove_census',), exclusive=('grower_coops', 'lease_groves'), cost=10,
              reward=(Idea('state_rubber_board'),)),
        Focus('grower_coops', 'Grower Cooperatives on the Coast',
              "Families who tap the groves form cooperatives that grade, store and sell their own latex, with the state "
              "lending sheds and boats. Income stays in District C and the coast becomes calmer. The treasury collects only "
              "an export duty, so the capital has less money for its own plans and less say over prices.",
              ('civil', 'economy'), after=('grove_census',), exclusive=('rubber_board', 'lease_groves'), cost=10,
              reward=(Idea('grower_cooperatives'),)),
        Focus('lease_groves', 'Lease the Groves to Outside Buyers',
              "Large buyers from abroad lease whole blocks of groves for twenty years and bring their own tapping crews, "
              "sheds and ships. Lease money arrives quickly and pays for building elsewhere. In return the country gives up "
              "control of its most valuable crop, and local growers become hired hands on land they once worked themselves.",
              ('document', 'economy'), after=('grove_census',), exclusive=('rubber_board', 'grower_coops'), cost=10,
              reward=(Idea('grove_leases'),)),
        Focus('latex_works', 'Latex Works at the Harbours',
              "Raw latex sells cheaply; sheet, crepe and moulded goods sell for more. Building a processing works beside the "
              "largest of the three District C harbours keeps the value at home and gives the coast steady factory jobs. It "
              "needs power, fresh water and a road the rains cannot wash out, which the district lacks.",
              ('industry', 'navy'), after_any=('rubber_board', 'grower_coops', 'lease_groves'),
              reward=(Build('industrial_complex', 1, 459),)),
        Focus('jungle_tracks', 'Tracks Through the Groves',
              "Latex is carried out of the groves on foot or by cart along tracks that vanish each rainy season. Graded and "
              "drained tracks with small bridges would let lorries reach the works all year round. The labour comes from the "
              "growers themselves, paid in cash, and the work will take most of a year.",
              ('logistics', 'bridge'), after=('latex_works',), reward=(Build('infrastructure', 1, 459), Stability(0.01))),
        Focus('harbour_customs', 'One Customs House, Three Harbours',
              "Each of the three District C harbours keeps its own customs clerks, ledgers and favourites. Merging them into a "
              "single customs house with one ledger closes the gaps that let latex leave unrecorded. Harbour towns will lose "
              "jobs and local influence, but the treasury and the convoy planners will finally see the whole trade.",
              ('document', 'navy'), after=('latex_works',), reward=(Flag('single_customs'), PP(30))),
        Focus('synthetic_trials', 'Synthetic Rubber Trials',
              "Natural rubber is plentiful today, but a blight, a storm season or a closed sea lane could cut supply "
              "overnight. A small laboratory at the latex works experiments with synthetic compounds made from plateau oil. "
              "It will not replace the groves, yet it keeps chemists employed and gives the army a fallback for tyres and "
              "seals.",
              ('science', 'industry'), after=('jungle_tracks',), reward=(Research('synth_resources', 0.75, 1),)),
        Focus('tyre_plant', 'A Tyre Plant for the Army',
              "The army's lorries and the air arm's aircraft run on imported tyres bought at high prices. A plant beside the "
              "latex works, built to military specifications, would supply both and sell the surplus. It turns District C "
              "into a strategic district, which raises its importance in any future emergency and makes it a target.",
              ('industry', 'security'), after=('jungle_tracks', 'harbour_customs'),
              reward=(Build('arms_factory', 1, 459),)),
        Focus('growers_price_board', 'Growers Set the Grove Price',
              "Because the census was published grove by grove, growers can see what their neighbours produce and earn. A "
              "price board elected by the growers meets each month at the customs house and posts a reference price. "
              "Middlemen lose their margin, disputes fall, and the coast trusts the capital a little more.",
              ('scales', 'civil'), after=('harbour_customs',), requires=(HasFlag('census_public'),),
              reward=(Stability(0.04), Tooltip('The growers price board meets monthly at the customs house.'))),
        Focus('quiet_export_quota', 'A Quiet Export Quota',
              "With the census kept inside the ministry, the government can set export quotas that buyers cannot easily "
              "check. Holding back part of each season's latex lifts the price abroad and fills a reserve fund. It works "
              "only while the figures stay secret, and growers suspect they are paid for less than they deliver.",
              ('economy', 'document'), after=('harbour_customs',), requires=(HasFlag('census_sealed'),),
              reward=(PP(60), Stability(-0.02))),
        Focus('rubber_for_escorts', 'Rubber Credit for the Escorts',
              "Foreign shipyards will supply designs and fittings for escort hulls if paid partly in rubber delivered over "
              "several seasons. Pledging future latex as credit gives the navy a way to renew its ships without draining the "
              "treasury. It also ties a share of every harvest to the yards for years, whatever happens to prices.",
              ('navy', 'economy'), after=('tyre_plant',), reward=(Flag('rubber_credit'), Research('naval_equipment'))),
    )),

    Branch('flats', 'Rain on the Flats', 1992, 'FOCUS_FILTER_STABILITY', (
        Focus('rain_gauges', 'Rain Gauges Across the Flats',
              "The capital, District B, District E and the desert hinterland all share the low country of the flats, where "
              "heavy rain turns roads to mud for weeks at a time. A network of rain gauges and flood wardens in every "
              "district records where water gathers and when it peaks. It is cheap, dull and overdue work.",
              ('tools', 'civil'), reward=(Idea('flood_wardens'),)),
        Focus('storm_drains', 'Storm Drains Under the Capital',
              "The capital's streets flood every heavy season, closing shops, workshops and the road to the air base. Brick "
              "storm drains under the main avenues, sized from the wardens' records, would carry the water to outfalls "
              "beyond the city. Digging will close streets for a year, and contractors want paying long before the benefit "
              "is felt.",
              ('tools', 'rebuild'), after=('rain_gauges',), reward=(Build('infrastructure', 1, 0), Stability(0.02))),
        Focus('raised_roads', 'Raised Roads Over the Mud',
              "District E's yards depend on a single road that disappears under water whenever the rains are heavy. Raising "
              "the road on an embankment with culverts every few hundred metres keeps steel, timber and workers moving to "
              "the yards. The embankment uses spoil dug from the capital drains, so the two projects share their cost.",
              ('logistics', 'tools'), after=('rain_gauges',), reward=(Build('infrastructure', 1, 520),)),
        Focus('district_b_dykes', 'Dykes for the District B Fields',
              "District B is good, flat farmland with no buildings and no roads worth the name, mostly because it floods. "
              "Low dykes and drainage ditches around the best fields would make it worth settling. Farmers will not move "
              "there until a dry season proves the work, so the state must carry the cost alone at first.",
              ('rebuild', 'civil'), after=('raised_roads',), reward=(Build('infrastructure', 1, 32), Stability(0.01))),
        Focus('mud_line_depots', 'Depots Above the Mud Line',
              "Army supply depots on the flats sit on low ground and must be emptied when the water rises. Moving fuel, food "
              "and ammunition to raised platforms near the road junctions keeps units supplied through the mud season. The "
              "army must give up some convenient town depots that officers have used for years.",
              ('logistics', 'security'), after=('raised_roads',),
              reward=(Flag('depots_above_mud'), Research('logistics_tech'))),
        Focus('flats_dry', 'The Flats Kept Dry',
              "With drains, dykes and raised roads working together, the wardens can predict and limit most floods instead "
              "of reacting to them. The flood service becomes a permanent drainage authority with its own budget and "
              "engineers. It will compete with every other ministry for money, but the flats will be usable in every season.",
              ('bridge', 'tools'), after=('storm_drains', 'district_b_dykes'),
              reward=(SwapIdea('flood_wardens', 'drained_flats'), Flag('drainage_complete'))),
        Focus('weather_service', 'A National Weather Service',
              "The wardens' gauges, the air base observers and the harbour masters all keep separate weather records. A "
              "national weather service combines them, adds a radar mast at the capital and issues daily forecasts for the "
              "farms, the yards and the air arm. Forecasting will also matter if the sky ever brings more than rain.",
              ('radar', 'communications'), after=('flats_dry',),
              reward=(Build('radar_station', 1, 0), Research('electronics'))),
    )),

    Branch('plateau', 'Plateau Mines and Mills', 1992, 'FOCUS_FILTER_INDUSTRY', (
        Focus('plateau_assay', 'Assay the Plateau Seams',
              "District F sits on a dry plateau with oil, aluminium ore and iron that support two civilian works and two arms "
              "works. Nobody has mapped how long the seams will last or how deep they run. An assay by the mines ministry, "
              "with drilling teams and a field laboratory, decides how much to invest above ground.",
              ('science', 'tools'), reward=(Event('plateau_survey'), Research('excavation_tech'))),
        Focus('smelt_on_plateau', 'Smelt on the Plateau',
              "Build smelters and refineries next to the mines so that District F ships finished metal and fuel rather than "
              "ore and crude. The plateau gains skilled jobs and the railway carries lighter loads. Power and water are "
              "scarce up there, so the works will run hot and expensive until their supply lines mature.",
              ('industry', 'tools'), after=('plateau_assay',), exclusive=('ore_to_capital',), cost=10,
              reward=(Idea('plateau_smelters'), Flag('smelters_upland'))),
        Focus('ore_to_capital', 'Ore Trains to the Capital',
              "Send raw ore and crude down to the capital, where power, labour and the older works already exist. "
              "Processing stays concentrated in one city that is easier to supply and defend. District F remains a mining "
              "district with fewer skilled jobs, and its towns will feel that the capital takes the wealth and leaves the "
              "dust.",
              ('rail', 'industry'), after=('plateau_assay',), exclusive=('smelt_on_plateau',), cost=10,
              reward=(Idea('ore_trains'), Flag('ore_line'))),
        Focus('plateau_power', 'A Power Station on the Plateau',
              "Every plan for District F runs into the same limit: there is not enough electricity. A thermal station "
              "burning plateau oil would light the mining towns, run pumps for the seams and feed new works. It consumes "
              "fuel the country might want to sell, and its chimneys will be the tallest structure on the plateau.",
              ('industry', 'economy'), after_any=('smelt_on_plateau', 'ore_to_capital'),
              reward=(Build('industrial_complex', 1, 539),)),
        Focus('plateau_rail', 'Grade the Plateau Railway',
              "The line that climbs from the flats to the plateau is steep, single track and slow, and it limits everything "
              "District F can ship. Easing its grades and adding passing loops would double its capacity. Track gangs will "
              "work through the hot season, and traffic will be cut to a few trains a day while they do.",
              ('rail', 'tools'), after_any=('smelt_on_plateau', 'ore_to_capital'),
              reward=(Build('infrastructure', 1, 539), Research('train_tech'))),
        Focus('aluminium_line', 'An Aluminium Rolling Line',
              "Aluminium ore from District F currently leaves the country as ore and returns as expensive sheet. A rolling "
              "line beside the new power station would supply sheet and extrusions to the air arm's workshops and the yards. "
              "It needs specialist engineers who must be trained or hired abroad, and the first output will be poor.",
              ('industry', 'air'), after=('plateau_power',), reward=(Build('arms_factory', 1, 539),)),
        Focus('plateau_shell_works', 'Shell Works on the Plateau',
              "Steel, power and a railway put District F in a position to make artillery shells and mortar bombs far from "
              "the shore. Dispersing ammunition work inland suits a country that already spreads its forces along the "
              "coast. Neighbours will notice, and each mining town will have to accept a magazine at its edge.",
              ('industry', 'security'), after=('aluminium_line', 'plateau_rail'),
              reward=(Build('arms_factory', 1, 539), Research('artillery'))),
        Focus('plateau_hostels', 'Hostels for Plateau Workers',
              "Miners and smelter crews on the plateau live in tents and borrowed rooms, and most leave after one hot "
              "season. Proper hostels with water, a canteen and a clinic would keep trained men and women long enough to "
              "repay their training. The housing budget comes out of the works' first profits, delaying expansion.",
              ('civil', 'shelter'), after=('plateau_rail',),
              reward=(Stability(0.03), Tooltip('Worker hostels open in each District F mining town.'))),
    )),

    Branch('districts', 'The Empty Districts', 1993, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
        Focus('empty_survey', 'Survey the Two Empty Districts',
              "District B and the desert hinterland together hold a large share of the country's land and almost none of "
              "its buildings, roads or works. Before the state spends money there, a survey team records water, soil, "
              "tracks and the few settlements that exist. The survey takes a full year and decides which district gets the "
              "first road.",
              ('document', 'logistics'), reward=(Event('empty_districts'),)),
        Focus('district_b_road', 'A Paved Road to District B',
              "District B lies close to the capital but is reached only by farm tracks that close in the rains. A paved road "
              "from the edge of the capital across the plains would let produce reach the markets and settlers reach the "
              "land. The road is short and cheap by national standards, which makes it a good first test.",
              ('logistics', 'civil'), after=('empty_survey',), reward=(Build('infrastructure', 1, 32), Stability(0.02))),
        Focus('hinterland_wells', 'Wells Across the Hinterland',
              "The desert hinterland cannot be crossed, garrisoned or settled without water. Drilling a line of wells along "
              "the route of the survey track creates stopping points every day's drive. The wells cost little compared to a "
              "road, but each one needs a keeper, and keepers have to be persuaded to live in the desert.",
              ('tools', 'logistics'), after=('empty_survey',), reward=(Build('infrastructure', 1, 512),)),
        Focus('homestead_grants', 'Homestead Grants on the Plains',
              "Offer families from the crowded capital a plot of District B land, seed and a small loan, with title after "
              "five years of farming. Homesteads create a loyal rural population close to the capital. They grow slowly, "
              "they need schools and clinics, and the state cannot direct what the families choose to grow.",
              ('civil', 'rebuild'), after=('district_b_road',), exclusive=('state_farms_b',),
              reward=(Idea('plains_homesteads'), Flag('homesteads_open'))),
        Focus('state_farms_b', 'State Farms for District B',
              "Organise District B as a few large state farms run by the agriculture ministry, with hired crews and "
              "machinery bought in bulk. Output rises fast and feeds the capital and the army. Workers have no stake in the "
              "land, the farms depend on ministry budgets, and the plains stay thinly settled outside harvest season.",
              ('economy', 'logistics'), after=('district_b_road',), exclusive=('homestead_grants',),
              reward=(Idea('district_b_state_farms'), Build('infrastructure', 1, 32))),
        Focus('district_b_market', 'A Market Town for District B',
              "Farms need a place to sell grain, repair machines and buy supplies without travelling to the capital. A "
              "market town at the road's midpoint, with a grain store, a workshop and a district office, gives District B "
              "its first real centre. Its success depends on whether the farms around it actually produce a surplus.",
              ('economy', 'civil'), after_any=('homestead_grants', 'state_farms_b'),
              reward=(Build('industrial_complex', 1, 32),)),
        Focus('hinterland_relays', 'Relay Masts, Not Settlers',
              "Accept that the hinterland will stay empty and use it for what empty land does best: carrying signals and "
              "watching the sky. A chain of relay masts and a radar post links the capital to the far coast and the plateau. "
              "It costs little to staff, but it leaves the district without people to defend or develop it.",
              ('communications', 'radar'), after=('hinterland_wells',), exclusive=('hinterland_settlers',),
              reward=(Build('radar_station', 1, 512), Flag('relay_masts'))),
        Focus('hinterland_settlers', 'Settlers for the Hinterland Wells',
              "Turn the wells into small settlements with irrigated gardens, a school and a police post, and pay families to "
              "stay for ten years. A settled hinterland is easier to govern and harder for anyone to cross unseen. The "
              "subsidy runs for a decade, and many families will still leave when the first drought arrives.",
              ('civil', 'shelter'), after=('hinterland_wells',), exclusive=('hinterland_relays',),
              reward=(Build('infrastructure', 1, 512), Stability(0.02))),
        Focus('grants_formula', 'A Grants Formula for the Districts',
              "The district delegates heard in 1991 asked for a fair rule rather than favours. A formula based on "
              "population, distance from the capital and missing services decides each district's share of development "
              "grants. The capital's own projects lose some priority, and every district will lobby to change the formula "
              "in its favour.",
              ('scales', 'economy'), after=('district_b_market',), requires=(HasFlag('delegates_heard'),),
              reward=(TimedIdea('district_grants', 730), PP(20))),
    )),

    Branch('air', 'The Air Arm', 1993, 'FOCUS_FILTER_AIR_XP', (
        Focus('air_arm_review', 'Review the Forty-Eight Fighters',
              "The air arm has forty-eight fighters, one air base at the capital and too few instructors to train "
              "replacements. A review counts which airframes can fly, which pilots are current and what spares exist. The "
              "findings will embarrass the service, but they set the size of every later air budget.",
              ('air', 'document'), reward=(Idea('air_instructors'), XP('air', 10))),
        Focus('second_airfield', 'A Second Airfield on the Plateau',
              "With only one air base, a single raid or flood could ground the entire air arm. A second field in District F, "
              "dry and high above the flats, gives the fighters a place to disperse and train in clear weather. It is far "
              "from the harbours the fighters are meant to protect.",
              ('runway', 'air'), after=('air_arm_review',), reward=(Build('air_base', 1, 539),)),
        Focus('coastal_airstrip', 'An Airstrip for District C',
              "District C's harbours and rubber works have no air cover closer than the capital. A short airstrip cut from "
              "the edge of the groves would let a flight of fighters stand alert over the coast. Jungle humidity and heavy "
              "rain will wear out aircraft and crews quickly, and the strip will need constant repair.",
              ('runway', 'navy'), after=('air_arm_review',), reward=(Build('air_base', 1, 459),)),
        Focus('interceptor_screen', 'An Interceptor Screen',
              "Train the fighters for one job: meeting hostile aircraft over the country's own territory, guided from the "
              "ground. The doctrine fits a small country that does not intend to fight abroad. It leaves the coast and the "
              "convoys without an air arm able to strike ships, and it depends on radar the country does not yet have.",
              ('air', 'radar'), after_any=('second_airfield', 'coastal_airstrip'), exclusive=('coastal_strike_wing',),
              cost=10, reward=(Idea('fighter_screen'),)),
        Focus('coastal_strike_wing', 'A Coastal Strike Wing',
              "Train a share of the fighters to carry bombs and rockets against ships and landing craft off the coast. The "
              "doctrine suits a country whose real exposure is its long shoreline and its convoy routes. Pilots trained for "
              "strike work are less practised in air combat, and the wing will need longer runways.",
              ('air', 'navy'), after_any=('second_airfield', 'coastal_airstrip'), exclusive=('interceptor_screen',),
              cost=10, reward=(Idea('maritime_strike'),)),
        Focus('capital_runway', 'Lengthen the Capital Runway',
              "The capital's runway was laid for older, lighter aircraft and is short for loaded fighters in hot, humid "
              "air. Extending it and adding hardstands and drainage keeps it usable through the rains. The work closes the "
              "base to heavy traffic for months, so the other fields must carry the air arm while it lasts.",
              ('runway', 'tools'), after_any=('interceptor_screen', 'coastal_strike_wing'),
              reward=(Build('air_base', 1, 0), XP('air', 10))),
        Focus('ground_controllers', 'Ground Controllers for the Fighters',
              "An interceptor screen is only as good as the people on the ground telling pilots where to go. A control room "
              "at the capital, a radar mast and a corps of trained controllers turn the screen into a working system. "
              "Controllers take two years to train and are easily lured away by civil aviation.",
              ('radar', 'command'), after=('capital_runway', 'interceptor_screen'),
              reward=(Build('radar_station', 1, 0), XP('air', 15))),
        Focus('anti_ship_range', 'An Anti-Ship Practice Range',
              "Strike pilots need targets that move on water. A practice range off the District E coast, with towed targets "
              "supplied by the yards, gives them that. Boat owners will lose a stretch of water during exercises and "
              "complain loudly, and the range will draw attention from anyone watching the coast.",
              ('missile', 'navy'), after=('capital_runway', 'coastal_strike_wing'),
              reward=(XP('air', 20), Research('air_doctrine'))),
        Focus('air_mechanics', 'Mechanics Before More Fighters',
              "More aircraft are useless without people to keep them flying. A mechanics school at the capital base, taking "
              "apprentices from the yards and the plateau works, raises the number of serviceable fighters on any given day. "
              "It delays new purchases by a budget year, which the pilots will resent.",
              ('tools', 'air'), after=('capital_runway',),
              reward=(SwapIdea('air_instructors', 'air_mechanics_school'), Research('electronics', 0.5, 1))),
    )),

    Branch('coast', 'The Coastal Dispersal', 1995, 'FOCUS_FILTER_NAVY_XP', (
        Focus('yard_inventory', 'Inventory the District E Yards',
              "District E's three dockyards build and repair the navy's three destroyers, its single submarine and the "
              "merchant hulls of the coast trade. Their slipways are old and their order book is thin. An inventory of "
              "yards, hulls and skilled workers shows what the navy can maintain and what it should stop pretending to own.",
              ('navy', 'document'), reward=(Event('yard_inventory'), XP('navy', 10))),
        Focus('harbour_pilots', 'A Harbour Pilots School',
              "The country has four naval harbours spread between District C and District E, each with awkward channels "
              "known only to a few old pilots. A pilots school in District E trains young officers and merchant mates in "
              "every channel. Ships move faster and safer, and the navy stops depending on a handful of men near retirement.",
              ('navy', 'training'), after=('yard_inventory',), reward=(Idea('pilot_service'),)),
        Focus('convoy_escorts', 'Escort the Merchant Convoys',
              "Organise the destroyers and armed merchant ships to escort coastal convoys between the harbours and out to "
              "the shipping lanes. The country's trade, rubber above all, travels by sea, and escorts protect it directly. "
              "Escort duty is slow and wears out hulls, and it leaves no ships free to watch the approaches.",
              ('navy', 'logistics'), after=('harbour_pilots',), exclusive=('submarine_pickets',), cost=10,
              reward=(Idea('escort_convoys'),)),
        Focus('submarine_pickets', 'Submarine Pickets Offshore',
              "Station the submarine and small patrol craft far out on the approaches to watch for hostile ships and report "
              "them early. A small navy cannot fight every intruder, but it can refuse to be surprised. Merchant ships sail "
              "without escorts, and the picket boats spend long, lonely weeks at sea.",
              ('submarine', 'radar'), after=('harbour_pilots',), exclusive=('convoy_escorts',), cost=10,
              reward=(Idea('offshore_pickets'),)),
        Focus('island_watch', 'Watch the Coast After Skully',
              "At the end of 1995 rebels in the Skully Islands showed how a small armed group can use remote islands and "
              "coastline, until Unified Command defeated them. This country's shore is long and thinly watched. A coast "
              "watch of volunteers, harbour police and naval reservists closes the gaps, at the cost of a standing payroll.",
              ('security', 'navy'), after=('harbour_pilots',), requires=(After('1995.12.31'),),
              reward=(Flag('coast_watch_founded'), XP('navy', 15))),
        Focus('convoy_office', 'A Convoy Office in District E',
              "Merchant masters, harbour clerks and naval officers each keep their own sailing lists. A convoy office in "
              "District E collects them, schedules departures and decides which ships sail together. Masters lose some "
              "freedom to sail when they like, and the office becomes the country's best record of who carries what.",
              ('logistics', 'document'), after_any=('convoy_escorts', 'submarine_pickets'),
              reward=(Flag('convoy_office_open'), PP(20))),
        Focus('escort_hulls_credit', 'Escort Designs on Rubber Credit',
              "The rubber credit agreed with foreign yards can now be called in. Modern escort designs and fittings, paid for "
              "in latex over several harvests, reach the District E drawing offices. They give the escort force real speed "
              "and sensors, but every poor harvest from now on will be felt in the navy budget.",
              ('navy', 'science'), after=('convoy_escorts',), requires=(HasFlag('rubber_credit'),),
              reward=(Research('naval_equipment', 0.75, 2), XP('navy', 10))),
        Focus('picket_relay', 'Pickets Report by Radio Relay',
              "A picket that cannot report is just a lonely boat. Radio relays on headlands and a shore station in District "
              "C pass sightings to the capital within minutes. The system makes the pickets useful, but it depends on "
              "equipment bought abroad and on operators who will be scarce in any emergency.",
              ('communications', 'submarine'), after=('submarine_pickets',),
              reward=(Build('radar_station', 1, 459), XP('navy', 10))),
        Focus('coastal_mines', 'Mine Stores for the Approaches',
              "Defensive minefields could close the harbour approaches in a crisis, but only if the mines are already "
              "stored, maintained and charted. Magazines in District E and District C hold a stock of moored mines and the "
              "charts to lay them. Boat owners and merchants will want assurance that no field is laid without warning.",
              ('security', 'document'), after=('island_watch',),
              reward=(Research('naval_equipment'), WarSupport(0.02))),
    )),

    Branch('ulysses', 'Preparing for Ulysses', 1996, 'FOCUS_FILTER_STABILITY', (
        Focus('ulysses_warning', 'Hear the Ulysses Warning',
              "In April 1996 Central Usea announced that the asteroid Ulysses would strike the Earth, and fragments could "
              "fall anywhere. The country must decide what to tell its people, what to build and what to stockpile in the "
              "years before the pass. The first decision is how openly the government speaks about the danger.",
              ('meteor', 'communications'), requires=(After('1996.4.20'),), reward=(Event('ulysses_warning'),)),
        Focus('national_shelters', 'A National Shelter Plan',
              "Fund shelters, reserves and warning sirens from a special levy, built and run entirely by the country's own "
              "ministries. The government keeps full control of where shelters go and who uses them. The levy raises prices "
              "on everyday goods, and a small state must build the whole programme with its own engineers.",
              ('shelter', 'economy'), after=('ulysses_warning',), exclusive=('treaty_shelter_compact',), cost=10,
              reward=(Idea('shelter_levy'),)),
        Focus('treaty_shelter_compact', 'The Treaty Council Shelter Compact',
              "Join other Treaty Council members in a common shelter compact that shares designs, engineers and warning "
              "data. Shelters go up faster and cost less. In exchange the compact sets standards, inspects sites and expects "
              "help for other members when fragments fall, which ties relief planning to decisions taken elsewhere.",
              ('shelter', 'diplomacy'), after=('ulysses_warning',), exclusive=('national_shelters',), cost=10,
              reward=(Idea('shelter_compact'),)),
        Focus('observatory_bulletins', 'Weekly Observatory Bulletins',
              "Since the government chose openness, astronomers and the flood wardens publish a weekly bulletin on the "
              "asteroid, its predicted pass and what it means for the coast and the flats. Panic drops once people see "
              "regular facts. Every revised forecast also makes headlines, and the bulletins must never be caught softening "
              "bad news.",
              ('telescope', 'communications'), after=('ulysses_warning',), requires=(HasFlag('open_warning'),),
              reward=(Research('electronics'), Stability(0.02))),
        Focus('rumour_desks', 'Rumour Control Desks',
              "Since the government chose to release only confirmed figures, rumours fill the gap. Rumour desks in every "
              "district answer questions by telephone and notice board, correcting false dates and miracle cures. They calm "
              "the markets, but people learn to ask the desks what the government is not saying.",
              ('communications', 'security'), after=('ulysses_warning',), requires=(HasFlag('managed_warning'),),
              reward=(PP(40), Stability(0.02))),
        Focus('capital_shelters', 'Shelters Under the Capital',
              "The capital holds most of the country's people and industry on flat, waterlogged ground where deep digging "
              "floods. Shelters must be half buried, reinforced and pumped. The first ones go under schools, the hospital "
              "and the main works, and the queue for places will show the public exactly who the state protects first.",
              ('shelter', 'civil'), after_any=('national_shelters', 'treaty_shelter_compact'),
              reward=(Flag('shelters_dug'), Stability(0.03))),
        Focus('grain_fuel_reserve', 'Grain and Fuel Reserves',
              "A strike anywhere on the coast could cut harbours and roads for weeks. A national reserve of grain, medicine "
              "and fuel, stored on the dry plateau and in the capital, buys that time. Filling it takes money away from "
              "development and ties up plateau oil that would otherwise be exported.",
              ('logistics', 'shelter'), after=('capital_shelters',), reward=(Idea('strategic_reserve'),)),
        Focus('coast_evac', 'Evacuation Tables for the Coast',
              "Low harbour towns in District C and District E would be the hardest places to protect from fragments or the "
              "waves they might raise. Evacuation tables assign every street a route, a shelter and a time. Drawing them up "
              "means admitting which towns cannot be defended, and property values there will fall.",
              ('refugees', 'document'), after=('capital_shelters',),
              reward=(Flag('evacuation_tables'), Build('infrastructure', 1, 520))),
        Focus('rubber_sheeting', 'Rubber Sheeting for Shelters',
              "Half buried shelters on the flats leak in every heavy rain. The latex works in District C can roll "
              "waterproof sheeting to line them, along with seals for doors and vents. It is a rare case where the rubber "
              "coast and the capital need each other, and it keeps the works busy when exports slow.",
              ('industry', 'shelter'), after=('capital_shelters',),
              reward=(Build('industrial_complex', 1, 459), Stability(0.01))),
        Focus('hospital_reserve', 'A Hospital Bed Reserve',
              "The capital's hospital and the district clinics run full in an ordinary year. A reserve of beds, stretchers "
              "and trained volunteers, stored in schools and warehouses, doubles emergency capacity on paper. It costs "
              "relatively little, but volunteers must be retrained each year or the reserve exists only in a ledger.",
              ('medical', 'civil'), after=('grain_fuel_reserve',),
              reward=(Stability(0.02), Tooltip('Stretchers, beds and volunteer rosters are stored in every district.'))),
        Focus('last_drills', 'The Last Drills Before the Pass',
              "In the final months before Ulysses passes, every district runs full drills: sirens, evacuation by table, "
              "shelter entry and hospital reception. The drills expose gaps while there is still time to fix them. They "
              "also frighten people, and attendance falls each time the predicted danger feels more distant.",
              ('training', 'shelter'), after=('coast_evac', 'hospital_reserve'), requires=(After('1999.1.1'),),
              reward=(Flag('drills_held'), Stability(0.02))),
    )),

    Branch('coup', 'After the May Coup', 1997, 'FOCUS_FILTER_POLITICAL', (
        Focus('coup_news', 'The Coup Across Usea',
              "On 30 May 1997 a coup broke out across Usea, and Unified Command moved to defeat it. At home the army's units "
              "must report their loyalty and the government must decide how far to trust them. The question is not only who "
              "rules this year, but how the army answers to civilians afterwards.",
              ('security', 'command'), requires=(After('1997.5.30'),), reward=(Event('coup_news'), Idea('coup_alert'))),
        Focus('loyalty_commission', 'An Army Loyalty Commission',
              "A commission of civil servants, judges and senior officers interviews every unit commander about the May "
              "days: where they were, who they called and what orders they gave. The army resents being questioned by "
              "outsiders. The alternative, trusting every officer on their word, is worse after what happened elsewhere in "
              "Usea.",
              ('scales', 'command'), after=('coup_news',), reward=(SwapIdea('coup_alert', 'army_loyalty_board'),)),
        Focus('defend_charter', 'Defend the Charter Ballot',
              "The charter restored earlier in the decade faces its first real test. Instead of suspending ballots in the "
              "emergency, the government keeps the electoral calendar and invites every district to watch the count. If it "
              "succeeds, the charter becomes harder to suspend again; if turnout falls, opponents will call it a failure.",
              ('ballot', 'scales'), after=('coup_news',), requires=(HasFlag('charter_path'),),
              reward=(SwapIdea('charter_rolls', 'charter_defended'),)),
        Focus('directorate_officers', 'Audit the Directorate Officers',
              "The administrative path chosen earlier left senior officials and officers working closely, with few "
              "outsiders watching. After the coup, the ministries' own auditors examine every contract between the army and "
              "the administration. Some friendships will end, and the audit shows that unelected government can still police "
              "its own ranks.",
              ('document', 'security'), after=('coup_news',), requires=(HasFlag('directorate_path'),),
              reward=(SwapIdea('performance_tables', 'performance_audit'),)),
        Focus('rein_rally', 'Rein In the Rally Halls',
              "A mass movement with drilled volunteers looks different after a coup. The government puts the rally halls' "
              "volunteer squads under the coast watch chain of command and bans uniforms outside parades. Movement veterans "
              "will call this betrayal, but the state cannot allow armed loyalties it does not control.",
              ('assembly', 'command'), after=('coup_news',), requires=(HasFlag('rally_path'),),
              reward=(SwapIdea('rally_halls', 'rally_discipline'),)),
        Focus('defence_directorate', 'Seat a Coastal Defence Directorate',
              "Hand government to a Coastal Defence Directorate of senior officers and security officials until Usea is "
              "calm. It promises order, fast decisions and a firm grip on the army it comes from. It suspends elections, "
              "overrides the districts and sets a precedent that every later government will have to unwind.",
              ('command', 'security'), after=('loyalty_commission',), exclusive=('civil_government',), cost=10,
              reward=(Regime('defence_directorate'), Flag('directorate_rule'), Event('directorate_seated'))),
        Focus('civil_government', 'Keep the Government Civilian',
              "Refuse to hand power to the officers, whatever the emergency. The civilian government keeps its ministries, "
              "places the army under a civilian oversight board and publishes its orders. It is slower in a crisis and the "
              "officer corps will grumble, but the country avoids inviting the army into politics.",
              ('civil', 'scales'), after=('loyalty_commission',), exclusive=('defence_directorate',), cost=10,
              reward=(Idea('civil_oversight'), Flag('civil_rule'))),
        Focus('quiet_officer_review', 'A Quiet Review of Officers',
              "Units confined to barracks during the coup reported at different speeds and in different moods. A "
              "confidential review of the late and reluctant commanders lets the army retire or move them without a public "
              "trial. The army keeps its dignity, but the public never learns who hesitated.",
              ('document', 'command'), after=('loyalty_commission',), requires=(HasFlag('barracks_confined'),),
              reward=(XP('army', 20), Stability(0.02))),
        Focus('street_patrols_end', 'Bring the Patrols Off the Streets',
              "Soldiers kept in the capital's streets after the coup reassured some people and frightened many others. "
              "Withdrawing them on a published schedule, district by district, returns policing to the police. Officers "
              "who enjoyed the visibility will object, and any incident during the withdrawal will be blamed on the "
              "decision.",
              ('security', 'civil'), after=('loyalty_commission',), requires=(HasFlag('army_in_streets'),),
              reward=(Stability(0.04), WarSupport(-0.02))),
        Focus('mutiny_code', 'A Written Mutiny Code',
              "Write down, for the first time, exactly what counts as mutiny, who judges it and what the penalties are. "
              "Officers know where the line is and the courts can enforce it. A written code also shows that the army can "
              "be held to account, which some commanders will read as an insult to their service.",
              ('document', 'scales'), after_any=('defence_directorate', 'civil_government'),
              exclusive=('reporting_amnesty',), reward=(Idea('mutiny_code_rules'),)),
        Focus('reporting_amnesty', 'Amnesty for Late Reporters',
              "Declare that any soldier or officer who reported late during the coup, without joining it, faces no further "
              "action. The amnesty ends speculation and lets the army move on. It also tells the next plotters that "
              "hesitation costs nothing, and officers who reported at once feel their loyalty went unrewarded.",
              ('peace', 'command'), after_any=('defence_directorate', 'civil_government'),
              exclusive=('mutiny_code',), reward=(Stability(0.05), PP(-15))),
        Focus('barracks_out', 'Barracks Out of the Capital',
              "The army's largest barracks sit beside the ministries, a reminder of how easily soldiers could reach the "
              "government. Moving the main garrison to new barracks in District B, beside the road and the farms, puts "
              "distance between the army and politics. The move is expensive, and officers' families will resist leaving "
              "the capital.",
              ('security', 'rebuild'), after_any=('mutiny_code', 'reporting_amnesty'),
              reward=(Build('infrastructure', 1, 32), XP('army', 10))),
    )),

    Branch('stonehenge', 'The Stonehenge Question', 1998, 'FOCUS_FILTER_POLITICAL', (
        Focus('railgun_debate', 'The Railgun Question',
              "In June 1998 Central Usea completed Stonehenge, eight railguns in neutral San Salvacion meant to break up the "
              "asteroid's fragments. This country is not part of the project and cannot know whether the guns will protect "
              "its coast. The government must decide how far to rely on them and what to build in case they fail.",
              ('missile', 'meteor'), requires=(After('1998.6.19'),), reward=(Event('stonehenge_debate'),)),
        Focus('join_council_watch', 'Join the Treaty Council Air Watch',
              "Share radar reports, debris tracking and air defence plans with the other Treaty Council members. The "
              "country gets early warning far beyond its own masts and a voice in the council's air committees. In return "
              "it accepts council standards and the expectation that its own skies will be watched by others too.",
              ('radar', 'diplomacy'), after=('railgun_debate',), exclusive=('declare_neutral_skies', 'every_capital'),
              cost=10, reward=(Idea('council_air_watch'), Flag('council_watch'))),
        Focus('declare_neutral_skies', 'Declare Neutral Airspace',
              "Announce that the national airspace is closed to every military aircraft but the country's own, whatever "
              "the emergency, and that the government takes no side in Usean disputes. Neutrality keeps the country out of "
              "other states' plans. It also means the air arm must watch and defend its skies without help.",
              ('air', 'peace'), after=('railgun_debate',), exclusive=('join_council_watch', 'every_capital'),
              cost=10, reward=(Idea('declared_neutral_airspace'), Flag('neutral_skies'))),
        Focus('every_capital', 'Talks With Every Capital',
              "Keep channels open to every Usean government, Treaty Council member or not, through trade missions, liaison "
              "officers and quiet consultations. The country becomes useful to everyone and committed to no one. The policy "
              "brings influence and information, but it relies on diplomats more than radar, and partners may doubt its "
              "word.",
              ('diplomacy', 'communications'), after=('railgun_debate',),
              exclusive=('join_council_watch', 'declare_neutral_skies'), cost=10,
              reward=(Idea('diplomatic_channels'), Flag('open_channels'))),
        Focus('capital_debris_radar', 'Debris Radar Over the Capital',
              "Whatever policy the country follows, it needs to see what is falling toward it. A debris tracking radar at "
              "the capital, paired with the weather records, gives minutes of warning instead of none. The equipment is "
              "imported, expensive and fragile in the humidity, and its operators must be trained in a hurry.",
              ('radar', 'meteor'), after_any=('join_council_watch', 'declare_neutral_skies', 'every_capital'),
              reward=(Build('radar_station', 1, 4), Research('radar_tech'))),
        Focus('radar_district_c', 'A Radar Post for District C',
              "The rubber coast has the country's busiest harbours and its longest exposed shore. A radar post on the hills "
              "behind the groves covers the harbour approaches and the sea lanes beyond. The jungle damages equipment "
              "quickly, so the post needs its own workshop, its own generator and a crew willing to live there.",
              ('radar', 'navy'), after=('capital_debris_radar',), reward=(Build('radar_station', 1, 459),)),
        Focus('radar_plateau', 'A Radar Post on the Plateau',
              "The plateau's height gives radar a long view across the flats and the interior. A post near the District F "
              "mining towns watches the inland approaches and the high debris tracks. It is the cheapest post to build and "
              "the hardest to supply with spare parts, which come up the slow railway.",
              ('radar', 'rail'), after=('capital_debris_radar',), reward=(Build('radar_station', 1, 539),)),
        Focus('relief_budget_shift', 'Move Air Funds to Relief',
              "Having decided to trust Stonehenge with the sky, the government moves part of the air defence budget into "
              "relief stores, hospitals and roads. The decision frees money now and saves lives after any impact. If the "
              "railguns miss a fragment headed for the coast, the decision will be remembered bitterly.",
              ('medical', 'economy'), after=('capital_debris_radar',), requires=(HasFlag('trust_railguns'),),
              reward=(TimedIdea('relief_fund', 730),)),
        Focus('debris_roofs', 'Debris Roofs for the Works',
              "Planning as if the railguns will miss means protecting what the country cannot replace. Reinforced roofs and "
              "blast walls go up over the capital's main works and the largest plant in each district. Production slows "
              "while builders work around the machines, but the works should survive anything short of a direct hit.",
              ('rebuild', 'industry'), after=('capital_debris_radar',), requires=(HasFlag('plan_for_misses'),),
              reward=(Stability(0.02), Research('construction_tech'))),
        Focus('capital_aa', 'Anti-Air Guns for the Capital',
              "Radar gives warning; guns give an answer. A ring of anti-air batteries around the capital, fed by the radar "
              "posts, protects the city and its works against hostile aircraft. Gun crews are drawn from the army reserve, "
              "and their training competes with every other demand on it.",
              ('missile', 'security'), after=('radar_district_c', 'radar_plateau'),
              reward=(Idea('capital_air_defence'),)),
    )),

    Branch('relief', 'Impact Relief', 1999, 'FOCUS_FILTER_STABILITY', (
        Focus('fragments_fall', 'When the Fragments Fell',
              "On 8 July 1999 Ulysses passed the Roche limit and broke apart, and fragments fell across the world. Reports "
              "from across Usea describe damaged towns, closed ports and families on the move. The government must "
              "organise relief at home and decide how to receive people arriving from elsewhere.",
              ('meteor', 'refugees'), requires=(After('1999.7.8'),),
              reward=(Event('impact_night'), Idea('relief_command'))),
        Focus('open_harbour_camps', 'Open Camps at the Harbours',
              "Receive displaced people at the District C and District E harbours in organised camps with food, clinics "
              "and registration. The camps are visible, easy to supply by sea and welcomed abroad. They also concentrate "
              "thousands of people in low coastal towns, and closing them later will be harder than opening them.",
              ('refugees', 'navy'), after=('fragments_fall',), exclusive=('disperse_inland',), cost=10,
              reward=(Idea('harbour_camp_system'), Flag('camps_opened'))),
        Focus('disperse_inland', 'Disperse the Displaced Inland',
              "Move arrivals quickly from the harbours to small reception points in District B, the plateau towns and the "
              "capital's outskirts. No single town carries the whole burden and nobody settles in a camp. Dispersal needs "
              "transport, roads and willing host families, and it spreads the strain into every district at once.",
              ('refugees', 'logistics'), after=('fragments_fall',), exclusive=('open_harbour_camps',), cost=10,
              reward=(Idea('inland_dispersal'),)),
        Focus('field_hospitals', 'Field Hospitals on the Flats',
              "Hospitals in the capital fill within days, and the district clinics cannot handle injuries or the sickness "
              "that follows crowding and broken water supplies. Field hospitals in tents and schools, staffed by army doctors "
              "and volunteers, spread care across the flats. They draw down medical stores that took years to build.",
              ('medical', 'shelter'), after=('fragments_fall',), reward=(TimedIdea('field_hospital_network', 540),)),
        Focus('clear_runways', 'Keep the Capital Runway Open',
              "Relief flights and medical evacuations need the capital runway open day and night, but it was built for a "
              "small air arm. Engineers add lighting, hardstands and a second taxiway so that cargo aircraft can unload "
              "while fighters stay on alert. Until the work is done, relief must come by road and sea.",
              ('runway', 'medical'), after=('fragments_fall',), reward=(Build('air_base', 1, 0), Stability(0.01))),
        Focus('army_relief_columns', 'Army Relief Columns',
              "Because the government sent the army to the coast, its lorries and engineers now carry food, water and "
              "tents along fixed relief routes. The columns are disciplined and fast. Soldiers gain experience in movement "
              "and supply, while some coastal towns grow uneasy at seeing troops in charge of their streets.",
              ('logistics', 'command'), after=('fragments_fall',), requires=(HasFlag('army_relief'),),
              reward=(XP('army', 20), WarSupport(0.02))),
        Focus('district_relief_boards', 'District Relief Boards',
              "Because relief was placed in the districts' hands, each district forms a board of officials, doctors and "
              "local volunteers that sets its own priorities. Help reaches people who know the board members. Districts "
              "with weak administrations, the empty ones above all, fall behind and ask the capital to step in.",
              ('assembly', 'medical'), after=('fragments_fall',), requires=(HasFlag('district_relief'),),
              reward=(TimedIdea('relief_fund', 365), Stability(0.01))),
        Focus('drained_camps', 'Camps on Drained Ground',
              "The drainage work on the flats pays a second dividend: dry ground for tents, kitchens and latrines through "
              "the rainy season. Placing camps and reception points on drained land prevents the floods and fevers that "
              "would otherwise follow. District B farmers lose some fields for the duration and expect compensation.",
              ('shelter', 'bridge'), after_any=('open_harbour_camps', 'disperse_inland'),
              requires=(HasFlag('drainage_complete'),), reward=(Build('infrastructure', 1, 32), Stability(0.03))),
        Focus('open_shelters', 'Shelters Open to the Displaced',
              "The shelters dug under the capital before the pass stand mostly empty once the immediate danger is over. "
              "Opening them as temporary housing for displaced families gives roofs and pumps to people who have neither. "
              "Residents who queued for places before the pass will ask why newcomers get them first.",
              ('shelter', 'refugees'), after_any=('open_harbour_camps', 'disperse_inland'),
              requires=(HasFlag('shelters_dug'),),
              reward=(Stability(0.04), Tooltip('Capital shelters house displaced families until the emergency ends.'))),
        Focus('evacuate_by_table', 'Evacuate by the Tables',
              "The evacuation tables drawn up for the coast now guide families out of damaged or threatened harbour streets. "
              "Because routes and shelters were assigned in advance, the movement is orderly and quick. People who ignored "
              "the drills, or whose streets were left off the tables, still need help from someone.",
              ('refugees', 'document'), after_any=('open_harbour_camps', 'disperse_inland'),
              requires=(HasFlag('evacuation_tables'),), reward=(Stability(0.03), Build('infrastructure', 1, 459))),
        Focus('drill_wardens', 'Drill Wardens on the Streets',
              "Wardens trained in the last drills before the pass already know every street, shelter and route in their "
              "districts. Putting them in charge of local registration and distribution saves days of confusion. They are "
              "volunteers, and many are exhausted after months of drills followed by weeks of real emergency.",
              ('training', 'civil'), after_any=('open_harbour_camps', 'disperse_inland'),
              requires=(HasFlag('drills_held'),), reward=(Stability(0.03), WarSupport(0.01))),
        Focus('rebuild_capital_roads', 'Rebuild the Capital Roads',
              "Relief traffic, heavy rain and overloaded lorries have broken the capital's roads faster than crews can patch "
              "them. A proper rebuilding programme, with drained foundations and new surfaces on the main routes, replaces "
              "patching with repair. It closes roads for months and takes engineers away from the districts.",
              ('rebuild', 'logistics'), after=('clear_runways',), reward=(Build('infrastructure', 2, 0),)),
        Focus('relief_wind_down', 'Wind Down the Emergency',
              "Emergency powers, ration cards and relief command posts were meant to be temporary. Ending them on a "
              "published date, district by district, returns ordinary government and tells people the worst has passed. "
              "Some officials prefer emergency powers, and some families still depend on relief that must become welfare.",
              ('peace', 'document'), after=('rebuild_capital_roads', 'field_hospitals'),
              reward=(RemoveIdea('relief_command'), Stability(0.03))),
    )),

    Branch('lean', 'The Lean Years', 2000, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
        Focus('lean_budget', 'A Budget for the Lean Years',
              "Shelters, reserves, relief and lost trade have emptied the treasury, and buyers for rubber and ore are "
              "scarce after the impact. A lean budget cuts new projects, freezes salaries and delays the districts' grants. "
              "It keeps the state solvent, but every district will feel the cuts and blame the capital for them.",
              ('economy', 'scales'), reward=(Idea('austerity_ledger'),)),
        Focus('harbour_quota', 'A Quota at the Harbours',
              "After Erusea stopped taking in refugees in April 2000, pressure on the smaller Usean coasts grew. A fixed "
              "yearly quota, processed at the District E harbour, lets the country admit families in an orderly way. The "
              "quota pleases relief agencies abroad and angers people at home who feel the lean years leave nothing to share.",
              ('refugees', 'scales'), after=('lean_budget',), exclusive=('close_coast', 'resettle_district_b'),
              requires=(After('2000.4.21'),), reward=(Flag('quota_set'), PP(40), Stability(-0.02))),
        Focus('close_coast', 'Close the Coast to New Arrivals',
              "Follow the Erusean example of April 2000 and stop admitting new arrivals by sea, apart from medical "
              "emergencies. The coast watch and the navy turn boats away. Many voters welcome the decision in the lean "
              "years, but the country's reputation abroad suffers and the navy's crews dislike the work they are given.",
              ('security', 'navy'), after=('lean_budget',), exclusive=('harbour_quota', 'resettle_district_b'),
              requires=(After('2000.4.21'),), reward=(Flag('coast_closed'), Stability(0.03), XP('navy', 10))),
        Focus('resettle_district_b', 'Resettle Arrivals in District B',
              "The homestead scheme on the District B plains still has land without families. Offering arrivals homestead "
              "plots on the same terms as citizens turns a burden into settlers. Older homesteaders worry about "
              "competition, and the scheme only works if the dykes and the market town keep pace with new farms.",
              ('refugees', 'rebuild'), after=('lean_budget',), exclusive=('harbour_quota', 'close_coast'),
              requires=(After('2000.4.21'), HasFlag('homesteads_open')),
              reward=(Build('industrial_complex', 1, 32), Stability(-0.01))),
        Focus('phantom_payroll', 'Cut the Phantom Payroll',
              "The payrolls published in the early years still show names that never come to work. With every coin now "
              "counted, the finance ministry removes them, along with duplicate allowances and pensions paid to the dead. "
              "The savings are real and quick, and the officials who signed those payrolls will be unhappy.",
              ('document', 'economy'), after=('lean_budget',), requires=(HasFlag('payrolls_published'),),
              reward=(PP(60), Stability(0.01))),
        Focus('reschedule_debts', 'Reschedule the Relief Debts',
              "The relief years were paid for partly with short loans that now fall due together. Negotiating longer terms "
              "with the lenders spreads payments across a decade. It costs more interest in total and gives creditors a say "
              "in the budget, but it avoids a default that would close every market to the country.",
              ('economy', 'diplomacy'), after=('lean_budget',), reward=(TimedIdea('debt_moratorium', 730), PP(20))),
        Focus('close_harbour_camps', 'Close the Harbour Camps',
              "The harbour camps opened after the impact have become semi-permanent towns with schools, markets and police "
              "posts. Closing them means moving residents into housing elsewhere or helping them leave. The process is "
              "slow, contested and expensive, but camps cannot remain the main address of thousands of families forever.",
              ('refugees', 'civil'), after=('lean_budget',), requires=(HasFlag('camps_opened'),),
              reward=(RemoveIdea('harbour_camp_system'), Stability(0.03))),
        Focus('quota_classes', 'Classes for the Quota Families',
              "Families admitted under the quota need language, work permits and schooling to stop depending on relief. "
              "Evening classes in District E, run by teachers and earlier arrivals, teach the national language and the "
              "rules of work. The classes are cheap, but they need steady funding through years when every budget line is "
              "challenged.",
              ('training', 'refugees'), after=('harbour_quota',),
              reward=(Stability(0.03), Tooltip('Evening classes run in every District E harbour town.'))),
        Focus('balance_ledger', 'Balance the Ledger',
              "Once the debts are rescheduled and the worst cuts have done their work, the budget can stop shrinking. "
              "Balancing the ledger restores the districts' grants on a smaller scale and lifts the salary freeze. It also "
              "makes the finance ministry the most powerful office in government, with a veto over every new idea.",
              ('scales', 'economy'), after=('reschedule_debts',),
              reward=(SwapIdea('austerity_ledger', 'balanced_ledger'),)),
    )),

    Branch('war', 'The Usean War', 2003, 'FOCUS_FILTER_WAR_SUPPORT', (
        Focus('war_news', 'News From San Salvacion',
              "In the summer of 2003 Erusea invaded neutral San Salvacion and seized Stonehenge, and in August Central Usea "
              "founded ISAF to resist. The railguns built to protect the continent are now turned against aircraft. The "
              "country must choose its own posture without sending its small forces abroad.",
              ('missile', 'communications'), requires=(After('2003.8.22'),),
              reward=(Event('war_summer'), WarSupport(0.03))),
        Focus('armed_neutrality', 'Armed Neutrality on the Coast',
              "Declare strict neutrality and back it with a full guard on the coast, the harbours and the airspace. No "
              "warring side may use the country's territory, ports or skies. The posture demands men and money for the "
              "whole war and gives the country no friends when it ends, but it keeps the fighting away.",
              ('security', 'peace'), after=('war_news',), exclusive=('quiet_help', 'trade_every_side'), cost=10,
              reward=(Idea('coast_neutrality'),)),
        Focus('quiet_help', 'Quiet Help for the Coalition',
              "Stay formally outside the war while selling fuel, rubber and repair work to the coalition's forces through "
              "the District E yards and the plateau oil fields. The arms works run at full capacity. The help is quiet only "
              "until someone on the other side notices, and the country's neutrality becomes a matter of opinion.",
              ('logistics', 'industry'), after=('war_news',), exclusive=('armed_neutrality', 'trade_every_side'),
              cost=10, reward=(Idea('quiet_logistics'),)),
        Focus('trade_every_side', 'Trade With Every Side',
              "Sell rubber, fuel and ship repairs to anyone who pays, coalition or Erusean, through neutral brokers. War "
              "prices refill the treasury emptied in the lean years. Both sides will suspect the country of favouring the "
              "other, and support for the war effort at home stays low because there is no side to support.",
              ('economy', 'navy'), after=('war_news',), exclusive=('armed_neutrality', 'quiet_help'), cost=10,
              reward=(Idea('wartime_trade'),)),
        Focus('ration_fuel_tyres', 'Ration Fuel and Tyres',
              "Whatever the country's posture, the war disrupts imports and raises prices. Rationing fuel and tyres for "
              "private use keeps the army, the coast guard and the relief services supplied. Drivers, farmers and traders "
              "feel it first and loudest, and a black market will grow in the harbour towns.",
              ('logistics', 'document'), after=('war_news',), reward=(Idea('war_rationing'),)),
        Focus('neutral_guard', 'Guard Posts on Every Harbour',
              "Neutrality means stopping warships, aircraft and armed boats that try to use the harbours or shelter in "
              "home waters. Guard posts with guns, searchlights and radio at each harbour make the declaration credible. "
              "They need a standing garrison through the war, drawn from reservists who would rather be at home.",
              ('security', 'navy'), after=('armed_neutrality',), reward=(Build('arms_factory', 1, 0), XP('army', 10))),
        Focus('coalition_yards', 'Coalition Repairs in District E',
              "Damaged coalition ships can be repaired in the District E yards without crossing any formal line. The yards "
              "fill with work, skilled hands return from abroad and the arms works gain contracts. Every repaired hull is "
              "also evidence that a hostile power could cite against the country's claim to be neutral.",
              ('tools', 'navy'), after=('quiet_help',),
              reward=(Build('arms_factory', 1, 520), Research('naval_equipment', 0.5, 1))),
        Focus('war_prices', 'War Prices for Rubber and Fuel',
              "Wartime demand pushes rubber and fuel prices higher than they have been in a decade. The treasury takes a "
              "windfall levy on exports and spends it on the capital's works before peace returns prices to normal. Growers "
              "and drillers complain that the state takes their good years and leaves them the bad.",
              ('economy', 'industry'), after=('trade_every_side',),
              reward=(Build('industrial_complex', 1, 0), PP(30))),
        Focus('reservist_depots', 'Reservists at the Raised Depots',
              "The depots moved above the mud line in the early years can now equip reservists called up for the war. Units "
              "mobilise faster and stay supplied through the rains. The call-ups take workers from farms and works just as "
              "wartime demand peaks, and employers ask for exemptions.",
              ('logistics', 'training'), after=('ration_fuel_tyres',), requires=(HasFlag('depots_above_mud'),),
              reward=(XP('army', 20), Research('land_doctrine'))),
        Focus('war_insurance', 'War Insurance at the Customs House',
              "Shipowners refuse to sail without war risk insurance, and foreign insurers charge ruinous rates. The single "
              "customs house can now issue state-backed war cover for ships carrying the country's cargo, priced from its "
              "complete trade records. Cover keeps the harbours working, and one sunk ship would cost the treasury dearly.",
              ('document', 'economy'), after=('ration_fuel_tyres',), requires=(HasFlag('single_customs'),),
              reward=(PP(40), Tooltip('Ships sailing from the District C harbours carry state war cover.'))),
        Focus('coast_watch_stands_to', 'The Coast Watch Stands To',
              "The coast watch founded after the Skully Islands rebellion has years of practice spotting strangers on the "
              "shore. In wartime it reports smugglers, deserters and armed boats that try to use quiet coves. Volunteers "
              "need pay and radios now rather than thanks, and some coastal villages resent being watched.",
              ('security', 'communications'), after=('ration_fuel_tyres',), requires=(HasFlag('coast_watch_founded'),),
              reward=(XP('navy', 15), Stability(0.02))),
        Focus('neutral_convoy_rules', 'Convoy Rules for Neutral Waters',
              "The convoy office writes new rules for wartime: neutral markings, lights, sailing lists filed with every "
              "navy in the area and routes that avoid the war zones. Merchant masters gain some protection from mistaken "
              "attacks. The rules slow trade and depend on warring navies respecting them, which is never certain.",
              ('navy', 'document'), after_any=('neutral_guard', 'coalition_yards', 'war_prices'),
              requires=(HasFlag('convoy_office_open'),), reward=(XP('navy', 20), Research('naval_equipment'))),
        Focus('council_liaison', 'Treaty Council Liaison Officers',
              "Membership in the council air watch gives the country a seat in its wartime coordination rooms. Liaison "
              "officers share radar tracks and warnings while the country stays formally outside the fighting. Early warning "
              "improves, but other members expect information to flow both ways and ask uncomfortable questions.",
              ('diplomacy', 'radar'), after_any=('neutral_guard', 'coalition_yards', 'war_prices'),
              requires=(HasFlag('council_watch'),), reward=(Build('radar_station', 1, 520), XP('air', 10))),
        Focus('neutral_skies_enforced', 'Neutral Skies, Enforced',
              "The neutral airspace declared in 1998 is tested by aircraft from both sides. Fighters scramble to intercept "
              "every intruder and escort it away or force it down. Pilots gain hard experience, and each incident risks a "
              "diplomatic quarrel or, worse, an exchange of fire that someone will call an act of war.",
              ('air', 'security'), after_any=('neutral_guard', 'coalition_yards', 'war_prices'),
              requires=(HasFlag('neutral_skies'),), reward=(XP('air', 25), WarSupport(0.03))),
        Focus('wartime_back_channels', 'Back Channels in Wartime',
              "The channels kept open to every capital since 1998 become valuable once Usea is at war. The country's "
              "diplomats carry messages about prisoners, shipping and local truces that the warring governments cannot send "
              "directly. The role brings influence and occasional gratitude, and it can end abruptly if a message goes wrong.",
              ('diplomacy', 'peace'), after_any=('neutral_guard', 'coalition_yards', 'war_prices'),
              requires=(HasFlag('open_channels'),), reward=(PP(60), Stability(0.02))),
        Focus('war_accounts', 'Close the War Accounts',
              "By the autumn of 2005 the government must decide when the emergency measures end, whatever the final terms "
              "abroad. Closing the war accounts lifts rationing, releases reservists and publishes what the war years cost. "
              "The publication will start arguments about the posture chosen in 2003 that will last for years.",
              ('document', 'peace'), after=('ration_fuel_tyres',),
              after_any=('neutral_guard', 'coalition_yards', 'war_prices'), requires=(After('2005.10.1'),),
              reward=(Event('war_ledger'), RemoveIdea('war_rationing'))),
    )),

    Branch('recovery', 'The Recovery Compact', 2006, 'FOCUS_FILTER_POLITICAL', (
        Focus('draft_compact', 'Draft the Recovery Compact',
              "Fifteen years of reform, warning, impact and war have left the country tired, indebted and still standing. A "
              "recovery compact sets out what the next decade must deliver: rebuilt harbours, a working plateau, settled "
              "districts and an honest government. Drafting it forces every faction to say what it wants and what it will "
              "give up.",
              ('rebuild', 'document'), reward=(Event('recovery_vote'), Idea('recovery_programme'))),
        Focus('open_elections', 'Return to Open Elections',
              "Whatever government brought the country through the war, the compact can end with a normal national election "
              "and a Recovery Assembly chosen by it. Parties will form around the old arguments about rubber, the plateau "
              "and the war years. Government becomes noisier and slower, and much harder for any group to capture.",
              ('ballot', 'assembly'), after=('draft_compact',), exclusive=('governors_council',), cost=10,
              reward=(Regime('recovery_assembly'), Stability(0.03))),
        Focus('governors_council', 'A Council of District Governors',
              "Let the compact be carried out by a council of the six district governors, appointed for their records in "
              "the relief and war years. Each district gains a direct voice in national decisions and the capital loses its "
              "automatic lead. Elections remain suspended, and governors may favour their districts over the country.",
              ('assembly', 'scales'), after=('draft_compact',), exclusive=('open_elections',), cost=10,
              reward=(Regime('governors_council'), PP(30))),
        Focus('rubber_exports_return', 'Rubber Exports Return',
              "With shipping insured again at normal rates, the rubber coast can sell abroad without wartime risks. New "
              "buyers, refurbished harbours and the latex works' spare capacity rebuild the trade. Prices are lower than at "
              "the wartime peak, and growers must accept that the windfall years are gone.",
              ('economy', 'navy'), after=('draft_compact',),
              reward=(Build('industrial_complex', 1, 459), Stability(0.02))),
        Focus('yard_contracts', 'Merchant Hull Contracts',
              "The District E yards survived on repair work and wartime orders. Long-term contracts for merchant hulls and "
              "fishing boats, backed by state guarantees, give them a steady order book for the first time since 1991. Yard "
              "workers gain security, while the treasury carries the risk if buyers default.",
              ('navy', 'economy'), after=('draft_compact',),
              reward=(Build('infrastructure', 1, 520), Research('naval_equipment', 0.5, 2))),
        Focus('directorate_stands_down', 'The Directorate Stands Down',
              "The Coastal Defence Directorate seated after the 1997 coup still holds offices it promised to hold only for "
              "the emergency. Standing down formally, with honours for its members and a professional army code in its "
              "place, closes the chapter. Some officers want to stay, and the army's new role must be written in law.",
              ('medal', 'command'), after_any=('open_elections', 'governors_council'),
              requires=(HasFlag('directorate_rule'),), reward=(SwapIdea('army_loyalty_board', 'professional_army'),)),
        Focus('civil_decade', 'A Decade of Civil Rule',
              "Since the coup the army has answered to a civilian board, and nearly a decade of practice has turned "
              "emergency oversight into routine. Writing the board's powers into a permanent civil service code makes the "
              "arrangement independent of any one government. Officers accept it more readily than they would have in 1997.",
              ('scales', 'document'), after_any=('open_elections', 'governors_council'),
              requires=(HasFlag('civil_rule'),), reward=(SwapIdea('civil_oversight', 'civil_service_code'),)),
        Focus('vote_observers', 'Observers for the Count',
              "Because the compact itself went to a national vote, every later count is watched closely. Inviting observers "
              "from abroad and from every district to the next national count shows that the result can be trusted. The "
              "observers will also report faults, and their reports will be read in every Usean capital.",
              ('ballot', 'diplomacy'), after_any=('open_elections', 'governors_council'),
              requires=(HasFlag('compact_vote'),), reward=(Stability(0.04), PP(20))),
        Focus('governors_conference', 'An Annual Governors Conference',
              "Because the governors signed the compact, they meet each year to review its progress district by district. "
              "The conference keeps the districts committed and spots failures early. It also becomes the place where "
              "governors trade favours, and the capital's ministries must attend as equals rather than as masters.",
              ('assembly', 'document'), after_any=('open_elections', 'governors_council'),
              requires=(HasFlag('compact_signed'),), reward=(TimedIdea('district_grants', 365), PP(15))),
        Focus('plateau_mill_upgrade', 'Plateau Mills to Modern Gauge',
              "The smelters built on the plateau in the early years are worn and inefficient. Rebuilding them to modern "
              "standards with better furnaces, cleaner power and automated rolling keeps District F competitive. The work "
              "idles the mills for a season and needs engineers trained at home rather than hired abroad.",
              ('industry', 'science'), after=('rubber_exports_return',), requires=(HasFlag('smelters_upland'),),
              reward=(SwapIdea('plateau_smelters', 'modern_plateau_mills'),)),
        Focus('ore_line_double', 'Double-Track the Ore Line',
              "The ore trains that have carried District F's output to the capital since the early years run on a single "
              "line that cannot take more traffic. Doubling the track and adding modern wagons lets the capital's works grow. "
              "The plateau towns, still mostly mining camps, ask again what they gain from the arrangement.",
              ('rail', 'logistics'), after=('rubber_exports_return',), requires=(HasFlag('ore_line'),),
              reward=(SwapIdea('ore_trains', 'double_ore_line'),)),
        Focus('reopen_coast', 'Reopen the Coast to Arrivals',
              "The coast closed to new arrivals in 2000 remains closed years after the emergency that justified it. "
              "Reopening it under a modest annual quota restores the country's standing abroad and brings workers to "
              "districts that need them. Opponents argue that the closure kept the lean years bearable and should stay.",
              ('gate', 'refugees'), after=('yard_contracts',), requires=(HasFlag('coast_closed'),),
              reward=(Build('infrastructure', 1, 459), Stability(-0.02))),
        Focus('quota_citizenship', 'Citizenship for Quota Families',
              "Families admitted under the harbour quota in the lean years have lived, worked and paid taxes here for years. "
              "A path to citizenship ends their uncertain status and makes them full members of their districts. "
              "Nationalist groups object loudly, but employers and district governors back the measure.",
              ('document', 'civil'), after=('yard_contracts',), requires=(HasFlag('quota_set'),),
              reward=(Stability(0.03), PP(-20))),
        Focus('compact_accounts', 'Close the Compact Accounts',
              "By the end of its decade the recovery compact should show results in the ledgers rather than in speeches. "
              "Auditors compare its promises with miles of road, harbour tonnage and plateau output. The report decides "
              "whether the compact's programme becomes the normal way of government or is quietly replaced.",
              ('scales', 'rebuild'), after=('rubber_exports_return', 'yard_contracts'), requires=(After('2014.1.1'),),
              reward=(SwapIdea('recovery_programme', 'steady_growth'),)),
    )),

    Branch('decade', 'The Second Decade', 2011, 'FOCUS_FILTER_RESEARCH', (
        Focus('college_charter', 'A National Technical College',
              "The country has spent twenty years hiring engineers, controllers and chemists from abroad or training them in "
              "a hurry. A national technical college in the capital, with workshops at the yards, the latex works and the "
              "plateau mills, trains them at home. It takes a decade to repay itself and competes with schools for every "
              "teacher.",
              ('science', 'training'), reward=(Idea('technical_college'),)),
        Focus('yard_electronics', 'Electronics Courses for the Yards',
              "Modern hulls carry more electronics than steel by value, and the District E yards cannot fit or repair them. "
              "A college course with a teaching workshop at the yards trains technicians to install and maintain sensors, "
              "radios and engine controls. Graduates are in demand everywhere, and some will leave for better pay abroad.",
              ('science', 'navy'), after=('college_charter',),
              reward=(Research('electronics', 0.5, 2), Build('industrial_complex', 1, 520))),
        Focus('weather_radar_net', 'A Weather Radar Network',
              "The single weather radar at the capital cannot see storms forming over the sea or the desert. New masts on "
              "the District E coast and in the hinterland give the forecasters a national picture. Farmers, the yards and "
              "the air arm all benefit, and the masts double as a watch on the sky.",
              ('radar', 'satellite'), after=('college_charter',),
              reward=(Build('radar_station', 1, 520), Build('radar_station', 1, 512))),
        Focus('ground_station', 'A Satellite Ground Station',
              "Weather, navigation and communications increasingly come from satellites the country does not own. A ground "
              "station at the capital receives and processes their data for the forecasters, the harbours and the "
              "government. It ties the country to foreign operators, and the dish is the most expensive instrument it has "
              "ever bought.",
              ('satellite', 'communications'), after=('weather_radar_net',),
              reward=(Research('electronics', 0.75, 1), Research('radar_tech'))),
        Focus('relay_data_line', 'Relay Masts Into a Data Line',
              "The relay masts built across the hinterland in the early years now carry little traffic. Re-equipping them as "
              "a digital data line links the plateau, the far coast and the capital to the college and the forecasters. It "
              "is a cheap upgrade because the masts, wells and access tracks already exist.",
              ('communications', 'rail'), after=('weather_radar_net',), requires=(HasFlag('relay_masts'),),
              reward=(Build('infrastructure', 1, 512), Research('electronics', 0.5, 1))),
        Focus('latex_chemistry', 'Rubber Chemistry Laboratories',
              "Natural rubber now competes with synthetic products everywhere. Laboratories at the college and the latex "
              "works develop specialty compounds, medical goods and industrial seals that sell for far more than raw sheet. "
              "The research takes years to pay and needs chemists the country has only recently begun to train.",
              ('science', 'industry'), after=('college_charter',),
              reward=(Research('synth_resources', 0.5, 2), Build('industrial_complex', 1, 4))),
        Focus('plateau_engineering', 'Plateau Engineering Course',
              "Mining, smelting and railway engineering on the plateau have always depended on a few experienced men and "
              "women. A college course based in District F turns their knowledge into a curriculum, with field work in the "
              "seams and the mills. Graduates stay on the plateau more often than those trained in the capital.",
              ('training', 'tools'), after=('college_charter',),
              reward=(Research('excavation_tech'), Research('engineers_tech'))),
        Focus('graduates_service', 'Graduates Into the Ministries',
              "The first college graduates are ready for public service. Placing them in the ministries, the yards and the "
              "district offices replaces some officials appointed during the emergencies with technically trained staff. "
              "Older officials resist being judged by people half their age, but the government becomes more capable.",
              ('document', 'science'), after=('yard_electronics', 'weather_radar_net', 'plateau_engineering'),
              reward=(SwapIdea('technical_college', 'graduate_service'), PP(30))),
        Focus('thirty_year_account', 'A Thirty-Year Account',
              "Nearly thirty years after the National Administration's audit, the government publishes a full account of "
              "what the country built, lost and changed. Districts compare their roads, works and harbours with the figures "
              "of 1991. The account will be argued over, but it gives the next generation a baseline as honest as the first.",
              ('document', 'medal'), after=('graduates_service',), requires=(After('2019.1.1'),),
              reward=(Stability(0.03), PP(50), Tooltip('The account is printed district by district, as in 1991.'))),
    )),
)
