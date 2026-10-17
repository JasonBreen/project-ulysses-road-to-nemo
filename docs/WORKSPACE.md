# Workspace and source evidence

This is a local-only continuation workspace for Sam's private Project Ulysses HOI4 Strangereal mod work. No remote repository, publishing, developer contact, release, or downloaded-code execution is part of this workspace.

## Local layout

- `G:\Project-Ulysses-Continuation\source\archive-original\2985041246_Project_Ulysses.zip` — preserved source archive, marked read-only.
- `G:\Project-Ulysses-Continuation\source\baseline\2985041246\` — static extraction of that archive; baseline files are intended to remain immutable.
- `G:\Project-Ulysses-Continuation\mod\2985041246\` — separate editable working copy, preserving the archive's wrapper layout.
- `G:\Project-Ulysses-Continuation\mod\2985041246.mod` — working descriptor wrapper.
- `G:\Project-Ulysses-Continuation\docs\` — development plan, checklists and the 1.19 port log.
- `G:\Project-Ulysses-Continuation\inventory\` — source and inventory evidence.

The project is intentionally separate from `G:\Project-Swallow`.

## Source evidence

- Source archive: `2985041246_Project_Ulysses.zip`
- Size: `166,822,410` bytes
- SHA-256: `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071`
- Supplied source revision: April 5, 2024 SkyMods entry / Modsbase mirror (open alpha v0.2, "Under Our Treads"); this is not the original team's separate unreleased 2026 rebuild.
- Supplied source links: [SkyMods archive entry](https://hearts-of-iron-4.smods.ru/archives/32830), [Modsbase mirror](https://modsbase.com/0zew6lfuuww9/2985041246_Project_Ulysses.zip.html).

## Local HOI4 install

- Installation: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`
- Steam appmanifest: `G:\steamlbirary\steamapps\appmanifest_394360.acf`
- Game version (from `launcher-settings.json`): **Operation Postern v1.19.3.0.c01a**
- Steam build ID at baseline: `25205862`
- `hoi4.exe` file metadata reports a generic `1.0` and is not used as the version label.

## Dev test registration

Runtime testing uses a separate descriptor so the original workshop copy in `Documents\Paradox Interactive\Hearts of Iron IV\mod\2985041246` is left alone:

- `Documents\Paradox Interactive\Hearts of Iron IV\mod\ProjectUlysses_dev.mod` — copy of `mod/2985041246.mod` with `name="Project Ulysses: Continuation (dev)"` and `path=` pointing at the working copy being tested.
- Before a test launch, `dlc_load.json` is backed up (`dlc_load.json.bak-20261017-ulysses`) and set to enable only that descriptor; the backup is copied back afterwards so the normal playset is unchanged.
