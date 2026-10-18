# Pull-request guidance

The repository template follows the current Millennium Dawn / MD-OEM layout:
the description begins with `### Changes` and a short, direct scope statement.
The Ulysses additions keep that layout while recording validation, stacked
dependencies, installation scope, and native-test status.

Use a real UTF-8 body file with actual line breaks when publishing or updating
a pull request. For example:

```powershell
gh pr edit <number> --body-file .github\pr-bodies\pr-<number>.md
```

Do not build Markdown bodies with shell-escaped `\n` prose. The repository
check permits backslash sequences inside fenced code examples, but rejects
literal escaped newlines or disallowed control characters in prose.

Before updating a PR body, run:

```powershell
py tools\Test-PullRequestText.py .github\pull_request_template.md .github\pr-bodies\pr-13.md .github\pr-bodies\pr-14.md
```

PR descriptions must preserve substantive changes, exact validation evidence,
dependencies/base branches, and explicit native-testing caveats. Updating
formatting does not authorize merging.
