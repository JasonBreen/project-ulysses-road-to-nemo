# World foundations — source acceptance, 31 October 2026

The implementation commit is `fb08414`; current main `3810d1a` was merged as
`60c3d97` before the final checks. The registry was then refreshed for main's
six additional FCU rebellion focuses. Commands and metrics are retained in
[validation.json](validation.json), with the changed-script
[PR scan](pr-scan.md). These are local source/offline results, not GitHub CI or
native HOI4 acceptance.

All ten new foundation tests passed with the installed game used read-only for
effective equipment/module definitions. They check 16 country/DLC combinations,
variant-before-roster ordering, one roster per branch, production capacity,
replacement stocks, scoped AI, protected state identity, owned coastal bases,
actual adjacent owned-land routes and registry completeness. Declared economic
history markers are preserved; disguised extra effects are rejected. Both
complete Anea/world generators ran in either order without changing any payload
hash. Stale, missing-partial, mutated and unknown foreign logistics records are
rejected by the explicit ownership composer.

Existing Anea foundation (11), Usean expansion (17), interface/government (8),
Continental War (29), supporting-country (13), aftermath (24), rebellion (3)
and PR-scanner self-tests (6) passed. Generated content/governments and strict
authored assets passed. The effective source reference was the installed
HOI4 1.19.4.1 game; it was never launched or altered.

The full static wrapper passed after the main merge: map errors 0, with two
existing placeholder warnings; reference warnings 2,007 and technology warnings
1 remain open audit items. The entire warning inventory is not certified inherited.
Strict assets checked 5,081 sprites and 940
focus bindings with zero missing authored textures. The PR scan found zero
errors and warnings in 57 changed script files. These limits remain explicit;
the source checks do not prove every engine-selected visual is non-vanilla.

**Native testing remains paused.** The new four starts still need engine parsing,
save/reload, old-save verification, supply/fuel throughput, aircraft/fleet
placement, AI deployment/production/growth and natural campaign balance checks.
The registry exposes inherited gaps rather than declaring all 69 countries
playable. Its offline parser also reports the pre-existing `FAT_navy` issue;
no native outcome is inferred from that report.

Archive/baseline, province geometry, state ownership/cores/manpower, state 171
and strategic-region geography are preserved. No normal installation, user
profile or save was synchronized or changed. PR review follows the approved
delivery workflow; release publication, remote merging and installation delivery
remain separate actions.

Root review additionally tightened the national AI/research scopes to require
the current tag as well as its original tag. All ten foundation tests and the
read-only equipment/module check passed again after regeneration. This keeps a
dynamic civil-war clone from losing generic AI priorities in favor of a national
template unavailable to that clone. Native AI acceptance is still open.

The subsequent owned-capital review adds eight geographic/source regressions
and fourteen one-field history repairs. All62 currently landowning countries now
have owned capital states; the 48 other owned-capital assignments and seven dormant
histories are preserved. Raster-derived placements use the approved provisional
fallback, not invented canonical city mappings. See [the capital ledger](../../WORLD_CAPITAL_REPAIRS.md).
The registry is regenerated after these changes; its industry, infrastructure,
roster and native-acceptance gaps remain explicit.

Automated review additionally found that the input digest used the host's Path
sort order. It now sorts explicit POSIX-style relative strings by case-folded
name and then exact spelling. The eleventh foundation regression compares
PureWindowsPath and PurePosixPath ordering of mixed-case inputs. The capital
workflow now runs the registry/foundation and eight capital checks on Windows
and Linux; final-commit CI results remain separate from these local observations.

The cross-platform job then exposed a last-bit floating-point difference in
diagnostic squared distances. Capital selection now uses exact rational raster
moments, with six-decimal diagnostic output. The additional tie regression raises
the focused capital suite to nine. Both Windows and Linux jobs pass on697b65d;
all fourteen selected states remain unchanged. This is source reproducibility,
not native geographic or supply acceptance.
