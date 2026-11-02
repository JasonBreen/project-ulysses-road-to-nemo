# Reviewed regional caption repairs

The active-world label audit found 204 state captions and 13 existing locality
captions matching the installed English Earth templates. Four locality captions
also came only from the engine fallback. The independent full-caption audit
then exposed two empty state captions and 24 existing victory points with no
caption in mod or inspected loose engine English. This package gives all
206 states and 37 localities neutral
captions derived from their existing national identity. Every replacement is
**provisional gameplay presentation**, not an official place name or newly
established location.

The explicit mappings and primary file hashes are in
`tools/regional_labels/labels.json`. The state caption scope is reviewed and
fixed; the generator does not silently rename future source-backed locations.
Capital District means the existing 1991 capital state. Other district letters
follow the state-ID order within the existing owner. Locality letters avoid
earlier caption collisions. All 37 locality provinces already contain an
authored positive-value victory point. No city, point value, border, province,
core, population, state owner, building or raster is created or moved.

Two inherited Sapin training schools used the Earth city names Toledo and
Zaragoza in their visible focus and first-stage idea titles. Those four captions
become National Fighter Weapons School and National Tactical Support School.
Their technical IDs, modifiers, prerequisites, training purpose and full focus
descriptions remain unchanged. These are adaptations of inherited mod
presentation, with no new canonical institution claim.

Existing names outside the explicit mapping remain unchanged. PLH/state 171 and
the inherited `XXX` caption in state 607 retain their existing source
requirements. The latter remains an acknowledged unresolved caption; this
package does not conceal it behind an invented named region. Strategic-region
`XXX` geography, unreviewed name pools and the wider presentation conversion
remain separate backlog items.

The generator writes one BOM-marked English replacement file. It checks actual
state/province ownership, original captions, existing point placements and
conflicting replacement owners. Future official or approved mod-continuity
mapping must deliberately remove/adapt a provisional entry, rather than being
silently overwritten. Offline primary recapture verifies the matching shipped
names and file hashes when a read-only installed reference is supplied.

Reproduction:

```powershell
python -B tools/regional_labels/build.py --check
python -B tools/regional_labels/render_review.py --check
python -B tools/regional_labels/test_labels.py --reference '<read-only HOI4 root>'
python -B tools/regional_labels/audit.py --reference '<read-only HOI4 root>' --gate-reviewed
```

The eight source tests cover explicit scope, effective English ownership,
preserved names/descriptions, negative mutations, point placements, generated
consistency and installed-primary metadata. CI executes seven source tests and
explicitly skips the primary recapture without an installed reference. The
searchable source comparison is under
`docs/evidence/regional-labels/caption-review.html`; it is not a native map or
screenshot. Native testing and desktop control remain paused.
