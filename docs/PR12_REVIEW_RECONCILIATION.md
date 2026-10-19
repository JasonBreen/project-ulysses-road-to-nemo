# PR #12 review reconciliation

This record reconciles the review findings against merged head `2a55a2f1128e3439b0ff8f9e28ae3f2996fd0494` and the follow-up repair branch. It is static evidence only; HOI4 was not launched.

| Finding | Status | Evidence in the follow-up |
| --- | --- | --- |
| Nuclear-ending `world_event.2` could replace the defeat tree | Confirmed and fixed | The nuclear event sets `ac_postwar_wait_for_defeat_tree` and no longer fires `world_event.2`; inherited `belka_dlp_lost.7` fires it after the defeat tree, and the popup clears the wait flag. |
| New opening branch bypassed established chronology | Confirmed and fixed | `ac_belkan_prewar_briefing` now requires `BLK_the_crisis_continues`. |
| Postwar decision categories were missing | Confirmed and fixed | Added `ac_postwar_continuation` and `ac_postwar_local_settlement` categories and localization. |
| Neutral fallback was unguarded and could dead-end | Superseded by merged fix | The merged code already restricts it to unknown outcome flags and supplies a neutral settlement/legacy path. The follow-up regression locks this behavior. |
| Demobilization focus/decision localization collision | Confirmed and fixed | Preserved the established `ac_postwar_demobilization` ID in both the focus and decision namespaces; both use the supported shared label so no save identifier is renamed. |
| Duplicate continuation description/option key | Confirmed and fixed | The neutral option now uses `ac_continuation.1.e`; `.d` remains the event description. |
| Opening-stage decisions could run simultaneously | Confirmed and fixed | Each opening decision excludes the other with `has_decision`. |
| Local recovery `allowed` depended on a late flag | Confirmed and fixed | `allowed` uses stable FAT/GEB/REC tags; dynamic settlement flags remain in visibility/availability. |
| Continuation idea descriptions were missing | Confirmed and fixed | Added descriptions for narrow peace, occupation burden, and guarantor ideas. |
| Wartime ideas survived the postwar handoff | Confirmed and fixed | Added shared `ac_clear_belkan_campaign_ideas` cleanup to all four handoff outcomes. |
| AI fallbacks raced active decisions | Confirmed and fixed | Weekly thresholds are now `>18`, `>22`, and `>26` weeks, with stage-relative resets and pending locks preventing a fallback or sibling decision during the one-day delayed dispatch. `days_remove` is decision cleanup timing after completion, not an expiry window. |
| Validator omitted continuation coverage | Confirmed and fixed | Contract now covers continuation decisions, ideas, scripted effects, events, localization, categories, old defeat-story handoff, duplicate keys, AI syntax, and fallback timing. |
| Aggregate PowerShell wrapper swallowed child failures | Confirmed and fixed | `Run-UlyssesCampaignChecks.ps1` checks `$LASTEXITCODE` after every child; `Test-RunUlyssesCampaignChecks.ps1` injects a failing child and verifies nonzero propagation. |
| Neutral settlement penalty was not removed | Confirmed and fixed | `ac_campaign.35` removes `ac_postwar_unclassified_settlement`. |
| Focus AI weights used decision syntax | Confirmed and fixed | Campaign focus `ai_will_do` blocks use `factor`, not `base`. |

## Follow-up evidence

- Campaign review regressions: passed.
- Campaign contract: 0 errors, 0 warnings.
- Economy tests: 27/27 passed.
- Static/map validation: 0 errors; 3 inherited design warnings.
- Reference audit: 16.48 seconds, 0 errors, 0 missing focus references, 0 missing owned event references; 3,180 inherited archive localization warnings.
- No-vanilla comparison: 13 inherited baseline matches, 0 new matches, 0 path-independent matches, 0 warnings.
- Wrapper negative regression: passed.

Native parser, launch, save/load, AI long-run, and gameplay acceptance remain unverified by design.

## PR #13 review reconciliation

- Stable IDs: preserved `ac_postwar_demobilization` for both the focus and decision objects; the shared localization label avoids renaming either save key.
- AI fallback timing: `ac_campaign_war_weeks` resets inside each guarded stage event; later fallbacks use relative thresholds `>22` and `>26` after the initial `>18` threshold.
- Idempotency: stage decisions set a pending transition lock, dispatch their guarded events, and avoid duplicating stage flags, ideas, and economy effects in the decision completion block.
- Pending transitions: both opening decisions set and check the shared stage-one pending lock before their one-day delayed dispatch; later decisions and weekly fallbacks remain blocked until the stage event clears its lock, and postwar cleanup clears stranded locks.
- Validator coverage: all five continuation decisions are enforced, and mutation tests prove removed decision/localization entries fail validation.
- PowerShell portability: the negative wrapper test resolves the current host and also exercises the available alternate supported host.
- Focus layout: the inherited `(8,0)` anchor now places the campaign opening at `(12,1)` with non-overlapping child nodes; structural regression coverage computes absolute positions.
