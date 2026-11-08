"""Data records for the minors B package. State modules in states/ build these.

Every state module defines, at module level:

    TAG, NAME, ADJ           tag, country name and adjective used in text
    ACCENT                   RGBA accent colour for the generated art
    SILHOUETTE               icon frame polygon on a 192 px canvas
    TREE_TITLE, TREE_DESC    focus tree name and description
    IDEAS                    list of I(...)
    REGIMES                  list of R(...)  (two or three political paths)
    FOCUSES                  list of F(...)
    EVENTS                   list of E(...)  (numbered in list order)
    DECISIONS                list of D(...)  (state programmes; the adopt decision is generated)
    FLAGS                    {name: readable label} for every <TAG>_ud_<name> flag set or read
    LEDGER                   list of L(...)  rows for docs/usea_depth/MINORS_B.md

Reward and effect strings use the small vocabulary expanded by build.py:

    idea:<slug>                      add_ideas = <TAG>_ud_<slug>
    swap:<old>:<new>                 swap one of our ideas for another
    remove:<slug>                    remove_ideas = <TAG>_ud_<slug>
    timed:<slug>:<days>              add_timed_idea
    cap:<n>                          institution capacity through ac_pol_change_capacity
    pp:<n> stab:<f> ws:<f>           political power, stability, war support
    xp:<army|navy|air>:<n>           experience
    tech:<category>:<bonus>          one-use research bonus named after the focus
    build:<state>:<building>:<n>     instant construction in an owned and controlled state
    build_capital:<building>:<n>     the same in the capital state (used by Shilage)
    slots:<state>:<n>                extra shared building slots in an owned state
    resource:<state>:<res>:<n>       extra resource output in an owned state
    flag:<name>                      set_country_flag = <TAG>_ud_<name>
    pop:<ideology>:<f>               add_popularity (placeholder seeding only)
    manpower:<n>                     add_manpower
    convoys:<n>                      add convoys to the stockpile
    event:<slug>                     fire one of this state's events next day
    regime:<slug>                    ac_ud_minors_b_regime_<tag>_<slug> (AI weight forced to 0)
    raw:<script>                     verbatim script (reviewed: must pass the package guards)

Eras gate focuses by calendar or by flags read (never written) from the
Continental War owner:

    open        no gate (1991 onward)
    ulysses     from 1996.4.20, the Ulysses announcement
    coup        from 1997.5.30, the Usea-wide coup
    stonehenge  from 1998.6.19, Stonehenge completed
    impact      from 1999.7.8, the impact
    closure     from 2000.4.21, the Erusean refugee closure
    late        from 2003.6.21, the provisional war window
    war         ac_ucw_war_started is set (2003 onward)
    isaf        ac_ucw_isaf_formed is set
    averted     ac_ucw_war_averted is set (provisional alternative)
    postwar     any Continental War outcome or the averted accord
"""
from dataclasses import dataclass, field
from typing import Tuple

ERAS = {
    "open": None,
    "ulysses": "date > 1996.4.19",
    "coup": "date > 1997.5.29",
    "stonehenge": "date > 1998.6.18",
    "impact": "date > 1999.7.7",
    "closure": "date > 2000.4.20",
    "late": "date > 2003.6.20",
    "war": "has_global_flag = ac_ucw_war_started",
    "isaf": "has_global_flag = ac_ucw_isaf_formed",
    "averted": "has_global_flag = ac_ucw_war_averted",
    "postwar": "OR = { has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_ucw_outcome_erusean_victory has_global_flag = ac_ucw_outcome_stalemate has_global_flag = ac_ucw_war_averted }",
}

# Era bands used for the icon frame decoration and the ledger.
BANDS = {
    "open": "rebuilding", "ulysses": "preparation", "coup": "preparation", "stonehenge": "preparation",
    "impact": "relief", "closure": "relief", "late": "war", "war": "war", "isaf": "war", "averted": "war", "postwar": "war",
}


@dataclass
class F:
    """One focus. parents: each item is a slug (its own prerequisite block, ANDed)
    or a tuple of slugs (one block, any of them)."""
    slug: str
    title: str
    x: int
    y: int
    subjects: Tuple[str, str]
    desc: str
    parents: tuple = ()
    excludes: tuple = ()
    cost: int = 5
    era: str = "open"
    reward: tuple = ()
    ai: int = 1
    event: str = ""
    regime: str = ""
    available: str = ""
    bypass: str = ""


@dataclass
class O:
    name: str
    effects: tuple = ()
    ai: int = 1
    trigger: str = ""


@dataclass
class E:
    """A long-form event. paragraphs are joined by seams.event_text()."""
    slug: str
    title: str
    paragraphs: tuple
    options: tuple
    picture: str = "document"
    layer: str = "Provisional gameplay"
    citation: str = ""


@dataclass
class I:
    slug: str
    title: str
    desc: str
    modifiers: dict
    subjects: Tuple[str, str] = ("document", "assembly")


@dataclass
class R:
    """A political path. slug is unique within the state."""
    slug: str
    office: str
    office_desc: str
    party: str
    ideology: str
    elections: bool
    popularities: dict
    subjects: Tuple[str, str] = ("assembly", "ballot")


@dataclass
class D:
    """A state programme decision: paid through the fiscal owner when ready."""
    slug: str
    title: str
    desc: str
    requires: str
    effects: tuple
    days_re_enable: int = 180
    pp: int = 25


@dataclass
class L:
    claim: str
    layer: str
    citation: str
    ids: str
    status: str = "Implemented; static-validated; native untested"
