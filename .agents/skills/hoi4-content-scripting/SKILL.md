---
name: hoi4-content-scripting
description: Extend Project Ulysses HOI4 events, focuses, decisions, ideas, flags, and follow-on branches using guarded repository conventions and static validation.
---

# HOI4 content scripting

Use this skill for event/focus/decision/idea/flag changes.

- Trace existing IDs and outcome flags before editing. For Belkan continuation, inspect `events\Belka.txt`, `events\ac_world_events.txt`, and the Belkan focus files.
- Use namespaced `ac_` IDs for shared continuation systems and avoid reusing archive IDs.
- Add the event/focus/decision/idea definitions, localization, and documentation as one contract. Guard effects with explicit flags and `fire_only_once`/completion flags where appropriate.
- Preserve existing alternate outcomes; do not replace the original Belkan tree simply to add a continuation hook.
- Use existing effect syntax as a model: `country_event`, `set_global_flag`, `set_country_flag`, `add_timed_idea`, `random_owned_controlled_state`, and timed decisions.
- Keep new prose explicit when it is a provisional gameplay branch. Do not represent unsupported postwar borders or future history as official.

Validation from the repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-UlyssesStatic.ps1 -ModRoot (Join-Path $PWD 'mod\2985041246')
```

Acceptance: no duplicate IDs, no unresolved owned references, no missing new localization keys, and no claim that static checks prove in-game reachability.
