# Canon and provenance ledger

This ledger is a work queue, not a claim that the entries below are settled. Official-source links are preferred for official-canon claims; the mod archive is retained as provenance only.

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Strangereal is the shared fictional setting across numbered ACE COMBAT stories | Official | [ACES official site](https://acecombat.jp/) | Confirmed at the setting level; use official title materials for individual dates and borders. |
| ACE COMBAT Zero / Belkan War as source context | Official | [ACES official archive](https://acecombat.jp/) | Confirmed as official title context; this does not validate every mod event or date. |
| April 5, 2024 Project Ulysses archive content | Mod provenance | Immutable archive SHA-256 `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071` | Preserved and audited; not official-canon proof. |
| 1991 bookmarks and existing Belkan branches | Mod provenance | Archive and current static inventory | Preserve/adapt with provenance; verify reachability and chronology at runtime later. |
| Joker 1: Ustian birth, Belkan connections, Moon11/Shadow22, Watchtowerorganization, Cope, and Tasha's mother shooting him down | User-authored continuity | The supplied planning outline | Approved creative layer, not official canon; compile exact dates/details from the author before implementation. |
| 2065-12-31 inclusive campaign cutoff | Project requirement / provisional engineering contract | `docs/DESIGN.md` | Engine permission, authored content, and runtime coverage must be reported separately. No invented future lore. |
| Ulysses fallout and Usean Continental War, 1999–2005; Stonehenge, Megalith, Excalibur, V2 and Arkbird project framing | Official | [ACES Chronicle details and Super Weapons](USEAN_CONTINENTAL_WAR.md), accessed 27 Oct 2026 | Sources and actor contracts compiled; nothing implemented yet. The war's start day, Megalith's construction timing and every alternate outcome are provisional gameplay. Recta has no Chronicle entry and stays mod provenance. |
| Technology/equipment names through 2065 | Mixed / pending | Current files are mostly inherited IDs with 1991–2005 dates; date syntax validator now covers 1900–2065 | Audit names, localization, provenance, and canon conflicts before adding later-era content. |
| Skully Islands rebel base, 31 December 1995, and the Usean coup, 30 May 1997 | Official for the Chronicle sentences; provisional gameplay for the prolonged emergency and the modifier values | [ACES Chronicle](https://acecombat.jp/en/chronicle/details/), 1995 / 12.31 and 1997 / 05.30. IDs `ac_ur.1`–`.4`, `FCU_ur_*`, `ac_ur_coup_strain` | Implemented in script and static checks. Robert Tyler and Scarface are named only as the Chronicle names them. No rebel country list, no border change, no native test. |

## Flight-cadence campaign

The flight-cadence slice separates its one official chronology input from the
authored national programs and their gameplay rewards.

| Claim or contract | Source layer | Exact reference | Affected IDs | Implementation / validation status |
| --- | --- | --- | --- | --- |
| Ulysses reaches the Roche limit on 8 July 1999 | Official chronology only | [ACES Chronicle details](https://acecombat.jp/en/chronicle/details/), entry `1999 / 07.08`, checked 1 November 2026 | `ac_flight_ulysses_clock`, `ac_flight_planetfall_resolved`, `ac_flight_cadence.3` | Used as the campaign handoff date. It is not a claim that every local impact or national response happened at that instant. |
| The 1991 bookmark and the existing Osea, Yuktobania and Erusea tags | Mod provenance for the inherited start and identities; provisional gameplay for selecting these three participants | April 2024 archive SHA-256 recorded above and the current 1991 bookmark; [PR #64 design contract](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/64), 1 November 2026 | `ac_flight_cadence_cat`, `ac_flight_program_open`, `ac_flight_cadence_on_actions` | The three launch programs are authored for this slice, not official national history. Belka is deliberately excluded. |
| Static fires, success loss, three-success cadence, pad construction and their political, stability, technology and research values | Provisional gameplay | [PR #64 summary and test plan](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/64), implemented in `cd76d9d1` | `ac_flight_static_fire`, `ac_flight_static_fire_effect`, `ac_flight_success`, `ac_flight_claim_cadence`, `ac_flight_cadence`, `ac_flight_raise_a_pad`, `ac_flight_pad_raised`, `ac_flight_cadence.1`–`.2` | Authored mechanics with offline/static regression coverage. No launch cadence, failure rate, national institution, pad location or balance value is presented as sourced setting history. |
| Stonehenge-complete response and Osea's Arkbird research head start | Existing mod contract for `ac_sp_stonehenge_complete`; provisional gameplay for the response and bonus | Existing special-project scripts at the PR base; [PR #64 design contract](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/64), 1 November 2026 | `ac_flight_cadence.3`, `ac_flight_sky_held`, `ac_flight_we_flew`, `ac_flight_arkbird_head_start` | Reads the existing Stonehenge flag without changing Stonehenge, Megalith or Arkbird. The response, modifiers and bonus are authored. Native parser, UI, timing, save/load, AI and balance acceptance remain open. |

## The Peace We Inherit expansion

The [expansion source and implementation ledger](PEACE_WE_INHERIT.md#sources-and-authored-branches)
records exact official Chronicle entries, affected IDs and adaptations for Lumen,
AWWNB, the 1996 Rald/Blauvelt reference, the FCU warning, former Belkan aggressor
instructors and Ulysses in July 1999. All four slices are authored in source;
postwar policy, pressure indices, reconstruction accords and humanitarian response
calculations are **provisional gameplay**. Existing victory/Wacht/defeat, monarchy,
Ratio and annexation behavior remains **mod provenance**. Native gameplay and
save/load acceptance remain open; the [24 October native report](NATIVE_PEACE_WE_INHERIT_20261024.md)
records isolated fixture coverage and remaining gaps without changing source layers.
No Joker 1 details, future wars, new borders,
or unsourced local impact zones were inferred.

## Citation rule

The [Pacific personal-story ledger](PACIFIC_STORIES_LEDGER.md) separates the
official cold-war, 1999 Arkbird-cooperation and 2010 conflict context from the
original Osean and Yuktobanian casts, incidents and chapter dates. Those personal
stories are authored fiction and provisional gameplay. They read national
capabilities and actual relations without controlling war or project outcomes;
their people are never substitute national officeholders. Source, offline and
native acceptance remain separate.

The Anea foundation's [source and implementation ledger](ANEA_EXPANSION_LEDGER.md)
records the1998 Anean risk/shelter entries,2000 aid,2002 sanctions,2004 agency
and incomplete Chandelier separately from provisional gameplay. No1991 named
officeholder, canonical provincial geography, civil-war outcome or later
invasion is inferred. Territory and inherited manpower remain mod provenance.

Do not promote a row from pending to official based only on a wiki, fan archive, old mod file, or an unreferenced comment. If no primary source is available, retain the row as user-authored, mod provenance, or provisional gameplay and say so in the implementation note.

## Faction and council systems

The [faction provenance ledger](FACTIONS_PROVENANCE.md#canon-ledger) classifies ac_fac_, ac_corp_, ac_sub_ and ac_factions.1–.3 additions as provisional gameplay, records the exact OEM reference/license and private request, and lists inherited files preserved. No canonical alliance, corporate history or future event is asserted. See [system/DLC mapping](FACTIONS.md) and [validation status](FACTIONS_VALIDATION.md).

## 2026-10-30 starting-government repair

Robert Sinclair at the 1991 FCU start is user-approved provisional chronology, not a new official-history claim. Unknown officeholders use user-approved office representations. Exact source layers, affected IDs, status and evidence are in [the interface/FCU addendum](USEA_INTERFACE_FCU_ADDENDUM.md).

## FATO and South Belka national campaigns

The [national campaign ledger](FATO_SOUTH_BELKA.md) separates the official
1991/08.29 and 1995/03.25,06.01–04,06.20 Chronicle context from inherited FAT/SBK
territorial, force, faction, release and reintegration contracts. All 96 national
focus purposes, 20 dialogues, administrative institutions, later review dates,
warrant quantities and civil-case policy details are provisional authored fiction
and gameplay, individually mapped in `tools/fato_south_belka/purposes.json`.
Eight original scene masters retain exact prompts and packaging provenance.
No new government biography, border, core, force transfer or war is asserted.
Implementation/source evidence is separate from paused native acceptance.
