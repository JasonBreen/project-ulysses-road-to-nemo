# Strangereal overhaul: 1991–2020

This is the user-approved implementation roadmap, recorded against the approval baseline
`1f04456750b6e17a900cbfa407fddc3a4e96f3d5` and integrated with main `3810d1a`. It is a delivery contract, **not a
claim that its content or systems are implemented**. Package 0 is source-ready for review, with native acceptance pending;
Packages 1–5 and their new gameplay, art and native acceptance are pending.
The machine-readable counterpart is
[release_plan.json](../tools/overhaul/release_plan.json). Check its budgets with
`python -B tools/overhaul/check_release_plan.py`.

The overhaul takes breadth and dramatic national choices from TFR and systemic
depth from TNO as design inspiration. It does not import their lore, artwork,
code or economics wholesale. Retain Ulysses' national identities and original
material, with navy/cyan briefing presentation and original artwork without
added watermarks. Official chronology, user-authored fiction, inherited mod
provenance and provisional gameplay remain separately labeled.

## Delivery packages and focus budgets

| Package | Horizon | Deliverable | Status |
| --- | --- | --- | --- |
| 0 | Current candidate | Privacy cleanup; Steam screenshot/interface repairs; this roadmap and verification evidence | Source-ready; native pending |
| 1 | 1991–2005 | World foundations, country institutions, monthly macroeconomics, regional framework and anti-vanilla audit | Pending |
| 2 | 1991–2005 | Four Usean partners and six independent global squadron stories | Pending |
| 3 | 2006–2013 | Reconstruction, internal fracture, Circum-Pacific routes and supporting-country campaigns | Pending |
| 4 | 2014–2016 | Anea's military crisis and consequences, preserving previous policies and aid outcomes | Pending |
| 5 | 2017–2020 | Renewed Usea, Aurelia/Leasath and the remaining 2020 technology/campaign coverage | Pending |

Packages are reviewable releases, not permission to skip previous acceptance.
Package 0 removes unintended personal-name references from active instructions
and documentation while retaining technical identifiers, unrelated names and
the supplied creative outline. Preserve `source/archive-original` and
`source/baseline`. Its UI work must be assessed against the reported screenshots,
not inferred from a successful source audit.

| Country | Definitions at approval | Planned total | Budgeted additions |
| --- | ---: | ---: | ---: |
| San Salvacion | 0 | 72 | 72 |
| Amber | 0 | 60 | 60 |
| Ugellas | 0 | 48 | 48 |
| Delarus | 0 | 48 | 48 |
| Osea | 58 | 150 | 92 |
| Yuktobania | 30 | 120 | 90 |
| Erusea | 54 | 144 | 90 |
| Central Usea | 54 | 108 | 54 |
| Emmeria | 54 | 108 | 54 |
| Estovakia | 54 | 120 | 66 |
| North Point | 30 | 48 | 18 |
| Recta | 24 | 42 | 18 |
| Sapin | 102 | 114 | 12 |
| Gebet | 73 | 85 | 12 |
| FATO | 0 | 54 | 54 |
| South Belka | 0 | 42 | 42 |
| Nordennavic | 0 | 42 | 42 |
| Aurelia | 0 | 84 | 84 |
| Leasath | 0 | 72 | 72 |
| **Budgeted countries** | **533** | **1,561** | **1,028** |

Counts include existing shared imports and mutually exclusive alternatives;
they do not establish engine reachability or a single-run completion count.
The **36-focus regional framework is separate** from the 1,028 country additions.
PR #31 subsequently delivered six FCU focuses. They count against the FCU
budget: six delivered, 1,022 national additions remaining across this program.
The historical approval baseline is retained rather than counting those six twice.
Belka and Ustio retain their already large campaigns and gain cohesion, decisions
and narrative consequences without a new fixed focus quota; AWWNB's emergent
entry remains intact. Never pad a budget with interchangeable factory or
political-power rewards. Use 35-day focuses by default and 70-day major
commitments, with evergreen domestic branches and continuing decisions between
dated milestones.

The first country expansion is SNS/AMB/UGE/DEL: **228 new focuses**, starting
foundations and four distinct national institution/decision systems. Extend the
existing Continental War generator and owner effects. Do not duplicate its
war, ISAF, Stonehenge or settlement flags. All 69 country histories require a
profile and declared support status, distinguishing active countries, emergent
countries and unresolved geography; this does not promise identical bespoke
campaigns for all 69. Industry, logistics, valid capitals, deployable forces,
DLC equipment, production, AI and effective localization are foundation work.
Territory, cores and province geometry require reviewed sources before changes.

## Independent squadron stories

| Host | Original story | Role and central conflict |
| --- | --- | --- |
| BLK | Cold Orders | Reserve interception; credible orders and crew survival |
| UST | Last Road Home | Fighter/close support; evacuation protection and sovereignty |
| ERU | The Narrow Sea | Maritime reconnaissance/strike; duty and civilian costs |
| SNS | Empty Frequency | Air defense/warning networks; withdrawal and continuity |
| EMM | The Open Corridor | Airspace patrol/relief escort; conditions and sustained burden |
| EVA | The Last Serviceable Aircraft | Local reconnaissance/airfield defense; maintenance and distribution |

Each has **20 core chapters, at least 12 choice chapters, at least three endings
and four core original characters**: 120 initial core chapters and 24 core cast
members across three theaters. The initial art package contains **24 portraits,
48 illustrations and six loading screens**. Later independent Osean,
Yuktobanian, Aurelian and Leasathian stories each receive 20 core chapters.
These are pending authoring targets, not delivered events or assets.

Stories have separate casts, choices, state and conclusions. Cameos require
primary sources establishing their timing and presence; they do not replace
the original casts or invent biographies for canon characters. Existing
national war/project/aid effects own outcomes. Story choices change a unit's
conditions and bounded national consequences, not canonical victories by fiat.
Support annexation, capitulation, subject status, disbandment and alternate
settlements. Never revive a concluded cast or require another story's completion.
Match deployed squadron roles to actual equipment, bases and DLC variants.

## Shared economic and campaign contracts

Full v2 macroeconomics is the **new-campaign default**, with simplified/disabled
campaign routes retained. It uses fictional gameplay accounting, not official
GDP statistics: state-based real output starts from physical 1991 capacity,
the price index starts at 100, and nominal output is real output × price / 100.
GDP growth does not spawn factories. A single idempotent monthly owner settles
the economy; UI queries only quote results. Stocks, current policy, forecast,
settled history and contracts remain distinct records. Preserve legacy v1 weekly
units and pending contracts rather than reinterpreting them as v2 balances.

- Three distinct tax bases: household income, business surplus and consumption.
- Five spending envelopes: administration, public services, education/research,
  infrastructure/development and defense operations. Debt and contract cash
  flows remain separate.
- Five pages: Overview, Budget, Industry and readiness, Debt and contracts,
  Ledger. Four presets: balanced, development, emergency relief, mobilization.
- State output is realized once for the controller with an occupation discount;
  an owner loses taxes on lost control. Treasury, debt and contracts remain
  attached to their country.
- Force upkeep uses observable manpower, aircraft and ship roles. Readiness is
  0–100 and changes gradually with funding; physical fuel, supply and replacements
  remain necessary. Initial equipment transfers are stockpile-backed.
- Recoverable crises use two failed monthly settlements, a three-month warning
  and three funded recovery months. National institutions create distinct
  continuing constraints and choices, rather than identical generic score bars.
- Stable guarded spend, receive, commitment, loan, aid, procurement, shock and
  readiness effects are the integration API. Country and story content must use
  these owners instead of writing contradictory parallel economies.

Historical AI follows the supported route when eligible; alternatives must be
earned through earlier choices and conditions. Keep existing country, tree,
focus, event and outcome IDs. Apply opening consequences once after their owning
initialization and clamping. Diplomacy rechecks both participants and handles
refusal, timeout, war, subjects, annexation and capitulation. Guard rewards and
project payouts against repetition and interruption.

New campaigns are the primary target. Old saves retain completed content and
receive only eligible future additions: no expired historical replay, starting
army/industry grants or retroactive preparation. Recovery assessments remain
available when real prerequisites finish after a calendar cutoff. Generators
and committed output change together. Use bounded scheduled work, not
uncontrolled daily global scans. Temporary civil-war tags are allowed only
after reviewed source, territorial, lifecycle and save-continuity contracts.

## Anti-vanilla, chronology and acceptance

Full anti-vanilla covers **effective player-facing** Earth/WWII names, prose,
artwork, portraits, models/materials, sound and reachable country/crisis/decision
content. Preserve necessary internal IDs, engine commands, control names,
shaders, production, combat, logistics, diplomacy, espionage and DLC interfaces.
Audit effective localization precedence and engine/mod GUI dependencies, not
only authored texture paths. Require `--strict-all`, frame/alpha/control checks,
loaded-content review and separate native screen/DLC coverage. A static GFX pass
cannot certify every reachable screen.

The [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/) supplies
reference anchors: Free Erusea in 2006; Estovakia's civil war in 2007–2013;
the Circum-Pacific War in 2010; the Emmeria–Estovakia War in 2015–2016;
the Lighthouse War in 2019; and the Aurelia–Leasath conflict in 2020. Unknown
days in the 2020 entries remain unknown in the ledger. These references never
force an outcome over valid prior alternatives. New borders, precise provincial
mapping, political terms, force rosters, cameo locations and authored branches
need their own source or explicit provisional-gameplay classification.

The authored release target ends in **2020**. The existing engine permission
through 2065 is retained without inventing post-2020 history. Add a sourced
2006–2020 equipment/technology program; the current engineering end date does
not supply one. Each package closes its own campaign horizon before claiming
the next, with save/reload checks at 2005, 2010, 2016 and 2020 transitions.

Run existing campaign, economy, faction, aftermath, Continental War,
supporting-country, project, briefing, typography and asset checks, plus new
system/country/story and generation regressions. Verify invalid partners,
duplicate effects, interrupted projects, historical/earned alternate routes,
late saves and fiscal-disabled play. Keep source/static, actual-script offline,
shortcut native and natural native evidence distinct.

**Native testing remains paused.** Final candidate acceptance requires an exact
isolated payload on the verified installed HOI4 1.19.4.1 build, the three display
configurations (3440×1440 at 1.0, 1920×1080 at 1.0, 2560×1440 at 1.25), and the
appropriate DLC/fallback and natural-progression cases. Normal installations,
profiles and user saves remain untouched. PRs, merges, publication and
installation synchronization remain separate delivery actions.
