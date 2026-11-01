# The two reviewed financial-owner updates

The original AIR preservation capture still contains exactly its original 1,107
file hashes. It has not been refreshed to accept another owner's work.

The reviewed release-country package legitimately changes two captured files:
`ac_economy_compat.txt` and `ac_macro_effects.txt`. A separate
`tools/air_program/reviewed_owner_updates.json` identifies their exact old/new
normalized hashes, original capture commit, release component and composed owner.
It inventories every unchanged top-level effect by its parsed-AST hash and the
two reviewed initializer changes separately. Only two new public adapters are
added; no existing effect is removed.

The compatibility owner changes `ac_econ_initialize` and adds
`ac_econ_adopt_release_account`/`ac_econ_try_fund_release_project`. The macro owner
changes only `ac_macro_initialize`. This preserves LAND's instrument observations
and all other existing macro functions, while preventing a legitimate release
from seeding a second opening account. Release finance/lifecycle regressions
remain the authoritative tests for those behaviors.

AIR's preservation test permits exactly those reviewed file versions. Its new
owner-composition regression verifies the function inventory and every current
function hash, requires the approved two-file scope and unchanged original
hashes, and runs the canonical economy generator in strict check mode. The other
1,105 protected files still require their original capture hashes, including all
1991 equipment, histories, forces, technologies and project/on-action contracts.
No whole source, GUI capture or manifest was recaptured to make composition pass.

The PR #47 review successor `45da6a51` tightens the same reviewed macro initializer:
partial stocks and receipt fragments are preserved and review-locked. The current
normalized effect-file hash is `fba2577bf92630a7e9236769fbacbd93ebaa855cb924a7fdb741ad482a256f96`;
the initializer AST hash is `bef7f228eb057e12dcf5978fabaab5542ade4cd9aecf0f39b655fa1bf7f79d62`.
The previous approved `cfac214a` file and `4a6318e4` initializer version remain
explicitly recorded in the separate update table. All 53 unchanged function hashes
remain exact. Companion trigger additions are checked through the canonical
financial generator and 16 actual-owner release-finance cases; they are not a new
blanket exception to the captured effect files.

This is source ownership and generated-output evidence. It changes no AIR design,
aircraft grant, starting force, strategic project, territory or native acceptance.
