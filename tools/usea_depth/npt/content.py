"""North Point Usea Depth content: focuses, ideas, government paths and helpers.

Source layers (docs/CANON_POLICY.md): the National Defense Council, the
subdivision governments, the four 1991 parties and the 1991 mandates are mod
provenance (April 2024 archive). Dated anchors cite the official ACES
Chronicle. Every effect, branch and alternate government is provisional
gameplay. No new named people, no place-to-state mapping, no border changes.
"""
from collections import namedtuple

PACKAGE = "npt"
TAG = "NPT"
MARKER = "USEA DEPTH NORTH POINT"
TREE = "npt_pre_continental_war_focus"
NAMESPACE = "ac_ud_npt"
BAND = (44, 94)

# Footer lines appended to every focus description.
PROV = "§gProvisional gameplay.§!"
MOD = ("§gMod provenance:§! the National Defense Council, its subdivision governments and the 1991 "
       "parties come from the April 2024 archive. The effects are provisional gameplay.")


def OFF(cite):
    return "§YOfficial:§! ACES Chronicle, %s. The effects are provisional gameplay." % cite


ARCHIVE = "April 5, 2024 Project Ulysses archive, SHA-256 e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071 (docs/CANON_LEDGER.md): NPT history, characters and ideas"
CHRONICLE = "ACES Chronicle, https://acecombat.jp/en/chronicle/details/"

Focus = namedtuple("Focus", "slug title x y cost pre excl available ai reward desc layer cite subjects event section")


def ident(ref):
    return ref if ref.startswith("NPT_") else "NPT_ud_" + ref


FOCUSES = []


def F(slug, title, x, y, desc, reward, subjects, section, cost=5, pre=(), excl=(), available="", ai="factor = 40",
      layer="prov", cite="", event=None):
    """pre is a list of OR-groups; every group must be satisfied."""
    FOCUSES.append(Focus(slug, title, x, y, cost, [list(g) for g in pre], list(excl), available, ai, reward.strip(),
                         desc, layer, cite, subjects, event, section))


SHELTER = "ac_ud_npt_shelter_progress = yes"
BUDGET = "ac_ud_npt_refresh_budget = yes"
PROGRAMME = "ac_ud_npt_fund_programme = yes"
RECOVERY = "ac_ud_npt_war_recovery = yes"
ANY_MANDATE = ("OR = { has_completed_focus = NPT_old_guard_mandate has_completed_focus = NPT_drp_mandate "
               "has_completed_focus = NPT_reformist_mandate }")
HOSTING = "OR = { has_completed_focus = NPT_host_isaf has_idea = ac_ucw_npt_isaf_rear_base }"
BEFORE_IMPACT = "date > 1996.4.19 date < 1999.7.8 NOT = { has_global_flag = ac_ucw_calendar_started }"


def swap(old_ideas, new):
    """Replace the first held idea in old_ideas with new, or add new."""
    lines = []
    for i, old in enumerate(old_ideas):
        lines.append("%s = { limit = { has_idea = %s } swap_ideas = { remove_idea = %s add_idea = %s } }"
                     % ("if" if i == 0 else "else_if", old, old, new))
    lines.append("else = { add_ideas = %s }" % new)
    return "\n".join(lines)


def friend(modifier="considers_friend", target="FCU"):
    return ("if = { limit = { country_exists = %s } add_opinion_modifier = { target = %s modifier = %s } "
            "%s = { add_opinion_modifier = { target = ROOT modifier = %s } } }") % (target, target, modifier, target, modifier)


STRATOCRACY = ["NPT_ud_compact_stratocracy_spirit", "NPT_democratic_stratocracy_idea"]

# ---------------------------------------------------------------- politics
F("council_question", "The Question Before the Council", 52, 0, [
    "The 1991 returns are counted, sealed and filed, and they have answered nothing. Every party now calls the vote a mandate, and every officer on the National Defense Council knows that the arrangement which kept the islands out of the continent's wars was never written down anywhere it could be amended.",
    "The Council has called a closed session to decide what the islands are to become. The subdivision governments have sent observers. The harbour unions have sent a letter. Nobody has sent a plan."],
  "add_political_power = 25\ncountry_event = { id = ac_ud_npt.1 }", ("assembly", "ballot"), "politics",
  available=ANY_MANDATE, ai="factor = 100", layer="mod", event=1)

F("council_endures", "The Council Endures", 46, 1, [
    "The Old Guard officers make their case in the language of ledgers: the harbours kept open to every flag, the wars the islands stayed out of, the ferries that ran on time. The Council will not dissolve itself, and it will not apologise for existing.",
    "What it offers instead is repair. The National Defense Council keeps the foreign ministry, the harbours and the guns, and it will learn to explain itself to the islands it protects. Nobody is promised a parliament. Everybody is promised an answer."],
  "set_country_flag = NPT_ud_path_council\nadd_stability = 0.03\ncountry_event = { id = ac_ud_npt.2 }",
  ("command", "security"), "politics", pre=[["council_question"]], excl=["parliament_petition", "reformist_programme"],
  ai="factor = 100", layer="mod", event=2)

F("parliament_petition", "Petition for a Parliament", 52, 1, [
    "The Democratic Republicans carry the petition from island to island on the morning ferries, and by the time it reaches the capital it fills three crates bound with fishing twine. It asks for one thing: a parliament elected by every island, with the Council answerable to it.",
    "The Council cannot ignore a petition signed across half the port towns. It can decide how long to spend reading it. The Democratic Republicans have decided not to let it take long."],
  "set_country_flag = NPT_ud_path_parliament\nadd_popularity = { ideology = democratic popularity = 0.05 }",
  ("ballot", "document"), "politics", pre=[["council_question"]], excl=["council_endures", "reformist_programme"],
  available="has_completed_focus = NPT_drp_mandate", ai="factor = 0", layer="mod")

F("reformist_programme", "The Reformist Programme", 58, 1, [
    "The Reformists never wanted the Council gone. They want it whole: one budget, one chain of command, one plan for every island, and no more harbour councils voting on whether the coastal guns may be test-fired.",
    "Their programme is printed on the naval academy's own press and handed out by cadets on leave. It calls the present arrangement a peacetime luxury and promises that a North Point which plans as one nation will never need to choose a side."],
  "set_country_flag = NPT_ud_path_directorate\nadd_popularity = { ideology = fascism popularity = 0.05 }",
  ("training", "document"), "politics", pre=[["council_question"]], excl=["council_endures", "parliament_petition"],
  available="has_completed_focus = NPT_reformist_mandate", ai="factor = 0", layer="mod")

# Council (stratocracy, the AI path): no change of ruling party.
F("merit_boards", "Open the Merit Boards", 44, 2, [
    "The Council has always called itself meritocratic, and the islands have always noticed that merit tends to run in the same few service families. The new boards will examine candidates from every subdivision in public halls, with the marks posted on the harbour notice boards the next morning.",
    "The first examination draws a queue around the block. Not every candidate passes. Every candidate goes home knowing why."],
  "add_ideas = NPT_ud_merit_boards_spirit", ("training", "medal"), "politics", pre=[["council_endures"]], ai="factor = 80")

F("subdivision_compact", "The Subdivision Compact", 48, 2, [
    "For decades the line between the Council's business and the subdivisions' business has been settled by habit, telephone calls and the occasional threat. The compact writes it down: what the islands govern, what the Council governs, and how a dispute between them is heard.",
    "It is a dry document and the radio announcers struggle to make it sound exciting. The subdivision clerks, who have spent their careers guessing, read it twice."],
  swap(["NPT_democratic_stratocracy_idea"], "NPT_ud_compact_stratocracy_spirit"), ("scales", "document"), "politics",
  pre=[["council_endures"]], ai="factor = 80", layer="mod")

F("council_bulletin", "The Council Bulletin", 44, 3, [
    "Every Friday the Council will publish what it decided, what it spent and what it declined to discuss. The first edition runs to four pages, two of which are a list of harbour dues.",
    "The Bulletin is pinned up in post offices and read aloud on the evening broadcast. Within a month the subdivision newspapers are printing replies, and the Council has started reading them."],
  "add_political_power = 40\nadd_stability = 0.02", ("document", "communications"), "politics", pre=[["merit_boards"]],
  ai="factor = 60")

F("civil_liaison", "Civil Liaison Officers", 48, 3, [
    "Each subdivision hall receives an officer whose only duty is to listen. They carry no weapons and command no troops; they write reports, and the Council has promised to answer every one within a month.",
    "The first reports are about ferries, school roofs and fishing quotas. The second batch is about the liaison officers themselves. The Council reads both."],
  "add_stability = 0.03\nadd_political_power = 20", ("civil", "communications"), "politics",
  pre=[["subdivision_compact"]], ai="factor = 60")

F("succession_question", "The Question of Succession", 46, 4, [
    "Nobody has ever written down how a seat on the National Defense Council is filled when its holder retires. Seats have changed hands by understanding, by recommendation and, now and then, by funeral. The compact and the merit boards have made that silence conspicuous.",
    "The Council must decide whether it renews itself by seniority, as it always has in practice, or by rotation through the merit boards. Either answer will outlast the officers who give it."],
  "country_event = { id = ac_ud_npt.3 }", ("command", "scales"), "politics",
  pre=[["council_bulletin"], ["civil_liaison"]], ai="factor = 60", event=3)

F("seniority_rule", "Seniority on the Council", 44, 5, [
    "The Council chooses continuity. Seats pass to the longest-serving officers of each service, and the islands are told, with some justice, that experience cannot be examined in a public hall.",
    "The decision steadies the barracks and the wardrooms. In the port towns it is received as the Council protecting its own, which is not entirely unfair either."],
  "add_ideas = NPT_ud_council_seniority_spirit", ("medal", "security"), "politics", pre=[["succession_question"]],
  excl=["rotation_by_merit"], ai="factor = 60")

F("rotation_by_merit", "Rotation by Merit", 48, 5, [
    "Seats on the Council will rotate on fixed terms, filled from officers who have passed the merit boards and served a term in a subdivision post. Nobody will sit at the table who has not first sat in a harbour office and been shouted at about ferry fares.",
    "The older officers call it a revolution. The younger ones call it overdue. The fishing towns call it the first Council decision they have fully understood."],
  "add_ideas = NPT_ud_council_rotation_spirit", ("training", "scales"), "politics", pre=[["succession_question"]],
  excl=["seniority_rule"], ai="factor = 40")

F("council_charter", "A Charter for the Council", 46, 6, [
    "Everything the Council has conceded since 1991 is gathered into a single charter: the compact, the merit boards, the Bulletin and the rules of succession. It is read in every subdivision hall on the same evening and signed by every member of the Council in front of the cameras.",
    "The charter does not make North Point a democracy. It makes it something rarer: a military government that has written down the limits of its own authority."],
  swap(STRATOCRACY, "NPT_ud_chartered_council_spirit"), ("document", "assembly"), "politics", cost=10,
  pre=[["seniority_rule", "rotation_by_merit"]], ai="factor = 80", layer="mod")

F("council_emergency_powers", "Emergency Powers for the Sky", 44, 7, [
    "The asteroid warning has given the Council something it has wanted for years and dreaded for as long: a reason for emergency powers. The charter lets it requisition ferries, warehouses and labour for civil defence. It also obliges the Council to publish every requisition in the Bulletin.",
    "The officers draft the orders carefully. If the islands are to give up their boats and their warehouses, they will want to know exactly who asked, and why."],
  SHELTER + "\nadd_political_power = 30", ("meteor", "command"), "politics", pre=[["council_charter"]],
  available="date > 1996.4.19", ai="factor = 60", layer="official", cite="1996 / 04.20")

F("council_open_sessions", "Open Sessions of the Council", 48, 7, [
    "Twice a year the Council will sit with the public gallery open. Any citizen may submit a written question, and the Council must answer the ten most supported in person.",
    "The first open session runs four hours over time. The admirals are asked about ferry timetables, and a schoolchild asks why the radar station on the headland hums at night. The Council answers both. It is not dignified, but every household with a radio is listening."],
  "add_stability = 0.04\nadd_war_support = 0.02", ("assembly", "communications"), "politics", pre=[["council_charter"]],
  ai="factor = 50")

F("council_long_watch", "The Council's Long Watch", 46, 8, [
    "The Council that sat down in 1991 to answer the question of the islands has given its answer. It remains, it governs the harbours and the guns, and it has learned to account for both.",
    "No one would call it a perfect arrangement. It has survived elections, petitions and the threat of a falling sky, and the islands have discovered that they can argue with their soldiers without fearing them."],
  "add_stability = 0.05\nadd_war_support = 0.05\narmy_experience = 20\nnavy_experience = 20", ("security", "medal"),
  "politics", pre=[["council_emergency_powers", "council_open_sessions"]], ai="factor = 60", layer="mod")

# Parliament (democratic): player-only, provisional alternate history.
F("subdivision_delegates", "Convene the Subdivision Delegates", 52, 2, [
    "Every subdivision government is invited to send three delegates to the capital: one from its council, one from its civil service and one chosen by lot from its electoral roll. The Council provides the hall, the stenographers and a guarantee that nobody will be arrested for anything said inside it.",
    "The delegates arrive with competing drafts, regional grievances and, in one case, a crate of smoked fish as a gesture of goodwill. The first week is spent agreeing on the order of business."],
  "add_political_power = 25\nadd_popularity = { ideology = democratic popularity = 0.05 }", ("assembly", "refugees"),
  "politics", pre=[["parliament_petition"]], ai="factor = 0")

F("constitutional_convention", "The Constitutional Convention", 52, 3, [
    "The convention sits in the old customs hall, the only building in the capital large enough to seat every delegate and honest enough to have no portraits on the walls. The Council's observers take the back row and say nothing for three days.",
    "The argument that matters is not whether North Point will have a parliament. It is what kind: a federal compact that leaves the islands their own governments, or a single roll of electors that makes the archipelago one nation."],
  "add_stability = -0.03\nadd_political_power = 30\ncountry_event = { id = ac_ud_npt.4 }", ("document", "ballot"),
  "politics", cost=10, pre=[["subdivision_delegates"]], ai="factor = 0", event=4)

F("federal_compact", "A Federal Compact of Islands", 50, 4, [
    "The convention votes for the islands as they are. Each subdivision keeps its government, its budget and its courts; the parliament will sit for what they share: defence, foreign relations, the harbours and the currency.",
    "The outer islands celebrate. The capital's economists warn that a federation of fishing towns will struggle to raise a loan. Both are right."],
  "set_country_flag = NPT_ud_convention_federal\nadd_stability = 0.04", ("bridge", "assembly"), "politics",
  pre=[["constitutional_convention"]], excl=["unitary_parliament"], ai="factor = 0")

F("unitary_parliament", "One Roll for All the Islands", 54, 4, [
    "The convention votes for one nation. Every adult on every island will be entered on a single electoral roll, and the parliament it elects will govern the whole archipelago. The subdivision governments become local councils, with their powers set by law.",
    "The capital celebrates. Several outer-island delegates walk out and are persuaded back with guaranteed seats. The compromise is ugly, and it holds."],
  "set_country_flag = NPT_ud_convention_unitary\nadd_political_power = 50\nadd_stability = -0.02", ("ballot", "civil"),
  "politics", pre=[["constitutional_convention"]], excl=["federal_compact"], ai="factor = 0")

F("parliament_of_islands", "The Parliament of the Islands", 52, 5, [
    "The National Defense Council hands its foreign and defence portfolios to a cabinet answerable to the new Parliament of the Islands. The handover takes place in the customs hall at noon, with the Council in dress uniform and the cabinet in borrowed suits.",
    "Until the first national election can be organised, the cabinet governs as a provisional office. It has no leader the islands know by name, only a mandate, a convention and a very short list of things it is allowed to get wrong."],
  "ac_ud_npt_regime_parliament = yes\n" + swap(STRATOCRACY, "NPT_ud_island_parliament_spirit")
  + "\ncountry_event = { id = ac_ud_npt.5 }", ("assembly", "peace"), "politics", cost=10,
  pre=[["federal_compact", "unitary_parliament"]], ai="factor = 0", event=5)

F("civilian_defence_ministry", "A Civilian Ministry of Defence", 50, 6, [
    "The Defense Forces now report to a minister who has never worn a uniform. The officers are courteous about it in public and less so in the wardrooms, but the orders are obeyed.",
    "The new ministry inherits the old doctrine of isolation along with the coastal guns, and it is quietly rewriting the first while keeping the second. North Point will still defend every island. It will no longer pretend that the rest of Usea does not exist."],
  swap(["NPT_militarist_isolationism_idea"], "NPT_ud_civilian_defence_spirit"), ("civil", "security"), "politics",
  pre=[["parliament_of_islands"]], ai="factor = 0", layer="mod")

F("open_budget", "The Open Budget", 54, 6, [
    "For the first time the national budget is debated line by line in public. The harbour dues, the fuel subsidies and the Defense Forces' spare-parts account are all read into the record, and the record is printed.",
    "The debate lasts eleven days. Several long-standing payments to suppliers nobody can locate are quietly cancelled, and the treasury discovers it has rather more money than it believed."],
  "add_political_power = 40\nadd_stability = 0.02\n" + BUDGET, ("economy", "document"), "politics",
  pre=[["parliament_of_islands"]], ai="factor = 0")

F("council_retired", "Retire the Council with Honour", 50, 7, [
    "The National Defense Council still exists on paper: a committee of senior officers with no portfolio and a great deal of prestige. The cabinet must decide whether to abolish it outright or keep it as an advisory body the generals can be proud to sit on.",
    "The question is not sentimental. The Defense Forces accepted civilian rule because the Council told them to. How the Council itself is treated will be remembered in every barracks."],
  "army_experience = 15\ncountry_event = { id = ac_ud_npt.6 }", ("medal", "peace"), "politics",
  pre=[["civilian_defence_ministry"]], ai="factor = 0", layer="mod", event=6)

F("first_national_election", "The First National Election", 54, 7, [
    "The ballot boxes come ashore on the morning ferries again, as they did in 1991. This time they will elect a parliament with the power to govern, and the candidates know it. Posters cover the harbour walls and the radio carries debates into the small hours.",
    "The provisional cabinet has promised to hand over to whoever wins. The Defense Forces have promised to escort the ballot boxes and nothing else."],
  "add_stability = 0.05\ncountry_event = { id = ac_ud_npt.23 }", ("ballot", "fishing"), "politics",
  pre=[["open_budget"]], ai="factor = 0", event=23)

F("island_rights_charter", "A Charter of Island Rights", 52, 8, [
    "The parliament's first great act is a charter that no government, civilian or military, may repeal by an ordinary vote: the right of every island to its own council, the right of every citizen to petition, and the right of the harbours to stay open to anyone in distress.",
    "The last clause is the convention's tribute to the fishing towns, and it will be quoted more often than any of the others."],
  "add_ideas = NPT_ud_rights_charter_spirit", ("scales", "civil"), "politics", cost=10,
  pre=[["council_retired"], ["first_national_election"]], ai="factor = 0")

F("voice_in_usea", "A Voice in Usean Councils", 52, 9, [
    "The new government sends its foreign minister to the mainland with a message the old Council never cared to deliver: North Point is a parliamentary state and expects to be treated as one. The continental diplomats are polite and a little surprised.",
    "The islands gain no alliance and want none. They gain a seat at the conferences where shipping, fisheries and the asteroid are discussed, and a reputation for doing what they say."],
  "add_political_power = 25\n" + friend(), ("diplomacy", "assembly"), "politics", pre=[["island_rights_charter"]],
  ai="factor = 0")

# Readiness Directorate (armed neutrality): player-only, provisional alternate history.
F("readiness_audit", "The National Readiness Audit", 58, 2, [
    "Reformist staff officers spend a season touring every island with clipboards. They count rifles, ferries, fuel drums, fishing boats that could carry troops and harbour cranes that could lift a gun. Nothing is too small to be listed.",
    "The audit's conclusion is a single sentence: the islands could defend themselves, if anyone were in charge of all of them at once. The Reformists intend to be."],
  "army_experience = 15\nair_experience = 10\nnavy_experience = 10", ("document", "tools"), "politics",
  pre=[["reformist_programme"]], ai="factor = 0")

F("readiness_directorate", "The Readiness Directorate", 58, 3, [
    "The National Defense Council votes, by a narrow and bitterly argued margin, to suspend the old division of powers and govern through a Readiness Directorate. The subdivision governments remain, but their budgets, their ports and their roads now answer to the Directorate's plan.",
    "The Directorate is an office, not a person. Its orders are signed with a seal and its spokesmen never give their names. The Reformists call this modesty. Their opponents call it the point."],
  "ac_ud_npt_regime_directorate = yes\n" + swap(STRATOCRACY, "NPT_ud_readiness_state_spirit")
  + "\ncountry_event = { id = ac_ud_npt.7 }", ("command", "gate"), "politics", cost=10,
  pre=[["readiness_audit"]], ai="factor = 0", event=7)

F("national_service", "Universal National Service", 56, 4, [
    "Every citizen of North Point will serve: eighteen months for most, in the Defense Forces, the coast watch or the civil defence corps. Exemptions are few and published.",
    "The ferries fill with conscripts heading for the training depots, and the fishing towns complain that their crews have been taken in the middle of the season. The Directorate adjusts the call-up dates and nothing else."],
  "add_ideas = NPT_ud_national_service_spirit", ("training", "refugees"), "politics", pre=[["readiness_directorate"]],
  excl=["professional_cadre"], ai="factor = 0")

F("professional_cadre", "A Professional Cadre", 60, 4, [
    "The Directorate decides that a small, well-paid, long-serving force will defend the islands better than a large and resentful one. Recruiters tour the schools with brochures and the promise of a trade.",
    "The Defense Forces become smaller, older and much harder to surprise. The fishing towns keep their crews, and the Directorate keeps their gratitude."],
  "add_ideas = NPT_ud_professional_cadre_spirit", ("medal", "training"), "politics", pre=[["readiness_directorate"]],
  excl=["national_service"], ai="factor = 0")

F("subdivision_prefects", "Prefects for the Subdivisions", 58, 5, [
    "Each subdivision receives a prefect from the Directorate, with authority over its harbours, its fuel stores and its emergency plans. The elected councils keep their schools, their clinics and their tempers.",
    "The first prefects are met at the ferry ramps by silent crowds. In two subdivisions the councils refuse to hand over the keys to the harbour offices."],
  "add_political_power = 50\nadd_stability = -0.04\ncountry_event = { id = ac_ud_npt.8 }", ("gate", "civil"),
  "politics", pre=[["national_service", "professional_cadre"]], ai="factor = 0", event=8)

F("hedgehog_doctrine", "The Hedgehog Doctrine", 56, 6, [
    "Armed neutrality, the Directorate declares, means making every island a separate fortress that must be taken separately. Coastal batteries are dispersed, ammunition is buried, and every harbour is surveyed for blocking with sunken hulks.",
    "Visiting attaches are invited to watch the exercises. They are meant to report home that North Point would be expensive to invade. Most of them do."],
  swap(["NPT_militarist_isolationism_idea"], "NPT_ud_hedgehog_islands_spirit"), ("security", "tools"), "politics",
  pre=[["subdivision_prefects"]], ai="factor = 0", layer="mod")

F("directorate_radio", "Directorate Radio", 60, 6, [
    "The evening broadcast is reorganised under the Directorate's information office. The shipping forecast stays. The music becomes more martial, the news becomes shorter, and a nightly segment explains, patiently and at length, why the plan is working.",
    "The islands keep listening, because there is little else to listen to and because the shipping forecast is still the best on the coast."],
  "add_war_support = 0.05\nadd_political_power = 30", ("communications", "radar"), "politics",
  pre=[["subdivision_prefects"]], ai="factor = 0")

F("neutrality_declared", "Neutrality Declared to the World", 58, 7, [
    "The Directorate sends identical notes to every government with an embassy on the islands. North Point will join no alliance, host no foreign base and admit no foreign warship to its harbours without inspection. Any power that violates its waters will be treated as an enemy.",
    "The notes are acknowledged with diplomatic courtesy. In private, at least one embassy asks whether the islands are serious, and its attache is invited to watch a live-fire exercise from very close range."],
  "add_stability = 0.05\narmy_experience = 20", ("diplomacy", "security"), "politics",
  pre=[["hedgehog_doctrine"], ["directorate_radio"]], ai="factor = 0")

F("directorate_review", "The Directorate Reviews Itself", 58, 8, [
    "The Directorate was established for an emergency its founders defined generously. The audit is complete, the islands are fortified and the harbours answer to a single plan. The question now is whether it remains a temporary office or becomes the permanent government of North Point.",
    "The Reformists are divided. The subdivision councils, which kept their schools and lost their harbours, are watching closely."],
  "add_stability = 0.03\ncountry_event = { id = ac_ud_npt.9 }", ("command", "document"), "politics",
  pre=[["neutrality_declared"]], ai="factor = 0", event=9)

# ---------------------------------------------------------------- island industry
F("island_economy", "What the Islands Make", 68, 0, [
    "The islands have always lived by the sea: fish, ferries, harbour dues and the repair trade for ships passing through the straits. The government's economists have produced the first complete survey of what North Point actually makes, and it is a short document.",
    "There is money for one serious industrial programme. The yards and the airfields are both asking, and the survey's authors have declined, very carefully, to recommend either."],
  "add_political_power = 20\ncountry_event = { id = ac_ud_npt.10 }", ("economy", "industry"), "industry",
  ai="factor = 70", event=10)

F("grid_interconnect", "Interconnect the Island Grids", 64, 1, [
    "Each island has its own generators, its own voltage and its own opinion about which is correct. Undersea cables will tie the larger islands into a single grid, so that a storm on one does not plunge the others into darkness.",
    "The cable ships work through two winters. When the switch is thrown, half the capital's lights flicker and then steady, and the engineers break out a bottle they have been saving for a year."],
  "add_tech_bonus = { name = NPT_ud_grid_interconnect bonus = 0.5 uses = 1 category = industry }\n"
  "ac_ud_npt_capital_infrastructure = yes", ("bridge", "industry"), "industry", pre=[["island_economy"]], ai="factor = 50")

F("fuel_reserve", "The Strategic Fuel Reserve", 68, 1, [
    "North Point imports every litre of fuel it burns. The reserve will hold enough to keep the ferries, the fishing fleet and the Defense Forces running for a season if the tankers stop coming.",
    "The tanks are dug into the hillsides behind the main harbour and painted the colour of the rock. The harbour children are told they are water tanks, and believe it for nearly a week."],
  "ac_ud_npt_build_fuel = yes\n" + BUDGET, ("logistics", "gate"), "industry", pre=[["island_economy"]], ai="factor = 50")

F("ferry_timetable", "A National Ferry Timetable", 72, 1, [
    "Every island runs its own ferries, and no two timetables agree. A national timetable will coordinate them so that a passenger, a crate of fish or a company of reservists can cross the archipelago in a day.",
    "It takes a year of negotiation with a dozen ferry companies and a fishermen's cooperative. The result is printed on a single sheet and pinned up in every harbour office, and it is the most popular document the government has ever produced."],
  "ac_ud_npt_build_infrastructure = yes\nadd_stability = 0.02", ("navy", "logistics"), "industry",
  pre=[["island_economy"]], ai="factor = 50")

F("harbour_yards", "The Harbour Yards", 66, 2, [
    "The government chooses the sea. The ship-repair yards around the main harbours will grow into real shipyards, able to build the patrol craft and coasters the islands have always bought abroad.",
    "The yard foremen are delighted and immediately ask for twice the money. The welders ask for a training school. The government gives them half of each and a deadline."],
  "ac_ud_npt_build_dockyard = yes\nac_ud_npt_build_dockyard = yes\nadd_ideas = NPT_ud_harbour_yards_spirit\n" + PROGRAMME,
  ("industry", "navy"), "industry", cost=10, pre=[["grid_interconnect", "fuel_reserve", "ferry_timetable"]],
  excl=["airframe_workshops"], ai="factor = 60")

F("airframe_workshops", "The Airframe Workshops", 70, 2, [
    "The government chooses the air. The overhaul hangars at the Defense Forces' airfields will become workshops able to rebuild engines, airframes and radar sets, and in time to build light aircraft of their own.",
    "The ground crews are delighted and immediately ask for a wind tunnel. They do not get one. They do get licences, tools and a contract to service every airliner that lands on the islands."],
  "ac_ud_npt_build_arms = yes\nac_ud_npt_capital_air_base = yes\nadd_ideas = NPT_ud_airframe_workshops_spirit\n" + PROGRAMME,
  ("air", "tools"), "industry", cost=10, pre=[["grid_interconnect", "fuel_reserve", "ferry_timetable"]],
  excl=["harbour_yards"], ai="factor = 40")

F("longer_slipways", "Lengthen the Slipways", 64, 3, [
    "The old slipways were built for trawlers. Lengthened and reinforced, they will take hulls the size of a coastal escort, and the yards will no longer turn away ferries that need a new keel.",
    "The work is done in the off-season, when the fishing fleet is laid up and the yards would otherwise be idle. It finishes a month late, which the foremen describe as early."],
  "ac_ud_npt_build_dockyard = yes\nnavy_experience = 10", ("rebuild", "navy"), "industry", pre=[["harbour_yards"]],
  ai="factor = 50")

F("marine_engines", "Marine Engine Workshops", 66, 3, [
    "Most ships that fail in North Point's waters fail in the engine room. The yards will build their own engine workshops, able to overhaul the diesels of the fishing fleet and, in time, of the Defense Forces' patrol craft.",
    "The first apprentices are the children of fishermen who have been repairing engines on deck for years. They pass the practical examination with ease and struggle with the paperwork."],
  "add_tech_bonus = { name = NPT_ud_marine_engines bonus = 0.5 uses = 1 category = ac_naval_systems_category }",
  ("tools", "fishing"), "industry", pre=[["harbour_yards"]], ai="factor = 50")

F("shipwright_schools", "Shipwright Schools", 64, 4, [
    "A shipyard is only as good as the people in it, and North Point has been losing its best shipwrights to the mainland for years. The new schools pay apprentices a wage and promise them a berth in the island yards when they qualify.",
    "The first class is twice the size the instructors expected. Half have relatives already in the yards. The other half have relatives who left, and want to know whether it is worth coming home."],
  "add_tech_bonus = { name = NPT_ud_shipwright_schools bonus = 1 uses = 1 category = ac_naval_escort_category }\n"
  "add_stability = 0.02", ("training", "navy"), "industry", pre=[["longer_slipways", "marine_engines"]], ai="factor = 40")

F("overhaul_hangars", "Overhaul Hangars", 70, 3, [
    "New hangars at the main airfield will let the workshops strip an aircraft to its frame, inspect every rivet and rebuild it to a better standard than it left the factory.",
    "The first aircraft through is the oldest trainer in the Defense Forces' inventory. It flies out six weeks later, and its instructor swears it climbs better than it did on the day the instructor first learned to fly it."],
  "ac_ud_npt_capital_air_base = yes\nair_experience = 15", ("air", "rebuild"), "industry", pre=[["airframe_workshops"]],
  ai="factor = 50")

F("avionics_benches", "Avionics Benches", 72, 3, [
    "Radios, radar sets and navigation equipment fail in the salt air faster than anything else on an aircraft. The avionics benches will repair them on the islands instead of shipping them to the mainland and waiting months for their return.",
    "The technicians are recruited from the radar stations on the headlands, where they have been keeping old equipment alive with spare parts and patience."],
  "add_tech_bonus = { name = NPT_ud_avionics_benches bonus = 0.5 uses = 1 category = electronics }",
  ("radar", "tools"), "industry", pre=[["airframe_workshops"]], ai="factor = 50")

F("aero_engines", "Licensed Aero-Engine Production", 72, 4, [
    "The workshops have learned to repair engines. The next step is to build them under licence, so that the Defense Forces' aircraft no longer depend on a single foreign supplier's goodwill.",
    "The licence is expensive and the first engines come slowly. They are also, the test pilots report, entirely reliable, which on islands with few emergency runways is the only quality that matters."],
  "ac_ud_npt_build_arms = yes\nadd_tech_bonus = { name = NPT_ud_aero_engines bonus = 0.5 uses = 1 category = ac_air_systems_category }",
  ("air", "industry"), "industry", pre=[["overhaul_hangars", "avionics_benches"]], ai="factor = 40")

F("self_sufficiency", "Self-Sufficiency within the Archipelago", 68, 5, [
    "Whatever the government chose to build, the lesson of the programme is the same: the islands can make more of what they need than anyone believed. A civil works programme now spreads the new skills from the main harbour to the outer islands.",
    "Workshops open in towns that have never had anything larger than a boatyard. Not all of them will last. Enough of them will."],
  "ac_ud_npt_build_civilian = yes\nadd_ideas = NPT_ud_self_sufficient_islands_spirit\n" + PROGRAMME, ("industry", "civil"),
  "industry", cost=10, pre=[["shipwright_schools", "aero_engines"]], ai="factor = 50")

F("cannery_contracts", "Cannery Contracts with the Mainland", 66, 6, [
    "North Point's fish has always gone to the continent fresh, at whatever price the mainland buyers chose to pay. The new canneries will put it in tins, with the islands' name on the label, and sell it on contracts the government negotiates.",
    "The first contract is signed with a Central Usean wholesaler and the second with an Erusean one. The government sees no contradiction in feeding both."],
  "add_political_power = 40\n" + BUDGET, ("fishing", "economy"), "industry", pre=[["self_sufficiency"]], ai="factor = 40")

F("spare_parts", "The Spare-Parts Depots", 70, 6, [
    "The surveys found that half of North Point's broken machinery was waiting for a part that existed somewhere on the islands, in a warehouse nobody had catalogued. The new depots catalogue everything and ship it on the national ferry timetable.",
    "The wait for a spare part falls from months to days. The Defense Forces, which have been hoarding parts in their own stores for decades, are persuaded to join the catalogue, eventually."],
  "add_equipment_to_stockpile = { type = support_equipment_1 amount = 150 producer = NPT }\nadd_stability = 0.02",
  ("logistics", "tools"), "industry", pre=[["self_sufficiency"]], ai="factor = 40")

F("industry_stands_alone", "An Industry That Can Stand Alone", 68, 7, [
    "The yards, the workshops, the canneries and the depots now form a single economy rather than a collection of harbours that happen to fly the same flag. North Point still imports its fuel and its steel, but it no longer imports its skills.",
    "If the tankers ever stop coming, the islands will not run for long. They will run for longer than anyone on the continent expects."],
  swap(["NPT_ud_self_sufficient_islands_spirit"], "NPT_ud_island_industry_spirit") + "\nac_ud_npt_build_civilian = yes",
  ("industry", "medal"), "industry", cost=10, pre=[["cannery_contracts"], ["spare_parts"]], ai="factor = 50")

# ---------------------------------------------------------------- fleet
F("fleet_review", "The Fleet at Anchor", 80, 0, [
    "Once a year the Defense Forces' small navy anchors in a single line off the capital so the islands can see it. This year the naval staff use the review to ask a question nobody has asked in a generation: what is the fleet for?",
    "One school of officers wants a fleet that can make the straits impassable. The other wants a fleet that can keep the sea lanes open when the tankers need an escort. The budget will pay for one of them."],
  "navy_experience = 10\ncountry_event = { id = ac_ud_npt.11 }", ("navy", "command"), "fleet", ai="factor = 60",
  event=11)

F("coastal_fleet", "A Coastal Defence Fleet", 78, 1, [
    "The naval staff choose the straits. North Point's fleet will be small, fast and close to home: torpedo boats, minelayers and submarines that make any approach to the islands a gamble.",
    "The fleet will never cross an ocean. It is not meant to. It is meant to make sure that nobody crosses the narrow seas around North Point without the islands' permission."],
  "add_ideas = NPT_ud_coastal_fleet_spirit\nnavy_experience = 15", ("submarine", "security"), "fleet",
  pre=[["fleet_review"]], excl=["ocean_escorts"], ai="factor = 60")

F("ocean_escorts", "An Ocean Escort Fleet", 82, 1, [
    "The naval staff choose the sea lanes. North Point's fleet will build frigates and fleet oilers able to escort a tanker convoy across open water, because islands that cannot import fuel have already surrendered.",
    "The fleet will never be large. It will practise convoy work until it is second nature."],
  "add_ideas = NPT_ud_escort_fleet_spirit\nnavy_experience = 15", ("navy", "economy"), "fleet", pre=[["fleet_review"]],
  excl=["coastal_fleet"], ai="factor = 40")

F("fast_attack_craft", "Fast Attack Craft for the Straits", 76, 2, [
    "The yards and the naval staff design a fast attack craft small enough to hide in a fishing harbour and armed heavily enough to threaten a destroyer. The first boats are laid down on the old trawler slipways.",
    "Their crews come from the fishing towns, where people who have handled boats since childhood find the work familiar and the pay better than fishing."],
  "add_tech_bonus = { name = NPT_ud_fast_attack_craft bonus = 0.5 uses = 1 category = ac_naval_escort_category }\n"
  "navy_experience = 10", ("navy", "missile"), "fleet", pre=[["coastal_fleet"]], ai="factor = 50")

F("straits_minefields", "Plans for the Straits Minefields", 78, 2, [
    "North Point will not lay mines in peacetime. It will survey every channel, stockpile the mines and train the minelayers, so that the straits can be closed within days if the islands are threatened.",
    "The survey charts are classified. The fishermen, who know every channel better than the charts do, are quietly consulted anyway."],
  "add_tech_bonus = { name = NPT_ud_straits_minefields bonus = 1 uses = 1 category = naval_mines }\nnavy_experience = 5",
  ("gate", "navy"), "fleet", pre=[["coastal_fleet"]], ai="factor = 50")

F("coastal_submarines", "A Submarine Flotilla", 76, 3, [
    "A handful of coastal submarines will lie in wait in the deep channels between the islands. They are cramped, slow and miserable to serve in, and they are the one weapon every naval staff on the continent takes seriously.",
    "The first crews train for months before the island yards can deliver their boats. The flotilla's motto, painted on its first conning tower, is a single word: patience."],
  "add_tech_bonus = { name = NPT_ud_coastal_submarines bonus = 0.5 uses = 2 category = ac_naval_submarine_category }\n"
  "navy_experience = 10", ("submarine", "training"), "fleet", pre=[["fast_attack_craft"]], ai="factor = 50")

F("straits_watch", "The Straits Watch", 78, 3, [
    "A chain of radar stations and observation posts along the headlands will watch every channel into North Point's waters, day and night, and report to a single naval control room in the capital.",
    "The watch logs every ship that passes: tankers, trawlers, freighters and the occasional warship that wanders closer than its captain intended. Within a year the logbooks are the best record of northern shipping anywhere."],
  "ac_ud_npt_capital_radar = yes\nnavy_experience = 5", ("radar", "navy"), "fleet", pre=[["straits_minefields"]],
  ai="factor = 50")

F("escort_frigates", "Escort Frigates", 82, 2, [
    "The yards will build frigates designed for one task: shepherding merchant ships through hostile water. They will carry sonar, anti-aircraft guns and enough fuel to stay with a slow convoy for a week.",
    "The design is unglamorous and the admirals who prefer big guns grumble about it. The tanker captains who may one day sail through a war zone do not grumble at all."],
  "add_tech_bonus = { name = NPT_ud_escort_frigates bonus = 0.5 uses = 1 category = ac_naval_escort_category }\n"
  "navy_experience = 10", ("navy", "radar"), "fleet", pre=[["ocean_escorts"]], ai="factor = 50")

F("convoy_school", "The Convoy School", 84, 2, [
    "Escorting a convoy cannot be learned from a manual. The convoy school will train naval officers and merchant captains together, in classrooms and at sea, until each understands what the other will do when the first torpedo is reported.",
    "The merchant captains are sceptical until the first exercise, when a frigate lays a smoke screen exactly where it said it would. After that they ask to come back."],
  "navy_experience = 20", ("training", "logistics"), "fleet", pre=[["ocean_escorts"]], ai="factor = 50")

F("fleet_oilers", "Fleet Oilers", 82, 3, [
    "Frigates are useless if they must turn back for fuel halfway across the sea. Coastal tankers converted in the island yards will let the escort fleet stay at sea as long as its convoy does.",
    "The first replenishment exercise ends with a fuel hose in the water and a frigate captain in a towering rage. The second goes better."],
  "add_tech_bonus = { name = NPT_ud_fleet_oilers bonus = 0.5 uses = 1 category = ac_naval_fleet_category }\n"
  "navy_experience = 5", ("logistics", "navy"), "fleet", pre=[["escort_frigates"]], ai="factor = 50")

F("sea_lane_patrols", "Sea-Lane Patrols", 84, 3, [
    "The escort fleet begins regular patrols along the tanker routes, showing the islands' flag to every merchant ship that passes and logging anything unusual.",
    "The patrols find nothing dramatic: a drifting lifeboat, an unlit freighter, a fishing fleet far outside its waters. They find enough to convince the naval staff that the sea lanes are less empty than they look."],
  "navy_experience = 15\nadd_war_support = 0.02", ("navy", "communications"), "fleet", pre=[["convoy_school"]],
  ai="factor = 50")

F("naval_air_wing", "A Naval Air Wing", 80, 4, [
    "Whatever kind of fleet North Point has chosen, it cannot see far enough from the sea. A naval air wing of patrol aircraft and helicopters will extend its eyes beyond the horizon and its reach beyond its guns.",
    "The aviators and the sailors argue for a month about who will command it. The answer is both, which satisfies neither and works surprisingly well."],
  "air_experience = 15\nadd_tech_bonus = { name = NPT_ud_naval_air_wing bonus = 0.5 uses = 1 category = ac_air_maritime_category }",
  ("air", "submarine"), "fleet", pre=[["coastal_submarines", "straits_watch", "fleet_oilers", "sea_lane_patrols"]],
  ai="factor = 50")

F("fishermen_reserve", "The Fishermen's Naval Reserve", 78, 5, [
    "The islands' fishermen know the waters better than any naval officer. The new reserve enlists them, their boats and their radios as auxiliary patrol craft and observers in time of crisis.",
    "The reservists drill one weekend a month and are paid for their fuel. Their reports are informal, frequently profane and, the naval staff admit, almost always accurate."],
  "navy_experience = 10\nadd_stability = 0.02", ("fishing", "communications"), "fleet", pre=[["naval_air_wing"]],
  ai="factor = 40")

F("harbour_booms", "Harbour Defence Booms", 82, 5, [
    "Anti-submarine nets and booms will close the main harbours at a moment's notice, so that no hostile submarine can slip in among the ferries and the fishing fleet.",
    "The booms are tested at night to avoid disrupting the ferry timetable. The ferries are disrupted anyway, and the harbourmasters write a strongly worded letter."],
  "navy_experience = 10\nadd_war_support = 0.03", ("gate", "submarine"), "fleet", pre=[["naval_air_wing"]],
  ai="factor = 40")

F("command_of_waters", "Command of the Island Waters", 80, 6, [
    "North Point's fleet will never challenge a great power at sea. It does not need to. Within its own waters it knows every channel, every harbour and every ship that passes, and it can close those waters or keep them open as the government decides.",
    "This year's review is held without speeches. The fleet anchors in line, the islands come out to watch, and the ships put to sea again the same afternoon."],
  "ac_ud_npt_build_dockyard = yes\nnavy_experience = 25\n" + PROGRAMME, ("navy", "medal"), "fleet", cost=10,
  pre=[["fishermen_reserve"], ["harbour_booms"]], ai="factor = 50")

# ---------------------------------------------------------------- Ulysses shelters, 1996-1999
F("sky_announcement", "A Date Written in the Sky", 90, 0, [
    "Central Usea has announced that the asteroid Ulysses will strike the Earth. The broadcast is repeated on the islands' radio in full, twice, and followed by a long silence while the station decides what to play next.",
    "The government and the subdivision councils meet the same evening. The astronomers cannot yet say where the fragments will fall. North Point has to prepare for a disaster nobody can map."],
  SHELTER + "\nset_country_flag = NPT_ud_ulysses_brief\nadd_ideas = NPT_ud_shelter_programme_spirit\n"
  "country_event = { id = ac_ud_npt.12 }", ("meteor", "communications"), "shelters",
  available="date > 1996.4.19 date < 1999.7.8", ai="factor = 90", layer="official", cite="1996 / 04.20", event=12)

F("headland_survey", "Survey the Headland Rock", 88, 1, [
    "Geologists are flown in from the mainland to survey the hard rock of the headlands, where tunnels could shelter the islands' people if the fragments fall nearby.",
    "Their report is cautiously encouraging. The rock is sound, the old coastal battery galleries can be extended, and the harbour towns are close enough to reach them within an hour. The outer islands are another matter."],
  SHELTER + "\nadd_tech_bonus = { name = NPT_ud_headland_survey bonus = 0.5 uses = 1 category = construction_tech }",
  ("shelter", "tools"), "shelters", pre=[["sky_announcement"]], available=BEFORE_IMPACT, ai="factor = 80")

F("civil_wardens", "Island Civil Wardens", 92, 1, [
    "Every street, village and fishing hamlet will have a civil warden: a volunteer trained to count heads, sound the alarm and lead the way to shelter. Each warden receives an armband, a whistle and a list of names.",
    "The volunteers come from every corner of island life: retired sailors, schoolteachers, ferry clerks and harbour shopkeepers who already know everyone's business. The training is short. The lists are long."],
  SHELTER + "\nadd_stability = 0.02", ("civil", "refugees"), "shelters", pre=[["sky_announcement"]],
  available=BEFORE_IMPACT, ai="factor = 80")

F("deep_tunnels", "Tunnels under the Headlands", 88, 2, [
    "The government chooses depth. Engineers will extend the battery galleries into tunnels beneath the headlands, deep enough to survive anything short of a direct strike and large enough to hold the people of the harbour towns.",
    "The work is slow, expensive and loud, and the blasting can be heard across the straits. The outer islands ask, reasonably, what is being built for them. The answer is ferries."],
  SHELTER + "\n" + SHELTER + "\nset_country_flag = NPT_ud_shelters_deep\n" + PROGRAMME, ("shelter", "rebuild"),
  "shelters", cost=10, pre=[["headland_survey", "civil_wardens"]], excl=["dispersed_shelters"],
  available=BEFORE_IMPACT, ai="factor = 50")

F("dispersed_shelters", "A Shelter in Every Village", 92, 2, [
    "The government chooses breadth. Instead of a few great tunnels, every village and hamlet will build its own shelter: a reinforced cellar, a dugout in a hillside, a chapel crypt with a steel door.",
    "No single shelter will survive a direct strike. Between them they put a refuge within a short walk of every household on every island, and the work gives every community something to do with its fear."],
  SHELTER + "\n" + SHELTER + "\nset_country_flag = NPT_ud_shelters_dispersed\nadd_stability = 0.02",
  ("shelter", "civil"), "shelters", cost=10, pre=[["headland_survey", "civil_wardens"]], excl=["deep_tunnels"],
  available=BEFORE_IMPACT, ai="factor = 50")

F("rock_wards", "Wards beneath the Rock", 86, 3, [
    "Hospitals cannot be evacuated in an hour. Underground wards with operating theatres, generators and a month of supplies will let the islands' doctors keep working while the sky falls.",
    "The surgeons inspect the first ward and ask for three changes, all of them involving light. The engineers provide them, and the doctors begin to stock the shelves."],
  SHELTER + "\nadd_stability = 0.02", ("medical", "shelter"), "shelters", pre=[["deep_tunnels"]],
  available=BEFORE_IMPACT, ai="factor = 60")

F("seed_vaults", "Grain and Seed Vaults", 88, 3, [
    "If the fragments darken the sky or foul the sea, the islands must feed themselves for a season without fishing or imports. Vaults of grain, seed and preserved food are sealed in the tunnels and inventoried by the civil wardens.",
    "The inventories are published, so that every island knows what is stored for it. Nothing does more for the islands' nerves than knowing, to the sack, what stands between them and hunger."],
  SHELTER + "\nadd_stability = 0.03", ("logistics", "shelter"), "shelters", pre=[["deep_tunnels"]],
  available=BEFORE_IMPACT, ai="factor = 60")

F("ferry_evacuation", "Evacuation by Ferry", 92, 3, [
    "The ferry fleet will rehearse moving the people of the most exposed islands to safer ground in a single day. Every ferry, trawler and harbour launch is given a route, a schedule and a list of passengers.",
    "The first rehearsal takes three days instead of one. The second takes a day and a half. The harbourmasters are told that the third had better take a day, and it does."],
  SHELTER + "\nadd_war_support = 0.02", ("navy", "refugees"), "shelters", pre=[["dispersed_shelters"]],
  available=BEFORE_IMPACT, ai="factor = 60")

F("shelter_kits", "Shelter Kits for the Outer Islands", 94, 3, [
    "The outer islands have no tunnels and few cellars. Each household there will receive a kit: water drums, a radio, a lamp, a first-aid case and instructions printed in large type.",
    "The kits arrive by ferry, and by fishing boat where the ferries do not run. The outer islanders are unimpressed by the instructions and delighted by the radios."],
  SHELTER + "\nadd_stability = 0.02", ("medical", "communications"), "shelters", pre=[["dispersed_shelters"]],
  available=BEFORE_IMPACT, ai="factor = 60")

F("fragment_forecasts", "Ask for the Fragment Forecasts", 88, 4, [
    "Central Usea's Stonehenge project is complete: eight railguns in a desert of San Salvacion, built to bring down the fragments of Ulysses before they reach the ground. North Point has no claim on the project and no guns that can reach the sky.",
    "It can ask for the forecasts. The trajectories the project's astronomers calculate will decide where the fragments fall, and the islands' shelter plans are only as good as their warning."],
  SHELTER + "\ncountry_event = { id = ac_ud_npt.14 }", ("telescope", "diplomacy"), "shelters",
  pre=[["rock_wards", "seed_vaults", "ferry_evacuation", "shelter_kits"]],
  available="date > 1998.6.18 date < 1999.7.8 NOT = { has_global_flag = ac_ucw_calendar_started }", ai="factor = 70",
  layer="official", cite="1998 / 06.19, and Super Weapons, Stonehenge", event=14)

F("fragment_watch", "The Headland Fragment Watch", 92, 4, [
    "The radar stations on the headlands were built to watch for aircraft. Retuned and joined by optical trackers, they will watch the sky for fragments and give the islands minutes of warning instead of seconds.",
    "The technicians are given new equipment, new orders and a direct telephone line to the civil wardens. They test the siren every evening at the same time, and the islands set their clocks by it."],
  SHELTER + "\nac_ud_npt_capital_radar = yes\nair_experience = 10", ("radar", "meteor"), "shelters",
  pre=[["rock_wards", "seed_vaults", "ferry_evacuation", "shelter_kits"]], available=BEFORE_IMPACT, ai="factor = 70")

F("last_drill", "The Last Drill", 90, 5, [
    "The final full-scale shelter drill is held with only months left on the calendar. The sirens sound across every island at once, the wardens open the tunnels and cellars, the ferries sail their evacuation routes and the hospitals move their patients below ground.",
    "When the all-clear sounds, the wardens count heads and file their reports, and the government reads every one. Whatever comes, North Point will meet it having rehearsed."],
  SHELTER + "\n" + SHELTER + "\nadd_war_support = 0.03\ncountry_event = { id = ac_ud_npt.15 }", ("shelter", "medal"),
  "shelters", pre=[["fragment_forecasts", "fragment_watch"]],
  available="date > 1998.12.31 date < 1999.7.8 NOT = { has_global_flag = ac_ucw_calendar_started }", ai="factor = 80",
  event=15)

F("coup_across_the_water", "The Coup across the Water", 94, 0, [
    "Coup forces have risen across Usea. The radio reports are confused and contradictory: barracks seized, broadcasts cut, airfields closed. By evening it is clear that the Unified Command is fighting back, and that the islands will not know for days who holds the coast opposite.",
    "North Point is no part of the rising and intends to stay that way. Its harbours are filling with ships whose captains would rather not go home until the shooting stops."],
  "add_war_support = 0.02\ncountry_event = { id = ac_ud_npt.13 }", ("security", "communications"), "shelters",
  available="date > 1997.5.29 date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started }", ai="factor = 70",
  layer="official", cite="1997 / 05.30", event=13)

F("harbour_garrisons", "Harbour Garrisons after the Coup", 94, 1, [
    "The coup has shown how quickly a quiet port can become a battlefield. Each main harbour will now have a standing garrison, a guarded fuel store and a plan for closing its gates within the hour.",
    "The garrisons are small and mostly bored. They are also the reason the shipping agents and the ferry companies sleep better, and soon nobody in the harbour towns can remember the docks without a sentry."],
  "army_experience = 15\nadd_stability = 0.03", ("security", "gate"), "shelters", pre=[["coup_across_the_water"]],
  ai="factor = 60")

# ---------------------------------------------------------------- impact relief, 1999-2002
F("after_the_fragments", "After the Fragments", 90, 7, [
    "Ulysses has passed the Roche limit and broken apart, and its fragments have fallen across the world. On the islands the sirens sounded, the shelters filled and the radio went silent for hours that felt like days.",
    "Now the shelter doors are opening. The first reports from the continent are fragmentary and terrible. What happened to the islands themselves will take weeks to count, and the government must decide where to begin."],
  "set_country_flag = NPT_ud_after_impact\nremove_ideas = NPT_ud_shelter_programme_spirit\ncountry_event = { id = ac_ud_npt.16 }",
  ("meteor", "rebuild"), "relief", available="date > 1999.7.7", ai="factor = 90", layer="official",
  cite="1999 / 07.08", event=16)

F("count_every_island", "Count Every Island", 88, 8, [
    "The civil wardens go door to door with the lists they drew up for the drills. Every name is checked, every building inspected, every harbour sounded for wreckage.",
    "The count is slow and painstaking, and the government refuses to publish a figure until it is finished. When it is published, it is believed, because every household on the islands helped to make it."],
  "add_stability = 0.04\nadd_political_power = 20", ("document", "refugees"), "relief",
  pre=[["after_the_fragments"]], ai="factor = 80")

F("reopen_harbours", "Reopen the Harbours", 92, 8, [
    "Nothing on the islands works without the harbours. Divers clear the channels, the cranes are inspected, and the ferry timetable restarts one route at a time, beginning with the routes that carry food.",
    "The first ferry to complete its full timetable since the fragments fell is met at every stop by a crowd. It is carrying flour and mail, which is exactly what the crowds were waiting for."],
  "ac_ud_npt_capital_infrastructure = yes\nadd_stability = 0.03", ("navy", "rebuild"), "relief",
  pre=[["after_the_fragments"]], ai="factor = 80")

F("ration_boards", "The Ration Boards", 86, 9, [
    "Until the tankers and freighters return, fuel and food will be rationed by elected boards on each island, using the inventories the civil wardens kept before the impact.",
    "The boards are argumentative, slow and scrupulously fair. Black markets appear and are reported to the boards by the very people they were meant to serve. Nobody on the islands goes hungry, though nobody eats well either."],
  "add_stability = 0.03\nadd_war_support = 0.02", ("scales", "logistics"), "relief", pre=[["count_every_island"]],
  ai="factor = 70")

F("outer_island_services", "Restore the Outer Island Services", 88, 9, [
    "The outer islands were the last to receive shelter kits and the last to receive news after the fragments fell. Engineers, doctors and radio technicians sail on the first available ferries to restore their power, their clinics and their link to the capital.",
    "The teams find the outer islanders already at work, with their own generators running and their own lists of what they need. The engineers mostly take notes."],
  "ac_ud_npt_build_infrastructure = yes\nadd_stability = 0.02", ("rebuild", "communications"), "relief",
  pre=[["count_every_island"]], ai="factor = 70")

F("relief_flights", "Relief Flights to the Continent", 92, 9, [
    "The islands have airfields, transport aircraft and, for the moment, more food than parts of the mainland coast. The government organises relief flights to the continent, flying supplies in and the injured out.",
    "The flights land wherever a runway is still usable and nobody objects to a North Point roundel. The aircrews fly until they are ordered to rest, and then fly again."],
  "air_experience = 15\n" + friend("air_force_cooperation"), ("air", "refugees"), "relief", pre=[["reopen_harbours"]],
  ai="factor = 70")

F("mainland_hospital_beds", "Hospital Beds for the Mainland", 94, 9, [
    "The shelter wards are emptying, and the government offers their beds to patients from the continent. Hospital ships and transport aircraft bring the injured to the islands for treatment.",
    "The island hospitals fill with patients who speak with mainland accents and ask, when they are well enough, how they can repay the islands. The doctors tell them to recover first."],
  "add_political_power = 30\nadd_stability = 0.02", ("medical", "navy"), "relief", pre=[["reopen_harbours"]],
  ai="factor = 70")

F("boats_from_the_south", "Boats from the South", 90, 10, [
    "Across Usea the displaced are still moving. In April 2000 Erusea's government reached its decision about the refugees at its borders, and whatever that decision has meant on the continent, small boats have begun to appear off North Point's southern harbours.",
    "They carry families, fishermen and a great many people who simply have nowhere else to go. The harbours cannot turn them away without a decision, and the government cannot postpone it much longer."],
  "country_event = { id = ac_ud_npt.17 }", ("refugees", "navy"), "relief",
  pre=[["ration_boards", "outer_island_services", "relief_flights", "mainland_hospital_beds"]],
  available="date > 2000.4.20", ai="factor = 80", layer="official", cite="2000 / 04.21", event=17)

F("open_harbours", "Open Harbours", 88, 11, [
    "The harbours will stay open. Anyone who reaches North Point by sea will be fed, sheltered and registered, and allowed to stay until it is safe to go home.",
    "The decision is popular in the port towns, where the old seafaring rule that no boat in distress is turned away is quoted on every quay. It is less popular in the treasury, which has to pay for it."],
  "set_country_flag = NPT_ud_harbours_open\nadd_ideas = NPT_ud_relief_harbour_spirit", ("refugees", "peace"), "relief",
  pre=[["boats_from_the_south"]], excl=["registered_quota"], ai="factor = 40")

F("registered_quota", "A Registered Quota", 92, 11, [
    "The harbours will accept refugees up to a quota the government sets each month, registered on arrival and housed in camps on the larger islands. Boats beyond the quota are given fuel, food and water and escorted onward.",
    "The policy satisfies nobody completely. It is, the government argues, the most the islands can promise and still keep."],
  "set_country_flag = NPT_ud_harbours_quota\nadd_ideas = NPT_ud_registered_quota_spirit", ("scales", "refugees"), "relief",
  pre=[["boats_from_the_south"]], excl=["open_harbours"], ai="factor = 60")

F("relief_ledger", "The Relief Ledger", 90, 12, [
    "With the worst of the relief work behind them, the government publishes the relief ledger: everything the islands spent, everyone they sheltered, every flight and every ferry.",
    "The ledger is not triumphant. It records the mistakes beside the successes, and the work of the wardens, doctors and aircrews who carried the islands through. The islands read it, argue about it and keep it."],
  "add_stability = 0.03\ncountry_event = { id = ac_ud_npt.18 }", ("document", "economy"), "relief",
  pre=[["open_harbours", "registered_quota"]], available="date > 2000.12.31", ai="factor = 70", event=18)

# ---------------------------------------------------------------- the continent, 2003-2005
F("continent_at_the_edge", "The Continent at the Edge", 74, 9, [
    "Years after the fragments fell, Usea has not recovered and has not forgiven. The refugee camps, the ruined towns and old grievances have left the continent's governments suspicious of one another, and the radio from the mainland grows more anxious every month.",
    "North Point is party to none of those quarrels. It is, however, an island chain within reach of all of them, with airfields, harbours and a fleet. Whatever happens on the continent, someone will soon ask the islands which side they are on."],
  "add_war_support = 0.05\narmy_experience = 10\ncountry_event = { id = ac_ud_npt.19 }", ("diplomacy", "radar"), "late",
  available="date > 2002.12.31", ai="factor = 80", event=19)

F("allied_rear", "Open the Islands to the Allies", 70, 10, [
    "North Point has agreed to host the Independent State Allied Forces, and the agreement is now a fact on the ground: aircraft on the runways, staff officers in the schools and allied ships in the harbours. The government must decide how far the islands will go.",
    "The answer is as far as the islands can bear. North Point will be the allies' rear base in earnest, with its yards, workshops and hospitals at their disposal, and in return it will ask to be consulted on everything done from its soil."],
  "set_country_flag = NPT_ud_lane_allied\nadd_ideas = NPT_ud_allied_rear_services_spirit\n" + RECOVERY, ("runway", "diplomacy"),
  "late", pre=[["continent_at_the_edge"]], excl=["neutral_waters"], available=HOSTING, ai="factor = 100",
  layer="official", cite="2004 / 09.16")

F("neutral_waters", "Keep the Waters Neutral", 78, 10, [
    "North Point will be nobody's base. Whatever coalitions form on the continent, the islands' airfields, harbours and yards will stay under the islands' own flag, open to ships in distress and closed to fleets at war.",
    "The decision costs the islands friends on the mainland and earns them a different kind of respect. A neutral harbour in a crisis is a rare and valuable thing, and the government intends to keep it that way."],
  "set_country_flag = NPT_ud_lane_neutral\nadd_ideas = NPT_ud_neutral_waters_spirit", ("peace", "navy"), "late",
  pre=[["continent_at_the_edge"]], excl=["allied_rear"], available="NOT = { " + HOSTING + " }",
  ai="factor = 10\nmodifier = { factor = 0 date < 2004.9.17 }")

F("schools_returned", "Give the Schools Back", 66, 11, [
    "The allied staff officers who took over the island schools have been grateful tenants, but the children want their classrooms back. The government builds a proper headquarters compound on the edge of the capital, with secure communications, barracks and an operations room.",
    "The move takes a fortnight. The children return to schools whose walls are covered in faded situation maps, and several teachers decide to leave them up."],
  "ac_ud_npt_build_civilian = yes\nadd_stability = 0.03", ("civil", "command"), "late", pre=[["allied_rear"]],
  ai="factor = 80")

F("joint_air_control", "A Joint Air Control Centre", 70, 11, [
    "Allied squadrons, island squadrons and civilian traffic now share the same crowded airspace. A joint control centre on the headlands, built around the radar stations, will coordinate all of them.",
    "The controllers speak with four accents and follow one procedure. Within a month the near-misses have stopped, and allied pilots who distrust anything that sounds like a headquarters begin to trust the voice from North Point."],
  "ac_ud_npt_capital_radar = yes\nair_experience = 20", ("radar", "air"), "late", pre=[["allied_rear"]], ai="factor = 80")

F("squadron_repair_depots", "Repair Depots for Allied Squadrons", 64, 12, [
    "Damaged allied aircraft land on the islands every day, many with damage their squadrons' own mechanics cannot repair. The island hangars open to them, working in shifts around the clock.",
    "The island mechanics learn more about modern aircraft in a month than in the previous decade, and allied pilots learn to ask for North Point by name when their aircraft are hit."],
  "ac_ud_npt_capital_air_base = yes\nair_experience = 10\n" + RECOVERY, ("tools", "air"), "late",
  pre=[["schools_returned"]], ai="factor = 80")

F("sealift_berths", "Sealift Berths", 68, 12, [
    "The allies' supplies arrive by sea, and the island harbours were built for ferries and trawlers. New deep-water berths, cranes and warehouses will let the sealift ships unload in hours instead of days.",
    "The work goes on around the ferry traffic, and the harbourmasters, who have lived through the impact and the relief years, take the crowding in their stride."],
  "ac_ud_npt_build_infrastructure = yes\n" + RECOVERY, ("bridge", "logistics"), "late",
  pre=[["schools_returned", "joint_air_control"]], ai="factor = 80")

F("field_hospitals", "Field Hospitals for the Front", 72, 12, [
    "The hospitals that sheltered the islands through the impact now receive the wounded of the war. Island doctors and nurses work beside allied medical staff, and the hospital ships cross every week.",
    "The work is grim and constant. It is also, the island doctors say, what they were trained for."],
  "add_manpower = 3000\nadd_war_support = 0.02", ("medical", "runway"), "late", pre=[["joint_air_control"]],
  ai="factor = 80")

F("harbour_town_strangers", "Strangers in the Harbour Towns", 68, 13, [
    "The allied presence has doubled the population of some harbour towns. Rents and tempers are rising together, and the island newspapers are full of letters about noise, traffic and allied personnel who do not know that the ferries leave on time.",
    "Nothing has gone seriously wrong yet. Both the government and the allied command know that one bad night could turn grumbling into something worse."],
  "country_event = { id = ac_ud_npt.20 }", ("refugees", "security"), "late",
  pre=[["squadron_repair_depots", "sealift_berths", "field_hospitals"]], ai="factor = 80", event=20)

F("islands_carried_the_load", "The Islands That Carried the Load", 68, 14, [
    "Whatever the war's outcome on the continent, North Point's part in it is already clear. The islands fed, repaired, sheltered and supplied the allied forces from their own harbours and runways, without surrendering their own government or their own voice.",
    "When the war ends, the allied squadrons will fly home and the staff officers will pack their maps. The berths, the hangars and the habits of islands that learned to carry more than their size will stay."],
  "add_stability = 0.05\nadd_war_support = 0.05\n" + RECOVERY, ("medal", "runway"), "late",
  pre=[["harbour_town_strangers"]], available="date > 2004.12.31", ai="factor = 80")

F("internment_convention", "The Internment Convention", 76, 11, [
    "Under the old rules of neutrality, any armed aircraft or warship that takes refuge in a neutral's territory during a war must be interned until the fighting ends. The government publishes the rules, prepares the camps and informs every embassy, so that nobody can claim surprise.",
    "The camps stand empty and the rules gather dust. Both, the government says, are working exactly as intended."],
  "army_experience = 10\nadd_stability = 0.02", ("document", "gate"), "late", pre=[["neutral_waters"]], ai="factor = 60")

F("neutral_hospital_berths", "Neutral Hospital Berths", 80, 11, [
    "North Point's harbours will receive hospital ships of any flag, under the islands' inspection. Whoever is hurt in the continent's quarrels will be treated in the same wards by the same doctors.",
    "The arrangement depends entirely on everyone believing that the islands are truly neutral. The government is careful to give nobody a reason to doubt it."],
  "add_political_power = 30\nadd_stability = 0.02", ("medical", "peace"), "late", pre=[["neutral_waters"]],
  ai="factor = 60")

F("neutral_ground", "Neutral Ground", 78, 12, [
    "Diplomats from quarrelling governments cannot meet on the continent without one side or the other feeling threatened. North Point offers its customs hall, its guarantees and its discretion for talks of any kind: prisoners, corridors, perhaps one day a settlement.",
    "No government accepts at first. Then a request arrives, unsigned and through a third embassy, for a quiet meeting."],
  "country_event = { id = ac_ud_npt.21 }", ("diplomacy", "peace"), "late",
  pre=[["internment_convention", "neutral_hospital_berths"]], ai="factor = 60", event=21)

F("armed_watch", "Armed Watch on the Straits", 82, 12, [
    "Neutrality that cannot defend itself is an invitation. The coast watch, the fleet and the air squadrons stand ready to intercept any aircraft or warship, of any side, that violates the islands' waters.",
    "The first interception is an unidentified reconnaissance aircraft that turns away when island fighters appear on its wing. The government does not say whose aircraft it was."],
  "air_experience = 15\nnavy_experience = 10\nadd_war_support = 0.03", ("air", "radar"), "late",
  pre=[["neutral_hospital_berths"]], ai="factor = 60")

F("neutral_to_the_end", "Neutral to the End", 80, 13, [
    "Whatever has happened on the continent, it has happened without North Point. The islands' harbours sheltered the shipwrecked and the displaced, their camps stood ready, and their diplomats carried messages nobody else could carry.",
    "It has not made the islands popular. It has made them trusted, which may prove the more valuable thing."],
  "add_stability = 0.05\nadd_political_power = 50", ("peace", "medal"), "late", pre=[["neutral_ground"], ["armed_watch"]],
  available="date > 2004.12.31", ai="factor = 60")

F("islands_take_stock", "The Islands Take Stock", 74, 15, [
    "Fourteen years have passed since the ballot boxes came ashore on the morning ferries in 1991. In that time North Point has argued about its government, built and rebuilt its economy, prepared for the fall of Ulysses, lived through its aftermath and watched the continent's quarrels from closer than it ever wished.",
    "The islands are not what they were. The government commissions a review of everything that has changed, and the islands, as always, hear it on the evening broadcast and argue about it on the morning ferries."],
  "add_stability = 0.03\ncountry_event = { id = ac_ud_npt.22 }", ("document", "peace"), "late",
  pre=[["islands_carried_the_load", "neutral_to_the_end"]], available="date > 2005.1.1", ai="factor = 80", event=22)


# ---------------------------------------------------------------- ideas (provisional gameplay values)
Idea = namedtuple("Idea", "ident title desc modifiers glyph")
IDEAS = [
    Idea("NPT_ud_compact_stratocracy_spirit", "The Subdivision Compact",
         "The division of powers between the National Defense Council and the subdivision governments is written down at last. Disputes go to a joint hearing instead of a telephone call.",
         {"drift_defence_factor": 0.25, "political_power_gain": -0.05, "war_support_factor": 0.05, "democratic_drift": 0.005}, "scales"),
    Idea("NPT_ud_chartered_council_spirit", "The Council Charter",
         "A military government that has written down the limits of its own authority, and publishes what it does within them.",
         {"drift_defence_factor": 0.30, "stability_factor": 0.05, "political_power_gain": 0.05, "war_support_factor": 0.05}, "document"),
    Idea("NPT_ud_merit_boards_spirit", "Merit Boards",
         "Promotion examinations are held in public halls on every island, and the results are posted the next morning.",
         {"experience_gain_army_factor": 0.10, "army_org_factor": 0.03}, "training"),
    Idea("NPT_ud_council_seniority_spirit", "Seniority on the Council",
         "Council seats pass to the longest-serving officers of each service.",
         {"stability_factor": 0.04, "war_support_factor": 0.03}, "medal"),
    Idea("NPT_ud_council_rotation_spirit", "Rotation by Merit",
         "Council seats rotate on fixed terms among officers who have passed the merit boards and served in a subdivision post.",
         {"political_power_gain": 0.10, "research_speed_factor": 0.02, "stability_factor": -0.02}, "scales"),
    Idea("NPT_ud_island_parliament_spirit", "The Parliament of the Islands",
         "Foreign and defence affairs answer to a cabinet responsible to an elected parliament. Provisional alternate history.",
         {"stability_factor": 0.03, "political_power_gain": 0.05, "drift_defence_factor": 0.10, "opinion_gain_monthly_factor": 0.10}, "assembly"),
    Idea("NPT_ud_civilian_defence_spirit", "A Civilian Ministry of Defence",
         "The Defense Forces report to a civilian minister. The islands still defend every shore, but no longer pretend the continent does not exist.",
         {"army_core_defence_factor": 0.05, "opinion_gain_monthly_factor": 0.15, "stability_factor": 0.03}, "civil"),
    Idea("NPT_ud_rights_charter_spirit", "The Charter of Island Rights",
         "Every island keeps its council, every citizen may petition, and the harbours stay open to anyone in distress.",
         {"stability_factor": 0.05, "drift_defence_factor": 0.15}, "peace"),
    Idea("NPT_ud_readiness_state_spirit", "The Readiness Directorate",
         "The subdivisions' budgets, ports and roads answer to a single defence plan. Provisional alternate history.",
         {"political_power_gain": 0.10, "stability_factor": -0.03, "war_support_factor": 0.10, "conscription_factor": 0.05}, "command"),
    Idea("NPT_ud_national_service_spirit", "Universal National Service",
         "Every citizen serves in the Defense Forces, the coast watch or the civil defence corps.",
         {"conscription_factor": 0.15, "training_time_army_factor": -0.10, "stability_factor": -0.02}, "training"),
    Idea("NPT_ud_professional_cadre_spirit", "A Professional Cadre",
         "A small, long-serving and well-paid defence force.",
         {"army_org_factor": 0.05, "experience_gain_army_factor": 0.10}, "medal"),
    Idea("NPT_ud_hedgehog_islands_spirit", "The Hedgehog Doctrine",
         "Every island is a separate fortress that must be taken separately.",
         {"army_core_defence_factor": 0.15, "army_core_attack_factor": 0.10, "enemy_justify_war_goal_time": 0.30,
          "opinion_gain_monthly_factor": -0.25, "stability_factor": 0.05}, "security"),
    Idea("NPT_ud_harbour_yards_spirit", "The Harbour Yards",
         "The ship-repair yards have become shipyards able to build for the islands.",
         {"production_speed_dockyard_factor": 0.15, "industrial_capacity_dockyard": 0.05}, "navy"),
    Idea("NPT_ud_airframe_workshops_spirit", "The Airframe Workshops",
         "Overhaul hangars that rebuild engines, airframes and radar sets on the islands.",
         {"production_speed_air_base_factor": 0.20, "experience_gain_air_factor": 0.10, "industrial_capacity_factory": 0.03}, "air"),
    Idea("NPT_ud_self_sufficient_islands_spirit", "Self-Sufficient Islands",
         "A civil works programme carries new industrial skills to the outer islands.",
         {"consumer_goods_factor": -0.02, "production_factory_max_efficiency_factor": 0.05}, "industry"),
    Idea("NPT_ud_island_industry_spirit", "An Industry That Can Stand Alone",
         "Yards, workshops, canneries and depots form one island economy.",
         {"consumer_goods_factor": -0.03, "production_factory_max_efficiency_factor": 0.08, "production_speed_buildings_factor": 0.05}, "rebuild"),
    Idea("NPT_ud_coastal_fleet_spirit", "A Coastal Defence Fleet",
         "Torpedo boats, minelayers and submarines that make every approach to the islands a gamble.",
         {"naval_damage_factor": 0.05, "navy_org_factor": 0.05}, "submarine"),
    Idea("NPT_ud_escort_fleet_spirit", "An Ocean Escort Fleet",
         "Frigates and oilers trained to bring a tanker convoy through hostile water.",
         {"naval_coordination": 0.10, "naval_speed_factor": 0.05}, "logistics"),
    Idea("NPT_ud_shelter_programme_spirit", "The Shelter Programme",
         "Every island is preparing for the fall of Ulysses. The work steadies nerves and strains budgets.",
         {"stability_factor": 0.03, "war_support_factor": 0.02, "consumer_goods_factor": 0.02}, "shelter"),
    Idea("NPT_ud_relief_harbour_spirit", "Open Harbours",
         "Anyone who reaches North Point by sea is fed, sheltered and registered.",
         {"stability_factor": -0.02, "political_power_gain": -0.05, "opinion_gain_monthly_factor": 0.20, "monthly_population": 0.05}, "refugees"),
    Idea("NPT_ud_registered_quota_spirit", "A Registered Quota",
         "Refugees are admitted up to a monthly quota; boats beyond it are supplied and escorted onward.",
         {"stability_factor": 0.02, "political_power_gain": 0.03, "opinion_gain_monthly_factor": 0.05}, "scales"),
    Idea("NPT_ud_allied_rear_services_spirit", "Allied Rear Services",
         "The islands' yards, hangars and hospitals work for the allied forces. Official framing: ACES Chronicle, 2004 / 09.16; the values are provisional gameplay.",
         {"production_speed_air_base_factor": 0.15, "supply_consumption_factor": -0.05, "war_support_factor": 0.05}, "runway"),
    Idea("NPT_ud_neutral_waters_spirit", "Neutral Waters",
         "Open to ships in distress, closed to fleets at war.",
         {"enemy_justify_war_goal_time": 0.25, "stability_factor": 0.05, "opinion_gain_monthly_factor": 0.10}, "peace"),
]

# ---------------------------------------------------------------- unnamed offices and government changes
Office = namedtuple("Office", "slug title desc sub_ideology glyph")
OFFICES = [
    Office("island_cabinet", "Provisional Cabinet of the Islands",
           "The cabinet answerable to the Parliament of the Islands. It governs as an office until the islands elect a government of their own. Unnamed office leader; provisional alternate history.",
           "liberalism", "assembly"),
    Office("readiness_directorate", "The Readiness Directorate",
           "The office through which the Reformist officers govern North Point. Its orders carry a seal, not a name. Unnamed office leader; provisional alternate history.",
           "stratocracy_fascism", "command"),
]

# (slug, ruling party, office slug, sub-ideology, elections allowed, placeholder popularities)
REGIMES = [
    ("parliament", "democratic", "island_cabinet", "liberalism", True,
     {"democratic": 52, "neutrality": 33, "fascism": 12, "communism": 3}),
    ("directorate", "fascism", "readiness_directorate", "stratocracy_fascism", False,
     {"fascism": 46, "neutrality": 38, "democratic": 14, "communism": 2}),
]

# Readable labels for every flag and variable this package sets or reads.
LABELS = {
    "NPT_ud_path_council": "The Council Endures path chosen",
    "NPT_ud_path_parliament": "The Parliament of the Islands path chosen",
    "NPT_ud_path_directorate": "The Readiness Directorate path chosen",
    "NPT_ud_convention_federal": "The convention chose a federal compact",
    "NPT_ud_convention_unitary": "The convention chose a single electoral roll",
    "NPT_ud_ulysses_brief": "The islands have been briefed on Ulysses",
    "NPT_ud_shelters_deep": "Shelters dug under the headlands",
    "NPT_ud_shelters_dispersed": "Shelters dispersed across every village",
    "NPT_ud_after_impact": "The islands have emerged from the shelters",
    "NPT_ud_harbours_open": "The harbours are open to refugees",
    "NPT_ud_harbours_quota": "The harbours admit refugees by quota",
    "NPT_ud_lane_allied": "North Point serves as the allied rear base",
    "NPT_ud_lane_neutral": "North Point keeps its waters neutral",
    "NPT_ud_shelter_readiness": "Shelter readiness",
    "ac_ucw_calendar_started": "The Continental War calendar has begun",
}

# Scripted effects owned by this package (besides the regime effects).
EFFECTS = {
    "ac_ud_npt_shelter_progress": (
        "add_to_variable = { NPT_ud_shelter_readiness = 1 }\n"
        "clamp_variable = { var = NPT_ud_shelter_readiness min = 0 max = 12 }"),
    "ac_ud_npt_refresh_budget": "if = { limit = { ac_econ_ready = yes } ac_econ_refresh_budget = yes }",
    "ac_ud_npt_fund_programme": "if = { limit = { ac_econ_ready = yes } ac_econ_pay_programme = yes ac_econ_refresh_budget = yes }",
    "ac_ud_npt_war_recovery": (
        "if = { limit = { ac_ucw_active = yes has_variable = ac_ucw_recovery } add_to_variable = { ac_ucw_recovery = 3 } ac_ucw_bound = yes }"),
    "ac_ud_npt_capital_air_base": "capital_scope = { add_building_construction = { type = air_base level = 1 instant_build = yes } }",
    "ac_ud_npt_capital_infrastructure": "capital_scope = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }",
    "ac_ud_npt_capital_radar": "capital_scope = { add_building_construction = { type = radar_station level = 1 instant_build = yes } }",
    "ac_ud_npt_build_infrastructure": (
        "random_owned_controlled_state = { limit = { is_coastal = yes } "
        "add_building_construction = { type = infrastructure level = 1 instant_build = yes } }"),
}
for _kind in ("civilian", "arms", "dockyard", "fuel"):
    _type = {"civilian": "industrial_complex", "arms": "arms_factory", "dockyard": "dockyard", "fuel": "fuel_silo"}[_kind]
    EFFECTS["ac_ud_npt_build_" + _kind] = (
        "random_owned_controlled_state = { limit = { is_coastal = yes } add_extra_state_shared_building_slots = 1 "
        "add_building_construction = { type = %s level = 1 instant_build = yes } }" % _type)
