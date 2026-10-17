# Open the portable workspace

Open [Project-Ulysses.code-workspace](../Project-Ulysses.code-workspace) with VS Code's **File > Open Workspace from File**. Its single folder is `.`, so it follows this checkout when moved or opened in a worktree. No personal `.vscode` settings existed in the inspected baseline and none were overwritten.

Use **Terminal > Run Task**:

- **Ulysses: static validation** runs the existing PowerShell map/reference suite.
- **Ulysses: economy validation** runs the stdlib script and accounting tests.
- **Ulysses: validate all** runs both in sequence; it is also the default test task.

Prerequisites are already-installed PowerShell 7 (`pwsh` on PATH) for static checks and Python 3.9+ for economy checks. The Python task prompts for an executable command or path; the default is `python`. Enter an installed Python executable if that command is unavailable. The task invokes a process with separate arguments and works with paths containing spaces. It does not install Python, an extension or other software. CI uses its own Python setup independently of the desktop.

Equivalent commands from the repository root:

```powershell
pwsh -NoProfile -File tools/Test-UlyssesStatic.ps1
python -m unittest discover -s tools -p test_economy.py -v
# Optional PowerShell wrapper; supply an installed executable if needed:
pwsh -NoProfile -File tools/Test-UlyssesEconomy.ps1 -PythonCommand python
```

The workspace contains no absolute personal paths, credentials, extension recommendations, editor preference overrides, auto-start tasks, game launch task, security settings or workspace-trust changes. Tasks run only when selected. The map suite's inherited internal invocation behavior is unchanged.

This is a VS Code-compatible JSON workspace with standard process tasks. Its relative paths, task targets and absence of personal/security settings are covered by automated checks. Native IDE opening/task execution has not been exercised through desktop control. Antigravity was not launched or verified; if an installed version supports VS Code workspace files, the file may be useful there, but compatibility is not claimed.
