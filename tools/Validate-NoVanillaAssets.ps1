[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModRoot,
    [Parameter(Mandatory = $true)]
    [string]$ReferenceGameRoot,
    [Parameter(Mandatory = $true)]
    [string]$BaselineRoot,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

function Get-NormalizedRelativePath {
    param([string]$Path)
    return ($Path -replace '\\', '/')
}

function Get-HashOrNull {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

if (-not (Test-Path -LiteralPath $ModRoot -PathType Container)) { throw "Mod root does not exist: $ModRoot" }
if (-not (Test-Path -LiteralPath $ReferenceGameRoot -PathType Container)) { throw "Reference game root does not exist: $ReferenceGameRoot" }
if (-not (Test-Path -LiteralPath $BaselineRoot -PathType Container)) { throw "Baseline root does not exist: $BaselineRoot" }

$inheritedMatches = New-Object System.Collections.Generic.List[string]
$newMatches = New-Object System.Collections.Generic.List[string]
$modFiles = Get-ChildItem -LiteralPath $ModRoot -File -Recurse
foreach ($file in $modFiles) {
    $relative = Get-NormalizedRelativePath ([IO.Path]::GetRelativePath((Resolve-Path -LiteralPath $ModRoot), $file.FullName))
    $referencePath = Join-Path $ReferenceGameRoot ($relative -replace '/', '\')
    if (-not (Test-Path -LiteralPath $referencePath -PathType Leaf)) { continue }
    $modHash = Get-HashOrNull $file.FullName
    $referenceHash = Get-HashOrNull $referencePath
    if ($modHash -ne $referenceHash) { continue }

    $baselinePath = Join-Path $BaselineRoot ($relative -replace '/', '\')
    $baselineHash = Get-HashOrNull $baselinePath
    if ($baselineHash -eq $referenceHash) {
        [void]$inheritedMatches.Add($relative)
    } else {
        [void]$newMatches.Add($relative)
    }
}

$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
if ($newMatches.Count -gt 0) {
    [void]$errors.Add("New files exactly matching the installed HOI4 reference: $($newMatches -join ', ')")
}

$descriptorPaths = @(
    (Join-Path $ModRoot '..\2985041246.mod'),
    (Join-Path $ModRoot 'descriptor.mod'),
    (Join-Path $ModRoot 'ProjectUlysses.mod')
)
foreach ($descriptor in $descriptorPaths) {
    if (-not (Test-Path -LiteralPath $descriptor -PathType Leaf)) {
        [void]$errors.Add("Missing descriptor: $descriptor")
        continue
    }
    $text = Get-Content -LiteralPath $descriptor -Raw
    if ($text -notmatch 'supported_version\s*=\s*"1\.19\.\*"') {
        [void]$errors.Add("Descriptor does not target supported_version=1.19.*: $descriptor")
    }
    if ($text -match '(?i)(remote_file_id|[A-Z]:\\[^\r\n"]*(?:Hearts of Iron IV|Project[- ]Ulysses))') {
        [void]$errors.Add("Descriptor contains a remote ID or developer-local absolute path: $descriptor")
    }
}

$allTextFiles = Get-ChildItem -LiteralPath $ModRoot -File -Recurse | Where-Object { $_.Extension -in @('.txt', '.gui', '.gfx', '.yml', '.mod') }
foreach ($file in $allTextFiles) {
    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($text -match '(?i)[A-Z]:\\[^\r\n"]*Hearts of Iron IV') {
        [void]$errors.Add("Mod text contains an absolute installed-game path: $($file.FullName)")
    }
}

$backgroundConfig = Join-Path $ModRoot 'common\frontend\backgrounds\base_backgrounds.txt'
if (Test-Path -LiteralPath $backgroundConfig -PathType Leaf) {
    $backgroundText = Get-Content -LiteralPath $backgroundConfig -Raw
    foreach ($match in [regex]::Matches($backgroundText, '(?m)^\s*(load_[0-9]+)\s*=\s*\{')) {
        $dds = Join-Path $ModRoot ("gfx\loadingscreens\{0}.dds" -f $match.Groups[1].Value)
        if (-not (Test-Path -LiteralPath $dds -PathType Leaf)) {
            [void]$errors.Add("Background config references a missing mod texture: $($match.Groups[1].Value).dds")
        }
        $small = Join-Path $ModRoot ("gfx\loadingscreens\{0}_small.dds" -f $match.Groups[1].Value)
        if (-not (Test-Path -LiteralPath $small -PathType Leaf)) {
            [void]$warnings.Add("Background picker thumbnail is missing and remains runtime-unverified: $($match.Groups[1].Value)_small.dds")
        }
    }
}

$result = [ordered]@{
    Summary = [ordered]@{
        ModFiles = $modFiles.Count
        InheritedVanillaMatches = $inheritedMatches.Count
        NewVanillaMatches = $newMatches.Count
        Errors = $errors.Count
        Warnings = $warnings.Count
    }
    InheritedVanillaMatches = @($inheritedMatches | Sort-Object)
    NewVanillaMatches = @($newMatches | Sort-Object)
    Errors = @($errors)
    Warnings = @($warnings)
}

if ($Json) {
    $result | ConvertTo-Json -Depth 5
} else {
    $result.Summary.GetEnumerator() | ForEach-Object { '{0}={1}' -f $_.Key, $_.Value }
    if ($result.NewVanillaMatches.Count -gt 0) { 'NEW VANILLA MATCHES:'; $result.NewVanillaMatches | ForEach-Object { "- $_" } }
    if ($result.InheritedVanillaMatches.Count -gt 0) { 'INHERITED BASELINE MATCHES:'; $result.InheritedVanillaMatches | ForEach-Object { "- $_" } }
    if ($result.Warnings.Count -gt 0) { 'WARNINGS:'; $result.Warnings | ForEach-Object { "- $_" } }
    if ($result.Errors.Count -gt 0) { 'ERRORS:'; $result.Errors | ForEach-Object { "- $_" } }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
