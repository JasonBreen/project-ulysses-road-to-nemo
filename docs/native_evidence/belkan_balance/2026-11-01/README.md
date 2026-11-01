# Belkan balance round evidence ledger — 2026-11-01

## Status

This ledger separates offline/static evidence from copied-engine boot evidence.
It contains **no gameplay acceptance result**. The owner instructed the agent to
perform no playtesting before the natural-run matrix began. All human,
observer, save/reload, war-duration, outcome, economy-comparison and postwar
cases therefore remain explicitly unrun.

No raw save, copied profile, engine file, screenshot, Windows username, player
name or normal-profile manifest is tracked here. Local forensic material remains
outside Git in the preserved native-session roots.

## Source and baseline

- Baseline: `origin/main` at
  `797f941e04e51a884b2d26f14eb1b9d66d49ce95`, after the merged #59 → #60 →
  #61 stack.
- Isolated branch: `codex/belkan-balance-round-1`.
- Last implementation commit before this ledger:
  `aade0b993f4a7c0576ff8d1ce8a2c12e824d0243`.
- Gameplay content is archive/mod provenance plus provisional gameplay. This
  round adds no new official ACE COMBAT history or canonical outcome claim.

## Offline evidence

The implementation head passed:

- aggregate campaign contracts;
- campaign-review chronology, layout, category, lifecycle and localization
  regressions;
- the full static validator with zero errors;
- the installed-reference map validator with zero errors and the two inherited
  placeholder warnings;
- reference audits covering 1,648 focus definitions and 1,055 event
  definitions;
- 16 startup-chronology tests;
- Economy v2 generation parity, 27 macro tests and 14 ledger/UI tests;
- all nine force-upkeep tests with the installed engine reference;
- 15 Belkan native-evidence unit tests, including text-save rejection cases,
  schema-2 privacy bounds, real game-rule/flag economy-state extraction, exact
  payload provenance, fail-closed root preparation and verification receipts,
  normal-profile comparison, exact `userdir.txt` bytes, and unchanged or
  engine-rewritten graphics-settings layouts;
- `git diff --check` and a clean tracked worktree after checks.

These are static/offline results only. They do not establish that a focus was
rendered, a decision was clickable, a campaign date was reached, AI fought a
front, or a settlement completed in HOI4.

## Copied-engine preflight history

The installed/copy source reported HOI4 Operation Postern
`v1.19.4.1.99a5`, Steam build `26282552`, checksum `f584`. The exact copied mod
payload contained 7,537 files.

| Session root label | Source commit | Result | Evidence class |
| --- | --- | --- | --- |
| `Project-Ulysses-Native-20261101-Belkan-Balance` | `76df54696c19af47c1cd26e396a9a96e7316ba12` | Prepared, but an explicit `-userdir=` smoke routed writes to the normal profile. The copied PID was stopped. | Failed isolation diagnostic; not gameplay |
| `Project-Ulysses-Native-20261101-Belkan-Balance-483897c2` | `483897c2d9f5da3e9d11b7afe2a237ef71cba8d9` | Preparation stopped without provenance because the engine-rewritten one-line display block was not yet supported. | Failed preparation; never launched |
| `Project-Ulysses-Native-20261101-Belkan-Balance-2bf360da` | `2bf360dab0366cf96948f4852290768fc2ed2841` | Exact payload and one-mod selection passed. A second explicit `-userdir=` smoke reproduced the normal-profile routing defect. A later marker-only smoke routed logs to the disposable profile and preserved the then-current normal baseline. | Isolation boot smoke only; not menu or gameplay acceptance |
| `Project-Ulysses-Native-20261101-Belkan-Balance-aade0b99` | `aade0b993f4a7c0576ff8d1ce8a2c12e824d0243` | Preparation was stopped and the partial root preserved immediately after the owner instructed that no playtesting be performed. | Partial preparation; never launched |

The marker-only smoke used the copied engine's exact `userdir.txt` and copied
launcher `gameDataPath`, with only `-gdpr-compliant` on the command line. It
created disposable logs, a responsive DX11 window and a 3440×1440 graphics
initialization record. It did **not** establish the main menu, active mod list,
bookmark, focus tree, game date or any gameplay behavior.

## Normal-profile preservation record

The first explicit-override smoke changed eight protected file hashes and
removed two rotating log files relative to its before snapshot. The changed
set was `settings.txt`, `naval_dist_checksum.cache`, and six log files; the
removed set was `logs/random_1.log` and `logs/random_2.log`.

The second explicit-override smoke changed six protected log hashes relative to
its before snapshot. The subsequent marker-only smoke compared 146 protected
files before and after and reported zero changed, added or removed files.

No prior bytes were restored or overwritten to make any comparison appear
clean. The two dirty launch records remain part of the preservation result.

## Native matrix

| Run ID | Status | Reason |
| --- | --- | --- |
| `blk-full-historical` | Not run | Owner instructed: no playtesting |
| `blk-full-early` | Not run | Owner instructed: no playtesting |
| `ust-full` | Not run | Owner instructed: no playtesting |
| `ose-full` | Not run | Owner instructed: no playtesting |
| `obs-full-01` | Not run | Owner instructed: no playtesting |
| `obs-full-02` | Not run | Owner instructed: no playtesting |
| `obs-full-03` | Not run | Owner instructed: no playtesting |
| `obs-econ-off-01` | Not run | Owner instructed: no playtesting |

There are no natural or forced saves, sanitized save checkpoints, war-duration
samples, player-viability results, observer outcomes, economy-on/off comparison
or postwar-loop observations for this round.

## Tooling limitation encountered before the stop

Both supported Windows-control backends failed initialization with the same
host error: `failed to write kernel assets: The system cannot find the path
specified. (os error 3)`. No ad-hoc input injection was substituted. The owner
then removed playtesting from scope, so this limitation was not pursued further.

## Balance and delivery consequence

No combat, OOB, supply, production, stage-cost, AI-strategy or Economy v2
coefficient was changed on the basis of the boot diagnostics. The round only
contains the static lifecycle/focus/AI-timing correction and evidence tooling.
The 90–210 day duration target, two-of-three coalition observer target, human
Belka/Ustio/Osea viability and postwar loops remain unaccepted. They must not be
described as passed in a pull request or release note.
