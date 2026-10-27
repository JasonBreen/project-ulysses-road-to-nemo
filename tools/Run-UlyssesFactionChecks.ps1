[CmdletBinding()]
param(
 [string]$ModRoot = (Join-Path $PSScriptRoot '..\mod\2985041246'),
 [string]$ReferenceGameRoot,
 [switch]$IncludeCampaign
)
$ErrorActionPreference = 'Stop'
$hostPath = if ($PSVersionTable.PSEdition -eq 'Core') { Join-Path $PSHOME 'pwsh.exe' } else { Join-Path $PSHOME 'powershell.exe' }
$pythonHost = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
$pythonArguments = @('-B', (Join-Path $PSScriptRoot 'Test-UlyssesFactions.py'), '--mod-root', $ModRoot, '-v')
if ($ReferenceGameRoot) { $pythonArguments += @('--reference-game-root', $ReferenceGameRoot) }
& $pythonHost @pythonArguments
if ($LASTEXITCODE -ne 0) { throw "Faction contracts failed with exit code $LASTEXITCODE." }
if ($IncludeCampaign) {
 & $hostPath -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Run-UlyssesCampaignChecks.ps1') -ModRoot $ModRoot
 if ($LASTEXITCODE -ne 0) { throw "Campaign integration checks failed with exit code $LASTEXITCODE." }
}
Write-Output 'Faction offline checks passed. Native HOI4 acceptance was not run.'
