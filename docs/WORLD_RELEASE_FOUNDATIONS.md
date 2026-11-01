# Nonlandowning country setup: inherited contracts and pending work

The 61 active-country foundation checkpoint does not establish released-country
acceptance. These seven inherited histories own no state at the 1991 start.
They receive no blanket army, industrial, resource, fiscal or old-save grant from
WorldStarts. The following observations describe mod provenance, not official
chronology. `tools/world_starts/release_inventory.json` records exact source
inputs and reproduces the literal event/caller/OOB inventory.

| Tag | Existing authored entry/force contract | Established once protection and remaining source gap |
|---|---|---|
| AWW | `events/AWWNB.txt`: `awwnb.1` transfers state 272, inherits BLK technology and takes 25% of BLK's non-naval units; it dispatches `awwnb.2`, which loads `AWW_land` (9 additional formations). | No literal caller of `awwnb.1` was found in the scanned event/focus/decision/on-action/effect source. Neither entry event declares `fire_only_once` or a shared force-setup flag. The existing OOB has no production queues. Reachability, repeat protection, DLC replacements and a lawful release-time logistics/resource/fuel owner remain pending. |
| REC | `events/Belka.txt`: `belka.9` dispatches `recta.1` to GEB after 90 days. `events/Recta.txt` transfers 345/300/316, conditionally 293, inherits GEB technology and loads `REC_land` (10 formations). | `recta.1` has no explicit setup-once flag; its OOB has no production queues. Later Belkan treaty/continuation transfers can re-establish REC through different territorial paths without calling this event. A release owner must distinguish those existing routes and avoid duplicate or retroactive preparation rewards. |
| SBK | `events/South_Belka.txt`: `south_belka.2/.3/.4` transfer 330/369/302/8/364, inherit BLK technology, and transfer respectively 25/25/15% of BLK's non-naval units. Weekly human/AI collapse conditions call `.2/.4`; `BLK_belkan_war_collapse` mission timeout calls `.3`. | Each of the three events is individually `fire_only_once=yes`. That does not demonstrate a shared group setup guard across different entry events. Belkan defeat/armistice events also create SBK through a different state settlement without the same troop transfer. There is no direct SBK OOB or reviewed replacement/logistics setup owner. |
| REL | History and generic political/fiscal profiles exist. | No authored release/setup event owner or tag-prefixed OOB was identified. A legitimate entry contract must precede any physical setup. |
| SER | History and generic political/fiscal profiles exist. | No authored release/setup event owner or tag-prefixed OOB was identified. A legitimate entry contract must precede any physical setup. |
| SHI | History and generic political/fiscal profiles exist. | No authored release/setup event owner or tag-prefixed OOB was identified. A legitimate entry contract must precede any physical setup. |
| TER | History and generic political/fiscal profiles exist. | No authored release/setup event owner or tag-prefixed OOB was identified. A legitimate entry contract must precede any physical setup. |

RAT is the active Ratio country and already belongs to the WorldStarts owner. It
is not an eighth dormant tag. The registered South Belka tag is **SBK**; there is
no registered `SBL` country history. PLH/state 171 remains an unresolved placeholder
and receives no inferred geography or release contract.

The inherited AWW/Recta/South Belka events remain unchanged. This inventory does
not fix or silently replace their war, border, faction, leader, political or
unit-transfer behavior. A later narrow release foundation must use the legitimate
owning outcome, inspect actual retained territory and surviving forces, grant
only missing eligible capability once, and define interrupted/annexed/released
behavior. It must preserve the existing campaign and save contracts instead of
loading a generic 1991 start into a newly released country.

Existing country histories, government-office representation and macro profiles
are not evidence that their release-time forces, production, trade or transport
work. Native release, random unit transfer, source-event reachability, re-release,
save/reload, AI growth and physical throughput are untested. Generic engine
release UI behavior is not substituted for an authored/accepted entry contract.

Reproduce this read-only source inventory with:

```powershell
python -B tools/world_starts/release_inventory.py --check
```
