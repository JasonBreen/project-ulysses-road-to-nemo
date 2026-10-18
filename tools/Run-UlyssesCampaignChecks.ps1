[CmdletBinding()]
param(
    [string]$ModRoot = (Join-Path $PSScriptRoot '..\mod\2985041246')
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host '== Project Ulysses campaign contract ==' -ForegroundColor Cyan
python (Join-Path $PSScriptRoot 'validate_campaign.py') --mod-root $ModRoot

Write-Host '== Project Ulysses static validation ==' -ForegroundColor Cyan
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Test-UlyssesStatic.ps1') -ModRoot $ModRoot

Write-Host '== Project Ulysses economy tests ==' -ForegroundColor Cyan
python (Join-Path $PSScriptRoot 'test_economy.py')

Write-Host 'Native HOI4 launch/playtest: intentionally not run.' -ForegroundColor Yellow
