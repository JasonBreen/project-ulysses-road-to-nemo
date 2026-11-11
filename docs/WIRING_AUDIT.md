# Wiring audit

`tools/wiring/audit.py` checks that the mod's script is wired together. Every flag
it reads is set somewhere, every event it fires exists and has a caller, and
every idea, character, decision, category, focus tree, shared focus, variable,
state and province it names is defined. `tools/Test-Wiring.py` runs the audit in
CI as a ratchet.

This is static source evidence. It does not show that any of this fires in game;
native behaviour stays under #8 and #70.

```text
python -B tools/Test-Wiring.py                 # unit tests on a synthetic mod, then the ratchet
python -B tools/Test-Wiring.py --record        # after fixing findings: lower the baseline
python -B tools/wiring/audit.py --report       # every open defect and warning
python -B tools/wiring/audit.py --report info  # also written-but-never-read, defined-but-unused
python -B tools/wiring/audit.py --reference-game-root <read-only HOI4 install>
```

## How it works

**`tools/wiring/index.py`** reads `common/`, `events/` and `history/`, together
with the localisation, `history/states` and `map/definition.csv`.
- Its brace-aware parser ignores comments and keeps line numbers.
- Unbalanced braces are reported as problems; the parser does not crash on
  them.
- Interpolated names (`$param$`, `[?var]`, `@TAG`) become patterns, so
  `ac_$what$_set` matches a read of `ac_alpha_set`.

**`tools/wiring/audit.py`** turns the index into findings at three levels:
- **defect:** something is read, fired or called but never written or defined,
  or guarded code does nothing;
- **warning:** probably unintended but harmless to the engine;
- **info:** written but never read. Info is reported but never blocks a change.

| Check | Level |
| --- | --- |
| `flag-read-never-set` (global, country, state, character) | defect |
| `event-undefined` (owned namespaces), `event-duplicate` | defect |
| `event-no-caller` (`is_triggered_only` with no caller in script or `on_actions`) | defect |
| `scripted-undefined` (an `ac_` or tag-prefixed `= yes` call that nothing defines) | defect |
| `idea-undefined`, `character-undefined`, `decision-undefined`, `category-undefined` | defect |
| `tree-unassignable`, `tree-load-undefined`, `shared-focus-undefined` | defect |
| `variable-read-never-set` (the mod's own variable names) | defect |
| `state-undefined`, `province-undefined` | defect |
| `empty-guarded-block` (an `if` that holds only its `limit`, with no `else` after it) | defect |
| `scripted-param-missing`, `shared-focus-unimported`, `loc-missing` (events and focuses) | warning |
| `flag-set-never-read`, `scripted-unused`, `idea-unreferenced`, `empty-else` | info |

**The mod's own names** start with `ac_` or one of its country tags (`BLK_`,
`sap_`). Names outside those prefixes belong to vanilla. Without a reference
install they are counted as unverified externals rather than findings.

With `--reference-game-root`, or `ULYSSES_GAME_ROOT` set, the audit also reads
the game's own definitions.
- It honours the descriptor's `replace_path` entries and same-path overrides.
- Vanilla names then resolve, and unresolved ones become defects.
- The CI ratchet always runs in mod-only mode, so its result is the same on
  every machine.

Sprites and art are left to `tools/overhaul/audit_consumers.py`. Focus
references and duplicate events are also checked by
`tools/Validate-UlyssesReferences.ps1`.

## Exceptions

`tools/wiring/allowlist.json` lists the reviewed exceptions. Each entry gives a
check, a name glob and optionally a file glob, a class, a reason and a source
layer.

| Class | Meaning |
| --- | --- |
| `external-unverified` | Vanilla's; resolve with a reference install (#4) |
| `inherited-inert` | From the archive or the vanilla template; does nothing and harms nothing |
| `intentional` | Works as designed |
| `tracked` | A known defect owned by an open issue |
| `owner-decision` | Needs the repository owner's content decision (TODO in source) |

An entry that matches nothing fails the test, so the list can only shrink.

## Ratchet

`docs/evidence/wiring/baseline.json` lists every open defect and warning.
- A finding that is not in the baseline fails the test.
- So does a baseline entry that has been fixed, until `--record` removes it.
- `--record` refuses to add new findings.

## First run (11 November 2026, branch `claude/content-planning-syzow6`)

The first run produced 402 defects and 264 warnings. After the reviewed
exceptions, 28 defects and 25 warnings remained:

- **AWW and SER release networks.**
  - Their finish effects hold an empty guarded block, so the projects end
    without repairing anything.
  - `ac_release_AWW_network_done` and `ac_release_SER_network_done` are never
    set.
- **Sapin.** Seven flags gate decisions, categories and events that nothing
  sets: `sap_political_crisis_over` (10 reads), `SAP_has_mobilized`,
  `SAP_politics_calmed`, `sap_imminent_civil_war_flag`,
  `sap_imminent_republican_revolt_flag` and `sap_urf_split_flag`.
- **Belka.** `BLK_excalibur_fire_aa_flag`, and the achievement flag
  `used_excalibur_on_hoffnung_achievement`.
- **Ideas.** `BLK_grunder_air_designer` and
  `sap_improved_laser_guidance_systems` are referenced but not defined.
- **Events.** 14 events are `is_triggered_only` but have no caller: Osea 3,
  Belka 3, Ustio 2, `ac_war_events` 2, AWW, Gebet, Sapin and `world_event.2`.
- **Text.** 25 event text keys are missing.

These are fixed in batches (plan Part A2). Each fix lowers the baseline.

## Repairs (11 November 2026)

The baseline is now **0 defects and 0 warnings**. Each fix below is mod
provenance: it makes inherited content do what it plainly intends. Nothing new
is invented.

| Finding | Repair |
| --- | --- |
| AWW and SER network repair: decision visible but never available; empty finish block | `tools/release_foundations/network.py`: a release whose recorded footprints are already fully connected gets a hidden decision, an `always = no` availability and no done flag. The empty block is no longer emitted. Outputs and the dormant-release inventory are regenerated. |
| `SAP_has_mobilized` never set, so `SAP_demobilize` never appears | National-guard mobilisation sets it (`SAP_decisions.txt`). |
| `sap_political_crisis_over` never set, so the `sapin_politics.3`–`.13` chain re-arms forever | Set when either civil war starts (`sapin_civil_war.1`/`.2`). |
| The Sapin civil-war category opens only on a flag nothing sets, so its recruitment decision (which needs `has_civil_war`) is unreachable | The category also opens during a civil war. |
| `used_excalibur_on_hoffnung_achievement` never set | The Excalibur land-strike button sets it when the target is Hoffnung (state 602) during Wacht am Wal, matching the achievement text. |
| `BLK_excalibur_fire_during_aa` activation read an unset flag | `always = no`; the decision activates the mission directly. |
| `BLK_grunder_air_designer`, `sap_improved_laser_guidance_systems` undefined | Removed the dead references. The Gruender MIO replaced the designer, and the laser focus grants no idea. No change to the outcome. |
| Six live events showed raw keys (`belka.8`, `belka.9`, `belka_dlp.5`, `belka_dlp_coup.8`, `osea.80`, `ustio.19`) | `localisation/english/ac_wiring_repairs_l_english.yml` states what each effect does. |

**What remains in the allowlist, each with a reason:**
- uncalled archive stubs and debug events;
- the `owner-decision` items, which wait for a content choice:
  - `belka_l_monarchy.1`, `gebet_election.2`, `sapin.1` and `ustio.21`;
  - the Sapin imminent-revolt mission and `SAP_politics_calmed`;
  - the `glrdc_good_flag` branch.

**Belkan defeat flag:** `belka_lost_belkan_war` is set by `belka_dlp_war.103`
and `belka_dlp_lost.7`. It is read by `ac_dispatch_belkan_war_outcome`,
`ac_continuation.1` and the campaign decisions. `tools/validate_campaign.py`
reports 0 errors.
