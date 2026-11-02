"""Wave D: Nordennavic, 1991-2016 (Packages 1/3/4).

Source layers
-------------
* Mod provenance: Nordennavic's country history, starting government office,
  world-start foundation (regional maritime reserve), institutional profile
  (scope of consultation) and the guarded 2004 Anean bureau invitation.
* Provisional gameplay: every focus, policy, service, dialogue and value here.
  No ACES Chronicle entry for Nordennavic has been compiled, so no dated event,
  named person, place, alliance, border or war role is asserted. The
  neutrality branch prepares for a neighbour's conflict without assuming one.
"""
from content_waves.framework import Branch, Wave, block

STAGE_1 = ("harbours", "reserve", "consultation")
STAGE_2 = ("technical_reserve", "northern_routes")
STAGE_3 = ("neutral_waters", "account")


def settled(keys):
    return tuple(f"NEC_nc_{k}_settlement" for k in keys)


BRANCHES = (
    Branch("NEC", "harbours", (), "",
        ("A Register of Northern Harbours", "Open Commercial Berths", "Reserve Fleet Anchorages",
         "Winter Repairs Before Summer Promises", "Review a Harbour Season", "Harbours Ready in Every Season"),
        ("Nordennavic's harbours serve fishing fleets, coastal freight and the maritime reserve, often from the same quays. The harbour board will record every berth, crane and repair crew, and which service has first claim on each.",
         "Commercial berths will have priority at the busiest harbours. Trade and fishing gain predictable access, and the reserve accepts longer notice whenever it needs a quay for exercises or repairs.",
         "Selected anchorages will be held for the maritime reserve throughout the year. The reserve can assemble quickly, while freight and fishing pay the price in crowded remaining berths.",
         "Ice, storms and short daylight decide what a northern harbour can do. Maintenance crews will finish winter repairs before the board promises summer capacity to anyone.",
         "The board will review one funded harbour season that actually finished. A plan that worked on paper but failed in the first storm cannot become national practice.",
         "The settlement keeps the chosen priority and a maintenance calendar that respects the weather. Harbours remain limited by their quays and crews; the difference is that every promise is now made against a real season."),
        (("navy", "document"), ("fishing", "economy"), ("navy", "security"), ("tools", "navy"), ("scales", "navy"), ("navy", "peace")),
        (("Commercial berth priority", {"production_factory_efficiency_gain_factor": 0.025}, {"naval_coordination": -0.01}),
         ("Reserved fleet anchorages", {"naval_coordination": 0.025}, {"consumer_goods_factor": 0.005})),
        (("Fund a Harbour Survey Season", "Survey quays, cranes and channels before the next season's commitments are made.", "The northern harbour board", {"production_speed_infrastructure_factor": 0.04}),
         ("Run a Reserve Mooring Rota", "Rotate reserve vessels through maintenance berths without displacing scheduled freight.", "The maritime reserve staff", {"repair_speed_factor": 0.04})),
        ("The Same Quay, Three Times",
         "The harbour master's board shows one quay booked three times for the same week: a fish-processing ship, a fuel delivery and a reserve vessel due for hull inspection. Each booking was made correctly by a different office. None of them knew about the others.\n\nThe board's secretary proposes publishing the whole season's bookings, so that every user can see the conflicts and settle them before the boats arrive. The reserve staff would rather keep its bookings in a separate protected list; announcing when reserve vessels are in for repair tells anyone watching when they are not at sea.",
         ("Publish the season's bookings.", "Keep reserve bookings in a protected list.")),
        ("A Harbour Calendar That Includes the Weather",
         "The final review is a calendar with storms marked on it. Winter repairs come first; summer capacity is promised only after they are finished. The quay that was booked three times now has one booking per week, and a note explaining which service waits when the weather closes the harbour.\n\nNobody claims the harbours are larger than they were. The board claims only that its promises can now be kept.")),
    Branch("NEC", "reserve", (), "",
        ("Keep the Maritime Reserve Honest", "Civil Crews in Reserve", "Standing Reserve Squadrons",
         "Train with the Ships We Have", "Review a Reserve Training Period", "A Reserve That Answers When Called"),
        ("The maritime reserve exists partly on paper: crews listed against vessels that are laid up, sold or crewed by the same people twice. The reserve staff will count the sailors and hulls that could actually sail.",
         "Reserve crews will keep civilian jobs on fishing boats, ferries and freighters and train in short, regular periods. The country keeps their skills at sea, and accepts a slower call-up.",
         "A small number of reserve squadrons will be kept crewed and ready throughout the year. They can respond quickly, and the crews they keep from civilian work are a cost the coastal economy feels.",
         "Training will use the vessels Nordennavic actually has, not the ones in old plans. No exercise will assume a hull that has not been inspected or a crew that has not been called.",
         "The staff will review a completed, funded training period before its methods replace the old reserve rules. Attendance, inspected vessels and lessons recorded matter more than the size of the list.",
         "The settlement fixes the reserve's size, readiness and cost at a level the country can sustain. It creates no new ships. It gives the government a reserve whose numbers can be trusted."),
        (("navy", "scales"), ("fishing", "training"), ("navy", "command"), ("training", "navy"), ("scales", "training"), ("medal", "navy")),
        (("Civil crews in reserve", {"repair_speed_factor": 0.03}, {"naval_coordination": -0.01}),
         ("Standing reserve squadrons", {"naval_coordination": 0.025}, {"production_factory_efficiency_gain_factor": -0.01})),
        (("Call Up a Training Period", "Call reserve crews for a scheduled period aboard inspected vessels.", "The maritime reserve staff", {"naval_coordination": 0.03}),
         ("Inspect the Reserve Returns", "Reconcile crew lists and vessel inspections with the reserve register.", "The reserve inspectorate", {"repair_speed_factor": 0.04})),
        ("The Name on Two Lists",
         "A ferry engineer appears on the reserve list twice: once as chief engineer of a patrol vessel and once as a deck hand on a minesweeper that was sold for scrap years ago. He also appears, correctly, on the ferry company's roster for the winter season. When the reserve staff call him for training, the ferry company calls the ministry.\n\nThe reserve inspector wants to publish the corrected list, so that employers and reservists can check it for themselves. The staff would prefer to correct it internally; a public list of how few crews the reserve really has is not a document it wants to circulate.",
         ("Publish the corrected reserve list.", "Correct the list internally.")),
        ("A Smaller List That Is True",
         "The reserve list at the end of the review is shorter than the one at the beginning. Every name on it belongs to a person who answered the last call, and every vessel to a hull that passed its last inspection. The ferry engineer appears once, with a training period scheduled outside the winter season.\n\nThe reserve is not stronger because its list is shorter. It is more useful, because the government now knows what it can ask of it.")),
    Branch("NEC", "consultation", (), "",
        ("Decide What We Will Discuss", "Open Technical Consultation", "A Narrow Diplomatic Mandate",
         "Answer Invitations Without Overpromising", "Review the Consultation Record", "Consultation on Our Own Terms"),
        ("Neighbouring governments and regional bodies send invitations to talks, studies and exercises. The foreign ministry will record which subjects Nordennavic is willing to discuss, who may speak for it and what it will not commit to.",
         "Engineers, harbour officials and scientists may consult foreign counterparts on technical matters without a ministerial mandate for each meeting. Expertise travels more easily, and the ministry has less control over what is said.",
         "Only the foreign ministry will speak for Nordennavic, on subjects the cabinet has approved in advance. The country's commitments stay clear and limited, and many useful technical contacts are slower to arrange.",
         "Every invitation will receive an answer that states what Nordennavic can offer and what it cannot. A clear refusal is better than an acceptance that later has to be withdrawn.",
         "The ministry will review a completed, funded consultation period before its rules become permanent. The review asks which contacts produced useful work and which only produced obligations.",
         "The settlement keeps the chosen scope of consultation and the costs that come with it. It joins no alliance and accepts no other government's authority. Nordennavic decides, case by case, what to discuss."),
        (("diplomacy", "document"), ("science", "diplomacy"), ("diplomacy", "gate"), ("communications", "document"), ("scales", "diplomacy"), ("diplomacy", "peace")),
        (("Open technical consultation", {"research_speed_factor": 0.015}, {"political_power_gain": -0.05}),
         ("Narrow diplomatic mandate", {"political_power_gain": 0.05}, {"research_speed_factor": -0.01})),
        (("Staff the Consultation Desk", "Answer invitations, brief delegations and record what was discussed.", "The foreign ministry consultation desk", {"political_power_gain": 0.08}),
         ("Publish the Consultation Record", "Publish a summary of consultations and the commitments they did or did not create.", "The foreign ministry", {"stability_factor": 0.025})),
        ("An Invitation Accepted by the Wrong Office",
         "A harbour engineer accepted an invitation to a regional technical meeting, which was entirely within her remit. At the meeting she was asked whether Nordennavic would join a shared maintenance roster, and she said she would ask. The other delegations recorded her answer as a promise.\n\nThe consultation desk proposes publishing the meeting record with a note on what Nordennavic did and did not agree to, so that the misunderstanding is corrected in public. The ministry would rather send a private letter to each delegation; correcting a colleague in public may make technical experts reluctant to attend the next meeting.",
         ("Publish the meeting record with a correction.", "Correct the record privately with each delegation.")),
        ("A Record of What Was Agreed",
         "The consultation record at the end of the period lists every meeting, who spoke for Nordennavic and what, if anything, was agreed. Most entries say nothing was agreed, which is accurate and useful. The harbour engineer's meeting is listed with its correction.\n\n[NEC_nc_anean_record]\n\nThe settlement does not make Nordennavic more or less willing to cooperate. It makes its willingness legible.")),
    Branch("NEC", "technical_reserve", settled(STAGE_1), "date > 2005.12.31",
        ("A National Technical Reserve", "A Civil Engineering Reserve", "A Defence Technical Reserve",
         "Keep the Skills Current", "Review a Reserve Call-Up", "Expertise the Country Can Call On"),
        ("Engineers, electricians and technicians who left public service still hold skills the country may need in a storm, a disaster or a crisis. The government will record who is willing to be called, for what work and on what terms.",
         "The technical reserve will be organised around civil emergencies: power, water, harbours and communications. Its members train for the disasters a northern country expects, and defence work receives less priority.",
         "The technical reserve will support the armed forces' maintenance and communications first. Defence gains depth, and civil authorities must plan for emergencies with fewer reserve specialists.",
         "A reserve register is only useful if its members can still do the work. Short refresher periods will keep skills current and remove names that no longer match a real person and skill.",
         "The government will review a completed, funded call-up before the reserve's rules become permanent. The review asks who answered, what they could do and how long it took.",
         "The settlement fixes the technical reserve's purpose, size and cost. It conscripts no one. It gives Nordennavic a list of skilled people it can actually call, and the obligation to treat them fairly."),
        (("tools", "document"), ("civil", "tools"), ("tools", "security"), ("training", "tools"), ("scales", "tools"), ("tools", "peace")),
        (("Civil engineering reserve", {"production_speed_infrastructure_factor": 0.04}, {"political_power_gain": -0.05}),
         ("Defence technical reserve", {"repair_speed_factor": 0.035}, {"consumer_goods_factor": 0.005})),
        (("Call Up a Technical Exercise", "Call reserve specialists for a scheduled exercise on real equipment.", "The national technical reserve office", {"production_speed_infrastructure_factor": 0.045}),
         ("Run a Refresher Period", "Retrain reserve members on current equipment and procedures.", "The technical reserve training board", {"repair_speed_factor": 0.04})),
        ("The Switchboard Nobody Remembers",
         "During the first exercise the reserve office asks a retired telephone engineer to restore an old coastal switchboard kept for emergencies. He can do it, but only he can: the manuals are lost and the two colleagues who also knew the system have died. The exercise succeeds and the report raises an uncomfortable question about everything else the reserve depends on.\n\nThe reserve office wants to publish a list of skills held by fewer than three registered people, so that training can be planned openly. The defence staff argues that such a list would describe the country's weakest points exactly, and wants it kept protected.",
         ("Publish the list of rare skills.", "Keep the list of rare skills protected.")),
        ("Skills Written Down",
         "The final review lists the skills the reserve can call on, how many people hold each and when they last practised. The coastal switchboard has a new manual, written by the retired engineer and two younger technicians he trained during the refresher period.\n\nThe reserve remains small. Its members are no longer the only copy of what they know.")),
    Branch("NEC", "northern_routes", settled(STAGE_1), "date > 2005.12.31",
        ("Northern Shipping Routes", "Protected Fishing and Freight Lanes", "Patrolled Approaches",
         "Rescue Before Patrol Schedules", "Review a Season at Sea", "Routes Kept Open"),
        ("Fishing grounds, coastal freight lanes and the approaches to the harbours share the same cold waters. The maritime authority will chart which routes matter most, in which seasons, and who answers when a vessel is in trouble.",
         "Fishing and freight lanes will receive protected status, weather services and priority for rescue resources. Coastal communities gain security for their livelihoods, and the reserve has fewer ships for other tasks.",
         "The approaches to Nordennavic's harbours will be patrolled regularly by reserve vessels. Visible patrols deter trouble and reassure the public, at a steady cost in fuel and crews.",
         "Every patrol will also be a rescue service. A crew that passes a vessel in distress to complete its patrol schedule has failed at the more important task.",
         "The authority will review one funded season at sea that actually finished, counting rescues, inspections and routes kept open rather than miles patrolled.",
         "The settlement keeps the chosen protection for the northern routes and a rescue service built into every patrol. It claims no new waters and changes no border."),
        (("fishing", "navy"), ("fishing", "logistics"), ("navy", "radar"), ("medical", "navy"), ("scales", "fishing"), ("logistics", "peace")),
        (("Protected fishing and freight lanes", {"production_factory_efficiency_gain_factor": 0.025}, {"naval_coordination": -0.01}),
         ("Patrolled approaches", {"naval_coordination": 0.03}, {"consumer_goods_factor": 0.005})),
        (("Fund a Rescue Coordination Season", "Keep rescue coordination, weather reporting and standby crews ready for a season.", "The maritime authority", {"stability_factor": 0.025}),
         ("Run an Approach Patrol Period", "Patrol harbour approaches on a published schedule that includes rescue duties.", "The maritime reserve staff", {"naval_coordination": 0.03})),
        ("A Patrol That Turned Back",
         "A reserve patrol vessel abandoned its scheduled route to assist a fishing boat with a flooded engine room, and towed it home through a rising storm. The patrol log records the route as incomplete. The fishing community records the crew as heroes. The maritime authority must decide which record it intends to keep.\n\nThe authority's director wants the incident published as an example of what the patrols are for. The reserve staff would rather report it internally; a public account of a patrol leaving its route also tells observers when the approaches were unwatched.",
         ("Publish the incident as an example.", "Report the incident internally.")),
        ("A Season Counted in Rescues",
         "The final review counts rescues, inspections and routes kept open, and only then miles patrolled. The patrol that turned back appears in the first column, not as a failure in the last.\n\nThe northern routes are no safer from the weather than they were. The people who use them now know who will come when it turns.")),
    Branch("NEC", "neutral_waters", settled(STAGE_2), "date > 2013.12.31",
        ("Neutral Waters in a Troubled Region", "Humanitarian Transit Only", "Armed Neutral Patrols",
         "Say No Before Being Asked", "Review a Neutrality Period", "A Neutrality Others Can Rely On"),
        ("Relations among Nordennavic's neighbours are tense, and nobody can promise that a crisis beyond its waters will stay there. The government will decide in advance what passage, supplies and services it would permit if one came.",
         "Only humanitarian transit and civilian trade will be permitted through Nordennavic's waters and ports during a neighbour's conflict. The rule is simple to explain and to verify, and it leaves the country with little leverage.",
         "Neutral patrols will make sure no side uses Nordennavic's waters or ports for its own purposes. Armed neutrality is credible and expensive, and it needs ships at sea when others would prefer they were not.",
         "Requests for passage, fuel and repairs will be answered according to published rules, before a crisis makes every answer political. A refusal announced early is easier to defend than one improvised under pressure.",
         "The government will review a completed, funded neutrality period before its rules are fixed. The review asks whether the rules were understood, applied consistently and respected.",
         "The settlement fixes the terms of Nordennavic's neutrality and the costs of maintaining it. It takes no side in any conflict, joins no faction and makes no claim on a neighbour."),
        (("peace", "navy"), ("medical", "logistics"), ("navy", "security"), ("gate", "document"), ("scales", "peace"), ("peace", "diplomacy")),
        (("Humanitarian transit only", {"stability_factor": 0.025}, {"naval_coordination": -0.01}),
         ("Armed neutral patrols", {"naval_coordination": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Fund a Port Control Period", "Inspect requests for passage, fuel and repairs under the published neutrality rules.", "The ports and customs authority", {"stability_factor": 0.025}),
         ("Run a Neutrality Patrol", "Patrol territorial waters to observe and report, without engaging foreign vessels.", "The maritime reserve staff", {"naval_coordination": 0.03})),
        ("A Fuel Request in Calm Weather",
         "A foreign naval auxiliary asks to refuel at a northern harbour during an ordinary week. There is no crisis and no war; the request is routine and the fuel is available. The customs officer on duty notices that the published neutrality rules do not say whether routine peacetime requests count as precedent for later ones.\n\nThe ports authority wants to publish the request and its answer, so that every government can see the rules applied in calm weather before anyone tests them in a storm. The foreign ministry would rather answer privately; publishing a foreign navy's movements is a diplomatic act in itself.",
         ("Publish the request and the answer.", "Answer the request privately.")),
        ("Rules That Were Tested Early",
         "The final review lists every request for passage, fuel and repairs during the period and the rule applied to each. Most were routine. A few were refused, and the refusals were accepted because the rules had been published before anyone needed them.\n\nNordennavic's neutrality is not a promise that its neighbours will keep the peace. It is a promise about what Nordennavic will do if they do not.")),
    Branch("NEC", "account", settled(STAGE_2), "date > 2013.12.31",
        ("The Reserve's Public Account", "A Civil Audit", "A Protected Reserve Ledger",
         "Count What the Reserve Costs", "Review the Long Service Record", "A Reserve the Public Understands"),
        ("The maritime and technical reserves have grown out of decisions made over many years. The government will publish what they cost, what they have delivered and what they are for, so that parliament decides the next budget with a full account.",
         "Independent auditors will examine the reserves' accounts and readiness, and their reports will be public. Confidence rises, and so does the political cost of every shortfall the audit finds.",
         "Readiness details will stay in a protected ledger shared only with the relevant parliamentary committee. Sensitive information stays protected, at the price of public suspicion about what is being kept back.",
         "Every vessel, specialist and harbour reservation will be costed, including the civilian work it displaces. A reserve that looks cheap because its costs are hidden is not cheap.",
         "The government will review a completed, funded audit or readiness period before the account becomes the standard for future budgets.",
         "The settlement fixes how the reserves are accounted for and reviewed. It keeps the chosen balance between openness and protection, and the obligation to explain the reserves to the people who pay for them."),
        (("document", "economy"), ("scales", "assembly"), ("document", "security"), ("economy", "scales"), ("scales", "document"), ("assembly", "peace")),
        (("Civil audit", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Protected reserve ledger", {"political_power_gain": 0.05}, {"stability_factor": -0.01})),
        (("Fund an Independent Audit", "Commission auditors to examine reserve accounts and readiness returns.", "The national audit office", {"stability_factor": 0.025}),
         ("Run a Readiness Inspection", "Inspect reserve vessels, harbours and specialists against the published account.", "The reserve inspectorate", {"naval_coordination": 0.025})),
        ("The Cost Nobody Listed",
         "The auditors find that the reserve's budget is accurate and incomplete. It lists salaries, fuel and maintenance. It does not list the fishing days lost when reserve crews train, the freight delayed when anchorages are reserved, or the hours civil engineers spend on defence work. Nobody hid those costs; nobody was asked to count them.\n\nThe audit office wants the full cost published. The defence committee agrees the costs are real but would rather the figures stay in the protected ledger, where they cannot be read as a measure of how much the country could lose in a crisis.",
         ("Publish the full cost of the reserves.", "Keep the full cost in the protected ledger.")),
        ("An Account That Includes Everyone",
         "The final account lists the reserves' cost in money, in lost fishing days, in delayed freight and in borrowed engineering hours. It also lists what the reserves delivered: rescues, repairs, harbour seasons that worked, and refusals given early enough to keep the peace.\n\nParliament can now argue about the reserves with the same numbers in front of every member. That is what the settlement was for.")),
)

OPENINGS = {
    "NEC": ("Three Ministries, One Quay",
        "The first inter-ministry meeting on the northern harbours begins with a map. The fisheries ministry has marked its landing quays, the transport ministry its freight berths and the defence ministry its reserve anchorages. Several marks sit on top of each other. None of the ministries is wrong; each has simply planned as if the others did not exist.\n\nThe cabinet must decide how to untangle them, and whether to do it in front of the coastal communities who will live with the result.",
        ("Open the harbour register to public questions.", "Begin with a protected ministry docket.")),
}
FINALS = {
    "NEC": ("A Northern Country That Knows Its Reserves",
        "The last review of the period sets the harbours, the maritime and technical reserves, the northern routes and the neutrality rules side by side. Each has a cost, a purpose and a record of what it delivered. Some delivered less than their founders hoped; the review says so.\n\nNordennavic has not become a larger or more powerful country. It has become one that can say, accurately, what it is able to do and what it is not.",
        {"naval_coordination": 0.02}),
}

WAVE = Wave(
    prefix="ac_nec", infix="nc", label="The Northern Reserve", source="tools/content_waves",
    countries={"NEC": "Nordennavic"}, eligible="",
    branches=BRANCHES,
    layout={"NEC_harbours": (2, 1), "NEC_reserve": (8, 1), "NEC_consultation": (14, 1),
            "NEC_technical_reserve": (5, 7), "NEC_northern_routes": (11, 7),
            "NEC_neutral_waters": (5, 13), "NEC_account": (11, 13)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"NEC": "has_country_flag = NEC_nc_neutral_waters_settlement_done has_country_flag = NEC_nc_account_settlement_done"},
    themes={"NEC": ("navy", "scales")},
)

TREE_ID = "nec_national_campaign"


def owner():
    """Tree adoption for saves that already hold the generic or regional tree,
    plus a read-only callback to the existing Anean bureau invitation."""
    loc = {
        TREE_ID: "Nordennavic: The Northern Reserve",
        TREE_ID + "_desc": "Harbours, the maritime and technical reserves, consultation and neutrality, 1991-2016. Provisional gameplay.",
        "NEC_nc_adopt_campaign": "Adopt the Northern Reserve Programme",
        "NEC_nc_adopt_campaign_desc": "Switch from the regional or generic focus tree to Nordennavic's national programme. Completed focuses are kept. Available only while no regional or generic focus is in progress.",
        "NEC_nc_anean_participates": "Nordennavic accepted the Anean bureau's invitation to consult on civilian infrastructure; the record lists that participation and its limits.",
        "NEC_nc_anean_declined": "Nordennavic did not join the Anean bureau's consultations; the record shows that decision as a choice, not a failure.",
        "NEC_nc_anean_none": "No invitation from the Anean bureau has been recorded.",
    }
    custom = block("defined_text", "name = NEC_nc_anean_record\n" +
        block("text", "trigger = { has_global_flag = ac_anea_nec_participates }\nlocalization_key = NEC_nc_anean_participates") +
        block("text", "trigger = { has_global_flag = ac_anea_nec_closed }\nlocalization_key = NEC_nc_anean_declined") +
        block("text", "localization_key = NEC_nc_anean_none"))
    adopt = block("NEC_nc_adopt_campaign",
        "icon = ac_nec_NEC_nc_adopt_campaign\nallowed = { tag = NEC original_tag = NEC }\n"
        f"visible = {{ tag = NEC original_tag = NEC NOT = {{ has_focus_tree = {TREE_ID} }} ac_pol_previous_tree_idle = yes }}\n"
        f"available = {{ ac_pol_previous_tree_idle = yes }}\ncost = 0\n" +
        block("complete_effect", f"load_focus_tree = {{ tree = {TREE_ID} keep_completed = yes }}") + "ai_will_do = { base = 10 }\n")
    return dict(loc=loc, custom=custom, decisions={"ac_nec_nec_services": [adopt]})
