"""Shilage: a dormant release tree. Provisional gameplay on mod-provenance geography.

Shilage cannot exist at the 1991 start. Its history file holds no state; its three cores
(426, 447, 607) are owned by Erusea (history/states). No authored release event exists
(docs/WORLD_RELEASE_FOUNDATIONS.md); the only routes in 1991-2005 are the engine's own
release mechanics (an Erusean player releasing it, or a peace conference). This tree is
weighted only for tag = SHI, so the engine assigns it only when such a country is created.
It adds no release, annexation, core or border effect. States 447 and 607 are never named:
607 is an unresolved XXX placeholder and the package maps no Chronicle place to a state.
"""
from schema import F, E, O, I, R, D, L

TAG, NAME, ADJ = "SHI", "Shilage", "Shilagian"
STATES = (426, 447, 607)
CNEA = False
ACCENT = (176, 196, 140, 255)
SILHOUETTE = [(96, 10), (178, 52), (166, 160), (96, 182), (26, 160), (14, 52)]
TREE_TITLE = "Shilage Restored"
TREE_DESC = ("A short programme for a Shilagian state that exists only if Erusea releases it, by a player's choice or "
             "at a peace conference. It builds a government, a treasury and a border from almost nothing, and never "
             "touches the release itself.")

FLAGS = {
    "terms_with_erusea": "Shilage has sought practical terms with Erusea",
    "amber_road_open": "Shilage has opened the Amber road",
    "war_neutrality": "Shilage has declared itself outside the war",
}

IDEAS = [
    I("provisional_state", "A Provisional State",
      "Shilage's institutions are new, thin and borrowed. Every office is learning its work at the same time.",
      {"political_power_gain": -0.1, "stability_factor": -0.05, "production_speed_buildings_factor": 0.05}, ("assembly", "rebuild")),
    I("district_registers", "District Registers",
      "Each district now keeps its own register of residents, land and claims, checked against what survived the former administration.",
      {"stability_factor": 0.03, "political_power_gain": 0.05}, ("document", "civil")),
    I("national_treasury", "A National Treasury",
      "Shilage collects and spends its own revenue for the first time, in a currency that few yet trust.",
      {"consumer_goods_factor": -0.02, "political_power_gain": 0.05}, ("economy", "document")),
    I("constituent_assembly", "The Constituent Assembly",
      "An elected assembly writes the constitution in public, slowly and with every argument recorded.",
      {"stability_factor": 0.04, "political_power_gain": -0.05, "drift_defence_factor": 0.1}, ("ballot", "assembly")),
    I("directorate_decrees", "Government by Decree",
      "The Provisional Directorate governs by numbered decree until it decides that the emergency has ended.",
      {"political_power_gain": 0.1, "stability_factor": 0.02, "drift_defence_factor": 0.15}, ("document", "command")),
    I("practical_terms", "Practical Terms with Erusea",
      "Customs, post, rail and the records of the former administration are handled by agreed procedure with the former sovereign.",
      {"trade_opinion_factor": 0.1, "stability_factor": 0.02}, ("diplomacy", "document")),
    I("amber_road", "The Amber Road",
      "Shilage trades and travels through Amber, and plans its roads and depots around that border.",
      {"trade_opinion_factor": 0.1, "production_speed_infrastructure_factor": 0.1}, ("logistics", "diplomacy")),
    I("border_constabulary", "Border Constabulary",
      "A small armed constabulary that keeps the border posts open and the roads safe, and is not an army.",
      {"army_core_defence_factor": 0.05, "experience_gain_army_factor": 0.05}, ("security", "gate")),
    I("relief_clinics", "District Clinics",
      "Clinics in the district towns, staffed by whoever can be found and supplied by whoever will send supplies.",
      {"stability_factor": 0.03, "monthly_population": 0.03}, ("medical", "shelter")),
    I("outside_the_war", "Outside the War",
      "Shilage declares itself outside the continental war and asks every army to respect its roads.",
      {"stability_factor": 0.03, "war_support_factor": -0.05}, ("peace", "gate")),
]

REGIMES = [
    R("assembly", "Provisional Assembly Cabinet",
      "A cabinet answerable to the elected constituent assembly of restored Shilage.",
      "democratic", "centrism", True, {"democratic": 46, "neutrality": 38, "communism": 8, "fascism": 6, "monarchism": 2},
      ("ballot", "assembly")),
    R("directorate", "Provisional Directorate",
      "A small directorate of administrators governing by decree until a constitution can be agreed.",
      "neutrality", "centrism_na", False, {"neutrality": 58, "democratic": 28, "communism": 7, "fascism": 5, "monarchism": 2},
      ("command", "document")),
]

FOCUSES = [
    F("provisional_council", "Convene a Provisional Council", 6, 0, ("assembly", "rebuild"),
      "Shilage exists as a state again, and someone has to answer the telephone. A provisional council of the district officials who stayed at their posts will govern until something better is agreed.",
      reward=("idea:provisional_state", "cap:5"), event="restored"),
    F("count_the_districts", "Count the Districts", 2, 1, ("document", "civil"),
      "Nobody knows exactly who lives in Shilage now, who owns what, or which records survived the former administration. The districts will count, and the council will publish what they find.",
      parents=("provisional_council",), reward=("idea:district_registers", "cap:3")),
    F("recover_the_registers", "Recover the Civil Registers", 6, 1, ("document", "communications"),
      "Birth, land and property registers were held by the former administration. Recovering them, or rebuilding them where they are lost, is the first condition of governing anyone.",
      parents=("provisional_council",), reward=("cap:4", "stab:0.02")),
    F("staff_the_border_posts", "Staff the Border Posts", 10, 1, ("gate", "security"),
      "A border that nobody staffs is a line on a map. Shilage will put officials at every crossing it controls, with orders to record traffic and to keep the roads open.",
      parents=("provisional_council",), reward=("build_capital:infrastructure:1",)),
    F("border_constabulary", "A Border Constabulary", 14, 1, ("security", "training"),
      "A constabulary, not an army: lightly armed, recruited locally and trained to keep order at the crossings without starting anything.",
      parents=("provisional_council",), reward=("idea:border_constabulary", "manpower:1500")),
    F("national_treasury", "Found a National Treasury", 0, 2, ("economy", "document"),
      "Shilage needs its own revenue, its own budget and somebody whose job it is to say no. The treasury opens in borrowed rooms with a borrowed safe.",
      parents=("count_the_districts",), reward=("idea:national_treasury",)),
    F("national_assembly", "Elect a National Assembly", 4, 2, ("ballot", "assembly"),
      "The council will hand power to an elected assembly as soon as the registers allow an election. The assembly will write the constitution and choose the cabinet.",
      parents=("count_the_districts", "recover_the_registers"), excludes=("provisional_directorate",), cost=10,
      ai=0, regime="assembly", event="assembly", reward=("swap:provisional_state:constituent_assembly",)),
    F("provisional_directorate", "Appoint a Provisional Directorate", 8, 2, ("command", "document"),
      "The council will hand power to a small directorate of administrators who can act quickly. Elections will follow when the emergency allows, which the directorate will decide.",
      parents=("count_the_districts", "recover_the_registers"), excludes=("national_assembly",), cost=10,
      ai=0, regime="directorate", event="directorate", reward=("swap:provisional_state:directorate_decrees",)),
    F("former_administration", "Accounts with the Former Administration", 12, 2, ("diplomacy", "scales"),
      "Pensions, debts, property and records left behind by the former administration all need an answer. Shilage must decide how it will deal with Erusea about them.",
      parents=("staff_the_border_posts",), event="erusea_question"),
    F("constabulary_training", "Constabulary Training Depot", 14, 2, ("training", "security"),
      "A training depot in the capital gives the constabulary a common drill, common rules of conduct and somewhere to keep its records.",
      parents=("border_constabulary",), reward=("xp:army:5", "build_capital:anti_air_building:1")),
    F("shilagian_currency", "Issue a Shilagian Currency", 0, 3, ("economy", "scales"),
      "A national currency, backed by very little except the treasury's promise to be careful. Its first value will be set by how carefully the promise is kept.",
      parents=("national_treasury",), reward=("pp:25", "cap:2")),
    F("first_constituent_session", "The First Constituent Session", 4, 3, ("assembly", "ballot"),
      "The assembly meets for the first time. Its opening session will be broadcast in full, including the arguments about procedure.",
      parents=("national_assembly",), reward=("stab:0.03", "pop:democratic:0.05")),
    F("directorate_numbered_decrees", "The Numbered Decrees", 8, 3, ("document", "command"),
      "The directorate publishes its decrees in numbered order, so that at least everyone knows what the rules are this week.",
      parents=("provisional_directorate",), reward=("pp:40", "cap:2")),
    F("practical_terms", "Practical Terms with Erusea", 10, 3, ("diplomacy", "document"),
      "Customs, post, rail and old records will be handled with the former sovereign by agreed procedure. It is not friendship. It is paperwork that works.",
      parents=("former_administration",), excludes=("amber_road",), reward=("idea:practical_terms", "flag:terms_with_erusea")),
    F("amber_road", "Open the Amber Road", 14, 3, ("logistics", "diplomacy"),
      "Shilage will look to its other neighbour. Trade, travel and supplies will run through Amber, and the state's roads will be planned around that border.",
      parents=("former_administration",), excludes=("practical_terms",), reward=("idea:amber_road", "flag:amber_road_open")),
    F("capital_works", "Capital Works Programme", 0, 4, ("rebuild", "tools"),
      "Roads, water and workshops in the capital, paid for in the new currency and built by local contractors who are paid on time.",
      parents=("shilagian_currency",), cost=10, reward=("build_capital:infrastructure:1", "build_capital:industrial_complex:1")),
    F("district_councils", "Elected District Councils", 4, 4, ("civil", "ballot"),
      "Each district elects a council with authority over its schools, roads and registers. The assembly keeps the rest.",
      parents=("first_constituent_session",), reward=("cap:4", "stab:0.02")),
    F("directorate_works_office", "The Directorate Works Office", 8, 4, ("tools", "command"),
      "A works office answerable to the directorate will build what the directorate decides needs building, quickly and without a public inquiry.",
      parents=("directorate_numbered_decrees",), reward=("build_capital:arms_factory:1", "pp:15")),
    F("customs_schedule", "A Joint Customs Schedule", 10, 4, ("economy", "gate"),
      "A customs schedule agreed with Erusea lets goods and travellers cross without a fresh argument, and a fresh fee, at every border post.",
      parents=("practical_terms",), reward=("pp:30", "tech:logistics_tech:0.5")),
    F("amber_road_depots", "Depots on the Amber Road", 14, 4, ("logistics", "rail"),
      "Fuel and goods depots along the road to Amber, so that trucks can make the journey without carrying their own supplies.",
      parents=("amber_road",), reward=("build_capital:fuel_silo:1", "tech:logistics_tech:0.5")),
    F("shilagian_constitution", "Adopt the Constitution", 4, 5, ("document", "ballot"),
      "The constitution is finished, argued over, amended and put to the districts. If they accept it, the provisional state stops being provisional.",
      parents=("district_councils",), cost=10, reward=("remove:constituent_assembly", "stab:0.05", "cap:5")),
    F("directorate_order", "The Directorate's Order", 8, 5, ("security", "command"),
      "The directorate declares the emergency managed and its decrees permanent, subject to review. Shilage is orderly and very quiet.",
      parents=("directorate_works_office",), reward=("stab:0.04", "cap:3")),
    F("seek_recognition", "Seek Recognition Abroad", 12, 5, ("diplomacy", "communications"),
      "Shilage will ask the governments of Usea to recognise it and to exchange representatives. Most will wait to see what Erusea says first.",
      parents=(("customs_schedule", "amber_road_depots"),), reward=("pp:30", "cap:2")),
    F("shelter_registers", "Shelter Registers", 6, 6, ("shelter", "document"),
      "Central Usea has warned that Ulysses will strike. Shilage has no observatory and few shelters, but it can count its cellars and decide who goes where.",
      era="ulysses", reward=("cap:3", "stab:0.02")),
    F("impact_relief", "Impact Relief Office", 6, 7, ("medical", "logistics"),
      "A relief office for the districts: what was damaged, who needs what, and what can be asked of neighbours who are dealing with the same night.",
      parents=("shelter_registers",), era="impact", reward=("cap:3",), event="impact"),
    F("refugee_columns", "Columns on the Roads", 4, 8, ("refugees", "gate"),
      "Erusea has closed its doors to refugees, and some of the people turned away are walking towards Shilage's border posts.",
      parents=("impact_relief",), era="closure", reward=("manpower:2000", "stab:-0.02", "cap:2")),
    F("district_clinics", "Clinics in the District Towns", 8, 8, ("medical", "civil"),
      "Clinics in every district town, staffed by whoever can be found and supplied by whoever will send supplies.",
      parents=("impact_relief",), era="impact", reward=("idea:relief_clinics",)),
    F("war_on_the_continent", "War on the Continent", 6, 9, ("communications", "security"),
      "Erusea has invaded San Salvacion. Shilage is small, newly made and between the belligerents' roads. It must decide what it will say.",
      parents=(("refugee_columns", "district_clinics"),), era="war", event="war", reward=("cap:2",)),
    F("outside_the_war", "Declare Shilage Outside the War", 6, 10, ("peace", "gate"),
      "Shilage declares that it is outside the war, asks every army to respect its roads, and staffs its border posts accordingly.",
      parents=("war_on_the_continent",), era="war", reward=("idea:outside_the_war", "flag:war_neutrality")),
    F("shilage_after_the_war", "Shilage After the War", 6, 11, ("peace", "document"),
      "The continental war is over. Shilage takes stock of what it built, what it promised and who now recognises it.",
      parents=(("outside_the_war", "seek_recognition"),), era="postwar", cost=10, event="postwar", reward=("stab:0.03", "cap:4")),
]

EVENTS = [
    E("restored", "Shilage Restored", (
        "The district officials who stayed at their posts met in the capital in a building that still carried the former administration's signs over the door. Nobody had thought to take them down. There were not enough chairs, and the first resolution of the provisional council was to borrow some.",
        "Shilage is a state again because Erusea has released it. How that happened, and what was agreed, will be argued about for years; for the council it is simply the fact they wake up to. The districts are there. The roads are there. The registers, the treasury, the courts and the border posts, the things that make a place a state rather than a region, are either missing or belong to someone else.",
        "The council's first list is short and urgent. Count the people. Recover the registers or rebuild them. Staff the border posts so that the border is a fact. Raise enough revenue to pay the people doing all of this. Every item depends on another, and none of them can wait for a constitution.",
        "Outside the building, a crowd waited most of the afternoon to hear what the council would say. When it came out, the announcement was brief: the council exists, it intends to hand over to something better, and it would be grateful if everyone kept the roads open in the meantime.",
        "This is an alternate branch. In the official chronology Shilage is among the small nations annexed by Erusea that declare independence only in 2019.",
    ), (O("Begin with the registers.", ("cap:2",)), O("Begin with the border posts.", ("stab:0.02",))),
        picture="gate", citation="Shilage's cores are mod provenance (history/states 426, 447, 607); the official 2019 / 10.01 independence declaration is outside this window (ACES Chronicle)"),
    E("assembly", "The Assembly Elected", (
        "The election was held in schools, post offices and, in one district, a cinema, because the registers allowed it and because the council had promised. Turnout was high. Counting was slow, partly because the ballot boxes had been borrowed from three different places and opened three different ways, and partly because every party sent observers who wanted to watch every ballot.",
        "The assembly that has emerged is a mixture of district notables, former officials, teachers, merchants and a small number of people who seem to have stood for election mainly to find out whether they could. Nobody has a majority. The largest group wants a constitution quickly and a cabinet that answers to the assembly; the second largest wants the constitution to be argued line by line in public, however long that takes.",
        "The provisional council has dissolved itself, as it said it would. Its members have mostly been elected, which some find reassuring and others find suspicious. The new cabinet is drawn from the assembly and has promised to govern by law while the law is being written, a promise that will be tested every week.",
        "Abroad, the election has been noticed. Several governments that had said nothing about Shilage have now said something cautious. Erusea has said that it notes the result.",
        "Shilage's assembly has bought itself legitimacy at home. Whether it can buy time as well depends on whether the treasury, the registers and the border posts keep working while the assembly argues.",
        "This is an alternate political path for an unsourced state. No Shilagian assembly is established in any official chronology.",
    ), (O("Write the constitution in public.", ("stab:0.02",), ai=0), O("Let a committee draft it first.", ("pp:25",), ai=0)),
        picture="assembly"),
    E("directorate", "The Provisional Directorate", (
        "The council's last act was to appoint five administrators as a Provisional Directorate and to give them the authority it had never quite had itself: to issue decrees, to appoint officials, and to decide when the emergency would end and elections could be held. The vote was close. Several council members left the room before it was taken.",
        "The directorate's argument is that a state with no registers, no treasury and no army cannot afford a parliament that argues. Roads need repairing now. Officials need paying now. The border posts need orders that will not be overturned by next week's vote. A directorate can act; an assembly can only discuss.",
        "Its first decrees are sensible and numerous. Officials keep their posts and their pay. The registers will be rebuilt district by district. Customs will be collected at every post. Public meetings require a permit, which will usually be granted. Newspapers may publish freely, provided they publish the decrees as well.",
        "The districts have accepted the directorate with relief in some places and resignation in others. Abroad, governments that like order have noticed that Shilage has some. Governments that prefer elections have noticed that it has none, and have said so politely.",
        "The directorate has promised elections when the emergency has passed. It has not said what passing would look like, and it has the authority to decide. In the cafes of the capital, people have started counting the decrees the way they once counted the days until the next election.",
        "This is an alternate political path for an unsourced state. No Shilagian directorate is established in any official chronology.",
    ), (O("Publish a timetable for elections.", ("stab:0.02",), ai=0), O("Govern first; elections later.", ("pp:40",), ai=0)),
        picture="document"),
    E("erusea_question", "The Former Administration", (
        "The files arrived in a lorry from the frontier: pension records, land titles, a list of property that had belonged to the former administration and a much longer list of debts it had owed. The covering letter, from Erusean officials, was courteous and brief. It said that these were the records Shilage had asked for, that others would follow, and that certain questions remained open.",
        "Shilage's officials have read the files and agree that the questions are large. Who pays the pensions of people who worked for the former administration? Who owns the buildings it left? Which debts did it incur on Shilage's behalf, and which on its own? None of these has an easy answer, and each answer will tell Erusea and everyone else what kind of state Shilage intends to be.",
        "There are two broad paths. Shilage can seek practical terms with Erusea: agreed procedures for customs, post, rail and records, which keep things working and say nothing about the past. Or it can turn to its other neighbour, Amber, and build its trade and travel around that border instead, keeping dealings with the former sovereign to the minimum.",
        "Neither path changes where the border is. Both will be read in Farbanti and elsewhere as a statement.",
    ), (O("Answer the letter promptly.", ("cap:2",)), O("Take time over the reply.", ("stab:0.01",))),
        picture="diplomacy"),
    E("impact", "The Night the Sky Fell", (
        "The relief office opened the morning after the impact in two rooms of the treasury building, because the treasury had telephones and the relief office did not. By noon it had a list of what the districts were reporting, a second list of what they needed, and a third, much shorter list of what Shilage could provide from its own resources.",
        "The reports are confused and will remain so for days. Lines are down. Some districts have not reported at all, and the office cannot yet tell whether that means they are unharmed or unable to report. Radio stations from the larger states are carrying news of damage across the continent, and Shilage's officials are listening to it with the same mixture of fear and helplessness as everyone else.",
        "What the office can do is modest. It can count. It can send the constabulary's trucks where the roads allow. It can ask the neighbours for help, knowing that they are asking the same of their own neighbours. And it can make sure that, whatever Shilage receives, it reaches the districts that need it and not the ones that shout loudest.",
        "The relief office's first public notice says exactly that, in plain words, and asks everyone with a working vehicle to report to their district council.",
    ), (O("Send the constabulary's trucks.", ("stab:0.02",)), O("Ask the neighbours for help.", ("cap:2",))),
        picture="medical", citation="the impact is official (ACES Chronicle, 1999 / 07.08); no impact site or damage in Shilage is asserted"),
    E("war", "Between the Armies", (
        "The news reached the capital by radio and then by the border posts, which reported unusual traffic on the roads within the hour. Erusea has invaded San Salvacion. The continent is at war again, and Shilage, which has never fought one as a state, lies between the belligerents' roads.",
        "Shilage has no army worth the name, no alliance and no seat at any table where the war will be decided. It has a constabulary, a set of border posts and a government that is still learning how to govern. Both sides will want things from it: passage, supplies, silence. Neither side is likely to ask politely for long.",
        "The government's options are few. It can declare itself outside the war, ask every army to respect its roads, and hope that a small state's neutrality is less trouble to violate than to respect. It can try to keep its head down and say nothing. Or it can wait to see which way the war goes before it decides anything at all.",
        "Whatever it decides, Shilage will be judged afterwards by what it did in these months, by its neighbours and by its own people. The constabulary has already asked for orders in writing, so that whoever comes to the border posts can be shown exactly what Shilage has decided, and nobody at a crossing has to improvise its foreign policy.",
    ), (O("Double the border posts.", ("xp:army:5",)), O("Say nothing yet.", ("pp:20",))),
        picture="security", citation="Erusea's invasion of San Salvacion is official (ACES Chronicle, 2003 / SUMMER)"),
    E("postwar", "Shilage After the War", (
        "The war is over and Shilage is still a state, which in the first months of the fighting not everyone had expected. Its border posts are still staffed. Its treasury is poorer and its registers are thicker. Its constabulary is more experienced than anyone wanted it to be.",
        "The government is now taking stock. Some neighbours recognised Shilage during the war; some did not, and some recognised it in ways that were carefully worded to mean very little. The refugees who crossed its border in the closure years are now residents, and some of them are now voters, or would be if Shilage held elections. The roads that were built for trade carried armies, and are in worse repair than they were.",
        "Above all, Shilage now has a history of its own: a few years of decisions made by its own government, for its own reasons, that nobody else can be blamed for. Its officials disagree about whether that history is a source of pride or of embarrassment, and they will go on disagreeing.",
        "The provisional state is no longer quite provisional. What it becomes next is a question for the years after this programme, and for people who will not remember a time before the border posts were staffed.",
    ), (O("Publish the war record.", ("stab:0.03",)), O("Rebuild the roads first.", ("build_capital:infrastructure:1",))),
        picture="peace", citation="the war's official end is ACES Chronicle, 2005 / 09.19; Shilage's part in it is not"),
]

DECISIONS = [
    D("district_census", "District Census Round",
      "Send the census teams back to the districts to update the registers and settle disputed claims for six months.",
      "has_completed_focus = SHI_ud_count_the_districts", ("timed:district_registers:180", "stab:0.01")),
]

LEDGER = [
    L("Shilage does not exist at the 1991 start: its history file holds no state, and its three cores (426, 447, 607) are owned by Erusea",
      "Mod provenance", "history/countries/SHI - Shilage.txt; history/states/426-State_426.txt, 447-State_447.txt, 607-State_607.txt",
      "ac_ud_shi_tree", "Recorded; the tree stays dormant until a SHI country exists"),
    L("No authored Shilage release event exists; in 1991-2005 a SHI country can appear only through the engine's own release mechanics (an Erusean player releasing it, or a peace conference). The existing release foundation (capital 426) is unchanged",
      "Mod provenance", "docs/WORLD_RELEASE_FOUNDATIONS.md (SHI row); tools/release_foundations/README.md, 'Shilage core release'",
      "ac_ud_shi_tree, SHI_ud_adopt_programme", "No release, annexation, core or border change added"),
    L("Officially, Shilage is among the small nations annexed by Erusea that declare independence on 1 October 2019",
      "Official", "ACES Chronicle, 2019 / 10.01, compiled in docs/STRANGEREAL_2006_2020_SOURCES.md",
      "SHI event text only", "Reference only; outside this package's 1991-2005 window. The SHI tree is an explicit alternate branch"),
    L("State 607 is an unresolved XXX placeholder and state 447 is not named in text; Shilage rewards use the capital or an ownership guard",
      "Mod provenance", "history/states/607-State_607.txt; AGENTS.md geography rule", "SHI_ud_* build rewards", "Implemented"),
]
