# Southern squadron stories (`ac_sqs`)

Two new original supporting stories for the 1991-2020 campaign:
Aurelia's **Kept in Repair** (base 900; Ciro Avellan, Lucia Ferro, Ines
Carvalho, Hector Mendaro) and Leasath's **Orders in Two Hands** (base 1000;
Mateo Salvaterra, Noemi Arcos, Gabriel Tenorio, Sofia Landa). Each has twenty
core chapters with two or three choices, four recurring people and three
personal conclusions. Incidents, dates, dialogue and personnel are authored
fiction, not official ACE COMBAT history; no official character, squadron or
weapon is a character, and no officeholder is appointed. The writer brief is
[brief.md](brief.md); the rules are enforced by
[story_contract.py](story_contract.py).

## Status: text and script complete, art awaiting generation, not admitted

The text, metadata and compiled script are complete and validated offline.
The thirteen art masters per story are planned in
[`../southern_art/plan.json`](../southern_art/plan.json) and have **not been
generated**: the authoring session had no image generator. So neither story
is admitted (`ADMITTED = ()`): the mod contains no southern file and no
placeholder picture. The compiled script is pinned as an offline preview in
[preview.json](preview.json) (per-file SHA-256) so the text cannot drift
silently. Admission steps are in [`../southern_art/README.md`](../southern_art/README.md).

## Compiler and runtime contract

[build.py](build.py) runs the pinned initial compiler (`tools/squadrons/build.py`)
with the Pacific component's default-preserving seams and renames everything
to `ac_sqs` / `ac_squadrons_southern`: numeric identity receipts, the
annexation interrupt, the 2020 admission horizon and the `ac_sq_stories`
rule. Act calendar: 1991-1999, 2000-2008, 2009-2019.6.30, 2019.7.1 onward
(the last act stays open so an admitted story can finish after 2020). A save
that reaches a host after an act closes files that act's chapters as missed,
without their choices; an unanswered scene expires after 30 days; annexation
interrupts; a host first reached after 2020 is closed without grants. Scores
start at 50/50: trusted needs both at 65, cohesion below 45 is fractured,
otherwise compromised. The trusted conclusion grants the existing modest
365-day debrief idea after an actually read scene; no choice pays money,
equipment, manpower or national effects.

Conditional scenes read only the published Aurelia-Leasath (`ac_alc_*`) and
Leasath civil-war (`ac_lcw_*`) records, the counterpart war relation,
capitulation and aircraft presence; the context is frozen when a scene is
delivered. Base scenes stay true whether or not any war happens.

## Checks

```text
python -B tools/squadrons/southern/story_contract.py
python -B tools/squadrons/southern/build.py --check      # source valid, mod clean, preview pinned
python -B tools/squadrons/southern/test_runtime.py       # compiled preview executed offline
python -B tools/squadrons/southern_art/plan.py --check
```

[harness.py](harness.py) is a small interpreter for compiled story scripts; an
unmodelled key raises. A test also runs the shipped Pacific stories through it
end to end (21 scenes per host, one description each). Offline evidence only; native
parsing and play remain untested (#8).
