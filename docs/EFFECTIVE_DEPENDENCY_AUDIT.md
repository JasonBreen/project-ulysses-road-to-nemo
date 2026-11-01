# Effective presentation dependencies and explicit DLC profiles

This follow-up extends Package 0's source audit to installed directory and ZIP
providers. It does not deliver a completed visual conversion. The repaired
decision-screen ownership gate and the whole-presentation provenance gate are
separate results. No engine/DLC pixels, fonts, audio, shader source or executable
code were copied into this change; retained installed evidence contains paths,
sizes, hashes, counts and dependency dispositions only.

## Reproduce

The synthetic regression suite requires Python only and runs in its own CI step:

```powershell
python -B tools/Test-EffectiveDependencies.py
python -B tools/Test-DecisionUI.py
```

With a read-only installed reference, run a legacy decision ownership check or a
strict presentation check with an explicit profile:

```powershell
python -B tools/overhaul/audit_consumers.py <engine> --profile docs/evidence/effective-dependencies/profiles/base-only.json --gate-decisions --summary-only --output <local-report.json>
python -B tools/overhaul/audit_consumers.py <engine> --profile docs/evidence/effective-dependencies/profiles/archives-and-music.json --gate-presentation --summary-only --output <local-report.json>
```

`--gate-presentation` is expected to exit **1** for the retained installed
scenarios. It fails unresolved potentially reachable presentation, provider and
definition ambiguity, source-reader failures and missing supported scripted-GUI
bindings. Removing `--summary-only` retains the detailed consumer graph.

The metadata capture helper regenerates all three explicit scenarios and bounded
evidence summaries. Its success means the observed PASS/FAIL results match the
documented expectations, including failed conversion gates; it is not an
acceptance gate:

```powershell
python -B tools/overhaul/capture_dependency_evidence.py <engine>
```

The retained summaries list failure counts and samples and hash the complete
failure lists. They explicitly record how many failures were omitted. The full
lists and graph remain reproducible through the audit command above. The
capture helper records the exact executed source hashes alongside its baseline
Git head, because the source capture occurs before the evidence is committed.

## Profiles and provider selection

Without a profile, DLC descriptors and archive metadata are inventoried but no
DLC payload is mounted. An explicit empty selection means a base-only **static
scenario**. A selection never establishes ownership, enabled DLC, campaign
reachability, or the engine's native load order.

Profiles use schema 1:

```json
{
  "schema": 1,
  "name": "An explicit static scenario",
  "enabled_dlc": ["dlc/example/example.dlc"],
  "provider_overrides": [],
  "payload_overrides": [],
  "provenance": []
}
```

The engine-relative descriptor path identifies a provider as
`dlc:dlc/example/example.dlc`. `engine://` may prefix a selected descriptor. Mod
resources use provider `mod`; base installed resources use `engine`.

The installed descriptors are primary evidence for their literal `path` or
`archive` values. They do not establish a total cross-DLC precedence contract.
The audit applies the repository's same-path mod shadowing and descriptor
`replace_path` model, but it refuses to certify differing fallback bytes by
sorting descriptor names. Identical fallback bytes may be equivalent for file
resolution; differing bytes remain ambiguous. Cross-file definition conflicts
also remain unresolved. Identical definition text in different directories is
still ambiguous when its literal media can resolve relative to those different
directories; comparing the text alone cannot certify equivalent resources.
The complete gate also fails any ambiguous effective fallback path, including
content files whose explanatory winner happens to expose no image references.

An exceptional `provider_overrides` entry names one effective resource `path`,
its exact `provider`, lowercase `sha256`, nonempty `reason`, and `evidence`.
It is an explicit audit assumption and requires review. Wildcards, absent or
changed resources, and stale hashes do not resolve a conflict. It does not
silently settle conflicting definitions spread across different files.

Four installed descriptors live under `integrated_dlc` while their literal
`path` values still name empty `dlc/...` directories. Their adjacent integrated
directories contain the actual installed presentation files. The audit does not repair
that mismatch automatically. The all-installed stress profile contains four
explicit `payload_overrides`: descriptor `path`, provider identity, descriptor
SHA256, actual installed `payload` directory, reason and evidence. These are
marked `explicit_audit_mapping_not_native_mount_proof`. A stale descriptor hash,
unsafe mapping, or a mapping for an unselected provider fails inspection.

ZIP members are read in place without extraction or execution. Unsafe paths,
symlinks and encrypted members are not mounted. Text definitions are bounded at
8 MiB before decompression; exceeding this bound remains an unresolved source
inspection. Resource paths are normalized case-insensitively. Relative media
paths are resolved from their defining file; differing root-relative and
source-relative candidates remain ambiguous instead of being guessed.

## Classification and reachability

Every supported consumer receives a conservative potential-reachability label.
The only static retirement currently applied is a decision/category explicitly
disabled by `allowed` or `visible` with `always = no`; every excluded row retains
its reason in `statically_retired_consumers`. Conditional pictures, fallback
icons, portrait pools, music choices and unused-looking model/audio definitions
are not silently removed based on presumed campaign conditions.

| Classification | Requirement |
|---|---|
| `authored` | Exact mod file, matching SHA256 and provider, with a per-file provenance reason and evidence. Installed content cannot be relabeled authored. |
| `approved_sourced` | Exact provider/file/hash with a reviewed sourcing assertion and evidence. The tool checks the binding; it cannot establish legal permission or the truth of an assertion. |
| `technical` | Shader/program service files (`.lua`, `.shader`, `.fx`, `.fxh`) consumed through an explicit program binding, with no pixel/audio family exemption. |
| `unreachable` | A statically disabled decision/category with a recorded reason. |
| `unresolved` | Missing, ambiguous, conflicting, uninspected, or lacking matching provenance; this also propagates through dependencies. |

The retained selected-DLC profiles credit only the 690 exact original
procedural decision textures already pinned by `decisions_assets.json`. They do
not approve any installed artwork/audio or other inherited mod imagery. A local
file's existence alone establishes neither originality nor approval.

The independent follow-up review qualifies program exceptions by the consumer's
binding. A shader or legacy `.lua` alias used as `texturefile`, mask, normal map,
portrait or sound is unresolved, even when the program file exists. Valid
`effectFile`/effect program bindings keep their original-root shader alias.
Two additional negative/positive fixtures cover this false-green path; the
dependency regression suite now contains 31 tests. Resource metadata records
the inspected usage where the binding supplies it.

## Supported dependency edges and limits

The audit inspects effective GUI sprites and literal texture fields, bitmap-font resources, scrollbar
templates, authored and selected fallback content icons, conditional decision
defaults, MIO includes and icons, agency images, character portrait files and
literal generic portrait-pool choices. Strict mode includes all effective GUI
files and conservative engine/DLC/mod runtime roots; it also checks selected
fallback scripted-GUI window, click and dynamic-list bindings. Animated sprite
masks/overlays and map-arrow texture, normal, specular and effect bindings are
included. Other literal media/program paths in supported definitions stay in
the graph instead of being hidden by a closed field-name allowlist.

Model traversal follows entity clones, meshes, suffix-independent named
attachments, particle/proxy references, declared mesh animation IDs and animation
files. Declared `meshsettings` diffuse/normal/specular overrides are inspected
as separate material resources. Nested entity/particle sound effects lead to
named sound definitions and their relative media. UI/event/effect sound
consumers and named music playlist songs are also included.

**Binary `.mesh` embedded materials are not decoded.** Finding the mesh, or even
approving that file's source, cannot certify its embedded material closure; it
remains unresolved. Entity state animation labels without resolved inherited
mesh IDs remain explicitly uninspected. An attachment's animation labels cannot
satisfy its parent entity's state. Clone-plus-explicit-mesh overrides remain
uninspected rather than certifying a union of possibly replaced bindings.
Engine-generated culture/entity
combinations are logged but not fully expanded. Native country-flag selection,
random portrait eligibility, hidden engine consumers and unsupported engine
conventions are not certified. Source-reader parse failures describe this
reader's coverage limits and are not evidence that HOI4 rejects a file.

The legacy `mod_resolved` status and requested-screen gates retain their
ownership purpose for compatibility. They do not imply provenance, visual
appropriateness, frame correctness or native input/rendering. Existing asset,
geometry and typography suites remain separate checks. The complete source
gate is stricter, but it still cannot establish unsupported native behavior.

## Installed-reference evidence

The read-only reference reports `rawVersion = 1.19.4.1` in
`engine://launcher-settings.json`. There are **39 descriptors**: 35 under `dlc`
and four under `integrated_dlc`; 37 directory payloads and two ZIP payloads in
the explicitly mapped all-installed stress scenario. Membership is not proof of
enabled content.

The Rocket Launcher Unit Pack ZIP has 27 regular-file members and SHA256
`3619c316ed8a10a81be6bb6ddec946e0be10889b4a84a72a2fc583186b67fb57`.
The Heavy Cruisers ZIP has one regular-file member, `thumbnail.png`, and SHA256
`921a92f3266259da5355e7e5137d8317ee9e173ee81e8ab4c7fdd83a739131b1`.
The latter archive contributes no member under the audited presentation roots.
Descriptor hashes, archive sizes, mount assumptions, errors and file-extension
counts are retained in
[`installed-reference.json`](evidence/effective-dependencies/installed-reference.json).

[`results.json`](evidence/effective-dependencies/results.json) records the three
scenarios. The base-only legacy decision ownership gate passes. The two
completed-presentation gates fail and retain the wider conversion backlog.
The all-installed scenario deliberately selects every discovered descriptor
and maps the four integrated payloads for stress coverage; it is not a record
of this user's actual enabled DLC. No native test was run, and normal
installation files, profiles and saves were untouched.

The latest reports inspect the composed repair, world-foundation, economy,
Usean-partner and squadron-story payload, including all 162 story decision
rows' owned icons. `macro-screen.json` separately records zero ownership
failures for `countrydecisionview.gui` and `ac_macro_economy.gui`. That narrower
check does not certify provenance, native rendering or the rest of the graph.
The selected archive/music scenario retains 20,235 failed presentation entries;
the explicitly mapped all-installed stress scenario retains 31,625. Those are
dependency entries, including uncertain or unclassified resources, rather than
counts of unique vanilla pictures. The source and profile hashes in
`results.json` identify the exact audit which produced them.
