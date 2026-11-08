# Belka human-played native test, 8 November 2026

Status: preparation in progress; no native acceptance claimed.

Authorized scope: 1991 through January 2000 as human-controlled Belka, checkpoint
repairs, separate alternate outcomes, AI Belka, economy-disabled and no-DLC checks.
Tracking contracts: [#70](https://github.com/JasonBreen/project-ulysses-road-to-nemo/issues/70)
and [#8](https://github.com/JasonBreen/project-ulysses-road-to-nemo/issues/8).

Frozen base: `385d01a74b71227fa58140abc1496d81455ebd5d`.
Branch: `codex/native-belka-1991-2000-20261108`.
Installed reference: Operation Postern 1.19.4.2.2da5 (0bdb), Steam build 26409260.
Runtime version and active DLC remain to be confirmed.

The original workspace and its four pre-existing uncommitted changes are excluded.
Large native evidence, profiles, saves and the physical engine copy remain under
the local session directory recorded in the resumption checkpoint. No GitHub
publication, automatic merge or release is authorized by this test.

## Results

No native scenarios exercised yet. Static results are recorded separately from
natural native play, AI observation and forced diagnostics in COVERAGE.csv.

### Initial offline preflight

All thirteen selected subsystem commands passed on the frozen base: Economy v2
(27 tests), settled ledger, force upkeep, institutions, shared systems, native
compatibility contracts, startup chronology, interface repairs, focus screen,
responsive frontend, decision UI (24 tests), frontend briefing and typography.
Campaign validation reports zero errors and zero warnings; its path report also
completed successfully. The aggregate static wrapper passed under the current
`pwsh` host with installed-reference and preserved-baseline arguments. Its first
Windows PowerShell 5.1 invocation failed on the unavailable GetRelativePath API;
both logs are retained locally. Provenance: four inherited baseline matches,
zero new matches, zero path-independent matches. The reference audit reports
3,868 focus definitions, 1,721 event definitions and 520 warnings; the technology
audit reports one warning. These are baseline offline findings, not native passes.

The map phase reports zero errors and two inherited warnings: one placeholder-
owned state and 204 placeholder strategic-region files. These are not native
findings and their geography is not changed by this playtest.

## Preservation

Preparation records protected normal configuration, save and log hashes and backs
up normal configuration/log contents. Runtime isolation and final preservation
remain unverified until their audits run.
