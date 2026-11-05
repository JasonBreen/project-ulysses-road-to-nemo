# Ace Combat 04 and 5 campaign expansion

This is the implementation of the privately approved 5 November 2026 campaign
plan, based on integrated `main` at `5b74e504`. The campaign still starts in
1991. Native testing and normal-install synchronization remain paused.

## Delivered content and ownership

The deterministic compiler in `tools/ac_campaigns/build.py` delivers 186 additive
shared focuses: 24 each for ERU, FCU, OSE, YUK and BLK, and six each for SNS,
NPT, AMB, UGE, DEL, SBK, SAP, UST, GEB, REC and FAT. These are a separate
approved expansion, not a reinterpretation of the original 1,028-focus budget.
Alternative policies are included in those counts; no playthrough completes
both policies in a pair. `manifest.json` records every focus purpose and operation.

The four major national lanes cover preparation, military/coalition endurance,
command under pressure and settlement. Belka instead reads the earlier settlement
and offers institutional resistance or support for a tagless covert network.
The eleven supporting countries keep their own receiving, transport, inspection,
civil-protection, access, sovereignty, transit or council mandate.

The new `ac_camp` namespace owns funded work, scene delivery, choices, personal
consequences and journals. Existing `ac_ucw` and `ac_cpw` effects remain the writers
of war stages, declarations and settlements. Their stage prerequisites now read
the completed operations when the expansion is active. Legacy source fixtures
that do not load its startup retain the earlier owner contract.

Each operation has a paid start, a maturation interval, a deadline and exactly
one success/failed/cancelled/interrupted result; the clinic can instead close as
a limited arrangement. Completion rechecks the unexpired deadline as well as
the current context. It costs 25 PP, two real P1
institutional-capacity points and the existing programme fee in enabled fiscal
play. A macro transaction must succeed before the nonfinancial costs are spent.
The occupied clinic uses FCU as its explicitly consenting sponsor because the
institutional owner refuses domestic authorizations from a capitulated
government. The sponsor pays through its real owners when the operation starts;
San Salvacion's private accounts are not bypassed or rewritten. Keeping the
patient list private still allows civil consent. A restricted route can close
as a limited arrangement, distinct from full delivery and outright failure.
Enabled but unready fiscal owners cannot authorize work. Disabled fiscal play
retains the political and institutional costs. No refund or completion is
manufactured after interruption. Result rows are free, read-only records.

Present deployment and territorial requirements are real observations: air
operations need deployed aircraft and personnel; landings need an actual
foothold; liberation requires state 310 under SNS control. They do not establish
combat telemetry or an official order of battle. No operation spawns forces.

Foreign offers require an extant, eligible receiver and an actual answer.
Refusal cancels the offered work. A vanished, capitulated, subject or hostile
receiver cannot complete it merely because it accepted earlier. Offers confer
no automatic faction membership, base, guarantee, resource transfer or war.

## Original stories and meaningful alternatives

The initial San Salvacion sequence has twelve long scenes, six choices and three
perspectives: the clinic and its local administration, Erusean occupation command,
and an ISAF liaison. Its separate closure scenes cover a completed route,
restricted/interrupted arrangements and failure, with independent ERU/FCU accounts
and a later liberation return to the clinic. The clinic staff are anonymous,
original supporting fiction, not newly asserted game characters.

Scenes 7-12 each answer one of the six actual earlier replies with a specific
paragraph. Dispatch captures that paragraph once, and the journal uses the same
captured variant. A private patient list, a restricted checkpoint, a refused
sponsorship, the inquiry channel, retained correspondence and reserved observation
therefore receive distinct later accounts. Unanswered choices retain neutral text.

The other authored scenes cover the engineering families, maritime preparation,
the battery, Yellow Four/Thirteen, Wardog's receiving island, Yuktobanian crews
and evacuation, protected evidence, rescue preparations, the political rescues,
the Arkbird and final interception, and Belkan archives, witnesses and the network.
Sixteen shorter national interludes give every covered country its own account.
The narrative source has 73 core events, including those sixteen interludes.
Wardog, Nagase, Grimm, Chopper, Blaze and Pops receive original supporting scenes;
the Mobius and Yellow perspectives include flight preparation, maintenance,
radio work and personal consequences.
The editable narrative source is `tools/ac_campaigns/narrative.py`.

The writing references were the installed TNO Guangdong scenes and Requiem's
Shukshin/Omsk scenes. Their authorship is not imported. New prose uses recurring
objects, conflicting institutional interests, private consequences and later
callbacks; the existing original squadron stories and their immutable art/source
receipts remain untouched.

Delivered scenes have a thirty-day reply window. Silence is recorded as
unanswered, without granting either choice. Replies require the actual pending
window and current eligibility. Archives retain the delivered text and expose the
recorded choice; their options grant nothing. Stale events have a harmless close.

Yellow Four's alternate preservation requires maintenance completed before the
battery result. Yellow Thirteen's withdrawal must be earned before the terminal
settlement. Chopper's alternate outcome requires rescue coverage completed before
29 November. Fates close once and cannot be backfilled by later preparation.
First entry after the relevant period leaves personal history unknown rather
than retroactively assigning a death or rescue. Original casts are not killed,
revived or reassigned by this module.

Stonehenge has three guarded dispositions: destruction, disablement, or securing
the intact engineering site. Intact capture requires actual SNS control of state
310. All remove the enemy railgun effect; only destruction sets the existing
destruction flag. Megalith's conclusion requires its completed operation.
The second submarine can be recalled through Yuktobanian preparation, in which
case the historical destruction news is suppressed. The opposing strike cannot
claim a withdrawn carrier as a target. Recall likewise cannot claim a carrier
after the successful strike. If both operations are pending, the first recorded
success blocks the other's completion; its spent costs remain spent.

Belka's investigation and network paths can expose witnesses, build a channel,
influence procurement or contest strategic access. Foreign protected evidence
and domestic witness work can block that access. The final account waits for the
Pacific campaign's actual closure before recording an explicit alternate network
success or exposure. Strategic access imposes a temporary command penalty on both
principals; protected foreign evidence or a domestic witness removes it and
blocks further access. It does not declare Belka at war
or equate its government/population with the network.

The earned AC5 peace route requires the two successful political rescues and
final interception, current independent principals and a campaign-owned,
untainted bilateral war. A stricter participant scan excludes every other current
belligerent, including subjects. Osea sends a fourteen-day offer; Yuktobania must
accept while every condition still holds. Only then is bilateral white peace
requested and the existing owner asked to observe cessation. Refusal, silence,
an expired offer or a new participant never terminates a war. A fresh offer after
refusal or expiry costs the normal programme authorization and has a thirty-day
renewal cooldown. Earlier refusals remain in the record.

## Provenance, source limits and compatibility

`tools/ac_campaigns/sources.json` records exact references and affected families.
The official Chronicle and superweapon pages establish broad chronology and
named assets. Character interludes were compared against identified reproductions
of the game's dialogue; those secondary transcripts are explicitly identified.
All new conversations, clinic incidents, policies, numerical values, durations,
mandates, covert operations and alternate fates are original fiction/provisional
gameplay. They are not additional official history.

The four source layers remain separate. No Joker detail, new officeholder,
postwar border, corporate origin, 2065 event, state 171 interpretation, core,
province geometry or new place-to-state mapping is added. Starting rosters,
bookmarks, old personal stories and normal profiles are preserved.

Focus imports use a marked additive block and are present in every inherited
tree in a multi-tree country file, including the Belkan continuation tree.
The partner and FAT/SBK generators preserve those blocks on regeneration.
Existing war, national and personal-story owners remain separate.
Older national-tree preservation checks validate and remove only the exact
registered campaign imports before comparing the remaining tree to its unchanged
capture. Missing, duplicate or unknown campaign IDs fail that restoration.

Artwork is original diagram/control geometry composed from the existing Ulysses
glyph library. `assets.json` records actual runtime consumers, DDS hashes,
dimensions and exported PNG masters. Idea, decision and category bindings use
their actual engine naming conventions. The reference mods supplied no pixels.

The older event-picture capture remains unchanged. Its proof restores exactly
two registered Megalith gameplay edits through
`tools/ac_campaigns/event_migration.py`, then compares the entire ordered event
AST against that historical capture. Added rewards, altered guards, missing
nodes or unrelated event edits still fail. This records the separately approved
gameplay work without recapturing the picture-only baseline.

The aviation and naval preservation captures also remain unchanged. Their separate
`tools/ac_campaigns/reviewed_owner_updates.json` receipt enumerates only
`ac_ucw_eru_war_tick` and `ac_ucw_destroy_megalith` as changed functions, pins the
other 25 UCW function bodies and requires canonical output of that protected
scripted-effect file. The owner check uses `--check --check-owner-effects` so
unrelated PNG serialization does not enter the aviation/naval contract. Complete
UCW artwork validation remains in the separate full generation and picture checks. No new
function is added to or removed from that protected owner, and the existing
financial and history repair contracts retain their own separate scopes.

## Reproduction and acceptance

With the repository's pinned Pillow 11.3.0 and Python 3.12:

```text
python -B tools/ac_campaigns/build.py --check
python -B tools/ac_campaigns/build_art.py --check
python -B tools/ac_campaigns/test_campaigns.py
python -B tools/ac_campaigns/run_checks.py
python -B tools/build_continental_war.py --check
python -B tools/content_waves/build.py --check
python -B tools/analysis/campaign_path_report.py --campaign all --format json
```

Run `tools/Test-UlyssesStatic.ps1` with the current PowerShell host, the editable
mod root and the read-only installed reference where available. Source/offline
execution is not native parsing, balance, AI pacing, rendering or serialization.
The source fixtures in `tools/ac_campaigns/fixtures.json` are opt-in observations,
not installed or fabricated native saves. Native acceptance remains under #8.

The independent runner retains individual commands, exits and raw-log hashes in
`runtime-output/ac04-ac05/results.json`. It hashes the script inputs before and
after the pass and fails if they changed. Those receipts establish source and
offline execution evidence only.

Pass `--powershell` with the current host executable to include the full static
suite and a warning comparison with the immutable starting revision. Add
`--reference-game-root` for the optional read-only installed reference. The
runner uses the same Python interpreter for child checks and records every exit
independently; no failed step is hidden by a later successful one.

When native testing is separately resumed, acceptance must cover ordinary 1991
progression as well as the opt-in late fixtures, both AI and human actors, the
sixteen focus-tree imports, operation rows and event pictures, all fiscal modes,
and save/reload across pending replies, deadlines, character fates and peace
offers. The occupied clinic needs both sponsored delivery and restricted closure;
the battery needs each disposition and a later loss of custody; the Pacific
settlement needs refusal, expiry, acceptance and a third-party interruption.
Record native parsing, rendering, pacing and serialization separately from the
source checks. No native fixture has been installed or run for this change.
