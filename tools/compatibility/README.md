# Startup consumer chronology

`variant_order.py` checks explicit starting-equipment consumers in country history
and the OOBs that history actually selects. It replaces the older blanket rule
that every aircraft and naval variant had to precede the first air or naval OOB.
An independent naval designer block may follow an aircraft load, provided its
own selected consumers receive their required research and named designs first.

The checker evaluates the installed DLC names actually used in history, current
country and explicitly read foreign AI identities, supported Boolean selectors,
and country flags in statement order. OOB `instant_effect` blocks use that same
context and may update it. An unselected NSB or legacy production branch cannot
create a false dependency on the other route. Unknown selectors and unhandled
nested military wrappers fail explicitly. Each DLC/AI case is reported separately;
this matrix is source selection coverage, not enabled-DLC or native acceptance.

Typed consumers include air wings, ship equipment, forced named designs,
stockpiles and production queues, including land queues loaded through `set_oob`.
Required equipment and the used named design's modules must have a selected
technology grant before consumption. An unused historical design does not need
to be researched merely because its declaration remains in the source. Missing
startup declarations cannot be excused by a similarly named runtime decision.
Cross-country producer designs require a separate explicit startup proof; the
current checker fails those cases rather than assuming load order between tags.
It does not infer battalion equipment, validate module fit or personnel, or
model the engine's production/supply behavior.

`research_contract.json` contains identifiers and SHA-256 hashes from the loose
installed HOI4 1.19.4.1 technology files. It contains no complete engine scripts,
pixels or audio. Current same-path mod files replace their captured fallback
facts. Conflicting effective technology definitions fail. The sole explicit
inherent equipment baseline is `convoy_1`, whose primary definition and lack of
a technology unlock are captured. Additional DLC-archive-only definitions are
outside this loose-source contract and must be added as explicit primary facts
if an actual consumer needs them; they receive no blanket exception.

Run the offline regressions with:

```powershell
python -B tools/Test-StartupChronology.py
python -B tools/Test-NativeCompatibilityContracts.py
python -B tools/compatibility/variant_order.py --output runtime-output/startup-chronology.json
```

The synthetic fixtures cover independent aircraft/naval initialization, unused
declarations, selected NSB/legacy OOB effects, land production, stockpiles, shared
flags, AI scope, late research and designs, unknown conditions, effective file
replacement and repeated unlock lists. A real AMB source mutation moves its
used naval design and research after the corresponding naval load; both must
fail while the unmodified independently initialized family passes. Test mutations
stay in memory and never rewrite authored exports.

To refresh the captured metadata against a read-only primary installation:

```powershell
python -B tools/compatibility/variant_order.py --capture-reference <HOI4-directory>
```

Refreshing metadata still runs the current source audit. A failed source audit
does not invalidate the capture or prove a native issue. Keep source debt and
native limitations separate in the associated evidence.
