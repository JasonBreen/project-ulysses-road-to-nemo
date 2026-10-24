# The Peace We Inherit: native evidence, 24 October 2026

User authorization: native playtest in an isolated setup, keeping the normal
playset and saves untouched. Initial source was `6d6bcff`, PR #21. Native defects
were repaired in `195c2b6` (artwork) and `19bd5dc` (timed flags and condition text).
Full gameplay acceptance remains open. The accompanying CSV distinguishes
exercised checks from cases still requiring native coverage: **12 NATIVE_PASS,
eight NATIVE_PARTIAL and 46 NOT_RUN** across
[66 cases](NATIVE_PEACE_WE_INHERIT_20261024.csv). Partial checks include explicit
fixture, older-build, rendering, isolation and full-matrix limitations.

Final preservation audit: all **81 normal saves** (15,747,919,535 bytes) and
**eight protected configuration/launcher files** retain their original SHA-256
hashes. No normal saves were added or removed. However, the **24 normal log files
were refreshed** during the session, with startup timestamps around 14:40 local,
coincident with the windowless diagnostic launch. This is an isolation exception:
the normal log history was not preserved. It does not alter the verified save,
playset or configuration preservation result. Original log contents were not
backed up, so they cannot be restored from the metadata manifest.

## Isolation and reproducibility

The disposable root is `G:\Project-Ulysses-Native-20261024-PWI-6d6bcff`.
It contains a full physical copy of the installed engine, separate `profile/`
user data, source-matched mod payload and local `evidence/`. There are no hardlinks
or junctions to normal saves or the installed engine. Normal launcher databases,
playset, settings and installed launcher configuration are protected by manifests.
Normal saves were never loaded or copied. All native saves use the Local tab;
autosaves are disabled in the test profile.

The payload contains 2,841 files. Launch validation checks source/payload parity.
Runtime system.log confirms HOI4 Operation Postern `1.19.3.0.c01a`, Steam build
25205862, one active mod and descriptor `Project Ulysses PWI Native 6d6bcff`.
Both engine executables have SHA-256
`7DC947BE34970DA1E1C787BCDDBE7F62B610FF258AEBF8F06AA8B348F3A031D5`.
Copied userdir.txt and copied launcher gameDataPath point to the isolated profile.
The installed engine has no new userdir.txt. Checksums identify revisions: `181e`
original, `af02` artwork repair, `21db` timer repair. The descriptor retains its
session name. The isolated renderer uses 3440 by 1440; normal display settings
were not edited. Input follows the Computer Use skill's selected returned-window,
observe/action/refresh workflow.

Large saves, logs, crash dumps and the proprietary engine remain local. Fixture
recipes, save-derived JSON, preservation manifests and coverage are in evidence/.
No crash report or user data was submitted.

## Native defects repaired

**Focus artwork.** All 58 new focuses referenced an undefined political-reform
sprite and displayed question marks. The generator now selects existing
Strangereal regional, diplomacy, defense and security sprites with shine
definitions. The restarted Belkan tree displays the repaired icons in the observed
upper portion. Regressions check all 58 definitions and texture paths. Lower
Belkan branches and other national tree views remain uninspected. No vanilla
artwork or new visual asset files were introduced.

**Timed flags.** Engine saves showed that set_country_flag blocks with days but
no value serialized as value zero. The 90-day opening wait, 60-day negotiation
window and 180-day preparation capacity lock consequently tested false immediately.
All such authored flags now explicitly use value = 1. The offline model reproduces
the observed zero default, with two regressions. A fresh engine-created 23 August
1995 save records the opening flag as value 1 with 31 days remaining from 25 June
initialization. A pending offer records value 1 with 60 days and survives reload.
Readable condition text also replaces raw new flag identifiers.

## Initialization, diplomacy and continuity

| Check | Native observation | Scope |
| --- | --- | --- |
| New campaign | 1991 Belka bookmark reaches map and writes local save | Isolated profile |
| Initialization | Weekly tick initializes defeat recovery 20, confidence 25, tension 65, preparedness 0 on 25 June 1995 | Existing settlement context seeded; PWI state not seeded |
| Decision presentation | Status values, costs and three Belkan offers render | Observed Belkan panel |
| Initialization reload | Graceful shutdown/restart and UI load retain values; original Belkan save resumes on repaired source | Native continuity |
| Pending-offer reload | BLK_1995_08_27_13 retains Osean offer and 60-day window, reloads through UI and resumes normally | Source 19bd5dc |
| Refusal | Osea refuses on 28 August; pending clears without recovery rewards | Native AI reply |
| Withdrawal | Belka withdraws Gebet offer on 10 October; no reward; stale reply does not revive it | Native decision and delayed recipient |
| Acceptance | Sapin accepts on 11 October; accepted/active flags and reciprocal effects persist | Native AI reply |
| Event presentation | Localized closing correspondence, existing paper/pen artwork and localized choice appear | Withdrawal notification |

The native BLK_1995_11_03_04 save records all three terminal results and no pending
state among them. Belka has **25 recovery, 29 confidence, 57 tension**, exactly one
accepted-accord reward from 20/25/65: +5/+4/-8. Osea and Gebet retain 40/50/30 after
refusal/withdrawal. This does not substitute for testing every dyad's timeout,
invalidation and repeated dispatch cases.

## Fixture controls and crash limitation

The initializer derives from a new disposable 1991 save: current date moved to
20 June 1995; existing defeat/continuation globals, Belka ready flag and inherited
postwar tree supplied. It seeds no PWI flags, variables or new completed focuses.
It exercises weekly initialization and subsequent engine progression, without
proving a natural 1991-to-war-to-treaty handoff or intervening world history.

The old AI checkpoint LEA_1996_06_09_09 resumes on repaired source through 19 July
1996. A derivative that changes only the player from Leasath back to Belka crashes
on its first resumed hour even without an offer. A pending offer derived from that
fixture also crashes after hot/cold/debug reload. The offer is therefore not
necessary for that crash. Dumps provide no actionable mod-script attribution;
player-switch fixture reliability remains unresolved.

The original native player-controlled BLK_1995_07_24_22 resumes successfully on the
same repaired build. Its subsequent pending-offer save reloads and resumes,
followed by the three diplomatic terminal results above. Failed fixtures and logs
remain diagnostic evidence. A paused load alone is never counted as continuation.

## AI progression on the repaired build

A fresh initializer was loaded on `19bd5dc` / `21db`, with the player assigned to
existing Leasath so all expansion participants use native AI. No PWI pressure,
policy, completed focus, offer or preparedness state was supplied. On 23 April
1997, Belka had completed all six shared focuses, four defeat focuses and four
revanchist focuses, resolved its tension incident, and recorded its national
settlement. Values were recovery 55, confidence 100, tension 77, preparedness 0.
Ustio completed all seven eligible independent focuses and Sapin all six of its
focuses. Osea and Gebet were progressing through both inherited and new content.

`LEA_1997_04_23_07.hoi4` was saved, selected and reloaded through native UI, then
unpaused. The campaign advanced beyond 5 August 1997. This is continuity evidence
after political settlement, including the revanchist branch's persistent flags;
it does not establish all political branches or natural war reachability.

The earlier icon-fixed AI run reached 24 February 2000 with a negotiated Belkan
settlement. Its preparedness choices predate the timer repair, so its endurance
and relief results are retained as older-build observations, not corrected-build
acceptance of the capacity opportunity cost.

On the corrected run, the warning flag dates are 22 April 1996 and crisis
resolution dates are 12 July 1999 for all six surviving covered countries, within
the documented weekly windows. Recta and South Belka are absent in this fixture.
The 28 October 1999 native save records the following post-crisis state:

| Country | Recovery | Confidence | Tension | Preparedness | Relief capacity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Belka, revanchist settlement | 60 | 92 | 72 | 0 | 10 |
| Osea | 56 | 72 | 32 | 0 | 0 |
| Independent Ustio | 78 | 77 | 18 | 45 | 55 |
| Sapin | 71 | 74 | 13 | 0 | 10 |
| Gebet | 77 | 75 | 24 | 25 | 35 |
| FATO | 60 | 70 | 29 | 25 | 35 |

All six have the strained-relief outcome. Ustio takes civil defense on 24 October
1998 and logistics on 2 May 1999; its capacity lock saves as value 1 with one day
remaining on 28 October 1999. This confirms the repaired lock's native countdown
and serialized state. Gebet takes civil defense on 24 November 1998; FATO on
23 January 1999. No reconstruction accord is concluded in this AI run. The
experimental fiscal system is disabled (`ac_econ_ready` is absent).

AI preparedness uptake is late and insufficient in this run: all participants
miss the resilient-response threshold. This is a balance/AI follow-up, not proof
that preparedness is unreachable; the engine executes selected commitments and
the corresponding relief calculation. Corrected-build high preparedness and
cooperative relief comparisons remain open.

The post-crisis save was loaded through native UI, unpaused and continued through
20 March 2000. `LEA_2000_03_20_02.hoi4` records assessment completion and the 1999
record for all six survivors. The assessment flags are dated 6 December 1999;
Ustio's capacity lock has expired, preparedness remains 45 and relief remains 55.
The crisis does not repeat after reload. Gebet subsequently reaches 80 recovery,
81 confidence and 21 tension; FATO reaches 68/73/29 through recovery choices.
The other four countries retain the post-crisis values above. This completes a
corrected-build AI endurance run from the seeded June 1995 context through the
expansion endpoint, including policy and crisis reload/resume checkpoints.

The copied engine exited gracefully through its native menu; no hoi4.exe process
remained in the final process inventory. Final logs are preserved in
`evidence/run8-19bd5dc-valid-baseline-and-ai-logs/`. The log inventory found no
PWI identifier diagnostic lines; the broad non-PWI error inventory remains open.

## Static evidence, separate from native evidence

After both repairs Test-UlyssesStatic.ps1 passes. The aftermath suite has 24 tests;
generator parity covers 15 generated files, 58 focuses and 464 English keys;
the economy suite has 27 tests. Reference warnings remain 2,011; technology has
one warning; map has zero errors and three inherited warnings. Four CI jobs pass
on implementation head 19bd5dc.

These results do not prove engine rendering, natural reachability or the full
outcome matrix. Native logs contain substantial other-content and installed-DLC
diagnostics, including Earth-country events and Osean decision scope errors. No
no-mod control was run for causal attribution of that inventory. The runtime log
must not be described as clean.

## Outstanding gameplay acceptance

Native coverage still needs remaining Belkan outcome/policy combinations,
unclassified fallback and inherited monarchy, remaining tree views, subject/absent
Ustio and lost-Ratio transitions, compatible/incompatible inherited AWWNB conditions,
fiscal-enabled progression, every unexercised reciprocal terminal outcome,
partner invalidation before relief and unusually late natural settlements. These
cases remain explicit in the coverage CSV.
