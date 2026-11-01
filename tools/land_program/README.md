# Conventional Land Systems, 2006–2020

This is an additive source/offline packet based on `224c9ccb23f7745d1829b334c5f901c897e83c72`. It introduces 32 research commitments, 40 concrete equipment definitions, 36 designer modules and two supplied support companies. It does not grant early research or equipment, replace existing starting formations, or complete the whole military conversion.

All new names, dates, industrial costs, materials and statistics are **provisional gameplay**. They are not claims about official ACES hardware, procurement programmes or real military specifications. No new lore-sensitive individual, national identity, war, strategic project or territorial change is introduced.

## Authoring and reproduction

Run from the repository root with Python3.12 and the CI-pinned `Pillow==11.3.0`. Text generation and the primary worksheet use the standard library. Packaging and offline font reconstruction use Pillow. Nothing requires a commercial editor or installed game to reproduce from the committed primary contract.

```powershell
python -B tools/land_program/build.py
python -B tools/land_program/build_ui.py
python -B tools/land_program/build_art.py
python -B tools/land_program/audit.py
python -B tools/land_program/render_review.py
python -B tools/economy_v2/build.py
python -B tools/land_program/test_land.py
```

Each authoring script accepts `--check`. The audit verifies captured effective mod hashes even without an installed reference. Refresh primary facts explicitly only after reviewing actual changes:

```powershell
python -B tools/land_program/audit.py --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/land_program/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --core
```

`run_checks.py` writes only this packet's evidence directory and runs at most two source checks concurrently. It does not launch HOI4. The engine argument is a read-only loose-file reference; it does not prove active DLC or runtime acceptance. `--only` accepts comma-separated check names for rerunning a changed or failed gate while retaining the other results.

The source files have distinct roles:

- `land_content.py` declares eight families, four tiers, dependencies and module recipes.
- `build.py` generates technology, equipment, support units, AI and English localization.
- `build_ui.py` adds the real research folder, tab and templates. Its captured pre-change GUI remains in `source/research_base.gui`; normalization removes only the declared additions and two description-scrollbar properties before comparing the whole old AST.
- `build_art.py` is the editable geometric master. It also exports 68 editable SVGs and packages 106 RGBA8 DDS textures with 158 sprite bindings. `assets.json` records dimensions, frames, alpha, hashes and provenance. Shared physical default legacy/designer variants intentionally share their vehicle art. Research cards use 112×40 icons, equipment 192×96, modules64×64, support counters two frames at76×42 or30×12 per frame, and the tab four89×30 frames. Alpha below4 is removed after Lanczos downsampling to prevent invisible bright-color fringe.
- Offline gallery labels use the shipped raster font atlas, avoiding operating-system TrueType rasterization. Review PNG checks require identical dimensions and RGBA pixels; delivered DDS and editable/binding sources retain exact-byte checks.
- `audit.py` captures effective definitions, validates paid physical routes and produces `capabilities.json`. Its arithmetic is a source comparison, not an engine simulation.
- `render_review.py` reconstructs the shipped new page using actual GUI coordinates, sprites, localization and ACBriefing BMFont glyph advances/kerning. It fails on text or bounds findings. Its deliberately labelled PNG is an offline review artifact.
- `preserved_sources.json` pins the inherited technical/history payload used by the 61 current starts. A separately reviewed owner changing those sources must be composed explicitly; do not refresh hashes merely to make a test green.

## Research and production contract

Each family has nodes dated2006,2010,2015 and2020. Every node has a paid research cost, an explicit hard date gate, engine dependencies and real equipment/effect unlocks. Later tiers require their preceding tier. The first tracked-artillery programme requires the first battle platform; later artillery requires the corresponding platform tier. Earlier industrial/support/reconnaissance foundations remain useful and are not silently researched for the player.

| Family | Physical use | Enduring requirement |
|---|---|---|
| Infantry Systems | Native infantry-equipment archetype | Steel/aluminium and delivered replacements |
| Protected Mobility | Native mechanized-equipment archetype | More costly vehicles, crews and fuel |
| Battle Platforms | Modern armor | Steel/chromium/tungsten, fuel and actual production |
| Tracked Fire Support | Tracked-artillery role | Separate funded vehicle production and supply |
| Combat Services | Native support equipment plus engineering/maintenance improvements | Manufactured service sets and trained support |
| Distribution Systems | Native trucks plus logistics-company improvements | Physical trucks, delivered fuel and infrastructure |
| Field Surveillance | A specialist reconnaissance company and sensor gear | Crews, sensors, trucks and support sets |
| Electronic Support | A specialist signal-support alternative and electronics | Crews, electronic sets, trucks and support sets |

With No Step Back disabled, each platform tier unlocks one complete legacy-format vehicle. With it enabled, the same technology unlocks a modular chassis and its necessary researched components. The two production gates are mutually exclusive. All eight default modular recipes have validated required slots/categories and exactly match their complete counterpart's source cost, resources, fuel, manpower and combat statistics. Creating a design and paying XP/production remain native actions; a research unlock supplies no vehicles. Optional configurations can differ and do not inherit a universal parity claim.

At2020 the default battle platform costs53IC and uses5steel/3chromium/2tungsten per assigned line factory; tracked artillery costs50IC and uses5steel/2chromium/2tungsten. Resource coefficients describe continuing factory input, not a bill consumed once per vehicle. The worksheet's one-MIL/30-day calculation assumes a clearly labelled50% reference efficiency and the captured base factory speed; no national output, trade capacity, fuel tempo or actual production time is certified by that reference.

The surveillance company competes with other reconnaissance support through `same_support_type=recon`; the electronic company competes with signal support. Neither creates strategic map intelligence, air jamming, radar suppression or a strategic weapon. The reconnaissance company benefits from retained recon-category training. The electronic company's base initiative0.5 avoids being inferior to the retained signal company's0.1 plus three0.12 upgrades. Higher-tier specialist benefits cost further research and physically produced replacement instruments. Both companies use real manpower, supply, eight trucks and15support sets, plus10sensor or12electronic sets respectively.

## AI and fiscal ownership

Research priorities activate after2005. New designer groups have zero effective priority before2006 or before their first relevant technology. Their designs require the dated researched chassis/modules; they do not create a free national variant or early design. An optional AI support role requires more than12MIL and actual stock buffers above100sensor/120electronic sets. A bounded native archetype-production strategy requests one MIL per empty specialist buffer before a supplied template becomes eligible. This competes for existing industry; it is not a capacity grant or proof of natural AI behavior.

The optional full target also requires researched engineer/logistics companies and at least610infantry equipment,80support equipment and26trucks. Those minima cover the actual six-infantry-plus-four-support target; its enable, field-upgrade and role guards check the same complete requirement. Tests derive the needs from actual unit definitions and reject every missing required technology or equipment family. Equipment priorities increase above their actual inherited parents, including the legacy modern tank's170: the new complete models use200/210/220/230, and designer chassis use2100/2110/2120/2130. These are authored ordering contracts, not proof of native replacement choices.

The existing macro owner retains all cost formulas and coefficients. Infantry, trucks, carriers, service sets and platforms inherit its already covered archetypes. The only shared change adds the two genuinely separate instrument archetypes to its existing support pool at the same provisional coefficient. The packet ships those definitions and queries together. Company crews/trucks/support gear remain distinct costs. Armor still uses `max(parent observation, sum distinct child observations)` within each family, so a parent including artillery does not also charge that child twice. The tests execute actual `FiscalWorld` effects and confirm positive specialist cost, additive support instruments, overlap protection and disabled-fiscal inertness. Native equipment-query aggregation/precision remains unverified.

The separately owned release-foundation generator can also change macro initialization. Integrate by composing its generator changes with this observation data and regenerating `ac_macro_effects.txt`; do not choose one generated file and lose the other owner's work.

## Remaining presentation and hardware work

This packet **does not remove the inherited land tabs**. `capabilities.json` inventories their exact effective IDs, dates and files. On this captured base:

| Retained folder | Effective nodes | Dated before1950 | Disposition |
|---|---:|---:|---|
| Infantry |46|43|Still reachable; inherited weapons, uniforms and other labels remain to convert |
| Support |33|1|Still reachable; existing1991–2000 support progression remains useful |
| Armor |14|14|Still reachable; inherited1918–1945 path and labels remain backlog |
| Artillery |28|27|Still reachable; one node has no explicit year, and inherited gun labels remain backlog |
| Electronics |29|0|Still reachable; six nodes have no explicit year; inherited electronics/radar progression remains |
| Old NSB Armor |0|0|Explicitly unavailable compatibility folder; `NSB_armor.txt` remains fully commented |

Examples still present in actual effective localization include `gwtank` = “Great War Tank,” `infantry_weapons2` = “Improved Infantry Equipment I,” and inherited `interwar_artillery`/`artillery2` names. Leaving those controls stable avoids silently deleting the current countries' prerequisite/research contracts. Their future conversion requires its own equipment and national-start migration review. The new LAND page cannot be represented as closure of that backlog.

The new companies deliberately retain the existing infantry map entity until an original compatible3D model is authored. Native3D land models, animated attachments, legacy counters outside these two new units, historical MIO identities and older research images are separate presentation work. Air, naval, missile, strategic-weapon, intelligence-agency and operational electronic-warfare families are outside this conventional land packet. Post2020 and campaign end-date contracts are unchanged.

No research search control exists in the captured effective GUI or the installed1.19.4.1 GUI. The new page retains real left/middle drag, wheel scrolling and native vertical/horizontal scrollbar bindings. No decorative unbound search field is presented as functional search.

## Acceptance boundary

The retained results distinguish source checks, actual-owner interpreter fixtures, primary loose-file comparisons, original-art inspections and offline GUI reconstruction. None is a native screenshot, live designer test, natural AI run or save/reload result.

When native testing is separately resumed, test the following without changing the normal installation or saves:

| Area | Required native coverage |
|---|---|
| Displays |3440×1440/1.0,1920×1080/1.0,2560×1440/1.25; tab discovery, all32nodes, detail scroll, drag/wheel/horizontal scroll, tooltips, research states and keyboard controls |
| DLC |No Step Back on/off; independent BBA/MTG/LaR on/off. Source tests enumerate all16switch combinations; native activation is not inferred from them |
| Research |Natural2006/2010/2015/2020 checkpoints and separately labelled shortcut coverage; prerequisites, actual completion time, locks and no late-load grants |
| Production |Complete-vehicle route; researched modular chassis, default and optional slots, paid XP/design creation, line/resource/fuel costs, upgrade/replacement delivery and old recipes |
| Support |Correct division support-slot exclusion, actual equipment shortages, reconnaissance/initiative/supply/fuel effects, selection frames and map entities |
| Economy |Native equipment-query observations for the custom archetypes and parent/child chassis; enabled/disabled fiscal modes; no duplicate bill or stockpile charge |
| AI |Research choice, XP/template creation, two paid buffer lines, affordable retained national queues, natural supplied-role selection and replacement pacing |
| Saves |New1991campaigns, old campaign before/after2006, current research at save/reload, completed old technologies, missing prerequisites and reload with different eligible future nodes |

Native testing, desktop control, installation synchronization, merging, publication and release acceptance remain separate actions.
