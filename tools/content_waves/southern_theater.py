"""Wave F2b: the Aurelia-Leasath war, 2020 (Package 5). Aurelia 30 and Leasath 30.

Source layers
-------------
Official (ACES site, read 4 November 2026; compiled in
docs/STRANGEREAL_2006_2020_SOURCES.md): the Chronicle's 2020 entries, which
give months but no days (10.XX, 11.XX, 12.XX) and, for Griswall, no month at
all (XX.XX); the ACE COMBAT X abstract and product blurb; the Super Weapons
rows for the Gleipnir and Archelon Fortress. Named people, squadrons, places
and weapons appear only in event text, as the source names them; none becomes
a unit, character, leader, state, border or tag. Leasath's "years of
exploitation" is recorded only as Leasath's stated claim.

Mod provenance, read only: the Leasath civil-war record (``ac_lcw_*``),
Aurelia's foundation records (``AUR_au_*``), the capitals' states (Aurelia
120, Leasath 134).

Provisional gameplay: every focus, policy, service, dialogue and value; the
month windows; idea values and decisions; the scripted ceasefire after the
commander's removal; the two special projects; the earned withheld
declaration and early settlement. The Nevera Jammer and the Meson Cannons
stay reference only: the record gives them no dates and the map has no
places for them.
"""
from content_waves.framework import Branch, Wave, block, guard

P = "ac_alc"
STARTED = "has_global_flag = ac_alc_started"
ENDED = "has_global_flag = ac_alc_ended"
TAINTED = "has_global_flag = ac_alc_tainted"
EXISTING = "has_global_flag = ac_alc_existing_war_observed"
CLOSED = "has_global_flag = ac_alc_closed"
AVOIDED = "OR = { has_global_flag = ac_alc_declaration_withheld has_global_flag = ac_alc_route_unreachable }"
ROUTE_SETTLED = f"NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_alc_declaration_withheld }} NOT = {{ {CLOSED} }}"
AUR_CAPITAL = 120
POSTWAR = "has_global_flag = ac_lcw_ended"

BRANCHES = (
    # Aurelia -------------------------------------------------------------------------
    Branch("AUR", "exile", (), STARTED,
        ("Govern From Aubrey", "A Government Abroad", "A Government at the Last Base",
         "Keep the Federation's Accounts", "Review an Exile Period", "The Federation Still Governs"),
        ("The ACES Chronicle records that Leasath's invasion caught Aurelia off guard and that almost the whole country fell under Leasath's control (2020 / 10.XX). The federal government must decide where it governs from while its capital is occupied.",
         "The cabinet will govern from a friendly capital abroad, safe from the fighting and close to the federation's creditors. It keeps the state's accounts and treaties; it governs a country it cannot see.",
         "The cabinet will govern from the last base still in Aurelian hands, beside the forces still fighting. It keeps the government visible to its soldiers; it puts the government within the enemy's reach.",
         "The federation's accounts, pensions and salaries will be kept and paid from wherever the government sits. A federation that still pays its people is still a federation.",
         "A completed, funded service period of government in exile must be reviewed before the arrangement becomes the federation's wartime constitution. The review counts what the ministries delivered and to whom.",
         "The settlement records how the federation governed while it was occupied. It names no date of return. It leaves a government its citizens could find."),
        (("assembly", "document"), ("diplomacy", "assembly"), ("assembly", "runway"), ("economy", "document"), ("scales", "assembly"), ("assembly", "peace")),
        (("Government abroad", {"political_power_gain": 0.05}, {"stability_factor": -0.02}),
         ("Government at the last base", {"stability_factor": 0.02}, {"army_core_defence_factor": -0.02})),
        (("Run the Exile Ministries", "Staff and fund the ministries operating in exile for one period.", "The cabinet office", {"political_power_gain": 0.08}),
         ("Pay the Displaced Service", "Pay the salaries and pensions of displaced civil servants.", "The treasury", {"stability_factor": 0.025})),
        ("A Minister Who Stayed in Griswall",
         "A deputy minister stayed in the occupied capital and keeps the water and power running under the occupation's orders. The occupiers tolerate him; the cabinet cannot decide whether he serves the federation or the invader.\n\nThe cabinet can recognise his work publicly, or say nothing and keep him on the payroll.",
         ("Recognise his work publicly.", "Say nothing and keep paying him.")),
        ("The Federation Still Governs",
         "The final review is a ledger of the exile government's work: salaries paid, permits issued, appeals answered. Some entries carry an occupied city's name.\n\nThe deputy minister who stayed is in the ledger, with the decision the cabinet took.")),
    Branch("AUR", "resistance", (), STARTED,
        ("Organise the Resistance", "Sabotage and Raids", "Records and Witnesses",
         "Protect the Resisters' Families", "Review a Resistance Period", "A Resistance on Record"),
        ("Aurelians in the occupied regions want to fight back, and the federation must decide what it asks of them. The interior ministry will organise a resistance that answers to the government.",
         "The resistance will sabotage the occupation's supply lines and raid its depots. Sabotage slows the occupier; it brings reprisals on the towns where it happens.",
         "The resistance will record what the occupation does: arrests, requisitions, abuses, with names and dates. Records do not stop the occupier today; they make sure it answers tomorrow.",
         "The families of resisters will be protected with money, false papers and routes out. A resistance that cannot protect its families will not last.",
         "A completed, funded service period under the chosen resistance must be reviewed before it becomes the federation's practice. The review counts what the resistance did and what it cost the towns.",
         "The settlement records the resistance the federation asked of its people and what they gave. It names no resister. It leaves an account the federation owes them."),
        (("security", "document"), ("missile", "logistics"), ("document", "scales"), ("shelter", "refugees"), ("scales", "security"), ("security", "peace")),
        (("Sabotage and raids", {"army_attack_factor": 0.03}, {"stability_factor": -0.02}),
         ("Records and witnesses", {"stability_factor": 0.02}, {"political_power_gain": -0.03})),
        (("Supply the Resistance", "Smuggle money and equipment to the resistance for one period.", "The interior ministry", {"army_org_factor": 0.03}),
         ("Protect the Families", "Move resisters' families out of reach for one period.", "The consular service", {"stability_factor": 0.025})),
        ("A Reprisal in a Mining Town",
         "After a raid on a depot, the occupation has arrested the mayor and twenty townspeople of a mining town. The resistance wants to raid again; the town's priest begs the government to stop.\n\nThe government can order the raids paused and say why, or leave the decision to the resistance commanders.",
         ("Pause the raids and say why.", "Leave it to the commanders.")),
        ("A Resistance on Record",
         "The final review lists what the resistance did and what the occupation did in return, town by town. The mining town is there, with what happened to its mayor.\n\nThe account is the federation's debt to the people who carried it.")),
    Branch("AUR", "liberation", (), STARTED,
        ("Plan the Liberation", "Return With Terms", "Return Without Terms",
         "Restore the Liberated Regions", "Review a Liberation Period", "A Federation Restored"),
        ("The official abstract records that the Aurelians recovered their territory region by region and retook the capital (Abstracts, ACE COMBAT X). Whatever the war brings, the government must plan for its return.",
         "The federation will offer Leasath terms once the capital is free: a ceasefire, prisoner exchanges and an accounting of the occupation. Terms end the fighting sooner; they leave questions open.",
         "The federation will return without offering terms and fight until Leasath stops. The government keeps every claim intact; the war lasts as long as Leasath can fight.",
         "Water, power and schools in the liberated regions will be restored in a published order. A region is liberated when its people can live in it again.",
         "A completed, funded service period of restoration must be reviewed before the liberation is declared complete. The review lists the services restored and the regions still waiting.",
         "The settlement records the federation's return and the terms it offered or withheld. It leaves a government back in its capital with a ledger of what the occupation cost."),
        (("gate", "civil"), ("peace", "document"), ("command", "gate"), ("civil", "rebuild"), ("scales", "civil"), ("civil", "peace")),
        (("Return with terms", {"stability_factor": 0.02}, {"war_support_factor": -0.02}),
         ("Return without terms", {"war_support_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Restore a Region's Utilities", "Repair water, power and transport in one liberated region.", "The infrastructure ministry", {"stability_factor": 0.025}),
         ("Reopen the Schools", "Restaff and resupply the liberated regions' schools.", "The education ministry", {"political_power_gain": 0.08})),
        ("The Occupation's Files",
         "The occupation administration left its files behind: requisitions, arrests and the names of those who worked with it. Every family in the liberated regions wants to know what is in them.\n\nThe justice ministry wants the files opened to the people named in them. The interior ministry wants them sealed for the courts.",
         ("Open the files to the people named.", "Seal the files for the courts.")),
        ("A Federation Restored",
         "The final review lists the liberated regions with the date each regained water, power and a school. The occupation's files are where the cabinet decided to put them.\n\nThe federation is back in its capital. The review says what it cost to get there.")),
    Branch("AUR", "recovery", (), ENDED,
        ("Count the War's Cost", "Rebuild First", "Compensate First",
         "Rebuild the Defences", "Review a Recovery Period", "After the Occupation"),
        ("The war is over. The federation that a pacifist constitution kept out of every war for a generation must now count what one war cost it, and decide what to pay first.",
         "Reconstruction comes first: roads, power, ports and housing, region by region. Rebuilding gets the economy moving; the people who lost family wait for their compensation.",
         "Compensation comes first: the families of the dead, the injured and the dispossessed, paid before the roads. Compensation keeps faith with the victims; the economy waits.",
         "The federation will rebuild its defences so that it is never caught with no means to fight back again. Defence costs the pacifist federation its oldest argument; the war settled it.",
         "A completed, funded service period of recovery must be reviewed before the federation declares the war's account settled. The review lists what was rebuilt and who was paid.",
         "The settlement records what the war cost Aurelia and what the federation paid back. It leaves a country that knows its losses, and a constitution that has had to answer the war."),
        (("rebuild", "civil"), ("rebuild", "industry"), ("scales", "refugees"), ("security", "command"), ("scales", "rebuild"), ("rebuild", "peace")),
        (("Rebuild first", {"production_factory_efficiency_gain_factor": 0.03}, {"stability_factor": -0.015}),
         ("Compensate first", {"stability_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Rebuild a Region", "Fund one period of reconstruction in a war-damaged region.", "The reconstruction office", {"production_factory_efficiency_gain_factor": 0.025}),
         ("Pay the War Claims", "Pay one period of compensation claims.", "The claims tribunal", {"stability_factor": 0.025})),
        ("A Claim From a Leasathian",
         "A Leasathian family has filed a claim with the federation's tribunal: their son, a conscript, was killed by Aurelian fire in a town he did not want to occupy. The tribunal's rules do not exclude foreigners.\n\nThe cabinet can let the tribunal hear the claim in public, or change the rules to exclude it.",
         ("Let the tribunal hear it.", "Change the rules.")),
        ("After the Occupation",
         "The final review lists what was rebuilt, who was paid and what the defences cost. The Leasathian family's claim is there, with the tribunal's ruling.\n\nThe federation is not the country it was before October. It knows what it lost.")),
    Branch("AUR", "neighbour", (), AVOIDED,
        ("Keep the Southern Peace", "A Joint Commission With Leasath", "A Watchful Border",
         "Open the Southern Crossings", "Review a Peace Period", "A Neighbour at Peace"),
        ("The war the ACES Chronicle records for October 2020 did not come in this history: Leasath withheld its declaration, or its civil war never ended in a way that allowed one. The federation will decide how to keep a peace it did not have to win.",
         "A joint commission with Leasath will meet each quarter on trade, the mines and the border. The commission gives both governments a place to argue before they act.",
         "The federation will keep its southern border watched and its forces ready, without provoking its neighbour. Readiness reassures the federation; it also tells Leasath what Aurelia expects.",
         "The crossings closed during Leasath's civil war will reopen on a published schedule. Open crossings make the peace visible to the people who live beside the border.",
         "A completed, funded service period under the chosen policy must be reviewed before it becomes settled practice. The review counts incidents, crossings and the commission's answers.",
         "The settlement records a peace this history kept and the official record did not. It leaves two neighbours that know how to argue without invading."),
        (("peace", "diplomacy"), ("diplomacy", "assembly"), ("security", "radar"), ("gate", "civil"), ("scales", "peace"), ("peace", "civil")),
        (("Joint commission", {"stability_factor": 0.03}, {"army_core_defence_factor": -0.02}),
         ("Watchful border", {"army_core_defence_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Hold a Commission Session", "Convene the joint commission on the quarter's disputes.", "The foreign ministry", {"political_power_gain": 0.08}),
         ("Staff the Crossings", "Staff the reopened crossings with customs and health officers.", "The border service", {"stability_factor": 0.025})),
        ("A Complaint About the Old Terms",
         "Leasath's delegation has tabled the old mining terms at the commission and called them exploitation. The federation's delegation can answer in public with its own figures, or ask for the item to be taken in closed session.",
         ("Answer in public with the figures.", "Ask for a closed session.")),
        ("A Neighbour at Peace",
         "The final review lists the commission's sessions, the incidents on the border and the complaint about the old terms, with each government's answer.\n\nThe list is long. None of its entries became a war.")),
    # Leasath -------------------------------------------------------------------------
    Branch("LEA", "war_government", (), STARTED,
        ("Govern the War", "The Commander Governs", "The Assembly Governs",
         "Report to the Country", "Review a War Government Period", "Who Decided the War"),
        ("The ACES Chronicle records that Leasath declared war on Aurelia, citing years of exploitation as its just cause (2020 / 10.XX). The country had just ended a civil war. Its leaders must decide who governs a country at war.",
         "The commander of the armed forces will govern for the duration: decrees instead of laws, officers instead of ministers. Decisions are quick; nobody outside the command knows why they were taken.",
         "The assembly will keep governing, with the commander answering to it. Civil government is slower; it keeps a record of who decided what.",
         "The war's conduct will be reported to the country each month: the casualties, costs and occupied regions. Reporting costs the government secrecy; it gives the country a reason to believe it.",
         "A completed, funded service period under the chosen arrangement must be reviewed before it becomes the country's wartime constitution. The review asks who decided, and on whose authority.",
         "The settlement records who governed Leasath's war. The official record names Diego Navarro as its chief orchestrator; this record names no officeholder and changes none. It leaves a record someone will read later."),
        (("command", "assembly"), ("command", "security"), ("assembly", "document"), ("assembly", "scales"), ("scales", "command"), ("document", "peace")),
        (("The commander governs", {"army_org_factor": 0.03}, {"stability_factor": -0.02}),
         ("The assembly governs", {"stability_factor": 0.02}, {"army_org_factor": -0.01})),
        (("Report to the Country", "Prepare and publish one month's report on the war.", "The cabinet office", {"stability_factor": 0.025}),
         ("Run the Decree Office", "Issue and record the war government's decrees for one period.", "The command's civil office", {"political_power_gain": 0.08})),
        ("Figures the Command Will Not Sign",
         "The month's report lists casualties higher than the command has announced. The command refuses to sign it; the assembly's clerk refuses to publish it unsigned.\n\nThe government can publish the report with the command's objection, or accept the command's figures.",
         ("Publish with the objection.", "Accept the command's figures.")),
        ("Who Decided the War",
         "The final review lists the war government's decisions with the body that took each one. The unsigned report is in the file, with the figures that turned out to be right.")),
    Branch("LEA", "occupation", (), STARTED,
        ("Administer the Occupied Regions", "A Civil Administration", "A Military Administration",
         "Account for the Requisitions", "Review an Occupation Period", "An Occupation on Record"),
        ("Leasathian forces hold Aurelian regions in this history, as the Chronicle records they held almost the whole country (2020 / 10.XX). Leasath must decide how it governs people who did not choose it.",
         "The occupied regions will be governed by civil administrators: food first, schools open, local officials kept where they will serve. The administration costs money and patience; it makes fewer enemies.",
         "The occupied regions will be governed by the army: curfews, requisitions and arrests at the commanders' discretion. Military rule secures the lines; it makes enemies of everyone it governs.",
         "Every requisition will be recorded with a receipt. A receipt is a promise that someone will be paid back.",
         "A completed, funded service period under the chosen administration must be reviewed before it becomes policy. The review counts what was taken, paid and owed.",
         "The settlement puts the occupation on record. It does not decide whether the regions are kept. Whoever reads it afterwards will know how they were governed."),
        (("gate", "document"), ("medical", "civil"), ("security", "gate"), ("scales", "document"), ("scales", "gate"), ("document", "peace")),
        (("Civil administration", {"stability_factor": 0.02}, {"consumer_goods_factor": 0.02}),
         ("Military administration", {"army_core_defence_factor": 0.03}, {"stability_factor": -0.02})),
        (("Run the Civil Administration", "Administer the occupied regions' food, schools and records for one period.", "The occupation's civil office", {"stability_factor": 0.025}),
         ("Audit the Requisitions", "Audit one period's requisitions against their receipts.", "The army's audit office", {"political_power_gain": 0.08})),
        ("Receipts Nobody Can Pay",
         "The audit has found thousands of requisition receipts for goods Leasath has no budget to pay for. Their holders are queuing outside the civil office.\n\nThe administration can publish the list and a payment schedule it cannot yet fund, or pay what it can and keep the rest in the file.",
         ("Publish the list and a schedule.", "Pay what can be paid.")),
        ("An Occupation on Record",
         "The final review lists the occupied regions with their administration, requisitions and receipts paid. The unpaid receipts are listed too.")),
    Branch("LEA", "aftermath", (), "has_global_flag = ac_alc_stage_removal",
        ("After the Commander", "A Transitional Government", "A Government of the Officers",
         "Bring the Soldiers Home", "Review a Transition Period", "Leasath After the War"),
        ("The Chronicle records that Leasath's commanding officer and the conflict's chief orchestrator, Diego Navarro, was removed from office and that the war ended (2020 / 12.XX). Whoever governs Leasath now must decide what kind of government it will be.",
         "A transitional government of civilians and officers will govern until elections, with a published timetable. The transition reassures Leasath's neighbours; it gives the officers a reason to wait.",
         "The officers will govern until order is restored, with no timetable. The officers keep the army together; the neighbours wonder what they will do with it.",
         "Soldiers will be brought home from the occupied regions on a published schedule. An army that comes home in order does not come home angry.",
         "A completed, funded service period of transition must be reviewed before the arrangement becomes the constitution. The review asks whether the timetable held.",
         "The settlement records Leasath's government after the war. It names no new leader. It leaves a country that must explain a war it started."),
        (("assembly", "ballot"), ("ballot", "assembly"), ("command", "security"), ("refugees", "rail"), ("scales", "assembly"), ("peace", "assembly")),
        (("Transitional government", {"stability_factor": 0.03}, {"army_org_factor": -0.02}),
         ("Government of the officers", {"army_org_factor": 0.02}, {"stability_factor": -0.02})),
        (("Demobilise a Formation", "Bring one formation home and discharge its conscripts.", "The general staff", {"stability_factor": 0.025}),
         ("Hold a Public Hearing", "Hold a public hearing on the war's conduct and costs.", "The assembly", {"political_power_gain": 0.08})),
        ("The Commander's Papers",
         "The removed commander's office has been sealed. His papers describe how the invasion was planned and who approved it. Several of the people named are in the new government.\n\nThe government can publish the papers, or hand them to a closed commission.",
         ("Publish the papers.", "Hand them to a closed commission.")),
        ("Leasath After the War",
         "The final review lists the government's decisions since the commander's removal, the soldiers brought home and the hearings held. The commander's papers are where the government decided to put them.")),
    Branch("LEA", "grievance", (), POSTWAR,
        ("State the Grievance", "Arbitration of the Old Terms", "The Grievance as Policy",
         "Publish the Mining Ledgers", "Review a Grievance Period", "A Grievance on the Record"),
        ("The official record says Leasath justified its 2020 war by citing years of exploitation by Aurelia. This campaign records that claim as Leasath's own and does not decide whether it is fair. After the civil war, the government must decide what to do with the grievance.",
         "Leasath will take the old mining terms to arbitration and accept the arbitrators' ruling. Arbitration may win back some of what Leasath believes it lost; it may also find that the terms were fair.",
         "Leasath will make the grievance national policy: speeches, schoolbooks and demands. A grievance as policy unites a country after a civil war; it also points it somewhere.",
         "The ledgers of every mine Aurelian firms ever worked in Leasath will be published, with what each paid. The ledgers are the evidence for the grievance, or against it.",
         "A completed, funded service period under the chosen policy must be reviewed before it becomes settled doctrine. The review asks what the evidence showed.",
         "The settlement records Leasath's grievance and what its government did with it. It does not judge the claim. It leaves the evidence where both countries can read it."),
        (("scales", "industry"), ("scales", "diplomacy"), ("assembly", "security"), ("document", "industry"), ("scales", "document"), ("document", "peace")),
        (("Arbitration of the old terms", {"stability_factor": 0.02}, {"war_support_factor": -0.03}),
         ("The grievance as policy", {"war_support_factor": 0.05}, {"stability_factor": -0.02})),
        (("Fund the Arbitration Case", "Fund one period of the arbitration case.", "The ministry of justice", {"political_power_gain": 0.08}),
         ("Publish the Ledgers", "Publish one period's recovered mining ledgers.", "The ministry of mines", {"stability_factor": 0.025})),
        ("A Ledger That Says Otherwise",
         "One recovered ledger shows that an Aurelian firm paid more in royalties than Leasath's own state mines did. The ministry of information wants it left out of the publication.\n\nThe government can publish every ledger, including this one, or publish a selection.",
         ("Publish every ledger.", "Publish a selection.")),
        ("A Grievance on the Record",
         "The final review lists the ledgers, the arbitration's progress and the speeches. The ledger that said otherwise is in the file, published or not, with the decision.")),
    Branch("LEA", "restraint", (), POSTWAR,
        ("Keep the Army at Home", "Restraint Toward Aurelia", "Readiness on the Border",
         "Keep the Channels Open", "Review a Restraint Period", "A Country That Did Not March"),
        ("Leasath is out of a civil war and its army is the strongest institution it has. The government must decide whether that army will be used abroad.",
         "Leasath will keep its army at home and answer Aurelia through talks, whatever the grievance. Restraint is the record the official history did not keep; it costs the government the army's patience.",
         "Leasath will keep its army ready on the Aurelian border, without crossing it. Readiness reassures the army; it tells Aurelia exactly what Leasath could do.",
         "Channels to Aurelia's government will be kept open at every level. A channel that is open in peacetime is the one that is used in a crisis.",
         "A completed, funded service period under the chosen policy must be reviewed before it becomes the country's settled practice. The review asks whether the army stayed home and the channels stayed open.",
         "The settlement records a choice the official record says Leasath did not make in October 2020. Policy A is the record Leasath needs to withhold its declaration; it claims nothing else."),
        (("peace", "command"), ("peace", "diplomacy"), ("security", "radar"), ("communications", "diplomacy"), ("scales", "peace"), ("peace", "assembly")),
        (("Restraint toward Aurelia", {"stability_factor": 0.03}, {"army_org_factor": -0.02}),
         ("Readiness on the border", {"army_core_defence_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Hold a Border Liaison Period", "Keep liaison officers meeting Aurelia's on a fixed schedule.", "The foreign ministry", {"political_power_gain": 0.08}),
         ("Exercise at Home", "Exercise the army well inside the country's borders.", "The general staff", {"army_org_factor": 0.03})),
        ("A General Who Wants the South",
         "A general who fought in the civil war has told cadets that Aurelia's wealth was built on Leasath's mines and that the army should take it back. He has a following.\n\nThe government can answer him in public, or retire him quietly.",
         ("Answer him in public.", "Retire him quietly.")),
        ("A Country That Did Not March",
         "The final review lists the army's exercises, the liaison meetings and the general's speech, with the government's answer.\n\nLeasath has its grievance and its army. It has kept them apart.")),
)

OPENINGS = {
    "AUR": ("A Pacifist Federation in 2020",
        "The cabinet meets with the federation's records of the years before 2020: its relations with Leasath, its readiness review and its account of what it owes. Across the southern border, Leasath's civil war has ended.\n\nThe question before the cabinet is what a federation that has kept out of every war owes its people if one comes to it, and how much of that answer to give in public.",
        ("Open the question to the public.", "Begin with a protected cabinet docket.")),
    "LEA": ("After Ten Years of War",
        "The cabinet meets with the records the civil war left: the provinces, the army, the mines and a grievance against Aurelia that every faction shared.\n\nThe question before the cabinet is what Leasath will do with its army and its grievance now that it is no longer fighting itself, and how much of that decision to make where its neighbour can see it.",
        ("Open the question to the public.", "Begin with a protected cabinet docket.")),
}
FINALS = {
    "AUR": ("A Federation Tested",
        "The last review of the period lists what the federation did when it was tested: where it governed from, what its people resisted, what it rebuilt and what it paid.\n\nAurelia is not the country it was before October. It knows what it can do.",
        {"army_org_factor": 0.02}),
    "LEA": ("A Country That Answered for Its War",
        "The last review of the period lists the decisions Leasath took after its civil war: the grievance, the army, the war and its end. Some entries are not to its credit; they are in the list.\n\nLeasath has a record of what it did. That is where an answer begins.",
        {"stability_factor": 0.02}),
}

WAVE = Wave(
    prefix=P, infix="sw", label="The Aurelia-Leasath War", source="tools/content_waves",
    countries={"AUR": "Aurelia", "LEA": "Leasath"}, eligible="date > 2018.12.31",
    branches=BRANCHES,
    layout={"AUR_exile": (2, 19), "AUR_resistance": (8, 19), "AUR_liberation": (14, 19), "AUR_recovery": (20, 19), "AUR_neighbour": (26, 19),
            "LEA_war_government": (2, 13), "LEA_occupation": (8, 13), "LEA_aftermath": (14, 13), "LEA_grievance": (20, 13), "LEA_restraint": (26, 13)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"AUR": "OR = { has_country_flag = AUR_sw_recovery_settlement_done has_country_flag = AUR_sw_neighbour_settlement_done has_country_flag = AUR_sw_liberation_settlement_done }",
                 "LEA": "OR = { has_country_flag = LEA_sw_aftermath_settlement_done has_country_flag = LEA_sw_restraint_settlement_done has_country_flag = LEA_sw_grievance_settlement_done }"},
    themes={"AUR": ("runway", "peace"), "LEA": ("command", "missile")},
    weekly_extra={"LEA": "ac_alc_owner_weekly = yes\n"},
    event_base=50,
)

# Owner -------------------------------------------------------------------------
CALENDAR = "2020.8.31"       # the owner's calendar opens on 1 September 2020
OCTOBER = ("2020.9.30", "2020.11.1")    # the declaration month; the Chronicle gives no day (2020 / 10.XX)
NOVEMBER = ("2020.10.31", "2020.12.1")
DECEMBER = ("2020.11.30", "2021.1.1")

# (name, (after, before) or None, extra condition, body, news event). Month windows have no day:
# each stage fires on the first observation inside its month, or is skipped once the month passes.
STAGES = (
    ("overrun", None, f"LEA = {{ controls_state = {AUR_CAPITAL} }}", "AUR = { add_ideas = ac_alc_aur_griswall_occupied }", 20),
    ("aubrey", OCTOBER, "", "", 21),
    ("port_patterson", NOVEMBER, "has_global_flag = ac_alc_stage_overrun", "", 22),
    ("gleipnir", NOVEMBER, "has_global_flag = ac_sp_gleipnir_complete",
     "set_global_flag = ac_alc_gleipnir_lost\nremove_ideas = ac_sp_gleipnir_fortress\nremove_ideas = ac_alc_lea_gleipnir_over_aurelia", 23),
    ("sachana", DECEMBER, "has_global_flag = ac_alc_stage_overrun", "", 24),
    ("griswall", None, f"has_global_flag = ac_alc_stage_overrun AUR = {{ controls_state = {AUR_CAPITAL} }}",
     "AUR = { remove_ideas = ac_alc_aur_griswall_occupied }", 25),
    ("removal", DECEMBER, "", "add_timed_idea = { idea = ac_alc_lea_commander_removed days = 120 }", 26),
    ("archelon", DECEMBER, "has_global_flag = ac_sp_archelon_complete",
     "set_global_flag = ac_alc_archelon_lost\nremove_ideas = ac_sp_archelon_works", 27),
)

WAR_IDEAS = ("ac_alc_lea_war_footing", "ac_alc_aur_war_footing", "ac_alc_aur_griswall_occupied", "ac_alc_lea_gleipnir_over_aurelia")


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

    triggers["ac_alc_principals"] = "country_exists = AUR country_exists = LEA"
    triggers["ac_alc_war_running"] = f"{STARTED} NOT = {{ {ENDED} }}"
    triggers["ac_alc_course_open"] = f"ac_alc_war_running = yes NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} ac_alc_principals = yes"
    triggers["ac_alc_pair_at_war"] = "ac_alc_principals = yes LEA = { has_war_with = AUR }"
    triggers["ac_alc_can_declare"] = ("tag = LEA original_tag = LEA has_capitulated = no is_subject = no country_exists = AUR "
                                      f"AUR = {{ has_capitulated = no is_subject = no }} NOT = {{ has_war_with = AUR }} {ROUTE_SETTLED}")
    triggers["ac_alc_restraint_earned"] = ("tag = LEA original_tag = LEA has_country_flag = LEA_sw_restraint_policy_a_done "
                                           "AUR = { has_country_flag = AUR_au_relations_policy_a_done has_country_flag = AUR_au_readiness_settlement_done }")
    triggers["ac_alc_third_party_present"] = ("any_country = { NOT = { tag = AUR } NOT = { tag = LEA } NOT = { is_subject_of = AUR } NOT = { is_subject_of = LEA } "
                                              "OR = { has_war_with = AUR has_war_with = LEA } }")
    triggers["ac_alc_principal_fallen"] = ("OR = { NOT = { country_exists = AUR } NOT = { country_exists = LEA } has_global_flag = ac_alc_aur_fallen "
                                           "has_global_flag = ac_alc_lea_fallen AUR = { has_capitulated = yes } LEA = { has_capitulated = yes } }")

    effects["ac_alc_restore"] = guard(f"ac_alc_war_running = yes NOT = {{ {EXISTING} }}",
        guard("tag = LEA NOT = { has_idea = ac_alc_lea_war_footing }", "add_ideas = ac_alc_lea_war_footing") +
        guard("country_exists = AUR AUR = { NOT = { has_idea = ac_alc_aur_war_footing } }", "AUR = { add_ideas = ac_alc_aur_war_footing }"))
    # The sourced route needs Leasath's civil war over (any ending); a war still being fought closes it.
    effects["ac_alc_calendar_tick"] = guard(
        f"date > {CALENDAR} NOT = {{ has_global_flag = ac_alc_calendar_started }} NOT = {{ {CLOSED} }}",
        guard(f"date < {OCTOBER[1]} ac_alc_principals = yes {POSTWAR}", "set_global_flag = ac_alc_calendar_started") +
        block("else_if", block("limit", f"date < {OCTOBER[1]} NOT = {{ {POSTWAR} }}") + "set_global_flag = ac_alc_closed\nset_global_flag = ac_alc_route_unreachable") +
        block("else_if", block("limit", "NOT = { ac_alc_principals = yes }") + "set_global_flag = ac_alc_closed\nset_global_flag = ac_alc_principal_missing") +
        block("else", "set_global_flag = ac_alc_closed\nset_global_flag = ac_alc_late_start_skipped"))
    settle = "clr_country_flag = ac_alc_declaration_pending\nclr_country_flag = ac_alc_declaration_window\n"
    effects["ac_alc_observe_existing_war"] = guard(f"ac_alc_pair_at_war = yes {ROUTE_SETTLED}",
        settle + "set_global_flag = ac_alc_started\nset_global_flag = ac_alc_existing_war_observed\nnews_event = { id = ac_alc.3 days = 1 }")
    effects["ac_alc_taint"] = guard(f"ac_alc_war_running = yes NOT = {{ {TAINTED} }}", "set_global_flag = ac_alc_tainted")
    effects["ac_alc_declare"] = guard("ac_alc_can_declare = yes",
        guard("OR = { has_war = yes AUR = { has_war = yes } }", "set_global_flag = ac_alc_pre_existing_war") +
        "declare_war_on = { target = AUR type = topple_government }\n" + settle +
        guard("has_war_with = AUR",
              "set_global_flag = ac_alc_started\nadd_ideas = ac_alc_lea_war_footing\nAUR = { add_ideas = ac_alc_aur_war_footing }\n"
              "news_event = { id = ac_alc.1 days = 1 }\n" +
              guard("has_global_flag = ac_alc_pre_existing_war", "ac_alc_taint = yes\nnews_event = { id = ac_alc.4 days = 2 }") +
              guard("has_global_flag = ac_sp_gleipnir_complete NOT = { has_global_flag = ac_alc_gleipnir_lost }",
                    "add_ideas = ac_alc_lea_gleipnir_over_aurelia\nnews_event = { id = ac_alc.15 days = 2 }")) +
        block("else", "clr_global_flag = ac_alc_pre_existing_war\nset_global_flag = ac_alc_closed\nset_global_flag = ac_alc_declaration_refused"))
    effects["ac_alc_withhold"] = guard("ac_alc_can_declare = yes ac_alc_restraint_earned = yes",
        "set_global_flag = ac_alc_declaration_withheld\n" + settle +
        "add_timed_idea = { idea = ac_alc_lea_restraint_kept days = 365 }\nnews_event = { id = ac_alc.2 days = 1 }")
    effects["ac_alc_declaration_tick"] = guard(
        f"has_global_flag = ac_alc_calendar_started date > {OCTOBER[0]} {ROUTE_SETTLED}",
        guard("ac_alc_pair_at_war = yes", "ac_alc_observe_existing_war = yes") +
        block("else_if", block("limit", "ac_alc_can_declare = yes") +
              guard("NOT = { has_country_flag = ac_alc_declaration_asked }",
                    "set_country_flag = ac_alc_declaration_asked\nset_country_flag = ac_alc_declaration_pending\n"
                    "set_country_flag = { flag = ac_alc_declaration_window days = 14 }\ncountry_event = { id = ac_alc.5 days = 1 }") +
              block("else_if", block("limit", "has_country_flag = ac_alc_declaration_pending NOT = { has_country_flag = ac_alc_declaration_window }") +
                    "ac_alc_declare = yes")) +
        block("else", settle + "set_global_flag = ac_alc_closed\nset_global_flag = ac_alc_principal_unable"))
    remove_all = "".join(f"remove_ideas = {i}\n" for i in WAR_IDEAS)

    def end_news(number, survivor):
        return (guard(f"country_exists = {survivor} NOT = {{ has_global_flag = ac_alc_{survivor.lower()}_fallen }}",
                      f"{survivor} = {{ news_event = {{ id = ac_alc.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_alc.{number} days = 1 }}"))

    def survivor_news(number):
        return (guard("country_exists = AUR NOT = { has_global_flag = ac_alc_aur_fallen }", f"AUR = {{ news_event = {{ id = ac_alc.{number} days = 1 }} }}") +
                block("else_if", block("limit", "country_exists = LEA NOT = { has_global_flag = ac_alc_lea_fallen }") +
                      f"LEA = {{ news_event = {{ id = ac_alc.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_alc.{number} days = 1 }}"))
    not_external = "NOT = { has_global_flag = ac_alc_external_fall }"
    effects["ac_alc_record_end"] = guard("ac_alc_war_running = yes",
        "set_global_flag = ac_alc_ended\n" +
        guard(f"{not_external} OR = {{ NOT = {{ country_exists = LEA }} has_global_flag = ac_alc_lea_fallen LEA = {{ has_capitulated = yes }} }}",
              "set_global_flag = ac_alc_outcome_aurelian_victory\n" + end_news(9, "AUR")) +
        block("else_if", block("limit", f"{not_external} OR = {{ NOT = {{ country_exists = AUR }} has_global_flag = ac_alc_aur_fallen AUR = {{ has_capitulated = yes }} }}") +
              "set_global_flag = ac_alc_outcome_leasathian_victory\n" + end_news(10, "LEA")) +
        block("else_if", block("limit", "has_global_flag = ac_alc_ceasefire_signed") +
              "set_global_flag = ac_alc_outcome_ceasefire\n" +
              guard(f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} has_global_flag = ac_alc_stage_removal NOT = {{ has_global_flag = ac_alc_ceasefire_early }}",
                    "set_global_flag = ac_alc_historical_course") +
              guard("has_global_flag = ac_alc_ceasefire_early", survivor_news(8)) + block("else", survivor_news(7))) +
        block("else_if", block("limit", f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }}") +
              "set_global_flag = ac_alc_outcome_cessation\n" + survivor_news(11)) +
        block("else", "set_global_flag = ac_alc_outcome_cessation\n" + survivor_news(12)) +
        guard("country_exists = LEA", "LEA = { " + remove_all.replace("\n", " ") + "}") +
        guard("country_exists = AUR", "AUR = { " + remove_all.replace("\n", " ") + "}"))
    effects["ac_alc_observation_tick"] = guard("ac_alc_war_running = yes",
        guard(f"NOT = {{ {TAINTED} }} ac_alc_third_party_present = yes", "ac_alc_taint = yes\nnews_event = { id = ac_alc.4 days = 1 }") +
        guard("OR = { ac_alc_principal_fallen = yes NOT = { ac_alc_pair_at_war = yes } }", "ac_alc_record_end = yes"))
    stages = ""
    for name, window, extra, body, number in STAGES:
        fire = f"set_global_flag = ac_alc_stage_{name}\n" + body + ("\n" if body else "") + f"news_event = {{ id = ac_alc.{number} days = 1 }}"
        if window is None:
            stages += guard(f"ac_alc_course_open = yes NOT = {{ has_global_flag = ac_alc_stage_{name} }} {extra}".rstrip(), fire)
        else:
            stages += guard(f"ac_alc_course_open = yes date > {window[0]} NOT = {{ has_global_flag = ac_alc_stage_{name} }} NOT = {{ has_global_flag = ac_alc_stage_{name}_skipped }}",
                            guard(f"date < {window[1]} {extra}".rstrip(), fire) +
                            block("else_if", block("limit", f"NOT = {{ date < {window[1]} }}") + f"set_global_flag = ac_alc_stage_{name}_skipped"))
    effects["ac_alc_stage_tick"] = stages
    effects["ac_alc_sign_ceasefire"] = guard("OR = { AND = { tag = LEA original_tag = LEA } AND = { tag = AUR original_tag = AUR } } ac_alc_war_running = yes ac_alc_pair_at_war = yes NOT = { has_global_flag = ac_alc_ceasefire_signed }",
        "clr_country_flag = ac_alc_ceasefire_pending\nclr_country_flag = ac_alc_ceasefire_window\n" +
        guard("tag = LEA", "white_peace = AUR") + block("else", "white_peace = LEA") +
        guard("NOT = { ac_alc_pair_at_war = yes }", "set_global_flag = ac_alc_ceasefire_signed\nac_alc_record_end = yes") +
        block("else", "set_global_flag = ac_alc_ceasefire_not_made\nac_alc_taint = yes"))
    effects["ac_alc_fight_on"] = guard("tag = LEA original_tag = LEA ac_alc_war_running = yes",
        "set_global_flag = ac_alc_ceasefire_refused\nclr_country_flag = ac_alc_ceasefire_pending\nclr_country_flag = ac_alc_ceasefire_window\n"
        "add_timed_idea = { idea = ac_alc_lea_fought_on days = 180 }\nnews_event = { id = ac_alc.13 days = 1 }")
    effects["ac_alc_ceasefire_tick"] = guard(
        "ac_alc_course_open = yes has_global_flag = ac_alc_stage_removal NOT = { has_global_flag = ac_alc_ceasefire_refused } NOT = { has_global_flag = ac_alc_ceasefire_not_made }",
        guard("NOT = { has_country_flag = ac_alc_ceasefire_asked }",
              "set_country_flag = ac_alc_ceasefire_asked\nset_country_flag = ac_alc_ceasefire_pending\n"
              "set_country_flag = { flag = ac_alc_ceasefire_window days = 14 }\ncountry_event = { id = ac_alc.6 days = 1 }") +
        block("else_if", block("limit", "has_country_flag = ac_alc_ceasefire_pending NOT = { has_country_flag = ac_alc_ceasefire_window }") +
              "ac_alc_sign_ceasefire = yes"))
    effects["ac_alc_early_settlement"] = guard("tag = AUR original_tag = AUR ac_alc_war_running = yes ac_alc_pair_at_war = yes has_global_flag = ac_alc_stage_griswall "
                                               "has_country_flag = AUR_sw_liberation_policy_a_done NOT = { has_global_flag = ac_alc_ceasefire_signed } NOT = { has_global_flag = ac_alc_ceasefire_early }",
        "set_global_flag = ac_alc_ceasefire_early\nac_alc_sign_ceasefire = yes\n" +
        guard("NOT = { has_global_flag = ac_alc_ceasefire_signed }", "clr_global_flag = ac_alc_ceasefire_early"))
    effects["ac_alc_owner_weekly"] = guard("tag = LEA original_tag = LEA",
        "ac_alc_calendar_tick = yes\nac_alc_declaration_tick = yes\nac_alc_observation_tick = yes\nac_alc_stage_tick = yes\nac_alc_ceasefire_tick = yes")
    effects["ac_alc_owner_weekly_aur"] = guard("tag = AUR original_tag = AUR ac_alc_war_running = yes NOT = { country_exists = LEA }", "ac_alc_record_end = yes")
    principal = "OR = { AND = { tag = AUR original_tag = AUR } AND = { tag = LEA original_tag = LEA } } ac_alc_war_running = yes"
    fallen = guard("tag = AUR", "set_global_flag = ac_alc_aur_fallen") + block("else", "set_global_flag = ac_alc_lea_fallen")
    external = "set_global_flag = ac_alc_external_fall\nac_alc_taint = yes\n"
    effects["ac_alc_interrupt_principal"] = guard(principal,
        fallen + guard("NOT = { OR = { AND = { tag = AUR has_war_with = LEA } AND = { tag = LEA has_war_with = AUR } } }", external) +
        "ac_alc_record_end = yes")
    effects["ac_alc_interrupt_external"] = guard(principal, fallen + external + "ac_alc_record_end = yes")
    effects["ac_sp_gleipnir_complete_effect"] = guard("NOT = { has_global_flag = ac_alc_gleipnir_lost }",
        "set_global_flag = ac_sp_gleipnir_complete\n" + guard("NOT = { has_idea = ac_sp_gleipnir_fortress }", "add_ideas = ac_sp_gleipnir_fortress"))
    effects["ac_sp_archelon_complete_effect"] = guard("NOT = { has_global_flag = ac_alc_archelon_lost }",
        "set_global_flag = ac_sp_archelon_complete\n" + guard("NOT = { has_idea = ac_sp_archelon_works }", "add_ideas = ac_sp_archelon_works"))

    idea("ac_alc_lea_war_footing", "Leasath at War", "The ACES Chronicle records Leasath's declaration of war on the Federal Republic of Aurelia for October 2020 (2020 / 10.XX), giving no day. Leasath is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_alc_aur_war_footing", "Aurelia at War", "The ACES Chronicle records that Leasath's invasion caught Aurelia off guard (2020 / 10.XX). The federation is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_alc_aur_griswall_occupied", "Griswall Occupied", "Leasathian forces hold Aurelia's capital, as the Chronicle records that almost the whole country fell under Leasath's control (2020 / 10.XX). The federation governs from elsewhere until Aurelian forces actually hold the capital again; the values are provisional gameplay.",
         {"political_power_gain": -0.1, "stability_factor": -0.03})
    idea("ac_alc_lea_gleipnir_over_aurelia", "The Gleipnir Over Aurelia", "The Chronicle records that Leasath invaded using the Gleipnir aerial fortress (2020 / 10.XX). In this campaign the fortress flies only because its project was completed; the modifier is provisional gameplay.",
         {"air_superiority_efficiency": 0.04, "army_attack_factor": 0.03})
    idea("ac_alc_lea_commander_removed", "The Commander Removed", "The Chronicle records that Leasath's commanding officer, Diego Navarro, was removed from office and that the war ended (2020 / 12.XX). The country's will to fight collapses for 120 days; the value is provisional gameplay. Its politics are not changed by script.",
         {"war_support_factor": -0.15, "army_org_factor": -0.05})
    idea("ac_alc_lea_restraint_kept", "A Declaration Withheld", "Leasath's government withheld the declaration the ACES Chronicle records for October 2020 (2020 / 10.XX), on its own restraint and Aurelia's renegotiated terms and readiness. This earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "army_org_factor": -0.02, "political_power_gain": -0.03})
    idea("ac_alc_lea_fought_on", "Fighting On After the Removal", "Leasath refused the end of the war the ACES Chronicle records for December 2020 (2020 / 12.XX) and fights on. This provisional alternative weighs on the country for 180 days.",
         {"war_support_factor": -0.05, "stability_factor": -0.02})
    idea("ac_sp_gleipnir_fortress", "The Gleipnir", "§YProvisional gameplay§! reward. The strategic airship Gleipnir, with optical camouflage, shockwave ballistic missiles and a Shock Cannon, is complete (Super Weapons, Gleipnir). It is never deployed as a unit; the Chronicle records it shot down in November 2020.",
         {"air_superiority_efficiency": 0.04, "political_power_gain": -0.03})
    idea("ac_sp_archelon_works", "Archelon Fortress", "§YProvisional gameplay§! reward. A military fortification and weapons plant, built in secret on Sentry Island in the Danern Straits (Super Weapons, Archelon Fortress). The island is not on this map; the Chronicle records the fortress destroyed in December 2020.",
         {"industrial_capacity_factory": 0.03, "army_core_defence_factor": 0.02})

    texts = {
        1: ("Leasath Invades Aurelia",
            "Leasath has declared war on the Federal Republic of Aurelia, citing years of exploitation as its just cause, and has invaded. The ACES Chronicle records the declaration for October 2020 (2020 / 10.XX) without a day.\n\nThe grievance is recorded as Leasath's stated claim; this campaign does not judge it. The war ends when the fighting actually ends, not on a calendar date.",
            "The south is at war.", "ac_alc_news_declaration"),
        2: ("The Declaration Leasath Withheld",
            "October 2020 has passed without a Leasathian declaration of war. Leasath's own restraint and Aurelia's renegotiated terms and readiness gave its government the standing to withhold the war the ACES Chronicle records (2020 / 10.XX).\n\nThis is an earned alternative to the official record and is provisional gameplay.",
            "Record the restraint.", "ac_alc_news_withheld"),
        3: ("Aurelia and Leasath Already at War",
            "When the month the ACES Chronicle gives for Leasath's declaration came (2020 / 10.XX), the two countries were already fighting one another by other means.\n\nThe owner records that war and observes it from outside; the war's end will be recorded when the fighting actually stops.",
            "Observe the war as it is.", "ac_alc_news_observed"),
        4: ("Other Fighting Enters the Southern War",
            "A third country is now at war with Aurelia or Leasath. The owner moves to external observation and the dated news of the official course stops here.\n\nThe war's end will still be recorded when the fighting between Aurelia and Leasath actually stops.",
            "Observe the wider war.", "ac_alc_news_expanded"),
        7: ("The War in the South Ends",
            "Leasath's commanding officer has been removed from office, and the war between Leasath and Aurelia has ended in a ceasefire. The ACES Chronicle records the end for December 2020 (2020 / 12.XX); the official abstract records the downfall of the conflict's chief orchestrator.\n\nThis campaign records the end on the day the ceasefire was actually signed.",
            "Begin the accounting.", "ac_alc_news_end"),
        8: ("An Early Settlement",
            "Aurelia has offered Leasath terms after retaking its capital, and the fighting has stopped before the end the ACES Chronicle records for December 2020 (2020 / 12.XX).\n\nThis is an earned alternative to the official record and is provisional gameplay.",
            "Begin the accounting.", "ac_alc_news_end"),
        9: ("Leasath Capitulates",
            "Leasath has capitulated. The war ends in an Aurelian victory.\n\nThe ACES Chronicle records a different end: the commander's removal and the end of the war in December 2020 (2020 / 12.XX). This outcome is the actual result of the campaign, not the official one.",
            "Record the outcome.", "ac_alc_news_end"),
        10: ("Aurelia Capitulates",
             "Aurelia has capitulated. The war ends in a Leasathian victory.\n\nThe ACES Chronicle records a different end: Aurelia's counter-offensive and the end of the war in December 2020 (2020 / 12.XX). This outcome is the actual result of the campaign, not the official one.",
             "Record the outcome.", "ac_alc_news_end"),
        11: ("The War in the South Ends",
             "The fighting between Aurelia and Leasath has stopped. Neither country capitulated, and no ceasefire was signed through this owner.\n\nThe ACES Chronicle records the end for December 2020 (2020 / 12.XX); this campaign records the day the fighting actually ceased.",
             "Begin the accounting.", "ac_alc_news_end"),
        12: ("The Fighting Between Aurelia and Leasath Stops",
             "The fighting between Aurelia and Leasath has stopped. The owner observed this war from outside and asserts nothing about how it was fought.",
             "Record the cessation.", "ac_alc_news_end"),
        13: ("Leasath Fights On",
             "Leasath has refused the end of the war the ACES Chronicle records for December 2020 (2020 / 12.XX) and fights on.\n\nThis is a provisional alternative; the war's end will be recorded when the fighting actually stops.",
             "The war goes on.", "ac_alc_news_fought_on"),
        15: ("The Gleipnir Over Aurelia",
             "Leasath's invasion uses the Gleipnir aerial fortress, as the ACES Chronicle records (2020 / 10.XX). The Super Weapons record describes a strategic airship with optical camouflage, shockwave ballistic missiles and a Shock Cannon.\n\nIn this campaign the fortress flies because its project was completed; it remains text, not a unit.",
             "The sky darkens.", "ac_alc_news_gleipnir"),
        20: ("Aurelia Overrun",
             "Leasathian forces hold Griswall, the capital of the Federal Republic of Aurelia. The ACES Chronicle records that almost the whole country fell under Leasath's control (2020 / 10.XX), and the official abstract that only Aubrey Base in the remote southwest stayed unoccupied.\n\nThis campaign reports the occupation only because Leasathian forces actually hold the capital; no state was moved by script.",
             "The capital is lost.", "ac_alc_news_overrun"),
        21: ("Aubrey Base Holds",
             "Aurelia's Gryphus Squadron has repelled an attack by the Leasath air force on Aubrey Base (2020 / 10.XX).\n\nAubrey Base is not on this map; the record is reported as the Chronicle gives it, in its month.",
             "The base holds.", "ac_alc_news_aubrey"),
        22: ("Port Patterson Reclaimed",
             "Aurelian forces have reclaimed Port Patterson (2020 / 11.XX).\n\nThe Chronicle gives the month only; no territory changes hands by script.",
             "The port is ours.", "ac_alc_news_port_patterson"),
        23: ("The Gleipnir Shot Down",
             "Aurelian forces have found the means to disable the Gleipnir's stealth and shot the flying fortress down; the key transport hub of Santa Elva was liberated the same day (2020 / 11.XX).\n\nThis campaign reports the loss because the Gleipnir project was completed; its reward is removed.",
             "The fortress falls.", "ac_alc_news_gleipnir_down"),
        24: ("Sachana Air Base Retaken",
             "Aurelia has launched an assault to reclaim its largest air base, Sachana Air Base in the Raven Woods, and the operation has succeeded (2020 / 12.XX).\n\nThe Chronicle gives the month only; no territory changes hands by script.",
             "The air base is ours.", "ac_alc_news_sachana"),
        25: ("Griswall Retaken",
             "Aurelian forces have retaken Griswall, and Leasathian forces have marched away from the mainland to regroup at Archelon Fortress (2020 / XX.XX).\n\nThe Chronicle gives no month. This campaign reports the recapture because Aurelian forces actually hold the capital again.",
             "The capital is free.", "ac_alc_news_griswall"),
        26: ("The Commander Removed",
             "Leasath's commanding officer and the chief orchestrator of the conflict, Diego Navarro, has been removed from office (2020 / 12.XX). The ACES Chronicle records that the war ended.\n\nLeasath's politics are not changed by script; its government must now answer.",
             "The war is ending.", "ac_alc_news_removal"),
        27: ("Archelon Fortress Destroyed",
             "Archelon Fortress has been destroyed (2020 / 12.XX).\n\nThis campaign reports the destruction because the Archelon project was completed; its reward is removed. Sentry Island is not on this map.",
             "The fortress is gone.", "ac_alc_news_archelon"),
    }
    for number, (title, prose, label, picture) in texts.items():
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, label
        news(number, picture)
    loc.update({
        "ac_alc.5.t": "October 2020",
        "ac_alc.5.d": "The ACES Chronicle records that in October 2020 Leasath declared war on the Federal Republic of Aurelia, citing years of exploitation as its just cause, and invaded (2020 / 10.XX).\n\nThe government can declare the war the record describes, or withhold it, if the standing to withhold was earned: Leasath's own restraint as policy, and Aurelia's renegotiated terms and completed readiness review. Withholding is a provisional alternative.",
        "ac_alc.5.a": "Declare war on Aurelia.",
        "ac_alc.5.b": "Withhold the declaration.",
        "ac_alc.6.t": "The End of the War",
        "ac_alc.6.d": "The commander has been removed. The ACES Chronicle records that the war ended in December 2020 (2020 / 12.XX).\n\nThe government can sign a ceasefire, or fight on. Fighting on is a provisional alternative; the war's end is then recorded when the fighting actually stops.",
        "ac_alc.6.a": "Sign the ceasefire.",
        "ac_alc.6.b": "Fight on.",
    })
    events.append(block("country_event", "id = ac_alc.5\ntitle = ac_alc.5.t\ndesc = ac_alc.5.d\npicture = GFX_ac_alc_event_lea_declaration\nis_triggered_only = yes\n"
                        "trigger = { tag = LEA original_tag = LEA ac_alc_can_declare = yes }\n" +
                        block("option", "name = ac_alc.5.a\nai_chance = { factor = 100 }\nac_alc_declare = yes") +
                        block("option", "name = ac_alc.5.b\ntrigger = { ac_alc_restraint_earned = yes }\nai_chance = { factor = 0 }\nac_alc_withhold = yes")))
    events.append(block("country_event", "id = ac_alc.6\ntitle = ac_alc.6.t\ndesc = ac_alc.6.d\npicture = GFX_ac_alc_event_lea_ceasefire\nis_triggered_only = yes\n"
                        "trigger = { tag = LEA original_tag = LEA ac_alc_course_open = yes ac_alc_pair_at_war = yes NOT = { has_global_flag = ac_alc_ceasefire_signed } }\n" +
                        block("option", "name = ac_alc.6.a\nai_chance = { factor = 100 }\nac_alc_sign_ceasefire = yes") +
                        block("option", "name = ac_alc.6.b\nai_chance = { factor = 0 }\nac_alc_fight_on = yes")))

    decisions = {}
    ident = "AUR_sw_early_settlement"
    loc[ident] = "Offer Terms After Griswall"
    loc[ident + "_desc"] = "Offer Leasath terms once Griswall is retaken (2020 / XX.XX), before the end the Chronicle records for December 2020 (2020 / 12.XX). Requires the return with terms as policy. If the engine accepts the peace, the war ends now; this earned alternative is provisional gameplay."
    decisions["ac_alc_aur_services"] = [block(ident, f"icon = ac_alc_{ident}\nallowed = {{ tag = AUR original_tag = AUR }}\nvisible = {{ ac_alc_war_running = yes }}\n"
                                              "available = { ac_alc_war_running = yes ac_alc_pair_at_war = yes has_global_flag = ac_alc_stage_griswall has_country_flag = AUR_sw_liberation_policy_a_done NOT = { has_global_flag = ac_alc_ceasefire_signed } }\n"
                                              "cost = 50\nfire_only_once = yes\n" + block("complete_effect", "ac_alc_early_settlement = yes") + "ai_will_do = { base = 0 }\n")]
    fallbacks = []
    for project, available, cancel in (
            ("gleipnir", "date > 2014.12.31 has_country_flag = LEA_le_army_operations_done NOT = { has_global_flag = ac_sp_gleipnir_complete } NOT = { has_global_flag = ac_alc_gleipnir_lost }",
             "has_global_flag = ac_alc_gleipnir_lost"),
            ("archelon", "date > 2014.12.31 has_country_flag = LEA_le_front_operations_done NOT = { has_global_flag = ac_sp_archelon_complete } NOT = { has_global_flag = ac_alc_archelon_lost }",
             "has_global_flag = ac_alc_archelon_lost")):
        body = (f"icon = GFX_decision_ac_sp_{project}\n" + block("allowed", 'NOT = { has_dlc = "Gotterdammerung" }\noriginal_tag = LEA') +
                block("visible", f"always = yes\nNOT = {{ has_global_flag = ac_sp_{project}_complete }}") + block("available", available) +
                block("cancel_trigger", block("OR", cancel)) +
                "fire_only_once = yes\ncost = 75\ndays_remove = 300\n" + block("ai_will_do", "base = 5") +
                block("complete_effect", "custom_effect_tooltip = ac_superweapons_programme_started_tt") +
                block("remove_effect", guard(f"NOT = {{ has_global_flag = ac_sp_{project}_complete }}", f"ac_sp_{project}_complete_effect = yes")))
        fallbacks.append(block(f"ac_superweapons_{project}", body))
    decisions["ac_superweapons"] = fallbacks

    def project(ident, specialization, blueprint, tag, available, reward, options, generic):
        unique = block(reward["name"], f"icon = GFX_{reward['name']}\nfire_only_once = yes\n" + block("threshold", "min = 0\nmax = 80") +
                       block("weight", reward["weight"]) + "".join(block("option", o) for o in options))
        return block(ident, f"specialization = {specialization}\nicon = GFX_{ident}\nblueprint_image = {blueprint}\n" +
                     block("project_tags", tag) + block("allowed", "original_tag = LEA") + block("visible", "always = yes") +
                     block("available", available) + "complexity = sp_complexity.large\nprototype_time = sp_time.prototype.long\n" +
                     block("ai_will_do", "base = 10") + block("project_output", block("country_effects", f"{ident}_complete_effect = yes")) +
                     block("generic_prototype_rewards", "\n".join(generic)) + block("unique_prototype_rewards", unique))

    def options(stem, cautious, bold):
        return (f"token = {stem}_{cautious}\ndefault = yes\n" +
                block("iteration_output", block("country_effects", "FROM = { add_project_progress_ratio = constant:sp_progress.gain.low }\nadd_stability = 0.02")),
                f"token = {stem}_{bold}\n" +
                block("iteration_output", block("country_effects", "add_political_power = -50\nFROM = { add_project_progress_ratio = constant:sp_progress.gain.medium }")))
    projects = (
        "# Source: Super Weapons, Gleipnir; Chronicle 2020 / 10.XX and 11.XX. Gate and timing are provisional gameplay.\n" +
        project("ac_sp_gleipnir", "specialization_air", "GFX_ac_sp_blueprint_air_defence", "ac_sp_tag_aerial_fortress",
                "date > 2014.12.31\nFROM = { has_country_flag = LEA_le_army_operations_done }\nNOT = { has_global_flag = ac_sp_gleipnir_complete }\nNOT = { has_global_flag = ac_alc_gleipnir_lost }",
                dict(name="ac_sp_gleipnir_reward_camouflage_trials", weight="base = 20"),
                options("ac_sp_gleipnir_reward_camouflage_trials", "ground", "flight"),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_air_defence")) +
        "\n# Source: Super Weapons, Archelon Fortress; Chronicle 2020 / 12.XX. Sentry Island is unmapped. Gate and timing are provisional gameplay.\n" +
        project("ac_sp_archelon", "specialization_land", "GFX_ac_sp_blueprint_land", "ac_sp_tag_aerial_fortress",
                "date > 2014.12.31\nFROM = { has_country_flag = LEA_le_front_operations_done }\nNOT = { has_global_flag = ac_sp_archelon_complete }\nNOT = { has_global_flag = ac_alc_archelon_lost }",
                dict(name="ac_sp_archelon_reward_secrecy", weight="base = 20"),
                options("ac_sp_archelon_reward_secrecy", "audited", "secret"),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_air_defence")))
    loc.update({
        "ac_sp_gleipnir": "The Gleipnir",
        "ac_sp_gleipnir_desc": "A strategic airship with optical camouflage, shockwave ballistic missiles and a Shock Cannon (Super Weapons, Gleipnir). Requires the army's place defined and an officer class trained.\n\n§YProvisional gameplay§!: the gate, timing and reward values are balance choices. The Chronicle records the fortress shot down in November 2020.",
        "ac_sp_gleipnir_reward_camouflage_trials": "Camouflage Trials",
        "ac_sp_gleipnir_reward_camouflage_trials_desc": "The optical camouflage can be tested on the ground first, or in flight at once.",
        "ac_sp_gleipnir_reward_camouflage_trials_ground": "Test on the ground first",
        "ac_sp_gleipnir_reward_camouflage_trials_flight": "Test in flight",
        "ac_sp_archelon": "Archelon Fortress",
        "ac_sp_archelon_desc": "A military fortification and weapons manufacturing plant, built in secret on Sentry Island in the Danern Straits (Super Weapons, Archelon Fortress). Requires the civil war's front held and its roads protected.\n\n§YProvisional gameplay§!: the gate, timing and reward values are balance choices. The island is not on this map; the Chronicle records the fortress destroyed in December 2020.",
        "ac_sp_archelon_reward_secrecy": "Secrecy",
        "ac_sp_archelon_reward_secrecy_desc": "The fortress's construction can be audited by the assembly, or kept secret even from it.",
        "ac_sp_archelon_reward_secrecy_audited": "Let the assembly audit it",
        "ac_sp_archelon_reward_secrecy_secret": "Keep it secret",
        "ac_sp_tag_aerial_fortress": "Aerial Fortress Projects",
        "ac_sp_tag_aerial_fortress_speed_factor": "Aerial Fortress Projects Speed",
        "ac_sp_tag_aerial_fortress_speed_factor_tt": " $ac_sp_tag_aerial_fortress_speed_factor$: $RIGHT|+=%1$",
        "ac_superweapons_gleipnir": "The Gleipnir",
        "ac_superweapons_gleipnir_desc": "Without the special-projects feature, the Gleipnir programme runs as a timed decision and grants the same reward as the project (Super Weapons, Gleipnir). It is cancelled if the Chronicle's loss of the fortress is reached first.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
        "ac_superweapons_archelon": "Archelon Fortress",
        "ac_superweapons_archelon_desc": "Without the special-projects feature, the Archelon programme runs as a timed decision and grants the same reward as the project (Super Weapons, Archelon Fortress). It is cancelled if the Chronicle's destruction of the fortress is reached first.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
    })

    status = (("has_global_flag = ac_alc_outcome_aurelian_victory", "Ended: Leasath capitulated. The end the Chronicle records for December 2020 did not occur."),
              ("has_global_flag = ac_alc_outcome_leasathian_victory", "Ended: Aurelia capitulated. The end the Chronicle records for December 2020 did not occur."),
              ("has_global_flag = ac_alc_historical_course", "Ended: the ceasefire was signed after the commander's removal, as the official course records (2020 / 12.XX)."),
              ("has_global_flag = ac_alc_ceasefire_early", "Ended: an early settlement was earned and signed after Griswall (provisional gameplay)."),
              ("has_global_flag = ac_alc_outcome_ceasefire", "Ended: a ceasefire was signed before the official course had run its length."),
              (f"{ENDED} OR = {{ {TAINTED} {EXISTING} }}", "Ended: the fighting stopped while the owner observed the war from outside."),
              (ENDED, "Ended: the fighting stopped without a ceasefire signed through this owner."),
              ("has_global_flag = ac_alc_ceasefire_refused ac_alc_war_running = yes", "Running after the removal: Leasath refused to end the war; the end is recorded when the fighting stops."),
              ("has_global_flag = ac_alc_ceasefire_not_made", "Under external observation: the ceasefire was signed but the engine kept the war."),
              (TAINTED, "Under external observation: other fighting entered the war; the official course is no longer asserted."),
              (EXISTING, "Under external observation: the pair was already at war in the Chronicle's declaration month."),
              (STARTED, "Running on the official course since Leasath's declaration of October 2020 (2020 / 10.XX)."),
              ("has_global_flag = ac_alc_declaration_withheld", "Withheld: Leasath withheld the declaration on its earned standing (provisional gameplay)."),
              ("has_global_flag = ac_alc_route_unreachable", "Closed: Leasath's civil war was not over in 2020; the sourced route is unreachable."),
              (CLOSED, "Closed: the pair could not fight the recorded war, or the record's month had passed."),
              (None, "Pending: the Chronicle records Leasath's declaration of war on Aurelia for October 2020."))
    entries = ""
    for n, (condition, value) in enumerate(status):
        loc[f"ac_alc_status_{n}"] = value
        entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + f"localization_key = ac_alc_status_{n}")
    custom = block("defined_text", "name = ac_alc_status_text\n" + entries)
    loc.update({
        "ac_alc_started": "The Aurelia-Leasath war has begun",
        "ac_alc_tainted": "The Aurelia-Leasath war is under external observation",
        "ac_alc_declaration_withheld": "Leasath withheld the 2020 declaration",
        "ac_alc_ended": "The Aurelia-Leasath war has ended",
        "ac_alc_closed": "The Aurelia-Leasath war owner is closed",
        "ac_alc_calendar_started": "The Aurelia-Leasath war calendar is open",
        "ac_alc_historical_course": "The Aurelia-Leasath war followed its official course",
        "ac_alc_outcome_cessation": "The fighting between Aurelia and Leasath stopped without a ceasefire signed here",
        "ac_alc_outcome_ceasefire": "Aurelia and Leasath signed a ceasefire",
        "ac_alc_outcome_aurelian_victory": "Leasath capitulated",
        "ac_alc_outcome_leasathian_victory": "Aurelia capitulated",
        "ac_alc_pre_existing_war": "A principal was already at war when the declaration came",
        "ac_alc_existing_war_observed": "Aurelia and Leasath were already at war in the Chronicle's declaration month",
        "ac_alc_late_start_skipped": "The Chronicle's declaration month had passed before this content first loaded",
        "ac_alc_principal_missing": "Aurelia or Leasath did not exist when the calendar opened",
        "ac_alc_principal_unable": "Aurelia or Leasath could not fight the recorded war",
        "ac_alc_route_unreachable": "Leasath's civil war was not over, so the sourced 2020 route is unreachable",
        "ac_alc_declaration_refused": "The engine did not create the declared war; the owner is closed",
        "ac_alc_declaration_asked": "The Leasathian government has been asked about the declaration",
        "ac_alc_declaration_pending": "The Leasathian declaration is pending",
        "ac_alc_declaration_window": "The declaration window is open",
        "ac_alc_ceasefire_asked": "The Leasathian government has been asked about the end of the war",
        "ac_alc_ceasefire_pending": "The ceasefire answer is pending",
        "ac_alc_ceasefire_window": "The ceasefire window is open",
        "ac_alc_ceasefire_signed": "The ceasefire was signed",
        "ac_alc_ceasefire_early": "An early settlement was earned and signed",
        "ac_alc_ceasefire_refused": "Leasath refused to end the war and fought on",
        "ac_alc_ceasefire_not_made": "The ceasefire was signed but the engine kept the war",
        "ac_alc_aur_fallen": "Aurelia has fallen during the war",
        "ac_alc_lea_fallen": "Leasath has fallen during the war",
        "ac_alc_external_fall": "A principal fell to a third party, or outside the pair's own war",
        "ac_alc_gleipnir_lost": "The Gleipnir was shot down",
        "ac_alc_archelon_lost": "Archelon Fortress was destroyed",
        "ac_alc_principals": "Aurelia and Leasath both exist",
        "ac_alc_war_running": "The Aurelia-Leasath war is running",
        "ac_alc_course_open": "The Aurelia-Leasath war follows its official course",
        "ac_alc_pair_at_war": "Aurelia and Leasath are at war",
        "ac_alc_can_declare": "Leasath can declare the recorded war",
        "ac_alc_restraint_earned": "Leasath's restraint and Aurelia's renegotiated terms and readiness give Leasath the standing to withhold",
        "ac_alc_third_party_present": "A third country is at war with Aurelia or Leasath",
        "ac_alc_principal_fallen": "A principal has capitulated or fallen",
    })
    for name, window, _, _, number in STAGES:
        loc[f"ac_alc_stage_{name}"] = "Aurelia-Leasath war stage: " + loc[f"{P}.{number}.t"]
        if window:
            loc[f"ac_alc_stage_{name}_skipped"] = "Aurelia-Leasath war stage passed unreported: " + loc[f"{P}.{number}.t"]

    hooks = {
        "on_startup": "if = { limit = { country_exists = LEA } LEA = { ac_alc_restore = yes } }",
        "on_weekly_AUR": "ac_alc_owner_weekly_aur = yes",
        "on_annex": ("if = { limit = { OR = { tag = AUR tag = LEA } } FROM = { ac_alc_interrupt_principal = yes } }\n"
                     "else = { FROM = { ac_alc_interrupt_external = yes } }"),
        "on_capitulation_immediate": ("if = { limit = { FROM = { OR = { tag = AUR tag = LEA } } } ac_alc_interrupt_principal = yes }\n"
                                      "else = { ac_alc_interrupt_external = yes }"),
        "on_subject_annexed": ("if = { limit = { FROM = { OR = { tag = AUR tag = LEA } } } ac_alc_interrupt_principal = yes }\n"
                               "else = { ac_alc_interrupt_external = yes }"),
    }
    ai = "\n".join((
        block("ac_alc_lea_tension", "allowed = { original_tag = LEA }\n" +
              block("enable", f"has_global_flag = ac_alc_calendar_started {ROUTE_SETTLED}") +
              "abort_when_not_enabled = yes\nai_strategy = { type = antagonize id = AUR value = 60 }"),
        block("ac_alc_lea_war", "allowed = { original_tag = LEA }\n" + block("enable", "ac_alc_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = AUR value = 150 }"),
        block("ac_alc_aur_war", "allowed = { original_tag = AUR }\n" + block("enable", "ac_alc_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = LEA value = 120 }"),
    ))
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                categories=[], decisions=decisions, hooks=hooks, ai_strategy=ai,
                category_prefix={"AUR": "[ac_alc_status_text]\n\n", "LEA": "[ac_alc_status_text]\n\n"},
                projects=projects, project_tags=["ac_sp_tag_aerial_fortress"])


# Registry declarations ------------------------------------------------------
KEY = "F2b"
NAME = "southern_theater"
IMPORTS = {"AUR": "SOUTHERN THEATER", "LEA": "SOUTHERN THEATER"}
LEDGER = "docs/CONTENT_WAVE_F2.md"
SOURCES = {"official": ["Chronicle 2020 / 10.XX to 12.XX and XX.XX: the Aurelia-Leasath war (months only)",
                        "Abstracts and Product, ACE COMBAT X", "Super Weapons: Gleipnir; Archelon Fortress"],
           "mod_provenance": "Leasath civil-war record, Aurelia foundation records and the capitals' states, read only",
           "provisional_gameplay": "Every focus, policy, service, dialogue and value; the month windows; the scripted ceasefire; the two projects; the earned alternatives"}
NEWS_ART = (("ac_alc_news_declaration", ("command", "missile"), "Leasath Invades Aurelia", "LEA"),
            ("ac_alc_news_withheld", ("document", "peace"), "The Declaration Leasath Withheld", "LEA"),
            ("ac_alc_news_observed", ("telescope", "command"), "Aurelia and Leasath Already at War", "AUR"),
            ("ac_alc_news_expanded", ("telescope", "assembly"), "Other Fighting Enters the Southern War", "AUR"),
            ("ac_alc_news_end", ("peace", "assembly"), "The War in the South Ends", "AUR"),
            ("ac_alc_news_fought_on", ("command", "security"), "Leasath Fights On", "LEA"),
            ("ac_alc_news_gleipnir", ("air", "missile"), "The Gleipnir Over Aurelia", "LEA"),
            ("ac_alc_news_overrun", ("gate", "security"), "Aurelia Overrun", "AUR"),
            ("ac_alc_news_aubrey", ("runway", "air"), "Aubrey Base Holds", "AUR"),
            ("ac_alc_news_port_patterson", ("navy", "gate"), "Port Patterson Reclaimed", "AUR"),
            ("ac_alc_news_gleipnir_down", ("air", "radar"), "The Gleipnir Shot Down", "AUR"),
            ("ac_alc_news_sachana", ("runway", "command"), "Sachana Air Base Retaken", "AUR"),
            ("ac_alc_news_griswall", ("peace", "civil"), "Griswall Retaken", "AUR"),
            ("ac_alc_news_removal", ("assembly", "security"), "The Commander Removed", "LEA"),
            ("ac_alc_news_archelon", ("industry", "missile"), "Archelon Fortress Destroyed", "LEA"))
EVENT_ART = (("ac_alc_event_lea_declaration", ("command", "missile"), "October 2020", "LEA"),
             ("ac_alc_event_lea_ceasefire", ("peace", "assembly"), "The End of the War", "LEA"))
OWNER_ART = {
    "ac_alc_lea_war_footing": ("command", "missile", "LEA"), "ac_alc_aur_war_footing": ("command", "runway", "AUR"),
    "ac_alc_aur_griswall_occupied": ("gate", "security", "AUR"), "ac_alc_lea_gleipnir_over_aurelia": ("air", "missile", "LEA"),
    "ac_alc_lea_commander_removed": ("assembly", "security", "LEA"), "ac_alc_lea_restraint_kept": ("document", "peace", "LEA"),
    "ac_alc_lea_fought_on": ("command", "security", "LEA"),
    "ac_sp_gleipnir_fortress": ("air", "missile", "LEA"), "ac_sp_archelon_works": ("industry", "security", "LEA"),
}
PROJECT_ART = {
    "ac_sp_gleipnir": ("air", "missile", "LEA", {"camouflage_trials": "radar"}),
    "ac_sp_archelon": ("industry", "security", "LEA", {"secrecy": "document"}),
}
