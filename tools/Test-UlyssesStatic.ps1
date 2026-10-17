[CmdletBinding()]
param(
    [string]$ModRoot = (Join-Path $PSScriptRoot '..\mod\2985041246'),
    [string]$ReferenceGameRoot
)

$ErrorActionPreference = 'Stop'
$scriptHost = if ($PSVersionTable.PSEdition -eq 'Core') { Join-Path $PSHOME 'pwsh.exe' } else { Join-Path $PSHOME 'powershell.exe' }
if (-not (Test-Path -LiteralPath $scriptHost -PathType Leaf)) { throw "Could not locate the current PowerShell host executable: $scriptHost" }
$validator = Join-Path $PSScriptRoot 'Validate-UlyssesMap.ps1'
$arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $validator, '-ModRoot', $ModRoot, '-Json')
if ($ReferenceGameRoot) { $arguments += @('-ReferenceGameRoot', $ReferenceGameRoot) }
$jsonText = (& $scriptHost @arguments | Out-String)
$validatorExitCode = $LASTEXITCODE
if ($validatorExitCode -ne 0) {
    Write-Error "Static map validator exited with code $validatorExitCode.`n$jsonText"
    exit $validatorExitCode
}
$report = $jsonText | ConvertFrom-Json

$failures = New-Object System.Collections.Generic.List[string]
foreach ($property in @(
    @{ Name = 'Errors'; Expected = 0 },
    @{ Name = 'UnassignedNonLakeLandDefinitions'; Expected = 0 },
    @{ Name = 'ExtraRasterColors'; Expected = 0 },
    @{ Name = 'OutOfBoundsBuildingCoordinates'; Expected = 0 },
    @{ Name = 'InvalidBuildingProvinceAssociations'; Expected = 0 },
    @{ Name = 'OutOfBoundsUnitStackCoordinates'; Expected = 0 }
)) {
    $actual = [int]$report.Summary.($property.Name)
    if ($actual -ne $property.Expected) {
        [void]$failures.Add("$($property.Name) expected $($property.Expected), got $actual")
    }
}

$continuationEvent = Join-Path $ModRoot 'events\ac_world_events.txt'
if (-not (Test-Path -LiteralPath $continuationEvent -PathType Leaf)) {
    [void]$failures.Add('events/ac_world_events.txt is missing')
} elseif ((Get-Content -LiteralPath $continuationEvent -Raw) -notmatch '(?s)id\s*=\s*world_event\.2.*?set_global_flag\s*=\s*ac_continuation_active') {
    [void]$failures.Add('world_event.2 does not set ac_continuation_active')
}

$report.Summary.PSObject.Properties | ForEach-Object { '{0}={1}' -f $_.Name, $_.Value }
if ($report.Warnings.Count -gt 0) {
    Write-Output 'WARNINGS:'
    $report.Warnings | ForEach-Object { "- $_" }
}
if ($report.Notes.Count -gt 0) {
    Write-Output 'NOTES:'
    $report.Notes | ForEach-Object { "- $_" }
}
if ($failures.Count -gt 0) {
    Write-Error ("Static regression checks failed:`n- " + ($failures -join "`n- "))
    exit 1
}

$belkanLocalization = Join-Path $ModRoot 'localisation\english\country_BLK_continuation_l_english.yml'
if (Test-Path -LiteralPath $belkanLocalization -PathType Leaf) {
    $bytes = [IO.File]::ReadAllBytes($belkanLocalization)
    if ($bytes.Length -lt 3 -or $bytes[0] -ne 0xEF -or $bytes[1] -ne 0xBB -or $bytes[2] -ne 0xBF) {
        Write-Error "Belkan continuation localization is missing a UTF-8 BOM: $belkanLocalization"
        exit 1
    }
} else {
    Write-Error "Belkan continuation localization is missing: $belkanLocalization"
    exit 1
}

$referenceValidator = Join-Path $PSScriptRoot 'Validate-UlyssesReferences.ps1'
$referenceJson = (& $scriptHost -NoProfile -ExecutionPolicy Bypass -File $referenceValidator -ModRoot $ModRoot -Json | Out-String)
$referenceExitCode = $LASTEXITCODE
if ($referenceExitCode -ne 0) {
    Write-Error "Reference validator exited with code $referenceExitCode.`n$referenceJson"
    exit $referenceExitCode
}
$referenceReport = $referenceJson | ConvertFrom-Json
Write-Output "Reference audit: $($referenceReport.Summary.FocusDefinitions) focus definitions, $($referenceReport.Summary.EventDefinitions) event definitions, $($referenceReport.Summary.Warnings) warnings."
foreach ($property in @('DuplicateEventDefinitions', 'MalformedEventReferences')) {
    if ([int]$referenceReport.Summary.$property -ne 0) {
        Write-Error "Reference audit regression: $property expected 0, got $($referenceReport.Summary.$property)."
        exit 1
    }
}

Write-Output 'Static regression checks passed.'
exit 0
