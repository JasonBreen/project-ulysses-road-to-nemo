# Compatibility report

## Evidence captured

- Outer descriptor: `supported_version="1.13.*"`.
- Historical embedded descriptor: `supported_version="1.14.3"`.
- Installed HOI4 path: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`.
- Steam appmanifest build ID: `25205862`.
- Executable file/product metadata: generic `1.0`, not a reliable branch identifier.

## Changes made

- Removed the historical embedded absolute developer path from the editable descriptor.
- Removed the historical workshop `remote_file_id` from the editable private descriptor.
- Kept the outer descriptor's local repository path unchanged.
- Kept the immutable baseline untouched for source comparison.

## Not assumed

The installed build ID has not been translated into a `supported_version` string, and no branch-specific syntax has been rewritten. That choice requires a verified game-version mapping and runtime parser evidence; changing the descriptor speculatively could hide compatibility problems.

## Runtime status

No HOI4 launch, mod activation, save/load, or gameplay test has run in this session. A safe isolated user-data workflow has not been established, so the repository remains at static-validation scope rather than claiming runtime compatibility.
