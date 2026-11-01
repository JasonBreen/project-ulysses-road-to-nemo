# PR47 review repairs: exact-source results

Validated source: `ec2f7f325945c85bb3381cc9fabc116fe1dd8e09`, based on`00b8936714804657f73985e3e67268f9846a6a9e`. Raw source SHA256:`bf28a78ea2471fb6a678cd2c976e733aee0fd14eb314c7e6ab8363b0766de769` across 7234 tracked inputs; `docs/evidence` excluded.

All26 release/shared/static gates pass. No native game, desktop, save/profile/installation change, GitHub push, PR mutation or review reply occurred.

| Gate | Result | Unit tests where applicable |
| --- | --- | ---: |
| release-finance | PASS | 16 |
| release-lifecycle | PASS | 10 |
| release-physical | PASS | 19 |
| release-source | PASS | 11 |
| release-office-lifecycle | PASS | 7 |
| release-primary | PASS | — |
| release-intake | PASS | — |
| release-recipes | PASS | — |
| release-author | PASS | — |
| release-leaders | PASS | — |
| release-worksheet | PASS | — |
| release-art | PASS | — |
| canonical-economy-generator | PASS | — |
| registry-equality | PASS | — |
| release-inventory | PASS | — |
| release-scalar-inventory | PASS | 4 |
| active-owner-coverage | PASS | — |
| authored-assets | PASS | — |
| macro | PASS | 27 |
| ledger | PASS | 14 |
| forces | PASS | 9 |
| shared | PASS | 5 |
| legacy | PASS | 27 |
| decision-ui | PASS | 23 |
| campaign-contracts | PASS | — |
| full-static | PASS | 6 |

The16 finance tests include every expanded initializer field/receipt (positive and zero fragments), all seven released countries, arrears-only/annual-obligation-only/escrow-only records, missing mandatory stocks, and genuine history-marker/UI-only admission. Incomplete accounts retain their values/flags and remain locked on repeated callbacks.

The ordered whole-AST contract independently restores only reviewed guards/hooks, preserving country and option scope and execution order. Nine mutation vectors cover REC→GEB army scope, value changes, command/option order, extra rewards, altered or missing guards and snapshot order. The11 source tests also retain all624 protected inputs.

The19 physical tests include all four BBA/MTG recipe routes, actual5PP certification with zero industry/resources, historical counters, busy/deleted native-line observations and stale retired queue calls. Retirement changes no PP, production, equipment, material or receipt; existing queues stay intact. Captured available-factory names do not establish free-allocation semantics; the manual/certification fallback is explicit.

The initial UI gate rejected its stale derived consumer-bounds artifact. No code changed: the report was regenerated and the actual23-test UI suite passed against the identical pinned source. Both logs are retained. Authored assets pass`--strict-all`; all244 active-start selected source cases retain exact integrated owner receipts. Universal sustainable/native acceptance remains false.

Six original source captures remain byte-identical to the reviewed parent; no repin accepted a mutation. Source and evidence are distinct commits. [Implementation details](../../RELEASE_REVIEW_FIXES.md) and machine/log receipts accompany this report.
