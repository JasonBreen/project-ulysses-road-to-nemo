"""Shared data model and reward vocabulary for the Usea Depth minor states A package.

Each state module (cho.py, pla.py, fru.py, alr.py, dor.py, sca.py, bld.py) declares
its own tree, national spirits, office governments, flags and long-form events with
the helpers below. build.py compiles them; build_art.py draws their icons.

Source layers: no official source covers any of these seven states. Their
geography, names and starting ideas are mod provenance (history/countries and
history/states); everything authored here is provisional gameplay. Only the
Chronicle anchors listed in ERAS are official, and they are used as dates only.
"""
from dataclasses import dataclass, field
import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MOD = ROOT / "mod/2985041246"
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from usea_depth import seams  # noqa: E402

PACKAGE = "minors_a"
NAMESPACE = "ac_ud_mina"
TAGS = ("CHO", "PLA", "FRU", "ALR", "DOR", "SCA", "BLD")
# Event numbers: one hundred per state, in TAGS order.
EVENT_BASE = {tag: 100 * (index + 1) for index, tag in enumerate(TAGS)}
MAX_X = 23
WEIGHT = 45
OPENER_WORDS = 230   # branch openers and political turns run well past seams.EVENT_MIN_WORDS

# Era gates. Official anchors are used as dates only (ACES Chronicle); the
# national response that each era opens is provisional gameplay.
ERAS = {
    "early": "",
    "settled": "date > 1992.12.31",                      # provisional pacing gate
    "ulysses": "date > 1996.4.19",                       # Chronicle, 1996 / 04.20
    "coup": "date > 1997.5.29",                          # Chronicle, 1997 / 05.30
    "stonehenge": "date > 1998.6.18",                    # Chronicle, 1998 / 06.19
    "impact": "date > 1999.7.7",                         # Chronicle, 1999 / 07.08
    "refugee": "date > 2000.4.20",                       # Chronicle, 2000 / 04.21
    "war": "has_global_flag = ac_ucw_war_started",       # Chronicle, 2003 / SUMMER (read only)
    "isaf": "has_global_flag = ac_ucw_isaf_formed",      # Chronicle, 2003 / 08.22 (read only)
    "averted": "has_global_flag = ac_ucw_war_averted",   # provisional alternative (read only)
    "postwar": "OR = { has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_ucw_outcome_erusean_victory has_global_flag = ac_ucw_outcome_stalemate }",
}
ERA_ORDER = ("early", "settled", "ulysses", "coup", "stonehenge", "impact", "refugee", "war", "isaf", "averted", "postwar")
# Frame marker drawn on each icon so the era of a focus is legible at a glance.
ERA_BAND = {"early": 0, "settled": 0, "ulysses": 1, "coup": 1, "stonehenge": 1, "impact": 2, "refugee": 2,
            "war": 3, "isaf": 3, "averted": 3, "postwar": 3}

SUBJECTS = seams.SUBJECTS
PICTURES = ("nation", "politics", "crisis", "war")


@dataclass
class Focus:
    slug: str
    title: str
    desc: str
    x: int
    y: int
    icon: tuple
    req: tuple = ()          # each entry "a" or "a|b" (an OR group); entries are ANDed
    excl: tuple = ()
    cost: int = 5            # 5 (35 days) or 10 (70 days, a major commitment)
    era: str = "early"
    avail: str = ""          # extra available trigger
    reward: str = ""         # completion effects, written with the helpers below
    event: str = ""          # event slug fired on completion
    regime: str = ""         # government slug applied on completion (player only)
    ai: int = 5


@dataclass
class Idea:
    slug: str
    title: str
    desc: str
    modifier: str
    icon: tuple


@dataclass
class Government:
    slug: str
    title: str               # office leader name, e.g. "Garrison Council"
    desc: str
    party: str
    sub: str
    elections: bool
    popularities: dict
    icon: str                # glyph subject for the generated office card


@dataclass
class Event:
    slug: str
    title: str
    paragraphs: list
    citation: str
    options: list            # [(text, effects), ...]
    picture: str = "nation"
    layer: str = "Provisional gameplay"


@dataclass
class State:
    tag: str
    name: str
    tree_title: str
    tree_desc: str
    root: str
    owned_states: tuple
    focuses: list
    ideas: list
    governments: list
    events: list
    flags: dict = field(default_factory=dict)      # slug -> readable label
    tooltips: dict = field(default_factory=dict)   # slug -> custom effect tooltip text
    country_names: dict = field(default_factory=dict)  # ideology -> name for missing name keys
    accent: tuple = (93, 208, 223, 255)
    frame: tuple = ()
    ledger: list = field(default_factory=list)     # extra MINORS_A.md rows: (claim, layer, citation, ids, status)


def fid(tag, slug):
    return "%s_ud_%s" % (tag, slug)


def tree_id(tag):
    return "ac_ud_%s_tree" % tag.lower()


def regime_name(tag, slug):
    return "ac_ud_%s_regime_%s_%s" % (PACKAGE, tag.lower(), slug)


def office_id(tag, slug):
    return "%s_ud_%s_office" % (tag, slug)


def idea_id(tag, slug):
    """Spirits carry a suffix so they never share an ID or localisation key with a focus."""
    return "%s_ud_%s_spirit" % (tag, slug)


def idea_picture(tag, slug):
    return "ac_ud_%s_%s" % (tag.lower(), slug)


# ---------------------------------------------------------------- rewards
# Every helper returns script text; a reward is the concatenation of helpers.
# The tag argument is bound per state by Rewards(tag).

class Rewards:
    def __init__(self, tag, owned):
        self.tag = tag
        self.owned = tuple(owned)

    def cap(self, amount):
        """Institutional capacity through the public ac_pol owner API."""
        return "ac_pol_initialize = yes\nset_temp_variable = { ac_pol_capacity_delta = %d }\nac_pol_change_capacity = yes\n" % amount

    def idea(self, slug):
        return "add_ideas = %s\n" % idea_id(self.tag, slug)

    def swap(self, old, new):
        return "if = { limit = { has_idea = %s } remove_ideas = %s }\nadd_ideas = %s\n" % (idea_id(self.tag, old), idea_id(self.tag, old), idea_id(self.tag, new))

    def drop(self, slug):
        return "if = { limit = { has_idea = %s } remove_ideas = %s }\n" % (idea_id(self.tag, slug), idea_id(self.tag, slug))

    def drop_inherited(self, ident):
        """Retire an inherited archive spirit (mod provenance) that this tree resolves."""
        return "if = { limit = { has_idea = %s } remove_ideas = %s }\n" % (ident, ident)

    def timed(self, slug, days):
        return "add_timed_idea = { idea = %s days = %d }\n" % (idea_id(self.tag, slug), days)

    def flag(self, slug):
        return "set_country_flag = %s\n" % fid(self.tag, slug)

    def stab(self, value):
        return "add_stability = %s\n" % _num(value)

    def ws(self, value):
        return "add_war_support = %s\n" % _num(value)

    def pp(self, value):
        return "add_political_power = %d\n" % value

    def exp(self, kind, value):
        if kind not in ("army", "air", "navy"):
            raise ValueError("Unknown experience " + kind)
        return "%s_experience = %d\n" % (kind, value)

    def manpower(self, value):
        return "add_manpower = %d\n" % value

    def tech(self, focus_slug, category, bonus=0.5, uses=1):
        if category not in TECH_CATEGORIES:
            raise ValueError("Unchecked technology category " + category)
        return "add_tech_bonus = { name = %s bonus = %s uses = %d category = %s }\n" % (fid(self.tag, focus_slug), _num(bonus), uses, category)

    def build(self, state, kind, level=1):
        if state not in self.owned:
            raise ValueError("%s does not own state %s" % (self.tag, state))
        if kind not in BUILDINGS:
            raise ValueError("Unchecked building " + kind)
        return ("if = { limit = { %d = { is_owned_by = ROOT } } %d = { add_building_construction = { type = %s level = %d instant_build = yes } } }\n"
                % (state, state, kind, level))

    def resource(self, state, kind, amount):
        if state not in self.owned:
            raise ValueError("%s does not own state %s" % (self.tag, state))
        if kind not in RESOURCES:
            raise ValueError("Unknown resource " + kind)
        return ("if = { limit = { %d = { is_owned_by = ROOT } } add_resource = { type = %s amount = %d state = %d } }\n"
                % (state, kind, amount, state))

    def fund(self):
        """A programme fee, paid only when the fiscal owner is ready."""
        return "if = { limit = { ac_econ_ready = yes } ac_econ_pay_programme = yes }\n"

    def tip(self, slug):
        return "custom_effect_tooltip = %s_tt\n" % fid(self.tag, slug)


def _num(value):
    text = ("%.3f" % value).rstrip("0").rstrip(".")
    return text if text not in ("-0", "") else "0"


TECH_CATEGORIES = frozenset({
    "industry", "electronics", "construction_tech", "naval_equipment", "radar_tech", "logistics_tech",
    "infantry_weapons", "synth_resources", "excavation_tech", "engineers_tech", "train_tech", "artillery",
    "support_tech", "light_fighter", "rocketry",
})
# State-level buildings only; province buildings (radar_station, naval_base, bunker) need a province and are not offered.
BUILDINGS = frozenset({"infrastructure", "air_base", "anti_air_building", "industrial_complex",
                       "arms_factory", "dockyard", "fuel_silo"})
RESOURCES = frozenset({"oil", "aluminium", "rubber", "tungsten", "steel", "chromium"})

# Chronicle place names that must not be tied to a state by this package. The
# mod's own state and victory-point names include some of them (mod provenance);
# this package refers to those places descriptively instead.
CHRONICLE_PLACES = ("Saint Ark", "Comberth", "Istas", "Los Canas", "Comona", "Farbanti", "Ice Creek",
                    "Whiskey Corridor", "Mount Shezna", "Shezna", "Tango Line", "Megalith", "Skully")
# Inherited real-world placeholder state names in the mod. They are avoided in
# authored text so no real-world place is presented as Strangereal geography.
# Phrases that would place or rule out Ulysses fragments on a state's soil (no
# invented impact zones or damage). Text says what people saw and what reached them.
IMPACT_GEOGRAPHY = ("fell far", "fell elsewhere", "was spared", "were spared", "been spared", "spared the", "struck the coast",
                    "hit the coast", "fragment struck", "fragments struck", "crater", "fell on the", "fell into the")
FACTORIES = ("industrial_complex", "arms_factory", "dockyard")
PLACEHOLDER_NAMES = ("Alpes", "Algiers", "Patagonia", "Northern Territory", "Gabon", "Kabul", "Manila", "French India",
                     "French Somaliland", "Nova Scotia", "Punjab", "Chihuahua", "Lipetsk", "Khorasan", "Samsun",
                     "Pennsylvania", "Muntenia", "Casablanca", "Indochina", "Balakovo", "Guerrero", "Pastaza")


def load_states():
    """Import every state module in TAGS order."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    states = []
    for tag in TAGS:
        module = importlib.import_module(tag.lower())
        states.append(module.STATE)
    return states


def requirement_groups(focus):
    return [entry.split("|") for entry in focus.req]


WORD = re.compile(r"[A-Za-z']+")
