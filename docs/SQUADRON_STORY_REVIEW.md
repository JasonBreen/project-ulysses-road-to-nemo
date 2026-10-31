# Squadron story runtime and narrative review

This review covers the six-story working-tree candidate and the later runtime,
regional-context and flight-scene changes. The source/offline suite passes **24
tests**. No runtime correction was required by this independent follow-up. The
small wording recommendations and no-air-service fallback issues identified by
this review are resolved in source; their disposition is recorded below.
Artwork is a separate gate and was not evaluated by this runtime review.

## Material inspected

The compiler, schema, generated event/effect/trigger/on-action libraries and the
actual-script harness were inspected together with every conditional continuation,
its choices and the source/target of its callbacks. The six campaigns contain
120 core scenes, 240 substantive choices, 24 recurring original cast members and
18 personal conclusions. Their callback counts are BLK 8, UST 10, ERU 9, SNS 11,
EMM 9 and EVA 8. Core scene minimums range from 104 to 125 words; conditional
scene minimum length is enforced independently at 80 words.

The revised flight passages reviewed were BLK 8, UST 7, ERU 16 and SNS 14, plus
the capability-conditioned EMM 12 and EVA 17 service flights. EMM 12 returns to
the unopened family photograph before its choices; EVA 17 returns to the trainees'
corrected classroom sheet. Their earlier objects, option replies and later
callbacks therefore still refer to the decision actually offered. Pavel's old
shoulder injury does not become an untracked death or permanent disability.
No recurring core person is killed by these scenes or silently replaced later.

The war and capitulation accounts preserve a peace or continued-service base.
They do not award national victory, compel restoration, promise every civilian
route is safe, deliver national aid, remove sanctions or independently operate a
strategic installation. The incidents, weather, dialogue, personal relationships
and chapter dates remain approved original supporting fiction. The source-layer
ledger is [SQUADRON_CAMPAIGNS.md](SQUADRON_CAMPAIGNS.md#provenance-and-campaign-ownership).
No new official history, protected private continuity or named canonical city
mapping was added by this review.

## Context ownership

| Reader and chapters | Observed condition | Source ownership |
| --- | --- | --- |
| BLK 9 / UST 9 | Current control of existing capital districts 224 / 335 | Existing map/history plus engine control; no state transfer by the story. |
| BLK 17 / UST 17 | Actual bilateral faction membership | Existing faction state; the story does not create an alliance. |
| ERU 12 / SNS 12 | `ac_ucw_stonehenge_destroyed` | `common/scripted_effects/ac_ucw.txt`; the story only reads the established flag. |
| ERU 15 | Actual faction membership with FCU | Existing country/faction state; the scene does not settle a national dispute. |
| SNS 15 | Current control of existing district 310 | Existing project geography/control; no new canonical city or border claim. |
| EMM 11 / EVA 11 | `ac_anea_accord` | `common/scripted_effects/ac_anea.txt`; accepted procedures do not guarantee a delivered shipment. |
| EMM 16 / EVA 16 | `ac_anea_sanctions_active` | The same Anea owner; a squadron cannot waive the active policy. |
| BLK 8 (peaceful return) | No war, `ac_sq_air_capable` and no capitulation | A peaceful training flight; otherwise the simulator scene remains available. |
| EMM 12 / EVA 17 | `ac_sq_air_capable` and no capitulation | A narrow documented national air-service manpower observation, not individual-wing telemetry. |

All fifteen conditional variants explicitly exclude a capitulated host. The nine
wartime continuations additionally require actual war, no capitulation and the
same national air-service capability. Capitulation continuations take precedence
where authored. Variant precedence is compiled into mutually exclusive display
conditions; delivery snapshots exactly one context and any eligible callback.

The source tests execute the actual squadron libraries. External control,
faction, project and Anea states are explicit fixtures; this suite does not
execute those other owners' complete campaigns or establish their native timing.
Their defining and clearing sites were inspected to confirm the reader uses the
existing contract rather than inventing another outcome flag.

## Follow-up regression coverage

The earlier suite already exercised every core option, actual relationship
clamping, all eighteen BFS ending witnesses including mixed-choice trusted paths,
late entry, post-2005 completion, expiry, stale replay, cloned/current-original
identity, disabled rules, manual reading, deep-copy reload and a synthetic weekly
1991–2006 schedule without chapter-position shortcuts. These remain offline
models, not native AI or save serialization.

The follow-up adds or strengthens these actual-script checks:

- All fifteen policy, control, faction and flight contexts are positively
  delivered and archived with their authored callbacks where applicable.
- Missing live owner conditions, unrelated historical flags, restored district
  control and absent air service produce the base scene. Even when all external
  owner conditions are positive, capitulation excludes the fifteen variants.
- Every airborne war/service context falls back when the observed air service is
  absent. Choice execution preserves the modeled physical equipment, manpower,
  external policy flags and war state.
- Gaining capability, policy eligibility, faction membership or an earlier choice
  later cannot rewrite a previously delivered base archive or append a callback.
- Losing those conditions after a conditional scene cannot replace its archived
  continuation. Opening and closing these archives preserves all modeled country,
  global, control, faction, war, queue and news state.
- Country-scoped weekly dispatch executes one tick per eligible host. It does not
  nest another world iteration inside each ordinary country callback.
- Initialization after January 1991 skips the opening without its choice effects;
  existing final acts may complete after 2005, while a newly initialized unread
  post-2005 archive earns no historical relationship or training grants.

## Editorial findings

| Finding | Recommendation | Status |
| --- | --- | --- |
| ERU 16 capitulated prose distinguished its ground account from a flight debrief. | Use “Finish the account before speaking personally.” with the same flag, statistics and reply. | Resolved by narrative owner; source inspected. |
| BLK 6 wartime flight is already receiving airborne instructions, while option A's reply left a release sheet unsigned. | Make Eva record the unresolved restriction, which works both before and after takeoff. | Resolved by narrative owner; source inspected. |
| ERU 16 base account named a flight even when national air service is absent. | Describe the base return as a journey and its account; keep explicit military flying in the guarded war continuation. | Resolved by narrative owner; source inspected. |

## All-base capability fallback pass

Every base scene in BLK, UST, ERU, SNS, EMM and EVA (chapters 1–20 for each)
received a manual pass for a newly occurring military flight. A base may retain
stationary maintenance, hypothetical duties, a ground exercise, civilian travel,
recordings or a character's earlier service. Those do not establish a current
flight or per-tail engine telemetry. The pass made these concrete changes:

| Base scene | Correction | Preserved continuity |
| --- | --- | --- |
| BLK 8 | The ground trainer returns a simulated aircraft to its practice runway after a fault. The original peaceful flying paragraph is retained unchanged in `training_return`, gated by no war, no capitulation and observed air service; the existing wartime flight remains separately guarded. | Same title, two options, replies, choice flags, statistics and fault callback. The later remembered “landing” can be the explicitly simulated landing. |
| ERU 2 | The eleven-second navigation contest happens at a chart table using a weather problem. | Rivalry, stopwatch, damaged cup, both options and later references remain intact. Discussing a first difficult landing describes earlier personal service. |
| ERU 3 | Celine and Adrien disagree about what can be verified in the photograph, rather than a newly completed patrol. | Same uncertain identification, correction/private enquiry choices and future exaggerated legend. |
| ERU 5 | Adrien helps the disabled vessel from the shore operations desk; the civilian crew still performs the tow. | The photograph, exaggerated rescue caption, civilian signatures, cup callback and later missing-name scene remain intact. |
| SNS 4 | The uneventful patrol is a chart-table exercise with a missed route-sheet instruction. | The debrief quarrel, radio carried up the tower, open microphone, options and replies are unchanged. |
| ERU 16 | The narrative owner's neutral journey/account baseline is retained. | The airborne war and ground capitulation accounts, personal fear choices and earlier warning callback remain coherent. |

No new telemetry, physical equipment effects or national outcome ownership was
added. A dedicated actual-script test crosses peaceful/war, capable/incapable,
capitulated/independent and callback/no-callback states for BLK 8. It asserts the
expected ground, peaceful-flight or wartime text directly, executes the unchanged
choice, verifies inventory preservation, reverses the circumstances, and reads
the frozen archive without further effects. The other fifteen-context negative
and archive tests include the new peaceful-flight variant.

## Reproduction and acceptance limits

Run `python -B tools/squadrons/run_checks.py` to retain the generated-narrative and
24-case runtime results. [runtime-results.json](evidence/squadrons/runtime-results.json)
records the base commit, exact tested source/generated hashes, commands, exit
codes and timings; `runtime.txt` and `generated-narrative.txt` retain output with
repository paths redacted. Rerun it after any narrative/compiler edit. The CI
workflow has separate PowerShell steps for narrative generation, runtime tests
and `Test-SquadronArt.py`, so an art failure is not hidden by a later command.
The art test owns its independent packaging/reproducibility check.

The synthetic interpreter is fail-closed but is not the HOI4 engine. Native
country identity and capability observations, simultaneous event scheduling,
real save/reload, localization rendering, long-description scrolling, all three
display configurations, actual AI pacing, performance and artwork presentation
remain untested while native testing is paused. This review did not launch the
game, operate the desktop, change the installation or touch user saves. The
artwork packager, source PNGs, provenance records and image selection were left
to their separate owner.
