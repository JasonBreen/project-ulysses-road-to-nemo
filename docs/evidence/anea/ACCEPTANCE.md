# Anea candidate acceptance

**Source implementation and static/offline validation; native acceptance pending.**
Base: `cf8fec41abe5080b1af66eb86189b35c7af522f6`. The candidate lives on an isolated
branch/worktree. No ordinary mod installation, launcher playset, game save or
display setting is changed by this work. No HOI4 launch was performed.

## Offline evidence

All22 recorded check groups pass. The six Anea suites total64 tests:
foundation11, national campaign8, shared systems21, integrated routes5,
artwork8 and presentation11. The installed reference was used read-only for
effective technology/module and GUI-dependency checks. Strict authored assets:
5,081 sprite definitions,934 focus bindings,zero missing textures; effective
repaired-screen dependencies:zero missing references or conflicting definitions.
The no-vanilla comparison against the immutable baseline and installed reference
also passes. None of these results establishes native gameplay acceptance.

`static-results.json` records the check command, exit code and retained log for
the candidate. Foundation tests inspect actual province raster adjacency,
territorial/manpower conservation, correct capital ownership, exact industry,
internal supply routes, placement, DLC roster parity and effective technology
and module prerequisites against a read-only installed reference.

Campaign tests inspect all108 focuses, prerequisites/exclusions, positions,
reward guards, policy alternatives, recovery conclusions,16 narrative events,
late entry and English localization. Shared-system tests execute shipped scripts
through a strict offline subset, covering every integer preparedness value,
payment, actual60/120/180-day delivery scheduling, renewal, interruption,
sanctions, consent, save-like state copies and optional-system independence.

Artwork tests inspect frame dimensions, alpha apertures, texture hashes,
108 distinct focus compositions, actual sprite/picture bindings and source
packaging. The strict authored asset audit is separate from native rendering.
Deepcopy model reloads are not real HOI4 save serialization. Offline AI preferred
choices are not proof of native strategy selection, deployment, pacing or balance.

The country-selection history control now has separate heading/narrative/button
bounds and a380×145 scrolling area. Its captured original control is retained;
the historical whole-layout fingerprint is checked after normalizing only this
explicit repair. The effective engine dependency audit additionally follows this
control's scrollbar. It does not certify every unchanged frontend control.

The builder was launched for the optional scratch check, but capture timed out
twice and no import/export was performed. The user requested their PC back;
all desktop interaction stopped. Repository checks continued headlessly.

## Native acceptance to perform only after separate authorisation

- Record the actual engine build and exact candidate payload hash. Use a
  disposable engine/profile and preserve the normal installation and saves.
- Load both1991 starts and inspect leaders, capitals, industry, building slots,
  production, fuel, stockpiles, land supply, airbase capacity and fleet ports.
- Exercise all available BBA/legacy aircraft and MTG/legacy navy combinations;
  confirm equivalent capabilities and no double-loaded rosters.
- Verify both54-focus trees, exclusive alternatives, long descriptions,
  selected/available/unavailable/completed states, search, zoom, continuous
  focuses, scrolling, keyboard and drag controls at3440×1440/1.0,
 1920×1080/1.0 and2560×1440/1.25.
- Exercise broad/conditional aid, audited/command distribution, self-reliance,
  founding refusal/expiry, renewed services, affordability, interrupted deliveries,
  sanctions/alternative/lifting and optional Nordennavic participation.
- Save and reload around preparation expiry, crisis conversion, pending offers,
  deliveries, cooldowns, reviews, bureau invitations and the final assessment
  after2005. Verify generic/continuous-focus entry really defers active work.
- Check old saves keep existing leaders, forces, technology, industry, resources
  and treasury; receive no retroactive setup/preparation; and can enter future
  eligible recovery content.
- Natural AI checkpoints:1992,1996,1999,2000,2002,2004,2005. Record actual
  construction, equipment replacement, fielded supply, policy selection and
  recovery pacing. Distinguish shortcuts from natural progression.

PR#29's final-candidate fiscal/event presentation, starting-government and vanilla
cleanup, full outcome and DLC/fallback acceptance gaps remain independently
tracked in `docs/evidence/usea-expansion/ACCEPTANCE.md`. This expansion's offline
checks do not close those native gaps. Release readiness and ordinary-install
synchronisation remain separate from source review.
