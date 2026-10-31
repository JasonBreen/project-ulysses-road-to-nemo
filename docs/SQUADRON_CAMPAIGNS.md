# Six original squadron campaigns — Package 2

Six independent stories accompany national play from 1991 to 2005. Each has twenty
core chapters, four recurring original characters, forty consequential choices
and three substantive personal conclusions. This delivers 120 core chapters,
24 cast members and 18 conclusions. The additional twenty-chapter Osean,
Yuktobanian, Aurelian and Leasathian campaigns belong to later release packages.

| Host | Story | Recurring cast | Personal and professional conflict |
| --- | --- | --- | --- |
| Belka | Cold Orders | Leonie Falk, Markus Voss, Eva Heller, Tomas Wendt | Reserve service, dangerous instructions, loyalty and the account left afterward. |
| Ustio | Last Road Home | Mara Dalen, Elias Vey, Niko Arven, Irena Sorel | Survival, civilian routes, obligations to people waiting and the meaning of returning. |
| Erusea | The Narrow Sea | Adrien Valcourt, Celine Marot, Bastien Roux, Lise Armand | Maritime uncertainty, professional rivalry, civilian contacts and the record of an order. |
| San Salvacion | Empty Frequency | Elena Neris, Rafael Caro, Mina Vale, Oren Serra | Warnings, maintaining contact, family care and handing responsibility to another person. |
| Emmeria | The Open Corridor | Anika Reeve, Jonas Mercer, Sera Vale, Dario Keene | Generosity, domestic duties, safe maintenance and promises that another crew must sustain. |
| Estovakia | The Last Serviceable Aircraft | Nadia Orlov, Pavel Kresin, Vera Dolin, Milan Sarek | Scarcity, injury, care, compatible assistance and honest definitions of readiness. |

These casts are **user-approved original supporting fiction**. They are not
newly asserted official people, replacements for government officeholders, or
additions to protected private continuity. Existing national leaders and office
cards remain unchanged. No official cameo is invented to connect the stories.
Supporting family bereavements and Pavel's injury are authored personal events;
the four core people in each first-wave campaign remain alive. Future service,
retirement, loss and return need their own reviewed continuation records.

## Choices and continuity

Every core scene has two consequential choices and an authored response. Country
flags retain individual promises and professional decisions; earlier choices
return in contextual dialogue. Separate 0–100 cohesion and credibility measures
start at 50. Many choices protect one at the expense of the other. Neither button
consistently represents the morally correct choice. Breadth-first score checks,
followed by execution of actual authored option effects, establish that all three
conclusions are reachable in every campaign, including mixed-choice trusted paths.

- Trusted: cohesion and credibility both at least 65.
- Fractured: cohesion below 45, unless the trusted condition is satisfied.
- Compromised: the remaining personal outcomes.

Only a trusted conclusion after actually reading eligible material grants a
temporary 365-day 2% air-experience benefit. There are no historic equipment,
factory, treasury, preparation or political-power grants. The stories do not
claim telemetry for individual HOI4 wings or remove aircraft to represent a
personal incident. Real observed national air-service manpower gates airborne
wartime descriptions; ground and personal continuations remain useful without it.

All 120 base scenes have received a capability fallback review. Fresh military
flying uses an observed-capability continuation; ground exercises, shore radio
work, planned duties and personal journeys remain available without an active
air service. BLK chapter 8 keeps its original peaceful exercise return behind
no-war/no-capitulation/air-service conditions and uses an explicitly simulated
landing as its ground baseline. The complete package has fifteen condition
variants in addition to nine wartime and nine capitulation continuations. This
is authored supporting fiction, not telemetry for individual aircraft.

Scenes also read actual capital/district control, bilateral faction membership,
Stonehenge destruction, the Anea accord and actual sanctions policy. These
conditions change written continuations without changing the underlying war,
faction, project, aid or sanctions state. The event captures its displayed
context and prior-choice callback at delivery. Reading it from the archive later
replays that text without applying an option again.

The source files `tools/squadrons/chapters/TAG.json` retain the prose, options,
callbacks, date gates and conclusions. `campaigns.json` records cast and act
windows. These are the editable narrative sources; generated localization is
not the authoring copy. The compiler commits the full descriptions rather than
shortening them to conceal a layout defect. Repaired scroll behavior remains a
separate interface/native acceptance contract.

## Calendar and interruption

The four five-chapter acts use host-appropriate windows. Belka/Ustio split at 1995,
1997 and 2000; Erusea/San Salvacion at 1995,2000 and June 2003; Emmeria/Estovakia at 1998,
2000 and 2003. Within an act, authored dates and a thirty-day reading interval
pace scenes. Dates are gameplay scheduling, not additional official events.

One thirty-day reservation owns one scene ID. An unanswered reservation expires
as missed without choice effects; it cannot be reissued as the same event ID.
Stale events cannot clear a newer reservation. Annexation and restoration cannot
repeat a choice; current and original tags both bind the owner. Pause stops
automatic scenes and conclusions; a manual action can open an eligible scene
or the final assessment. Ordinary weekly callbacks have country scope and do
not iterate the whole world once per country.

Late initialization after January 1991 skips the opening. Expired acts are marked
missed without relationship or national rewards. Initialization after 2005 closes
an unread archive; it does not reconstruct a fictitious service history. An
already active final act can finish after 2005, and its conclusion stays reachable.
Opening the archive, a cast card or a tooltip is financially and politically pure.
The optional fiscal and faction-council settings do not own story eligibility.

## Provenance and campaign ownership

| Material | Source layer | Affected content and boundary |
| --- | --- | --- |
| All original casts, dialogue, family relationships, personal incidents, choices, endings and chapter dates | Approved original supporting fiction | `tools/squadrons/campaigns.json`, `chapters/*.json`; `ac_sq` events, flags and variables. No official biography or city mapping claim. |
| Belkan War and Ustian restoration backdrop | Official history: [ACES Chronicle](https://acecombat.jp/en/chronicle/details/),1995 entries | Context only. Existing campaign owners determine whether the authored alternative actually reaches war, defeat or peace. No story schedules a compulsory canonical battle. |
| Ulysses warning/crisis and Usean conflict backdrop | Official history: same chronology,1994/1996/1999 and 2003–2005 entries | Read through existing regional owners; no newly asserted exact impact timestamp, casualty map or compulsory territorial outcome. |
| Stonehenge | Official technical history: [Super Weapons Chronicle](https://acecombat.jp/en/chronicle/weapons/), Stonehenge section; inherited implementation: `ac_ucw_stonehenge_destroyed` | Descriptions read the owner's destruction flag and district 310 control. No story constructs, operates, captures or destroys the installation. |
| Anea aid and sanctions | Official chronology,2000 and 2002 entries; inherited `ac_anea_accord` and `ac_anea_sanctions_active` | Personal consequences follow the actual policy. A squadron cannot offer unlimited aid or repeal sanctions. |
| Capitals, tags, faction membership and national capabilities | Existing mod provenance | Source maps and governments remain with their owners. Capital-displacement variants use the existing BLK 224 and UST 335 districts, not new canonical locations. |
| Portraits, scenes and loading screens | Original generated artwork, with retained individual production records | `sources/*/*.png` and matching JSON record exact prompts, selected source, dimensions, hash and individual review. Official AC8 presentation remains separate. |
| Category/spirit geometry | Original code-native artwork plus established flags | `build_art.py`; no installed-game pixels or invented national emblems. |

## Artwork and reproduction

The complete artwork gate requires 24 portrait masters,48 narrative masters and
six independent loading compositions. Related chapters share explicitly mapped,
outcome-neutral scenes; the three personal endings use each host's quiet airfield
composition rather than an image asserting victory or destruction. Loading
screens are separately composed sources, not enlarged event crops. Individual
records preserve corrective image edits and the source masters stay in the
repository rather than depending on a generator cache.

Packaging produces 115 DDS textures:24 portraits at 156×210,24 cast event cards and
48 scene cards at 200×160, six 1920×1080 loading screens and their 192×144 picker
thumbnails, six 100×100 category icons and one 75×75 spirit icon. All use deliberate
single frames. Images use opaque navy containment to retain entire heads and
scenes; the category/spirit silhouettes retain transparent outer corners.
The assets manifest records dimensions, frames, alpha requirements, bindings,
source hashes and 120 chapter-to-scene mappings. The gallery exposes every full
master and country contact sheets for composition and artifact review.

Use Python 3.12 with Pillow 11.3.0 for reproducible packaging:

```powershell
python -B tools/squadrons/build.py
python -B tools/squadrons/build_art.py
python -B tools/squadrons/build.py --check
python -B tools/squadrons/build_art.py --check
python -B tools/Test-SquadronStories.py
python -B tools/Test-SquadronArt.py
python -B tools/audit_visual_dependencies.py --strict-all
```

`build_art.py --gallery-only` can review an incomplete production batch without
writing mod assets. It states its incomplete status and is not the full artwork
gate. The final gate requires every selected master. Tool output and acceptance
records must state whether the complete package or a partial gallery was checked.

The runtime suite uses the existing fail-closed Continental War interpreter,
extended for current/original identity, event delivery and read-only archives.
It executes the authored scripts and rejects unknown behavior. A synthetic
weekly 1991–2006 calendar is an offline schedule test; copied-state reloads are
not native save serialization. Native aircraft observations, GUI controls,
long-text scrolling, display configurations, AI reading/pacing, actual game saves
and all visual acceptance remain untested while native testing is paused.
