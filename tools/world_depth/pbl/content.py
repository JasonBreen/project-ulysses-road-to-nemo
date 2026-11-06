"""Perbla (PBL): bespoke national focus tree, 1991 to 2020.

Source layers. Mod provenance: the inherited history file, ideas, the
perbla_intervention events and the perblan_totalitarianism sub-ideology.
Official: a handful of ACES Chronicle rows used only as date anchors for regional
pressure. Everything else, including every Perblan choice, office, idea, building
and event, is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='PBL', name='Perbla', root='world', package='pbl',
                  themes=('command', 'industry', 'communications'), max_columns=35)

SOURCES = (
    Source('Mod provenance',
           'Inherited Perbla state: monarchism ruling at 70 percent popularity with a constitutional_monarchy leader; ideas '
           'PBL_mandatory_service, PBL_eco_crisis_1, PBL_south_belka_munitions, PBL_federal_kingdom and PBL_electronics. '
           'The tree builds on these ideas and never removes or edits them.',
           'mod/2985041246/history/countries/PBL - Perbla.txt; mod/2985041246/localisation/english/country_PBL_l_english.yml'),
    Source('Mod provenance',
           'The inherited intervention path: perbla_intervention.1 to .3, fired by a Belkan decision only when PBL holds '
           'pbl_help_belka_flag (a 1 percent roll at game start), plus the historical_friends (BLK) and historical_enemies (OSE) '
           'opinion modifiers. The 1995 branch debates the old alliance but commits no forces and never sets that flag.',
           'mod/2985041246/events/Perbla.txt; mod/2985041246/common/on_actions/ac_on_actions.txt; '
           'mod/2985041246/common/decisions/BLK_decisions.txt'),
    Source('Mod provenance',
           'perblan_totalitarianism is an archive monarchism sub-ideology (can_be_randomly_selected = no); used only for the '
           'unnamed Crown Directorate of Order office.',
           'mod/2985041246/common/ideologies/00_ideologies.txt; mod/2985041246/localisation/english/replace/pu_parties_l_english.yml'),
    Source('Mod provenance',
           'Geography: 1991 states 112, 173, 207, 209, 236, 389 (capital), 571, 581, 592, 597 and 601; crown-land cores REL '
           '(173, 207, 236, 597), TER (209, 571) and SER (581); DAK claims on 209 and 571; land neighbours OSE (via 581), DAK '
           'and ARK, computed from map/provinces.bmp. Place names come from existing state and victory point localisation.',
           'mod/2985041246/history/states; mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml'),
    Source('Official',
           'Date anchors for regional pressure only: the Belkan War breaks out (1995 / 03.25); the Ulysses warnings '
           '(1994 / 12.10 and 1996 / 04.20); the Circum-Pacific War begins (2010 / 09.27); drone strikes on four Osean naval '
           'ports as the Lighthouse War begins (2019 / 05.15); satellites destroyed and Usean network communications cut '
           '(2019 / 09.19). No Perblan role in any of them is claimed.',
           'docs/research/CHRONICLE_INDEX.md rows 1995 / 03.25, 1994 / 12.10, 1996 / 04.20, 2010 / 09.27, 2019 / 05.15, '
           '2019 / 09.19; https://acecombat.jp/en/chronicle/'),
    Source('Provisional gameplay',
           'All Perblan focuses, ideas, offices, buildings, flags and events in this spec. No named people; offices are '
           'collective and unnamed; no border, core, war, annexation or faction effects.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # political order
    IdeaDef('court_in_session', 'Court in Session', 'The crown has put the government itself on the order paper; every faction is listening.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('command', 'assembly')),
    IdeaDef('ministry_charter', 'The Ministry Charter', 'Ministers answer to the elected chamber and the crown signs on their advice.',
            {'stability_factor': 0.05, 'political_power_factor': 0.05}, ('ballot', 'document')),
    IdeaDef('privy_seal', 'The Privy Seal', 'The great seals sit with a privy council chosen by the throne.',
            {'political_power_gain': 0.20, 'stability_factor': -0.03}, ('command', 'document')),
    IdeaDef('order_decrees', 'Decrees of Order', 'Government by decree under the hardline creed of Perblan Totalitarianism.',
            {'stability_factor': 0.08, 'war_support_factor': 0.05, 'consumer_goods_factor': 0.05}, ('security', 'command')),
    IdeaDef('assembly_mandate', 'The Assembly Mandate', 'The elected assembly governs in its own name; the crown reigns but does not rule.',
            {'stability_factor': 0.04, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('assembly', 'ballot')),
    IdeaDef('settled_constitution', 'A Settled Constitution', 'One written constitution and a court to read it.',
            {'stability_factor': 0.08, 'political_power_factor': 0.08, 'research_speed_factor': 0.02}, ('scales', 'document')),
    IdeaDef('crown_prerogative', 'The Written Prerogative', 'The throne knows exactly what it may do, and does it.',
            {'political_power_gain': 0.25, 'war_support_factor': 0.04}, ('command', 'medal')),
    IdeaDef('ordered_kingdom', 'The Ordered Kingdom', 'A permanent code of public order replaces emergency decrees.',
            {'stability_factor': 0.10, 'war_support_factor': 0.08, 'consumer_goods_factor': 0.03}, ('security', 'medal')),
    IdeaDef('federal_parliament', 'The Federal Parliament', 'Two chambers, one for the people and one for the four crown lands.',
            {'stability_factor': 0.06, 'research_speed_factor': 0.04, 'production_factory_efficiency_gain_factor': 0.04}, ('assembly', 'scales')),
    # crown lands
    IdeaDef('crown_lands_compact', 'Compact of the Crown Lands', 'A census-backed compact among Perbla, Serenava, Terentio and Relentio.',
            {'stability_factor': 0.02, 'production_speed_infrastructure_factor': 0.10}, ('assembly', 'rail')),
    IdeaDef('land_charters', 'Charters of the Four Lands', 'Each crown land keeps its own budget, courts and diet.',
            {'stability_factor': 0.05, 'production_speed_infrastructure_factor': 0.15}, ('document', 'civil')),
    IdeaDef('single_chancery', 'The Single Chancery', 'One chancery at Gatewood governs every crown land by one code.',
            {'political_power_gain': 0.10, 'production_speed_buildings_factor': 0.05}, ('command', 'rail')),
    # heavy industry
    IdeaDef('arms_ledger', 'The Arms Ledger', 'Every arms plant has been audited; the waste is now on paper.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.05}, ('industry', 'document')),
    IdeaDef('plowshare_works', 'Plowshare Works', 'Arms halls retooled for trucks, pumps and household goods under protection.',
            {'production_speed_industrial_complex_factor': 0.10, 'consumer_goods_factor': -0.03}, ('rebuild', 'industry')),
    IdeaDef('southern_arsenal', 'The Southern Arsenal', 'Arms lines kept at full rate for licensed export.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.05}, ('missile', 'economy')),
    IdeaDef('circuit_economy', 'The Circuit Economy', 'Electronics and components set the pace for all industry.',
            {'research_speed_factor': 0.04, 'production_factory_max_efficiency_factor': 0.04}, ('communications', 'industry')),
    IdeaDef('consumer_drive', 'Shops Before Shells', 'Excise relief on household goods made in converted plants.',
            {'consumer_goods_factor': -0.05, 'stability_factor': 0.03}, ('economy', 'civil')),
    IdeaDef('civil_works_board', 'The Civil Works Board', 'Converted industry competes on its own merits with export credit.',
            {'production_speed_industrial_complex_factor': 0.15, 'consumer_goods_factor': -0.05}, ('rebuild', 'economy')),
    IdeaDef('arsenal_contracts', 'Long Arsenal Contracts', 'Arms exports sold as decades-long service contracts.',
            {'production_speed_arms_factory_factor': 0.15, 'industrial_capacity_factory': 0.08}, ('missile', 'document')),
    IdeaDef('circuit_exports', 'Circuits Abroad', 'Gatewood components sell in foreign markets.',
            {'research_speed_factor': 0.06, 'production_factory_max_efficiency_factor': 0.06}, ('communications', 'diplomacy')),
    IdeaDef('public_accounts', 'Public Accounts', 'Every large crown contract is published with its price and supplier.',
            {'political_power_factor': 0.05, 'production_factory_efficiency_gain_factor': 0.03}, ('scales', 'document')),
    # electronics
    IdeaDef('gatewood_labs', 'Gatewood Public Laboratories', 'Public research outside the national firm.',
            {'research_speed_factor': 0.03}, ('science', 'telescope')),
    IdeaDef('gatewood_institute', 'The Gatewood Institute', 'A technical institute training engineers for every firm.',
            {'research_speed_factor': 0.05, 'air_detection': 0.05}, ('science', 'document')),
    IdeaDef('crown_stake', 'A Crown Stake', 'The treasury holds a minority stake and a veto in the national electronics firm.',
            {'production_factory_efficiency_gain_factor': 0.04, 'political_power_gain': -0.05}, ('economy', 'command')),
    IdeaDef('open_components', 'Open Component Tenders', 'Defence component contracts open to every qualified supplier.',
            {'research_speed_factor': 0.02, 'consumer_goods_factor': -0.02}, ('economy', 'diplomacy')),
    # service year
    IdeaDef('service_year_reformed', 'The Reformed Service Year', 'Universal service kept, with shorter drill and more field training.',
            {'training_time_army_factor': -0.10, 'army_org_factor': 0.03}, ('training', 'security')),
    IdeaDef('reserve_rolls', 'Rolls of the Reserve', 'A single register of every trained adult.',
            {'training_time_army_factor': -0.15, 'army_core_defence_factor': 0.08}, ('document', 'security')),
    IdeaDef('volunteer_cadres', 'Volunteer Cadres', 'A professional core of volunteers over a shortened universal year.',
            {'army_org_factor': 0.05, 'experience_gain_army_factor': 0.08}, ('medal', 'training')),
    IdeaDef('professional_corps', 'The Professional Corps', 'Long-service volunteers on career pay.',
            {'army_org_factor': 0.08, 'experience_gain_army_factor': 0.12, 'army_attack_factor': 0.04}, ('medal', 'command')),
    IdeaDef('civil_service_year', 'A Civil Service Year', 'Conscripts may serve in civil brigades instead of the army.',
            {'production_speed_infrastructure_factor': 0.10, 'stability_factor': 0.03}, ('civil', 'tools')),
    IdeaDef('civil_brigades', 'Civil Brigades', 'Conscript brigades building roads and water lines in the crown lands.',
            {'production_speed_infrastructure_factor': 0.15, 'stability_factor': 0.05}, ('civil', 'rebuild')),
    # the Belkan War years
    IdeaDef('border_watch', 'Watch on the Frontiers', 'Frontier commands on alert while war burns around Belka.',
            {'army_core_defence_factor': 0.05, 'war_support_factor': 0.03}, ('security', 'communications')),
    IdeaDef('old_friendship', 'Faith with Old Friends', 'Public sympathy for Belka; no troops committed.',
            {'production_speed_arms_factory_factor': 0.05, 'war_support_factor': 0.05}, ('diplomacy', 'medal')),
    IdeaDef('armed_neutrality', 'Armed Neutrality', 'No arms to either side and full readiness on every frontier.',
            {'army_core_defence_factor': 0.10, 'stability_factor': 0.03}, ('security', 'peace')),
    IdeaDef('osean_channel', 'A Channel to Osea', 'A discreet promise that Perbla will not serve the war against Osea.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.04}, ('diplomacy', 'communications')),
    IdeaDef('osean_trade', 'Open Frontier Trade', 'The wartime channel to Osea became a trade and transit agreement.',
            {'consumer_goods_factor': -0.05, 'stability_factor': 0.05}, ('diplomacy', 'logistics')),
    IdeaDef('belkan_ties', 'Belkan Ties', 'Credit, contracts and student places for Belkan friends after the war.',
            {'production_speed_arms_factory_factor': 0.08, 'research_speed_factor': 0.02}, ('diplomacy', 'rebuild')),
    IdeaDef('neutral_standing', 'Neutral Standing', 'Perbla as a neutral venue for talks, banking and shipping.',
            {'army_core_defence_factor': 0.08, 'political_power_gain': 0.10}, ('peace', 'scales')),
    # air and sea
    IdeaDef('serenava_wing', 'The Serenava Air Wing', 'A small air arm concentrated on the Serenava fields.',
            {'experience_gain_air_factor': 0.05}, ('air', 'runway')),
    IdeaDef('interceptor_arm', 'Interceptor Air Arm', 'An air arm built to deny Perblan skies.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05}, ('air', 'radar')),
    IdeaDef('strike_arm', 'Strike Air Arm', 'An air arm built to support the army.',
            {'air_mission_efficiency': 0.08, 'experience_gain_air_factor': 0.08}, ('air', 'missile')),
    IdeaDef('air_day', 'The Air Review Year', 'Morale and recruiting after the crown air review.',
            {'war_support_factor': 0.05, 'experience_gain_air_factor': 0.05}, ('medal', 'air')),
    IdeaDef('sofern_squadron', 'The Sofern Squadron', 'Sofern yards keep the coastal squadron at sea.',
            {'navy_org_factor': 0.04}, ('navy', 'tools')),
    IdeaDef('submarine_screen', 'The Submarine Screen', 'Coastal submarines guard every approach.',
            {'naval_coordination': 0.05, 'navy_org_factor': 0.06}, ('submarine', 'navy')),
    IdeaDef('escort_flotillas', 'Escort Flotillas', 'Surface escorts organised around the convoy lanes.',
            {'naval_speed_factor': 0.05, 'navy_org_factor': 0.06}, ('navy', 'logistics')),
    # aftermath
    IdeaDef('relief_offices', 'Relief Offices', 'One office in each crown land for housing, jobs and grants.',
            {'stability_factor': 0.05}, ('refugees', 'civil')),
    IdeaDef('deep_shelters', 'Deep Shelters', 'Shelters under the large cities, stocked for weeks.',
            {'static_anti_air_damage_factor': 0.10, 'stability_factor': 0.03}, ('shelter', 'civil')),
    IdeaDef('early_warning', 'Early Warning Network', 'Observatory links, radar posts and sirens in every district.',
            {'air_detection': 0.10, 'air_defence_factor': 0.05}, ('telescope', 'radar')),
    # desert
    IdeaDef('terentio_crown_oil', 'Crown Oil of Terentio', 'A state company holds every Terentio lease.',
            {'production_speed_buildings_factor': 0.05, 'political_power_gain': 0.05}, ('economy', 'command')),
    IdeaDef('terentio_concessions', 'Terentio Concessions', 'Private drillers work the desert for royalties.',
            {'production_speed_industrial_complex_factor': 0.08, 'stability_factor': -0.02}, ('economy', 'tools')),
    # 2010 to 2020
    IdeaDef('harbour_guard', 'Harbour Guard', 'Naval police and harbour defences on alert while a neighbour is at war.',
            {'static_anti_air_damage_factor': 0.10, 'naval_coordination': 0.05}, ('security', 'navy')),
    IdeaDef('wartime_orders', 'Wartime Orders', 'Osean wartime orders fill Perblan factories.',
            {'industrial_capacity_factory': 0.05, 'stability_factor': -0.02}, ('industry', 'diplomacy')),
    IdeaDef('pacific_distance', 'Distance from the War', 'No military sales to any party in the war.',
            {'stability_factor': 0.04}, ('peace', 'scales')),
    IdeaDef('good_offices', 'Good Offices', 'A reputation as an honest broker, earned by relief voyages.',
            {'stability_factor': 0.05, 'political_power_gain': 0.10}, ('peace', 'medical')),
    IdeaDef('national_network', 'The National Network', 'Domestic routing and backup links for essential services.',
            {'research_speed_factor': 0.03, 'planning_speed': 0.05}, ('communications', 'satellite')),
    IdeaDef('hardened_network', 'The Hardened Network', 'Ground backups, radio relays and manual procedures if orbit goes dark.',
            {'research_speed_factor': 0.04, 'planning_speed': 0.10, 'air_detection': 0.05}, ('communications', 'shelter')),
    IdeaDef('harbour_guns', 'Harbour Guns', 'Radar-guided guns and short-range missiles around every major port.',
            {'static_anti_air_damage_factor': 0.15, 'air_defence_factor': 0.05}, ('security', 'radar')),
    IdeaDef('signal_shield', 'The Signal Shield', 'Electronic shields that jam and spoof drone links near the ports.',
            {'air_detection': 0.10, 'research_speed_factor': 0.03}, ('radar', 'communications')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('crown_ministry', 'Crown Ministry of the Chamber',
           'A cabinet drawn from the elected chamber majority, governing collectively in the name of the crown and bound by '
           'ministerial responsibility. Provisional gameplay office with no named holder.',
           'monarchism', 'constitutional_monarchy', elections=True),
    Office('privy_council', 'Privy Council of the Crown Lands',
           'A small council named by the throne that holds the seals, the officer lists and the budget, with the chamber kept '
           'as an advisory body. Provisional gameplay office with no named holder.',
           'monarchism', 'absolutism'),
    Office('order_directorate', 'Crown Directorate of Order',
           'A directorate of court officers, police chiefs and loyal ministers ruling by decree under the archive creed of '
           'Perblan Totalitarianism. Provisional gameplay office with no named holder.',
           'monarchism', 'perblan_totalitarianism'),
    Office('assembly_government', 'Assembly Government of the Four Lands',
           'An executive committee elected by the assembly of the four crown lands, with the throne kept as a ceremonial office. '
           'Provisional gameplay office with no named holder.',
           'democratic', 'social_democracy', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('crown_question', 'The Crown Question', (
        "The session opens in the old throne hall at Gatewood with the usual music and an unusual agenda. For the first time in "
        "living memory the clerks have placed the government itself on the order paper. Perbla is a kingdom of four crown lands "
        "held together by one throne, a century-old service year and an economy that leans on its arms plants. Each of those "
        "pillars now has a faction that wants it rebuilt.",
        "The constitutional camp wants ministers who answer to an elected chamber. The palace party wants the seals returned to "
        "a privy council that can act without waiting for votes. A harder faction speaks of order above all, of a crown that "
        "governs by decree because elected governments always drift back to greed. Deputies from the outer lands ask whether "
        "the crown needs to govern at all, or only to reign.",
        "None of these camps commands a majority today. What the court decides in this first session is not which answer wins, "
        "but how the question will be argued: in the open, with the chamber and the press watching, or behind the palace doors. "
        "Either way, the arms trusts, the officer corps and the four lands are already counting their friends.",
    ), (
        Option('Argue it in the open chamber.', (Stability(0.03), PP(-15))),
        Option('Keep the debate inside the palace.', (PP(40), Stability(-0.02))),
    ), picture=0),
    EventDef('four_lands', 'Four Lands, One Throne', (
        "The census clerks return from the crown lands with trunks of ledgers and a list of complaints. Serenava, the frontier "
        "land facing Osea, says it carries the kingdom's airfields and bunker lines but receives little else. Terentio, spread "
        "between the desert fields and the northern coast, reports towns that still haul their water by truck. Relentio, home "
        "of the great port of Sofern, wants its harbour councils recognised and its customs revenue respected.",
        "Perbla proper, around Gatewood and the old heartland, has its own grievance: it pays most of the taxes and is blamed "
        "for most of the decisions. The old charters that bind the four lands disagree with one another about courts, the "
        "language of record and who may levy what. Every land can quote a charter that favours it, and most of them do.",
        "Ministers must decide how to present the census. Published in full, it will start a long argument about fairness "
        "that the crown cannot control. Kept for the ministries, it will guide policy quietly while every land suspects the "
        "worst. The crown lands have lived together for generations; the question is whether they will keep doing so out of "
        "loyalty or out of habit.",
    ), (
        Option('Publish the census in full.', (Stability(0.03), PP(-20))),
        Option('Keep it for the ministries.', (PP(35), Stability(-0.01))),
    ), picture=0),
    EventDef('unfinished_plants', 'The Unfinished Plants', (
        "The audit teams have walked every arms plant in the kingdom, and their report is long. The last expansion left halls "
        "without roofs, presses delivered but never installed, and payrolls for production lines that exist only on paper. "
        "Arms output still dominates the economy, which means the waste is not a side issue. In many districts it is the "
        "economy.",
        "Economists have warned for years that a sector this large and this fragile could take the whole kingdom down with it "
        "if a big customer vanished or a major firm failed. The audit puts numbers on that warning. Some plants can be finished "
        "cheaply; others should never have been started. A handful of contractors were paid twice for the same work, and the "
        "trusts would very much like that paragraph removed.",
        "The treasury wants the audit to become the foundation of a new industrial model, whatever that model turns out to be. "
        "The trusts want it treated as a confidential briefing. The officer corps asks only that nothing be closed before it "
        "knows what it would lose. The cabinet has the report on the table and must decide who else gets to read it.",
    ), (
        Option('Share the report with the chamber.', (Stability(-0.02), Research('industry', 0.5, 1))),
        Option('Brief the trusts privately.', (PP(40), WarSupport(0.02))),
    ), picture=1),
    EventDef('one_firm', 'One Firm, One Kingdom', (
        "The study on the national electronics firm arrives with a plain title and an alarming summary. The firm makes nearly "
        "every circuit the army uses and most of those in civilian industry, from radios to factory controls. It is famous "
        "abroad and proud at home. If it failed, the study concludes, whole sectors would stop within weeks for lack of parts.",
        "The firm's board insists it is healthy and that the study insults a national success. Its few rivals say the firm uses "
        "its size to starve them of contracts. The defence staff says it does not care who is right; it wants a second source "
        "for anything that keeps an aircraft flying or a radar turning. The university at Gatewood says it could train twice "
        "the engineers if it had laboratories outside the firm's gates.",
        "The government now has to decide what kind of partner the crown should be to the kingdom's most important company. It "
        "can back the firm as a national champion, or it can work patiently to make the kingdom less dependent on it. Either "
        "path takes years, and the firm's board will be reading every line of the cabinet minutes.",
    ), (
        Option('Back the firm as a national champion.', (PP(20), Research('electronics', 0.5, 1))),
        Option('Plan for a kingdom less dependent on it.', (Stability(-0.01), Research('industry', 0.5, 1))),
    ), picture=2),
    EventDef('service_year', 'The Service Year Debate', (
        "For more than a century every young Perblan has spent a year in uniform. The policy was built to match the size of "
        "Osea's forces, and it has given the kingdom an enormous pool of trained reservists. It has also given it barracks that "
        "flood every spring, a training budget larger than some ministries and a year of every worker's youth spent away from "
        "fields and factories.",
        "The general staff wants the year kept and modernised; in its view, the frontier with Osea has not moved and neither "
        "should the policy. Employers and many families want it shortened or made voluntary, arguing that a growing economy "
        "needs young workers more than parade grounds. A third group proposes that conscripts be allowed to serve in civil "
        "brigades building roads and wells in the poorer crown lands.",
        "The royal review must hear all of them before it recommends anything. How it is run matters as much as what it "
        "concludes: a review led by generals will be trusted by the army and doubted by everyone else, while a review open to "
        "employers and families will be trusted by the public and resented in the officers' messes.",
    ), (
        Option('Let the general staff lead the review.', (XP('army', 20), WarSupport(0.02))),
        Option('Give employers and families a voice.', (Stability(0.03), PP(-10))),
    ), picture=0),
    EventDef('belkan_war', 'War Beyond the Frontier', (
        "In the spring of 1995 the long crisis around Belka becomes open war. Perbla is not a party to it, yet it can hardly "
        "stand apart from it in spirit. Belka has been the kingdom's oldest friend for generations, and the Belkan munitions "
        "branch at Gatewood employs thousands. Osea, the largest neighbour, sits directly across the Serenava frontier, and the "
        "service year was built a century ago to match its army.",
        "The first days bring rumours faster than facts. Radio bulletins contradict each other, foreign embassies ask what "
        "Perbla intends, and shipping insurers raise their rates on every lane near the war. Frontier commanders in Serenava "
        "report heavy traffic on the far side of the line, though nobody can say whether it is guarding or preparing. In the "
        "capital, crowds gather outside newspaper offices waiting for the evening editions.",
        "The crown has opened a war room in Gatewood and placed the frontier commands on watch. It has not yet said where its "
        "sympathies lie, and every faction is pressing for a statement. The government's first task is smaller and harder: to "
        "decide how much of its own uncertainty it should share with the public.",
    ), (
        Option('Tell the public everything we know.', (Stability(-0.02), WarSupport(0.04))),
        Option('Reassure first, explain later.', (Stability(0.02), WarSupport(-0.02))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25 in docs/research/CHRONICLE_INDEX.md; the Perblan response is gameplay',
        picture=2),
    EventDef('old_alliance', 'The Old Alliance Debated', (
        "Behind closed doors, the court takes up the question every officers' mess has argued since the war began: what does "
        "Perbla owe Belka? The friendship between the two nations is old enough to be ceremonial and warm enough to be real. "
        "Belkan contracts keep the munitions branch at Gatewood busy, and many senior officers trained beside Belkan colleagues. "
        "Osea, by long habit, is the neighbour the kingdom plans against.",
        "A loud minority wants more than sympathy. They speak of a second front, of a brother nation in its hour of need, of "
        "honour. Others answer that any second front would be fought on Perblan soil, along the Serenava bunkers, against a "
        "neighbour many times larger. The ports and converted factories, which trade across the frontier every day, want no "
        "part of it. The crown listens to all of them and says very little.",
        "The decision recorded today is a statement of policy, not a declaration of war. Any armed intervention would be a "
        "separate and grave act, taken only if the war itself forced the question. What the court can settle now is the tone: "
        "how warmly Perbla speaks of its old friend, and how carefully it speaks to its larger neighbour.",
    ), (
        Option('Speak warmly of our old friends.', (WarSupport(0.03), PP(15))),
        Option('Speak carefully to everyone.', (Stability(0.03),)),
        Option('Remind Osea of our frontier divisions.', (WarSupport(0.02), XP('army', 15))),
    ), layer='Mod provenance',
        citation='events/Perbla.txt perbla_intervention.1 to .3 and the historical_friends and historical_enemies opinion '
                 'modifiers in common/on_actions/ac_on_actions.txt; this debate commits no forces and leaves that path unchanged',
        picture=0),
    EventDef('ulysses', 'Ulysses in the Night Sky', (
        "Since the astronomers' warning of December 1994, the asteroid called Ulysses has been a distant worry. In April 1996 "
        "it becomes a near one, when the world is told that it will strike the Earth and that nations must prepare. Nobody can "
        "yet say where the fragments will fall. Perbla, like every country, has to plan for a danger whose location is still a "
        "guess.",
        "The crown's advisers split along familiar lines. Engineers propose deep shelters under the large cities, stocked for "
        "weeks. Astronomers and radar specialists propose early warning and evacuation instead, arguing that hours of notice "
        "save more lives than concrete. The treasury notes that either plan costs as much as a new arms programme, and the "
        "arms trusts note that their own plans would be delayed.",
        "Public mood swings between panic and denial. Places of worship are full, hardware shops sell out of tinned food, and "
        "some families on the coast talk of moving inland. The government must decide how to speak about a threat it cannot "
        "control, and whether its first priority is calm or preparation. Both, the ministers know, cannot be bought at once.",
    ), (
        Option('Prepare openly and quickly.', (WarSupport(0.02), Stability(-0.02), Research('construction_tech', 0.5, 1))),
        Option('Keep calm and keep working.', (Stability(0.03),)),
    ), citation='date anchors only, ACES Chronicle rows 1994 / 12.10 and 1996 / 04.20 in docs/research/CHRONICLE_INDEX.md; '
                'Perblan preparations are gameplay', picture=2),
    EventDef('desert_oil', 'Oil Under Terentio', (
        "The geological survey of the Terentio desert is finished, and its maps are better than anyone hoped. The fields hold "
        "far more oil than the old rigs suggested, and the bauxite beds stretch toward Torre Mountain. For a kingdom that has "
        "lived on arms contracts, the desert offers a second income that does not depend on anyone else's war.",
        "The question is who will own it. A crown company would keep the revenue at home but drill slowly, managed by "
        "ministries with other priorities. Private concessions would bring rigs and foreign capital within a few years but "
        "hand the desert's future to shareholders. Terentio's own towns, which have hauled water by truck for generations, "
        "want to know what share of the wealth will stay where it is pumped.",
        "Investors are already calling the ministry, and some are offering terms that sound generous until the fine print. "
        "The trusts want first claim on the steel and power the new fields will need. Before any model is chosen, the "
        "government must decide whether to slow the rush or welcome it, knowing that whatever it says this week will be quoted in every negotiation that follows.",
    ), (
        Option('Keep the desert under the crown for now.', (PP(30), Stability(0.01))),
        Option('Let the investors move fast.', (Research('excavation_tech', 0.5, 1), Stability(-0.01))),
    ), picture=1),
    EventDef('decade_review', 'Ten Years On', (
        "A decade after the crown question was first opened, an independent panel publishes its review of how the kingdom "
        "governs itself. It lists what the chosen order has built, whom it has failed and what it now costs to run. The panel "
        "includes judges, economists and deputies from all four crown lands, and its members were chosen by lot rather than "
        "by the government of the day.",
        "The findings are mixed in ways every faction can quote. The industrial towns are richer and the frontier is calm, but "
        "the outer lands still feel governed from Gatewood, young graduates still leave for jobs abroad, and too many decisions "
        "depend on a handful of offices and firms. The panel warns that the next decade will test whether the arrangements of "
        "the nineties can bend without breaking.",
        "The government must decide how to answer. It can publish the review unedited and accept a season of hostile "
        "headlines, or release an approved summary that highlights success and buries the rest. Either way, the review "
        "will set the terms of political argument for the new century, and every faction already has its quotations ready.",
    ), (
        Option('Publish the review unedited.', (Stability(0.03), PP(-20))),
        Option('Release an approved summary.', (PP(35), Stability(-0.02))),
    ), picture=0),
    EventDef('firm_stress', 'The Monday Morning Exercise', (
        "At six on a Monday morning the treasury opens the sealed rescue plan and runs it as though the national electronics "
        "firm had missed its payroll. Banks are told to freeze credit lines, suppliers are told to expect no payment, and the "
        "defence staff is asked which aircraft would be grounded first. Nobody outside the exercise is supposed to know.",
        "By noon the gaps are obvious. The emergency credit line takes three days to clear rather than three hours. Two "
        "critical radar parts have no second source after all. The plan assumed the firm's managers would cooperate, and in "
        "the exercise they did not. By evening a newspaper has the story, and the firm's investors begin a nervous week of "
        "phone calls to the ministry.",
        "The exercise has done its job: it found the failures before a real crisis did. Now the government must decide what "
        "to do with what it learned. It can close the gaps quietly and deny the leak, or publish the lessons and accept that "
        "the firm's reputation will take a knock. The defence staff has already said which it prefers, and the firm's board has said the opposite.",
    ), (
        Option('Close the gaps quietly.', (PP(-20), Research('electronics', 0.5, 1))),
        Option('Publish the lessons.', (Stability(-0.02), PP(25))),
    ), picture=2),
    EventDef('pacific_war', 'A Neighbour at War', (
        "In late September 2010 Yuktobania declares war on Osea and attacks an Osean port. Perbla wakes to the news that its "
        "largest neighbour, the country its service year was built to match, is fighting a war that has nothing to do with "
        "the Serenava frontier. For once, Osea's guns point away from Perbla.",
        "The consequences arrive anyway. Shipping insurers raise rates on every lane that touches Osean waters. Osean buyers "
        "call Perblan factories asking for trucks, electronics and munitions, and they want them now. Yuktobanian diplomats ask "
        "pointed questions about what Perbla intends to sell. Frontier towns that live on trade with Osea worry about their "
        "customers, and harbour masters worry about submarines.",
        "The security council meets in Gatewood to decide the kingdom's posture. Some ministers see a commercial opportunity "
        "that may not come again. Others see a trap: a neutral kingdom that sells to one side of a war is no longer neutral in "
        "the eyes of the other. The first decision is how to describe Perbla's position in public, before Osean and Yuktobanian newspapers describe it for the kingdom.",
    ), (
        Option('Declare strict neutrality at once.', (Stability(0.02), PP(15))),
        Option('Keep every option open for now.', (PP(30), Stability(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 2010 / 09.27 in docs/research/CHRONICLE_INDEX.md; the Perblan response is gameplay',
        picture=1),
    EventDef('port_drones', 'Drones Over the Harbours', (
        "On 15 May 2019 drone attacks strike four major Osean naval ports, and on the same day Erusea declares war on Osea. "
        "The footage from the Osean harbours is everywhere by evening: small, cheap aircraft slipping past defences built for "
        "missiles and bombers. Perbla's own harbours at Sofern and Baleton are smaller, but they are built the same way.",
        "The security council meets the same night. The navy reports that its harbour defences could not reliably stop a "
        "swarm of small drones. The engineers at Gatewood argue that most such drones depend on radio links and satellite "
        "navigation that could be jammed. The ports' owners ask who will pay for any of it, and the ministers ask how long "
        "it would take.",
        "Nobody in the room expects Perbla to be a target. That is precisely what worries the navy: the Osean ports did not "
        "expect it either. The government must decide whether to treat this as a distant war's lesson or as an immediate "
        "warning, and the answer will shape a decade of spending. Whatever it chooses, the harbour masters want an answer before the summer shipping season begins.",
    ), (
        Option('Treat it as an immediate warning.', (WarSupport(0.03), PP(-15))),
        Option('Study it before spending.', (Research('radar_tech', 0.5, 1),)),
    ), citation='date anchor only, ACES Chronicle row 2019 / 05.15 in docs/research/CHRONICLE_INDEX.md; the Perblan response is gameplay',
        picture=2),
)

# --- branches ------------------------------------------------------------------------------------
CROWN = Branch('crown', 'The Crown Question', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('crown_court_sits', 'The Court Sits at Gatewood',
          "The crown opens the 1991 session at Gatewood with a kingdom that runs on arms plants, a service year and four crown "
          "lands that answer to one throne. Before any reform, the court has to agree who actually governs. Opening the question "
          "costs the palace its habit of deciding in private, but it buys every faction a hearing.",
          ('command', 'assembly'), reward=(Idea('court_in_session'), Event('crown_question'))),
    Focus('crown_powers_ledger', 'A Ledger of Royal Powers',
          "Clerks of the court list every power the crown actually uses: appointments, war powers, the budget seal, the pardon "
          "and the right to dissolve the chamber. The list is dull and dangerous at once, because every faction will read it "
          "as a menu. Compiling it spends political capital and makes the next choice unavoidable.",
          ('document', 'scales'), after=('crown_court_sits',),
          reward=(PP(35), Tooltip('Opens the four constitutional paths; only one can be taken.'))),
    Focus('crown_parliament_path', 'Ministers Answer to the Chamber',
          "The constitutional camp wants the crown kept and the cabinet made answerable to an elected chamber. Ministers would "
          "face questions, budgets would be voted and the palace would sign rather than decide. It is the path closest to how "
          "the kingdom already claims to work, and it costs the crown the quiet authority it still enjoys.",
          ('ballot', 'assembly'), after=('crown_powers_ledger',),
          exclusive=('crown_privy_path', 'crown_order_path', 'crown_assembly_path'),
          reward=(SwapIdea('court_in_session', 'ministry_charter'),)),
    Focus('crown_privy_path', 'The Seals Return to the Palace',
          "Courtiers argue that a kingdom with a fragile arms economy cannot wait on chamber votes. They propose that the great "
          "seals, the budget and the officer lists go back to a privy council chosen by the throne, with the chamber left to "
          "advise. The palace gains speed. The parties lose their reason to cooperate with anyone.",
          ('command', 'document'), after=('crown_powers_ledger',),
          exclusive=('crown_parliament_path', 'crown_order_path', 'crown_assembly_path'),
          reward=(SwapIdea('court_in_session', 'privy_seal'),)),
    Focus('crown_order_path', 'The Doctrine of Order',
          "A hard faction at court, followers of the creed called Perblan Totalitarianism, holds that elected governments slide "
          "back into greed and self-interest the moment they feel safe. It offers obedience in exchange for safety: rule by "
          "decree, a policed press and a crown that answers to no chamber. Order arrives quickly; consent never does.",
          ('security', 'command'), after=('crown_powers_ledger',),
          exclusive=('crown_parliament_path', 'crown_privy_path', 'crown_assembly_path'),
          reward=(SwapIdea('court_in_session', 'order_decrees'),)),
    Focus('crown_assembly_path', 'The Assembly Claims the Seals',
          "Deputies from the four crown lands propose that the elected assembly govern in its own name, with the crown kept as "
          "a ceremonial office above party. It would end the throne's working role while keeping its symbols. Industrial towns "
          "and the Relentio ports favour the idea; the officer corps and the palace staff do not.",
          ('assembly', 'ballot'), after=('crown_powers_ledger',),
          exclusive=('crown_parliament_path', 'crown_privy_path', 'crown_order_path'),
          reward=(SwapIdea('court_in_session', 'assembly_mandate'),)),
    Focus('crown_parliament_ministry', 'Form the Crown Ministry',
          "A cabinet drawn from the chamber majority takes the government seals, and the crown is bound to act on ministerial "
          "advice. The change runs through the office, not a person: the ministry governs collectively and answers for its "
          "budget. The palace loses daily control, and the chamber gains the blame for every bad year.",
          ('ballot', 'document'), after=('crown_parliament_path',), cost=10,
          exclusive=('crown_privy_council', 'crown_order_directorate', 'crown_assembly_government'),
          reward=(Regime('crown_ministry'), Flag('path_parliament'))),
    Focus('crown_privy_council', 'Convene the Privy Council',
          "The throne names a small privy council to hold the seals, the officer lists and the budget. Elections are suspended "
          "while the council governs by order, keeping the chamber as a sounding board. It is efficient and narrow. Every "
          "decision now carries the crown's name, so every failure will carry it too.",
          ('command', 'assembly'), after=('crown_privy_path',), cost=10,
          exclusive=('crown_parliament_ministry', 'crown_order_directorate', 'crown_assembly_government'),
          reward=(Regime('privy_council'), Flag('path_privy'))),
    Focus('crown_order_directorate', 'Install the Directorate of Order',
          "A directorate of court officers, police chiefs and loyal ministers takes executive power under the crown's banner. "
          "Decrees replace statutes, parties are suspended and the newspapers report to a censor. The directorate promises calm "
          "in the arms towns and a disciplined service year. It pays for that calm with fear, which never balances a budget.",
          ('security', 'document'), after=('crown_order_path',), cost=10,
          exclusive=('crown_parliament_ministry', 'crown_privy_council', 'crown_assembly_government'),
          reward=(Regime('order_directorate'), Flag('path_order'))),
    Focus('crown_assembly_government', 'Seat the Assembly Government',
          "The assembly elects an executive committee that governs in its own right, and the crown withdraws to ceremony, "
          "honours and the oath of office. Elections stay on a fixed calendar. The arms trusts lose their private line to the "
          "palace, and the deputies inherit an economy built for war that they have never had to run.",
          ('assembly', 'scales'), after=('crown_assembly_path',), cost=10,
          exclusive=('crown_parliament_ministry', 'crown_privy_council', 'crown_order_directorate'),
          reward=(Regime('assembly_government'), Flag('path_assembly'))),
    Focus('crown_question_time', 'Question Time for Ministers',
          "Every week the ministers stand in the chamber and answer questions from any deputy, broadcast on national radio. "
          "Scandals that once stayed in palace corridors now reach every kitchen. The government looks weaker for a while and "
          "the officer corps dislikes being questioned in public. Over time, people trust what they can hear argued.",
          ('ballot', 'communications'), after=('crown_parliament_ministry',),
          exclusive=('crown_privy_estates', 'crown_order_censors', 'crown_assembly_charter'),
          reward=(Stability(0.04), WarSupport(-0.02))),
    Focus('crown_privy_estates', 'Crown Estates Pay Their Way',
          "The privy council orders the crown's own estates in the old heartland to fund a modern mill instead of the court's "
          "ceremonies. It is a show of seriousness that costs the palace some comfort and much patronage, and courtiers lose "
          "their sinecures. Old Perbla gains a working plant and a reason to defend the council's rule.",
          ('economy', 'command'), after=('crown_privy_council',),
          exclusive=('crown_question_time', 'crown_order_censors', 'crown_assembly_charter'),
          reward=(Build('industrial_complex', 1, 601), PP(-25))),
    Focus('crown_order_censors', 'A Censor in Every Newsroom',
          "The directorate places a censor in every newspaper, radio studio and printing house, with authority to stop any story "
          "touching security, the crown or the economy. Rumours vanish from print and move to kitchens and bars. Foreign "
          "correspondents leave. The government gains silence and loses the ability to hear bad news before it becomes a crisis.",
          ('security', 'communications'), after=('crown_order_directorate',),
          exclusive=('crown_question_time', 'crown_privy_estates', 'crown_assembly_charter'),
          reward=(WarSupport(0.05), Stability(0.03), PP(-30))),
    Focus('crown_assembly_charter', 'A Written Federal Charter',
          "The assembly drafts a federal charter defining the powers of the executive committee, the deputies and the four crown "
          "lands, and the narrow ceremonial duties left to the throne. Ratification needs every land's consent, which costs "
          "months of bargaining and several concessions. The charter is long and imperfect, and widely read.",
          ('document', 'assembly'), after=('crown_assembly_government',),
          exclusive=('crown_question_time', 'crown_privy_estates', 'crown_order_censors'),
          reward=(Stability(0.05), PP(-40))),
))

LANDS = Branch('lands', 'The Four Crown Lands', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('lands_count', 'Count the Four Crown Lands',
          "Perbla is a union of four crown lands, Perbla proper, Serenava, Terentio and Relentio, held together by one throne and "
          "a tangle of old charters. Nobody in Gatewood has an accurate count of their roads, schools or tax rolls. A full "
          "census costs a season of clerical work and tells every land exactly what it is owed.",
          ('document', 'civil'), reward=(Idea('crown_lands_compact'), Event('four_lands'))),
    Focus('lands_serenava', 'Serenava Frontier Towns',
          "Serenava is the crown land that faces Osea, and its towns live among airfields and bunker lines left by older "
          "governments. Residents want roads that serve markets as well as garrisons. Paving the civil roads costs money the "
          "army would rather spend on concrete, but a frontier that resents Gatewood is a poor frontier.",
          ('security', 'civil'), after=('lands_count',), reward=(Build('infrastructure', 1, 581),)),
    Focus('lands_terentio', 'Wells for the Terentio Towns',
          "Terentio's towns stretch from the desert fields to the northern coast, and most of them still haul water by truck. "
          "Drilling municipal wells and fixing the roads between them is cheap compared to an oil rig, yet it has never been "
          "anyone's priority. The crown pays now so that the desert stops treating Gatewood as a stranger.",
          ('tools', 'civil'), after=('lands_count',), reward=(Build('infrastructure', 1, 209),)),
    Focus('lands_relentio', 'Relentio Harbour Councils',
          "Relentio holds the busiest docks in the kingdom and a merchant class that already runs its own harbour councils. "
          "Recognising those councils formally, and rebuilding the coastal road between them, buys the loyalty of the ports. "
          "The price is that Relentio will expect a voice in every customs decision the crown makes afterwards.",
          ('navy', 'assembly'), after=('lands_count',), reward=(Build('infrastructure', 1, 597),)),
    Focus('lands_old_perbla', 'Old Perbla Keeps Its Mills',
          "The heartland around Old Perbla has steel and tungsten mines but few modern mills to use them. A crown loan lets the "
          "district build its own finishing works instead of shipping ore to the arms plants. It is a modest investment, and it "
          "reminds the other three lands that Perbla proper also needs work.",
          ('industry', 'civil'), after=('lands_count',), reward=(Build('industrial_complex', 1, 601),)),
    Focus('lands_dakrain_commission', 'A Frontier Commission with Dakrain',
          "Dakrain disputes the Terentio frontier, and herders, smugglers and water trucks cross it every day without asking "
          "anyone. A joint commission on crossings, wells and customs posts changes nobody's claim, but it gives both sides a "
          "desk to call before an incident turns into a crisis. The cost is admitting in public that the dispute exists.",
          ('diplomacy', 'document'), after=('lands_count',),
          reward=(Stability(0.03), Tooltip('No claim, core or border changes; the commission handles crossings, water and customs only.'))),
    Focus('lands_charters', 'Charters for Each Crown Land',
          "Each crown land receives a written charter with its own budget line, local courts and a governor answerable to a "
          "land diet. Gatewood keeps defence, foreign affairs and the currency. Devolution calms the outer lands and speeds "
          "local building, though it hands four treasuries the power to bargain with the capital every year.",
          ('document', 'scales'), after_any=('lands_serenava', 'lands_terentio', 'lands_relentio'), cost=10,
          exclusive=('lands_chancery',), reward=(SwapIdea('crown_lands_compact', 'land_charters'), Flag('lands_devolved'))),
    Focus('lands_chancery', 'One Chancery in Gatewood',
          "The opposite answer folds the old charters into one chancery at Gatewood, with a single tax code and prefects sent "
          "out from the capital. Decisions get faster and the budget gets simpler. The outer lands lose their separate seals, "
          "and their notables will remember who took them the next time Gatewood asks for help.",
          ('command', 'document'), after_any=('lands_serenava', 'lands_terentio', 'lands_relentio'), cost=10,
          exclusive=('lands_charters',), reward=(SwapIdea('crown_lands_compact', 'single_chancery'), Flag('lands_centralised'))),
    Focus('lands_diets', 'Diets Meet in Every Land',
          "With charters signed, each crown land convenes its own diet. Their first budgets go to projects Gatewood never funded, "
          "and the Serenava diet votes a workshop district for its garrison towns. The diets are slow and quarrelsome, and the "
          "crown must now negotiate rather than instruct, but local money finally builds local things.",
          ('assembly', 'ballot'), after=('lands_charters',), reward=(Build('industrial_complex', 1, 581),)),
    Focus('lands_prefects', 'Prefects on the Circuit',
          "Chancery prefects ride the rail circuit from Gatewood through every land, inspecting tax offices, schools and road "
          "works on a fixed calendar. Their reports go straight to the capital. The circuit costs salaries and train time, and "
          "it ends the local habit of reporting only good news, which is exactly why land notables hate it.",
          ('command', 'rail'), after=('lands_chancery',), reward=(Build('infrastructure', 1, 112), PP(25))),
    Focus('lands_accord', 'The Crown Lands Accord',
          "Whichever constitutional answer the crown chose, the four lands sign a short accord fixing the shares of revenue, "
          "the language of the courts and the order of precedence at state occasions. It is mostly paperwork. It also ends a "
          "decade of petitions and lets later governments plan without reopening the union every year.",
          ('peace', 'assembly'), after_any=('lands_diets', 'lands_prefects'), reward=(Flag('lands_accord_set'), Stability(0.03))),
))

HEAVY = Branch('heavy', 'The Heavy Industry Reckoning', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('heavy_audit', 'Audit the Unfinished Plants',
          "The arms sector that dominates the economy is full of half-built halls, idle presses and contracts paid but never "
          "delivered. An audit team from the treasury walks every plant and prices what it would take to finish or close it. "
          "The audit annoys the trusts and costs a year of political quiet, but nothing else can start without it.",
          ('industry', 'document'), reward=(Idea('arms_ledger'), Event('unfinished_plants'))),
    Focus('heavy_finish_halls', 'Finish What Was Started',
          "Some unfinished halls in the Serenava garrison towns need only roofs, power lines and machine tools to work. The crown pays to finish "
          "the most advanced of them rather than starting new ones, accepting that the money rewards contractors who failed the "
          "first time. Finished halls are cheaper than new ones, and the workforce is already there.",
          ('tools', 'industry'), after=('heavy_audit',), reward=(Build('industrial_complex', 1, 581),)),
    Focus('heavy_missing_funds', 'Publish the Missing Funds',
          "The audit found money paid for machines that were never installed. Publishing the totals, without trial by newspaper "
          "of individuals, tells the trusts that the old arrangements are over. It costs stability, because the numbers are "
          "ugly, and it makes enemies among suppliers who expected discretion. Honest books make later reforms believable.",
          ('scales', 'document'), after=('heavy_audit',), reward=(Flag('audit_published'), Stability(-0.03))),
    Focus('heavy_plowshares', 'Plowshares from the Arsenals',
          "The conversion school says the kingdom builds too many shells for a country at peace. It proposes turning arms halls "
          "into plants for trucks, pumps, rail stock and household goods, protected for a decade. Civil output rises and jobs "
          "stay local. The army loses capacity it may want back, and the trusts lose their richest customer.",
          ('rebuild', 'industry'), after=('heavy_finish_halls',), cost=10, exclusive=('heavy_arsenal', 'heavy_circuits_lead'),
          reward=(SwapIdea('arms_ledger', 'plowshare_works'), Flag('model_conversion'))),
    Focus('heavy_arsenal', 'An Arsenal for Export',
          "The export school says the arms plants are the kingdom's comparative advantage and should sell to any buyer the "
          "crown approves. Licences, credit and a sales office would keep the lines running at full rate. Revenue comes fast "
          "and the army keeps its supplier base. The kingdom becomes dependent on other countries' wars and its own discretion.",
          ('missile', 'economy'), after=('heavy_finish_halls',), cost=10, exclusive=('heavy_plowshares', 'heavy_circuits_lead'),
          reward=(SwapIdea('arms_ledger', 'southern_arsenal'), Flag('model_arsenal'))),
    Focus('heavy_circuits_lead', 'Let Electronics Lead Industry',
          "A third school wants the national electronics firm, already the kingdom's best-known company, to set the pace. Arms "
          "plants would shrink toward components, sensors and machine controls, with credit flowing to suppliers. It promises "
          "higher value per worker. It also deepens the dependence on one firm that the treasury already fears.",
          ('communications', 'industry'), after=('heavy_finish_halls',), cost=10, exclusive=('heavy_plowshares', 'heavy_arsenal'),
          reward=(SwapIdea('arms_ledger', 'circuit_economy'), Flag('model_circuits'))),
    Focus('heavy_tractor_lines', 'Truck and Tractor Lines',
          "The first conversion contract retools two arms halls in the Relentio valley to build trucks and tractors for the "
          "crown lands. Machine tools come from idle shell lines, and the workforce keeps its jobs. Output is slow for a year "
          "while crews retrain, and the army watches its reserve capacity vanish into farm equipment.",
          ('logistics', 'tools'), after=('heavy_plowshares',), reward=(Build('industrial_complex', 2, 173),)),
    Focus('heavy_shops_before_shells', 'Shops Before Shells',
          "Converted plants turn to household goods, and the treasury lowers excise on stoves, radios and bicycles for two "
          "years. Shops fill for the first time in a generation. The tax break costs revenue, and some trusts complain that "
          "they now compete with imports they cannot beat. The goodwill in the towns is real and measurable.",
          ('economy', 'civil'), after=('heavy_plowshares',), reward=(TimedIdea('consumer_drive', 730),)),
    Focus('heavy_export_board', 'An Arms Export Board',
          "A crown export board licenses every sale, checks end users and finances new orders with credit. The Relentio valley "
          "plants get two new lines to meet the first contracts. The board's rules are only as strict as the government that "
          "appoints it, and every foreign order ties the kingdom's reputation to someone else's war.",
          ('diplomacy', 'missile'), after=('heavy_arsenal',), reward=(Build('arms_factory', 2, 173),)),
    Focus('heavy_licence_lines', 'Licensed Production Lines',
          "Foreign designs built under licence keep the export lines modern without a full design bureau. The kingdom pays "
          "royalties and accepts limits on resale, while its engineers learn from every drawing. A plant in the western valley "
          "takes the first licence. It is a faster route than domestic design, and a more dependent one.",
          ('tools', 'missile'), after=('heavy_arsenal',), reward=(Build('arms_factory', 1, 112), Research('artillery', 0.5, 1))),
    Focus('heavy_component_suppliers', 'Components for Every Factory',
          "Arms halls in the western valley convert to circuit boards, wiring looms and instrument panels that every other "
          "factory needs. The electronics firm guarantees orders for five years, and small suppliers multiply around the plant. "
          "The guarantee means the firm, not the treasury, now sets the pace of a whole district.",
          ('communications', 'tools'), after=('heavy_circuits_lead',), reward=(Build('industrial_complex', 1, 112),)),
    Focus('heavy_supplier_credit', 'Credit for Small Suppliers',
          "A crown credit window lends to small component makers that the big firm will not finance. Loans carry low rates in "
          "exchange for open books and shared test labs. Defaults will happen and the treasury will carry them. The aim is a "
          "second tier of suppliers, so that the kingdom does not stand or fall with one company.",
          ('economy', 'science'), after=('heavy_circuits_lead',), reward=(Research('electronics', 0.5, 2), PP(-20))),
    Focus('heavy_shock_reserve', 'A Reserve Against the Shock',
          "Whatever model wins, the treasury sets aside a reserve fund for the day a major customer cancels or a firm fails. It "
          "is invested in nothing glamorous and earns little. Ministers will be tempted to raid it every budget year. If it "
          "survives, the next industrial shock lands on a cushion instead of on the streets.",
          ('scales', 'economy'), after_any=('heavy_plowshares', 'heavy_arsenal', 'heavy_circuits_lead'),
          reward=(Flag('shock_reserve'), PP(-30))),
))

CIRCUITS = Branch('circuits', 'Gatewood Electronics', 1992, 'FOCUS_FILTER_RESEARCH', (
    Focus('circ_one_firm', 'One Firm Holds the Kingdom',
          "The national electronics firm supplies almost every circuit used by the army and by civilian industry. Its success "
          "is a national boast and a national risk. Before choosing a policy, ministers commission a frank study of what the "
          "kingdom would lose if the firm stumbled. The study costs goodwill with a board that dislikes outside eyes.",
          ('communications', 'economy'), reward=(Event('one_firm'), Research('electronics', 0.5, 1))),
    Focus('circ_public_labs', 'Public Laboratories at Gatewood',
          "The crown opens public laboratories beside the university at Gatewood, so that research no longer lives only inside "
          "the firm. Graduates can test designs without signing the firm's contracts. The labs need a standing budget and years "
          "to matter. They are the first public alternative to a private monopoly of know-how.",
          ('science', 'telescope'), after=('circ_one_firm',), reward=(Idea('gatewood_labs'),)),
    Focus('circ_second_source', 'A Second Source for Parts',
          "The army orders that every critical component must have a second qualified maker, even at a higher price. A small "
          "plant in the harbour district of Perbla proper wins the first contracts. The firm protests that duplication wastes "
          "money. The defence staff answers that a single supplier is a single point of failure.",
          ('tools', 'communications'), after=('circ_one_firm',),
          reward=(Flag('second_source'), Build('industrial_complex', 1, 592))),
    Focus('circ_crown_stake', 'A Crown Stake in the Firm',
          "The treasury buys a minority stake and two seats on the firm's board, gaining a veto over closures and foreign sales "
          "of the core plants. Private investors resent the intrusion and the share price sinks. In exchange the kingdom gains a "
          "hand on the wheel of the company it cannot afford to lose.",
          ('economy', 'command'), after=('circ_public_labs',), exclusive=('circ_open_market',), reward=(Idea('crown_stake'),)),
    Focus('circ_open_market', 'Open the Components Market',
          "The opposite course opens defence component tenders to every qualified supplier, foreign or domestic, and ends the "
          "firm's informal preference. Prices fall and new makers appear. The firm loses guaranteed orders and may cut jobs at "
          "Gatewood. Ministers bet that competition will make the sector sturdier than protection ever did.",
          ('economy', 'diplomacy'), after=('circ_public_labs',), exclusive=('circ_crown_stake',), reward=(Idea('open_components'),)),
    Focus('circ_avionics', 'Avionics with the Belkan Branch',
          "The South Belka Munitions branch at Gatewood builds aircraft parts and needs local electronics. A joint avionics "
          "workshop seats Perblan engineers beside the branch's designers on navigation and fire control sets. The arrangement "
          "depends on the old friendship holding. While it lasts, it is the fastest way to learn aircraft electronics.",
          ('air', 'science'), after=('circ_public_labs',), reward=(Research('radar_tech', 0.5, 1), XP('air', 10))),
    Focus('circ_coastal_radar', 'Radar Sets for the Coast',
          "Locally built radar sets go to the Sofern coast first, where the navy and the air arm share the busiest approaches "
          "in the kingdom. Each station proves that domestic electronics can be trusted in service. The sets are heavier and "
          "less refined than imported ones. They are also repairable at home, which matters more.",
          ('radar', 'navy'), after=('circ_second_source',), reward=(Build('radar_station', 1, 236),)),
    Focus('circ_institute', 'The Gatewood Institute',
          "The public laboratories merge into a technical institute with its own degrees, test ranges and contract office. It "
          "trains the engineers the firm and its rivals both need. The institute costs more each year than the labs did. It "
          "also outlives any single company, which is the whole point of building it.",
          ('science', 'document'), after_any=('circ_crown_stake', 'circ_open_market'),
          reward=(SwapIdea('gatewood_labs', 'gatewood_institute'),)),
    Focus('circ_field_radios', 'Field Radios for the Service Year',
          "Every conscript class trains on radios, field telephones and simple sensors made in Gatewood. The kits are rugged "
          "and cheap, and they produce a generation of recruits who can repair electronics in the field. The order keeps "
          "smaller suppliers busy. It also ties the service year more tightly to the electronics sector.",
          ('communications', 'training'), after=('circ_institute',), reward=(Research('electronics', 0.75, 1), XP('army', 10))),
    Focus('circ_rescue_plan', 'A Plan for the Bad Year',
          "Treasury and defence staff write a sealed plan for the day the electronics firm cannot pay its suppliers: emergency "
          "credit, protected payrolls and priority orders for critical lines. Nobody wants to need it. Drafting it costs time "
          "and a few leaks that worry investors. Having it means a crisis is met by procedure rather than panic.",
          ('shelter', 'economy'), after=('circ_institute',), reward=(Flag('firm_rescue_plan'), Stability(-0.01))),
))

SERVICE = Branch('service', 'The Year of Service', 1991, 'FOCUS_FILTER_MANPOWER', (
    Focus('serv_review', 'Review the Service Year',
          "For more than a century every young Perblan has served a year in uniform, a policy built to match the size of "
          "Osea's forces. The year produces a vast reserve and a heavy bill for barracks, rations and lost labour. A royal "
          "review asks whether the old answer still fits a kingdom that wants to grow.",
          ('training', 'document'), reward=(Event('service_year'),)),
    Focus('serv_depots', 'Repair the Training Depots',
          "Many training depots date from the previous century and flood every spring. Rebuilding their roads, ranges and "
          "kitchens makes the service year less miserable and less wasteful. The depot at Torre Mountain goes first. The work "
          "takes engineering units off frontier duty for a season, which the border commands resent.",
          ('rebuild', 'training'), after=('serv_review',), reward=(Build('infrastructure', 1, 207), XP('army', 10))),
    Focus('serv_keep_year', 'The Year Stays',
          "The crown keeps universal service but rewrites it: shorter drill, more field training and a proper reserve call-up "
          "schedule. The large army remains, and Osea still faces a kingdom where every adult knows how to fight. The economy "
          "keeps paying for a year of every worker's youth, and the barracks budget stays enormous.",
          ('training', 'security'), after=('serv_review',), cost=10, exclusive=('serv_volunteer', 'serv_civil_option'),
          reward=(Idea('service_year_reformed'),)),
    Focus('serv_volunteer', 'A Professional Core',
          "The reformers build a professional core of paid volunteers and long-service officers, while the universal year "
          "shrinks to basic training and reserve listing. Units are better trained and stay together. Families welcome the "
          "change and employers gain workers. The trained reserve will thin within a decade, and generals warn about Osea.",
          ('medal', 'training'), after=('serv_review',), cost=10, exclusive=('serv_keep_year', 'serv_civil_option'),
          reward=(Idea('volunteer_cadres'),)),
    Focus('serv_civil_option', 'A Civil Service Year',
          "A compromise keeps the year of service but lets conscripts choose civil brigades that build roads, wells and "
          "clinics in the crown lands. The army keeps a smaller intake of willing recruits, and public works speed up across "
          "the poorer districts. Officers complain that the choice drains their best candidates into shovels instead of rifles.",
          ('civil', 'tools'), after=('serv_review',), cost=10, exclusive=('serv_keep_year', 'serv_volunteer'),
          reward=(Idea('civil_service_year'),)),
    Focus('serv_reserve_rolls', 'Rolls of the Reserve',
          "A single reserve register lists every trained adult by skill, district and unit, updated each year at the local "
          "town hall. Mobilisation that took weeks now takes days. Keeping the rolls current costs clerks and patience, and "
          "civil liberties groups object to a state that knows where every former soldier lives.",
          ('document', 'security'), after=('serv_keep_year',), reward=(SwapIdea('service_year_reformed', 'reserve_rolls'),)),
    Focus('serv_career_pay', 'Career Pay for Volunteers',
          "Volunteer pay rises to compete with industry, with housing, pensions and technical courses for those who sign on for "
          "longer terms. Recruiting stops being a struggle. The wage bill climbs sharply and the treasury must find the money "
          "every year. In return the kingdom gets soldiers who stay long enough to master their equipment.",
          ('economy', 'medal'), after=('serv_volunteer',), reward=(SwapIdea('volunteer_cadres', 'professional_corps'),)),
    Focus('serv_civil_brigades', 'Brigades for the Crown Lands',
          "The civil brigades take on their first large project, the roads and water lines of the Terentio desert districts. "
          "Conscripts work in rotations under engineers from the army and the ministry of works, and results are visible within "
          "a year. Critics note that free labour also undercuts private builders in the same districts.",
          ('civil', 'rebuild'), after=('serv_civil_option',),
          reward=(SwapIdea('civil_service_year', 'civil_brigades'), Build('infrastructure', 1, 571))),
    Focus('serv_armour_parks', 'Keep the Armour Parks Running',
          "The kingdom keeps hundreds of tanks and tracked guns that need more maintenance than the budget allows. A workshop "
          "programme cannibalises the worst vehicles to keep the rest running and trains mechanics in every armoured unit. "
          "Fewer machines will be ready, but those that are will actually move when the frontier needs them.",
          ('command', 'tools'), after=('serv_depots',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 15))),
    Focus('serv_staff_college', 'A Staff College at Gatewood',
          "Officers learn planning, logistics and combined arms at a staff college instead of inheriting habits from their "
          "regiments. The superior firepower school that guides the army is rewritten for the kit the kingdom actually owns. "
          "The college takes good officers out of units for a year, and curriculum fights delay its first graduation.",
          ('command', 'science'), after=('serv_depots',), reward=(Research('land_doctrine', 0.5, 1), XP('army', 20))),
    Focus('serv_frontier_divisions', 'Divisions for the Frontier',
          "Whatever service model the kingdom chose, the army assigns its readiest divisions to the Serenava frontier that faces "
          "Osea. Units rotate on fixed schedules rather than whenever a crisis looms. Standing frontier divisions cost more than "
          "a reserve that waits at home, but they make every later border decision quicker.",
          ('security', 'gate'), after_any=('serv_reserve_rolls', 'serv_career_pay', 'serv_civil_brigades'),
          reward=(Flag('northern_line'), XP('army', 10))),
))

BORDER = Branch('border', 'The Belkan War Next Door', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bord_news', 'News from the Belkan War',
          "When fighting breaks out around Belka in 1995, Perbla is not a party to it, but it is close to every side. Osea is "
          "its largest neighbour and Belka its oldest friend. The crown puts the frontier commands on watch and opens a war room "
          "at Gatewood. Watching costs fuel, overtime and nerves; ignoring the war would cost far more.",
          ('communications', 'security'), requires=(After('1995.3.25'),), reward=(Idea('border_watch'), Event('belkan_war'))),
    Focus('bord_court_debate', 'The Court Weighs the Old Alliance',
          "The court has always spoken of Belka as a brother nation, and some officers talk openly about helping it. Others "
          "remember that Osea sits on the Serenava frontier. The debate is held in closed session, and its record decides what "
          "the kingdom says in public. Any armed intervention remains a separate and grave decision outside this debate.",
          ('assembly', 'diplomacy'), after=('bord_news',), reward=(Event('old_alliance'),)),
    Focus('bord_refugee_posts', 'Posts for Those Who Flee',
          "War on the continent will send people looking for safety, and some will reach the kingdom by sea or over land. "
          "Reception posts at the main crossings and harbours register arrivals, give them food and a bed, and decide where "
          "they go next. The posts cost money and invite argument. Without them, arrivals become a crisis instead of a task.",
          ('refugees', 'shelter'), after=('bord_news',), reward=(Flag('refugee_posts'), Stability(-0.02))),
    Focus('bord_frontier_bunkers', 'Man the Serenava Bunkers',
          "The bunker lines along the Serenava frontier were built for a war with Osea that never came. The frontier divisions "
          "reoccupy them, clear their fields of fire and wire them to new radar posts. Osea will notice, and the move costs "
          "goodwill on the far side of the line. The kingdom would rather be noticed than surprised.",
          ('security', 'radar'), after=('bord_news',), requires=(HasFlag('northern_line'),),
          reward=(Build('radar_station', 1, 581), WarSupport(0.03))),
    Focus('bord_stance_belka', 'Keep Faith with Old Friends',
          "The crown declares public sympathy for Belka, keeps its envoys in place and lets the Gatewood munitions branch fill "
          "Belkan orders under existing contracts. No Perblan unit crosses any border. Osea will treat the kingdom as an "
          "unfriendly neighbour for years. The officer corps and the arms trusts approve, and the ports fear for their trade.",
          ('diplomacy', 'medal'), after=('bord_court_debate',), cost=10, exclusive=('bord_stance_neutral', 'bord_stance_osea'),
          reward=(SwapIdea('border_watch', 'old_friendship'), Flag('stance_belka'),
                  Tooltip('Commits no troops. Any armed intervention remains the separate inherited Belkan decision path.'))),
    Focus('bord_stance_neutral', 'Neither Banner Nor Border',
          "The crown proclaims armed neutrality: no arms to either side, no transit for foreign troops and full readiness on "
          "every frontier. It satisfies nobody and protects everyone. Belka will call it betrayal, Osea will call it suspicious, "
          "and the readiness bill will run for as long as the war does. The kingdom stays its own master.",
          ('security', 'peace'), after=('bord_court_debate',), cost=10, exclusive=('bord_stance_belka', 'bord_stance_osea'),
          reward=(SwapIdea('border_watch', 'armed_neutrality'), Flag('stance_neutral'))),
    Focus('bord_stance_osea', 'A Quiet Channel to Osea',
          "The foreign ministry opens a discreet channel to Osea, promising that Perbla will not let its territory or factories "
          "serve the war against it. In return, trade across the frontier continues. The court's Belkan sympathisers call it a "
          "betrayal of a century of friendship. The ports and the converted plants keep their customers.",
          ('diplomacy', 'communications'), after=('bord_court_debate',), cost=10, exclusive=('bord_stance_belka', 'bord_stance_neutral'),
          reward=(SwapIdea('border_watch', 'osean_channel'), Flag('stance_osea'))),
    Focus('bord_branch_orders', 'Orders for the Gatewood Branch',
          "Belkan contracts placed with the munitions branch at Gatewood are honoured in full, and the crown lets the branch add "
          "a production line. Jobs and foreign currency follow. Every crate shipped is a fact Osea will remember. The trusts "
          "insist the orders are only business; the frontier divisions know that business has a return address.",
          ('industry', 'missile'), after=('bord_stance_belka',), reward=(Build('arms_factory', 1, 389),)),
    Focus('bord_frontier_patrols', 'Patrols Along Every Frontier',
          "Neutral patrols fly along every frontier and coast, reporting any foreign aircraft that strays into Perblan airspace. "
          "The northern Terentio state receives a new radar post to close a gap in coverage. The patrols burn fuel and airframe "
          "hours. They also make neutrality visible, which is the only kind of neutrality anyone respects.",
          ('air', 'security'), after=('bord_stance_neutral',), reward=(Build('radar_station', 1, 209), XP('air', 15))),
    Focus('bord_crossings_open', 'Keep the Crossings Open',
          "Border posts on the Serenava frontier stay open for trucks, rail freight and families, with extra customs officers "
          "to keep war contraband out. Repairs to the frontier roads make the crossings faster. Trade keeps flowing and the "
          "frontier towns stay calm. Belkan sympathisers at court see every open gate as a favour to the enemy.",
          ('rail', 'diplomacy'), after=('bord_stance_osea',), reward=(Build('infrastructure', 1, 581), Stability(0.02))),
    Focus('bord_raid_drills', 'Air Raid Drills in Sofern',
          "Sofern is the largest city and port in the kingdom, and its people have never practised for an air raid. Civil "
          "defence wardens run sirens, blackouts and shelter drills, and the harbour gets an extra radar post. The drills "
          "frighten shopkeepers and slow the port for a week. They also make the war feel real to those who must survive it.",
          ('shelter', 'radar'), after_any=('bord_frontier_bunkers', 'bord_refugee_posts'),
          reward=(Build('radar_station', 1, 236), WarSupport(0.03))),
    Focus('bord_stand_down', 'Stand the Frontier Down',
          "Once the court judges that the fighting no longer threatens Perblan soil, the frontier commands return to peacetime "
          "rotations and reservists go home. The war room at Gatewood closes and its files go to the archive. Standing down too "
          "early would be reckless; standing down too late keeps factories short of workers.",
          ('peace', 'document'), after_any=('bord_branch_orders', 'bord_frontier_patrols', 'bord_crossings_open'),
          requires=(After('1996.1.1'),), reward=(Flag('frontier_stood_down'), Stability(0.03))),
))

AIR = Branch('air', 'The Serenava Air Arm', 1993, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_count', 'Count the Air Arm Airframes',
          "The air arm is small, old and concentrated on the giant Serenava airfields that face Osea. An honest count shows how "
          "many fighters can actually fly, how many pilots are current and how much fuel the stores hold. The answer "
          "embarrasses the air staff. It also gives the crown a real baseline for every later decision.",
          ('air', 'document'), reward=(Idea('serenava_wing'),)),
    Focus('air_pilot_school', 'A Pilot School at Gatewood',
          "Pilots have trained in their squadrons, each with its own habits. A central school near the capital standardises "
          "flying, navigation and gunnery, and graduates move between units without retraining. The school takes instructors "
          "out of frontline squadrons for its first two years. After that, every pilot in the arm speaks the same language.",
          ('training', 'air'), after=('air_count',), reward=(XP('air', 20), Research('air_doctrine', 0.5, 1))),
    Focus('air_dispersal', 'Dispersal Fields in Old Perbla',
          "Everything the kingdom owns in the air sits on a handful of fields in Serenava, where one bad morning could end the "
          "air arm. Dispersal strips in the Old Perbla heartland give squadrons somewhere to go. They are rough fields with fuel "
          "bladders and tents, cheap to build, miserable to operate and much harder to destroy at once.",
          ('runway', 'security'), after=('air_count',), reward=(Build('air_base', 2, 601),)),
    Focus('air_interceptors', 'Interceptors Over the Crown Lands',
          "The air staff chooses defence: interceptors, ground control and fast reaction from hardened fields. The arm's purpose "
          "becomes keeping foreign aircraft out of Perblan skies rather than supporting distant ground battles. The army loses "
          "its promised air support. The kingdom gains an air arm that can credibly deny its airspace to a larger neighbour.",
          ('air', 'radar'), after=('air_pilot_school',), cost=10, exclusive=('air_strike',),
          reward=(SwapIdea('serenava_wing', 'interceptor_arm'),)),
    Focus('air_strike', 'Strike Wings for the Army',
          "The air staff chooses to support the army: strike aircraft, forward controllers and joint training with the frontier "
          "divisions. The arm becomes the army's long-range artillery, and air defence falls back on ground guns and luck. The "
          "army is delighted. The treasury notes that strike munitions cost more each year than interceptor fuel.",
          ('air', 'missile'), after=('air_pilot_school',), cost=10, exclusive=('air_interceptors',),
          reward=(SwapIdea('serenava_wing', 'strike_arm'),)),
    Focus('air_spares', 'Spares from Gatewood Electronics',
          "Grounded aircraft usually wait for one imported part. A domestic spares programme gives Gatewood suppliers the "
          "drawings for radios, instruments and wiring looms and pays them to stock replacements. Readiness rises within a year. "
          "Foreign makers grumble about licences, and the air arm grows more tied to the national electronics sector.",
          ('tools', 'communications'), after=('air_dispersal',), reward=(Research('electronics', 0.5, 1), XP('air', 10))),
    Focus('air_reserve_pilots', 'Reserve Pilots from Civil Flying',
          "Civil flying clubs and airline crews join an air reserve, training on light aircraft at the Sofern field and "
          "reporting for refresher flying each summer. In a crisis they ferry aircraft, fly liaison missions and free regular "
          "pilots for combat. The reserve costs little. It also gives thousands of citizens a stake in the air arm.",
          ('runway', 'training'), after=('air_pilot_school',), reward=(Build('air_base', 1, 236), XP('air', 15))),
    Focus('air_radar_chain', 'A Radar Chain for the Air Arm',
          "A chain of linked radar posts across Serenava feeds a single control room, so that the air arm sees intruders minutes "
          "earlier than before. Gatewood engineers build most of the sets. The chain is expensive and needs constant "
          "calibration. Without it, even the best pilots are scrambled late and blind.",
          ('radar', 'air'), after_any=('air_interceptors', 'air_strike'), reward=(Build('radar_station', 2, 581),)),
    Focus('air_crown_review', 'The Crown Air Review',
          "Every squadron flies over Gatewood for a public review, with open hangars, school visits and a recruiting fair. It is "
          "theatre, and expensive theatre, burning fuel and maintenance hours on a parade. It also lifts the arm's morale, fills "
          "the pilot school's waiting list and shows neighbours that the kingdom's aircraft can fly together.",
          ('medal', 'air'), after_any=('air_radar_chain', 'air_spares'), reward=(TimedIdea('air_day', 365), XP('air', 15))),
))

COAST = Branch('coast', 'Sofern and the Coast', 1993, 'FOCUS_FILTER_NAVY_XP', (
    Focus('coast_yards', 'Sofern Yards Back to Work',
          "Sofern's yards build and repair almost every hull the kingdom owns, but half the slipways stand idle for lack of "
          "orders. A steady programme of refits and small escorts keeps the yards working and their skilled crews employed. The "
          "navy gets ships back faster. The treasury commits to a shipbuilding budget it cannot easily cut later.",
          ('navy', 'tools'), reward=(Idea('sofern_squadron'), XP('navy', 10))),
    Focus('coast_baleton', 'Harbour Works at Baleton',
          "Baleton, the naval harbour near the capital, has deep berths but a road and rail link built for a smaller fleet. "
          "Widening the quays and rebuilding the access roads lets ships load and repair in days rather than weeks. Commuters "
          "in the capital district suffer a year of closures. The navy finally gets a proper home port.",
          ('bridge', 'navy'), after=('coast_yards',), reward=(Build('infrastructure', 1, 389),)),
    Focus('coast_escorts', 'Escorts for the Convoy Lanes',
          "The kingdom's trade moves by sea, and its convoys sail with little protection. Small escorts with sonar, guns and "
          "depth charges join each convoy on the main lanes, and crews train on real routes rather than exercises. Escorts are "
          "unglamorous ships, and they are the ones a trading kingdom needs most when a war breaks out nearby.",
          ('navy', 'logistics'), after=('coast_yards',), reward=(XP('navy', 20), Research('naval_equipment', 0.5, 1))),
    Focus('coast_submarines', 'A Submarine Screen',
          "The navy decides that a few coastal submarines can make any approach dangerous for a stronger fleet. Sofern "
          "specialises in building and maintaining them, and crews train in the coastal shallows they would defend. Submarines "
          "are cheap deterrence. They cannot escort a convoy or show the flag, and merchants notice the difference.",
          ('submarine', 'navy'), after=('coast_escorts',), cost=10, exclusive=('coast_surface',),
          reward=(SwapIdea('sofern_squadron', 'submarine_screen'),)),
    Focus('coast_surface', 'Surface Escort Flotillas',
          "The navy decides that protecting trade matters more than threatening invaders. Sofern builds flotillas of surface "
          "escorts and the navy organises them around the main convoy lanes. The ships are visible at sea and in foreign ports. "
          "They are also easier targets, and the escort budget grows with every route merchants open.",
          ('navy', 'security'), after=('coast_escorts',), cost=10, exclusive=('coast_submarines',),
          reward=(SwapIdea('sofern_squadron', 'escort_flotillas'),)),
    Focus('coast_watch_office', 'Coastal Watch at the Harbour',
          "The harbour district of Perbla proper gets a coastal radar and a watch office that tracks shipping, smugglers and "
          "fishing boats in all weather. The navy and customs share the data. The station costs little, but staffing it around "
          "the clock does not. It ends the old practice of learning about arrivals when they dock.",
          ('radar', 'navy'), after=('coast_baleton',), reward=(Build('radar_station', 1, 592),)),
    Focus('coast_fishery', 'Fishery Patrols',
          "Fishing towns along the coast lose catches to foreign trawlers working inside Perblan waters. Patrol boats enforce "
          "the limits, and the harbour roads are rebuilt so catches reach markets fresh. Crews gain sea time on real missions. "
          "Trawler owners protest to their governments, and the foreign ministry spends a year answering their notes.",
          ('fishing', 'navy'), after=('coast_escorts',), reward=(Build('infrastructure', 1, 592), XP('navy', 10))),
    Focus('coast_marines', 'Marine Battalions at Sofern',
          "The marines are scattered in harbour guard companies. Gathering them into battalions at Sofern, with landing craft "
          "and joint drills alongside the navy, gives the kingdom a force that can secure its own ports and coast quickly. "
          "Marines draw the best volunteers away from the army. Their real value is speed when a harbour needs holding.",
          ('navy', 'training'), after_any=('coast_submarines', 'coast_surface'),
          reward=(Research('engineers_tech', 0.5, 1), XP('navy', 15))),
    Focus('coast_merchant_register', 'A Merchant Fleet Register',
          "Every Perblan merchant ship is listed with its owner, crew, cargo type and the routes it sails. In peacetime the "
          "register is a customs tool. In a crisis it tells the navy which ships to protect, which to recall and which could "
          "be requisitioned. Owners dislike the paperwork, and a few reflag their ships abroad.",
          ('document', 'logistics'), after=('coast_watch_office',), reward=(Flag('merchant_register'), Stability(0.02))),
))

AFTERMATH = Branch('aftermath', 'After the War Years', 1996, 'FOCUS_FILTER_STABILITY', (
    Focus('after_relief', 'Open the Relief Offices',
          "The war years leave the kingdom with displaced families, returning reservists and businesses that lost foreign "
          "customers. Relief offices in each crown land handle housing, jobs and small grants under one roof. They cost money "
          "and attract complaints from every side. They also turn scattered grievances into cases that can be closed.",
          ('refugees', 'civil'), reward=(TimedIdea('relief_offices', 540),)),
    Focus('after_new_homes', 'From Reception Posts to Homes',
          "People who arrived at the wartime reception posts still live in temporary halls. The crown funds housing and roads "
          "on the edge of the Relentio valley towns, where factories need workers. Newcomers become tenants and taxpayers rather "
          "than wards. Some councils resent the arrivals, and the programme must be defended every budget year.",
          ('shelter', 'rebuild'), after=('after_relief',), requires=(HasFlag('refugee_posts'),),
          reward=(Build('infrastructure', 1, 173),)),
    Focus('after_reservists_home', 'Send the Reservists Home',
          "With the frontier stood down, the last reservists return to civilian life with a bonus, a job placement and their "
          "old posts protected by law. A closed plant in northern Relentio reopens with returning workers. Employers grumble "
          "about the protected posts, and the towns are glad to have their sons and daughters back.",
          ('peace', 'training'), after=('after_relief',), requires=(HasFlag('frontier_stood_down'),),
          reward=(Build('industrial_complex', 1, 597), Stability(0.03))),
    Focus('after_veterans', 'Pensions for Service Veterans',
          "Veterans of the war-year mobilisations ask for pensions, medical care and priority in civil service hiring. The crown "
          "grants a modest package funded by a small levy on arms exports. Veterans' clubs become loyal to the government that "
          "paid them. The levy angers the trusts, and future governments inherit a promise they cannot reduce.",
          ('medal', 'medical'), after=('after_reservists_home',), reward=(Stability(0.03), PP(-25))),
    Focus('after_ulysses', 'Ulysses in the Night Sky',
          "The asteroid Ulysses is now a fixed subject of every bulletin, with warnings that fragments will strike the Earth "
          "within a few years. The kingdom cannot change the asteroid's path, only its own readiness. The crown convenes "
          "scientists, engineers and civil defence officials to decide what readiness means and what it will cost.",
          ('meteor', 'telescope'), after=('after_relief',), requires=(After('1996.4.20'),), reward=(Event('ulysses'),)),
    Focus('after_shelters', 'Shelters Under the Cities',
          "The civil defence school wants deep shelters under Gatewood, Sofern and the other large towns, stocked with water and "
          "power for weeks. Crews and steel are diverted from industry for years. If debris ever falls near the kingdom, "
          "millions have somewhere to go. If it never does, the kingdom will own very expensive basements.",
          ('shelter', 'civil'), after=('after_ulysses',), cost=10, exclusive=('after_warning',), reward=(Idea('deep_shelters'),)),
    Focus('after_warning', 'An Early Warning Network',
          "The scientific school argues that warning time saves more lives than concrete. An observatory link, radar posts and "
          "a national siren network would give each district hours of notice, with evacuation plans instead of bunkers. It is "
          "cheaper and smarter, and useless if the warning comes and nobody has anywhere safe to go.",
          ('telescope', 'radar'), after=('after_ulysses',), cost=10, exclusive=('after_shelters',),
          reward=(Idea('early_warning'), Build('radar_station', 1, 389))),
    Focus('after_arklith_roads', 'Trade Roads to Arklith',
          "Wartime caution froze trade with every neighbour, including Arklith on the western frontier. Reopening customs posts "
          "and rebuilding the western valley roads restores a modest but steady market for Perblan goods. Arklith's traders "
          "want lower tariffs in return. The deal is small, peaceful and unglamorous, which is what the economy needs.",
          ('logistics', 'diplomacy'), after=('after_relief',), reward=(Build('infrastructure', 1, 112), Stability(0.02))),
    Focus('after_osean_thaw', 'A Thaw with Osea',
          "The quiet wartime channel to Osea becomes an open trade and transit agreement once the fighting ends. Osean buyers "
          "return to Perblan ports and factories, and the frontier towns prosper. The court's Belkan sympathisers call it the "
          "price of betrayal. Ministers call it the reward for keeping a promise when keeping it was hard.",
          ('diplomacy', 'peace'), after=('after_relief',), requires=(HasFlag('stance_osea'),),
          exclusive=('after_belkan_ties', 'after_neutral_dividend'), reward=(SwapIdea('osean_channel', 'osean_trade'),)),
    Focus('after_belkan_ties', 'Help for Belkan Friends',
          "The kingdom keeps faith with Belka after the war, offering credit, contracts for the Gatewood munitions branch and "
          "university places for Belkan students. Old friendships deepen. Osea notes every gesture and keeps its frontier "
          "posture stiff for years. The arms trusts welcome the business, and the ports pay for the chill.",
          ('diplomacy', 'rebuild'), after=('after_relief',), requires=(HasFlag('stance_belka'),),
          exclusive=('after_osean_thaw', 'after_neutral_dividend'), reward=(SwapIdea('old_friendship', 'belkan_ties'),)),
    Focus('after_neutral_dividend', 'The Neutrality Dividend',
          "Having refused both sides, the kingdom markets itself as a neutral venue for talks, banking and shipping. Its "
          "harbours handle cargo with fewer questions, and its diplomats host meetings both sides need. Neutrality pays modest "
          "dividends. It also requires a frontier army credible enough that nobody tests whether the crown means it.",
          ('peace', 'scales'), after=('after_relief',), requires=(HasFlag('stance_neutral'),),
          exclusive=('after_osean_thaw', 'after_belkan_ties'), reward=(SwapIdea('armed_neutrality', 'neutral_standing'),)),
))

DESERT = Branch('desert', 'Terentio Oil and Ore', 2000, 'FOCUS_FILTER_INDUSTRY', (
    Focus('desert_survey', 'Survey the Terentio Fields',
          "The Terentio desert holds oil and bauxite that the kingdom has barely tapped, worked by a few old rigs and the arms "
          "plants that sit on the same ground. A geological survey maps the fields properly and rebuilds the track to the main "
          "deposits. The survey takes two dry seasons, and its maps will decide who gets rich.",
          ('tools', 'economy'), reward=(Event('desert_oil'), Build('infrastructure', 1, 571))),
    Focus('desert_pipeline', 'Pipelines and Water Wells',
          "Oil fields need water, roads and pipelines before they need drillers. The crown lays a pipeline corridor from the "
          "desert to Torre Mountain, where the refineries and smelters will sit, and drills wells for the towns along it. The "
          "corridor is slow to build. Once it exists, every later desert project costs less.",
          ('bridge', 'tools'), after=('desert_survey',), reward=(Build('infrastructure', 1, 207),)),
    Focus('desert_crown_oil', 'A Crown Oil Company',
          "A state oil company holds every Terentio lease and pays its profits into the treasury. Drilling is slower, because "
          "the company is cautious and politically managed, but the revenue stays at home. The crown gains a second income "
          "besides arms, and another national champion that must be rescued if it ever stumbles.",
          ('economy', 'command'), after=('desert_survey',), cost=10, exclusive=('desert_concessions',),
          reward=(Idea('terentio_crown_oil'),)),
    Focus('desert_concessions', 'Concessions to Private Drillers',
          "The crown auctions drilling concessions to private firms, domestic and foreign, for royalties and local hiring rules. "
          "Rigs go up quickly and the fields produce within a few years. Royalties are smaller than full ownership, and "
          "Terentio's towns will deal with managers who answer to shareholders rather than to Gatewood.",
          ('economy', 'tools'), after=('desert_survey',), cost=10, exclusive=('desert_crown_oil',),
          reward=(Idea('terentio_concessions'),)),
    Focus('desert_land_share', 'A Share for the Desert Land',
          "Under its crown land charter, Terentio's diet claims a fixed share of oil revenue for its own budget. The crown "
          "agrees, and the land spends its first share on a workshop district in its northern towns. Gatewood receives less. The "
          "desert finally sees oil money building things where the oil is, and its loyalty firms up.",
          ('scales', 'civil'), after_any=('desert_crown_oil', 'desert_concessions'), requires=(HasFlag('lands_devolved'),),
          reward=(Build('industrial_complex', 1, 209), Stability(0.03))),
    Focus('desert_chancery_royalty', 'Royalties to the Chancery',
          "The single chancery collects all oil royalties centrally and allocates them by national plan. Its first allocation "
          "funds an industrial park in the northern Terentio state, chosen by Gatewood rather than by the desert towns. Revenue "
          "is larger and easier to steer. Local notables complain that the wealth flows past them to the capital.",
          ('command', 'economy'), after_any=('desert_crown_oil', 'desert_concessions'), requires=(HasFlag('lands_centralised'),),
          reward=(Build('industrial_complex', 1, 209), PP(40))),
    Focus('desert_shared_revenue', 'Desert Revenues Shared',
          "The Crown Lands Accord already fixes how revenue is shared, so oil income is split by formula between the treasury "
          "and all four lands. Old Perbla uses its share to repair the heartland roads. Nobody gets everything they want, and "
          "nobody can claim the desert's money was taken by stealth, which keeps the union quiet.",
          ('scales', 'assembly'), after=('desert_survey',), requires=(HasFlag('lands_accord_set'),),
          reward=(Build('infrastructure', 1, 601), Stability(0.03))),
    Focus('desert_smelters', 'Smelters in the Western Valley',
          "Bauxite from the desert and steel from the western valley mines meet at a new smelter complex on the Arklith "
          "road. Aluminium can be rolled at home instead of shipped out as ore. The smelters need enormous power and years "
          "of debt. They give the air arm and the electronics sector a domestic metal supply.",
          ('industry', 'tools'), after=('desert_pipeline',), reward=(Build('industrial_complex', 1, 112),)),
    Focus('desert_fuel_research', 'Fuel Research at Gatewood',
          "Gatewood's laboratories and the oil sector fund joint research on refining, lubricants and synthetic fuels from the "
          "desert's heavier crude. The army wants fuel independence and the firms want higher margins. Results come slowly and "
          "the budget is easy to cut, but every point of yield gained stays in the kingdom.",
          ('science', 'industry'), after_any=('desert_crown_oil', 'desert_concessions'),
          reward=(Research('synth_resources', 0.5, 1), Research('excavation_tech', 0.5, 1))),
    Focus('desert_railway', 'A Railway Across the Desert',
          "A heavy railway links the desert fields and the smelters to the coast, replacing convoys of tanker trucks on bad "
          "roads. Freight costs fall and the army gains a fast supply line inland. The railway is the largest civil project in "
          "the kingdom's recent history, and its debt will outlast the ministers who opened it.",
          ('rail', 'logistics'), after=('desert_smelters',), reward=(Build('infrastructure', 1, 571), Build('infrastructure', 1, 207), Research('train_tech', 0.5, 1))),
))

MILLENNIUM = Branch('millennium', 'The Kingdom at the Millennium', 2003, 'FOCUS_FILTER_POLITICAL', (
    Focus('mill_review', 'Ten Years of the New Order',
          "A decade after the crown question was first opened, the government commissions a public review of how the kingdom "
          "governs itself: what it built, whom it failed and what it now costs to run. The panel is chosen by lot rather than "
          "from the government's friends. Its findings will frame every political choice of the new century.",
          ('document', 'ballot'), reward=(Event('decade_review'),)),
    Focus('mill_parliament', 'A Constitution in One Volume',
          "The ministry consolidates a century of charters, conventions and court rulings into one written constitution, "
          "ratified by the chamber and signed by the crown. Disputes that once needed palace mediation go to a constitutional "
          "court. Drafting takes two sessions and every clause becomes a battle. The result is a government nobody must guess about.",
          ('document', 'scales'), after=('mill_review',), requires=(HasFlag('path_parliament'),),
          exclusive=('mill_privy', 'mill_order', 'mill_assembly'), reward=(SwapIdea('ministry_charter', 'settled_constitution'),)),
    Focus('mill_privy', 'The Prerogative Written Down',
          "The privy council records exactly which powers the throne holds, which it delegates and which the chamber may still "
          "debate. Clarity strengthens the council: no minister can plead confusion, and no deputy can claim a right the text "
          "omits. Critics call it absolutism with an index. Investors call it predictable, and that wins the argument.",
          ('command', 'medal'), after=('mill_review',), requires=(HasFlag('path_privy'),),
          exclusive=('mill_parliament', 'mill_order', 'mill_assembly'), reward=(SwapIdea('privy_seal', 'crown_prerogative'),)),
    Focus('mill_order', 'The Ordered Kingdom',
          "The directorate replaces emergency decrees with a permanent code of public order, giving its police, censors and "
          "labour boards a legal footing. Strikes vanish from the arms towns and crime falls. Talented people quietly leave for "
          "jobs abroad, and those who stay learn to say less. The kingdom is orderly, efficient and noticeably quieter.",
          ('security', 'medal'), after=('mill_review',), requires=(HasFlag('path_order'),),
          exclusive=('mill_parliament', 'mill_privy', 'mill_assembly'), reward=(SwapIdea('order_decrees', 'ordered_kingdom'),)),
    Focus('mill_assembly', 'The Federal Parliament Act',
          "The assembly government passes a federal act creating two chambers, one elected by population and one by the four "
          "crown lands, with the crown kept as a symbol of their union. Lawmaking slows, but the outer lands finally hold a "
          "formal veto. The arrangement is clumsy, durable and hard for any single faction to capture.",
          ('assembly', 'scales'), after=('mill_review',), requires=(HasFlag('path_assembly'),),
          exclusive=('mill_parliament', 'mill_privy', 'mill_order'), reward=(SwapIdea('assembly_mandate', 'federal_parliament'),)),
    Focus('mill_civil_exam', 'A Civil Service Examination',
          "Ministries in Gatewood still hire through family, regiment and party. A single competitive examination for every "
          "civil service post opens careers to graduates from all four lands. Years pass before the new intake reaches senior "
          "posts. Meanwhile the examined juniors outperform their patrons, which quietly makes it the most popular reform.",
          ('document', 'training'), after=('mill_review',),
          reward=(Stability(0.02), PP(30), Tooltip('Ministries hire by open examination from this point on.'))),
    Focus('mill_public_accounts', 'A Public Accounts Act',
          "The published arms audit of the early nineties set a precedent, and this act makes it law: every crown contract above "
          "a set value is published with its price, supplier and delivery date. Suppliers grumble about exposure. Overpriced "
          "bids fall within a year, and the press finds fewer scandals because there are fewer secrets.",
          ('scales', 'document'), after=('mill_review',), requires=(HasFlag('audit_published'),), reward=(Idea('public_accounts'),)),
    Focus('mill_industry_review', 'The Industrial Model Revisited',
          "Ten years after the industrial reckoning, the treasury asks whether the chosen model still fits. It walks the plants "
          "again, this time measuring exports, wages and dependence rather than waste, and funds a new hall in northern "
          "Relentio as a test case. The review costs a year of argument with every trust in the kingdom.",
          ('industry', 'scales'), after=('mill_review',),
          reward=(Build('industrial_complex', 1, 597), Research('industry', 0.5, 1))),
    Focus('mill_civil_board', 'A Civil Works Board',
          "Ten years of conversion have produced trucks, tractors and appliances, and a generation of workers who never made a "
          "shell. Protection for converted plants ends, replaced by a works board that funds exports and modernisation. Weak "
          "plants will close. The strong ones finally compete on their own merits, which was the point all along.",
          ('rebuild', 'economy'), after=('mill_industry_review',), requires=(HasFlag('model_conversion'),),
          exclusive=('mill_arsenal_contracts', 'mill_circuit_exports'), reward=(SwapIdea('plowshare_works', 'civil_works_board'),)),
    Focus('mill_arsenal_contracts', 'Long Contracts for the Arsenal',
          "The export board moves from single sales to long service contracts that bundle weapons, spares, training and upgrades "
          "over decades. Revenue becomes steady and the arms lines plan years ahead. Every long contract also ties the kingdom "
          "to the conduct of its customers, and scrutiny of sales becomes the hottest political question in Gatewood.",
          ('missile', 'document'), after=('mill_industry_review',), requires=(HasFlag('model_arsenal'),),
          exclusive=('mill_civil_board', 'mill_circuit_exports'), reward=(SwapIdea('southern_arsenal', 'arsenal_contracts'),)),
    Focus('mill_circuit_exports', 'Circuits for Foreign Markets',
          "The component economy has matured enough to sell abroad. Gatewood suppliers win foreign contracts for sensors, "
          "control boards and communications equipment, backed by crown export credit. The national firm remains the anchor, "
          "but it no longer carries the whole sector. Foreign competitors respond with price cuts and lawsuits.",
          ('communications', 'diplomacy'), after=('mill_industry_review',), requires=(HasFlag('model_circuits'),),
          exclusive=('mill_civil_board', 'mill_arsenal_contracts'), reward=(SwapIdea('circuit_economy', 'circuit_exports'),)),
    Focus('mill_firm_stress', 'Stress Test the Electronics Firm',
          "Treasury officials run the sealed rescue plan as a full exercise, assuming the electronics firm misses its payroll on "
          "a Monday morning. Banks, suppliers and the defence staff all take part. The exercise exposes gaps that a real crisis "
          "would have found first. Word leaks, and the firm's investors spend a nervous week.",
          ('economy', 'shelter'), after=('mill_industry_review',), requires=(HasFlag('firm_rescue_plan'),),
          reward=(Event('firm_stress'),)),
    Focus('mill_shock_cushion', 'Draw on the Shock Reserve',
          "The industrial shock reserve has grown untouched for a decade. Rather than spend it on promises, the government uses "
          "a slice to retool the oldest plants in Sofern before they fail on their own, and the rest stays in reserve. Every "
          "party has a better idea for the money, and the reserve's board must defend it.",
          ('economy', 'scales'), after=('mill_industry_review',), requires=(HasFlag('shock_reserve'),),
          reward=(Build('industrial_complex', 1, 236), PP(20))),
    Focus('mill_second_sources', 'Second Sources Pay Off',
          "The second-source rule for defence parts, once mocked as duplication, has produced a ring of capable suppliers around "
          "the harbour district. One of them is now large enough to run a small arms line in a Serenava garrison town. Prices stay higher than a "
          "monopoly would charge, and nobody in the defence staff misses the old single point of failure.",
          ('tools', 'science'), after=('mill_industry_review',), requires=(HasFlag('second_source'),),
          reward=(Build('arms_factory', 1, 581), Research('electronics', 0.5, 1))),
))

NEIGHBOUR = Branch('neighbour', 'A Neighbour at War', 2010, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('pac_news', 'Osea Goes to War',
          "In September 2010 Osea, the large neighbour the service year was built to match, is suddenly at war with Yuktobania. "
          "The kingdom is not a belligerent, but Osean ports, buyers and warships are part of its daily life. The security "
          "council convenes to judge what the war means for Perblan trade, shipping and safety.",
          ('communications', 'navy'), requires=(After('2010.9.27'),), reward=(Event('pacific_war'),)),
    Focus('pac_harbour_guard', 'Guard the Neutral Harbours',
          "Warring navies and their submarines make every sea lane nervous, and Perblan harbours handle cargo for peaceful and "
          "warlike customers alike. Naval police inspect suspicious ships, harbour defences go on alert and the coast watch "
          "doubles its shifts. The measures slow trade and cost overtime, and they keep the ports from becoming targets.",
          ('security', 'navy'), after=('pac_news',), reward=(Idea('harbour_guard'),)),
    Focus('pac_supply_osea', 'Sell to the Osean War Effort',
          "Osean buyers want trucks, electronics and munitions at once, and they pay well. The government lets Perblan firms "
          "take the orders under export rules that bar weapons to any other belligerent. Factories run three shifts. "
          "Yuktobania notes the sales, and prosperity now depends partly on a war the kingdom did not choose.",
          ('industry', 'diplomacy'), after=('pac_news',), cost=10, exclusive=('pac_stay_clear',),
          requires=(NotFlag('stance_belka'),), reward=(Idea('wartime_orders'),)),
    Focus('pac_stay_clear', 'Stay Clear of the Pacific',
          "The government refuses military sales to any party in the war and limits its role to humanitarian shipping and "
          "diplomacy. Osean buyers go elsewhere, and some frontier businesses suffer. The kingdom's reputation for distance "
          "grows. When the war ends, nobody has a grievance against Perbla, which may prove worth more than the lost orders.",
          ('peace', 'scales'), after=('pac_news',), cost=10, exclusive=('pac_supply_osea',), reward=(Idea('pacific_distance'),)),
    Focus('pac_three_shifts', 'Three Shifts in the Arms Halls',
          "Wartime orders fill the old arms halls in the Relentio valley, and a new line opens to meet Osean demand for shells "
          "and spares. Workers earn overtime and the trusts post record profits. Everyone knows that orders like these vanish "
          "when the war ends, and ministers warn the trusts not to borrow as though the demand will last.",
          ('industry', 'missile'), after=('pac_supply_osea',), reward=(Build('arms_factory', 1, 173), WarSupport(0.02))),
    Focus('pac_relief_ships', 'Relief Ships for the War Zone',
          "Perblan hospital ships and grain freighters sail under neutral colours to ports on both sides of the war, carrying "
          "medicine and food rather than munitions. The crews take real risks, and the voyages cost the treasury without "
          "earning anything. They give the kingdom a reputation as an honest broker that its diplomats will spend for years.",
          ('medical', 'navy'), after=('pac_stay_clear',), reward=(SwapIdea('pacific_distance', 'good_offices'),)),
    Focus('pac_merchant_recall', 'Call Up the Merchant Register',
          "The merchant register compiled in the nineties proves its worth: every Perblan ship in a dangerous lane is known, "
          "routed and warned. Ships near the war zone are recalled, and a new coastal watch post in northern Relentio tracks "
          "them home. Owners complain about lost voyages. The aim is that no Perblan crew becomes a casualty of this war.",
          ('logistics', 'document'), after=('pac_harbour_guard',), requires=(HasFlag('merchant_register'),),
          reward=(Build('radar_station', 1, 597), XP('navy', 15))),
    Focus('pac_lessons', 'Lessons from the Osean War',
          "Perblan officers study the war next door closely: the submarines, the air battles over cities and the vulnerability "
          "of ports and carriers to determined attack. A joint study recommends more air defence, dispersed bases and smaller, "
          "more numerous ships. It is uncomfortable for admirals with big-ship plans, and the cheapest lesson the kingdom will buy.",
          ('command', 'document'), after_any=('pac_three_shifts', 'pac_relief_ships', 'pac_merchant_recall'),
          requires=(After('2011.1.1'),), reward=(Research('air_doctrine', 0.5, 1), Research('naval_equipment', 0.5, 1))),
    Focus('pac_capital_defence', 'Air Defence for the Capital',
          "Following the study, Gatewood receives a modern air defence network of radars and missile batteries linked to the "
          "air arm's control room. The capital had relied on fighters alone. The batteries are expensive and their crews need a "
          "year to train. The capital district can now defend itself while the fighters are elsewhere.",
          ('radar', 'security'), after=('pac_lessons',), reward=(Build('radar_station', 2, 389),)),
))

NETWORK = Branch('network', 'The Network Years', 2016, 'FOCUS_FILTER_RESEARCH', (
    Focus('net_national', 'A National Data Network',
          "Ministries, banks, factories and military commands now run on networks that depend on foreign satellites and "
          "undersea cables. A national data network with domestic routing and backup links keeps essential services online "
          "under pressure. Building it takes years of digging and fibre. The electronics sector wins most contracts, and "
          "complains about the deadlines anyway.",
          ('communications', 'satellite'), reward=(Idea('national_network'),)),
    Focus('net_ground_stations', 'Satellite Ground Stations',
          "Ground stations in the Old Perbla heartland receive weather, navigation and communications data from leased satellite "
          "capacity. The kingdom does not own a satellite, but it controls its own antennas, receivers and data. Leases are "
          "expensive. The stations also train the engineers the kingdom would need if it ever launched something of its own.",
          ('satellite', 'radar'), after=('net_national',), reward=(Build('radar_station', 1, 601),)),
    Focus('net_sounding_rockets', 'A Sounding Rocket Programme',
          "Gatewood engineers launch small sounding rockets from the Terentio desert to test sensors and train launch crews. It "
          "is a modest programme, far from orbit. Neighbours ask pointed questions about missiles, and the foreign ministry "
          "answers them carefully. The programme keeps rocket skills at home without promising a space programme.",
          ('missile', 'science'), after=('net_ground_stations',), reward=(Research('rocketry', 0.5, 1), Research('electronics', 0.5, 1))),
    Focus('net_export_park', 'Electronics for the Wider World',
          "The electronics sector has grown from one famous firm into a cluster of exporters selling navigation, communications "
          "and sensor equipment abroad. A new export park in the western valley gathers testing, logistics and customs under one "
          "roof. Exporters want more tax relief; the crown offers just enough to keep them at home.",
          ('communications', 'economy'), after=('net_ground_stations',),
          reward=(Build('industrial_complex', 1, 112), Research('electronics', 0.5, 2))),
    Focus('net_drone_news', 'Drones Strike Osean Harbours',
          "In May 2019 drone attacks hit four major Osean naval ports on the same day a new war begins between Osea and Erusea. "
          "Perblan ports are smaller but built the same way, with open quays and soft defences. The security council meets "
          "that night to ask what a cheap drone could do to Sofern or Baleton, and how fast anyone could stop it.",
          ('security', 'communications'), after=('net_national',), requires=(After('2019.5.15'),), reward=(Event('port_drones'),)),
    Focus('net_harbour_guns', 'Guns Around Every Harbour',
          "The navy rings Sofern, Baleton and the harbour district with radar-guided guns and short-range missiles designed to "
          "swat small drones. It is proven technology and visible protection. The batteries are expensive to man around the "
          "clock, and drones cost a fraction of the shells used to stop them. The ports sleep better regardless.",
          ('security', 'navy'), after=('net_drone_news',), cost=10, exclusive=('net_signal_shield',), reward=(Idea('harbour_guns'),)),
    Focus('net_signal_shield', 'Jam the Drone Signals',
          "Gatewood engineers argue that most small drones depend on radio links and satellite navigation that can be jammed or "
          "spoofed. A network of electronic shields around the ports is cheaper than guns and uses domestic expertise. It "
          "disrupts civil radio nearby, and it may fail entirely against a drone that flies without any signal.",
          ('radar', 'communications'), after=('net_drone_news',), cost=10, exclusive=('net_harbour_guns',),
          reward=(Idea('signal_shield'),)),
    Focus('net_dark_sky', 'If the Satellites Go Dark',
          "When satellites over Usea are destroyed in the autumn of 2019 and network communications across that continent "
          "collapse, the kingdom sees what dependence on orbit can mean. The national network is hardened with ground backups, "
          "radio relays and manual procedures. Hardening costs money and convenience, and keeps the kingdom working if its sky goes quiet.",
          ('satellite', 'shelter'), after=('net_national',), requires=(After('2019.9.19'),),
          reward=(SwapIdea('national_network', 'hardened_network'),)),
    Focus('net_signals_reserve', 'A Signals Reserve',
          "Network engineers, radio amateurs and electronics graduates join a signals reserve that trains on weekends to defend "
          "networks, run jammers and restore communications after an attack. The service year tradition adapts to a new kind of "
          "front. The reserve costs little and gives the kingdom skills no conscript class could provide.",
          ('training', 'communications'), after_any=('net_harbour_guns', 'net_signal_shield'),
          reward=(Research('radar_tech', 0.5, 1), XP('army', 15))),
    Focus('net_account_2020', 'The Kingdom at Twenty Twenty',
          "At the end of the decade the government publishes a plain account of where the kingdom stands: its industry, its "
          "frontier, its networks and the four crown lands that still share one throne. The account is a baseline for whoever "
          "governs next. It promises nothing about the years ahead, because the kingdom has learned how quickly years change.",
          ('document', 'assembly'), after_any=('net_dark_sky', 'net_signals_reserve'), requires=(After('2020.1.1'),),
          reward=(Stability(0.04), WarSupport(0.02), Tooltip('Closes the 1991 to 2020 programme; later decades are not yet written.'))),
))

BRANCHES = (CROWN, LANDS, HEAVY, SERVICE, CIRCUITS, BORDER, AIR, COAST, AFTERMATH, DESERT, MILLENNIUM, NEIGHBOUR, NETWORK)
