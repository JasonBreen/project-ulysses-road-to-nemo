# Belka human-played native test, 8 November 2026

Status: paused at the user's request while they play AC8. No HOI4 process remains.
Original animated globe restoration is verified. Healthy economy initialization
passed on6b350f17; the monthly date-scope repair e7fd76f2 passes the full static
wrapper but still needs native settlement acceptance. Human play reachedJan20.2
before a reproducible naval-exercise crash (N009); latest managed save isJan3.5
on e7fd76f2. The January2000 campaign and additional scenarios are incomplete;
no full acceptance claim is made.

Authorized scope: 1991 through January 2000 as human-controlled Belka, checkpoint
repairs, separate alternate outcomes, AI Belka, economy-disabled and no-DLC checks.
Tracking contracts: [#70](https://github.com/JasonBreen/project-ulysses-road-to-nemo/issues/70)
and [#8](https://github.com/JasonBreen/project-ulysses-road-to-nemo/issues/8).

Frozen base: `385d01a74b71227fa58140abc1496d81455ebd5d`.
Branch: `codex/native-belka-1991-2000-20261108`.
Installed reference: Operation Postern 1.19.4.2.2da5 (0bdb), Steam build 26409260.
Runtime confirmed: 1.19.4.2.2da5, control checksum0bdb, initial mod checksum7918,
35 active DLC. Primary startup reports exactly one active mod.

The original workspace and its four pre-existing uncommitted changes are excluded.
Large native evidence, profiles, saves and the physical engine copy remain under
the local session directory recorded in the resumption checkpoint. No GitHub
publication, automatic merge or release is authorized by this test.

## Results

The no-mod control and initial mod frontend reached their native menus. The
control has zero active mods. Both launch audits and the control-exit audit
verified 838 protected files unchanged with no additions. The first natural BLK
opening was saved locally at 1991.1.1.12 on 6636c641 before advancing the clock.
The sanitized primary-opening.json records that state; it does not establish
gameplay or monthly progression. The engine omits default game rules in this
opening save, so the extractor reports ac_economy as unknown; the checksum-only
version difference is retained as an extractor warning. Static results remain
separate from natural native play, AI observation and forced diagnostics in
COVERAGE.csv.

The owner identified the original globe replacement as unacceptable. Recovered
the original archive globe fallback and animated layout; preservation and
generator regressions are in place. Native restoration verification passed at
6636c641: original artwork, rotating globe across separate frames, and no missing
background lookup warning. The final repair's aggregate static wrapper also
passed (local log globe-final-static.log). No replacement artwork was created.
See BUGS.md for malformed localization, starting doctrine failures and frontend
presentation findings. The generic buffer-allocation message also occurs in the
no-mod control and is not attributed to the mod from these observations.

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
up normal configuration/log contents. Control, initial mod, profile transitions
and globe-retest audits all passed. The globe audit at 18:11:32 UTC found all 838
protected files unchanged with zero additions. The post-save audit at 18:21:32 UTC
also passed with 838 unchanged and zero additions. Completion still requires a final
audit after all remaining campaign and compatibility work.

Closed the exact isolated game through its native Quit control and confirmed no
HOI4 process or target window remained. The post-exit audit at 18:23:53 UTC passed:
838 unchanged, zero additions. globe-restoration.json records the repair revision,
native observations, screenshot hashes, static command/result and this audit.
The original workspace still has exactly its four pre-existing modified paths.

## Native opening repair results

N002 malformed special-project localization and N003 missing starting doctrines
passed fresh-start and normal save/reload tests on c159a742. Belka now has Mobile
Warfare, Fleet in Being and Strategic Destruction. Full static wrapper passed.

The first human-play attempt crashed at1991.1.2.1. An unchanged opening replay
reproduced the same access violation.8072d3fa isolates the mod's authored event
directory from inherited Earth-specific event polling. The same saved opening
then advanced to6 January, saved/reloaded, and continued to13 January19:00. This
was a separate diagnostic without management decisions; it is not the main
campaign's progress. Full static wrapper passed. Individual event causality is
not isolated, and no-mod first-day control remains outstanding.

N007's initialization repair6b350f17 passed a fresh native start: GDP4361.99998,
cash87.23999 and debt1308.59999. The first monthly boundary exposed N008, a numeric
date scope error. e7fd76f2 qualifies those operations with global.date and passes
29 economy tests,14 ledger tests and the full static wrapper. Its native replay
was interrupted by N009: fleet exercises followed by unpausing reproduce the
same C++ exception atJan20.2 andJan3.5. Missing sea-terrain dominance values are
the next candidate repair; they have not been changed. N004 scenario layout and
N005 placeholder/interface graphics remain open. No new artwork or geography
was introduced. See RESUME.json for the preserved checkpoint.

The final audit for this paused session,20261108T201339Z, passes all838 protected
files unchanged with zero additions. The main workspace still retains its
pre-existing work. Large crash bundles and logs remain local; no publication.
