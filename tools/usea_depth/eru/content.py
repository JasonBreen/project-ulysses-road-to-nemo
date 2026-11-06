"""Usea Depth: Erusea (package eru). Focus, idea and leader data.

Everything here is provisional gameplay or mod provenance unless a row cites the
official ACES Chronicle; docs/usea_depth/ERU.md is generated from these tables.
No new named people, no state mapping beyond the existing Stonehenge contract,
no construction dates for Megalith or Stonehenge, and no ownership changes.

Opening tree (ac_exp_eru_opening, 1991-1999): x <= 23, y >= 6. Every focus is
gated `date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started }`.
War tree (ac_ucw_eru_tree, 2000-2005 and the postwar lanes): x 42-94.
Government changes happen only in ac_ud_eru_regime_* effects (see build.py),
reached only by focuses with ai_will_do 0.
"""
from dataclasses import dataclass, field

PACKAGE = "eru"
TAG = "ERU"
NAMESPACE = "ac_ud_eru"
OPENING_TREE = "ac_exp_eru_opening"
WAR_TREE = "ac_ucw_eru_tree"

# Era bands of the opening tree. Dates are the official Chronicle anchors; the
# Erusean responses gated by them are provisional gameplay.
BANDS = {
    "ulysses": ("date > 1996.4.19", "Chronicle, 1996 / 04.20: Central Usea announces Ulysses will strike Earth"),
    "coup": ("date > 1997.5.29", "Chronicle, 1997 / 05.30: a coup breaks out across Usea"),
    "stonehenge": ("date > 1998.6.18", "Chronicle, 1998 / 06.19: Stonehenge is completed in San Salvacion"),
    "impact": ("date > 1999.7.7", "Chronicle, 1999 / 07.08: Ulysses passes the Roche limit"),
    "war": ("has_global_flag = ac_ucw_war_started", "Chronicle, 2003 / SUMMER: Erusea invades San Salvacion"),
}

OPENING_GATE = "original_tag = ERU ac_exp_eligible = yes date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started }"
WAR_GATE = "original_tag = ERU ac_ucw_active = yes"


@dataclass
class Focus:
    slug: str
    x: int
    y: int
    title: str
    desc: str
    reward: str = ""
    pre: tuple = ()
    excl: tuple = ()
    cost: int = 5
    ai: int = 20
    band: str = ""
    gate: str = ""
    art: tuple = ("document", "command")
    lane: str = ""
    tree: str = "opening"
    event: int = 0

    @property
    def id(self):
        return "ERU_ud_" + self.slug


FOCUSES = []
_lane = {"lane": "", "tree": "opening"}


def lane(name, tree=None):
    _lane["lane"] = name
    if tree:
        _lane["tree"] = tree


def F(slug, x, y, title, desc, reward="", pre=(), excl=(), cost=5, ai=20, band="", gate="", art=("document", "command"), event=0):
    if isinstance(pre, str):
        pre = (pre,)
    if isinstance(excl, str):
        excl = (excl,)
    if isinstance(reward, (list, tuple)):
        reward = "\n".join(r for r in reward if r)
    FOCUSES.append(Focus(slug, x, y, title, " ".join(desc.split()), reward, tuple(pre), tuple(excl), cost, ai, band, gate,
                         tuple(art), _lane["lane"], _lane["tree"], event))


# ---------------------------------------------------------------- reward helpers
def num(value):
    text = format(value, ".3f").rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def idea(name):
    return "add_ideas = " + name


def swap(old, new):
    return "remove_ideas = %s\nadd_ideas = %s" % (old, new)


def drop(name):
    return "remove_ideas = " + name


def flag(name):
    return "set_country_flag = " + name


def pp(n):
    return "add_political_power = %d" % n


def stab(v):
    return "add_stability = " + num(v)


def ws(v):
    return "add_war_support = " + num(v)


def xp(kind, n):
    return "%s_experience = %d" % (kind, n)


def tech(category, bonus=0.5):
    # {id} is filled in with the focus ID, which also names the bonus.
    return "add_tech_bonus = { name = {id} bonus = %s uses = 1 category = %s }" % (num(bonus), category)


def pop(ideology, v):
    return "add_popularity = { ideology = %s popularity = %s }" % (ideology, num(v))


def fiscal(effect):
    return "if = { limit = { ac_econ_ready = yes } %s = yes }" % effect


def timed(name, days):
    return "add_timed_idea = { idea = %s days = %d }" % (name, days)


def manpower(n):
    return "add_manpower = %d" % n


def ucw(grievance=0, pressure=0, recovery=0):
    """Continental War indices; only valid in the war tree, after the calendar start."""
    lines = ["add_to_variable = { ac_ucw_%s = %d }" % (name, value)
             for name, value in (("grievance", grievance), ("pressure", pressure), ("recovery", recovery)) if value]
    return "\n".join(lines + ["ac_ucw_bound = yes"])


def done(slug):
    return "has_completed_focus = ERU_ud_" + slug


# ================================================================ OPENING TREE
# Court trunk: under ERU_exp_opening_assessment (10, 5).
lane("court", "opening")
F("crown_and_court", 9, 6, "The Crown and the Court",
  """The opening reviews closed on a question nobody in Farbanti wanted to answer aloud: who actually governs
  Erusea between royal audiences? The palace offices, the cabinet secretaries and the general staff each keep
  their own registers. Begin with an honest map of the court.""",
  [idea("ERU_ud_court_ledger")], pre="ERU_exp_opening_assessment", ai=30, art=("document", "assembly"), event=1)
F("palace_chancery", 5, 7, "The Palace Chancery",
  """Seven royal secretariats answer letters, sign warrants and lose each other's files. Fold them into one
  chancery with one register of decrees, so a signature in the palace means the same thing in every ministry.""",
  [swap("ERU_ud_court_ledger", "ERU_ud_court_chancery")], pre="crown_and_court", ai=30, art=("document", "communications"))
F("privy_council_minutes", 9, 7, "Privy Council Minutes",
  """The Privy Council has met for a century without a written record of what it decided or why. From this
  session onward a clerk sits at the end of the table, and the minutes are kept in the palace archive.""",
  [stab(0.03), flag("ERU_ud_council_minuted")], pre="crown_and_court", ai=30, art=("document", "scales"))
F("civil_list_audit", 13, 7, "Audit the Civil List",
  """The Crown's household is paid from a civil list that nobody outside the palace has read since the last
  succession. An audit by the treasury will not be popular at court, but it removes the cheapest argument
  the reformers have.""",
  [pp(-20), stab(0.02), flag("ERU_ud_civil_list_audited")], pre="crown_and_court", ai=25, art=("economy", "document"))
F("royal_progress", 5, 8, "A Royal Progress",
  """For the first time in a generation the monarch leaves the capital for a month, by rail and by road, to
  be seen in the district towns. The court calls it a progress. The provinces will call it what they see.""",
  [ws(0.03), stab(0.02)], pre="palace_chancery", ai=30, art=("rail", "medal"), event=6)
F("succession_statute", 9, 8, "The Succession Statute",
  """The rules of succession live in precedent, in letters patent and in the memories of three elderly
  courtiers. Codify them in a single statute, so that no faction can ever claim the throne is in doubt.""",
  [stab(0.03), flag("ERU_ud_succession_settled")], pre="privy_council_minutes", ai=30, art=("scales", "document"))
F("crown_estates_lease", 13, 8, "Lease the Crown Estates",
  """The Crown owns farmland, forest and harbour frontage that earn almost nothing. Long leases to district
  cooperatives and shipping firms would fund public works without a new tax, and tie the estates' tenants to
  the palace's fortunes.""",
  [idea("ERU_ud_crown_estates")], pre="civil_list_audit", ai=25, art=("economy", "fishing"))
F("court_of_petitions", 5, 9, "The Court of Petitions",
  """Once a month the palace gates open to anyone with a written grievance. Clerks sort the petitions; the
  monarch hears a few in person. It costs an afternoon and earns a reputation for listening.""",
  [stab(0.02), pop("monarchism", 0.02)], pre="royal_progress", ai=25, art=("document", "civil"))
F("palace_archive", 13, 9, "Open the Palace Archive",
  """Historians and engineers have petitioned for decades to read the palace's survey records, harbour charts
  and old treaty files. Opening the reading room flatters the universities and costs the court nothing it
  still needs to hide.""",
  [tech("electronics", 0.5)], pre="crown_estates_lease", ai=20, art=("science", "document"))
F("crowns_question", 9, 9, "The Crown's Question",
  """Every review in the court ledger ends at the same place. Erusea is governed by a monarchy whose ministers
  answer to the palace, an officer corps that answers to itself, and a public that answers to nobody. Somebody
  will settle the question. Better that the Crown asks it first.""",
  [flag("ERU_ud_question_posed")], pre=("succession_statute", "royal_progress|crown_estates_lease"), cost=10, ai=30,
  art=("scales", "assembly"), event=2)

# Political path openers, mutually exclusive. Only the Crown path is open to the AI.
F("path_prerogative", 5, 10, "Rule by Prerogative",
  """The Crown answers its own question: Erusea will be governed as it always has been, by royal prerogative,
  through ministers who serve at the palace's pleasure. The court will be modernized, not shared.""",
  [flag("ERU_ud_course_crown"), swap("ERU_ud_court_chancery", "ERU_ud_prerogative_rule")],
  pre="crowns_question", excl=("path_constitution", "path_regency"), cost=10, ai=60, art=("command", "medal"), event=3)
F("path_constitution", 9, 10, "Toward a Constitution",
  """The Crown answers by giving part of the answer away. A written constitution, an elected assembly and a
  cabinet responsible to it, with the monarchy kept above politics. Provisional gameplay: no official source
  describes Erusean reform before 2005.""",
  [flag("ERU_ud_course_constitution"), drop("ERU_ud_court_chancery"), idea("ERU_ud_drafting_commission_idea")],
  pre="crowns_question", excl=("path_prerogative", "path_regency"), cost=10, ai=0, art=("ballot", "document"), event=4)
F("path_regency", 13, 10, "The General Staff Steps In",
  """The general staff answers for the Crown. Its memorandum proposes a regency council of serving officers to
  run the ministries as a command administration until the country is 'secure'. Provisional gameplay: an
  alternate-history path with no official source.""",
  [flag("ERU_ud_course_regency"), drop("ERU_ud_court_chancery")],
  pre="crowns_question", excl=("path_prerogative", "path_constitution"), cost=10, ai=0, art=("command", "security"), event=5)

# ---------------------------------------------------------------- Crown absolutism (AI path), x 4/6
lane("crown")
F("cabinet_of_secretaries", 4, 11, "A Cabinet of Secretaries",
  """Ministers become royal secretaries, appointed and dismissed by the palace and answerable to no assembly.
  The cabinet meets in the chancery rooms. Policy will be faster, and so will its mistakes.""",
  [swap("ERU_ud_prerogative_rule", "ERU_ud_royal_secretariat")], pre="path_prerogative", ai=25, art=("command", "document"))
F("decree_register", 6, 11, "The Decree Register",
  """Every royal decree is printed in one register, numbered and dated, and posted in every district office.
  Rule by prerogative does not have to mean rule by rumour.""",
  [stab(0.02), pp(25)], pre="path_prerogative", ai=25, art=("document", "communications"))
F("provincial_intendants", 4, 12, "Provincial Intendants",
  """Royal intendants take charge of the districts, with authority over the prefects, the police and the
  public works budget. The palace finally has eyes outside the capital.""",
  [idea("ERU_ud_intendants")], pre="cabinet_of_secretaries", ai=25, art=("civil", "command"))
F("court_gazette", 6, 12, "The Court Gazette",
  """A daily gazette, printed by the chancery, carries the decrees, the honours and the palace's view of
  events. The independent papers are not closed; they simply stop receiving invitations.""",
  [pop("monarchism", 0.03), pop("democratic", -0.01)], pre="decree_register", ai=25, art=("communications", "document"))
F("officers_oath", 5, 13, "The Officers' Oath",
  """Every officer swears a personal oath to the Crown, not to the constitution the country does not have and
  not to the general staff. The ceremony is old. The intent behind reviving it is not.""",
  [idea("ERU_ud_officers_oath_idea")], pre="provincial_intendants|court_gazette", ai=25, art=("medal", "security"), event=19)
F("old_houses", 4, 14, "Patronage of the Old Houses",
  """Govern through the old landed families, who have served the Crown in the districts for centuries and
  expect to be asked. They bring stability and they bring their cousins.""",
  [idea("ERU_ud_old_houses_idea")], pre="officers_oath", excl="crown_technocrats", ai=25, art=("scales", "civil"))
F("crown_technocrats", 6, 14, "Crown Technocrats",
  """Govern through the engineers, economists and scientists of the royal academies, appointed on merit and
  answerable only to the palace. The old families will be offended. The ministries will work.""",
  [idea("ERU_ud_crown_technocrats_idea")], pre="officers_oath", excl="old_houses", ai=10, art=("science", "tools"))
F("palace_guard_reform", 4, 15, "Reform the Palace Guard",
  """The palace guard is a ceremonial regiment with a modern rifle and an antique chain of command. Put it
  under one officer, train it for real duty and keep it outside the general staff's reach.""",
  [xp("army", 10), flag("ERU_ud_guard_reformed")], pre="old_houses|crown_technocrats", ai=25, art=("security", "training"))
F("honours_of_the_realm", 6, 15, "Honours of the Realm",
  """A new order of merit for engineers, teachers, pilots and district officials. The Crown cannot pay
  everyone what they are worth. It can make sure they are seen.""",
  [stab(0.02), ws(0.02), xp("air", 10)], pre="old_houses|crown_technocrats", ai=20, art=("medal", "civil"))
F("royal_ulysses_commission", 4, 16, "The Royal Ulysses Commission",
  """Central Usea has told the world that Ulysses will strike. The Crown appoints a royal commission with
  power to requisition, build and plan, answerable to the palace alone.""",
  [idea("ERU_ud_royal_commission")], pre="palace_guard_reform|honours_of_the_realm", band="ulysses", ai=30,
  art=("meteor", "command"), event=20)
F("shelter_decree", 6, 16, "The Shelter Decree",
  """By royal decree every district builds public shelters to a single standard, paid for by the Crown
  estates and the district levy. The palace will be blamed if they are not ready. It intends to be thanked.""",
  [flag("ERU_ud_shelters_ready"), stab(0.02)], pre="palace_guard_reform|honours_of_the_realm", band="ulysses", ai=30,
  art=("shelter", "document"))
F("palace_granaries", 4, 17, "The Palace Granaries",
  """Buy grain in the good years, store it in royal granaries and release it when the sky falls. The palace
  takes custody of the national reserve, and with it the gratitude or the blame.""",
  [flag("ERU_ud_grain_ready")], pre="royal_ulysses_commission|shelter_decree", band="ulysses", ai=30, art=("economy", "shelter"))
F("royal_observatory_grants", 6, 17, "Royal Observatory Grants",
  """Erusea cannot shoot at an asteroid, but it can watch one. Royal grants fund the observatories that will
  track the fragments, and give the commission its own numbers instead of borrowed ones.""",
  [tech("electronics", 0.5)], pre="royal_ulysses_commission|shelter_decree", band="ulysses", ai=20, art=("telescope", "meteor"))
F("loyal_regiments", 4, 18, "The Loyal Regiments",
  """A coup has broken out across Usea. Before deciding who to punish, the Crown decides who to trust: a list
  of regiments whose officers held to their oath, to be garrisoned near the capital.""",
  [idea("ERU_ud_loyal_regiments_idea")], pre="palace_granaries|royal_observatory_grants", band="coup", ai=30,
  art=("security", "medal"), event=21)
F("emergency_prerogative", 6, 18, "Emergency Prerogative",
  """For one year the Crown may legislate by decree without the formality of the Privy Council. The court
  calls it a precaution. The universities call it a precedent.""",
  [timed("ERU_ud_emergency_prerogative_idea", 365)], pre="palace_granaries|royal_observatory_grants", band="coup", ai=30,
  art=("command", "document"))
F("crown_tribunals", 4, 19, "Tribunals of the Crown",
  """Those who plotted against their oath are tried by royal tribunals sitting in closed session. Justice will
  be swift. Whether it will be seen as justice is another question.""",
  [idea("ERU_ud_crown_tribunals_idea")], pre="loyal_regiments|emergency_prerogative", excl="royal_clemency", band="coup", ai=30,
  art=("scales", "security"))
F("royal_clemency", 6, 19, "Royal Clemency",
  """The Crown pardons officers who surrender their commissions and confess, and keeps the trials for the
  ringleaders. Mercy from strength is still strength.""",
  [stab(0.04), pop("monarchism", 0.03)], pre="loyal_regiments|emergency_prerogative", excl="crown_tribunals", band="coup",
  ai=10, art=("peace", "scales"))
F("crowns_protest", 4, 20, "The Crown's Protest",
  """Stonehenge is complete, eight railguns built under Central Usea's leadership on neutral soil. The palace
  protests that the continent's defence was decided without Erusea. Provisional gameplay: no official source
  records an Erusean protest.""",
  [flag("ERU_ud_stonehenge_protested"), ws(0.03)], pre="crown_tribunals|royal_clemency", excl="crowns_acceptance",
  band="stonehenge", ai=30, art=("diplomacy", "missile"), event=22)
F("crowns_acceptance", 6, 20, "The Crown's Acceptance",
  """The palace welcomes Stonehenge as the continent's shield and asks only to be kept informed. It is the
  prudent answer, and the general staff will say the weak one. Provisional gameplay.""",
  [flag("ERU_ud_stonehenge_accepted"), stab(0.03)], pre="crown_tribunals|royal_clemency", excl="crowns_protest",
  band="stonehenge", ai=0, art=("peace", "missile"), event=37)
F("royal_engineering_corps", 4, 21, "The Royal Engineering Corps",
  """Engineers from the army, the railways and the public works ministry are gathered into one royal corps,
  ready to dig, shore and rebuild wherever the fragments fall.""",
  [tech("construction_tech", 0.5), xp("army", 10)], pre="crowns_protest|crowns_acceptance", band="stonehenge", ai=25,
  art=("tools", "rebuild"))
F("envoys_to_the_treaty_capitals", 6, 21, "Envoys to the Treaty Capitals",
  """Royal envoys tour the capitals that built Stonehenge with one message: Erusea expects a seat when the
  continent's shield is discussed. They come home with polite letters.""",
  [pp(30), flag("ERU_ud_envoys_sent")], pre="crowns_protest|crowns_acceptance", band="stonehenge", ai=20,
  art=("diplomacy", "document"))
F("open_the_granaries", 4, 22, "Open the Palace Granaries",
  """Ulysses has broken apart. The royal granaries open to the districts, and the palace's name is printed on
  every sack. Requires the reserve to have been bought in time.""",
  [stab(0.05), flag("ERU_ud_relief_ready")], pre="royal_engineering_corps|envoys_to_the_treaty_capitals",
  band="impact", gate="has_country_flag = ERU_ud_grain_ready", ai=30, art=("economy", "refugees"))
F("crown_among_the_displaced", 6, 22, "The Crown Among the Displaced",
  """The monarch visits the camps where displaced families from across the continent are arriving, and the
  court learns that a photograph can be worth a regiment.""",
  [stab(0.03), ws(0.02)], pre="royal_engineering_corps|envoys_to_the_treaty_capitals", band="impact", ai=25,
  art=("refugees", "medal"))
F("royal_relief_fund", 4, 23, "The Royal Relief Fund",
  """The Crown estates' leases, the palace's own accounts and a public subscription fill one fund for the
  displaced, administered by the intendants.""",
  [fiscal("ac_econ_set_basic_services"), stab(0.02)], pre="open_the_granaries|crown_among_the_displaced", band="impact",
  ai=25, art=("economy", "civil"))
F("palace_hospital_wards", 6, 23, "The Palace Hospital Wards",
  """Two palace wings are turned over to the army medical service. The court complains about the noise. The
  wounded and the sick do not.""",
  [manpower(2000), stab(0.02)], pre="open_the_granaries|crown_among_the_displaced", band="impact", ai=20,
  art=("medical", "shelter"))
F("unbroken_crown", 5, 24, "The Unbroken Crown",
  """The decade that began with a question ends with an answer. The Crown governs, the regiments are loyal and
  the granaries were full when the sky fell. Whatever comes next, Erusea will face it as a kingdom.""",
  [swap("ERU_ud_royal_secretariat", "ERU_ud_unbroken_crown_idea"), flag("ERU_ud_crown_settled")],
  pre="royal_relief_fund|palace_hospital_wards", band="impact", cost=10, ai=30, art=("medal", "command"), event=23)

# ---------------------------------------------------------------- Constitutional reform (player only), x 8/10
lane("constitution")
F("drafting_commission", 8, 11, "Convene a Drafting Commission",
  """Jurists, district notables and two palace secretaries meet to draft a constitution. Nobody agrees on
  anything except that the first draft must be finished before the court changes its mind.""",
  [flag("ERU_ud_draft_begun")], pre="path_constitution", ai=0, art=("document", "assembly"), event=24)
F("publish_the_minutes", 10, 11, "Publish the Council Minutes",
  """The Privy Council's new minutes are published in full. The country reads, for the first time, how it is
  governed, and discovers that the answer is often 'by accident'.""",
  [pop("democratic", 0.04), stab(-0.02)], pre="path_constitution", ai=0, art=("communications", "document"))
F("legalize_the_parties", 8, 12, "Legalize the Parties",
  """The liberal clubs, the labour societies and even the monarchist leagues may organize openly, register
  members and stand candidates. Erusea discovers it has more opinions than it had newspapers.""",
  [swap("ERU_ud_drafting_commission_idea", "ERU_ud_party_politics"), pop("democratic", 0.08)], pre="drafting_commission", ai=0,
  art=("ballot", "civil"))
F("free_press_law", 10, 12, "A Free Press Law",
  """No licence to print, no prior censorship, and a court rather than a ministry to judge libel. The court
  gazette loses its subsidy and gains competitors.""",
  [pop("democratic", 0.04), ws(-0.02)], pre="publish_the_minutes", ai=0, art=("communications", "scales"))
F("charter_granted", 8, 13, "A Charter Granted by the Crown",
  """The constitution is granted by the monarch, who keeps reserve powers over war, peace and the dissolution
  of the assembly. Continuity reassures the court and disappoints the clubs.""",
  [stab(0.05), flag("ERU_ud_charter_by_crown")], pre=("legalize_the_parties", "free_press_law"), excl="charter_written", ai=0,
  art=("document", "medal"))
F("charter_written", 10, 13, "A Charter Written by Delegates",
  """The constitution is written and ratified by elected delegates, and the monarchy accepts it. The Crown
  becomes a guardian of the charter rather than its author.""",
  [pop("democratic", 0.06), stab(-0.03), flag("ERU_ud_charter_by_delegates")], pre=("legalize_the_parties", "free_press_law"),
  excl="charter_granted", ai=0, art=("ballot", "assembly"))
F("first_assembly_elections", 9, 14, "The First Assembly Elections",
  """Erusea votes. Whatever the result, a cabinet responsible to the assembly takes office, and the palace
  becomes a constitutional monarchy. Provisional gameplay: this government change is an alternate path with no
  official source, and the cabinet is represented by an unnamed office.""",
  ["ac_ud_eru_regime_constitution = yes", swap("ERU_ud_party_politics", "ERU_ud_constitutional_cabinet")],
  pre="charter_granted|charter_written", cost=10, ai=0, art=("ballot", "assembly"), event=25)
F("budget_before_the_assembly", 8, 15, "The Budget Before the Assembly",
  """For the first time the national budget is debated line by line in public. The army's estimates shrink;
  the schools' grow; everyone discovers what a district road actually costs.""",
  [fiscal("ac_econ_set_standard_tax"), pp(30)], pre="first_assembly_elections", ai=0, art=("economy", "assembly"))
F("civilian_defence_minister", 10, 15, "A Civilian Defence Minister",
  """The defence ministry is given to a civilian who answers to the assembly. The general staff keeps its
  maps. It loses its veto.""",
  [idea("ERU_ud_civilian_control")], pre="first_assembly_elections", ai=0, art=("command", "scales"))
F("assembly_ulysses_committee", 8, 16, "The Assembly's Ulysses Committee",
  """Central Usea has announced that Ulysses will strike. The assembly forms a standing committee with
  members from every party to plan for the fragments, in public, with published numbers.""",
  [idea("ERU_ud_assembly_committee")], pre="budget_before_the_assembly|civilian_defence_minister", band="ulysses", ai=0,
  art=("meteor", "assembly"), event=26)
F("public_shelter_bill", 10, 16, "The Public Shelter Bill",
  """A shelter in every district, built to a public standard, paid for by a levy the assembly voted for.
  Nobody likes the levy. Everybody wants the shelter near their own street.""",
  [flag("ERU_ud_shelters_ready"), pp(-20)], pre="budget_before_the_assembly|civilian_defence_minister", band="ulysses", ai=0,
  art=("shelter", "ballot"))
F("invite_the_observatories", 8, 17, "Invite the Observatories",
  """The committee invites astronomers from the neighbouring republics to share tracking data with Erusean
  observatories. Science, for once, is the easiest diplomacy available.""",
  [tech("electronics", 0.75)], pre="assembly_ulysses_committee|public_shelter_bill", band="ulysses", ai=0,
  art=("telescope", "diplomacy"))
F("provincial_relief_boards", 10, 17, "Provincial Relief Boards",
  """Elected boards in every province plan evacuation routes, grain stores and field hospitals, and answer to
  their own voters if the plans fail.""",
  [flag("ERU_ud_grain_ready"), stab(0.02)], pre="assembly_ulysses_committee|public_shelter_bill", band="ulysses", ai=0,
  art=("civil", "shelter"))
F("defend_the_assembly", 8, 18, "Defend the Assembly",
  """A coup has broken out across Usea, and some Erusean officers have read the news with interest. The
  assembly calls the loyal garrisons, the police and the public into the streets around the chamber.""",
  [timed("ERU_ud_defended_assembly", 365)], pre="invite_the_observatories|provincial_relief_boards", band="coup", ai=0,
  art=("assembly", "security"), event=27)
F("garrison_oversight_act", 10, 18, "The Garrison Oversight Act",
  """An assembly committee may inspect any garrison, read any order and question any officer. The general
  staff calls it an insult. The act passes anyway.""",
  [pop("fascism", -0.03), xp("army", -5)], pre="invite_the_observatories|provincial_relief_boards", band="coup", ai=0,
  art=("document", "security"))
F("purge_the_conspirators", 8, 19, "Purge the Conspirators",
  """Officers who corresponded with the plotters across Usea are dismissed, tried in open court and barred from
  public office. The army is smaller and quieter.""",
  [stab(0.03), xp("army", -10), pop("fascism", -0.04)], pre="defend_the_assembly|garrison_oversight_act",
  excl="pardon_and_reconcile", band="coup", ai=0, art=("scales", "security"))
F("pardon_and_reconcile", 10, 19, "Pardon and Reconcile",
  """The assembly pardons every officer who swears to the charter, and asks only for the names of the
  ringleaders. Some deputies call it weakness. The army calls it a debt.""",
  [stab(0.02), ws(0.02)], pre="defend_the_assembly|garrison_oversight_act", excl="purge_the_conspirators", band="coup",
  ai=0, art=("peace", "ballot"))
F("stonehenge_debate", 8, 20, "The Stonehenge Debate",
  """Stonehenge is complete. The assembly debates for three days whether Erusea should welcome the battery,
  protest it or ask to join its oversight, and votes to welcome it with conditions. Provisional gameplay.""",
  [flag("ERU_ud_stonehenge_accepted"), stab(0.02)], pre="purge_the_conspirators|pardon_and_reconcile", band="stonehenge",
  ai=0, art=("assembly", "missile"), event=28)
F("seat_at_the_continental_table", 10, 20, "A Seat at the Continental Table",
  """Erusean delegates ask to join the continental committees that coordinate the fragment response. Being
  in the room costs pride. Being outside it costs more.""",
  [pp(25), flag("ERU_ud_continental_seat")], pre="purge_the_conspirators|pardon_and_reconcile", band="stonehenge", ai=0,
  art=("diplomacy", "assembly"))
F("courts_stand_apart", 8, 21, "The Courts Stand Apart",
  """Judges are appointed for life by an independent council and cannot be moved by ministers or the palace.
  The charter acquires teeth.""",
  [stab(0.03)], pre="stonehenge_debate|seat_at_the_continental_table", band="stonehenge", ai=0, art=("scales", "gate"))
F("district_ombudsman", 10, 21, "An Ombudsman for the Districts",
  """Any citizen may complain to an independent ombudsman about any office. The first year brings eleven
  thousand letters, most of them about roads.""",
  [stab(0.02), pop("democratic", 0.02)], pre="stonehenge_debate|seat_at_the_continental_table", band="stonehenge", ai=0,
  art=("document", "civil"))
F("relief_act", 8, 22, "The Relief Act",
  """Ulysses has broken apart. The Relief Act funds housing, food and medical care for the displaced, through
  the provincial boards the assembly built three years ago.""",
  [fiscal("ac_econ_set_reconstruction"), flag("ERU_ud_relief_ready")], pre="courts_stand_apart|district_ombudsman",
  band="impact", ai=0, art=("refugees", "ballot"))
F("open_the_reception_camps", 10, 22, "Open the Reception Camps",
  """Refugees from across the continent are reaching the border. The assembly votes to receive them in
  registered camps, with work permits after a year. Provisional gameplay: the official chronology records
  that Erusea stopped taking in refugees on 21 April 2000.""",
  [flag("ERU_ud_refugees_received"), stab(-0.02)], pre="courts_stand_apart|district_ombudsman", band="impact", ai=0,
  art=("refugees", "gate"))
F("budget_for_the_displaced", 8, 23, "A Budget for the Displaced",
  """The supplementary budget for the camps passes by four votes after an all-night session. The treasury
  warns that the next one will not.""",
  [pp(-25), stab(0.03)], pre="relief_act|open_the_reception_camps", band="impact", ai=0, art=("economy", "refugees"))
F("citizens_relief_committees", 10, 23, "Citizens' Relief Committees",
  """Parish halls, unions and veterans' leagues organize their own relief committees, registered with the
  provincial boards. The state cannot do everything. It can make sure nobody does it twice.""",
  [manpower(1500), stab(0.02)], pre="relief_act|open_the_reception_camps", band="impact", ai=0, art=("civil", "medical"))
F("constitutional_settlement", 9, 24, "The Constitutional Settlement",
  """The decade ends with a charter, an assembly, an independent bench and a monarchy above the fray. It is
  untested by war. It has already been tested by the sky.""",
  [swap("ERU_ud_constitutional_cabinet", "ERU_ud_constitutional_settlement_idea"), flag("ERU_ud_constitution_settled")],
  pre="budget_for_the_displaced|citizens_relief_committees", band="impact", cost=10, ai=0, art=("assembly", "peace"), event=29)

# ---------------------------------------------------------------- General Staff regency (player only), x 12/14
lane("regency")
F("staff_memorandum", 12, 11, "The Staff Memorandum",
  """The general staff circulates its memorandum to every garrison: the ministries are failing, the Crown is
  badly advised, and only a command administration can carry Erusea through what is coming.""",
  [ws(0.03), pop("fascism", 0.04)], pre="path_regency", ai=0, art=("document", "command"))
F("secure_the_ministries", 14, 11, "Secure the Ministries",
  """Staff officers take up 'liaison posts' in every ministry, with copies of every file and keys to every
  room. No shots are fired. None are needed.""",
  [stab(-0.03), xp("army", 5)], pre="path_regency", ai=0, art=("security", "gate"))
F("regency_ordinance", 13, 12, "The Regency Ordinance",
  """The monarch signs the ordinance. A regency council of serving officers governs in the Crown's name, with
  the ministries reorganized as a command administration. Provisional gameplay: an alternate-history government
  change, represented by an unnamed office.""",
  ["ac_ud_eru_regime_regency = yes", idea("ERU_ud_regency_council")], pre=("staff_memorandum", "secure_the_ministries"),
  cost=10, ai=0, art=("command", "medal"), event=30)
F("command_administration", 12, 13, "Command Administration",
  """Ministries become directorates, ministers become directors and every file acquires a classification
  stamp. Decisions are fast and orders are clear. Nobody is allowed to ask why.""",
  [idea("ERU_ud_command_administration_idea")], pre="regency_ordinance", ai=0, art=("command", "document"))
F("military_governors", 14, 13, "Military Governors",
  """Each district is placed under a colonel with civil authority and a garrison. The prefects stay on as
  their deputies, and most of them are relieved to.""",
  [stab(0.03), pop("democratic", -0.03)], pre="regency_ordinance", ai=0, art=("security", "civil"))
F("mobilization_economy", 12, 14, "A Mobilization Economy",
  """The directorates run industry on a mobilization schedule: arms first, rail second, households last. The
  factories hum. The shops thin out.""",
  [idea("ERU_ud_mobilization_economy_idea")], pre="command_administration|military_governors", excl="garrison_austerity", ai=0,
  art=("industry", "command"))
F("garrison_austerity", 14, 14, "Garrison Austerity",
  """The regency cuts its own coat: smaller garrisons, fewer parades, savings returned to the districts. An
  army government that does not spend like one confuses everybody.""",
  [idea("ERU_ud_garrison_austerity_idea")], pre="command_administration|military_governors", excl="mobilization_economy", ai=0,
  art=("economy", "security"))
F("requisition_boards", 12, 15, "Requisition Boards",
  """Boards of officers may requisition trucks, warehouses and fuel for national purposes, with receipts that
  are redeemable 'after the emergency'. Everybody keeps their receipts.""",
  [xp("army", 10), stab(-0.02)], pre="mobilization_economy|garrison_austerity", ai=0, art=("logistics", "document"), event=31)
F("staff_college_ministries", 14, 15, "Staff College Ministries",
  """The staff college trains its graduates to run ministries as they would run a corps: plans, reports,
  inspections. The civil service is invited to attend.""",
  [tech("land_doctrine", 0.5)], pre="mobilization_economy|garrison_austerity", ai=0, art=("training", "command"))
F("civil_defence_command", 12, 16, "Civil Defence Command",
  """Central Usea has announced that Ulysses will strike. The regency answers the way it knows how: a single
  Civil Defence Command, with a general at its head and the districts under its orders.""",
  [idea("ERU_ud_civil_defence_command_idea")], pre="requisition_boards|staff_college_ministries", band="ulysses", ai=0,
  art=("meteor", "security"), event=32)
F("evacuation_drills", 14, 16, "Evacuation Drills",
  """Every town practises its evacuation twice a year, by siren and by timetable, with soldiers at the
  crossroads. The drills are resented. They are also fast.""",
  [flag("ERU_ud_shelters_ready"), stab(-0.01)], pre="requisition_boards|staff_college_ministries", band="ulysses", ai=0,
  art=("logistics", "shelter"))
F("army_shelter_engineers", 12, 17, "Army Shelter Engineers",
  """Engineer battalions dig and pour public shelters on a military schedule. The concrete is thick, the
  ventilation is poor and the deadlines are met.""",
  [tech("construction_tech", 0.5), flag("ERU_ud_grain_ready")], pre="civil_defence_command|evacuation_drills", band="ulysses",
  ai=0, art=("shelter", "tools"))
F("broadcast_censorship", 14, 17, "Censor the Broadcasts",
  """Every broadcast about Ulysses is read by a staff officer first, to prevent panic. It prevents a great
  deal else as well.""",
  [stab(0.02), pop("democratic", -0.02)], pre="civil_defence_command|evacuation_drills", band="ulysses", ai=0,
  art=("communications", "security"))
F("martial_law_ordinances", 12, 18, "Martial Law Ordinances",
  """A coup has broken out across Usea, and the regency is the one government on the continent that cannot be
  overthrown by its own army. It does not intend to be overthrown by anyone else's.""",
  [timed("ERU_ud_martial_law", 365)], pre="army_shelter_engineers|broadcast_censorship", band="coup", ai=0,
  art=("security", "document"), event=33)
F("root_out_the_conspiracies", 14, 18, "Root Out the Conspiracies",
  """Military intelligence turns on the officers' clubs. Anyone who corresponded with plotters abroad is
  transferred, retired or arrested.""",
  [stab(0.02), xp("army", -5)], pre="army_shelter_engineers|broadcast_censorship", band="coup", ai=0,
  art=("security", "radar"))
F("regency_without_end", 12, 19, "A Regency Without End",
  """The council announces that the emergency will last as long as the emergency does. The Crown is not
  consulted.""",
  [pop("fascism", 0.05), flag("ERU_ud_regency_perpetual")], pre="martial_law_ordinances|root_out_the_conspiracies",
  excl="promise_of_restoration", band="coup", ai=0, art=("command", "gate"))
F("promise_of_restoration", 14, 19, "The Promise of Restoration",
  """The council publishes a date: once the fragments have fallen and the camps are emptied, the seals of
  office will return to the Crown. Some officers believe it.""",
  [stab(0.03), flag("ERU_ud_regency_promised")], pre="martial_law_ordinances|root_out_the_conspiracies",
  excl="regency_without_end", band="coup", ai=0, art=("medal", "peace"))
F("railgun_assessment", 12, 20, "Assess the Railgun Battery",
  """Stonehenge is complete. The general staff studies what the published specifications say about eight
  railguns on neutral soil, and what they do not. Provisional gameplay: an internal staff study, not a record
  of Erusean planning.""",
  [tech("artillery", 0.5), flag("ERU_ud_stonehenge_protested")], pre="regency_without_end|promise_of_restoration",
  band="stonehenge", ai=0, art=("missile", "radar"), event=34)
F("air_defence_review", 14, 20, "The Air Defence Review",
  """If fragments can be shot down, so can aircraft. The regency reviews every radar and gun site in Erusea
  and finds most of them wanting.""",
  [tech("radar_tech", 0.5)], pre="regency_without_end|promise_of_restoration", band="stonehenge", ai=0, art=("radar", "air"))
F("continental_contingency_studies", 12, 21, "Continental Contingency Studies",
  """The staff war-games every continental emergency it can imagine: fragments, famine, refugees and the
  collapse of a neighbour. The studies are filed. The habit of filing them is not.""",
  [xp("army", 10), tech("land_doctrine", 0.5)], pre="railgun_assessment|air_defence_review", band="stonehenge", ai=0,
  art=("command", "training"))
F("observatory_liaison", 14, 21, "Staff Liaison to the Observatories",
  """A staff officer sits in every observatory with a direct line to Civil Defence Command. The astronomers
  learn to report in grid squares.""",
  [tech("electronics", 0.5)], pre="railgun_assessment|air_defence_review", band="stonehenge", ai=0, art=("telescope", "command"))
F("army_relief_columns", 12, 22, "Army Relief Columns",
  """Ulysses has broken apart. Columns of army trucks carry food, water and tents to the displaced, under
  officers who have been planning this for three years.""",
  [stab(0.04), flag("ERU_ud_relief_ready")], pre="continental_contingency_studies|observatory_liaison", band="impact", ai=0,
  art=("logistics", "refugees"))
F("requisitioned_trains", 14, 22, "Requisitioned Trains",
  """Every passenger train in Erusea is requisitioned for a month to move relief and the displaced. Commuters
  walk, and are told why.""",
  [stab(0.02), xp("army", 5)], pre="continental_contingency_studies|observatory_liaison", band="impact", ai=0,
  art=("rail", "refugees"))
F("command_relief_directorate", 12, 23, "The Relief Directorate",
  """Relief becomes a directorate with a general, a staff and a war diary. It is efficient, it is unloved
  and it works.""",
  [timed("ERU_ud_relief_directorate", 180)], pre="army_relief_columns|requisitioned_trains", band="impact", ai=0,
  art=("command", "medical"))
F("field_kitchens_order", 14, 23, "The Field Kitchens Order",
  """Every garrison kitchen feeds the district around it, twice a day, without asking who is a citizen. It
  is the regency's most popular order.""",
  [stab(0.03)], pre="army_relief_columns|requisitioned_trains", band="impact", ai=0, art=("civil", "refugees"))
F("regencys_mandate", 12, 24, "The Regency's Mandate",
  """The council declares that it has earned its mandate by carrying Erusea through the decade. It will carry
  the country into the next one too.""",
  [swap("ERU_ud_regency_council", "ERU_ud_regency_mandate"), flag("ERU_ud_regency_settled")],
  pre=("command_relief_directorate|field_kitchens_order", "regency_without_end"), excl="return_the_seals", band="impact",
  cost=10, ai=0, art=("command", "medal"), event=35)
F("return_the_seals", 14, 24, "Return the Seals",
  """The council keeps its promise. The seals of office return to the Crown, which governs through a restored
  Crown Council with the officers back in their barracks. Provisional gameplay: an alternate-history government
  change, represented by an unnamed office.""",
  ["ac_ud_eru_regime_restoration = yes", swap("ERU_ud_regency_council", "ERU_ud_restored_council"),
   flag("ERU_ud_regency_settled")],
  pre=("command_relief_directorate|field_kitchens_order", "promise_of_restoration"), excl="regencys_mandate", band="impact",
  cost=10, ai=0, art=("medal", "peace"), event=36)

# ---------------------------------------------------------------- Industry and rail, x 0/2
lane("industry")
F("rail_ministry_ledger", 1, 6, "The Rail Ministry Ledger",
  """The freight reserves are counted and the industrial standards are printed. Now the rail ministry opens its
  ledger: every line, every bridge, every locomotive and what it would cost to make the network carry a modern
  economy. The answer will decide who owns the railways.""",
  [tech("train_tech", 0.5)], pre="ERU_exp_industrial_standards", ai=30, art=("rail", "document"), event=7)
F("state_railways_trust", 0, 7, "The State Railways Trust",
  """One public trust owns every line, sets every tariff and answers to the government. It will be slow to
  modernize and impossible to bankrupt, and the army will always have a timetable.""",
  [idea("ERU_ud_state_railways")], pre="rail_ministry_ledger", excl="concession_railways", ai=30, art=("rail", "command"))
F("concession_railways", 2, 7, "Concession Railways",
  """Lease the main lines to private operators for thirty years, with investment written into the
  concessions. The trains will be newer and the fares higher, and the state will have to negotiate for its
  own timetable.""",
  [idea("ERU_ud_concession_railways_idea")], pre="rail_ministry_ledger", excl="state_railways_trust", ai=10, art=("rail", "economy"))
F("electrify_trunk_lines", 0, 8, "Electrify the Trunk Lines",
  """The trust strings catenary along the busiest trunk lines, starting with the capital's approaches. Diesel
  stays on the branch lines; the coal yards close.""",
  [tech("train_tech", 0.5), tech("industry", 0.25)], pre="state_railways_trust", ai=25, art=("rail", "industry"))
F("rolling_stock_licences", 2, 8, "Rolling-Stock Licences",
  """The concessionaires license foreign locomotive and wagon designs and build them in Erusean shops. The
  designs are not ours, but the jobs are.""",
  [tech("train_tech", 0.75)], pre="concession_railways", ai=20, art=("rail", "tools"))
F("military_rail_timetables", 0, 9, "Military Rail Timetables",
  """Every line has a secret second timetable, for mobilization. The trust prints it, the general staff keeps
  it and the commuters never see it.""",
  [tech("logistics_tech", 0.5), xp("army", 5)], pre="electrify_trunk_lines", ai=25, art=("rail", "security"))
F("private_freight_terminals", 2, 9, "Private Freight Terminals",
  """Shipping firms and manufacturers build their own freight terminals beside the concession lines.
  Factories follow the terminals, and towns follow the factories.""",
  [tech("industry", 0.5)], pre="rolling_stock_licences", ai=20, art=("logistics", "economy"))
F("machine_tool_bureau", 1, 10, "The Machine-Tool Bureau",
  """Erusea's factories run on imported machine tools and spare parts that arrive late. A bureau with a budget
  and an engineering school sets out to change that, one lathe at a time.""",
  [tech("industry", 0.5)], pre="military_rail_timetables|private_freight_terminals", ai=30, art=("tools", "industry"), event=8)
F("steel_quota", 0, 11, "The Steel Quota",
  """Heavy industry first: a national steel quota, guaranteed prices for the mills and priority for coal and
  power. Shoes and radios can wait.""",
  [idea("ERU_ud_steel_quota_idea")], pre="machine_tool_bureau", excl="light_industry_first", ai=30, art=("industry", "economy"))
F("light_industry_first", 2, 11, "Light Industry First",
  """Households first: credit for the textile mills, the furniture shops and the radio assemblers that employ
  half the towns. The mills can wait for demand.""",
  [idea("ERU_ud_light_industry")], pre="machine_tool_bureau", excl="steel_quota", ai=10, art=("economy", "civil"))
F("armour_plate_mills", 0, 12, "Armour-Plate Mills",
  """Two mills are converted to roll armour plate to the army's specifications. The order book is small. The
  capability is not.""",
  [tech("armor", 0.5)], pre="steel_quota", ai=25, art=("industry", "security"))
F("consumer_electronics_plants", 2, 12, "Consumer Electronics Plants",
  """Radios, televisions and telephone exchanges assembled in Erusea, for Erusea. The same lines can make
  military radios if anyone asks.""",
  [tech("electronics", 0.5)], pre="light_industry_first", ai=20, art=("communications", "industry"))
F("aero_engine_works", 0, 13, "Aero-Engine Works",
  """A state engine works builds jet engines under licence and learns, slowly, how to design its own. The air
  arm will not have to beg for spares.""",
  [tech("industry", 0.25), flag("ERU_ud_engine_works")], pre="armour_plate_mills", ai=25, art=("air", "industry"))
F("export_credit_board", 2, 13, "The Export Credit Board",
  """Erusean manufacturers sell abroad on government-guaranteed credit, and the board keeps a ledger of every
  buyer. It learns, faster than the foreign ministry, which neighbours pay their bills and which ones expect
  Erusea to forget.""",
  [pp(25), flag("ERU_ud_export_credit")], pre="consumer_electronics_plants", ai=20, art=("economy", "diplomacy"))
F("shipyard_modernization", 1, 14, "Modernize the Shipyards",
  """New cranes, covered slipways and welding halls for the national yards. Whatever fleet Erusea decides to
  build, it will be built here.""",
  [idea("ERU_ud_modern_slipways")], pre="aero_engine_works|export_credit_board", ai=30, art=("navy", "tools"))
F("strategic_fuel_reserves", 0, 15, "Strategic Fuel Reserves",
  """Tank farms at the refineries and the main depots hold a season's fuel for the army, the air arm and the
  fleet. The treasury hates paying for oil that sits still.""",
  [idea("ERU_ud_fuel_reserves")], pre="shipyard_modernization", ai=25, art=("logistics", "industry"))
F("power_grid_interconnect", 2, 15, "Interconnect the Power Grid",
  """The district power companies are linked into one national grid, so a failure in one valley no longer
  stops the factories in the next.""",
  [tech("industry", 0.5)], pre="shipyard_modernization", ai=20, art=("industry", "communications"))
F("shelter_steel_programme", 0, 16, "The Shelter Steel Programme",
  """Central Usea has announced that Ulysses will strike. The mills set aside steel for shelter doors, blast
  shutters and reinforcing bar, at a fixed price.""",
  [flag("ERU_ud_shelters_ready"), tech("construction_tech", 0.5)], pre="strategic_fuel_reserves|power_grid_interconnect",
  band="ulysses", ai=25, art=("shelter", "industry"))
F("hardened_rail_junctions", 2, 16, "Hardened Rail Junctions",
  """The great junctions get duplicate tracks, buried signal cables and spare bridges stored nearby. If one
  fragment can cut the network, the network was not ready.""",
  [tech("logistics_tech", 0.5)], pre="strategic_fuel_reserves|power_grid_interconnect", band="ulysses", ai=20,
  art=("rail", "shelter"))
F("emergency_production_plan", 0, 17, "The Emergency Production Plan",
  """Every large plant files a plan for working through the fragment years: what it makes, what it needs and
  what it can stop making.""",
  [tech("industry", 0.5)], pre="shelter_steel_programme|hardened_rail_junctions", band="ulysses", ai=25,
  art=("document", "industry"))
F("construction_steel_stockpile", 2, 17, "Stockpile Construction Steel",
  """Girders, sheet and rebar are stockpiled at the depots for rebuilding whatever the sky breaks. The
  stockpile is guarded more carefully than the gold reserve.""",
  [flag("ERU_ud_rebuild_stock")], pre="shelter_steel_programme|hardened_rail_junctions", band="ulysses", ai=20,
  art=("rebuild", "logistics"))
F("guard_the_rail_yards", 0, 18, "Guard the Rail Yards",
  """A coup has broken out across Usea. Railway police and army pickets guard the yards and the junctions:
  whoever holds the trains holds the country.""",
  [xp("army", 5), stab(0.02)], pre="emergency_production_plan|construction_steel_stockpile", excl="strike_arbitration_boards",
  band="coup", ai=25, art=("security", "rail"))
F("strike_arbitration_boards", 2, 18, "Strike Arbitration Boards",
  """In a year of plots, the unions are offered binding arbitration instead of strikes, with wages indexed to
  bread. The yards stay open by consent.""",
  [stab(0.03)], pre="emergency_production_plan|construction_steel_stockpile", excl="guard_the_rail_yards", band="coup",
  ai=10, art=("scales", "industry"))
F("plant_security_councils", 0, 19, "Plant Security Councils",
  """Managers, foremen and police meet weekly in every large plant to review who comes and goes. Sabotage
  falls. So does trust.""",
  [stab(0.01), tech("industry", 0.25)], pre="guard_the_rail_yards|strike_arbitration_boards", band="coup", ai=20,
  art=("security", "industry"))
F("restart_the_lines", 2, 19, "Restart the Lines",
  """The plants that stood idle during the coup scare are restarted on double shifts to recover the lost
  months.""",
  [tech("industry", 0.5)], pre="guard_the_rail_yards|strike_arbitration_boards", band="coup", ai=20, art=("industry", "tools"))
F("hardened_factory_roofs", 0, 20, "Hardened Factory Roofs",
  """Stonehenge is complete, and the engineers' question is the same as before: what if a fragment gets
  through? Harden the roofs, bury the transformers and stay where the workers live.""",
  [idea("ERU_ud_hardened_industry")], pre="plant_security_councils|restart_the_lines", excl="dispersal_of_industry",
  band="stonehenge", ai=25, art=("shelter", "industry"))
F("dispersal_of_industry", 2, 20, "Disperse the Industry",
  """Move a third of the key plants out of the river valleys into smaller towns, so that no single strike
  can stop a whole industry. It is expensive and slow.""",
  [idea("ERU_ud_dispersed_industry")], pre="plant_security_councils|restart_the_lines", excl="hardened_factory_roofs",
  band="stonehenge", ai=10, art=("logistics", "industry"))
F("spare_machine_tools", 0, 21, "Spare Machine-Tool Depots",
  """A second set of critical machine tools, crated and stored far from the plants that use them, ready to
  restart a ruined line within weeks.""",
  [tech("industry", 0.5)], pre="hardened_factory_roofs|dispersal_of_industry", band="stonehenge", ai=20, art=("tools", "logistics"))
F("precision_optics_works", 2, 21, "Precision Optics Works",
  """The observatories need lenses, the air arm needs gunsights and the survey office needs theodolites. One
  optics works can serve all three.""",
  [tech("electronics", 0.5)], pre="hardened_factory_roofs|dispersal_of_industry", band="stonehenge", ai=20,
  art=("telescope", "tools"))
F("relief_trains", 0, 22, "Relief Trains",
  """Ulysses has broken apart. The railways run relief trains on the military timetable, carrying food and
  tents out and the injured back.""",
  [timed("ERU_ud_relief_trains_idea", 180), flag("ERU_ud_relief_ready")], pre="spare_machine_tools|precision_optics_works",
  band="impact", ai=30, art=("rail", "refugees"), event=38)
F("rebuild_the_supply_lines", 2, 22, "Rebuild the Supply Lines",
  """Bridges, sidings and pipelines damaged in the fragment months are repaired first, before anything else
  is rebuilt.""",
  [tech("construction_tech", 0.5)], pre="spare_machine_tools|precision_optics_works", band="impact", ai=20,
  art=("bridge", "rebuild"))
F("emergency_housing_works", 0, 23, "Emergency Housing Works",
  """Factories that made shelter doors now make prefabricated housing for the displaced, from the stockpiled
  steel.""",
  [stab(0.03)], pre="relief_trains|rebuild_the_supply_lines", band="impact",
  gate="OR = { has_country_flag = ERU_ud_rebuild_stock has_country_flag = ERU_ud_shelters_ready }", ai=25,
  art=("rebuild", "refugees"))
F("prefabricated_shelters", 2, 23, "Prefabricated Shelters",
  """Tens of thousands of steel huts roll off the lines and onto flat wagons, bound for the camps.""",
  [manpower(1000), stab(0.02)], pre="relief_trains|rebuild_the_supply_lines", band="impact", ai=20, art=("shelter", "rail"))
F("industrial_census", 1, 24, "The Industrial Census",
  """At the end of the decade the statistics office counts every plant, worker and machine in Erusea. The
  census will be the starting point for whatever the next decade demands.""",
  [tech("industry", 0.75), flag("ERU_ud_industry_counted")], pre="emergency_housing_works|prefabricated_shelters",
  band="impact", cost=10, ai=30, art=("document", "industry"))

# ---------------------------------------------------------------- Army, x 16/18 (17 for single nodes)
lane("army")
F("defence_review", 19, 6, "The Defence Review",
  """The reserve exercises are over and the general staff has written its report. The army, the air arm and
  the navy each want everything. The review decides who gets what, in what order and on whose authority.""",
  [xp("army", 5), xp("air", 5), xp("navy", 5)], pre="ERU_exp_reserve_exercises", ai=30, art=("command", "document"), event=9)
F("army_board", 17, 7, "The Army Board",
  """A board of senior officers and treasury officials sets the army's shape for the decade: how many
  divisions, how many reservists and how much of either Erusea can afford.""",
  [xp("army", 10)], pre="defence_review", ai=25, art=("command", "training"))
F("mass_reserve_army", 16, 8, "A Mass Reserve Army",
  """A small regular army and a very large trained reserve, called up by district. Cheap in peacetime and
  enormous in war.""",
  [idea("ERU_ud_mass_reserve")], pre="army_board", excl="professional_mobile_corps", ai=25, art=("training", "civil"))
F("professional_mobile_corps", 18, 8, "A Professional Mobile Corps",
  """Fewer soldiers, longer service, more vehicles. A corps that can move across the continent faster than its
  neighbours can mobilize.""",
  [idea("ERU_ud_professional_corps")], pre="army_board", excl="mass_reserve_army", ai=15, art=("logistics", "training"))
F("reserve_depots", 16, 9, "District Reserve Depots",
  """Every district keeps its reservists' rifles, uniforms and trucks in a local depot, ready to issue within
  forty-eight hours.""",
  [manpower(3000), tech("infantry_weapons", 0.5)], pre="mass_reserve_army", ai=25, art=("logistics", "security"))
F("mobile_brigades", 18, 9, "Mobile Brigades",
  """The first mechanized brigades are formed from the best regular battalions, with their own transport,
  artillery and engineers.""",
  [tech("cat_mechanized_equipment", 0.5)], pre="professional_mobile_corps", ai=25, art=("logistics", "command"))
F("artillery_parks", 17, 10, "Artillery Parks",
  """The army's guns are concentrated in regional parks with trained crews, instead of scattered among
  garrisons that cannot fire them.""",
  [tech("artillery", 0.5)], pre="reserve_depots|mobile_brigades", ai=25, art=("missile", "training"))
F("coastal_regiments", 16, 11, "Coastal Regiments",
  """Erusea has a long coast and a short memory of defending it. Regiments are raised for the beaches and
  harbours, trained with the navy.""",
  [xp("army", 10), flag("ERU_ud_coast_garrisoned")], pre="artillery_parks", ai=20, art=("navy", "security"))
F("armour_school", 18, 11, "The Armour School",
  """A school for tank crews, commanders and mechanics, with its own ranges and workshops. The army's first
  real armoured doctrine will be written there.""",
  [tech("armor", 0.5)], pre="artillery_parks", ai=20, art=("training", "industry"))
F("coastal_batteries", 16, 12, "Coastal Artillery Batteries",
  """Old coastal guns are replaced with mobile missile and artillery batteries that can be moved before an
  enemy finds them.""",
  [tech("artillery", 0.5)], pre="coastal_regiments", ai=20, art=("missile", "navy"))
F("combined_arms_exercises", 18, 12, "Combined-Arms Exercises",
  """Infantry, armour, artillery and the air arm exercise together for the first time in a decade. Most of the
  lessons are about radios.""",
  [xp("army", 15)], pre="armour_school", ai=20, art=("training", "communications"))
F("army_doctrine_manual", 17, 13, "The Army's Doctrine Manual",
  """The board's conclusions are printed as a manual and issued to every officer. Whatever the army becomes,
  it will at least agree on what it is trying to be.""",
  [tech("land_doctrine", 0.75)], pre="coastal_batteries|combined_arms_exercises", ai=25, art=("document", "training"))
F("army_civil_defence_corps", 17, 16, "The Army Civil Defence Corps",
  """Central Usea has announced that Ulysses will strike. Reservists are given a second duty: digging out,
  shoring up and keeping order when fragments fall.""",
  [manpower(2000), flag("ERU_ud_army_civil_defence")], pre="army_doctrine_manual", band="ulysses", ai=25,
  art=("shelter", "training"))
F("reserve_call_up_rehearsal", 16, 17, "Rehearse the Call-Up",
  """The whole reserve is called up for one weekend, district by district, to prove the depots and the trains
  work. They mostly do.""",
  [xp("army", 10)], pre="army_civil_defence_corps", band="ulysses", ai=20, art=("rail", "training"))
F("fragment_watch_posts", 18, 17, "Fragment Watch Posts",
  """Army observers in the hills report anything that falls from the sky, with a telephone line to the
  nearest engineer battalion.""",
  [tech("radar_tech", 0.25)], pre="army_civil_defence_corps", band="ulysses", ai=20, art=("telescope", "security"))
F("garrison_loyalty_review", 16, 18, "The Garrison Loyalty Review",
  """A coup has broken out across Usea. Every garrison commander is interviewed, every officers' club is
  watched and every transfer is approved by the board.""",
  [stab(0.02), xp("army", -5)], pre="reserve_call_up_rehearsal|fragment_watch_posts", excl="officers_assurance", band="coup",
  ai=25, art=("security", "document"))
F("officers_assurance", 18, 18, "The Officers' Assurance",
  """The board publicly assures the officer corps that it is trusted, and asks only that rumours be reported.
  Morale holds. So, perhaps, do the rumours.""",
  [xp("army", 10)], pre="reserve_call_up_rehearsal|fragment_watch_posts", excl="garrison_loyalty_review", band="coup",
  ai=10, art=("medal", "command"))
F("rotate_the_garrisons", 17, 19, "Rotate the Garrisons",
  """No regiment stays in the same town for more than two years. Officers cannot build local followings, and
  the army learns the whole country.""",
  [tech("logistics_tech", 0.25), stab(0.01)], pre="garrison_loyalty_review|officers_assurance", band="coup", ai=20,
  art=("logistics", "security"))
F("frontier_survey", 16, 20, "The Frontier Survey",
  """Stonehenge is complete and the continent's map has changed without a border moving. Army surveyors
  redraw the frontier defence plans with the battery's range in mind. Provisional gameplay.""",
  [xp("army", 10), flag("ERU_ud_frontier_surveyed")], pre="rotate_the_garrisons", band="stonehenge", ai=20,
  art=("document", "missile"))
F("air_defence_artillery", 18, 20, "Air-Defence Artillery Regiments",
  """Fragments are not the only things that fall from the sky. The army raises its first modern air-defence
  regiments.""",
  [tech("artillery", 0.5)], pre="rotate_the_garrisons", band="stonehenge", ai=20, art=("missile", "radar"))
F("engineers_for_the_camps", 16, 22, "Engineers for the Camps",
  """Ulysses has broken apart. Engineer battalions lay out camps for the displaced: water, drains, roads and
  tents in straight lines.""",
  [stab(0.03), flag("ERU_ud_relief_ready")], pre="frontier_survey|air_defence_artillery", band="impact", ai=25,
  art=("refugees", "tools"))
F("army_water_columns", 18, 22, "Army Water Columns",
  """Water purification trucks and tanker columns supply the districts where pipes and wells were damaged in
  the fragment months.""",
  [stab(0.02)], pre="frontier_survey|air_defence_artillery", band="impact", ai=20, art=("logistics", "medical"))
F("readiness_review", 17, 24, "The Army Readiness Review",
  """At the end of the decade the army counts what it has: divisions, reservists, depots and lessons. The
  review is honest, which is more than most armies manage.""",
  [xp("army", 20), flag("ERU_ud_army_reviewed")], pre="engineers_for_the_camps|army_water_columns", band="impact", cost=10,
  ai=25, art=("command", "medal"))

# ---------------------------------------------------------------- Air arm, x 20/22 (21 for single nodes)
lane("air")
F("air_arm_charter", 21, 7, "The Air Arm Charter",
  """The air arm receives a charter of its own, separate from the army, with its own staff, budget and
  schools. Its officers have been asking for twenty years.""",
  [xp("air", 15)], pre="defence_review", ai=25, art=("air", "document"), event=11)
F("pilot_academy", 20, 8, "The Pilot Academy",
  """One academy for every pilot Erusea trains, with modern simulators and instructors rotated in from the
  operational squadrons.""",
  [idea("ERU_ud_pilot_academy_idea")], pre="air_arm_charter", ai=25, art=("air", "training"))
F("licensed_airframes", 22, 8, "Licensed Airframes",
  """The air arm buys foreign fighter designs with the right to build them in Erusea. The aero-engine works
  will matter.""",
  [tech("light_fighter", 0.5)], pre="air_arm_charter", ai=20, art=("air", "tools"))
F("interceptor_doctrine", 20, 9, "Interceptor Doctrine",
  """The air arm's purpose is to own Erusean skies: fast interceptors, ground radar and pilots trained to
  fight outnumbered.""",
  [idea("ERU_ud_interceptor_doctrine_idea")], pre="pilot_academy", excl="strike_doctrine", ai=25, art=("air", "radar"))
F("strike_doctrine", 22, 9, "Strike Doctrine",
  """The air arm's purpose is to support the army: strike aircraft, forward air controllers and runways close
  to the front.""",
  [idea("ERU_ud_strike_doctrine_idea")], pre="pilot_academy", excl="interceptor_doctrine", ai=15, art=("air", "missile"))
F("radar_belt", 20, 10, "The Radar Belt",
  """A chain of radar stations along the coast and the borders, linked to the interceptor bases by buried
  cable.""",
  [tech("radar_tech", 0.75)], pre="interceptor_doctrine", ai=25, art=("radar", "communications"))
F("strike_wings", 22, 10, "Strike Wings",
  """The strike squadrons are grouped into wings with their own maintenance and munitions, ready to deploy as
  a unit.""",
  [tech("cas_bomber", 0.5)], pre="strike_doctrine", ai=20, art=("air", "logistics"))
F("reserve_squadrons", 21, 11, "Reserve Squadrons",
  """Pilots who leave the air arm keep flying on weekends with reserve squadrons, so that a war would not
  start with empty cockpits.""",
  [xp("air", 10)], pre="radar_belt|strike_wings", ai=20, art=("air", "civil"))
F("dispersal_airstrips", 20, 12, "Dispersal Airstrips",
  """Stretches of highway and farm strips are surveyed and prepared so that squadrons can scatter if their
  bases are hit.""",
  [tech("construction_tech", 0.25), flag("ERU_ud_airstrips_dispersed")], pre="reserve_squadrons", ai=20,
  art=("runway", "logistics"))
F("night_flying_course", 22, 12, "The Night Flying Course",
  """Every operational pilot completes a night and bad-weather course. The accident rate rises before it
  falls.""",
  [xp("air", 10)], pre="reserve_squadrons", ai=20, art=("air", "training"))
F("air_staff_college", 21, 13, "The Air Staff College",
  """The air arm opens its own staff college, so that its commanders learn to plan campaigns and not only to
  fly them.""",
  [tech("air_doctrine", 0.5)], pre="dispersal_airstrips|night_flying_course", ai=25, art=("training", "command"))
F("fragment_tracking_radar", 21, 16, "Fragment-Tracking Radar",
  """Central Usea has announced that Ulysses will strike. The radar belt's operators retrain to track
  objects falling from orbit, not only aircraft crossing the border.""",
  [tech("radar_tech", 0.5)], pre="air_staff_college", band="ulysses", ai=25, art=("radar", "meteor"))
F("high_altitude_reconnaissance", 20, 17, "High-Altitude Reconnaissance",
  """Reconnaissance aircraft are refitted with long-focus cameras to photograph debris fields and damaged
  districts from high altitude. The same photographs will tell the relief planners where the roads still run.""",
  [xp("air", 10)], pre="fragment_tracking_radar", band="ulysses", ai=20, art=("air", "telescope"))
F("air_rescue_squadrons", 22, 17, "Air Rescue Squadrons",
  """Helicopter squadrons train for rescue in collapsed towns, flooded valleys and burning forests. Their crews
  learn to land where there is no landing ground, and to choose who goes first.""",
  [manpower(500), stab(0.01)], pre="fragment_tracking_radar", band="ulysses", ai=20, art=("air", "medical"))
F("airfield_security", 21, 18, "Airfield Security Regiments",
  """A coup has broken out across Usea, and in several countries it began at an airfield. Every Erusean base
  gets its own security regiment.""",
  [stab(0.02)], pre="high_altitude_reconnaissance|air_rescue_squadrons", band="coup", ai=25, art=("security", "runway"))
F("airspace_near_the_battery", 20, 20, "Airspace Near the Battery",
  """Stonehenge is complete. The air arm rewrites its flight rules for the airspace near the battery and
  studies what eight railguns mean for anything that flies. Provisional gameplay.""",
  [xp("air", 10), flag("ERU_ud_battery_airspace")], pre="airfield_security", band="stonehenge", ai=20,
  art=("missile", "air"))
F("coastal_interceptor_patrols", 22, 20, "Coastal Interceptor Patrols",
  """Standing interceptor patrols along the coast, ready for whatever comes in from the sea or falls from the
  sky.""",
  [tech("light_fighter", 0.25)], pre="airfield_security", band="stonehenge", ai=20, art=("air", "navy"))
F("relief_air_bridge", 20, 22, "The Relief Air Bridge",
  """Ulysses has broken apart. Transport squadrons fly food and medicine into districts the roads cannot
  reach.""",
  [stab(0.03), flag("ERU_ud_relief_ready")], pre="airspace_near_the_battery|coastal_interceptor_patrols", band="impact",
  ai=25, art=("air", "refugees"))
F("medical_evacuation_flights", 22, 22, "Medical Evacuation Flights",
  """The injured are flown out of the damaged districts to hospitals that still have power, beds and surgeons.
  The flights run until the last patient on every list is moved.""",
  [manpower(500), stab(0.02)], pre="airspace_near_the_battery|coastal_interceptor_patrols", band="impact", ai=20,
  art=("medical", "air"))
F("air_arm_at_decades_end", 21, 24, "The Air Arm at Decade's End",
  """The air arm ends the decade with its own charter, academy and staff college, and pilots who have flown
  through the worst sky in history.""",
  [xp("air", 20), flag("ERU_ud_air_reviewed")], pre="relief_air_bridge|medical_evacuation_flights", band="impact", cost=10,
  ai=25, art=("air", "medal"))

# ---------------------------------------------------------------- Aegir fleet, lower section x 3-7
# Rooted by an availability condition, not a prerequisite line, to keep lines clear of other lanes.
lane("fleet")
F("aegir_fleet_plan", 5, 26, "The Aegir Fleet Plan",
  """The navy's plan for a modern fleet, to be known as the Aegir fleet, built over the decade in Erusean
  yards. Provisional gameplay: the official chronology names the Aegir fleet only at its loss in November
  2004; its 1990s build-up and timing here are a gameplay abstraction.""",
  [xp("navy", 15), flag("ERU_ud_aegir_planned")], gate=done("defence_review"), cost=10, ai=30, art=("navy", "document"),
  event=10)
F("fleet_officers_school", 3, 27, "The Fleet Officers' School",
  """A fleet needs officers before it needs hulls. The naval school doubles its intake and adds a staff
  course for squadron commanders.""",
  [xp("navy", 10)], pre="aegir_fleet_plan", ai=25, art=("navy", "training"))
F("dockyard_slipways", 7, 27, "Dockyard Slipways",
  """New covered slipways at the national yards, sized for the largest hulls the plan calls for.""",
  [tech("naval_equipment", 0.5)], pre="aegir_fleet_plan", ai=25, art=("navy", "industry"))
F("battle_line_doctrine", 4, 28, "The Battle Line",
  """The Aegir fleet will be built around a battle line of large surface combatants, able to fight any
  squadron in Usean waters.""",
  [idea("ERU_ud_battle_line")], pre=("fleet_officers_school", "dockyard_slipways"), excl="escort_screen_doctrine", ai=25,
  art=("navy", "command"))
F("escort_screen_doctrine", 6, 28, "Escort and Submarine Screen",
  """The Aegir fleet will be built around escorts and submarines that protect the coast and the convoys, not
  around a battle line.""",
  [idea("ERU_ud_escort_screen")], pre=("fleet_officers_school", "dockyard_slipways"), excl="battle_line_doctrine", ai=10,
  art=("submarine", "navy"))
F("capital_ship_crews", 4, 29, "Capital-Ship Crews",
  """Large ships need large, trained crews. The fleet's first big hulls are manned by sailors drafted from
  the whole navy.""",
  [xp("navy", 15)], pre="battle_line_doctrine", ai=25, art=("navy", "medal"))
F("submarine_pickets", 6, 29, "Submarine Pickets",
  """A flotilla of submarines patrols the approaches to the Erusean coast, trained to report before they
  fight.""",
  [tech("naval_equipment", 0.5)], pre="escort_screen_doctrine", ai=20, art=("submarine", "radar"))
F("home_anchorage_defences", 5, 30, "Home Anchorage Defences",
  """Nets, mines, guns and radar around the fleet's home anchorage. A fleet in harbour should be the safest
  fleet in the world.""",
  [tech("naval_equipment", 0.5), flag("ERU_ud_anchorage_defended")], pre="capital_ship_crews|submarine_pickets", ai=25,
  art=("navy", "security"))
F("fleet_dispersal_plan", 3, 31, "The Fleet Dispersal Plan",
  """Central Usea has announced that Ulysses will strike. A fleet crowded into one harbour is one target, so
  the navy plans to scatter it along the coast when the fragments come.""",
  [xp("navy", 10)], pre="home_anchorage_defences", band="ulysses", ai=25, art=("navy", "meteor"))
F("coastal_interdiction_patrols", 7, 31, "Coastal Interdiction Patrols",
  """A coup has broken out across Usea. Patrol boats watch the coast for arms, plotters and anyone trying to
  leave in a hurry.""",
  [stab(0.01), xp("navy", 5)], pre="home_anchorage_defences", band="coup", ai=20, art=("navy", "security"))
F("aegir_keels", 3, 32, "The Aegir Keels",
  """The first large hulls of the Aegir fleet are laid down in the new slipways. Provisional gameplay: no
  official source dates the fleet's construction.""",
  [idea("ERU_ud_aegir_keels_idea"), flag("ERU_ud_aegir_keels_laid")], pre="fleet_dispersal_plan|coastal_interdiction_patrols",
  band="stonehenge", cost=10, ai=30, art=("navy", "industry"))
F("fleet_trials", 7, 32, "Fleet Trials",
  """The new escorts run their sea trials along the coast, with Stonehenge's construction news on every
  wardroom radio.""",
  [tech("naval_equipment", 0.5)], pre="fleet_dispersal_plan|coastal_interdiction_patrols", band="stonehenge", ai=20,
  art=("navy", "tools"))
F("fleet_relief_convoys", 5, 33, "Fleet Relief Convoys",
  """Ulysses has broken apart. The fleet's transports and escorts carry relief to the coastal towns and bring
  the displaced to safer harbours.""",
  [stab(0.02), xp("navy", 10), flag("ERU_ud_relief_ready")], pre="aegir_keels|fleet_trials", band="impact", ai=25,
  art=("navy", "refugees"))

# ---------------------------------------------------------------- Continental diplomacy, lower section x 14-20
lane("diplomacy")
F("continental_desk_expands", 17, 26, "The Continental Desk Expands",
  """The foreign ministry's continental desk has done its work. Now it becomes a directorate, with an
  ambassador's office for every Usean capital and a mandate to decide what Erusea wants from its neighbours.""",
  [pp(25)], gate="has_completed_focus = ERU_exp_continental_desk", ai=25, art=("diplomacy", "document"), event=12)
F("embassies_in_every_capital", 15, 27, "Embassies in Every Capital",
  """Erusea has consulates in the trading towns and embassies in only a few capitals. It opens the rest, from
  the largest republic to the smallest principality.""",
  [pp(-15), flag("ERU_ud_embassies_opened")], pre="continental_desk_expands", ai=25, art=("diplomacy", "gate"))
F("usean_trade_missions", 19, 27, "Usean Trade Missions",
  """Trade missions carry Erusean manufacturers to the continent's fairs, with export credit and catalogues in
  every language.""",
  [tech("industry", 0.25)], pre="continental_desk_expands", ai=20, art=("economy", "diplomacy"))
F("central_usean_confidence", 15, 28, "Seek Central Usea's Confidence",
  """The Federation of Central Usea is the continent's largest power. Erusea seeks its confidence: regular
  consultations, shared statistics and no surprises.""",
  [idea("ERU_ud_central_usean_confidence_idea")], pre="embassies_in_every_capital|usean_trade_missions",
  excl="independent_course", ai=10, art=("diplomacy", "peace"))
F("independent_course", 19, 28, "An Independent Course",
  """Erusea keeps its own counsel. It trades with everyone, consults when it must and signs nothing that
  binds its hands.""",
  [idea("ERU_ud_independent_course_idea")], pre="embassies_in_every_capital|usean_trade_missions",
  excl="central_usean_confidence", ai=25, art=("diplomacy", "command"))
F("joint_border_commission", 14, 29, "A Joint Border Commission",
  """Erusean and neighbouring officials meet every month at a customs house on the frontier to settle border
  incidents before they become headlines. Most of the incidents are about cattle.""",
  [stab(0.02)], pre="central_usean_confidence", ai=10, art=("scales", "gate"))
F("military_attaches", 16, 29, "Exchange Military Attaches",
  """Erusean officers serve as attaches in the neighbouring capitals, and theirs serve in Farbanti. Each side
  learns what the other is buying.""",
  [xp("army", 5), xp("air", 5)], pre="central_usean_confidence", ai=10, art=("medal", "diplomacy"))
F("neutral_ports_policy", 18, 29, "The Neutral Ports Policy",
  """Erusean ports are open to every flag on equal terms, and closed to every warship except in distress.""",
  [tech("naval_equipment", 0.25)], pre="independent_course", ai=20, art=("navy", "scales"))
F("non_aligned_credits", 20, 29, "Non-Aligned Credits",
  """Erusea lends to the smaller Usean states on its own terms, without asking which side they are on.""",
  [pp(20)], pre="independent_course", ai=20, art=("economy", "gate"))
F("usean_summit_circuit", 17, 30, "The Usean Summit Circuit",
  """Erusea's ministers attend every continental summit, sit on every working group and speak at every dinner.
  They are remembered at most of them, and quoted at a few.""",
  [pp(30)], pre="joint_border_commission|military_attaches|neutral_ports_policy|non_aligned_credits", ai=20,
  art=("assembly", "diplomacy"))
F("join_the_ulysses_talks", 15, 31, "Join the Ulysses Talks",
  """Central Usea has announced that Ulysses will strike, and the continent's governments are talking about a
  common response. Erusea joins the talks and shares its observatory data. Provisional gameplay.""",
  [idea("ERU_ud_ulysses_partnership")], pre="usean_summit_circuit", excl="prepare_alone", band="ulysses", ai=10,
  art=("diplomacy", "meteor"))
F("prepare_alone", 19, 31, "Erusea Prepares Alone",
  """Erusea will plan for Ulysses with its own engineers, its own grain and its own shelters, and owe nobody
  for them. Provisional gameplay.""",
  [idea("ERU_ud_alone_preparation")], pre="usean_summit_circuit", excl="join_the_ulysses_talks", band="ulysses", ai=25,
  art=("shelter", "command"))
F("coup_intelligence_exchange", 15, 32, "Coup Intelligence Exchange",
  """A coup has broken out across Usea. Erusea offers its neighbours what its intelligence service knows about
  the plotters, and asks for the same in return.""",
  [stab(0.02)], pre="join_the_ulysses_talks|prepare_alone", band="coup", ai=15, art=("radar", "diplomacy"))
F("condemn_the_coup", 19, 32, "Condemn the Coup",
  """Erusea condemns the coup in every continental forum. It costs nothing, and it reminds the officer corps
  at home which side the government is on.""",
  [pp(20), stab(0.01)], pre="join_the_ulysses_talks|prepare_alone", band="coup", ai=20, art=("scales", "assembly"))
F("the_stonehenge_question", 17, 33, "The Stonehenge Question",
  """Stonehenge is complete, built under Central Usea's leadership in neutral San Salvacion. Erusea must decide
  what it says about the most powerful battery on the continent. Provisional gameplay: the official chronology
  records no Erusean position before 2003.""",
  [flag("ERU_ud_stonehenge_question_asked")], pre="coup_intelligence_exchange|condemn_the_coup", band="stonehenge", ai=20,
  art=("missile", "diplomacy"), event=13)
F("appeals_for_relief", 15, 34, "Appeals for Relief",
  """Ulysses has broken apart. Erusea appeals for relief and receives some, from neighbours who have their own
  dead to count.""",
  [stab(0.02)], pre="the_stonehenge_question", band="impact", ai=15, art=("refugees", "diplomacy"))
F("border_aid_corridors", 19, 34, "Border Aid Corridors",
  """Relief convoys cross the borders in both directions under joint escort, carrying food one way and the
  displaced the other.""",
  [stab(0.01), flag("ERU_ud_aid_corridors")], pre="the_stonehenge_question", band="impact", ai=20, art=("logistics", "gate"))
F("continental_ledger", 17, 35, "The Continental Ledger",
  """At the end of the decade the foreign ministry writes down what Erusea is owed, what it owes and who
  helped when the sky fell. The ledger will be read again.""",
  [pp(40), flag("ERU_ud_ledger_written")], pre="appeals_for_relief|border_aid_corridors", band="impact", cost=10, ai=25,
  art=("document", "diplomacy"))

# ================================================================ WAR TREE (ac_ucw_eru_tree), x 42-94
# Lanes are rooted by availability conditions on flags set by the carry-over effect or by the
# existing Continental War focuses, never by prerequisite lines into the older part of the tree.
WAR = "has_global_flag = ac_ucw_war_started"

lane("crown_war", "war")
CROWN_WAR = "has_country_flag = ERU_ud_war_crown"
F("crown_new_decade", 43, 0, "The Crown's New Decade",
  """The palace enters the new decade with its prerogative intact and its granaries empty. The camps on the
  border, the craters in the neighbours' fields and the bill for the fragment years all arrive on the same
  desk.""",
  [stab(0.02), pp(25)], gate=CROWN_WAR, ai=25, art=("medal", "rebuild"))
F("crown_speaks_for_the_grievance", 42, 1, "The Crown Speaks for the Grievance",
  """The monarch tells the nation, in a broadcast from the palace, that Erusea's suffering was ignored by the
  continent that built the battery. The grievance now has a royal voice.""",
  [ucw(grievance=5), ws(0.03)], pre="crown_new_decade", gate=CROWN_WAR, ai=25, art=("communications", "medal"))
F("palace_reconstruction_fund", 44, 1, "The Palace Reconstruction Fund",
  """The Crown estates' revenues are pledged to rebuild the districts damaged in the fragment years. Every
  rebuilt school and bridge carries a plaque with the royal arms, and nobody pretends that is an accident.""",
  [ucw(recovery=5)], pre="crown_new_decade", gate=CROWN_WAR, ai=20, art=("rebuild", "economy"))
F("household_guard_expanded", 43, 2, "The Household Guard Expands",
  """The palace guard grows into a brigade, with its own vehicles and its own officers' school. The general
  staff notices.""",
  [xp("army", 10), stab(0.01)], pre="crown_speaks_for_the_grievance|palace_reconstruction_fund", gate=CROWN_WAR, ai=20,
  art=("security", "medal"))
F("royal_mobilization_decrees", 42, 3, "Royal Mobilization Decrees",
  """The mobilization laws are reissued as royal decrees, so that the Crown, not a ministry, will call the
  reserves when the time comes.""",
  [ws(0.03)], pre="household_guard_expanded", gate=CROWN_WAR, ai=20, art=("document", "command"))
F("crown_envoys_to_the_neutrals", 44, 3, "Crown Envoys to the Neutrals",
  """Royal envoys visit the capitals that are not yet anyone's allies, with gifts, invitations and questions.
  They come home with fewer promises than gifts, and with a list of who refused to receive them.""",
  [pp(30)], pre="household_guard_expanded", gate=CROWN_WAR, ai=15, art=("diplomacy", "gate"))
F("crown_at_war", 43, 4, "The Crown at War",
  """Erusea is at war, and the Crown leads it. Every decree now carries the weight of a casualty list.""",
  [timed("ERU_ud_crown_at_war_idea", 365), ws(0.03)], pre="royal_mobilization_decrees|crown_envoys_to_the_neutrals",
  gate=CROWN_WAR + " " + WAR, ai=25, art=("command", "medal"), event=46)
F("royal_visits_to_the_front", 42, 5, "Royal Visits to the Front",
  """The monarch visits the forward airfields and the field hospitals, shakes hands with pilots and sits with the
  wounded. The newsreels do the rest, and the recruiting offices notice the difference.""",
  [ws(0.02), stab(0.02)], pre="crown_at_war", gate=CROWN_WAR + " " + WAR, ai=20, art=("medal", "medical"))
F("wartime_privy_council", 44, 5, "The Wartime Privy Council",
  """The Privy Council sits every day, with the chiefs of staff at the table. The minutes, for once, are
  secret.""",
  [pp(40)], pre="crown_at_war", gate=CROWN_WAR + " " + WAR, ai=20, art=("assembly", "command"))
F("the_crowns_burden", 43, 6, "The Crown's Burden",
  """The enemy has landed on the continent. Whatever happens now, the Crown will be held to account for the
  war it led.""",
  [stab(0.03)], pre="royal_visits_to_the_front|wartime_privy_council",
  gate=CROWN_WAR + " has_global_flag = ac_ucw_stage_counteroffensive", ai=20, art=("medal", "scales"))

lane("assembly_war")
ASSEMBLY_WAR = "has_country_flag = ERU_ud_war_assembly"
F("assembly_new_decade", 47, 0, "The Assembly's New Decade",
  """The assembly opens the new decade with a full gallery, a camp crisis on the border and a cabinet that
  promised the voters it would never close the door. The chronology says the door will close.""",
  [stab(0.02)], gate=ASSEMBLY_WAR, ai=0, art=("assembly", "refugees"))
F("refugee_hearings", 46, 1, "The Refugee Hearings",
  """Public hearings on the camps, with testimony from the displaced, the guards and the district mayors. The
  country hears what it is doing and argues about whether to stop.""",
  [ucw(grievance=-5, pressure=3)], pre="assembly_new_decade", gate=ASSEMBLY_WAR, ai=0, art=("refugees", "assembly"))
F("reconstruction_committee", 48, 1, "The Reconstruction Committee",
  """A standing committee of the assembly oversees every reconstruction contract over a set value and publishes
  the bids. Contractors complain about the paperwork. Fewer of them get rich on a ruined district.""",
  [ucw(recovery=6)], pre="assembly_new_decade", gate=ASSEMBLY_WAR, ai=0, art=("rebuild", "document"))
F("peace_caucus", 47, 2, "The Peace Caucus",
  """Deputies from every party form a caucus pledged to settle Erusea's grievances by negotiation. They are
  outnumbered, and loud.""",
  [ucw(grievance=-5)], pre="refugee_hearings|reconstruction_committee", gate=ASSEMBLY_WAR, ai=0, art=("peace", "assembly"))
F("war_powers_debate", 46, 3, "The War Powers Debate",
  """The assembly writes into law that no Erusean soldier crosses a border without its vote. The general staff
  calls it a gift to the enemy; the peace caucus calls it the least the charter owes the dead.""",
  [stab(0.03), ws(-0.03)], pre="peace_caucus", excl="emergency_powers_act", gate=ASSEMBLY_WAR, ai=0, art=("scales", "assembly"))
F("emergency_powers_act", 48, 3, "The Emergency Powers Act",
  """The cabinet receives emergency powers for the duration of any war, renewable every six months by vote.""",
  [ws(0.03), pp(30)], pre="peace_caucus", excl="war_powers_debate", gate=ASSEMBLY_WAR, ai=0, art=("document", "command"))
F("assembly_at_war", 47, 4, "The Assembly at War",
  """Erusea is at war, and its assembly voted for it or failed to stop it. Every sitting is now a war
  council.""",
  [timed("ERU_ud_assembly_at_war_idea", 365)], pre="war_powers_debate|emergency_powers_act", gate=ASSEMBLY_WAR + " " + WAR, ai=0,
  art=("assembly", "command"), event=47)
F("casualty_inquiry", 46, 5, "The Casualty Inquiry",
  """A committee of inquiry examines every major loss in public, with the generals as witnesses and the families
  in the gallery. The army hates the hearings and learns from them anyway.""",
  [stab(0.02), xp("army", 5)], pre="assembly_at_war", gate=ASSEMBLY_WAR + " " + WAR, ai=0, art=("document", "medical"))
F("wartime_coalition", 48, 5, "The Wartime Coalition",
  """Every party but the peace caucus joins a coalition cabinet for the duration. Old enemies share ministries,
  briefings and blame, and the opposition benches are suddenly very quiet.""",
  [stab(0.03), ws(0.02)], pre="assembly_at_war", gate=ASSEMBLY_WAR + " " + WAR, ai=0, art=("assembly", "ballot"))
F("armistice_motion", 47, 6, "The Armistice Motion",
  """After Los Canas the peace caucus tables a motion asking the cabinet to seek an armistice. It fails by a
  handful of votes and changes the debate anyway.""",
  [flag("ERU_ud_armistice_motion_tabled"), ws(-0.02)], pre="casualty_inquiry|wartime_coalition",
  gate=ASSEMBLY_WAR + " has_global_flag = ac_ucw_stage_los_canas", ai=0, art=("peace", "ballot"))

lane("regency_war")
REGENCY_WAR = "has_country_flag = ERU_ud_war_regency"
F("regency_new_decade", 51, 0, "The Regency's New Decade",
  """The regency council enters the new decade claiming credit for the decade just ended. The camps on the
  border are run by the army, and so is everything else.""",
  [stab(0.01), ws(0.02)], gate=REGENCY_WAR, ai=0, art=("command", "refugees"))
F("command_reconstruction", 50, 1, "Command Reconstruction",
  """Engineer brigades rebuild the damaged districts on a military schedule, with daily progress reports and no
  public tenders. Bridges go up fast; questions about who was paid go unanswered.""",
  [ucw(recovery=5)], pre="regency_new_decade", gate=REGENCY_WAR, ai=0, art=("rebuild", "command"))
F("border_command", 52, 1, "The Border Command",
  """The frontier is placed under a single command with authority over the camps, the crossings and the
  roads behind them.""",
  [ucw(pressure=-5)], pre="regency_new_decade", gate=REGENCY_WAR, ai=0, art=("gate", "security"))
F("total_mobilization_order", 51, 2, "The Total Mobilization Order",
  """The regency orders the nation's industry, transport and labour placed on a mobilization footing, in
  peacetime.""",
  [ucw(grievance=5), ws(0.03)], pre="command_reconstruction|border_command", gate=REGENCY_WAR, ai=0, art=("industry", "command"))
F("staff_war_plan_review", 50, 3, "The Staff's Plan Review",
  """The general staff reviews every contingency plan it filed in the 1990s, and updates the ones it intends
  to use.""",
  [xp("army", 15)], pre="total_mobilization_order", gate=REGENCY_WAR, ai=0, art=("document", "training"))
F("regency_propaganda_office", 52, 3, "The Regency Propaganda Office",
  """One office writes every broadcast, poster and newsreel. Its message is simple: the army saved Erusea
  once and will again.""",
  [ws(0.04), stab(-0.01)], pre="total_mobilization_order", gate=REGENCY_WAR, ai=0, art=("communications", "command"))
F("regency_at_war", 51, 4, "The Regency at War",
  """Erusea is at war, and it is governed by the men who planned it. There is nobody else to blame.""",
  [timed("ERU_ud_regency_at_war_idea", 365)], pre="staff_war_plan_review|regency_propaganda_office",
  gate=REGENCY_WAR + " " + WAR, ai=0, art=("command", "medal"), event=48)
F("command_of_the_home_front", 50, 5, "Command of the Home Front",
  """The home front is a theatre of operations, with a general in charge of rations, factories and
  morale.""",
  [stab(0.02)], pre="regency_at_war", gate=REGENCY_WAR + " " + WAR, ai=0, art=("civil", "command"))
F("staff_rotation", 52, 5, "Rotate the Staff",
  """Staff officers rotate between the ministries and the front every six months, so that the planners know
  what their plans cost.""",
  [xp("army", 10)], pre="regency_at_war", gate=REGENCY_WAR + " " + WAR, ai=0, art=("training", "logistics"))
F("regency_answers", 51, 6, "The Regency Answers",
  """The enemy has landed on the continent, and the council must answer for a war it promised to win.""",
  [stab(-0.02), ws(0.03)], pre="command_of_the_home_front|staff_rotation",
  gate=REGENCY_WAR + " has_global_flag = ac_ucw_stage_counteroffensive", ai=0, art=("scales", "command"))

# ---------------------------------------------------------------- Refugees and the home front, x 56-66
lane("home_front")
F("camps_along_the_border", 61, 0, "The Camps Along the Border",
  """The displaced of a continent are at Erusea's border and in its camps. Whatever the government decides
  about the frontier, the camps already exist and someone must run them.""",
  [flag("ERU_ud_camps_administered")], ai=25, art=("refugees", "gate"), event=43)
F("register_the_displaced", 58, 1, "Register the Displaced",
  """Every person in the camps is registered: name, origin, trade and family. The register will decide who
  works, who moves and who waits.""",
  [ucw(pressure=-3)], pre="camps_along_the_border", ai=25, art=("document", "refugees"))
F("border_medical_stations", 64, 1, "Border Medical Stations",
  """Army doctors and volunteer nurses staff medical stations at every crossing and camp, vaccinating, dressing
  wounds and counting the sick. Their reports are the first honest numbers the cabinet receives.""",
  [stab(0.02)], pre="camps_along_the_border", ai=20, art=("medical", "gate"))
F("holding_camps", 57, 2, "Holding Camps",
  """The displaced stay in guarded camps until they can be returned. It is cheap, it is orderly and it makes
  the border towns angrier by the month.""",
  [idea("ERU_ud_holding_camps_idea"), ucw(grievance=3)], pre="register_the_displaced", excl="integration_programme", ai=25,
  art=("gate", "security"))
F("integration_programme", 59, 2, "The Integration Programme",
  """Registered refugees may work, rent and study after six months. The camps empty slowly; the factories
  fill. Provisional gameplay.""",
  [idea("ERU_ud_integration_programme_idea"), ucw(grievance=-3, pressure=-4)], pre="register_the_displaced",
  excl="holding_camps", ai=0, art=("civil", "refugees"))
F("disease_control_teams", 63, 2, "Disease Control Teams",
  """Mobile teams vaccinate, test the water and isolate outbreaks before they reach the towns. A single epidemic
  in the camps would cost more lives than the fragments did in some districts.""",
  [ucw(recovery=2)], pre="border_medical_stations", ai=20, art=("medical", "science"))
F("charity_under_licence", 65, 2, "Charity Under Licence",
  """Churches, unions and foreign charities may work in the camps under a government licence that tells
  them where and how.""",
  [stab(0.01), ucw(pressure=-2)], pre="border_medical_stations", ai=20, art=("civil", "document"))
F("labour_exchanges", 58, 3, "Labour Exchanges",
  """Exchanges match the registered displaced with farms and factories that need hands. Wages are low and
  the work is real.""",
  [ucw(recovery=3), manpower(2000)], pre="holding_camps|integration_programme", ai=20, art=("industry", "refugees"))
F("public_health_ordinance", 64, 3, "The Public Health Ordinance",
  """A national ordinance sets standards for water, food and sanitation in every camp and every barracks.""",
  [stab(0.02)], pre="disease_control_teams|charity_under_licence", ai=20, art=("medical", "document"))
F("home_front_council", 61, 4, "The Home Front Council",
  """Ministries, districts, unions and employers sit on one council for the camps, the rations and the
  factories. Whatever comes next, Erusea will not improvise it.""",
  [idea("ERU_ud_home_front_council_idea")], pre="labour_exchanges|public_health_ordinance", cost=10, ai=25,
  art=("assembly", "civil"), event=44)
F("rationing_boards", 57, 5, "Rationing Boards",
  """Erusea is at war. Rationing boards in every district issue cards for fuel, meat and sugar.""",
  [idea("ERU_ud_rationing")], pre="home_front_council", gate=WAR, ai=25, art=("economy", "document"))
F("war_bonds", 59, 5, "War Bonds",
  """The treasury sells war bonds in every post office. The first issue is oversubscribed; the third is
  not.""",
  [fiscal("ac_econ_set_high_tax"), pp(40)], pre="home_front_council", gate=WAR, ai=20, art=("economy", "medal"))
F("air_raid_precautions", 63, 5, "Air-Raid Precautions",
  """The shelters built for the fragments are reopened for the bombers. Wardens, sirens and sandbags return
  to the towns.""",
  [idea("ERU_ud_air_raid_precautions_idea")], pre="home_front_council", gate=WAR, ai=25, art=("shelter", "air"))
F("blackout_ordinance", 65, 5, "The Blackout Ordinance",
  """Every town goes dark at night, from the capital's boulevards to the smallest farm. Traffic accidents rise,
  so does the sale of torches, and the night sky is visible over Erusea for the first time in a century.""",
  [stab(-0.01), ws(0.02)], pre="home_front_council", gate=WAR, ai=15, art=("shelter", "security"))
F("censored_news", 58, 6, "Censor the War News",
  """Every report from the front is read by a censor first. The papers print the communiques and the
  weather.""",
  [idea("ERU_ud_censored_news_idea")], pre="rationing_boards|war_bonds", excl="open_reporting", gate=WAR, ai=25,
  art=("communications", "security"))
F("open_reporting", 60, 6, "Open Reporting",
  """Correspondents may go to the front and report what they see, subject only to operational security. The
  country learns what the war costs, every morning.""",
  [idea("ERU_ud_open_reporting_idea")], pre="rationing_boards|war_bonds", excl="censored_news", gate=WAR, ai=5,
  art=("communications", "scales"))
F("factory_shifts", 64, 6, "Three Factory Shifts",
  """The arms plants run three shifts, seven days a week. The fourth shift is made of the displaced.""",
  [tech("industry", 0.5), stab(-0.01)], pre="air_raid_precautions|blackout_ordinance", gate=WAR, ai=20,
  art=("industry", "civil"))
F("casualty_lists", 59, 7, "The Casualty Lists",
  """The lists are posted every Friday at every town hall. Families read them before they read anything
  else.""",
  [stab(-0.01), flag("ERU_ud_casualty_lists_posted")], pre="censored_news|open_reporting", gate=WAR, ai=20,
  art=("document", "medical"), event=45)
F("labour_service", 63, 7, "The Labour Service",
  """Everyone not in uniform may be directed to essential work for the duration: farms, mines, rail yards and
  hospitals. The law is resented, obeyed and, in the border districts, enforced by the army.""",
  [manpower(3000), ws(-0.01)], pre="factory_shifts", gate=WAR, ai=20, art=("industry", "training"))
F("home_front_holds", 61, 8, "The Home Front Holds",
  """The rations are short, the lists are long and the factories have not stopped. Whatever happens at the
  front, the home front has held.""",
  [swap("ERU_ud_home_front_council_idea", "ERU_ud_home_front_held")], pre="casualty_lists|labour_service", gate=WAR, cost=10,
  ai=25, art=("civil", "medal"))

# ---------------------------------------------------------------- The Aegir fleet at war, x 70-74
lane("aegir_war")
AEGIR = "has_country_flag = ERU_ucw_aegir_fleet_done"
F("aegir_fleet_command", 72, 0, "Aegir Fleet Command",
  """The Aegir fleet has a commander, a staff and a home anchorage. It does not yet have a doctrine for a war
  against a coalition that controls the sea lanes.""",
  [xp("navy", 15)], gate=AEGIR, ai=25, art=("navy", "command"), event=49)
F("fleet_in_being", 70, 1, "A Fleet in Being",
  """The fleet's purpose is to exist: to stay in harbour under strong defences and force the enemy to guard
  against it.""",
  [idea("ERU_ud_fleet_in_being_idea")], pre="aegir_fleet_command", excl="decisive_battle_doctrine", gate=AEGIR, ai=25,
  art=("navy", "security"))
F("decisive_battle_doctrine", 74, 1, "Decisive Battle Doctrine",
  """The fleet's purpose is to find the enemy's main force and destroy it in one battle.""",
  [idea("ERU_ud_decisive_battle")], pre="aegir_fleet_command", excl="fleet_in_being", gate=AEGIR, ai=10, art=("navy", "missile"))
F("harbour_air_defence", 70, 2, "Harbour Air Defence",
  """Guns, missiles and interceptors ring the anchorage. A fleet in harbour is a target unless the sky above
  it is closed.""",
  [tech("radar_tech", 0.5)], pre="fleet_in_being", gate=AEGIR, ai=25, art=("radar", "navy"))
F("fleet_oilers", 72, 2, "Fleet Oilers",
  """Tankers and supply ships are converted to keep the fleet at sea for weeks rather than days.""",
  [tech("naval_equipment", 0.5)], pre="fleet_in_being|decisive_battle_doctrine", gate=AEGIR, ai=20, art=("logistics", "navy"))
F("battle_squadron_drills", 74, 2, "Battle Squadron Drills",
  """The capital ships exercise as one squadron, night and day, in every sea state, until manoeuvres that took an
  hour take minutes. The fuel bill is enormous. So is the squadron's confidence.""",
  [xp("navy", 15)], pre="decisive_battle_doctrine", gate=AEGIR, ai=20, art=("navy", "training"))
F("convoy_escorts", 72, 3, "Convoy Escorts",
  """Escorts are assigned to the coastal convoys that carry fuel and food to the southern ports.""",
  [tech("naval_equipment", 0.5)], pre="harbour_air_defence|fleet_oilers|battle_squadron_drills", gate=AEGIR, ai=20,
  art=("navy", "logistics"))
F("submarine_war_patrols", 71, 4, "Submarine War Patrols",
  """Erusea is at war. The submarines sail on war patrols into the sea lanes the coalition depends on.""",
  [xp("navy", 10)], pre="convoy_escorts", gate=AEGIR + " " + WAR, ai=20, art=("submarine", "navy"))
F("hold_the_home_waters", 73, 4, "Hold the Home Waters",
  """The fleet's first duty is to keep enemy ships away from the Erusean coast. Everything else comes
  second.""",
  [timed("ERU_ud_home_waters", 365)], pre="convoy_escorts", gate=AEGIR + " " + WAR, ai=25, art=("navy", "security"))
F("after_comberth", 72, 5, "After Comberth Harbor",
  """The official chronology records that ISAF sank the Aegir fleet at Comberth Harbor on 23 November 2004.
  What survives must be gathered, counted and given a purpose. Losses are not scripted by this focus.""",
  [xp("navy", 10), stab(0.01)], pre="submarine_war_patrols|hold_the_home_waters",
  gate=AEGIR + " has_global_flag = ac_ucw_brief_comberth", ai=25, art=("navy", "rebuild"), event=50)

# ---------------------------------------------------------------- Air doctrine at war, x 76-80
lane("air_war")
AIR = "has_country_flag = ERU_ucw_air_arm_done"
F("air_doctrine_board", 78, 0, "The Air Doctrine Board",
  """The air arm's commanders meet to decide how Erusea will fight for its skies against a coalition with more
  aircraft and more money.""",
  [xp("air", 15)], gate=AIR, ai=25, art=("air", "command"), event=51)
F("air_superiority_doctrine", 76, 1, "Air Superiority Doctrine",
  """Win the sky with pilots and aircraft: the best squadrons concentrated where they can fight on their own
  terms.""",
  [idea("ERU_ud_air_superiority")], pre="air_doctrine_board", excl="battery_umbrella_doctrine", gate=AIR, ai=15,
  art=("air", "medal"))
F("battery_umbrella_doctrine", 80, 1, "The Battery Umbrella",
  """If Erusea holds Stonehenge, its railguns can close the sky to enemy aircraft. Fight under the battery's
  umbrella. The official chronology records that Erusea used the railguns against aircraft; this doctrine is
  provisional gameplay.""",
  [idea("ERU_ud_battery_umbrella")], pre="air_doctrine_board", excl="air_superiority_doctrine", gate=AIR, ai=25,
  art=("missile", "air"))
F("elite_squadrons", 76, 2, "Elite Squadrons",
  """The best pilots are gathered into a few elite squadrons and sent where the fighting is hardest.""",
  [xp("air", 15)], pre="air_superiority_doctrine", gate=AIR, ai=20, art=("air", "medal"))
F("pilot_rotation", 78, 2, "Pilot Rotation",
  """Pilots rotate between the front, the training squadrons and rest, so that experience is passed on
  rather than lost.""",
  [tech("air_doctrine", 0.5)], pre="air_superiority_doctrine|battery_umbrella_doctrine", gate=AIR, ai=20,
  art=("training", "air"))
F("battery_coordination_cell", 80, 2, "Battery Coordination Cell",
  """A cell of air arm officers sits with the battery's fire controllers, so that interceptors and railguns do
  not fight each other.""",
  [xp("air", 10)], pre="battery_umbrella_doctrine", gate=AIR + " has_global_flag = ac_ucw_stonehenge_seized", ai=25,
  art=("communications", "missile"))
F("wartime_dispersal_fields", 78, 3, "Wartime Dispersal Fields",
  """Squadrons scatter to the dispersal strips surveyed in the 1990s, so that no single raid can catch them on
  the ground.""",
  [tech("construction_tech", 0.25)], pre="elite_squadrons|pilot_rotation|battery_coordination_cell", gate=AIR, ai=20,
  art=("runway", "air"))
F("aces_in_the_newsreels", 77, 4, "Aces in the Newsreels",
  """Erusea is at war. The air arm lets the newsreels film its pilots, without names, as the face of the war.""",
  [ws(0.03)], pre="wartime_dispersal_fields", gate=AIR + " " + WAR, ai=20, art=("communications", "air"))
F("fire_control_links", 79, 4, "Fire-Control Links",
  """Radar plots from the air arm's stations feed the battery's fire control directly, so that the railguns know
  where every aircraft is before it is in range. Provisional gameplay.""",
  [tech("radar_tech", 0.5)], pre="wartime_dispersal_fields",
  gate=AIR + " " + WAR + " has_global_flag = ac_ucw_stonehenge_seized", ai=20, art=("radar", "missile"))
F("air_defence_of_the_capital", 78, 5, "Air Defence of the Capital",
  """Whatever else is lost, the sky over the capital will be defended to the last squadron.""",
  [timed("ERU_ud_capital_air_defence", 365)], pre="aces_in_the_newsreels|fire_control_links", gate=AIR + " " + WAR, ai=25,
  art=("air", "security"))

# ---------------------------------------------------------------- Megalith, x 82-86
lane("megalith")
MEGALITH = "has_country_flag = ERU_ucw_megalith_done"
F("megalith_directorate", 84, 0, "The Megalith Directorate",
  """Megalith is an Erusean fortress built to bring down orbiting Ulysses fragments, according to the official
  record. A directorate now answers for its engineers, its budget and its secrets. No construction date is
  given or implied.""",
  [idea("ERU_ud_megalith_directorate_idea")], gate=MEGALITH, ai=20, art=("meteor", "command"), event=52)
F("fragment_interception_studies", 82, 1, "Fragment Interception Studies",
  """The directorate's scientists study the orbiting fragments that Megalith was built to bring down: their
  orbits, their decay and their danger.""",
  [tech("rocketry", 0.5)], pre="megalith_directorate", gate=MEGALITH, ai=20, art=("meteor", "science"))
F("engineers_quarters", 86, 1, "The Engineers' Quarters",
  """The engineers and their families live in closed quarters near the site, with good pay and no
  visitors.""",
  [stab(0.01)], pre="megalith_directorate", gate=MEGALITH, ai=20, art=("civil", "security"))
F("megalith_security_perimeter", 84, 2, "The Security Perimeter",
  """A security perimeter with its own garrison, checkpoints and counter-intelligence officers surrounds the
  site. Nobody enters without a pass signed in the capital, and nobody leaves with a notebook.""",
  [xp("army", 5)], pre="fragment_interception_studies|engineers_quarters", gate=MEGALITH, ai=20, art=("security", "gate"))
F("shield_against_the_sky", 82, 3, "A Shield Against the Sky",
  """The directorate insists that Megalith remains what it was built to be: a defence against the sky, not a
  weapon in the war.""",
  [stab(0.03), flag("ERU_ud_megalith_shield")], pre="megalith_security_perimeter", excl="under_military_seal", gate=MEGALITH,
  ai=10, art=("shelter", "meteor"))
F("under_military_seal", 86, 3, "Under Military Seal",
  """The general staff places Megalith under military seal. What it is for becomes a question only the staff
  may ask. Provisional gameplay.""",
  [ws(0.02), flag("ERU_ud_megalith_sealed")], pre="megalith_security_perimeter", excl="shield_against_the_sky", gate=MEGALITH,
  ai=20, art=("security", "missile"))
F("watch_the_young_officers", 84, 4, "Watch the Young Officers",
  """Some of the young officers at Megalith talk about what they would do if the war were lost. The
  counter-intelligence officers write it down. The official chronology records that young officers seized
  Megalith after the surrender.""",
  [flag("ERU_ud_young_officers_watched")], pre="shield_against_the_sky|under_military_seal", gate=MEGALITH, ai=20,
  art=("security", "document"), event=53)
F("megaliths_ledger", 84, 5, "Megalith's Ledger",
  """The directorate keeps a complete ledger of the site's people, budget and work, so that whatever happens,
  someone will be able to account for it.""",
  [pp(30)], pre="watch_the_young_officers", gate=MEGALITH, ai=20, art=("document", "meteor"))
F("after_the_megalith", 84, 6, "After the Megalith",
  """The official chronology records that ISAF destroyed Megalith after young officers seized it, and that
  Erusea formed a provisional autonomous government under ISAF oversight. The directorate's ledger is handed
  to the provisional authorities.""",
  [stab(0.03)], pre="megaliths_ledger", gate=MEGALITH + " has_global_flag = ac_ucw_megalith_destroyed", ai=25,
  art=("rebuild", "document"), event=61)

# ---------------------------------------------------------------- Administering occupied territory, x 88-94
# No ownership, core or controller changes: occupation is shown through ideas and flags only.
lane("occupation")
OCCUPATION = "ac_ucw_war_running = yes has_global_flag = ac_ucw_stonehenge_seized"
F("occupation_authority", 91, 0, "The Occupation Authority",
  """Erusean forces hold Stonehenge and the territory around it. An occupation authority is created to govern
  what the army holds, under the laws of war and without annexing anything.""",
  [flag("ERU_ud_occupation_governed")], gate=OCCUPATION, ai=20, art=("command", "document"), event=54)
F("military_administration", 89, 1, "Military Administration",
  """Occupied districts are governed by army officers under martial law, with orders posted in two languages on
  every town hall door. It is fast, firm and widely hated.""",
  [idea("ERU_ud_military_administration_idea")], pre="occupation_authority", excl="civil_commissioners", gate=OCCUPATION, ai=20,
  art=("security", "command"))
F("civil_commissioners", 93, 1, "Civil Commissioners",
  """Occupied districts are governed by civilian commissioners from the interior ministry, with the army in
  support rather than in charge. It is slower, more correct and slightly less hated.""",
  [idea("ERU_ud_civil_commissioners_idea")], pre="occupation_authority", excl="military_administration", gate=OCCUPATION, ai=10,
  art=("civil", "scales"))
F("curfew_ordinances", 88, 2, "Curfew Ordinances",
  """A curfew from dusk to dawn in every occupied town, enforced by patrols with lists of the few who may be out
  at night: doctors, midwives and the patrols themselves.""",
  [xp("army", 5)], pre="military_administration", gate=OCCUPATION, ai=20, art=("security", "gate"))
F("requisition_rules", 90, 2, "Requisition Rules",
  """The army may requisition food and fuel only with written receipts and fixed prices, payable by the
  occupation authority. The rules are not always kept, but they are written down.""",
  [stab(0.01)], pre="military_administration", gate=OCCUPATION, ai=20, art=("document", "logistics"))
F("local_councils", 92, 2, "Local Councils",
  """Existing town councils keep working under the commissioners' supervision, collecting rubbish, running
  schools and quietly deciding which Erusean orders to obey first.""",
  [stab(0.01)], pre="civil_commissioners", gate=OCCUPATION, ai=10, art=("assembly", "civil"))
F("food_distribution", 94, 2, "Food Distribution",
  """The occupation authority distributes food in the towns it governs, under the eyes of the neutral relief
  agencies.""",
  [stab(0.01)], pre="civil_commissioners", gate=OCCUPATION, ai=10, art=("economy", "refugees"))
F("camp_inspectors", 89, 3, "Inspectors for the Camps",
  """Independent inspectors visit every detention and displaced persons' camp in occupied territory and report
  to the occupation authority.""",
  [stab(0.01)], pre="curfew_ordinances|requisition_rules|local_councils|food_distribution", gate=OCCUPATION, ai=15,
  art=("scales", "refugees"))
F("occupation_courts", 93, 3, "Occupation Courts",
  """Courts with Erusean judges and local assessors hear cases under the occupation's published code. The
  verdicts are recorded, and the records will be read by whoever governs next.""",
  [stab(0.01)], pre="curfew_ordinances|requisition_rules|local_councils|food_distribution", gate=OCCUPATION, ai=15,
  art=("scales", "document"))
F("occupation_review", 91, 4, "The Occupation Review",
  """A year into the occupation, the authority reviews what it governs and what it costs: garrisons, food, courts
  and resentment. The review is circulated to the cabinet and to nobody else.""",
  [pp(30)], pre="camp_inspectors|occupation_courts", gate=OCCUPATION, ai=20, art=("document", "command"))
F("withdrawal_plans", 91, 5, "Withdrawal Plans",
  """The enemy has landed on the continent. The authority prepares to hand back what it governs in good
  order, if it must.""",
  [stab(0.02)], pre="occupation_review", gate="ac_ucw_war_running = yes has_global_flag = ac_ucw_stage_counteroffensive",
  ai=20, art=("logistics", "document"))

# ---------------------------------------------------------------- Postwar lanes, one per outcome, y 10-15
# Linked by flags to the existing outcome focuses and to the Free Erusea content; no government change.
lane("postwar_isaf")
OVERSIGHT = "has_country_flag = ERU_ucw_provisional_government_done"
F("under_oversight", 46, 10, "Under Oversight",
  """Erusea has surrendered. The official chronology records that it formed a provisional autonomous
  government under ISAF oversight. The government is not replaced by this focus; it learns to work under
  supervision.""",
  [stab(0.02)], gate=OVERSIGHT, ai=25, art=("scales", "peace"), event=55)
F("disarmament_registry", 44, 11, "The Disarmament Registry",
  """Every weapon, unit and depot is registered with the oversight commission, down to the last rifle in the last
  district armoury. The registry is checked, and then checked again.""",
  [stab(0.01)], pre="under_oversight", gate=OVERSIGHT, ai=25, art=("document", "security"))
F("return_of_the_prisoners", 48, 11, "Return of the Prisoners",
  """Prisoners of war come home by train, carriage after carriage, and the stations are full of families holding
  photographs. Some of the photographs are of men who are not on any train.""",
  [stab(0.02), manpower(2000)], pre="under_oversight", gate=OVERSIGHT, ai=25, art=("rail", "peace"))
F("cooperate_with_the_commission", 44, 12, "Cooperate with the Commission",
  """The provisional government cooperates fully with the oversight commission, opens its files and asks to be
  judged by its record. It is humbling. It is also the fastest way out from under supervision.""",
  [idea("ERU_ud_oversight_cooperation")], pre="disarmament_registry|return_of_the_prisoners",
  excl="quiet_non_cooperation", gate=OVERSIGHT, ai=25, art=("peace", "assembly"))
F("quiet_non_cooperation", 48, 12, "Quiet Non-Cooperation",
  """The government complies with every order of the commission slowly, and with none of them completely. Files
  go missing, inspections are delayed and the commission's patience wears thin.""",
  [ws(0.03), flag("ERU_ud_unreconciled")], pre="disarmament_registry|return_of_the_prisoners",
  excl="cooperate_with_the_commission", gate=OVERSIGHT, ai=5, art=("security", "document"))
F("demobilization_boards", 43, 13, "Demobilization Boards",
  """Boards in every district discharge the conscripts, return their papers and find them work on farms, in
  factories and on the reconstruction sites. A discharged soldier with a job is not a recruit for anyone.""",
  [manpower(-2000), stab(0.02)], pre="cooperate_with_the_commission", gate=OVERSIGHT, ai=25, art=("civil", "training"))
F("veterans_pensions", 45, 13, "Veterans' Pensions",
  """Pensions for the wounded and the families of the dead are paid from the first postwar budget. They are
  smaller than the veterans' leagues demanded and larger than the treasury wanted.""",
  [stab(0.03), pp(-20)], pre="cooperate_with_the_commission", gate=OVERSIGHT, ai=20, art=("medal", "economy"))
F("the_unreconciled", 49, 13, "The Unreconciled",
  """Some officers will not accept the surrender. The government knows their names, their meeting places and
  their grievances, and decides for now to watch rather than act.""",
  [flag("ERU_ud_unreconciled_known")], pre="quiet_non_cooperation", gate=OVERSIGHT, ai=5, art=("security", "medal"))
F("watch_the_veterans_leagues", 46, 14, "Watch the Veterans' Leagues",
  """Veterans' leagues are meeting in back rooms. Some want pensions; some want another war. The government
  watches both, and reads the reports on any armed insurrection carefully.""",
  ["if = { limit = { has_global_flag = ac_fe_insurrection_started } add_stability = 0.02 }",
   flag("ERU_ud_leagues_watched")], pre="demobilization_boards|veterans_pensions|the_unreconciled", gate=OVERSIGHT, ai=20,
  art=("security", "civil"))
F("a_provisional_order", 46, 15, "A Provisional Order",
  """The provisional government has a registry, a budget and a working relationship with its supervisors.
  It is not sovereign in the old sense. It is functioning.""",
  [swap("ERU_ud_oversight_cooperation", "ERU_ud_provisional_order"), flag("ERU_ud_provisional_order_working")],
  pre="watch_the_veterans_leagues", gate=OVERSIGHT, cost=10, ai=25, art=("assembly", "peace"), event=56)

lane("postwar_victory")
VICTORY = "has_country_flag = ERU_ucw_victors_order_done"
F("victors_peace", 60, 10, "The Victor's Peace",
  """Erusea has won the war in this alternate history. It now governs a continent it does not own, in a
  peace it has to keep. Provisional gameplay: in the official chronology Erusea surrendered in 2005.""",
  [ws(0.03)], gate=VICTORY, ai=25, art=("medal", "scales"), event=57)
F("occupation_without_annexation", 58, 11, "Occupation Without Annexation",
  """Erusea annexes nothing. Its garrisons stay in the defeated countries as guarantors of the peace, under
  published terms with a published end date that nobody quite believes.""",
  [stab(0.02)], pre="victors_peace", gate=VICTORY, ai=25, art=("security", "document"))
F("victory_parade_question", 62, 11, "The Victory Parade Question",
  """The general staff wants a parade through Farbanti. The treasury wants to know who pays for it.""",
  [ws(0.02), pp(-15)], pre="victors_peace", gate=VICTORY, ai=20, art=("medal", "economy"))
F("magnanimous_peace", 58, 12, "A Magnanimous Peace",
  """Erusea offers its defeated neighbours generous terms: no reparations, early withdrawal and help with
  reconstruction. The general staff calls it throwing away the victory. The neutral capitals call it wisdom.""",
  [idea("ERU_ud_magnanimous_peace_idea")], pre="occupation_without_annexation|victory_parade_question", excl="hard_peace",
  gate=VICTORY, ai=10, art=("peace", "rebuild"))
F("hard_peace", 62, 12, "A Hard Peace",
  """Erusea demands guarantees, garrisons and payment for the decade it suffered. The terms are signed under
  protest, and the protest is remembered longer than the signatures.""",
  [idea("ERU_ud_hard_peace_idea")], pre="occupation_without_annexation|victory_parade_question", excl="magnanimous_peace",
  gate=VICTORY, ai=25, art=("scales", "security"))
F("reconstruction_credits", 57, 13, "Reconstruction Credits",
  """Erusean banks lend to the rebuilding of the neighbours' cities on easy terms, guaranteed by the treasury.
  The loans buy goodwill, contracts for Erusean firms and a great deal of influence.""",
  [pp(-25), stab(0.02)], pre="magnanimous_peace", gate=VICTORY, ai=20, art=("economy", "rebuild"))
F("prisoner_releases", 59, 13, "Prisoner Releases",
  """All prisoners of war are released within the year, without exchange and without conditions. Their
  governments receive them with relief, and Erusea receives a rare word of thanks.""",
  [stab(0.02)], pre="magnanimous_peace", gate=VICTORY, ai=20, art=("peace", "rail"))
F("reparations_demands", 61, 13, "Reparations Demands",
  """The defeated pay reparations in kind: grain, steel and fuel, delivered by rail to Erusean depots. The
  deliveries are on time, resented and carefully counted by both sides.""",
  [tech("industry", 0.5), stab(-0.01)], pre="hard_peace", gate=VICTORY, ai=20, art=("economy", "logistics"))
F("garrison_rotation_abroad", 63, 13, "Garrisons Abroad",
  """Regiments rotate through the foreign garrisons every year. Morale is poor, discipline is worse and the
  soldiers write home about streets where nobody speaks to them.""",
  [xp("army", 10), stab(-0.01)], pre="hard_peace", gate=VICTORY, ai=20, art=("security", "logistics"))
F("demobilize_the_reserves", 60, 14, "Demobilize the Reserves",
  """The reservists go home. The ones who stay are the ones who have nowhere else to go.""",
  [manpower(-3000), stab(0.03)],
  pre="reconstruction_credits|prisoner_releases|reparations_demands|garrison_rotation_abroad", gate=VICTORY, ai=25,
  art=("civil", "rail"))
F("the_continental_order", 60, 15, "The Continental Order",
  """Erusea's peace has a shape: garrisons, treaties and debts. Whether it is an order or an occupation
  depends on who is asked.""",
  [flag("ERU_ud_continental_order")], pre="demobilize_the_reserves", gate=VICTORY, cost=10, ai=25,
  art=("diplomacy", "medal"), event=58)

lane("postwar_armistice")
ARMISTICE = "has_country_flag = ERU_ucw_armistice_line_done"
F("the_line_holds", 74, 10, "The Line Holds",
  """The war ended without a decision, or never began. Erusea and its neighbours face each other across a
  line that nobody has agreed to call a border. Provisional gameplay.""",
  [stab(0.02)], gate=ARMISTICE, ai=25, art=("gate", "scales"), event=59)
F("demarcation_patrols", 72, 11, "Demarcation Patrols",
  """Joint patrols walk the line every week, so that an incident does not become a war.""",
  [stab(0.01)], pre="the_line_holds", gate=ARMISTICE, ai=25, art=("security", "peace"))
F("prisoner_lists", 76, 11, "Prisoner Lists",
  """Both sides exchange lists of the prisoners they hold and the missing they are looking for.""",
  [stab(0.02)], pre="the_line_holds", gate=ARMISTICE, ai=20, art=("document", "peace"))
F("keep_the_line_manned", 72, 12, "Keep the Line Manned",
  """The army stays on the armistice line at full strength until a treaty is signed. It is expensive, it is safe
  and it keeps a great many reservists away from the farms that need them.""",
  [idea("ERU_ud_line_manned")], pre="demarcation_patrols|prisoner_lists", excl="thin_the_line", gate=ARMISTICE, ai=25,
  art=("security", "gate"))
F("thin_the_line", 76, 12, "Thin the Line",
  """The army leaves a screen of regulars on the line and sends the reservists home to rebuild. It is a bet that
  the other side wants peace as much as Erusea does.""",
  [idea("ERU_ud_line_thinned")], pre="demarcation_patrols|prisoner_lists", excl="keep_the_line_manned", gate=ARMISTICE,
  ai=10, art=("rebuild", "civil"))
F("fortify_the_line", 71, 13, "Fortify the Line",
  """Bunkers, minefields and observation posts are built along the whole armistice line, so that a smaller
  garrison can hold it. The concrete makes the line look permanent, which it may become.""",
  [tech("construction_tech", 0.5)], pre="keep_the_line_manned", gate=ARMISTICE, ai=20, art=("security", "tools"))
F("reservist_rotation", 73, 13, "Reservist Rotation",
  """Reservists serve three months on the line every two years, so that the burden is shared and every district
  knows what the line looks like at night.""",
  [xp("army", 10)], pre="keep_the_line_manned", gate=ARMISTICE, ai=20, art=("training", "rail"))
F("return_of_the_reservists", 75, 13, "Return of the Reservists",
  """The reservists come home to farms and factories that have waited for them, and to towns that held their jobs
  open. The harvest that year is the best since the fragments.""",
  [manpower(-2000), stab(0.03)], pre="thin_the_line", gate=ARMISTICE, ai=20, art=("civil", "rail"))
F("armistice_commission", 77, 13, "The Armistice Commission",
  """A standing commission of officers from both sides meets monthly to settle incidents along the line. Its
  meetings are dull, which is exactly what they are for.""",
  [stab(0.02)], pre="thin_the_line", gate=ARMISTICE, ai=20, art=("assembly", "scales"))
F("the_long_armistice", 74, 14, "The Long Armistice",
  """The line holds for another year, and then another. An armistice that lasts long enough starts to look
  like a peace.""",
  [flag("ERU_ud_long_armistice"), stab(0.03)],
  pre="fortify_the_line|reservist_rotation|return_of_the_reservists|armistice_commission", gate=ARMISTICE, cost=10, ai=25,
  art=("peace", "gate"), event=60)
F("recovery_before_revenge", 74, 15, "Recovery Before Revenge",
  """The government tells the country that the next decade belongs to rebuilding, not to settling scores.""",
  [ucw(grievance=-5, recovery=5)], pre="the_long_armistice",
  gate=ARMISTICE, ai=0, art=("rebuild", "peace"))

# ================================================================ NATIONAL SPIRITS
# (title, description, modifiers, art pair). All values are provisional gameplay.
IDEAS = {
    # Court and Crown
    "ERU_ud_court_ledger": ("The Court Ledger", "The court has been mapped. It has not yet been tamed.",
                            {"political_power_gain": 0.05, "stability_factor": -0.02}, ("document", "assembly")),
    "ERU_ud_court_chancery": ("The Palace Chancery", "One chancery, one register of decrees and one signature that means the same thing everywhere.",
                              {"political_power_gain": 0.1}, ("document", "communications")),
    "ERU_ud_crown_estates": ("Crown Estates Leases", "Leases on the Crown's farms, forests and harbours fund public works without a new tax.",
                             {"production_speed_infrastructure_factor": 0.1, "stability_factor": -0.01}, ("economy", "fishing")),
    "ERU_ud_prerogative_rule": ("Rule by Prerogative", "Ministers serve at the palace's pleasure, and the palace intends to be pleased.",
                                {"political_power_gain": 0.1, "democratic_drift": -0.02, "stability_factor": 0.02}, ("command", "medal")),
    "ERU_ud_royal_secretariat": ("The Royal Secretariat", "A cabinet of secretaries, appointed and dismissed by the Crown.",
                                 {"political_power_gain": 0.15, "democratic_drift": -0.03, "stability_factor": 0.03}, ("command", "document")),
    "ERU_ud_intendants": ("Provincial Intendants", "Royal intendants govern the districts with authority over prefects, police and public works.",
                          {"production_speed_buildings_factor": 0.05, "stability_factor": 0.02}, ("civil", "command")),
    "ERU_ud_officers_oath_idea": ("The Officers' Oath", "Every officer has sworn personally to the Crown.",
                             {"army_morale_factor": 0.03, "fascism_drift": -0.02}, ("medal", "security")),
    "ERU_ud_old_houses_idea": ("Patronage of the Old Houses", "The landed families govern the districts for the Crown, and expect to be thanked.",
                          {"stability_factor": 0.05, "research_speed_factor": -0.02}, ("scales", "civil")),
    "ERU_ud_crown_technocrats_idea": ("Crown Technocrats", "Engineers and economists of the royal academies run the ministries on merit.",
                                 {"research_speed_factor": 0.04, "stability_factor": -0.02}, ("science", "tools")),
    "ERU_ud_royal_commission": ("The Royal Ulysses Commission", "A royal commission with power to requisition, build and plan for the fragments.",
                                {"production_speed_buildings_factor": 0.05, "consumer_goods_factor": 0.02}, ("meteor", "command")),
    "ERU_ud_loyal_regiments_idea": ("The Loyal Regiments", "Regiments that held to their oath during the coup year garrison the capital.",
                               {"army_org_factor": 0.03, "stability_factor": 0.02}, ("security", "medal")),
    "ERU_ud_emergency_prerogative_idea": ("Emergency Prerogative", "For one year the Crown legislates by decree alone.",
                                     {"political_power_factor": 0.1, "stability_factor": 0.02}, ("command", "document")),
    "ERU_ud_crown_tribunals_idea": ("Tribunals of the Crown", "Royal tribunals try those who broke their oath, in closed session.",
                               {"stability_factor": 0.03, "democratic_drift": -0.03, "war_support_factor": 0.02}, ("scales", "security")),
    "ERU_ud_unbroken_crown_idea": ("The Unbroken Crown", "The Crown governed Erusea through the fragment years, and intends to govern it through the next decade.",
                              {"political_power_gain": 0.15, "stability_factor": 0.05, "war_support_factor": 0.03, "democratic_drift": -0.03},
                              ("medal", "command")),
    # Constitution
    "ERU_ud_drafting_commission_idea": ("The Drafting Commission", "A constitution is being written, and every faction wants a clause.",
                                   {"political_power_gain": -0.05, "democratic_drift": 0.05}, ("document", "assembly")),
    "ERU_ud_party_politics": ("Legal Parties", "The parties organize, campaign and argue in public for the first time.",
                              {"stability_factor": -0.02, "democratic_drift": 0.05}, ("ballot", "civil")),
    "ERU_ud_constitutional_cabinet": ("The Constitutional Cabinet", "A cabinet responsible to an elected assembly governs under a written charter.",
                                      {"stability_factor": 0.05, "political_power_gain": 0.05, "war_support_factor": -0.05}, ("ballot", "assembly")),
    "ERU_ud_civilian_control": ("Civilian Control", "A civilian minister answers to the assembly for the armed forces.",
                                {"fascism_drift": -0.05, "war_support_factor": -0.03, "stability_factor": 0.03}, ("command", "scales")),
    "ERU_ud_assembly_committee": ("The Assembly's Ulysses Committee", "A cross-party committee plans for the fragments with published numbers.",
                                  {"production_speed_buildings_factor": 0.05, "stability_factor": 0.02}, ("meteor", "assembly")),
    "ERU_ud_defended_assembly": ("The Defended Assembly", "The public stood around the chamber during the coup year, and the assembly remembers.",
                                 {"stability_factor": 0.05, "democratic_drift": 0.03}, ("assembly", "security")),
    "ERU_ud_constitutional_settlement_idea": ("The Constitutional Settlement", "A charter, an assembly, an independent bench and a monarchy above the fray.",
                                         {"stability_factor": 0.08, "democratic_drift": 0.03, "political_power_gain": 0.05}, ("assembly", "peace")),
    # Regency
    "ERU_ud_regency_council": ("The Regency Council", "Serving officers govern in the Crown's name through a command administration.",
                               {"political_power_gain": 0.1, "stability_factor": -0.03, "war_support_factor": 0.05}, ("command", "medal")),
    "ERU_ud_command_administration_idea": ("Command Administration", "Ministries are directorates, ministers are directors and every file is classified.",
                                      {"industrial_capacity_factory": 0.05, "stability_factor": -0.02}, ("command", "document")),
    "ERU_ud_mobilization_economy_idea": ("A Mobilization Economy", "Arms first, rail second, households last.",
                                    {"production_speed_arms_factory_factor": 0.1, "consumer_goods_factor": 0.03}, ("industry", "command")),
    "ERU_ud_garrison_austerity_idea": ("Garrison Austerity", "An army government that spends less on itself than its predecessors did.",
                                  {"consumer_goods_factor": -0.03, "army_org_factor": -0.03, "stability_factor": 0.02}, ("economy", "security")),
    "ERU_ud_civil_defence_command_idea": ("Civil Defence Command", "One command, with a general at its head, prepares the districts for the fragments.",
                                     {"production_speed_buildings_factor": 0.05, "stability_factor": 0.02, "democratic_drift": -0.02},
                                     ("meteor", "security")),
    "ERU_ud_martial_law": ("Martial Law Ordinances", "For one year military courts and curfews keep the coup's contagion out of Erusea.",
                           {"stability_factor": 0.05, "political_power_gain": -0.05, "democratic_drift": -0.05}, ("security", "document")),
    "ERU_ud_relief_directorate": ("The Relief Directorate", "Relief is run as a military operation, with a staff and a war diary.",
                                  {"stability_factor": 0.04, "production_speed_buildings_factor": 0.05}, ("command", "medical")),
    "ERU_ud_regency_mandate": ("The Regency's Mandate", "The council claims the mandate it says it earned in the fragment years.",
                               {"political_power_gain": 0.1, "war_support_factor": 0.05, "army_org_factor": 0.03}, ("command", "medal")),
    "ERU_ud_restored_council": ("The Restored Crown Council", "The seals of office are back with the Crown, and the officers are back in their barracks.",
                                {"stability_factor": 0.08, "political_power_gain": 0.05}, ("medal", "peace")),
    # Industry and rail
    "ERU_ud_state_railways": ("The State Railways Trust", "One public trust owns every line and keeps a second timetable for the army.",
                              {"production_speed_infrastructure_factor": 0.15, "consumer_goods_factor": 0.01}, ("rail", "command")),
    "ERU_ud_concession_railways_idea": ("Concession Railways", "Private operators run the main lines under thirty-year concessions.",
                                   {"production_speed_infrastructure_factor": 0.1, "consumer_goods_factor": -0.02, "stability_factor": -0.01},
                                   ("rail", "economy")),
    "ERU_ud_steel_quota_idea": ("The Steel Quota", "Heavy industry first, with guaranteed prices for the mills.",
                           {"industrial_capacity_factory": 0.05, "consumer_goods_factor": 0.02}, ("industry", "economy")),
    "ERU_ud_light_industry": ("Light Industry First", "Credit for the mills and workshops that employ half the towns.",
                              {"consumer_goods_factor": -0.03, "stability_factor": 0.02}, ("economy", "civil")),
    "ERU_ud_modern_slipways": ("Modern Slipways", "Covered slipways, new cranes and welding halls in the national yards.",
                               {"industrial_capacity_dockyard": 0.05, "production_speed_dockyard_factor": 0.05}, ("navy", "tools")),
    "ERU_ud_fuel_reserves": ("Strategic Fuel Reserves", "A season's fuel for the army, the air arm and the fleet, held in tank farms.",
                             {"fuel_gain_factor": 0.05, "supply_consumption_factor": -0.02}, ("logistics", "industry")),
    "ERU_ud_hardened_industry": ("Hardened Factories", "Buried transformers and reinforced roofs keep the plants working through a strike.",
                                 {"industry_repair_factor": 0.1, "production_speed_buildings_factor": -0.02}, ("shelter", "industry")),
    "ERU_ud_dispersed_industry": ("Dispersed Industry", "Key plants have moved into the small towns, so no single strike can stop an industry.",
                                  {"industry_repair_factor": 0.05, "production_factory_max_efficiency_factor": 0.02}, ("logistics", "industry")),
    "ERU_ud_relief_trains_idea": ("Relief Trains", "Relief runs on the military timetable.",
                             {"stability_factor": 0.03, "production_speed_infrastructure_factor": 0.05}, ("rail", "refugees")),
    # Army, air arm and fleet
    "ERU_ud_mass_reserve": ("A Mass Reserve Army", "A small regular army and a very large trained reserve, called up by district.",
                            {"conscription_factor": 0.05, "training_time_army_factor": -0.05}, ("training", "civil")),
    "ERU_ud_professional_corps": ("A Professional Mobile Corps", "Fewer soldiers, longer service and more vehicles.",
                                  {"army_org_factor": 0.05, "army_speed_factor": 0.05}, ("logistics", "training")),
    "ERU_ud_pilot_academy_idea": ("The Pilot Academy", "One academy, modern simulators and instructors from the operational squadrons.",
                             {"air_training_xp_gain_factor": 0.1, "experience_gain_air_factor": 0.05}, ("air", "training")),
    "ERU_ud_interceptor_doctrine_idea": ("Interceptor Doctrine", "Own the sky over Erusea with interceptors and ground radar.",
                                    {"air_superiority_efficiency": 0.05, "static_anti_air_damage_factor": 0.05}, ("air", "radar")),
    "ERU_ud_strike_doctrine_idea": ("Strike Doctrine", "The air arm exists to support the army.",
                               {"air_cas_efficiency": 0.05, "army_attack_factor": 0.02}, ("air", "missile")),
    "ERU_ud_battle_line": ("The Battle Line", "The Aegir fleet is built around large surface combatants.",
                           {"naval_damage_factor": 0.05, "navy_org_factor": 0.03}, ("navy", "command")),
    "ERU_ud_escort_screen": ("Escort and Submarine Screen", "The Aegir fleet is built to protect the coast and the convoys.",
                             {"convoy_escort_efficiency": 0.1, "navy_submarine_detection_factor": 0.05}, ("submarine", "navy")),
    "ERU_ud_aegir_keels_idea": ("The Aegir Keels", "The first large hulls of the Aegir fleet are on the slipways.",
                           {"production_speed_dockyard_factor": 0.1, "industrial_capacity_dockyard": 0.05}, ("navy", "industry")),
    # Diplomacy
    "ERU_ud_central_usean_confidence_idea": ("Confidence with Central Usea", "Regular consultations, shared statistics and no surprises.",
                                        {"trade_opinion_factor": 0.1, "war_support_factor": -0.03}, ("diplomacy", "peace")),
    "ERU_ud_independent_course_idea": ("An Independent Course", "Erusea trades with everyone and signs nothing that binds it.",
                                  {"war_support_factor": 0.03, "political_power_gain": 0.05}, ("diplomacy", "command")),
    "ERU_ud_ulysses_partnership": ("Ulysses Partnership", "Erusean observatories share their data with the continent's response.",
                                   {"research_speed_factor": 0.03, "stability_factor": 0.02}, ("diplomacy", "meteor")),
    "ERU_ud_alone_preparation": ("Preparing Alone", "Erusea prepares for Ulysses with its own engineers, grain and shelters.",
                                 {"production_speed_buildings_factor": 0.05, "war_support_factor": 0.03}, ("shelter", "command")),
    # War-era politics
    "ERU_ud_crown_at_war_idea": ("The Crown at War", "Every royal decree carries the weight of a casualty list.",
                            {"war_support_factor": 0.05, "stability_factor": 0.02}, ("command", "medal")),
    "ERU_ud_assembly_at_war_idea": ("The Assembly at War", "Every sitting of the assembly is a war council.",
                               {"stability_factor": 0.04, "war_support_factor": -0.02}, ("assembly", "command")),
    "ERU_ud_regency_at_war_idea": ("The Regency at War", "The men who planned the war are governing it.",
                              {"war_support_factor": 0.05, "army_org_factor": 0.03, "stability_factor": -0.02}, ("command", "security")),
    # Home front
    "ERU_ud_holding_camps_idea": ("Holding Camps", "The displaced wait in guarded camps until they can be returned.",
                             {"stability_factor": -0.02, "war_support_factor": 0.03}, ("gate", "security")),
    "ERU_ud_integration_programme_idea": ("The Integration Programme", "Registered refugees may work, rent and study after six months.",
                                     {"stability_factor": 0.02, "conscription_factor": 0.02, "consumer_goods_factor": 0.02}, ("civil", "refugees")),
    "ERU_ud_home_front_council_idea": ("The Home Front Council", "Ministries, districts, unions and employers sit on one council.",
                                  {"production_speed_buildings_factor": 0.05, "stability_factor": 0.02}, ("assembly", "civil")),
    "ERU_ud_home_front_held": ("The Home Front Held", "The rations were short and the factories never stopped.",
                               {"stability_factor": 0.05, "war_support_factor": 0.03, "production_factory_efficiency_gain_factor": 0.05},
                               ("civil", "medal")),
    "ERU_ud_rationing": ("Rationing", "Fuel, meat and sugar are rationed by district boards.",
                         {"consumer_goods_factor": -0.03, "stability_factor": -0.02}, ("economy", "document")),
    "ERU_ud_air_raid_precautions_idea": ("Air-Raid Precautions", "Wardens, sirens and the shelters built for the fragments.",
                                    {"industry_repair_factor": 0.1, "stability_factor": 0.01}, ("shelter", "air")),
    "ERU_ud_censored_news_idea": ("Censored War News", "The papers print the communiques and the weather.",
                             {"war_support_factor": 0.05, "stability_factor": -0.01}, ("communications", "security")),
    "ERU_ud_open_reporting_idea": ("Open Reporting", "Correspondents report what they see at the front.",
                              {"stability_factor": 0.03, "war_support_factor": -0.03}, ("communications", "scales")),
    # The Aegir fleet, the air arm and Megalith at war
    "ERU_ud_fleet_in_being_idea": ("A Fleet in Being", "The fleet's purpose is to exist, and to be guarded against.",
                              {"navy_org_factor": 0.05, "repair_speed_factor": 0.05}, ("navy", "security")),
    "ERU_ud_decisive_battle": ("Decisive Battle Doctrine", "Find the enemy's main force and destroy it in one battle.",
                               {"naval_damage_factor": 0.08, "navy_org_factor": -0.02}, ("navy", "missile")),
    "ERU_ud_home_waters": ("Hold the Home Waters", "The fleet's first duty is the Erusean coast.",
                           {"navy_org_factor": 0.03, "convoy_escort_efficiency": 0.05}, ("navy", "security")),
    "ERU_ud_air_superiority": ("Air Superiority Doctrine", "The best squadrons fight where they can choose their terms.",
                               {"air_superiority_efficiency": 0.05, "air_ace_generation_chance_factor": 0.1}, ("air", "medal")),
    "ERU_ud_battery_umbrella": ("The Battery Umbrella", "Fight under the railguns' umbrella while Erusea holds the battery.",
                                {"static_anti_air_damage_factor": 0.1, "air_superiority_efficiency": 0.03}, ("missile", "air")),
    "ERU_ud_capital_air_defence": ("Air Defence of the Capital", "The sky over the capital will be defended to the last squadron.",
                                   {"static_anti_air_damage_factor": 0.05, "stability_factor": 0.02}, ("air", "security")),
    "ERU_ud_megalith_directorate_idea": ("The Megalith Directorate", "A directorate answers for Megalith's engineers, budget and secrets.",
                                    {"special_project_speed_factor": 0.1, "research_speed_factor": 0.02}, ("meteor", "command")),
    # Occupation and postwar
    "ERU_ud_military_administration_idea": ("Military Administration", "Occupied districts are governed by officers under martial law.",
                                       {"compliance_growth_on_our_occupied_states": 0.05, "resistance_growth_on_our_occupied_states": 0.05},
                                       ("security", "command")),
    "ERU_ud_civil_commissioners_idea": ("Civil Commissioners", "Civilian commissioners govern occupied districts, with the army in support.",
                                   {"compliance_growth_on_our_occupied_states": 0.1, "required_garrison_factor": 0.05}, ("civil", "scales")),
    "ERU_ud_oversight_cooperation": ("Cooperation with the Commission", "The provisional government asks to be judged by its record.",
                                     {"stability_factor": 0.03, "political_power_gain": -0.05}, ("peace", "assembly")),
    "ERU_ud_provisional_order": ("A Provisional Order", "The provisional government functions under supervision.",
                                 {"stability_factor": 0.05, "production_speed_buildings_factor": 0.05}, ("assembly", "peace")),
    "ERU_ud_magnanimous_peace_idea": ("A Magnanimous Peace", "No reparations, early withdrawal and help with reconstruction.",
                                 {"stability_factor": 0.05, "war_support_factor": -0.05}, ("peace", "rebuild")),
    "ERU_ud_hard_peace_idea": ("A Hard Peace", "Guarantees, garrisons and payment for the decade Erusea suffered.",
                          {"war_support_factor": 0.05, "stability_factor": -0.03, "political_power_gain": 0.05}, ("scales", "security")),
    "ERU_ud_line_manned": ("The Line Manned", "The army stays on the armistice line at full strength.",
                           {"army_core_defence_factor": 0.05, "consumer_goods_factor": 0.02}, ("security", "gate")),
    "ERU_ud_line_thinned": ("The Line Thinned", "A screen on the line, and the reservists home to rebuild.",
                            {"production_speed_buildings_factor": 0.05, "army_core_defence_factor": -0.03}, ("rebuild", "civil")),
}

# ================================================================ OFFICE LEADERS AND REGIMES
# Unnamed offices for the provisional governments (seams.office_character). Popularities are placeholders.
OFFICES = {
    "constitutional_cabinet": ("The Constitutional Cabinet", "liberalism",
                               "A cabinet responsible to the elected assembly under a written charter. No individual officeholder is established in the mod chronology; the office represents the government. Provisional gameplay."),
    "general_staff_regency": ("The General Staff Regency", "stratocracy_fascism",
                              "A council of serving officers governing in the Crown's name as a command administration. No individual officeholder is established in the mod chronology; the office represents the government. Provisional gameplay."),
    "crown_council": ("The Restored Crown Council", "constitutional_monarchy",
                      "The Crown's council, restored when the regency returned the seals of office. No individual officeholder is established in the mod chronology; the office represents the government. Provisional gameplay."),
}
REGIMES = {
    # regime slug: (ruling party, office slug, elections allowed, placeholder popularities)
    "constitution": ("democratic", "constitutional_cabinet", True,
                     {"democratic": 45, "monarchism": 35, "fascism": 12, "neutrality": 6, "communism": 2}),
    "regency": ("fascism", "general_staff_regency", False,
                {"fascism": 50, "monarchism": 30, "neutrality": 12, "democratic": 6, "communism": 2}),
    "restoration": ("monarchism", "crown_council", False,
                    {"monarchism": 55, "fascism": 25, "neutrality": 10, "democratic": 8, "communism": 2}),
}
