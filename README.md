<div align="center">

# PROJECT ULYSSES: CONTINUATION

### ROAD TO ITHACA · v0.3-dev

**A Strangereal grand-strategy campaign for Hearts of Iron IV 1.19 "Operation Postern"**

`CONTINUATION FORK` · `1991 — THE BELKAN WAR` · `UNOFFICIAL · NOT AFFILIATED WITH BANDAI NAMCO OR PROJECT ACES`

![Main menu](docs/screenshots/main-menu.jpg)

</div>
The project is intentionally separate from `G:\Project-Swallow`.

---

> **[ AWACS ]** All units, this is your eyes in the sky. The skies over Belka have been quiet for too long. The war that should have ended is back on the board — and this time, it runs on 1.19. Check your instruments and form up.

---

## ▌ INCOMING TRANSMISSION

**Project Ulysses** brought the world of *Ace Combat* — Strangereal — into Hearts of Iron IV: Belka, Osea, Ustio, Sapin, Gebet, Yuktobania and the rest, with their own map, histories, focus trees, decisions and superevents.

This repository is the **Continuation fork**. It picks up the April 2024 open alpha (v0.2, *Under Our Treads*), rebuilds it for **HOI4 1.19.3**, and carries the war forward. Like a pilot pulled from the sea and handed a new callsign, the mod gets a second sortie.

> This fork is not made by, or affiliated with, the original Project Ulysses team. All credit for the original mod belongs to them. *Ace Combat* and Strangereal belong to Bandai Namco Entertainment.

Open [Project-Ulysses.code-workspace](Project-Ulysses.code-workspace) in VS Code for portable, manual validation tasks; see [workspace instructions](docs/IDE_WORKSPACE.md). Antigravity has not been verified. The additive, default-off [experimental economy](docs/ECONOMY.md) provides treasury, budgets, bounded debt and a basic procurement contract with explicitly non-canonical calibration. Its runtime integration requires the separate repaired 1.19 port and original-content parity work. [Source attribution](docs/ECONOMY_PROVENANCE.md) is scoped to the new economy adaptation.
Open [Project-Ulysses.code-workspace](Project-Ulysses.code-workspace) in VS Code for portable, manual validation tasks; see [workspace instructions](docs/IDE_WORKSPACE.md). Antigravity has not been verified. The additive, default-off [experimental economy](docs/ECONOMY.md) provides treasury, budgets, bounded debt and a basic procurement contract with explicitly non-canonical calibration. Its runtime integration requires the separate repaired 1.19 port and original-content parity work. [Source attribution](docs/ECONOMY_PROVENANCE.md) is scoped to the new economy adaptation.

---

## ▌ OPERATION BRIEFING

| | |
|---|---|
| **Operation** | Road to Ithaca |
| **Theater** | Osean continent and the Belkan frontier, Strangereal |
| **Start date** | `1 January 1991`: *The Ring of Time* |
| **Engine** | Hearts of Iron IV **1.19.3** (Operation Postern) |
| **Status** | `SORTIE READY`: campaign starts and runs on 1.19 |
| **Primary objective** | A stable, fully playable 1991 Belkan War on the current game version |
| **Secondary objective** | Bring 1.15–1.19 systems into Strangereal, with Strangereal art only |

### Flight roster (nations with focus content)

| Callsign | Nation | Content |
|---|---|---|
| `GELB` | **Belkan Federation** | Start, election, DLP, war-won and war-lost trees; civil-war decisions; superevents |
| `GALM` | **Republic of Ustio** | Shared focus tree, decisions |
| `ESPADA` | **Kingdom of Sapin** | Pre-Belkan-War tree, balance of power, ideas |
| `SNOWFALL` | **Gebet** | Pre-Belkan-War tree, decisions |
| `WARDOG` | **Osean Federation** | Pre-Belkan-War tree, Osean Congress GUI, elections |
| `PIXY` | **A World With No Boundaries** | Shared focus tree |

All other Strangereal nations are playable with the generic tree.

---

## ▌ MISSION STATUS: 1.19 PORT

The original alpha targeted HOI4 1.13/1.14. On 1.19 it crashed at the main menu and failed to load the map. This fork's first sortie fixed that. Everything below was **verified in a live 1.19.3 campaign** (Belka, 1 Jan 1991 → Feb 1992, no crash):

| System | Status |
|---|---|
| Main menu | ✅ Original Project Ulysses menu: animated globe, Ulysses logo, `CONTINUATION FORK` label in the Aces font. No Paradox branding. |
| Scenario & country select | ✅ Original layout restored, 1.19-safe |
| Map load | ✅ Weather for all 326 strategic regions, 1.19 building spawn points, rivers palette fixed |
| Tech tree | ✅ Original modern-era trees (1973–2004), tabs working |
| National focus | ✅ Mod trees render; 1.19 continuous focuses available |
| Doctrines | ✅ Moved to the 1.17+ grand-doctrine system (Belka: Mobile Warfare · Osea/Ustio: Superior Firepower · Gebet: Grand Battleplan) |
| Experimental Facilities | ✅ 1.15+ special-projects tab present |
| Leader traits, abilities, buildings | ✅ Rebased on 1.19 rules (removed modifiers and effects migrated) |
| Crash-risk warnings in `error.log` | 24 → 2 |

Full engineering log: [docs/PORT_1_19.md](docs/PORT_1_19.md).

![Belkan Federation, 1 January 1991](docs/screenshots/in-game-1991.jpg)

---

## ▌ SORTIE PROCEDURE

1. Copy `mod/2985041246/` into `Documents\Paradox Interactive\Hearts of Iron IV\mod\`, or point a descriptor at this checkout (see [docs/WORKSPACE.md](docs/WORKSPACE.md)).
2. Copy `mod/2985041246.mod` next to it, then enable **Project Ulysses: Continuation** in the launcher. Don't run it alongside other total conversions.
3. Single Player → New Game → **1 January 1991** → pick your nation → **Start**.

> **[ AWACS ]** Recommended: run in a dedicated playset. This mod replaces the map, countries, history, units and AI templates wholesale.

---

## ▌ HANGAR: WHAT 1.19 BRINGS

| Feature | State in this fork |
|---|---|
| Grand doctrines and subdoctrines (1.17+) | Live. Starting doctrines set for the Belkan War powers. Subdoctrine bonuses for mod-specific units still need tuning. |
| Experimental Facilities / special projects (1.15+) | Facility spawn points on every province; the vanilla WWII project list still needs Strangereal replacements (superweapons are the obvious fit). |
| New buildings: naval HQ, supply hub, strongholds, facilities | Positions generated for the whole Strangereal map |
| Continuous focuses | Live |
| Main-menu background manager | Hidden. The original menu is used. |

---

## ▌ KNOWN BOGEYS

- **Vanilla art still visible** in places the mod never had its own art for (1.19 doctrine icons, continuous focuses, some building and tech icons). The goal is **zero WWII vanilla visuals**; these are tracked for replacement.
- `error.log` still carries vanilla-content noise: Earth country scripts that reference tags and equipment the mod removes. It's harmless at runtime but should be silenced with blank overrides.
- AI templates use deprecated 1.19 syntax (`roles`, `target_width`) and need a rewrite for the AI to build sensible divisions.
- Some ship and aircraft variants in country histories reference invalid name groups or module layouts (Sapin, FATO, the P-3 Orion).
- The postwar branches still end at the original demo terminal event (`world_event.2`).

---

## ▌ FLIGHT PLAN

```
PHASE 0  ▸ Baseline + 1.19 port ......................... COMPLETE: campaign starts and runs
PHASE 1  ▸ Clean 1991 Belkan War ........................ error-log cleanup, AI templates, OOB fixes
PHASE 1b ▸ Strangereal-only visuals ..................... replace every remaining vanilla sprite
PHASE 2  ▸ Postwar continuity ........................... replace the demo ending; Belkan victory / defeat branches
PHASE 3  ▸ Wider Usea and later wars .................... Yuktobania, Erusea, Usean conflicts; special projects as superweapons
```

> **[ AWACS ]** One war at a time. Today, Belka. Tomorrow, the whole of Usea.

Details: [Phased plan](docs/PHASED_PLAN.md) · [Next tasks](docs/NEXT_TASKS.md)

---

## ▌ INTEL ARCHIVE

| Document | Contents |
|---|---|
| [docs/PORT_1_19.md](docs/PORT_1_19.md) | What changed for 1.19 and why |
| [docs/WORKSPACE.md](docs/WORKSPACE.md) | Local layout, source archive hashes, dev-test setup |
| [docs/PHASED_PLAN.md](docs/PHASED_PLAN.md) | Development phases |
| [docs/NEXT_TASKS.md](docs/NEXT_TASKS.md) | Prioritized next tasks |
| [docs/CONTENT_INVENTORY.md](docs/CONTENT_INVENTORY.md) | Static content inventory |
| [docs/COMPATIBILITY_CHECKLIST.md](docs/COMPATIBILITY_CHECKLIST.md) | Compatibility checklist |
| [docs/TESTING_CHECKLIST.md](docs/TESTING_CHECKLIST.md) | Test plan and results |

---

<div align="center">

### ▌ DEBRIEFING

*Original mod by the Project Ulysses Development Team.*
*Continuation fork: unofficial, private, fan-made.*
*Not sponsored or endorsed by Bandai Namco Entertainment, Project Aces, or Paradox Interactive.*

`MISSION UPDATE: CAMPAIGN AIRBORNE ON 1.19 · RETURN TO BASE`

</div>
