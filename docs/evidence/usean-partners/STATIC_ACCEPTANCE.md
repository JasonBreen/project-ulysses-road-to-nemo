# Usean partner Package 2: offline evidence

Evidence date: 2026-10-31. Worktree: `G:\Project-Ulysses-Usean-Partners`, branch
`codex/strangereal-usean-partners`, base `3810d1a`. This report describes the
uncommitted national-content candidate before the separately owned Package 1
system integration. It is not an exact-head CI or native acceptance report.

## Candidate scope

- 228 persistent focuses: SNS72, AMB60, UGE48, DEL48.
- 24 authored national choice events, four reciprocal FCU reply events.
- 54 decisions: the original 25 plus 29 operational scopes, ten temporary
  service programmes, 32 enduring policy alternatives and four national dynamic modifiers.
- 311 original RGBA DDS textures with dimensions, frame and alpha metadata;
  all 228 focus compositions have distinct rendered SHA-256 values.
- Four 1991 programme starts, date-gated preparation, domestic and reciprocal
  services, delayed-save adoption, differentiated settlements and assessments.
- No history, character, state, province, OOB, equipment, border, faction, war
  or project-owner file changes in this package.

## Passed checks

The local Python checks used Python 3.12 with Pillow11.3.0 and numpy2.2.6,
matching the artwork CI pins. Commands use the project root as working directory.

| Check | Result |
|---|---|
| `python -B tools/usean_partners/build.py --check` | All 15 generated script/localization files and the focus-purpose manifest match sources. |
| `python -B tools/usean_partners/build_art.py --check` | All textures, bindings, manifests and review artifacts reproduce byte-for-byte. |
| `python -B tools/usean_partners/test_content.py` | 27 tests passed, including all 228 reward guards, all 117 curated capability consumers, 29 finite-resource scopes, 64 chronological policy courses, annexation/return, costs, interrupted leases, obligations, bilateral eligibility, late saves, panel extents and art. |
| `python -B tools/audit_visual_dependencies.py --strict-all` | Zero unresolved texture references; zero cleaned-family regressions. Authored sprites 5624; focus icons checked 1168. |
| `pwsh -NoProfile -ExecutionPolicy Bypass -File tools/Test-UlyssesStatic.ps1 -ModRoot ./mod/2985041246 -ReferenceGameRoot <installed HOI4 root>` | Passed using the read-only installed 1.19.4.1 reference. Map errors0. Existing map warnings: one placeholder-owned state, 204 placeholder strategic regions. The reference audit reported2007 warnings and the technology audit one warning; this packet does not claim a warning-free reference audit or classify that entire inventory as inherited. |
| `python -B tools/validate_campaign.py` | Errors0, warnings0. |
| `python -B tools/test_economy.py` | 27 tests passed. |
| `python -B tools/Test-UseaExpansion.py` | 17 tests passed. |
| `python -B tools/Test-ContinentalWar.py` | 29 tests passed. Also included in the full static suite. |
| `python -B tools/Test-UlyssesFactions.py --reference-game-root <installed HOI4 root>` | 35 tests passed, no skips. |
| `python -B tools/Test-AneaIntegration.py` | Five tests passed. |
| `python -B tools/frontend_briefing/validate.py` | Passed:44 textures,59 sprites,30 bookmark bindings. |
| `python -B tools/frontend_typography/validate.py` | Passed:465 glyphs, atlas/metrics/license/branding. |
| Changed-file `pr_scan.scan_changed` against the new mod payload | 327 mod files inspected, zero findings. |
| `git diff --check` | Passed. |

The full static suite also passed its aftermath24, supporting-country13,
special-project, Usean-rebellion3 and PR-scanner6 checks. Placeholder geography
was preserved. These are pre-existing source debts, not resolved map claims.

## Evidence boundaries and dependency gate

The national test harness executes the shipped partner ASTs and the existing
`ac_ucw` owner scripts. Its politics and fiscal calls are explicitly documented
adapters of the published Package 1 contracts. They verify caller guards and
once-only charging, not the full economic model's arithmetic. Their owners have
separate suites. No adapter or substitute owner is shipped in the mod.

`build.py --check --require-dependencies` currently refuses release on this
isolated base because the separately authored `ac_pol_active`,
`ac_pol_change_capacity`, `ac_pol_previous_tree_idle`, `ac_econ_can_pay_programme` and
`ac_econ_pay_programme` definitions have not been integrated here. CI deliberately
requires this gate. The candidate must integrate the reviewed Package 1 owners
and rerun the combined checks before publication.

The purpose audit originally identified 117 index-only nodes (SNS 42, AMB 33,
UGE 20, DEL 22). Their specific capabilities now gate 29 named paid operational
scopes, with different benefits, opportunity costs and finite-resource uses.
`purposes.json` records zero remaining sole-axis rows. The tests individually
remove each capability, prove the linked action is blocked, execute its actual
focus reward and prove that action becomes eligible. This is a concrete action
consumer check, not a title or token-presence check.

All four continuous-focus panels now sit beside the upper tree at x 1536 / y 16.
The extent check reads the shipped GUI spacing and panel dimensions, verifies
clearance from every resolved node, and checks the primary viewport. Secondary
display configurations still require native pan/scroll and readability checks.

The annexation hook uses the engine's documented ROOT-winner / FROM-annexed
country scopes. It interrupts paid work before a quick release can complete it,
closes pending offers and stops accepted service relationships. The regression
covers every operational scope, all four base-service actors and both pending
and accepted offers, including restoration inside the original reply window.

The chronological courses execute real prerequisite groups, mutual exclusions,
35/70-day costs, bypasses and rewards for every combination of the four policy
pairs. They use a deterministic national-focus selection model and a peaceful
settlement fixture. They establish route reachability and permit assessments
to finish after 2005; they establish neither native historical AI selection nor
natural war progression. War outcome tests set the existing owning outcome
flags as fixtures; no new content sets those flags.

The source contact sheet was visually inspected. Focus symbols have transparent
corners, opaque central panels and no baked captions or added watermark. The
artwork gallery and contact sheet are authored review artifacts, not game
screenshots.

## Still pending

- Integration against the real Package 1 owners and exact-head CI after review.
- Native 1.19.4.1 tree selection, tooltips, focus states, search/zoom, long
  descriptions, continuous-focus placement and decision presentation at all
  three required display configurations.
- Native natural progression and AI pacing, war/peace/occupation branches,
  save/reload and diplomatic interruption cases.
- Native special-project DLC/fallback observations of the unchanged owner.
- No native game, desktop, normal installation, user save or settings action was
  performed. Native testing remains paused.
