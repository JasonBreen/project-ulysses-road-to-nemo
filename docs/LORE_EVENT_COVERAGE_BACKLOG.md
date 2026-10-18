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
| Recta | Country history, events, decisions, capitulation hooks; no dedicated focus tree | Write a branch contract before adding a tree or border | Open decision |
| Yuktobania | Country history, events, AI references; no dedicated focus tree | Define when and why it enters the continuation | Open decision |
| North Point | Country history/definition; focus files are commented/empty | Establish whether it is an active campaign actor or background nation | Open decision |
| Wider Usea wars | Histories/hooks for Erusea, Emmeria, Estovakia, Aurelia, Leasath and others | Add sourced chronology, actors, wars, peace outcomes, AI, and transitions | Later phase; not authored as a complete arc |
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

## Coverage contract for new work

Every new lore/event slice should record:

1. source layer and exact citation/private reference;
2. affected country tags, focus IDs, event IDs, decision IDs, ideas, states, and localization keys;
3. whether it is implemented, static-validated, reachable, native-tested, disputed, or pending;
4. whether it changes an existing branch or adds a provisional gameplay branch; and
5. the next test or source needed to close the gap.

Existing roadmap issues remain authoritative: issue #6 covers canon/Joker 1, #8 covers approved native testing, #5 covers 2065/technology naming, #7 covers economy/workspace integration, and #4 covers 1.19 parity. This backlog expands their coverage without creating duplicate issue scope.
