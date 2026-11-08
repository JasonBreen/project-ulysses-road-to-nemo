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
reference/technology warnings are retained as baseline offline findings. Finished
the physical engine copy with a non-deleting multithreaded copy after retaining
the sequential copy's completed files.
