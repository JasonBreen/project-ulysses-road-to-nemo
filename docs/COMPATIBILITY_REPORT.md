# Compatibility report

## Evidence captured

- Outer descriptor: `supported_version="1.13.*"`.
- Historical embedded descriptor: `supported_version="1.14.3"`.
- The isolated 1.19 continuation candidate targets `supported_version="1.19.*"`; the repair branch keeps that target in all three descriptors. This is a target declaration, not runtime compatibility evidence.
- Installed HOI4 path: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`.
- Steam appmanifest build ID: `25205862`.
- Executable file/product metadata: generic `1.0`, not a reliable branch identifier.

## Changes made

- Removed the historical embedded absolute developer path from the editable descriptor.
- Removed the historical workshop `remote_file_id` from the editable private descriptor.
- Kept the outer descriptor's local repository path unchanged.
- Kept the immutable baseline untouched for source comparison.
- Replaced the preserved demo-end option's no-op body with `set_global_flag = ac_continuation_active`; this is a static continuation hook, not proof that downstream content is playable.
- Added static checks for province RGB coverage, placement-coordinate bounds, railway/supply-node references, and an installed-reference comparison for the empty `map/positions.txt` format.
- Audited the uncommitted Claude 1.19 candidate against the installed game and verified baseline; removed 12 newly imported exact vanilla files and excluded seven unverified loading-screen thumbnails. See [NO_VANILLA_ASSETS.md](NO_VANILLA_ASSETS.md).

## Not assumed

The installed build ID has not been translated into a `supported_version` string, and no branch-specific syntax has been rewritten. That choice requires a verified game-version mapping and runtime parser evidence; changing the descriptor speculatively could hide compatibility problems.

The repair branch records `1.19.*` as the intended port target because that is the candidate's explicit target. It must not be treated as proof that the installed build is 1.19 or that the port parses successfully.

## Runtime status

No HOI4 launch, mod activation, save/load, or gameplay test has run in this session. A safe isolated user-data workflow has not been established, so the repository remains at static-validation scope rather than claiming runtime compatibility.
