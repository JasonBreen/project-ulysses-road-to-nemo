# Six-country replacement follow-up

This packet repairs starting replacement production for Emmeria, Estovakia,
San Salvacion, Amber, Ugellas and Delarus. It starts from WorldStarts commit
`f37ff3beae899e38279a4f16d6703cd770a56bbe`, including the reviewed Legacy component.
The production allocations, limited resource additions and reference loss rates
are **provisional gameplay calibration**, not canonical industrial deposits,
military inventories or historical agreements. Existing formations, ship names,
air wings, politics, leaders, industry, borders, cores and manpower are preserved.

| Country | Unchanged MIL | Starting aircraft replacements | Unchanged yards | Starting naval replacements | Manual constraint |
|---|---:|---|---:|---|---|
| EMM | 14 | fighter 1, CAS 1 | 6 | convoy 1, escort 3, submarine 1, patrol cruiser 1 | All four naval roles funded |
| EVA | 16 | fighter 1, CAS 1 | 4 | convoy 1, escort 1, submarine 1, patrol cruiser 1 | All four naval roles funded |
| SNS | 5 | fighter 1, CAS 1 | 2 | convoy 1, escort 1 | Switch combat yard to submarine when needed |
| AMB | 4 | CAS 1 | 2 | convoy 1, escort 1 | Switch the aviation line to fighters and combat yard to submarines when needed |
| UGE | 3 | fighter 1 | 1 | convoy 1 | Switch the single yard to an escort, then restore convoys |
| DEL | 3 | fighter 1 | 1 | convoy 1 | Switch the single yard to an escort, then restore convoys |

Emmeria moves one of five infantry factories to CAS. Estovakia splits its two
aviation factories between fighters and CAS. San Salvacion moves one of two
infantry factories to CAS. Amber retains all three ground-equipment lines;
its single aviation factory cannot replace two aircraft roles simultaneously.
Amber's existing 36 fighters, 12 reserve fighters, 12 CAS and 6 reserve CAS remain
unchanged. The illustrative 2%-per-month fighter-loss sensitivity gives 16.6667
months of reserve alone; this is not an observed loss rate or a permanent
replacement guarantee.

No ships are added. Ugellas and Delarus retain their two **fielded** escorts,
with **zero stored replacement hulls**. A single yard does not produce escorts
and convoys concurrently. San Salvacion and Amber retain their fielded
submarine; their one combat yard requires an escort/submarine switch. The
worksheet includes both Amber switches together as well as each separately.

The existing country AI receives modest CAS/escort sustainment priorities.
These are additive preferences, not an automated rotation controller. Automatic
AI rotation is **not implemented** and native AI queue retention is untested.
`build_notes.py` supplies six persistent, read-only Production references in the
Decisions interface. They do not spend resources, switch queues or grant units.
Their icons reuse the existing original navy/cyan recovery artwork, with both
sprite aliases already bound in `interface/ac_anea_art.gfx` and provenance in
`tools/anea/assets.json`. This packet imports no artwork or vanilla pixels.

## Bounded material correction

The actual default laws matter: Anea uses `limited_exports`; the four partners
retain default `export_focus` and `civilian_economy`. The worksheet applies
their captured literal modifiers, the effective 15% infrastructure resource
coefficient, conservative extraction/retention floors and consumer goods rounded
up before reserving CIV for imports. Each imported resource type rounds its
CIV cost up separately. The inherited partner allocations otherwise needed
three imported material types against only one or two available CIV.

| Country / existing core capital state | Raw resource change | Original → new floor | Reason |
|---|---|---|---|
| SNS / 587 | aluminium +3 | 8→11 | BBA fighter/CAS requirements fit the two-CIV material-import budget |
| AMB / 501 | aluminium +1 | 6→7 | Both aviation rotation endpoints fit the two-CIV import budget |
| UGE / 474 | aluminium +3, steel +5 | 4→7, 6→11 | Convoy and escort endpoints fit the one-CIV import budget |
| DEL / 268 | aluminium +3, steel +5 | 4→7, 6→11 | Same bounded requirement as Ugellas |

These changes are owned by `world_foundation/profiles.json` and its placement
generator. No original resource floor is reduced. The removal regression takes
one raw unit away from each approved increase and requires at least one actual
DLC/manual endpoint to exceed its import budget. The initial estimates were
reduced to these tested minima; no excess buffer or oil addition is hidden in
the allocation. Anea resources are unchanged.

## Source worksheet and limits

`worksheet.json` evaluates 48 actual profiles: six countries × BBA/MTG/NSB on/off.
These six starts field no tank battalions, so NSB enumeration confirms unchanged
selection rather than claiming a new armor-designer route. It evaluates 96
opening/manual-plan endpoints in total, including Amber's combined switch.
It checks selected research before exact named variants, required/category
module bindings captured from primary sources, actual equipment production
gates, stock bindings and allocations against core-owned capacity.

`primary_contract.json` records effective equipment/module resource costs,
build costs, fuel coefficients, unit needs, default/history laws, economic tech
modifiers, trade terms, source hashes and observed launcher version 1.19.4.1.
Text source hashes normalize CRLF to LF. Facts are captured from the mod plus
the read-only installed reference; no installed source payload or asset is copied.

| Country | Lowest CIV margin after starting material imports | CIV margin after material imports plus full-roster fuel sensitivity |
|---|---:|---:|
| EMM | 5 | 1–2 |
| EVA | 2 | -2 |
| SNS | 0 | 0 |
| AMB | 0 | -1–0 |
| UGE | 0 | 0 |
| DEL | 0 | 0 |

All starting material plans and manual endpoints fit the rounded CIV budget.
The table does **not** claim autarky, free construction capacity, existing trade
agreements or sustainable whole-fleet combat tempo. Estovakia and some Amber
DLC profiles need lower operational tempo, a changed allocation or additional
trade capacity for the full-roster fuel sensitivity. Imports still require
eligible willing suppliers and functioning transport. No supplier, transit or
delivery is invented by the worksheet.

Army fuel includes the fuel-using equipment required by motorized/mechanized
subunits even where the subunit has no direct fuel field. A maximum-equipment-
stat-per-subunit proxy and a separate literal count-times-stat stress bound
remain explicitly labelled; neither is a verified native aggregation formula.
Aircraft and naval coefficients use primary definitions. The conservative
opening fuel-stock floor excludes positive silo storage and unverified unit-tank
fill transfers. Replacement rates assume 50% MIL efficiency for sensitivity and
exclude positive output bonuses; the native interpretation of history
`efficiency = 50` remains a separate engine question. Existing history efficiency
values are preserved.

## Preservation and reproducibility

`baseline.json` retains the pre-change country-history hashes, force AST
fingerprints, state identity/industry/logistics fingerprints and resource floors
for all six countries plus Erusea. Erusea's history, roster bytes and resources
are unchanged. All histories remain byte-stable apart from line endings, so
the packet introduces no old-save starting grants or leader/policy changes.
Replacement queues remain new-campaign OOB content.

`world_foundation/original_four.json` is **not refreshed**. The established test
reverses only the explicit fields in `approved_changes.json` before comparing
the old profile/placement/output fingerprints. Current generated consistency,
unchanged force/state fingerprints and exact resource-delta tests separately
check the actual candidate. Undeclared profile edits still fail the old hash.

From the repository root:

```powershell
python -B tools/anea/foundation.py
python -B tools/world_foundation/placements.py
python -B tools/world_foundation/build.py
python -B tools/replacements/build_notes.py
python -B tools/replacements/worksheet.py
python -B tools/replacements/test_replacements.py
python -B tools/replacements/worksheet.py --check
```

All five generators are also checked without writes by the focused suite.
To deliberately refresh technical facts, review the new primary contract and
worksheet together:

```powershell
python -B tools/replacements/worksheet.py --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/replacements/worksheet.py --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --check
```

The independent owner registry becomes stale after these legitimate input
changes. The World owner must regenerate/rebind registry, overview, receipts and
combined coverage on integration. The component never commits those owner
files. For its 20-test World foundation run, the registry was regenerated
transiently with `registry.py --output` and its original bytes restored in a
`finally` block; `evidence/world.txt` states this prerequisite explicitly.

Source checks are not native acceptance. All 14 focused replacement tests,
11 Anea setup tests and 20 World setup tests (with the transient registry) pass.
The broad static runner also passes; its log is retained in `evidence/static.txt`. Native loading,
display of the new notes, production/AI behavior, import delivery, supply/fuel
throughput and save/reload remain untested while native testing is paused.
No game, desktop, installation, normal profile or save was touched.
