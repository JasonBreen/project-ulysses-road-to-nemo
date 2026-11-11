"""Relentio (REL): bespoke national focus tree, era e1 (1991 to 2005).

Relentio owns nothing on 1 January 1991. It is one of Perbla's crown lands, and this
tree applies only once it exists as a released country; tools/release_foundations owns
when and how that happens, and nothing here assumes a date or a mechanism. Its own
states are its cores (173 Faroe, 207 Torre Mountain, 236 Sofern, 597 North Relentio)
plus its history capital (581); every build stays guarded by owns_state and targets
only the four cores.

Source layers. Mod provenance: the inherited history file, the Office of the Crown
character, the country names, the core states and their place names, the Belkan War
outcome flags, and the Perbla spec (tools/world_depth/pbl/content.py), whose crown-lands
branch this tree never contradicts. Official: a few ACES Chronicle rows used only as
date anchors for regional pressure. Everything else, including every Relentian choice,
office, idea, building and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='REL', name='Relentio', root='world', package='rel',
                  themes=('navy', 'assembly', 'industry'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited Relentio history: monarchism ruling at 70 percent popularity, elections not allowed, no starting ideas, '
           'and the REL_ac_government_office character (Office of the Crown, constitutional_monarchy, no named holder). The '
           'country is the Duchy of Relentio under monarchism and the Republic of Relentio under every other ideology.',
           'mod/2985041246/history/countries/REL - Relentio.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/countries_l_english.yml; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml'),
    Source('Mod provenance',
           'Release-country scope: REL owns no state in 1991; its cores are 173, 207, 236 and 597 (all owned by PBL) and its '
           'history capital is 581. tools/release_foundations owns when and how Relentio exists; this tree assumes neither, '
           'and its builds target only the four cores under owns_state guards.',
           'tools/release_foundations/intake.json (REL); tools/world_foundation/country_registry.json (REL); '
           'docs/WORLD_RELEASE_FOUNDATIONS.md'),
    Source('Mod provenance',
           'Geography and place names from existing localisation only: Faroe (173, victory point Driscol), Torre Mountain (207), '
           'Sofern (236, victory point Sofern), North Relentio (597, victory point Fraeport). Resources and buildings from the '
           'state histories. Neighbouring names (Perbla, Gatewood, Serenava, Terentio) come from the Perbla spec and localisation.',
           'mod/2985041246/history/states/173-State_173.txt, 207-State_207.txt, 236-State_236.txt, 597-State_597.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml'),
    Source('Mod provenance',
           'Consistency with the approved Perbla tree: Relentio as the crown land of the Sofern docks and its harbour councils, '
           'the arms halls of the Relentio valley, and Torre Mountain inland. Nothing here narrates which Perblan focuses were '
           'taken before Relentio governs itself.',
           'tools/world_depth/pbl/content.py (LANDS, HEAVY and COAST branches)'),
    Source('Mod provenance',
           'Campaign hooks read only outcomes the mod already records: belka_lost_belkan_war and belka_won_belkan_war, set by '
           'the Belkan War events, and belka_dropped_nukes. Each is a separate gameplay branch; none is asserted as history.',
           'mod/2985041246/events/Belka.txt'),
    Source('Official', 'Date anchor only: the Ulysses close-approach warning.', '1994 / 12.10'),
    Source('Official', 'Date anchor only: the Belkan War breaks out.', '1995 / 03.25'),
    Source('Official', 'Date anchor only: Belkan nuclear devices in the Waldreich Mountains.', '1995 / 06.06'),
    Source('Official', 'Date anchor only: the treaty signed in Lumen ends the Belkan War.', '1995 / 06.20'),
    Source('Official', 'Date anchor only: the announcement that Ulysses will strike the Earth.', '1996 / 04.20'),
    Source('Official', 'Date anchor only: Ulysses passes through the Roche limit.', '1999 / 07.08'),
    Source('Official', 'Date anchor only: the FCU demand to Erusea and the founding of the ISAF in Usea.', '2003 / 08.22'),
    Source('Provisional gameplay',
           'All Relentian focuses, ideas, offices, decisions, buildings, flags and events in this spec. No named people; offices '
           'are collective and unnamed; no border, core, war, annexation or faction effects; no new place names.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # who governs
    IdeaDef('chamber_convened', 'A Chamber Still Finding Its Feet',
            'The chamber sits, the ducal office keeps the seals, and nobody has yet settled who decides what.',
            {'political_power_gain': 0.05, 'stability_factor': -0.03}, ('assembly', 'ballot')),
    IdeaDef('ducal_charter', 'The Ducal Charter', 'Ministers answer to the chamber and the ducal office signs on their advice.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'document')),
    IdeaDef('seals_mandate', 'The Seals Mandate', 'A council named by the ducal office holds the seals, the budget and the coast guard.',
            {'political_power_gain': 0.20, 'stability_factor': -0.02}, ('command', 'document')),
    IdeaDef('merchant_mandate', 'The Merchant Mandate', 'The harbour councils press for a republic run like a well-kept ledger.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.03, 'political_power_gain': -0.05}, ('assembly', 'economy')),
    IdeaDef('ducal_constitution', 'A Written Ducal Constitution', 'One text says what the ducal office may sign and what the chamber must approve.',
            {'stability_factor': 0.08, 'political_power_factor': 0.08}, ('scales', 'document')),
    IdeaDef('seals_code', 'The Standing Code of the Seals', 'The council governs by a published code instead of case-by-case orders.',
            {'political_power_gain': 0.25, 'stability_factor': 0.03}, ('command', 'scales')),
    IdeaDef('republic_rights', 'The Republican Bill of Rights', 'Courts protect the press, the unions and the small districts from any one majority.',
            {'stability_factor': 0.06, 'consumer_goods_factor': -0.04, 'research_speed_factor': 0.02}, ('scales', 'assembly')),
    # the port
    IdeaDef('customs_ledger', 'The Sofern Customs Ledger', 'Every cargo across the quays is counted, and the count is the treasury.',
            {'political_power_gain': 0.05}, ('economy', 'navy')),
    IdeaDef('free_port', 'The Free Port of Sofern', 'Low duties and bonded sheds draw foreign firms to the quays.',
            {'consumer_goods_factor': -0.05, 'production_speed_buildings_factor': 0.05}, ('economy', 'diplomacy')),
    IdeaDef('port_authority', 'The Relentian Port Authority', 'One public authority owns the quays, sets the tariffs and plans the dredging.',
            {'political_power_gain': 0.10, 'production_speed_infrastructure_factor': 0.10}, ('command', 'navy')),
    IdeaDef('insurance_exchange', 'The Sofern Insurance Exchange', 'Shippers insure their hulls and cargoes at home, priced with local knowledge.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.02}, ('scales', 'navy')),
    IdeaDef('transit_levy', 'The Transit Levy', 'A small charge on transit cargo pays for dredging and quay repairs.',
            {'production_speed_infrastructure_factor': 0.10, 'political_power_gain': 0.05}, ('economy', 'tools')),
    IdeaDef('port_plan', 'The Twenty Year Port Plan', 'Every dredge, crane and siding is costed and scheduled years in advance.',
            {'production_speed_buildings_factor': 0.06, 'planning_speed': 0.05}, ('document', 'navy')),
    IdeaDef('night_shifts', 'Night Shifts on the Quays', 'Floodlights and double crews keep the cranes working through the night.',
            {'industrial_capacity_dockyard': 0.05, 'stability_factor': -0.01}, ('navy', 'tools')),
    # the treasury
    IdeaDef('thin_treasury', 'A Thin Treasury', 'Customs, a patchwork of district taxes and obligations nobody has fully totalled.',
            {'political_power_gain': -0.05, 'stability_factor': -0.02}, ('scales', 'economy')),
    IdeaDef('assessment_year', 'The Assessment Year', 'Assessors are rebuilding the tax roll district by district.',
            {'political_power_gain': 0.10, 'stability_factor': -0.03}, ('document', 'civil')),
    IdeaDef('customs_windfall', 'Customs Pledged to Payroll', 'Harbour duty is pledged first to salaries and pensions.',
            {'political_power_gain': 0.10}, ('economy', 'document')),
    IdeaDef('sound_books', 'Balanced Books', 'No new borrowing until lenders trust the record.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05, 'production_speed_buildings_factor': -0.03}, ('scales', 'document')),
    IdeaDef('development_credit', 'The Development Credit Bank', 'Cheap state credit for the halls, the yards and the port workshops.',
            {'production_speed_industrial_complex_factor': 0.10, 'stability_factor': -0.02}, ('economy', 'industry')),
    # the valley
    IdeaDef('idle_halls', 'Idle Halls in the Valley', 'Arms lines built for a larger army stand half used.',
            {'production_factory_efficiency_gain_factor': -0.03}, ('industry', 'document')),
    IdeaDef('civil_lines', 'Civil Lines in the Valley', 'The halls make tractors, pumps, wagons and machine tools.',
            {'production_speed_industrial_complex_factor': 0.08, 'consumer_goods_factor': -0.03}, ('rebuild', 'industry')),
    IdeaDef('export_lines', 'Licensed Export Lines', 'The halls keep making arms for buyers the export board approves.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04}, ('missile', 'economy')),
    IdeaDef('valley_overtime', 'Valley Overtime', 'Extra shifts in the halls while the orders last.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'tools')),
    # neighbours
    IdeaDef('gatewood_ties', 'Close Ties with Gatewood', 'Shared standards and coordinated tariffs with Perbla.',
            {'stability_factor': 0.04, 'production_speed_infrastructure_factor': 0.10}, ('diplomacy', 'rail')),
    IdeaDef('osean_market', 'The Osean Market', 'Osean lines and buyers have favoured berths at Sofern.',
            {'consumer_goods_factor': -0.04, 'industrial_capacity_factory': 0.03}, ('economy', 'diplomacy')),
    IdeaDef('open_harbour', 'A Harbour for Every Flag', 'One published tariff for every flag, and no bloc at all.',
            {'army_core_defence_factor': 0.05, 'political_power_gain': 0.08}, ('peace', 'navy')),
    IdeaDef('osean_charters', 'Osean Berth Contracts', 'Osean lines hold long contracts for the best Sofern berths.',
            {'consumer_goods_factor': -0.03, 'production_speed_buildings_factor': 0.03}, ('navy', 'economy')),
    IdeaDef('flag_registry', 'Neutral Papers for Hire', 'Foreign owners register hulls in Sofern under inspected rules.',
            {'political_power_gain': 0.08, 'naval_coordination': 0.03}, ('document', 'navy')),
    IdeaDef('export_orders', 'Export Orders on the Books', 'Signed foreign orders keep the lines busy.',
            {'industrial_capacity_factory': 0.03, 'stability_factor': 0.02}, ('economy', 'logistics')),
    # defence
    IdeaDef('coast_guard', 'The Relentian Coast Guard', 'Patrol boats, a few aircraft and crews who know the coast.',
            {'navy_org_factor': 0.04, 'naval_coordination': 0.03}, ('navy', 'security')),
    IdeaDef('volunteer_force', 'A Volunteer Defence Force', 'Long-service sailors, marines and pilots on career contracts.',
            {'army_org_factor': 0.05, 'experience_gain_army_factor': 0.08}, ('medal', 'training')),
    IdeaDef('harbour_militia', 'Harbour and Valley Militia', 'Former servicemen on local rolls, drilling a few weekends a year.',
            {'army_core_defence_factor': 0.08, 'training_time_army_factor': -0.08}, ('security', 'civil')),
    IdeaDef('interceptor_wing', 'The Sofern Interceptor Wing', 'A few modern aircraft trained to find and escort intruders.',
            {'air_superiority_efficiency': 0.05, 'air_detection': 0.05}, ('air', 'radar')),
    # the Belkan War years
    IdeaDef('war_risk_rates', 'War Risk Premiums', 'Insurers charge extra for every lane near the fighting.',
            {'consumer_goods_factor': 0.04, 'stability_factor': -0.02}, ('navy', 'scales')),
    IdeaDef('closed_port', 'No War Cargo at Sofern', 'Munitions for any belligerent are barred from the quays and the flag.',
            {'stability_factor': 0.04, 'consumer_goods_factor': 0.02}, ('peace', 'security')),
    IdeaDef('wartime_freight', 'Wartime Freight', 'Any lawful cargo for any customer, at wartime rates.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.03}, ('logistics', 'economy')),
    IdeaDef('shared_schedules', 'Shared Sailing Schedules', 'Relentian and Perblan shipping offices exchange schedules and warnings.',
            {'naval_coordination': 0.05, 'stability_factor': 0.02}, ('communications', 'navy')),
    IdeaDef('war_charters', 'Osean War Charters', 'Relentian freighters carry civilian goods for Osean lines.',
            {'industrial_capacity_dockyard': 0.05, 'war_support_factor': -0.03}, ('logistics', 'diplomacy')),
    IdeaDef('neutral_markings', 'Neutral Colours at Sea', 'Every Relentian hull carries large lit neutral markings.',
            {'naval_speed_factor': 0.03, 'stability_factor': 0.03}, ('peace', 'navy')),
    IdeaDef('fallout_watch', 'The Fallout Watch', 'Daily wind, rain, food and water readings after Waldreich.',
            {'stability_factor': -0.02, 'research_speed_factor': 0.02}, ('medical', 'telescope')),
    IdeaDef('reconstruction_freight', 'Reconstruction Freight', 'Ships and quays for the rebuilding after the war.',
            {'industrial_capacity_factory': 0.04, 'consumer_goods_factor': -0.02}, ('rebuild', 'navy')),
    IdeaDef('belkan_buyers', 'Belkan Buyers', 'A victorious Belka buys steel, trucks and port services.',
            {'production_speed_arms_factory_factor': 0.06, 'stability_factor': -0.02}, ('diplomacy', 'industry')),
    IdeaDef('new_tenants', 'From Berths to Tenancies', 'Wartime arrivals housed and placed in work.',
            {'stability_factor': 0.02, 'production_speed_buildings_factor': 0.03}, ('refugees', 'civil')),
    # Ulysses
    IdeaDef('sky_watch', 'Under the Ulysses Warning', 'Every district plans for a danger nobody can yet place on a map.',
            {'stability_factor': -0.02, 'war_support_factor': 0.03}, ('meteor', 'telescope')),
    IdeaDef('deep_cellars', 'Cellars Under the Cities', 'Deep shelters under Sofern and Driscol, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('evacuation_drill', 'The Evacuation Timetable', 'Ferries, trains and trucks rehearsed to move the coast inland.',
            {'stability_factor': 0.04, 'planning_speed': 0.05}, ('logistics', 'rail')),
    IdeaDef('hospital_reserve', 'Hospitals in Reserve', 'Field hospitals stored in the Torre Mountain districts.',
            {'stability_factor': 0.03, 'war_support_factor': 0.02}, ('medical', 'shelter')),
    # the new century
    IdeaDef('usean_war_rates', 'Usean War Premiums', 'Insurers reprice every lane after war breaks out in Usea.',
            {'consumer_goods_factor': 0.03, 'naval_coordination': 0.03}, ('navy', 'diplomacy')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('ducal_ministry', 'Ducal Ministry of the Chamber',
           'A cabinet drawn from the majority of the Relentian chamber, governing collectively in the name of the ducal crown '
           'and answerable for every budget it passes. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('seals_council', 'Council of the Ducal Seals',
           'A small council named by the ducal office that keeps the seals, the budget and the coast guard, with the chamber '
           'called only for advice. Provisional gameplay office with no named holder.',
           'monarchism', 'absolutism'),
    Office('harbour_republic', 'Executive Council of the Harbour Republic',
           'An executive council elected by the chamber of the Republic of Relentio on a fixed calendar, with the ducal title '
           'retired. Provisional gameplay office with no named holder.',
           'democratic', 'liberalism', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('who_governs', 'Who Governs Relentio', (
        "The chamber meets for its first full session in a hall borrowed from the Sofern harbour councils, because no building "
        "in Relentio was designed to hold a national parliament. The ducal office sends its clerk with a short message: the "
        "seals are kept, the coast guard is paid and a budget will follow. Everything else, the message says, is for the "
        "chamber to argue.",
        "And argue it does. Shipowners from Sofern want a government that moves as quickly as a freight market. Deputies from "
        "the Relentio valley around Driscol want protection for the arms halls and the wages they pay. The Torre Mountain "
        "districts, smallest of all, want a guarantee that the coast will not outvote them on every question. A few voices ask "
        "whether a ducal crown suits a state of merchants at all.",
        "No camp holds a majority today. What the session can decide is how the question will be argued: openly, with the "
        "press gallery full and every speech printed, or quietly, in committee rooms where bargains are easier to strike and "
        "harder to explain. Either way, the shipping lines, the valley unions and the officer corps are already counting "
        "their friends.",
    ), (
        Option('Open the gallery to the press.', (Stability(0.03), PP(-15))),
        Option('Settle it in committee.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('sofern_quays', 'The Sofern Customs Count', (
        "For a full season the customs clerks of Sofern have counted everything: every container, sack and barrel that "
        "crosses the quays, every receipt issued and every receipt that should have been. Their tally lands on the minister's "
        "desk in four thick volumes and a one-page summary that nobody in the harbour wanted written.",
        "The port is busier than the old books admitted. Duty that ought to reach the treasury has leaked through favours, "
        "private storage deals and gate staff whose wages never matched their houses. The harbour councils insist that most "
        "of the leak is custom rather than crime, and that the port would stall if every old arrangement ended overnight. "
        "Shipping agents warn that foreign lines are watching how Relentio treats its largest asset.",
        "The government has to choose how to use what it now knows. It can publish the count and let the press and the "
        "chamber chase the missing money, at the cost of a bruising year on the quays. Or it can use the figures quietly to "
        "renegotiate with the councils, gaining revenue without headlines and leaving the old arrangements half intact.",
    ), (
        Option('Publish the count in full.', (Stability(-0.02), WarSupport(0.01), PP(10))),
        Option('Renegotiate quietly with the councils.', (PP(35),)),
    ), picture=2),
    EventDef('first_budget', 'The First Relentian Budget', (
        "The first Relentian budget is presented to the chamber on a grey morning, printed on paper ordered in a hurry and "
        "bound with string. It lists customs receipts, a patchwork of valley taxes and a long column of obligations that the "
        "government must honour before it can promise anything new. The finance office reads it aloud in under an hour; the "
        "debate takes three weeks.",
        "Deputies from Sofern want lower duties to keep the shipping lines loyal. Valley deputies want credit for the arms "
        "halls and their suppliers. Torre Mountain wants its haul road. Everyone wants the coast guard paid and nobody wants "
        "to pay for it. Foreign banks send polite letters asking about the state's intentions, and the polite tone fools no "
        "one about what the letters mean.",
        "The government must decide what kind of first impression to make. A lean budget with no borrowing would reassure "
        "lenders and disappoint almost everyone at home. A budget that borrows to set the ports and the valley moving would "
        "please the chamber and test the patience of creditors who have never lent to Relentio before. The finance office has drafted both versions and waits for a decision.",
    ), (
        Option('Present a lean budget.', (Stability(0.02), PP(-10))),
        Option('Borrow to get things moving.', (PP(25), Stability(-0.02))),
    ), picture=1),
    EventDef('valley_halls', 'Silence in the Valley Halls', (
        "The inspection team returns from the Relentio valley and Torre Mountain with notebooks full of numbers and "
        "photographs of empty floors. Some halls run three shifts on orders signed long ago. Others stand idle with their "
        "machines oiled and covered, waiting for contracts that were meant for a much larger army. A few were never finished "
        "at all.",
        "Around Driscol the halls are the economy. Shops, schools and bus routes exist because the plants pay wages, and every "
        "rumour of closure empties the cafes. At Torre Mountain the arms lines sit beside the ore beds and a haul road that "
        "barely survives each winter. The unions want guarantees, the managers want orders and the banks want to know who "
        "will pay if neither arrives.",
        "The government must decide how to speak about the valley before it decides what to do there. A frank statement that "
        "some halls will close would let planning begin and frighten thousands of families. A promise that every hall has a "
        "future would buy calm now and make every later choice more expensive. The banks are waiting for the answer as eagerly as the unions.",
    ), (
        Option('Tell the valley the truth.', (Stability(-0.02), Research('industry', 0.5, 1))),
        Option('Promise every hall a future.', (Stability(0.02), PP(-20))),
    ), picture=1),
    EventDef('gatewood_envoys', 'Envoys at Gatewood', (
        "The Relentian envoys travel to Gatewood with a list of practical questions and instructions to avoid grand ones. Who "
        "pays the pensions of officials who served the crown lands? Which court hears a dispute between a Sofern shipper and "
        "a Perblan buyer? How do freight trains clear a frontier desk that older timetables never had to allow for?",
        "The envoys are received correctly and carefully. Both peoples share courts, schools, family ties and a long habit of "
        "doing business together, and neither government wants a quarrel that would block the rails or the quays. Yet both "
        "also know that every agreement signed now becomes a precedent, and that their own chambers will read each clause "
        "looking for concessions. Officials keep the old shared files open on the table between them, because nobody yet knows which records belong to whom.",
        "The envoys must decide what tone to set. They can ask for a broad settlement covering trade, transit and pensions in "
        "one package, which would take longer and risk a single failure sinking everything. Or they can settle small matters "
        "one at a time, building trust slowly and leaving the hardest questions for later governments.",
    ), (
        Option('Seek a broad settlement.', (PP(-20), Stability(0.03))),
        Option('Settle small matters first.', (PP(20), Stability(0.01))),
    ), picture=0),
    EventDef('belkan_war_sea', 'War on the Shipping Lanes', (
        "In the spring of 1995 the crisis around Belka becomes open war. Relentio is not a party to it, and none of its "
        "soldiers is anywhere near a front. Its ships are another matter. Within days, freighters bound for Sofern report "
        "warships asking for their papers, and insurers in foreign markets publish new war-risk premiums for every lane near "
        "the fighting.",
        "The port reacts the way ports always do. Some shipowners lay up their hulls and wait; others raise their rates and "
        "sail. Cargo that used to go elsewhere suddenly arrives at Sofern, some of it with paperwork that does not bear close "
        "reading. On the third day a freighter under a foreign flag docks with a manifest listing machine parts and a hold "
        "that the customs officers are not allowed to see.",
        "The government must decide how hard to look. Holding the ship for a full inspection would show every warring power "
        "that Relentian quays are not a convenient back door, and it would start an argument with the ship's owners and their "
        "government. Letting it unload with a written warning keeps trade moving and leaves the question of what was in the "
        "hold to someone else.",
    ), (
        Option('Hold the ship for inspection.', (WarSupport(0.02), Event('held_freighter', 10))),
        Option('Let it unload with a warning.', (PP(15), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in tools/lore/chronicle.json; the Relentian response is gameplay',
        picture=2),
    EventDef('held_freighter', 'The Held Freighter', (
        "Ten days after the freighter was held, the inspection is complete. Customs officers and marines have opened every "
        "container in the hold. Most contain exactly what the manifest promised. Several do not: crated spare parts for "
        "military vehicles, packed beneath machine tools and invoiced to a trading company that shares its address with a "
        "laundry.",
        "The ship's owners protest that they had no idea, and their government sends a note demanding the vessel's release. "
        "Two other governments, on opposite sides of the war, send notes of their own asking what was found. The harbour "
        "councils complain that the inspection has frightened other shippers, while the coast guard points out that "
        "frightening careless shippers was the whole point.",
        "The parts sit in a Relentian shed and the ship is tied up at a Relentian quay. The government can confiscate the "
        "cargo and release the ship, setting a clear rule that will be tested again, or return everything with a formal "
        "protest and a fine, keeping the quarrel small and the precedent vague. Whatever it decides will be read in every "
        "shipping office on the coast.",
    ), (
        Option('Confiscate the cargo and release the ship.', (WarSupport(0.03), Stability(0.01), PP(-10))),
        Option('Fine the owners and let it go.', (PP(25), Stability(-0.01))),
    ), picture=2),
    EventDef('ulysses_coast', 'A Coast Under Ulysses', (
        "The announcement of April 1996 turns the asteroid Ulysses from an astronomers' topic into a government's problem. The "
        "world is told that the asteroid will strike the Earth and that every nation must prepare, yet nobody can say where "
        "its fragments will fall. For a state whose people live almost entirely along the coast, every possible answer is "
        "frightening.",
        "Engineers warn about waves as well as impacts: a fragment at sea could push water into the low streets of Sofern and "
        "Fraeport. Planners argue for shelters, or for evacuation, or for both, and the treasury reminds them that it cannot "
        "buy everything at once. Shipowners ask whether their fleets will be requisitioned. Churches fill, and hardware shops "
        "run out of tinned food within a week.",
        "Before it chooses any plan, the government must decide how to speak. It can publish everything it knows and "
        "everything it does not, trusting citizens with uncertainty, or it can keep the message calm and short while the "
        "experts work. Both approaches have costs, and the first public statement will be quoted back at ministers for years.",
    ), (
        Option('Publish everything we know.', (WarSupport(0.02), Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Keep the message calm.', (Stability(0.02),)),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20 in tools/lore/chronicle.json; '
                'Relentian preparations are gameplay', picture=0),
    EventDef('sky_watch_night', 'The Watch Night', (
        "In July 1999 Ulysses passes Earth's Roche limit, and years of preparation turn into nights of watching. Wardens open "
        "their posts, ferry and rail crews sleep beside their vehicles, hospital volunteers switch on their generators and "
        "observers report every few minutes to the coast guard office. Schools and halls stand open as assembly points, and the trains wait at the platforms with their doors unlocked.",
        "Radio stations stay on the air all night, reading official bulletins between records. Some families go to their "
        "assigned places early; others sit on rooftops to watch the sky. Rumours travel faster than reports: a fire on the "
        "horizon, a wave sighted off the coast, a ship that has stopped answering. Each one has to be checked before it can be "
        "dismissed or acted upon, and the checking exhausts everyone.",
        "The government's plans now meet the real thing. Ministers must decide whether to keep the whole coast on alert until "
        "the observatories declare the danger past, at great cost to work and nerves, or to stand most districts down after "
        "the first nights, trusting the warning network to call them back if it is needed.",
    ), (
        Option('Keep the coast on alert.', (WarSupport(0.03), Stability(-0.02))),
        Option('Stand most districts down.', (Stability(0.03), WarSupport(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08 in tools/lore/chronicle.json; the Relentian watch is gameplay',
        picture=0),
    EventDef('state_account', 'An Account of the State', (
        "The panel's report on the state of Relentio is published in one volume with a plain cover. It describes what the "
        "government has built since it began governing in its own name: a chamber that meets, a treasury that collects, a "
        "coast guard that sails and ports that handle more cargo than the old books ever recorded. It also lists what has not "
        "been built.",
        "The valley towns still depend on a handful of buyers. Torre Mountain still feels forgotten by the coast. Young "
        "graduates leave for jobs abroad, and too many decisions pass through a few offices and firms. The panel warns that a "
        "small state can be agile or fragile, and that the difference lies in whether its institutions can survive a bad "
        "year without improvising.",
        "The government must decide how to answer. It can accept the report in full and publish a response to each "
        "recommendation, inviting a season of hostile headlines. Or it can thank the panel, highlight its praise and send the "
        "criticisms to committee, where they will move slowly if they move at all. The panel members have already said they will tell the press which course the government took.",
    ), (
        Option('Answer every recommendation.', (Stability(0.03), PP(-20))),
        Option('Highlight the praise.', (PP(30), Stability(-0.02))),
    ), picture=1),
    EventDef('trade_mission', 'A Trade Mission Returns', (
        "The trade mission comes home after a month abroad with a folder of business cards, three signed contracts and a much "
        "longer list of promises. Valley manufacturers found buyers for rugged vehicles and machine parts. The yard firms "
        "found ship operators who want cheaper repairs. The port services sold well everywhere, and the arms halls sold well "
        "in places the foreign ministry would rather not discuss.",
        "Every contract comes with a request. One buyer wants credit from the treasury. Another wants a guarantee that "
        "deliveries will continue whatever happens at Sofern. A third wants an exclusive agency that would shut out other "
        "Relentian firms. The mission leaders insist that small states must say yes more often than large ones; the treasury "
        "notes that small states also go bankrupt faster.",
        "The government must decide how to follow up. It can back the new contracts with state export credit, turning promises "
        "into orders at some risk to the treasury. Or it can leave the firms to finance their own deals, keeping the state's "
        "money safe and accepting that some of the promises will quietly evaporate.",
    ), (
        Option('Back the contracts with export credit.', (PP(-25), TimedIdea('export_orders', 365))),
        Option('Let the firms finance themselves.', (PP(15), Stability(0.01))),
    ), picture=2),
)

# --- branches ------------------------------------------------------------------------------------
GOVERN = Branch('gov', 'The Duchy and Its Chamber', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('gov_chamber_meets', 'The Relentian Chamber Sits',
          "Relentio governs itself with a ducal crown, an office of state and a chamber gathered from the Sofern harbour councils, "
          "the valley towns around Driscol and the Torre Mountain districts. Nobody has yet agreed how those three bodies share "
          "power. Opening the question in public costs the office its quiet, but it gives every faction a seat.",
          ('assembly', 'ballot'), reward=(Idea('chamber_convened'), Event('who_governs'))),
    Focus('gov_powers_list', 'What the Ducal Crown May Do',
          "Clerks list the powers the ducal office actually holds: naming ministers, sealing the budget, commanding the coast guard "
          "and dissolving the chamber. Much of the list was written for a crown land and now answers to no throne beyond its own. "
          "Publishing it spends goodwill and forces a choice between three ways of governing.",
          ('document', 'scales'), after=('gov_chamber_meets',),
          reward=(PP(30), Tooltip('Opens three constitutional paths; only one can be taken.'))),
    Focus('gov_duchy_path', 'A Duchy Bound by Its Chamber',
          "The constitutional camp would keep the ducal crown and make the cabinet answer to the chamber. Ministers would face "
          "questions, budgets would be voted line by line, and the ducal office would sign on advice. It is the most familiar "
          "arrangement for a former crown land, and it costs the office its freedom to act alone.",
          ('ballot', 'document'), after=('gov_powers_list',), exclusive=('gov_seals_path', 'gov_republic_path'),
          reward=(SwapIdea('chamber_convened', 'ducal_charter'),)),
    Focus('gov_seals_path', 'The Seals Stay with the Duchy',
          "Shipowners and senior officials argue that a small state with one great port cannot wait on chamber votes when a "
          "freighter is impounded or a bank wobbles. They want the seals, the budget and the coast guard kept by a council the "
          "ducal office names. Decisions come fast, and the chamber becomes a place to complain.",
          ('command', 'document'), after=('gov_powers_list',), exclusive=('gov_duchy_path', 'gov_republic_path'),
          reward=(SwapIdea('chamber_convened', 'seals_mandate'),)),
    Focus('gov_republic_path', 'Merchants Propose a Republic',
          "The harbour councils of Sofern have long run their own quays, and many of their members see no reason to keep a crown "
          "at all. They propose an elected executive and a Republic of Relentio, with the ducal title retired to the museums. The "
          "ports cheer the idea; the valley towns and the officer corps are far less sure.",
          ('assembly', 'economy'), after=('gov_powers_list',), exclusive=('gov_duchy_path', 'gov_seals_path'),
          reward=(SwapIdea('chamber_convened', 'merchant_mandate'),)),
    Focus('gov_ducal_ministry', 'Form the Ducal Ministry',
          "A cabinet drawn from the chamber majority takes the seals and governs collectively in the name of the ducal crown. The "
          "change runs through an office, not a person, and the ministry answers for every budget it passes. The ducal office "
          "keeps its ceremonies and hands its daily authority to people who must win elections.",
          ('ballot', 'assembly'), after=('gov_duchy_path',), cost=10,
          exclusive=('gov_seals_council', 'gov_harbour_republic'), reward=(Regime('ducal_ministry'), Flag('path_duchy'))),
    Focus('gov_seals_council', 'Name the Council of Seals',
          "The ducal office names a small council to hold the seals, the budget and the coast guard, with elections suspended "
          "while it governs by order. The chamber survives as an advisory body that meets when it is called. The council is quick "
          "and narrow, and every failure from now on will carry its name rather than a minister's.",
          ('command', 'security'), after=('gov_seals_path',), cost=10,
          exclusive=('gov_ducal_ministry', 'gov_harbour_republic'), reward=(Regime('seals_council'), Flag('path_seals'))),
    Focus('gov_harbour_republic', 'Proclaim the Harbour Republic',
          "The chamber votes a republican charter and elects an executive council from its own benches, with elections fixed on a "
          "calendar that no office can move. The ducal crown becomes a coat of arms. Shipowners gain a government that thinks "
          "like them, and the valley towns must now win their arguments by votes.",
          ('assembly', 'scales'), after=('gov_republic_path',), cost=10,
          exclusive=('gov_ducal_ministry', 'gov_seals_council'), reward=(Regime('harbour_republic'), Flag('path_republic'))),
    Focus('gov_question_days', 'Ministers Answer on Fridays',
          "Every Friday the ministers stand in the chamber and take questions from any deputy, broadcast on Sofern radio. Quayside "
          "rumours that once lived for weeks are answered in an afternoon. The ministry looks weaker for a while and the coast "
          "guard dislikes explaining itself in public. Over the years, people come to trust what they hear argued.",
          ('ballot', 'communications'), after=('gov_ducal_ministry',),
          exclusive=('gov_seals_inspectors', 'gov_ports_senate'), reward=(Stability(0.04), WarSupport(-0.01))),
    Focus('gov_seals_inspectors', 'Council Inspectors on the Quays',
          "The council sends its own inspectors to the customs sheds, the yards and the valley payrolls with authority to stop "
          "any contract on the spot. Petty theft drops quickly and so does initiative, because clerks learn to wait for an "
          "inspector before signing anything. The council gains control of the money and loses early warning of bad news.",
          ('security', 'economy'), after=('gov_seals_council',),
          exclusive=('gov_question_days', 'gov_ports_senate'), reward=(PP(45), Stability(-0.02))),
    Focus('gov_ports_senate', 'A Senate of Ports and Valleys',
          "The republic adds a second chamber in which the harbour councils, the valley towns and the Torre Mountain districts sit "
          "as equals, whatever their population. Sofern loses the easy majority it expected, and the valley gains a veto over port "
          "spending. Lawmaking slows, but no single district can capture the republic it helped found.",
          ('assembly', 'navy'), after=('gov_harbour_republic',), requires=(HasFlag('harbour_councils'),),
          exclusive=('gov_question_days', 'gov_seals_inspectors'), reward=(Stability(0.05), PP(-30))),
    Focus('gov_civil_service', 'A Relentian Civil Service',
          "Whatever constitution prevails, the government needs clerks who answer to Relentio rather than to habits from the "
          "crown-land years. A civil service board writes job descriptions, pay grades and a code of conduct for every ministry. "
          "Staffing it pulls able people out of the ports and the valley firms, and their employers complain loudly.",
          ('document', 'civil'), after_any=('gov_ducal_ministry', 'gov_seals_council', 'gov_harbour_republic'),
          reward=(Flag('own_civil_service'), PP(25))),
))

HARBOUR = Branch('harb', 'The Port of Sofern', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('harb_customs_count', 'Weigh the Sofern Customs',
          "Sofern is the largest port Relentio has, and its customs sheds are the first money the treasury can count on. Nobody "
          "has measured exactly what passes the quays, who pays duty and who has a friend at the gate. A full count of cargo and "
          "receipts costs a season of clerical work and a few uncomfortable dinners.",
          ('economy', 'navy'), reward=(Idea('customs_ledger'), Event('sofern_quays'))),
    Focus('harb_councils', 'Charter the Harbour Councils',
          "The merchants and dockers of Sofern already run their quays through harbour councils, as they did in the crown-land "
          "years. Giving those councils a written charter, a budget line and a seat at the customs table buys the loyalty of the "
          "port. The price is that the councils will expect to be asked before every harbour decision.",
          ('assembly', 'navy'), after=('harb_customs_count',), reward=(Flag('harbour_councils'), Stability(0.02))),
    Focus('harb_quay_road', 'Rebuild the Quay Roads',
          "Trucks queue for hours on the narrow roads between the Sofern quays and the main highway, and spoiled cargo is written "
          "off every summer. Widening the approaches and adding rail sidings is unglamorous work that pays back within a few "
          "years. The city suffers a season of closures, and the hauliers complain until the first lane opens.",
          ('logistics', 'bridge'), after=('harb_customs_count',), reward=(Build('infrastructure', 1, 236),)),
    Focus('harb_fraeport', 'Deepen the Fraeport Berths',
          "Fraeport in North Relentio handles coastal freight and fishing boats, but its berths silt up and larger ships anchor "
          "offshore to unload by lighter. Dredging the channel and rebuilding the quay road lets the second port take traffic "
          "Sofern cannot. Sofern merchants grumble about subsidising a rival, and the dredgers must return every few years.",
          ('navy', 'tools'), after=('harb_customs_count',), reward=(Build('infrastructure', 1, 597),)),
    Focus('harb_free_port', 'A Free Port at Sofern',
          "The merchant school wants Sofern declared a free port: low duties, bonded warehouses and foreign firms welcome to trade "
          "through the quays. Cargo volumes would rise quickly and so would rents. The treasury gives up a large share of its "
          "customs income for a busier port, betting that trade will pay in other ways.",
          ('economy', 'diplomacy'), after=('harb_councils',), cost=10, exclusive=('harb_port_authority',),
          reward=(SwapIdea('customs_ledger', 'free_port'), Flag('model_free_port'))),
    Focus('harb_port_authority', 'One Authority for Every Quay',
          "The administrative school wants a single public port authority to own the quays, set the tariffs and plan dredging for "
          "Sofern and Fraeport together. Revenue stays with the state and investment follows a plan. The harbour councils lose "
          "their private arrangements, and some shippers move to ports where nobody asks questions.",
          ('command', 'navy'), after=('harb_councils',), cost=10, exclusive=('harb_free_port',),
          reward=(SwapIdea('customs_ledger', 'port_authority'), Flag('model_authority'))),
    Focus('harb_bonded_sheds', 'Bonded Sheds on the Waterfront',
          "Free-port status means little without warehouses where foreign goods can wait duty-free. A row of bonded sheds and light "
          "workshops rises beside the main quay, built with merchant money on public land. Rents climb across the harbour "
          "district, and residents who lived there for decades start moving inland.",
          ('industry', 'navy'), after=('harb_free_port',), reward=(Build('industrial_complex', 1, 236),)),
    Focus('harb_authority_works', 'Port Workshops at Fraeport',
          "The port authority builds a repair and fabrication district at Fraeport to serve both harbours, financed from the "
          "tariffs it now collects directly. Cranes, engines and refrigeration units are fixed at home instead of abroad. The "
          "workshops are slow to turn a profit, and Sofern deputies ask why their tariffs build someone else's town.",
          ('tools', 'industry'), after=('harb_port_authority',), reward=(Build('industrial_complex', 1, 597),)),
    Focus('harb_pilots', 'Pilots and Tugs for the Channel',
          "Ships entering Sofern rely on harbour pilots and tugs whose boats are older than most of their crews. A new pilot school "
          "and a modest tug fleet cut waiting times and the risk of a grounding that would close the channel for weeks. Pilots "
          "win better pay, and shipowners pay higher fees on every visit.",
          ('navy', 'training'), after=('harb_quay_road',), reward=(XP('navy', 10), Research('naval_equipment', 0.5, 1))),
    Focus('harb_ship_register', 'A Relentian Ship Register',
          "Many ships owned in Sofern still carry papers issued in the crown-land years. A Relentian register records every hull, "
          "owner, crew list and usual route. Owners dislike the paperwork and the fees, and a few reflag abroad. In any crisis, "
          "though, the government will know exactly which ships are its own.",
          ('document', 'logistics'), after=('harb_fraeport',), reward=(Flag('ship_register'), PP(15))),
    Focus('harb_insurance', 'A Marine Insurance Exchange',
          "Sofern shippers buy cover in foreign markets that raise premiums whenever a war starts anywhere near the coast. A local "
          "insurance exchange, backed by a modest state guarantee, keeps some of that money at home and prices risk with local "
          "knowledge. A single bad loss could drain the guarantee, and foreign underwriters will not welcome the rival.",
          ('scales', 'navy'), after_any=('harb_bonded_sheds', 'harb_authority_works'), reward=(Idea('insurance_exchange'),)),
))

TREASURY = Branch('treas', 'A Treasury of Its Own', 1991, 'FOCUS_FILTER_STABILITY', (
    Focus('treas_open_books', 'Open the First Relentian Budget',
          "Relentio has a government but only the outline of a treasury: customs offices, district tax rolls copied from older "
          "files and obligations whose full size nobody has agreed. The first budget must say what the state owns, what it owes "
          "and what it can afford this year. Writing it honestly will frighten the chamber.",
          ('scales', 'document'), reward=(Idea('thin_treasury'), Event('first_budget'))),
    Focus('treas_tax_roll', 'A Tax Roll for Every District',
          "Tax records in the valley and the Torre Mountain districts are old, incomplete and often kept in someone's cupboard. "
          "Assessors visit every farm, workshop and warehouse to build one roll the treasury can trust. Assessment costs salaries "
          "and goodwill, and some families discover they have underpaid for years and must now catch up.",
          ('document', 'civil'), after=('treas_open_books',), reward=(TimedIdea('assessment_year', 365), PP(20))),
    Focus('treas_customs_share', 'Customs as First Revenue',
          "Until the tax roll is finished, harbour duty is almost the only income the treasury can collect on time. Ministers "
          "pledge the first year of customs receipts to salaries and pensions rather than to any new programme. It keeps the state "
          "solvent and the clerks paid, and it makes the treasury hostage to every slow month at the quays.",
          ('economy', 'document'), after=('treas_open_books',), reward=(TimedIdea('customs_windfall', 365),)),
    Focus('treas_sound', 'Balanced Books First',
          "The cautious school wants every budget balanced, every loan published and no new borrowing until the treasury has a "
          "record lenders respect. Public works slow and the valley firms wait for credit. In exchange, Relentio pays little "
          "interest, and nobody abroad doubts that its government means what it signs.",
          ('scales', 'security'), after=('treas_tax_roll',), cost=10, exclusive=('treas_credit',),
          reward=(SwapIdea('thin_treasury', 'sound_books'),)),
    Focus('treas_credit', 'Credit for the Works',
          "The development school wants a state credit bank that lends to the valley halls, the yards and the port workshops at "
          "low rates. Growth comes faster and jobs stay local. The treasury carries the risk of every failed loan, and lenders "
          "will charge a little more each time the chamber raises the borrowing limit.",
          ('economy', 'industry'), after=('treas_tax_roll',), cost=10, exclusive=('treas_sound',),
          reward=(SwapIdea('thin_treasury', 'development_credit'),)),
    Focus('treas_audit_office', 'An Audit Office Above Party',
          "An independent audit office checks every ministry's accounts each year and reports to the chamber rather than to the "
          "government of the day. Its first report embarrasses several departments. Auditors cost little; their real price is "
          "that no government, whatever its politics, can hide its own mistakes for long.",
          ('scales', 'ballot'), after=('treas_sound',),
          reward=(Stability(0.03), Tooltip('Every ministry is audited each year from this point on.'))),
    Focus('treas_harbour_bond', 'A Harbour Bond Issue',
          "The credit bank raises its first money through a bond sold to Sofern savers and foreign buyers, secured on future port "
          "revenue. The proceeds fund a new hall for machine parts in the Relentio valley. Interest will be owed for twenty years, "
          "and the port's income is now promised to bondholders before ministers.",
          ('economy', 'rebuild'), after=('treas_credit',), reward=(Build('industrial_complex', 1, 173),)),
    Focus('treas_savings_banks', 'Savings Banks in the Valley',
          "Valley families keep their savings in cash or in banks headquartered elsewhere. A network of small public savings banks "
          "in Driscol and the valley towns gives them a safe place at home, and lends the deposits to local builders for roads and "
          "houses. The banks need careful supervision and a reserve in case of a run.",
          ('civil', 'economy'), after=('treas_tax_roll',), reward=(Build('infrastructure', 1, 173), Stability(0.02))),
    Focus('treas_statistics', 'A Statistics Office',
          "The government argues about prices, wages and trade with numbers from three sources that never agree. A statistics "
          "office publishes one set of figures every quarter, gathered by its own surveyors. Ministers lose the right to choose "
          "their favourite numbers, and the chamber gains a common basis for every argument that follows.",
          ('document', 'science'), after=('treas_customs_share',), reward=(Research('industry', 0.5, 1), PP(15))),
    Focus('treas_reserve', 'A Reserve for Lean Seasons',
          "Whichever fiscal school prevailed, the treasury sets aside a fund for the year a big shipper fails or the quays go "
          "quiet. It earns little, sits in safe paper and is the first thing every minister wants to spend. If it survives the "
          "budget rounds, the next downturn lands on a cushion rather than on payrolls.",
          ('shelter', 'scales'), after_any=('treas_audit_office', 'treas_harbour_bond'),
          reward=(Flag('treasury_reserve'), PP(-20))),
))

VALLEY = Branch('vall', 'The Valley Arms Halls', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('vall_walk_halls', 'Walk the Valley Arms Halls',
          "Relentio's industry rests on arms halls in the Relentio valley around Driscol and a heavy cluster at Torre Mountain, "
          "built for a larger kingdom's army and now serving a much smaller state. An inspection team walks every line and counts "
          "what runs, what idles and what was never finished. The answer shapes every industrial choice that follows.",
          ('industry', 'document'), reward=(Idea('idle_halls'), Event('valley_halls'))),
    Focus('vall_torre_road', 'The Torre Mountain Haul Road',
          "Ore, steel and finished goods leave Torre Mountain on a winding road that closes with every heavy storm. Rebuilding it "
          "with proper grades, bridges and passing places keeps the halls and mines supplied all year. Engineers spend two seasons "
          "on the slopes, and the mountain towns finally get a reliable route to the coast.",
          ('bridge', 'logistics'), after=('vall_walk_halls',), reward=(Build('infrastructure', 1, 207),)),
    Focus('vall_civil', 'Tractors Instead of Tank Parts',
          "The conversion camp wants the valley halls retooled for tractors, pumps, rail wagons and machine tools that a small "
          "trading state can actually sell. Workers keep their jobs, though output falls for a year while lines are rebuilt. The "
          "army loses capacity it may later regret, and the arms buyers who knew the valley go elsewhere.",
          ('rebuild', 'industry'), after=('vall_walk_halls',), cost=10, exclusive=('vall_export',),
          reward=(SwapIdea('idle_halls', 'civil_lines'),)),
    Focus('vall_export', 'Arms Lines Kept for Export',
          "The export camp says the halls are Relentio's most valuable industrial asset and should keep making shells, rifles and "
          "vehicle parts for licensed foreign buyers. Revenue arrives quickly and the skilled workforce stays together. The state "
          "now depends on other countries' wars, and every contract invites questions about who will use the goods.",
          ('missile', 'economy'), after=('vall_walk_halls',), cost=10, exclusive=('vall_civil',),
          reward=(SwapIdea('idle_halls', 'export_lines'),)),
    Focus('vall_machine_tools', 'Machine Tools from Shell Lines',
          "Lathes and presses from idle shell lines are rebuilt into a machine-tool works at Driscol that supplies the yards, the "
          "port workshops and the farms. It is the first valley plant designed for civilian customers from the start. Retraining "
          "takes a year, and engineers who preferred weapons work leave for jobs abroad.",
          ('tools', 'industry'), after=('vall_civil',), reward=(Build('industrial_complex', 1, 173),)),
    Focus('vall_trucks', 'Valley Trucks for Valley Roads',
          "The converted halls build a simple, rugged truck for farms, quarries and the Torre Mountain haul road. It will never win "
          "a design prize, but parts are cheap and every village mechanic can fix it. Orders from the state and the harbour "
          "councils keep the line open while it learns to sell further afield.",
          ('logistics', 'tools'), after=('vall_civil',),
          reward=(Research('logistics_tech', 0.5, 1), Research('engineers_tech', 0.5, 1))),
    Focus('vall_licences', 'Export Licences and End Users',
          "An export board licenses every sale from the valley lines and checks where each shipment finally goes. The halls near "
          "Driscol add a line to meet the first contracts. The board is only as honest as the people who sit on it, and each "
          "refused buyer is an order a competitor will gladly take.",
          ('diplomacy', 'missile'), after=('vall_export',), reward=(Build('arms_factory', 1, 173),)),
    Focus('vall_proof_range', 'A Proof Range at Torre Mountain',
          "Shells and rockets from Torre Mountain have always been tested at ranges outside Relentio. A proof range on the high "
          "ground lets the halls test their own output and fix faults before foreign inspectors find them. Nearby farms object to "
          "the noise, and the range must be fenced, staffed and insured.",
          ('missile', 'security'), after=('vall_export',), reward=(Research('artillery', 0.5, 1), XP('army', 10))),
    Focus('vall_north_plant', 'An Engine Works at Fraeport',
          "North Relentio has fewer industrial jobs than the valley, and its young workers drift south to Sofern every year. An "
          "engine and pump works at Fraeport gives the north steady employment and the ports a nearby supplier. The first two "
          "years cost far more than they earn while crews learn the trade.",
          ('industry', 'civil'), after=('vall_walk_halls',), reward=(Build('industrial_complex', 1, 597),)),
    Focus('vall_housing', 'Housing for the Valley Shifts',
          "Valley workers commute for hours from villages because the towns near the halls never built enough housing. A housing "
          "programme with new roads and bus routes around Driscol cuts the journey and fills the night shifts. Builders profit, "
          "land prices rise, and older residents say the town they knew is disappearing.",
          ('civil', 'rebuild'), after=('vall_torre_road',), reward=(Build('infrastructure', 1, 173),)),
    Focus('vall_metals', 'Steel and Tungsten Contracts',
          "The tungsten and steel of Faroe and the heavier ore beds of Torre Mountain have mostly left as raw rock. Long contracts "
          "with the valley halls and the yards keep more of that metal at home, at prices fixed for five years. Mine owners give "
          "up the chance of a boom and gain certainty, which their banks reward.",
          ('tools', 'economy'), after_any=('vall_machine_tools', 'vall_trucks', 'vall_licences', 'vall_proof_range'),
          reward=(Research('excavation_tech', 0.5, 1), Flag('valley_settled'))),
))

NEIGHBOURS = Branch('nb', 'Between Gatewood and the Wider World', 1992, 'FOCUS_FILTER_POLITICAL', (
    Focus('nb_envoys', 'Envoys to Gatewood',
          "Perbla is Relentio's nearest neighbour and the state its people know best, from courts and schools to rail timetables "
          "and family ties. The first Relentian envoys to Gatewood must settle practical matters before grand ones: post, "
          "pensions, transit and shared files. How the talks begin will colour every agreement after them.",
          ('diplomacy', 'document'), reward=(Event('gatewood_envoys'), Stability(0.01))),
    Focus('nb_transit', 'Transit Papers with Perbla',
          "Goods from the Relentian quays reach the interior on Perblan rails and roads, and Perblan cargo uses Relentian berths. "
          "A transit agreement sets the paperwork, the fees and the inspection points so that trains do not wait days at a "
          "frontier desk. Both sides give a little, and the hauliers notice the difference within a month.",
          ('rail', 'document'), after=('nb_envoys',), reward=(Build('infrastructure', 1, 597), PP(10))),
    Focus('nb_sister_lands', 'Letters to Serenava and Terentio',
          "Serenava and Terentio were crown lands alongside Relentio, and their towns share courts, customs habits and many family "
          "names with the ports. Whatever their governments now are, Relentio writes to their authorities about trade, students "
          "and pensions. The letters claim nothing and promise little, but they keep old roads of contact open.",
          ('diplomacy', 'assembly'), after=('nb_envoys',),
          reward=(Stability(0.02), Tooltip('No claim, core or border changes; contacts concern trade, students and pensions only.'))),
    Focus('nb_gatewood', 'Close Ties with Gatewood',
          "One camp wants Relentio to stay close to Perbla: shared standards, coordinated tariffs and regular meetings between "
          "ministers. Trade with the interior flows easily and old networks keep working. Critics warn that Relentio risks becoming "
          "a province by contract, and Osean buyers wonder whether Sofern makes its own decisions at all.",
          ('diplomacy', 'rail'), after=('nb_envoys',), cost=10, exclusive=('nb_osea', 'nb_neutral'),
          reward=(Idea('gatewood_ties'), Flag('align_gatewood'))),
    Focus('nb_osea', 'Open the Port to Osean Trade',
          "Another camp looks past Perbla to Osea, a vast market and the biggest customer any port could want. Osean shipping lines "
          "would get favourable berths and Osean firms easy access to the valley halls. Revenue rises fast. Gatewood will read the "
          "choice as a statement, and the valley's old customers will notice.",
          ('economy', 'diplomacy'), after=('nb_envoys',), cost=10, exclusive=('nb_gatewood', 'nb_neutral'),
          reward=(Idea('osean_market'), Flag('align_osea'))),
    Focus('nb_neutral', 'A Harbour for Every Flag',
          "A third camp wants no special friends at all. Relentio would treat every flag alike at its quays, publish one tariff for "
          "everyone and stay out of every bloc. Neutrality suits a small trading state and annoys every large one, and it only "
          "works if the coast guard can enforce the rules the government publishes.",
          ('peace', 'navy'), after=('nb_envoys',), cost=10, exclusive=('nb_gatewood', 'nb_osea'),
          reward=(Idea('open_harbour'), Flag('align_neutral'))),
    Focus('nb_timetables', 'Shared Timetables with Perbla',
          "Relentian and Perblan rail planners agree common timetables, through tickets and shared freight wagons on the line from "
          "Torre Mountain to the interior. Travellers stop changing trains at the frontier and freight clears faster. The "
          "arrangement ties Relentian rail closely to Perbla's network, which pleases hauliers and worries the ports.",
          ('rail', 'logistics'), after=('nb_gatewood',), reward=(Build('infrastructure', 1, 207), Stability(0.01))),
    Focus('nb_osean_agents', 'Osean Shipping Agents at Sofern',
          "Osean shipping lines open agencies on the Sofern waterfront and sign long berth contracts for their freighters. Dock "
          "work becomes steadier and wages rise. Local shipowners lose their best berths to larger foreign fleets, and the harbour "
          "councils argue every month about whether the port still belongs to the people who work in it.",
          ('navy', 'economy'), after=('nb_osea',), reward=(TimedIdea('osean_charters', 540),)),
    Focus('nb_flag_registry', 'Neutral Papers for Foreign Hulls',
          "Foreign shipowners who want neutral papers can register their hulls in Sofern for a fee, under rules on safety and crew "
          "pay that the coast guard actually inspects. The registry earns steady revenue and makes the Relentian flag common on "
          "distant seas. Each badly run ship under that flag becomes Relentio's embarrassment in someone else's port.",
          ('document', 'peace'), after=('nb_neutral',), reward=(TimedIdea('flag_registry', 730),)),
    Focus('nb_trade_fair', 'The Sofern Trade Fair',
          "Whatever partners Relentio chose, its products need buyers who have seen them. A yearly fair on the Sofern waterfront "
          "gathers the valley manufacturers, the yard repair firms and the port services in one hall. Hotels fill for a week, "
          "foreign delegations sign letters of intent, and the government learns which industries actually sell.",
          ('economy', 'assembly'), after_any=('nb_timetables', 'nb_osean_agents', 'nb_flag_registry'),
          reward=(TimedIdea('export_orders', 540),)),
))

DEFENCE = Branch('def', 'Coast Guard and Air Wing', 1993, 'FOCUS_FILTER_NAVY_XP', (
    Focus('def_count', 'Who Guards the Relentian Coast',
          "Relentio's armed forces begin with whatever hulls, aircraft and trained crews are Relentian today: patrol boats at "
          "Sofern, a few aircraft on the city field and reservists who learned their trade in a larger service. A frank count "
          "shows what can sail and fly this month. The answer is modest, and the officers know it.",
          ('navy', 'document'), reward=(Idea('coast_guard'), XP('navy', 10))),
    Focus('def_marines', 'Marine Companies at Sofern',
          "Relentio's marines are few but trained for exactly the jobs a port state needs: securing quays, boarding suspect ships "
          "and landing on its own coast. Gathering them into proper companies with boats and radios at Sofern gives the government "
          "a fast response force. The army complains that marines take its best volunteers.",
          ('training', 'navy'), after=('def_count',), reward=(XP('army', 15), Research('infantry_weapons', 0.5, 1))),
    Focus('def_sofern_field', 'Hangars at the Sofern Field',
          "The airfield outside Sofern was built for a larger air arm and now hosts a handful of aircraft and a great deal of empty "
          "concrete. New hangars, fuel stores and a repaired runway let the small air wing work from one well-kept base. The money "
          "could have built schools, and the teachers' unions say so in the papers.",
          ('runway', 'air'), after=('def_count',), reward=(Build('air_base', 2, 236),)),
    Focus('def_volunteers', 'A Volunteer Defence Force',
          "The volunteer school wants a small, paid professional force: long-service sailors, marines and pilots on career "
          "contracts, with no conscription at all. Units stay together and master their equipment. The force is expensive per "
          "head and could not hold a long war alone, but a port state lives on trade and needs its workers on the quays.",
          ('medal', 'training'), after=('def_count',), cost=10, exclusive=('def_militia',), reward=(Idea('volunteer_force'),)),
    Focus('def_militia', 'Harbour and Valley Militia',
          "The militia school wants every adult who once served to stay on local rolls, training a few weekends a year with the "
          "coast guard or the valley defence companies. Mobilisation would be quick and cheap, and the force could hold its home "
          "districts. Employers dislike losing workers to drills, and the militia's equipment will always be second-hand.",
          ('security', 'civil'), after=('def_count',), cost=10, exclusive=('def_volunteers',), reward=(Idea('harbour_militia'),)),
    Focus('def_patrol_boats', 'Patrol Boats from Sofern Slipways',
          "The Sofern yards can build small patrol boats far faster than they could ever build a warship. A class of fast, lightly "
          "armed boats for fisheries, customs and rescue work replaces the oldest hulls. They are no match for a real navy, but "
          "they make the coast guard visible every day along the coast.",
          ('navy', 'tools'), after=('def_marines',), reward=(XP('navy', 15), Research('naval_equipment', 0.75, 1))),
    Focus('def_coast_radar', 'Radar Posts Above Fraeport',
          "The northern approaches past Fraeport have no radar cover at all, and ships or aircraft can arrive there unannounced. A "
          "radar post on the high ground above the port, linked to the coast guard office, closes the gap. It costs little to "
          "build and much to staff around the clock, every night of the year.",
          ('radar', 'navy'), after=('def_patrol_boats',), reward=(Build('radar_station', 1, 597),)),
    Focus('def_air_wing', 'A Small Interceptor Wing',
          "The air staff concentrates its few modern aircraft in one interceptor wing at the Sofern field, trained to identify and "
          "escort intruders rather than to fight a long war. Pilots fly more hours and the wing becomes credible. Ground attack and "
          "transport work fall to older aircraft, and the army notices how little air support it now has.",
          ('air', 'radar'), after=('def_sofern_field',), reward=(Idea('interceptor_wing'), XP('air', 15))),
    Focus('def_joint_staff', 'One Staff for Sea and Air',
          "Coast guard, marines and air wing have planned separately, each with its own radio net and maps. A joint staff writes "
          "common procedures for searches, boarding operations and air cover. Commanders lose some independence and resent the "
          "new paperwork. In return, a single crisis no longer produces three different answers from three offices.",
          ('command', 'communications'), after_any=('def_volunteers', 'def_militia'),
          reward=(Research('air_doctrine', 0.5, 1), Research('land_doctrine', 0.5, 1))),
    Focus('def_valley_strips', 'Grass Strips Near Driscol',
          "Every aircraft Relentio owns sits at the Sofern field, where one bad morning could end the air wing. Grass strips in the "
          "valley near Driscol, stocked with fuel and spare parts, give the wing other places to land and rearm. They are "
          "uncomfortable, need guards and are hard to supply in winter, but an enemy would have to find them one by one.",
          ('runway', 'security'), after=('def_air_wing',), reward=(Build('air_base', 1, 173),)),
))

WARYEARS = Branch('war', 'The Belkan War at Sea', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('war_news', 'Sofern Hears of the Belkan War',
          "Fighting around Belka from March 1995 changes life at Sofern long before any soldier is seen. Insurers raise premiums "
          "on every lane near the war, freight rates jump and foreign navies ask questions about cargo. Relentio is no party to "
          "the fighting, but its port, its ships and its valley halls are part of the market the war is reshaping.",
          ('communications', 'navy'), requires=(After('1995.3.25'),), reward=(Idea('war_risk_rates'), Event('belkan_war_sea'))),
    Focus('war_quay_watch', 'Night Watch on the Quays',
          "Strangers, smugglers and agents of every side drift into a busy neutral port during a nearby war. The coast guard posts "
          "night watches on the Sofern quays and installs a harbour radar to track every arrival. Watches cost overtime and slow "
          "cargo handling, and they keep the port from becoming a convenient stage for someone else's operations.",
          ('security', 'radar'), after=('war_news',), reward=(Build('radar_station', 1, 236), WarSupport(0.02))),
    Focus('war_berths', 'Reception Berths at Sofern',
          "Ships arriving from the war zone carry people as well as cargo: families, deserters and sailors whose ships will not go "
          "home. Reception berths at Sofern register each arrival, provide food and a bed, and decide where they go next. The "
          "berths cost money and start arguments in the chamber, but without them every arrival becomes a crisis.",
          ('refugees', 'navy'), after=('war_news',), reward=(Flag('refugee_berths'), Stability(-0.02))),
    Focus('war_close_port', 'Close Sofern to War Cargo',
          "The government bars munitions and military stores for any belligerent from the Relentian quays and the Relentian flag. "
          "Inspectors search suspicious holds and turn ships away. Trade falls and some shipowners move their registrations "
          "abroad. Relentio's neutrality becomes visible and believable, which matters more to a small state than a season of "
          "freight income.",
          ('peace', 'security'), after=('war_news',), cost=10, exclusive=('war_carry_all',),
          reward=(SwapIdea('war_risk_rates', 'closed_port'),)),
    Focus('war_carry_all', 'Carry Cargo for Anyone Who Pays',
          "The government lets Relentian ships and quays handle any lawful cargo for any customer, including the armies of "
          "countries at war. Freight rates are the highest in a generation and the valley halls fill export orders. Every side "
          "watches the port, and each shipload that reaches a front makes Relentio's neutrality look more like a business model.",
          ('logistics', 'economy'), after=('war_news',), cost=10, exclusive=('war_close_port',),
          reward=(SwapIdea('war_risk_rates', 'wartime_freight'),)),
    Focus('war_waldreich_winds', 'Wind Reports After Waldreich',
          "News that nuclear weapons were used in the Waldreich Mountains reaches Sofern by radio, and the first question in every "
          "kitchen is which way the wind blows. The observers and the coast guard publish daily wind and rain readings, and food "
          "inspectors test milk, fish and water. The readings will decide whether fear or facts set the public mood.",
          ('medical', 'telescope'), after=('war_news',), requires=(HasGlobal('belka_dropped_nukes'),),
          reward=(TimedIdea('fallout_watch', 365), Stability(-0.01))),
    Focus('war_contraband', 'Search the Holds',
          "The ship register tells inspectors which hulls are Relentian, who owns them and where they usually sail. Customs officers "
          "and marines board suspect freighters at the harbour mouth and check manifests against cargo. Owners complain about "
          "delays and some captains lie anyway, but each search tells the warring powers that Relentio watches its own ships.",
          ('security', 'navy'), after=('war_quay_watch',), requires=(HasFlag('ship_register'),),
          reward=(XP('navy', 15), Tooltip('Relentian ships are searched under the register; foreign ships only with cause.'))),
    Focus('war_gatewood_lanes', 'Shared Convoy Schedules',
          "Relentian and Perblan shipping offices exchange sailing schedules, weather reports and warnings during the war, so that "
          "freighters from both countries avoid the same dangers. No warship changes flag and no convoy is placed under foreign "
          "command. The exchange saves ships and money, and critics in the chamber call it alignment by timetable.",
          ('communications', 'rail'), after_any=('war_close_port', 'war_carry_all'), requires=(HasFlag('align_gatewood'),),
          exclusive=('war_osean_charters', 'war_neutral_colours'), reward=(TimedIdea('shared_schedules', 365),)),
    Focus('war_osean_charters', 'Osean Charters Through the War',
          "Osean shipping lines, already at home in Sofern, charter Relentian freighters to carry civilian goods while their own "
          "hulls serve the war. Rates are generous and crews earn bonuses. Belkan sympathisers in the valley protest, and insurers "
          "treat every Relentian ship as half Osean. The money is real, and so is the risk to the crews.",
          ('logistics', 'diplomacy'), after_any=('war_close_port', 'war_carry_all'), requires=(HasFlag('align_osea'),),
          exclusive=('war_gatewood_lanes', 'war_neutral_colours'), reward=(TimedIdea('war_charters', 365),)),
    Focus('war_neutral_colours', 'Paint the Neutral Colours Large',
          "Every Relentian ship at sea paints its name, flag and neutral markings large on both sides of the hull and lights them "
          "at night. Captains report their positions to every side on open channels. It is an old practice that works only when "
          "everyone believes it, and the coast guard must punish any ship that abuses the markings.",
          ('peace', 'communications'), after_any=('war_close_port', 'war_carry_all'), requires=(HasFlag('align_neutral'),),
          exclusive=('war_gatewood_lanes', 'war_osean_charters'), reward=(TimedIdea('neutral_markings', 365),)),
    Focus('war_new_tenants', 'From Berths to Tenancies',
          "Families who came through the wartime reception berths still sleep in harbour sheds while their papers are processed. A "
          "placement office matches each household with a job on the North Relentio fishing boats or in coastal firms short of "
          "hands, and with rented rooms nearby. Within a year the arrivals pay taxes; the quarrel over their first rents lasts longer.",
          ('shelter', 'refugees'), after=('war_berths',), requires=(HasFlag('refugee_berths'),),
          reward=(TimedIdea('new_tenants', 730),)),
    Focus('war_stand_down', 'Stand the Quays Down',
          "Once the fighting no longer threatens the shipping lanes, the coast guard returns to peacetime rotations, inspectors go "
          "back to ordinary customs work and the special wartime rules lapse. Standing down too early invites trouble; too late "
          "keeps freight expensive and the chamber restless. The government chooses a date, publishes it and keeps it.",
          ('peace', 'document'), after_any=('war_close_port', 'war_carry_all'), requires=(After('1995.6.20'),),
          reward=(RemoveIdea('closed_port'), RemoveIdea('wartime_freight'), Stability(0.03))),
    Focus('war_belka_beaten', 'Trade After the Belkan Defeat',
          "With Belka defeated, the lanes near the war reopen to ordinary commerce and insurers slowly lower their rates. Rebuilding "
          "across the region needs ships, quays and machinery, and Sofern bids for the work alongside larger harbours. The valley "
          "halls lose their wartime orders, and the government must find them peacetime customers quickly.",
          ('rebuild', 'navy'), after=('war_stand_down',), requires=(HasGlobal('belka_lost_belkan_war'),),
          exclusive=('war_belka_prevails',), reward=(TimedIdea('reconstruction_freight', 540),)),
    Focus('war_belka_prevails', 'Trade With a Victorious Belka',
          "Belka comes out of its war the victor, and the pattern of trade around it shifts accordingly. Belkan buyers return to the "
          "market for steel, trucks and port services, while Osean lines grow cautious about every harbour that serves them. "
          "Relentio must decide how much Belkan business it wants and how loudly to say so.",
          ('diplomacy', 'industry'), after=('war_stand_down',), requires=(HasGlobal('belka_won_belkan_war'),),
          exclusive=('war_belka_beaten',), reward=(TimedIdea('belkan_buyers', 540),)),
))

SKY = Branch('sky', 'Ulysses Over the Coast', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_warning', 'The Ulysses Warning Reaches Sofern',
          "The December 1994 notice about the asteroid Ulysses was a matter for astronomers. The April 1996 announcement that it "
          "will strike the Earth is a matter for every government, though nobody can yet say where its fragments will land. "
          "Relentio, whose people mostly live along the coast, must plan for a danger it cannot place on a map.",
          ('meteor', 'telescope'), requires=(After('1996.4.20'),), reward=(Idea('sky_watch'), Event('ulysses_coast'))),
    Focus('sky_observatory', 'An Observatory on Torre Mountain',
          "Torre Mountain's height makes it the natural place in Relentio to watch the sky. An observatory and a tracking radar "
          "on the heights, linked to the coast guard office, give the state its own eyes on Ulysses rather than foreign bulletins "
          "alone. Astronomers and radar engineers now share one hilltop and one tight budget.",
          ('telescope', 'radar'), after=('sky_warning',), reward=(Build('radar_station', 1, 207),)),
    Focus('sky_tide_tables', 'Flood and Tide Tables',
          "Engineers warn that a fragment falling at sea could raise waves along the whole coast. Surveyors map which streets of "
          "Sofern, Fraeport and the low coastal districts would flood, and publish tide and evacuation tables for each one. The "
          "maps lower property values in the lowest streets, and their owners demand compensation.",
          ('document', 'navy'), after=('sky_warning',), reward=(Research('construction_tech', 0.5, 1), Stability(-0.01))),
    Focus('sky_hospitals', 'Field Hospitals in the Hills',
          "Whatever happens, injured people will need beds far from the coast. Field hospitals are prepared in schools and halls in "
          "the Torre Mountain districts, with stored equipment and volunteer staff trained twice a year. Doctors in Sofern grumble "
          "about the drills and the equipment ages in storage, but no city will depend on a single hospital.",
          ('medical', 'civil'), after=('sky_warning',), reward=(TimedIdea('hospital_reserve', 1095),)),
    Focus('sky_cellars', 'Shelters Under Sofern and Driscol',
          "The engineering school wants deep shelters under the two largest cities, stocked with water, power and food for weeks. "
          "Construction diverts steel and crews from the yards and the valley halls for years. Should fragments fall nearby, "
          "hundreds of thousands have a place to go; should they miss, the cost will be argued over for decades.",
          ('shelter', 'civil'), after=('sky_tide_tables',), cost=10, exclusive=('sky_evacuation',), reward=(Idea('deep_cellars'),)),
    Focus('sky_evacuation', 'Evacuation by Sea and Rail',
          "The planning school would rather buy hours of warning than tons of concrete. Ferries, trains and trucks would move the "
          "coastal districts inland on a timetable rehearsed every year. It is cheaper than shelters and depends on notice, "
          "disciplined crowds and roads that stay open when everyone uses them at once.",
          ('logistics', 'rail'), after=('sky_tide_tables',), cost=10, exclusive=('sky_cellars',),
          reward=(Idea('evacuation_drill'),)),
    Focus('sky_cellar_stores', 'Stock the Cellars',
          "Shelters without supplies are only holes. Water tanks, generators, bunks and tinned food go into every completed cellar, "
          "with wardens trained to open them in minutes and to manage the crowds inside. Stocks spoil and must be rotated each year, "
          "which keeps a small army of clerks busy and the food wholesalers very happy.",
          ('shelter', 'tools'), after=('sky_cellars',), reward=(Research('engineers_tech', 0.5, 1), Stability(0.02))),
    Focus('sky_ferries', 'Ferries on Standby at Fraeport',
          "The evacuation plan depends on ships, and Fraeport becomes the staging port for ferries kept on standby. The quay road is "
          "rebuilt to carry columns of buses and the berths are marked for loading in darkness. Shipowners are paid to keep hulls "
          "nearby instead of earning abroad, which they accept with visible reluctance.",
          ('navy', 'logistics'), after=('sky_evacuation',), reward=(Build('infrastructure', 1, 597), XP('navy', 10))),
    Focus('sky_roche', 'Ulysses Crosses the Roche Limit',
          "In July 1999 Ulysses passes the distance at which Earth's gravity begins to tear it apart, and the waiting turns into "
          "watching. Every warden, crew and hospital volunteer goes to their post while observers track what the sky will do. "
          "Whatever falls or does not fall near Relentio, the country will judge its leaders by the next weeks.",
          ('meteor', 'shelter'), after_any=('sky_cellar_stores', 'sky_ferries'), requires=(After('1999.7.8'),),
          reward=(Event('sky_watch_night'),)),
    Focus('sky_lessons', 'Lessons from the Watch',
          "When the danger has passed, the government asks wardens, doctors, crews and observers what worked and what failed. The "
          "answers are frank: some plans worked as written, others failed on details nobody expected. The report goes to every "
          "district council, and the plans are rewritten for the next emergency, whatever form it takes.",
          ('document', 'peace'), after=('sky_roche',), reward=(RemoveIdea('sky_watch'), Stability(0.03))),
))

CENTURY = Branch('cent', 'Relentio at the New Century', 2002, 'FOCUS_FILTER_POLITICAL', (
    Focus('cent_review', 'Relentio Takes Stock',
          "After years of building institutions, ports and plans, the government commissions a public account of what Relentio has "
          "become: who governs, what the treasury holds, which industries sell and which only survive. A panel drawn from the "
          "chamber, the councils and the universities writes it, and its findings will frame the arguments of the new century.",
          ('document', 'assembly'), reward=(Event('state_account'),)),
    Focus('cent_duchy', 'A Ducal Constitution in One Text',
          "The ducal ministry drafts a single constitution setting out what the ducal office may sign, what the chamber must "
          "approve and which rights no government may suspend. A constitutional court is created to read it. Every clause is "
          "fought over for two sessions, and the result is a duchy whose rules any citizen can look up.",
          ('scales', 'document'), after=('cent_review',), requires=(HasFlag('path_duchy'),),
          exclusive=('cent_seals', 'cent_republic'), reward=(SwapIdea('ducal_charter', 'ducal_constitution'),)),
    Focus('cent_seals', 'The Council Publishes Its Code',
          "The council of seals publishes a standing code listing which powers it holds, which it delegates to ministries and which "
          "questions the chamber may still debate. Investors welcome the predictability and diplomats finally know whom to call. "
          "Critics reply that a decree printed in a book is still a decree.",
          ('command', 'scales'), after=('cent_review',), requires=(HasFlag('path_seals'),),
          exclusive=('cent_duchy', 'cent_republic'), reward=(SwapIdea('seals_mandate', 'seals_code'),)),
    Focus('cent_republic', 'The Republic Writes Its Rights',
          "The harbour republic adds a bill of rights to its charter, protecting the press, the unions, the shipowners and the "
          "valley towns from any single majority. Courts gain the power to strike down laws that breach it. Passing it takes a long "
          "session and several compromises. It is the republic's answer to those who called it a merchants' club.",
          ('scales', 'assembly'), after=('cent_review',), requires=(HasFlag('path_republic'),),
          exclusive=('cent_duchy', 'cent_seals'), reward=(SwapIdea('merchant_mandate', 'republic_rights'),)),
    Focus('cent_civil_exam', 'Open Examinations for Every Post',
          "The civil service board replaces recommendations and family connections with one open examination for every post in the "
          "ministries. Graduates from Driscol, Fraeport and Torre Mountain compete on equal terms with those from Sofern. The first "
          "intake takes years to reach senior posts, and the patrons of the old system complain about standards.",
          ('training', 'document'), after=('cent_review',), requires=(HasFlag('own_civil_service'),),
          reward=(Stability(0.02), PP(30), Tooltip('Every ministry post is filled by open examination from now on.'))),
    Focus('cent_free_port_age', 'The Free Port Comes of Age',
          "Years of free-port rules have filled the bonded sheds and brought foreign firms to the Sofern waterfront. The chamber now "
          "asks whether low duties still pay for themselves. It keeps the free port but adds a modest levy on transit cargo for "
          "dredging and quay repairs. Shippers grumble and stay, because nowhere nearby offers better terms.",
          ('economy', 'tools'), after=('cent_review',), requires=(HasFlag('model_free_port'),),
          exclusive=('cent_authority_plan',), reward=(TimedIdea('transit_levy', 730),)),
    Focus('cent_authority_plan', 'A Twenty Year Port Plan',
          "The port authority publishes a twenty-year plan for both harbours: deeper channels at Fraeport, new cranes at Sofern and "
          "rail sidings linking them to the valley. Every project is costed and scheduled, and the authority borrows against its "
          "tariffs to begin. Shipowners welcome the certainty; deputies wonder whether anyone should plan so far ahead.",
          ('document', 'navy'), after=('cent_review',), requires=(HasFlag('model_authority'),),
          exclusive=('cent_free_port_age',), reward=(TimedIdea('port_plan', 730),)),
    Focus('cent_reserve_use', 'Draw Carefully on the Reserve',
          "The reserve fund has grown untouched through several budget rounds. Its trustees release part of it to modernise the "
          "oldest works in the Faroe district, where breakdowns now cost more than repairs, and keep the remainder invested. Each "
          "party argues it had a better use for the money, and the trustees answer that a reserve spent on everything protects nothing.",
          ('economy', 'shelter'), after=('cent_review',), requires=(HasFlag('treasury_reserve'),),
          reward=(Build('industrial_complex', 1, 173), PP(15))),
    Focus('cent_valley_review', 'The Valley Model Reviewed',
          "Years after the valley chose its industrial path, the ministry of industry walks the halls again, this time counting "
          "exports, wages and the number of firms that depend on a single buyer. The review funds new laboratories at Driscol for "
          "whatever the valley now makes best, and every hall manager lobbies to be counted a success.",
          ('science', 'industry'), after=('cent_review',), requires=(HasFlag('valley_settled'),),
          reward=(Research('industry', 0.5, 1), Research('electronics', 0.5, 1))),
    Focus('cent_usean_war', 'War on the Usean Lanes',
          "War in Usea, where Erusea and the coalition formed against it in August 2003 fight over the continent, sends shipping "
          "insurers into another panic. Usean cargo routes close or turn dangerous, and freight looks for other ports. Relentio is "
          "far from the fighting, but its shipowners, insurers and exporters feel it in every contract they sign.",
          ('navy', 'diplomacy'), after=('cent_review',), requires=(After('2003.8.22'),),
          reward=(TimedIdea('usean_war_rates', 540),)),
    Focus('cent_new_account', 'Relentio in Two Thousand Five',
          "At the close of the period the government publishes a plain account of where Relentio stands: its constitution, its "
          "ports, its treasury and its relations with every neighbour. The account is a baseline for whoever governs next. It makes "
          "no promises about later years; the state has learned that plans rarely survive their first surprise.",
          ('assembly', 'peace'), after_any=('cent_duchy', 'cent_seals', 'cent_republic', 'cent_usean_war'),
          requires=(After('2005.1.1'),),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2005 programme; later eras are not yet written.'))),
))

BRANCHES = (GOVERN, HARBOUR, TREASURY, VALLEY, NEIGHBOURS, DEFENCE, WARYEARS, SKY, CENTURY)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('night_shifts', 'Night Shifts on the Sofern Quays',
                'Pay for floodlights and double crews so the cranes work through the night for half a year.',
                cost=40, effects=(TimedIdea('night_shifts', 180),), requires=(Completed('harb_customs_count'),), cooldown=365),
    DecisionDef('customs_amnesty', 'A Customs Amnesty',
                'Forgive old unpaid duty for traders who register their stock and pay in full from now on.',
                cost=50, effects=(Stability(0.02), TimedIdea('customs_windfall', 180)), requires=(Completed('treas_open_books'),)),
    DecisionDef('trade_mission', 'Send a Trade Mission Abroad',
                'Send officials and firms abroad for a month to find buyers for Relentian goods and services.',
                cost=60, effects=(Event('trade_mission'),), requires=(Completed('nb_envoys'),), cooldown=730),
    DecisionDef('valley_overtime', 'Overtime in the Valley Halls',
                'Fund extra shifts in the valley halls for half a year, at some cost to tempers on the shop floor.',
                cost=50, effects=(TimedIdea('valley_overtime', 180),), requires=(Completed('vall_walk_halls'),), cooldown=365),
    DecisionDef('shelter_drill', 'A Coastwide Shelter Drill',
                'Sound the sirens and walk every district to its assigned shelter or assembly point.',
                cost=25, effects=(WarSupport(0.02), Stability(0.01)), requires=(Completed('sky_warning'),), cooldown=180),
    DecisionDef('coast_exercise', 'A Joint Coast Exercise',
                'Put the coast guard, marines and air wing through a week of searches, boardings and intercepts.',
                cost=35, effects=(XP('navy', 15), XP('air', 10)), requires=(Completed('def_count'),), cooldown=365),
    DecisionDef('second_radar', 'Buy a Second Coastal Radar Set',
                'Buy one more radar set for the Relentio valley coast, once, from whichever supplier offers the best terms.',
                cost=75, effects=(Build('radar_station', 1, 173),), requires=(Completed('def_coast_radar'),)),
)
