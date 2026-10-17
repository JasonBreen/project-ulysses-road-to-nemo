# Project Ulysses continuation design

## 1. Purpose and guardrails

Project Ulysses is treated as a private Strangereal historical simulator and campaign continuation, not as a generic replacement map or a public release project. The preserved April 5, 2024 archive is the source baseline. Existing names, events, art references, country content, and canon relationships are preserved unless a change is explicitly justified by repository evidence or approved design direction.

This document separates three states:

- **Implemented** means present in the editable working copy and covered by static checks where applicable.
- **Proposed** means an engineering direction that has not yet been implemented or runtime-verified.
- **Open decision** means the archive does not provide enough evidence to choose safely; no agent should silently decide it.

No section of this document authorizes changing the immutable archive, installing downloaded code, launching HOI4, changing user saves/settings, contacting upstream developers, merging the draft PR, or publishing a release.

### 1.19 port asset boundary

The current continuation target is HOI4 `1.19.*`, based on the explicit target in the isolated port candidate. The target descriptor is not runtime evidence. The port may use engine-compatible configuration and interface definitions where needed, but it must not deliver copied vanilla HOI4 assets or content. The repair branch enforces this with a hash comparison against the installed reference and the last verified Ulysses working copy; inherited baseline matches are reported separately from newly introduced matches.

## 2. Simulator vision

### Proposed target

The continuation should model Strangereal as a coherent alternate-history campaign in which the player can move from the 1991 Belkan War through its political, military, economic, and diplomatic consequences. The simulation should prioritize:

1. a stable and legible 1991 starting campaign;
2. understandable consequences for Belka, Osea, Sapin, Ustio, Gebet, and the other countries already represented;
3. event and focus continuity after victory, defeat, or alternate Belkan outcomes;
4. supply, AI, diplomacy, and production systems that produce playable decisions rather than decorative content; and
5. save-safe expansion into later Strangereal conflicts only after the first campaign arc is stable.

The design goal is a durable private development base. Public-release polish, broad new lore, and exhaustive localization come after the simulation contract is working.

## 3. Inherited baseline versus target

### Implemented inherited baseline

The editable copy currently preserves the archive's broad structure:

- two January 1, 1991 bookmarks;
- 69 country histories;
- 19 focus files, with 650 focus definitions found by the current static audit;
- 599 event definitions, including the Belkan War and postwar branches;
- 15 technology files mixing 1991–2005 content with inherited armor/naval dates;
- 11,352 province definitions, 612 states, and 326 strategic regions;
- province, terrain, heightmap, river, tree, city, and normal-map rasters at the archive dimensions;
- existing country, character, advisor, equipment, diplomacy, and AI configuration;
- an explicit `ac_continuation_active` handoff flag after the preserved demo-end popup;
- static map/reference validation and a private CI workflow that does not launch the game.

The immutable archive and extracted baseline remain unchanged. The editable embedded descriptor no longer contains the historical developer-local path or workshop ID.

### Proposed target

The target is a staged continuation rather than a wholesale rewrite:

- **Stage A — Baseline compatibility:** establish the semantic HOI4 branch, parser compatibility, DLC assumptions, and a reproducible isolated runtime test.
- **Stage B — 1991 Belkan War:** make the existing war start, escalation, AI behavior, supply, focus graph, and victory/defeat outcomes coherent.
- **Stage C — Postwar continuity:** connect existing victory flags, postwar focus trees, elections, occupation, demobilization, and the continuation handoff without inventing borders or successor states.
- **Stage D — Wider Usea and later wars:** add or repair later content only when its geography, dates, and existing repository intent are established.

## 4. Campaign dates and structure

### Evidence

The archive supplies January 1, 1991 bookmarks. The existing Belkan War content and technology definitions establish a 1991–2005 content span, but they do not establish a single authoritative chronology for every later conflict. `world_event.2` was an end-of-demo popup called by several Belkan outcome branches; it did not itself stop the game clock.

### Proposed campaign contract

- Treat January 1, 1991 as the primary compatibility and playability milestone.
- Treat the Belkan War as the first complete campaign arc.
- Treat postwar years as a continuation layer driven by existing flags, focus trees, and outcome events.
- Keep later dates behind explicit content gates until their chronology is documented.

### Open decisions

- Whether the final project should support both archive bookmarks or designate one as primary.
- Which later wars are in scope and their authoritative start dates.
- Which technologies/equipment should receive authored names and localization rather than resolving from inherited engine IDs.

### Inclusive campaign cutoff

The continuation target is an inclusive playable campaign horizon through **2065-12-31**. This is an engine/content contract to audit, not a claim that the archive contains authored events or canon-backed history for every year. No demo-end event, scripted transition, focus gate, technology date, or equipment progression may silently terminate the campaign before the cutoff once later-era work is implemented. The project must separately report:

- whether the engine and scripts permit the campaign clock to reach 2065-12-31;
- which authored content is actually present and tested through that date; and
- which later content is only a placeholder, gameplay abstraction, inherited base-game definition, or open decision.

Every technology and equipment name added or changed for the continuation needs a stable localization key and a provenance classification. Official Project Aces material is the source of truth for lore-sensitive facts; user-authored Joker 1 continuity is a separate approved creative layer and must never be represented as official canon. Future dates or events without either source-backed support or an explicit provisional-gameplay label remain open decisions.

## 5. Geography and shared identifiers

### Implemented rules and facts

- Province IDs are defined by `map/definition.csv` and currently range from 0 through 11,351.
- The province raster is 5,632 by 2,048 and the current definition-to-raster audit finds no extra RGB colors.
- State files own non-lake land provinces; ocean and lake definitions are intentionally not assigned to states.
- Strategic regions cover the defined province IDs, while 204 placeholder strategic-region files remain.
- State 171 remains a `PLH` placeholder with minimal data; its geography and ownership are not inferred.

### Proposed rules

- Never reuse an existing province, state, strategic-region, country tag, focus ID, event ID, or localization key for a different meaning.
- Allocate new IDs only from an explicit inventory and record the allocation in the design/change documentation.
- Treat province RGB values, `definition.csv`, state ownership, strategic-region membership, adjacency endpoints, buildings, railways, supply nodes, and unit-stack coordinates as one versioned geography contract.
- Do not rename or reassign `XXX` regions or state 171 until a user-approved geography decision exists.
- Keep map edits deterministic and reviewable; every raster or coordinate change must be accompanied by validator output.

### Open decisions

- The intended owner, core, name, and geography of state 171.
- The intended names and membership of the 203 `XXX` regions plus the `Placeholder` region.
- Any new borders for postwar or later-war countries.

## 6. Country-content architecture

### Implemented structure

Country histories live under `history/countries`, country definitions under `common/countries`, and country-specific focus, event, AI, character, and localization files use tag- or country-oriented namespaces. The current reference audit validates focus prerequisites and owned event references while allowing inherited vanilla event namespaces explicitly.

### Proposed structure

Each supported country should have a traceable content bundle:

- country history and starting setup;
- country definition and names/colors;
- focus tree or shared-focus inclusion;
- events and scripted effects/triggers;
- AI strategy and diplomatic behavior;
- technology/equipment exceptions;
- localization and art references;
- a short campaign-arc note identifying entry conditions, outcomes, and unresolved gaps.

Country-specific IDs should use stable tag-prefixed names. Shared systems should use a documented `ac_` namespace. Event namespaces should be treated as owned only when defined by the mod; inherited vanilla namespaces must remain allowlisted rather than copied or rewritten casually.

## 7. Systems design

### Technology and equipment

**Inherited:** the archive contains 15 technology files and a mixture of 1991–2005 and inherited armor/naval dates.

**Proposed:** first classify technologies into starting-era, war-era, postwar, and later-content groups, then audit dates, names, localization, and provenance through the 2065 cutoff. Preserve existing names and effects where possible; repair only parser-invalid or clearly unreachable definitions. Equipment balance should be evaluated after a stable 1991 supply/AI baseline, not by changing every inherited date at once.

**Open decisions:** target research speed, historical versus gameplay abstraction, and whether later equipment is available through a single continuous tree or separate era gates.

### Economy and industry

**Inherited:** country histories, buildings, resources, occupation, demobilization, and economic crisis ideas already exist, but reachability and balance are unverified.

**Proposed:** use the Belkan War and its aftermath as the first economy test: mobilization, wartime strain, reconstruction, occupation costs, and demobilization should create meaningful tradeoffs without requiring new lore.

**Open decisions:** the intended economic difficulty and the extent to which postwar industry should be transferred, damaged, or rebuilt; how the child economy implementation will integrate with the static design ledger without competing edits to the repair branch.

### Diplomacy and factions

**Inherited:** existing events and country content reference Osea, Sapin, Ustio, Gebet, Yuktobania, Recta, and other Strangereal actors; current faction and treaty behavior is not runtime-verified.

**Proposed:** preserve existing diplomatic names and effects, then trace them from Belkan War outcomes into postwar relationships. Add no new border or faction outcome until the archive establishes the intended relationship.

**Open decisions:** postwar occupation treaties, alliance structure, and the diplomatic timing of later wars.

### AI

**Inherited:** AI strategy plans and wartime AI modifiers exist, including Belkan crisis and war buffs.

**Proposed:** validate that AI modifiers are removed or transitioned at the existing victory/defeat events, then test supply, front behavior, production, and diplomacy in isolated runs. The new continuation flag is a hook, not an AI implementation.

**Open decisions:** desired AI difficulty, historical aggression, and how much alternate-history divergence is acceptable.

## 8. Continuation beyond the demo

### Implemented

The former demo-end popup remains at the existing event endpoint, but its option now sets `ac_continuation_active`. The Belkan War trace is documented in `docs/BELKAN_CONTINUATION_TRACE.md`. Two active references to fully commented-out Ustio content were removed because their intended definitions were not present.

### Proposed

Use `ac_continuation_active` as a stable contract for future postwar systems. A future continuation layer should consume existing outcome flags such as Belkan victory/defeat markers, existing focus trees, and existing postwar events before adding new content. Each consumer should be idempotent, save-safe, and gated so it cannot fire before its originating outcome.

### Open decisions

- Which existing flag combinations represent each postwar branch.
- Which country remains the player-controlled perspective after each outcome.
- What content follows the handoff and when it should end.
- Whether the demo-end event should eventually be replaced by a branch-specific transition screen.

## 9. Compatibility and acceptance

### Current acceptance evidence

- Static map validation passes with zero structural errors, zero extra raster colors, and zero out-of-bounds placement coordinates.
- Static reference validation passes with zero unresolved owned focus or event references.
- CI runs the combined static suite on Windows and does not launch HOI4.
- Installed reference inspection found an empty `map/positions.txt` in both the mod and installed game format.

### Proposed acceptance gates

1. Static validation is clean except for explicitly documented design warnings.
2. The selected HOI4 semantic version and DLC assumptions are recorded.
3. An isolated runtime smoke test loads the mod and reaches both January 1, 1991 bookmarks without modifying user saves/settings.
4. The Belkan War can start, progress, and reach each existing outcome branch without parser errors.
5. A save/load cycle preserves focus, event, flag, state, supply, and diplomacy state.
6. A controlled long-run test evaluates AI and supply behavior before any public-release decision.

Runtime gates remain open. No runtime success is claimed by this document.

## 11. Canon and authorship policy

Official Project Aces/ACE COMBAT sources are authoritative for lore-sensitive facts such as dates, borders, country/faction names, characters, and named equipment. The official ACES site describes the shared Strangereal setting and its series chronology; repository content and the April 2024 archive are provenance for this mod, not proof of official canon. See [docs/CANON_POLICY.md](CANON_POLICY.md) and [docs/CANON_LEDGER.md](CANON_LEDGER.md).

Sam's established Joker 1 continuity is an explicitly permitted user-authored layer alongside official canon. It is not to be discarded as unofficial, but it must be compiled from Sam's established material before implementation. The current planning note records only the unverified outline: Ustian-born Joker 1; Belkan connections; history with Moon11/Shadow22; Watchtowerorganization; connection with Cope; and Tasha's mother as the pilot who shot him down. Dates, details, and causal links remain unverified and must not be invented or promoted into the official canon ledger.

## 10. Coordinated agent development

Agents should work in narrow, reviewable slices:

- **Repository/compatibility:** descriptors, version evidence, parser-safe syntax, and baseline preservation.
- **Geography:** map definitions, states, regions, coordinates, and validator updates only.
- **Belkan campaign:** focus/event graph, existing flags, postwar handoff, and branch trace.
- **Country systems:** economy, diplomacy, AI, technology, and equipment within documented country bundles.
- **Localization/art:** labels and descriptions grounded in existing comments, effects, or established identifiers; no placeholder lore presented as canon.
- **Testing:** static regression, isolated runtime, save/load, and long-run AI checks when authorized.

Every agent should state whether a change is implemented, proposed, or an open decision; preserve the baseline; add or update a regression check when practical; and leave unresolved design questions explicit for Sam.

### Economy and portable workspace integration

The economy/IDE work is owned by a separate child task and worktree. This repair branch must not edit that child implementation in place. The integration contract is to review and merge the child task's Markdown economy model, assumptions, IDs, and validation notes into the shared design/roadmap after the child reports its exact branch and files. The final workspace should remain portable for VS Code and Antigravity-compatible agents: repository-relative paths, PowerShell entry points, no machine-local editor settings as requirements, no hard-coded developer paths, and a concise handoff document for each agent-owned slice.

The child work is **in progress and unverified** until its branch is reviewed. The integration issue must track dependencies on the 1.19 descriptor, country/economy IDs, technology naming, canon provenance, and static validation. Runtime economy balance remains open.
