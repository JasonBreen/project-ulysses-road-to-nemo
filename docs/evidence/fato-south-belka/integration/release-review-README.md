# Release-owner review composition

The FATO/South Belka packet composes PR47's reviewed account preservation and
retired automatic line purchases through aviation parent `81e86bae`. The
original fifteen-file `engine_contract.json` capture is unchanged. Fourteen
files retain their captured hashes; only
`common/scripted_effects/ac_release_maintenance.txt` also admits the exact
reviewed version from `45da6a51393edd6b909f5bb45930e09d0c1350e5` (tested source
`ec2f7f325945c85bb3381cc9fabc116fe1dd8e09`). The original and reviewed normalized
hashes are explicit in `source_contract.py`. A changed file, wrong path or
changed original capture is rejected. No national caller changes that owner.

The initial clean composition `e8d3198e48b0645b1122e6380acacc48d978b09f` passed
16 of 18 selected groups. The two failures were the source/art and primary
preservation checks still requiring the retired release-maintenance version.
Their complete logs remain in [the initial report](release-review/checks.json).
National28, macro27, ledger14, upkeep9, release finance16, lifecycle10,
release-source11, decisions23, generators, registry, receipt10 and strict assets
passed. The separate [full installed-reference/baseline static audit](release-review-static/results.json)
passed against the same clean source and all 8,148 raw inputs.

After the exact-version rule and its negative fixtures, all **10 affected groups
pass** at `48e29b873ff7eb1a774e70d7945a6fe54a3a5092`: source/art10, content/art
generation, primary contract, registry, institution generation, focus pacing,
receipt10, decision-gallery equality and strict assets. See
[the fresh exact-source report](release-review-proof/checks.json). It pins
8,148 raw inputs before/after, fingerprint
`edc2b2f87a30afb3f4cf2bcb600582572dd12f541a9a5949aabd76ef65475ef5`.
The changed files are the preservation check and its test only. Both phases
have the same mod payload, SHA-256
`4cf1750ddce61d87db6f0777389af14a61c251daec824fb9c5e4f662c110f2a7`,
using sorted repository-relative POSIX paths, NUL and raw delivered bytes.
These phases are retained separately; no aggregate current-source receipt
relabels earlier tests. The combined row inventory is 912 variants, zero bounds
findings, after the parent's retirement of70 automatic queue entries.

The earlier Windows receipt-fixture CI correction at `92f864fa` resolves the
temporary repository path before comparing it with subprocess-reported paths.
This handles TEMP aliases without relaxing source identity. Failure output is
now surfaced by the runner, and a dedicated Windows/Ubuntu workflow runs the
ten real temporary-Git/subprocess receipt regressions. All19 remote checks
passed on that earlier head. Final-head CI is reported separately on the PR.

Native testing remains paused. These are source/offline, primary-syntax and
reconstruction results, not engine, save/reload, production, AI or installation
acceptance. No review thread was replied to or resolved.
