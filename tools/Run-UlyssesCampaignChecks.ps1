[CmdletBinding()]
param(
    [string]$ModRoot
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($ModRoot)) {
    $ModRoot = Join-Path $repoRoot 'mod\2985041246'
}
$ModRoot = (Resolve-Path -LiteralPath $ModRoot).Path
$scriptHost = if ($PSVersionTable.PSEdition -eq 'Core') { Join-Path $PSHOME 'pwsh.exe' } else { Join-Path $PSHOME 'powershell.exe' }
if (-not (Test-Path -LiteralPath $scriptHost -PathType Leaf)) { throw "Could not locate the current PowerShell host executable: $scriptHost" }

function Invoke-CheckedCommand {
    param(
        [string]$Label,
        [scriptblock]$Command
    )

    & $Command
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        throw "$Label failed with exit code $exitCode."
    }
}

Write-Host '== Project Ulysses campaign contract ==' -ForegroundColor Cyan
Invoke-CheckedCommand 'Campaign contract' { python (Join-Path $PSScriptRoot 'validate_campaign.py') --mod-root $ModRoot }

Write-Host '== Project Ulysses pull-request text checks ==' -ForegroundColor Cyan
Invoke-CheckedCommand 'Pull-request text checks' {
    python (Join-Path $PSScriptRoot 'Test-PullRequestText.py') `
        (Join-Path $repoRoot '.github\pull_request_template.md') `
        (Join-Path $repoRoot '.github\pr-bodies\pr-13.md') `
        (Join-Path $repoRoot '.github\pr-bodies\pr-14.md') `
        --self-test
}

Write-Host '== Project Ulysses Ustio continuity regressions ==' -ForegroundColor Cyan
Invoke-CheckedCommand 'Ustio continuity regressions' { python (Join-Path $PSScriptRoot 'Test-UstioContinuity.py') --mod-root $ModRoot }

Write-Host '== Project Ulysses static validation ==' -ForegroundColor Cyan
Invoke-CheckedCommand 'Static validation' { & $scriptHost -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Test-UlyssesStatic.ps1') -ModRoot $ModRoot }

Write-Host '== Project Ulysses economy tests ==' -ForegroundColor Cyan
Invoke-CheckedCommand 'Economy tests' { python (Join-Path $PSScriptRoot 'test_economy.py') }

Write-Host 'Native HOI4 launch/playtest: intentionally not run.' -ForegroundColor Yellow
