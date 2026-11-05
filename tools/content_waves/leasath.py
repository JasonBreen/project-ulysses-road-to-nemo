"""Wave F2a: Leasath's foundation and civil war, 1991-2019 (Package 5). Leasath 42.

Source layers
-------------
Official (ACES Chronicle, read 4 November 2026; compiled in
docs/STRANGEREAL_2006_2020_SOURCES.md): 2019 / XX.XX, the Leasath Civil War
ends after ten years of fighting. Its start about 2009 is **derived** from
"ten years", and the record gives no day, month or winner for the end. The
Super Weapons record calls the country the Democratic Republic of Leasath;
the mod's democratic name is "Federal Republic of Leasath" and its communist
name "Democratic Republic of Leasath". The names are recorded, not changed.

Mod provenance, read only: Leasath's country history and the institution and
world-start profiles; Aurelia's foundation records (``AUR_au_*``).

Provisional gameplay: every focus, policy, service, dialogue and value; the
civil-war owner's authority measure, its prolonged and negotiated
alternatives and its idea values. No tag, border, civil-war split or
officeholder is created or changed.
"""
from content_waves.framework import Branch, Wave, block, guard

P = "ac_lcw"
TREE_ID = "lea_national_campaign"
STARTED = "has_global_flag = ac_lcw_started"
RUNNING = "has_global_flag = ac_lcw_started NOT = { has_global_flag = ac_lcw_ended } NOT = { has_global_flag = ac_lcw_closed }"


def authority(points):
    return f"add_to_variable = {{ ac_lcw_authority = {points} }}\nclamp_variable = {{ var = ac_lcw_authority min = 0 max = 100 }}"


BRANCHES = (
    # The foundation, 1991-2018 ------------------------------------------------------
    Branch("LEA", "mines", (), "",
        ("Review the Mining Concessions", "Renegotiate the Concessions", "Take the Mines Into State Hands",
         "Publish the Royalty Accounts", "Review a Concession Service Period", "Mines on the Record"),
        ("Leasath's wealth is in the ground, and much of it is worked under concessions signed with foreign firms on terms few Leasathians have read. The ministry of mines will list every concession, who holds it and what it pays the country.",
         "The concessions will be renegotiated one by one, with royalties raised and local hiring written into each. Renegotiation keeps the firms and their investment; it takes years, and the firms will remember who pressed them.",
         "The largest mines will be taken into state hands, with compensation paid over a decade. The state keeps the revenue and the jobs; the firms and their governments call it confiscation.",
         "The royalty accounts will be published every year: what each mine produced, what it paid and where the money went. Publication answers the question every Leasathian asks about the mines, and it shows how little some of them paid.",
         "A completed, funded service period under the chosen policy must be reviewed before the concessions become settled law. The review compares royalties collected with the figures published.",
         "The settlement fixes the terms on which Leasath's minerals are worked. It does not decide whether anyone exploited anyone. It leaves a country that can read its own accounts."),
        (("industry", "document"), ("scales", "industry"), ("industry", "command"), ("economy", "document"), ("scales", "economy"), ("industry", "peace")),
        (("Renegotiated concessions", {"production_factory_efficiency_gain_factor": 0.02}, {"political_power_gain": -0.03}),
         ("Mines in state hands", {"industrial_capacity_factory": 0.03}, {"stability_factor": -0.015})),
        (("Audit the Royalties", "Audit one year's royalties against the mines' production.", "The ministry of mines", {"political_power_gain": 0.08}),
         ("Train Mine Inspectors", "Train inspectors to check safety and output at the concessions.", "The mining inspectorate", {"production_factory_efficiency_gain_factor": 0.025})),
        ("A Contract Signed Abroad",
         "The audit has found a concession signed in a foreign capital, in a foreign language, by an official who no longer works for the ministry. The firm says the contract is valid; the ministry's lawyers are not sure it was ever ratified.\n\nThe ministry can publish the contract and the doubt about it, or negotiate quietly with the firm and keep the question out of the newspapers.",
         ("Publish the contract and the doubt.", "Negotiate quietly with the firm.")),
        ("Mines on the Record",
         "The final review lists every concession with its terms, royalties and inspection results. The contract signed abroad is there, with what became of it.\n\nThe accounts do not settle the argument about the mines. They give both sides the same numbers.")),
    Branch("LEA", "provinces", (), "",
        ("Map the Provinces' Authority", "A Federal Settlement", "A Strong Centre",
         "Fund the Provincial Councils", "Review a Provincial Service Period", "A Country of Provinces"),
        ("Leasath's provinces were drawn by treaties and governors, not by the people who live in them. The interior ministry will record what each province decides for itself, what the capital decides for it and where nobody decides at all.",
         "The provinces will keep their councils and their budgets under a federal settlement, with the capital responsible for defence and foreign affairs. Federalism gives every region a stake; it gives every regional leader a platform.",
         "The capital will appoint the provincial governors and set their budgets. A strong centre acts quickly and speaks with one voice; the regions it overrides learn to look for another.",
         "Provincial councils will be funded to deliver schools, roads and clinics, with their accounts reported to the capital. Councils that deliver earn trust; councils that cannot become grievances.",
         "A completed, funded service period under the chosen settlement must be reviewed before it becomes the country's constitution. The review asks which provinces delivered and which complained.",
         "The settlement records how Leasath shares power among its provinces. It does not predict which of them will one day take up arms. It leaves a map of who decides what."),
        (("assembly", "document"), ("assembly", "diplomacy"), ("command", "assembly"), ("civil", "economy"), ("scales", "assembly"), ("assembly", "peace")),
        (("Federal settlement", {"stability_factor": 0.025}, {"political_power_gain": -0.03}),
         ("Strong centre", {"political_power_gain": 0.05}, {"stability_factor": -0.02})),
        (("Fund the Councils", "Fund the provincial councils' services for one period.", "The interior ministry", {"stability_factor": 0.025}),
         ("Convene the Governors", "Convene the provincial governors on the period's disputes.", "The cabinet office", {"political_power_gain": 0.08})),
        ("A Province That Will Not Pay",
         "The southern mining province has refused to pass its royalty share to the capital until the capital funds its roads. The governor says the province has paid for decades and received nothing back.\n\nThe cabinet can publish the province's accounts and the capital's spending side by side, or negotiate privately with the governor.",
         ("Publish both accounts.", "Negotiate privately.")),
        ("A Country of Provinces",
         "The final review lists the provinces with their councils, budgets and disputes. The southern province's refusal is there, with the settlement it reached.\n\nThe map has not changed. Who decides on it has.")),
    Branch("LEA", "army", (), "date > 1999.12.31",
        ("Define the Army's Place", "An Army Under the Assembly", "An Army Above the Factions",
         "Train an Officer Corps", "Review an Army Service Period", "An Army That Answers"),
        ("Leasath's army has guarded mines, borders and governments in turn. The defence ministry will decide what the army is for, and to whom it answers when the government and the assembly disagree.",
         "The army will answer to the assembly, with its budget voted each year and its commanders confirmed in public. Civilian control is slow and political; it makes a coup harder to justify.",
         "The army will stand above the factions as the guardian of the state, answering to its own command. A guardian army is united and confident; it decides for itself what the state needs guarding from.",
         "Officers will be trained at a national academy, with promotion by examination rather than patronage. A professional corps fights better; it also knows its own strength.",
         "A completed, funded service period under the chosen arrangement must be reviewed before it becomes doctrine. The review asks whom the army obeyed when it mattered.",
         "The settlement records the army's place in the state. It names no commander. The official record says a commander later led Leasath into war; this record asks who he would answer to."),
        (("command", "assembly"), ("assembly", "command"), ("command", "security"), ("training", "command"), ("scales", "command"), ("command", "peace")),
        (("Army under the assembly", {"stability_factor": 0.02}, {"army_org_factor": -0.01}),
         ("Army above the factions", {"army_org_factor": 0.03}, {"stability_factor": -0.02})),
        (("Train an Officer Class", "Train one class of officers at the national academy.", "The defence ministry", {"army_org_factor": 0.03}),
         ("Hold a Budget Hearing", "Hold the assembly's annual hearing on the army's budget.", "The assembly's defence committee", {"political_power_gain": 0.08})),
        ("A Colonel's Speech",
         "A colonel has told graduating cadets that the army owes loyalty to the nation, not to whoever happens to govern it. The speech was cheered. The assembly wants him disciplined.\n\nThe ministry can publish the speech with its own answer, or transfer the colonel quietly to a remote post.",
         ("Publish the speech and an answer.", "Transfer him quietly.")),
        ("An Army That Answers",
         "The final review records the army's chain of command and the hearings it attended. The colonel's speech is in the file, with the ministry's answer.\n\nWhether the army will answer in a crisis is a question no review can settle. This one records who asked.")),
    Branch("LEA", "labour", (), "date > 2004.12.31",
        ("Hear the Mine Workers", "A Labour Charter", "Order in the Mines",
         "Fund the Workers' Clinics", "Review a Labour Service Period", "A Charter on the Record"),
        ("Strikes in the mines have grown longer and angrier since the asteroid years. The labour ministry will hear the workers' grievances and decide what the state will guarantee them.",
         "A labour charter will set wages, hours and safety in every mine, enforced by inspectors and courts. The charter costs the mines money and the state effort; it gives the workers a law to appeal to instead of a picket line.",
         "Order will be kept in the mines by the police and, if necessary, the army, with strikes banned in essential sites. Order keeps the minerals moving; it makes the grievances quieter and deeper.",
         "Clinics will be opened in the mining towns, funded by the royalties. A clinic is the first thing the state can show a mining town that it gets back from its mines.",
         "A completed, funded service period under the chosen policy must be reviewed before it becomes settled law. The review counts strikes, injuries and clinic visits.",
         "The settlement records what the state guarantees the people who work its mines. It does not end the grievance. It writes down what was promised."),
        (("industry", "assembly"), ("scales", "assembly"), ("security", "industry"), ("medical", "civil"), ("scales", "industry"), ("assembly", "peace")),
        (("Labour charter", {"stability_factor": 0.025}, {"production_factory_efficiency_gain_factor": -0.015}),
         ("Order in the mines", {"production_factory_efficiency_gain_factor": 0.02}, {"stability_factor": -0.02})),
        (("Run the Clinics", "Staff and supply the mining towns' clinics for one period.", "The health ministry", {"stability_factor": 0.025}),
         ("Inspect the Mines", "Inspect wages, hours and safety at the mines for one period.", "The labour inspectorate", {"political_power_gain": 0.08})),
        ("A Strike at the Largest Mine",
         "The largest mine's workers have struck over a collapsed tunnel that killed six men. The company says the tunnel was inspected; the union says the inspector never went underground.\n\nThe ministry can publish the inspection report and open an inquiry, or end the strike first and examine the report afterwards.",
         ("Publish the report and open an inquiry.", "End the strike first.")),
        ("A Charter on the Record",
         "The final review lists the mines with their wages, injuries and strikes, and the clinics with their patients. The collapsed tunnel is there, with the inquiry's finding.\n\nThe miners have a record of what they were promised. So does the state.")),
    # The civil war, 2009-2019 -------------------------------------------------------------
    Branch("LEA", "government", (), STARTED,
        ("Keep the State Running", "A Government of National Unity", "Emergency Rule",
         "Pay the Civil Service", "Review a Wartime Government Period", "A State That Survived"),
        ("Leasath is at war with itself. The ACES Chronicle records only that the civil war ended in 2019 after ten years of fighting; who fought it, and why, is this campaign's own provisional account. The government must decide how to keep the state running while its provinces fight.",
         "The government will invite every faction that will stop fighting into a national unity cabinet. Unity brings in the moderates; it leaves the government arguing with itself.",
         "The government will rule by emergency decree until the fighting stops, with the assembly suspended. Emergency rule acts quickly; every faction it excludes calls it a dictatorship.",
         "Teachers, nurses and clerks will be paid wherever the government can reach them, including in contested provinces. A salary paid is the state's claim to exist.",
         "A completed, funded service period under the chosen government must be reviewed before it becomes the country's wartime constitution. The review asks how far the state's authority reached.",
         "The settlement records the government that carried Leasath through its civil war. It names no victor; the record names none. It leaves a state that still paid its clerks."),
        (("assembly", "security"), ("assembly", "peace"), ("command", "document"), ("economy", "civil"), ("scales", "assembly"), ("assembly", "document")),
        (("Government of national unity", {"stability_factor": 0.02}, {"political_power_gain": -0.05}),
         ("Emergency rule", {"political_power_gain": 0.05}, {"stability_factor": -0.03})),
        (("Pay the Contested Provinces", "Pay civil servants in contested provinces for one period.", "The treasury", {"stability_factor": 0.025}),
         ("Run the Emergency Cabinet", "Staff and fund the wartime cabinet office for one period.", "The cabinet office", {"political_power_gain": 0.08})),
        ("A Faction Asks for a Ministry",
         "A faction that has fought the government for three years offers to stop if its leader is made minister of mines. Half the cabinet says this rewards rebellion; the other half says it ends a front.\n\nThe government can announce the offer and put it to the assembly, or negotiate in secret and present the result.",
         ("Put the offer to the assembly.", "Negotiate in secret.")),
        ("A State That Survived",
         "The final review lists the provinces where the state paid its servants, year by year, through the war. The map shrinks and grows again.\n\nThe faction that asked for a ministry is in the record, with the answer it received.")),
    Branch("LEA", "front", (), STARTED,
        ("Hold the Front", "Hold the Cities", "Take the Mines",
         "Protect the Roads", "Review a Front Service Period", "The Front Held"),
        ("The civil war is fought over cities, mines and the roads between them. The general staff will decide what the government's forces defend first.",
         "The army will hold the cities, where most people live and the state's offices stand. Holding the cities keeps the government visible; it leaves the mines to whoever takes them.",
         "The army will take the mines, which pay for every side's war. Holding the mines funds the government; it leaves the cities to fend for themselves.",
         "Convoys and roads will be protected so that food and fuel reach the cities and the front. A road kept open feeds a city; a road lost starves it.",
         "A completed, funded service period under the chosen strategy must be reviewed before it becomes doctrine. The review counts what was held, what was lost and what got through.",
         "The settlement records what the government's forces held and why. It does not decide the war. It leaves an account of what each choice cost."),
        (("command", "security"), ("civil", "security"), ("industry", "command"), ("logistics", "rail"), ("scales", "command"), ("command", "peace")),
        (("Hold the cities", {"army_core_defence_factor": 0.04}, {"production_factory_efficiency_gain_factor": -0.02}),
         ("Take the mines", {"industrial_capacity_factory": 0.03}, {"stability_factor": -0.02})),
        (("Escort the Convoys", "Escort the convoys on the main roads for one period.", "The army's transport command", {"supply_consumption_factor": -0.03}),
         ("Fortify a City", "Fortify one city's approaches and supply stores.", "The general staff", {"army_core_defence_factor": 0.03})),
        ("A Mine Town Asks for Soldiers",
         "A mining town besieged by a faction asks for a battalion. The general staff can send one only by taking it from a city's garrison.\n\nThe government can publish the choice and its reasons, or let the general staff decide without an announcement.",
         ("Publish the choice.", "Let the staff decide.")),
        ("The Front Held",
         "The final review lists the cities, mines and roads the government's forces held, year by year. The besieged mining town is there, with what happened to it.\n\nThe front moved. The review records where.")),
    Branch("LEA", "settlement", (), STARTED,
        ("Seek an End to the War", "Talks Across the Lines", "Victory First",
         "Prepare the Amnesty", "Review a Settlement Period", "A War That Ended"),
        ("Ten years is a long time for a country to fight itself. The government must decide whether it will talk to the factions or fight until they stop.",
         "The government will open talks with every faction that names a negotiator, with ceasefires local first and national later. Talks may end the war sooner; they also give every faction a seat it did not win.",
         "The government will fight until the factions surrender, with talks only on the terms of surrender. Victory settles the question of who governs; it takes as long as the factions can fight.",
         "An amnesty will be drafted for fighters who lay down their arms, with exceptions for crimes the courts must hear. An amnesty is the bridge a war crosses to become a peace.",
         "A completed, funded service period under the chosen approach must be reviewed before it becomes the country's settlement. The review asks who came to the table, and who stayed away.",
         "The settlement records how Leasath's civil war was meant to end. The official record says only that it ended in 2019. This record says how the government tried."),
        (("diplomacy", "peace"), ("diplomacy", "assembly"), ("command", "security"), ("document", "scales"), ("scales", "diplomacy"), ("peace", "assembly")),
        (("Talks across the lines", {"stability_factor": 0.025}, {"war_support_factor": -0.03}),
         ("Victory first", {"war_support_factor": 0.04}, {"stability_factor": -0.02})),
        (("Hold a Round of Talks", "Hold one round of talks with the factions' negotiators.", "The foreign ministry", {"political_power_gain": 0.08}),
         ("Draft the Amnesty Rolls", "Compile the rolls of fighters eligible for the amnesty.", "The ministry of justice", {"stability_factor": 0.025})),
        ("A Negotiator Who Was a Commander",
         "The largest faction has named as its negotiator a commander accused of shelling a market. The government's own negotiators refuse to sit with him.\n\nThe government can accept him and publish the accusation alongside the talks, or refuse him and ask the faction for someone else.",
         ("Accept him and publish the accusation.", "Ask for someone else.")),
        ("A War That Ended",
         "The final review lists the talks held, the ceasefires agreed and broken, and the amnesty's rolls. The commander-negotiator is there, with what the courts later decided.\n\nThe war ended. The review records how much of the ending the government chose.")),
)

OPENINGS = {
    "LEA": ("A Country Rich Underground",
        "The cabinet meets with the country's oldest arguments in front of it: the mines and who works them, the provinces and who governs them, the army and whom it serves.\n\n[LEA_le_route_context]\n\nThe question before the cabinet is which of these arguments to settle first, and how much of the settling to do in public.",
        ("Open the arguments to public questions.", "Begin with a protected cabinet docket.")),
}

ROUTE_CONTEXT = {
    "LEA": (("has_global_flag = ac_lcw_historical_end", "The civil war is over, ended in 2019 as the official record says, after ten years of fighting."),
            ("has_global_flag = ac_lcw_negotiated", "The civil war ended in a negotiated settlement this government earned."),
            ("has_global_flag = ac_lcw_ended", "The civil war is over, later than the official record says."),
            (RUNNING, "The civil war is being fought; the official record says it lasted ten years."),
            (None, "The country is at peace with itself, for now.")),
}

FINALS = {
    "LEA": ("A Country That Knows Its Grievances",
        "The last review of the period sets Leasath's records side by side: the mines, the provinces, the army, the workers and the civil war. Each has a cost and a record of what it delivered.\n\nThe arguments are not settled. They are written down, which is the first thing a country needs before it can settle them without fighting.",
        {"stability_factor": 0.02}),
}

FOUNDATION = " ".join(f"has_country_flag = LEA_le_{k}_settlement_done" for k in ("mines", "provinces", "army", "labour"))
WAVE = Wave(
    prefix=P, infix="le", label="Leasath's Foundation and Civil War", source="tools/content_waves",
    countries={"LEA": "Leasath"}, eligible="",
    branches=BRANCHES,
    layout={"LEA_mines": (2, 1), "LEA_provinces": (8, 1), "LEA_army": (14, 1), "LEA_labour": (20, 1),
            "LEA_government": (5, 7), "LEA_front": (11, 7), "LEA_settlement": (17, 7)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"LEA": f"OR = {{ has_country_flag = LEA_le_settlement_settlement_done {FOUNDATION} }}"},
    themes={"LEA": ("industry", "assembly")},
    weekly_extra={"LEA": "ac_lcw_owner_weekly = yes\n"},
    event_base=50,
)

# Authority the civil-war branches add (provisional gameplay). The war ends historically in
# 2019 at 50 or more; the earned settlement ends it on the talks' own terms.
AUTHORITY = {("government", "policy_a"): 10, ("government", "policy_b"): 15, ("government", "settlement"): 10,
             ("front", "policy_a"): 15, ("front", "policy_b"): 10, ("front", "settlement"): 10,
             ("settlement", "policy_a"): 5, ("settlement", "policy_b"): 10, ("settlement", "settlement"): 5}
BRANCHES = tuple(
    Branch(**{**b.__dict__,
              "policy_effects": (guard(RUNNING, authority(AUTHORITY.get((b.key, "policy_a"), 0))) if (b.key, "policy_a") in AUTHORITY else "",
                                 guard(RUNNING, authority(AUTHORITY.get((b.key, "policy_b"), 0))) if (b.key, "policy_b") in AUTHORITY else ""),
              "settlement_effect": guard(RUNNING, authority(AUTHORITY[(b.key, "settlement")])) if (b.key, "settlement") in AUTHORITY else ""})
    for b in BRANCHES)
WAVE = Wave(**{**WAVE.__dict__, "branches": BRANCHES})

START = "2008.12.31"       # the war's start about 2009 is derived from "ten years" (Chronicle, 2019 / XX.XX)
LATE_LIMIT = "2010.1.1"    # a first observation in 2010 or later never starts a war the record places a decade earlier


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

    triggers["ac_lcw_running"] = RUNNING
    triggers["ac_lcw_settlement_earned"] = ("tag = LEA original_tag = LEA has_country_flag = LEA_le_settlement_policy_a_done "
                                            "has_country_flag = LEA_le_settlement_operations_done")
    end = "remove_ideas = ac_lcw_civil_war\nadd_timed_idea = { idea = ac_lcw_war_over days = 365 }\n"
    effects["ac_lcw_owner_weekly"] = guard("tag = LEA original_tag = LEA NOT = { has_global_flag = ac_lcw_closed }",
        # Opening: the derived 2009 start, never replayed by a late first observation.
        guard(f"date > {START} NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_lcw_late_start_skipped }}",
              guard(f"date < {LATE_LIMIT} has_capitulated = no",
                    "set_global_flag = ac_lcw_started\nset_variable = { ac_lcw_authority = 40 }\nadd_ideas = ac_lcw_civil_war\n"
                    "news_event = { id = ac_lcw.1 days = 1 }") +
              block("else", "set_global_flag = ac_lcw_late_start_skipped\nset_global_flag = ac_lcw_closed")) +
        guard("ac_lcw_running = yes",
              # The historical end: within 2019 and on the government's own authority, never before.
              guard("date > 2018.12.31 date < 2020.1.1 check_variable = { ac_lcw_authority > 49 }",
                    "set_global_flag = ac_lcw_ended\nset_global_flag = ac_lcw_historical_end\n" + end + "news_event = { id = ac_lcw.2 days = 1 }") +
              block("else_if", block("limit", "NOT = { date < 2020.1.1 } NOT = { has_global_flag = ac_lcw_prolonged }") +
                    "set_global_flag = ac_lcw_prolonged\nnews_event = { id = ac_lcw.3 days = 1 }") +
              block("else_if", block("limit", "has_global_flag = ac_lcw_prolonged check_variable = { ac_lcw_authority > 49 }") +
                    "set_global_flag = ac_lcw_ended\nset_global_flag = ac_lcw_late_end\n" + end + "news_event = { id = ac_lcw.4 days = 1 }")))
    effects["ac_lcw_negotiate"] = guard("ac_lcw_running = yes ac_lcw_settlement_earned = yes",
        "set_global_flag = ac_lcw_ended\nset_global_flag = ac_lcw_negotiated\n" + end + "news_event = { id = ac_lcw.5 days = 1 }")
    effects["ac_lcw_interrupt_war"] = guard("tag = LEA original_tag = LEA ac_lcw_running = yes",
        "set_global_flag = ac_lcw_closed\nset_global_flag = ac_lcw_interrupted\nremove_ideas = ac_lcw_civil_war\nnews_event = { id = ac_lcw.6 days = 1 }")

    idea("ac_lcw_civil_war", "Civil War in Leasath", "The ACES Chronicle records that the Leasath Civil War ended in 2019 after ten years of fighting (2019 / XX.XX); this campaign starts it in 2009, a date derived from that sentence. The values, the sides and the authority measure are provisional gameplay. No tag or border changes.",
         {"stability_factor": -0.1, "political_power_gain": -0.1, "production_factory_efficiency_gain_factor": -0.05})
    idea("ac_lcw_war_over", "After the Civil War", "The civil war is over. The country recovers for a year; the value is provisional gameplay.",
         {"stability_factor": 0.03, "war_support_factor": 0.02})
    texts = {
        1: ("Civil War in Leasath",
            "Leasath is at war with itself. The ACES Chronicle records that the Leasath Civil War ended in 2019 after ten years of fighting (2019 / XX.XX); this campaign begins it in 2009, a date derived from that sentence.\n\nThe record does not say who fought or why. The factions, the authority measure and the government's choices are this campaign's own provisional account; no tag, border or leader changes.",
            "A long war begins.", "ac_lcw_news_begins"),
        2: ("The Leasath Civil War Ends",
            "Leasath's civil war has ended after ten years of fighting, as the ACES Chronicle records for 2019 (2019 / XX.XX). The record gives neither the day nor the victor, and this campaign names none.\n\nThe government ended the war on its own authority, measured in this campaign's provisional terms.",
            "Begin the recovery.", "ac_lcw_news_ends"),
        3: ("Leasath's War Goes On",
            "2019 has ended, and Leasath's civil war has not. The ACES Chronicle records its end in 2019 (2019 / XX.XX); in this history the government's authority did not reach far enough.\n\nThe war will end when the government's authority is restored or a settlement is earned. This is a provisional alternative to the official record.",
            "The war goes on.", "ac_lcw_news_begins"),
        4: ("The Leasath Civil War Ends at Last",
            "Leasath's civil war has ended, later than the ACES Chronicle records (2019 / XX.XX). The government's authority has finally reached across the country.\n\nThis provisional alternative ends the war on its own terms; the record's date is a reference anchor.",
            "Begin the recovery.", "ac_lcw_news_ends"),
        5: ("A Negotiated Peace in Leasath",
            "Leasath's government and its opponents have agreed a settlement. The talks the government chose, and the rounds it funded, ended the war on terms every side signed.\n\nThe ACES Chronicle records the war's end in 2019 (2019 / XX.XX) without saying how. This earned settlement is provisional gameplay.",
            "Sign the settlement.", "ac_lcw_news_ends"),
        6: ("Leasath's Civil War Interrupted",
            "Leasath has fallen to a foreign power while its civil war was still being fought. The civil-war owner closes; the record's 2019 end will not be reported.\n\nNothing about the factions is decided by this record.",
            "Record the interruption.", "ac_lcw_news_begins"),
    }
    for number, (title, prose, label, picture) in texts.items():
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, label
        news(number, picture)

    # Decisions: the earned settlement and the tree adoption.
    decisions = {}
    loc.update({
        TREE_ID: "Leasath: Mines, Provinces and War",
        TREE_ID + "_desc": "The mines, the provinces, the army, the workers and the civil war of 2009-2019. Provisional gameplay.",
        "LEA_le_adopt_campaign": "Adopt the National Programme",
        "LEA_le_adopt_campaign_desc": "Switch from the regional or generic focus tree to Leasath's national programme. Completed focuses are kept. Available only while no regional or generic focus is in progress.",
        "LEA_le_negotiate_settlement": "Sign the Negotiated Settlement",
        "LEA_le_negotiate_settlement_desc": "End the civil war on the terms of the talks this government chose and funded. The ACES Chronicle records the war's end in 2019 (2019 / XX.XX) without saying how; this earned settlement is provisional gameplay.",
    })
    adopt = block("LEA_le_adopt_campaign",
        "icon = ac_lcw_LEA_le_adopt_campaign\nallowed = { tag = LEA original_tag = LEA }\n"
        f"visible = {{ tag = LEA original_tag = LEA NOT = {{ has_focus_tree = {TREE_ID} }} ac_pol_previous_tree_idle = yes }}\n"
        "available = { ac_pol_previous_tree_idle = yes }\ncost = 0\n" +
        block("complete_effect", f"load_focus_tree = {{ tree = {TREE_ID} keep_completed = yes }}") + "ai_will_do = { base = 10 }\n")
    negotiate = block("LEA_le_negotiate_settlement",
        "icon = ac_lcw_LEA_le_negotiate_settlement\nallowed = { tag = LEA original_tag = LEA }\n"
        "visible = { ac_lcw_running = yes }\navailable = { ac_lcw_running = yes ac_lcw_settlement_earned = yes }\n"
        "cost = 50\nfire_only_once = yes\n" + block("complete_effect", "ac_lcw_negotiate = yes") + "ai_will_do = { base = 5 }\n")
    decisions["ac_lcw_lea_services"] = [adopt, negotiate]

    status = (("has_global_flag = ac_lcw_historical_end", "Civil war ended in 2019, as the record says (2019 / XX.XX)."),
              ("has_global_flag = ac_lcw_negotiated", "Civil war ended in an earned settlement (provisional)."),
              ("has_global_flag = ac_lcw_late_end", "Civil war ended after 2019 (provisional alternative)."),
              ("has_global_flag = ac_lcw_interrupted", "Closed: Leasath fell to a foreign power in its civil war."),
              ("has_global_flag = ac_lcw_prolonged", "Civil war past 2019: authority [?ac_lcw_authority|0]/100, needs 50."),
              (RUNNING, "Civil war since 2009 (derived): authority [?ac_lcw_authority|0]/100."),
              ("has_global_flag = ac_lcw_late_start_skipped", "Closed: first loaded after 2009; no civil war is started."),
              (None, "Pending: the civil war the record ends in 2019 begins about 2009."))
    entries = ""
    for n, (condition, value) in enumerate(status):
        loc[f"ac_lcw_status_{n}"] = value
        entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + f"localization_key = ac_lcw_status_{n}")
    custom = block("defined_text", "name = ac_lcw_status_text\n" + entries)
    for tag, rows_ in ROUTE_CONTEXT.items():
        entries = ""
        for n, (condition, value) in enumerate(rows_):
            key = f"{tag}_le_route_context_{n}"
            loc[key] = value
            entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + "localization_key = " + key)
        custom += block("defined_text", f"name = {tag}_le_route_context\n" + entries)
    loc.update({
        "ac_lcw_started": "Leasath's civil war has begun",
        "ac_lcw_ended": "Leasath's civil war has ended",
        "ac_lcw_historical_end": "Leasath's civil war ended in 2019, as the record says",
        "ac_lcw_negotiated": "Leasath's civil war ended in an earned settlement",
        "ac_lcw_late_end": "Leasath's civil war ended after 2019",
        "ac_lcw_prolonged": "Leasath's civil war ran past 2019",
        "ac_lcw_closed": "The Leasath civil-war owner is closed",
        "ac_lcw_interrupted": "Leasath fell to a foreign power during its civil war",
        "ac_lcw_late_start_skipped": "This content first loaded after 2009; no civil war was started",
        "ac_lcw_running": "Leasath's civil war is being fought",
        "ac_lcw_settlement_earned": "The government's talks and funded rounds earned a settlement",
    })
    hooks = {
        # on_annex: ROOT is the annexer and FROM the annexed; on_capitulation_immediate: ROOT capitulated.
        "on_annex": "FROM = { if = { limit = { tag = LEA original_tag = LEA } ac_lcw_interrupt_war = yes } }",
        "on_capitulation_immediate": "if = { limit = { tag = LEA original_tag = LEA } ac_lcw_interrupt_war = yes }",
    }
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                categories=[], decisions=decisions, hooks=hooks, category_prefix={"LEA": "[ac_lcw_status_text]\n\n"})


# Registry declarations ------------------------------------------------------
KEY = "F2a"
NAME = "leasath"
TREES = {"LEA": TREE_ID}
LEDGER = "docs/CONTENT_WAVE_F2.md"
SOURCES = {"official": ["Chronicle 2019 / XX.XX: the Leasath Civil War ends after ten years (start about 2009, derived)"],
           "mod_provenance": "Leasath's country history and institution and world-start profiles, read only",
           "provisional_gameplay": "Every focus, policy, service, dialogue and value; the authority measure; the prolonged and negotiated alternatives"}
NEWS_ART = (("ac_lcw_news_begins", ("security", "industry"), "Civil War in Leasath", "LEA"),
            ("ac_lcw_news_ends", ("peace", "assembly"), "The Leasath Civil War Ends", "LEA"))
EVENT_ART = ()
OWNER_ART = {"ac_lcw_civil_war": ("security", "assembly", "LEA"), "ac_lcw_war_over": ("peace", "rebuild", "LEA")}
