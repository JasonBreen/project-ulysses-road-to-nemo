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

## 2026-11-02 content waves A and D

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Free Erusea's armed insurrection and its defeat by Mobius 1, 26 September 2006 | Official | Chronicle, 2006 / 09.26, compiled in [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md) (read 3 November 2026). IDs `ac_fe.1`, `ac_fe.5`, `ac_fe.6`, `ac_fe_defeat`, `ac_fe_insurrection_defeated` | Reconciled 3 November 2026. The historical route records the defeat when Central Usea answers (`ac_fe.5`, AI always). Mobius 1 is named only in text and is not a unit. Members, aims and places are not sourced and are not asserted. Offline-tested; native untested. |
| Prolonged insurrection: pressure model, containment, crisis review and partner assistance | Provisional gameplay (alternative to the historical defeat) | `tools/content_waves/free_erusea.py`; IDs `ac_fe_prolonged`, `ac_fe_pressure`, `ac_fe.2`–`.4`, `ac_fe_pressure_*`, `ac_fe_emergency_administration`, `ac_fe_partner_assistance` | Implemented, offline-tested. Runs only when Central Usea leaves the response to the provisional government, cannot answer, or lets the 30-day window lapse. `ac_fe.3` names the official defeat date. No country tag, civil war, border or core change. |
| Erusean and Central Usean oversight-years branches, 2005–2009 (60 focuses) | Provisional gameplay, gated on existing `ac_ucw` outcome flags (mod provenance) | `common/national_focus/ac_free_erusea.txt`, `ERU_fe_*`, `FCU_fe_*` | Implemented, offline-tested. Each Continental War outcome opens a different lane; only the ISAF-victory route meets the sourced oversight context. |
| Nordennavic national programme, 1991–2016 (42 focuses) | Mod provenance (country history, office, world start, institution profile, 2004 Anean bureau invitation) plus provisional gameplay | `common/national_focus/NEC.txt`, `ac_nordennavic.txt`, `NEC_nc_*`, `ac_nec_*` | Implemented, offline-tested. No Chronicle entry for Nordennavic is compiled, so no dated event, person, alliance, border or war role is asserted. The neutrality lane prepares for a neighbour's conflict without assuming one. |
| Estovakian civil war mechanic (future Wave B) | Project decision | User decision recorded 2 November 2026 in `docs/CONTENT_PLAN_2006_2020.md` | Pending. A tagless internal-conflict owner comes first; a temporary civil-war tag needs a reviewed source, state mapping, lifecycle and save-continuity contract. |

Details, affected files and validation are in [CONTENT_WAVES_A_D.md](CONTENT_WAVES_A_D.md).

## 2026-11-03 Wave B and Aurelia's foundation

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Estovakian civil war chain, 3 April 2007 to 4 February 2014 | Official, as compiled in [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md) | Chronicle, 2007 / 04.03, 06.30; 2008 / 07.15, 10.23; 2010 / 02.19; 2011 / 05.09; 2013 / 01.15, 10.29, 11.25, 12.02; 2014 / 02.03, 02.04. IDs `ac_ecw.1`–`.12`, `ac_ecw_owner_weekly` | Implemented as a tagless owner; offline-tested; native untested. Factions and people appear only in news text as the Chronicle names them. No tag, civil war, border, core, leader or ideology change. |
| Negotiated settlement, prolonged war, authority and strength values, Estovakian and Emmerian branches (48 focuses) | Provisional gameplay | `tools/content_waves/estovakia.py`; `EVA_ecw_*`, `EMM_ecw_*`, `ac_ecw.13`–`.14` | Implemented, offline-tested, labelled where they diverge from the record. Existing `ac_anea_*` state is read, never written. |
| Aurelia's national foundation, 1991–2018 (54 focuses) | Mod provenance plus provisional gameplay; Leasath's trade complaint is context from Chronicle, 2020 / 10.XX, recorded as Leasath's claim; the Leasath civil war's start is derived from Chronicle, 2019 / XX.XX | `common/national_focus/AUR.txt`, `ac_aurelia.txt`, `AUR_au_*`, `ac_aur_*` | Implemented, offline-tested. No 2020 place, person or weapon is used; the remaining 30 focuses belong to the 2019–2020 crisis lanes. |

Details are in [CONTENT_WAVES_B_AUR.md](CONTENT_WAVES_B_AUR.md).

## 2026-11-03 Wave C: the Circum-Pacific War

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| The Arkbird Summit (2008 / 08.21) and the 2010 chain from Cape Landers (09.23) to the SOLG (12.31) | Official, as compiled in [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md) (2010 rows re-read 4 November 2026) | `tools/content_waves/circum_pacific.py`; IDs `ac_cpw.1`–`.15` and `ac_cpw.20`–`.35` (31 events), `ac_cpw_declare`, `ac_cpw_stage_*` | Implemented as an owner-only wave; offline-tested; native untested. Yuktobania's declaration is the only scripted war (AI always). Territorial rows wait for an observed Osean foothold; nothing is mapped. People, squadrons, ships, places and weapons appear only in event text, and in the idea and flag tooltips derived from it, as the Chronicle names them. |
| Arkbird, SOLG, Scinfaxi and Hrimfaxi | Official: Super Weapons rows | `ac_cpw_arkbird_*` flags, `ac_cpw_yuk_submarine_carrier(s)`, `ac_cpw.35` text | The Arkbird stages need `ac_sp_arkbird_complete` and Osea's commitment; the project is never created, revived, weaponized or completed by script, and its two ideas are removed only on the sourced loss. No ship, railgun or project is created. |
| Earned reciprocal exchange, earned withheld declaration, external observation, no scripted peace, idea values and decisions | Provisional gameplay under the published consumer contract ([PACIFIC_NATIONAL_CONTINUATIONS.md](PACIFIC_NATIONAL_CONTINUATIONS.md)) | `ac_cpw_prevented`, `ac_cpw_declaration_withheld`, `ac_cpw_tainted` (third-party entry), `ac_cpw_existing_war_observed` (a war the pair already fought, observed without the expanded marker), `ac_cpw_record_end` | Implemented, labelled in-game. The war's end is recorded only on actual cessation, capitulation or the earned peace after the appeal (content-plan decision 6, decided 5 November 2026: `OSE_cpw_accept_appeal`, `YUK_cpw_accept_appeal`, `ac_cpw.16`/`.17`, `ac_cpw_make_peace`; provisional gameplay, not a Chronicle claim). |

Details are in [CONTENT_WAVE_C.md](CONTENT_WAVE_C.md).

## 2026-11-04 Wave F1: the Lighthouse War

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| The 2019 chain from the declaration (05.15) to the Expo City ceasefire (12.01) | Official, as compiled in [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md): Chronicle 2019 / 05.15, 05.17, 05.30, 06.06, 08.10, 08.19, 09.19, 10.01, 10.10, 10.31, 12.01; Abstracts and Product, ACE COMBAT 7 | `tools/content_waves/lighthouse.py`; IDs `ac_lhw.1`–`.13`, `.20`–`.29`, `ac_lhw_declare`, `ac_lhw_sign_ceasefire`, `ac_lhw_stage_*` | Implemented; offline-tested; native untested. Erusea's declaration is the waves' second scripted war (AI always) and the Expo City ceasefire the only scripted peace (user decision 7); both write state only if the engine acted. The route opens only after the ISAF victory. People, forces, places and weapons appear only in event and idea text as the sources name them. |
| Arsenal Birds and Alicorn | Official: Super Weapons rows | projects `ac_sp_arsenal_birds` (OSE) and `ac_sp_alicorn` (ERU) in generator-owned files; ideas, tags, fallbacks, art | Implemented (user decision 8). The Track C files stay hash-pinned and unchanged. The seized birds, the Liberty and the Justice follow the owner's course; the Alicorn is built and held, never deployed. |
| Erusean and Central Usean Lighthouse-era branches (78 focuses), the withheld declaration, the early ceasefire, fighting on, every value | Provisional gameplay, gated on `ac_ucw`, `ac_fe` and `ac_lhw` state (mod provenance read only) | `common/national_focus/ac_lighthouse.txt`, `ERU_lw_*`, `FCU_lw_*`, `OSE_lw_*` | Implemented, offline-tested, labelled in-game. The Shilage release flags are read for text only; nothing is released, cored or moved. |

Details are in [CONTENT_WAVE_F1.md](CONTENT_WAVE_F1.md).

## 2026-11-04 The official lore record, 1991–2020

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Every statement on the official ACES Chronicle (Details, Super Weapons, Abstracts) and product pages: 207 statements, 292 claims | Official | [STRANGEREAL_LORE_1991_2020.md](research/STRANGEREAL_LORE_1991_2020.md), [CHRONICLE_INDEX.md](research/CHRONICLE_INDEX.md), `tools/lore/chronicle.json` (hashes, never text); read 4 November 2026 | Compiled and independently checked against the official text. Listing is not implementation: 114 claims are implemented by sourced ledger rows, 24 are owned by inherited mod content, 47 are pending a wave, 43 are not covered, 10 are reference only and 54 are out of scope |
| The 1991–1999 entries no earlier ledger cited (the Kestrel, the Great Lakes company, Cinigrad, the 1991 border redrawing, the Liberal Democratic Party, the 1995 war stages, Espada Team, Robert Tyler, Hresvelgr) | Official | [BELKAN_WAR_SOURCES.md](BELKAN_WAR_SOURCES.md) | Thirteen reference briefs implemented (`ac_bwr.1`–`.13`, tools/content_waves/belkan_record.py, 5 November 2026): each fires once on observed state inside its window and writes only `ac_bwr_*`; archive owners keep their rows; no border, unit or officeholder. Hresvelgr stays reference; the unset `belka_lost_belkan_war` is recorded for separate review. |
| Official Bandai Namco pages outside the four ACES pages (the ACE COMBAT 7 site's world, elevator, character and column pages; the European press page) | Official, not yet cross-checked | Pointers in the report | Read the page before using it. Notably: the Kingdom of Erusea as the former Republic with a restored monarchy, and ISEV building the elevator from about 2011 in southern Usea |
| Fan wikis (acecombat.wiki.gg, acecombat.fandom.com) | Secondary, unverified | Pointers in the report | Never promoted to official here |
| The Emmeria–Estovakia War, 2015–2016; the Aerial Fleet and the Chandelier | Official (Chronicle 2015 / 04.21 to 2016 / 04.01; Abstracts and Super Weapons) and provisional gameplay | [CONTENT_WAVE_E.md](CONTENT_WAVE_E.md); `ac_eew`, `EMM_ew_*`, `EVA_ew_*`, `ac_sp_aerial_fleet`, `ac_sp_chandelier` | Implemented 5 November 2026; static/offline only. The fireballs are not attributed; places stay unmapped; scripted ceasefire written only if the engine acts. |
| The Leasath civil war (2009–2019, start derived) and the Aurelia–Leasath war, 2020; the Gleipnir and Archelon | Official (Chronicle 2019 / XX.XX, 2020 / 10.XX to 12.XX and XX.XX; Abstracts, Product and Super Weapons) and provisional gameplay | [CONTENT_WAVE_F2.md](CONTENT_WAVE_F2.md); `ac_lcw`, `ac_alc`, `LEA_le_*`, `LEA_sw_*`, `AUR_sw_*`, `ac_sp_gleipnir`, `ac_sp_archelon` | Implemented 5 November 2026; static/offline only. Month windows (no days); "years of exploitation" is Leasath's stated claim; no winner of the civil war is named; the Nevera Jammer and Meson Cannons stay reference only. |
| Text for seven reachable inherited events that had none: `perbla_intervention.1`, `ustio_f.1`–`.5`, `gebet_belkan_war.5`, `osea_oia.2` (5 November 2026) | Mod provenance (repair) | Written from each event's own script and the archive's comments; marked in `country_PBL`, `country_UST`, `country_GEB` and `country_OSE_l_english.yml`; [EVENT_DEFAULTS_STYLE.md](EVENT_DEFAULTS_STYLE.md#current-measurement) | Implemented; static only. Not archive text and not official history. The 12 keys of unreachable events stay listed, not written. |
