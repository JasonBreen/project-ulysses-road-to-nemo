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
- Native confirmation of the restored animation is next; campaign still unstarted.
