[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModRoot,

    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ModRoot).Path
$technologyRoot = Join-Path $root 'common\technologies'
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$dateRows = New-Object System.Collections.Generic.List[object]
$startYearRows = New-Object System.Collections.Generic.List[object]

function Add-TechError([string]$Message) { [void]$script:errors.Add($Message) }
function Add-TechWarning([string]$Message) { [void]$script:warnings.Add($Message) }
function Strip-Comment([string]$Line) {
    if ($null -eq $Line) { return '' }
    return ([regex]::Replace($Line, '#.*$', '')).Trim()
}

if (-not (Test-Path -LiteralPath $technologyRoot -PathType Container)) {
    Add-TechError "Technology directory is missing: $technologyRoot"
} else {
    foreach ($file in Get-ChildItem -LiteralPath $technologyRoot -File -Filter *.txt) {
        $lineNumber = 0
        foreach ($line in Get-Content -LiteralPath $file.FullName) {
            $lineNumber++
            $clean = Strip-Comment $line
            if ($clean -match '^\s*date\s*[<>]=?\s*"([^"]+)"') {
                $literal = $Matches[1]
                $dateRows.Add([pscustomobject]@{ Literal = $literal; File = $file.FullName; Line = $lineNumber })
                if ($literal -notmatch '^(\d{4})\.(\d{1,2})\.(\d{1,2})$') {
                    Add-TechError "Malformed technology date '$literal' ($($file.FullName):$lineNumber)"
                } else {
                    $year = [int]$Matches[1]
                    $month = [int]$Matches[2]
                    $day = [int]$Matches[3]
                    if ($year -lt 1900 -or $year -gt 2065 -or $month -lt 1 -or $month -gt 12 -or $day -lt 1 -or $day -gt 31) {
                        Add-TechError "Technology date '$literal' falls outside the 1900-2065 valid range or calendar bounds ($($file.FullName):$lineNumber)"
                    }
                }
            }
            if ($clean -match '^\s*start_year\s*=\s*(\d+)') {
                $year = [int]$Matches[1]
                $startYearRows.Add([pscustomobject]@{ Year = $year; File = $file.FullName; Line = $lineNumber })
                if ($year -lt 1900 -or $year -gt 2065) {
                    Add-TechError "Technology start_year '$year' falls outside the 1900-2065 audit horizon ($($file.FullName):$lineNumber)"
                }
            }
        }
    }
}

# Many technology IDs intentionally inherit base-game localization. This is a
# warning rather than a completeness failure; provenance is tracked in the canon docs.
Add-TechWarning 'Technology-name localization is not a completeness proof: inherited engine IDs may resolve from the base game. Review names and provenance before adding or renaming content.'

$summary = [ordered]@{
    TechnologyFiles = if (Test-Path -LiteralPath $technologyRoot -PathType Container) { @(Get-ChildItem -LiteralPath $technologyRoot -File -Filter *.txt).Count } else { 0 }
    DateLiterals = $dateRows.Count
    StartYearLiterals = $startYearRows.Count
    InvalidDates = @($errors | Where-Object { $_ -match 'technology date' }).Count
    InvalidStartYears = @($errors | Where-Object { $_ -match 'start_year' }).Count
    Errors = $errors.Count
    Warnings = $warnings.Count
}

if ($Json) {
    [pscustomobject]@{ Summary = $summary; Errors = @($errors); Warnings = @($warnings) } | ConvertTo-Json -Depth 5
} else {
    $summary.GetEnumerator() | ForEach-Object { '{0}={1}' -f $_.Key, $_.Value }
    if ($errors.Count -gt 0) { Write-Output 'ERRORS:'; $errors | ForEach-Object { "- $_" } }
    if ($warnings.Count -gt 0) { Write-Output 'WARNINGS:'; $warnings | ForEach-Object { "- $_" } }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
