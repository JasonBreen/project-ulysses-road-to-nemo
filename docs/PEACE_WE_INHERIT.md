# The Peace We Inherit

Implementation of the approved Belkan aftermath expansion, based on main
`33df8a288be02c1937612847d221224254b48ea9`. All four slices are authored in
source. Static/offline checks exercise the authored contracts. Native parsing,
rendering, reachability, AI focus selection, save serialization and balance
remain unverified. No game installation, playset or user save is changed.

## Delivered slices

| Slice | Content | Integration |
| --- | --- | --- |
| Belka | 30 focuses: six shared opening, four for each of defeat/victory/Wacht, four for each of negotiated/authoritarian/revanchist policy; cabinet choices, pressure incidents and enduring national policies | Additive imports in `ac_belkan_postwar`; existing nine focuses and their IDs remain. New focuses add no factory, border, government or reconstruction reward from the original tree. |
| Osea and Ustio | Eight focuses each; Osea has outcome-dependent guarantor/constrained roles and exclusive dialogue/containment endings; Ustio has independent/subject alternatives and contracted-expertise/security content | Imports in both Osean and all three Ustian trees. No new tree load; the Ratio and lost-Ratio transitions remain untouched. |
| Sapin and Gebet | Six focuses each; domestic war costs, demobilization, authority, industry, resources and foreign commitments | Existing political systems and trees remain. FATO, Recta and South Belka receive two-option local recovery briefs. |
| 1996–1999 | Four preparedness commitments, warning and crisis assessments, relief outcome, late-1999 record, reform/aggressor-training briefs | Calendar runs for the eight covered original tags, including during war and before a settlement. No invented impact zones, province damage, new war, or changed campaign cutoff. |

Country-specific files, effects, events, decisions, ideas, triggers and status
localization are generated from `tools/build_peace_we_inherit.py`. Keep the
authoring source and committed output together:

```powershell
py tools/build_peace_we_inherit.py
py tools/build_peace_we_inherit.py --check
py tools/Test-PeaceWeInherit.py
pwsh -NoProfile -File tools/Run-UlyssesCampaignChecks.ps1
```

The check flag never writes. Regeneration only writes the declared additive
files and inserts missing shared-focus imports into existing country trees.
Localization uses UTF-8 BOM. No art or audio assets are added; existing focus,
event and idea sprite references retain the baseline's presentation.

## Pressure and timing contract

The aftermath decision panel shows recovery, political confidence, settlement
tension and preparedness. The first three are 0–100 provisional indices, not
canon statistics. They do not decay periodically. Initial Belkan values are:

| Outcome | Recovery | Confidence | Tension |
| --- | ---: | ---: | ---: |
| Defeat | 20 | 25 | 65 |
| Conventional victory | 45 | 65 | 55 |
| Wacht am Wal | 35 | 45 | 40 |
| Unclassified | 30 | 35 | 30 |
| Other covered participants | 40 | 50 | 30 |

Initialization waits for the existing global postwar contract, peace and no
capitulation. Belka additionally requires `ac_postwar_ready`, preserving the
inherited defeat sequence. The first political commitment is unavailable for
90 days after that country's actual initialization. A completed outcome review
is required; unclassified outcomes can use only negotiated domestic recovery.
Policy never replaces the leader, ideology, monarchy or constitution.

Negotiated recovery favors civilian recovery and reduces tension; authoritarian
policy concentrates administration while increasing suspicion; revanchist policy
trades recovery and cooperation for military readiness. Their permanent ideas
include countervailing costs. Final flags and ideas persist for later content.

At tension 75 or higher, or confidence below 25, one cabinet incident can be
dispatched. Expensive repeatable recovery, accounts and de-escalation decisions
remain available every 180 days. These indices never trigger a war. One-time
focus rewards, cabinet choices and decisions have script guards as well as
engine completion state. A delayed cabinet choice made during war is retained
and applied once peace returns. The weekly hook introduces no passive drift.

## Reciprocal diplomacy

Six directed offers are supported: Belka→Osea, Osea→Ustio, Belka→Gebet,
Belka→Sapin, Sapin→Osea and Sapin→Gebet. Sending costs 50 political power;
it gives no reward. Both parties must exist, have initialized aftermath content,
be independent, be at peace, and not have capitulated. The sender must have
tension below 75 and cannot follow the revanchist program.

There is one negotiation per dyad. A reply can accept or refuse; the sender can
withdraw; the offer expires after 60 days or is invalidated by changed
circumstances. The recipient rechecks eligibility at dispatch and selection.
Pending flags clear before rewards, so duplicate or stale replies cannot revive
an offer. Acceptance adds recovery/confidence to both countries, reduces their
tension, and grants a reciprocal +25 opinion modifier. It transfers no land,
money, sovereignty or automatic security guarantee.

An accord stops being active if a party disappears, becomes a subject, goes to
war or capitulates. Earlier recovery work is retained; opinion modifiers are
removed. Crisis relief checks actual partner eligibility even if the sender's
weekly cleanup has not yet run. A constrained Osea can negotiate cooperation
but cannot acquire its victorious-guarantor focus.

Independent Ustio can negotiate; a surviving subject has a domestic recovery
branch; an annexed Ustio receives no event. Belka's victory administration focus
records the inherited annexed-Ustio context without restoring a country.

## Calendar, preparation and 1999 record

The warning window opens on 20 April 1996 and closes on 8 July 1999. Country
weekly scheduling observes absolute dates within its next pulse (up to seven
days), with briefing dispatch one day later. It does not postpone world events
until a peace or focus completes. The weekly hooks are fixed to eight tags;
there are no new every-country or every-state scans.

Four one-time commitments compete for a shared 180-day capacity lock. Civil
defense adds 25 preparedness; logistics adds 20; cooperation with a live accord
adds 25; military readiness adds 10 and 10 army experience. Each costs 50
political power and imposes a temporary civilian-construction or production
efficiency penalty. Preparation is available in peace, including before a late
settlement; it closes at the crisis date. No crisis-day click can retroactively
prepare a country.

On or after 8 July 1999, relief capacity is snapshotted once: preparedness +10
for recovery at least 60, +20 for at least one functioning accord. Capacity at
least 60 gives a 180-day resilience idea; otherwise a 180-day strain idea.
Initialized aftermath countries gain/lose eight confidence respectively. No
direct physical damage is inferred for the covered countries. A December 1999
assessment records the pressures, preparedness, relief capacity, national policy
and live relationships while leaving the campaign running.

Old saves first initialized after the crisis mark it as past without receiving
retroactive preparation rewards or historical popups. Old saves first loaded
after the assessment skip that popup too. A later settlement still receives its
own 90-day opening and must perform reconstruction; calendar history never
instantly completes it. New 1991 campaigns are the primary acceptance target.

## Sources and authored branches

Primary source: [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/),
accessed 24 October 2026. The chronology entries below supply reference points;
all cabinet programs, pressure values, costs, accords and relief calculations
are provisional gameplay from the user-approved expansion plan.

| Claim | Layer and exact source | Affected content | Disposition |
| --- | --- | --- | --- |
| Lumen treaty, 20 June 1995 | Official; Chronicle, 1995 / 06.20 | Existing outcome flags; `ac_pwi_start`, Belkan outcome branches | Reference only: the inherited war's real outcome and date initialize gameplay. No forced historical treaty or borders. |
| AWWNB rebellion, December 1995 | Official; Chronicle, 1995 / 12.25 and 12.31 | `ac_pwi.74`, `ac_pwi_aww_observed`; inherited `events/AWWNB.txt` | Observe an existing AWW tag or Belkan rebellion idea. Does not dispatch another uprising or rewrite the inherited spawn, unit transfer or player choice. Its inherited reachability remains native-unverified. |
| Rald overthrow and Blauvelt air-force reform, 17 January 1996 | Official; Chronicle, 1996 / 01.17 | `ac_pwi.73`, `ac_pwi_reform_*` | Conditional historical reference brief after defeat in 1996; authored reform choice. No forced leader replacement, invented office or biography. |
| FCU announcement, 20 April 1996 | Official; Chronicle, 1996 / 04.20 | `ac_pwi.70`, preparedness decisions | Global chronology reference; the eight national responses are authored. |
| Belkan former pilots abroad as aggressor instructors, 1998 | Official; Chronicle, 1998 / 06.19 | `ac_pwi.75`, `ac_pwi_aggressors_*` | Conditional defeat-path brief in 1998; no named pilot movement or invented personal history. |
| Ulysses crosses Earth's Roche limit, 8 July 1999 | Official; Chronicle, 1999 / 07.08 | `ac_pwi.71`, crisis resolution and ideas | Calendar reference. Humanitarian capacity consequences are authored; no invented local impacts. |
| Inherited victory, Wacht, defeat, monarchy, Ratio and annexation | Mod provenance; existing campaign files at base `33df8a2` | Additive shared-focus imports; all `*_pwi_*` national branches | Preserved, not promoted to official canon. |
| All postwar programs and coefficients | Provisional gameplay; approved The Peace We Inherit plan | `common/**/ac_pwi.txt`, `events/ac_pwi.txt`, `ac_pwi_l_english.yml` | Authored and offline-tested; native reachability and balance open. |

Joker 1 chronology, new borders, a second regional war, world impact simulation,
new national campaigns for FATO/Recta/South Belka, and an AWWNB campaign redesign
remain outside this expansion. Existing issues #6 (canon), #7 (fiscal), #8
(runtime), #4 (parity), and #5 (technology/horizon) retain their scope.

## Recorded static evidence — 24 October 2026

- Aggregate campaign checks pass; campaign contract: zero errors and warnings.
- Aftermath transition suite: 21 tests pass, including nine outcome/policy routes
  and all six diplomatic dyads with five terminal results each.
- Existing campaign review/mutation, Ustio continuity, native compatibility and
  native semantic mapping regressions pass. These are offline/static checks.
- Economy: 27 tests pass. Wrapper failure propagation passes under PowerShell 7
  and Windows PowerShell; the injected child exit 17 is an expected negative test.
- Reference inventory: 666 to 724 focuses, 620 to 662 events; warnings remain
  2,011. Map structural errors remain zero; technology/horizon checks pass.
- Installed-reference asset audit against a frozen `33df8a2` mod snapshot:
  four inherited map text/config matches, zero new vanilla matches, zero
  path-independent asset matches, zero errors and zero warnings.
- No native HOI4 launch, rendered-UI, save/load, AI or balance acceptance is claimed.

## Acceptance checklist

The offline suite reads the shipped script AST and rejects unsupported commands.
It exercises nine outcome/policy combinations, neutral fallback, preserved
government state, subject/absent Ustio, all six negotiations and five terminal
results, stale replies, lost partners, calendar/settlement independence,
preparation locks, pressure bounds, fiscal on/off, deferred cabinet choices,
focus imports/coordinates, localization and regeneration parity. This is a
contract harness, not a HOI4 parser or saved-game emulator.

Before claiming playable/native acceptance, separately authorize and perform:

- Verify isolated payload/source manifests and the actual game configuration.
- Render each national tree, pressure panel, event options and inherited artwork.
- Exercise the nine Belkan routes and unclassified fallback, including monarchy.
- Exercise independent, subject and absent Ustio and its Ratio-loss safeguards.
- Exercise accepts, refusals, withdrawal, timeout and participant invalidation.
- Exercise inherited AWWNB-compatible and incompatible outcomes without a duplicate.
- Save/reload at initialization, policy commitment, pending negotiation and crisis.
- Compare preparedness and partner-loss outcomes; verify late-war calendar behavior.
- Run an AI campaign through December 1999 and inspect logs and progression.

Native tests have not been run for this expansion. Preserve the normal playset
and saves; use the approved isolated workflow for any later test.
