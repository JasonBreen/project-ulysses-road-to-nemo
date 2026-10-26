# Faction validation record — 25 October 2026

Branch: codex/faction-systems-20261025. Isolated E: worktree: ulysses-faction-systems-20261025. Initial base: **2c728e9625fd12d9474a40c6b811539369a603b8**. Reconciled base: **f48428aa829f6b5fe97fd64d9f2abefc108ed84d**. Existing presentation, aftermath, visual and OEM worktrees were inspected/preserved. Open issues #4–#8 were read. Ongoing visual/economy PR #23 owns the shared static wrapper and visual/economy files; this patch changes none of them.

## Evidence levels

- Read-only installed interface inspection: HOI4 1.19.3 / Steam build 25205862.
- Offline interpreter executes actual effects/triggers/decisions/consent events and rejects unknown commands.
- State-copy/852-month fixture checks modeled persistence only, not HOI4 save serialization or a native campaign to 2065.
- Native parser/UI/AI/play/save/reload: **UNRUN**, constrained by the active MD playtest. No game launched/stopped/restarted, and no installed mod/game/playset/save/setting changed.
- At the 25 October reconciliation checkpoint: no MD edits, remote push, PR, external comment, remote merge, publication or generated art. Authorized reconciliation used a local rebase and read-only object retrieval. Later publication authorization is recorded below; native restrictions remain.

## Commands and results

1. tools/Run-UlyssesFactionChecks.ps1 -ReferenceGameRoot (installed HOI4) -IncludeCampaign: PASS. Sequential, below-normal priority, 65.7 seconds total, with TEMP/TMP redirected to the E: evidence directory and Python bytecode disabled.
2. That run passed 31 faction scenarios, campaign contract/PR text/Ustio continuity/native-compatibility checks, static map/reference/technology checks, 24 Peace We Inherit tests and 27 economy tests.
3. Final focused Test-UlyssesFactions.py -v --reference-game-root (installed HOI4): **35 tests passed in 2.070 seconds** after final host-epoch, cross-council isolation, stale-transfer, live-consent and saturated-influence fixes. A generation-guard mutation is detected. The inherited campaign/map/economy files were not changed by those fixes.
4. Reference audit: 724 focuses, 665 events, zero errors, zero duplicate events, zero missing owned events and zero malformed event references. 2,011 inherited localization/reference warnings remain. The new bundle has 95 English localization keys, all checked with BOM/duplicate/reference coverage.
5. Map: 11,352 definition rows, 612 states, 326 regions; zero unassigned non-lake land, extra raster colors, invalid/out-of-bounds building/unit coordinates or errors. Three inherited warnings: one placeholder-owned state, 204 placeholder strategic regions, empty positions file (the inherited campaign runner does not pass its optional reference root to the map wrapper).
6. Technology: 189 dates, 291 start years, one inherited warning. Inclusive 2065 end-date contract passed.
7. Existing mod sprite definitions and textures for all three new references resolve. No corresponding same-path installed vanilla texture is identical. No graphics/audio/font/binary asset was added.
8. All source/execution artifacts and logs created for this work are on E:. Detailed log: E:/Codex/ulysses-factions-evidence-20261025/integration.log; source hashes: source-reference.json in that evidence directory.

## Remote state and handoff boundary

Read-only inspection found main advanced to f48428aa829f6b5fe97fd64d9f2abefc108ed84d (five frontend/typography commits merged as PR #22). The requested local reconciliation completed without conflicts: 89 upstream files and 20 faction files had zero path overlap. The original 3ba65778a5beaa591939f95ad0ade7cc56a055c7 is retained on codex/faction-systems-preserved-3ba6577. Existing E:/G: checkouts and the pending visual/economy PR #23 were not edited. No earlier stopped presentation/campaign task was resumed.

Verified repository identity: **JasonBreen/project-ulysses-road-to-nemo**, URL **https://github.com/JasonBreen/project-ulysses-road-to-nemo**. The configured old origin https://github.com/JasonBreen/project-ulysses-continuation redirects to that repository. Exact evidence:
- gh repo view JasonBreen/project-ulysses-continuation --json nameWithOwner,url,visibility,isPrivate returns nameWithOwner=JasonBreen/project-ulysses-road-to-nemo, visibility=PUBLIC, isPrivate=false, and the Road to Nemo URL.
- gh api repos/JasonBreen/project-ulysses-continuation returns full_name=JasonBreen/project-ulysses-road-to-nemo, html_url=https://github.com/JasonBreen/project-ulysses-road-to-nemo, private=false, visibility=public and default_branch=main.

At the 25 October checkpoint this contradicted the initial private-repository expectation, and no visibility change, push, PR/comment, remote merge or publication had been attempted. On 26 October the user confirmed that public visibility is intentional and explicitly authorized pushing the faction branch and opening a draft PR. This authorization does not permit changing visibility, security settings, merging or force pushing. Machine-readable identity evidence remains in E:/Codex/ulysses-factions-evidence-20261025/repository-identity.json.

Native acceptance is pending because the user confirmed an active MD playtest. This is an explicit execution restriction, not a failed or uncertain native test. There is no installation to restore.

## Reconciliation validation

All applicable modest sequential checks passed on f48428a plus the rebased faction patch in **19.4 seconds**, below-normal priority, with E: TEMP/TMP and bytecode disabled. Detailed log: E:/Codex/ulysses-factions-evidence-20261025/reconciliation.log.

- Faction runner: **35 tests passed**, including installed 1.19 interfaces/DLC descriptors.
- Upstream briefing validator: original layout/control geometry and artwork bindings passed.
- Upstream typography validator: atlas/metrics/license/branding checks passed.
- Campaign: zero errors and warnings; Ustio continuity and native compatibility static contracts passed.
- Aftermath: **24 tests passed**. Economy: **27 tests passed**.
- Reference audit: zero errors, missing owned event references, duplicate events or malformed event references; 2,011 inherited warnings, zero warnings mentioning the new faction IDs.
- Technology audit: zero invalid dates/start years/errors; one inherited warning.
- Original faction source/tool blobs are unchanged by reconciliation; docs now describe the exact base and limits.

The local CI workflow now registers Test-UlyssesFactions.py alongside the existing frontend/static checks. The hosted command omits the unavailable installed-game path: it runs the offline matrix and explicitly skips only the installed-interface test. At that reconciliation checkpoint remote CI was unrun. Subsequent publication/check results belong to the draft PR and exact-head handoff, rather than a claim of native acceptance.

The earlier full map-raster check is retained: neither upstream nor this patch changed map rasters/geography, and the inherited frontend validator also verifies the pinned geography hashes. No native test was scheduled.

## Authorized draft publication — 26 October 2026

The user explicitly approved pushing these faction changes and opening a draft PR at 04:36:38 UTC. The public target is JasonBreen/project-ulysses-road-to-nemo; public visibility is intentional. Before publication, the local branch was clean at ac12afbe8fa29517ca8c02d9ba0d03658d93102d and remote main remained f48428aa829f6b5fe97fd64d9f2abefc108ed84d. A remote faction branch/equivalent PR did not exist; the only open PR was the separate visual/economy #23.

The implementation checkpoint ac12afbe8fa29517ca8c02d9ba0d03658d93102d is preserved on codex/faction-systems-preserved-ac12afb. Publication uses normal commits/pushes and a draft PR. The active MD playtest hold remains: no native launch, UI input, installed mod/game, saves, settings or playset changes. The final source SHA, modest preflight checks and hosted CI results are recorded in the PR/handoff. No merge or visibility/security change is authorized.

Pre-publication verification passed sequentially in **15.9 seconds** at below-normal priority: 35 faction tests with installed-reference verification, the hosted entrypoint (34 passes / one installed-reference skip), frontend/typography and campaign/Ustio/native static checks, 24 aftermath tests, 27 economy tests and PR-text validation. All logs and temporary files remain on E:. The code is unchanged from the preserved ac12afb implementation; the follow-up changes only this publication record.
