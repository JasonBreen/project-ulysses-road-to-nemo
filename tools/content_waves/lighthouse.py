"""Wave F1: the Lighthouse War, 2010-2019 (Package 5). Erusea 54 and Central Usea 24.

Source layers
-------------
Official (ACES site, read 4 November 2026; compiled in
docs/STRANGEREAL_2006_2020_SOURCES.md and docs/research/STRANGEREAL_LORE_1991_2020.md):
every 2019 Chronicle entry from 05.15 to 12.01; the ACE COMBAT 7 abstract
(Erusea seizes the Arsenal Birds with the elevator; the "clean war"; the
voluntary coalition and the traditionalist sect; Expo City); the ACE COMBAT 7
product blurb (Erusea accuses Osea of overreach in their joint international
projects); the Super Weapons rows for the Arsenal Birds and the Alicorn. Named
people, squadrons, ships, places and weapons appear only in event text, as the
source names them; none becomes a unit, character, leader, state, border or tag.

Mod provenance, read only: the Continental War outcome flags (``ac_ucw_*``), the
Free Erusea records (``ERU_fe_*``, ``FCU_fe_*``), the Shilage release flags
(``ac_release_SHI_*``), the Stonehenge project state.

Provisional gameplay: every focus, policy, service, dialogue and value; the
owner's fourteen-day windows, idea values and decisions; the scripted ceasefire
(user decision 7); the two special projects (user decision 8); the earned
withheld declaration and early ceasefire.
"""
from content_waves.framework import Branch, Wave, block, guard

P = "ac_lhw"
COUNTRIES = {"OSE": "Osea"}          # extra category art for the Osean crisis decisions
ERU_ASSESSMENT = "ERU_ucw_exp_settlement_assessment"
FCU_ASSESSMENT = "FCU_ucw_exp_settlement_assessment"
ISAF = "has_global_flag = ac_ucw_outcome_isaf_victory"
STARTED = "has_global_flag = ac_lhw_started"
ENDED = "has_global_flag = ac_lhw_ended"
TAINTED = "has_global_flag = ac_lhw_tainted"
EXISTING = "has_global_flag = ac_lhw_existing_war_observed"
CLOSED = "has_global_flag = ac_lhw_closed"
ROUTE_SETTLED = f"NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_lhw_declaration_withheld }} NOT = {{ {CLOSED} }}"


def fe(tag, keys):
    return tuple(f"{tag}_fe_{k}_settlement" for k in keys)


A_ISAF = fe("ERU", ("oversight", "insurrection", "return")) + (ERU_ASSESSMENT,)
A_OTHER = fe("ERU", ("victor", "armistice", "ordinary", "return")) + (ERU_ASSESSMENT,)
A_ALL = fe("ERU", ("oversight", "insurrection", "return", "victor", "armistice", "ordinary")) + (ERU_ASSESSMENT,)
FCU_ENTRY = fe("FCU", ("oversight", "security", "partners", "drawdown")) + (FCU_ASSESSMENT,)

BRANCHES = (
    # Erusea, stage 1 ---------------------------------------------------------------
    Branch("ERU", "sovereignty", A_ISAF, ISAF + " date > 2009.12.31",
        ("Close the Oversight File", "Treaty Obligations Kept", "A Republic Rearmed",
         "Return the Last Countersignatures", "Review a Sovereignty Service Period", "A Sovereignty With Accounts"),
        ("Fifteen years after the surrender, the oversight instruments of 2005 are still on the books, most of them dormant. Before the republic declares itself fully sovereign again, the cabinet will list every duty that still carries a foreign countersignature and every undertaking Erusea gave in exchange for its return to self-government.",
         "Erusea will keep every treaty obligation it accepted in 2005 and publish its compliance each year. The policy costs the government political room whenever a minister wants to act first and explain later, and it gives Erusea's partners a record they can hold the republic to.",
         "Erusea will rebuild the forces the oversight years ran down, within the letter of its obligations and at the edge of their spirit. The army and navy regain organisation and confidence; the civilian budget and the republic's standing with its partners pay for it.",
         "The last oversight countersignatures will be returned to Erusean offices on a published schedule, each with a receiving official who answers for it. The handover is administrative, not ceremonial, and it is complete only when the partners confirm it.",
         "A completed, funded service period under the chosen policy must be examined before the republic calls its sovereignty settled. The review compares the obligations kept, the forces rebuilt and the duties returned with what the cabinet promised.",
         "The settlement records what the republic now does on its own authority and what it has undertaken to go on doing. It is a sovereignty with accounts: the chosen policy stands, and its continuing cost is written down beside it."),
        (("document", "scales"), ("diplomacy", "document"), ("command", "industry"), ("gate", "civil"), ("scales", "document"), ("assembly", "peace")),
        (("Treaty obligations kept", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("A republic rearmed", {"army_org_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Publish a Compliance Return", "Compile and publish the republic's compliance with its 2005 undertakings for the year.", "The treaty compliance office", {"political_power_gain": 0.08}),
         ("Staff the Returned Desks", "Train the officials who take over the last countersigned duties.", "The cabinet office", {"stability_factor": 0.025})),
        ("The Clause Nobody Has Read Since 2005",
         "The compliance office has found a clause in the 2005 instruments that requires Erusea to notify its partners before any joint international project changes hands. Nobody has invoked it in fifteen years. Now a ministry wants to know whether a change in the management of a shared project would trigger it, and the lawyers disagree.\n\nThe treaty office wants to publish its reading of the clause and invite the partners to answer, so that the republic cannot be accused later of acting in the dark. The defence ministry would rather keep the question inside the cabinet: a public reading commits the republic to an interpretation it may regret.",
         ("Publish the reading and invite the partners' answer.", "Keep the question inside the cabinet.")),
        ("Accounts Rendered",
         "The final review lists every 2005 undertaking with its current status: kept, returned, renegotiated or lapsed with the partners' knowledge. The forces rebuilt are listed in the same table as the obligations they test.\n\nThe clause about shared projects is in the appendix, with the reading the cabinet adopted and the date the partners were told. Whatever the republic decides next, it will not be able to say it did not know what it had promised.")),
    Branch("ERU", "standing", A_OTHER, "NOT = { " + ISAF + " } date > 2009.12.31",
        ("Take Stock of the Decade", "A Settled Border Policy", "A Watchful Border Policy",
         "Publish the Republic's Position", "Review a Standing Service Period", "A Republic on Its Own Terms"),
        ("The Continental War did not end with an ISAF victory in this history, and the road the official record describes for 2019 does not run through this republic. The cabinet will take stock of the decade on its own terms: what Erusea holds, what it owes and what its neighbours expect of it.",
         "Erusea will treat its postwar lines as settled and say so to every neighbour. The policy lowers the cost of the border and the temperature of the continent; it also gives up the leverage that an unsettled line provides.",
         "Erusea will keep its lines under watch and its claims open, without pressing them. Commanders keep their options and the government its leverage, at a continuing cost in money and in the neighbours' trust.",
         "The republic will publish its position on each outstanding question with a neighbour: what it claims, what it concedes and what it will negotiate. A published position can be held to; it also removes the convenience of ambiguity.",
         "A completed, funded service period under the chosen policy must be reviewed before the position becomes doctrine. The review asks whether the neighbours answered, whether incidents fell and whether the republic's costs matched its words.",
         "The settlement fixes the republic's position for the decade ahead. It does not reproduce the official record's 2019 war, which this history never reached, and it does not invent another. It leaves a government that knows what it stands for."),
        (("document", "scales"), ("peace", "gate"), ("security", "radar"), ("document", "communications"), ("scales", "document"), ("assembly", "civil")),
        (("Settled border policy", {"stability_factor": 0.025}, {"army_org_factor": -0.01}),
         ("Watchful border policy", {"army_core_defence_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Run a Border Liaison Period", "Keep liaison officers meeting each neighbour's counterparts on a fixed schedule.", "The foreign ministry's border desk", {"political_power_gain": 0.08}),
         ("Audit the Standing Claims", "Review every outstanding claim and concession with the office responsible for it.", "The cabinet legal office", {"stability_factor": 0.025})),
        ("A Map Marked in Two Colours",
         "The legal office has produced a map of the republic's borders marked in two colours: the lines every neighbour accepts and the lines Erusea alone calls settled. The second colour covers more ground than the ministers expected.\n\nThe foreign ministry proposes publishing the map, so that the republic's position is the one its neighbours read rather than the one they guess at. The general staff asks that it stay inside the cabinet: a published map is a list of what Erusea will not fight for.",
         ("Publish the two-colour map.", "Keep the map inside the cabinet.")),
        ("The Position the Republic Holds",
         "The final review is a single statement of position, neighbour by neighbour, with the date each was told. Some answered. Some did not. The incidents of the year are listed beside the answers.\n\nThe two-colour map is in the file. Fewer lines are marked in the second colour than when it was drawn.")),
    Branch("ERU", "elevator", A_ALL, "date > 2013.12.31",
        ("Survey the Space Elevator's Shadow", "A Shared-Project Partnership", "A Sovereign Project Posture",
         "Audit the Joint Accounts", "Review an Elevator Service Period", "An Elevator Policy on Record"),
        ("The International Space Elevator stands within reach of Erusean territory and under a joint international management. The cabinet will record what the project means for the republic: the traffic it brings, the obligations it carries and the questions nobody has asked in public.",
         "Erusea will take its place in the joint management of the elevator and its projects as one partner among several. The partnership brings investment and a seat at the table; it also binds the republic to decisions it does not control.",
         "Erusea will treat the elevator's shadow as a matter of sovereign interest and keep its own posture around it. The posture reassures the republic's own public and its armed forces; it costs the republic goodwill in the joint management and money at home.",
         "The joint accounts of the shared projects will be audited by Erusean officials with the partners' consent. An audit answers the question of who pays and who benefits; it may also produce the grievance the official record says Erusea later voiced.",
         "A completed, funded service period under the chosen posture must be examined before the republic's elevator policy becomes doctrine. The review compares what the partnership delivered or what the posture cost with the figures in the audit.",
         "The settlement puts Erusea's elevator policy on record. It names the joint projects the republic takes part in and the ones it watches, and it does not decide the war the official record places in 2019. That decision belongs to the Lighthouse War owner."),
        (("satellite", "telescope"), ("diplomacy", "satellite"), ("security", "satellite"), ("economy", "scales"), ("scales", "satellite"), ("document", "peace")),
        (("Shared-project partnership", {"research_speed_factor": 0.02}, {"political_power_gain": -0.05}),
         ("Sovereign project posture", {"army_core_defence_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Second Engineers to the Joint Projects", "Place Erusean engineers with the elevator's joint projects for a defined period.", "The science and technology ministry", {"research_speed_factor": 0.03}),
         ("Run a Shadow Survey Period", "Survey the traffic, rules and obligations in the elevator's shadow and report to the cabinet.", "The cabinet survey office", {"political_power_gain": 0.08})),
        ("A Line Item Nobody Explains",
         "The audit team has found a line in the joint accounts that the partners describe as 'defence of the elevator' and will not itemise. It is not small. Erusean officials have asked three times what it pays for and received three polite answers that do not say.\n\nThe survey office wants to publish the question, so that the republic's partners answer it in public or admit they will not. The foreign ministry prefers a private note: a public question about defence spending reads as an accusation, and the official record of 2019 shows where accusations led.",
         ("Publish the question about the line item.", "Send a private note and wait for the answer.")),
        ("The Elevator Policy on Record",
         "The final review records the republic's elevator policy as a list of projects: the ones Erusea takes part in, the ones it audits, the ones it watches. The unexplained line item is still unexplained. The review says so, and names the office that will keep asking.\n\nNothing in the record decides what the republic will do if the questions stop being answered.")),
    Branch("ERU", "alicorn", A_ALL, "date > 2012.12.31",
        ("Authorise the Submarine Cruiser", "A Royal Navy Programme", "A Civil Shipyard Programme",
         "Set the Custody Rules", "Review a Cruiser Service Period", "Custody Rules for the Cruiser"),
        ("The Erusean Royal Navy's Rán Fleet has asked for a submarine aviation cruiser: a nuclear-powered boat that is both a carrier and a long-range railgun platform, designed to strike while submerged and beyond an enemy's reach. The Super Weapons record names it the Alicorn. Before any keel is laid, the cabinet will decide who builds it and who answers for it.",
         "The Royal Navy will run the programme from design to commissioning. The navy keeps its requirements intact and its secrets close; the civilian budget and the cabinet's oversight pay for a programme nobody outside the fleet can audit.",
         "A civil shipyard will build the hull under naval specification and civilian accounts. The programme is cheaper and better documented, and the navy will say, correctly, that a cruiser built in public is a cruiser the enemy knows.",
         "Custody rules will be written before the boat exists: who may order it to sea, who may order it to fire and what record each order leaves. A weapon designed to disappear needs rules written while it is still on paper.",
         "A completed, funded service period under the chosen programme must be reviewed before the cabinet accepts the cruiser into service. The review asks whether the custody rules held during trials and whether the accounts match the hull.",
         "The settlement fixes the custody rules for the Alicorn and the programme that builds it. It commissions no voyage and fires no railgun. The Super Weapons record says the boat disappeared during a sea trial; this campaign records nothing of the kind by script."),
        (("submarine", "document"), ("navy", "submarine"), ("industry", "submarine"), ("scales", "submarine"), ("scales", "document"), ("submarine", "peace")),
        (("Royal Navy programme", {"naval_coordination": 0.05}, {"consumer_goods_factor": 0.01}),
         ("Civil shipyard programme", {"industrial_capacity_dockyard": 0.05}, {"political_power_gain": -0.05})),
        (("Run a Design Review Period", "Review the cruiser's design against the custody rules before construction proceeds.", "The naval design bureau", {"research_speed_factor": 0.03}),
         ("Fund a Yard Preparation Period", "Prepare the yard, the crews and the accounts for a hull of this size.", "The shipbuilding directorate", {"industrial_capacity_dockyard": 0.05})),
        ("A Captain Chosen Before the Boat",
         "The navy has named the officer it wants to command the cruiser, years before it will float. He is a Continental War veteran with a loyal following and a reputation that fills the file. The cabinet did not ask for a name; the navy sent one anyway.\n\nThe design bureau wants the custody rules published now, with the command appointment made subject to them in public. The navy prefers a private understanding: a public rule reads as distrust of an officer who has given the republic nothing but service.",
         ("Publish the custody rules with the appointment.", "Settle the rules privately with the fleet.")),
        ("Rules Written While It Was Still on Paper",
         "The final review records the custody rules as adopted: who orders the cruiser to sea, who orders it to fire, what record each order leaves and who reads it. The programme's accounts are attached, whichever yard kept them.\n\nThe officer's name is in the file. The rules apply to him as they apply to anyone.")),
    Branch("ERU", "drones", A_ALL, "date > 2016.12.31",
        ("Charter an Unmanned Aviation Programme", "An Unmanned Strike Doctrine", "A Manned-Primary Doctrine",
         "Write the Rules of Engagement", "Review a Drone Service Period", "A Doctrine on Record"),
        ("Unmanned aircraft are cheaper than pilots and need no funerals. The Chronicle records that the Lighthouse War opened with drone strikes on four Osean naval ports; it does not say whose drones they were, and this campaign does not. Before Erusea builds a programme, the cabinet will decide what it is for.",
         "Erusea will make unmanned aircraft the core of its air power: mass, range and the willingness to lose airframes. The doctrine multiplies sorties and divides the risk to aircrew; it costs the air force its traditions and the republic the question of who is responsible when a machine chooses.",
         "Erusea will keep pilots at the centre and use unmanned aircraft as their escorts and sensors. The doctrine preserves judgment in the cockpit and the air force's identity; it forgoes the mass that an unmanned fleet provides.",
         "Rules of engagement for unmanned aircraft will be written before the programme fields them: what a machine may attack on its own, what needs a human order and what record the decision leaves. The official abstract records that Erusea proclaimed a 'clean war'; the rules are what such a claim would have to rest on.",
         "A completed, funded service period under the chosen doctrine must be reviewed before it becomes the air force's standing practice. The review compares the sorties flown, the rules applied and the incidents recorded.",
         "The settlement puts the doctrine on record with its rules of engagement attached. It fields no strike and attributes none; it leaves the republic an air force that knows what its machines are allowed to do."),
        (("air", "science"), ("air", "missile"), ("air", "training"), ("scales", "air"), ("scales", "document"), ("air", "peace")),
        (("Unmanned strike doctrine", {"air_mission_efficiency": 0.04}, {"stability_factor": -0.015}),
         ("Manned-primary doctrine", {"army_org_factor": 0.02}, {"research_speed_factor": -0.01})),
        (("Run a Trials Programme", "Fly the programme's trials under the draft rules of engagement and record every decision.", "The air force test wing", {"air_mission_efficiency": 0.03}),
         ("Fund a Rules Review", "Review the rules of engagement with the legal office and the aircrews who will apply them.", "The air staff legal office", {"political_power_gain": 0.08})),
        ("A Target the Machine Chose",
         "During trials an unmanned aircraft selected a target its operators had not marked. It did not fire; the rules did not allow it to. The test wing's report describes the selection in detail and asks whether the rules should be loosened, since the target was, in fact, legitimate.\n\nThe legal office wants the report published, so that the republic's 'clean war' claim, if it is ever made, rests on a record anyone can read. The air staff prefers to keep it inside the programme: a public account of what the machine nearly did is an invitation to every critic of the programme.",
         ("Publish the trials report.", "Keep the report inside the programme.")),
        ("The Doctrine on Record",
         "The final review records the doctrine and its rules as adopted, with the trials that tested them. The incident of the unmarked target is in the file with the decision the cabinet took about it.\n\nThe programme fielded no strike in the review period. The record says what it would be allowed to do.")),
    # Erusea, stage 2 and 3 --------------------------------------------------------------
    Branch("ERU", "lighthouse", ("ERU_lw_elevator_settlement",), STARTED,
        ("Garrison the Captured Elevator", "A Fortress Elevator", "An Elevator Kept Running",
         "Keep the Civil Traffic Moving", "Review an Elevator Garrison Period", "The Elevator After the War"),
        ("Erusean forces hold the International Space Elevator, as the Chronicle records for 15 May 2019. Holding it is not the same as running it. The cabinet will decide what the garrison is for: a fortress, or a facility kept working under Erusean guard.",
         "The elevator will be a fortress: its approaches fortified, its traffic stopped, its defences the republic's first line. The posture is clear and expensive, and it turns a shared civil project into the war's most obvious target.",
         "The elevator will be kept running under guard: civil traffic continued where it can be, the facility's staff kept at work, the defences kept out of the way. The posture preserves what the republic captured; it leaves the garrison exposed and the staff in the line of fire.",
         "Civil traffic through the elevator will continue under published rules while the garrison holds it. Keeping the traffic moving is the republic's claim that it captured a facility rather than destroyed one, and every incident on the way will test that claim.",
         "A completed, funded garrison period must be examined before the republic decides the elevator's future. The review compares the posture's cost with the traffic kept moving, the incidents recorded and the staff who stayed.",
         "The settlement decides the elevator's future after the fighting, whoever holds it then: fortress, facility or handover. The early-ceasefire record belongs to this lane. It changes nothing about who controls the elevator in the end; the war decides that."),
        (("satellite", "security"), ("gate", "satellite"), ("satellite", "civil"), ("logistics", "satellite"), ("scales", "satellite"), ("satellite", "peace")),
        (("A fortress elevator", {"army_core_defence_factor": 0.04}, {"stability_factor": -0.015}),
         ("An elevator kept running", {"stability_factor": 0.025}, {"army_org_factor": -0.01})),
        (("Run a Garrison Rotation", "Rotate the garrison and its supply through the elevator's approaches under the chosen posture.", "The elevator garrison command", {"army_core_defence_factor": 0.03}),
         ("Keep the Civil Staff at Work", "Keep the facility's civil staff paid, protected and working under Erusean guard.", "The occupation civil office", {"stability_factor": 0.025})),
        ("The Engineer Who Would Not Leave",
         "A senior engineer of the elevator's civil staff has refused evacuation. The facility, she says, needs its operators more than its guards, and she will not hand it to people who do not know how it works. The garrison commander wants her removed; the civil office wants her name in the official account.\n\nThe civil office proposes publishing the staff who stayed, as evidence that the elevator is kept working rather than seized. The garrison command wants the list protected: every name on it is a name the other side can use.",
         ("Publish the staff who stayed.", "Protect the staff list.")),
        ("What the Garrison Held",
         "The final review records what the garrison held and what it kept moving: the traffic, the staff, the incidents and the cost. It decides the elevator's future after the fighting without deciding who will hold it then.\n\nThe engineer's name is in the file. She is still at work.")),
    Branch("ERU", "capital", ("ERU_lw_sovereignty_settlement",), STARTED,
        ("Prepare the Capital's Defence", "A Capital Under Arms", "A Capital Kept Open",
         "Keep the Ministries Working", "Review a Capital Service Period", "A Capital That Kept Working"),
        ("Farbanti is the Erusean capital, and the Chronicle records an Osean offensive against it that failed in May 2019 and an attack that began in September. The cabinet will prepare the capital's defence now, before the record's dates arrive, and decide what the city is to be while the war lasts.",
         "The capital will be put under arms: its approaches fortified, its districts organised for defence, its government ready to move. The policy gives the defenders their best chance and the city's residents the worst of both worlds.",
         "The capital will be kept open: ministries working, courts sitting, markets trading, with the defence held outside the city as long as it can be. The policy keeps the republic governing; it stakes the government's survival on lines it may not hold.",
         "The ministries will keep working through the attack with the records and the staff that an evacuation would scatter. When the satellites fall and the networks go dark, as the Chronicle records for 19 September, the republic's ground relays and paper files will be what is left.",
         "A completed, funded service period under the chosen policy must be examined before the capital's wartime posture becomes permanent. The review compares the ministries that kept working with the districts that held and the cost of each.",
         "The settlement records a capital that kept working, under arms or open, through the attack the Chronicle places in September 2019. It changes no territory; it leaves a government that knows how it governed under fire."),
        (("gate", "command"), ("security", "gate"), ("civil", "gate"), ("communications", "document"), ("scales", "civil"), ("civil", "peace")),
        (("A capital under arms", {"army_core_defence_factor": 0.04}, {"consumer_goods_factor": 0.015}),
         ("A capital kept open", {"stability_factor": 0.03}, {"army_core_defence_factor": -0.01})),
        (("Fund a Ground Relay Network", "Build and staff ground relays so the ministries keep working when the satellite networks fail.", "The communications ministry", {"stability_factor": 0.025}),
         ("Run a Ministry Continuity Period", "Keep the ministries' records, staff and decisions working through the attack on the capital.", "The cabinet continuity office", {"political_power_gain": 0.08})),
        ("The Day the Screens Went Dark",
         "On the morning the networks failed, the finance ministry's payroll ran anyway, from paper ledgers a clerk had kept against instructions. The relay network the communications ministry built reached the districts it was meant to reach and no further. The cabinet now has two reports: one about the ledgers and one about the relays, and they disagree about what saved the day.\n\nThe continuity office wants both published, so that the capital's residents know what worked. The communications ministry asks that the relay report stay protected: its gaps are a map of where the capital cannot hear.",
         ("Publish both reports.", "Protect the relay report.")),
        ("A Capital That Kept Working",
         "The final review lists what the capital kept doing while the attack the Chronicle records for 19 September 2019 went on: payroll, courts, water, the relays that worked and the ones that did not. It does not say who held the city; the war says that.\n\nThe clerk's ledgers are in the appendix. They are now the ministry's instructions.")),
    Branch("ERU", "ceasefire", ("ERU_lw_sovereignty_settlement", "ERU_lw_elevator_settlement"), ENDED,
        ("The War's Account", "A Public Accounting", "A Protected Accounting",
         "Answer the Partners' Questions", "Review a Postwar Service Period", "A Republic After the Lighthouse War"),
        ("The fighting is over, however it ended. The Chronicle records a ceasefire treaty signed at the Expo City Conference on 1 December 2019; this campaign records the end it actually reached. Either way, the republic owes itself an account of the war before it decides what comes after.",
         "The account will be public: the decisions, the orders, the strikes and the blunders, in a record the republic's own citizens and its partners can read. The policy restores standing abroad and costs the government at home, where every page is an argument.",
         "The account will be protected: compiled in full, read by the cabinet and the courts, published in summary. The policy keeps the republic's secrets and its officers' names; it leaves the partners to draw their own conclusions.",
         "The republic's partners will have questions, whether the war ended at Expo City or elsewhere. Each will be answered in writing by the office responsible, with the account as its basis. The answers are the republic's first postwar diplomacy.",
         "A completed, funded service period of the accounting must be examined before the republic closes the war's file. The review asks whether the questions were answered, whether the account was read and what it changed.",
         "The settlement is the republic after the Lighthouse War: its account rendered, its partners answered, its chosen degree of openness on record. It asserts no outcome the war did not reach and no treaty the republic did not sign."),
        (("document", "scales"), ("assembly", "document"), ("security", "document"), ("diplomacy", "document"), ("scales", "peace"), ("peace", "civil")),
        (("A public accounting", {"stability_factor": 0.03}, {"political_power_gain": -0.06}),
         ("A protected accounting", {"political_power_gain": 0.05}, {"stability_factor": -0.01})),
        (("Compile the War Record", "Compile the account of the war from the orders, strikes and decisions on file.", "The war records commission", {"political_power_gain": 0.08}),
         ("Answer the Partner Questionnaires", "Answer each partner's written questions from the compiled account.", "The foreign ministry's postwar desk", {"stability_factor": 0.025})),
        ("The Order Without a Signature",
         "The commission has found an order from the war's last weeks that nobody signed. It was carried out. The officers who carried it out say it came through the chain of command; the chain of command says it did not. The official abstract records that a traditionalist sect of the Erusean Army joined a voluntary coalition of Osean forces at the end; the commission does not know whether this order belongs to that story.\n\nThe commission wants the unsigned order published as found. The defence ministry asks for a protected finding first: a public order without a signature is an invitation to name one.",
         ("Publish the unsigned order as found.", "Protect the finding until the signature is traced.")),
        ("A Republic After the Lighthouse War",
         "The final review is the republic's account of the war as it was actually fought and ended, with the partners' questions and the answers given. The unsigned order is in it, with what the commission could and could not establish.\n\nThe republic signed what it signed and no more. The account says so.")),
    Branch("ERU", "secession", ("ERU_lw_sovereignty_settlement", "ERU_lw_elevator_settlement"), "has_global_flag = ac_lhw_stage_secession",
        ("Answer the Declarations of Independence", "Negotiated Autonomy", "Restored Authority",
         "Keep the Conflict Inside the Law", "Review a Settlement Service Period", "A Settlement With the Small Nations"),
        ("The Chronicle records that the autonomous state of Shilage and other small nations annexed by the Kingdom of Erusea declared independence on 1 October 2019, that the Erusean government refused to recognise them and that internal conflict followed. This campaign changes no border on that date. The cabinet must answer the declarations with a policy.",
         "Erusea will negotiate autonomy with the small nations: self-government within the republic, with the terms written down and the conflict ended by agreement. The policy costs the republic authority and some of its revenue; it ends the internal conflict without ending the republic.",
         "Erusea will restore its authority over the small nations by administration and, where needed, by force. The policy keeps the republic whole and its army occupied; it turns the internal conflict into a standing obligation.",
         "The internal conflict will be fought, or settled, inside the law: arrests recorded, searches warranted, negotiations minuted. The republic's answer to secession is also the republic's answer to the question of what kind of state it is.",
         "A completed, funded service period under the chosen policy must be examined before the republic calls the conflict settled. The review compares the terms agreed or the authority restored with the incidents recorded and the cost.",
         "The settlement records the republic's terms with the small nations as negotiated or restored. It releases no country, draws no border and moves no state; those remain the release contracts' business and the war's."),
        (("assembly", "document"), ("diplomacy", "assembly"), ("security", "command"), ("scales", "security"), ("scales", "document"), ("assembly", "peace")),
        (("Negotiated autonomy", {"stability_factor": 0.03}, {"political_power_gain": -0.06}),
         ("Restored authority", {"army_org_factor": 0.025}, {"stability_factor": -0.015})),
        (("Run a Negotiation Period", "Keep negotiators, interpreters and a protected meeting place available to the small nations.", "The cabinet negotiation office", {"political_power_gain": 0.08}),
         ("Fund an Administrative Restoration", "Restore the republic's administration in the districts that declared independence, under recorded rules.", "The interior ministry", {"stability_factor": 0.025})),
        ("A Delegation at the Door",
         "A delegation from one of the small nations has arrived in the capital with a declaration in one hand and a list of grievances in the other. The grievances are specific: taxes collected and not returned, offices closed, a language not taught. The declaration is general. The cabinet can answer either.\n\nThe negotiation office wants the grievances published with the republic's answers, so that the declaration is argued in public. The interior ministry prefers a protected answer: a published list of grievances is a published list of the republic's failures.",
         ("Publish the grievances with the republic's answers.", "Answer the delegation in private.")),
        ("The Terms on Record",
         "The final review records the terms reached with each small nation, negotiated or restored, with the incidents of the period and the cost. It draws no border. Where a nation exists as a country in this campaign, the record says so and changes nothing about it.\n\nThe delegation's list of grievances is in the file, with the answers given.")),
    # Central Usea --------------------------------------------------------------------
    Branch("FCU", "airspace", FCU_ENTRY, "date > 2018.12.31",
        ("Rule on the Continental Airspace", "Closed Airspace", "A Declared Transit Corridor",
         "Publish the Airspace Rules", "Review an Airspace Service Period", "An Airspace Policy on Record"),
        ("Tensions between Osea and Erusea are rising over the elevator and the joint projects around it, and Central Usean airspace lies between them. The federation will decide, before anyone asks, what crosses its skies and on what terms.",
         "Central Usean airspace will be closed to foreign military flight. The policy keeps the federation out of other people's wars and costs it the goodwill of partners who expected a route; it also makes every unidentified aircraft a decision.",
         "The federation will declare a transit corridor under published rules, open to any party that accepts them. The corridor earns the federation a role and a record; it also earns it the attention of every air force that wants the corridor's other end.",
         "The airspace rules will be published, with the office that administers them and the procedure for a violation. A published rule is the federation's protection against being accused of taking sides by silence.",
         "A completed, funded service period under the chosen rules must be examined before the airspace policy becomes permanent. The review compares the flights recorded, the violations answered and the partners' complaints.",
         "The settlement fixes the federation's airspace policy: closed or a corridor, with the rules and the record that go with it. It grants no membership of any force, no access to any base and no judgment about the war."),
        (("radar", "scales"), ("gate", "radar"), ("air", "communications"), ("document", "radar"), ("scales", "radar"), ("radar", "peace")),
        (("Closed airspace", {"army_core_defence_factor": 0.03}, {"political_power_gain": -0.05}),
         ("A declared transit corridor", {"political_power_gain": 0.05}, {"stability_factor": -0.01})),
        (("Run an Airspace Monitoring Period", "Keep the radar and reporting stations that record every flight through federal airspace staffed.", "The federal air traffic authority", {"army_core_defence_factor": 0.03}),
         ("Staff the Violations Desk", "Answer every recorded violation in writing through the published procedure.", "The foreign ministry's airspace desk", {"political_power_gain": 0.08})),
        ("A Flight That Filed No Plan",
         "A military aircraft crossed federal airspace at night without a flight plan and left the way it came. The radar record is clear; the nationality is not. The violations desk has drafted a note to two governments, since it cannot tell which one to send it to.\n\nThe air traffic authority wants the radar track published with the note, so that whoever flew it knows the federation saw it. The foreign ministry prefers to send the note privately to both: a published track is an accusation against one of them.",
         ("Publish the track with the note.", "Send the note privately to both governments.")),
        ("An Airspace Policy on Record",
         "The final review records the flights, the violations and the answers of the period, with the policy as adopted. It grants nothing to anyone. The night flight is in the record, still without a nationality, with the notes that were sent.")),
    Branch("FCU", "corridor", FCU_ENTRY, STARTED,
        ("Open a Humanitarian Corridor", "A Corridor Under Federal Escort", "A Corridor Under Neutral Flags",
         "Register Every Convoy", "Review a Corridor Service Period", "A Corridor That Reached Its End"),
        ("The Lighthouse War has begun on the federation's doorstep. People and supplies will move whether the federation organises them or not. The cabinet will open a humanitarian corridor and decide whose flag protects it.",
         "Federal forces will escort the corridor's convoys. The escort makes the corridor reliable and the federation a participant in everyone's eyes; a single incident will test how neutral an armed escort can be.",
         "The corridor will run under neutral flags and the agreed rules of the belligerents, with federal staff unarmed. The arrangement keeps the federation out of the war and leaves the convoys to the belligerents' good faith.",
         "Every convoy will be registered: cargo, route, escort and the office that cleared it. A corridor whose contents are recorded can answer the accusation that it carried something else.",
         "A completed, funded corridor period must be examined before the federation renews it. The review counts the convoys that reached their end, the incidents recorded and the belligerents' complaints.",
         "The settlement fixes the corridor's rules for as long as the fighting lasts and records what it carried. It changes no border and takes no side; it leaves the federation a procedure it can use the next time."),
        (("logistics", "medical"), ("security", "logistics"), ("diplomacy", "logistics"), ("document", "logistics"), ("scales", "logistics"), ("logistics", "peace")),
        (("A corridor under federal escort", {"army_org_factor": 0.025}, {"political_power_gain": -0.05}),
         ("A corridor under neutral flags", {"stability_factor": 0.025}, {"supply_consumption_factor": 0.02})),
        (("Run a Convoy Period", "Move a scheduled series of registered convoys through the corridor under the chosen protection.", "The federal relief logistics office", {"supply_consumption_factor": -0.03}),
         ("Staff the Convoy Registry", "Register every convoy's cargo, route and clearance and answer the belligerents' queries.", "The corridor registry", {"political_power_gain": 0.08})),
        ("A Convoy Stopped at a Checkpoint",
         "A registered convoy was stopped at a belligerent checkpoint and held for a day while its cargo was searched. The cargo was what the registry said. The convoy commander's report asks whether the federation will protest, and the registry's report asks whether the search was within the rules the belligerents agreed.\n\nThe logistics office wants the stop published, so that the next checkpoint knows the federation records them. The foreign ministry prefers a private protest: a published stop reads as a charge against one side.",
         ("Publish the stop and the registry entry.", "Protest privately and keep the convoy moving.")),
        ("A Corridor That Reached Its End",
         "The final review counts the convoys, the cargo, the stops and the answers. It takes no side and changes no line. The stopped convoy is in the record, with the search that found what the registry said it would.")),
    Branch("FCU", "blackout", FCU_ENTRY, "has_global_flag = ac_lhw_stage_farbanti",
        ("Answer the Continental Blackout", "Ground Relays First", "A Replacement Satellite Programme",
         "Keep the Federal Services Reachable", "Review a Blackout Service Period", "Communications the Federation Controls"),
        ("The Chronicle records that an operation to destroy military satellites cut off network communications across the entire Usean continent on 19 September 2019. The federation's networks went dark with everyone else's. The cabinet will decide how the federation gets its communications back and who will control them afterwards.",
         "The federation will rebuild its communications on ground relays it owns: slower, local and beyond the reach of whoever shoots down satellites next. The policy is cheap to begin and expensive to finish, and it leaves the continent's long-range traffic to others.",
         "The federation will fund a replacement satellite programme, alone or with partners. The programme restores the long-range traffic the blackout destroyed and depends on launch capacity the federation does not own; it also makes the federation a party to the next war's targeting.",
         "Federal services will be kept reachable by whatever works: relays, couriers, paper. A government that cannot be reached cannot be obeyed, and the blackout's first casualty was the assumption that the networks would always be there.",
         "A completed, funded service period under the chosen policy must be examined before the federation's communications policy is fixed. The review compares the services restored with the money spent and the dependence accepted.",
         "The settlement fixes the communications the federation controls after the blackout and records what it depends on others for. It assigns no blame for the satellites; the Chronicle does not say whose operation it was, and this campaign does not."),
        (("communications", "satellite"), ("communications", "rail"), ("satellite", "science"), ("civil", "communications"), ("scales", "communications"), ("communications", "peace")),
        (("Ground relays first", {"stability_factor": 0.025}, {"research_speed_factor": -0.01}),
         ("A replacement satellite programme", {"research_speed_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Build a Relay Network", "Build and staff the ground relays that restore federal communications district by district.", "The federal communications authority", {"stability_factor": 0.025}),
         ("Run a Satellite Design Period", "Design the replacement satellites and secure the launch capacity to orbit them.", "The federal space office", {"research_speed_factor": 0.03})),
        ("The District Nobody Could Reach",
         "For eleven days after the blackout, one district received no instruction from the federal government and gave none. Its council ran the district on its own authority and kept a record. The record is good. The council now asks whether it did the right thing, and whether it will be reached next time.\n\nThe communications authority wants the district's record published as a model, so that every council knows what to do when the networks fail. The interior ministry prefers a protected review: a published model of self-government is an invitation to use it.",
         ("Publish the district's record as a model.", "Review the record privately.")),
        ("Communications the Federation Controls",
         "The final review lists what the federation can now reach on its own, what it reaches through partners and what it cannot reach at all. The district that governed itself for eleven days is in the record, with the instruction it now has for the next time.")),
    Branch("FCU", "settlement", FCU_ENTRY, ENDED,
        ("Convene the Postwar Settlement", "A Guarantor of the Settlement", "A Convenor of the Conference",
         "Keep the Federation's Name Off the Terms", "Review a Settlement Service Period", "A Federation That Hosted the Peace"),
        ("The fighting between Osea and Erusea has ended, at the Expo City Conference the Chronicle records for 1 December 2019 or in some other way. The federation sits between the two and will be asked what part it plays in what follows. The cabinet will decide whether to guarantee the settlement or merely to host it.",
         "The federation will guarantee the settlement: a signatory with obligations, whose forces and standing back the terms. The role earns the federation a place at every later table and binds it to a peace it did not make.",
         "The federation will convene the conference and keep its name off the terms. The role costs nothing but staff and goodwill, and it leaves the federation without a say when the terms are tested.",
         "The federation's name will stay off the terms of the settlement unless the cabinet decides otherwise. Expo City is not claimed as Central Usean by this campaign; the conference is hosted wherever the parties agree, and the federation's part in it is its own choice.",
         "A completed, funded service period under the chosen role must be examined before the federation's postwar policy is fixed. The review compares the obligations accepted or declined with what the settlement delivered.",
         "The settlement records the federation's part in the peace that followed the Lighthouse War, as guarantor or as host. It asserts no treaty the parties did not sign and no border the war did not draw."),
        (("diplomacy", "assembly"), ("scales", "diplomacy"), ("assembly", "diplomacy"), ("document", "diplomacy"), ("scales", "document"), ("peace", "assembly")),
        (("A guarantor of the settlement", {"political_power_gain": 0.05}, {"army_org_factor": -0.01}),
         ("A convenor of the conference", {"stability_factor": 0.025}, {"political_power_gain": -0.05})),
        (("Staff the Conference Secretariat", "Keep the secretariat, interpreters and the record of the postwar conference running.", "The treaty secretariat", {"political_power_gain": 0.08}),
         ("Run a Guarantee Review", "Review each obligation the federation accepted or declined under the settlement.", "The federal cabinet office", {"stability_factor": 0.025})),
        ("The Chair at the End of the Table",
         "The parties have asked the federation to take the chair at the end of the table: not a seat among them, but the seat that calls the session to order and signs the record. Taking it costs nothing today. Refusing it is a statement; accepting it is a precedent.\n\nThe secretariat wants the invitation and the federation's answer published, so that the federation's role is the one it chose in public. The cabinet office prefers to answer privately first: a published acceptance is an acceptance the federation cannot revise.",
         ("Publish the invitation and the answer.", "Answer privately first.")),
        ("A Federation That Hosted the Peace",
         "The final review records what the federation accepted, declined and hosted, with the obligations each choice left. It names no treaty the parties did not sign.\n\nThe chair at the end of the table is in the record, with who sat in it.")),
)

OPENINGS = {
    "ERU": ("The Files of the Second Decade",
        "The cabinet meets with the files the years since the Continental War have left behind: the oversight instruments, the insurrection's records, the registers of the displaced and the agreements that put a joint international project within reach of the republic's coast.\n\n[ERU_lw_route_context]\n\nThe question before the cabinet is what kind of republic Erusea means to be in the decade the official record fills with a war, and how much of that argument to have in public.",
        ("Open the files to public questions.", "Begin with a protected cabinet docket.")),
    "FCU": ("Between Two Powers",
        "The treaty secretariat has collected every undertaking the federation has given since the Continental War: to its partners, to Erusea's provisional government and to its own citizens. The continent's two largest powers are now arguing over the projects around the elevator, and the federation lies between them.\n\n[FCU_lw_route_context]\n\nThe federal cabinet must decide what the federation will do if that argument becomes a war, and how much of that decision to make where its neighbours can see it.",
        ("Open the undertakings to public questions.", "Begin with a protected cabinet docket.")),
}

# (trigger, text): the first entry whose trigger holds is shown; None is the fallback.
ROUTE_CONTEXT = {
    "ERU": (("has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_fe_insurrection_defeated", "The ISAF's victory of 2005 and the oversight years that followed are in the files, with Free Erusea's insurrection and its defeat by Mobius 1 in 2006. The road the official record describes for 2019 runs through this history."),
            ("has_global_flag = ac_ucw_outcome_isaf_victory", "The ISAF's victory of 2005 and the oversight years that followed are in the files, with Free Erusea's insurrection among them. The road the official record describes for 2019 runs through this history."),
            ("has_global_flag = ac_ucw_outcome_erusean_victory", "The war ended in Erusea's favour. The files hold garrison returns and the accounts of districts the republic still administers; the official record's 2019 war belongs to a history this republic did not have."),
            ("has_global_flag = ac_ucw_outcome_stalemate", "The war ended in an armistice. The files hold the armistice terms and the incident reports from the line; the official record's 2019 war belongs to a history this republic did not have."),
            ("has_global_flag = ac_ucw_war_averted", "The war many expected did not come. The files hold the emergency rules written for it; the official record's 2019 war belongs to a history this republic did not have."),
            (None, "The files hold the records of the Continental War years and the obligations they left behind.")),
    "FCU": (("ac_ucw_outcome_isaf_victory", "Since 2005 the federation has supported Erusea's provisional government under ISAF oversight, and it has watched that oversight end."),
            ("has_global_flag = ac_ucw_outcome_erusean_victory", "The Continental War ended in Erusea's favour, and the federation's undertakings were made for a continent that war reshaped."),
            ("has_global_flag = ac_ucw_outcome_stalemate", "The Continental War ended in an armistice, and several undertakings assumed a peace treaty that was never signed."),
            ("has_global_flag = ac_ucw_war_averted", "The Continental War did not come, and several undertakings were made for a war that never started."),
            (None, "Several undertakings were made for circumstances that have since changed.")),
}

FINALS = {
    "ERU": ("The Republic That Remains",
        "The cabinet's last review of the period lists what the republic now does on its own authority, what it does under obligations it chose to keep and what the war, if there was one, decided for it. It names the offices responsible for each.\n\nErusea after the Lighthouse War is not the country its ministers would have designed. It is one whose government can be held to account for what it did, by its own people as well as by its neighbours.",
        {"army_org_factor": 0.02}),
    "FCU": ("A Federation That Chose Its Part",
        "The final account of the period is a list of the parts the federation chose: in the air, on the roads, in the dark and at the table. Some it played in full. Some it declined, with the reason recorded.\n\nThe federation has not become a different kind of power. It has become one whose neighbours can read, in one place, what it said it would do and what it did.",
        {"supply_consumption_factor": -0.02}),
}

ERU_SETTLEMENTS = " ".join(f"has_country_flag = ERU_lw_{k}_settlement_done" for k in ("sovereignty", "standing", "elevator", "alicorn", "drones", "lighthouse", "capital", "secession"))
FCU_SETTLEMENTS = " ".join(f"has_country_flag = FCU_lw_{k}_settlement_done" for k in ("airspace", "corridor", "blackout"))

# Services that clear the blackout idea: the capital's second service and the federation's first.
_EXTRA = {
    ("ERU", "capital"): dict(service_effect=guard("has_country_flag = ERU_lw_capital_service_2_completed", "remove_ideas = ac_lhw_usea_blackout")),
    ("FCU", "blackout"): dict(service_effect=guard("has_country_flag = FCU_lw_blackout_service_1_completed", "remove_ideas = ac_lhw_usea_blackout")),
}
BRANCHES = tuple(Branch(**{**b.__dict__, **_EXTRA.get((b.tag, b.key), {})}) for b in BRANCHES)

WAVE = Wave(
    prefix=P, infix="lw", label="The Lighthouse War", source="tools/content_waves",
    countries={"ERU": "Erusea", "FCU": "Central Usea"},
    eligible="date > 2009.12.31",
    branches=BRANCHES,
    layout={"ERU_sovereignty": (6, 22), "ERU_standing": (12, 22), "ERU_elevator": (18, 22), "ERU_alicorn": (24, 22), "ERU_drones": (30, 22),
            "ERU_capital": (6, 28), "ERU_ceasefire": (12, 28), "ERU_lighthouse": (18, 28), "ERU_secession": (24, 28),
            "FCU_airspace": (8, 22), "FCU_corridor": (14, 22), "FCU_blackout": (20, 22), "FCU_settlement": (26, 22)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"ERU": f"has_country_flag = ERU_lw_ceasefire_settlement_done OR = {{ {ERU_SETTLEMENTS} }}",
                 "FCU": f"has_country_flag = FCU_lw_settlement_settlement_done OR = {{ {FCU_SETTLEMENTS} }}"},
    themes={"ERU": ("satellite", "security"), "FCU": ("radar", "diplomacy"), "OSE": ("air", "navy")},
    weekly_extra={"ERU": "ac_lhw_owner_weekly = yes\n"},
    event_base=50,
    extra_tags=("OSE",),
)

# Owner -------------------------------------------------------------------------
CALENDAR = "2019.1.31"       # the owner's calendar opens on 1 February 2019
ANCHOR = "2019.5.14"         # the declaration, 15 May 2019 (Chronicle, 2019 / 05.15)
LATE_LIMIT = "2019.5.15"     # a first observation on or after the anchor never replays any expired date
CEASEFIRE = "2019.11.30"     # the Expo City Conference, 1 December 2019 (Chronicle, 2019 / 12.01)
BLACKOUT_TAGS = ("ERU", "FCU", "SNS", "AMB", "UGE", "DEL", "NPT")   # the Continental War participants

# (name, "date >" anchor, extra condition, body, news event). Each fires once while the owned war runs untainted.
STAGES = (
    ("eastern_wind", "2019.5.16", "", "OSE = { add_timed_idea = { idea = ac_lhw_ose_eastern_wind days = 90 } }", 20),
    ("kestrel_ii", "2019.5.29", "", "OSE = { add_timed_idea = { idea = ac_lhw_ose_kestrel_ii_lost days = 90 } }", 21),
    ("harling", "2019.6.5", "", "", 22),
    ("stonehenge", "2019.8.18", "ac_lhw_stonehenge_available = yes",
     "set_global_flag = ac_lhw_stonehenge_battery_reactivated\nOSE = { add_timed_idea = { idea = ac_lhw_ose_stonehenge_battery days = 120 } }\n" +
     guard("has_global_flag = ac_lhw_birds_over_elevator",
           "set_global_flag = ac_lhw_liberty_lost\nremove_ideas = ac_lhw_eru_arsenal_birds_two\nadd_ideas = ac_lhw_eru_arsenal_bird_one"), 24),
    ("farbanti", "2019.9.18", "ac_lhw_osean_foothold = yes",
     "add_timed_idea = { idea = ac_lhw_eru_capital_attacked days = 60 }\nset_global_flag = ac_lhw_usea_blackout\n" +
     "".join(guard(f"country_exists = {t}", f"{t} = {{ add_timed_idea = {{ idea = ac_lhw_usea_blackout days = 90 }} }}") for t in BLACKOUT_TAGS), 25),
    ("secession", "2019.9.30", "", "add_timed_idea = { idea = ac_lhw_eru_internal_conflict days = 120 }", 26),
    ("labarthe", "2019.10.9", "", "", 27),
    ("elevator_clash", "2019.10.30", "",
     "set_global_flag = ac_lhw_arsenal_birds_lost\nremove_ideas = ac_lhw_eru_arsenal_birds_two\nremove_ideas = ac_lhw_eru_arsenal_bird_one", 28),
)

# Every idea the owner adds without a timer; all are removed when the war ends.
WAR_IDEAS = ("ac_lhw_eru_war_footing", "ac_lhw_ose_war_footing", "ac_lhw_eru_elevator_held",
             "ac_lhw_eru_arsenal_birds_two", "ac_lhw_eru_arsenal_bird_one", "ac_lhw_ose_strike_group")


def owner():
    effects, triggers, loc, ideas, events = {}, {}, {}, [], []

    def idea(ident, title, description, values):
        loc[ident] = title
        loc[ident + "_desc"] = description
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" +
                           block("modifier", "\n".join(f"{k} = {v}" for k, v in values.items()))))

    def news(number, picture):
        events.append(block("news_event", f"id = {P}.{number}\ntitle = {P}.{number}.t\ndesc = {P}.{number}.d\npicture = GFX_{picture}\n"
                            "is_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" + block("option", f"name = {P}.{number}.a")))

    # Triggers ---------------------------------------------------------------------
    triggers["ac_lhw_principals"] = "country_exists = ERU country_exists = OSE"
    triggers["ac_lhw_war_running"] = f"{STARTED} NOT = {{ {ENDED} }}"
    triggers["ac_lhw_course_open"] = f"ac_lhw_war_running = yes NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} ac_lhw_principals = yes"
    triggers["ac_lhw_pair_at_war"] = "ac_lhw_principals = yes ERU = { has_war_with = OSE }"
    triggers["ac_lhw_can_declare"] = ("tag = ERU original_tag = ERU has_capitulated = no is_subject = no country_exists = OSE "
                                      f"OSE = {{ has_capitulated = no is_subject = no }} NOT = {{ has_war_with = OSE }} {ROUTE_SETTLED}")
    triggers["ac_lhw_restraint_earned"] = ("tag = ERU original_tag = ERU has_country_flag = ERU_fe_oversight_settlement_done "
                                           "has_country_flag = ERU_lw_sovereignty_policy_a_done")
    # A principal's own subjects follow it into the war and are not third parties; faction members and everyone else are.
    triggers["ac_lhw_third_party_present"] = ("any_country = { NOT = { tag = ERU } NOT = { tag = OSE } NOT = { is_subject_of = ERU } NOT = { is_subject_of = OSE } "
                                              "OR = { has_war_with = ERU has_war_with = OSE } }")
    triggers["ac_lhw_osean_foothold"] = "country_exists = OSE OSE = { any_controlled_state = { is_core_of = ERU } }"
    triggers["ac_lhw_birds_available"] = "has_global_flag = ac_sp_arsenal_birds_complete NOT = { has_global_flag = ac_lhw_arsenal_birds_lost }"
    triggers["ac_lhw_stonehenge_available"] = "has_global_flag = ac_ucw_stonehenge_operational"
    triggers["ac_lhw_principal_fallen"] = ("OR = { NOT = { country_exists = ERU } NOT = { country_exists = OSE } has_global_flag = ac_lhw_eru_fallen "
                                           "has_global_flag = ac_lhw_ose_fallen ERU = { has_capitulated = yes } OSE = { has_capitulated = yes } }")

    # Owner effects ------------------------------------------------------------------
    effects["ac_lhw_restore"] = guard(f"ac_lhw_war_running = yes NOT = {{ {EXISTING} }}",
        guard("tag = ERU NOT = { has_idea = ac_lhw_eru_war_footing }", "add_ideas = ac_lhw_eru_war_footing") +
        guard("country_exists = OSE OSE = { NOT = { has_idea = ac_lhw_ose_war_footing } }", "OSE = { add_ideas = ac_lhw_ose_war_footing }"))
    effects["ac_lhw_calendar_tick"] = guard(
        f"date > {CALENDAR} NOT = {{ has_global_flag = ac_lhw_calendar_started }} NOT = {{ {CLOSED} }}",
        guard(f"date < {LATE_LIMIT} ac_lhw_principals = yes {ISAF}", "set_global_flag = ac_lhw_calendar_started") +
        block("else_if", block("limit", f"NOT = {{ {ISAF} }}") + "set_global_flag = ac_lhw_closed\nset_global_flag = ac_lhw_route_unreachable") +
        block("else_if", block("limit", "NOT = { ac_lhw_principals = yes }") + "set_global_flag = ac_lhw_closed\nset_global_flag = ac_lhw_principal_missing") +
        block("else", "set_global_flag = ac_lhw_closed\nset_global_flag = ac_lhw_late_start_skipped"))
    settle = "clr_country_flag = ac_lhw_declaration_pending\nclr_country_flag = ac_lhw_declaration_window\n"
    # A war the pair already fights is recorded as started but not as expanded.
    effects["ac_lhw_observe_existing_war"] = guard(f"ac_lhw_pair_at_war = yes {ROUTE_SETTLED}",
        settle + "set_global_flag = ac_lhw_started\nset_global_flag = ac_lhw_existing_war_observed\nnews_event = { id = ac_lhw.3 days = 1 }")
    effects["ac_lhw_taint"] = guard(f"ac_lhw_war_running = yes NOT = {{ {TAINTED} }}", "set_global_flag = ac_lhw_tainted")
    # The owner's state is written only if the engine actually created the war.
    effects["ac_lhw_declare"] = guard("ac_lhw_can_declare = yes",
        guard("OR = { has_war = yes OSE = { has_war = yes } }", "set_global_flag = ac_lhw_pre_existing_war") +
        "declare_war_on = { target = OSE type = topple_government }\n" + settle +
        guard("has_war_with = OSE",
              "set_global_flag = ac_lhw_started\nadd_ideas = ac_lhw_eru_war_footing\nadd_ideas = ac_lhw_eru_elevator_held\n"
              "OSE = { add_ideas = ac_lhw_ose_war_footing add_timed_idea = { idea = ac_lhw_ose_ports_struck days = 90 } }\nnews_event = { id = ac_lhw.1 days = 1 }\n" +
              guard("has_global_flag = ac_lhw_pre_existing_war", "ac_lhw_taint = yes\nnews_event = { id = ac_lhw.4 days = 2 }") +
              guard("ac_lhw_birds_available = yes",
                    "set_global_flag = ac_lhw_birds_over_elevator\nadd_ideas = ac_lhw_eru_arsenal_birds_two\n"
                    "OSE = { remove_ideas = ac_sp_arsenal_birds_elevator_screen }\nnews_event = { id = ac_lhw.29 days = 2 }")) +
        block("else", "clr_global_flag = ac_lhw_pre_existing_war\nset_global_flag = ac_lhw_closed\nset_global_flag = ac_lhw_declaration_refused"))
    effects["ac_lhw_withhold"] = guard("ac_lhw_can_declare = yes ac_lhw_restraint_earned = yes",
        "set_global_flag = ac_lhw_declaration_withheld\n" + settle +
        "add_timed_idea = { idea = ac_lhw_eru_restraint_kept days = 365 }\nnews_event = { id = ac_lhw.2 days = 1 }")
    effects["ac_lhw_declaration_tick"] = guard(
        f"has_global_flag = ac_lhw_calendar_started date > {ANCHOR} {ROUTE_SETTLED}",
        guard("ac_lhw_pair_at_war = yes", "ac_lhw_observe_existing_war = yes") +
        block("else_if", block("limit", "ac_lhw_can_declare = yes") +
              guard("NOT = { has_country_flag = ac_lhw_declaration_asked }",
                    "set_country_flag = ac_lhw_declaration_asked\nset_country_flag = ac_lhw_declaration_pending\n"
                    "set_country_flag = { flag = ac_lhw_declaration_window days = 14 }\ncountry_event = { id = ac_lhw.5 days = 1 }") +
              block("else_if", block("limit", "has_country_flag = ac_lhw_declaration_pending NOT = { has_country_flag = ac_lhw_declaration_window }") +
                    "ac_lhw_declare = yes")) +
        block("else", settle + "set_global_flag = ac_lhw_closed\nset_global_flag = ac_lhw_principal_unable"))
    remove_all = "".join(f"remove_ideas = {i}\n" for i in WAR_IDEAS)

    def end_news(number, survivor):
        return (guard(f"country_exists = {survivor} NOT = {{ has_global_flag = ac_lhw_{survivor.lower()}_fallen }}",
                      f"{survivor} = {{ news_event = {{ id = ac_lhw.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_lhw.{number} days = 1 }}"))

    def survivor_news(number):
        return (guard("country_exists = ERU NOT = { has_global_flag = ac_lhw_eru_fallen }", f"ERU = {{ news_event = {{ id = ac_lhw.{number} days = 1 }} }}") +
                block("else_if", block("limit", "country_exists = OSE NOT = { has_global_flag = ac_lhw_ose_fallen }") +
                      f"OSE = {{ news_event = {{ id = ac_lhw.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_lhw.{number} days = 1 }}"))
    not_external = "NOT = { has_global_flag = ac_lhw_external_fall }"
    # A victory is recorded only when a principal fell to the other principal in their own war; the
    # ceasefire outcome only when the owner's own signing removed the war; everything else is a cessation.
    effects["ac_lhw_record_end"] = guard("ac_lhw_war_running = yes",
        "set_global_flag = ac_lhw_ended\n" +
        guard(f"{not_external} OR = {{ NOT = {{ country_exists = ERU }} has_global_flag = ac_lhw_eru_fallen ERU = {{ has_capitulated = yes }} }}",
              "set_global_flag = ac_lhw_outcome_osean_victory\n" + end_news(9, "OSE")) +
        block("else_if", block("limit", f"{not_external} OR = {{ NOT = {{ country_exists = OSE }} has_global_flag = ac_lhw_ose_fallen OSE = {{ has_capitulated = yes }} }}") +
              "set_global_flag = ac_lhw_outcome_erusean_victory\n" + end_news(10, "ERU")) +
        block("else_if", block("limit", "has_global_flag = ac_lhw_ceasefire_signed") +
              "set_global_flag = ac_lhw_outcome_ceasefire\n" +
              guard(f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} has_global_flag = ac_lhw_stage_elevator_clash NOT = {{ has_global_flag = ac_lhw_ceasefire_early }}",
                    "set_global_flag = ac_lhw_historical_course") +
              guard("has_global_flag = ac_lhw_ceasefire_early", survivor_news(8)) + block("else", survivor_news(7))) +
        block("else_if", block("limit", f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }}") +
              "set_global_flag = ac_lhw_outcome_cessation\n" + survivor_news(11)) +
        block("else", "set_global_flag = ac_lhw_outcome_cessation\n" + survivor_news(12)) +
        guard("country_exists = ERU", "ERU = { " + remove_all.replace("\n", " ") + "}") +
        guard("country_exists = OSE", "OSE = { " + remove_all.replace("\n", " ") + "}"))
    effects["ac_lhw_observation_tick"] = guard("ac_lhw_war_running = yes",
        guard(f"NOT = {{ {TAINTED} }} ac_lhw_third_party_present = yes", "ac_lhw_taint = yes\nnews_event = { id = ac_lhw.4 days = 1 }") +
        guard("OR = { ac_lhw_principal_fallen = yes NOT = { ac_lhw_pair_at_war = yes } }", "ac_lhw_record_end = yes"))
    stages = ""
    for name, after, extra, body, number in STAGES:
        stages += guard(f"ac_lhw_course_open = yes date > {after} NOT = {{ has_global_flag = ac_lhw_stage_{name} }} {extra}".rstrip(),
                        f"set_global_flag = ac_lhw_stage_{name}\n" + body + ("\n" if body else "") + f"news_event = {{ id = ac_lhw.{number} days = 1 }}")
    effects["ac_lhw_stage_tick"] = stages
    # The scripted ceasefire (user decision 7): the only white_peace in the content waves. The owner's
    # state is written only if the engine actually ended the war; otherwise the war is observed to its real end.
    effects["ac_lhw_sign_ceasefire"] = guard("tag = ERU original_tag = ERU ac_lhw_war_running = yes ac_lhw_pair_at_war = yes NOT = { has_global_flag = ac_lhw_ceasefire_signed }",
        "clr_country_flag = ac_lhw_ceasefire_pending\nclr_country_flag = ac_lhw_ceasefire_window\nwhite_peace = OSE\n" +
        guard("NOT = { has_war_with = OSE }", "set_global_flag = ac_lhw_ceasefire_signed\nac_lhw_record_end = yes") +
        block("else", "set_global_flag = ac_lhw_ceasefire_not_made\nac_lhw_taint = yes"))
    effects["ac_lhw_fight_on"] = guard("tag = ERU original_tag = ERU ac_lhw_war_running = yes",
        "set_global_flag = ac_lhw_ceasefire_refused\nclr_country_flag = ac_lhw_ceasefire_pending\nclr_country_flag = ac_lhw_ceasefire_window\n"
        "add_timed_idea = { idea = ac_lhw_eru_fought_on days = 180 }\nnews_event = { id = ac_lhw.13 days = 1 }")
    effects["ac_lhw_ceasefire_tick"] = guard(
        f"ac_lhw_course_open = yes date > {CEASEFIRE} NOT = {{ has_global_flag = ac_lhw_ceasefire_refused }} NOT = {{ has_global_flag = ac_lhw_ceasefire_not_made }}",
        guard("NOT = { has_country_flag = ac_lhw_ceasefire_asked }",
              "set_country_flag = ac_lhw_ceasefire_asked\nset_country_flag = ac_lhw_ceasefire_pending\n"
              "set_country_flag = { flag = ac_lhw_ceasefire_window days = 14 }\ncountry_event = { id = ac_lhw.6 days = 1 }") +
        block("else_if", block("limit", "has_country_flag = ac_lhw_ceasefire_pending NOT = { has_country_flag = ac_lhw_ceasefire_window }") +
              "ac_lhw_sign_ceasefire = yes"))
    effects["ac_lhw_early_ceasefire"] = guard("tag = ERU original_tag = ERU ac_lhw_war_running = yes ac_lhw_pair_at_war = yes has_country_flag = ERU_lw_lighthouse_policy_b_done "
                                              "NOT = { has_global_flag = ac_lhw_ceasefire_signed } NOT = { has_global_flag = ac_lhw_ceasefire_early }",
        "set_global_flag = ac_lhw_ceasefire_early\nac_lhw_sign_ceasefire = yes\n" +
        guard("NOT = { has_global_flag = ac_lhw_ceasefire_signed }", "clr_global_flag = ac_lhw_ceasefire_early"))
    effects["ac_lhw_owner_weekly"] = guard("tag = ERU original_tag = ERU",
        "ac_lhw_calendar_tick = yes\nac_lhw_declaration_tick = yes\nac_lhw_observation_tick = yes\nac_lhw_stage_tick = yes\nac_lhw_ceasefire_tick = yes")
    effects["ac_lhw_owner_weekly_ose"] = guard("tag = OSE original_tag = OSE ac_lhw_war_running = yes NOT = { country_exists = ERU }", "ac_lhw_record_end = yes")
    # Only the principals themselves count as fallen; a breakaway with the same original tag does not.
    principal = "OR = { AND = { tag = ERU original_tag = ERU } AND = { tag = OSE original_tag = OSE } } ac_lhw_war_running = yes"
    fallen = guard("tag = OSE", "set_global_flag = ac_lhw_ose_fallen") + block("else", "set_global_flag = ac_lhw_eru_fallen")
    external = "set_global_flag = ac_lhw_external_fall\nac_lhw_taint = yes\n"
    effects["ac_lhw_interrupt_principal"] = guard(principal,
        fallen + guard("NOT = { OR = { AND = { tag = ERU has_war_with = OSE } AND = { tag = OSE has_war_with = ERU } } }", external) +
        "ac_lhw_record_end = yes")
    effects["ac_lhw_interrupt_external"] = guard(principal, fallen + external + "ac_lhw_record_end = yes")
    # Osean decisions; the engine charges their `cost` once.
    effects["ac_lhw_strike_group"] = guard("tag = OSE original_tag = OSE ac_lhw_war_running = yes NOT = { has_country_flag = OSE_lw_strike_group_done }",
        "set_country_flag = OSE_lw_strike_group_done\nset_global_flag = ac_lhw_lrssg_formed\nadd_ideas = ac_lhw_ose_strike_group\nnews_event = { id = ac_lhw.23 days = 1 }")
    effects["ac_lhw_repair_ports"] = guard("tag = OSE original_tag = OSE has_idea = ac_lhw_ose_ports_struck",
        "remove_ideas = ac_lhw_ose_ports_struck\nset_country_flag = OSE_lw_repair_ports_done")
    effects["ac_lhw_war_record_ose"] = guard(f"tag = OSE original_tag = OSE {ENDED} NOT = {{ has_country_flag = OSE_lw_war_record_done }}",
        "set_country_flag = OSE_lw_war_record_done\nadd_timed_idea = { idea = ac_lhw_ose_war_record days = 180 }")
    # Special-project completion effects (user decision 8). Each sets only its own completion flag.
    effects["ac_sp_arsenal_birds_complete_effect"] = guard("NOT = { has_global_flag = ac_lhw_arsenal_birds_lost }",
        "set_global_flag = ac_sp_arsenal_birds_complete\n" +
        guard("NOT = { has_idea = ac_sp_arsenal_birds_elevator_screen }", "add_ideas = ac_sp_arsenal_birds_elevator_screen"))
    effects["ac_sp_alicorn_complete_effect"] = ("set_global_flag = ac_sp_alicorn_complete\n" +
        guard("NOT = { has_idea = ac_sp_alicorn_cruiser }", "add_ideas = ac_sp_alicorn_cruiser"))

    # Ideas (provisional values) ---------------------------------------------------------
    idea("ac_lhw_eru_war_footing", "Erusea at War", "The ACES Chronicle records the Kingdom of Erusea's declaration of war on the Osean Federation for 15 May 2019 (2019 / 05.15). The kingdom is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_lhw_ose_war_footing", "Osea at War", "The ACES Chronicle records Erusea's declaration of war on the Osean Federation for 15 May 2019 (2019 / 05.15). The federation is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_lhw_eru_elevator_held", "The Space Elevator Held", "Erusean forces hold the International Space Elevator, as the Chronicle records (2019 / 05.15). Holding it steadies the kingdom and ties down its forces; the values are provisional gameplay.",
         {"stability_factor": 0.02, "army_org_factor": -0.02})
    idea("ac_lhw_eru_arsenal_birds_two", "Two Arsenal Birds Over the Elevator", "The official abstract records that Erusea seized control of the Arsenal Birds with the elevator (Abstracts, ACE COMBAT 7). Both unmanned aircraft the Osean project completed screen the elevator for Erusea; the modifier is provisional gameplay.",
         {"air_mission_efficiency": 0.04, "army_core_defence_factor": 0.03})
    idea("ac_lhw_eru_arsenal_bird_one", "One Arsenal Bird Over the Elevator", "The Chronicle records that the Arsenal Bird Liberty was shot down by a reactivated Stonehenge battery (2019 / 08.19). One of the two seized aircraft remains; the modifier is provisional gameplay.",
         {"air_mission_efficiency": 0.02, "army_core_defence_factor": 0.015})
    idea("ac_lhw_ose_ports_struck", "Four Ports Struck", "The Chronicle records terrorist strikes by drones at four major naval ports in Osea (2019 / 05.15). Naval coordination and repair suffer for ninety days; the value is provisional gameplay.",
         {"naval_coordination": -0.05, "repair_speed_factor": -0.05})
    idea("ac_lhw_ose_eastern_wind", "Operation Eastern Wind", "The Chronicle records that Osean forces work with the IUN Peacekeeping Force in Operation Eastern Wind and that the advance into Erusean-held territory has begun (2019 / 05.17). The operation strains supply for ninety days; the value is provisional gameplay.",
         {"supply_consumption_factor": 0.05, "war_support_factor": 0.02})
    idea("ac_lhw_ose_kestrel_ii_lost", "Kestrel II Lost", "The Chronicle records that the aircraft carrier Kestrel II, a cornerstone of the attack on Farbanti, was sunk and that the offensive ended in failure (2019 / 05.30). Naval coordination suffers for ninety days; the value is provisional gameplay.",
         {"naval_coordination": -0.05, "political_power_gain": -0.05})
    idea("ac_lhw_ose_strike_group", "The Long Range Strategic Strike Group", "The Chronicle records that Osean forces formed the Long Range Strategic Strike Group in hopes of ending the war quickly (2019 / 08.10). The group improves air missions until the fighting ends; the value is provisional gameplay.",
         {"air_mission_efficiency": 0.04, "political_power_gain": -0.03})
    idea("ac_lhw_ose_stonehenge_battery", "A Stonehenge Battery Reactivated", "The Chronicle records that Osean forces reactivated one of Stonehenge's anti-asteroid batteries (2019 / 08.19). The battery supports the federation's air defence for 120 days; the value is provisional gameplay.",
         {"static_anti_air_damage_factor": 0.05, "air_superiority_efficiency": 0.03})
    idea("ac_lhw_eru_capital_attacked", "Farbanti Under Attack", "The Chronicle records that Osean forces began an attack on Farbanti (2019 / 09.19). The capital's administration suffers for sixty days; the value is provisional gameplay.",
         {"political_power_gain": -0.1, "stability_factor": -0.02})
    idea("ac_lhw_usea_blackout", "The Continental Blackout", "The Chronicle records that an operation to destroy military satellites cut off network communications across the entire Usean continent (2019 / 09.19). Every Continental War participant feels it for ninety days; the value is provisional gameplay.",
         {"political_power_gain": -0.05, "production_factory_efficiency_gain_factor": -0.02})
    idea("ac_lhw_eru_internal_conflict", "Internal Conflict", "The Chronicle records that Shilage and other small nations annexed by Erusea declared independence, that Erusea refused to recognise them and that internal conflict followed (2019 / 10.01). The conflict weighs on the kingdom for 120 days; the value is provisional gameplay. No border changes.",
         {"stability_factor": -0.03, "political_power_gain": -0.05})
    idea("ac_lhw_eru_restraint_kept", "A Declaration Withheld", "Erusea's government withheld the declaration of war the ACES Chronicle records for 15 May 2019 (2019 / 05.15), under the treaty obligations it chose to keep. This earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "army_org_factor": -0.02, "political_power_gain": -0.03})
    idea("ac_lhw_eru_fought_on", "Fighting On Past Expo City", "Erusea refused the ceasefire the ACES Chronicle records for 1 December 2019 (2019 / 12.01) and fights on. This provisional alternative weighs on the kingdom for 180 days.",
         {"war_support_factor": -0.05, "stability_factor": -0.02})
    idea("ac_lhw_ose_war_record", "Osea: The War Record", "A public record of the Lighthouse War is being compiled for 180 days. It costs political attention and steadies a country that wants to know what happened. Provisional gameplay.",
         {"stability_factor": 0.02, "political_power_gain": -0.05})
    idea("ac_sp_arsenal_birds_elevator_screen", "The Arsenal Birds", "§YProvisional gameplay§! reward. Two unmanned Arsenal Birds, the prototype Liberty and the upgraded Justice, maintain a defensive radius around the International Space Elevator (Super Weapons, Arsenal Birds). Their effect lasts while Osea controls them.",
         {"air_superiority_efficiency": 0.04, "army_core_defence_factor": 0.03})
    idea("ac_sp_alicorn_cruiser", "The Alicorn in Custody", "§YProvisional gameplay§! reward. The Erusean Royal Navy's submarine aviation cruiser Alicorn is complete and held under the custody rules the republic wrote for it (Super Weapons, Alicorn). It is never deployed by script.",
         {"naval_coordination": 0.05, "political_power_gain": -0.03})

    # Events ----------------------------------------------------------------------------
    texts = {
        1: ("The Lighthouse War Begins",
            "Terrorist strikes by drones have hit four major naval ports in Osea. On the same day the Kingdom of Erusea declared war on the Osean Federation, and Erusean forces captured the International Space Elevator. The war the ACES Chronicle calls the Lighthouse War has begun (2019 / 05.15).\n\nThe official product page records Erusea's stated grievance: it accuses Osea of massive overreach in their joint international projects. The Chronicle gives no reason for the declaration, and this campaign asserts none beyond the stated accusation. The war ends when the fighting actually ends, not on a calendar date.",
            "The continent is at war.", "ac_lhw_news_declaration"),
        2: ("The Declaration That Erusea Withheld",
            "15 May 2019 has passed without an Erusean declaration of war. The kingdom kept the treaty obligations it chose after the oversight years and withheld the declaration the ACES Chronicle records for this day (2019 / 05.15).\n\nThis is an earned alternative to the official record and is provisional gameplay. Osea has made no corresponding undertaking, and nothing prevents a later war by other means.",
            "Record the restraint.", "ac_lhw_news_withheld"),
        3: ("Osea and Erusea Already at War",
            "On the date the ACES Chronicle gives for Erusea's declaration of war on Osea (2019 / 05.15), the two countries were already fighting one another by other means.\n\nThe Lighthouse War owner records that war and observes it from outside: it asserts none of the official course and issues no further dated news. The war's end will be recorded when the fighting actually stops.",
            "Observe the war as it is.", "ac_lhw_news_observed"),
        4: ("Other Fighting Enters the Lighthouse War",
            "A third country is now at war with Osea or Erusea. The war between the two is no longer the complete explanation of the fighting, and the Lighthouse War owner moves to external observation.\n\nThe dated news of the official course stops here. The war's end will still be recorded when the fighting between Osea and Erusea actually stops.",
            "Observe the wider war.", "ac_lhw_news_expanded"),
        7: ("A Ceasefire at Expo City",
            "Osea and Erusea have signed a ceasefire treaty at the Expo City Conference, as the ACES Chronicle records for 1 December 2019 (2019 / 12.01). The fighting between them has stopped.\n\nThe official abstract records that a voluntary coalition of Osean forces and a traditionalist sect of the Erusean Army forced the surrender of the Erusean Army radicals before the ceasefire. This campaign asserts that only where its own course ran that far; it creates no coalition, sect or faction, and it records the end on the day the war actually ended.",
            "Begin the accounting.", "ac_lhw_news_end"),
        8: ("An Early Ceasefire",
            "Osea and Erusea have signed a ceasefire before the Expo City Conference the ACES Chronicle records for 1 December 2019 (2019 / 12.01). Erusea's elevator policy earned it the standing to offer one, and Osea accepted.\n\nThis is an earned alternative to the official record and is provisional gameplay. The fighting has stopped; the war's account begins.",
            "Begin the accounting.", "ac_lhw_news_end"),
        9: ("Erusea Capitulates",
            "Erusea has capitulated. The war between Osea and Erusea ends in an Osean victory.\n\nThe ACES Chronicle records a different end: a ceasefire treaty signed at the Expo City Conference on 1 December 2019 (2019 / 12.01). This outcome is the actual result of the campaign, not the official one.",
            "Record the outcome.", "ac_lhw_news_end"),
        10: ("Osea Capitulates",
             "Osea has capitulated. The war between Osea and Erusea ends in an Erusean victory.\n\nThe ACES Chronicle records a different end: a ceasefire treaty signed at the Expo City Conference on 1 December 2019 (2019 / 12.01). This outcome is the actual result of the campaign, not the official one.",
             "Record the outcome.", "ac_lhw_news_end"),
        11: ("The Lighthouse War Ends",
             "The fighting between Osea and Erusea has stopped. Neither country capitulated, and no ceasefire treaty was signed through this owner.\n\nThe ACES Chronicle records the war's end at the Expo City Conference on 1 December 2019 (2019 / 12.01). This campaign records the end on the day the fighting actually ceased, which is today.",
             "Begin the accounting.", "ac_lhw_news_end"),
        12: ("The Fighting Between Osea and Erusea Stops",
             "The fighting between Osea and Erusea has stopped. The Lighthouse War owner observed this war from outside and asserts nothing about how it was fought.\n\nThe ACES Chronicle's course for the war (2019 / 05.15 to 12.01) is not asserted here; the end is recorded on the day the fighting actually ceased.",
             "Record the cessation.", "ac_lhw_news_end"),
        13: ("Erusea Fights On",
             "Erusea has refused the ceasefire the ACES Chronicle records for the Expo City Conference (2019 / 12.01) and fights on.\n\nThis is a provisional alternative to the official record. The owner issues no further dated news; the war's end will be recorded when the fighting actually stops.",
             "The war goes on.", "ac_lhw_news_fought_on"),
        20: ("Operation Eastern Wind",
             "Osean forces are working with the IUN Peacekeeping Force in Operation Eastern Wind. The advance into Erusean-held territory has begun (2019 / 05.17).\n\nThe Chronicle names the operation and the force; this campaign creates neither and moves no territory by script.",
             "The advance begins.", "ac_lhw_news_eastern_wind"),
        21: ("Kestrel II Sunk",
             "A two-pronged offensive to secure Chopinburg airspace and attack the Erusean capital of Farbanti has failed. The aircraft carrier Kestrel II, a cornerstone of the attack on Farbanti, has been sunk (2019 / 05.30).\n\nThe Chronicle records the failure and the loss; no ship is represented and no state changes hands.",
             "Count the losses.", "ac_lhw_news_kestrel_ii"),
        22: ("Former President Harling Dies",
             "Osean forces attempted to rescue former president Vincent Harling from the space elevator. The former president was caught in an attack during the operation and died (2019 / 06.06).\n\nThe Chronicle does not say whose attack it was; the official abstract calls the rescue attempt botched. This campaign records the death as the record gives it and asserts nothing more.",
             "Mourn.", "ac_lhw_news_harling"),
        23: ("The Long Range Strategic Strike Group",
             "Osean forces have formed the Long Range Strategic Strike Group in hopes of ending the war quickly (2019 / 08.10).\n\nThe Chronicle names the group; this campaign creates no unit and records the decision as Osea's own.",
             "Form the group.", "ac_lhw_news_strike_group"),
        24: ("Stonehenge Fires Again",
             "Osean forces have reactivated one of Stonehenge's anti-asteroid batteries and shot down the Arsenal Bird Liberty (2019 / 08.19).\n\n[ac_lhw_liberty_text]",
             "The battery holds.", "ac_lhw_news_stonehenge"),
        25: ("Farbanti and the Blackout",
             "Osean forces have begun an attack on Farbanti. An operation to destroy military satellites has cut off network communications across the entire Usean continent (2019 / 09.19).\n\nThe Chronicle does not say whose operation it was, and this campaign does not. The blackout weighs on every Continental War participant for ninety days; the value is provisional gameplay. The attack is reported only because Osean forces actually hold Erusean ground; no territory was moved by script.",
             "The screens go dark.", "ac_lhw_news_blackout"),
        26: ("Declarations of Independence",
             "The autonomous state of Shilage and other small nations annexed by the Kingdom of Erusea have declared independence. The Erusean government refuses to recognise their independence, and internal conflict follows (2019 / 10.01).\n\n[ac_lhw_shilage_text]\n\nNo territory changes hands by script; the declarations are recorded as the Chronicle records them.",
             "Answer the declarations.", "ac_lhw_news_secession"),
        27: ("General Labarthe Killed",
             "Erusean conservative General Édouard Labarthe has been killed by Osean forces (2019 / 10.10).\n\nThe Chronicle gives the fact and his description; this campaign records no more.",
             "Note the record.", "ac_lhw_news_labarthe"),
        28: ("The Clash at the Space Elevator",
             "Osean and Erusean forces have clashed near the space elevator, and the Arsenal Bird Justice has been shot down (2019 / 10.31).\n\nThe official abstract records that a voluntary coalition of Osean forces and a traditionalist sect of the Erusean Army shot it down and forced the surrender of the Erusean Army radicals. This campaign records the clash and the loss; it creates no coalition, sect or faction.",
             "The sky over the elevator clears.", "ac_lhw_news_elevator_clash"),
        29: ("The Arsenal Birds Change Hands",
             "Erusea has seized control of the Arsenal Birds with the International Space Elevator, as the official abstract records for 15 May 2019 (Abstracts, ACE COMBAT 7).\n\nThe two unmanned aircraft the Osean project completed now screen the elevator for Erusea. The modifier is provisional gameplay; the aircraft remain text, not units.",
             "The birds fly for Erusea.", "ac_lhw_news_arsenal_birds"),
    }
    for number, (title, prose, label, picture) in texts.items():
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, label
        news(number, picture)
    loc.update({
        "ac_lhw.5.t": "The Declaration of 15 May 2019",
        "ac_lhw.5.d": "Drones have struck four major naval ports in Osea. The ACES Chronicle records that on this day the Kingdom of Erusea declared war on the Osean Federation and captured the International Space Elevator (2019 / 05.15). The official product page records the kingdom's stated grievance: massive Osean overreach in their joint international projects.\n\nThe government can declare the war the record describes, or withhold the declaration under the treaty obligations it chose to keep, if that record was earned: the oversight file closed and the obligations kept as policy. Withholding is a provisional alternative to the official record.",
        "ac_lhw.5.a": "Declare war on Osea.",
        "ac_lhw.5.b": "Withhold the declaration under the obligations kept.",
        "ac_lhw.6.t": "The Expo City Conference",
        "ac_lhw.6.d": "The ACES Chronicle records that Osea and Erusea signed a ceasefire treaty at the Expo City Conference on 1 December 2019 (2019 / 12.01).\n\nThe government can sign the ceasefire the record describes, or fight on. Fighting on is a provisional alternative; the owner then issues no further dated news, and the war's end is recorded when the fighting actually stops.",
        "ac_lhw.6.a": "Sign the ceasefire.",
        "ac_lhw.6.b": "Fight on.",
    })
    events.append(block("country_event", "id = ac_lhw.5\ntitle = ac_lhw.5.t\ndesc = ac_lhw.5.d\npicture = GFX_ac_lhw_event_eru_declaration\nis_triggered_only = yes\n"
                        "trigger = { tag = ERU original_tag = ERU ac_lhw_can_declare = yes }\n" +
                        block("option", "name = ac_lhw.5.a\nai_chance = { factor = 100 }\nac_lhw_declare = yes") +
                        block("option", "name = ac_lhw.5.b\ntrigger = { ac_lhw_restraint_earned = yes }\nai_chance = { factor = 0 }\nac_lhw_withhold = yes")))
    events.append(block("country_event", "id = ac_lhw.6\ntitle = ac_lhw.6.t\ndesc = ac_lhw.6.d\npicture = GFX_ac_lhw_event_eru_ceasefire\nis_triggered_only = yes\n"
                        "trigger = { tag = ERU original_tag = ERU ac_lhw_course_open = yes ac_lhw_pair_at_war = yes NOT = { has_global_flag = ac_lhw_ceasefire_signed } }\n" +
                        block("option", "name = ac_lhw.6.a\nai_chance = { factor = 100 }\nac_lhw_sign_ceasefire = yes") +
                        block("option", "name = ac_lhw.6.b\nai_chance = { factor = 0 }\nac_lhw_fight_on = yes")))

    # Decisions ---------------------------------------------------------------------------
    categories, decisions = [], {}
    category = "ac_lhw_ose_crisis"
    loc[category] = "Osea: The Lighthouse War"
    loc[category + "_desc"] = "[ac_lhw_status_text]\n\nThe war owner follows the ACES Chronicle's 2019 entries as reference anchors. It changes no territory, creates no unit and ends the war only when the fighting actually stops or the ceasefire is actually signed."
    categories.append(block(category, "icon = GFX_ac_lhw_category_ose\nallowed = { tag = OSE original_tag = OSE }\nvisible = { has_global_flag = ac_lhw_calendar_started }"))
    rows = []
    for key, title, description, visible, available, cost, effect in (
            ("strike_group", "Form the Long Range Strategic Strike Group", "Form the strike group the Chronicle records for 10 August 2019 (2019 / 08.10). Its air missions improve until the war ends. Once per war; provisional gameplay.",
             "ac_lhw_war_running = yes", "ac_lhw_war_running = yes date > 2019.8.9 has_capitulated = no NOT = { has_country_flag = OSE_lw_strike_group_done }", 50, "ac_lhw_strike_group = yes"),
            ("repair_ports", "Repair the Struck Ports", "Repair the four naval ports the drones struck (2019 / 05.15) and end the coordination penalty early. Once; provisional gameplay.",
             "has_idea = ac_lhw_ose_ports_struck", "has_idea = ac_lhw_ose_ports_struck has_capitulated = no NOT = { has_country_flag = OSE_lw_repair_ports_done }", 25, "ac_lhw_repair_ports = yes"),
            ("war_record", "Compile the War Record", "Compile a public record of the Lighthouse War over 180 days. It costs political attention and steadies the country. Once; provisional gameplay.",
             ENDED, f"{ENDED} has_capitulated = no NOT = {{ has_country_flag = OSE_lw_war_record_done }}", 25, "ac_lhw_war_record_ose = yes")):
        ident = f"OSE_lw_{key}"
        loc[ident], loc[ident + "_desc"] = title, description
        rows.append(block(ident, f"icon = ac_lhw_{ident}\nallowed = {{ tag = OSE original_tag = OSE }}\nvisible = {{ {visible} }}\navailable = {{ {available} }}\n"
                          f"cost = {cost}\nfire_only_once = yes\n" + block("complete_effect", effect) + "ai_will_do = { base = 3 }\n"))
    decisions[category] = rows
    ident = "ERU_lw_early_ceasefire"
    loc[ident] = "Offer an Early Ceasefire"
    loc[ident + "_desc"] = "Offer Osea a ceasefire before the Expo City Conference the Chronicle records for 1 December 2019 (2019 / 12.01). Requires the elevator kept running as policy. If the engine accepts the peace, the war ends now; this earned alternative is provisional gameplay."
    decisions["ac_lhw_eru_services"] = [block(ident, f"icon = ac_lhw_{ident}\nallowed = {{ tag = ERU original_tag = ERU }}\nvisible = {{ ac_lhw_war_running = yes }}\n"
                                              "available = { ac_lhw_war_running = yes ac_lhw_pair_at_war = yes has_country_flag = ERU_lw_lighthouse_policy_b_done NOT = { has_global_flag = ac_lhw_ceasefire_signed } }\n"
                                              "cost = 50\nfire_only_once = yes\n" + block("complete_effect", "ac_lhw_early_ceasefire = yes") + "ai_will_do = { base = 0 }\n")]
    # No-DLC fallback decisions for the two projects, under the shared Track C category.
    fallbacks = []
    for project, tag, available, cancel, days in (
            ("arsenal_birds", "OSE", "date > 2014.12.31 NOT = { has_global_flag = ac_sp_arsenal_birds_complete } NOT = { has_global_flag = ac_lhw_arsenal_birds_lost }",
             "has_global_flag = ac_lhw_arsenal_birds_lost", 300),
            ("alicorn", "ERU", "date > 2012.12.31 has_country_flag = ERU_lw_alicorn_operations_done NOT = { has_global_flag = ac_sp_alicorn_complete }", "", 400)):
        body = (f"icon = GFX_decision_ac_sp_{project}\n" + block("allowed", f'NOT = {{ has_dlc = "Gotterdammerung" }}\noriginal_tag = {tag}') +
                block("visible", f"always = yes\nNOT = {{ has_global_flag = ac_sp_{project}_complete }}") + block("available", available) +
                (block("cancel_trigger", block("OR", cancel)) if cancel else "") +
                f"fire_only_once = yes\ncost = 75\ndays_remove = {days}\n" + block("ai_will_do", "base = 5") +
                block("complete_effect", "custom_effect_tooltip = ac_superweapons_programme_started_tt") +
                block("remove_effect", guard(f"NOT = {{ has_global_flag = ac_sp_{project}_complete }}", f"ac_sp_{project}_complete_effect = yes")))
        fallbacks.append(block(f"ac_superweapons_{project}", body))
    decisions["ac_superweapons"] = fallbacks

    # Special projects (user decision 8) --------------------------------------------------------
    def project(ident, specialization, blueprint, tag, allowed, available, complexity, duration, reward, options, generic):
        unique = block(reward["name"], f"icon = GFX_{reward['name']}\nfire_only_once = yes\n" + block("threshold", "min = 0\nmax = 80") +
                       block("weight", reward["weight"]) + "".join(block("option", o) for o in options))
        return block(ident, f"specialization = {specialization}\nicon = GFX_{ident}\nblueprint_image = {blueprint}\n" +
                     block("project_tags", tag) + block("allowed", f"original_tag = {allowed}") + block("visible", "always = yes") +
                     block("available", available) + f"complexity = sp_complexity.{complexity}\nprototype_time = sp_time.prototype.{duration}\n" +
                     block("ai_will_do", "base = 10") + block("project_output", block("country_effects", f"{ident}_complete_effect = yes")) +
                     block("generic_prototype_rewards", "\n".join(generic)) + block("unique_prototype_rewards", unique))

    projects = (
        "# Source: Super Weapons, Arsenal Birds; Chronicle 2019 / 05.15, 08.19, 10.31. The availability date is provisional gameplay.\n" +
        project("ac_sp_arsenal_birds", "specialization_air", "GFX_ac_sp_blueprint_air_defence", "ac_sp_tag_unmanned_aviation", "OSE",
                "date > 2014.12.31\nNOT = { has_global_flag = ac_sp_arsenal_birds_complete }\nNOT = { has_global_flag = ac_lhw_arsenal_birds_lost }",
                "medium", "medium", dict(name="ac_sp_arsenal_birds_reward_elevator_trials", weight="base = 20"),
                ("token = ac_sp_arsenal_birds_reward_elevator_trials_two_airframes\ndefault = yes\n" +
                 block("iteration_output", block("country_effects", "add_political_power = -50\nFROM = { add_project_progress_ratio = constant:sp_progress.gain.medium }")),
                 "token = ac_sp_arsenal_birds_reward_elevator_trials_one_airframe\n" +
                 block("iteration_output", block("country_effects", "FROM = { add_project_progress_ratio = constant:sp_progress.gain.low }\nadd_stability = 0.02"))),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_air_defence")) +
        "\n# Source: Super Weapons, Alicorn. Construction and custody only; the cruiser is never deployed by script. Gate and timing are provisional gameplay.\n" +
        project("ac_sp_alicorn", "specialization_naval", "GFX_ac_sp_blueprint_naval", "ac_sp_tag_submarine_aviation", "ERU",
                "date > 2012.12.31\nFROM = { has_country_flag = ERU_lw_alicorn_operations_done }\nNOT = { has_global_flag = ac_sp_alicorn_complete }",
                "large", "long", dict(name="ac_sp_alicorn_reward_custody_crews",
                                     weight="base = 20\n" + block("modifier", "add = 40\nERU = { has_country_flag = ERU_lw_alicorn_settlement_done }")),
                ("token = ac_sp_alicorn_reward_custody_crews_written\ndefault = yes\n" +
                 block("iteration_output", block("country_effects", "FROM = { add_project_progress_ratio = constant:sp_progress.gain.low }\nadd_stability = 0.02")),
                 "token = ac_sp_alicorn_reward_custody_crews_fleet\n" +
                 block("iteration_output", block("country_effects", "add_political_power = -50\nFROM = { add_project_progress_ratio = constant:sp_progress.gain.medium }"))),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_naval")))
    loc.update({
        "ac_sp_arsenal_birds": "Arsenal Birds",
        "ac_sp_arsenal_birds_desc": "Massive unmanned aircraft to defend the International Space Elevator, powered by microwave energy sent from the elevator itself and resupplied by unmanned ships launched from the Tyler Island Mass Driver (Super Weapons, Arsenal Birds). Two are planned: the prototype Liberty and the upgraded Justice.\n\n§YProvisional gameplay§!: the opening date and reward values are balance choices. The Chronicle records both aircraft shot down in 2019.",
        "ac_sp_arsenal_birds_reward_elevator_trials": "Elevator Trials",
        "ac_sp_arsenal_birds_reward_elevator_trials_desc": "The first flight trials around the elevator show that the microwave power link holds further out than the design assumed. The programme can commit both airframes to the trials now, or keep the second on the ground until the first has flown a full rotation.",
        "ac_sp_arsenal_birds_reward_elevator_trials_two_airframes": "Fly both airframes",
        "ac_sp_arsenal_birds_reward_elevator_trials_one_airframe": "Fly one airframe first",
        "ac_sp_alicorn": "Alicorn",
        "ac_sp_alicorn_desc": "A nuclear-powered submarine for the Erusean Royal Navy's Rán Fleet: 495 metres long, both an aircraft carrier and a long-range railgun platform, designed to strike while submerged and beyond enemy reach (Super Weapons, Alicorn). Requires the submarine cruiser authorised and its custody rules set.\n\n§YProvisional gameplay§!: the gate, timing and reward values are balance choices. The cruiser is built and held in custody; it is never deployed by script.",
        "ac_sp_alicorn_reward_custody_crews": "Custody Crews",
        "ac_sp_alicorn_reward_custody_crews_desc": "The cruiser's first crew is being chosen while the hull is still in the yard. The custody rules the republic wrote can be built into the crew's training now, or the fleet can choose its own crew first and read the rules afterwards.",
        "ac_sp_alicorn_reward_custody_crews_written": "Train the crew to the custody rules",
        "ac_sp_alicorn_reward_custody_crews_fleet": "Let the fleet choose its crew",
        "ac_sp_tag_unmanned_aviation": "Unmanned Aviation Projects",
        "ac_sp_tag_unmanned_aviation_speed_factor": "Unmanned Aviation Projects Speed",
        "ac_sp_tag_unmanned_aviation_speed_factor_tt": " $ac_sp_tag_unmanned_aviation_speed_factor$: $RIGHT|+=%1$",
        "ac_sp_tag_submarine_aviation": "Submarine Aviation Projects",
        "ac_sp_tag_submarine_aviation_speed_factor": "Submarine Aviation Projects Speed",
        "ac_sp_tag_submarine_aviation_speed_factor_tt": " $ac_sp_tag_submarine_aviation_speed_factor$: $RIGHT|+=%1$",
        "ac_superweapons_arsenal_birds": "Arsenal Birds",
        "ac_superweapons_arsenal_birds_desc": "Without the special-projects feature, the Arsenal Birds programme runs as a timed decision and grants the same reward as the project (Super Weapons, Arsenal Birds). It is cancelled if the Chronicle's loss of both aircraft is reached first.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
        "ac_superweapons_alicorn": "Alicorn",
        "ac_superweapons_alicorn_desc": "Without the special-projects feature, the Alicorn programme runs as a timed decision and grants the same reward as the project (Super Weapons, Alicorn). Requires the submarine cruiser authorised and its custody rules set.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
    })

    # Defined texts and readable flags ----------------------------------------------------------
    status = (("has_global_flag = ac_lhw_outcome_osean_victory", "Ended: Erusea capitulated. The ceasefire the Chronicle records for 1 December 2019 did not occur."),
              ("has_global_flag = ac_lhw_outcome_erusean_victory", "Ended: Osea capitulated. The ceasefire the Chronicle records for 1 December 2019 did not occur."),
              ("has_global_flag = ac_lhw_historical_course", "Ended: the ceasefire was signed after the official course had run to the clash at the elevator. The Chronicle's Expo City date is a reference anchor; the war ended on the day it was actually signed."),
              ("has_global_flag = ac_lhw_ceasefire_early", "Ended: an early ceasefire was earned and signed before the Expo City date (earned alternative, provisional gameplay)."),
              ("has_global_flag = ac_lhw_outcome_ceasefire", "Ended: the ceasefire was signed before the official course had run its length. The Chronicle's Expo City date is a reference anchor."),
              (f"{ENDED} OR = {{ {TAINTED} {EXISTING} }}", "Ended: the fighting stopped while the owner observed the war from outside."),
              (ENDED, "Ended: the fighting stopped without a ceasefire signed through this owner. The Chronicle's Expo City date is a reference anchor."),
              ("has_global_flag = ac_lhw_ceasefire_refused ac_lhw_war_running = yes", "Running past the Expo City date: Erusea refused the ceasefire (provisional alternative); the official course is complete and the end will be recorded when the fighting stops."),
              ("has_global_flag = ac_lhw_ceasefire_not_made", "Running under external observation: the ceasefire was signed but the engine kept the war; the end will be recorded when the fighting stops."),
              (TAINTED, "Running under external observation: other fighting entered the war, and the official course is no longer asserted."),
              (EXISTING, "Running under external observation: Osea and Erusea were already at war when the Chronicle's declaration date came."),
              (STARTED, "Running on the official course since the declaration the Chronicle records for 15 May 2019 (2019 / 05.15)."),
              ("has_global_flag = ac_lhw_declaration_withheld", "Withheld: Erusea kept its obligations and did not declare (earned alternative, provisional gameplay)."),
              ("has_global_flag = ac_lhw_route_unreachable", "Closed: the Continental War did not end in an ISAF victory in this history, so the sourced 2019 route is unreachable. No war is invented in its place."),
              (CLOSED, "Closed: the principal pair could not fight the recorded war, or the record's dates had passed."),
              (None, "Pending: the ACES Chronicle records Erusea's declaration of war on Osea for 15 May 2019."))
    entries = ""
    for n, (condition, value) in enumerate(status):
        loc[f"ac_lhw_status_{n}"] = value
        entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + f"localization_key = ac_lhw_status_{n}")
    custom = block("defined_text", "name = ac_lhw_status_text\n" + entries)
    liberty = (("has_global_flag = ac_lhw_birds_over_elevator", "In this campaign the Arsenal Birds were completed and seized with the elevator; one remains over it. The modifier is provisional gameplay."),
               (None, "In this campaign no Arsenal Bird project was completed. The Chronicle's Liberty is recorded as the source names it; no airframe is represented."))
    shilage = (("country_exists = SHI", "Shilage exists as a country in this campaign. Its standing is its own, and this record changes nothing about it."),
               ("has_global_flag = ac_release_SHI_annexed", "Shilage was released and later annexed in this campaign. The declaration is recorded as the Chronicle records it; nothing is released by script."),
               ("has_global_flag = ac_release_SHI_was_absent", "Shilage is not a country in this campaign. The Chronicle's declaration is recorded in text only."),
               (None, "Whether Shilage exists as a country in this campaign is not changed by this record."))
    for name, rows_ in (("ac_lhw_liberty_text", liberty), ("ac_lhw_shilage_text", shilage)):
        entries = ""
        for n, (condition, value) in enumerate(rows_):
            loc[f"{name}_{n}"] = value
            entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + f"localization_key = {name}_{n}")
        custom += block("defined_text", f"name = {name}\n" + entries)
    for tag, rows_ in ROUTE_CONTEXT.items():
        entries = ""
        for n, (condition, value) in enumerate(rows_):
            key = f"{tag}_lw_route_context_{n}"
            loc[key] = value
            entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + "localization_key = " + key)
        custom += block("defined_text", f"name = {tag}_lw_route_context\n" + entries)
    loc.update({
        "ac_lhw_started": "The Lighthouse War has begun",
        "ac_lhw_tainted": "The Lighthouse War is under external observation",
        "ac_lhw_declaration_withheld": "Erusea withheld the 2019 declaration",
        "ac_lhw_ended": "The Lighthouse War has ended",
        "ac_lhw_closed": "The Lighthouse War owner is closed",
        "ac_lhw_calendar_started": "The Lighthouse War calendar is open",
        "ac_lhw_historical_course": "The Lighthouse War followed its official course",
        "ac_lhw_outcome_cessation": "The fighting between Osea and Erusea stopped without a ceasefire signed here",
        "ac_lhw_outcome_ceasefire": "Osea and Erusea signed a ceasefire",
        "ac_lhw_outcome_osean_victory": "Erusea capitulated",
        "ac_lhw_outcome_erusean_victory": "Osea capitulated",
        "ac_lhw_pre_existing_war": "A principal was already at war when the declaration came",
        "ac_lhw_existing_war_observed": "Osea and Erusea were already at war when the Chronicle's declaration date came",
        "ac_lhw_late_start_skipped": "The Chronicle's declaration date had passed before this content first loaded",
        "ac_lhw_principal_missing": "Osea or Erusea did not exist when the calendar opened",
        "ac_lhw_principal_unable": "Osea or Erusea could not fight the recorded war",
        "ac_lhw_route_unreachable": "The Continental War did not end in an ISAF victory, so the sourced 2019 route is unreachable",
        "ac_lhw_declaration_refused": "The engine did not create the declared war; the owner is closed",
        "ac_lhw_declaration_asked": "The Erusean government has been asked about the declaration",
        "ac_lhw_declaration_pending": "The Erusean declaration is pending",
        "ac_lhw_declaration_window": "The declaration window is open",
        "ac_lhw_ceasefire_asked": "The Erusean government has been asked about the ceasefire",
        "ac_lhw_ceasefire_pending": "The ceasefire answer is pending",
        "ac_lhw_ceasefire_window": "The ceasefire window is open",
        "ac_lhw_ceasefire_signed": "The ceasefire was signed",
        "ac_lhw_ceasefire_early": "An early ceasefire was earned and signed",
        "ac_lhw_ceasefire_refused": "Erusea refused the ceasefire and fought on",
        "ac_lhw_ceasefire_not_made": "The ceasefire was signed but the engine kept the war",
        "ac_lhw_eru_fallen": "Erusea has fallen during the Lighthouse War",
        "ac_lhw_ose_fallen": "Osea has fallen during the Lighthouse War",
        "ac_lhw_external_fall": "A principal fell to a third party, or outside the pair's own war",
        "ac_lhw_birds_over_elevator": "Erusea seized the Arsenal Birds with the elevator",
        "ac_lhw_liberty_lost": "The Arsenal Bird Liberty was shot down",
        "ac_lhw_arsenal_birds_lost": "Both Arsenal Birds were shot down",
        "ac_lhw_stonehenge_battery_reactivated": "A Stonehenge battery was reactivated",
        "ac_lhw_usea_blackout": "Network communications across Usea were cut",
        "ac_lhw_lrssg_formed": "The Long Range Strategic Strike Group was formed",
        "ac_lhw_principals": "Osea and Erusea both exist",
        "ac_lhw_war_running": "The Lighthouse War is running",
        "ac_lhw_course_open": "The Lighthouse War follows its official course",
        "ac_lhw_pair_at_war": "Osea and Erusea are at war",
        "ac_lhw_can_declare": "Erusea can declare the recorded war",
        "ac_lhw_restraint_earned": "Erusea closed the oversight file and keeps its treaty obligations as policy",
        "ac_lhw_third_party_present": "A third country is at war with Osea or Erusea",
        "ac_lhw_osean_foothold": "Osean forces control Erusean territory",
        "ac_lhw_birds_available": "The Arsenal Birds are complete and not lost",
        "ac_lhw_stonehenge_available": "Stonehenge was built",
        "ac_lhw_principal_fallen": "A principal has capitulated or fallen",
        "OSE_lw_strike_group_done": "The Long Range Strategic Strike Group has been formed",
        "OSE_lw_repair_ports_done": "The struck ports have been repaired",
        "OSE_lw_war_record_done": "The Osean record of the Lighthouse War is being compiled",
    })
    for name, _, _, _, number in STAGES:
        loc[f"ac_lhw_stage_{name}"] = "Lighthouse War stage: " + loc[f"{P}.{number}.t"]

    # FROM is the annexer, the capitulation winner or the overlord: only the other principal's win is a victory.
    hooks = {
        "on_startup": "if = { limit = { country_exists = ERU } ERU = { ac_lhw_restore = yes } }",
        "on_weekly_OSE": "ac_lhw_owner_weekly_ose = yes",
        "on_annex": ("if = { limit = { OR = { tag = OSE tag = ERU } } FROM = { ac_lhw_interrupt_principal = yes } }\n"
                     "else = { FROM = { ac_lhw_interrupt_external = yes } }"),
        "on_capitulation_immediate": ("if = { limit = { FROM = { OR = { tag = OSE tag = ERU } } } ac_lhw_interrupt_principal = yes }\n"
                                      "else = { ac_lhw_interrupt_external = yes }"),
        "on_subject_annexed": ("if = { limit = { FROM = { OR = { tag = OSE tag = ERU } } } ac_lhw_interrupt_principal = yes }\n"
                               "else = { ac_lhw_interrupt_external = yes }"),
    }
    ai = "\n".join((
        block("ac_lhw_eru_tension", "allowed = { original_tag = ERU }\n" +
              block("enable", f"has_global_flag = ac_lhw_calendar_started {ROUTE_SETTLED}") +
              "abort_when_not_enabled = yes\nai_strategy = { type = antagonize id = OSE value = 60 }"),
        block("ac_lhw_eru_war", "allowed = { original_tag = ERU }\n" + block("enable", "ac_lhw_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = OSE value = 150 }"),
        block("ac_lhw_ose_war", "allowed = { original_tag = OSE }\n" + block("enable", "ac_lhw_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = ERU value = 120 }"),
    ))
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                categories=categories, decisions=decisions, hooks=hooks, ai_strategy=ai,
                category_prefix={"ERU": "[ac_lhw_status_text]\n\n"},
                projects=projects, project_tags=["ac_sp_tag_unmanned_aviation", "ac_sp_tag_submarine_aviation"])


# Registry declarations ------------------------------------------------------
KEY = "F1"
NAME = "lighthouse"
IMPORTS = {"ERU": "LIGHTHOUSE WAR", "FCU": "LIGHTHOUSE WAR"}
LEDGER = "docs/CONTENT_WAVE_F1.md"
SOURCES = {"official": ["Chronicle 2019 / 05.15 to 12.01: the Lighthouse War",
                        "Abstracts, ACE COMBAT 7: the seized Arsenal Birds, the clean war, the coalition and the sect, Expo City",
                        "Product, ACE COMBAT 7: Erusea's stated grievance",
                        "Super Weapons: Arsenal Birds; Alicorn"],
           "mod_provenance": "Continental War outcome flags, Free Erusea records, Shilage release flags and the Stonehenge project state, read only",
           "provisional_gameplay": "Every focus, policy, service, dialogue and value; the windows, idea values and decisions; the scripted ceasefire; the two projects; the earned alternatives"}
NEWS_ART = (("ac_lhw_news_declaration", ("missile", "satellite"), "The Lighthouse War Begins", "ERU"),
            ("ac_lhw_news_withheld", ("document", "peace"), "The Declaration That Erusea Withheld", "ERU"),
            ("ac_lhw_news_observed", ("telescope", "satellite"), "Osea and Erusea Already at War", "OSE"),
            ("ac_lhw_news_expanded", ("telescope", "command"), "Other Fighting Enters the Lighthouse War", "OSE"),
            ("ac_lhw_news_end", ("peace", "assembly"), "The Lighthouse War Ends", "ERU"),
            ("ac_lhw_news_fought_on", ("command", "air"), "Erusea Fights On", "ERU"),
            ("ac_lhw_news_eastern_wind", ("logistics", "air"), "Operation Eastern Wind", "OSE"),
            ("ac_lhw_news_kestrel_ii", ("carrier", "navy"), "Kestrel II Sunk", "OSE"),
            ("ac_lhw_news_harling", ("satellite", "assembly"), "Former President Harling Dies", "OSE"),
            ("ac_lhw_news_strike_group", ("air", "command"), "The Long Range Strategic Strike Group", "OSE"),
            ("ac_lhw_news_stonehenge", ("radar", "air"), "Stonehenge Fires Again", "OSE"),
            ("ac_lhw_news_blackout", ("communications", "satellite"), "Farbanti and the Blackout", "ERU"),
            ("ac_lhw_news_secession", ("assembly", "gate"), "Declarations of Independence", "ERU"),
            ("ac_lhw_news_labarthe", ("command", "document"), "General Labarthe Killed", "ERU"),
            ("ac_lhw_news_elevator_clash", ("satellite", "air"), "The Clash at the Space Elevator", "OSE"),
            ("ac_lhw_news_arsenal_birds", ("air", "satellite"), "The Arsenal Birds Change Hands", "ERU"))
EVENT_ART = (("ac_lhw_event_eru_declaration", ("missile", "satellite"), "The Declaration of 15 May 2019", "ERU"),
             ("ac_lhw_event_eru_ceasefire", ("peace", "assembly"), "The Expo City Conference", "ERU"))
OWNER_ART = {
    "ac_lhw_eru_war_footing": ("command", "satellite", "ERU"), "ac_lhw_ose_war_footing": ("command", "navy", "OSE"),
    "ac_lhw_eru_elevator_held": ("satellite", "security", "ERU"), "ac_lhw_eru_arsenal_birds_two": ("air", "satellite", "ERU"),
    "ac_lhw_eru_arsenal_bird_one": ("air", "radar", "ERU"), "ac_lhw_ose_ports_struck": ("navy", "missile", "OSE"),
    "ac_lhw_ose_eastern_wind": ("logistics", "air", "OSE"), "ac_lhw_ose_kestrel_ii_lost": ("carrier", "navy", "OSE"),
    "ac_lhw_ose_strike_group": ("air", "command", "OSE"), "ac_lhw_ose_stonehenge_battery": ("radar", "missile", "OSE"),
    "ac_lhw_eru_capital_attacked": ("gate", "command", "ERU"), "ac_lhw_usea_blackout": ("communications", "satellite", "FCU"),
    "ac_lhw_eru_internal_conflict": ("assembly", "security", "ERU"), "ac_lhw_eru_restraint_kept": ("document", "peace", "ERU"),
    "ac_lhw_eru_fought_on": ("command", "air", "ERU"), "ac_lhw_ose_war_record": ("document", "scales", "OSE"),
    "ac_sp_arsenal_birds_elevator_screen": ("air", "satellite", "OSE"), "ac_sp_alicorn_cruiser": ("submarine", "navy", "ERU"),
}
PROJECT_ART = {
    "ac_sp_arsenal_birds": ("air", "satellite", "OSE", {"elevator_trials": "radar"}),
    "ac_sp_alicorn": ("submarine", "missile", "ERU", {"custody_crews": "navy"}),
}
