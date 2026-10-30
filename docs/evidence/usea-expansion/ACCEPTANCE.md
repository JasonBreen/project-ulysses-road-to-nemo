# Candidate acceptance record — 30 October 2026

**Status: implementation candidate; native release acceptance remains open.**
Base: `8f503d1de6b434031fcb110a6dd1dd7f26622a78`. Worktree:
`G:\Project-Ulysses-Usea-Expansion`, branch `codex/usea-art-expansion`.
The normal installed mod has not been synchronized by this task. Nothing was
published, pushed, merged or released.

## Static and offline coverage

`static-results.json` records commands and exit status; each `static-*.txt`
retains output. The runner is `tools/usea_expansion/run_checks.py`. It includes
campaign, fiscal economy, faction, aftermath, Continental War, supporting
countries, special projects, briefing, typography, strict authored assets,
engine GUI dependencies and generated-output consistency.

Focused regressions cover normal/continuous focus bounds and controls,
country-selection substitutions, direct fiscal page visibility in enabled and
disabled economies, event scroll controls, all authored scripted-GUI windows
and click targets, 69-country starting-leader coverage, retained mission/MIO
references, and harmless retired event handlers. FCU's four policy combinations,
opening/later handoff, partner interruption, expiry and duplicate replies are
exercised offline. This does not establish engine execution of every script.

The strict authored-asset gate reports 4,809 sprite definitions, 826 focus icon
bindings, and zero unresolved texture references. The effective engine/mod
dependency report has zero missing repaired-screen dependencies or conflicting
sprite definitions. Runtime-selected event pictures and flag/background
catalogues are explicitly distinguished. Operative/leader event layouts are
not included in the country/news visual-repair claim.

## Native observations before desktop control stopped

Installed reference: HOI4 **1.19.4.1.99a5**. A physical engine copy and disposable
profile were used at `G:\Project-Ulysses-Native-20261030-Expansion`.
These observations concern earlier candidates from this implementation session,
not a complete retest of the final candidate.

| Configuration | Observed | Retained evidence / limitation |
| --- | --- | --- |
| 3440×1440, scale 1.0 | Readable Belka country/character tooltip; Yuktobania 30-focus tree; Arkbird narrative scrolls separately from rewards and Start; focus zoom; 35-day opening focus starts and completes | `3440-belka-tooltip-after.png`, `3440-arkbird-top.png`, `3440-arkbird-scrolled.png`; before Steam images retained |
| 1920×1080, scale 1.0 | February save reload preserves completed YUK focus; Arkbird long text and continuous-focus rewards scroll; available/completed/unavailable states remain distinct | `1920-arkbird-top.png`, `1920-arkbird-scrolled.png`, `1920-continuous-rewards.png` |
| 2560×1440, scale 1.25 | FCU 18-focus opening loads; first focus completes; opening narrative appears; shortcut handoff loads the 36-focus later tree | `native-fcu-opening.json` is a sanitized save checkpoint; latest Steam screenshot shows the subsequently reported fiscal/news defects |
| Loading presentation | Official AC8 loading art appeared in the disposable game | `3440-ac8-loading.png` |

Natural progression: FCU played from January into March 1991. The March 3 save
records the player completing the treaty-secretariat opening, with ERU, NPT
and YUK AI completing their opening inventory/account focuses. Recta's
postwar entry remained gated. This is an early pacing checkpoint, not a
1991–2005 natural campaign acceptance run.

Shortcut coverage: existing playtest decisions opened the Usean calendar,
started the Continental War, formed ISAF and advanced to Los Canas. North
Point accepted the ISAF invitation during subsequent AI ticks. No complete
victory, defeat, armistice or avoided-war native outcome is claimed.

Desktop control was stopped with the physical Escape key. It was not resumed
in this repair pass. The latest fiscal-page repair, event-scroll/chrome repair,
200×160 country-event packaging, final icon spacing, FCU policy refinements,
Sinclair/office leaders and vanilla-mechanic retirement remain **native untested**.
No current-candidate after screenshot for the economy is claimed.

## Outstanding acceptance

- Recreate the fiscal and long-news defects and retain after evidence at all
  three display configurations; test every fiscal tab with the rule enabled
  and disabled, close/drag, keyboard behavior and overlapping event windows.
- Recheck final focus captions/art, long descriptions, selected/unavailable/
  completed/mutually exclusive states, continuous focuses, search and drag.
  Search/keyboard and window drag were not conclusively verified earlier.
- Verify starting leader names, descriptions and office pictures on new games;
  verify old-save government and crisis cleanup behavior without replacing
  saved leaders or replaying rewards.
- Exercise every expanded tree and all required outcomes, including FCU's four
  opening combinations, save/reload around handoffs, invalid partners,
  North Point neutrality/participation, Rectan recovery and Yuktobanian
  intervention/reform. Test special projects through DLC and fallback routes.
- Complete research/equipment-surface checks and natural AI/pacing checkpoints
  through the covered 2005 outcomes. Static success is not a substitute.

## Normal-profile preservation observation

An earlier comparison found all 953 protected files unchanged. The later
comparison detected 19 changed files and one added file: launcher/playset and
settings files, normal game logs, and CWIC repository Git logs. No protected
save file was listed as changed. The normal game's logs record a later launch
after desktop control stopped. Those changes were left intact; this task does
not claim a clean final whole-profile comparison or restore files from another
activity. The disposable payload, engine and profile remain separate.

Raw saves and a screenshot containing an unrelated Discord overlay are kept
outside the repository. The committed checkpoint contains only campaign facts,
version, date and a hash, without player-profile data.
