"""Central Usea (FCU) Usea Depth rows: focuses, ideas, flags and tooltips.

Every row names its source layer. Official rows cite the ACES Chronicle
(https://acecombat.jp/en/chronicle/details/, read for the Continental War
ledger on 27 October 2026 and 3 November 2026) as "Chronicle, YYYY / MM.DD",
or the Super Weapons page (https://acecombat.jp/en/chronicle/weapons/).
UTO, CNEA, the 1991 faction and the 1991 Sinclair term are mod provenance.
Everything else, including both regime paths, is provisional gameplay.

Placement: the opening tree (ac_exp_fcu_opening) uses x <= 23 and y >= 6.
The war tree (ac_ucw_fcu_tree) uses x 42-94.
"""
from dataclasses import dataclass

OPENING = "ac_exp_fcu_opening"
WAR = "ac_ucw_fcu_tree"
OPENING_GUARD = "date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started }"
CHRONICLE = "https://acecombat.jp/en/chronicle/details/"
WEAPONS = "https://acecombat.jp/en/chronicle/weapons/"


@dataclass
class Focus:
    id: str
    tree: str
    section: str
    x: int
    y: int
    title: str
    desc: str
    reward: str = ""
    pre: tuple = ()
    excl: tuple = ()
    cost: int = 5
    ai: int = 10
    gate: str = ""
    subj: tuple = ("assembly", "document")
    layer: str = "Provisional gameplay"
    cite: str = ""
    regime: str = ""


FOCUSES = []
_SECTION = [None, None]


def section(name, tree):
    _SECTION[:] = [name, tree]


def full(slug):
    return slug if slug.startswith("FCU_") else "FCU_ud_" + slug


def F(slug, x, y, title, desc, reward="", pre="", excl="", cost=5, ai=10, gate="", subj="assembly document",
      layer="Provisional gameplay", cite="", regime=""):
    """pre: ',' separates AND groups and '|' separates OR alternatives."""
    groups = tuple(tuple(full(p) for p in group.split("|")) for group in pre.split(",") if group)
    FOCUSES.append(Focus(full(slug), _SECTION[1], _SECTION[0], x, y, title, desc, reward, groups,
                         tuple(full(e) for e in excl.split("|") if e), cost, ai, gate, tuple(subj.split()), layer, cite, regime))


# ----------------------------------------------------------------- reward helpers
def R(*parts):
    return "\n".join(p for p in parts if p)


def idea(name):
    return "add_ideas = FCU_ud_" + name + "_idea"


def drop(name):
    return "remove_ideas = FCU_ud_" + name + "_idea"


def timed(name, days):
    return "add_timed_idea = { idea = FCU_ud_%s_idea days = %d }" % (name, days)


def flag(name):
    return "set_country_flag = FCU_ud_" + name


def clear(name):
    return "clr_country_flag = FCU_ud_" + name


def ev(number):
    return "country_event = { id = ac_ud_fcu.%d days = 1 }" % number


def pp(n):
    return "add_political_power = %d" % n


def stab(v):
    return "add_stability = %s" % v


def ws(v):
    return "add_war_support = %s" % v


def army(n):
    return "army_experience = %d" % n


def air(n):
    return "air_experience = %d" % n


def navy(n):
    return "navy_experience = %d" % n


def manpower(n):
    return "add_manpower = %d" % n


def tech(category, bonus=0.5):
    # %ID% is replaced with the focus ID, which also names the bonus.
    return "add_tech_bonus = { name = %%ID%% bonus = %s uses = 1 category = %s }" % (bonus, category)


def ready(n):
    """Evacuation readiness (0-100): FCU's own index, read once at the 1999 impact."""
    return "ac_ud_fcu_readiness_init = yes\nadd_to_variable = { FCU_ud_readiness = %d }\nac_ud_fcu_bound = yes" % n


def recovery(n):
    """The Continental War recovery index belongs to the UCW owner; only add when it exists."""
    return "if = { limit = { has_variable = ac_ucw_recovery } add_to_variable = { ac_ucw_recovery = %d } ac_ucw_bound = yes }" % n


def fiscal(effect):
    return "if = { limit = { ac_econ_ready = yes } %s = yes }" % effect


def regime(slug):
    return "ac_ud_fcu_regime_%s = yes" % slug


# ----------------------------------------------------------------- gates
WARNING = "date > 1996.4.19"                       # Chronicle, 1996 / 04.20
SKULLY = "has_country_flag = ac_ur_skully_recorded"  # Chronicle, 1995 / 12.31 (set by ac_ur on_actions)
COUP = "has_country_flag = ac_ur_coup_started"       # Chronicle, 1997 / 05.30 (set by ac_ur on_actions)
STONEHENGE_DONE = "OR = { has_global_flag = ac_sp_stonehenge_complete date > 1998.6.18 }"  # Chronicle, 1998 / 06.19
IMPACT = "date > 1999.7.7"                         # Chronicle, 1999 / 07.08
GOV_DIRECTORATE = "has_country_flag = FCU_ud_gov_directorate"
GOV_UNITY = "has_country_flag = FCU_ud_gov_unity"
GOV_FEDERAL = "NOT = { has_country_flag = FCU_ud_gov_directorate } NOT = { has_country_flag = FCU_ud_gov_unity }"


def brief(name):
    return "OR = { has_global_flag = ac_ucw_brief_%s has_global_flag = ac_ucw_brief_%s_done }" % (name, name)


ALT = "Alternate history"   # regime paths: player-only, labelled in every description


# =================================================================== OPENING TREE
section("politics", OPENING)
F("federal_question", 4, 6, "The Federal Question",
  "The Federation enters the decade with a presidency, an Assembly and a treaty bloc that all claim to speak for Central Usea. Before the cabinet can plan anything larger, it must decide how the Federation will be governed when the next emergency comes.",
  R(flag("politics_open"), pp(25), ev(1)), ai=30, subj="assembly ballot")
F("hold_course", 0, 7, "Hold the Federal Course",
  "Keep the government the Federation already has. The presidency governs with the Assembly as it did in 1991, and every reform passes through the ordinary calendar.",
  R(flag("path_course"), idea("federal_course")), pre="federal_question", excl="emergency_powers|unity_talks", ai=40, subj="assembly document")
F("emergency_powers", 4, 7, "Draft Emergency Powers",
  "A faction of the cabinet and the staff argues that a federation this large cannot answer a continental emergency through committees. It asks for a legal framework that hands day-to-day authority to a military directorate when a crisis is declared.",
  R(flag("path_directorate"), idea("emergency_framework"), ev(2)), pre="federal_question", excl="hold_course|unity_talks", ai=0,
  subj="command security", layer=ALT)
F("unity_talks", 8, 7, "Open All-Party Talks",
  "Invite every party in the Assembly into talks on a cabinet of national unity. Broad consent is slower, but a government that includes its rivals cannot easily be brought down by them.",
  R(flag("path_unity"), pp(-25), ev(3)), pre="federal_question", excl="hold_course|emergency_powers", ai=0,
  subj="diplomacy ballot", layer=ALT)

# Status quo: the AI path. The 1991 government stays in office.
F("cabinet_continuity", 0, 8, "Cabinet Continuity",
  "Ministers keep their portfolios and their senior officials. The cabinet trades the attention of a reshuffle for a year of uninterrupted administration.",
  R(pp(40), stab(0.02)), pre="hold_course", ai=30, subj="assembly communications")
F("assembly_calendar", 0, 9, "The Assembly Calendar",
  "Publish a legislative calendar for the session so that the Assembly knows which bills the presidency will bring and when. Predictable business lowers the temperature of every debate.",
  R(stab(0.02), pp(15)), pre="cabinet_continuity", ai=30, subj="document assembly")
F("presidential_decrees", 0, 10, "Presidential Decree Programme",
  "Use the presidency's existing decree authority for administrative matters and keep the Assembly for legislation. Faster, but the opposition will call it government by signature.",
  R(timed("decree_programme", 365), pp(30)), pre="assembly_calendar", excl="assembly_partnership", ai=10, subj="document command")
F("assembly_partnership", 2, 10, "Assembly Partnership",
  "Bring the Assembly's committee chairs into the drafting of every major bill. Slower, but the bills that pass are not reopened after the next quarrel.",
  R(timed("assembly_partnership", 365), stab(0.02)), pre="assembly_calendar", excl="presidential_decrees", ai=30, subj="assembly diplomacy")
F("federal_budget_law", 1, 11, "Federal Budget Law",
  "A multi-year budget law fixes what the federal treasury owes the regions and what the regions owe in return. Most of the Federation's quarrels are about money; this one is settled in writing.",
  R(pp(20), stab(0.02), fiscal("ac_econ_refresh_budget")), pre="presidential_decrees|assembly_partnership", ai=30, subj="scales economy")
F("regional_governors", 1, 12, "Regional Governors' Conference",
  "Gather the regional governments in a standing annual conference with the presidency. Grievances that used to reach the press first now reach a table first.",
  R(stab(0.03), pp(-15)), pre="federal_budget_law", ai=25, subj="assembly diplomacy")
F("civil_service_review", 1, 13, "Civil Service Review",
  "A review of the federal civil service merges duplicated offices and publishes the posts that remain. It costs some goodwill among officials and returns a faster administration.",
  R(tech("industry", 0.5), pp(25)), pre="regional_governors", ai=25, subj="document tools")
F("ministry_of_preparedness", 0, 14, "Ministry of Preparedness",
  "After the Ulysses warning, give one ministry the authority and the budget to prepare the whole Federation. One minister answers for every shelter, timetable and stockpile.",
  R(idea("ministry_of_preparedness"), ready(6)), pre="civil_service_review", excl="interagency_board", gate=WARNING, ai=25, subj="civil assembly")
F("interagency_board", 2, 14, "Interagency Emergency Board",
  "After the Ulysses warning, leave each ministry its own duties and coordinate them through a board that meets daily. No new ministry, and no single point of failure.",
  R(idea("interagency_board"), ready(4), pp(20)), pre="civil_service_review", excl="ministry_of_preparedness", gate=WARNING, ai=10, subj="command communications")
F("continuity_of_government", 1, 15, "Continuity of Government",
  "Write down who governs if the capital cannot. Alternate seats, a line of succession for every ministry and copies of the federal records stored away from the coast.",
  R(stab(0.03), ready(4)), pre="ministry_of_preparedness|interagency_board", gate=WARNING, ai=25, subj="shelter document")
F("address_to_the_federation", 1, 16, "An Address to the Federation",
  "After the coup of 30 May 1997, the presidency speaks to the whole Federation: what failed, what held, and what the government will change. The speech is short and the promises are specific.",
  R(stab(0.04), ws(0.02)), pre="continuity_of_government", gate=COUP, ai=25, subj="communications assembly",
  cite="Chronicle, 1997 / 05.30")
F("course_held", 1, 17, "The Course Held",
  "The Federation has met the decade's emergencies with the government it chose in 1991. The cabinet records the course it held and prepares the account it will give to the next century.",
  R(stab(0.03), pp(40), ev(4)), pre="address_to_the_federation", gate="date > 1998.6.18", ai=30, subj="assembly medal")

# Emergency Unified Command directorate: player-only alternate history.
F("emergency_statute", 4, 8, "The Emergency Statute",
  "Draft the statute: who may declare a continental emergency, for how long, and what passes to the directorate when they do. Every article is argued over twice.",
  R(pp(30), flag("emergency_statute_drafted")), pre="emergency_powers", ai=0, subj="document security", layer=ALT)
F("command_liaison", 4, 9, "Unified Command Liaison",
  "Station cabinet liaison officers with Unified Command's staff so that a future directorate would not have to learn the ministries in the middle of a crisis.",
  R(army(15), pp(-15)), pre="emergency_statute", ai=0, subj="command communications", layer=ALT)
F("staff_directorate", 4, 10, "A Staff Directorate",
  "Model the directorate on a military staff: a small number of officers with clear lines of command and civilian ministers who carry out their orders.",
  R(timed("staff_directorate", 730), army(10)), pre="command_liaison", excl="civil_military_board", ai=0, subj="command training", layer=ALT)
F("civil_military_board", 6, 10, "A Civil-Military Board",
  "Model the directorate as a board: officers and senior civilians in equal number, deciding by majority. Slower than a staff, but harder to accuse of seizing the state.",
  R(timed("civil_military_board", 730), stab(0.02)), pre="command_liaison", excl="staff_directorate", ai=0, subj="assembly command", layer=ALT)
F("emergency_threshold", 5, 11, "The Emergency Threshold",
  "The statute is ready, but it needs an emergency. A rebellion in the southern islands or the warning about Ulysses would meet the threshold the drafters wrote.",
  R(pp(25), ws(0.03)), pre="staff_directorate|civil_military_board", gate="OR = { %s %s }" % (SKULLY, WARNING), ai=0,
  subj="meteor security", layer=ALT)
F("proclaim_directorate", 5, 12, "Proclaim the Directorate",
  "Declare the continental emergency and transfer executive authority to a directorate built around Unified Command. The presidency and the Assembly remain, but they no longer govern.",
  R(regime("directorate"), flag("gov_directorate"), flag("directorate_proclaimed"), drop("emergency_framework"),
    idea("directorate_rule"), ev(5)),
  pre="emergency_threshold", cost=10, ai=0, subj="command assembly", layer=ALT, regime="directorate")
F("martial_evacuation_law", 4, 13, "Martial Evacuation Law",
  "Place the evacuation programme under military law. Movement orders become binding, requisitions are immediate, and appeals wait until afterwards.",
  R(timed("martial_evacuation", 730), ready(10), stab(-0.03)), pre="proclaim_directorate", excl="civil_compact", ai=0,
  subj="refugees security", layer=ALT)
F("civil_compact", 6, 13, "The Civil Compact",
  "Promise in writing that the directorate will not use its authority against lawful parties, newspapers or courts. The officers lose some speed and keep some trust.",
  R(stab(0.04), pp(-20), ready(4)), pre="proclaim_directorate", excl="martial_evacuation_law", ai=0, subj="scales document", layer=ALT)
F("emergency_information_board", 5, 14, "Emergency Information Board",
  "One board issues every public announcement about the emergency. It ends the contradictory bulletins and also ends the newspapers' habit of asking questions first.",
  R(ws(0.03), stab(0.02)), pre="martial_evacuation_law|civil_compact", ai=0, subj="communications command", layer=ALT)
F("district_councils", 5, 15, "District Councils",
  "The directorate governs the regions through councils that pair a district commander with the regional administration. Orders arrive faster; local politics does not disappear.",
  R(pp(30), army(10)), pre="emergency_information_board", ai=0, subj="assembly security", layer=ALT)
F("loyalty_reviews", 4, 16, "Loyalty Reviews",
  "After 30 May 1997 the directorate reviews every officer who served in a command that went silent. It finds what it looks for, and the corps learns what is being looked for.",
  R(timed("loyalty_reviews", 365), army(15), stab(-0.02)), pre="district_councils", excl="directorate_amnesty", gate=COUP, ai=0,
  subj="security document", layer=ALT)
F("directorate_amnesty", 6, 16, "The Directorate's Amnesty",
  "After 30 May 1997 the directorate offers an amnesty to officers who surrender their commands and give evidence. A government built on Unified Command cannot afford to fight its own corps for long.",
  R(stab(0.03), manpower(5000)), pre="district_councils", excl="loyalty_reviews", gate=COUP, ai=0,
  subj="peace security", layer=ALT)
F("directorate_review", 5, 17, "The Directorate Review",
  "The statute required a review once the emergency eased. With Stonehenge complete and the evacuation plans in place, the directorate must account for itself.",
  R(pp(20), ev(6)), pre="loyalty_reviews|directorate_amnesty", gate="date > 1998.6.18", ai=0, subj="scales command", layer=ALT)
F("return_authority", 4, 18, "Return Authority to the Assembly",
  "End the emergency before Ulysses arrives and return executive authority to the presidency and the Assembly. The directorate's staff goes back to Unified Command.",
  R(regime("restoration"), clear("gov_directorate"), flag("gov_restored"), flag("authority_returned"), drop("directorate_rule"),
    idea("restored_assembly"), ev(7)),
  pre="directorate_review", excl="extend_directorate", cost=10, ai=0, subj="ballot assembly", layer=ALT, regime="restoration")
F("extend_directorate", 6, 18, "Extend the Directorate",
  "Ulysses has not yet arrived and the emergency is not over. Renew the directorate's mandate until the danger has passed, whenever that is.",
  R(flag("directorate_extended"), drop("directorate_rule"), idea("extended_directorate"), ws(0.03), ev(8)),
  pre="directorate_review", excl="return_authority", ai=0, subj="command meteor", layer=ALT)

# Federal unity government: player-only alternate history.
F("cross_bench_compact", 8, 8, "The Cross-Bench Compact",
  "A written compact between the presidency and every Assembly party: no motions of no confidence while the talks last, and no cabinet appointments without consultation.",
  R(stab(0.03), pp(-20)), pre="unity_talks", ai=0, subj="document diplomacy", layer=ALT)
F("coalition_arithmetic", 8, 9, "Coalition Arithmetic",
  "Count the portfolios, count the parties and count the regions. Every cabinet seat has to satisfy at least two of the three.",
  R(pp(30)), pre="cross_bench_compact", ai=0, subj="scales assembly", layer=ALT)
F("regional_ministers", 8, 10, "Regional Ministers",
  "Fill the unity cabinet with ministers who answer to the regions. The Federation will be governed by people the provinces already trust.",
  R(timed("regional_ministers", 730), stab(0.03)), pre="coalition_arithmetic", excl="technocratic_ministers", ai=0,
  subj="assembly civil", layer=ALT)
F("technocratic_ministers", 10, 10, "Technocratic Ministers",
  "Fill the unity cabinet's key ministries with officials and specialists who belong to no party. The parties keep the vote; the experts keep the files.",
  R(timed("technocratic_ministers", 730), tech("electronics", 0.5)), pre="coalition_arithmetic", excl="regional_ministers", ai=0,
  subj="science assembly", layer=ALT)
F("form_unity_government", 9, 11, "Form the Unity Government",
  "Dissolve the cabinet and swear in a government of national unity. Its office answers to the whole Assembly; the old majority becomes one partner among several.",
  R(regime("unity"), flag("gov_unity"), flag("unity_formed"), idea("unity_cabinet"), ev(9)),
  pre="regional_ministers|technocratic_ministers", cost=10, ai=0, subj="assembly ballot", layer=ALT, regime="unity")
F("unity_programme", 9, 12, "The Unity Programme",
  "Publish the unity government's programme: one page, five commitments, signed by every party leader in the cabinet.",
  R(stab(0.03), pp(25)), pre="form_unity_government", ai=0, subj="document ballot", layer=ALT)
F("burden_sharing_act", 8, 13, "The Burden-Sharing Act",
  "Spread the cost of preparedness across every region by a fixed formula. Richer provinces pay more and are allowed to say so.",
  R(timed("burden_sharing", 730), fiscal("ac_econ_refresh_budget")), pre="unity_programme", excl="regional_autonomy_charter", ai=0,
  subj="scales economy", layer=ALT)
F("regional_autonomy_charter", 10, 13, "Regional Autonomy Charter",
  "Hand the regions more control over their own preparedness budgets. The centre loses leverage and gains partners who own their results.",
  R(timed("regional_autonomy", 730), stab(0.02)), pre="unity_programme", excl="burden_sharing_act", ai=0, subj="assembly civil", layer=ALT)
F("continental_hearings", 9, 14, "Continental Hearings",
  "After the Ulysses warning, the unity cabinet holds open hearings in every region on the preparedness plans. Ministers listen first and then answer.",
  R(stab(0.03), ready(6)), pre="burden_sharing_act|regional_autonomy_charter", gate=WARNING, ai=0, subj="assembly communications", layer=ALT)
F("unity_emergency_cabinet", 9, 15, "Unity Emergency Cabinet",
  "A small emergency cabinet drawn from every party meets daily on Ulysses preparations. Rival parties sit at the same table and share the same briefing.",
  R(timed("unity_emergency_cabinet", 730), ready(6)), pre="continental_hearings", gate=WARNING, ai=0, subj="civil command", layer=ALT)
F("defend_the_assembly", 8, 16, "Defend the Assembly",
  "After 30 May 1997 every party in the unity cabinet signs a declaration in support of the Assembly. Officers who backed the coup find no politician willing to speak for them.",
  R(stab(0.04), ws(0.02)), pre="unity_emergency_cabinet", excl="reconciliation_committee", gate=COUP, ai=0, subj="assembly security", layer=ALT)
F("reconciliation_committee", 10, 16, "Reconciliation Committee",
  "After 30 May 1997 the unity cabinet forms an all-party committee to hear the officers' grievances once the rebellion is defeated. Complaints are heard; mutiny is not excused.",
  R(stab(0.02), army(10), manpower(4000)), pre="unity_emergency_cabinet", excl="defend_the_assembly", gate=COUP, ai=0, subj="peace scales", layer=ALT)
F("unity_mandate", 9, 17, "The Unity Mandate",
  "The parties renew the unity government for the years of the impact. It was formed for an emergency; the emergency is still coming.",
  R(pp(30), ev(10)), pre="defend_the_assembly|reconciliation_committee", ai=0, subj="ballot assembly", layer=ALT)
F("constitutional_settlement", 9, 18, "Constitutional Settlement",
  "Write the unity government's practice into the constitution: a cabinet drawn from the whole Assembly whenever a continental emergency is declared.",
  R(stab(0.03), pp(30)), pre="unity_mandate", ai=0, subj="document scales", layer=ALT)

# Closing focuses shared by every path.
F("federal_settlement", 5, 20, "The Federal Settlement",
  "Whichever government carried the Federation through the decade, its record now has to be settled: what powers remain, which emergency laws expire, and what the next century inherits.",
  R(pp(50), ev(11)), pre="course_held|return_authority|extend_directorate|constitutional_settlement", ai=30,
  subj="scales assembly")
F("open_archives", 3, 21, "Open the Federal Archives",
  "Publish the decade's cabinet papers, emergency orders included, after a short review. The Federation learns what was decided in its name.",
  R(stab(0.03), pp(-25), flag("archives_opened")), pre="federal_settlement", excl="seal_records", ai=30, subj="document communications")
F("seal_records", 7, 21, "Seal the Emergency Records",
  "Seal the decade's emergency papers for thirty years. Officials keep their candour, and critics keep their suspicions.",
  R(pp(40), stab(-0.01), flag("records_sealed")), pre="federal_settlement", excl="open_archives", ai=10, subj="security document")
F("politics_handover", 5, 22, "A Government for the New Century",
  "The cabinet prepares a handover brief for whoever governs in 2000: the laws in force, the emergencies still open and the promises not yet kept.",
  R(stab(0.02), pp(30)), pre="open_archives|seal_records", ai=25, subj="assembly document")

section("economy", OPENING)
F("federal_economy", 5, 24, "The Federal Economy",
  "Central Usea is the continent's largest economy and its largest treasury. The cabinet must decide whether to grow it through open trade or through federal industry.",
  R(pp(20), ev(27)), ai=25, subj="economy industry")
F("continental_trade", 3, 25, "Continental Trade Programme",
  "Lower the Federation's tariffs on its treaty partners and open federal contracts to their firms. Usean trade binds Usean partners.",
  R(idea("continental_trade")), pre="federal_economy", excl="federal_industry", ai=25, subj="economy diplomacy")
F("federal_industry", 7, 25, "Federal Industrial Policy",
  "Direct federal credit to the industries the Federation would need in an emergency: steel, heavy engineering, aircraft and power.",
  R(idea("federal_industry")), pre="federal_economy", excl="continental_trade", ai=10, subj="industry economy")
F("open_the_ports", 3, 26, "Open the Ports",
  "Modernise the federal ports for container traffic and simplify customs for treaty members. The harbours become the Federation's busiest workplaces.",
  R(tech("industry", 0.5), navy(5)), pre="continental_trade", ai=25, subj="navy economy")
F("strategic_plants", 7, 26, "Strategic Plants",
  "Fund a short list of strategic plants that can switch to emergency production. Each one keeps a reserve line idle and ready.",
  R(tech("industry", 0.75)), pre="federal_industry", ai=10, subj="industry tools")
F("currency_board", 5, 27, "Federal Currency Board",
  "An independent board defends the federal currency. Treaty partners that price their trade in it can rely on its value.",
  R(stab(0.02), pp(20), fiscal("ac_econ_refresh_budget")), pre="open_the_ports|strategic_plants", ai=25, subj="scales economy")
F("ulysses_bonds", 3, 28, "Ulysses Bonds",
  "After the Ulysses warning, finance the preparations with long-dated federal bonds sold to citizens and partners. The cost is deferred to the generation that survives.",
  R(timed("ulysses_bonds", 1095), ready(4)), pre="currency_board", excl="emergency_levy", gate=WARNING, ai=25, subj="economy meteor")
F("emergency_levy", 7, 28, "The Emergency Levy",
  "After the Ulysses warning, finance the preparations now with a temporary federal levy. Nobody likes it, and nobody inherits it.",
  R(timed("emergency_levy", 1095), ready(6), fiscal("ac_econ_set_high_tax")), pre="currency_board", excl="ulysses_bonds", gate=WARNING, ai=10,
  subj="scales meteor")
F("confidence_programme", 5, 29, "Confidence Programme",
  "After the coup of 30 May 1997, markets want proof that the Federation still governs. Guarantee the banks, publish the accounts and keep paying salaries on time.",
  R(stab(0.03), pp(15), fiscal("ac_econ_set_reconstruction")), pre="ulysses_bonds|emergency_levy", gate=COUP, ai=25, subj="economy security")
F("impact_insurance_pool", 3, 30, "Impact Insurance Pool",
  "Pool federal and private insurance against the impact. Homes and firms destroyed by debris will be rebuilt by formula, not by petition.",
  R(timed("impact_insurance", 1095), stab(0.02)), pre="confidence_programme", excl="strategic_stockpile_law", ai=25, subj="shelter scales")
F("strategic_stockpile_law", 7, 30, "Strategic Stockpile Law",
  "Require every major firm to hold six months of critical inputs in reserve. Prices rise now so that factories run after the impact.",
  R(timed("strategic_stockpile", 1095), ready(4)), pre="confidence_programme", excl="impact_insurance_pool", ai=10, subj="logistics industry")
F("economy_review", 5, 31, "Economic Review of the Decade",
  "Treasury economists publish a review of the decade: what the Federation earned, what it spent on preparedness and what it still owes.",
  R(pp(30), tech("industry", 0.5)), pre="impact_insurance_pool|strategic_stockpile_law", ai=25, subj="document economy")
F("post_impact_markets", 5, 32, "Reopen the Markets",
  "After the impact, reopen the exchanges and the ports on a fixed schedule. A date, kept, does more for confidence than any statement.",
  R(stab(0.02), pp(15)), pre="economy_review", gate=IMPACT, ai=25, subj="economy rebuild")

section("treaty", OPENING)
MOD_UTO = "Mod provenance"   # UTO and CNEA come from the 1991 bookmark and FCU history, not the Chronicle.
F("uto_chair", 13, 6, "Chair the Treaty Organization",
  "Central Usea holds the presidency of the Usean Treaty Organization and leads the faction its partners joined. Chairing it well means more than hosting the meetings.",
  R(pp(20), ev(12)), ai=25, subj="diplomacy assembly", layer=MOD_UTO, cite="1991 bookmark and FCU history (UTO_president_idea)")
F("uto_secretariat", 13, 7, "A Standing Secretariat",
  "Give the treaty a permanent secretariat with its own staff and budget. Decisions stop depending on which foreign ministry happens to hold the chair.",
  R(idea("treaty_secretariat"), pp(-20)), pre="uto_chair", ai=25, subj="assembly document", layer=MOD_UTO)
F("uto_integrated_staff", 12, 8, "Integrated Treaty Staff",
  "Merge the members' planners into one treaty staff. Plans are written once, in one language, for one chain of command.",
  R(timed("integrated_treaty_staff", 1095), army(10)), pre="uto_secretariat", excl="uto_national_contingents", ai=25, subj="command diplomacy", layer=MOD_UTO)
F("uto_national_contingents", 14, 8, "National Contingents",
  "Keep each member's forces under its own command and coordinate them by agreement. Sovereignty is preserved; speed is not.",
  R(timed("national_contingents", 1095), stab(0.02)), pre="uto_secretariat", excl="uto_integrated_staff", ai=10, subj="security diplomacy", layer=MOD_UTO)
F("uto_combined_exercises", 13, 9, "Combined Treaty Exercises",
  "Hold the treaty's first combined exercise: staffs, signals and logistics from every member, tested together for a week.",
  R(army(15), air(10)), pre="uto_integrated_staff|uto_national_contingents", ai=25, subj="training command", layer=MOD_UTO)
F("uto_observer_seat", 12, 10, "Offer Erusea an Observer Seat",
  "Invite Erusea to observe the treaty's exercises and staff talks. An observer is not a member, but a neighbour who sees the plans has less reason to fear them.",
  R(pp(-15), stab(0.02), flag("uto_observer_offered")), pre="uto_combined_exercises", excl="uto_western_watch", ai=25, subj="diplomacy peace", layer=MOD_UTO)
F("uto_western_watch", 14, 10, "The Western Watch",
  "Keep a standing treaty watch on the western frontier with Erusea. The 1991 standoff in western Usea is managed by vigilance rather than invitation.",
  R(timed("western_watch", 730), army(10)), pre="uto_combined_exercises", excl="uto_observer_seat", ai=10, subj="radar security", layer=MOD_UTO,
  cite="1991 bookmark text (standoff between Erusean and UTO forces)")
F("uto_member_review", 13, 11, "Member Review",
  "Review what each member contributes and what each needs. The treaty is only as strong as the partners who carry it.",
  R(pp(20)), pre="uto_observer_seat|uto_western_watch", ai=25, subj="document diplomacy", layer=MOD_UTO)
F("uto_amber_liaison", 12, 12, "Amber Liaison Office",
  "Open a federal liaison office with Amber's government for treaty planning. The office handles staff talks, not domestic politics.",
  R(pp(10), army(5)), pre="uto_member_review", ai=20, subj="diplomacy communications", layer=MOD_UTO)
F("uto_ugellas_liaison", 14, 12, "Ugellas Liaison Office",
  "Open a federal liaison office with Ugellas for treaty planning, focused on coastal approaches and shared harbours.",
  R(pp(10), navy(5)), pre="uto_member_review", ai=20, subj="diplomacy navy", layer=MOD_UTO)
F("uto_san_salvacion_liaison", 12, 13, "San Salvacion Liaison Office",
  "Open a federal liaison office with San Salvacion. Its place in the treaty is mod provenance; the official chronology describes the country as neutral.",
  R(pp(10), stab(0.01)), pre="uto_member_review", ai=20, subj="diplomacy peace", layer=MOD_UTO,
  cite="SNS faction membership in FCU history; Chronicle, 1998 / 06.19 calls San Salvacion neutral")
F("uto_delarus_liaison", 14, 13, "Delarus Liaison Office",
  "Open a federal liaison office with Delarus for treaty planning, focused on overland transport and reserve depots.",
  R(pp(10), army(5)), pre="uto_member_review", ai=20, subj="diplomacy logistics", layer=MOD_UTO)
F("uto_burden_question", 13, 14, "The Burden Question",
  "The Federation pays most of the treaty's costs, and every member knows it. The cabinet must decide whether to keep paying or to share the bill.",
  R(pp(15), ev(13)), pre="uto_amber_liaison|uto_ugellas_liaison|uto_san_salvacion_liaison|uto_delarus_liaison", ai=25,
  subj="scales diplomacy", layer=MOD_UTO)
F("uto_federal_subsidy", 12, 15, "The Federal Subsidy",
  "Keep paying. Central Usea covers the treaty's common costs and receives the leadership that comes with them.",
  R(timed("federal_subsidy", 1095), pp(-30)), pre="uto_burden_question", excl="uto_shared_assessment", ai=25, subj="economy diplomacy", layer=MOD_UTO)
F("uto_shared_assessment", 14, 15, "A Shared Assessment Scale",
  "Assess every member by the size of its economy. The Federation still pays most of the bill, but no longer all of it.",
  R(timed("shared_assessment", 1095), pp(20)), pre="uto_burden_question", excl="uto_federal_subsidy", ai=10, subj="scales economy", layer=MOD_UTO)
F("uto_ulysses_mandate", 13, 16, "A Ulysses Mandate",
  "After the Ulysses warning, add preparedness to the treaty's purpose. The members agree to plan the evacuation and the relief together.",
  R(ready(5), pp(15)), pre="uto_federal_subsidy|uto_shared_assessment", gate=WARNING, ai=25, subj="meteor diplomacy", layer=MOD_UTO)
F("uto_air_defence_net", 12, 17, "Treaty Air-Defence Net",
  "Link the members' radars into a single treaty air picture. It watches the sky for aircraft now and for debris later.",
  R(timed("treaty_air_picture", 1095), air(10)), pre="uto_ulysses_mandate", excl="uto_relief_command", ai=20, subj="radar air", layer=MOD_UTO)
F("uto_relief_command", 14, 17, "Treaty Relief Command",
  "Create a treaty relief command that owns the transport, field hospitals and stores every member will need after the impact.",
  R(timed("treaty_relief_command", 1095), ready(8)), pre="uto_ulysses_mandate", excl="uto_air_defence_net", ai=25, subj="medical logistics", layer=MOD_UTO)
F("uto_coup_solidarity", 13, 18, "Solidarity After the Coup",
  "The coup of 30 May 1997 struck across Usea. The treaty members exchange what they know and agree not to shelter the officers who led it.",
  R(stab(0.03), army(10)), pre="uto_air_defence_net|uto_relief_command", gate=COUP, ai=25, subj="security diplomacy", layer=MOD_UTO)
F("uto_treaty_review", 13, 19, "Treaty Review",
  "The members review the treaty's articles against the decade they have lived through. Some clauses are retired, and one is rewritten for the impact.",
  R(pp(25)), pre="uto_coup_solidarity", ai=25, subj="document assembly", layer=MOD_UTO)
F("uto_decade", 13, 20, "A Decade of the Treaty",
  "The Treaty Organization ends the decade intact. Whatever comes after the impact, its members have already learned to plan together.",
  R(stab(0.02), pp(30), ev(14)), pre="uto_treaty_review", ai=25, subj="diplomacy medal", layer=MOD_UTO)

section("skully", OPENING)
F("southern_district", 13, 22, "The Southern District",
  "The FCU Army Southern District covers the federal south and its islands. Its staff asks for attention long before anyone in the capital asks it for results.",
  R(army(10), pp(10)), ai=20, subj="security navy", cite="Chronicle, 1995 / 12.31 names the Southern District")
F("island_patrols", 12, 23, "Island Patrol Rotations",
  "Rotate patrol craft and garrison detachments through the southern islands on a fixed schedule. The islands see the Federation more often.",
  R(navy(10), army(5)), pre="southern_district", excl="island_development_grants", ai=20, subj="navy security")
F("island_development_grants", 14, 23, "Island Development Grants",
  "Fund roads, clinics and harbours in the southern islands. The Federation is more welcome where it is useful.",
  R(stab(0.02), pp(-15)), pre="southern_district", excl="island_patrols", ai=10, subj="rebuild civil")
F("skully_operation", 13, 24, "The Skully Islands Operation",
  "On 31 December 1995 Robert Tyler of the Southern District eliminates a rebel base in the Skully Islands, and Unified Command defeats those rebels through Scarface Squadron. The cabinet records the action.",
  R(flag("skully_recorded"), army(15), air(10), ev(15)), pre="island_patrols|island_development_grants", gate=SKULLY, ai=25,
  subj="security air", layer="Official", cite="Chronicle, 1995 / 12.31")
F("southern_tribunals", 12, 25, "Southern Tribunals",
  "Try the surviving rebels in federal courts sitting in the south. The process is public, and the sentences are meant to be remembered.",
  R(timed("southern_tribunals", 365), stab(0.01)), pre="skully_operation", excl="island_amnesty", ai=20, subj="scales security")
F("island_amnesty", 14, 25, "Island Amnesty",
  "Offer an amnesty to islanders who supported the rebels but did not fight. Keep the courts for those who did.",
  R(stab(0.03), pp(-10)), pre="skully_operation", excl="southern_tribunals", ai=10, subj="peace civil")
F("permanent_southern_garrison", 12, 26, "Permanent Southern Garrison",
  "Station a permanent garrison in the southern islands. The rebel base is gone; the Federation intends to stay.",
  R(idea("southern_garrison")), pre="southern_tribunals", ai=20, subj="security rebuild")
F("island_reconstruction", 14, 26, "Island Reconstruction",
  "Rebuild what the fighting damaged and what the islands never had. Contracts go to island firms where they can do the work.",
  R(idea("island_reconstruction")), pre="island_amnesty", ai=10, subj="rebuild tools")
F("unified_command_citations", 13, 27, "Unified Command Citations",
  "Cite Unified Command and Scarface Squadron for the Skully Islands action. The citations name the units the Chronicle names, and no one else.",
  R(air(15), ws(0.02)), pre="permanent_southern_garrison|island_reconstruction", ai=20, subj="medal air",
  layer="Official", cite="Chronicle, 1995 / 12.31")
F("coast_guard_charter", 12, 28, "Coast Guard Charter",
  "Give the southern waters a federal coast guard with police powers. Smugglers and rebels lose the sea lanes between the islands.",
  R(navy(10), timed("coast_guard", 730)), pre="unified_command_citations", excl="island_councils", ai=20, subj="navy document")
F("island_councils", 14, 28, "Island Councils",
  "Give each island group an elected council with a voice in the Southern District's planning. Grievances arrive as motions, not as rumours.",
  R(stab(0.03), pp(-10)), pre="unified_command_citations", excl="coast_guard_charter", ai=10, subj="ballot civil")
F("southern_lessons", 13, 29, "Lessons of the Southern Islands",
  "The Southern District writes up what the Skully Islands taught: which warnings were missed, which reports arrived late and which units answered at once.",
  R(army(10), ev(29)), pre="coast_guard_charter|island_councils", ai=20, subj="document security")

section("evacuation", OPENING)
F("ulysses_warning", 17, 6, "The Ulysses Warning",
  "On 20 April 1996 Central Usea announces that the asteroid Ulysses will strike the Earth. The government that made the announcement must now prepare for it.",
  R(ready(10), flag("warning_answered"), ev(16)), gate=WARNING, ai=30, subj="meteor communications",
  layer="Official", cite="Chronicle, 1996 / 04.20")
F("evacuation_census", 17, 7, "The Evacuation Census",
  "Count everyone: where they live, how they would travel and who would need help to move. Every later plan starts from this register.",
  R(ready(6), pp(-15), ev(17)), pre="ulysses_warning", gate=WARNING, ai=30, subj="document refugees")
F("dispersal_doctrine", 16, 8, "Dispersal Doctrine",
  "Plan to move people away from the coasts and the cities, spreading them across the interior. Fewer targets, more roads to manage.",
  R(idea("dispersal_doctrine"), ready(8)), pre="evacuation_census", excl="hardened_shelters", cost=10, gate=WARNING, ai=30, subj="refugees rail")
F("hardened_shelters", 18, 8, "Hardened Shelter Programme",
  "Plan to keep people near home in hardened public shelters. Fewer journeys, more concrete.",
  R(idea("hardened_shelters"), ready(8)), pre="evacuation_census", excl="dispersal_doctrine", cost=10, gate=WARNING, ai=10, subj="shelter industry")
F("transport_requisition", 17, 9, "Transport Requisition Orders",
  "Draft the orders that would requisition buses, trains, ships and aircraft for the evacuation. Owners are told now, not on the day.",
  R(ready(6), tech("logistics_tech", 0.5)), pre="dispersal_doctrine|hardened_shelters", gate=WARNING, ai=30, subj="logistics document")
F("rail_timetables", 16, 10, "Rail Evacuation Timetables",
  "Write the evacuation around the railways: fixed timetables, numbered trains and stations assigned by district.",
  R(ready(7), tech("train_tech", 0.5)), pre="transport_requisition", excl="civil_air_bridge", gate=WARNING, ai=30, subj="rail logistics")
F("civil_air_bridge", 18, 10, "The Civil Air Bridge",
  "Write the evacuation around aircraft: civil airliners and military transports flying a shuttle from the coast to the interior.",
  R(ready(7), air(10)), pre="transport_requisition", excl="rail_timetables", gate=WARNING, ai=10, subj="air refugees")
F("hospital_relocation", 17, 11, "Hospital Relocation Plan",
  "Move the hospitals that cannot be evacuated in a week, and plan the field hospitals that will replace them.",
  R(ready(6), manpower(2000)), pre="rail_timetables|civil_air_bridge", gate=WARNING, ai=30, subj="medical logistics")
F("coastal_evacuation_zones", 16, 12, "Coastal Evacuation Zones",
  "Draw evacuation zones along the coasts by distance and elevation. The maps are published so that families can plan before they are told.",
  R(ready(7), stab(-0.01)), pre="hospital_relocation", excl="inland_reception_towns", gate=WARNING, ai=30, subj="refugees navy")
F("inland_reception_towns", 18, 12, "Inland Reception Towns",
  "Designate inland towns to receive evacuees and fund them now: water, schools, clinics and housing before the arrivals.",
  R(ready(6), stab(0.01)), pre="hospital_relocation", excl="coastal_evacuation_zones", gate=WARNING, ai=10, subj="shelter civil")
F("national_public_drills", 17, 13, "National Public Drills",
  "Hold a national drill: sirens, timetables, reception points. Millions of people walk through the evacuation once, so they will know it the second time.",
  R(ready(8), stab(-0.02), ev(18)), pre="coastal_evacuation_zones|inland_reception_towns", gate=WARNING, ai=30, subj="training refugees")
F("compulsory_registration", 16, 14, "Compulsory Registration",
  "Require every household to register its evacuation plan. The register is complete, and some citizens resent being counted.",
  R(ready(8), stab(-0.02)), pre="national_public_drills", excl="voluntary_registers", gate=WARNING, ai=20, subj="document security")
F("voluntary_registers", 18, 14, "Voluntary Registers",
  "Invite households to register and reward them with priority places. The register is incomplete, but nobody is forced to sign it.",
  R(ready(4), stab(0.02)), pre="national_public_drills", excl="compulsory_registration", gate=WARNING, ai=20, subj="ballot refugees")
F("evacuation_fuel_reserve", 17, 15, "Evacuation Fuel Reserve",
  "Set aside fuel for the evacuation and lock it away from every other claim, including the army's.",
  R(ready(6)), pre="compulsory_registration|voluntary_registers", gate=WARNING, ai=30, subj="logistics security")
F("partner_reception", 16, 16, "Partner Reception Agreements",
  "Agree with the treaty partners that each will receive evacuees from the others' threatened districts. Borders open for the emergency only.",
  R(ready(6), pp(-15)), pre="evacuation_fuel_reserve", excl="federal_self_reliance", gate=WARNING, ai=30, subj="diplomacy refugees")
F("federal_self_reliance", 18, 16, "Federal Self-Reliance",
  "Plan to receive every federal evacuee inside the Federation. Partners keep their room for their own people.",
  R(ready(4), stab(0.02)), pre="evacuation_fuel_reserve", excl="partner_reception", gate=WARNING, ai=10, subj="shelter security")
F("continuity_bunkers", 17, 17, "Continuity Bunkers",
  "Build protected sites for the government, the records and the communications that must survive the impact.",
  R(ready(5), stab(0.02)), pre="partner_reception|federal_self_reliance", gate=WARNING, ai=30, subj="shelter communications")
F("the_final_count", 17, 18, "The Final Count",
  "In the last months before the impact, recount the evacuation: seats, places, fuel, beds. What is missing now will be missing on the day.",
  R(ready(6), ev(19)), pre="continuity_bunkers", gate="date > 1998.12.31", ai=30, subj="document meteor")
F("stay_behind_teams", 16, 19, "Stay-Behind Teams",
  "Keep volunteers behind in every evacuated district to guard property, run utilities and report damage the moment it happens.",
  R(ready(5), flag("stay_behind")), pre="the_final_count", excl="total_evacuation_order", gate="date > 1999.3.31", ai=30, subj="security civil")
F("total_evacuation_order", 18, 19, "Total Evacuation Order",
  "Order everyone out of the threatened districts, with no exceptions. Nobody is left in harm's way; nobody is left to watch the empty towns.",
  R(ready(8), stab(-0.03), flag("total_evacuation")), pre="the_final_count", excl="stay_behind_teams", gate="date > 1999.3.31", ai=10, subj="refugees meteor")
F("the_last_convoys", 17, 20, "The Last Convoys",
  "The last convoys leave the coast. Whatever has not moved by now stays where it is.",
  R(ready(6), flag("last_convoys")), pre="stay_behind_teams|total_evacuation_order", gate="date > 1999.5.31", ai=30, subj="logistics refugees")
F("evacuation_after_action", 17, 21, "Evacuation After-Action Report",
  "After the impact, every district reports how its evacuation went. The report is blunt about failures, because there may be a next time.",
  R(pp(30), army(10)), pre="the_last_convoys", gate=IMPACT, ai=30, subj="document refugees")

section("stonehenge", OPENING)
SH = "Chronicle, 1998 / 06.19; Super Weapons, Stonehenge"
F("stonehenge_consortium", 17, 23, "The Stonehenge Consortium",
  "Central Usea leads an international project to build a battery of railguns against Ulysses' fragments. The consortium needs members, money and engineers before it needs a timetable.",
  R(idea("stonehenge_consortium"), ev(20)), gate=WARNING, ai=30, subj="radar diplomacy", layer="Official", cite=SH)
F("federal_lead_share", 16, 24, "A Federal Lead Share",
  "Central Usea takes the largest share of the project's cost and the largest voice in its decisions.",
  R(pp(-30), flag("stonehenge_federal_lead")), pre="stonehenge_consortium", excl="international_shares", gate=WARNING, ai=30, subj="economy radar")
F("international_shares", 18, 24, "Open International Shares",
  "Invite every interested government to buy a share of the project. More partners, more money and more voices in the room.",
  R(pp(20), flag("stonehenge_shared")), pre="stonehenge_consortium", excl="federal_lead_share", gate=WARNING, ai=10, subj="diplomacy economy")
F("host_agreement", 17, 25, "The Host Agreement",
  "The battery will stand in a desert region of neutral San Salvacion. The host agreement covers access, security and what happens to the site afterwards.",
  R(pp(15), stab(0.01)), pre="federal_lead_share|international_shares", gate=WARNING, ai=30, subj="document peace", layer="Official", cite=SH)
F("engineers_family_quarters", 16, 26, "Engineers' Family Quarters",
  "Build housing at the site so that the engineers can bring their families. The project keeps its experts; the experts keep their homes nearby.",
  R(tech("electronics", 0.5), flag("stonehenge_families")), pre="host_agreement", excl="rotating_contract_crews", gate=WARNING, ai=30, subj="civil science")
F("rotating_contract_crews", 18, 26, "Rotating Contract Crews",
  "Staff the site with contract crews on rotation. Nobody settles in the desert, and nobody stays long enough to know the battery best.",
  R(tech("electronics", 0.5), pp(15)), pre="host_agreement", excl="engineers_family_quarters", gate=WARNING, ai=10, subj="training tools")
F("eight_batteries", 17, 27, "Eight Batteries",
  "The design calls for eight railguns. Each must be supplied with power, ammunition and fire control, and each must be able to fire alone.",
  R(tech("rocketry", 0.5)), pre="engineers_family_quarters|rotating_contract_crews", gate=WARNING, ai=30, subj="missile radar",
  layer="Official", cite="Super Weapons, Stonehenge (eight railguns)")
F("fragment_tracking_network", 16, 28, "Fragment Tracking Network",
  "Build the tracking network that will tell the batteries where the fragments are. Without it, eight guns are eight guesses.",
  R(tech("radar_tech", 0.5)), pre="eight_batteries", gate=WARNING, ai=25, subj="telescope radar")
F("battery_power_grid", 18, 28, "The Battery Power Grid",
  "Build the power plants and the grid the railguns will draw on. The desert site needs more electricity than a city.",
  R(tech("industry", 0.5)), pre="eight_batteries", gate=WARNING, ai=25, subj="industry radar")
F("stonehenge_completed", 17, 29, "Stonehenge Completed",
  "On 19 June 1998 Central Usea completes Stonehenge in a desert region of San Salvacion. Eight railguns now wait for Ulysses.",
  R(flag("stonehenge_recorded"), stab(0.03), ws(0.02), ev(21)), pre="fragment_tracking_network|battery_power_grid", gate=STONEHENGE_DONE, ai=30,
  subj="radar medal", layer="Official", cite=SH)
F("neutral_custody_protocol", 16, 30, "Neutral Custody Protocol",
  "Agree that the battery serves every nation under the consortium's rules and that its host remains neutral.",
  R(stab(0.02), flag("stonehenge_neutral")), pre="stonehenge_completed", excl="federal_battery_custody", ai=30, subj="peace radar")
F("federal_battery_custody", 18, 30, "Federal Custody of the Batteries",
  "Keep operational control of the battery with federal crews and federal officers. The consortium funds it; the Federation runs it.",
  R(pp(20), air(5), flag("stonehenge_federal")), pre="stonehenge_completed", excl="neutral_custody_protocol", ai=10, subj="security radar")
F("interception_drills", 17, 31, "Interception Drills",
  "Rehearse the interception: tracking, firing order and power load, against a sky that will soon be full of debris.",
  R(air(10), ready(4)), pre="neutral_custody_protocol|federal_battery_custody", ai=30, subj="training radar")

section("coup", OPENING)
F("coup_inquiry", 22, 6, "The Coup Inquiry",
  "Unified Command has defeated the coup of 30 May 1997, or is still fighting it. The cabinet opens an inquiry into how commands across Usea turned at once.",
  R(pp(20), ev(22)), pre="FCU_ur_assessment", gate=COUP, ai=30, subj="document security", cite="Chronicle, 1997 / 05.30")
F("coup_tribunals", 20, 7, "Federal Coup Tribunals",
  "Try the coup's leaders before federal tribunals. The trials are swift and public.",
  R(idea("coup_tribunals")), pre="coup_inquiry", excl="coup_reconciliation", gate=COUP, ai=25, subj="scales security")
F("coup_reconciliation", 22, 7, "Reconciliation Hearings",
  "Hear the officers who joined the coup before deciding who stands trial. Some were leaders; many were led.",
  R(idea("coup_reconciliation")), pre="coup_inquiry", excl="coup_tribunals", gate=COUP, ai=10, subj="peace scales")
F("officer_corps_review", 21, 8, "Officer Corps Review",
  "Review promotion, rotation and command assignments across the officer corps. The coup used gaps in all three.",
  R(army(15), pp(-15)), pre="coup_tribunals|coup_reconciliation", gate=COUP, ai=25, subj="command document")
F("restore_the_districts", 20, 9, "Restore the Districts",
  "The coup has been defeated. Return the districts that went silent to their civil administrations and their regular commanders.",
  R(stab(0.03), pp(20)), pre="officer_corps_review", excl="pacification_campaign", gate="has_country_flag = ac_ur_coup_defeated", ai=25,
  subj="rebuild assembly", cite="Chronicle, 1997 / 05.30")
F("pacification_campaign", 22, 9, "Pacification Campaign",
  "In this provisional branch the emergency has not ended. Plan a campaign to bring the districts that still defy the government back under federal control.",
  R(army(20), stab(-0.02)), pre="officer_corps_review", excl="restore_the_districts", gate="has_country_flag = ac_ur_coup_prolonged", ai=25,
  subj="security command")
F("honour_unified_command", 20, 10, "Honour Unified Command",
  "Honour Unified Command and Scarface 1 for defeating the coup. The ceremony names those the Chronicle names.",
  R(air(15), ws(0.02)), pre="restore_the_districts", gate=COUP, ai=25, subj="medal air", layer="Official", cite="Chronicle, 1997 / 05.30")
F("district_emergency_cells", 22, 10, "District Emergency Cells",
  "Form emergency cells in every district still contested: a commander, an administrator and a police chief with joint authority.",
  R(army(10), pp(15)), pre="pacification_campaign", gate=COUP, ai=25, subj="command civil")
F("lessons_of_30_may", 21, 11, "Lessons of 30 May",
  "The inquiry reports. It names no wider conspiracy, because the evidence does not show one; it names the failures that let commands go silent together.",
  R(flag("coup_lessons"), army(10), ev(23)), pre="honour_unified_command|district_emergency_cells", gate=COUP, ai=25, subj="document command")
F("civilian_control_act", 20, 12, "Civilian Control Act",
  "Put every deployment order through a civilian minister's signature. The army will move a little slower and answer a little more.",
  R(idea("civilian_control")), pre="lessons_of_30_may", excl="command_autonomy_charter", gate=COUP, ai=25, subj="assembly document")
F("command_autonomy_charter", 22, 12, "Command Autonomy Charter",
  "Give Unified Command authority to act without waiting for ministers in a declared emergency. The coup was defeated by speed.",
  R(idea("command_autonomy")), pre="lessons_of_30_may", excl="civilian_control_act", gate=COUP, ai=10, subj="command security")
F("intelligence_reform", 21, 13, "Intelligence Reform",
  "Merge the overlapping intelligence offices that each saw part of the coup and none saw the whole.",
  R(tech("encryption_tech", 0.5), pp(-10)), pre="civilian_control_act|command_autonomy_charter", gate=COUP, ai=25, subj="radar document")
F("coup_warning_net", 20, 14, "Coup-Warning Net",
  "Link the treaty members' command centres so that a silent garrison anywhere in Usea is noticed everywhere within the hour.",
  R(timed("coup_warning_net", 1095), army(10)), pre="intelligence_reform", excl="federal_security_service", gate=COUP, ai=25,
  subj="communications radar")
F("federal_security_service", 22, 14, "Federal Security Service",
  "Create a federal security service with authority to investigate officers. It will find plots; it may also find enemies where there are only critics.",
  R(idea("federal_security_service")), pre="intelligence_reform", excl="coup_warning_net", gate=COUP, ai=10, subj="security assembly")
F("thirty_may_memorial", 21, 15, "The 30 May Memorial",
  "Raise a memorial to the soldiers and civilians who died resisting the coup. It lists the dead and leaves out the names of the plotters.",
  R(stab(0.03), ws(0.02)), pre="coup_warning_net|federal_security_service", gate=COUP, ai=25, subj="medal civil")
F("coup_settlement", 21, 16, "The Coup Settlement",
  "The cabinet closes the coup file: who was tried, who was pardoned, what changed and what must never change again.",
  R(flag("coup_settled"), stab(0.03), pp(30), ev(24)), pre="thirty_may_memorial", gate=COUP, ai=25, subj="scales document")

section("impact", OPENING)
F("relief_planning_cell", 21, 18, "Relief Planning Cell",
  "Months before the impact, a planning cell drafts the relief effort: who goes where, with what, the day after.",
  R(ready(4), pp(-10)), gate="date > 1998.12.31", ai=30, subj="medical document")
F("forward_relief_depots", 20, 19, "Forward Relief Depots",
  "Stock relief depots near the threatened districts so that aid is already close when roads are cut.",
  R(ready(5), flag("relief_depots")), pre="relief_planning_cell", excl="mobile_relief_columns", gate="date > 1998.12.31", ai=30, subj="logistics shelter")
F("mobile_relief_columns", 22, 19, "Mobile Relief Columns",
  "Keep relief on wheels: columns of trucks, field kitchens and clinics that can go wherever the damage is worst.",
  R(ready(5), flag("relief_columns")), pre="relief_planning_cell", excl="forward_relief_depots", gate="date > 1998.12.31", ai=10, subj="logistics medical")
F("impact_night", 21, 20, "Impact Night",
  "On 8 July 1999 Ulysses passes the Roche limit and breaks apart, and its fragments fall across the world. The Federation counts what it saved and starts on what it did not.",
  R(ev(25)), pre="relief_planning_cell", gate=IMPACT, ai=30, subj="meteor shelter",
  layer="Official", cite="Chronicle, 1999 / 07.08")
F("federal_relief_corps", 19, 21, "Federal Relief Corps",
  "Put the relief effort under a federal civil corps: one command, civilian staff, federal money.",
  R(flag("relief_lane_corps"), idea("relief_corps")), pre="impact_night", excl="treaty_relief_compact|military_relief_command", gate=IMPACT, ai=30,
  subj="civil medical")
F("treaty_relief_compact", 21, 21, "Treaty Relief Compact",
  "Run the relief effort with the treaty partners: shared stores, shared transport and shared responsibility for the results.",
  R(flag("relief_lane_treaty"), idea("treaty_relief")), pre="impact_night", excl="federal_relief_corps|military_relief_command", gate=IMPACT, ai=10,
  subj="diplomacy medical")
F("military_relief_command", 23, 21, "Military Relief Command",
  "Hand the relief effort to the army. It has the trucks, the engineers and the discipline; it does not have a light touch.",
  R(flag("relief_lane_military"), idea("military_relief")), pre="impact_night", excl="federal_relief_corps|treaty_relief_compact", gate=IMPACT, ai=10,
  subj="command shelter")
F("field_kitchens", 19, 22, "Field Kitchens",
  "Feed the displaced: field kitchens in every reception town, supplied daily from the depots.",
  R(stab(0.02), manpower(2000)), pre="federal_relief_corps", gate=IMPACT, ai=30, subj="civil logistics")
F("partner_airlift", 21, 22, "Partner Airlift",
  "Treaty transports fly relief from undamaged partners to the worst-hit districts.",
  R(stab(0.02), air(10)), pre="treaty_relief_compact", gate=IMPACT, ai=30, subj="air diplomacy")
F("engineer_battalions", 23, 22, "Engineer Battalions",
  "Army engineers clear roads, raise bridges and restore power where the fragments struck.",
  R(army(10), tech("construction_tech", 0.5)), pre="military_relief_command", gate=IMPACT, ai=30, subj="bridge tools")
F("rebuild_lifelines", 19, 23, "Rebuild the Lifelines",
  "Restore water, power and communications first. Everything else in the recovery depends on them.",
  R(flag("relief_lane_finished"), stab(0.03), drop("relief_corps")), pre="field_kitchens", gate=IMPACT, ai=30, subj="rebuild communications")
F("shared_reconstruction", 21, 23, "Shared Reconstruction",
  "Divide the reconstruction among the treaty partners by district. Each partner takes responsibility for what it rebuilds.",
  R(flag("relief_lane_finished"), stab(0.03), drop("treaty_relief")), pre="partner_airlift", gate=IMPACT, ai=30, subj="rebuild diplomacy")
F("order_in_the_camps", 23, 23, "Order in the Camps",
  "Bring the reception camps under military administration until the districts can take their people back.",
  R(flag("relief_lane_finished"), stab(0.02), army(10), drop("military_relief")), pre="engineer_battalions", gate=IMPACT, ai=30,
  subj="security shelter")

section("forces", OPENING)
F("federal_forces_review", 21, 25, "Federal Forces Review",
  "Review what the Federation's forces are for in a decade without a declared enemy: treaty defence, disaster relief and the long watch in the west.",
  R(army(10), ev(28)), ai=25, subj="command training")
F("air_arm_first", 20, 26, "The Air Arm First",
  "Put the air arm first in the budget. The Federation is large; aircraft reach its edges fastest.",
  R(idea("air_arm_first")), pre="federal_forces_review", excl="balanced_forces", ai=25, subj="air economy")
F("balanced_forces", 22, 26, "Balanced Forces",
  "Fund the army, navy and air arm in proportion. No service is starved to feed another.",
  R(idea("balanced_forces")), pre="federal_forces_review", excl="air_arm_first", ai=10, subj="command scales")
F("aircrew_schools", 21, 27, "Aircrew Schools",
  "Expand the federal flight schools and lengthen the course. Pilots who trained longer live longer.",
  R(air(15), tech("air_doctrine", 0.5)), pre="air_arm_first|balanced_forces", ai=25, subj="training air")
F("interceptor_wings", 20, 28, "Interceptor Wings",
  "Build the air arm around interceptors that defend federal airspace and the treaty partners' skies.",
  R(tech("light_fighter", 0.5), air(5)), pre="aircrew_schools", excl="strike_wings", ai=25, subj="air radar")
F("strike_wings", 22, 28, "Strike Wings",
  "Build the air arm around strike aircraft that support the army on the ground.",
  R(tech("tactical_bomber", 0.5), army(5)), pre="aircrew_schools", excl="interceptor_wings", ai=10, subj="air security")
F("joint_air_ground_drills", 21, 29, "Joint Air-Ground Drills",
  "Train the air arm and the army together until a request for support is answered in minutes, not hours.",
  R(army(10), air(10)), pre="interceptor_wings|strike_wings", ai=25, subj="training command")
F("coastal_air_patrols", 20, 30, "Coastal Air Patrols",
  "Fly regular patrols along the federal coasts and over the southern islands.",
  R(air(10), navy(5)), pre="joint_air_ground_drills", ai=20, subj="air navy")
F("interior_garrisons", 22, 30, "Interior Garrisons",
  "Reinforce the interior garrisons that protect the rail lines and the reception towns.",
  R(army(10), manpower(2000)), pre="joint_air_ground_drills", ai=20, subj="security rail")
F("radar_belt", 21, 31, "The Radar Belt",
  "Close the gaps in the federal radar cover. Nothing should cross the border, or fall from the sky, unseen.",
  R(tech("radar_tech", 0.5)), pre="coastal_air_patrols|interior_garrisons", ai=25, subj="radar air")
F("reserve_wings", 20, 32, "Reserve Wings",
  "Keep trained reserve pilots current with a few weeks of flying every year.",
  R(timed("reserve_wings", 1095)), pre="radar_belt", excl="rapid_reaction_brigades", ai=25, subj="air training")
F("rapid_reaction_brigades", 22, 32, "Rapid-Reaction Brigades",
  "Keep two brigades at short notice for any emergency in the Federation or the treaty area.",
  R(timed("rapid_reaction", 1095)), pre="radar_belt", excl="reserve_wings", ai=10, subj="security logistics")
F("forces_at_decades_end", 21, 33, "The Forces at Decade's End",
  "The forces review their decade: the southern islands, the coup and the impact. They report what they are ready for and what they are not.",
  R(army(10), air(10), pp(20)), pre="reserve_wings|rapid_reaction_brigades", ai=25, subj="document command")


# =================================================================== WAR TREE
NOT_AT_WAR = "NOT = { has_global_flag = ac_ucw_war_started }"
WAR_ON = "has_global_flag = ac_ucw_war_started"
ISAF = "has_global_flag = ac_ucw_isaf_formed"
COUNTER = "has_global_flag = ac_ucw_stage_counteroffensive"
WAR_ENDED = ("OR = { has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_ucw_outcome_erusean_victory "
             "has_global_flag = ac_ucw_outcome_stalemate has_global_flag = ac_ucw_war_averted }")

section("aftermath", WAR)
F("long_aftermath", 46, 0, "The Long Aftermath",
  "The impact has passed and the debris has not. The Federation enters the new century with reception towns still full and a sky still crossed by falling fragments.",
  R(pp(30), ev(31)), ai=30, subj="rebuild meteor", cite="Chronicle, 1999 / 07.08")
F("debris_season", 44, 1, "The Debris Season",
  "Fragments of Ulysses keep falling. Federal agencies publish a seasonal forecast of where and when the risk is highest.",
  R(stab(0.02), recovery(2)), pre="long_aftermath", ai=30, subj="meteor radar")
F("refugee_ledger", 48, 1, "The Refugee Ledger",
  "On 21 April 2000 Erusea stops taking in refugees. The Federation must decide how many of those turned away it can receive.",
  R(pp(-10), ev(32)), pre="long_aftermath", gate="date > 2000.4.20", ai=30, subj="refugees document", layer="Official", cite="Chronicle, 2000 / 04.21")
F("battery_crew_rotations", 42, 2, "Battery Crew Rotations",
  "Keep Stonehenge's crews rotating on a schedule that matches the debris forecast. The battery is only useful when its people are fresh.",
  R(air(10), stab(0.01)), pre="debris_season", gate="ac_ucw_stonehenge_intact = yes", ai=30, subj="radar training",
  cite="Super Weapons, Stonehenge")
F("open_federal_camps", 46, 2, "Open the Federal Camps",
  "Open federal reception camps to refugees turned away elsewhere. The camps are crowded; the alternative is worse.",
  R(idea("open_camps"), recovery(-2)), pre="refugee_ledger", excl="partner_resettlement_quotas", ai=30, subj="shelter refugees")
F("partner_resettlement_quotas", 50, 2, "Partner Resettlement Quotas",
  "Agree quotas with the treaty partners so that every member receives its share of the refugees.",
  R(idea("resettlement_quotas"), pp(-20)), pre="refugee_ledger", excl="open_federal_camps", ai=10, subj="diplomacy refugees")
F("fragment_warning_service", 44, 3, "Fragment Warning Service",
  "Broadcast fragment warnings to every district with enough notice to take cover.",
  R(stab(0.02), tech("radar_tech", 0.5)), pre="debris_season", ai=30, subj="radar communications")
F("camp_schools", 48, 3, "Camp Schools",
  "Open schools in the reception camps. Children who have lost their homes should not also lose their years.",
  R(stab(0.03), recovery(2)), pre="open_federal_camps|partner_resettlement_quotas", ai=30, subj="training shelter")
F("forward_deterrence", 44, 4, "Forward Deterrence",
  "Erusea has closed its border and the continent is tense. Move federal units forward and make the treaty's commitments visible.",
  R(idea("forward_deterrence"), ev(33)), pre="fragment_warning_service", excl="continental_restraint", gate="date > 2000.12.31 " + NOT_AT_WAR, ai=25,
  subj="security command")
F("continental_restraint", 48, 4, "Continental Restraint",
  "Keep the federal posture defensive and the units at home. Nothing the Federation does should give Erusea a reason it does not already have.",
  R(idea("continental_restraint"), ev(34)), pre="camp_schools", excl="forward_deterrence", gate="date > 2000.12.31 " + NOT_AT_WAR, ai=10,
  subj="peace command")
F("border_air_patrols", 44, 5, "Border Air Patrols",
  "Fly patrols along the western border inside federal airspace. They watch; they do not cross.",
  R(air(15)), pre="forward_deterrence", gate=NOT_AT_WAR, ai=25, subj="air radar")
F("confidence_measures", 48, 5, "Confidence Measures",
  "Publish the federal exercise calendar and invite observers. The Federation has nothing to hide from its neighbours.",
  R(stab(0.02), pp(15)), pre="continental_restraint", gate=NOT_AT_WAR, ai=25, subj="peace document")
F("reserve_callup_plans", 44, 6, "Reserve Call-Up Plans",
  "Update the reserve call-up plans so that mobilisation can begin within days if the worst happens.",
  R(army(15), manpower(5000)), pre="border_air_patrols", gate=NOT_AT_WAR, ai=25, subj="command training")
F("relief_diplomacy", 48, 6, "Relief Diplomacy",
  "Offer federal relief experts to any Usean government that asks, Erusea included. Help is harder to refuse than talks.",
  R(stab(0.02), pp(20)), pre="confidence_measures", gate=NOT_AT_WAR, ai=25, subj="diplomacy medical")
F("summer_of_2003", 46, 7, "The Summer of 2003",
  "In the summer of 2003 Erusea invades neutral San Salvacion and seizes Stonehenge. The Federation's decade of preparation now meets a war.",
  R(ws(0.05), ev(35)), gate=WAR_ON, ai=30, subj="security meteor", layer="Official", cite="Chronicle, 2003 / SUMMER")
F("national_mobilisation", 44, 8, "National Mobilisation",
  "Call up every reserve and move the economy onto a war footing at once.",
  R(idea("national_mobilisation")), pre="summer_of_2003", excl="measured_mobilisation", gate=WAR_ON, ai=25, subj="command industry")
F("measured_mobilisation", 48, 8, "Measured Mobilisation",
  "Call up the reserves in stages and keep the civilian economy running. The war may be long.",
  R(idea("measured_mobilisation")), pre="summer_of_2003", excl="national_mobilisation", gate=WAR_ON, ai=10, subj="scales command")
F("home_front_councils", 46, 9, "Home Front Councils",
  "Form councils in every region to manage rationing, refugees and war work together.",
  R(stab(0.03), recovery(2)), pre="national_mobilisation|measured_mobilisation", gate=WAR_ON, ai=25, subj="assembly civil")
F("war_economy_board", 46, 10, "War Economy Board",
  "A single board allocates steel, fuel and labour between the war and the recovery.",
  R(tech("industry", 0.75), fiscal("ac_econ_refresh_budget")), pre="home_front_councils", gate=WAR_ON, ai=25, subj="industry scales")
F("war_bonds", 44, 11, "War Bonds",
  "Sell war bonds to citizens and partners. The war is paid for over decades.",
  R(timed("war_bonds", 730), pp(20)), pre="war_economy_board", excl="allied_credit", gate=WAR_ON, ai=25, subj="economy medal")
F("allied_credit", 48, 11, "Allied Credit",
  "Borrow from allies and partners beyond Usea. The money comes quickly and with conditions.",
  R(timed("allied_credit", 730), stab(-0.01)), pre="war_economy_board", excl="war_bonds", gate=WAR_ON, ai=10, subj="diplomacy economy")
F("home_front_endures", 46, 12, "The Home Front Endures",
  "Two years of war and five years of debris have not broken the home front. The Federation keeps working.",
  R(stab(0.04), ws(0.03), ev(36)), pre="war_bonds|allied_credit", gate=WAR_ON, ai=25, subj="civil medal")

section("continuity", WAR)
F("federal_question_returns", 55, 0, "The Federal Question Returns",
  "The government that carried the Federation through the impact must now carry it into a new century and, perhaps, a war.",
  R(pp(20), ev(37)), ai=30, subj="assembly ballot")
F("presidential_continuity", 52, 1, "Presidential Continuity",
  "The federal presidency and the Assembly govern as they have since 1991. Continuity is itself a policy.",
  R(stab(0.03), pp(20)), pre="federal_question_returns", gate=GOV_FEDERAL, ai=30, subj="assembly document",
  layer="Mod provenance", cite="1991 FCU government; Sinclair's earlier term is user-approved provisional chronology")
F("directorate_second_term", 55, 1, "The Directorate's Second Term",
  "The directorate enters the new century still in power. The emergency it was built for has passed; its critics say so daily.",
  R(pp(30), stab(-0.02)), pre="federal_question_returns", gate=GOV_DIRECTORATE, ai=0, subj="command assembly", layer=ALT)
F("unity_renewal", 58, 1, "Renew the Unity Government",
  "The unity cabinet asks the parties to stay in government through the recovery. Most agree; some want their independence back.",
  R(stab(0.02), pp(20)), pre="federal_question_returns", gate=GOV_UNITY, ai=0, subj="ballot assembly", layer=ALT)
F("federal_war_cabinet", 52, 2, "A Federal War Cabinet",
  "Form a small war cabinet inside the federal government, ready before it is needed.",
  R(pp(25), army(10)), pre="presidential_continuity", ai=30, subj="command assembly")
F("restore_before_the_charter", 54, 2, "Restore Civilian Rule",
  "End the directorate now, before any war or alliance tests it. Executive authority returns to the presidency and the Assembly.",
  R(regime("restoration"), clear("gov_directorate"), flag("gov_restored"), flag("authority_returned"), drop("directorate_rule"),
    drop("extended_directorate"), idea("restored_assembly"), ev(59)),
  pre="directorate_second_term", excl="directorate_war_footing", cost=10, ai=0, subj="ballot assembly", layer=ALT, regime="restoration")
F("directorate_war_footing", 56, 2, "Directorate War Footing",
  "Keep the directorate and prepare it for war. Its staff structure was built for emergencies; this is one.",
  R(timed("directorate_war_footing", 730), army(15)), pre="directorate_second_term", excl="restore_before_the_charter", ai=0,
  subj="command security", layer=ALT)
F("unity_war_cabinet", 58, 2, "Unity War Cabinet",
  "Draw a war cabinet from every party in the unity government. Each party shares the decisions and the blame.",
  R(stab(0.03), pp(15)), pre="unity_renewal", ai=0, subj="assembly command", layer=ALT)
F("presidents_coalition", 52, 3, "The President's Coalition",
  "FCU President Robert Sinclair founds ISAF on 22 August 2003. The federal government turns the treaty partners into an allied force.",
  R(ws(0.03), pp(30)), pre="federal_war_cabinet", gate=ISAF, ai=30, subj="diplomacy medal", layer="Official", cite="Chronicle, 2003 / 08.22")
F("directorate_accounting", 55, 3, "The Directorate's Accounting",
  "Whether it ended or endured, the directorate must account to the Assembly for the years it governed.",
  R(pp(20), stab(0.02)), pre="restore_before_the_charter|directorate_war_footing", ai=0, subj="scales document", layer=ALT)
F("unity_charter_vote", 58, 3, "A Vote for the Charter",
  "The unity cabinet puts the ISAF charter to an Assembly vote. Every party votes, and every party is bound.",
  R(stab(0.03), ws(0.03), ev(60)), pre="unity_war_cabinet", gate=ISAF, ai=0, subj="ballot diplomacy", layer=ALT)
F("assembly_war_powers", 52, 4, "Assembly War Powers",
  "The Assembly grants the presidency war powers for the duration and keeps the right to review them every six months.",
  R(ws(0.03), pp(20)), pre="presidents_coalition", ai=30, subj="assembly security")
F("wartime_constitution", 55, 5, "The Wartime Constitution",
  "Whatever government leads the Federation, the war needs rules: who decides, who is consulted and when the emergency ends.",
  R(stab(0.02), ev(38)), pre="assembly_war_powers|directorate_accounting|unity_charter_vote", ai=30, subj="document scales")
F("postwar_elections_pledge", 53, 6, "Pledge Postwar Elections",
  "Promise federal elections within a year of the war's end. The promise is meant to be kept.",
  R(stab(0.03), flag("elections_pledged")), pre="wartime_constitution", excl="emergency_continuity", ai=30, subj="ballot document")
F("emergency_continuity", 57, 6, "Emergency Continuity",
  "Keep the emergency arrangements until the reconstruction is complete. Elections can wait for peace.",
  R(pp(40), stab(-0.02), flag("emergency_continued")), pre="wartime_constitution", excl="postwar_elections_pledge", ai=10, subj="command document")

section("isaf", WAR)
F("charter_articles", 65, 0, "The Charter Articles",
  "On 22 August 2003 FCU President Robert Sinclair establishes ISAF after Erusea refuses to leave San Salvacion and Stonehenge. Its charter must turn partners into one force.",
  R(pp(20), ev(39)), gate=ISAF, ai=30, subj="document diplomacy", layer="Official", cite="Chronicle, 2003 / 08.22")
F("integrated_isaf_staff", 62, 1, "Integrated ISAF Staff",
  "Merge the members' staffs into one ISAF headquarters with officers from every nation in every section.",
  R(idea("isaf_integrated_staff")), pre="charter_articles", excl="lead_nation_command", gate=ISAF, ai=25, subj="command diplomacy")
F("lead_nation_command", 68, 1, "Lead-Nation Command",
  "Central Usea leads ISAF and the partners attach liaison officers. Faster decisions, fewer voices.",
  R(idea("isaf_lead_nation")), pre="charter_articles", excl="integrated_isaf_staff", gate=ISAF, ai=10, subj="command security")
F("member_contributions", 65, 2, "Member Contributions",
  "Agree what each ISAF member contributes: units, bases, transport and money.",
  R(pp(20), manpower(5000)), pre="integrated_isaf_staff|lead_nation_command", gate=ISAF, ai=25, subj="scales diplomacy")
F("san_salvacion_liaison", 61, 3, "Liaison with San Salvacion",
  "Keep a liaison with San Salvacion's authorities through the occupation. ISAF fights to restore the country, not to replace its government.",
  R(stab(0.01), pp(10)), pre="member_contributions", gate=ISAF, ai=20, subj="diplomacy peace")
F("isaf_logistics_pool", 65, 3, "ISAF Logistics Pool",
  "Pool fuel, ammunition and spare parts so that any member's unit can draw from any member's depot.",
  R(tech("logistics_tech", 0.5)), pre="member_contributions", gate=ISAF, ai=25, subj="logistics diplomacy")
F("isaf_signals_net", 69, 3, "ISAF Signals Net",
  "Build a common signals net with shared codes and shared frequencies.",
  R(tech("encryption_tech", 0.5)), pre="member_contributions", gate=ISAF, ai=25, subj="communications command")
F("los_canas_line", 65, 4, "The Los Canas Line",
  "On 14 September 2003 Stonehenge pushes ISAF back to Los Canas, and its first offensive against the battery fails. Hold the line that remains.",
  R(army(15), ev(40)), pre="charter_articles", gate="has_global_flag = ac_ucw_stage_los_canas", ai=30, subj="security bridge",
  layer="Official", cite="Chronicle, 2003 / 09.14")
F("hold_at_any_cost", 62, 5, "Hold at Any Cost",
  "Hold every position for as long as possible. Each day bought is a day for the reserves.",
  R(timed("hold_at_any_cost", 365), manpower(-5000)), pre="los_canas_line", excl="trade_space_for_time", ai=25, subj="security command")
F("trade_space_for_time", 68, 5, "Trade Space for Time",
  "Fall back in good order and keep the army whole. Ground can be retaken; soldiers cannot be replaced.",
  R(timed("trade_space", 365), army(10)), pre="los_canas_line", excl="hold_at_any_cost", ai=10, subj="logistics command")
F("evacuate_federal_assets", 65, 6, "Evacuate Federal Assets",
  "Move aircraft, ships, records and specialists out of reach of the advance.",
  R(air(15), navy(10)), pre="hold_at_any_cost|trade_space_for_time", ai=25, subj="logistics navy")
F("north_point_exile", 65, 7, "Exile at North Point",
  "On 16 September 2004 ISAF establishes its headquarters in North Point. Driven from the continent, the alliance rebuilds on the islands.",
  R(air(20), ev(41)), pre="evacuate_federal_assets", gate="has_global_flag = ac_ucw_stage_north_point", ai=30, subj="navy runway",
  layer="Official", cite="Chronicle, 2004 / 09.16")
F("concentrate_at_north_point", 62, 8, "Concentrate at North Point",
  "Bring every federal unit that can reach the islands to North Point. Rebuild there, then return together.",
  R(timed("concentrated_exile", 365), army(10)), pre="north_point_exile", excl="foothold_on_the_continent", ai=25, subj="navy logistics")
F("foothold_on_the_continent", 68, 8, "A Foothold on the Continent",
  "Keep the units still fighting on the continent supplied, however thinly. A foothold now is a beachhead later.",
  R(timed("continental_foothold", 365), stab(-0.01)), pre="north_point_exile", excl="concentrate_at_north_point", ai=10, subj="security logistics")
F("training_in_exile", 65, 9, "Training in Exile",
  "Turn the islands into training grounds: ranges, airfields and the drills the return will need.",
  R(army(15), air(10)), pre="concentrate_at_north_point|foothold_on_the_continent", ai=25, subj="training runway")
F("saint_ark_withdrawal", 61, 10, "Cover the Saint Ark Withdrawal",
  "On 10 October 2004 the Mount Shezna radar is destroyed to cover the ISAF retreat from Saint Ark. Bring the withdrawn units home to the islands.",
  R(air(10), manpower(3000)), pre="training_in_exile", gate=brief("shezna"), ai=25, subj="radar air", layer="Official", cite="Chronicle, 2004 / 10.10")
F("comberth_harbor", 65, 10, "Comberth Harbor",
  "On 23 November 2004 ISAF sinks the Aegir fleet at Comberth Harbor. The sea approaches to the continent are opening.",
  R(navy(20)), pre="training_in_exile", gate=brief("comberth"), ai=25, subj="navy air", layer="Official", cite="Chronicle, 2004 / 11.23")
F("comona_islands", 69, 10, "Over the Comona Islands",
  "On 31 December 2004 a large air battle is fought over the Comona Islands. The federal wings learn what the return will cost.",
  R(air(20)), pre="training_in_exile", gate=brief("comona"), ai=25, subj="air medal", layer="Official", cite="Chronicle, 2004 / 12.31")
F("plans_for_return", 65, 11, "Plans for the Return",
  "Plan the return to the continent: where to land, what to bring and what to do on the first day ashore.",
  R(army(15), ev(42)), pre="saint_ark_withdrawal|comberth_harbor|comona_islands|training_in_exile", ai=30, subj="command carrier")
F("landing_rehearsals", 62, 12, "Landing Rehearsals",
  "Rehearse the landing on the islands' beaches until every unit knows its place in the order.",
  R(timed("landing_rehearsals", 365)), pre="plans_for_return", excl="deception_plan", ai=25, subj="carrier training")
F("deception_plan", 68, 12, "A Deception Plan",
  "Let the enemy prepare for the wrong landing. Dummy traffic, false orders and a feint where it is least expected.",
  R(timed("deception_plan", 365)), pre="plans_for_return", excl="landing_rehearsals", ai=10, subj="communications security")

section("air", WAR)
F("air_wings_review", 76, 0, "The Air Wings Review",
  "The federal air arm reviews its wings for the new century: what it flies, who flies it and what the debris has taught about flying at all.",
  R(air(15), ev(43)), gate="date > 2000.12.31", ai=30, subj="air document")
F("air_superiority_doctrine", 72, 1, "Air Superiority Doctrine",
  "Win the sky first. Every other mission depends on it.",
  R(idea("air_superiority_doctrine")), pre="air_wings_review", excl="precision_strike_doctrine|electronic_warfare_doctrine", ai=25, subj="air security")
F("precision_strike_doctrine", 76, 1, "Precision Strike Doctrine",
  "Build the wings around precise strikes on the targets that matter most.",
  R(idea("precision_strike_doctrine")), pre="air_wings_review", excl="air_superiority_doctrine|electronic_warfare_doctrine", ai=10, subj="air missile")
F("electronic_warfare_doctrine", 80, 1, "Electronic Warfare Doctrine",
  "Blind the enemy's radars and let the wings fly unseen.",
  R(idea("electronic_warfare_doctrine")), pre="air_wings_review", excl="air_superiority_doctrine|precision_strike_doctrine", ai=10, subj="radar air")
F("interceptor_alerts", 72, 2, "Interceptor Alerts",
  "Keep interceptors on alert at every major airfield, ready in minutes.",
  R(tech("light_fighter", 0.5)), pre="air_superiority_doctrine", ai=25, subj="air runway")
F("strike_packages", 76, 2, "Strike Packages",
  "Plan strike packages of escorts, jammers and strike aircraft that train and fly together.",
  R(tech("tactical_bomber", 0.5)), pre="precision_strike_doctrine", ai=25, subj="air command")
F("jamming_pods", 80, 2, "Jamming Pods",
  "Equip the wings with jamming pods and the crews to use them.",
  R(tech("electronics", 0.5)), pre="electronic_warfare_doctrine", ai=25, subj="radar tools")
F("aircrew_pipeline", 74, 3, "Aircrew Pipeline",
  "Train replacement aircrew faster without training them worse.",
  R(timed("aircrew_pipeline", 730), air(10)), pre="interceptor_alerts|strike_packages", ai=25, subj="training air")
F("tanker_fleet", 78, 3, "Tanker Fleet",
  "Expand the tanker fleet so that the wings can reach the whole continent.",
  R(tech("air_doctrine", 0.5)), pre="strike_packages|jamming_pods", ai=25, subj="air logistics")
F("railgun_evasion", 76, 4, "Railgun Evasion Training",
  "Erusea now holds Stonehenge and turns its railguns on aircraft. Train every crew to fly where the battery cannot reach.",
  R(air(20), ev(44)), pre="aircrew_pipeline|tanker_fleet", gate="has_global_flag = ac_ucw_stonehenge_seized", ai=30, subj="air radar",
  layer="Official", cite="Chronicle, 2003 / SUMMER")
F("low_level_profiles", 74, 5, "Low-Level Profiles",
  "Fly low, under the battery's reach and under the radars.",
  R(timed("low_level_profiles", 730)), pre="railgun_evasion", excl="high_altitude_profiles", ai=25, subj="air training")
F("high_altitude_profiles", 78, 5, "High-Altitude Profiles",
  "Fly high and fast, and stay out of the battery's arcs.",
  R(timed("high_altitude_profiles", 730)), pre="railgun_evasion", excl="low_level_profiles", ai=10, subj="air radar")
F("rebuilding_the_wings", 76, 6, "Rebuilding the Wings",
  "Rebuild the wings at North Point with the aircraft that escaped and the crews that survived.",
  R(air(20), manpower(2000)), pre="low_level_profiles|high_altitude_profiles", gate="has_global_flag = ac_ucw_stage_north_point", ai=30,
  subj="air rebuild", cite="Chronicle, 2004 / 09.16")
F("island_maintenance_depots", 72, 7, "Island Maintenance Depots",
  "Build maintenance depots on the islands so that damaged aircraft fly again within days.",
  R(tech("industry", 0.5)), pre="rebuilding_the_wings", ai=25, subj="tools air")
F("airborne_early_warning", 76, 7, "Airborne Early Warning",
  "Keep early-warning aircraft over the front so that the wings always see first.",
  R(tech("radar_tech", 0.5)), pre="rebuilding_the_wings", ai=25, subj="radar air")
F("combat_search_and_rescue", 80, 7, "Combat Search and Rescue",
  "Bring back every downed crew that can be reached. Pilots fly better when they know someone will come.",
  R(air(10), stab(0.01)), pre="rebuilding_the_wings", ai=25, subj="medical air")
F("recognise_the_aces", 76, 8, "Recognise the Aces",
  "Recognise the pilots whose records stand out. Their example teaches faster than any manual.",
  R(idea("aces_recognised")), pre="island_maintenance_depots|airborne_early_warning|combat_search_and_rescue", ai=25, subj="medal air")
F("partner_air_contingents", 74, 9, "Partner Air Contingents",
  "Fly the partners' squadrons under ISAF command beside the federal wings.",
  R(timed("partner_air", 730), air(10)), pre="recognise_the_aces", excl="federal_air_command", ai=25, subj="air diplomacy")
F("federal_air_command", 78, 9, "Federal Air Command",
  "Keep the federal wings under federal command and assign partners their own sectors.",
  R(timed("federal_air", 730), air(10)), pre="recognise_the_aces", excl="partner_air_contingents", ai=10, subj="air command")
F("air_supremacy_campaign", 76, 10, "The Air Supremacy Campaign",
  "ISAF returns to the continent. Win the sky over the beachheads and keep it.",
  R(air(25), ev(45)), pre="partner_air_contingents|federal_air_command", gate=COUNTER, ai=30, subj="air security", cite="Chronicle, 2005 / 01.24")
F("wings_over_usea", 76, 11, "Wings over Usea",
  "The federal wings fly over the whole continent again.",
  R(air(20), ws(0.03)), pre="air_supremacy_campaign", ai=30, subj="air medal")

section("liberation", WAR)
F("return_to_usea", 88, 0, "The Return to Usea",
  "On 24 January 2005 ISAF lands on the Usean continent. The Federation is going home.",
  R(army(20), ev(46)), gate=COUNTER, ai=30, subj="carrier air", layer="Official", cite="Chronicle, 2005 / 01.24")
F("beachhead_logistics", 84, 1, "Beachhead Logistics",
  "Keep the beachheads supplied: fuel, ammunition, food and the trucks to move them inland.",
  R(tech("logistics_tech", 0.5)), pre="return_to_usea", gate=COUNTER, ai=25, subj="logistics carrier")
F("liberation_principle", 88, 1, "Liberation, Not Annexation",
  "Every place ISAF frees goes back to the government it belongs to. The Federation takes no territory and redraws no border.",
  R(stab(0.03), ev(47)), pre="return_to_usea", gate=COUNTER, ai=30, subj="peace document")
F("engineers_escape", 92, 1, "The Engineers' Escape",
  "On 14 March 2005 Stonehenge's engineers and their families escape from Erusean custody. They have to be received, sheltered and heard.",
  R(tech("electronics", 0.5), ev(48)), pre="return_to_usea", gate=brief("engineers"), ai=30, subj="refugees science",
  layer="Official", cite="Chronicle, 2005 / 03.14")
F("civil_affairs_directorate", 86, 2, "Civil Affairs Directorate",
  "A federal civil affairs directorate restores services behind the front until local authorities return.",
  R(idea("civil_affairs")), pre="liberation_principle", excl="partner_led_administration", gate=COUNTER, ai=25, subj="civil assembly")
F("partner_led_administration", 90, 2, "Partner-Led Administration",
  "Each liberated area is run by its own government's returning officials, with ISAF support only when asked.",
  R(idea("partner_administration")), pre="liberation_principle", excl="civil_affairs_directorate", gate=COUNTER, ai=10, subj="diplomacy assembly")
F("through_the_tango_line", 84, 3, "Through the Tango Line",
  "On 28 February 2005 ISAF takes Istas Fortress and breaches the Tango Line.",
  R(army(20)), pre="beachhead_logistics", gate=brief("istas"), ai=25, subj="gate security", layer="Official", cite="Chronicle, 2005 / 02.28")
F("restore_the_utilities", 88, 3, "Restore the Utilities",
  "Repair power, water and telephone lines in every liberated town.",
  R(stab(0.02), recovery(3)), pre="civil_affairs_directorate|partner_led_administration", gate=COUNTER, ai=25, subj="rebuild communications")
F("stonehenge_silenced", 92, 3, "Stonehenge Silenced",
  "On 2 April 2005 ISAF destroys Stonehenge. The battery built to defend the world from Ulysses will not fire again.",
  R(ws(0.05), air(15), ev(49)), pre="engineers_escape", gate="has_global_flag = ac_ucw_stonehenge_destroyed", ai=30,
  subj="radar rebuild", layer="Official", cite="Chronicle, 2005 / 04.02; Super Weapons, Stonehenge")
F("assisted_returns", 86, 4, "Assisted Returns",
  "Help refugees go home to the liberated districts as soon as they are safe.",
  R(stab(0.03), recovery(3)), pre="restore_the_utilities", excl="hold_the_camps", gate=COUNTER, ai=25, subj="refugees rebuild")
F("hold_the_camps", 90, 4, "Hold the Camps Until Spring",
  "Keep refugees in the camps until the districts are rebuilt. Safer now, harder later.",
  R(stab(0.01), manpower(3000)), pre="restore_the_utilities", excl="assisted_returns", gate=COUNTER, ai=10, subj="shelter refugees")
F("ice_creek_landing", 82, 5, "The Ice Creek Landing",
  "On 18 June 2005 ISAF lands in the north at Ice Creek.",
  R(navy(15), army(10)), pre="through_the_tango_line", gate=brief("ice_creek"), ai=25, subj="carrier security", layer="Official", cite="Chronicle, 2005 / 06.18")
F("san_salvacion_liberated", 88, 5, "San Salvacion Liberated",
  "On 10 July 2005 San Salvacion is liberated. The Federation's task now is to hand the country back, not to hold it.",
  R(stab(0.03), ws(0.03), ev(50)), pre="assisted_returns|hold_the_camps", gate=brief("san_salvacion"), ai=30, subj="peace rebuild",
  layer="Official", cite="Chronicle, 2005 / 07.10")
F("whiskey_corridor", 94, 5, "The Whiskey Corridor",
  "On 15 August 2005 ISAF breaches the Whiskey Corridor.",
  R(army(15), air(10)), pre="stonehenge_silenced", gate=brief("whiskey"), ai=25, subj="bridge air", layer="Official", cite="Chronicle, 2005 / 08.15")
F("no_federal_flag", 86, 6, "No Federal Flag",
  "Leave no federal flag over liberated San Salvacion. ISAF units fly their own colours beside the host's.",
  R(stab(0.02), pp(20)), pre="san_salvacion_liberated", excl="joint_site_custody", ai=25, subj="peace security")
F("joint_site_custody", 90, 6, "Joint Custody of the Battery Site",
  "Propose joint custody of the ruined battery site with San Salvacion until the wreckage is cleared. The ground stays San Salvacion's.",
  R(pp(10), tech("rocketry", 0.5)), pre="san_salvacion_liberated", excl="no_federal_flag", ai=10, subj="radar document")
F("supply_the_road", 88, 7, "Supply the Road to Farbanti",
  "Push supplies down the road to Farbanti fast enough to keep the advance moving.",
  R(army(15), tech("logistics_tech", 0.5)), pre="no_federal_flag|joint_site_custody|ice_creek_landing|whiskey_corridor", gate=WAR_ON, ai=25,
  subj="logistics bridge")
F("lenient_terms", 86, 8, "Lenient Terms",
  "Prepare surrender terms that leave Erusea a government able to rebuild.",
  R(flag("terms_lenient"), stab(0.02)), pre="supply_the_road", excl="strict_terms", ai=25, subj="peace scales")
F("strict_terms", 90, 8, "Strict Terms",
  "Prepare surrender terms with strict oversight and full accountability.",
  R(flag("terms_strict"), ws(0.03)), pre="supply_the_road", excl="lenient_terms", ai=10, subj="scales security")
F("liberation_accounting", 88, 9, "The Liberation Accounting",
  "Count what the war cost and what liberation has restored. The ledger is long on both sides.",
  R(pp(30), recovery(3)), pre="lenient_terms|strict_terms", ai=25, subj="document rebuild")

section("postwar", WAR)
F("victory_in_usea", 47, 14, "Victory in Usea",
  "On 19 September 2005 Farbanti falls and Erusea surrenders. The Continental War is over.",
  R(stab(0.05), ev(51)), gate="has_global_flag = ac_ucw_outcome_isaf_victory", ai=30, subj="medal peace", layer="Official", cite="Chronicle, 2005 / 09.19")
F("oversight_council", 45, 15, "An Oversight Council",
  "Oversee Erusea's provisional government through a standing ISAF council that meets every week.",
  R(timed("oversight_council", 730), pp(20)), pre="victory_in_usea", excl="light_oversight", ai=25, subj="assembly scales")
F("light_oversight", 49, 15, "Light Oversight",
  "Keep oversight to the terms of surrender and let Erusea's provisional government govern.",
  R(timed("light_oversight", 730), stab(0.02)), pre="victory_in_usea", excl="oversight_council", ai=10, subj="peace document")
F("megalith_aftermath", 47, 16, "After Megalith",
  "On 26 September 2005 young Erusean officers seize Megalith, ISAF destroys it, and Erusea forms a provisional autonomous government under ISAF oversight.",
  R(ws(0.02), stab(0.02), ev(52)), pre="oversight_council|light_oversight", gate="has_global_flag = ac_ucw_megalith_destroyed", ai=30,
  subj="missile peace", layer="Official", cite="Chronicle, 2005 / 09.26; Super Weapons, Megalith")
F("victors_restraint", 47, 17, "The Victor's Restraint",
  "Take no territory and demand no government. The Federation's victory is that the war is over.",
  R(stab(0.03), pp(30)), pre="megalith_aftermath", ai=30, subj="peace scales")
F("federation_endures", 57, 14, "The Federation Endures",
  "In this provisional outcome Erusea has won the war. The Federation has lost battles, ground and allies, but it still governs.",
  R(stab(0.03), ev(53)), gate="has_global_flag = ac_ucw_outcome_erusean_victory", ai=30, subj="shelter assembly")
F("rebuild_the_army", 55, 15, "Rebuild the Army",
  "Rebuild the federal army from the units that came home.",
  R(army(25), manpower(10000)), pre="federation_endures", excl="accept_the_peace", ai=25, subj="command rebuild")
F("accept_the_peace", 59, 15, "Accept the Peace",
  "Accept the peace and spend the next decade on recovery rather than revenge.",
  R(stab(0.04), recovery(5)), pre="federation_endures", excl="rebuild_the_army", ai=10, subj="peace rebuild")
F("survival_compact", 57, 16, "The Survival Compact",
  "Bind the remaining partners in a compact for recovery and mutual defence.",
  R(stab(0.02), pp(30)), pre="rebuild_the_army|accept_the_peace", ai=25, subj="diplomacy shelter")
F("armistice_line", 67, 14, "The Armistice Line",
  "In this provisional outcome the war ends in an armistice. A line on the map divides Usea, and neither side calls it peace.",
  R(stab(0.02), ev(54)), gate="has_global_flag = ac_ucw_outcome_stalemate", ai=30, subj="gate peace")
F("armed_vigilance", 65, 15, "Armed Vigilance",
  "Keep the army at the line and the air arm on alert.",
  R(army(15), air(10)), pre="armistice_line", excl="demilitarised_zone", ai=25, subj="security radar")
F("demilitarised_zone", 69, 15, "A Demilitarised Zone",
  "Propose a demilitarised zone along the line, watched by neutral observers.",
  R(stab(0.03), pp(20)), pre="armistice_line", excl="armed_vigilance", ai=10, subj="peace gate")
F("cold_peace", 67, 16, "A Cold Peace",
  "Live with a peace nobody signed. Trade where possible, watch where necessary.",
  R(stab(0.02), pp(20)), pre="armed_vigilance|demilitarised_zone", ai=25, subj="scales peace")
F("war_that_was_not", 77, 14, "The War That Was Not",
  "In this provisional outcome the continental accord has averted the war. The Federation must build a peace that lasts.",
  R(stab(0.04), ev(55)), gate="has_global_flag = ac_ucw_war_averted", ai=30, subj="peace diplomacy")
F("accord_guarantees", 75, 15, "Accord Guarantees",
  "Guarantee the accord with treaty forces kept ready but at home.",
  R(timed("accord_guarantees", 730), army(10)), pre="war_that_was_not", excl="continental_market", ai=25, subj="security peace")
F("continental_market", 79, 15, "A Continental Market",
  "Bind the accord with trade: lower tariffs and shared reconstruction contracts across Usea.",
  R(timed("continental_market", 730), recovery(4)), pre="war_that_was_not", excl="accord_guarantees", ai=10, subj="economy peace")
F("long_peace", 77, 16, "The Long Peace",
  "The accord holds through 2005. The Federation turns to the recovery the impact demanded.",
  R(stab(0.03), pp(30)), pre="accord_guarantees|continental_market", ai=25, subj="peace rebuild")
F("the_usean_order", 89, 14, "The Usean Order",
  "Whatever the outcome, Usea needs an order that holds after 2005. The Federation must decide what part it plays.",
  R(pp(20), ev(56)), gate=WAR_ENDED, ai=30, subj="assembly diplomacy")
F("standing_isaf", 86, 15, "A Standing ISAF",
  "Keep ISAF's headquarters and staff in peacetime. The alliance has learned too much to forget it.",
  R(timed("standing_isaf", 1095), army(10)), pre="the_usean_order", excl="return_the_staff", gate=ISAF, ai=25, subj="command diplomacy")
F("return_the_staff", 92, 15, "Return the Staff to Peace",
  "Send ISAF's officers home to their own services and keep only a small secretariat.",
  R(stab(0.03), pp(20)), pre="the_usean_order", excl="standing_isaf", ai=10, subj="peace document")
F("veterans_charter", 89, 16, "The Veterans' Charter",
  "Guarantee veterans their care, pensions and places in the reconstruction.",
  R(stab(0.03), manpower(3000)), pre="the_usean_order|standing_isaf|return_the_staff", ai=25, subj="medal civil")
F("order_of_2005", 89, 17, "The Order of 2005",
  "The Federation records the settlement it helped to build. The authored chronology of this campaign ends here.",
  R(stab(0.03), pp(40), ev(57)), pre="veterans_charter", ai=30, subj="document peace")
F("federal_question_answered", 55, 7, "The Federal Question Answered",
  "The government that led the Federation through Ulysses and the war gives its account to the Assembly and the voters.",
  R(stab(0.03), pp(30), ev(58)), pre="postwar_elections_pledge|emergency_continuity", gate=WAR_ENDED, ai=30, subj="ballot assembly")


# =================================================================== IDEAS
# Every value is provisional gameplay. Modifiers are limited to keys already used
# by the mod's own idea files.
IDEAS = []


def I(slug, name, desc, subj="assembly document", **modifiers):
    IDEAS.append(("FCU_ud_" + slug + "_idea", name, desc, tuple(subj.split()), modifiers))


# Politics
I("federal_course", "The Federal Course", "The 1991 government governs as it was elected to govern.", "assembly document",
  political_power_gain=0.05, stability_factor=0.03)
I("decree_programme", "Decree Programme", "Administrative matters move by presidential decree.", "document command",
  political_power_gain=0.1, stability_factor=-0.02)
I("assembly_partnership", "Assembly Partnership", "The Assembly's committee chairs draft major bills with the cabinet.", "assembly diplomacy",
  stability_factor=0.04, political_power_gain=-0.03)
I("ministry_of_preparedness", "Ministry of Preparedness", "One minister answers for every shelter, timetable and stockpile.", "civil assembly",
  production_speed_infrastructure_factor=0.05, political_power_gain=-0.03)
I("interagency_board", "Interagency Emergency Board", "Each ministry keeps its duties; a board coordinates them daily.", "command communications",
  planning_speed=0.05, stability_factor=0.01)
I("emergency_framework", "Emergency Framework", "A statute stands ready to hand authority to a directorate. Alternate history.", "command security",
  war_support_factor=0.03, political_power_gain=0.05)
I("staff_directorate", "Staff Directorate Model", "The directorate is designed as a military staff. Alternate history.", "command training",
  planning_speed=0.05, army_org_factor=0.03)
I("civil_military_board", "Civil-Military Board", "The directorate is designed as a mixed board. Alternate history.", "assembly command",
  stability_factor=0.03, drift_defence_factor=0.1)
I("directorate_rule", "Unified Command Directorate", "A directorate built around Unified Command governs the Federation. Alternate history; provisional gameplay.", "command assembly",
  stability_factor=0.05, war_support_factor=0.05, political_power_gain=0.1, drift_defence_factor=0.25, consumer_goods_factor=0.02)
I("martial_evacuation", "Martial Evacuation Law", "The evacuation programme is under military law. Alternate history.", "refugees security",
  production_speed_infrastructure_factor=0.1, stability_factor=-0.03)
I("loyalty_reviews", "Loyalty Reviews", "Officers from commands that went silent are under review. Alternate history.", "security document",
  drift_defence_factor=0.2, army_morale_factor=-0.03)
I("extended_directorate", "Extended Directorate", "The directorate's mandate has been renewed until the danger passes. Alternate history.", "command meteor",
  war_support_factor=0.05, political_power_gain=0.1, stability_factor=-0.03, drift_defence_factor=0.2)
I("restored_assembly", "Restored Assembly", "Executive authority has returned to the presidency and the Assembly. Alternate history.", "ballot assembly",
  stability_factor=0.05, democratic_drift=0.02)
I("regional_ministers", "Regional Ministers", "The unity cabinet's ministers answer to the regions. Alternate history.", "assembly civil",
  stability_factor=0.04, political_power_gain=-0.03)
I("technocratic_ministers", "Technocratic Ministers", "Specialists without party hold the key ministries. Alternate history.", "science assembly",
  research_speed_factor=0.03, stability_factor=-0.01)
I("unity_cabinet", "Federal Unity Cabinet", "Every Assembly party sits in the government. Alternate history; provisional gameplay.", "assembly ballot",
  stability_factor=0.08, political_power_gain=-0.05, drift_defence_factor=0.15)
I("burden_sharing", "Burden-Sharing Act", "Preparedness costs are spread across the regions by formula. Alternate history.", "scales economy",
  consumer_goods_factor=-0.01, stability_factor=0.01)
I("regional_autonomy", "Regional Autonomy Charter", "The regions control their own preparedness budgets. Alternate history.", "assembly civil",
  stability_factor=0.03, production_speed_buildings_factor=0.03)
I("unity_emergency_cabinet", "Unity Emergency Cabinet", "An all-party emergency cabinet meets daily. Alternate history.", "civil command",
  planning_speed=0.05, stability_factor=0.02)
# Economy
I("continental_trade", "Continental Trade Programme", "Treaty partners trade with the Federation on easier terms.", "economy diplomacy",
  consumer_goods_factor=-0.02, trade_opinion_factor=0.1)
I("federal_industry", "Federal Industrial Policy", "Federal credit flows to emergency industries.", "industry economy",
  production_factory_efficiency_gain_factor=0.05, consumer_goods_factor=0.01)
I("ulysses_bonds", "Ulysses Bonds", "Preparedness is paid for with long-dated bonds.", "economy meteor",
  production_speed_buildings_factor=0.05, political_power_gain=-0.03)
I("emergency_levy", "The Emergency Levy", "A temporary levy pays for preparedness now.", "scales meteor",
  production_speed_buildings_factor=0.05, stability_factor=-0.02)
I("impact_insurance", "Impact Insurance Pool", "Losses from the impact will be rebuilt by formula.", "shelter scales",
  stability_factor=0.03)
I("strategic_stockpile", "Strategic Stockpile Law", "Firms hold six months of critical inputs.", "logistics industry",
  production_factory_max_efficiency_factor=0.03, consumer_goods_factor=0.01)
# Treaty
I("treaty_secretariat", "Treaty Secretariat", "The Treaty Organization has a standing secretariat. Mod provenance UTO.", "assembly diplomacy",
  political_power_gain=0.03, opinion_gain_monthly_factor=0.1)
I("integrated_treaty_staff", "Integrated Treaty Staff", "The members plan through one treaty staff.", "command diplomacy",
  planning_speed=0.05, army_org_factor=0.03)
I("national_contingents", "National Contingents", "Each member keeps its forces under its own command.", "security diplomacy",
  army_morale_factor=0.03, training_time_army_factor=-0.05)
I("western_watch", "The Western Watch", "A standing treaty watch faces the western frontier.", "radar security",
  army_core_defence_factor=0.05)
I("federal_subsidy", "Federal Treaty Subsidy", "The Federation pays the treaty's common costs.", "economy diplomacy",
  political_power_gain=-0.05, opinion_gain_monthly_factor=0.15)
I("shared_assessment", "Shared Assessment Scale", "Members pay the treaty's costs by the size of their economies.", "scales economy",
  political_power_gain=0.03)
I("treaty_air_picture", "Treaty Air Picture", "The members share one radar picture.", "radar air",
  air_mission_efficiency=0.05, air_detection=0.05)
I("treaty_relief_command", "Treaty Relief Command", "A treaty command owns the relief stores and transport.", "medical logistics",
  supply_consumption_factor=-0.03, stability_factor=0.02)
# Skully Islands
I("southern_tribunals", "Southern Tribunals", "Rebels from the southern islands are tried in federal courts.", "scales security",
  drift_defence_factor=0.1)
I("southern_garrison", "Southern Garrison", "A permanent garrison holds the southern islands.", "security rebuild",
  army_core_defence_factor=0.05, stability_factor=0.01)
I("island_reconstruction", "Island Reconstruction", "The southern islands are being rebuilt by their own firms.", "rebuild tools",
  stability_factor=0.03, production_speed_infrastructure_factor=0.05)
I("coast_guard", "Southern Coast Guard", "A federal coast guard polices the southern waters.", "navy document",
  naval_coordination=0.05)
# Evacuation and Stonehenge
I("dispersal_doctrine", "Dispersal Doctrine", "The evacuation spreads people across the interior.", "refugees rail",
  production_speed_infrastructure_factor=0.1, consumer_goods_factor=0.01)
I("hardened_shelters", "Hardened Shelters", "Public shelters keep people near home.", "shelter industry",
  production_speed_bunker_factor=0.1, stability_factor=0.02)
I("stonehenge_consortium", "Stonehenge Consortium", "Central Usea leads the international railgun project. Official: Chronicle, 1998 / 06.19.", "radar diplomacy",
  research_speed_factor=0.02, political_power_gain=-0.03)
# Coup
I("coup_tribunals", "Coup Tribunals", "The coup's leaders face federal tribunals.", "scales security",
  drift_defence_factor=0.2, stability_factor=-0.01)
I("coup_reconciliation", "Reconciliation Hearings", "Officers who joined the coup are heard before anyone is tried.", "peace scales",
  stability_factor=0.03, army_morale_factor=0.02)
I("civilian_control", "Civilian Control Act", "Every deployment order carries a minister's signature.", "assembly document",
  political_power_gain=0.05, planning_speed=-0.03)
I("command_autonomy", "Command Autonomy Charter", "Unified Command may act without ministers in a declared emergency.", "command security",
  planning_speed=0.08, army_org_factor=0.03, political_power_gain=-0.05)
I("coup_warning_net", "Coup-Warning Net", "Treaty command centres watch for silent garrisons.", "communications radar",
  drift_defence_factor=0.1, army_org_factor=0.02)
I("federal_security_service", "Federal Security Service", "A federal service investigates officers.", "security assembly",
  drift_defence_factor=0.25, stability_factor=-0.02)
# Impact relief
I("relief_corps", "Federal Relief Corps", "A federal civil corps runs the relief effort.", "civil medical",
  stability_factor=0.03, production_speed_infrastructure_factor=0.05)
I("treaty_relief", "Treaty Relief Compact", "The treaty partners share the relief effort.", "diplomacy medical",
  stability_factor=0.02, opinion_gain_monthly_factor=0.1)
I("military_relief", "Military Relief Command", "The army runs the relief effort.", "command shelter",
  production_speed_infrastructure_factor=0.08, stability_factor=-0.01)
I("impact_aftershock_light", "Impact Aftershock", "The Federation absorbs the impact with its plans intact.", "meteor shelter",
  stability_factor=-0.02, consumer_goods_factor=0.01)
I("impact_aftershock", "Impact Strain", "The impact has strained the Federation's plans.", "meteor civil",
  stability_factor=-0.05, consumer_goods_factor=0.03, production_speed_buildings_factor=-0.05)
I("impact_aftershock_severe", "Impact Emergency", "The impact has overwhelmed the Federation's plans.", "meteor refugees",
  stability_factor=-0.08, consumer_goods_factor=0.05, production_speed_buildings_factor=-0.1, war_support_factor=-0.05)
I("relief_work_continues", "Relief Work Continues", "The relief lane chosen in 1999 continues into the new century.", "rebuild civil",
  stability_factor=0.02, production_speed_infrastructure_factor=0.05)
# Forces
I("air_arm_first", "The Air Arm First", "The air arm comes first in the federal budget.", "air economy",
  experience_gain_air_factor=0.1, air_accidents_factor=-0.1)
I("balanced_forces", "Balanced Forces", "The services are funded in proportion.", "command scales",
  experience_gain_army_factor=0.05, experience_gain_air_factor=0.05)
I("reserve_wings", "Reserve Wings", "Reserve pilots fly every year.", "air training",
  air_ace_generation_chance_factor=0.1, air_accidents_factor=-0.05)
I("rapid_reaction", "Rapid-Reaction Brigades", "Two brigades stand at short notice.", "security logistics",
  mobilization_speed=0.05, army_org_factor=0.02)
# War tree: aftermath and home front
I("open_camps", "Open Federal Camps", "Federal camps receive refugees turned away elsewhere.", "shelter refugees",
  stability_factor=-0.02, monthly_population=0.05)
I("resettlement_quotas", "Resettlement Quotas", "Treaty partners share the refugees by quota.", "diplomacy refugees",
  stability_factor=0.02, political_power_gain=-0.03)
I("forward_deterrence", "Forward Deterrence", "Federal units stand forward and visible.", "security command",
  army_core_defence_factor=0.05, war_support_factor=0.03, stability_factor=-0.01)
I("continental_restraint", "Continental Restraint", "The federal posture stays defensive and at home.", "peace command",
  stability_factor=0.03, war_support_factor=-0.02)
I("national_mobilisation", "National Mobilisation", "Every reserve is called and the economy is on a war footing.", "command industry",
  conscription_factor=0.1, production_speed_arms_factory_factor=0.05, stability_factor=-0.03)
I("measured_mobilisation", "Measured Mobilisation", "Reserves are called in stages.", "scales command",
  conscription_factor=0.05, stability_factor=0.02)
I("war_bonds", "War Bonds", "Citizens and partners are paying for the war over decades.", "economy medal",
  war_support_factor=0.03, political_power_gain=0.03)
I("allied_credit", "Allied Credit", "Credit from allies beyond Usea pays for the war.", "diplomacy economy",
  production_speed_buildings_factor=0.05, political_power_gain=-0.03)
I("directorate_war_footing", "Directorate War Footing", "The directorate prepares for war. Alternate history.", "command security",
  planning_speed=0.05, war_support_factor=0.05, stability_factor=-0.02)
# ISAF and exile
I("isaf_integrated_staff", "Integrated ISAF Staff", "ISAF plans through one combined headquarters.", "command diplomacy",
  planning_speed=0.08, army_org_factor=0.03)
I("isaf_lead_nation", "Lead-Nation Command", "Central Usea leads ISAF directly.", "command security",
  army_attack_factor=0.03, political_power_gain=0.03)
I("hold_at_any_cost", "Hold at Any Cost", "Every position is held for as long as possible.", "security command",
  army_defence_factor=0.05, dig_in_speed_factor=0.1)
I("trade_space", "Trade Space for Time", "The army falls back in good order.", "logistics command",
  army_speed_factor=0.05, army_org_factor=0.03)
I("concentrated_exile", "Concentrated at North Point", "Federal units gather and rebuild at North Point.", "navy logistics",
  training_time_army_factor=-0.1, experience_gain_army_factor=0.05)
I("continental_foothold", "A Foothold on the Continent", "Units still fighting on the continent are kept supplied.", "security logistics",
  army_core_defence_factor=0.05, supply_consumption_factor=0.03)
I("landing_rehearsals", "Landing Rehearsals", "Every unit knows its place in the landing.", "carrier training",
  naval_coordination=0.05, army_org_factor=0.02)
I("deception_plan", "Deception Plan", "The enemy expects the wrong landing.", "communications security",
  army_attack_factor=0.03, encryption_factor=0.05)
# Air wings
I("air_superiority_doctrine", "Air Superiority Doctrine", "The wings fight for the sky first.", "air security",
  air_superiority_efficiency=0.05, experience_gain_air_factor=0.05)
I("precision_strike_doctrine", "Precision Strike Doctrine", "The wings strike the targets that matter most.", "air missile",
  air_cas_efficiency=0.05, air_strategic_bomber_bombing_factor=0.05)
I("electronic_warfare_doctrine", "Electronic Warfare Doctrine", "The wings blind the enemy's radars.", "radar air",
  air_mission_efficiency=0.05, air_detection=0.05)
I("aircrew_pipeline", "Aircrew Pipeline", "Replacement aircrew train faster.", "training air",
  experience_gain_air_factor=0.05, air_accidents_factor=-0.05)
I("low_level_profiles", "Low-Level Profiles", "Crews fly under the battery's reach.", "air training",
  air_mission_efficiency=0.03, air_accidents_factor=0.03)
I("high_altitude_profiles", "High-Altitude Profiles", "Crews fly high and fast.", "air radar",
  air_superiority_efficiency=0.03)
I("aces_recognised", "The Aces Recognised", "Outstanding pilots teach by example.", "medal air",
  air_ace_generation_chance_factor=0.15, experience_gain_air_factor=0.05)
I("partner_air", "Partner Air Contingents", "Partner squadrons fly under ISAF command.", "air diplomacy",
  air_mission_efficiency=0.03, opinion_gain_monthly_factor=0.05)
I("federal_air", "Federal Air Command", "Federal wings keep federal command.", "air command",
  air_superiority_efficiency=0.03, political_power_gain=0.02)
# Liberation and postwar
I("civil_affairs", "Civil Affairs Directorate", "A federal directorate restores services behind the front.", "civil assembly",
  production_speed_infrastructure_factor=0.08, stability_factor=0.02)
I("partner_administration", "Partner-Led Administration", "Liberated areas are run by their own returning officials.", "diplomacy assembly",
  stability_factor=0.03, opinion_gain_monthly_factor=0.1)
I("oversight_council", "Oversight Council", "A standing ISAF council oversees Erusea's provisional government.", "assembly scales",
  political_power_gain=0.05, stability_factor=0.01)
I("light_oversight", "Light Oversight", "Oversight is limited to the terms of surrender.", "peace document",
  stability_factor=0.03, political_power_gain=-0.02)
I("accord_guarantees", "Accord Guarantees", "Treaty forces stand ready to guarantee the accord.", "security peace",
  army_core_defence_factor=0.05, stability_factor=0.02)
I("continental_market", "Continental Market", "Trade binds the continental accord.", "economy peace",
  consumer_goods_factor=-0.02, trade_opinion_factor=0.1)
I("standing_isaf", "A Standing ISAF", "ISAF's staff remains in peacetime.", "command diplomacy",
  planning_speed=0.05, army_org_factor=0.02)


# =================================================================== FLAG AND VARIABLE LABELS
# Every has_*_flag in this package has a readable label. Flags owned by ac_ur
# have no labels of their own, so this package supplies them.
FLAG_LABELS = {
    "ac_ur_skully_recorded": "The Skully Islands action has been recorded",
    "ac_ur_coup_started": "The 1997 coup has broken out",
    "ac_ur_coup_defeated": "Unified Command has defeated the 1997 coup",
    "ac_ur_coup_prolonged": "The 1997 emergency has been prolonged",
    "FCU_ud_gov_directorate": "The Unified Command directorate governs (alternate history)",
    "FCU_ud_gov_unity": "The federal unity government governs (alternate history)",
    "FCU_ud_gov_restored": "Civilian rule has been restored (alternate history)",
    "FCU_ud_path_course": "Political path: the federal course",
    "FCU_ud_path_directorate": "Political path: the emergency directorate (alternate history)",
    "FCU_ud_path_unity": "Political path: the unity government (alternate history)",
    "FCU_ud_impact_prepared": "The Federation met the impact prepared",
    "FCU_ud_impact_strained": "The impact strained the Federation",
    "FCU_ud_impact_overwhelmed": "The impact overwhelmed the Federation",
    "FCU_ud_impact_tallied": "The impact has been tallied",
    "FCU_ud_carryover_done": "The opening decade has been carried into the Usean calendar",
    "FCU_ud_relief_lane_finished": "A relief lane has been completed",
}
# Remaining FCU_ud flags take their label from the focus that sets them.
VARIABLE_LABELS = {"FCU_ud_readiness": "Evacuation Readiness"}
TOOLTIPS = {
    "FCU_ud_readiness_tt": "Evacuation Readiness, Central Usea's own preparedness index, is read once when Ulysses arrives on 8 July 1999: 60 or more meets the impact prepared, 30 or more strained, below 30 overwhelmed.",
    "FCU_ud_regime_tt": "Alternate history: the government changes. No source shows a Central Usea regime change before ISAF's founding on 22 August 2003, and the AI never takes this path.",
}
