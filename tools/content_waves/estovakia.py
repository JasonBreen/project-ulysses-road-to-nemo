"""Wave B: the Estovakian civil war, 2007-2013 (Package 3).

Source layers
-------------
* Official: the Chronicle chain compiled in docs/STRANGEREAL_2006_2020_SOURCES.md
  -- 2007 / 04.03 the Lyes Faction seizes the capital; 2007 / 06.30 the civil war
  begins; 2008 / 07.15 the Eastern Faction takes the northeastern oil platforms;
  2008 / 10.23 the Republic of Anea Initiative is put on hold; 2010 / 02.19 and
  2011 / 05.09 Emmeria ends aid; 2013 / 01.15 the Eastern Faction offensive;
  2013 / 10.29 General Lyes is killed and the war ends; 2013 / 11.25, 12.02 and
  2014 / 02.03-04 the aftermath. Super Weapons, Chandelier (incomplete).
* Factions and people (the Lyes United Front, the Eastern Faction, the Northern
  Highlands Faction, General Lyes, Isaac Arensky, Antonina Koznick) appear only
  in news text, exactly as the Chronicle names them.
* Provisional gameplay: the authority and strength values, their changes, the
  negotiated settlement, the prolonged-war alternative, every focus, policy,
  service, dialogue and number. The war is tagless: no start_civil_war,
  country tag, transfer_state, core, leader or ideology change. Existing Anea
  flags are read, never written.
"""
from content_waves.framework import Branch, Wave, block, guard

S = "ac_ecw"
STARTED = "has_global_flag = ac_ecw_capital_seized"
WAR = "has_global_flag = ac_ecw_war_running"

BRANCHES = (
    Branch("EVA", "capital", (), STARTED,
        ("Authority in the Capital", "Accommodate the Factions", "Order Through Suppression",
         "Keep the Ministries Working", "Review a Contested Year", "A Capital That Answers to the Country"),
        ("The Lyes Faction has seized the capital, and the ministries now take orders from a command much of the country does not accept. Officials must decide which instructions they will carry out, which they will delay, and how to keep ordinary services running while the question of authority is fought elsewhere.",
         "Ministries will open channels to the factions outside the capital, keep records of every local agreement and refuse orders that target civilians. Accommodation lowers the temperature and keeps a settlement possible, at the cost of authority in the capital and the anger of those who demand obedience.",
         "Order will be imposed from the capital: curfews, purges of disloyal officials and force against cities that resist. Suppression holds the capital and the ministries together for now, and hardens every faction it does not defeat.",
         "Whatever the policy, water, power and pensions still need officials who come to work. The ministries will protect a core of ordinary services from the conflict and keep a record of every instruction they were given and what they did with it.",
         "The cabinet will review one funded period of contested government rather than claim control from a map. The review asks which services reached the people they were meant for and which orders were refused, and by whom.",
         "The settlement fixes how the capital's offices work during and after the fighting. It decides nothing about who wins. It gives whichever government follows a civil service that kept records and kept working."),
        (("assembly", "security"), ("diplomacy", "civil"), ("security", "command"), ("tools", "civil"), ("scales", "document"), ("assembly", "peace")),
        (("Accommodation of the factions", {"stability_factor": 0.03}, {"political_power_gain": -0.06}),
         ("Order through suppression", {"army_org_factor": 0.03}, {"stability_factor": -0.03})),
        (("Staff the Core Services", "Keep water, power and pension offices staffed and outside the conflict.", "The ministry of public administration", {"stability_factor": 0.025}),
         ("Record the Instructions", "Log every order received and how each office answered it.", "The cabinet secretariat", {"political_power_gain": 0.08})),
        ("The Order That Was Not Signed",
         "An order arrives from the capital's new command: close the registry offices in three cities that have refused to recognise it. The registry director reads it twice and does not sign the forwarding slip. Without registries, families in those cities cannot record births, deaths or the property they have lost.\n\nThe director's deputy wants the refusal published, with the reasons, so that other offices know they are not alone. The director fears that a public refusal will bring soldiers to the ministry, and wants the record kept inside, where it can be produced later when someone asks who obeyed and who did not.",
         ("Publish the refused orders.", "Keep the refusals inside the ministry.")),
        ("What the Ministries Kept",
         "The final review is a ledger of instructions and answers. Some orders were carried out; some were delayed until they no longer mattered; a few were refused outright, and the officials who refused are named in the record. The registry offices in the three cities stayed open.\n\nThe review does not say who governs Estovakia. It says what its offices did while the question was being fought, which is what any government that follows will need to know."),
        policy_effects=("ac_ecw_shift_accommodation = yes\n", "ac_ecw_shift_suppression = yes\n")),
    Branch("EVA", "cities", (), WAR,
        ("The Cities That Resisted", "Protect the Civilians", "Restore Control First",
         "Food, Water and Medicine", "Review a Winter in the Cities", "Cities That Can Recover"),
        ("The LUF's suppression of the cities that resist has turned the dispute over the capital into a civil war. Whatever the cabinet's policy, people in those cities need food, water and medicine. The ministries will record which cities are cut off, who is supplying them and what is missing.",
         "Relief will reach civilians in contested cities whichever faction holds them, through local councils, churches and relief workers. Protection saves lives and earns trust, and it lets supplies reach people the capital would rather see starved into submission.",
         "Relief will follow control: cities that accept the capital's authority receive supplies, and those that resist receive them once they submit. The policy rewards loyalty and punishes resistance, and it is remembered in every city that went hungry.",
         "Supply convoys, water repairs and medical teams need routes, guarantees and people willing to drive them. The relief office will negotiate passage with whoever controls each road and keep a record of every convoy that arrived and every one that did not.",
         "The review covers one funded winter of relief in the contested cities. It counts the convoys that arrived, the clinics that stayed open and the cities that were reached, not the statements made about them.",
         "The settlement keeps the chosen relief policy and the convoy routes that worked. It leaves the cities with a record of who helped them, which will matter long after the fighting ends."),
        (("refugees", "document"), ("medical", "civil"), ("security", "gate"), ("logistics", "medical"), ("scales", "refugees"), ("shelter", "peace")),
        (("Civilian protection", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Control before relief", {"political_power_gain": 0.05}, {"stability_factor": -0.03})),
        (("Run a Relief Convoy Season", "Negotiate passage and run supply convoys to contested cities.", "The national relief office", {"stability_factor": 0.03}),
         ("Keep the Clinics Open", "Staff and supply clinics in cities cut off by the fighting.", "The ministry of health", {"production_speed_infrastructure_factor": 0.03})),
        ("A Convoy at the Checkpoint",
         "A relief convoy has waited two days at a checkpoint outside a city that refused the capital's authority. The officer in command has orders to let nothing through until the city's council submits. The convoy carries flour, insulin and water purification tablets; the driver's manifest lists them in order of how long the city can last without each.\n\nThe relief office can publish the manifest and the officer's orders, shaming the command into opening the road. Or it can negotiate quietly, trading something the officer's superiors want for a single night's passage that nobody announces.",
         ("Publish the convoy manifest and the orders.", "Negotiate a quiet passage.")),
        ("The Convoys That Arrived",
         "The final review lists the convoys by date, route and outcome. Most arrived, some late; a few were turned back, and the review names the checkpoints that turned them. The city outside which the convoy waited is in the list twice: once for the night it was refused, once for the night it was let through.\n\nThe cities will remember the war differently from the capital. The record gives both a common place to start."),
        policy_effects=("ac_ecw_shift_accommodation_small = yes\n", "ac_ecw_shift_suppression_small = yes\n")),
    Branch("EVA", "oil", (), STARTED,
        ("The Northeastern Platforms", "Public Operation Under Contract", "Keep the Platforms in State Hands",
         "Protect the Crews", "Review a Production Year", "Revenue That Outlasts the War"),
        ("The oil platforms in the northeast are held by a public corporation, and every faction can see what their revenue would buy. Before the fighting reaches them, the government will record what the platforms produce, who works on them and where the money goes.",
         "The platforms will keep producing under a published contract with the public corporation, with revenue paid into an account that no faction can draw on alone. The arrangement protects the crews and the income, and it depends on every side accepting a contract it did not write.",
         "The state will take direct control of the platforms and their revenue, with guards sent from the capital. Control denies the revenue to the factions in the northeast, and it makes the platforms a target that guards alone may not be able to hold.",
         "Whoever holds the platforms, the people on them need relief crews, safe transport and pay. The corporation will keep a register of every crew member and a plan to evacuate them if the fighting arrives.",
         "The review covers one funded production year: barrels produced, revenue paid and crews kept safe. Promises about future output do not count.",
         "The settlement fixes how the platforms' revenue is held and spent, and it keeps the crews' register. Whoever governs after the war inherits an account rather than a prize."),
        (("industry", "document"), ("economy", "scales"), ("security", "industry"), ("navy", "medical"), ("scales", "economy"), ("economy", "peace")),
        (("Published operating contract", {"production_factory_efficiency_gain_factor": 0.025}, {"political_power_gain": -0.05}),
         ("State custody of the platforms", {"political_power_gain": 0.05}, {"army_org_factor": -0.01})),
        (("Fund a Crew Rotation", "Rotate and pay platform crews with evacuation plans in place.", "The public oil corporation", {"production_factory_efficiency_gain_factor": 0.03}),
         ("Audit the Revenue Account", "Reconcile production with the revenue paid into the platform account.", "The national audit office", {"political_power_gain": 0.08})),
        ("A Helicopter With No Flight Plan",
         "A helicopter lands on the northernmost platform without a flight plan. The men aboard say they represent the Eastern Faction and ask the crew chief to show them the control room. They are polite, armed and in no hurry. The crew chief radios the corporation's office for instructions.\n\nThe office can tell the crew to cooperate and publish what happened, so that every faction knows the platforms are a civilian workplace. Or it can tell the crew to delay, while the ministry tries to settle the matter with the visitors' commanders out of public view.",
         ("Tell the crew to cooperate and publish the visit.", "Delay and settle it out of public view.")),
        ("The Account and the Register",
         "The final review sets two documents side by side: the revenue account, with every payment in and out, and the crew register, with every person who worked a shift on the platforms. Both are complete. Neither says who controls the northeast today.\n\nThe crew chief who radioed for instructions is in the register. The visit is in the account, as a week of lost production.")),
    Branch("EVA", "chandelier", (), STARTED,
        ("The Unfinished Railgun", "Seal the Project", "Keep the Research Team Together",
         "Protect the Records and the People", "Review the Custody Year", "Custody, Not a Weapon"),
        ("The Chandelier, the railgun built to destroy fragments of Ulysses, was unfinished when the asteroid arrived. Its site, its records and the engineers who know how it works are now in a country at war with itself. The government will record what exists, who can reach it and who wants it.",
         "The project will be sealed: records archived, components inventoried and the site placed under a neutral caretaker staff. Sealing reduces the risk that a faction seizes it, and it disperses the team that understands it.",
         "The research team will be kept together and paid, with its records intact, under the ministry's protection. Continuity preserves expertise the country may need, at the price of keeping a valuable target in one place.",
         "Engineers and their families need protection from every faction that might want their knowledge. The ministry will keep them on a register, with relocation plans and a guarantee that nobody works on the project under duress.",
         "The review examines one funded custody year: records kept, staff protected and the site untouched. It does not measure progress toward completion, because completion is not the purpose of custody.",
         "The settlement fixes the Chandelier's custody arrangements and the protection of its people. It neither completes nor arms the project. Any later decision about it will be made by a government with the records in hand."),
        (("science", "document"), ("gate", "document"), ("science", "training"), ("shelter", "science"), ("scales", "science"), ("science", "peace")),
        (("Sealed project", {"stability_factor": 0.02}, {"research_speed_factor": -0.01}),
         ("Retained research team", {"research_speed_factor": 0.015}, {"political_power_gain": -0.05})),
        (("Fund the Caretaker Staff", "Keep a caretaker staff at the site and the records archived.", "The ministry of science", {"stability_factor": 0.02}),
         ("Protect the Engineers", "Keep engineers and their families on a protected register with relocation plans.", "The internal security service", {"research_speed_factor": 0.015})),
        ("A Request for the Blueprints",
         "A colonel with a letter from the capital's command asks the site's caretaker for a complete set of the Chandelier's blueprints. The letter is signed and stamped; it does not say why. The caretaker knows that two other factions have made similar requests, less politely.\n\nThe ministry can publish the request and its refusal, making clear that the records are in custody and will stay there. Or it can answer each request privately, buying time without announcing to every faction that the blueprints are worth asking for.",
         ("Publish the request and the refusal.", "Answer each request privately.")),
        ("The Inventory Is Unchanged",
         "The final custody review is short. The inventory taken at the start matches the inventory taken at the end. The engineers on the register are all accounted for; two have moved abroad with the ministry's help. The site has had visitors, and none of them left with anything.\n\nThe review is careful about what it does not claim. The railgun is unfinished, as it was when Ulysses arrived. What happens to it next is a decision for a government that does not yet exist.")),
    Branch("EVA", "talks", (), WAR + " date > 2009.12.31",
        ("Talk Across the Lines", "A Negotiated Settlement", "Wait for the Decisive Battle",
         "Prepare for Whoever Governs Next", "Review the Contacts", "A Peace the Factions Can Sign"),
        ("After years of fighting, every faction knows the cost of the war and none can say how it ends. Officials with contacts across the lines will record who is willing to talk, about what, and who would have to agree before any agreement could hold.",
         "The government will pursue a negotiated settlement: local ceasefires first, then talks between the factions' representatives with outside observers. Negotiation can end the war sooner and leave fewer wounds, and it requires concessions that hardliners on every side will call betrayal.",
         "The government will wait for the war to be decided on the battlefield and prepare to govern afterwards. Waiting avoids concessions and keeps options open, and every month it lasts is paid for by the cities and the people in them.",
         "Whoever governs after the war will need lists of prisoners, missing persons and damaged property, and officials more than one faction can trust. The ministries will prepare those lists now.",
         "The review examines a funded period of contacts across the lines: which channels stayed open, which ceasefires held and which talks produced anything written down.",
         "The settlement keeps the chosen course and the records prepared for the peace. It cannot end the war by itself. It makes sure that when the war ends, by agreement or by force, the country is not starting from nothing."),
        (("diplomacy", "communications"), ("diplomacy", "peace"), ("command", "security"), ("document", "shelter"), ("scales", "diplomacy"), ("peace", "assembly")),
        (("Negotiated settlement course", {"stability_factor": 0.03}, {"army_org_factor": -0.02}),
         ("Waiting for the decisive battle", {"army_org_factor": 0.03}, {"stability_factor": -0.02})),
        (("Keep the Channels Open", "Fund intermediaries and local ceasefire contacts across the lines.", "The ministry of foreign affairs", {"political_power_gain": 0.08}),
         ("Compile the Peace Lists", "Compile lists of prisoners, missing persons and damaged property.", "The ministry of justice", {"stability_factor": 0.025})),
        ("A Ceasefire in One Valley",
         "In a valley between two front lines, local commanders have agreed to stop shooting for the harvest. Nobody in the capital authorised it, and nobody in the Eastern Faction's command has denied it. The farmers are bringing in the crop. An official who knows both commanders asks the ministry what to do.\n\nThe ministry can publicise the ceasefire as proof that talks can work, risking orders from either side to end it. Or it can protect it quietly, telling no one beyond the officials who need to know, and hope it lasts long enough to become a habit.",
         ("Publicise the valley ceasefire.", "Protect it quietly.")),
        ("Lists for the Peace",
         "The final review contains the lists: prisoners by name and location, missing persons by last known whereabouts, property by district and condition. They are incomplete, and the review says where. They are also the only lists of their kind that every faction has agreed to read.\n\nThe valley ceasefire is in the record. It lasted through two harvests.")),
    Branch("EMM", "aid", (), STARTED,
        ("Conditions for Reconstruction Aid", "Conditional Aid With Monitors", "Withhold Aid Until the Fighting Ends",
         "Reach Civilians, Not Commanders", "Review an Aid Year", "Aid With Terms That Hold"),
        ("Emmeria has given Estovakia reconstruction aid since the asteroid, through programmes that were frozen and reformed more than once. With the Lyes Faction in the capital, the cabinet must decide what aid it will still give, to whom, and on what terms.",
         "Aid will continue under strict conditions: independent monitors, delivery to named civilian projects and suspension if any of it is used to suppress opposition. Conditional aid keeps a channel open, and it can be accused of funding the government it is meant to restrain.",
         "Aid to the government in the capital will stop until the fighting ends, while emergency relief continues through international agencies. Withholding aid avoids funding repression, and it leaves Emmeria with little influence over what happens next.",
         "Whatever the policy, the aid that does go must reach civilians: clinics, water systems and schools, not ministries that can redirect it. The aid office will keep a delivery register for every shipment.",
         "The review examines one funded aid year: shipments delivered, projects completed and any diversion found by the monitors. It records failures as carefully as successes.",
         "The settlement fixes the terms on which Emmeria gives aid to a neighbour at war with itself. It keeps the chosen policy and its costs, and it gives any future government in Estovakia a clear account of what Emmeria offered and why."),
        (("economy", "diplomacy"), ("scales", "economy"), ("gate", "economy"), ("medical", "logistics"), ("document", "scales"), ("diplomacy", "peace")),
        (("Conditional aid with monitors", {"stability_factor": 0.02}, {"political_power_gain": -0.05}),
         ("Aid withheld until the fighting ends", {"political_power_gain": 0.05}, {"stability_factor": -0.01})),
        (("Fund the Aid Monitors", "Pay independent monitors to inspect aid deliveries in Estovakia.", "The Emmerian aid office", {"political_power_gain": 0.08}),
         ("Ship Civilian Relief", "Deliver clinic, water and school supplies to named projects.", "The Emmerian aid office", {"stability_factor": 0.025})),
        ("The Monitor's Report",
         "An aid monitor's report arrives with photographs of a warehouse in an Estovakian city. The flour in it was shipped for a school feeding programme. The soldiers guarding it belong to the capital's command, and the school has received nothing for a month.\n\nThe aid office can publish the report, which will force the cabinet to suspend the programme. Or it can raise the matter privately with the capital, hoping to get the flour to the school without ending the only channel Emmeria still has.",
         ("Publish the monitor's report.", "Raise it privately with the capital.")),
        ("An Account of What Emmeria Gave",
         "The final review lists every programme Emmeria funded in Estovakia during the war, what each delivered and how each ended. Some ended because the fighting reached them. Some ended because the monitors found the aid going to the wrong people. The review does not soften either.\n\nThe school in the photographs is in the list. Its feeding programme resumed, then stopped again, and the record says why both times.")),
    Branch("EMM", "border", (), WAR,
        ("The Eastern Border", "Open Reception Centres", "Controlled Crossing Points",
         "Register Every Arrival", "Review a Season at the Border", "A Border That Can Stay Open"),
        ("The fighting in Estovakia has sent people toward Emmeria's eastern border: families fleeing the cities, deserters and people who cannot say which they are. The interior ministry will record who is arriving, where they are crossing and what the border towns can absorb.",
         "Reception centres will take in anyone fleeing the fighting, with shelter, food and medical care near the border. Open reception saves lives and honours Emmeria's commitments, and it places a heavy, visible burden on the border towns.",
         "Arrivals will cross only at controlled points, with screening and limits set by the capacity of each centre. Control keeps the border orderly and reassures the towns, and it leaves people waiting on the other side of a war.",
         "Every arrival will be registered with a name, a point of origin and any family members missing. The register protects people from disappearing and helps families find each other, whatever the reception policy.",
         "The review examines one funded season at the border: arrivals received, families reunited and centres that coped or did not. It counts what happened at the border, not statements about it.",
         "The settlement keeps the chosen border policy and the register. It makes no claim on Estovakian territory and closes no road permanently. It gives Emmeria a way to receive people from a neighbour's war without improvising each time."),
        (("refugees", "gate"), ("shelter", "medical"), ("gate", "security"), ("document", "refugees"), ("scales", "gate"), ("refugees", "peace")),
        (("Open reception centres", {"stability_factor": 0.02}, {"consumer_goods_factor": 0.01}),
         ("Controlled crossing points", {"army_org_factor": 0.02}, {"political_power_gain": -0.05})),
        (("Staff the Reception Centres", "Run shelter, food and medical care at the border centres.", "The interior ministry", {"stability_factor": 0.025}),
         ("Run the Arrivals Register", "Register arrivals and trace missing family members.", "The border registry office", {"political_power_gain": 0.08})),
        ("A Bus With No Papers",
         "A bus reaches the border crossing at night with forty people aboard and no papers among them. The driver says they are from a city that has been shelled for weeks; two passengers say they are soldiers who left their unit. The border officer has room for twenty in the reception centre and instructions that do not cover this.\n\nThe interior ministry can admit everyone and publish the case, pressing the cabinet for more capacity. Or it can admit the families, hold the soldiers for screening, and deal with the case without a public argument about the border.",
         ("Admit everyone and publish the case.", "Admit the families and screen the soldiers quietly.")),
        ("The Register at the Border",
         "The final review is built from the register: names, dates, points of origin and the families who found each other through it. The bus that arrived at night is there, all forty people, with what became of each.\n\nThe border towns carried more than their share. The review says so, and names what the cabinet did and did not send them.")),
    Branch("EMM", "initiative", (), "has_global_flag = ac_ecw_anea_initiative_on_hold",
        ("The Suspended Initiative", "Preserve the Initiative's Records", "Close the Preparatory Offices",
         "Keep the Technical Contacts", "Review the Suspension", "An Initiative That Can Resume"),
        ("The Republic of Anea Initiative, prepared since 2004 to unify the continent, has been put on hold because of the strife in Estovakia. Its offices, files and staff remain. The cabinet will decide what to keep while the initiative waits.",
         "The initiative's records, agreements and technical studies will be preserved by a small staff, ready for the day it can resume. Preservation keeps years of work from being lost, and it costs money for an institution with nothing to do.",
         "The preparatory offices will close and their staff return to their ministries, with the files archived. Closing saves money and ends an awkward institution, and it means starting again from the archive if the initiative revives.",
         "Engineers and officials on both sides of the border built working relationships while preparing the initiative. Those contacts can keep water, power and transport links running between the two countries, whatever happens to the initiative itself.",
         "The review examines one funded period under the chosen arrangement: what was preserved, what was lost and which contacts still answer.",
         "The settlement fixes what remains of the initiative while it is suspended. It creates no common government and claims no territory. It makes sure that a decision to resume, if one comes, can be made with the initiative's work still in hand."),
        (("document", "diplomacy"), ("document", "science"), ("gate", "document"), ("communications", "bridge"), ("scales", "document"), ("bridge", "peace")),
        (("Preserved initiative records", {"research_speed_factor": 0.01}, {"political_power_gain": -0.04}),
         ("Closed preparatory offices", {"political_power_gain": 0.04}, {"stability_factor": -0.01})),
        (("Fund the Records Staff", "Keep a small staff preserving the initiative's files and studies.", "The preparatory agency's remaining office", {"research_speed_factor": 0.015}),
         ("Run the Technical Liaison", "Keep cross-border engineering contacts working on shared services.", "The ministry of infrastructure", {"production_speed_infrastructure_factor": 0.035})),
        ("Boxes in the Corridor",
         "The preparatory agency's corridor is lined with boxes: treaty drafts, survey maps, the minutes of hundreds of meetings. The building's lease ends next month. A junior official has made an index of everything, on her own time, and asks the ministry what happens to it.\n\nThe ministry can publish the index, so that anyone in either country can see what the initiative produced and argue for keeping it. Or it can transfer the boxes quietly to a government archive, where they will be safe and largely forgotten.",
         ("Publish the index.", "Transfer the boxes quietly.")),
        ("The Index",
         "The final review attaches the junior official's index, now complete. It lists what was preserved, what was archived and what was lost when the offices moved. The technical contacts are listed too: the engineers on both sides who still answer each other's calls.\n\nThe initiative remains suspended. Its work does not.")),
)

OPENINGS = {
    "EVA": ("A Capital Under New Command",
        "The Lyes Faction holds the capital. Its new command has issued instructions to every ministry; some are routine, some are not, and a few contradict each other. The ministers who remain at their desks must decide how to govern under a command much of the country rejects, and how much of that decision to make in public.\n\nOutside the capital, other factions are organising. Nobody in the cabinet room believes this will end quickly.",
        ("Open the cabinet's decisions to public questions.", "Begin with a protected cabinet docket.")),
    "EMM": ("News from Across the Border",
        "Reports from Estovakia describe a capital seized by the Lyes Faction and cities that refuse to accept it. Emmeria's aid programmes, its border towns and the Republic of Anea Initiative all depend on a neighbour that may be about to fight itself.\n\nThe cabinet must decide what Emmeria will do, and how openly.",
        ("Open the cabinet's response to public questions.", "Begin with a protected cabinet docket.")),
}
FINALS = {
    "EVA": ("A Country That Kept Its Records",
        "The cabinet's final review of the war years lists what the ministries kept running, what they lost and what they refused to do. It does not decide who was right. It gives whatever government now governs Estovakia a civil service that remembers the war accurately.\n\n[EVA_ecw_outcome_text]",
        {"stability_factor": 0.02}),
    "EMM": ("A Neighbour's War, Accounted For",
        "The final account of the war years sets out what Emmeria gave, received and refused: aid, refugees, border crossings and a suspended initiative. Some of its choices worked and some did not. The account names both.",
        {"political_power_gain": 0.05}),
}

WAVE = Wave(
    prefix=S, infix="ecw", label="The Estovakian Civil War", source="tools/content_waves",
    countries={"EVA": "Estovakia", "EMM": "Emmeria"},
    eligible="date > 2007.4.2",
    branches=BRANCHES,
    layout={"EVA_capital": (3, 31), "EVA_cities": (9, 31), "EVA_oil": (15, 31), "EVA_chandelier": (21, 31), "EVA_talks": (27, 31),
            "EMM_aid": (6, 31), "EMM_border": (12, 31), "EMM_initiative": (18, 31)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"EVA": "has_country_flag = EVA_ecw_talks_settlement_done", "EMM": "has_country_flag = EMM_ecw_aid_settlement_done"},
    themes={"EVA": ("security", "assembly"), "EMM": ("diplomacy", "refugees")},
    weekly_extra={"EVA": "ac_ecw_owner_weekly = yes\n"},
    event_base=100,
)

# Owner -------------------------------------------------------------------
LATE_LIMIT = "2008.4.3"   # a first observation a year after the seizure never replays it
TIERS = (("luf_holds_capital", 59.99, {"stability_factor": -0.05, "political_power_gain": -0.05, "consumer_goods_factor": 0.02}),
         ("divided_country", 29.99, {"stability_factor": -0.08, "political_power_gain": -0.1, "production_factory_efficiency_gain_factor": -0.03}),
         ("luf_in_retreat", 0, {"stability_factor": -0.04, "political_power_gain": -0.05}))


def owner():
    """Tagless Estovakian civil-war owner: two Estovakian variables, idea tiers, dated stages."""
    effects, triggers, loc, ideas, events = {}, {}, {}, [], []

    def idea(ident, title, description, values):
        loc[ident] = title
        loc[ident + "_desc"] = description
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" +
                           block("modifier", "\n".join(f"{k} = {v}" for k, v in values.items()))))

    def news(number, title, desc, option, picture):
        ident = f"{S}.{number}"
        loc.update({ident + ".t": title, ident + ".d": desc, ident + ".a": option})
        events.append(block("news_event", f"id = {ident}\ntitle = {ident}.t\ndesc = {ident}.d\npicture = GFX_{picture}\nis_triggered_only = yes\nmajor = yes\ntrigger = {{ always = yes }}\n" +
                            block("option", f"name = {ident}.a")))

    def fire(number):
        return f"news_event = {{ id = {S}.{number} days = 1 }}\n"

    def change(variable, amount):
        verb = "add_to_variable" if amount > 0 else "subtract_from_variable"
        return f"{verb} = {{ {variable} = {abs(amount)} }}\nclamp_variable = {{ var = {variable} min = 0 max = 100 }}\n"

    triggers["ac_ecw_owner_eligible"] = "tag = EVA original_tag = EVA any_owned_state = { always = yes }"
    triggers["ac_ecw_running"] = f"{STARTED} NOT = {{ has_global_flag = ac_ecw_ended }} NOT = {{ has_global_flag = ac_ecw_closed }}"
    triggers["ac_ecw_emm_can_answer"] = "country_exists = EMM EMM = { has_capitulated = no }"
    triggers["ac_ecw_settlement_earned"] = (
        "has_country_flag = EVA_ecw_talks_policy_a_done has_country_flag = EVA_ecw_capital_policy_a_done "
        "OR = { has_global_flag = ac_ecw_emm_aid_conditional check_variable = { ac_anea_recovery > 39 } } "
        "check_variable = { ac_ecw_eastern_strength > 19 }")

    remove = "".join(f"remove_ideas = ac_ecw_{name}\n" for name, _, _ in TIERS)
    effects["ac_ecw_update_tier"] = (
        guard("ac_ecw_running = yes check_variable = { ac_ecw_luf_authority > 59.99 }",
              guard("NOT = { has_idea = ac_ecw_luf_holds_capital }", remove + "add_ideas = ac_ecw_luf_holds_capital")) +
        block("else_if", block("limit", "ac_ecw_running = yes check_variable = { ac_ecw_luf_authority > 29.99 }") +
              guard("NOT = { has_idea = ac_ecw_divided_country }", remove + "add_ideas = ac_ecw_divided_country")) +
        block("else_if", block("limit", "ac_ecw_running = yes") +
              guard("NOT = { has_idea = ac_ecw_luf_in_retreat }", remove + "add_ideas = ac_ecw_luf_in_retreat")) +
        block("else", remove.rstrip()))
    for name, authority, eastern in (("accommodation", -5, -3), ("accommodation_small", -2, -1),
                                     ("suppression", 8, 5), ("suppression_small", 3, 3)):
        effects[f"ac_ecw_shift_{name}"] = guard("ac_ecw_running = yes tag = EVA original_tag = EVA",
            change("ac_ecw_luf_authority", authority) + change("ac_ecw_eastern_strength", eastern) + "ac_ecw_update_tier = yes")
    effects["ac_ecw_luf_loses_aid"] = guard("ac_ecw_running = yes tag = EVA original_tag = EVA",
        change("ac_ecw_luf_authority", -5) + "ac_ecw_update_tier = yes")
    effects["ac_ecw_begin"] = ("set_global_flag = ac_ecw_capital_seized\nset_variable = { ac_ecw_luf_authority = 75 }\n"
                               "set_variable = { ac_ecw_eastern_strength = 20 }\nac_ecw_update_tier = yes\n" + fire(1))
    effects["ac_ecw_end_historical"] = guard("ac_ecw_running = yes",
        "set_global_flag = ac_ecw_ended\nset_global_flag = ac_ecw_eastern_victory\nset_global_flag = ac_ecw_historical_end\n"
        "ac_ecw_update_tier = yes\nadd_timed_idea = { idea = ac_ecw_civil_war_ended days = 365 }\n" + fire(9))
    effects["ac_ecw_end_late"] = guard("ac_ecw_running = yes",
        "set_global_flag = ac_ecw_ended\nset_global_flag = ac_ecw_eastern_victory\n"
        "ac_ecw_update_tier = yes\nadd_timed_idea = { idea = ac_ecw_civil_war_ended days = 365 }\n" + fire(13))
    effects["ac_ecw_negotiate"] = guard("ac_ecw_running = yes tag = EVA original_tag = EVA ac_ecw_settlement_earned = yes",
        "add_political_power = -50\nset_global_flag = ac_ecw_ended\nset_global_flag = ac_ecw_negotiated\n"
        "ac_ecw_update_tier = yes\nadd_timed_idea = { idea = ac_ecw_negotiated_peace days = 365 }\n" + fire(14))
    effects["ac_ecw_close"] = guard(f"{STARTED} NOT = {{ has_global_flag = ac_ecw_ended }} NOT = {{ has_global_flag = ac_ecw_closed }}",
        "set_global_flag = ac_ecw_closed\n" + guard("country_exists = EVA", "EVA = { " + remove.replace("\n", " ") + "}"))
    emm_luf = guard("ac_ecw_emm_can_answer = yes", "EMM = { country_event = { id = ac_ecw.5 days = 1 } }") + block("else", "set_global_flag = ac_ecw_emm_aid_ended_luf")
    emm_all = guard("ac_ecw_emm_can_answer = yes", "EMM = { country_event = { id = ac_ecw.6 days = 1 } }") + block("else", "set_global_flag = ac_ecw_emm_aid_ended_all")
    stages = (
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_war_running } date > 2007.6.29",
              "set_global_flag = ac_ecw_war_running\n" + change("ac_ecw_luf_authority", -5) + "ac_ecw_update_tier = yes\n" + fire(2)) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_stage_oil } date > 2008.7.14",
              "set_global_flag = ac_ecw_stage_oil\n" +
              guard("has_country_flag = EVA_ecw_oil_policy_b_done", change("ac_ecw_eastern_strength", 5)) +
              block("else", change("ac_ecw_eastern_strength", 15) + change("ac_ecw_luf_authority", -5)) +
              "ac_ecw_update_tier = yes\n" + fire(3)) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_anea_initiative_on_hold } date > 2008.10.22",
              "set_global_flag = ac_ecw_anea_initiative_on_hold\n" +
              guard("OR = { has_global_flag = ac_anea_bureau has_global_flag = ac_anea_accord }", fire(4))) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_stage_aid_luf } date > 2010.2.18",
              "set_global_flag = ac_ecw_stage_aid_luf\n" + emm_luf) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_stage_aid_all } date > 2011.5.8",
              "set_global_flag = ac_ecw_stage_aid_all\n" + emm_all) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_stage_offensive } date > 2013.1.14",
              "set_global_flag = ac_ecw_stage_offensive\n" +
              guard("check_variable = { ac_ecw_eastern_strength > 29.99 }", change("ac_ecw_luf_authority", -40) + "ac_ecw_update_tier = yes\n" + fire(7)) +
              block("else", "set_global_flag = ac_ecw_prolonged\n" + fire(8))) +
        guard("ac_ecw_running = yes NOT = { has_global_flag = ac_ecw_prolonged } has_global_flag = ac_ecw_stage_offensive date > 2013.10.28",
              guard("check_variable = { ac_ecw_luf_authority < 40 }", "ac_ecw_end_historical = yes") +
              block("else", "set_global_flag = ac_ecw_prolonged\n" + fire(8))) +
        guard("ac_ecw_running = yes has_global_flag = ac_ecw_prolonged",
              change("ac_ecw_luf_authority", -0.1) + change("ac_ecw_eastern_strength", 0.05) +
              guard("OR = { has_idea = EVA_ecw_capital_policy_b_spirit has_idea = EVA_ecw_capital_policy_b_spirit_settled }", change("ac_ecw_luf_authority", 0.05)) +
              "ac_ecw_update_tier = yes\n" +
              guard("check_variable = { ac_ecw_luf_authority < 20 }", "ac_ecw_end_late = yes")))
    aftermath = (
        guard("has_global_flag = ac_ecw_historical_end NOT = { has_global_flag = ac_ecw_after_arensky } date > 2013.11.24 date < 2014.11.25",
              "set_global_flag = ac_ecw_after_arensky\n" + fire(10)) +
        guard("has_global_flag = ac_ecw_historical_end NOT = { has_global_flag = ac_ecw_after_koznick } date > 2014.2.2 date < 2015.2.3",
              "set_global_flag = ac_ecw_after_koznick\n" + fire(11)) +
        guard("has_global_flag = ac_ecw_historical_end NOT = { has_global_flag = ac_ecw_after_vistoc } date > 2014.2.3 date < 2015.2.4",
              "set_global_flag = ac_ecw_after_vistoc\n" + fire(12)))
    effects["ac_ecw_owner_weekly"] = (
        guard(f"ac_ecw_owner_eligible = yes NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_ecw_closed }} date > 2007.4.2",
              guard(f"date < {LATE_LIMIT}", "ac_ecw_begin = yes") +
              block("else", "set_global_flag = ac_ecw_closed\nset_global_flag = ac_ecw_late_start_skipped")) +
        guard("ac_ecw_running = yes ac_ecw_owner_eligible = no", "ac_ecw_close = yes") +
        guard("ac_ecw_owner_eligible = yes", stages + aftermath))

    idea("ac_ecw_luf_holds_capital", "Civil War: The LUF Holds the Capital",
         "The Lyes United Front controls the capital and its ministries. LUF authority: [?ac_ecw_luf_authority|0]/100; Eastern Faction strength: [?ac_ecw_eastern_strength|0]/100. Values are provisional gameplay.", TIERS[0][2])
    idea("ac_ecw_divided_country", "Civil War: A Divided Country",
         "No faction governs the whole country. LUF authority: [?ac_ecw_luf_authority|0]/100; Eastern Faction strength: [?ac_ecw_eastern_strength|0]/100. Values are provisional gameplay.", TIERS[1][2])
    idea("ac_ecw_luf_in_retreat", "Civil War: The LUF in Retreat",
         "The Lyes United Front has lost most of the country. LUF authority: [?ac_ecw_luf_authority|0]/100; Eastern Faction strength: [?ac_ecw_eastern_strength|0]/100. Values are provisional gameplay.", TIERS[2][2])
    idea("ac_ecw_civil_war_ended", "After the Civil War",
         "The fighting is over and the country begins to count what it lost. Relief steadies the public mood; reconstruction absorbs the government's attention for a year.",
         {"stability_factor": 0.03, "political_power_gain": -0.05})
    idea("ac_ecw_negotiated_peace", "A Negotiated Peace",
         "The factions signed a settlement before the war was decided by force. The peace is broader than a victory would have been, and keeping every signatory inside it costs political attention.",
         {"stability_factor": 0.05, "political_power_gain": -0.08})

    news(1, "The Lyes Faction Seizes the Capital",
         "The Lyes Faction, later known as the Lyes United Front, has seized control of the Estovakian capital (ACES Chronicle, 2007 / 04.03).\n\nThe ministries now answer to a command that much of the country does not accept. In this campaign the country tag, borders and government are unchanged; the struggle is tracked as authority and strength, which are provisional gameplay.",
         "The capital is under new command.", "ac_ecw_news_fracture")
    news(2, "The Estovakian Civil War Begins",
         "The Lyes United Front has begun to suppress the cities that resist its rule, and other factions have risen against it. The Estovakian Civil War has begun (ACES Chronicle, 2007 / 06.30).",
         "A country at war with itself.", "ac_ecw_news_fracture")
    news(3, "The Northeastern Platforms Change Hands",
         "Estovakia's Eastern Faction has taken and restored the oil platforms in the northeast of the country that were held by a public corporation (ACES Chronicle, 2008 / 07.15).\n\nHow much the platforms strengthen the faction in this campaign depends on whether the government took them into state custody beforehand.",
         "The northeast has a new paymaster.", "ac_ecw_news_platforms")
    news(4, "The Anea Initiative Is Put on Hold",
         "The Republic of Anea Initiative has been put on hold because of the internal strife in Estovakia (ACES Chronicle, 2008 / 10.23).\n\nThe initiative's existing bureau records are not altered by this event; Emmeria decides what to keep while it waits.",
         "The initiative waits.", "ac_ecw_news_initiative")
    news(7, "The Eastern Faction Breaks the LUF",
         "The Eastern Faction and the Lyes United Front have clashed. The LUF's superior numbers were overwhelmed by the Eastern Faction's new weapons and elite aviation units, and it lost about 80 percent of its territory in a single week (ACES Chronicle, 2013 / 01.15).\n\nNo territory changes hands on the map; the loss is tracked as LUF authority.",
         "The balance has turned.", "ac_ecw_news_offensive")
    news(8, "The Civil War Continues",
         "The decisive defeat that the historical record places in 2013 has not happened in this campaign: the Eastern Faction is too weak, or the LUF still holds too much of the country. The war goes on.\n\nThis is a provisional alternative. It ends when the LUF's authority collapses or the factions negotiate a settlement.",
         "The fighting goes on.", "ac_ecw_news_offensive")
    news(9, "General Lyes Is Killed; the Civil War Ends",
         "The Lyes United Front fought on but suffered a major defeat near the border with Emmeria. General Lyes was killed and the Estovakian Civil War is over (ACES Chronicle, 2013 / 10.29).",
         "The war is over.", "ac_ecw_news_end")
    news(10, "An Attack on the Foreign Minister",
         "Estovakian Foreign Minister Isaac Arensky, a former air marshal of the Northern Highlands Faction, has been left unconscious by a sudden attack. A week later, fifteen former LUF soldiers are arrested for the crime (ACES Chronicle, 2013 / 11.25).",
         "The peace is fragile.", "ac_ecw_news_aftermath")
    news(11, "A New Foreign Minister",
         "The death of Foreign Minister Arensky, which occurred on 2 December 2013 and was withheld from the public, has been made public. Antonina Koznick, a former captain in the Eastern Faction navy, is named as his successor (ACES Chronicle, 2013 / 12.02 and 2014 / 02.03).\n\nNo leader, advisor or portrait is created by this report.",
         "The government changes hands.", "ac_ecw_news_aftermath")
    news(12, "Former LUF Fighters Attack Relief Supplies",
         "An armed force of former LUF members has attacked a temporary storage facility for relief supplies in the western Estovakian city of Vistoc (ACES Chronicle, 2014 / 02.04).",
         "The war leaves a long shadow.", "ac_ecw_news_aftermath")
    news(13, "The LUF Collapses",
         "The Lyes United Front's hold on the country has collapsed after a war that lasted longer than the historical record. The fighting is over.\n\nThis ending belongs to a provisional alternative route; the historical war ended on 29 October 2013.",
         "The war is over at last.", "ac_ecw_news_end")
    news(14, "A Negotiated Settlement in Estovakia",
         "Estovakia's factions have signed a negotiated settlement, ending the civil war before it was decided on the battlefield.\n\nThis is an earned alternative to the historical record, in which General Lyes was killed and the war ended on 29 October 2013. It required an accommodating government, a negotiated course and outside support.",
         "Peace by agreement.", "ac_ecw_news_end")

    def emm_event(number, title, desc, options):
        ident = f"{S}.{number}"
        loc.update({ident + ".t": title, ident + ".d": desc})
        body = f"id = {ident}\ntitle = {ident}.t\ndesc = {ident}.d\npicture = GFX_ac_ecw_event_emm_national\nis_triggered_only = yes\ntrigger = {{ tag = EMM original_tag = EMM }}\n"
        for letter, (label, condition, ai, action) in zip("ab", options):
            loc[f"{ident}.{letter}"] = label
            body += block("option", f"name = {ident}.{letter}\n" + (block("trigger", condition) if condition else "") + f"ai_chance = {{ factor = {ai} }}\n" + action)
        events.append(block("country_event", body))

    emm_event(5, "Aid for the LUF's Reconstruction Programme",
              "The ACES Chronicle records that Emmeria ended aid for the LUF's reconstruction programme because the LUF suppressed all opposition (2010 / 02.19).\n\nIf the cabinet has built a monitored, conditional aid policy, it may instead keep a narrow channel open under strict terms. That choice is a provisional alternative.",
              (("End aid for the LUF's reconstruction programme.", "", 100,
                "set_global_flag = ac_ecw_emm_aid_ended_luf\n" + guard("country_exists = EVA", "EVA = { ac_ecw_luf_loses_aid = yes }")),
               ("Continue aid under monitors and strict conditions.", "has_country_flag = EMM_ecw_aid_policy_a_done", 0,
                "set_global_flag = ac_ecw_emm_aid_conditional\nadd_political_power = -25\n")))
    emm_event(6, "Reconstruction Aid to Estovakia",
              "The ACES Chronicle records that Emmeria ended aid for Estovakia's reconstruction (2011 / 05.09).\n\nA cabinet that kept a monitored channel open may preserve a humanitarian line instead. That choice is a provisional alternative.",
              (("End reconstruction aid to Estovakia.", "", 100, "set_global_flag = ac_ecw_emm_aid_ended_all\n"),
               ("Keep a humanitarian channel open.", "has_global_flag = ac_ecw_emm_aid_conditional", 0,
                "set_global_flag = ac_ecw_emm_channel_kept\nadd_political_power = -15\n")))

    loc.update({
        "EVA_ecw_negotiate": "Sign a Negotiated Settlement",
        "EVA_ecw_negotiate_desc": "End the civil war by agreement before it is decided by force. Requires the negotiated-settlement course, an accommodating government, and either Emmerian conditional aid or strong Anean recovery (40 or more), with an Eastern Faction able to sign (strength 20 or more). Costs 50 political power. This is an earned alternative to the historical end in 2013.",
        "EVA_ecw_outcome_negotiated": "The war ended in a negotiated settlement, an alternative to the historical record.",
        "EVA_ecw_outcome_historical": "The war ended as the historical record describes: General Lyes was killed on 29 October 2013.",
        "EVA_ecw_outcome_late": "The war ended late, when the LUF's hold collapsed, in a provisional alternative route.",
        "EVA_ecw_outcome_none": "The civil war's outcome has not yet been recorded.",
        "ac_ecw_owner_eligible": "Estovakia is a landowning country",
        "ac_ecw_running": "The Estovakian civil war owner is active",
        "ac_ecw_emm_can_answer": "Emmeria exists and has not capitulated",
        "ac_ecw_settlement_earned": "A negotiated settlement has been earned",
    })
    negotiate = block("EVA_ecw_negotiate",
        "icon = ac_ecw_EVA_ecw_negotiate\nallowed = { tag = EVA original_tag = EVA }\n"
        "visible = { ac_ecw_running = yes has_global_flag = ac_ecw_war_running has_country_flag = EVA_ecw_talks_policy_a_done }\n"
        "available = { ac_ecw_settlement_earned = yes political_power >= 50 }\ncost = 0\n" +
        block("complete_effect", "ac_ecw_negotiate = yes") + "ai_will_do = { base = 5 }\n")
    custom = block("defined_text", "name = EVA_ecw_outcome_text\n" +
        block("text", "trigger = { has_global_flag = ac_ecw_negotiated }\nlocalization_key = EVA_ecw_outcome_negotiated") +
        block("text", "trigger = { has_global_flag = ac_ecw_historical_end }\nlocalization_key = EVA_ecw_outcome_historical") +
        block("text", "trigger = { has_global_flag = ac_ecw_eastern_victory }\nlocalization_key = EVA_ecw_outcome_late") +
        block("text", "localization_key = EVA_ecw_outcome_none"))
    status = ("Lyes United Front authority: [?ac_ecw_luf_authority|0]/100. Eastern Faction strength: [?ac_ecw_eastern_strength|0]/100. "
              "Dates follow the ACES Chronicle; values and alternatives are provisional gameplay.\n\n")
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                decisions={"ac_ecw_eva_services": [negotiate]}, category_prefix={"EVA": status},
                interrupt_extra=guard("original_tag = EVA", "ac_ecw_close = yes"))


# Registry declarations ------------------------------------------------------
KEY = "B"
NAME = "estovakia"
IMPORTS = {"EVA": "ESTOVAKIAN FRACTURE", "EMM": "ESTOVAKIAN FRACTURE"}
LEDGER = "docs/CONTENT_WAVES_B_AUR.md"
SOURCES = {"official": ["Chronicle 2007 / 04.03 to 2014 / 02.04: the Estovakian civil war chain (see docs/STRANGEREAL_2006_2020_SOURCES.md)",
                        "Super Weapons, Chandelier: incomplete when Ulysses arrived"],
           "provisional_gameplay": "Authority and strength values, the negotiated settlement, the prolonged war, every focus, policy, service, dialogue and value"}
NEWS_ART = (("ac_ecw_news_fracture", ("security", "assembly"), "The Estovakian Civil War", "EVA"),
            ("ac_ecw_news_platforms", ("industry", "navy"), "The Northeastern Platforms", "EVA"),
            ("ac_ecw_news_initiative", ("document", "diplomacy"), "The Anea Initiative Is Put on Hold", "EMM"),
            ("ac_ecw_news_offensive", ("air", "command"), "The Turning of the War", "EVA"),
            ("ac_ecw_news_end", ("peace", "document"), "The End of the Civil War", "EVA"),
            ("ac_ecw_news_aftermath", ("document", "security"), "After the Civil War", "EVA"))
OWNER_ART = {"ac_ecw_luf_holds_capital": ("assembly", "security", "EVA"), "ac_ecw_divided_country": ("gate", "security", "EVA"),
             "ac_ecw_luf_in_retreat": ("security", "refugees", "EVA"), "ac_ecw_civil_war_ended": ("rebuild", "peace", "EVA"),
             "ac_ecw_negotiated_peace": ("diplomacy", "peace", "EVA")}
