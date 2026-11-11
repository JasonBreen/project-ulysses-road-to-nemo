"""The bespoke country spec: plain data a writer fills in, one module per country.

A spec module defines COUNTRY, BRANCHES, IDEAS, EVENTS, OFFICES and SOURCES using
the constructors below; DECISIONS is optional. A spec that sets SCHEMA = 2 is
written to main's national-campaign era targets: it also sets ERAS (for example
('e1',)) and is linted against tools/world_campaigns/manifest.json. Keys are short snake_case slugs; the compiler adds the
country prefix (<TAG>_ud_ for Usea Depth, <TAG>_wd_ for World Depth). Rewards and
requirements are drawn only from this catalogue, so every effect the compiler
writes is one it knows how to check.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Country:
    tag: str
    name: str
    root: str                      # 'usea' or 'world'
    package: str                   # usea_depth package (minors_a, ...) or the tag for world_depth
    themes: tuple = ('assembly', 'document', 'industry')   # three glyph subjects for the national pictures
    max_columns: int = 23          # Usean minors keep x <= 23; others may use up to 35


@dataclass(frozen=True)
class Source:
    layer: str                     # 'Official', 'Mod provenance' or 'Provisional gameplay'
    note: str
    citation: str = ''


@dataclass(frozen=True)
class Focus:
    key: str
    title: str
    desc: str
    icon: tuple = ('document', 'assembly')     # (primary, secondary) glyph subjects
    after: tuple = ()              # every listed focus is required (AND)
    after_any: tuple = ()          # at least one is required (OR)
    exclusive: tuple = ()          # mutually exclusive with these (made symmetric)
    cost: int = 5                  # 5, or 10 for a major commitment
    reward: tuple = ()
    requires: tuple = ()           # extra availability conditions (HasFlag, NotFlag, Completed, After)
    ai: int = 1                    # AI weight; regime focuses are forced to 0


@dataclass(frozen=True)
class Branch:
    key: str
    title: str
    era: int = 1991                # earliest year any focus in the branch is available
    filter: str = 'FOCUS_FILTER_POLITICAL'
    focuses: tuple = ()


@dataclass(frozen=True)
class IdeaDef:
    key: str
    title: str
    desc: str
    modifiers: dict = field(default_factory=dict)
    icon: tuple = ('document', 'assembly')


@dataclass(frozen=True)
class Option:
    title: str
    effects: tuple = ()
    ai: int = 1


@dataclass(frozen=True)
class EventDef:
    key: str
    title: str
    paragraphs: tuple              # at least three paragraphs and 180 words in all
    options: tuple
    layer: str = 'Provisional gameplay'
    citation: str = ''
    picture: int = 0               # one of the country's three national pictures


@dataclass(frozen=True)
class DecisionDef:
    key: str
    title: str
    desc: str                      # one or two sentences: what the decision does and costs
    cost: int = 50                 # political power, 0-150
    effects: tuple = ()            # the same rewards a focus may grant
    requires: tuple = ()           # availability conditions, as for a focus
    cooldown: int = 0              # days before it can be taken again; 0 means once only
    ai: int = 1


@dataclass(frozen=True)
class Office:
    key: str
    title: str
    desc: str
    party: str                     # ruling party: democratic, communism, fascism, neutrality, monarchism
    ideology: str                  # a sub-ideology of that party
    elections: bool = False


# --- rewards ---------------------------------------------------------------------------------
@dataclass(frozen=True)
class Idea:
    key: str


@dataclass(frozen=True)
class SwapIdea:
    old: str
    new: str


@dataclass(frozen=True)
class RemoveIdea:
    key: str


@dataclass(frozen=True)
class TimedIdea:
    key: str
    days: int = 365


@dataclass(frozen=True)
class Build:
    kind: str                      # a catalogue building type
    level: int = 1
    state: int = 0                 # 0: the capital; otherwise one of the country's own 1991 states


@dataclass(frozen=True)
class Research:
    category: str                  # a catalogue technology category
    bonus: float = 0.5
    uses: int = 1


@dataclass(frozen=True)
class PP:
    amount: int


@dataclass(frozen=True)
class Stability:
    amount: float


@dataclass(frozen=True)
class WarSupport:
    amount: float


@dataclass(frozen=True)
class XP:
    kind: str                      # army, air or navy
    amount: int


@dataclass(frozen=True)
class Event:
    key: str
    days: int = 1


@dataclass(frozen=True)
class Flag:
    name: str                      # every flag a spec sets must be read somewhere in the spec


@dataclass(frozen=True)
class Regime:
    office: str                    # an Office key; the government change runs only through its regime effect


@dataclass(frozen=True)
class Tooltip:
    text: str                      # a sentence shown in the reward tooltip


# --- requirements ------------------------------------------------------------------------------
@dataclass(frozen=True)
class HasFlag:
    name: str


@dataclass(frozen=True)
class NotFlag:
    name: str


@dataclass(frozen=True)
class HasGlobal:
    name: str                      # a global flag something in the mod already sets (checked at compile time)


@dataclass(frozen=True)
class NotGlobal:
    name: str


@dataclass(frozen=True)
class Completed:
    focus: str                     # a focus key in this spec


@dataclass(frozen=True)
class After:
    date: str                      # 'YYYY.M.D'; the focus is available only after this date


CURRENCY = (PP, Stability, WarSupport, XP)
DEFINED = (Idea, SwapIdea, RemoveIdea, TimedIdea, Event, Flag, Regime, Build)
