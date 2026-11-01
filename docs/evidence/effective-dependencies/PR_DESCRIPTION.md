# Audit explicit DLC providers and hidden presentation dependencies

This tooling and evidence follow-up is stacked on the completed story bindings
in PR #36. Its reports inspect the composed repair, foundation, economy,
Usean-partner and story payload; the runtime changes belong to their earlier
PRs. The audit itself adds no game payload or installed media.

The earlier effective-consumer audit could see loose engine/mod files but could
not resolve DLC archive members or directory-backed packs. This adds a
read-only provider layer with explicit descriptor selections, safe ZIP access,
hash-pinned exceptional payload/provider choices and exact per-file provenance.
It inventories all 39 installed descriptors, including four integrated packs
whose literal descriptor paths name empty roots instead of their adjacent
populated integrated directories.
Installed membership never implies ownership, activation or native precedence.

The dependency graph now includes animated sprite masks/overlays, literal GUI
textures, map objects, archive scrollbar templates, entity clones and named
attachments, declared material textures, animation bindings, portrait pools,
selected fallback scripted-GUI bindings, nested/UI audio and music playlists.
Unknown binary mesh materials, unsupported runtime bindings, ambiguous fallback
providers and conflicting definitions remain unresolved.

A separate `--gate-presentation` gate fails conservative reachable/potential
unresolved presentation; the existing requested-screen ownership gates retain
their narrower purpose. The installed base-only decision ownership gate passes,
while both retained complete-presentation scenarios fail and expose the wider
conversion backlog. Source tests and the existing authored-GFX strict gate do
not turn those failed scenarios into conversion acceptance.

The automated review findings are fixed: music uses an explicit audio binding,
providers with duplicate normalized ZIP member names are rejected before
mounting, and scripted GUI parsing completes before the gate snapshots errors.
Regressions cover approved shaders/images used as tracks, unequal duplicate
members (including an oversized first entry), case/slash aliases, and malformed
authored/fallback scripted GUIs.

Validation:

- 34 synthetic provider/closure regressions and 16 existing decision tests,
  including program-as-texture/audio rejection and valid shader-alias context.
- Focus canvas 9, overview/screenshot 7, briefing and typography checks pass.
- `audit_visual_dependencies.py --strict-all` passes with zero authored-GFX
  missing references.
- Full static/reference suite passes with inherited map 2/reference 2006/tech 1
  warnings retained.
- The composed payload has 6,552 authored sprites and 1,204 checked focus icons.
  Both the decision screen and five-page macroeconomy screen have zero failures
  in their narrower requested-screen ownership checks. This is not provenance
  or native visual acceptance.
- Installed 1.19.4.1 scenarios, exact source hashes, descriptor/archive metadata,
  explicit profiles and failed-gate summaries are retained under
  `docs/evidence/effective-dependencies/`.

Only tooling, CI, documentation and metadata evidence changed. No installed
media/program bytes were copied, no mod payload changed, no game was launched,
and no user profile or saves were touched. Native acceptance remains pending.
