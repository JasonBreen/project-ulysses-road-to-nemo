# Economy PR tracking and port compatibility

On 2026-10-17, [PR #3](https://github.com/JasonBreen/project-ulysses-continuation/pull/3) was rechecked at economy implementation head `ddb191aa5c3407d9f13b2fd275dbab3f9b0e3b33`, based on `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8`. All four push/PR CI check runs passed. The automatic code review completed on that exact implementation head with no findings; there were no review threads or unresolved inline comments. These are snapshot results, not a guarantee about later heads.

## Detached combination with PR #2

The tested port snapshot is [PR #2](https://github.com/JasonBreen/project-ulysses-continuation/pull/2) head `92173286b8315e22b3949a98ad6b559225fd0a15`. A separate detached worktree was created from it and the economy implementation commit applied with `git cherry-pick --no-commit`. No shared branch, active port checkout, Claude checkout, game installation, save or playset was changed. No integration commit was published.

The first application had one conflict, in `README.md`: both branches inserted useful paragraphs immediately after the design-contract link. Both sides were retained for testing. The economy branch follow-up moves its existing paragraph into the status section, so the final combined delta can retain the port/parity paragraphs without that insertion conflict. There were no game-file conflicts; all economy game changes remained additions. DESIGN and ROADMAP merged without textual conflict, but their implemented/proposed status still needs human review when choosing the eventual integration baseline.

Results on the detached combination:

| Check | Result |
| --- | --- |
| Economy script/accounting suite | All 27 checks passed, including the three 3,914-week offline scenarios |
| Map | Zero structural errors, extra colors, out-of-bounds placements or invalid building/province associations; two inherited placeholder warnings |
| References | 650 focuses, 600 events; no blocking errors; 3,180 inherited warnings |
| Technologies | 384 date literals, 391 start-year literals; no blocking errors; one warning |
| Campaign boundary | `END_DATE=2066.1.1.1` passed the port's assertion |
| Asset comparison against frozen c72422d working baseline | Zero new installed-reference matches, zero asset-audit errors; 13 inherited plaintext/config matches; three missing-thumbnail warnings |
| Asset comparison against the April archive | Failed with 12 installed-reference plaintext matches absent or different in that older archive baseline |

The commands were the existing economy unittest entry point, followed by the port's `Test-UlyssesStatic.ps1` with read-only `ReferenceGameRoot` and `BaselineRoot` arguments. The full wrapper used the April archive baseline and therefore exited nonzero at the asset stage after the map/reference/technology/horizon stages passed. Only the asset comparison was then repeated with the port's documented **last verified working copy** baseline, frozen at c72422d in a separate detached worktree, and passed. This was not an all-green full-wrapper result against the April archive.

The live working checkout was not used as the second baseline: it had moved to another local commit and had an unrelated validator edit during this assessment. Freezing c72422d avoided reading a moving baseline or disturbing another session's work.

## Asset-policy distinction and remaining decisions

The 13 inherited exact installed-reference matches at c72422d are:

- `common/units/equipment/convoys.txt`;
- `common/units/equipment/upgrades/air_upgrades.txt`;
- seven `common/units/names_divisions` files prefixed `AFA`, `GXC`, `MEX`, `SHX`, `SIK`, `XSM`, and `YUN`;
- `map/cities.txt`, `map/colors.txt`, `map/positions.txt`, and `map/seasons.txt`.

Only `map/positions.txt` also matched the immutable April archive. None of these files is added or modified by the economy slice. The comparison against c72422d proves the economy combination introduces no new exact vanilla matches under the port audit's current baseline policy. It does **not** prove that every retained text/config file is original Ulysses content or that the entire mod contains zero vanilla-derived material. The port/parity owner must classify these retained files under the approved packaging and no-vanilla-content boundary; this economy follow-up neither deletes them nor weakens the validator. Missing background-picker thumbnails also remain runtime-unverified.

Tracking dependencies are [economy/workspace issue #7](https://github.com/JasonBreen/project-ulysses-continuation/issues/7), [parity issue #4](https://github.com/JasonBreen/project-ulysses-continuation/issues/4), and [runtime issue #8](https://github.com/JasonBreen/project-ulysses-continuation/issues/8). Issue #7's earlier description calls the workspace Antigravity-compatible; the verified claim remains a portable VS Code-format workspace only. Antigravity execution and native IDE task execution have not been tested. The coordinated canon policy/ledger on the port snapshot must govern later country or equipment calibration.

No native HOI4 parsing, fixed-point precision/range, weekly scheduling, category rendering, save/load/civil-war inheritance, original-content runtime parity, AI balance or actual end-2065 campaign run has been accepted. The long simulations are offline script evidence. Keep these gates open regardless of CI or PR ready-for-review status. Choose the final port/parity snapshot and reconcile shared documentation before considering integration; nothing here authorizes a merge or main-branch push.
