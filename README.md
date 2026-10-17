# Project Ulysses continuation groundwork

This is a private continuation workspace for Sam's Project Ulysses HOI4 Strangereal mod work. The repository and draft PR are private; no public release, developer contact, installation change, or downloaded-code execution is part of this workspace.

## Local layout

- `G:\Project-Ulysses-Continuation\source\archive-original\2985041246_Project_Ulysses.zip` — preserved source archive, marked read-only.
- `G:\Project-Ulysses-Continuation\source\baseline\2985041246\` — static extraction of that archive; baseline files are intended to remain immutable.
- `G:\Project-Ulysses-Continuation\mod\2985041246\` — separate editable working copy, preserving the archive's wrapper layout.
- `G:\Project-Ulysses-Continuation\mod\2985041246.mod` — working descriptor wrapper.
- `G:\Project-Ulysses-Continuation\docs\` — development plan and checklists.
- `G:\Project-Ulysses-Continuation\inventory\` — source and inventory evidence.

The design contract is [docs/DESIGN.md](docs/DESIGN.md). It separates inherited behavior, proposed implementation, and open user decisions.

The isolated 1.19 port repair is kept in `G:\Project-Ulysses-Continuation-1.19-repair` on branch `codex/1.19-no-vanilla-assets`. Its no-vanilla-assets policy and audit are documented in [docs/NO_VANILLA_ASSETS.md](docs/NO_VANILLA_ASSETS.md). The repair worktree does not modify the active Claude worktree.

The project is intentionally separate from `G:\Project-Swallow`.

## Source evidence

- Source archive: `2985041246_Project_Ulysses.zip`
- Size: `166,822,410` bytes
- SHA-256: `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071`
- Supplied source revision: April 5, 2024 SkyMods entry / Modsbase mirror; this is not the team's separate unreleased 2026 rebuild.
- Supplied source links: [SkyMods archive entry](https://hearts-of-iron-4.smods.ru/archives/32830), [Modsbase mirror](https://modsbase.com/0zew6lfuuww9/2985041246_Project_Ulysses.zip.html).

Local HOI4 evidence was read without modifying the installation:

- Installation: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`
- Steam appmanifest: `G:\steamlbirary\steamapps\appmanifest_394360.acf`
- Steam build ID: `25205862`
- Executable file/product metadata: `hoi4.exe` reports generic `1.0`; it is not sufficient by itself to identify the game version.

## Scope and current status

The current work is static inspection and authoring groundwork only. The mod has not been installed, launched, parsed by the game, or runtime-tested. Runtime compatibility, DLC requirements, focus reachability, AI behavior, save stability, and long-run behavior remain unverified.

See:

- [Phased development plan](docs/PHASED_PLAN.md)
- [Content inventory](docs/CONTENT_INVENTORY.md)
- [Compatibility checklist](docs/COMPATIBILITY_CHECKLIST.md)
- [Testing checklist](docs/TESTING_CHECKLIST.md)
- [Prioritized next tasks](docs/NEXT_TASKS.md)
- [Continuation design document](docs/DESIGN.md)
