# Canon and provenance ledger

This ledger is a work queue, not a claim that the entries below are settled. Official-source links are preferred for official-canon claims; the mod archive is retained as provenance only.

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Strangereal is the shared fictional setting across numbered ACE COMBAT stories | Official | [ACES Chronicle — Super Weapons](https://acecombat.jp/en/chronicle/weapons/) names the "Strangereal" world; [Details](https://acecombat.jp/en/chronicle/details/) is the connected chronology across numbered titles. Read 3 Nov 2026. No single date. | Confirmed at the setting level; use the details chronology for individual dates and borders. |
| ACE COMBAT Zero / Belkan War as source context | Official | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), section "ACE COMBAT ZERO: THE BELKAN WAR", read 3 Nov 2026. War breaks out 1995 / 03.25; Lumen treaty 1995 / 06.20; AWWNB coup 1995 / 12.25; Avalon facilities attacked 1995 / 12.31. | Confirmed as official title context; this does not validate every mod event or date. |
| Excalibur completed 1994 / 12.23 and destroyed by Allied Forces 1995 / 05.23 | Official for those two dates | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1994 / 12.23 and 1995 / 05.23, read 3 Nov 2026. Belkan War period, not the 1999–2005 window. | Dated completion and destruction are official. The in-game "1981 chemical laser" wording is not that sentence and is not promoted. Affected: `belka_dlp_war.3`, `ac_news_event.12`, `ac_sp_excalibur`. |
| V2 mass-retaliation plans and Avalon launch facilities, 1995 | Official | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1995 / 05.17 and 1995 / 12.31, read 3 Nov 2026. Belkan War period, not the 1999–2005 window. | Plans discovered 17 May 1995; launch facilities at Avalon Dam attacked 31 December 1995. No 1985 Avalon date is promoted. Affected: `ac_sp_v2`. |
| April 5, 2024 Project Ulysses archive content | Mod provenance | Immutable archive SHA-256 `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071` | Preserved and audited; not official-canon proof. |
| Joker 1: Ustian birth, Belkan connections, Moon11/Shadow22, Watchtowerorganization, Cope, and Tasha's mother shooting him down | User-authored continuity | The supplied planning outline | Approved creative layer, not official canon; compile exact dates/details from the author before implementation. |
| 2065-12-31 inclusive campaign cutoff | Project requirement / provisional engineering contract | `docs/DESIGN.md` | Engine permission, authored content, and runtime coverage must be reported separately. No invented future lore. |
| Ulysses fallout and Usean Continental War, 1999–2005; Stonehenge, Megalith and Arkbird project framing | Official | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/) and [Super Weapons](https://acecombat.jp/en/chronicle/weapons/), read 3 Nov 2026. Implementation notes remain in [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md). Excalibur and V2 are the Belkan War rows above. | Implemented in source through the existing UCW and special-project owners; the AC04/AC5 expansion below adds operations and authored branches. Native acceptance remains open. The war's start day, Megalith's construction timing and every alternate outcome are provisional gameplay. Recta has no Chronicle entry and stays mod provenance. |
| ISAF headquarters in North Point, `NPT_host_isaf`, 2004 / 09.16 | Official for the Chronicle sentence; provisional gameplay for the modifiers | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 2004 / 09.16, read 3 Nov 2026. The focus comment and `NPT_host_isaf_desc` already cite that entry. | Implemented. `common/national_focus/NPT_pre_continental_war.txt`; idea `NPT_isaf_rear_base_idea`. Gated on `ac_ucw_isaf_formed`, which this focus reads and does not set. |
| Yuktobanian Arkbird partnership, `yuk_arkbird_partnership`, 1999 / 10.08 | Official for the Chronicle sentence; provisional gameplay for the modifiers | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1999 / 10.08, read 3 Nov 2026. `YUK.txt` and `yuk_arkbird_partnership_desc` already cite that entry. | Implemented. Idea in `common/ideas/yuktobania.txt`, granted by `YUK_arkbird_debris_programme`. Debris clearing only; no weapon. |
| Federal Law Review year on the approved Ustio and Gebet strings | Official for 1987 / 12.17 | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1987 / 12.17: the Belkan Federation undergoes legal reforms. Re-read 5 Nov 2026. The mod label "Federal Law Review" is already used by `belka_dlp_coup.5.d`, which already said 1987. | Reform year corrected from 1988 to 1987 in `UST_GATHERING_STORM_DESC`, `GEB_GATHERING_STORM_DESC`, `UST_start_desc`, and `UST_they_are_coming_desc` only. The two Ustio starting descriptions now separate the reforms from independence in 1988 (next row). Other 1988 "Federal Law Review" strings were outside that list and are unchanged. |
| Ustio gains independence on 12 May 1988, after the 17 December 1987 Belkan legal reforms | Official | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), section "ACE COMBAT ZERO: THE BELKAN WAR", separate entries 1987 / 12.17 and 1988 / 05.12, read 5 Nov 2026. | Implemented in `localisation/english/bookmarks_l_english.yml` (`UST_GATHERING_STORM_DESC`) and `localisation/english/country_UST_l_english.yml` (`UST_start_desc`). Corrects the earlier audit's conflation of the dates. "Federal Law Review" and the unchanged occupation/cultural backstory remain mod provenance, not facts established by these entries. Regression in `tools/Test-UstioContinuity.py`; native presentation untested. |
| Republic of Gebet | Official | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1988 / 02.08: "The Republic of Gebet gains its independence." | "Confederation of Gebet" corrected on `GEB_communism`, `GEB_democratic`, `GEB_neutrality` and their `_DEF` keys, and in `GEB_GATHERING_STORM_DESC`. `GEB_fascism` ("Gebetian Federation") and `GEB_monarchism` ("Kingdom of Gebet") were not Confederation strings and were left. |
| Belkan Liberal Democratic Party name | Official for the 1992 / 02.24 name | [ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), 1992 / 02.24: "The Belkan Liberal Democratic Party wins a single-party majority." | `ac_news_event.5.d` now uses that name. `BLK_dlp_victory` and `belka.13` use the abbreviation DLP only, so they were not edited. Party-name keys and `osea.23.d` still say "Democratic Liberal Party" and were outside the approved keys. "Far-right" wording was not changed. |
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

## 1991 bookmarks and Belkan branches

The former single row "1991 bookmarks and existing Belkan branches = mod provenance" is split here. A Chronicle paraphrase is official only for the cited sentence. Invented people, elections, and the named excesses stay mod provenance. Campaign scaffolding stays provisional gameplay. In-game text was not rewritten for these rows.

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Two January 1991 bookmark files | Mod provenance | Both `common/bookmarks/blitzkrieg.txt` and `common/bookmarks/the_gathering_storm.txt` set `date = 1991.1.1.12` and `default = yes`. `blitzkrieg.txt` lists BLK, OSE, UST, SAP, GEB, EMM and EVA. `the_gathering_storm.txt` lists only EMM and EVA. | Not identical. Which file is canonical is an open owner decision. Documented in `PORT_1_19.md` and `NEXT_TASKS.md`. Neither file was edited. |
| Belka 1991 start ideology | Mod provenance | `blitzkrieg.txt` sets BLK `ideology = fascism`. `history/countries/BLK - Belka.txt` sets `ruling_party = neutrality`. | Flagged only. Which value is the start is an open owner decision. Neither file was edited. |
| `BLK_osean_prop`, `BLK_sell_the_land`, `BLK_wait_for_profit` | Official for the 1991 sale and the GLRDC loss | [Chronicle details](https://acecombat.jp/en/chronicle/details/), 1991 / 08.16 (GLRDC, jointly financed, operating at a loss) and 1991 / 08.29 (Belka sells northern land to FATO, eastern land to neighbors, and cedes the Great Lakes and northern islands to Osea). Focuses in `common/national_focus/BLK_start.txt`. | Implemented paraphrase. `BLK_wait_for_profit` keeps the `glrdc_good_flag` branch, with the `id = xxx` fire commented out. Revive versus delete is an open owner decision. |
| `belka.8`, `belka.9`, `belka.10` | Official for the same 1991 / 08.16 and 08.29 sentences | `events/Belka.txt`; `country_BLK_l_english.yml` | Implemented paraphrase of the sale and the company. The offer's motives and the recovery-plan wording are not Chronicle sentences. |
| `ac_news_event.1`, `ac_news_event.4` | Official for 1991 / 08.29 and 1991 / 08.16 | `events/ac_news_events.txt`; `ac_new_events_l_english.yml` | `.1` paraphrases the territorial sales. `.4` paraphrases the company operating at a loss. The sabotage speculation in `.4` is not a Chronicle sentence. |
| `ose_acquisition_of_belkan_land` | Official for the Great Lakes cession, 1991 / 08.29 | `common/national_focus/OSE_pre_belkan_war.txt` | Implemented as the Osean follow-up to the cession. What Osea does with the land afterwards is gameplay. |
| `osea_glrdc.1`–`.3` | Official for the GLRDC loss (1991 / 08.16); the 1905/1910 "Osean War" is mod provenance | `events/Osea.txt`. `osea_glrdc.2.d` states a 1905 war. `osea_belka_land.2.d` and `belka_dlp_war.102` state a 1910 end. No such war is on the Chronicle details page. | The company cover-up can be cited. The 1905 annexation story, the "Osean War", and the 1910 ending stay mod provenance. `osea_glrdc.3.b`, which would set `glrdc_good_flag`, is commented out. |
| `OSE_1991_cold_war_build_up_plan` | Mod provenance for the 1991 white paper; the cold-war backdrop is official | [Chronicle details](https://acecombat.jp/en/chronicle/details/), 1980s: "Osea and Yuktobania enter a state of cold war." No 1991 defense white paper, maritime/air priority, or ground-force neglect. Focus in `OSE_pre_belkan_war.txt`. | The plan exceeds the Chronicle and stays mod provenance. The 1980s cold war is the only official part. |
| `belka_dlp_war.97` | Official for 1995 / 03.25 and 1995 / 06.20 | [Chronicle details](https://acecombat.jp/en/chronicle/details/). `events/Belka.txt`. | The dated war span matches. The crisis-to-revenge causal paragraph, including "far-right", is not a Chronicle sentence and is not promoted. In-game wording unchanged. |
| `belka_dlp_war.100`, `ac_news_event.8` | Official for seven nuclear devices in the Waldreich Mountains, 1995 / 06.06 | [Chronicle details](https://acecombat.jp/en/chronicle/details/), 1995 / 06.06. | Implemented. The operational-order flavor is not the Chronicle sentence. |
| `belka_dlp_war.101` | Official for the Lumen treaty, 1995 / 06.20 | [Chronicle details](https://acecombat.jp/en/chronicle/details/), 1995 / 06.20: "A treaty is signed in Lumen. The Belkan War ends." | The date and place match. The event's territorial, reparations, and force-limit terms are not that sentence and are not promoted. |
| `belka_dlp_war.3`, `ac_news_event.12` | Official for Allied destruction of Excalibur, 1995 / 05.23 | [Chronicle details](https://acecombat.jp/en/chronicle/details/), 1995 / 05.23. | The destruction date matches. "Chemical laser" and the 1981 design claim are not promoted. In-game text unchanged. |
| Osea Mackenzie and Andrews | Mod provenance | `common/characters/OSE.txt` (`Tyler Mackenzie`, `Daniel Andrews`); `OSE_pre_belkan_war.txt` | Invented officeholders. No Chronicle entry for either name. |
| Ustio Naruszewicz, Morkawiecki, and the Ratio/Tyrann/Boikos dispute | Mod provenance | `common/characters/UST.txt` (`Grzegorz Naruszewicz`, `Kuba Morkawiecki`); `UST_deal` and `ustio.1` in `country_UST_l_english.yml` | Invented people and the Ratio purchase. The Chronicle names Ustio's independence on 1988 / 05.12, not this dispute. |
| Gebet Ebner, Albrecht, and Faulmann | Mod provenance | `common/characters/GEB.txt` (`Ilse Ebner`, `Rafael Albrecht`); ace Jakob Faulmann in `history/countries/GEB - Gebet.txt`; focus `GEB_faulmann_doctrine` | Invented people. The Chronicle names the Republic of Gebet from 1988 / 02.08 only. |
| Belka Lehmann, Meier, BNCP, Alternative Wege, Weber, and `BLK_abelard_straub` | Mod provenance | `common/characters/BLK.txt`; `belka.7`, `BLK_chaos_in_the_assembly`, `osea_glrdc.1` | Invented parties and people. The Chronicle names the Belkan Liberal Democratic Party (1992 / 02.24) and Waldemarr Rald. It does not name these. |
| Sapin 1991 elections and the 1990 reform | Mod provenance | `sap_1991_parliamentary_elections` and the 1990 Constitutional Reform sentences in `country_SAP_l_english.yml` | No Chronicle entry for a 1990 reform or a 1991 election. The Kingdom of Sapin appears at 1995 / 10.18 (Espada Team). |
| Carbonero peace branch | Mod provenance | `belka_dlp_war.102` in `country_BLK_l_english.yml` (Carbonero treaty, with a 1910 callback) | Invented peace branch. Not a Chronicle outcome. |
| `ac_belkan_campaign.txt` | Provisional gameplay | `events/ac_belkan_campaign.txt`, `common/national_focus/ac_belkan_campaign.txt`, and the decisions and ideas of the same name | Campaign scaffolding. Not an official chronology. |
| `ERU_opening` and `FCU_opening` | Provisional gameplay | `common/national_focus/ERU_opening.txt` (`ac_exp_eru_opening`) and `FCU_opening.txt` (`ac_exp_fcu_opening`) | Pre-1999 opening trees. Not Chronicle events. |
| AWW/AWWNB stub | Provisional gameplay | `common/national_focus/AWW.txt` (`awwnb_focus`) and `AWW_shared.txt` (empty rewards); `history/countries/AWW - AWWNB.txt` | Stub tree. The Chronicle coup is 1995 / 12.25 and the Avalon defeat is 1995 / 12.31. This stub does not implement those sentences. Anton Kupchenko is not promoted. |

## Unconfirmed claims left unpromoted

These were not given official rows, and their in-game text was not edited. Hedge versus delete is an open owner decision.

| Claim | Where it still appears | Why it stays unpromoted |
| --- | --- | --- |
| Excalibur as a 1981 chemical laser | `belka_dlp_coup.6.d`, `belka_dlp_war.3.d`, `ac_news_event.12.d` | [Super Weapons](https://acecombat.jp/en/chronicle/weapons/) calls Excalibur a laser conceived under the 1981 ballistic-missile-defence program. It does not say "chemical laser". |
| Avalon Dam in 1985 | `belka_dlp_coup.7.d` | The Chronicle dates the Avalon attack to 1995 / 12.31. No 1985 Avalon entry was on the details page read 3 Nov 2026. |
| Pendragon as an ICBM | `belka_dlp_coup.7.d`, `belka_dlp_war.99.d` | 1985 says only "Project Pendragon is launched in Belka." The ICBM reading is not that sentence. |
| Dr. Anton Kupchenko / Gault | `belka_dlp_coup.7.d`; `AWW_anton_kupchenko` in `common/characters/AWW.txt` | Neither name is on the Chronicle details page read 3 Nov 2026. |
| `BLK_project_rhongomyniad` | `common/national_focus/BLK_war_won.txt`; `ac_sp_rhongomyniad` | No Chronicle entry. The project file already marks it provisional gameplay on mod provenance. |
| Sapin 1972 Recta rebellion | `sap_hire_rectan_war_refugees_desc` | No Chronicle entry. The text says Recta rebelled against the Belkan Federation in 1972. |
| Recta independence from Gebet | `recta.1.d`, `ac_news_event.3.d` | The Chronicle has no Recta entry. Already mod provenance on the Usean row. `ac_news_event.3.d` already dated the Federal Law Review to 1987 and was not edited. |

## Open layer-tag questions

These labels sit outside the four source layers in `CANON_POLICY.md` (official, user-authored, mod provenance, provisional gameplay). They were not remapped.

- `Mixed / pending` on the technology/equipment row above.
- `Project requirement / provisional engineering contract` on the 2065-12-31 row above.
- "User-approved provisional chronology" and "user-approved office representations" in the 2026-10-30 starting-government repair section below.

Whether to remap them is an open owner decision. See `docs/NEXT_TASKS.md`.

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

## 1991 hull programs and name corrections

Checked against the English [ACES Chronicle details](https://acecombat.jp/en/chronicle/details/), 5 November 2026.

| Claim | Source layer | IDs | Status |
| --- | --- | --- | --- |
| 17 December 1987 Belkan Federation legal reforms; Republic of Gebet independent 8 February 1988; Republic of Ustio independent 12 May 1988 | Official Chronicle, 1987 / 12.17, 1988 / 02.08, 1988 / 05.12 | `GEB_democratic`, `GEB_neutrality`, `GEB_GATHERING_STORM_DESC`, `UST_GATHERING_STORM_DESC`, `UST_start_desc` | The 1991 democratic, non-aligned, and communist names now say Republic of Gebet. The select-screen text and Ustio's opening focus use the Chronicle dates. Fascism and monarchism names for Gebet stay provisional alternates. Older focus and event lines still say "Federal Law Review," which the Chronicle does not name. |
| Democratic Republic of Leasath | Ace Combat X, Japanese レサス民主共和国. The Chronicle's 2020 rows say Leasath and give Federal Republic only to Aurelia. | `LEA_democratic`, `LEA_neutrality` | The 1991 democratic and non-aligned names no longer use Aurelia's federal title. Communism already used the democratic-republic name. |
| Great Lakes Resource Development Company found covering up an operating loss, 16 August 1991 | Official Chronicle, 1991 / 08.16 | `ac_news_event.4` | The world news no longer says the firm was a weeks-old sabotage plot or that the territorial sales had already happened. Belka's own focus text is unchanged. |
| Osea orders the Kestrel, seventh Hubert-class carrier, 29 July 1991; commissions her 16 September 1999 | Official Chronicle, 1991 / 07.29 and 1999 / 09.16 | `ac_yards.1`, `ac_yards.2`, `ac_yards_fund_berth`, `ac_yards_sea_trial` | The order and the commission fire on those days for Osea. Funding the berth and the trial odds are provisional gameplay. No ship is spawned. |
| Scinfaxi class announced at Cinigrad, 2 September 1991; Osean Foreign Minister Howards belittles it | Official Chronicle, 1991 / 09.02 | `ac_yards.3`, `ac_yards.4`, `ac_yards_draft_class` | The announcement and Howards' answer fire on the calendar. The draft bonus is provisional gameplay. No submarine is spawned. |

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

## AC04 and AC5 campaign expansion

The [campaign implementation ledger](AC04_AC05_CAMPAIGNS.md) and exact
`tools/ac_campaigns/sources.json` references distinguish official chronology,
game dialogue reproduced in identified secondary transcripts, inherited
geography and original supporting fiction. The new `ac_camp` scenes, policies,
operation rules, clinic, dialogue and alternate fates are provisional authored
gameplay approved in the private 5 November 2026 plan. They are implemented in
source; static/offline and native acceptance remain separate. Existing `ac_ucw`
and `ac_cpw` owners retain their war outcomes. No Joker continuity, border,
officeholder, source archive, state 171 or new canonical biography is changed.

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

## Belkan War outcome handoff (static, 2026-11-05)

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| Conventional victory, Wacht am Wal, and the inherited defeat tree hand off without the demo popup | Provisional gameplay on mod-provenance flags. Not an official postwar settlement. | Flags `belka_won_belkan_war`, `belka_won_belkan_war_wacht_am_wal`, `belka_lost_belkan_war`. Effect `ac_dispatch_belkan_war_outcome`. Event `ac_continuation.1`. Trees `ac_belkan_postwar` and existing Ustio reload `ac_ustio.1`. | Statically wired. Belka, Ustio, focus, decision, on-action, and news paths no longer schedule `world_event.2`. The defeat flag is set at `belka_dlp_lost.7` only after `ac_postwar_wait_for_defeat_tree`. No new borders. Native HOI4 untested. `belka_dlp_war.103` still has no natural caller, and its title disagrees with its defeat effects. Wacht failure events `.4` and `.7` still have no scripted peace. |

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
| Original squadron stories for Aurelia (*Kept in Repair*) and Leasath (*Orders in Two Hands*), and the Anean continuations *What Tomorrow Inherits* (EMM) and *The Inspection Already Due* (EVA) (5 November 2026) | User-approved original supporting fiction (mod-authored); reads only published gameplay records (`ac_alc_*`, `ac_lcw_*`, `ac_eew_*`) and the original stories' recorded conclusions | `tools/squadrons/southern` (`ac_sqs`, bases 900/1000), `tools/squadrons/anean_epilogue` (`ac_sqa`, bases 100/200), art plan `tools/squadrons/southern_art/plan.json` | Text and compiled preview validated offline; **not admitted**: the 32 art masters are not generated, so no script or picture ships. No official character, unit or weapon is a character; officials unnamed; Leasath's "years of exploitation" is voiced only by Leasathian characters or broadcasts; all principals live. Not official history. |

## 1991 Ustio provisional force loads

| Claim or content family | Source layer | Current evidence | Status / required action |
| --- | --- | --- | --- |
| `UST_mercs_1`, loaded by decision `UST_buy_mercs` | Provisional gameplay | No official ACE COMBAT order of battle is cited. The file copies the existing `MP` template: three infantry battalions and no support companies. Ustio's 1991 history already has `infantry_weapons` and `infantry_weapons1`. The decision keeps its id and its cost of 150. Two detachments spawn in state 335 (provinces 2930 and 2140) when Ustio controls that state, and in the capital otherwise. The decision adds 600 `infantry_equipment_1` and the detachments use `start_equipment_factor = 0`. Country history does not load the file. | Implemented. Static contract in `tools/Test-HistoryDataCleanup.py`. Size and experience are a balance placeholder pending a native playtest. Native HOI4 is untested. |
| `UST_moblise_militia_focus_oob`, loaded by focus `UST_moblise_militia` | Provisional gameplay | No official ACE COMBAT order of battle is cited. The file copies the existing civil-war `Militia` template: two locked infantry battalions and no support companies. The focus id keeps its spelling. Four detachments spawn in states 335 and 340 when Ustio controls them, and each uncontrolled pair spawns in the capital. The focus adds 800 `infantry_equipment_1` and the detachments use `start_equipment_factor = 0`. Country history does not load the file. | Implemented. Static contract in `tools/Test-HistoryDataCleanup.py`. Size is a balance placeholder pending a native playtest. Native HOI4 is untested. |
| Focus visibility repairs (6 November 2026): Ustio and Belkan postwar roots moved right so no node sits left of x = 0; `BLK_party_disagreements` pointed to a defined sprite; titles and descriptions for 15 inherited AWW focuses | Mod provenance (repair) | `UST_shared.txt`, `ac_belkan_campaign.txt`, `BLK_DLP.txt`, `ac_focus_text_repairs_l_english.yml`; [FOCUS_SCREEN_REPAIRS_20261031.md](FOCUS_SCREEN_REPAIRS_20261031.md); `tools/Test-FocusVisibility.py` | Implemented; static only. The AWW texts state what each focus does from its own script and add no history. Native rendering is unconfirmed. |
