# Implementation roadmap

## Completed in this session

- Created and verified the private GitHub repository.
- Removed the historical developer-local absolute path from the editable embedded descriptor; the immutable baseline is unchanged.
- Sanitized tracked evidence so the repository does not retain the original user's local Downloads path.
- Added a repeatable static map validator covering province definitions, state assignments, strategic-region coverage, adjacency endpoints, airport/rocket references, building and unit-stack coordinate bounds, railway/supply-node references, province RGB coverage, raster headers, and known placeholders.
- Added a static regression wrapper and private CI workflow; the checks do not launch HOI4.
- Replaced the preserved demo-end event's no-op option with an explicit `ac_continuation_active` global handoff flag and neutral continuation wording. Existing gameplay continuation remains unverified.

## Next implementation slices

1. Use validator output as a pre-commit gate and add reference checks for country tags, focus IDs, event IDs, scripted effects, and localization keys.
2. Decide the target HOI4 branch from the installed build evidence before changing `supported_version` or branch-specific syntax.
3. Resolve state 171 only after Sam supplies intended geography/ownership; do not invent a replacement.
4. Classify the 203 `XXX` strategic regions and rename only where lore-backed intent is established.
5. Trace the 1991 Belkan War event/focus graph beyond the new handoff contract and replace remaining demo-terminal transitions with explicit continuation contracts.
6. Run the approved isolated runtime smoke test once a safe non-destructive HOI4 launch method is verified.
