# Decision-row repair: source/offline evidence

This candidate is based on `78e573625ec2ad9265b6aca348966866a857693e`. The [implementation ledger](../../../tools/decision_row_art/README.md) records the art owners, actual geometry, preserved source contracts, localization and native acceptance boundary.

The [before/after gallery](index.html) uses actual DDS frames, shipped GUI coordinates and ACBriefing bitmap-font glyphs. Inspect the [standard](decision_item.png), [targeted](targeted_decision_item.png) and [timed](timed_decision_item.png) row reconstructions. Before garrison titles retain the originally missing-key display; after titles use the restored English localization. Review annotations are not part of the delivered DDS. These are offline reconstructions, not Steam/game screenshots or native acceptance.

The [consumer-bound report](consumer-bounds.json) enumerates549active authored row-icon variants, including all repeated conditional alternatives and conservative defaults. It finds67previously oversized active variants and zero current source-bound failures across all three templates. Six additional statically retired Anea references share the repaired row bindings. The former13source textures and all263original Anea/institution textures remain byte-preserved. Existing flags and illustrations are retained.

The [retained results](results.json) cover11check groups:

- [DecisionUI23](decision-ui.txt), including actual DDS/GFX/frame/scale bounds, all dynamic garrison alternatives/defaults, localized title fit and negative oversized-image/scale/conditional fixtures.
- [AneaArt](anea-art.txt), [institutions](institutions.txt) and [six strategic-project source checks](projects.txt).
- [Anea](anea-generated.txt), [institutions](institutions-generated.txt) and [compact project/garrison](compact-generated.txt) art-generator consistency.
- [Offline gallery reproduction](offline-review.txt).
- [Strict authored-asset gate](assets.txt), with no missing authored texture references.
- [Effective requested decision-screen gate](effective-decisions.txt) and its [dependency report](effective-dependencies.json): zero requested-screen failures. Its broader inventory still reports12unrelated installed-reference parse failures outside the requested decision screen; this is not a claim that every effective screen/model family is closed.
- [Full static/source/map/reference validation](static.txt).

The new small assets are recorded in the owning [Anea manifest](../../../tools/anea/assets.json), [institution manifest](../../../tools/institutions/assets.json) and [project/garrison manifest](../../../tools/decision_row_art/assets.json), with source geometry, dimensions, transparency, frames, bindings and hashes.

Native testing remains paused. Screen visibility, half-pixel alignment, flag substitution, on-map rendering, hover states and actual input/scaling at3440×1440/1.0,1920×1080/1.0 and2560×1440/1.25 remain untested. The garrison decisions' inherited `SPR_*` flags, map-only behavior and legacy variable syntax are recorded gameplay gaps; this repair does not rewrite them. No normal installation, user save, game launch or desktop interaction was used.
