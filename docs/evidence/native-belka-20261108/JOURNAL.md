# Campaign journal

## Preparation

- Froze latest origin/main at 385d01a74b71227fa58140abc1496d81455ebd5d.
- Created an isolated test worktree; left the original story branch unchanged.
- Selected E: for engine/profiles/evidence because G: has insufficient free space
  for the engine and a campaign save archive.
- Started static, campaign-path and native-isolation preparation checks.
- All thirteen selected subsystem preflight commands passed. Campaign validation
  has zero errors/warnings; the map phase has zero errors and its two inherited
  placeholder warnings. Aggregate static validation remains in progress.
- Preservation manifest covers 838 protected files; engine executable SHA-256 is
  `bccc62909b6a1ec2c1d5a46ef18608e4d0c7cdc89ad341b7402a23c40f7a8037`.

No campaign choices or native progression recorded yet.

## Preflight host correction

The first aggregate invocation used Windows PowerShell 5.1 via `powershell`.
Its provenance phase failed because `System.IO.Path.GetRelativePath` is absent
from that host. The failed log is preserved. Reran the same wrapper under the
current `pwsh` host, consistent with the repository's current-host instruction.
No game source change was made for this invocation mismatch.

The current-host aggregate rerun passed, including installed-reference provenance:
four inherited baseline matches and zero new or path-independent matches. The
reference/technology warnings are retained as baseline offline findings. Resumed
the physical engine copy with a non-deleting multithreaded copy after retaining
the sequential copy's completed files.

The E: copies remained unusually slow. After unrelated activity freed more than
100 GiB on G:, switched the disposable engine and profiles to the same dated root
on G:. E: retains preflight logs and protected configuration/log backups. No E:
engine was launched. The pre-launch audit at 17:40:32 UTC found all 838 protected
files unchanged, with no additions. Partial generated E: copies will be removed
only after validating the G: candidate.

## Isolated no-mod control

- G: physical copy completed: 59,930 files, 10.367 GiB, zero failures/mismatches.
- Primary payload validated: 11,615 files exactly match source at c6473167
  (documentation-only descendant of frozen base 385d01a7).
- Launched the copied DirectX11 executable; observed the native main menu at
  3440x1440, scale1.0, Operation Postern 1.19.4.2.2da5 (0bdb).
- Runtime system.log reports 35 active DLC and zero active mods.
- At 17:47:19 UTC the post-launch audit found all 838 protected files unchanged
  with zero additions. Native logs were created under the disposable profile.
- The control error log contains the userdir-marker deprecation notice (copied
  launcher gameDataPath supplies the effective path) and repeating line238
  "Failed allocate data buffer" exceptions. Keep these as control diagnostics.
- Closed the control through its native Quit button and confirmed no HOI4 window
  or process remained. No Earth-country gameplay was exercised.
- Automatic approval review rejected recursive removal of the incomplete E:
  generated engine/profiles. No deletion occurred; retained the partial copies
  and continued with the validated G: session. No retry through another mechanism.

## Owner-directed globe restoration

- Primary startup was isolated: one active mod, 35 active DLC, checksum7918.
  Its post-launch audit at17:50:37 UTC again found all838 protected files unchanged.
- Before starting a campaign, the owner directed restoration of the original
  animated globe. Recovered the archive fallback and 35-tile layout; all35
  animation textures remain byte-identical to source commitc452cf3.
- Prevented the scrub generator from writing the globe and added regressions
  for preserved bytes, original tile bindings and non-destructive regeneration.
- Focused visual, responsive and interface checks pass; the full static wrapper
  with installed reference and preserved baseline also passes on the repair.
- Alt+F4 left the old setup rendering without controls. Closed only owned test
  PID52132 after checking its exact copied-engine path; no campaign/save existed.
  Archived the initial native logs before resynchronizing the repaired payload.
- Native confirmation passed at6636c641: original globe visibly rotates across
  separate screenshots, and the 1.19 background lookup warning is gone. Full
  static wrapper passed again. Latest preservation audit: 838 unchanged, zero
  additions at18:11:32 UTC.
- Selected Belka in the first 1991 bookmark, Regular difficulty, Ironman off,
  Canon AI Focuses checked. Inspected default rules and zero nation buffs without
  changing them. Started and read the welcome screen. Preserved the paused
  opening via the native Local save dialog as BLK_1991_01_01_12.hoi4. Extracted
  primary-opening.json without editing the save; date1991.1.1.12, playerBLK,
  difficulty normal, speed0. No first tick/monthly progression is claimed.
- Returned through the native exit-to-menu flow. The original globe still renders
  after leaving the campaign; evidence restored-globe-after-campaign-exit.png.
- Post-save preservation audit at18:21:32 UTC: all838 protected files unchanged,
  zero additions. Original workspace retains exactly its four pre-existing dirty
  paths. The full campaign and additional cases remain outstanding.
- Closed the isolated game using its native Quit button; confirmed the process
  and target window are absent. Post-exit audit at18:23:53 UTC passed: 838 unchanged,
  zero additions. Recorded the sanitized globe-restoration.json receipt. The art
  repair is complete; the broader 1991-2000 test remains at its saved opening.

## Resumed test and initialization repairs

- Resume audit at18:45:29 UTC: 838 protected files unchanged, zero additions.
  Revalidated the single enabled descriptor and exact 6636c641 payload parity,
  then launched the copied engine and reloaded the preserved opening normally.
- Land, naval and air doctrine screens all show no grand doctrine assigned.
  Captured N003 before evidence for all three; no console or save edits used.
- N002 source repair d7cedf5c removes14 malformed orphan lines while preserving
  all107 localization definitions and the BOM. Existing special-project checker
  now rejects malformed/unkeyed rows; native relaunch retest is pending.
- N003: verified12 installed grand-doctrine ID/folder headers read-only, repaired
  only invalid effect values across60 histories, and regenerated all four owning
  generators. Frozen source snapshots and baseline inventories are unchanged.
  Preserved whole-file fingerprints by projecting only reviewed doctrine effects;
  updated current-source registry and explicit repair receipts.
- Focused offline checks pass: Legacy17, World Foundation20 (one reference-only
  skip), Active Starts25 (three reference-only skips), native compatibility and
  special projects. All four generated-output checks and the exact legacy binding
  gate pass. Full static wrapper is in progress; native after evidence pending.
- Closed the exact test process through native Exit Game. Retained reproduction
  logs locally under evidence/logs/6636c641-N003-reproduction before payload sync.
- First aggregate rerun stopped at the cleanup receipt check's seven-file
  whitelist. Extended that explicit list to the60 N003 histories, retaining exact
  old hashes from all three preserved manifests and exact current hashes. The
  eight cleanup checks and the1050-input preservation/font checks now pass.
  This is validation metadata for the same doctrine-only source change.
- Post-reproduction audit at18:55:52 UTC again passed:838 unchanged, zero additions.
  The old opening save is retained under the explicit before-doctrine-repair name
  in the same disposable save directory, preventing accidental overwrite.

## Repaired opening and first human-play attempt

- Full aggregate static wrapper passed on c159a742 using the installed reference
  and preserved baseline; log N002-N003-static-retest.log. Native fresh start
  assigns Mobile Warfare, Fleet in Being and Strategic Destruction. Saved and
  reloaded the repaired opening normally; all three assignments persist. N002
  special-project localization and N003 doctrine errors are absent from logs.
- Post-launch audit at19:02:48 UTC passed:838 unchanged, zero additions.
- Human decisions from the reloaded opening: The Crisis Continues; research New
  Line Of Construction Vehicles, Charles Fort's Industrial Theory, Improved
  Infantry Equipment I with Heckler & Koch, and Radio; civilian factories in
  Dinsmark then Zentrum Belka; support equipment increased from one to two
  factories;24 rubber imported from Chopinburg for three civilian factories.
  Recorded N005 interface problems and O001 coal/O002 technology-date observations.
- Clock advanced through1 January, then crashed at1991.1.2.1. No console, edited
  save, tag switching or observer mode used. Unsaved opening decisions are lost;
  the repaired pre-decision save is intact. N006 retains the access-violation
  bundle and raw logs locally. Last visible observation was1991.1.1.18; the crash
  log reaches1991.1.2.1. The primary-through2000 case is blocked pending repair.
- Post-crash audit at19:12:57 UTC passed:838 unchanged, zero additions. Archived
  logs before relaunch. Exact unchanged c159a742 payload revalidated11615 files;
  relaunch PID27124 is an explicitly labeled reproduction run, not campaign progress.

## Event isolation retest and fiscal initialization blocker

-8072d3fa isolates the authored event directory. Full static wrapper passed.
  Loaded the same opening, advanced to6 January, saved/reloaded, and continued
  through13 January19:00 without the first-day crash. This was a diagnostic,
  without focus/research/build decisions. N006 native repair retest passed.
- Preservation audit20261108T192153Z:838 unchanged, zero additions.
- Fiscal dashboard showed zero GDP/output and no public funds. Refresh did not
  change it. A new8072d3fa Belka start reproduces zero GDP before any save/reload.
  N007 recorded; the main human campaign remains at its opening checkpoint.
- Closed the exact isolated engine through native Exit Game. Archived logs under
 8072d3fa-N006-pass-N007-before before generator repairs.

## Healthy opening and first monthly boundary

-6b350f17 fresh full-mode Belka initializes GDP4361.99998 and positive public
  funds. Native opening screenshot and Jan1.16 save preserved. The full static
  wrapper passed before this launch; explicit native trigger inversion and
  comparison parser errors are absent. Preservation audit193627Z passed.
- Replayed the human opening choices above, added two parallel infantry divisions
  for one cycle each at Dinsmark, and advanced on speed3 with observation. The
  Crisis Continues completed January31; read Nation In Pieces and chose its
  sole God Save Belka response. No second focus selected before the fiscal check.
- February3.5: first monthly settlement is absent (N008), with the opening
  balances unchanged and an empty ledger. Paused and saved this state. No console,
  tag switch, observer mode or edited save used in the primary campaign.
- Engine closed normally. Archived6b350f17 logs. Preservation audit195128Z passed:
  all838 protected files unchanged, zero additions. Repair qualifies numeric date
  references as global.date per installed engine documentation and usage; native
  replay from the healthy pre-boundary opening remains required.

## Global-date repair replay and new crash

- e7fd76f2 full static wrapper passed (N008-static.log), including29 economy and
 14 settled-ledger tests in focused runs. Exact11615-file payload validated.
- Loaded the healthy Jan1.16 save and replayed all opening decisions normally;
  saved the managed opening atJan3.5. Continued toJan20.2 on speed3. Assigned
  Aayden Kreutzberg to Hochseeflotte and ordered Naval Exercises. No army orders
  yet: injected keyboard chords and drag selection have not worked reliably;
  mouse controls remain usable. This is a control limitation under investigation.
- Resuming the clock was followed by a distinct C++ exception (N009), bundle
  hoi4_20261108_150749. Causality is unconfirmed. Preserved logs and Jan3.5 save.
  February native settlement acceptance is still pending. Relaunching unchanged
  e7fd76f2 for reproduction, with ordinary controls and no edited saves.
- Post-crash audit20261108T200917Z passed:838 unchanged, zero additions.
- Unchanged managed-opening replay assigned the same admiral and exercised the
  same fleet atJan3.5; resuming reproduced the exact exception stack. Bundle
  hoi4_20261108_151209 retained. Dump type is std::bad_optional_access. Missing
  sea-terrain minimum_seazone_dominance values identified against installed
  definitions; repair is not yet applied or natively tested.
- User explicitly paused playtesting to play AC8. Confirmed no HOI4 process is
  running. No further native inputs, launches or profile changes. Last audit
  20261108T201339Z passes838 unchanged, zero additions. Resume only when the
  user asks; begin with N009 repair/retest from the Jan3.5 managed save, then
  finish the N008 monthly-settlement replay. No campaign acceptance claimed.

## Static follow-up on a separate branch, 9 November 2026

- No native input. HOI4 not launched; the session directory, profiles and saves
  were read only for screenshots.
- Merged this branch onto current main in `claude/codex-work-fixes-ed7947`; the
  only conflict was the generated country registry, which was regenerated.
- Applied the N009 terrain candidate, repaired the N004 bookmark binding and the
  N005 labelled backdrops, and bound the installed doctrine sprite names. Causes
  of O001 and O002 recorded. Details are in BUGS.md under the same date.
- Native retests owed: N009 fleet exercise from the Jan 3.5 save, N004 scenario
  screen, N005 research and doctrine screens, then the N008 February settlement.
- Pull-request checks then failed on five jobs. All five traced to session
  repairs that other generators and preserved-source receipts had not
  followed: bare `date` in four more generators (N008), and pins on the
  pre-repair economy, reconstruction and country-history text (N003, N007,
  N008). Repaired statically and recorded in BUGS.md. The remaining `>=`/`<=`
  shorthand outside the fiscal blocks is listed there as open.
