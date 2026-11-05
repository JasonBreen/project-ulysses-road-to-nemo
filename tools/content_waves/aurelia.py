"""Aurelia's national foundation, 1991-2018 (Packages 1/5, 54 of 84 focuses).

Source layers
-------------
* The ACES Chronicle names Aurelia only for 2020 (the Aurelia-Leasath war); see
  docs/STRANGEREAL_2006_2020_SOURCES.md. Nothing from 2020 is used here: no
  Diego Navarro, Gleipnir, Gandr, Nevera Jammer, Aubrey Base, Archelon or
  other 2020 places. Those belong to the later 2019-2020 crisis lanes.
* Leasath's 2020 justification ("years of exploitation") is recorded only as
  Leasath's stated claim; the southern trade lane lets Aurelia review the terms
  without the game deciding whether the claim is fair.
* The Leasath civil war ended in 2019 "after 10 years of fighting"; its start
  about 2009 is derived. The response lane opens from 2010 as context only.
* Mod provenance: Aurelia's country history, office, world start and
  institution profile (services and technical capacity).
* Provisional gameplay: every focus, policy, service, dialogue and value. The
  policy completion flags (for example AUR_au_relations_policy_a_done) are the
  hand-off interface the later crisis lanes will read.
"""
from content_waves.framework import Branch, Wave, block

STAGE_1 = ("services", "trade", "airspace")
STAGE_2 = ("leasath_war", "finance", "exports")
STAGE_3 = ("relations", "readiness", "account")


def settled(keys):
    return tuple(f"AUR_au_{k}_settlement" for k in keys)


BRANCHES = (
    Branch("AUR", "services", (), "",
        ("A Register of Public Services", "Civilian Service Review", "Preparedness Staff First",
         "Technical Capacity Where It Is Needed", "Review a Service Year", "Services the Federation Can Sustain"),
        ("Aurelia's federal and provincial services have grown without a common record of what each office does or how many people it needs. The cabinet will register every service, its staff and its technical capacity before deciding where the next budget goes.",
         "Services will be reviewed by civilian panels that publish what each office delivers and what it costs. Civilian review improves trust and exposes waste, and it slows any reallocation that the panels have not examined.",
         "Preparedness staff will have first claim on engineers, communications specialists and logistics officers. Readiness for emergencies improves, and ordinary services wait longer for the specialists they share.",
         "Technical staff are scarce in the provinces and concentrated around the capital. The register will show where engineers and specialists are actually needed, and the ministries will move posts to match.",
         "The review examines one funded service year: what each office delivered, what it cost and where specialists were missing. Promised reforms do not count until they appear in the year's record.",
         "The settlement keeps the chosen balance between civilian review and preparedness. It gives the federation a register of its own capacity, which every later government will need."),
        (("document", "civil"), ("assembly", "scales"), ("command", "tools"), ("tools", "logistics"), ("scales", "document"), ("civil", "peace")),
        (("Civilian service review", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Preparedness staff first", {"production_speed_infrastructure_factor": 0.035}, {"consumer_goods_factor": 0.005})),
        (("Fund a Service Audit", "Audit federal and provincial services against the register.", "The federal audit office", {"political_power_gain": 0.08}),
         ("Post Specialists to the Provinces", "Move engineering and communications posts to where the register shows need.", "The federal civil service commission", {"production_speed_infrastructure_factor": 0.04})),
        ("Two Offices, One Engineer",
         "The register shows the same water engineer assigned to two provincial offices, three hundred kilometres apart. Both offices list her as their only qualified inspector. She has been driving between them every week for two years and has filed a complaint that nobody answered.\n\nThe audit office wants her case published as an example of what the register is for. The civil service commission would rather fix it quietly and move on, before every province starts counting the specialists it does not have.",
         ("Publish the engineer's case.", "Fix it quietly through the commission.")),
        ("A Federation That Knows Its Staff",
         "The final review is the register itself, now complete. Each service lists its staff, its specialists and the posts it cannot fill. The water engineer appears once, in one province, with a deputy in the other.\n\nThe register does not make Aurelia richer. It tells the federation where its people are, which is the first thing any emergency will ask.")),
    Branch("AUR", "trade", (), "",
        ("The Southern Trade Relationship", "Review the Terms Fairly", "Protect Aurelian Contracts",
         "Answer Complaints in Writing", "Review a Trading Year", "Trade on Terms Both Sides Can Read"),
        ("Aurelian firms hold contracts across the southern trade with Leasath: mines, ports, plantations and loans. Leasathian partners complain that the terms favour Aurelia. The cabinet will record every major contract, its terms and its revenue before deciding whether the complaints deserve an answer.",
         "A joint review will examine contract terms with Leasathian representatives and publish its findings, including any terms it finds unfair. Fairness reviews build goodwill and may cost Aurelian firms income they have come to rely on.",
         "Existing contracts will be defended as signed, with Aurelian courts as the forum for disputes. Protection keeps revenue and investor confidence, and it leaves the complaints unanswered, to be remembered by the people who made them.",
         "Every complaint from a Leasathian partner will receive a written answer that states the contract, the term in dispute and the government's position. Written answers will not settle every dispute, but they put a record where there was only resentment.",
         "The review examines one funded trading year: revenue, disputes raised and disputes resolved. It counts what changed in the contracts, not statements of good intentions.",
         "The settlement keeps the chosen approach to the southern trade and a written record of every dispute. It does not decide whether Leasath's complaints are just. It decides how Aurelia will answer them."),
        (("economy", "diplomacy"), ("scales", "diplomacy"), ("document", "security"), ("document", "communications"), ("economy", "scales"), ("diplomacy", "peace")),
        (("Fair-terms trade review", {"stability_factor": 0.02}, {"production_factory_efficiency_gain_factor": -0.01}),
         ("Protected Aurelian contracts", {"production_factory_efficiency_gain_factor": 0.025}, {"stability_factor": -0.01})),
        (("Fund the Joint Contract Panel", "Pay for a joint panel to examine disputed contract terms.", "The ministry of trade", {"political_power_gain": 0.08}),
         ("Run a Dispute Registry", "Record every complaint and the written answer it received.", "The commercial courts office", {"stability_factor": 0.025})),
        ("A Port Fee Nobody Explained",
         "A Leasathian trade delegation brings a single document to its meeting with the ministry: an invoice for port fees charged to its exporters, under a contract signed decades ago. The fees have risen every year. Nobody at the ministry can say what they pay for.\n\nThe ministry can publish the fee schedule and the contract, admitting it cannot justify parts of it. Or it can promise the delegation a confidential review, protecting the firms involved until the ministry knows what it is defending.",
         ("Publish the fee schedule and the contract.", "Offer a confidential review.")),
        ("A Register of Disputes",
         "The final review is a register of disputes: each contract, each complaint, each written answer and what became of it. Some terms were changed. Some were defended, and the review says why. The port fee is in the register, with a schedule that now explains what each charge pays for.\n\nThe register does not end the argument about the southern trade. It makes sure the argument is about facts both sides can read.")),
    Branch("AUR", "airspace", (), "",
        ("Weather and Air Warning", "A Civil Weather Service", "A Joint Air Warning Network",
         "Keep the Radar Sites Staffed", "Review a Season of Watch", "Eyes on the Sky in Every Season"),
        ("Aurelia's weather observation radars and air warning stations were built by different ministries for different purposes. The cabinet will record every site, what it watches and who staffs it, before deciding what the network is for.",
         "The radar network will serve the civil weather service first, with storm warnings, aviation forecasts and agricultural data published to the public. A civil network is popular and useful every day, and it gives the air force second claim on the sites.",
         "Weather and air warning sites will be joined into one network under a joint command, with civil forecasts as a secondary output. A joint network gives earlier warning of aircraft, and it makes every weather station a military installation in the eyes of its neighbours.",
         "Remote radar sites need technicians, power and supplies through the worst weather of the year. The service will keep a staffing rota and a supply plan for every site, so that no station goes dark because its relief failed to arrive.",
         "The review examines one funded season of watch: storms forecast, aircraft tracked and sites kept running. A site that went dark counts against the season, whatever the reason.",
         "The settlement keeps the chosen purpose for the network and a rota that keeps it staffed. It makes no claim beyond Aurelia's own airspace."),
        (("radar", "civil"), ("radar", "communications"), ("radar", "air"), ("tools", "radar"), ("scales", "radar"), ("radar", "peace")),
        (("Civil weather service", {"stability_factor": 0.02}, {"political_power_gain": -0.04}),
         ("Joint air warning network", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.005})),
        (("Staff the Remote Sites", "Fund technicians, power and supplies for remote radar sites through the year.", "The national weather service", {"production_speed_infrastructure_factor": 0.035}),
         ("Run a Warning Exercise", "Exercise storm and aircraft warnings across the network.", "The air warning directorate", {"army_org_factor": 0.025})),
        ("A Storm Warning and a Radar Track",
         "On the same night, a mountain radar site records a storm front moving toward the coast and an unidentified aircraft crossing the southern border. The duty technician has one telephone line and two people who need to be called first. She calls the weather service, then the air force, and files a report about the order.\n\nThe weather service wants the report published to show that civil warnings come first. The air directorate wants it kept internal, since a public account tells anyone watching how slowly an aircraft report travels.",
         ("Publish the night's report.", "Keep the report internal.")),
        ("A Network That Did Not Go Dark",
         "The final review lists every site, every season and every night a site went dark. There are fewer of those than there were. The mountain station has a second telephone line now, and the duty book says which call comes first.\n\nThe network watches the weather and the sky. It promises nothing about what either will bring.")),
    Branch("AUR", "leasath_war", settled(STAGE_1), "date > 2009.12.31",
        ("The War in Leasath", "Humanitarian Access First", "Protect Commercial Exposure",
         "Keep Aurelians Out of the Fighting", "Review a Year of the War", "A Neighbour's War, Answered"),
        ("Leasath is at war with itself, and the fighting reaches Aurelian contracts, ports and citizens across the south. The cabinet will record who is affected, which assets are exposed and what Aurelia can do without taking a side.",
         "Aurelia will press every Leasathian faction for humanitarian access, fund relief through neutral agencies and accept refugees at its southern ports. Access saves lives and builds goodwill in Leasath, and it costs money while Aurelian firms watch their contracts suffer.",
         "Aurelian firms and their staff in Leasath will be protected through evacuation plans, insurance guarantees and negotiations with whichever faction controls each site. Protection limits losses, and it can look to Leasathians like Aurelia caring more for its contracts than for their war.",
         "Aurelian citizens, contractors and security firms will be kept out of the fighting by law, with penalties for anyone who sells their services to a faction. Neutrality protects Aurelia from being drawn in, and it is hard to enforce on people who are already there.",
         "The review examines one funded year of the war's effect on Aurelia: relief delivered, citizens evacuated and contracts lost or kept. It does not judge the war; it judges Aurelia's response to it.",
         "The settlement keeps the chosen response and the neutrality law. Aurelia takes no side in Leasath's war. What Leasathians remember about Aurelia's choices will outlast the fighting."),
        (("refugees", "medical"), ("medical", "diplomacy"), ("economy", "security"), ("gate", "document"), ("scales", "refugees"), ("peace", "diplomacy")),
        (("Humanitarian access first", {"stability_factor": 0.02}, {"political_power_gain": -0.05}),
         ("Protected commercial exposure", {"production_factory_efficiency_gain_factor": 0.025}, {"stability_factor": -0.01})),
        (("Fund Neutral Relief", "Fund neutral agencies delivering relief inside Leasath.", "The ministry of foreign affairs", {"stability_factor": 0.025}),
         ("Run an Evacuation Rota", "Keep evacuation plans and transport ready for Aurelians in Leasath.", "The consular service", {"political_power_gain": 0.08})),
        ("A Contractor's Offer",
         "An Aurelian security contractor has been offered a lucrative contract to guard a mine for one of Leasath's factions. The firm asks the ministry whether this breaks the neutrality rules; its lawyers think it does not, because the mine is Aurelian-owned. The faction has made clear what the guards would be expected to do if anyone approached the mine.\n\nThe ministry can publish its ruling, warning every firm in Leasath where the line is. Or it can answer privately, avoiding a public argument with an influential firm while it decides what the law should say.",
         ("Publish the ruling.", "Answer the firm privately.")),
        ("Neutral, and on the Record",
         "The final review lists relief delivered, citizens evacuated and contracts lost. It also lists every neutrality ruling and every firm that tested it. The security contractor is there, with the ruling and what the firm did next.\n\nAurelia did not end Leasath's war and did not take a side in it. The record shows what it did instead.")),
    Branch("AUR", "finance", settled(STAGE_1), "date > 2005.12.31",
        ("Development Finance", "A Public Investment Bank", "Private Capital Guarantees",
         "Finance Where the Register Shows Need", "Review the Lending Year", "Investment That Outlasts a Budget"),
        ("Provinces, ports and industries all want investment, and the federal budget cannot pay for all of it. The treasury will record what is needed, what is already funded and what private capital would finance if the risks were shared.",
         "A public investment bank will lend for infrastructure and industry on published terms, with the federation carrying the risk. Public lending builds where private capital will not, and it ties up federal credit for years.",
         "The federation will guarantee private loans for approved projects instead of lending itself. Guarantees draw in private money at low cost to the budget, and they leave the federation responsible for projects it does not control.",
         "Lending will follow the services register and the provinces' own lists, not the loudest lobby. Projects will be ranked by need and published with the ranking.",
         "The review examines one funded lending year: projects financed, projects completed and loans in trouble. Announcements do not count until the work is done.",
         "The settlement keeps the chosen instrument and the ranking that guides it. It gives the federation a way to invest that does not depend on a single year's budget."),
        (("economy", "industry"), ("economy", "assembly"), ("economy", "scales"), ("document", "industry"), ("scales", "economy"), ("industry", "peace")),
        (("Public investment bank", {"production_speed_infrastructure_factor": 0.04}, {"political_power_gain": -0.05}),
         ("Private capital guarantees", {"production_factory_efficiency_gain_factor": 0.025}, {"stability_factor": -0.01})),
        (("Fund a Lending Round", "Finance a ranked round of infrastructure and industry projects.", "The federal treasury", {"production_speed_infrastructure_factor": 0.04}),
         ("Audit the Loan Book", "Review every loan and guarantee against the projects they paid for.", "The federal audit office", {"political_power_gain": 0.08})),
        ("A Bridge on the Ranking",
         "The ranking places a provincial bridge above a new terminal at the capital's airport. The airport's backers have more votes in the federal assembly and a minister who has already announced the terminal. The bridge's backers have a ranking that says the bridge carries more freight.\n\nThe treasury can publish the ranking and fund the bridge first, provoking a fight in the assembly. Or it can fund both by stretching the budget quietly, keeping the peace and weakening the ranking that was meant to settle exactly this kind of argument.",
         ("Publish the ranking and fund the bridge first.", "Fund both quietly.")),
        ("A Loan Book in Daylight",
         "The final review publishes the loan book: every project, its ranking, its cost and whether it was finished. The bridge is there, carrying freight. So is the terminal, funded a year later than its backers wanted.\n\nThe settlement does not end arguments about where Aurelia should invest. It makes sure they start from the same list.")),
    Branch("AUR", "exports", settled(STAGE_1), "date > 2005.12.31",
        ("Arms Export and Procurement Rules", "Restrictive Export Licensing", "Open Export Licensing",
         "Buy What the Forces Can Maintain", "Review the Licensing Year", "Rules That Survive a Crisis"),
        ("Aurelian manufacturers sell equipment abroad and the armed forces buy at home, under rules written piecemeal over decades. The cabinet will record every licence, every buyer and every procurement contract before writing one set of rules.",
         "Export licences will be refused for buyers at war or likely to use equipment against civilians, with every decision published. Restrictive rules keep Aurelian equipment out of other countries' wars, and they cost manufacturers sales.",
         "Export licences will be granted to any buyer not under international sanctions, with decisions kept confidential. Open licensing supports industry and jobs, and it accepts that Aurelian equipment may appear in wars Aurelia wanted no part in.",
         "The forces will buy only equipment they can maintain with their own crews and supplies, even when more impressive systems are offered. Maintainable procurement is less glamorous, and it is the equipment that will still work in a crisis.",
         "The review examines one funded licensing and procurement year: licences granted and refused, equipment delivered and equipment that worked. It records the refusals as carefully as the sales.",
         "The settlement fixes the export rules and the procurement standard. It does not decide who Aurelia's friends are. It decides what Aurelia will sell, to whom, and what its own forces will buy."),
        (("document", "industry"), ("gate", "document"), ("industry", "diplomacy"), ("tools", "training"), ("scales", "industry"), ("industry", "peace")),
        (("Restrictive export licensing", {"stability_factor": 0.02}, {"production_factory_efficiency_gain_factor": -0.01}),
         ("Open export licensing", {"production_factory_efficiency_gain_factor": 0.025}, {"political_power_gain": -0.04})),
        (("Run the Licensing Board", "Fund a board that reviews every export licence under the rules.", "The ministry of trade", {"political_power_gain": 0.08}),
         ("Audit Procurement Readiness", "Check that purchased equipment can be maintained by the forces' own crews.", "The defence procurement office", {"army_org_factor": 0.025})),
        ("A Licence Request From the South",
         "A manufacturer asks for a licence to sell armoured vehicles to a buyer in the south whose paperwork is in order. The intelligence service attaches a note: the buyer is a front for one side in a neighbour's civil war. The manufacturer says it cannot be expected to read intelligence notes it never sees.\n\nThe licensing board can refuse the licence and publish its reasons, accepting a public quarrel with the manufacturer. Or it can refuse privately, protecting the intelligence service's source and the manufacturer's reputation.",
         ("Refuse publicly, with reasons.", "Refuse privately.")),
        ("A Ledger of Licences",
         "The final review lists every licence granted and refused, with the reasons. The armoured vehicles were never shipped. The procurement section lists equipment the forces bought and could maintain, and the more impressive systems they declined.\n\nThe rules will be tested by the next crisis. They were written so that the test would not have to be improvised.")),
    Branch("AUR", "relations", settled(STAGE_2), "date > 2013.12.31",
        ("Review Relations with Leasath", "Renegotiate the Terms", "Hold the Existing Agreements",
         "Talk to Every Faction That Answers", "Review a Year of Contacts", "Relations on the Record"),
        ("Aurelia's agreements with Leasath were signed with governments and factions that may no longer speak for the country. The cabinet will record every treaty, contract and channel still in force, and who on the Leasathian side still answers.",
         "Aurelia will offer to renegotiate the southern agreements, including the terms Leasathians have complained about for years. Renegotiation could lower tensions with a neighbour emerging from war, and it costs Aurelian firms and asks the federation to admit old terms were unequal.",
         "Aurelia will hold to the agreements as signed and insist that any successor government honour them. Holding firm protects contracts and the principle that treaties bind, and it hands Leasathian nationalists a grievance they can use.",
         "Contacts will be kept with every Leasathian faction willing to talk, through consular offices, trade missions and church networks. Wide contacts give early warning of trouble, and each one can be read in Leasath as Aurelia picking a side.",
         "The review examines one funded year of contacts: who answered, what was agreed and which warnings proved accurate. It does not count meetings that produced nothing.",
         "The settlement keeps the chosen course and the record of every contact. Whether it is enough to keep the peace with Leasath is not something the federation alone can decide."),
        (("diplomacy", "document"), ("scales", "diplomacy"), ("document", "gate"), ("communications", "diplomacy"), ("scales", "communications"), ("diplomacy", "peace")),
        (("Renegotiated southern terms", {"stability_factor": 0.025}, {"production_factory_efficiency_gain_factor": -0.015}),
         ("Existing agreements held", {"production_factory_efficiency_gain_factor": 0.02}, {"stability_factor": -0.015})),
        (("Staff the Southern Missions", "Keep consular and trade missions open to every faction that answers.", "The ministry of foreign affairs", {"political_power_gain": 0.08}),
         ("Fund a Renegotiation Round", "Pay for negotiating teams, legal review and compensation studies.", "The ministry of trade", {"stability_factor": 0.025})),
        ("A Letter That Names the Old Terms",
         "A letter arrives from a Leasathian minister. It is polite and specific: it lists the port fees, mining royalties and loan terms that Leasathians have complained about for years, and asks whether Aurelia is prepared to discuss them before 'other voices' in Leasath decide the matter for everyone.\n\nThe ministry can publish the letter and a reply that commits to talks, putting the issue before the Aurelian public. Or it can reply confidentially, keeping options open while it decides what Aurelia is willing to give.",
         ("Publish the letter and commit to talks.", "Reply confidentially.")),
        ("The Contacts File",
         "The final review is the contacts file: every Leasathian office, faction and individual who answered Aurelia's calls, and what each said. The minister's letter is in it, with Aurelia's reply and the meetings that followed.\n\nThe file cannot say what Leasath will do next. It records what Aurelia offered and what it refused, which is what Leasathians will judge.")),
    Branch("AUR", "readiness", settled(STAGE_2), "date > 2013.12.31",
        ("A Readiness Review", "Dispersed Readiness", "Concentrated Capital Defence",
         "Keep Reserves Where They Can Move", "Review an Exercise Year", "Forces That Can Answer an Emergency"),
        ("Aurelia's forces have been organised for a peace that has lasted a long time. The defence ministry will record where units, aircraft and supplies are based, and how long each would take to answer an emergency anywhere in the country.",
         "Forces and supplies will be spread across bases throughout the country, including remote ones, so that no single loss leaves Aurelia defenceless. Dispersal is expensive and hard to command, and it keeps the federation able to fight from anywhere.",
         "Forces will be concentrated around the capital and the main industrial areas, where most people and infrastructure are. Concentration is efficient and easy to command, and it puts much of the federation's strength in one place.",
         "Reserves need transport, fuel and orders that work when communications fail. The ministry will plan movement for every reserve unit and test it, rather than assume roads, railways and radios will be available.",
         "The review examines one funded exercise year: units moved, bases reached and plans that failed. It records failures plainly, because an exercise that cannot fail teaches nothing.",
         "The settlement fixes the federation's readiness posture and the plans that support it. It names no enemy. It decides how quickly Aurelia can answer if one appears."),
        (("command", "logistics"), ("runway", "logistics"), ("command", "security"), ("rail", "logistics"), ("scales", "command"), ("security", "peace")),
        (("Dispersed readiness", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.01}),
         ("Concentrated capital defence", {"production_factory_efficiency_gain_factor": 0.02}, {"army_org_factor": -0.01})),
        (("Run a National Exercise", "Exercise reserve movement to bases across the country.", "The defence ministry", {"army_org_factor": 0.03}),
         ("Stock the Dispersed Depots", "Fund fuel and supply depots at bases outside the capital.", "The defence logistics directorate", {"production_speed_infrastructure_factor": 0.035})),
        ("A Base at the Edge of the Map",
         "The exercise report singles out one remote base. Its runway is in good order and its crews are trained, but the fuel convoy took four days to arrive and the radio link failed twice. The base commander's note ends with a question: if the capital went silent, what would the base be expected to do?\n\nThe defence ministry can publish the report, including the commander's question, and invite a public debate on readiness. Or it can circulate it to commanders only, fixing the convoy and radio without telling the public how thin the margins are.",
         ("Publish the report and the question.", "Circulate it to commanders only.")),
        ("Orders That Work Without the Capital",
         "The final review lists every base, its supplies and the time it takes to answer. The remote base is there, with a fuel depot of its own and written orders for the case its commander asked about.\n\nAurelia's forces are no larger than before. They are better placed to answer an emergency the federation hopes will never come.")),
    Branch("AUR", "account", settled(STAGE_2), "date > 2013.12.31",
        ("The Public Account", "An Open Audit", "A Protected Ledger",
         "Count What the Federation Owes", "Review the Long Record", "An Account the Public Can Read"),
        ("Decades of contracts, loans, licences and services have left the federation with obligations scattered across ministries. The cabinet will publish what Aurelia owes, what it is owed and what its choices have cost, before the next parliament has to decide what to keep.",
         "Independent auditors will examine the federation's accounts and agreements, and their reports will be published in full. An open audit builds confidence at home and abroad, and it exposes every awkward contract to public argument.",
         "Sensitive accounts, from defence procurement to foreign agreements, will be kept in a protected ledger available to parliamentary committees only. Protection keeps negotiations and security matters private, at the price of public suspicion about what is being kept back.",
         "Every obligation will be counted, including guarantees, contracts in dispute and promises made to other governments. An obligation that is not counted is still owed.",
         "The review examines one funded audit period before the account becomes the standard for future budgets.",
         "The settlement fixes how Aurelia accounts for its obligations and who may read the account. It keeps the chosen balance between openness and protection, and the duty to explain both to the people who pay."),
        (("document", "economy"), ("scales", "assembly"), ("document", "security"), ("economy", "scales"), ("scales", "document"), ("assembly", "peace")),
        (("Open federal audit", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Protected federal ledger", {"political_power_gain": 0.05}, {"stability_factor": -0.01})),
        (("Fund an Independent Audit", "Commission auditors to examine the federation's accounts and agreements.", "The federal audit office", {"stability_factor": 0.025}),
         ("Count the Obligations", "Compile every guarantee, contract and promise into one account.", "The federal treasury", {"political_power_gain": 0.08})),
        ("The Guarantee in the Footnote",
         "The auditors find a guarantee in a footnote: the federation is liable for a large loan taken by a firm operating in Leasath, signed by a minister long since retired. Nobody in the treasury knew it existed. If the firm defaults, Aurelia pays.\n\nThe audit office wants the guarantee published with everything else. The treasury would rather keep it in the protected ledger until it knows whether the firm will default, so as not to start the default by announcing the risk.",
         ("Publish the guarantee.", "Keep it in the protected ledger for now.")),
        ("Everything the Federation Owes",
         "The final account lists every obligation: loans, guarantees, contracts in dispute and promises to other governments. The footnoted guarantee is there, on the first page of its section.\n\nParliament can now argue about what Aurelia owes with the same numbers in front of every member. That is what the account was for.")),
)

OPENINGS = {
    "AUR": ("A Federation Without a Register",
        "The cabinet's first meeting on the state of the federation begins with a request nobody can fulfil: a list of what Aurelia's services do, who staffs them and what they cost. Each ministry has its own figures. None agree.\n\nThe ministers must decide how to build a common record, and how much of the disagreement between their ministries to show in public.",
        ("Open the register to public questions.", "Begin with a protected cabinet docket.")),
}
FINALS = {
    "AUR": ("A Federation That Knows Itself",
        "The last review of the period sets the federation's records side by side: services, trade disputes, radar sites, loans, licences, contacts with Leasath, readiness and the public account. Each has a cost and a record of what it delivered.\n\nAurelia is not safer because it keeps records. It is better placed to know what it can do when it is tested.",
        {"army_org_factor": 0.02}),
}

WAVE = Wave(
    prefix="ac_aur", infix="au", label="The Federal Foundations", source="tools/content_waves",
    countries={"AUR": "Aurelia"}, eligible="",
    branches=BRANCHES,
    layout={"AUR_services": (2, 1), "AUR_trade": (8, 1), "AUR_airspace": (14, 1),
            "AUR_leasath_war": (2, 7), "AUR_finance": (8, 7), "AUR_exports": (14, 7),
            "AUR_relations": (2, 13), "AUR_readiness": (8, 13), "AUR_account": (14, 13)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"AUR": "has_country_flag = AUR_au_relations_settlement_done has_country_flag = AUR_au_account_settlement_done"},
    themes={"AUR": ("document", "radar")},
)

TREE_ID = "aur_national_campaign"


def owner():
    """Tree adoption for saves that already hold the generic or regional tree."""
    loc = {
        TREE_ID: "Aurelia: The Federal Foundations",
        TREE_ID + "_desc": "Services, the southern trade, weather and air warning, Leasath's civil war, finance, export rules, relations, readiness and the public account, 1991-2018. Provisional gameplay.",
        "AUR_au_adopt_campaign": "Adopt the Federal Foundations Programme",
        "AUR_au_adopt_campaign_desc": "Switch from the regional or generic focus tree to Aurelia's national programme. Completed focuses are kept. Available only while no regional or generic focus is in progress.",
    }
    adopt = block("AUR_au_adopt_campaign",
        "icon = ac_aur_AUR_au_adopt_campaign\nallowed = { tag = AUR original_tag = AUR }\n"
        f"visible = {{ tag = AUR original_tag = AUR NOT = {{ has_focus_tree = {TREE_ID} }} ac_pol_previous_tree_idle = yes }}\n"
        f"available = {{ ac_pol_previous_tree_idle = yes }}\ncost = 0\n" +
        block("complete_effect", f"load_focus_tree = {{ tree = {TREE_ID} keep_completed = yes }}") + "ai_will_do = { base = 10 }\n")
    return dict(loc=loc, decisions={"ac_aur_aur_services": [adopt]})


# Registry declarations ------------------------------------------------------
KEY = "AUR"
NAME = "aurelia"
TREES = {"AUR": TREE_ID}
LEDGER = "docs/CONTENT_WAVES_B_AUR.md"
SOURCES = {"official_context": ["Chronicle 2019 / XX.XX: the Leasath civil war ends after ten years (start about 2009, derived)",
                                "Chronicle 2020 / 10.XX: Leasath cites years of exploitation (recorded as Leasath's claim only)"],
           "mod_provenance": ["Country history, office, world start and institution profile"],
           "provisional_gameplay": "Every focus, policy, service, dialogue and value; no 2020 place, person or weapon is used"}
NEWS_ART = ()
OWNER_ART = {}
