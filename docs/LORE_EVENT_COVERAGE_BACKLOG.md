# Lore and event coverage backlog

This is a source-traceable coverage backlog for the private continuation. It is not a claim that every row is official canon or that every scripted definition is reachable. “Static” means present or reference-checked in files; “native” requires an approved HOI4 run and is currently out of scope.

## Source layers

| Layer | Use | Rule |
| --- | --- | --- |
| Official | Project Aces/ACE COMBAT games, manuals, official archive, publisher material | Use for dates, borders, names, characters, equipment, and established relationships. Cite the primary source. |
| User-authored | Sam’s established Joker 1 continuity | Preserve as user-authored; compile exact details before implementation. |
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
| Postwar handoff | world_event.2 previously only set ac_continuation_active | Consume the flag exactly once and expose follow-on systems | Implemented; native reachability unverified |
| Occupied/affected states | Existing transfers to South Belka, Gebet, Recta, FATO | Source-backed borders, cores, administration, resistance, and local consequences | Existing state effects are mod provenance; decisions are provisional |
| Osea politics | Election content and AI references exist; some branches were commented in the archive | Verify election reachability and postwar coalition/guarantor behavior | Static references; native unverified |
| Ustio | Shared focus/events, occupation and reconstruction hooks; repaired initial focus exposure and guarded postwar tree handoff | Trace postwar sovereignty, resistance, and diplomacy; native focus reachability | Static implementation in this slice; mod provenance only, chronology open |
| Sapin | Prewar tree, politics, revolt/demobilization content | Connect postwar government and war-cost consequences | Existing scaffold; chronology open |
| Gebet | Prewar tree, decisions, industrial/resource content | Connect settlement, reconstruction, and diplomatic effects | Existing scaffold; chronology open |
| Recta | Country history, events, decisions, capitulation hooks; `recta.1` localised; `rec_postwar_consolidation_focus` (`common/national_focus/REC.txt`, 13 focuses), ideas in `common/ideas/recta.txt`, AI in `common/ai_strategy/REC.txt` | Native reachability and AI behaviour of the tree | Static contract implemented as mod provenance and provisional gameplay. Branches cover Gebet relations, hardline versus reform communism and FATO relations. `REC_local_recovery_programme` waits for `ac_postwar_local_recovery` and reads the `ac_pwi.76` choice flags. No `transfer_state` and no new borders; checked by `tools/Test-UseaActors.py`. Native unverified. |
| Yuktobania | Country history, events, AI references; `yuktobania_fp.1` options now record `YUK_fp_intervened` / `YUK_fp_stood_aside`; `yuk_reform_focus` (`common/national_focus/YUK.txt`, 14 focuses), ideas in `common/ideas/yuktobania.txt` | Native reachability and AI behaviour of the tree | Static contract implemented. The post-intervention and non-intervention reform branches are mutually exclusive, and both end by replacing `yuk_top_heavy_command_structure` (mod provenance, provisional gameplay). The Arkbird debris-clearing branch is available from 8 October 1999 and sets `ac_yuk_arkbird_partner` (official: Chronicle 1999 / 10.08; effects provisional). There are no leader changes and nothing is dated after 2005. Native unverified. |
| North Point | Country history/definition; `npt_pre_continental_war_focus` rebuilt from the commented sketch (`NPT.txt`, `NPT_pre_continental_war.txt`, 15 focuses); new ideas in `common/ideas/north point.txt`; AI in `common/ai_strategy/NPT.txt` | Native reachability; PR A must set `ac_ucw_isaf_formed` for the Host ISAF branch to open | Static contract implemented. The 1991 election is a player choice and never sets a result (mod provenance). Isolation and FCU/UTO alignment are mutually exclusive. `NPT_host_isaf` reads `ac_ucw_isaf_formed` and sets `ac_npt_hosts_isaf` (official: Chronicle 2004 / 09.16; effects provisional). The rest of the tree works if the flag never appears. Native unverified. |
| Wider Usea wars | Histories/hooks for Erusea, Emmeria, Estovakia, Aurelia, Leasath and others | Ulysses fallout (2000–2003) and the Usean Continental War (2003–2005) as namespace `ac_ucw`; 1997 Usean coup recorded as an unscripted gap | Sources compiled in [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md); not yet authored |
| Characters | Static leaders/advisors/military roles and portraits | Replace placeholders, add biographies/dates only from sources, connect character exits to events | Partial mod provenance; audit required |
| Joker 1 | Sam outline: Ustian-born, Belkan ties, Moon11/Shadow22, Watchtowerorganization, Cope, Tasha’s mother | Compile exact dates, locations, motives, sequence, and source/private references | User-authored; do not infer |
| Organizations/corporates | Four MIO files; OTEC references in existing scripts/localization | Source and implement corporate history, procurement, rivalries, and later organizations | Partial/provisional; no dedicated Neucom/General Resource package found |
| Technology/equipment | 1991–2005 markers and inherited engine IDs | Provenance, localization, era gates, and later-war source audit | Open; issue #5 |
| Geography | 11,352 provinces, 612 states, 326 regions | Resolve state 171 and 203 XXX regions; source every later border | Open geography decisions |
| 2065 horizon | Engine cutoff contract through 2065-12-31 | Authored, source-backed content is not established for every year; do not fill with invented history | Engineering target only |

## Campaign arc implementation record

| Slice | Source layer | Static implementation | Native status |
| --- | --- | --- | --- |
| Belka prewar preparation and war-stage mechanics | Mod provenance context plus provisional gameplay | `ac_belkan_campaign.txt` focus/decision/event/idea files, attached to the existing BLK tree and war-start contract | Not tested in HOI4 |
| AI war-stage fallback | Provisional gameplay | `ac_on_weekly_on_action.txt` increments a bounded campaign-week variable and fires each missing stage once | Not tested in HOI4 |
| Victory, Wacht am Wal, and defeat postwar focus arc | Existing outcome flags plus provisional gameplay | `ac_belkan_postwar` focus tree and branch-gated events/decisions; no new borders or canon claims | Not tested in HOI4 |
| Economy integration | Existing repository economy prototype | All campaign economy effects are guarded by `ac_econ_ready` | Offline economy tests pass; native balance unverified |
| Ustio scaffold reconnection | Inherited Ustio focus/event files and existing Ratio outcome flags | Restored the initial child focuses, repaired one malformed coordinate, and reloaded the existing branch tree after live postwar outcomes; conventional victory is excluded because the inherited outcome annexes Ustio before handoff | Static-validated; no new borders/cores; native reachability unverified |

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
