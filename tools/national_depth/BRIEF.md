# National depth: writer brief for one country's bespoke tree

You are writing one country's national focus tree as a Python spec module. The
compiler (`tools/national_depth`) turns it into the mod's tree, ideas, events,
office leaders, localisation and icons. Your spec is the only file you write.

## Where the spec lives

- **Usean country:** main's Usea Depth generators (`tools/usea_depth/*/build.py`)
  already own every Usean tree (`ac_ud_minor_<tag>.txt`, `CHO_ud_*` and so on).
  Their era top-ups wait for attach mode, which adds a marker block of shared
  focuses to the owner's tree. `package.py` refuses to overwrite a file another
  generator owns.
- **Any other country:** `tools/world_depth/<tag>/content.py`, with
  `Country(..., root='world', package='<tag lowercase>', max_columns=35)`.

Start the module with `from spec import *`. Define `COUNTRY`, `SOURCES`,
`BRANCHES`, `IDEAS`, `EVENTS`, `OFFICES`, `DECISIONS`, `SCHEMA = 2` and `ERAS`; the constructors are documented in
`tools/national_depth/spec.py`. Keys are snake_case slugs, and the compiler
adds the country prefix.

## Schema 2: write to the national-campaign era targets (all new specs)

New specs set `SCHEMA = 2` and `ERAS`, for example `ERAS = ('e1',)`. The eras are:

| Era | Years |
| --- | --- |
| `e1` | 1991–2005 |
| `e2` | 2006–2020 |
| `e3` | 2021–2040 |

The size comes from main's programme (`docs/WORLD_CAMPAIGNS_2040.md`):
- **Focuses per era.** For each era you claim, the focuses opening in it must
  cover the target in `tools/world_campaigns/manifest.json`, less what other
  owners already delivered. The targets are principal 240, regional 120, and
  other or emergent 80.
- **Branches.** At least one per 12 focuses (minimum 6), and every branch's
  `era` falls inside a claimed era.
- **Decisions.** 4–8 per claimed era, in `DECISIONS`.
  - A `DecisionDef` gives a title, a short description, a political-power cost,
    its effects and optional `requires`.
  - `cooldown` is the number of days before it can be taken again; 0 means once
    only.
  - A decision may not change the government, and a repeatable one may not
    build.
- **Event chains.** At least one event option fires a follow-up event
  (`Event(key, days)`).
- **Reachability.** Every event must be fired by a focus, a decision or a
  reachable event's option.
- **Official sources.** An `Official` event or source row must cite an exact
  Chronicle key from `tools/lore/chronicle.json`, such as `1995 / 12.31`.
  Content in 2021–2040 is provisional gameplay unless such a row exists.
- **Campaign hooks.** Use `HasGlobal(flag)` and `NotGlobal(flag)` to react to
  outcomes the mod already records:
  - Belkan War: `belka_won_belkan_war`, `belka_lost_belkan_war`,
    `ose_lost_belkan_war`;
  - Stonehenge: `ac_ucw_stonehenge_seized`, `_destroyed`, `_recaptured`;
  - Emmeria–Estovakia War: `ac_eew_outcome_emmerian_victory`;
  - campaign stages: `ac_*_stage_*`.

  The build refuses any global flag that no mod script sets.
- **Buildings.** Every `Build` must fit its state:
  - shared slots come from the state category, less the buildings already
    there;
  - infrastructure is capped at 5, air bases at 10 and radar at 6;
  - a `dockyard` goes only in a coastal state.

  Mutually exclusive alternatives count once.

Schema 1 (the Perbla pilot) keeps the old flat rule: 120 own focuses, 10
branches and open work after 2002.

## What "bespoke" means here (the build fails otherwise: `lint.py`)

**Size and shape**
- At least **120 of the country's own focuses**, in at least **10 branches**.
  The tree also imports 36 shared institutional focuses; don't write those.
- At least **20%** of focuses sit in mutually exclusive groups: political
  paths, economic models, doctrines, foreign alignments.
- No branch shape (prerequisite pattern and costs) repeats more than twice.
- No branch ends in the 6-node register / policy A / policy B / operations /
  review / settlement pattern.

**Rewards**
- Every focus has a reward.
- No identical reward appears more than 3 times.
- At most 10% of focuses grant only bare currency (political power, stability,
  war support, experience).
- At least **60%** touch something the spec itself defines: an idea, flag,
  event, regime or building.
- Every flag you set is read by a later focus (`HasFlag`/`NotFlag`), and every
  flag you read is set.

**Text**
- Every title is unique in the tree, and must not reuse an existing mod focus
  title.
- Every description is at least **45 words**: what the focus does in this
  country, why, and what it costs.
- Descriptions must not reuse 5-word runs from each other or from other
  countries (0.3 similarity limit).

**Time**
- Branch `era` years spread from 1991 to 2020, so a playthrough has work in
  every decade.
- Some non-exclusive focuses must open in 2002 or later.

## Content rules (reviewed; see `docs/CANON_POLICY.md` and `AGENTS.md`)

**Read the country first:**
- its history file `mod/2985041246/history/countries/<TAG> - *.txt`;
- its 1991 states;
- its row in `tools/world_foundation/country_registry.json`;
- any localisation that names it;
- any ledger rows about it (grep `docs/` for the tag and the country's name).

**What you may and may not claim:**
- Official ACE COMBAT facts appear only where a source exists, cited in
  `SOURCES` with the exact Chronicle row. For most minors there are none:
  label everything `Provisional gameplay`.
- **Never** name new real people. Leadership is collective and unnamed
  (councils, directorates, ministries) and appears only through `Office` plus
  a `Regime` reward. Those focuses get AI weight 0 automatically.
- **Never** move borders or cores, declare war, annex, change factions or name
  new places. Buildings target only the capital (`state=0`) or the country's
  own 1991 states.
- Ground the tree in what the files say: terrain and states, government type,
  neighbours, the 1991 starting economy, the country's region and the known
  regional crises. Usea, for example, has the 1995 Skully Islands rebels, the
  1996 Ulysses announcement, the 1997 coup, Stonehenge in 1998, the 1999
  impact and the 2003–2005 war. Present these as pressures on this country.
  Never assert an outcome the Chronicle does not give.

**How to write it:**
- Write like the existing waves: plain, concrete, specific to the place.
  Focuses state real trade-offs. No filler such as "Industrial Effort 3".
- Events: each branch's opening event, or a political turn, gets an
  `EventDef` of at least 3 paragraphs and 180 words, with 2–3 options.
- ASCII only, and no double quotes in text.

## Vocabulary

**Rewards:** `Idea`, `SwapIdea`, `RemoveIdea`, `TimedIdea`, `Build(kind,
level, state)`, `Research(category, bonus, uses)`, `PP`, `Stability`,
`WarSupport`, `XP(kind, amount)`, `Event(key, days)`, `Flag(name)`,
`Regime(office)` and `Tooltip(text)`.

**Requirements:** `HasFlag`, `NotFlag`, `HasGlobal`, `NotGlobal`,
`Completed(focus)` and `After(date)`.

**Decisions:** `DecisionDef(key, title, desc, cost, effects, requires=(),
cooldown=0, ai=1)`.

**Allowed values** (`tools/national_depth/catalogue.py`):

| Kind | Allowed |
| --- | --- |
| Buildings | `industrial_complex`, `arms_factory`, `infrastructure`, `air_base`, `radar_station`, `dockyard` (coastal states) |
| Technology categories | as listed in `TECH_CATEGORIES` |
| Idea modifiers | listed in `MODIFIERS`, each with a maximum magnitude |
| Search filters | listed in `FILTERS` |
| Icon subjects | listed in `seams.SUBJECTS`: industry, logistics, air, navy, carrier, submarine, assembly, ballot, science, radar, diplomacy, economy, civil, rebuild, communications, training, command, meteor, missile, gate, refugees, medical, shelter, rail, tools, telescope, satellite, document, scales, peace, fishing, runway, bridge, medal, security |

Give every focus an `icon=(primary, secondary)` pair. The same pair can be used
at most 6 times in a tree.

**Parties and sub-ideologies:**

| Party | Sub-ideologies |
| --- | --- |
| democratic | conservatism, liberalism, social_democracy, centrism |
| communism | socialism, democratic_socialism, conservative_socialism, liberal_socialism, authoritarian_socialism, religious_socialism |
| fascism | fascism_ideology, ultranationalism, ethnonationalism, nativism, religious_nationalism, stratocracy_fascism |
| neutrality | conservatism_na, centrism_na, despotism, oligarchism, stratocracy |
| monarchism | absolutism, constitutional_monarchy |

## Check your work

From the repository root, run with the pinned Pillow environment:

```text
python -B tools/national_depth/package.py --only <TAG> --check
```

The first run reports the files as stale. That is expected: the lead writes
them. Lint and validation errors appear before that message.

For a quick lint-only loop:

```text
python -B -c "import sys; sys.path.insert(0,'tools/national_depth'); import package, lint, compile as c; m=package.load(__import__('pathlib').Path('<spec path>')); print(lint.lint(m, package.mod_focus_texts())); c.compile_country(m)"
```
