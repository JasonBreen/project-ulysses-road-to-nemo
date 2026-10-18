---
name: validation-integration
description: Validate Project Ulysses changes, distinguish static from native evidence, and prepare safe isolated worktree/PR integration.
---

# Validation and integration

Use this skill before handing off a branch or opening/updating a PR.

- Start with `git status --short --branch`, `git log -1 --oneline`, and `git worktree list`. Preserve unrelated worktrees.
- From the repository root run `tools\Test-UlyssesStatic.ps1`; optionally pass a read-only `-ReferenceGameRoot` and `-BaselineRoot`.
- Inspect the diff for duplicate IDs, missing localization, new imported vanilla files, hard-coded developer paths, and accidental baseline edits.
- Run repository-provided offline tests when the changed system has them. Do not launch HOI4 while native testing is paused; never describe static or offline checks as runtime success.
- Before a PR, fetch current `origin/main`, rebase or merge only on the isolated branch if safe, record the exact head SHA, push the branch, open a ready-for-review PR, and leave it unmerged. Track exact-head CI and review feedback.
- If a check fails, fix in scope or report the blocker; do not force-push or broaden the change silently.

Acceptance: clean intended diff, static checks recorded, native status explicit, PR link/head/CI reported, and no automatic merge or release.
