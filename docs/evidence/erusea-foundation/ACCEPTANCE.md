# Erusean foundation — source acceptance

The local component extends world-foundation base `fb3e8c3` on the isolated
`codex/strangereal-erusea-foundation` branch. It has not been pushed or published.
The [implementation and provenance ledger](../../ERUSEA_FOUNDATION.md) describes
the roster, bounded economic additions, retained identities and every acceptance
limit. The [machine-readable results](validation.json) retain commands, logs,
source base, primary-reference version and candidate payload digests.

**All 23 completed focused check groups and the full current-PowerShell static
wrapper pass.** The [changed-script scan](pr-scan.md) finds zero errors and zero
warnings in 34 actual changed mod scripts. The initial CLI scan used the
committed HEAD before this component existed and therefore selected zero files;
the retained report instead scans the actual staged diff against `fb3e8c3`, using
the same scanner implementation. Git diff whitespace checks pass.

| Check | Observed source result |
|---|---|
|World foundation|16 regressions; 20 country/DLC combinations, including all four ERU BBA/MTG combinations |
|Primary equipment reference|Effective technology, repeated unlock blocks, modules, creator/owner, variant-before-roster order, one land/air/naval load per branch; installed launcher metadata `rawVersion=1.19.4.1`, read-only |
|Original four starts|Profiles and manifest rows exact; individual generated files exact; country-history AST exact except the explicitly validated foreign macro-eligibility marker |
|ERU preservation|Every individual factory placement, all inherited resource floors and VP values, all 16 existing ports/levels, owners/cores/manpower/province lists retained |
|ERU logistics|30 disjoint owned-land components, 45 valid coastal ports, eight hubs, 31 same-component railway paths; no cross-water rail; four operational island deployments; all ports/airfields retain valid authored spawn/position coverage |
|Calibration|Actual per-role production and stocks match profile in every DLC branch; all 23 MIL/11 docks assigned; primary-definition resource/fuel/replacement worksheet reproducible |
|Defensive negatives|Changed factories, lost owned state, negative resource addition, stale/mutated/unknown foreign logistics, and extra commands hidden in the economic marker are rejected; fractional inherited resources are preserved |
|Existing focused suites|Capitals9, Anea foundation11, Usean expansion17, interface/government8, Continental War29, supporting-country13, aftermath24, rebellion3, factions35, legacy economy27, PR-scanner self-tests6; special-project source checks also pass |
|Generated output|World placements/output/registry, Anea, governments, Continental War, briefing and typography checks pass |
|Strict authored assets|5,081 sprites and 940 focus bindings; zero missing authored textures, no cleaned-family regressions |
|Full map/static wrapper|Zero map errors; two existing placeholder warnings; 2,007 reference warnings and one technology warning remain explicit audit items |
|No-vanilla hash audit|Zero new or path-independent matches; four inherited technical map matches (`cities`, `colors`, `positions`, `seasons`) |

The [full-generator composition record](generator-composition.json) runs Anea →
World → starting governments and the reverse order. After canonical packaging,
the complete mod payload is stable. The first raw-byte attempt identified only
an existing generated GFX checkout changing CRLF to LF; that unrelated file was
restored instead of included in the component. P0 separately pins GFX line
endings. The candidate record therefore supplies both raw and explicitly
normalized-text digests without confusing line endings with content changes.

The [cross-package history record](macro-history-composition.json) composes the
actual P1 `history_marker` owner from component `5965a5f` with all five World
country histories, in both orders and for three repeats. The same fixed point
is reached. No copied fiscal implementation or permissive fiscal stub is used.

The first full wrapper was invoked under Windows PowerShell5.1 and completed
map/reference/technology checks, then failed because its .NET runtime lacks
`Path.GetRelativePath` used by the inherited hash auditor. That environment
failure is [retained separately](checks/initial-unsupported-host.log). The full
wrapper was rerun successfully under the required current `pwsh` host; its
[passing log](checks/full-static.log) is the acceptance result.

**Native testing remains paused.** No engine launch, shortcut playthrough,
natural progression, old-save load, actual sea supply/fuel throughput, battle
losses, AI growth, story-aircraft behavior or save/reload acceptance is inferred
from these source checks. This roster creates physical starting aircraft but
does not implement or certify an operational squadron story. Normal installation,
profiles, saves, display settings and immutable archive/baseline are untouched.
Root integration, exact-head CI, review and publication are separate next steps.
