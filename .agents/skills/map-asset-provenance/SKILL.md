---
name: map-asset-provenance
description: Review Project Ulysses geography, map references, and visual assets while preserving the immutable baseline and no-imported-vanilla-assets boundary.
---

# Map and asset provenance

Use this skill for states, provinces, strategic regions, borders, coordinates, rasters, sprites, or asset parity.

- Treat `source/archive-original` and `source/baseline` as immutable evidence. Work only in the editable mod copy.
- Never infer the intended owner, core, geography, or name of state 171 or `XXX` strategic regions. Record the decision as open until source-backed direction exists.
- Before adding an asset, compare it against the baseline and installed reference with the repository's no-vanilla/parity checks. Do not import downloaded executables or untrusted asset packages.
- For map edits, validate `definition.csv`, state ownership, strategic-region membership, adjacency, railways, supply nodes, airports, buildings, unit stacks, raster colors, and coordinate bounds together.
- Keep engine compatibility plumbing distinct from delivered mod art. Existing vanilla references are audit items, not permission to add more.

Acceptance: the source/provenance disposition is documented, static map and no-vanilla checks pass, and any unresolved geography remains explicitly open.
