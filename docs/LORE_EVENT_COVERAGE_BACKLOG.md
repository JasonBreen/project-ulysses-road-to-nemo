# Lore and event coverage backlog

This is a source-traceable coverage backlog for the private continuation. It is not a claim that every row is official canon or that every scripted definition is reachable. “Static” means present or reference-checked in files; “native” requires an approved HOI4 run and is currently out of scope.

## Source layers

| Layer | Use | Rule |
| --- | --- | --- |
| Official | Project Aces/ACE COMBAT games, manuals, official archive, publisher material | Use for dates, borders, names, characters, equipment, and established relationships. Cite the primary source. |
| User-authored | Established Joker 1 continuity | Preserve as user-authored; compile exact details before implementation. |
| Mod provenance | April 5, 2024 archive and inherited repository content | Shows what the original mod attempted, not official canon proof. |
| Provisional gameplay | HOI4 balance, abstractions, placeholder IDs, branch mechanics | Label in docs/localization; never present as lore fact. |

## Coverage matrix

| Area | Existing evidence | Missing or unresolved work | Status / next task |
| --- | --- | --- | --- |
| Campaign start | Two Jan 1, 1991 bookmarks | Decide whether they are duplicates or distinct scenarios; do not imply the war began on Jan 1 | Mod provenance; static audit |
| Belkan War core | Belka, Ustio, Sapin, Gebet, Osea, AWWNB focus/event content | Trace opening, escalation, AI, OOBs, supply, peace, and branch reachability | Static contracts exist; native unverified |
| Belkan victory | belka_won_belkan_war; occupation, demobilization, Excalibur, Rhongomyniad branches | Tie outcome to postwar decisions and reconstruction without inventing borders | Implemented in this branch as provisional gameplay handoff |
| Wacht am Wal | belka_won_belkan_war_wacht_am_wal | Preserve as a distinct narrow-peace branch and document divergent consequences | Implemented as distinct handoff flag |
| Belkan defeat | belka_lost_belkan_war; shattered army/industry/pride, elections, monarchy path | Add reconstruction and political settlement consequences; trace all alternate choices | Implemented as provisional handoff and decisions |
| Postwar handoff | world_event.2 previously only set ac_continuation_active and was the visible demo endpoint | Outcome flags are consumed by ac_dispatch_belkan_war_outcome and ac_continuation.1; world_event.2 is no longer scheduled | Statically wired for victory, Wacht am Wal, and the inherited defeat tree; provisional gameplay; native reachability unverified |
| Occupied/affected states | Existing transfers to South Belka, Gebet, Recta, FATO | Source-backed borders, cores, administration, resistance, and local consequences | Existing state effects are mod provenance; decisions are provisional |
| Osea politics | Election content and AI references exist; some branches were commented in the archive | Verify election reachability and postwar coalition/guarantor behavior | Static references; native unverified |
| Ustio | Shared focus/events, occupation and reconstruction hooks; repaired initial focus exposure and guarded postwar tree handoff | Trace postwar sovereignty, resistance, and diplomacy; native focus reachability | Static implementation in this slice; mod provenance only, chronology open |
| Sapin | Prewar tree, politics, revolt/demobilization content | Connect postwar government and war-cost consequences | Existing scaffold; chronology open |
| Gebet | Prewar tree, decisions, industrial/resource content | Connect settlement, reconstruction, and diplomatic effects | Existing scaffold; chronology open |
| Recta | Country history, events, decisions, capitulation hooks; `recta.1` localised; `rec_postwar_consolidation_focus` (`common/national_focus/REC.txt`, 13 focuses), ideas in `common/ideas/recta.txt`, AI in `common/ai_strategy/REC.txt` | Native reachability and AI behaviour of the tree | Static contract implemented as mod provenance and provisional gameplay. Branches cover Gebet relations, hardline versus reform communism and FATO relations. `REC_local_recovery_programme` waits for `ac_postwar_local_recovery` and reads the `ac_pwi.76` choice flags. No `transfer_state` and no new borders; checked by `tools/Test-UseaActors.py`. Native unverified. |
| Yuktobania | Country history, events, AI references; `yuktobania_fp.1` options now record `YUK_fp_intervened` / `YUK_fp_stood_aside`; `yuk_reform_focus` (`common/national_focus/YUK.txt`, 14 focuses), ideas in `common/ideas/yuktobania.txt` | Native reachability and AI behaviour of the tree | Static contract implemented. The post-intervention and non-intervention reform branches are mutually exclusive, and both end by replacing `yuk_top_heavy_command_structure` (mod provenance, provisional gameplay). The Arkbird debris-clearing branch is available from 8 October 1999 and sets `ac_yuk_arkbird_partner` (official: Chronicle 1999 / 10.08; effects provisional). There are no leader changes and nothing is dated after 2005. Native unverified. |
| North Point | Country history/definition; `npt_pre_continental_war_focus` rebuilt from the commented sketch (`NPT.txt`, `NPT_pre_continental_war.txt`, 15 focuses); new ideas in `common/ideas/north point.txt`; AI in `common/ai_strategy/NPT.txt` | Native reachability; the Host ISAF branch opens once `ac_ucw_form_isaf` (scripted effect in `ac_ucw.txt`) sets `ac_ucw_isaf_formed` | Static contract implemented. The 1991 election is a player choice and never sets a result (mod provenance). Isolation and FCU/UTO alignment are mutually exclusive. `NPT_host_isaf` reads `ac_ucw_isaf_formed` and sets `ac_npt_hosts_isaf` (official: Chronicle 2004 / 09.16; effects provisional). The rest of the tree works if the flag never appears. Native unverified. |
| North Point: Usea Depth (`npt`) | 107 focuses in `common/national_focus/ac_ud_npt.txt`, imported by the `USEA DEPTH NORTH POINT` block in `NPT.txt`; 23 long-form events `ac_ud_npt.1`-`.23`; ideas, unnamed office leaders and generated art. Ledger: [docs/usea_depth/NPT.md](usea_depth/NPT.md) | Native reachability, AI focus choice and balance. The Council, Parliament and Readiness Directorate paths and every 1991-2005 lane are provisional gameplay; only the 1996 / 04.20, 1997 / 05.30, 1998 / 06.19, 1999 / 07.08, 2000 / 04.21 and 2004 / 09.16 Chronicle dates are official | Static contract implemented (`tools/usea_depth/npt/test_npt.py`). Government changes only through `ac_ud_npt_regime_*` with AI weight 0; no border, core, war or `ac_ucw_*` flag writes; not tested in HOI4 (#8) |
| Wider Usea wars | Ulysses fallout (2000–2003) and the Usean Continental War (2003–2005) authored as namespace `ac_ucw`, with Erusea and Central Usea/ISAF trees; histories and hooks for Emmeria, Estovakia, Aurelia, Leasath and others. The 31 December 1995 Skully Islands action and the 30 May 1997 coup are scripted as `ac_ur` | Native reachability, AI war behaviour and balance are unverified. The prolonged 1997 branch is provisional gameplay | Continental War static contract remains as described in [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md#track-a-implementation-pr-a). The rebellion is static-validated by `tools/Test-UseanRebellion.py`. Chronicle dates are official. Native play stays under #8 |
| Usea Depth: Usean partners (San Salvacion, Amber, Ugellas, Delarus) | 260 shared focuses in `common/national_focus/ac_ud_partners.txt`, imported by the `USEA DEPTH PARTNERS` block of `SNS.txt`, `AMB.txt`, `UGE.txt` and `DEL.txt`; 52 long-form events `ac_ud_up.1`-`.52`; 63 spirits; 10 player-only provisional governments (`ac_ud_partners_regime_*`, unnamed office leaders). San Salvacion's rows cite the ACES Chronicle (1995 / 12.31, 1996 / 04.20, 1997 / 05.30, 1998 / 06.19, 1999 / 07.08, 2000 / 04.21, 2003 / SUMMER, 2005 / 03.14, 04.02, 07.10); everything about Amber, Ugellas and Delarus is provisional gameplay. Ledger: [usea_depth/PARTNERS.md](usea_depth/PARTNERS.md) | Native focus reachability, AI focus choice in the engine and balance of the spirits; the offline AI run only shows the Continental War still starts on 24 June 2003 | Static and offline (`tools/usea_depth/partners/test_partners.py`); not tested in HOI4 |
| Characters | Static leaders/advisors/military roles and portraits | Replace placeholders, add biographies/dates only from sources, connect character exits to events | Partial mod provenance; audit required |
| Joker 1 | Supplied outline: Ustian-born, Belkan ties, Moon11/Shadow22, Watchtowerorganization, Cope, Tasha’s mother | Compile exact dates, locations, motives, sequence, and source/private references | User-authored; do not infer |
| Organizations/corporates | Four MIO files; OTEC references in existing scripts/localization | Source and implement corporate history, procurement, rivalries, and later organizations | Partial/provisional; no dedicated Neucom/General Resource package found |
| Technology/equipment | 1991–2005 markers and inherited engine IDs | Provenance, localization, era gates, and later-war source audit | Open; issue #5 |
| Geography | 11,352 provinces, 612 states, 326 regions | Resolve state 171 and 203 XXX regions; source every later border | Open geography decisions |
| 2065 horizon | Engine cutoff contract through 2065-12-31 | Authored, source-backed content is not established for every year; do not fill with invented history | Engineering target only |
| Usea Depth minors B: Spayca, Calladen, Roca Roja, Rohden, Voslage, Corscae and a dormant Shilage release tree | Seven national trees in `common/national_focus/ac_ud_minor_<tag>.txt` (394 focuses), `ac_ud_minb` events, ideas, programme and adopt decisions, unnamed office cards; ledger [usea_depth/MINORS_B.md](usea_depth/MINORS_B.md); generator `tools/usea_depth/minors_b/` | Native reachability, AI pacing and balance. Shilage exists in 1991–2005 only through the engine's own release mechanics; no release is authored | Provisional gameplay on mod-provenance geography; official Chronicle dates are used only as gates and news. Static-validated; native untested (#8) |

## Campaign arc implementation record

| Slice | Source layer | Static implementation | Native status |
| --- | --- | --- | --- |
| Belka prewar preparation and war-stage mechanics | Mod provenance context plus provisional gameplay; official ACES Chronicle 1995 / 03.25 is only the historical date reference | `ac_belkan_campaign.txt` focus/decision/event/idea files, attached to both existing prewar BLK trees; `ac_commit_belkan_war_campaign` gives the player and 1995 event one guarded start contract | Static regression implemented for tree continuity, AI timing, shared commitment and inherited notifications; native reachability and balance were not run in this round at the owner's instruction and remain pending under issue #8 |
| AI war-stage fallback | Provisional gameplay | `ac_on_weekly_on_action.txt` increments a bounded campaign-week variable and fires each missing stage once | Not tested in HOI4 |
| Victory, Wacht am Wal, and defeat postwar focus arc | Existing outcome flags plus provisional gameplay | `ac_belkan_postwar` focus tree and branch-gated events/decisions; no new borders or canon claims | Not tested in HOI4 |
| Economy integration | Existing repository economy prototype | All campaign economy effects are guarded by `ac_econ_ready` | Offline economy tests pass; native balance unverified |
| Ustio scaffold reconnection | Inherited Ustio focus/event files and existing Ratio outcome flags | Restored the initial child focuses, repaired one malformed coordinate, and reloaded the existing branch tree after live postwar outcomes; conventional victory is excluded because the inherited outcome annexes Ustio before handoff | Static-validated; no new borders/cores; native reachability unverified |
| Usea Depth minor states A: Chopinburg (CHO), Platania (PLA), Ferustia (FRU), Albard (ALR), Dorondo (DOR), Scandia (SCA) and Bulgurdarest (BLD) | Mod provenance geography and starting spirits; provisional gameplay for every national response; official ACES Chronicle anchors (1996 / 04.20, 1997 / 05.30, 1998 / 06.19, 1999 / 07.08, 2000 / 04.21, 2003-2005) used only as dates or read-only `ac_ucw_*` flags | Seven trees `ac_ud_<tag>_tree` in `common/national_focus/ac_ud_minor_<tag>.txt`, namespace `ac_ud_mina`, unnamed office governments through `ac_ud_minors_a_regime_*` (AI weight 0), idle-gated adoption decisions for old saves; counts, citations and every lore row in `docs/usea_depth/MINORS_A.md`; generator and tests in `tools/usea_depth/minors_a` | Not tested in HOI4; native acceptance remains under #8 |
| Usea Depth: Central Usea (`ac_ud_fcu`) | Official Chronicle anchors (1995 / 12.31 to 2005 / 09.26) and Super Weapons, Stonehenge and Megalith; mod provenance for the UTO, CNEA, the 1991 faction and Sinclair's 1991 term; everything else provisional gameplay. The emergency directorate and unity government are player-only alternate history | 294 focuses (172 in `ac_exp_fcu_opening`, 122 in `ac_ucw_fcu_tree`), 60 long-form events, 90 ideas, two unnamed offices and the `ac_ud_fcu_regime_*` effects. Extends the 1997 `FCU_ur_*` branch without duplicating it; reads the `ac_ucw` flags and never sets them; no borders, cores or ownership changes. Ledger: [usea_depth/FCU.md](usea_depth/FCU.md) | Static-validated by `tools/usea_depth/fcu/test_fcu.py`, including an offline World-harness run in which the AI keeps its 1991 government and Erusea still invades in summer 2003. Native untested; acceptance stays under #8 |

## The Peace We Inherit implementation

The approved expansion adds all four authored slices: 30 Belkan focuses; eight
each for Osea and Ustio; six each for Sapin and Gebet; targeted FATO/Recta/South
Belka briefs; six reciprocal reconstruction negotiations; and a preparedness,
relief and late-1999 record layer. See [the expansion ledger](PEACE_WE_INHERIT.md)
for source entries, affected namespaces, balance values, compatibility contracts
and the native acceptance checklist. It extends the existing postwar handoff
without replacing inherited governments or Ustio branches. The matrix above is
the earlier coverage baseline; these additions do not establish native reachability.
The authorized isolated [24 October native session](NATIVE_PEACE_WE_INHERIT_20261024.md)
adds engine observations and an explicit coverage CSV; seeded aftermath contexts
do not establish the natural war-to-settlement handoff.

## Coverage contract for new work

Every new lore/event slice should record:

1. source layer and exact citation/private reference;
2. affected country tags, focus IDs, event IDs, decision IDs, ideas, states, and localization keys;
3. whether it is implemented, static-validated, reachable, native-tested, disputed, or pending;
4. whether it changes an existing branch or adds a provisional gameplay branch; and
5. the next test or source needed to close the gap.

Existing roadmap issues remain authoritative: issue #6 covers canon/Joker 1, #8 covers approved native testing, #5 covers 2065/technology naming, #7 covers economy/workspace integration, and #4 covers 1.19 parity. This backlog expands their coverage without creating duplicate issue scope.
