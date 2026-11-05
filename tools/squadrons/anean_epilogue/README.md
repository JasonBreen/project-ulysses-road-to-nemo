# Anean continuations, 2015-2016 (`ac_sqa`)

Two six-chapter epilogues to pinned initial stories, ten years on, as the
Emmeria-Estovakia War begins or is avoided:

| Host | Epilogue | Continues | Cast by recorded conclusion |
| --- | --- | --- | --- |
| EMM | **What Tomorrow Inherits** (`open_corridor_after`, base 100) | *The Open Corridor* | trusted and compromised: all four; fractured: Anika Reeve and Dario Keene |
| EVA | **The Inspection Already Due** (`last_serviceable_after`, base 200) | *The Last Serviceable Aircraft* | trusted and compromised: all four; fractured: Nadia Orlov and Vera Dolin |

Original supporting fiction, not official lore; the original stories are read
and never edited. The writer brief is [brief.md](brief.md); the rules are
enforced by [epilogue_contract.py](epilogue_contract.py).

## How an epilogue opens

Only from the conclusion the player actually reached. The pinned initial
compiler records it as `ac_sq_<tag>_ending_<kind>`; the epilogue snapshots it
once, inside its window (2015.4.20-2016.12.31), into
`ac_sqa_<tag>_kind_<kind>`. Each chapter has one scene per conclusion, and a
conclusion's scene names only the people it left together; text shared by all
three (choices, callbacks, national context) names only the cast every
conclusion permits. No recorded conclusion, no epilogue; a save that first
reaches the host after the window is closed as a late archive.

Each scene is followed by one national paragraph, chosen when the scene is
delivered and then frozen: the war under way, Gracemeria fallen, liberation,
the coup, a ceasefire, a refused ceasefire, either outcome, capitulation, or
the routes on which no war came (withheld, divergent, unreachable). The
paragraph reads only the published Emmeria-Estovakia War record (`ac_eew_*`)
and the counterpart war relation; the scenes are true on every route. Choices
record personal flags only: no score, reward or national effect. A scene left
unanswered for 30 days, or when the window closes, is filed as missed;
annexation interrupts.

## Status: text and script complete, art awaiting generation, not admitted

Three scene masters per epilogue are planned in
[`../southern_art/plan.json`](../southern_art/plan.json) (portraits reuse the
original masters) and have not been generated, so `ADMITTED = ()` and the mod
contains no epilogue file. The compiled script is pinned in
[preview.json](preview.json).

```text
python -B tools/squadrons/anean_epilogue/epilogue_contract.py
python -B tools/squadrons/anean_epilogue/build.py --check
python -B tools/squadrons/anean_epilogue/test_runtime.py
```

Offline evidence only; native parsing and play are untested (#8).
